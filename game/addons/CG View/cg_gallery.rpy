# =============================================================================
# cg_gallery.rpy  --  CG GALLERY (archive feature)
# =============================================================================
#
# WHAT THIS FILE PROVIDES
#   A browsable gallery of CG artwork organized as Act > Chapter > CG. The main
#   screen (cg_gallery) is a sidebar of acts on the left + a content panel of
#   chapters/thumbnails on the right. Clicking an unlocked thumbnail opens the
#   fullscreen viewer (cg_viewer) with left/right navigation through that act's
#   unlocked CGs.
#
# HOW IT IS REACHED
#   - Archive "CG Gallery" card -> Show("cg_gallery")   (see game/archive.rpy).
#
# UNLOCKING
#   Every CGEntry is gated by a persistent bool, DERIVED FROM ITS IMAGE PATH so
#   the catalog stays a plain list of art (see CGEntry.__init__). A CG unlocks
#   the first time the player is shown it, via an explicit `$ cg_unlock(...)` at
#   the beat that shows it -- see cg_unlock() below for where those live and why
#   they are hand-placed rather than detected.
#   The gallery PANEL itself is open from the first launch now; this file is what
#   decides which art inside it is real and which is a "?" tile.
#
# DATA MODEL (built once at init time; see init 5 python at bottom of init block)
#   cg_gallery_catalog = [ CGAct( name, [ CGChapter( name, [ CGEntry... ] ) ] ) ]
#   - CGEntry   : one image (title, image_path, optional unlock_attr).
#   - CGChapter : group of CGs; exposes any_unlocked / unlocked_count.
#   - CGAct     : group of chapters; exposes any_unlocked / unlocked_count / total_count.
#
# CROSS-FILE CONSUMERS OF THIS DATA
#   - game/addons/Music Room/music_room.rpy -> pick_random_cg() walks
#     cg_gallery_catalog to show a random unlocked CG as "now playing" art.
#
# SHARED THEME BORROWED FROM game/archive.rpy
#   - screen archive_backdrop, screen archive_header(...)
#   - styles archive_shell_frame / archive_sidebar_panel / archive_panel
#   - style archive_return_button (the viewer's Close button)
#   - generic "dialog" screen (locked-CG popup)
#   NOTE: the viewports here set style_prefix "cs_sv", but no cs_sv_* styles are
#   defined anywhere in the project, so they fall back to Matsu'Py default
#   scrollbar styling (compare archive's own "archive_sv" prefix).
# =============================================================================

# CG Gallery addon
# A browsable gallery of CGs organized by act and chapter, accessed from the archive menu.
# Uses vanilla DDLC CGs as placeholders until original CGs are created.

# ----- Data Definitions -----

