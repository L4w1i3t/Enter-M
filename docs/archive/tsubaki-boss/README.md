# Tsubaki boss-sprite sources

This directory preserves the image-generation masters and registration audit
used for the Tsubaki-mode boss refresh. It is outside the release build; the
small shipping sprites live under
`game/addons/Matsuda's Sick Boss Fight/tsubakimode/`.

## Files and consumers

- Generated masters: the five `*_black_master.png` files in this directory.
- Normalizer: `tools/process_tsubaki_boss_sprites.py`.
- Registration audit: `processed_manifest.json`.
- Shipping set: `phase1.png`, `phase1_strained.png`, `phase2.png`,
  `phase2_exhausted.png`, and `phase2_limp.png` in `tsubakimode/`.
- Superseded shipping art: `tsubakimode/archive/phase1_legacy.png` and
  `tsubakimode/archive/phase2_legacy.png`.

The normalizer extracts the character from each opaque black master, removes
background noise, applies one global 0.25 scale, aligns every lower body to
pixel `(92, 334)` on a shared 184x344 crop, and quantizes to four grayscale
levels. The shipping files deliberately remain opaque on exact black because
the fight's color matrix converts luminance to alpha at render time.

## Rebuild

The tool requires Python, Pillow, NumPy, and OpenCV.

```powershell
python tools/process_tsubaki_boss_sprites.py
```

It rewrites the five shipping PNGs and this directory's manifest. The manifest
records source/output bounds, scale, translation, baseline, visible-pixel
counts, palette, and background-cleanliness checks for every pose.

## Generation direction

Built-in image generation used the legacy boss stills for outfit and battle
silhouette, plus
`game/assets/characters/tsubaki/neutral.png` as the canonical identity
and current-hair reference. The production prompt was:

> Use case: identity-preserving stylized concept art for a production game
> sprite. Draw the same original character, Tsubaki, as a full-body monochrome
> RPG boss figure. Preserve her face, proportions, cropped jacket over a dark
> top, pale fitted pants, high-top shoes, and feather hair ornament on the
> viewer-right side. Her current hair is long, loose, center-parted, and
> increasingly disordered; never give her the retired ponytail. Use confident
> white and gray ink shapes on a completely empty pure-black field, a strong
> readable silhouette, restrained detail, and no environment, floor, shadow,
> text, frame, effects, extra characters, or drawn external strings. Across
> five consistent poses show: controlled but subtly held upright; strained;
> buckling with one hand at her chest; visibly exhausted and messier; and limp,
> head dropped, barely supported. Keep costume, identity, light direction,
> proportions, and line language consistent across the set. Leave safe padding
> around the entire body for rotation and cropping.

A precise background-edit pass then used this instruction for each selected
master:

> Preserve the character exactly. Replace every checkerboard, gray speck, halo,
> and background artifact with uniform RGB `#000000`; add nothing and do not
> crop or redraw the figure.
