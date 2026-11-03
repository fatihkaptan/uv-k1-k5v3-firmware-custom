#!/usr/bin/env python3
# USB Term read-only assets: screen texts, serial replies, the command table,
# the multi-tap keypad map and the UTF-8 -> ASCII transliteration table.
#
#   ./gen_assets.py usbterm_assets.bin usbterm_assets.h
#
# APP_VER comes from build.sh (environment), so the banner and /info always
# show the version packed into the .app header.
import os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from app_assets import Assets

VER = os.environ.get("APP_VER", "1.0")

a = Assets("USBTERM")

# ---- status line ----
a.text("T_TITLE", "TERM")
a.table("T_CAPS", ["USB", "NO USB"])            # host has the port open (DTR) or not
a.table("T_MODES", ["abc", "ABC", "123"])       # keypad input mode, cycled by *
a.text("T_SOUND", "BEEP")                        # notification sound on

# ---- serial replies (radio -> computer). Every reply line starts with "# "
# so that a program on the computer can tell them from chat text. ----
a.text("T_BANNER", f"# USB Term {VER} ready - /help")
a.text("T_INFO", f"# USB Term {VER}")
a.text("T_FW", " / F4HWN ")
a.text("T_RX", "# RX ")
a.text("T_MHZ", " MHz  ")
a.text("T_DBM", " dBm")
a.text("T_BAT", "# BAT ")
a.text("T_VOLT", " V  ")
a.text("T_LOST", "lost ")
a.text("T_HELP1", "# /info /ping /beep /clear")
a.text("T_HELP2", "# /echo on  /echo off")

# ---- commands from the computer: a whole line "/<name>", any case. The
# order is the C_* enum of usbterm_app.c; T_RESP is the one-line reply. ----
CMDS = ["help", "info", "ping", "beep", "clear", "echo on", "echo off"]
a.table("CMDS", CMDS)
a.table("T_RESP", ["", "", "# pong", "# beep", "# clear", "# echo on", "# echo off"])

# ---- multi-tap keypad (phone style): key k cycles through KEYMAP[k]; the
# digit is the last entry, and a long press types it directly. ----
a.table("KEYMAP", [
    " 0",                    # 0
    ".,?!-'/:@()+=*#1",      # 1
    "abc2", "def3", "ghi4", "jkl5", "mno6", "pqrs7", "tuv8", "wxyz9",
])

# ---- UTF-8 two-byte letters the 3x5 font cannot draw: (lead, cont, ASCII).
# Turkish first; anything else shows as '?'. ----
PAIRS = "çcÇCğgĞGıiİIöoÖOşsŞSüuÜUâaÂAîiÎIûuÛUéeÉEäaÄAàaèe"
trl = bytearray()
for i in range(0, len(PAIRS), 2):
    ch, asc = PAIRS[i], PAIRS[i + 1]
    b = ch.encode("utf-8")
    assert len(b) == 2, ch
    trl += bytes([b[0], b[1], ord(asc)])
a.raw("TRL", trl)

a.main()
