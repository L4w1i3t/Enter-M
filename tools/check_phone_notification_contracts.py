"""Guard the phone alert's interaction and native-resolution layout contracts.

Ren'Py propagates non-None Function action results out of the current
interaction. A repeating quick-menu timer must therefore call a void wrapper,
or ordinary dialogue will advance as though the player dismissed it.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHONE_PATH = ROOT / "game" / "addons" / "Phone System" / "text.rpy"
SCREENS_PATH = ROOT / "game" / "screens.rpy"


def fail(message: str) -> None:
    raise SystemExit("PHONE NOTIFICATION CONTRACT FAILED: " + message)


def main() -> None:
    phone_source = PHONE_PATH.read_text(encoding="utf-8")
    screens_source = SCREENS_PATH.read_text(encoding="utf-8")

    expected_timer = (
        "timer 0.5 repeat True action "
        "Function(phone_notification_poll_action, _update_screens=False)"
    )
    if expected_timer not in screens_source:
        fail("quick-menu timer is not routed through the non-updating void wrapper")
    if "Function(phone_notification_poll)" in screens_source:
        fail("quick-menu timer directly exposes the poll's boolean result")

    wrapper_match = re.search(
        r"^    def phone_notification_poll_action\(\):\n(?P<body>.*?)"
        r"(?=^    def |^# )",
        phone_source,
        re.MULTILINE | re.DOTALL,
    )
    if wrapper_match is None:
        fail("phone_notification_poll_action() is missing")

    wrapper = wrapper_match.group("body")
    required_wrapper_lines = (
        "changed = phone_notification_poll()",
        "if changed:",
        "renpy.restart_interaction()",
    )
    for line in required_wrapper_lines:
        if line not in wrapper:
            fail(f"void wrapper lost required behavior: {line}")
    if not wrapper.rstrip().endswith("return None"):
        fail("screen-action wrapper can return a non-None interaction result")

    alert_match = re.search(
        r"^screen phone_notification_alert\(.*?\):\n(?P<body>.*?)"
        r"(?=^# -{20,}\n# SCREEN: phone_text_screen)",
        phone_source,
        re.MULTILINE | re.DOTALL,
    )
    if alert_match is None:
        fail("phone_notification_alert screen is missing")
    alert = alert_match.group("body")

    if "xysize (344, 76)" not in alert:
        fail("alert is no longer the reviewed 344x76 native-resolution panel")
    if "yoffset -198" not in alert or "xpos 108" not in alert:
        fail("alert moved into the quick-menu/dialogue clearance zone")
    if not re.search(
        r"vbox:\s+.*?text _phone_alert_title.*?text _phone_alert_detail",
        alert,
        re.DOTALL,
    ):
        fail("title and detail no longer flow together inside the alert vbox")

    style_match = re.search(
        r"^style phone_notification_alert_button is empty:\n(?P<body>.*?)"
        r"(?=^style )",
        phone_source,
        re.MULTILINE | re.DOTALL,
    )
    if style_match is None or "xysize (344, 76)" not in style_match.group("body"):
        fail("button hitbox and rendered alert panel no longer match")

    screen_height = 720
    alert_height = 76
    alert_yoffset = -198
    alert_bottom = screen_height - alert_height + alert_yoffset + alert_height
    textbox_top = screen_height - 182
    if alert_bottom >= textbox_top:
        fail("alert overlaps the 1280x720 dialogue-box bounds")

    print(
        "Phone notification contracts passed: void 0.5s poll action; "
        "344x76 flowing alert clears the 1280x720 dialogue box."
    )


if __name__ == "__main__":
    main()
