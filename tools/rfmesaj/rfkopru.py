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
rfkopru - the computer side of the RF Mesaj overlay app: a radio on USB-C
becomes a gateway between the radio messages and the outside world.

  rfkopru.py                         chat: type, the radio sends it over the air
  rfkopru.py --anahtar SIFRE         also set the group key on the radio
  rfkopru.py telegram --token T --sohbet ID
                                     radio messages <-> a Telegram chat
  rfkopru.py komut [--betik X]       "!komut" messages from the air get an
                                     automatic answer over the air (!saat,
                                     !ping, !hava, or your own script)

Needs Python 3.8+ and pyserial; uses uvterm.py (../uvterm) for the port.
Lines from the radio: "TA2AAA> text" (tagged with our key), "TA2AAA* text"
(encrypted, decrypted), "TA2AAA? text" (another key or none), "# ..."
(status: "# + aldi: TA2BBB", "# x iletilemedi", ...).
"""

import argparse
import json
import os
import re
import subprocess
import sys
import threading
import time
import unicodedata
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "uvterm"))
import uvterm  # noqa: E402

TEXT_MAX = 48                       # bytes of text in one radio packet
TR = str.maketrans("çÇğĞıİöÖşŞüÜâÂîÎûÛ", "cCgGiIoOsSuUaAiIuU")
MSG = re.compile(r"^([A-Z0-9/]{1,7})([>*?]) (.*)$")


def ascii_tr(text):
    """Turkish letters to their ASCII base, other accents dropped, the rest '?'."""
    text = unicodedata.normalize("NFKD", text.translate(TR))
    out = []
    for ch in text:
        if unicodedata.combining(ch):
            continue
        out.append(ch if " " <= ch <= "~" else "?")
    return "".join(out)


def chunks(text, n=TEXT_MAX):
    """Radio-sized pieces, cut at spaces when possible."""
    text = " ".join(ascii_tr(text).split())
    out = []
    while text:
        if len(text) <= n:
            out.append(text)
            break
        cut = text.rfind(" ", 0, n + 1)
        if cut <= 0:
            cut = n
        out.append(text[:cut].rstrip())
        text = text[cut:].lstrip()
    return out


def parse(line):
    """('msg', call, mark, text) for a radio message, ('status', text) or None."""
    m = MSG.match(line)
    if m:
        return ("msg",) + m.groups()
    if line.startswith("# "):
        return ("status", line[2:])
    return None


class Radio:
    """The serial link to RF Mesaj: lines in (callback), lines out (paced)."""

    def __init__(self, ser, on_line, key=None):
        self.ser = ser
        self.on_line = on_line
        self.key = key
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.reader, daemon=True)

    def start(self):
        self.thread.start()
        time.sleep(0.2)
        self.hello()

    def hello(self):
        self.write_line("/echo off")
        if self.key:
            self.write_line("/key " + ascii_tr(self.key))

    def write_line(self, text):
        with self.lock:
            uvterm.paced_write(self.ser, text.encode("ascii", "replace") + b"\r\n")

    def send(self, text):
        """A message of any length: one radio message per 48 characters."""
        parts = chunks(text)
        for p in parts:
            self.write_line(p)
            if len(parts) > 1:
                time.sleep(1.5)       # one transmission + its acknowledgement
        return parts

    def reader(self):
        buf = bytearray()
        while not self.stop.is_set():
            try:
                data = self.ser.read(256)
            except Exception as e:     # unplugged, or closed at exit
                if not self.stop.is_set():
                    self.on_line(f"# baglanti koptu: {e}")
                    self.stop.set()
                break
            buf += data
            while b"\n" in buf:
                raw, _, rest = bytes(buf).partition(b"\n")
                buf = bytearray(rest)
                line = raw.rstrip(b"\r").decode("ascii", "replace")
                if uvterm.classify(line)[0] == "banner":
                    self.hello()       # the app (re)started: echo and key again
                self.on_line(line)

    def close(self):
        self.stop.set()
        self.thread.join(1.0)


# ---------------------------------------------------------------------------
# chat
# ---------------------------------------------------------------------------

def show_line(line):
    p = parse(line)
    t = time.strftime("%H:%M:%S")
    if not p:
        return
    if p[0] == "msg":
        _, call, mark, text = p
        note = {">": "", "*": " (sifreli)", "?": " (imza yok / baska anahtar)"}[mark]
        print(uvterm.color(f"[{t}] ", "2") + uvterm.color(f"{call}{note}: ", "32;1") + text)
    elif p[1] in ("echo off",):
        return
    else:
        print(uvterm.color(f"  · {p[1]}", "2"))


def cmd_chat(args, ser):
    radio = Radio(ser, show_line, args.anahtar)
    radio.start()
    print(uvterm.color(f"rfkopru - {ser.port}. Telsizde RF Mesaj acik olmali (F+7 -> RF Mesaj). "
                       "Yazin + Enter: havaya gider. Cikis: /quit", "36"))
    try:
        while True:
            try:
                text = input()
            except (EOFError, KeyboardInterrupt):
                break
            if text.strip().lower() in ("/quit", "/q", "/exit"):
                break
            if text.strip():
                for p in radio.send(text):
                    print(uvterm.color(f"  > {p}", "2"))
    finally:
        radio.close()


# ---------------------------------------------------------------------------
# Telegram bridge
# ---------------------------------------------------------------------------

class Telegram:
    """The two Bot API calls the bridge needs, over HTTPS (urllib)."""

    def __init__(self, token, opener=urllib.request.urlopen):
        self.base = f"https://api.telegram.org/bot{token}/"
        self.opener = opener
        self.offset = 0

    def call(self, method, params, timeout=35):
        data = json.dumps(params).encode()
        req = urllib.request.Request(self.base + method, data=data,
                                     headers={"Content-Type": "application/json"})
        with self.opener(req, timeout=timeout) as r:
            res = json.loads(r.read().decode())
        if not res.get("ok"):
            raise RuntimeError(res.get("description", "Telegram hatasi"))
        return res["result"]

    def send(self, chat, text):
        return self.call("sendMessage", {"chat_id": chat, "text": text})

    def updates(self, wait=25):
        res = self.call("getUpdates", {"offset": self.offset, "timeout": wait}, timeout=wait + 10)
        for u in res:
            self.offset = max(self.offset, u["update_id"] + 1)
        return [u["message"] for u in res if "message" in u]


class Bridge:
    """Radio messages to the chat, the chat's messages to the radio."""

    def __init__(self, tg, chat, radio_factory):
        self.tg = tg
        self.chat = int(chat)
        self.radio = radio_factory(self.from_radio)

    def from_radio(self, line):
        show_line(line)
        p = parse(line)
        if not p:
            return
        if p[0] == "msg":
            _, call, mark, text = p
            lock = {">": "", "*": " 🔒", "?": " ⚠️"}[mark]
            self.tg.send(self.chat, f"📻 {call}{lock}: {text}")
        elif p[1].startswith("+ aldi:"):
            self.tg.send(self.chat, "✅ telsizde alindi:" + p[1][len("+ aldi:"):])
        elif p[1].startswith("x "):
            self.tg.send(self.chat, "❌ " + p[1][2:])

    def from_chat(self, msg):
        if msg.get("chat", {}).get("id") != self.chat or "text" not in msg:
            return                     # only the configured chat may transmit
        name = msg.get("from", {}).get("first_name", "")
        text = msg["text"]
        if text.startswith("/start"):
            self.tg.send(self.chat, "RF Mesaj koprusu hazir: yazdiklariniz telsizden yayinlanir.")
            return
        prefix = ascii_tr(name)[:10] + ": " if name else ""
        self.radio.send(prefix + text)

    def poll_once(self, wait=25):
        for m in self.tg.updates(wait):
            self.from_chat(m)


