#!/usr/bin/env python3
# qsodefteri.py tests: bands, ADIF writing (lengths in bytes, SSB submode,
# contacts without a time), and an end-to-end run against the QSO Defteri app
# (built for the computer, live on a pty): clock set, log fetched, emptied.
#
#   python3 tools/qsodefteri/test_qsodefteri_pc.py
import calendar, datetime, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import qsodefteri as qd  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + name + ("" if cond else f"  -> {detail}"))
    if not cond:
        FAILS.append(name)


def main():
    print("ADIF")
    check("bands", qd.band(145.5) == "2m" and qd.band(433.5) == "70cm" and qd.band(14.2) == "20m"
          and qd.band(446.0) == "70cm" and qd.band(100.0) is None)
    t = calendar.timegm((2026, 11, 4, 14, 32, 5))
    csv = ("call,khz,unix,rst_s,rst_r,mode\nTA2ABC,145500,%d,57,55,FM\nTA1XYZ/P,144300,%d,59,59,SSB\n"
           "YM2KA,433500,0,59,58,FM\n" % (t, t + 60))
    qsos = qd.parse_csv(csv)
    check("CSV read", len(qsos) == 3 and qsos[1]["call"] == "TA1XYZ/P", qsos)
    now = datetime.datetime(2026, 11, 5, 9, 0, tzinfo=datetime.timezone.utc)
    text, skipped = qd.adif(qsos, "ta2xx", "kn50tr", now=now)
    recs = qd.parse_adif(text)
    check("header: ADIF 3.1.4, <EOH>", "<ADIF_VER:5>3.1.4" in text and "<EOH>" in text)
    check("a contact without a time is left out (counted)", len(recs) == 2 and skipped == 1, (len(recs), skipped))
    check("fields of the first", recs[0] == {"CALL": "TA2ABC", "QSO_DATE": "20261104", "TIME_ON": "143205",
                                            "FREQ": "145.5", "BAND": "2m", "MODE": "FM", "RST_SENT": "57",
                                            "RST_RCVD": "55", "STATION_CALLSIGN": "TA2XX", "MY_GRIDSQUARE": "KN50tr"},
          recs[0])
    check("SSB with SUBMODE USB", recs[1]["MODE"] == "SSB" and recs[1]["SUBMODE"] == "USB" and recs[1]["FREQ"] == "144.3")
    text, skipped = qd.adif(qsos, untimed=t)
    check("--zamansiz gives it a time", skipped == 0 and len(qd.parse_adif(text)) == 3)

    e2e()
    if FAILS:
        sys.exit(f"{len(FAILS)} check(s) failed")
    print("all checks passed")


def e2e():
    print("end to end: qsodefteri.py <-> QSO Defteri (live, pty)")
    try:
        import pty, tty
        import serial  # noqa: F401
    except ImportError:
        print("  (pyserial or pty missing: skipped)")
        return
    apps = os.path.join(ROOT, "App", "apps")
    sys.path.insert(0, apps)
    import host_test as ht
    app = os.path.join(apps, "qsodefteri")
    ht.build(app, "qsodefteri")
    master, slave = pty.openpty()
    tty.setraw(slave)
    # the radio: a contact logged before the clock is set, then one after
    s = ["host 1", "wait 50", "press MENU", "wait 50", "press 8", "wait 1000", "press 2", "wait 1000",
         "press MENU", "wait 2500", "press MENU", "wait 50", "press 3", "wait 1000", "press MENU", "wait 4000", "state"]
    p = subprocess.Popen([os.path.join(app, "test", "out", "host_qsodefteri"), os.path.join(app, "qsodefteri_assets.bin")],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, cwd=app,
                         env=dict(os.environ, LIVE_FD=str(master)), pass_fds=(master,))
    p.stdin.write(ht.script(*s))
    p.stdin.close()
    import uvterm
    ser = uvterm.serial.Serial(os.ttyname(slave), 115200, timeout=0.05)
    radio = qd.Radio(ser)
    time.sleep(2.6)                       # the first contact is logged at ~2.6 s
    radio.set_clock()
    t_set = time.time()
    time.sleep(5.0)                       # the second at ~6.5 s
    qsos = qd.parse_csv(radio.fetch())
    radio.clear()
    out = p.communicate(timeout=30)[0]
    ser.close()
    os.close(master)
    os.close(slave)
    check("two contacts fetched: TA, then D", [q["call"] for q in qsos] == ["TA", "D"], qsos)
    if len(qsos) == 2:
        check("the first without a time, the second stamped by the clock set (+-3 s)",
              qsos[0]["unix"] == 0 and abs(qsos[1]["unix"] - (t_set + 3.9)) <= 3, (qsos, t_set))
    check("/temizle emptied the radio", "STATE view=0 n=0" in out, [l for l in out.splitlines() if l.startswith("STATE")])


if __name__ == "__main__":
    main()
