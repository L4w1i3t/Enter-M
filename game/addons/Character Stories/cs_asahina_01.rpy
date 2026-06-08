# Asahina Character Story 01
# Inspired by the Lacey Games horror series -- a 2000s Flash site that presents
# itself as a flash game portal, but something is wrong.
# This story is a point-and-click adventure set inside a Windows XP / IE6 browser.
#
# Reference guardrails:
# - Use the Lacey Games structure: cute lost-Flash nostalgia as the mask, then
#   UI wrongness, player complicity, and a buried personal horror underneath.
# - Do not copy Lacey characters, scenarios, or specific reveals. Hina's World
#   should center Asahina's public cheerfulness, body/food scrutiny, athletic
#   pressure, and the way a "fun" site can quietly turn her into a performance.

default hinas_world_page = "home"
default hinas_world_corruption = 0
default hinas_world_seen_outfitter = False
default hinas_world_seen_chatting = False
default hinas_world_seen_quiz = False
default hinas_world_seen_rating = False

init python:
    HINAS_WORLD_NAV = [
        ("Home", "home"),
        ("Games", "games"),
        ("Gallery", "gallery"),
        ("About", "about"),
    ]

    HINAS_WORLD_ADDRESSES = {
        "home": "http://www.hinasworld.net/home.html",
        "games": "http://www.hinasworld.net/games.html",
        "gallery": "http://www.hinasworld.net/gallery.html",
        "about": "http://www.hinasworld.net/about.html",
    }

    HINAS_WORLD_GAMES = [
        ("outfitter", "#e0559a", "#c20060", "Hina's\nOutfitter", "Dress Hina for school, practice, and tonight's plans."),
        ("chatting", "#aa55e0", "#7700cc", "Hina's\nChatting", "Chat with cute friends from all over the web."),
        ("quiz", "#55aadd", "#0066aa", "Hina's\nQuiz Corner", "Find out which Hina mood matches you best."),
        ("rating", "#e08844", "#bb5500", "Hina's\nRating Game", "Score today's looks, snacks, and crushes."),
    ]

# =============================================================================
#  SCREEN: cs_asahina_window98 -- Internet Explorer 6 browser window with Flash site
#  Resolution target: 1280x720
# =============================================================================

