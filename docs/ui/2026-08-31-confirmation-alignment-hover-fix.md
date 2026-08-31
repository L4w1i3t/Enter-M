# Confirmation Alignment and Hover Fix

Date: 2026-08-31

## Outcome

The room-family confirmation prompt now remains optically centered for both
short and long messages. Yes and No also have independent, visibly different
hover/focus plates rather than sharing the generic selector hover treatment.

## Cause and correction

- The prompt's label container was 600 pixels wide, but its child text retained
  intrinsic width. `text_align 0.5` therefore had no usable line box for short
  messages. The screen now renders the prompt as a 600-pixel text displayable
  with both `xalign 0.5` and `text_align 0.5`.
- Yes and No previously inherited the same generic hover plate, while their
  text changed only from warm paper to near-white. The result was technically
  stateful but visually ambiguous through the modal scrim.
- `selector_yes_hover.png` now brightens the destructive coral family;
  `selector_no_hover.png` brightens the safe teal/burgundy family. Each button
  explicitly names its text style and carries a matching hover outline.
- No retains `default_focus True`. Ren'Py intentionally uses hover styling for
  keyboard focus, so the safe choice is visibly highlighted when the panel
  opens.

The shared palette and selector definitions use init priority `-100`. This
keeps Data Bank and Credits top-level color tables valid regardless of the
theme file's filename or filesystem load order.

## Validation

- `python -B tools/check_screens.py`: all 293 screens and 263 referenced names
  resolve.
- Embedded-Python MatsuPy compile: pass, with 0 unreachable items across 124
  source files.
- Both new hover sources are 112x56 RGBA PNGs.
- Live GL2 captures at 1280x720 confirm the short prompt is centered and each
  focus state is visibly distinct:
  - `docs/ui/evidence/2026-08-31-confirm-yes-hover-live-gl2.png`
  - `docs/ui/evidence/2026-08-31-confirm-no-hover-live-gl2.png`

The capture driver moves Ren'Py's ordered focus between No and Yes because the
engine deliberately unifies pointer-hover and keyboard-focus presentation.
