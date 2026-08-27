# Season 1 pacing analysis

Snapshot: August 25, 2026. Line numbers refer to the source as it existed on
that date, after the May 25 outline was replaced with a complete scene.

## Scope and standard

This audit covers every Ren'Py source file directly under
`game/story/season1/`: the seventeen dated chapters from `0515.rpy` through
`0531.rpy`, plus `exam_guard.rpy`, `s1_choices.rpy`, and `s1disc.rpy`. Compiled
`.rpyc` files are not separate story sources and are therefore excluded.

For this report, pacing feels unnatural, quick, or forced when one or more of
the following is true:

- a conversation changes subject without a local trigger;
- a character offers intimacy, information, responsibility, or agreement
  before the relationship has earned it;
- a plot-required entrance, exit, interruption, or choice is more visible than
  the character reason for it;
- an emotional turn resolves before the people involved have time to react,
  resist, misunderstand, or repair;
- a scene repeats its dramatic or informational point after the point has
  already landed.

The test is not whether a scene is dramatic or long. The test is whether the
beats feel like something these people could arrive at in real time.

Revision status matters:

- **Current-revision zone:** `0515.rpy` through the completed `0525.rpy`.
  Findings here assess the presently established voice and intent.
- **Provisional downstream zone:** `0526.rpy` through `0531.rpy`, including the
  exam-guard story branches they call. Findings here identify pacing risks, not
  definitive judgments about final mood, intrigue, or authorial intent.
- **Support files:** `s1_choices.rpy` and `s1disc.rpy` are assessed for any
  player-facing pacing effect, even though most of their contents are utility
  code or notices rather than scene prose.

Severity is used as follows:

- **High:** the scene's dramatic structure or route flow is substantially
  distorted.
- **Moderate-high:** a major relationship or causal step is not yet fully
  earned.
- **Moderate:** a noticeable local or recurring pacing problem.
- **Low / watch:** a plausible or intentional beat whose construction is just
  visible enough to monitor.

Copyediting, factual accuracy, code behavior, and continuity are outside this
report unless they directly affect pacing.

## Priority summary

### Current-revision priorities

| Priority | Location | Severity | Core issue |
|---|---|---:|---|
| 1 | `0523.rpy:338-384` | Moderate-high | The dependency-route offer jumps from a near-stranger's missed assignments to daily personal management without a trial step. |
| 2 | `0521.rpy:245-271`; `0523.rpy:108-210, 262-384, 444-467`; `0524.rpy:160-241` | Moderate-high in aggregate | Tsubaki's trust, private disclosures, and the group's confidence in reading her accumulate faster than the shared history does. |
| 3 | `0522.rpy:168-290` | Moderate | A heated club argument becomes almost completely solved by the first clean reframing. |
| 4 | `0517.rpy:341-383` | Moderate | Matsuda requests contact after a one-sided collision encounter, and every player response must agree. |
| 5 | `0516.rpy:401-414`; `0524.rpy:229-241` | Moderate | Sam delivers two highly useful private observations with little conversational setup. |
| 6 | `0519.rpy:188-219`; `0521.rpy:602-619`; `0523.rpy:182-217`; `0524.rpy:324-382` | Moderate in aggregate | Bells, doors, phones, and arrivals repeatedly cut in at the exact moment subtext becomes explicit. |

### Provisional watchlist

| Priority | Location | Severity | Core issue |
|---|---|---:|---|
| 1 | `exam_guard.rpy:295-533, 561-801`; call sites in `0526.rpy:297-300`, `0527.rpy:263-266`, `0528.rpy:308-311` | High | Conditional home confrontations are exhaustive prosecutorial monologues, then a second offense can immediately add a separate terminal climax. |
| 2 | `0525.rpy:92-103, 140-400`; exam sequences in `0526.rpy:47-127, 190-278`, `0527.rpy:12-106, 159-241`, `0528.rpy:12-108, 161-250` | Moderate | The study day teaches nearly every exact tested concept, after which three days repeat a uniform question/menu/explanation cadence. |
| 3 | `0526.rpy:27-38` | Moderate | A long system explanation interrupts the instant the first exam paper lands. |
| 4 | `0529.rpy:321-359` | Moderate | Dinner pivots from Sam's unsolicited schedule to Asahina's lunch without an audible or visible bridge. |
| 5 | `0529.rpy:375-535` | Low-moderate | Copper Crown continues several rounds after the family dynamic and strategic joke are already established. |

