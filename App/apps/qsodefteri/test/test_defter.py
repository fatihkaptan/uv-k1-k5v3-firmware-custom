#!/usr/bin/env python3
# QSO Defteri host tests: the app built for the computer against the mock API
# of App/apps/host_mock.h. A contact typed on the keypad, the VFO frequency and
# mode, the clock (from the computer, from the keypad, lost after a restart),
# dupes, delete, the full log, the CSV, and the log kept across restarts.
#
#   python3 App/apps/qsodefteri/test/test_defter.py
import calendar, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(APP))
import host_test as ht  # noqa: E402
from host_test import check, press, script  # noqa: E402

NAME = "qsodefteri"


def Run(s, **kw):
    r = ht.Run(APP, NAME, s, **kw)
    r.qsos = []
    cur = None
    for l in r.lines:
        if l.startswith("STATE "):
            cur = []
            r.qsos.append(cur)
        elif l.startswith("QSO ") and cur is not None:
            f = l[4:].split(",")
            cur.append((f[0], int(f[1]), int(f[2]), int(f[3]), int(f[4]), int(f[5])))
    r.save = next((l[5:] for l in r.lines if l.startswith("SAVE ")), None)
    return r


# "TA2ABC": T (8), A (2), 2 (hold 2), A (2), B (2 2), C (2 2 2)
TA2ABC = [*press(8), "wait 1000", *press(2), "wait 1000", "down 2", "wait 800", "up", "wait 100",
          *press(2), "wait 1000", *press(2, 2), "wait 1000", *press(2, 2, 2), "wait 1000"]
NEW = ["press MENU", "wait 50", *TA2ABC, "press DOWN", *press(5, 7), "press DOWN", *press(5, 5), "wait 50"]
UNIX = calendar.timegm((2026, 11, 4, 14, 32, 0))


def kept(save, extra=None):
    blob = bytearray(open(os.path.join(APP, f"{NAME}_assets.bin"), "rb").read())
    blob[-1024:] = bytes.fromhex(save) if save else extra
    path = os.path.join(APP, "test", "out", "kept_assets.bin")
    open(path, "wb").write(blob)
    return path


