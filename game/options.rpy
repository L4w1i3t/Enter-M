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
define config.main_menu_music = audio.map003   # Set this to whatever you want the main menu music to be

# These settings control transitions between scenes
define config.enter_transition = Dissolve(.45)
define config.exit_transition = Dissolve(.18)
define config.after_load_transition = None
define config.end_game_transition = Fade(.35, .15, .45, color="#02050a")

# Window settings
define config.window = "auto"
define config.window_show_transition = Dissolve(.18)
define config.window_hide_transition = Dissolve(.14)

# Default text speed and auto-forward mode timing
default preferences.text_cps = 50          # Characters per second (bigger number = faster text)
default preferences.afm_time = 15          # Auto-forward mode wait time

# Default volume settings
default preferences.music_volume = 1
default preferences.sfx_volume = 1

# Save directory - change to match your mod's name. This is located in AppData/Roaming/Ren'Py/ on Windows
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
define config.layers = [ 'master', 'transient', 'screens', 'overlay', 'front' ]

# Performance settings
define config.image_cache_size = 64        # Number of images kept in active memory (higher = more memory usage)
define config.predict_statements = 50      # How many statements to look ahead
define config.rollback_enabled = config.developer  # Only enable rollback in dev mode

# Menu settings
define config.menu_clear_layers = ["front"]
define config.gl_test_image = "white"

init python:
    # Removes persistent data from other Ren'Py games
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

    # Forces integer scaling for better pixel art
    def force_integer_multiplier(width, height):
        if float(width) / float(height) < float(config.screen_width) / float(config.screen_height):
            return (width, float(width) / (float(config.screen_width) / float(config.screen_height)))
        else:
            return (float(height) * (float(config.screen_width) / float(config.screen_height)), height)

init python:
    # Build settings - defines how files are packaged when building your mod
    # Usually you won't need to change this, but it's here for reference
    
    # Define the archives (packages) that will contain your mod's files
    # NOTE FROM MODCEN: WHEN INSTALLING MODS, BE SURE TO ADD ALL FOUR OF THESE COMMENTED OUT RPA ARCHIVES TO THE GAME FOLDER.
    # OTHERWISE THE MOD WILL NOT WORK. LIKE, AT ALL.
    # build.archive("scripts", "all")
    # build.archive("images", "all")
    # build.archive("audio", "all")
    # build.archive("fonts", "all")
    build.archive("mod", "all") # Custom archive to differentiate between mod files and vanilla files

    # Classify which files go into which archives
    build.classify("game/**.jpg", "mod")
    build.classify("game/**.png", "mod")
    build.classify("game/**.webp", "mod")
    build.classify("game/**.gif", "mod")
    build.classify("game/**.rpyc", "mod") # Swap this with rpy to include raw files instead.
    build.classify("game/**.txt", "mod")
    build.classify("game/**.chr", "mod")
    build.classify("game/story/**", "mod") # Custom partitioning for mod story files. Not required, but useful for larger mods
    build.classify("game/addons/**", "mod") # Custom partitioning for mod add-on files. Not required, but useful for larger mods
    build.classify("game/mod_assets/**", "mod") # Add all files and subfolders in the mod_assets folder to the mod archive
    build.classify("game/**.wav", "mod")
    build.classify("game/**.mp3", "mod")
    build.classify("game/**.ogg", "mod")
    build.classify("game/**.ttf", "mod")
    build.classify("game/**.otf", "mod")

    # Files that should be excluded from the build
    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('**.rpy', None) # Swap this with rpyc to exclude compiled files instead
    build.classify('**.psd', None)
    build.classify('**.sublime-project', None)
    build.classify('**.sublime-workspace', None)
    build.classify('/music/*.*', None)
    build.classify('script-regex.txt', None)
    build.classify('/game/10', None)
    build.classify('/game/cache/*.*', None)
    build.classify('/game/**.rpa', None)      # Exclude all .rpa files
    build.classify('/game/firstrun', None)  # Exclude the firstrun file
    build.classify('/game/**.bak', None)
    build.classify('**/.vscode/**', None)
    build.classify('**/__pycache__/**', None)
    build.classify('/**.bat', None)
    build.classify('/traceback.txt', None)
    build.classify('/errors.txt', None)
    build.classify('/log.txt', None)
    build.classify('/README.md', None)
    build.classify('**/.git/**', None)
    build.classify('**/.github/**', None)
    build.classify('/game/saves/**', None)  # Exclude save files

    # Documentation files to include
    build.documentation('*.html')
    build.documentation('*.txt')

    # Disables including old Ren'Py themes
    build.include_old_themes = False

    build.package("Mod Export (All Platforms)", "zip", "windows mac linux renpy all")

##### Commented out as we have no use for this
# define build.itch_project = "teamsalvato/ddlc"

# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
