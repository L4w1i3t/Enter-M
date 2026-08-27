"""Measure proper-noun density in MC's narration prose.

Companion to ``docs/story/audits/NARRATION_NAMING_AUDIT.md``. Re-run after an apply pass to
check the targets in that document's section 6.

A "narration line" is a bare quoted string in a story file -- MC's first-person
voice, with no speaker prefix. Speaker lines, ``nier`` blackout narration, screen
text, and comments are excluded from the counts but are read for context, since
a namebox on the preceding line is what makes a narration line's name redundant.

Each name-opening narration line is sorted into one of three tiers:

    T1  first naming of this person in the scene beat        -> keep
    T2  established, no rival same-gender referent in scope  -> free to vary
    T3  another woman on stage or recently speaking          -> name disambiguates

Scene beats reset on every ``scene`` statement. "In scope" means on stage via
``show``/``hide`` tracking, among the last four speakers, or named elsewhere in
the same line.

Usage:
    python tools/narration_naming_report.py
    python tools/narration_naming_report.py --tier T2 --list
    python tools/narration_naming_report.py --csv out.csv
"""

from __future__ import annotations

import argparse
import collections
import csv
import re
import sys
from pathlib import Path

STORY_GLOB = "game/story/**/*.rpy"

# Speaker variable -> the name that appears in the namebox.
VAR_TO_NAME = {
    "ma": "Matsuda", "ts": "Tsubaki", "ah": "Asahina", "sa": "Sam",
    "ko": "Kotonoha", "mom": "Mom", "mo": "Monika", "monika": "Monika",
    "track_coach": "Coach", "hikari": "Hikari", "homura": "Homura",
    "dai": "Daichi",
}

# Sprite tag -> name, for tracking who is physically on stage.
TAG_TO_NAME = {
    "matsuda": "Matsuda", "tsubaki": "Tsubaki", "asahina": "Asahina",
    "sam": "Sam", "kotonoha": "Kotonoha", "mom": "Mom", "monika": "Monika",
    "track_coach": "Coach", "hikari": "Hikari", "homura": "Homura",
    "daichi": "Daichi",
}

# A bare "she" is only ambiguous against other women in scope.
FEMALE = {
    "Matsuda", "Tsubaki", "Asahina", "Sam", "Kotonoha", "Mom", "Monika",
    "Hikari", "Homura",
}

NAMES = set(VAR_TO_NAME.values())
NAME_ALT = "|".join(sorted(NAMES, key=len, reverse=True))

RE_NARRATION = re.compile(r'^\s*"(.*)"\s*$')
RE_SPEAKER = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s+"(.*)"\s*$')
RE_SHOW = re.compile(r"^\s*show\s+([a-z_0-9]+)\b")
RE_HIDE = re.compile(r"^\s*hide\s+([a-z_0-9]+)\b")
RE_SCENE = re.compile(r"^\s*scene\b")
# Leading {i}/{b} style tags do not stop a line from opening on a name.
RE_OPENS_NAME = re.compile(r"^(?:\{[^}]*\})*\s*(" + NAME_ALT + r")\b")
RE_ANY_NAME = re.compile(r"\b(" + NAME_ALT + r")\b")
# The verb slot immediately after a person-subject, where the drone lives.
RE_SUBJECT_VERB = re.compile(
    r"\b(?:" + NAME_ALT + r"|She|He|They)(?:'s)?\s+([a-z]+)"
)

TARGETS = """
Targets after the apply pass (docs/story/audits/NARRATION_NAMING_AUDIT.md section 6):
  name-openers        452 -> ~300 (15.6% -> ~10%)
  worst-file density  35% -> at or under 22%
  'looks' after a person-subject   67 -> ~35
  T1 count            unchanged at 98
The last one is the guard rail: if re-establish lines are disappearing, the pass
has gone too far and the reader is losing track of who is in the room.
"""


class Row:
    __slots__ = ("path", "line", "who", "tier", "text", "rivals", "echo")

    def __init__(self, path, line, who, tier, text, rivals, echo):
        self.path = path
        self.line = line
        self.who = who
        self.tier = tier
        self.text = text
        self.rivals = rivals
        self.echo = echo


