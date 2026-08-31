# Tsubaki expression semantic-detail repair - 2026-08-29

> Superseded in part on 2026-08-30: native-scale gameplay review found that
> schema v4 still retained pale source-master upper-eyelid ghost arcs in several
> expressions. Its alpha normalization and semantic-ownership work remain in
> force, but its fixed-path cleanup and visual-acceptance claims do not. See
> `2026-08-30-tsubaki-adaptive-ghost-arc-repair.md` for the corrected diagnosis,
> adaptive negative mask, and current acceptance gates.

## Scope

This revision repairs the eyebrow and eye-detail failures visible in Tsubaki's
conditioned sprite bank. The reported May 23 frames resolve to the following
uniform expression assets:

- `annoyed` for "Then use the back."
- `embarrassed` for "You came up here Wednesday..."
- `disgusted` for "Plantar fasciitis, right?"
- `shocked` for Matsuda's entrance

The repair was applied bank-wide to all 20 non-neutral expressions in both the
casual and uniform outfits. The two original neutral bases and the two
transparent `neut` compatibility layers remain unchanged.

## Diagnosis

Ren'Py wiring was not cropping or offsetting individual face layers. Every
Tsubaki face asset uses the same 1023x1537 canvas, shared `fit "contain"`
geometry, `xysize (640, 960)`, and whole-character transforms. All four story
calls selected the intended uniform PNG.

The source expression masters still contained the missing brow strokes,
eyelid tapers, lashes, and eye corners. Loss happened downstream in
`tools/process_tsubaki_face_patches.py`:

1. The same two `SOURCE_CREASE_PATHS` were used for every expression.
2. The duplicate-arc cleanup replaced the complete eroded corridor with
   featureless skin, even where an expression's authored brow or eye crossed it.
3. The broad skin-constrained patch alpha left additional fine semantic pixels
   partially owned, making some eye corners look unfinished.

The strongest measured cleanup losses included `shocked`, `nervous`,
`panicked`, `afraid`, and `determined` around the eyes, with especially visible
brow losses in `thinking`, `annoyed`, `angry`, `curious`, and `shocked`.

## Schema-v4 repair

The authoring build now separates positive authored detail from negative
duplicate-arc cleanup:

- Each reviewed sparse expression layer is thresholded at source alpha 8 and
  registered as a binary mask with `INTER_NEAREST`.
- Nearest-neighbor ownership is deliberate. A rejected Lanczos prototype added
  977 casual and 1,067 uniform ringing pixels to the outfit unions.
- The expression mask is dilated by the declared 3x3 ellipse and subtracted
  from the fixed cleanup corridor before featureless replacement.
- The exact authored RGB from the corrected registered master is restored on
  each expression's support.
- The union of all 20 supports is made opaque in every alternate for that
  outfit, retaining one stable mask during expression switches.
- Semantic ownership is rejected anywhere the corresponding base is not alpha
  255.
- Approved semantic layers, masters, head part, featureless donors, outfit
  matrices, and per-expression donor registrations are pinned by schema-v4
  provenance checks.

The accepted ownership geometry is:

| Outfit | Union pixels | Bounding box | Per-layer support |
|---|---:|---|---:|
| Casual | 10,862 | `(405,323)-(605,483)` | 3,397-7,250 |
| Uniform | 10,639 | `(406,318)-(605,476)` | 3,337-7,154 |

Both unions lie completely on opaque base pixels. Connected-component counts
remain diagnostic because nearest-neighbor rasterization can split thin
diagonals; exact mask SHA equality is the acceptance invariant.

## Validator changes

`tools/validate_tsubaki_sprites.py` now independently reconstructs and verifies:

- all 40 binary semantic masks and both outfit unions;
- the pinned outfit and per-expression crop/registration matrices;
- raw cleanup, dilated protection, post-protection, and eroded-core masks;
- zero cleanup/protection overlap;
- full opacity across each expression and union support;
- the authored composite RGB digest on active support;
- source-bundle provenance, fixed outfit alpha topology, byte-identical
  canonical/production output, exact Ren'Py definitions, and all story calls.

## Asset and runtime integration

The canonical schema-v4 build was written to
`tmp/tsubaki_face_patch/output/` and all 42 reviewed layers were installed to
`game/assets/characters/tsubaki/`. No obsolete shared face files required
archiving. Runtime definitions and story scripts required no changes.

No generative repaint was used. This repair preserves the intact expression
masters and corrects only deterministic composition, protection, and ownership.

## Verification

- Canonical rebuild: 42/42 layers reproduced byte-for-byte from the accepted
  staging bank.
- Production validator: 42/42 byte matches, 40/40 duplicate-arc guards, 40/40
  semantic-safe cleanup masks, 40/40 authored-detail layers, 2/2 ownership
  unions, 2/2 neutral guards, and 2/2 alpha-topology checks.
- Story/definition audit: exact layeredimage wiring and all 277 `show tsubaki`
  calls passed.
- Visual QA: 40/40 alternates passed casual/uniform light, dark, checker, head,
  and full-body review. `annoyed`, `embarrassed`, `disgusted`, and `shocked`
  passed in both outfits with no truncation, misalignment, unfinished eyes,
  ringing specks, pale wedges, seams, or visible binary stair-stepping.
- Runtime probe: 42 exact, unique, decodable 1280x960 Ren'Py screenshots passed.
- Python tooling: Ruff check and format check passed.
- Main project: MatsuPy compile passed with zero unreachable items across 121
  source files. Lint exited successfully; its existing missing-asset warnings
  concern unrelated Monika/background and Natsuki MPT files, not Tsubaki.

## Reproduction

```powershell
python -B tools/process_tsubaki_face_patches.py
python -B tools/install_tsubaki_sprites.py
python -B tools/validate_tsubaki_sprites.py `
  --review-sheet tmp/tsubaki_face_patch/output/_review/production_validated_contact_sheet.png
python -B tools/build_tsubaki_render_probe.py
```

Run the generated probe with the local MatsuPy SDK, then compile and lint the
main project with the SDK's bundled Python runner. The accepted production
review is
`tmp/tsubaki_face_patch/output/_review/production_validated_contact_sheet.png`.

## Remaining authoring rule

The semantic masks prove downstream preservation for the reviewed source
features; they do not replace visual review of a newly generated master. Any
future source-bundle change must deliberately update the pinned provenance and
repeat all 40 alternate-expression visual gates before production installation.
