# Sprite height scaling — CUT, kept for reference

**Status:** built, measured, verified in-engine, then **removed** on 2026-08-06.
Nothing in `game/` implements this today. This file is the record so it does not
have to be re-derived from scratch if it is picked up again.

**Superseded 2026-08-23** by `docs/SPRITE_AUTHORING_GUIDE.md`, which solves the
same problem by REDRAWING the cast at a shared pixels-per-inch instead of
scaling finished art after the fact. That removes the hair clipping and the
`xnudge`/Archive-chip fallout recorded below by construction. The measurements,
the Monika head-ratio finding, and the known problems in this file are still
the reason the new approach is shaped the way it is -- read it before starting.

**Why it was cut:** it changed how every sprite in the game sits in every scene,
and it was not worth carrying that while the Archive work was still landing.
It was a "start", not a finished art pass.

---

## The problem it was solving

Every cast sprite is defined in `game/asset_definitions/def_characters.rpy` as:

```renpy
image matsuda neut = Transform(".../neutral.png", fit="contain", xysize=(640, 960))
```

A flat 640×960 for everyone makes the cast one **size**, not one **scale**.

Measured from the alpha bounding box of each PNG (source canvas 1023×1537 for
the whole project cast), at the standard slot zoom of 0.80:

| sprite | height | figure drawn | px per inch |
|---|---|---|---|
| sam | 71" | 753 px | 10.60 |
| mc | 70" | 759 px | 10.84 |
| matsuda | 69" | 752 px | 10.90 |
| mom | 66" | 753 px | 11.41 |
| kotonoha | 65" | 735 px | 11.31 |
| tsubaki | 64" | 740 px | 11.55 |
| asahina | 64" | 746 px | 11.66 |
| **monika** | **65"** | **715 px** | **11.00** |

So a 71" character and a 64" character drew within 2% of each other, and
px-per-inch swung 10.6–11.7 — i.e. stated heights were ignored entirely.

Two secondary findings worth keeping:

1. **Characters changed height when they changed clothes.** Each PNG has the
   figure drawn at a slightly different size inside the shared canvas, so
   Tsubaki's casual (924 px at zoom 1) and her `post_neut` (934 px) differ by
   ~1%, and `post_revelation` by ~2%.
2. **No figure is centred in its canvas.** `transforms.rpy` places sprites with
   `xcenter`, which centres the *canvas*. Measured offsets of the figure centre
   from the canvas centre, at slot zoom: Matsuda **+31 px**, Monika **+42 px**,
   Tsubaki +15, Sam +15, Mom +14, Kotonoha +10, MC +3, Asahina −7.

## The model that was built

**Monika is the ruler**, because she is the one asset the project does not draw
and cannot re-cut. Her forward pose composites to a **894 px figure on a 960 px
canvas**, and she is 65", giving

```
CAST_PX_PER_INCH = 894 / 65 = 13.754   # px per inch of character height, at zoom 1.0
```

Each sprite then gets `scale = (inches × 13.754) / (that file's own normalised
figure height)`, applied by widening the normalising canvas:

```renpy
init -1 python:
    def cast_sprite(path, scale=1.0, xnudge=0):
        sized = Transform(path, fit="contain",
                          xysize=(int(round(640 * scale)), int(round(960 * scale))))
        if not xnudge:
            return sized
        return Transform(sized, xoffset=xnudge)
```

`xnudge` re-centres the *figure* on its slot. Matsu'Py Transforms do not clip, so
a nudge can only ever move a figure, never crop it.

**Monika was excluded**: scale 1.0 by definition, and no nudge, because her
layeredimage has no single centre to correct — her arm attributes move her
centroid ~40 px between `ldown/rdown` and `lpoint/rhip`, so one fixed number
would be wrong for half her poses.

## The measured table

