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
qsodefteri - the computer side of the QSO Defteri overlay app.

  qsodefteri.py saat                      set the radio's UTC clock from this computer
  qsodefteri.py al defter.adi [--cagri TA2XX] [--kare KN50TR] [--temizle]
                                          set the clock, fetch the log, write ADIF
                                          (and defter.csv), optionally empty the radio
  qsodefteri.py adif defter.csv defter.adi
                                          a saved CSV to ADIF

ADIF 3.1.4: CALL, QSO_DATE, TIME_ON, FREQ, BAND, MODE (+ SUBMODE USB),
RST_SENT, RST_RCVD, and STATION_CALLSIGN / MY_GRIDSQUARE when given: what
Log4OM, N1MM, QRZ.com or TQSL (LoTW) import. A contact logged while the radio
had no clock has no time: it is left out, unless --zamansiz gives one.
Needs pyserial and uvterm.py (../uvterm) for "saat" and "al".
"""

import argparse
import datetime
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "uvterm"))

VERSION = "1.0"
# ADIF band limits, MHz
BANDS = [("160m", 1.8, 2.0), ("80m", 3.5, 4.0), ("60m", 5.06, 5.45), ("40m", 7.0, 7.3),
         ("30m", 10.1, 10.15), ("20m", 14.0, 14.35), ("17m", 18.068, 18.168), ("15m", 21.0, 21.45),
         ("12m", 24.89, 24.99), ("10m", 28.0, 29.7), ("6m", 50.0, 54.0), ("4m", 70.0, 71.0),
         ("2m", 144.0, 148.0), ("1.25m", 222.0, 225.0), ("70cm", 420.0, 450.0), ("33cm", 902.0, 928.0),
         ("23cm", 1240.0, 1300.0)]


def band(mhz):
    return next((b for b, lo, hi in BANDS if lo <= mhz <= hi), None)


def parse_csv(text):
    """[dict] from the radio's CSV (call,khz,unix,rst_s,rst_r,mode)."""
    out = []
    for line in text.splitlines():
        f = line.strip().split(",")
        if len(f) != 6 or f[0] == "call" or not f[1].isdigit():
            continue
        out.append({"call": f[0], "khz": int(f[1]), "unix": int(f[2]), "rst_s": f[3], "rst_r": f[4],
                    "mode": f[5]})
    return out


def field(name, value):
    value = str(value)
    return f"<{name}:{len(value.encode())}>{value} "


def adif(qsos, station=None, grid=None, untimed=None, now=None):
    """(ADIF text, how many were left out for want of a time)."""
    now = now or datetime.datetime.now(datetime.timezone.utc)
    head = ("QSO Defteri (UV-K1 / UV-K5 V3, F4HWN Labs) disa aktarimi\n"
            + field("ADIF_VER", "3.1.4") + field("PROGRAMID", "QSO Defteri") + field("PROGRAMVERSION", VERSION)
            + field("CREATED_TIMESTAMP", now.strftime("%Y%m%d %H%M%S")) + "<EOH>\n")
    recs, skipped = [], 0
    for q in qsos:
        t = q["unix"] or untimed
        if not t:
            skipped += 1
            continue
        dt = datetime.datetime.fromtimestamp(t, datetime.timezone.utc)
        mhz = q["khz"] / 1000
        r = field("CALL", q["call"]) + field("QSO_DATE", dt.strftime("%Y%m%d")) + field("TIME_ON", dt.strftime("%H%M%S"))
        r += field("FREQ", f"{mhz:.6f}".rstrip("0").rstrip("."))
        b = band(mhz)
        if b:
            r += field("BAND", b)
        if q["mode"] == "SSB":
            r += field("MODE", "SSB") + field("SUBMODE", "USB")
        else:
            r += field("MODE", q["mode"])
        r += field("RST_SENT", q["rst_s"]) + field("RST_RCVD", q["rst_r"])
        if station:
            r += field("STATION_CALLSIGN", station.upper())
        if grid:
            r += field("MY_GRIDSQUARE", grid.upper()[:4] + grid.lower()[4:])
        recs.append(r + "<EOR>")
    return head + "\n".join(recs) + ("\n" if recs else ""), skipped


def parse_adif(text):
    """[{FIELD: value}] - enough to check what adif() writes."""
    out, cur = [], {}
    body = text.split("<EOH>", 1)[-1]
    i = 0
    while True:
        i = body.find("<", i)
        if i < 0:
            break
        j = body.index(">", i)
        tag = body[i + 1:j]
        if tag.upper() == "EOR":
            out.append(cur)
            cur = {}
            i = j + 1
            continue
        name, n = tag.split(":")[:2]
        cur[name.upper()] = body[j + 1:j + 1 + int(n)]
        i = j + 1 + int(n)
    return out


