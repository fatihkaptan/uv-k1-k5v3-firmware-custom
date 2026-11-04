#!/usr/bin/env python3
# uvterm tests without a radio: a fake radio that implements the resident
# serial protocol the way App/app/uart.c and App/apps/app_overlay.c do
# (framing, obfuscation, CRC, timestamp check, slot erase / write / validate
# on a NOR-like flash), and the install / apps code of uvterm run against it.
#
#   python3 tools/uvterm/test_uvterm.py
import io, os, struct, sys, tempfile, zlib
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import uvterm  # noqa: E402

SLOT_STRIDE = 0x2000
REGION_BASE = 0x102000
AVAILABLE_CAPS = 0x01 | 0x08 | 0x10 | 0x20 | 0x40     # a Labs build


class FakeRadio:
    """The resident side of the protocol, byte for byte."""

    def __init__(self, version="v6.3.0 Labs", caps=AVAILABLE_CAPS):
        self.port = "fake"
        self.flash = bytearray(b"\xFF" * (48 * SLOT_STRIDE))
        self.rx = bytearray()          # host -> radio
        self.out = bytearray()         # radio -> host
        self.ts = None
        self.version = version
        self.caps = caps
        self.noise = b""               # bytes mixed in before each reply (K5Viewer, junk)
        self.writes = 0
        self.erases = 0

    # -- serial.Serial duck type --
    def write(self, data):
        self.rx += data
        self.process()
        return len(data)

    def flush(self):
        pass

    def read(self, n=1):
        d = bytes(self.out[:n])
        del self.out[:n]
        return d

    def close(self):
        pass

    # -- firmware --
    def reply(self, body):
        size = len(body)
        enc = uvterm.obfuscate(body + b"\xFF\xFF")       # footer: Obfuscation ^ 0xFF
        self.out += self.noise + b"\xAB\xCD" + struct.pack("<H", size) + enc + b"\xDC\xBA"

    def process(self):
        while True:
            i = self.rx.find(b"\xAB\xCD")
            if i < 0 or len(self.rx) - i < 8:
                return
            del self.rx[:i]
            size = self.rx[2] | self.rx[3] << 8
            if size + 8 > 256:
                raise AssertionError(f"packet of {size + 8} B: larger than the 256-byte ring")
            if len(self.rx) < size + 8:
                return
            assert self.rx[4 + size + 2:4 + size + 4] == b"\xDC\xBA", "bad tail"
            buf = uvterm.obfuscate(bytes(self.rx[4:4 + size + 2]))
            del self.rx[:size + 8]
            crc = buf[size] | buf[size + 1] << 8
            assert uvterm.crc16_xmodem(buf[:size]) == crc, "bad CRC"
            msg_id, msg_size = struct.unpack_from("<HH", buf)
            assert msg_size <= size - 4, "header size larger than the packet"
            self.command(msg_id, buf[4:4 + msg_size])

    def base(self, slot):
        return slot * SLOT_STRIDE

    def validate(self, slot):
        h = self.flash[self.base(slot):self.base(slot) + 64]
        (magic, hv, abi, api_min, code_size, _crc, entry, flags, _n, _v, _vma, caps,
         asset_size, _acrc) = uvterm.APP_HEADER.unpack(h)
        if struct.unpack("<I", magic)[0] != uvterm.APP_MAGIC or hv != 1:
            return 2
        if abi != 1 or api_min == 0 or api_min > 3:
            return 3
        if not flags & 1:
            return 4
        if caps & ~self.caps:
            return 9
        if code_size < 2 or code_size > 0x1000 or entry > code_size - 2 or entry & 1 \
                or asset_size > 0xF00:
            return 5
        return 0

    def command(self, msg_id, d):
        if msg_id == 0x0514:
            self.ts = struct.unpack_from("<I", d)[0]
            self.reply(struct.pack("<HH", 0x0515, 36) + self.version.encode().ljust(16, b"\0")
                       + bytes(20))
        elif msg_id == 0x0730:
            slot = d[0]
            if slot >= 48:
                st, hdr = 1, bytes(64)
            else:
                hdr = bytes(self.flash[self.base(slot):self.base(slot) + 64])
                st = 0 if struct.unpack_from("<I", hdr)[0] == uvterm.APP_MAGIC else 2
            self.reply(struct.pack("<HHBB", 0x0731, 66, slot, st) + hdr)
        elif msg_id == 0x0732:
            slot = d[0]
            ts = struct.unpack_from("<I", d, 2)[0]
            if ts != self.ts:
                st = 8
            elif slot >= 48:
                st = 1
            else:
                b = self.base(slot)
                keep = bytes(self.flash[b + 0x40:b + 0x60])
                if keep[0x10] == 0xFF and self.validate(slot) == 0:
                    keep = keep[:0x10] + bytes(self.flash[b + 20:b + 36])   # header name
                self.flash[b:b + SLOT_STRIDE] = b"\xFF" * SLOT_STRIDE
                if keep[0x10] != 0xFF:
                    self.flash[b + 0x40:b + 0x60] = keep
                self.erases += 1
                st = 0
            self.reply(struct.pack("<HHBB", 0x0733, 2, slot, st))
        elif msg_id == 0x0734:
            slot = d[0]
            off, n, ts = struct.unpack_from("<IHI", d, 2)
            if ts != self.ts:
                st = 8
            elif n > len(d) - 12:
                st = 5
            elif slot >= 48:
                st = 1
            elif off > SLOT_STRIDE or n > SLOT_STRIDE - off:
                st = 5
            else:
                b = self.base(slot) + off
                for i in range(n):                       # NOR programming: 1 -> 0 only
                    self.flash[b + i] &= d[12 + i]
                self.writes += 1
                st = 0
            self.reply(struct.pack("<HHBB", 0x0735, 2, slot, st))
        elif msg_id == 0x0736:
            slot = d[0]
            self.reply(struct.pack("<HHBB", 0x0737, 2, slot, self.validate(slot)))


