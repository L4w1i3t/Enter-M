"""Flip ENTER-M's release toggles: the ENTER_M_SHIP_* defines in game/options.rpy.

    python dev/release_toggles.py            show every toggle and its state
    python dev/release_toggles.py on         switch every toggle back on
    python dev/release_toggles.py off        switch every toggle off (the Oct 14 2026 demo state)
    python dev/release_toggles.py op on      switch one toggle (its name without ENTER_M_SHIP_)

A toggle that is off also keeps its files out of the built package (see the
build excludes in options.rpy), so flip it before you build, not after. A
running game picks the change up on its next reload.
"""
import pathlib
import re
import sys

OPTIONS = pathlib.Path(__file__).resolve().parent.parent / "game" / "options.rpy"
TOGGLE = re.compile(r"^(define -100 ENTER_M_SHIP_(\w+) = )(True|False)\b", re.M)


def states(text):
    return {m.group(2).lower(): m.group(3) == "True" for m in TOGGLE.finditer(text)}


def main(args):
    text = OPTIONS.read_bytes().decode("utf-8")
    current = states(text)
    if not current:
        sys.exit("No ENTER_M_SHIP_* toggles found in %s" % OPTIONS)
    if not args:
        for name, on in sorted(current.items()):
            print("%-10s %s" % (name, "on" if on else "off"))
        return

    *names, value = [a.lower() for a in args]
    if value not in ("on", "off"):
        sys.exit(__doc__)
    names = names or list(current)
    unknown = [n for n in names if n not in current]
    if unknown:
        sys.exit("Unknown toggle: %s. Known: %s" % (", ".join(unknown), ", ".join(sorted(current))))

    want = "True" if value == "on" else "False"
    flip = lambda m: m.group(1) + want if m.group(2).lower() in names else m.group(0)
    # Bytes in, bytes out: the file's own line endings survive untouched.
    OPTIONS.write_bytes(TOGGLE.sub(flip, text).encode("utf-8"))

    after = states(OPTIONS.read_bytes().decode("utf-8"))
    assert all(after[n] == (value == "on") for n in names), after  # the write took
    for name in sorted(names):
        print("%-10s %s" % (name, value))


if __name__ == "__main__":
    main(sys.argv[1:])
