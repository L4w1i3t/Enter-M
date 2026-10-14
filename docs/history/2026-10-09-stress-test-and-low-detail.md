# Stress test, spec emulation and Effects Detail — October 9, 2026

The heavy side modes were measured on emulated low-end machines. The pass
removed the wasted work it found (five sources) without changing a pixel, gave
the resolution dial something to do (the one backdrop where capping
measurably pays), and added a Low setting that drops decoration. No mode's
rules, art or audio changed.

Pre-change snapshot (56 files, SHA-256 manifest):
`C:\Users\Admin\ENTER-M-backups\20261009-perf-pass-before\`.

## The brief

The user asked for:

- a stress test of the most graphically intense sections, mostly the side
  content: Matsuda's fight, the Archivist Invasions, the Kotonoha (Touhou) mode
  and the like;
- emulated specs, because the development PC (Ryzen 5 8400F, RTX 5060,
  240 Hz) runs everything without strain;
- optimization of flow that keeps graphical fidelity;
- a low-detail mode in Settings for the intensive parts.

## The spec emulator

`game/addons/Dev Hub/spec_emulator.rpy` is developer-only. The Dev Hub folder
is excluded from builds. Pick a preset in the SPEC EMULATOR block on the Dev
Hub's SYSTEM page, or launch with `ENTER_M_SPEC=<key>` in the environment.
READOUT puts the live numbers in the bottom-left corner.

| Preset | CPU × | GPU × | Display | Stands for |
|---|---|---|---|---|
| `native` | 1 | 1 | native refresh | measurement only |
| `native60` | 1 | 1 | 60 Hz | this PC on a 60 Hz panel |
| `midrange` | 1.4 | 9 | 60 Hz, 1920×1080 | i5-1135G7 + Iris Xe (2021 thin-and-light) |
| `deck` | 2.0 | 8 | 60 Hz, 1280×800 | Steam Deck |
| `budget` | 2.4 | 23 | 60 Hz, 1920×1080 | i5-8250U + UHD 620 (2018 laptop) |
| `potato` | 5.0 | 45 | 60 Hz, 1366×768 | Celeron N4020 + UHD 600 |

The emulator measures two times every frame:

- CPU time: wall time from one flip to the next, minus the time spent blocked
  waiting for events.
- GPU time: a `GL_TIME_ELAPSED` query from the end of the render tree to the
  flip.

It then holds the flip until `max(CPU× × cpu, GPU× × area × gpu)` has passed.
`area` is the preset's screen divided by the window: the Budget GPU factor at a
1280×720 window is 23 × 2.25 = 51.75. Frames present on a virtual 60 Hz vblank
grid with one frame of render-ahead. A real swap interval of 4 on the 240 Hz
panel is not equivalent. The driver presents "at least four vblanks later", so
a late frame cost 4 ms instead of 16.7 ms.

The factors are ratios against this PC: published single-thread scores for the
CPU, and for the GPU the geometric mean of ALU throughput and memory bandwidth.
The module header lists what the model leaves out: caches, drivers, thermals,
off-thread decode and fixed per-draw costs.

### The clock pin

At this game's load the RTX 5060 stays in a low power state: P5, about
700–1100 MHz graphics and 810 MHz memory, against maxima of 3090/14001. GPU
timer readings there are inflated, and by different amounts for different
work. One render-to-texture pass measured 0.207 ms at P5 and 0.019 ms at full
clocks (11×). No formula over the clock readings can correct that.

**PIN GPU CLOCKS** runs one small dummy pass right after each flip: 512×512,
arithmetic only, adapted until NVML reports full clocks, capped at 6 ms. It
runs outside the timed window and is never counted. A first version used six
full-screen passes, and that work leaked into the CPU readings: Kotonoha's
flood went from 9.4 to 21 ms, because the next frame's GL calls queued behind
it. Use pinned runs for GPU numbers. Unpinned runs give slightly cleaner CPU
numbers.

The pin has a limit. Once a preset drags a mode far below 60 fps, the real GPU
idles for most of each held frame and drops its clocks anyway. The inflated
readings then lengthen the next hold, so a collapse looks worse than it is. In
the tables below, † marks a run whose graphics clock averaged under 2000 MHz.

## How the modes were driven

A harness outside the project tree loads its scenarios through
`RENPY_SEARCHPATH` and runs with `MATSU_FRESH_RUN=1` and a private save
directory. It boots each mode straight into its fight and plays it with a bot:

| Scenario | What runs |
|---|---|
| `koto` | Kotonoha pinned to chosen cards: an invulnerable, auto-firing soul, the boss's HP and card clock held. The `flood` segments top the field up to the 480-bullet cap, which no authored card reaches (the heaviest, the finale, holds about 310). `bombs_full` adds a bomb every 2.5 s. |
| `msbf`, `msbf_id` | Matsuda's fight and Id Mode. A bot commits moves through the same call a click makes. Segment names are targets: where the bot has reached in a fight varies between runs. |
| `tsb` | Tsubaki, forcing each authored dodge pattern in turn (phase one, then phase two after the real shift), with a soul that can't die and a pilot that weaves inside the box. |
| `ar_home`, `ar_zavodila` | Asarhythm on autoplay, from the densest horror-effect window of "home" (46 effects) and the densest chart ("zavodila_remix"). |
| `inv_*` | All four invasions in godmode under one bot (they share an input shape): Biography's act one and act two, the other three in act two. |

The harness, its README and the batch result tables are kept outside the
project at `C:\Users\Admin\ENTER-M-backups\20261009-stress-harness\`.

## What was found and fixed

None of these changes alters the picture. The numbers are mean milliseconds
per frame on this PC at full clocks, at 1280×720.

**Matsuda's pixel stage redrew its sprites every frame.** A render census of a
phase-one turn counted 28 render-to-texture passes per frame. Ten were created
fresh every frame: the five fighters and their shadows. Turning the pixel
stage off removed 0.675 of the frame's 0.761 ms of GPU time. Turning off every
decorative layer removed 0.000 ms.

- `_draw_sprite` built its mesh `Transform` from a path string each frame. A
  path becomes a new `Image` on every call, and here the render cache did not
  match it, so every sprite texture was redrawn. `msbf_px_disp(path)` now
  keeps one displayable per path: GPU 0.75 → 0.44 ms.
- `_draw_shadow` built a new shader `Transform` for every shadow, every frame.
  It is now memoized on size and strength (`_msbf_px_shadow_tf`). The
  formation layout is memoized too (`_MSBF_PX_FORMATIONS`): GPU
  0.44 → 0.16 ms, and less CPU.
- Id Mode's phase 3 went from 1.16 to 0.24 ms of GPU time.

Tsubaki's boss sprite and the invasion rooms used the same pattern, but there
`Image` equality already let the cache match. They now go through caches as
well (the stage's `_misc` cache and `inv_disp`), and measured no change.

**Tsubaki redrew two things every frame that never needed it.**

- Her strings were drawn on a full-width software canvas. While they were on
  screen, a 1280×420 `Canvas` was rasterized on the CPU and uploaded every
  frame, though the five threads cover a small part of it. The strokes are now
  collected during the render and rasterized into a canvas the size of their
  bounding box (`flush_strings`; `TSB_STRINGS_BBOX = False` restores the old
  full canvas). A/B: −0.36 ms GPU, −0.6 ms CPU.
- Her grid's quad was built around a new `Solid` every frame, so its mesh pass
  rendered a fresh full-screen texture every frame. One shared base
  (`TSB_GRID_BASE`): 0.50 → 0.38 ms.

Together, phase two went from 0.86 to 0.37 ms of GPU time (−57%) and from 5.09
to 4.37 ms of CPU.

The canvas identity check rendered the same frame twice, once with each
canvas. All eleven pairs matched exactly (0 differing pixels). A
negative-control pair with the strings removed differed in 2950 pixels, which
shows the check can see a difference. The shared base is the same `Solid`, so
it draws the same picture by construction.

**Every strike walked 534 transform properties.** Every registered shader
uniform becomes a transform property, and this project has 534 properties,
467 of them uniforms. The engine's `TransformState.take_state` and `diff` read
all of them on every call: 113 and 154 µs a call, about 9 ms in a strike frame
that creates around 35 transforms.

`game/transform_fastpath.rpy` copies and compares only keys present in either
state's instance dictionary. Every other key reads the class default on both
sides, so the result is the same, and `diff` keeps its iteration order. The
patch installs only over the exact engine bytecode it was written against
(fingerprinted for Matsu'Py 8.6.0); on any other engine it leaves the original
methods alone. A shadow run compared both versions on every real call through
a fight: 15,665 `take_state` and 13,140 `diff` calls, 0 mismatches. In
Matsuda's turns:

- mean CPU fell 0.35 and 0.56 ms (two interleaved pairs);
- the worst frame fell from 31.1 to 22.9 ms;
- frames over 20 ms fell from 12 to 5 (838 frames each).

**The resolution dial scaled nothing, and capping only pays on a heavy
shader.** The old Fight Effects stops cap render resolution through
`msbf_fx_scaled`. Its only caller was an arena screen retired in the Seer
facelift, so all three stops drew the same. A capped backdrop is rendered into
a texture of its own every frame and then scaled up. That saves time only where
the backdrop's shader costs more per pixel than the extra pass. All six
candidate backdrops were routed through the dial, then measured at a
1739×978 window with clocks held (GPU ms per frame):

| Backdrop | Native | 720p | 540p |
|---|---|---|---|
| Matsuda's Seer environment | 0.238 | 0.274 | 0.254 |
| Tsubaki's grid | 0.408 | 0.505 | 0.456 |
| Biography's room | 0.685 | 0.629 | 0.478 |
| Horror's corridor | 0.510 | 0.560 | 0.495 |
| Nonfiction's page | 0.376 | 0.459 | 0.418 |
| Mystery's room | 0.306 | 0.393 | 0.359 |

Only Biography's room got cheaper: 30% at 540p. Horror's 540p difference is
noise, and its 720p stop is worse. So the dial now caps Biography's room alone,
and the other five draw directly again, as before the pass. Tsubaki's grid
keeps its shared base. The dial never caps the invasion lens, because the lens
also carries the sprites. At 540p the capped backdrops were aligned and only
softer.

## Tried and dropped

- **Shading the crisp pixel sprites at art resolution** instead of screen
  resolution cost 0.31 ms more GPU (five extra render-to-texture passes at
  about 60 µs each) and was not pixel-identical. It was reverted. Its first
  identity check passed falsely: `render_to_surface` returned the cached
  picture for both paths, and only the negative control exposed it.
  `renpy.display.render.invalidate()` did not prevent that. Rendering the
  stage directly did.
- **Blur** was the costliest single operation benchmarked. In the fights it
  appears only in two arena screens that have been dead code since the Seer
  facelift.
- **Kotonoha's bullet loop and sim** were already tight: plain transforms, no
  render-to-texture. Its floods are bound by Python cost per blit.

## Effects Detail and Effects Resolution

Settings > Graphics has two rows for the heavy modes.

- **Effects Detail** (new; Full or Low; `game/graphics_detail.rpy`), for
  Matsuda's fight and Id Mode, Kotonoha, Tsubaki and the Archivist Invasions.
  Low drops decoration and never anything read to play. Bullets, hazards,
  telegraphs, hit flashes, health and the interface draw exactly as on Full.
- **Effects Resolution** (formerly Fight Effects; Native, 720p or 540p;
  `persistent.msbf_gfx`). It caps Biography's room, the one backdrop measured
  cheaper capped. The caps are 1280×720 and 960×540, so a stop only changes
  anything when the window is larger than it.

| Mode | What Low drops |
|---|---|
| Matsuda's fight, Id Mode | Every layer marked garnish. `msbf_gfx_garnish()` now reads Effects Detail. |
| Kotonoha | The veil's rays, ambient motes, the boss's afterimages, the soul's dash ghosts and the spawn rings. Half the sparks and two thirds of the bullet-cancel stars. |
| Tsubaki | Background streaks and ambient petals. The camellias stay at three. |
| Archivist Invasions | Half the decorative `InvFX` particles, and the lens bloom. |

Thinning keys on a hash of each particle's identity, never on its list
position. Particles die out of the middle of their lists, so a stride would
hand the drawn half to different particles every frame, and the field would
flicker. Raw `id()` values are allocator-aligned and their low bits barely
move: a parity split on them measured 0.000.

Asarhythm doesn't read the switch. It already holds 60 fps on the Budget
preset at 1080p, and its effects are choreography with their own
Photosensitive switch. The story doesn't read it either; it has the Atmosphere
setting.

A profile that had picked the old Fast stop is seeded to Low once, because
Fast also dropped decoration. Restore Defaults sets Full and Native.

Low mostly buys CPU time in the busiest moments. On this PC, Kotonoha's flood
with bombs went from 13.1 to 8.5 ms (p95 20.8 → 11.6) and Matsuda's turns from
5.2 to 4.1 ms. The large GPU costs this pass found were fixed for everyone, so
Low doesn't have to carry them.

## Results under emulation

"Before" ran the frozen pre-change copy. "After" ran the live tree. Both used
the same harness and bots, pinned, at a 1280×720 window. Tsubaki's "before"
was re-run once its scenario brought the room live. Steam Deck runs held full
clocks and give the cleanest per-frame costs. Budget runs show what the 2018
laptop would see. Act-two rows pool all three act-two segments, because what
happens on screen there varies from run to run.

The "after" batch ran before the dial sweep took five backdrops back off the
dial. At Native, which these runs used, the dial only wrapped them without
capping them. Smoke runs after the revert measured the same costs.

### Frame rate

| Moment | Steam Deck fps | Budget 2018 fps | Budget 2018, Low |
|---|---|---|---|
| Kotonoha, 310-bullet finale card | 60 → 60 | 58 → 59 | 60 |
| Kotonoha, 480-bullet flood | 47 → 43 ‡ | 36 → 35 | 38 |
| Kotonoha, flood + bombs | 45 → 41 ‡ | 34 → 33† | 40 |
| Matsuda fight, phase 1 turns | 57 → 59 | 24† → 54 | 56 |
| Matsuda fight, phase 2 turns | 58 → 59 | 25† → 59 | 56 |
| Id Mode, phase 2 turns | 58 → 59 | 16† → 57 | 57 |
| Id Mode, phase 3 turns | 55 → 58 | 11† → 53 | 52 |
| Tsubaki, phase 1 dodges | 60 → 60 | 42 → 53 | 53 |
| Tsubaki, phase 2 dodges | 60 → 60 | 13† → 44 | 43 |
| Asarhythm, densest horror FX | 60 → 60 | 60 → 60 | — |
| Biography, act one | 58 → 59 | 45 → 45 | — |
| Biography, act two | 60 → 60 | 45 → 44 | 46 |
| Horror, act two | 60 → 60 | 55 → 56 | 57 |
| Nonfiction, act two | 60 → 60 | 60 → 60 | — |
| Mystery, act two | 60 → 60 | 60 → 60 | — |

‡ Drift, not code. Kotonoha's Full path only gained a few per-frame checks, and
interleaved runs of the two builds measured within noise (see the cost notes
below).

† The run's GPU clock averaged under 2000 MHz. Matsuda's rows held about
1470 MHz and match what the Deck runs' full-clock costs predict (about
25 fps). Id Mode's rows and Tsubaki's phase two fell under 1000 MHz and
overstate the collapse. From full-clock costs, expect about 25 fps for Id
Mode's phase 2, 17 for its phase 3 and 22 for Tsubaki's phase 2 before the
fixes. Those estimates use mean costs, so they read a few fps high. Kotonoha's
flood with bombs is CPU-bound, so its clock dip doesn't move it.

On the Budget preset at Native and Full, these still fall short of 60 fps
after the pass:

- Kotonoha's synthetic floods: CPU-bound.
- Tsubaki's phase two, at 44 fps: GPU, 0.38 ms at full clocks.
- Biography, at about 45 fps: GPU, mostly its room and the lens.
- Horror, at about 56 fps: right at the edge.

Effects Detail and Effects Resolution are for those cases. Low's numbers
follow; the dial's are in the sweep table above.

### Per-frame cost (Steam Deck runs, full clocks)

These are raw costs on this PC, before any preset factor. Act-two p95s are
frame-weighted averages of the segments' p95s.

| Moment | GPU ms, mean (p95) | CPU ms, mean (p95) |
|---|---|---|
| Kotonoha, 310-bullet finale card | 0.07 (0.09) → 0.07 (0.09) | 6.15 (7.47) → 6.70 (8.23) |
| Kotonoha, 480-bullet flood | 0.16 (0.19) → 0.16 (0.19) | 10.41 (12.97) → 11.36 (13.71) |
| Kotonoha, flood + bombs | 0.09 (0.12) → 0.09 (0.11) | 10.87 (16.67) → 11.93 (17.60) |
| Matsuda fight, phase 1 turns | 0.75 (0.98) → 0.17 (0.42) | 5.97 (11.66) → 5.17 (11.02) |
| Matsuda fight, phase 2 turns | 0.76 (1.03) → 0.16 (0.43) | 5.86 (10.92) → 4.72 (9.01) |
| Id Mode, phase 2 turns | 0.77 (1.05) → 0.17 (0.43) | 5.85 (11.67) → 4.97 (10.32) |
| Id Mode, phase 3 turns | 1.16 (1.61) → 0.20 (0.58) | 7.76 (15.15) → 5.63 (11.44) |
| Tsubaki, phase 1 dodges | 0.41 (0.68) → 0.27 (0.45) | 3.48 (4.74) → 3.71 (4.94) |
| Tsubaki, phase 2 dodges | 0.86 (1.15) → 0.38 (0.56) | 5.14 (6.46) → 4.81 (6.04) |
| Asarhythm, densest horror FX | 0.25 (0.31) → 0.25 (0.31) | 2.84 (4.43) → 3.00 (4.66) |
| Biography, act one | 0.40 (0.50) → 0.41 (0.52) | 4.27 (11.00) → 4.34 (8.94) |
| Biography, act two | 0.42 (0.51) → 0.42 (0.51) | 4.48 (6.57) → 4.48 (6.57) |
| Horror, act two | 0.31 (0.43) → 0.32 (0.43) | 3.97 (5.50) → 4.06 (5.40) |
| Nonfiction, act two | 0.22 (0.25) → 0.22 (0.25) | 2.75 (3.61) → 2.67 (3.61) |
| Mystery, act two | 0.19 (0.21) → 0.19 (0.23) | 3.40 (4.57) → 3.54 (4.90) |

CPU readings drifted about 5% over the hour between the two batches.
Asarhythm, whose code this pass didn't touch, read 0.16 ms more after.
Kotonoha read up to 1 ms more, so its Full path was re-measured with the two
builds interleaved: two rounds each, unpinned, with Asarhythm as a control.

| Segment | Before | After | Difference |
|---|---|---|---|
| Kotonoha finale card | 6.18 ms | 6.24 ms | +0.06 |
| Kotonoha flood | 9.70 ms | 9.72 ms | +0.02 |
| Kotonoha flood + bombs | 10.13 ms | 10.50 ms | +0.38 |
| Asarhythm (control) | 2.88 ms | 2.93 ms | +0.05 |

The same segment varied by up to ±0.5 ms between runs, so none of these
differences is a regression. The batch gap was drift.

Biography's act-two row matches to two decimals by coincidence: its segments
differ, and their pooled means happen to round the same.

### Effects Detail on the Budget preset

Full and Low, run back to back on the same tree.

| Moment | fps Full → Low | CPU ms Full → Low | GPU ms Full → Low |
|---|---|---|---|
| Kotonoha, 310-bullet finale card | 59 → 60 | 6.15 → 5.41 | 0.07 → 0.07 |
| Kotonoha, 480-bullet flood | 35 → 38 | 11.59 → 10.83 | 0.16 → 0.16 |
| Kotonoha, flood + bombs | 33 → 40 | 12.24 → 10.20 | 0.09 → 0.09 |
| Matsuda fight, phase 1 turns | 54 → 56 | 5.21 → 4.06 | 0.17 → 0.15 |
| Matsuda fight, phase 2 turns | 59 → 56 | 4.07 → 3.79 | 0.11 → 0.15 |
| Id Mode, phase 2 turns | 57 → 57 | 4.57 → 3.84 | 0.15 → 0.15 |
| Id Mode, phase 3 turns | 53 → 52 | 5.83 → 4.91 | 0.20 → 0.22 |
| Tsubaki, phase 1 dodges | 53 → 53 | 3.67 → 2.94 | 0.29 → 0.28 |
| Tsubaki, phase 2 dodges | 44 → 43 | 4.73 → 3.96 | 0.38 → 0.38 |
| Biography, act two | 44 → 46 | 4.78 → 4.50 | 0.43 → 0.41 |
| Horror, act two | 56 → 57 | 4.00 → 3.88 | 0.31 → 0.30 |

Low cut CPU in every mode that reads it, by 0.3 to 2.0 ms here, and it lifted
Kotonoha's flood with bombs from 33 to 40 fps. It barely moves GPU-bound
frames: the large GPU costs were waste, and they are gone at Full too.
Matsuda's and Id Mode's turn segments depend on where the bot is in the fight,
so a few fps either way between runs is noise; their CPU column is the steadier
measure.

### Effects Resolution

The measurements are the sweep table under "What was found and fixed".
Budget-preset runs made for this section first were discarded. The emulator
had applied the 1280×720 window's area factor (×2.25) to a 1739×978 window,
where ×1.22 is right, because the harness resized the window after the preset
was armed. That bug is fixed: the factor now follows the window.

## Files

| File | Change |
|---|---|
| `game/addons/Dev Hub/spec_emulator.rpy` | New. The emulator, the clock pin and the readout overlay, which shows the GPU clocks and flags low ones. Developer-only. |
| `game/addons/Dev Hub/dev_hub.rpy` | SPEC EMULATOR block on the SYSTEM page: presets, PIN GPU CLOCKS, READOUT and per-preset stats. |
| `game/graphics_detail.rpy` | New. The Effects Detail preference and its one-time seed. |
| `game/transform_fastpath.rpy` | New. The fingerprinted fast path for `take_state` and `diff`. |
| `game/screens.rpy` | Settings > Graphics: the Effects Detail row. Fight Effects became Effects Resolution (Native/720p/540p). Restore Defaults resets both. |
| `Matsuda's Sick Boss Fight/perf.rpy` | Garnish reads Effects Detail. The F3 readout shows both settings. `msbf_fx_scaled` records the sweep. |
| `Matsuda's Sick Boss Fight/pixel_stage.rpy` | `msbf_px_disp`, the shadow memo and the formation memo. |
| `kotonohamode/kototouhou.rpy` | Effects Detail. |
| `tsubakimode/tsubaki_soul.rpy` | Effects Detail, the shared grid base, the cached boss sprite and the bounding-box string canvas. |
| `Archivist Invasions/inv_kit.rpy` | Effects Detail in `inv_fx_paint` and the lens bloom. New `inv_disp`. |
| `inv_biography.rpy` | Room texture through `inv_disp`. The room draws through the dial. |
| `inv_horror.rpy`, `inv_nonfiction.rpy`, `inv_mystery.rpy` | Room textures through `inv_disp`. |

