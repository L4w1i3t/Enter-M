init python:
    menu_trans_time = 1
    splash_message_default = "This game is not suitable for children\nor those who are easily disturbed."
    splash_messages = [
    "Some memories arrive out of order.",
    "Signal found.",
    "The archive remembers.",
    "It's just a story, mostly.",
    "This game is not suitable for children\nor those who are easily disturbed?",
    "connection-lost",
    "null",
    "The room is waiting.",
    "You were only partially awake.",
    "This game is not suitable for children\nor those who are easily disturbed."
    ]

    def enter_m_cleanup_unpickleable_store_values():
        leaked_file = globals().get("f", None)
        if leaked_file is None:
            return

        if not (hasattr(leaked_file, "read") or hasattr(leaked_file, "write") or hasattr(leaked_file, "close")):
            return

        globals().pop("f", None)
        try:
            leaked_file.close()
        except Exception:
            pass

    def enter_m_read_firstrun():
        try:
            return renpy.file("firstrun").read(1)
        except Exception:
            with open(config.basedir + "/game/firstrun", "wb"):
                pass
            return ""

    def enter_m_write_firstrun():
        with open(config.basedir + "/game/firstrun", "w") as firstrun_file:
            firstrun_file.write("1")

image splash_warning = ParameterizedText(style="splash_text", xalign=0.5, yalign=0.5)

image menu_bg:
    topleft
    "mod_assets/gui/menu_bg.png"
    menu_bg_drift

image game_menu_bg:
    topleft
    "mod_assets/gui/menu_bg.png"
    menu_bg_drift

image menu_fade:
    "white"
    menu_fadeout

image menu_art_y = Null()
image menu_art_n = Null()
image menu_art_s = Null()
image menu_art_m = Null()
image menu_art_y_ghost = Null()
image menu_art_n_ghost = Null()
image menu_art_s_ghost = Null()
image menu_art_m_ghost = Null()
image menu_art_s_glitch = Null()

image menu_nav:
    #"gui/overlay/main_menu.png"
    #menu_nav_move

image menu_logo:
    "mod_assets/gui/logo.png"
    subpixel True
    xcenter 640
    ycenter 360
    zoom 0.60
    menu_logo_idle

image menu_particles = Null()

transform particle_fadeout:
    easeout 1.5 alpha 0

transform menu_bg_move:
    subpixel True
    topleft
    parallel:
        xoffset 0 yoffset 0
        linear 3.0 xoffset -100 yoffset -100
        repeat
    parallel:
        ypos 0
        time 0.65
        ease_cubic 2.5 ypos -500

transform menu_bg_loop:
    subpixel True
    topleft
    parallel:
        xoffset 0 yoffset 0
        linear 3.0 xoffset -100 yoffset -100
        repeat

transform menu_bg_drift:
    subpixel True
    zoom 1.035
    xalign 0.5
    yalign 0.5
    block:
        ease 16.0 xoffset -18 yoffset 10
        ease 16.0 xoffset 14 yoffset -8
        repeat

transform menu_logo_idle:
    subpixel True
    block:
        ease 4.5 yoffset -5
        ease 4.5 yoffset 5
        repeat

transform menu_logo_reveal:
    subpixel True
    xcenter 858
    ycenter 322
    zoom 0.56
    alpha 0.0
    yoffset 24
    pause 0.10
    easeout 0.70 alpha 1.0 yoffset 0
    block:
        ease 4.5 yoffset -5
        ease 4.5 yoffset 5
        repeat

transform menu_panel_enter(delay=0.0, xoff=-42, yoff=0):
    subpixel True
    alpha 0.0
    xoffset xoff
    yoffset yoff
    pause delay
    easeout 0.45 alpha 1.0 xoffset 0 yoffset 0

transform menu_button_enter(delay=0.0):
    subpixel True
    on show:
        alpha 0.0
        xoffset -18
        pause delay
        easeout 0.35 alpha 1.0 xoffset 0
    on hover:
        easeout 0.12 xoffset 10
    on idle:
        easeout 0.16 xoffset 0

transform menu_scanline_slow:
    subpixel True
    ypos -24
    alpha 0.0
    pause 0.45
    block:
        alpha 0.0
        ypos -24
        linear 0.12 alpha 0.55
        linear 4.0 ypos 744
        linear 0.18 alpha 0.0
        pause 2.2
        repeat

