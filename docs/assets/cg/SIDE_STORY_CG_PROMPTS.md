# Side-Story Completion CG Production Prompts

This document records the 2026-08-27 completion rewards for the two Kotonoha
stories, **Hina's World**, and the paired **Heads / Tails** stories. The five
finals were revised after continuity and composition review, generated with the
built-in image-generation tool, and normalized from 1672x941 RGB sources to the
project's native 1280x720 CG canvas. **Purgatorium** was deliberately left
untouched; **Dead Fantasy** now has its own production record in
`DEAD_FANTASY_ART_PRODUCTION.md`.

## Runtime integration

| Story completion | Gallery title | Final file |
| --- | --- | --- |
| The Girl with Every Face | No One Lived There | `game/assets/cg/kotonoha_every_face.png` |
| The Void Hunter | Open Hands | `game/assets/cg/kotonoha_void_hunter.png` |
| Hina's World | Hina's World | `game/assets/cg/hinas_world.png` |
| Tails (paired reward 1) | What I Keep | `game/assets/cg/heads_what_i_keep.png` |
| Tails (paired reward 2) | What She Kept | `game/assets/cg/tails_what_she_kept.png` |

The first three unlock only at their respective real completion paths. Both
gothic CGs unlock together when **Tails** is completed; **Heads** itself grants
neither. Archive entry also recovers these rewards idempotently for profiles
whose corresponding completion flags predate the art.

## Shared rendering contract

Except for Hina's deliberately child-drawn picture, the finals use the
project's polished modern 2D anime visual-novel language: crisp controlled
linework, natural expressive anatomy, soft painterly cel shading, cinematic
lighting, detailed environments, and no text, UI, signatures, or watermarks.
`game/assets/cg/archive_roster.png` and
`game/assets/cg/archive_cg_gallery.png` are finish references only; their
characters, clothes, poses, and locations are not copied.

## No One Lived There

### Story rationale

The image now centers the small hand mirror Kotonoha inherited from her
grandmother rather than inventing another human stand-in for her. Its wooden
frame is darkened and smoothed by years of touch, its glass is faintly clouded
at the edges, and the faded pale-blue cotton that once wrapped it lies beneath
it on a sparse dresser beside the room's single lamp. Five-petal cherry
blossoms remain carved only into the exposed back/underside of the handle.

The glass is physically whole and plainly lit, but its reflection is entirely
blank: no girl, room, lamp, cloth, or camera appears in it. That impossible
absence is presented quietly rather than as a portal or horror effect. No
person appears anywhere in the CG; the missing reflection carries the allegory
on its own.

### Reference images

1. `game/assets/cg/archive_cg_gallery.png` -- finish/style only.
2. `game/assets/cg/archive_roster.png` -- finish/style only.

### Final generation prompt

> Use case: stylized-concept  
> Asset type: 16:9 visual-novel completion CG titled "No One Lived There"  
> Input images: Images 1 and 2 are finish/style references only. Do not copy
> their characters, identities, poses, clothing, or locations.  
> Primary request: Create a quiet still-life allegory built around the small,
> old hand mirror a girl inherited from her grandmother.  
> Scene/backdrop: A sparse bedroom dresser against a nearly bare dark wall at
> blue hour. A single warm desk lamp is cropped at the far left. Rest the mirror
> face-up and diagonally across its faded pale-blue cotton wrapping, with the
> handle extending just beyond the dresser edge.  
> Subject/object: Exactly one hand mirror. Its simple wooden bezel and handle
> are darkened and worn smooth by decades of touch. The visible top/front is
> plain. Let the overhanging handle expose a narrow portion of its back or
> underside, where small cherry blossoms with exactly five petals are carved.
> The glass remains intact and is only faintly clouded around its outer edge.  
> Reflection: The mirror contains a completely blank, featureless muted
> pearl-gray field with a slight blue cast. It reflects absolutely nothing--no
> person, face, silhouette, room, lamp, wall, dresser, cloth, window, camera,
> object, or shaped highlight. A thin rim sheen may establish that it is glass,
> but the center stays empty.  
> Style/medium: Polished modern 2D anime visual-novel CG; crisp controlled
> linework, elegant simplified shapes, deliberate cel-shaded light planes, and
> painterly anime background finishing matching the reference finish.  
> Composition/framing: Wide 16:9 close still life. Make the mirror the clear
> focal point while preserving generous bare-wall negative space.  
> Lighting/mood: Warm lamplight from the left meets subdued blue ambient light
> from the right; intimate, melancholy, restrained, and still.  
> Constraints: No human anywhere; exactly one mirror; no text, title, UI,
> signature, or watermark.  
> Avoid: A reflected image of any kind, black void, portal, glowing glass,
> broken glass, supernatural effects, person, hands, masks, trophies, clutter,
> photorealism, photography, or 3D-rendered materials.

