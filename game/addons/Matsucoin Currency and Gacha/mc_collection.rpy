# =============================================================================
# mc_collection.rpy  --  THE CARD BINDER (Archive module 7)
# =============================================================================
#
# WHAT THIS FILE IS
#   The album of everything the prize machine has handed over. It is the seventh
#   Archive module, reached from the Archive hub exactly like Roster, CG Gallery,
#   Music Room, Side Stories, Lost Records and Achievements, and it deliberately
#   reuses that hub's shared chrome -- archive_backdrop / archive_header /
#   archive_readout / archive_shell_frame / the archive_sv scrollbar / the chip
#   and meta text styles -- so it reads as the same subsystem rather than as the
#   Arcade leaking into the Archive.
#
# WHY THE BINDER IS HERE AND THE MACHINE IS NOT
#   The machine is a coin-op object and lives on the Arcade floor
#   (mc_gacha.rpy). What it dispenses is a COLLECTION, and every other
#   collection in this game -- CGs, tracks, roster slots, side stories -- is
#   already in the Archive. Splitting them puts each half in the room whose
#   language it actually speaks, and the two are one click apart from each hub.
#
# WHAT IS GATED
#   Nothing about the shell. The binder ships open and shows every card's SLOT
#   from the first launch, silhouetted until it is pulled -- the same reasoning
#   the Archive flag block gives for the CG Gallery and the Roster: an unowned
#   card is visibly a card, the same size and in the same place it will occupy
#   once it is yours, because a grid of identical "???" tells a first-time
#   player nothing about what is in there.
#
# THE CARD FACE ITSELF
#   screen mc_card_face + the enter_m.mc_card shader live in mc_gacha.rpy, and
#   this file calls them unchanged. A card therefore looks identical in the
#   machine that gave it to you and in the album it ends up in, which is the
#   entire point of having one widget.
# =============================================================================

# --- thumbnail cell geometry -------------------------------------------------
# MC_THUMB_LIFT is reserved as blank headroom INSIDE every cell (the `null` at
# the top of the thumb's vbox), and the hover lift then moves the contents up
# into that reserved space. The card therefore never leaves its own button, and
# a viewport -- which clips hard at its bounds and does not care why something
# crossed them -- has nothing to clip.
#
# The earlier attempt put the lift on the BUTTON and padded the top of the
# scrolling content instead. That fixed the very first row and nothing else:
# the moment the grid was scrolled, whichever row was straddling the viewport's
# top edge had its cards' heads cut off on hover, because the padding was at the
# top of the CONTENT, not at the top of each cell.
define MC_THUMB_LIFT = 8
define MC_THUMB_CAPTION = 34          # two lines of mc_thumb_name
define MC_THUMB_H = 265               # 8 lift + 5 + 213 card + 5 + 34 caption

# Entrance only, on the button. It drops IN from below (+14 -> 0), which moves
# toward the middle of the viewport and so can never be clipped by its top edge.
transform mc_binder_thumb(delay=0.0):
    subpixel True
    alpha 0.0
    yoffset 14
    pause delay
    easeout 0.30 alpha 1.0 yoffset 0

# Hover, on the cell's contents.
transform mc_binder_lift:
    subpixel True
    on idle:
        ease 0.15 yoffset 0
    on hover:
        ease 0.15 yoffset -MC_THUMB_LIFT

transform mc_detail_pop:
    subpixel True
    on show:
        alpha 0.0
        zoom 0.94
        easein_back 0.32 alpha 1.0 zoom 1.0
    on hide:
        easeout_quad 0.18 alpha 0.0 zoom 0.97


