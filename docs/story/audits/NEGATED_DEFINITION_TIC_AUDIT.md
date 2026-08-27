# ENTER M — "This isn't X. X is [anecdote]" Prose-Tic Audit

Status: complete sweep, August 1, 2026. **Read-only — no `.rpy` file was modified.**

## What was searched

The construction under audit is the *negated definition*: a sentence denies a
label, and the next sentence supplies the "real" one, usually with a concrete
image or vignette attached.

> This isn't grief. Grief is when you go to text someone who's dead.

The literal string `is when` occurs **once** in the entire story corpus
(`0521.rpy:209`, and it is ordinary past-tense dialogue, not the tic). So the
pattern lives in this project as its *structural* variants, which is what this
document catalogs.

### Scope

| Path | Lines | Covered |
| --- | --- | --- |
| `game/story/season1/0515.rpy` – `0531.rpy` | ~8,900 | yes |
| `game/story/season1/exam_guard.rpy` | 794 | yes |
| `game/story/season1/s1_choices.rpy`, `s1disc.rpy` | 194 | yes |
| `game/story/out_of_context/ooc_1026_passed_out.rpy` | 240 | yes |
| `game/story/out_of_context/ooc_1224_unasked.rpy` | 17 (design notes only) | yes |
| `game/story/season2`, `season3`, `seasonintermission` | empty | n/a |

Three OOC files are currently stubs reading
`# deleted because i'm gonna rewrite this one by hand`
(`ooc_0101_this_year_too.rpy`, `ooc_1030_nothing_to_add.rpy`,
`ooc_1224_closing_exercises.rpy`), so they contributed nothing.

Method: every dialogue/narration string was flattened, sentence-split, and
filtered to the 303 sites containing a categorial negation; each was then read
in context against its following 1–3 sentences. Addons/character stories were
spot-checked only (see Appendix B).

### Severity labels

- **T1 — full tic.** Denies a label, then redefines it with a concrete
  image, list, or vignette. This is the pattern as stated.
- **T2 — bare corrective swap.** `It isn't X. It's Y.` Same rhythm, but the
  replacement is abstract — no anecdote. The load-bearing filler version.
- **T3 — stacked negation triple.** `Not A. Not B. C.` A compressed sibling
  that reads as the same authorial reflex when it clusters.
- **T4 — aphorism family.** `X is not the same as Y.` A distinct sentence
  shape, but the same "correct the reader's word choice" move. Listed because
  it is the single most repeated formula in the corpus and shares the tic's
  fingerprint.

**Headline count: 47 sites — 11 T1, 13 T2, 15 T3, 8 T4.**

---

## T1 — Full tic (11 sites)

The negation lands, then a concrete image does the redefining. These are the
strongest and, individually, mostly the best writing in the list.

| # | Location | Line |
| --- | --- | --- |
| 1 | `season1/0520.rpy:278` | "It's not that they're shutting me out. It's that they've built a small room I don't have a key to, and they're being very polite about handing me snacks through the door." |
| 2 | `season1/0530.rpy:519` | "Not night-dark. Empty-house dark: curtains half open, kitchen clock bright enough to be rude, no voice answering the door before it closes." |
| 3 | `season1/0526.rpy:153` | "Lunch is not lunch." / "It is forty minutes of pretending my bag has not turned into a sealed envelope marked *disciplinary matter*." |
| 4 | `season1/0519.rpy:296` | "It isn't that Matsuda got quieter. It's that I asked her to, and she did, and the sky stayed up." |
| 5 | `season1/exam_guard.rpy:463` | "It isn't a laugh." / "It's what her voice does because the body has no professional tool for this." |
| 6 | `season1/0523.rpy:317` | "Not the violent argument of a sprint start, not the twelve-second dare of turning the body into a weapon." / "This is time, posture, breath, and the patience to let easy become honest." |
| 7 | `season1/0526.rpy:246` | "Not just someone who lies. Someone whose version cannot be trusted without checking the room around them." |
| 8 | `season1/0526.rpy:23` | "a paper that leaves this room and comes back different is not a corrected paper." / "It is a different paper, and I will treat it as one." |
| 9 | `season1/0519.rpy:385` | "It's not necessarily the decision to keep watching, because there isn't one, but the absence of any decision to stop, stretched out long enough that it feels deliberate." |
| 10 | `season1/0518.rpy:458` | "the iron rod wasn't actually the weapon. It was the promise." *(phone message — Monika)* |
| 11 | `season1/exam_guard.rpy:489` | "That's the line." / "Not the loudest one." / "Not the cruelest." / "The one that changes the room from home into evidence." *(also a T3 stack)* |

