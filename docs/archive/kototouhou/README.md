# Kotonoha boss sheet source

This directory preserves the image-generation source used to build the shipping
Kototouhou boss atlas. It is excluded from release builds by `game/options.rpy`.

## Files and consumers

- Generated source: `kotoboss_sheet_imagegen_source.png` (1224x1285 RGBA)
- Normalizer/validator: `tools/build_kotonoha_boss_sheet.py`
- Shipping atlas: `game/addons/Matsuda's Sick Boss Fight/kotonohamode/kotoboss_sheet.png`
- Legacy still: `game/addons/Matsuda's Sick Boss Fight/kotonohamode/archive/kotobosssprite_legacy.png`

The shipping atlas is 512x512 RGBA: four columns by four rows of 128x128 cells.
Rows are idle, bank left, bank right, and spell cast. The normalizer extracts
the dominant subject in each generated tile, applies one global scale, anchors
all frames at bottom center, enforces six pixels of padding, hardens alpha, and
quantizes the sheet to at most 48 opaque colors.

## Rebuild

Tested with Python 3.14, Pillow 12.2.0, NumPy 2.4.0, and SciPy 1.16.3.

```powershell
python tools/build_kotonoha_boss_sheet.py `
  docs/archive/kototouhou/kotoboss_sheet_imagegen_source.png `
  "game/addons/Matsuda's Sick Boss Fight/kotonohamode/kotoboss_sheet.png"
```

The tool validates that the result has 16 distinct nonempty cells, binary
alpha, safe cell padding, and no more than 48 opaque colors before saving.

## Generation prompt

Built-in image generation was given the legacy boss still as the primary
costume/proportion reference and `game/assets/characters/kotonoha/neutral.png`
as the canonical identity reference, with this prompt:

> Use case: stylized-concept
>
> Asset type: production-ready pixel-art boss sprite sheet for a vertical
> danmaku game
>
> Primary request: expand Kotonoha into one coherent 4-column by 4-row
> animation sheet with exactly 16 full-body frames, suitable for a classic
> Japanese bullet-hell boss.
>
> Subject: the same young woman with very long wavy lavender hair, a small
> braid across her fringe, purple eyes, gray ribbed turtleneck sweater, dark
> purple pleated knee-length skirt, dark socks, and brown shoes. Preserve her
> recognizable identity and restrained, slightly uncanny calm.
>
> Style/medium: crisp hand-authored pixel art with a limited
> lavender/charcoal/plum palette, strong readable silhouette, clean clusters,
> restrained highlights, and a late-1990s/early-2000s Japanese PC danmaku-game
> sprite sensibility. Original character only.
>
> Composition/framing: exact regular 4x4 grid, 16 equally sized square cells.
> One complete character per cell, consistently scaled and centered on the
> same bottom-center anchor, with generous transparent padding and no clipping.
>
> Animation plan: row 1 is a four-frame hovering idle loop with subtle
> hair/skirt/arm motion; row 2 is a four-frame bank/move-left sequence; row 3
> is a separately drawn four-frame bank/move-right sequence; row 4 is a
> four-frame spell-card cast from composed hands through open channeling and
> recovery.
>
> Constraints: genuinely transparent background; consistent anatomy, outfit,
> scale, palette, light direction, pixel density, and bottom anchor; hard pixel
> edges; no antialiasing; no text, labels, borders, guide marks, extra
> characters, weapons, projectiles, magic circles, logos, or watermarks.
