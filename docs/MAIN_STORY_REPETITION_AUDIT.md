# ENTER M — Main-Story Repetition and Overexplanation Audit

Status: complete close-read audit, July 24, 2026.

## Scope and editorial standard

This audit covers the complete playable main-story sequence:

- `game/story/season1/s1disc.rpy`
- `game/story/season1/0515.rpy` through `0531.rpy`
- the story prose and alternate/repeat prose in `game/story/season1/exam_guard.rpy`
- the Chapter 0.5 trailer called by `0531.rpy`, in
  `game/addons/Next Time Trailer/next_time_trailer.rpy`

The May 15–31 day files contain about 70,000 displayed words. Including the
notice and exam-guard prose brings the reviewed total to roughly 74,200 words.
The audit reads the prose itself, not only the 571 existing `# REVISION [...]`
notes. Existing annotations are treated as leads and checked against their
surrounding scenes.

The question used throughout is not merely “Does this word occur more than
once?” It is:

> Is this the first, strongest, or most character-specific version of the beat,
> or is it another polished sentence doing a job the scene has already done?

### Finding labels

- **A — already annotated:** An existing `# REVISION` or `# REVIEW` note
  identifies substantially the same problem.
- **N — new catch:** This audit found a repetition or cumulative pattern not
  directly identified by the nearby annotations.
- **A+N — expanded catch:** A local annotation exists, but the audit found a
  broader word-, syntax-, gesture-, or cross-file pattern.
- **KEEP — intentional echo:** The recurrence creates structure, character
  voice, ritual, reversal, or payoff. It should survive a general cut pass.

Priorities:

- **P1:** Meaningfully slows the story, overdetermines interpretation, blurs
  voices, or repeats a major beat.
- **P2:** Noticeable line-level habit worth varying during the rewrite.
- **P3:** Micro-level polish; change only while already revising the passage.

## Report map

This overview holds the corpus diagnosis, cross-file matches, notice/trailer
review, and the detailed May 29–31 close read. The earlier files and exam
branches have companion inventories so the minute findings remain usable
rather than turning one document into an unsearchable wall:

- [`MAIN_STORY_REPETITION_DETAILS_0515_0519.md`](MAIN_STORY_REPETITION_DETAILS_0515_0519.md)
  — 139 line-addressed findings, plus cross-day patterns and intentional
  motifs.
- [`MAIN_STORY_REPETITION_DETAILS_0520_0524.md`](MAIN_STORY_REPETITION_DETAILS_0520_0524.md)
  — 182 local and cross-file findings, including 367 validated file/line
  references.
- [`MAIN_STORY_REPETITION_DETAILS_0525_0528_EXAM.md`](MAIN_STORY_REPETITION_DETAILS_0525_0528_EXAM.md)
  — every ordinary exam branch, caught route, first/repeat Himeko
  confrontation, bad end, and locked-load notice.
- May 29–31 are tabulated in this overview under their own headings.

The most important instruction for using these reports is: **delete the
duplicate job before searching for a synonym.** A thesaurus pass alone would
leave the explanatory ladder intact and merely disguise it.

## Corpus-wide diagnosis

The existing annotations correctly identify interpretive redundancy as the
central issue. The additional finding is that the redundancy is carried by a
small set of highly repeatable sentence engines. Those engines make otherwise
different scenes sound composed by the same intelligence.

Counts below exclude full-line comments and are diagnostic rather than
automatic deletion totals. Dialogue, narration, phone text, poems, and
player-facing thought-ledger text are included.

| Construction or word family | Approx. uses | Editorial significance |
|---|---:|---|
| `enough to` | 110 | 93 are in ordinary narrator lines and 12 more in Nier transitions. It is the clearest prose tic. |
| `enough to make` | 22 | Repeated cause/effect cadence: sensory fact, then an exact interpretation supplied for it. |
| `before X can` | 55 person/pronoun subjects; 75 including objects and abstractions | Every use is in narrator/Nier prose. It repeatedly predicts, interrupts, or mind-reads an action; 28 are the exact phrase `before I can` and 14 are `before she can`. |
| `for a second` | 35 | 33 are narrator lines; pauses acquire the same measured duration across different characters. |
| `like a/an` | about 80 | Frequent simile scaffold; often followed by another explanation of the image. |
| `looks/sounds/feels like` | about 91 | Perceptual hedge that often becomes a diagnosis rather than an observation. |
| `without` + `-ing` | about 83 | Commonly announces what a beat is *not* doing: not making a lesson, not turning into an event, not asking silence to perform. |
| `actual/actually` | about 78 | Shared intensifier across narrator, MC, Mom, Monika, and Asahina. Often removable. |
| `exactly` | about 68 | Over-calibrates reactions and distances; 47 uses are in narration/Nier. |
| `almost` | about 67 | Recurrent softener that makes moments hover at the same level of qualification. |
| `small` / `little` | about 152 | 121 uses are narration/Nier. Repeatedly tells the reader a beat is restrained. |
| `quiet/quietly` | about 94 | 83 uses are narration/Nier. Frequently doubles as sound level, emotional safety, restraint, and absence. |
| `line/sentence/question` | about 223 | Inflated by classes, exams, and poems, but also reflects a strong habit of naming dialogue as a textual object immediately after it lands. |
| legal/administrative/evidence vocabulary | about 173 | Narrator 84, MC 28, Mom 17, Nier 16, Asahina 11, phone text 10. Mom’s profession no longer contains the register. |
| eyes/look/glance/gaze | about 408 | Not a problem by raw count; it becomes one when the look is immediately translated. |
| hand/finger/thumb | about 199 | Same caveat: concrete gestures are useful, but many receive a narrator-supplied answer key. |
| phone buzz/light/facedown beats | about 42 | Repeated scene-entry and scene-exit mechanism; several days use it three or more times. |

### G1. The calibration sentence: “X enough to Y” — P1, N

The narrator repeatedly measures an adjective until it produces a precise
psychological or comic result:

- `0516.rpy:492`: “Just enough to make my free time feel pre-owned.”
- `0517.rpy:254`: “quiet enough to make the day feel further away”
- `0518.rpy:133`: “cheerful enough to make the screen feel brighter”
- `0519.rpy:142`: “agreeable enough to sound like a plan and vague enough...”
- `0520.rpy:61`: “calm enough to make other people nervous”
- `0523.rpy:611`: “just enough to make me realize...”
- `0524.rpy:138`: “smiles just enough to make Asahina’s ears turn pink”
- `0525.rpy:145`: “soft enough to make textbooks look briefly innocent”
- `0528.rpy:417`: “long enough to make sure the answer is not just a reflex”
- `0530.rpy:410`, `0530.rpy:594`: two separate “plain enough to...” judgments
- `0531.rpy:751`: a bag lands “hard enough to make the tableware notice”

This construction is often good in isolation. At 110 uses it becomes the
narrator’s default measuring instrument. During revision, keep versions that
deliver indispensable physical information; vary or cut versions whose
`to`-clause merely tells the reader how to interpret the adjective. A useful
first target is the dense May 24–25 stretch, where the construction appears 34
times across two days.

### G2. The pre-emptive action: “before X can...” — P1, A+N

This syntax appears in nearly every day and gives many people the same
half-second self-suppression. There are 55 uses with a person or pronoun as
the subject, rising to 75 when personified objects and abstractions are
included:

- `0515.rpy:133`, `0515.rpy:139`, `0515.rpy:223`
- `0517.rpy:41`, `0517.rpy:213`, `0517.rpy:396`, `0517.rpy:427`,
  `0517.rpy:462`
- `0520.rpy:75`, `0520.rpy:271`, `0520.rpy:359`, `0520.rpy:489`,
  `0520.rpy:498`
- `0521.rpy:226`, `0521.rpy:426`, `0521.rpy:492`, `0521.rpy:518`,
  `0521.rpy:561`, `0521.rpy:806`
- `0523.rpy:142`, `0523.rpy:234`, `0523.rpy:348`, `0523.rpy:639`
- `0524.rpy:381`, `0524.rpy:502`, `0524.rpy:597`, `0524.rpy:878`,
  `0524.rpy:896`, `0524.rpy:979`, `0524.rpy:1010`
- `0530.rpy:156`, `0530.rpy:211`, `0530.rpy:297`, `0530.rpy:495`,
  `0530.rpy:536`, `0530.rpy:550`, `0530.rpy:621`, `0530.rpy:754`
- `0531.rpy:328`, `0531.rpy:532`, `0531.rpy:603`, `0531.rpy:970`

It works best when literal timing matters. It is weakest when an abstraction
acts like a person (“before the sentence can follow me home,” “before the
moment can become a conversation,” “before the silence can become too
visible”) or when it certifies a character’s hidden inhibition (“smiles before
she can audit it”). Keep a minority as an MC avoidance tic; recast the rest as
direct action, an unqualified gesture, or a pause the reader can interpret.

### G3. Measured micro-pauses — P2, N

`for a second` occurs about 35 times, nearly always in narration. It combines
with `half a second`, `for one second`, `for a moment`, `for a few minutes`,
`pauses`, and `waits` to give unrelated characters the same timed hesitation.
The densest zones are `0523.rpy` through `0525.rpy` and the May 31 cafe/home
sequence.

Do not remove hesitation. Vary its embodiment: missed eye contact, an
unfinished physical task, a delayed reply, a change in subject, or no explicit
duration at all. When a concrete gesture already supplies the pause, delete
“for a second.”

### G4. Announcing restraint instead of practicing it — P1, A+N

The prose repeatedly praises a moment for remaining restrained:

- silence is not asked “to perform”;
- a moment is not made into “a lesson” or “an event”;
- a line needs no “decoration”;
- a beat carries only what it “needs”;
- something stays “small,” “plain,” “ordinary,” or “quiet”;
- people leave “before either of us can make” a moment heavier.

The local annotations catch many examples, but the aggregate pattern matters:
the story explains that it is not explaining. Strong examples to revise
include `0523.rpy:419`, `0523.rpy:557`, `0524.rpy:896`,
`0529.rpy:423-425`, `0530.rpy:262`, `0530.rpy:410`,
`0530.rpy:843`, `0531.rpy:588`, and `0531.rpy:966-970`.

The corrective rule is simple: if the sentence’s main purpose is to certify
restraint, test the scene without it.

### G5. Text about text after the text already worked — P1, A+N

The narrator often names the unit that just carried the emotion: “the line,”
“the sentence,” “the answer,” “the question,” “the joke,” or “the word.”
Then it supplies a verb and interpretation: the line lands, sits, catches,
leaves; the answer arrives; the joke lands; the question waits.

Representative clusters:

- `0525.rpy:378-392`: a line leaves, sits, becomes a container, and is escaped.
- `0530.rpy:151` and `0530.rpy:359`: “The joke lands” appears twice in one day.
- `0530.rpy:410`: the sentence is “plain enough to stop the next joke.”
- `0530.rpy:594`: the apology is “plain enough” to disarm the next line.
- `0531.rpy:240-249`: Monika’s line catches an answer, delays a smile, and is
  carried to track.
- `0531.rpy:573`: the answer is ranked beneath the joke.
- `0531.rpy:792`: the joke’s protective function is labeled.
- `0531.rpy:1068-1077`: an easy question waits, cues a memory montage, receives
  an answer, then has the lack of qualification explained.

Prefer the spoken line plus one physical consequence. Avoid turning dialogue
into a miniature piece of literary criticism immediately after the player
hears it.

### G6. Gesture, then mind-reading, then ledger — P1, A+N

The repeated ladder is:

1. eyes, fingers, a sleeve, a cup, a phone, or a bag move;
2. narration names the emotion or strategy;
3. dialogue confirms it;
4. `update_character_thought` records the approved interpretation.

The raw gesture vocabulary is not the problem. The problem is closure. This is
especially dense in `0523.rpy`–`0525.rpy`, `0530.rpy`, `0531.rpy`, and both
exam-guard confrontations. Treat roster thoughts as durable factual memory,
not a scene abstract. Where the gesture is legible, remove the diagnosis; where
the gesture is ambiguous in a productive way, do not make the ledger settle it.

### G7. Legal and administrative metaphor escaped Mom’s voice — P1, A+N

Mom’s profession justifies a legal register, and MC plausibly borrows it.
However, roughly half the uses belong to the narrator/Nier rather than either
speaker, and the register spreads to Asahina, Monika, Matsuda, Coach, phone
chats, school transitions, food, running, games, and flirtation.

Recurring fields include:

- court, counsel, evidence, testimony, record, precedent, ruling, appeal;
- file, audit, review board, case file, paperwork, procedure;
- contract, committee, jurisdiction, litigation, motion, injunction;
- administrative and bureaucratic punch lines.

The concentration rises sharply from May 19 onward and peaks on May 30–31.
Reserve the cleanest legal formulations for Mom. Let MC borrow fewer of them.
Give Asahina, Monika, Matsuda, Coach, and neutral narration other joke engines
so their voices stop converging.

### G8. The house/room “holds,” “settles,” “remembers,” or finds a “shape” — P1, N

This is a strong image family used often enough to become a scene-ending
template:

- `0521.rpy:126`: “the room settles around them”
- `0521.rpy:440`: track turns “back into a shape”
- `0523.rpy:824`: “The house settles around the tail end of the week.”
- `0524.rpy:1011`: “The house holds together in small domestic pieces...”
- `0525.rpy:1149`: “The house settles into paper noise again...”
- `0528.rpy:420`: “The house keeps making its ordinary sounds anyway.”
- `0529.rpy:41`: the kitchen settles “back into a shape”
- `0529.rpy:425`: “The house holds together in small pieces.”
- `0530.rpy:128`: the kitchen decides “what shape to hold”
- `0530.rpy:545`: “The room remembers what it was for.”
- `0531.rpy:1143`: “The house settles around ordinary plans.”

`0524.rpy:1011` and `0529.rpy:425` are especially close: both say the house
“holds together” in “small ... pieces.” Keep one as the signature formulation.
Elsewhere, end on the actual domestic object or sound instead of abstracting
the whole house.

### G9. Phones as punctuation — P2, A+N

Buzzing, lighting, vibrating, turning facedown, and being set beside another
object repeatedly start or close scenes. The gesture is most saturated when
“facedown” means privacy, restraint, avoidance, care, and simple scene closure
within the same day.

High-density examples:

- `0524.rpy:502`, `0524.rpy:545`, `0524.rpy:1025`, `0524.rpy:1048`
- `0525.rpy:88`, `0525.rpy:1123`, `0525.rpy:1196`, `0525.rpy:1279`,
  `0525.rpy:1308`
