/* Host build of BK Lab against the mock app_api_t of ../../host_mock.h, with
 * a mock BK4819: 128 registers in RAM (REG_67 RSSI, REG_65 noise, REG_63
 * glitch preset), every write printed as BKW <reg> <value>.
 *
 * "state" prints: STATE view=N sel=N top=N cur=N edit=N armed=N mon=N, then
 * REGS <128 values, hex>. "reg <r> <v>" (hex) sets a register from outside. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define HOST_TEST 1
#define _Static_assert(...)   /* the API layout checks assume 32-bit pointers */
#include "../bklab_app.c"

static uint16_t chip[128];
static uint16_t bk_rd(uint8_t r) { return r < 128u ? chip[r] : 0; }
static void bk_wr(uint8_t r, uint16_t v) { printf("BKW %02X %04X\n", r, v); if (r < 128u) chip[r] = v; }
static int cmd(const char *c, const char *arg) {
    if (strcmp(c, "reg")) return 0;
    unsigned r, v;
    if (sscanf(arg, "%x %x", &r, &v) != 2 || r >= 128) return 0;
    chip[r] = (uint16_t)v;
    return 1;
}
static void mock_state(void) {
    printf("STATE view=%u sel=%u top=%u cur=%u edit=%u armed=%u mon=%u\n",
           g.view, g.sel, g.top, g.cur, g.edit, g.armed, g.mon);
    printf("REGS");
    for (int i = 0; i < 128; i++) printf(" %04X", chip[i]);
    printf("\n");
}
static void mock_quit(void) { g.quit = true; }

#include "../../host_mock.h"

int main(int argc, char **argv) {
    for (int i = 0; i < 128; i++) chip[i] = (uint16_t)(0x1000 + i);
    chip[0x30] = 0xBFF1; chip[0x13] = 0x03DF;
    chip[0x67] = 2 * (160 - 97) + 1;     /* -96.5 dBm */
    chip[0x65] = 12; chip[0x63] = 3;
    mock_bk_read = bk_rd;
    mock_bk_write = bk_wr;
    mock_cmd = cmd;
    return mock_main(argc, argv);
}
