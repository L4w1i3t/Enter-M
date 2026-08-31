# Tsubaki Face-Plate Authoring Record

Current revision: 2026-08-30

## Current production contract

Tsubaki now uses the same slicing model as Himeko and Asahina: an intact
outfit-native neutral sprite under one broad, full-color oval face plate. Each
alternate plate carries the surrounding bangs, both brows, both eyes, nose,
and mouth as one registered raster. The plate therefore owns the complete
neutral-brow footprint instead of trying to reconstruct separate facial parts
or trace a skin-shaped mask around them.

The two production bases remain byte-unchanged:

- Casual: `game/assets/characters/tsubaki/neutral.png`
- Uniform: `game/assets/characters/tsubaki/neut_uniform.png`

There are 21 conditioned layers per outfit. `face_neut_<outfit>.png` is fully
transparent because the corresponding base already contains the neutral face;
the other 20 layers share one pixel-identical oval alpha within that outfit.
Casual and uniform keep separate registration because their eyes differ by
about six vertical pixels.

The canonical builder is `tools/build_tsubaki_faceplates.py`. Its oval is
clipped only by the approved base silhouette and uses:

- radius `(155, 135)`;
- solid radius `0.84`;
- center 31 pixels below the detected eye midpoint; and
- a geometric lower fade from 85 through 105 pixels below center.

Unlike the retired schema-v5 pipeline, the exported alpha does not use a skin
component, sparse semantic union, neutral-brow guard, or expression-specific
negative mask. The expression masters do contain detached pale upper-lid
residue. A bounded lash-relative cleanup replaces only that residue with the
color-matched featureless authoring donor *before* the complete source raster
is sliced through the oval. Intentional near-lash eyelid folds remain.

Current staging and review paths:

- Build: `tmp/tsubaki_oval_faceplates/built/`
- Metrics: `tmp/tsubaki_oval_faceplates/metrics.json`
- Review sheets: `tmp/tsubaki_oval_faceplates/review/`
- Pre-install backup: `tmp/tsubaki_oval_faceplates/pre_install_backup/`
- Runtime screenshots: `tmp/tsubaki_render_probe/`

Canonical commands:

```text
python -B tools/build_tsubaki_faceplates.py build
python -B tools/build_tsubaki_faceplates.py review
python -B tools/build_tsubaki_faceplates.py validate
python -B tools/install_tsubaki_sprites.py
python -B tools/build_tsubaki_render_probe.py
python -B tools/validate_tsubaki_sprites.py --render-root tmp/tsubaki_render_probe
```

`tools/process_tsubaki_face_patches.py` remains only as a compatibility entry
point and forwards to the oval builder. It cannot recreate schema v5. The dated
acceptance record is `2026-08-30-tsubaki-oval-faceplate-rebuild.md`.

## Superseded pipeline history

Everything below this heading documents the earlier skin-stencil approaches.
It is retained as failure analysis, not as the current build specification or
command source.

Original record date: 2026-08-24

This records the approved pipeline for Tsubaki's face-only sprite bank. The
runtime design deliberately mirrors Himeko's: one intact neutral whole-body
base per outfit, with an outfit-conditioned face layer placed over it. The old
head/body/arm decomposition and Tsubaki-specific pose groups are not part of
this production contract.

Earlier sprite-authoring and height-scaling documents are intentionally not a
specification for this rebuild. Runtime geometry uses only the shared
`fit "contain"`, `xysize (640, 960)` transform. There is no Tsubaki-specific
height adjustor, zoom, translation, per-outfit offset, or face-layer offset.

## Approved source boundary

Only these two raw sprites were approved as whole-body bases or image-edit
references:

- Casual: `game/assets/characters/tsubaki/neutral.png`
- Uniform: `game/assets/characters/tsubaki/neut_uniform.png`

Both files are native 1023x1537 RGBA sprites. They remain byte-unchanged in
production and retain their original canvas, placement, silhouette, hair,
clothing, hands, lighting, palette, and neutral faces.