- `0529.rpy:129`, `0529.rpy:141`, `0529.rpy:211`,
  `0529.rpy:381-392`, `0529.rpy:424`, `0529.rpy:599`, `0529.rpy:627`
- `0530.rpy:705`, `0530.rpy:719`, `0530.rpy:866`, `0530.rpy:889`
- `0531.rpy:112`, `0531.rpy:607`, `0531.rpy:1023`, `0531.rpy:1165`

Keep facedown-phone gestures where orientation is meaningful, especially the
Sam and Mom work beats. Vary neutral message arrivals and scene exits.

### G10. Decompression repeatedly announced — P1, A+N

After exam week, May 29–31 repeatedly prove that ordinary life has resumed:
body release, harmless classes, free lunch, controlled track, normal dinner,
games, an altered bedroom, Saturday classes, and multiple end-of-day ledgers.
The scenes are worth keeping; the abstract reassurances around them are not.

The clearest exact recurrence is “For the first time in a week” at
`0529.rpy:109`, `0529.rpy:325`, and `0529.rpy:614`. Keep it once. The repeated
May 29, May 30, and May 31 classroom montages should become one full reset
montage followed by much shorter bridges on the next two days.

### G11. “Actual,” “exactly,” “apparently,” and “almost” — P2, N

These are not individually conspicuous, but together they produce a constant
tone of calibration:

- `actual/actually`: about 78 uses;
- `exactly`: about 68;
- `apparently`: about 31;
- `almost`: about 67.

They frequently occur in jokes (“actual writing,” “exactly four things,”
“apparently survived committee”) or narrator explanations. Cut the word when
the surrounding fact already establishes the contrast. Preserve it where a
speaker’s correction genuinely depends on emphasis.

### G12. Intentional repetition to protect — KEEP

Not all recurrence is excess:

- Coach’s “Pending external review” at `0529.rpy:247` and `0529.rpy:315` is a
  clean callback.
- “History rounds upward” at `0531.rpy:528` and `0531.rpy:551` reverses the
  earlier joke after MC wins.
- “Bookstore first” at `0530.rpy:609-610` demonstrates that Matsuda heard
  Tsubaki.
- “We can figure it out” at `0531.rpy:952-954` lets Matsuda mirror MC’s
  flexibility.
- The trailer’s `still` progression (`next_time_trailer.rpy:472`, `:480`,
  `:506`), its look-away echo (`:497`, `:536`), and its stop/could/remember
  reversals are architectural. They accumulate accusation and reframe the
  preceding ordinary days; do not “vary” them.

### G13. Near-verbatim lines hidden across different days — P2, N

A fuzzy line comparison found several small echoes that are easy to miss in a
day-by-day read:

| Locations | Echo | Direction |
|---|---|---|
| `0523.rpy:413`, `0524.rpy:643` | “(Then) the warning bell rings below us, thin and distant.” | Same transition on consecutive days. Change the second staging or omit the adjective pair. |
| `0523.rpy:872`, `0524.rpy:716` | “I stare at the screen/prompt longer than I should.” | Same self-conscious duration formula in adjacent files. Keep the prompt version if it marks the poem choice; make the earlier phone beat physical. |
| `0521.rpy:251`, `0523.rpy:278` | “Asahina looks/glances at me, then back at Tsubaki.” | Nearly identical social-triangle blocking. Vary one with dialogue or Tsubaki’s reaction. |
| `0523.rpy:639`, `0524.rpy:979` | “A (small) laugh gets out/escapes before I can stop it.” | Same laugh, same involuntary-release verb, same `before I can` syntax on consecutive days. Keep one. |
| `0523.rpy:443`, `0527.rpy:426` | “A few sprinters work/are doing starts near the straightaway.” | Reused track dressing. Replace the later background detail or omit it. |
| `0524.rpy:745`, `0525.rpy:970` | “Her handwriting is neater than mine (even) when she is drafting/slows down.” | Same comparison on consecutive days. Keep the one that matters to the poem/study object. |
| `0530.rpy:577`, `0531.rpy:624` | Matsuda puts one (gloved) hand to her chest. | Repeated theatrical reaction on consecutive days. Give one joke a different physical button. |
| `0518.rpy:471`, `0523.rpy:583` | “For a second, neither of us moves/opens it.” | The same bilateral-pause frame; remove explicit duration from one. |
| `0523.rpy:491`, `0529.rpy:265` | “Relax the hands... Let the pace stay boring. Continuing is the plan.” | This can be a useful learned-running mantra. **KEEP** the later shortened callback if the earlier line remains; do not paraphrase it merely for variety. |

Exact repeats inside exam answer branches are evaluated separately: some are
required so normal, wrong-answer, and caught-load paths rejoin coherently;
others are duplicated because two branches currently replay the same prose.

## Highest-value repetitions at story scale

These are the changes most likely to improve pace and voice before any
word-by-word polish:

| Thread / repeated scene job | Main locations | Why it now repeats | Revision direction |
|---|---|---|---|
| Glue/poster thread | `0515.rpy:409-434`; `0516.rpy:82-93`; `0517.rpy:38-49`, `:133-135`, `:194-218`, `:425-466`; `0518.rpy:533-578`; `0519.rpy:462-468` | Request, recap, reminders, purchase, handoff, progress, and praise keep re-establishing the same proof of care/competence. | Keep the initial deal, purchase/handoff, and one clean praise payoff. |
| Horror-movie plan and aftermath | `0515.rpy:165-181`; `0516.rpy:244-255`; `0517.rpy:133-143`; `0518.rpy:33-70`, `:521-620`; `0519.rpy:36-59`, `:263-306`, `:547-556` | Logistics are replayed before the date, then the date is debriefed on the ride, at home, at dinner, by text, next morning, at lunch, and at night. | Keep the date, one family debrief, and one theory exchange that creates new private language. |
| Matsuda/Tsubaki first impression | `0517.rpy:273-351`, `:415-496`; `0519.rpy:312-320`, `:333-442`, `:470-504` | Their collision already characterizes both girls; narration, family talk, and later summaries repeatedly deliver the critical reading. | Preserve their excess and friction; cut the observer recaps and roster-answer keys. |
| Classroom/quiz form | `0516.rpy:112-190`; `0517.rpy:71-113`; `0519.rpy:184-254`; exam drills and branches in `0525.rpy`–`0528.rpy` | Definition → analogy → life application → question → correction → recap becomes a reusable lesson machine. | Let only plot-bearing lessons run full length. Enter later, stop after the answer, and avoid teaching the exam verbatim in advance. |
| Return-to-running protocol | `0521.rpy:418-527`; `0523.rpy:429-540`; `0527.rpy:401-454`; `0529.rpy:239-287`; `0531.rpy:266-350` | Foot checks, easy-pace rules, bodily inventory, temptation to test, Coach correction, and post-run status are dramatized repeatedly. | Keep each genuinely changed threshold; summarize repeated mechanics and retain the learned mantra as a callback. |
| Tsubaki’s anxiety/growth choreography | `0521.rpy:244-385`; `0523.rpy:173-287`, `:390-417`; `0524.rpy:191-297`, `:479-500`; `0530.rpy:211-324`; `0531.rpy:392-476` | Tightened hands, backward/caught step, lowered gaze, apology, delayed smile, and narrator translation make her increasingly predictable. | Choose two signature tells and prioritize her self-authored boundaries; vary or withhold the rest. |
| Exam curriculum echo chain | `0525.rpy:179-453`, `:1011-1096`; `0526.rpy:67-345`; `0527.rpy:65-299`; `0528.rpy:224-325` | Sunday drill, teacher reminder, question, options, explanation, italic mnemonic, and guilt coda can state the same concept up to seven times. | Keep the study seed and exam application; reduce each answer to one feedback beat and let wrong choices remain wrong. |
| Six caught routes | `0526.rpy:547-646`; `0527.rpy:536-626`; `0528.rpy:659-750` | Each adult becomes quiet, names a zero, moralizes through the subject, invokes Mom/Monika/the record, and exits through guilt. | Give each teacher a different institutional behavior and one route-specific verdict/fear. |
| First/repeat Himeko confrontations | `exam_guard.rpy:361-680`, `:711-1008` | Both use door, standing Mom, phone, bag command, rejected excuse, panic-versus-choice lecture, institutional inventory, obedience lesson, and stairs. | Let the first scene own procedure/fairness. Start the repeat scene later and keep only the new trust/identity wound. |
| Post-exam decompression and plans | `0529.rpy:33-109`, `:325`, `:614`; `0530.rpy:182-191`, `:429-546`, `:598-681`, `:892-921`; `0531.rpy:161-254`, `:720-797`, `:1079-1126` | Three days repeatedly announce normality, club revival, and the complete outing itinerary before and after enacting them. | Give May 29 the full reset; use changed objects/actions as the May 30–31 proof. State each plan once before enactment and once only if it changes. |
| Mom’s absence/return objects | `0530.rpy:97-165`, `:651-795`; `0531.rpy:44-154`, `:1064-1077` | Empty chair, sugar-bowl note, third place setting, facedown phone, table size, return, and verbal interpretation repeatedly certify the same family state. | Protect the accidental third setting/larger table and all-three-chairs payoffs; cut intermediate chair/note glosses. |

