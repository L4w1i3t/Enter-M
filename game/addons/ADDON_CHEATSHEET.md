# Addon Cheat Sheet

Scope: addon systems currently used by `game/story/s1pro.rpy`.

## Common Story Flow

Use this when introducing a new notable character:

```renpy
$ mark_character_met("matsuda")
$ phone_mark_contact_met("matsuda")
$ update_character_thought("matsuda", "New thought text.")
```

Use `mark_character_met` for the People screen. Use `phone_mark_contact_met` only when the character should appear in the phone contacts.

The phone uses the current Calendar date when a text thread has no explicit timestamp, so set or advance the calendar before text scenes.

## Calendar System

Source: `game/addons/Calendar System/calendar_system.rpy`

Purpose: tracks the in-game date, shows the date overlay, provides the Calendar menu, and supplies date labels to phone threads.

### Set The Initial Date

```renpy
$ calendar.set_date(2025, 5, 15)
```

Equivalent label form:

```renpy
call calendar_set_date(2025, 5, 15)
```

Use direct `$ calendar.set_date(...)` in story setup. Use the label form only if you specifically want a callable script helper.

### Show And Hide The Overlay

```renpy
$ show_calendar()
$ hide_calendar()
```

Current story pattern:

```renpy
scene bg club_day
$ show_calendar()
with dissolve_scene_full

$ hide_calendar()
scene black with wipeleft_scene
```

`show_calendar()` enables the calendar display and shows `calendar_overlay`.

`hide_calendar()` hides the overlay screen. It does not change the stored date.

### Advance Time

Animated date-change panel:

```renpy
call calendar_advance(days=1)
```

Silent advance:

```renpy
call calendar_advance(days=1, animate=False)
```

Direct Python advance, also silent:

```renpy
$ calendar.advance_day(1)
```

Prefer `call calendar_advance(days=1)` for day breaks in the main story because it keeps the transition consistent.

### Read Date Data

```renpy
$ full_date = calendar.get_formatted_date("full")
$ persona_date = calendar.get_formatted_date("persona")
$ is_weekend = calendar.is_weekend()
$ day = calendar.get_day()
$ month = calendar.get_month()
$ year = calendar.get_year()
```

Formats:

```renpy
$ calendar.get_formatted_date("full")     # Thursday, May 15
$ calendar.get_formatted_date("short")    # THU 5/15
$ calendar.get_formatted_date("numeric")  # 05/15/2025
$ calendar.get_formatted_date("persona")  # 5/15 (THU)
```

### Calendar Menu

The game menu navigation already has:

```renpy
textbutton _("Calendar") action ShowMenu("calendar_menu")
```

Usually you do not call `calendar_menu` from story script.

## Nier Text Adventure

Source: `game/addons/Nier Forest Text Adventure Format/nier_text_adventure.rpy`

Purpose: black-background NVL prose sections where text accumulates on screen.

### Basic Block

```renpy
call nier_enter
call nier_section("NOTICE")
nier "First prose line."
nier "Second prose line."
call nier_clear
nier "New page of prose."
call nier_exit
```

### Choices

```renpy
menu (screen="nier_nvl_choice"):
    "Proceed":
        pass
    "Do not proceed":
        nier "...Then I cannot allow you to partake in this story."
        $ renpy.quit()
```

### What Each Helper Does

```renpy
call nier_enter
```

Sets `nier_ta_active = True`, disables `quick_menu`, fades to black, and enters the mode.

```renpy
call nier_section("TITLE")
```

Clears accumulated NVL text, shows a centered title card, then returns to black.

```renpy
call nier_clear
```

Runs `nvl clear` without leaving Nier mode.

```renpy
call nier_exit
```

Clears NVL text, sets `nier_ta_active = False`, restores `quick_menu`, and returns to black.

### Gotchas

Always exit with `call nier_exit` before returning to normal ADV scenes.

Use `nier "..."` for prose while in the mode. Normal ADV dialogue will not use the Nier NVL screen.

## ID Card Entry

Source: `game/addons/ID Card Name and Info/card.rpy`

Purpose: gets the player name and birthday from an in-world ID card UI.

### Story Usage

```renpy
scene bg ether with wipeleft_scene
call screen id_card_info_entry
scene bg club_day
```

The screen handles validation, persistence, and input state internally.

### Saved Values

On valid issue, the screen updates:

