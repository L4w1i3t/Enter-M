# ENTER M — Review Fix Checklist

Companion to `BLIND_PLAYER_REVIEW.md`. The main story (May 15–31) has now been
annotated in place — every day file in `game/story/season1/` plus
`exam_guard.rpy` and `s1disc.rpy` carries a `BLIND PLAYER REVIEW NOTES` header
block and inline comments at the exact lines the review's findings live on.
**No code or prose was changed; annotations only.**

To find every annotation:

```
grep -rn "REVIEW \[" "game/story/season1"        # inline notes, tagged by category
grep -rn "BLIND PLAYER REVIEW NOTES" "game/story/season1"   # per-file headers
```

Inline tags used: `[CONTRACT]` `[REDUNDANCY]` `[AGENCY]` `[KEEP]`
`[VOICE HOMOGENEITY]` `[CURRICULUM-AS-ANNOTATION]` `[FIRST IMPRESSION RISK]`
`[NARRATOR BLIND SPOTS]` `[STAKES]` `[PACING]` `[STUDY-GUIDE PROBLEM]`.

Two design principles govern everything below (your stated goals, which the
review fully endorses):

1. **Trust the well-read audience.** Cut the second explanation, not the image.
   The poems are the house standard — trim the narration toward them.
2. **The player must matter.** Small converging expressive choices, honestly
   contracted rules, and judgments that only fire on things the player
   actually chose. "If it wants to judge me, it must first let the choice be
   mine."

---

## PART 1 — Main story: what to fix (work through the inline annotations)

### 1A. Opening contract (Priority #1) — `s1disc.rpy`, `0515.rpy`, `0531.rpy`
- [ ] Loan a restrained trailer fragment ("we were still happy here" shape) to
      the pre-Day-1 notice — promise the *shape* of loss, not events.
      (`s1disc.rpy` header, note 1; `0531.rpy` trailer note)
- [ ] Fix the Day-1 ending: "plenty more just like it ahead" is thematically
      perfect and a terrible retention message. Either end on an unresolved
      ordinary mismatch (the food detail), or return once to Monika's
      "What do you want?" in a way the protagonist can't explain.
      (`0515.rpy`, end-of-file note; camera-line note near the top)
- [ ] Decide what the camera line *is*: dormant meta-thread (soften the
      promise) or central (give it one more quiet disturbance before the
      trailer). Pick one; the current middle position is the problem.
- [x] Rename "Prologue" → **"Chapter 0.5"**: ~70k words is a novel-length
      act, and "prologue" told the player the real story hadn't started.
      Applied to the chapter plan (`s1disc.rpy`), the trailer sign-off card
      (`next_time_trailer.rpy`), `roadmap.md`, and every prose reference in
      the day files. Still to check when they exist: archive labels, store
      page copy.

### 1B. The 15–20% prose cut (Priority #2) — every day file
Cut in this order (the review's list; inline `[REDUNDANCY]` tags mark live
examples of each):
- [ ] The sentence after a gesture that already made the subtext clear.
- [ ] The third joke in an exchange after the dynamic has landed.
- [ ] Repeated travel/class/track/meal/phone transitions that change no
      relationship.
- [ ] Thematic school exposition later repeated by exams, poems, or family
      conversations.
- [ ] Emotional confirmations after a scene already found its ending.

Named first targets:
- [ ] **May 25** — ten emotional landings inventoried in the `0525.rpy`
      header; keep 4–5, demote the rest to ordinary exchange. Events all stay.
- [ ] **Copper Crown (May 29)** — keep the four load-bearing beats listed in
      the `0529.rpy` inline note; let nier narration carry the middle game.
- [ ] **Curriculum echoes** — keep at most 1–2 lessons with thematic
      resonance (the May 21 omitted-agency lesson is the strongest candidate;
      the May 22 dream already delivers it as image). Cut the italic recaps
      everywhere (`[CURRICULUM-AS-ANNOTATION]` tags in 0516/0517/0519/0521).