screen cs_asahina_window98(page="home", corruption=0, seen_outfitter=False, seen_chatting=False, seen_quiz=False, seen_rating=False):
    modal True
    key "game_menu" action Return("exit")
    key "K_ESCAPE" action Return("exit")

    $ _hw_address = HINAS_WORLD_ADDRESSES.get(page, HINAS_WORLD_ADDRESSES["home"])

    # Windows XP default blue-gray desktop
    add Solid("#3a6ea5")

    # --- Drop shadow ---
    frame:
        xalign 0.5
        yalign 0.5
        xoffset 4
        yoffset 5
        xsize 920
        ysize 636
        padding (0, 0, 0, 0)
        background "#202020"

    # --- Main browser window ---
    frame:
        xalign 0.5
        yalign 0.5
        xsize 920
        ysize 636
        padding (0, 0, 0, 0)
        background "#d4d0c8"

        vbox:
            spacing 0
            xsize 920

            # =========================================================
            #  TITLE BAR  (height: 26px)
            #  Windows XP Luna blue gradient simulated with nested frames
            # =========================================================
            frame:
                xsize 920
                ysize 26
                padding (0, 0, 0, 0)
                background "#0a246a"

                # Thin lighter strip along the top edge (XP gradient hint)
                frame:
                    xsize 920
                    ysize 2
                    xpos 0
                    ypos 0
                    padding (0, 0, 0, 0)
                    background "#3169c6"

                # Left: IE icon + window title
                hbox:
                    xpos 4
                    ypos 15
                    yalign 0.5
                    spacing 4

                    # IE "e" logo placeholder
                    frame:
                        xysize (18, 18)
                        background "#1e4fd4"
                        padding (0, 0, 0, 0)
                        yalign 0.5
                        text "e":
                            color "#ffffff"
                            bold True
                            size 13
                            xalign 0.5
                            yalign 0.5

                    text "Hina's World - Internet Explorer":
                        color "#ffffff"
                        size 11
                        yalign 0.5

                # Right: window control buttons (Windows XP style, right-aligned)
                hbox:
                    xalign 1.0
                    xoffset -3
                    yalign 0.5
                    spacing 2

                    # Minimize
                    frame:
                        xysize (17, 15)
                        padding (0, 0, 0, 0)
                        background "#c0c0c0"
                        yalign 0.5
                        text "_":
                            color "#000000"
                            size 12
                            bold True
                            xalign 0.5
                            yalign 0.5

                    # Maximize -- drawn as a nested frame border (□ unsupported in Aller)
                    frame:
                        xysize (17, 15)
                        padding (0, 0, 0, 0)
                        background "#c0c0c0"
                        yalign 0.5
                        frame:
                            xysize (9, 8)
                            padding (0, 0, 0, 0)
                            background "#000000"
                            xalign 0.5
                            yalign 0.5
                            frame:
                                xysize (7, 6)
                                padding (0, 0, 0, 0)
                                background "#c0c0c0"
                                xalign 0.5
                                yalign 1.0

                    # Close (red)
                    frame:
                        xysize (17, 15)
                        padding (0, 0, 0, 0)
                        background "#c00000"
                        yalign 0.5
                        text "X":
                            color "#ffffff"
                            bold True
                            size 10
                            xalign 0.5
                            yalign 0.5

            # =========================================================
            #  MENU BAR  (height: 20px)
            # =========================================================
            frame:
                xsize 920
                ysize 20
                padding (6, 3, 0, 0)
                background "#d4d0c8"

                hbox:
                    yalign 0.5
                    spacing 14

                    for item in ["File", "Edit", "View", "Favorites", "Tools", "Help"]:
                        text item:
                            color "#ffffff"
                            size 11

            # Thin separator
            frame:
                xsize 920
                ysize 1
                padding (0, 0, 0, 0)
                background "#808080"

            # =========================================================
            #  TOOLBAR  (height: 30px)
            # =========================================================
            frame:
                xsize 920
                ysize 30
                padding (4, 3, 4, 3)
                background "#d4d0c8"

                hbox:
                    yalign 0.5
                    spacing 3

                    # Navigation buttons
                    for btn in ["< Back", "Fwd >", "Stop", "Refresh", "Home"]:
                        frame:
                            background "#c8c8c4"
                            padding (6, 2, 6, 2)
                            yalign 0.5
                            text btn:
                                color "#ffffff"
                                size 10

                    # Vertical separator
                    frame:
                        xysize (2, 20)
                        padding (0, 0, 0, 0)
                        background "#808080"
                        yalign 0.5

                    text "Address:":
                        color "#ffffff"
                        size 10
                        yalign 0.5

                    # Address field
                    frame:
                        xsize 486
                        ysize 20
                        padding (4, 2, 4, 2)
                        background "#ffffff"
                        yalign 0.5
                        text _hw_address:
                            color "#ffffff"
                            size 10
                            yalign 0.5

                    frame:
                        background "#c8c8c4"
                        padding (8, 2, 8, 2)
                        yalign 0.5
                        text "Go":
                            color "#ffffff"
                            size 10

            # Thin separator
            frame:
                xsize 920
                ysize 1
                padding (0, 0, 0, 0)
                background "#808080"

            # =========================================================
            #  FLASH SITE CONTENT AREA
            #  Remaining height: 636 - 26 - 20 - 1 - 30 - 1 - 1 - 19 = 538px
            # =========================================================
            frame:
                xsize 920
                ysize 538
                padding (0, 0, 0, 0)
                background "#ffcce8"

                vbox:
                    spacing 0
                    xsize 920

                    # --- Site header bar ---
                    frame:
                        xsize 920
                        ysize 68
                        padding (0, 0, 0, 0)
                        background "#c20060"

                        # Subtle top accent stripe
                        frame:
                            xsize 920
                            ysize 3
                            xpos 0
                            ypos 0
                            padding (0, 0, 0, 0)
                            background "#ff3399"

                        text "~*~ Hina's World ~*~":
                            color "#ffff99"
                            bold True
                            size 26
                            xalign 0.5
                            ypos 7

                        text "dress up  •  chatting  •  quizzes  •  makeover  •  and more!":
                            color "#ffccee"
                            size 11
                            xalign 0.5
                            ypos 47

                    # --- Site navigation bar ---
                    frame:
                        xsize 920
                        ysize 28
                        padding (0, 3, 0, 3)
                        background "#8800aa"

                        hbox:
                            xalign 0.5
                            yalign 0.5
                            spacing 4

                            for nav, nav_page in HINAS_WORLD_NAV:
                                $ _hw_nav_bg = "#ff33dd" if page == nav_page else "#dd00cc"
                                button:
                                    background _hw_nav_bg
                                    hover_background "#ff66dd"
                                    padding (10, 2, 10, 2)
                                    yalign 0.5
                                    action Return("nav_" + nav_page)
                                    text nav:
                                        color "#ffffff"
                                        bold True
                                        size 11

                    # --- Main content (left sidebar + body) ---
                    hbox:
                        spacing 0
                        xsize 920

                        # === Left Sidebar (196px) ===
                        frame:
                            xsize 196
                            ysize 442
                            padding (8, 8, 8, 8)
                            background "#ffaad4"

                            vbox:
                                spacing 8
                                xsize 180

                                # News box
                                frame:
                                    xsize 180
                                    padding (7, 6, 7, 6)
                                    background "#ffffff"
                                    vbox:
                                        spacing 4
                                        text "* News *":
                                            color "#ff0080"
                                            bold True
                                            size 12
                                        text "» New game added!\n  Hina's Chatting\n  is finally here!":
                                            color "#ffa7a7"
                                            size 11
                                        text "» Outfitter updated\n  with 20 new items!":
                                            color "#ffa7a7"
                                            size 11

                                # Friend links box
                                frame:
                                    xsize 180
                                    padding (7, 6, 7, 6)
                                    background "#ffffff"
                                    vbox:
                                        spacing 4
                                        text "* Friends *":
                                            color "#ff0080"
                                            bold True
                                            size 12
                                        for lnk in ["Emily's Corner", "Star Cute!", "Dreamy Dolls", "Pixel Hearts"]:
                                            text "» " + lnk:
                                                color "#e169ff"
                                                size 11

                                # Decorative divider
                                text "-~*~-~*~-~*~-~*~-":
                                    color "#ff3399"
                                    size 12
                                    xalign 0.5

                                # Visitor counter (classic 2000s staple)
                                frame:
                                    xsize 180
                                    padding (7, 6, 7, 6)
                                    background "#330033"
                                    vbox:
                                        spacing 2
                                        text "Visitor No.":
                                            color "#ff99dd"
                                            size 10
                                            xalign 0.5
                                        text "001,337":
                                            color "#00ff88"
                                            bold True
                                            size 14
                                            xalign 0.5

                        # Thin column separator
                        frame:
                            xsize 1
                            ysize 442
                            padding (0, 0, 0, 0)
                            background "#dd88bb"

                        # === Main Content Area (723px) ===
                        frame:
                            xsize 723
                            ysize 442
                            padding (12, 10, 12, 10)
                            background "#ffe6f4"

                            use hinas_world_page_content(page, corruption, seen_outfitter, seen_chatting, seen_quiz, seen_rating)

            # =========================================================
            #  STATUS BAR  (height: 20px)
            # =========================================================
            frame:
                xsize 920
                ysize 1
                padding (0, 0, 0, 0)
                background "#808080"

            frame:
                xsize 920
                ysize 19
                padding (4, 2, 4, 2)
                background "#d4d0c8"

                text "Done":
                    color "#ffffff"
                    size 10
                    xpos 0
                    yalign 0.5

                # Right: browser zone indicator
                text "Internet":
                    color "#ffffff"
                    size 10
                    xalign 1.0
                    xoffset -4
                    yalign 0.5


