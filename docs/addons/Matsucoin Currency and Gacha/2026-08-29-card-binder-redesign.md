# Card Binder and Exterior Redesign

Date: 2026-08-29  
Status: implemented and engine-validated

## Scope

The collection screen had three related problems:

- card art was treated as a full-face image inside a plain rarity border;
- the binder used a single shallow row that crowded the paper and could not
  scale past a small subject group;
- unused layout padding was labelled `OPEN POCKET`, so even a 41/41 archive
  looked incomplete.

The detail overlay also exposed a compositing defect: tall sprite displayables
could render outside the intended art aperture and over the physical card
footer. A `Composite` has a declared output size, but it does not clip an
oversized child by itself.

## Runtime design

### Category drawer and paging

`mc_collection` now separates two pieces of state:

- `mc_sel_subject` selects the character/category from the left-leaf catalog
  drawer;
- `mc_sel_page` turns spreads inside that category.

The open binder is a 3-row by 4-column spread: two columns and three rows on
each leaf. Every spread therefore owns 12 deterministic catalog positions.
Positions fill row-major across the complete spread, so a five-card category
uses both leaves instead of stranding all five cards on the left page.
Short categories keep their unused positions as numbered clear sleeves marked
`VACANT`; they are genuine capacity, not fake missing collectibles. Categories
larger than 12 remain selected while the edge arrows paginate the next slice.
Those arrows are absent when that category has no previous or next spread.

The catalog drawer reports owned/total counts for all 12 subjects, retains NEW
indicators, resets only the category-local page when a new category is chosen,
and shields the cards behind it from click-through. Escape closes the drawer
before it closes the collection. C and I toggle the drawer; Left/Right and
PageUp/PageDown turn category-local spreads when another spread exists.

A follow-up discoverability pass replaced the ambiguous `CATALOG` stub and the
detached black subject/status plate with one 420-pixel paper divider tab on the
left leaf. It reads `CATEGORY`, the current name, owned/total cards, and the
explicit verb `CHANGE`; it receives initial controller focus and changes to
`CLOSE` while the attached drawer is open. The drawer now begins directly under
that tab and is titled `SELECT A CATEGORY`. `SPREAD x / y` is stamped on the
paper only when a category actually has more than one spread, so `P.1/1` no
longer adds permanent noise. The footer teaches `C` and click behavior, then
switches to the hovered card's full name as an inspect cue.

While the drawer is open, covered cards, page arrows, and the divider tab leave
the keyboard focus chain; the selected category row owns focus instead. The
footer simultaneously changes to Up/Down, Enter, and close instructions, so a
previously focused card cannot be activated through the modal drawer.

The divider's label, category, count, and action use four standalone local text
styles rather than inheriting `gui_text`. Their medium blue/cyan archive-ink
palette remains readable on the pale tab without turning near-black, and global
UI text-state changes cannot leak into this control or vice versa.

Pocket placement uses fixed card/sleeve coordinates. This removes the former
six-pixel real-slot/filler-slot drift, keeps hover lift inside each cell, and
keeps every sleeve inside the measured pale-paper bounds of
`binder_spread.png`. The catalog and subject controls were moved above the
first sleeve row so neither can cover a card. The grid trades three pixels of
inter-row air for six pixels of additional clearance below the divider while
preserving the bottom paper margin.

The clear pockets use the existing GL2 shader path, with a simple translucent
fallback if shader registration fails. This keeps the catalog usable on a
renderer that cannot initialize the custom sleeve shaders.

### Physical card fronts

The built-in image generator produced four 5:7 raster masters. The production
copies were normalized to 600x840 RGB, twice the largest regular card size,
which keeps detail cards sharp without loading four unnecessary 1K-class UI
textures.

Prompt briefs:

- R: empty front-facing graphite-steel Archive dossier shell, cyan circuitry,
  clipped industrial corners, dark illustration aperture, no words or logos;
- SR: empty violet arcane/circuit Archive shell, restrained luminous engraving,
  dark aperture, no words or logos;
- SSR: empty obsidian-and-gold anomaly shell, fractured prismatic foil rails,
  premium engraved hardware, dark aperture, no words or logos;
- back: face-down dark Archive record card, symmetric cyan/violet seal and
  technical linework, no words or logos.

Production assets:

- `game/assets/gui/cards/card_shell_r.png`
- `game/assets/gui/cards/card_shell_sr.png`
- `game/assets/gui/cards/card_shell_ssr.png`
- `game/assets/gui/cards/card_back_archive.png`

`mc_card_front` now builds the shared physical front as opaque stock, authored
rarity shell, clipped live illustration, then live card metadata. Its art child
is wrapped in an explicit `Crop` matching the shell aperture, which fixes the
detail-overlay bleed. Fronts are cached by card ID and output size.

`mc_card_face` remains the single consumer-facing widget, so the binder,
inspection modal, single pull, and ten-pull all use the same exterior design.
The settled binder disables animated holo work. On an inspected SSR, the shader
foil mask excludes the exact expanded illustration aperture; it no longer
washes across the portrait. Binder cards are 96x134. Their six-pixel nameplates
use deliberate compact editions such as `School U.` and `Encore` instead of
clipping a canonical title; the 300x420 detail card keeps the complete name and
full title size. The tiny binder footer serial is suppressed because it was not
legible at this physical scale.

The reveal back now uses `card_back_archive.png` through the cached
`McCardBack` displayable and the same rounded clipping shader as the fronts.

### Detail overlay

The inspected card is free-standing at 300x420 instead of resting on the old
large grey sleeve pedestal. The complete card name appears only on the physical
card; the duplicate right-column heading is now the non-redundant `ARCHIVE
NOTES`. Category, rarity, category-relative entry position, flavor text, and
duplicate value live in the Archive panel. Previous/Next navigation stays within
the selected card's category, is anchored to the bottom of the metadata column,
and supports the arrow/PageUp/PageDown keys.

## Evidence

All captures were made through the production Ren'Py 8.1.1 GL2 renderer at
1280x720 with an isolated throwaway save and a synthetic 41/41 collection. The
temporary probe source, bytecode, save data, launcher copy, and hook were
removed after capture.

- [Final 3x4 binder spread](evidence/2026-08-29-card-binder-grid.png)
- [Attached category drawer](evidence/2026-08-29-card-binder-catalog.png)
- [Single-name detail card](evidence/2026-08-29-card-detail.png)

The captures verify numbered vacant sleeves, row-major distribution across both
leaves, page-safe geometry, the explicit category divider, its attached drawer,
and a free-standing detail card with one visible name. Earlier shader inspection
and the exact aperture mask verify portrait clipping and SSR foil isolation.

## Verification

- `python -B tools/check_screens.py`: pass; 286 screens defined, 260 distinct
  names referenced, every reference defined.
- Scoped `git diff --check`: pass; line-ending notices only.
- MatsuPy/Ren'Py compile: pass; exit 0 and 0 unreachable items across 121
  production source files after probe cleanup.
- MatsuPy/Ren'Py lint: exit 0. It still reports the repository's existing
  missing legacy Monika room, Natsuki MPT component, and base background/UI
  assets; no new card shell, card back, collection screen, or card renderer
  warning was emitted.
- Accelerated render probe: pass on GL2 at 1280x720; all three screenshots were
  written and the probe exited 0.

Current live categories contain two to five cards, so multi-spread navigation
is structurally exercised by the generalized slice/page math but does not yet
have a production category large enough to display a second spread.
