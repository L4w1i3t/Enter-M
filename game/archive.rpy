# Archive hub and shared catalog UI. archive_items defines the seven doors
# and their persistent unlock keys. Six doors start open; Music Room opens
# after Chapter 0.5. Individual galleries/rosters/stories own their item gates.
# archive_unlocked_poems is retained state but has no card in archive_items.
# Shared portrait crops use original image dimensions, independent of story
# framing. Replay OP uses the OP's entry label and cleanup helpers.

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
    def archive_start_isolated_content(label_name):
        """Start standalone Archive content with a clean per-game store."""
        if not label_name or not renpy.has_label(label_name):
            if config.developer:
                raise Exception("archive_start_isolated_content: unknown label %r." % (label_name,))
            return None

        # Start(label) only jumps out of the menu context. From the in-game
        # Archive that lands in the loaded save and exposes all of its per-save
        # state to the standalone story. A full restart restores Ren'Py's clean
        # stores first, then jumps directly to the requested content label.
        renpy.full_restart(label=label_name, save=False)

    # Each entry: (label, unlock_persistent_key, unlocked_action, icon)
    # unlock_persistent_key of None means always locked (placeholder)
    archive_items = [
        ("Roster",       "archive_unlocked_roster",            Show("roster_view_screen", transition=enter_m_menu_doorway), "assets/gui/archive_panels/roster.png"),
        ("CG Gallery",   "archive_unlocked_cgs",               Show("cg_gallery", transition=enter_m_menu_doorway),         "assets/gui/archive_panels/cg_gallery.png"),
        ("Music Room",   "archive_unlocked_music",             Show("music_room", transition=enter_m_menu_doorway),         "assets/gui/archive_panels/music_room.png"),
        ("Side Stories", "archive_unlocked_character_stories", Show("character_stories", transition=enter_m_menu_doorway),  "assets/gui/archive_panels/side_stories.png"),
        ("Lost Records", "archive_unlocked_lost_records",      Show("lost_records", transition=enter_m_menu_doorway),       "assets/gui/archive_panels/lost_records.png"),
        ("Achievements", "archive_unlocked_achievements",      Show("achievements", transition=enter_m_menu_doorway),       "assets/gui/archive_panels/achievements.png"),
        ("Cards",        "archive_unlocked_cards",             Show("mc_collection", transition=enter_m_menu_doorway),      "assets/gui/archive_panels/cards.png"),
    ]

    # Each hub panel also has a full-resolution CG Gallery master. The module
    # flag remains the source of truth for whether the player has actually seen
    # that panel; the CG keeps its own path-derived persistent key so gallery
    # recovery and Archive availability cannot accidentally mutate each other.
    # ach_audit_content() reads this table as a truthful dynamic unlock source.
    archive_panel_cg_unlocks = (
        ("archive_unlocked_roster",            "Roster"),
        ("archive_unlocked_cgs",               "CG Gallery"),
        ("archive_unlocked_music",             "Music Room"),
        ("archive_unlocked_character_stories", "Side Stories"),
        ("archive_unlocked_lost_records",      "Lost Records"),
        ("archive_unlocked_achievements",      "Achievements"),
        ("archive_unlocked_cards",             "Cards"),
    )

    # Recover completion-reward CGs for profiles that finished these stories
    # before the reward art shipped. Keep the gallery's own path-derived keys
    # separate from story completion so developer gallery unlocks cannot forge
    # story progress in the opposite direction.
    archive_completed_story_cg_unlocks = (
        ("cs_tsubaki_02_completed", ("What I Keep", "What She Kept")),
        ("cs_asahina_01_completed", ("Hina's World",)),
        ("cs_kotonoha_01_completed", ("No One Lived There",)),
        ("cs_kotonoha_02_completed", ("Open Hands",)),
    )

    def archive_sync_panel_cgs():
        recovered = [
            title for archive_key, title in archive_panel_cg_unlocks
            if getattr(persistent, archive_key, False)
        ]
        for completed_key, titles in archive_completed_story_cg_unlocks:
            if getattr(persistent, completed_key, False):
                recovered.extend(titles)
        if recovered:
            # One batched call means at most one persistent write when several
            # default-open panels and old story rewards are recovered together.
            cg_unlock(*recovered)

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
    $ enter_m_menu_music(audio.archive)
    $ renpy.show_screen("archive")
    return

