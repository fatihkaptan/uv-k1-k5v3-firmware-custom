#!/usr/bin/env python3
# Copyright 2026 Fatih Kaptan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
"""
muzik - the computer side of the Muzik Kutusu overlay app: the radio's
speaker as a (one-voice) MIDI instrument over USB-C.

  muzik.py cal sarki.mid [--hiz 1.2] [--transpoze -12] [--kanal 1]
                                  play a MIDI file (its melody: the highest
                                  note sounding at each moment, drums left out)
  muzik.py klavye                 the computer keyboard as a piano
  muzik.py canli [--giris AD]     a MIDI keyboard (needs: pip install mido python-rtmidi)
  muzik.py kaydet cikti.mid       what is played on the radio's keypad -> .mid
  muzik.py bilgi sarki.mid        what is in a MIDI file
  muzik.py gom sarki.mid [--baslik "Ad"] [--bas 12 --sure 40]
                                  a MIDI file's melody -> a song of the app
                                  (App/apps/muzikkutusu/sarkilar/kendi.txt,
                                  not in git): rebuild and install the app

The radio's protocol is two commands per line: "n<MIDI note>" (60 = C4)
starts a note, "x" stops it; the radio sends the same when its keypad plays.
Needs pyserial; uses uvterm.py (../uvterm) for the port. Pure Python MIDI
reader and writer, no other dependency.
"""

import argparse
import os
import re
import struct
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "uvterm"))
import uvterm  # noqa: E402

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_name(n):
    return f"{NAMES[n % 12]}{n // 12 - 1}"


# ---------------------------------------------------------------------------
# MIDI files
# ---------------------------------------------------------------------------

class MidiError(Exception):
    pass


def _vlq(data, i):
    v = 0
    for _ in range(4):
        b = data[i]
        i += 1
        v = (v << 7) | (b & 0x7F)
        if not b & 0x80:
            return v, i
    raise MidiError("bozuk degisken uzunluklu sayi")


def read_midi(data):
    """(ticks per quarter, [events]): events = (tick, kind, a, b, track) with
    kind 'on' / 'off' (a = channel, b = note) or 'tempo' (a = us per quarter).
    A RIFF-wrapped file (RMID, .rmi) is unwrapped."""
    if data[:4] == b"RIFF" and data[8:12] == b"RMID" and b"MThd" in data:
        data = data[data.index(b"MThd"):]
    if data[:4] != b"MThd":
        raise MidiError("MIDI dosyasi degil (MThd yok)")
    hlen, fmt, ntrk, div = struct.unpack(">IHHH", data[4:14])
    if div & 0x8000:
        raise MidiError("SMPTE zamanlamasi desteklenmiyor")
    i, events = 8 + hlen, []
    for trk in range(ntrk):
        while data[i:i + 4] != b"MTrk":
            if i + 8 > len(data):
                raise MidiError("iz (MTrk) eksik")
            i += 8 + struct.unpack(">I", data[i + 4:i + 8])[0]   # skip unknown chunks
        size = struct.unpack(">I", data[i + 4:i + 8])[0]
        j, end, tick, status = i + 8, i + 8 + size, 0, 0
        while j < end:
            delta, j = _vlq(data, j)
            tick += delta
            b = data[j]
            if b & 0x80:
                status = b
                j += 1
            elif not status:
                raise MidiError("calisan durum (running status) baslangicsiz")
            kind = status & 0xF0
            if status == 0xFF:                  # meta
                mtype = data[j]
                mlen, j = _vlq(data, j + 1)
                if mtype == 0x51 and mlen == 3:
                    events.append((tick, "tempo", int.from_bytes(data[j:j + 3], "big"), 0, trk))
                j += mlen
                status = 0
                if mtype == 0x2F:
                    break
            elif status in (0xF0, 0xF7):        # sysex
                slen, j = _vlq(data, j)
                j += slen
                status = 0
            elif kind in (0x80, 0x90):
                note, vel = data[j], data[j + 1]
                j += 2
                on = kind == 0x90 and vel > 0
                events.append((tick, "on" if on else "off", status & 0x0F, note, trk))
            elif kind in (0xA0, 0xB0, 0xE0):
                j += 2
            elif kind in (0xC0, 0xD0):
                j += 1
            else:
                raise MidiError(f"bilinmeyen olay 0x{status:02X}")
        i = end
    events.sort(key=lambda e: (e[0], 0 if e[1] == "tempo" else 1 if e[1] == "off" else 2))
    return div, events


