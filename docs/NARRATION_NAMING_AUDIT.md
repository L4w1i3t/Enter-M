# ENTER M — Narration Proper-Noun / Referent-Register Audit

Status: complete corpus sweep, August 19, 2026. **Audit written, then APPLIED
the same day — 155 narration lines rewritten across 18 files.** Lint clean
(0 errors, 0 warnings, 0 unreachable items across 123 source files).

Deliverable: a stated rule for how MC's narration refers to other characters,
plus every violating line addressed by file and line number.

Results are in §8. Two hazards discovered *during* the apply pass, which any
future prose sweep must respect, are in §4a and §4b. The inventory in §7 is the
**pre-pass** snapshot and is kept as the historical record; re-run
`tools/narration_naming_report.py` for current state.

## Scope

| Path | Narration lines | Covered |
| --- | --- | --- |
| `game/story/season1/0515.rpy` – `0531.rpy` (17 files) | 2,494 | yes |
| `game/story/out_of_context/*.rpy` (8 files) | 245 | yes |
| `game/story/season1/exam_guard.rpy` | 144 | yes |
| `game/story/dependency_route.rpy` | 8 | yes |
| `game/story/season1/s1_choices.rpy`, `s1disc.rpy` | 6 | yes |
| `game/story/season2`, `season3`, `seasonintermission` | empty | n/a |

"Narration line" means a bare quoted string with no speaker prefix — MC's
first-person present-tense voice, including `{i}…{/i}` interior thought. Speaker
lines, `nier` blackout narration, screen text, and comments are excluded from the
counts but were read for context.

**Total narration lines analysed: 2,897.**

---

## 1. The complaint, and what the corpus actually shows

The reported problem was consecutive narration lines opening with the same proper
noun:

> "Asahina does this" / "Then Asahina does that" / "Then Asahina does this too"

**That literal pattern is nearly absent.** Across 2,897 narration lines there are
**four** instances of two consecutive narration lines opening with the same name,
and exactly **one** run of four or more consecutive narration lines opening with
any person at all (`ooc_1030_uhoh.rpy:435-439`). Sentence-opener variety is
otherwise healthy:

| How the line opens | Count | Share |
| --- | --- | --- |
| Adverbial / subordinate clause / other | 741 | 25.6% |
| Object or abstraction (`The`, `A`, `It`, `There`…) | 690 | 23.8% |
| `I` / `We` / `My` | 519 | 17.9% |
| Pronoun (`She`, `He`, `They`, `Her`…) | 495 | 17.1% |
| **Proper name** | **452** | **15.6%** |

So the perception is correct but the mechanism was misidentified. Three separate
things generate it, and only the third is a craft failure.

### 1a. Density per scene, not adjacency per line

Name-openers are not evenly spread. They cluster hard in group scenes:

| File | Name-openers / narration lines | Density |
| --- | --- | --- |
| `0531.rpy` | 99 / 280 | **35.4%** |
| `ooc_1030_uhoh.rpy` | 31 / 124 | 25.0% |
| `0516.rpy` | 18 / 77 | 23.4% |
| `0529.rpy` | 32 / 141 | 22.7% |
| `0530.rpy` | 43 / 200 | 21.5% |
| `0523.rpy` | 39 / 184 | 21.2% |
| `0518.rpy` | 18 / 106 | 17.0% |
| `0520.rpy` | 13 / 86 | 15.1% |
| `0525.rpy` | 30 / 220 | 13.6% |
| `0524.rpy` | 28 / 215 | 13.0% |
| *(corpus mean)* | 452 / 2,897 | 15.6% |

Every high-density file except one is a file with three or more named people in a
room. The May 31 arcade sequence re-tags every actor on nearly every line because
the narration never trusts an antecedent to survive one intervening line of
dialogue. At 35% the reader is being handed a name roughly every third line — well
past the point where it reads as courtesy and into the range where it reads as a
tic.

`0516.rpy` is the exception and partly a different problem: it is a *small* file
(77 narration lines) carrying several separate two-hander introductions, so its
T1 share is 33% against the 22% corpus average — proportionally more of its names
are earned first-encounter beats. But that only accounts for 6 of its 18 openers;
the other 12 (3 T2, 9 T3) are ordinary targets. Rank it mid-priority: the density
figure overstates the problem, it does not excuse it.

### 1b. The verb slot is where the drone actually lives

Of 1,099 `<person> <verb>` constructions in narration, the top ten verbs cover
**27%**, and one verb dominates everything:

| Verb after a person-subject | Count |
| --- | --- |
| `looks` | **67** |
| `is` | 49 |
| `has` | 34 |
| `says` | 34 |
| `takes` | 27 |
| `smiles` | 19 |
| `does` | 18 |
| `turns` | 17 |
| `points` | 16 |
| `sits` | 16 |

`Matsuda looks at me` / `Monika looks up` / `Mom looks at the pile growing beside
Asahina` — the subject slot varies, so no duplicate-phrase check ever fires, but
the **construction** is identical. This is why substituting pronouns for names
would not fix the problem on its own: `She looks at me` three times running is the
same drone with a smaller word in it. Any pass that only touches the subject slot
will move the numbers and not the reading experience.

### 1c. The retreat tell — the actual craft failure

This is the finding that matters.

The register MC uses for another character (name vs. pronoun) is currently
**unmotivated** — it alternates at roughly 48/52 with no discernible logic. But
it is not random in its *placement*. Reading the clusters in context, the name
reasserts itself disproportionately on emotionally loaded beats: the narration
runs close and pronoun-anchored through ordinary action, then reaches for the full
name at exactly the moment the scene goes quiet.

`0530.rpy:518-555`, the empty-chair dinner. Asahina is the only other person in
the room, so every name in the passage is optional:

```
"She pulls out the covered leftovers and reads Mom's second note…"
"Her hand rests on the back of Mom's chair."
"She removes the extra bowl and returns it to the cabinet."
"Neither of us says anything while she does it."
"The table looks larger afterward."
mc "Mom said late, not never."
ah "I know."
"Asahina sits."                          <- the flinch
```

Four consecutive close-register references, then the beat lands — Mom's chair, the
extra bowl, the silence — and the camera pulls back to the full name on the
two-word line that needed to stay closest. Same move at `0524.rpy:524`: MC is
holding a poem she wrote, cannot get a sentence out (`"It should be easy to say
something." / "It is not."`), and the narration says **"Monika looks up."** — full
name plus the most generic verb in the corpus, on the most charged line in the
scene.

Unmotivated, this reads as insecure writing: the prose does not trust the reader
to hold an antecedent across two lines. But the placement is not arbitrary, and
that is the opportunity. **MC formalizes when he is uncomfortable.** Made
deliberate, the tic becomes a tell.

---

## 2. Why this is worth doing properly

`0521.rpy:24-45` is a Japanese-literature lesson whose entire subject is this
exact device. The teacher:

> "This kind of prose allows subjects to disappear without the sentence
> collapsing."
> "When a passage repeatedly refuses to identify who acts, the omission does not
> only create ambiguity. It can redistribute guilt."

And MC's correct answer (`:56-58`):

> "It makes the reader participate in assigning culpability."
> "The actions are concrete, but the missing subjects keep responsibility
> unstable."

The scene is a thesis statement about subject omission that the surrounding
70,000 words decline to enact. MC can articulate that withholding a subject forces
the reader to *decide* — and then narrates his own life with compulsive subject
naming that forecloses exactly that participation.

Left as is, a reader who is paying attention gets unintentional lampshading: the
game teaching a technique it visibly cannot perform. Fixed, `0521` retroactively
becomes the key to how the narration works, and the hidden-route material
(`dependency_route.rpy`, the weird-route OOC scenes) inherits a prose grammar that
already knows how to make responsibility unstable on purpose.

This is the argument for treating the fix as characterization rather than as a
find-and-replace.

---

## 3. The rule

MC has four registers available for another character. Currently he uses two, and
picks between them at random.

| Register | Form | What it means |
| --- | --- | --- |
| **Name** | *Monika*, *Asahina*, *Mom* | He is aware of her as a separate person with a name — assessing, cataloguing, newly noticing, or holding her at arm's length. |
| **Pronoun** | *she*, *her* | He is inside the moment with her. Attention continuous; no gap between perceiving and reacting. |
| **Epithet** | *my sister*, *the president* | He is seeing a role rather than a person. Carries warmth or irony depending on context. |
| **Body anchor** | *Her hand*, *Her grip*, *Her card* | He is focused on a part rather than the whole. Highest intimacy, or highest tension. |

> **The rule: the register tracks MC's distance from the person in that moment.**

Applied per line, the test is:

> **Does MC have a reason to re-notice her as a named person right now?**

- **Yes, and the reason is narrative** — she just walked in, attention has been
  elsewhere, she is a stranger, she is being an authority. Keep the name.
- **Yes, and the reason is emotional retreat** — the beat is uncomfortable and he
  is stepping back from it. Keep the name, and this is now doing work. Do not
  "fix" these; they are the payoff.
- **No** — the name is the author disambiguating for the reader, not MC noticing.
  Convert to one of the other three registers.

### The corollary that resolves the group scenes

In a scene with three or more people the reader genuinely does need to know who
acted, and 62% of all name-openers fall in that case. But that is an
**information** problem, and the name is only one of four ways to solve it. The
other three — body anchor, object-lead, and folding two beats into one sentence so
a single antecedent governs both — all disambiguate without spending the
distance register. That is the bulk of the work in `0531` and `ooc_1030_uhoh`.

### Character-specific notes

- **Everyone goes by given name** (Western order: *Matsuda Akai*, *Tsubaki
  Kareda*), so there is no surname/given-name axis to exploit. The dial is
  naming vs. not-naming.
- **Mom** is a name, not a common noun (see the existing capitalization rule) and
  it is already the intimate register. The dial inverts for her: the retreat tell
  is MC *avoiding* referring to her at all, narrating the room instead of the
  person. Do not pronoun-substitute Mom for variety alone.
- **Asahina** is the sister, so `my sister` is live as an epithet, and it is
  already the sibling-frame register in 11 existing uses.
- **Kotonoha** is close to correct already (10 name-openers, mostly first-contact
  beats where distance is the point).

### Epithet budget

Epithets are the technique most likely to be over-applied and become the next tic.
Hard limits for the apply pass:

- `my sister` — currently 11. **Cap at 18 across season 1.**
- `the president` / `the vice president` — currently 2. **Cap at 6**, and only
  where the office is genuinely what is operating (club business, authority jokes).