def tests():
    print("a contact")
    r = Run(script("wait 50", *NEW, "state", "press MENU", "wait 50", "state"))
    check("callsign by multi-tap with a held digit: TA2ABC", r.states[0]["call"] == "TA2ABC", r.states[0])
    check("reports typed: 57 sent, 55 received", r.states[0]["rs"] == 57 and r.states[0]["rr"] == 55, r.states[0])
    check("MENU logs it: VFO 145.500 MHz, FM, no clock -> time 0",
          r.qsos[-1] == [("TA2ABC", 145500, 0, 57, 55, 0)] and r.last["view"] == 0, r.qsos[-1])
    check("a good beep", (1500, 80) in r.tones)
    r = Run(script("wait 50", "press MENU", "wait 50", "press MENU", "wait 50", "state"))
    check("no callsign: refused (low beep), still in the form", r.last["view"] == 1 and (300, 120) in r.tones, r.last)
    r = Run(script("af 7", "freq 12150000", "wait 50", "press MENU", "wait 50", "state"))
    check("mode from the AF output: AM on 121.500", r.last["mode"] == 1, r.last)
    r = Run(script("wait 50", "press MENU", *press(5), "wait 1000", "press DOWN", "press EXIT", "state",
                   "press UP", "press EXIT", "press EXIT", "state"))
    check("EXIT in a report: one digit off (59 -> 5)", r.states[0]["rs"] == 5, r.states[0])
    check("EXIT on an empty callsign: back to the list, nothing logged",
          r.states[1]["view"] == 0 and r.states[1]["n"] == 0, r.states[1])

    print("clock")
    r = Run(script("host 1", "wait 50", f"rx /saat {UNIX}\\r", "wait 2000", *NEW, "press MENU", "wait 50",
                   "rx /liste\\r", "wait 50", "state"))
    t = r.qsos[-1][0][2]
    check("from the computer: /saat, the contact stamped (+- 1 s)", abs(t - (UNIX + 2 + 7)) <= 3 and r.last["set"] == 1,
          (t - UNIX, r.last))
    lines = r.tx.decode().split("\r\n")
    check("/liste: CSV header, the contact, # tamam",
          "call,khz,unix,rst_s,rst_r,mode" in lines and f"TA2ABC,145500,{t},57,55,FM" in lines
          and "# tamam" in lines, lines)
    r = Run(script("wait 50", "press F", "press 1", "wait 50", *press(*"2611041432"), "press MENU", "wait 50", "state"))
    check("from the keypad: F+1, 2611041432, MENU -> 2026-11-04 14:32 UTC", abs(r.last["utc"] - UNIX) <= 3, r.last["utc"] - UNIX)
    r = Run(script("wait 50", "press F", "press 1", "wait 50", *press(*"2613041432"), "press MENU", "wait 50", "state"))
    check("month 13: refused", r.last["set"] == 0 and r.last["view"] == 2 and (300, 120) in r.tones, r.last)
    cfg = struct.pack("<BBxxIII", 0x51, 1, UNIX, 100000, 0).hex()
    r = Run(script("wait 50", "state"), cfg=cfg)
    check("the tick counter below the last exit (a restart): no clock", r.last["set"] == 0, r.last)
    cfg = struct.pack("<BBxxIII", 0x51, 1, UNIX, 0, 0).hex()
    r = Run(script("wait 3000", "state", "press EXIT", "wait 50"), cfg=cfg)
    check("same power-on: the clock still runs", abs(r.last["utc"] - (UNIX + 3)) <= 1, r.last)
    check("its last tick count saved", r.cfg and struct.unpack_from("<I", r.cfg, 8)[0] >= 3, r.cfg)

    print("list: dupes, delete, full, kept")
    r = Run(script("wait 50", *NEW, "press MENU", "wait 50", *NEW, "state", "press MENU", "wait 50",
                   "press F", "press 3", "wait 50", "state", "press 3", "wait 50", "state",
                   "press F", "press 0", "press 0", "wait 50", "state"))
    check("the same callsign again: flagged (2nd)", r.states[0]["dupes"] == 1, r.states[0])
    check("F+3 asks first", r.states[1]["n"] == 2 and r.states[1]["confirm"] == 3, r.states[1])
    check("3 again: deleted", r.states[2]["n"] == 1, r.states[2])
    check("F+0 0: all deleted", r.states[3]["n"] == 0, r.states[3])
    r = Run(script("wait 50", *NEW, "press MENU", "wait 50", "press EXIT", "wait 50"), env={"SAVEDUMP": "1"})
    r2 = Run(script("wait 50", "state"), assets=kept(r.save))
    check("the log kept across a restart", r2.qsos[-1] == [("TA2ABC", 145500, 0, 57, 55, 0)], r2.qsos)
    full = struct.pack("<HBBI", 0x5144, 50, 0, 0) + b"".join(
        struct.pack("<8sIIHH", f"TA{i:04d}".encode(), 145500, 0, 59, 59) for i in range(50))
    r = Run(script("wait 50", "press MENU", "wait 50", "state", *["press DOWN"] * 60, "wait 50", "state"),
            assets=kept(None, full + bytes(1024 - len(full))))
    check("50 contacts: a 51st is refused", r.states[0]["view"] == 0 and r.states[0]["n"] == 50, r.states[0])
    check("scrolling to the oldest", r.states[1]["sel"] == 49 and r.states[1]["top"] == 45, r.states[1])
    r = Run(script("host 1", "wait 50", *NEW, "press MENU", "wait 50", "rx /temizle\\r", "wait 50", "state"))
    check("/temizle from the computer empties the log", r.last["n"] == 0 and b"# tamam" in r.tx)


def mockups():
    s = script("host 1", "wait 50", f"rx /saat {UNIX}\\r", "wait 50",
               *NEW, "press MENU", "wait 50", "freq 43350000", *NEW[:1], *press(8), "wait 1000",
               *press(2), "wait 1000", *press(1), "wait 1000", *press(7, 7, 7), "wait 1000",
               *press(5, 5, 5), "wait 1000", "wait 50", "shot form",
               "press MENU", "wait 50", "shot liste")
    Run(s)
    for name in ("liste", "form"):
        path = ht.png(APP, name)
        if path:
            print(f"  mockup {os.path.relpath(path, ht.ROOT)}")


if __name__ == "__main__":
    ht.build(APP, NAME)
    tests()
    mockups()
    ht.finish()
