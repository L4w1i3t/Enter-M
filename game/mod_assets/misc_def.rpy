##########################################################################################################
# CHARACTER DEFINITIONS
##########################################################################################################

# Matsuda Definitions
image matsuda neut = Transform("mod_assets/char_sprites/matsuda/neutral.png", fit="contain", xysize=(640, 960))
define ma = DynamicCharacter('ma_name', image='matsuda', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
default ma_name = "Matsuda"

# Tsubaki Definitions
image tsubaki neut = Transform("mod_assets/char_sprites/tsubaki/neutral.png", fit="contain", xysize=(640, 960))
image tsubaki post = Transform("mod_assets/char_sprites/tsubaki/post.png", fit="contain", xysize=(640, 960))

define ts = DynamicCharacter('ts_name', image='tsubaki', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
default ts_name = "Tsubaki"

# Asahina Definitions
image asahina neut = Transform("mod_assets/char_sprites/asahina/neutral.png", fit="contain", xysize=(640, 960))

define ah = DynamicCharacter('as_name', image='asahina', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
default as_name = "Asahina"

# Sam Definitions
image sam neut = Transform("mod_assets/char_sprites/masayami/neutral.png", fit="contain", xysize=(640, 960))

define sa = DynamicCharacter('sa_name', image='sam', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
default sa_name = "Sam"

# Kotonoha Definitions
image kotonoha neut = Transform("mod_assets/char_sprites/kotonoha/neutral.png", fit="contain", xysize=(640, 960))

define ko = DynamicCharacter('ko_name', image='kotonoha', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
default ko_name = "Kotonoha"

# Mom/Himeko Definitions
image mom neut = Transform("mod_assets/char_sprites/himeko/neutral.png", fit="contain", xysize=(640, 960))

define mom = DynamicCharacter('mom_name', image='mom', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
default mom_name = "Mom"

# Other Character Definitions
image mc neut = Transform("mod_assets/char_sprites/mc/neutral.png", fit="contain", xysize=(640, 960))
image math_teacher neut = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image civics_teacher neut = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image science_teacher neut = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image japanese_teacher neut = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image english_teacher neut = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image track_coach neut = Transform("mod_assets/char_sprites/npc/track_coach.png", fit="contain", xysize=(640, 960))
image hikari neut = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image homura neut = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image gary = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image gregor = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image leif = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))

define math_teacher = Character("Teacher", image="math_teacher", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define civics_teacher = Character("Teacher", image="civics_teacher", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define science_teacher = Character("Teacher", image="science_teacher", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define japanese_teacher = Character("Teacher", image="japanese_teacher", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define english_teacher = Character("Teacher", image="english_teacher", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define track_coach = Character("Coach", image="track_coach", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define hikari = Character("Hikari", image="hikari", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define homura = Character("Homura", image="homura", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define npc1 = Character("NPC 1", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define npc2 = Character("NPC 2", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")

image purg_girl = Transform("mod_assets/extra_sprites/purg_girl.png", fit="contain", xysize=(640, 960))
image purg_girl_day7 = Transform("mod_assets/extra_sprites/purg_girl_day7.png", fit="contain", xysize=(640, 960))
image purg_girl_yukata = Transform("mod_assets/extra_sprites/purg_girl_yukata.png", fit="contain", xysize=(640, 960))

##########################################################################################################
# MUSIC DEFINITIONS
##########################################################################################################

define audio.roster_place = "mod_assets/bgm/roster_place.ogg"
define audio.hopeless = "mod_assets/bgm/13am.ogg"
define audio.twelveam = "mod_assets/bgm/12am.ogg"
define audio.map003 = "mod_assets/bgm/map003.ogg"
define audio.hotr = "mod_assets/bgm/hotr.ogg"
define audio.flight = "mod_assets/bgm/flight.ogg"
define audio.devoted = "mod_assets/bgm/devoted.ogg"
define audio.grandma = "mod_assets/bgm/grandma.mp3"
define audio.stone = "mod_assets/bgm/stone.mp3"
define audio.seafront = "mod_assets/bgm/seafront.mp3"
define audio.family = "mod_assets/bgm/family.mp3"
define audio.sis = "mod_assets/bgm/sis.mp3"
define audio.sis_quiet = "mod_assets/bgm/sis_quiet.mp3"
define audio.devola = "mod_assets/bgm/devola.mp3"
define audio.dream = "mod_assets/bgm/dream.mp3"
define audio.beautiful = "mod_assets/bgm/beautiful.mp3"
define audio.apology = "mod_assets/bgm/apology.mp3"
define audio.dump = "mod_assets/bgm/dump.ogg"
define audio.sands = "mod_assets/bgm/sands.mp3"
define audio.automatons = "mod_assets/bgm/automatons.mp3"
define audio.popola = "mod_assets/bgm/popola.mp3"
define audio.blubird = "mod_assets/bgm/blubird.mp3"
define audio.hollow = "mod_assets/bgm/hollow.mp3"
define audio.dailyfantasy = "mod_assets/bgm/dailyfantasy.ogg"
define audio.holdmusic = "mod_assets/bgm/holdmusic.ogg"
define audio.fantasypassion = "mod_assets/bgm/fantasypassion.ogg"
define audio.fantasyserenity = "mod_assets/bgm/fantasyserenity.ogg"
define audio.dailyleisure = "mod_assets/bgm/dailyleisure.ogg"
define audio.daily = "mod_assets/bgm/daily.ogg"
define audio.epicbattlephase1 = "mod_assets/bgm/epicbattlephase1.ogg"
define audio.epicbattlephase2 = "mod_assets/bgm/epicbattlephase2.ogg"

##########################################################################################################
# SFX DEFINITIONS
##########################################################################################################

define audio.moddooropen = "mod_assets/sfx/dooropen.ogg"
define audio.moddoorclose = "mod_assets/sfx/doorclose.ogg"
define audio.ac = "mod_assets/sfx/ac.ogg"
define audio.hellbassboost = "mod_assets/sfx/hellbassboost.ogg"

##########################################################################################################
# BG DEFINITIONS
##########################################################################################################

image bg living_room = "mod_assets/bg/living_room.png"
image bg bus_interior = "mod_assets/bg/bus_interior.png"
image bg cafe = "mod_assets/bg/cafe.png"
image bg battlefield01 = "mod_assets/bg/battlefield01.png"
image bg castle01_strategyroom = "mod_assets/bg/castle01_strategyroom.png"
image bg park_winter = "mod_assets/bg/park_winter.png"
image bg doordark = "mod_assets/bg/doordark.png"
image bg doorday = "mod_assets/bg/doorday.png"
image bg doornight = "mod_assets/bg/doornight.png"
image bg grassy = "mod_assets/bg/grassy.png"
image bg hollow = "mod_assets/bg/hollow.png"
image bg corridor_bootleg = "mod_assets/bg/corridor_bootleg.png"
image bg town_day = "mod_assets/bg/town_day.png"
image bg river = "mod_assets/bg/river.png"
image bg fields = "mod_assets/bg/fields.png"
image bg park_washed = "mod_assets/bg/park_washed.png"
image bg park1 = "mod_assets/bg/park1.png"
image bg classroom_purg = "mod_assets/bg/classroom_purg.png"
image bg courtyard_purg = "mod_assets/bg/courtyard_purg.png"
image bg sam_room_night = "mod_assets/bg/sam_room_night.png"
image bg roof_purg = "mod_assets/bg/roof_purg.png"
image bg fortress = "mod_assets/bg/fortress.png"
image bg ether = "mod_assets/bg/ether.png"
image bg store_techsection = "mod_assets/bg/store_techsection.png"
image bg residential_night = "mod_assets/bg/residential_night.png"
image bg hallway = "mod_assets/bg/corridor_bootleg.png"
image bg house_night = "mod_assets/bg/house_night.png"
image bg living_room_night = "mod_assets/bg/living_room_night.png"
image bg city_morning = "mod_assets/bg/city_morning.png"
image bg city_day = "mod_assets/bg/city_day.png"
image bg city_night = "mod_assets/bg/city_night.png"
image bg theater_day = "mod_assets/bg/theater_day.png"
image bg theater_evening = "mod_assets/bg/theater_evening.png"
image bg theater_inside = "mod_assets/bg/theater_inside.png"
image bg theater_lobby = "mod_assets/bg/theater_lobby.png"
image bg track_day = "mod_assets/bg/track_day.png"
image bg rooftop = "mod_assets/bg/rooftop.png"
image bg rooftop_door = "mod_assets/bg/rooftop_door.png"
image bg battle_setpiece = "mod_assets/bg/battle_setpiece.png"
image bg schoolgym = "mod_assets/bg/schoolgym.png"

# CG DEFINITIONS
image cg hell = "mod_assets/cg/hell.png"
image cg hell2 = "mod_assets/cg/hell2.png"
image cg ransom = "mod_assets/cg/ransom.png"
image cg everyface = "mod_assets/cg/everyface.png"
image cg lies = "mod_assets/cg/lies.png"
image cg campaign = "mod_assets/cg/campaign.png"
image cg voidhunter = "mod_assets/cg/voidhunter.png"

##########################################################################################################
# GUI DEFINITIONS
##########################################################################################################

##########################################################################################################
# FONTS DEFINITIONS
##########################################################################################################

##########################################################################################################
# LOGIC DEFINITIONS
##########################################################################################################

init python:
    renpy.music.register_channel("sfxtrack1", "sfx", False)
    renpy.music.register_channel("sfxtrack2", "sfx", False)
    renpy.music.register_channel("voice", "sfx", False)
    renpy.music.register_channel("track1", "music", True)
    renpy.music.register_channel("track2", "music", True)
    renpy.music.register_channel("track3", "music", True)
    renpy.music.register_channel("track4", "music", True)
