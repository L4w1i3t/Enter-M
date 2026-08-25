# =============================================================================
# cs_mom_01.rpy  --  PLACEHOLDER for Mom's character story "Continuance"
# =============================================================================
#
# STATUS: NOT YET WRITTEN. This file is intentionally empty of script.
#
# WIRING (where this story is referenced from):
#   game/addons/Character Stories/char_stories.rpy registers it as:
#     CharacterStoryEntry("Continuance", "A case file with no verdict.",
#                         "cs_mom_01", "cs_mom_01_unlocked")
#   so the hub expects a `label cs_mom_01:` here plus the unlock flag
#   `persistent.cs_mom_01_unlocked` (defaulted in char_stories.rpy).
#
# NOTE: no `label cs_mom_01:` is defined yet, so this entry must stay locked --
#   launching it while unlocked would jump to a missing label. When writing it,
#   mirror the structure of the finished cs_*.rpy stories and end with:
#     $ persistent.cs_mom_01_unlocked = True
#     return
# =============================================================================