### Exam-week routing and repetition guardrails

The exam material needs a path-aware edit rather than a linear “remove every
duplicate” pass:

- The recurring subject/day structure, checkpoints, menus, subject labels,
  caught-paper procedure, restart instructions, and locked-load instruction
  are ritual or mechanical clarity. Keep them unless the underlying mechanic
  changes.
- The avoidable bulk is the 54-branch
  **selected answer → rationale → italic answer/mnemonic** pattern. Wrong
  options are immediately overwritten by the correct answer in MC’s thoughts,
  so every branch repeats the curriculum and ordinary error never persists.
- May 25 teaches the exact civics, literature, biology, chemistry, and English
  material that May 26–28 repeat in prompts, choices, explanations, and
  mnemonics. Keep a study seed and test application/transfer rather than
  recognition of the just-displayed wording.
- At two catches, the dispatcher can send a same-day player into the label
  called “repeat” as their *first* home confrontation
  (`exam_guard.rpy:319-343`, `:686-695`). Its “last time,” “this time,” and
  changed-stairs prose then becomes false, while the normal confrontation’s
  `_home_multiple` variant is unreachable at that threshold. Fix dispatch
  before deciding which callbacks to retain.
- The bad end fires at two catches, but `exam_guard.rpy:1039` says “Anything
  past that,” grammatically assigning chosen agency to a later offense. Tie the
  judgment to the second catch or to the actual branch count.
- A stale in-exam load can represent crash recovery or an ordinary resumed
  session, not only answer revision (`exam_guard.rpy:309-312`). Even after the
  no-revision rule is stated up front, the guilt prose is earned only if the
  system distinguishes those states or offers a safe resume path.
- Source duplicates that are mutually exclusive in play—such as “Day two ends
  without applause,” the May 28 corridor setup, and branch-parity transitions—
  are not player-facing fatigue. Consolidate them only for maintainability.

## Notice and trailer

### `s1disc.rpy`

| Priority / label | Location | Finding and revision direction |
|---|---|---|
| P1 / A | `s1disc.rpy:64-73` | Coincidence-as-pattern, hidden heaviness, “warn you a second time,” discretion, and accepting what was said are four versions of ominous instruction. Decide whether the passage is a real content notice or a fictional hook. Replace one vague warning with the proposed concrete loss-fragment; do not add the fragment on top. |
| P1 / A | `s1disc.rpy:83-97` | After the player has already chosen Proceed, cooperation thanks, the school-year span, the generous road, deceptive perspective, and “Make the most” form a second notice ending. Keep the dates plus one loaded closing image. |
| P2 / N | `s1disc.rpy:68-73`, `:83` | “what waits,” “warn,” “discretion,” “accept,” “Understood,” and “cooperation” all keep the exchange in procedural language. If the opening borrows the trailer’s intimate loss-fragment, remove at least one institutional phrase so the new line is not smothered by contract language. |

### `next_time_trailer.rpy`

The trailer is a useful negative control for this audit: its repetitions change
meaning as they recur.

| Label | Location | Finding |
|---|---|---|
| KEEP | `next_time_trailer.rpy:472`, `:480`, `:506` | “still smiling” → “still here” → “still happy here” is deliberate escalation. |
| KEEP | `next_time_trailer.rpy:476`, `:545` | “You can stop” becomes “I couldn’t stop it either.” The repeated verb transfers agency and guilt. |
| KEEP | `next_time_trailer.rpy:497`, `:536` | Permission to “look away” returns as the accusation that everyone did. |
| KEEP | `next_time_trailer.rpy:561`, `:567`, `:573` | “can read” → “always could” → “remember” is the meta-contract. The lexical echo is the structure, not filler. |
| P3 / KEEP | `next_time_trailer.rpy:472-536` | “Everyone” and “here” recur, but the framing is short, beat-locked, and accumulative. Do not apply a thesaurus pass to it. |

## Day-level close read: May 29

### `0529.rpy`

