# ENTER M — Forced-Conundrum / Punished-Choice Audit

Status: swept August 10, 2026. Revised the same day against author intent.
**Read-only as to script content — the only edits made were comments,
docstrings, and the route-gating logic, all listed in "Changes made" below.**

## What was searched

Instances where **the game forces a moral conundrum on the player and then
punishes them for choosing the intuitive option, or for choosing the only
option available.** Three parts, all required for a Tier A finding:

1. **Forced.** The player cannot decline, skip, or route around the decision.
2. **Moral.** The options differ in what kind of person you are being, not in
   whether you pressed the right button.
3. **Punished.** The outcome retroactively frames a reasonable answer as a
   wrong one.

Two distinctions do most of the work in this document:

- **An unhappy outcome is not a punishment.** Tragedy the player watches is
  craft. Tragedy the player is *blamed for*, after being given no honest
  alternative, is the thing catalogued here.
- **Who the second person is aimed at.** Most of the apparent findings in the
  first pass of this audit turned out to be cases where a story addresses its
  *protagonist* as "you" and a reader can mistake that for being addressed
  themselves. That is a legibility question, not a fairness one — but it is the
  single most common way this project *looks* like it is doing the bad thing
  when it is not.

### Scope

| Path | Covered |
| --- | --- |
| `game/story/season1/*.rpy` (0515–0531, exam_guard, s1_choices, s1disc) | yes |
| `game/story/out_of_context/*.rpy` | yes |
| `game/addons/Character Stories/*.rpy` (all 11 + `char_stories.rpy`) | yes |
| `game/addons/Matsuda's Sick Boss Fight/` (incl. `monikamode`, `kotonohamode`, `tsubakimode`) | yes |
| `game/addons/Archivist Invasions/`, `game/addons/Arcade/games/` | yes (see note) |
| `game/lost_records/`, `game/splash.rpy`, `game/screens.rpy`, `game/dev.rpy` | yes |
| `game/story/season2`, `season3`, `seasonintermission` | empty — n/a |

`ag_trial.rpy` (Nonstop Rebuttal) exists only as `ag_trial.rpyc.bak`; the source
is not in the tree, so its MISTRIAL ending could not be verified and is excluded.

---

## Tier A — the full pattern

### A1. Exam save-scumming — terminal punishment for standard VN behavior
`game/story/season1/exam_guard.rpy`

**The one finding that survives review unchanged, and the strongest in the
project.** Rolling back or reloading after a wrong answer is the most normalized
interaction in the genre. Here it is a moral offense with an unrecoverable
penalty.

- **Offense 1** → the home confrontation. Mom at `:414`: *"I cannot protect you
  from the part where you chose this twice."*
- **Offense 2** (`exam_guard_should_bad_end()`, `:125` — threshold is **2**) →
  `label exam_guard_bad_ending` at `:754`: *"Through your dishonesty, you have
  derailed this story beyond repair. The route cannot continue from here."* …
  *"**I am disappointed.**"* Then `renpy.full_restart()` at `:776`.
- The lock is **persistent, not save-local**. `exam_guard_bad_ending_locked_load`
  (`:779`) rejects any load that isn't from before May 26 — a second full restart
  at `:794`.

**In fairness, the trigger is engineered carefully.** `renpy.block_rollback()`
fires at each checkpoint so rollback is *prevented* rather than punished;
`exam_guard_has_mismatch()` (`:155`) returns `False` when either key is missing,
so loading a pre-exam save is safe; detection is date-gated to May 26–28.

**Verdict:** the narrowness makes the rule fair. It does not make the penalty
proportionate — the player loses the run, and the last thing the story says to
them is that it is disappointed in them personally. Worth noting the asymmetry:
the in-fiction offense is cheating on a school test; the out-of-fiction behavior
punished is pressing Load. This one is left standing as a genuine open question.

### A2. Monika mode — kindness is the losing move, and the finale is rigged
`game/addons/Matsuda's Sick Boss Fight/monikamode/monika_date.rpy`

