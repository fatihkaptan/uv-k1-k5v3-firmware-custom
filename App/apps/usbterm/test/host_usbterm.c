/* Host build of USB Term against the mock app_api_t of ../../host_mock.h
 * (script language, live pty mode and output there).
 *
 *   cc -std=gnu11 -I App -DENABLE_SMALL_BOLD -o test/out/host_usbterm \
 *      test/host_usbterm.c App/font.c
 *   test/out/host_usbterm usbterm_assets.bin [cfg-hex] < script
 *
 * "state" prints: STATE in=[..] rx=[..] rows=N scroll=N mode=N sound=N
 * echo=N host=N tap=N lost=N, then one ROW [..] line per history row. */

#include <stdio.h>
#include <string.h>
#define HOST_TEST 1
#define _Static_assert(...)   /* the API layout checks assume 32-bit pointers */
#include "../usbterm_app.c"

static void mock_state(void) {
    printf("STATE in=[%.*s] rx=[%.*s] rows=%u scroll=%u mode=%u sound=%u echo=%u host=%u tap=%u lost=%u\n",
           g.inLen, g.in, g.rxLen, g.rx, g.count, g.scroll, g.cfg.mode, g.cfg.sound,
           g.echo, g.host, g.tap, g.lost);
    for (uint8_t i = 0; i < g.count; i++) {
        const char *r = g.hist[(g.head - g.count + i) & (HROWS - 1u)];
        printf("ROW [%.*s]\n", (int)strnlen(r, COLS), r);
    }
}
static void mock_quit(void) { g.quit = true; }

#include "../../host_mock.h"

int main(int argc, char **argv) { return mock_main(argc, argv); }