| Priority / label | Location | Finding and revision direction |
|---|---|---|
| P1 / A | `0529.rpy:33-38` | Five formulations announce post-exam release before breakfast starts. Keep the body-that-forgot image and either absent dread or “unweaponized” school. |
| P2 / A+N | `0529.rpy:33`, `:90` | A body “forgot it was allowed to,” then the school “remembers it is allowed to be loud again.” The mirrored permission syntax makes the travel line feel composed from the opener. Keep it in one location. |
| P2 / N | `0529.rpy:42`, `:128`, `:166` | “the specific slump of a person,” “the leisure of a person,” and “the pleased expression of someone” repeat the same explanatory simile scaffold within 125 lines. Turn at least two into direct posture/action. |
| P1 / A | `0529.rpy:49-61` | Mom’s portal warning, contract comparison, paused thumb, inventorying glance, and “on the record” interpret the same watchfulness in layers. Preserve the thumb/glance and let the legal comparison or italic verdict go. |
| P2 / N | `0529.rpy:67`, `:320`, `:340` | MC repeatedly decides what an act “counts as”: a win, maturity rather than fatigue, enjoying weather rather than disobeying Coach. One is voice; three in a day becomes a self-scoring formula. |
| P1 / A | `0529.rpy:71-77` | The banana already conveys care. “I notice,” “not make it a thing,” and “Filed quietly” translate the unspoken exchange three times. |
| P1 / A | `0529.rpy:84-90` | Goodbye, uneventful departure, accomplishment, and a school “allowed to be loud again” all bridge the same return to normality. Compress to one travel line. |
| P1 / A | `0529.rpy:98-110` | Documentary, read-aloud, coffee, loose halls, a biology reenactment, small morning, absent fear, and the shoulder/bag simile are eight proofs of one post-exam mood. Keep the three-class montage and one release image. |
| P1 / N | `0529.rpy:109`, `:325`, `:614` | “For the first time in a week” appears three times on the same day. Keep the first use or the bedroom use, not all three. |
| P1 / A | `0529.rpy:113-119` | Lunch re-earns the freedom just established by the class montage. The first two Nier lines can become one clause before the corridor location. |
| P2 / N | `0529.rpy:129`, `:141`, `:211` | “My phone buzzes once,” “phone buzzes again,” and “phone buzzes once more” create the same transition three times in roughly eighty lines. Let Matsuda’s footsteps or name enter one beat without a buzz sentence. |
| P1 / A | `0529.rpy:149-223` | Matsuda announces restraint twice by text; then quiet sitting, MC’s diagnosis, her pacing line, a volume leak, her mission summary, a follow-up text, and the thought ledger prove it again. Keep her self-conscious text and the audible slip/recovery. |
| P2 / A+N | `0529.rpy:133-138`, `:214-216`, `:344-425`, `:588-614` | `normal`, `regular`, `ordinary`, `actual`, `small`, and `quiet` cluster across every phase of the day. The decompression is already structural; reduce the abstract labels and let changed routines carry it. |
| P1 / A+N | `0529.rpy:226-228`, `:236-325` | The “harmless” afternoon bridge opens a third decompression proof, followed by a roughly seventy-line track scene about accepting an easy day. Preserve Coach’s invitational decision and one successful restraint beat. |
| P2 / N | `0529.rpy:255`, `:263-267`, `:273-285` | The foot can “talk,” stays “quiet,” mental “quiet” lasts, MC answers “Quiet,” and Coach again conditions the entries on the foot staying quiet. Keep `quiet` as the foot-status shorthand; change the mental-release line so the word does not perform two jobs five times. |
| KEEP | `0529.rpy:247`, `:315-316` | “Pending external review” returns with Coach’s “review board.” This is a controlled callback inside one relationship. |
| P1 / A | `0529.rpy:258-267` | Slow on purpose, laps being only laps, shoulders talked down, an italic command, stopped inventory, and the quiet curve all interpret controlled effort. Keep physical shoulders/hands plus the foot status. |
| P1 / A | `0529.rpy:288-300` | “Maybe has enough room...” explains the exact mistake Coach catches with “spending it like yes.” Coach’s line is more voiced; cut the aphorism. |
| P1 / A | `0529.rpy:307-314` | Coach says MC need not win fitness back; narration admits he needs the advice; MC recites the plan. Choose private admission or spoken recap. |
| P1 / A | `0529.rpy:323-345` | Clean practice, no foot mention, long route, slow walk, earned legs, extra block, survivable distinction, ordinary noises, and “ordinary is almost loud” form an extended coda to the same easy session. Keep one track exit and one neighborhood image. |
| P2 / N | `0529.rpy:42`, `:354` | “specific slump” and “specific steam” use `specific` as a shortcut for observational precision. Neither is fatal, but the repeated adjective is less vivid than naming the actual posture or rice smell. |
| P1 / A | `0529.rpy:367-373` | The pickle argument shows normality; the no-grades inventory and “conversation finds smaller work” explain it twice. |
| P1 / A | `0529.rpy:378-415` | Slowed spoon, dark screen, colored grid, facedown phone, “colored fences,” “useful is hard to object to,” Mom’s second contract read, uncertainty, and filing turn Sam’s deniable control into a completed critical essay. Keep the grid/phone and MC’s uncertainty. |
| P1 / N | `0529.rpy:381-392`, `:424`, `:532`, `:561`, `:599`, `:627` | Screens/cards/phones repeatedly go dark or facedown. Some are literal game staging, but four different phone closures make `facedown` a general-purpose emotional punctuation mark. Protect Asahina’s Sam beat and Mom’s work beat; vary MC’s neutral bedtime action. |
| P1 / A | `0529.rpy:407-416` | Mom’s glance is called quick read, contract read, a read of both siblings, different things/same look, uncertain evidence, a filing, then two thought ledgers explain both targets. Reduce to glance + uncertainty; factual ledgers only. |
| P1 / A | `0529.rpy:419-425` | Dinner already ends on the uneasy glance. The dishes/call and “house holds together in small pieces” create a second family thesis immediately before another family scene. Transition on dishes. |
| P1 / A | `0529.rpy:473-488` | Rules premise, expansion dispute, Smuggler errata, and “nobody plays” consume twelve lines before the character-revealing purchases. Enter closer to “quiet arithmetic.” |
| P1 / A | `0529.rpy:489-520` | The first purchase round and the fifth-round market paragraph each fully define all three play styles. Use one compact style pass, then keep Mom’s deck-thinning advice. |
| P1 / A | `0529.rpy:541-573` | Coalition premise, terms, handshake, interrogation, offense, collapse, recount, and audit joke keep proving sibling chemistry. Compress to proposal plus one-round failure. |
| P1 / A | `0529.rpy:584-600` | Fist bump, “small and ordinary,” cleanup, room-work thesis, thought ledger, box, facedown work phone, and retreat are seven endings. End on the knuckle tap plus one cleanup image. |
| P1 / N | `0529.rpy:223`, `:632` | Matsuda’s character thought is updated twice with substantially the same facts: low-key lunch and a bookstore/arcade proposal. The later entry replays the earlier one. Keep one durable plan update. |
| P1 / A | `0529.rpy:608-614` | The no-exam room, ordinary desk, hidden sheets, calculator joke, long gaming, and regular-school line announce exam release for the fourth major time that day. One altered object is enough. |
| P1 / A | `0529.rpy:635-642` | Exams, grades, track, club, Tsubaki, sleep, and tomorrow form a full final ledger after the itemized-toll joke already closes the bedroom beat. End on that joke or the club reopening, not both plus the inventory. |

## Day-level close read: May 30

### `0530.rpy`