transform splash_bg_push:
    subpixel True
    zoom 1.08
    xalign 0.5
    yalign 0.5
    alpha 0.0
    easeout 0.55 alpha 0.55
    block:
        ease 10.0 xoffset -14 yoffset 7
        ease 10.0 xoffset 10 yoffset -6
        repeat

transform splash_icon_reveal(xc=640, z=0.32, delay=0.0):
    subpixel True
    xcenter xc
    ycenter 360
    zoom z * 0.95
    alpha 0.0
    yoffset 16
    pause delay
    parallel:
        easeout 0.55 alpha 1.0 yoffset 0
    parallel:
        easeout 0.55 zoom z
    pause 1.55
    easein 0.35 alpha 0.0 yoffset -10

transform splash_panel_reveal:
    subpixel True
    alpha 0.0
    yoffset 22
    pause 0.15
    easeout 0.55 alpha 1.0 yoffset 0

transform splash_sweep:
    subpixel True
    ypos -16
    alpha 0.0
    pause 0.30
    block:
        alpha 0.0
        ypos -16
        linear 0.08 alpha 0.75
        linear 1.6 ypos 736
        linear 0.12 alpha 0.0
        pause 0.7
        repeat

screen enter_m_splash_intro():
    add Solid("#02040b")
    add "mod_assets/gui/menu_bg.png" at splash_bg_push
    add Solid("#00000099")
    add Solid("#75f7ff35") xysize (1280, 2) at splash_sweep
    add "mod_assets/gui/TS_SF_splash.png" at splash_icon_reveal(420, 0.30, 0.10)
    add "mod_assets/gui/TRM_splash.png" at splash_icon_reveal(860, 0.34, 0.10)

screen enter_m_splash_warning(message):
    add Solid("#02040b")
    add "mod_assets/gui/menu_bg.png" at splash_bg_push
    add Solid("#000000cc")
    add Solid("#ff2f5f33") xysize (1280, 2) at splash_sweep

    frame:
        style "splash_warning_panel"
        at splash_panel_reveal

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 18

            text "CONTENT WARNING":
                style "splash_warning_heading"

            text message:
                style "splash_text"

transform menu_logo_move:
    subpixel True
    yoffset -300
    time 1.925
    easein_bounce 1.5 yoffset 0

transform menu_nav_move:
    subpixel True
    xoffset -500
    time 1.5
    easein_quint 1 xoffset 0

transform menu_fadeout:
    easeout 0.75 alpha 0
    time 2.481
    alpha 0.4
    linear 0.5 alpha 0

transform menu_art_move(z, x, z2):
    subpixel True
    yoffset 0 + (1200 * z)
    xoffset (740 - x) * z * 0.5
    zoom z2 * 0.75
    time 1.0
    parallel:
        ease 1.75 yoffset 0
    parallel:
        pause 0.75
        ease 1.5 zoom z2 xoffset 0

image intro:
    truecenter
    "white"
    0.5
    "bg/splash.png" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

image warning:
    truecenter
    "white"
    "splash_warning" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

image tos = "mod_assets/gui/warning.png"
image tos2 = "mod_assets/gui/warning2.png"

