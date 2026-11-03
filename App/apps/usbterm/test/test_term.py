#!/usr/bin/env python3
# USB Term host tests: the app built for the computer against the mock API of
# App/apps/host_mock.h (the firmware's own fonts), driven by scripts. Checks
# the serial protocol (banner, echo, commands, line ends, UTF-8), the keypad
# (multi-tap, long press, modes, EXIT), the history and the two-line keypad
# area, runs the app against uvterm.py over a pty, and renders LCD mockups
# into test/out/*.png.
#
#   python3 App/apps/usbterm/test/test_term.py
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
sys.path.insert(0, os.path.dirname(APP))
import host_test as ht  # noqa: E402
from host_test import check, press, script  # noqa: E402

ROOT = ht.ROOT
OUT = os.path.join(HERE, "out")
VER = ht.app_version(APP).encode()


def Run(s, cfg=None):
    return ht.Run(APP, "usbterm", s, cfg=cfg)


def raw(shot):
    return open(os.path.join(OUT, shot + ".raw"), "rb").read()


def fbline(shot, line):
    """Frame line 0-6 of a shot (128 bytes)."""
    return raw(shot)[128 * (line + 1):128 * (line + 2)]


# ---------------------------------------------------------------------------
def tests():
    print("serial: connection, echo, line ends")
    r = Run(script("wait 50", "host 1", "wait 50", "rx Merhaba\\r\\n", "wait 50", "state"))
    check("banner on connection", r.tx.startswith(b"# USB Term " + VER + b" ready - /help\r\n"), r.tx)
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
    check("/info", info == b"# USB Term " + VER + b" / F4HWN Labs v6.3.0\r\n"
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
                   "state", "down UP", "wait 3000", "up", "wait 50", "state"))
    check("UP / DOWN scroll the history", r.states[0]["scroll"] == 2, r.states[0])
    check("UP held repeats, stops at the oldest row (20 rows, 6 on screen)",
          r.states[1]["scroll"] == 14, r.states[1])

    r = Run(script("host 1", "wait 50", "rx " + rows + "/pi", "wait 100", "down UP", "wait 2500", "up",
                   "wait 50", "state", "rx ng\\r", "wait 100", "state", "shot clamp"))
    check("scrolled to the top with an unfinished line", r.states[0]["scroll"] == 15, r.states[0])
    check("that line ends as a command: scroll pulled back in, rows still drawn",
          r.states[1]["scroll"] == 14 and ht.screen_text(APP, "clamp"),
          r.states[1])

    r = Run(script("host 1", "wait 50", "rx " + "".join(f"r{i}\\r" for i in range(40)), "wait 100", "state"))
    check("32-row scrollback keeps the newest rows",
          r.last["rows_n"] == 32 and r.last["rows"][0] == "r8" and r.last["rows"][-1] == "r39", r.last)

    print("keypad area (v2: 6x7 font, two lines of 18)")
    num = ["press STAR", "press STAR"]           # 123 mode: one press, one digit
    r = Run(script("host 1", "wait 50", *num, *press(*"12345"), "wait 50", "shot in5",
                   *press(*"6789012345678901"), "wait 50", "shot in21",
                   *press(*"2345678901234567890"), "wait 50", "shot in40", "state"))
    l5, l6 = fbline("in5", 5), fbline("in5", 6)
    check("5 characters: first keypad line only", any(l5) and not any(l6))
    check("block cursor after them (x 35..41)", all(b & 0x7F == 0x7F for b in l5[35:42]), l5[35:42].hex())
    check("21 characters: the second line in use", any(fbline("in21", 6)))
    l6 = fbline("in40", 6)
    check("40 characters: text moved up a line, cursor on line 2, column 4",
          r.last["in"] == "1234567890123456789012345678901234567890"
          and all(b & 0x7F == 0x7F for b in l6[28:35]) and not any(l6[36:]), l6.hex())
    Run(script("host 1", "wait 50", *num, *press(*"901234567890123456"), "wait 50", "shot in18"))
    check("40 characters: line 1 shows characters 19-36, as typed alone",
          fbline("in40", 5) == fbline("in18", 5) and any(fbline("in18", 5)))

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
    p = subprocess.Popen([os.path.join(OUT, "host_usbterm"), os.path.join(APP, "usbterm_assets.bin")],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
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
        *press(2), "wait 1000", *press(6), "wait 1000", *press(0), "wait 1000",
        *press(8), "wait 1000", *press(3, 3), "wait 1000", *press(5, 5, 5), "wait 1000",
        *press(7, 7, 7, 7), "wait 1000", *press(4, 4, 4), "wait 1000", *press(9, 9, 9, 9), "wait 50",
        "shot chat",
    )
    for shot in Run(s).shots:
        path = ht.png(APP, shot)
        if path:
            print(f"  mockup {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    ht.build(APP, "usbterm")
    tests()
    e2e()
    mockups()
    ht.finish()
