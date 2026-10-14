# Archive CG gallery, organized as act > chapter > artwork.
# CGEntry keys derive from image paths; explicit unlock_attr values preserve keys
# when art moves or changes. cg_unlock() records authored unlock beats.
# The gallery is available from the Archive; individual unseen CGs remain locked.
# Music Room also reads this catalog for unlocked background artwork.
# Empty chapters reserve catalog positions for content that has not been authored.

init python:
    def cg_key_from_path(image_path):
        """Derive an unlock key; moved art must retain its previous unlock_attr."""
        cleaned = str(image_path).lower()
        for junk in ("\\", "/", " ", "-", ".", "'"):
            cleaned = cleaned.replace(junk, "_")
        # Collapse the runs the substitutions above can create, so
        # "Sick Ass Anime OP/x.png" does not become "..._op__x_png".
        while "__" in cleaned:
            cleaned = cleaned.replace("__", "_")
        # The extension carries no information and just makes the key noisy.
        for suffix in ("_png", "_jpg", "_jpeg", "_webp"):
            if cleaned.endswith(suffix):
                cleaned = cleaned[:-len(suffix)]
        return "cg_seen_" + cleaned.strip("_")

    class CGEntry:
        """Represents a single CG image in the gallery."""
        def __init__(self, title, image_path, unlock_attr=None):
            self.title = title
            self.image_path = image_path
            # Explicit keys preserve existing unlocks when art is moved or replaced.
            self.unlock_attr = unlock_attr or cg_key_from_path(image_path)
            # Backwards-compatibility: older code expects a `persistent_key`
            # attribute on CG entries. Provide an alias so existing checks
            # like `_cg.persistent_key` continue to work.
            self.persistent_key = self.unlock_attr

        @property
        def unlocked(self):
            return bool(getattr(persistent, str(self.unlock_attr), False))

    class CGChapter:
        """Groups CGs under a specific chapter."""
        def __init__(self, name, cgs):
            self.name = name
            self.cgs = cgs

        # any_unlocked / unlocked_count let the UI show progress and decide
        # whether to render a chapter as available or "Locked".
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

        # Act-level rollups of the chapter stats above (used by the sidebar).
        @property
        def any_unlocked(self):
            return any(ch.any_unlocked for ch in self.chapters)

        @property
        def unlocked_count(self):
            return sum(ch.unlocked_count for ch in self.chapters)

        @property
        def total_count(self):
            return sum(len(ch.cgs) for ch in self.chapters)

    # -------------------------------------------------------------------------
    # MASTER CG CATALOG (act > chapter > CG). This is the single source the
    # gallery renders and that the Music Room reads from. Empty CGAct/CGChapter
    # lists are intentional placeholders for not-yet-authored content. Image
    # paths are relative to the game/ folder.
    # -------------------------------------------------------------------------
    cg_gallery_catalog = [
        CGAct("Other", [
            CGChapter("Archive Panels", [
                CGEntry("Roster", "assets/cg/archive_roster.png"),
                CGEntry("CG Gallery", "assets/cg/archive_cg_gallery.png"),
                CGEntry("Music Room", "assets/cg/archive_music_room.png"),
                CGEntry("Side Stories", "assets/cg/archive_side_stories.png"),
                CGEntry("Lost Records", "assets/cg/archive_lost_records.png"),
                CGEntry("Achievements", "assets/cg/archive_achievements.png"),
                CGEntry("Cards", "assets/cg/archive_cards.png"),
            ]),
        ]),
        CGAct("Main Campaign", [
            # These chapter CGs replace the first draft set. Preserve its keys
            # so the new art does not relock a chapter already selected.
            CGChapter("Chapter 0.5", [
                CGEntry("Open Invitation", "assets/cg/chapter_select/chapter_05_open_invitation.png",
                    unlock_attr=cg_key_from_path("assets/cg/chapter_select/chapter_05_beginning.png")),
            ]),
            CGChapter("Chapter 1", [
                CGEntry("Room for Six", "assets/cg/chapter_select/chapter_1_room_for_six.png",
                    unlock_attr=cg_key_from_path("assets/cg/chapter_select/chapter_1_friend_group.png")),
            ]),
            CGChapter("Chapter 2", [
                CGEntry("Summer Uncontained", "assets/cg/chapter_select/chapter_2_summer_uncontained.png",
                    unlock_attr=cg_key_from_path("assets/cg/chapter_select/chapter_2_midsummer.png")),
            ]),
            CGChapter("Chapter 3", [
                CGEntry("Between Bells", "assets/cg/chapter_select/chapter_3_between_bells.png",
                    unlock_attr=cg_key_from_path("assets/cg/chapter_select/chapter_3_before_storm.png")),
            ]),
            CGChapter("Chapter 4", [
                CGEntry("After the Noise", "assets/cg/chapter_select/chapter_4_after_the_noise.png",
                    unlock_attr=cg_key_from_path("assets/cg/chapter_select/chapter_4_first_domino.png")),
            ]),
            CGChapter("Chapter 5", [
                CGEntry("Somewhere Warm", "assets/cg/chapter_select/chapter_5_somewhere_warm.png",
                    unlock_attr=cg_key_from_path("assets/cg/chapter_select/chapter_5_winter_walk.png")),
            ]),
        ]),

        CGAct("Side Stories", [
            CGChapter("Matsuda's Story", [
                CGEntry(
                    "Seer",
                    "assets/cg/seer.png",
                    unlock_attr=cg_key_from_path("assets/cg/seer.png")
                ),
                CGEntry(
                    "Greywake Draw",
                    "assets/cg/dead_fantasy_greywake_draw.png"
                )
            ]),
            CGChapter("Player's Story", [

            ]),
            CGChapter("Tsubaki's Story", [
                CGEntry("What I Keep", "assets/cg/heads_what_i_keep.png"),
                CGEntry("What She Kept", "assets/cg/tails_what_she_kept.png"),
            ]),
            CGChapter("Asahina's Story", [
                CGEntry("Hina's World", "assets/cg/hinas_world.png"),
            ]),
            CGChapter("Sam's Story", [
                CGEntry(
                    "Ransom",
                    "assets/cg/ransom.png",
                    unlock_attr=cg_key_from_path("assets/cg/ransom.png")
                ),
                CGEntry(
                    "A Girl",
                    "assets/cg/hell.png",
                    unlock_attr=cg_key_from_path("assets/cg/hell.png")
                ),
            ]),
            CGChapter("Mom's Story", [
            ]),
            CGChapter("Monika's Story", [
            ]),
            CGChapter("Kotonoha's Story", [
                CGEntry("No One Lived There", "assets/cg/kotonoha_every_face.png"),
                CGEntry("Open Hands", "assets/cg/kotonoha_void_hunter.png"),
            ])
        ])
    ]

    # -------------------------------------------------------------------------
    # PUBLIC API: cg_unlock(...) -- "the player has now seen this".
    #
    # Takes CG TITLES ("Ransom") or current image paths ("assets/cg/ransom.png");
    # titles are what read best at a call site, paths are there for art that is
    # in the catalog under a title you would rather not spell out in the script.
    # Several at once is fine -- a montage that puts four CGs on screen in one
    # breath should be one line, not four.
    #
    # WHY THESE ARE HAND-PLACED. A CG is a discrete event: it happens once, at a
    # specific beat, and it is worth being able to grep "where does this unlock"
    # and get an answer. That is the opposite of an outfit, which is a state the
    # cast is constantly in and so is detected automatically instead (see
    # roster_scan_worn_outfits in Roster View/roster_view.rpy).
    #
    # In developer mode a name that matches nothing is a hard error rather than a
    # shrug, because the failure it catches -- a CG renamed in the catalog while
    # the script still unlocks the old title -- is invisible otherwise: the art
    # simply never appears in the gallery and nothing says why.
    # -------------------------------------------------------------------------
    def cg_unlock(*names):
        changed = False

        for name in names:
            entry = cg_find(name)

            if entry is None:
                if config.developer:
                    raise Exception("cg_unlock: no CG titled or pathed %r is in cg_gallery_catalog." % (name,))
                continue

            if not entry.unlocked:
                setattr(persistent, entry.persistent_key, True)
                changed = True

        if changed:
            renpy.save_persistent()

    def cg_find(name):
        """Resolve a CG by title or image path, case-insensitively."""
        wanted = str(name).strip().lower()

        for act in cg_gallery_catalog:
            for chapter in act.chapters:
                for cg in chapter.cgs:
                    if cg.title.lower() == wanted or cg.image_path.lower() == wanted:
                        return cg
        return None

    def cg_all_keys():
        """Every CG's persistent key (for the dev all-content switch)."""
        return tuple(
            cg.persistent_key
            for act in cg_gallery_catalog
            for chapter in act.chapters
            for cg in chapter.cgs
        )