screen hinas_world_page_content(page, corruption, seen_outfitter, seen_chatting, seen_quiz, seen_rating):
    $ _hw_seen = {
        "outfitter": seen_outfitter,
        "chatting": seen_chatting,
        "quiz": seen_quiz,
        "rating": seen_rating,
    }

    vbox:
        spacing 10
        xsize 699

        if page == "home":
            frame:
                xsize 699
                padding (10, 8, 10, 8)
                background "#ffffff"
                vbox:
                    spacing 4
                    text "* Welcome to Hina's World! *":
                        color "#fc6ab3"
                        bold True
                        size 15
                    text ("The #1 destination for fun Flash games and so much more! Updated weekly~" if corruption < 2 else "The #1 destination for girls who can keep smiling. Updated when she answers."):
                        color "#ffa0a0"
                        size 11

            text ("- Featured Games -" if corruption < 2 else "- Featured Files -"):
                color "#8800aa"
                bold True
                size 13
                xalign 0.5

            hbox:
                spacing 10
                xsize 699

                for game_id, bg_light, bg_dark, title, blurb in HINAS_WORLD_GAMES:
                    use hinas_world_game_card(game_id, bg_light, bg_dark, title, blurb, _hw_seen.get(game_id, False))

            text "~*~  ~*~  ~*~  ~*~  ~*~  ~*~  ~*~  ~*~  ~*~  ~*~  ~*~":
                color "#ff3399"
                size 11
                xalign 0.5

        elif page == "games":
            frame:
                xsize 699
                padding (10, 8, 10, 8)
                background "#ffffff"
                vbox:
                    spacing 4
                    text "* Game Cabinet *":
                        color "#fc6ab3"
                        bold True
                        size 15
                    text ("Pick any game! They are all super fun!" if corruption < 2 else "Pick any game. They remember what you picked last time."):
                        color "#ffa0a0"
                        size 11

            grid 2 2:
                spacing 10
                for game_id, bg_light, bg_dark, title, blurb in HINAS_WORLD_GAMES:
                    use hinas_world_game_card(game_id, bg_light, bg_dark, title, blurb, _hw_seen.get(game_id, False), wide=True)

        elif page == "gallery":
            frame:
                xsize 699
                padding (10, 8, 10, 8)
                background "#ffffff"
                vbox:
                    spacing 4
                    text "* Gallery *":
                        color "#fc6ab3"
                        bold True
                        size 15
                    text ("Cute pictures coming soon! Please check back later~" if corruption < 1 else "Cute pictures coming soon. The missing ones keep loading first."):
                        color "#ffa0a0"
                        size 11

            hbox:
                spacing 10
                for slot in ["Track Meet", "Sleepover", "Donut Day"]:
                    frame:
                        xysize (219, 136)
                        padding (6, 6, 6, 6)
                        background "#ffffff"
                        vbox:
                            spacing 5
                            frame:
                                xysize (207, 92)
                                background ("#ffb5df" if corruption < 2 else "#4b2141")
                                text ("COMING SOON" if corruption < 2 else "IMAGE ERROR"):
                                    color "#ffffff"
                                    bold True
                                    size 13
                                    xalign 0.5
                                    yalign 0.5
                            text slot:
                                color "#e169ff"
                                bold True
                                size 11
                                xalign 0.5

            if corruption >= 2:
                text "private/gallery/lockerroom_0000.tmp could not be deleted":
                    color "#660044"
                    size 11
                    xalign 0.5

        else:
            frame:
                xsize 699
                padding (10, 8, 10, 8)
                background "#ffffff"
                vbox:
                    spacing 4
                    text "* About Hina *":
                        color "#fc6ab3"
                        bold True
                        size 15
                    text "Hina loves friends, running, donuts, sleepovers, and making every day fun!":
                        color "#ffa0a0"
                        size 11

            frame:
                xsize 699
                padding (10, 8, 10, 8)
                background "#fff7fb"
                vbox:
                    spacing 5
                    text "Favorite game: Anything with friends!":
                        color "#884477"
                        size 11
                    text "Favorite snack: Donuts, obviously!":
                        color "#884477"
                        size 11
                    text "Favorite saying: A smile fixes everything!":
                        color "#884477"
                        size 11
                    if corruption >= 1:
                        text "Least favorite question: Are you really going to eat all that?":
                            color "#660044"
                            size 11
                    if corruption >= 2:
                        text "Least favorite game: Rating Game. Rating Game. Rating Game.":
                            color "#660044"
                            bold True
                            size 11


