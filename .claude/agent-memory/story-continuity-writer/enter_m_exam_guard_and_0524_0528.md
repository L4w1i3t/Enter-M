---
name: enter-m-exam-guard-and-0524-0528
description: State of ENTER M days 0524-0528 and the exam_guard save-scum punishment system
metadata:
  type: project
---

**Voice state of 0524-0528 (as of 2026-06-16 pass):** These five target days were already very strongly voice-matched to the 0515-0523 baseline before I touched them. They follow the restraint rule, show MC's unreliability behaviorally, let beats breathe, avoid meme slang, and use established callbacks ("sidewalk traffic," cup/open-door handout, "joint custody," Kotonoha's deadpan, pasta-salad-as-salad). Drift was minimal and localized, NOT pervasive. Do not assume these need heavy rework in future passes — they are near-baseline. Standout strong scenes: 0524 rooftop Monika invitation + poem exchange; 0525 library study + Mom pocket-call + Asahina recycled-packet study; 0528 ice cream ending.

**exam_guard.rpy** (`game/story/season1/exam_guard.rpy`, new untracked file): a meta anti-save-scum system spanning the May 26-28 exam days. If the player reloads to retry an exam answer (save-scum), `exam_guard_checkpoint_or_jump` detects the mismatch and jumps to a `a05XX_<subject>_save_scum` label where a teacher catches MC "revising an answer without time, process, or permission" → zero for that subject + `did_save_scum_<subject>` flag. Subjects: civics/la (0526), biology/chemistry (0527), algebra/english (0528). Consequences escalate:
- 1 scummed subject → `exam_guard_home_confrontation` (Mom confronts, grounding).
- 2+ → `exam_guard_should_bad_end()` true → `exam_guard_home_repeat_confrontation` (Mom's rawest scene) then `exam_guard_bad_ending` (Nier voice ejects player to title; route "broken").
Each exam day branches every after-section nier block, lunch, and evening on `persistent.did_save_scum_*` / `persistent.exam_save_scum_subjects`. PRESERVE all `exam_guard_*` python calls, checkpoint labels, and persistent flags — they are load-bearing game logic, edit only prose inside quotes.

**Mom confrontation registers (REWRITTEN 2026-06-17, supersedes the 2026-06-16 notes below). The two scenes are now deliberately differentiated:**
- `exam_guard_home_confrontation` (FIRST offense) = a furious mom CLAMPING DOWN. She keeps her voice level on purpose ("I'm going to keep my voice down. Not for your sake. Because if I start, I won't be fair"), speaks in precise lawyerly complete sentences, no yelling/profanity; the rage is in the precision and the physical tells; the COST is revealed at the very end — she'd been shaking the whole time, held on purpose. Removed the prior "GODDAMN"/f-bomb/"STOP STOP"/caps yelling.
- `exam_guard_home_repeat_confrontation` (2+ offenses, bad-end path) = composure THROWN ASIDE. Explicit hinge line: "Last time she kept her voice in a box. Tonight the box is open, and she is not putting anything back in it." Volatile, colloquial, fragmented, loud-then-broken; profanity OK ("Put your shit down"); the lawyer voice visibly in pieces; the grief breakdown ("I love you so much it is making me stupid… and I don't know if I can trust you").

**Other 2026-06-17 exam-arc edits:** All 6 caught-cheating catch scenes deepened, each tying despair to that subject's material (bio=contamination, chem=controlled-reaction-needs-control-first, algebra=sign-error-vs-choice, english=unreal-past/real-present, civics=clean-record-deleted/asterisk, la=can't-bury-himself-in-grammar). Exam questions reshuffled so the correct answer is no longer always the top option (4 moved per exam across 0526/0527/0528) — checkpoints key off the question, not option order, so this is SAFE. **0525 was substantially REWRITTEN this session** (exam-arc seeding; rote drilling compressed to montage) — it is no longer "near-baseline untouched"; the line-8 note above describes the 2026-06-16 state.

**Earlier 2026-06-16 edits (historical, exam_guard.rpy):** repeat-confrontation toned doubled "pissed"; normalized "?!?!" -> "?!"; bad-ending Nier line cleanup. Largely overwritten by the 2026-06-17 rewrite above.

See [[enter-m-session-2026-06-17]] for the full session, [[enter-m-character-voices]] for Mom's register, [[enter-m-voice-fingerprint]] for restraint/Nier/music/fragment rules.
