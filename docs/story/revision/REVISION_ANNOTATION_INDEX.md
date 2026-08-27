# ENTER M - Second-Pass Editorial Annotation Index

Status: annotation-only pass completed July 20, 2026.

This pass responds to the continuing blind-reader complaint that the main story often lands a
beat successfully and then explains it again. It supplements `BLIND_PLAYER_REVIEW.md` and
`REVIEW_FIX_CHECKLIST.md`; it does not replace the earlier notes.

No dialogue, narration, menus, labels, state updates, or Python/Matsu'Py logic were changed during
this pass. All 571 targets are standalone comments whose first line begins `# REVISION [`.

## Finding the notes

```powershell
rg -n '^\s*# REVISION \[' game/story/season1
```

To inspect one category or idea:

```powershell
rg -n -i '^\s*# REVISION .*?(TRIM|REDUND|VOICE|CONTINUITY|AGENCY|KEEP)' game/story/season1
```

Continuation lines belong to the nearest `# REVISION [...]` line above them. Each note is placed
immediately before the passage it evaluates.

## Third pass: repetition notes (`# REPETITION [`)

A later annotation-only pass (July 26, 2026) carried the four
`MAIN_STORY_REPETITION_*.md` audits into the same files under a separate tag, so the two
passes never collide:

```powershell
rg -n '^\s*# REPETITION \[' game/story/season1
```

Each note reads `# REPETITION [<id> | <priority> | <status>] <file>:<lines> <source-doc>`, where
the source doc is `<AUDIT>`, `<D0515-0519>`, `<D0520-0524>` or `<D0525-0528>`. Every file also
gained a header block listing the corpus-wide patterns (G1-G13 and the cross-file catches) that
land in that file, with this file's own line numbers. Line numbers in the notes are the
pre-insertion numbers the audits cite; the notes themselves sit directly above their passage, so
use the note position rather than the quoted number when editing.

Precedence between the two tags: a `# REPETITION` note is an aggregate judgment (this beat is the
Nth time the story has done this job), while a `# REVISION` note is local. When both touch a
passage and disagree, the aggregate one usually wins, because the local note could not see the
other eight occurrences.

## Coverage

| File | New targets | File | New targets |
|---|---:|---|---:|
| `0515.rpy` | 17 | `0525.rpy` | 42 |
| `0516.rpy` | 23 | `0526.rpy` | 21 |
| `0517.rpy` | 24 | `0527.rpy` | 24 |
| `0518.rpy` | 24 | `0528.rpy` | 30 |
| `0519.rpy` | 29 | `0529.rpy` | 26 |
| `0520.rpy` | 22 | `0530.rpy` | 39 |
| `0521.rpy` | 21 | `0531.rpy` | 62 |
| `0522.rpy` | 22 | `exam_guard.rpy` | 54 |
| `0523.rpy` | 39 | `s1disc.rpy` | 3 |
| `0524.rpy` | 49 | **Total** | **571** |

Every main-story day from May 15 through May 31 is covered. The pre-story notice and the story
prose inside the exam guard are covered as well.

## How to use conflicting notes

These are revision options, not automatic deletion orders. When a `KEEP` note and a trim note
touch the same scene, preserve the load-bearing action or line and trim the explanation around it.
Broad older notes that call a day or scene `KEEP` protect its event, outcome, or dramatic function;
they do not protect every sentence. The newer `RECONSIDER PRIOR KEEP` note in `exam_guard.rpy`
and `RECONSIDER THE PRIOR KEEP NOTE` at May 31's open-door ending explicitly supersede earlier
prose-level protection.

Use this order of precedence:

1. Fix continuity, copy, state-text spoilers, and player-contract problems.
2. Protect specific actions, objects, awkward pauses, and character-voiced lines that already
   carry the subtext.
3. Remove the narrator sentence that translates a successful gesture or line.
4. Remove the third joke, metaphor, example, or emotional landing after the dynamic is clear.
5. Compress repeated travel, class, practice, meal, phone, and cleanup transitions.
6. Add clarification only when the missing fact creates genuine confusion. Do not add another
   explanation merely because an implication is subtle.

The default question is not "Is this sentence good?" Many cut candidates are good sentences.
The question is "Is this still the first or best sentence doing this job?"

## The most common overexplaining ladder

The recurring sequence is:

1. A gesture or object shows the feeling.
2. Narration names the feeling.
3. Dialogue diagnoses the same feeling.
4. A joke or metaphor reframes it.
5. The scene closes on it.
6. A transition, recap, or character-thought update records it again.

Most scenes need one or two rungs, not all six. Prefer the most concrete and character-specific
version. A thought-ledger update should preserve a durable fact, not provide an authoritative
interpretation of a scene the player just read.

## Highest-density revision zones

- **May 24-25:** poem line-count continuity, poem/self-analysis repetition, date-scene landings,
  and several moments where a strong image is followed by its critical explanation.
- **May 26-28:** lesson/exam/study-guide repetition, self-correcting answers, hidden save/load
  rules, caught-route verdicts, and repeated guilt codas.
