# ENTER M — Annotation Apply Log

Record of the pass that **applied** the three stacked annotation passes
(`# REVIEW`, `# REVISION`, `# REPETITION`) to the main story, rather than
adding more notes. Started 2026-07-27.

The annotation comments were deleted as each was applied, per the decision to
let the files come out clean. `# SFX SUGGESTION`, `# SEED`, `# TODO`, and
ordinary authoring comments were kept. The three source documents
(`BLIND_PLAYER_REVIEW.md`, `REVISION_ANNOTATION_INDEX.md`, the four
`MAIN_STORY_REPETITION_*.md`) are untouched and remain the record of *why*.

## Decisions taken before the pass

| Question | Answer |
|---|---|
| Scope | Prose edits **+** the 17 agency insertions **+** the mechanic/contract fixes |
| Annotations | Delete as applied |
| Monika's camera line (0515) | **Dormant** — staging softened; Day 1 now ends on the unresolved food detail instead of a second meta beat |
| Matsuda's 0531 backstory | **Sideways off the TV thread** — no "Why are you trying so hard?", she never names her own pattern |

## New files

- `game/story/season1/s1_choices.rpy` — the converging expressive-choice
  store (`s1_pick` / `s1_stance` / `s1_was`), plus the 0518 showtime helper.
  Header carries the rule: no branch may change an event, a location, who is
  present, or what anyone decides.

## Landmines (done first)

- **`0519.rpy` ended with a live `return` above `jump a0520`.** May 20–31 were
  unreachable in normal play. The whole leftover temp block (already-commented
  author stop-note and all-content unlock) is gone; the day now falls through
  to `a0520`.
- `0531.rpy` end-of-chapter unlock is now a **curated explicit list** of the
  seven shipped stories instead of a loop over the catalog, so a story added
  later cannot arrive pre-unlocked. Dead `_all_on` copy-paste removed. The
  announcement now names real titles and states the Heads-then-Tails order.
- `char_stories.rpy`: the init-10 master pass that flipped every story flag
  whenever `archive_unlocked_character_stories` was set is now
  `config.developer`-gated. Without this the curated 0531 unlock would be
  undone on the next launch. Section gate and per-story flags are now separate
  concepts.
- `s1disc.rpy` unlock was already dev-gated; left as is, comment rewritten.

## Per-file