# -----------------------------------------------------------------------------
# TRANSFORMS (animation)
# -----------------------------------------------------------------------------
# Per-card entrance + hover. `delay` staggers a short settling motion. Idle
# cards are still; Transitions Off skips the arrival animation.
# Combined entrance + hover for archive cards
transform archive_card_anim(delay=0.0):
    alpha (0.0 if _preferences.transitions != 0 else 1.0)
    yoffset (16 if _preferences.transitions != 0 else 0)
    subpixel True
    pause (delay if _preferences.transitions != 0 else 0.0)
    easeout_cubic (0.35 if _preferences.transitions != 0 else 0.0) alpha 1.0 yoffset 0
    on idle:
        ease 0.15 yoffset 0
    on hover:
        ease 0.15 yoffset -3

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
        alpha (0.0 if _preferences.transitions != 0 else 1.0)
        yoffset (-min(rise, 18) if _preferences.transitions != 0 else 0)
        easeout_cubic (secs if _preferences.transitions != 0 else 0.0) alpha 1.0 yoffset 0
    on hide:
        alpha 1.0
        easeout_quad (out if _preferences.transitions != 0 else 0.0) alpha 0.0 yoffset -min(fall, 12)

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

# A mounted print under the cursor comes up to full colour from a faded idle,
# like a photo taken off the pile (Roster cards, CG Gallery prints). 8.6
# containers pass hover/idle down to nested transforms
# (config.containers_pass_transform_events), so this sits on the print itself
# and the paper around it stays one stock.
transform archive_print_develop:
    matrixcolor SaturationMatrix(0.6)
    on hover:
        easeout_cubic 0.18 matrixcolor SaturationMatrix(1.0)
    on idle:
        easeout_cubic 0.18 matrixcolor SaturationMatrix(0.6)

# -----------------------------------------------------------------------------
# BACKDROP
# Shared background layer: the Archive's dedicated physical preservation room
# and a light readability grade. Keep this alias separate from `bg ether`: that
# image is also story/transition art and must not be repurposed for menus.
# -----------------------------------------------------------------------------
image enter_m_archive_bg = "assets/gui/menu/archive_vn.png"

screen archive_backdrop():
    add "enter_m_archive_bg"
    add Solid("#02050a30")

# -----------------------------------------------------------------------------
# REUSABLE HEADER
# An engraved book mark, title, and "Return" button. Parameterised so
# sub-screens (roster/music/etc.) can reuse the same look:
#   title         : heading text
#   return_action : action list run by the Return button
#   return_text   : button caption (defaults to localized "Return")
# -----------------------------------------------------------------------------
screen archive_header(title, return_action, return_text=_("Return"), static=False):
    hbox:
        xfill True
        ysize 64

        frame:
            style "archive_header_title_frame"

            hbox:
                spacing 12
                yalign 0.5
                use illustrated_menu_motif("archive", 48, 54)
                text title style "archive_title" yalign 0.5

        null width 1 xfill True

        textbutton return_text:
            id "archive_return"
            style "archive_return_button"
            yalign 0.5
            action return_action

# -----------------------------------------------------------------------------
# REUSABLE CENSUS / READOUT STRIP
# The thin catalogue census the hub and child screens show under their header.
# Factored out here so every sub-screen renders an identical strip:
#   left_text  : primary readout (left, next to a small printed diamond)
#   right_text : secondary readout (right-aligned); omit for none
#   width      : rail width (defaults to the shell content width)
#   rule       : draw the plum hairline under the strip (default True)
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
screen archive_readout(left_text, right_text="", width=1150, rule=True, right_slot=False, slot_spacing=20, text_style="archive_meta_text", static=False):
    vbox:
        xalign 0.5
        spacing 8

        fixed:
            xsize width
            ysize 20

            add Solid(IM_PLUM) xysize (5, 5) xpos 1 yalign 0.5 rotate 45
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
            add Solid("#c5a0bd55") xysize (width, 1)

