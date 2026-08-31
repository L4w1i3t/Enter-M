# Tsubaki adaptive upper-eyelid ghost-arc repair - 2026-08-30

> Superseded later on 2026-08-30 by
> `2026-08-30-tsubaki-oval-faceplate-rebuild.md`. This document records why
> schema v5 failed; its skin-constrained alpha, semantic restoration, and
> adaptive negative-mask export are no longer the production architecture.

## Scope and screenshot mapping

This revision fixes the remaining eyebrow-like lines visible in Tsubaki's May
23 uniform expressions. The circled gameplay frames resolve directly to:

| Story call | Runtime asset | Reported symptom |
|---|---|---|
| `0523.rpy:137` - `show tsubaki uniform disgusted` | `face_disgusted_uniform.png` | broken pale arc above both lashes |
| `0523.rpy:139` - `show tsubaki uniform worried` | `face_worried_uniform.png` | detached inner/outer arc fragments |
| `0523.rpy:232` - `show tsubaki uniform unamused` | `face_unamused_uniform.png` | long line floating above lowered lids |

There is no sticky-expression or Ren'Py placement ambiguity in these frames.
All Tsubaki layers share one canvas and transform; the selected PNGs already
contained the defect.

The repair is bank-wide for all 20 non-neutral expressions in both casual and
uniform. The approved full-body bases and transparent `neut` compatibility
layers remain unchanged.

## Corrected diagnosis

The circled marks are not truncated primary eyebrows. Native-pixel comparison
shows that the real brows are continuous and registered. The extra marks are
pale/peach upper-eyelid arcs present in the source expression masters,
immediately above the true dark lashes. They entered the sparse semantic mask,
so schema v4 treated them as authored positive ownership and restored them after
cleanup.

The schema-v4 cleanup used universal traced source paths. Those paths happened
to intersect some expressions, but they did not follow vertical lid movement.
For the two clearest lowered-lid failures, the old uniform boxes were too high:

| Expression | Old fixed cleanup box | Actual adaptive negative box |
|---|---|---|
| `disgusted` | `(410,345)-(602,360)` | `(407,350)-(606,369)` |
| `unamused` | `(411,344)-(602,359)` | `(405,352)-(606,369)` |

This explains why broad semantic preservation repaired missing eye/brow detail
yet also resurrected the unwanted line.

Rejected alternatives:

- Crop/offset correction: runtime wiring and full-canvas registration are
  already consistent; moving the layer would move the entire face.
- Full-brow replacement: current schema-v4 brows are continuous across all 40
  alternates, and a second extraction path adds needless registration risk.
- Same-source sparse RGB fill: it creates dark speckles, blush fragments, and
  antialiasing residue rather than reconstructing clean local skin.
- One wider fixed strip: lowered, closed, and wide-open eyes occupy different
  heights, so a universal strip either misses residue or damages real lashes.

## Schema-v5 adaptive negative mask

For each outfit/expression pair, the builder now:

1. Finds the two real dark upper-lash components around the registered amber
   iris centers.
2. Interpolates each component's top edge, median-filters it with a five-pixel
   kernel, and clamps local excursions to the median plus or minus four pixels.
3. Constructs a nine-pixel candidate band from two through ten pixels above the
   real lash profile.
4. Subtracts three-by-three-dilated source-authored brow ellipses and the
   selected lash itself, then clips the corridor to the opaque approved base.
5. Compares the authored master against the outfit-matched featureless donor.
   Seeds require a channel delta of at least 6 and a donor-minus-authored
   luminance gain of at least 2.0. A closed core relaxes those limits to 3 and
   1.0; the one-pixel fringe requires 2 and 0.5.
6. Replaces every accepted negative pixel with exact featureless-donor RGB and
   subtracts the same mask from semantic positive ownership before RGB restore.
7. Unions all 20 negative masks per outfit and combines that result with the
   positive-detail union as the common opaque topology for every alternate.
   Only the active negative mask receives exact featureless RGB; pixels owned
   solely for another expression encode their unchanged pre-ownership composite.

The cleanup is exact, local, and deterministic. It does not repaint the face or
regenerate any expression.

## Measured footprint

The circled uniform states produce these exact negative masks:

| Expression | Pixels | Bounding box |
|---|---:|---|
| `worried` | 638 | `(407,338)-(606,356)` |
| `disgusted` | 955 | `(407,350)-(606,369)` |
| `unamused` | 1,078 | `(405,352)-(606,369)` |

Across the complete bank, casual masks range from 246 to 941 pixels and uniform
masks range from 287 to 1,078 pixels. Their complete counts are:

| Expression | Casual | Uniform |
|---|---:|---:|
| `happy` | 630 | 697 |
| `smug` | 689 | 817 |
| `teasing` | 814 | 857 |
| `thinking` | 563 | 605 |
| `curious` | 817 | 848 |
| `unamused` | 883 | 1,078 |
| `annoyed` | 941 | 995 |
| `frustrated` | 889 | 932 |
| `angry` | 578 | 569 |
| `sad` | 795 | 870 |
| `crying` | 782 | 819 |
| `embarrassed` | 716 | 736 |
| `nervous` | 281 | 300 |
| `worried` | 604 | 638 |
| `shocked` | 246 | 287 |
| `afraid` | 478 | 510 |
| `panicked` | 459 | 511 |
| `determined` | 676 | 748 |
| `empty` | 693 | 1,045 |
| `disgusted` | 778 | 955 |

The outfit-wide negative union contains 3,137 casual pixels and 3,423 uniform
pixels. Of those, 454 casual and 612 uniform pixels lie outside the sparse
positive-detail union; precomputing the negative union is therefore required to
keep every alternate's alpha topology identical. The final combined ownership
is 11,316 pixels at `(404,323)-(606,483)` for casual and 11,251 pixels at
`(405,318)-(606,476)` for uniform.

## Acceptance invariants

The builder and independent validator require, per expression:

- the negative mask is a subset of the dynamic band and fully opaque base;
- the negative mask has zero overlap with dilated authored brows and the
  selected real lash;
- every negative pixel met the declared donor-difference thresholds before
  cleanup;
- cleaned RGB equals featureless-donor RGB exactly on the negative mask and
  pre-cleanup RGB is unchanged everywhere else;
- active semantic detail excludes the negative mask, so restoration cannot
  reintroduce the ghost arc;
- the union of all adaptive negative masks is reproduced independently and the
  same combined positive/negative ownership is opaque in all 20 alternates;
- real brow and lash pixels remain bit-for-bit unchanged;
- mask count, bounding box, and SHA-256 digest reproduce from source inputs.

The bank also retains the prior semantic-ownership, source-provenance,
alpha-topology, story-token, and canonical-versus-production checks.

## Visual gate

Downsampled contact sheets hid the thin pale lines, so they are no longer a
sufficient acceptance artifact. The builder emits native-pixel upper-face crops
at 2x nearest-neighbor scale:

- `tmp/tsubaki_face_patch/output/_review/tsubaki_casual_upper_faces_native_2x.png`
- `tmp/tsubaki_face_patch/output/_review/tsubaki_uniform_upper_faces_native_2x.png`

All 40 canonical alternates passed this gate with continuous primary brows,
intact lashes/eyes/sclera/tears, and no detached ghost arcs. The three reported
uniform states were also compared directly before and after at native detail.

## Production and runtime verification

- Canonical schema-v5 build: 42 face layers generated successfully.
- Production installation: all 42 reviewed layers installed under
  `game/assets/characters/tsubaki/`; no obsolete shared face files required
  archiving.
- Independent validator: 42/42 production files byte-match the canonical bank;
  40/40 adaptive negative masks, 40/40 exact donor-clean runtime composites,
  40/40 authored-detail layers, 2/2 positive-detail unions, 2/2 combined
  positive/negative unions, 2/2 neutral guards, and 2/2 alpha-topology repairs
  passed. All 277 `show tsubaki` calls and exact layeredimage wiring passed.
- Ren'Py probe: 42/42 unique, decodable 1280x960 captures rendered, from
  `01_casual_neut.png` through `42_uniform_disgusted.png`. Native runtime review
  of `28_uniform_unamused.png`, `36_uniform_worried.png`, and
  `42_uniform_disgusted.png` confirms that the reported ghost arcs are absent.
- Python tooling: Ruff format/check and bytecode compilation passed for both
  builder and validator; `git diff --check` passed.
- Main project: MatsuPy compile passed with zero unreachable items across 122
  source files. Lint exited successfully. Its existing missing-image warnings
  concern unrelated Monika, Natsuki MPT, and stock DDLC references, not Tsubaki.

## Reproduction

```powershell
python -B tools/process_tsubaki_face_patches.py
python -B tools/install_tsubaki_sprites.py
python -B tools/validate_tsubaki_sprites.py `
  --review-sheet tmp/tsubaki_face_patch/output/_review/production_validated_contact_sheet.png
python -B tools/build_tsubaki_render_probe.py
```

Run the generated 42-state probe and the main project compile/lint with the
local MatsuPy SDK. The accepted production contact sheet is
`tmp/tsubaki_face_patch/output/_review/production_validated_contact_sheet.png`;
the native upper-face sheets remain the final thin-line review gate.
