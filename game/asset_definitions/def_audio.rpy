# Shared music/SFX aliases and mixer channels. Addon-owned tracks can live
# beside their addon (including Asahina Rhythm/songs). Aliases initialize at -50
# before GUI defaults, credits, and other consumers evaluate them.
# Choose cues by scene role; literal filenames and playback live below.

define -50 audio.mainmenu = "assets/audio/bgm/mainmenu.ogg"               # main menu
define -50 audio.canyoufeel = "assets/audio/bgm/canyoufeel.ogg"           
define -50 audio.archive = "assets/audio/bgm/archive.ogg"       # archive

define -50 audio.day_c = "assets/audio/bgm/day_c.ogg"       # day, bustling/public -- "Slow life continues", junichirou
define -50 audio.day_a = "assets/audio/bgm/day_a.ogg"       # day, chill beat, low-energy
define -50 audio.house_day_a = "assets/audio/bgm/house_day_a.ogg"          # day, calm/at home -- "Sometimes", KHAIM
define -50 audio.day_b = "assets/audio/bgm/day_b.ogg"         # daily life outside of school or home. chill -- "Killing Time", Kevin MacLeod
define -50 audio.club_b = "assets/audio/bgm/club_b.ogg"         # literature club music B -- "you know what", Edamame88
define -50 audio.scorchingeurobeat = "assets/audio/bgm/scorchingeurobeat.ogg" # "Scorching Eurobeat", Maniira
define -50 audio.meatballparade = "assets/audio/bgm/meatballparade.ogg"   # used during particularly comedic segments (slapstick-level) -- "Meatball Parade", Kevin MacLeod
define -50 audio.tendermoment = "assets/audio/bgm/tendermoment.ogg"       # for emotional, feel-good, and/or wistful moments
define -50 audio.school_day_a = "assets/audio/bgm/school_day_a.ogg"   # "Chasing the Summer", shinsanworks
define -50 audio.ch4_day = "assets/audio/bgm/ch4_day.ogg"                # day theme chapter 4 onwards. lofi, calm intensity
define -50 audio.ch4_serious = "assets/audio/bgm/ch4_serious.ogg"             # serious music for chapter 4 onwards
define -50 audio.ch5_day = "assets/audio/bgm/ch5_day.ogg"
define -50 audio.night_a = "assets/audio/bgm/night_a.ogg"  # night, serious -- "The 4 PM Walk Philosophy", Nekoto
define -50 audio.night_b = "assets/audio/bgm/night_b.ogg" # night, calm -- "As Time Carries Us Away", Yosuke Matsuura
define -50 audio.hearttoheart = "assets/audio/bgm/hearttoheart.ogg"       # tender, emotional
define -50 audio.ch4_night = "assets/audio/bgm/ch4_night.ogg"         # primary night theme chapter 4

define -50 audio.twelveam = "assets/audio/bgm/12am.ogg"                   # alone with your thoughts
define -50 audio.hopeless = "assets/audio/bgm/13am.ogg"                   # darker, more hopeless
define -50 audio.holdmusic = "assets/audio/bgm/holdmusic.ogg"             # dream sequences
define -50 audio.safety = "assets/audio/bgm/safety.ogg"                   # "you screwed up"
define -50 audio.quiz = "assets/audio/bgm/quiz.ogg"                       # quizzes
define -50 audio.exam = "assets/audio/bgm/exam.ogg"                       # exams
define -50 audio.ancestry = "assets/audio/bgm/ancestry.ogg"               # creepy, unnerving (Minecraft OST)
define -50 audio.scamall = "assets/audio/bgm/scamall.ogg"                 # serious, mysterious, ethereal (ZZZ)
define -50 audio.noreturn = "assets/audio/bgm/noreturn.ogg"               # the music playing during the culmination of the hidden route that manipulates tsubaki.

define -50 audio.theme_matsuda_a = "assets/audio/bgm/theme_matsuda_a.ogg" # Matsuda's theme -- "A Quiet Place Among Strangers", Yosuke Matsuura

# -----------------------------------------------------------------------------
# Music -- side stories and character stories only
# -----------------------------------------------------------------------------

define -50 audio.raiseupyourbat = "addons/Asahina Rhythm/songs/raiseupyourbat.ogg"             # Asarhythm test song and developer chart preview
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
define -50 audio.blackwolf = "assets/audio/bgm/blackwolf.ogg"             # Archivist Invasions encounters
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

# Shared sound effects.
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

# Reused DDLC cues stored as ordinary files in the shared asset tree.
define -50 audio.glitch1 = "assets/audio/sfx/glitch1.ogg"                            # the tearing/glitch one-shot in effects.rpy
define -50 audio.fall2 = "assets/audio/sfx/fall2.ogg"


# sfxtrack1 carries location ambience; sfxtrack2 carries a sustained prop.
# sound handles one-shots; track1-4 provide independent looping music layers.
init python:
    renpy.music.register_channel("sfxtrack1", "sfx", False)
    renpy.music.register_channel("sfxtrack2", "sfx", False)
    renpy.music.register_channel("voice", "sfx", False)
    renpy.music.register_channel("track1", "music", True)
    renpy.music.register_channel("track2", "music", True)
    renpy.music.register_channel("track3", "music", True)
    renpy.music.register_channel("track4", "music", True)
