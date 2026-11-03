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
uvterm - the computer side of the "USB Term" overlay app (F4HWN Labs).

Talks to a UV-K1 / UV-K5 V3 over its USB-C serial port:

  uvterm.py                     chat with the radio (the USB Term app is open)
  uvterm.py send "text"         send one line and leave (scripts, cron...)
  uvterm.py ports               list the serial ports, the radio marked
  uvterm.py apps                list the overlay apps installed on the radio
  uvterm.py install X.app       install an overlay app (radio on its main screen)

Needs Python 3.8+ and pyserial (pip install pyserial).

Chat protocol (see App/apps/usbterm/README.md): plain text lines, CR LF. The
radio answers commands with lines that start with "# ". uvterm sends
"/echo off" at each connection: it shows what you type itself.

The install / apps commands use the resident firmware's serial protocol
(0x0514 hello, 0x0730 slot info, 0x0732 erase, 0x0734 write, 0x0736 validate;
App/app/uart.c), the same one UV Studio uses. They only touch the Apps region
of the external flash (never the firmware or the calibration).
"""

import argparse
import os
import random
import struct
import sys
import threading
import time
import zlib

try:
    import serial
    from serial.tools import list_ports
except ImportError:  # pragma: no cover - message for the user
    serial = None
    list_ports = None

USB_VID = 0x36B7          # App/usb/usbd_cdc_if.c
USB_PID = 0xFFFF
BAUD = 115200             # ignored by the USB CDC port, required by the API

CHUNK = 32                # bytes per write in chat: the radio polls every 10 ms
CHUNK_GAP = 0.05          # ... into a 256-byte ring, and may be busy beeping

# ---------------------------------------------------------------------------
# Terminal output
# ---------------------------------------------------------------------------

if os.name == "nt":
    os.system("")         # enables ANSI escape sequences on Windows 10+

try:
    import readline       # noqa: F401  (line editing + prompt redraw on Unix)
except ImportError:       # Windows: works without, the prompt is just not redrawn
    readline = None

USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def color(text, code):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def die(msg, code=1):
    print(color("Hata: ", "31;1") + msg, file=sys.stderr)
    sys.exit(code)


def need_pyserial():
    if serial is None:
        die("pyserial kurulu değil. Kurmak için:  pip install pyserial")


# ---------------------------------------------------------------------------
# Serial port
# ---------------------------------------------------------------------------

def radio_ports():
    return [p for p in list_ports.comports() if p.vid == USB_VID and p.pid == USB_PID]


def find_port(explicit):
    if explicit:
        return explicit
    ports = radio_ports()
    if not ports:
        die("Telsiz bulunamadı (USB VID:PID 36B7:FFFF). USB-C kablosunu ve telsizin açık "
            "olduğunu kontrol edin, ya da portu elle verin: -p COM5  /  -p /dev/ttyACM0\n"
            "Portları görmek için:  uvterm.py ports")
    if len(ports) > 1:
        print(color(f"Birden çok telsiz bulundu, {ports[0].device} kullanılıyor "
                    "(-p ile seçebilirsiniz).", "33"))
    return ports[0].device


def open_port(name):
    need_pyserial()
    try:
        ser = serial.Serial(name, BAUD, timeout=0.05, write_timeout=2)
    except serial.SerialException as e:
        die(f"{name} açılamadı: {e}\n"
            "Port başka bir programda (UV Studio, CHIRP, başka bir terminal) açık olabilir. "
            "Linux'ta 'dialout' grubunda olmanız gerekebilir.")
    try:
        ser.dtr = True    # the app sees the host through DTR (pyserial sets it on open too)
    except (OSError, serial.SerialException):
        pass              # a pseudo-terminal (tests) has no modem lines
    return ser


def cmd_ports(args):
    need_pyserial()
    ports = list(list_ports.comports())
    if not ports:
        print("Hiç seri port yok.")
        return
    for p in ports:
        mark = color("  <- telsiz (UV-K1 / UV-K5 V3)", "32") \
            if (p.vid, p.pid) == (USB_VID, USB_PID) else ""
        vidpid = f"{p.vid:04X}:{p.pid:04X}" if p.vid is not None else "----:----"
        print(f"{p.device:20s} {vidpid}  {p.description}{mark}")


# ---------------------------------------------------------------------------
# Chat with the USB Term app
# ---------------------------------------------------------------------------

def paced_write(ser, data, chunk=CHUNK, gap=CHUNK_GAP):
    """Write in small chunks, so the radio's 256-byte receive ring never laps."""
    for i in range(0, len(data), chunk):
        ser.write(data[i:i + chunk])
        ser.flush()
        if i + chunk < len(data):
            time.sleep(gap)