# -----------------------------------------------------------------------------
# REUSABLE PORTRAIT WINDOW
# A framed sprite window with a textured dark mount and fine plum rules.
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
#               its frame and backing but shows the hub's sealed-record art,
#               and its hairlines go grey. Use it for a subject the player has
#               not met: a desaturated
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

        add IM_DARK_PANEL xysize (w, h)

        if locked:
            # One sealed-record engraving conceals the subject at every size.
            add Transform("assets/gui/menu/illustrated/archive/sealed_record.svg", xysize=(int(w * 0.84), int(h * 0.72)), fit="contain"):
                align (0.5, 0.5)
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

        add Solid("#5b525e" if locked else "#c5a0bd88") xysize (w, 1)
        add Solid("#5b525e" if locked else "#c5a0bd88") xysize (w, 1) ypos (h - 1)

# -----------------------------------------------------------------------------
# THE SHELL'S BOOKPLATE CORNERS
# Every archive sub-screen sits in an `archive_shell_frame` (1200x690, styled
# below) and draws engraved corners around it. Those four numbers ARE the frame,
# so they live here once instead of being restated at each sub-screen -- an
# earlier round of copies drifted to a narrower 1160 and clipped the right edge.
# -----------------------------------------------------------------------------
screen archive_shell_brackets():
    # Engraved bookplate corners retain the 1200 x 690 shell boundary.
    use archive_bookplate_corners(40, 15, 1200, 690)

screen archive_bookplate_corners(x, y, w, h):
    add "assets/gui/menu/illustrated/archive/bookplate_corner.svg" xpos x ypos y
    add "assets/gui/menu/illustrated/archive/bookplate_corner.svg" xpos (x + w - 50) ypos y xzoom -1
    add "assets/gui/menu/illustrated/archive/bookplate_corner.svg" xpos x ypos (y + h - 50) yzoom -1
    add "assets/gui/menu/illustrated/archive/bookplate_corner.svg" xpos (x + w - 50) ypos (y + h - 50) xzoom -1 yzoom -1

# Gold photo corners holding a print at (x, y, w, h): one corner engraving,
# mirrored into place the same way. Roster mounts, its case file, and the CG
# Gallery's prints and viewer all hold their art with these.
screen archive_photo_corners(x, y, w, h):
    add "assets/gui/menu/illustrated/archive/photo_corner.svg" xpos (x - 4) ypos (y - 4)
    add "assets/gui/menu/illustrated/archive/photo_corner.svg" xpos (x + w - 26) ypos (y - 4) xzoom -1
    add "assets/gui/menu/illustrated/archive/photo_corner.svg" xpos (x - 4) ypos (y + h - 26) yzoom -1
    add "assets/gui/menu/illustrated/archive/photo_corner.svg" xpos (x + w - 26) ypos (y + h - 26) xzoom -1 yzoom -1

