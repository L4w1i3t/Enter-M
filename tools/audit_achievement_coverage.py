#!/usr/bin/env python3
"""Static coverage audit for ENTER M's live achievement catalog.

This deliberately checks both halves of the award contract:

* every trophy has an exact completion-event hook, before any Arcade/story split;
* every trophy has a persisted derived condition for old-save reconciliation.

It also rejects literal grants to retired/unknown ids and verifies the developer
grant/revoke surface. The checker imports no Ren'Py code, so it is safe to run in
ordinary Python from the repository root.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ACHIEVEMENTS_PATH = Path("game/addons/Achievements/achievements.rpy")


@dataclass(frozen=True)
class Coverage:
    path: Path
    markers: tuple[str, ...]
    recovery: str


# The catalog is deliberately nine trophies until more playable content ships.
# Keeping the objective contract here makes an edit fail loudly if a row is
# renamed, removed, or repointed without its completion event being updated.
EXPECTED: dict[str, Coverage] = {
    "music_on": Coverage(
        Path("game/story/season1/0531.rpy"),
        ("persistent.chapter05_completed = True", 'ach_grant("music_on")'),
        'flag="chapter05_completed"',
    ),
    "beat_matsuda": Coverage(
        Path("game/addons/Character Stories/cs_matsuda_02.rpy"),
        (
            "$ persistent.id_mode_unlocked = True",
            '$ ach_grant("beat_matsuda")',
            "if arcade_active:",
        ),
        'flag="id_mode_unlocked"',
    ),
    "koto_clear": Coverage(
        Path("game/addons/Matsuda's Sick Boss Fight/kotonohamode/kototouhou.rpy"),
        (
            'if _kt_result == "victory" and not (kt_last_practice or kt_last_endless):',
            '$ ach_grant("koto_clear")',
            "if arcade_active:",
        ),
        'flag="kotomode_cleared"',
    ),
    "date_win": Coverage(
        Path("game/addons/Matsuda's Sick Boss Fight/monikamode/monika_date.rpy"),
        (
            "$ persistent.arcade_monika_cleared = True",
            '$ ach_grant("date_win")',
            "if arcade_active:",
        ),
        'flag="arcade_monika_cleared"',
    ),
    "cards_30": Coverage(
        Path("game/addons/Matsucoin Currency and Gacha/mc_gacha.rpy"),
        ('Function(ach_grant_if_met, "cards_30")',),
        "earned=lambda: _ach_unique_card_count() >= ACH_CARD_TARGET",
    ),
    "matsuda_id": Coverage(
        Path("game/addons/Character Stories/cs_matsuda_02.rpy"),
        (
            "$ persistent.arcade_id_cleared = True",
            '$ ach_grant("matsuda_id")',
            "if arcade_active:",
        ),
        'flag="arcade_id_cleared"',
    ),
    "tsuba_spare": Coverage(
        Path("game/addons/Matsuda's Sick Boss Fight/tsubakimode/tsubaki_soul.rpy"),
        (
            '$ persistent.tsubamode_outcome = "pacifist"',
            '$ tsb_record_route_clear("pacifist")',
            '$ ach_grant("tsuba_spare")',
            "if arcade_active:",
        ),
        'earned=lambda: _ach_tsubaki_route_cleared("pacifist")',
    ),
    "tsuba_violence": Coverage(
        Path("game/addons/Matsuda's Sick Boss Fight/tsubakimode/tsubaki_soul.rpy"),
        (
            '$ persistent.tsubamode_outcome = "violence"',
            '$ tsb_record_route_clear("violence")',
            '$ ach_grant("tsuba_violence")',
            "if arcade_active:",
        ),
        'earned=lambda: _ach_tsubaki_route_cleared("violence")',
    ),
    "tsuba_betrayal": Coverage(
        Path("game/addons/Matsuda's Sick Boss Fight/tsubakimode/tsubaki_soul.rpy"),
        (
            '$ persistent.tsubamode_outcome = "betrayal"',
            '$ tsb_record_route_clear("betrayal")',
            '$ ach_grant("tsuba_betrayal")',
            "if arcade_active:",
        ),
        'earned=lambda: _ach_tsubaki_route_cleared("betrayal")',
    ),
}


def source(path: Path) -> str:
    return (PROJECT_ROOT / path).read_text(encoding="utf-8-sig")


def code_before_comment(line: str) -> str:
    """Return a Ren'Py/Python line without an unquoted trailing comment."""
    quote: str | None = None
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quote is not None:
            escaped = True
            continue
        if char in ("'", '"'):
            if quote is None:
                quote = char
            elif quote == char:
                quote = None
            continue
        if char == "#" and quote is None:
            return line[:index]
    return line


def code_lines(text: str) -> list[str]:
    return [code_before_comment(line) for line in text.splitlines()]