label splashscreen:

    $ enter_m_cleanup_unpickleable_store_values()

    python:
        process_list = []
        currentuser = ""
        if renpy.windows:
            try:
                process_list = subprocess.check_output("wmic process get Description", shell=True).lower().replace("\r", "").replace(" ", "").split("\n")
            except:
                pass
            try:
                for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
                    user = os.environ.get(name)
                    if user:
                        currentuser = user
            except:
                pass


    python:
        firstrun = enter_m_read_firstrun()
    if not firstrun:
        if persistent.first_run and (config.version == persistent.oldversion or persistent.autoload == "postcredits_loop"):
            $ quick_menu = False
            scene black
            menu:
                "A previous save file has been found. Would you like to delete your save data and start over?"
                "Yes, delete my existing data.":
                    "Deleting save data...{nw}"
                    python:
                        delete_all_saves()
                        renpy.loadsave.location.unlink_persistent()
                        renpy.persistent.should_save_persistent = False
                        renpy.utter_restart()
                "No, continue where I left off.":
                    $ restore_relevant_characters()

        python:
            if not firstrun:
                try:
                    enter_m_write_firstrun()
                except:
                    renpy.jump("readonly")

    if config.version != persistent.oldversion:
        $ restore_relevant_characters()
        $ persistent.oldversion = config.version
        $ renpy.save_persistent()

    if not persistent.first_run:
        python:
            restore_all_characters()
        $ quick_menu = False
        scene white
        pause 0.5
        scene tos
        with Dissolve(1.0)
        pause 1.0

        # ==================================================================================================================================================
        # CHANGE THIS TO YOUR OWN TERMS OF SERVICE
        # ==================================================================================================================================================

        "This is an early demo build of ENTER-M."
        "This build contains placeholder art, temporary audio, unfinished systems, and experimental scenes."
        "Some presentation, story flow, and archive features may change before a later release."
        "{b}Personal note: some placeholder artwork in this demo was created using Stable Diffusion (with my own trained AI models).{/b}"
        "{b}They're PLACEHOLDERS. This game is being developed by one person who's a talentless hack and also can't afford an artist.{/b}"
        "{b}Please direct all complaints about AI usage to your nearest brick wall.{/b}"
        "{b}Anyway...{/b}"
        "The full story is planned to include mature topics, including but not limited to:"
        "Self-harm."
        "Self-destruction."
        "Sexual Harrassment."
        "Sexual and emotional manipulation."
        "Eating disorders."
        "Medical trauma."
        "Graphic injury."
        "Mental illness."
        "Ego death."
        "Other potential distressing material."
        "By playing this game, you agree that you are of sufficient age and mental state to handle the contents within."
        $ persistent.first_run = True
        scene tos2
        with Dissolve(1.5)
        pause 1.0
        scene white

    python:
        s_kill_early = None
        if persistent.playthrough == 0:
            try: renpy.file("../characters/sayori.chr")
            except: s_kill_early = True
        if not s_kill_early:
            if persistent.playthrough <= 2 and persistent.playthrough != 0:
                try: renpy.file("../characters/monika.chr")
                except: open(config.basedir + "/characters/monika.chr", "wb").write(renpy.file("monika.chr").read())
            if persistent.playthrough <= 1 or persistent.playthrough == 4:
                try: renpy.file("../characters/natsuki.chr")
                except: open(config.basedir + "/characters/natsuki.chr", "wb").write(renpy.file("natsuki.chr").read())
                try: renpy.file("../characters/yuri.chr")
                except: open(config.basedir + "/characters/yuri.chr", "wb").write(renpy.file("yuri.chr").read())
            if persistent.playthrough == 4:
                try: renpy.file("../characters/sayori.chr")
                except: open(config.basedir + "/characters/sayori.chr", "wb").write(renpy.file("sayori.chr").read())

    if not persistent.special_poems:
        python hide:
            persistent.special_poems = [0,0,0]
            a = range(1,12)
            for i in range(3):
                b = renpy.random.choice(a)
                persistent.special_poems[i] = b
                a.remove(b)

    $ basedir = config.basedir.replace('\\', '/')

    if persistent.autoload:
        jump autoload

    $ config.allow_skipping = False

    if s_kill_early:
        show black
        with dissolve_scene_soft
        "Required local character data is missing."
        "Please restore the project files before continuing."
        $ config.allow_skipping = True
        $ renpy.quit()


    scene black
    $ persistent.ghost_menu = False
    $ splash_message = splash_message_default
    $ starttime = datetime.datetime.now()
    show screen enter_m_splash_intro with Dissolve(0.5, alpha=True)
    $ pause(2.80 - (datetime.datetime.now() - starttime).total_seconds())
    hide screen enter_m_splash_intro with Dissolve(max(0, 3.15 - (datetime.datetime.now() - starttime).total_seconds()), alpha=True)
    if persistent.playthrough == 2 and renpy.random.randint(0, 3) == 0:
        $ splash_message = renpy.random.choice(splash_messages)
    show screen enter_m_splash_warning(splash_message) with Dissolve(max(0, 3.50 - (datetime.datetime.now() - starttime).total_seconds()), alpha=True)
    $ pause(5.50 - (datetime.datetime.now() - starttime).total_seconds())
    hide screen enter_m_splash_warning with Dissolve(max(0, 6.00 - (datetime.datetime.now() - starttime).total_seconds()), alpha=True)
    $ pause(6.00 - (datetime.datetime.now() - starttime).total_seconds())
    scene black
    call enter_m_sick_ass_anime_op
    $ config.allow_skipping = True
    return

