# Achievement Coverage Audit — 2026-08-30

## Outcome

The nine-trophy catalog now uses two independent award paths for every objective:

1. an exact `ach_grant()` event at the completion beat, before any Arcade/story
   result split; and
2. a persisted derived condition used by `ach_sync()` to reconcile older saves,
   interrupted result screens, persistent merges, and quit/relaunch cases.

This closes both failure shapes: a completed objective no longer has to wait for
an unrelated Archive visit, and a missed exact hook can no longer leave a trophy
permanently unobtainable.

## Objective-to-trigger coverage

| Trophy id | Player objective | Exact event hook | Derived recovery | Non-qualifying exits audited |
| --- | --- | --- | --- | --- |
| `music_on` | Complete Chapter 0.5 | `a0531`, after the curtain/trailer and `chapter05_completed = True` | `persistent.chapter05_completed` | The chapter has one linear return; no earlier return awards it. |
| `beat_matsuda` | Beat Normal Mode | `cs_matsuda_02_battle`, Normal victory branch | `persistent.id_mode_unlocked` | Defeat, retry, party repick, and pause-menu forfeit do not grant. Award precedes the Arcade split. |
| `koto_clear` | Beat Kotonoha's fixed eight-bar mode | `kototouhou_fight`, real/debug victory excluding Practice and Endless | `persistent.kotomode_cleared` from `KTGame._finish()` | Practice, Endless, debug wave, defeat, give-up, and pre-fight leave do not grant. Award precedes the Arcade split. |
| `date_win` | Beat Monika date mode | `mm_victory`, after the last-resort clear | `persistent.arcade_monika_cleared` | The mode's loop cannot reach the ending without `mm_lr_win`; award precedes the Arcade split. |
| `cards_30` | Pull at least 30 unique cards | Completed reveal close through `ach_grant_if_met("cards_30")` | Live unique-card census, target 30 | Duplicates do not advance the census. Quitting during the reveal is recovered on next load from the already-saved card set. |
| `matsuda_id` | Beat Id Mode | `cs_matsuda_02_battle`, Id victory branch | `persistent.arcade_id_cleared` | Defeat/forfeit do not grant. Award precedes the Arcade split. |
| `tsuba_spare` | Clear Tsubaki Soul through pacifism | `tsubamode_fight`, `victory_p` branch after route history is recorded | `tsubamode_routes_cleared` plus last-outcome migration | Defeat, give-up, and other endings do not grant. Award precedes the Arcade split. |
| `tsuba_violence` | Clear Tsubaki Soul through violence | `tsubamode_fight`, `victory_v` branch after route history is recorded | Same, exact route `violence` | Same exit audit; other routes cannot satisfy it. |
| `tsuba_betrayal` | Clear Tsubaki Soul through betrayal | `tsubamode_fight`, `victory_b` branch after route history is recorded | Same, exact route `betrayal` | Same exit audit; violence and betrayal are no longer conflated. |

Developer-only fast clears intentionally award their corresponding trophy so the
real presentation, persistence, payout ledger, and toast path can be tested
without completing a full-length combat run. Practice/preview modes remain
non-qualifying where their UI says they do not count.

## Runtime hardening

- `ach_grant()` now always performs its derived cascade, even when the explicit
  trophy was already earned. Previously its early return could skip other state
  completed by the same beat on a replay.
- `ach_earned` and `ach_history` are updated together and saved immediately for
  both explicit and derived awards. This removes the window where a quit/crash
  after an award but before the next achievement interaction could leave the
  soft-reset history ledger stale.
- Monika and Matsuda Id clears now use their Arcade clear flags as recovery
  predicates. Those flags were already persisted at the same victories, so an
  old save cannot hold a cleared cabinet and a permanently missed trophy.
- Chapter 0.5's legacy Music Room migration is one-shot. In developer builds it
  also requires evidence of the legacy `music_on` trophy, so the ALL SIDE CONTENT
  switch cannot impersonate story completion after the migration is considered.
- The after-load reconciliation blocks rollback across its migration boundary,
  following current Ren'Py guidance for callbacks that change data.

## Developer award support

- `ach_dev_grant()` writes both ledgers immediately.
- `ach_dev_grant_all()` unlocks the complete live catalog in catalog order and
  is exposed as **GRANT ALL** in the Achievement Dev Shop.
- `ach_dev_revoke()` removes any queued toast for the revoked id and places the
  id in a session-only retest latch. Derived reconciliation cannot instantly
  re-award it; replaying the exact objective hook clears the latch and proves the
  live trigger. The latch deliberately disappears on restart so developer state
  cannot strand a later player session.
- **CLEAR ALL** remains the softer presentation test: it preserves history, so
  previously earned rows read READY and can be granted one at a time with
  auto-unlock disabled.

## Repeatable validation

Run from the project root:

```powershell
python tools/audit_achievement_coverage.py
```

The checker verifies:

- the exact nine-id catalog and derived predicate for every row;
- ordered state-write/event-grant/result-split placement;
- the Kotonoha simulation's real-clear persistence;
- no literal grant references a retired or unknown id; and
- developer grant, grant-all, and revoke/retest plumbing is present.

Result on 2026-08-30:

```text
Achievement coverage audit passed: 9/9
literal award ids: 9; unknown/retired: 0
developer grant, grant-all, revoke/retest: covered
```

Targeted `git diff --check` also passed. The combined integration pass completed
a clean production MatsuPy compile (0 unreachable items across 122 source files)
and exit-0 lint after the phone, currency-receipt, and prose changes landed.

Reference consulted: [Ren'Py configuration callbacks](https://www.renpy.org/doc/html/config.html#var-config.after_load_callbacks)
and [persistent data](https://www.renpy.org/doc/html/persistent.html).
