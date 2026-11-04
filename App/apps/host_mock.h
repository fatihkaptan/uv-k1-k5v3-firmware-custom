/* Copyright 2026 Fatih Kaptan
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 *     Unless required by applicable law or agreed to in writing, software
 *     distributed under the License is distributed on an "AS IS" BASIS,
 *     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *     See the License for the specific language governing permissions and
 *     limitations under the License.
 */

/*
 * host_mock.h - run an overlay app on a computer, for tests: a mock app_api_t
 * whose text services draw with the firmware's own fonts (App/font.c), driven
 * by a script. Used by usbterm/test and telsizokulu/test.
 *
 *   #define HOST_TEST 1
 *   #define _Static_assert(...)          // the layout checks assume 32-bit pointers
 *   #include "../myapp_app.c"
 *   static void mock_state(void) { ... }  // "state": print the app's state
 *   static void mock_quit(void)  { ... }  // end of script: make app_main return
 *   #include "../../host_mock.h"
 *   int main(int argc, char **argv) { return mock_main(argc, argv); }
 *
 *   cc -std=gnu11 -I App -DENABLE_SMALL_BOLD host_myapp.c App/font.c
 *   host_myapp <assets.bin> [cfg-hex] < script
 *
 * Time is simulated: delay_ms() and play_tone() advance it, and delay_ms()
 * runs the script until the next "wait". Script lines (# comments allowed):
 *
 *   wait <ms>        let the app run that long
 *   host <0|1>       a host has the USB port open (DTR) or not
 *   rx <text>        bytes from the host (C escapes \r \n \t \\ \xNN)
 *   lost             the next serial_ctl reports a lapped receive ring
 *   freq <10 Hz>     the RX VFO frequency (rx_freq)
 *   down <key>       key pressed and held (0-9 MENU UP DOWN EXIT STAR F PTT)
 *   up               all keys released
 *   press <key>      down for 60 ms, then up for 60 ms
 *   state            call mock_state()
 *   shot <name>      write test/out/<name>.raw (status line + frame buffer)
 *   txstate <n>      what tx_state() returns (0: transmitting allowed)
 *   call <callsign>  what boot_callsign() returns (TA2AAA)
 *   anything else    the harness's mock_cmd hook (e.g. "air <hex>")
 *
 * Output: TX <hex> per serial_write, TONE <hz> <ms>, LED <0|1>, SHOT <name>,
 * CFG <hex> (cfg_save), TXON / TXOFF (tx_set_params / tx_end), END (script
 * exhausted), QUIT (app_main returned).
 *
 * Live mode (LIVE_FD=<fd> in the environment, e.g. a pty master): the serial
 * port is that descriptor and delay_ms() really sleeps, so a program on the
 * other side talks to the app in real time.
 */

#ifndef APPS_HOST_MOCK_H
#define APPS_HOST_MOCK_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include "font.h"

static void mock_state(void);
static void mock_quit(void);

/* Optional hooks a harness sets before mock_main(): the BK4819 registers
 * (bk_read / bk_write), and script commands of its own (return 1 when the
 * command was handled). */
static uint16_t (*mock_bk_read)(uint8_t reg);
static void     (*mock_bk_write)(uint8_t reg, uint16_t v);
static int      (*mock_cmd)(const char *cmd, const char *arg);
static uint8_t  txDenied;        /* "txstate <n>": what tx_state() returns */
static char     bootCall[12] = "TA2AAA";

static uint8_t  fb[7][128], status[128];
static uint8_t  assets[4096];
static size_t   assetLen;
static uint8_t  cfgMem[16];
static uint32_t now;
static int      key = APP_KEY_INVALID;
static int      host;
static int      lostEvt;
static uint8_t  rxq[4096];
static size_t   rxHead, rxTail;
static uint16_t battery = 785;
static uint32_t rxFreq = 14550000u;
static uint32_t rng = 0x12345678u;
static uint32_t resume;          /* the script runs again at this time */
static int      done;            /* script exhausted */
static int      pendingUp;       /* "press": release the key at the next resume */
static int      liveFd = -1;

