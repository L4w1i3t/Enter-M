# Room Menu Family Revamp — Second Pass

Date: 2026-08-30

## Outcome

The title screen, Settings, Records, Credits, History, Calendar, About, and the
generic confirmation panel now read as one authored menu family built around
Matsuda's evening room. The family is calm and domestic at first glance, but it
does not resolve into one clean identity: editorial folio, fabric tag, game
selector, production notebook, and a trace of technical UI all coexist. Arcade,
Archive, and the bespoke combat pause overlays retain their existing authored
identities.

This pass directly addresses the review of the first room/menu version:

- the room architecture is no longer a variation of MC's centered-bed and
  centered-window composition;
- the palette now carries teal, coral, ochre, cream, walnut, indigo, burgundy,
  lavender, and silver instead of collapsing into brown and blue;
- the laptop is open to a generic dark-theme IDE;
- the sports-car model has a coherent low coupe body, four aligned wheels,
  silver rims, and a dedicated display plinth;
- four normal wall posters cover motorsport, mystery/noir, games/fantasy, and
  synth/music interests;
- the medal rail contains cool silver medals only, with no gold or bronze;
- the existing `logo.png` is now the title's corner badge instead of a large
  text-only `ENTER M` heading;
- selector buttons use a purpose-built raster asset family; and
- Settings, Records, Credits, History, Calendar, About, and confirmations use
  the same domestic visual vocabulary without changing their behavioral models;
  and
- the Settings viewport now reserves a real gutter for its scrollbar, so the
  right corners and button faces are never clipped when an accordion opens.

## Matsuda room direction

The new room is an asymmetrical long plan viewed diagonally from the doorway.
The bed runs toward the camera along a deep teal left wall, the recessed
wardrobe interrupts the rear silhouette, a low open bookcase divides sleeping
and work zones, and an L-shaped desk follows a wide corner window on the right.
The window is not behind the bed and the desk is not simply placed beside it.

Established continuity remains the basis of the prop language: Matsuda likes
mystery novels, sports cars, games, and synth/eurobeat; she creates exact little
islands of order while larger purchases and plans sprawl. The precisely aligned
desk notes, silver medal row, and paired white gloves coexist with the bowed
shopping bag and overflow book stack. The bedroom remains menu-only geography,
not a promise about her canonical home layout or household.

## Implementation map

| Area | Live implementation | Contract retained |
|---|---|---|
| Shared room theme | `game/room_menu_theme.rpy` | Isolated palette, selector Frames, shell, navigation, and Settings-only styles |
| Main Menu | `game/main_menu_room.rpy` | Eight actions, descriptions, dev-hub mount, immediate Escape-to-quit |
| Settings | `game/screens.rpy` | Accordion reset, every Preference/FieldValue/SetField action, exact 620/588 and 289/189/141 widths |
| Records | `game/data_bank.rpy` | 36-slot mapping, five modes, confirmations, labels, metadata, rename rules, save/load shims, boss lock |
| Credits | `game/addons/Credits/credits.rpy` | Full dataset, section navigation, two adjustments, scroll reset, stable loop keys, Return behavior |
| History | `game/screens.rpy` | `_history_list`, newest-first viewport position, speaker colors, narration distinction, mouse-wheel and drag review |
| Calendar | `game/addons/Calendar System/calendar_system.rpy` | Real date, browsed month, Today sensitivity, weekday/weekend distinction, and no mutation of the story date |
| About | `game/screens.rpy` | Long-form viewport and working Ren'Py hyperlink markup |
| Confirmation | `game/screens.rpy` | Modal/z-order contract, caller-supplied actions, Escape/RMB as No, and safe default focus on No |
| Menu movement | `game/menu_transitions.rpy` | Archive/Arcade flavours unchanged; room-family screens use a quiet dissolve; Credits keeps a recolored curtain |
| Background wiring | `game/splash.rpy` | `enter_m_main_menu_bg` uses the room; cold-open, Dev Hub, and legacy drifting plates remain on `main_menu_vn.png`/`game_menu_vn.png` |