# ----- Transforms -----
# (entrance/exit + per-item stagger animations; cosmetic only.)

# Sidebar entry stagger
transform cg_sidebar_anim(delay=0.0):
    alpha 0.0
    xoffset -15
    subpixel True
    pause delay
    easein_quad 0.3 alpha 1.0 xoffset 0

# Print grid stagger
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

# Fullscreen viewer: the print zooms up on open, and on a page turn travels in
# from the side of the key pressed (`slide` -1 / +1). Paging re-shows the
# screen, which delivers `replace`, so both events carry the same body -- the
# same fix as detail_frame_page in Roster View.
transform cg_viewer_enter(slide=0):
    on show, replace:
        alpha 0.0
        zoom (1.0 if slide else 0.96)
        xoffset (90 * slide)
        parallel:
            easeout_quad 0.28 xoffset 0
        parallel:
            easeout_quad 0.24 alpha 1.0 zoom 1.0
    on hide:
        alpha 1.0
        easeout_quad 0.2 alpha 0.0 zoom 0.96

# ----- Fullscreen CG Viewer -----
# One CG as a matted print on the dark table, held by photo corners, with a
# paper placard under it naming the chapter and the piece. Navigation
# RE-SHOWS this screen with the neighbouring index (no Hide), so the print's
# transform gets `replace` and can slide; it WRAPS past either end.
#   cg_list       : the act's flat list of UNLOCKED CGs (built by cg_gallery)
#   current_index : position within cg_list (drives the placard + counter)
#   slide         : -1 / +1 for a page turn, 0 for an open
screen cg_viewer(cg_list, current_index, slide=0):
    modal True
    zorder 200

    python:
        _cg = cg_list[current_index]
        _cg_count = len(cg_list)
        _cg_prev = Show("cg_viewer", cg_list=cg_list, current_index=(current_index - 1) % _cg_count, slide=-1)
        _cg_next = Show("cg_viewer", cg_list=cg_list, current_index=(current_index + 1) % _cg_count, slide=1)
        # The placard's kicker: the catalog chapter this print belongs to.
        _cg_chapter = next((ch.name for act in cg_gallery_catalog for ch in act.chapters if _cg in ch.cgs), "")

    key "game_menu" action Hide("cg_viewer")
    key "K_ESCAPE" action Hide("cg_viewer")

    # Left/right (keyboard) wrap through the unlocked CGs.
    if _cg_count > 1:
        key "K_LEFT" action _cg_prev
        key "K_RIGHT" action _cg_next

    add Solid("#05080bf2")

    # The print: a 1104x621 window (16:9, the shape of every CG) on a paper
    # mat, with the gallery's gold photo corners.
    fixed:
        xysize (1280, 720)
        align (0.5, 0.5)
        at cg_viewer_enter(slide)

        add Solid("#efe4cf") xpos 82 ypos 16 xysize (1116, 633)
        add Transform(_cg.image_path, fit="contain", xysize=(1104, 621)) xpos 88 ypos 22
        use archive_photo_corners(88, 22, 1104, 621)

    # The placard: chapter, title, and where this print sits in the run.
    frame:
        style "cg_viewer_placard"
        xalign 0.5
        ypos 656
        at cs_detail_swap(current_index)

        fixed:
            xysize (520, 40)

            text _cg_chapter.upper() style "cg_viewer_kicker" xpos 0 ypos 0
            text _cg.title style "cg_viewer_title" xpos 0 ypos 13
            text "{:02d} / {:02d}".format(current_index + 1, _cg_count):
                style "cg_viewer_counter"
                xanchor 1.0
                xpos 520
                ypos 14

    # Side page tabs (wrap-around), the same engraved tabs as the Roster file.
    if _cg_count > 1:
        textbutton "<":
            style "cg_viewer_pager"
            xpos 20
            yalign 0.46
            action _cg_prev

        textbutton ">":
            style "cg_viewer_pager"
            xanchor 1.0
            xpos 1260
            yalign 0.46
            action _cg_next

    textbutton _("Close"):
        style "archive_return_button"   # shared style from archive.rpy
        xanchor 1.0
        xpos 1198
        ypos 661
        action Hide("cg_viewer")

