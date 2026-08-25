---
name: project-enter-m-overview
description: ENTER M is a Ren'Py DDLC-style dark comedy VN; structure, files, and where the canonical voice lives
metadata:
  type: project
---

ENTER M is a Ren'Py visual novel (DDLC mod framing) by user L4w1i3t. Act 1 is a slice-of-life dark comedy that slowly reveals a colder, continuous underlying narrative. Spans a Japanese school year, May 15 2025 to March 7 2026.

**Story files:** `game/story/season1/MMDD.rpy`, one label `aMMDD:` per in-game day, each ending with `call calendar_advance(days=1)` then `jump a<nextday>`. Framing files: `s1disc.rpy` (Nier-voiced disclaimer), `s1ch1.rpy` (currently near-empty, 1 line — ID-card cold open actually lives in `0515.rpy`).

**Key planning docs:**
- `game/story/critique.md` — two-pass critique. The SECOND pass ("Addendum: Second-Pass Critique With Author Context") is authorial intent and is the controlling guide. Reference files (0515-0523) also carry inline `# CRITIQUE:` comments marking drift; some are tagged `(ADDRESSED)`.
- `roadmap.md` (project root) — arc blueprint. Note it warns it is "severely out of date" but useful.

**Reference / ground-truth voice files (match these):** `0515.rpy` through `0523.rpy`. These are the polished baseline.

Core thematic engine: comedy as camouflage/avoidance, NOT a reset button. Slow burn where stakes hide in plain sight; the facts are visible, only the interpretation is hidden. Every day should move at least one "pressure meter" (MC's time/energy/grades/sleep/appetite, Monika's access, Matsuda's claim, Asahina's self-image, Tsubaki's routines, Sam's information access, Mom's health).

See [[enter-m-voice-fingerprint]] and [[enter-m-character-voices]].
