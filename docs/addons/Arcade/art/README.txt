ARCADE BOX ART
==============

Drop a SQUARE cover image in game/addons/Arcade/art/ to give an Arcade
cartridge its box art. No code change is needed; game/addons/Arcade/arcade.rpy
finds it by filename.

Filename = the catalog title, lowercased, with every non-alphanumeric character
turned into an underscore:

    Ontological Seer          ->  ontological_seer.png
    Ontological Seer: Id      ->  ontological_seer_id.png
    A Fine Date               ->  a_fine_date.png
    Embodiment of Violet Ink  ->  embodiment_of_violet_ink.png
    The Unwritten Act         ->  the_unwritten_act.png
    Coming Soon               ->  coming_soon.png

.png, .jpg, .jpeg and .webp all work (tried in that order).

NOTES
- Square (1:1) is the format. Anything else is centre-cropped to fill the card.
- 512px on a side is the preferred delivery size. The card renders at 320px
  featured / 126px on the shelf, so larger sources only increase decode cost.
- Put the game's TITLE in the artwork itself. The card draws nothing but the
  picture -- no title, no genre band -- so it reads like a real jewel case.
- The shipped library uses a deliberate 16-bit-era print language: one strong
  gameplay silhouette, a limited palette, exact typography, and light halftone
  / offset-print texture. Avoid glossy modern concept art, fake microtext,
  random circuitry, and over-detailed ornamental frames.
- A cartridge with no art in game/addons/Arcade/art/ falls back to its plain
  accent color, drawn as a lit blank case. Nothing breaks.
- An entry in the arcade_items table may also name an explicit path, which wins
  over game/addons/Arcade/art/. Shipped cartridges use explicit optimized paths;
  the filename convention remains the zero-code route for new additions.