class Radio:
    def __init__(self, ser):
        self.ser = ser

    def command(self, cmd, until, timeout=3.0):
        self.ser.reset_input_buffer()
        self.ser.write(cmd.encode() + b"\r\n")
        self.ser.flush()
        buf, end = b"", time.time() + timeout
        while time.time() < end:
            buf += self.ser.read(512)
            if until.encode() in buf:
                return buf.decode("ascii", "replace")
        raise RuntimeError(f"telsiz '{cmd}' komutuna cevap vermedi: QSO Defteri acik mi?")

    def set_clock(self, unix=None):
        return self.command(f"/saat {int(unix or time.time())}", "# tamam")

    def fetch(self):
        return self.command("/liste", "# tamam")

    def clear(self):
        return self.command("/temizle", "# tamam")


def open_radio(port):
    import uvterm
    uvterm.need_pyserial()
    ser = uvterm.open_port(uvterm.find_port(port))
    time.sleep(0.3)
    return ser, Radio(ser)


def cmd_saat(args):
    ser, radio = open_radio(args.port)
    try:
        radio.set_clock()
        print("Telsizin saati ayarlandi (UTC):", datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
    finally:
        ser.close()


def write(qsos, path, args):
    untimed = None
    if args.zamansiz:
        untimed = int(datetime.datetime.strptime(args.zamansiz, "%Y-%m-%d %H:%M").replace(
            tzinfo=datetime.timezone.utc).timestamp())
    text, skipped = adif(qsos, args.cagri, args.kare, untimed)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"{len(qsos) - skipped} QSO -> {path}")
    if skipped:
        print(f"Uyari: {skipped} QSO saatsiz kaydedilmis, disarida birakildi "
              "(--zamansiz 'YYYY-AA-GG ss:dd' ile ekleyin).")


def cmd_al(args):
    ser, radio = open_radio(args.port)
    try:
        radio.set_clock()
        text = radio.fetch()
        qsos = parse_csv(text)
        csv_path = os.path.splitext(args.dosya)[0] + ".csv"
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("call,khz,unix,rst_s,rst_r,mode\n")
            f.write("".join(f"{q['call']},{q['khz']},{q['unix']},{q['rst_s']},{q['rst_r']},{q['mode']}\n" for q in qsos))
        write(qsos, args.dosya, args)
        if args.temizle and qsos:
            if args.evet or input(f"Telsizdeki {len(qsos)} QSO silinsin mi? [e/H] ").strip().lower() in ("e", "evet"):
                radio.clear()
                print("Telsizdeki defter bosaltildi.")
    except RuntimeError as e:
        print("Hata:", e, file=sys.stderr)
        sys.exit(1)
    finally:
        ser.close()


def cmd_adif(args):
    write(parse_csv(open(args.csv, encoding="utf-8").read()), args.dosya, args)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="qsodefteri.py", description="QSO Defteri icin PC araci.")
    sub = ap.add_subparsers(dest="cmd", metavar="komut", required=True)
    s = sub.add_parser("saat", help="telsizin UTC saatini bilgisayardan ayarla")
    s.add_argument("-p", "--port")
    for name, hlp in (("al", "saati ayarla, defteri al, ADIF yaz"), ("adif", "kaydedilmis CSV'den ADIF")):
        p = sub.add_parser(name, help=hlp)
        if name == "adif":
            p.add_argument("csv")
        p.add_argument("dosya", help="cikti .adi")
        p.add_argument("--cagri", help="kendi cagri isaretiniz (STATION_CALLSIGN)")
        p.add_argument("--kare", help="Maidenhead kareniz (MY_GRIDSQUARE), or. KN50TR")
        p.add_argument("--zamansiz", help="saatsiz QSO'lara verilecek zaman: 'YYYY-AA-GG ss:dd' (UTC)")
        if name == "al":
            p.add_argument("-p", "--port")
            p.add_argument("--temizle", action="store_true", help="aktardiktan sonra telsizdeki defteri bosalt")
            p.add_argument("-y", "--evet", action="store_true", help="silmeden once sorma")
    args = ap.parse_args(argv)
    {"saat": cmd_saat, "al": cmd_al, "adif": cmd_adif}[args.cmd](args)


if __name__ == "__main__":
    main()
