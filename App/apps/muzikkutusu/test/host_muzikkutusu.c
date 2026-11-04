/* Host build of Muzik Kutusu against the mock app_api_t of ../../host_mock.h.
 * Every BK4819 register write is printed as BK <reg> <value> <ms>, so the
 * test rebuilds the notes from REG_71 (pitch) and the MUTE lines (on / off).
 *
 * "state" prints: STATE view=N sel=N cur=N last=N src=N pos=N len=N tempo=N
 * oct=N vol=N song=N rec=N n=N sharp=N audio=N (0 off, 1 speaker, 2 TX) tx=N */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define HOST_TEST 1
#define _Static_assert(...)   /* the API layout checks assume 32-bit pointers */
#include "../muzikkutusu_app.c"

static uint32_t now;          /* host_mock.h's clock (a tentative definition) */
static void bk_write(uint8_t r, uint16_t v) { printf("BK %02x %04x %u\n", r, v, now); }

static void mock_state(void) {
    printf("STATE view=%u sel=%u cur=%u last=%u src=%u pos=%u len=%u tempo=%u oct=%u vol=%u song=%u "
           "rec=%u n=%u sharp=%u audio=%u tx=%u\n",
           g.view, g.sel, g.cur, g.last, g.src, g.pos, g.len, g.tempo, g.cfg.oct, g.cfg.vol, g.cfg.song,
           g.rec, g.R->n, g.sharp, g.audio, g.tx);
}
static void mock_quit(void) { g.quit = true; }

#include "../../host_mock.h"

int main(int argc, char **argv) {
    mock_bk_write = bk_write;
    return mock_main(argc, argv);
}