## Findings by file

### Current-revision zone

#### `0515.rpy` — no meaningful pacing issue

**Coverage:** lines 1-412.

The invitation, college discussion, meal, and glue interruption all have local
triggers. The characters are allowed to hesitate, joke around a subject, and
react before the next beat. No entrance, exit, disclosure, or agreement feels
materially rushed or plot-forced.

#### `0516.rpy`

**Moderate — lines 401-414: Sam volunteers Asahina's eating habits.**

**Why it feels forced:** Sam glances toward the living room and says Asahina has
been trying to eat better. When the protagonist asks whether he means
volleyball or school, Sam redirects to food anyway. Nothing at the sink, dinner
table, or preceding exchange prompts a recent boyfriend to disclose that
private detail to her brother. Because the line is also a planted warning sign,
the plot purpose is easier to see than Sam's conversational reason.

**Revision direction:** Keep the unsettling information, but give it a concrete
doorway: leftovers being packed, a rejected snack, Mom asking what Asahina
liked, or Sam checking whether a meal choice is normal for her. A small pause
about whether it is his information to share would make the red flag feel lived
rather than delivered.

**Remaining coverage:** lines 1-400 and 415-442 contain no additional
high-confidence pacing problem. In particular, the algebra lesson, track
sequence, dinner entrance, and Sam's departure are causally clear.

#### `0517.rpy`

**Moderate — lines 341-383, within the encounter at lines 262-435: contact is
mandatory before mutual interest is established.**

**Why it feels forced:** The encounter is intentionally a performance by
Matsuda, and the protagonist accurately describes it as being talked at by a
parade. She then requests his contact information, and all three menu options
hand it over. His later doormat characterization helps explain compliance, but
the scene has not yet supplied a positive hook strong enough to make exchanging
numbers feel like his choice rather than the route's access requirement.

**Revision direction:** Add one moment of genuine mutual interest before the
request, let Tsubaki provide a practical school-related reason to stay in touch,
or make the first exchange a lower-stakes social handle. Matsuda can remain
fast and overbearing; the protagonist just needs one readable reason to say
yes.

**Remaining coverage:** lines 1-261 and 384-525 contain no separate pacing
issue. The encounter's exit itself is gradual and motivated.

#### `0518.rpy` — no meaningful pacing issue

**Coverage:** lines 1-558, including `a0518` and `a0518_showtime_pick`.

The movie outing moves naturally from scheduling to arrival, concessions, the
film, and goodbye. The selected showtime changes local texture without making
the characters teleport between emotional states. The goodbye has enough room
for both awkwardness and closure.

#### `0519.rpy`

**Low by itself; moderate as a repeated pattern — lines 188-219: the bell ends
the first open crack in Monika's council persona.**

**Why it feels constructed:** Monika admits that remembering everything for
other people is lonely and snaps briefly about her peers. The protagonist asks
whether she is all right; she answers "Always"; the halfway bell immediately
prevents a follow-up. A school bell is entirely plausible, but its precision
becomes noticeable because later vulnerable exchanges are also ended by an
external cue.

**Revision direction:** This instance can remain if other chapters vary the
device. Elsewhere, let a character choose not to answer, change the subject,
leave because they are uncomfortable, or sit in the aftermath. If revising this
specific scene, give the protagonist one reaction after "Always" before the
bell.

**Remaining coverage:** lines 1-187 and 220-458 have no additional local
pacing concern. The later home and dinner material is properly motivated.

#### `0520.rpy` — no meaningful pacing issue

**Coverage:** lines 1-403.

The chapter's classroom, club/phone, track, game, and home movements follow one
another causally. Topic changes occur through visible activity rather than
characters supplying the next plot item on demand.

#### `0521.rpy`

