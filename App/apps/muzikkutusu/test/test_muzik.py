#!/usr/bin/env python3
# Muzik Kutusu host tests: the app built for the computer against the mock
# API of App/apps/host_mock.h. The notes it plays are rebuilt from the
# BK4819 writes (REG_71 = pitch) and the mute switches (start / end, in ms)
# and compared with the melodies of gen_assets.py, the keys held, the
# recording and its playback after a restart (the saved block), and the USB
# note protocol. LCD mockups go to test/out/*.png.
#
#   python3 App/apps/muzikkutusu/test/test_muzik.py
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(APP))
import host_test as ht  # noqa: E402
from host_test import check, press, script  # noqa: E402

NAME = "muzikkutusu"
TOL = 15                                   # ms: 10 ms ticks + 5 ms polling


def data():
    ns = {"__file__": os.path.join(APP, "gen_assets.py"), "__name__": "data"}
    src = open(os.path.join(APP, "gen_assets.py")).read().replace("a.main()", "")
    argv, sys.argv = sys.argv, ["gen_assets.py", os.devnull, os.devnull]
    try:
        exec(compile(src, "gen_assets.py", "exec"), ns)
    finally:
        sys.argv = argv
    return ns


D = data()
REG2NOTE = {}
for n in range(D["LO"], D["HI"] + 1):
    hz = 440.0 * 2 ** ((n - 69) / 12)
    REG2NOTE[(round(hz) * 1353245 + (1 << 16)) >> 17] = n


def Run(s, **kw):
    r = ht.Run(APP, NAME, s, **kw)
    r.notes = []                            # (midi, start ms, length ms)
    reg, on = None, None
    for l in r.lines:
        f = l.split()
        if f[0] == "BK" and f[1] == "71":
            reg = int(f[2], 16)
        elif f[0] == "MUTE":
            t = int(f[2])
            if f[1] == "0":
                on = (REG2NOTE.get(reg), t)
            elif on:
                r.notes.append((on[0], on[1], t - on[1]))
                on = None
    r.save = next((l[5:] for l in r.lines if l.startswith("SAVE ")), None)
    return r


