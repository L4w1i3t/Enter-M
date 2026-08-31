# Systems, phone, and Chapter 0.5 integration pass — 2026-08-30

## Scope and outcome

This pass integrated six related requests: non-invasive Matsucoin receipts,
achievement coverage, developer tooling, phone usability and notifications,
Chapter 0.5 texture, and a from-scratch twelve-entry random conversation catalog.
The current production tree compiles with zero unreachable content. No existing
0515–0525 prose, choice, state write, label, or route was removed.

## Matsucoin receipts

- Earnings, lifetime totals, and one-time payout keys commit immediately.
- Notification amount and event count persist separately until the player next
  reaches the title, whether by returning normally or relaunching the game.
- `before_main_menu` reconciles achievements first, then Matsucoins, and stages
  one aggregate receipt. Nothing renders while `main_menu` is false.
- A receipt is acknowledged only after its animation finishes. Leaving the title
  early retries the same receipt later without crediting the wallet twice.
- Arcade results and gacha refunds retain their contextual inline readouts and do
  not also create a title receipt.

Detailed implementation note:
`docs/addons/Matsucoin Currency and Gacha/2026-08-30-deferred-payout-receipts-and-dev-audit.md`.

## Achievement and developer coverage

All nine live achievements now have both an exact completion hook and persisted
derived recovery. Hooks occur before Arcade/story result splits, while defeats,
forfeits, Practice, Endless, preview/debug waves, and unrelated Tsubaki routes
remain non-qualifying. The coverage audit reports 9/9 and no unknown award ids.

The Dev Hub's function and screen targets resolve, its release-build exclusion
and guarded title mount remain intact, and ALL SIDE CONTENT was behavior-tested
through enable, partial-repair, and disable. Achievement tools now include grant
all and a session-only revoke/retest path. Economy give/fill/reset and binder
controls remain reachable; reset also clears staged and persisted payout receipts.

Detailed achievement note:
`docs/addons/Achievements/2026-08-30-achievement-coverage-audit.md`.

## Phone experience

- Every badge counts actual available conversation entries, not conversation
  kinds. The quick menu, Phone header, contact row, thread header, and individual
  text/call/FaceTime controls all derive from `phone_random_available()`.
- A newly available id plays one existing receive cue on a dedicated SFX channel
  and shows a compact clickable phone chip above the dialogue box. The persistent
  quick-menu badge remains until the conversations are consumed.
- The saved availability snapshot detects a new id even when the total is
  unchanged, suppresses repeats after save/load, pauses while the handset is
  open, and accumulates skipped unlocks into one cue.
- The contact list explains what rows do; the thread exposes exact action counts;
  right-click/Escape closes the Phone or moves back one level.
- Compatibility saves cannot strand an available entry behind a missing contact
  row.

Production-runtime QA at 1280x720 staged two Asahina texts and one call at once.
All five total surfaces agreed on `3`, the thread displayed `2 texts / 1 call`,
the alert and controls were unclipped and legible, and the receive sound played
through the isolated channel. The test used a disposable source file and save
directory, both removed afterward.

Detailed UX note:
`docs/addons/Phone System/2026-08-30-phone-notification-ux.md`.

## Random conversation rebuild

The runtime catalog contains exactly twelve fresh `rc2_*` entries: three each
for Asahina, Matsuda, Himeko/Mom, and Monika. There are eight texts, two calls,
and two FaceTimes. Every entry is one-shot but independently gated by established
contact/media access and, where useful, a story date; none uses `seen` or `unseen`
to depend on another random conversation.

The premises are: Ashen Vow's “git gud” boss advice, Mr. Toast's disappearance,
the soup-store call, Matsuda's UI review, Matsuda's wrong-number blame shift,
the duck-hat FaceTime, Mom defining “mid,” Mom versus autocorrect, Mom's work
opinion call, Monika's detail-free draft request, the horror committee verdict,
and Monika's vice-president FaceTime rant. Retired conversation bodies were
removed from initialization; only their ids remain as old-save documentation.

## Chapter 0.5 texture pass

The full 0515–0525 run was reviewed against the live pacing ledger and character
continuity. Existing scenes already carried most of the required momentum, so
the additions stay small and causal:

- 0516: Sam reveals Asahina's complaint about MC hoarding healing items.
- 0517: Asahina repays the chip debt with a masking-tape warning label.
- 0519: Matsuda turns a threatened spreadsheet into a “field guide.”
- 0520: Sam silently trades MC away from the controller dropping inputs.
- 0522: Asahina installs three increasingly threatening wake-up alarms.
- 0523: she returns the “good charger” after quietly asking Mom about dorms.

Two nearby rough lines were also repaired during the continuity review: the
0515 cashier comeback and Asahina's grammatically broken 0520 stairway retort.
All additions remain at no more than two substantial sentences per textbox and
do not merge narration with dialogue.

## Validation

Passed from the project root:

```text
Achievement coverage audit: 9/9; 9 literal ids; 0 unknown/retired
Matsucoin deferred receipt contract: PASS
Developer unlock-all contract: PASS
Developer Hub contract: PASS (11 function buttons, 2 screen buttons)
Phone random conversation audit: 12/12 independent entries
Screen reference audit: 290 defined; 262 referenced; 0 missing
Ruff: clean for all six audit/test scripts
Scoped git diff --check: clean
Production MatsuPy compile: 0 unreachable items across 122 source files
Production MatsuPy lint: exit 0; no task-scoped warnings
```

Lint still lists the project's existing unloaded placeholder/legacy images (169
warning lines, chiefly the absent Natsuki MPT bank and old background assets).
This pass added no missing asset reference and produced no warning in a touched
story, phone, achievement, economy, or screen file.