# -----------------------------------------------------------------------------
# HUB MINI-CG
# The old placeholder was squeezed into a narrow 80x112 portrait. These scenes
# need room for interactions, so every module now gets a 16:9 window while the
# 250x230 card and the surrounding 4+3 wall remain exactly the same size.
# Production art is stored at 384x216 (2x this window) for clean downsampling.
# A fine mount keeps the mini-CGs reusable without catalogue marks baked in.
# -----------------------------------------------------------------------------
screen archive_module_thumbnail(img, unlocked):
    fixed:
        xysize (192, 108)
        xalign 0.5

        if unlocked and img:
            add Transform(img, xysize=(192, 108), fit="contain")
        else:
            add "assets/gui/menu/illustrated/archive/sealed_record.svg"

        $ _amt_rule = "#71496688" if unlocked else "#8d788b"
        add Solid(_amt_rule) xysize (192, 1)
        add Solid(_amt_rule) xysize (192, 1) ypos 107
        add Solid(_amt_rule) xysize (1, 108)
        add Solid(_amt_rule) xysize (1, 108) xpos 191

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
    # archive starts, at full volume, on the frame this screen appears.
    # See menu_transitions.rpy section 6.
    on "show" action [EnterMMenuMusic(audio.archive), Function(archive_sync_panel_cgs), Function(ach_refresh)]
    on "replace" action [EnterMMenuMusic(audio.archive), Function(archive_sync_panel_cgs), Function(ach_refresh)]

    use illustrated_menu_backdrop("archive")

    # Back/Escape both bail out: restore menu BGM, then Return() to the caller.
    # The track is handed over with a fade rather than cut -- see section 6 of
    # menu_transitions.rpy for why a hard cut here stuttered the way out.
    key "game_menu" action [EnterMMenuMusic(audio.mainmenu), Return()]
    key "K_ESCAPE" action [EnterMMenuMusic(audio.mainmenu), Return()]

    # Live module census for the subsystem readout.
    $ a_total = len(archive_items)
    $ a_online = sum(1 for _it in archive_items if archive_is_unlocked(_it[1]))

    frame:
        style "archive_frame"
        at archive_frame_enter()

        vbox:
            xalign 0.5
            yalign 0.5
            # The old 10px outer gaps plus a 25px card-row gap totalled 625px
            # inside a 620px content well. Tighten only the hub's rhythm so both
            # rows and the footer sit inside the frame without changing card size.
            spacing 8

            # Reuse the header defined above; its Return mirrors the key actions.
            use archive_header("ARCHIVE", [EnterMMenuMusic(audio.mainmenu), Return()])

            # Collection census and accent rule -- the same strip every sub-screen
            # uses, so the hub is styled by the same definition it exports.
            use archive_readout(
                "THE COLLECTION / %d OF %d ROOMS OPEN" % (a_online, a_total),
                "STORY / ART / MEMORY",
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
                spacing 20
                xalign 0.5

                for _a_row in _a_rows:
                    # Centre a short final row within the full first-row width so
                    # seven modules read as a deliberate 4+3 wall, not a missing
                    # fourth card.
                    hbox:
                        spacing 25
                        xalign 0.5

                        for i, item in _a_row:
                            # Unpack the data tuple and resolve its lock state.
                            $ a_label, a_key, a_action, a_icon = item
                            $ a_unlocked = archive_is_unlocked(a_key)
                            $ a_delay = i * 0.07   # staggered entrance delay per card
                            $ a_id = "NO. %02d" % (i + 1)

                            button:
                                id ("archive_module_%02d" % (i + 1))
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
                                            # Static status is enough here; seven
                                            # independent blink loops added motion
                                            # without conveying changing state.
                                            add Solid("#714966") xysize (6, 6) rotate 45 xanchor 1.0 xpos 214 yalign 0.5
                                        else:
                                            add Solid("#99878e") xysize (6, 6) rotate 45 xanchor 1.0 xpos 214 yalign 0.5

                                    add Solid("#71496688" if a_unlocked else "#99878e66"):
                                        xsize 214
                                        ysize 2

                                    # The sealed-book engraving conceals locked art.
                                    use archive_module_thumbnail(a_icon, a_unlocked)

                                    # The title stays legible while the contents remain
                                    # sealed. Music Room is the only gated whole room.
                                    if a_unlocked and a_icon:
                                        text a_label style "archive_item_text" xalign 0.5
                                        text "OPEN COLLECTION" style "archive_item_status" xalign 0.5
                                    else:
                                        text a_label style "archive_locked_text" xalign 0.5
                                        text ("FINISH CHAPTER 0.5 TO OPEN" if a_key == "archive_unlocked_music" else "NOT YET AVAILABLE") style "archive_locked_status" xalign 0.5

            # The catalogue's colophon.
            fixed:
                xsize 1100
                ysize 16

                add Solid(IM_PLUM) xysize (5, 5) xpos 0 yalign 0.5
                text "THE THINGS WE KEEP" style "archive_footer_text" xpos 13 yalign 0.5
                text "ENTER M / THE ARCHIVE" style "archive_footer_text" xanchor 1.0 xpos 1100 yalign 0.5

    # Engraved corners framing the catalogue.
    use archive_bookplate_corners(60, 28, 1160, 664)

    # Floating corner button: relaunch the opening movie. Uses call_in_new_context
    # so the OP plays in its own context and returns here cleanly (see the
    # enter_m_archive_replay_op label above).
    textbutton _("Replay OP"):
        id "archive_replay_op"
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

    # The Vault: the one room in here that isn't finished. Bottom-right,
    # mirroring Replay OP in the top-right and in the same corner style,
    # because it is an Archive door and should read as one. vault_open()
    # hands the music over, greets a first-timer, and SHOWS the room over
    # this screen rather than replacing it -- so leaving the Vault lands
    # back here, not on the title. Guarded, so deleting addons/Vault/ takes
    # the button with it. See addons/Vault/vault.rpy.
    if renpy.has_screen("vault"):
        textbutton _("The Vault"):
            id "archive_vault"
            style "archive_corner_button"
            xalign 0.985
            yalign 0.975
            action Function(vault_open)
            at transform:
                on show:
                    alpha 0.0
                    xoffset 14
                    pause 0.28
                    easeout 0.22 alpha 1.0 xoffset 0

# =============================================================================
# STYLES
# The Archive is an engraved plum-and-paper catalogue. The hub's cards use
# light ink stock; shared child shells retain cream-on-dark contrast. Several
# styles use `is <parent>` to inherit and tweak (e.g. corner button is the
# return button at a different size). archive_shell_frame / archive_panel* /
# archive_sv_vscrollbar are shared building blocks the sub-screens reuse.
# =============================================================================
style archive_frame:
    xalign 0.5
    yalign 0.5
    xsize 1160
    ysize 664
    background IM_DARK_PANEL
    padding (30, 22)

style archive_shell_frame is archive_frame:
    xsize 1200
    ysize 690
    padding (24, 16)

style archive_header_title_frame:
    background None
    padding (0, 0)
    yalign 0.5

style archive_title:
    font gui.default_font
    size 36
    color IM_PAPER
    bold True
    outlines []

style archive_item_button:
    xysize (250, 230)
    background "assets/gui/menu/illustrated/archive/catalogue_card_idle.svg"
    hover_background "assets/gui/menu/illustrated/archive/catalogue_card_hover.svg"
    selected_background "assets/gui/menu/illustrated/archive/catalogue_card_hover.svg"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (18, 12)

style archive_item_text:
    font gui.default_font
    color IM_INK
    size 22
    xalign 0.5
    text_align 0.5
    bold True
    outlines []

style archive_item_status:
    font gui.interface_font
    color "#714966"
    size 11
    xalign 0.5
    text_align 0.5
    kerning 0.8
    outlines []

style archive_locked_text is archive_item_text:
    color "#6b5a67"

style archive_locked_status is archive_item_status:
    color "#766471"
    size 10
    kerning 0.0

style archive_meta_text is default:
    font gui.interface_font
    size 12
    color IM_PLUM
    kerning 1.0
    outlines []

style archive_footer_text is default:
    font gui.interface_font
    size 10
    color IM_MUTED
    kerning 1.0
    outlines []

style archive_card_id is default:
    font gui.interface_font
    size 11
    color "#714966"
    kerning 1.0
    outlines []

style archive_return_button:
    xsize 126
    ysize 42
    background IM_RETURN_IDLE
    hover_background IM_RETURN_HOVER
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (15, 8)

style archive_return_button_text:
    font gui.interface_font
    color IM_PAPER
    hover_color "#ffffff"
    size 20
    bold False
    outlines []

style archive_corner_button is archive_return_button:
    xsize 150
    ysize 38

style archive_corner_button_text is archive_return_button_text:
    size 18

style archive_panel:
    background IM_DARK_PANEL
    padding (18, 18)

style archive_sidebar_panel is archive_panel:
    background IM_DARK_PANEL

style archive_sv_vscrollbar:
    xsize 6
    base_bar Frame(Solid("#4b4350"), 0, 0, 0, 0)
    thumb Frame(Solid(IM_PLUM), 2, 2, 2, 2)
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
# #b9793f, silver #9fb0bd, gold #e0ac33) and cyan status chips. Measured contrast
# of #04121a on those fills stays comfortably readable; swapping to near-white
# makes the same pairings strictly worse, and an outline cannot rescue them.
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