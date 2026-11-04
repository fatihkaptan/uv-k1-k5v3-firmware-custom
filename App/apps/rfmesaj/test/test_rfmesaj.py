#!/usr/bin/env python3
# RF Mesaj host tests: two (or three) radios, each the app built for the
# computer (test/host_rfmesaj.c, a mock BK4819 FSK modem): the packet one
# radio puts on the air is handed to the next. Every packet is also checked
# against an independent Python implementation of the format and of the
# crypto (XTEA CBC-MAC tag, counter-mode text, passphrase key).
#
#   python3 App/apps/rfmesaj/test/test_rfmesaj.py
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(APP))
import host_test as ht  # noqa: E402
from host_test import check, press, script  # noqa: E402

NAME = "rfmesaj"
VER = ht.app_version(APP)
M = 0xFFFFFFFF

# ---- reference implementation ----
def xtea(v, k):
    v0, v1, s = v[0], v[1], 0
    for _ in range(32):
        v0 = (v0 + (((((v1 << 4) & M) ^ (v1 >> 5)) + v1) & M ^ ((s + k[s & 3]) & M))) & M
        s = (s + 0x9E3779B9) & M
        v1 = (v1 + (((((v0 << 4) & M) ^ (v0 >> 5)) + v0) & M ^ ((s + k[(s >> 11) & 3]) & M))) & M
    return [v0, v1]


def mac(b, k):
    w = struct.unpack("<16I", bytes(b[:64]))
    kk = [x ^ 0xA5A5A5A5 for x in k]
    v = [0, 0]
    for i in range(0, 16, 2):
        v = xtea([v[0] ^ w[i], v[1] ^ w[i + 1]], kk)
    return v[0]


def key_from(p):
    b = bytearray(72)
    b[16:16 + min(48, len(p))] = p.encode()[:48]
    key = []
    for l in range(3):
        b[3] = l
        key.append(mac(b, [0, 0, 0, 0]))
    return key + [key[0] ^ key[1] ^ key[2]]


def crc16(b):
    c = 0
    for x in b:
        c ^= x << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x1021) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
    return c


def crypt(pk, k):
    nonce, seq = struct.unpack_from("<I", pk, 4)[0], pk[3]
    t = bytearray(pk[16:64])
    for i in range(0, 12, 2):
        v = xtea([nonce, (seq << 8) | i], k)
        for j, x in enumerate(struct.pack("<2I", *v)):
            t[4 * i + j] ^= x
    return bytes(t)


def parse(hexs):
    pk = bytes.fromhex(hexs)
    magic, flags, seq, nonce = struct.unpack_from("<HBBI", pk)
    call = pk[8:16].split(b"\0")[0].decode()
    tag, crc, tail = struct.unpack_from("<IHH", pk, 64)
    return dict(raw=pk, magic=magic, flags=flags, seq=seq, call=call, text=pk[16:64], mac=tag,
                crc=crc, tail=tail)


KEY = "bolu-ortak-anahtar"
K = key_from(KEY)


def Run(s, seed=1):
    r = ht.Run(APP, NAME, s, seed=seed)
    r.air = [l[4:] for l in r.lines if l.startswith("AIR ")]
    return r


def radio(call, *cmds, key=KEY, host=True):
    pre = [f"call {call}", "host 1" if host else "host 0", "wait 50"]
    if key:
        pre += [f"rx /key {key}\\r", "wait 50"]
    return script(*pre, *cmds)


