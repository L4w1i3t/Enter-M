"""Every screen NAMED anywhere must actually be DEFINED somewhere.

Ren'Py's lint does not check this: a screen that simply stops existing is a
runtime `Screen <x> is not known.` the first time something tries to show it,
and nothing before that says a word. That is exactly how a bad splice removed
`screen mc_collection` and still linted clean.
"""
import io
import os
import re
import sys

Q = chr(34)
defined = set()
refs = {}

for root, dirs, files in os.walk("game"):
    dirs[:] = [d for d in dirs if d not in ("cache", "saves", "python-packages")]
    for fn in files:
        if not fn.endswith(".rpy"):
            continue
        path = os.path.join(root, fn).replace(os.sep, "/")
        text = io.open(path, encoding="utf-8", errors="replace").read()

        for m in re.finditer(r"^\s*screen\s+([A-Za-z_][A-Za-z_0-9]*)", text, re.M):
            defined.add(m.group(1))

        # Show("x") / Hide("x") / ShowMenu("x") / ShowTransient("x")
        for m in re.finditer(
                r"\b(?:Show|Hide|ShowTransient|ShowMenu)\s*\(\s*" + Q
                + r"([A-Za-z_][A-Za-z_0-9]*)" + Q, text):
            refs.setdefault(m.group(1), set()).add(path)
        # show screen x / hide screen x / call screen x / use x
        for m in re.finditer(
                r"^\s*(?:show|hide|call)\s+screen\s+([A-Za-z_][A-Za-z_0-9]*)",
                text, re.M):
            refs.setdefault(m.group(1), set()).add(path)
        for m in re.finditer(r"^\s*use\s+([A-Za-z_][A-Za-z_0-9]*)", text, re.M):
            refs.setdefault(m.group(1), set()).add(path)
        # renpy.show_screen("x") / renpy.get_screen("x") / hide_screen
        for m in re.finditer(
                r"renpy\.(?:show|hide|get)_screen\s*\(\s*" + Q
                + r"([A-Za-z_][A-Za-z_0-9]*)" + Q, text):
            refs.setdefault(m.group(1), set()).add(path)

# Screens Ren'Py itself ships, plus the menu names ShowMenu takes.
BUILTIN = {
    "say", "choice", "input", "nvl", "main_menu", "navigation", "preferences",
    "save", "load", "file_slots", "quick_menu", "history", "help", "about",
    "keyboard_help", "mouse_help", "gamepad_help", "confirm", "skip_indicator",
    "notify", "nvl_screen", "menu", "yesno_prompt", "context_menu", "bubble",
    "_console", "_console_history", "dismiss", "game_menu", "quit",
    # Developer screens live in the SDK's renpy/common/_developer, which is not
    # under game/ and so is never scanned.
    "_image_load_log", "_profile_screen", "_developer",
}

missing = {k: v for k, v in refs.items() if k not in defined and k not in BUILTIN}

print("screens defined: %d   distinct names referenced: %d" % (len(defined), len(refs)))
if missing:
    print("\nREFERENCED BUT NEVER DEFINED:")
    for name in sorted(missing):
        for path in sorted(missing[name]):
            print("  %-34s <- %s" % (name, path))
    sys.exit(1)
print("every referenced screen is defined.")