### Final anime-style and carving-placement correction

The generated still-life composition was retained as the edit target, while
`archive_cg_gallery.png` and `archive_roster.png` were supplied as style-only
references. This pass removed the realistic material finish and corrected the
cherry-blossom carving from the front of the handle to its visible underside.

> Use case: style-transfer  
> Asset type: 16:9 visual-novel completion CG titled "No One Lived There"  
> Input images: Image 1 is the exact still-life composition and object edit
> target. Images 2 and 3 are the project's established polished 2D anime finish
> references only; do not import their characters or locations.  
> Primary request: Convert all of Image 1 into unmistakably illustrated modern
> 2D anime visual-novel art while preserving its composition and symbolism. Use
> crisp controlled ink linework around the mirror, dresser, lamp, cloth, and
> drawer; elegant simplified shapes; deliberate cel-shaded light planes;
> painterly anime background finishing; restrained stylized wood grain and
> fabric folds. Remove the semi-photorealistic, 3D-rendered, physically based
> material appearance.  
> Object continuity correction: Keep the old hand mirror face-up in the same
> place and at the same angle. Make the visible top/front of its wooden handle
> and bezel plain, touch-worn dark wood. Move the existing five-petal
> cherry-blossom carvings off the front: show them only on the narrow exposed
> underside/back of the handle where it overhangs the dresser's front edge,
> consistent with carvings being on the mirror's back. Make the pale-blue
> wrapping a simple faded soft cotton cloth rather than a plush terry towel.  
> Blank reflection invariant: Preserve the mirror glass as a completely
> featureless muted pearl-gray field with a slight blue cast. It reflects
> absolutely nothing. No face, person, hand, silhouette, room, lamp, wall,
> dresser, cloth, window, camera, object, or shaped highlight appears inside the
> glass. Keep only a thin rim sheen and faint clouding at the outermost edge so
> it still reads as intact glass.  
> Constraints: Preserve exact camera, crop, mirror scale and position, dresser
> geometry, lamp position, bare wall, lighting direction, cool/warm palette,
> negative space, and quiet mood. No human anywhere. Exactly one mirror. No
> text, UI, signature, or watermark.  
> Avoid: Photorealism, photography, 3D render, realistic ray tracing, hyperreal
> wood or fabric, depth-of-field lens look, carving on the front/top, black
> void, portal, glowing glass, broken glass, reflected imagery, supernatural
> effects, or added objects.

## Open Hands

### Story rationale

The revised image freezes the river sequence before release: the unnamed
thirty-nine-year-old traveler is still carrying the blade's weight as it first
touches the rock. She is an arbitrary older woman rather than aged-up Kotonoha.
The only inherited cue is the requested dusty-lavender hair color; the face,
unbraided disheveled hairstyle, build, and fifteen-years-worn medieval travel
clothes are original. Her expression is blank and unperformed, and the scene
has no ceremony, triumph, or supernatural meaning imposed on it.

### Reference images

1. `game/assets/cg/archive_roster.png` -- finish/style only.
2. `game/assets/cg/archive_cg_gallery.png` -- finish/style only.
3. `game/assets/backgrounds/river.png` -- broad setting geography only.

Kotonoha's sprite and the superseded CG were deliberately excluded as identity
references.

### Final generation prompt