| Priority / label | Location | Finding and revision direction |
|---|---|---|
| P1 / A | `0530.rpy:97-100` | Empty chair, hurried handwriting, and the note establish Mom’s absence/care. Counting “three instructions, one forecast, and an emotional clause” turns it into an answer key. |
| P1 / A+N | `0530.rpy:97`, `:102`, `:127`, `:151`, `:163`, `:651`, `:688-697`, `:724`, `:788` | Chair and sugar-bowl note are revisited throughout breakfast, arrival, dinner, and Mom’s late scene. The dinner’s accidental third setting/table-larger image is the best payoff. Keep opener + that payoff + Mom noticing the saved note; cut intermediate reminders. |
| P1 / A | `0530.rpy:103-121` | Air-traffic control, litigation, zoning, architect, mitochondria, market testing, lawyer, and jurisdiction crowd one breakfast. Preserve two jokes in distinct voices. |
| P1 / N | `0529.rpy:135`, `0530.rpy:130` | Monika texts “real hours... Actual writing” on May 29; MC repeats “Real hours... Actual writing” at breakfast the next morning. Asahina only needs to learn that club is back; paraphrase or cut one half. |
| P1 / A | `0530.rpy:123-128` | Empty chair, mug, folder, missing phone intervention, functioning kitchen, and uncertain house-shape spend the dinner payoff in advance. |
| P1 / A | `0530.rpy:137-156` | “Any plans?” / “nothing scheduled” / “not what I asked” already shows evasion. Lawyer, jurisdiction, labeled joke landing, chair look, and cross-examination extend the defense. Move sooner to Asahina’s opening. |
| P2 / N | `0530.rpy:151`, `:359` | “The joke lands” occurs twice in one day as narrator stage direction. Delete both labels and let the changed gesture after each joke supply the tonal turn. |
| P1 / A | `0530.rpy:159-165` | Returning Mom’s note is clear attachment. “No practical reason” and “I keep it” explain the choice twice. End on replacing the note. |
| P1 / A | `0530.rpy:168-174` | On-time departure, bright walk, other students’ plans, MC’s non-contribution, and early arrival re-land breakfast. One bridge line. |
| P1 / A | `0530.rpy:182-191` | Four-subject reset, locked portal, Monday metaphor, clean page, and “return to form” repeat May 29’s full teacher montage. Retain Monday-grade pressure and compress the rest. |
| P1 / A | `0530.rpy:211-262` | Unaudited smile, numbered cards, separate lists, straight lettering, closed fingers, apology, one-finger release, hidden “testimony,” and silence not performing make Tsubaki’s anxiety transparent. Keep three concrete details and remove the supplied interpretation. |
| P2 / N | `0530.rpy:156`, `:211`, `:297`, `:342`, `:495`, `:536`, `:550`, `:621`, `:754` | This day is the densest late-act example of `before X can`: cross-examination, self-audit, deciding whether to laugh, gravity filing a motion, making a poem prettier, producing a defense, assigning another line, stopping laughter, objecting. Recast most; keep only literal timing. |
| P1 / A | `0530.rpy:274-304` | Straightened sleeve, secretary boundary, surprise at meaning it, quiet delivery, delayed laugh, escaped laugh, and decision whether to keep it explain assertion and humor repeatedly. Keep sleeve + boundary + one shared laugh. |
| P1 / A | `0530.rpy:307-324` | Correct-bag check, goodbye, reassurance, smile, follow, and thought ledger recite inventory, preference, and confidence. End on “See you later” or the smile. |
| P1 / A | `0530.rpy:337-419` | Box weight, held hand, quiet-club diagnosis, exam explanation, normal-quiet distinction, folded-slip fidget, fragile-peace joke, three absence prompts, ratification jokes, plain wish, and extra door jokes layer Monika’s concern. Keep the hand/folded slip and “I want today to feel like the club came back.” |
| P2 / A+N | `0530.rpy:340-416` | Permit, gravity “filing its motion,” presidential authority, crowdsourcing, scientific process, ratification, democracy, and transition of power extend the global administrative register outside Mom’s scenes. Replace at least half with non-bureaucratic banter. |
| P1 / A | `0530.rpy:429-436` | “The literature club is alive again” is immediately followed by “The room is actually alive,” then an activity inventory proves both. Keep only the activity. |
| P1 / A | `0530.rpy:456-463` | The train, map, conductor, lights, and stairs are paraphrased immediately before the displayed poem. Delete the synopsis. |
| P1 / A | `0530.rpy:476-493` | Narration diagnoses absent desire before “Home, probably,” then explains the added line as less clever but directional before Monika offers the stronger critique. Let dialogue reveal both discoveries. |
| P1 / A | `0530.rpy:537-546` | Activity montage proves the club is back; “club gets to be club,” nobody studies, the room remembers, and the thought ledger state it four more ways. Keep drafts moving across desks. |
| P1 / A | `0530.rpy:564-582` | The hillbilly voice receives roughly nine separate comic samples before the invitation. Keep three: opening accent, one Tsubaki correction, and the attempted invitation. |
| P1 / A | `0530.rpy:583-602` | Stop, open mouth, closed mouth, vanished accent, annoyed shoulder, self-diagnosis, shelving the voice, plain apology, explanation of plainness, “normal question,” and no-speech narration overdocument one correction. Keep stop + “Sorry” + direct question. |
| P2 / N | `0530.rpy:289`, `:410`, `:594` | “comes out cleanly,” “plain enough to stop the next joke,” and “plain enough to take the fight out...” repeatedly certify unperformed speech. Delete the certificates and trust Tsubaki/Monika/Matsuda’s actual lines. |
| P1 / A | `0530.rpy:598-628` | Narration praises lack of a speech; acceptance lands; bookstore order lands; accent button, relief laugh, history exchange, and narrator-labeled pleasure add multiple buttons. End sooner, ideally on Tsubaki’s “No” or the mirrored “After track.” |
| P1 / A | `0530.rpy:641-645` | Matsuda’s thought ledger retells the voice arc seconds later. Record only tomorrow’s durable plan. |
| P1 / A | `0530.rpy:660-681` | Asahina repeats Matsuda’s full invitation format, restraint, title, and order immediately after the player saw it. Enter on “Did you say yes?” |
| P2 / N | `0530.rpy:668`, `:681`, `:887`, `:908` | “order of operations”/binding-order language becomes a minor refrain around an itinerary the story already repeats. Keep it once in Asahina’s voice. |
| P1 / KEEP | `0530.rpy:686-693` | Accidental third place, “Oh,” removed bowl, and larger table are precise and unexplained. This is the keeper. |
| P1 / A | `0530.rpy:694-729` | Reassurance, refrigerator-hum interpretation, empty chair restatement, Mom’s explanatory text, unsolicited dishes, and thought ledger continue closing the keeper image. Move from the larger table to the Sam exchange or out of scene. |
| P1 / A | `0530.rpy:732-740` | Shower, phone call, uniform, arrival, kiss, shoulder squeeze, saved plate, and open folder create a second scene inside the bridge to the actual Mom scene. Keep arrival + folder/plate. |
| P1 / A | `0530.rpy:754-761` | Mom allowing MC to remove the folder, “tells me more,” thanks, and first real bite explain exhaustion three times. Keep action + thanks/bite. |
| P1 / A | `0530.rpy:774-795` | Takeover, injunction, counsel, precedent, packaging defense, court rejection, and appeal saturate a care exchange. Keep the something-with-color callback and one legal reply. |
| P1 / A | `0530.rpy:833-855` | “five minutes” is stated by Mom, interpreted as a lesson, copied into the thought ledger, repeated in Nier narration, and abstracted as the house regaining its center. Closed eyes/open hands/unreachable folder already end the scene. |
| P1 / A | `0530.rpy:869-887` | The group chat establishes order, vetoes, and tone. A final litigation sentence paraphrases the unresolved food choice. End on “Philistines.” |
| P1 / A | `0530.rpy:892-908` | Monika asks whether the traveler goes inside; narration repeats deadline, weekend, MC’s schedule, and judgment of the order. Keep one glance at the draft. |
| P1 / A | `0530.rpy:912-921` | School, track, arcade, arrivals, bookstore priority, and forbidden group name repeat the complete itinerary. End on unfinished traveler or May’s one remaining day. |

## Day-level close read: May 31

### `0531.rpy`