No filename containing `old` was used. Neither `post_neut.png` nor
`post_rev.png` was used as a face source, identity reference, registration
target, color reference, or image-generation input. The `tsubaki post_neut`
and `tsubaki post_revelation` image names are separate legacy runtime cards;
they are not members of the normal casual/uniform expression system.

## Featureless authoring-donor edit

The built-in image generator's precise-object edit mode was run separately on
each approved base. This was an in-place removal edit, not a redraw or a new
sprite generation pass. The operative instruction was:

> Edit this exact sprite in place. Remove only the eyebrows, eyelashes, eyes,
> irises, mouth, and cheek blush, replacing those pixels with matching local
> facial skin. Retain the nose exactly. Preserve every other pixel and feature:
> head shape, jaw, ears, hair, hair clip, neck, body, clothing, hands, shading,
> palette, linework, silhouette, scale, position, and camera. Keep the exact
> 1023x1537 canvas and the exact existing sprite geometry; do not crop, resize,
> translate, rotate, re-pose, or restyle anything. Return real RGBA transparency
> outside the sprite. Do not add a checkerboard, grid, matte, background, text,
> scenery, props, or any new facial feature.

The tool preserved the requested canvas and registration, but returned opaque
RGB checker-backed images rather than the requested transparent RGBA. The
resulting featureless files are therefore authoring references only:

- `tmp/tsubaki_face_patch/featureless_casual_generated.png`
- `tmp/tsubaki_face_patch/featureless_uniform_generated.png`

They are never installed or displayed directly. Processing reads the
flood-connected facial-skin topology from each reference. Following the
eyebrow-regression repair documented below, it also color-matches the
outfit-native featureless RGB and uses it only inside two tightly guarded
cleanup regions: a conservative neutral-feature region centered on the base
eyebrows, and the duplicated pale upper-eyelid arcs. The disconnected checker is excluded by the registered
sprite/cleanup masks. Review sheets also place finished sprites over a
synthetic checker for edge inspection, but no checker pixels enter a production
PNG.

## Deterministic registration and export

`tools/process_tsubaki_face_patches.py` performs every operation after the two
precise-object edits:

1. It loads the approved 1023x1537 casual and uniform bases without modifying
   their geometry.
2. It locates each base's two amber irises and derives an outfit-specific
   similarity transform from the previously registered expression bank.
3. It reuses the existing expression masters under
   `tmp/tsubaki_sprite_masters/` and their deterministic registration metrics
   under `tmp/tsubaki_sprite_processed/`. `happy` uses
   `expression_happy_v2.png`; the other alternates use
   `expression_<token>.png`.
4. It derives the connected facial-skin field from the featureless authoring
   reference, color-matches expression-master skin to the corresponding
   approved base, and clips the result to one fixed, broad, softly feathered
   face mask per outfit. The mask is constrained to the connected facial-skin
   field and stops above the chin/neck join.
5. It isolates a conservative eye-relative region from the reviewed sparse
   neutral layer, warps that guarded footprint into each outfit, and places a
   small featureless cleanup plate below every alternate face. The flattened
   source connects brow ink to a few bang and upper-eye fragments, so the guard
   intentionally overincludes them rather than risking lost brow edges. The
   alternate face plate covers those extra pixels; the underlay is exposed only
   where the broad face mask previously missed base-brow/bang intersections.
6. It registers each reviewed sparse expression layer as a binary semantic
   keep mask. Source alpha is thresholded before an `INTER_NEAREST` warp, so
   filtered resampling cannot create ringing islands that later become facial
   detail. The exact registered masks and their outfit unions are hashed.
7. It locates the real upper lash independently in each registered expression,
   builds a robust top profile, and searches only the 2-10-pixel band above that
   profile. A featureless-donor comparison selects the darker pale/peach ghost
   arc, while dilated authored-brow and selected-lash masks are absolute keep
   zones. The negative mask is therefore expression-relative instead of a
   universal traced strip.
