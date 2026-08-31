# Main-Menu Bedroom Canon Rerender

Date: 2026-08-31

## Outcome

`game/assets/gui/menu/main_menu_matsuda_evening.png` has been rerendered and
reinstalled as a polished evening-bedroom plate. The new image preserves the
established room layout and title-screen light anchors while replacing the
previous all-over muddy surface treatment with the controlled material finish
used by the shipped background family.

The desk props were also rebuilt at delivery scale:

- the controller is one compact matte-charcoal shell with two grips, two
  circular sticks, one cross D-pad, four separate coral face buttons, and
  small centered controls;
- there are exactly two small white wrist-length fashion gloves;
- each final glove has exactly five total digits: four fingers and one thumb;
- both gloves use smooth thin fabric, narrow cuffs, restrained folds, and soft
  contact shadows rather than beige, padded, tactical, driving, or work-glove
  construction.

This report supersedes the selected-art claims in
`docs/ui/2026-08-31-main-menu-bedroom-artifact-cleanup.md`. That earlier pass
was useful construction work, but the runtime PNG and high-resolution master
recorded here are the current authoritative assets.

## Style contract

The finish was matched against these shipped project backgrounds:

- `game/assets/backgrounds/kitchen_evening.png`
- `game/assets/backgrounds/house_evening.png`
- `game/assets/backgrounds/residential_night.png`
- `game/assets/backgrounds/bedroom.png`
- `game/assets/backgrounds/living_room_tabletop_night.png`

The shared target language is polished matte 2D anime/VN background art:
clean controlled edges, broad tonal gradients, localized material texture,
restrained saturation, lifted colored shadows, and selective highlights on
metal, glass, screens, and painted model surfaces. Plaster, cloth, wood, and
paper stay diffuse. The rerender deliberately avoids uniform canvas noise,
oily micro-mottle, muddy stippling, and product-render gloss.

## Composition and integration constraints

The existing architecture, window, desk, wall art, lamp, laptop, and music
poster positions were preserved because `game/main_menu_fx.rpy` attaches its
additive light regions to those painted coordinates. The title implementation
also applies a centered 1.028 zoom and, in Full Atmosphere, small positional
drift. The corrected props retain safe right-edge clearance under that motion.

The left side remains compositionally quiet because the live title places a
430-pixel navigation block over it. No source wiring was changed. The same PNG
continues to feed:

- `enter_m_main_menu_bg` and the interactive title screen;
- the drifting `menu_bg` used by title-context secondary screens;
- Credits and the room-family menu context;
- the intro and content-warning cold-open plates.

## Generation and compositing provenance

Mode: built-in image-generation editor, followed by deterministic FFmpeg
masking, compositing, and one final Lanczos delivery resize.

| Output | Use |
|---|---|
| `exec-3a4b8096-54f7-4c41-9020-eff2c5a3e712.png` | Selected clean global room repaint and material pass |
| `exec-4228bec4-d37b-470a-9d41-337108b311c0.png` | Clean high-resolution room base with the old desk controller/gloves removed |
| `exec-1136f7b1-1a55-485f-9c83-bf42328bd38e.png` | Controller topology reference |
| `exec-a56633ee-5059-40fa-9720-3d368ad5102b.png` | Two topology-locked five-digit glove sources |
| `exec-744759bd-faef-46b8-b209-3a426ae70897.png` | Rejected local prop pass; its glove silhouettes had five fingers plus a thumb |
| `exec-e8478800-d775-4377-9e9c-427f75005df7.png` | Controller-only desk pass after removing the rejected gloves |
| `exec-6d2db26d-4fb7-41cb-87b3-f42bab3d46c2.png` | Selected local polish pass using the locked four-fingers-plus-thumb silhouettes |

The final desk region was rendered as a large focused crop so the controller
controls and glove anatomy were not compressed into a full-room generation.
The exact glove sources were chroma-keyed into RGBA, rotated and scaled as
separate layers, and placed on the controller-only desk crop. The final local
editor pass harmonized their folds, warm edge light, cool-white midtones, and
contact shadows. A feathered 320x220 patch was then composited into the clean
1672x941 room base. This retained the exact room geometry and prevented a
visible rectangular seam.

The first focused prop candidate was not accepted. A close inspection showed
that both gloves contained six projections: five long fingers and a thumb.
The final candidate instead starts from deterministic silhouettes containing
four fingers and one thumb, and the accepted editor output preserves those
outlines. This correction was verified again at both master and runtime size.

## Final prompt set

The global-room brief used the existing plate as the structural target and the
five shipped backgrounds above as finish references. It froze the architecture
and light-source geography, removed global muddy texture, retained warm/cool
evening exposure, and reserved fine texture for material-specific details.

