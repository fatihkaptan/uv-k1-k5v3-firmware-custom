#!/usr/bin/env python3
# Mors Okur host tests: the app built for the computer against the mock API of
# App/apps/host_mock.h and a mock microphone (REG_64 follows a Morse pattern:
# test/host_morsokur.c). Text at several speeds, hand keying, a weak signal in
# noise, a steady sound, the speed adapting, Turkish letters; the BK4819
# writes (no RF section ever on), USB, keys. Mockups: test/out/*.png.
#
#   python3 App/apps/morsokur/test/test_morsokur.py
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(APP))
import host_test as ht  # noqa: E402
from host_test import check, press, script  # noqa: E402

NAME = "morsokur"
MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....",
    "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.",
    "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.", "?": "..--..", "/": "-..-.",
    "=": "-...-", ".": ".-.-.-", "Ç": "-.-..", "Ğ": "--.-.", "Ö": "---.", "Ş": ".--..", "Ü": "..--",
}
SHOWN = {"Ç": "c", "Ğ": "g", "Ö": "o", "Ş": "s", "Ü": "u"}


def pattern(text):
    return "/".join(" ".join(MORSE[c] for c in w) for w in text.split())


def length(text, wpm):
    dot = 1200 // wpm
    n = sum(1 + 2 * (e == "-") + 1 for e in pattern(text) if e in ".-")
    return n * dot + pattern(text).count(" ") * 2 * dot + pattern(text).count("/") * 6 * dot


def Run(text, wpm=15, tail=1500, extra=(), pre=(), **env):
    """The sender keys `text` at `wpm`; `pre` are the keys pressed first."""
    if pre:
        env.setdefault("START", 400 + 80 * len(pre))
    e = {"PATTERN": pattern(text), "WPM": str(wpm)}
    e.update({k: str(v) for k, v in env.items()})
    wait = int(env.get("START", 500)) + length(text, wpm) + tail
    r = ht.Run(APP, NAME, script("wait 50", *pre, "wait 350", f"wait {wait}", "state", *extra), env=e)
    r.text = next((l[5:] for l in reversed(r.lines) if l.startswith("TEXT ")), "")
    r.flat = r.text.replace("|", "").strip()
    r.writes = [(int(l.split()[1], 16), int(l.split()[2], 16)) for l in r.lines if l.startswith("BK ")]
    return r


