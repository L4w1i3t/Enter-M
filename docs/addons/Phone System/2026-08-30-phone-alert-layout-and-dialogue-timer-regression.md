# Phone alert layout and dialogue-timer regression

Date: 2026-08-30

## Reported regressions

- The in-game phone alert compressed its title, detail, icon, and count into a
  248x50 chip. A wrapped title occupied the detail line and made the whole alert
  look piled together.
- Dialogue advanced roughly every half-second with Auto disabled after the
  notification poll was added to the quick menu.

## Root cause

The repeating quick-menu timer called `Function(phone_notification_poll)`.
`phone_notification_poll()` returns `False` on an ordinary poll and `True` when
it announces an unlock. Ren'Py propagates every non-`None` Function result out
of the current interaction, so either boolean could dismiss the active say
statement.

The visual collision was independent: the chip gave its title only 156 pixels
of width and pinned the detail to `ypos 27`. Any title wrap therefore had no
layout space of its own and drew directly over the detail.

## Fix

- `phone_notification_poll_action()` now consumes the poll's internal boolean,
  requests a screen restart only when an alert actually changes the UI, and
  always returns `None`.
- The 0.5-second timer calls that void wrapper with `_update_screens=False`, so
  quiet polling neither ends dialogue nor forces two unnecessary full screen
  updates per second.
- The alert is now a 344x76 panel at `xpos 108`, `yoffset -198`. Its bottom edge
  remains above the quick menu's first row and the dialogue/namebox region.
- The icon, a 220-pixel flowing text `vbox`, and a minimum 28x28 count badge each
  have their own column. Title and detail height can grow together instead of
  colliding at fixed y coordinates.
- Alert copy distinguishes the newly available batch from the total ready
  count: `N new phone conversations` and `Open Phone - N ready total`.

## Regression coverage

`tools/check_phone_notification_contracts.py` protects both contracts. It fails
if the repeating timer again exposes the poll's boolean result, loses its
change-only restart behavior, mismatches the panel and button hitbox, removes
the flowing title/detail layout, or moves the alert into the 1280x720 dialogue
box bounds.

An isolated production-runtime probe then staged three available Asahina
conversations over `bg bedroom`, disabled Auto, and held one real MC say line
for 2.2 seconds. The watchdog observed four executions of the half-second poll,
confirmed both the say and alert screens were still active, and captured the
rendered alert without overlap. The probe source, compiled cache, screenshot,
and isolated save were removed afterward.

## Validation

- Phone notification contract check: pass.
- Screen-reference audit: 290 defined screens, 262 referenced names, none
  missing.
- Random-conversation audit: 12/12 independent entries, with eight texts, two
  calls, and two FaceTimes.
- Runtime hold probe: pass after four polls with Auto disabled; alert visible
  once with three conversations ready.
- Production MatsuPy compile: pass, 0 unreachable items across 122 source
  files.
- Production lint: no warning names the touched phone, quick-menu, or random-
  conversation files. The command continues to report the repository's
  existing missing placeholder/legacy image assets.
- Ruff and scoped `git diff --check`: pass.

The catalog audit also caught and corrected one concurrent wording drift in the
Matsuda review: the explicitly requested `UI can suck my fat ass` punchline is
restored.
