# Asahiko (MC) Sprite Rebuild Record

Date: 2026-08-27

This is the production contract for Asahiko's front-facing casual sprite and
layered expression bank. The visible source art was made with the built-in
image-generation tool. `tools/build_mc_sprites.py` is deterministic local
post-processing only: it normalises the generated sources, cuts the shared
face plates, validates the bank, and writes the review sheet.

## Runtime design and file contract

The retired pre-consolidation source
`game/mod_assets/char_sprites/mc/neutral.png` was used only as the identity,
clothing, palette, and rendering reference. It is angled relative to the viewer
and is not a runtime layer in the rebuilt rig. The new canonical base is a
strict straight-on view of the same late-teen, slim runner in his gray hoodie
and black joggers.

Production files live under `game/assets/characters/mc/`:

- `neutral.png`: the intact front-facing casual base.
- `face_neut.png`: a fully transparent compatibility layer.
- `face_<token>.png`: one full-canvas registered face plate for each of the 20
  non-neutral expression tokens.

The complete 21-token house bank, in runtime declaration order, is `neut`,
`happy`, `smug`, `teasing`, `thinking`, `curious`, `unamused`, `annoyed`,
`frustrated`, `angry`, `sad`, `crying`, `embarrassed`, `nervous`, `worried`,
`shocked`, `afraid`, `panicked`, `determined`, `empty`, and `disgusted`.

The Ren'Py rig has one outfit, `casual`, and keeps both `casual` and `neut` as
defaults. Existing callers continue to use `mc neut`; `mc <expression>` and
`mc casual <expression>` select the same base with the requested face plate.

## Built-in base edit

Image 1 was the supplied old MC neutral and served as the identity/style
reference and edit target. The front-facing anchor used this prompt structure:

```text
Use case: identity-preserve
Asset type: full-canvas source render for a Ren'Py layered character sprite
Input images: Image 1 is the supplied old MC neutral and the canonical identity, clothing, palette, proportions, and rendering reference.
Primary request: Redraw the same character, Asahiko, in a strict straight-on/front-facing neutral standing pose. Keep him a late-teen slim runner with short tousled dark-brown hair, amber eyes, a plain gray pullover hoodie, and black joggers.
Scene/backdrop: genuinely transparent background.
Style/medium: polished DDLC-style anime visual-novel character sprite; match Image 1's linework, coloring, and soft cel shading.
Composition/framing: centered full-body portrait on a 1023x1537 canvas; head, shoulders, torso, hips, knees, and feet aligned straight toward the viewer; level shoulders; arms relaxed symmetrically at his sides; balanced stance; same apparent character scale as Image 1; generous clear margin around the silhouette.
Lighting/mood: even neutral visual-novel sprite lighting; calm, reserved expression.
Constraints: preserve Asahiko's identity, age, slim runner build, hair, amber eyes, outfit design, palette, and clean anatomy. Exactly two arms, two hands, two legs, and coherent fingers. Preserve actual transparent alpha.
Avoid: three-quarter or side angle; torso twist; contrapposto; crossed arms; hands in pockets; dramatic gesture; smile or frown; school uniform; jewelry; props; floor or cast shadow; background color, checkerboard, or fake transparency; text; logo; watermark.
```

## Built-in alpha repair

The first approved front-facing render contained a visible transparency
checker. It was repaired as a single-purpose built-in edit before any
expression work. The character itself was locked:

```text
Use case: background-extraction
Asset type: transparent full-canvas Ren'Py character sprite
Input images: Image 1 is the approved front-facing Asahiko sprite and the exact edit target.
Primary request: Replace only the checker/fake-transparency background with genuine transparent alpha.
Constraints: preserve the character exactly, pixel-for-pixel in visible design: identity, face, expression, hair, body, clothing, pose, scale, placement, crop, linework, color, lighting, and shading. Preserve fine hair and clothing edges with clean antialiasing. No halo or matte residue.
Avoid: redrawing, restyling, recoloring, moving, resizing, or changing any part of Asahiko; opaque background; checkerboard; floor shadow; text; logo; watermark.
```

## Built-in expression edits

Every non-neutral expression was a separate built-in identity-preserving edit
of the repaired front-facing alpha anchor. The same anchor was supplied anew
for each token so expression edits could not accumulate drift.

```text
Use case: identity-preserve
Asset type: full-canvas source render for a Ren'Py layered character-expression sprite
Input images: Image 1 is the approved front-facing transparent Asahiko anchor and the exact edit target.
Primary request: Change only Asahiko's face to <EXPRESSION INSERT>.
Scene/backdrop: genuinely transparent background.
Style/medium: match Image 1's polished DDLC-style anime visual-novel linework, rendering, palette, anatomy, and soft cel shading exactly.
Composition/framing: preserve Image 1's exact straight-on body pose, head angle, hair silhouette, scale, stage location, crop, and 1023x1537 portrait canvas.
Constraints: preserve exact identity, late-teen slim runner proportions, short tousled dark-brown hair, amber eye color, skin tone, gray hoodie, black joggers, lighting, and every non-face detail. Change only eyebrows, eyes, mouth, and small expression-specific cheek, tear, or sweat details explicitly requested. Keep genuine transparent alpha.
Avoid: body, outfit, hair, camera, scale, canvas, crop, or pose changes; extra or duplicated eyes, brows, mouths, teeth, tears, or sweat; warped anatomy; background, checker, matte, or edge residue; text; logo; watermark.
```

The expression inserts were:

| Token | Intended expression insert |
|---|---|
| `happy` | HAPPY: a warm, genuine smile with a small clean glimpse of upper teeth, gently lifted cheeks, softened bright amber eyes, and relaxed brows. Pleased and open, not manic or childish. |
| `smug` | SMUG: half-lidded amber eyes, one subtly raised brow, and a small asymmetric one-corner smirk. Quiet self-satisfaction, not seduction. |
| `teasing` | TEASING: lively asymmetric eyes, one cocked brow, and a playful open grin with clean natural teeth. Friendly provocation, distinct from smug and not cartoonish. |
| `thinking` | THINKING: eyes looking slightly upward and aside, uneven contemplative brows, and a small closed pursed mouth. Analytical concentration, not worry. |
| `curious` | CURIOUS: attentive slightly widened amber eyes, gently raised brows, and a small softly parted mouth as if asking a follow-up question. Interested, not shocked. |
| `unamused` | UNAMUSED, the restrained "bruh" face: level half-lidded eyes, relaxed-low brows, and a straight closed mouth. Dry disbelief without anger. |
| `annoyed` | ANNOYED: narrowed eyes, mildly pinched brows, and a small tight frown. Irritated and impatient, clearly stronger than unamused but not furious. |
| `frustrated` | FRUSTRATED: eyes squeezed nearly shut, brows drawn hard inward with visible tension, and a strained open grimace as if suppressing an exasperated outburst. |
| `angry` | ANGRY: a sharp direct glare, strongly furrowed brows, and an open raised-voice mouth with clean natural teeth. Intense anger without monstrous distortion. |
| `sad` | SAD: downcast glossy amber eyes, gently raised inner brows, and a small closed downturned mouth. Quiet hurt with no tears yet. |
| `crying` | CRYING: clean visible tear streams from both glossy amber eyes, grief-raised inner brows, flushed lower eyelids, and a trembling open sobbing mouth. Emotional but anatomically clean. |
| `embarrassed` | EMBARRASSED: natural warm blush across both cheeks, eyes averted, uneven raised brows, and a small awkward closed smile. Flustered, not seductive. |
| `nervous` | NERVOUS: uneasy off-center gaze, asymmetric pinched brows, a tight wavering mouth, and one subtle sweat bead. Trying to keep composure, distinct from fear. |
| `worried` | WORRIED: slightly widened focused eyes, raised and pulled-together inner brows, and a small parted concerned frown. Sustained concern, not surprise. |
| `shocked` | SHOCKED: very wide amber eyes with small centered pupils, high brows, and a clean round open mouth. Sudden surprise with no tears or sweat. |
| `afraid` | AFRAID: tense wide amber eyes, raised inward-pinched brows, trembling parted lips, and one light sweat bead. Fear without full panic. |
| `panicked` | PANICKED: extremely wide eyes with tiny pupils, high pinched brows, several clean sweat beads, and one open strained gasp. Acute escalating panic with no comic blue shading. |
| `determined` | DETERMINED: steady amber eyes locked forward, firmly lowered brows, and a resolute closed mouth. Controlled focus, distinct from anger. |
| `empty` | EMPTY / DEAD-EYED: half-lidded unfocused amber eyes with dulled highlights, motionless brows, and a slack nearly neutral mouth. Emotion switched off, not supernatural horror. |
| `disgusted` | DISGUSTED: uneven narrowed side gaze, one raised brow and one pinched brow, a slight nose wrinkle, and a restrained curled upper lip. Revulsion, not anger or teasing. |

## Deterministic build

The built-in image-generation outputs are stored in the build-excluded
`game/assets/archive/asahiko_sprite_sources/` tree as one transparent anchor
and 20 full-canvas expression masters. Given that source layout, this command
normalises, builds, validates, and writes the production bank plus its review
sheet:

```text
python tools/build_mc_sprites.py --anchor game/assets/archive/asahiko_sprite_sources/anchor.png --master-dir game/assets/archive/asahiko_sprite_sources/masters --output-dir game/assets/characters/mc --review-sheet docs/assets/sprites/ASAHIKO_SPRITE_REVIEW.png
```

The checked-in [composite review sheet](ASAHIKO_SPRITE_REVIEW.png) shows the
canonical neutral followed by every alternate expression in declaration order.

The builder expects each master to be named
`expression_<token>.png`. It does not generate artwork. It writes
`neutral.png`, a transparent `face_neut.png`, the 20 `face_<token>.png`
overlays, and the optional 21-panel composited review sheet.

## Invariants

- Every production PNG is 1023x1537 RGBA and uses real transparency.
- `neutral.png` is the approved strict front-facing casual anchor; expressions
  never replace or reposition its body, outfit, hair silhouette, or canvas.
- `face_neut.png` is entirely transparent black, so `mc neut` is visually the
  canonical base and remains backward-compatible.
- Every alternate is a face-only overlay on the full canonical canvas. All 20
  alternates use the exact same softly feathered alpha mask.
- The shared mask stays within the canonical head silhouette. Its opaque core
  covers the changing brows, eyes, nose, cheeks, and mouth while its feather
  ends before the untouched hair and neck, preventing a visible oval seam.
- Fully transparent pixels contain zero RGB; no checker, matte color, halo,
  floor shadow, text, logo, or watermark reaches production.
- Every expression plate is pixel-distinct. A missing token, duplicate plate,
  wrong canvas, mismatched alpha mask, or dirty transparent RGB fails the
  builder's validation.
- Runtime sizing remains `fit "contain"` at `(640, 960)`, and `Flatten` is
  applied after composition so stage fades and alpha effects affect the sprite
  once rather than once per overlapping layer.
- Runtime paths are relative to `game/` and use only
  `assets/characters/mc/...`; the old angled sprite and generated masters are
  not runtime dependencies.