Monika is *"genuinely, earnestly trying to have a nice evening"* (`:6`). To win
you must reject her, coldly, on a 2.8→1.5s timer. Warmth **heals her**; so does
hesitating. The header names the intent: *"that dissonance teaches the player to
be cruel."*

Tier A by construction and almost entirely earned — it is an anti-dating-sim and
the discomfort is the text. **One residual issue, and it is mechanical rather
than thematic:** the Last Resort is rigged and says so only in the comments
(`:50`) — *"RIGGED (untold): the deck never shuffles here, so the correct answer
is ALWAYS the top option."* Options shuffle every prompt for the entire fight
(`:29`), training the player to read fast under pressure; the finale silently
stops shuffling and scores them on a rule they were never told changed. That
punishes the exact skill the fight spent twenty minutes teaching.

### A3. Tsubaki mode — three moral routes, one identical fall
`game/addons/Matsuda's Sick Boss Fight/tsubakimode/tsubaki_soul.rpy`

VIOLENCE, PACIFISM, BETRAYAL (`:52`–`:57`), with pacifism the most expensive to
reach — every earned SPARE spends the whole bar to cut one thread, and the grip
*"clamps back down for the next."* Then (`:66`): *"**AND THE OUTCOME IS THE
SAME.** … Same physics every route. Only the words differ."*

**Verdict: deliberate and coherent — the point is that she was never yours to
save,** and both mid-fight cinematics are built on "completely out of Tsubaki's
control." Kept in Tier A only because it is the cleanest *structural* example in
the project of a moral question asked with real mechanical cost and then
discarded. No change recommended.

### A4. The dependency route — by design, and now gated to match
`game/story/season1/0523.rpy` (`:191`–`:297`), `game/story/dependency_route.rpy`,
`game/story/out_of_context/ooc_1224_unasked.rpy`

This pattern **on purpose**. The contract requires the substitution branch be
*"the better-written scene: faster relief, warmer payoff, visible gratitude"* and
that *"a blind player should finish it believing they found the most attentive
way to care for her."* The culmination (`ooc_1224_unasked.rpy:5`, `:7`) then
tells the player they became *"the narrative replacement"* and *"arguably worse
than Sam"* — **"even if you meant well."**

What makes that legitimate rather than a trap is the gate, which was **changed on
Aug 10** from a threshold to an unbroken chain:

- **All boxes or nothing.** The route requires the substitution branch at *every*
  insertion. Any different menu option — or any other deviating action the route
  watches — calls `dep_break()` and ends it permanently for that playthrough.
- **No partial credit, no recovery.** `dep_take()` after a break records a nice
  thing MC did, not a step back onto the route.
- **Still abortable at the very end.** `ooc_1224_unasked.rpy:14` — two of three
  final options end it and rewind to after the culture festival.

A threshold would have convicted a player of a pattern they only partly chose.
All-or-nothing means the ending is only ever addressed to someone who chose
substitution *every single time*, which is the only footing on which "you became
the replacement" is a fair thing to say to anyone.

**Guardrail now in code:** `DEP_MANIFEST_COMPLETE` is `False` until `DEP_REQUIRED`
lists every insertion in the finished story, so the unfinished chain cannot fire
the Dec 24 skip early. Every new insertion must add its key.

---

## Reviewed and cleared

These were flagged in the first pass and are **not** findings. Recorded with the
reasoning so the same false positive isn't re-raised later.

### C1. Purgatorium — the contempt is Sam's, not the player's
`game/addons/Character Stories/cs_sam_01.rpy`

The first pass read Day 7's accusations (*"You skipped my dialogue"*, *"You only
moved when Desire moved"*, *"Not by accident"*) as aimed at the person holding the
mouse. **They are aimed at Sam.** The player is playing *through* Sam — the
corridor is his session — and every accusation has a matching Sam-room interlude
that already showed him doing it:

| Day 7 line | Interlude |
| --- | --- |
| "You skipped my dialogue" | `:1184` — he scrolls back and skips everything she said about herself |
| "You screenshotted me on Day 1" | `:1186` — "He screenshots it for later" (already cross-referenced at `:1082`) |
| "You checked my profile. Height. Weight. The third number." | `:1285` — he opens her stat page |
| "There was a girl in your phone. She sent you five messages." | `:1384` — he deletes the thread unread |

The back half was never ambiguous at all — *"There was one before her. And one
before that"*, *"You don't remember their names"*, *"You designed them not to"* is a
serial-predator portrait no reader mistakes for themselves.

Two things created the misreading, both now fixed: a header comment claiming
`purg_skip_mode`/`purg_stat_popup` *"simulate the PLAYER'S behavior"* (they replay
**Sam's**, and nothing in the file measures the player at all), and the absence
of any anchor at the top of Day 7 naming who is being addressed.

### C2. Hina's World — a canon event, not a player-driven one
`game/addons/Character Stories/cs_asahina_01.rpy`

The first pass read the required games as an accelerant the player is then shown
the receipt for. **This is canon:** it happened to Asahina when she was nine,
years before Chapter 0.5. The player is coming across the record of it, not
steering it. The ending cannot be avoided because the part where anyone could
have intervened was over long before the desktop boots.

The axes were never authorship. They govern how much of the record surfaces and
in what voice — which log files exist, how plainly the diary says it, how far the
desktop has rotted at log-off. The horror is watching the whole shape of a
finished thing from outside and having it go exactly where it went.

The mechanics needed no change; several comments did (`"how much you pushed her
there"`, `"how you find out you helped"`, `"only if YOU let her go there"`) and
have been re-aimed. The existing guardrails were already right: `HW_GRACE` (`:199`)
means browsing alone triggers nothing, three of seven games are optional,
persistence never gates on `hw_guest`, and Mr Toast & Mochi never sours.

### C3. Kotonoha's attention checks — a Nier Replicant homage with a job
`cs_kotonoha_01.rpy` (checks at `:91`, `:219`, `:342`, `:442`, `:563`, `:674`,
`:862`; fail label `:1067`) · `cs_kotonoha_02.rpy` (23 fail-jumps)

Direct homage to Nier Replicant, which does this to its reader. The working
purpose is to catch the two readers the story can't survive: the one holding
down skip, and the one who walked away with it running. Both get the same
answer — the narrator stops telling it.

Read that way the design is pointed rather than punitive: a story about a girl
nobody actually listened to declines to continue for someone who isn't
listening. The questions are all about *her* (what was behind her eyes; the word
the old man kept returning to), never plot mechanics, so a present reader has
nothing to fear from any of the seven. Failing is explicitly not an ending —
`:1056` marks the real one and notes the failure below it isn't one.

Note retained: `ADDONS_AND_SIDE_CONTENT_OPINIONS.md:310` argues against these on
craft grounds. That's a live disagreement about execution, not a fairness
finding, and it is left as-is.

### C4. Declining the content warning — fixed
`game/story/season1/s1disc.rpy:20`

Previously `renpy.quit()`; now `return` to the main menu. A content warning whose
only honest answer closes the application isn't offering a choice. Resolved.

### C5. Illusory choice without punishment

- **`cs_tsubaki_01.rpy:116`** — the coin flip. *"It does not matter what either
  of us called. It came up tails."* The irrelevance is the thesis (*"A coin
  cannot want. That is why I trusted it"*), stated to the reader's face rather
  than sprung on them.
- **`cs_matsuda_02.rpy:127`** — "I want to leave." → `renpy.quit()`. In
  character, and the sibling option `"...Never mind."` (`:120`) exits gracefully.
  Low stakes; noted only because the two exits sit in the same menu.
- **`splash.rpy:711`** — save deletion. Destructive but explicitly labelled.
- **`inv_horror.rpy:2375` / `inv_biography.rpy:2724`** — ordinary retry menus.
- **`ooc_0604`, `ooc_1026`, `ooc_1030`** — `s1_pick` stance menus. Clean.
- **Purgatorium's menus** (`:1096` walk-away refused, `:1675`/`:1683` the same
  string twice) — these are the bootleg game denying *Sam* an exit, which is the
  form working as intended.

