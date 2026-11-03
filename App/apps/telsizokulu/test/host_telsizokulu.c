/* Host build of Telsiz Okulu against the mock app_api_t of ../../host_mock.h.
 *
 *   cc -std=gnu11 -I App -DENABLE_SMALL_BOLD -o test/out/host_telsizokulu \
 *      test/host_telsizokulu.c App/font.c
 *
 * "state" prints: STATE view=N sel=N n=N top=N in=[..] khz=N ant=N vfo=N
 * reveal=N qn=N score=N right=N chosen=N best=N, then Q [question] and
 * OPT [answer] x4 while a quiz question is on screen. */

#include <stdio.h>
#include <string.h>
#define HOST_TEST 1
#define _Static_assert(...)   /* the API layout checks assume 32-bit pointers */
#include "../telsizokulu_app.c"

static void mock_state(void) {
    printf("STATE view=%u sel=%u n=%u top=%u in=[%s] khz=%u ant=%u vfo=%u reveal=%u qn=%u score=%u "
           "right=%u chosen=%u best=%u\n",
           g.view, g.sel, g.n, g.top, g.in, g.khz, antKhz(), g.vfo, g.reveal, g.qn, g.score,
           g.right, g.chosen, g.cfg.best);
    if (g.view == V_QUIZ && g.qn < NQ) {
        printf("Q [%s]\n", g.Q->q);
        for (int k = 0; k < 4; k++) printf("OPT [%s]\n", g.Q->opt[k]);
    }
}
static void mock_quit(void) { g.quit = true; }

#include "../../host_mock.h"

int main(int argc, char **argv) { return mock_main(argc, argv); }