def melody(div, events, channel=None, transpose=0, drums=False):
    """[(seconds, note or 0)]: the highest note sounding at each change."""
    out, active, us, t_last, sec = [], {}, 500000, 0, 0.0
    for tick, kind, a, b, _ in events:
        sec += (tick - t_last) * us / 1e6 / div
        t_last = tick
        if kind == "tempo":
            us = a
            continue
        if (channel is not None and a != channel) or (not drums and a == 9):
            continue
        key = (a, b)
        if kind == "on":
            active[key] = active.get(key, 0) + 1
        elif key in active:
            active[key] -= 1
            if not active[key]:
                del active[key]
        top = max((n for _, n in active), default=0)
        top = top + transpose if top else 0
        if top and not 0 < top < 128:
            top = 0
        if out and abs(out[-1][0] - sec) < 1e-9:
            out[-1] = (sec, top)               # several events at once: the last state
        elif not out or out[-1][1] != top:
            out.append((sec, top))
    return [(t, n) for k, (t, n) in enumerate(out) if k == 0 or out[k - 1][1] != n]


def write_midi(notes, path, tpq=480, us=500000):
    """notes = [(start s, length s, MIDI note)] -> a format 0 file, 120 BPM."""
    ev = []
    for start, length, n in notes:
        ev.append((round(start * 1e6 / us * tpq), 1, n))
        ev.append((round((start + length) * 1e6 / us * tpq), 0, n))
    ev.sort()

    def vlq(v):
        out = [v & 0x7F]
        while v > 0x7F:
            v >>= 7
            out.insert(0, (v & 0x7F) | 0x80)
        return bytes(out)
    body, last = bytearray(b"\x00\xFF\x51\x03" + us.to_bytes(3, "big")), 0
    for tick, on, n in ev:
        body += vlq(tick - last) + bytes([0x90 if on else 0x80, n, 100 if on else 0])
        last = tick
    body += b"\x00\xFF\x2F\x00"
    data = b"MThd" + struct.pack(">IHHH", 6, 0, 1, tpq) + b"MTrk" + struct.pack(">I", len(body)) + bytes(body)
    with open(path, "wb") as f:
        f.write(data)
    return data


# ---------------------------------------------------------------------------
# the radio
# ---------------------------------------------------------------------------

def send(ser, cmd):
    ser.write(cmd.encode() + b"\r\n")
    ser.flush()


def play(ser, changes, speed=1.0, clock=time.perf_counter, sleep=time.sleep, show=print):
    """Send the changes on time; returns how many commands went out."""
    t0, sent = clock(), 0
    try:
        for t, n in changes:
            wait = t0 + t / speed - clock()
            if wait > 0:
                sleep(wait)
            send(ser, f"n{n}" if n else "x")
            sent += 1
            if show and n:
                show(f"\r  {note_name(n):4s} {t / speed:7.2f} s", end="", flush=True)
    finally:
        send(ser, "x")
    if show:
        show()
    return sent


def cmd_cal(args, ser):
    try:
        div, ev = read_midi(open(args.dosya, "rb").read())
    except (OSError, MidiError) as e:
        uvterm.die(str(e))
    ch = args.kanal - 1 if args.kanal else None
    m = melody(div, ev, ch, args.transpoze, args.davul)
    if not m:
        uvterm.die("dosyada calinacak nota yok")
    print(f"{args.dosya}: {sum(1 for _, n in m if n)} nota, {m[-1][0] / args.hiz:.1f} s. Ctrl+C: dur")
    time.sleep(0.3)
    try:
        play(ser, m, args.hiz)
    except KeyboardInterrupt:
        print()


# the computer keyboard: two rows like a piano (z / x: octave down / up)
KEYS = {"a": 0, "w": 1, "s": 2, "e": 3, "d": 4, "f": 5, "t": 6, "g": 7, "y": 8, "h": 9, "u": 10,
        "j": 11, "k": 12, "o": 13, "l": 14, "p": 15, ";": 16, "'": 17}


