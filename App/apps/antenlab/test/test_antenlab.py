#!/usr/bin/env python3
# Anten Lab host tests: the app built for the computer against the mock API
# of App/apps/host_mock.h and a simulated antenna (test/host_antenlab.c:
# peak 70 degrees, -3 dB beamwidth 108 degrees, front/back 25 dB, -60 dBm).
# Both modes must find that pattern; plus the attenuator, the reference,
# the CSV export, the patterns kept across restarts. Mockups: test/out/*.png.
#
#   python3 App/apps/antenlab/test/test_antenlab.py
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(APP))
import host_test as ht  # noqa: E402
from host_test import check, press, script  # noqa: E402

NAME = "antenlab"
NOVAL = -32768


def Run(s, **kw):
    r = ht.Run(APP, NAME, s, **kw)
    r.cur = [[int(x) for x in l.split()[1:]] for l in r.lines if l.startswith("CUR")]
    r.ref = [[int(x) for x in l.split()[1:]] for l in r.lines if l.startswith("REF")]
    r.save = next((l[5:] for l in r.lines if l.startswith("SAVE ")), None)
    return r


STEP36 = [x for _ in range(36) for x in ("press MENU", "wait 300")]   # a measurement takes ~230 ms


def tests():
    print("ADIM: point, MENU, 36 times")
    r = Run(script("wait 50", *STEP36, "state"))
    st, cur = r.last, r.cur[-1]
    check("all 36 bearings measured", NOVAL not in cur and st["dir"] == 0, cur)
    check("beam at 70 +- 2 degrees (between the -3 dB points), -60.0 dBm",
          abs(st["beam"] - 700) <= 20 and st["pk"] == -240, st)
    check("front/back 25 dB", st["fb"] == 100, st)
    check("-3 dB beamwidth 108 +- 6 degrees (interpolated between 10-degree bins)",
          abs(st["bw"] - 1080) <= 60, st["bw"])
    check("half-dB resolution from REG_67 (not rssi_dbm's whole dB)", any(v % 4 for v in cur), cur)
    check("a beep per bearing, its pitch rising with the level",
          len(r.tones) == 36 and max(r.tones)[0] == r.tones[7][0], r.tones[:8])

    print("TUR: one even turn")
    r = Run(script("wait 50", "press 1", "wait 50", "state", "press MENU", "wait 1000", "state", "wait 3100", "state",
                   "wait 20500", "state"))
    check("TUR mode, 20 s by default", r.states[0]["mode"] == 1, r.states[0])
    check("countdown first", r.states[1]["phase"] == 1 and r.states[2]["phase"] == 2, r.states[1:3])
    st, cur = r.last, r.cur[-1]
    check("after the turn: every bin filled, back to idle", st["phase"] == 0 and NOVAL not in cur, (st, cur))
    check("beam at 70 +- 5 degrees (bins centred on their bearing)", abs(st["beam"] - 700) <= 50, st)
    check("front/back above 20 dB, beamwidth 108 +- 15 degrees",
          st["fb"] >= 80 and abs(st["bw"] - 1080) <= 150, (st["fb"], st["bw"]))
    beeps = [t for t in r.tones]
    check("3 countdown beeps, go, 3 quarter beeps, done",
          beeps[:4] == [(800, 60)] * 3 + [(1600, 120)] and beeps.count((1200, 40)) == 3 and beeps[-1] == (1500, 300),
          beeps)
    r = Run(script("wait 50", "press 1", "press MENU", "wait 6000", "press EXIT", "wait 50", "state"))
    check("EXIT during a turn: cancelled, nothing kept", r.last["phase"] == 0 and set(r.cur[-1]) == {NOVAL}, r.last)
    r = Run(script("wait 50", "press 1", "press 2", "press 2", "wait 50", "press 1", "press 2", "press 2", "wait 50",
                   "press EXIT", "wait 50"))
    check("turn time cycles 10 / 20 / 30 / 60 s, saved", r.cfg is not None and r.cfg[3] == 1, r.cfg)

    print("attenuator, reference, export, kept")
    r = Run(script("wait 50", "point 70", "press 3", "wait 300", "press MENU", "wait 300", "state"))
    check("6 dB attenuator: compensated, still -60.0 dBm", r.last["att"] == 1 and r.cur[-1][0] == -240, r.last)
    r = Run(script("host 1", "wait 50", *STEP36, "press 4", "wait 50", "state", "press 0", "wait 50",
                   "press 3", "press 3", "wait 300", *STEP36[:20], "state", "press F", "wait 50"), env={"SAVEDUMP": "1"})
    check("4: the pattern becomes the reference (shown)", r.states[0]["ref"] == 1 and r.ref[0] == r.cur[0], r.states[0])
    check("0 then a new half pattern, 15 dB attenuator: same values",
          r.cur[-1][:10] == r.ref[-1][:10] and r.cur[-1][10] == NOVAL, (r.cur[-1][:12], r.ref[-1][:12]))
    lines = r.tx.decode().split("\r\n")
    i = lines.index("derece,dBm,ref_dBm")
    rows = [l.split(",") for l in lines[i + 1:i + 37]]
    check("F: CSV of 36 bearings, both patterns, quarter dB",
          len(rows) == 36 and rows[7] == ["70", "-60.00", "-60.00"] and rows[11][1] == ""
          and float(rows[11][2]) == r.ref[-1][11] / 4, rows[6:12])
    blob = bytearray(open(os.path.join(APP, f"{NAME}_assets.bin"), "rb").read())
    blob[-1024:] = bytes.fromhex(r.save)
    kept = os.path.join(APP, "test", "out", "kept_assets.bin")
    open(kept, "wb").write(blob)
    r2 = Run(script("wait 50", "state"), assets=kept)
    check("both patterns back after a restart", r2.cur[-1] == r.cur[-1] and r2.ref[-1] == r.ref[-1])
    r = Run(script("host 1", "wait 50", "rx ?", "wait 50"))
    check("'?' from the computer asks for the CSV", b"derece,dBm,ref_dBm\r\n" in r.tx, r.tx[:60])
    check("banner on connection", r.tx.startswith(b"# Anten Lab 1.0 ready\r\n"), r.tx[:30])


def mockups():
    s = script("wait 50", *STEP36, "press 4", "wait 50", "press 0", "press 1", "press MENU", "wait 3100",
               "noise 1", "wait 20500", "wait 300", "shot desen")
    Run(s)
    s = script("wait 50", "press 1", "press MENU", "wait 3100", "wait 8000", "shot tur")
    Run(s)
    for name in ("desen", "tur"):
        path = ht.png(APP, name)
        if path:
            print(f"  mockup {os.path.relpath(path, ht.ROOT)}")


if __name__ == "__main__":
    ht.build(APP, NAME)
    tests()
    mockups()
    ht.finish()