- `the coach` — free, he is a role character.
- **Never introduce appearance epithets.** No *the redhead*, *the green-eyed
  girl*, *the taller one*. The corpus narration is currently clean of these and
  they are a worse tic than the one being fixed. (`redhead` appears once, in
  Asahina's dialogue at `0530.rpy:520`, which is characterization and stays.)

---

## 4. Move catalog

Each inventory row below carries a suggested move. **These are starting
suggestions from context, not verdicts** — the apply pass makes the prose call.

| Code | Move | Use when |
| --- | --- | --- |
| **K** | Keep the name | First naming in a scene beat, or a deliberate retreat tell. |
| **C** | Cut the echo | The namebox on the immediately preceding line already said who this is. |
| **P** | Pronoun | Established, unambiguous, MC is inside the moment. |
| **B** | Body anchor | Open on the possessive — `Her hand`, `Her grip`. Disambiguates *and* tightens. |
| **F** | Fold | Merge into the neighbouring sentence so one antecedent governs both beats. |
| **O** | Object-lead / restructure | Group scenes. Open on the object, gesture, or result instead of the actor. |

Distribution of suggested moves across the 452:

| Move | Count |
| --- | --- |
| O — object-lead / restructure | 238 |
| K — keep | 98 |
| P — pronoun | 58 |
| B — body anchor | 37 |
| C — cut namebox echo | 16 |
| F — fold | 5 |

### Tiers

| Tier | Definition | Count | Share |
| --- | --- | --- | --- |
| **T1** | First naming of this person in the scene beat | 98 | 22% |
| **T2** | Already established, no rival same-gender referent in scope | 74 | 16% |
| **T3** | Another woman on stage or recently speaking — the name is disambiguating | 280 | 62% |

Tier assignment is mechanical: a scene beat resets on every `scene` statement;
"in scope" means on stage via `show`/`hide` tracking, or among the last four
speakers, or named elsewhere in the same line. T1 is a keep-list. T2 is the
low-risk pass. T3 is the real work and cannot be done by substitution.

---

## 4a. Callback dependencies — check before changing any gesture

**Discovered during the apply pass, after nearly breaking one.** A gesture is not
always local. Several are the setup half of a deliberate setup/payoff pair, and
the payoff can be fifty lines or two in-game days away.

The near-miss: `0523.rpy:150` was `"Tsubaki smiles, but it arrives a little
late."` Removing the smile looked like an obvious de-duplication — until
`0523.rpy:288` turned out to read *"It's also the first one today that arrived on
time."* The late smile is load-bearing. It was restored (sharpened to `half a
second late`, which sets up `on time` more crisply), and the redundant
suppression at `:139` was recast instead.

**Before altering a gesture, grep forward for its payoff.** These phrases mark a
line that depends on an earlier one:

> `this time` · `again` · `the first one` · `the same one` · `for once` ·
> `not the first` · `second time` · `still` · `unlike` · `the way she did`

Known live dependencies in the corpus:

| Payoff | Depends on |
| --- | --- |
| `0523.rpy:288` "the first one today that arrived on time" | the late smile at `:150` |
| `0530.rpy:162` "Her smile stays this time" | the audited smile at `:158` |
| `0517.rpy:398` "bows once more, smaller this time" | the earlier bow |
| `0529.rpy:331` "the quick read again, the contract read" | `0529.rpy:36` |
| `0523.rpy:397` "does not shout this time" | Coach's earlier shouting |
| `0519.rpy:329` "less like a spotlight this time" | `0519.rpy:293` |
| `0522.rpy:314` "No nickname this time" | Matsuda's nickname habit |
| `0531.rpy:514` "The sleeve stays where it is" | `0531.rpy:510` |

## 4b. Worn constructions — the second axis

Name density was only half the problem. The other half is **frames**: syntactic
constructions that read fine once and mechanical by the tenth time. Measured
across all narration:

| Construction | Uses | Verdict |
| --- | --- | --- |
| `<person> looks …` | 67 | **Cut to 27.** Was 2.5× the next verb; the drone lived here. |
| `before X can …` | ~46 | Flagged in the existing repetition audit. Left alone this pass. |
| `She/He says it …` | 24 | Cut to 21. Three opened `says it lightly, but` — two recast. |
| `of/like someone (who)` | 19 | MC's signature move; kept. One adjacent pair at `0519:293`/`:329` split. |
| `enough to / enough that` | ~18 | Left alone. |
| `pretending not to` | 7 | Left alone; watch it. |
| `in a way that` | 6 | Left alone. |

Two rules that came out of doing the work:

1. **Pronoun substitution alone fixes nothing.** `She looks at me` three times is
   the same drone as `Matsuda looks at me` three times. The verb slot has to move
   with the subject slot.
2. **Every replacement is a new tic in waiting.** Mid-pass, five freshly written
   lines in `0531` alone had converged on `comes up` / `comes down` / `comes off`,
   and one rewrite duplicated an existing `pretending not to enjoy`. Sweep your
   own additions for repetition before declaring a file done — the probe list in
   the apply notes exists for exactly this.

## 5. Highest-value passages

Six passages where the fix changes the reading experience rather than the
statistics. Excerpts are identifying fragments; rewrites are illustrative.

### 5.1 — `0530.rpy:546` — the empty chair (P1)

The retreat tell in its purest form, quoted in §1c. The passage runs four close
references, lands the empty-chair beat, then formalizes.

```
- "Asahina sits."
+ "She sits."
```

Two words, and the camera stays in the room. `:527` (`Asahina drops her bag beside
the chair and opens the refrigerator`) and `:555` (`Asahina's phone lights beside
her bowl`) are also T2 in this beat — `:555` is a clean **B** (`Her phone lights
beside her bowl`). Keep `:518` (`Asahina comes in not long after me…`): she is
entering, that is a real re-notice.

### 5.2 — `0524.rpy:506-524` — the poem exchange (P1)

Seven name-openers (`:478`, `:480`, `:492`, `:506`, `:508`, `:520`, `:524`) with
Monika as the only other named person in the room, and the worst of them on the
most charged line.

`:508` is the outright redundancy — the previous line already established the
standing and the notebook, and this one repeats both plus the name:

```
- "Monika stands and brings her notebook to my desk once the timer on her phone buzzes."
- "The voluntary exchange becomes voluntary once Monika is standing there with her notebook."
+ "Monika stands and brings her notebook to my desk once the timer on her phone buzzes."
+ "The voluntary exchange becomes voluntary once she is standing there with it."
```

`:524` is the flinch, and also the corpus's dominant verb:

```
- "Monika looks up."
+ "Her eyes come up."
```

Keep `:478` (entrance) and `:480` (`Monika turns when she hears the door` — she is
reacting to *him* arriving, a genuine re-notice).

### 5.3 — `0531.rpy:436-476` — the arcade, light-gun stretch (P1)

The densest passage in the game: 99 name-openers across the file, and this
stretch names three people in a four-person scene on nearly every line. Two things
are happening and they need opposite treatment.

The triadic comparison lines are **KEEP** — the naming *is* the joke structure,
one clause per player:

> `:464` "Matsuda takes the left side. I take the right. Tsubaki stands between us
> and quietly rescues every civilian…"

But `:465` immediately repeats the identical triad shape, and that is what makes
the passage feel mechanical — not the names, the **structure**:

> `:465` "Matsuda shoots anything with a health bar. I reload at the wrong times.
> Tsubaki finishes the first stage with the highest accuracy…"

Fix by breaking the second triad, not by renaming: collapse two of its three
clauses, or lead on the score readout. Then `:463` and `:471` (`Tsubaki lowers the
gun`) go **O**/**B** — the scene has only one person holding a gun.

### 5.4 — `0529.rpy:375-470` — the deck-building game (P2)

Thirteen `Mom` references in one beat, the largest single-name cluster in the
corpus. Genuinely three-handed (Mom / Asahina / MC), so most are T3 — but the
board game supplies an unusual amount of *object* to lead on (the market row, the
piles, the Crown, the Province) and almost none of it is being used. This is the
best test case for whether **O** carries a long group scene on its own. Do it
early in the apply pass; if object-lead works here it works anywhere.

### 5.5 — Namebox echoes (P3, 18 lines, mostly mechanical)

Eighteen narration lines open with the name of the character who spoke the
*immediately preceding* line, where the namebox has already said it. These are
the closest thing to free cuts in the audit:

`ooc_1026_passed_out.rpy:141` · `ooc_1030_uhoh.rpy:316`, `:342`, `:381` ·
`0518.rpy:399` · `0521.rpy:227`, `:284` · `0523.rpy:397` · `0524.rpy:263` ·
`0528.rpy:471` · `0529.rpy:405` · `0530.rpy:478`, `:546`, `:555` ·
`0531.rpy:453`, `:811`, `:861` · `exam_guard.rpy:683`

Sixteen carry move **C**. Two do not, and should not: `ooc_1030_uhoh.rpy:316`
names Matsuda later in the same line, so it is a comparison and takes **O**; and
`ooc_1030_uhoh.rpy:381` (`Matsuda's hands come down`) is already a possessive and
wants **B** rather than a flat deletion.

### 5.6 — The `looks` monopoly (P2, cross-file)

67 uses of `looks` directly after a person-subject, plus 9 `glances` and 8
`watches`. No single instance is wrong; the aggregate is. Target roughly half.
Most are replaceable by naming what was actually seen, which usually also removes
the name and the verb in one move (`Monika looks up` → `Her eyes come up`;
`Mom looks at the pile growing beside Asahina` → `The pile beside Asahina has
Mom's attention`). Run this pass **after** the tier work so the two do not fight
over the same lines.

---

## 6. Apply-pass order

1. §5.5 namebox echoes — 16 lines, mechanical, no judgment.
2. T2 (74 lines) — pronoun / body anchor / fold. Low risk.
3. T3 by file, worst-first: `0531` → `0530` → `0523` → `0529` → `ooc_1030_uhoh`
   → `0525` → `0524` → `0516` → remainder.
4. §5.6 verb-slot pass.
5. Re-measure and lint.

### Re-measure

`tools/narration_naming_report.py` reproduces every figure in this document and
is the check for the apply pass:

```
python tools/narration_naming_report.py                 # summary + density table
python tools/narration_naming_report.py --tier T2 --list # work a single tier
python tools/narration_naming_report.py --csv rows.csv   # full inventory
```

Targets after the pass:

- Name-openers: **452 → ~300** (15.6% → ~10%).
- No file above **22%** density (currently `0531` at 35%).
- `looks` after a person-subject: **67 → ~35**.
- T1 count **unchanged at 98** — if re-establish lines are dropping, the pass has
  gone too far and antecedents are being lost.

The last check is the important one. The failure mode of this work is stripping
names until the reader loses track of who is in the room, which is a worse defect
than the one being fixed.

---

## 8. Results of the apply pass

155 narration lines rewritten across 18 files, August 19 2026.

| Measure | Before | After | Target |
| --- | --- | --- | --- |
| Name-opening narration lines | 452 (15.6%) | **367 (12.7%)** | ~300 (~10%) |
| T1 re-establish (guard rail) | 98 | **98** | unchanged |
| T2 free to vary | 74 | **30** | — |
| T3 disambiguating | 280 | **239** | — |
| Namebox echoes | 18 | **4** | 0–5 |
| `looks` after a person-subject | 67 | **27** | ~35 |

**The guard rail held exactly.** T1 is unchanged at 98, so no re-establishing
line was lost and no antecedent was stripped past the point of legibility. That
was the failure mode named in §6 and it did not happen.

`looks` beat its target and is no longer the dominant verb — the distribution is
now flat, led by unavoidable copulas (`is` 49, `has` 34) rather than a single
overused action verb.

Lines changed by file: `0531` 48 · `0523` 24 · `0530` 20 · `0524` 11 · `0525` 8 ·
`0518` 7 · `0528` 7 · `0529` 5 · `0516` 5 · `ooc_1030_uhoh` 5 · `0520` 3 ·
`0515` 2 · `0519` 2 · `0521` 2 · `0522` 2 · `ooc_1026_passed_out` 2 ·
`0526` 1 · `exam_guard` 1.

Also fixed in passing: `0524.rpy:245` used British `whilst`, and
`s1_choices.rpy:84` used `colours` — both against the project's American-spelling
convention.

### What did not reach target

Two files remain above the 22% density line:

- **`0531.rpy` — 26.1%** (was 35.4%). The arcade day is the highest-cast file in
  the game: four named characters plus Mom, most of it in group scenes where the
  name is the only thing telling the reader who acted. Pushing further would have
  started removing genuinely load-bearing names.
- **`ooc_1030_uhoh.rpy` — 24.2%** (was 25.0%). Six people at one cafeteria table.
  The file is also *later, better-written* prose than season one — most of its
  name-openers are already doing real work, so there was little to take.

**A measurement caveat that flatters neither number:** the script counts source
lines, not lines a player sees. `0531.rpy` has three menu branches that each
carry `"Matsuda's thumb goes still on the sugar packet."`, of which exactly one
displays per playthrough. Branch-heavy files are over-counted, so true
per-playthrough density in both files is lower than reported.

### Remaining work

- `before X can` (~46 uses) — the largest untouched construction. Belongs with
  the existing repetition audit, which already catalogs it.
- `pretending not to` (7).
- The exam-answer ritual lines in `0527`/`0528` (`"I circle it and keep going."`
  and three others, 4× each) are verbatim repeats *by design* — an exam montage,
  and each pair sits in a different `if/else` route branch. Deliberate. Left
  alone, recorded here so a future sweep does not "fix" them.

---

## 9. Second pass — the calibration tic (August 19, 2026)

A voice-consistency read of the full main story followed the naming pass. It
confirmed MC's voice is consistent and that **the legal register is healthy and
should stay**: ~200 lines in 4,534 (about 1 in 23), and the densest passage
anywhere is only 5-in-15 — `0530:613-627`, where he and his lawyer mother
deliberately riff in courtroom language over cucumbers. That is the ideal form of
the tic: diegetic, *shared between two characters* so it reads as family culture
rather than narrator quirk, and funny. The peak file, `0526` at 10.9%, is the
civics exam, where the vocabulary is the subject matter.

But the legal jargon was **not** MC's only tic, and it was not his biggest. Four
constructions were larger, none of them legal, and all four do the same job:

> **MC never states a thing plainly. He states it, calibrates its exact degree,
> then tells you what the degree means.**

That is the mechanism that takes interpretation away from the reader — the same
failure §2 describes. `0521` says withholding the actor makes the reader
*decide*; these constructions supply the degree **and** the verdict, leaving
nothing to decide.

| Construction | Before | After |
| --- | --- | --- |
| `X enough to / enough that Y` — the calibration | **93** | **47** |
| `, which is / means / tells …` — the appended verdict | **43** | **29** |
| `which is how I know/notice` — the explicit caption | 4 | **1** |
| `It comes out [X] than I meant` | 3 | **1** |
| `with the [noun] of someone who …` — attributed-manner simile | 20 | **17** |

70 lines rewritten across 17 files. Lint clean. Displayed word count 104,884 →
104,667.

### The method: subtract the verdict, keep the observation

The fix is almost never a synonym and almost never a pure deletion. It is
**cutting the second half of the sentence and letting the first half stand**,
then — where there is room — spending the reclaimed space on something concrete
rather than something interpretive.

```
- "Tsubaki moves fast enough to make it obvious how much she wanted to be asked."
+ "Tsubaki moves before the sentence is finished."

- "Mom lets me, which tells me more about the day than the folders do."
+ "Mom lets me."

- "She lets that one go, which is how I know she is already tired."
+ "She lets that one go. Normally she would not."

- "The opening starts with a thunderclap loud enough to make someone in the
   front three rows jump."
+ "The opening starts with a thunderclap. Someone in the front three rows jumps."
```

Where a cut left room, the replacement adds **observation or narrative thread**,
never a fresh verdict:

- `0516:226` — "which has quietly become one of the school's accepted facts" →
  *"Nobody I know has ever seen her arrive."* Feeds Kotonoha's omnipresence motif.
- `0518:149` — "cheerful enough to make the screen feel brighter" → *"still
  wearing more exclamation points than the sentence needed."* Calls back to the
  punctuation motif established at `0517:221`.
- `0523:516` — cut "just enough to make me remember this is really something I
  have to worry about." The underline is now ominous instead of explained.
- `0517:248` — "bright enough to cut through the evening air" → *"pitched to
  carry"*, which characterizes Matsuda's theatricality before she is introduced.

### What was deliberately kept

Not every instance is a tic. Kept: rhetorical pairs (`0527:278-279`,
`exam_guard:464-465`, `0525:784`); jokes where the construction *is* the joke
(`0530:81` "suspended long enough to qualify for air traffic control",
`0531:393` "screens wide enough to support poor judgment", `0521:32` "which is
usually how teachers hide knives", `0530:138` "which feels like making the victim
write the incident report"); literal measurements of time or distance; and
`0525:650` "just enough to restore the ecosystem", which is a deliberate
pun-bridge into `0525:651` "Ecology comes next."

### Two duplicate jokes found while reading

- `0519:52` "the foot … files a brief, formal complaint" and `0522:79` "gives my
  spine the chance to briefly file its own complaint" were the same
  body-part-files-a-complaint joke. `0522:79` was recast.
- `0518:446` / `0519:261` / `0519:370` were three near-identical `It comes out
  [X] than I meant it to` lines carrying three different emotional registers
  (vulnerable / blunt / cruel). `0519:261` was kept as the canonical one; the
  other two were differentiated.

### Standing rule

MC may **notice**. He may not **conclude** on the reader's behalf. When a
narration line has two halves and the second explains the first, the second half
is usually the one to cut.

---

## 7. Full inventory

**Pre-pass snapshot**, retained as the historical record — 85 of these rows have
since been rewritten. Run `tools/narration_naming_report.py --list` for current
state.

452 rows, every name-opening narration line in the corpus, by file and line.
Excerpts truncated at 115 characters. `rivals` lists the other same-gender
referents in scope that make a row T3.

### `game/story/season1/0515.rpy`

10 name-openers — T1 keep 5 · T2 2 · T3 3

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 62 | Monika | T1 | K | Monika flicks up her hand. |
| 69 | Monika | T2 | P | Monika flips the card toward me as if it were a coin, and I catch it between two fingers mostly by accident. |
| 94 | Monika | T1 | K | Monika shrugs. There are bags under her eyes that weren't there last week. |
| 100 | Monika | T2 | P | Monika takes the pages and reads the way she always does: lips slightly parted, pen capped but held ready, like … |
| 158 | Monika | T1 | K | Monika waltzes to the door and begins her exit. |
| 247 | Mom | T1 | K | Mom's already at the counter, prepping different vegetables and a spice mix. |
| 281 | Monika | T1 | K | {i}Monika's probably had this figured out since the day she started primary or something.{/i}<br><sub>rivals: Mom</sub> |
| 328 | Asahina | T3 | O | Asahina pauses before picking up her chopsticks and nudging the pork slightly.<br><sub>rivals: Mom</sub> |
| 331 | Mom | T3 | O | Mom watches a beat longer than the moment needs, then makes herself look at her own plate. The chopsticks in her…<br><sub>rivals: Asahina</sub> |
| 375 | Asahina | T3 | O | Asahina sighs and takes a subtle bow.<br><sub>rivals: Mom</sub> |

### `game/story/season1/0516.rpy`

18 name-openers — T1 keep 6 · T2 3 · T3 9

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 34 | Mom | T1 | K | Mom is at the counter when I come in, elegantly moving between the toaster and the stove. |
| 36 | Asahina | T1 | K | Asahina sits at the table with her head tilted over one shoulder while she tries to fix a twist in her sleeve wi…<br><sub>rivals: Mom</sub> |
| 44 | Asahina | T3 | O | Asahina catches me looking at the sleeve and narrows her eyes.<br><sub>rivals: Mom</sub> |
| 48 | Mom | T3 | O | Mom plates the eggs and sets them down.<br><sub>rivals: Asahina</sub> |
| 68 | Asahina | T3 | B | Asahina's expression tightens by about one millimeter.<br><sub>rivals: Mom</sub> |
| 156 | Monika | T1 | K | Monika is already here, flipping through a thin notebook with a pen tucked behind her ear. Nobody else is. |
| 169 | Monika | T2 | P | Monika closes her notebook halfway, keeping one finger between the pages. |
| 235 | Kotonoha | T2 | P | Kotonoha adjusts the bag in her hand. The convenience store logo crinkles under her fingers. |
| 245 | Kotonoha | T2 | P | Kotonoha steps back without looking down. |
| 287 | Asahina | T1 | K | Asahina is standing near the couch, arms folded in a way she keeps adjusting.<br><sub>rivals: Sam</sub> |
| 299 | Asahina | T3 | O | Asahina elbows him in the side, but he takes it like he saw it coming five seconds ago.<br><sub>rivals: Sam</sub> |
| 328 | Mom | T3 | O | Mom points at my sister.<br><sub>rivals: Asahina, Sam</sub> |
| 335 | Sam | T3 | B | Sam's eyes flick to Asahina for half a second before he answers, the way you check a gauge only you can read.<br><sub>rivals: Asahina, Mom</sub> |
| 379 | Sam | T3 | O | Sam smiles in a rather giddy way, contrasting everything I've seen up to this point.<br><sub>rivals: Mom</sub> |
| 381 | Asahina | T1 | K | Asahina, from the living room, makes a triumphant noise.<br><sub>rivals: Mom, Sam</sub> |
| 386 | Sam | T3 | O | Sam dries his hands and glances toward the living room.<br><sub>rivals: Asahina, Mom</sub> |
| 396 | Mom | T3 | O | Mom looks between us, then goes back to the containers.<br><sub>rivals: Sam</sub> |
| 421 | Mom | T1 | K | Mom says something after that, too faint for me to catch. |

### `game/story/season1/0517.rpy`

12 name-openers — T1 keep 4 · T2 2 · T3 6

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 13 | Asahina | T1 | K | Asahina is crouched near the shoe rack, fixing the heel of her loafer with the intensity of emergency surgery.<br><sub>rivals: Mom</sub> |
| 20 | Mom | T3 | O | Mom gives me the look she reserves for sentences she chooses not to dignify.<br><sub>rivals: Asahina</sub> |
| 29 | Mom | T3 | O | Mom smiles into her coffee, and Asahina sees it and immediately looks away.<br><sub>rivals: Asahina</sub> |
| 35 | Mom | T3 | O | Mom snaps her fingers and gestures out the door.<br><sub>rivals: Asahina</sub> |
| 156 | Kotonoha | T1 | K | Kotonoha is at the register when I get there. |
| 183 | Asahina | T1 | K | Asahina meets me home at the door with a strip of masking tape stuck to her sleeve. |
| 201 | Asahina | T2 | P | Asahina snorts, then retreats toward the living room before I can inspect the poster. |
| 291 | Tsubaki | T3 | O | Tsubaki gives me a small, mortified bow.<br><sub>rivals: Matsuda</sub> |
| 325 | Tsubaki | T3 | B | Tsubaki's mouth twitches and loses the fight. The laugh gets out through her nose anyway.<br><sub>rivals: Matsuda</sub> |
| 331 | Matsuda | T3 | O | Matsuda has already pulled out her phone.<br><sub>rivals: Tsubaki</sub> |
| 431 | Asahina | T1 | K | Asahina is on the living room floor when I come back in, surrounded by poster board, paper cutouts, and the desp… |
| 442 | Asahina | T2 | P | Asahina repeats the name under her breath, testing it against whatever rumor index she keeps in her head. |

### `game/story/season1/0518.rpy`

18 name-openers — T1 keep 5 · T2 6 · T3 7

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 33 | Asahina | T2 | P | Asahina lightly punches my shoulder. |
| 97 | Asahina | T2 | P | Asahina looks at me, unamused. |
| 167 | Monika | T1 | K | Monika lifts a hand as she comes through the crowd. Her pace is quick until she sees me, then it eases. |
| 193 | Monika | T2 | B | Monika's expression shifts, just a little. Not alarmed. |
| 197 | Monika | T2 | P | Monika folds her ticket against her palm and nods toward the entrance. |
| 218 | Monika | T1 | K | Monika steps up beside me and studies the menu board.<br><sub>rivals: Kotonoha</sub> |
| 227 | Monika | T3 | O | Monika glances at me.<br><sub>rivals: Kotonoha</sub> |
| 233 | Kotonoha | T3 | O | Kotonoha taps the order in, then reaches for two cups without looking away from the register.<br><sub>rivals: Monika</sub> |
| 250 | Monika | T1 | K | Monika pays before I get my wallet halfway out.<br><sub>rivals: Kotonoha</sub> |
| 253 | Monika | T3 | O | Monika looks down first, busying herself with the cup lids.<br><sub>rivals: Kotonoha</sub> |
| 262 | Kotonoha | T3 | O | Kotonoha nods once and turns to the next customer.<br><sub>rivals: Monika</sub> |
| 264 | Monika | T3 | O | Monika balances both drinks against her chest, then leans one toward me.<br><sub>rivals: Kotonoha</sub> |
| 289 | Monika | T1 | K | Monika finds our row before I do. |
| 316 | Monika | T2 | P | Monika tries not to smile and fails miserably. |
| 341 | Monika | T2 | B | Monika's hand closes around my sleeve. |
| 399 | Kotonoha | T3 | C | Kotonoha gathers abandoned napkins from the counter and stacks them with precision.<br><sub>rivals: Monika</sub> |
| 405 | Monika | T1 | K | Monika laughs into her cup lid.<br><sub>rivals: Kotonoha</sub> |
| 417 | Monika | T3 | O | Monika and I drift toward the doors with the crowd.<br><sub>rivals: Kotonoha</sub> |

### `game/story/season1/0519.rpy`

8 name-openers — T1 keep 2 · T2 1 · T3 5

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 30 | Matsuda | T1 | K | {i}Matsuda Akai.{/i} Saved Saturday, untouched since. |
| 84 | Mom | T3 | O | Mom holds my eye a half second past the comfortable mark.<br><sub>rivals: Asahina</sub> |
| 262 | Matsuda | T2 | P | Matsuda freezes mid-gesture, one hand still lifted like she was about to address a balcony that does not exist. |
| 353 | Asahina | T3 | O | Asahina focuses very hard on her rice.<br><sub>rivals: Mom</sub> |
| 356 | Matsuda | T1 | K | Matsuda's hallway entrance flashes through my head with all the subtlety it lacked in person.<br><sub>rivals: Asahina, Mom</sub> |
| 364 | Asahina | T3 | B | Asahina's chopsticks pause in midair.<br><sub>rivals: Mom</sub> |
| 387 | Mom | T3 | O | Mom talks about a coworker who keeps labeling food in the shared fridge but never actually brings anything worth…<br><sub>rivals: Asahina</sub> |
| 388 | Asahina | T3 | O | Asahina complains about volleyball practice in the tone of someone who likes it too much to quit.<br><sub>rivals: Mom</sub> |

### `game/story/season1/0520.rpy`

13 name-openers — T1 keep 6 · T2 3 · T3 4

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 42 | Mom | T2 | F | Mom sets her work bag on one chair and starts the kettle with the tired precision of someone who has already bee… |
| 57 | Mom | T2 | P | Mom checks her phone, then turns it facedown before the screen can ask more of her. |
| 132 | Monika | T1 | K | Monika is at the front desk with a stack of papers and the unmistakable posture of someone pretending she is not… |
| 147 | Monika | T2 | P | Monika returns to her notebook, pen moving in small, neat lines. |
| 234 | Asahina | T1 | K | Asahina is on the floor by the coffee table with one controller in her lap, and Sam is on the couch leaning forw…<br><sub>rivals: Sam</sub> |
| 256 | Asahina | T3 | O | Asahina hands me the crappy third-party AngryDawgz controller.<br><sub>rivals: Sam</sub> |
| 303 | Matsuda | T1 | K | Matsuda, probably, sending another progress report from whatever digital battlefield she has thrown herself into.<br><sub>rivals: Asahina, Sam</sub> |
| 311 | Asahina | T3 | O | Asahina points at him like she has discovered corruption at the highest level.<br><sub>rivals: Sam</sub> |
| 312 | Sam | T3 | O | Sam smiles back, completely unbothered.<br><sub>rivals: Asahina</sub> |
| 327 | Sam | T1 | K | Sam leaves a little before Mom said she'd get back.<br><sub>rivals: Mom</sub> |
| 330 | Asahina | T1 | K | Asahina walks him to the door, which is frankly to be expected of teenagers in that particular phase of puppy love.<br><sub>rivals: Sam</sub> |
| 349 | Asahina | T3 | O | Asahina follows him just far enough to say whatever goodbye did not qualify for indoor broadcast.<br><sub>rivals: Sam</sub> |
| 381 | Mom | T1 | K | Mom gets home late enough that I only catch the sound of the front door opening through the small gap between my… |

### `game/story/season1/0521.rpy`

9 name-openers — T1 keep 2 · T2 0 · T3 7

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 169 | Tsubaki | T3 | B | Tsubaki's fingers tighten around the paper bag, just enough for the sound to answer before she does.<br><sub>rivals: Asahina</sub> |
| 185 | Tsubaki | T3 | O | Tsubaki says her words a tad softly, and for some reason that makes it harder to joke over.<br><sub>rivals: Asahina</sub> |
| 188 | Tsubaki | T3 | O | Tsubaki shifts one foot back toward the door.<br><sub>rivals: Asahina</sub> |
| 203 | Asahina | T1 | K | Asahina's confidence takes up space without asking, and Tsubaki's caution almost stumbles over itself.<br><sub>rivals: Tsubaki</sub> |
| 227 | Tsubaki | T3 | C | Tsubaki pauses, then looks down at her food as if she said more than she meant to.<br><sub>rivals: Asahina</sub> |
| 260 | Asahina | T3 | O | Asahina groans like the school has personally betrayed her.<br><sub>rivals: Tsubaki</sub> |
| 284 | Coach | T3 | C | Coach's voice cuts across the infield before I can pretend to tie an already tied shoe. |
| 415 | Mom | T3 | B | Mom's the one who fills the kitchen with noise like pot lids being lopsided and some random ass podcast about a …<br><sub>rivals: Asahina</sub> |
| 439 | Asahina | T1 | K | Asahina twists spaghetti around her fork with a grim concentration. |

### `game/story/season1/0522.rpy`

10 name-openers — T1 keep 2 · T2 0 · T3 8

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 95 | Mom | T1 | K | Mom's mug is gone too, which means the case from work has claimed her before breakfast could become a family act… |
| 165 | Monika | T1 | K | Monika is between them in spirit, if not yet in actual proximity.<br><sub>rivals: Hikari, Homura</sub> |
| 179 | Monika | T3 | B | Monika's expression enters emergency management mode.<br><sub>rivals: Hikari, Homura</sub> |
| 195 | Hikari | T3 | O | Hikari crosses her arms.<br><sub>rivals: Homura, Monika</sub> |
| 196 | Homura | T3 | O | Homura looks at the paper instead of either of us.<br><sub>rivals: Hikari, Monika</sub> |
| 215 | Hikari | T3 | O | Hikari stares at her for a second.<br><sub>rivals: Homura, Monika</sub> |
| 226 | Homura | T3 | O | Homura catches herself and goes quiet.<br><sub>rivals: Hikari, Monika</sub> |
| 239 | Hikari | T3 | B | Hikari's arms loosen by about half an inch.<br><sub>rivals: Homura, Monika</sub> |
| 253 | Homura | T3 | B | Homura's mouth opens.<br><sub>rivals: Hikari, Monika</sub> |
| 259 | Hikari | T3 | O | Hikari looks at her.<br><sub>rivals: Homura, Monika</sub> |

### `game/story/season1/0523.rpy`

39 name-openers — T1 keep 7 · T2 5 · T3 27

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 15 | Mom | T1 | K | Mom has already dressed for work, but she hasn't left yet. That alone makes the morning feel almost ceremonial.<br><sub>rivals: Asahina</sub> |
| 20 | Mom | T3 | O | Mom looks over her case folder without changing expression.<br><sub>rivals: Asahina</sub> |
| 22 | Asahina | T3 | O | Asahina lowers her eyes back to her plate, the facetious comment flying over her head.<br><sub>rivals: Mom</sub> |
| 42 | Mom | T3 | B | Mom's gaze flicks to her, then back to me.<br><sub>rivals: Asahina</sub> |
| 48 | Asahina | T3 | O | Asahina makes the tiny nose-sound she makes when she almost laughs and decides not to spend the energy.<br><sub>rivals: Mom</sub> |
| 50 | Mom | T3 | O | Mom closes her folder and stands, and just like that the future gets put into a work bag for later.<br><sub>rivals: Asahina</sub> |
| 74 | Asahina | T1 | K | Asahina finds me before I've decided where to eat. |
| 82 | Asahina | T2 | F | Asahina walks half a step ahead of me, lunch bag swinging from one hand, phone in the other. |
| 95 | Tsubaki | T1 | K | Tsubaki is sitting near the same shaded wall from Wednesday. |
| 116 | Tsubaki | T3 | O | Tsubaki moves fast enough to make it obvious how much she wanted to be asked.<br><sub>rivals: Asahina</sub> |
| 118 | Tsubaki | T3 | O | Tsubaki eats neatly. Asahina eats like an office worker with thirty seconds left of her break.<br><sub>rivals: Asahina</sub> |
| 139 | Tsubaki | T3 | O | Tsubaki smiles into her food before she can stop herself.<br><sub>rivals: Asahina</sub> |
| 150 | Tsubaki | T3 | O | Tsubaki smiles, but it arrives a little late.<br><sub>rivals: Asahina</sub> |
| 161 | Asahina | T3 | O | Asahina glances at me, then back at Tsubaki.<br><sub>rivals: Tsubaki</sub> |
| 165 | Tsubaki | T3 | B | Tsubaki's next bite waits untouched for a while before she eats it.<br><sub>rivals: Asahina</sub> |
| 172 | Matsuda | T1 | K | Matsuda steps through with one hand lifted near her face and a folded sheet of paper pinched between two gloved …<br><sub>rivals: Asahina, Tsubaki</sub> |
| 179 | Tsubaki | T3 | O | Tsubaki closes her eyes.<br><sub>rivals: Asahina, Matsuda</sub> |
| 243 | Tsubaki | T3 | O | Tsubaki looks down at her yellow notebook like she has been personally called out by an inanimate object.<br><sub>rivals: Asahina, Matsuda</sub> |
| 262 | Tsubaki | T3 | O | Tsubaki doesn't answer that, but she doesn't close the notebook, either.<br><sub>rivals: Asahina, Matsuda</sub> |
| 274 | Tsubaki | T3 | O | Tsubaki blinks at me.<br><sub>rivals: Asahina, Matsuda</sub> |
| 293 | Tsubaki | T3 | O | Tsubaki chuckles.<br><sub>rivals: Asahina, Matsuda</sub> |
| 302 | Matsuda | T3 | O | Matsuda, who has been standing there this whole time with the patience of someone waiting for a cue, decides she…<br><sub>rivals: Asahina, Tsubaki</sub> |
| 315 | Matsuda | T3 | O | Matsuda looks at me again.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 323 | Matsuda | T3 | O | Matsuda turns back to her friend.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 333 | Tsubaki | T3 | O | Tsubaki reaches into her lunch bag and pulls out a small wrapped rice cracker, then she holds it up without a word.<br><sub>rivals: Asahina, Matsuda</sub> |
| 335 | Matsuda | T3 | O | Matsuda looks at it, then at her.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 357 | Tsubaki | T3 | O | Tsubaki presses her lips together.<br><sub>rivals: Asahina, Matsuda</sub> |
| 366 | Asahina | T3 | B | Asahina's mouth opens like she has a joke ready but ultimately lets it go.<br><sub>rivals: Tsubaki</sub> |
| 369 | Asahina | T3 | O | Asahina gives me a look.<br><sub>rivals: Tsubaki</sub> |
| 378 | Asahina | T3 | O | Asahina laughs, not because the line is sharp, but because Tsubaki actually offered it.<br><sub>rivals: Tsubaki</sub> |
| 397 | Coach | T3 | C | Coach does not shout this time. |
| 488 | Mom | T1 | K | Mom is in the living room when I come downstairs. |
| 490 | Asahina | T1 | K | Asahina is nowhere in sight. |
| 493 | Mom | T2 | P | Mom looks up when I stop near the couch. |
| 570 | Mom | T2 | P | Mom lets that sit. |
| 593 | Asahina | T3 | O | Asahina making efficiency sound like a joke and not quite managing it.<br><sub>rivals: Mom</sub> |
| 616 | Mom | T2 | P | Mom does not let me hover over the homepage too long. |
| 625 | Mom | T2 | P | Mom writes that one down without looking at me. |
| 693 | Matsuda | T1 | K | Matsuda Akai. |

### `game/story/season1/0524.rpy`

28 name-openers — T1 keep 5 · T2 11 · T3 12

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 117 | Asahina | T3 | B | Asahina's sleeve cuff is folded weirdly.<br><sub>rivals: Sam</sub> |
| 118 | Sam | T3 | O | Sam notices before she does, reaches over, fixes it with two fingers, and steps back like nothing happened.<br><sub>rivals: Asahina</sub> |
| 127 | Sam | T3 | O | Sam smiles just enough to make Asahina's ears turn pink instead of making her defensive.<br><sub>rivals: Asahina</sub> |
| 140 | Sam | T3 | O | Sam replicates her actions a fraction later, casual enough that it could be coincidence if I had not started not…<br><sub>rivals: Asahina</sub> |
| 158 | Tsubaki | T3 | B | Tsubaki's hands tighten around the notebook, only a little.<br><sub>rivals: Asahina, Sam</sub> |
| 175 | Tsubaki | T3 | O | Tsubaki lowers her eyes toward the sheet like it might hide her face if she believes hard enough.<br><sub>rivals: Asahina, Sam</sub> |
| 220 | Asahina | T1 | K | Asahina finds me by the stairwell, checking her phone with one thumb. |
| 245 | Asahina | T1 | K | Asahina sits against the wall and opens her lunch bag whilst blatantly side-eying her phone. |
| 263 | Asahina | T2 | C | Asahina pokes at her food. |
| 270 | Asahina | T2 | P | Asahina keeps her eyes on the skyline. |
| 302 | Monika | T1 | K | Monika steps out with a folder against her chest and wind immediately pulling at the loose ribbon of her bow.<br><sub>rivals: Asahina</sub> |
| 324 | Monika | T3 | O | Monika remains standing for a second, fingers tightening around the folder.<br><sub>rivals: Asahina</sub> |
| 345 | Monika | T3 | O | Monika keeps talking before the silence can become too visible.<br><sub>rivals: Asahina</sub> |
| 376 | Monika | T3 | O | Monika stands first and I follow suit.<br><sub>rivals: Asahina</sub> |
| 478 | Monika | T1 | K | Monika stands near the board, writing the prompt in clean letters. |
| 480 | Monika | T2 | P | Monika turns when she hears the door. |
| 492 | Monika | T2 | P | Monika writes steadily, pauses, crosses out exactly three words, and keeps going. |
| 506 | Monika | T2 | P | Monika stands and brings her notebook to my desk once the timer on her phone buzzes. |
| 520 | Monika | T2 | P | Monika sits across from me, reading my six defensive lines with a focused expression. |
| 524 | Monika | T2 | P | Monika looks up. |
| 565 | Monika | T2 | P | Monika reads over my shoulder, close enough that I can feel her attention before I see her reaction. |
| 572 | Monika | T3 | O | Monika turns red so quickly that I almost feel the heat from across the desk.<br><sub>rivals: Hikari</sub> |
| 577 | Monika | T3 | O | Monika presses the back of one hand to her cheek and tries to regain presidential authority from somewhere under…<br><sub>rivals: Hikari</sub> |
| 587 | Monika | T3 | O | Monika gives notes, takes notes, and only glances at me twice.<br><sub>rivals: Hikari</sub> |
| 631 | Mom | T1 | K | Mom and I take the kitchen table with leftovers, tea, and a tiredness that prefers not to host a full family deb… |
| 648 | Mom | T2 | B | Mom's eyebrows lift a fraction. |
| 683 | Mom | T2 | P | Mom smiles, tired but present. |
| 693 | Mom | T2 | P | Mom nods once, accepting the answer without making me expand it under oath. |

### `game/story/season1/0525.rpy`

30 name-openers — T1 keep 7 · T2 7 · T3 16

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 20 | Monika | T1 | K | {i}Monika and emotional stability, allegedly.{/i} |
| 70 | Monika | T1 | K | Monika is already there. |
| 103 | Monika | T2 | B | Monika's pen stops. |
| 112 | Monika | T2 | P | Monika moves the civics pile aside and slides over the language arts handout. |
| 118 | Monika | T2 | B | Monika's laugh is quiet enough for the library. |
| 137 | Monika | T2 | P | Monika looks out the window while I do. |
| 153 | Monika | T2 | P | Monika folds her hands around her pen. |
| 244 | Monika | T2 | B | Monika's eyes stay on mine. |
| 265 | Monika | T1 | K | Monika walks beside me with her folder held against her chest, like she has nowhere else to put the nervous ener… |
| 292 | Kotonoha | T1 | K | Kotonoha.<br><sub>rivals: Monika</sub> |
| 299 | Monika | T1 | K | Monika blinks once.<br><sub>rivals: Kotonoha</sub> |
| 312 | Monika | T3 | O | Monika slides into the seat across from me and looks toward the counter again.<br><sub>rivals: Kotonoha</sub> |
| 320 | Monika | T3 | O | Monika studies the menu card.<br><sub>rivals: Kotonoha</sub> |
| 324 | Kotonoha | T3 | O | Kotonoha returns with water and two menus.<br><sub>rivals: Monika</sub> |
| 330 | Monika | T3 | O | Monika looks at me.<br><sub>rivals: Kotonoha</sub> |
| 335 | Monika | T3 | O | Monika puts one hand over her mouth and loses the fight quietly, somewhere between a laugh and a cough.<br><sub>rivals: Kotonoha</sub> |
| 349 | Monika | T3 | O | Monika lets the laugh escape properly once Kotonoha is out of earshot.<br><sub>rivals: Kotonoha</sub> |
| 364 | Monika | T3 | O | Monika receives hers with both hands.<br><sub>rivals: Kotonoha</sub> |
| 366 | Kotonoha | T3 | B | Kotonoha's gaze lands briefly on the folders tucked beside Monika's bag.<br><sub>rivals: Monika</sub> |
| 381 | Monika | T3 | O | Monika takes one careful bite, then another less careful one.<br><sub>rivals: Kotonoha</sub> |
| 418 | Monika | T3 | B | Monika's expression changes by a careful degree.<br><sub>rivals: Kotonoha</sub> |
| 421 | Monika | T3 | O | Monika does not joke.<br><sub>rivals: Kotonoha</sub> |
| 429 | Monika | T3 | O | Monika glances at me.<br><sub>rivals: Kotonoha</sub> |
| 442 | Monika | T3 | O | Monika smiles, then takes another bite.<br><sub>rivals: Kotonoha</sub> |
| 470 | Monika | T3 | O | Monika does too.<br><sub>rivals: Kotonoha</sub> |
| 494 | Monika | T1 | K | Monika says it without looking away.<br><sub>rivals: Kotonoha</sub> |
| 495 | Kotonoha | T3 | O | Kotonoha nods once.<br><sub>rivals: Monika</sub> |
| 500 | Monika | T3 | O | Monika tucks her copy of the receipt into her wallet.<br><sub>rivals: Kotonoha</sub> |
| 660 | Asahina | T2 | P | Asahina looks down at her packet. |
| 729 | Mom | T1 | K | Mom. |

### `game/story/season1/0526.rpy`

11 name-openers — T1 keep 6 · T2 2 · T3 3

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 91 | Mom | T1 | K | {i}Mom would appreciate that last part more than the exam grader.{/i} |
| 158 | Mom | T1 | K | {i}Mom is going to hear about this.{/i} |
| 343 | Monika | T1 | K | Monika finds me near the stairwell with her folder hugged against her chest. |
| 358 | Monika | T2 | P | Monika and I both pretend we cannot hear them, which is a mercy offered to ourselves. |
| 382 | Monika | T2 | P | Monika sits across from me, not quite smiling, not quite collapsing. |
| 404 | Mom | T1 | K | Mom makes rice, soup, and a pan of vegetables cut smaller than necessary because chopping gives her hands someth… |
| 405 | Asahina | T1 | K | Asahina appears halfway through setting the table, sees me place a glass on the wrong side of the plate, and sil… |
| 413 | Asahina | T3 | O | Asahina sits and nudges the serving spoon toward me with her knuckles.<br><sub>rivals: Mom</sub> |
| 418 | Mom | T3 | O | Mom watches the exchange, decides not to press, and passes the soup.<br><sub>rivals: Asahina</sub> |
| 420 | Asahina | T3 | O | Asahina wins because she grabs it while pretending not to.<br><sub>rivals: Mom</sub> |
| 473 | Mom | T1 | K | {i}Mom. Counselor. Honor status. Monika looking at me like she has to decide whether to ask what happened.{/i}<br><sub>rivals: Monika</sub> |

### `game/story/season1/0527.rpy`

11 name-openers — T1 keep 6 · T2 0 · T3 5

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 16 | Mom | T1 | K | {i}Mom knows. The office knows. Monika still does not know. That does not make it better. That makes it unevenly…<br><sub>rivals: Monika</sub> |
| 131 | Mom | T1 | K | {i}Mom can argue with institutions for a living, but she cannot cross-examine a security log into making me inno… |
| 132 | Monika | T1 | K | {i}Monika would ask what happened with that careful president voice, and I would have to watch the exact second … |
| 273 | Mom | T1 | K | Mom sits at the end of the coffee table with her work notes on one side and my algebra sheet on the other. |
| 287 | Asahina | T1 | K | Asahina passes through once with a glass of water.<br><sub>rivals: Mom</sub> |
| 301 | Mom | T3 | O | Mom does not comment on it.<br><sub>rivals: Asahina</sub> |
| 350 | Coach | T3 | O | Coach waves me down near the water bottles. |
| 377 | Asahina | T1 | K | Asahina's history notes are on the other. |
| 388 | Asahina | T3 | O | Asahina flips one page over and points her pen at the margin.<br><sub>rivals: Mom</sub> |
| 395 | Mom | T3 | O | Mom reaches over and turns my water bottle so the cap faces me.<br><sub>rivals: Asahina</sub> |
| 400 | Asahina | T3 | O | Asahina looks between us.<br><sub>rivals: Mom</sub> |

### `game/story/season1/0528.rpy`

14 name-openers — T1 keep 4 · T2 3 · T3 7

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 15 | Mom | T1 | K | Mom knowing has not made the fear smaller. |
| 278 | Mom | T1 | K | {i}Mom? Monika? The office?{/i}<br><sub>rivals: Monika</sub> |
| 330 | Asahina | T1 | K | Asahina's footsteps upstairs, stopping once near the landing before deciding not to come down.<br><sub>rivals: Mom</sub> |
| 385 | Monika | T2 | P | Monika sits at one of the center desks and sets her folder facedown where neither of us can open it by accident. |
| 404 | Monika | T2 | P | Monika smiles. |
| 419 | Monika | T1 | K | Monika stays behind to straighten the chairs. |
| 431 | Monika | T2 | P | Monika looks at it, then at me. |
| 458 | Asahina | T3 | O | Asahina looks at me with the flat intensity of a person whose last exam has removed several normal filters.<br><sub>rivals: Mom</sub> |
| 471 | Mom | T3 | C | Mom opens the freezer and produces a small carton of ice cream with the care she usually reserves for important …<br><sub>rivals: Asahina</sub> |
| 480 | Asahina | T3 | O | Asahina explains that Sam sent her a sticker of a calculator on fire, which Mom says sounds less encouraging tha…<br><sub>rivals: Mom, Sam</sub> |
| 482 | Asahina | T3 | O | Asahina asks whether that counts as a club activity.<br><sub>rivals: Mom</sub> |
| 483 | Mom | T3 | O | Mom asks whether it worked.<br><sub>rivals: Asahina</sub> |
| 494 | Asahina | T3 | O | Asahina and I swap bowls twice and end up with the same ones we started with.<br><sub>rivals: Mom</sub> |
| 495 | Mom | T3 | O | Mom watches this with the exhausted satisfaction of someone who engineered a small household argument just to pr…<br><sub>rivals: Asahina</sub> |

### `game/story/season1/0529.rpy`

32 name-openers — T1 keep 6 · T2 2 · T3 24

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 23 | Mom | T1 | K | Mom is dressed for work and reading something on her tablet. Asahina is hunched over toast with the specific slu…<br><sub>rivals: Asahina</sub> |
| 34 | Mom | T3 | O | Mom turns a page without looking up.<br><sub>rivals: Asahina</sub> |
| 44 | Asahina | T3 | O | Asahina snorts into her toast, which I count as the day's first genuine win.<br><sub>rivals: Mom</sub> |
| 45 | Mom | T3 | O | Mom stands, gathers her bag, and pauses at the counter to slide a banana into the side pocket of mine without co…<br><sub>rivals: Asahina</sub> |
| 50 | Asahina | T3 | O | Asahina opens her mouth, finds no defense, and closes it.<br><sub>rivals: Mom</sub> |
| 92 | Monika | T1 | K | Monika. |
| 104 | Matsuda | T1 | K | Matsuda Akai. |
| 122 | Matsuda | T2 | P | Matsuda appears wearing the pleased expression of someone whose no-reason has produced immediate results. |
| 153 | Matsuda | T2 | P | Matsuda points the last piece of melon bread at me. |
| 194 | Coach | T1 | K | Coach is by the lane line, clipboard against his hip, watching me arrive with the patience of a man who knows ex… |
| 291 | Asahina | T1 | K | Asahina is at the table with her phone propped against the soy sauce, half-watching something and half-typing. M…<br><sub>rivals: Mom</sub> |
| 302 | Mom | T3 | O | Mom doesn't dignify that, which in this house counts as a confession.<br><sub>rivals: Asahina</sub> |
| 310 | Mom | T3 | B | Mom's spoon doesn't pause, exactly. It just slows by a fraction on its way to the bowl.<br><sub>rivals: Asahina</sub> |
| 313 | Asahina | T3 | B | Asahina's thumb taps her phone once. The screen goes dark, but not before I catch a grid of colored blocks.<br><sub>rivals: Mom</sub> |
| 324 | Asahina | T3 | O | Asahina looks up, betrayed.<br><sub>rivals: Mom</sub> |
| 359 | Mom | T3 | O | Mom turns the box around.<br><sub>rivals: Asahina</sub> |
| 371 | Asahina | T3 | O | Asahina looks at me.<br><sub>rivals: Mom</sub> |
| 375 | Mom | T3 | O | Mom takes the floor across from her and hands me the stack of starting cards without asking whether I am joining.<br><sub>rivals: Asahina</sub> |
| 378 | Mom | T3 | O | Mom does it better.<br><sub>rivals: Asahina</sub> |
| 389 | Asahina | T3 | O | Asahina buys a Militia at the earliest opportunity, because she approaches deck construction the way she approac…<br><sub>rivals: Mom</sub> |
| 390 | Mom | T3 | O | Mom buys one Quarry, then removes two starting cards from her deck.<br><sub>rivals: Asahina</sub> |
| 395 | Asahina | T3 | O | Asahina plays Militia against both of us on her next turn and looks personally restored by the act.<br><sub>rivals: Mom</sub> |
| 405 | Mom | T3 | C | Mom looks at the pile growing beside Asahina.<br><sub>rivals: Asahina</sub> |
| 409 | Asahina | T3 | O | Asahina studies her deck as though betrayal may be visible along the edges.<br><sub>rivals: Mom</sub> |
| 418 | Mom | T3 | B | Mom's hand remains above the market row, one card held between two fingers.<br><sub>rivals: Asahina</sub> |
| 430 | Asahina | T3 | O | Asahina looks at Mom's three neat piles.<br><sub>rivals: Mom</sub> |
| 444 | Mom | T3 | O | Mom returns before either of us can commit the first coordinated offense.<br><sub>rivals: Asahina</sub> |
| 460 | Asahina | T3 | O | Asahina falls backward onto the rug and stares at the ceiling.<br><sub>rivals: Mom</sub> |
| 465 | Asahina | T3 | O | Asahina raises one fist from the floor.<br><sub>rivals: Mom</sub> |
| 467 | Mom | T3 | O | Mom taps her knuckles against it.<br><sub>rivals: Asahina</sub> |
| 470 | Mom | T3 | O | Mom begins sorting the market cards back into their labeled slots. I gather the starting decks. Asahina remains …<br><sub>rivals: Asahina</sub> |
| 493 | Matsuda | T1 | K | Matsuda Akai. |

### `game/story/season1/0530.rpy`

43 name-openers — T1 keep 7 · T2 20 · T3 16

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 76 | Mom | T1 | K | Mom's handwriting leans harder to the right when she writes in a hurry. This one looks like it nearly outran the… |
| 80 | Asahina | T1 | K | Asahina sits across from the empty chair with her phone beside her bowl and a piece of egg held between her chop… |
| 97 | Mom | T3 | B | Mom's chair stays empty while we eat. Her mug is gone, her case folder is gone, and nobody reaches over to turn …<br><sub>rivals: Asahina</sub> |
| 107 | Asahina | T2 | P | Asahina glances at the blank strip on her screen, then at me. |
| 115 | Asahina | T2 | P | Asahina locks her phone and picks up her bowl. |
| 157 | Tsubaki | T1 | K | Tsubaki is already near the shaded wall, her lunch arranged beside a stack of index cards held together with a p… |
| 166 | Tsubaki | T2 | P | Tsubaki has already wiped a bead of condensation from her drink and turned the label outward. Her index cards ar… |
| 177 | Tsubaki | T2 | P | Tsubaki loosens her grip by one finger at a time. |
| 188 | Tsubaki | T2 | P | Tsubaki smiles into her food. |
| 217 | Tsubaki | T2 | P | Tsubaki clips the index cards together, checks the number on the top one, and returns everything to the correct … |
| 254 | Monika | T2 | P | Monika looks toward the corner behind us. |
| 283 | Monika | T2 | P | Monika unfolds it. |
| 301 | Monika | T2 | P | Monika looks down at it, caught. |
| 308 | Monika | T2 | P | Monika nods once. |
| 327 | Hikari | T1 | K | Hikari is arguing with a stapler near the windows. Homura has claimed the back desk and three colors of pen. Som…<br><sub>rivals: Homura</sub> |
| 337 | Monika | T3 | O | Monika caps the marker and turns toward me.<br><sub>rivals: Hikari, Homura</sub> |
| 351 | Monika | T3 | O | Monika makes a slow circuit of the room, answering one question and refusing two attempts to make her define non…<br><sub>rivals: Hikari, Homura</sub> |
| 378 | Hikari | T3 | O | Hikari turns toward Homura before the last word finishes.<br><sub>rivals: Homura, Monika</sub> |
| 379 | Monika | T3 | O | Monika reaches my desk with her notebook already extended.<br><sub>rivals: Hikari, Homura</sub> |
| 387 | Monika | T3 | O | Monika is reading my train piece with one finger resting near the last line.<br><sub>rivals: Hikari, Homura</sub> |
| 409 | Monika | T3 | O | Monika returns my notebook.<br><sub>rivals: Hikari, Homura</sub> |
| 418 | Monika | T3 | O | Monika circulates, gives notes, takes one argument about semicolons under advisement, and returns the marker tra…<br><sub>rivals: Hikari, Homura</sub> |
| 436 | Matsuda | T1 | K | Matsuda pushes off the wall when she sees me.<br><sub>rivals: Tsubaki</sub> |
| 448 | Matsuda | T3 | O | Matsuda puts one gloved hand to her chest.<br><sub>rivals: Tsubaki</sub> |
| 452 | Matsuda | T3 | O | Matsuda ignores both of us and plants her feet like the corridor has become a porch.<br><sub>rivals: Tsubaki</sub> |
| 464 | Tsubaki | T3 | O | Tsubaki watches her, index cards held loosely against her bag.<br><sub>rivals: Matsuda</sub> |
| 470 | Matsuda | T3 | O | Matsuda blinks once.<br><sub>rivals: Tsubaki</sub> |
| 478 | Tsubaki | T3 | C | Tsubaki clips her cards together. The order has apparently survived committee.<br><sub>rivals: Matsuda</sub> |
| 483 | Matsuda | T3 | O | Matsuda closes her eyes.<br><sub>rivals: Tsubaki</sub> |
| 518 | Asahina | T1 | K | Asahina comes in not long after me with her gym bag on one shoulder and her phone already unlocked. |
| 527 | Asahina | T2 | P | Asahina drops her bag beside the chair and opens the refrigerator. |
| 546 | Asahina | T2 | C | Asahina sits. |
| 555 | Asahina | T3 | C | Asahina's phone lights beside her bowl. Sam's name is visible at the top before she turns it over.<br><sub>rivals: Sam</sub> |
| 565 | Asahina | T2 | P | Asahina looks at me across the table. |
| 571 | Mom | T3 | O | Mom texts that the meeting became document review and she will be home late. Asahina sends a thumbs-up. I send a…<br><sub>rivals: Asahina</sub> |
| 590 | Mom | T1 | K | Mom has arranged herself at one end of the couch with the folder on her knee and the plate balanced on top of it. |
| 597 | Mom | T2 | P | Mom lets me, which tells me more about the day than the folders do. |
| 614 | Mom | T2 | B | Mom's mouth twitches around another bite. |
| 628 | Mom | T2 | P | Mom accepts the cucumbers without further appeal. |
| 633 | Mom | T2 | B | Mom's chopsticks pause above the plate. |
| 636 | Mom | T2 | P | Mom nods. The next bite takes a little longer. |
| 651 | Mom | T2 | P | Mom looks at me over the edge of the plate. |
| 663 | Mom | T2 | F | Mom smiles and lets me keep it. |

### `game/story/season1/0531.rpy`

99 name-openers — T1 keep 11 · T2 3 · T3 85

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 18 | Mom | T1 | K | Mom is at the end of the table with her hair still pinned up from yesterday, a mug between both hands, and no fo… |
| 19 | Asahina | T1 | K | Asahina has one knee bouncing beneath her chair while she eats toast and checks the time every few bites. |
| 26 | Asahina | T3 | O | Asahina tears her toast in half and looks at me.<br><sub>rivals: Mom</sub> |
| 42 | Mom | T3 | O | Mom drinks from her mug without smiling. Her eyes do it for her as she sets it down.<br><sub>rivals: Asahina</sub> |
| 58 | Mom | T3 | O | Mom looks at it, then finishes the sip already in progress before she stands. This is apparently what restraint …<br><sub>rivals: Asahina</sub> |
| 71 | Mom | T3 | O | Mom reaches for the jam and slides it across before Asahina asks.<br><sub>rivals: Asahina</sub> |
| 87 | Asahina | T3 | O | Asahina watches my side of the table over the top of her phone.<br><sub>rivals: Mom</sub> |
| 91 | Mom | T3 | O | Mom reaches for a second piece of toast.<br><sub>rivals: Asahina</sub> |
| 96 | Asahina | T3 | O | Asahina gives Mom a look that says she has proved her point. Mom stays out of it.<br><sub>rivals: Mom</sub> |
| 141 | Monika | T1 | K | Monika descends with a canvas bag over one shoulder and yesterday's green pen clipped to the outside pocket. |
| 198 | Coach | T3 | O | Coach waits beside the first row of hurdles with his clipboard tucked beneath one arm. |
| 209 | Coach | T3 | O | Coach gives me four strides at controlled speed. I run the first too hard because the word controlled has always… |
| 221 | Coach | T3 | O | Coach lets me reach the cone. |
| 235 | Coach | T3 | O | Coach checks my first few walking steps. |
| 242 | Coach | T3 | O | Coach points the pen at me before I can spend the maybe. |
| 249 | Coach | T3 | O | Coach finally lowers the clipboard. |
| 273 | Matsuda | T1 | K | Matsuda is crouched beside a low shelf, reading the back of a mystery serial with the severity of a judge review…<br><sub>rivals: Tsubaki</sub> |
| 280 | Matsuda | T3 | O | Matsuda looks up. The book closes around one gloved finger.<br><sub>rivals: Tsubaki</sub> |
| 288 | Tsubaki | T3 | B | Tsubaki's shoulders ease. Matsuda stands and looks down at my shoes before she looks back at me.<br><sub>rivals: Matsuda</sub> |
| 303 | Tsubaki | T3 | O | Tsubaki adjusts the stack on her arm. The top three magazines are old school literary journals, their years hand…<br><sub>rivals: Matsuda</sub> |
| 315 | Matsuda | T3 | O | Matsuda slides the mystery book into her bag and turns toward a rotating rack near the register.<br><sub>rivals: Tsubaki</sub> |
| 319 | Tsubaki | T3 | O | Tsubaki leans closer to the cover.<br><sub>rivals: Matsuda</sub> |
| 322 | Matsuda | T3 | B | Matsuda's fingers stop at the corner.<br><sub>rivals: Tsubaki</sub> |
| 340 | Matsuda | T3 | O | Matsuda keeps her eyes on the rack.<br><sub>rivals: Tsubaki</sub> |
| 342 | Tsubaki | T3 | O | Tsubaki shifts her magazines against her chest, paper settling against paper.<br><sub>rivals: Matsuda</sub> |
| 346 | Matsuda | T3 | O | Matsuda hooks two fingers beneath the heavy bag and lifts it. By the time she turns back, some of the brightness…<br><sub>rivals: Tsubaki</sub> |
| 352 | Tsubaki | T3 | B | Tsubaki's mouth twitches.<br><sub>rivals: Matsuda</sub> |
| 361 | Matsuda | T3 | O | Matsuda smiles.<br><sub>rivals: Tsubaki</sub> |
| 365 | Tsubaki | T3 | O | Tsubaki picks it up first and holds it out.<br><sub>rivals: Matsuda</sub> |
| 386 | Tsubaki | T1 | K | Tsubaki rents a locker near the entrance and places both sets of books inside. She reads the number twice before… |
| 387 | Matsuda | T1 | K | Matsuda waits for almost eight seconds before her restraint gives out. |
| 405 | Matsuda | T3 | O | Matsuda chooses a rear-wheel-drive car with terrible stability and enough acceleration to turn every corner into…<br><sub>rivals: Tsubaki</sub> |
| 413 | Matsuda | T3 | O | Matsuda raises both hands from the wheel.<br><sub>rivals: Tsubaki</sub> |
| 422 | Matsuda | T3 | O | Matsuda looks at me. The victory speech drops out of her face before it reaches the next line.<br><sub>rivals: Tsubaki</sub> |
| 436 | Tsubaki | T3 | O | Tsubaki has taken one of the molded spectator seats. She keeps our bags between her shoes and watches the replay…<br><sub>rivals: Matsuda</sub> |
| 438 | Matsuda | T3 | O | Matsuda and I answer at the same time.<br><sub>rivals: Tsubaki</sub> |
| 453 | Tsubaki | T3 | C | Tsubaki avoids my eyes.<br><sub>rivals: Matsuda</sub> |
| 455 | Matsuda | T3 | O | Matsuda taps the side of her nose.<br><sub>rivals: Tsubaki</sub> |
| 463 | Tsubaki | T3 | O | Tsubaki chooses a cooperative light-gun game next, then apologizes to the plastic weapon when its cable catches …<br><sub>rivals: Matsuda</sub> |
| 464 | Matsuda | T3 | O | Matsuda takes the left side. I take the right. Tsubaki stands between us and quietly rescues every civilian the …<br><sub>rivals: Tsubaki</sub> |
| 465 | Matsuda | T3 | O | Matsuda shoots anything with a health bar. I reload at the wrong times. Tsubaki finishes the first stage with th…<br><sub>rivals: Tsubaki</sub> |
| 471 | Tsubaki | T3 | O | Tsubaki lowers the gun.<br><sub>rivals: Matsuda</sub> |
| 478 | Asahina | T1 | K | Asahina has sent one message to the group.<br><sub>rivals: Matsuda, Tsubaki</sub> |
| 487 | Asahina | T3 | O | Asahina appears three minutes later with damp hair at her temples, her volleyball bag across her chest, and the …<br><sub>rivals: Matsuda, Tsubaki</sub> |
| 494 | Matsuda | T3 | O | Matsuda puts one hand to her chest.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 501 | Tsubaki | T3 | O | Tsubaki lifts her hand.<br><sub>rivals: Asahina, Matsuda</sub> |
| 508 | Asahina | T3 | O | Asahina looks at her, recalibrating.<br><sub>rivals: Matsuda, Tsubaki</sub> |
| 510 | Tsubaki | T3 | B | Tsubaki's fingers move toward the edge of her sleeve.<br><sub>rivals: Asahina, Matsuda</sub> |
| 519 | Tsubaki | T3 | O | Tsubaki covers the stairs. Matsuda covers everything else. I spend the boss fight reviving Asahina while she ins…<br><sub>rivals: Asahina, Matsuda</sub> |
| 520 | Tsubaki | T3 | O | Tsubaki keeps the high score.<br><sub>rivals: Asahina, Matsuda</sub> |
| 524 | Asahina | T3 | O | Asahina looks toward the pulsing machines in the back.<br><sub>rivals: Matsuda, Tsubaki</sub> |
| 530 | Matsuda | T3 | O | Matsuda attacks the first thirty seconds with enough confidence to make accuracy seem optional. Asahina starts m…<br><sub>rivals: Asahina, Tsubaki</sub> |
| 532 | Asahina | T3 | O | Asahina wins by a margin too large for excuses.<br><sub>rivals: Matsuda, Tsubaki</sub> |
| 539 | Asahina | T3 | O | Asahina steps down glowing with exertion and victory.<br><sub>rivals: Matsuda, Tsubaki</sub> |
| 548 | Tsubaki | T3 | O | Tsubaki stops in front of a claw cabinet filled with small cloth birds in colors no bird has requested. One pale…<br><sub>rivals: Asahina, Matsuda</sub> |
| 555 | Matsuda | T3 | O | Matsuda takes her hand off the card.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 562 | Matsuda | T3 | O | Matsuda studies the cabinet long enough to find the side angle.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 566 | Tsubaki | T3 | O | Tsubaki looks at the yellow bird again.<br><sub>rivals: Asahina, Matsuda</sub> |
| 568 | Matsuda | T3 | O | Matsuda taps her card, centers the claw, and moves it back by less than a centimeter. The timer counts down.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 577 | Tsubaki | T3 | O | Tsubaki laughs first, trying to hold it behind one hand until Matsuda leans close to the glass and tells the bir…<br><sub>rivals: Asahina, Matsuda</sub> |
| 578 | Matsuda | T3 | O | Matsuda straightens. Her card is still in her hand.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 580 | Tsubaki | T3 | O | Tsubaki touches two fingers to the glass near the bird's flattened beak.<br><sub>rivals: Asahina, Matsuda</sub> |
| 584 | Matsuda | T3 | O | Matsuda retrieves the bookstore bags. Tsubaki checks the locker twice, then closes it with nothing left inside.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 605 | Tsubaki | T1 | K | Tsubaki lowers the bookstore bundle into the basket with both hands. Matsuda's nine-volume mystery purchase land…<br><sub>rivals: Matsuda</sub> |
| 607 | Asahina | T1 | K | Asahina gets a grilled chicken sandwich and steals fries from my plate before hers arrives. Tsubaki orders soup …<br><sub>rivals: Matsuda, Tsubaki</sub> |
| 612 | Matsuda | T3 | O | Matsuda looks at Tsubaki.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 620 | Matsuda | T3 | O | Matsuda unfolds her napkin and aligns one corner with the table edge.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 624 | Asahina | T3 | O | Asahina leans forward.<br><sub>rivals: Matsuda, Tsubaki</sub> |
| 629 | Matsuda | T3 | O | Matsuda looks down at the napkin.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 642 | Tsubaki | T3 | O | Tsubaki wraps both hands around her water glass.<br><sub>rivals: Asahina, Matsuda</sub> |
| 648 | Matsuda | T3 | O | Matsuda glances at me.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 654 | Asahina | T3 | O | Asahina finishes half her sandwich quickly, then slows. She moves the remaining fries into a line along the plat…<br><sub>rivals: Matsuda, Tsubaki</sub> |
| 655 | Tsubaki | T3 | O | Tsubaki notices the arrangement and nudges the shared pickle dish toward the center without comment. Asahina tak…<br><sub>rivals: Asahina, Matsuda</sub> |
| 657 | Matsuda | T3 | O | Matsuda tells us the mystery serial's landlord is guilty based on basement frequency. Tsubaki counters that the …<br><sub>rivals: Asahina, Tsubaki</sub> |
| 666 | Matsuda | T3 | O | Matsuda points one fry at her.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 671 | Matsuda | T3 | O | Matsuda eats the fry and accepts the loss.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 677 | Tsubaki | T3 | O | Tsubaki locks her phone and returns it to her bag.<br><sub>rivals: Asahina, Matsuda</sub> |
| 694 | Tsubaki | T3 | O | Tsubaki hides a smile behind her glass.<br><sub>rivals: Asahina, Matsuda</sub> |
| 697 | Asahina | T3 | O | Asahina goes to the counter for change. Tsubaki follows to buy a wrapped cookie for the train.<br><sub>rivals: Matsuda, Tsubaki</sub> |
| 710 | Matsuda | T3 | O | Matsuda presses the packets flat with one finger.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 725 | Matsuda | T3 | B | Matsuda's thumb goes still on the sugar packet.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 732 | Matsuda | T3 | B | Matsuda's thumb goes still on the sugar packet.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 740 | Matsuda | T3 | O | Matsuda waits. She doesn't fill it, which is new.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 742 | Matsuda | T3 | B | Matsuda's thumb goes still on the sugar packet.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 760 | Matsuda | T3 | O | Matsuda gives a small nod.<br><sub>rivals: Asahina, Tsubaki</sub> |
| 766 | Asahina | T3 | O | Asahina and Tsubaki return.<br><sub>rivals: Matsuda, Tsubaki</sub> |
| 786 | Asahina | T1 | K | Asahina and I walk home beneath storefront lights and the last blue left in the sky. |
| 811 | Asahina | T2 | C | Asahina catches the swinging strap of my track bag before it bumps a railing. |
| 835 | Mom | T3 | O | Mom takes Asahina's bag from my shoulder and sets it near the stairs.<br><sub>rivals: Asahina</sub> |
| 850 | Mom | T3 | O | Mom looks from one of us to the other, then seems satisfied enough to move on.<br><sub>rivals: Asahina</sub> |
| 858 | Asahina | T3 | O | Asahina drops onto the couch and pulls one leg beneath her.<br><sub>rivals: Mom</sub> |
| 861 | Mom | T3 | C | Mom waits for my answer.<br><sub>rivals: Asahina</sub> |
| 870 | Mom | T3 | O | Mom raises an eyebrow.<br><sub>rivals: Asahina</sub> |
| 879 | Asahina | T3 | O | Asahina looks at me from the couch.<br><sub>rivals: Mom</sub> |
| 890 | Asahina | T3 | O | Asahina points at the kitchen in defeated acknowledgment and heads upstairs.<br><sub>rivals: Mom</sub> |
| 893 | Mom | T3 | O | Mom returns with water in the mug and sits in the chair beside the closed laptop.<br><sub>rivals: Asahina</sub> |
| 902 | Mom | T2 | P | Mom looks at the legal pad. Her pen rests across the top instead of in her hand. |
| 912 | Mom | T2 | P | Mom opens the laptop only after I stand. The legal pad remains untouched. |
| 935 | Monika | T1 | K | Monika's question rests beneath them in green ink. |

### `game/story/season1/exam_guard.rpy`

7 name-openers — T1 keep 3 · T2 2 · T3 2

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 296 | Mom | T1 | K | Mom is already in the living room. |
| 499 | Asahina | T1 | K | Asahina heard enough.<br><sub>rivals: Mom</sub> |
| 509 | Mom | T2 | F | Mom notices. |
| 548 | Mom | T1 | K | Mom is standing in the living room. Her work bag is still by her feet. Her jacket is still on. Her phone is face… |
| 624 | Mom | T2 | P | Mom writing dates down so the future would look less impossible. |
| 683 | Asahina | T3 | C | Asahina stops with one foot still outside the room.<br><sub>rivals: Mom</sub> |
| 708 | Mom | T3 | O | Mom waits until the upstairs floorboard gives its smallest complaint.<br><sub>rivals: Asahina</sub> |

### `game/story/out_of_context/ooc_0604_out_of_ten.rpy`

3 name-openers — T1 keep 0 · T2 2 · T3 1

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 187 | Matsuda | T2 | F | Matsuda takes the can away from her mouth. |
| 245 | Daichi | T3 | O | Daichi takes about a second and a half with that.<br><sub>rivals: Matsuda</sub> |
| 260 | Matsuda | T2 | P | Matsuda opens her mouth. |

### `game/story/out_of_context/ooc_0612_reception.rpy`

1 name-openers — T1 keep 1 · T2 0 · T3 0

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 51 | Asahina | T1 | K | Asahina is at a friend's until tomorrow. Mom is four hours away in a hotel with a conference room attached, doin…<br><sub>rivals: Mom</sub> |

### `game/story/out_of_context/ooc_1026_passed_out.rpy`

5 name-openers — T1 keep 1 · T2 0 · T3 4

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 141 | Asahina | T3 | C | Asahina is laughing so hard she has to put a hand over her eyes.<br><sub>rivals: Mom</sub> |
| 148 | Mom | T3 | B | Mom's eyes are pointed at her without being aimed at her.<br><sub>rivals: Asahina</sub> |
| 166 | Asahina | T3 | O | Asahina catches my eye across the table and tips her head at the stairs, and for once neither of us has to say i…<br><sub>rivals: Mom</sub> |
| 177 | Asahina | T3 | O | Asahina looks at me like I have asked her to do long division.<br><sub>rivals: Mom</sub> |
| 214 | Asahina | T1 | K | Asahina is exactly where I left her, still in her jacket, elbows on the table. |

### `game/story/out_of_context/ooc_1030_uhoh.rpy`

31 name-openers — T1 keep 2 · T2 0 · T3 29

| Line | Who | Tier | Move | Text |
| --- | --- | --- | --- | --- |
| 88 | Matsuda | T1 | K | Matsuda has cleared a landing zone by stacking three trays on top of each other. She performed this as a public …<br><sub>rivals: Asahina, Sam, Tsubaki</sub> |
| 101 | Tsubaki | T3 | O | Tsubaki does not even look up. She has the lid off already and she is unfolding something out of the bottom of t…<br><sub>rivals: Asahina, Matsuda, Sam</sub> |
| 111 | Sam | T3 | O | Sam reaches across me for the box lid and I let him have it, and then he holds it up next to Matsuda's face and …<br><sub>rivals: Asahina, Matsuda, Tsubaki</sub> |
| 117 | Matsuda | T3 | O | Matsuda takes the lid back with the dignity of a woman who has decided not to hear something.<br><sub>rivals: Asahina, Sam, Tsubaki</sub> |
| 120 | Sam | T3 | O | Sam picks his hand up and has it sorted in about four seconds.<br><sub>rivals: Asahina, Matsuda, Tsubaki</sub> |
| 131 | Tsubaki | T3 | O | Tsubaki has gone very still behind the rules sheet in the way she does when a document turns out to be worse tha…<br><sub>rivals: Asahina, Matsuda, Sam</sub> |
| 142 | Matsuda | T3 | O | Matsuda closes her eyes for a moment, the way somebody does when a gift has exceeded the occasion.<br><sub>rivals: Asahina, Sam, Tsubaki</sub> |
| 154 | Sam | T3 | O | Sam wins it.<br><sub>rivals: Asahina, Matsuda, Tsubaki</sub> |
| 173 | Tsubaki | T3 | O | Tsubaki wins the second hand.<br><sub>rivals: Asahina, Matsuda, Sam</sub> |
| 188 | Monika | T1 | K | Monika arrives at the end of it with a tray and the expression of someone who has spent forty minutes in a room …<br><sub>rivals: Asahina, Matsuda, Tsubaki</sub> |
| 195 | Asahina | T3 | O | Asahina takes one of Monika's fries during the transfer, in full view, at arm's length, with no attempt at conce…<br><sub>rivals: Matsuda, Monika, Tsubaki</sub> |
| 205 | Tsubaki | T3 | O | Tsubaki turns the sheet over. Turns it back. Runs a finger down one column and then the other, and then down the…<br><sub>rivals: Asahina, Matsuda, Monika</sub> |
| 209 | Matsuda | T3 | O | Matsuda picks the card up and holds it toward the window like a jeweler.<br><sub>rivals: Asahina, Monika, Tsubaki</sub> |
| 222 | Asahina | T3 | O | Asahina points a fry at him, at length, and does not come up with anything.<br><sub>rivals: Matsuda, Monika, Sam, Tsubaki</sub> |
| 246 | Matsuda | T3 | O | Matsuda gets up on her chair.<br><sub>rivals: Asahina, Monika, Tsubaki</sub> |
| 253 | Matsuda | T3 | O | Matsuda gets down.<br><sub>rivals: Asahina, Monika, Tsubaki</sub> |
| 305 | Tsubaki | T3 | O | Tsubaki looks at the sheet for a long moment.<br><sub>rivals: Asahina, Matsuda, Monika</sub> |
| 316 | Asahina | T3 | O | Asahina takes her three cards one at a time, with a look on her face for each one, and Matsuda watches her do it…<br><sub>rivals: Matsuda, Monika, Tsubaki</sub> |
| 342 | Matsuda | T3 | C | Matsuda has both hands out over the table like a woman presenting a body.<br><sub>rivals: Asahina, Monika, Tsubaki</sub> |
| 344 | Asahina | T3 | O | Asahina does not look up.<br><sub>rivals: Matsuda, Monika, Tsubaki</sub> |
| 347 | Sam | T3 | O | Sam laughs. It's a good line.<br><sub>rivals: Asahina, Matsuda, Monika, Tsubaki</sub> |
| 349 | Tsubaki | T3 | O | Tsubaki has stopped with the rules sheet half-folded in her lap.<br><sub>rivals: Asahina, Matsuda, Monika</sub> |
| 353 | Asahina | T3 | O | Asahina puts the phone face-down on the table.<br><sub>rivals: Matsuda, Monika, Tsubaki</sub> |
| 381 | Matsuda | T3 | B | Matsuda's hands come down.<br><sub>rivals: Asahina, Monika, Tsubaki</sub> |
| 387 | Sam | T3 | O | Sam comes up the table and rights the chair and pushes it back in, and then he does not sit down in it.<br><sub>rivals: Matsuda, Monika, Tsubaki</sub> |
| 413 | Monika | T3 | O | Monika has stacked her hand neatly in front of her and put both palms flat on the table on either side of it.<br><sub>rivals: Matsuda, Sam, Tsubaki</sub> |
| 419 | Tsubaki | T3 | O | Tsubaki folds the rules sheet along its original creases, all six of them, and does not put it away.<br><sub>rivals: Matsuda, Monika, Sam</sub> |
| 437 | Tsubaki | T3 | O | Tsubaki has the rules sheet in both hands.<br><sub>rivals: Asahina, Matsuda, Monika</sub> |
| 438 | Tsubaki | T3 | O | Tsubaki says nothing.<br><sub>rivals: Asahina, Matsuda, Monika</sub> |
| 439 | Matsuda | T3 | O | Matsuda looks at the card for a while.<br><sub>rivals: Asahina, Monika, Tsubaki</sub> |
| 460 | Sam | T3 | O | Sam has both trays, his and Asahina's, stacked the way Matsuda stacks them.<br><sub>rivals: Asahina, Matsuda, Monika, Tsubaki</sub> |