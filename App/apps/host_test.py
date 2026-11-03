#!/usr/bin/env python3
# Shared helpers for the host tests of overlay apps that use host_mock.h:
# build the app's assets and its host harness, run scripts, parse the output,
# count checks and render the LCD mockups.
#
#   sys.path.insert(0, <App/apps>); import host_test as ht
#   ht.build(app_dir, "usbterm")            # assets + test/out/host_<name>
#   r = ht.Run(app_dir, "usbterm", ht.script("host 1", "wait 50", "state"))
#   ht.check("name", condition, detail)
#   ht.png(app_dir, "shot-name")            # test/out/<shot>.raw -> .png
import os, re, subprocess, sys

APPS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(APPS, "..", ".."))
FAILS = []


def app_version(app_dir):
    """APP_VER from the app's build.sh: the tests expect what the build packs."""
    m = re.search(r'^APP_VER="([^"]+)"', open(os.path.join(app_dir, "build.sh")).read(), re.M)
    return m.group(1)


def build(app_dir, name):
    out = os.path.join(app_dir, "test", "out")
    os.makedirs(out, exist_ok=True)
    env = dict(os.environ, APP_VER=app_version(app_dir))
    subprocess.check_call([sys.executable, os.path.join(app_dir, "gen_assets.py"),
                           os.path.join(app_dir, f"{name}_assets.bin"),
                           os.path.join(app_dir, f"{name}_assets.h")], env=env)
    subprocess.check_call(["cc", "-std=gnu11", "-O1", "-g", "-Wall", "-Wextra", "-Werror",
                           "-Wno-unused-function", "-DENABLE_SMALL_BOLD",
                           "-I", os.path.join(ROOT, "App"),
                           "-o", os.path.join(out, f"host_{name}"),
                           os.path.join(app_dir, "test", f"host_{name}.c"),
                           os.path.join(ROOT, "App", "font.c")], cwd=app_dir)


class Run:
    """One harness run: tx bytes, tones, STATE dicts (key=value, key=[text]),
    ROW lists, saved config, whether the script ran out (ended)."""

    def __init__(self, app_dir, name, script, cfg=None, seed=None, env=None):
        args = [os.path.join(app_dir, "test", "out", f"host_{name}"),
                os.path.join(app_dir, f"{name}_assets.bin")] + ([cfg] if cfg else [])
        e = dict(os.environ, **(env or {}))
        if seed is not None:
            e["SEED"] = str(seed)
        p = subprocess.run(args, input=script, capture_output=True, text=True, cwd=app_dir, env=e)
        if p.returncode:
            sys.exit(f"host_{name} failed: {p.stderr}")
        self.lines = p.stdout.splitlines()
        self.parse()

    def parse(self):
        self.tx = b"".join(bytes.fromhex(l[3:]) for l in self.lines if l.startswith("TX "))
        self.tones = [tuple(map(int, l.split()[1:])) for l in self.lines if l.startswith("TONE ")]
        self.states = []
        cur = None
        for l in self.lines:
            if l.startswith("STATE "):
                cur = {}
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
        self.shots = [l.split()[1] for l in self.lines if l.startswith("SHOT ")]

    @property
    def last(self):
        return self.states[-1]


def script(*cmds):
    return "\n".join(cmds) + "\n"


def press(*keys):
    return [f"press {k}" for k in keys]


def check(name, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + name + ("" if cond else f"  -> {detail}"))
    if not cond:
        FAILS.append(name)


def png(app_dir, shot, scale=4):
    """test/out/<shot>.raw (status line + 7 frame lines) -> <shot>.png, LCD colours."""
    try:
        from PIL import Image
    except ImportError:
        return None
    out = os.path.join(app_dir, "test", "out")
    raw = open(os.path.join(out, shot + ".raw"), "rb").read()
    img = Image.new("RGB", (128, 64), (196, 214, 170))
    for page in range(8):
        for x in range(128):
            b = raw[page * 128 + x]
            for bit in range(8):
                if b >> bit & 1:
                    img.putpixel((x, page * 8 + bit), (32, 40, 32))
    path = os.path.join(out, shot + ".png")
    img.resize((128 * scale, 64 * scale), Image.NEAREST).save(path)
    return path


def screen_text(app_dir, shot):
    """True when the frame (below the status line) is not blank."""
    raw = open(os.path.join(app_dir, "test", "out", shot + ".raw"), "rb").read()
    return any(raw[128:])


def finish():
    if FAILS:
        sys.exit(f"{len(FAILS)} check(s) failed")
    print("all checks passed")
