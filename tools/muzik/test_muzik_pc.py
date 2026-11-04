#!/usr/bin/env python3
# muzik.py tests without a radio: the MIDI reader (running status, several
# tracks, tempo changes, sysex, drums), the melody of chords, the writer
# (round trip), timed sending, recording, and an end-to-end run against the
# Muzik Kutusu app itself (built for the computer, live on a pty).
#
#   python3 tools/muzik/test_muzik_pc.py
import os, struct, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import muzik  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + name + ("" if cond else f"  -> {detail}"))
    if not cond:
        FAILS.append(name)


def track(body):
    return b"MTrk" + struct.pack(">I", len(body)) + body


def main():
    print("MIDI reader")
    # format 1, 96 ticks per quarter: track 0 = tempo map, track 1 = notes
    t0 = (b"\x00\xFF\x51\x03\x07\xA1\x20"            # 500000 us: 120 BPM
          b"\x81\x40\xFF\x51\x03\x0F\x42\x40"         # at tick 192: 1000000 us (60 BPM)
          b"\x00\xFF\x2F\x00")
    t1 = (b"\x00\xF0\x03\x01\x02\xF7"                 # sysex, skipped
          b"\x00\xB0\x07\x64"                         # controller, skipped
          b"\x00\x90\x3C\x64"                         # C4 on
          b"\x00\x40\x64"                             # E4 on, running status (chord)
          b"\x60\x80\x40\x00"                         # +96: E4 off
          b"\x60\x3C\x00"                             # +96: C4 off (running status 0x80)
          b"\x00\x99\x24\x64"                         # drum on channel 10
          b"\x00\x90\x43\x64"                         # G4 on
          b"\x60\x43\x00"                             # +96: G4 off (note on, velocity 0)
          b"\x00\x89\x24\x00"
          b"\x00\xFF\x2F\x00")
    data = b"MThd" + struct.pack(">IHHH", 6, 1, 2, 96) + track(t0) + track(t1)
    div, ev = muzik.read_midi(data)
    ons = [(e[0], e[3]) for e in ev if e[1] == "on"]
    check("events: running status, sysex and controllers skipped", ons == [(0, 60), (0, 64), (192, 36), (192, 67)], ons)
    m = muzik.melody(div, ev)
    check("melody: the top of the chord (E4), C4 when E4 ends, G4 after the tempo change, drums out",
          m == [(0.0, 64), (0.5, 60), (1.0, 67), (2.0, 0)], m)
    check("only channel 1 asked: the same melody", muzik.melody(div, ev, channel=0) == m, m)
    m = muzik.melody(div, ev, transpose=-12)
    check("transpose", [n for _, n in m] == [52, 48, 55, 0], m)
    for bad, why in ((b"RIFF....", "not MIDI"), (b"MThd" + struct.pack(">IHHH", 6, 0, 1, 0xE728), "SMPTE")):
        try:
            muzik.read_midi(bad)
            check(f"refused: {why}", False)
        except muzik.MidiError:
            check(f"refused: {why}", True)

    print("writer, sending, recording")
    d = tempfile.mkdtemp()
    path = os.path.join(d, "t.mid")
    notes = [(0.0, 0.5, 60), (0.5, 0.25, 62), (1.0, 1.0, 64)]
    muzik.write_midi(notes, path)
    div, ev = muzik.read_midi(open(path, "rb").read())
    m = muzik.melody(div, ev)
    check("written file reads back", m == [(0.0, 60), (0.5, 62), (0.75, 0), (1.0, 64), (2.0, 0)], m)

    class Ser:
        def __init__(self):
            self.out = []

        def write(self, b):
            self.out.append((clock.t, b.decode().strip()))

        def flush(self):
            pass

    class Clock:
        t = 0.0

        def __call__(self):
            return self.t

        def sleep(self, s):
            self.t += s
    clock = Clock()
    ser = Ser()
    muzik.play(ser, m, speed=2.0, clock=clock, sleep=clock.sleep, show=None)
    check("commands on time (speed 2: twice as fast), x at the end",
          [(round(t, 3), c) for t, c in ser.out] == [(0, "n60"), (0.25, "n62"), (0.375, "x"), (0.5, "n64"),
                                                     (1.0, "x"), (1.0, "x")], ser.out)
    times = iter([0.0, 0.4, 0.6, 1.1, 1.2])
    rec = list(muzik.record(["n60", "x", "n67", "n69", "x"], clock=lambda: next(times)))
    check("recording: n/x lines with their times -> notes",
          [(round(a, 2), round(b, 2), n) for a, b, n in rec] == [(0.0, 0.4, 60), (0.6, 0.5, 67), (1.1, 0.1, 69)], rec)

    e2e()
    if FAILS:
        sys.exit(f"{len(FAILS)} check(s) failed")
    print("all checks passed")


def e2e():
    """muzik.play over a pty into the Muzik Kutusu app, in real time."""
    print("end to end: muzik.py -> Muzik Kutusu (live, pty)")
    try:
        import pty, tty
        import serial  # noqa: F401
    except ImportError:
        print("  (pyserial or pty missing: skipped)")
        return
    apps = os.path.join(ROOT, "App", "apps")
    sys.path.insert(0, apps)
    import host_test as ht
    app = os.path.join(apps, "muzikkutusu")
    ht.build(app, "muzikkutusu")
    master, slave = pty.openpty()
    tty.setraw(slave)
    p = subprocess.Popen([os.path.join(app, "test", "out", "host_muzikkutusu"),
                          os.path.join(app, "muzikkutusu_assets.bin")],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, cwd=app,
                         env=dict(os.environ, LIVE_FD=str(master)), pass_fds=(master,))
    p.stdin.write(ht.script("host 1", "wait 2500"))
    p.stdin.close()
    import uvterm
    ser = uvterm.serial.Serial(os.ttyname(slave), 115200, timeout=0.05)
    time.sleep(0.2)
    melody = [(0.0, 67), (0.3, 69), (0.6, 71), (0.9, 72), (1.4, 0)]
    muzik.play(ser, melody, show=None)
    out = p.communicate(timeout=30)[0]
    ser.close()
    os.close(master)
    os.close(slave)
    reg2note = {}
    for n in range(48, 97):
        reg2note[(round(440.0 * 2 ** ((n - 69) / 12)) * 1353245 + (1 << 16)) >> 17] = n
    got, reg = [], None
    for line in out.splitlines():
        f = line.split()
        if f[0] == "BK" and f[1] == "71":
            reg = int(f[2], 16)
        elif f[0] == "MUTE" and f[1] == "0":
            got.append((reg2note.get(reg), int(f[2])))
    check("the radio played G4 A4 B4 C5", [n for n, _ in got] == [67, 69, 71, 72], got)
    if len(got) == 4:
        steps = [got[i + 1][1] - got[i][1] for i in range(3)]
        check("300 ms apart (+-60 ms, real time)", all(abs(s - 300) <= 60 for s in steps), steps)


if __name__ == "__main__":
    main()
