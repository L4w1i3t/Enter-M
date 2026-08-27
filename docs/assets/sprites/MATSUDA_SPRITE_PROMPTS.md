# Matsuda Sprite Rebuild Authoring Record

Date: 2026-08-24

This is the production record for Matsuda's clean-room sprite rebuild. The
runtime system deliberately follows Himeko and Tsubaki: one intact neutral
whole-body base per outfit, with one outfit-conditioned face layer placed over
it. Alternate poses are standalone whole-body images because their arms, hair,
and silhouettes move.

Every Matsuda face or pose from an earlier iteration was treated as obsolete.
No file whose name contains `old` or `post_`, no prior Matsuda expression
layer, and no prior alternate pose was used as an image-generation input,
identity reference, registration target, color source, or processing input.

## Approved source boundary

The only pre-existing whole-body source sprites retained are the two requested
neutral bases:

- Casual: `game/assets/characters/matsuda/neutral.png`
- Uniform: `game/assets/characters/matsuda/neut_uniform.png`

Both are native 1023x1537 RGBA sprites. The casual artwork did not need to be
redrawn: its outfit, anatomy, linework, and matte shading passed visual review.
Before the final builder pass, four known detached one-pixel, alpha-3 specks at
`(708,916)`, `(710,917)`, `(708,918)`, and `(229,1438)` were removed from the
casual base. No connected character artwork changed. The uniform base required
no pixel cleanup. The installer now copies both verified bases byte-for-byte.

For image generation, each approved base was composited over a flat saturated
magenta authoring screen without rescaling or moving it:

- `tmp/matsuda_rebuild_fresh/generation_anchor_casual_magenta.png`
- `tmp/matsuda_rebuild_fresh/generation_anchor_uniform_magenta.png`

The built-in image generator returned a baked checker when asked directly for
transparent expression edits. The uniform magenta anchor was therefore used
for all 20 fresh expression masters. The screen is an authoring aid only; the
processor derives the face patches and removes it before export.

## Expression generation prompt

The built-in image generator was called once per non-neutral expression in
identity-preserving edit mode. Each call used only the approved uniform anchor
and this prompt structure:

```text
Use case: identity-preserve
Asset type: Ren'Py visual-novel character sprite expression master
Input images: Image 1 is the edit target and sole identity, style, composition,
and texture anchor: Matsuda's canonical uniform neutral sprite on a flat
saturated magenta production-key background.
Primary request: Change only Matsuda's facial expression to [EXPRESSION].
Style/medium: preserve Image 1's exact polished matte 2D anime sprite rendering,
facial proportions, line weight, colors, and non-glossy texture.
Composition/framing: preserve the exact 1023x1537 portrait canvas, character
position, scale, head angle, silhouette, and all non-face regions.
Constraints: keep the flat magenta background perfectly uniform and
untextured. Preserve hair, headband, braid, earrings, outfit, gloves, jewelry,
body, hands, pose, lighting, and every region outside the face. Keep all facial
details clean and spatially aligned to the neutral face for later overlay
extraction.
Avoid: transparency checkerboard, grid/checker texture anywhere, black, white,
or color residue on the face, crop, shift, blur, jagged edges, glossy/plastic
shading, identity drift, altered hair/outfit, garbled or duplicated facial
features, extra objects, text, or watermark.
```

The `[EXPRESSION]` directive used for each fresh master was:

| Runtime token | Expression directive |
|---|---|
| `happy` | A broad, warm, genuine smile with cheerfully closed eyes. |
| `smug` | Half-lidded confident eyes, one subtly lifted brow, and a compact knowing smirk. |
| `teasing` | A playful wink and open, lighthearted grin; mischievous rather than cruel. |
| `thinking` | An upward side glance, lightly raised contemplative brows, and a tiny closed mouth. |
| `curious` | Alert widened eyes, lifted brows, and a softly open questioning mouth. |
| `unamused` | A heavy half-lidded "bruh" stare, flat brows, and a level closed mouth. |
| `annoyed` | Pinched lowered brows, narrowed eyes, and a restrained displeased pout. |
| `frustrated` | Eyes squeezed shut, tense brows, and visibly clenched teeth. |
| `angry` | Sharply lowered brows, a hard direct glare, and an open angry retort. |
| `sad` | Raised inner brows, softened downcast eyes, and a small downturned mouth. |
| `crying` | Clear tears from both eyes, distressed brows, and an open trembling sob. |
| `embarrassed` | Strong natural cheek blush, gently averted eyes, and an awkward small smile. |
| `nervous` | Uneven worried brows, tense eyes, a small uncertain smile, and one sweat drop. |
| `worried` | Strongly raised inner brows, open concerned eyes, and a small parted mouth. |
| `shocked` | Very wide eyes, high brows, and a small round mouth; surprise rather than fear. |
| `afraid` | Wide tense eyes, distressed brows, clenched teeth, and a faint sweat cue. |
| `panicked` | Tiny pupils, extreme high brows, an open alarmed mouth, and visible sweat. |
| `determined` | A firm direct gaze, strongly set brows, and a tight resolved mouth. |
| `empty` | Unfocused, glassy, half-lidded eyes with slack brows and an affectless mouth. |
| `disgusted` | Sideward narrowed eyes, uneven pinched brows, and a curled asymmetric grimace. |

Neutral is not generated. `face_neut_casual.png` and
`face_neut_uniform.png` are intentionally transparent compatibility layers so
the exact face already present in each neutral base remains visible.