# ----- Main Gallery Screen (sidebar + content) -----
# Left: one cloth index tab per act (cg_gallery_catalog) -- the binder tabs
# Credits uses. Right: the selected act's chapters, each CG a mounted print
# with its title on the mount. `selected_act` is screen-local state.
screen cg_gallery():
    modal True

    # Selected act index
    default selected_act = 0

    use archive_backdrop

    key "game_menu" action Hide("cg_gallery", transition=enter_m_menu_doorway)
    key "K_ESCAPE" action Hide("cg_gallery", transition=enter_m_menu_doorway)

    # Keyboard navigation between acts (QoL).
    if len(cg_gallery_catalog) > 1:
        key "K_UP" action SetScreenVariable("selected_act", (selected_act - 1) % len(cg_gallery_catalog))
        key "K_DOWN" action SetScreenVariable("selected_act", (selected_act + 1) % len(cg_gallery_catalog))

    # Live census for the readout strip.
    $ _cg_total = sum(act.total_count for act in cg_gallery_catalog)
    $ _cg_unlocked = sum(act.unlocked_count for act in cg_gallery_catalog)

    frame:
        style "archive_shell_frame"
        padding (24, 20)
        at archive_frame_enter(50, 0.5, 30)

        vbox:
            spacing 12

            use archive_header("CG GALLERY", Hide("cg_gallery", transition=enter_m_menu_doorway))

            use archive_readout(
                "THE PRINT ROOM / {} OF {} RECOVERED".format(_cg_unlocked, _cg_total),
                "{} ACTS".format(len(cg_gallery_catalog)))

            hbox:
                spacing 2

                # --- LEFT: act index ----------------------------------------
                frame:
                    xsize 240
                    ysize 520
                    style "archive_sidebar_panel"
                    padding (14, 16)

                    vbox:
                        spacing 8

                        for idx, act in enumerate(cg_gallery_catalog):
                            $ _act_frac = (float(act.unlocked_count) / act.total_count) if act.total_count else 0.0

                            # SetScreenVariable reports itself selected for the
                            # current act, which is what puts its tab in the
                            # warm selected cloth.
                            button:
                                style "cg_sidebar_tab"
                                at cg_sidebar_anim(idx * 0.04)
                                action SetScreenVariable("selected_act", idx)

                                fixed:
                                    if act.any_unlocked:
                                        text act.name style "cg_sidebar_name" xpos 18 ypos 11

                                        # Progress as a gold rule along a hairline.
                                        add Solid("#d9cdb633") xpos 18 ypos 42 xysize (176, 1)
                                        add Solid(IM_GOLD) xpos 18 ypos 41 xysize (max(2, int(176 * _act_frac)), 2)

                                        text "{} OF {} PRINTS".format(act.unlocked_count, act.total_count):
                                            style "cg_sidebar_count"
                                            xpos 18
                                            ypos 50
                                    else:
                                        text act.name style "cg_sidebar_name_locked" xpos 18 ypos 11
                                        text ("NO PRINTS" if act.total_count == 0 else "SEALED"):
                                            style "cg_sidebar_count_locked"
                                            xpos 18
                                            ypos 50

                # --- RIGHT: selected act content ----------------------------
                frame:
                    xsize 910
                    ysize 520
                    style "archive_panel"
                    padding (22, 18)

                    $ _sel_act = cg_gallery_catalog[selected_act]
                    # Build a flat list of all unlocked CGs in this act for viewer navigation
                    # (the viewer pages through THIS list, so locked CGs are skipped).
                    $ _act_unlocked = [cg for ch in _sel_act.chapters for cg in ch.cgs if cg.unlocked]
                    # Chapters that actually contain CGs (skip empty placeholder chapters).
                    $ _act_chapters = [ch for ch in _sel_act.chapters if len(ch.cgs) > 0]
                    $ _act_frac_r = (float(_sel_act.unlocked_count) / _sel_act.total_count) if _sel_act.total_count else 0.0

                    vbox:
                        spacing 12

                        # Act header: name left, tally pinned right (a fixed
                        # with xanchor -- see archive_readout for why not an
                        # hbox), then a plum rule as long as the act is found.
                        fixed:
                            xsize 866
                            ysize 40

                            text _sel_act.name style "cg_panel_charname" xpos 0 yalign 0.5

                            if _sel_act.total_count == 0:
                                text "NO PRINTS ON RECORD" style "cg_panel_subtitle_locked" xanchor 1.0 xpos 866 yalign 0.5
                            elif _sel_act.any_unlocked:
                                text "{} OF {} RECOVERED".format(_sel_act.unlocked_count, _sel_act.total_count):
                                    style "cg_panel_subtitle"
                                    xanchor 1.0
                                    xpos 866
                                    yalign 0.5
                            else:
                                text "NONE RECOVERED YET" style "cg_panel_subtitle_locked" xanchor 1.0 xpos 866 yalign 0.5

                        fixed:
                            xsize 866
                            ysize 3

                            add Solid("#d9cdb640") ypos 1 xysize (866, 1)
                            if _act_frac_r > 0:
                                add Solid(IM_PLUM) xysize (max(2, int(866 * _act_frac_r)), 3)

                        viewport:
                            style_prefix "archive_sv"
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            pagekeys True
                            xsize 866
                            ysize 418

                            vbox:
                                spacing 22

                                if not _act_chapters:
                                    # Empty-act state (placeholder acts).
                                    fixed:
                                        xsize 850
                                        ysize 150

                                        text "NO PRINTS ON RECORD" style "cg_chapter_title_locked" xalign 0.5 ypos 48
                                        text "Nothing has been recovered for this act yet." style "cg_panel_subtitle_locked" xalign 0.5 ypos 86

                                # Chapters (only those with CGs)
                                # Keyed on the chapter, not on its position --
                                # see the note on the CG loop further down.
                                for chidx, chapter index (_sel_act.name, chapter.name) in enumerate(_act_chapters):
                                    $ _ch_delay = chidx * 0.08

                                    vbox:
                                        spacing 10
                                        at cg_chapter_anim(_ch_delay)

                                        # Chapter header: diamond, name, tally.
                                        hbox:
                                            spacing 10

                                            add Solid(IM_PLUM if chapter.any_unlocked else "#6f6670") xysize (6, 6) rotate 45 yalign 0.5

                                            if chapter.any_unlocked:
                                                text chapter.name style "cg_chapter_title" yalign 0.5
                                                text "{} OF {}".format(chapter.unlocked_count, len(chapter.cgs)):
                                                    style "cg_chapter_count"
                                                    yalign 0.5
                                            else:
                                                text chapter.name style "cg_chapter_title_locked" yalign 0.5
                                                text "SEALED" style "cg_chapter_count_locked" yalign 0.5

                                        # The prints, four to a row.
                                        vbox:
                                            spacing 14

                                            for row_start in range(0, len(chapter.cgs), 4):
                                                hbox:
                                                    spacing 14

                                                    # KEYED ON THE CG, NOT ON ITS POSITION. SL2
                                                    # caches a loop's children by LOOP COUNTER
                                                    # unless told otherwise, so switching acts
                                                    # handed the new act the old one's
                                                    # displayables wherever the positions lined
                                                    # up -- transform and all, already settled.
                                                    # Only the surplus prints faded in, and two
                                                    # acts of equal size animated nothing.
                                                    # Keying on the CG's own file makes each one
                                                    # its own displayable, so they all run the
                                                    # entrance from the top.
                                                    for row_idx, cg index cg.image_path in enumerate(chapter.cgs[row_start:row_start + 4]):
                                                        $ cidx = row_start + row_idx
                                                        # Index of this CG within the act's unlocked list (for the viewer).
                                                        $ _viewer_idx = _act_unlocked.index(cg) if cg.unlocked else 0

                                                        # The mount IS the button, so hovering it
                                                        # lifts the print (cs_card_focus, on the
                                                        # direct child) and develops its colour.
                                                        button:
                                                            style "cg_print_button"
                                                            at cg_thumb_anim(_ch_delay + cidx * 0.05)

                                                            # Unlocked -> open viewer; locked -> "not unlocked" dialog.
                                                            if cg.unlocked:
                                                                action Show("cg_viewer",
                                                                    cg_list=_act_unlocked,
                                                                    current_index=_viewer_idx)
                                                            else:
                                                                action Show("dialog",
                                                                    message="This CG hasn't been unlocked yet.",
                                                                    ok_action=Hide("dialog"))

                                                            fixed:
                                                                if cg.unlocked:
                                                                    at cs_card_focus

                                                                add "assets/gui/menu/illustrated/archive/print_mount.svg"

                                                                if cg.unlocked:
                                                                    add Transform(cg.image_path, fit="cover", xysize=(186, 105)):
                                                                        xpos 8
                                                                        ypos 8
                                                                        at archive_print_develop
                                                                    text cg.title style "cg_print_title" xpos 9 ypos 121
                                                                else:
                                                                    # The hub's sealed-record engraving, also 16:9.
                                                                    add Transform("assets/gui/menu/illustrated/archive/sealed_record.svg", fit="contain", xysize=(186, 105)):
                                                                        xpos 8
                                                                        ypos 8
                                                                    text "NOT YET RECOVERED" style "cg_print_title_locked" xpos 10 ypos 127

                                                                use archive_photo_corners(8, 8, 186, 105)

    # Console brackets framing the shell (cohesion with the archive hub).
    use archive_shell_brackets()

