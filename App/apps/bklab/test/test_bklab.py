#!/usr/bin/env python3
# BK Lab host tests: the app built for the computer against the mock API of
# App/apps/host_mock.h and a mock BK4819 (128 registers in RAM). The list,
# the bit editor, protected registers, the restore at exit, every USB
# command. Mockups: test/out/*.png.
#
#   python3 App/apps/bklab/test/test_bklab.py
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(APP))
import host_test as ht  # noqa: E402
from host_test import check, press, script  # noqa: E402

NAME = "bklab"


def Run(s, **kw):
    r = ht.Run(APP, NAME, s, **kw)
    r.regs = [[int(x, 16) for x in l.split()[1:]] for l in r.lines if l.startswith("REGS")]
    r.writes, r.wat = [], []                # all writes; those made before each STATE
    for l in r.lines:
        if l.startswith("BKW "):
            r.writes.append((int(l.split()[1], 16), int(l.split()[2], 16)))
        elif l.startswith("STATE "):
            r.wat.append(list(r.writes))
    r.out = [l for l in r.tx.decode().split("\r\n") if l]
    return r


def tests():
    print("list and bit editor")
    r = Run(script("wait 50", "press 1", "press DOWN", "press DOWN", "press DOWN", "wait 50", "state",
                   "press 7", *["press DOWN"] * 18, "wait 50", "state",
                   "press 0", "press UP", "wait 50", "state"))
    check("1 jumps to 0x10, DOWN x3: 0x13", r.states[0]["sel"] == 0x13, r.states[0])
    check("past 0x7F: wraps to 0x00, the list stays in range",
          r.states[1]["sel"] == 0x02 and r.states[1]["top"] <= 0x02, r.states[1])
    check("UP from 0x00: 0x7F, the last six rows shown", r.states[2]["sel"] == 0x7F and r.states[2]["top"] == 0x7A,
          r.states[2])
    r = Run(script("wait 50", "press 1", "press DOWN", "press DOWN", "press DOWN", "press MENU", "wait 50", "state",
                   "press DOWN", "press DOWN", "press DOWN", "press DOWN", "press DOWN", "press DOWN", "press MENU",
                   "wait 50", "state", "press F", "wait 50", "state", "press EXIT", "press EXIT", "wait 50", "state"))
    check("MENU on 0x13: the editor with the chip's value 03DF", r.states[0]["view"] == 1
          and r.states[0]["edit"] == 0x03DF, r.states[0])
    check("cursor to bit 9, MENU flips it: 01DF, not yet written", r.states[1]["edit"] == 0x01DF
          and r.states[1]["cur"] == 6 and not r.wat[1], (r.states[1], r.wat[1]))
    check("F writes it (with a beep)", r.wat[2] == [(0x13, 0x01DF)] and r.regs[2][0x13] == 0x01DF
          and (1500, 40) in r.tones, r.wat[2])
    check("at exit the launch value 03DF is written back", r.writes == [(0x13, 0x01DF), (0x13, 0x03DF)], r.writes)
    r = Run(script("wait 50", "press 3", "press MENU", "wait 50", "press MENU", "press F", "wait 50", "state",
                   "press F", "wait 50", "state", "press STAR", "wait 50", "state"))
    check("0x30 (TX enables) is protected: the first F only arms", r.states[0]["armed"] == 1 and not r.wat[0]
          and (600, 80) in r.tones, r.states[0])
    check("F again writes", r.writes and r.writes[0] == (0x30, 0x3FF1), r.writes)
    check("* takes the chip's value back into the editor", r.states[2]["edit"] == 0x3FF1, r.states[2])
    r = Run(script("wait 50", "press 3", "press MENU", "press MENU", "press F", "press DOWN", "press F",
                   "wait 50", "state"))
    check("another key disarms: F after it arms again", not r.wat[0] and r.last["armed"] == 1, (r.wat, r.last))

    print("USB")
    r = Run(script("host 1", "wait 50", "rx r 13\\r", "rx r 10 3\\r", "rx w 13 3d9\\r", "rx w 30 0\\r",
                   "rx w! 30 bff0\\r", "rx s\\r", "rx d\\r", "rx x 1\\r", "rx r 99\\r", "rx /echo off\\r",
                   "wait 100", "state", "rx geri\\r", "wait 50", "state"))
    o = r.out
    check("banner", o[0] == "# BK Lab 1.0 ready", o[:1])
    check("r 13 -> 13=03DF; r 10 3 -> three", o[1] == "13=03DF" and o[2:5] == ["10=1010", "11=1011", "12=1012"], o[1:5])
    check("w 13 3d9 writes, read back", o[5] == "13=03D9" and r.states[0] and r.regs[0][0x13] == 0x03D9, o[5])
    check("w 30 refused (protected), w! 30 writes", o[6].startswith("! korumali") and o[7] == "30=BFF0", o[6:8])
    check("s: RSSI -96.5, noise 12, glitch 3", o[8] == "RSSI -96.5  Gr 12  Gl 3", o[8])
    check("d: 16 lines of 8", o[9] == "00: 1000 1001 1002 1003 1004 1005 1006 1007" and o[24].startswith("78:")
          and len(o[9].split()) == 9, (o[9], o[24]))
    check("unknown command and register 0x99: the help line", o[25].startswith("! komut") and o[26].startswith("! komut"),
          o[25:27])
    check("/echo off answered (uvterm.py works)", o[27] == "# echo off", o[27:])
    check("geri: both written registers back", o[-1] == "# geri yuklendi 2" and r.regs[1][0x13] == 0x03DF
          and r.regs[1][0x30] == 0xBFF1, (o[-1], hex(r.regs[1][0x13])))
    r = Run(script("host 1", "wait 50", "rx m 67 250\\r\\n", "wait 1100", "reg 67 0100", "wait 400", "rx x\\r",
                   "wait 600"))
    mon = [l for l in r.out if l.startswith("67=")]
    check("m 67 250: every 250 ms, follows the register, any byte stops it",
          5 <= len(mon) <= 7 and mon[0] == "67=007F" and mon[-1] == "67=0100", mon)


def mockups():
    Run(script("host 1", "wait 50", "rx w 13 3d9\\r", "press 1", "press DOWN", "press DOWN", "press DOWN",
               "wait 250", "shot liste"))
    Run(script("wait 50", "press 3", "press MENU", "press DOWN", "press DOWN", "press MENU", "wait 50", "press F",
               "wait 50", "shot bitler"))
    for name in ("liste", "bitler"):
        path = ht.png(APP, name)
        if path:
            print(f"  mockup {os.path.relpath(path, ht.ROOT)}")


if __name__ == "__main__":
    ht.build(APP, NAME)
    tests()
    mockups()
    ht.finish()
