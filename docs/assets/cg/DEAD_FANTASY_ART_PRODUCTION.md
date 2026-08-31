# Dead Fantasy Art Production Record

This record covers the original art generated for Matsuda's "Dead Fantasy"
side story on 2026-08-28. All source imagery was created or edited with the
built-in image-generation mode, then copied into the project. Wide images were
normalized with Lanczos scaling to the native 1280x720 Ren'Py canvas; character
sprites remain 1024x1536 RGBA and are staged through a crop-free portrait
transform. The west-ridge plate received a composition-preserving top crop to
remove a faint generated mark. Sam's generator baked a checkerboard into its
background; the runtime `sam_clean.png` preserves every RGB pixel and clears
13,417 additional alpha pixels, including two enclosed checkerboard islands.

## Runtime files

| Role | Final project path |
| --- | --- |
| Akai council | game/assets/backgrounds/castle01_strategyroom_night.png |
| Rival council | game/assets/backgrounds/greywake_rival_keep.png |
| Field deployment | game/assets/backgrounds/greywake_field_dawn.png |
| Ravine rescue | game/assets/backgrounds/greywake_ravine.png |
| West-ridge reversal | game/assets/backgrounds/greywake_west_ridge.png |
| Collapse, parley, and duel | game/assets/backgrounds/greywake_field_aftermath.png |
| Tabletop reveal | game/assets/backgrounds/living_room_tabletop_night.png |
| Duel CG / gallery reward | game/assets/cg/dead_fantasy_greywake_draw.png |
| Fantasy cast | game/assets/extra_sprites/dead_fantasy/{akai,rival,tsubaki,gary,gregor,leif}.png and sam_clean.png |

## Exact accepted prompts

### Greywake field at dawn

Mode: built-in image generation, stylized-concept.

~~~text
Use case: stylized-concept
Asset type: 16:9 visual-novel background for an original medieval tactical-RPG chapter
Primary request: Create the pre-battle establishing view of Greywake Field just before two armies meet.
Scene/backdrop: A vast cold valley before dawn in late autumn, with thin windblown snow beginning to cover brown grass. The terrain must be tactically legible: a steep west ridge on one side, a shallow central road and ford, a narrow ravine with a guarded wagon convoy, a north road climbing toward a mountain pass, and a distant grounded stone keep. Two opposing medieval armies wait in disciplined formations far apart, red and blue standards small and generic.
Style/medium: Polished original modern 2D anime visual-novel environment art; crisp controlled linework, painterly cel shading, detailed hand-painted tactical-RPG background, not photorealistic and not 3D.
Composition/framing: Wide cinematic 16:9 establishing shot from a slightly elevated commander's viewpoint. Keep the important terrain and distant formations above the lower quarter because a dialogue box will cover the bottom 214 pixels. Strong depth and readable geography, with no close character.
Lighting/mood: Blue predawn, low steel clouds, one pale seam of dawn behind the pass; tense, exhausted, solemn, wind carrying first snow.
Color palette: Slate blue, cold gray, muted brown, small restrained red and blue standard accents.
Constraints: original world and heraldry; no recognizable copyrighted characters, faction symbols, logos, readable text, UI, signature, or watermark; no active combat yet; no corpses; no fires; exactly one wagon convoy.
Avoid: photorealism, 3D render, sci-fi, magic effects, demonic architecture, giant castles, modern objects, gore, close-up soldiers, illegible clutter.
~~~

### Greywake ravine

Mode: built-in image generation, stylized-concept.