> Use case: stylized-concept  
> Asset type: 16:9 visual-novel completion CG titled "Open Hands"  
> Input images: Images 1 and 2 are finish/style references only; Image 3 is
> broad setting geography only. Do not copy any character identity from the
> references.  
> Primary request: Depict the exact quiet instant when an original
> thirty-nine-year-old medieval traveler actively lays down the plain sword she
> has carried for fifteen years.  
> Scene/backdrop: Dawn in a thin pine wood beside a wide shallow stream running
> over old-bronze stones. A broad flat rock sits at the water's edge; it bears
> only a faint scratched arrow pointing east and illegible weathering.  
> Subject: One wholly original, weathered late-thirties woman kneels in
> three-quarter profile. She has a long/square jaw, slightly crooked nose,
> sun-browned wind-chapped skin, subtle fine age lines, and a blank, unperformed
> expression. Her dusty-lavender hair reaches between shoulder and mid-back, cut
> unevenly and disheveled by travel, loose and wind-tangled with absolutely no
> braid.  
> Action: Freeze the active placement--not the aftermath. A long undecorated
> sword, longer than her arm, is just making contact and settling horizontally
> across the flat rock. Her dominant hand is still firmly around the grip; her
> other hand still supports the flat near the guard through stained loose
> wrapping. Her torso and shoulders follow the blade's weight. A loose strip of
> wrapping and worn baldric trail naturally. Both hands are occupied; the sword
> is not yet separate from her.  
> Clothing: Convincingly medieval fantasy traveler clothing worn for fifteen
> hard years: a calf-length heavy wool campaign coat once black but faded to
> sickly indeterminate yellow-gray, frayed hem and cuffs, visible hand-stitched
> patches; coarse undyed split-neck linen tunic; cracked broad leather belt and
> plain pouch; patched smoke-brown wool trousers; wrapped calves; cracked dark
> leather boots. Everything stained, repaired, softened, and sun-faded through
> long use.  
> Style/medium: Polished modern 2D anime visual-novel CG with crisp controlled
> linework, plausible mature anatomy, painterly cel shading, and cinematic
> environmental finish matching the style references.  
> Composition/framing: Low camera across moving water; broken reflection in the
> foreground, woman and rock readable in the middle ground. The reflection
> stays fragmented.  
> Lighting/mood: Pale uneven dawn light; sober, tender, unresolved--not relief
> yet, not triumph, not despair.  
> Constraints: Clearly late thirties; arbitrary identity; blank expression;
> sword visibly in the act of being placed; no readable writing, text, title,
> UI, signature, or watermark.  
> Avoid: Kotonoha's face, youthful teen face, braided crown, any braid,
> cardigan, sweater, turtleneck, modern jacket/lapels/zipper, pristine fashion,
> armor, jewelry, open palms, sword already lying untouched, ceremony, salute,
> combat, tears, smile, glowing weapon, magic, monster.

## Hina's World

### Story rationale

The family picture retains its wholesome first read and domestic wrongness:
four smiling figures joined before one house, the fold between the parents,
the erased second house, the almost-missed hand, and the real empty chair. The
wardrobe revision changes only the children's clothes. Nine-year-old Hina and
eleven-year-old Asahiko no longer wear simplified copies of their present-day
teen sprites; their new child/preteen wardrobes are compatible with the
story's 2000s setting and avoid unsupported school-grade details. A final
anatomy pass removes the accidental third arm and places Mr Toast independently
on the grass at Hina's feet.

### Edit target

The previous pass of `game/assets/cg/hinas_world.png` was used as the exact
edit target. No character sprite was supplied, preventing its current outfit
from leaking back into the drawing.

### Final edit prompt

