# Phone notification and quick-menu UX revision

Date: 2026-08-30

## Goal

Make random phone conversations discoverable without turning them into generic
toast notifications, and make every displayed count represent the actual number
of conversations the player can start.

## Player-facing behavior

- The in-game quick menu's **Phone** button carries a live numeric badge whenever
  one or more random conversations are available.
- When one or more conversation ids become available, the existing incoming-
  message sound plays once and a small, clickable phone chip appears beside the
  quick menu for 3.25 seconds. The chip opens the Phone directly.
- The chip is not a `renpy.notify` toast and does not cover the center of the
  scene. The quick-menu badge remains after the chip leaves, until the available
  conversations are played.
- Opening the Phone now leads with a plain **Phone** header, an exact
  `N conversations ready` summary, per-contact exact badges, and a short footer
  explaining that a contact row opens history and conversation actions.
- A contact thread repeats the exact total in its header. Its text, call, and
  video controls show their own entry counts; for example, two available texts
  remain visibly `2`, rather than collapsing into one "text type" notification.
- Right-click/Escape closes the contact list and acts as Back from a contact
  thread. The explicit X still exits the Phone.

## State and compatibility

`phone_notification_snapshot` is per-save state containing the exact catalog ids
available on the previous alert poll. Comparing ids rather than only totals means
an unlock is detected even when one entry replaces another and the total stays
the same. The snapshot also prevents the sound from repeating after save/load.

The poll pauses while any Phone screen is open. A conversation that unlocks
behind the handset is therefore announced after the handset closes, unless the
player already consumed it there. Fast-forward defers snapshot changes; when
skipping ends, one cue announces the whole accumulated set instead of
machine-gunning notification sounds.

All counts and ids are obtained dynamically from `phone_random_available()`.
There are no hard-coded conversation ids, channels, contacts, or catalog sizes,
so rebuilding the random-conversation catalog does not require notification UI
changes. Available contacts are also added to the visible contact list as a
compatibility fallback if an older save is missing its historical contact state.

## Audio and art

`audio.phone_notification` reuses
`assets/audio/sfx/phone/messagereceive.ogg` on the dedicated `phone_alert`
channel under the SFX mixer, so it does not cut off a story sound effect. The
phone glyph is drawn with the existing `PhonePanel` toolkit; no new raster asset
was added.

## Files changed

- `game/addons/Phone System/phone_model_construct.rpy`
- `game/addons/Phone System/text.rpy`
- `game/addons/Phone System/random_conversations.rpy`
- `game/screens.rpy`
- `game/story/season1/0525.rpy`
- `tools/audit_phone_random_conversations.py`
- `docs/addons/ADDON_CHEATSHEET.md`
- `docs/assets/audio/SFX_SHOPPING_LIST.md`
- `docs/addons/Phone System/2026-08-30-phone-notification-ux.md`

The final integration also replaced the runtime catalog with the twelve requested
independent conversations. Retired message bodies no longer execute at init;
only their stable ids remain documented for harmless old-save state.

## Validation

- `python tools/check_screens.py`: all referenced screens are defined.
- `git diff --check` on the three runtime files: clean.
- Final catalog integration audit: 12 unique `rc2_*` runtime ids, three entries
  per contact, no `seen`/`unseen` cross-entry dependencies. Each contact has two
  texts plus one call or FaceTime, directly exercising the exact same-kind count
  path this revision fixes.
- `monika_video` is present in the channel tuple, compatibility fallback,
  per-save default, and the 0525 story opening beat.
- MatsuPy compile using the production sibling SDK: pass; the content
  reachability audit reported 0 unreachable items across 122 source files.
- Automated production-runtime QA at 1280x720 used an isolated save and three
  simultaneously available Asahina entries. The alert chip, quick-menu badge,
  Phone header, contact row, and thread header all displayed `3`; the thread
  controls resolved the same total as `2 texts / 1 call`.
- The receive cue loaded and played through `phone_alert` with the dummy audio
  backend. The three rendered screens were visually inspected for clipping,
  overlap, and legibility. The disposable probe source, compiled cache, and
  isolated save data were removed after the pass.
