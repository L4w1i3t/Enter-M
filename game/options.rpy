##### ENGINE SETTINGS FOR YOUR MOD #####

# The formal name of the mod. Change the value of this to your mod's name
define config.name = "ENTER-M"

# The version of the mod
define config.version = "0.1.0"

# The description of the mod. Typically not used, but you can set it to whatever you want
define gui.about = _("")

# What your mod's filename will be called when it is built
define build.name = "ENTER-M"

# Toggles for different audio features.
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.main_menu_music = audio.canyoufeel   # Set this to whatever you want the main menu music to be

# The transitions BETWEEN MENUS (enter/exit/intra/game_main/end_game) live in
# menu_transitions.rpy, next to the choreographies they are built from. The
# transitions between STORY SCENES live in fx.rpy.

# Window settings
define config.window = "auto"
define config.window_show_transition = Dissolve(.18)
define config.window_hide_transition = Dissolve(.14)

# KEEPING "auto" ACTUALLY AUTOMATIC.
#
# `window hide` and `window show` are not the scoped, one-shot statements they
# look like. Both of them ALSO set `_window_auto = False` (see the statement
# handlers in renpy/common/000window.rpy), which switches the policy above off
# for the REST OF THE RUN -- not just for the next statement. So one game mode
# hiding the box by hand on its way in left the whole session with automatic
# hiding disabled: the empty textbox then sat through every later `scene`
# change instead of fading out before it, and a mode with its own dialogue card
# drew that card on top of a stray default DDLC box whose wider, lower edges
# peeked out around it. `game/story/season1/s1disc.rpy` and `arcade_launch_prep`
# both hand off into long sections that way.
#
# Re-arming on the following statement keeps `window hide` doing its immediate
# job -- the box goes away NOW -- while making it impossible for one to disarm
# the policy permanently. The callback is appended after 000window.rpy's own
# (registered at init -1200), so for any given statement it runs AFTER the auto
# show/hide decision has been made, and only takes effect from the next one.
# That one-statement gap is deliberate: it is what lets an explicit `window
# hide` still suppress the auto-hide of the `scene` or `call screen` it was
# written to precede.
init python:

    def _enter_m_rearm_window_auto(statement):
        if config.window == "auto" and not store._window_auto:
            store._window_auto = True

    config.statement_callbacks.append(_enter_m_rearm_window_auto)

# Default text speed and auto-forward mode timing
default preferences.text_cps = 50          # Characters per second (bigger number = faster text)
default preferences.afm_time = 15          # Auto-forward mode wait time

# Default volume settings
default preferences.music_volume = 1.0
default preferences.sfx_volume = 1.0

# Save directory - change to match your mod's name. This is located in AppData/Roaming/Matsu'Py/ on Windows
# and in ~/.renpy/ on Linux.
define config.save_directory = "ENTERM"

# Window icon that appears in your taskbar
define config.window_icon = "mod_assets/gui/window_icon.png"

# Gameplay settings
define config.allow_skipping = True        # Allows player to skip unseen dialogue
define config.has_autosave = False         # Disables autosaving
define config.autosave_on_quit = False
define config.autosave_slots = 0

# Display Layers [defined order of foreground and background elements; do not edit unless you are familiar with ATL]
define config.layers = [ 'master', 'cinematic', 'transient', 'screens', 'overlay', 'front' ]

# Performance settings
define config.image_cache_size = 64        # Number of images kept in active memory (higher = more memory usage)
define config.predict_statements = 50      # How many statements to look ahead
define config.rollback_enabled = config.developer  # Only enable rollback in dev mode

# Menu settings
define config.menu_clear_layers = ["front"]
define config.gl_test_image = "white"

init python:
    # Removes persistent data from other Matsu'Py games
    if len(renpy.loadsave.location.locations) > 1: del(renpy.loadsave.location.locations[1])

    # Disables gamepad support
    renpy.game.preferences.pad_enabled = False

    # Function to replace plain dashes with proper em dashes
    def replace_text(s):
        s = s.replace('--', u'\u2014')
        s = s.replace(' - ', u'\u2014')
        return s
    config.replace_text = replace_text

    # Function to handle game menu access
    def game_menu_check():
        if quick_menu: renpy.call_in_new_context('_game_menu')

    config.game_menu_action = game_menu_check

