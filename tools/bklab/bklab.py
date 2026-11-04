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
bklab - the computer side of the BK Lab overlay app: the BK4819 / BK4829
registers of a UV-K1 / UV-K5 V3 from a shell or from Python.

  bklab.py                     interactive shell (help: yardim)
  bklab.py betik dosya.txt     run the shell commands of a file
  bklab.py fark a.txt b.txt    compare two register dumps (offline)

From Python:

  from bklab import BK
  bk = BK.open()                 # finds the radio (USB VID:PID 36B7:FFFF)
  bk.read(0x13); bk.write(0x13, 0x03D9); bk.status(); bk.dump(); bk.restore()

Shell commands (hex registers and values): r 13 [n], w 13 03D9, w! 30 BFF1
(protected: can key the transmitter), d, s, m 67 [ms], geri, kaydet dosya,
tara 13 03D0 03DF [adim] [bekle_ms] (write each value, read RSSI / noise),
cik. Needs pyserial and uvterm.py (../uvterm).
"""

import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "uvterm"))

# the app's table (App/apps/bklab/gen_assets.py; the tests keep them equal)
NAMES = {
    0x02: "IRQ DURUM", 0x07: "CTC FREK", 0x0B: "DURUM", 0x0C: "IRQ VAR", 0x0D: "TARAMA 1",
    0x0E: "TARAMA 2", 0x10: "KAZANC 0", 0x11: "KAZANC 1", 0x12: "KAZANC 2", 0x13: "KAZANC 3",
    0x14: "KAZANC 4", 0x19: "MIC AGC", 0x20: "AGC", 0x21: "DTMF", 0x24: "DTMF ALGI",
    0x28: "GENISLET", 0x29: "SIKISTIR", 0x2B: "KARISTIR", 0x30: "GUC ETKIN", 0x31: "OZELLIK",
    0x32: "TARAMA", 0x33: "GPIO", 0x36: "PA", 0x37: "LDO OSC", 0x38: "FREK ALT",
    0x39: "FREK UST", 0x3F: "IRQ ETKIN", 0x43: "FILTRE BW", 0x46: "VOX ESIK", 0x47: "AF CIKIS",
    0x48: "AF KAZANC", 0x49: "AGC ESIK", 0x4D: "SQ GLITCH", 0x4E: "SQ GECIKM", 0x4F: "SQ GURULT",
    0x50: "TX SUSTUR", 0x51: "CTCSS DCS", 0x58: "FSK", 0x59: "FSK KONT", 0x5A: "FSK SYNC",
    0x5B: "FSK SYNC", 0x5C: "FSK CRC", 0x5D: "FSK BOY", 0x5F: "FSK FIFO", 0x63: "GLITCH",
    0x64: "SES GENL", 0x65: "GURULTU", 0x67: "RSSI", 0x68: "CTC SONUC", 0x69: "DCS SONUC",
    0x6A: "DCS SONUC", 0x6F: "AF TX/RX", 0x70: "TON KONT", 0x71: "TON1 FRK", 0x72: "TON2 FRK",
    0x78: "SQ RSSI", 0x79: "VOX", 0x7A: "VOX GECIK", 0x7B: "AGC TABLO", 0x7D: "MIC HASS",
    0x7E: "AGC SABIT",
}
PROTECTED = {0x30, 0x33, 0x36}


class BKError(Exception):
    pass


class BK:
    """The BK Lab app's line protocol."""

    def __init__(self, ser, timeout=2.0):
        self.ser = ser
        self.timeout = timeout
        self.buf = b""

    @classmethod
    def open(cls, port=None):
        import uvterm
        uvterm.need_pyserial()
        ser = uvterm.open_port(uvterm.find_port(port))
        time.sleep(0.3)
        return cls(ser)

    def close(self):
        self.ser.close()

    def _lines(self, cmd, count=None, until=None):
        self.ser.reset_input_buffer()
        self.buf = b""
        self.ser.write(cmd.encode() + b"\r\n")
        self.ser.flush()
        out, end = [], time.time() + self.timeout
        while time.time() < end:
            self.buf += self.ser.read(256)
            while b"\n" in self.buf:
                line, _, self.buf = self.buf.partition(b"\n")
                line = line.strip().decode("ascii", "replace")
                if not line or line.startswith("# BK Lab"):
                    continue
                if line.startswith("!"):
                    raise BKError(line[1:].strip())
                out.append(line)
                if (count and len(out) >= count) or (until and until(line)):
                    return out
        raise BKError(f"telsiz '{cmd}' komutuna cevap vermedi: BK Lab acik mi?")

    @staticmethod
    def _reg(line):
        m = re.fullmatch(r"([0-9A-F]{2})=([0-9A-F]{4})", line)
        if not m:
            raise BKError(f"beklenmeyen cevap: {line}")
        return int(m.group(1), 16), int(m.group(2), 16)

    def read(self, reg, n=1):
        vals = [self._reg(l)[1] for l in self._lines(f"r {reg:02X} {n:X}", count=n)]
        return vals[0] if n == 1 else vals

    def write(self, reg, value, force=False):
        """Write and read back; a protected register needs force=True."""
        if reg in PROTECTED and not force:
            raise BKError(f"0x{reg:02X} korumali (verici acilabilir): force=True")
        line = self._lines(f"w{'!' if force else ''} {reg:02X} {value & 0xFFFF:04X}", count=1)[0]
        return self._reg(line)[1]

    def dump(self):
        vals = []
        for line in self._lines("d", count=16):
            vals += [int(x, 16) for x in line.split(":")[1].split()]
        return vals

    def status(self):
        line = self._lines("s", count=1)[0]
        m = re.fullmatch(r"RSSI (-?[\d.]+)\s+Gr (\d+)\s+Gl (\d+)", line)
        if not m:
            raise BKError(f"beklenmeyen cevap: {line}")
        return {"rssi": float(m.group(1)), "gurultu": int(m.group(2)), "glitch": int(m.group(3))}

    def restore(self):
        line = self._lines("geri", count=1)[0]
        return int(line.rsplit(" ", 1)[1])

    def monitor(self, reg, ms=100, seconds=2.0):
        """[(seconds, value)] streamed by the radio, then stopped."""
        self.ser.reset_input_buffer()
        self.ser.write(f"m {reg:02X} {int(ms)}\r\n".encode())
        t0, out, buf = time.time(), [], b""
        while time.time() - t0 < seconds:
            buf += self.ser.read(256)
            while b"\n" in buf:
                line, _, buf = buf.partition(b"\n")
                line = line.strip().decode("ascii", "replace")
                if re.fullmatch(r"[0-9A-F]{2}=[0-9A-F]{4}", line):
                    out.append((time.time() - t0, self._reg(line)[1]))
        self.ser.write(b"x\r\n")
        time.sleep(0.1)
        self.ser.reset_input_buffer()
        return out

    def sweep(self, reg, start, stop, step=1, wait_ms=100):
        """Write each value, wait, read the meters: [(value, status)]; the
        register is written back as it was."""
        old = self.read(reg)
        out = []
        try:
            for v in range(start, stop + 1, step):
                self.write(reg, v)
                time.sleep(wait_ms / 1000)
                out.append((v, self.status()))
        finally:
            self.write(reg, old)
        return out


