# =============================================================================
# archive.rpy  --  THE ARCHIVE HUB ("extras" / bonus-content menu)
# =============================================================================
#
# WHAT THIS FILE IS
#   This is the central "Archive" menu reachable from the main menu / game menu.
#   It is a grid of six cards, each card being a gateway to one bonus feature
#   (Roster, CG Gallery, Music Room, Side Stories, Lost Records, Achievements),
#   gated by the persistent.archive_unlocked_* flags defined at the top of this
#   file. Five of the six now ship OPEN -- read the flag block for why, and for
#   where the per-item gating moved to instead.
#
# HOW IT IS REACHED (who opens this screen)
#   - game/screens.rpy line ~424 and ~522:  textbutton "Archive" -> ShowMenu("archive")
#     (so the "archive" screen below is the entry point from the menus).
#
# WHO FLIPS THE UNLOCK FLAGS (the persistent.archive_unlocked_* below)
#   - game/story/season1/0531.rpy          : end of Chapter 0.5, opens the Music Room.
#   - Developer Date Jump/dev_date_jump.rpy: the ALL SIDE CONTENT dev switch.
#
# WHERE THE TARGET SCREENS LIVE (what each card opens)
#   - "roster_view_screen"  -> game/addons/Roster View/roster_view.rpy
#   - "cg_gallery"          -> game/addons/CG View/cg_gallery.rpy
#   - "music_room"          -> game/addons/Music Room/music_room.rpy
#   - "character_stories"   -> game/addons/Character Stories/char_stories.rpy
#   - "lost_records"        -> game/addons/Lost Records View/lost_records.rpy
#   - "dialog"              -> generic OK dialog screen (used for locked cards)
#
# EXTERNAL SYMBOLS THIS FILE LEANS ON (defined elsewhere)
#   - image "bg ether"             : background art (defined in definitions/images).
#   - transform menu_scanline_slow : scrolling-scanline effect (game/screens.rpy).
#   - label enter_m_sick_ass_anime_op + enter_m_op_cleanup_screens()
#                                  : the OP intro sequence (game/addons/Sick Ass Anime OP/op.rpy),
#                                    reused here by the "Replay OP" button.
#   - gui.hover_sound / gui.activate_sound : standard UI sounds (game/gui.rpy).
#   - BGM tracks under mod_assets/bgm/ (roster_place, canyoufeel).
# =============================================================================

# Custom screens/labels for archive

# -----------------------------------------------------------------------------
# UNLOCK FLAGS
# One persistent bool per archive feature. `default` means "set this once on a
# fresh save and never overwrite it after". These are the single source of truth
# for whether a card is playable; story/dev code only ever flips these.
# NOTE: archive_unlocked_poems exists but currently has no card in archive_items
#       (poems are surfaced elsewhere -- see game/addons/poem_display.rpy).
#
# WHAT IS GATED AND WHAT IS NOT
#   The SHELL is not the reward. Five of the six panels ship open on a brand new
#   save, because an Archive that is six identical "???" cards tells a first-time
#   player nothing about what is in there or how to earn it. What is actually
#   withheld lives one level DOWN, per item, and is visibly incomplete instead of
#   invisible:
#       Roster        -- slot per character, grayed until she is met
#                        (Roster View/roster_view.rpy)
#       CG Gallery    -- entry per CG, grayed until it has been on screen
#                        (CG View/cg_gallery.rpy)
#       Side Stories  -- rows stay HIDDEN, not grayed, because a title is a
#                        spoiler (Character Stories/char_stories.rpy)
#       Lost Records  -- unconditional, all of it, from the first launch
#       Achievements  -- a roadmap/checklist, so showing it locked is pointless
#   The Music Room is the one whole-panel reward left, because a soundtrack is
#   the thing you go back for once the story is over: it opens on clearing the
#   main campaign, which for now means the end of Chapter 0.5 (0531.rpy).
# -----------------------------------------------------------------------------
default persistent.archive_unlocked_roster = True
default persistent.archive_unlocked_cgs = True
default persistent.archive_unlocked_music = False
default persistent.archive_unlocked_poems = False
default persistent.archive_unlocked_character_stories = True
default persistent.archive_unlocked_lost_records = True
default persistent.archive_unlocked_achievements = True
# The card binder (addons/Matsucoin Currency and Gacha/mc_collection.rpy).
# Ships open like the other five: what is withheld is the CARDS, which are
# visibly empty slots until they are pulled. No migration entry is needed --
# `default` writes whenever the stored value is None, which is exactly what an
# older profile has for a flag that did not exist when it was written.
default persistent.archive_unlocked_cards = True

