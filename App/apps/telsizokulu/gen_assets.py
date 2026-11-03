#!/usr/bin/env python3
# Telsiz Okulu read-only assets: every text the app shows, the question bank,
# the Q codes, the phonetic alphabet, the amateur bands and the band plan.
#
#   ./gen_assets.py telsizokulu_assets.bin telsizokulu_assets.h
#
# Texts are ASCII (the radio fonts have no Turkish letters): c for ç, g for ğ,
# i for ı, o for ö, s for ş, u for ü. A line of the 6x7 font holds 18
# characters: answers are at most 16 (after "1 "), questions at most 3 lines.
import os, struct, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from app_assets import Assets
import collections


def build_dict(corpus, max_codes=128, min_len=2, max_len=12):
    """Greedy substring dictionary for the long texts: the substring that saves
    the most bytes becomes byte 0x80 + k, again and again. Entries never hold a
    NUL or another code, so the app expands a byte with one asset read."""
    seqs = [bytes(b) for b in corpus]
    entries = []
    for k in range(max_codes):
        counts = collections.Counter()
        for s in seqs:
            for i in range(len(s)):
                if s[i] == 0 or s[i] >= 0x80:
                    continue
                for n in range(min_len, max_len + 1):
                    if i + n > len(s) or s[i + n - 1] == 0 or s[i + n - 1] >= 0x80:
                        break
                    counts[s[i:i + n]] += 1
        best, gain = None, 0
        for sub, cnt in counts.items():          # the entry costs its bytes + a u16 offset
            g = cnt * (len(sub) - 1) - (len(sub) + 2)
            if g > gain or (g == gain and best is not None and sub < best):
                best, gain = sub, g
        if not best:
            break
        seqs = [s.replace(best, bytes([0x80 + k])) for s in seqs]
        entries.append(best)
    return entries


def encode(entries, text):
    b = text.encode("ascii")
    for k, e in enumerate(entries):
        b = b.replace(e, bytes([0x80 + k]))
    return b


a = Assets("TELSIZOKULU")

# ---- screens ----
a.text("T_TITLE", "TELSIZ OKULU")
MENU = ["Sinav", "Q kodlari", "Fonetik alfabe", "Bant plani", "Anten hesabi"]
a.table("T_MENU", MENU)
a.text("T_BEST", "En iyi puan ")
a.text("T_HINT", "1-5 / MENU sec  EXIT cik")
a.text("T_OK", "DOGRU")
a.text("T_BAD", "YANLIS")
a.text("T_SORU", "SORU ")
a.text("T_SCORE", "Puan")
a.table("T_VERDICT", ["Harika!", "Iyi gidiyorsun", "Calismaya devam"])
a.text("T_AGAIN", "MENU yeni tur  EXIT menu")
a.text("T_FLIP", "MENU: anlami goster")
a.text("T_CALL", "Cagri isareti yaz")
a.text("T_STROKE", "Stroke")           # '/' in a callsign, ITU spelling
a.text("T_NOTLIST", "Bu frekans listede yok")
a.text("T_BANDHINT", "UP/DOWN gez  MENU VFO")
a.text("T_ANTHINT", "rakam,* nokta  boylar x0.95")
a.table("T_ANT", ["Tam dalga", "1/4 dalga", "1/2 dipol", "5/8 dalga"])
a.text("T_VFO", "VFO ")
a.text("T_F", "f   ")
a.text("T_MHZ", " MHz")
a.text("T_QHINT", "  MENU cevir  UP/DOWN gez")
# multi-tap keypad of the phonetic speller: callsigns, upper case
a.table("KEYMAP", ["0", "1/", "ABC2", "DEF3", "GHI4", "JKL5", "MNO6", "PQRS7", "TUV8", "WXYZ9"])

# ---- generated questions: the pieces they are built from ----
a.text("T_QF", "' ne demektir?")              # "'QTH' ne demektir?"
a.text("T_QR", "' hangi Q kodu?")             # "'Konum' hangi Q kodu?"
a.text("T_BQ", " MHz hangi amator bandidir?")
a.text("T_OHM", "Ohm yasasi: U=")             # "Ohm yasasi: U=12 V, R=4 ohm ise I=?"
a.text("T_OHM2", " V, R=")
a.text("T_OHM3", " ohm ise akim I=?")
a.table("T_UNIT", [" V", " A", " ohm", " W", " cm", " m"])   # U I R P, antenna

# ---- Q codes: code and a meaning of at most 16 characters ----
QCODES = [
    ("QRA", "Istasyon adi"), ("QRG", "Tam frekans"), ("QRK", "Okunabilirlik"),
    ("QRL", "Frekans mesgul"), ("QRM", "Insan paraziti"), ("QRN", "Dogal parazit"),
    ("QRO", "Gucu artir"), ("QRP", "Dusuk guc"), ("QRQ", "Hizli gonder"),
    ("QRS", "Yavas gonder"), ("QRT", "Yayini bitir"), ("QRU", "Mesajim yok"),
    ("QRV", "Hazirim"), ("QRX", "Bekle"), ("QRZ", "Beni kim cagirdi"),
    ("QSB", "Sinyal sonumu"), ("QSL", "Alindi, teyit"), ("QSO", "Gorusme"),
    ("QSP", "Mesaj aktar"), ("QSY", "Frekans degistir"), ("QTH", "Konum"),
    ("QTR", "Tam saat"),
]
a.table("QC_CODE", [c for c, _ in QCODES])
a.const("NQC", len(QCODES))
assert all(len(m) <= 16 for _, m in QCODES)

