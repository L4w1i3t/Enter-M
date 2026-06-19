# Character Stories addon
# A catalog of single short-stories pertaining to each character in the mod,
# independent of the main story and its continuity. Stories unlock as the player
# meets each character, providing extra development, worldbuilding, and "what-if"
# scenarios. Accessed from the archive menu.

# ----- Data Definitions -----

init python:
    class CharacterStoryEntry:
        """Represents a single story for a character."""
        def __init__(self, title, description, label_name, persistent_key):
            self.title = title
            self.description = description
            self.label_name = label_name
            self.persistent_key = persistent_key

        @property
        def unlocked(self):
            return getattr(persistent, self.persistent_key, False)

    class CharacterStoryCatalog:
        """Groups stories under a character with a display image."""
        def __init__(self, name, sprite_image, stories, fit_mode="contain"):
            self.name = name
            self.sprite_image = sprite_image
            self.stories = stories
            self.fit_mode = fit_mode

        @property
        def any_unlocked(self):
            return any(s.unlocked for s in self.stories)

        @property
        def unlocked_count(self):
            return sum(1 for s in self.stories if s.unlocked)

    # Master catalog
    character_story_catalog = [
        CharacterStoryCatalog(
            "Matsuda",
            "matsuda neut",
            [
                CharacterStoryEntry("Dead Fantasy", "Two armies meet at Greywake Field.", "cs_matsuda_01", "cs_matsuda_01_unlocked"),
                CharacterStoryEntry("Ontological Seer", "You guys like RPGs, right?", "cs_matsuda_02", "cs_matsuda_02_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Player",
            "mc neut",
            [
                CharacterStoryEntry("Coming Soon", "This story hasn't been written yet.", "cs_player_01", "cs_player_01_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Tsubaki",
            "tsubaki neut",
            [
                CharacterStoryEntry("Same Coin", "A split narrative.", "cs_tsubaki_01", "cs_tsubaki_01_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Asahina",
            "asahina neut",
            [
                CharacterStoryEntry("Hina's World", "Inspired by the Lacey Games horror series.", "cs_asahina_01", "cs_asahina_01_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Sam",
            "sam neut",
            [
                CharacterStoryEntry("Purgatorium", "Never download weird apps from Aptoide.", "cs_sam_01", "cs_sam_01_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Mom",
            "mom neut",
            [
                CharacterStoryEntry("Continuance", "A case file with no verdict.", "cs_mom_01", "cs_mom_01_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "Monika",
            "monika 1a",
            [
                CharacterStoryEntry("Lies and Poems", "It feels like something should be remembered, but...", "cs_monika_01", "cs_monika_01_unlocked"),
            ],
            fit_mode="cover",
        ),
        CharacterStoryCatalog(
            "Kotonoha",
            "kotonoha neut",
            [
                CharacterStoryEntry("The Girl with Every Face", "Who is she?", "cs_kotonoha_01", "cs_kotonoha_01_unlocked"),
                CharacterStoryEntry("The Void Hunter", "When you stare into the abyss, the abyss stares back.", "cs_kotonoha_02", "cs_kotonoha_02_unlocked"),
            ],
        ),
        CharacterStoryCatalog(
            "???",
            "mod_assets/dump/icon_placeholder.png",
            [
                CharacterStoryEntry("???", "This story is still locked.", "", ""),
            ],
        ),
    ]

# Persistent unlock flags (default False)
default persistent.cs_matsuda_01_unlocked = False
default persistent.cs_matsuda_02_unlocked = False
default persistent.cs_tsubaki_01_unlocked = False
default persistent.cs_asahina_01_unlocked = False
default persistent.cs_sam_01_unlocked = False
default persistent.cs_mom_01_unlocked = False
default persistent.cs_monika_01_unlocked = False
default persistent.cs_kotonoha_01_unlocked = False
default persistent.cs_kotonoha_02_unlocked = False
# If archive_unlocked_character_stories is True, all individual story flags get flipped on.
# Useful for dev/testing so I don't have to toggle each flag manually.

init 10 python:
    if persistent.archive_unlocked_character_stories:
        for _cat in character_story_catalog:
            for _story in _cat.stories:
                setattr(persistent, _story.persistent_key, True)

# ----- Transforms -----

# Frame entrance / exit
transform cs_frame_enter:
    on show:
        alpha 0.0
        yoffset -50
        easein_back 0.5 alpha 1.0 yoffset 0
    on hide:
        alpha 1.0
        easeout_quad 0.25 alpha 0.0 yoffset -30

# Sidebar entry stagger
transform cs_sidebar_anim(delay=0.0):
    alpha 0.0
    xoffset -15
    subpixel True
    pause delay
    easein_quad 0.3 alpha 1.0 xoffset 0

# ----- Main Screen (sidebar + content) -----

screen character_stories():
    modal True

    # Selected character index -- defaults to first in list
    default selected_idx = 0

    use archive_backdrop

    key "game_menu" action Hide("character_stories")
    key "K_ESCAPE" action Hide("character_stories")

    frame:
        style "archive_shell_frame"
        padding (24, 20)
        at cs_frame_enter

        vbox:
            spacing 14

            use archive_header("CHARACTER STORIES", Hide("character_stories"))

            add Solid("#56d7ff66"):
                xsize 1150
                ysize 2
                xalign 0.5

            hbox:
                spacing 0

                frame:
                    xsize 320
                    ysize 556
                    style "archive_sidebar_panel"
                    padding (14, 16)

                    viewport:
                        style_prefix "archive_sv"
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        xsize 292
                        ysize 524

                        vbox:
                            spacing 8

                            for idx, catalog in enumerate(character_story_catalog):
                                $ _sb_delay = idx * 0.04

                                button:
                                    xfill True
                                    ysize 76
                                    padding (12, 10)
                                    hover_sound gui.hover_sound
                                    activate_sound gui.activate_sound
                                    at cs_sidebar_anim(_sb_delay)

                                    if idx == selected_idx:
                                        background Solid("#12314af2")
                                        hover_background Solid("#17415fee")
                                    else:
                                        background Solid("#07111dcc")
                                        hover_background Solid("#12314aee")

                                    action SetScreenVariable("selected_idx", idx)

                                    hbox:
                                        spacing 14
                                        yalign 0.5

                                        # Character thumbnail
                                        frame:
                                            xsize 52
                                            ysize 52
                                            background Solid("#07101add")
                                            padding (0, 0)

                                            # viewport clips overflow from tall portrait sprites
                                            viewport:
                                                xsize 52
                                                ysize 52

                                                if catalog.any_unlocked:
                                                    add catalog.sprite_image:
                                                        fit "cover"
                                                        xalign 0.5
                                                        yalign 0.0
                                                else:
                                                    add catalog.sprite_image:
                                                        fit "cover"
                                                        xalign 0.5
                                                        yalign 0.0
                                                        matrixcolor BrightnessMatrix(0.0) * SaturationMatrix(0.0)

                                        vbox:
                                            spacing 2
                                            yalign 0.5

                                            if catalog.any_unlocked:
                                                text catalog.name style "cs_sidebar_name"
                                                text "{}/{} stories".format(catalog.unlocked_count, len(catalog.stories)):
                                                    style "cs_sidebar_count"
                                            else:
                                                text catalog.name style "cs_sidebar_name_locked"
                                                text "Locked" style "cs_sidebar_count_locked"

                add Solid("#56d7ff44"):
                    xsize 2
                    ysize 556

                frame:
                    xsize 830
                    ysize 556
                    style "archive_panel"
                    padding (24, 24)

                    $ _sel_catalog = character_story_catalog[selected_idx]

                    vbox:
                        spacing 18

                        # Character name + sprite preview
                        hbox:
                            spacing 24

                            # Character portrait
                            frame:
                                xsize 140
                                ysize 155
                                background Solid("#07101add")
                                padding (0, 0)

                                if _sel_catalog.any_unlocked:
                                    add _sel_catalog.sprite_image:
                                        fit _sel_catalog.fit_mode
                                        xalign 0.5
                                        yalign 1.0
                                else:
                                    add _sel_catalog.sprite_image:
                                        fit _sel_catalog.fit_mode
                                        xalign 0.5
                                        yalign 1.0
                                        matrixcolor BrightnessMatrix(0.0) * SaturationMatrix(0.0)

                            vbox:
                                spacing 8
                                yalign 0.5

                                text _sel_catalog.name style "cs_panel_charname"

                                if _sel_catalog.any_unlocked:
                                    text "{} of {} stories unlocked".format(_sel_catalog.unlocked_count, len(_sel_catalog.stories)):
                                        style "cs_panel_subtitle"
                                else:
                                    text "No stories unlocked yet" style "cs_panel_subtitle_locked"

                        # Separator
                        add Solid("#56d7ff22"):
                            xsize 780
                            ysize 1

                        # Story rows
                        viewport:
                            style_prefix "archive_sv"
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            xsize 780
                            ysize 340

                            vbox:
                                xfill True
                                spacing 10

                                for sidx, story in enumerate(_sel_catalog.stories):
                                    $ _sr_delay = sidx * 0.07
                                    $ _story_num = "{:02d}".format(sidx + 1)

                                    # Card-style story row
                                    button:
                                        xfill True
                                        ysize 88
                                        padding (0, 0)
                                        hover_sound gui.hover_sound
                                        activate_sound gui.activate_sound

                                        if story.unlocked:
                                            background Solid("#07111dcc")
                                            hover_background Solid("#12314af2")
                                            action [Hide("character_stories"), Hide("archive"), Start(story.label_name)]
                                        else:
                                            background Solid("#050811cc")
                                            hover_background Solid("#07111dcc")
                                            action Show("dialog", message="This story is still locked.", ok_action=Hide("dialog"))

                                        vbox:
                                            xfill True
                                            spacing 0

                                            # Main card body
                                            hbox:
                                                xfill True
                                                spacing 0

                                                # Number badge column
                                                frame:
                                                    xsize 64
                                                    yminimum 88
                                                    padding (0, 0)
                                                    if story.unlocked:
                                                        background Solid("#56d7ff22")
                                                    else:
                                                        background Solid("#030609aa")

                                                    text _story_num:
                                                        xalign 0.5
                                                        yalign 0.5
                                                        if story.unlocked:
                                                            style "cs_story_num"
                                                        else:
                                                            style "cs_story_num_locked"

                                                # Title and description
                                                frame:
                                                    xfill True
                                                    yminimum 88
                                                    background None
                                                    padding (20, 14, 16, 14)

                                                    vbox:
                                                        yalign 0.5
                                                        spacing 6

                                                        if story.unlocked:
                                                            text story.title style "cs_story_title"
                                                            if story.description:
                                                                text story.description style "cs_story_desc"
                                                        else:
                                                            text "???" style "cs_story_title_locked"
                                                            text "This story is still locked." style "cs_story_locked_label"

                                                # Status column
                                                frame:
                                                    xsize 90
                                                    yminimum 88
                                                    background None
                                                    padding (0, 0)

                                                    if story.unlocked:
                                                        text "PLAY  >" style "cs_story_status":
                                                            xalign 0.5
                                                            yalign 0.5
                                                    else:
                                                        text "LOCKED" style "cs_story_status_locked":
                                                            xalign 0.5
                                                            yalign 0.5

                                            # Bottom accent bar
                                            frame:
                                                xfill True
                                                ysize 3
                                                padding (0, 0)
                                                if story.unlocked:
                                                    background Solid("#56d7ff")
                                                else:
                                                    background Solid("#374654")

# ----- Styles -----

style cs_title:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 36
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

# Sidebar styles
style cs_sidebar_name:
    size 20
    color "#dff8ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_sidebar_name_locked:
    size 20
    color "#687787"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_sidebar_count:
    size 14
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

style cs_sidebar_count_locked:
    size 14
    color "#4f5b67"
    outlines [(1, "#02040b", 0, 0)]

# Right panel styles
style cs_panel_charname:
    size 32
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style cs_panel_subtitle:
    size 16
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

style cs_panel_subtitle_locked:
    size 16
    color "#4f5b67"
    outlines [(1, "#02040b", 0, 0)]

# Story row styles
style cs_story_title:
    size 21
    color "#dff8ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_story_desc:
    size 14
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

style cs_story_title_locked:
    size 21
    color "#4f5b67"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_story_locked_label:
    size 13
    color "#4f5b67"
    outlines [(1, "#02040b", 0, 0)]

style cs_story_num:
    size 22
    color "#56d7ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_story_num_locked:
    size 22
    color "#374654"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_story_status:
    size 13
    color "#56d7ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cs_story_status_locked:
    size 12
    color "#4f5b67"
    bold True
    outlines [(1, "#02040b", 0, 0)]

