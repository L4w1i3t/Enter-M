# =============================================================================
# cs_player_01.rpy  --  PLACEHOLDER for the Player's character story
# =============================================================================
#
# STATUS: NOT YET WRITTEN. This file is intentionally empty of script.
#
# WIRING (where this story is referenced from):
#   game/addons/Character Stories/char_stories.rpy registers it as:
#     CharacterStoryEntry("Coming Soon", "This story hasn't been written yet.",
#                         "cs_player_01", "cs_player_01_unlocked")
#   so the hub expects a `label cs_player_01:` to exist here and an unlock flag
#   `persistent.cs_player_01_unlocked` (defaulted in char_stories.rpy).
#
# NOTE: because no `label cs_player_01:` is defined yet, this entry must stay
#   locked -- launching it while unlocked would jump to a missing label. When
#   writing the story, follow the pattern of the other cs_*.rpy files:
#     label cs_player_01:
#         hide screen archive
#         hide screen character_stories
#         ... story ...
#         $ persistent.cs_player_01_unlocked = True   # idempotent re-affirm
#         return
# =============================================================================
