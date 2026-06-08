# CG Gallery addon
# A browsable gallery of CGs organized by act and chapter, accessed from the archive menu.
# Uses vanilla DDLC CGs as placeholders until original CGs are created.

# ----- Data Definitions -----

init python:
    class CGEntry:
        """Represents a single CG image in the gallery."""
        def __init__(self, title, image_path, unlock_attr=None):
            self.title = title
            self.image_path = image_path
            # `unlock_attr` is the name of a boolean attribute on `persistent`
            # that tracks whether this CG has been unlocked. If `None`, treat
            # the CG as unlocked by default (useful for mod-added assets).
            self.unlock_attr = unlock_attr
            # Backwards-compatibility: older code expects a `persistent_key`
            # attribute on CG entries. Provide an alias so existing checks
            # like `_cg.persistent_key` continue to work.
            self.persistent_key = unlock_attr

        @property
        def unlocked(self):
            # If no persistent key was supplied, assume the CG is available.
            if self.unlock_attr is None:
                return True

            # Ensure we pass a string attribute name to getattr; if the stored
            # key isn't a string, coerce it to string just in case.
            key = str(self.unlock_attr)
            return getattr(persistent, key, False)

    class CGChapter:
        """Groups CGs under a specific chapter."""
        def __init__(self, name, cgs):
            self.name = name
            self.cgs = cgs

        @property
        def any_unlocked(self):
            return any(c.unlocked for c in self.cgs)

        @property
        def unlocked_count(self):
            return sum(1 for c in self.cgs if c.unlocked)

    class CGAct:
        """Groups chapters under a story act."""
        def __init__(self, name, chapters):
            self.name = name
            self.chapters = chapters

        @property
        def any_unlocked(self):
            return any(ch.any_unlocked for ch in self.chapters)

        @property
        def unlocked_count(self):
            return sum(ch.unlocked_count for ch in self.chapters)

        @property
        def total_count(self):
            return sum(len(ch.cgs) for ch in self.chapters)

    # Master CG catalog -- organized by act > chapter
    # Uses vanilla DDLC CGs as placeholders
    cg_gallery_catalog = [
        CGAct("Opening", [
            CGChapter("All Opening CGs", [
                CGEntry("Title Drop", "addons/Sick Ass Anime OP/titledropalt.png"),
                CGEntry("Matsuda Performing", "mod_assets/gui/warning2.png"),
                CGEntry("Club President", "addons/Sick Ass Anime OP/monikaclub.png"),
                CGEntry("Argue", "addons/Sick Ass Anime OP/arguing.png"),
                CGEntry("Poster Session", "addons/Sick Ass Anime OP/asahinaposter.png"),
                CGEntry("Mom at Work", "addons/Sick Ass Anime OP/momwork.png"),
                CGEntry("Sam Bus", "addons/Sick Ass Anime OP/sambus.png"),
                CGEntry("Matsuda Wistful", "addons/Sick Ass Anime OP/matsuwistful.png"),
                CGEntry("Ice Cream", "addons/Sick Ass Anime OP/tsubakimatsudaicecream.png"),
                CGEntry("Consoling Tsubaki", "addons/Sick Ass Anime OP/consoletsubaki.png"),
                CGEntry("Redshift", "addons/Sick Ass Anime OP/redshift.png"),
                CGEntry("Blueshift", "addons/Sick Ass Anime OP/blueshift.png"),
                CGEntry("Puppet", "addons/Sick Ass Anime OP/puppet.png"),
                CGEntry("World Broken", "addons/Sick Ass Anime OP/asahinaworldbroken.png"),
                CGEntry("No Marks", "addons/Sick Ass Anime OP/nomarks.png"),
                CGEntry("Cashier Kotonoha", "addons/Sick Ass Anime OP/storekoto.png"),
                CGEntry("Turmoil", "addons/Sick Ass Anime OP/turmoil.png"),
                CGEntry("Smug Sam", "addons/Sick Ass Anime OP/samvillain.png"),
                CGEntry("Next Line Missing", "addons/Sick Ass Anime OP/missing.png"),
            ])
        ]),
        CGAct("Season 1", [

        ]),
        CGAct("Season 2", [

        ]),
        CGAct("Intermission", [

        ]),
        CGAct("Season 3", [

        ]),
        CGAct("Side Stories", [
            CGChapter("Matsuda's Story", [
                CGEntry("Campaign", "mod_assets/cg/campaign.png"),
                CGEntry("Seer", "mod_assets/cg/seer.png")
            ]),
            CGChapter("Player's Story", [
                
            ]),
            CGChapter("Tsubaki's Story", [
                
            ]),
            CGChapter("Asahina's Story", [
                
            ]),
            CGChapter("Sam's Story", [
                CGEntry("Ransom", "mod_assets/cg/ransom.png"),
                CGEntry("A Girl", "mod_assets/cg/hell.png"),
            ]),
            CGChapter("Mom's Story", [
                
            ]),
            CGChapter("Monika's Story", [
                CGEntry("Lies", "mod_assets/cg/lies.png"),
            ]),
            CGChapter("Kotonoha's Story", [
                CGEntry("Every Face", "mod_assets/cg/everyface.png"),
                CGEntry("Void Hunter", "mod_assets/cg/voidhunter.png"),
            ])
        ])
    ]