def name(reg):
    return NAMES.get(reg, "")


def bits(v):
    return " ".join(f"{(v >> s) & 0xF:04b}" for s in (12, 8, 4, 0))


def fmt_dump(vals):
    return "\n".join(f"{r:02X}  {v:04X}  {bits(v)}  {name(r)}" for r, v in enumerate(vals))


def parse_dump(text):
    vals = {}
    for line in text.splitlines():
        m = re.match(r"\s*([0-9A-Fa-f]{2})\s+([0-9A-Fa-f]{4})\b", line)
        if m:
            vals[int(m.group(1), 16)] = int(m.group(2), 16)
    return vals


def diff(a, b):
    """Lines for the registers whose values differ, with the changed bits."""
    out = []
    for r in sorted(set(a) & set(b)):
        if a[r] != b[r]:
            changed = [str(i) for i in range(15, -1, -1) if (a[r] ^ b[r]) >> i & 1]
            out.append(f"{r:02X}  {a[r]:04X} -> {b[r]:04X}  bit {','.join(changed)}  {name(r)}")
    return out


HELP = """Komutlar (onaltilik):
  r 13 [n]          oku (n tane)          w 13 03D9      yaz (okuyup gosterir)
  w! 30 BFF1        korumali yaz (TX!)    d              tum registerlar, bitler, adlar
  s                 RSSI, gurultu, glitch m 67 [ms]      izle (Ctrl+C: dur)
  geri              yazilanlari geri al   kaydet dosya   dokumu dosyaya
  tara 13 03D0 03DF [adim] [bekle_ms]     her degeri yaz, RSSI/gurultu oku
  yardim            bu metin              cik            cikis"""


