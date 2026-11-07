#!/usr/bin/env python3
# Mors Okur read-only assets: texts and the Morse table.
#
#   ./gen_assets.py morsokur_assets.bin morsokur_assets.h
#
# MORSE[code] is the character of a pattern of up to six elements: code = 1,
# then one bit per element, dot 0, dash 1 ("-.-" = 0b1101 = 13). Unknown
# patterns are "_". The Turkish letters are shown in lower case (the font has
# no accents): c = C cedilla, g = G breve, o = O umlaut, s = S cedilla, u = U
# umlaut.
import os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from app_assets import Assets

VER = os.environ.get("APP_VER", "1.1")
a = Assets("MORSOKUR")

a.text("T_TITLE", "MORS OKUR")
a.text("T_TON", "TON")
a.text("T_WPM", " WPM")
a.text("T_OTO", " OTO")
a.table("T_HELP", ["Mikrofona mors calin:", "duduk, osilator, hoparlor", "UP/DN hiz  1-9 hassasiyet",
                   "F oto hiz  MENU sil  0 kaynak"])
a.text("T_BANNER", f"# Mors Okur {VER} ready")
a.text("T_ECHO", "# echo off")

MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....",
    "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.",
    "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....",
    "7": "--...", "8": "---..", "9": "----.",
    ".": ".-.-.-", ",": "--..--", "?": "..--..", "/": "-..-.", "=": "-...-", "+": ".-.-.", "-": "-....-",
    "@": ".--.-.", "'": ".----.", "(": "-.--.", ")": "-.--.-", ":": "---...", "!": "-.-.--", '"': ".-..-.",
    # Turkish: C cedilla, G breve, O umlaut, S cedilla, U umlaut
    "c": "-.-..", "g": "--.-.", "o": "---.", "s": ".--..", "u": "..--",
}
table = bytearray(b"_" * 128)
for ch, p in MORSE.items():
    code = 1
    for e in p:
        code = code << 1 | (e == "-")
    assert code < 128 and table[code] == ord("_"), ch
    table[code] = ord(ch)
a.raw("MORSE", table)

if __name__ == "__main__":
    a.main()