def cmd_klavye(args, ser):
    print("Bilgisayar klavyesi piyano: a s d f g h j k l = do re mi fa sol la si do re, "
          "w e t y u o p = diyezler, z/x oktav, q cikis")
    base = 60
    getch = _getch()
    off_at = [0.0]
    stop = threading.Event()

    def off_timer():
        while not stop.is_set():
            if off_at[0] and time.perf_counter() >= off_at[0]:
                send(ser, "x")
                off_at[0] = 0.0
            time.sleep(0.01)
    threading.Thread(target=off_timer, daemon=True).start()
    try:
        while True:
            c = getch()
            if c in ("q", "\x03", "\x1b"):
                break
            if c in "zx":
                base = max(36, base - 12) if c == "z" else min(96, base + 12)
                print(f"\r  oktav {base // 12 - 1}   ", end="", flush=True)
            elif c in KEYS:
                n = base + KEYS[c]
                send(ser, f"n{n}")
                off_at[0] = time.perf_counter() + 0.35
                print(f"\r  {note_name(n):4s}      ", end="", flush=True)
    finally:
        stop.set()
        send(ser, "x")
        print()


def _getch():
    if os.name == "nt":
        import msvcrt
        return lambda: msvcrt.getwch()
    import termios
    import tty

    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return getch


def cmd_canli(args, ser):
    try:
        import mido
    except ImportError:
        uvterm.die("MIDI klavye icin: pip install mido python-rtmidi")
    names = mido.get_input_names()
    if not names:
        uvterm.die("MIDI girisi yok: klavyeyi takin (muzik.py canli --liste)")
    if args.liste:
        print("\n".join(names))
        return
    name = args.giris or names[0]
    print(f"{name} -> telsiz. Ctrl+C: cikis")
    held = []
    with mido.open_input(name) as port:
        try:
            for msg in port:
                if msg.type == "note_on" and msg.velocity:
                    held.append(msg.note)
                elif msg.type in ("note_on", "note_off") and msg.note in held:
                    held.remove(msg.note)
                else:
                    continue
                send(ser, f"n{held[-1]}" if held else "x")   # the last key held sounds
        except KeyboardInterrupt:
            send(ser, "x")


def record(lines, clock=time.perf_counter):
    """Yields (start s, length s, note) from the radio's n/x lines as each
    note ends (a new n, or x)."""
    cur, t0 = None, None
    for line in lines:
        t = clock()
        if t0 is None:
            t0 = t
        if cur:
            yield (cur[1] - t0, t - cur[1], cur[0])
            cur = None
        if line.startswith("n") and line[1:].isdigit():
            cur = (int(line[1:]), t)


def cmd_kaydet(args, ser):
    print(f"Telsizde Piyano'yu acin ve calin; Ctrl+C ile bitirin -> {args.dosya}")
    stop = threading.Event()

    def lines():
        buf = b""
        while not stop.is_set():
            buf += ser.read(64)
            while b"\n" in buf:
                line, _, buf = buf.partition(b"\n")
                line = line.strip().decode("ascii", "replace")
                if line == "x" or (line.startswith("n") and line[1:].isdigit()):
                    if line != "x":
                        print(f"\r  {note_name(int(line[1:])):4s}", end="", flush=True)
                    yield line
    got = []
    try:
        for item in record(lines()):
            got.append(item)
    except KeyboardInterrupt:
        pass
    stop.set()
    notes = got
    if not notes:
        uvterm.die("hic nota gelmedi", 0)
    write_midi(notes, args.dosya)
    print(f"\n{len(notes)} nota -> {args.dosya}")


# ---------------------------------------------------------------------------
# gom: a MIDI file -> a song of the app (sarkilar/kendi.txt)
# ---------------------------------------------------------------------------

SONG_FILE = os.path.join(HERE, "..", "..", "App", "apps", "muzikkutusu", "sarkilar", "kendi.txt")
TR = str.maketrans("çğıöşüÇĞİÖŞÜâîûÂÎÛ", "cgiosuCGIOSUaiuAIU")


def length(u):
    """32nds -> the song file's length: 8 -> '/4', 12 -> '/4.', 5 -> '*5/32'."""
    from fractions import Fraction
    fr = Fraction(u, 32)
    if fr.numerator == 1:
        return f"/{fr.denominator}"
    if fr.numerator == 3 and fr.denominator % 2 == 0:
        return f"/{fr.denominator // 2}."
    return f"*{fr.numerator}/{fr.denominator}"


