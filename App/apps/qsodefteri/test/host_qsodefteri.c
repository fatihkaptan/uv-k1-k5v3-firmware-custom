/* Host build of QSO Defteri against the mock app_api_t of ../../host_mock.h.
 * "af <n>" sets the BK4819 AF output the mode is read from (REG_47 11:8).
 *
 * "state" prints: STATE view=N n=N sel=N top=N field=N call=[..] rs=N rr=N
 * mode=N dupes=N set=N utc=N fn=N confirm=N, then QSO call,khz,t,rs,rr per
 * contact, oldest first. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define HOST_TEST 1
#define _Static_assert(...)   /* the API layout checks assume 32-bit pointers */
#include "../qsodefteri_app.c"

static unsigned af = 1;
static uint16_t bk(uint8_t r) { return r == 0x47 ? (uint16_t)(af << 8) : 0; }
static int cmd(const char *c, const char *arg) {
    if (!strcmp(c, "af")) { af = (unsigned)atoi(arg); return 1; }
    return 0;
}
static void mock_state(void) {
    printf("STATE view=%u n=%u sel=%u top=%u field=%u call=[%.8s] rs=%u rr=%u mode=%u dupes=%u set=%u utc=%u "
           "fn=%u confirm=%u\n", g.view, g.L->n, g.sel, g.top, g.field, g.f.call, g.f.rs & 0x3FFu, g.f.rr,
           g.f.rs >> 14, dupes(g.f.call), g.cfg.set, utc(), g.fn, g.confirm);
    for (unsigned i = 0; i < g.L->n; i++) {
        const qso_t *q = &g.L->q[i];
        printf("QSO %.8s,%u,%u,%u,%u,%u\n", q->call, q->khz, q->t, q->rs & 0x3FFu, q->rr, q->rs >> 14);
    }
}
static void mock_quit(void) { g.quit = true; }

#include "../../host_mock.h"

int main(int argc, char **argv) {
    mock_bk_read = bk;
    mock_cmd = cmd;
    return mock_main(argc, argv);
}
