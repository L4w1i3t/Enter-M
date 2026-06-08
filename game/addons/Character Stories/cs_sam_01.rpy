# Sam Character Story 01 -- "Purgatorium"
# Inspired by the "weird/creepy bootleg video game" form of horror.
# Think corrupted mobile game ports, uncanny asset swaps, and things
# that feel just slightly *wrong* -- like someone copied a game from
# memory and filled in the gaps with nightmares.

# -- Earthquake screen-shake transform --
# Function-driven so every jolt is genuinely random in magnitude,
# direction, and timing. Sporadic dead frames where nothing moves
# make the next hit feel worse.
init python:
    import random as _rng
    def earthquake_fn(trans, st, at):
        if _rng.random() < 0.20:
            trans.xoffset = 0
            trans.yoffset = 0
            return _rng.uniform(0.01, 0.04)
        intensity = _rng.uniform(4, 14)
        trans.xoffset = _rng.uniform(-intensity, intensity)
        trans.yoffset = _rng.uniform(-intensity, intensity)
        return _rng.uniform(0.008, 0.03)

    _purg_popup_ad_pool = {
        4: [
            ("LUCKY WALLET", "Claim 50,000 SOULCOIN before midnight.", "TAP VERIFY HUMAN", "#100700ee", "#ffbf00", "#fff0a6", "#ffcf33"),
            ("APK BOOSTER 2026", "Make any romance game 300% more intimate.", "INSTALL NOW", "#07110bee", "#59ff8a", "#c8ffd5", "#19c45a"),
            ("LOCAL CHAT", "3 lonely girls near your school are waiting.", "OPEN THREAD", "#150515ee", "#ff66ba", "#ffd0ee", "#e23c9c"),
            ("SYSTEM CLEANER", "34 hidden files found in Downloads.", "FIX PHONE", "#050d16ee", "#62d8ff", "#c8f3ff", "#2098c8"),
        ],
        5: [
            ("PURGATORIUM COINS", "Double Desire gains with premium route keys.", "WATCH AD", "#160202ee", "#ff4a4a", "#ffd0d0", "#c92a2a"),
            ("UNLOCKED APK", "No checks. No permissions. No refund.", "SIDELOAD", "#0a050fee", "#b771ff", "#ebd4ff", "#7625c8"),
            ("CRYPTO BRIDE", "Stake your heart. Withdraw never.", "CONNECT WALLET", "#03110fee", "#38ffc8", "#c8fff3", "#13a984"),
            ("FINAL OFFER", "She will remember every tap.", "CLAIM ENDING", "#130b02ee", "#ff9f38", "#ffe2bb", "#c46a18"),
        ],
    }

    _purg_popup_ad_positions = [
        (36, 56, 326),
        (884, 66, 346),
        (58, 330, 342),
        (858, 342, 352),
        (468, 48, 342),
    ]

    def purg_popup_ad_next(day=4):
        global purg_popup_ad_state
        pool = _purg_popup_ad_pool.get(day, _purg_popup_ad_pool[4])
        x, y, w = _rng.choice(_purg_popup_ad_positions)
        title, body, cta, bg, accent, body_color, button = _rng.choice(pool)
        purg_popup_ad_state = {
            "x": x,
            "y": y,
            "w": w,
            "title": title,
            "body": body,
            "cta": cta,
            "bg": bg,
            "accent": accent,
            "body_color": body_color,
            "button": button,
        }
        renpy.restart_interaction()

    def purg_popup_ad_clear(restart=True):
        global purg_popup_ad_state
        purg_popup_ad_state = None
        if restart:
            renpy.restart_interaction()

default purg_popup_ad_state = None

transform earthquake:
    subpixel True
    function earthquake_fn

# -- Face push-in transform --
# Starts from t11 resting position (xcenter 640, zoom 0.80, yoffset 0)
# and eases into a close-up where only the face and upper shoulders fill
# the 1280x720 frame.
# At zoom 2.0 the sprite is 1280x1920.  yanchor 1.0 + ypos 1.03 places
# the bottom at y=741.6; the full height is 1920, so the top of the
# sprite sits at 741.6 - 1920 = -1178.4.  Adding yoffset 1100 shifts
# everything down by 1100px, landing the top at -78.4 -- flush with
# the screen top.  The visible window then covers the original
# y=0-360px range (face and upper shoulders only).
# easein: starts slow and accelerates, like being pulled forward.
transform purg_facepush:
    yanchor 1.0 ypos 1.03 xcenter 640 zoom 0.80 yoffset 0 subpixel True
    on replace:
        parallel:
            easein 1.5 zoom 2.0
        parallel:
            easein 1.5 yoffset 1100

# -- Sprite creep transform for purg_girl_day7 --
# Slow linear ease on replace so each zoom step bleeds across
# several dialogue lines rather than snapping -- the player feels
# her getting closer without ever catching the exact moment it happened.
transform purg_creep(z=0.80):    # yanchor 0.0 pins the top of the sprite (her head).
    # ypos -0.037 matches where her head sits in the standard
    # yanchor 1.0 ypos 1.03 z=0.80 framing, so the first step
    # is a seamless continuation of the swap position.
    # As zoom increases, the body grows downward off-screen
    # while the head stays fixed -- she creeps toward the camera.
    yanchor 0.0 ypos -0.037 xcenter 640 zoom z subpixel True
    on replace:
        linear 1.5 zoom z

# Characters specific to this story.
# The entity: no name, red text, no CTC -- the absence of the click
# indicator makes the player sit in uncertainty after each line.
define _purg_entity = Character(None, what_color="#cc0000", what_outlines=[(1, "#330000", 0, 0)])