- [ ] **"He's good at this" Sam-verdict recitals** — one deliberate callback
      max; currently ~4 across the week (0516, 0520 ×2).
- [ ] **Motif tics** — "I file it under nothing" twice in one day (0519).

### 1C. Player agency (Priority #3) — converging expressive choices
All outcomes fixed; the player chooses tone/attention/honesty. Candidates are
tagged `[AGENCY]` in place, best first:
- [ ] Himeko's "What do you feel first?" — pick which honest-but-incomplete
      answer he leads with (`0523.rpy`). *The single highest-value insertion.*
- [ ] The Matsuda callout text — choose the tone, never the outcome
      (`0523.rpy`).
- [ ] Poem revision choice, remembered later (`0524.rpy`; payoff spots noted
      in `0530.rpy` and `0531.rpy`).
- [ ] Day-1 dinner: joke / stay quiet / say something real about Asahina's
      plate (`0515.rpy`).
- [ ] Day-1 movie-invite reply tone (`0515.rpy`).
- [ ] Monika's corridor silence: step into it or around it (`0517.rpy`).
- [ ] Handing Matsuda the contact info — tone (`0517.rpy`).
- [ ] Movie showtime pick — Monika literally says "I'll leave it up to you"
      (`0518.rpy`).
- [ ] Post-movie goodbye — the narration already lists the menu (`0518.rpy`).
- [ ] "Okay, stop." — the player sets the boundary (`0519.rpy`).
- [ ] Club mediation — whom to address first (`0522.rpy`).
- [ ] Final arcade invitation — HOW he offers, never whether (`0531.rpy`).

### 1D. Exam week save/load rule (Priority #4) — `exam_guard.rpy`, `0526–0528`
- [ ] State the rule diegetically BEFORE the first checkpoint arms — proctor
      speech slot marked in `0526.rpy` ("Answers are final once marked...").
- [ ] Make wrong exam answers STAY wrong; grade absorbs them. This creates
      the honest temptation the whole system currently lacks, and it makes
      all 18 exam menus real choices for free. (Tagged once in `0526.rpy`,
      applies to every "correction accepted" branch in all three days.)
- [ ] If feasible, distinguish crash/resume loads from answer-revision loads.
- [ ] Keep the mom confrontation scenes and the bad ending as written — they
      are earned once the doorway in is fair. Make "The exam remembers" a
      callback to the stated rule, not the rule's first reveal.

### 1E. Voice differentiation
- [ ] Let some characters be less articulate in the moment. Asahina should be
      blunt, not precise (`0517.rpy` "loud people find you" note). Let a
      character misread a gesture without narration correcting them; let an
      awkward sentence stay awkward.
- [ ] Reserve instant-perfect social diagnosis for SAM — it's his tell, and
      it only reads as sinister if nobody else does it (`0524.rpy` note).
- [ ] Give the narrator blind spots that STAY blind for a while — audit the
      elegant self-diagnoses (doomscroll essay etc.) and keep the best 2–3
      (`0519.rpy` note; Day-1 "Noted, filed" note).

### 1F. First-impression lines — `0515.rpy`
- [ ] "Fatass": keep the abrasive sibling rhythm, lose the body-size punchline
      OR make the discomfort register in-scene before the dinner beat.