> Use case: precise-object-edit  
> Asset type: 16:9 visual-novel completion CG  
> Input images: Image 1 is the exact edit target.  
> Primary request: Change only the colored-pencil clothing worn by the two
> drawn children on the paper. The nine-year-old girl, second from left and
> holding the rabbit plush, must wear a lemon-yellow long-sleeve shirt under a
> medium-blue denim overall/pinafore dress ending near her knees, white ankle
> socks, and pink Velcro/light-up sneakers. The eleven-year-old boy, third from
> left, must wear a faded forest-green short-sleeve ringer T-shirt layered over
> cream long sleeves, loose tan knee-length cargo shorts, and blue-and-white
> sneakers.  
> Style/medium: Preserve the existing genuinely child-drawn colored-pencil look
> inside the paper: blunt uneven strokes, imperfect anatomy, uneven pressure,
> and coloring outside the lines.  
> Constraints: Preserve the exact overhead camera, paper, table, lighting,
> crop, all four family figures, facial features, hair, ages, proportions,
> linked-hand poses, rabbit plush, cat, house, erased second-house marks,
> vertical crease, empty chair, colored pencils, sharpener, eraser, sun, hearts,
> stars, and every other detail. Keep the girl's two barrettes on her
> anatomical-left. Keep the boy only modestly taller. Mr Toast remains a
> separate plush; no rabbit graphic on clothing.  
> Avoid: Changing any object except the two children's clothes; present-day
> teen athletic outfits; hoodie; school uniform; grade markings; readable text;
> new props; watermark.

### Anatomy and Mr Toast correction

> Use case: precise-object-edit  
> Input images: Image 1 is the exact edit target.  
> Primary request: Remove the extra third arm and remove Mr Toast from in front
> of Hina's torso. Restore the pinafore naturally. Keep exactly two arms: one
> remains linked to Mom and the other remains linked to Asahiko. Place Mr Toast
> as a separate small stuffed rabbit sitting on the drawn grass at Hina's feet,
> near one pink sneaker and clearly separate from Mochi.  
> Constraints: Change only the extra arm, rabbit location, and directly revealed
> pinafore/grass. Preserve every other person, face, outfit, linked-hand pose,
> prop, family clue, paper artifact, and colored-pencil texture. Hina has exactly
> two arms and two hands; no hand holds Mr Toast.  
> Avoid: Third arm, extra hand, rabbit attached to the torso, moving the cat,
> clothing changes, pose changes, new objects, text, or watermark.

## What I Keep / What She Kept

### Story rationale

The revised pair treats gothic tone as composition rather than cosplay or a
catalogue of symbols. Two wholly original girls occupy a contemporary dark-wood
bedroom. The open tin is required by both accounts, but its contents are never
shown: lid, rim, hand, and matte shadow withhold the interior while the girls'
faces carry its meaning. **What I Keep** is warm care beginning to curdle into
horror; **What She Kept** is the reverse moral camera, where horror thaws into
devotion. The east door is fully shut in both angles; no guest, hallway, or
exterior space remains visible, making the encounter a genuinely closed room.

The paired room uses one locked floor plan:

```text
                         NORTH WALL
                curtained rain-dark window

                         MENDER
               notebook       lifted third board
       tea tray (WEST)       OPEN TIN       cup + milk (EAST)
                                          closed door on east wall
                         FRIEND

                         SOUTH WALL
```

The first camera looks north, placing the closed door and spill screen-right and
the tray/futon screen-left. The second camera crosses the room and looks south,
so closed door/spill move to screen-left and tray/futon to screen-right; the north
window is then behind camera. The cup stays in the same world position.

### What I Keep -- reference images

1. `game/assets/cg/archive_roster.png` -- finish/style only.
2. `game/assets/cg/archive_cg_gallery.png` -- finish/style only.

### What I Keep -- final generation prompt

