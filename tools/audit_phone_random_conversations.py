"""Audit the rebuilt one-shot phone conversation catalog.

This is deliberately source-level: it catches catalog drift before Ren'Py boots,
while the normal compile/lint pass remains responsible for script syntax.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "game" / "addons" / "Phone System" / "random_conversations.rpy"
MONIKA_OPEN_PATH = ROOT / "game" / "story" / "season1" / "0525.rpy"

EXPECTED = {
    "rc2_asa_ashen_vow": ("Asa", "text", "Git gud."),
    "rc2_asa_mr_toast": ("Asa", "text", "between the bed and the wall"),
    "rc2_asa_soup_store": ("Asa", "call", "soup aisle"),
    "rc2_matsuda_ui_review": ("Matsuda Akai", "text", "UI can suck my fat ass"),
    "rc2_matsuda_wrong_person": ("Matsuda Akai", "text", "wrong person"),
    "rc2_matsuda_duck_hat": ("Matsuda Akai", "facetime", "duck hat"),
    "rc2_mom_mid": ("Mom", "text", "Apparently only mid"),
    "rc2_mom_autocorrect": ("Mom", "text", "turning autocorrect off"),
    "rc2_mom_work_opinion": ("Mom", "call", "tenant-rights workshop"),
    "rc2_monika_vague_draft": ("Monika", "text", "I understand nothing"),
    "rc2_monika_horror_verdict": ("Monika", "text", "aggravated bad taste"),
    "rc2_monika_vp_rant": ("Monika", "facetime", "bad at his job"),
}


def fail(message: str) -> None:
    raise SystemExit("PHONE RANDOM AUDIT FAILED: " + message)


def main() -> None:
    source = CATALOG_PATH.read_text(encoding="utf-8")
    start = source.rfind("PHONE_RANDOM_CONVERSATIONS = [")
    if start < 0:
        fail("runtime catalog assignment is missing")

    end = source.find("# Which of these have already happened", start)
    if end < 0:
        fail("could not locate the end of the runtime catalog")
    catalog = source[start:end]

    matches = list(re.finditer(r'"id"\s*:\s*"([^"]+)"', catalog))
    ids = [match.group(1) for match in matches]
    if len(ids) != len(set(ids)):
        fail("runtime conversation ids are not unique")
    if set(ids) != set(EXPECTED):
        missing = sorted(set(EXPECTED) - set(ids))
        extra = sorted(set(ids) - set(EXPECTED))
        fail(f"expected exactly 12 rebuilt entries; missing={missing}, extra={extra}")

    if '("seen",' in catalog or '("unseen",' in catalog:
        fail("a rebuilt conversation depends on another random conversation")

    for index, match in enumerate(matches):
        entry_id = match.group(1)
        segment_end = matches[index + 1].start() if index + 1 < len(matches) else len(catalog)
        segment = catalog[match.start():segment_end]
        contact, kind, premise_token = EXPECTED[entry_id]
        if f'"contact": "{contact}"' not in segment:
            fail(f"{entry_id} is assigned to the wrong contact")
        if f'"kind": "{kind}"' not in segment:
            fail(f"{entry_id} has the wrong conversation kind")
        if premise_token not in segment:
            fail(f"{entry_id} no longer contains its defining premise")

    if '"monika_video"' not in source or "default phone_open_monika_video = False" not in source:
        fail("Monika's independent FaceTime channel is not registered")
    monika_day = MONIKA_OPEN_PATH.read_text(encoding="utf-8")
    if '$ phone_open("monika_video")' not in monika_day:
        fail("0525 does not open Monika's FaceTime channel")

    kinds = {
        kind: sum(1 for _, entry_kind, _ in EXPECTED.values() if entry_kind == kind)
        for kind in ("text", "call", "facetime")
    }
    print(
        "Phone random conversation audit passed: "
        f"{len(ids)}/12 independent entries "
        f"({kinds['text']} text, {kinds['call']} call, {kinds['facetime']} facetime)."
    )


if __name__ == "__main__":
    main()
