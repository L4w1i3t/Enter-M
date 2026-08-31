# Seer CG Production Prompt

This document records the 2026-08-27 replacement for the unlockable **Seer**
CG awarded by defeating Matsuda's boss fight. The art was generated with the
built-in image-generation tool and normalized to the project's native
1280x720 CG canvas.

## Runtime integration

- Final file: `game/assets/cg/seer.png`
- Gallery location: **Side Stories > Matsuda's Story > Seer**
- Unlock call: `cg_unlock("Seer")`
- Persistent key: `cg_seen_mod_assets_cg_seer`

The replacement deliberately keeps the existing path, title, and legacy-derived
persistent key so previously unlocked profiles remain unlocked.

## Continuity brief

The chosen instant is phase two's **Redline Sweep**, viewed from the established
downstage/party side of the arena. Tohu Imago banks across the opened,
cathedral-lit cosmic deck while a white-gold wind crescent tears diagonally past
the camera. Four cropped, near-black party silhouettes brace along the bottom
edge; they remain anonymous because the player may choose any four of seven
fighters.

Tohu Imago retains Matsuda's crimson hair, aqua eyes, calm analytical expression,
ivory feather armor, antique-gold structures, turquoise gems, charcoal inner
feathers, layered eye-wing hierarchy, crown, spiked halo, and separate overhead
blue eye. Her canonical anatomical-right braid may be absent where the loose
phase-two hair, crown, and banking action obscure it; it must never move to the
opposite side or duplicate. Phase-one black/cyan armor and glaive are excluded.

## Reference images

1. `game/addons/Matsuda's Sick Boss Fight/phase2.png` -- primary exact Tohu
   Imago costume, wing, crown, halo, and eye reference.
2. `game/assets/characters/matsuda/neutral.png` -- Matsuda's face, eye color,
   crimson hair, and canonical right-side braid.
3. `game/addons/Matsuda's Sick Boss Fight/phase1concept.png` -- transformed
   facial identity and braid only; its black/cyan suit is explicitly ignored.
4. `game/assets/backgrounds/battle_setpiece.png` -- cosmic-sky reference only,
   repainted beneath the phase-two gold deck and cathedral lighting.

The old `seer.png` was not used as a composition reference because its centered,
symmetrical cutout treatment was the element being replaced.

## Prompt set

### 1. Action composition

> Create an entirely new 16:9 action freeze-frame of Tohu Imago performing the
> named phase-two attack Redline Sweep. Use a low, canted deck-level camera from
> behind the party. Matsuda banks hard through the air in a violent three-quarter
> turn: torso twisted, crimson hair and feather train dragged backward, inner
> wings folding into the turn while the broad eye-studded lateral tiers scythe a
> compressed white-gold wind crescent diagonally across the gold deck and close
> past the lens in extreme foreshortening. Give the wind blade a thin crimson
> pressure edge and sparse aqua accents. Keep Matsuda's face eerily calm and the
> overhead halo-eye tracking the party. Show the dark perspective deck, luminous
> floor sigil, opened cathedral-like roof, gold shafts, and cosmic void. Place
> exactly four tiny cropped near-black, back-facing, anonymous combatant
> silhouettes only along the bottom edge. Preserve Tohu Imago's exact phase-two
> identity and exclude handheld weapons, text, HUD, logos, and watermarks.

### 2. Traditional-animation direction

> Preserve the action and repaint it as a genuinely hand-produced late-1980s/
> 1990s Japanese broadcast-anime freeze-frame: photographed painted cels over a
> hand-painted gouache background, hard variable ink contours, broad opaque
> fills, two-tone cel shadows, limited-animation wing and wind smears, blown
> white-gold impact paint, subtle line boil, restrained 35mm grain and dust,
> slight red/cyan cel-layer misregistration, and mild broadcast softness. Reduce
> ornate micro-rendering while preserving the major costume, halo, wing, and eye
> motifs. Avoid contemporary glossy game-key-art rendering, 3D CGI, perfect
> symmetry, and direct recreation of any existing anime frame.

### 3. Final cel-authenticity pass

> Keep the exact canted camera, Redline Sweep crescent, banking pose, four bottom
> silhouettes, gold deck, halo-eye, wing placement, and 16:9 crop. Convert the
> characters, wings, hair, costume, silhouettes, and attack into clean flat
> acetate-cel paint: bold economical hand-inked outlines, large unbroken color
> fills, a strict limited palette, one hard-edged shadow tone plus occasional
> deep impact shadow, sparse solid highlights, and simplified graphic feather
> groups. Render the sweep as a stark white-gold smear with a solid crimson rim
> and only two or three thin aqua streaks. Keep the environment a soft painted
> matte and replace fantasy towers with dark abstract arena ribs framing the
> opened cathedral-like roof. Preserve exactly one Matsuda, exactly four
> anonymous silhouettes, one separate halo-eye, coherent anatomy, and the
> original attack direction. No text, HUD, logos, signatures, or watermark.

## Runtime normalization

The selected 1672x941 RGB source was reduced to 1280x720 with a near-lossless
16:9 crop and Lanczos downsampling:

```text
scale=1280:720:force_original_aspect_ratio=increase:flags=lanczos,
crop=1280:720:0:0,setsar=1
```

The composition keeps Matsuda, the halo-eye, and the sweep inside the central
vertical safe area because the Music Room may reuse unlocked CGs in a shallow
`fit "cover"` panel.