def encode_line(text):
    return text.encode("utf-8", "replace") + b"\r\n"


def classify(line):
    """What a line from the radio is: ('banner'|'ack'|'info'|'echo'|'msg', text)."""
    if line.startswith("# USB Term") and "ready" in line:
        return "banner", line
    if line == "# echo off":
        return "ack", line
    if line.startswith("# "):
        return "info", line[2:]
    if line == "/echo off":           # the radio's echo of our handshake
        return "echo", line
    return "msg", line


class Chat:
    PROMPT = "PC> "

    def __init__(self, ser, log=None, quiet=False):
        self.ser = ser
        self.log = log
        self.quiet = quiet
        self.lock = threading.Lock()
        self.ready = threading.Event()
        self.stop = threading.Event()
        self.handshake_sent = 0.0
        self.thread = None

    # -- output, redrawing the prompt line under the message -----------------
    def show(self, text):
        with self.lock:
            buf = readline.get_line_buffer() if readline and sys.stdin.isatty() else ""
            if sys.stdin.isatty():
                sys.stdout.write("\r\033[K" + text + "\n" + self.PROMPT + buf)
            else:
                sys.stdout.write(text + "\n")
            sys.stdout.flush()

    def write_log(self, who, text):
        if self.log:
            self.log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {who} {text}\n")
            self.log.flush()

    # -- radio -> computer -----------------------------------------------------
    def handshake(self):
        self.handshake_sent = time.time()
        paced_write(self.ser, encode_line("/echo off"))

    def on_line(self, line):
        kind, text = classify(line)
        if kind == "banner":
            self.show(color(f"[{text[2:]}]", "36"))
            self.handshake()              # a new session: echo is back on
        elif kind == "ack":
            if not self.ready.is_set():
                self.ready.set()
                self.show(color("[telsiz hazır - yazıp Enter'a basın, çıkmak için /quit]", "36"))
        elif kind == "info":
            self.show(color("  · " + text, "2"))
            self.write_log("#", text)
        elif kind == "msg":
            stamp = time.strftime("%H:%M:%S")
            self.show(color(f"[{stamp}] ", "2") + color("TELSİZ> ", "32;1") + text)
            self.write_log("TELSIZ>", text)

    def reader(self):
        buf = bytearray()
        while not self.stop.is_set():
            try:
                data = self.ser.read(256)
            except Exception as e:        # unplugged, or closed under us at exit
                if not self.stop.is_set():
                    self.show(color(f"[bağlantı koptu: {e}]", "31"))
                    self.stop.set()
                break
            if not data:
                continue
            buf += data
            while True:
                i = buf.find(b"\n")
                if i < 0:
                    break
                raw = bytes(buf[:i]).rstrip(b"\r")
                del buf[:i + 1]
                self.on_line(raw.decode("utf-8", "replace"))

    # -- computer -> radio -----------------------------------------------------
    def send(self, text):
        paced_write(self.ser, encode_line(text))
        self.write_log("PC>", text)

    def send_file(self, path):
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except OSError as e:
            self.show(color(f"[dosya okunamadı: {e}]", "31"))
            return
        for line in lines:
            self.send(line)
            time.sleep(0.1)   # the radio beeps on each line
        self.show(color(f"[{len(lines)} satır gönderildi]", "36"))

    def help(self):
        self.show(color(
            "PC komutları:   /quit  çıkış   |  /send <dosya>  metin dosyası gönder\n"
            "Telsiz komutları: /info  /ping  /beep  /clear  /echo on|off\n"
            "Diğer her satır telsizin ekranına mesaj olarak gider.", "36"))

    def start(self):
        self.thread = threading.Thread(target=self.reader, daemon=True)
        self.thread.start()

    def close(self):
        """Stop the reader, then the port can be closed."""
        self.stop.set()
        if self.thread:
            self.thread.join(1.0)

    def run(self):
        self.start()
        print(color(f"uvterm - {self.ser.port} açık. Telsizde USB Term uygulamasını açın "
                    "(F+7 -> USB Term). Yardım: /help, çıkış: /quit", "36"))
        time.sleep(0.2)
        self.handshake()
        warned = False
        while not self.stop.is_set():
            if not warned and not self.ready.is_set() and time.time() - self.handshake_sent > 2:
                warned = True
                self.show(color("[telsizden yanıt yok: USB Term uygulaması açık mı? "
                                "(F+7 -> USB Term). Açıldığında bağlantı kendiliğinden kurulur.]",
                                "33"))
            try:
                text = input(self.PROMPT) if sys.stdin.isatty() else sys.stdin.readline()
            except (EOFError, KeyboardInterrupt):
                break
            if not sys.stdin.isatty():
                if text == "":
                    time.sleep(0.5)       # stdin closed: let the last replies arrive
                    break
                text = text.rstrip("\r\n")
            if self.stop.is_set():
                break
            cmd = text.strip()
            if cmd.lower() in ("/quit", "/exit", "/q"):
                break
            if cmd.lower() == "/help":
                self.help()
                self.send("/help")
                continue
            if cmd.lower().startswith("/send "):
                self.send_file(cmd[6:].strip())
                continue
            if not cmd:
                continue
            try:
                self.send(text)
            except (serial.SerialException, OSError) as e:
                self.show(color(f"[gönderilemedi: {e}]", "31"))
                break
        self.stop.set()