~~~text
Use case: stylized-concept
Asset type: 16:9 visual-novel battle background for an original medieval tactical-RPG chapter
Primary request: Create the Greywake ravine during a daring prisoner-wagon rescue before dawn.
Scene/backdrop: A narrow rocky ravine dusted with fresh snow, switchback road hemmed by dark pines and low cliffs. Exactly four canvas-covered medieval prison wagons have halted in a staggered convoy; simple wooden cages and cut harnesses suggest a rescue in progress. A small distant cavalry unit and scattered guards are silhouettes only, leaving the foreground and central upper area readable for visual-novel character sprites.
Style/medium: Polished original modern 2D anime visual-novel environment art, controlled linework, painterly cel shading, hand-painted tactical-RPG background, not photorealistic and not 3D.
Composition/framing: Wide 16:9 view looking along the ravine, road leading toward a visible north exit and dawn glow. Keep key action above the bottom quarter because dialogue UI covers it. No close-up character.
Lighting/mood: Cold predawn blue with one small orange diversion fire far behind the wagons, whipping snow, urgent but hopeful.
Color palette: Slate blue, charcoal rock, muted pine green, restrained amber fire.
Constraints: original setting, exactly four wagons, no readable text, no logos, no recognizable copyrighted designs, no UI, no signature, no watermark, no gore.
Avoid: giant armies, fantasy magic, demonic scenery, modern vehicles, close faces, photorealism, 3D render, excessive fire.
~~~

### Greywake west ridge

Mode: built-in image generation, stylized-concept, followed by a surgical
image-generation cleanup and safe crop.

~~~text
Use case: stylized-concept
Asset type: 16:9 visual-novel battle background for an original medieval tactical-RPG chapter
Primary request: Create the west ridge at the turning point of the Battle of Greywake.
Scene/backdrop: A steep snow-streaked ridge above a broad valley, churned cavalry tracks and broken generic lances showing that light horsemen just captured it. The reverse slope hides a brutal counterattack: distant armored silhouettes crest through blowing snow while riderless horses and torn red standards retreat. A narrow uphill footpath from the valley establishes where infantry reinforcements would charge.
Style/medium: Polished original modern 2D anime visual-novel environment art; crisp controlled linework, painterly cel shading, dynamic hand-painted tactical-RPG background; not photorealistic and not 3D.
Composition/framing: Wide low-angle 16:9 view along the ridge spine with strong diagonal momentum. Reserve open readable space in the upper-middle for VN sprites, and keep essential action above the lower quarter dialogue box.
Lighting/mood: Storm arriving early at blue dawn, wind-driven snow erasing visibility, desperate and heroic without glorifying gore.
Color palette: Cold steel blue, gray stone, dirty white, small torn red accents.
Constraints: original armor and heraldry, no identifiable close characters, no corpses in focus, no blood, no text, no logos, no UI, no signature, no watermark.
Avoid: recognizable Fire Emblem characters or symbols, magic, monsters, demonic elements, modern gear, photorealism, 3D render, overcrowding.
~~~

Cleanup prompt:

~~~text
Use case: surgical cleanup of a production background.
Preserve the supplied snowy west-ridge battle background exactly: same camera, composition, terrain, horses, distant troops, generic torn red standards, lighting, painterly anime tactical-RPG style, and 16:9 framing. Remove only the faint artist-like mark/signature/watermark in the lower-right corner and reconstruct clean snow and rock texture underneath it. Do not add, remove, or change any other element.
No text, no logo, no signature, no watermark, no UI.
~~~

### Greywake aftermath

Mode: built-in image editing using the dawn field as the structural reference.

~~~text
Use case: image edit / production background.
Strictly preserve the geography, camera, 16:9 framing, painted anime tactical-RPG style, west cliff, central ford and road, north pass, and hilltop keep from the supplied Greywake Field image. Transform the same location into the immediate aftermath of a long battle at gray sunrise: formations have broken into small exhausted clusters, churned snow and mud cover the center, snapped generic spears and abandoned shields lie scattered, a few distant medics tend wounded silhouettes, and both armies have stopped fighting around a clear central lane prepared for two commanders to parley. Show restrained small smoke plumes and torn generic red and blue standards. No close characters, no active combat, no gore, no visible corpses. Keep the central upper field readable for VN sprites and all crucial visual information above the lower quarter dialogue UI.
No text, no logos, no recognizable copyrighted heraldry, no signature, no watermark. Avoid photorealism, 3D render, magic, monsters, huge fires, and clutter.
~~~

### Akai's night council

Mode: built-in image editing using castle01_strategyroom.png.