### The one hard collision

Sites **3** and the T2 entry at `0526.rpy:167` are the *same sentence stem* in
the *same file*, on the two sides of one branch:

- `0526.rpy:153` (save-scum branch): "Lunch is not lunch."
- `0526.rpy:167` (clean branch): "Lunch is not lunch so much as a scheduled
  decompression chamber."

A player who replays the exam week hits both. This is the only place where the
tic is provably visible to a single player twice in one scene.

---

## T2 — Bare corrective swap (13 sites)

Same rhythm, abstract replacement. These are the ones that read as reflex
rather than choice, because nothing concrete arrives to justify the setup.

| # | Location | Line |
| --- | --- | --- |
| 12 | `season1/0526.rpy:167` | "Lunch is not lunch so much as a scheduled decompression chamber." |
| 13 | `season1/0519.rpy:139` | "The issue is not that the person spoke publicly." / "The issue is that the public display replaced the substance." |
| 14 | `season1/0527.rpy:281` | "Good is not forgiveness." / "Tonight, it is just a fact placed carefully where a fact belongs." |
| 15 | `season1/0528.rpy:428` | "It isn't triumphant." / "It's quieter than that, maybe more useful." |
| 16 | `season1/exam_guard.rpy:419` | "The second one isn't anger." / "It's almost pleading." |
| 17 | `season1/exam_guard.rpy:662` | "Not even a question. A door she isn't opening." |
| 18 | `season1/0521.rpy:65` | "The restrained diction may resemble objectivity, but the effect is not neutral." / "The omission controls where blame can settle." |
| 19 | `season1/0524.rpy:565` | "Add one image after it. Not an explanation." / "Something the seat physically does." |
| 20 | `season1/0523.rpy:462` | "Not the classes. The rest of it." / "The rest of it is usually what people mean." |
| 21 | `season1/0525.rpy:343` | "It's a beverage, not a pact." |
| 22 | `season1/0529.rpy:132` | "The melon bread is a choice, not a cry for help." |
| 23 | `season1/0530.rpy:406` | "Not when I wrote the directions." *(Monika, on whether the place exists)* |
| 24 | `season1/0526.rpy:483` | "*Not a lecture. Not yelling. Just the sound of a door closing because I gave it a reason to.*" *(also a T3 stack)* |

Entries **21** and **22** are the comic inversion of the tic — a character
using it as a deadpan joke. They're doing different work from the rest and are
worth keeping even if the family gets thinned.

---

## T3 — Stacked negation triple (15 sites)

`Not A. Not B. C.` Individually fine; the concern is density. **Nine of the
fifteen are in `exam_guard.rpy` alone**, a 794-line file — that scene runs the
same rhythm roughly every 40 lines.

### `exam_guard.rpy` cluster

