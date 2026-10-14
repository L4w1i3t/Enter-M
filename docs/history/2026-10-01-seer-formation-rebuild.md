# Ontological Seer formation rebuild: October 1, 2026

The party picker for both Seer fights (Normal and Id Mode) was rebuilt around
how it is used. Monika's archetype was also corrected for scale, both on this
screen and in battle. Battle rules and balance are unchanged. One picker
helper had a default-row bug, which is now fixed (see below).

Pre-pass snapshot (the screen, the stage files, every pixel sprite and the
builder; SHA-256 manifest): `C:\Users\Admin\ENTER-M-backups\20261001-formation-before\`.

## What was wrong

The user's report, each item confirmed in a capture before the rebuild:

- **Keyboard.** UP/DOWN walked a focus ring of the roster, then each chosen
  member, then READY. Reaching BEGIN took one press per party member plus one.
- **Mouse.** There were no hover states, and hovering inspected nothing.
- **Buttons** were flat `Solid` rectangles.
- **Tofu.** The Id Mode title was `FORMATION · ID MODE` in Myanmar.otf, which
  has no U+00B7.
- **Collisions.** "ID MODE" ran under the roster cards. The member cursor sat
  on the FRONT label. The formation preview's sprites covered the dossier's
  SPD value.
- **Monika's portrait** was drawn at 78% of everyone else's and stood on the
  floor (details below).

## The layout

| Region | What is there |
|---|---|
| Left | The official design, at one shared scale (below). The Seer's `seal.png` and `orbit_current.png` counter-rotate behind it, tinted to the fighter's accent. The class name runs down the edge as a vertical watermark. Browsing replays a slide-in with an accent-coloured afterimage. |
| Top left | Kicker, the FORMATION title, and a one-line instruction. Id Mode adds a crimson ID MODE stamp; the tofu is gone. |
| Top | The ROSTER: seven slanted cards with head shots, names and classes. Locked cards (party full) desaturate. Party members carry an order badge in their row colour. |
| Centre | The DOSSIER: stats, affinity chips, skills with MP costs, party status, and an ADD / REMOVE button. |
| Right | The FORMATION DECK: the battle sprites standing in their rows, on floor lanes with EO-style rings. Each formation is centred in the deck box and slides when it changes. An empty row shows a dashed lane and a ghost ring. FRONT has chevrons running toward her. |
| Bottom | The PARTY strip in turn order: number, head shot, name, and a row chip that flips when changed. Below it, a context help strip and BEGIN, which glows and glints when ready and states what is missing when it is not. |
| Bottom left | BATTLE ART: PIXEL / ILLUSTRATED (also TAB). |

All plates use one new shader, `msbf.formation_plate`. It is `msbf.plate`
plus a cursor glow, a sheen sweep, hatching, a dashed outline and a vertical
fade. The floor rings use `msbf.formation_ring`, which keeps a 1.5-pixel line
all the way round a squashed ellipse.

## Controls: three rows, one cursor

ROSTER, PARTY and BEGIN are three horizontal rows, so the keys mean the same
thing in each:

| Input | Action |
|---|---|
| LEFT / RIGHT | Move along the row. Held, they scroll the roster. |
| UP / DOWN | Change row. BEGIN is at most two presses away. |
| Z / ENTER | Roster: add or remove. Party: swap row. BEGIN: begin. |
| X / SHIFT | Remove. |
| SPACE | Begin from anywhere, once the party is ready. |
| TAB | Switch battle art. |

Picking the fourth fighter moves the cursor onto BEGIN.

The mouse drives the same cursor. Hovering a card, plate, sprite or BEGIN moves
the cursor there, so hovering a card is how you inspect someone. Click acts.
Right-click removes; on empty space it opens the pause menu. The help strip
follows whichever device was touched last.

Every handler reads and writes the live screen scope through `renpy.get_screen`.
The keys are bound last, so they always act on the cursor and never on a button
that happens to be under a resting pointer.

**Right-click needed its own binding.** `definitions.rpy` removes `mouseup_3`
from `game_menu`, as DDLC did: right-click hides the windows. The old screen's
right-click therefore never opened its pause menu. The new screen binds
`mouseup_3` explicitly, as Asarhythm, Tsubaki, Kotonoha, the Arcade and the
Invasions already do.

## Monika's scale

All seven archetypes were painted at one scale: eye line to chin measures 57–65
source px on every one. Their canvases differ, though. Monika's is landscape
(1375×1144) because she is mid-leap.

**On this screen,** the old `fit="contain"` fitted each canvas to the panel,
which shrank her. Now every source draws at `MSBF_FM_HERO_K` (0.42) with its
head centre on `MSBF_FM_HERO_HEAD_Y`. Faces are one size and the eyes do not
jump as you browse. She floats, because she is airborne. The roster and party
head shots use the same rule: one source-pixel window for everybody, instead of
a cover-fit crop.

**In battle,** `tools/build_seer_pixel_sprites.py` normalises each sprite by its
head-to-feet span. Her mid-leap span is short, so the standing target of 78
scaled her by 0.0865, against roughly 0.066 for the others. Her face came out
about 35% larger than the cast mean.

Her span is now **58**, chosen by face size (her eye-to-chin is now about 4.2
art px; the cast mean is 4.15). The rebuild is seeded and deterministic. Only
`pixel/party/monika.png`, `pixel/hq/party/monika.png` and her `sprites.json`
entry changed, verified by hash against the snapshot.

Measured but left alone, as an open option: Tsubaki's face is about 16% above
the cast mean in battle, and Himeko's about 15% below.

## The default-row bug

`msbf_select_member` (in `battle_logic.rpy`) assigns a newcomer to the front
if fewer than two members stand there. It counted *after* appending the
newcomer. `msbf_front_count` reads a member with no row yet as front, so only
the first pick ever went front. The user's pre-pass screenshot shows this
("FRONT 1": Seeker in front, everyone else rear). The count now happens
first, so the first two picks stand front, matching `msbf_default_rows`. The
only caller is the picker.

## Files

| File | Change |
|---|---|
| `party_select.rpy` | Rewritten: shaders, layout and input handlers. |
| `battle_logic.rpy` | `msbf_select_member` counts the front row before appending. |
| `tools/build_seer_pixel_sprites.py` | Monika's span is 58, with the reason in a comment. |
| `pixel/` | Monika's pixel sprite, her illustrated twin, and `sprites.json`. |
| `tools/run_msbf_look_probe.py` + `tools/probes/msbf_look_capture.rpy` | New formation targets, `--size`, and real-input steps with pass/fail checks. |

## Checks that ran

- **Lint:** clean, using the isolated recipe with its own TEMP and a
  throwaway savedir.
- **Captures:** the look probe covers 12 formation states (empty, two picks,
  ready, party cursor, full, mouse hints, four front, one front and three
  rear, no front, Id Mode, launch, illustrated), plus battle captures with
  Monika in the party in both art modes and seven-member phase 3. The kept set
  is `tmp/msbf_look_probe/formation_final/`; the pre-pass set is
  `formation_before/`.
- **Input:** 52 of 52 checks pass. `input_keys` posts real key events and
  `input_mouse` drives Ren'Py's test mouse; each `expect` step asserts the
  screen's live state.

**Two probe gotchas** turned up while testing:

- **A bare `MOUSEMOTION` posted before a pause never hovers anything.** Every
  interaction starts by draining queued motion (`core.py`, "Accumulate
  relative mouse movement from otherwise obsolete events"). Clicks survive,
  because button events are not drained. The probe now posts motion from
  inside the pause through a screen timer with `_update_screens=False`.
- **A float position is a fraction of the screen.** One `xcenter` had picked
  up the lane slant, a float. It must be `int()`.

## Not covered

- Real-hardware play with a physical mouse. The test mouse goes through
  Ren'Py's own focus path, but nobody has used the screen by hand yet.
- Frame cost was not profiled. The screen draws about 30 small mesh plates and
  11 `AlphaMask` windows over the same stage the old screen drew.
- Gamepad input has no bindings beyond what Ren'Py maps by default.

## October 2: the navigation stutter

The user reported a freeze or stutter on every cursor move, in every row.
It was measured with `tools/probes/fm_perf_hook.rpy`, a look-probe `--extra`
that times screen executions, `render_screen`, the GL draw and image-cache
loads, profiles chosen windows, and counts `take_state` calls by source line.

**Cause.** There were zero image loads. Every input re-executed the screen
(about 37 ms) and re-rendered it (about 26 ms), so the worst frame gap was
75–83 ms. Two engine facts combine to make that happen:

- **Reuse needs equal arguments.** Screen language reuses a node only when its
  arguments compare equal to the previous execution's, and a Transform
  (including ATL) is equal only to itself. Every `at some_atl(args)` built a
  new transform on every execution. So did any helper that returned a new
  displayable, such as `Solid(..., xysize=...)` or the plate and window
  factories. About 370 transforms were rebuilt per keypress.
- **Each rebuild copies every transform property.** That is about 490
  properties in this project: 374 distinct shader uniforms across all files,
  each registered as a transform property, plus Ren'Py's own. The copying
  happens in `take_state`, and `diff` scans the same set on a new ATL's first
  frame.

**Fix.** `msbf_t(atl, *args)` and `msbf_memo(factory, *args)` (in
`seer_battle.rpy`) return the same object for the same arguments. A
re-execution now rebuilds only what actually changed, and a transform whose
arguments did change still restarts exactly as before. `msbf_blank(w, h)` is
the reusable transparent base for shader plates.

The formation screen routes every animated transform and factory through
these helpers. Pieces that change with the cursor but do not need to animate
between states became ready-made memoized displayables: card portrait looks,
the positioned hero art and afterimage, and static `msbf.bar` stat bars.

The shared screens it uses got `msbf_t` too: `msbf_hud_scrim`,
`msbf_boss_aura`, `msbf_energy_bar` and `msbf_seer_environment`. The battle
HUD uses all four. Behaviour is unchanged, and fewer transforms are rebuilt
in the fight as well.

**After.** Measured in the probe at 1280×720:

| | Before | After |
|---|---|---|
| Screen execution per input | about 37 ms | about 9 ms |
| Render on the input frame | about 26 ms | about 15 ms |
| Worst frame gap per input | 75–83 ms | about 21 ms mean, 25.5 ms max |
| Idle frames | unchanged | unchanged (render about 4 ms) |
| Transforms rebuilt on an unchanged re-execution | — | 4 |

Input checks: 52 of 52 pass. Lint is clean.

What remains per browse is genuine change: the portrait, afterimage,
watermark, dossier text, accent-tinted seal and plates, affinity chips and
two cards. Each rebuild still costs about four times what it would in a plain
Ren'Py game, because of the property count.

**Not covered.** The fight's own `msbf_battle_screen` was not measured or
changed beyond the shared screens. It likely builds `at atl(args)` the same
way.

## October 2: battle input audit

The user reported that battle input "sometimes feels hitchy… not as
egregious". It was measured with the same instrument, through new probe steps
for battle targets (`key`, `call`, mouse). Pre-pass copies of every file
touched are in `C:\Users\Admin\ENTER-M-backups\20261002-battle-perf-before\`.

### Findings

1. **The same rebuild problem as the formation screen, in milder form.** One
   execution of `msbf_battle_screen` took 7–9 ms. A re-execution with nothing
   changed rebuilt 53 transforms, and each navigation key rebuilt 107.
   Re-executions happen on every input, on every timer, and twice per ambient
   wave in phases 2–3 (the repeating `ambient_wave` timer). The sources:
   - `msbf_press_turn_luster(slot * 0.07)`, once per turn icon;
   - the mug's `phone_round(...)` and `ArchivePortraitCrop(...)`;
   - `msbf_ticker_pop`;
   - the arena background's inline `at transform:` blocks;
   - inline `msbf_plate(...)` calls everywhere;
   - camera-punch, banner, float, bar-chip and cast-projectile transforms;
   - every cinematic and overlay `use`d by the battle screen (phase break,
     nova, defeat, reveal, turnover sweep, KO bursts).
2. **Big images decoded mid-fight, on the frame they were needed.** Each
   decode took 26–30 ms inside a 55–70 ms frame:
   - each archetype PNG the first time its owner's command window opened;
   - `arena_gold.webp` and `arena_rupture.webp` on the frame a bar breaks;
   - `idmode/idphase.png` mid-reveal.

   The formation screen already loads the archetypes and the seal in real
   play. The phase plates and illustrations were never loaded before their
   phase.
3. **Ruled out:**
   - GC: five gen-0 collections of about 1 ms in 17 s.
   - Audio: every SFX load runs on Ren'Py's audio thread. The main-thread
     audio time in cProfile was misattribution, confirmed by wrapping
     `renpy.audio.audio.load`.

### Fixes

- **Battle-flow screens.** Every `at transform(args)` in `seer_battle.rpy`,
  `ui.rpy`, `arena.rpy`, `cinematics.rpy`, `fx.rpy` and
  `seer_presentation.rpy` now goes through `msbf_t`: 145 call sites. The
  change was a scripted, dry-run-reviewed wrap, line by line, preserving each
  file's own line endings.
- **`msbf_plate` itself is memoized.** Every caller is a screen `add` or
  `background`, so the shared object is never mutated.
- **`msbf_t` / `msbf_memo` fall back** to a plain call when arguments are
  unhashable.
- **The mug and camera punch are memoized.** The two inline floor-seal blocks
  became `msbf_seer_floor_squash`.
- **`msbf_px_warm_fight_art()` in `pixel_stage.rpy`** decodes every large
  image the fight can draw on a daemon thread, the way Ren'Py's preload thread
  does (`cache.get(predict=True, texture=True)`; the GPU upload is finished by
  the main thread). It runs when a pixel stage is first built: the formation
  preview, then the battle intro. Two alternatives do not work on 8.6:
  `renpy.cache_pin` is a no-op, and preloads queued from a label are cleared
  by the next interaction's cache tick.
- **Tried and reverted:** staggering the command window by one frame. The
  strike's own effects, not the window, were the cost, and the window's
  entrance then replayed on every hand-off, which was a visible change.

### After

Measured in the probe at 1280×720:

| | Before | After |
|---|---|---|
| Battle-screen execution | 7–9 ms | 3–4 ms |
| Transforms rebuilt by an unchanged re-execution | 53 | 0 |
| Transforms rebuilt per navigation key | 107 | 3 |
| Navigation, worst frame per input (phase 1 / phase 3) | 17–20 / 21–38 ms | 11–14 / 14–16 ms |
| Phase-2 idle with the ambient wave | 15 ms max | 12 ms max |
| Mid-fight image decodes | several | none |

In a six-action flow, the median frame is 5.5 ms and the 99th percentile is
11.7 ms. One frame per strike still runs 20–28 ms. That strike frame is about
35 ATL transforms that legitimately start at once (camera punch, arena shock,
banner, float numbers, bar chips, flash, HP bar). Each pays two full property
scans on its first frame. Reducing it means fewer strike effects, or fewer
shader uniforms project-wide.

Input checks: 52 of 52 pass. Lint is clean. The battle regression captures
are in `tmp/msbf_look_probe/battle_after/`. Against the facelift's final set,
only frames with animation timing in them differ.