~~~text
Use case: image edit / production visual-novel background.
Preserve the exact room geometry, table, chairs, maps, banners, camera, 16:9 framing, original polished 2D anime background style, and empty-room composition. Change the daylight war room into a tense midnight strategy council during the first snowfall: the arched window shows deep blue predawn darkness and windblown snow, candles and the lantern provide warm restrained light, and the campaign map on the table has several small red and blue wooden markers arranged around a ridge, ravine, road, and pass. Make the room feel actively used but orderly.
No people, no readable text, no new logos, no UI, no signature, no watermark. Do not alter the banner designs or furniture layout. Avoid photorealism, 3D render, excessive darkness, fire, clutter, and magical effects.
~~~

### Rival's keep

Mode: built-in image generation, stylized-concept.

~~~text
Use case: stylized-concept
Asset type: 16:9 visual-novel strategy-meeting background for an original medieval tactical-RPG chapter.
Primary request: Create the opposing commander's grounded field headquarters inside Greywake Keep before dawn.
Scene/backdrop: A cold, austere stone command chamber in a small mountain border keep. A battered rectangular table holds a large terrain map showing a ridge, central ford, east ravine, prison-wagon route, and north pass, with disciplined charcoal-and-ivory wooden markers and a smaller line of red markers. Narrow arrow-slit windows show predawn snow. Practical weapon racks, damp cloaks, two shield lanterns, and one brazier make the room inhabited but morally neutral.
Style/medium: Polished original modern 2D anime visual-novel environment art, controlled linework, painterly cel shading, grounded tactical-RPG background, not photorealistic and not 3D.
Composition/framing: Wide 16:9, empty room, table angled for readable strategy geography, clear upper-middle staging space for VN sprites, important content above lower-quarter dialogue UI.
Lighting/mood: Steel-blue window light and restrained amber brazier light; disciplined, exhausted, tense, not sinister.
Color palette: Charcoal stone, muted ivory cloth, dark timber, steel blue, restrained amber.
Constraints: original heraldry and architecture, no people, no demonic or villain-coded symbols, no readable text, no UI, no logo, no signature, no watermark.
Avoid: purple magic, skulls, torture devices, gothic excess, giant throne room, recognizable copyrighted emblems, photorealism, 3D render.
~~~

### Tabletop reveal

Mode: built-in image editing using living_room_night.png.

~~~text
Use case: image edit / production visual-novel reveal background.
Preserve the exact living-room architecture, night lighting, camera, 16:9 framing, sofa, TV, dining area, and polished 2D anime background style. Turn the coffee table and nearby seating into the immediate aftermath of a heated six-player tabletop fantasy campaign without showing any people: place a large hand-drawn battle map across the coffee table, a low cardboard game-master screen at the far edge, six distinct clusters of character sheets and notebooks distributed around the table and sofa, miniatures, pencils, erasers, many polyhedral dice, open snack bowls, soda cans, and one charcuterie plate. Put one conspicuous twenty-sided die stopped beside a spiral GM notebook near the center. The mess should look used by emotional teenagers, not staged, while retaining believable clear floor space for visual-novel sprites.
No readable text on papers or screen, no alcohol, no brand logos, no added people, no UI, no signature, no watermark. Avoid photorealism, 3D render, fantasy magic appearing in the real room, excessive clutter, changing wall/furniture geometry, or daylight.
~~~

### Greywake Draw CG

Mode: built-in image editing/composition using Matsuda, MC, and the Greywake
aftermath as identity and setting references.

~~~text
Use case: production CG for an original 16:9 anime visual novel and medieval tactical-RPG side story.
Create the climactic frozen draw at Greywake, using the supplied red-haired green-eyed woman as Akai's exact facial/hair identity, the supplied brown-haired amber-eyed young man as the Rival commander's exact facial/hair identity, and the supplied aftermath landscape as the setting/style reference. Reimagine both as grounded original medieval commanders, not in their modern clothes.
Action: in the center of a trampled snowy battlefield at gray sunrise, the exhausted commanders finish a long duel in a mutual lethal lock. The Rival stands on the viewer's right with his straight sword point stopped a finger-width from Akai's throat. Akai stands on the viewer's left, lower and braced, with her sword edge tucked under his ribs. Their blades and bodies must be anatomically coherent and visibly make a true draw; neither has won. Both armies have frozen in a wide ring far behind them, weapons lowered. Akai wears practical teal-accented light plate and a weather-beaten blue cloak; the Rival wears restrained charcoal-and-ivory field armor and a torn dark cloak. Their faces show fury collapsing into exhausted recognition, not romance.
Style: polished original modern 2D anime visual-novel CG, crisp controlled linework, painterly cel shading, cinematic tactical-RPG key art, natural anatomy, restrained detail.
Composition: wide 16:9, waist-to-full figures, clear silhouettes and both sword endpoints unmistakable. Keep their faces and blade lock above the bottom quarter so either full-screen CG or dialogue overlay works.
Lighting/mood: cold gray dawn, sparse snow, backlit breath, grand and tragic but human.
Constraints: preserve the two supplied character identities; original armor/heraldry; only two foreground characters; no text, UI, logo, signature, or watermark; no blood or gore.
Avoid: recognizable copyrighted armor/designs, photorealism, 3D render, magic, glowing weapons, romance pose, extra limbs/fingers, crossed blades that fail to threaten both characters, victory framing.
~~~

