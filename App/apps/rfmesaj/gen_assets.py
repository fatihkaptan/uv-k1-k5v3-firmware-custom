#!/usr/bin/env python3
# RF Mesaj read-only assets: texts, the multi-tap keypad, the UTF-8 -> ASCII
# table and the BK4819 FSK register sequences (those of the BEAM app, proven
# between radios: 1200 bps FSK, 72-byte packets, hardware CRC).
#
#   ./gen_assets.py rfmesaj_assets.bin rfmesaj_assets.h
import os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from app_assets import Assets

VER = os.environ.get("APP_VER", "1.0")
a = Assets("RFMESAJ")

# ---- screen ----
a.text("T_TITLE", "RF MESAJ")
a.table("T_MODE", ["HERKES", "IMZALI", "GIZLI"])     # no key / key / key + encryption
a.table("T_MODES", ["abc", "ABC", "123"])
a.text("T_TX", "TX")
a.text("T_USB", "USB")
a.text("T_F", "F")

# ---- system lines, on the screen and to the computer ("# ...") ----
a.text("T_HELLO", "# F+1 mod F+2 anahtar F+3 ses")
a.text("T_NOCALL", "# Cagri isareti yok: PonMsg")
a.text("T_KEYASK", "# Anahtari yaz, MENU")
a.text("T_KEYSET", "# Anahtar ayarlandi")
a.text("T_NEEDKEY", "# Once anahtar: F+2")
a.text("T_WARN", "# UYARI: amatorde sifre yasak!")      # ITU RR 25.2A
a.table("T_MODESET", ["# Mod: HERKES (anahtarsiz)", "# Mod: IMZALI (acik metin)", "# Mod: GIZLI (sifreli)"])
a.text("T_ACKED", "# + aldi: ")
a.text("T_FAIL", "# x iletilemedi")
a.text("T_TXNO", "# x TX yok (kilit/pil/FM degil)")
a.table("T_SOUND", ["# Ses kapali", "# Ses acik"])
a.text("T_BANNER", f"# RF Mesaj {VER} ready - ")
a.text("T_ECHO", "# echo off")               # uvterm.py's handshake
a.text("T_INFO", f"# RF Mesaj {VER} ")


a.table("KEYMAP", [" 0", ".,?!-'/:@()+=*#1", "abc2", "def3", "ghi4", "jkl5", "mno6",
                   "pqrs7", "tuv8", "wxyz9"])

# ---- BK4819 FSK register sequences (BEAM): (register, value) word pairs,
# register SEQ_DELAY meaning "wait value ms" ----
SEQ_DELAY = 0xFF
a.const("SEQ_DELAY", SEQ_DELAY)


def seq(name, pairs):
    a.u16(name, [w for pair in pairs for w in pair])


RESET = [                       # BK4819_ResetFSK
    (0x3F, 0x0000), (0x59, 0x0068), (SEQ_DELAY, 30), (0x30, 0x0000),
]
seq("SEQ_RESET", RESET)
seq("SEQ_SETUP", [              # BK4819_SetupAircopy + BK4819_ResetFSK
    (0x70, 0x00C3),             # Tone2 on, tuning gain 48
    (0x72, 0x3065),             # Tone2 baud rate 1200
    (0x58, 0x00C1),             # FSK on, 1.2K RX bandwidth, TX/RX FSK 1.2K
    (0x5C, 0x5665),             # CRC on
    (0x5D, 0x4700),             # FSK data length 72 bytes
    (0x5E, 0x3204),
] + RESET)
seq("SEQ_RX", RESET + [         # BK4819_PrepareFSKReceive
    (0x02, 0x0000), (0x3F, 0x0000), (0x37, 0x9F1F), (0x30, 0x0000), (0x30, 0xBFF1),
    (0x3F, 0x3000),             # RX finished | FIFO almost full interrupts
    (0x59, 0x4068), (0x59, 0x3068),
])
seq("SEQ_TX_LOAD", [(SEQ_DELAY, 30), (0x3F, 0x8000), (0x59, 0x8068), (0x59, 0x0068)])
seq("SEQ_TX_GO", [(SEQ_DELAY, 20), (0x59, 0x2868)])
seq("SEQ_TX_END", [(0x02, 0x0000), (SEQ_DELAY, 30)] + RESET + [(0x36, 0x0088)])
a.main()