def cmd_chat(args):
    ser = open_port(find_port(args.port))
    log = open(args.log, "a", encoding="utf-8") if args.log else None
    chat = Chat(ser, log)
    try:
        chat.run()
    finally:
        chat.close()
        ser.close()
        if log:
            log.close()


def cmd_send(args):
    ser = open_port(find_port(args.port))
    try:
        time.sleep(0.2)                  # the radio notices the new connection
        for text in args.text:
            paced_write(ser, encode_line(text))
            time.sleep(0.1)
        time.sleep(0.1)
    finally:
        ser.close()


# ---------------------------------------------------------------------------
# Resident serial protocol (App/app/uart.c): apps list / install
# ---------------------------------------------------------------------------

OBFUSCATION = bytes([0x16, 0x6C, 0x14, 0xE6, 0x2E, 0x91, 0x0D, 0x40,
                     0x21, 0x35, 0xD5, 0x40, 0x13, 0x03, 0xE9, 0x80])

# app_overlay.h
APP_MAGIC = 0x31504146            # "FAP1"
APP_HDR_VERSION = 1
APP_FLAG_COMMITTED = 0x0001
APP_SLOT_COUNT = 48
APP_ASSET_OFFSET = 0x100
APP_ASSET_MAX = 0xF00
APP_CODE_OFFSET = 0x1000
APP_OVERLAY_MAX = 0x1000
APP_HEADER = struct.Struct("<4sHBBIIHH16s16sIIHH")    # app_header_t, 64 bytes
APP_STATUS = ["OK", "SLOT (geçersiz slot)", "MAGIC (boş / geçersiz)",
              "ABI (firmware API seviyesi düşük)", "NOT_COMMITTED", "SIZE", "CRC",
              "VMA (başka firmware sürümü için derlenmiş)",
              "AUTH (oturum zaman damgası tutmadı)",
              "CAP (firmware'de gereken özellik yok)", "CHAIN_ABORTED"]
CAPS = {0x01: "fm", 0x04: "beam", 0x08: "sysinfo", 0x10: "beam2",
        0x20: "cfgproxy", 0x40: "serial"}
WRITE_CHUNK = 128


def crc16_xmodem(data):
    crc = 0
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) if crc & 0x8000 else (crc << 1)
            crc &= 0xFFFF
    return crc


def obfuscate(data):
    return bytes(b ^ OBFUSCATION[i % 16] for i, b in enumerate(data))


