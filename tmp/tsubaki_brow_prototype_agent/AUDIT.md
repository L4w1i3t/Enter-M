# Tsubaki brow repair staging audit (2026-08-30)

Production and shared source files were not edited by this prototype.

## Recommendation

The current schema-v4 bank already has continuous, registered primary brow
strokes in both outfits. The `width20/core32/halo16` contrast-reject pass is
the lower-risk completion: it removes the detached low-contrast upper-lid
duplicates without visibly deleting brows, lashes, irises, blush, or tears in
the 40 current/fixed comparisons.

The full-master brow extraction below is a viable fallback/reconstruction
prototype, but it should not replace the simpler pass unless a primary brow
segment is objectively absent. Its source curve fits are least stable for
`happy` viewer-right, both `angry` sides, and `sad` viewer-right.

## Contrast-reject audit

- Source sheets: `tmp/tsubaki_brow_diagnosis/contrast_reject/`
- Extracted native cells and eight labeled audit montages:
  `tmp/tsubaki_brow_prototype_agent/contrast_cells/`
- Result: no detached pale ghost arc remains across 20 expressions and two
  outfits. Remaining faint peach lines follow the authored master eyelid
  crease and are not floating duplicates.
- Limitation: contrast rejection is subtractive. It cannot reconstruct a brow
  segment that never entered semantic support.

## Full-master fallback

1. Register every full expression master to canonical `head_raw.png` with its
   stored per-expression affine matrix.
2. Use reviewed sparse support only as positive seed evidence.
3. For each source brow, search an ellipse centered at `(402, 596)` or
   `(614, 596)`, axes `(92, 42)`, clipped to `y <= 623`.
4. Robustly fit a quadratic centerline and retain full-master darkening within
   `+-5.25 px`; require every final component to touch a reviewed seed.
5. Map the support mask and expression-minus-`head_raw` RGB through the exact
   same canonical-to-outfit transform. This prevents the mask/RGB divergence
   that created displaced fragments in the earlier pipeline.
6. In target space retain a contrast core of at least `32` and a connected
   halo of at least `16` against the outfit's matched featureless donor.
7. Replace old sparse brow support, reject the duplicate-arc corridor, preserve
   all accepted non-brow semantic details, and write the active brow opaque.

Target iris centers used by the stored registration:

- uniform: `(447.4905, 371.2920)`, `(569.7107, 375.1869)`
- casual: `(446.8642, 376.5356)`, `(570.0014, 381.8663)`

The target brow exclusion zone is an ellipse with axes `(78, 31)` centered
`42 px` above each target iris.

## Output and verification

- Full 42-layer fallback bank:
  `tmp/tsubaki_brow_prototype_agent/full_brow_output/`
- Reported native before/after panels:
  `full_brow_output/_review/{uniform,casual}_reported_native_before_after.png`
- Full-bank native audit:
  `full_brow_output/_review/{uniform,casual}_full_brow_bank_native.png`
- Extraction overlays:
  `full_brow_analysis/reported_extraction_diagnostics.png`
- Machine-readable metrics: `full_brow_output/metrics.json`

The fallback bank passes:

`python tools/validate_tsubaki_sprites.py --layer-root tmp/tsubaki_brow_prototype_agent/full_brow_output`

Validation reports 42 conditioned layers, fixed feather masks, no interior
partial-alpha islands, all 20 alternates distinct per outfit, preserved
silhouettes, exact definitions, and 277 story show calls audited.

## Rejected prototype

Sampling RGB from the sparse layer itself was rejected. Making its union
opaque exposes low-alpha black/speckled fringes and turns blush support into
opaque blobs; it does not reliably reconstruct the main brows.
