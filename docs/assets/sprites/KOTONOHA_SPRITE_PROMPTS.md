# Kotonoha Sprite Rebuild Authoring Record

Date: 2026-08-25

This is the clean-room production record for Kotonoha's normal visual-novel
sprite set. The rebuilt runtime contract follows the same broad structure as
Himeko, Matsuda, and Tsubaki: one intact canonical base for each outfit, plus
one outfit-conditioned face layer selected by the layered image. Alternate
poses are standalone sprites because their arms and silhouettes change.

Kotonoha is reserved, but she is not shy. Her story dialogue is concise,
literal, observant, and practical; she notices where cars are, straightens
small irregularities, folds a receipt exactly down the middle, and generally
answers with a nod or a small bow. Her character stories also establish the
more unsettling side of that restraint: she watches closely, reproduces forms
precisely, and often seems to have more happening behind her eyes than reaches
her face. Accordingly, the expression bank uses small changes in gaze, brows,
eyelids, and mouth tension. Even the extreme tokens are controlled breaks in
composure rather than the cast's usual broad anime reactions. Embarrassment
and nervousness must never be drawn as coyness, meekness, or bashful shyness.

## Clean-room source boundary

Only these two pre-existing Kotonoha sprites are canonical sources for this
rebuild:

| Role | Canonical file | Geometry | SHA-256 |
|---|---|---:|---|
| Casual base and primary identity/style/expression anchor | `game/assets/characters/kotonoha/neutral.png` | 1023x1537 RGBA | `3cc12dcd7bd018724a7232fe8aeaef505e312f7117b80f284c1b4719ba6a866b` |
| Work base and matching-outfit pose anchor | `game/assets/characters/kotonoha/work.png` | 1023x1537 RGBA | `72bc79cc551f8895ae66e94aacd551f01dfd7d6e74d35c59863132c0841d889c` |

Both bases retain their original transparent canvas, character placement,
hair, anatomy, outfit design, shading, and neutral face. They are the only
approved identity, palette, registration, and style references. The casual
base supplies the common facial design; processing conditions each exported
face patch against its actual casual or work base.

The following boss-mode art is explicitly outside this source boundary and
was not used as an image-generation input, face donor, identity reference,
style reference, registration target, color source, or processing input:

| Rejected artifact | SHA-256 | Reason |
|---|---|---|
| `game/addons/Matsuda's Sick Boss Fight/kotonohamode/kotoboss_sheet.png` | `0ddd0eaa25799849471e4b476ae79d7994b2e60b50828108e8b4e94c3508a6da` | Purpose-built, quantized 128px-cell pixel-art atlas, not visual-novel sprite art. |
| `game/addons/Matsuda's Sick Boss Fight/kotonohamode/archive/kotobosssprite_legacy.png` | `14946e87c7d297517ebd507827e3c000eba607214ac5ced7fed3c004b3141226` | Obsolete legacy boss still. |
| `docs/archive/kototouhou/kotoboss_sheet_imagegen_source.png` | `8c13d3a1d674cb62feaf24db7222e2e3c8bd009b79bf544ebecc5580ee14f5c1f` | Generated source for the unrelated boss atlas. |

No checker-backed face from another character, no old Kotonoha expression or
pose, and no previous sprite experiment was reused. The three current-turn
`pose_small_bow_casual*` drafts were also rejected: they are not production
inputs and are not runtime assets. This document and the selected masters
below supersede every earlier Kotonoha normal-sprite iteration.

## Generation mode and authoring masters

All new art was made with the image-generation skill's default **built-in
image generator**. The API/CLI fallback was not used, no `OPENAI_API_KEY` was
required, and the service did not expose a backend model version. Each
expression or pose was a separate built-in identity-preserving edit/generation
call; a multi-output `n` request was not used as a substitute for individually
specified assets.

The selected opaque RGB authoring masters live under:

`tmp/kotonoha_sprite_build/masters/`

The generator was asked for a flat saturated magenta production-key backdrop.
Magenta was chosen because it is far from Kotonoha's lavender hair, violet
eyes/skirt, gray sweater, black apron/trousers, and skin. It is an authoring
screen, not transparency and never runtime content. Generated magenta is not
assumed to be one mathematically exact RGB value; the deterministic processor
recognizes the screen as a chroma field, reconstructs clean edge colors, and
exports real RGBA. A synthetic checker is used only behind finished RGBA in QA
review sheets. Neither the magenta screen nor a checker pattern is copied into
a production PNG.