/* ---- display, as App/ui/helper.c draws it ---- */
static uint8_t *row(bool st, uint8_t y) { return st ? status : fb[y / 8]; }
static void px(bool st, uint8_t x, uint8_t y, bool fill) {
    if (x >= 128 || (!st && y >= 56) || (st && y >= 8)) return;
    uint8_t *b = &row(st, y)[x];
    if (fill) *b |= (uint8_t)(1u << (y % 8)); else *b &= (uint8_t)~(1u << (y % 8));
}
static void m_tiny(const char *s, uint8_t x, uint8_t y, bool st, bool fill) {
    for (; *s; s++, x += 4) {
        uint8_t c = (uint8_t)(*s - 0x20);
        for (int i = 0; i < 3; i++) {
            uint8_t p = gFont3x5[c][i];
            for (int j = 0; j < 6; j++, p >>= 1)
                if (p & 1) px(st, (uint8_t)(x + i), (uint8_t)(y + j), fill);
        }
    }
}
static void m_inverse(const char *s, uint8_t x, uint8_t line, bool st, bool fill, uint8_t end) {
    m_tiny(s, x, (uint8_t)(line * 8 + 1), st, fill);
    uint8_t *b = st ? status : fb[line];
    b[x - 2] ^= 0x3E;
    for (uint8_t i = (uint8_t)(x - 1); i < end; i++) b[i] ^= 0x7F;
    b[end] ^= 0x3E;
}
static void small(const char *s, uint8_t start, uint8_t end, uint8_t line, const uint8_t *font) {
    const size_t len = strlen(s);
    if (end > start) start = (uint8_t)(start + (((end - start) - len * 7u) + 1) / 2);
    for (size_t i = 0; i < len; i++) {
        if (s[i] <= ' ' || s[i] >= 127) continue;
        const unsigned index = (unsigned)(s[i] - ' ' - 1);
        uint16_t bit = (uint16_t)(index * FONT_SMALL_WIDTH * 7u);
        for (unsigned col = 0; col < FONT_SMALL_WIDTH; col++, bit += 7) {
            const unsigned x = start + i * 7u + 1u + col;
            const uint16_t packed = (uint16_t)(font[bit >> 3] | (font[(bit >> 3) + 1] << 8));
            if (x < 128) fb[line][x] = (uint8_t)((packed >> (bit & 7u)) & 0x7Fu);
        }
    }
}
static void m_normal(const char *s, uint8_t a, uint8_t b, uint8_t line) { small(s, a, b, line, gFontSmallPacked); }
static void m_bold(const char *s, uint8_t a, uint8_t b, uint8_t line) { small(s, a, b, line, gFontSmallBoldPacked); }
static void m_string(const char *s, uint8_t start, uint8_t end, uint8_t line, uint8_t width) {
    const size_t len = strlen(s);
    if (end > start) start = (uint8_t)(start + (((end - start) - len * width) + 1) / 2);
    for (size_t i = 0; i < len; i++) {
        const unsigned ofs = start + i * width;
        if (s[i] > ' ' && s[i] < 127 && ofs + 7 <= 128)
            FONT_DrawBigGlyph((uint8_t)(s[i] - ' ' - 1), fb[line] + ofs, fb[line + 1] + ofs);
    }
}
static void m_frequency(uint32_t f, uint8_t x, uint8_t line) {   /* as app_draw_frequency */
    char s[16];
    snprintf(s, sizeof s, "%u.%05u", f / 100000u, f % 100000u);
    if (x > 33) x = 33;
    if (f / 100000u >= 1000u) { m_string(s, x, 0, line, 8); return; }
    char *o = strchr(s, '.') + 4;
    m_normal(o, (uint8_t)(x + (o - s - 1) * 13 + 3), 0, (uint8_t)(line + 1));
    *o = '\0';
    uint8_t *p0 = fb[line] + x, *p1 = fb[line + 1] + x;
    for (char *c = s; *c; c++) {
        if (*c == '.') { p1[0] = p1[1] = p1[2] = 0x60; p0 += 3; p1 += 3; continue; }
        memcpy(p0 + 2, gFontBigDigits[*c - '0'], 10);
        memcpy(p1 + 2, gFontBigDigits[*c - '0'] + 10, 10);
        p0 += 13; p1 += 13;
    }
}
static void m_line(app_fb_t b, int16_t x1, int16_t y1, int16_t x2, int16_t y2, bool black) {
    (void)b;
    int dx = abs(x2 - x1), sx = x1 < x2 ? 1 : -1, dy = -abs(y2 - y1), sy = y1 < y2 ? 1 : -1, e = dx + dy;
    for (;;) {
        if (x1 >= 0 && y1 >= 0) px(false, (uint8_t)x1, (uint8_t)y1, black);
        if (x1 == x2 && y1 == y2) break;
        int e2 = 2 * e;
        if (e2 >= dy) { e += dy; x1 = (int16_t)(x1 + sx); }
        if (e2 <= dx) { e += dx; y1 = (int16_t)(y1 + sy); }
    }
}
static void m_clear(void) { memset(fb, 0, sizeof fb); }
static void m_status_clear(void) { memset(status, 0, sizeof status); }
static void m_battery(void) {     /* a plain battery outline at the right edge */
    for (int x = 114; x < 127; x++) status[x] |= 0x41;
    status[113] |= 0x7F; status[126] |= 0x7F; status[127] |= 0x1C;
    for (int x = 115; x < 124; x++) status[x] |= 0x3E;
}
static void m_blit(void) {}