```renpy
$ player
$ persistent.playername
$ persistent.player_birthday      # MM/DD
$ persistent.player_birth_month   # MM
$ persistent.player_birth_day     # DD
```

### Validation Rules

The screen rejects:

- Empty names.
- Names shorter than 3 characters.
- Names longer than 24 characters.
- Names made only from separators, such as spaces, hyphens, or apostrophes.
- Unsupported name characters outside letters, spaces, hyphens, and apostrophes.
- Unoriginal names like `mc`, `player`, and `protagonist`.
- Reserved character names and blocked terms in `illegal_names`, including spacing, separator, case, basic leetspeak, and Unicode normalization bypasses.
- Invalid or non-numeric birthdays.

### Direct Commit Helper

Normally use the screen. For debug scripts only:

```renpy
$ commit_id_card_info("Alex", "05", "15")
```

This validates and saves the same values as the screen.

### Gotchas

`id_card_info_entry` disables `quick_menu` while open and restores it on hide.

`id_card_photo_for_name()` has special-case photo routing for blocked template names. If that route is used without its asset present, Ren'Py will error on the missing image.

## Phone System

Sources:

- `game/addons/Phone System/phone_model_construct.rpy`
- `game/addons/Phone System/text.rpy`
- `game/addons/Phone System/call.rpy`
- `game/addons/Phone System/facetime.rpy`

Purpose: in-story phone UI, contacts list, message threads, phone calls, and video calls.

### Message Types

```renpy
phone_msg("them", "Incoming text.")
phone_msg("me", "Player reply.")
phone_thumb("them")
phone_thumb("me")
phone_note("System note.")
```

Optional message time:

```renpy
phone_msg("them", "See you soon.", time="8:14 PM")
```

Sender values currently used by the UI:

- `"them"`: left-side received bubble.
- `"me"`: right-side sent bubble.
- `"system"`: centered note/date text.

### Incremental Text Conversation

Use this for normal story texting. Each call contains only the new message or messages.

```renpy
python:
    _phone_messages = [
        phone_msg("them", "Don't forget tomorrow morning."),
    ]
call phone_text_conversation("Monika", _phone_messages, append=True)

python:
    _phone_messages = [
        phone_msg("me", "Roger wilco."),
    ]
call phone_text_conversation("Monika", _phone_messages, append=True)
```

`append=True` extends the existing saved thread, keeps the old messages visible, and animates only the new messages.

### Full Thread Replacement

Use this only when intentionally replacing the thread with a full message list.

```renpy
python:
    _phone_messages = [
        phone_msg("them", "First."),
        phone_msg("me", "Second."),
    ]
call phone_text_conversation("Monika", _phone_messages)
```

No `append=True` means `messages` is treated as the complete thread for that contact.

### Group New Messages In One Reveal

```renpy
python:
    _phone_messages = [
        phone_msg("them", "First new message."),
        phone_msg("them", "Second new message."),
    ]
call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True)
```

Both new messages are appended and animated in order.

### Timestamps And Phone Clock

```renpy
call phone_text_conversation(
    "Monika",
    _phone_messages,
    timestamp="Sun, May 18",
    clock_text="08:12",
    append=True
)
```

If `timestamp` is omitted, the system uses the current calendar date label.

`timestamp` is used for the thread/date label. `clock_text` is used in the phone status bar.

### Contacts

Known contact IDs and aliases:

```text
monika
mom / himeko
asahina / asa
matsuda / matsuda akai
```

Unlock an existing contact:

```renpy
$ phone_mark_contact_met("monika")
```

Create and unlock a custom contact:

```renpy
$ phone_mark_contact_met("new_person", contact_name="New Person", subtitle="Classmate")
```

Text conversations also call the storage path that marks the contact as met, but explicit `phone_mark_contact_met` is useful when the player gets the contact before any messages exist.

### Phone Contacts Screen

The quick menu already has:

```renpy
textbutton _("Phone") action Show("phone_contacts_screen")
```

Direct story/script usage:

```renpy
show screen phone_contacts_screen
```

Usually use the quick menu or `Show("phone_contacts_screen")`, not a story `call screen`, unless you need to block script flow.

### Phone Call

Not used in `s1pro.rpy` yet, but available in the same system:

```renpy
call phone_call("Mom", status="Calling...", clock_text="21:12")

if _return == "answer":
    mom "Hello?"
elif _return == "decline":
    "I let it ring out."
```