# MIGRATION (2026-08): the five flags above used to default False and be flipped
# at the end of Chapter 0.5. `default persistent.x` only writes when the value is
# currently None (renpy/common/000namespaces.rpy, _PersistentNamespace.set_default),
# so an existing profile carries its stored False forever and would sit on a
# fully locked Archive. Force them once, and remember that we did.
default persistent.archive_open_shell_migrated = False

# init 50: `default` statements execute in the init phase at priority 0, so this
# has to run after them or it would write flags that are about to be defaulted.
init 50 python:
    if not persistent.archive_open_shell_migrated:
        for _key in (
            "archive_unlocked_roster",
            "archive_unlocked_cgs",
            "archive_unlocked_character_stories",
            "archive_unlocked_lost_records",
            "archive_unlocked_achievements",
        ):
            setattr(persistent, _key, True)
        persistent.archive_open_shell_migrated = True

# -----------------------------------------------------------------------------
# DATA-DRIVEN ARCHIVE CARD TABLE
# The archive grid is built by looping over `archive_items` (see screen archive
# below). Keeping the cards as data instead of hand-written buttons means adding
# a feature = adding one tuple here.
# -----------------------------------------------------------------------------
# Data-driven archive item definitions
init python:
    # Each entry: (label, unlock_persistent_key, unlocked_action, icon)
    # unlock_persistent_key of None means always locked (placeholder)
    archive_items = [
        ("Roster",       "archive_unlocked_roster",            Show("roster_view_screen"), "mod_assets/dump/icon_placeholder.png"),
        ("CG Gallery",   "archive_unlocked_cgs",               Show("cg_gallery"),         "mod_assets/dump/icon_placeholder.png"),
        ("Music Room",   "archive_unlocked_music",             Show("music_room"),         "mod_assets/dump/icon_placeholder.png"),
        ("Side Stories", "archive_unlocked_character_stories", Show("character_stories"),  "mod_assets/dump/icon_placeholder.png"),
        ("Lost Records", "archive_unlocked_lost_records",      Show("lost_records"),       "mod_assets/dump/icon_placeholder.png"),
        ("Achievements", "archive_unlocked_achievements",      Show("achievements"),       "mod_assets/dump/icon_placeholder.png"),
        ("Cards",        "archive_unlocked_cards",             Show("mc_collection"),      "mod_assets/dump/icon_placeholder.png"),
    ]

    # Modules that ship unlocked rather than gated behind story progress. They
    # are excluded from archive_unlock_keys() by default so "bring a module
    # online" progress counts only what the player actually earns -- which, since
    # the shell opened up (see the flag block above), is the Music Room alone.
    # Anything listed here is still a real card; it is just not a trophy.
    archive_ungated_keys = frozenset((
        "archive_unlocked_roster",
        "archive_unlocked_cgs",
        "archive_unlocked_character_stories",
        "archive_unlocked_lost_records",
        "archive_unlocked_achievements",
        "archive_unlocked_cards",
    ))

    # The single source of truth for "which persistent flags gate the Archive".
    # Anything that needs the list (achievement predicates, the dev all-content
    # switch) asks here instead of keeping its own copy, so adding a module is
    # still a one-tuple edit to archive_items above.
    def archive_unlock_keys(gated_only=True):
        return tuple(
            key for _label, key, _action, _icon in archive_items
            if key and not (gated_only and key in archive_ungated_keys)
        )

    # Resolve a card's lock state. `key` is the *string name* of a persistent
    # attribute (e.g. "archive_unlocked_roster"); we read it dynamically with
    # getattr so the table above can stay pure data. A None key (the "???"
    # placeholder) is always treated as locked.
    def archive_is_unlocked(key):
        if key:
            return getattr(persistent, key, False)
        return False

    # -------------------------------------------------------------------------
    # ArchivePortraitCrop: the portrait window's clipper.
    #
    # Scales `img` so it COVERS a w x h window (times `zoom`), then crops that
    # scaled render back to exactly w x h -- centred horizontally, `focus` of the
    # way down vertically. The result is exactly window-sized, so nothing can
    # bleed past the frame.
    #
    # WHY NOT A VIEWPORT. A viewport clips too, and xinitial/yinitial can pan it,
    # but that pan lives in the viewport's SCROLL STATE -- and Matsu'Py has a
    # viewport inherit the offsets of the viewport it replaces:
    #     if replaces is not None:
    #         self.xoffset = replaces.xoffset
    #         self.yoffset = replaces.yoffset
    # (renpy/display/viewport.py). Re-showing a screen -- exactly what paging
    # between dossiers does -- therefore keeps the PREVIOUS character's pan, and
    # xinitial/yinitial never re-apply. Measured: paging from a 2:3 sprite to
    # Monika put her figure at x[147..338] instead of x[99..329], shoved right and
    # clipped, while opening her directly was correct. This is stateless, so a
    # re-shown portrait and a freshly shown one are pixel-identical.
    #
    # WHY TWO NESTED TRANSFORMS. A Transform applies `crop` BEFORE its own
    # size/fit (see cropping() then the size block in display/accelerator.pyx), so
    # crop and fit on the SAME transform crops the source and then scales the crop
    # up -- which overflows the frame. The inner transform scales, the outer crops.
    #
    # `aspect` is the SOURCE's width/height. It is needed because it decides which
    # axis the cover fit ran out of, and therefore how much overflow there is to
    # crop away. Every character sprite is pre-normalised to 640x960 by
    # def_characters.rpy, which is the default; Monika's DDLC layeredimage is a
    # 960x960 square, so she passes 1.0.
    #
    # `scale` IS NOT A RAW ZOOM -- it is how big this subject should read RELATIVE
    # to a standard 640x960 sprite, and the actual zoom is derived from the window.
    # That indirection is necessary because how much of a source a cover fit shows
    # depends on the window's aspect as well as the source's: a 2:3 sprite in the
    # 300x360 dossier shows 80% of its height, but in a 52x52 drawer chip it shows
    # only 67%. A square source shows 100% in both. So one fixed zoom that matches
    # Monika to the cast in the dossier leaves her too small in the chips -- which
    # is exactly what happened. Normalising against the reference aspect makes
    # `scale` mean the same thing in every window, and leaves every standard sprite
    # at exactly zoom 1.0 (the ratio below is 1 when aspect == reference).
    # -------------------------------------------------------------------------
    ARCHIVE_PORTRAIT_REF_ASPECT = 640.0 / 960.0

    # xfocus is 0..1 across the width, defaulting to 0.5 (dead centre), which is
    # what every existing caller was getting implicitly. It only starts to
    # matter once you crop in far enough that the subject can leave the frame
    # sideways: at dossier scale a 2:3 source shows its full width so there is
    # nothing to pan, but a head-shot crop of a full-body figure shows about a
    # third of it, and a character who stands off-centre (or holds a weapon out
    # to one side) is simply not in the middle of their own art.
    def ArchivePortraitCrop(img, w, h, focus=0.0, scale=1.0, aspect=(640.0 / 960.0), xfocus=0.5):
        w = float(w)
        h = float(h)
        aspect = float(aspect) or 1.0
        ref = ARCHIVE_PORTRAIT_REF_ASPECT

        # How tall a cover fit renders each source in THIS window (source
        # normalised to 1.0 tall). The ratio is the window-dependent correction.
        ref_mul = max(w / ref, h)
        own_mul = max(w / aspect, h)
        zoom = (ref_mul / own_mul) * max(0.05, float(scale))

        box_w = w * zoom
        box_h = h * zoom

        # Cover into (box_w, box_h), measured against a source normalised to 1.0
        # tall, so the scaled render is (mul * aspect) x mul.
        mul = max(box_w / aspect, box_h)
        frac_w = min(1.0, w / (mul * aspect))
        frac_h = min(1.0, h / mul)

        crop_x = (1.0 - frac_w) * max(0.0, min(1.0, float(xfocus)))
        crop_y = (1.0 - frac_h) * max(0.0, min(1.0, float(focus)))

        scaled = Transform(
            img,
            fit="cover",
            xysize=(int(round(box_w)), int(round(box_h))),
        )

        return Transform(
            scaled,
            crop=(crop_x, crop_y, frac_w, frac_h),
            crop_relative=True,
        )

