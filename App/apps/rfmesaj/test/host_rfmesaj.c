/* Host build of RF Mesaj against the mock app_api_t of ../../host_mock.h,
 * with a mock BK4819 FSK modem:
 *
 *   - a packet the app transmits is printed as AIR <144 hex digits> (the 36
 *     words written to REG_5F between the TX FIFO clear and TX enable);
 *   - "air <hex>" hands a packet to the receiver (delivered once RX is
 *     armed, all 36 words at "RX finished"); "crcerr 1" makes the next one
 *     fail the hardware CRC (REG_0B bit 4).
 *
 * "state" prints: STATE mode=N in=[..] waiting=N tries=N seq=N fn=N key=N
 * flags=N host=N rows=N, then one ROW [..] per history row. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define HOST_TEST 1
#define _Static_assert(...)   /* the API layout checks assume 32-bit pointers */
#include "../rfmesaj_app.c"

static uint16_t txw[64], rxw[36];
static int txn, txMode, txDone, rxArmed, rxn, rxi, crcErr, crcNow;

static void fsk_write(uint8_t r, uint16_t v) {
    if (r == 0x59) {
        if (v == 0x8068) { txn = 0; txMode = 1; }
        else if (v == 0x2868) {                       /* TX enable: on the air */
            txMode = 0; txDone = 1;
            printf("AIR ");
            for (int i = 0; i < txn; i++) printf("%02x%02x", txw[i] & 0xFF, txw[i] >> 8);
            printf("\n");
        } else if (v == 0x3068) rxArmed = 1;
        else if (v == 0x0068 && !txMode) rxArmed = 0;  /* BK4819_ResetFSK */
    } else if (r == 0x5F && txMode && txn < 64) txw[txn++] = v;
    else if (r == 0x02) txDone = 0;
}
static uint16_t fsk_read(uint8_t r) {
    const int pending = rxArmed && rxi < rxn;
    if (r == 0x0C) return (uint16_t)(txDone || pending);
    if (r == 0x02) return pending ? (uint16_t)(1u << 13) : 0;
    if (r == 0x5F) return rxi < rxn ? rxw[rxi++] : 0;
    if (r == 0x0B) { const int e = crcNow; crcNow = 0; return e ? 0x0010 : 0; }
    return 0;
}
static int fsk_cmd(const char *cmd, const char *arg) {
    if (!strcmp(cmd, "crcerr")) { crcErr = atoi(arg); return 1; }
    if (strcmp(cmd, "air")) return 0;
    for (int i = 0; i < 36; i++) {
        unsigned lo, hi;
        if (sscanf(arg + 4 * i, "%2x%2x", &lo, &hi) != 2) { fprintf(stderr, "bad air\n"); exit(2); }
        rxw[i] = (uint16_t)(lo | hi << 8);
    }
    rxn = 36; rxi = 0; crcNow = crcErr; crcErr = 0;
    return 1;
}

static void mock_state(void) {
    printf("STATE mode=%u in=[%.*s] waiting=%u tries=%u seq=%u fn=%u key=%u flags=%u host=%u rows=%u\n",
           mode(), g.inLen, g.b->in, g.waiting, g.tries, g.seq, g.fn, g.keyEntry, g.cfg.flags, g.host,
           g.count);
    for (uint8_t i = 0; i < g.count; i++) {
        const char *r = g.hist[(g.head - g.count + i) & (HROWS - 1u)];
        printf("ROW [%.*s]\n", (int)strnlen(r, COLS), r);
    }
}
static void mock_quit(void) { g.quit = true; }

#include "../../host_mock.h"

int main(int argc, char **argv) {
    mock_bk_read = fsk_read;
    mock_bk_write = fsk_write;
    mock_cmd = fsk_cmd;
    return mock_main(argc, argv);
}
