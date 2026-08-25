# Generates the platform icon files the build needs, from the single source
# image in mod_assets/gui.
#
# Ren'Py takes each icon from a different place, which is why setting one of
# them does not set the others:
#
#   Window icon - the icon in the title bar and taskbar while the game is
#   running. Comes from config.window_icon in game/options.rpy, a PNG under
#   game/. Already configured; this script does not touch it.
#
#   Windows executable icon - what Explorer, the taskbar and any desktop
#   shortcut show for the built .exe. Comes from icon.ico in the PROJECT ROOT,
#   which the launcher injects into the executable at build time (write_exe in
#   launcher/game/distribute.rpy). With no icon.ico the build silently keeps
#   the stock Ren'Py/Matsu'Py icon - there is no warning.
#
#   macOS application icon - comes from icon.icns in the project root, copied
#   into the .app bundle. Falls back to the launcher's own icon when absent.
#
# Ren'Py's default build rules classify icon.ico and icon.icns as None, so
# neither is shipped as a data file; they only ever affect the executables.
#
# Re-run this whenever the source art changes:
#
#     python tools/make_icons.py

import argparse
import os
import sys

from PIL import Image

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_SOURCE = os.path.join("game", "mod_assets", "gui", "desktop_icon.png")

# Windows picks the closest match from whatever the .ico contains, so cover the
# sizes it actually asks for rather than shipping one big image.
ICO_SIZES = [ 16, 24, 32, 48, 64, 128, 256 ]

# What macOS wants in an .icns. Pillow derives the smaller members itself.
ICNS_SIZE = 1024


def load_source(path):

    im = Image.open(path)

    if im.width != im.height:
        sys.exit("Icon source must be square, but %s is %dx%d."
                 % (path, im.width, im.height))

    # An icon needs an alpha channel even when the art is fully opaque.
    return im.convert("RGBA")


def main():

    ap = argparse.ArgumentParser(
        description="Generate icon.ico and icon.icns for the build.")

    ap.add_argument(
        "--source", default=DEFAULT_SOURCE,
        help="source image, relative to the project root (default: %s)" % DEFAULT_SOURCE)

    args = ap.parse_args()

    source = os.path.join(PROJECT, args.source)

    if not os.path.exists(source):
        sys.exit("Source image not found: %s" % source)

    im = load_source(source)
    print("source: %s (%dx%d)" % (args.source, im.width, im.height))

    ico = os.path.join(PROJECT, "icon.ico")
    im.save(ico, format="ICO", sizes=[ (s, s) for s in ICO_SIZES ])
    print("wrote icon.ico   (%s) %d bytes"
          % (", ".join("%d" % s for s in ICO_SIZES), os.path.getsize(ico)))

    icns = os.path.join(PROJECT, "icon.icns")
    im.resize((ICNS_SIZE, ICNS_SIZE), Image.LANCZOS).save(icns, format="ICNS")
    print("wrote icon.icns  (%d) %d bytes" % (ICNS_SIZE, os.path.getsize(icns)))

    return 0


if __name__ == "__main__":
    sys.exit(main())