**Moderate in the trust arc — lines 245-271: Tsubaki discloses Matsuda's shaking
hands to two people she barely knows.**

**Why it feels quick:** Asahina gives her a natural prompt by asking about the
rumors, so the anecdote itself belongs in the conversation. The private ending
is the issue: Tsubaki reveals that Matsuda's hands shook through a committee
speech, explains what Matsuda dislikes being seen doing, and then asks them not
to repeat it. The group has not yet earned much confidence, especially from
Tsubaki.

**Revision direction:** Tell the public, funny half of the committee story here
and save the shaking-hands observation for a later lunch, or let someone else
offer a comparable vulnerability first. Another option is to make Tsubaki stop
before the physical detail and allow it to surface through action later.

**Low by itself; moderate as a repeated pattern — lines 602-619: the phone call
ends immediately after Tsubaki becomes the subject.**

**Why it feels constructed:** Monika says she cannot read Tsubaki and Matsuda's
chemistry, then yawns and closes a long, otherwise leisurely call. The timing
can imply deliberate avoidance, but there is not quite enough reaction to tell
whether it is subtext or scheduling convenience.

**Revision direction:** If Monika is uncomfortable, add one readable beat—a
pause, a changed register, or a slightly too-fast goodnight. If no intrigue is
intended, place the yawn in a neutral wind-down before Tsubaki is mentioned.

**Remaining coverage:** lines 1-244, 272-601, and 620-635 have no additional
high-confidence pacing issue. Tsubaki's lunch exit at lines 283-304 is
character-motivated and includes a practical reason rather than an unexplained
disappearance.

#### `0522.rpy`

**Moderate — lines 168-290: the club argument resolves too completely on the
first translation.**

**Why it feels quick:** Hikari and Homura begin at shouting temperature. In
every branch, the protagonist's first mediation prompt uncovers the exact
misunderstanding, both girls accept the translation, and Monika's tidy writing
assignment finishes the repair. There is very little embarrassment,
defensiveness, or residue proportional to the opening heat.

**Revision direction:** Let the first reframing only partly work. One speaker
can object to the wording, repeat the original hurt, or need a specific apology
before discussing the poem again. Splitting the work—protagonist slows them
down, Monika later finds the workable exercise—would also make the repair feel
shared rather than instantaneous.

**Remaining coverage:** lines 1-167 and 291-325 contain no additional pacing
problem.

#### `0523.rpy`

**Moderate-high in aggregate — lines 108-138 and 182-210: Tsubaki waits for the
siblings, then offers family-wound language very early.**

**Why it feels quick:** Her embarrassment about waiting is well observed, and
the ordinary running/poster conversation helps. Even so, this is only the
second shared rooftop lunch. "You just say things, and then the other person is
still there" exposes a deep relational wound before the group has built much
reciprocal trust. The line is effective in isolation; its placement is what
makes it feel accelerated.

**Revision direction:** Keep either the deliberate waiting or the deepest
sentence here, not both at full intensity. A mundane lunch between this and the
disclosure, or a smaller first admission such as "you two make silence look
easy," would preserve the trajectory while earning the later line.

**Moderate-high, intentional route risk — lines 262-384, especially the
dependency branch at lines 338-384: a one-time school problem becomes daily
personal management.**

**Why it feels forced:** The protagonist hears that a near-stranger has needed
many extensions and immediately offers to receive every board photo, decide
whether there is a problem, and tell her what to do. Tsubaki escalates the
mechanism and Asahina endorses it. The hidden route intentionally makes
substitution feel generous, but the size of the responsibility jump risks
revealing the route machinery before the care feels ordinary.

**Revision direction:** Begin with a bounded trial: "send me today's board" or
"I'll check this assignment." Let the daily system emerge after the first
success, even if that escalation occurs later in the same route. The
collaborative branch at lines 286-337 is more naturally scaled because it hands
Tsubaki a method rather than immediately becoming a service.

**Moderate as part of the trust arc — lines 444-467: Tsubaki supplies another
private diagnosis of Matsuda.**

**Why it feels quick:** Soon after the shaking-hands anecdote, Tsubaki explains
that Matsuda attaches to patterns and people and then apologizes for her. This
is plausible knowledge from a close friend, but it is another intimate
interpretive shortcut delivered to the new group before much shared history is
shown.

