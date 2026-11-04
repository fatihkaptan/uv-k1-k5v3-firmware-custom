#!/usr/bin/env python3
# QSO Defteri read-only assets: texts, the callsign keypad, and the
# 1024-byte block the loader keeps at exit (APP_FLAG_SAVE_SCREEN): the log.
#
#   ./gen_assets.py qsodefteri_assets.bin qsodefteri_assets.h
import os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from app_assets import Assets

VER = os.environ.get("APP_VER", "1.0")
a = Assets("QSODEFTERI")

a.text("T_TITLE", "DEFTER")
a.text("T_EMPTY", "Defter bos")
a.text("T_NEWHINT", "MENU: yeni QSO")
a.text("T_LISTHINT", "MENU yeni  F islem  EXIT cik")
a.text("T_FHINT", "F: 1 saat 2 USB 3 sil 0 hepsi")
a.text("T_SURE", "Emin misiniz? Ayni tusa basin")
a.text("T_FULL", "Defter dolu: USB ile aktarin")
a.table("T_FIELD", ["Cagri ", "Verilen ", "Alinan "])
a.text("T_FORMHINT", "UP/DN alan MENU kaydet EXIT sil")
a.text("T_TEKRAR", " tekrar")
a.text("T_NOCLOCK", "Saat yok: F+1 ya da PC")
a.text("T_TIMEHINT", "YYAAGGssdd  MENU tamam")
a.text("T_TIME", "UTC saat")
a.table("T_MODE", ["FM", "AM", "SSB"])
a.text("T_MHZ", " MHz ")
a.text("T_Z", "Z")
a.text("T_BANNER", f"# QSO Defteri {VER} ready")
a.text("T_CSV", "call,khz,unix,rst_s,rst_r,mode")
a.text("T_OK", "# tamam")
a.text("T_ECHO", "# echo off")

a.table("KEYMAP", ["0", "1/", "ABC2", "DEF3", "GHI4", "JKL5", "MNO6", "PQRS7", "TUV8", "WXYZ9"])
a.raw("SAVE", bytes(1024))      # must stay last: the loader rewrites the last 1024 B
a.main()