# -----------------------------------------------------------------------------
# "REPLAY OP" ENTRY POINT
# Triggered by the corner button in `screen archive`. Because it is launched via
# renpy.call_in_new_context (see the button's action), this label runs as its
# own self-contained context: hide the archive, play the full OP sequence, clean
# up the OP's leftover screens, then reopen the archive with menu BGM.
#   - enter_m_sick_ass_anime_op  : the OP label        (Sick Ass Anime OP/op.rpy)
#   - enter_m_op_cleanup_screens : the OP teardown func (Sick Ass Anime OP/op.rpy)
# -----------------------------------------------------------------------------
label enter_m_archive_replay_op:
    $ renpy.hide_screen("archive")
    call enter_m_sick_ass_anime_op from _call_enter_m_sick_ass_anime_op
    $ enter_m_op_cleanup_screens()
    scene black
    $ enter_m_menu_music(audio.roster_place)
    $ renpy.show_screen("archive")
    return

# -----------------------------------------------------------------------------
# TRANSFORMS (animation)
# -----------------------------------------------------------------------------
# Per-card entrance + hover. `delay` staggers each card so they cascade in (the
# screen passes i*0.07). Fades up from below with an easein_back overshoot, then
# bobs up slightly on hover.
# Combined entrance + hover for archive cards
transform archive_card_anim(delay=0.0):
    alpha 0.0
    yoffset 30
    subpixel True
    pause delay
    easein_back 0.45 alpha 1.0 yoffset 0
    on idle:
        ease 0.15 yoffset 0
    on hover:
        ease 0.15 yoffset -5