def hexes(args):
    return [int(a, 16) for a in args]


def run(bk, line, show=print):
    """One shell command. False: leave."""
    f = line.split()
    if not f or f[0].startswith("#"):
        return True
    c, a = f[0].lower(), f[1:]
    try:
        if c in ("cik", "q", "quit", "exit"):
            return False
        if c in ("yardim", "help", "?"):
            show(HELP)
        elif c == "r":
            reg = hexes(a[:1])[0]
            n = hexes(a[1:2])[0] if len(a) > 1 else 1
            vals = bk.read(reg, n)
            for i, v in enumerate([vals] if n == 1 else vals):
                show(f"{reg + i:02X}  {v:04X}  {bits(v)}  {name(reg + i)}")
        elif c in ("w", "w!"):
            reg, val = hexes(a[:2])
            v = bk.write(reg, val, force=c == "w!")
            show(f"{reg:02X}  {v:04X}  {bits(v)}  {name(reg)}")
        elif c == "d":
            show(fmt_dump(bk.dump()))
        elif c == "s":
            s = bk.status()
            show(f"RSSI {s['rssi']:.1f} dBm  gurultu {s['gurultu']}  glitch {s['glitch']}")
        elif c == "m":
            reg = hexes(a[:1])[0]
            ms = int(a[1]) if len(a) > 1 else 100
            try:
                while True:
                    for t, v in bk.monitor(reg, ms, 1.0):
                        show(f"{reg:02X}  {v:04X}  {bits(v)}")
            except KeyboardInterrupt:
                pass
        elif c == "geri":
            show(f"{bk.restore()} register geri yuklendi")
        elif c == "kaydet":
            with open(a[0], "w") as fh:
                fh.write(fmt_dump(bk.dump()) + "\n")
            show(f"-> {a[0]}")
        elif c == "tara":
            reg, start, stop = hexes(a[:3])
            step = int(a[3], 16) if len(a) > 3 else 1
            wait = int(a[4]) if len(a) > 4 else 100
            show(f"{name(reg) or hex(reg)}: deger  RSSI  gurultu  glitch")
            for v, s in bk.sweep(reg, start, stop, step, wait):
                show(f"  {v:04X}  {s['rssi']:7.1f}  {s['gurultu']:3d}  {s['glitch']:3d}")
        else:
            show("bilinmeyen komut (yardim)")
    except (ValueError, IndexError):
        show("eksik ya da hatali arguman (yardim)")
    except BKError as e:
        show(f"hata: {e}")
    return True


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["fark"]:
        a, b = (parse_dump(open(p).read()) for p in argv[1:3])
        print("\n".join(diff(a, b)) or "fark yok")
        return
    port = None
    if argv[:1] == ["-p"]:
        port, argv = argv[1], argv[2:]
    bk = BK.open(port)
    try:
        if argv[:1] == ["betik"]:
            for line in open(argv[1]):
                print(">", line.rstrip())
                if not run(bk, line):
                    break
            return
        try:
            import readline  # noqa: F401
        except ImportError:
            pass
        print("BK Lab kabugu. 'yardim' komutlari listeler, 'cik' cikar.")
        while True:
            try:
                line = input("bk> ")
            except (EOFError, KeyboardInterrupt):
                break
            if not run(bk, line):
                break
    finally:
        bk.close()


if __name__ == "__main__":
    main()