# ----- Styles -----
# The print room's materials: Credits' cloth index tabs, paper print mounts
# with gold corners, and paper ink on the Archive's dark panels.

style cg_sidebar_tab:
    xysize (212, 70)
    padding (0, 0)
    background Frame("assets/gui/menu/illustrated/credits/section_tab.svg", 12, 10, 12, 10)
    hover_background Frame("assets/gui/menu/illustrated/credits/section_tab_selected.svg", 12, 10, 12, 10)
    selected_background Frame("assets/gui/menu/illustrated/credits/section_tab_selected.svg", 12, 10, 12, 10)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style cg_sidebar_name is gui_text:
    font gui.default_font
    size 20
    color IM_PAPER
    outlines []

style cg_sidebar_name_locked is cg_sidebar_name:
    color "#8f8a86"

style cg_sidebar_count is gui_text:
    font gui.interface_font
    size 10
    kerning 1.2
    color "#d9c9a8"
    outlines []

style cg_sidebar_count_locked is cg_sidebar_count:
    color "#8f8a86"

style cg_panel_charname is gui_text:
    font gui.default_font
    size 30
    color IM_PAPER
    outlines []

style cg_panel_subtitle is archive_meta_text

style cg_panel_subtitle_locked is archive_meta_text:
    color IM_MUTED

style cg_chapter_title is gui_text:
    font gui.default_font
    size 21
    color IM_PAPER
    outlines []

style cg_chapter_title_locked is cg_chapter_title:
    color "#8f8a86"

style cg_chapter_count is archive_meta_text:
    size 10

style cg_chapter_count_locked is cg_chapter_count:
    color "#8f8a86"

style cg_print_button:
    xysize (202, 152)
    padding (0, 0)
    background None
    hover_background None
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

# Titles on the mounts use Chapter Select's folio ink (teal on hover).
style cg_print_title is cs_name:
    size 16

style cg_print_title_locked is cs_span_locked

style cg_viewer_placard is frame:
    background IM_PAPER_PANEL
    padding (20, 6)

style cg_viewer_kicker is cs_kicker:
    color "#714966"

style cg_viewer_title is gui_text:
    font gui.default_font
    size 22
    color IM_INK
    outlines []

style cg_viewer_counter is gui_text:
    font gui.interface_font
    size 14
    kerning 1.2
    color "#714966"
    outlines []

style cg_viewer_pager is archive_return_button:
    xsize 48
    ysize 96
    padding (0, 0)

style cg_viewer_pager_text is archive_return_button_text:
    size 26
    align (0.5, 0.5)