There are 20 selected expression masters named
`expression_<token>.png`. Neutral was not regenerated. There are three
selected pose masters:

- `pose_exact_fold_work.png`
- `pose_watching_casual.png`
- `pose_open_hands_casual.png`

## Common expression prompt

The built-in generator was called once for each non-neutral expression. Image
1 was the approved casual neutral sprite and the sole identity, style,
composition, and texture anchor. The following is the production prompt
specification reconstructed from the operative built-in calls, not a verbatim
API/tool-call log. It faithfully preserves the instructions and constraints;
only line wrapping and non-operative phrasing varied between calls:

```text
Use case: identity-preserve
Asset type: Ren'Py visual-novel character-sprite expression master for later
face-patch extraction
Input images: Image 1 is the edit target and sole identity, style, palette,
texture, anatomy, and composition reference: Kotonoha's canonical casual
neutral sprite.
Primary request: Change only Kotonoha's facial expression to [DIRECTIVE]. She
has a reserved, low-affect demeanor, not a shy demeanor. Make the emotion
readable through restrained changes to her gaze, eyelids, eyebrows, and small
mouth; do not give her another character's broad theatrical reaction.
Scene/backdrop: replace the transparent exterior with a flat saturated magenta
production-key screen, uniform and untextured.
Style/medium: preserve Image 1's polished matte 2D anime visual-novel sprite
rendering, identity, facial proportions, lavender hair and braid, purple eyes,
line weight, palette, soft shading, and non-glossy texture.
Composition/framing: preserve the same portrait canvas and the same
mid-thigh-and-up framing, character scale, head angle, head location, silhouette, and
bottom alignment. Do not turn this into a full-body shot.
Constraints: keep her hair, head, skin tone, gray ribbed turtleneck, purple
pleated skirt, body, hands, pose, lighting, and every non-face feature fixed.
Keep exactly one clean, anatomically coherent face whose brows, eyes, irises,
and mouth remain registered for later overlay extraction.
Avoid: transparency checkerboard, checker/grid texture anywhere, black, white,
or magenta residue on the character, crop or shift, full-body framing, blur,
jagged edges, glossy/plastic shading, identity drift, altered hair or outfit,
garbled/doubled facial features, extra objects, text, logo, or watermark.
```

## Runtime expression directions

The following table is both the generation directive set and the semantic
contract for writers. The low-amplitude direction is intentional. A token may
be visually subtle, but it must remain distinguishable from `neut` and from
its neighboring emotions after compositing over either outfit.

| Requested emotion | Runtime token | Kotonoha-specific directive |
|---|---|---|
| Neutral | `neut` | Use the exact face already present in the applicable canonical base: composed posture, attentive eyes, and the faint polite micro-smile. No generated neutral redraw. |
| Happy | `happy` | Quiet, sincere happiness: gently softened eyes and a small closed-mouth smile. No broad grin, shut-eye laugh, or bouncing cheer. |
| Smug | `smug` | Restrained self-satisfaction: slightly lowered lids, one brow only subtly higher, and a tiny knowing smile. |
| Teasing | `teasing` | Dry, gentle teasing: a faint sideward look and a very small asymmetric smile. No wink, tongue, open-mouthed grin, or coy flirtation. |
| Thinking | `thinking` | Quiet calculation: eyes turned slightly aside, one brow barely raised, and a compact neutral mouth, as though she is processing a detail before answering. |
| Curious | `curious` | Attentive curiosity: eyes a little wider and lips just parted. Interested and analytical, not childishly excited. |
| Unamused | `unamused` | The requested "bruh" face at Kotonoha's amplitude: heavy half-lidded direct stare, level brows, and a tiny flat mouth. |
| Annoyed | `annoyed` | Contained irritation: brows drawn inward, eyes slightly narrowed, and a small firm frown. No yelling or puffed cheeks. |
| Frustrated | `frustrated` | Restraint starting to strain: tighter brows and eye corners with a compressed mouth. More pressure than `annoyed`, but not an outburst. |
| Angry | `angry` | Cold, controlled anger: hard direct gaze, sharply lowered brows, and a small tight frown. Mouth closed; no screaming rage. |
| Sad | `sad` | Quiet sadness: raised inner brows, softened downcast eyes, and a slight downturn of the mouth. No melodramatic collapse. |
| Crying | `crying` | Silent, restrained crying: visible tears from both eyes, wet distressed gaze, and a small unsteady mouth held against a sob. No wailing face. |
| Embarrassed | `embarrassed` | Composure disturbed by being seen: eyes averted, a mild natural blush, and a tiny awkward smile. Not shy, helpless, bashful, or coy. |
| Nervous | `nervous` | Quiet unease: sideways checking glance, slightly uneven worried brows, and a small tense attempt at composure. Not a shy-girl expression. |
| Worried | `worried` | Controlled concern for something external: raised inner brows, focused open eyes, and lips barely parted as if about to give a practical warning. |
| Shocked | `shocked` | A brief visible break in composure: widened eyes, high brows, and a small round mouth. Surprise, not yet fear or screaming. |
| Afraid | `afraid` | Fear held in place: wide tense eyes, distressed inner brows, and a small parted mouth. No flailing, tears, or comic terror. |
| Panicked | `panicked` | The strongest permitted loss of control: very wide eyes with contracted pupils, tightly raised brows, and a tense small open mouth. Still anatomically clean and non-comedic. |
| Determined | `determined` | Calm resolve: a direct steady gaze, slightly lowered set brows, and a firm level mouth. Focused, not angry. |
| Empty/Dead-eyed | `empty` | Truly affectless and uncanny: unfocused half-lidded eyes, slack level brows, and a tiny flat mouth, as though watched from behind glass. Not merely tired or unamused. |
| Disgusted | `disgusted` | Suppressed distaste: gaze turned slightly aside, one brow pinched higher, and the smallest asymmetric upper-lip curl. No gagging or broad grimace. |