# -----------------------------------------------------------------------------
# THE BINDER
# Modal overlay over the Archive hub (mirroring cg_gallery / character_stories):
# return is Hide, which reveals the hub underneath.
# -----------------------------------------------------------------------------
screen mc_collection():
    modal True

    # Anything earned since the hub last synced (a fight, a side story, an
    # achievement) is paid before the wallet is drawn.
    on "show" action Function(mc_refresh)

    default mc_sel_subject = 0

    use archive_backdrop

    key "game_menu" action Hide("mc_collection")
    key "K_ESCAPE" action Hide("mc_collection")

    if len(MC_SUBJECTS) > 1:
        key "K_UP" action SetScreenVariable("mc_sel_subject", (mc_sel_subject - 1) % len(MC_SUBJECTS))
        key "K_DOWN" action SetScreenVariable("mc_sel_subject", (mc_sel_subject + 1) % len(MC_SUBJECTS))

    python:
        _mcb_owned, _mcb_total = mc_collection_counts()
        _mcb_subject_id, _mcb_subject_label = MC_SUBJECTS[min(mc_sel_subject, len(MC_SUBJECTS) - 1)]
        _mcb_cards = mc_cards_for(_mcb_subject_id)
        # Fixed 5 columns; the rows are chunked here rather than left to a grid
        # so a subject with a number of cards that is not a multiple of 5 packs
        # its last row left instead of spreading it.
        _mcb_cols = 5
        _mcb_rows = [_mcb_cards[i:i + _mcb_cols]
                    for i in range(0, len(_mcb_cards), _mcb_cols)]

    frame:
        style "archive_shell_frame"
        padding (24, 20)
        at archive_frame_enter(50, 0.5, 30)

        vbox:
            spacing 12

            use archive_header("CARD COLLECTION", Hide("mc_collection"))

            # Census strip. The right slot carries the wallet, because the
            # binder is the one place a player looks up "how close am I" and
            # "can I afford to keep going" in the same glance.
            use archive_readout(
                "CARD ARCHIVE // %d/%d COLLECTED" % (_mcb_owned, _mcb_total),
                right_slot=True):

                use mc_balance_chip(15, light=True)

            hbox:
                spacing 0

                # --- LEFT: subject sidebar --------------------------------
                frame:
                    xsize 240
                    ysize 520
                    style "archive_sidebar_panel"
                    padding (14, 14)

                    viewport:
                        mousewheel True
                        scrollbars "vertical"
                        style_prefix "archive_sv"
                        ysize 492

                        vbox:
                            spacing 6

                            for _idx, (_sid, _slabel) in enumerate(MC_SUBJECTS):
                                $ _s_done, _s_all = mc_subject_counts(_sid)
                                $ _s_sel = (_idx == mc_sel_subject)
                                $ _s_frac = (float(_s_done) / _s_all) if _s_all else 0.0
                                $ _s_new = any(mc_is_new(c.id) for c in mc_cards_for(_sid))

                                button:
                                    xsize 200
                                    ysize 58
                                    padding (0, 0)
                                    hover_sound gui.hover_sound
                                    activate_sound gui.activate_sound
                                    action SetScreenVariable("mc_sel_subject", _idx)

                                    if _s_sel:
                                        background Solid("#12314af2")
                                        hover_background Solid("#17415fee")
                                    else:
                                        background Solid("#07111dcc")
                                        hover_background Solid("#12314aee")

                                    hbox:
                                        spacing 0
                                        yfill True

                                        if _s_sel:
                                            add Solid("#56d7ff") xysize (4, 58) at enter_m_pip_pulse
                                        else:
                                            add Solid("#0c1a27") xysize (4, 58)

                                        vbox:
                                            spacing 4
                                            yalign 0.5
                                            xoffset 11

                                            hbox:
                                                spacing 6
                                                text _slabel style "mc_side_name" yalign 0.5
                                                if _s_new:
                                                    add Solid("#ffb454") xysize (6, 6) yalign 0.5 at console_blink

                                            fixed:
                                                xysize (172, 6)
                                                add Solid("#091622") xysize (172, 6)
                                                if _s_frac > 0:
                                                    add Solid("#56d7ff"):
                                                        xpos 1
                                                        ypos 1
                                                        xysize (max(1, int(170 * _s_frac)), 4)

                                            text ("%d/%d" % (_s_done, _s_all)) style "mc_side_count"

                add Solid("#56d7ff44") xysize (2, 520)

                # --- RIGHT: the selected subject's cards -------------------
                frame:
                    xsize 910
                    ysize 520
                    style "archive_panel"
                    padding (22, 16)

                    vbox:
                        spacing 10

                        hbox:
                            spacing 12
                            text _mcb_subject_label style "archive_panel_label" yalign 0.5
                            add Solid("#56d7ff66") xysize (120, 2) yalign 0.5 at enter_m_accent_grow

                        viewport:
                            mousewheel True
                            scrollbars "vertical"
                            style_prefix "archive_sv"
                            ysize 450
                            xsize 866

                            vbox:
                                spacing 14

                                for _r, _row in enumerate(_mcb_rows):
                                    hbox:
                                        spacing 14

                                        for _c, _card in enumerate(_row):
                                            $ _mc_have = mc_card_owned(_card.id)
                                            $ _mc_delay = (_r * _mcb_cols + _c) * 0.03

                                            button:
                                                style "mc_thumb_button"
                                                xysize (152, MC_THUMB_H)
                                                at mc_binder_thumb(_mc_delay)
                                                action (
                                                    [Function(mc_card_seen, _card.id),
                                                    Show("mc_card_detail", card=_card)]
                                                    if _mc_have else NullAction()
                                                )

                                                vbox:
                                                    spacing 5
                                                    xalign 0.5
                                                    # The lift lives on the CONTENTS, not on the
                                                    # button: the button keeps its slot in the row
                                                    # (so nothing reflows and its hover plate stays
                                                    # put) and the card rises inside the headroom
                                                    # the cell already reserves.
                                                    at mc_binder_lift

                                                    null height MC_THUMB_LIFT

                                                    fixed:
                                                        xysize (152, 213)

                                                        use mc_card_face(
                                                            _card, 152, 213,
                                                            locked=(not _mc_have))

                                                        if mc_is_new(_card.id):
                                                            frame:
                                                                background Solid("#0b0818ee")
                                                                padding (5, 1)
                                                                xpos 6
                                                                ypos 6
                                                                text "NEW" style "mc_thumb_new"

                                                    # FIXED-HEIGHT caption well, deep enough for
                                                    # two lines. Letting the label size itself made
                                                    # a two-line name ("Ontological Seer // Second
                                                    # Movement") taller than its own button, so it
                                                    # overflowed the hover plate and shoved the
                                                    # row's baseline out of line with its
                                                    # neighbours. Reserved space costs nothing and
                                                    # keeps every cell identical.
                                                    fixed:
                                                        xysize (148, MC_THUMB_CAPTION)
                                                        text (_card.name if _mc_have else "UNCOLLECTED"):
                                                            style ("mc_thumb_name" if _mc_have else "mc_thumb_name_locked")
                                                            xsize 148
                                                            xalign 0.5
                                                            yalign 0.0
                                                            text_align 0.5
                                                            layout "subtitle"

            # Footer status line, matching the hub's.
            fixed:
                xsize 1150
                ysize 16

                add Solid("#345a6b") xysize (5, 5) xpos 0 yalign 0.5
                text "CARD.SYS :: PRIZE MACHINE ON THE ARCADE FLOOR":
                    style "archive_footer_text"
                    xpos 13
                    yalign 0.5
                text ("PULLS %s" % mc_num(persistent.mc_pulls_total)):
                    style "archive_footer_text"
                    xanchor 1.0
                    xpos 1150
                    yalign 0.5

    use archive_shell_brackets