screen hinas_world_game_card(game_id, bg_light, bg_dark, title, blurb, seen=False, wide=False):
    $ _hw_card_size = (334, 92) if wide else (162, 132)
    $ _hw_thumb_size = (96, 70) if wide else (154, 90)
    $ _hw_play_label = "PLAYED" if seen else "- PLAY -"

    button:
        xysize _hw_card_size
        padding (4, 4, 4, 4)
        background bg_dark
        hover_background "#ff66cc"
        hover_sound gui.hover_sound
        activate_sound gui.activate_sound
        action Return("game_" + game_id)

        if wide:
            hbox:
                spacing 8
                yalign 0.5

                frame:
                    xysize _hw_thumb_size
                    padding (0, 0, 0, 0)
                    background bg_light
                    text _hw_play_label:
                        color "#ffffff"
                        bold True
                        size 12
                        xalign 0.5
                        yalign 0.5

                vbox:
                    spacing 4
                    xsize 218
                    text title.replace("\n", " "):
                        color "#ffffff"
                        bold True
                        size 11
                    text blurb:
                        color "#ffe8f4"
                        size 9
        else:
            vbox:
                spacing 4
                xsize 154

                frame:
                    xysize _hw_thumb_size
                    padding (0, 0, 0, 0)
                    background bg_light
                    text _hw_play_label:
                        color "#ffffff"
                        bold True
                        size 15
                        xalign 0.5
                        yalign 0.5

                text title:
                    color "#ffffff"
                    bold True
                    size 10
                    xalign 0.5


