"""Check the story prose against the background art it plays over.

Swapping a background is cheap; the prose written for the OLD art is what
breaks. The vanilla `bg kitchen` was replaced with a galley that has no table
in it, and eighteen scenes went on describing people sitting down to eat in a
room with no chairs. This finds that class of problem.

Two modes:

  report   For every `scene bg <name>`, list the room fixtures the prose names
           while that background is on screen. Run it after replacing a piece
           of art and read the list against the new image -- if the prose says
           "locker" and the new art has none, that is the whole answer.

  check    Enforce the RULES table below, which records what a given background
           does NOT contain. Exits 1 on a violation, so it can gate a build.

    python tools/bg_prose_consistency.py report --bg club_day
    python tools/bg_prose_consistency.py check
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STORY_DIRS = ("game/story/season1",)

# Nouns worth noticing. Deliberately over-inclusive: `report` is for a human to
# read, and a few homonyms ("not a fan of", "on the fence") are cheaper than a
# missed contradiction. The RULES below are what gets enforced, and those use
# tighter patterns.
FIXTURE_WORDS = re.compile(
    r"\b("
    r"board|blackboard|chalkboard|chalk|whiteboard|marker|eraser|podium|lectern|"
    r"closet|locker|lockers|cabinet|shelf|shelves|bookshelf|"
    r"window|windows|curtain|curtains|blinds|"
    r"desk|desks|chair|chairs|table|stool|bench|couch|sofa|"
    r"door|doorway|stairs|staircase|stairwell|landing|"
    r"sink|counter|stove|oven|kettle|refrigerator|fridge|toaster|microwave|"
    r"clock|poster|bulletin|projector|screen|piano|plant|fan|radiator|vending|"
    r"floor|carpet|rug|tile|ceiling|"
    r"rail|railing|gate|fence|hedge|porch|driveway|mailbox|lawn|garage|"
    r"street|sidewalk|curb|crossing"
    r")\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Rule:
    """`pattern` must not appear in prose while `bg` is the active background."""

    bg: str
    pattern: str
    why: str


# What each replaced background does NOT have in it. Add a row whenever a piece
# of art is swapped for one that drops a fixture the prose had been using.
RULES: tuple[Rule, ...] = (
    # images/bg/kitchen.png is a galley: counters, stove, sink, back door.
    Rule("kitchen", r"\b(takes? (?:his|her|my|their) seat|sits? down at the table"
                    r"|around the table|sets? the table)\b",
         "the kitchen art is a galley with no table and no chairs -- "
         "use `bg dining_table`"),
    # images/bg/club.png and class.png both have green/slate CHALKboards.
    Rule("club_day", r"\b(marker|whiteboard|dry[- ]erase)\b",
         "the club room's board is a chalkboard"),
    Rule("class_day", r"\b(marker|whiteboard|dry[- ]erase)\b",
         "the classroom board is a chalkboard"),
    # mod_assets/bg/dining_table.png is the dining room; the kitchen is next door.
    # Fixtures may be referenced (sound carries, people walk through), but nobody
    # should be *standing at* one while the dining room is on screen.
    Rule("dining_table", r"\b(?:stands?|standing|is|was) at the (?:counter|stove|sink)\b",
         "the dining room has no counter, stove or sink -- "
         "move the beat to `bg kitchen` or send the character through"),
    Rule("dining_table_night", r"\b(?:stands?|standing|is|was) at the (?:counter|stove|sink)\b",
         "the dining room has no counter, stove or sink -- "
         "move the beat to `bg kitchen` or send the character through"),
)

# Night art is lit by its own practical lights and has a dark window; under a
# daytime grade the frame fights itself. Every dining scene shipped that way
# until Aug 21 2026, because the art arrived after the scenes were written.
#
# Only this one direction is checked. The reverse -- daytime art under a night
# grade -- is CORRECT wherever no night variant of that art exists, which is the
# normal case: `bg bedroom` has no night twin, so all fourteen of MC's evening
# bedroom scenes are `bedroom` + `home_night` on purpose. Flagging that produced
# nothing but noise.
NIGHT_BG = re.compile(r"night|dark", re.IGNORECASE)
DAY_PRESETS = frozenset({"home", "afternoon", "overcast", "winter", "winter_evening"})

SCENE_BG = re.compile(r"^\s*scene\s+bg\s+([A-Za-z_0-9]+)")
SCENE_ANY = re.compile(r"^\s*scene\b")
# nier_clear ends a narration block, which usually also ends the location.
SCOPE_BREAK = re.compile(r"^\s*call\s+nier_clear\b")
# A displayed line of prose or dialogue, as opposed to a statement.
SPOKEN = re.compile(r'^\s*(?:[a-z_][a-z_0-9]*\s+)?(?:[a-z0-9_]+\s+)*"(?P<text>.*)"\s*$')


def iter_prose(paths: list[Path]):
    """Yield (path, lineno, active_bg, text) for every displayed line."""
    for path in paths:
        active_bg = None
        lines = path.read_text(encoding="utf-8").split("\n")
        for lineno, raw in enumerate(lines, start=1):
            stripped = raw.strip()
            if not stripped or stripped.startswith("#"):
                continue
            scene_match = SCENE_BG.match(raw)
            if scene_match:
                active_bg = scene_match.group(1)
                continue
            if SCENE_ANY.match(raw) or SCOPE_BREAK.match(raw):
                active_bg = None
                continue
            if active_bg is None:
                continue
            spoken = SPOKEN.match(raw)
            if spoken:
                yield path, lineno, active_bg, spoken.group("text")


def collect_story_files(story_dirs: list[str]) -> list[Path]:
    files: list[Path] = []
    for rel in story_dirs:
        directory = PROJECT_ROOT / rel
        if not directory.is_dir():
            sys.exit("no such directory: %s" % directory)
        files.extend(sorted(directory.glob("*.rpy")))
    if not files:
        sys.exit("no .rpy files found in %s" % ", ".join(story_dirs))
    return files


def run_report(files: list[Path], only_bg: str | None) -> int:
    per_bg: dict[str, Counter] = defaultdict(Counter)
    examples: dict[tuple[str, str], list[str]] = defaultdict(list)
    for path, lineno, bg, text in iter_prose(files):
        if only_bg and bg != only_bg:
            continue
        for word in FIXTURE_WORDS.findall(text):
            word = word.lower()
            per_bg[bg][word] += 1
            if len(examples[(bg, word)]) < 3:
                examples[(bg, word)].append("%s:%d" % (path.name, lineno))

    if not per_bg:
        print("no prose found" + (" for bg %s" % only_bg if only_bg else ""))
        return 0

    for bg in sorted(per_bg):
        print("=== bg %s ===" % bg)
        for word, count in per_bg[bg].most_common():
            print("  %-14s %4d   %s" % (word, count, " ".join(examples[(bg, word)])))
        print()
    print("Read each list against the art. A fixture the new image does not have "
          "is a line to rewrite or a scene to reassign.")
    return 0


ATMOS_CALL = re.compile(r"""^\s*\$\s*atmos\(\s*["']([a-z_]+)["']""")


def check_grade_pairing(files: list[Path]) -> int:
    """Flag night art opened under a daytime atmos preset. Only the atmos call
    belonging to the same scene block is considered, so a deliberate mid-scene
    change of grade is left alone."""
    violations = 0
    for path in files:
        lines = path.read_text(encoding="utf-8").split("\n")
        for index, raw in enumerate(lines):
            scene_match = SCENE_BG.match(raw)
            if not scene_match:
                continue
            bg = scene_match.group(1)
            preset = None
            # the scene's own grade is set within the few statements that follow
            for follower in lines[index + 1:index + 7]:
                if SCENE_ANY.match(follower):
                    break
                atmos_match = ATMOS_CALL.match(follower)
                if atmos_match:
                    preset = atmos_match.group(1)
                    break
            if preset is None:
                continue
            if NIGHT_BG.search(bg) and preset in DAY_PRESETS:
                violations += 1
                print("%s:%d  night art `%s` opened under the daytime grade %r"
                      % (path.name, index + 1, bg, preset))
    return violations


def run_check(files: list[Path]) -> int:
    compiled = [(rule, re.compile(rule.pattern, re.IGNORECASE)) for rule in RULES]
    violations = 0
    for path, lineno, bg, text in iter_prose(files):
        for rule, pattern in compiled:
            if bg != rule.bg:
                continue
            found = pattern.search(text)
            if found:
                violations += 1
                print("%s:%d  [bg %s]  %r -- %s"
                      % (path.name, lineno, bg, found.group(0), rule.why))
                print("      %s" % text[:120])
    violations += check_grade_pairing(files)
    if violations:
        print("\n%d violation(s)." % violations)
        return 1
    print("No violations across %d fixture rule(s), the grade pairing check, "
          "and %d file(s)." % (len(RULES), len(files)))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("report", "check"))
    parser.add_argument("--bg", help="report mode: limit to one background name")
    parser.add_argument("--story-dir", action="append", dest="story_dirs",
                        help="repo-relative story directory (repeatable); "
                             "defaults to %s" % ", ".join(DEFAULT_STORY_DIRS))
    args = parser.parse_args()

    files = collect_story_files(args.story_dirs or list(DEFAULT_STORY_DIRS))
    if args.mode == "report":
        return run_report(files, args.bg)
    return run_check(files)


if __name__ == "__main__":
    raise SystemExit(main())