```renpy
image matsuda neut           = cast_sprite(".../matsuda/neutral.png",      1.0096, -39)  # 69"
image matsuda uniform neut   = cast_sprite(".../matsuda/neut_uniform.png", 1.0096, -34)  # 69"
image tsubaki neut           = cast_sprite(".../tsubaki/neutral.png",      0.9522, -18)  # 64"
image tsubaki uniform neut   = cast_sprite(".../tsubaki/neut_uniform.png", 0.9516,  -8)  # 64"
image tsubaki post_neut      = cast_sprite(".../tsubaki/post_neut.png",    0.9421,  -1)  # 64"
image tsubaki post_revelation= cast_sprite(".../tsubaki/post_rev.png",     0.9594,  -4)  # 64"
image asahina neut           = cast_sprite(".../asahina/neutral.png",      0.9439,   8)  # 64"
image asahina uniform neut   = cast_sprite(".../asahina/neut_uniform.png", 0.9439,  10)  # 64"
image asahina uniform terror = cast_sprite(".../asahina/terror.png",       0.9458,  11)  # 64"
image sam neut               = cast_sprite(".../masayami/neutral.png",     1.0382, -19)  # 71"
image sam uniform neut       = cast_sprite(".../masayami/neut_uniform.png",1.0382, -21)  # 71"
image kotonoha neut          = cast_sprite(".../kotonoha/neutral.png",     0.9730, -12)  # 65"
image kotonoha work neut     = cast_sprite(".../kotonoha/work.png",        0.9691, -11)  # 65"
image mom neut               = cast_sprite(".../himeko/neutral.png",       0.9644, -17)  # 66"
image mom uniform neut       = cast_sprite(".../himeko/neut_uniform.png",  0.9644,   0)  # 66"
image mom wasted             = cast_sprite(".../himeko/wasted.png",        0.9820, -13)  # 66"
image mc neut                = cast_sprite(".../mc/neutral.png",           1.0154,  -4)  # 70"
# incidental cast, scaled against an ASSUMED height (no roster entry):
image math_teacher neut      = cast_sprite(".../npc/math_teacher.png",     0.9902,  12)  # assumed 67"
image civics_teacher neut    = cast_sprite(".../npc/civics_teacher.png",   1.0239,   2)  # assumed 67"
image track_coach neut       = cast_sprite(".../npc/track_coach.png",      1.0802, -16)  # assumed 70"
```

Resulting slot zooms (base `z` 0.80): sam 0.831, mc 0.812, matsuda 0.808,
monika 0.800, kotonoha 0.778, mom 0.772, tsubaki 0.762, asahina 0.755.

Heights come from `character_roster` in
`game/addons/Roster View/roster_view.rpy`. **If this is revived, keep the two in
step** — the scale encodes the roster's number.

## Known problems with it as built

1. **Sam's hair is clipped.** True proportional puts him at 0.831, which pushes
   ~40 px of hair above the frame (it was ~11 px before). Two one-line fixes,
   neither applied because both are global framing changes:
   - base `z` 0.759 makes him fit, but shrinks Monika ~5% and she was supposed
     to be the fixed point;
   - `ypos` 1.03 → ~1.085 in `transforms.rpy` drops everyone by 40 px, costing
     leg — cheap, since every sprite is thigh-cropped anyway.
2. **Suspected Archive fallout, never diagnosed.** After this went in, the Side
   Stories drawer's 52×52 subject chip rendered wrong for Matsuda (the largest
   `xnudge`, −39). The likely cause is `ArchivePortraitCrop` doing
   `fit="cover"` + `crop` over a Transform that already carries an `xoffset`.
   **If this is revived, check the small chips first** — the 300×308 roster
   cards and the 300×360 dossier looked fine, so it only showed up at chip size.
3. **The head-size mismatch is untouched.** DDLC art has a much larger
   head-to-body ratio than the project sprites, so even at matched heights
   Monika reads closer/younger. Matching total figure height does not fix that;
   matching head size would, but automatic head detection was tried and failed —
   long hair means there is no reliable neck minimum in the alpha width profile.

## Decisions already made about it

- Scale anchor: **true proportional, Monika as the ruler** (chosen over "Monika
  is the ceiling", which would have shrunk her ~4% along with everyone).
- Crowd shrink for busy stages: **declined for now.** The idea was a multiplier
  by slot count (e.g. 3-up ×0.95, 4-up ×0.90). Max slot count actually used in
  script is 4 (`t41`–`t44`); there are no 5-slot transforms.

## How it was measured

PIL over each PNG's alpha bounding box; Monika's extent is the **union** of the
pieces a pose composites (`monika_forward_facebase.png` +
`monika_forward_uniform_left_down.png` + `..._right_down.png`), not any one file,
because `forward` has no bodybase — her arms are the body.

Verified in-engine with the env-gated
`config.label_overrides["splashscreen"]` screenshot harness. Two traps there:
two `show monika ...` statements share the tag `monika`, so the second replaces
the first (use `as`); and `game/dev.rpy`'s SingleInstance lock blocks a CLI
launch while the game is open — copy `renpy.exe`/`renpy.py` to another name in
the SDK dir to get a private lock.