The generic `game_menu` delegates only its actual consumers, About and Calendar,
to `room_menu_shell`. History opts in explicitly, and Credits keeps a
content-specific folio shell. The shared navigation records the destination in
`_game_menu_screen` before `ShowMenu` runs, preventing stale selected states and
wrong transition flavors on intra-menu moves such as Settings to Calendar. No
Archive, Arcade, or combat-pause style, transform, or scrollbar is changed.

## Settings scrollbar geometry

The clipping in the review screenshot came from treating the viewport's full
620 pixels as both content and scrollbar space. Ren'Py's vertical-scrollbar
`Side` took its width from that same allocation, so the right clipped corners
of 620-pixel section headers and controls fell underneath it.

The corrected geometry is explicit:

- 620 pixels for the authored controls;
- 12 pixels of empty gutter;
- 8 pixels for the muted-teal scrollbar; and
- 640 pixels total viewport width.

The Graphics section is the regression case because it is tall enough to force
the bar on. Its live GL2 capture shows every two- and three-column control ending
before the gutter, with all right corners intact.

## Custom selector assets

Shipping assets:

- `game/assets/gui/menu/room_theme/selector_idle.png`
- `game/assets/gui/menu/room_theme/selector_hover.png`
- `game/assets/gui/menu/room_theme/selector_selected.png`
- `game/assets/gui/menu/room_theme/selector_danger.png`
- `game/assets/gui/menu/room_theme/selector_yes_hover.png`
- `game/assets/gui/menu/room_theme/selector_no_hover.png`

Each source plate is a 112x56 RGBA PNG. Ren'Py consumes them as nine-slice
`Frame` displayables, so the authored clipped corners, colored bookmark edge,
inner seam, and thread line remain crisp at title-row, navigation, Settings,
Credits, and compact Records sizes without allocating separate full-width
textures.

`tools/build_room_menu_assets.ps1` deterministically rebuilds all six files
with System.Drawing. On hosts where local PowerShell scripts are disabled, run
it with `powershell.exe -NoProfile -ExecutionPolicy Bypass -File`.

## Background asset and provenance

Shipping plate:

`game/assets/gui/menu/main_menu_matsuda_evening.png`

- 1280x720, RGB24 PNG.
- Generated with the built-in OpenAI image-generation tool.
- Selected raw result:
  `C:\Users\Admin\.codex\generated_images\01a0557f-6d80-7662-bd03-0e0bcf43ad02\exec-7e4adc01-8331-4b3c-88a1-82e50d0ee1e2.png`.
- Raw result: 1672x941, RGB24 PNG.
- Shipping derivative: one Lanczos resize to 1280x720 with FFmpeg.
- The previous generated room was replaced at the same menu-only asset path;
  no story background definition points to it.

Reference roles:

- `game/assets/backgrounds/cafe_stationery.png`: primary interior finish,
  linework, material rendering, and controlled color reference only.
- `game/assets/backgrounds/living_room_tabletop_night.png`: warm/cool evening
  exposure and coherent hobby-clutter grouping only.
- `game/assets/characters/matsuda/neutral.png`: Matsuda palette and personality
  reference only; no person was included.

The MC bedroom was deliberately excluded from the generation references so its
architecture could not be copied again.

### Final image-generation prompt

