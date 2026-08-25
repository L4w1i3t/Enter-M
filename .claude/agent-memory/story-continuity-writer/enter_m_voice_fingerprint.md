---
name: enter-m-voice-fingerprint
description: ENTER M prose/narration style fingerprint and Ren'Py formatting conventions for voice-matching passes
metadata:
  type: project
---

**Narration POV:** First-person present tense, MC narrating. Two narration channels:
- `"..."` bare quotes = MC's in-scene narration (present tense, observational, dry).
- `nier "..."` = the same MC voice used for between-scene/time-skip bridges (the "Nier" character tag is a stylistic interstitial narrator, still MC). Ends each block with `call nier_clear from _call_nier_clear_<file>_<n>`.
- `"{i}...{/i}"` italic bare quotes = MC's interior thoughts (often the sharpest jokes, or the quiet admission he won't say aloud).

**MC voice rhythm:** Observational; finds the small physical detail in a room. Jokes are camouflage. Best beats let MC LOSE the clean witty sentence when blindsided ("...Huh.", "...", a plain flat line). Treats his own exhaustion/feelings as logistics. Calls distress "annoying," "a lot," "tiring," "nothing worth a fuss." Unreliable: says "fine"/"nothing major" while the scene shows otherwise. Self-aware bits like "personal growth at desk level."

**Restraint rule (CRITICAL):** After a tender/tense/revealing line, let 2-3 lines pass WITHOUT a punchline — use physical detail, silence, or action. Do not defuse every beat. Reference models: Monika's sleeve-grab aftermath, Mom's college talk, Tsubaki's "you don't sound like you're checking every sentence," Matsuda's plain "...Thank ya."

**Show, don't tell (CRITICAL):** Reveal emotion, character, and stakes through physical action, behavior, and concrete detail — never by naming the feeling or stating the trait. Don't write "she was nervous / he felt guilty / Mom was worried"; show the chopsticks that stop moving, the hand that migrates to the same sleeve she grabbed in the theater, the water-bottle cap turned so it faces him, the laugh that escapes through the nose, the bag set down too carefully. MC's unreliability, Tsubaki's insecurity, Sam's menace, Asahina's food/body strain, and Mom's fear are all meant to be carried behaviorally — keep them that way. Pairs with the restraint rule and the "don't over-diagnose characters in dialogue" note: if a line explains a character's internal model out loud (e.g. "her anxiety and her performance are directly proportional"), cut it and dramatize it instead. The reader should assign the meaning; the prose supplies the visible evidence.

**Joke economy:** In a banter chain, keep the sharpest joke and cut the second-best. Avoid every line being a punchline / competing for a laugh track.

**Fragment economy (STRONG user directive, added 2026-06-17):** SERIOUSLY reduce staccato narration tics — "Not x. Not y. Z." fragment runs, "the kind of x that…" constructions, "[verb]. [verb right after period]." clipped combinations, and lone single-word fragment lines ("Standing." / "Pain." / "Almost."). Prefer flowing sentences. The deliberate blindsided-flat-line for MC ("...Huh.", "...") is still fine; this targets the OVERUSED crutch, especially in narration. (The dedicated cleanup pass was DONE 2026-06-18 across 0517-0528 — see [[enter-m-session-2026-06-18]] for which staccato runs are INTENTIONAL and must be preserved: running-cadence litanies, rhetorical anaphora, despair-branch fragmentation, the repeat-confrontation composure-break register, MC's "...Huh."/"Mostly." beats.)

**Music transitions (house pattern, set 2026-06-17):** To change tracks at a scene change, put `stop music fadeout X.X` as the line BEFORE the `with <transition>` (the fade plays during the wipe/dissolve), then `play music <track>` with NO `fadein` right AFTER the transition. Do not use crossfades or `play music ... fadein`.

**Avoid:** dated internet/meme phrasing ("skill issue," "chosen violence," "rizz") UNLESS character-specific and intentional (Asahina does use online-speak as a teen tic, then MC narrates the cringe). Avoid purple prose on mundane errands ("stygian embrace"). Avoid over-diagnosing characters in dialogue (author-explaining-the-model lines).

**Ren'Py mechanics — preserve exactly:** character tags `mc m ma ts ah sa ko mom nier` plus teacher tags (`civics_teacher`, `math_teacher`, `science_teacher`, `japanese_teacher`, `track_coach`), sprite expressions (e.g. `show monika 1a at t11`), `$` python lines, `menu:` blocks, `jump`/`call`/`label`, `[player]` and `+ player +` substitution, phone helpers `phone_msg`, `phone_text_conversation`, `phone_call_line`, `phone_call_conversation`, mood/effect overlays, music/sound, `with` transitions. Blank `m_name`/`ma_name`/`ts_name` reassignments gate name reveals — keep. Only edit prose inside quotes; never the machinery.

**Recurring motifs/callbacks:** "sidewalk traffic" (Asahina's name for the Matsuda collision), the cup-and-open-door handout (recurs as dream + club joke), "joint custody" of MC's afternoons (club vs track), Kotonoha's behavioral uncanniness ("Most people watch where cars were"), Matsuda's bard/ornate voice that MC can ask her to drop.
