# Ontological Seer facelift — September 30, 2026

A full presentation rebuild of Matsuda's boss fight (Normal and Id Mode), its
two entrances, its phase reveals and its party select. Battle rules, balance,
timers and saves are unchanged. The one battle-logic addition is a
presentation feed: the action banner.

Pre-facelift snapshot (100 files, SHA-256 manifest):
`C:\Users\Admin\ENTER-M-backups\20260930-seer-facelift-before\`.

## The brief

Final Fantasy × Shin Megami Tensei × Etrian Odyssey, with a sense of scale on
Matsuda's side. The party select shows each fighter's illustrated archetype as
their official design. In battle, everyone is pixel art, Matsuda at a grander
scale than the party. The forms are Nahobino (phase 1), Tohu Imago (phase 2)
and Imago Rupta (phase 3, where the genre itself ruptures).

## Layout

The party stands on the LEFT and faces right; Matsuda stands on the RIGHT.
The user asked for this swap mid-pass.

| Region | What is there |
|---|---|
| World, left | The party as 2× pixel sprites in two EO ranks. FRONT stands nearer her and REAR a long step back. Each column zig-zags, and the stagger widens as the column gets crowded. |
| World, right | Matsuda as a 3× pixel sprite. Forms 2 and 3 are taller than the frame: the crown and halo run off the top. |
| Top left | SMT-sized press turns, the round, and the LOG / CONTROLS chips. |
| Top right | Her form kicker, her name in serif caps, a slanted HP bar and her affinities. |
| Top centre | An FF-style action banner (who did what). Otherwise the latest log line as a ticker. |
| Bottom left | An FF party status list. The acting row steps toward her. |
| Bottom right | The command window, on your turn only. It shows the acting member's official portrait, a 2×4 command list with element pips and the FF pointing-glove cursor. A help strip sits above it. |

Every plate is one shader, `msbf.plate` (seer_battle.rpy): a slanted
parallelogram with a gradient, a lit edge and an accent rail.

## Files

| File | Role |
|---|---|
| `pixel_stage.rpy` (new) | `msbf.px` (the actor shader) and `msbf.pxfx` (pixel FX), the formation and boss placement, the presentation bus, and `MSBFPixelStage`: animation, choreography, entrances and frame playback. |
| `seer_battle.rpy` (new) | `msbf.plate` and the HUD pieces. `msbf_battle_screen` moved here from ui.rpy. |
| `party_select.rpy` (rewritten) | The FORMATION picker. The revolver cylinder is in the snapshot. |
| `cinematics.rpy` | The new entrances, the shared SMT name card (`msbf_px_name_card`), and phase reveals that no longer draw the illustration. |
| `arena.rpy` | `msbf_stage_anchor` / `msbf_boss_anchor` / `MSBF_BOSS_STAGE` now read the pixel sprites. The handover sweep is horizontal. |
| `ui.rpy` | The old battle screen was removed and replaced by a pointer. `msbf_fx_layer` is cut down to the screen flash and the call-out words. |
| `fx.rpy` | `msbf_turn_banner` is restyled to the plate language. |
| `battle_logic.rpy` | `_raise_banner` and `action_banner` / `action_banner_serial` (presentation only). |
| `pixel/` (new) | The derived sprites, the UI pixel bits (glove, down cursor, diamond) and `sprites.json`. |
| `tools/build_seer_pixel_sprites.py` | Builds `pixel/` from the illustrated art. |
| `tools/import_seer_sprite_sheets.py` | Imports hand-made or generated frame strips (see the sprite brief). |
| `tools/run_msbf_look_probe.py` + `tools/probes/msbf_look_capture.rpy` | Screenshot harness with scripted steps: cue, use, enemy, kill, break, handover, micro. |

Nothing was deleted from the art. `msbf_matsuda_phase1..3` and
`msbf_arch_<id>` are still defined, and the gacha cards still read the
original files.

## The pixel sprites (and what they are not)

The shipped battle sprites are DERIVED from the existing illustrations.
`build_seer_pixel_sprites.py` does the following:

1. Normalises each figure by head-to-feet span.
2. Mean-shift flattens the art, then area-downscales it.
3. Quantises in Lab to a per-sprite palette with a cool-shadow / warm-light
   ramp.
4. Despeckles, keeps the source line art as inner contours, and adds a
   one-pixel selective outline.

The party ends up roughly 100 art px tall and the boss roughly 230.

This means they hold their portrait's pose. All motion comes from `msbf.px`
warping the one image per art pixel (breath, lean, squash, extremity flutter,
wing rotation, writhing), plus whole-sprite choreography.

Per state:

| State | Party | Matsuda |
|---|---|---|
| Idle | breath and flutter | per form: weight-shift with streaming hair; a wing stroke with a pulse inside it; writhing with genre glitches |
| Ready | step forward, outline, cursor | — |
| Attack | dash and strike; Asahina's Dragoon jump; Sam's heavy chop; Himeko's card throw | lunge per form; Nahobino switches to her standing pose (phase1concept.png) to cast |
| Cast / support | magic circle, rise and flash | power: tint and lift, and the standing pose in phase 1 |
| Hurt | knockback and flash | flash, knockback and shake |
| Evade, guard | hop; crouch | — |
| Weak | kneel | — |
| KO / revive | exact quarter-turn lying down; revive pillar | — |
| Phase break | — | the outgoing form shatters into blocks |
| Phase reveal | — | the descent (phase 2); the tear-in (phase 3) |
| Final victory | — | collapse synced to the hypernova |
| Defeat | — | looming |

The "distinct poses" version of this needs genuinely new art. The runtime
already supports it: imported strips in `sprites.json["anims"]` replace a
state's frames and switch off the body warps. The prompts and the workflow
are in `docs/assets/sprites/SEER_PIXEL_SPRITE_PROMPTS.md`. The stage, the
importer round trip, and playback of imported idle and attack strips in the
real fight were verified with a synthetic strip that was then removed.

## The entrances

- **Normal, about 6.4s.** The camera starts tilted at the sky. The party runs
  in (FF battle entry). A glint appears and she falls. The landing hits:
  shockwave, flash, camera hit, and the party is shoved a step. She rises.
  Her eyes cut in from phase1.png. The glaive sweep cuts the frame. Then the
  name card: MATSUDA / CRIMSON-AZURE, THE ONTOLOGICAL SEER · PHASE I,
  NAHOBINO.
- **Id Mode, about 5.1s.** The room and the party decode in torn frames. Tohu
  Imago is simply there, in 6× blocks and posterised. Her wings open tier by
  tier. Her halo-eye cuts in, then the light. The card arrives corrupted.

The running orders are `MSBF_PX_INTRO` / `MSBF_PX_ID_INTRO` in
pixel_stage.rpy. The stage and the screens both read them, so a retime is
one edit.

## Numbers worth knowing

- Stage render cost is about 1.2 ms per frame in phase 2 with 4 members, and
  about 2.0 ms in phase 3 with 7. Uncapped frame intervals measured about
  4.4 ms and 6.4 ms.
- Commit (wind-up) times come from `msbf_px_commit_time`: dash 0.36s, jump
  0.46s, heavy 0.44s, cast 0.40s. The resolve lands on the frame the
  choreography strikes.
- Her coil before each action is `max(enemy_step_delay, 0.52)`, set by the
  screen timer. Battle logic is untouched.

## Engine facts this pass established

1. **`renpy.register_shader` emits `fragment_functions` before that part's
   uniform declarations.** A helper that reads a uniform fails to compile
   ("undefined variable u_px_seed"). Pass uniforms, and samplers, into
   helpers as parameters.
2. **A class with `__slots__` must inherit `python_object`** in Ren'Py. Lint
   does not catch it; the boot dies with "Classes with __slots__ do not
   support rollback".
3. **`easeinout` is not an ATL warper.** Use `ease`. Lint reports it as "two
   expressions in a row".
4. **Pixel-crisp warping recipe.** Wrap the image in
   `Transform(img, mesh=True, nearest=True, shader=…)` with an OUTER
   `Transform(zoom=N, nearest=True)`. In the shader, quantise `v_tex_coord`
   to art-pixel cells, warp the cell centre, then sample at `floor(s) + 0.5`.
   Rotation uses `rotate_pad=False` and only ever quarter turns.
5. Bash heredocs with an odd number of apostrophes break the tool's quoting.
   Write patch scripts to files.

## October 1 follow-up: the killing-blow freeze, and Battle Art

**Bug: a striker froze mid-dash across a bar break.** A physical move that
delivered the killing blow on a bar left the attacker standing at Matsuda's
feet through the whole next phase.

Cause: a killing blow raises `phase_blackout`, not `hit`. The stage only
starts the walk home on a hit, so the attacker stayed in `commit` forever,
pinned at full reach.

Two fixes in `MSBFPixelStage`:
- A phase change now resets everything in flight: moves, hurt/evade/support
  timers, and Matsuda's coil.
- A `commit` older than `MSBF_PX_COMMIT_TIMEOUT` (1.2s) is walked home. This
  also covers Id Mode's 50% rupture threshold and the finale.

Probe target `bug_killdash` reproduces the case.

**Battle Art: Pixel / Illustrated** (`persistent.msbf_seer_art`, `"pixel"` or
`"hq"`). Illustrated draws the original art, the archetypes and Matsuda's
three forms, through the same stage. Every dash, flash, warp, wing beat,
writhe, KO and entrance is shared.

How it works:
- `build_seer_pixel_sprites.py` writes an "illustrated twin" for every sprite
  in `pixel/hq/`. Each twin is the source art, area-downscaled onto the pixel
  sprite's own canvas at `HQ_UNIT` texels per art pixel (party 3, boss 4.5),
  mirrored the same way, with the crop landing exactly where the pixel art
  sits. A registration overlay showed no doubling. The pixel PNGs are
  byte-identical after the rebuild.
- `msbf.px` now works in art units (`u_px_unit`, `u_px_hq`). Pixel mode snaps
  to texel centres as before. Illustrated mode samples continuously, keeps
  soft alpha, and draws the selection outline and rim one art unit wide.
  Glitch blocks (`u_px_block` ≥ 2) pixelate the illustration itself.
- Imported hand-animated strips are pixel art, so they only play in Pixel
  mode.
- Phase 3's genre glitch inverts: in Illustrated mode she flickers into her
  pixel sprite instead of into the illustration.
- Pixel effects draw on a one-pixel grid under the illustrations, which gives
  a banded, cel-like look.
- Cost is unchanged: about 2.1 ms per frame in phase 3 with 7 members.

The toggle is in the fight's pause menu (a BATTLE ART panel) and on the
party select, next to the formation preview. It is read live, so flipping it
mid-fight changes the art on the next frame.