**Revision direction:** Keep the concrete behavior—Matsuda finding the roof—and
let the protagonist and Asahina remain uncertain longer. Tsubaki can name the
pattern after another example has occurred in front of them.

**Intentional awkwardness, not a defect — lines 819-899:** Matsuda plans an
"emerging circle" six days after meeting the protagonist. The text identifies
the overreach, the protagonist sets a boundary, and Matsuda apologizes. This is
supposed to feel too fast and therefore does not need to be normalized. If more
messiness is wanted, carry a trace of awkwardness into the next contact rather
than making the repair itself less clear.

**Remaining coverage:** lines 1-107, 139-181, 211-261, 385-443, and 468-818 have
no additional high-confidence pacing issue.

#### `0524.rpy`

**Moderate — lines 160-241, especially 229-239: Sam diagnoses Tsubaki after a
minute-long introduction.**

**Why it feels forced:** The introduction naturally includes a dropped paper,
a poster compliment, and Tsubaki's nervous response. Once she leaves, Sam calls
her skittish and claims she was constantly looking over her shoulder and not
committing to her grip. The scene has shown only a few small tells, so the
accuracy and specificity sound like information the next scene needs rather
than the limited impression a new acquaintance would reasonably report.

**Revision direction:** Limit Sam to the behavior he visibly saw: "She seemed
nervous" or "She kept an exit open." Let Asahina form the fuller concern from
her two lunches with Tsubaki, or let Sam's first impression be partly wrong.

**Low by itself; moderate as a repeated pattern — lines 302-382, especially
324-382: a sibling thought is interrupted twice.**

**Why it feels constructed:** Asahina begins to connect Tsubaki's reaction to
her own feelings about unsolicited compliments. The protagonist offers only
"Perchance" before a text announces Monika, Monika arrives, and a second phone
buzz gives Asahina an immediate exit. Each event is plausible; stacked at the
most vulnerable point, they make the handoff to the Monika scene visible.

**Revision direction:** Give the siblings one genuine response-and-processing
beat before the first buzz, or let Asahina decide to leave because she reads the
room. Either change preserves the Monika scene while making the transition
belong to a character.

**Remaining coverage:** lines 1-159, 242-301, and 383-835 have no additional
high-confidence pacing issue. Lines 1-96 are setup/data rather than displayed
conversation.

#### `0525.rpy`

**Moderate only as part of the downstream exam structure — lines 92-103 and
140-400: the study sequence covers nearly every later question in the same
conceptual shape.**

**Why it can feel repetitive:** Inside May 25, the timed subject rotations,
props, mistakes, breaks, and banter make the three-hour study session believable.
The issue appears only when it is followed by `0526`-`0528`: judicial review,
federalism, due process, missing agency, unreliable narration, recurring
images, cell transport, meiosis, keystone species, equilibrium, pH,
stoichiometry, rational-function domains, logarithms, vertex form, present
perfect, unreal past conditionals, and the final reading inference all return
as near-direct exam questions.

**Revision direction:** The requested complete coverage can stay in May 25.
Reduce duplication downstream: let the exam invoke the sticky-note image or a
brief memory instead of restating the full explanation, vary the number and
shape of interactive questions, and allow some tested concepts to appear in a
new application rather than the identical classroom definition.

**No local pacing defect in the newly completed material:** the honest check-in
and shared study rule at lines 104-137, café outing and goodbye at lines 401-621,
sibling study scene at lines 622-731, and jog/home wind-down at lines 732-833 all
have clear triggers and adequate reaction space. Monika's admission at lines
517-551 is prepared by the earlier instruction-manual joke, an interval of
ordinary conversation, and an actual silence before the deeper answer. Asahina
refuses help at lines 662-667 and asks on her own at lines 668-686, which makes
the assistance feel earned. The chapter is long, but its scene changes and
emotional cadence prevent length alone from becoming a pacing problem.

**Remaining coverage:** lines 1-91, 138-139, and 834-837 contain no additional
pacing issue.