Possible returns:

```text
answer
decline
dismiss
```

### Video Call

Not used in `s1pro.rpy` yet, but available:

```renpy
call phone_video_call("Monika", status="Video Call", clock_text="21:12")
```

Alias:

```renpy
call phone_facetime("Monika")
```

Possible returns:

```text
end
dismiss
```

### Phone Gotchas

`phone_text_conversation`, `phone_call`, and `phone_video_call` all hide the dialogue window.

If normal ADV dialogue follows immediately, restore window auto mode:

```renpy
window auto
```

Do not rebuild the whole text thread for each new message. Use `append=True` and pass only the new messages.

## Roster And Character Thoughts

Source: `game/addons/Roster View/roster_view.rpy`

Purpose: full character roster plus the quick-menu People screen (`character_thoughts_screen`).

### Unlock A Character In People

```renpy
$ mark_character_met("monika")
```

This uses the default thought from `character_thought_catalog`.

### Unlock With A Custom Thought

```renpy
$ mark_character_met("matsuda", "Matsuda crashed into the evening.")
```

### Update A Thought Later

```renpy
$ update_character_thought("matsuda", "Matsuda crashed into the evening, took my contact info, and somehow made the whole thing feel premeditated by fate.")
```

`update_character_thought` also marks the character as met if needed.

### Current Thought IDs

```text
monika
mom
asahina
sam
kotonoha
matsuda
tsubaki
```

If you pass an ID that is not in `character_thought_catalog`, it will be stored in `met_character_ids` but will not appear in the People screen.

### People Screen

The quick menu already has:

```renpy
textbutton _("People") action Show("character_thoughts_screen")
```

Direct usage:

```renpy
show screen character_thoughts_screen
```

### Full Roster Screen

The full profile roster is available as:

```renpy
call roster_view
```

or:

```renpy
show screen roster_view_screen
```

Story script usually only needs the People thought helpers. The full roster is better suited for archive/menu access.

### Adding A New Character To People

Add an entry to `character_thought_catalog`:

```python
{
    "id": "new_person",
    "name": "New Person",
    "subtitle": "Classmate",
    "sprite_image": "new_person neut",
    "fit_mode": "contain",
    "thought": "Initial read goes here.",
}
```

Then unlock in story:

```renpy
$ mark_character_met("new_person")
```

### Adding A New Full Roster Profile

Add a `CharacterProfile(...)` to `init_roster()`:

```python
CharacterProfile(
    "New Person",
    "New Person Fullname",
    "new_person neut",
    18,
    65,
    125,
    34,
    "Likes",
    "Dislikes",
    "Bio text.",
    "contain",
    None,
    False,
)
```

Use `manual_exception` to replace the chest field with a build descriptor:

```python
manual_exception="Athletic"
```

Use `grayed_out=True` to render the sprite in grayscale and show status as dead.

## Cross-System Recipes

### New Day, New Scene

```renpy
$ hide_calendar()
scene black with dissolve_scene_full
call calendar_advance(days=1)

scene bg living_room
$ show_calendar()
with dissolve_scene_full
```

### Meet A Non-Phone Character

```renpy
$ mark_character_met("kotonoha")
$ update_character_thought("kotonoha", "She makes ordinary transactions feel rehearsed.")
```

### Meet A Phone Contact And Text Them Later

```renpy
$ mark_character_met("matsuda")
$ phone_mark_contact_met("matsuda")

python:
    _phone_messages = [
        phone_msg("them", "For the record, I survived."),
    ]
call phone_text_conversation("Matsuda Akai", _phone_messages, status="New Contact", append=True)
```

### Nier Narration Into Normal Story

```renpy
call nier_enter
nier "A prose passage."
call nier_clear
nier "Another prose passage."
call nier_exit

scene bg bedroom
$ show_calendar()
with dissolve_scene_full
window auto
```

## Maintenance Notes

When adding a recurring character, check both catalogs:

- Phone contact: `PHONE_CONTACT_CATALOG`, `PHONE_CONTACT_ALIASES`, and `PHONE_CONTACT_ORDER`.
- People screen: `character_thought_catalog`.
- Full roster: `character_roster` inside `init_roster()`.

When adding a text scene, default to `append=True`.

When adding a day break, default to `call calendar_advance(days=1)`.

When leaving modal systems that hide UI, restore with `window auto` if ADV dialogue follows immediately.
