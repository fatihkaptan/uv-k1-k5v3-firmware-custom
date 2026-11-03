#!/usr/bin/env python3
# USB Term host tests: the app built for the computer against a mock API
# (test/host_term.c), driven by scripts. Checks the serial protocol (banner,
# echo, commands, line ends, UTF-8), the keypad (multi-tap, long press, modes,
# EXIT) and the history, and renders LCD mockups into test/out/*.png.
#
#   python3 App/apps/usbterm/test/test_term.py
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(APP, "..", "..", ".."))
OUT = os.path.join(HERE, "out")
BIN = os.path.join(OUT, "host_term")
ASSETS = os.path.join(APP, "usbterm_assets.bin")

def build():
    os.makedirs(OUT, exist_ok=True)
    # The 3x5 font, straight from the firmware source.
    src = open(os.path.join(ROOT, "App", "font.c"), encoding="utf-8").read()
    body = src[src.index("gFont3x5[][3]"):]
    body = body[body.index("{") + 1:]
    rows = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("};"):
            break
        m = re.match(r"\{\s*(0x[0-9a-fA-F]+),\s*(0x[0-9a-fA-F]+),\s*(0x[0-9a-fA-F]+)\s*\}", s)
        if m:
            rows.append(m.groups())
    assert len(rows) >= 95, len(rows)
    with open(os.path.join(OUT, "font3x5.h"), "w") as f:
        f.write("static const uint8_t gFont3x5[][3] = {\n")
        f.write("".join(f"    {{{a}, {b}, {c}}},\n" for a, b, c in rows))
        f.write("};\n")
    env = dict(os.environ, APP_VER=os.environ.get("APP_VER", "1.0"))
    subprocess.check_call([sys.executable, os.path.join(APP, "gen_assets.py"),
                           ASSETS, os.path.join(APP, "usbterm_assets.h")], env=env)
    subprocess.check_call(["cc", "-std=gnu11", "-O1", "-g", "-Wall", "-Wextra", "-Werror",
                           "-Wno-unused-function", "-I", OUT, "-o", BIN,
                           os.path.join(HERE, "host_term.c")], cwd=APP)

class Run:
    def __init__(self, script, cfg=None):
        args = [BIN, ASSETS] + ([cfg] if cfg else [])
        p = subprocess.run(args, input=script, capture_output=True, text=True, cwd=APP)
        if p.returncode:
            sys.exit(f"host_term failed: {p.stderr}")
        self.lines = p.stdout.splitlines()
        self.tx = b"".join(bytes.fromhex(l[3:]) for l in self.lines if l.startswith("TX "))
        self.tones = [tuple(map(int, l.split()[1:])) for l in self.lines if l.startswith("TONE ")]
        self.states = []
        cur = None
        for l in self.lines:
            if l.startswith("STATE "):
                cur = {"rows": []}
                for m in re.finditer(r"(\w+)=(\[[^\]]*\]|\S+)", l[6:]):
                    k, v = m.groups()
                    cur[k] = v[1:-1] if v.startswith("[") else int(v)
                cur["rows_n"] = cur.pop("rows", None)
                cur["rows"] = []
                self.states.append(cur)
            elif l.startswith("ROW ") and cur is not None:
                cur["rows"].append(l[5:-1])
        self.cfg = next((bytes.fromhex(l[4:]) for l in self.lines if l.startswith("CFG ")), None)
        self.ended = "END" in self.lines        # False: the app quit by itself
    @property
    def last(self):
        return self.states[-1]

def script(*cmds):
    return "\n".join(cmds) + "\n"

FAILS = []
def check(name, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + name + ("" if cond else f"  -> {detail}"))
    if not cond:
        FAILS.append(name)

def press(*keys):
    return [f"press {k}" for k in keys]

