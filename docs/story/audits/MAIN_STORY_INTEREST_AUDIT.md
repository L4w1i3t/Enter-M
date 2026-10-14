# ENTER M — Main-Story Interest Audit

**Chapter 0.5 (May 15–31), read as a first-time player**

September 28, 2026. Findings only: no source file was changed for this audit.

## Summary

**Question.** Is the main story interesting to someone playing it for the
first time?

**Answer.** Yes, as a character piece. The cast is distinct and funny, the
family scenes feel lived in, and a disciplined undertow rewards attention:
Asahina's eating, Sam's managing, Matsuda's watching, Monika's avoidance and
Mom's workload. As plot it is not interesting, and it mostly doesn't try to
be. The difficulty is scale. Roughly 72,000 words (5–6 hours) sit between the
cold open and the closing trailer. Every strange event in between gets an
ordinary explanation within its own scene, unless the player cheats during
exams. The chapter therefore works only for players who enjoy these people
minute to minute. Most of the modeled readers will. The plot-first horror
reader won't, and anyone who arrives expecting horror will wait a long time
for it.

**Principal findings**

1. The first narration after the cold open is the weakest prose in the
   chapter. It comes exactly when readers decide whether to trust the
   writing.
2. Early "wait, what?" moments get explained away within their own scenes,
   and the fourth-wall beats mostly land only for readers who know DDLC.
3. May 25–28 is a homework stretch: 23 of the chapter's 27 quiz questions and
   one character choice, placed right after its two strongest days.
4. The exam guard is the most striking idea in the chapter, but only players
   who reload during an exam will see it.
5. The boot OP shows a "Smug Sam" CG before New Game, which works against the
   main story's slow read of Sam (§8).

**Second question (§10).** Does Chapter 0.5 do its job as a setup chapter?
Yes. It establishes the cast, the world and the undertow well, and it ends
with Chapter 1's first week already booked. Its main shortfalls: Monika is
walled off from the rest of the cast, and Matsuda has no footing in the
graduation-speech race.

## 1. Scope and method

