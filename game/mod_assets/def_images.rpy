# =============================================================================
# def_images.rpy  --  ENTER M backgrounds and CGs
# =============================================================================
#
# WHAT THIS FILE IS
#   Every `bg` and `cg` image the main story and side stories can `scene` or
#   `show`. Vanilla DDLC's own backgrounds stay in game/definitions.rpy.
#
# NAMING
#   `image bg <place>[_<time>]` -- time suffix only when more than one lighting
#   variant of the same place exists (city_morning / city_day / city_night).
#   Lighting grade on top of these comes from atmosphere.rpy's atmos() helper,
#   NOT from more image variants.
#
# WHERE THE FILES LIVE
#   mod_assets/bg/    finished backgrounds
#   mod_assets/cg/    finished CGs
#   mod_assets/dump/  art not yet sorted into bg/ or cg/; entries pointing here
#                     are the ones still waiting on a home.
#
# RELATED FILES
#   def_characters.rpy -- cast sprites and Characters
#   def_audio.rpy      -- music / SFX aliases and extra audio channels
#   CG View/cg_gallery.rpy -- the gallery; add unlockable CGs there too
# =============================================================================


# -----------------------------------------------------------------------------
# Home
# -----------------------------------------------------------------------------

# The house has two separate rooms and they are not interchangeable: vanilla
# `bg kitchen` is a galley with counters, stove and sink and NO table, so any
# beat where somebody sits down, eats, or reads a note off the table belongs
# here instead.
image bg dining_table = "mod_assets/bg/dining_table.png"
image bg dining_table_night = "mod_assets/bg/dining_table_night.png"
image bg living_room = "mod_assets/bg/living_room.png"
image bg living_room_night = "mod_assets/bg/living_room_night.png"
image bg house_night = "mod_assets/bg/house_night.png"
image bg sam_room_night = "mod_assets/bg/sam_room_night.png"
image bg doorday = "mod_assets/bg/doorday.png"
image bg doornight = "mod_assets/bg/doornight.png"
image bg doordark = "mod_assets/bg/doordark.png"


# -----------------------------------------------------------------------------
# School
# -----------------------------------------------------------------------------

# WARNING: corridor_bootleg is the deliberately flat, abstract corridor built for
# Sam's Purgatorium (cs_sam_01.rpy). It is NOT a main-story hallway -- it reads as
# a bootleg-game space on purpose. `bg hallway` is kept only because older files
# reference it; do not point new main-story scenes at either name.
# For the main story use `bg corridor` (vanilla) or `bg corridor_long` below.
image bg corridor_bootleg = "mod_assets/bg/corridor_bootleg.png"
image bg hallway = "mod_assets/bg/corridor_bootleg.png"   # deprecated alias -- see warning above

# Deep-perspective corridor with a dark tiled floor. Holds a heavy grade far
# better than the vanilla corridor, so it is the one to reach for once the story
# stops being bright (Chapter 4 onward). Pairs with atmos("winter_dim").
image bg corridor_long = "mod_assets/dump/corridor2.png"

# Empty classroom, dark wood floor, no cast. For after-hours and out-of-term
# scenes where the vanilla club/classroom art is too cheerful and too occupied.
image bg classroom_empty = "mod_assets/dump/class2.png"

# The genkan locker bank with its noticeboard. Where students actually linger on
# the way out of the building.
image bg shoe_lockers = "mod_assets/dump/lockers.png"

image bg rooftop = "mod_assets/bg/rooftop.png"
image bg rooftop_door = "mod_assets/bg/rooftop_door.png"
image bg track_day = "mod_assets/bg/track_day.png"
image bg schoolgym = "mod_assets/bg/schoolgym.png"
image bg cafeteria = "mod_assets/bg/cafeteria.png"


# -----------------------------------------------------------------------------
# Town and outdoors
# -----------------------------------------------------------------------------

image bg city_morning = "mod_assets/bg/city_morning.png"
image bg city_day = "mod_assets/bg/city_day.png"
image bg city_night = "mod_assets/bg/city_night.png"
image bg city_evening = "mod_assets/dump/city_evening.png"
image bg town_day = "mod_assets/bg/town_day.png"
image bg residential_night = "mod_assets/bg/residential_night.png"
image bg cafe = "mod_assets/bg/cafe.png"
image bg bookstore = "mod_assets/dump/bookstore.png"
image bg arcade = "mod_assets/dump/arcade.png"
image bg store_techsection = "mod_assets/bg/store_techsection.png"
image bg theater_day = "mod_assets/bg/theater_day.png"
image bg theater_lobby = "mod_assets/bg/theater_lobby.png"
image bg theater_inside = "mod_assets/bg/theater_inside.png"
image bg bus_interior = "mod_assets/bg/bus_interior.png"
image bg park1 = "mod_assets/bg/park1.png"
image bg park_winter = "mod_assets/bg/park_winter.png"
image bg park_washed = "mod_assets/bg/park_washed.png"
image bg river = "mod_assets/bg/river.png"
image bg fields = "mod_assets/bg/fields.png"
image bg grassy = "mod_assets/bg/grassy.png"


# -----------------------------------------------------------------------------
# Side stories and unreal spaces
# -----------------------------------------------------------------------------

image bg ether = "mod_assets/bg/ether.png"                       # the in-between (ID card, transitions)
image bg hollow = "mod_assets/bg/hollow.png"
image bg fortress = "mod_assets/bg/fortress.png"
image bg battlefield01 = "mod_assets/bg/battlefield01.png"       # Dead Fantasy
image bg battle_setpiece = "mod_assets/bg/battle_setpiece.png"
image bg castle01_strategyroom = "mod_assets/bg/castle01_strategyroom.png"
image bg classroom_purg = "mod_assets/bg/classroom_purg.png"     # Purgatorium
image bg courtyard_purg = "mod_assets/bg/courtyard_purg.png"
image bg roof_purg = "mod_assets/bg/roof_purg.png"
image bg monika_room = "images/cg/monika/monika_room.png"        # carried over from vanilla


# -----------------------------------------------------------------------------
# CGs
# -----------------------------------------------------------------------------

image cg hell = "mod_assets/cg/hell.png"
image cg hell2 = "mod_assets/cg/hell2.png"
image cg ransom = "mod_assets/cg/ransom.png"