# ---------------------------------------------------------------------------
def tests():
    print("serial: connection, echo, line ends")
    r = Run(script("wait 50", "host 1", "wait 50", "rx Merhaba\\r\\n", "wait 50", "state"))
    check("banner on connection", r.tx.startswith(b"# USB Term 1.0 ready - /help\r\n"), r.tx)
    check("echo of the received line", b"Merhaba\r\n" in r.tx, r.tx)
    check("line shown", r.last["rows"] == ["Merhaba"], r.last)
    check("notification tone", (1200, 40) in r.tones, r.tones)

    r = Run(script("host 1", "wait 50", "rx a\\rb\\nc\\r\\nd\\n\\n", "wait 50", "state"))
    check("CR, LF and CR LF each end one line; empty lines skipped",
          r.last["rows"] == ["a", "b", "c", "d"], r.last)

    r = Run(script("host 1", "wait 50", "rx abc\\x08d\\x7fe\\r", "wait 50", "state"))
    check("backspace and DEL delete", r.last["rows"] == ["abe"], r.last)
    check("backspace echoed as BS SP BS", b"\x08 \x08" in r.tx, r.tx)

    r = Run(script("host 1", "wait 50", "rx x\\x1b[Ay\\x1bOBz\\x1b[1;5Cw\\r", "wait 50", "state"))
    check("ANSI escape sequences skipped", r.last["rows"] == ["xyzw"], r.last)

    tr = "Çalışıyor şüphesiz ĞÜÖİ é€".encode("utf-8")
    r = Run(script("host 1", "wait 50", "rx " + "".join(f"\\x{b:02x}" for b in tr) + "\\r",
                   "wait 50", "state"))
    check("UTF-8 Turkish letters shown in ASCII", r.last["rows"] == ["Calisiyor suphesiz GUOI e?"], r.last)
    check("UTF-8 echoed unchanged", tr in r.tx, r.tx)

    r = Run(script("host 1", "wait 50", "rx " + "x" * 40 + "\\r", "wait 50", "state"))
    check("long line wrapped at 32 columns", r.last["rows"] == ["x" * 32, "x" * 8], r.last)

    r = Run(script("host 1", "wait 50", "rx partial", "wait 50", "state"))
    check("unfinished line kept apart", r.last["rx"] == "partial" and r.last["rows"] == [], r.last)

    print("commands")
    r = Run(script("host 1", "wait 50", "rx /echo off\\r\\n", "wait 50", "rx hello\\r\\n",
                   "wait 50", "state"))
    check("/echo off answered", b"# echo off\r\n" in r.tx, r.tx)
    check("no echo after /echo off", r.tx.endswith(b"# echo off\r\n"), r.tx)
    check("command not shown", r.last["rows"] == ["hello"] and r.last["echo"] == 0, r.last)

    r = Run(script("host 1", "wait 50", "rx /PING\\r", "wait 50", "rx /Beep\\r", "wait 50",
                   "rx /help\\r", "wait 50", "rx /foo\\r", "wait 50", "state"))
    check("/ping -> # pong (any case)", b"# pong\r\n" in r.tx, r.tx)
    check("/beep answers and beeps", b"# beep\r\n" in r.tx and r.tones.count((1200, 40)) >= 2, r.tones)
    check("/help lists the commands", b"# /info /ping /beep /clear\r\n# /echo on  /echo off\r\n" in r.tx, r.tx)
    check("unknown /foo shown as text", r.last["rows"] == ["/foo"], r.last)

    r = Run(script("host 1", "wait 50", "lost", "wait 50", "rx /echo off\\r", "wait 50",
                   "rx /info\\r", "wait 50"))
    info = r.tx.split(b"# echo off\r\n", 1)[1]
    check("/info", info == b"# USB Term 1.0 / F4HWN Labs v6.3.0\r\n"
                           b"# RX 145.50000 MHz  -97 dBm\r\n"
                           b"# BAT 7.85 V  lost 1\r\n", info)

    r = Run(script("host 1", "wait 50", "rx one\\rtwo\\r", "wait 50", "rx /clear\\r", "wait 50", "state"))
    check("/clear empties the history", r.last["rows"] == [] and b"# clear\r\n" in r.tx, r.last)

    r = Run(script("host 1", "wait 50", "rx /echo off\\r", "wait 50", "host 0", "wait 600",
                   "host 1", "wait 50", "state"))
    check("a new connection turns echo back on, with a new banner",
          r.last["echo"] == 1 and r.tx.count(b"ready - /help") == 2, r.tx)

    print("keypad")
    r = Run(script("host 1", "wait 50", *press(4, 4), "wait 1000", *press(4, 4, 4), "wait 1000",
                   "state", "press MENU", "wait 50", "state"))
    check("multi-tap: 4 4, pause, 4 4 4 -> hi", r.states[0]["in"] == "hi", r.states[0])
    check("MENU sends the line with CR LF", r.tx.endswith(b"hi\r\n"), r.tx)
    check("sent line shown as '> hi', input cleared",
          r.states[1]["rows"] == ["> hi"] and r.states[1]["in"] == "", r.states[1])

    r = Run(script("host 1", "wait 50", *press(7, 7, 7, 7, 7), "wait 1000", *press(0), "wait 1000",
                   *press(1), "wait 1000", "state"))
    check("7 pressed 5 times: p q r s -> 7", r.last["in"].startswith("7"), r.last)
    check("0 types a space, 1 a period", r.last["in"] == "7 .", r.last)

    r = Run(script("host 1", "wait 50", "down 5", "wait 800", "up", "wait 100", "state"))
    check("long press types the digit", r.last["in"] == "5" and r.last["tap"] == 0, r.last)

    r = Run(script("host 1", "wait 50", *press("STAR"), *press(2), "wait 1000", *press("STAR"),
                   *press(2), *press(2), "wait 50", "state", "press STAR", "wait 50", "state"))
    check("* -> ABC, * -> 123", r.states[0]["in"] == "A22" and r.states[0]["mode"] == 2, r.states[0])
    check("* wraps back to abc", r.states[1]["mode"] == 0, r.states[1])

    r = Run(script("host 1", "wait 50", *press(2), "wait 1000", *press(3), "wait 1000",
                   "press EXIT", "wait 50", "state", "down EXIT", "wait 900", "up", "wait 50", "state",
                   "press EXIT", "wait 50", "rx never\\r", "wait 50", "state"))
    check("EXIT deletes one character", r.states[0]["in"] == "a", r.states[0])
    check("EXIT held clears the line", r.states[1]["in"] == "" and r.ended is False, r.states[1])
    check("EXIT on an empty line quits (saved config)", len(r.states) == 2 and r.cfg == bytes([0x54, 0, 1]), r.cfg)

    r = Run(script("host 0", "wait 50", *press(2), "wait 50", "press MENU", "wait 50", "state"))
    check("no host: error tone, the line is kept", (300, 120) in r.tones and r.last["in"] == "a", r.last)

    r = Run(script("host 1", "wait 50", "rx ab", "wait 50", *press(4, 4), "wait 1000",
                   "press MENU", "wait 50", "state"))
    check("raw terminal mid-line: CR LF, our line, then its partial line again",
          r.tx.endswith(b"ab\r\nh\r\nab"), r.tx)
    check("history: our line, then the partial line still pending",
          r.last["rows"] == ["> h"] and r.last["rx"] == "ab", r.last)

    r = Run(script("host 1", "wait 50", *press(2), "wait 1000",
                   *[x for _ in range(64) for x in ("press 1", "wait 1000")], "state"))
    check("input stops at 64 characters with an error tone",
          len(r.last["in"]) == 64 and (300, 120) in r.tones, (len(r.last["in"]), r.tones[-3:]))

    r = Run(script("host 1", "wait 50", *press("F"), "wait 50", "rx quiet\\r", "wait 50", "state"))
    check("F turns the notification beep off", r.last["sound"] == 0 and (1200, 40) not in r.tones, r.tones)

    rows = "".join(f"line {i}\\r" for i in range(20))
    r = Run(script("host 1", "wait 50", "rx " + rows, "wait 100", *press("UP", "UP", "UP", "DOWN"),
                   "state", "down UP", "wait 2000", "up", "wait 50", "state"))
    check("UP / DOWN scroll the history", r.states[0]["scroll"] == 2, r.states[0])
    check("UP held repeats, stops at the oldest row", r.states[1]["scroll"] == 12, r.states[1])

    r = Run(script("host 1", "wait 50", "rx " + rows + "/pi", "wait 100", "down UP", "wait 2500", "up",
                   "wait 50", "state", "rx ng\\r", "wait 100", "state", "shot clamp"))
    check("scrolled to the top with an unfinished line", r.states[0]["scroll"] == 13, r.states[0])
    check("that line ends as a command: scroll pulled back in, rows still drawn",
          r.states[1]["scroll"] == 12 and any(open(os.path.join(OUT, "clamp.raw"), "rb").read()[128:]),
          r.states[1])

    r = Run(script("host 1", "wait 50", "rx " + "".join(f"r{i}\\r" for i in range(40)), "wait 100", "state"))
    check("32-row scrollback keeps the newest rows",
          r.last["rows_n"] == 32 and r.last["rows"][0] == "r8" and r.last["rows"][-1] == "r39", r.last)

    r = Run(script("wait 50", "state"), cfg="540200")
    check("saved config restored (123, beep off)", r.last["mode"] == 2 and r.last["sound"] == 0, r.last)
    r = Run(script("wait 50", "state"), cfg="ffffff")
    check("erased config -> defaults", r.last["mode"] == 0 and r.last["sound"] == 1, r.last)