```text
Use case: stylized-concept.
Asset type: production-ready 16:9 Ren'Py visual-novel title-screen background, a clean environment plate with absolutely no UI baked into it.

Reference roles:
- Image 1 is the primary canon style reference for ENTER M interior linework, hand-painted wood/material detail, clean perspective, and restrained but varied color. Do not copy its cafe architecture, furniture layout, or plants.
- Image 2 is the canon reference for evening warm/cool exposure and coherent lived-in hobby clutter. Do not copy its room architecture.
- Image 3 is a Matsuda Akai character palette/personality reference only. Do not draw Matsuda or any person.

Primary request:
Create a completely new empty bedroom belonging to Matsuda Akai at early evening. The surface feeling is calm, intimate, and compatible with a lo-fi beat. On a slower read, the room seems unable to settle on one identity: mystery reader, sports-car obsessive, programmer, gamer, athlete, former child performer, meticulous organizer, and impulsive collector all coexist without becoming a themed bedroom.

MANDATORY STRUCTURAL DIFFERENCE:
This must NOT resemble a conventional centered bedroom composition. Do not put a bed beneath a centered window and do not put a desk beside that bed. Use a clearly different, asymmetrical L-shaped plan and diagonal camera:
- camera just inside the doorway at about eye level, looking diagonally across a long room;
- the single bed runs toward the camera along the LEFT SIDE WALL, strongly foreshortened, with its headboard on the distant wall;
- a low open bookcase/room divider separates the sleeping strip from the work zone;
- the work desk runs ALONG THE FAR-RIGHT WALL beneath a wide HORIZONTAL CORNER WINDOW that wraps toward the back wall;
- window and desk are off-center on the right, never behind the bed;
- include a shallow recessed wardrobe or alcove in the far-left corner so the silhouette of the room is visibly irregular rather than a plain rectangle.
Keep straight verticals and believable contemporary architecture.

Color and atmosphere:
Avoid monochrome brown-and-blue. Use a calm but unmistakably varied Matsuda palette: one deep muted teal painted wall, warm cream adjacent walls, walnut and pale ash wood, a muted coral-red duvet or folded throw, petrol-blue bedding, a small ochre/mustard rug, burgundy paper accents, cool indigo sky, and amber practical light. The colors must be visibly distinct while remaining sophisticated, slightly desaturated, and restful. No neon or cyberpunk color wash.

Specific prop storytelling, all clearly visible and anatomically/perspectivally correct:
- The laptop on the right-wall desk is OPEN and visibly displays a generic dark-theme IDE/code editor: orderly panes and short colored syntax lines in teal, coral, violet, and soft yellow, but NO readable words, real code, logos, or brands.
- Beside it is an unmistakable small MODEL SPORTS CAR on a simple rectangular display plinth: a low-slung modern performance coupe/supercar silhouette, long low hood, compact cabin, four correctly aligned black tires with silver rims, symmetrical headlights, clean body panels, one coherent rear spoiler, accurate perspective. It must look like a deliberately manufactured scale model, not a warped toy, melted car, ordinary sedan, or full-sized vehicle. No glass display case.
- A wall rail holds several nondescript SILVER medals only: cool metallic silver discs with believable ribbons in teal, navy, burgundy, and white. Every medal is silver—absolutely no gold, yellow-metal, bronze, trophies, cups, or first-place symbols.
- Add a fuller but curated poster wall showing her other hobbies with no readable text: one generic motorsport/sports-car graphic, one stylized mystery/noir illustration, one retro video-game/fantasy cabinet-art image, and one abstract synth/music waveform-as-art poster. These are normal printed posters, not monitors or UI panels.
- Include short runs of mystery novels with abstract unlettered spines, one generic car magazine, a controller and two game cases, compact headphones, squared sticky-note clusters, graph paper, and clean white gloves placed together.
- Preserve the character contradiction: notebook, medals, and desk islands are precisely aligned; a bowed shopping bag and an overflow stack of nine-ish books beside the divider are untidy at the larger scale.
- Optional tiny nod to former performance work: a single clapperboard-shaped bookend or blank storyboard strip, with no photo, face, child image, celebrity shrine, or readable production title.

Composition for interface:
True wide 16:9. Reserve roughly the LEFTMOST 390 pixels of a 1280x720 crop as medium-dark, lower-detail overlay-safe space, but it must still be recognizable room architecture rather than a black panel. Put the most important personality props, IDE laptop, model sports car, posters, and silver medal rack in the center-right and right half so UI cannot cover them. Leave the top-left corner quiet enough for a small existing game logo. No baked panel, button, title, words, logo, border, or menu.

Style/medium:
Match ENTER M backgrounds: polished 2D anime visual-novel environment painting with grounded softly rendered realism, controlled clean edges, moderate hand-painted texture, coherent object geometry, natural atmospheric perspective, and subtle linework. Not photorealistic, not 3D CGI, not watercolor, not sketchy.

Lighting:
Blue hour outside the corner window, with cool indigo ambient light. A warm articulated desk lamp and a small warm wall sconce create balanced pools of amber. The open laptop adds only a faint neutral glow; it does not light the whole room. Calm, inhabited, slightly wistful—not gloomy, horror-coded, ominous, or abandoned.

Hard constraints:
Empty cast. No person, silhouette, face, body reflection, portrait, family photo, second bed, centered bed-under-window layout, MC-bedroom geometry, dorm bunk, luxury mansion, streamer RGB setup, radio tuner, broadcast studio, waveform interface, terminal, scanlines, glitch effect, supernatural anomaly, plant used as generic decoration, real brand, readable generated text, garbled letters, signature, watermark, or baked UI. Ensure the model sports car, open laptop, ribbons, furniture, hands-free gloves, chair, wheels, window mullions, and room perspective are coherent and not duplicated or malformed.
```