def make_packet(msg_id, data=b""):
    """AB CD | len | obfuscated(ID, Size, data [, pad] + CRC16) | DC BA"""
    msg = struct.pack("<HH", msg_id, len(data)) + data
    if len(msg) % 2:
        msg += b"\x00"
    body = msg + struct.pack("<H", crc16_xmodem(msg))
    return b"\xAB\xCD" + struct.pack("<H", len(msg)) + obfuscate(body) + b"\xDC\xBA"


def status_name(code):
    return APP_STATUS[code] if code < len(APP_STATUS) else f"hata {code}"


class ProtocolError(Exception):
    pass


class Link:
    """Request / reply over the resident command parser."""

    def __init__(self, ser):
        self.ser = ser
        self.buf = bytearray()
        self.timestamp = random.randint(1, 0xFFFFFFFF)
        self.version = None

    def fetch(self):
        """The next complete reply in buf as (id, payload), or None."""
        while True:
            i = self.buf.find(b"\xAB\xCD")
            if i < 0:
                del self.buf[:-1 if self.buf.endswith(b"\xAB") else len(self.buf)]
                return None
            del self.buf[:i]
            if len(self.buf) < 8:
                return None
            size = self.buf[2] | self.buf[3] << 8
            total = 4 + size + 2 + 2
            if size < 4 or size > 512:
                del self.buf[:2]
                continue
            if len(self.buf) < total:
                return None
            if self.buf[total - 2:total] != b"\xDC\xBA":
                del self.buf[:2]
                continue
            body = obfuscate(bytes(self.buf[4:4 + size]))
            del self.buf[:total]
            msg_id, msg_size = struct.unpack_from("<HH", body)
            return msg_id, body[4:4 + msg_size]

    def request(self, msg_id, data, reply_id, timeout=2.0):
        self.ser.write(make_packet(msg_id, data))
        self.ser.flush()
        deadline = time.time() + timeout
        while time.time() < deadline:
            chunk = self.ser.read(256)
            if chunk:
                self.buf += chunk
            while True:
                reply = self.fetch()
                if reply is None:
                    break
                if reply[0] == reply_id:
                    return reply[1]
        raise ProtocolError(f"telsiz 0x{msg_id:04X} komutuna yanıt vermedi")

    def hello(self):
        payload = self.request(0x0514, struct.pack("<I", self.timestamp), 0x0515)
        self.version = payload[:16].split(b"\x00")[0].decode("ascii", "replace")
        return self.version

    def slot_info(self, slot):
        p = self.request(0x0730, bytes([slot, 0]), 0x0731)
        if len(p) < 2 + APP_HEADER.size or p[0] != slot:
            raise ProtocolError("slot bilgisi beklenmedik biçimde")
        return p[1], parse_header(p[2:2 + APP_HEADER.size])

    def slot_erase(self, slot):
        p = self.request(0x0732, bytes([slot, 0]) + struct.pack("<I", self.timestamp),
                         0x0733, timeout=6.0)
        return p[1]

    def slot_write(self, slot, offset, data):
        head = bytes([slot, 0]) + struct.pack("<IHI", offset, len(data), self.timestamp)
        p = self.request(0x0734, head + data, 0x0735)
        return p[1]

    def slot_validate(self, slot):
        p = self.request(0x0736, bytes([slot, 0]), 0x0737)
        return p[1]


def parse_header(raw):
    (magic, hdr_ver, abi, api_min, code_size, code_crc, entry, flags, name, ver,
     vma, caps, asset_size, asset_crc) = APP_HEADER.unpack(raw[:APP_HEADER.size])
    return {
        "magic": struct.unpack("<I", magic)[0], "hdr_version": hdr_ver, "abi": abi,
        "api_min": api_min, "code_size": code_size, "code_crc": code_crc, "entry": entry,
        "flags": flags, "name": name.split(b"\x00")[0].decode("ascii", "replace"),
        "version": ver.split(b"\x00")[0].decode("ascii", "replace"), "vma": vma,
        "caps": caps, "asset_size": asset_size, "asset_crc": asset_crc,
    }


def caps_text(caps):
    names = [n for bit, n in CAPS.items() if caps & bit]
    return ",".join(names) if names else "-"