def tests():
    print("decoding")
    msg = "CQ CQ DE TA2ABC K"
    r = Run(msg)
    check(f"15 WPM keyer: '{msg}'", r.flat == msg, r.flat)
    check("manual 15 WPM by default (dot 80 ms), not automatic", r.last["wpm"] == 15 and r.last["dot"] == 80
          and r.last["oto"] == 0, r.last)
    r = Run("PARIS PARIS PARIS PARIS", wpm=25, pre=press("UP") * 10)
    check("UP x10: 25 WPM, read from the first word on", r.flat == "PARIS PARIS PARIS PARIS"
          and r.last["wpm"] == 25 and r.last["dot"] == 48, (r.flat, r.last))
    r = Run("TEST DE TA2ABC", wpm=6, tail=3000, pre=press("DOWN") * 9)
    check("DOWN x9: 6 WPM, slow", r.flat == "TEST DE TA2ABC" and r.last["wpm"] == 6, r.flat)
    for w in (11, 19):
        r = Run("CQ DE TA2ABC K", wpm=w)
        check(f"set to 15, a sender at {w} WPM ({round((w - 15) / 15 * 100):+d} %) still read",
              r.flat == "CQ DE TA2ABC K" and r.last["dot"] == 80, r.flat)
    r = Run("PARIS PARIS PARIS PARIS", wpm=25, pre=press("F"))
    check("F: automatic speed, from 15 to 25 WPM within the first word, shown as OTO",
          r.flat.endswith("PARIS PARIS PARIS") and r.last["oto"] == 1 and abs(1200 / r.last["dot"] - 25) <= 3,
          (r.flat, r.last))
    r = Run("BOLU 73 SK", wpm=18, HAND=20, pre=press("UP") * 3)
    check("hand keying, every element and gap +-20 %", r.flat == "BOLU 73 SK".replace("SK", "SK"), r.flat)
    r = Run("QRV 145.500", wpm=15, LEVEL=420, FLOOR=200, NOISE=60)
    check("weak: tone only 2.1 x the quiet level, noise +-60", r.flat == "QRV 145.500", r.flat)
    r = Run("ÇÖÜŞĞ", wpm=15)
    check("Turkish letters in lower case: cousg", r.flat == "".join(SHOWN[c] for c in "ÇÖÜŞĞ"), r.flat)
    r = Run("HI HI", wpm=15, START=3500, STEADY="300,2800")
    check("a 2.5 s steady sound is not Morse: nothing written, then 'HI HI'", r.flat == "HI HI", r.flat)
    r = Run("", tail=10000, NOISE=80)
    check("10 s of room noise (+-80) alone: no characters", r.flat == "", r.flat)
    r = Run("ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ", wpm=20, pre=press("UP") * 5)
    check("long text: rows scroll, the last rows kept",
          r.text.split("|")[-1].strip().endswith("STUVWXYZ") and "0123456789" in r.text.replace("|", ""), r.text)

    print("radio, keys, USB")
    r = Run("E")
    w30 = [v for reg, v in r.writes if reg == 0x30]
    check("mic ADC + TX DSP on, PLL / VCO / PA gain off (no RF), AF muted",
          w30[:2] == [0, 0x0306] and not any(v & 0x00F8 for v in w30[:2]) and "AF 0" in r.lines, w30)
    check("never keys the transmitter", not any(l in ("TXON",) for l in r.lines))
    r = Run("E", extra=("press 0", "wait 50", "state", "press EXIT", "wait 50"))
    w = r.writes
    check("0: the receiver kept, mic ADC added (0xBFF5), VOX detector on; EXIT puts REG_31 back",
          (0x30, 0xBFF5) in w and (0x31, 0x1234 | 4) in w and w[-1] == (0x31, 0x1234)
          and any(l.startswith("TONESOFF") for l in r.lines), w[-4:])
    r = Run("E", extra=(*press("UP") * 30, "state", *press("DOWN") * 40, "state", "press 9", "state", "press 2",
                        "press F", "wait 50", "state", "press EXIT", "wait 50"))
    st = r.states
    check("UP/DOWN: 5 .. 40 WPM", st[1]["wpm"] == 40 and st[1]["dot"] == 30 and st[2]["wpm"] == 5
          and st[2]["dot"] == 240, st[1:3])
    check("1-9: sensitivity", st[3]["sens"] == 9 and st[4]["sens"] == 2, st[3:5])
    check("speed, sensitivity and the mode saved", r.cfg is not None and r.cfg[1] == 2 and r.cfg[3] == 5
          and r.cfg[4] == 1, r.cfg)
    r = Run("TEST", extra=("press MENU", "wait 50", "state"))
    check("MENU clears the text", r.states[0] and not r.text.replace("|", "").strip(), r.text)
    e = {"PATTERN": pattern("CQ DE TA2ABC"), "WPM": "15"}
    r = ht.Run(APP, NAME, script("host 1", "wait 50", "rx /echo off\\r", f"wait {600 + length('CQ DE TA2ABC', 15) + 2500}"),
               env=e)
    out = r.tx.decode()
    check("USB: banner, /echo off answered, the text as decoded, a new line after a pause",
          out.startswith("# Mors Okur 1.1 ready\r\n# echo off\r\n") and "CQ DE TA2ABC \r\n" in out, out)


def mockups():
    e = {"PATTERN": pattern("CQ CQ DE TA2ABC TA2ABC K"), "WPM": "18", "START": "700"}
    ht.Run(APP, NAME, script("wait 50", *press("UP") * 3, "wait 400", "wait 7000", "shot dinliyor"), env=e)
    ht.Run(APP, NAME, script("wait 300", "shot bos"), env={"PATTERN": ""})
    for name in ("dinliyor", "bos"):
        path = ht.png(APP, name)
        if path:
            print(f"  mockup {os.path.relpath(path, ht.ROOT)}")


if __name__ == "__main__":
    ht.build(APP, NAME)
    tests()
    mockups()
    ht.finish()