# Whole-panel entrance/exit: drops in from above on show, lifts out and fades on
# hide. Applied to the main archive frame.
# Entrance for the main frame
# The archive shell's entrance: drop in from `rise` px over `secs`, lift back
# out by `fall` px on the way to hidden. Every sub-screen (Roster, Music Room,
# CG Gallery, Lost Records, Side Stories) used to keep its own near-identical
# copy that differed only in these three numbers, which meant retiming the shell
# entrance was a six-file edit -- pass the numbers instead of forking the ATL.
transform archive_frame_enter(rise=40, secs=0.45, fall=25, out=0.25):
    on show:
        alpha 0.0
        yoffset -rise
        easein_back secs alpha 1.0 yoffset 0
    on hide:
        alpha 1.0
        easeout_quad out alpha 0.0 yoffset -fall

# Locked-card "corrupted signal" flicker -- a subtle periodic opacity dip with a
# tiny horizontal jitter, so locked modules read as unstable/encrypted. Applied
# to the placeholder icon of locked cards.
transform enter_m_locked_flicker:
    subpixel True
    block:
        alpha 1.0 xoffset 0
        pause 1.7
        alpha 0.66
        pause 0.04
        alpha 1.0
        pause 0.05
        alpha 0.85 xoffset 1
        pause 0.03
        alpha 1.0 xoffset 0
        pause 2.4
        repeat

# Accent rule that wipes out from its left edge. Reused by the credits section
# rule so it re-plays whenever the selected section changes.
transform enter_m_accent_grow:
    subpixel True
    xanchor 0.0
    xzoom 0.0
    easeout 0.42 xzoom 1.0

# Gentle pulse for status pips that should breathe rather than hard-blink.
# Also reused by sub-screens as the "selected row" accent-rail pulse.
transform enter_m_pip_pulse:
    subpixel True
    alpha 0.55
    block:
        easeout 0.9 alpha 1.0
        easein 0.9 alpha 0.55
        repeat

# Reusable portrait-window scanline. `h` is the window height so the thin bar
# sweeps from the top of the frame to the bottom and loops. Parameterised so any
# sub-screen (roster detail, lost records, etc.) can share one look regardless of
# its portrait size. Pair it with a clipping viewport so it never bleeds out.
transform archive_scanline(h=156):
    subpixel True
    ypos 0
    alpha 0.0
    linear 0.2 alpha 1.0
    block:
        ypos 0
        linear 2.6 ypos h
        pause 0.5
        repeat

# -----------------------------------------------------------------------------
# BACKDROP
# Shared background layer: the "ether" art, a dark tint, and a thin animated
# scanline strip (menu_scanline_slow lives in game/screens.rpy).
# -----------------------------------------------------------------------------
screen archive_backdrop():
    add "bg ether"
    add Solid("#00000050")
    add Solid("#75f7ff1f") xysize (1280, 2) at menu_scanline_slow

# -----------------------------------------------------------------------------
# REUSABLE HEADER
# A titled header bar with an accent rule and a "Return" button. Parameterised so
# sub-screens (roster/music/etc.) can reuse the same look:
#   title         : heading text
#   return_action : action list run by the Return button
#   return_text   : button caption (defaults to localized "Return")
# -----------------------------------------------------------------------------
screen archive_header(title, return_action, return_text=_("Return")):
    hbox:
        xfill True
        ysize 64

        frame:
            style "archive_header_title_frame"
            at transform:
                on show:
                    alpha 0.0
                    xoffset -18
                    easeout 0.35 alpha 1.0 xoffset 0

            hbox:
                spacing 13
                yalign 0.5

                add Solid("#56d7ff") xysize (11, 11) yalign 0.5 at console_blink
                text title style "archive_title"

        add Solid("#56d7ff") xysize (3, 46) yalign 0.5 xoffset 16 at enter_m_pip_pulse

        null width 1 xfill True

        textbutton return_text:
            style "archive_return_button"
            yalign 0.5
            action return_action
            at transform:
                on show:
                    alpha 0.0
                    pause 0.18
                    ease 0.25 alpha 1.0

