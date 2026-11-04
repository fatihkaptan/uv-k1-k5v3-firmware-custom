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
antenlab - the computer side of the Anten Lab overlay app.

  antenlab.py al yagi.csv            fetch the radio's pattern (and its
                                     reference) -> CSV, plus yagi.svg
  antenlab.py ciz a.csv b.csv -o karsilastirma.svg
                                     polar plot of one or more patterns, on
                                     one dB scale, with their numbers
  antenlab.py ozet a.csv             beam, level, front/back, -3 dB width

The CSV is the radio's: "derece,dBm,ref_dBm", 36 rows of 10 degrees, empty
where nothing was measured. Pure Python (the SVG is written by hand); "al"
needs pyserial and uvterm.py (../uvterm).
"""

import argparse
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "uvterm"))

NB = 36
COLORS = ["#c0392b", "#2471a3", "#1e8449", "#7d3c98", "#b9770e"]


def parse_csv(text):
    """{'cur': [dBm or None] x36, 'ref': [...]} from the radio's CSV."""
    cur, ref = [None] * NB, [None] * NB
    for line in text.splitlines():
        f = line.strip().split(",")
        if len(f) < 2 or not f[0].strip().isdigit():
            continue
        k = int(f[0]) // 10
        if 0 <= k < NB:
            cur[k] = float(f[1]) if f[1].strip() else None
            if len(f) > 2 and f[2].strip():
                ref[k] = float(f[2])
    return {"cur": cur, "ref": ref}