# ----- Transforms -----

# Main frame entrance/exit
transform cg_frame_enter:
    on show:
        alpha 0.0
        yoffset -50
        easein_back 0.5 alpha 1.0 yoffset 0
    on hide:
        alpha 1.0
        easeout_quad 0.25 alpha 0.0 yoffset -30

# Sidebar entry stagger
transform cg_sidebar_anim(delay=0.0):
    alpha 0.0
    xoffset -15
    subpixel True
    pause delay
    easein_quad 0.3 alpha 1.0 xoffset 0

# Thumbnail grid stagger
transform cg_thumb_anim(delay=0.0):
    alpha 0.0
    zoom 0.9
    subpixel True
    pause delay
    easein_back 0.35 alpha 1.0 zoom 1.0

# Chapter row stagger (slides in from right)
transform cg_chapter_anim(delay=0.0):
    alpha 0.0
    xoffset 20
    subpixel True
    pause delay
    easein_quad 0.3 alpha 1.0 xoffset 0

# Fullscreen viewer entrance/exit
transform cg_viewer_enter:
    on show:
        alpha 0.0
        zoom 0.95
        easein_back 0.3 alpha 1.0 zoom 1.0
    on hide:
        alpha 1.0
        easeout_quad 0.2 alpha 0.0 zoom 0.95

# ----- Fullscreen CG Viewer -----

screen cg_viewer(image_path, cg_list, current_index):
    modal True
    zorder 200

    key "game_menu" action Hide("cg_viewer")
    key "K_ESCAPE" action Hide("cg_viewer")

    # Navigate between unlocked CGs
    if current_index > 0:
        key "K_LEFT" action [
            Hide("cg_viewer"),
            Show("cg_viewer",
                image_path=cg_list[current_index - 1].image_path,
                cg_list=cg_list,
                current_index=current_index - 1)
        ]
    if current_index < len(cg_list) - 1:
        key "K_RIGHT" action [
            Hide("cg_viewer"),
            Show("cg_viewer",
                image_path=cg_list[current_index + 1].image_path,
                cg_list=cg_list,
                current_index=current_index + 1)
        ]

    add Solid("#000000f2")

    # CG image centered
    frame:
        background None
        xfill True
        yfill True
        padding (40, 40)
        at cg_viewer_enter

        add image_path:
            fit "contain"
            xalign 0.5
            yalign 0.5

    # Nav arrows (only if multiple CGs)
    if len(cg_list) > 1:
        # Left arrow
        if current_index > 0:
            textbutton "<":
                xalign 0.0
                yalign 0.5
                xoffset 10
                text_size 60
                text_color "#56d7ffaa"
                text_hover_color "#ffffff"
                text_bold True
                text_outlines [(2, "#02040b", 0, 0)]
                background None
                hover_background None
                action [
                    Hide("cg_viewer"),
                    Show("cg_viewer",
                        image_path=cg_list[current_index - 1].image_path,
                        cg_list=cg_list,
                        current_index=current_index - 1)
                ]

        # Right arrow
        if current_index < len(cg_list) - 1:
            textbutton ">":
                xalign 1.0
                yalign 0.5
                xoffset -10
                text_size 60
                text_color "#56d7ffaa"
                text_hover_color "#ffffff"
                text_bold True
                text_outlines [(2, "#02040b", 0, 0)]
                background None
                hover_background None
                action [
                    Hide("cg_viewer"),
                    Show("cg_viewer",
                        image_path=cg_list[current_index + 1].image_path,
                        cg_list=cg_list,
                        current_index=current_index + 1)
                ]

    # Counter label (e.g. "2 / 3")
    text "{} / {}".format(current_index + 1, len(cg_list)):
        xalign 0.5
        yalign 1.0
        yoffset -12
        size 20
        color "#9fc9d6"
        outlines [(1, "#02040b", 0, 0)]

    textbutton "Close":
        xalign 1.0
        yalign 0.0
        xoffset -20
        yoffset 15
        style "archive_return_button"
        action Hide("cg_viewer")