8. It makes both the union of all 20 semantic masks and the union of all 20
   adaptive negative masks fully opaque in every alternate layer. It subtracts
   the active ghost-arc mask from that expression's positive support, restores
   corrected master RGB on the remainder, and finally writes exact
   outfit-matched featureless RGB on the active negative mask. This gives all
   alternates one stable alpha topology while preserving complete authored
   brows, eye contours, blush, tears, and mouths without resurrecting rejected
   source residue.
9. It exports 42 outfit-conditioned broad-feathered face-patch assets: 21
   runtime tokens for casual and the same 21 for uniform. The two `neut` assets
   are intentionally transparent compatibility layers because each approved
   base already contains its exact neutral face; the 40 alternate assets carry
   the visible replacement patch.
10. It zeros RGB beneath zero alpha and emits metrics plus full-body and head
   review sheets on light, dark, and checker backgrounds. A separate 2x
   nearest-neighbor upper-face sheet preserves native pixels for the final
   brow/lash gate; downsampled contact sheets are not sufficient acceptance.

The expression masters are reused as authored expression designs, but they are
never copied directly into production. Registration, skin matching, masking,
and export are deterministic and outfit-specific; no second image-generation
pass creates the alternate faces.

## Eyebrow regression repair

Repair completed: 2026-08-26.

The May 23 `uniform sad` frame exposed two independent artifacts in the first
face-patch export:

- Every expression master contained a pale upper-eyelid arc which could read as
  a second eyebrow once an emotional brow moved away from it. The arc was
  already present inside the fully opaque face-layer RGB, so changing Ren'Py
  attributes or merely widening alpha could not remove it.
- The common feathered mask did not fully own the intact bases' neutral brow
  strokes near the bang intersections. Roughly three tenths of a conservative
  neutral-feature guard centered on that region was partially blended,
  allowing a second base-brow fragment to survive under all 40 alternate
  faces.

`process_tsubaki_face_patches.py` handles the defects separately. It lays an
outfit-native featureless neutral-feature guard below the alternate face, then
removes pale source-master ghost arcs through an adaptive lash-relative negative
mask. The 2026-08-30 correction replaced the universal traced paths: those paths
sat above the artifact in lowered-lid expressions and semantic restoration then
reintroduced the missed pixels. Builder and validator assertions now require
exact adaptive-mask reconstruction, complete donor replacement on the negative
mask, no changes outside it, and zero overlap with the dilated real brow or
selected lash. Both approved neutral bases and both transparent `neut`
compatibility layers remain byte-unchanged.

## Semantic detail ownership repair

Repair completed: 2026-08-29.

Gameplay review exposed incomplete eyes, half-erased brows, and apparent brow
misalignment in `annoyed`, `embarrassed`, `disgusted`, and `shocked`. Runtime
definitions and placement were correct: the damage was already present in the
generated face PNGs. The expression masters still contained the missing
strokes, but the universal duplicate-arc cleanup crossed authored brow and eye
support, and the broad skin-constrained face mask did not fully own every fine
feature pixel.

Schema-v4 authoring fixes both causes without repainting or regenerating the
art. Each sparse authored-feature mask is thresholded in source space, warped
with nearest-neighbor registration, and protected from cleanup. Its corrected
master RGB is restored exactly, while the union across all expressions is
encoded into every alternate alpha mask to prevent topology changes during
attribute switches. The approved source bundles and crop matrices are pinned;
the validator independently rebuilds every semantic, protection, cleanup, and
registration mask before accepting production.

The semantic unions remain 10,862 pixels for casual at
`(405,323)-(605,483)` and 10,639 pixels for uniform at
`(406,318)-(605,476)`. Both lie entirely on fully opaque base pixels. The
2026-08-29 visual-acceptance claim was superseded after native-scale gameplay
review exposed remaining ghost arcs. The corrected implementation and current
acceptance record is `2026-08-30-tsubaki-adaptive-ghost-arc-repair.md`.