### Gary

Mode: built-in image generation, production game asset.

~~~text
Use case: production game asset.
Asset type: transparent-background full-body character sprite for an original anime visual novel / medieval tactical RPG.
Character: Gary, a lean late-teen cavalry scout and rescue leader. He has warm medium-brown skin, short wind-tossed dark chestnut hair, gray-green eyes, an alert tired face, and a narrow athletic build. Practical weathered slate-blue gambeson, short mail shoulder cape, muted brown riding boots and gloves, compact sword at his hip, folded blue strap and small wheel-brace tool on his belt. No helmet. Determined neutral stance, one hand near belt, humane and meticulous rather than flashy.
Style: polished original modern 2D anime VN sprite, crisp linework, painterly cel shading, natural anatomy, clean readable silhouette, coherent with high-quality 640x960 character sprites.
Composition: full body head-to-boots, centered, upright 2:3 portrait canvas, generous transparent margin, no cropping.
Lighting: soft neutral studio light matching visual-novel sprites.
Constraints: truly transparent RGBA background, one character only, original design, no text, no logo, no signature, no watermark, no copyrighted character resemblance.
Avoid: opaque backdrop, scenery, horse, modern clothing, ornate royal armor, magic, exaggerated muscles, chibi, photorealism, 3D render, extra limbs/fingers.
~~~

### Gregor

Mode: built-in image generation, production game asset.

~~~text
Use case: production game asset.
Asset type: transparent-background full-body character sprite for an original anime visual novel / medieval tactical RPG.
Character: Gregor, a broad late-teen shield captain who speaks of himself in the third person until one painful break. He has olive skin, heavy dark-auburn hair cut unevenly at the jaw, weary hazel eyes, a small old scar through one eyebrow, and a powerful stocky build. Worn forest-gray brigandine over mail, faded blue sash, practical boots, a large battered kite shield resting beside him, plain arming sword sheathed. No helmet. Guarded neutral stance with shoulders carrying too much history; kind under the fatigue.
Style: polished original modern 2D anime VN sprite, crisp linework, painterly cel shading, natural anatomy, clean readable silhouette, coherent with high-quality 640x960 character sprites.
Composition: full body head-to-boots, centered, upright 2:3 portrait canvas, generous transparent margin, no cropping.
Lighting: soft neutral studio light matching visual-novel sprites.
Constraints: truly transparent RGBA background, one character only, original design, no text, no logo, no signature, no watermark, no copyrighted character resemblance.
Avoid: opaque backdrop, scenery, modern clothing, evil/villain coding, skull motifs, ornate armor, magic, chibi, photorealism, 3D render, extra limbs/fingers.
~~~

### Leif

Mode: built-in image generation, production game asset.