## Common alternate-pose prompt

Each selected pose was a separate built-in identity-preserving call using only
the matching canonical outfit sprite as its identity, clothing, rendering,
and palette anchor. As above, this is the faithful production specification of
the operative prompts rather than a verbatim API/tool-call transcript:

```text
Use case: identity-preserve
Asset type: standalone mid-thigh-and-up Ren'Py visual-novel character pose
Input images: Image 1 is the sole approved identity, style, palette, anatomy,
outfit, and spatial reference: Kotonoha's matching canonical [CASUAL/WORK]
sprite.
Primary request: [POSE DIRECTIVE]
Subject direction: Kotonoha is reserved rather than shy. The action should be
small, deliberate, observant, and economical; emotion is carried by posture,
hands, and a restrained face, never by theatrical body language.
Style/medium: preserve the canonical sprite's exact polished matte 2D anime
rendering, recognizable face, long wavy lavender hair and braid, purple eyes,
line weight, palette, restrained highlights, and non-glossy texture.
Composition/framing: portrait canvas, centered and framed only from the head to
mid-thigh. Match the canonical sprite's apparent character scale, head height,
and bottom alignment. Keep the complete visible silhouette and both hands in
frame. Do not show knees, calves, shoes, or a complete body.
Scene/backdrop: perfectly flat saturated magenta production-key screen,
uniform and untextured.
Constraints: preserve the exact requested outfit. Use exactly two anatomically
coherent arms and two hands with clean fingers. Keep the gesture readable at
Ren'Py display scale.
Avoid: full-body shot, feet, lower-leg framing, transparency checkerboard,
checker/grid texture, magenta/black/white residue, crop through a hand or hair,
glossy/plastic shading, malformed or extra fingers/limbs, identity or outfit
drift, unrequested props or effects, text, logo, or watermark.
```

The built-in generator occasionally returned more lower body than requested.
That excess canvas is not an authorization for full-body runtime art: the
deterministic pose normalizer enforces the canonical mid-thigh-and-up frame.

| Runtime image name | Selected master and operative pose directive |
|---|---|
| `kotonoha work pose_exact_fold` | `pose_exact_fold_work.png`: in her exact work uniform, hold one narrow customer receipt in both hands and fold it once, precisely down the middle; hands close together at the lower chest/upper waist, posture upright, face calm and professionally pleasant. The paper is the only prop. This is the visual counterpart to her established exact receipt-folding habit. |
| `kotonoha casual pose_watching` | `pose_watching_casual.png`: an observant, evaluating stance with one forearm crossing low to support the opposite elbow, fingertips of the raised hand resting lightly near her chin, and her gaze turned just off-camera as she notices a detail. Analytical and self-contained, not bashful or coquettish. |
| `kotonoha casual pose_open_hands` | `pose_open_hands_casual.png`: a rare moment of restrained uncertainty or honest vulnerability, both forearms held low and slightly forward with palms open; small worried face, shoulders quiet. It is not a broad shrug, plea, apology pose, or shy retreat. |

No alternate pose is a full-body shot. All three runtime files use the same
1023x1537 transparent production canvas and the same mid-thigh-and-up stage
envelope as the canonical sprites.