# ---------------------------------------------------------------------------
def e2e():
    """The app (live mode) and uvterm.py's chat over a pseudo-terminal pair."""
    print("end to end: uvterm.py <-> USB Term over a pty")
    try:
        import pty, tty
        import serial  # noqa: F401
    except ImportError:
        print("  (pyserial or pty missing: skipped)")
        return
    sys.path.insert(0, os.path.join(ROOT, "tools", "uvterm"))
    import uvterm
    uvterm.USE_COLOR = False
    master, slave = pty.openpty()
    tty.setraw(slave)                # no line discipline echo before pyserial opens it
    radio = script("host 1", "wait 1500", *press(4, 4), "wait 1000", *press(4, 4, 4), "wait 1000",
                   "press MENU", "wait 1500", "state")
    p = subprocess.Popen([BIN, ASSETS], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                         cwd=APP, env=dict(os.environ, LIVE_FD=str(master)), pass_fds=(master,))
    p.stdin.write(radio)
    p.stdin.close()
    ser = uvterm.serial.Serial(os.ttyname(slave), 115200, timeout=0.05)
    shown = []
    chat = uvterm.Chat(ser)
    chat.show = shown.append
    chat.start()
    chat.handshake()
    ready = chat.ready.wait(3)
    chat.send("Merhaba telsiz ÇŞ")
    out = p.communicate(timeout=30)[0]
    chat.close()
    ser.close()
    os.close(master); os.close(slave)
    rows = [l[5:-1] for l in out.splitlines() if l.startswith("ROW ")]
    check("handshake: '/echo off' acknowledged", ready, shown)
    check("computer -> radio: line shown, Turkish letters in ASCII",
          rows == ["Merhaba telsiz CS", "> hi"], rows)
    check("radio -> computer: 'hi' shown as a radio message",
          any(t.endswith("TELSİZ> hi") for t in shown), shown)
    check("no echo of our own line", not any("Merhaba" in t for t in shown), shown)