def load_app(path):
    """Read and check a .app blob: (header bytes, header dict, code, assets)."""
    try:
        blob = open(path, "rb").read()
    except OSError as e:
        die(f"{path} okunamadı: {e}")
    if len(blob) < APP_HEADER.size:
        die(f"{path}: .app dosyası değil (çok kısa)")
    h = parse_header(blob)
    if h["magic"] != APP_MAGIC or h["hdr_version"] != APP_HDR_VERSION:
        die(f"{path}: .app dosyası değil (FAP1 başlığı yok)")
    code = blob[64:64 + h["code_size"]]
    assets = blob[64 + h["code_size"]:]
    if not 0 < h["code_size"] <= APP_OVERLAY_MAX or len(code) != h["code_size"]:
        die(f"{path}: kod boyutu tutarsız")
    if len(assets) != h["asset_size"] or len(assets) > APP_ASSET_MAX:
        die(f"{path}: varlık (asset) boyutu tutarsız")
    if zlib.crc32(code) & 0xFFFFFFFF != h["code_crc"]:
        die(f"{path}: kod CRC'si tutmuyor (dosya bozuk)")
    if assets and (zlib.crc32(assets) & 0xFFFF) != h["asset_crc"]:
        die(f"{path}: varlık CRC'si tutmuyor (dosya bozuk)")
    if not h["flags"] & APP_FLAG_COMMITTED:
        die(f"{path}: başlıkta COMMITTED bayrağı yok")
    return blob[:64], h, code, assets


def connect(args):
    ser = open_port(find_port(args.port))
    link = Link(ser)
    try:
        version = link.hello()
    except ProtocolError:
        ser.close()
        die("Telsiz komut protokolüne yanıt vermedi. Telsiz ana ekranda (VFO) ya da "
            "Apps menüsünde olmalı; açık bir uygulama varsa EXIT ile kapatın. "
            "Port başka bir programda açık olmamalı.")
    print(f"Telsiz: {color(version, '1')}  ({ser.port})")
    return ser, link


def read_slots(link, progress=True):
    slots = []
    for s in range(APP_SLOT_COUNT):
        if progress:
            print(f"\rSlotlar okunuyor... {s + 1}/{APP_SLOT_COUNT}", end="", flush=True)
        status, h = link.slot_info(s)
        slots.append(h if h["magic"] == APP_MAGIC else None)
    if progress:
        print("\r" + " " * 40 + "\r", end="")
    return slots


def cmd_apps(args):
    ser, link = connect(args)
    try:
        slots = read_slots(link)
        used = 0
        print(f"{'Slot':>4}  {'Ad':16s} {'Sürüm':8s} {'API':>3}  {'Kod':>5}  {'Varlık':>6}  Gerekenler")
        for s, h in enumerate(slots):
            if not h:
                continue
            used += 1
            print(f"{s:>4}  {h['name']:16s} {h['version']:8s} {h['api_min']:>3}  "
                  f"{h['code_size']:>5}  {h['asset_size']:>6}  {caps_text(h['caps'])}")
        print(f"{used} uygulama yüklü, {APP_SLOT_COUNT - used} slot boş.")
    finally:
        ser.close()


def choose_slot(slots, name, wanted, yes):
    if wanted is not None:
        if not 0 <= wanted < APP_SLOT_COUNT:
            die(f"slot 0-{APP_SLOT_COUNT - 1} arasında olmalı")
        cur = slots[wanted]
        if cur and cur["name"] != name and not yes:
            ans = input(f"Slot {wanted} dolu ('{cur['name']}' {cur['version']}). "
                        "Üzerine yazılsın mı? [e/H] ").strip().lower()
            if ans not in ("e", "evet", "y", "yes"):
                die("İptal edildi.", 0)
        return wanted
    for s, h in enumerate(slots):           # an update keeps the app's slot (and settings)
        if h and h["name"] == name:
            return s
    for s, h in enumerate(slots):
        if not h:
            return s
    die("Boş slot yok: önce bir uygulamayı --slot ile değiştirin.")


def install(link, slot, header, code, assets, progress=lambda done, total: None):
    """Erase the slot, write assets, code and finally the header, validate."""
    st = link.slot_erase(slot)
    if st:
        raise ProtocolError(f"silme başarısız: {status_name(st)}")
    jobs = [(APP_ASSET_OFFSET, assets), (APP_CODE_OFFSET, code), (0, header)]
    total = sum(len(d) for _, d in jobs)
    done = 0
    for base, data in jobs:                 # the header last: a cut install stays invalid
        for i in range(0, len(data), WRITE_CHUNK):
            part = data[i:i + WRITE_CHUNK]
            st = link.slot_write(slot, base + i, part)
            if st:
                raise ProtocolError(f"yazma başarısız (ofset 0x{base + i:04X}): {status_name(st)}")
            done += len(part)
            progress(done, total)
    return link.slot_validate(slot)