The controller brief specified one connected compact charcoal shell, exactly
two sticks, one cross D-pad, four separate muted-coral buttons, two small center
controls, no cable, no logo, and desk-matched three-quarter perspective.

The final glove-polish prompt was:

```text
Polish the first image as a tightly controlled local visual-novel background
edit. Preserve the exact crop, camera, desk geometry, wood grain, notebook,
car stand, blue game case, chair, drawers, and the controller pixel-position
and exact controls. The only intended refinement is to harmonize the two
existing small white gloves with the scene lighting and painterly finish.

Critical topology lock: there are exactly two separate gloves already
present. Preserve both existing glove silhouettes and positions. Each glove
must contain exactly five total digit projections: one thumb plus four
fingers, never five fingers plus a thumb. Do not add, split, duplicate, fork,
overlap, hide, merge, or remove any digit. Keep the current small scale,
wrist-length narrow cuffs, flat empty shape, and clear separation between the
gloves.

Add restrained fabric folds, warm desk-lamp edge light, cool-white midtones,
and soft physically coherent contact shadows so the gloves look painted into
the same polished matte 2D anime/VN background. No beige leather, tactical
panels, padding, bulky work gloves, arms, hands inside, people, extra objects,
text, logos, watermark, muddy texture, or global grain.
```

## Final assets

- High-resolution master:
  `docs/ui/evidence/2026-08-31-main-menu-bedroom-canon-rerender-master.png`
  - 1672x941, RGB24
  - 1,995,819 bytes
  - SHA-256:
    `92492944FDB831950A91610FFA6EB5509F5A1E6FFA5666CCE5ECF1CE6B0FCBB9`
- Shipping runtime PNG:
  `game/assets/gui/menu/main_menu_matsuda_evening.png`
  - 1280x720, RGB24
  - 1,221,913 bytes
  - SHA-256:
    `DC247009482537A63F53A8A148489B3237BB5DAA31877B7673F493DCF181225C`

The runtime image is a single Lanczos derivative of the final master. There is
no additional crop, sharpening pass, or intermediate runtime resize.

## Delivery-scale topology audit

The accepted 1280x720 image was inspected directly rather than inferred from
the high-resolution generation preview.

- Upper/left glove: four separate leftward fingers plus one distinct down-left
  thumb; five total.
- Lower/right glove: four separate leftward fingers plus one distinct up-left
  thumb; five total.
- A wood-colored gap separates the gloves, so their contours do not merge into
  an extra projection.
- Both gloves retain narrow open cuffs, thin fabric, small scale, and separate
  contact shadows.
- The controller remains a single coherent two-grip body with two sticks, one
  cross D-pad, and four readable coral buttons.
- No patch edge, halo, tonal jump, or wood-grain discontinuity is visible.

## Runtime validation

The external probe at `tools/probes/main_menu_rerender_capture.rpy` loads only
when its dedicated environment variable and search path are supplied. It is
not part of a normal build.

The final plate was exercised through the real MatsuPy/Ren'Py GL2 path:

- process exit: 0;
- content reachability: 0 unreachable items across 125 source files;
- renderer: NVIDIA GL2;
- virtual resolution: 1280x720;
- windowed drawable: 1274x717;
- saved screenshots: 1274x716, the established Windows window-border capture
  artifact rather than a source-asset resize;
- Atmosphere Off, Light, and Full all preserve the lamp, laptop, poster, and
  window light alignment;
- Credits and both direct cold-open screen consumers render without cropping,
  seam, or contrast regressions.

Live evidence:

- `docs/ui/evidence/2026-08-31-main-menu-bedroom-rerender-off-live-gl2.png`
- `docs/ui/evidence/2026-08-31-main-menu-bedroom-rerender-light-live-gl2.png`
- `docs/ui/evidence/2026-08-31-main-menu-bedroom-rerender-full-live-gl2.png`
- `docs/ui/evidence/2026-08-31-main-menu-bedroom-rerender-credits-live-gl2.png`
- `docs/ui/evidence/2026-08-31-main-menu-bedroom-rerender-intro-live-gl2.png`
- `docs/ui/evidence/2026-08-31-main-menu-bedroom-rerender-warning-live-gl2.png`

The MatsuPy compile and lint runs both exit 0. Lint retains the project's
established missing Natsuki MPT, splash/end, notebook/glitch, blood-drop, and
BSOD warning families; none names this rerender or its probe. Project contract
checks also pass:

- `python -B tools/check_screens.py`
- `python -B tools/check_dev_hub_contracts.py`
- `python -B tools/test_matsucoin_deferred_receipts.py`

