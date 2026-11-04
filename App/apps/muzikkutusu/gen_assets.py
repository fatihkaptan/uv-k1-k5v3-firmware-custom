#!/usr/bin/env python3
# Muzik Kutusu read-only assets: texts, the BK4819 tone register value of
# every note it plays, the built-in melodies, and the 1024-byte block where
# the loader keeps the last keypad recording (APP_FLAG_SAVE_SCREEN).
#
#   ./gen_assets.py muzikkutusu_assets.bin muzikkutusu_assets.h
#
# Melodies are written as text: "C4/4 D#4/2 R/1" = note (C, C#/Db ... B, R for
# a rest), octave (MIDI: C4 = 60), "/" duration in sixteenths. Every one here
# is in the public domain (traditional, or composers dead for over a century).
# To add your own, append to SONGS and rebuild.
import os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from app_assets import Assets

VER = os.environ.get("APP_VER", "1.0")
LO, HI = 48, 96            # the notes the tone table covers: C3 .. C7
a = Assets("MUZIKKUTUSU")

# ---- screens ----
a.text("T_TITLE", "MUZIK KUTUSU")
a.table("T_MENU", ["Melodiler", "Piyano", "Ses: "])
a.text("T_HINT", "1-3 sec  MENU gir  EXIT cik")
a.text("T_USB", "USB: PC'den MIDI calar")
a.table("T_NOTE", ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
a.text("T_HZ", " Hz")
a.text("T_BPM", " BPM")
a.text("T_OCT", "Oktav ")
a.text("T_REC", "REC")
a.text("T_PLAY", "CAL")
a.text("T_PC", "PC")
a.text("T_SONGHINT", "MENU cal/dur  UP/DN tempo")
a.text("T_PIANOHINT", "* diyez MENU kayit F cal")
a.text("T_RECN", "Kayit: ")
a.text("T_NOTA", " nota")
a.text("T_BANNER", f"# Muzik Kutusu {VER} ready")
a.text("T_ECHO", "# echo off")

# ---- BK4819 REG_71 for MIDI notes LO..HI: Hz x 1353245 / 2^17, rounded,
# as the firmware's scale_freq() ----
regs = []
for n in range(LO, HI + 1):
    hz = 440.0 * 2 ** ((n - 69) / 12)
    regs.append((round(hz) * 1353245 + (1 << 16)) >> 17)
a.u16("TONE", regs)
a.u16("HZ", [round(440.0 * 2 ** ((n - 69) / 12)) for n in range(LO, HI + 1)])
a.const("NOTE_LO", LO)
a.const("NOTE_HI", HI)

# ---- melodies ----
NAMES = {"C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3, "E": 4, "F": 5, "F#": 6, "GB": 6,
         "G": 7, "G#": 8, "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11}


def notes(text):
    out = []
    for tok in text.split():
        m = re.fullmatch(r"([A-Ga-g][#bB]?|R)(-?\d)?/(\d+)", tok)
        if not m:
            sys.exit(f"bad note {tok!r}")
        name, octv, dur = m.group(1).upper(), m.group(2), int(m.group(3))
        n = 0 if name == "R" else 12 * (int(octv) + 1) + NAMES[name]
        if n and not LO <= n <= HI:
            sys.exit(f"note {tok} outside C3..C7")
        assert 1 <= dur <= 64, tok
        out += [n, dur]
    return out


def morse(text, note="F5"):
    code = {"C": "-.-.", "Q": "--.-", "D": "-..", "E": ".", "T": "-", "A": ".-", "7": "--...",
            "3": "...--"}
    out = []
    for word in text.split():
        for letter in word:
            for i, s in enumerate(code[letter]):
                out.append(f"{note}/{1 if s == '.' else 3}")
                out.append("R/1")
            out[-1] = "R/3"
        out[-1] = "R/7"
    return " ".join(out)


TWINKLE = "C4/4 C4/4 G4/4 G4/4 A4/4 A4/4 G4/8 F4/4 F4/4 E4/4 E4/4 D4/4 D4/4 C4/8 "
SONGS = [
    ("Daha Dun Annemiz", 100,
     TWINKLE + "G4/4 G4/4 F4/4 F4/4 E4/4 E4/4 D4/8 G4/4 G4/4 F4/4 F4/4 E4/4 E4/4 D4/8 " + TWINKLE),
    ("Nese Marsi", 110,                                    # Beethoven, 9th symphony
     "E4/4 E4/4 F4/4 G4/4 G4/4 F4/4 E4/4 D4/4 C4/4 C4/4 D4/4 E4/4 E4/6 D4/2 D4/8 "
     "E4/4 E4/4 F4/4 G4/4 G4/4 F4/4 E4/4 D4/4 C4/4 C4/4 D4/4 E4/4 D4/6 C4/2 C4/8"),
    ("Fur Elise", 75,                                      # Beethoven
     "E5/1 D#5/1 E5/1 D#5/1 E5/1 B4/1 D5/1 C5/1 A4/2 R/1 C4/1 E4/1 A4/1 B4/2 R/1 E4/1 G#4/1 B4/1 "
     "C5/2 R/1 E4/1 E5/1 D#5/1 E5/1 D#5/1 E5/1 B4/1 D5/1 C5/1 A4/2 R/1 C4/1 E4/1 A4/1 "
     "B4/2 R/1 E4/1 C5/1 B4/1 A4/6"),
    ("Iyi ki Dogdun", 100,
     "G4/3 G4/1 A4/4 G4/4 C5/4 B4/8 G4/3 G4/1 A4/4 G4/4 D5/4 C5/8 "
     "G4/3 G4/1 G5/4 E5/4 C5/4 B4/4 A4/8 F5/3 F5/1 E5/4 C5/4 D5/4 C5/8"),
    ("Jingle Bells", 140,                                  # Pierpont, 1857
     "E4/2 E4/2 E4/4 E4/2 E4/2 E4/4 E4/2 G4/2 C4/3 D4/1 E4/8 F4/2 F4/2 F4/3 F4/1 "
     "F4/2 E4/2 E4/2 E4/1 E4/1 E4/2 D4/2 D4/2 E4/2 D4/4 G4/4 "
     "E4/2 E4/2 E4/4 E4/2 E4/2 E4/4 E4/2 G4/2 C4/3 D4/1 E4/8 F4/2 F4/2 F4/3 F4/1 "
     "F4/2 E4/2 E4/2 E4/1 E4/1 G4/2 G4/2 F4/2 D4/2 C4/8"),
    ("Tembel Cocuk", 120,                                  # Frere Jacques
     "C4/4 D4/4 E4/4 C4/4 C4/4 D4/4 E4/4 C4/4 E4/4 F4/4 G4/8 E4/4 F4/4 G4/8 "
     "G4/2 A4/2 G4/2 F4/2 E4/4 C4/4 G4/2 A4/2 G4/2 F4/2 E4/4 C4/4 "
     "C4/4 G3/4 C4/8 C4/4 G3/4 C4/8"),
    ("Menuet Sol Majr", 120,                              # Petzold, BWV Anh. 114
     "D5/4 G4/2 A4/2 B4/2 C5/2 D5/4 G4/4 G4/4 E5/4 C5/2 D5/2 E5/2 F#5/2 G5/4 G4/4 G4/4 "
     "C5/4 D5/2 C5/2 B4/2 A4/2 B4/4 C5/2 B4/2 A4/2 G4/2 F#4/4 G4/2 A4/2 B4/2 G4/2 A4/12"),
    ("CQ CQ (Mors)", 250, morse("CQ CQ")),
]
blob, offs = bytearray(), []
for title, bpm, text in SONGS:
    ns = notes(text)
    assert len(title) <= 16 and len(ns) // 2 <= 255, title
    offs.append(len(blob))
    # header: ms per sixteenth, note count, title NUL; then (note, sixteenths)
    blob += bytes([round(15000 / bpm), len(ns) // 2]) + title.encode() + b"\0" + bytes(ns)
a.u16("SONG_OFF", offs)
a.raw("SONG", blob)
a.const("NSONG", len(SONGS))

# ---- the saved recording (must stay the last item: the loader writes the
# screen it leaves at exit over the last 1024 bytes of the assets) ----
a.raw("SAVE", bytes(1024))
a.main()
