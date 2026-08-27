# Asahina Sprite Rebuild Record

Date: 2026-08-25

This is the production contract for Asahina's rebuilt expression bank and four
uniform alternate poses. All visible art was generated fresh with the built-in
image-generation tool. Earlier Asahina face decompositions, expression layers,
and pose renders were treated as obsolete and were not used as generation or
pixel donors.

## Approved anchors and runtime design

Only these two existing sprites were used as identity/style anchors and intact
runtime bases:

- Casual: `game/assets/characters/asahina/neutral.png`
- Uniform: `game/assets/characters/asahina/neut_uniform.png`

Both are 1023x1537 RGBA images. The layered image now places a shared,
full-replacement face plate over one of those intact neutral bases. The neutral
plate is transparent because each base already contains its neutral face. No
featureless-body asset participates in the runtime.

The normal bank exposes all 21 TODO tokens: `neut`, `happy`, `smug`, `teasing`,
`thinking`, `curious`, `unamused`, `annoyed`, `frustrated`, `angry`, `sad`,
`crying`, `embarrassed`, `nervous`, `worried`, `shocked`, `afraid`, `panicked`,
`determined`, `empty`, and `disgusted`.

## Expression-generation prompt

Each non-neutral expression was a separate built-in identity-preserving edit of
`neut_uniform.png`. The shared prompt was:

```text
Use case: identity-preserve
Asset type: full-canvas source render for a Ren'Py layered character-expression sprite
Input images: Image 1 is the canonical edit target for Asahina.
Primary request: Change only Asahina's face to <EXPRESSION INSERT>.
Style/medium: match Image 1's polished anime visual-novel sprite rendering exactly.
Composition/framing: preserve the exact crossed-arm pose, head angle, silhouette, scale, location, and 1023x1537 portrait canvas.
Constraints: preserve exact identity, sixteen-year-old athletic proportions, blue eye color, dark chestnut hair and bangs with two barrettes, uniform, lighting, line weight, palette, and shading. Change only eyes, eyebrows, mouth, and expression-related cheek shading or a tiny conventional sweat/tear detail if explicitly required.
Avoid: body/outfit/hair/camera/scale/crop/pose changes; adult-coded styling; extra or duplicated facial features, fingers, limbs, or accessories; facial distortion; text; watermark. Background may be plain because only the registered face region will be used.
```

The expression inserts were:

| Token | Final insert |
|---|---|
| `happy` | HAPPY: a clearly genuine open smile with a small glimpse of upper teeth, relaxed lifted cheeks, softened bright-blue eyes, and gently raised relaxed brows. Warm and pleased, but still recognizably confident and not childish. |
| `smug` | SMUG: one brow subtly raised, half-lidded bright-blue eyes aimed toward the viewer, and a small self-satisfied asymmetric closed-mouth smirk. She is a bold, prickly sixteen-year-old showing competitive older-sister-style swagger, not seduction. |
| `teasing` | TEASING: a playful one-eye wink, one brow cocked, and a small mischievous open grin. Bold sisterly ribbing, not seductive and not cutesy. |
| `thinking` | THINKING: eyes looking slightly upward and to the side, one brow raised and the other mildly knit, lips closed and pursed off-center in concentration. Reflective and skeptical, not worried. |
| `curious` | CURIOUS: attentive slightly widened bright-blue eyes, gently lifted brows, and a small softly parted mouth as if asking a follow-up question. Interested and alert, not shocked. |
| `unamused` | UNAMUSED, the dry "bruh" face: both eyes distinctly half-lidded in a level deadpan stare toward the viewer, relaxed-low brows, and a perfectly flat closed mouth. Comedic disbelief without anger. |
| `annoyed` | ANNOYED: narrowed sideways-looking eyes, mildly pinched inward brows, and a small tight off-center frown. Irritated and impatient, clearly stronger than unamused but not furious. |
| `frustrated` | FRUSTRATED: eyes squeezed mostly shut, brows drawn hard inward and upward with visible tension, and a clenched wavy grimace as though suppressing an exasperated outburst. No pose change. |
| `angry` | ANGRY: a sharp direct glare, strongly furrowed brows, and an open raised-voice mouth with natural teeth visible. Intense teenage anger, not horror and not a monstrous transformation. |
| `sad` | SAD: downcast glossy blue eyes, inner brows gently raised, and a small closed downturned mouth. Quietly hurt and trying to hold composure; no tears yet. |
| `crying` | CRYING: clearly visible clean tear streams from both glossy blue eyes, inner brows raised in grief, flushed lower eyelids, and a trembling open sobbing mouth. Emotional but anatomically clean, with exactly two eyes and one mouth. |
| `embarrassed` | EMBARRASSED: strong natural pink blush across both cheeks and faintly pink ears, eyes averted to the side, brows raised unevenly, and a small tight awkward smile. Flustered by attention, not seductive. |
| `nervous` | NERVOUS: uneasy side glance, asymmetrically raised pinched brows, a small strained wavering smile, and one subtle sweat bead near the temple. Trying to play it cool, distinct from fear. |
| `worried` | WORRIED: eyes focused forward and slightly widened, inner brows lifted and pulled together, and lips softly parted in a small concerned frown. Sustained concern, not surprise and not panic. |
| `shocked` | SHOCKED: both blue eyes opened very wide with normal centered pupils, brows high, and a clean round open mouth. Sudden surprise, no tears, no sweat, and no fear shading. |
| `afraid` | AFRAID: wide tense blue eyes with slightly contracted pupils, brows raised and sharply pinched inward, a small trembling parted mouth, and very light sweat. She looks half-paralyzed and wants to back away, not screaming. |
| `panicked` | PANICKED: extremely wide blue eyes with tiny pupils, brows arched high and pinched, several clean sweat beads, flushed tension, and one open strained gasp. Acute escalating panic, more intense than afraid, but no blue-face comic shading. |
| `determined` | DETERMINED: steady intense blue eyes locked forward, brows lowered in firm focus, and a resolute closed mouth with the faintest confident set. Controlled resolve, not anger. |
| `empty` | EMPTY / DEAD-EYED: unfocused flat forward stare, blue irises visibly dulled and desaturated with highlights nearly absent, relaxed motionless brows, and a small blank neutral mouth. Emotion abruptly switched off; eerie but not supernatural, injured, or crying. |
| `disgusted` | DISGUSTED: eyes narrowed unevenly and looking slightly aside, one brow raised while the other pinches down, a subtly wrinkled nose, and an asymmetric curled upper lip. Clear revulsion, not anger and not playful teasing. |