- **Read in full, in play order:**
  - the disclaimer ([s1disc.rpy](../../../game/story/season1/s1disc.rpy#L14));
  - all 17 day files;
  - the exam-guard home confrontation and bad ending
    ([exam_guard.rpy](../../../game/story/season1/exam_guard.rpy#L477));
  - the closing trailer
    ([next_time_trailer.rpy](../../../game/addons/Next%20Time%20Trailer/next_time_trailer.rpy#L394)).
- **Considered only where it shapes the story:** the boot OP (§8).
- **Not assessed:** art, audio and presentation; Archive content, character
  stories and minigames; out-of-context scenes.
- **Readers:** thirteen first-time reader profiles, covering different
  reasons for playing and different constraints. Each is judged on whether
  they would finish Chapter 0.5 and where it sags for them.
- **Audience assumption:** ENTER M began as a DDLC mod and is now its own
  game. Monika is still DDLC's Monika, so DDLC-literate readers are one
  audience among several, not the default player.
- **Measurements:** word and menu counts come from a script that reads say
  statements and phone lines. Reading time assumes 200–250 words per minute.
  These are estimates; a timed playthrough at normal speed would be separate
  evidence.

## 2. The chapter by the numbers

| Measure | Value |
|---|---|
| Player-facing words, main path | About 72,400. In-day exam-cheat variants are included, so an honest path is slightly shorter. |
| Estimated reading time | 5–6 hours to the trailer |
| Menus | 45: 27 academic quiz questions, 18 character choices |
| May 25–28 | About 17,000 words; 23 of the 27 quiz questions; 1 character choice (the sleep-in) |
| Pauses a release build cannot click through | 212 `pause` statements, about 7 minutes in total. [script.rpy:22](../../../game/script.rpy#L22) sets `_dismiss_pause = config.developer`. |
| Scene transitions | 377 |
| Recurring scenes | 16 of 17 days have a kitchen or dining-table scene, and 14 show a shared family meal. 14 have a bedroom-at-night scene. |
| Longest day | May 25, about 7,700 words |
| Longest run before a choice | May 31, about 5,900 words |

Per-day figures are in Appendix A.

## 3. The interest curve

| Days | Words | What carries it | Temperature |
|---|---|---|---|
| May 15–16 | 7.6k | Cold open, Monika's poem workshop, Asahina, Sam, Kotonoha | Warm, low voltage |
| May 17–18 | 7.2k | Matsuda and Tsubaki collision, movie date | First real lift, about 45–60 minutes in |
| May 19–22 | 12.6k | Monika's cracks, the bard bit, exams announced, bus-seat poem, lit-class passage, dream, club fight | Steady, with spikes |
| May 23–24 | 10.1k | College talk, Matsuda's boundary text, poems, Monika asks him out | Peak |
| May 25–28 | 17.0k | Library, cafe, three exam days | Low point, the cafe excepted |
| May 29–31 | 18.0k | Matsuda's shy act, Sam's schedule, Copper Crown, erasure prompts, arcade, trailer | Strong finish |

Only two things stay unexplained: the cold open at minute zero
([0515.rpy:26](../../../game/story/season1/0515.rpy#L26)) and the trailer.
The May 22 dream turns out to be autoplay. The exam guard reveals itself
only to players who reload during a paper.

## 4. Thirteen first-time readers

| Reader | Finishes Ch 0.5? | Where it sags for them |
|---|---|---|
| Well-read / literary | Yes, and recommends it | The first narration after the cold open |
| Well-educated / STEM | Yes | The library on May 25, which rehearses the exams |
| Slice-of-life / character-VN reader | Yes, happily | Quiz density in exam week |
| Young adult, 18–25 | Yes | Exam week |
| Parent, 30+ | Yes | Exam week |
| DDLC-literate reader | Probably | Exam week, if nothing has "happened" yet |
| Horror/thriller, plot-first | Unlikely | Drops during May 16–18 |
| Romance reader | Yes | The finale swerving toward Matsuda |
| Teen, 13–17 | Likely, skimming | Exam week |
| ADHD reader | Coin flip | Likely drops on May 25 |
| Eating-disorder history or exam anxiety | Yes, carefully | No specific content warning |
| Non-native English speaker | Likely | Matsuda's dialect bits |
| Streamer | Depends on chat | Library and exams are dead air |

### 4.1 Well-read / literary reader

This reader gets the most from the chapter.

- MC's bracketed asides
  ([0515.rpy:92](../../../game/story/season1/0515.rpy#L92)), which Monika
  calls "part of the poem," are gone from the May 24 draft
  ([0524.rpy:562](../../../game/story/season1/0524.rpy#L562)). It is a
  character arc told in punctuation.
- The May 21 passage on withheld agency ("It can redistribute guilt,"
  [0521.rpy:26](../../../game/story/season1/0521.rpy#L26)) works as a key to
  the book. The dream answers it with "The room was left this way"
  ([0522.rpy:37](../../../game/story/season1/0522.rpy#L37)). The final line
  answers it with "The door is already open"
  ([0531.rpy:1165](../../../game/story/season1/0531.rpy#L1165)).
- Monika's three May 30 prompts are all about erasure
  ([0530.rpy:315](../../../game/story/season1/0530.rpy#L315)).

The risk is the first impression. The narration right after the cold open is
the weakest writing in the chapter
([0515.rpy:39–47](../../../game/story/season1/0515.rpy#L39)): "no other entity
in sight," "any possible noise that could be in my vicinity," "off of my dome
and ears." A few passages also state the theme outright, such as the civics
lecture on "performative virtue"
([0519.rpy:112](../../../game/story/season1/0519.rpy#L112)).

### 4.2 Well-educated / STEM reader

All keyed quiz answers hold up. I checked the math, chemistry and genetics
items by hand: log domains, holes versus asymptotes, 24% recombination, both
limiting-reactant yields, Q versus K, pH and inverse branches.

Wrong answers are narrated as real reasoning traps ("I let the word carry my
pencil to the first answer before the rest of the facts catch up,"
[0526.rpy:127](../../../game/story/season1/0526.rpy#L127)), and this reader
will respect that. The perfectionist in this group is the player most likely
to reload for a perfect paper and meet the exam guard. The counselor exchange
is the moment they will retell: "I loaded an earlier save so I could change
it." / "That is accurate."
([0529.rpy:123](../../../game/story/season1/0529.rpy#L123)).

Two caveats:
- The exams re-ask nearly every library question, so the May 25 study block
  reads as a rehearsal of a rehearsal.
- A player who misclicks an answer and reloads to fix it is treated as a
  cheater. The first catch can be recovered from; the second ends the run.

### 4.3 Slice-of-life / character-VN reader

This reader is the best fit for the chapter as written. For them, routine,
banter, found family and small domestic victories are the point, and the
undertow is a bonus. Kotonoha's running gag, a different job at each
appearance, is aimed squarely at them. The only friction is how dense the
quizzes get in exam week.

### 4.4 Young adult (18–25)

This is the reader GOALS has in mind when it asks that the player "genuinely
miss the warm, casual feeling." The May 23 college talk
([0523.rpy:598](../../../game/story/season1/0523.rpy#L598)) is their scene:
"Not nobody. Just nobody with a completed file on me." and "Walk instead if
you need to." The bus-seat poem
([0520.rpy:268](../../../game/story/season1/0520.rpy#L268)) reads as burnout
written from the inside.

### 4.5 Parent / older reader (30+)

Mom will be this reader's favorite. She is funny ("I'm not nagging, but I
*am* establishing a paper trail,"
[0519.rpy:75](../../../game/story/season1/0519.rpy#L75); the pocket-dial call,
[0525.rpy:938](../../../game/story/season1/0525.rpy#L938)). Her Copper Crown
line is the best double meaning in the chapter: "If it helped on turn one but
keeps wrecking my draw now, why would I keep it?"
([0529.rpy:628](../../../game/story/season1/0529.rpy#L628)).

This reader will notice her running on empty before anyone else:
- crackers for lunch
  ([0530.rpy:721](../../../game/story/season1/0530.rpy#L721));
- taking fruit last
  ([0527.rpy:470](../../../game/story/season1/0527.rpy#L470));
- Asahina setting her place by accident
  ([0530.rpy:614](../../../game/story/season1/0530.rpy#L614)).

### 4.6 DDLC-literate reader

Monika primes this reader from the first frame. The OP's "technically a doki
doki literature club mod" gag confirms she is that Monika. "...What do you
want?" is aimed at them, and they will read every unguarded Monika
expression as a threat. Three beats keep that suspicion going:
- the cafe that matches her poem
  ([0525.rpy:635](../../../game/story/season1/0525.rpy#L635));
- the piano piece
  ([0528.rpy:450](../../../game/story/season1/0528.rpy#L450));
- "Wait until the place becomes real"
  ([0530.rpy:53](../../../game/story/season1/0530.rpy#L53)).

They are also the likeliest to test saves, and so the likeliest to find the
exam guard.

The problem is that each oddity closes:
- The poster shadow is a studio change the next morning
  ([0519.rpy:165](../../../game/story/season1/0519.rpy#L165)).
- The dream is autoplay
  ([0522.rpy:63](../../../game/story/season1/0522.rpy#L63)).
- Monika had seen the cafe's menu photos
  ([0525.rpy:649](../../../game/story/season1/0525.rpy#L649)).

DDLC teaches players to expect an early turn. Here, the next unexplained
event after minute one is the trailer.

### 4.7 Horror/thriller reader (plot-first)

This is the likeliest dropout. The disclaimer promises something "heavier than
it first appears" ([s1disc.rpy:19](../../../game/story/season1/s1disc.rpy#L19)),
but the first week's stakes are a glue bottle, a movie and a college printout.
The first deadline, exams, is announced on May 20
([0520.rpy:144](../../../game/story/season1/0520.rpy#L144)). The dream, about
two hours in, is the first genre beat.

Now that ENTER M stands alone, how big this group is depends on how the game
is presented: positioning it as horror first brings more of them. Those who
reach the trailer get hooked again.

### 4.8 Romance reader

Monika's side of the romance is carefully built:
- the sleeve grab in the tunnel
  ([0518.rpy:383](../../../game/story/season1/0518.rpy#L383));
- "There wasn't a somebody else"
  ([0518.rpy:494](../../../game/story/season1/0518.rpy#L494));
- "I *missed* this"
  ([0524.rpy:400](../../../game/story/season1/0524.rpy#L400)).

By design it is one-sided. The prose guide's September 7 note says MC notices
her interest and doesn't pursue it, without confusion or fear
([Monika](../MAIN_STORY_PROSE_AND_INTENT_GUIDE.md)). This reader will keep
waiting for him to answer her, and the finale confirms he won't. MC's one big
initiative is aimed at Matsuda
([0531.rpy:907](../../../game/story/season1/0531.rpy#L907)), and Monika gets a
short goodbye on the stairs
([0531.rpy:164](../../../game/story/season1/0531.rpy#L164)). This reader will
still enjoy the chapter, but they will feel that swerve.

### 4.9 Teen (13–17)

Asahina carries this reader:
- the "Awwww" that runs off the textbox
  ([0518.rpy:537](../../../game/story/season1/0518.rpy#L537));
- "Skill issue"
  ([0526.rpy:529](../../../game/story/season1/0526.rpy#L529));
- "Due process, bitch"
  ([0525.rpy:913](../../../game/story/season1/0525.rpy#L913)).

Matsuda's cowboy bit lands
([0530.rpy:546](../../../game/story/season1/0530.rpy#L546)), and so does the
arcade. Exam week is literally homework.

A few expressions sound older than the people saying them: "Geez Louise"
([0515.rpy:140](../../../game/story/season1/0515.rpy#L140)), "cornball"
([0516.rpy:219](../../../game/story/season1/0516.rpy#L219)), "whoopty doo"
([0523.rpy:52](../../../game/story/season1/0523.rpy#L52)). Skimmers will miss
the undertow and meet it later as a shock, which still works.

### 4.10 ADHD reader

This reader will recognize MC:
- the autoplay spiral
  ([0522.rpy:76](../../../game/story/season1/0522.rpy#L76));
- "the pile's part of the process"
  ([0515.rpy:102](../../../game/story/season1/0515.rpy#L102));
- a planner he opens only "when memory alone starts to feel like a bad idea"
  ([0516.rpy:564](../../../game/story/season1/0516.rpy#L564)).

The May 23 dependency choice
([0523.rpy:291](../../../game/story/season1/0523.rpy#L291)), whether to build
Tsubaki a system or do the work for her, is a dilemma this reader lives with.

The friction is long stretches with nothing to press:
- May 31 runs about 5,900 words before its only choice.
- The 60-line monster-video call
  ([0521.rpy:519](../../../game/story/season1/0521.rpy#L519)) changes nothing.
- Most scene changes include a two-second black screen that can't be clicked
  through.

May 25, the longest day and mostly studying, is where they are most likely to
drop.

### 4.11 Reader with an eating-disorder history, or exam anxiety

Asahina's food thread has about a dozen touchpoints, from "practice burns it
off" ([0515.rpy:224](../../../game/story/season1/0515.rpy#L224)) to the fries
lined along her plate
([0531.rpy:830](../../../game/story/season1/0531.rpy#L830)). It never uses
numbers, weights or methods. It also gets family dynamics right: "Most is a
passing grade in some subjects." / "Not in mine."
([0529.rpy:556](../../../game/story/season1/0529.rpy#L556)).

That restraint is right. But this reader will recognize the thread by May 16,
and the advisory card is deliberately vague. For an anxious perfectionist who
cheats, Mom's confrontation
([exam_guard.rpy:551](../../../game/story/season1/exam_guard.rpy#L551)) is the
heaviest scene in the game so far.

### 4.12 Non-native English reader

The plot stays easy to follow, but the comedy thins. Matsuda's
characterization depends on switching registers:
- Shakespeare pastiche
  ([0517.rpy:273](../../../game/story/season1/0517.rpy#L273));
- bard ([0519.rpy:228](../../../game/story/season1/0519.rpy#L228));
- anime hero ([0523.rpy:225](../../../game/story/season1/0523.rpy#L225));
- cowboy ([0530.rpy:477](../../../game/story/season1/0530.rpy#L477)).

The literature quizzes lean on terms such as "focalization"
([0521.rpy:12](../../../game/story/season1/0521.rpy#L12)).

### 4.13 Streamer

An honest playthrough gives few clips: the cold open, the collision, the
"Awwww," the dream and the trailer. Twenty-seven quiz questions are dead air
on stream. Chat will probably push for a reload during exams, though, and
getting caught is the best clip the chapter has.

## 5. What earns the interest

**The undertow.** None of these threads is flagged, and all of them are clear
on a second look.
- **Asahina's eating** runs through nearly every day.
- **Sam's care, which doubles as control.** He:
  - knows her diet
    ([0516.rpy:535](../../../game/story/season1/0516.rpy#L535));
  - tells MC he "missed a button" when every button is done
    ([0524.rpy:128](../../../game/story/season1/0524.rpy#L128));
  - repeats her private compliment in front of Tsubaki
    ([0524.rpy:196](../../../game/story/season1/0524.rpy#L196));
  - sends a schedule she didn't ask for
    ([0529.rpy:532](../../../game/story/season1/0529.rpy#L532));
  - asks which arcade they're going to
    ([0530.rpy:651](../../../game/story/season1/0530.rpy#L651));
  - checks whether practice ran late
    ([0531.rpy:624](../../../game/story/season1/0531.rpy#L624)).
- **Matsuda keeping tabs.** She:
  - finds Tsubaki uninvited
    ([0523.rpy:461](../../../game/story/season1/0523.rpy#L461));
  - asks "Are you on campus presently?" before turning up
    ([0529.rpy:248](../../../game/story/season1/0529.rpy#L248));
  - offers MC a "field guide"
    ([0519.rpy:314](../../../game/story/season1/0519.rpy#L314));
  - reads his lean during the race
    ([0531.rpy:510](../../../game/story/season1/0531.rpy#L510));
  - performs on purpose: "I could wait by the gate?"
    ([0529.rpy:321](../../../game/story/season1/0529.rpy#L321)).
- **Monika's avoidance.** Her own folder stays unopened under her elbow all
  morning at the library
  ([0525.rpy:257](../../../game/story/season1/0525.rpy#L257)).

**Payoffs inside the chapter.**
- The good charger
  ([0523.rpy:706](../../../game/story/season1/0523.rpy#L706) →
  [886](../../../game/story/season1/0523.rpy#L886)).
- Mom's spare eraser, which becomes the guilt object in the cheat branch
  ([0526.rpy:27](../../../game/story/season1/0526.rpy#L27) →
  [574](../../../game/story/season1/0526.rpy#L574)).
- The brackets.
- "Et tu" ([0516.rpy:96](../../../game/story/season1/0516.rpy#L96) →
  [0529.rpy:732](../../../game/story/season1/0529.rpy#L732)).
- The cup poem becoming the cafe table.
- The May 15 bottle cap
  ([0515.rpy:198](../../../game/story/season1/0515.rpy#L198)), answered by the
  one Asahina kicks into the gutter while talking about Matsuda
  ([0531.rpy:996](../../../game/story/season1/0531.rpy#L996)).

**Kotonoha.** She has a different job at every appearance and quietly knows
everything ("Six papers in three days is a lot of writing,"
[0527.rpy:427](../../../game/story/season1/0527.rpy#L427)). She is the most
reliable smile in the chapter and a solid foundation for her Chapter 5 role.

**Choices with real consequences.**
- Sleeping in costs Monika a three-hour wait ("Thank you for not saying your
  phone died,"
  [0525.rpy:536](../../../game/story/season1/0525.rpy#L536)).
- The player writes the boundary text to Matsuda
  ([0523.rpy:821](../../../game/story/season1/0523.rpy#L821)).
- The poem-image choice
  ([0524.rpy:578](../../../game/story/season1/0524.rpy#L578)) is the
  chapter's best interactive moment for literary readers.

**The fourth-wall layer, when it surfaces.** The exam guard (the teacher's
"the correction in its place wasn't made in this room,"
[0526.rpy:599](../../../game/story/season1/0526.rpy#L599)) and the trailer
([next_time_trailer.rpy:525](../../../game/addons/Next%20Time%20Trailer/next_time_trailer.rpy#L525))
are the best work in the game so far.

## 6. What costs interest

1. **The first impression.** The narration right after the cold open is the
   weakest writing in the chapter, and May 15's only energy outside the house
   is the movie invitation.
2. **Oddities that explain themselves, and meta that needs DDLC.** The
   [prose guide](../MAIN_STORY_PROSE_AND_INTENT_GUIDE.md) asks for early
   disturbances that create a quiet "wait, what?" At present the text explains
   each one away within its own scene, so the reader never has to. Only the
   dream's "The room was left this way" is left standing.

   The cold-open comment keeps the fourth-wall thread dormant on purpose
   ([0515.rpy:22](../../../game/story/season1/0515.rpy#L22)). The beats that do
   surface depend on knowing DDLC: the cold open, the cafe poem, the piano,
   and the trailer's "You always could"
   ([next_time_trailer.rpy:531](../../../game/addons/Next%20Time%20Trailer/next_time_trailer.rpy#L531)).
   Players who don't know DDLC get no genre signal from these, so the undertow
   and the disclaimer card carry the promise on their own.
3. **The homework stretch.** May 25–28 is about 17,000 words holding 23 of
   the 27 quiz questions and one character choice, placed right after the two
   strongest days. For an honest player the exams carry no drama; all of it
   sits in the cheat branch.
4. **A routine that rarely breaks.** The repetition is deliberate, since later
   chapters will take the routine away. Still, the days that break it are
   clearly livelier than the ones that don't: the dream opening, the library
   and cafe, the arcade.
5. **Borrowed stakes.** The Hikari/Homura argument on May 22
   ([0522.rpy:148](../../../game/story/season1/0522.rpy#L148)) is well
   written. But the two have had about four lines of description beforehand
   ([0520.rpy:233](../../../game/story/season1/0520.rpy#L233)), so the player
   has no side to take.

## 7. Options

These are options for the author, not prescriptions.

- **Line-edit the opening.**
  [0515.rpy:39–47](../../../game/story/season1/0515.rpy#L39) plus the garbled
  sentence at [0515.rpy:386](../../../game/story/season1/0515.rpy#L386) is the
  cheapest, highest-leverage fix in the chapter.
- **Leave one early oddity unexplained.** The poster shadow is already built.
  It currently closes the next morning at
  [0519.rpy:165–167](../../../game/story/season1/0519.rpy#L165).
- **Thin the library.** Keep two quizzes plus the poster book, Monika's folder
  and the joke about the classroom cup being "granted parole." Alternatively,
  give each exam day one character choice. *Done September 28: the session was
  rewritten to about 1,450 words per path with two quizzes. May 25 fell from
  about 7,700 words to 5,600. The rest of this audit describes the chapter as
  it stood before that change.*
- **Leave the exam guard's discoverability as decided.** The academic
  continuity reference records that an explicit pre-exam warning and its
  proctor-rule equivalent were removed on purpose, with a note not to restore
  them ([Academic standing and integrity](../reference/ITSUKI_ACADEMY_ACADEMIC_CONTINUITY.md)).
  The guard stays a discovery for players who reload. Thinning the library
  (above) would raise those odds on its own: less-rehearsed players get more
  answers wrong, and more of them will be tempted to reload.
- **Offer specific content warnings.** An opt-in list of themes behind the
  current card would protect readers with lived experience without spoiling
  anyone else.
- **Decide on the boot OP's Sam beat** (§8).
- **Close the setup gaps** in §10.3: put Matsuda in the speech race, consider
  one early glance between Matsuda and Monika, and pay off or cut the
  untracked details.

## 8. Adjacent finding: the boot OP and Sam

This sits outside the main story, but it is on every first-time player's way
in. The OP plays on every boot before the title screen
([splash.rpy:766](../../../game/splash.rpy#L766)). At
[op.rpy:1632–1668](../../../game/addons/Sick%20Ass%20Anime%20OP/op.rpy#L1632)
it shows the "Smug Sam" CG (`samvillain.png`): Sam at night on a dark couch,
with a city view, decanters and a wine glass, grinning, one hand reaching
toward the viewer. It is graded amber, with red heat pulses laid over it.

The project has already moved away from coding Sam as a villain elsewhere:
- The OP's shadow card dropped a silhouette because it "telegraphed Sam's
  role" ([op.rpy:1155–1157](../../../game/addons/Sick%20Ass%20Anime%20OP/op.rpy#L1155)).
- The bus edit is kept free of "the separate samvillain art or any noir/red
  coding"
  ([op_fx.rpy:1658–1659](../../../game/addons/Sick%20Ass%20Anime%20OP/op_fx.rpy#L1658)).
- Purgatorium stays locked until "the main story has had its slow read of Sam"
  ([0531.rpy:1179–1181](../../../game/story/season1/0531.rpy#L1179)).

With this beat in place, no first-time player gets that slow read. They meet
Sam on May 16 already knowing this image. Dramatic irony isn't necessarily
worse than a slow read, but the main-story seeds (the diet line, the button
joke, the schedule) were written for the slow read. This is worth deciding
deliberately.

## 9. Loose ends

| Location | Issue |
|---|---|
| [0528.rpy:27](../../../game/story/season1/0528.rpy#L27) | "It's in Japanese." brings back a language name that the July setting sweep removed (see the standing author rules in the [roadmap](../../project/roadmap.md)). The Charlie joke works just as well as "It's not in English." |
| [0528.rpy:235](../../../game/story/season1/0528.rpy#L235), 240, 245 | "Osaka" appears in all three English-exam options: the same regression. |
| [0516.rpy:493](../../../game/story/season1/0516.rpy#L493) | Typo: "excepetions." |
| [0517.rpy:278](../../../game/story/season1/0517.rpy#L278) | MC calls Matsuda Tsubaki's "sister" just after noting that Tsubaki's hair matches *his own* ([0517.rpy:274](../../../game/story/season1/0517.rpy#L274)). Matsuda is a redhead, so nothing on screen supports the guess. |
| [0515.rpy:386](../../../game/story/season1/0515.rpy#L386) | Garbled sentence: "moved from candescent to somewhat tranquil, if there wasn't someone outside…" |

## 10. Setup-chapter assessment

**Question.** Does Chapter 0.5 do its job as a setup chapter, establishing
relationships, the setting and the world before Chapter 1?

**Answer.** Yes. It does the setup job better than the entertainment job. By
May 31 a player knows:
- who everyone is;
- how the house, school and town work;
- what MC wants, and what he avoids;
- enough of the undertow for Chapters 1–5 to build on.

It also ends with Chapter 1's first week already booked. The gaps are
specific; §10.3 covers them.

### 10.1 Against the brief

| Goal ([GOALS.txt](../../GOALS.txt)) | Verdict | Evidence |
|---|---|---|
| Core cast introduced | Done by May 17, about 10,000 words in | Sam and Kotonoha on May 16; Matsuda and Tsubaki on May 17. The other 14 days deepen instead of introducing, which is the right order. |
| Relationships established | Done for everything running through MC and the family; partial for the group | See §10.3, item 1. |
| World built and lived in | The chapter's strongest result | The swing chain that has squeaked since they moved in ([0515.rpy:227](../../../game/story/season1/0515.rpy#L227)), Asahina's scuff from moving the couch ([0523.rpy:712](../../../game/story/season1/0523.rpy#L712)), dryer #3 and the bus-stop puddle ([0516.rpy:314](../../../game/story/season1/0516.rpy#L314)), the old bank and green awning, council budget forms, the pep assembly. Its own media too: *Iron Rod*, Copper Crown, the press-turn RPG. No country is named, apart from the 0528 regression (§9). |
| Day-by-day structure cohesive without being boring | Cohesive, yes; "not boring" only in part | The calendar, the between-scene narration and the recurring rooms hold it together. May 25–28 is where it drags (§6, item 3). |

### 10.2 Jobs outside the brief

- **Plants the undertow.** It lays in Asahina's eating, Sam's managing,
  Matsuda's watching and Mom's overwork (§5). For Tsubaki's erasure it builds
  the tools later chapters will need:
  - the lesson on sentences that leave out who acted
    ([0521.rpy:24](../../../game/story/season1/0521.rpy#L24));
  - the "room one minute after everyone leaves" prompt
    ([0530.rpy:320](../../../game/story/season1/0530.rpy#L320));
  - three objects that record she existed: the TSK high score
    ([0531.rpy:580](../../../game/story/season1/0531.rpy#L580)), the yellow
    notebook, and the photo strip
    ([0531.rpy:737](../../../game/story/season1/0531.rpy#L737)).
- **Stages the theme in miniature.** MC's foot goes from tape
  ([0519.rpy:49](../../../game/story/season1/0519.rpy#L49)), to light practice
  ([0521.rpy:311](../../../game/story/season1/0521.rpy#L311)), to strides
  ([0531.rpy:226](../../../game/story/season1/0531.rpy#L226)), to "maybe both
  races" ([0529.rpy:435](../../../game/story/season1/0529.rpy#L435)). That is a
  complete perseverance arc inside 17 days, and Himeko names it with "Walk
  instead if you need to"
  ([0523.rpy:701](../../../game/story/season1/0523.rpy#L701)). Chapter 5's
  "his heart isn't in it" will land because this arc exists.
- **Gives MC a complete arc, pointed the wrong way.** He starts as "a guy who
  won't say what he wants"
  ([0520.rpy:259](../../../game/story/season1/0520.rpy#L259)) and ends by
  extending an invitation himself, to Matsuda
  ([0531.rpy:907](../../../game/story/season1/0531.rpy#L907)). That is setup
  irony of the best kind.
- **Builds the rituals the story will break.** Copper Crown, Mom's sticky
  notes, the swing, a place set at dinner, the club sign-in sheet. The
  roadmap's rule that routines "must have changed meaning when they return"
  needs exactly this stock.
- **Ends on appointments.** The Copper Crown rematch is Sunday, grades come
  Monday, Monika wants "one line, Monday"
  ([0531.rpy:183](../../../game/story/season1/0531.rpy#L183)), the
  invitational is in two weeks, and arcade round two is floated. Chapter 1
  opens with momentum it didn't have to create.
- **Draws the fault lines.** The chapter ends with a four-person group chat:
  MC, Asahina, Matsuda and Tsubaki
  ([0531.rpy:1130](../../../game/story/season1/0531.rpy#L1130)). The two
  outside it are Sam and Monika, the future villain and the future rival.
  Deliberate or not, the group's cracks are drawn before the group forms.

### 10.3 Shortfalls

1. **Monika is walled off.** She never shares a scene with Matsuda, Sam or
   Tsubaki, and gets one short rooftop exchange with Asahina
   ([0524.rpy:349](../../../game/story/season1/0524.rpy#L349)).
   - The Matsuda/Monika rivalry due by July rests only on each knowing of the
     other: Matsuda's "Lady Monika's court"
     ([0517.rpy:312](../../../game/story/season1/0517.rpy#L312)), and Monika's
     story about the marker pens labeled "armaments"
     ([0521.rpy:573](../../../game/story/season1/0521.rpy#L573)).
   - The deferral is deliberate
     ([0530.rpy:63](../../../game/story/season1/0530.rpy#L63)). But it leaves
     Chapter 1 with the heaviest relationship work in Act 1: bringing both
     Monika and Sam into the group.
   - Sam is similar. He only ever appears in Asahina's orbit, which suits a man
     whose nature is withheld, but the group has no reason of its own to want
     him yet.
   - If the rivalry should feel inevitable rather than scheduled, one glance
     between Matsuda and Monika in May is the cheapest place to set it up.
2. **Matsuda isn't in the graduation-speech race.** GOALS makes MC, Monika or
   Matsuda the speaker depending on exams, and the author named all three as
   valedictorian contenders on September 7
   ([academic continuity reference](../reference/ITSUKI_ACADEMY_ACADEMIC_CONTINUITY.md)).
   The chapter frames the valedictorian race as MC vs Monika
   ([0525.rpy:1005](../../../game/story/season1/0525.rpy#L1005)) and gives
   Matsuda no academic presence at all. The chapter that introduces the exam
   system is the natural place to put her in the race.
3. **Details nobody downstream tracks.** None of these appear in the roadmap,
   GOALS, the prose guide or the TODO, so each should be either paid off later
   or cut now:
   - "the man who doesn't live here. Fourth year running."
     ([0515.rpy:269](../../../game/story/season1/0515.rpy#L269))
   - MC's "prescribed medication"
     ([0515.rpy:471](../../../game/story/season1/0515.rpy#L471))
   - Charlie's dry cough, which the text dwells on
     ([0528.rpy:12](../../../game/story/season1/0528.rpy#L12),
     [0528.rpy:25](../../../game/story/season1/0528.rpy#L25),
     [0529.rpy:393](../../../game/story/season1/0529.rpy#L393)); "Dry, like
     he's been doing it all week" reads as planted
   - the Portrait of Zahrath
     ([0523.rpy:816](../../../game/story/season1/0523.rpy#L816))
   - the unresolved Hikari/Homura friction
     ([0530.rpy:407](../../../game/story/season1/0530.rpy#L407))
4. **A reading rhythm the later chapters can't keep.** At about 4,300 words a
   day for 17 straight days, the chapter teaches that every day is shown.
   Chapters 1–5 cover 44–77 days each. The switch to skipped days (decision 1
   in the [roadmap](../../project/roadmap.md)) needs a signal, or it will read
   as the story losing interest. Handled on purpose, it could become a
   feature: time speeding up as things fall apart.
5. **Kotonoha is a gag and an observer, with no inner life yet.** That's the
   right amount for May. But her Chapter 5 role depends on Chapters 1–4
   turning her into a person before she becomes the one hand still reaching
   out.

### 10.4 Length and identity

"0.5" is the right label. The chapter works like the shared opening of a
visual novel, or a TV pilot arc, and the chapter-select line frames it
honestly: "Seventeen days in May, and most of a school year still ahead"
([chapter_select.rpy:16](../../../game/chapter_select.rpy#L16)).

- **For making the player live there, the length is right.** The later losses
  need hours of warmth behind them, and a 20,000-word prologue couldn't earn
  that.
- **For telling the player what they need to know, it's longer than it has to
  be.** Introductions are done by May 17, and relationships are mostly in
  place by May 24. The last week earns its place mainly by building the exam
  system the ending depends on and by bringing Matsuda's arc to the
  invitation.
- **If you trim,** the redundant library quizzes and the 60-line May 21 phone
  call do the least setup per word. The family meals and the arcade do the
  most, even where they feel slow.

### 10.5 Conclusion

Chapter 0.5 sets the characters up for tragedy better than it sets the player
up to expect one. For a setup chapter that's the right priority, because the
trailer does the expectation-setting at the handoff. (The cost to keeping
players engaged is covered in §6.) The fixes that matter most for later acts
are the first two shortfalls: Monika being walled off, and Matsuda missing
from the speech race.

## Appendix A. Per-day measurements

| Day | Words | Menus | Words before first menu |
|---|---|---|---|
| May 15 | 3,690 | 2 | 1,146 |
| May 16 | 3,903 | 2 | 682 |
| May 17 | 3,239 | 2 | 756 |
| May 18 | 3,925 | 2 | 347 |
| May 19 | 3,294 | 2 | 943 |
| May 20 | 3,561 | 1 | 1,340 |
| May 21 | 3,629 | 1 | 383 |
| May 22 | 2,073 | 1 | 1,129 |
| May 23 | 5,562 | 3 | 1,657 |
| May 24 | 4,540 | 2 | 2,279 |
| May 25 | 7,736 | 6 | 71 |
| May 26 | 3,199 | 6 | 624 |
| May 27 | 2,802 | 6 | 335 |
| May 28 | 3,297 | 6 | 426 |
| May 29 | 4,963 | 1 | 1,732 |
| May 30 | 5,681 | 1 | 3,101 |
| May 31 | 7,335 | 1 | 5,909 |
| **Total** | **72,429** | **45** | |

Notes:
- Words cover say statements and phone lines on the main path.
- Branches stored under their own labels are excluded: the exam-cheat scenes
  and the May 25 sleep-in, about 1,400 words across May 25–28.
- Menu counts include the academic quiz questions.

Related: [Act 1 plans](../../project/roadmap.md) ·
[author checkpoints](../../GOALS.txt) ·
[prose and intent guide](../MAIN_STORY_PROSE_AND_INTENT_GUIDE.md)