| Priority / label | Location | Finding and revision direction |
|---|---|---|
| KEEP / A | `0531.rpy:44` | “all three chairs occupied” is the clean answer to May 30. Protect it. |
| P1 / A | `0531.rpy:67-90` | Full safety rules, felony routine, foot warning, demanded recitation, sibling jab/apology, and second foot confirmation replay yesterday’s rules and prefigure Coach repeating them. Keep one Mom line plus MC’s remembered limit. |
| P1 / A | `0531.rpy:92-103` | Finished sip, short reply, facedown phone, returned chair, explicit “restraint,” and morning “keeping” Mom all interpret the same family choice. Keep the actions. |
| P1 / A | `0531.rpy:112-139` | Group chat shows Matsuda’s early energy and MC’s fast reply; Asahina diagnoses both, Mom calls him amused, and the seven-second response proves it again. Keep chat behavior or family diagnosis. |
| P1 / A | `0531.rpy:140-154` | “all three chairs where they belong” repeats the opener; bag checks and “Have fun” produce another breakfast ending; narration then explains why the second instruction works. End on Mom choosing family/work restraint or her repeated line. |
| P1 / A | `0531.rpy:161-188` | Destinations/chat recap leads into the third consecutive post-exam school montage. Named subjects, portal, six numbers, clean copying, fear diagnosis, and migration should compress to final-bell release. |
| P1 / A | `0531.rpy:203-254` | Outing itinerary and unfinished line were covered last night and return again at bedtime. The corridor reminder, Monika’s full defense diagnosis, delayed smile, carryout image, and thought ledger interpret “allowed to enjoy” repeatedly. Keep Monika’s line and the Monday deadline; trim its wake. |
| P1 / A | `0531.rpy:266-350` | Foot check, controlled pace, overreach, correction, successful restraint, invitational reminder, three warnings, no secret lap, no test, and fourteen-minute proof substantially replay May 29. Keep the clean seventy-five-percent run, Coach’s “Go be eighteen,” and responsible arrival. |
| P2 / N | `0531.rpy:274-300`, `:346`, `:375`, `:1051-1058` | `quiet` is used repeatedly as the foot’s status, then checked again at the bookstore and at home. Necessary continuity need not use the identical adjective every time; keep Coach’s shorthand and vary later confirmations (“no pain,” “still fine,” or simply the walk). |
| P1 / A | `0531.rpy:296-316` | Narration names MC’s permission/test compulsion before Coach’s sharper “personally offended” line; three more strides and the final adjective/repetition joke prove it. Let Coach own the diagnosis. |
| P1 / A | `0531.rpy:323-338` | Train, stairs, and arcade warnings repeat one instruction before “Go be eighteen.” Keep the release line; one warning is enough setup. |
| P1 / A | `0531.rpy:392-407` | Tsubaki’s “Not yet,” satisfaction diagnosis, remembered-promise claim, journal interest, held place, “Maybe,” and no-apology explanation close a small answer several times. Preserve her interest and unqualified “Maybe.” |
| P1 / A | `0531.rpy:413-443` | Stopped fingers, repeated caption, covered line, flat misspelling, no-stage-voice rubric, refusal, Tsubaki’s acceptance, and measured return of brightness thoroughly grade Matsuda’s performance level. Keep covered caption + “No” + ordinary transition. |
| P2 / N | `0529.rpy:137`, `0531.rpy:446` | Monika says “I contain multitudes”; two days later Matsuda says “Literature contains multitudes.” The common quotation is recognizable, but placing it in two voices this close reinforces authorial voice-sharing. Keep the stronger Monika/clipboard joke or make Matsuda’s defense hers. |
| KEEP / A | `0531.rpy:450-467` | Tsubaki pays/carries; Matsuda moves her bag back and later accepts “Inventory.” These actions carry both arcs without a speech. |
| P1 / A | `0531.rpy:468-476` | “Thanks” with both hands is called plain; Tsubaki’s smile is called plain; the ledger again explains that she did not apologize. Keep word/action and factual purchase. |
| P1 / A | `0531.rpy:480-510` | Transition declares Matsuda no longer needs to make the room louder; an eight-second restraint meter grades her again; waiting at the kiosk proves changed behavior a third time. Let the cabinet choice reveal her. |
| P2 / A+N | `0531.rpy:528-555`, `:788`, `:1172` | `History` becomes a running Matsuda/MC bit: rounds upward twice, is specific/rude, contains clerical sins, and becomes “accurate history” in the final chat. Keep the race reversal; consider varying at least one later use so the tag does not become her only joke engine. |
| P1 / A | `0531.rpy:534-550` | Blink, tentative “Yeah?”, victory speech leaving her face, balcony-less grin, full second-race tactics, and tied result overplay MC’s “Again.” Keep the request and compress race two to result. |
| P1 / A | `0531.rpy:561-588` | Third race is useful because it yields Matsuda’s body read; narration then ranks the answer beneath the joke, followed by title banter, hand up, grip quality, paired “Good” lines, and a sentence saying they need no decoration. Cut the rankings/meta-end cap. |
| P1 / A | `0531.rpy:589-606` | Tsubaki’s rescue pattern and high score show competence; “exposed her private life,” hidden-talent announcement, training explanation, second stage, shouting, and laugh keep proving it. Keep rescue pattern + her request for the next stage. |
| P1 / A | `0531.rpy:637-681` | Asahina’s recalibration is supplied before the exchange; a full repeated light-gun stage then re-proves integration before the dance contest. Remove the label and compress the replay. |
| P1 / A | `0531.rpy:683-719` | One-attempt negotiation, failed bird, silence, geometry joke, shared laugh, “one attempt” twice, card visible, card away, glass touch, “next time,” and no-date narration land the honored limit repeatedly. Keep failure + card put away + “Maybe next time.” |
| P1 / A | `0531.rpy:720-737` | Arcade activity montage, tired-body coda, locker check, food consensus, committee word-choice explanation, and two thought ledgers make a long exit. “Committee” already shows Matsuda remembered the veto; do not translate it. |
| P1 / A | `0531.rpy:757-797` | The cafe repeats the television role, three/four lines, age, misspelled name, and refusal from the bookstore. Summarize Asahina asking and enter on the misspelling/too-fast “No.” |
| P1 / A | `0531.rpy:789-808` | Napkin fold is labeled as protective joking, then cafe silence is assigned a precise function before the excellent fries/pickle beat. Delete both readings and protect the food exchange exactly as written. |
| KEEP / A | `0531.rpy:807-808` | Fries aligned, pickle dish nudged, one pickle taken: the food thread at its correct volume. |
| P1 / A | `0531.rpy:809-826` | Landlord callback establishes easy table talk; title correction, marketing defense, inquiry, nine-book requirement, resignation, and fry button extend it. Trim the middle. |
| P1 / A | `0531.rpy:827-837` | Tsubaki states her train time; narration says she addresses the table; Matsuda accepts; narration says “No negotiation.” Dialogue already demonstrates both arcs. |
| P1 / A | `0531.rpy:838-862` | Mom text, arcade-credit joke, hidden smile, four-hand check, cultural-exchange joke, change errand, and cookie errand form a long runway to the core conversation. Keep only actions needed to leave MC/Matsuda alone. |
| P2 / N | `0531.rpy:863-872`, `:884-910`, `:933`, `:959`, `:971-973` | Sugar packets are stacked, watched, flattened, removed, turned, refitted, traced, straightened, frozen under a thumb, left in a square, and turned into “sugar business.” The prop is good; cut two or three handling updates so it does not visibly work for every beat. |
| P1 / A | `0531.rpy:877-910` | “Why are you trying so hard?” is productive. The following dossier lists club, surname, schedule, racing tell, plans, voices, books, bread, and TV; Matsuda then supplies a near-complete diagnosis of her future overdependence. Use one asymmetry example and withhold “I keep pushing after it stops helping.” |
| P1 / A | `0531.rpy:905-923` | Narration certifies that Matsuda is not asking for rescue and later certifies her smile as real. Her uninterrupted answer and “No. It wasn’t” establish both. |
| KEEP / A | `0531.rpy:932-954` | MC initiates the next outing; Matsuda corrects “next weekend” to open timing; “We can figure it out” is mirrored. This is the capstone action. |
| P1 / A | `0531.rpy:945-970` | Narration identifies velocity/retreat, then calendar closed, group unnamed, packets ordered, tone labeled light-not-careless, and a sentence says the moment carries only enough. Dialogue already proves flexibility. Keep at most the packet image. |
| P2 / N | `0531.rpy:980-982` | Station narration again emphasizes Tsubaki carrying her bundle, refusing Matsuda twice, and Matsuda carrying all nine books. These facts were enacted at the bookstore/cafe. A simple departure can preserve geography without regrading boundaries. |
| P1 / A | `0531.rpy:1009-1018` | Asahina’s “She listened when people said no” is a useful judgment shift; claw limit, dropped title, and MC’s slowdown request retell all three demonstrations. Keep conclusion + one example. |
| P1 / A | `0531.rpy:1064-1077` | Patient-question explanation, arcade memory montage, answer, and “no qualification” frame “Yeah. It was fun.” Trust the pause, answer, and Mom’s “Good.” |
| P1 / A | `0531.rpy:1079-1126` | The new invitation is litigated by Asahina, joked about by Mom, interpreted in advance friendship advice, then examined again one-on-one with a second, plainer thesis. Keep the private exchange or the family teasing, not both. |
| P1 / A | `0531.rpy:1139-1144` | Ordinary-plan list carries retrospective unease; threshold aphorism explicitly instructs the player to flag it. Keep list or aphorism. |
| P1 / A | `0531.rpy:1155-1164` | The train poem was displayed twice and discussed repeatedly. Re-listing train, conductor, lights, stairs, television, and dishes tests recall. Enter on Monika’s green-ink question. |
| P1 / A | `0531.rpy:1179-1195` | Unanimous “Good day” group chat is followed by private thanks, race banter, future rematch, and goodnight already landed at the cafe. Choose communal confirmation or private intimacy. |
| P1 / A | `0531.rpy:1197-1205` | Seventeen-day/card frame is valuable; ticket, foot, exams, cafe seat, people, tomorrow, Monday, invitational, and no-date inventories summarize the act before its symbolic ending. Keep frame; cut lists. |
| KEEP | `0531.rpy:1212-1213` | “The door is already open” is the right final poem addition. |
| P1 / A | `0531.rpy:1214-1237` | The line is followed by ambiguity explanation, acceptance, Matsuda ledger, ordinary-pieces coda, non-explanation thesis, and open-door echo. This is the project’s “beautiful beat → explain → restate → echo” habit in miniature. End on the poem line or keep one Nier sentence only. |