> Use case: stylized-concept  
> Asset type: 16:9 visual-novel completion CG, first member of a spatially
> matched pair, titled "What I Keep"  
> Input images: Images 1 and 2 are finish/style references only. Do not copy
> their characters, identities, clothes, or locations.  
> Primary request: Create a restrained literary-gothic aftermath in a
> contemporary Japanese bedroom using two wholly arbitrary late-teen girls,
> not any canonical characters.  
> Locked room geography: North wall has one curtained rain-dark window. A low
> bed and folded futon run along the west wall. A fully shut dark-walnut door is east of
> the central floor opening. The lifted third floorboard is three board-widths
> south of the north window. An open, scrubbed domestic brass tin sits
> immediately south of that opening. The quiet mender kneels north of the tin
> facing south; her closed notebook and pencil are northwest beside her. The
> loud friend kneels south of the tin facing north. The tea tray was moved
> safely west of the tin. One overturned good cup and its white milk spill lie
> east of the tin beside the closed east door.  
> Camera/composition: Camera is south of and slightly behind the friend, looking
> NORTH. Fully show the mender beyond the tin with the rain-dark window behind
> her. The closed east door, cup, and milk must appear on
> SCREEN-RIGHT. The safe tray, low bed, and folded futon must appear on
> SCREEN-LEFT. Show only a partial foreground shoulder/profile and bent knee of
> the friend as she lowers instead of recoiling.  
> Characters: The mender is compact, with a narrow wholly original face,
> chin-length blue-black bob with blunt uneven ends, gray-blue eyes, and no hair
> accessory. She wears a plain faded sage long-sleeved cotton dress and dark
> socks. Her posture is small, exact, and contained. One hand has just withdrawn
> from the lid and the other rests open beside it, offering rather than
> displaying. Her face is composed, exhausted, and pleadingly sincere, with no
> smile. The friend is unrelated and slightly taller, with tousled
> shoulder-length honey-blonde waves, blue eyes, freckles, muted ochre
> rolled-sleeve blouse, and charcoal trousers. No other person appears.  
> Tin treatment: The brass tin is open because the story requires it, but
> reveal absolutely none of its contents. Set the low camera and tin angle so
> the raised lid and near inner rim completely occlude the interior. The viewer
> sees the back of the lid, rim, and one unbroken matte darkness only--no
> identifiable object, shape, label, or shine inside.  
> Style/medium: Polished modern 2D anime visual-novel CG with crisp controlled
> linework, natural anatomy, painterly cel shading, cinematic environmental
> detail matching the references. Contemporary modest clothing, not period
> costume.  
> Lighting/mood: One ordinary shaded bedside lamp; warm amber domestic light
> around the girls, with restrained cold rain-blue shadows intruding.
> Claustrophobic low framing and deep negative space create subtle Poe-esque
> unease. Care and violation coexist without a villain cue.  
> Constraints: Spatial directions are mandatory; exactly the same world
> geometry will be reversed later. No readable text, title, UI, signature, or
> watermark.  
> Avoid: Resemblance to Tsubaki or Matsuda; brown waist-length hair; red hair;
> ponytail; braid; feather hairpin; amber or green eyes; burgundy-black dress;
> lace-heavy Victorian clothing; visible tin contents; tags; thread; glass;
> cotton bundles; coin or heart token; gore; body parts; blood; candelabra;
> candles; ravens; skulls; occult marks; supernatural soot or ash; scorched
> frame edges; symbolic clutter.

### What She Kept -- reference images

1. The selected 1672x941 source for **What I Keep** -- room, identity,
   clothing, and world-space geometry reference.
2. `game/assets/cg/archive_roster.png` -- finish/style only.
3. `game/assets/cg/archive_cg_gallery.png` -- finish/style only.

### What She Kept -- final generation prompt