# -----------------------------------------------------------------------------
# REUSABLE CENSUS / READOUT STRIP
# The thin "SUBSYSTEM // x/y ONLINE ......... STATUS" line the archive hub and the
# Side Stories screen both show under their header. Factored out here so every
# sub-screen renders an identical strip:
#   left_text  : primary readout (left, next to a blinking pip)
#   right_text : secondary readout (right-aligned); omit for none
#   width      : rail width (defaults to the shell content width)
#   rule       : draw the cyan hairline under the strip (default True)
# -----------------------------------------------------------------------------
# NB the layout here is a `fixed` with explicit xpos/xanchor, NOT an hbox with a
# greedy `null xfill`. Measured in an isolated harness: giving a box an explicit
# `xsize` stops it packing its children to the left -- it spreads them instead --
# so `hbox: xsize width` + `null width 1 xfill True` did NOT pin the right-hand
# readout to the right edge; it floated both halves toward the middle (which is
# why this strip used to read as a pip, a gap, then the text). `text_align` on a
# Text is also inert here. A fixed with xanchor 1.0 is exact to the pixel.
# `right_slot=True` right-aligns a TRANSCLUDED block instead of a plain string,
# for the screens whose right-hand side is a widget (Achievements' per-tier
# tally). It's the same 10px-precise layout either way, which is the point --
# a caller that needs a richer right side extends the strip, it doesn't fork it.
# `text_style` is for the one sub-screen with a deliberately different typeface
# (Side Stories' dossier face) -- it shares the LAYOUT without being forced into
# the default archive face.
screen archive_readout(left_text, right_text="", width=1150, rule=True, right_slot=False, slot_spacing=20, text_style="archive_meta_text"):
    vbox:
        xalign 0.5
        spacing 8

        fixed:
            xsize width
            ysize 20

            add Solid("#56d7ff") xysize (6, 6) xpos 0 yalign 0.5 at console_blink
            text left_text style text_style xpos 16 yalign 0.5

            if right_text:
                text right_text style text_style xanchor 1.0 xpos width yalign 0.5

            if right_slot:
                # An hbox with NO xsize shrinks to fit, so xanchor 1.0 at
                # xpos width lands its right edge exactly on the rule's.
                hbox:
                    spacing slot_spacing
                    xanchor 1.0
                    xpos width
                    yalign 0.5
                    transclude

        if rule:
            add Solid("#56d7ff66") xysize (width, 2)

# -----------------------------------------------------------------------------
# REUSABLE PORTRAIT WINDOW
# A framed sprite window with the archive's technical dressing: dark backing, a
# sweeping scanline, and cyan hairlines top and bottom.
#   img       : sprite/displayable to show
#   w, h      : window size in px
#   fit_mode  : "cover"   -- the art FILLS the window and the overflow is clipped
#                            (what character portraits want: no dead gutters, and
#                            every subject at the same scale)
#               "contain" -- the whole image, letterboxed and centred (what a
#                            logo or a record thumbnail wants)
#   gray      : desaturate + dim (used for dead/locked subjects)
#   focus     : 0.0..1.0, WHERE in the over-tall art the window sits. Only
#               meaningful for "cover". 0.0 = top of the art (heads), 1.0 =
#               bottom. Ignored by "contain", which is always centred.
#   scale     : how big this subject should read RELATIVE to a standard 640x960
#               sprite. 1.0 = the cast default. Only meaningful for "cover"; the
#               overflow it creates is what `focus` then pans through. It is NOT a
#               raw zoom -- see ArchivePortraitCrop for why the window aspect has
#               to be folded in, and why a fixed zoom cannot be right in both the
#               300x360 dossier and a 52x52 chip.
#   aspect    : the SOURCE image's width/height. Defaults to the 640x960 every
#               character sprite is normalised to (def_characters.rpy); Monika's
#               DDLC layeredimage is a 960x960 square, so she passes 1.0. See
#               ArchivePortraitCrop for why this is needed.
#   locked    : REDACT the subject. `img` is not drawn at all -- the window keeps
#               its frame, backing and scanline but shows the hub's unavailable
#               placeholder under enter_m_locked_flicker, and its hairlines go
#               grey. Use it for a subject the player has not met: a desaturated
#               sprite is still a recognisable sprite, so greying is not
#               concealment. Nothing else about the window changes, which is the
#               point -- an unmet slot is visibly a slot, the same size and in
#               the same place it will occupy once it is filled.
#
# WHY "cover" NEEDS A CLIPPER AT ALL
#   Matsu'Py's `fit` only chooses a uniform SCALE -- it does not crop. So a "cover"
#   sprite renders LARGER than the window in one axis and simply overhangs it: a
#   960x960 portrait in a 300x360 frame drew 360x360 and bled 30px out of each
#   side, over the hairlines and into the panel next door. ArchivePortraitCrop
#   (top of this file) does the scale-then-crop so the result is exactly window
#   sized. It replaced a clipping viewport, which worked but kept the PREVIOUS
#   portrait's pan whenever the screen was re-shown -- read the comment there
#   before reaching for a viewport again. "contain" keeps the plain `fixed`,
#   because there the child is never bigger than the frame anyway.
# -----------------------------------------------------------------------------
screen archive_portrait(img, w, h, fit_mode="contain", gray=False, focus=0.0, scale=1.0, aspect=(640.0 / 960.0), locked=False):
    fixed:
        xysize (w, h)

        add Solid("#07101add") xysize (w, h)

        if locked:
            # The placeholder is sized against the window rather than pinned at
            # the hub's 80x112, so the same redaction reads right in a 300px
            # dossier and a 118px People chip.
            $ _ap_icon_w = int(w * 0.34)
            $ _ap_icon_h = int(w * 0.48)
            add Transform("mod_assets/dump/unavailable_icon_placeholder.png", size=(_ap_icon_w, _ap_icon_h)):
                align (0.5, 0.5)
                at enter_m_locked_flicker
        elif fit_mode == "cover":
            if gray:
                add ArchivePortraitCrop(img, w, h, focus, scale, aspect):
                    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.12)
            else:
                add ArchivePortraitCrop(img, w, h, focus, scale, aspect)
        else:
            if gray:
                add img:
                    fit fit_mode
                    xysize (w, h)
                    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.12)
            else:
                add img:
                    fit fit_mode
                    xysize (w, h)

        add Solid("#76e6ff18") xysize (w, 2) at archive_scanline(h - 2)
        add Solid("#33414d" if locked else "#56d7ff66") xysize (w, 2)
        add Solid("#33414d" if locked else "#56d7ff66") xysize (w, 2) ypos (h - 2)