# ----- Main Gallery Screen (sidebar + content) -----

screen cg_gallery():
    modal True

    # Selected act index
    default selected_act = 0

    use archive_backdrop

    key "game_menu" action Hide("cg_gallery")
    key "K_ESCAPE" action Hide("cg_gallery")

    frame:
        style "archive_shell_frame"
        padding (24, 20)
        at cg_frame_enter

        vbox:
            spacing 14

            use archive_header("CG GALLERY", Hide("cg_gallery"))

            add Solid("#56d7ff66"):
                xsize 1150
                ysize 2
                xalign 0.5

            hbox:
                spacing 0

                frame:
                    xsize 240
                    ysize 556
                    style "archive_sidebar_panel"
                    padding (14, 16)

                    vbox:
                        spacing 8

                        for idx, act in enumerate(cg_gallery_catalog):
                            $ _sb_delay = idx * 0.04

                            button:
                                xsize 212
                                ysize 76
                                padding (12, 10)
                                hover_sound gui.hover_sound
                                activate_sound gui.activate_sound
                                at cg_sidebar_anim(_sb_delay)

                                if idx == selected_act:
                                    background Solid("#12314af2")
                                    hover_background Solid("#17415fee")
                                else:
                                    background Solid("#07111dcc")
                                    hover_background Solid("#12314aee")

                                action SetScreenVariable("selected_act", idx)

                                vbox:
                                    spacing 4
                                    yalign 0.5

                                    if act.any_unlocked:
                                        text act.name style "cg_sidebar_name"
                                        text "{}/{} CGs".format(act.unlocked_count, act.total_count):
                                            style "cg_sidebar_count"
                                    else:
                                        text act.name style "cg_sidebar_name_locked"
                                        text "Locked" style "cg_sidebar_count_locked"

                add Solid("#56d7ff44"):
                    xsize 2
                    ysize 556

                frame:
                    xsize 910
                    ysize 556
                    style "archive_panel"
                    padding (24, 20)

                    $ _sel_act = cg_gallery_catalog[selected_act]
                    # Build a flat list of all unlocked CGs in this act for viewer navigation
                    $ _act_unlocked = [cg for ch in _sel_act.chapters for cg in ch.cgs if cg.unlocked]

                    viewport:
                        style_prefix "cs_sv"
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        xsize 860
                        ysize 516

                        vbox:
                            spacing 20

                            # Act header
                            text _sel_act.name style "cg_panel_charname"

                            if _sel_act.any_unlocked:
                                text "{} of {} CGs unlocked".format(_sel_act.unlocked_count, _sel_act.total_count):
                                    style "cg_panel_subtitle"
                            else:
                                text "No CGs unlocked yet" style "cg_panel_subtitle_locked"

                            # Separator
                            add Solid("#56d7ff22"):
                                xsize 840
                                ysize 1

                            # Chapters
                            for chidx, chapter in enumerate(_sel_act.chapters):
                                $ _ch_delay = chidx * 0.08

                                vbox:
                                    spacing 12
                                    at cg_chapter_anim(_ch_delay)

                                    # Chapter header
                                    hbox:
                                        spacing 12
                                        yalign 0.5

                                        # Status pip
                                        frame:
                                            yalign 0.5
                                            xsize 4
                                            ysize 24
                                            if chapter.any_unlocked:
                                                background Solid("#56d7ff")
                                            else:
                                                background Solid("#374654")

                                        if chapter.any_unlocked:
                                            text chapter.name style "cg_chapter_title"
                                            text "({}/{})".format(chapter.unlocked_count, len(chapter.cgs)):
                                                style "cg_chapter_count"
                                                yalign 0.5
                                        else:
                                            text chapter.name style "cg_chapter_title_locked"
                                            text "(Locked)":
                                                style "cg_chapter_count_locked"
                                                yalign 0.5

                                    # CG thumbnails for this chapter, wrapped into rows.
                                    vbox:
                                        spacing 12
                                        xoffset 16

                                        for row_start in range(0, len(chapter.cgs), 4):
                                            hbox:
                                                spacing 14

                                                for row_idx, cg in enumerate(chapter.cgs[row_start:row_start + 4]):
                                                    $ cidx = row_start + row_idx
                                                    $ _t_delay = _ch_delay + cidx * 0.05
                                                    $ _viewer_idx = _act_unlocked.index(cg) if cg.unlocked else 0

                                                    button:
                                                        xsize 200
                                                        ysize 118
                                                        padding (3, 3)
                                                        hover_sound gui.hover_sound
                                                        activate_sound gui.activate_sound
                                                        at cg_thumb_anim(_t_delay)

                                                        if cg.unlocked:
                                                            background Solid("#07111dcc")
                                                            hover_background Solid("#12314af2")
                                                            action Show("cg_viewer",
                                                                image_path=cg.image_path,
                                                                cg_list=_act_unlocked,
                                                                current_index=_viewer_idx)
                                                        else:
                                                            background Solid("#050811cc")
                                                            action Show("dialog",
                                                                message="This CG hasn't been unlocked yet.",
                                                                ok_action=Hide("dialog"))

                                                        frame:
                                                            background None
                                                            xfill True
                                                            yfill True

                                                            if cg.unlocked:
                                                                add cg.image_path:
                                                                    fit "contain"
                                                                    xalign 0.5
                                                                    yalign 0.5
                                                            else:
                                                                # Locked placeholder
                                                                vbox:
                                                                    xalign 0.5
                                                                    yalign 0.5
                                                                    spacing 4

                                                                    text "?":
                                                                        xalign 0.5
                                                                        size 30
                                                                        color "#4f5b67"
                                                                        bold True
                                                                        outlines [(1, "#02040b", 0, 0)]
                                                                    text "Locked":
                                                                        xalign 0.5
                                                                        size 12
                                                                        color "#4f5b67"
                                                                        outlines [(1, "#02040b", 0, 0)]

                                    add Solid("#56d7ff16"):
                                        xsize 840
                                        ysize 1

# ----- Styles -----

style cg_title:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 36
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style cg_sidebar_name:
    size 20
    color "#dff8ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cg_sidebar_name_locked:
    size 20
    color "#687787"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cg_sidebar_count:
    size 14
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

style cg_sidebar_count_locked:
    size 14
    color "#4f5b67"
    outlines [(1, "#02040b", 0, 0)]

style cg_panel_charname:
    size 30
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style cg_panel_subtitle:
    size 16
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

style cg_panel_subtitle_locked:
    size 16
    color "#4f5b67"
    outlines [(1, "#02040b", 0, 0)]

style cg_chapter_title:
    size 20
    color "#dff8ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cg_chapter_title_locked:
    size 20
    color "#4f5b67"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style cg_chapter_count:
    size 14
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

style cg_chapter_count_locked:
    size 14
    color "#4f5b67"
    outlines [(1, "#02040b", 0, 0)]
