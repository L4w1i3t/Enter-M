# Main-Menu Bedroom Artifact Cleanup

Date: 2026-08-31

## Outcome

The Matsuda evening-bedroom plate received a forensic redraw followed by a
canon-style repaint. The final image keeps the established calm blue-hour
room, character palette, hobby cues, menu-safe left side, and warm/cool
lighting while removing the visible generative construction errors. A rejected
intermediate was too glossy and product-rendered; the selected revision instead
uses the matte, softly painted material language of the shipped backgrounds.

The live asset remains:

`game/assets/gui/menu/main_menu_matsuda_evening.png`

The selected high-resolution master is retained at:

`docs/ui/evidence/2026-08-31-main-menu-bedroom-clean-master.png`

## Corrected construction

- The bed is now a genuinely narrow single bed with separate mattress,
  pillow, duvet, throw, frame, and sewn hems.
- The bed no longer blocks the recessed wardrobe. A continuous floor approach
  reaches the hanging rail and drawer tower.
- Wardrobe garments, hangers, luggage, boxes, rails, drawer fronts, and pulls
  have discrete silhouettes and coherent support geometry.
- The loose and shelved books are rigid volumes with coherent covers, page
  blocks, independent contact, and no generated title text.
- The shopping bag is opaque folded paper with one unambiguous visible handle;
  its second handle is tucked inside. The glassy/X-shaped gusset artifact is
  gone.
- The clapperboard is one flat hinged slate. Its neighboring black case has a
  separate outline, air gap, top plane, and shadow.
- The low bookcase, storage bins, L-desk join, drawer pedestal, chair, floor,
  and rug now agree with the room's perspective and material language.
- The laptop is a physically coherent machine open to a generic dark IDE with
  abstract syntax blocks rather than generated pseudo-code.
- The headphones are one complete two-cup set. The larger face-up controller
  now has one connected two-grip shell, two sticks, one cross-shaped D-pad,
  and four distinct coral face buttons that survive the 1280x720 reduction.
- The model is unmistakably a miniature red sports car with circular wheels,
  a supported rear wing, and clean contact on a perspective-correct plinth.
- The desk holds exactly two distinct, anatomically coherent five-digit white
  gloves with separate cuffs.
- Four coordinated hobby posters now cover motorsport, mystery, fantasy/games,
  and music. The poster car is a vintage teal rally car rather than a duplicate
  of the red desk model.
- The rack holds exactly five cool-silver medals. The window corner, mullions,
  sill, and dusk glazing read as one built structure.
- Matte plaster, satin wood, diffuse fabric, lifted charcoal/brown shadows,
  selective detail, and broad highlights now match `bedroom.png`,
  `kitchen_evening.png`, and `living_room_tabletop_night.png`. Shine is limited
  to plausible glass, metal, screen, and painted-model accents.

## Repair sequence and provenance

The built-in image-generation editor was used in precise-object-edit mode. Each
pass used the previous accepted high-resolution result as its sole target and
froze non-target areas.

| Pass | Selected raw output | Scope |
|---|---|---|
| 1 | `exec-1ee7c3b2-1663-4390-875c-a900d432962f.png` | Desk props, car, gloves, controller, headphones, laptop, chair |
| 2 | `exec-3818e36f-6be3-4c29-88a3-8a80795be89c.png` | Bedding, wardrobe contents, books, shelf, bag, clapperboard, rug |
| 3 | `exec-863b7130-c7e3-402a-9b80-8b5bb1913c7f.png` | Bed/wardrobe access and revealed floor |
| 4 | `exec-0d901631-0b30-45a5-a1f8-cf6856ed49af.png` | Posters, medals, and window construction |
| 5 | `exec-30d8b7c9-5a6d-4664-bcea-1cfd2062985a.png` | Bag, clapperboard separation, and rug material |
| 6 | `exec-adb3544a-4749-4c0d-8384-913bf044f674.png` | Simplified bag and low-pile rug; rejected later for global gloss |
| 7 | `exec-1137eb00-3c6f-45ca-afb4-5bb298125c3a.png` | Full canon-style repaint using three shipped background references |
| 8 | `exec-514f72f0-1eec-4732-8b43-2d5f1dc1154a.png` | Larger controller footprint, local notebook/case spacing; selected master |