## Runtime token mapping

The Ren'Py attribute remains `neut`, even though the approved casual base file
is named `neutral.png`. `uniform` remains the outfit attribute; the filename
`neut_uniform.png` is not an image attribute.

| Requested expression | Runtime token | Authored face intent |
|---|---|---|
| Neutral | `neut` | Exact neutral face already present in the approved outfit base. |
| Happy | `happy` | Bright, genuine smile and warm, lively eyes. |
| Smug | `smug` | Lowered eyelids, subtly raised brow, compact knowing smirk. |
| Teasing | `teasing` | Playful focused eyes and a light asymmetric grin; amused, not cruel. |
| Thinking | `thinking` | Sideward glance, lightly knit brows, small contemplative mouth. |
| Curious | `curious` | Alert widened eyes, lifted brows, softly open questioning mouth. |
| Unamused | `unamused` | Heavy half-lidded "bruh" stare, flat brows, tiny level mouth. |
| Annoyed | `annoyed` | Pinched brows and restrained pout; irritated, not furious. |
| Frustrated | `frustrated` | Tense lowered brows, narrowed eyes, compressed mouth. |
| Angry | `angry` | Sharply lowered brows, hard direct glare, pronounced frown. |
| Sad | `sad` | Raised inner brows, softened downcast eyes, small downturned mouth. |
| Crying | `crying` | Clear tears from both eyes and a visibly distressed, trembling mouth. |
| Embarrassed | `embarrassed` | Averted eyes, gentle blush, awkward small smile; neither helpless nor coy. |
| Nervous | `nervous` | Uneven worried brows, tense eyes, uncertain mouth, faint allowed blush. |
| Worried | `worried` | Strongly raised inner brows, open concerned eyes, small parted mouth. |
| Shocked | `shocked` | Very wide eyes, high brows, round open mouth; surprise rather than fear. |
| Afraid | `afraid` | Wide tense eyes, distressed brows, fearful open mouth, faint allowed flush. |
| Panicked | `panicked` | Extreme alarm with contorted high brows and a broad trembling mouth. |
| Determined | `determined` | Firm direct gaze, strongly set brows, tight resolved mouth. |
| Empty/Dead-eyed | `empty` | Unfocused half-lidded stare, slack brows, affectless mouth. |
| Disgusted | `disgusted` | Sideward narrowed eyes, uneven pinched brows, curled asymmetric grimace. |

## Production paths and commands

Authoring inputs and intermediate records:

- Approved bases: `game/assets/characters/tsubaki/neutral.png` and
  `game/assets/characters/tsubaki/neut_uniform.png`
- Featureless donors: `tmp/tsubaki_face_patch/featureless_*_generated.png`
- Existing expression masters: `tmp/tsubaki_sprite_masters/`
- Existing registration layers/metrics: `tmp/tsubaki_sprite_processed/`
- Registered output and metrics: `tmp/tsubaki_face_patch/output/`
- Visual reviews: `tmp/tsubaki_face_patch/output/_review/`

Production runtime files:

- Whole-body bases: `game/assets/characters/tsubaki/neutral.png` and
  `game/assets/characters/tsubaki/neut_uniform.png`
- Face layers:
  `game/assets/characters/tsubaki/face_<token>_<outfit>.png`
- Runtime wiring: `game/asset_definitions/def_characters.rpy`

Build and review commands:

```text
python tools/process_tsubaki_face_patches.py
python tools/install_tsubaki_sprites.py
python tools/validate_tsubaki_sprites.py
python tools/build_tsubaki_render_probe.py
```

The installer manifest covers the 42 generated face layers. The two approved
bases already live in the production directory and are deliberately not
rewritten by installation. The isolated render probe copies those 42 installed
layers plus both unchanged bases and renders every outfit/token combination.
