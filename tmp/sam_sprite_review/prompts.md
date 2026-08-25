# Sam sprite generation prompt manifest

Mode: built-in image generation/editing. Expression and featureless masters used
`game/mod_assets/char_sprites/masayami/neutral.png` as the exact edit target.
Uniform poses used `neut_uniform.png`; casual poses used `neutral.png`.

## Shared expression prompt

Use case: identity-preserve. Asset type: Ren'Py visual-novel sprite master for
expression-layer extraction. Change only Sam's eyebrows, eyes, mouth, tears,
and minimal cheek shading needed by the named expression. Preserve the exact
identity, face shape, head angle, golden-blond hair, amber eyes, body, pose,
casual outfit, accessories, linework, palette, scale, 1023x1537 canvas,
placement, baseline, and framing. Keep all hair and limbs uncropped. Request a
genuine transparent background with clean alpha and no checkerboard, text,
watermark, border, extra objects, repainting, shifting, resizing, or chibi
distortion.

Expression-specific requests:

- `happy`: warm unguarded smile, softly closed smiling eyes, relaxed brows.
- `smug`: half-lidded eyes, subtly raised brow, small closed asymmetric smirk.
- `teasing`: gentle wink, bright open eye, raised brow, playful open smile.
- `thinking`: gaze up and aside, gently knit brows, contemplative closed mouth.
- `curious`: attentive widened eyes, uneven brows, barely parted lips.
- `unamused`: flat half-lidded "bruh" eyes, low level brows, straight mouth.
- `annoyed`: narrowed eyes, lowered brows, tight asymmetric frown.
- `frustrated`: tense brows, partly squeezed eyes, lightly clenched teeth.
- `angry`: direct glare, sharply furrowed brows, restrained open snarl.
- `sad`: lowered glossy eyes, raised inner brows, quiet downturned mouth.
- `crying`: wet reddened eyes, two tear tracks, pinched brows, trembling mouth.
- `embarrassed`: averted gaze, uneven tense brows, soft blush, awkward smile.
- `nervous`: slightly widened side glance, tense raised brows, uncertain smile.
- `worried`: inward-raised brows, concerned forward gaze, uneven frown.
- `shocked`: wide eyes, high brows, small natural gasp.
- `afraid`: wide glistening eyes, sharply raised inner brows, parted lips.
- `panicked`: very wide eyes, small tense pupils, pinched brows, ragged gasp.
- `determined`: steady focused gaze, resolved brows, firm closed mouth.
- `empty`: unfocused dead-eyed stare, flattened highlights, neutral mouth.
- `disgusted`: curled upper lip, side-pulled mouth, narrowed eyes, pinched brows.

## Featureless authoring plate

Use case: precise-object-edit. Remove only eyebrows, eyes, and mouth; replace
them with seamless surrounding facial skin while preserving the nose, face
contour, hair, anatomy, shading, and every non-feature detail. This is an
intermediate plate used to construct outfit-native bases and exact neutral
overlays, not a visible sprite.

## Shared pose prompt

Use case: identity-preserve. Asset type: finished full-body Ren'Py sprite pose.
Match the selected canonical outfit's identity, anatomy, polished anime
linework, painterly cel shading, fabric detail, palette, and accessories. Keep
the 1023x1537 stage scale, head height, bottom baseline, upper-thigh framing,
and safe top/side margins. Request clean real transparency with no checker,
halo, text, watermark, duplicate limbs, oversized hands, extreme
foreshortening, chibi proportions, or unrelated objects.

Pose-specific requests:

- `pose_open_hand_casual`: left hand in pocket; right hand extended palm-up in
  a relaxed "hear me out" gesture; warm, self-assured smile.
- `pose_crossed_uniform`: arms loosely folded; relaxed shoulders; subtle smug
  smile; hands and fingers naturally readable.
- `pose_thinking_uniform`: one arm across torso; opposite hand lightly at chin;
  sideward analytical gaze; quietly calculating, not worried.
- `pose_phone_casual`: left hand in pocket; right hand holds a slim unbranded
  phone at chest height; knowing glance toward the viewer.

The built-in generator returned opaque RGB masters containing a visible
transparency checker despite the alpha request. Those masters are review-only;
the production pipeline reconstructs clean alpha, decontaminates edges, and
extracts only registered expression features.
