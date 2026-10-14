# ENTER M Background Art Bible

Design/provenance reference retained September 25, 2026. Fixed landmarks and
camera relationships remain authoring guidance. Current registered variants
and filenames come from `game/asset_definitions/def_images.rpy`; historical
production inventories below are not a runtime asset audit.

This file is the source of truth for the story-canon background families. It
records spatial invariants, rendering language, selected generation outputs,
and the prompt set used for the August 26-27, 2026 replacement pass.

October 12, 2026 approved polish covered the rooftop and both grocery plates.
The `_polished_20261012.png` filenames from that pass are historical; current
declarations use `rooftop.png`, `store_checkout.png`, and `store_techsection.png`.

October 14, 2026 rooftop cleanup replaces `rooftop.png` in place with cleaner
concrete, coherent distant buildings, and clearer fixture detail. Both benches,
the full left/far perimeter fence, the stairwell, and service equipment remain.
The pre-edit plate, generation prompts, and validation details are preserved in
the [dated cleanup report](rooftop_cleanup_2026-10-14/README.md).

## Authority and scope

- **STORY-CANON** assets live in `game/assets/backgrounds/` or `game/assets/backgrounds/` and
  are defined as `bg ...` images. Their geometry is authoritative.
- **OP-DERIVED** shots may crop, pan, or grade a story-canon plate, but may not
  invent a second version of the same location. The OP aliases now consume the
  shared house, kitchen, residential, city, and library plates.
- **RETROSPECTIVE / OTHER LOCATION** plates such as `doorday`, `doornight`, and
  `doordark` are not the current family entry. The current house uses
  `home_entry_day` and `home_entry_night`.
- A time suffix means the exterior light visible in the plate materially
  changes. `atmos()` may grade a plate, but it must not repair incompatible
  geometry.

## Shared rendering language

> Polished 2D anime visual-novel environment painting; softly rendered realism
> with clean controlled edges; moderate material texture; natural atmospheric
> perspective; restrained saturation; warm practical lighting; contemporary
> Japanese-adjacent suburban/civic architecture; no photographic texture,
> glossy CGI look, real logos, baked-in people, watermarks, or garbled signage.

All shipping plates are 1280x720 sRGB PNGs. Cameras use an approximately 35 mm
eye-level perspective, straight verticals, and an open lower/central stage for
sprites and dialogue UI. Time and weather variants reuse the same camera,
architecture, furniture, and permanent props; only sky, illumination,
reflections, and justified weather change.

## Spatial families

### House

```text
street -> gate -> short path / worn yard / swing -> front entry
                                                   |
                                        living + dining core -> galley kitchen
                                                   |
                                               stairs upstairs
                                                   |
                                      MC room / Asahina room / Himeko room
```

Immutable landmarks:

- Exterior: compact yard, swing with dirt wear, single dark door plus sidelight,
  front living/dining window, kitchen window, close neighbors, utility wires.
- Entry: matching single door/sidelight, shoe step and cabinet, stairs at right,
  umbrella stand, Himeko's work coat/tote, Asahina's volleyball bag, family memo
  rail. It connects to the same downstairs core.
- Living wide: kitchen corridor is the only rear-left passage. The wall behind
  the dining table is continuous; there is no right-hand doorway.
- Dining: same kitchen corridor left, uninterrupted memo wall behind, wide
  multi-drawer walnut sideboard right. The memo rail always has four items:
  family photo, volleyball image, calendar, child drawing. The sideboard always
  carries two small photos, a burgundy thermos, and a closed navy folder/laptop.
- Dining table: exactly four identical plain walnut ladder-back chairs, one
  centered on each table edge. Himeko uses one head; the siblings sit opposite
  on the long sides; the other head remains the habitual empty fourth chair.
- Kitchen: narrow galley aligned with the living/dining corridor, refrigerator
  left, slatted rear door centered, sink/window right. Keep work surfaces mostly
  open because the script supplies food and notes dynamically.
- MC bedroom: bed/window center, desk right, shelves left. Persistent dressing
  is JRPG hardware/games, writing and school material, alarm/coin jar/charger,
  running shoes and recovery basket, backpack, and a uniform shirt. No trophies,
  luxury gaming rig, or plant décor.