### `s1disc.rpy`
- Loaned the trailer's shape-of-loss forward as the fourth notice line
  ("...the people you are about to meet are happy right now. I would like you
  to notice it while it is happening."), **replacing** the procedural
  "Proceed only if you accept what you have just been told" rather than
  stacking on top of it (D-10).
- De-fanged the punitive "will not stop to warn you a second time" (CLARIFY
  FUNCTION), cut "Understood. Thank you for your cooperation." (D-12
  institutional phrasing) and "Make the most of your time here." (D-11 second
  notice ending). Kept the date span + the road image.
- Trailer stays at the end of 0531 where its placement is correct.

### `0515.rpy` (781 → 378)
- Camera line staged small: the 4.0s ceremony before it is now 1.0s and she is
  still mid-cleanup, so it reads as deniably aimed at the card. Line itself
  intact.
- **Day-1 ending replaced.** The routine sign-off is gone; the day now ends on
  Asahina's plate already rinsed and face-down in the rack and a paper towel
  laid flat over the bin. No interpretation attached.
- Two agency menus: the movie-invite reply (joke / plain / almost-says-it) and
  the dinner plate (mirin joke / say nothing / name it).
- "Fatass" cut — the abrasive rhythm stays as a cashier jab, her over-reaction
  to a *non*-body joke now does the work, and MC's exit shortens to a retreat
  instead of a second food joke. With the body punchline gone, the glue
  innuendo no longer stacks on the audition day, so it stays.
- Trims: 15.03 fatigue caption, 15.04 two critique jokes, 15.05/15.06/15.08
  transition scaffolds, 15.09 routine ladder, 15.10 university-pressure
  triple, 15.12/15.13 montage inventories, 15.15 glue-deal logistics,
  15.16 four-exit ending, crossword/"the color" second diagnosis.
- Copy: "What do you want me to do about it?" → "And what exactly am I
  supposed to do about it?" (15.01, protects the camera line); two "before I
  can" recast (A-X3); "drink some water, take my medication" (15.14).

### `0516.rpy` (918 → 414)
- **Club-regulars continuity fixed**: Monika now accounts for Hikari and
  Homura ("cram school on Fridays, and Homura goes wherever Hikari goes"), so
  0520 does not introduce them as unexplained regulars.
- Copy: "The only think of note" → "thing" (16.14); triple "same" reduced.
- Teacher voice: "Come on, it's a layup!" → plainer diction (VOICE/SETTING).
- Trims: 16.01 personification pile-up, 16.02 double command, 16.03 glue
  breakfast recap (now one line), 16.04 punchline stack, 16.05 hostile-algebra
  metaphors, 16.06 double validation, 16.08–16.09 transition captions,
  16.10 triple hedge, 16.11–16.13 critique repeats, 17.10 Sunday-plan volley,
  16.15–16.17 Kotonoha captions, 16.18 context-clue joke, 16.19 Sam triple
  read, 16.21 calibration proofs, 16.24 planner framing.
- Sam KEEPs protected: the mirrored handshake scan and the "eating better"
  kitchen beat are untouched. His "He says it lightly" caption became an
  action (19.16).
- Second "face" joke made a conscious callback ("You did the face thing
  again") so it reads as family idiolect, not a fresh punchline (A-X5).

### `0517.rpy` (981 → 449)
- Two agency menus: Monika's corridor silence (step into it / step around it)
  and handing over the contact info (grudging / play along / just hand it
  over). Both replace narration that made the choice for the player;
  "Probably for the best." is gone.
- Trims: 17.01 Saturday-oppression formulations, 17.02 glue thread reminders,
  17.03 traffic simile, 17.05/17.07 civics answer key, 17.06 "committed
  metaphor", 17.08 bell/crowd double staging, 17.09 corridor errand recap,
  17.11 Kotonoha diagnosis, 17.12 gratitude re-show, 17.13 game restraint
  analysis, 17.14/17.15 walk set-up, 17.16 narrated apology count,
  17.17–17.21 introduction summaries, 17.23 second exit + third phone screen
  (merged into one thread), 17.24–17.26 debrief ladder, 17.27 double "rest of
  the night", 17.28 bedroom character summary, 17.29 forgotten-school
  aftermath.
- Roster thoughts rewritten to hold **durable facts** (names, transfer, what
  each was observed doing) instead of restating the scene's reading (A-X1).
- Copy: "Civics always feels easy; that is the dangerous part" (17.04).

### `0518.rpy` (1162 → 465)
- Two agency menus: the **showtime** (noon / a couple hours later / evening —
  it now actually reshapes four time-of-day lines via `s1_pick_movie_time`),
  and the post-movie goodbye (plain thanks / the joke / the true one), which
  replaces the narrated menu and "my brain files all of them incorrectly."
- **Popcorn continuity fixed**: the "extra large bucket, as insisted" recap is
  gone; the order stays a medium.
- Trims: 18.01 second girlfriend tease, 18.03 six-beat transition, 18.04
  three-line button, 18.05 shoulder pre-reminder, 18.06 kids' debate,
  18.07/18.08 hype and availability recaps, 18.09–18.15 lobby captions,
  18.16 metaphor dosage, 18.18 cinnamon volley, 18.19 normal/not-normal
  thesis, 18.20 duplicate film criticism, 18.21 second explanation for his
  stillness, 18.23 timing lecture, 18.24 employee-policy riff, 18.27 essay
  exchange, 18.28 pause simile, 18.29 landing caption + double ending,
  18.30–18.32 bus inventory, 18.31/19.24 second praise landing, ending stack.
- Sleeve gesture chain kept exactly as staged (review exemplar); only the
  captions around it were cut.
- Copy: tangled "particular darkness, like any other theater" rewritten;
  duplicate "That's not what I said" varied (18.17); the runaway "Aww"
  shortened (TONE/UI); credits "sacred ritual" varied (18.22).
- One tenant metaphor kept across 0518/0519 — "rented space" lives here
  (19.05).

### `0519.rpy` (1154 → 403)
- **Foot injury seeded**: "The foot I came down wrong on at practice two weeks
  ago", so "better than it was last week" no longer assumes knowledge the
  player doesn't have and can't be confused with Saturday's shoulder.
- **Cinnamon continuity** cut — it could not survive a night, a shower and a
  commute; the date motif no longer forces its way into lunch.
- Agency menu at the treasure beat: "Okay, stop." / "Take it down about forty
  percent?" / (Ride it out). All three converge — she drops the bard voice
  regardless — but in the third she reads his silence instead of being told,
  which is the same lesson landing without him having to say it.
- Matsuda now **stays** in her quieter register through the goodbye
  (BOUNDARY CONTINUITY); the bard diction no longer returns two lines after
  she agreed to drop it.
- Curriculum echo cut entirely here (the ponytail/fitting-room mapping): the
  Matsuda hallway scene twenty lines later already teaches it, and the May 21
  omitted-agency lesson is the one keeping its resonance. This also stops MC
  from stating the underselling diagnosis that Matsuda delivers later — which
  is now unsettlingly hers.
- Disability slur cut (no consequence followed it, per the note's own test).
- "I file it under nothing" now appears **once** (dinner).
- Trims: 19.01 four personifications, 19.02 double ceiling, 19.03/19.06 theory
  recap, 19.04 avoidance essay, 19.07 twenty-three-line foot exchange,
  19.08 printout re-teach, 19.09 commute inventory, 19.11–19.13 lesson
  delivery modes and quiz coda, 19.14/19.17 lunch recap and fatigue
  diagnosis, 19.19 corridor restaging, 19.20 duplicate hail, 19.21–19.22
  boundary over-proof, 19.23 triple-explained exit, 19.25–19.28 dinner
  debrief, 19.29–19.31 evening theses, 19.34 doubled "for tonight".
- Copy: orphan "I much prefer if she played hookey" cut; the damaged
  "five-minutes-that-felt-like-it" and the authorial "that motif" rewritten;
  glowing-rectangles image limited to screens.

### `0520.rpy` – `0525.rpy`
Same treatment, hand-rewritten day by day. Highlights:
- **0521** keeps the omitted-agency literature lesson (the one thematic echo
  the checklist elects to survive) but loses its italic answer key; missing
  verb fixed ("my clothes smell faintly of rubber"); the cup-conspiracy call
  compressed to its four load-bearing beats.
- **0522**: "reach" → "reach for it"; **club-mediation choice** (start with
  what Homura meant / with what Hikari heard) — MC's most active scene is now
  the player's; bell-continuity wobble named (homeroom vs final).
- **0523**: the two highest-value insertions — **Himeko's "what do you feel
  first?"** (relief / that I'd be bad at it / guilty, all arriving at the
  "space" answer) and the **Matsuda callout tone** (flat / kind / joking-firm,
  outcome untouched: she is told, she apologizes, she changes). Copy: "which
  my Azure Eye hungers for", "puzzledly", the orphaned "how stressed was she?"
  now answered, "fifteen minutes apart".
- **0524**: the poem is **relined to six actual lines**, so "It's only six
  lines" is now true on screen; the thesis-inheriting couplet is gone and the
  prompt no longer hands both poems their own conclusion. **Poem-revision
  choice** (vinyl / warmth / spring) — whichever closing image the player adds
  is the draft from then on, and May 31 quotes it back. "six and a half lines"
  → "eight lines". Tsubaki's roster entry no longer confirms her crush.
- **0525**: the review's #1 named target. Ten emotional landings reduced to
  four (the integrity speech, the keystone beat, distance-vs-disappearance,
  and the station goodbye); every event kept — study session, cafe, Kotonoha,
  the Asahina tutoring scene (protected wholesale), the jog, the pocket-dial.
  **29.8% shorter.**

### Exam week — `exam_guard.rpy`, `0526` – `0528`
The review's #1 structural complaint. All three halves of the fix are in:

1. **The rule is stated before anything arms.** The civics proctor gives the
   in-world version ("an answer is final once it is marked... a paper that
   leaves this room and comes back different is a different paper"), then
   nier gives the player the other half in plain language: saving, quitting
   and resuming are fine; going back to an answer you already marked is not;
   and the whole exam period can be restarted from before the first paper.
   `exam_guard_begin_exam_period()` and the first checkpoint now run *after*
   that block. "The exam remembers" is finally a callback instead of a reveal.
2. **Wrong answers stay wrong.** All 54 branches across the three days were
   rebuilt: a wrong pick no longer self-corrects in MC's head. He commits to
   the mark and moves on, and `s1_exam_mark()` records it. This is what makes
   the reload temptation real and therefore the mom scenes earned.
3. **Routing bug fixed.** `exam_guard_home_confrontation` dispatched to the
   *repeat* scene on the bad-end count, so two catches in one day could make a
   player's **first** confrontation the one full of "last time" callbacks —
   and the normal scene's two-subject variant was unreachable. Dispatch now
   keys on `persistent.exam_guard_confrontations`, so the first time is the
   first time and the repeat scene only runs when there was a previous one.
4. Bad-end copy aligned to the actual two-catch threshold ("Two stops being an
   accident and starts being a shape you chose").
5. `0526`: civics teacher's "His voice" → "Her voice"; the study-guide
   lampshade and the language-arts answer-key reminder cut.
6. `0528`: MC's caught-route "...What?" — the clearest dialogue symptom of the
   old entrapment — becomes "I know exactly what he is asking. That is the
   whole problem." / "...I'd rather not." He was told the rule on Monday.
7. Himeko's confrontations: threat-classification and fear-naming stacks
   trimmed per the hard-cut spine. Her anger is untouched.

### `0529` – `0531`
- **0529**: Copper Crown compressed to its four load-bearing beats (family
  texture, the deck-thinning advice, the work call, the Sunday pact); the
  post-exam relief triple at the open and the closing ledger trimmed.
- **0530**: the train poem is no longer paraphrased in the line before the
  player reads it; duplicate "The joke lands" / "plain enough to" varied.
- **0531** — **the Matsuda backstory is now passive.** "Why are you trying so
  hard?" and the whole dossier are gone. Her transfer, the timing, and the
  old-school social difficulty now leak sideways out of the TV-show thread at
  the dinner table, tossed off between jokes ("...enough for everyone at that
  school to have a full opinion about me by lunch. You know how that goes."),
  with the napkin doing the work her voice refuses to. **She never names her
  own pattern** — "making friends and keeping them are different jobs" and
  "I keep pushing after it stops helping" are cut entirely, so her later
  overdependence can still surprise her. The two-person table beat shrinks to
  "Was today okay?" → MC actually answering it.
  Also: the **arcade-invitation choice** (plain / behind the racing game /
  almost doesn't) — how he offers, never whether; the May 24 poem line quoted
  back before "The door is already open"; Matsuda's roster entry rewritten to
  hold only what she actually let slip.

## Measured result

Comment-stripped script lines, May 16–31 (May 15 was rewritten before the
baseline snapshot was taken, so it is excluded from the arithmetic):

| Range | Cut |
|---|---|
| 0516–0525 (fully hand-rewritten) | **7–30%**, avg ~12% |
| 0525 alone (the review's named target) | **29.8%** |
| 0526–0531 + exam_guard | ~1% — see below |
| Whole span | 7.3% |

## What is NOT done

Honest accounting. The exam-week and finale files (`0526`, `0527`, `0528`,
`0529`, `0530`, `0531`, `exam_guard`) received **every mechanic, contract,
agency, continuity and copy fix their notes called for**, and their annotation
comments are gone — but their bulk *prose-redundancy* trimming is only
partially applied. The specific named cuts were done; the long tail of
"third joke / second explanation / scene-ending inventory" trims in those
seven files was not, which is why their percentages are ~1% rather than the
10–20% the earlier days hit.

The source documents remain in the repo, so the outstanding work is still
fully specified — but the inline notes that pointed at it are gone from those
files. The relevant sections to work from are:
`MAIN_STORY_REPETITION_DETAILS_0525_0528_EXAM.md` (C-93 onward, and the
`exam_guard` C-170 to C-218 block) and the May 29–31 entries in
`MAIN_STORY_REPETITION_AUDIT.md` (D-101 to D-123).

---

Matsu'Py lint verified clean after every step.
