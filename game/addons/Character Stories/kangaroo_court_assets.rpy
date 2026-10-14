# Kangaroo Court - courtroom art refresh, 2026-10-12.
# Fixed room plates and independent RGBA character sprites. Portraits are
# registered on a 1280x720 canvas: show at (0, 0), without tcommon/cast transforms.
# Background sources retain native sizes and fit the logical 1280x720 stage.
# No story entry label, gameplay, or persistent state is added.

image bg kc car highway day = Transform("assets/backgrounds/kangaroo_court/car_highway_day.png", xysize=(1280, 720))
image bg kc lobby day = Transform("assets/backgrounds/kangaroo_court/kc_lobby_day.png", xysize=(1280, 720))
image bg kc lobby panic = Transform("assets/backgrounds/kangaroo_court/kc_lobby_panic.png", xysize=(1280, 720))
image bg kc courtroom overview = Transform("assets/backgrounds/kangaroo_court/kc_courtroom_overview.png", xysize=(1280, 720))
image bg kc prosecution bench = Transform("assets/backgrounds/kangaroo_court/kc_prosecution_bench.png", xysize=(1280, 720))
image bg kc defense bench = Transform("assets/backgrounds/kangaroo_court/kc_defense_bench.png", xysize=(1280, 720))
image bg kc witness stand = Transform("assets/backgrounds/kangaroo_court/kc_witness_stand.png", xysize=(1280, 720))
image bg kc judge bench = Transform("assets/backgrounds/kangaroo_court/kc_judge_bench.png", xysize=(1280, 720))

image kc himeko neutral = "assets/characters/kangaroo_court/himeko_neutral.png"
image kc himeko objection = "assets/characters/kangaroo_court/himeko_objection.png"
image kc himeko concerned = "assets/characters/kangaroo_court/himeko_concerned.png"
image kc himeko shaken = "assets/characters/kangaroo_court/himeko_shaken.png"
image kc stan dard neutral = "assets/characters/kangaroo_court/stan_dard_neutral.png"
image kc stan dard objection = "assets/characters/kangaroo_court/stan_dard_objection.png"
image kc stan dard concerned = "assets/characters/kangaroo_court/stan_dard_concerned.png"
image kc naoto mori neutral = "assets/characters/kangaroo_court/naoto_mori_neutral.png"
image kc judge neutral = "assets/characters/kangaroo_court/judge_neutral.png"
image kc judge stern = "assets/characters/kangaroo_court/judge_stern.png"
image kc judge surprised = "assets/characters/kangaroo_court/judge_surprised.png"

# Foregrounds sample the SAME room displayable, so no second painted desk can
# drift. Current sprites already stop at the rear desk edge; these masks support
# later leaning/ducking animation. Draw foreground hands/binder above this layer.
# Static poses already include their hands/props: show bg + kc only. These desk
# layers must not be drawn above a whole static portrait (the judge's fingers
# can extend over the front lip). See the dated art handoff for animation use.
image kc_desk prosecution = AlphaMask("bg kc prosecution bench", "assets/gui/kangaroo_court/prosecution_desk_mask.png")
image kc_desk defense = AlphaMask("bg kc defense bench", "assets/gui/kangaroo_court/defense_desk_mask.png")
image kc_desk witness = AlphaMask("bg kc witness stand", "assets/gui/kangaroo_court/witness_desk_mask.png")
image kc_desk judge = AlphaMask("bg kc judge bench", "assets/gui/kangaroo_court/judge_desk_mask.png")
