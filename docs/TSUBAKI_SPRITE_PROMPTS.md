# Tsubaki Face-Patch Authoring Record

Date: 2026-08-24

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

- Casual: `game/mod_assets/char_sprites/tsubaki/neutral.png`
- Uniform: `game/mod_assets/char_sprites/tsubaki/neut_uniform.png`

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

They are never installed or displayed directly. Processing reads only the
flood-connected facial-skin topology from each reference; it does not copy the
reference's RGB pixels into a face layer. The disconnected checker is excluded
by that mask. Review sheets also place finished sprites over a synthetic
checker for edge inspection, but no checker pixels enter a production PNG.

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
   face mask per outfit.
   The mask is constrained to the connected facial-skin field, stops above the
   chin/neck join, and has a solid center large enough to replace all neutral
   brows, eyes, irises, mouth, tears, and allowed cheek blush cleanly.
5. It exports 42 outfit-conditioned broad-feathered face-patch assets: 21
   runtime tokens for casual and the same 21 for uniform. The two `neut` assets
   are intentionally transparent compatibility layers because each approved
   base already contains its exact neutral face; the 40 alternate assets carry
   the visible replacement patch.
6. It zeros RGB beneath zero alpha and emits metrics plus full-body and head
   review sheets on light, dark, and checker backgrounds.

The expression masters are reused as authored expression designs, but they are
never copied directly into production. Registration, skin matching, masking,
and export are deterministic and outfit-specific; no second image-generation
pass creates the alternate faces.

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

- Approved bases: `game/mod_assets/char_sprites/tsubaki/neutral.png` and
  `game/mod_assets/char_sprites/tsubaki/neut_uniform.png`
- Featureless donors: `tmp/tsubaki_face_patch/featureless_*_generated.png`
- Existing expression masters: `tmp/tsubaki_sprite_masters/`
- Existing registration layers/metrics: `tmp/tsubaki_sprite_processed/`
- Registered output and metrics: `tmp/tsubaki_face_patch/output/`
- Visual reviews: `tmp/tsubaki_face_patch/output/_review/`

Production runtime files:

- Whole-body bases: `game/mod_assets/char_sprites/tsubaki/neutral.png` and
  `game/mod_assets/char_sprites/tsubaki/neut_uniform.png`
- Face layers:
  `game/mod_assets/char_sprites/tsubaki/face_<token>_<outfit>.png`
- Runtime wiring: `game/mod_assets/def_characters.rpy`

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