init python:
    def cg_key_from_path(image_path):
        """
        Turn an image path into the persistent key that records its unlock.

        THE CG'S IDENTITY IS ITS ART, so the persistent key is derived from the
        path rather than hand-written next to every entry. Two reasons: a catalog
        this long picks up typos and duplicates the moment it needs a second
        column, and a key that is generated cannot silently disagree with the
        image it is supposed to gate. Moved art supplies its pre-move path to
        ``unlock_attr`` below, deliberately freezing the old key so an asset-tree
        cleanup cannot relock a CG on an existing profile.
        """
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
            # `unlock_attr` is the name of a boolean attribute on `persistent`
            # that tracks whether this CG has been unlocked. Passing one is only
            # for a CG that has to share another's unlock; leaving it off derives
            # the key from the art, which is what the whole catalog does.
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
    # Master CG catalog -- organized by act > chapter
    # Uses vanilla DDLC CGs as placeholders
    cg_gallery_catalog = [
        CGAct("Opening", [
            CGChapter("All Opening CGs", [
                CGEntry("Title Drop", "addons/Sick Ass Anime OP/titledropalt.png"),
                CGEntry("Matsuda Performing", "addons/Sick Ass Anime OP/warning2.png"),
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
                CGEntry(
                    "Seer",
                    "assets/cg/seer.png",
                    unlock_attr=cg_key_from_path("mod_assets/cg/seer.png")
                )
            ]),
            CGChapter("Player's Story", [

            ]),
            CGChapter("Tsubaki's Story", [

            ]),
            CGChapter("Asahina's Story", [

            ]),
            CGChapter("Sam's Story", [
                CGEntry(
                    "Ransom",
                    "assets/cg/ransom.png",
                    unlock_attr=cg_key_from_path("mod_assets/cg/ransom.png")
                ),
                CGEntry(
                    "A Girl",
                    "assets/cg/hell.png",
                    unlock_attr=cg_key_from_path("mod_assets/cg/hell.png")
                ),
            ]),
            CGChapter("Mom's Story", [
            ]),
            CGChapter("Monika's Story", [
            ]),
            CGChapter("Kotonoha's Story", [
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
        """Resolve a CG by title (case-insensitive) or by exact image path."""
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

# Main frame entrance/exit
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
# Shows one CG fullscreen. Navigation works by HIDING this screen and re-SHOWING
# it with the neighbouring index, so each image gets a fresh entrance transform.
# Navigation now WRAPS (past the last CG loops to the first and vice versa).
#   cg_list       : the act's flat list of UNLOCKED CGs (built by cg_gallery)
#   current_index : position within cg_list (drives the title, counter + arrows)
screen cg_viewer(cg_list, current_index):
    modal True
    zorder 200

    $ _cg = cg_list[current_index]
    $ _cg_count = len(cg_list)
    $ _cg_prev = (current_index - 1) % _cg_count
    $ _cg_next = (current_index + 1) % _cg_count

    key "game_menu" action Hide("cg_viewer")
    key "K_ESCAPE" action Hide("cg_viewer")

    # Left/right (keyboard) wrap through the unlocked CGs.
    if _cg_count > 1:
        key "K_LEFT" action [Hide("cg_viewer"), Show("cg_viewer", cg_list=cg_list, current_index=_cg_prev)]
        key "K_RIGHT" action [Hide("cg_viewer"), Show("cg_viewer", cg_list=cg_list, current_index=_cg_next)]

    add Solid("#000000f2")

    # CG image centered
    frame:
        background None
        xfill True
        yfill True
        padding (40, 40)
        at cg_viewer_enter

        add _cg.image_path:
            fit "contain"
            xalign 0.5
            yalign 0.5

    # Nav arrows (only if multiple CGs), now wrap-around so both always show.
    if _cg_count > 1:
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
            action [Hide("cg_viewer"), Show("cg_viewer", cg_list=cg_list, current_index=_cg_prev)]

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
            action [Hide("cg_viewer"), Show("cg_viewer", cg_list=cg_list, current_index=_cg_next)]

    # Bottom caption bar: CG title + "N / M" counter.
    frame:
        xalign 0.5
        yalign 1.0
        yoffset -22
        background Solid("#050811d0")
        padding (22, 10)

        hbox:
            spacing 16
            yalign 0.5

            add Solid("#56d7ff") xysize (6, 6) yalign 0.5 at console_blink
            add Solid("#56d7ff44") xysize (2, 20) yalign 0.5
            text "{} / {}".format(current_index + 1, _cg_count) style "cg_viewer_counter" yalign 0.5

    textbutton "Close":
        xalign 1.0
        yalign 0.0
        xoffset -20
        yoffset 15
        style "archive_return_button"   # shared style from archive.rpy
        action Hide("cg_viewer")

# ----- Main Gallery Screen (sidebar + content) -----
# Left: one button per act (cg_gallery_catalog). Right: the selected act's
# chapters and thumbnail grid. `selected_act` is screen-local state.
screen cg_gallery():
    modal True

    # Selected act index
    default selected_act = 0

    use archive_backdrop

    key "game_menu" action Hide("cg_gallery")
    key "K_ESCAPE" action Hide("cg_gallery")

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

            use archive_header("CG GALLERY", Hide("cg_gallery"))

            # Census / readout strip.
            use archive_readout(
                "CG ARCHIVE // {}/{} RECOVERED".format(_cg_unlocked, _cg_total),
                "ACTS {}".format(len(cg_gallery_catalog)))

            hbox:
                spacing 0

                # --- LEFT: act sidebar ------------------------------------
                frame:
                    xsize 240
                    ysize 520
                    style "archive_sidebar_panel"
                    padding (14, 16)

                    vbox:
                        spacing 8

                        for idx, act in enumerate(cg_gallery_catalog):
                            $ _sb_delay = idx * 0.04
                            $ _cg_sb_sel = (idx == selected_act)
                            $ _act_frac = (float(act.unlocked_count) / act.total_count) if act.total_count else 0.0

                            button:
                                xsize 212
                                ysize 78
                                padding (0, 0)
                                hover_sound gui.hover_sound
                                activate_sound gui.activate_sound
                                at cg_sidebar_anim(_sb_delay)
                                action SetScreenVariable("selected_act", idx)

                                # Highlight the currently-selected act.
                                if _cg_sb_sel:
                                    background Solid("#12314af2")
                                    hover_background Solid("#17415fee")
                                else:
                                    background Solid("#07111dcc")
                                    hover_background Solid("#12314aee")

                                hbox:
                                    spacing 0
                                    yfill True

                                    # Selection accent rail (pulses when active).
                                    if _cg_sb_sel:
                                        add Solid("#56d7ff") xysize (4, 78) at enter_m_pip_pulse
                                    else:
                                        add Solid("#0c1a27") xysize (4, 78)

                                    vbox:
                                        spacing 5
                                        yalign 0.5
                                        xoffset 12

                                        if act.total_count == 0:
                                            text act.name style "cg_sidebar_name_locked"
                                            text "NO CGS" style "cg_sidebar_count_locked"
                                        elif act.any_unlocked:
                                            text act.name style "cg_sidebar_name"

                                            # Mini progress bar + count.
                                            fixed:
                                                xysize (184, 8)
                                                add Solid("#091622") xysize (184, 8)
                                                if _act_frac > 0:
                                                    add Solid("#56d7ff") xpos 1 ypos 1 xysize (int(182 * _act_frac), 6)
                                            text "{}/{} CGs".format(act.unlocked_count, act.total_count):
                                                style "cg_sidebar_count"
                                        else:
                                            text act.name style "cg_sidebar_name_locked"
                                            text "LOCKED" style "cg_sidebar_count_locked"

                add Solid("#56d7ff44"):
                    xsize 2
                    ysize 520

                # --- RIGHT: selected act content --------------------------
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

                        # Act header: pip + name + progress bar + subtitle.
                        hbox:
                            spacing 12
                            yalign 0.5

                            add Solid("#56d7ff") xysize (9, 9) yalign 0.5 at console_blink
                            text _sel_act.name style "cg_panel_charname" yalign 0.5

                            null width 1 xfill True

                            if _sel_act.total_count == 0:
                                text "No CGs on record" style "cg_panel_subtitle_locked" yalign 0.5
                            elif _sel_act.any_unlocked:
                                text "{} of {} unlocked".format(_sel_act.unlocked_count, _sel_act.total_count):
                                    style "cg_panel_subtitle"
                                    yalign 0.5
                            else:
                                text "No CGs unlocked yet" style "cg_panel_subtitle_locked" yalign 0.5

                        # Act progress bar (only when the act has CGs).
                        if _sel_act.total_count > 0:
                            fixed:
                                xysize (866, 12)
                                add Solid("#091622") xysize (866, 12)
                                if _act_frac_r > 0:
                                    add Solid("#56d7ff") xpos 2 ypos 2 xysize (int(862 * _act_frac_r), 8)
                                add Solid("#56d7ff55") xysize (866, 1)
                                add Solid("#56d7ff55") xysize (866, 1) ypos 11

                        add Solid("#56d7ff22"):
                            xsize 866
                            ysize 1

                        viewport:
                            style_prefix "archive_sv"
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            pagekeys True
                            xsize 866
                            ysize 396

                            vbox:
                                spacing 20

                                if not _act_chapters:
                                    # Empty-act state (Season 1/2/3 placeholders etc.).
                                    frame:
                                        xfill True
                                        ysize 150
                                        background Solid("#070f18cc")
                                        padding (24, 20)

                                        vbox:
                                            align (0.5, 0.5)
                                            spacing 10
                                            text "NO CGS ON RECORD":
                                                xalign 0.5
                                                style "cg_chapter_title_locked"
                                            text "No CGs have been recovered for this act yet.":
                                                xalign 0.5
                                                style "cg_panel_subtitle_locked"

                                # Chapters (only those with CGs)
                                for chidx, chapter in enumerate(_act_chapters):
                                    $ _ch_delay = chidx * 0.08

                                    vbox:
                                        spacing 12
                                        at cg_chapter_anim(_ch_delay)

                                        # Chapter header
                                        hbox:
                                            spacing 12
                                            yalign 0.5

                                            # Status pip (cyan if any CG unlocked, grey if not)
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
                                        # Outer loop = rows of up to 4; inner loop = cells.
                                        vbox:
                                            spacing 14
                                            xoffset 16

                                            for row_start in range(0, len(chapter.cgs), 4):
                                                hbox:
                                                    spacing 12

                                                    for row_idx, cg in enumerate(chapter.cgs[row_start:row_start + 4]):
                                                        $ cidx = row_start + row_idx
                                                        $ _t_delay = _ch_delay + cidx * 0.05
                                                        # Index of this CG within the act's unlocked list (for the viewer).
                                                        $ _viewer_idx = _act_unlocked.index(cg) if cg.unlocked else 0

                                                        # Cell = clickable tile + caption below it. The tile is the
                                                        # button, so its own hover state drives the highlight.
                                                        vbox:
                                                            spacing 5
                                                            at cg_thumb_anim(_t_delay)

                                                            button:
                                                                xsize 196
                                                                ysize 110
                                                                padding (3, 3)
                                                                hover_sound gui.hover_sound
                                                                activate_sound gui.activate_sound

                                                                # Unlocked -> open viewer; locked -> "not unlocked" dialog.
                                                                if cg.unlocked:
                                                                    background Solid("#07111dcc")
                                                                    hover_background Solid("#12314af2")
                                                                    action Show("cg_viewer",
                                                                        cg_list=_act_unlocked,
                                                                        current_index=_viewer_idx)
                                                                else:
                                                                    background Solid("#050811cc")
                                                                    hover_background Solid("#0a1524cc")
                                                                    action Show("dialog",
                                                                        message="This CG hasn't been unlocked yet.",
                                                                        ok_action=Hide("dialog"))

                                                                if cg.unlocked:
                                                                    add cg.image_path:
                                                                        fit "contain"
                                                                        xalign 0.5
                                                                        yalign 0.5
                                                                else:
                                                                    # Locked placeholder
                                                                    vbox:
                                                                        align (0.5, 0.5)
                                                                        spacing 4

                                                                        text "?":
                                                                            xalign 0.5
                                                                            size 30
                                                                            color "#4f5b67"
                                                                            bold True
                                                                            outlines [(1, "#02040b", 0, 0)]
                                                                        text "LOCKED":
                                                                            xalign 0.5
                                                                            size 11
                                                                            color "#4f5b67"
                                                                            outlines [(1, "#02040b", 0, 0)]

                                        add Solid("#56d7ff16"):
                                            xsize 840
                                            ysize 1

    # Console brackets framing the shell (cohesion with the archive hub).
    use archive_shell_brackets()

# ----- Styles -----
# Cyan-on-near-black palette consistent with the Archive theme.

style cg_title:
    font "assets/fonts/SF Automaton Extended.ttf"
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

# Thumbnail caption (under each grid tile).
style cg_thumb_title:
    font gui.interface_font
    size 12
    color "#c9dbe4"
    text_align 0.5
    xmaximum 192
    outlines [(1, "#02040b", 0, 0)]

style cg_thumb_title_locked:
    font gui.interface_font
    size 12
    color "#41505c"
    text_align 0.5
    xmaximum 192
    outlines [(1, "#02040b", 0, 0)]

# Fullscreen viewer caption bar.
style cg_viewer_title:
    font gui.interface_font
    size 20
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style cg_viewer_counter:
    font gui.interface_font
    size 16
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]
