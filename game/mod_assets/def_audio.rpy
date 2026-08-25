# =============================================================================
# def_audio.rpy  --  ENTER M music, SFX aliases, and extra audio channels
# =============================================================================
#
# WHAT THIS FILE IS
#   The `audio.<name>` aliases for everything in mod_assets/bgm and
#   mod_assets/sfx that the MAIN STORY plays, plus the extra mixer channels the
#   project registers on top of Matsu'Py's built-in music/sound/voice.
#
# WHERE AUDIO LIVES
#   mod_assets/bgm/         all music
#   mod_assets/sfx/         shared one-shots
#   mod_assets/sfx/msbf/    Matsuda boss-fight combat + UI cues
#   mod_assets/sfx/touhou/  ZUN-standard SE used by the Kotonoha/Tsubaki modes
#   mod_assets/sfx/phone/   phone message + ringtone cues
#   Nothing audio-related lives under game/addons any more; an addon that owns a
#   track declares its own `audio.<name>` alias next to the code that plays it
#   (see op.rpy, kototouhou.rpy, monika_date.rpy, tsubaki_soul.rpy,
#   phone_model_construct.rpy, calendar_system.rpy, cs_tsubaki_gothic.rpy).
#
# ADDING A TRACK
#   Drop the file in mod_assets/bgm, add one `define -50 audio.<name> = ...` line
#   in the right block below, and describe when it should play. The comment is
#   the point: it is how the next scene picks the right cue.
#
# NEVER WRITE A FILE PATH IN A STORY FILE OR AN ADDON
#   `play music "mod_assets/bgm/whatever.ogg"` is not allowed. Every cue in the
#   main story and the addons goes through an `audio.<name>` alias -- here if two
#   or more files use it, or next to the owning code if exactly one does. The
#   only paths left inline anywhere are the boss fight's own SFX registry
#   (msbf_sfx("hit.wav") + a base folder, which IS a definition system) and the
#   build.classify globs in options.rpy.
#
# WHY EVERY ALIAS IS `define -50`
#   Matsu'Py evaluates same-priority `define`s in FILE ORDER, and this file sorts
#   under mod_assets/, i.e. after gui.rpy and after most of addons/. At the
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

define -50 audio.canyoufeel = "mod_assets/bgm/canyoufeel.ogg"           # main menu
define -50 audio.roster_place = "mod_assets/bgm/roster_place.ogg"       # archive

define -50 audio.daily = "mod_assets/bgm/daily.ogg"                     # day, bustling/public
define -50 audio.dailyfantasy = "mod_assets/bgm/dailyfantasy.ogg"       # day, upbeat
define -50 audio.dailyleisure = "mod_assets/bgm/dailyleisure.ogg"       # day, calm/at home
define -50 audio.schooldays = "mod_assets/bgm/schooldays.ogg"           # school, cheerful
define -50 audio.emotions = "mod_assets/bgm/ch4_day.ogg"                # day theme chapter 4 onwards. lofi, calm intensity
define -50 audio.opus1 = "mod_assets/bgm/ch5_day.ogg"

define -50 audio.fantasypassion = "mod_assets/bgm/fantasypassion.ogg"   # night, serious
define -50 audio.fantasyserenity = "mod_assets/bgm/fantasyserenity.ogg" # night, calm/at school
define -50 audio.hearttoheart = "mod_assets/bgm/hearttoheart.ogg"       # tender, emotional
define -50 audio.smoothsailing = "mod_assets/bgm/ch4_night.ogg"         # primary night theme chapter 4 onwards

