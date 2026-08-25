# QA: exam-week material versus the root repetition audit

Compared the live `MAIN_STORY_REPETITION_AUDIT.md` against
`.agents/audit_0525_0528_exam.md` and the current scripts. No story file was
edited.

## Must fix or retain in the live root draft

1. **Phone references — now corrected in the live draft.** The earlier G9 list
   incorrectly cited `0525.rpy:428` and `0525.rpy:870`; neither is a phone
   beat. The current list correctly uses `0525.rpy:88,1123,1196,1279,1308`.
2. **`before X can` count — now corrected/defined in the live draft.** A
   punctuation-bounded displayed-string scan finds 75 constructions: 55 with
   person/pronoun subjects and another 20 with named, object, or abstract
   subjects. The current table and G2 text now state both figures. Keep that
   definition; a bare “55 uses” is misleading because G2 itself discusses the
   personified variants.
3. **Scope count — use an approximation and state inclusion rules.** The live
   draft has already softened the old `69,700 / 73,700` claims to about
   `70,000 / 74,200`. That is safer. Custom-displayed strings
   (`phone_call_line`, phone-message arrays, poems, planner text, and thought
   ledgers) make “displayed words” parser-sensitive, so do not present a
   single exact total without publishing the extraction rule.

## Exam-week findings that need a root-level overview

These are structural enough that leaving them only in day tables would hide
the most important diagnosis:

1. **Separate three kinds of exam repetition.** The daily exam ritual is useful;
   the checkpoints, menus, subject labels, and caught-paper procedure are
   mechanical/clarifying; the avoidable fatigue is the 54-branch pattern
   `selected answer -> rationale -> italic answer/mnemonic`.
2. **Name the study-guide echo chain.** May 25 drills the exact civics,
   literature, biology, chemistry, and English material that May 26–28 then
   restate in prompts, options, explanations, and mnemonics. The story teaches
   a guide to its themes and then tests recognition rather than transfer.
3. **Name the wrong-answer overwrite.** Every wrong option is immediately
   corrected in MC’s thoughts. This repeats the right answer, lengthens all
   branches, prevents honest academic error from mattering, and removes the
   ordinary temptation that could make reloading a meaningful choice.
4. **Summarize the six caught-route template.** Each teacher becomes controlled
   or quiet, assigns a zero, turns the subject into a moral metaphor, then
   sends MC through the same Mom/record/Monika/home fear ledger. A player sees
   at most two catches, but any pair exposes the shared grammar. Differentiate
   institutional behavior and let each teacher own one subject-specific
   verdict.
5. **Treat the two Himeko confrontations as one duplicated structure.** Both use
   front door, standing mother/phone, bag command, refused explanation,
   panic-versus-choice distinction, institutional inventory,
   obedience-versus-remorse lesson, and stairs coda. The repeat scene should
   enter later and own only the changed category: trust becoming identity
   doubt, maternal inability, and love coexisting with distrust.
6. **Flag the branch-continuity problem.** At two catches,
   `exam_guard_home_confrontation` diverts immediately to the label named
   “repeat.” Two catches on the same day can therefore make that the player’s
   first home confrontation, even though its prose says “this time,” “last
   time,” and treats the stairs as altered. Conversely,
   `_exam_guard_home_multiple` in the normal confrontation is unreachable at
   the current two-catch threshold.
7. **Correct the bad-end threshold sentence.** The end fires at two catches,
   but `exam_guard.rpy:1039` says “Anything past that” starts becoming the
   chosen shape, grammatically assigning chosen agency to a third catch. Attach
   the judgment to the second catch or branch on the actual count.
8. **Keep the contract/resume caveat adjacent to the prose diagnosis.** Even an
   announced no-revision rule does not make every stale in-exam load an answer
   revision; it can be crash recovery or ordinary resume. The confrontation’s
   guilt is editorially “earned” only after this state distinction or a safe
   resume path exists.
9. **Protect route-parity duplicates.** Exact repetitions such as “Day two ends
   without applause,” the May 28 corridor setup, and branch-parity transition
   text are mutually exclusive in play. Do not list them as player fatigue;
   consolidate only for maintainability.

## Status-label QA

- Under the root report’s own definitions, G2 is more consistently **A+N** than
  **N**: `0530.rpy:207-211` already annotates the exact construction as narrator
  mind-reading, while the 75-instance corpus family is the expansion.
- G9 is likewise arguably **A+N** rather than **N**: local notes already target
  phone length, phone-as-scene-hinge behavior, facedown staging, and translated
  phone suspicion; “phones as punctuation” is the new synthesis.
- If the root report reserves **N** for a newly quantified corpus family even
  when individual instances are annotated, say so once. Otherwise these labels
  are inconsistent with G4–G7 and G10, which use **A+N** for the same
  local-symptom-plus-broader-pattern relationship.
- In the detailed exam audit, broad `facedown` and cross-speaker `Good` rows are
  better understood as **NEW SYNTHESIS** than bare **NEW**, because local notes
  already protect or criticize individual uses. This does not alter their
  editorial recommendations.

## Count QA for the detailed exam audit

The five-file lexical paragraph now correctly distinguishes strings containing
the term from total occurrences:

- `enough`: 68 strings / 71 occurrences
- `still`: 59 / 62
- `exact`/`exactly`: 34 / 35
- `clean`: 25 / 26
- `room`: 74 / 76

The earlier shorthand figures were string counts, not occurrence counts; the
live `.agents/audit_0525_0528_exam.md` has already been corrected.
