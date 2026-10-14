# Kotonoha boss sprite rebuild and Endless Practice — September 30, 2026

Two changes to Kotonoha's danmaku mode
(`game/addons/Matsuda's Sick Boss Fight/kotonohamode/kototouhou.rpy`):

- a new boss sprite, drawn from one procedural pixel-art rig, in a stage
  costume instead of her casual wear;
- a fifth reading, **Endless Practice**: the Endless hat of cards played under
  Practice rules.

## The sprite

**Why it was replaced.** The September 20 sheet was sixteen image-generator
cells, one drawing per cell. Her head size, hair mass and leg length drifted
between frames. Each action had only four cells, so the renderer could hold a
pose or flap between two poses, with nothing in between. The sheet was drawn
at a 1.35 zoom, which made its pixels alternate between one and two screen
pixels wide, so the sprite shimmered as she moved.

**What replaced it.** `tools/build_kotonoha_boss_rig.py` draws every frame from
the same model:
- Parts are polygons, rasterized with hard edges.
- Shading is a distance-field dome lit from the upper left.
- Part edges are re-inked after compositing.
- Contact shadows fall where one part overlaps another.
- The eyes, the braid weave and the hair sheen are placed by hand.

Proportions cannot drift, because there is only one body.

- **Layout:** 14 pose rows × 8 loop columns of 96px cells (768×1344).
  - Rows: idle; the lean left and right at three depths; the cast at three
    arm spreads; the declaration at three stages of lifting the card; and a
    recoil.
  - Columns: one shared secondary-motion loop (hair, sleeves, sash tails,
    skirt hem, the book). Every row at column N has its cloth at the same
    point in the loop, so changing pose never jumps the hair.
- **Display:** 2× integer zoom, so every art pixel is a 2×2 block. She is
  about 132px tall on screen, the old sheet's height. The cut-in portrait uses
  the card-raised row at 4× and breathes on the same loop.
- **The costume ("Embodiment of Violet Ink"):**
  - White blouse, with the turtleneck's high collar and long bell sleeves.
  - A slate pinafore in her sweater grey, with the hem and cuffs dipped in
    violet ink.
  - A violet collar bow pinned with a small gold plate: her work name tag,
    the one self that carries her name.
  - A violet sash bowed at the back.
  - The crown braid, pinned with a writing-brush kanzashi and a tassel.
  - The open book she reads her eight lives from, floating at her side.
  - Violet is an accent, not the main colour: the stage backdrop is violet,
    and a violet dress disappeared into it.
- **Poses:** idle is hands clasped low in front (her counter posture). The
  declaration draws the card out of the book and lifts it. The recoil squeezes
  her eyes shut.

**How it animates.** The column is the clock:
`(tick // KT_BOSS_PHASE_TICKS) % 8` in every pose, so a held pose never
freezes. The row is a pose *level* per action (lean, cast, declare; 0–3). Each
level steps one depth at a time, so every pose change plays its in-betweens.
Rules, all in `KTStage._advance_boss_anim` and the `KT_BOSS_*` constants:

- Lean depth comes from eased travel speed, with rise/fall hysteresis. The
  facing latch guarantees a lean never shows the wrong direction.
- A cast is a pulse. It starts only from a gently moving body, holds while
  volleys keep arriving, is capped, and then rests before the next one.
- A hard lean that starts mid-pulse ends the pulse. The arms come down and
  she leans into the travel.
- Cast, card and recoil rows are upright. The lean is walked down underneath
  them and back up afterwards, instead of popping between a tilt and upright.
- No shown row changes faster than 4 ticks. The declaration's first step is
  exempt, because it lands on its beat under the cut-in's white kick.

Boss Transforms moved to their own `KTStage._boss_cache`. 112 cells × 5 draw
variants would otherwise compete with text and shader quads for `_misc`'s
1,200-key budget.

**Backups.**
- The old sheet is at `kotonohamode/archive/kotoboss_sheet_2026-09-20_casual.png`.
- Pre-change copies of every edited file, with a SHA-256 manifest, are in
  `C:\Users\Admin\ENTER-M-backups\20260930-kotonoha-boss-facelift\`.
- `tools/build_kotonoha_boss_sheet.py` and the Kotonoha half of
  `tools/side_mode_sprite_registration.py` belong to the old sheet and were
  left untouched. Neither runs against the new art.

## Endless Practice

In the mode menu (story) and the Arcade variant picker, `kt_practice` and
`kt_endless` together select it:
- Random cards forever, with the Endless HP ladder and speed ramp.
- Unlimited lives.
- No records of any kind.

- **Records gate (the real hazard).** `KTGame._finish` used to write Endless
  records whenever `endless` was set, without checking practice. An
  unlimited-lives run would have set the Endless high score and best wave.
  Practice and debug now skip every record first.
- **HUD.**
  - A cyan `ENDLESS PRACTICE` chip.
  - A `FALLS` counter in place of `BEST W`, a record this mode cannot set.
  - An intro subtitle: "Endless Practice -- No Last Page, No Last Life".
  - The pause panel's exit reads `END RUN`: with no game over, leaving is the
    only way a run ends.
- **Endings.** `kototouhou_quit` has an Endless Practice branch:
  - Kotonoha reports the wave reached, the score and the falls, then offers
    another run or leaving.
  - The Arcade result reads `RUN ENDED`, with wave reached and falls.
  - It pays no Matsucoins, like Practice.

## Also fixed

`tools/run_koto_cutin_probe.py` now sets `MATSU_FRESH_RUN` and a short TEMP.
Before, it ran on the real persistent, a known gap. It also
has `--endless`: the harness always runs practice rules, so this gives Endless
Practice.

Its driver timer lacked `_update_screens=False`. That restarted the
interaction every 0.03s and rebuilt `KTStage` each time, so every capture
showed a newborn stage with no pose or FX-envelope history. The fight's own
poll timer already passes the flag.

The sprite-audit probes (`tools/sprite_audit_modes_probe.py`,
`tools/sprite_audit_modes_motion_probe.py`) were updated to the new layout and
state fields.

## Checks that ran

- Rig: all 112 cells drawn, none touching a cell edge. Loop steps change
  221–421 pixels with no spike at the wrap.
- State machine: the real methods, exec'd out of the .rpy, driven through the
  sway, sweep, dart, high, wild and center moves, declarations and breaks, and
  three fire cadences. Zero skipped depths, zero wrong-facing leans, minimum
  row hold 4 ticks. The one exception is a cast cut short by a declaration on
  its beat.
- Ren'Py 8.6 lint (isolated): clean. No orphan `.rpyc`.
- In engine (`run_koto_look_probe.py`, `run_koto_cutin_probe.py --endless`):
  - The sprite, life ring and cut-in portrait render.
  - The declaration raises and lowers the card in real time.
  - The Endless Practice HUD shows its chip and falls.
  - 60 frames/s, 1.5–1.8 ms mean CPU per frame.

## Not covered

- Nobody has played it by hand yet. The feel of the cast cadence
  (`KT_BOSS_CAST_*`) and lean thresholds needs a real session.
- The VN scenes around the fight still show her casual sprite. The costume
  exists only on the stage.
- Review sheets and animated GIFs of every row are in `tmp/kotonoha_boss_rig/`.