define -50 audio.twelveam = "mod_assets/bgm/12am.ogg"                   # alone with your thoughts
define -50 audio.hopeless = "mod_assets/bgm/13am.ogg"                   # darker, more hopeless
define -50 audio.holdmusic = "mod_assets/bgm/holdmusic.ogg"             # dream sequences
define -50 audio.safety = "mod_assets/bgm/safety.ogg"                   # "you screwed up"
define -50 audio.quiz = "mod_assets/bgm/quiz.ogg"                       # quizzes and exams
define -50 audio.enterm = "mod_assets/bgm/enterm.ogg"                   # Matsuda's theme
define -50 audio.samsara = "mod_assets/bgm/ch4_serious.ogg"             # serious music for chapter 4 onwards
define -50 audio.ancestry = "mod_assets/bgm/ancestry.ogg"               # creepy, unnerving (Minecraft OST)
define -50 audio.scamall = "mod_assets/bgm/scamall.ogg"                 # serious, mysterious, ethereal (ZZZ)
define -50 audio.noreturn = "mod_assets/bgm/noreturn.ogg"               # the music playing during the culmination of the hidden route that manipulates tsubaki.


# -----------------------------------------------------------------------------
# Music -- side stories and character stories only
# -----------------------------------------------------------------------------

define -50 audio.hotr = "mod_assets/bgm/hotr.ogg"
define -50 audio.flight = "mod_assets/bgm/flight.ogg"
define -50 audio.devoted = "mod_assets/bgm/devoted.ogg"
define -50 audio.grandma = "mod_assets/bgm/grandma.mp3"
define -50 audio.stone = "mod_assets/bgm/stone.mp3"
define -50 audio.seafront = "mod_assets/bgm/seafront.mp3"
define -50 audio.family = "mod_assets/bgm/family.mp3"
define -50 audio.sis = "mod_assets/bgm/sis.mp3"
define -50 audio.sis_quiet = "mod_assets/bgm/sis_quiet.mp3"
define -50 audio.devola = "mod_assets/bgm/devola.mp3"
define -50 audio.popola = "mod_assets/bgm/popola.mp3"
define -50 audio.dream = "mod_assets/bgm/dream.mp3"
define -50 audio.beautiful = "mod_assets/bgm/beautiful.mp3"
define -50 audio.apology = "mod_assets/bgm/apology.mp3"
define -50 audio.dump = "mod_assets/bgm/dump.ogg"
define -50 audio.sands = "mod_assets/bgm/sands.mp3"
define -50 audio.automatons = "mod_assets/bgm/automatons.mp3"
define -50 audio.blubird = "mod_assets/bgm/blubird.mp3"
define -50 audio.hollow = "mod_assets/bgm/hollow.mp3"
define -50 audio.epicbattlephase1 = "mod_assets/bgm/epicbattlephase1.ogg"
define -50 audio.epicbattlephase2 = "mod_assets/bgm/epicbattlephase2.ogg"
define -50 audio.tails = "mod_assets/bgm/tails.ogg"                     # Tsubaki side story 2 main theme
define -50 audio.beautifulwrong = "mod_assets/bgm/beautifulwrong.ogg"   # Purgatorium, the wrong-sounding reprise
define -50 audio.blackwolf = "mod_assets/bgm/blackwolf.ogg"             # encounter music for a future implementation called Archivist Invasions
define -50 audio.blackwolf_corruptive = "mod_assets/bgm/blackwolf_corruptive.ogg" # certain music during Archivist Invasions


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
define -50 audio.mm_phase4 = "mod_assets/bgm/mm_phase4.ogg"
define -50 audio.kotoboss = "mod_assets/bgm/kotobossmusic.ogg"
define -50 audio.kotoendlessmode = "mod_assets/bgm/kotoendlessmode.ogg"
define -50 audio.tsubaphase1 = "mod_assets/bgm/tsubaphase1.ogg"
define -50 audio.tsubaphase2 = "mod_assets/bgm/tsubaphase2.ogg"
define -50 audio.embracedflame_inst = "mod_assets/bgm/embracedbytheflameinst.ogg"
define -50 audio.embracedflame_vocal = "mod_assets/bgm/embracedbytheflamevocal.ogg"
define -50 audio.arcade_theme = "mod_assets/bgm/arcade.ogg"             # Arcade hub
define -50 audio.tetris = "mod_assets/bgm/tetris.ogg"