def scan(path: Path, root: Path):
    """Yield a Row per name-opening narration line, plus per-file totals."""
    rel = path.relative_to(root).as_posix()
    rows = []
    narration = 0
    verbs = collections.Counter()

    on_stage: set[str] = set()
    recent: collections.deque[str] = collections.deque(maxlen=4)
    named_in_beat: set[str] = set()
    previous_speaker: str | None = None

    for number, raw in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if RE_SCENE.match(raw):
            on_stage, named_in_beat, previous_speaker = set(), set(), None
            recent.clear()
            continue

        match = RE_SHOW.match(raw)
        if match:
            name = TAG_TO_NAME.get(match.group(1))
            if name:
                on_stage.add(name)
            continue

        match = RE_HIDE.match(raw)
        if match:
            name = TAG_TO_NAME.get(match.group(1))
            if name:
                on_stage.discard(name)
            continue

        match = RE_SPEAKER.match(raw)
        if match:
            name = VAR_TO_NAME.get(match.group(1))
            previous_speaker = name
            if name:
                recent.append(name)
                named_in_beat.add(name)
            continue

        match = RE_NARRATION.match(raw)
        if not match:
            continue

        narration += 1
        text = match.group(1)
        for verb in RE_SUBJECT_VERB.findall(re.sub(r"\{[^}]*\}", "", text)):
            verbs[verb] += 1

        opener = RE_OPENS_NAME.match(text)
        if not opener:
            named_in_beat.update(RE_ANY_NAME.findall(text))
            previous_speaker = None
            continue

        who = opener.group(1)
        rivals = {n for n in (on_stage | set(recent)) if n in FEMALE}
        rivals |= {n for n in RE_ANY_NAME.findall(text) if n != who and n in FEMALE}
        rivals.discard(who)

        if who not in named_in_beat:
            tier = "T1"
        elif who in FEMALE and not rivals:
            tier = "T2"
        else:
            tier = "T3"

        rows.append(Row(rel, number, who, tier, text, sorted(rivals),
                        previous_speaker == who))

        named_in_beat.add(who)
        named_in_beat.update(RE_ANY_NAME.findall(text))
        previous_speaker = None

    return rows, narration, verbs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="project root (default: parent of tools/)")
    parser.add_argument("--tier", choices=("T1", "T2", "T3"),
                        help="restrict --list and --csv to one tier")
    parser.add_argument("--list", action="store_true", help="print every matching line")
    parser.add_argument("--csv", type=Path, help="write matching lines to a CSV")
    args = parser.parse_args()

    root: Path = args.root
    paths = sorted(root.glob(STORY_GLOB))
    if not paths:
        print(f"no story files under {root / STORY_GLOB}", file=sys.stderr)
        return 1

    rows: list[Row] = []
    narration_by_file: collections.Counter = collections.Counter()
    verbs: collections.Counter = collections.Counter()
    for path in paths:
        file_rows, narration, file_verbs = scan(path, root)
        rows.extend(file_rows)
        narration_by_file[path.relative_to(root).as_posix()] = narration
        verbs.update(file_verbs)

    total_narration = sum(narration_by_file.values())
    tiers = collections.Counter(row.tier for row in rows)

    print(f"narration lines           {total_narration}")
    print(f"opening with a name       {len(rows)}"
          f"  ({100 * len(rows) / max(1, total_narration):.1f}%)")
    print(f"  T1 re-establish (keep)  {tiers['T1']}")
    print(f"  T2 free to vary         {tiers['T2']}")
    print(f"  T3 disambiguating       {tiers['T3']}")
    print(f"namebox echoes            {sum(1 for r in rows if r.echo)}")
    print(f"'looks' after a subject   {verbs['looks']}")

    print("\ndensity by file (name-openers / narration lines):")
    by_file = collections.Counter(row.path for row in rows)
    for rel, count in by_file.most_common():
        total = narration_by_file[rel]
        flag = "  <-- over 22%" if total and 100 * count / total > 22 else ""
        print(f"  {rel:<48}{count:>4} / {total:<4} {100 * count / max(1, total):>5.1f}%{flag}")

    print("\nmost common verb after a person-subject:")
    for verb, count in verbs.most_common(10):
        print(f"  {verb:<12}{count}")

    selected = [r for r in rows if not args.tier or r.tier == args.tier]

    if args.list:
        print()
        for row in selected:
            rivals = f"  (rivals: {', '.join(row.rivals)})" if row.rivals else ""
            echo = "  [namebox echo]" if row.echo else ""
            print(f"{row.path}:{row.line} [{row.who}] {row.tier}{echo}")
            print(f"    {row.text[:150]}{rivals}")

    if args.csv:
        with args.csv.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["file", "line", "who", "tier", "namebox_echo",
                             "rivals", "text"])
            for row in selected:
                writer.writerow([row.path, row.line, row.who, row.tier,
                                 int(row.echo), " ".join(row.rivals), row.text])
        print(f"\nwrote {len(selected)} rows to {args.csv}")

    print(TARGETS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