- [ ] Glue innuendo: decide whether it earns its slot in the audition hour
      (both risk-lines currently stack in the player's first 20 minutes).

### 1G. Archive gating (Priority #5) — `s1disc.rpy`, `0531.rpy`
- [ ] Gate the `s1disc.rpy` all-content unlock behind `config.developer` /
      dev mode. It must not ship — it destroys the meet-people-then-learn-more
      progression and lets Purgatorium spoil Sam before Day 2.
- [ ] Make the `0531.rpy` end-of-Chapter-0.5 unlock a CURATED list, not a loop
      over the whole catalog. Stories unlock after the relevant character
      intro; the most revealing pieces (Purgatorium especially) after
      Chapter 0.5.

---

## PART 2 — Side content: the fixes (from the review, per piece)

### Archive-wide
- [ ] Add compact metadata to every side-story card:
      **Form** (prose / desktop sim / RPG / bullet hell / QTE / soul fight) ·
      **Approx. length** · **Input requirements** · **Difficulty / assisted
      mode available** · **Content notes** · **Canon status** (canon /
      non-canon / what-if / legacy).
- [ ] Sweep every archive description for undersell: "You guys like RPGs,
      right?" does not communicate a multi-hour genre suite; "Inspired by the
      Lacey Games horror series" does not communicate grooming/body/food/child
      endangerment themes.

### Tsubaki — "Heads" / "Tails"
- [ ] Make the reading order explicit: "Heads" first. (UI ordering, a label,
      or a soft lock.)
- [ ] Optional light trim only — the repetition is ritualistic, not redundant.
      Review: do NOT explain these more. Otherwise leave alone; strongest
      pure prose in the project.

### Kotonoha — "The Girl with Every Face"
- [ ] **Remove or rework the attention checks.** They test short-term memory,
      not interpretation, and eject the reader with an insult ("You weren't
      listening. No one ever does."). If a check must exist, make failure a
      diegetic beat, not an ejection.
- [ ] Trim the mid-story symmetry: each movement re-proves the same point;
      the cumulative effect turns confirmation instead of discovery.
      Protect the grandmother scene and the imperfect bow.

### Kotonoha — "The Void Hunter"
- [X] **BUG (fix before anyone tests it):** the elder says "the hollow" but
      the attention check requires "The Recess." Align the term, accept both,
      or rewrite the question.
- [ ] Same attention-check decision as above.
- [ ] Differentiate its structure from "Girl with Every Face" — read together,
      the titled-movements/variations/reflection/object/release template
      becomes formula. Vary at least the movement structure or the ending
      mechanism.

### Asahina — "Hina's World"
- [ ] Add an unobtrusive progress cue (the full mother confrontation currently
      requires core games + ALL chat sessions; a reasonable early logoff can
      miss the clearest real-world consequence)…
- [ ] …or ensure an early logoff still yields a smaller but COMPLETE ending.
- [ ] Rewrite the archive card description (see Archive-wide sweep) — long,
      fully diegetic desktop story; grooming, body/food pressure, child
      endangerment themes.
- [ ] Excess audit: seven games / eight chats / big gallery / huge filesystem
      — decide what is texture vs. requirement, and make the requirement set
      small. (Do NOT flatten the form — the review calls this the strongest
      interactive piece in the build; it's the agency model the main story
      should learn from.)

### Sam — "Purgatorium"
- [ ] Resolve the rigged prosecution, one of two ways:
      - Keep every accusation aimed explicitly at **Sam**, not "you"; or
      - Give the player genuine resistible choices (don't screenshot / read
        her history / close the app / refuse to chase Desire) and have the
        ending accusations track what the player actually did.
- [ ] Cut at least two of the stacked endings (Day-7 confrontation → crash →
      mirror room → phone intrusion → fragment assault → stat reveal →
      bedroom → ransom image all compete for the final word).
- [ ] Unlock AFTER Chapter 0.5 (see 1G) — it must not preempt the main
      story's slow read of Sam.

### Matsuda — "Ontological Seer" / normal & Id fights
- [ ] Form/difficulty label on the archive entry (it's effectively a game
      suite: length, keyboard demands, save restrictions).
- [ ] Add a story-only or assisted option so a narrative player can see the
      character material without JRPG + bullet-hell literacy.

### Monika — alternate fight (date mode)
- [ ] Warn about the QTE format on the entry card.
- [ ] Add a timing-accessibility option (2.8→1.5s shuffled QTEs are a
      reflex-reading wall).
- [ ] Reconsider the final-barrage top-slot rig — it's the same hidden-rule
      pattern as the exam guard (see Part 3).
- [ ] Look at Matsuda's "broke hers clean" joke in the quiet ending — it
      partially undoes the refusal-as-respect reframe.

### Kotonoha — alternate fight (danmaku)
- [ ] Keep practice mode; add a no-record **assisted reading** that lets a
      narrative player advance bar by bar without full-run restarts.
      (Keep the real mode untouched for enthusiasts.)

### Tsubaki — alternate fight (soul mode)
- [ ] Shorten the post-fight scolding on all routes (violence route
      especially — the game supplied the FIGHT verb, then condemns its use
      at length).
- [ ] Let each route leave one meaningful residue even though Tsubaki still
      falls (fatalism can stay; route choice must not reduce to font).
- [ ] Add a player-facing assist/practice mode (the dev-only fast route is
      not a player option).
- [ ] Betrayal route: reward discovery with content, not an extended attack
      on the player for finding it.

### Lost Record — "Mika"
- [ ] Relabel honestly: "Original 2021 record; preserved largely as written."
- [ ] Fix the genre tag — "Slice-of-Life" is wrong for meta powers, obsession,
      estrangement, and a threat against Monika's friends.
- [ ] Otherwise keep as an artifact; the Archive framing protects it.

---

## PART 3 — The cross-cutting rule: earned guilt, not entrapment

The review's most important structural observation. Five systems currently
create a player action, quietly rig its meaning, then prosecute the player:

| System | The trap | The fix (all above) |
|---|---|---|
| Exam week | Ordinary VN loading = "cheating" | State rule first + real wrong answers |
| Purgatorium | Forced acts, then "YOU did this" | Aim at Sam, or track real choices |
| Tsubaki FIGHT | Supplied verb, then condemnation | Shorten scolding, route residue |
| Tsubaki betrayal | Authored secret route, then punishment for finding it | Reward discovery |
| Kotonoha checks | Memory slip = "you never listen" | Remove/rework ejections |

**The keeper test for any judgment mechanic:** did the player (1) have a
comprehensible alternative, (2) understand enough of the stakes, and
(3) choose anyway? If yes to all three, judge away — that's the signature
motif the review says ENTER M could own ("interfaces that expose the desire
to control people and outcomes"). If not, it's entrapment; fix or cut.

---

## PART 4 — What NOT to change (review's explicit list)

- Daily structure — central to the eventual sense of lost ordinary time.
- Quiet, non-plot scenes as a category — remove repetition, not life.
- Matsuda's excess — manage dosage, don't flatten her.
- The Monika romance's restraint — do not make it more explicit earlier.
- Family meals / errands / calls / school texture — trim, never wholesale.
- "Heads"/"Tails" — do not explain them more.
- The side content's formal restlessness — curate access, don't unify genre.
- The trailer's placement at the end of May 31 — loan a fragment forward,
  keep the payoff where it is.

---

## PART 5 — Suggested order of operations

1. **Bugs & landmines first:** "the hollow"/"The Recess" (Void Hunter);
   gate both all-content unlocks (s1disc + 0531).
2. **Contract fixes:** pre-Day-1 trailer fragment; Day-1 ending; exam rule
   stated + wrong answers stay wrong. (These change how everything else
   reads, so do them before the prose pass.)
3. **Agency pass:** insert the converging choices, starting with Himeko's
   question and the Matsuda text (0523).
4. **Prose cut pass:** work day by day through the `[REDUNDANCY]` /
   `[CURRICULUM-AS-ANNOTATION]` / `[PACING]` tags; protect every `[KEEP]`.
5. **Side-content fairness & access:** Purgatorium accusations, Tsubaki
   scolding/residue, attention checks, assist modes, archive metadata.
6. **Labels & copy:** act renaming, archive descriptions, Mika relabel.
7. Re-run lint, then get a fresh blind playtest — specifically someone who
   did not build the arcade modes, for the balance questions the review
   declined to judge.