## Recommended revision sequence

1. **Fix exam path semantics first.** Resolve the contract/resume distinction,
   same-day-double dispatch, two-catch threshold language, and wrong-answer
   persistence before judging how much guilt/confrontation prose is earned.
2. **Remove duplicated scene jobs across days.** Start with the glue/poster,
   movie aftermath, Matsuda/Tsubaki introduction, repeated running protocol,
   full pre-exam curriculum, caught-route template, and repeated post-exam
   reset/itinerary. This produces more improvement than swapping individual
   words.
3. **For every P1 emotional cluster, select one keeper.** Usually that is the
   first concrete action, the character’s strongest self-authored line, or the
   altered object at the end. Challenge every later diagnosis, joke, ledger
   entry, and transition summary until it contributes a genuinely new fact.
4. **Thin quiz feedback, thought ledgers, and Nier bridges.** Feedback should
   not give an answer three times; ledgers should store durable plans or
   unresolved wording; bridges should communicate elapsed time plus one
   changed detail.
5. **Restore ownership of voice registers.** Himeko may retain precise
   legal/professional language; MC can inherit and misuse part of it; Matsuda
   can keep theatrical bureaucracy. Remove generic court/filing/evidence
   metaphors from neutral transitions and do not let Monika, Asahina, Coach,
   teachers, and rooms all borrow the same engine.
6. **Then perform the sentence-level sweep.** Target the list below in context,
   deleting first and varying second. Do not impose a blind quota: motifs,
   character rituals, and earned callbacks are listed as KEEP for a reason.
7. **Re-read complete reachable paths without annotations visible.** Check the
   ordinary route, each possible pair of caught subjects, same-day double,
   first/repeat home confrontation, bad end, locked-load notice, and trailer.
   Linear source order alone cannot reveal player-facing repetition.

## Minute line-edit checklist

| Search family | What to challenge |
|---|---|
| `enough to`, `enough that`, `enough for`, `enough to make` | Does the result clause merely grade how legible/strong the preceding action is? |
| `before I/she/either... can`; abstract `before the sentence/silence/moment can` | Is a hypothetical reaction being narrated only to prove inhibition or create artificial timing? |
| `not X—just Y`, `not X, more Y`, `not because`, negative-fragment triads | Is the prose narrowing the reader to the correct emotional category after the image already worked? |
| `for a second`, `half a second`, `a beat`, `a moment`, `for a while`, `pauses`, `waits` | Would paragraphing, sprite change, or the next action supply the pause without measuring it? |
| `actual(ly)`, `exact(ly)`, `apparently`, `almost`, `probably`, `honestly`, `somehow` | Is the qualifier voice-specific, or a shared softener/intensifier that can disappear? |
| `small`, `little`, `quiet(ly)`, `plain`, `ordinary`, `normal`, `clean`, `shape` | Is the word announcing restraint, sincerity, scale, or repair that the concrete object/action already demonstrates? |
| `line`, `sentence`, `question`, `word`, `answer`; `land/lands`, “the joke lands,” “there it is” | Is the narration rating, naming, or explaining dialogue immediately after the player read it? |
| `look/glance/gaze/eyes`, `hand/finger/thumb`, smile timing | After the gesture, how many sentences translate the feeling, certify it, or repeat it in dialogue/ledger form? |
| `phone buzzes/lights`, `facedown`, thread opened/closed, phone set beside an object | Is the phone plot-relevant here, or serving as the default entrance, interruption, and scene button? |
| room/house/day/sentence/phone personification: `holds`, `settles`, `remembers`, `breathes`, `decides`, `asks`, `knows` | Is this the load-bearing image, or another abstraction performing emotional interpretation? |
| court, counsel, evidence, file, record, jurisdiction, contract, committee, procedure, verdict, appeal, audit | Does the speaker own this register, and is it the one best administrative joke in the scene? |
| `same`, `usual`, `the rest of`, `by the final bell`, “afternoon classes take...,” daily inventories | Does the transition label routine and then show the same routine again? Keep the changed detail. |
| joke volleys and endings | Does the exchange have a premise, good reply, confirming reply, metaphorical reply, narrator verdict—and can it stop at the good reply? Does the scene end, explain its ending, then inventory the night? |

## Audit validation

- All four deliverables use the current workspace snapshot and current line
  numbers.
- The May 15–19 report independently validated 248 explicit file/line
  references.
- The May 20–24 report contains 367 validated file/line references.
- The May 25–28/exam report validated 325 citation spans, expanding to 3,512
  unique file/line pairs, with no missing or out-of-bounds targets.
- This overview’s explicit full `file.rpy:line` references were also checked
  against the current files. Story prose was not edited during the audit.