# -----------------------------------------------------------------------------
# THE SHELL'S CORNER BRACKETS
# Every archive sub-screen sits in an `archive_shell_frame` (1200x690, styled
# below) and draws console brackets around it. Those four numbers ARE the frame,
# so they live here once instead of being restated at each sub-screen -- an
# earlier round of copies drifted to a narrower 1160 and clipped the right edge.
# `console_brackets` itself stays parameterised for the genuinely bespoke
# callers (pause menu, splash, main menu).
# -----------------------------------------------------------------------------
screen archive_shell_brackets():
    use console_brackets(40, 15, 1200, 690, "#56d7ff7a", 24, 2)

# -----------------------------------------------------------------------------
# THE ARCHIVE SCREEN (main hub)
# `tag menu` => it participates in the menu screen group (showing another menu
# screen auto-replaces this one). Built from the data table archive_items above.
# -----------------------------------------------------------------------------
screen archive():
    tag menu

    # Re-sync achievements so derived unlocks (a fight cleared, a side story
    # recovered) toast the moment the player lands back on the hub.
    #
    # The archive theme is asked for HERE rather than later, because the ask has
    # to happen in the same interaction that starts the move: the main-menu
    # track then fades out across the black beat of enter_m_menu_shutter and
    # roster_place starts, at full volume, on the frame this screen appears.
    # See menu_transitions.rpy section 6.
    on "show" action [EnterMMenuMusic(audio.roster_place), Function(ach_refresh)]
    on "replace" action [EnterMMenuMusic(audio.roster_place), Function(ach_refresh)]

    use archive_backdrop

    # Back/Escape both bail out: restore menu BGM, then Return() to the caller.
    # The track is handed over with a fade rather than cut -- see section 6 of
    # menu_transitions.rpy for why a hard cut here stuttered the way out.
    key "game_menu" action [EnterMMenuMusic(audio.canyoufeel), Return()]
    key "K_ESCAPE" action [EnterMMenuMusic(audio.canyoufeel), Return()]

    # Live module census for the subsystem readout.
    $ a_total = len(archive_items)
    $ a_online = sum(1 for _it in archive_items if archive_is_unlocked(_it[1]))

    frame:
        style "archive_frame"
        at archive_frame_enter()

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 10

            # Reuse the header defined above; its Return mirrors the key actions.
            use archive_header("ARCHIVE", [EnterMMenuMusic(audio.canyoufeel), Return()])

            # Subsystem readout + accent rail -- the same strip every sub-screen
            # uses, so the hub is styled by the same definition it exports.
            use archive_readout(
                "ARCHIVE SUBSYSTEM // %d/%d MODULES ONLINE" % (a_online, a_total),
                "SIGNAL LOCKED // 0x4D",
                1100)

            # Card wall, 4 across. Chunked into rows here rather than handed to
            # a Matsu'Py `grid`, which demands EXACTLY rows*cols children -- the
            # old `grid 3 2` was hardwired to a six-module Archive and adding
            # the seventh would have meant either a dead filler cell or an
            # every-time edit to two numbers. This way "adding a feature = adding
            # one tuple" (see the table above) stays true at 7, 8 and 9 modules.
            # Two rows of 4 occupy exactly the height two rows of 3 did, so the
            # shell's geometry is unchanged.
            python:
                _a_cols = 4
                _a_all = list(enumerate(archive_items))
                _a_rows = [_a_all[_i:_i + _a_cols]
                        for _i in range(0, len(_a_all), _a_cols)]

            vbox:
                spacing 25
                xalign 0.5

                for _a_row in _a_rows:
                    # xalign 0.0, so a short final row lines its cards up under
                    # the first row's left edge instead of centring them into a
                    # pyramid. The VBOX is what is centred (above), so the wall
                    # as a whole still sits in the middle of the shell.
                    hbox:
                        spacing 25
                        xalign 0.0

                        for i, item in _a_row:
                            # Unpack the data tuple and resolve its lock state.
                            $ a_label, a_key, a_action, a_icon = item
                            $ a_unlocked = archive_is_unlocked(a_key)
                            $ a_delay = i * 0.07   # staggered entrance delay per card
                            $ a_id = "MOD_%02d" % (i + 1)

                            button:
                                style "archive_item_button"
                                at archive_card_anim(a_delay)

                                # Unlocked + has an action -> run it; otherwise show
                                # the "not unlocked yet" dialog (generic "dialog").
                                if a_unlocked and a_action:
                                    action a_action
                                else:
                                    action Show("dialog", message="This feature hasn't been unlocked yet.", ok_action=Hide("dialog"))

                                vbox:
                                    xsize 214
                                    yalign 0.5
                                    spacing 5

                                    # Slot ID + live status pip, pinned to the card's
                                    # two edges (fixed + xanchor, not a greedy null --
                                    # see the note on archive_readout).
                                    fixed:
                                        xsize 214
                                        ysize 16

                                        text "[a_id]" style "archive_card_id" xpos 0 yalign 0.5

                                        if a_unlocked:
                                            add Solid("#56d7ff") xysize (7, 7) xanchor 1.0 xpos 214 yalign 0.5 at console_blink
                                        else:
                                            add Solid("#4f5b67") xysize (7, 7) xanchor 1.0 xpos 214 yalign 0.5

                                    add Solid("#56d7ff" if a_unlocked else "#33414d"):
                                        xsize 214
                                        ysize 2

                                    # Visual fork: real card (icon + label + AVAILABLE)
                                    # vs. locked (flickering mystery icon + ??? + LOCKED).
                                    # NB: a bare `fixed` here is greedy and blows the
                                    # card up -- add the icon directly at a fixed size.
                                    if a_unlocked and a_icon:
                                        add Transform(a_icon, size=(80, 112)) xalign 0.5
                                        text a_label style "archive_item_text" xalign 0.5
                                        text "AVAILABLE" style "archive_item_status" xalign 0.5
                                    else:
                                        add Transform("mod_assets/dump/unavailable_icon_placeholder.png", size=(80, 112)) xalign 0.5 at enter_m_locked_flicker
                                        text "???" style "archive_locked_text" xalign 0.5
                                        text "LOCKED" style "archive_locked_status" xalign 0.5

            # Subsystem footer status line.
            fixed:
                xsize 1100
                ysize 16

                add Solid("#345a6b") xysize (5, 5) xpos 0 yalign 0.5
                text "ARCHIVE.SYS :: STATUS NOMINAL" style "archive_footer_text" xpos 13 yalign 0.5
                text "CONNECTION STABLE" style "archive_footer_text" xanchor 1.0 xpos 1100 yalign 0.5

    # Console brackets framing the archive panel.
    use console_brackets(60, 28, 1160, 664, "#56d7ff7a", 24, 2)

    # Floating corner button: relaunch the opening movie. Uses call_in_new_context
    # so the OP plays in its own context and returns here cleanly (see the
    # enter_m_archive_replay_op label above).
    textbutton _("Replay OP"):
        style "archive_corner_button"
        xalign 0.985
        yalign 0.025
        action Function(renpy.call_in_new_context, "enter_m_archive_replay_op")
        at transform:
            on show:
                alpha 0.0
                xoffset 14
                pause 0.22
                easeout 0.22 alpha 1.0 xoffset 0

