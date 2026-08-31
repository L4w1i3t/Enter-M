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
#   assets/backgrounds/  finished backgrounds
#   assets/cg/           finished CGs
#   assets/dump/         art not yet sorted into backgrounds or CGs; entries
#                        pointing here are the ones still waiting on a home.
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
image bg dining_table = "assets/backgrounds/dining_table.png"
image bg dining_table_night = "assets/backgrounds/dining_table_night.png"
image bg living_room = "assets/backgrounds/living_room.png"
image bg living_room_night = "assets/backgrounds/living_room_night.png"
image bg living_room_tabletop_night = "assets/backgrounds/living_room_tabletop_night.png"
image bg bedroom_night = "assets/backgrounds/bedroom_night.png"
image bg kitchen_evening = "assets/backgrounds/kitchen_evening.png"
image bg kitchen_night = "assets/backgrounds/kitchen_night.png"
image bg house_evening = "assets/backgrounds/house_evening.png"
image bg house_night = "assets/backgrounds/house_night.png"
image bg home_entry_day = "assets/backgrounds/home_entry_day.png"
image bg home_entry_night = "assets/backgrounds/home_entry_night.png"
image bg sam_room_night = "assets/backgrounds/sam_room_night.png"
# These three entry plates belong to Kotonoha's retrospective material. The
# current household uses home_entry_* so the two locations cannot drift into
# one another again.
image bg doorday = "assets/backgrounds/doorday.png"
image bg doornight = "assets/backgrounds/doornight.png"
image bg doordark = "assets/backgrounds/doordark.png"


# -----------------------------------------------------------------------------
# School
# -----------------------------------------------------------------------------

# WARNING: corridor_bootleg is the deliberately flat, abstract corridor built for
# Sam's Purgatorium (cs_sam_01.rpy). It is NOT a main-story hallway -- it reads as
# a bootleg-game space on purpose. `bg hallway` is kept only because older files
# reference it; do not point new main-story scenes at either name.
# For the main story use `bg corridor` (vanilla) or `bg corridor_long` below.
image bg corridor_bootleg = "assets/backgrounds/corridor_bootleg.png"
image bg hallway = "assets/backgrounds/corridor_bootleg.png"   # deprecated alias -- see warning above

# Deep-perspective corridor with a dark tiled floor. Holds a heavy grade far
# better than the vanilla corridor, so it is the one to reach for once the story
# stops being bright (Chapter 4 onward). Pairs with atmos("winter_dim").
image bg corridor_long = "assets/dump/corridor2.png"

# Empty classroom, dark wood floor, no cast. For after-hours and out-of-term
# scenes where the vanilla club/classroom art is too cheerful and too occupied.
image bg classroom_empty = "assets/dump/class2.png"

# The genkan locker bank with its noticeboard. Where students actually linger on
# the way out of the building.
image bg shoe_lockers = "assets/dump/lockers.png"

image bg rooftop = "assets/backgrounds/rooftop.png"
image bg rooftop_door = "assets/backgrounds/rooftop_door.png"
image bg track_day = "assets/backgrounds/track_day.png"
image bg track_evening = "assets/backgrounds/track_evening.png"
image bg schoolgym = "assets/backgrounds/schoolgym.png"
image bg cafeteria = "assets/backgrounds/cafeteria.png"
image bg cafeteria_winter = "assets/backgrounds/cafeteria_winter.png"
image bg cafeteria_winter_dim = "assets/backgrounds/cafeteria_winter_dim.png"


# -----------------------------------------------------------------------------
# Town and outdoors
# -----------------------------------------------------------------------------

image bg city_morning = "assets/backgrounds/city_morning.png"
image bg city_day = "assets/backgrounds/city_day.png"
image bg city_night = "assets/backgrounds/city_night.png"
image bg city_evening = "assets/backgrounds/city_evening.png"
image bg town_day = "assets/backgrounds/town_day.png"
image bg residential_night = "assets/backgrounds/residential_night.png"
image bg cafe = "assets/backgrounds/cafe_stationery.png"
image bg bookstore = "assets/dump/bookstore.png"
image bg arcade = "assets/dump/arcade.png"
image bg store_techsection = "assets/backgrounds/store_techsection.png"
image bg store_checkout = "assets/backgrounds/store_checkout.png"
image bg library = "assets/backgrounds/library.png"
image bg theater_day = "assets/backgrounds/theater_day.png"
image bg theater_lobby = "assets/backgrounds/theater_lobby.png"
image bg theater_inside = "assets/backgrounds/theater_inside.png"
image bg bus_interior = "assets/backgrounds/bus_interior.png"
image bg park1 = "assets/backgrounds/park1.png"
image bg park_winter = "assets/backgrounds/park_winter.png"
image bg park_washed = "assets/backgrounds/park_washed.png"
image bg river = "assets/backgrounds/river.png"
image bg fields = "assets/backgrounds/fields.png"
image bg grassy = "assets/backgrounds/grassy.png"


# -----------------------------------------------------------------------------
# Side stories and unreal spaces
# -----------------------------------------------------------------------------

image bg ether = "assets/backgrounds/ether.png"                       # the in-between (ID card, transitions)
image bg hollow = "assets/backgrounds/hollow.png"
image bg fortress = "assets/backgrounds/fortress.png"
image bg battlefield01 = "assets/backgrounds/battlefield01.png"       # Dead Fantasy
image bg battle_setpiece = "assets/backgrounds/battle_setpiece.png"
image bg castle01_strategyroom = "assets/backgrounds/castle01_strategyroom.png"
image bg castle01_strategyroom_night = "assets/backgrounds/castle01_strategyroom_night.png"
image bg greywake_rival_keep = "assets/backgrounds/greywake_rival_keep.png"
image bg greywake_field_dawn = "assets/backgrounds/greywake_field_dawn.png"
image bg greywake_ravine = "assets/backgrounds/greywake_ravine.png"
image bg greywake_west_ridge = "assets/backgrounds/greywake_west_ridge.png"
image bg greywake_field_aftermath = "assets/backgrounds/greywake_field_aftermath.png"
image bg classroom_purg = "assets/backgrounds/classroom_purg.png"     # Purgatorium
image bg courtyard_purg = "assets/backgrounds/courtyard_purg.png"
image bg roof_purg = "assets/backgrounds/roof_purg.png"
image bg monika_room = "assets/cg/monika/monika_room.png"        # carried over from vanilla


# -----------------------------------------------------------------------------
# CGs
# -----------------------------------------------------------------------------

image cg hell = "assets/cg/hell.png"
image cg hell2 = "assets/cg/hell2.png"
image cg ransom = "assets/cg/ransom.png"
image cg dead_fantasy_greywake_draw = "assets/cg/dead_fantasy_greywake_draw.png"