/* ---- the script ---- */
static int keyCode(const char *s) {
    static const char *names[] = { "MENU", "UP", "DOWN", "EXIT", "STAR", "F", "PTT" };
    if (s[0] >= '0' && s[0] <= '9' && !s[1]) return s[0] - '0';
    for (int i = 0; i < 7; i++) if (!strcmp(s, names[i])) return APP_KEY_MENU + i;
    fprintf(stderr, "bad key %s\n", s); exit(2);
}
static void unescape(const char *s) {
    while (*s) {
        uint8_t c = (uint8_t)*s++;
        if (c == '\\' && *s) {
            char e = *s++;
            if (e == 'r') c = '\r'; else if (e == 'n') c = '\n';
            else if (e == 't') c = '\t'; else if (e == '\\') c = '\\';
            else if (e == 'x') { char h[3] = { s[0], s[1], 0 }; c = (uint8_t)strtol(h, NULL, 16); s += 2; }
        }
        rxq[rxTail++ % sizeof rxq] = c;
    }
}
static void shot(const char *name) {
    char path[256];
    snprintf(path, sizeof path, "test/out/%s.raw", name);
    FILE *f = fopen(path, "wb");
    if (!f) { perror(path); exit(2); }
    fwrite(status, 1, sizeof status, f);
    fwrite(fb, 1, sizeof fb, f);
    fclose(f);
    printf("SHOT %s\n", name);
}
static void script(void) {
    char line[1024];
    while (!done && now >= resume) {
        if (pendingUp) { pendingUp = 0; key = APP_KEY_INVALID; resume = now + 60; continue; }
        if (!fgets(line, sizeof line, stdin)) { done = 1; printf("END\n"); break; }
        line[strcspn(line, "\n")] = 0;
        char *arg = strchr(line, ' ');
        if (arg) *arg++ = 0; else arg = line + strlen(line);
        if (!line[0] || line[0] == '#') continue;
        if (!strcmp(line, "wait")) resume = now + (uint32_t)atoi(arg);
        else if (!strcmp(line, "host")) host = atoi(arg);
        else if (!strcmp(line, "rx")) unescape(arg);
        else if (!strcmp(line, "lost")) lostEvt = 1;
        else if (!strcmp(line, "freq")) rxFreq = (uint32_t)strtoul(arg, NULL, 10);
        else if (!strcmp(line, "down")) key = keyCode(arg);
        else if (!strcmp(line, "up")) key = APP_KEY_INVALID;
        else if (!strcmp(line, "press")) { key = keyCode(arg); resume = now + 60; pendingUp = 1; }
        else if (!strcmp(line, "state")) mock_state();
        else if (!strcmp(line, "shot")) shot(arg);
        else if (!strcmp(line, "txstate")) txDenied = (uint8_t)atoi(arg);
        else if (!strcmp(line, "call")) snprintf(bootCall, sizeof bootCall, "%s", arg);
        else if (!mock_cmd || !mock_cmd(line, arg)) { fprintf(stderr, "bad command %s\n", line); exit(2); }
    }
}