~~~text
Use case: production game asset.
Asset type: transparent-background full-body character sprite for an original anime visual novel / medieval tactical RPG.
Character: Leif, a proud late-teen light-cavalry officer whose bravado masks loyalty. He has fair skin reddened by cold, tousled sandy-blond hair, sharp blue eyes, a slender athletic rider's build, and a crooked confident smile that is almost exhausted. Practical burgundy riding coat over light steel cuirass, off-white scarf, dark trousers and boots, cavalry saber at his hip, torn generic red ribbon tied at one shoulder. No helmet and no horse. Upright confident neutral pose, one hand at saber hilt.
Style: polished original modern 2D anime VN sprite, crisp linework, painterly cel shading, natural anatomy, clean readable silhouette, coherent with high-quality 640x960 character sprites.
Composition: full body head-to-boots, centered, upright 2:3 portrait canvas, generous transparent margin, no cropping.
Lighting: soft neutral studio light matching visual-novel sprites.
Constraints: truly transparent RGBA background, one character only, original design, no text, no logo, no signature, no watermark, no copyrighted character resemblance.
Avoid: opaque backdrop, scenery, horse, crown, ornate prince armor, recognizable copyrighted designs, magic, chibi, photorealism, 3D render, extra limbs/fingers.
~~~

### Akai

Mode: built-in image editing/composition using Matsuda and the duel CG.

~~~text
Use case: production game asset.
Asset type: transparent-background full-body character sprite for an original anime visual novel / medieval tactical RPG.
Character: Akai, the fantasy incarnation of the supplied red-haired green-eyed woman. Preserve her exact facial identity, long dark-red high ponytail, narrow side braid, teal hair tie, green eyes, pearl earring, confident build, and mature late-teen appearance. Replace modern clothing with the same grounded commander outfit shown in the supplied Greywake duel CG: practical worn steel light plate over deep teal quilted armor, dark navy weather-beaten cloak, fitted black trousers, armored boots and gloves, plain original longsword sheathed at her left hip. Determined exhausted neutral stance, one hand near sword, no smile.
Style: polished original modern 2D anime VN sprite, crisp linework, painterly cel shading, natural anatomy, clean readable silhouette, coherent with high-quality 640x960 character sprites and the supplied duel CG.
Composition: full body head-to-boots, centered, upright 2:3 portrait canvas, generous transparent margin, no cropping.
Constraints: truly transparent RGBA background, one character only, original armor/heraldry, no text, logo, signature, watermark, or copyrighted character resemblance.
Avoid: opaque backdrop, scenery, modern sportswear, ornate royal armor, magic, sexualized armor, chibi, photorealism, 3D render, extra limbs/fingers.
~~~

### Rival commander

Mode: built-in image editing/composition using MC and the duel CG.

~~~text
Use case: production game asset.
Asset type: transparent-background full-body character sprite for an original anime visual novel / medieval tactical RPG.
Character: the Rival commander, fantasy incarnation of the supplied brown-haired amber-eyed young man. Preserve his exact facial identity, tousled dark-brown hair, amber eyes, lean late-teen build, and understated serious expression. Replace modern hoodie with the same grounded commander outfit shown in the supplied Greywake duel CG: restrained charcoal-and-ivory field armor, dark weather-torn cloak, fitted leather gauntlets and boots, plain original straight sword sheathed at his hip, no eagle or recognizable heraldic device. Tired determined neutral stance, shoulders squared, not villainous.
Style: polished original modern 2D anime VN sprite, crisp linework, painterly cel shading, natural anatomy, clean readable silhouette, coherent with high-quality 640x960 sprites and the supplied duel CG.
Composition: full body head-to-boots, centered, upright 2:3 portrait canvas, generous transparent margin, no cropping.
Constraints: truly transparent RGBA background, one character only, original armor/heraldry, no text, logo, signature, watermark, or copyrighted character resemblance.
Avoid: opaque backdrop, scenery, hoodie, evil/villain coding, ornate prince armor, magic, chibi, photorealism, 3D render, extra limbs/fingers.
~~~

### Sam

Mode: built-in image editing/composition using the transparent Leif asset as a
format reference and Sam's existing sprite as an identity reference.

~~~text
Use case: production sprite transformation.
Use the first supplied transparent fantasy sprite strictly as the asset-format reference: preserve its true transparent RGBA canvas, clean alpha edges, full-body scale, generous empty margins, polished anime linework, and painterly cel shading. Replace that character completely with the identity from the second reference: Sam's exact short tousled blond hair, amber eyes, late-teen face, lean athletic build, and dangerous half-smile.
Dress Sam as a grounded veteran berserker in battered tan-and-charcoal lamellar armor over cream cloth, dark trousers, boots and bracers, ragged off-white scarf, with a broad single-edged sword resting on one shoulder. One character only, full body and sword uncropped.
Outside the character silhouette must remain true alpha-0 transparency inherited from the first sprite. Do not render a checkerboard, white field, gradient, scenery, floor, or shadow. No text, logo, signature, watermark, modern clothing, magic, gore, photorealism, 3D render, extra limbs, or extra fingers.
~~~

