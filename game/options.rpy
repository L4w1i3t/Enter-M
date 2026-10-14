# ENTER M engine and distribution settings.

# Runtime art now lives in category-specific directories and is explicitly
# declared. Disable Ren'Py's single-directory basename scan: pointing it at the
# whole assets tree would create ambiguous aliases for duplicate filenames and
# do unnecessary work at startup. Keep the compatibility search prefix for
# engine-generated ``gui/**`` lookups. This must run after common code creates
# these config variables (init -1900), but before ordinary init blocks begin.
init -999 python:
    config.images_directory = None
    config.search_prefixes = ["", "assets/"]

# Displayed project name and release version.
define config.name = "ENTER-M"

define config.version = "0.17.0"

# Optional About-screen description.
define gui.about = _("")

# Distribution basename.
define build.name = "ENTER-M"

# Toggles for different audio features.
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.main_menu_music = audio.mainmenu

# The transitions BETWEEN MENUS (enter/exit/intra/game_main/end_game) live in
# menu_transitions.rpy, next to the choreographies they are built from. The
# transitions between STORY SCENES live in fx.rpy.

# Window settings
define config.window = "auto"
define config.window_show_transition = Dissolve(.18)
define config.window_hide_transition = Dissolve(.14)

# STRICT AUTOMATIC WINDOW OWNERSHIP.
#
# Stock Ren'Py deliberately carries an empty dialogue window through `pause`
# statements. ENTER-M uses pauses as visual beats, so an automatic window should
# be absent for the whole beat instead. Characters with a bespoke say screen use
# the `say-custom` statement name; hiding the stock empty window for that name
# leaves the character's actual say screen as the sole owner of the text layer.
#
# These are statement names reported through Ren'Py's normal window-auto
# callback. They do not affect ATL `pause` clauses or the contents of a custom
# screen.
define config.window_auto_hide += [ "pause", "say-custom" ]

# KEEPING "auto" ARMED.
#
# Window visibility is owned here, not reset piecemeal in story labels. Ordinary
# script must rely on the semantic statement names above and Ren'Py's stock
# scene/menu/call-screen rules. The sole manual exception is `window hide(None)`
# for an authored hard cut where even the normal hide dissolve would be wrong.
#
# Every `window hide`, including the no-transition form, also sets
# `_window_auto = False`. This callback restores automatic ownership on the
# following statement. It is appended after 000window.rpy's callback, so the
# one-statement delay preserves the hard cut and its immediate beat; the next
# dialogue or owned non-dialogue statement resumes normal automatic behavior.
# Bespoke Characters report `say-custom`, keeping the stock box hidden while
# their custom say screen is active.
init python:

    def _enter_m_rearm_window_auto(statement):
        if config.window == "auto" and not store._window_auto:
            store._window_auto = True

    config.statement_callbacks.append(_enter_m_rearm_window_auto)

# Default text speed and auto-forward mode timing
# NUDGE DECIDE 10.5: default is 50 cps but the "Normal" preset is 60. Pick one (plan suggests 60); screens.rpy's reset-to-defaults also writes 50.
default preferences.text_cps = 50          # Characters per second (bigger number = faster text)
default preferences.afm_time = 15          # Auto-forward mode wait time

# Default volume settings
default preferences.music_volume = 1.0
default preferences.sfx_volume = 1.0

# Save identity resolved by the installed MatsuPy launcher.
define config.save_directory = "ENTERM"

# Window icon that appears in your taskbar
define config.window_icon = "assets/gui/window_icon.png"

# Gameplay settings
define config.allow_skipping = True        # Allows player to skip unseen dialogue
define config.has_autosave = False         # Disables autosaving
define config.autosave_on_quit = False
define config.autosave_slots = 0

# Display Layers [defined order of foreground and background elements; do not edit unless you are familiar with ATL]
define config.layers = [ 'master', 'cinematic', 'transient', 'screens', 'overlay', 'front' ]

# Performance settings
define config.image_cache_size = 64        # Cache budget in screen-sized images, not a file count.
define config.predict_statements = 50      # How many statements to look ahead
define config.rollback_enabled = config.developer  # Only enable rollback in dev mode

# Menu settings
define config.menu_clear_layers = ["front"]
define config.gl_test_image = "white"