Fresh expression masters are stored at:

`tmp/matsuda_rebuild_fresh/masters/face_<token>_uniform.png`

## Alternate-pose generation prompts

Each pose was a separate built-in identity-preserving image-generation call on
a flat magenta authoring screen. The service did not expose a backend model
version. The common prompt was:

```text
Use case: identity-preserve
Asset type: standalone full-body Ren'Py visual-novel reaction sprite
Input image(s): [APPROVED MATCHING MAGENTA ANCHOR, plus only the newly generated
uniform laughing pose when transferring that action to the casual outfit]
Primary request: [POSE DIRECTIVE]
Style/medium: preserve the exact polished matte 2D anime sprite rendering,
identity, facial proportions, line weight, palette, restrained highlights,
and non-glossy texture of the approved anchor.
Composition/framing: preserve the exact 1023x1537 portrait canvas, the same
apparent character height, scale, and bottom alignment, and keep the complete
silhouette and every hand inside frame.
Constraints: preserve Matsuda's exact identity and requested outfit. Keep the
background perfectly flat saturated magenta and untextured. Use exactly two
anatomically coherent arms and hands.
Avoid: transparency checkerboard, grid/checker texture, magenta/black/white
residue, glossy or plastic shading, malformed or extra fingers/limbs, crop,
identity or outfit drift, extra objects, props or effects unless requested,
text, and watermark.
```

| Output | Fresh pose directive and inputs |
|---|---|
| `pose_laughing_uniform.png` | From the approved uniform anchor: explosive genuine laughter, eyes shut, open laughing mouth, one gloved hand at her stomach and the other raised loosely. |
| `pose_laughing_casual.png` | From the approved casual anchor, with only the new uniform laughing master as an action reference: the same uncontrollable laughing action in the exact casual outfit. |
| `pose_shrug_uniform.png` | From the approved uniform anchor: a smug theatrical shrug, shoulders raised, elbows outward, both forearms lifted, and both palms up; exactly two arms and hands. |
| `pose_facepalm_uniform.png` | From the approved uniform anchor: an amused theatrical-disbelief facepalm with one gloved hand across her forehead and a wry smile; not upset. |
| `pose_chuuni_uniform.png` | From the approved uniform anchor: an exaggerated chuuni stance with one hand framing an eye and the other open palm thrust dramatically toward the viewer; no prop or magic effect. |

The untouched RGB generation masters are stored under:

`tmp/matsuda_rebuild_fresh/masters/poses/`

## Deterministic post-processing

Image generation itself is stochastic. The following registration, masking,
keying, normalization, export, and validation steps are deterministic for the
recorded masters and canonical bases.

`tools/build_matsuda_fresh_faces.py` performs all expression processing after
generation. It reads only the two approved bases and the 20 exact fresh
masters. Hair-only SIFT/RANSAC registration keeps extreme expressions from
moving the fit; an outfit transform maps the authored face to the casual base.
One fixed, connected, 256-level feather mask is shared by all 20 non-neutral
expressions in each outfit; neutral remains fully transparent. The complete
brow/eye/iris/mouth envelope is forced to alpha 255 so the neutral base cannot
show through at outer eye corners, while the lower jaw feather remains more
than four pixels inside the canonical exterior silhouette. It exports 42
full-canvas RGBA layers, zeros RGB beneath zero alpha, verifies 21 unique
composites per outfit, and emits full-body/head reviews plus focused
`casual smug` and `casual thinking` regressions from `0517.rpy` over light,
dark, and checker backgrounds.

`tools/build_matsuda_fresh_poses.py` uses only the five fresh magenta pose
masters as art inputs and reads both canonical bases for scale/color QA. It
performs color-decontaminated chroma keying, high-precision premultiplied
resampling, scale/baseline normalization, detached-component cleanup, and
edge-safe RGB reconstruction. It exports five 1023x1537 RGBA pose sprites and
light, dark, and checker review sheets.

`tools/install_matsuda_fresh_sprites.py` assembles the complete two-base,
42-face, five-pose candidate in a temporary workspace directory. It requires
the exact face/pose manifests, binds every staged file and base to the builder
reports by SHA-256, runs the strict validator, and performs file-by-file atomic
replacement with rollback for the complete set. It does not touch
`convention_fullbody.png` or any unrelated asset.

## Runtime contract and commands

Production face layers use:

`game/assets/characters/matsuda/face_<token>_<outfit>.png`

The only layered-image bases are `neutral.png` and `neut_uniform.png`.
`game/asset_definitions/def_characters.rpy` exposes the unchanged story-facing tokens
`casual`, `uniform`, `neut`, the 20 alternate expressions above, and the four
pose names. Laughing supports both outfits, so four pose names map to five
files.

Build, review, install, and validate with:

```text
python tools/build_matsuda_fresh_faces.py
python tools/build_matsuda_fresh_poses.py
python tools/install_matsuda_fresh_sprites.py
python tools/validate_matsuda_sprites.py
python tools/build_matsuda_render_probe.py --staged-eye-only
python tools/build_matsuda_render_probe.py --run-eye-only
```

Detailed input/output hashes and QA metrics are recorded in:

- `tmp/matsuda_rebuild_fresh/face_build_metrics.json`
- `tmp/matsuda_rebuild_fresh/poses/provenance_metrics.json`
- `tmp/matsuda_rebuild_fresh/diagnostics/`
- `tmp/matsuda_rebuild_fresh/poses/contact_sheet_{light,dark,checker}.png`
