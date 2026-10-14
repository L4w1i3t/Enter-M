# ENTER M Act 1 plans

Updated September 25, 2026. [GOALS.txt](../GOALS.txt) preserves the author's
month-by-month checkpoints; the [prose guide](../story/MAIN_STORY_PROSE_AND_INTENT_GUIDE.md)
preserves voice and creative direction. Future events below are plans, not
implemented story. Current script content takes priority over old inventories.

## Implemented boundary

May 15–31 are present as 17 day files in `game/story/season1/`, with choice,
sleep-in, disclaimer, and exam-guard support. `game/chapter_select.rpy` checks
entry-label existence; its later-chapter cards are not proof of written days.
`game/story/out_of_context/` contains written-ahead scenes and author stubs.
Those files remain separate from campaign continuity and are excluded by the
build rules. Read each file before treating it as finished prose.

The dependency route has its May insertion and an incomplete-manifest gate in
`game/story/dependency_route.rpy`. Exam state and checkpoints exist; a complete
multi-term class-ranking/graduation system is still future work. Neither old
developer-scene labels nor historical roadmap code tables establish current
features. Repository status and backups must be checked directly, not inferred
from a previous report claiming version control was missing.

## Calendar and author checkpoints

| Chapter | Planned dates | Checkpoints |
| --- | --- | --- |
| 0.5 | May 15–31 | Introduce the cast, relationships, ordinary warmth, and a lived-in daily structure. |
| 1 | June 1–July 15 | Define the six-person friend group by June's end; Tsubaki's birthday; establish follow-through on May invitations. |
| 2 | July 16–September 1 | Triangle hints and Matsuda/Monika rivalry; beach and fireworks; visits to MC's and Matsuda's houses; Asahina's birthday. |
| 3 | September 2–October 15 | Triangle in full bloom, convention, Monika's and Matsuda's birthdays, growing fractures and the first major domino. |
| 4 | October 16–December 31 | Festival and Halloween without Asahina; Himeko's confrontation/illness; Sam unveiled; Tsubaki's decline and gradual disappearance; Matsuda's dominance. |
| 5 | January 1–March 7 | MC isolated, Kotonoha reaches out, Tsubaki absent without an exit scene; relationships end or transform; club disbands; graduation and perseverance. |

GOALS establishes monthly deadlines; the chapter table is their planning
placement. Exact dates inherited from deleted drafts, including illness
disclosure and entrance-exam days, need author confirmation before drafting.
Birthdays already in the roster can be read from `roster_view.rpy`; do not
silently replace author checkpoints with dates from older summaries.

## Decisions before later chapters

1. Choose the mix of full days, individual scenes, and calendar passages.
   Earlier numeric word/day budgets were proposals, not author requirements.
2. Define Chapter 3's first domino and its preparation. Deniable irregularities
   can precede the shocking high-stakes event required by GOALS.
3. Decide what Sam's true nature means and how the cast learns it in November.
   His earlier friendship and care must not become retroactively fraudulent.
4. Give MC a believable excuse to leave Matsuda. The author favors an exit he
   can permit himself, not sudden therapeutic insight.
5. Design multi-term exam results, rival standings, and the three possible
   graduation speakers. Preserve current checkpoint/scoring contracts while
   adding later periods; do not silently override the player's answers to force
   a scripted academic decline.
6. Define music meanings before new cue placement. Existing authored cues stay
   meaningful; `ch5_day` and `ch5_night` are not a complete scoring plan.
7. Plan new gestures and camera movement against the current slot, framing,
   Autofocus, and stage-panel implementations. The old “0/17 days” claim was not
   a current presentation audit; see [open work](TODO.txt).
8. Decide whether Tsubaki's erasure affects only the story or also phone history,
   optional conversations, roster, Archive stories, CGs, and achievements. A
   “Dead” label or explicit farewell conflicts with GOALS. Inspect actual gate
   APIs before proposing a new one.