# ---- ITU phonetic alphabet: A-Z then 0-9, NUL separated ----
PHON = ("Alfa Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliett Kilo Lima Mike "
        "November Oscar Papa Quebec Romeo Sierra Tango Uniform Victor Whiskey X-ray "
        "Yankee Zulu Zero One Two Three Four Five Six Seven Eight Nine").split()
assert len(PHON) == 36
a.raw("PHON", b"".join(w.encode() + b"\0" for w in PHON))

# ---- amateur bands (quiz): kHz ranges, IARU Region 1 ----
BANDS = [("80 m", 3500, 3800), ("40 m", 7000, 7200), ("20 m", 14000, 14350),
         ("15 m", 21000, 21450), ("10 m", 28000, 29700), ("6 m", 50000, 52000),
         ("2 m", 144000, 146000), ("70 cm", 430000, 440000), ("23 cm", 1240000, 1300000)]
a.table("BAND_NAME", [n for n, _, _ in BANDS])
a.u32("BAND_KHZ", [v for _, lo, hi in BANDS for v in (lo, hi)])
a.const("NBAND", len(BANDS))

# ---- band plan (summary of the IARU Region 1 plans, plus a few services):
# sorted kHz ranges [lo, hi), the text of each at SEG_TXT + offset ----
SEGS = [
    (28000, 29700, "10 m amator bandi (HF)"),
    (50000, 52000, "6 m amator bandi"),
    (87500, 108000, "FM radyo yayinlari"),
    (108000, 118000, "Havacilik seyrusefer (VOR, ILS)"),
    (118000, 137000, "Havacilik telsizi (AM)"),
    (144000, 144150, "2 m: CW, EME (144.050 CW)"),
    (144150, 144400, "2 m: SSB/CW (144.300 SSB cagri)"),
    (144400, 144490, "2 m: Beacon (isaret vericileri)"),
    (144490, 144794, "2 m: Tum modlar (SSTV, RTTY)"),
    (144794, 144990, "2 m: Dijital (144.800 APRS)"),
    (144990, 145194, "2 m: Role girisleri"),
    (145194, 145206, "2 m: Uzay haberlesmesi"),
    (145206, 145594, "2 m: FM simplex (145.500 cagri)"),
    (145594, 145794, "2 m: Role cikislari (-600 kHz)"),
    (145794, 145806, "2 m: Uzay haberlesmesi"),
    (145806, 146000, "2 m: Uydu (145.800 ISS)"),
    (156000, 162050, "Deniz VHF (Kanal 16: 156.800)"),
    (430000, 432000, "70 cm: Tum modlar, roleler"),
    (432000, 432150, "70 cm: CW, EME"),
    (432150, 432500, "70 cm: SSB/CW (432.200 cagri)"),
    (432500, 433400, "70 cm: Tum modlar"),
    (433400, 433600, "70 cm: FM simplex (433.500 cagri)"),
    (433600, 435000, "70 cm: Tum modlar, dijital"),
    (435000, 438000, "70 cm: Uydu haberlesmesi"),
    (438000, 440000, "70 cm: Roleler, dijital, ATV"),
    (446000, 446200, "PMR446: lisanssiz, amator degil"),
    (1240000, 1300000, "23 cm amator bandi"),
]
assert all(SEGS[i][1] <= SEGS[i + 1][0] for i in range(len(SEGS) - 1))
a.const("NSEG", len(SEGS))
a.const("SEG_REC", 10)

