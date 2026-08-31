# Tsubaki expression alpha revision - 2026-08-29

> Follow-up: the alpha-topology diagnosis and 220-pixel normalization below
> remain valid, but the earlier claim that every brow and eye detail was already
> complete has been superseded by the schema-v4 semantic-detail repair in
> `2026-08-29-tsubaki-expression-semantic-detail-repair.md`. The source masters
> were intact; a later audit proved that the universal cleanup corridor erased
> legitimate feature pixels after registration.

## Scope

This revision audited and rebuilt Tsubaki's 42 conditioned expression layers:
21 casual layers and 21 uniform layers under
`game/assets/characters/tsubaki/`.

The reported symptoms were apparently over-cropped brows and facial features,
a dark circular spot near the middle of some expressions, and miscellaneous
edge/artifact concerns.

## Diagnosis

The expression files are transparent overlays, not standalone portraits. A
viewer that renders transparency against black makes their intentionally
limited face patch look like a hard black crop. At runtime, the neutral base
supplies the hair, forehead, neck, and outfit around that overlay.

The existing authoring guards showed that both outfit families already owned
the full neutral brow and upper-eyelid replacement region, with no unowned brow
pixels. Broadening or dilating the face mask would therefore have increased the
risk of doubled features, seams, and silhouette drift.

The reproducible defect was instead an enclosed partial-alpha island in the
solid face core of the uniform mask. It occupied 220 pixels at
`(489,402)-(506,418)`. All 20 non-neutral uniform variants inherited the same
island, which could read as a dark center spot. The casual mask did not contain
this defect.

## Repair

`tools/process_tsubaki_face_patches.py` now emits schema-v3 output and performs
a conservative, deterministic normalization before neutral-feature guarding
and expression extraction. A component is eligible only when it is:

- partial alpha;
- enclosed in the central solid face core;
- within narrow area and distance bounds; and
- surrounded by a fully opaque 8-connected ring.

The verified uniform component is promoted to alpha 255. RGB data is untouched,
no alpha value is lowered, and the visible support of the mask is unchanged.
The builder pins the expected outfit-specific repair, so a future source drift
fails instead of silently altering a different region.

`tools/validate_tsubaki_sprites.py` independently checks the same topology,
requires schema-v3 provenance, confirms the exact repair metrics, and rejects
any remaining enclosed partial-alpha island.

## Asset impact

- 20 non-neutral uniform layers changed by exactly 220 alpha pixels each.
- All 21 casual layers remained byte-identical.
- Both transparent neutral layers remained byte-identical.
- RGB changed in zero pixels.
- Visible mask support changed in zero pixels.
- All 42 production layers byte-match the canonical schema-v3 output.

## Verification

- Canonical authoring build: 42 layers generated successfully.
- Fresh paired replay audit: 20 expected uniform layers changed by the exact
  detector-selected 220-pixel component; 22 expected layers remained unchanged;
  fresh repaired, staging, canonical, and production PNG bytes matched.
- Production validator: 42/42 byte matches, 40/40 duplicate-arc guards, 2/2
  neutral-feature guards, 2/2 alpha-topology checks, and exact Ren'Py wiring.
- Runtime probe: all 42 expected 1280x960 screenshots rendered, decoded, and
  produced unique hashes.
- Visual QA: every layer and full-body composite was reviewed on light and
  checker backgrounds; brows and expression features remain complete, and no
  center spot, halo, seam, checker bleed, or pose jump remains.
- Main ENTER M project: MatsuPy compile and lint completed successfully. The
  SDK required write access to its own common-script cache; the initial
  sandbox-only attempt failed for that environmental reason before the clean
  rerun.

## Reproduction

```powershell
python -B tools/process_tsubaki_face_patches.py
python -B tools/install_tsubaki_sprites.py
python -B tools/validate_tsubaki_sprites.py --review-sheet tmp/tsubaki_face_patch/output/_review/production_validated_contact_sheet.png
python -B tmp/tsubaki_expression_revision/verify_repair_delta.py
python -B tools/build_tsubaki_render_probe.py
```

The canonical production review is
`tmp/tsubaki_face_patch/output/_review/production_validated_contact_sheet.png`.