> Use case: stylized-concept  
> Asset type: 16:9 visual-novel completion CG, exact spatial companion to
> "What I Keep," titled "What She Kept"  
> Input images: Image 1 establishes the same room, two original girl designs,
> clothing, props, and world-space geometry that must continue. Images 2 and 3
> are finish/style references only. Generate a new camera view; do not simply
> mirror-flip or repaint Image 1.  
> Primary request: Show the same room and aftermath several seconds later from
> a genuine 180-degree reverse angle, after the two guests have fled. The friend
> now understands that she was noticed and kept; the open tin remains
> narratively unreadable to the viewer.  
> Locked room continuity from Image 1: North wall has the rain-dark window. West
> wall has the low bed/folded futon. East wall has the fully shut dark-walnut door. The lifted third
> floorboard is just south of the north window. The open scrubbed brass tin sits
> immediately south of the opening. Mender remains north of tin facing south;
> friend remains south of tin facing north. Closed notebook and pencil stay
> northwest by mender. Safe tea tray remains west of tin. The same overturned
> cup and milk remain east of tin by the closed door; the puddle may have spread
> slightly but the cup does not move.  
> Camera/composition: Move camera NORTH of and slightly behind the mender,
> looking SOUTH across the tin at the friend--a true reverse shot, not a flip.
> The north window is now behind the camera and MUST NOT appear in the
> background. The closed east door, same cup, and same milk spill must now appear on
> SCREEN-LEFT. The west-side safe tray, low bed, and folded futon must now appear
> on SCREEN-RIGHT. Put the lifted floorboard in the near foreground
> behind/alongside the mender's partial silhouette. The south wall is now the
> background.  
> Characters and emotion: Preserve Image 1's wholly original identities
> exactly. Fully reveal the slightly taller friend with tousled shoulder-length
> honey-blonde waves, blue eyes, freckles, muted ochre rolled-sleeve blouse, and
> charcoal trousers. She has settled onto both knees. Her normally expansive
> posture has become completely still: shoulders lowered, mouth barely open at
> the beginning of a quiet "thank you," eyes damp but not theatrically crying.
> One hand braces on the floor; the other stops just above the tin rim without
> entering. She looks into the concealed darkness with stunned recognition, not
> horror. Make the compact mender partial in near foreground--blue-black chin
> bob, faded sage cotton dress, shoulder/profile and unnaturally still fingers
> beside the closed notebook.  
> Tin treatment: The tin stays open but reveal absolutely none of its contents.
> Use the reverse camera height, raised lid, foreground rim, hand, and deep matte
> shadow to block the interior. No identifiable object, shape, tag, bundle,
> token, label, or reflective empty-bottom shine is visible.  
> Style/medium: Polished modern 2D anime visual-novel CG, crisp controlled
> linework, natural anatomy, painterly cel shading, cinematic environment
> matching Image 1 and the style references. Contemporary modest clothing, not
> period costume.  
> Lighting/mood: Cool blue-black rain-muted night fills the south wall, while
> one narrow ordinary amber bedside-lamp pool still
> visually joins the two girls and tin. Horror melts quietly into devotion.
> Subtle Poe-esque pressure through framing and silence, not props or costume.  
> Constraints: Exact reverse geometry is mandatory; two main girls only; the
> room is fully closed; no readable text, title, UI, signature, or
> watermark.  
> Avoid: Repeating Image 1's camera side; showing the north window; spill/tray
> on their old screen sides; resemblance to Tsubaki or Matsuda; brown
> waist-length hair; red hair; ponytail; braid; feather hairpin; amber or green
> eyes; burgundy-black dress; lace-heavy Victorian clothes; visible tin
> contents; tags; thread; glass; cotton bundles; coin or heart token; gore; body
> parts; blood; screaming; recoil; candelabra; candles; ravens; skulls; occult
> motifs; supernatural soot/ash; symbolic clutter.

### Closed-room correction passes

**What I Keep:**

> Use case: precise-object-edit  
> Primary request: Remove the two background people at screen-right and replace
> the entire open doorway/corridor with one fully shut solid dark-walnut interior
> door in the same east-wall position. The door is opaque and flush, with a
> simple recessed panel and dark metal handle; no glass, gap, hall, silhouette,
> person, or light leak remains.  
> Constraints: Preserve both girls, the tin, lifted board, closed window,
> bed/futon, tray, notebook, cup and screen-right milk spill, lighting, camera,
> and every other object exactly.

**What She Kept:**

> Use case: precise-object-edit  
> Input images: Image 1 is the reverse-angle edit target; Image 2 is the corrected
> companion shot, used only to match the shut east door.  
> Primary request: Replace the open corridor at screen-left with the reverse-angle
> view of the same fully shut dark-walnut door. No hallway, exterior space,
> silhouette, person, or light leak remains.  
> Constraints: Preserve the reverse camera and geometry. The closed east door,
> cup, and milk remain screen-left; tray and futon remain screen-right. Preserve
> both girls, tin, lifted board, notebook, lighting, and every other prop exactly.

## Runtime normalization

Every selected 1672x941 RGB source was converted to 1280x720 RGB with Lanczos
downsampling and a near-lossless center crop:

```text
scale=1280:720:force_original_aspect_ratio=increase:flags=lanczos,
crop=1280:720:0:0,setsar=1
```

The important subjects and completion clues remain within the central safe area
because the Music Room may reuse unlocked CGs in a shallower `fit "cover"`
panel.