def to_song(m, bpm, start=0.0, dur=None, legato=True):
    """A melody [(seconds, note or 0)] -> ([(note or 0, 32nds)], why it was
    cut or None). Lengths on a 1/32 grid at bpm, octaves folded into the
    app's C3 .. C7; with legato a rest of a 1/16 or less is added to the note
    before it (the app detaches its notes anyway: half the events for a
    staccato file). It stops before the 256th note, the 16th pitch or the
    17th length (the app's limits for one song)."""
    q = 60.0 / bpm / 8
    cap = max(1, min(256, int(8 * bpm)))          # <= 60 s a note
    ev = []
    for k in range(len(m) - 1):
        t, n = m[k]
        t1 = m[k + 1][0]
        if t1 <= start + 1e-9:
            continue
        if dur is not None and t >= start + dur:
            break
        t = max(t, start)
        if dur is not None:
            t1 = min(t1, start + dur)
        u = round((t1 - start) / q) - round((t - start) / q)
        if u <= 0:
            continue
        while n and n < 48:
            n += 12
        while n > 96:
            n -= 12
        if ev and not n and (not ev[-1][0] or (legato and u <= 2)):
            ev[-1][1] += u                             # rests merged, short ones into the note
        else:
            ev.append([n, u])
    while ev and not ev[0][0]:
        ev.pop(0)
    while ev and not ev[-1][0]:
        ev.pop()
    out, pitches, lens, why = [], set(), set(), None
    for n, u in ev:
        while u > 0:
            v = min(u, cap)
            if len(out) == 255:
                why = "255 nota"
            elif n and n not in pitches and len(pitches) == 15:
                why = f"16. perde ({note_name(n)})"
            elif v not in lens and len(lens) == 16:
                why = "17. uzunluk"
            if why:
                return out, why
            out.append((n, v))
            pitches.add(n) if n else None
            lens.add(v)
            u -= v
    return out, None


def song_text(title, bpm, ev, makam=""):
    toks = [(note_name(n) if n else "R") + length(u) for n, u in ev]
    return (f"= {title} | {makam} | {bpm:g}\n"
            + "\n".join(" ".join(toks[i:i + 12]) for i in range(0, len(toks), 12)) + "\n")


def put_song(path, title, text):
    """Write (or replace, same title) one song in the song file."""
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else \
        "# Muzik Kutusu - kendi sarkilarim (git'e girmez). Bicim: gen_assets.py\n"
    blocks = re.split(r"(?m)^(?==)", old)
    keep = [b for b in blocks if not re.match(r"=\s*" + re.escape(title) + r"\s*\|", b)]
    new = "".join(keep).rstrip("\n") + "\n\n" + text
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    return len(keep) != len(blocks)


def cmd_gom(args, _ser=None):
    try:
        div, ev = read_midi(open(args.dosya, "rb").read())
    except (OSError, MidiError) as e:
        uvterm.die(str(e))
    ch = args.kanal - 1 if args.kanal else None
    m = melody(div, ev, ch, args.transpoze, args.davul)
    us = next((a for _, k, a, _, _ in ev if k == "tempo"), 500000)
    bpm = args.bpm or round(60e6 / us, 1)
    ev2, why = to_song(m, bpm, args.bas, args.sure, not args.suslar)
    if not ev2:
        uvterm.die("dosyada gomulecek nota yok")
    title = (args.baslik or os.path.splitext(os.path.basename(args.dosya))[0]).translate(TR)
    title = "".join(c for c in title if c.isascii() and c.isprintable() and c not in "|#")[:16].strip() or "Sarki"
    makam = "".join(c for c in args.makam.translate(TR) if c.isascii() and c.isalnum())[:8]
    shown = round(bpm * args.hiz, 1)
    replaced = put_song(args.cikti, title, song_text(title, shown, ev2, makam))
    secs = sum(u for _, u in ev2) * 60 / shown / 8
    print(f"'{title}': {sum(1 for n, _ in ev2 if n)} nota, {len({n for n, _ in ev2 if n})} perde, "
          f"{secs:.1f} s, {shown:g} BPM -> {os.path.relpath(args.cikti)}" + (" (eskisinin yerine)" if replaced else ""))
    if why:
        print(f"  uygulamanin sinirinda kesildi ({why}): --bas / --sure ile baska bir bolum secilebilir")
    print("  telsize: ./compile-app.sh muzikkutusu, sonra App/apps/muzikkutusu/MuzikKutusu.app'i yukle")