### Provisional downstream zone

#### `0526.rpy`

**Moderate — lines 27-38: the system tutorial interrupts the first exam's point
of maximum anticipation.**

**Why it feels unnatural:** The paper lands on the desk, the story cuts to
black, and six narrator lines explain persistent save/load rules before the
bell. The rule is important and properly disclosed before enforcement, but its
placement suspends the lived classroom at the exact instant the exam begins.

**Revision direction:** Put a shorter system notice before the paper lands, use
a visually distinct notice that does not pretend to be in-scene time, or state
the core prohibition here and move recovery details to a help screen.

**Moderate, structural — lines 47-127 and 190-278:** both exams use the same
question/menu/explanation rhythm and directly repeat May 25 material.

**Why it feels repetitive:** Each subject presents three questions, three
options, an explanatory inner monologue, and a short closing response. The
language is polished, but the repeated unit makes the school day feel modular
and lowers uncertainty because the preceding chapter supplied the exact answer
chain.

**Revision direction:** Keep assessment choices where player accountability
matters, but vary the cadence. One question can be summarized, one can require
application instead of definition, and correct answers can trigger only a
brief sensory callback rather than a second lesson.

**Conditional high-severity flow — lines 297-300:** these lines call the long
home confrontation and can immediately jump to the separate bad-ending notice.
The pacing issue is detailed under `exam_guard.rpy`.

**Remaining coverage:** no additional local conversational pacing issue was
found in lines 1-26, 39-46, 128-189, or 279-545. The clean-route lunch and home
aftermath provide useful decompression.

#### `0527.rpy`

**Moderate, structural — lines 12-106 and 159-241:** Biology and Chemistry repeat
the same three-question exam template and the May 25 explanations.

**Why it feels repetitive:** The second exam day changes subjects but not the
reader's action rhythm. Several wrong-answer branches also reduce to "I mark
it," "good enough," or "move on," making the mechanics more visible than the
protagonist's fluctuating state.

**Revision direction:** Give the two subjects different dramatic jobs. Biology
could move faster through recognition; Chemistry could spend its interaction
budget on one calculation where process matters. Vary wrong-answer reactions
according to confidence rather than reusing one neutral cadence.

**Conditional high-severity flow — lines 263-266:** a detected offense calls the
long confrontation, and a second cumulative offense immediately jumps to the
bad ending. See `exam_guard.rpy`.

**Remaining coverage:** no additional local pacing problem was found in lines
107-158 or 242-521. Track and family transitions are causally clear, including
the altered aftermath on the dishonesty route.

#### `0528.rpy`

**Moderate, structural — lines 12-108 and 161-250:** Algebra and English repeat
the same exam template and nearly exact May 25 study prompts.

**Why it feels repetitive:** This is the third day of three-option questions
followed by compact explanations. The final English reading passage also
repeats the same want-versus-responsibility inference used in the study session,
so the end of the exam cycle offers recognition more often than discovery.

**Revision direction:** Make the final day formally distinct: fewer but more
consequential interactions, a time-pressure or fatigue beat between questions,
or transformed examples that test transfer rather than recall.

**Conditional high-severity flow — lines 308-311:** a detected offense calls the
long confrontation and may immediately jump to the bad ending. See
`exam_guard.rpy`.

**Remaining coverage:** no additional local pacing issue was found in lines
109-160 or 251-610. The club decompression and home return are earned.

#### `0529.rpy`

**Low / watch — lines 111-186: Matsuda requests the protagonist's exact location
under "no reason" and appears within a minute.**

**Why it can feel forced:** This is a playful reveal, and line 133 immediately
clarifies that she was already nearby. However, it arrives just after she was
asked to slow down, so hiding the reason can briefly resemble another boundary
crossing before the scene demonstrates her restraint.

**Revision direction:** No change is required if that flash of uncertainty is
intentional. If the goal is unambiguously benign repair, have her say she is
already in the same corridor or ask whether she may join him before appearing.

**Moderate — lines 321-359, especially the turn at line 344: two Sam-related
concerns are queued without a bridge.**