FAILS = []


def check(name, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + name + ("" if cond else f"  -> {detail}"))
    if not cond:
        FAILS.append(name)


def make_app(name, ver="1.0", code=b"\x00\xbf" * 600, assets=b"", caps=0x40, api_min=3):
    hdr = struct.pack("<4sHBBIIHH16s16sIIHH", b"FAP1", 1, 1, api_min, len(code),
                      zlib.crc32(code) & 0xFFFFFFFF, 0, 1, name.encode().ljust(16, b"\0"),
                      ver.encode().ljust(16, b"\0"), 0x20000280, caps, len(assets),
                      (zlib.crc32(assets) & 0xFFFF) if assets else 0)
    return hdr, code, assets


def write_app(path, parts):
    with open(path, "wb") as f:
        f.write(b"".join(parts))


def main():
    print("framing")
    pkt = uvterm.make_packet(0x0730, bytes([5, 0]))
    check("packet starts AB CD, ends DC BA", pkt[:2] == b"\xAB\xCD" and pkt[-2:] == b"\xDC\xBA", pkt)
    check("CRC-16/XMODEM check value", uvterm.crc16_xmodem(b"123456789") == 0x31C3)
    r = FakeRadio()
    r.noise = b"\x00\xAB\x12K5V junk \xAB"
    link = uvterm.Link(r)
    check("hello: firmware version", link.hello() == "v6.3.0 Labs", link.version)
    check("replies found among other bytes", link.slot_info(0)[0] == 2)

    print("install")
    out = tempfile.mkdtemp(prefix="uvterm-test-")
    app = make_app("USB Term", assets=b"assets!" * 50)
    path = os.path.join(out, "USBTerm.app")
    write_app(path, app)
    header, h, code, assets = uvterm.load_app(path)
    check("load_app reads the blob", h["name"] == "USB Term" and code == app[1] and assets == app[2])

    r = FakeRadio()
    link = uvterm.Link(r)
    link.hello()
    slots = uvterm.read_slots(link, progress=False)
    slot = uvterm.choose_slot(slots, h["name"], None, False)
    check("empty radio: slot 0", slot == 0, slot)
    st = uvterm.install(link, slot, header, code, assets)
    b = r.base(0)
    check("validate OK", st == 0, st)
    check("header at the slot start", r.flash[b:b + 64] == header)
    check("assets at +0x100", r.flash[b + 0x100:b + 0x100 + len(assets)] == assets)
    check("code at +0x1000", r.flash[b + 0x1000:b + 0x1000 + len(code)] == code)
    check("nothing else written", r.flash[b + 0x40:b + 0x100] == b"\xFF" * 0xC0)

    # the app saved settings; an update keeps the slot and the settings
    r.flash[b + 0x40:b + 0x43] = b"T\x02\x00"
    r.flash[b + 0x50:b + 0x60] = b"USB Term".ljust(16, b"\0")
    app2 = make_app("USB Term", ver="1.1", code=b"\x01\xbf" * 700)
    write_app(path, app2)
    header2, h2, code2, assets2 = uvterm.load_app(path)
    slots = uvterm.read_slots(link, progress=False)
    slot = uvterm.choose_slot(slots, h2["name"], None, False)
    st = uvterm.install(link, slot, header2, code2, assets2)
    check("update: same slot", slot == 0 and st == 0, (slot, st))
    check("update: settings kept", r.flash[b + 0x40:b + 0x43] == b"T\x02\x00")
    check("update: new code", r.flash[b + 0x1000:b + 0x1000 + len(code2)] == code2)

    other = make_app("Tetris", caps=0)
    write_app(path, other)
    header3, h3, code3, assets3 = uvterm.load_app(path)
    slots = uvterm.read_slots(link, progress=False)
    slot = uvterm.choose_slot(slots, h3["name"], None, False)
    st = uvterm.install(link, slot, header3, code3, assets3)
    check("another app: first free slot", slot == 1 and st == 0, (slot, st))

    r2 = FakeRadio(caps=0x01)                          # a build without serial
    link2 = uvterm.Link(r2)
    link2.hello()
    st = uvterm.install(link2, 3, header, code, assets)
    check("firmware without the serial capability refuses it (CAP)", st == 9, st)

    link.timestamp ^= 1                                 # a stale session
    try:
        uvterm.install(link, 5, header, code, assets)
        check("wrong timestamp refused", False)
    except uvterm.ProtocolError as e:
        check("wrong timestamp refused (AUTH)", "AUTH" in str(e), e)

    print("command line")
    real_open = uvterm.open_port
    radio = FakeRadio()
    uvterm.open_port = lambda name: radio
    try:
        write_app(path, app)
        buf = io.StringIO()
        with redirect_stdout(buf):
            uvterm.main(["-p", "fake", "install", path])
        check("uvterm install", "slot 0" in buf.getvalue() and radio.validate(0) == 0, buf.getvalue())
        buf = io.StringIO()
        with redirect_stdout(buf):
            uvterm.main(["apps", "-p", "fake"])
        check("uvterm apps lists it", "USB Term" in buf.getvalue() and "serial" in buf.getvalue()
              and "1 uygulama" in buf.getvalue(), buf.getvalue())
        bad = bytearray(app[0] + app[1] + app[2])
        bad[100] ^= 0xFF
        write_app(path, [bytes(bad)])
        try:
            with redirect_stdout(io.StringIO()):
                uvterm.main(["-p", "fake", "install", path])
            check("corrupt .app refused", False)
        except SystemExit as e:
            check("corrupt .app refused before touching the radio", e.code == 1 and radio.erases == 1,
                  (e.code, radio.erases))
    finally:
        uvterm.open_port = real_open

    for real in ("archive/apps/v6.3.0/KISSTNC.app", "App/apps/usbterm/prebuilt/USBTerm.app"):
        p = os.path.join(ROOT, real)
        if os.path.exists(p):
            header, h, code, assets = uvterm.load_app(p)
            r = FakeRadio()
            link = uvterm.Link(r)
            link.hello()
            st = uvterm.install(link, 7, header, code, assets)
            check(f"real blob {os.path.basename(p)} installs and validates", st == 0, st)

    print("chat helpers")
    check("banner", uvterm.classify("# USB Term 1.0 ready - /help")[0] == "banner")
    check("RF Mesaj banner", uvterm.classify("# RF Mesaj 1.0 ready - TA2AAA")[0] == "banner")
    check("handshake ack", uvterm.classify("# echo off")[0] == "ack")
    check("info line", uvterm.classify("# RX 145.50000 MHz  -97 dBm") == ("info", "RX 145.50000 MHz  -97 dBm"))
    check("our echoed handshake ignored", uvterm.classify("/echo off")[0] == "echo")
    check("radio message", uvterm.classify("selam") == ("msg", "selam"))
    check("line encoding: UTF-8 + CR LF", uvterm.encode_line("ğ") == b"\xc4\x9f\r\n")

    class Sink:
        def __init__(self):
            self.chunks = []

        def write(self, d):
            self.chunks.append(bytes(d))

        def flush(self):
            pass
    s = Sink()
    uvterm.paced_write(s, b"x" * 70, gap=0)
    check("paced writes of 32 bytes", [len(c) for c in s.chunks] == [32, 32, 6], s.chunks)

    if FAILS:
        sys.exit(f"{len(FAILS)} check(s) failed")
    print("all checks passed")


if __name__ == "__main__":
    main()