Household dressing is practical, maintained, and slightly worn. Himeko's legal
work, Asahina's volleyball/design gear, MC's games/writing/running gear, small
three-person photos, the wall scuff, and the battered game under the television
replace generic botanical prints and repeated potted plants. Tables stay usable.

### Itsuki Academy

- Track: the six-lane curve, central four-story classroom block, left equipment
  shed, perimeter fence, field, high-jump mat, light poles, and right-side gym
  are fixed. Late-May trees carry full green foliage, never spring blossom. The
  gym is a shallow-gabled rectangular building whose roof and high window band
  agree with the interior trusses and clerestory.
- Track evening: an illumination-only continuation of the day camera. The sun
  lowers at camera-left and shadows lengthen; lane count, buildings, field
  equipment, trees, and crop do not move. No full-night track scene is authored.
- Rooftop: the dry, pale-gray service roof keeps a broad clear lunch-stage at
  center, fence and skyline to the left/far side, two institutional benches along
  the shaded sitting wall, and the compact stairwell block in the right third.
  That block has one gray steel door with a wired-glass upper pane, a shallow rain
  hood, a narrow exterior window immediately left, and a fixed maintenance ladder
  immediately right. HVAC, drains, conduit, bins, safety paint, and light wear
  make it a working school roof without turning it into a glossy patio or garden.
- Rooftop landing: `rooftop_door` is the reverse camera from *inside* that compact
  top stairwell, looking through the same door as it opens outward. Consequently,
  the interior hinges are screen-left and handle screen-right, while the exterior
  west-side window appears on the viewer's right wall. After a character steps
  fully outside and closes the door, cut back to `bg rooftop`.
- Gym: the shallow-gabled steel truss roof and clerestory correspond to the track
  exterior. The assembly setup includes one lowered projector screen to the left
  of the stage, leaving the podium and proscenium clear.
- Cafeteria: furniture and camera stay fixed. Its current authored use is October
  30, so the exterior trees are mostly bare with sparse rust-gold leaves. The
  sunlit plate has long diagonal lunch-hour sunbars; the dim plate removes them
  without moving any furniture when the prose says the light leaves the room.

### Residential corner

The nearby road slopes toward the distant city. The first left frontage is a
tiny neighborhood shop with one white-and-muted-blue vending machine occupying
about half the pedestrian strip; the adjacent fence post supports the May 17
collision. Day and night keep the same road curve, houses, fences, manhole,
railing, poles, wires, trees, shop, and vending machine.

### Downtown

The city master is one walkable historic district:

```text
residential slope -> station/bus route -> historic bank/cafe/bookstore block
                                      -> crosswalk -> library steps
                                      -> shopping stretch -> Velvet Cinema
```

The public library is the raised civic building on the left. The pale old bank,
bookstore/cafe frontage, black lamps, crosswalk, bus stops, and distant
`VELVET CINEMA` marquee persist in morning, day, blue hour, and rainy night.
Green-and-white livery establishes the route, but the bus is transient: it is at
the stop in the day plate and absent at the other times. The night plate is
intentionally rainy and wet because its current story consumer is an umbrella
scene.

### Public library

The story plate is the renovated second floor of the downtown civic library:
carpet, tall street-facing windows, pale morning rectangles, medium study
tables, two adjacent burgundy padded chairs and a color-coded sticky-note row in
the foreground, public stacks, and an implied stair/printer route. It is not a
mirrored bookstore, reception desk, or OP-owned alias. Current use is 9 a.m.
through noon, so no night plate is required.

### Supermarket media and craft department

The store is one coherent, ordinary supermarket rather than a specialty shop.
The browsing camera looks down a broad general-merchandise cross-aisle: two
utilitarian game/electronics gondola bays and one locked case are on the left,
craft supplies are on the right, cleaning/pantry gondolas continue through the
middle distance, and carts, baskets, front windows, and checkout circulation
anchor it unmistakably as a supermarket. `store_checkout` moves to the same
front end and shows one conventional staffed lane with conveyor, scanner/scale,
POS, printer, card terminal, bagging deck, cart guide, and adjacent numbered
lanes. Its cashier position is unambiguous: a recessed employee well with a
black anti-fatigue mat and open right-side access gate. The POS screen sits on
the right return and faces down-left into that well; the separate payment
terminal faces the customer. Both cameras keep the same cream fluorescent
ceiling, pale warm tile, gray metal fixtures, medium-walnut laminate, muted
burgundy accents, soft daylight, and simplified painted merchandise. Story
purchases and bags remain dynamic, never baked into either plate.