# Vanilla DDLC tracks the Music Room lists. definitions.rpy already aliases these
# as t1 / td / mend / ghostmenu, but those carry "<loop ...>" prefixes for the
# same reason as above, so the Music Room needs bare ones.
define -50 audio.ddlc_main = "bgm/1.ogg"
define -50 audio.ddlc_sayonara = "bgm/d.ogg"
define -50 audio.ddlc_still_love_you = "bgm/monika-end.ogg"
define -50 audio.ddlc_ghostmenu = "bgm/ghostmenu.ogg"


# -----------------------------------------------------------------------------
# SFX
# -----------------------------------------------------------------------------

define -50 audio.moddooropen = "mod_assets/sfx/dooropen.ogg"
define -50 audio.moddoorclose = "mod_assets/sfx/doorclose.ogg"
define -50 audio.ac = "mod_assets/sfx/ac.ogg"                           # hum of an air conditioner
define -50 audio.hellbassboost = "mod_assets/sfx/hellbassboost.ogg"     # Purgatorium
define -50 audio.modwriting = "mod_assets/sfx/writing.ogg"              # pen/pencil on paper
define -50 audio.interjection = "mod_assets/sfx/interject.wav"
define -50 audio.tick = "mod_assets/sfx/tick.ogg"                       # wall clock, one-second tick

# Ambience and room tone
define -50 audio.wind = "mod_assets/sfx/sfx-wind.wav"                   # outdoor night wind bed
define -50 audio.heartbeat_ominous = "mod_assets/sfx/heartbeat_ominous.ogg"
define -50 audio.heartbeat = "mod_assets/sfx/sfx-heartbeat.wav"          # single beat one-shot
define -50 audio.hollowboom = "mod_assets/sfx/sfx-hollowboom.wav"        # deep hollow impact
define -50 audio.vinyl = "mod_assets/sfx/vinyl.wav"                     # record crackle / dead-air room tone

# Impacts and stingers (shared by the character stories and the game modes)
define -50 audio.sfx_swing = "mod_assets/sfx/sfx-swing.wav"
define -50 audio.sfx_shing = "mod_assets/sfx/sfx-shing.wav"
define -50 audio.sfx_stab = "mod_assets/sfx/sfx-stab.wav"
define -50 audio.sfx_stab2 = "mod_assets/sfx/sfx-stab2.wav"
define -50 audio.sfx_wham = "mod_assets/sfx/sfx-wham.wav"
define -50 audio.sfx_shock = "mod_assets/sfx/sfx-shock.wav"
define -50 audio.sfx_thunder = "mod_assets/sfx/sfx-thunder.wav"
define -50 audio.sfx_longwoosh = "mod_assets/sfx/sfx-longwoosh.wav"
define -50 audio.sfx_pshuu = "mod_assets/sfx/sfx-pshuu.wav"
define -50 audio.sfx_fwashing = "mod_assets/sfx/sfx-fwashing.wav"

# Interface and glitch
define -50 audio.uihover = "mod_assets/sfx/hover.ogg"                   # menu hover (gui.hover_sound)
define -50 audio.uiselect = "mod_assets/sfx/select.ogg"                 # menu activate (gui.activate_sound)
define -50 audio.notif = "mod_assets/sfx/notifsound.ogg"                # achievement toast
define -50 audio.censorbeep = "mod_assets/sfx/censorbeep.ogg"
define -50 audio.sfx_beep = "mod_assets/sfx/sfx-beep.wav"
define -50 audio.loudstatic = "mod_assets/sfx/loudstatic.wav"
define -50 audio.sfx_static = "mod_assets/sfx/sfx-staticy.wav"
define -50 audio.weirdjingle = "mod_assets/sfx/weirdjingle.ogg"         # plays for when the player progresses the weird route/dependency route choices

# Vanilla DDLC SFX the mod reuses (these live in the vanilla archives, not
# mod_assets, which is why they have no mod_assets/ prefix).
define -50 audio.glitch1 = "sfx/glitch1.ogg"                            # the tearing/glitch one-shot in effects.rpy
define -50 audio.fall2 = "sfx/fall2.ogg"


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