init python:
    # Keep the launcher's primary save location; omit its secondary sync location.
    # This changes the active locations, not the files already on disk.
    if len(renpy.loadsave.location.locations) > 1:
        del renpy.loadsave.location.locations[1]

    # Disables gamepad support
    renpy.game.preferences.pad_enabled = False

    # Function to replace plain dashes with proper em dashes
    def replace_text(text):
        return text.replace('--', u'\u2014').replace(' - ', u'\u2014')
    config.replace_text = replace_text

    # Function to handle game menu access.
    #
    # Escape opens `_game_menu_screen`, and in play that name has exactly two
    # legitimate values: the engine's own default (captured at the bottom of
    # this file, after init) and None, which a game mode sets to switch the
    # pause OFF for the length of a fight. Anything else is some menu screen's
    # name that escaped from a menu. The title-screen leak that did that is
    # now scoped away at the source (before_main_menu, splash.rpy) -- but a
    # save written before that fix still carries the name, so it is put back
    # here, on the only path that reads it outside a menu. None is left alone.
    def game_menu_check():
        if not quick_menu:
            return

        default_menu_screen = ENTER_M_GAME_MENU_DEFAULT
        if (default_menu_screen is not None
                and store._game_menu_screen is not None
                and store._game_menu_screen != default_menu_screen):
            store._game_menu_screen = default_menu_screen

        renpy.call_in_new_context('_game_menu')

    config.game_menu_action = game_menu_check

init python:
    # Runtime content is classified into the project's mod archive.
    build.archive("mod", "all")

    # Build classification. build.classify is FIRST-MATCH-WINS, so all excludes
    # are grouped ABOVE the includes -- otherwise catch-all dir includes (e.g.
    # game/story/**) would package .rpy/.bak/.md junk before the excludes run.
    # Affects the built distribution only; the SDK still loads every file.

    # --- Excludes ---
    build.classify("**.rpy", None)              # ship compiled .rpyc, never source
    build.classify("/docs/**", None)            # developer docs, including .txt guides
    build.classify("game/**.md", None)          # READMEs, cheatsheets, critiques
    build.classify("/**.md", None)
    build.classify("game/assets/**.txt", None) # asset READMEs and vendor notes
    build.classify("/.claude/**", None)
    build.classify("/.agents/**", None)
    build.classify("/dev/**", None)             # authoring drafts, rollback archives, maintenance evidence
    build.classify("/tmp/**", None)             # isolated QA runs and SDK copies
    build.classify("**sync-conflict**", None)   # Syncthing conflict copies
    # Dev tools (gated by config.developer, never run in release). Do NOT exclude
    # dev.rpy -- it also defines runtime state (player name, singleton, defaults).
    build.classify("/game/addons/Dev Hub/**", None)
    build.classify("/game/addons/Story Writer/**", None)
    build.classify("/game/python-packages/story_writer_**", None)
    build.classify("/game/addons/Developer Date Jump/**", None)
    build.classify("/game/addons/Asahina Rhythm/chart_editor.rpyc", None)
    build.classify("/game/addons/Asahina Rhythm/charts/exports/**", None)
    build.classify("/game/python-packages/asahina_rhythm_editor.py", None)
    build.classify("/game/python-packages/asahina_rhythm_editor.pyc", None)
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
    build.classify("/game/firstrun", None)
    build.classify("/game/cache/*.*", None)
    build.classify("/game/**.rpa", None)
    build.classify("/game/saves/**", None)

    # NUDGE P5: nothing references assets/audio/sfx/kangaroo_court/ (checked Oct 12), so excluding it is free. Uncomment:
    # build.classify("game/assets/audio/sfx/kangaroo_court/**", None)
    # NUDGE P5: sfx/touhou/ IS played by six side modes (Arcade, Invasions, Asarhythm, gacha, Kotonoha, Tsubaki); excluding it silences them (no crash):
    # build.classify("game/assets/audio/sfx/touhou/**", None)
    # --- Includes (only reached by files that survived the excludes) ---
    # MatsuPy's importer reads python-packages through its archive loader. Its
    # protected build converts this source to the corresponding protected .pyc.
    # The chart editor module remains developer-only.
    build.classify("game/python-packages/asahina_rhythm_core.py", "mod")
    build.classify("game/**.jpg", "mod")
    build.classify("game/**.png", "mod")
    build.classify("game/**.webp", "mod")
    build.classify("game/**.gif", "mod")
    build.classify("game/**.rpyc", "mod")
    build.classify("game/**.txt", "mod")
    build.classify("game/**.wav", "mod")
    build.classify("game/**.mp3", "mod")
    build.classify("game/**.ogg", "mod")
    build.classify("game/**.ttf", "mod")
    build.classify("game/**.otf", "mod")
    build.classify("game/story/**", "mod")
    build.classify("game/addons/**", "mod")
    build.classify("game/assets/**", "mod")
    build.classify("game/lost_records/**", "mod")

    # Documentation files to include
    build.documentation('*.html')
    build.documentation('*.txt')

    # Disables including old Matsu'Py themes
    build.include_old_themes = False

    build.package("Mod Export (All Platforms)", "zip", "windows mac linux renpy all")

# The pause menu's destination exactly as the engine set it during init:
# gui.init() -- called from gui.rpy at init offset -2 -- runs layout.defaults(),
# which names the save screen. Read here at init 999, after every init block
# in the project, so it is the pristine value and never one a menu wrote.
# game_menu_check() above heals back to it.
init 999 python:
    ENTER_M_GAME_MENU_DEFAULT = _game_menu_screen