The final controller used the isolated matte geometry reference
`exec-6221840a-0952-44ee-b26c-307a640f4770.png`.

All raw outputs are 1672x941 RGB24. The final runtime derivative was produced
with a single Lanczos resize to 1280x720, square pixels, RGB24.

Final hashes:

- High-resolution master SHA-256:
  `9B17A88939A024D99EB0DDC812F81D0A0CD584EE6E5701B9FC8D6DFC6911838F`
- Runtime PNG SHA-256:
  `FB5545A069A6C02A9E2CA5810C7E4D928327A20F472005E2E0D39671556AD409`

## Final selected edit brief

```text
Use case: precise local desk-prop relayout and controller replacement in a
finished 1672x941 visual-novel background.

Image 1 is the sole target room and rendering style. Image 2 is the exact
controller design reference. Preserve the entire room except the small desk
cluster containing the open spiral notebook, malformed controller, and two
blue game cases.

Erase the malformed controller and restore the satin wood beneath it. Shift the
notebook modestly left and stack the two blue cases at the far right so nothing
overlaps. Place one larger face-up matte-charcoal controller between them,
approximately 138–148 by 62–68 pixels at final 1280x720 size. Use one connected
two-grip shell, two circular sticks, one cross-shaped D-pad, four separate coral
face buttons, small center controls, and a soft close contact shadow. The
silhouette, D-pad, and four-button group must remain readable after reduction.

Match the room's matte softly painted 2D anime/VN finish. No glossy product
rendering, extra controls, detached geometry, cable, logo, text, symbols, hands,
or changes outside the local notebook/controller/case cluster.
```

The isolated guide was deliberately retro-simple to keep the D-pad and face
buttons legible. The selected room edit resolved it as a plausible modern
dual-stick pad instead; native-resolution QA accepted the result because it has
one connected two-grip shell, two sticks, one cross D-pad, four distinct face
buttons, and no malformed or ambiguous appendages.

## Delivery-scale QA

The selected master was downsampled first, then audited at the actual 1280x720
delivery resolution rather than accepted from the generator preview.

Independent visual passes covered:

- left/center architecture and props;
- desk/right prop anatomy and contact geometry;
- upper-wall, window, global perspective, palette, and style consistency.
- direct comparison against three shipped backgrounds for matte material and
  lighting consistency;
- a controller-specific native-resolution check of silhouette and control
  topology after the final local relayout.

All three passes reported no remaining delivery-scale blocker. The final
standalone plate was also checked at source resolution to make sure the resize
was not hiding duplicated anatomy or fused object silhouettes.

## Runtime validation

- `main_menu_matsuda_evening.png` probes as 1280x720 RGB24 with square pixels.
- Direct embedded-Python MatsuPy compile exits 0 with 0 unreachable items
  across 124 source files. The first sandboxed compile was discarded because
  it could not refresh shared SDK common-script caches; the clean rerun had no
  permission tracebacks.
- Direct MatsuPy lint exits 0. Its missing Natsuki MPT, splash, notebook/glitch,
  blood, and BSOD assets are established project warnings; none names the
  revised menu background.
- The external title probe launches the real main-menu lifecycle with isolated
  saves and persistent data, renders through NVIDIA GL2, captures the real
  `screen main_menu`, and quits automatically.
- The renderer reports virtual size 1280x720. Windows supplied a 1274x717
  drawable and Ren'Py saved 1274x716; this is the established windowed-capture
  artifact, not a source-asset resize.
- The live frame was checked for matte material consistency, background crop,
  menu contrast, corrected controller legibility, prop integrity, and
  unobstructed right-side composition.

Live evidence:

`docs/ui/evidence/2026-08-31-main-menu-bedroom-matte-live-gl2.png`