label after_load:
    $ enter_m_cleanup_unpickleable_store_values()
    if persistent.playthrough == 0:
        $ restore_all_characters()
    $ config.allow_skipping = allow_skipping
    $ _dismiss_pause = config.developer
    $ persistent.ghost_menu = False

    if persistent.yuri_kill > 0 and persistent.autoload == "yuri_kill_2":
        if persistent.yuri_kill >= 1380:
            $ persistent.yuri_kill = 1440
        elif persistent.yuri_kill >= 1180:
            $ persistent.yuri_kill = 1380
        elif persistent.yuri_kill >= 1120:
            $ persistent.yuri_kill = 1180
        elif persistent.yuri_kill >= 920:
            $ persistent.yuri_kill = 1120
        elif persistent.yuri_kill >= 720:
            $ persistent.yuri_kill = 920
        elif persistent.yuri_kill >= 660:
            $ persistent.yuri_kill = 720
        elif persistent.yuri_kill >= 460:
            $ persistent.yuri_kill = 660
        elif persistent.yuri_kill >= 260:
            $ persistent.yuri_kill = 460
        elif persistent.yuri_kill >= 200:
            $ persistent.yuri_kill = 260
        else:
            $ persistent.yuri_kill = 200
        jump expression persistent.autoload

    elif anticheat != persistent.anticheat:
        stop music
        scene black
        "The save file could not be loaded."
        "Are you trying to cheat?"
        $ m_name = "Monika"
        show monika 1 at t11
        if persistent.playername == "":
            m "You're so funny."
        else:
            m "You're so funny, [persistent.playername]."
        $ renpy.utter_restart()
    else:
        if persistent.playthrough == 0 and not persistent.first_load and not config.developer:
            $ persistent.first_load = True
            call screen dialog("Hint: You can use the \"Skip\" button to\nfast-forward through text you've already read.", ok_action=Return())
    return

label autoload:
    python:

        if "_old_game_menu_screen" in globals():
            _game_menu_screen = _old_game_menu_screen
            del _old_game_menu_screen
        if "_old_history" in globals():
            _history = _old_history
            del _old_history
        renpy.block_rollback()


        renpy.context()._menu = False
        renpy.context()._main_menu = False
        main_menu = False
        _in_replay = None

    if persistent.yuri_kill > 0 and persistent.autoload == "yuri_kill_2":
        $ persistent.yuri_kill += 200

    if renpy.get_return_stack():
        $ renpy.pop_call()
    jump expression persistent.autoload

label autoload_yurikill:
    if persistent.yuri_kill >= 1380:
        $ persistent.yuri_kill = 1440
    elif persistent.yuri_kill >= 1180:
        $ persistent.yuri_kill = 1380
    elif persistent.yuri_kill >= 1120:
        $ persistent.yuri_kill = 1180
    elif persistent.yuri_kill >= 920:
        $ persistent.yuri_kill = 1120
    elif persistent.yuri_kill >= 720:
        $ persistent.yuri_kill = 920
    elif persistent.yuri_kill >= 660:
        $ persistent.yuri_kill = 720
    elif persistent.yuri_kill >= 460:
        $ persistent.yuri_kill = 660
    elif persistent.yuri_kill >= 260:
        $ persistent.yuri_kill = 460
    elif persistent.yuri_kill >= 200:
        $ persistent.yuri_kill = 260
    else:
        $ persistent.yuri_kill = 200
    jump expression persistent.autoload

label before_main_menu:
    $ persistent.ghost_menu = False
    $ config.main_menu_music = audio.map003
    $ renpy.music.play(config.main_menu_music)
    return

label quit:
    return

label readonly:
    scene black
    "The game cannot be run because you are trying to run it from a read-only location."
    "Please move ENTER-M to your desktop or another writable location and try again."
    $ renpy.quit()
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
