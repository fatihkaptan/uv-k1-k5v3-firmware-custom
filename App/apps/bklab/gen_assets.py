#!/usr/bin/env python3
# BK Lab read-only assets: texts, and short names of the BK4819 registers
# whose use is clear from the firmware's driver (App/driver/bk4829.c); the
# others stay unnamed. tools/bklab/bklab.py carries the same table.
#
#   ./gen_assets.py bklab_assets.bin bklab_assets.h
import os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from app_assets import Assets

VER = os.environ.get("APP_VER", "1.0")
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
PROTECTED = [0x30, 0x33, 0x36]      # can key the transmitter: two-step write
a = Assets("BKLAB")

a.text("T_TITLE", "BK LAB")
a.text("T_USB", "USB")
a.text("T_HINT", "MENU bit 0-7 git EXIT cik")
a.text("T_BITHINT", "UP/DN bit MENU cevir F yaz *geri")
a.text("T_ARM", "TX RISKI! F tekrar: yaz")
a.text("T_BIT", "bit ")
a.text("T_CIP", "  cip ")
a.text("T_BANNER", f"# BK Lab {VER} ready")
a.text("T_PROT", "! korumali (TX): w! ile yazin")
a.text("T_BAD", "! komut: r w w! d m s geri")
a.text("T_GERI", "# geri yuklendi ")
a.text("T_ECHO", "# echo off")
a.table("NAMES", [NAMES.get(r, "") for r in range(0x80)])
a.u8("PROT", PROTECTED)
a.main()