### Velvet Cinema

- Exterior: compact burgundy/walnut/brass art-deco neighborhood cinema, two
  ticket machines, cream-and-burgundy `VELVET CINEMA` marquee, a fabric
  `IRON ROD` premiere banner, and the two canonical campaigns.
- `MIGHTY LIGHTNING SQUAD`: five color-coded heroes and bright action key art.
- `IRON ROD`: restrained rusted-rod horror key art. The exterior presentation
  reads as the banner/campaign referenced by the story.
- Lobby: same two key-art designs, concession counter, antique equipment case,
  and an obvious open route marked Theater 3.
- Auditorium: same burgundy/walnut/brass materials, blank screen for
  `theater_fx.rpy`, unobstructed plain exit door, no poster mounted to the exit.

## Variant matrix

| Family | Day / morning | Evening | Night / weather |
|---|---|---|---|
| House exterior | `bg house` | `bg house_evening` | `bg house_night` |
| Entry | `bg home_entry_day` | grade only | `bg home_entry_night` |
| Living | `bg living_room` | grade only | `bg living_room_night` |
| Dining | `bg dining_table` | grade only | `bg dining_table_night` |
| Kitchen | `bg kitchen` | `bg kitchen_evening` | `bg kitchen_night` |
| MC bedroom | `bg bedroom` | grade only | `bg bedroom_night` |
| Residential corner | `bg residential_day` | grade day plate | `bg residential_night` |
| School track | `bg track_day` | `bg track_evening` | not warranted |
| School rooftop | `bg rooftop`, `bg rooftop_door` | not warranted | not warranted |
| School gym | `bg schoolgym` | not warranted | not warranted |
| Cafeteria | `bg cafeteria_winter` | `bg cafeteria_winter_dim` (light change) | not warranted |
| Downtown | `bg city_morning`, `bg city_day` | `bg city_evening` | `bg city_night` (rain) |
| Library interior | `bg library` | not warranted | not warranted |
| Supermarket department | `bg store_techsection`, `bg store_checkout` | not warranted | not warranted |
| Theater | `bg theater_day`; time grade | not separately warranted | not warranted |

## Final prompt set

Every base prompt began with the shared rendering language above and these
technical constraints: `16:9, 1280x720 delivery, approximately 35 mm eye-level
camera, straight verticals, sprite-safe center/lower frame, empty cast, no real
brands, no illegible signage, no photographic or glossy-CGI texture`.

Asset-specific prompt clauses:

- **House exterior:** modest two-story three-person home; compact worn dirt/grass
  yard; swing and dirt patch; single door plus sidelight; large front family-room
  window; kitchen window; gate/path; neighboring houses and utility wires; no
  decorative planters.
- **Entry:** same door/sidelight and downstairs proportions; genkan step, shoe
  storage, stairs, umbrellas, practical footwear, Himeko workwear/tote, Asahina
  volleyball duffel/kneepads/bottle, restrained four-item family memo rail.
- **Living/dining:** fixed open-plan geography documented above; dark television;
  mostly clear tables; family photos, work bag, volleyball bag, wall scuff,
  console/controller and battered family game beneath TV; dining inventory and
  four-chair rule locked exactly between cameras.
- **Kitchen:** narrow galley from the living-room corridor; practical appliances,
  reusable containers, three-person fridge schedule, mugs and radio; clear work
  area; no static plate or plant décor.
- **MC bedroom:** ordinary senior's room with modest JRPG setup, writing/study
  drafts, alarm/coin jar/charger, running/recovery gear and school bag; no medals,
  deluxe PC, plant art, or pristine collector display.
- **School track:** preserve the six-lane curve and classroom-block camera;
  replace spring blossom with late-May green foliage; make the right gym a
  shallow-gabled exterior compatible with its trussed interior. The evening
  plate is geometry-locked and changes only low sun, sky, and shadows.
- **Rooftop:** dry working school roof with a broad sprite-safe concrete stage;
  fence, skyline and distant mountains; shaded sitting wall and two institutional
  benches; right-third stairwell block with one wired-glass steel door, left-side
  exterior window, right-side ladder, plus restrained HVAC, drains, conduit,
  bins, safety paint, scuffs, and rust. No planters or wet patio finish.