def cmd_telegram(args, ser):
    token = args.token or os.environ.get("RFKOPRU_TOKEN")
    chat = args.sohbet or os.environ.get("RFKOPRU_SOHBET")
    if not token or not chat:
        uvterm.die("--token ve --sohbet gerekli (ya da RFKOPRU_TOKEN / RFKOPRU_SOHBET).")
    tg = Telegram(token)
    holder = {}

    def factory(cb):
        holder["r"] = Radio(ser, cb, args.anahtar)
        return holder["r"]
    br = Bridge(tg, chat, factory)
    br.radio.start()
    print(uvterm.color(f"Telegram koprusu calisiyor ({ser.port} <-> sohbet {chat}). Ctrl+C: cikis", "36"))
    try:
        while not br.radio.stop.is_set():
            try:
                br.poll_once()
            except Exception as e:     # network down: keep the bridge alive
                print(uvterm.color(f"  · Telegram: {e}; 10 s sonra tekrar", "33"))
                time.sleep(10)
    except KeyboardInterrupt:
        pass
    finally:
        br.radio.close()


# ---------------------------------------------------------------------------
# automatic answers to "!command" messages
# ---------------------------------------------------------------------------

def builtin_answer(cmd, arg, sender):
    """The built-in commands; None when unknown."""
    if cmd == "saat":
        return time.strftime("Saat %H:%M:%S, %d.%m.%Y")
    if cmd == "ping":
        return f"pong {sender}"
    if cmd == "hava":
        city = arg or "Bolu"
        url = "https://wttr.in/" + urllib.parse.quote(city) + "?format=%l:+%C+%t+%w"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "rfkopru"}),
                                        timeout=10) as r:
                return r.read().decode("utf-8", "replace").strip()
        except Exception as e:
            return f"hava alinamadi: {e.__class__.__name__}"
    if cmd == "yardim":
        return "Komutlar: !saat !ping !hava [sehir] !yardim"
    return None