def expected(song, tempo=100):
    title, bpm, text = D["SONGS"][song]
    ms16 = round(15000 / bpm)
    ev = D["notes"](text)
    out, t = [], 0
    for i in range(0, len(ev), 2):
        n, d = ev[i], ev[i + 1]
        ms = d * ms16 * 100 // tempo
        if n:
            out.append((n, t, ms - ms // 8))
        t += ms
    return out


def close(got, want, tol=TOL):
    if len(got) != len(want):
        return False
    t0g, t0w = got[0][1], want[0][1]
    return all(g[0] == w[0] and abs((g[1] - t0g) - (w[1] - t0w)) <= tol and abs(g[2] - w[2]) <= tol
               for g, w in zip(got, want))


def tests():
    print("melodies")
    for song in range(len(D["SONGS"])):
        want = expected(song)
        total = want[-1][1] + want[-1][2] + 500
        r = Run(script("wait 50", "press 1", "wait 50", f"press {song + 1}", f"wait {total}", "state"))
        if song < 3:
            check(f"'{D['SONGS'][song][0]}': every note, pitch and timing (+-{TOL} ms)",
                  close(r.notes, want), (r.notes[:4], want[:4], len(r.notes), len(want)))
        else:
            check(f"'{D['SONGS'][song][0]}': the notes in order", [n for n, _, _ in r.notes] == [n for n, _, _ in want],
                  (len(r.notes), len(want)))
        if song == 0:
            check("the song ends by itself, back to the list", r.last["src"] == 0, r.last)
    want = expected(1, tempo=120)
    r = Run(script("wait 50", "press 1", "wait 50", "press 2", "wait 5", "press UP", "press UP", "wait 20000"))
    check("UP x2 while playing: tempo 120 %, every note shorter", close(r.notes[1:], want[1:], tol=25),
          (r.notes[1:4], want[1:4]))
    r = Run(script("wait 50", "press 1", "wait 50", "press 3", "wait 1000", "press EXIT", "wait 50", "state",
                   "press EXIT", "wait 50", "state"))
    check("EXIT stops the song, then back to the menu", r.states[0]["src"] == 0 and r.states[0]["view"] == 1
          and r.states[1]["view"] == 0 and r.lines.count("MUTE 1 " + r.lines[-1].split()[-1]) <= 1, r.states)

    print("piano")
    r = Run(script("wait 50", "press 2", "wait 50", "down 1", "wait 300", "up", "wait 200", "down 3", "wait 500",
                   "up", "wait 100", "press STAR", "down 1", "wait 200", "up", "wait 100",
                   "press UP", "down 8", "wait 200", "up", "wait 100", "state"))
    got = [(n, l) for n, _, l in r.notes]
    check("held keys: C4 300 ms, E4 500 ms (as long as held)", got[0][0] == 60 and abs(got[0][1] - 300) <= TOL
          and got[1][0] == 64 and abs(got[1][1] - 500) <= TOL, got)
    check("* then 1: C#4", got[2][0] == 61, got)
    check("UP: one octave up, 8 = C an octave above: C6", got[3][0] == 84 and r.last["oct"] == 5, (got, r.last))
    r = Run(script("wait 50", "press 2", "wait 50", *press("UP") * 5, "state", *press("DOWN") * 5, "state"))
    check("octaves 3 .. 6", r.states[0]["oct"] == 6 and r.states[1]["oct"] == 3, r.states)

    print("recording, playback, kept across restarts")
    take = ["wait 50", "press 2", "wait 50", "press MENU", "wait 100", "down 1", "wait 300", "up", "wait 200",
            "down 3", "wait 500", "up", "wait 100", "press MENU", "wait 50", "state"]
    r = Run(script(*take, "press F", "wait 1500", "state", "press EXIT", "wait 50", "press EXIT", "wait 50"),
            env={"SAVEDUMP": "1"})
    check("MENU, two notes, MENU: three events (note, rest, note)", r.states[0]["n"] == 3 and r.states[0]["rec"] == 0,
          r.states[0])
    play = r.notes[2:]
    check("F plays it back: C4 300, rest 200, E4 500 (20 ms units)", len(play) == 2 and play[0][0] == 60
          and abs(play[0][2] - 300) <= 25 and play[1][0] == 64 and abs(play[1][1] - play[0][1] - 500) <= 25
          and abs(play[1][2] - 500) <= 25, play)
    check("the recording is left in the display buffers at exit", r.save is not None
          and bytes.fromhex(r.save)[:4] == b"MK\x03\x00", (r.save or "")[:16])
    blob = bytearray(open(os.path.join(APP, f"{NAME}_assets.bin"), "rb").read())
    blob[-1024:] = bytes.fromhex(r.save)
    kept = os.path.join(APP, "test", "out", "kept_assets.bin")
    with open(kept, "wb") as f:
        f.write(blob)
    r2 = Run(script("wait 50", "state", "press 2", "wait 50", "press F", "wait 1500", "shot kayit"), assets=kept)
    check("after a restart: the 3 events are back and play the same",
          r2.states[0]["n"] == 3 and [(n, l // 20) for n, _, l in r2.notes] == [(n, l // 20) for n, _, l in play],
          (r2.states[0], r2.notes))
    r3 = Run(script("wait 50", "state"), env={"SAVEDUMP": "1"})
    check("no recording: an empty block (not the screen) is kept",
          bytes.fromhex(r3.save) == b"MK\x00\x00" + bytes(1020), r3.save[:16])

    print("USB, volume, silence")
    r = Run(script("host 1", "wait 50", "rx n69\\r", "wait 300", "state", "rx x\\r", "wait 50", "rx /echo off\\r",
                   "wait 50", "press 1", "wait 300", "up", "wait 50"))
    check("banner on connection", r.tx.startswith(b"# Muzik Kutusu 1.0 ready\r\n"), r.tx[:40])
    check("'n69' plays A4 until 'x', the piano view opens", r.notes[0][0] == 69 and abs(r.notes[0][2] - 300) <= TOL
          and r.states[0]["view"] == 2, (r.notes, r.states[0]))
    check("/echo off answered", b"# echo off\r\n" in r.tx)
    check("keypad notes go to the computer: n60 ... x", r.tx.endswith(b"n60\r\nx\r\n"), r.tx[-20:])
    r = Run(script("wait 50", "press 3", "wait 50", "state", "wait 2500"))
    check("menu 3: volume up one step, a sample note", r.states[0]["vol"] == 3 and r.notes and r.notes[0][0] == 72,
          (r.states, r.notes))
    check("its level written to REG_70 (gain 40)", "BK 70 a800" in " ".join(r.lines))
    check("the amplifier goes off after 2 s of silence", any(l.startswith("AUDIO 0") for l in r.lines)
          and any(l.startswith("TONESOFF") for l in r.lines))
    r = Run(script("wait 50", "press 3", "press 3", "press 3", "wait 50", "press EXIT", "wait 50"))
    check("volume saved (wraps 5 levels)", r.cfg is not None and r.cfg[1] == 0, r.cfg)


def mockups():
    shots = [
        ("menu", script("wait 50", "shot menu")),
        ("liste", script("wait 50", "press 1", "wait 50", "press DOWN", "press DOWN", "wait 50", "shot liste")),
        ("calar", script("wait 50", "press 1", "wait 50", "press 3", "wait 2100", "shot calar")),
        ("piyano", script("wait 50", "press 2", "wait 50", "press MENU", "press STAR", "down 5", "wait 300",
                          "shot piyano")),
    ]
    for name, s in shots:
        Run(s)
        path = ht.png(APP, name)
        if path:
            print(f"  mockup {os.path.relpath(path, ht.ROOT)}")


if __name__ == "__main__":
    ht.build(APP, NAME)
    tests()
    mockups()
    ht.finish()