# -----------------------------------------------------------------------------
# CARD DETAIL
# A card on its own, big, with its flavor line. Shown over the binder rather
# than inline: the sidebar already claims 240px of the shell, and squeezing a
# detail column into what is left would have cost the grid a column.
# -----------------------------------------------------------------------------
screen mc_card_detail(card):
    modal True
    zorder 65

    key "game_menu" action Hide("mc_card_detail")
    key "K_ESCAPE" action Hide("mc_card_detail")

    add Solid("#010308ee")

    # Click anywhere off the panel to dismiss. `dismiss`, not a full-screen
    # button -- a childless button with xfill/yfill and no background renders no
    # hit area and is simply dead. See the note in mc_gacha.rpy's reveal.
    # The panel's own Close button still wins, because it is added AFTER this
    # and events dispatch to the topmost child first.
    dismiss action Hide("mc_card_detail")

    # The plate needs to be MORE opaque than the screen dim behind it, or it
    # does not read as a panel at all -- at #050811f2 over a dimmed binder both
    # sides of its edge were the same near-black and the card looked as though
    # it were floating on the backdrop. Opaque fill plus a cyan hairline.
    frame:
        style "archive_panel"
        background Frame(Solid("#070f1a"), 0, 0)
        xalign 0.5
        yalign 0.5
        xysize (760, 500)
        padding (28, 24)
        at mc_detail_pop

        hbox:
            spacing 28
            yalign 0.5

            fixed:
                xysize (300, 420)
                yalign 0.5
                use mc_card_face(card, 300, 420, radius=12.0)

            vbox:
                yalign 0.5
                xsize 372
                spacing 12

                hbox:
                    spacing 9
                    # Same treatment as the chip on the card face: dark plate,
                    # bright tier ink. See the note in mc_gacha.rpy.
                    frame:
                        background Solid("#0b0818ee")
                        padding (9, 2)
                        yalign 0.5
                        text card.tier["label"]:
                            style "mc_detail_chip"
                            color card.glow
                    text card.tier["full"]:
                        style "mc_detail_kicker"
                        color card.glow
                        yalign 0.5

                text card.name style "mc_detail_name"

                add Solid(card.color + "88") xysize (150, 2) at enter_m_accent_grow

                text card.flavor style "mc_detail_flavor"

                null height 4

                # No COPIES row: duplicates are not kept (see the collection
                # state note in mc_cards.rpy). What IS worth knowing is what
                # pulling this one again pays out.
                hbox:
                    spacing 10
                    text "DUPLICATE REFUND" style "archive_meta_text" yalign 0.5
                    add MatsucoinIcon(13) yalign 0.5
                    text str(card.refund) style "mc_detail_stat" yalign 0.5

                null height 6

                textbutton _("Close"):
                    style "archive_return_button"
                    action Hide("mc_card_detail")

    use console_brackets(258, 108, 764, 504, "#56d7ff5a", 20, 2)


