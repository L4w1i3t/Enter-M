# Deferred Matsucoin Payout Receipts and Developer Audit — 2026-08-30

## Goal

Keep Matsucoin accounting immediate and reliable without letting a currency
toast intrude on story scenes. Present one summary receipt the next time the
player reaches the main menu, including after returning normally or quitting
and relaunching.

## Runtime contract

- `mc_award()` and `mc_sync()` still credit `mc_balance`, `mc_lifetime`, and the
  one-time `mc_paid_keys` ledger immediately.
- A payout that requests notification adds only its credited amount and event
  count to `persistent.mc_pending_notice_amount` and
  `persistent.mc_pending_notice_events`.
- No Matsucoin receipt renders while `main_menu` is false. Arcade result cards
  and gacha refund readouts remain their own inline feedback and do not create a
  duplicate toast.
- A guarded `config.label_callbacks` hook watches for `before_main_menu`, which
  Ren'Py runs on first title entry and every return from gameplay. It reconciles
  achievements first, settles Matsucoin-derived rewards, and stages exactly one
  summary receipt.
- Pending counters are acknowledged only after the toast finishes. If the game
  closes during delivery or the player leaves the title quickly, the same
  persisted amount is reconstructed on the next title visit.
- A receipt subtracts only the amount/event count it represented. Any payout
  earned while that receipt is animating remains pending for the following
  main-menu entry.

## Developer controls audited

- The Dev Hub mount remains guarded by `config.developer` and
  `renpy.has_screen("dev_hub_mount")`; the entire Dev Hub folder remains excluded
  from release builds.
- Every literal `dev_hub_call` target and `dev_hub_show` screen resolves.
- ALL SIDE CONTENT reads the live Archive, Character Stories, CG, outfit,
  soundtrack, and roster catalogs; enable, partial-repair, and disable paths all
  persist, notify, and restart the interaction.
- Achievement manual grant/revoke, auto-unlock toggle, sync, and clear helpers
  are present and reachable from the Dev Hub. `mc_main_menu_enter()` calls
  `ach_sync()` first when installed, closing the cold-relaunch gap where an
  objective was saved before its achievement was reconciled.
- Matsucoin give/fill/reset, grant/clear cards, and payout-ledger reset targets
  all resolve. `mc_dev_reset()` now also clears persistent and staged payout
  receipts, preventing a stale pre-reset notification from appearing later.

## Targeted validation

Run from the project root:

```powershell
python -B tools/test_matsucoin_deferred_receipts.py
python -B tools/test_dev_unlock_all.py
python -B tools/check_dev_hub_contracts.py
python -B tools/check_screens.py
```

Validated in this pass:

- immediate credit plus one-time ledger idempotence;
- gameplay suppression and title-only staging;
- interrupted/relaunch delivery;
- achievement-before-Matsucoin cold-title ordering;
- aggregate derived receipts and exact wallet-cap behavior;
- developer reset cleanup;
- full side-content enable/partial/disable behavior;
- Dev Hub function/screen wiring and release exclusion;
- all project screen references resolving.

The coordinating integration pass completed a clean production MatsuPy compile
(0 unreachable items across 122 source files) and exit-0 lint. The behavioral
receipt harness covers normal title entry, interrupted delivery, and relaunch
reconstruction without touching the player's real persistent data.