def stats(p):
    """The app's numbers: beam between the -3 dB points (else the strongest
    bin), its level, front/back, -3 dB width (degrees, None when unknown)."""
    vals = [(v, k) for k, v in enumerate(p) if v is not None]
    if not vals:
        return None
    top, k = max(vals, key=lambda x: (x[0], -x[1]))

    def half(way):
        thr = top - 3
        for n in range(1, NB // 2 + 1):
            a, b = p[(k + way * (n - 1)) % NB], p[(k + way * n) % NB]
            if a is None or b is None:
                return None
            if b < thr:
                return 10 * (n - 1) + 10 * (a - thr) / (a - b)
        return None
    lo, hi = half(-1), half(1)
    beam, width = 10.0 * k, None
    if lo is not None and hi is not None:
        width = lo + hi
        beam += (hi - lo) / 2
    beam %= 360
    back = p[(round(beam / 10) + NB // 2) % NB]
    return {"beam": beam, "level": top, "fb": None if back is None else top - back, "width": width}


def describe(name, s):
    if not s:
        return f"{name}: olcum yok"
    out = f"{name}: tepe {s['beam']:.0f} derece, {s['level']:.2f} dBm"
    out += f", on/arka {s['fb']:.1f} dB" if s["fb"] is not None else ""
    out += f", -3 dB hüzme {s['width']:.0f} derece" if s["width"] is not None else ""
    return out


def svg(patterns, title="Anten Lab", dyn=30.0, size=480):
    """patterns = [(name, [dBm or None] x36)] -> SVG text, one dB scale."""
    c, R = size / 2, size / 2 - 50
    top = max((v for _, p in patterns for v in p if v is not None), default=0.0)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size + 30 * len(patterns)}" '
           f'font-family="sans-serif" font-size="12">',
           f'<rect width="100%" height="100%" fill="white"/>',
           f'<text x="{c}" y="18" text-anchor="middle" font-size="15">{title}</text>']
    for db in (0, -10, -20, -30):
        r = R * (1 + db / dyn)
        if r > 0:
            out.append(f'<circle cx="{c}" cy="{c}" r="{r:.1f}" fill="none" stroke="#bbb"/>')
            out.append(f'<text x="{c + 3}" y="{c - r + 12:.1f}" fill="#888">{db} dB</text>')
    for deg in range(0, 360, 30):
        a = math.radians(deg)
        x, y = c + R * math.sin(a), c - R * math.cos(a)
        out.append(f'<line x1="{c}" y1="{c}" x2="{x:.1f}" y2="{y:.1f}" stroke="#eee"/>')
        tx, ty = c + (R + 16) * math.sin(a), c - (R + 16) * math.cos(a) + 4
        out.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle">{deg}</text>')
    for i, (name, p) in enumerate(patterns):
        col = COLORS[i % len(COLORS)]
        pts = []
        for k in range(NB + 1):
            v = p[k % NB]
            if v is None:
                if len(pts) > 1:
                    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2"/>')
                pts = []
                continue
            r = max(0.0, R * (1 + (v - top) / dyn))
            a = math.radians(10 * k)
            pts.append(f"{c + r * math.sin(a):.1f},{c - r * math.cos(a):.1f}")
        if len(pts) > 1:
            out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2"/>')
        y = size + 20 + 30 * i
        out.append(f'<rect x="20" y="{y - 10}" width="14" height="4" fill="{col}"/>')
        out.append(f'<text x="40" y="{y - 4}">{describe(name, stats(p))}</text>')
    out.append("</svg>")
    return "\n".join(out)


def fetch(ser, timeout=4.0):
    """Ask the radio ('?') and read its CSV."""
    ser.reset_input_buffer()
    ser.write(b"?\r\n")
    ser.flush()
    buf, end = b"", time.time() + timeout
    while time.time() < end:
        buf += ser.read(512)
        rows = [l for l in buf.decode("ascii", "replace").splitlines() if l[:1].isdigit()]
        if len(rows) >= NB and buf.endswith(b"\n"):
            break
    text = buf.decode("ascii", "replace")
    if "derece,dBm" not in text:
        raise RuntimeError("telsiz cevap vermedi: Anten Lab acik mi?")
    return text[text.index("derece,dBm"):]


def main(argv=None):
    ap = argparse.ArgumentParser(prog="antenlab.py", description="Anten Lab icin PC araci.")
    sub = ap.add_subparsers(dest="cmd", metavar="komut", required=True)
    a = sub.add_parser("al", help="telsizdeki olcumu CSV + SVG olarak al")
    a.add_argument("dosya", help="cikti .csv")
    a.add_argument("-p", "--port")
    c = sub.add_parser("ciz", help="CSV'lerden kutupsal diyagram (SVG)")
    c.add_argument("dosyalar", nargs="+")
    c.add_argument("-o", "--cikti", default="diyagram.svg")
    c.add_argument("--baslik", default="Anten Lab")
    o = sub.add_parser("ozet", help="CSV'nin sayilari")
    o.add_argument("dosyalar", nargs="+")
    args = ap.parse_args(argv)

    if args.cmd == "al":
        import uvterm
        uvterm.need_pyserial()
        ser = uvterm.open_port(uvterm.find_port(args.port))
        try:
            time.sleep(0.3)
            text = fetch(ser)
        except RuntimeError as e:
            uvterm.die(str(e))
        finally:
            ser.close()
        with open(args.dosya, "w", encoding="utf-8") as f:
            f.write(text.replace("\r", ""))
        d = parse_csv(text)
        pats = [("olcum", d["cur"])] + ([("referans", d["ref"])] if any(v is not None for v in d["ref"]) else [])
        out = os.path.splitext(args.dosya)[0] + ".svg"
        with open(out, "w", encoding="utf-8") as f:
            f.write(svg(pats))
        for name, p in pats:
            print(describe(name, stats(p)))
        print(f"-> {args.dosya}, {out}")
    elif args.cmd == "ciz":
        pats = []
        for path in args.dosyalar:
            d = parse_csv(open(path, encoding="utf-8").read())
            pats.append((os.path.splitext(os.path.basename(path))[0], d["cur"]))
        with open(args.cikti, "w", encoding="utf-8") as f:
            f.write(svg(pats, args.baslik))
        print(f"-> {args.cikti}")
    else:
        for path in args.dosyalar:
            d = parse_csv(open(path, encoding="utf-8").read())
            print(describe(path, stats(d["cur"])))


if __name__ == "__main__":
    main()