init python:
    # Build settings - defines how files are packaged when building your mod
    # Usually you won't need to change this, but it's here for reference

    # Define the archives (packages) that will contain your mod's files
    # NOTE FROM MODCEN: WHEN INSTALLING MODS, BE SURE TO ADD ALL OF THESE COMMENTED OUT RPA ARCHIVES TO THE GAME FOLDER
    # EXCEPT FOR scripts.rpa.
    # OTHERWISE THE MOD WILL NOT WORK. LIKE, AT ALL.
    # build.archive("scripts", "all")
    # build.archive("images", "all")
    # build.archive("audio", "all")
    # build.archive("fonts", "all")
    build.archive("mod", "all") # Custom archive to differentiate between mod files and vanilla files

    # Build classification. build.classify is FIRST-MATCH-WINS, so all excludes
    # are grouped ABOVE the includes -- otherwise catch-all dir includes (e.g.
    # game/story/**) would package .rpy/.bak/.md junk before the excludes run.
    # Affects the built distribution only; the SDK still loads every file.

    # --- Excludes ---
    build.classify("**.rpy", None)              # ship compiled .rpyc, never source
    build.classify("/docs/**", None)            # developer docs, including .txt guides
    build.classify("game/**.md", None)          # READMEs, cheatsheets, critiques
    build.classify("/**.md", None)
    build.classify("/.claude/**", None)
    build.classify("/.agents/**", None)
    build.classify("/vanilla/**", None)         # DDLC reference dump; not loaded at runtime
    build.classify("/tools/**", None)           # dev/build scripts
    build.classify("**sync-conflict**", None)   # Syncthing conflict copies
    # Dev tools (gated by config.developer, never run in release). Do NOT exclude
    # dev.rpy -- it also defines runtime state (player name, singleton, defaults).
    build.classify("/game/addons/Developer Date Jump/**", None)
    build.classify("/game/story/dev_scene_manager.rpyc", None)  # rough unplaced scratch scenes
    build.classify("/game/story/out_of_context/**", None)       # dated dev-only preview scenes
    # Backups / editor / OS junk (can appear in any subdir).
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**.psd", None)
    build.classify("**.sublime-project", None)
    build.classify("**.sublime-workspace", None)
    build.classify("**/.**", None)
    build.classify("**/#**", None)
    build.classify("**/thumbs.db", None)
    build.classify("**/.vscode/**", None)
    build.classify("**/.renpy-temp/**", None)
    build.classify("**/__pycache__/**", None)
    build.classify("**/.git/**", None)
    build.classify("**/.github/**", None)
    # Logs / engine leftovers / root non-content.
    build.classify("/traceback.txt", None)
    build.classify("/errors.txt", None)
    build.classify("/log.txt", None)
    build.classify("/**.bat", None)
    build.classify("script-regex.txt", None)
    build.classify("/music/*.*", None)
    build.classify("/game/10", None)
    build.classify("/game/firstrun", None)
    build.classify("/game/cache/*.*", None)
    build.classify("/game/**.rpa", None)
    build.classify("/game/saves/**", None)
    # NOTE: root characters/ is NOT excluded -- it holds the only copies of the
    # .chr masters that definitions.rpy/splash.rpy regenerate from.

    # --- Includes (only reached by files that survived the excludes) ---
    build.classify("game/**.jpg", "mod")
    build.classify("game/**.png", "mod")
    build.classify("game/**.webp", "mod")
    build.classify("game/**.gif", "mod")
    build.classify("game/**.rpyc", "mod")
    build.classify("game/**.txt", "mod")
    build.classify("game/**.chr", "mod")
    build.classify("game/**.wav", "mod")
    build.classify("game/**.mp3", "mod")
    build.classify("game/**.ogg", "mod")
    build.classify("game/**.ttf", "mod")
    build.classify("game/**.otf", "mod")
    build.classify("game/story/**", "mod")
    build.classify("game/addons/**", "mod")
    build.classify("game/mod_assets/**", "mod")
    build.classify("game/lost_records/**", "mod")

    # Documentation files to include
    build.documentation('*.html')
    build.documentation('*.txt')

    # Disables including old Matsu'Py themes
    build.include_old_themes = False

    build.package("Mod Export (All Platforms)", "zip", "windows mac linux renpy all")