## Deterministic processing and 42-layer contract

Image generation is stochastic; all work after the selected masters is
deterministic. The production builder:

1. verifies both canonical SHA-256 values and an exact allowlist containing
   only the 20 selected expression masters and three selected pose masters;
2. identifies each expression master's saturated-magenta field from its four
   corners and rejects an implausible background fraction;
3. uses lavender-hair-only SIFT features and RANSAC similarity registration,
   rather than changeable eyes or mouths, to register every expression master
   to casual and to measure the one canonical casual-to-work head transform;
4. applies one connected 256-level face mask per outfit. The casual mask is a
   fixed facial-plane polygon with a 5.75-pixel Gaussian feather; the work mask
   is its measured registered counterpart. An expanded eye/brow envelope and
   the nose/mouth envelopes are forced opaque so no neutral feature can show
   through beside a raised, lowered, or angled replacement feature;
5. median-matches stable facial-skin samples independently to each canonical
   outfit and repairs any magenta that reaches the mask. Canonical lavender
   detail is restored only from connected hair regions of at least 1,000
   pixels; the much smaller lavender eyebrow and iris islands are explicitly
   excluded so the neutral face cannot be painted back over an alternate;
6. exports 21 full-canvas RGBA face layers for `casual` and the same 21 for
   `work`, for exactly 42 outfit-conditioned files; the two `neut` layers are
   intentionally transparent compatibility layers because each base already
   contains its exact neutral face;
7. chroma-keys each pose, measures its two purple irises against the matching
   canonical base, applies a premultiplied-Lanczos similarity transform, then
   performs final fringe and detached-component cleanup. The result must meet
   the 1023x1537 canonical canvas at the mid-thigh stage baseline without
   touching the top or side edges; and
8. writes input/output hashes, transforms, mask/geometry metrics, and expression,
   head, and pose sheets over light, dark, gray, green, and synthetic-checker
   backgrounds. Checker is a review background only.

The first generated expression pass was rejected after runtime review exposed
double-brow and lash artifacts. Every non-neutral master was regenerated from
the canonical neutral sprite as a complete face-feature replacement, and the
current production set supersedes that pass. Registered expression plates use
bilinear resampling to avoid high-contrast ringing around thin brow and lash
lines.

Production face-layer paths are:

`game/assets/characters/kotonoha/face_<token>_<outfit>.png`

where `<outfit>` is `casual` or `work` and `<token>` is one of the 21 tokens in
the table above. Production pose paths are:

- `game/assets/characters/kotonoha/pose_exact_fold_work.png`
- `game/assets/characters/kotonoha/pose_watching_casual.png`
- `game/assets/characters/kotonoha/pose_open_hands_casual.png`

## Runtime names and validation commands

The normal layered-image syntax is:

- `kotonoha casual <expression>`; `casual` is the default outfit and may be
  omitted, preserving existing calls such as `show kotonoha neut`;
- `kotonoha work <expression>`, preserving existing calls such as
  `show kotonoha work neut`.

The standalone pose image names are exactly:

- `kotonoha work pose_exact_fold`
- `kotonoha casual pose_watching`
- `kotonoha casual pose_open_hands`

Build, install/runtime-wire, validate, and produce isolated Ren'Py review
renders with:

```text
python tools/build_kotonoha_sprites.py
python tools/build_kotonoha_sprites.py --install
python tools/validate_kotonoha_sprites.py
python tools/build_kotonoha_render_probe.py
python tools/build_kotonoha_render_probe.py --run
```

The first builder command stages assets and review sheets without touching
production. `--install` performs file-by-file atomic replacement of the exact
42-face/three-pose manifest after a successful build. Detailed source hashes,
registration matrices, mask statistics, pose normalization, cleanup metrics,
and review hashes are recorded in
`tmp/kotonoha_sprite_build/build_metrics.json`; deterministic review sheets
are under `tmp/kotonoha_sprite_build/review/`. The render probe uses an
isolated project under `tmp/kotonoha_render_probe_project/` and writes verified
captures, review sheets, `source_metrics.json`, and `render_metrics.json` under
`tmp/kotonoha_render_probe/`.

Validation must cover the two canonical bases, all 42 expected face layers,
all 42 outfit/token composites, all three pose files, exact runtime wiring,
1023x1537 RGBA geometry, transparent-pixel RGB hygiene, expression
distinctness, face registration, mid-thigh framing, clean hands/anatomy, and
absence of magenta, black, white, or periodic checker residue on light, dark,
and checker review backgrounds.