## Alternate-pose generation prompt

Each pose was a separate built-in generation using `neut_uniform.png` as the
identity, style, uniform, scale, and placement reference. The shared prompt was:

```text
Use case: identity-preserve
Asset type: alternate full-body Ren'Py visual-novel character sprite
Input images: Image 1 is the canonical Asahina uniform sprite and identity/style/scale reference.
Primary request: Redraw Asahina in this alternate pose: <POSE INSERT>
Scene/backdrop: perfectly flat solid chroma-key green (#00FF00), edge-to-edge; no checkerboard, gradient, glow, texture, vignette, floor, or shadow.
Style/medium: match Image 1's polished anime visual-novel sprite linework, rendering, palette, anatomy, and shading exactly.
Composition/framing: same 1023x1537 portrait canvas, same stage placement and bottom crop at mid-thigh, same head size and overall character scale as Image 1. Center the resting body on the same axis; leave transparent-intended margin around all extended silhouette parts.
Constraints: preserve Asahina's exact sixteen-year-old identity, athletic proportions, fair skin, bright blue eyes, shoulder-length dark chestnut hair and bangs with two dark barrettes at her left temple (viewer-right), taupe-gray blazer with gold buttons, copper/orange diamond-knit sweater vest, white collared shirt, thin red ribbon bow, and navy pleated skirt. All anatomy and clothing must be coherent and clean.
Avoid: enlarged head/body, zoomed-in crop, top/side clipping, adult-coded styling, sexualized pose, extra or missing fingers/limbs, fused hands, duplicate phone or features, warped uniform details, black/white/checkerboard background, residue, text, logos, watermark.
```

The pose inserts were:

- `pose_hairflip_uniform`: Leaning back only slightly while flipping a lock of
  her shoulder-length hair with one hand; her other hand rests naturally on her
  hip. She wears a clear self-satisfied, smugly arrogant expression with
  half-lidded blue eyes and a small smirk. The gesture is confident competitive
  swagger, not seductive. Keep her head, torso, and legs the exact same apparent
  size as the canonical sprite; the extended arm/hair may widen the silhouette,
  but do not enlarge the character.
- `pose_pointing_uniform`: Pointing one index finger directly toward the camera
  with controlled foreshortening while raising her voice; her other hand is
  planted on her hip. She has a sharp angry/commanding expression and open
  speaking mouth. The visible pointing hand must have exactly five anatomically
  coherent fingers and remain fully inside the canvas. Keep her head, torso,
  and legs the exact same apparent size as the canonical sprite; do not enlarge
  the character.
- `pose_eyeroll_uniform`: Tilting her head slightly back and rolling both eyes
  upward with a dry, exasperated expression and small flat frown. One hand rests
  on her hip while the other arm hangs naturally at her side. Keep the pose
  restrained and sarcastic. Keep her head, torso, and legs the exact same
  apparent size as the canonical sprite; do not enlarge the character.
- `pose_phone_panic_uniform`: Looking down at one modern unbranded smartphone
  held in both hands, on the verge of an anxiety attack and almost fainting. Her
  posture is tense and slightly collapsed, shoulders raised; her face is pale
  with wide tiny-pupil blue eyes, pinched brows, sweat, and a strained half-open
  mouth. Exactly one phone, exactly two hands, five coherent fingers per hand.
  Keep her head, torso, and legs the exact same apparent size as the canonical
  sprite; do not enlarge the character.

## Deterministic processing and validation

`tools/build_asahina_sprites.py` performs every post-generation operation:

1. Registers each expression master to stable canonical hair/head edges while
   excluding the changing face region.
2. Exports one fixed, softly feathered 1023x1537 replacement mask for every
   non-neutral expression. Its opaque center fully covers the original eyes,
   brows, and mouth; its alpha is safe over both intact outfit bases.
3. Zeros RGB under zero alpha and produces casual/uniform review sheets on
   checker, light, and dark backgrounds.
4. Converts pose chroma mattes to real straight-alpha RGBA, expands clean
   opaque edge colors through the partial-alpha rim, and suppresses generated
   green spill. No chroma or checker pixels are copied into production.
5. Validates dimensions, mode, fixed face-mask identity, transparent-pixel RGB,
   pose margins, chroma residue, and the `terror.png` compatibility copy before
   installation.

Build, review, validate, and install with:

```text
python tools/build_asahina_sprites.py contact
python tools/build_asahina_sprites.py build
python tools/build_asahina_sprites.py review
python tools/build_asahina_sprites.py validate
python tools/build_asahina_sprites.py install
python tools/build_asahina_sprites.py validate-installed
```

Production files live under
`game/assets/characters/asahina/`. Runtime wiring remains in
`game/asset_definitions/def_characters.rpy`; `asahina uniform terror` is preserved as
an image-name alias to `pose_phone_panic_uniform.png`.
