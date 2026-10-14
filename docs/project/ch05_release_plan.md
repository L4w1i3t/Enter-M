# Chapter 0.5 release plan

> Bad night? Read [this](../READ-WHEN-IT-FEELS-HOPELESS.md) first.

> **Waking up Monday, October 12? Start at [§0](#0-wake-up-list-october-12).**
> Every open item with a place in the code now has a `# NUDGE` comment sitting
> right above that line.

Written October 9, 2026, for the Chapter 0.5 build going out on **Wednesday,
October 14** (Matsuda's birthday).

**Scope:** the main story, meaning everything a new player walks through from
boot to the end card. That covers the OP and title, Chapter Select, the
disclaimer, May 15 through May 31, the exam guard, and the closing trailer.
Side content counts only where it could break or embarrass the build.

**Based on:**
- all 17 day files, read in full as they stand today rather than the
  September 28 audit's copy;
- `options.rpy`, `script.rpy`, the boot path in `splash.rpy` and the exam-guard
  reset logic;
- a lint run today, which came back clean;
- per-day word and transition counts, and the audio inventory.

**Not yet based on:** a playthrough at normal speed, a built distribution, or
watching someone play. Those are separate evidence, and they're on the
checklist.

**How to read this:**
- **P0:** don't ship without it.
- **P1:** the structural drama pass, which answers your friends' feedback.
- **P2:** line notes in play order.
- **P3:** presentation and audio.
- **P4:** testing.
- **P5:** the release itself.

Items within each section are in priority order. Nothing is sized to five
days; this is the whole backlog, and the gameplan in §2 picks the order.

---

## 0. Wake-up list (October 12)

This section was added overnight on October 11-12 while you slept. None of the
story was rewritten. The only changes are comments in the code and this
section.

**How the nudges work.** Each open item that sits at a specific spot in the
code now has a one-line comment right above that spot, like this:

    # NUDGE P0.3: names the country. Try: mc "It's not in English." (the Charlie joke still works)

In VS Code, press Ctrl+Shift+F and search for a tag, such as `NUDGE P0`. The
results come back grouped by file, and the day files sort in play order. When
you finish an item, delete its nudge; whatever's left after the release is
your backlog. `.rpy` files never ship (`options.rpy` excludes them), so a
leftover nudge can't reach a player.

The line links further down date from October 9 and drift as you edit. The
nudges move with the text, so trust the tag over the line number.

**Checked tonight (October 12, 00:30 to 01:00):**
- Lint is clean (9,283 dialogue blocks and 97 menus) both before and after the
  nudges went in. There are no orphan `.rpyc` files.
- P0.4's two greps are clean. None of the 215 questions the check recognizes
  ends in a period, and there are no British spellings.
- A mechanical typo sweep found one real error in all of season 1: a missing
  period at 0523 ("straightaway Meanwhile"). The sweep covered doubled words,
  missing periods, stray spaces and common misspellings.
- I read the edits you made between midnight and 00:19. One line doesn't parse
  (0515, "noted to find"), and one word reads as setting ("Mate," in 0516).
  Both are nudged.
- The exam guard's one-ledger-per-run fix from October 11 is in the code. That
  already handles P4's cross-save bleed and decision 11.
- Every file touched tonight was snapshotted first, to
  `ENTER-M-backups/20261012-release-nudges-before`.

**October 13 evening pass (prose polish + nudges, 0521:456 through 0531):**
- **Done:** every cut / trim / merge / relocate nudge in 0521-0531 (52 nudge
  comments in 0522-0531 down to 17; the rest are `KEEP`, `DECIDE`, `P0.3`,
  `P0.5`, the sleep-in `P1.2`, and your pocket-dial call). Also the P1.1
  invitational plant (0521), P1.10 (Monika passes Matsuda, 0530), and a line
  polish of every displayed line from 0521:456 through 0531 plus exam_guard.
- **Relocations:** Matsuda's apology now lands on the night of May 24, merged
  into the RPG night (kept because May 29 and 30 call back to it); May 23 ends
  on "Understood." / "I overstepped."
- **May 25 library:** a scored rivalry with a dessert wager (rule four); the
  two quiz answers set the score and the cafe check pays it off. New keys
  `library_chem` / `library_alg` are registered in `s1_choices.rpy`.
- **Choices now pay off within a day or two:** `matsuda_stop` (0523),
  `sam_lunch`, `movie_goodbye`, `himeko_first`, the hidden-route branch and
  `matsuda_callout` (0524), `poem_revision` (0524 bus home), `asahina_plate`,
  `club_mediation`, `s1_slept_in` (0526), `arcade_invite` (0530),
  `matsuda_bit`, `arcade_offer` (0531).
- **Late additions:** English is now "foreign language" everywhere it shows
  (0516, 0525, 0527, 0528, and the exam guard's subject names); a sprite-face
  pass over 0522-0531 and exam_guard; the 0531 bookend (callbacks to 0515's
  "on purpose" line and its pen); 0528's three "large city" options now match.
- **Checks:** a single integration reviewer traced 13 cross-day threads;
  lint clean (8,697 dialogue blocks, 96 menus); no orphan `.rpyc`. Snapshot
  of the pre-pass files: `ENTER-M-backups/20261013-prose-polish-before`.

### Order of work

| # | Search | What it covers | Rough time |
|---|---|---|---|
| 0 | none | **Commit** (P0.1). The last commit is from August 31, so six weeks of work aren't in git yet. | 5 min |
| 1 | `NUDGE P0` | Setting words (Japanese, Osaka, North American, European, ocean, "Mate"), the 0523 typo, the 0515 grammar slip and the ending check. Each nudge gives a paste-ready wording. | 30 min |
| 2 | `DECIDE` | Six quick decisions: text speed, the Smug Sam CG, Charlie's cough, Zahrath, "prescribed medication" and the man who doesn't live here. Side content (§10.4) has no nudge, but decide it now too. | 15 min |
| 3 | `NUDGE P5` | `options.rpy`: excluding `sfx/kangaroo_court/` is free, because nothing uses it; uncomment one line. `sfx/touhou/` is your call. | 2 min |
| 4 | `NUDGE P1.2`, `P1.7`, `P1.8` | Residue (the May 19 dinner and the boundary text), then the cuts that are pure deletion: matrices, the monster call, the lectures and the exam hallways. | 2 to 3 h |
| 5 | `NUDGE P1.5`, `P1.1`, `P1.10` | Day endings (mostly deleting the last line or two), the spine plants, and Monika's one look at Matsuda. | 1 h |
| 6 | `NUDGE P2`, starting in 0516 to 0518, then `P1.4` | First-hour trims, then bookends and split scenes. | whatever's left |
| | **Tuesday noon** | **Freeze.** Ask Claude to re-run lint and the P0.4 greps on the final files, then build. | |

`NUDGE KEEP` marks the 10 lines to protect while you trim. Those aren't tasks.

**Exam-week rule.** When you cut anything in 0526 to 0528, or in the caught
branches of 0529 to 0531, keep every `$ exam_guard_...` line, every `label` and
every quiz menu. The prose around them is safe to cut. Lint won't notice a
missing checkpoint.

**Safe to skip for October 14.** These are post-release backlog, not
failures:
- The P1.2 sleep-in cost. It collides with the "NOT PUNISHED" contract in
  `s1_sleep_in.rpy`; the nudge explains.
- P1.4's "open three days mid-action". On May 29 it means reordering the
  caught branch's counselor morning.
- P1.9's third-joke pass. It's a reread of the whole chapter.
- The P3 ambience system. It's a new feature, not an edit.
- The exam-week B-plot in P2. It's new writing.

If a friend can play Days 1-3 tonight, that's still the best test you can run
before the freeze.

---

## 1. The verdict

Your friends are right, and the cause is more fixable than "the writing is
boring." Line for line, most of the prose is good. The cast is distinct, the
house feels lived in, and the undertow is well laid: Asahina's plate, Sam's
managing, Matsuda's tracking, Monika's mask, Mom's hours. The chapter fails
as drama for structural reasons, not sentence-level ones. Here they are, worst
first.

**1. Nothing is left open, so the reader is never waiting for anything.**
Slice of life asks what it's like to live here; drama asks what happens next.
Every thread in Chapter 0.5 shows up, gets its beat, and closes inside the
same scene. "Nothing happens" almost always means "nothing is pending."

Asahina's eating is the clearest case. It gets eight or more touchpoints, from
the portion at 0515:397 to the fries at 0531:830, all at the same low volume.
The same beat repeated reads as texture. A thread has to escalate.

**2. Conflict is resolved in the scene that raises it.** The chapter has real
friction and defuses it within lines:
- MC snaps at Asahina at dinner (0519:375) and apologizes five lines later
  (0519:380).
- The boundary text to Matsuda (0523:821) is the best dramatic beat in the
  chapter, and the player writes it. Her full apology and reconciliation land
  before the player puts the phone down (0523:868-883).
- Hikari and Homura's fight is mediated and settled before the scene ends
  (0522:258-262).
- Monika's "Always." (0519:193) gets one follow-up, and then the scene moves
  on.

Drama lives in residue, the thing that's still wrong the next morning. Right
now nothing ever is.

**3. The day template is the monotony.** All 17 days share one shape: home
morning, class, lunch, club or track or an errand, home dinner, bedroom at
night, an interstitial, the calendar dial.
- 16 of 17 days have a family meal, and 14 have a bedroom-at-night scene (Sep
  28 audit counts).
- Each day has 7 to 14 scene changes. Each one is a wipe to black, an
  interstitial, a 2-second pause, and a wipe back in.

By Day 3 a player can predict the next room and its mood, and that
predictability is the drone. The days that break the shape are the ones people
remember: the dream, the library and cafe, the arcade.

**4. MC never wants anything on screen, so every scene comes to him.**
- Monika finds him on May 15, 19, 22, 24 and 31.
- Matsuda finds him on May 17, 19, 23, 29 and 30.
- Asahina recruits him, and Sam seeks him out on May 20.

His one initiative is the arcade invitation at 0531:907. It's built as the
capstone and it works. But 70,000 words of a protagonist who never pushes
against anything is the main source of "nothing happens."

He does have wants: running again, both races at the invitational, dodging
the college talk, beating Monika for valedictorian, keeping his brackets.
They're mentioned, not dramatized. The valedictorian race is the one thing
that would give an honest player a stake in exam week, and its first mention
is a text the night before the exams (0525:799).

**5. The strange beats explain themselves.** Your prose guide asks for early
disturbances that create a quiet "wait, what?" Three of them close in-scene:
- the poster shadow, explained the next morning (0519:165-167);
- the dream, explained as autoplay (0522:63);
- the cafe that matches Monika's poem (0525:446).

Each explanation is a line or two. Deleting them is the cheapest intrigue in
the game.

**6. The narration reports logistics.** Shoes go by the door, seats get taken,
bags get shouldered, doors get held, plates get rinsed, buses get boarded. Your
own guide calls this "routine transition inventories that do not alter
understanding." It gets worse in the unrevised back half. Interstitial
narration runs 171 to 279 words a day on May 17-24. On May 25 and May 29-31
it runs roughly 320 to 350 a day on the honest path. Every box costs a click.

**7. Everyone is funny at the same rate.** Coach, Kotonoha, the teachers, Mom,
Sam, Asahina, Monika and MC all run the same loop: setup, quip, counter-quip,
narration beat. When every exchange lands a joke, no exchange can land a blow.
The voice-fingerprint pass changed how each character builds a sentence. It
didn't change how often everyone is funny.

**8. Class is a lecture, starting on Day 2.** The lectures run through math
(May 16), civics (May 17 and 19), biology (May 20), language arts (May 21) and
matrices (May 24). Each time, a teacher lectures and then quizzes the player,
so the homework feeling starts on Day 2 rather than in exam week. The matrix
lesson (0524:445-506) doesn't prime any exam question; the algebra exam asks
about discontinuities, logs and inverses. It also sits on the chapter's
romantic peak day.

**9. Seven minutes of forced dead air.** Season 1 has 215 `pause` statements,
430 seconds in all. **In a release build none of them can be clicked
through**, because `_dismiss_pause = config.developer` is set at script.rpy:22
and splash.rpy:780. You've never felt it because you play in developer mode.

Players sit through a mandatory black hold roughly every 30 boxes, on top of
transitions that already run 1.5 to 1.8 seconds each. The August 21 pause
convention was justified with "pause is click-dismissable so it is a floor,
not a wall." In release it's a wall. This is the biggest mechanical reason the
chapter drags.

**10. The hook arrives late.** The cold open is a real hook. Then come:
- 5 seconds of black (0515:32);
- the weakest narration in the chapter (0515:39-47), which survived your
  Day 1 revision;
- two days of domestic scenes.

Matsuda, the story's central arc by your own guide, collides with MC at
0517:251. That's about 9,500 words in, or 40 to 50 minutes of reading before
pauses and transitions. A player who bores easily is gone before she arrives.

**None of the fixes below adds spectacle or new plot events.** They rearrange
what's already there so the reader is always holding at least one open
question. That's how you get constant intrigue without overstimulating
anyone, and it keeps the world worth living in.

**Protect these when you cut; they're the best things in the chapter:**
- the cold open;
- the rinsed plate and the paper towel (0515:523);
- Sam at the sink (0516:534-549);
- the bus-seat poem (0520:268-272);
- Tsubaki praising the poster (0521:192-207);
- the college talk (0523:651-701) and the boundary text;
- the May 24 poems and the cafe;
- "Most is a passing grade in some subjects." / "Not in mine." (0529:556-558);
- Copper Crown;
- Asahina setting Mom's place (0530:614-618);
- the photo booth's first frame;
- "The door is already open."

---

## 2. Gameplan

Order of work:
1. Anything that would embarrass the build.
2. The structural moves in P1. They give the biggest return per hour, and
   they're mostly deletions.
3. Line edits in play order. The first hour gets the most care, because that's
   where impatient players decide.
4. Audio.

**Content freeze is Tuesday at noon**, so the full playthrough tests the files
you actually ship.

| Day | Work | Done when |
|---|---|---|
| **Fri 10/9** (tonight) | P0.1 commit. P0.2 pause decision. P0.3 and P0.4 text fixes. P0.6 the opening. | Lint is clean and the first narration reads like the rest of Day 1. |
| **Sat 10/10** | P1.1 plants. P1.6 Matsuda glimpse. P1.2 the May 19 residue. P2 for May 15-19. | Day 1 ends with at least three open questions, and Matsuda shows up sooner. |
| **Sun 10/11** | P1.2 boundary-text residue. P1.3 poster. P1.7 cut matrices. P1.8 monster call. P1.4 merges. P2 for May 20-24. P1.5 day endings for May 15-24. | Every day through May 24 ends on a turn, not on sleep. |
| **Mon 10/12** | P2 for May 25-31: exam-week stakes, hallway cuts, interstitial trims, cafe fixes. P3 audio if you've sourced it (the channel, a bell, three or four room tones). Tonight, a friend plays Days 1-3 of the new build. | Lint is clean, and exam week gives an honest player a reason to care. |
| **Tue 10/13** | **Freeze at noon.** Build the zip. Full normal-speed playthrough of the build (5-6 hours). Branch tests (P4). Fix only crashes, typos and softlocks. Write the release page (P5). | One clean end-to-end run on the shipped files. |
| **Wed 10/14** | Rebuild if anything changed, smoke-test from a fresh folder, and publish. | Live on her birthday. |

> *October 12:* for Monday and Tuesday, follow
> [§0](#0-wake-up-list-october-12) instead of the rows above.

**If you only get partway,** do all of P0. Then do P1.2 (residue), P1.3
(unexplained oddities), P1.1 (the spine) and the May 15-17 cuts. That work is
mostly deleting lines and planting a few new ones, and it changes how the
whole chapter reads.

---

## 3. P0: release blockers

### P0.1 Safety
- [ ] Commit the working tree before the pass, since the current diff touches
  every season-1 file. Don't `git checkout` anything (autocrlf).
- [ ] Take the usual snapshot to `ENTER-M-backups`.
  - *October 12:* both are still open. The last commit is `3d9de9a` from
    August 31. Two traps:
    - 953 files are untracked, including `chapter_select.rpy`,
      `menu_doorway.rpy` and `s1_sleep_in.rpy`, so commit with
      `git add -A`.
    - The `characters/` line in `.gitignore` excludes every sprite under
      `game/assets/characters/`, so git can't restore your art. The full
      snapshot to `ENTER-M-backups` (outside SYNC-FOLDER) is the real safety
      net.
    - Tonight's snapshot, `20261012-release-nudges-before`, covers only the 20
      files the nudges touched.

### P0.2 Make pauses clickable, or decide not to
- [X] **Recommended:** set `_dismiss_pause = True` at
  [script.rpy:22](../../game/script.rpy#L22) and
  [splash.rpy:780](../../game/splash.rpy#L780).
  - *Done October 11 at script.rpy:22 and in splash.rpy's `after_load`;
    verified October 12. `dev.rpy` still ties the define to
    `config.developer` for the cold open and the menus.*
  - If the cold open's 5-second hold
    ([0515:32](../../game/story/season1/0515.rpy#L32)) is meant to be
    unskippable, make that one `$ renpy.pause(3.0, hard=True)`. That also
    shortens it, which P0.6 recommends.
- [X] ~~If pauses stay unclickable, cut the scene-change `pause 2.0` to about
  0.6 at least.~~ Not needed now that pauses are clickable. Day openings currently stack 2 seconds, the calendar dial,
  then 2 more seconds.
- [ ] After the change, check that the trailer, the disclaimer cards, the
  calendar dial, and the Archive's OP replay still play correctly when someone
  clicks through them (P4).

### P0.3 Setting-rule regressions
- [x] ~~0528:27 "It's in Japanese."~~ Gone with the Charlie library scene
  (cut Oct 13).
- [ ] [0528:235](../../game/story/season1/0528.rpy#L235), 240 and 245:
  "Osaka" appears in all three options. Replace it with one invented city,
  spelled identically in all three so the grammar question stays fair.
- [ ] [0531:800](../../game/story/season1/0531.rpy#L800) "A North American
  educational adventure show" and
  [0531:819](../../game/story/season1/0531.rpy#L819) "my family crossed an
  ocean," plus the matching character thought at
  [0531:1166](../../game/story/season1/0531.rpy#L1166).
  - Combined with "an imported European soft drink"
    ([0515:200](../../game/story/season1/0515.rpy#L200)), these give the world
    a geography by elimination.
  - Suggested rewording: "a kids' show from overseas" and "then we moved."
  - How strict to be is your decision (§10).
- [ ] New since October 9: MC's "Mate," in your valedictorian line (0516)
  reads British or Australian, and he says "Dude" everywhere else.
- **Nudges:** `NUDGE P0.3`, six spots in 0515, 0516, 0528 and 0531, each
  with a paste-ready wording. For "Osaka", "in the city" needs no place name
  at all: the question stem already says Riku "still lives in his hometown."

### P0.4 Typos and garbled lines (players screenshot these)
- [X] [0515:386](../../game/story/season1/0515.rpy#L386): "moved from
  candescent to somewhat tranquil, if there wasn't someone outside…" is
  garbled. It's been flagged since the September 28 audit.
- [X] [0515:470](../../game/story/season1/0515.rpy#L470): "I run the filter
  until the water goes cold at the bottom" doesn't say what's happening.
  Rewrite it plainly.
- [X] [0515:126](../../game/story/season1/0515.rpy#L126): change "a pattern
  that she does every time" to "the way she does every time."
- [X] [0515:199](../../game/story/season1/0515.rpy#L199): change "In my years
  of living, I've never seen the brand before." to "I've never seen the
  brand."
- [X] [0517:278](../../game/story/season1/0517.rpy#L278): the "sister" guess.
  Have MC notice something first, such as the hovering hand at
  [0517:248](../../game/story/season1/0517.rpy#L248). Then Matsuda's "You have
  joined two households on remarkably little evidence!"
  ([0517:286](../../game/story/season1/0517.rpy#L286)) reads as the joke, not
  a continuity slip.
- [X] [0523:505](../../game/story/season1/0523.rpy#L505): "straightaway
  Meanwhile" is missing its period. It came from tonight's track trim.
- [ ] [0515:130](../../game/story/season1/0515.rpy#L130): "noted to find a
  better defense" doesn't parse. Also from tonight.
- [ ] Optional: [0515:127](../../game/story/season1/0515.rpy#L127), "every
  single time that grates my ears", reads as "every time that grates".
- **Nudges:** `NUDGE P0.4`, three spots, each with a fix.
- [ ] After all edits, run the two greps from the prose-conventions memory
  over season 1: questions that end in a period, and British spellings.
  - *October 12 at 00:40: both clean.* Re-run them after your last edit.
    Either ask Claude, or paste these into VS Code's search with regex on and
    `game/story/season1` as the folder to include. Imperatives such as "Do it."
    are expected false positives.
    - `(What|Who|Where|When|Why|How|Is|Are|Do|Does|Did|Can|Will|Would|Should|Have|Has)\b[^"]*\."`
    - `\b(colour|savour|favourite|realise|apologise|grey|theatre|centre|defence|jeweller|behaviour|humour|analyse|organise|recognise|whilst|amongst)\b`

### P0.5 Build hygiene
- [X] `config.version` is still "0.1.0"
  ([options.rpy:16](../../game/options.rpy#L16)). Set the release version. It
  also drives `persistent.oldversion` at
  [splash.rpy:725](../../game/splash.rpy#L725).
- [X] Lint was clean on October 9: 9,292 dialogue blocks and 97 menus across
  the whole game. Re-run it after every editing day and after Tuesday's last
  edit, using the isolated-savedir recipe so it can't touch your real
  persistent data.
  - *October 12: clean before and after the nudges, with identical counts
    (9,283 blocks, 97 menus, 0 unreachable).*
- [X] The orphan `.rpyc` check was clean on October 9. Re-run it before
  building.
  - *October 12: clean.*
- [ ] Confirm the ending you want in release. Currently it's the trailer, then
  "The Music Room is open.", then a return to the title.
  - The character-story unlocks and `ach_grant("music_on")` are commented out
    ([0531:1190](../../game/story/season1/0531.rpy#L1190)).
  - The comment says the achievement falls back to a value derived from
    `chapter05_completed`. P4 verifies that it actually registers.
  - **Nudge:** `NUDGE P0.5` at
    [0531:1200](../../game/story/season1/0531.rpy#L1200). Also,
    `renpy.save_persistent()` was commented out along with the rest of that
    block. The engine saves persistent data only on quit or on a save, so a
    crash between the end card and quitting would lose the Music Room unlock.
    Uncommenting just that one line (8-space indent) prevents that.
- [ ] Decide whether side content ships visible (§10). Whatever ships has to
  open and close without crashing (P4). There's no nudge for this one.

### P0.6 The first five minutes
- [X] Rewrite [0515:39-47](../../game/story/season1/0515.rpy#L39), the first
  narration after the cold open. It's still the weakest prose in the chapter,
  and it's the first thing every player reads after the hook.
  - Line 42: "My headphones drown out any possible noise that could be in my
    vicinity while my playlist has some newly added songs that I thought were
    pleasing." That's three clauses of filler, and "thought" slips the tense.
  - Line 44: "I think to myself in slanted wording" explains your italics
    convention to the player. Cut "in slanted wording."
  - Line 47: "rolls my headphones off of my dome and ears." "Off of" is
    redundant, and "dome and ears" is one body part too many.
  - Line 43: "before I can lower it" puts the pre-emption tic on the fifth
    line of the game.
  - Goal: the first box after the hook carries MC's voice and plants a small
    question. Right now it describes a pen tap and a locker door.
- [X] Shorten the 5-second black hold between the hook and the club room to 2
  or 3 seconds.

---

## 4. P1: the drama pass

These moves answer "nothing happens." Most are deletions, or plants of one to
five lines. Do them before the P2 line edits, because they decide which lines
survive.

### P1.1 Give the chapter a spine

Pick three or four open questions. Each one needs a plant in the first 20 to
30 minutes, a beat every few days that makes it a little more urgent, and an
open end on May 31 for Chapter 1 to inherit.

- [ ] **The valedictorian race.**
  - Plant it on Day 1 or Day 2: MC and Monika have traded first and second
    place since their first year.
  - Touch it again when exams are announced
    ([0520:144](../../game/story/season1/0520.rpy#L144)).
  - Exam week then has stakes for an honest player, and "Monday brings the
    grades." ([0531:1162](../../game/story/season1/0531.rpy#L1162)) becomes
    Chapter 1's hook.
  - This also fixes the gap in audit §10.3. One line putting **Matsuda** in
    the race ("third in the year, by the way") sets up the three possible
    speakers in GOALS.
  - *October 12: planted on Day 2 (0516, "trading places for, what, two
    years"). Still open: the touch at the exam announcement (`NUDGE P1.1` in
    0520) and Matsuda's line. Her line has no nudge; her May 29 post-exam text
    is one possible spot.*
- [ ] **The invitational.** The pieces already exist: "slow in June than gone
  in July" ([0523:551](../../game/story/season1/0523.rpy#L551)) and the
  entries talk ([0529:432-446](../../game/story/season1/0529.rpy#L432)).
  - Give the entries a deadline by May 21.
  - Have MC say out loud that he wants both races.
  - Every track scene then asks whether he'll get both, instead of rerunning
    the coach routine.
  - *Nudge: `NUDGE P1.1` in 0521, at Coach's after-practice talk. MC already
    says "I can handle both." on May 29.*
- [ ] **Asahina's eating should escalate, not repeat.**
  - Order the touchpoints so each one is a little more visible than the last.
  - Give MC one beat he can't shrug off. The tangerine at
    [0526:82](../../game/story/season1/0526.rpy#L82) is the right shape,
    since he nearly calls after her. Either let him, or let him stay quiet and
    have it cost him at dinner.
  - *Nudges: `NUDGE P1.1` at the tangerine in 0526, plus the matching May 26
    ending under P1.5.*
- [ ] **"The man who doesn't live here"**
  ([0515:269](../../game/story/season1/0515.rpy#L269)) is free intrigue that
  nothing picks up. Either pay it off with a second envelope later in May
  (Asahina: "Don't."), or cut it. What it means is your call (§10).
  *Nudge: `NUDGE P1.1 / DECIDE 10.7` in 0515.*
- [ ] **Who is Matsuda?** The answer-tease already exists on May 31 (her TV
  past). The question needs planting before May 17 (P1.6).

### P1.2 Let conflict leave residue
- [ ] **The May 19 dinner.**
  - Cut MC's same-scene apology
    ([0519:380](../../game/story/season1/0519.rpy#L380)) and let Asahina go
    quiet.
  - Carry it into the May 20 breakfast, where she already takes the last of
    the good jam "and does not apologize for it"
    ([0520:104](../../game/story/season1/0520.rpy#L104)). Write that so it
    reads as payback.
  - Her invite to play the party game
    ([0520:116](../../game/story/season1/0520.rpy#L116)) then becomes the
    olive branch.
  - That gives you a two-scene arc without writing a new scene.
  - *October 12: the apology is cut. She still bounces back smug in her very
    next line and jokes through the rest of dinner, so no residue survives
    yet. Nudges: `NUDGE P1.2` in 0519 (the dinner) and 0520 (the jam).*
- [ ] **The boundary text.**
  - Matsuda replies "Understood." and stops
    ([0523:868](../../game/story/season1/0523.rpy#L868)). Hold back the rest
    of her apology.
  - May 24 has no Matsuda in it, so make the silence felt: MC checks the
    thread at lunch, and again at night in place of the RPG scene
    ([0524:740-787](../../game/story/season1/0524.rpy#L740)).
  - Her "I did want to go with you. That part wasn't a bit." arrives on the
    night of May 24 or the morning of May 25.
  - The player spends a day wondering whether they ended it. On the dependency
    route, that silence is chilling in hindsight.
  - *Nudges: `NUDGE P1.2` in 0523 (hold the apology back) and in 0524 (the
    lunch check, and the RPG night it replaces).*
- [X] **Hikari and Homura.** Leave them unreconciled at the end of May 22 by
  cutting [0522:258-262](../../game/story/season1/0522.rpy#L258). Let the thaw
  land on May 26 with the "Board." exchange, which already plays like one.
- [ ] **The May 25 sleep-in branch.** Keep "It's okay! Really." but let it
  cost something the next morning, such as Monika's May 26 text being a beat
  shorter than usual.
  - *October 12: this collides with the contract in `s1_sleep_in.rpy` ("NOT
    PUNISHED... She lets him off, once, and means it."), and nothing reads
    `s1_slept_in` after May 25 yet. I'd skip it for this release (§0). Nudge:
    `NUDGE P1.2` in 0525.*
- [ ] **Monika's "Always."**
  ([0519:193](../../game/story/season1/0519.rpy#L193)). Let MC push once and
  get deflected. Her mask then becomes a question the player carries into the
  cafe ([0525:474-480](../../game/story/season1/0525.rpy#L474)), which
  answers part of it.
  - *October 12: this looks done. MC pushes once ("You just spent five
    minutes telling me how awful it is.") and she deflects twice. Check it off
    unless it still reads closed to you. Nudge: `NUDGE P1.2` in 0519.*

### P1.3 Leave two oddities unexplained
- [X] **The poster** ([0519:165-167](../../game/story/season1/0519.rpy#L165)).
  Delete "They changed it after the first trailer." and "They put it in the
  release poster." Keep "The old one doesn't have the hand." Nobody explains
  why.
- [X] **The cafe** ([0525:446](../../game/story/season1/0525.rpy#L446)).
  Delete only the first sentence, "I saw the pictures when I looked up the
  menu." What's left is "I kept thinking you'd take that seat.", said about a
  place she has never been, and that's the good kind of strange. Homura's
  "This is a real cafe." at
  [0530:433](../../game/story/season1/0530.rpy#L433) still works.
- [X] **The dream** (optional). Keep "Autoplay. Of course."
  ([0522:63](../../game/story/season1/0522.rpy#L63)), but leave one detail
  autoplay can't explain, such as the cup sliding toward the open door
  ([0522:42](../../game/story/season1/0522.rpy#L42)). One loose detail is
  enough.
- *Optional follow-up: `NUDGE P1.3` in 0519. MC's reply right after "The old
  one doesn't have the hand." still reads the hand as a marketing spoiler.*

### P1.4 Break the day template
- [ ] Cut a morning or bedroom-at-night bookend from at least eight days.
  These candidates change no relationship and leave no question open:
  - [0516:165-177](../../game/story/season1/0516.rpy#L165), the hallway;
  - [0517:206-224](../../game/story/season1/0517.rpy#L206), the bedroom (move
    the library text to the night scene);
  - [0519:423-431](../../game/story/season1/0519.rpy#L423), the knife video;
  - [0522:130-138](../../game/story/season1/0522.rpy#L130), class;
  - [0524:740-787](../../game/story/season1/0524.rpy#L740), the RPG, replaced
    per P1.2;
  - [0527:9-18](../../game/story/season1/0527.rpy#L9), the rooftop band;
  - [0529:183-198](../../game/story/season1/0529.rpy#L183), class;
  - [0529:470-481](../../game/story/season1/0529.rpy#L470), the walk home;
  - [0531:139-151](../../game/story/season1/0531.rpy#L139), class.
- [ ] Open three days in the middle of something, the way May 20 opens on
  Coach's call. For example:
  - May 17 opens on the evening walk, with the day summarized in two
    interstitial lines.
  - May 26 opens on the exam bell.
  - May 29 opens on Matsuda's "Are you on campus presently?" in the clean
    branch.
- [ ] Merge conversations that are split across scene changes. Each split
  costs a black screen plus a 2-second pause.
  - [0515:302-382](../../game/story/season1/0515.rpy#L302): the two kitchen
    scenes.
  - May 21: one rooftop lunch is split four times, at lines 85, 102, 115 and
    223.
  - May 18: the lobby is split by "Kotonoha spends the next half minute
    prepping our food" ([0518:278](../../game/story/season1/0518.rpy#L278)).
  - May 20: game night is three scenes, at lines 336, 387 and 439.
- **Nudges:** `NUDGE P1.4`, 16 spots: every bookend candidate and split scene
  listed above, plus the optional May 26 opening. Before cutting anything in
  0526 to 0529, read the exam-week rule in §0.

### P1.5 End days on turns, not on sleep

These days currently trail off at the end: May 16 (planner), May 18 (console),
May 19 (track shoes), May 20 ("Sleep takes a while to find me."), May 21
(microwave), May 24 (console off), May 25 ("Sunday ends without an
explosion."), May 26 (alarm), May 27 (cold pack), May 28 (freezer spoon),
May 29 (checkpoint) and May 30 (lamp).

- [ ] Rework at least five so they end on something open: an ignored buzz, a
  line he keeps replaying, an image. Your models are May 15 (the rinsed
  plate), May 17 ("Ah, SHIT!"), May 23 (the charger) and May 31.
- [ ] Specific swaps:
  - May 20: end on Asahina and Sam's glance
    ([0520:403](../../game/story/season1/0520.rpy#L403)).
  - May 24: end on Matsuda's silence (P1.2).
  - May 25: keep "Tomorrow, the papers turn over." and cut the line before
    it.
  - May 26: end on the lunch Asahina didn't eat.
  - May 28: end on Monika's still-unopened folder.
- **Nudges:** `P1.5`, seven spots: the five swaps above, plus two of my own
  candidates that need only deletions. May 16 ends on the lunch container,
  and May 19 ends on the unsent text to Matsuda.

### P1.6 Show Matsuda before May 17
- [X] Give her one glimpse on Day 1 or Day 2. The orange soda is "sold out
  again" ([0516:285](../../game/story/season1/0516.rpy#L285)), so a red-haired
  girl could walk off with the last bottle while talking at full volume to a
  friend holding a paper bag. That pays off the bottle cap, and the collision
  then answers a question instead of coming from nowhere.
- [ ] Alternatively, open May 17 on the evening walk so the collision lands
  early in the day (P1.4).
- *Nudges: `NUDGE P1.6` in 0516 and 0517. In 0516, May 17 and May 19 call her
  "the red-haired girl", but this line says "woman". In 0517, one line of
  recognition at the collision makes the glimpse pay off.*

### P1.7 Turn class scenes into scenes
- [ ] Cut [0524:445-506](../../game/story/season1/0524.rpy#L445) (matrices)
  outright.
- [ ] Halve these lectures. In each one, keep the quiz if it primes an exam,
  plus the one line about a person in the room.
  - [0516:112-161](../../game/story/season1/0516.rpy#L112), math. This is also
    the player's first quiz.
  - [0517:54-86](../../game/story/season1/0517.rpy#L54), civics.
  - [0519:109-148](../../game/story/season1/0519.rpy#L109), civics.
  - [0520:133-154](../../game/story/season1/0520.rpy#L133), biology.
  - [0521:9-78](../../game/story/season1/0521.rpy#L9), language arts.
- [ ] On May 21, keep the handout passage and "It can redistribute guilt."
  That line is the key to how the chapter's prose works. Cut the rest of the
  board talk.
- **Nudges:** `NUDGE P1.7`, six spots. The matrices nudge names the exact
  lines to delete. Nothing reads that lesson: no variable and no exam
  question.

### P1.8 Cut the back half's connective tissue
- [ ] Bring May 25-31's interstitial narration back down to the May 17-24
  level of about 200 to 250 words a day. Bus recaps, rinsed plates and walks
  go first.
- [ ] Exam week's between-paper hallway is the same scene six times: a
  classmate argues an answer and MC declines to weigh in. Keep two (the May 26
  water standard and the May 27 pH question), and cut or compress the rest.
- [ ] Cut the 60-line monster-video call
  ([0521:519-583](../../game/story/season1/0521.rpy#L519)) to about 15 lines.
  Keep practice, the cup handout, "Tsubaki Kareda?", "armaments" and "track
  boy." It was the September 28 audit's top trim candidate.
- **Nudges:** `NUDGE P1.8`, seven spots:
  - the interstitial targets at the top of 0525, 0529, 0530 and 0531;
  - the hallway repeats in 0527 and 0528 (the two keepers are marked `KEEP`);
  - the monster call. If you cut May 19's knife video, cut the call's knife
    joke too.

### P1.9 The third-joke rule
- [ ] In every scene, find runs of three or more quips in a row and cut the
  third. Give each scene a straight man. Coach and Kotonoha get funnier when
  they're funny less often.

### P1.10 Let Monika see Matsuda once
- [ ] The two never share a scene in May (audit §10.3), so the rivalry due by
  July has nothing to start from. The cheapest fix is in the May 30 hallway:
  Monika walks past with the second box while Matsuda is doing the cowboy
  bit. One look, no dialogue.
  - *Nudge: `NUDGE P1.10` in 0530, in the corridor during the cowboy bit.
    The boxes get carried before club, so she'd pass without one.*

---

## 5. P2: day by day

Line notes in play order. Anything already covered in P0 or P1 isn't repeated
here.

**Nudges:** every line note below has a `# NUDGE P2:` comment at its spot (30
in all), and every "keep" note is a `# NUDGE KEEP:` (10). Search `NUDGE P2`,
and the results list them in play order.

**May 15** (revised; 3,690 words, 13 scenes). The hook and the last scene are
the best bookends in the chapter. In between are eight home scenes with two
open threads, the movie and the college printout.
- [X] [0515:127](../../game/story/season1/0515.rpy#L127): "a place where it
  rightfully belongs" tacks a verdict onto the end. Stop the sentence at "back
  wall."
- [X] [0515:208](../../game/story/season1/0515.rpy#L208): "from a presumably
  brown paper bag." He can see the bag, so drop "presumably."
- [X] [0515:280-294](../../game/story/season1/0515.rpy#L280): nothing changes
  in the bedroom flop. Keep the water-stain rabbit if you love it, and fold
  the rest into the next interstitial.

**May 16** (revised; 3,911 words, 13 scenes). Sam's arrival and the kitchen
scene after it carry the day. The first half is breakfast banter, a lecture
and a hallway.
- [ ] [0516:24-26](../../game/story/season1/0516.rpy#L24): fold the wake-up
  into breakfast's first line.
- [ ] [0516:35-97](../../game/story/season1/0516.rpy#L35): breakfast runs
  three separate bits (the juice carton, the sleeve, the poster and the
  beard). Keep two.
- [ ] [0516:195-197](../../game/story/season1/0516.rpy#L195): give Hikari and
  Homura one concrete trait each here, so their May 22 fight has something to
  stand on.
- [ ] [0516:340-342](../../game/story/season1/0516.rpy#L340): cut the
  power-lines interstitial.

**May 17** (unrevised; 3,240 words, 12 scenes). The collision is the game's
first real lift, and it arrives at the end of the day. Everything before it
is the glue errand, for the fourth and fifth time.
- [ ] [0517:9-41](../../game/story/season1/0517.rpy#L9): the fourth scene in
  a row about the glue (after May 15's night and May 16's breakfast, and
  before 0517:172-199). Cut it, or make it about the college printout so "Ah,
  SHIT!" ([0517:518](../../game/story/season1/0517.rpy#L518)) gets set up.
- [ ] [0517:137-144](../../game/story/season1/0517.rpy#L137): fold the tech
  section into an interstitial and keep Kotonoha at the checkout.
- [ ] [0517:172-199](../../game/story/season1/0517.rpy#L172): cut the glue
  handoff to two lines.
- [ ] [0517:273-441](../../game/story/season1/0517.rpy#L273): the collision
  runs about 170 lines. Trim Matsuda's speeches by a quarter, and keep every
  one of Tsubaki's corrections.

**May 18** (unrevised; 3,926 words, 14 scenes). A well-built date. The sleeve
grab and "There wasn't a somebody else" are the romance's best beats, but the
day has two scenes too many.
- [ ] [0518:16-34](../../game/story/season1/0518.rpy#L16): trim the blender
  bit and get to Monika's text sooner.
- [ ] [0518:170-187](../../game/story/season1/0518.rpy#L170): fold the city
  walk into an interstitial.
- [ ] [0518:425-457](../../game/story/season1/0518.rpy#L425): cut the
  post-movie lobby. It's Kotonoha's fourth appearance in three days and her
  second in this room. Keep the photo outside.
- [ ] [0518:606-607](../../game/story/season1/0518.rpy#L606): cut the dinner
  summary lines, and keep the printout left face-up.

**May 19** (unrevised; 3,294 words, 7 scenes). The leanest day and a good
one. P1.2 and P1.3 make it strong.
- [ ] [0519:112](../../game/story/season1/0519.rpy#L112): "performative
  virtue" states the theme outright. Trim it under P1.7.

**May 20** (unrevised; 3,561 words, 12 scenes). Mom's case, Sam's volleyball
question, "A documentary." and "We don't derender when you leave the room" are
all strong.
- [ ] [0520:31-35](../../game/story/season1/0520.rpy#L31): the allergy pill
  could pay off "my prescribed medication" from 0515:471 (§10).
- [ ] [0520:233](../../game/story/season1/0520.rpy#L233): Hikari and Homura
  get their only real description here. Strengthen it.
- [ ] [0520:464-479](../../game/story/season1/0520.rpy#L464): keep the pizza
  beat whole when you merge the game-night scenes. It's the food thread's best
  escalation so far.

**May 21** (unrevised; 3,629 words, 11 scenes).
- [ ] [0521:298-385](../../game/story/season1/0521.rpy#L298): Coach's lines
  are good. Cut about a third of the warm-up narration.

**May 22** (unrevised; 2,073 words, 8 scenes).
- [ ] [0522:148-274](../../game/story/season1/0522.rpy#L148): the club fight
  has borrowed stakes, because the player barely knows Hikari and Homura. Two
  options:
  - set them up on May 16 and May 20; or
  - halve the fight and make it about **Monika**. Your demeanor note says
    she's tired of other people's behavior, and one passive-aggressive slip
    from her here would do more than the whole mediation.

**May 23** (unrevised; 5,563 words, 11 scenes). The chapter's best day.
- [ ] [0523:461-477](../../game/story/season1/0523.rpy#L461): keep "Wait, she
  knew you were up here?" exactly as written. It's the first deniable
  tracking beat.
- [ ] [0523:496-561](../../game/story/season1/0523.rpy#L496): trim the track
  narration.
- [ ] [0523:719-772](../../game/story/season1/0523.rpy#L719): cut a third of
  the website browsing. The heart of the scene is lines 651-701.

**May 24** (unrevised; 4,540 words, 9 scenes).
- [ ] [0524:105-152](../../game/story/season1/0524.rpy#L105): trim the
  principal. Keep Sam's button and the slogan.
- [ ] [0524:160-223](../../game/story/season1/0524.rpy#L160): keep Tsubaki's
  half-beat and Asahina's "That was private."

**May 25** (rewritten September 28; 6,033 words, 14 scenes).
- [ ] [0525:63-67](../../game/story/season1/0525.rpy#L63): cut the kid
  kicking the bus seat.
- [ ] [0525:719-772](../../game/story/season1/0525.rpy#L719): the pocket-dial
  call is funny. Halve it.

**May 26-28: exam week** (unrevised). For an honest player this is 18 quiz
questions and six versions of the same hallway. All the drama sits in the
cheat branch, which honest players never see.
- [ ] Give exam week a B-plot an honest player can see. Options:
  - Monika gets visibly worse each day. The cafe established her anxiety, so
    show her skipping lunch on May 27, and let the piano on May 28 be how she
    unwinds.
  - Asahina stops eating during her own exams.
  - Mom's hearing, promised for "this week" at
    [0520:48](../../game/story/season1/0520.rpy#L48), comes due during exam
    week.
- [ ] **Don't cut quiz questions this week.** The exam-guard checkpoints are
  keyed to them (`q1_open` through `q3_answered`), and the academic continuity
  doc treats them as a contract. Cut around them instead.
- [ ] [0527:413-448](../../game/story/season1/0527.rpy#L413): keep the
  Kotonoha cold-pack scene. "Six papers in three days" is a Chapter 5 seed.
- [ ] [0528:439-477](../../game/story/season1/0528.rpy#L439): keep Monika's
  piano.

**May 29** (unrevised; 4,963 words, 10 scenes).
- [ ] [0529:358-466](../../game/story/season1/0529.rpy#L358): Charlie's
  introduction works. Trim Coach's back-and-forth.
- [ ] [0529:625-691](../../game/story/season1/0529.rpy#L625): cut a third of
  the Copper Crown play-by-play. Keep the deck-thinning line (628) and the
  coalition.

**May 30** (unrevised; 5,681 words, 9 scenes).
- [ ] [0530:140-159](../../game/story/season1/0530.rpy#L140): cut class and
  the intercom down to the half-day logistics.
- [ ] [0530:273-344](../../game/story/season1/0530.rpy#L273): trim the box
  carrying. Keep the three erasure prompts (lines 315-320), because they're
  plants.
- [ ] [0530:351-456](../../game/story/season1/0530.rpy#L351): the club scene
  runs about 100 lines. Cut a third.

**May 31** (unrevised; 7,335 words, 10 scenes, about 5,900 words before its
only choice).
- [ ] [0531:14-129](../../game/story/season1/0531.rpy#L14): breakfast
  restates the plan a third time. Trim it.
- [ ] [0531:208-266](../../game/story/season1/0531.rpy#L208): trim track, and
  keep "Go be seventeen somewhere that does not have lanes painted on it."
- [ ] [0531:429-774](../../game/story/season1/0531.rpy#L429): the arcade runs
  about 340 lines.
  - Keep the races but compress one of the three, the TSK high score, the claw
    bird, and the photo booth.
  - Cut air hockey and the dance game to a line each.
- [ ] [0531:833-850](../../game/story/season1/0531.rpy#L833): trim the
  mystery-novel argument at the cafe.

---

## 6. P3: presentation and audio
- [ ] **Ambience:** add one audio channel plus a hook that maps each
  background to a room tone (§9). The main story has no ambience at all right
  now, so this is the biggest atmosphere upgrade available.
- [ ] **Bells:** the prose rings a school bell about 15 times, and the game
  has no bell sound.
- [ ] **Door variety:** all 40 door cues use the same pair of files
  (`moddooropen` and `moddoorclose`), whether it's the front door, the rooftop
  or the theater.
- [ ] Turn `# SFX SUGGESTION` comments into real cues wherever a sound now
  exists.
- [ ] After moving or cutting lines, check that each sprite expression still
  fits the line it now sits next to.
- [ ] Decide what to do with the OP's "Smug Sam" CG
  ([op.rpy:1634-1636](../../game/addons/Sick%20Ass%20Anime%20OP/op.rpy#L1634)).
  It still plays on every boot, before the main story's slow read of Sam
  (§10).
  - *Nudge: `NUDGE P3 / DECIDE 10.3`. Swapping in a different image keeps the
    OP in time with the music. Deleting the lines would throw the timing off.*
- [ ] **Music:** no cue changes (standing rule). Just confirm every
  main-story track has a Music Room credit. `Exam` and `Safety` still show
  "--" as the artist.
  - *Nudge: `NUDGE P3/P5` at
    [music_room.rpy:227](../../game/addons/Music%20Room/music_room.rpy#L227).*
- [ ] The sidewalk-collision CG is still a TODO
  ([0517:252](../../game/story/season1/0517.rpy#L252)). Ship without it.

---

## 7. P4: QA test matrix

Run everything on the **built zip in a fresh folder**, not from the SDK.
Developer mode changes how pauses, rollback and the dev tools behave.

- [ ] **Boot path:** first-run notice → OP (SKIP button, plus Esc, Space and
  Enter) → title → New Game → Chapter Select → disclaimer → name entry → Day 1.
  - At the disclaimer, also try "Do not proceed", which should return you to
    the title.
  - At name entry, try an empty name, a long name, and the "Yuri" refusal.
- [ ] **A full, timed, normal-speed playthrough on the honest path.** Write
  down every spot where your attention drifts. That's the next cut list.
- [ ] Save on each day, then load each save.
- [ ] The sleep-in branch on May 25.
- [ ] **Exam guard:**
  - one catch, carried through the May 29 counselor meeting, asking Mom on
    May 30, and the May 31 check-ins;
  - two catches, which lead to the bad ending, then a load attempt afterward
    (the locked-load path).
- [ ] **Cross-save bleed:** cheat in save B, then load a clean save A from
  after the exams. `_exam_one_catch` reads persistent data
  ([0529:13](../../game/story/season1/0529.rpy#L13), 0530:70, 0531:12), so A
  may show the caught branch. Decide whether that kind of meta-memory is
  intended (§10).
  - *Fixed October 11: the guard now keeps one ledger per run, and loading a
    save swaps that run's record in. `dev/checks/exam_guard_runs.rpy` prints
    14 PASS lines, and the recipe is in docs/engineering/QA.md. It's still
    worth one pass on the built zip.*
- [ ] **Dependency route:** on May 23, pick "You can leave it to me." Check
  that `weirdjingle` plays and the board photo arrives at 0523:581-585.
- [ ] Every character choice at least once (18 menus). Prioritize the ones
  with their own prose: the "Evening" showtime (May 18), the mediation
  (May 22), the callout tone (May 23), the poem image (May 24) and the offer
  (May 31).
- [ ] **Phone:** every thread opens, idle chatter unlocks on the right day,
  and the Saturday group chat shows 3 participants.
- [ ] Sticky notes, the planner and the poem display render. The theater
  house lights clear before the lobby (0518:420).
- [ ] **Ending:** the trailer plays, the Music Room line appears, the game
  returns to the title, the Music Room opens, and the "Curtain Call (For Now)"
  achievement registers.
- [ ] Skip through seen text, test auto-forward at its default, and open the
  history screen. Rollback is off in release
  ([options.rpy:101](../../game/options.rpy#L101)), so history is the only
  way to re-read a line.
- [ ] Text speed defaults to 50 cps
  ([options.rpy:76](../../game/options.rpy#L76)), but the "Normal" preset is
  60. Pick one (§10).
  - *Nudge: `NUDGE DECIDE 10.5`. If you pick 60, change the reset-to-defaults
    in screens.rpy too. It also writes 50.*
- [ ] **Performance** on the weakest machine you can find, mainly the blur
  transitions and the particles. If frames drop, lower the blur depths, not
  the timings.
- [ ] Time from launch to the title screen.
- [ ] **Fresh persistent data:** rename the save folder to see exactly what a
  new player sees.
- [ ] If side content ships visible, open and close every main-menu door with
  zero progress: Arcade, Archive, Vault, the gacha with no coins, and
  Achievements.
- [ ] Window title, icon, About and Credits, and the version string.

---

## 8. P5: release logistics
- [ ] **How it's distributed.** The build creates "Mod Export (All
  Platforms)" and excludes `game/**.rpa`
  ([options.rpy:197](../../game/options.rpy#L197),
  [232](../../game/options.rpy#L232)).
  - Confirm what a player needs installed for the build to run, and write the
    install steps to match.
  - Re-check Team Salvato's fan-work guidelines, since the build still relies
    on DDLC base files.
- [ ] **Third-party audio in the shipped files.** Everything under
  `game/assets/**` ships ([options.rpy:222](../../game/options.rpy#L222)).
  That includes `sfx/kangaroo_court/` (with names like `sfx-objection` and
  `sfx-guilty`) and `sfx/touhou/`, and both look ripped from other games.
  - Either exclude them from this build or accept the exposure knowingly.
  - Ask the same question of any music track without a license on file.
  - *October 12:*
    - Nothing in the code references `sfx/kangaroo_court/` (199 files), so
      excluding it can't break anything.
    - `sfx/touhou/` (37 files) is played by six side modes: Arcade,
      Invasions, the Asarhythm finale, the gacha, Kotonoha and Tsubaki.
    - A missing sound fails silently in release, because the engine raises
      only when `RENPY_DEBUG_SOUND` is set. Excluding `touhou/` mutes those
      modes but doesn't crash them.
    - Both exclude lines are ready to uncomment at `NUDGE P5` in
      options.rpy.
- [ ] **Content notes on the release page.** The in-game card is vague on
  purpose, but the page can be specific: implied disordered eating (never
  graphic), academic pressure and the consequences of cheating, and mild
  language.
- [ ] **Release page:**
  - sell the undertow and the genre promise, because the first hour won't do
    that on its own;
  - 4 to 6 screenshots (the cold open, Matsuda's entrance, the cafe, the photo
    booth);
  - playtime (5 to 6 hours) and platforms;
  - say that this is Chapter 0.5 of a longer story.
- [ ] Known issues and a changelog.
- [ ] A place for bug reports and feedback.

---

## 9. SFX shopping list

This list is short on purpose. These are the purchases that change how the
chapter *feels*; it doesn't try to cover every action.

Right now the script's sound design is 40 door cues, six other effects and
the music. The phone, sticky notes and planner bring their own sounds. **There
is no ambience at all.** Room tone gives the biggest atmosphere gain per
purchase, because each loop plays under hundreds of lines.

**Tier A: room tones (looping ambience)**

| # | Room tone | Where | Notes |
|---|---|---|---|
| 1 | House, day | breakfasts, kitchen, living room (~30 scenes) | fridge hum, faint street noise, a pipe tick |
| 2 | House, night | dinners and bedroom nights (~25) | quieter, with one distant car pass |
| 3 | Classroom | classes plus the 6 exam sessions (~20) | ventilation hum, chair creaks, pencils. For exams, drop the chatter and add the existing `clock.ogg`. |
| 4 | School hallway | lunch and between bells (~15) | a busy version and a near-empty one |
| 5 | Rooftop | 6 scenes | wind (audition the existing `sfx-wind.wav`) plus distant city and gym |
| 6 | Track | 6 scenes | open air, a distant whistle, footfalls on rubber |

**Tier B: signature one-shots**

| # | Sound | Why |
|---|---|---|
| 7 | School bells: warning, end of day, exam start | The prose rings a bell about 15 times, but the game has no bell sound. Use a generic electronic tone, **not the Westminster chime**, which reads as Japan. |
| 8 | Phone buzzing on a desk, plus a muffled pocket buzz | Only where the phone screen *doesn't* open. An ignored buzz is drama ("I leave it alone." 0520:419). The Phone System owns message sounds; don't double them. |
| 9 | Door variants: home front door, metal rooftop door, shop bell | Right now all 40 door cues use one pair of files. |
| 10 | Dream set: PA click and crackle, underwater bell, ticket-machine beep | May 22 is the chapter's main genre beat, and sound is what sells the uncanny. |
| 11 | The moment a teacher catches a cheater: a dry pencil-down or paper slap, then the room tone drops out | For the caught scenes that play under `safety`. |

**Tier C: big single scenes**

| # | Sound | Where |
|---|---|---|
| 12 | Cafe room tone, with cups and the espresso machine (mentioned twice in the prose) | May 25, May 31 |
| 13 | Arcade room tone, plus the photo-booth countdown and shutter | May 31 |
| 14 | Cooking: oil sizzle, kettle click and boil | the May 15 katsudon; the kettle on May 20 and May 23 |

**Already in the project; audition these before buying anything:**
- `clock.ogg`;
- `sfx-wind.wav`;
- `ac.ogg`, for the AC rattle at 0523:861;
- `rainpatter.ogg`, `pageflip.ogg` and `writing.ogg`;
- `fall2.ogg`, for the collision;
- `sfx-thunder.wav`.

Don't build the main story on `kangaroo_court/` or `touhou/` (see P5).

**Where to look:**
- Sonniss's GDC bundles (royalty-free);
- freesound.org, filtered to CC0 (CC-BY sounds need a credit);
- Pixabay;
- Zapsplat (the free tier needs a credit).

Check each license when you download, and keep the license file next to the
sound, as the audio README asks.

**Wiring it up in one evening, without editing 180 scene lines:**
1. Register one looping channel in `def_audio.rpy`:
   `renpy.music.register_channel("ambience", mixer="sfx", loop=True)`. Add a
   `define -50 audio.amb_*` alias for each loop, per the alias rule.
2. Map background names to room tones in a single dict.
3. Start the right loop from the `config.show` wrapper in
   [story_cast_framing.rpy](../../game/story_cast_framing.rpy#L346) whenever a
   `bg` image lands on the master layer. Chain onto that wrapper; don't
   replace it. The engine sends every `scene bg …` through `config.show`
   (`renpy/ast.py:730`).
   - Crossfade over about a second, and only restart when the loop actually
     changes.
4. Handle the exceptions by hand: the dream, the exam rooms (switch to the
   version without chatter), and the caught scenes (cut to silence).
5. Mix the room tones well under the music, so they're felt more than heard.

---

## 10. Decisions only you can make

My recommendation follows each one.

1. **Should players be able to click through pauses?** Yes (P0.2). It's the
   single largest pacing fix. *Done October 11.*
2. **How strict is the setting rule?** Fix "Japanese" and "Osaka" regardless.
   I'd also reword the continent references ("European," "North American,"
   "an ocean"). The food and the "indoor shoes" can stay.
3. **The OP's Smug Sam CG.** It still undercuts the slow read of Sam that the
   main story is built around (audit §8). I'd swap it out, or hold it back
   until Sam's turn is closer. *Nudge: `DECIDE 10.3` in op.rpy.*
4. **Side content in this build.** I'd ship it if every door passes the P4
   smoke test and each mode starts locked or empty. Otherwise, exclude it and
   say it's coming later.
5. **Default text speed: 50 or 60 cps.** I'd use 60, so the default matches
   the "Normal" preset. *Nudge: `DECIDE 10.5` in options.rpy.*
6. **Matsuda in the valedictorian race.** Add one line (P1.1).
7. **"The man who doesn't live here."** Pay it off or cut it. I'd pay it off,
   since it's free intrigue. *Nudge: `DECIDE 10.7` in 0515.*
8. **"My prescribed medication"**
   ([0515:471](../../game/story/season1/0515.rpy#L471)). If it's the allergy
   pill from May 20, say "allergy." Otherwise either cut it or follow it
   later. *Nudges: `DECIDE 10.8` in 0515 and 0520.*
9. **The Portrait of Zahrath**
   ([0523:816](../../game/story/season1/0523.rpy#L816)). Is it a deliberate
   setup? *Nudge: `DECIDE 10.9` in 0523.* (Charlie's cough went with the
   library scene, cut Oct 13; the 0529 track run is now his only
   introduction.)
10. **Rollback is off in release.** That's probably deliberate because of the
    exam guard, but it's unusual for a VN. Keep it, and make sure the history
    screen works.
11. **Exam memory across saves** (P4). Should the guard remember a cheat made
    in a *different* save once the exams are over? *Resolved October 11: the
    guard keeps one ledger per run, so a cheat in one run no longer reaches
    another run's saves.*

---

## 11. Not for this release

Out of scope, per your brief:
- side content, beyond the smoke test;
- what each music track means, and where cues go;
- rebuilding motion and gestures;
- Chapter 1 planning;
- dependency-route insertions after May 23;
- new CGs.