/* ---- mock services ---- */
static uint8_t  m_get_key(void) { return (uint8_t)key; }
static void     m_delay(uint32_t ms) {
    if (liveFd >= 0) usleep(ms * 1000u);
    now += ms;
    script();
    if (done) mock_quit();       /* end of the script: leave */
}
static void     m_tone(uint16_t hz, uint16_t ms) { printf("TONE %u %u\n", hz, ms); now += ms; }
static void     m_led(bool on) { printf("LED %d\n", on); }
static uint32_t m_ticks(void) { return now - now % 10u; }     /* 10 ms resolution */
static uint32_t m_rand(void) { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng; }
static uint16_t m_asset(uint16_t off, void *buf, uint16_t len) {
    if (off >= assetLen) return 0;
    if (len > assetLen - off) len = (uint16_t)(assetLen - off);
    memcpy(buf, assets + off, len);
    return len;
}
static void     m_cfg_load(uint8_t *b, uint8_t n) { memcpy(b, cfgMem, n); }
static void     m_cfg_save(const uint8_t *b, uint8_t n) {
    printf("CFG ");
    for (uint8_t i = 0; i < n; i++) printf("%02x", b[i]);
    printf("\n");
}
static void     m_nop(void) {}
static char    *m_u32(char *d, uint32_t u) { return d + sprintf(d, "%u", u); }
static char    *m_i32(char *d, int32_t v) { return d + sprintf(d, "%d", v); }
static uint64_t m_uidivmod(uint32_t n, uint32_t d) {
    return d ? ((uint64_t)(n % d) << 32) | (n / d) : ((uint64_t)n << 32);
}
static uint64_t m_idivmod(int32_t n, int32_t d) {
    if (!d) return (uint64_t)(uint32_t)n << 32;
    return ((uint64_t)(uint32_t)(n % d) << 32) | (uint32_t)(n / d);
}
static uint32_t m_freq(void) { return rxFreq; }
static int16_t  m_rssi(void) { return -97; }
static int8_t   m_nav(uint8_t k) { return k == APP_KEY_UP ? 1 : k == APP_KEY_DOWN ? -1 : 0; }
static uint16_t m_bk_read(uint8_t r) { return mock_bk_read ? mock_bk_read(r) : 0; }
static void     m_bk_write(uint8_t r, uint16_t v) { if (mock_bk_write) mock_bk_write(r, v); }
static uint8_t  m_tx_state(void) { return txDenied; }
static void     m_tx_params(void) { printf("TXON\n"); }
static void     m_tx_end(void) { printf("TXOFF\n"); }
static void     m_boot_call(char *buf, uint8_t len) { snprintf(buf, len, "%s", bootCall); }
static uint16_t m_serial_read(uint8_t port, void *buf, uint16_t len) {
    uint16_t n = 0;
    if (port != APP_SERIAL_USB) return 0;
    while (n < len && rxHead != rxTail) ((uint8_t *)buf)[n++] = rxq[rxHead++ % sizeof rxq];
    if (liveFd >= 0 && n < len) {
        ssize_t k = read(liveFd, (uint8_t *)buf + n, len - n);
        if (k > 0) n = (uint16_t)(n + k);
    }
    return n;
}
static bool     m_serial_write(uint8_t port, const void *buf, uint16_t len) {
    if (port != APP_SERIAL_USB || !host) return false;
    printf("TX ");
    for (uint16_t i = 0; i < len; i++) printf("%02x", ((const uint8_t *)buf)[i]);
    printf("\n");
    if (liveFd >= 0 && write(liveFd, buf, len) != (ssize_t)len) return false;
    return true;
}
static uint8_t  m_serial_ctl(uint8_t port, uint32_t baud) {
    (void)baud;
    if (port != APP_SERIAL_USB) return 0;
    uint8_t st = APP_SERIAL_OK | (host ? APP_SERIAL_HOST : 0) | (lostEvt ? APP_SERIAL_LOST : 0);
    lostEvt = 0;
    return st;
}

