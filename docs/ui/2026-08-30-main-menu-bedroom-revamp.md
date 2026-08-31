# Main Menu Bedroom Revamp

Date: 2026-08-30

## Outcome

The live title screen now opens on an empty Matsuda-coded bedroom at blue hour
instead of the broadcast/radio-control room. The first read is domestic, quiet,
and compatible with the existing lo-fi track. The second read is less settled:
mystery novels, cars, games, schoolwork, handmade planning, and visual
storytelling occupy their own carefully arranged zones without resolving into
one clean identity.

The active screen is `game/main_menu_room.rpy`. The former broadcast desk is
still available as `screen main_menu_terminal_legacy` in `game/screens.rpy`, but
normal play does not invoke it. Keeping the dormant authored version preserves
a rollback/reference point without leaving its perpetual animation active.

## Art direction and continuity

The room uses the private counterpoint to Matsuda's public performance: "the
stage after the audience has left." Main-story continuity supports the visible
prop language:

- Matsuda is a late-teen third-year transfer student.
- Her established interests include mystery novels, sports cars, and games.
- Under stress she aligns napkin corners and squares sugar packets, while her
  larger behavior includes buying nine books and forgetting an entire bag.
- Her public theatricality can give way to a quieter, more tentative person.
- Teal/aqua, red, white, navy, and walnut are established character colors, but
  the room desaturates them into fabric, paper, wood, and evening light rather
  than terminal neon.

The plate therefore uses precise small arrangements on the desk, a broader
loose arrangement across hobby zones, and one bowed shopping bag with an
overflow stack. White gloves, the model car, controller/game cases, mystery
serials, and planning/storyboard sheets identify her without a character,
portrait, family claim, real brand, or spoiler.

This is a menu-only location. Matsuda's dwelling type, household composition,
and exact neighborhood are not established, so this image is not story-canon
geography. If a future story scene reuses the room, its spatial contract must be
added to `docs/assets/backgrounds/BACKGROUND_ART_BIBLE.md` first.

## Interface language

The UI is a restrained editorial sidebar rather than another machine panel:

- warm off-white reading type over a translucent blue-black field;
- muted teal for continuity with Matsuda, with a soft burgundy hover accent;
- eight full-width rows with stable mouse/focus targets;
- one table controlling labels, quiet category verbs, contextual copy, and the
  original actions;
- the small `STORY / GAME / MEMORY` line deliberately sets `GAME` in the other
  display face and color, giving the menu its first almost-missed identity slip;
- no scanlines, grain, equalizer, waveform, tuner, CRT, status telemetry, or
  broadcast language;
- no perpetual ATL. The background, sidebar, rules, and rows stop redrawing
  after their short entrance, so Ren'Py can return to idle prediction.

The action contract remains:

| Row | Action |
|---|---|
| New Game | `Start()` |
| Load Game | `ShowMenu("data_bank")` |
| Arcade | `ShowMenu("arcade_hub")` |
| Archive | `ShowMenu("archive")` |
| Credits | `ShowMenu("credits_menu")` |
| Donate | existing Ko-fi `OpenURL` |
| Settings | `ShowMenu("preferences")` |
| Quit | `Quit(confirm=False)` |

The developer-hub mount and immediate Escape-to-quit behavior are preserved.
Achievement and Matsucoin title overlays retain their existing z-order and the
new sidebar leaves their bottom-right area unobstructed.

## Asset integration and provenance

Runtime asset:

`game/assets/gui/menu/main_menu_matsuda_evening.png`

- 1280x720, 24-bit RGB PNG.
- Generated with the built-in OpenAI image-generation tool.
- Selected raw output: `exec-25a74e0c-193d-4108-b0ae-c132ddeafffc.png`.
- Raw output: 1672x941, 24-bit RGB.
- Shipping derivative: one Lanczos resize to 1280x720 with FFmpeg; the raw
  output remains in the tool-managed generation directory.
- `enter_m_main_menu_bg` now points to the new file. The older
  `main_menu_matsuda_evening.png` is intentionally untouched because it is also consumed by
  the cold-open plates, legacy drifting `menu_bg`, and other terminal-family
  screens.

No raster button plates were needed. The new button faces, selection bars, and
rules are code-native Solids/styles, which remain crisp at the project's virtual
resolution and avoid another texture decode on the title path.

### Final image-generation prompt

