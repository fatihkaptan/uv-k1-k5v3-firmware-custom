#!/usr/bin/env python3
# Anten Lab read-only assets: texts, the attenuator ladder (Fox Hunt's REG_13
# gain steps), sin(10 degrees x k), and the 1024-byte block the loader keeps
# at exit (APP_FLAG_SAVE_SCREEN): the last pattern and the reference.
#
#   ./gen_assets.py antenlab_assets.bin antenlab_assets.h
import math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from app_assets import Assets

VER = os.environ.get("APP_VER", "1.0")
a = Assets("ANTENLAB")

a.text("T_TITLE", "ANTEN LAB")
a.table("T_MODE", ["ADIM", "TUR"])
a.text("T_REF", "REF")
a.text("T_YON", "Yon ")
a.text("T_TEPE", "Tepe ")
a.text("T_FB", "O/A ")
a.text("T_BW", "3dB ")
a.text("T_DB", "dB")
a.text("T_ATT", "Zayif ")
a.text("T_SURE", "Sure ")
a.text("T_S", " s")
a.text("T_HAZIR", "MENU basla")
a.text("T_HELP", "1 mod 2 sure 3 zayif 4 ref")
a.text("T_HELP2", "5 ref goster 0 sil F USB")
a.text("T_REFOK", "Referans kaydedildi")
a.text("T_BANNER", f"# Anten Lab {VER} ready")
a.text("T_CSV", "derece,dBm,ref_dBm")
a.text("T_ECHO", "# echo off")

a.u16("ATT_REG13", [0x03DF, 0x03DD, 0x03DB, 0x03D9])   # REG_13 gain bits (Fox Hunt)
a.u8("ATT_DB", [0, 6, 15, 27])                           # their attenuation
a.i8("SIN", [round(127 * math.sin(math.radians(10 * k))) for k in range(36)])

a.raw("SAVE", bytes(1024))      # must stay last: the loader rewrites the last 1024 B
a.main()