`seer_presentation.rpy` was edited during the pass and is back to its exact
pre-pass bytes, because the sweep took Matsuda's environment off the dial.

## Checks that ran

- Isolated lint of the live project, last run after every edit: clean. An
  earlier advisory (the fast path's init priority, −1500, outside −999…999)
  was fixed by moving it to −999. The only remaining note is Ren'Py's standing
  suggestion to set `config.check_conflicting_properties`, which predates the
  pass. No orphaned `.rpyc` files in `game/`.
- Fast-path shadow check, as above: 15,665 `take_state` and 13,140 `diff`
  calls in Matsuda's fight, 0 mismatches. A second run went through Chapter
  0.5's first day on fast auto-forward (random picks at menus), past the name
  entry, which was filled in through the card's own commit, to
  `0515.rpy:494`. It compared 13,986 `take_state` and 2,761 `diff` calls: 0
  mismatches.
- Tsubaki string canvas: eleven frame pairs pixel-identical, with a negative
  control that differed.
- Back-buffer captures at Full and Low of Kotonoha's fog card, Tsubaki's phase
  two (recaptured once its room was live), Biography's act two and Matsuda's
  fight. Every gameplay layer was the same at both levels (in the fog card, the
  darkness and the spotlight), and only the decoration thinned. Captures at
  Native and 540p showed the capped backdrops aligned and only softer.
- The emulated batches in the tables above, plus interleaved A/B pairs for the
  fast path (two pairs) and for Kotonoha at Full (two rounds, with Asarhythm
  as a control).
- The resolution sweep: six backdrops at three stops.
- After the final edits: smoke runs of all six heavy scenarios (no errors), the
  emulator's area factor at 1739×978 (×1.22), and Tsubaki's grid base
  re-measured twice (0.39 and 0.38 ms against 0.50).
- A strike-only profile of Matsuda's fight (the ten frames after each move
  resolves), to see what a strike frame still spends.

## Remaining

- No run on real low-end hardware. The emulator scales this PC's measured
  costs; it doesn't model another machine's caches, drivers or thermals. One
  session on a Steam Deck or an integrated-graphics laptop is worth more than
  another emulated batch.
- Kotonoha's 480-bullet floods are a synthetic ceiling, but they stay
  CPU-bound on the Deck and Budget presets at Full: every blit is Python.
  The authored cards hold 60 fps on the Deck. On Budget, Low lifts the flood
  with bombs from 33 to 40 fps.
- The resolution sweep ran on this GPU only. On an integrated GPU, shader
  arithmetic costs relatively more than the capped pass's extra copy, so
  capping Matsuda's or Tsubaki's backdrop might pay there. That is untested.
- A Matsuda strike frame still spends its time in the engine's Cython
  transform rendering and in screen execution. The next levers are fewer
  registered uniforms (467) or fewer transforms per strike.
- The clock pin cannot hold full clocks once a preset drags a mode far below
  60 fps; those rows (†) overstate the collapse.
- The `midrange` and `potato` presets were not batch-measured.
- Asarhythm and the story don't read Effects Detail, by decision.
- No human playtest at Low. Thinning was judged in still captures. Its
  stability in motion follows from the identity hash and was not watched.
