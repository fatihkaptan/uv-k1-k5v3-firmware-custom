#!/usr/bin/env python3
# Telsiz Okulu host tests: the app built for the computer against the mock
# API of App/apps/host_mock.h. Checks every quiz question of many rounds
# against the data in gen_assets.py (the right answer is right, the four
# answers differ, everything fits the screen), the menu, the Q code cards,
# the phonetic speller, the band plan lookup and the antenna input, and
# renders LCD mockups into test/out/*.png.
#
#   python3 App/apps/telsizokulu/test/test_okul.py
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(APP))
import host_test as ht  # noqa: E402
from host_test import check, press, script  # noqa: E402

NAME = "telsizokulu"


def data():
    """The tables of gen_assets.py, as the build packs them."""
    ns = {"__file__": os.path.join(APP, "gen_assets.py"), "__name__": "data"}
    src = open(os.path.join(APP, "gen_assets.py")).read().replace("a.main()", "")
    argv, sys.argv = sys.argv, ["gen_assets.py", os.devnull, os.devnull]
    try:
        exec(compile(src, "gen_assets.py", "exec"), ns)
    finally:
        sys.argv = argv
    return ns


D = data()


def Run(s, cfg=None, seed=None):
    r = ht.Run(APP, NAME, s, cfg=cfg, seed=seed)
    r.quiz = []                                 # (question, [answers]) per state
    for i, l in enumerate(r.lines):
        if l.startswith("Q ["):
            r.quiz.append((l[3:-1], [x[5:-1] for x in r.lines[i + 1:i + 5]]))
    return r


def wrap18(s):
    """The app's word wrap: lines of at most 18 characters."""
    out = []
    while s:
        n = min(len(s), 18)
        if n < len(s) and s[n] != " ":
            k = s.rfind(" ", 0, n + 1)
            if k > 0:
                n = k + 1
        out.append(s[:n])
        s = s[n:].lstrip(" ")
    return out


def kind(q):
    if any(f[0] == q for f in D["FIX"]):
        return "bank"
    for k, pat in (("qcode", r"'Q..' ne demektir\?"), ("qrev", r"'.+' hangi Q kodu\?"),
                   ("band", r".* MHz hangi amator bandidir\?"), ("ohm", r"Ohm yasasi: .*")):
        if re.fullmatch(pat, q):
            return k
    return "?"


def right_answer(q):
    """The right answer to a generated or bank question, from the data."""
    for f in D["FIX"]:
        if f[0] == q:
            return f[1]
    m = re.fullmatch(r"'(Q..)' ne demektir\?", q)
    if m:
        return dict(D["QCODES"])[m.group(1)]
    m = re.fullmatch(r"'(.+)' hangi Q kodu\?", q)
    if m:
        return {v: k for k, v in D["QCODES"]}[m.group(1)]
    m = re.fullmatch(r"(\d+)\.(\d{3}) MHz hangi amator bandidir\?", q)
    if m:
        khz = int(m.group(1)) * 1000 + int(m.group(2))
        return next(n for n, lo, hi in D["BANDS"] if lo <= khz < hi)
    m = re.fullmatch(r"Ohm yasasi: U=(\d+) V, R=(\d+) ohm ise akim I=\?", q)
    if m:
        u, r = int(m.group(1)), int(m.group(2))
        assert u % r == 0
        return f"{u // r} A"
    return None


