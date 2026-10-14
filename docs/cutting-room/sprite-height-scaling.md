# Retired sprite-height experiment

The August 2026 experiment rescaled finished sprites against Monika as a
pixels-per-inch reference. It was removed after changes to framing, clipping,
and dependent portrait layouts. Its measurements describe those historical
assets and must not be copied as current sprite dimensions.

The useful distinction remains: normalizing every image to one canvas size
does not establish one physical scale across differently drawn figures. Asset
authoring should preserve deliberate proportions and identity.

Current story framing is implemented separately in `game/story_cast_framing.rpy`
under the outer slot transforms. It changes shown story framing without changing
registered images used by screen portraits. Read that code and the installed
art rather than restoring the retired scaling experiment.

This path is retained because `game/asset_definitions/def_characters.rpy`
references it. The full old measurements are in the
[documentation snapshot](../history/README.md).