def answer(text, sender, script=None):
    """The answer to a "!cmd arg" message, or None."""
    m = re.match(r"^!(\w+)\s*(.*)$", text.strip())
    if not m:
        return None
    cmd, arg = m.group(1).lower(), m.group(2).strip()
    if script:
        try:
            out = subprocess.run([script, cmd, arg, sender], capture_output=True, text=True, timeout=30)
            first = out.stdout.strip().splitlines()
            if first:
                return first[0]
        except Exception as e:
            return f"betik hatasi: {e.__class__.__name__}"
    return builtin_answer(cmd, arg, sender)


def cmd_komut(args, ser):
    holder = {}

    def on_line(line):
        show_line(line)
        p = parse(line)
        if p and p[0] == "msg" and p[2] in ">*":          # only messages with our key
            a = answer(p[3], p[1], args.betik)
            if a:
                print(uvterm.color(f"  > cevap: {a}", "2"))
                holder["r"].send(a)
    holder["r"] = Radio(ser, on_line, args.anahtar)
    holder["r"].start()
    print(uvterm.color("Otomatik cevap acik: '!yardim' yazan istasyona komutlar gider. Ctrl+C: cikis", "36"))
    try:
        while not holder["r"].stop.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        holder["r"].close()


def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-p", "--port", default=argparse.SUPPRESS, help="seri port (varsayilan: otomatik)")
    common.add_argument("--anahtar", default=argparse.SUPPRESS,
                        help="grup anahtari: telsize /key ile gonderilir (iki telsizde ayni olmali)")
    ap = argparse.ArgumentParser(prog="rfkopru.py", description="RF Mesaj icin PC koprusu.")
    ap.add_argument("-p", "--port")
    ap.add_argument("--anahtar")
    sub = ap.add_subparsers(dest="cmd", metavar="komut")
    sub.add_parser("sohbet", parents=[common], help="telsizle sohbet (varsayilan)")
    t = sub.add_parser("telegram", parents=[common], help="Telegram sohbeti <-> telsiz")
    t.add_argument("--token", help="Telegram bot token (BotFather)")
    t.add_argument("--sohbet", help="izin verilen sohbet (chat) kimligi")
    k = sub.add_parser("komut", parents=[common], help="'!komut' mesajlarina otomatik cevap")
    k.add_argument("--betik", help="kendi betiginiz: <betik> <komut> <arguman> <cagri> -> ilk satir cevap")
    args = ap.parse_args(argv)
    uvterm.need_pyserial()
    ser = uvterm.open_port(uvterm.find_port(args.port))
    try:
        {"telegram": cmd_telegram, "komut": cmd_komut}.get(args.cmd, cmd_chat)(args, ser)
    finally:
        ser.close()


if __name__ == "__main__":
    main()