def tests():
    print("quiz: every question of 40 rounds")
    seen, bad, types = 0, [], set()
    for seed in range(1, 41):
        # enter the quiz, then look at each question and answer 1
        s = ["wait 50", "press 1", "wait 50"]
        for _ in range(10):
            s += ["state", "press 1", "wait 50", "press MENU", "wait 50"]
        r = Run(script(*s, "state"), seed=seed)
        for q, opts in r.quiz:
            seen += 1
            ans = right_answer(q)
            types.add(kind(q))
            if ans is None:
                bad.append(("unknown question", q))
                continue
            if len(set(opts)) != 4 or any(len(o) > 16 or not o for o in opts):
                bad.append(("answers", q, opts))
            if len(q) > 63 or len(wrap18(q)) > 3:
                bad.append(("question too long", q, wrap18(q)))
        rights = [st["right"] for st in r.states if st["view"] == 1 and st["chosen"] == 255]
        for (q, opts), k in zip(r.quiz, rights):
            if opts[k] != right_answer(q):
                bad.append(("right index", q, opts, k))
        if r.last["qn"] != 10:
            bad.append(("round did not end", seed, r.last))
    check(f"{seen} questions: right answer marked, 4 different answers, fits 3 lines", not bad and seen == 400,
          bad[:3])
    check("every kind of question came up (bank, Q codes both ways, bands, Ohm)",
          types == {"bank", "qcode", "qrev", "band", "ohm"}, types)

    print("quiz: score, tones, best")
    r0 = Run(script("wait 50", "press 1", "wait 50", *(["state", "press 1", "wait 50", "press MENU", "wait 50"] * 10)),
             seed=7)
    rights = [st["right"] for st in r0.states if st["chosen"] == 255]
    s = ["wait 50", "press 1", "wait 50"]
    for k in rights:
        s += [f"press {k + 1}", "wait 50", "state", "press MENU", "wait 50"]
    r = Run(script(*s, "state", "press EXIT", "wait 50", "press EXIT", "wait 50"), seed=7)
    check("all right: 10/10, the right tone every time",
          r.states[-1]["score"] == 10 and r.tones.count((1500, 80)) == 10, (r.states[-1], r.tones[:3]))
    check("best score saved with the menu choice", r.cfg == bytes([0x4F, 10, 0]), r.cfg)
    s = ["wait 50", "press 1", "wait 50"]
    for k in rights[:3]:
        s += [f"press {(k + 1) % 4 + 1}", "wait 50", "state", "press MENU", "wait 50"]
    r = Run(script(*s), seed=7)
    check("wrong answers: no point, low tone", r.states[-1]["score"] == 0 and r.tones.count((300, 250)) == 3,
          r.states[-1])
    r = Run(script("wait 50", "press 1", "wait 50", "press 5", "press MENU", "press UP", "wait 50", "state"), seed=3)
    check("before an answer only 1-4 count", r.last["chosen"] == 255 and r.last["qn"] == 0, r.last)
    r = Run(script("wait 50", "state"), cfg="4f0703")
    check("saved config restored (best 7, menu on item 4)", r.last["best"] == 7 and r.last["sel"] == 3, r.last)

    print("menu and Q code cards")
    r = Run(script("wait 50", "press DOWN", "press DOWN", "state", "press MENU", "wait 50", "state",
                   "press EXIT", "wait 50", "press UP", "press UP", "press UP", "state"))
    check("UP / DOWN move, MENU enters the item", r.states[0]["sel"] == 2 and r.states[1]["view"] == 3, r.states[:2])
    check("UP wraps around", r.states[2]["sel"] == 4 and r.states[2]["view"] == 0, r.states[2])
    r = Run(script("wait 50", "press 2", "wait 50", "state", "press MENU", "wait 50", "state",
                   "press DOWN", "wait 50", "state", "press UP", "press UP", "wait 50", "state"))
    check("card 1 hidden, MENU shows it", r.states[0]["reveal"] == 0 and r.states[1]["reveal"] == 1, r.states[:2])
    check("DOWN: next card, hidden again", r.states[2]["n"] == 1 and r.states[2]["reveal"] == 0, r.states[2])
    check("UP from the first card wraps to the last", r.states[3]["n"] == len(D["QCODES"]) - 1, r.states[3])

    print("phonetic speller")
    r = Run(script("wait 50", "press 3", "wait 50", *press(8), "wait 1000", *press(2), "wait 1000",
                   *press(1), "wait 1000", *press(2), "wait 1000", *press(2, 2), "wait 1000",
                   *press(2, 2, 2), "wait 1000", "state", "down 7", "wait 900", "up", "wait 50", "state",
                   "press EXIT", "wait 50", "state", "press MENU", "wait 50", "state"))
    check("multi-tap: TA1ABC", r.states[0]["in"] == "TA1ABC", r.states[0])
    check("long press types the digit", r.states[1]["in"] == "TA1ABC7", r.states[1])
    check("EXIT deletes, MENU clears", r.states[2]["in"] == "TA1ABC" and r.states[3]["in"] == "", r.states[2:])
    r = Run(script("wait 50", "press 3", "wait 50", "down DOWN", "wait 7000", "up", "wait 50", "state"))
    check("empty: the alphabet scrolls to its end (37 rows, 6 shown)", r.last["top"] == 31, r.last)

    print("band plan and antenna")
    segs = D["SEGS"]
    for f10, want in ((14550000, "145.500 cagri"), (14480000, "APRS"), (10000000, "FM radyo"),
                      (43350000, "433.500 cagri"), (44600625, "PMR446")):
        r = Run(script(f"freq {f10}", "wait 50", "press 4", "wait 50", "state"))
        n = r.last["n"]
        check(f"{f10 / 1e5:.5f} MHz -> {want}", n < len(segs) and want in segs[n][2], (n, r.last))
    r = Run(script("freq 30000000", "wait 50", "press 4", "wait 50", "state", "press DOWN", "wait 50", "state",
                   "press UP", "press UP", "wait 50", "state", "press MENU", "wait 50", "state"))
    # from NONE, DOWN gives entry 0; UP from 0 wraps to the last, UP again one before
    check("300 MHz: not in the plan", r.states[0]["n"] == 255, r.states[0])
    check("DOWN browses from the first entry, UP wraps",
          r.states[1]["n"] == 0 and r.states[1]["vfo"] == 0 and r.states[2]["n"] == len(segs) - 2, r.states[1:3])
    check("MENU goes back to the VFO", r.states[3]["vfo"] == 1 and r.states[3]["n"] == 255, r.states[3])
    r = Run(script("wait 50", "press 5", "wait 50", "state", *press(4, 3, 3, "STAR", 5, "STAR"), "wait 50", "state",
                   "press EXIT", "press EXIT", "wait 50", "state"))
    check("antenna: the VFO frequency first", r.states[0]["ant"] == 145500, r.states[0])
    check("typed 433*5: 433.500 MHz", r.states[1]["in"] == "433.5." and r.states[1]["ant"] == 433500, r.states[1])
    check("EXIT deletes typed characters", r.states[2]["in"] == "433.", r.states[2])


def mockups():
    shots = [
        ("menu", script("wait 50", "press DOWN", "press UP", "wait 50", "shot menu")),
        ("quiz", script("wait 50", "press 1", "wait 50", "press 2", "wait 50", "shot quiz")),
        ("qcode", script("wait 50", "press 2", "wait 50", *press("DOWN") * 20, "press MENU", "wait 50", "shot qcode")),
        ("fonetik", script("wait 50", "press 3", "wait 50", *press(8), "wait 1000", *press(2), "wait 1000",
                           *press(1), "wait 1000", *press(2), "wait 1000", *press(2, 2), "wait 1000",
                           *press(2, 2, 2), "wait 1000", "shot fonetik")),
        ("bant", script("wait 50", "press 4", "wait 50", "shot bant")),
        ("anten", script("wait 50", "press 5", "wait 50", "shot anten")),
    ]
    for name, s in shots:
        Run(s, seed=11)
        path = ht.png(APP, name)
        if path:
            print(f"  mockup {os.path.relpath(path, ht.ROOT)}")


if __name__ == "__main__":
    ht.build(APP, NAME)
    tests()
    mockups()
    ht.finish()
