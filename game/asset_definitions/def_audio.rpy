# =============================================================================
# def_audio.rpy  --  ENTER M music, SFX aliases, and extra audio channels
# =============================================================================
#
# WHAT THIS FILE IS
#   The `audio.<name>` aliases for everything in assets/audio/bgm and
#   assets/audio/sfx that the MAIN STORY plays, plus the extra mixer channels the
#   project registers on top of Matsu'Py's built-in music/sound/voice.
#
# WHERE AUDIO LIVES
#   assets/audio/bgm/         all music
#   assets/audio/sfx/         shared one-shots
#   assets/audio/sfx/msbf/    Matsuda boss-fight combat + UI cues
#   assets/audio/sfx/touhou/  ZUN-standard SE used by the Kotonoha/Tsubaki modes
#   assets/audio/sfx/phone/   phone message + ringtone cues
#   Nothing audio-related lives under game/addons any more; an addon that owns a
#   track declares its own `audio.<name>` alias next to the code that plays it
#   (see op.rpy, kototouhou.rpy, monika_date.rpy, tsubaki_soul.rpy,
#   phone_model_construct.rpy, calendar_system.rpy, cs_tsubaki_gothic.rpy).
#
# ADDING A TRACK
#   Drop the file in assets/audio/bgm, add one `define -50 audio.<name> = ...` line
#   in the right block below, and describe when it should play. The comment is
#   the point: it is how the next scene picks the right cue.
#
# NEVER WRITE A FILE PATH IN A STORY FILE OR AN ADDON
#   `play music "assets/audio/bgm/whatever.ogg"` is not allowed. Every cue in the
#   main story and the addons goes through an `audio.<name>` alias -- here if two
#   or more files use it, or next to the owning code if exactly one does. The
#   only paths left inline anywhere are the boss fight's own SFX registry
#   (msbf_sfx("hit.wav") + a base folder, which IS a definition system) and the
#   build.classify globs in options.rpy.
#
# WHY EVERY ALIAS IS `define -50`
#   Matsu'Py evaluates same-priority `define`s in FILE ORDER, and this file sorts
#   under asset_definitions/, i.e. after gui.rpy and after most of addons/. At the
#   default priority, `define gui.hover_sound = audio.uihover` in gui.rpy and
#   `CreditEntry(..., [audio.enter_m_op])` in an addon's init block both crash
#   with AttributeError, because the alias does not exist yet.
#   -50 puts every audio alias in the project -- here, in definitions.rpy, and in
#   the addons that own a track -- ahead of everything that consumes them. If you
#   add an alias anywhere, give it -50 too. Values must stay plain literals; an
#   alias that evaluates another store variable would defeat the early priority.
#
# RELATED FILES
#   def_characters.rpy -- cast sprites and Characters
#   def_images.rpy     -- backgrounds and CGs
#   Music Room/music_room.rpy -- the in-game player; add new tracks there too
# =============================================================================


# -----------------------------------------------------------------------------
# Music -- main story and menus
# -----------------------------------------------------------------------------

define -50 audio.mainmenu = "assets/audio/bgm/mainmenu.ogg"               # main menu
define -50 audio.canyoufeel = "assets/audio/bgm/canyoufeel.ogg"           
define -50 audio.roster_place = "assets/audio/bgm/roster_place.ogg"       # archive

define -50 audio.daily = "assets/audio/bgm/daily.ogg"                     # day, bustling/public
define -50 audio.dailyfantasy = "assets/audio/bgm/dailyfantasy.ogg"       # day, upbeat
define -50 audio.dailyleisure = "assets/audio/bgm/dailyleisure.ogg"       # day, calm/at home
define -50 audio.schooldays = "assets/audio/bgm/schooldays.ogg"           # school, cheerful
define -50 audio.emotions = "assets/audio/bgm/ch4_day.ogg"                # day theme chapter 4 onwards. lofi, calm intensity
define -50 audio.opus1 = "assets/audio/bgm/ch5_day.ogg"

