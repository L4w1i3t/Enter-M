# Sam Sprite Rebuild Record

Date: 2026-08-26

This is the production contract for Sam Masayami's rebuilt expression bank and
alternate poses. All visible replacement art was generated fresh with the
built-in image-generation workflow. Earlier Sam expression decompositions,
featureless bases, `post_` assets, `old` assets, and prior pose iterations were
treated as obsolete and were not used as image-generation or pixel donors.

## Approved anchors and runtime design

Only these two existing sprites were used as identity, style, scale, and outfit
references:

- Casual: `game/assets/characters/masayami/neutral.png`
- Uniform: `game/assets/characters/masayami/neut_uniform.png`

Both are 1023x1537 RGBA images. The rebuilt runtime follows the same simple
base-plus-face design as Himeko: one intact neutral base for each outfit and one
shared, full-canvas `face_<token>.png` bank. The new neutral face is baked into
both bases, so `face_neut.png` is a fully transparent compatibility layer. No
featureless body, outfit-specific face bank, crop offset, or runtime alignment
transform participates in the layered image.

The bank exposes all 21 TODO tokens: `neut`, `happy`, `smug`, `teasing`,
`thinking`, `curious`, `unamused`, `annoyed`, `frustrated`, `angry`, `sad`,
`crying`, `embarrassed`, `nervous`, `worried`, `shocked`, `afraid`, `panicked`,
`determined`, `empty`, and `disgusted`.

## Neutral-generation prompt

The new canonical neutral was a fresh built-in identity-preserving edit using
the two approved anchors only. The working prompt was:

```text
Use case: identity-preserve
Asset type: full-canvas source render for a Ren'Py layered character sprite
Input images: Image 1 is Sam's canonical casual identity/style/scale target;
Image 2 is his canonical uniform identity/outfit reference.
Primary request: Replace only Sam's facial expression with a new restrained
neutral. Give him a very subtle closed-mouth smile with absolutely no visible
teeth. He should read as quietly confident and reserved, a cool/pretty boy who
does not need to perform confidence. His warm amber eyes must not quite match
the smile: keep them guarded, slightly tired or privately melancholy, so the
pleasant mouth and emotionally distant gaze create understated tension.
Style/medium: match the anchors' polished anime visual-novel sprite rendering,
line weight, palette, lighting, and soft cel shading exactly.
Composition/framing: preserve the exact pose, head angle, hair silhouette,
anatomy, scale, location, and 1023x1537 canvas.
Constraints: preserve Sam's identity, youthful proportions, tousled golden
blond hair, amber eyes, skin tone, accessories, clothing, and all non-face art.
Avoid: teeth; an open mouth; a broad grin; seductive or arrogant affect;
body/outfit/hair/camera/scale/crop changes; extra or duplicated facial
features; residue; text; watermark.
```

## Expression-generation prompt

Every non-neutral expression was a separate built-in edit. Image 1 was always
the freshly generated neutral master and was the sole edit target. The approved
casual and uniform anchors were included only as supporting identity, style,
outfit, and placement references. The shared prompt was:

```text
Use case: identity-preserve
Asset type: full-canvas source render for a Ren'Py layered character-expression sprite
Input images: Image 1 is the freshly generated canonical Sam edit target.
Images 2 and 3 are approved casual/uniform supporting references only.
Primary request: Change only Sam's face to <EXPRESSION INSERT>.
Style/medium: match Image 1's polished anime visual-novel linework, rendering,
palette, anatomy, and shading exactly.
Composition/framing: preserve Image 1's exact body pose, head angle, hair,
silhouette, scale, stage location, and 1023x1537 portrait canvas.
Constraints: preserve exact identity, golden-blond hair, amber eyes, skin tone,
outfit, lighting, and all non-face pixels. Change only brows, eyes, mouth, and
small expression-specific cheek, tear, or sweat details explicitly requested.
Avoid: body/outfit/hair/camera/scale/crop changes; extra or duplicated eyes,
brows, mouths, teeth, tears, or sweat; warped anatomy; black, white, or checker
residue in the face; text; logos; watermark.
```

The final expression inserts were:

