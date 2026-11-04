#!/usr/bin/env python3
# rfkopru tests without a radio or the internet: text conversion, the
# Telegram bridge against a fake Bot API, the "!command" answers, and an
# end-to-end run against the RF Mesaj app itself (App/apps/rfmesaj, built for
# the computer, live on a pseudo-terminal).
#
#   python3 tools/rfmesaj/test_rfkopru.py
import io, json, os, stat, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import rfkopru  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + name + ("" if cond else f"  -> {detail}"))
    if not cond:
        FAILS.append(name)


class FakeRadio:
    def __init__(self):
        self.sent = []

    def send(self, text):
        self.sent.append(text)
        return rfkopru.chunks(text)


class FakeHTTP:
    """urlopen stand-in: records requests, answers from a queue."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.requests = []

    def __call__(self, req, timeout=0):
        self.requests.append((req.full_url, json.loads(req.data.decode())))
        body = json.dumps(self.replies.pop(0) if self.replies else {"ok": True, "result": []}).encode()

        class R(io.BytesIO):
            def __enter__(s):
                return s

            def __exit__(s, *a):
                return False
        return R(body)


def main():
    print("text")
    check("Turkish letters to ASCII", rfkopru.ascii_tr("Çağrı İşareti: ŞÜÖ ğüş") == "Cagri Isareti: SUO gus")
    check("other characters: accents dropped, the rest '?'", rfkopru.ascii_tr("café 😀") == "cafe ?")
    long = "Bolu Abant golu kiyisinda kamp kuruyoruz yarin sabah saat yedide yola cikacagiz"
    parts = rfkopru.chunks(long)
    check("long text cut at spaces into 48-character messages",
          all(len(p) <= 48 for p in parts) and " ".join(parts) == long and len(parts) == 2, parts)
    check("radio lines parsed", rfkopru.parse("TA2AAA> selam") == ("msg", "TA2AAA", ">", "selam")
          and rfkopru.parse("TA2AAA* gizli") == ("msg", "TA2AAA", "*", "gizli")
          and rfkopru.parse("# + aldi: TA2BBB") == ("status", "+ aldi: TA2BBB")
          and rfkopru.parse("> kendi mesajim") is None)

    print("Telegram bridge")
    http = FakeHTTP([{"ok": True, "result": {}}])
    tg = rfkopru.Telegram("TOKEN", opener=http)
    radio = FakeRadio()
    br = rfkopru.Bridge(tg, "4242", lambda cb: radio)
    out = io.StringIO()
    sys.stdout, real = out, sys.stdout
    try:
        br.from_radio("TA2AAA> Abant'a vardik")
    finally:
        sys.stdout = real
    url, body = http.requests[-1]
    check("a radio message goes to the chat", url.endswith("/botTOKEN/sendMessage")
          and body == {"chat_id": 4242, "text": "📻 TA2AAA: Abant'a vardik"}, (url, body))
    http.replies = [{"ok": True, "result": {}}] * 3
    sys.stdout = io.StringIO()
    try:
        br.from_radio("TA2AAA* sifreli")
        br.from_radio("# + aldi: TA2BBB")
        br.from_radio("# x iletilemedi")
    finally:
        sys.stdout = real
    texts = [b["text"] for _, b in http.requests[-3:]]
    check("encrypted marked, delivery and failure reported",
          texts == ["📻 TA2AAA 🔒: sifreli", "✅ telsizde alindi: TA2BBB", "❌ iletilemedi"], texts)
    http.replies = [{"ok": True, "result": [
        {"update_id": 10, "message": {"chat": {"id": 4242}, "from": {"first_name": "Şükrü"},
                                      "text": "Yemek hazır, dönün!"}},
        {"update_id": 11, "message": {"chat": {"id": 999}, "from": {"first_name": "X"}, "text": "hack"}},
    ]}]
    br.poll_once(wait=1)
    check("the chat's message goes on the air, sender's name first, ASCII",
          radio.sent == ["Sukru: Yemek hazir, donun!"] or radio.sent == ["Sukru: Yemek hazır, dönün!"], radio.sent)
    check("other chats cannot transmit", len(radio.sent) == 1, radio.sent)
    check("updates acknowledged (offset)", tg.offset == 12, tg.offset)
    check("getUpdates long polling", http.requests[-1][0].endswith("/getUpdates")
          and http.requests[-1][1] == {"offset": 0, "timeout": 1}, http.requests[-1])

    print("automatic answers")
    check("!saat", (rfkopru.answer("!saat", "TA2BBB") or "").startswith("Saat "))
    check("!ping answers the sender", rfkopru.answer("!ping", "TA2BBB") == "pong TA2BBB")
    check("!yardim", "!hava" in rfkopru.answer("!yardim", "X"))
    check("not a command: no answer", rfkopru.answer("selam", "X") is None
          and rfkopru.answer("!bilinmeyen", "X") is None)
    d = tempfile.mkdtemp()
    s = os.path.join(d, "betik.sh")
    with open(s, "w") as f:
        f.write('#!/bin/sh\nif [ "$1" = "isik" ]; then echo "Isik $2 yapildi ($3)"; fi\n')
    os.chmod(s, os.stat(s).st_mode | stat.S_IEXEC)
    check("your own script: first output line is the answer",
          rfkopru.answer("!isik ac", "TA2BBB", s) == "Isik ac yapildi (TA2BBB)")
    check("the script does not know it: the built-ins", rfkopru.answer("!ping", "TA2BBB", s) == "pong TA2BBB")

    e2e()
    if FAILS:
        sys.exit(f"{len(FAILS)} check(s) failed")
    print("all checks passed")


def e2e():
    """rfkopru's Radio class against the RF Mesaj app over a pty."""
    print("end to end: rfkopru <-> RF Mesaj (live, pty)")
    try:
        import pty, tty
        import serial  # noqa: F401
    except ImportError:
        print("  (pyserial or pty missing: skipped)")
        return
    apps = os.path.join(ROOT, "App", "apps")
    sys.path.insert(0, apps)
    import host_test as ht
    app = os.path.join(apps, "rfmesaj")
    ht.build(app, "rfmesaj")
    # a packet from TA2BBB, made by the app itself
    other = ht.Run(app, "rfmesaj", ht.script("call TA2BBB", "host 1", "wait 50", "rx /key ortak\\r",
                                             "wait 50", "rx Abant'tayiz, gel\\r", "wait 500"))
    air = [l[4:] for l in other.lines if l.startswith("AIR ")][0]
    master, slave = pty.openpty()
    tty.setraw(slave)
    radio = ht.script("host 1", "wait 1500", f"air {air}", "wait 2500", "state")
    p = subprocess.Popen([os.path.join(app, "test", "out", "host_rfmesaj"),
                          os.path.join(app, "rfmesaj_assets.bin")],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, cwd=app,
                         env=dict(os.environ, LIVE_FD=str(master)), pass_fds=(master,))
    p.stdin.write(radio)
    p.stdin.close()
    import uvterm
    ser = uvterm.serial.Serial(os.ttyname(slave), 115200, timeout=0.05)
    got = []
    r = rfkopru.Radio(ser, got.append, key="ortak")
    r.start()
    time.sleep(0.4)
    r.send("Çay hazır mı?")
    out = p.communicate(timeout=30)[0]
    r.close()
    ser.close()
    os.close(master)
    os.close(slave)
    airs = [l[4:] for l in out.splitlines() if l.startswith("AIR ")]
    texts = [bytes.fromhex(a)[16:64].rstrip(b"\0") for a in airs]
    check("the computer's line went on the air, in ASCII", b"Cay hazir mi?" in texts, texts)
    check("key set over USB: the other radio's message verified ('>')",
          "TA2BBB> Abant'tayiz, gel" in got, got)
    check("and acknowledged over the air", any(bytes.fromhex(a)[2] == 2 for a in airs), airs)


if __name__ == "__main__":
    main()
