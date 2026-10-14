# Story cast framing pass — October 11, 2026

Follow-up to the [September 26 cast presentation](2026-09-26-cast-presentation.md).
All changes are in `game/story_cast_framing.rpy`. Registered images, the Archive,
the phone and out-of-scope content are untouched, as before.

## What changed

**The cast is 6% closer (`ENTER_M_CAST_ZOOM = 1.06`).** This is a new house
camera, applied after the camera, stature and height rules and zoomed about the
slots' floor line. Every relationship between figures scales with it, including
eye spacing per inch. The framing layer sits inside the slot transform, so every
slot family (t, i, f, h, hf, l, lf, s) at every stage size, one to eight,
inherits it. The art kept below the crop grows with the zoom, so no hem can
show.

| | before | after |
|---|---|---|
| Sam (tallest), top of hair at rest, 3-up | y = 61 | y = 20 |
| Sam speaking (`f` pose) | y = 25 | y = −17 (hair tips cut) |
| 66" eye line | y = 262 | y = 233 |

Coordinates are 720-space. The focus pose zooms 4.5% about the floor, so at
1.06 a speaking Sam loses the top 17px of his hair. At 1.08 he would lose 32px.

**The incidental cast have heights.** They used to stand on the 66" reference
line. Each height is now read off the art and the script:

| tag | height | basis |
|---|---|---|
| `track_coach` | 72 | tall, athletic man |
| `math_teacher` | 70 | average middle-aged man |
| `charlie` | 69 | lean teenage distance runner |
| `daichi` | 69 | teenage boy (placeholder art) |
| `homura` | 67 | tall, long-legged |
| `civics_teacher` | 64 | average middle-aged woman |
| `science_teacher`, `japanese_teacher`, `english_teacher` | 64 | women in the script (placeholder art) |
| `hikari` | 60 | petite |

**Hikari and Homura were mis-scaled.** Both are drawn with the same head: pupils
75px apart, and 246 vs 251px from crown to chin. The Sep 26 cameras were ×1.08
for Hikari and ×0.94 for Homura, which put a 15% gap between two equal heads.
Hikari's body is drawn small because she is petite, not because the camera is
far away. Matching her shoulders to her peers' therefore made her head the
largest on stage. Both now take ×0.97, which matches pupil distance to the
reference group (Sam 72.6, MC 72.5, Kotonoha 72.4). Their heights carry the
difference between them.

**The photographic adults were matched on shoulders.** A photographed face
cannot be compared with a drawn one. At ×1.00 the coach's shoulders measured
narrower than the math teacher's (352 vs 384 registered px), so he is now
×1.08. Both teachers stay at ×1.00. The coach's eye line was also re-read at
8×: his irises sit at 134.5, not 143.

**Seven- and eight-person crowds frame closer when masked.** Their crowd zooms
are now ×0.70 and ×0.66, continuing the 4/5/6 ladder of ×0.78/0.76/0.74.
Before this, the shot fell from ×0.74 at six to ×0.58 at seven, and every face
sank into the lower half of the frame. Panel-sharing pairs overlap at the
shoulder, but faces stay clear: slots are 160–183px apart and faces about 100px
wide. With Story Panels off, crowds keep their slot zooms, as at four to six.

## Checks run

All runs used the installed 8.6 SDK, GL2, isolated saves (`MATSU_FRESH_RUN` plus
a private savedir and short TEMP). The real persistent kept its hash and mtime.

- Lint clean. Only the standing `check_conflicting_properties` advisory remains.
- An off-project probe (loaded through `RENPY_SEARCHPATH`, so no `.rpyc` reached
  `game/`) restaged 21 scenes before and after:
  - the May 16, 17, 19 and 22 screenshot scenes;
  - NPC solos, pairs and 3-ups;
  - 4- to 8-person stages, with and without a speaker, and with panels off;
  - `i`/`h`/`l`/`f` slots on a 4-up, and `hf`.
- The probe routes shows through `config.show`, the equalizer's seam, exactly as
  the `show` statement does. Logged frame bounds match the offline model of
  `_story_cast_framing` to the pixel.
- No pose reaches meaningfully above its owner's base crown. Sam's poses top out
  at the same 19.4 registered px as his base, so his hair is the binding
  constraint for the top edge.

Not verified: full-route play, packaged builds, and saves from real play.
Pickled frames re-derive their framing on first render, as designed Sep 26.