# ---------------------------------------------------------------------------
def mockups():
    """LCD mockups of a session, for the README (test/out/*.png)."""
    s = script(
        "host 1", "wait 100",
        "rx /echo off\\r", "wait 50",
        "rx Merhaba telsiz!\\r", "wait 100",
        *press(4, 4), "wait 1000", *press(4, 4, 4), "wait 1000", "press MENU", "wait 100",
        "rx Bilgisayardan selamlar :)\\r", "wait 100",
        "rx Frekans: 145.500 MHz\\r", "wait 100",
        *press(7, 7, 7, 7), "wait 1000", *press(3, 3), "wait 1000", *press(5, 5, 5), "wait 1000",
        *press(2), "wait 1000", *press(6), "wait 50",
        "shot chat",
    )
    r = Run(s)
    try:
        from PIL import Image
    except ImportError:
        print("  (PIL missing: no PNG mockups)")
        return
    for name in [l.split()[1] for l in r.lines if l.startswith("SHOT ")]:
        raw = open(os.path.join(OUT, name + ".raw"), "rb").read()
        img = Image.new("RGB", (128, 64), (196, 214, 170))
        for page in range(8):
            for x in range(128):
                b = raw[page * 128 + x]
                for bit in range(8):
                    if b >> bit & 1:
                        img.putpixel((x, page * 8 + bit), (32, 40, 32))
        img = img.resize((128 * 4, 64 * 4), Image.NEAREST)
        path = os.path.join(OUT, name + ".png")
        img.save(path)
        print(f"  mockup {os.path.relpath(path, ROOT)}")

if __name__ == "__main__":
    build()
    tests()
    e2e()
    mockups()
    if FAILS:
        sys.exit(f"{len(FAILS)} check(s) failed")
    print("all checks passed")
