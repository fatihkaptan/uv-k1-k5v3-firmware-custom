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
    src = open(os.path.join(APP, "gen_assets.py")).read().replace("a.main()", "pass")
    argv, sys.argv = sys.argv, ["gen_assets.py", os.devnull, os.devnull]
    try:
        exec(compile(src, "gen_assets.py", "exec"), ns)
    finally:
        sys.argv = argv
    return ns


D = data()
REG2NOTE = {r: D["LO"] + i for i, r in enumerate(D["TONE"])}      # piano notes -> MIDI
KREGS = [D["reg"](440.0 * 2 ** ((k - 305) / 53)) for k, _ in D["KUSED"]]
for i, r in enumerate(KREGS):
    REG2NOTE.setdefault(r, D["NTONE"] + i)                            # 53-TET pitches -> index


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
    out, t = [], 0
    for p, d in D["SONGS"][song]["ev"]:
        ms = d * 100 // tempo
        if p is not None:
            out.append((D["LO"] + p if p < D["NTONE"] else p, t, ms - ms // 8))
        t += ms
    return out


def pick(song):
    return [f"press {song + 1}"] if song < 9 else [*press("DOWN") * song, "press MENU"]


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
        r = Run(script("wait 50", "press 1", "wait 50", *pick(song), f"wait {total}", "state"))
        name = D["SONGS"][song]["title"]
        if song < 3:
            check(f"'{name}': every note, pitch and timing (+-{TOL} ms)",
                  close(r.notes, want), (r.notes[:4], want[:4], len(r.notes), len(want)))
        else:
            check(f"'{name}': the notes in order", [n for n, _, _ in r.notes] == [n for n, _, _ in want],
                  (len(r.notes), len(want)))
        if song == 0:
            check("the song ends by itself, back to the list", r.last["src"] == 0, r.last)
    short = min(range(len(D["SONGS"])), key=lambda i: sum(ms for _, ms in D["SONGS"][i]["ev"]))
    want = expected(short, tempo=120)
    r = Run(script("wait 50", "press 1", "wait 50", *pick(short), "wait 5", "press UP", "press UP",
                   f"wait {want[-1][1] + 3000}"))
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
    check("banner on connection", r.tx.startswith(b"# Muzik Kutusu 2.0 ready\r\n"), r.tx[:40])
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


def tx_tests():
    print("yayin: the active VFO")
    first = expected(0)
    end = first[-1][1] + first[-1][2]
    r = Run(script("wait 50", "state", "press 4", "wait 50", "state", "press 1", "wait 50", "press 1",
                   f"wait {end + 3000}", "state"))
    L = r.lines
    check("off at start, menu 4 switches it on", r.states[0]["tx"] == 0 and r.states[1]["tx"] == 1, r.states[:2])
    keyed = next((i for i, l in enumerate(L) if l.startswith("BK 30 c3fa")), None)
    on = next((i for i, l in enumerate(L) if l.startswith("MUTE 0")), None)
    check("a song keys up: tx_set_params, TONE1 gain 66, TX link, LED, then the notes",
          keyed is not None and "TXON" in L[:keyed] and "BK 70 c200" in " ".join(L[:keyed]) and "LED 1" in L[keyed:on]
          and not any(l.startswith("PREP") for l in L), L[:12])
    check("300 ms of carrier before the first note", int(L[on].split()[2]) - int(L[keyed].split()[3]) >= 300,
          (L[keyed], L[on]))
    got = [n for n, _, _ in r.notes]
    check("the whole song on the air, the same notes", got == [n for n, _, _ in first], (len(got), len(first)))
    off = next((i for i, l in enumerate(L) if l == "TXOFF"), None)
    check("unkeyed 2 s after the last note: REG_30 idle, tx_end, LED off", off is not None
          and "BK 30 c1fe" in " ".join(L[off - 4:off]) and "LED 0" in L[off:] and r.last["audio"] == 0, L[-8:])
    r = Run(script("wait 50", "press 4", "txstate 1", "press 1", "wait 50", "press 1", "wait 500", "state"))
    check("refused by the firmware (band, battery): the speaker plays instead",
          "TXON" not in r.lines and any(l.startswith("PREP") for l in r.lines) and r.last["audio"] == 1, r.last)
    r = Run(script("wait 50", "press 4", "press 3", "wait 300", "state"))
    check("the volume sample in the menu stays on the speaker", "TXON" not in r.lines and r.notes, r.lines[:6])
    r = Run(script("host 1", "wait 50", "press 4", "wait 50", "rx n69\\r", "wait 181000", "state"))
    check("USB notes go on the air too; after 3 min the time-out unkeys and switches yayin off",
          "TXON" in r.lines and "TXOFF" in r.lines and r.last["tx"] == 0 and r.last["audio"] == 0, r.last)


def mockups():
    shots = [
        ("menu", script("wait 50", "shot menu")),
        ("liste", script("wait 50", "press 1", "wait 50", "press DOWN", "press DOWN", "wait 50", "shot liste")),
        ("calar", script("wait 50", "press 1", "wait 50", "press 3", "wait 2100", "shot calar")),
        ("yayin", script("wait 50", "press 4", "wait 50", "shot yayin")),
        ("tx", script("wait 50", "press 4", "press 1", "wait 50", "press 2", "wait 1500", "shot tx")),
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
    tx_tests()
    mockups()
    ht.finish()