# =============================================================================
# STYLES
# Archive chrome: near-black panels, cyan accents. The only warm ink in here is
# the coin and the NEW badge -- both of which are Arcade objects that have
# wandered in, and should read that way.
# =============================================================================
style mc_thumb_button:
    background Solid("#07111d99")
    hover_background Solid("#12314ae6")
    padding (0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mc_thumb_name is gui_text:
    font gui.interface_font
    size 12
    color "#dff8ff"
    outlines [(1, "#02040b", 0, 0)]

style mc_thumb_name_locked is gui_text:
    font gui.interface_font
    size 11
    color "#4f5b67"
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

# Amber ink on a dark plate, not near-black on an amber plate. It reads just as
# loudly -- amber is still the colour that means "new" -- and it keeps the rule
# this UI follows everywhere else: bright text, dark ground, never the inverse.
style mc_thumb_new:
    font gui.interface_font
    size 10
    color "#ffd98a"
    bold True
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

style mc_side_name is gui_text:
    font gui.interface_font
    size 15
    color "#dff8ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style mc_side_count is gui_text:
    font gui.interface_font
    size 11
    color "#7fcfe0"
    kerning 1.0

style mc_detail_chip:
    font gui.interface_font
    size 14
    color "#a9b8cf"
    bold True
    kerning 1.0
    outlines [(1, "#02040b", 0, 0)]

style mc_detail_kicker is gui_text:
    font gui.interface_font
    size 11
    kerning 2.0
    bold True
    outlines [(1, "#02040b", 0, 0)]

style mc_detail_name:
    font gui.interface_font
    size 27
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff66", 1, 1)]

style mc_detail_flavor is gui_text:
    font gui.interface_font
    size 15
    color "#9fc9d6"
    line_spacing 3
    outlines [(1, "#02040b", 0, 0)]

style mc_detail_stat is gui_text:
    font gui.interface_font
    size 17
    color "#dff8ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]