# =============================================================================
#  LABEL
# =============================================================================

label cs_asahina_01:
    hide screen archive
    hide screen character_stories
    scene black
    stop music fadeout 1.0
    $ _hinas_world_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ hinas_world_page = "home"
    $ hinas_world_corruption = 0
    $ hinas_world_seen_outfitter = False
    $ hinas_world_seen_chatting = False
    $ hinas_world_seen_quiz = False
    $ hinas_world_seen_rating = False

    pause 1.5
    window auto
    "The archive loads an old browser capture with no timestamp, no author, and no clear reason to exist."
    "It looks harmless enough."

label cs_asahina_01_browser:
    window hide
    call screen cs_asahina_window98(hinas_world_page, hinas_world_corruption, hinas_world_seen_outfitter, hinas_world_seen_chatting, hinas_world_seen_quiz, hinas_world_seen_rating)
    $ _hw_choice = _return

    if _hw_choice == "exit":
        jump cs_asahina_01_exit

    if _hw_choice == "nav_home":
        $ hinas_world_page = "home"
        jump cs_asahina_01_browser

    if _hw_choice == "nav_games":
        $ hinas_world_page = "games"
        jump cs_asahina_01_browser

    if _hw_choice == "nav_gallery":
        $ hinas_world_page = "gallery"
        jump cs_asahina_01_browser

    if _hw_choice == "nav_about":
        $ hinas_world_page = "about"
        jump cs_asahina_01_browser

    if _hw_choice == "game_outfitter":
        jump cs_asahina_01_outfitter

    if _hw_choice == "game_chatting":
        jump cs_asahina_01_chatting

    if _hw_choice == "game_quiz":
        jump cs_asahina_01_quiz

    if _hw_choice == "game_rating":
        jump cs_asahina_01_rating

    jump cs_asahina_01_browser