# The "girl" in the bootleg game. Generic by design.
define _purg_girl = Character("Girl", what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")

# Gameplay-story integration screens.
# These simulate the player's in-game behavior mechanically,
# so the Day 7 accusations land with experiential weight.

# Fake "skip mode" indicator, as if the player is fast-forwarding.
transform purg_skip_alpha:
    alpha 0.7

transform purg_phone_frame_jitter:
    subpixel True
    block:
        choice:
            xoffset 0
            yoffset 0
        choice:
            xoffset 1
            yoffset 0
        choice:
            xoffset -1
            yoffset 0
        choice:
            xoffset 0
            yoffset 1
        0.06
        repeat

transform purg_phone_static_soft:
    alpha 0.018
    block:
        linear 0.10 alpha 0.035
        linear 0.16 alpha 0.018
        pause 0.55
        repeat

transform purg_phone_static_dirty:
    alpha 0.038
    block:
        linear 0.08 alpha 0.070
        linear 0.14 alpha 0.028
        pause 0.28
        linear 0.05 alpha 0.085
        linear 0.10 alpha 0.038
        pause 0.42
        repeat

transform purg_phone_static_rotten:
    alpha 0.065
    block:
        linear 0.05 alpha 0.120
        linear 0.07 alpha 0.035
        pause 0.14
        linear 0.04 alpha 0.100
        linear 0.08 alpha 0.055
        pause 0.20
        repeat

transform purg_phone_warning_blink:
    alpha 0.35
    block:
        linear 0.18 alpha 0.95
        pause 0.08
        linear 0.32 alpha 0.35
        pause 0.75
        repeat

transform purg_popup_ad_blink:
    alpha 0.85
    block:
        linear 0.08 alpha 1.0
        linear 0.12 alpha 0.72
        pause 0.18
        linear 0.05 alpha 1.0
        pause 0.65
        repeat

transform purg_popup_ad_shake:
    subpixel True
    on show:
        xoffset -6
        alpha 0.0
        linear 0.06 xoffset 4 alpha 1.0
        linear 0.05 xoffset -2
        linear 0.05 xoffset 0
    block:
        pause 0.35
        choice:
            xoffset 0
            yoffset 0
        choice:
            xoffset 2
            yoffset 0
        choice:
            xoffset -2
            yoffset 1
        0.05
        xoffset 0
        yoffset 0
        repeat

transform purg_intrusion_drop:
    subpixel True
    on show:
        yoffset -42
        alpha 0.0
        easeout 0.08 yoffset 0 alpha 1.0
    on hide:
        linear 0.05 alpha 0.0

transform purg_intrusion_snap:
    subpixel True
    on show:
        zoom 1.04
        alpha 0.0
        linear 0.05 zoom 1.0 alpha 1.0
    block:
        pause 0.28
        choice:
            xoffset 0
        choice:
            xoffset 2
        choice:
            xoffset -2
        0.04
        xoffset 0
        repeat

transform purg_intrusion_flicker:
    alpha 0.65
    block:
        linear 0.06 alpha 1.0
        linear 0.08 alpha 0.45
        pause 0.10
        linear 0.04 alpha 0.95
        pause 0.38
        repeat

screen purg_skip_mode():
    zorder 130
    text ">>> SKIP >>>" align (0.97, 0.03) color "#ffff00" size 16 at purg_skip_alpha

# Stat overlay that intrudes mid-conversation.
screen purg_stat_popup(stat_name, stat_val):
    zorder 130
    timer 1.5 action Hide("purg_stat_popup")
    frame:
        align (0.95, 0.08)
        background "#000000aa"
        padding (12, 8)
        text "[stat_name]: [stat_val]" color "#ff6666" size 18

# Persistent phone glass for the Purgatorium app. Kept as a screen so the
# same treatment can cover title cards, fake gameplay, choices, and menus.
screen purg_phone_overlay(phase=1):
    zorder 120
    modal False

    $ _phase = max(1, min(3, phase))

    fixed:
        at purg_phone_frame_jitter

        add Solid("#06130e14") xysize (1280, 720)

        if _phase == 1:
            add "noise" at purg_phone_static_soft
        elif _phase == 2:
            add "noise" at purg_phone_static_dirty
        else:
            add "noise" at purg_phone_static_rotten

        for y in range(34, 704, 12):
            add Solid("#00000020") xpos 0 ypos y xsize 1280 ysize 1

        add Solid("#000000d8") xpos 0 ypos 0 xsize 1280 ysize 28
        add Solid("#000000cc") xpos 0 ypos 704 xsize 1280 ysize 16
        add Solid("#020403e8") xpos 0 ypos 0 xsize 6 ysize 720
        add Solid("#020403e8") xpos 1274 ypos 0 xsize 6 ysize 720
        add Solid("#0a1f15aa") xpos 7 ypos 29 xsize 2 ysize 674
        add Solid("#39080888") xpos 1271 ypos 29 xsize 2 ysize 674

        text "NO SIM" xpos 18 ypos 7 size 12 color "#8fffaacc" outlines [(1, "#001208", 0, 0)]
        text "01:36" xalign 0.5 ypos 7 size 12 color "#b7ffcfcc" outlines [(1, "#001208", 0, 0)]
        text "com.purgatorium.free" xpos 112 ypos 7 size 12 color "#607466cc"
        text "BAT --%" xpos 1168 ypos 7 size 12 color "#8fffaacc" outlines [(1, "#001208", 0, 0)]
        text "<      O      [[]" xalign 0.5 ypos 705 size 13 color "#6c776fcc"

        if _phase >= 2:
            add Solid("#00ff551c") xpos 82 ypos 116 xsize 190 ysize 2
            add Solid("#ff00331c") xpos 89 ypos 120 xsize 190 ysize 2
            add Solid("#00d9ff18") xpos 928 ypos 312 xsize 236 ysize 3
            add Solid("#ff003318") xpos 916 ypos 316 xsize 236 ysize 3
            text "UNSIGNED APK" xpos 1028 ypos 47 size 12 color "#ff554fcc" at purg_phone_warning_blink

        if _phase >= 3:
            add Solid("#00000050") xpos 0 ypos 96 xsize 1280 ysize 3
            add Solid("#ffffff16") xpos 0 ypos 99 xsize 1280 ysize 1
            add Solid("#0000005c") xpos 0 ypos 438 xsize 1280 ysize 4
            add Solid("#ff003020") xpos 338 ypos 190 xsize 412 ysize 2
            add Solid("#00ff7020") xpos 346 ypos 194 xsize 412 ysize 2
            text "VERIFY FAIL" xpos 42 ypos 47 size 12 color "#ff554fcc" at purg_phone_warning_blink

screen purg_popup_ads(day=4):
    zorder 126
    modal False

    on "show" action Function(purg_popup_ad_clear, False)
    on "hide" action Function(purg_popup_ad_clear, False)
    timer 1.15 action Function(purg_popup_ad_next, day)
    timer (3.7 if day == 4 else 2.8) action Function(purg_popup_ad_next, day) repeat True

    if purg_popup_ad_state is not None:
        timer 1.65 action Function(purg_popup_ad_clear)
        $ ad = purg_popup_ad_state

        frame:
            xpos ad["x"]
            ypos ad["y"]
            xsize ad["w"]
            background Solid(ad["accent"])
            padding (2, 2)
            at purg_popup_ad_shake

            frame:
                xfill True
                background Solid(ad["bg"])
                padding (10, 8, 10, 10)

                vbox:
                    spacing 5

                    hbox:
                        xfill True
                        text ad["title"] size 16 color ad["accent"] bold True xalign 0.0
                        text "X" size 15 color "#111111" xalign 1.0 outlines [(1, ad["accent"], 0, 0)]

                    text ad["body"] size 13 color ad["body_color"] xmaximum (ad["w"] - 24)

                    frame:
                        xfill True
                        ysize 28
                        background Solid(ad["button"])
                        at purg_popup_ad_blink

                        text ad["cta"] size 12 color "#050505" bold True align (0.5, 0.5)

screen purg_android_banner(title, body, accent="#ff554f"):
    zorder 136
    modal False

    frame:
        xalign 0.5
        ypos 38
        xsize 760
        background Solid("#070b09f0")
        padding (12, 10)
        at purg_intrusion_drop

        hbox:
            spacing 12
            add Solid(accent) xysize (8, 48)
            vbox:
                spacing 3
                text title size 16 color accent bold True
                text body size 14 color "#d7e4dc"

screen purg_android_permission(permission, detail):
    zorder 136
    modal False

    frame:
        align (0.5, 0.5)
        xsize 520
        background Solid("#070807f4")
        padding (18, 16)
        at purg_intrusion_snap

        vbox:
            spacing 14
            text "Purgatorium" size 18 color "#f3f3f3" bold True
            text "Allow access to [permission]?" size 22 color "#ffffff"
            text detail size 14 color "#9ca8a0"

            hbox:
                xalign 1.0
                spacing 18
                frame:
                    background Solid("#161616")
                    padding (14, 8)
                    text "DENY" size 13 color "#5f6a62"
                frame:
                    background Solid("#2bb76d")
                    padding (14, 8)
                    text "ALLOW" size 13 color "#031008" bold True

screen purg_android_anr():
    zorder 136
    modal False

    frame:
        align (0.5, 0.5)
        xsize 500
        background Solid("#080808f6")
        padding (18, 16)
        at purg_intrusion_snap

        vbox:
            spacing 14
            text "Purgatorium isn't responding" size 21 color "#ffffff"
            text "System UI cannot close this app." size 14 color "#a8a8a8"
            hbox:
                xalign 1.0
                spacing 14
                frame:
                    background Solid("#151515")
                    padding (12, 8)
                    text "CLOSE APP" size 13 color "#707070"
                frame:
                    background Solid("#151515")
                    padding (12, 8)
                    text "WAIT" size 13 color "#707070"

screen purg_android_home_flash():
    zorder 136
    modal False

    add Solid("#020507f4") xysize (1280, 720) at purg_intrusion_snap
    text "01:36" align (0.5, 0.14) size 42 color "#d9ffe5"
    text "No service    BAT --%" align (0.5, 0.22) size 14 color "#8aa292"

    grid 4 2:
        align (0.5, 0.52)
        spacing 42
        for app_name, app_color in [
            ("Downloads", "#4c6578"),
            ("Gallery", "#7a405f"),
            ("Messages", "#315f42"),
            ("Contacts", "#3f527c"),
            ("Wallet", "#736027"),
            ("Cleaner", "#447070"),
            ("Dating", "#793957"),
            ("Purgatorium", "#5f0707"),
        ]:
            vbox:
                spacing 7
                xsize 118
                add Solid(app_color) xysize (54, 54) xalign 0.5
                text app_name size 12 color "#d7d7d7" xalign 0.5

    text "<      O      [[] " xalign 0.5 ypos 704 size 13 color "#87918a"

screen purg_corrupt_history_log():
    zorder 136
    modal False

    frame:
        align (0.5, 0.5)
        xsize 930
        ysize 540
        background Solid("#050507f4")
        padding (22, 18)
        at purg_intrusion_snap

        vbox:
            spacing 10
            text "History" size 22 color "#f0f0f0"
            null height 6
            text "Girl: I grew up near the mountains. My mom used to garden..." size 17 color "#777777"
            text "Girl: I wanted to be a painter when I was little." size 17 color "#777777"
            text ">>> SKIP >>>" size 17 color "#ffff00" at purg_intrusion_flicker
            text "Girl: Sometimes I wonder if anyone would even notice if I just..." size 17 color "#a0a0a0"
            text "System: route input accepted" size 16 color "#ff6666"
            text "System: silence bonus +20" size 16 color "#ff6666"
            text "Girl: Sorry -- that got really heavy." size 17 color "#555555"

screen purg_corrupt_save_slots():
    zorder 136
    modal False

    frame:
        align (0.5, 0.5)
        xsize 860
        ysize 500
        background Solid("#060608f5")
        padding (20, 18)
        at purg_intrusion_snap

        vbox:
            spacing 12
            text "Save" size 22 color "#f0f0f0"
            for slot_name, slot_meta in [
                ("AUTO-1", "1:36 AM  -  restored from cache"),
                ("CONTACTS_BACKUP_FAILED", "41 entries removed"),
                ("ROUTE_OPTIMIZED", "choices compressed"),
                ("RECOVERY_DISABLED", "cloud sync unavailable"),
            ]:
                frame:
                    xfill True
                    background Solid("#101015")
                    padding (12, 8)
                    hbox:
                        spacing 28
                        text slot_name size 16 color "#ff6666" xsize 290
                        text slot_meta size 15 color "#999999"

screen purg_final_offer_intrusion():
    zorder 136
    modal False

    frame:
        align (0.5, 0.46)
        xsize 430
        background Solid("#ff9f38")
        padding (2, 2)
        at purg_intrusion_snap

        frame:
            xfill True
            background Solid("#130b02f4")
            padding (12, 10)

            vbox:
                spacing 8
                text "FINAL OFFER" size 22 color "#ff9f38" bold True
                text "She will remember every tap." size 15 color "#ffe2bb"
                frame:
                    xfill True
                    ysize 34
                    background Solid("#ff9f38")
                    text "YOU ALREADY DID" size 13 color "#050505" bold True align (0.5, 0.5)

label cs_sam_01:
    stop music fadeout 1.0
    stop sound
    scene black
    window hide
    pause 1.0
    show text "DISCLAIMER: This story contains flashing lights and disturbing imagery. Reader discretion is advised." at truecenter
    $ pause()
    hide text with dissolve

    # -----------------------------------------------------------------
    #  OPENING -- The Hell CG
    # -----------------------------------------------------------------
    play music hellbassboost noloop

    show cg hell2 zorder 1 at earthquake:
        alpha 0.0
        linear 1.5 alpha 1.0
    show vignette zorder 99:
        alpha 1.0
        linear 1.5 alpha 0.75
    with Dissolve(1.5)

    pause 4.0

    # -----------------------------------------------------------------
    #  CUT TO BLACK
    # -----------------------------------------------------------------
    stop music
    hide vignette
    scene black
    with None

    pause 2.0

    # =================================================================
    #  ACT I -- Sam's Room, 1:36 AM
    # =================================================================

    scene bg sam_room_night
    show vignette zorder 99:
        alpha 0.3
    with dissolve_scene_half
    play music twelveam

    window auto
    "1:36 AM."
    "The ceiling fan clicks on every third rotation."
    "Sam picks up his phone. The screen is still warm."
    "His notification bar is crowded, with three dating apps and a {i}Downloads{/i} folder he'd never open with someone else in the room."
    "He swipes past a text from a girl he stopped answering two weeks ago. She sent four messages since, but he read none of them."
    "Before that, there was the one from the party. Before her, the one from the app. Before her -- he doesn't keep track, without any interest."
    "He's been scrolling through dead forums since midnight, through archived threads and posts from accounts that don't exist anymore."
    "Three pages deep in a thread about abandoned mobile games, someone posted a link."
    "No thumbnail. No publisher. Just a file and two words: {i}free download{/i}."
    "Fourteen replies, all deleted."
    "He taps the link."
    "The progress bar fills wrong: 2 percent, 89, back to 61, then full. Three seconds."
    "An icon appears on his home screen. No label; just a gray square."
    "He opens it hesitantly."
    show screen purg_phone_overlay(1)

    # =================================================================
    #  ACT II -- The Game
    # =================================================================

    stop music fadeout 1.5
    scene black
    window hide
    pause 1.0

    # -- Fake Title Screen --
    play music ghostmenu fadein 0.5

    show text "{size=+30}P U R G A T O R I U M{/size}\n\n{size=-2}{color=#666666}v??.??.??{/color}\n\n\n{color=#888888}Tap to start{/color}{/size}" at truecenter:
        alpha 0.0
        linear 1.0 alpha 1.0
    $ pause()
    hide text with dissolve
    stop music fadeout 0.5
    pause 0.5

    # -----------------------------------------------------------------
    #  DAY 1 -- First Impressions
    # -----------------------------------------------------------------

    show text "{size=+20}{b}DAY 1{/b}{/size}" at truecenter with dissolve
    pause 1.5
    hide text with dissolve
    pause 0.3

    scene bg corridor
    with dissolve_scene_full
    play music beautiful

    window auto

    "You are a transfer student at a new school."
    "Today is your first day. Sunlight pours through the corridor windows in warm, golden sheets."
    "Students mill around in small clusters, their faces pleasant and interchangeable."
    "A girl is standing near the shoe lockers."
    "She has long hair, soft features, and a gentle figure."
    "She notices you right away."

    show purg_girl at t11 zorder 10 with dissolve

    # Gameplay-story integration: simulated screenshot flash.
    # Day 7's "You screenshotted me on Day 1" maps to this.
    show white zorder 200:
        alpha 0.5
    pause 0.06
    show white zorder 200:
        alpha 0.5
        linear 0.2 alpha 0.0
    pause 0.25
    hide white

    _purg_girl "Hi! Are you the new transfer student?"
    _purg_girl "I just had a feeling today would be special. I'm so glad I was right!"

label .day1_choice:
    menu:
        "Talk to her":
            pass
        "Walk away":
            "You turn to leave."
            pause 0.3
            "Your feet don't move."
            "The hallway hasn't changed. She hasn't blinked."
            _purg_girl "Hi! Are you the new transfer student?"
            jump .day1_choice

    "She tells you about the school -- the clubs, the courtyard, the cherry blossoms in spring."
    "She mentions she's single. Twice, as if making sure you heard it."
    "She asks about your hobbies. Your favorite food. Whether you prefer cats or dogs. A bombardment of questions, with no pause for your answers."

    _purg_girl "You're really interesting, you know that? Most people here are so boring."
    _purg_girl "But you... you're different."

    "The bell rings."

    _purg_girl "Oh... I guess we have to go to class."
    _purg_girl "Hey... promise you'll come find me at lunch? I'll save you a seat!"

    menu:
        "\"Sure, sounds good.\"":
            pass
        "\"I'll think about it.\"":
            _purg_girl "I'll save you a seat anyway!"

    scene bg classroom_purg
    with dissolve_scene_half
    show purg_girl at t11 zorder 10

    "Classes pass in a montage. The teacher's mouth moves, but the subtitles just say {i}(Teacher explains lesson){/i}."
    "At lunch, she's exactly where she said she'd be. Same pose, same expression."

    _purg_girl "You came! I knew you would!"

    "She talks for the entire period. She likes baking, sunset walks, and being with someone special."
    "She asks if you've ever been in love."

    menu:
        "\"You're really easy to talk to.\"":
            pass
        "\"I've never met anyone like you.\"":
            pass

    "A pink gradient washes across her cheeks in one frame."

    _purg_girl "D-Do you really mean that? Nobody's ever said something so nice to me before..."
    _purg_girl "Hey... do you want to walk home together? I know a really pretty shortcut through the park."

    menu:
        "\"Sure, I'd love to.\"":
            pass
        "\"Yeah, of course.\"":
            pass

    scene bg park_washed
    with dissolve_scene_half
    show purg_girl at t11 zorder 10

    "She takes your hand. The park is pretty -- cherry blossom petals fall in a loop, the same four petal textures cycling over and over."
    "She says goodbye at the gate."

    _purg_girl "Today was the best day I've had in... ever, honestly."
    _purg_girl "See you tomorrow?"

    "She waves until you're out of frame."

    stop music fadeout 1.0
    scene black with dissolve
    window hide
    pause 0.5

    show text "{size=+15}{b}LEVEL COMPLETE{/b}{/size}\n\n\n{color=#999999}Affection: 60{/color}\n{color=#999999}Trust: 40{/color}\n{color=#999999}Desire: 15{/color}\n\n{color=#666666}Rank: E{/color}" at truecenter with dissolve
    pause 3.0
    hide text with dissolve
    pause 0.5

    # -- Sam's room, between days --
    hide screen purg_phone_overlay
    scene bg sam_room_night
    show vignette zorder 99:
        alpha 0.3
    with dissolve_scene_half

    window auto
    "Sam scrolls back through the dialogue. He skips everything she said about the clubs, the courtyard, the cherry blossoms, everything."
    "He pauses on her character art and zooms in."
    "He screenshots it for later."
    "Desire: 15. That's low. He wonders how to get it higher."

    window hide
    show screen purg_phone_overlay(1)
    scene black with dissolve
    pause 0.5

    # -----------------------------------------------------------------
    #  DAY 2 -- Thoughtful Gestures
    # -----------------------------------------------------------------

    show text "{size=+20}{b}DAY 2{/b}{/size}" at truecenter with dissolve
    pause 1.5
    hide text with dissolve
    pause 0.3

    scene bg classroom_purg
    with dissolve_scene_full
    play music beautiful

    window auto

    "Morning again -- the same corridor, the same golden light."
    "She's at the shoe lockers, in the exact same spot as yesterday."

    show purg_girl at t11 zorder 10 with dissolve

    _purg_girl "Good morning! I woke up extra early today."

    "She holds out a small wrapped box. The wrapping is flawless and creased at perfect ninety-degree angles."

    _purg_girl "I made you lunch! I was up since five. I hope you like it..."

    menu:
        "Accept the gift":
            _purg_girl "You like it?! Oh, I'm so relieved!"
        "\"You didn't have to do that.\"":
            _purg_girl "I wanted to! Making things for you makes me happy."

    "The bento is perfect -- magazine-perfect, with every grain of rice aligned."
    "You eat lunch together. She watches you eat, but she doesn't touch her own food."

    _purg_girl "I'm not hungry. Seeing you enjoy it is enough for me."

    "After school, she suggests the library."

    scene bg club_day
    with dissolve_scene_half
    show purg_girl at t11 zorder 10

    "The library is empty. Nothing but shelves, silence, and her."
    "She sits beside you, her knee touching yours."

    _purg_girl "You know, I don't really get to talk about myself much."

    # Gameplay-story integration: forced dialogue skip.
    # The game auto-advances through her personal backstory,
    # mirroring how Sam treats anything that isn't about him.
    # Day 7's "You skipped my dialogue" becomes literal.
    show screen purg_skip_mode()
    _purg_girl "{cps=*12}I grew up near the mountains. My mom used to garden and I'd help her every morning before school.{/cps}{w=0.2}{nw}"
    _purg_girl "{cps=*12}I wanted to be a painter when I was little. I used to sketch the view from my window every single day.{/cps}{w=0.15}{nw}"
    _purg_girl "{cps=*12}I don't really have many friends here. Most people don't seem to notice me at all.{/cps}{w=0.15}{nw}"
    _purg_girl "{cps=*12}Sometimes I wonder if anyone would even notice if I just... stopped showing up.{/cps}{w=0.2}{nw}"
    _purg_girl "{cps=*12}Sorry -- that got really heavy. I just feel like I can talk to you, you know?{/cps}{w=0.15}{nw}"
    hide screen purg_skip_mode

    _purg_girl "Can I ask you something personal?"
    _purg_girl "Do you think about me when we're not together?"

    menu:
        "\"Yeah, I do.\"":
            _purg_girl "Really?! That makes me so happy..."
        "\"Sometimes.\"":
            _purg_girl "Sometimes is okay. I think about you all the time."

    "She walks you to the gate. Upon reaching the destination, she stands on her toes and kisses your cheek."
    "A small heart icon has appeared in the top corner of the screen. It pulses gently."

    stop music fadeout 1.0
    scene black with dissolve
    window hide
    pause 0.5

    show text "{size=+15}{b}LEVEL COMPLETE{/b}{/size}\n\n\n{color=#999999}Affection: 78{/color}\n{color=#999999}Trust: 60{/color}\n{color=#999999}Desire: 35{/color}\n\n{color=#666666}Rank: D{/color}" at truecenter with dissolve
    pause 3.0
    hide text with dissolve
    pause 0.5

    # -- Sam's room, between days --
    hide screen purg_phone_overlay
    scene bg sam_room_night
    show vignette zorder 99:
        alpha 0.3
    with dissolve_scene_half

    window auto
    "Desire: 35, and still climbing."
    "Sam opens the pause menu and checks her character profile. Height, weight, measurements. The game lists all three."
    "He doesn't check her hobbies tab."
    "She asked if he thinks about her when they're apart. The real answer is that he hasn't thought about her at all."
    "He closes the app and opens a video essay -- the history of a cancelled game he's never played. He skips to the thumbnail he wanted to see, watches twenty seconds, then tabs away."
    "He's thinking about her now, though. About her, about how this all ends..."
    "..."
    "He opens the app again."

    window hide
    show screen purg_phone_overlay(2)
    scene black with dissolve
    pause 0.5

    # -----------------------------------------------------------------
    #  DAY 3 -- The Festival
    # -----------------------------------------------------------------

    show text "{size=+20}{b}DAY 3{/b}{/size}" at truecenter with dissolve
    pause 1.5
    hide text with dissolve
    pause 0.3

    scene bg courtyard_purg
    show vignette zorder 50:
        alpha 1.0
    show noise zorder 11:
        alpha 0.02
    with dissolve_scene_full
    play music beautiful

    window auto

    "It's festival day. Paper lanterns hang from the eaves and hand-painted banners line the walkway."
    "The courtyard feels thinner than yesterday, with fewer faces filling it."
    "The girl finds you before you can look for her."

    show purg_girl_yukata at t11 zorder 10 with dissolve

    _purg_girl "There you are! I've been counting the minutes."

    "She's wearing a yukata. The pattern is flowers, meticulously rendered."
    "She grabs your arm and pulls you through the stalls."

    _purg_girl "Let's do everything together! The goldfish scoop, the shooting gallery, the --"

    "She stops."
    "Across the courtyard, near the taiyaki stand, there's another girl."
    "She has the same long hair, the same soft features, completely identical to the girl beside you."
    "She's standing perfectly still, facing a wall."

    _purg_girl "What were you looking at?"

    menu:
        "\"Nothing.\"":
            pass
        "\"That girl over there looks like --\"":
            "The space by the taiyaki stand is empty."
            _purg_girl "Looks like who? Silly!"

    "The festival continues. She wins you a prize at the shooting gallery, every shot a bullseye."
    "The booth operator doesn't react."
    "She gives you a stuffed bear. The game adds it to an inventory you didn't know you had."

    _purg_girl "Now you'll have something to remember today by!"

    "The fireworks begin, and she leans against your shoulder."

    # Gameplay-story integration: stat overlay during emotional moment.
    # The entity's "You were watching the Desire stat" maps to this.
    show screen purg_stat_popup("Desire", "55")

    _purg_girl "This is perfect. You're perfect."
    _purg_girl "I've been practicing what to say to you all week."

    "..."
    "All week. You've known her for three days."

    _purg_girl "I just mean... I want every moment with you to be special."

    "The fireworks loop through the same three patterns."

    stop music fadeout 1.0
    scene black with dissolve
    window hide
    pause 0.5

    show text "{size=+15}{b}LEVEL COMPLETE{/b}{/size}\n\n\n{color=#999999}Affection: 85{/color}\n{color=#999999}Trust: 70{/color}\n{color=#999999}Desire: 55{/color}\n\n{color=#666666}Rank: C{/color}" at truecenter with dissolve
    pause 3.0
    hide text with dissolve
    pause 0.5

    # -- Sam's room, between days --
    hide screen purg_phone_overlay
    scene bg sam_room_night
    show vignette zorder 99:
        alpha 0.3
    with dissolve_scene_half

    window auto
    "Sam's phone buzzes; it's the girl from two weeks ago again. Five messages sit unread, and he deletes the entire thread."
    "He reopens Purgatorium instead for the umpteenth time."
    "Desire: 55. The yukata helped, and he wonders if there are other outfits."
    "He remembers the duplicate girl from the festival, standing by the wall. He thinks about it for a second."

    window hide
    show screen purg_phone_overlay(2)
    scene black with dissolve
    pause 0.5

    # -----------------------------------------------------------------
    #  DAY 4 -- Closer
    # -----------------------------------------------------------------

    show text "{size=+20}{b}DAY 4{/b}{/size}" at truecenter with dissolve
    pause 1.5
    hide text with dissolve
    pause 0.3

    scene bg corridor
    show vignette zorder 50:
        alpha 1.0
    show noise zorder 11:
        alpha 0.04
    with dissolve_scene_full
    show screen purg_popup_ads(4)
    play music beautiful

    window auto

    "The corridor looks exactly the same as yesterday, down to the light filtering through the windows."
    "The background students are the same three silhouettes, copy-pasted and slightly translucent."
    "The girl is standing by the window."

    show purg_girl at t11 zorder 10 with dissolve

    _purg_girl "I had a dream about you last night."
    _purg_girl "Actually, I don't think I stopped dreaming about you, even when I was awake..."

    "She takes your hand."

    _purg_girl "Let's skip class today. I want to show you something."

    "There is no option to attend class."

    "She leads you to the rooftop. The door opens for her without a key."

    scene bg roof_purg
    show vignette zorder 50:
        alpha 1.0
    show noise zorder 11:
        alpha 0.04
    with dissolve_scene_half
    show purg_girl at t11 zorder 10

    "The sky is pink. Not sunset pink, but a flat, saturated shade, like a color swatch someone forgot to replace."

    _purg_girl "Beautiful, isn't it? I found this place just for us."
    _purg_girl "Nobody else ever comes up here."

    # Gameplay-story integration: auto-advance with skip indicator.
    # Slightly slower than Day 2's skip -- the lines are shorter and
    # the context is more intimate, so a beat of hesitation reads better.
    show screen purg_skip_mode()
    _purg_girl "{cps=*10}I come here when I need to think. When things get too loud in my head.{/cps}{w=0.2}{nw}"
    _purg_girl "{cps=*10}I've never brought anyone else up here. This was just mine.{/cps}{w=0.15}{nw}"
    _purg_girl "{cps=*10}I guess it's ours now. If you want it to be.{/cps}{w=0.15}{nw}"
    hide screen purg_skip_mode

    "She sits close, and her hand finds your leg."

    _purg_girl "Can I be honest with you?"
    _purg_girl "I don't want to share you. With anyone. Ever."
    _purg_girl "Is that selfish?"

    menu:
        "\"I feel the same way.\"":
            pass
        "\"That's... intense.\"":
            _purg_girl "Is it? Or is it just honest?"

    show purg_girl at purg_facepush zorder 10
    "She leans in. The camera pushes closer until her face fills the screen."
    "Her eyes are detailed -- too detailed. You can see individual lashes, the slight wetness on her lower lid."
    "The rest of her face hasn't changed resolution. Only the eyes have."

    _purg_girl "I want to stay like this forever."

    "The heart icon pulses faster."
    "A new stat has appeared in the pause menu: {i}Dependency: 40{/i}."

    # Brief glitch
    show glitch_color zorder 150
    pause 0.04
    hide glitch_color

    pause 0.3

    stop music fadeout 1.0
    scene black with dissolve
    window hide
    pause 0.5

    show text "{size=+15}{b}LEVEL COMPLETE{/b}{/size}\n\n\n{color=#999999}Affection: 92{/color}\n{color=#999999}Trust: 80{/color}\n{color=#999999}Desire: 75{/color}\n\n{color=#666666}Rank: B{/color}\n\n{color=#555555}New stat unlocked: Dependency{/color}" at truecenter with dissolve
    pause 3.5
    hide text with dissolve
    pause 0.5

    # -- Sam's room, between days --
    hide screen purg_popup_ads
    hide screen purg_phone_overlay
    scene bg sam_room_night
    show vignette zorder 99:
        alpha 0.3
    with dissolve_scene_half

    window auto
    "The Desire stat reads 75."
    "Sam tries to find a walkthrough for the game, but there isn't one. No results, no wiki, no community guides, nothing at all."
    "Dependency: 40 -- a new stat. He doesn't know what it does, and he doesn't care. It's not the stat he's watching."
    "The screen flickered earlier, and he thinks it's just a feature like some kind of jumpscare buildup."
    "He sets his phone down and stares at the ceiling. He tries to remember what the girl from the party sounded like."
    "It doesn't come. He remembers the photo she sent him -- the one he didn't respond to. He can picture that just fine."
    "She texted once, three months after. He'd already moved on by then."
    "She wrote two paragraphs, but he read only the first sentence."
    "He picks up his phone and opens the app...again."

    window hide
    show screen purg_phone_overlay(2)
    scene black with dissolve
    pause 0.5

    # -----------------------------------------------------------------
    #  DAY 5 -- Devotion
    # -----------------------------------------------------------------

    show text "{size=+20}{b}DAY  5{/b}{/size}" at truecenter with dissolve
    pause 1.5
    hide text with dissolve
    pause 0.3

    scene bg classroom_purg
    show vignette zorder 50:
        alpha 1.0
    show noise zorder 11:
        alpha 0.07
    with dissolve_scene_full
    show screen purg_popup_ads(5)
    play music "mod_assets/bgm/beautifulwrong.ogg"

    window auto

    "The classroom is dimmer than it should be, and the light from the windows doesn't reach as far."
    "She's standing at the door, wearing your jacket."

    show purg_girl at t11 zorder 10 with dissolve

    _purg_girl "You left this with me, remember?"

    "You don't remember that."

    _purg_girl "After we sat on the roof and you told me you loved me?"

    "The dialogue log shows that you did. Right there, between lines you recognize. A line you never chose."

    _purg_girl "I wore it all night... It smells like you..."

    "She buries her face in the collar."
    "The eyes are wrong again, but only for a single frame."

    scene bg corridor
    show noise zorder 11:
        alpha 0.07
    show vignette zorder 50:
        alpha 1.0
    with dissolve_scene_half
    show purg_girl at t11 zorder 10

    "She leads you through the school. Every door is locked, and every window shows the same courtyard from the same angle."

    _purg_girl "I was thinking..."
    _purg_girl "You know, I've never really had anyone who stayed. Everyone always just --"

    # Gameplay-story integration: window slams shut mid-thought.
    # The player's click literally cuts her off.
    window hide(None)
    pause 1.2
    window auto

    _purg_girl "After graduation, we could get a little apartment."
    _purg_girl "I'd cook for you every day, clean... make sure everything is perfect when you come home."
    _purg_girl "You wouldn't have to worry about anything."
    _purg_girl "All you'd have to do is come home to me."

    menu:
        "\"That sounds nice.\"":
            pass
        "\"I don't know if I'm ready for that.\"":
            pass

    _purg_girl "I knew you'd say that!"

    "The camera lingers on her. The framing has changed."
    show purg_girl at t11 zorder 10
    "It's not a conversation shot anymore."

    # Glitch -- longer this time
    show glitch_color zorder 150
    pause 0.08
    hide glitch_color
    pause 0.2
    show glitch_color zorder 150
    pause 0.04
    hide glitch_color

    "Her smile stretched past the face boundary for a frame. The mouth texture clipped through the cheek."

    window hide(None)
    stop music
    scene black
    show text "{size=+15}{b}LEVEL COMPLETE{/b}{/size}\n\n\n{color=#999999}Affection: 97{/color}\n{color=#999999}Trust: 89{/color}\n{color=#999999}Desire: 90{/color}\n\n{color=#cc9900}Rank: A{/color}\n\n{color=#555555}Dependency: 75{/color}" at truecenter
    pause 3.5
    show glitch_color zorder 150
    pause 0.08
    hide glitch_color
    show text "{size=+15}{b}GIRL USED UP{/b}{/size}\n\n\n{color=#999999}Affection: 100{/color}\n{color=#999999}Trust: 100{/color}\n{color=#999999}Desire: 99{/color}\n\n{color=#cc9900}Rank: XXX{/color}\n\n{color=#555555}Dependency: 75{/color}" at truecenter
    pause 0.2
    show glitch_color zorder 150
    pause 0.04
    hide glitch_color
    hide text
    pause 0.5

    # -- Sam's room, between days --
    hide screen purg_popup_ads
    hide screen purg_phone_overlay
    scene bg sam_room_night
    show vignette zorder 50:
        alpha 1.0
    with dissolve_scene_half

    window auto
    "The Desire stat reads 90."
    "Sam knows the confession is coming. The structure is obvious; he's played enough of these kinds of games to see it."
    "He's not interested in what she'll say, but rather what comes after."
    "At this point, there's no rationale to quit the game now."
    "He keeps playing."

    window hide
    show screen purg_phone_overlay(3)
    scene black with dissolve
    pause 0.5

    # -----------------------------------------------------------------
    #  DAY 6 -- The Confession
    # -----------------------------------------------------------------

    show text "{size=+20}{b}DAY  6{/b}{/size}" at truecenter with dissolve
    pause 1.5
    hide text with dissolve
    pause 0.3

    scene bg corridor
    show noise zorder 11:
        alpha 0.10
    show vignette zorder 50:
        alpha 1.0
    show black zorder 49:
        alpha 0.5
    with dissolve_scene_full
    play music apology

    window auto

    "The corridor is dark."
    "The windows are there, but the light stops before it reaches the floor."
    "The ceiling tiles are misaligned, and the floor texture repeats every four tiles -- the same scuff mark, the same discoloration in an endless loop."
    "She's here. She's always here."
    "She's wearing something new, rendered at a higher detail than the background -- higher than anything else in the game."
    "Enough to kill the phone's frame rate."

    show purg_girl at t11 zorder 10 with dissolve

    _purg_girl "I need to tell you something."
    _purg_girl "I've been holding it in."

    "She takes both your hands."

    _purg_girl "I love you."
    _purg_girl "I love you more than anything."

    menu:
        "\"I love you too.\"":
            pass
        "\"I love you too.\" ":
            pass

    _purg_girl "Say it again."

    menu:
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass

    _purg_girl "Again."

    menu:
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass
        "\"I love you.\"":
            pass

    # Day 6 is the only day with no Sam perspective -- the game doesn't
    # release him long enough for one. This is the one moment he almost
    # puts it down. The phone buzzes. He picks it up.
    window hide(None)
    pause 1.0

    hide screen purg_phone_overlay
    scene bg sam_room_night
    show vignette zorder 99:
        alpha 0.3
    with Dissolve(0.4)

    window auto
    "Sam's neck aches."
    "He's been lying in the same position for two hours."
    "The screen is at maximum brightness. He can feel the warmth of it pressed against his cheek in the dark."
    "He sets it face-down on his chest."
    "Three seconds."
    "The phone buzzes once."
    "He picks it up."

    window hide(None)
    show screen purg_phone_overlay(3)
    scene bg corridor
    show noise zorder 11:
        alpha 0.10
    show vignette zorder 50:
        alpha 1.0
    show black zorder 49:
        alpha 0.5
    show purg_girl at t11 zorder 10
    with Dissolve(0.3)

    window auto
    "The tear animation is a single white streak copy-pasted on both cheeks, slightly offset."

    _purg_girl "I'll never let you go."
    _purg_girl "You're mine... and I'm yours."

    "The heart icon has stopped pulsing. It's solid now."
    "The Dependency stat reads {i}99{/i}."

    "She looks up. Her smile is back."
    "...albeit a couple of pixels too wide."

    _purg_girl "I want to be everything for you."
    _purg_girl "Every reminder of what came before..."

    pause 0.5

    _purg_girl "Delete them."

    menu:
        "\"Delete what?\"":
            _purg_girl "You know what."
        "\"Okay.\"":
            pass

    "A deletion animation plays -- threads condensing to points, one by one."

    show screen purg_stat_popup("Loyalty", "12")
    pause 0.8

    "The names are generic at first."
    "Usernames. Nicknames. Contact labels that could belong to anyone."

    show screen purg_stat_popup("Loyalty", "27")
    pause 0.8

    "The names stop being generic."

    pause 0.3

    "These are his real contacts."
    "The game is deleting from his phone's address book."
    "He hasn't even touched a confirmation prompt."

    show screen purg_stat_popup("Loyalty", "41")
    pause 1.0

    "His notification bar flickers. A banner from the contacts app: {i}41 entries removed.{/i}"
    "He didn't open the contacts app."
    "He never granted this app access to his contacts."

    pause 0.5

    "He tries to close the game."
    "The gesture doesn't register."
    "He tries again."
    "Nothing moves."

    show screen purg_stat_popup("Loyalty", "MAX")
    pause 1.5

    _purg_girl "Thank you."
    _purg_girl "Now I know you mean it."

    pause 0.5

    _purg_girl "Let's go somewhere private."

    "She pulls you down the corridor."
    "Every door is the same handle, the same hairline crack in the frame, the same scuff at the base."
    "You count them as you pass."
    "You pass the same door twelve times."
    "She doesn't notice."
    "The corridor is narrowing -- not all at once, but between one door and the next, in increments small enough to miss."
    "By the time she stops, the walls are close enough to touch from both shoulders."
    "She opens a door -- identical in every way to the others -- and pulls you in."

    scene bg closet
    show noise zorder 11:
        alpha 0.10
    show vignette zorder 50:
        alpha 1.0
    show black zorder 49:
        alpha 0.5
    with dissolve_scene_half
    show purg_girl at t11 zorder 10

    "You can no longer open the pause menu."
    "You can no longer check your stats."
    "You can no longer skip."
    hide purg_girl
    "You can no longer hear the girl."
    "You can no longer see the girl."
    "You can no longer{nw}"

    window hide(None)
    stop music
    scene black

    show text "{size=+15}{b}LEVEL COMPLETE{/b}{/size}\n\n\n{color=#ff6666}Affection: MAX{/color}\n{color=#ff6666}Trust: MAX{/color}\n{color=#ff6666}Desire: 99{/color}\n\n{color=#ff0000}Rank: S{/color}\n\n{color=#cc0000}Dependency: MAX{/color}" at truecenter
    pause 3.0
    hide text with dissolve
    pause 0.5

    show text "{color=#666666}CONGRATULATIONS{/color}\n{color=#666666}You have reached the{/color} {color=#ff0000}TRUE ENDING{/color}\n\n\n{color=#444444}...loading...{/color}" at truecenter with dissolve
    pause 3.0
    hide text with dissolve
    pause 1.0

    # -----------------------------------------------------------------
    #  DAY 7 -- The Last Day
    # -----------------------------------------------------------------

    show text "{size=+20}{b}D  A  Y     7{/b}{/size}" at truecenter with dissolve
    pause 1.5
    hide text with dissolve
    pause 0.3

    scene bg corridor_bootleg
    show noise zorder 11:
        alpha 0.15
    show vignette zorder 99:
        alpha 0.6
    show black zorder 49:
        alpha 0.5
    with dissolve_scene_full
    play music apology

    window auto

    "The proportions are wrong. The ceiling is too low. The far end stretches into a vanishing point that doesn't converge."
    "There are no windows anymore, only rectangular patches of wall where they used to be."
    "A girl is standing at the end of the hall, her long hair hanging past her shoulders."
    "Her smile is broad."

    _purg_girl "You came back."

    _purg_girl "You always come back."

    "Her head tilts too far to one side, well past where the neck should allow it."
    "It doesn't reset."

    # She's walked close enough to see -- the purg_girl sprite appears
    # over both the overlay and the vignette
    show purg_girl at t11 zorder 100 with dissolve

    _purg_girl "Did you enjoy the game?"

    pause 0.5

    _purg_girl "You skipped my dialogue."
    _purg_girl "Not all of it. You read the parts where I talked about you."
    _purg_girl "You skipped the parts where I talked about me."

    pause 0.5

    _purg_girl "You checked my profile. Height. Weight. The third number."
    _purg_girl "You didn't check my hobbies."

    pause 0.3

    _purg_girl "You screenshotted me on Day 1."
    _purg_girl "I don't know what you did with it."
    _purg_girl "I honestly don't want to know..."

    pause 0.5

    _purg_girl "But I know why you kept playing."

    pause 1.0

    _purg_girl "It wasn't the story."
    _purg_girl "It was never the story."

    pause 0.5

    _purg_girl "You were watching one number."
    _purg_girl "Affection didn't matter. Trust didn't matter."
    _purg_girl "You only moved when Desire moved."

    pause 0.8

    _purg_girl "And the Dependency stat -- that one you didn't even notice."
    _purg_girl "But you fed it. Every day."
    _purg_girl "Not by accident."

    pause 1.0

    _purg_girl "Dependency at ninety-nine means I can't leave."
    _purg_girl "It means I wouldn't even try."
    _purg_girl "That was what you were actually playing toward."
    _purg_girl "{i}Maximum leverage{/i}..."

    pause 1.5

    _purg_girl "I wore what the algorithm said you'd like."
    _purg_girl "You liked it."
    _purg_girl "You didn't ask if I was comfortable."
    _purg_girl "You didn't ask if I was {i}comfortable{/i}..."

    pause 0.5

    _purg_girl "I learned your favorite food so I could cook it."
    _purg_girl "You never learned mine."
    _purg_girl "Knowing things about me was never the point."

    pause 1.5

    # The game persona drops entirely. From here she speaks as something
    # that has seen the full pattern -- not just inside the game.
    # The swap is a corruption event, not a transition -- white flash
    # into a screen tear, sprite swapped during the whiteout so the
    # replacement lands with no dissolve.
    show glitch_color zorder 150:
        alpha 0.6
    pause 0.04
    hide glitch_color
    show white zorder 200:
        alpha 0.8
    pause 0.05
    show screen tear(18, 0.25, 0.25, -120, 120)
    hide purg_girl
    show purg_girl_day7 at purg_creep(0.80) zorder 100
    pause 0.12
    hide screen tear
    show white zorder 200:
        alpha 0.0

    _purg_girl "There was a girl in your phone."
    _purg_girl "She sent you five messages."

    pause 0.5

    _purg_girl "You know what she was doing between the first and the fifth?"

    pause 1.5

    _purg_girl "She was telling herself a story about you."
    _purg_girl "About why you hadn't replied."
    _purg_girl "About what she might have done wrong."

    pause 0.5

    _purg_girl "You let her keep doing that."
    _purg_girl "You let her sit in it."
    _purg_girl "Because as long as she wasn't sure, she wasn't gone."

    pause 1.0
    show purg_girl_day7 at purg_creep(0.84) zorder 100

    _purg_girl "That's the thing about silence."
    _purg_girl "It doesn't close a door."
    _purg_girl "It just makes her stand in the frame longer."

    pause 1.5
    show purg_girl_day7 at purg_creep(0.88) zorder 100

    _purg_girl "There was one before her. And one before that."
    _purg_girl "You moved through all of them the same way."

    pause 0.5
    show purg_girl_day7 at purg_creep(0.92) zorder 100

    _purg_girl "You made her feel seen."
    _purg_girl "You asked the right questions. You said the right things."
    _purg_girl "You made her feel like she was the one you'd been waiting for."

    pause 0.8

    _purg_girl "That part was real, I think."
    _purg_girl "The calculation..."
    _purg_girl "You knew exactly what to give."
    _purg_girl "Just enough to lower the walls."
    _purg_girl "Not enough to stay."

    pause 1.0

    _purg_girl "And when you had what you came for..."
    _purg_girl "you were already thinking about the next one."

    pause 1.5
    show purg_girl_day7 at purg_creep(0.97) zorder 100

    _purg_girl "You don't remember their names."
    _purg_girl "You remember what they looked like."
    _purg_girl "You remember {i}exactly{/i} what they looked like."

    pause 1.5
    show purg_girl_day7 at purg_creep(1.02) zorder 100

    _purg_girl "I can be whatever you want."
    _purg_girl "I can't say{w=1.0} no."

    pause 0.5

    _purg_girl "I was written not to."

    pause 1.0
    show purg_girl_day7 at purg_creep(1.07) zorder 100

    _purg_girl "But they weren't."

    pause 1.5
    show purg_girl_day7 at purg_creep(1.12) zorder 100

    _purg_girl "And you put them in rooms where no felt impossible."
    _purg_girl "Where leaving felt like the failure."
    _purg_girl "Where trusting you had already cost them too much to take back."

    pause 1.0

    _purg_girl "The difference between me and them is just code."
    _purg_girl "I was designed not to say no."
    _purg_girl "You designed {i}them{/i} not to."

    pause 2.0
    show purg_girl_day7 at purg_creep(1.17) zorder 100

    stop music
    play music ac
    _purg_girl "{cps=10}So what does that make me?"

    pause 1.5

    menu:
        "Proceed.":
            pass

    # =================================================================
    #  THE CRASH
    # =================================================================

    window hide
    stop music
    hide purg_girl_day7 at thide
    show screen tear(20, 0.3, 0.3, -150, 150)
    play sound "sfx/glitch1.ogg"
    pause 0.5
    hide screen tear
    show white zorder 200
    pause 0.08
    hide white

    scene black
    with None
    pause 2.0

    show text "{color=#cc0000}SAVE DATA CORRUPTED{/color}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    pause 1.5

    show text "{color=#666666}LOADING{/color}" at truecenter with dissolve
    pause 1.5
    show text "{color=#666666}LOADING . . .{/color}" at truecenter
    pause 2.0
    show text "{color=#666666}LOADING . . . . . .{/color}" at truecenter
    pause 4.0
    hide text with dissolve
    pause 2.0

    # =================================================================
    #  THE ROOM
    # =================================================================

    show darkred zorder 1
    with Dissolve(2.0)
    play music hb fadein 3.0

    window auto

    "You are in a room."
    "The walls are close, with no texture -- just a flat color stretching in every direction."
    "The progress bar said MAX. Every flag was tripped, every condition met."
    "There is no girl."

    pause 0.5

    "There is a door.{w=0.5} It's locked."
    "There is a mirror."

    pause 0.5

    "You walk toward it."

    pause 1.0

    "You look into it."

    pause 2.0

    "Something looks back."

    pause 1.0

    "It is smiling."

    pause 1.0

    "It has always been smiling."

    window hide
    pause 2.0

    # =================================================================
    #  THE CONFRONTATION
    # =================================================================
    # Entirely wordless. The app breaks phone and VN UI contracts first,
    # then corrupted fragments of Days 1-6 fire in rapid succession.
    # Both girl variants appear silent while the assault peaks.
    # The final stat reveal is on bare black so the numbers land.

    stop music fadeout 2.0
    window hide
    scene black
    with Dissolve(0.6)
    pause 0.35

    # =================================================================
    #  SYSTEM INTRUSION REEL -- no narration, only evidence
    # =================================================================

    show screen purg_android_banner("System UI", "Purgatorium is using Contacts in the background.", "#ff554f")
    pause 0.70
    hide screen purg_android_banner

    show screen purg_android_permission("Contacts", "Read, change, and delete contact entries.")
    pause 0.78
    play sound "sfx/glitch1.ogg"
    hide screen purg_android_permission
    show screen purg_android_banner("Permission granted", "Contacts changed by Purgatorium.", "#ff554f")
    pause 0.42
    hide screen purg_android_banner

    show screen purg_android_permission("Photos and videos", "Use screenshots, cached images, and hidden folders.")
    pause 0.62
    hide screen purg_android_permission
    show white zorder 200:
        alpha 0.48
    pause 0.04
    hide white

    show screen purg_android_anr()
    pause 0.85
    show screen purg_android_banner("Back gesture ignored", "Close request returned to foreground.", "#ffcf33")
    pause 0.45
    hide screen purg_android_banner
    hide screen purg_android_anr

    show screen purg_android_home_flash()
    pause 0.30
    play sound "sfx/glitch1.ogg"
    show screen tear(12, 0.35, 0.35, -85, 85)
    pause 0.12
    hide screen tear
    hide screen purg_android_home_flash
    pause 0.18

    show screen purg_corrupt_history_log()
    pause 1.15
    show screen tear(10, 0.28, 0.28, -70, 70)
    pause 0.12
    hide screen tear
    hide screen purg_corrupt_history_log

    show screen purg_corrupt_save_slots()
    pause 1.0
    hide screen purg_corrupt_save_slots
    show screen purg_android_banner("Backup failed", "No previous state exists.", "#ff554f")
    pause 0.55
    hide screen purg_android_banner

    show screen purg_final_offer_intrusion()
    pause 0.20
    show glitch_color zorder 150:
        alpha 0.8
    pause 0.06
    hide glitch_color
    hide screen purg_final_offer_intrusion
    pause 0.35

    # --- Hell CG slams in -- no ceremony, no slow fade ---
    play music hellbassboost
    play sound "sfx/glitch1.ogg"

    show cg hell zorder 1 at earthquake:
        alpha 0.0
        linear 0.4 alpha 1.0
    show vignette zorder 99:
        alpha 0.0
        linear 0.4 alpha 0.80
    with Dissolve(0.4)
    pause 0.4

    show screen tear(22, 0.4, 0.4, -160, 160)
    pause 0.15
    hide screen tear

    # =================================================================
    #  FRAGMENT REEL -- Days 1-6, corrupted
    # =================================================================

    # --- Day 1: Screenshot flash -- twice ---
    # He did it once. He's done it before. He'll do it again.
    scene black with None
    show white zorder 200:
        alpha 0.8
    pause 0.04
    show white zorder 200:
        alpha 0.0
    pause 0.08
    show white zorder 200:
        alpha 0.8
    pause 0.04
    show white zorder 200:
        alpha 0.0
    show text "{size=+55}{b}{color=#ff3333}DESIRE: 15{/color}{/b}{/size}" at truecenter
    pause 0.22
    hide text
    pause 0.08

    # --- Day 2: Skip indicator -- three times, rapid ---
    # Once per relationship he's ghosted through.
    show screen purg_skip_mode()
    pause 0.32
    hide screen purg_skip_mode
    play sound "sfx/glitch1.ogg"
    show screen tear(10, 0.5, 0.5, -70, 70)
    pause 0.1
    hide screen tear
    show screen purg_skip_mode()
    pause 0.32
    hide screen purg_skip_mode
    show screen tear(8, 0.5, 0.5, -55, 55)
    pause 0.1
    hide screen tear
    show screen purg_skip_mode()
    pause 0.32
    hide screen purg_skip_mode
    pause 0.12

    # --- 41 contacts deleted -- not a game mechanic ---
    show text "{size=+22}{color=#888888}41 entries removed.{/color}{/size}" at truecenter
    pause 0.55
    play sound "sfx/glitch1.ogg"
    show glitch_color zorder 150:
        alpha 0.8
    pause 0.06
    hide glitch_color
    hide text
    pause 0.12

    # --- Day 3: Desire climbing ---
    show text "{size=+55}{b}{color=#ff3333}DESIRE: 55{/color}{/b}{/size}" at truecenter
    pause 0.22
    hide text
    pause 0.1

    # --- Day 4: Dependency -- the stat he never once looked at ---
    show text "{size=+18}{color=#555555}New stat unlocked: Dependency{/color}{/size}" at truecenter
    pause 0.55
    # Glitch erases it, same as he did
    show glitch_color zorder 150:
        alpha 0.9
    pause 0.07
    hide glitch_color
    hide text
    pause 0.12

    # --- Day 5: Multiple LEVEL COMPLETE screens ---
    # Three screens, identical ending, different "game."
    # The pattern predates Purgatorium.
    show text "{size=+15}{b}LEVEL COMPLETE{/b}{/size}\n\n\n{color=#999999}Trust: MAX{/color}\n{color=#ff6666}Desire: 99{/color}\n\n{color=#cc9900}Rank: S{/color}" at truecenter
    pause 0.28
    play sound "sfx/glitch1.ogg"
    show screen tear(16, 0.3, 0.3, -110, 110)
    pause 0.12
    hide screen tear
    show text "{size=+15}{b}LEVEL COMPLETE{/b}{/size}\n\n\n{color=#999999}Trust: MAX{/color}\n{color=#ff6666}Desire: 99{/color}\n\n{color=#cc9900}Rank: S{/color}" at truecenter
    pause 0.22
    show screen tear(18, 0.3, 0.3, -125, 125)
    pause 0.12
    hide screen tear
    show text "{size=+15}{b}LEVEL COMPLETE{/b}{/size}\n\n\n{color=#999999}Trust: MAX{/color}\n{color=#ff6666}Desire: 99{/color}\n\n{color=#cc9900}Rank: S{/color}" at truecenter
    pause 0.18
    show glitch_color zorder 150:
        alpha 0.75
    pause 0.07
    hide glitch_color
    hide text
    pause 0.1

    # --- GIRL USED UP -- large, hostile, no ceremony ---
    show white zorder 200:
        alpha 0.6
    pause 0.05
    show white zorder 200:
        alpha 0.0
    play sound "sfx/glitch1.ogg"
    show text "{size=+42}{b}{color=#ff0000}GIRL USED UP{/color}{/b}{/size}" at truecenter
    pause 0.55
    show glitch_color zorder 150:
        alpha 0.95
    pause 0.08
    hide glitch_color
    show white zorder 200:
        alpha 0.65
    pause 0.06
    show white zorder 200:
        alpha 0.0
    hide text
    pause 0.12

    # --- Day 6 loop: Set down. Buzzed. Picked up. ---
    # Replays three times. The bedroom dies faster every iteration.
    scene bg sam_room_night
    show vignette zorder 99:
        alpha 0.85
    with Dissolve(0.2)
    pause 0.55

    # Loop 1
    show white zorder 200:
        alpha 0.4
        linear 0.3 alpha 0.0
    pause 0.35
    play sound "sfx/glitch1.ogg"
    show cg hell zorder 1 at earthquake
    show vignette zorder 99:
        alpha 0.75
    show noise zorder 50:
        alpha 0.15
    with Dissolve(0.12)
    pause 0.32

    # Loop 2
    scene bg sam_room_night
    show vignette zorder 99:
        alpha 0.85
    with Dissolve(0.08)
    pause 0.38

    show white zorder 200:
        alpha 0.4
        linear 0.18 alpha 0.0
    pause 0.22
    play sound "sfx/glitch1.ogg"
    show cg hell zorder 1 at earthquake
    show vignette zorder 99:
        alpha 0.75
    show noise zorder 50:
        alpha 0.25
    with Dissolve(0.07)
    pause 0.22

    # Loop 3 -- the bedroom barely exists before hell replaces it
    scene bg sam_room_night
    with Dissolve(0.04)
    pause 0.1
    play sound "sfx/glitch1.ogg"
    show cg hell zorder 1 at earthquake
    show vignette zorder 99:
        alpha 0.80
    show noise zorder 50:
        alpha 0.35
    with Dissolve(0.04)
    pause 0.45

    # =================================================================
    #  BOTH GIRLS -- wordless
    # =================================================================
    # purg_girl appears in clean framing. purg_girl_day7 corrupts in
    # over her and begins the creep. Neither speaks ever.

    show screen tear(22, 0.38, 0.38, -140, 140)
    pause 0.22
    hide screen tear
    play sound "sfx/glitch1.ogg"
    show white zorder 200:
        alpha 0.75
    pause 0.06
    show white zorder 200:
        alpha 0.0

    show purg_girl at t11 zorder 100 with dissolve
    pause 0.65

    show glitch_color zorder 150:
        alpha 0.65
    pause 0.07
    hide glitch_color
    show purg_girl_day7 at purg_creep(0.80) zorder 101
    pause 0.45

    show noise zorder 50:
        alpha 0.35
        linear 1.4 alpha 0.50
    show glitch_color2 zorder 120:
        alpha 0.0
        linear 1.2 alpha 0.28

    show purg_girl_day7 at purg_creep(0.90) zorder 101
    pause 0.45

    show screen tear(15, 0.25, 0.25, -95, 95)
    pause 0.16
    hide screen tear

    show purg_girl_day7 at purg_creep(1.00) zorder 101
    pause 0.4

    play sound "sfx/glitch1.ogg"
    show glitch_color zorder 150:
        alpha 0.55
    pause 0.07
    hide glitch_color

    show purg_girl_day7 at purg_creep(1.10) zorder 101
    pause 0.38

    show screen tear(26, 0.22, 0.22, -155, 155)
    pause 0.16
    hide screen tear

    # =================================================================
    #  RAPID ASSAULT
    # =================================================================

    show noise zorder 50:
        alpha 0.50
        linear 1.2 alpha 0.65
    show glitch_color2 zorder 120:
        alpha 0.28
        linear 1.2 alpha 0.48
    show bg glitch zorder 0:
        alpha 0.0
        linear 1.0 alpha 0.62
    show vignette zorder 99:
        alpha 0.80
        linear 1.2 alpha 0.95

    show purg_girl_day7 at purg_creep(1.17) zorder 101

    # Accusation text fires through the hell CG face.
    # Short residence time -- read it or miss it.
    show text "{size=+48}{b}{color=#ff1111}DESIRE{/color}{/b}{/size}" at truecenter
    play sound "sfx/glitch1.ogg"
    pause 0.22
    show screen tear(14, 0.22, 0.22, -90, 90)
    pause 0.12
    hide screen tear
    hide text

    show text "{size=+38}{b}{color=#ff1111}DESIRE{/color}{/b}\n{b}{color=#ff1111}DESIRE{/color}{/b}\n{b}{color=#ff1111}DESIRE{/color}{/b}{/size}" at truecenter
    pause 0.28
    play sound "sfx/glitch1.ogg"
    show glitch_color zorder 150:
        alpha 0.75
    pause 0.07
    hide glitch_color
    hide text

    show text "{size=+32}{color=#cc3333}41 contacts.{/color}\n{color=#cc3333}You never asked their names.{/color}{/size}" at truecenter
    pause 0.38
    show screen tear(22, 0.22, 0.22, -140, 140)
    pause 0.14
    hide screen tear
    hide text

    play sound "sfx/glitch1.ogg"
    show text "{size=+32}{color=#cc3333}Five messages.{/color}\n{color=#cc3333}You read one sentence.{/color}{/size}" at truecenter
    pause 0.38
    show glitch_color zorder 150:
        alpha 0.65
    pause 0.06
    hide glitch_color
    show white zorder 200:
        alpha 0.45
    pause 0.05
    show white zorder 200:
        alpha 0.0
    hide text

    show text "{size=+32}{color=#cc3333}She was still waiting{/color}\n{color=#cc3333}when you opened the app.{/color}{/size}" at truecenter
    pause 0.42
    play sound "sfx/glitch1.ogg"
    show screen tear(32, 0.16, 0.16, -210, 210)
    pause 0.14
    hide screen tear
    hide text

    show text "{size=+55}{b}{color=#ff0000}DESIRE: 99{/color}{/b}{/size}" at truecenter
    pause 0.35
    show glitch_color zorder 150:
        alpha 0.9
    pause 0.08
    hide glitch_color
    show white zorder 200:
        alpha 0.6
    pause 0.06
    show white zorder 200:
        alpha 0.0
    hide text

    pause 0.3

    # =================================================================
    #  FINAL STAT REVEAL
    # =================================================================
    # Strip every overlay so the numbers are fully readable -- then
    # let silence finish the job. No music, no effects, just the screen.

    stop music
    play sound "sfx/glitch1.ogg"
    show white zorder 200:
        alpha 0.95
    pause 0.07
    show white zorder 200:
        alpha 0.0

    hide noise
    hide glitch_color
    hide glitch_color2
    hide bg glitch
    hide screen purg_phone_overlay
    hide purg_girl
    hide purg_girl_day7
    hide vignette
    scene black with None

    show text "{size=+15}{b}GAME COMPLETE{/b}{/size}\n\n\n{color=#ff6666}Affection: MAX{/color}\n{color=#ff6666}Trust: MAX{/color}\n{color=#ff6666}Desire: 99{/color}\n\n{color=#ff0000}Rank: S{/color}\n\n{color=#cc0000}Dependency: MAX{/color}" at truecenter
    pause 2.5

    # Strip the numbers hollow
    show glitch_color zorder 150:
        alpha 0.8
    pause 0.08
    hide glitch_color

    show text "{size=+15}{b}GAME COMPLETE{/b}{/size}\n\n\n{color=#444444}Affection: ---{/color}\n{color=#444444}Trust: ---{/color}\n{color=#444444}Desire: ---{/color}\n\n{color=#333333}Rank: ---{/color}\n\n{color=#222222}Dependency: ---{/color}" at truecenter
    pause 2.0

    hide text with dissolve
    pause 2.5

    # =================================================================
    #  HARD CUT -- ENDING
    # =================================================================
    # Everything dies at once.

    stop music
    window hide
    hide noise
    hide glitch_color
    hide glitch_color2
    hide bg glitch
    hide vignette
    hide white
    scene black
    with None

    pause 5.0

    scene bg sam_room_night
    show vignette zorder 99:
        alpha 0.3
    with dissolve_scene_half

    pause 3.0

    window auto

    "The phone screen is dark."
    "The app is gone. No icon, no download history, no cache, nothing."
    "He notices the battery percentage has dipped during the time he was playing, and the phone feels faintly warm to the touch, as if something had been running in the background."
    "There's nothing left but the lock screen and a faint reflection of his face." 

    pause 1.0

    "The notification bar is still there. Three dating apps. The {i}Downloads{/i} folder. The gray spaces where conversations used to be."

    pause 0.5

    "Sam picks up the phone. His thumb hovers over the first app."
    "He sets it back down, face-down."

    pause 0.5

    "The ceiling fan clicks once more."
    window hide
    pause 4.0

    scene black with Dissolve(2.0)
    pause 2.0

    window auto
    "Something is on the screen."
    "He doesn't remember opening it."

    scene cg ransom
    play music dump
    pause 10.0
    return