define -50 audio.fantasypassion = "assets/audio/bgm/fantasypassion.ogg"   # night, serious
define -50 audio.fantasyserenity = "assets/audio/bgm/fantasyserenity.ogg" # night, calm/at school
define -50 audio.hearttoheart = "assets/audio/bgm/hearttoheart.ogg"       # tender, emotional
define -50 audio.smoothsailing = "assets/audio/bgm/ch4_night.ogg"         # primary night theme chapter 4 onwards

define -50 audio.twelveam = "assets/audio/bgm/12am.ogg"                   # alone with your thoughts
define -50 audio.hopeless = "assets/audio/bgm/13am.ogg"                   # darker, more hopeless
define -50 audio.holdmusic = "assets/audio/bgm/holdmusic.ogg"             # dream sequences
define -50 audio.safety = "assets/audio/bgm/safety.ogg"                   # "you screwed up"
define -50 audio.quiz = "assets/audio/bgm/quiz.ogg"                       # quizzes and exams
define -50 audio.enterm = "assets/audio/bgm/enterm.ogg"                   # Matsuda's theme
define -50 audio.samsara = "assets/audio/bgm/ch4_serious.ogg"             # serious music for chapter 4 onwards
define -50 audio.ancestry = "assets/audio/bgm/ancestry.ogg"               # creepy, unnerving (Minecraft OST)
define -50 audio.scamall = "assets/audio/bgm/scamall.ogg"                 # serious, mysterious, ethereal (ZZZ)
define -50 audio.noreturn = "assets/audio/bgm/noreturn.ogg"               # the music playing during the culmination of the hidden route that manipulates tsubaki.


# -----------------------------------------------------------------------------
# Music -- side stories and character stories only
# -----------------------------------------------------------------------------

define -50 audio.hotr = "assets/audio/bgm/hotr.ogg"
define -50 audio.flight = "assets/audio/bgm/flight.ogg"
define -50 audio.devoted = "assets/audio/bgm/devoted.ogg"
define -50 audio.grandma = "assets/audio/bgm/grandma.mp3"
define -50 audio.stone = "assets/audio/bgm/stone.mp3"
define -50 audio.seafront = "assets/audio/bgm/seafront.mp3"
define -50 audio.family = "assets/audio/bgm/family.mp3"
define -50 audio.sis = "assets/audio/bgm/sis.mp3"
define -50 audio.sis_quiet = "assets/audio/bgm/sis_quiet.mp3"
define -50 audio.devola = "assets/audio/bgm/devola.mp3"
define -50 audio.popola = "assets/audio/bgm/popola.mp3"
define -50 audio.dream = "assets/audio/bgm/dream.mp3"
define -50 audio.beautiful = "assets/audio/bgm/beautiful.mp3"
define -50 audio.apology = "assets/audio/bgm/apology.mp3"
define -50 audio.dump = "assets/audio/bgm/dump.ogg"
define -50 audio.sands = "assets/audio/bgm/sands.mp3"
define -50 audio.automatons = "assets/audio/bgm/automatons.mp3"
define -50 audio.blubird = "assets/audio/bgm/blubird.mp3"
define -50 audio.hollow = "assets/audio/bgm/hollow.mp3"
define -50 audio.epicbattlephase1 = "assets/audio/bgm/epicbattlephase1.ogg"
define -50 audio.epicbattlephase2 = "assets/audio/bgm/epicbattlephase2.ogg"
define -50 audio.tails = "assets/audio/bgm/tails.ogg"                     # Tsubaki side story 2 main theme
define -50 audio.beautifulwrong = "assets/audio/bgm/beautifulwrong.ogg"   # Purgatorium, the wrong-sounding reprise
define -50 audio.blackwolf = "assets/audio/bgm/blackwolf.ogg"             # encounter music for a future implementation called Archivist Invasions
define -50 audio.blackwolf_corruptive = "assets/audio/bgm/blackwolf_corruptive.ogg" # certain music during Archivist Invasions