- **Rooftop door:** compact top stairwell from inside, final three steps and
  landing facing the same open outward-swinging wired-glass steel door; interior
  hinges screen-left and handle screen-right; the block's west window on the
  viewer's right wall; off-white concrete, navy base trim, fluorescent light,
  rail and extinguisher; open doorway reveals only matching sky and roof fence.
- **School gym:** preserve court, stage, trusses, clerestory, hoops, and podium;
  integrate one lowered matte-white assembly screen left of the stage with an
  abstract blue field and no generated wording.
- **Cafeteria:** preserve every table, chair, column, and window; replace spring
  blossom with mostly bare late-October trees. The sunlit plate carries four
  long diagonal light bars; its aligned dim continuation removes all direct sun.
- **Residential:** retain road curve/slope and dense-neighborhood material
  vocabulary; make the near-left corner shop and obstructive vending machine
  story-readable beside the collision fence post.
- **Downtown:** original historic civic district with raised public library,
  pale old bank, bookstore/cafe, green-white transit route, black lamps,
  crosswalk and distant Velvet Cinema; coherent geography, transient vehicles,
  and fictional readable anchor names.
- **Library:** renovated second-floor public library, carpet, broad windows,
  pale morning sunlight, adjacent padded study chairs, medium tables, stacks,
  distant stair/printer route; no reception-desk emphasis.
- **Supermarket media/craft:** ordinary grocery-supercenter general-merchandise
  cross-aisle first, with carts/baskets and pantry/cleaning gondolas establishing
  the store; only two game/electronics bays, one integrated locked case and a
  plain pickup counter on the left, plus one craft gondola on the right. Use cream
  ceiling tile, long fluorescent tubes, pale warm floor, gray metal fixtures,
  medium-walnut laminate and muted burgundy markers. Render stocked shelves as
  simplified painted color groups, not photographic walls of tiny packaging.
  The connected front-end camera must show one anatomically conventional staffed
  checkout lane: long black conveyor, scanner/scale, POS, receipt printer, card
  terminal, flat bagging deck, cart guide and parallel numbered lanes. Include a
  clearly recessed employee well, black anti-fatigue mat and open side access
  gate; put the POS on the right return with its screen facing into the well and
  the separate payment terminal facing the customer. Keep the belt, scanner and
  landing surface in one readable flow. No exposed wire fixtures, dangling
  ceiling hardware, blocked employee access, people, purchases, receipts, or
  filled bags baked in.
- **Theater:** one compact art-deco material sheet across exterior/lobby/auditorium;
  fixed Lightning Squad and Iron Rod campaign concepts; ticket machines,
  Theater 3 route, blank screen and unobstructed exit.

The invariant variant prompt was:

> Create the strict time/weather lighting variant of this exact background.
> Preserve camera, architecture, furniture, permanent props, count, placement,
> and crop exactly. Do not redesign, move, add, or remove anything. Change only
> sky, exterior light, practical illumination, shadows, reflections, and the
> explicitly requested weather. Maintain the identical grounded semi-realistic
> hand-painted anime visual-novel rendering.

## Provenance and selected outputs

Generation dates: 2026-08-26 through 2026-08-27. Mode: OpenAI built-in
image-generation tool. The backend model/version was not exposed. Raw outputs
remain in the tool-managed generation directory; shipping derivatives were
resized once with Lanczos to 1280x720 RGB PNGs.

