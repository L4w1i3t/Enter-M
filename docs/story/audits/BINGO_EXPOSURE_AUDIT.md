# ENTER M — Bingo Exposure Audit

Audited August 24, 2026, against `docs/story/reference/BEATING_JAYS_BINGO_SHEET.txt`.

The brief was "find what in the whole game would tick these boxes, even as a
reach." So this document is written from **Jay's chair, not yours**: every square
is argued for the tick first, and your defense comes second. A square is only
called clean when a hostile reading genuinely runs out of material.

Three verdicts:

- **CONCEDED** — a reasonable viewer ticks it without needing to be talked into it.
- **REACHABLE** — a viewer can tick it with mental gymnastics; you have a real defense.
- **CLEAN** — there is nothing to point at. Contest it.

Tally: **11 conceded, 8 reachable, 6 clean.**

---

## The board

Reading the sheet's five columns as five columns of a 5×5 grid.

|   | Col 1 | Col 2 | Col 3 | Col 4 | Col 5 |
|---|---|---|---|---|---|
| 1 | Self harm · **CLEAN** | Referential humor · **CONCEDED** | OC-itis · **CONCEDED** | Art showcase · **CONCEDED** | Livestream joke · **REACHABLE** |
| 2 | Out-of-country item · **CONCEDED** | Fake-outs · **CONCEDED** | Dev mode shipped · **CLEAN** | Act 1 syndrome · **CLEAN** | "I gently open the door" · **CLEAN** |
| 3 | Monika main villain · **REACHABLE** | Yuri just exists · **REACHABLE** | FREE SPACE | Projection · **REACHABLE** | Mary Sue · **REACHABLE** |
| 4 | Randomly evil villain · **REACHABLE** | Meta/god complex · **CONCEDED** | Stuttering · **CLEAN** | Minor spelling · **REACHABLE** | Repetitive phrases · **CONCEDED** |
| 5 | Coding errors · **CLEAN** | Mental issues · **CONCEDED** | Pretentious writing · **REACHABLE** | Festival · **CONCEDED** | Contrivances · **CONCEDED** |

### The two lines that are actually live

Everything else on the board is broken by at least one clean square. Two lines
are not.

**COLUMN 2 — the dangerous one.** Referential humor, Fake-outs, Meta/god
complex, and Mental issues are all conceded. The whole column rests on one
square: **"Yuri just exists."** If Jay accepts that Yuri is not in the mod, the
line dies. If he counts her name-entry refusal line, he has a bingo without
arguing about anything else. This is the only place on the board where a single
concession loses you a line.

**ROW 3 — all reaches, no conceded squares.** Monika-as-villain, Yuri, FREE,
Projection, Mary Sue. Every cell is arguable and none is clean, so a generous
judge completes it and a strict one completes nothing. This row is decided
entirely by how charitable he is feeling, which means the row you cannot fix by
editing the game — only by being ready to argue it.

Both live lines pass through **Yuri**. That square is the single highest-value
thing on the board, and Section 8 is where it is argued.

Every other line is blocked:

| Line | Blocked by |
|---|---|
| Col 1 | Self harm, Coding errors |
| Col 3 | Dev mode, Stuttering |
| Col 4 | Act 1 syndrome |
| Col 5 | "I gently open the door" |
| Row 1 | Self harm |
| Row 2 | Dev mode, Act 1, gently-open-the-door |
| Row 4 | Stuttering |
| Row 5 | Coding errors |
| Diagonal ↘ | Self harm |
| Diagonal ↙ | Act 1 syndrome, Coding errors |

---

# COLUMN 1

## 1. Self harm — CLEAN

Searched for self-harm depiction, ideation, and euphemism across `game/`. The
only textual hit for the whole vocabulary is `kototouhou.rpy:250`, a GLSL comment
describing "two razor-thin concentric rings." Nothing self-inflicted happens to
anybody, and no character discusses it.

**What a hostile reading reaches for and why it fails:**

- `tsubaki_soul.rpy` ends all three routes in the same void fall
  (`:65`, "AND THE OUTCOME IS THE SAME"). But she is on marionette strings and
  the mode's whole thesis is that it is *"completely out of Tsubaki's control"* —
  the opposite of self-inflicted.
- Himeko has a `wasted` sprite and a drinking thread. That is substance use, not
  self-harm, and the sheet has a separate square for mental issues.
- Asahina's food thread is about being fed by other people, not about restriction.

The content-warning plate (`splash.rpy:3`) says *"not suitable for the faint of
heart or the sensitive"* — which invites the assumption more than the game earns
it. If Jay ticks this square, he is ticking your warning plate, not your script.