9. Decide Chapter 5's narration form and whether/when it returns. This can affect
   late-December writing and the handling of exams and time passage.
10. Decide the narrative use of player birthdays and other optional calendar
    beats. Existing input fields do not by themselves promise a story event.

## Chapter 5: direct author intent, September 21

The chapter should be somber, isolating, and almost frozen from January 1 to
March 7, despite the approaching deadline. It should not have the psychological
horror intensity of the previous chapters. MC is at his lowest and loneliest:
Himeko declines from cancer despite treatment; Asahina gives him a colder
shoulder; Sam is still at large; the friend group has fractured; Matsuda has him
enchained; Monika is reduced to club business; indoor track has begun and his
heart is not in it.

The collapse matters because he had learned to be more open and trusting. His
perception changes for good. Kotonoha, previously a background running gag, has
been paying attention and is the one hand that still reaches out to help.
Chapters 1–4 therefore need real warmth, chosen trust, meaningful track activity,
and Kotonoha's specific practical attention. Himeko's treatment needs a coherent
timeline. Formal club disbanding should acknowledge a club that already stopped
functioning, so graduation can make it feel like a bygone era.

The author's narration idea remains undecided: remove MC's narration and inner
thoughts, leaving action, dialogue, attention, and menus. If adopted, `nier`
also needs reconsideration because it carries his diction. Calendar, scene
cuts, blocking, phone behavior, objects, and sound must orient the player; other
characters must not become substitute narrators explaining his feelings.

Open choices include complete silence versus spare observable descriptions,
an abrupt chapter-boundary change versus December thinning, and whether his
voice returns when accepting help, leaving Matsuda, or graduating. The
perseverance beat cannot depend on MC giving the speech, because Monika or
Matsuda may speak instead. These are author decisions, not implementation tasks
already approved by the old roadmap.

Winter grades/music/backgrounds are possible tools, not proof of a final visual
or acoustic design. The deleted New Year's draft's numerical saturation and
camera rules remain historical proposals. Preserve a bittersweet spring rather
than a clean emotional reset.

## Continuity to carry forward

Read the actual closing May scenes and
`game/addons/Next Time Trailer/next_time_trailer.rpy` before drafting. Follow up
the Copper Crown rematch, returned grades, another arcade invitation, Saturday
chat, photo strip, poem, valedictorian competition, Matsuda's television past,
Asahina's unresolved food/body strain, Sam's practical management, Kotonoha's
attention, and Himeko's “Walk instead if you need to.” Assign the trailer's
unattributed fragments to scenes without treating an old proposed assignment as
canon. A chapter's quiet routines must have changed meaning when they return.

The six-person group should be established by June's end. Preserve unequal
starting familiarity: siblings, MC/Monika's year of friendship, Asahina/Sam's
relationship, and Matsuda/Tsubaki's friendship. Earn newer pairs' reasons to
seek one another without making MC or Matsuda arrange every encounter.

## Standing author rules

- Choices may change events, locations, participants, or decisions. The former
  rule limiting choices to tone is retired. Keep the dependency chain's own
  all-or-nothing contract and abort conditions.
- No country, currency, or loanwords in displayed setting exposition; retain
  the school calendar. Call the culture festival “the festival” on screen.
- Text messages use the phone system. Avoid ironic music drops on painful
  moments; preserve silence or sound from within the scene.
- Tsubaki has no death, move, goodbye, identifiable removal, or retrospective
  announcement that she existed. Her last appearance must not read as one.
- Matsuda's harm complicates sincere warmth; Sam's danger concerns his model
  of care. Preserve character knowledge and uncertainty.

Before shipping a chapter, verify its entry and prior-day handoff, route/state
contracts, optional-content gates, presentation/assets, unlocks, build exclusions,
and a normal-speed playthrough. Static checks and accelerated fixtures are
separate evidence. [Earlier design](../history/early-story-design.md) preserves
distinct character/later-act ideas; [revision history](../history/story-revisions.md)
records superseded editorial work.
