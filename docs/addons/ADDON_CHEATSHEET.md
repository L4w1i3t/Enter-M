# Story-facing addon calls

Checked September 25, 2026 against the declarations named below. Use the live
signature when adding arguments. Story state belongs to the active save;
Archive unlocks may be persistent across saves.

## Calendar

Source: `game/addons/Calendar System/calendar_system.rpy`.

```renpy
$ calendar.set_date(2025, 5, 15)
$ show_calendar()
call calendar_advance(days=1, animate=True)
$ hide_calendar()
```

`calendar.get_snapshot()` returns the display-ready fields used by other
systems. Browsing `calendar_menu` is separate from advancing the story date.

## Messages and calls

Source: `game/addons/Phone System/text.rpy` and `call.rpy`.

```renpy
$ phone_mark_contact_met("monika")
call phone_text_conversation("Monika", [phone_msg("them", "See you tomorrow."), phone_msg("me", "See you.")], append=True)
call phone_call_conversation("Monika", [phone_call_line("them", "Hello?")])
```

`phone_text_conversation` defaults to `append=False`; request append explicitly
when extending the saved thread. Text status, timestamp, and clock text are
optional. `phone_call(contact_name, ..., can_decline=True)` is the incoming-call
interaction; conversation playback is a separate label. Optional phone content
also obeys the Phone System's main-story and save-scope gates.

## People and outfits

Source: `game/addons/Roster View/roster_view.rpy`.

`mark_character_met(character_id, thought=None)` and
`update_character_thought(character_id, thought)` maintain current-save People
entries and also mark the character met in the persistent Archive.
`roster_mark_met(character_id)` and `outfit_unlock(*keys)` handle Archive discovery. Read the implementation before substituting one API for
another: their persistence scopes differ.

## ID card

Source: `game/addons/ID Card Name and Info/card.rpy`.

The card validates name and birth fields through `validate_id_card_info` before
`commit_id_card_info`. Follow the existing story's card-screen flow so invalid
fields are handled by the UI; do not bypass validation with direct persistent
assignments.

## Arcade

`arcade_launch(label_name, **launch_kwargs)` in `game/arcade_context.rpy` starts
the requested cabinet in a child context. The launch label queues the doorway
and owns temporary menu flags before calling the game label.