| # | Location | Line |
| --- | --- | --- |
| 25 | `exam_guard.rpy:293` | "Not facedown this time." / "Not waiting to testify." / "Already on the record." |
| 26 | `exam_guard.rpy:377` | "Not rage." / "Not strategy." / "Pain." |
| 27 | `exam_guard.rpy:434` | "Not yet." / "Not before you understand--" / "No. Not understand." |
| 28 | `exam_guard.rpy:444` | "It is not my good mood." / "It is not one evening." / "It is not even the calls from school." / "It is this." *(four-beat)* |
| 29 | `exam_guard.rpy:454` | "Not to me. Not *only* to me." |
| 30 | `exam_guard.rpy:458` | "Not enough to fall." / "Just enough to understand that falling would be easier." |
| 31 | `exam_guard.rpy:478` | "Not charm. Not grades. Not one more clean performance." |
| 32 | `exam_guard.rpy:489` | "Not the loudest one." / "Not the cruelest." / "The one that changes the room from home into evidence." *(= T1 #11)* |
| 33 | `exam_guard.rpy:665` | "Not even the cheating." / "That you're sitting there still solving for the exit." |

Sites **28**, **31**, and **32** land within 45 lines of each other, all in
Mom's voice, during the emotional peak of the scene. That's the densest
concentration in the corpus.

### Elsewhere

| # | Location | Line |
| --- | --- | --- |
| 34 | `season1/0525.rpy:10` | "Not fifteen minutes after, not in the middle of a dream where my phone has become an accusing rectangle." / "One minute before." |
| 35 | `season1/0526.rpy:134` | "Not the zero, not the teacher's voice, not the way the room looked away too quickly." |
| 36 | `season1/0526.rpy:483` | "*Not a lecture. Not yelling. Just the sound of a door closing...*" *(= T2 #24)* |
| 37 | `season1/0523.rpy:407` | "Not making a verdict, not committing your life, not picking the name that goes on every future holiday conversation..." |
| 38 | `season1/0528.rpy:295` **and** `:301` | "Not graded, not forgotten, not harmless." |
| 39 | `season1/0528.rpy:274` **and** `:285` | "Not happy exactly -- just released." |

### Branch-duplicated lines (38 and 39)

Both sit inside `if persistent.exam_save_scum_subjects: / else:` blocks in
`0528.rpy` and are **verbatim identical on both sides of the branch**:

- `0528.rpy:274` / `0528.rpy:285` — "Not happy exactly -- just released."
- `0528.rpy:295` / `0528.rpy:301` — "Not graded, not forgotten, not harmless."

Because they're identical, they could be hoisted above the branch. Flagged for
information only — no change made.

---

## T4 — "X is not the same as Y" (8 sites)

The most-repeated single formula in the story. Six of the eight are Mom or a
teacher, which makes it read as a deliberate adult-authority verbal signature —
but two are MC's own narration, which weakens that reading.

| # | Location | Speaker | Line |
| --- | --- | --- | --- |
| 40 | `season1/0517.rpy:78` | civics teacher | "tolerated is not the same as trusted." |
| 41 | `season1/0517.rpy:178` | Asahina | "I started without the most important part. That's not the same thing." |
| 42 | `season1/0523.rpy:441` | Mom | "It is not the same as a life sentence." |
| 43 | `season1/0523.rpy:551` | Mom | "An option is not the same as committing, just like how your rough draft shouldn't be your final draft." |
| 44 | `season1/0524.rpy:697` | Mom | "That is not the same as a budget." |
| 45 | `season1/0526.rpy:329` | MC (nier) | "Useful is not the same as enough." |
| 46 | `season1/0526.rpy:395` | MC (nier) | "I leave with nothing solved, which is not the same as leaving empty-handed." |
| 47 | `season1/0530.rpy:361` | MC narration | "copying instructions is not the same as following them." |

Note the pair at **45** and **46** — same file, same narration voice, 66 lines
apart.

There is also a nearby self-aware beat worth knowing about while reading this
section: `0523.rpy:443`, "Lawyer Mom says not a life sentence. / Add one sin to
the counter. / Lawyer Mom is very careful with sentence length." The narration
is already joking about Mom's habit of this construction.

---

## Appendix A — Where the tic is absent

- **`ooc_1026_passed_out.rpy`** (the drunk-Mom scene): **zero** instances.
  Its negations are all dialogue-natural ("You weren't there. You didn't *see*
  the boat.", "There's no fish."). The pamphlet turn at `:194` uses a bare
  restatement — "a crease across the middle that isn't a crease so much as a
  corner bent right back on itself" — which is the closest it gets, and it
  attaches to a physical object rather than an abstraction.
- **`0515.rpy`, `0516.rpy`, `0522.rpy`, `0531.rpy`**: no T1 or T2 sites. Their
  negations are all conversational fragments ("Not quite.", "Not really.").
- **`s1_choices.rpy`, `s1disc.rpy`**: none.

## Appendix B — Out of scope (spot-check only)

Not part of "main story," listed so the sweep is honest about its edges:

- `game/addons/Character Stories/cs_matsuda_02.rpy:138` — "This is not one of
  those stories. It's something else entirely." (T2)
- `game/addons/Matsuda's Sick Boss Fight/tsubakimode/tsubaki_soul.rpy:819` —
  "It isn't bad. It's like a foot falling asleep, if the foot were most of you,
  and if you'd agreed to it in advance." (T1 — and arguably the best-executed
  instance anywhere in the project)
- `tsubaki_soul.rpy:972` — "it isn't even aiming anymore. It's moving her
  because the arm still moves." (T1)

The character stories were not exhaustively swept.

## Appendix C — Reproducing this sweep

The scan scripts were written to the session scratchpad, not the repo. To
rebuild: flatten every `"..."` string in `game/story/**/*.rpy`, sentence-split
on `(?<=[.!?])\s+`, keep sentences matching a categorial-negation regex
(`isn't|is not|wasn't|were not|^Not\b|,\s*not\b|not (a|an|the|really|exactly)`),
then read each hit against its following 1–3 sentences. That filter yields 303
sites, of which the 47 above survived a read.
