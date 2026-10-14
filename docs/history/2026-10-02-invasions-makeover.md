# Archivist Invasions makeover — October 2, 2026

A presentation and flow rebuild of the four playable invasions (Biography,
Horror, Nonfiction, Mystery), plus a redesign of Mystery's act two. Act-one
rules and the other three fights' act-two rules are unchanged.

Pre-makeover snapshot (17 files, SHA-256 manifest):
`C:\Users\Admin\ENTER-M-backups\20261002-invasions-makeover-before\`.

## The brief

The user asked for:

- better graphics and VFX, coherent rooms instead of still images on
  backgrounds, and 2.5D/3D environments where they help;
- facelifts that use textures and the existing effects;
- less jank in the gameplay flow and loop;
- more clarity in Mystery, whose puzzle "feels rather loose".

They made two decisions during the pass:

1. **Mystery's act two becomes a witness lineup.**
2. **Original FX art replaces the ripped Touhou atlas pieces** in the
   invasions.

## What all four share now

Everything shared lives in `inv_kit.rpy` (new) and `fx/` (new).

| Piece | What it does |
|---|---|
| The lens (`inv.lens`) | The whole world is rendered to one texture and finished in one pass: grade, bloom from the texture's mip chain, radial aberration, barrel, a travelling shockwave, row tear, grain, vignette and flash. The HUD is drawn after the lens, so text stays crisp. This is what puts a sprite IN a room. |
| `InvFX` | Decorative particles owned and stepped by the game object. Pause freezes them, and every frame stays a pure function of the sim. Nothing in it owns a hitbox. |
| `InvPaint` | The per-frame painter: one render cache per frame, quantized texture quads for lines, rings and glows (no canvas strokes), and a world target plus a HUD target. |
| `inv.panel` | Cached chrome plates. Each fight has its own style. |
| `inv.sheet` | A projective (square-to-quad) sheet, so a flat image can hang and turn in 3D without the 3D stage. Nonfiction uses it. |
| Turn log | Act-one readouts no longer block on Z. A resolved action holds 30 ticks (skippable after 8), and its line stays in a four-line log until later turns push it out. |
| Retry overlay | `inv_retry_screen`. A loss in act two offers RETRY (from the tear, carrying what act one decided), RESTART, or STOP. The menu cursor also stays where you left it between turns. |
| FX art | `tools/build_invasion_fx_art.py` draws 53 original textures into `fx/`: glow, beam, bolts, sparks, rings, smoke, glass shards, paper scraps, ink, chalk glyphs, picture frames, corridor masses, and three tiling surfaces (corridor, paper, floorboards). Nothing in the invasions crops a ripped sheet any more. |

Shader names are unique and listed in the `invasions.rpy` header.
`inv.pall` (Horror) is retired; its name stays reserved.

## Per fight

**Biography** (`inv_biography.rpy`). `inv.soup` now recovers the floor's
world position per pixel. Act one has an unlit floor with gloss reflections
under the figure. Act two puts the rings, the blade, the thrust and the
daggers on a perspective floor as shader inputs. `inv.misreg` takes a key
tint, a rim and scanlines, so the body sits in the room's light. At the tear
the room shatters (tick 24) and a wave follows (tick 110). The loss word is
FILED.

**Horror** (`inv_horror.rpy`). There is a new corridor shader, `inv.dark`: a
perspective corridor with the `tex_corridor` surface, seams and the lantern
as the only light. Act one stands the figure in that corridor, at the distance
DREAD says, lit and shadowed by your lantern. Act two's masses are drawn
sprites with silhouettes and lit edges rather than boxes. At the tear the
corridor crumbles and the lantern gutters. The loss word is CAUGHT.

**Nonfiction** (`inv_nonfiction.rpy`). Act one prints the figure on a sheet
that hangs from a line between two clips, swings on a spring, and jolts when
struck. At the tear the panels are torn to scraps and the sheet falls flat.
Act two's page gains real paper stock, ink gloss and beads, pencil telegraphs,
a stamp anchor, margin citation numbers and a red ink trail. The loss word is
RETRACTED. The figure is still the placeholder silhouette (see Remaining).

**Mystery** (`inv_mystery.rpy`). Both acts are rebuilt, below.

## Mystery

### Act one: the room

The figure stands on boards in an interrogation room. One lamp hangs on a
cord over it. The lamp swings on a pendulum and takes kicks from heavy moves:
ACCUSE swings it, RECHECK steadies it, DENOUEMENT stills it, and REOPENED
blows the bulb. Its cone comes down through dust and its pool sweeps across
the figure. Act one's FIELD is drawn as a lineup of twelve empty picture
frames, each with its own glyph. A frame is crossed off when a reading is
ruled out (gold when the Archivist did it) and flashes red when one reopens.

The tear: the cord snaps, the bulb falls in front of the figure and breaks on
the boards, the figure leaves through the hole, the frames still open drop
out of the lineup, and the lights come up on those suspects standing in a row.

### Act two: the witness lineup

| Element | Rule |
|---|---|
| Suspects | One figure per reading carried, up to six, each under its frame and glyph. They are faint in the dark and fully lit in your lamp. One is the subject. |
| The bell | It rings on a countdown drawn round your lamp's rim, with a bar under the verdict. It reports whether the subject's FEET are inside the drawn rim (SEEN or UNSEEN), and every open suspect that doesn't match is crossed off. While a suspect's feet are inside the rim, its frame is gold. |
| Never one | At two it says TWO REMAIN and crosses no one. If a verdict would leave one, it withholds the verdict and leaves the mismatch nearest the rim. The side the other crosses fell on still gives the verdict away to anyone watching. |
| Dread | The heartbeat, the lamp's flicker and the closing frame. This is the last split's channel and the only damage warning. It is never printed. |
| ACCUSE (hold Z) | The subject is SOLVED (+25, heal 30), the case reopens (crosses lift, the subject re-rolls) and the field widens by one. A bystander is RULED OUT and leaves through a hole, a new reading walks in later, SOLVED loses 12, and every suspect closes on your light at once for 150 ticks. |
| Reopening | Every third or fourth stroke reopens the case instead of answering. Its countdown runs red, and REOPENING shows for the last 150 ticks. |
| Damage | Only the subject touching you (22). |
| Win | Four solves. The rest of the field leaves, the readout reads FIELD 1 (the only time it ever does), the subject is fully lit once, and then it opens. |

The floor is the same boards from above (`tex_boards`, resolved through the
old substrate). The room's edge is drawn only where you stand near it.

**The honesty contract.** The subject is never crossed off, no verdict is
false, and the bell never leaves fewer than two. `MYGame.audit` counts
violations, and the bot harness re-derives every stroke from positions.

**Tuning, measured** (`tools/run_my_bot_sim.py`, six seeds × carried field
2/4/6, 240 s cap):

| Policy | Wins | Median win time (field 2/4/6) | Notes |
|---|---|---|---|
| smart: splits the field with the rim, reads withheld verdicts, breaks ties by dread, dodges | 18/18 | 27 / 43 / 72 s | Withheld-verdict reads 18/0. Dread ties 39/5. |
| no dread: coin-flips the last two | 16/18 | 45 / 95 / 82 s | Coin flips 68 hits, 90 misses. |
| random: accuses whatever is in reach | 3/18 | — | 286 hits, 1159 misses. Mostly time-outs. |
| idle | 0/18 | — | No deaths inside 240 s. |

Two of the act-two rules came from these measurements. With time as the only
price of a wrong accusation, the random policy won every run as fast as the
smart one. A pull of 0.42 also made "the one that keeps coming closer" a
near-free answer. The miss penalty, the closing-in, a faster bell (255→210
ticks) and a weaker pull (0.28 against more frequent bystander curiosity)
fixed both. Honesty violations across every run: 0.

## Files

| File | Change |
|---|---|
| `game/addons/Archivist Invasions/inv_kit.rpy` | New. The shared kit above. |
| `game/addons/Archivist Invasions/fx/` | New. 53 textures plus `fx_sizes.json`. |
| `inv_biography.rpy`, `inv_horror.rpy`, `inv_nonfiction.rpy` | Shaders, stage rebuilds, act-one/tear/act-two FX, log, cursor memory, checkpoint/resume, retry overlay. |
| `inv_mystery.rpy` | Rewritten: `inv.lamp` (two textures: substrate and boards), `inv.lacuna` key tint, the act-one room and lineup, the act-two witness lineup, the stage, checkpoint/resume, the retry overlay (UNSOLVED). |
| `invasions.rpy` | Shader namespace in the header. Mystery's roster notes describe the lineup. |
| `tools/build_invasion_fx_art.py` | New. The FX art generator. The cross glyph became a keyhole, because a suspect wearing an × read as already crossed off. |
| `tools/run_inv_look_probe.py` + `tools/probes/inv_look_capture.rpy` | New. Scripted screenshots and CPU/wall timings per fight (`base`, `extra`, `extra_my`). |
| `tools/run_my_bot_sim.py` + `tools/probes/my_bot_sim.rpy` | New. Mystery's headless policy harness and honesty check. |

## Checks that ran

- Isolated lint: clean. 97 menus; Mystery's AGAIN/STOP menu became the retry overlay.
- Look probes for all four fights (arrival, menu, hit, tear, act two early and
  late, win, loss, live perf), plus Mystery's extra shots (lineup, bell
  warning, accusation, closing-in, bulb fall, break, lights up). All shader
  flags were OK on gl2.
- Live perf (gl2, 240 Hz panel, draw rate governed to the 60 Hz tick):
  every fight held 60 fps. Mean stage CPU per frame, act one / act two:
  Biography 1.2 / 3.0 ms, Horror 0.8 / 2.8 ms, Nonfiction 1.1 / 1.7 ms,
  Mystery 2.1 / 2.8–3.1 ms. One Mystery run had a single 55 ms stall (4 ms
  of it in the stage). Two reruns did not reproduce it (max 25–28 ms).
- Mystery bot harness as above.

## Remaining

- No hands-on human playtest yet. The bot times are a floor; people read the
  bell more slowly than a bot does.
- Mystery borrows its audio from existing stock: the stroke is `note`, the
  ticking is `text`. A real bell cue would help.
- Nonfiction's figure is still the placeholder silhouette. Per the
  no-procedural-art rule, it needs real art; a generation prompt can be
  written on request.
- Mystery's win shows the subject at lineup scale (about 131 px), not close up.