# ---- question bank: question, then the right answer, then three wrong
# ones (the app shuffles them). Answers at most 16 characters. ----
FIX = [
    ("Telsizde 'CQ' ne anlama gelir?", "Genel cagri", "Acil durum", "Anlasildi", "Bekle"),
    ("'73' ne demektir?", "En iyi dilekler", "Yardim edin", "Frekans mesgul", "Sesin zayif"),
    ("Hayati tehlikede yapilan sesli imdat cagrisi?", "MAYDAY", "PAN PAN", "SECURITE", "CQ DX"),
    ("RST raporunda 59 ne demektir?", "Net ve guclu", "Zor okunur", "Cok parazitli", "Sinyal yok"),
    ("Anten icin ideal SWR degeri?", "1:1", "3:1", "5:1", "10:1"),
    ("Role (repeater) ne yapar?", "Yeniden yayinlar", "Sesi kaydeder", "Frekans olcer", "Anteni ayarlar"),
    ("CTCSS ne ise yarar?", "Tonlu susturucu", "Gucu artirir", "Frekans kaydirir", "Pil tasarrufu"),
    ("Bolge 1'de 2 m FM simplex cagri frekansi?", "145.500 MHz", "144.800 MHz", "145.800 MHz", "146.520 MHz"),
    ("Bolge 1'de 2 m APRS frekansi?", "144.800 MHz", "145.500 MHz", "144.390 MHz", "433.500 MHz"),
    ("VHF hangi frekans araligidir?", "30-300 MHz", "3-30 MHz", "300-3000 MHz", "0.3-3 MHz"),
    ("UHF hangi frekans araligidir?", "300-3000 MHz", "30-300 MHz", "3-30 MHz", "3-30 GHz"),
    ("HF (kisa dalga) hangi araliktir?", "3-30 MHz", "30-300 MHz", "300-3000 kHz", "3-30 GHz"),
    ("VHF/UHF menzili en cok neye baglidir?", "Gorus hattina", "Iyonosfere", "Ay evresine", "Hava nemine"),
    ("HF'de uzak mesafe (DX) baglantisi neyle olur?", "Iyonosferle", "Uydu ile", "Kablo ile", "Gorus hattiyla"),
    ("Guc 2 katina cikarsa artis kac dB?", "3 dB", "2 dB", "6 dB", "10 dB"),
    ("Guc 10 katina cikarsa artis kac dB?", "10 dB", "3 dB", "20 dB", "100 dB"),
    ("Turkiye'nin amator cagri isareti oneki?", "TA", "DL", "JA", "G"),
    ("Turkiye'de amator telsiz iznini veren kurum?", "BTK", "TRT", "RTUK", "TSE"),
    ("FM'de bilgi neyle tasinir?", "Frekans degisimi", "Genlik degisimi", "Isik siddeti", "Kablo boyu"),
    ("SSB'nin acilimi nedir?", "Tek yan bant", "Cift yan bant", "Genis bant", "Sabit sinyal"),
    ("Squelch (susturucu) ne yapar?", "Gurultuyu keser", "Gucu artirir", "Frekans tarar", "Sesi kaydeder"),
    ("2 adet 100 ohm direnc seri baglanirsa?", "200 ohm", "50 ohm", "100 ohm", "10 ohm"),
    ("2 adet 100 ohm direnc paralel baglanirsa?", "50 ohm", "200 ohm", "100 ohm", "25 ohm"),
    ("Cagri yapmadan once ne yapilmalidir?", "Frekansi dinle", "Gucu artir", "Hemen CQ ver", "Anteni sok"),
    ("QSL karti ne icin gonderilir?", "Gorusme teyidi", "Odeme icin", "Sikayet icin", "Ruhsat icin"),
    ("Bolge 1'de 2 m role kaydirmasi?", "600 kHz", "5 MHz", "1.6 MHz", "7.6 MHz"),
    ("ISS'in 2 m ses indirme frekansi?", "145.800 MHz", "145.500 MHz", "144.800 MHz", "433.500 MHz"),
    ("Dalga boyu (metre) nasil bulunur?", "300 / f (MHz)", "f / 300", "f x 300", "3000 / f"),
    ("Cagri isaretinde '/M' ne demektir?", "Mobil (aracta)", "Denizde", "Ev istasyonu", "Mesgul"),
    ("Cagri isaretinde '/P' ne demektir?", "Portatif", "Polis", "Pil ile", "Parazitli"),
]
for q in FIX:
    assert len(q) == 5 and all(len(x) <= 16 for x in q[1:]), q
    assert len(set(q[1:])) == 4, q
a.const("NFIX", len(FIX))

# ---- the long texts share one dictionary: question blocks (question NUL
# answer NUL x4), band plan texts, Q code meanings (each NUL-terminated) ----
fix_txt = ["\0".join(q) + "\0" for q in FIX]
seg_txt = [t + "\0" for _, _, t in SEGS]
qc_txt = [m + "\0" for _, m in QCODES]
entries = build_dict([b"".join(x.encode() for x in group) for group in (fix_txt, seg_txt, qc_txt)])
assert len(entries) <= 128
offs, dict_blob = [], bytearray()
for e in entries:
    offs.append(len(dict_blob))
    dict_blob += e
a.u16("DICT_OFF", offs + [len(dict_blob)])
a.raw("DICT", dict_blob)

def packed(name, texts):
    blob, offs = bytearray(), []
    for t in texts:
        offs.append(len(blob))
        blob += encode(entries, t)
    a.raw(name, blob)
    return offs

fix_offs = packed("FIX", fix_txt)
a.u16("FIX_OFF", fix_offs)
a.const("FIX_MAX", max(len("\0".join(q)) + 1 for q in FIX))    # expanded size
seg_offs = packed("SEG_TXT", seg_txt)
a.raw("SEG", b"".join(struct.pack("<IIH", lo, hi, o) for (lo, hi, _), o in zip(SEGS, seg_offs)))
a.u16("QC_MEAN", packed("QC_TXT", qc_txt))
a.main()