**Why it feels forced:** The family discusses the unsolicited study schedule,
the protagonist internally notes how difficult usefulness is to object to, and
then he abruptly asks whether Asahina ate lunch. Both concerns are established,
but the dialogue does not show what makes one lead to the other in that moment.

**Revision direction:** Let a lunchbox, leftovers, an untouched plate, or Sam's
earlier comment about food trigger the question. A single internal bridge can
also make it clear that the protagonist is deliberately checking a second item
on the same pattern rather than changing topics for the script's benefit.

**Low-moderate — lines 375-535: Copper Crown keeps dramatizing after its point
has landed.**

**Why it feels slow:** By roughly lines 421-434, the scene has established
Asahina's aggression, the protagonist's unreliable engine, Mom's deck-thinning
competence, and the family's teasing dynamic. The scene then plays through more
turns, a work call, a coalition, its collapse, an audit, cleanup, and the rematch
agreement. The details are enjoyable, but several reiterate rather than change
the relationship.

**Revision direction:** Preserve the setup, Mom's work call, the failed
coalition, and the Sunday rematch. Compress the intervening turns into one
montage so each retained beat changes the family state rather than merely
confirming it.

**Remaining coverage:** lines 1-110, 187-320, 360-374, and 536-576 have no
additional high-confidence pacing issue.

#### `0530.rpy` — no meaningful local pacing issue

**Coverage:** lines 1-823. Lines 1-56 are setup before `a0530`.

Tsubaki's lunch, the literature club's return to normal activity, Matsuda's
invitation, and the empty-chair/home material each have an observable trigger
and room for response. Although downstream tone remains provisional, no
conversation presently requires an unearned agreement or abrupt emotional
turn.

#### `0531.rpy` — no meaningful local pacing issue

**Coverage:** lines 1-1160.

The chapter is the longest dated file, but length is not itself the issue. The
bookstore, arcade, café, walk, and home sequence all have clear geographic and
social transitions, and each phase changes the group dynamic. The outing earns
its quieter beats and does not depend on abrupt intimacy or unexplained exits.
Any later tightening should protect that varied cadence rather than cut solely
to match earlier chapter length.

### Support and conditional story files

#### `exam_guard.rpy`

**High, provisional — lines 561-801: the first home confrontation exhausts too
many arguments in one sitting.**

**Why it feels unnatural:** Mom's lawyerly precision is established, so a
controlled confrontation is in character. The scene nevertheless spends about
240 lines revisiting panic versus choice, a zero versus a record, scholarship
consequences, intent, shame, trust, punishment, and what remorse looks like.
The protagonist is repeatedly cut off and receives very little room to answer.
An angry parent may dominate, but the sustained sequence sounds like a complete
brief more often than a conversation happening under emotional pressure.

**Revision direction:** Choose two or three decisive movements for the first
offense—for example: admission, refusal of the panic excuse, concrete school
consequence, and punishment. Combine parallel formulations at lines 603-713;
allow one failed answer from the protagonist to alter Mom's next line; reserve
the deepest trust rupture for a repeat offense.

**High, provisional — lines 295-533: the repeat confrontation is even more
emotionally comprehensive.**

**Why it feels unnatural:** The scene climbs through anger, pattern, identity,
trust, tears, fear, maternal protection, love, institutional fallout, and
punishment in one uninterrupted exchange. Individual lines are strong, but the
scene states nearly every possible consequence before either character can
live with one. Mom's self-corrections add texture without sufficiently changing
the monologue-to-response ratio.

**Revision direction:** Give the repeat scene one dominant rupture—"this is now
a pattern" and the loss of trust—and let later fallout carry the other themes.
The protagonist should make at least one substantive attempt to answer, not
only fragments that cue the next prosecution point. A silence or physical task
between accusation and punishment would create real processing time.

**High, structural — lines 803-825, reached through `0526.rpy:297-300`,
`0527.rpy:263-266`, or `0528.rpy:308-311`: two climaxes stack on the terminal
path.**

**Why it feels forced:** After either long confrontation, a second detected
offense can immediately trigger a narrator notice that prosecutes the choice
again and ends the route. The domestic climax and the meta-story climax compete
for the same emotional conclusion. When both offenses happen on one day, the
first confrontation can also be followed immediately by the terminal notice.