---

## The main-story contract

`s1_choices.rpy` now states the rule and its exceptions together:

> No branch may change an event, a location, who is present, or what anyone
> decides. If deleting the menu would change the plot, it is the wrong menu.
> … these choices are never punished, because the story is not asking the player
> to guess.

The main story is not choice-driven and isn't becoming choice-driven. Where a
player action reaches the plot at all it should change the **order** things
happen in, not whether they happen. Anything that genuinely branches gets its own
store and its own contract — currently only the dependency route. All twelve
main-story keys and four OOC keys were checked and hold. The exam menus
(`0526`–`0528`) come closest: wrong answers stay wrong, but `s1_exam_mark()`
(`:147`) only colors a couple of later lines and its docstring is explicit that
*"nothing reads this to punish the player."*

---

## Summary

| # | Where | Status |
| --- | --- | --- |
| A1 | Exam save-scum guard | **open** — fair trigger, disproportionate penalty |
| A2 | Monika mode | mostly earned; **the untold rigged finale is the real issue** |
| A3 | Tsubaki mode | deliberate; convergence is the theme. No change |
| A4 | Dependency route | deliberate; gate rewritten to all-or-nothing |
| C1 | Purgatorium | cleared — aimed at Sam; comments + Day 7 anchor fixed |
| C2 | Hina's World | cleared — canon event; framing comments re-aimed |
| C3 | Kotonoha checks | cleared — Nier homage / anti-skip; intent documented |
| C4 | Content-warning decline | fixed — returns to menu |
| C5 | Illusory-choice set | cleared |

**Two things actually want attention:** the exam guard's penalty (A1) and Monika
mode's undisclosed rule change in the Last Resort (A2). Everything else is either
working as intended or was a documentation problem, now fixed.

---

## Changes made

Comments, docstrings, and one gating rewrite. No prose was cut and no scene
behavior changed except where noted.

| File | Change |
| --- | --- |
| `game/story/dependency_route.rpy` | Threshold gate → unbroken-chain gate. `dep_share()` → `dep_break()` (irreversible); added `DEP_REQUIRED`, `DEP_MANIFEST_COMPLETE`, `dep_intact()`, `dep_missing()`; dropped `DEP_ROUTE_THRESHOLD` and `dep_shared`. Switched to the `global` store idiom used in `exam_guard.rpy` |
| `game/story/season1/0523.rpy` | Insertion header documents the all-or-nothing gate; collaborative branch now calls `dep_break()` |
| `game/story/season1/s1_choices.rpy` | Added "THE EXCEPTIONS" — order-not-outcome rule, dependency route named as the only current exception |
| `game/story/season1/s1disc.rpy` | Comment recording why declining returns to menu rather than quitting |
| `cs_sam_01.rpy` | Header: `purg_skip_mode`/`purg_stat_popup` replay **Sam's** session, not the player's; added a "WHO THE 'YOU' IS" block with the accusation→interlude map. **Script:** a four-line anchor at the top of Day 7 naming Sam and grounding it in the Day 6 interlude |
| `cs_asahina_01.rpy` | Header: "THIS ALREADY HAPPENED" (canon, age nine) + "WHAT THE CHOICES ACTUALLY DO" (record, not authorship); three inline comments re-aimed off "you pushed her there" |
| `cs_kotonoha_01.rpy` | Header: "WHY THEY EJECT YOU" — Nier Replicant homage, anti-skip/anti-AFK purpose, and why failing isn't an ending |
| `cs_kotonoha_02.rpy` | Header pointer to the above; both files governed by one note |