## 2. Out-of-country item — CONCEDED

This one is conceded because you built it on purpose and it is load-bearing.

- `0515.rpy:175` — *"it's from some sort of imported soda from Scotland."* A
  named foreign country, in narration, on Day 1. The inline comment confirms the
  intent: it plants Matsuda's imported-drink habit.
- The motif then pays off across the game: `ooc_0604_out_of_ten.rpy:119`
  (*"Imported."*), `:176` (a place by the station that does the imported stuff),
  `tsubaki_soul.rpy:918` (*"You drink Matsuda's imported soda"*).
- `0531.rpy:719` — *"Different school. Different continent."*
- `0531.rpy:361` — Matsuda was in *"a minor foreign-market production"*; at
  `cs_matsuda_01` the show is placed in North America explicitly.
- `0515.rpy:227`, `:302` — katsudon, kept on purpose per the setting rule.

Note the irony: the July 2026 marker sweep stripped every Japan reference to make
the setting read as nowhere, and the *residue of that decision* is what ticks
this box. A country had to be named to make the drink foreign.

**Only real exposure to reduce:** none worth taking. Removing "Scotland" costs
you a running character motif to win one square.

## 3. Monika being the main villain — REACHABLE

The text works hard against this and one design decision hands it back.

**What ticks it:**

- `0515.rpy:33` — the third scene of the game, Monika alone, to the player:
  *"...What do {i}you{/i} want?"* This is the first hint of a fourth wall in the
  mod and it is Monika delivering it. A viewer eight minutes in files her as the
  aware one, which in DDLC-mod grammar means villain.
- She is a **boss fight you win by being cruel to her**. `monika_date.rpy:6`–`:18`:
  you reject her on a timer, warmth heals her, and *"that dissonance teaches the
  player to be cruel."* Regardless of the intent, the shape on screen is
  "the player fights Monika."

**Your defense, and it is strong:**

- She is the moral center of the two biggest ensemble scenes. `cs_matsuda_01:808`
  — she detonates the table specifically to get Tsubaki's ignored question
  answered, having *counted* the four times it was ignored. `ooc_1030_uhoh` has her
  calling *"Read the room"* at Matsuda when the room turns.
- `monika_date.rpy:13` states outright that she is *"genuinely, earnestly trying
  to have a nice evening"* and that the hostility belongs to **Matsuda's arena**,
  not to Monika.
- Your own comment at `0515.rpy:29`–`:32` calls the fourth-wall line *"staged
  deliberately SMALL"* and *"deniable as something said to it."*

**Verdict:** reachable on the boss fight alone. Unfixable without cutting a whole
mode, and the mode is one of the best things here. Argue it, don't edit it.

## 4. Randomly evil villain — REACHABLE (and it's a short reach)

Two separate antagonists are, by design, unexplained forces with no motive.