def cmd_bilgi(args, _ser=None):
    div, ev = read_midi(open(args.dosya, "rb").read())
    chans = sorted({a for _, k, a, _, _ in ev if k == "on"})
    m = melody(div, ev)
    print(f"{args.dosya}: {div} tik/ceyrek, kanallar {[c + 1 for c in chans]}, "
          f"melodi {sum(1 for _, n in m if n)} nota, {m[-1][0] if m else 0:.1f} s")


def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-p", "--port", default=argparse.SUPPRESS, help="seri port (varsayilan: otomatik)")
    ap = argparse.ArgumentParser(prog="muzik.py", description="Muzik Kutusu icin PC araci.")
    ap.add_argument("-p", "--port")
    sub = ap.add_subparsers(dest="cmd", metavar="komut", required=True)
    c = sub.add_parser("cal", parents=[common], help="MIDI dosyasi cal")
    c.add_argument("dosya")
    c.add_argument("--hiz", type=float, default=1.0, help="hiz carpani (1.0 = asli)")
    c.add_argument("--transpoze", type=int, default=0, help="yarim ses kaydir (-12 = bir oktav asagi)")
    c.add_argument("--kanal", type=int, help="yalnizca bu MIDI kanali (1-16)")
    c.add_argument("--davul", action="store_true", help="10. kanali (davul) da kat")
    sub.add_parser("klavye", parents=[common], help="bilgisayar klavyesi piyano")
    c = sub.add_parser("canli", parents=[common], help="MIDI klavye -> telsiz")
    c.add_argument("--giris", help="MIDI giris adi")
    c.add_argument("--liste", action="store_true", help="MIDI girislerini listele")
    c = sub.add_parser("kaydet", parents=[common], help="telsizde calinani .mid olarak kaydet")
    c.add_argument("dosya")
    c = sub.add_parser("bilgi", help="MIDI dosyasi hakkinda")
    c.add_argument("dosya")
    c = sub.add_parser("gom", help="MIDI'nin melodisini uygulamaya sarki olarak ekle (kendi.txt)")
    c.add_argument("dosya")
    c.add_argument("--baslik", help="listede gorunen ad (<= 16 harf; varsayilan dosya adi)")
    c.add_argument("--makam", default="", help="calarken ustte gorunen makam/tur (istege bagli)")
    c.add_argument("--bas", type=float, default=0.0, help="bu saniyeden basla")
    c.add_argument("--sure", type=float, help="en fazla bu kadar saniye al")
    c.add_argument("--bpm", type=float, help="tempo (varsayilan: dosyanin ilk temposu)")
    c.add_argument("--hiz", type=float, default=1.0, help="hiz carpani (1.0 = asli)")
    c.add_argument("--transpoze", type=int, default=0, help="yarim ses kaydir (-12 = bir oktav asagi)")
    c.add_argument("--kanal", type=int, help="yalnizca bu MIDI kanali (1-16)")
    c.add_argument("--davul", action="store_true", help="10. kanali (davul) da kat")
    c.add_argument("--suslar", action="store_true", help="1/16'dan kisa suslari da koru (varsayilan: notaya katilir)")
    c.add_argument("--cikti", default=SONG_FILE, help="sarki dosyasi (varsayilan: sarkilar/kendi.txt)")
    args = ap.parse_args(argv)
    if args.cmd in ("bilgi", "gom"):
        return {"bilgi": cmd_bilgi, "gom": cmd_gom}[args.cmd](args)
    uvterm.need_pyserial()
    ser = uvterm.open_port(uvterm.find_port(args.port))
    try:
        {"cal": cmd_cal, "klavye": cmd_klavye, "canli": cmd_canli, "kaydet": cmd_kaydet}[args.cmd](args, ser)
    finally:
        ser.close()


if __name__ == "__main__":
    main()