| Token | Final insert |
|---|---|
| `happy` | HAPPY: a warm, natural broader smile with a small clean glimpse of upper teeth, gently lifted cheeks, softened amber eyes, and relaxed brows. Genuine pleasure, not manic excitement. |
| `smug` | SMUG: half-lidded amber eyes, one subtly raised brow, and a small asymmetric one-corner smirk. Quietly self-satisfied cool-boy confidence, not seduction. |
| `teasing` | TEASING: playful asymmetric eyes, a cocked brow, and a light mischievous tooth-showing grin. Friendly provocation, distinct from smug and not cartoonish. |
| `thinking` | THINKING: gaze angled slightly upward and aside, uneven contemplative brows, and a closed pursed mouth. Focused reflection, not worry. |
| `curious` | CURIOUS: attentive slightly widened amber eyes, gently raised brows, and a small toothless parted mouth as if asking a follow-up question. Interested, not shocked. |
| `unamused` | UNAMUSED, the restrained "bruh" face: lowered half-lidded eyes, level brows, and a straight closed mouth. Dry disbelief without anger. |
| `annoyed` | ANNOYED: a narrowed side-eye, mildly pinched brows, and a small pressed off-center mouth. Irritated and impatient, but controlled. |
| `frustrated` | FRUSTRATED: tightly knit inner brows, strained eyes, and a tense slightly parted mouth as if holding back an exasperated response. |
| `angry` | ANGRY: a hard direct glare, sharply lowered brows, and a controlled clean snarl. Intense anger without monstrous distortion. |
| `sad` | SAD: downcast softened amber eyes, raised inner brows, and a small closed frown. Quiet hurt with no tears yet. |
| `crying` | CRYING: natural clean tear streams from both eyes, grief-raised inner brows, raw lower eyelids, and a restrained sobbing mouth. Emotional but anatomically clean. |
| `embarrassed` | EMBARRASSED: natural blush, averted eyes, uneven raised brows, and a sheepish closed half-smile. Flustered, not seductive. |
| `nervous` | NERVOUS: uneasy off-center gaze, asymmetric pinched brows, a tight wavering mouth, and one subtle sweat bead. Trying to keep composure. |
| `worried` | WORRIED: slightly widened soft eyes, raised and pulled-together inner brows, and a small parted frown. Sustained concern, not surprise. |
| `shocked` | SHOCKED: very wide amber eyes with small centered pupils, high brows, and a small clean open mouth. Sudden surprise with no sweat. |
| `afraid` | AFRAID: tense wide eyes, inward-pinched raised brows, trembling parted lips, and one light sweat bead. Fear without full panic. |
| `panicked` | PANICKED: extremely wide eyes with tiny pupils, high pinched brows, several clean sweat beads, and one open strained gasp. Acute panic, with no comic blue shading. |
| `determined` | DETERMINED: direct focused amber eyes, firmly lowered brows, and a resolute closed mouth. Controlled resolve, distinct from anger. |
| `empty` | EMPTY / DEAD-EYED: half-lidded unfocused amber eyes with dulled highlights, still brows, and a slack nearly neutral mouth. Emotion switched off, not supernatural horror. |
| `disgusted` | DISGUSTED: uneven narrowed side gaze, one raised brow and one pinched brow, a slight nose wrinkle, and a restrained curled upper lip. Revulsion, not anger. |

## Alternate-pose generation prompt

Each pose was generated fresh with the rebuilt neutral sprite as the principal
identity/style/scale reference and the matching approved outfit as support.
The shared prompt was:

```text
Use case: identity-preserve
Asset type: alternate full-body Ren'Py visual-novel character sprite
Primary request: Redraw Sam in this alternate pose: <POSE INSERT>.
Character direction: retain his cool/pretty-boy shtick: relaxed, self-possessed,
subtle, and attractive without becoming seductive or fashion-model theatrical.
Style/medium: match the canonical sprite's polished anime visual-novel linework,
rendering, proportions, palette, and shading exactly.
Composition/framing: exact 1023x1537 portrait canvas; same apparent head size,
body scale, top placement, and lower-body crop as the matching neutral outfit.
Constraints: preserve Sam's golden-blond hair, amber eyes, face, skin tone,
outfit, necklace and bracelets where visible, coherent anatomy, and five natural
fingers per visible hand. Keep all extended silhouette parts inside the canvas.
Avoid: oversized head/body; zoom or crop changes; extra/fused limbs or fingers;
duplicate features or props; warped clothing; text; logos; watermark.
```

The pose inserts were:

- `pose_open_hand_casual`: One hand rests casually in his jeans pocket while
  the other extends in a relaxed open-palm conversational gesture. Shoulders
  loose, restrained closed smile, composed and approachable.
- `pose_crossed_uniform`: Arms crossed naturally over the school blazer, weight
  settled comfortably, chin level, and a small reserved confident expression.
- `pose_thinking_uniform`: One hand rests at his chin while the other supports
  that elbow; gaze shifts slightly aside in quiet consideration. Introspective,
  elegant, and restrained.
- `pose_phone_casual`: One hand rests in his jeans pocket while the other holds
  one dark unbranded smartphone; eyes angle down at the screen with an easy,
  private half-smile. Exactly one phone and two coherent hands.

The first pose renders used a flat magenta background for silhouette
development. Identity-preserving cleanup edits first removed that color against
a neutral checker review source, then placed the approved character on a flat
`#00FF00` final extraction matte. `tools/build_sam_poses.py` keys those final
green masters, replaces transition RGB with verified interior character color,
and produces real straight-alpha RGBA. Neither the magenta/checker intermediates
nor any chroma pixels are copied into production.

## Deterministic processing and validation

`tools/build_sam_faces.py` performs the face build:

1. Builds one fixed, soft full-canvas face mask inside both canonical outfit
   silhouettes.
2. Bakes the newly generated neutral face into both intact neutral outfit bases.
3. Exports one shared 1023x1537 RGBA overlay per alternate expression and an
   empty `face_neut.png`.
4. Zeros RGB under every zero-alpha pixel.

`tools/build_sam_poses.py` extracts and registers the fresh alternate poses.
`tools/validate_sam_sprites.py` enforces the runtime file contract and generates
dark, light, and checker review sheets for both outfits and every pose.

Production files live under
`game/assets/characters/masayami/`. Runtime wiring is in
`game/asset_definitions/def_characters.rpy`.