static int mock_main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s <assets.bin> [cfg-hex]\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "rb");
    if (!f) { perror(argv[1]); return 2; }
    assetLen = fread(assets, 1, sizeof assets, f);
    fclose(f);
    memset(cfgMem, 0xFF, sizeof cfgMem);
    if (argc > 2)
        for (int i = 0; i < 16 && argv[2][2 * i] && argv[2][2 * i + 1]; i++) {
            char h[3] = { argv[2][2 * i], argv[2][2 * i + 1], 0 };
            cfgMem[i] = (uint8_t)strtol(h, NULL, 16);
        }
    setvbuf(stdout, NULL, _IOLBF, 0);
    if (getenv("LIVE_FD")) {
        liveFd = atoi(getenv("LIVE_FD"));
        fcntl(liveFd, F_SETFL, fcntl(liveFd, F_GETFL) | O_NONBLOCK);
    }
    if (getenv("SEED")) rng = (uint32_t)strtoul(getenv("SEED"), NULL, 0) | 1u;

    static const char edition[] = "Labs", version[] = "v6.3.0";
    static app_api_t api;
    api.abi_major = APP_ABI_MAJOR; api.api_level = APP_API_LEVEL; api.api_size = sizeof api;
    api.fb = fb; api.status_line = status;
    api.display_clear = m_clear; api.status_clear = m_status_clear;
    api.draw_line = m_line;
    api.print_tiny = m_tiny; api.print_inverse = m_inverse;
    api.print_normal = m_normal; api.print_bold = m_bold; api.print_string = m_string;
    api.draw_frequency = m_frequency;
    api.blit_full = m_blit; api.blit_status = m_blit;
    api.get_key = m_get_key; api.nav_dir = m_nav; api.delay_ms = m_delay;
    api.play_tone = m_tone; api.led = m_led;
    api.rssi_dbm = m_rssi; api.rx_freq = m_freq;
    api.cfg_load = m_cfg_load; api.cfg_save = m_cfg_save;
    api.draw_battery = m_battery; api.battery_sample = m_nop;
    api.backlight_on = m_nop; api.backlight_update = m_nop;
    api.ticks_ms = m_ticks; api.rand32 = m_rand; api.asset_read = m_asset;
    api.uidivmod = m_uidivmod; api.idivmod = m_idivmod;
    api.sys_edition = edition; api.sys_version = version;
    api.sys_battery_voltage = &battery;
    api.append_i32 = m_i32; api.append_u32 = m_u32;
    api.serial_read = m_serial_read; api.serial_write = m_serial_write;
    api.serial_ctl = m_serial_ctl;
    api.bk_read = m_bk_read; api.bk_write = m_bk_write;
    api.tx_state = m_tx_state; api.tx_set_params = m_tx_params; api.tx_end = m_tx_end;
    api.boot_callsign = m_boot_call;

    script();
    app_main(&api);
    printf("QUIT\n");
    return 0;
}

#endif /* APPS_HOST_MOCK_H */
