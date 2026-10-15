# Ontological Seer collectible portraits — October 14, 2026

Updated the seven SR archetype cards in
`game/addons/Matsucoin Currency and Gacha/mc_cards.rpy` to use the same named
images as Ontological Seer's current illustrated party portraits in
`game/addons/Matsuda's Sick Boss Fight/arena.rpy`.

| Card ID | Shared image | Current source dimensions |
| --- | --- | --- |
| `sr_arch_mc` | `msbf_arch_seeker` | 1060 × 1484 |
| `sr_arch_monika` | `msbf_arch_monika` | 1375 × 1144 |
| `sr_arch_kotonoha` | `msbf_arch_kotonoha` | 1024 × 1536 |
| `sr_arch_asahina` | `msbf_arch_asahina` | 1024 × 1536 |
| `sr_arch_sam` | `msbf_arch_sam` | 1024 × 1536 |
| `sr_arch_tsubaki` | `msbf_arch_tsubaki` | 1024 × 1536 |
| `sr_arch_mom` | `msbf_arch_himeko` | 1024 × 1536 |

These names currently resolve to `archetypes/v2/*.png`. Card aspect ratios
match the current canvases, including Seeker's taller canvas and Monika's
landscape pose. Sharing image names lets subsequent portrait replacements
reach the cards too; a future canvas-size change still needs its card aspect
updated. The shared card renderer applies this to the binder, inspection,
and gacha reveals.

Removed the unused legacy archetype directory constant and stale nearby
comments. Card IDs, names, rarity, subjects, flavor text, and ownership logic
are unchanged. No artwork or other card records were modified.

Validation:

- Evaluated all 41 catalog records before and after the change: only the
  seven intended image/aspect pairs differ.
- Both embedded Python init blocks compile.
- All seven image names resolve to existing, decodable PNGs; their dimensions
  agree with `MSBF_ARCH_SIZES` and the card aspect ratios.
- Visually reviewed the [offline crop preview](2026-10-14-seer-card-portraits-preview.png)
  using the existing shell aperture and cover-crop calculations. Faces are
  visible and the portraits fit the apertures. This preview approximates
  image sampling and labels; it is not a Ren'Py screenshot.
- Scoped `git diff --check` passes. No Ren'Py runtime session or full-project
  compile/lint was run for this catalog-only change.

Reference checked: current [Ren'Py displayables documentation](https://www.renpy.org/doc/html/displayables.html)
supports named images wherever a displayable is expected.