**Revision direction:** Pick the terminal path's primary climax. Either shorten
the home confrontation drastically when `exam_guard_should_bad_end()` is true,
or let the home scene deliver the ending and reduce the notice to the minimum
restart instruction. Do not ask both scenes to summarize the moral case.

**Remaining coverage:** lines 1-264 are state tracking and generic guard logic;
lines 265-271 are a concise immediate notice; lines 827-843 are a concise
locked-load notice. They introduce no additional conversational pacing issue.

#### `s1_choices.rpy` — no displayed-scene pacing issue

**Coverage:** lines 1-178.

This is utility code and documentation. Lines 5-24 explicitly define most
menus as expressive stances that converge on the same plot. That is not a
pacing defect by itself, but it raises one presentation rule: when an event is
mandatory, the menu should read as a choice of attitude rather than a choice of
whether the event occurs. The contact menu in `0517.rpy:357-379` is the clearest
place where that distinction currently becomes visible. No other local issue
exists in this support file.

#### `s1disc.rpy` — no meaningful pacing issue

**Coverage:** lines 1-44.

This is a short opening disclaimer/notice rather than an in-world conversation.
It is brief enough not to create a meaningful pacing problem.

## Cross-file synthesis

### Tsubaki's trust curve needs one more ordinary rung

The relevant progression is:

1. First encounter: `0517.rpy:262-426`.
2. Private information about Matsuda: `0521.rpy:245-271`.
3. Deliberately waiting on the roof and naming relational instability:
   `0523.rpy:108-210`.
4. Handing assignment management to the protagonist and explaining Matsuda's
   attachment pattern: `0523.rpy:262-384, 444-467`.
5. The group confidently interpreting her after a minute-long introduction:
   `0524.rpy:160-241`.

No single beat is impossible. The accumulation is fast because almost every
meeting advances private knowledge. One fully mundane shared interaction—or
one meeting where Tsubaki stays guarded and nothing is decoded—would make the
later intimacy feel chosen rather than scheduled.

### Vulnerability is too often protected by an external cutoff

The bell in `0519.rpy:211-219`, Monika's yawn in `0521.rpy:613-619`, Matsuda's
door entrance in `0523.rpy:211-217`, and the phone/arrival/exit chain in
`0524.rpy:329-382` all arrive when a character has just become readable. The
devices are individually credible. Their repetition teaches the reader that a
bell, door, or phone will save the conversation before either person has to
choose what happens next.

The best fix is distribution, not removal. Keep some external interruptions,
but let other scenes end through self-editing, discomfort, a deliberate subject
change, a failed question, or two people simply staying in the silence.

### The exam arc currently rehearses, then reproduces

Earlier classes seed the subjects (`0516.rpy:99-148`, `0517.rpy:58-96`,
`0520.rpy:101-126`, `0521.rpy:11-83`, and `0524.rpy:464-527`). May 25 then
performs a complete and lively review at `0525.rpy:92-103, 140-400`. The three exam days
mostly reproduce those concepts in the same order and explanatory language.

The May 25 scene should not lose the comprehensive coverage it was written to
provide. The more efficient revision target is the provisional exam prose:
compress repeated explanations, transform examples, and vary interaction
shape across days.

## Recommended revision order

1. Decide how much of each conditional `exam_guard.rpy` confrontation the final
   story actually needs, and prevent the terminal notice from repeating the
   same climax.
2. Add a bounded trial step to `0523.rpy:338-384`, then spread one Tsubaki
   disclosure into a later ordinary interaction.
3. Add residue to the club mediation in `0522.rpy:168-290`.
4. Give the protagonist a positive reason to accept Matsuda's contact request
   in `0517.rpy:341-383`.
5. Give Sam's useful observations concrete conversational triggers in
   `0516.rpy:401-414` and `0524.rpy:229-241`.
6. Diversify the external-cutoff pattern across `0519`-`0524`.
7. When provisional exam chapters are revised, preserve May 25's complete
   study coverage and remove repetition from the tests instead.