```text
Use case: stylized-concept
Asset type: production 16:9 Ren'Py visual-novel main-menu background, delivered as one clean environment plate with no UI baked in.
Input images: Image 1 is the canon reference for ENTER M interior perspective, linework, softly painted material detail, and 35 mm visual-novel camera scale. Image 2 is the canon reference for warm practical light against a cool blue-hour exterior. Image 3 is the canon reference for lived-in creative/tabletop clutter rendered as coherent prop groups. Image 4 is a palette and character-personality reference only; do not include the character or any person.
Primary request: Create a completely new, empty bedroom belonging to Matsuda Akai at early evening: "the stage after the audience has left." It should feel calming and intimate at first glance, while its props quietly suggest a girl whose small arrangements are exact but whose larger life is creatively disordered.
Scene/backdrop: A modest contemporary Japanese-adjacent late-teen bedroom at blue hour. Camera is inside the room at approximately eye level with straight verticals, looking diagonally toward a broad window in the center-right/right third. Beyond it are anonymous low-rise rooftops, a few utility lines, late-spring foliage, soft indigo sky, and a handful of distant warm windows; no recognizable landmark. A warm desk lamp reflects naturally in the window glass. Include a single neatly made bed, practical walnut desk, narrow shelving, school bag, small speakers or a closed laptop, desaturated teal curtains/accessories, slate/navy bedding, cream walls, and one or two restrained burgundy-red accents.
Matsuda-specific prop story: Keep x=40-430 medium-dark, low-detail, and readable as negative space for a vertical menu. Put the main window and desk anchor in the center-right. On/near the desk, create several precisely squared "islands" of order: aligned notebook and papers, a short run of mystery novels with abstract unlettered covers, one generic unbranded sports-car magazine or small model car, and a controller or compact game case. Nearby, let the room's macro-order loosen: one bowed paper shopping bag and a short overflow book stack forgotten beneath or beside the desk. Her pair of clean white gloves may rest together as a quiet signature. Optional minor texture: two or three unlabeled storyboard thumbnails or a graph-paper map and die, subordinate to the room.
Style/medium: Match the supplied ENTER M backgrounds: polished 2D anime visual-novel environment painting, grounded softly rendered realism, clean controlled edges, moderate hand-painted material texture, natural atmospheric perspective, restrained saturation, no photographic texture and no glossy CGI look.
Composition/framing: True wide 16:9 composition intended for 1280x720. Approximately 35 mm eye-level perspective, straight verticals. Left third quiet and darker for overlay navigation; window, desk, and personality props remain clearly visible in the right two-thirds. Do not bake in a dialogue box or any menu elements.
Lighting/mood: Calm blue hour. Cool indigo window light and soft warm amber desk light balance each other; restful lo-fi evening atmosphere, not gloomy, horror-coded, cyberpunk, or neon.
Color palette: cream, walnut, slate/navy, desaturated teal/aqua, indigo blue hour, warm amber practical light, tiny muted burgundy accents.
Constraints: Empty cast. No person, silhouette, face, body reflection, family portrait, second bed, luxury decor, streamer setup, broadcast studio, radio tuner, waveform, warning light, visible code, glitch effect, supernatural anomaly, real brand, readable generated words, garbled signage, watermark, plant used as generic decoration, or baked UI. No children's-TV photos or overt spoiler imagery. Preserve useful clean negative space on the left and keep the whole plate coherent with Images 1-3.
```

Input roles used for the selected generation:

- `game/assets/backgrounds/bedroom.png`: current interior finish and camera.
- `game/assets/backgrounds/kitchen_evening.png`: warm/cool evening exposure.
- `game/assets/backgrounds/living_room_tabletop_night.png`: handmade prop vocabulary.
- `game/assets/characters/matsuda/neutral.png`: palette/personality only.

## Validation

- `git diff --check` passed for the touched source files.
- `python -B tools/check_screens.py` passed: 291 screens defined and 262
  distinct names referenced; every referenced screen exists.
- `python -B tools/check_dev_hub_contracts.py` passed.
- `python -B tools/test_matsucoin_deferred_receipts.py` passed.
- Direct embedded-Python MatsuPy compile passed with exit code 0 and 0
  unreachable items across 123 source files. The first sandboxed compile was a
  known false start because it could not write SDK common-file caches; the
  successful compile was rerun with the required SDK access.
- Direct embedded-Python MatsuPy lint completed with exit code 0. Its missing
  Monika room, Natsuki MPT, splash, notebook/glitch, blood, and BSOD files are
  pre-existing project warnings; no warning points at the new main-menu source
  or background.
- The real title lifecycle was launched through an external, environment-gated
  search-path probe with isolated saves, persistent data, log, temp directory,
  and audio driver. It skipped the splash/OP, called the real
  `before_main_menu`, rendered the real `screen main_menu`, captured, and exited
  automatically.
- The renderer log confirms `Initializing gl2 renderer`, virtual size
  1280x720, NVIDIA GL2, and the generated background is consumed through
  `enter_m_main_menu_bg`.
- Windows supplied a 1274x717 client drawable for this windowed probe; Ren'Py's
  saved PNG is 1274x716. That is a physical-window capture artifact, not a
  virtual-layout or source-asset size change. The frame still covers the full
  virtual canvas and was visually checked for title, row, description, footer,
  developer mount, background crop, and right-side overlay clearance.

Live evidence:

`docs/ui/evidence/2026-08-30-main-menu-live-gl2.png`