def tests():
    print("on the air: one message")
    a_cmds = ["rx merhaba Bolu\\r", "wait 500", "state"]       # a transmission takes ~300 ms
    a = Run(radio("TA2AAA", *a_cmds))
    check("one packet sent, keyed up and back", len(a.air) == 1 and "TXON" in a.lines and "TXOFF" in a.lines,
          a.air)
    p = parse(a.air[0])
    check("format: magic, tail, CRC-16 over 68 bytes", p["magic"] == 0x4D52 and p["tail"] == 0xDCBA
          and p["crc"] == crc16(p["raw"][:68]), p)
    check("the sender's callsign in clear (station ID)", p["call"] == "TA2AAA", p["call"])
    check("plain text with a key: readable", p["text"].rstrip(b"\0") == b"merhaba Bolu" and p["flags"] == 0, p)
    check("tag = XTEA CBC-MAC under the passphrase key (Python reference)", p["mac"] == mac(p["raw"], K))
    check("sent line shown and given to the computer", a.last["rows"][-1] == "> merhaba Bolu"
          and b"> merhaba Bolu\r\n" in a.tx, a.last["rows"])

    print("the other radio")
    b = Run(radio("TA2BBB", f"air {a.air[0]}", "wait 1000", "state"))
    check("message shown as 'TA2AAA> ...'", "TA2AAA> merhaba Bolu" in b.last["rows"], b.last["rows"])
    check("and given to its computer", b"TA2AAA> merhaba Bolu\r\n" in b.tx, b.tx[-60:])
    check("notification beep", (1200, 40) in b.tones, b.tones)
    check("one acknowledgement sent back", len(b.air) == 1, b.air)
    ack = parse(b.air[0])
    check("acknowledgement: ACK flag, for TA2AAA's seq, tagged",
          ack["flags"] == 2 and ack["text"][:6] == b"TA2AAA" and ack["text"][8] == p["seq"]
          and ack["mac"] == mac(ack["raw"], K), ack)

    a2 = Run(radio("TA2AAA", *a_cmds[:-1], f"air {b.air[0]}", "wait 500", "state", "wait 8000", "state"))
    check("same seed, same packet (the test's replay is valid)", a2.air[0] == a.air[0])
    check("acknowledged: '# + aldi: TA2BBB', no retry", "# + aldi: TA2BBB" in a2.states[0]["rows"]
          and a2.states[0]["waiting"] == 0 and len(a2.air) == 1, (a2.states[0]["rows"], len(a2.air)))

    a3 = Run(radio("TA2AAA", *a_cmds[:-1], "wait 12000", "state"))
    check("no acknowledgement: 3 transmissions, then '# x iletilemedi'",
          len(a3.air) == 3 and a3.last["rows"][-1] == "# x iletilemedi" and len(set(a3.air)) == 1,
          (len(a3.air), a3.last["rows"][-2:]))

    b2 = Run(radio("TA2BBB", f"air {a.air[0]}", "wait 1000", f"air {a.air[0]}", "wait 1000", "state"))
    check("a repeat is shown once and acknowledged again",
          b2.last["rows"].count("TA2AAA> merhaba Bolu") == 1 and len(b2.air) == 2, (b2.last["rows"], len(b2.air)))

    c = Run(radio("TA2CCC", f"air {a.air[0]}", "wait 1000", "state", key="baska-anahtar"))
    check("another key: shown with '?', not acknowledged",
          "TA2AAA? merhaba Bolu" in c.last["rows"] and not c.air, c.last["rows"])
    n = Run(radio("TA2CCC", f"air {a.air[0]}", "wait 1000", "state", key=None))
    check("no key (HERKES): '?' too", "TA2AAA? merhaba Bolu" in n.last["rows"] and not n.air
          and n.last["mode"] == 0, n.last)

    bad = bytearray(bytes.fromhex(a.air[0]))
    bad[20] ^= 1
    r = Run(radio("TA2BBB", f"air {bad.hex()}", "wait 1000", "state"))
    check("a damaged packet (bad CRC-16) is dropped", not any("merhaba" in x for x in r.last["rows"])
          and not r.air)
    r = Run(radio("TA2BBB", "crcerr 1", f"air {a.air[0]}", "wait 1000", "state"))
    check("a hardware CRC error is dropped", not any("merhaba" in x for x in r.last["rows"]) and not r.air)

    print("GIZLI: encrypted text")
    g_cmds = ["press F", "press 1", "wait 50", "rx gizli bulusma 1400\\r", "wait 500", "state"]
    a = Run(radio("TA2AAA", *g_cmds))
    p = parse(a.air[0])
    check("F+1: GIZLI, with the legal warning", a.last["mode"] == 2
          and "# UYARI: amatorde sifre yasak!" in a.last["rows"], a.last["rows"])
    check("the text on the air is not readable", b"gizli" not in p["raw"] and p["flags"] == 1, p["text"])
    check("decrypts with the reference (XTEA counter mode)",
          crypt(p["raw"], K).rstrip(b"\0") == b"gizli bulusma 1400")
    check("tag over the ciphertext", p["mac"] == mac(p["raw"], K))
    b = Run(radio("TA2BBB", f"air {a.air[0]}", "wait 1000", "state"))
    check("same key: decrypted, shown with '*', acknowledged",
          "TA2AAA* gizli bulusma 1400" in b.last["rows"] and len(b.air) == 1, b.last["rows"])
    c = Run(radio("TA2CCC", f"air {a.air[0]}", "wait 1000", "state", key="yanlis"))
    check("another key: '(cozulemedi)'", "TA2AAA? (cozulemedi)" in c.last["rows"], c.last["rows"])
    r = Run(radio("TA2AAA", "press F", "press 1", "wait 50", "state", key=None))
    check("GIZLI needs a key", r.last["mode"] == 0 and "# Once anahtar: F+2" in r.last["rows"], r.last["rows"])

    print("keypad, settings, TX refused, computer")
    r = Run(radio("TA2AAA", "press F", "press 2", "wait 50", *press(2, 2), "wait 1000", *press(2), "wait 1000",
                  "press MENU", "wait 50", "state", "press F", "press 3", "wait 50", "state", key=None))
    check("F+2 then a line + MENU sets the key", "# Anahtar ayarlandi" in r.states[0]["rows"]
          and r.states[0]["mode"] == 1, r.states[0]["rows"])
    cfg = r.cfg
    check("saved key = the reference key of 'ba'", cfg is not None and list(struct.unpack_from("<3I", cfg, 4))
          == key_from("ba")[:3], cfg)
    check("F+3: beep off, saved", r.states[1]["rows"][-1] == "# Ses kapali" and cfg[1] & 4, r.states[1]["rows"])
    r = Run(radio("TA2AAA", *press(4, 4), "wait 1000", *press(4, 4, 4), "wait 1000", "press MENU", "wait 500",
                  "state"))
    check("keypad: 'hi' + MENU goes on the air", len(r.air) == 1 and parse(r.air[0])["text"][:2] == b"hi"
          and r.last["in"] == "", r.last)
    r = Run(radio("TA2AAA", "txstate 1", *press(4, 4), "wait 1000", "press MENU", "wait 50", "rx abc\\r",
                  "wait 50", "state"))
    check("TX refused (lock, battery, not FM): said, nothing sent, the line kept",
          not r.air and "# x TX yok (kilit/pil/FM degil)" in r.last["rows"] and r.last["in"] == "h", r.last)
    r = Run(radio("TA2AAA", "rx /echo off\\r", "wait 50"))
    check("banner with the callsign, /echo off answered (uvterm.py works)",
          r.tx.startswith(f"# RF Mesaj {VER} ready - TA2AAA\r\n".encode()) and b"# echo off\r\n" in r.tx, r.tx[:80])
    r = Run(radio("TA2AAA", "rx \\xc3\\xa7ay\\r", "wait 100", key=None))
    check("a UTF-8 letter from the computer becomes '?'", parse(r.air[0])["text"][:3] == b"?ay")


def mockups():
    a = Run(radio("TA2AAA", "rx Bolu'dan selam! Abant'tayiz\\r", "wait 500"))
    b = Run(radio("TA2BBB", f"air {a.air[0]}", "wait 1000", "rx Tamam, aksama geliyoruz\\r", "wait 500",
                  *press(8), "wait 1000", *press(2), "wait 1000", *press(6), "wait 1000", *press(2), "wait 1000",
                  *press(6), "wait 1000", *press(0), "wait 1000", *press(7), "wait 1000", *press(3), "wait 50",
                  "shot chat"))
    path = ht.png(APP, "chat")
    if path:
        print(f"  mockup {os.path.relpath(path, ht.ROOT)}")


if __name__ == "__main__":
    ht.build(APP, NAME)
    tests()
    mockups()
    ht.finish()
