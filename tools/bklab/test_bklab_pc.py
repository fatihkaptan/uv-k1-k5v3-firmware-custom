#!/usr/bin/env python3
# bklab.py tests: the names table equals the app's, dumps and their diff, and
# the BK class plus shell commands against the BK Lab app itself (built for
# the computer, live on a pty, with a mock BK4819).
#
#   python3 tools/bklab/test_bklab_pc.py
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import bklab  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + name + ("" if cond else f"  -> {detail}"))
    if not cond:
        FAILS.append(name)


def main():
    print("offline")
    ns = {"__file__": os.path.join(ROOT, "App", "apps", "bklab", "gen_assets.py"), "__name__": "x"}
    src = open(ns["__file__"]).read().replace("a.main()", "")
    sys.path.insert(0, os.path.join(ROOT, "App", "apps"))
    exec(compile(src, "gen_assets.py", "exec"), ns)
    check("register names and protected set equal the app's", ns["NAMES"] == bklab.NAMES
          and set(ns["PROTECTED"]) == bklab.PROTECTED)
    a = bklab.parse_dump(bklab.fmt_dump([0x1000 + i for i in range(128)]))
    b = dict(a)
    b[0x13] ^= 0x0204
    check("dump text read back", len(a) == 128 and a[0x7F] == 0x107F)
    check("diff: the register, the changed bits, the name",
          bklab.diff(a, b) == ["13  1013 -> 1217  bit 9,2  KAZANC 3"], bklab.diff(a, b))
    e2e()
    if FAILS:
        sys.exit(f"{len(FAILS)} check(s) failed")
    print("all checks passed")


def e2e():
    print("end to end: bklab.py <-> BK Lab (live, pty)")
    try:
        import pty, tty
        import serial  # noqa: F401
    except ImportError:
        print("  (pyserial or pty missing: skipped)")
        return
    sys.path.insert(0, os.path.join(ROOT, "App", "apps"))
    import host_test as ht
    app = os.path.join(ROOT, "App", "apps", "bklab")
    ht.build(app, "bklab")
    master, slave = pty.openpty()
    tty.setraw(slave)
    p = subprocess.Popen([os.path.join(app, "test", "out", "host_bklab"), os.path.join(app, "bklab_assets.bin")],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, cwd=app,
                         env=dict(os.environ, LIVE_FD=str(master)), pass_fds=(master,))
    p.stdin.write(ht.script("host 1", "wait 9000"))
    p.stdin.close()
    import uvterm
    bk = bklab.BK(uvterm.serial.Serial(os.ttyname(slave), 115200, timeout=0.05))
    time.sleep(0.4)
    check("read 0x13", bk.read(0x13) == 0x03DF)
    check("read 3 from 0x10", bk.read(0x10, 3) == [0x1010, 0x1011, 0x1012])
    check("write 0x13, read back", bk.write(0x13, 0x03D9) == 0x03D9)
    try:
        bk.write(0x30, 0)
        check("protected refused without force", False)
    except bklab.BKError:
        check("protected refused without force", True)
    check("forced", bk.write(0x30, 0xBFF0, force=True) == 0xBFF0)
    check("status", bk.status() == {"rssi": -96.5, "gurultu": 12, "glitch": 3})
    d = bk.dump()
    check("dump of 128 with the writes", len(d) == 128 and d[0x13] == 0x03D9 and d[0x30] == 0xBFF0)
    out = []
    bklab.run(bk, "tara 48 0 4 2 20", out.append)
    check("tara: 3 values with their meters, the register put back",
          len(out) == 4 and out[1].split()[0] == "0000" and out[3].split()[0] == "0004" and bk.read(0x48) == 0x1048,
          out)
    mon = bk.monitor(0x67, 100, 1.0)
    check("monitor ~10 lines a second", 7 <= len(mon) <= 12 and all(v == 0x7F for _, v in mon), len(mon))
    check("geri: the written registers back", bk.restore() == 3 and bk.read(0x30) == 0xBFF1 and bk.read(0x13) == 0x03DF)
    p.communicate(timeout=30)
    bk.close()
    os.close(master)
    os.close(slave)


if __name__ == "__main__":
    main()