## Motion and performance

- Main Menu, shared shell, Credits rules, and Records preview use short entrance
  or content-change transforms that settle.
- The old Data Bank monitor sweep was removed.
- Room-family entry, intra-menu, return-to-title, and return-to-game paths use a
  0.30-second dissolve rather than CRT power choreography. History, Calendar,
  and About are included in that routing.
- Credits retains its authored curtain, recolored from terminal cyan to coral
  and teal.
- Archive and Arcade transition mappings are unchanged.

## Validation

- `git diff --check` passes for every task-scoped source and tool file. Git
  reports only existing LF-to-CRLF working-copy advisories.
- `python -B tools/check_screens.py` passes: 293 screens defined, 263 distinct
  names referenced, every reference resolved.
- `python -B tools/check_dev_hub_contracts.py` passes: 11 function buttons and
  2 screen buttons.
- `python -B tools/test_matsucoin_deferred_receipts.py` passes.
- Direct embedded-Python MatsuPy compile passes after the final integration:
  0 unreachable items across 124 source files.
- MatsuPy lint exits 0. Its missing Monika room, Natsuki MPT, splash,
  notebook/glitch, blood, and BSOD assets are established project warnings; no
  warning names a room-family source or asset.
- The first direct compile attempt collided with the user's already-open
  MatsuPy singleton. The valid run used a project-local temporary directory,
  avoiding the launcher lock without terminating the user's process.
- `main_menu_matsuda_evening.png` probes as 1280x720 RGB24.
- All six selector sources probe as 112x56 RGBA.
- The real title lifecycle and a real started-game/pause context were launched
  with an external search-path probe, isolated saves/persistent data/log/temp
  directories, splash skip, and dummy audio. The title run retained
  `main_menu == True`; the pause run used `Start` to leave the menu context and
  exercise the actual `main_menu == False` shell. Both captured and quit
  automatically.
- The runtime log confirms the GL2 renderer, NVIDIA hardware, windowed mode,
  and exact virtual/physical/drawable size of 1280x720.

Live evidence:

- `docs/ui/evidence/2026-08-30-main-menu-room-family-live-gl2.png`
- `docs/ui/evidence/2026-08-30-settings-room-family-live-gl2.png`
- `docs/ui/evidence/2026-08-30-records-room-family-live-gl2.png`
- `docs/ui/evidence/2026-08-30-credits-room-family-live-gl2.png`
- `docs/ui/evidence/2026-08-30-history-room-family-live-gl2.png`
- `docs/ui/evidence/2026-08-30-calendar-room-family-live-gl2.png`
- `docs/ui/evidence/2026-08-30-about-room-family-live-gl2.png`
- `docs/ui/evidence/2026-08-30-confirm-room-family-live-gl2.png`
- `docs/ui/evidence/2026-08-31-confirm-yes-hover-live-gl2.png`
- `docs/ui/evidence/2026-08-31-confirm-no-hover-live-gl2.png`

The reusable external probe is `tools/probes/menu_family_capture.rpy`. It is not
inside `game/` and is therefore absent from normal runtime/build discovery.
