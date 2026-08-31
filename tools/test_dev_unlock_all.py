"""Behavioral test for the developer ALL SIDE CONTENT switch."""

from __future__ import annotations

import pathlib
import types


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "game" / "addons" / "Developer Date Jump" / "dev_date_jump.rpy"


def _python_model_source():
    text = SOURCE.read_text(encoding="utf-8")
    marker = "init python:\n"
    start = text.index(marker) + len(marker)
    lines = text[start:].splitlines()
    block = []
    for line in lines:
        if line and not line.startswith("    "):
            break
        block.append(line[4:] if line.startswith("    ") else line)
    return "\n".join(block).replace(
        "import renpy.store as _dev_date_jump_store",
        "_dev_date_jump_store = renpy.store",
    )


def main():
    persistent = types.SimpleNamespace(roster_met_ids={"always_present"})
    saved = []
    notices = []
    restarts = []

    stories = (
        types.SimpleNamespace(persistent_key="side_alpha_unlocked"),
        types.SimpleNamespace(persistent_key="side_beta_unlocked"),
        types.SimpleNamespace(persistent_key=None),
    )
    store = types.SimpleNamespace(
        character_story_catalog=(types.SimpleNamespace(stories=stories),),
        archive_unlock_keys=lambda: ("archive_music",),
        cg_all_keys=lambda: ("cg_alpha", "shared_key"),
        roster_outfit_keys=lambda: ("outfit_alpha", "shared_key"),
        music_all_keys=lambda: ("track_alpha",),
        roster_gated_ids=lambda: ("asahina", "matsuda"),
    )
    renpy = types.SimpleNamespace(
        store=store,
        save_persistent=lambda: saved.append(True),
        notify=lambda message: notices.append(message),
        restart_interaction=lambda: restarts.append(True),
        get_all_labels=lambda: (),
        has_label=lambda _label: False,
    )
    env = {"persistent": persistent, "renpy": renpy}
    exec(compile(_python_model_source(), str(SOURCE), "exec"), env)

    keys = env["dev_date_jump_side_content_keys"]()
    assert keys == (
        "archive_music",
        "side_alpha_unlocked",
        "side_beta_unlocked",
        "cg_alpha",
        "shared_key",
        "outfit_alpha",
        "track_alpha",
    )
    assert env["dev_date_jump_side_content_state"]() == "DISABLED"

    env["dev_date_jump_set_all_side_content"](True)
    assert env["dev_date_jump_side_content_state"]() == "ENABLED"
    assert all(getattr(persistent, key) is True for key in keys)
    assert persistent.roster_met_ids == {"always_present", "asahina", "matsuda"}

    # A partial manual change is reported honestly and the toggle repairs it.
    persistent.cg_alpha = False
    assert env["dev_date_jump_side_content_state"]() == "PARTIAL"
    env["dev_date_jump_toggle_all_side_content"]()
    assert env["dev_date_jump_side_content_state"]() == "ENABLED"

    env["dev_date_jump_toggle_all_side_content"]()
    assert env["dev_date_jump_side_content_state"]() == "DISABLED"
    assert all(getattr(persistent, key) is False for key in keys)
    assert persistent.roster_met_ids == {"always_present"}
    assert len(saved) == 3
    assert len(notices) == 3
    assert len(restarts) == 3

    print("developer unlock-all contract: PASS")


if __name__ == "__main__":
    main()
