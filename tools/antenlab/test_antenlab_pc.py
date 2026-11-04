#!/usr/bin/env python3
# antenlab.py tests: CSV parsing, the pattern numbers (the same as the app's),
# the SVG, and an end-to-end fetch from the Anten Lab app itself (built for
# the computer, live on a pty, measuring the simulated antenna).
#
#   python3 tools/antenlab/test_antenlab_pc.py
import math, os, subprocess, sys, time
import xml.dom.minidom

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import antenlab  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + name + ("" if cond else f"  -> {detail}"))
    if not cond:
        FAILS.append(name)


def yagi(peak=70, level=-60.0):
    out = []
    for k in range(36):
        g = ((1 + math.cos(math.radians(10 * k - peak))) / 2) ** 3
        out.append(round(max(10 * math.log10(max(g, 1e-9)), -25) + level, 2))
    return out


def main():
    print("numbers")
    s = antenlab.stats(yagi())
    check("beam 70, -60 dBm, front/back 25 dB, width 108 +- 6",
          abs(s["beam"] - 70) < 2 and s["level"] == -60 and abs(s["fb"] - 25) < 0.01 and abs(s["width"] - 108) <= 6, s)
    p = yagi(355)
    s = antenlab.stats(p)
    check("a beam across north (355)", abs((s["beam"] - 355 + 180) % 360 - 180) < 2, s)
    p = yagi()
    p[25] = None
    check("a gap at the back: no front/back", antenlab.stats(p)["fb"] is None)
    check("nothing measured", antenlab.stats([None] * 36) is None)

    print("CSV and SVG")
    csv = "derece,dBm,ref_dBm\n" + "\n".join(f"{10 * k},{v:.2f}," + ("-70.00" if k == 3 else "")
                                             for k, v in enumerate(yagi())) + "\n"
    d = antenlab.parse_csv(csv)
    check("CSV read: 36 values, the reference where given", d["cur"] == yagi() and d["ref"][3] == -70
          and d["ref"][4] is None, d["ref"][:5])
    text = antenlab.svg([("yagi", yagi()), ("dipol", [-66.0] * 36)])
    doc = xml.dom.minidom.parseString(text)
    lines = doc.getElementsByTagName("polyline")
    check("SVG is well formed, one curve per pattern", len(lines) == 2)
    check("the dipole (6 dB below the top) is a circle at 80 % of the radius",
          all(abs(math.hypot(float(x) - 240, float(y) - 240) - 0.8 * 190) < 0.2
              for x, y in (pt.split(",") for pt in lines[1].getAttribute("points").split())))
    check("legend with the numbers", "on/arka 25.0 dB" in text and "dipol" in text)

    e2e()
    if FAILS:
        sys.exit(f"{len(FAILS)} check(s) failed")
    print("all checks passed")


def e2e():
    print("end to end: antenlab.py al <- Anten Lab (live, pty)")
    try:
        import pty, tty
        import serial  # noqa: F401
    except ImportError:
        print("  (pyserial or pty missing: skipped)")
        return
    apps = os.path.join(ROOT, "App", "apps")
    sys.path.insert(0, apps)
    import host_test as ht
    app = os.path.join(apps, "antenlab")
    ht.build(app, "antenlab")
    master, slave = pty.openpty()
    tty.setraw(slave)
    steps = [x for _ in range(36) for x in ("press MENU", "wait 300")]
    p = subprocess.Popen([os.path.join(app, "test", "out", "host_antenlab"), os.path.join(app, "antenlab_assets.bin")],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, cwd=app,
                         env=dict(os.environ, LIVE_FD=str(master)), pass_fds=(master,))
    p.stdin.write(ht.script("host 1", "wait 50", *steps, "wait 3000"))
    p.stdin.close()
    import uvterm
    ser = uvterm.serial.Serial(os.ttyname(slave), 115200, timeout=0.05)
    time.sleep(11.5)                       # 36 measurements of ~300 ms
    text = antenlab.fetch(ser)
    p.communicate(timeout=30)
    ser.close()
    os.close(master)
    os.close(slave)
    s = antenlab.stats(antenlab.parse_csv(text)["cur"])
    check("fetched over the serial port: beam 70 +- 2, front/back 25 dB",
          s and abs(s["beam"] - 70) <= 2 and abs(s["fb"] - 25) < 0.01, s)


if __name__ == "__main__":
    main()