def extract_calls(text: str, name: str) -> list[str]:
    """Extract balanced ``name(...)`` calls while respecting quoted strings."""
    calls: list[str] = []
    needle = name + "("
    cursor = 0
    while True:
        start = text.find(needle, cursor)
        if start < 0:
            return calls
        index = start + len(name)
        depth = 0
        quote: str | None = None
        escaped = False
        while index < len(text):
            char = text[index]
            if escaped:
                escaped = False
            elif char == "\\" and quote is not None:
                escaped = True
            elif char in ("'", '"'):
                if quote is None:
                    quote = char
                elif quote == char:
                    quote = None
            elif quote is None:
                if char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                    if depth == 0:
                        calls.append(text[start : index + 1])
                        cursor = index + 1
                        break
            index += 1
        else:
            raise ValueError(f"unterminated {name} call at offset {start}")


def catalog_calls(text: str) -> dict[str, str]:
    start = text.index("ACHIEVEMENTS = [")
    end = text.index("ACH_BY_ID", start)
    calls: dict[str, str] = {}
    for call in extract_calls(text[start:end], "Achievement"):
        match = re.match(r'Achievement\(\s*["\']([^"\']+)["\']', call)
        if match is None:
            continue
        aid = match.group(1)
        if aid in calls:
            raise ValueError(f"duplicate catalog id {aid!r}")
        calls[aid] = call
    return calls


def find_ordered(path: Path, markers: tuple[str, ...]) -> tuple[bool, list[int]]:
    lines = code_lines(source(path))
    cursor = 0
    found: list[int] = []
    for marker in markers:
        for index in range(cursor, len(lines)):
            if marker in lines[index]:
                found.append(index + 1)
                cursor = index + 1
                break
        else:
            return False, found
    return True, found


def literal_award_sites() -> dict[str, list[str]]:
    sites: dict[str, list[str]] = {}
    direct = re.compile(r'\bach_grant\s*\(\s*["\']([^"\']+)["\']')
    conditional = re.compile(
        r'\bFunction\s*\(\s*ach_grant_if_met\s*,\s*["\']([^"\']+)["\']'
    )
    for path in sorted((PROJECT_ROOT / "game").rglob("*.rpy")):
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        for line_number, line in enumerate(code_lines(source(path.relative_to(PROJECT_ROOT))), 1):
            for pattern in (direct, conditional):
                for match in pattern.finditer(line):
                    sites.setdefault(match.group(1), []).append(
                        f"{relative}:{line_number}"
                    )
    return sites


def audit() -> int:
    problems: list[str] = []
    achievement_text = source(ACHIEVEMENTS_PATH)

    try:
        calls = catalog_calls(achievement_text)
    except (ValueError, OSError) as error:
        print(f"ERROR: cannot parse achievement catalog: {error}")
        return 1

    expected_ids = list(EXPECTED)
    actual_ids = list(calls)
    if actual_ids != expected_ids:
        problems.append(
            "live catalog mismatch:\n"
            f"    expected {expected_ids!r}\n"
            f"    actual   {actual_ids!r}"
        )

    sites = literal_award_sites()
    unknown = sorted(set(sites) - set(calls))
    if unknown:
        problems.append(f"literal award site(s) reference unknown/retired ids: {unknown}")

    coverage_lines: list[str] = []
    for aid, spec in EXPECTED.items():
        call = re.sub(r"\s+", " ", calls.get(aid, ""))
        recovery = re.sub(r"\s+", " ", spec.recovery)
        if recovery not in call:
            problems.append(f"{aid}: missing derived recovery condition {spec.recovery!r}")

        ok, lines = find_ordered(spec.path, spec.markers)
        if not ok:
            missing = spec.markers[len(lines)]
            problems.append(
                f"{aid}: missing/out-of-order event marker {missing!r} in "
                f"{spec.path.as_posix()}"
            )
        if aid not in sites:
            problems.append(f"{aid}: no literal exact-event award site")

        award_index = next(
            (index for index, marker in enumerate(spec.markers) if "ach_grant" in marker),
            0,
        )
        event_line = lines[award_index] if len(lines) > award_index else 0
        coverage_lines.append(
            f"  {aid:<17} event {spec.path.as_posix()}:{event_line:<5} "
            f"+ derived recovery"
        )

    # The CDD must persist a real Kotonoha clear before its wrapper reconciles.
    koto_path = EXPECTED["koto_clear"].path
    ok, _ = find_ordered(
        koto_path,
        ('if kind == "victory":', "persistent.kotomode_cleared = True"),
    )
    if not ok:
        problems.append("koto_clear: KTGame._finish no longer persists a real clear")

    required_dev_markers = (
        "def ach_dev_grant(aid):",
        "persistent.ach_history.add(aid)",
        "def ach_dev_grant_all(notify=True):",
        "persistent.ach_earned.update(a.id for a in newly)",
        "def ach_dev_revoke(aid):",
        "_ach_rt.retest.add(aid)",
    )
    ok, _ = find_ordered(ACHIEVEMENTS_PATH, required_dev_markers)
    if not ok:
        problems.append("developer grant-all/grant/retest contract is incomplete")

    if problems:
        print("Achievement coverage audit FAILED")
        for problem in problems:
            print("  ERROR " + problem)
        return 1

    print(f"Achievement coverage audit passed: {len(EXPECTED)}/{len(EXPECTED)}")
    for line in coverage_lines:
        print(line)
    print(f"  literal award ids: {len(sites)}; unknown/retired: 0")
    print("  developer grant, grant-all, revoke/retest: covered")
    return 0


if __name__ == "__main__":
    sys.exit(audit())
