#!/usr/bin/env python3
# Muzik Kutusu read-only assets: texts, the BK4819 tone register value of
# every piano note, the songs, and the 1024-byte block where the loader keeps
# the last keypad recording (APP_FLAG_SAVE_SCREEN).
#
#   ./gen_assets.py muzikkutusu_assets.bin muzikkutusu_assets.h
#
# The songs are read from text files, in this order (missing ones skipped):
#   sarkilar/kendi.txt     your own (not in git; tools/muzik/muzik.py gom)
#   sarkilar/turkuler.txt  Turkish songs in komas (derived from SymbTr,
#                          CC BY-NC-SA 4.0: see the file)
#   sarkilar/klasik.txt    public-domain melodies
#
# Song file format, a line starting with "#" is a comment:
#   = Title | Makam | BPM          title <= 16 ASCII, makam may be empty,
#                                  BPM = quarter notes a minute
#   C4/4 D#4/8 Eb4/8. R/2 F5#3/16 B4b1*5/8 ...
# A note: R (rest), C#4 / Db4 (equal temperament, C4 = middle C) or C5#4 /
# B4b1 (53-TET: the natural raised # or lowered b by that many komas, as in
# Turkish notation), then the length: /8 an eighth, /8. a dotted eighth,
# *5/8 five eighths. A song: at most 255 notes, 15 different pitches and 16
# different lengths. Songs that do not fit the asset space are dropped from
# the end, with a warning.
import math, os, re, struct, sys
from fractions import Fraction
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from app_assets import Assets, ASSET_MAX

VER = os.environ.get("APP_VER", "1.1")
LO, HI = 48, 96            # the piano's tone table: C3 .. C7
FILES = ["kendi.txt", "turkuler.txt", "klasik.txt"]
SAVE_SIZE = 1024
a = Assets("MUZIKKUTUSU")