# =============================================================================
# STYLES
# Visual theme for the archive. Color language: near-black panels (#050811 /
# #07111d) with cyan (#56d7ff) accents and a red drop-shadow on titles. Several
# styles use `is <parent>` to inherit and tweak (e.g. corner button is the
# return button at a different size). archive_shell_frame / archive_panel* /
# archive_sv_vscrollbar are shared building blocks the sub-screens reuse.
# =============================================================================
style archive_frame:
    xalign 0.5
    yalign 0.5
    xsize 1160
    ysize 664
    background Solid("#050811e8")
    padding (30, 22)

style archive_shell_frame is archive_frame:
    xsize 1200
    ysize 690
    padding (24, 16)

style archive_header_title_frame:
    background Solid("#07111dcc")
    padding (24, 12)
    yalign 0.5

style archive_title:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 40
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (2, "#ff315bcc", 1, 1)]

style archive_item_button:
    xysize (250, 230)
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    selected_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (18, 12)

style archive_item_text:
    font gui.interface_font
    color "#dff8ff"
    size 22
    xalign 0.5
    text_align 0.5
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style archive_item_status:
    font gui.interface_font
    color "#56d7ff"
    size 12
    xalign 0.5
    text_align 0.5
    outlines [(1, "#02040b", 0, 0)]

