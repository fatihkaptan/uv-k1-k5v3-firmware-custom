/* Host build of Anten Lab against the mock app_api_t of ../../host_mock.h,
 * with a simulated antenna: rssi_dbm() follows a known pattern for the
 * bearing the antenna points at, and the attenuator takes its dB off.
 *
 *   bearing: in ADIM the app's g.dir (the user points where it says), in TUR
 *   the elapsed share of the turn (a user turning evenly), else "point <deg>".
 *   pattern: -60 dBm x ((1 + cos(a - PEAK)) / 2)^3, floor 25 dB down
 *   (peak 70 degrees, -3 dB beamwidth 108.0 degrees, front/back 25 dB).
 *
 * "state" prints: STATE mode=N dir=N phase=N att=N ref=N live=N beam=N
 * (0.1 degree) pk=N fb=N bw=N (0.1 degree) corr=N, then CUR v x36 and REF
 * v x36 (quarter dB, -32768: none). */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define HOST_TEST 1
#define _Static_assert(...)   /* the API layout checks assume 32-bit pointers */
#include "../antenlab_app.c"

static uint32_t now;          /* host_mock.h's clock (a tentative definition) */
static double point = -1;     /* "point <deg>": a fixed bearing */
static int noise;

static double level(void) {
    double deg;
    if (point >= 0) deg = point;
    else if (g.phase == P_RUN) deg = 360.0 * (double)(now - g.t0) / (1000.0 * DUR[g.cfg.dur]);
    else deg = 10.0 * g.dir;
    const double gl = pow((1 + cos((deg - 70) * M_PI / 180)) / 2, 3);
    double db = 10 * log10(gl > 1e-9 ? gl : 1e-9);
    if (db < -25) db = -25;
    static const int att[4] = { 0, 6, 15, 27 };
    double v = -60 + db - att[g.cfg.att];
    if (noise) v += ((rand() % 5) - 2) * 0.5;
    return v;
}
/* the radio: REG_67 in half dB, rssi_dbm() = REG_67 / 2 - 160 (no band
 * correction here) */
static uint16_t simReg67(void) { return (uint16_t)lround(2 * (level() + 160)); }
static int16_t antenna(void) { return (int16_t)(simReg67() / 2 - 160); }
static uint16_t bk(uint8_t r) { return r == 0x67 ? simReg67() : 0; }
static int cmd(const char *c, const char *arg) {
    if (!strcmp(c, "point")) { point = atof(arg); return 1; }
    if (!strcmp(c, "noise")) { noise = atoi(arg); return 1; }
    return 0;
}

static void mock_state(void) {
    stat_t st;
    stats(g.S->cur, &st);
    printf("STATE mode=%u dir=%u phase=%u att=%u ref=%u live=%d beam=%d pk=%d fb=%d bw=%d corr=%d\n",
           g.cfg.mode, g.dir, g.phase, g.cfg.att, g.cfg.ref, g.live, st.beam, st.level, st.fb, st.bw, g.corr);
    printf("CUR"); for (unsigned i = 0; i < NB; i++) printf(" %d", g.S->cur[i]); printf("\n");
    printf("REF"); for (unsigned i = 0; i < NB; i++) printf(" %d", g.S->ref[i]); printf("\n");
}
static void mock_quit(void) { g.quit = true; }

#include "../../host_mock.h"

int main(int argc, char **argv) {
    mock_rssi = antenna;
    mock_bk_read = bk;
    mock_cmd = cmd;
    return mock_main(argc, argv);
}
