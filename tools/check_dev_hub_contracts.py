"""Static wiring audit for ENTER M's developer-only front door.

Ren'Py lint cannot prove that a function named as a string in ``dev_hub_call``
exists. This check keeps the hub's cross-addon buttons, screens, shipping-build
exclusion, and guarded title-screen mount from silently drifting apart.
"""

from __future__ import annotations

import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
HUB = GAME / "addons" / "Dev Hub" / "dev_hub.rpy"


def _sources():
    for path in GAME.rglob("*.rpy"):
        if any(part in {"cache", "saves", "python-packages"} for part in path.parts):
            continue
        yield path, path.read_text(encoding="utf-8", errors="replace")


def main():
    files = tuple(_sources())
    blob = "\n".join(text for _path, text in files)
    hub = HUB.read_text(encoding="utf-8")

    functions = set(re.findall(r"^\s*def\s+([A-Za-z_]\w*)\s*\(", blob, re.M))
    screens = set(re.findall(r"^\s*screen\s+([A-Za-z_]\w*)\s*\(", blob, re.M))

    call_targets = set(re.findall(
        r"Function\(dev_hub_call,\s*[\"']([A-Za-z_]\w*)[\"']", hub))
    show_targets = set(re.findall(
        r"Function\(dev_hub_show,\s*[\"']([A-Za-z_]\w*)[\"']", hub))

    errors = []
    missing_calls = sorted(call_targets - functions)
    missing_screens = sorted(show_targets - screens)
    if missing_calls:
        errors.append("missing dev_hub_call function(s): " + ", ".join(missing_calls))
    if missing_screens:
        errors.append("missing dev_hub_show screen(s): " + ", ".join(missing_screens))

    critical_functions = {
        # unlock-all ownership
        "dev_date_jump_toggle_all_side_content",
        "dev_date_jump_side_content_state",
        "archive_unlock_keys",
        "cg_all_keys",
        "music_all_keys",
        "roster_outfit_keys",
        "roster_gated_ids",
        # achievements
        "ach_refresh",
        "ach_dev_clear",
        "ach_dev_grant",
        "ach_dev_revoke",
        "ach_dev_toggle_autounlock",
        # economy and its deferred receipt
        "mc_balance",
        "mc_dev_give",
        "mc_dev_fill",
        "mc_dev_reset",
        "mc_dev_grant_all",
        "mc_dev_clear_cards",
        "mc_main_menu_enter",
    }
    missing_critical = sorted(critical_functions - functions)
    if missing_critical:
        errors.append("missing critical developer helper(s): " + ", ".join(missing_critical))

    options = (GAME / "options.rpy").read_text(encoding="utf-8")
    if not re.search(
            r"build\.classify\(\s*[\"']/game/addons/Dev Hub/\*\*[\"']\s*,\s*None\s*\)",
            options):
        errors.append("options.rpy no longer excludes addons/Dev Hub from builds")

    screens_source = (GAME / "screens.rpy").read_text(encoding="utf-8")
    mount_guard = re.compile(
        r"if\s+config\.developer\s+and\s+renpy\.has_screen\(\s*[\"']dev_hub_mount[\"']\s*\)"
        r"\s*:\s*\n\s*use\s+dev_hub_mount",
        re.M,
    )
    if not mount_guard.search(screens_source):
        errors.append("main-menu Dev Hub mount is not developer- and existence-guarded")

    if errors:
        print("developer hub contract: FAIL")
        for error in errors:
            print("- " + error)
        return 1

    print(
        "developer hub contract: PASS "
        f"({len(call_targets)} function buttons, {len(show_targets)} screen buttons)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