# Branch scaffold: dress-up game. Start cute, then make each outfit choice
# become a social rule Asahina is punished for failing.
label cs_asahina_01_outfitter:
    scene black with dissolve_scene_full
    window auto
    "Hina's Outfitter loads a paper-doll silhouette with three tabs: School, Practice, Party."
    "The first pass should play like a normal dress-up game: tops, shoes, hair clips, cute ratings, sparkly sound effects."
    "The second pass should make the same choices feel coercive. Too athletic. Too hungry. Too loud. Too much."
    "Scaffold note: build this as a small outfit picker with three checks, then let the browser remember the player's harshest result."
    $ hinas_world_seen_outfitter = True
    $ hinas_world_corruption = max(hinas_world_corruption, 1)
    $ hinas_world_page = "games"
    jump cs_asahina_01_after_game


# Branch scaffold: chat-room game. Friendly handles become witnesses, then
# accusers, then one voice that sounds too much like Asahina performing cheer.
label cs_asahina_01_chatting:
    scene black with dissolve_scene_full
    window auto
    "Hina's Chatting opens a pastel chat room full of usernames from the sidebar: Emily, StarCute, DreamyDoll, PixelHeart."
    "At first, the player picks safe responses for Hina: compliment, joke, reassure, change the subject."
    "Then the room starts answering before the player clicks."
    "Scaffold note: this branch should use timed chat lines and one impossible message that references a choice from Outfitter."
    $ hinas_world_seen_chatting = True
    $ hinas_world_corruption = max(hinas_world_corruption, 2)
    $ hinas_world_page = "games"
    jump cs_asahina_01_after_game


# Branch scaffold: quiz game. A personality quiz that turns into a profile.
label cs_asahina_01_quiz:
    scene black with dissolve_scene_full
    window auto
    "Hina's Quiz Corner asks which Hina mood matches you today."
    "The answers should look silly: Sweet Hina, Sporty Hina, Hungry Hina, Sleepover Hina."
    "By the last question, the quiz should stop asking preferences and start listing facts it should not know."
    "Scaffold note: the correct answer is always the one that keeps Hina smiling, even when the question has stopped being cute."
    $ hinas_world_seen_quiz = True
    $ hinas_world_corruption = max(hinas_world_corruption, 2)
    $ hinas_world_page = "games"
    jump cs_asahina_01_after_game


# Branch scaffold: rating game. This is the emotional hinge. Make the player
# participate in reducing Hina to scores, then show the cost of scoring her.
label cs_asahina_01_rating:
    scene black with dissolve_scene_full
    window auto
    "Hina's Rating Game presents a bright scorecard and asks for quick judgments."
    "Cute. Fun. Popular. Fit. Easy to be around."
    "The scorecard should look like a joke until the wording turns clinical."
    "Scaffold note: avoid gore-copying the inspiration. The horror here is social measurement: the player is asked to grade a person who is trying not to disappear."
    $ hinas_world_seen_rating = True
    $ hinas_world_corruption = max(hinas_world_corruption, 3)
    $ hinas_world_page = "games"
    jump cs_asahina_01_after_game


label cs_asahina_01_after_game:
    if hinas_world_seen_outfitter and hinas_world_seen_chatting and hinas_world_seen_quiz and hinas_world_seen_rating:
        jump cs_asahina_01_site_break

    jump cs_asahina_01_browser


label cs_asahina_01_site_break:
    scene black with dissolve_scene_full
    pause 0.5
    window auto
    "The fourth game closes without asking."
    "For a second, the browser title reads Hina's World."
    "Then it reads Hina's Work."
    "Then just Hina."

    $ hinas_world_page = "about"
    $ hinas_world_corruption = 3
    window hide
    show screen cs_asahina_window98(hinas_world_page, hinas_world_corruption, hinas_world_seen_outfitter, hinas_world_seen_chatting, hinas_world_seen_quiz, hinas_world_seen_rating)
    pause 2.0
    hide screen cs_asahina_window98

    window auto
    "Full route handoff scaffold: this is where the recovered-website framing should break into Asahina's point of view."
    "The site has taught the player its rules. The next scene should prove why those rules hurt her."

    $ persistent.cs_asahina_01_unlocked = True
    jump cs_asahina_01_exit


label cs_asahina_01_exit:
    $ quick_menu = _hinas_world_prev_quick_menu
    return