# -----------------------------------------------------------------------------
# Music -- game modes, BARE PATHS
# -----------------------------------------------------------------------------
# Each of these already has an addon-local alias next to the code that plays it
# (audio.mm_music_p4, audio.tsb_inst, audio.kt_boss_theme, ...) -- but those all
# carry a "<loop 0>" playback prefix baked into the string.
#
# The Music Room builds its playback string by CONCATENATING its own prefix onto
# the track path (music_room.rpy: `prefix + current_track.file_path`), so handing
# it a pre-prefixed alias produces "<loop 0><loop 0>path" and breaks. These bare
# aliases exist so the Music Room has something to reference instead of hardcoded
# paths. Same files, no prefix. Do not add a prefix to these.
define -50 audio.mm_phase4 = "assets/audio/bgm/mm_phase4.ogg"
define -50 audio.kotoboss = "assets/audio/bgm/kotobossmusic.ogg"
define -50 audio.kotoendlessmode = "assets/audio/bgm/kotoendlessmode.ogg"
define -50 audio.tsubaphase1 = "assets/audio/bgm/tsubaphase1.ogg"
define -50 audio.tsubaphase2 = "assets/audio/bgm/tsubaphase2.ogg"
define -50 audio.embracedflame_inst = "assets/audio/bgm/embracedbytheflameinst.ogg"
define -50 audio.embracedflame_vocal = "assets/audio/bgm/embracedbytheflamevocal.ogg"
define -50 audio.arcade_theme = "assets/audio/bgm/arcade.ogg"             # Arcade hub
define -50 audio.tetris = "assets/audio/bgm/tetris.ogg"

# Vanilla DDLC tracks the Music Room lists. definitions.rpy already aliases these
# as t1 / td / mend / ghostmenu, but those carry "<loop ...>" prefixes for the
# same reason as above, so the Music Room needs bare ones.
define -50 audio.ddlc_main = "assets/audio/bgm/1.ogg"
define -50 audio.ddlc_sayonara = "assets/audio/bgm/d.ogg"
define -50 audio.ddlc_still_love_you = "assets/audio/bgm/monika-end.ogg"
define -50 audio.ddlc_ghostmenu = "assets/audio/bgm/ghostmenu.ogg"


# -----------------------------------------------------------------------------
# SFX
# -----------------------------------------------------------------------------

define -50 audio.moddooropen = "assets/audio/sfx/dooropen.ogg"
define -50 audio.moddoorclose = "assets/audio/sfx/doorclose.ogg"
define -50 audio.ac = "assets/audio/sfx/ac.ogg"                           # hum of an air conditioner
define -50 audio.hellbassboost = "assets/audio/sfx/hellbassboost.ogg"     # Purgatorium
define -50 audio.modwriting = "assets/audio/sfx/writing.ogg"              # pen/pencil on paper
define -50 audio.interjection = "assets/audio/sfx/interject.wav"
define -50 audio.tick = "assets/audio/sfx/tick.ogg"                       # wall clock, one-second tick

# Ambience and room tone
define -50 audio.wind = "assets/audio/sfx/sfx-wind.wav"                   # outdoor night wind bed
define -50 audio.heartbeat_ominous = "assets/audio/sfx/heartbeat_ominous.ogg"
define -50 audio.heartbeat = "assets/audio/sfx/sfx-heartbeat.wav"          # single beat one-shot
define -50 audio.hollowboom = "assets/audio/sfx/sfx-hollowboom.wav"        # deep hollow impact
define -50 audio.vinyl = "assets/audio/sfx/vinyl.wav"                     # record crackle / dead-air room tone