style archive_locked_text:
    font gui.interface_font
    color "#687787"
    size 26
    xalign 0.5
    text_align 0.5
    bold True
    outlines [(2, "#02040b", 0, 0)]

style archive_locked_status is archive_item_status:
    color "#4f5b67"

style archive_meta_text is gui_text:
    font gui.interface_font
    size 12
    color "#7fcfe0"
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

style archive_footer_text is gui_text:
    font gui.interface_font
    size 10
    color "#5d7886"
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

style archive_card_id is gui_text:
    font gui.interface_font
    size 11
    color "#56d7ff"
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

style archive_return_button:
    xsize 126
    ysize 42
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (15, 8)

style archive_return_button_text:
    font gui.interface_font
    color "#dff8ff"
    hover_color "#ffffff"
    size 22
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style archive_corner_button is archive_return_button:
    xsize 150
    ysize 38
    background Solid("#07111dee")
    hover_background Solid("#12314af2")

style archive_corner_button_text is archive_return_button_text:
    size 18

style archive_panel:
    background Solid("#07101add")
    padding (18, 18)

style archive_sidebar_panel is archive_panel:
    background Solid("#050811e8")

style archive_panel_label:
    font gui.interface_font
    color "#f4fbff"
    size 20
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style archive_panel_small:
    font gui.interface_font
    color "#9fc9d6"
    size 14
    outlines [(1, "#02040b", 0, 0)]

style archive_sv_vscrollbar:
    xsize 6
    base_bar Frame(Solid("#102338"), 0, 0, 0, 0)
    thumb Frame(Solid("#56d7ff"), 2, 2, 2, 2)
    unscrollable "hide"

# Shared status-chip text styles. Draw a chip as a small frame with a Solid
# background + one of these text styles, so every sub-screen's "PLAY >" / "LOCKED"
# badges read identically (Side Stories, Lost Records, Roster, Achievements and
# the Card binder all use these two directly):
#   on  -> filled BRIGHT chip, near-black text
#   off -> muted grey chip, dim text
#
# WHY THE "on" INK STAYS NEAR-BLACK. It looks like it ought to be light, because
# every other piece of text in the Archive is. It must not be: this style is
# only ever stamped on chips whose fill is BRIGHT -- achievement tiers (bronze
# #b9793f, silver #9fb0bd, gold #e0ac33, platinum #5fd3ef) and the cyan status
# chips. Measured contrast of #04121a on those fills is 5.3:1 / 8.5:1 / 9.1:1 /
# 10.9:1 / 11.4:1; swapping to a near-white #f4fbff drops the same pairs to
# 3.4:1 / 2.1:1 / 2.0:1 / 1.7:1 / 1.6:1, i.e. strictly worse everywhere, and an
# outline cannot honestly rescue a 1.6:1 fill.
#
# A dark glyph on a MUTED fill is the combination that reads badly -- that is
# what made the card binder's R chip (steel #6f7d95, 4.7:1) hard to read. The
# fix there was to invert the chip itself (dark plate, bright tier ink) rather
# than to relight this style; see mc_rarity_chip in the Matsucoin addon. Invert
# the CHIP, never this ink, if another muted-fill badge shows up.
style archive_chip_on_text:
    font gui.interface_font
    size 13
    color "#04121a"
    bold True

style archive_chip_off_text:
    font gui.interface_font
    size 12
    color "#6f7d88"
    bold True
    outlines [(1, "#02040b", 0, 0)]

# -----------------------------------------------------------------------------
# PLACEHOLDER SCREENS
# The CG Gallery screen referenced by the "CG Gallery" card is NOT here; it is
# defined in addons/CG View/cg_gallery.rpy. poem_archive below is a stub
# "coming soon" screen kept for future use.
# -----------------------------------------------------------------------------
# Placeholder screens for features
# CG Gallery screen is defined in addons/CG View/cg_gallery.rpy

screen poem_archive():
    tag menu
    frame:
        xalign 0.5
        yalign 0.5
        padding (50, 50)

        vbox:
            text "Poem Archive - Coming Soon" size 32
            null height 20
            textbutton "Return" action Return()