- **`exam_guard.rpy`:** Himeko's emotional logic is strong, but both confrontations define each
  accusation, gesture, and consequence several times. Preserve her sharpest formulations and cut
  the narrator's answer key. Fixing the unfair mechanic upstream does not exempt this prose from
  the trim.
- **May 29:** post-exam relief is repeatedly announced; Copper Crown should retain family texture,
  deck-thinning advice, the work call, and the Sunday pact while compressing turn-by-turn play.
- **May 30:** empty-chair imagery, Matsuda's effort, Tsubaki's assertion, and the club's return are
  each demonstrated and then summarized. The displayed train poem is also paraphrased before or
  after the player reads it.
- **May 31:** the capstone structure is worth protecting, but practice, racing, cabinet play,
  character-growth checklists, poem reminders, social goodbyes, and the final open-door image all
  receive multiple proofs or codas.

## Cross-file habits to audit during the actual rewrite

- Narrator phrases that announce restraint: a silence does not need to "perform," a moment is not
  made into a "lesson," a line needs no "decoration," or a beat carries only what it "needs."
  These formulations often explain that the prose is not explaining.
- Legal, administrative, evidence, filing, jurisdiction, contract, committee, and procedure jokes.
  They fit MC and Himeko in moderation, but repeated use makes siblings, classmates, and narration
  share one polished voice.
- Physical behavior immediately followed by mind-reading: tightened fingers, adjusted sleeves,
  delayed smiles, turned cups, lowered volume, or facedown phones rarely need a diagnosis.
- Classroom material that maps too perfectly onto the current plot, followed by an italic recap,
  followed again by an exam question.
- Scene-ending inventories: a strong last line is followed by cleanup, a thematic summary, a
  transition summary, and a roster-thought summary.
- Repeated ordinary-life reassurance after exams. One altered room, meal, or body sensation can
  establish decompression without a complete checklist of absent threats.

## Concrete catches worth fixing before a broad prose cut

- `0516.rpy` presents the club as a private Monika/MC space, but `0520.rpy` introduces Hikari and
  Homura as regulars without accounting for their earlier absence.
- `0518.rpy`: Monika orders medium popcorn, but a later recap calls it an extra-large bucket.
- `0519.rpy`: the foot is suddenly "better than last week" before the injury has been established;
  the overnight cinnamon-on-fingers image also needs a literal continuity check. The temporary
  author stop-note is a release blocker, and its following all-content unlock is not guarded by
  developer mode.
- `0521.rpy`: "My clothes faintly like rubber" is missing a verb.
- `0522.rpy`: one sentence uses "reach" where the physical action requires "reach for it."
- `0523.rpy`: MC's "how stressed was she?" is never answered; "puzzledly" is nonstandard;
  "objects" is unclear in the program description; the Portrait of Zahrath relative clause is
  ungrammatical.
- `0524.rpy`: the displayed poem has nine nonblank lines while narration calls it six and later
  six-and-a-half; a character-thought update prematurely confirms Tsubaki's roadmap-hidden crush;
  "I save twice" teaches prudent saving immediately before the hidden load punishment.
- `0525.rpy`: `MOOOOOOOOOOOM!.` has conflicting terminal punctuation. **FIXED**
- `0526.rpy`: the civics teacher is otherwise she/her, but one line says "His voice."

The most urgent agency-ordering catches are also local-annotation targets:

- `0526.rpy` arms `exam_guard_begin_exam_period()` and creates the first checkpoint before the
  proctor's warning. A fair contract must precede both.
- Wrong classroom/exam choices are overwritten by immediate corrections, so they cannot create
  the honest temptation the punishment assumes. Preserve selected mistakes if grades should matter.
- `0528.rpy` has MC sincerely fail to understand the rule while the teacher treats his awareness
  as obvious. This is the clearest dialogue-level symptom of the current entrapment problem.
- In `exam_guard.rpy`, two same-day catches route directly to the label named "repeat," so its
  "last time" callbacks can play during the first home confrontation. The normal scene's
  `_exam_guard_home_multiple` branches are consequently unreachable at the current threshold.
- The bad end fires at two catches, but "Anything past that ... becomes a shape you chose" assigns
  its chosen-shape language to a third catch. Align the prose with the actual threshold.
- If converging expressive choices are implemented, carry them forward: the 0517 contact-sharing
  tone must affect 0519's canonical interpretation, and a 0524 poem revision should be remembered
  in 0530/0531.

Search the local `# REVISION [...]` notes at each target before editing; they include the exact
competing lines and the intended keeper.

One checklist status has already moved: the pre-Day-1 all-content unlock in `s1disc.rpy` is now
behind `config.developer`, although the older checklist still shows it as open. That does not fix
the separate unguarded unlock after May 19 or the uncurated end-of-Chapter-0.5 unlock on May 31.

## Annotation-only audit

Before this pass, a SHA-256 fingerprint was recorded for every season-one script after removing
full-line comments. After all annotations were inserted, the same normalization produced identical
hashes for all 19 `.rpy` files. This verifies that the pass changed comments only, including in
`exam_guard.rpy`, where story prose and system logic share a file.