- **The Archivists.** `invasions.rpy:6` — *"Not a character. A force — the way
  weather is a force."* Seven of them, named for genres, and `:35` sets the
  encounter rate at *"roughly 1/64"* at quiet story seams on repeat runs. So:
  seven nameless hostile entities that attack you at random, with the motive
  explicitly withheld (*"That motif pays off in the game's TRUE themes much
  later"*). "Randomly evil" is a fair-cop description of the mechanic even if it
  misreads the theme.
- **"It" in Tsubaki mode.** `tsubaki_soul.rpy:16`–`:26` — something finished the
  unbuilt roster slot, *"grabbed the SOUL sprite and bullet art from Kotonoha's
  cellar,"* and hung Tsubaki *"on marionette strings."* It is never named, never
  explains itself, and takes her because her hunger made her available. The
  header even instructs the writer to leave it *"as ambient wrongness."*

**Your defense:** neither is *random* — both are systems with stated rules, and
the withholding is a structural promise rather than a shrug. But "the villain's
motive is deferred to a later act that isn't written yet" is a hard sell to a
first-time viewer, and the Archivist encounter system is still on the drawing
board (`invasions.rpy:26`, nothing is wired to the story).

## 5. Coding errors — CLEAN

Verified this pass:

- `matsupy.exe <project> lint` → **zero warnings, zero errors**, report confirmed
  present (9,944 dialogue blocks, 104,966 words). Ran through a renamed SDK copy
  so the singleton did not swallow it.
- The project's own reachability audit reports **0 unreachable items across 127
  source files**.
- `dev.rpy:3` — `config.developer = "auto"`, which is off in a distribution.
- `options.rpy:97`–`:138` — thorough, first-match-wins build excludes: all `.rpy`
  source, `/docs/**`, the Developer Date Jump addon, `out_of_context/`,
  `dev_scene_manager.rpyc`, `errors.txt`, `traceback.txt`, `log.txt`, `**.bak`.
- No orphaned `.rpyc` (a `.rpyc` whose `.rpy` is gone loads anyway — checked, none).

**What is in the working tree that a repo-browsing judge could point at** — all
build-excluded, none of it ships:

- `errors.txt` — a real Ren'Py syntax error from a throwaway probe file
  (`game/zz_probe.rpy`, Aug 23 23:33). Harmless, but it is a crash log sitting in
  the project root.
- Five `.bak` files under `game/`: `arcade.rpy.bak`, `archive.rpy.bak`,
  `invasions.rpy.bak`, `dev_date_jump.rpy.bak`, and
  `games/ag_trial.rpyc.bak`.
- **Worth knowing independent of bingo:** `ag_trial.rpyc.bak` is the Nonstop
  Rebuttal minigame and **its `.rpy` source is not in the tree** — only the
  compiled artifact, renamed. Nothing references `ag_trial` any more, so the
  arcade is not broken; the mode is simply gone, and gone in a form you cannot
  edit. If you ever want it back, it has to be rewritten or recovered from git.

**Cheapest win on the whole board:** delete `errors.txt` and the five `.bak`
files. Thirty seconds, and the square stops having anything to photograph.

---

# COLUMN 2

## 6. Referential / meme humor — CONCEDED

Referential: heavily, deliberately, and credited. Meme: essentially absent.

The credits page names the debts out loud (`credits.rpy`):

- `:107` — Touhou Project (bullet-pattern grammar)
- `:108` — Undertale and Deltarune (box-fight format)
- `:104` — Shin Megami Tensei / Persona (press-turn system)
- `:91` — NieR (forest text-adventure format) — and the narrator's variable is
  literally `nier`
- `:172`–`:174` — borrowed music from Toby Fox, Fire Emblem: Radiant Dawn, and
  Danganronpa

Then the ID card name-entry screen is a dedicated reference bit
(`card.rpy:83`–`:129`): the entire Undertale cast has a bespoke refusal line
(*"already taken, kid"*, *"I'M NOT EVEN IN THIS GAME"*, *"Sorry, darling~"*), and
so does half the DDLC modding scene (*"Make a better template, first."*, *"The
Windows 11 of templates."*).

Lighter-weight referential humor in the main story: the JRPG played *"with about
fifteen self-imposed restrictions"* (`0515.rpy:351`), *"some chicken scratch of a
random character from a rhythm game I like"* (`0519.rpy:168`), Matsuda's chuuni
persona (`0523.rpy:221`).

**Your defense, on the meme half only:** a sweep for modern slang (rizz, sigma,
based, cringe, copium, skibidi, among us…) returns **nothing**. Nobody in this
game talks like a 2024 Discord server. If Jay's square means memes specifically,
you have a case. If it means "referential", it is conceded and there is no
argument to make.

## 7. Fake-outs — CONCEDED

The project has a house style of promising one shape and delivering another, and
the headers say so in your own words.

- **The rigged finale.** `monika_date.rpy:49` and `:1379` — *"RIGGED (untold): the
  deck never shuffles here, so the correct answer is ALWAYS the top option."*
  Options shuffle every prompt for the whole fight to train fast reading; the
  finale silently stops shuffling. Your own conundrum audit flags this as the one
  residual unfairness in that mode.
- **Three routes, one ending.** `tsubaki_soul.rpy:65` — *"AND THE OUTCOME IS THE
  SAME."* Violence, Pacifism, and Betrayal converge on an identical void fall.
  *"The routes change what YOU did, never what happens to her."*
- **The better-written trap.** The dependency route requires the substitution
  branch to be the *better scene* so that *"a blind player should finish it
  believing they found the most attentive way to care for her"* — and the
  culmination then tells them they became the replacement.
- **The declined warning that doesn't decline.** `s1disc.rpy:27` — picking "Do not
  proceed" gets *"...Then I cannot allow you any further"* and returns to the main
  menu instead of quitting.
- **The draw.** Greywake spends eight sessions building to a mutual KO, and the
  table's reaction *is* the scene (`cs_matsuda_01:673` onward, *"A {i}DRAW?!{/i}"*).

**No defense worth mounting.** These are good fake-outs, but they are fake-outs.

## 8. Yuri (the DDLC character) just exists — REACHABLE, and this is the square that matters

Both live bingo lines run through here, so it is worth being precise about
exactly how much Yuri there is.

**Her complete footprint in the mod:**

1. `card.rpy:87` — typing "yuri" as your name gets *"...Not appropriate."*
2. `credits.rpy:142` — one line acknowledging the original DDLC cast.
3. `ch_mika.rpy:467` / `ch_mika_rewrite.rpy:711` — Mika mentions *"My friends
   Monika and Yuri"*; `ch_mika_rewrite.rpy:819` names her in a list.
4. `lost_records/Mika/mod_assets/MPT/yuri_layeredimage.rpy` — a sprite definition
   that exists **only inside the Mika lost record**, not in the main cast file.

**The tick:** she is present, she has an asset, she has a canned line, and she
does nothing. That is a textbook reading of "just exists."

**The defense, and it is the best argument on the board:** she does not *exist* in
the mod at all. She has zero lines, zero appearances, and zero scenes. Her sprite
is scoped to a self-contained in-universe artifact where the DDLC cast is the
*subject*, not set dressing. And the one place a player can bump into her name,
the game's answer is to refuse. "Just exists" implies a character standing in a
room being unused; Yuri isn't in the building.

**If you want to kill this square outright**, the only cell you would have to
touch is `card.rpy:87` — and cutting a name-entry gag to break two bingo lines is
a real trade to consider. Leaving it in is also defensible; just know it is the
load-bearing cell.

## 9. Meta / god complex — CONCEDED

There is a narrator with authority over the player, and it is a designed feature.

- `s1disc.rpy:16` — *"Though coincidence, I have found, is only a pattern the
  reader has not finished tracing."*
- `s1disc.rpy:27` — *"...Then I cannot allow you any further."* The narrator gates
  entry to the story.
- The `nier` narrator addresses the player directly throughout and runs its own
  NVL presentation layer with sections and enter/exit ceremonies.
- `0515.rpy:33` — Monika's *"...What do {i}you{/i} want?"*
- One of the boss modes is named **Ontological Seer** (`credits.rpy:104`).
- `tsubaki_soul.rpy` is staged as a theater with a booth, marks, and lamps,
  possessed by an unnamed "it" that assembles the fight out of another mode's
  assets.
- The hidden route's culmination tells the player *they* became *"the narrative
  replacement"* — second person, aimed outward.

**No defense.** The meta thread is the spine of the project's back half. This box
is ticked by design and should be.

## 10. Mental issues — CONCEDED

Not a reach in any direction:

- **Tsubaki** — the entire dependency arc. `0523.rpy:121` (*"I swear I didn't
  follow you!"*), her twenty-minutes-before-asking speech, `0530.rpy:230`
  (*"She wanted to ask you herself"*), and a hidden route built on exploiting it.
- **Matsuda** — the performance mask; the acceptance speech delivered with
  visibly shaking hands (`0521.rpy`); the misspelled-name beat in the bookstore.
- **Asahina** — the food thread, and the phone that empties her face in
  `ooc_1030_uhoh`.
- **Kotonoha** — a character who *"can become any role someone needs and has
  almost no visible want of her own"* (your own `CHARACTER_OPINIONS.md:11`).
- **Himeko** — the drinking, and the `wasted` sprite.
- **Sam** — care that is indistinguishable from surveillance, tracked as a metric.

And the game announces it: `splash.rpy:3`, *"not suitable for the faint of heart
or the sensitive."*

---

# COLUMN 3

## 11. OC-itis — CONCEDED

Seven roster slots (`roster_view.rpy:387`–`:573`): Matsuda, Tsubaki, Asahina,
Sam, Mom (Himeko), Monika, Kotonoha. **Six are originals; one is from DDLC.**

Add the OC-only supporting cast — Mika (with her own lost record and a rewrite
of it), Daichi, Charlie, the NPC teachers, Gary/Gregor/Leif in Dead Fantasy — and
`ts` alone has 262 dialogue blocks against Monika's 657 and the narrator's 1,226.
The DDLC cast contributes Monika and a name-refusal list.

**No defense, and none wanted.** This is what the mod is. Worth noting only that
it is the single least contestable square on the sheet.

## 12. Dev mode enabled in the production build — CLEAN

- `dev.rpy:3` — `define config.developer = "auto"`. Off in a built distribution
  by definition; on only when launched from the SDK.
- `dev.rpy:6` — `_dismiss_pause = config.developer`, so it follows.
- Every dev surface is gated on `config.developer`: the achievements DEV SHOP
  (`achievements.rpy:924`), `inv_dev_godmode` (`invasions.rpy:667`), the four
  Archivist debug HUDs, the CG gallery and side-story dev unlocks.
- The dev-only *content* is excluded from the build outright, not merely gated:
  `options.rpy:114`–`:116` drops the Developer Date Jump addon,
  `dev_scene_manager.rpyc`, and all of `out_of_context/`.

**Standing risk, not a current one:** because the dev surfaces are gated on the
flag rather than excluded, a build made with `config.developer` forced to `True`
would ship a working achievement shop and four godmode toggles. The guard is one
line in one file. Worth a pre-release checklist item; not worth a tick today.

## 13. Free space — CONCEDED

Free.

## 14. Stuttering — CLEAN

Swept the full corpus for the `X-Xxx` pattern. **Thirteen instances in roughly
230,000 words**, and the distribution is the point:

| Where | Count | Lines |
|---|---|---|
| Main story, 0515–0531 (~74k words) | **2** | `0517.rpy:281` (*"A-Are you hurt?!"*), `0518.rpy:504` (*"S-Shut up!"*) |
| Mika lost record | 5 | `ch_mika.rpy:192`, `:329`, `:414`, `:464` |
| ID card name gags | 2 | `card.rpy:86` (Natsuki), `:125` (Alphys) |
| A Fine Date | 2 | `monika_date.rpy:1245`, `:1320` — Monika under duress |
| Purgatorium | 1 | `cs_sam_01.rpy:1160` |
| Next Time Trailer | 1 | `next_time_trailer.rpy:567` |

Two of those are quoted DDLC characters *as a joke about DDLC stuttering*, and
five are inside a document that is deliberately written in the vanilla register.

**Contest this one hard.** Two stutters in seventy-four thousand words of main
story is not a tic, it is an absence. If you want the number to be zero, the only
two cells are `0517.rpy:281` and `0518.rpy:504` — and the first one is Tsubaki
mid-collision, which is the one place it is earned.

## 15. Pretentious writing — REACHABLE

The main story is plain. Two other registers are not, and one of them is
extremely quotable out of context.

**What ticks it:**

- The gothic prose engine behind Heads/Tails. `cs_tsubaki_01.rpy:64` — *"But
  observe how calmly I write. Observe the evenness of these lines, the dates in
  the margins, the ink that has not once blotted. Would the mad number their
  pages?"* Also *"That is the whole of my life. You may keep that sentence; I have
  others."* Read aloud on stream, with no context, this is the single most
  tickable passage in the mod.
- The narrator's aphorisms: `s1disc.rpy:16`, *"coincidence… is only a pattern the
  reader has not finished tracing."*
- Your own repetition audit catalogs the adjacent failure modes as live tics:
  **G4 "Announcing restraint instead of practicing it"**, **G5 "Text about text
  after the text already worked"**, **G8 the house that "holds," "settles,"
  "remembers," or finds a "shape."** That document is evidence *for* the square as
  much as against it.

**Your defense:** the ornate register is diegetic — Heads is an in-universe
manuscript by a narrator whose whole characterization is a person performing
composure on paper, and Tails inverts it. The prose is pretentious *because she
is*. And the main-story narration, checked across `0515`–`0531`, stays concrete:
*"drafts traded, two read aloud, one unresolved argument about whether a sunset
can be 'smug.'"*

---

# COLUMN 4

## 16. Art showcase — CONCEDED

The Archive is seven modules of "look at the assets" (`archive.rpy:112`–`:120`):
Roster, **CG Gallery**, **Music Room**, Side Stories, Lost Records, Achievements,
**Cards**. On top of that:

- A 50-card gacha binder whose cards reference art that already shipped
  (`mc_cards.rpy`), plus a prize machine in the Arcade lobby.
- Roster View with per-character portraits, outfits, and a thoughts list.
- Music Room with play modes, a shuffle engine, and **CG visualization**.
- The Arcade hub as a jewel-case shelf with per-mode box art and three GLSL
  shaders on the cards.
- An **OP replay** hook and a **Next Time Trailer** — two sequences whose entire
  job is presentation.
- A credits page with 30+ entries.

**No defense.** A dedicated unlockable gallery *is* an art showcase. The only
honest framing is that it is a feature, not a symptom.

*(Unrelated but noticed: all seven Archive module icons still point at
`assets/dump/icon_placeholder.png`.)*

## 17. Act 1 syndrome — CLEAN

The square is specifically "retelling DDLC act 1, or even just the first day, to
set up the mod story." This mod does not do that.

- **Sayori and Natsuki do not appear anywhere in `game/story/`.** Zero hits, all
  files, main story and out-of-context alike.
- There is no recruitment scene. `0515.rpy` opens with MC already a club member
  handing in *"an obligatory poem for Monika's club"* (`:351`), mid-school-year,
  on May 15.
- There is no poem-writing minigame in the main story.
- The club room appears three times on Day 1 and the club is furniture, not the
  premise. Day 1's actual content is a corridor, a bus, a bottle cap, and cooking
  dinner with Mom.
- The story's own frame (`s1disc.rpy:30`) is a full school year, May to March,
  divided into six chapters — a structure DDLC does not have.

**Contest it flatly.** The only reach available is "it is still a literature club
with Monika in it," which describes the mod's premise, not a retelling.

## 18. Projection — REACHABLE

**What ticks it:** MC is a distance runner who writes, plays games under
self-imposed restriction rules (`0515.rpy:351`), has *"weird bouts of curiosity"*
(the inline note at `0515.rpy:175`), and narrates in a watchful, hesitant
register that your own character doc describes as *"MC watches everyone and
hesitates to act."* The credits are 30-plus consecutive *"by L4w1i3t"* lines. A
one-person project with an observer protagonist is the standard shape of this
accusation.

**Your defense is unusually good, because the game files the accusation itself.**
Matsuda's tabletop commander is named Matsuda Akai, and the table prosecutes her
for it in a scene you wrote:

- `cs_matsuda_01:883` — *"Akai is not a self-insert!"*
- *"Her name is Matsuda Akai."* / *"It's a COMMON name--"*
- *"You gave yourself a SOLO SCENE!"* / *"THAT WAS ATMOSPHERE."*

A story that stages the self-insert argument, loses it on purpose, and then has
the GM defend refusing to fudge the dice is not hiding from this. Whether that
counts as beating the square or proving it is exactly the mental gymnastics the
sheet invites.

## 19. Minor spelling mistakes — REACHABLE (one confirmed hit)

Method, so you can re-run it: extracted displayed strings only (say statements
and bare quoted narration, tags and interpolations stripped) from
`game/story`, `game/addons/Character Stories`, and `game/lost_records` — 7,796
distinct lowercase words. Then flagged every word used once that is a single edit
away from a word used six or more times, which is what a real typo looks like in
a 105,000-word corpus. Also swept the classic-misspelling list, British/American
variants, doubled words, doubled and missing spaces, and mid-sentence
capitalization.

**Confirmed:**

- `0521.rpy:258` — `mc "Oh, She's a third-year?"` — capital S mid-sentence. This
  is the only one, and it is in the main story where it will be seen.

**Arguable:**

- `ch_mika.rpy:48` and `:187` — *"towards"*. Acceptable American English but the
  house rule is American spelling, where *"toward"* is preferred. Both are inside
  the Mika lost record, so a register argument is available.

**Clean:** no classic misspellings (alot / definately / seperate / recieve /
occured / untill / wich / thier / …) anywhere in the project. No unintentional
doubled words — every hit (*that that*, *famous famous*, *kero kero*, *doki
doki*) is deliberate. No missing spaces after sentence punctuation. Every British
spelling in the project (`colour`, `realising`, `neighbours`, `cancelled`) is in a
**code comment**, never in displayed text.

**Fix the one cell and this square is as close to clean as a 105k-word script
gets.**

## 20. Festival — CONCEDED

The culture festival is not a set piece you could remove — it is a structural
landmark in the plot machinery:

- `dependency_route.rpy:128` — *"The culture festival gate."*
- `dependency_route.rpy:51` — the unwritten insertions run *"between June and the
  culture festival."*
- `ooc_1224_unasked.rpy` rewinds, on abort, to *"the following day … after the
  culture festival."*
- `ooc_0612_reception.rpy:16` — placed in June specifically to sit *"clear of the
  culture festival."*

And festivals appear as scenes across the side content:

- `cs_sam_01.rpy:1314`–`:1359` — "DAY 3 — The Festival": paper lanterns,
  hand-painted banners, a summer robe, a shooting gallery.
- `cs_kotonoha_01.rpy:405` — she organizes the autumn festival booth.
- `monika_date.rpy:96` — `mm_scene_festival` is in the phase-2 vignette pool.
- `mc_cards.rpy:325` — an SR card titled **"Festival Night."**
- Hina's World has a **"Festival Noodles"** photo with its own comment thread.

**No defense.** The July sweep removed the *words* "culture festival" from
displayed prose, but the event is still the calendar's spine and the side content
still stages festivals on screen.

---

# COLUMN 5

## 21. Livestream chat makes a dirty joke — REACHABLE (and out of your hands)

You cannot edit this square, but you can know where the trapdoors are. Ranked by
how certainly chat will take the shot:

1. **The ID card name entry.** A free-text field, early, with a bespoke response
   system. And `card.rpy:130`–`:157` proves the point: you already wrote a
   blacklist covering every major profanity, three slurs, and seven political
   figures. A name box with a blacklist is a dare.
2. **"A Fine Date."** A mode whose stated win condition is refusing Monika,
   escalating through phases titled EARNEST → INSISTENT → DESPERATE. The framing
   writes chat's joke for it.
3. **`0517`'s meet-cute.** A shoulder collision, two girls, *"Is your sister okay,
   though?"*, and a chin injury.
4. **`0531`'s claw machine.** *"Someone hit me with an inflatable sword"*
   (`0530.rpy:249`) and a bird *"with that much facial resolve."*
5. **The phone system.** Any UI where the player watches messages arrive.

Nothing here is salvageable by editing and nothing here is your fault. Consider
it a free square for Jay and move on.

## 22. "I gently open the door" in the writing — CLEAN

**Zero occurrences.** Searched the exact phrase, then every variant of
gently/softly/quietly + open/push + door.

*"gently"* appears **ten times in the entire project**, and never near a door:
eight are in code comments and file headers (`autofocus.rpy:7`, `card.rpy`,
`kototouhou.rpy`, `text.rpy`, `op_fx.rpy`, `atmosphere.rpy`), two are in prose
(`cs_kotonoha_01.rpy`, `cs_sam_01.rpy`) doing other work.

The only door-opening line in the project is `cs_kotonoha_01.rpy:553` — *"And I'd
open the door, just a crack, and she'd be sitting on her bed"* — which is a quoted
recollection inside a character's dialogue, has no adverb, and is not the cliché.

**Contest this one with confidence.** It is the cleanest square on the board.

## 23. Mary Sue characters — REACHABLE

**What ticks it:**

- **Sam.** `cs_sam_01.rpy:1359` — at the festival shooting gallery, *"every shot a
  bullseye."* He learns a card game in forty seconds and wins it politely
  (`ooc_1030_uhoh:138`), color-codes a study schedule before it is asked for, and
  reads Tsubaki's fear of notice on sight.
- **Kotonoha.** *"Can become any role someone needs and has almost no visible want
  of her own"* — your own words in `CHARACTER_OPINIONS.md:11`.
- **Matsuda's Akai** walks out of an eight-session war without a scratch.

**Your defense, which lands in every case:** the competence is always the
*symptom*, and the text always notices.

- Sam's flawlessness is written as unease, not wish-fulfilment — the care is
  *"optimized"* and *"objecting could make the objector sound unreasonable."* The
  festival girl is a duplicate in a bootleg space; the perfection is the horror.
- Kotonoha's role-fluency is her wound, and *Ontological Seer* exists specifically
  to *"let her be a clean loser when somebody actually learns her patterns."*
- Akai's unscratched exit is prosecuted at the table on the page
  (`cs_matsuda_01:883` onward), and the GM's answer is that she *wanted* Akai to
  win and the dice said no three times in the open.

A Mary Sue is unearned competence the story does not notice. Every candidate here
is competence the story is actively suspicious of. But the individual images —
every shot a bullseye, not a scratch — are tickable on sight.

## 24. Repetitive use of phrases — CONCEDED

Conceded, and the reason it is conceded is that you documented it yourself in
more detail than Jay ever will.

`MAIN_STORY_REPETITION_AUDIT.md` (July 24, 2026) is a close read of the ~74,200
displayed words of main story that names **thirteen corpus-wide patterns**:

- G1 the calibration sentence, *"X enough to Y"*
- G2 the pre-emptive action, *"before X can…"*
- G3 measured micro-pauses
- G4 announcing restraint instead of practicing it
- G5 text about text after the text already worked
- G6 gesture, then mind-reading, then ledger
- G7 legal/administrative metaphor escaping Mom's voice
- G8 the house that *holds*, *settles*, *remembers*, or finds a *shape*
- G9 phones as punctuation
- G10 decompression repeatedly announced
- G11 *actual*, *exactly*, *apparently*, *almost*
- G13 near-verbatim lines hidden across different days

The punctuation rule adds five more swept in August 2026 (without-ing,
pre-emption, *", which is"*, trailing *"anyway."*, and the triplet list) and warns
about the trap of replacing one tic with a single substitute phrase. And the audit
read the prose *on top of* 571 pre-existing `# REVISION` notes; a later pass
applied and deleted 1,673 annotations.

**Where that leaves you:** the tics are known, tracked, and partially fixed —
which is much better than not knowing. It does not make the square clean. G12 is
the honest counter: *"intentional repetition to protect"* — some recurrence is
structure, ritual, and payoff, and a viewer counting words cannot tell the
difference.

## 25. Contrivances — CONCEDED

Two tiers of exposure here.

**Mechanical, and catalogued in `FORCED_CONUNDRUM_AUDIT.md` Tier A:**

- **A1** — exam save-scumming carries a terminal punishment for standard VN
  behavior.
- **A2** — the rigged Last Resort (see square 7).
- **A3** — three moral routes, one identical fall.
- **A4** — the dependency route's all-or-nothing gate. Defensible by design, and
  the audit explains why the chain had to replace a threshold; still a machine
  that only ever produces one reading.

**Narrative, and this is what a viewer actually means by the word:**

- `0515.rpy` — MC's name is entered because Monika happens to find his ID card on
  the floor of the corridor she happens to be tidying.
- `0517.rpy` — the two most important new characters are met by walking into one
  of them while looking at a phone. Matsuda says it out loud: *"Collision as
  inciting incident! Crude, but effective."*
- `0523.rpy:121` — Tsubaki is on the same roof on consecutive days, and the game
  lampshades it rather than solving it: *"I mean...I swear I didn't follow you!"*
  followed by *"...Retroactively, that sounds worse out loud than it did in my
  head."*
- `0524.rpy` — Tsubaki's class happens to cut through the exact row where MC,
  Asahina, and Sam are standing, which is how Sam meets her.
- `0531.rpy:355` — the used-bookstore clearance rack happens to contain the one
  magazine that misspelled Matsuda's name.

**Your defense on the narrative tier:** every one of these is lampshaded by a
character in the scene, which is a deliberate choice and a real difference from a
contrivance the story hopes you don't notice. Matsuda naming the collision as an
inciting incident is the mod telling you it knows. Whether "we know" counts as a
fix is the argument, and it is the same argument as square 18.

---

## If you want to move the needle

Ranked by cost-to-benefit, not by importance.

1. **Delete `errors.txt` and the five `game/**/*.bak` files.** Thirty seconds.
   Removes the only physical evidence for "coding errors." *(Read the
   `ag_trial.rpyc.bak` note in square 5 first — that file is the last copy of a
   cut minigame, so move it out of the tree rather than deleting it.)*
2. **Fix `0521.rpy:258`** — *"Oh, She's"* → *"Oh, she's."* One character. Takes the
   spelling square from "one confirmed hit" to clean.
3. **Decide about `card.rpy:87`** — the Yuri name-entry line. It is the load-bearing
   cell in both live bingo lines. Cutting one joke breaks Column 2 and weakens
   Row 3. Keeping it means being ready to argue "she isn't in the mod."
4. **Consider `0518.rpy:504`** — *"S-Shut up!"* Removing it leaves exactly one
   stutter in the whole main story, and the survivor (`0517.rpy:281`) is the
   earned one. Cheap way to make an already-clean square unarguable.
5. **Add a pre-release check that `config.developer` is not forced `True`.** Not a
   current tick; the only thing standing between the shipped build and a working
   godmode menu is one line in `dev.rpy`.
6. **Everything else on this sheet is either load-bearing or out of your hands.**
   Scotland, the Archive, the festival, the OC cast, the meta narrator, and the
   referential debts are all things the mod is *made of*. Ticking those squares is
   the cost of the mod existing, and trading any of them for a bingo square would
   be a bad deal.

## Method

- Lint: `matsupy.exe "<project>" lint` via a renamed SDK copy (the singleton is
  keyed to the executable path, so a copy lints while the game runs). Clean,
  report verified present.
- Reachability: the project's own content audit, 0 unreachable across 127 files.
- Prose sweeps: displayed strings only — say statements and bare quoted narration,
  with `{tags}` and `[interpolations]` stripped — across `game/story`,
  `game/addons/Character Stories`, and `game/lost_records`.
- Typo detection: rare-word / common-neighbour edit-distance scan (see square 19),
  plus targeted lists for misspellings, transatlantic variants, doubled words, and
  spacing.
- Corroborating project docs: `FORCED_CONUNDRUM_AUDIT.md`,
  `MAIN_STORY_REPETITION_AUDIT.md`, `CHARACTER_OPINIONS.md`,
  `BEATING_JAYS_BINGO_SHEET.txt`.