# ---- screens ----
a.text("T_TITLE", "MUZIK KUTUSU")
a.table("T_MENU", ["Sarkilar", "Piyano", "Ses: "])
a.text("T_HINT", "1-3 sec  MENU gir  EXIT cik")
a.text("T_USB", "USB: PC'den MIDI calar")
a.table("T_NOTE", ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
a.text("T_HZ", " Hz")
a.text("T_BPM", " BPM")
a.text("T_OCT", "Oktav ")
a.text("T_REC", "REC")
a.text("T_PLAY", "CAL")
a.text("T_PC", "PC")
a.text("T_PIANOHINT", "* diyez MENU kayit F cal")
a.text("T_RECN", "Kayit: ")
a.text("T_NOTA", " nota")
a.text("T_BANNER", f"# Muzik Kutusu {VER} ready")
a.text("T_ECHO", "# echo off")


def reg(hz):
    """BK4819 REG_71 for a tone: Hz x 1353245 / 2^17 (the firmware's
    scale_freq() rounds the Hz first; the piano does the same)."""
    return round(hz * 1353245 / (1 << 17))


def hz12(n):
    return 440.0 * 2 ** ((n - 69) / 12)


TONE = [(round(hz12(n)) * 1353245 + (1 << 16)) >> 17 for n in range(LO, HI + 1)]
NTONE = len(TONE)

# ---- songs ----
SEMI = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
NATURAL = {"C": 0, "D": 9, "E": 18, "F": 22, "G": 31, "A": 40, "B": 49}   # komas above C
TOKEN = re.compile(r"(R|[A-G][#b]?\d|[A-G]\d[#b]\d)(?:/(\d+)(\.?)|\*(\d+)/(\d+))")
KOMA = []                  # the 53-TET pitches in use: (koma, name)


def pitch(p, where):
    """A global pitch index: 0 .. NTONE-1 the piano's notes, then KOMA."""
    if p[1:2] in ("#", "b") or p[1:].isdigit():                   # C#4, Db4, C4
        n = 12 * (int(p[-1]) + 1) + SEMI[p[0]] + {"#": 1, "b": -1}.get(p[1], 0)
    else:                                                          # C5#4, B4b1
        k = 265 + 53 * (int(p[1]) - 4) + NATURAL[p[0]] + int(p[3]) * (1 if p[2] == "#" else -1)
        hz = 440.0 * 2 ** ((k - 305) / 53)
        n = round(69 + 12 * math.log2(hz / 440))
        if abs(1200 * math.log2(hz / hz12(n))) > 3:                # not an equal-tempered note
            if not any(kk == k for kk, _ in KOMA):
                KOMA.append((k, p))
            return NTONE + next(i for i, (kk, _) in enumerate(KOMA) if kk == k)
    if not LO <= n <= HI:
        sys.exit(f"{where}: {p} outside C3 .. C7")
    return n - LO


def songs(path):
    out, cur = [], None
    for no, line in enumerate(open(path, encoding="utf-8"), 1):
        line = "" if line.lstrip().startswith("#") else line.strip()      # "#" also means sharp
        where = f"{os.path.basename(path)}:{no}"
        if line.startswith("="):
            f = [x.strip() for x in line[1:].split("|")]
            if len(f) != 3 or not f[0] or len(f[0]) > 16 or not f[0].isascii() or not f[1].isascii():
                sys.exit(f"{where}: '= Title (<= 16 ASCII) | Makam | BPM' expected")
            cur = {"title": f[0], "makam": f[1], "bpm": float(f[2]), "ev": [], "where": where}
            out.append(cur)
        elif line:
            if cur is None:
                sys.exit(f"{where}: notes before the first '= Title | Makam | BPM' line")
            for tok in line.split():
                m = TOKEN.fullmatch(tok)
                if not m:
                    sys.exit(f"{where}: bad note {tok!r}")
                fr = Fraction(1, int(m[2])) * (Fraction(3, 2) if m[3] else 1) if m[2] else Fraction(int(m[4]), int(m[5]))
                ms = round(fr * 240000 / cur["bpm"])
                if not 1 <= ms <= 65535:
                    sys.exit(f"{where}: {tok}: {ms} ms")
                cur["ev"].append((None if m[1] == "R" else pitch(m[1], where), ms))
    return out


def blob(s, makam):
    ev = s["ev"]
    pal = list(dict.fromkeys(p for p, _ in ev if p is not None))
    durs = list(dict.fromkeys(ms for _, ms in ev))
    w = f"{s['where']} '{s['title']}'"
    if not ev or len(ev) > 255 or len(pal) > 15 or len(durs) > 16:
        sys.exit(f"{w}: {len(ev)} notes, {len(pal)} pitches, {len(durs)} lengths (max 255, 15, 16)")
    # header: BPM, note count, makam, pitches, lengths, title NUL; the
    # pitches (global index), the lengths (ms at 100 %), then one byte a note:
    # pitch << 4 | length, pitch 15 = rest
    return (bytes([min(255, round(s["bpm"])), len(ev), makam, len(pal), len(durs)]) + s["title"].encode() + b"\0"
            + bytes(pal) + struct.pack(f"<{len(durs)}H", *durs)
            + bytes((15 if p is None else pal.index(p)) << 4 | durs.index(ms) for p, ms in ev))


SONGS = [s for f in FILES if os.path.exists(os.path.join(HERE, "sarkilar", f))
         for s in songs(os.path.join(HERE, "sarkilar", f))]
MAKAMS = [""] + list(dict.fromkeys(s["makam"] for s in SONGS if s["makam"]))

# the space left for the songs: everything else is fixed
fixed = sum(len(p) for _, p in a.texts) + 2 * NTONE + SAVE_SIZE + sum(len(m) + 1 for m in MAKAMS) * 2
while True:
    used = sorted({p for s in SONGS for p, _ in s["ev"] if p is not None and p >= NTONE})
    knames = max([len(KOMA[p - NTONE][1]) + 1 for p in used] or [1])
    blobs = [blob(s, MAKAMS.index(s["makam"])) for s in SONGS]
    size = fixed + sum(map(len, blobs)) + 2 * len(blobs) + len(used) * (3 + knames)
    if size <= ASSET_MAX or len(SONGS) == 1:
        break
    print(f"gen_assets.py: no room for '{SONGS[-1]['title']}' ({size} > {ASSET_MAX} B), dropped",
          file=sys.stderr)
    SONGS.pop()

# the 53-TET pitches the songs use, renumbered: REG_71, the nearest piano key
# (for the keyboard drawing), the name shown
used = sorted({p for s in SONGS for p, _ in s["ev"] if p is not None and p >= NTONE})
remap = {p: NTONE + i for i, p in enumerate(used)}
for s in SONGS:
    s["ev"] = [(remap.get(p, p), ms) for p, ms in s["ev"]]
KUSED = [KOMA[p - NTONE] for p in used]
assert NTONE + len(KUSED) <= 255
a.table("T_MAKAM", MAKAMS)
a.table("KNAME", [n for _, n in KUSED] or [""])
a.u16("TONE", TONE)
a.u16("KREG", [reg(440.0 * 2 ** ((k - 305) / 53)) for k, _ in KUSED] or [0])
a.u8("KMIDI", [round(69 + 12 * math.log2(2 ** ((k - 305) / 53))) for k, _ in KUSED] or [0])
a.const("NOTE_LO", LO)
a.const("NOTE_HI", HI)
a.const("NTONE", NTONE)
offs, data = [], bytearray()
for s in SONGS:
    offs.append(len(data))
    data += blob(s, MAKAMS.index(s["makam"]))
a.u16("SONG_OFF", offs)
a.raw("SONG", data)
a.const("NSONG", len(SONGS))

# ---- the saved recording (must stay the last item: the loader writes the
# screen it leaves at exit over the last 1024 bytes of the assets) ----
a.raw("SAVE", bytes(SAVE_SIZE))
if __name__ == "__main__":
    a.main()