#### Sam alpha repair

Mode: two built-in background-extraction edits were attempted and rejected
because both returned fully opaque checkerboard images. The production repair
therefore uses the accepted original's exact RGB data and changes alpha only:
two enclosed neutral checker components larger than 1,000 pixels were cleared,
removing 13,417 pixels while leaving the character, sword, and antialiased
subject edges untouched. The original `sam.png` remains as the source record;
the game loads `sam_clean.png`.

First rejected extraction prompt:

~~~text
Use case: background-extraction
Asset type: production transparent character sprite for a Ren'Py visual novel
Input image: the supplied Sam fantasy sprite is the sole edit target.
Primary request: Remove every white-and-light-gray checkerboard background pixel, including the enclosed checkerboard islands trapped between the sword, left forearm, scarf, torso, right arm, ragged cloth, and legs. Return a genuinely transparent RGBA cutout.
Subject invariants: Preserve Sam's face, blond hair, amber eyes, expression, anatomy, pose, both hands, broad single-edged sword, armor, scarf, belts, cloth strips, boots, linework, coloring, lighting, and every character detail exactly. Do not redesign, repaint, relight, sharpen, crop, rescale, or reposition him.
Composition/framing: Keep the complete existing full-body figure and sword uncropped on the same upright 2:3 canvas with the same margins.
Transparency: Every pixel outside the actual character, sword, clothing, and equipment silhouette must be alpha 0. All negative-space holes inside or between silhouette elements must also be alpha 0. Preserve soft antialiased alpha only along true subject edges. Do not render or retain a checkerboard pattern; checkerboard is not content.
Constraints: one character only; no backdrop, floor, shadow, glow, text, logo, signature, or watermark.
~~~

Second rejected extraction prompt:

~~~text
Use case: background-extraction
This is a single targeted correction to the supplied sprite: the checkerboard is currently baked into an opaque image, which is wrong.
Replace ALL white and light-gray checkerboard squares with genuine alpha-0 transparency, including every negative-space hole between the sword, arms, scarf, torso, clothing strips, and legs. The final file must be RGBA with alpha 0 everywhere outside Sam's true silhouette. Do not draw a checkerboard and do not leave an opaque background.
Preserve the character and weapon pixel-for-pixel as much as possible: same face, hair, expression, pose, anatomy, hands, sword, armor, scarf, belts, cloth, boots, colors, 1024x1536 canvas, scale, and position. No repainting, redesign, cropping, glow, shadow, backdrop, text, logo, signature, or watermark.
~~~

### Tsubaki

Mode: built-in image editing/composition using Tsubaki's existing sprite.

~~~text
Use case: production game asset.
Asset type: transparent-background full-body character sprite for an original anime visual novel / medieval tactical RPG.
Character: Tsubaki, fantasy incarnation of the supplied brown-haired amber-eyed young woman. Preserve her exact gentle late-teen facial identity, long warm-brown hair, amber eyes, white feather hairpin, and slender natural build. Reimagine her as a practical battlefield cleric: layered cream and muted-blue wool robes under a fitted brown leather healing satchel harness, long weathered blue cloak, durable boots and gloves, small original sunless-silver staff held upright, bandage rolls and herb pouch at belt. Determined worried neutral expression, brave without looking militant.
Style: polished original modern 2D anime VN sprite, crisp linework, painterly cel shading, natural anatomy, clean readable silhouette, coherent with high-quality 640x960 character sprites.
Composition: full body head-to-boots, centered, upright 2:3 portrait canvas, generous transparent margin, no cropping.
Constraints: truly transparent RGBA background, one character only, modest grounded original design, no text, logo, signature, watermark, or copyrighted character resemblance.
Avoid: opaque backdrop, scenery, denim/modern clothes, religious cross, glowing magic, ornate princess dress, sexualized outfit, chibi, photorealism, 3D render, extra limbs/fingers.
~~~