| Runtime target | Selected raw output ID |
|---|---|
| `game/assets/backgrounds/bedroom.png` | `exec-988e1c99-b227-42f8-a60c-423d783d0484` |
| `game/assets/backgrounds/bedroom_night.png` | `exec-52322a42-97b7-4c3b-ae18-ca5d3ce8785c` |
| `game/assets/backgrounds/house.png` | `exec-ef4f1aa9-7e12-441c-8f0c-2c5c106ddbdf` |
| `game/assets/backgrounds/house_evening.png` | `exec-b6ef1b9b-9430-4e43-bbfc-7f30baecb82f` |
| `game/assets/backgrounds/house_night.png` | `exec-41485795-9fb8-4a91-861a-5d297146ce53` |
| `game/assets/backgrounds/kitchen.png` | `exec-743157b1-5876-402e-aca9-c70c7df9034d` |
| `game/assets/backgrounds/kitchen_evening.png` | `exec-b3169a0e-2429-4f49-96d3-e760c12ee1d9` |
| `game/assets/backgrounds/kitchen_night.png` | `exec-b4a4af9e-59bc-4379-a541-504b6f94d2c8` |
| `game/assets/backgrounds/home_entry_day.png` | `exec-4e53fa43-5a27-44d8-afaf-d8542d00a791` |
| `game/assets/backgrounds/home_entry_night.png` | `exec-9bb64018-47c1-4a0a-94cf-62f578f6a595` |
| `game/assets/backgrounds/living_room.png` | `exec-66f1e6f1-25c5-4ba2-bfa6-a05d1ba4c033` |
| `game/assets/backgrounds/living_room_night.png` | `exec-d08623e2-288c-438a-a1a6-68a84cea0ab1` |
| `game/assets/backgrounds/dining_table.png` | `exec-9595736c-e20c-42c5-96d5-b61ef6b3ffff` |
| `game/assets/backgrounds/dining_table_night.png` | `exec-96b048a5-2b03-4d0f-92b6-86513145b6be` |
| `game/assets/backgrounds/residential.png` | `exec-2bc0cf30-8a56-4f35-955f-366347a6aa7f` |
| `game/assets/backgrounds/residential_night.png` | `exec-7d90f9b6-04ef-4f9b-8b43-545c1a50a002` |
| `game/assets/backgrounds/city_morning.png` | `exec-3766f1bd-113c-43f0-83fb-dbc4be0fffa9` |
| `game/assets/backgrounds/city_day.png` | `exec-c5a94541-2298-4d0c-9d43-39ffcf9524f7` |
| `game/assets/backgrounds/city_evening.png` | `exec-46fac649-f4dc-4883-8f1a-4c78377edd3a` |
| `game/assets/backgrounds/city_night.png` | `exec-f0cf0871-fc37-4596-bc95-e29f52ce60c0` |
| `game/assets/backgrounds/library.png` | `exec-ced42e31-45d6-4436-ba9a-634c305cdc9d` |
| `game/assets/backgrounds/theater_day.png` | `exec-d0c4ce1b-79e4-44c1-9829-4a19de8dddda` |
| `game/assets/backgrounds/theater_lobby.png` | `exec-5ac8eae3-864e-4a01-a315-322c6f76dd16` |
| `game/assets/backgrounds/theater_inside.png` | `exec-3613cd16-0d8d-4b93-abfb-676424fd0394` |
| `game/assets/backgrounds/track_day.png` | `exec-86561e69-2e36-4b33-9606-f2503fa68593` |
| `game/assets/backgrounds/track_evening.png` | `exec-9d4783c5-b1ee-481f-a636-48940c7b39bd` |
| `game/assets/backgrounds/rooftop.png` | `exec-a44c6a2e-53a7-440c-8cb5-4a19ec0cf264` |
| `game/assets/backgrounds/rooftop_door.png` | `exec-768a5201-7247-4ab4-983d-db8063c269cd` |
| `game/assets/backgrounds/schoolgym.png` | `exec-8b8d48e8-e90b-4c63-a96e-efbb804d7fd3` |
| `game/assets/backgrounds/cafeteria_winter.png` | `exec-4e801150-12cb-4431-9ef1-ec9c160a656f` |
| `game/assets/backgrounds/cafeteria_winter_dim.png` | `exec-d9a55655-31e2-4584-a853-cf41c63e629c` |
| `game/assets/backgrounds/store_techsection.png` | `exec-64cfbe3e-43ae-4ee8-871c-82ba5ac02fd6` |
| `game/assets/backgrounds/store_checkout.png` | `exec-22bc7243-bf80-4584-9b94-6ba51e535e77` |

## QA gate

Before accepting another plate or variant:

1. Compare connected cameras against this file's immutable landmarks.
2. Compare time variants for identical count, placement, crop, and geometry.
3. Verify 1280x720 RGB PNG delivery and no unintended people, brands, plants,
   corrupt text, or baked story props.
4. Check every `scene bg ...` consumer and keep OP aliases downstream of shared
   story assets, never the reverse.
5. Re-measure any shader target (especially the cinema screen), compile Ren'Py,
   and run lint after integration.