def cmd_install(args):
    header, h, code, assets = load_app(args.file)
    print(f"Uygulama: {color(h['name'], '1')} {h['version']}  (kod {h['code_size']} B, "
          f"varlık {h['asset_size']} B, API>={h['api_min']}, gerekenler: {caps_text(h['caps'])})")
    ser, link = connect(args)
    try:
        slots = read_slots(link)
        slot = choose_slot(slots, h["name"], args.slot, args.yes)
        cur = slots[slot]
        what = f"güncelleniyor ({cur['version']} -> {h['version']})" if cur and cur["name"] == h["name"] \
            else ("üzerine yazılıyor" if cur else "boş slota yükleniyor")
        print(f"Slot {slot}: {what}")

        def bar(done, total):
            n = 30 * done // total
            print(f"\r  [{'#' * n}{'.' * (30 - n)}] {100 * done // total:3d}%", end="", flush=True)

        st = install(link, slot, header, code, assets, bar)
        print()
        if st == 0:
            print(color(f"Tamam: '{h['name']}' slot {slot}'e yüklendi. Telsizde F+7 ile Apps "
                        "menüsünü açıp başlatabilirsiniz.", "32;1"))
        else:
            print(color(f"Yüklendi ama firmware uygulamayı reddediyor: {status_name(st)}.", "33;1"))
            print("Uygulamayı kurulu firmware ile aynı sürümden derleyin / indirin "
                  "(Labs firmware gerekir).")
            sys.exit(2)
    except ProtocolError as e:
        print()
        die(f"{e}. Slot yarım kalmış olabilir; komutu tekrar çalıştırın.")
    finally:
        ser.close()


# ---------------------------------------------------------------------------

def main(argv=None):
    port_help = "seri port (varsayılan: telsizi otomatik bul)"
    log_help = "sohbeti bu dosyaya da yaz"
    # -p / --log are accepted before and after the command: the subcommands'
    # copies default to SUPPRESS so they never reset a value given before.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-p", "--port", default=argparse.SUPPRESS, help=port_help)

    ap = argparse.ArgumentParser(
        prog="uvterm.py",
        description="UV-K1 / UV-K5 V3 (F4HWN Labs) USB Term uygulaması için PC terminali.")
    ap.add_argument("-p", "--port", help=port_help)
    ap.add_argument("--log", help=log_help)
    sub = ap.add_subparsers(dest="cmd", metavar="komut")
    sub.add_parser("chat", parents=[common], help="telsizle sohbet (varsayılan)") \
        .add_argument("--log", default=argparse.SUPPRESS, help=log_help)
    p = sub.add_parser("send", parents=[common], help="tek satır (veya birkaç satır) gönder ve çık")
    p.add_argument("text", nargs="+", help="gönderilecek satır(lar)")
    sub.add_parser("ports", help="seri portları listele")
    sub.add_parser("apps", parents=[common], help="telsizde yüklü uygulamaları listele")
    p = sub.add_parser("install", parents=[common], help=".app dosyasını telsize yükle")
    p.add_argument("file", help="yüklenecek .app dosyası (ör. build/Apps/USBTerm.app)")
    p.add_argument("--slot", type=int, help="hedef slot (0-47); varsayılan: aynı adlı "
                   "uygulamanın slotu, yoksa ilk boş slot")
    p.add_argument("-y", "--yes", action="store_true", help="dolu slotun üzerine sormadan yaz")
    args = ap.parse_args(argv)

    if args.cmd in (None, "chat"):
        cmd_chat(args)
    elif args.cmd == "send":
        cmd_send(args)
    elif args.cmd == "ports":
        cmd_ports(args)
    elif args.cmd == "apps":
        cmd_apps(args)
    elif args.cmd == "install":
        cmd_install(args)


if __name__ == "__main__":
    main()