# Impacts and stingers (shared by the character stories and the game modes)
define -50 audio.sfx_swing = "assets/audio/sfx/sfx-swing.wav"
define -50 audio.sfx_shing = "assets/audio/sfx/sfx-shing.wav"
define -50 audio.sfx_stab = "assets/audio/sfx/sfx-stab.wav"
define -50 audio.sfx_stab2 = "assets/audio/sfx/sfx-stab2.wav"
define -50 audio.sfx_wham = "assets/audio/sfx/sfx-wham.wav"
define -50 audio.sfx_shock = "assets/audio/sfx/sfx-shock.wav"
define -50 audio.sfx_thunder = "assets/audio/sfx/sfx-thunder.wav"
define -50 audio.sfx_longwoosh = "assets/audio/sfx/sfx-longwoosh.wav"
define -50 audio.sfx_pshuu = "assets/audio/sfx/sfx-pshuu.wav"
define -50 audio.sfx_fwashing = "assets/audio/sfx/sfx-fwashing.wav"

# Interface and glitch
define -50 audio.uihover = "assets/audio/sfx/hover.ogg"                   # menu hover (gui.hover_sound)
define -50 audio.uiselect = "assets/audio/sfx/select.ogg"                 # menu activate (gui.activate_sound)
define -50 audio.notif = "assets/audio/sfx/notifsound.ogg"                # achievement toast
define -50 audio.censorbeep = "assets/audio/sfx/censorbeep.ogg"
define -50 audio.sfx_beep = "assets/audio/sfx/sfx-beep.wav"
define -50 audio.loudstatic = "assets/audio/sfx/loudstatic.wav"
define -50 audio.sfx_static = "assets/audio/sfx/sfx-staticy.wav"
define -50 audio.weirdjingle = "assets/audio/sfx/weirdjingle.ogg"         # plays for when the player progresses the weird route/dependency route choices

# Vanilla DDLC SFX the mod reuses (these live in the vanilla archives, not
# the shared asset tree, which is why they have no assets/ prefix).
define -50 audio.glitch1 = "assets/audio/sfx/glitch1.ogg"                            # the tearing/glitch one-shot in effects.rpy
define -50 audio.fall2 = "assets/audio/sfx/fall2.ogg"


# -----------------------------------------------------------------------------
# Extra mixer channels
#   sfxtrack1/2 and voice sit on the SFX slider; track1-4 on the music slider.
#   They exist so a scene can layer cues without stopping whatever is already
#   playing on the default `sound` / `music` channels.
#
# WHAT EACH SFX CHANNEL IS FOR  (house convention -- keep to it)
#   These two drifted badly across the out-of-context scenes: the same channel
#   was carrying wind in one section and a wall clock in the next, so beds swapped
#   at cuts for no reason in the story. The roles are now fixed.
#
#   sfxtrack1  THE LOCATION BED. Exactly one at a time, and it changes only when
#              the location changes -- outdoor wind, a heater/room hum, a gym.
#              Coming back to a room the scene has already been in means starting
#              the SAME bed again at the SAME volume. A room that sounds one way
#              at breakfast and another way at dusk, with nothing in the story to
#              explain it, is the audio version of a shader popping on and off.
#   sfxtrack2  THE PROP. One sustained object or transient in the scene -- the
#              wall clock, a heartbeat under a menu beat, a ringtone. Never a
#              second room tone; if a space needs two layers of ambience, that is
#              one bed and the mix is wrong.
#
#   `sound` stays for one-shots (doors, impacts). `music` stays non-diegetic,
#   EXCEPT where a scene deliberately plays a real-world source -- a phone on a
#   desk, a ringtone in a coat -- which goes on an sfx channel so it sits under
#   the SFX slider like the real object it is.
# -----------------------------------------------------------------------------

init python:
    renpy.music.register_channel("sfxtrack1", "sfx", False)
    renpy.music.register_channel("sfxtrack2", "sfx", False)
    renpy.music.register_channel("voice", "sfx", False)
    renpy.music.register_channel("track1", "music", True)
    renpy.music.register_channel("track2", "music", True)
    renpy.music.register_channel("track3", "music", True)
    renpy.music.register_channel("track4", "music", True)
