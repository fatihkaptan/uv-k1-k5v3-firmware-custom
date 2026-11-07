/* Host build of Mors Okur against the mock app_api_t of ../../host_mock.h,
 * with a mock microphone: REG_64 follows a Morse pattern in time.
 *
 * Environment: PATTERN (".", "-", " " letter gap, "/" word gap), WPM (15),
 * START (ms, 500), LEVEL (tone, 1500), FLOOR (quiet, 200), NOISE (+-, 30),
 * HAND (% random length change of every element and gap, 0: a keyer),
 * LAG (ms: the level ramps between quiet and tone, 4), STEADY ("a,b": a
 * steady sound from a to b ms). Every BK4819 write is printed as
 * BK <reg> <value>.
 *
 * "state" prints STATE down=N dot=N sens=N mode=N wpm=N oto=N on=N peak=N lvl=N, then
 * TEXT <the five rows, joined by |> and PAT <the pattern being keyed>. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define HOST_TEST 1
#define TRACE(...) (getenv("TRACE") ? printf(__VA_ARGS__) : 0)
#define _Static_assert(...)   /* the API layout checks assume 32-bit pointers */
#include "../morsokur_app.c"

static uint32_t now;          /* host_mock.h's clock (a tentative definition) */
static int marks[4096][2], nmarks, level = 1500, quiet = 200, noise = 30, lag = 4, steady[2] = { -1, -1 };

static int env(const char *k, int d) { const char *v = getenv(k); return v && *v ? atoi(v) : d; }
static int jitter(int ms, int hand) { return hand ? ms + ms * (rand() % (2 * hand + 1) - hand) / 100 : ms; }

static void timeline(void) {
    const char *p = getenv("PATTERN");
    const int dot = 1200 / env("WPM", 15), hand = env("HAND", 0);
    int t = env("START", 500);
    srand(7);
    for (; p && *p && nmarks < 4096; p++) {
        if (*p == '.' || *p == '-') {
            int len = jitter(*p == '.' ? dot : 3 * dot, hand);
            marks[nmarks][0] = t; marks[nmarks][1] = t + len; nmarks++;
            t += len + jitter(dot, hand);
        } else if (*p == ' ') t += jitter(2 * dot, hand);           /* 1 + 2 = 3 dots */
        else if (*p == '/') t += jitter(6 * dot, hand);             /* 1 + 6 = 7 dots */
    }
    const char *s = getenv("STEADY");
    if (s) sscanf(s, "%d,%d", &steady[0], &steady[1]);
}

/* 1 inside a mark, else 0, ramped over LAG ms at both edges */
static double keyed(int t) {
    if (t >= steady[0] && t < steady[1]) return 1.0;
    for (int i = 0; i < nmarks; i++) {
        const int a = marks[i][0], b = marks[i][1];
        if (t < a) return 0.0;
        if (t < b) return lag && t - a < lag ? (double)(t - a) / lag : 1.0;
        if (lag && t - b < lag) return 1.0 - (double)(t - b) / lag;
    }
    return 0.0;
}
static uint16_t bk_rd(uint8_t r) {
    if (r != 0x64) return r == 0x31 ? 0x1234 : 0;
    const double k = keyed((int)now);
    int v = (int)(quiet + k * (level - quiet)) + (noise ? rand() % (2 * noise + 1) - noise : 0);
    return (uint16_t)(v < 0 ? 0 : v);
}
static void bk_wr(uint8_t r, uint16_t v) { printf("BK %02x %04x %u\n", r, v, now); }

static void mock_state(void) {
    printf("STATE down=%u dot=%u sens=%u mode=%u wpm=%u oto=%u on=%u peak=%u lvl=%u\n", g.down, g.dot, g.cfg.sens,
           g.cfg.mode, g.cfg.wpm, g.cfg.oto, g.on, g.peak, g.lvl);
    printf("TEXT ");
    for (unsigned r = 0; r < ROWS; r++) printf("%s%s", g.rows[r], r + 1u < ROWS ? "|" : "\n");
    printf("PAT %s\n", g.pat);
}
static void mock_quit(void) { g.quit = true; }

#include "../../host_mock.h"

int main(int argc, char **argv) {
    level = env("LEVEL", 1500); quiet = env("FLOOR", 200); noise = env("NOISE", 30); lag = env("LAG", 4);
    timeline();
    mock_bk_read = bk_rd;
    mock_bk_write = bk_wr;
    return mock_main(argc, argv);
}
