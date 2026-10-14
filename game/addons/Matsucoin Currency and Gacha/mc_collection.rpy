# Archive card binder, using mc_gacha's shared mc_card_face widget.
# The shell and slots are visible immediately; ownership controls card visibility.
# A raster binder underlay supplies paper/rings while pockets remain interactive.
# Sleeve order is well -> card -> plastic: a raised card emerges above the mouth
# while its lower portion remains behind the film. Preserve that layer order.

init -10 python:

    def _mc_register_binder_shaders():

        # ---- sleeve: the transparent pocket front ---------------------------
        # Drawn OVER the card. u_fill is how much of the pocket, measured up
        # from the bottom, still holds one: 1.0 for a seated thumbnail and a
        # smaller fixed value for the already-drawn detail card. The bright
        # welded mouth is drawn at that boundary and stays physically attached
        # to the page while the card itself moves.
        #
        # PREMULTIPLIED OUTPUT, like every custom shader in this project:
        # colour is accumulated straight and multiplied by alpha once at the
        # end. A dark detail (the lip's shadow, the inner recess) is alpha
        # WITHOUT colour, which darkens what is behind it; a bright one adds
        # both.
        renpy.register_shader("enter_m.mc_sleeve", variables="""
            uniform vec2 u_model_size;
            uniform float u_radius;
            uniform float u_fill;
            uniform float u_gloss;
            uniform float u_notch;      // thumb-notch RADIUS in px; 0 = none
            uniform vec4 u_tint;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float enterm_sleeve_rr(vec2 p, vec2 b, float r) {
                vec2 q = abs(p) - b + vec2(r);
                return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - r;
            }
        """, fragment_300="""
            vec2 sl_size = max(u_model_size, vec2(1.0));
            vec2 sl_uv = v_tex_coord;
            vec2 sl_px = sl_uv * sl_size;
            vec2 sl_half = sl_size * 0.5;
            float sl_rad = clamp(u_radius, 0.0, min(sl_half.x, sl_half.y));
            float sl_d = enterm_sleeve_rr(sl_px - sl_half, sl_half, sl_rad);
            float sl_aa = 1.25;
            float sl_shape = 1.0 - smoothstep(0.0, sl_aa, sl_d);

            if (sl_shape <= 0.0) {
                gl_FragColor = vec4(0.0);
                return;
            }

            // The mouth sits u_fill of the way up from the bottom. Everything
            // below it is still sleeved; everything above it is bare card.
            float sl_mouth = 1.0 - clamp(u_fill, 0.0, 1.0);
            float sl_in = smoothstep(sl_mouth - 0.004, sl_mouth + 0.004, sl_uv.y);

            vec3 sl_col = vec3(0.0);
            float sl_a = 0.0;

            // The film. Cool and faint -- enough to read as plastic lying over
            // the art without making the art itself look wrong.
            float sl_film = 0.095 * sl_in;
            sl_col += u_tint.rgb * sl_film;
            sl_a += sl_film;

            // Two gloss streaks on the diagonal. STATIC, not swept: a settled
            // binder asks for no frames at all, and a sweep keyed to ambient
            // time freezes for seconds and then snaps -- the same measured
            // reason the SSR holo interpolates a uniform of its own instead.
            float sl_ax = sl_uv.x * 0.86 + sl_uv.y * 0.34;
            float sl_g1 = exp(-pow((sl_ax - 0.40) * 3.1, 2.0)) * 0.26;
            float sl_g2 = exp(-pow((sl_ax - 0.83) * 7.5, 2.0)) * 0.40;
            float sl_gloss = (sl_g1 + sl_g2) * u_gloss * sl_in;
            sl_col += vec3(1.0) * sl_gloss;
            sl_a += sl_gloss;

            // Recess: the card sits INSIDE, so the inner edge is shaded.
            float sl_inner = (1.0 - smoothstep(0.0, 7.0, -sl_d)) * sl_in;
            sl_a += sl_inner * 0.34;

            // The welded seam running round the pocket.
            float sl_seam = (1.0 - smoothstep(1.4 - sl_aa, 1.4 + sl_aa, abs(sl_d)))
                * step(sl_d, 0.0) * sl_in;
            sl_col += u_tint.rgb * sl_seam * 0.55;
            sl_a += sl_seam * 0.30;

            // The lip, and the shadow it casts just inside the mouth.
            float sl_lip = 1.0 - smoothstep(0.0, 2.4,
                abs((sl_uv.y - sl_mouth) * sl_size.y));
            float sl_shade = (1.0 - smoothstep(0.0, 9.0,
                (sl_uv.y - sl_mouth) * sl_size.y)) * step(sl_mouth, sl_uv.y);
            sl_a += sl_shade * 0.26;

            // The thumb notch -- the half-moon cut every real pocket has, and
            // the one detail that stops this reading as a rounded rectangle
            // with a highlight on it. It is a HOLE: film, gloss and lip are all
            // removed inside it before its own rim is drawn.
            if (u_notch > 0.5) {
                vec2 sl_np = vec2((sl_uv.x - 0.5) * sl_size.x,
                                (sl_uv.y - sl_mouth) * sl_size.y);
                float sl_nl = length(sl_np);
                float sl_cut = (1.0 - smoothstep(u_notch - 1.2, u_notch + 1.2, sl_nl))
                    * step(0.0, sl_np.y);
                float sl_keep = 1.0 - sl_cut;
                sl_col *= sl_keep;
                sl_a *= sl_keep;
                sl_lip *= sl_keep;
                float sl_rim = (1.0 - smoothstep(0.0, 2.0, abs(sl_nl - u_notch)))
                    * step(0.0, sl_np.y);
                sl_col += u_tint.rgb * sl_rim * 1.15;
                sl_a += sl_rim * 0.62;
            }

            sl_col += u_tint.rgb * sl_lip * 1.30;
            sl_a += sl_lip * 0.66;

            sl_a = clamp(sl_a, 0.0, 1.0) * sl_shape;
            vec3 sl_rgb = clamp(sl_col, 0.0, 1.0) * sl_shape;
            gl_FragColor = vec4(min(sl_rgb, vec3(sl_a)), sl_a);
        """)

        # ---- well: the empty pocket behind the card -------------------------
        # Seen through an uncollected slot, and under any card that has been
        # lifted -- which is exactly when it has to look like somewhere a card
        # goes rather than a hole in the page.
        renpy.register_shader("enter_m.mc_well", variables="""
            uniform vec2 u_model_size;
            uniform float u_radius;
            uniform vec4 u_tint;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 wl_size = max(u_model_size, vec2(1.0));
            vec2 wl_uv = v_tex_coord;
            vec2 wl_half = wl_size * 0.5;
            float wl_rad = clamp(u_radius, 0.0, min(wl_half.x, wl_half.y));
            vec2 wl_q = abs(wl_uv * wl_size - wl_half) - wl_half + vec2(wl_rad);
            float wl_d = min(max(wl_q.x, wl_q.y), 0.0)
                + length(max(wl_q, 0.0)) - wl_rad;
            float wl_shape = 1.0 - smoothstep(0.0, 1.25, wl_d);

            if (wl_shape <= 0.0) {
                gl_FragColor = vec4(0.0);
                return;
            }

            // Darker at the top, where a seated card casts down into the pocket.
            vec3 wl_col = mix(u_tint.rgb * 0.32, u_tint.rgb,
                smoothstep(0.0, 0.72, wl_uv.y));
            wl_col *= 1.0 - (1.0 - smoothstep(0.0, 10.0, -wl_d)) * 0.45;
            gl_FragColor = vec4(clamp(wl_col, 0.0, 1.0) * wl_shape, wl_shape);
        """)

    try:
        _mc_register_binder_shaders()
        MC_BINDER_SHADERS = True
    except Exception as _mc_binder_shader_error:
        MC_BINDER_SHADERS = False
        renpy.log("ENTER-M BINDER: shader registration failed: %r"
            % (_mc_binder_shader_error,))


# --- pocket geometry ---------------------------------------------------------
# The pocket is the card plus its welded margin; the cell is the pocket plus the
# headroom the hover lift rises into. Two columns by three rows on each leaf
# form the requested 3-row x 4-column spread without crossing the ring gutter.
define MC_CARD_W = 96
define MC_CARD_H = 134
define MC_SLEEVE_PAD = 3              # plastic either side of the card
define MC_SLEEVE_MOUTH = 3            # the lip band above a seated card
define MC_POCKET_W = 102              # 3 + 96 + 3
define MC_POCKET_H = 140              # 3 mouth + 134 card + 3 foot
define MC_SLEEVE_LIFT = 7             # how far hover draws a card out
define MC_THUMB_H = 147               # 7 lift + 140 pocket; name is on-card

# Measured pale-page bounds in binder_spread.png. Keeping these explicit makes
# it impossible for a pocket row to drift back onto the black leather cover.
define MC_LEFT_LEAF_X = 80
define MC_LEFT_LEAF_W = 463
define MC_RIGHT_LEAF_X = 608
define MC_RIGHT_LEAF_W = 468
define MC_POCKET_X_GAP = 42
# Move the cards clear of the category divider without pushing the bottom row
# off the paper: six pixels move from inter-row air into the top margin.
define MC_POCKET_Y_GAP = 1
define MC_BINDER_GRID_Y = 34
define MC_BINDER_COLS = 2
define MC_BINDER_ROWS = 3
# The category accordion is a plain vbox -- one 28px row per divider, spaced 3
# -- inside a frame that CANNOT size itself, so its plate has to be measured by
# hand against the divider COUNT. Measured at nine dividers: 21 title row + 9 +
# 1 rule + 9 + (9 * 28 + 8 * 3) + 32 padding = 348. Re-measure whenever
# MC_SUBJECTS changes length -- too short does not clip, it hangs the last row
# off the bottom of the dark plate.
define MC_CATALOG_PANEL_H = 370

define MC_BINDER_SLOTS_PER_SPREAD = 12
# Slots are numbered row-major across the open spread. Each leaf's local grid
# therefore takes alternating pairs rather than the old leaf-major 1-6 / 7-12
# split, which stranded every shipped category on the left page.
define MC_BINDER_LEFT_POSITIONS = (0, 1, 4, 5, 8, 9)
define MC_BINDER_RIGHT_POSITIONS = (2, 3, 6, 7, 10, 11)

# Detail uses the same canonical 5:7 size as a single-pull reveal. Once a card
# has cleared the binder it is presented as the object itself, not left sitting
# on top of the giant half-empty pocket that used to read as a grey pedestal.
define MC_DETAIL_CARD_W = 300
define MC_DETAIL_CARD_H = 420

# The film's colour. Cool and pale, so it reads as clear plastic catching the
# shell's own light rather than as a coloured gel laid over the art.
define MC_SLEEVE_TINT = (0.62, 0.83, 1.0, 1.0)

transform mc_sleeve_front(fill=1.0, gloss=1.0, notch=16.0, radius=9.0):
    mesh True
    shader "enter_m.mc_sleeve"
    u_radius radius
    u_fill fill
    u_gloss gloss
    u_notch notch
    u_tint MC_SLEEVE_TINT

transform mc_sleeve_well(radius=9.0, tint=(0.055, 0.10, 0.155, 1.0)):
    mesh True
    shader "enter_m.mc_well"
    u_radius radius
    u_tint tint

# A subject change moves the whole spread once. Cards do not waterfall into
# their pockets independently; that made an ordinary divider change look like
# the binder was being repopulated in front of the player.
transform mc_spread_enter(direction=1):
    subpixel True
    alpha 0.0
    xoffset (18 * direction)
    easeout 0.20 alpha 1.0 xoffset 0

transform mc_index_enter:
    subpixel True
    alpha 0.0
    zoom 0.985
    easeout 0.16 alpha 1.0 zoom 1.0

# THE HOVER LIFT, AND WHY IT IS NOT AN `on hover` BLOCK.
# A button hands its hover event to its DIRECT child and nothing else: only
# Transform relays set_transform_event onward, and every container in between
# (vbox, fixed, hbox) inherits the base implementation, which does not. An
# `on hover` block nested inside the cell would therefore never fire once --
# verified in renpy/display/behavior.py, which calls self.child.set_transform_
# event, and renpy/display/transform.py, which is the only class that passes it
# down. The old cell got away with it because its `at` sat on the button's one
# direct child and moved the WHOLE cell.
#
# That is no longer good enough: the pocket has to STAY PUT while the card
# inside it rises, or nothing is being pulled out of anything. So the button
# reports its own hover through a screen variable instead, and the seat below
# takes the offset as an argument. Changing that argument builds a new Transform
# which take_state seeds with the offset the old one had, so the ease runs from
# wherever the card currently is -- in both directions, and correctly even if
# the pointer crosses several cards quickly.
transform mc_card_seat(off=0):
    subpixel True
    easeout 0.17 yoffset off

# Opening a detail still begins with a short upward draw, but the pocket belongs
# to the binder behind the modal. The inspected card settles free-standing.
transform mc_detail_card_in:
    subpixel True
    alpha 0.0
    yoffset 54
    zoom 0.965
    easeout 0.34 alpha 1.0 yoffset 0 zoom 1.0

transform mc_detail_panel_in:
    subpixel True
    alpha 0.0
    zoom 0.988
    easeout 0.18 alpha 1.0 zoom 1.0


# One reusable pocket. The open binder places six of these on each leaf; a
# None card is a genuinely empty sleeve rather than a disabled mystery tile.
screen mc_binder_slot(card, have=False, is_new=False, lifted=False,
                      open_action=None, hover_action=None, unhover_action=None,
                      slot_number=0, allow_keyboard_focus=True):
    $ _slot_lift = -MC_SLEEVE_LIFT if (card is not None and have and lifted) else 0

    if card is not None:
        button:
            style "mc_thumb_button"
            xysize (MC_POCKET_W, MC_THUMB_H)
            sensitive (have and allow_keyboard_focus)
            keyboard_focus (have and allow_keyboard_focus)
            hovered hover_action
            unhovered unhover_action
            action open_action

            fixed:
                xysize (MC_POCKET_W, MC_THUMB_H)

                if MC_BINDER_SHADERS:
                    add Solid("#000000"):
                        xysize (MC_POCKET_W, MC_POCKET_H)
                        ypos MC_SLEEVE_LIFT
                        at mc_sleeve_well(6.5)
                else:
                    add Solid("#06121dcc"):
                        xysize (MC_POCKET_W, MC_POCKET_H)
                        ypos MC_SLEEVE_LIFT

                fixed:
                    xysize (MC_CARD_W, MC_CARD_H)
                    xpos MC_SLEEVE_PAD
                    ypos (MC_SLEEVE_LIFT + MC_SLEEVE_MOUTH)
                    at mc_card_seat(_slot_lift)

                    use mc_card_face(
                        card, MC_CARD_W, MC_CARD_H,
                        locked=(not have), holo=0.0, radius=7.0,
                        show_title=True, show_serial=False)

                    if is_new:
                        frame:
                            background Solid("#0b0818ee")
                            padding (5, 1)
                            xpos 5
                            ypos 5
                            text "NEW" style "mc_thumb_new"

                if MC_BINDER_SHADERS:
                    add Solid("#000000"):
                        xysize (MC_POCKET_W, MC_POCKET_H)
                        ypos MC_SLEEVE_LIFT
                        at mc_sleeve_front(1.0, 1.0, 11.0, 6.5)
                else:
                    add Solid("#d8f4ff20"):
                        xysize (MC_POCKET_W, MC_POCKET_H)
                        ypos MC_SLEEVE_LIFT
    else:
        # Real unused catalog capacity: page visible through a clear pocket,
        # indexed so it reads as a deliberate slot rather than missing UI.
        fixed:
            xysize (MC_POCKET_W, MC_THUMB_H)

            if MC_BINDER_SHADERS:
                add Solid("#000000"):
                    xysize (MC_POCKET_W, MC_POCKET_H)
                    ypos MC_SLEEVE_LIFT
                    at mc_sleeve_front(1.0, 0.42, 10.0, 6.0)
            else:
                add Solid("#d8f4ff12"):
                    xysize (MC_POCKET_W, MC_POCKET_H)
                    ypos MC_SLEEVE_LIFT

            vbox:
                xalign 0.5
                ypos (MC_SLEEVE_LIFT + (MC_POCKET_H // 2) - 10)
                spacing 2

                text ("%02d" % slot_number):
                    style "mc_empty_slot_number"
                    xalign 0.5
                text "VACANT":
                    style "mc_empty_slot_label"
                    xalign 0.5



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
    default mc_sel_page = 0
    default mc_hover_card = None
    default mc_catalog_open = False
    default mc_page_direction = 1

    # The collection is a binder inside the Archive, so it shares that room.
    add "enter_m_archive_bg"
    add Solid("#01050a66")

    python:
        _mc_ensure_cards()
        _mcb_owned_ids = frozenset(persistent.mc_cards_owned)
        _mcb_new_ids = frozenset(persistent.mc_new_ids)
        _mcb_total = len(MC_CARDS)
        _mcb_owned = sum(1 for card in MC_CARDS if card.id in _mcb_owned_ids)
        mc_sel_subject = max(0, min(mc_sel_subject, len(MC_SUBJECTS) - 1))
        _mcb_subject_id, _mcb_subject_label = MC_SUBJECTS[mc_sel_subject]
        _mcb_cards = mc_cards_for(_mcb_subject_id)
        _mcb_subject_total = len(_mcb_cards)
        _mcb_subject_owned = sum(
            1 for card in _mcb_cards if card.id in _mcb_owned_ids)
        _mcb_hovered_card = (MC_CARD_BY_ID.get(mc_hover_card)
            if mc_hover_card else None)

        # Category selection and physical page turning are separate axes. One
        # spread holds a 3x4 catalog grid: 3 rows x 2 columns on each leaf,
        # producing four columns across the open binder.
        # Short categories receive real clear sleeves in the remaining capacity;
        # a future category with more than twelve cards stays selected while the
        # arrows turn to its next spread.
        _mcb_page_count = max(1, (
            _mcb_subject_total + MC_BINDER_SLOTS_PER_SPREAD - 1
        ) // MC_BINDER_SLOTS_PER_SPREAD)
        mc_sel_page = max(0, min(mc_sel_page, _mcb_page_count - 1))
        _mcb_page_start = mc_sel_page * MC_BINDER_SLOTS_PER_SPREAD
        _mcb_page_cards = list(_mcb_cards[
            _mcb_page_start:_mcb_page_start + MC_BINDER_SLOTS_PER_SPREAD])
        _mcb_page_cards.extend(
            [None] * (MC_BINDER_SLOTS_PER_SPREAD - len(_mcb_page_cards)))
        _mcb_left_slots = tuple(
            ("left-%d-%s" % (position, _mcb_page_cards[position].id
            if _mcb_page_cards[position] else "vacant"),
            _mcb_page_cards[position], _mcb_page_start + position + 1)
            for position in MC_BINDER_LEFT_POSITIONS)
        _mcb_right_slots = tuple(
            ("right-%d-%s" % (position, _mcb_page_cards[position].id
            if _mcb_page_cards[position] else "vacant"),
            _mcb_page_cards[position], _mcb_page_start + position + 1)
            for position in MC_BINDER_RIGHT_POSITIONS)

        _mcb_grid_w = (MC_BINDER_COLS * MC_POCKET_W
            + (MC_BINDER_COLS - 1) * MC_POCKET_X_GAP)
        _mcb_left_x = MC_LEFT_LEAF_X + (MC_LEFT_LEAF_W - _mcb_grid_w) // 2
        _mcb_right_x = MC_RIGHT_LEAF_X + (MC_RIGHT_LEAF_W - _mcb_grid_w) // 2

        _mcb_prev = mc_sel_page - 1
        _mcb_next = mc_sel_page + 1
        _mcb_prev_ok = _mcb_prev >= 0
        _mcb_next_ok = _mcb_next < _mcb_page_count

        _mcb_prev_action = [
            SetScreenVariable("mc_page_direction", -1),
            SetScreenVariable("mc_hover_card", None),
            SetScreenVariable("mc_catalog_open", False),
            SetScreenVariable("mc_sel_page", _mcb_prev),
        ]
        _mcb_next_action = [
            SetScreenVariable("mc_page_direction", 1),
            SetScreenVariable("mc_hover_card", None),
            SetScreenVariable("mc_catalog_open", False),
            SetScreenVariable("mc_sel_page", _mcb_next),
        ]
        _mcb_catalog_toggle_action = [
            SetScreenVariable("mc_hover_card", None),
            SetScreenVariable("mc_catalog_open", not mc_catalog_open),
        ]
        if mc_catalog_open:
            _mcb_footer_text = "UP/DOWN  CHOOSE CATEGORY  /  ENTER  SELECT  /  C OR ESC  CLOSE"
        elif _mcb_hovered_card is not None:
            _mcb_footer_text = "CLICK TO INSPECT  /  %s" % _mcb_hovered_card.name.upper()
        elif _mcb_page_count > 1:
            _mcb_footer_text = "C  CHANGE CATEGORY  /  LEFT/RIGHT  TURN SPREAD  /  CLICK A CARD TO INSPECT"
        else:
            _mcb_footer_text = "C  CHANGE CATEGORY  /  CLICK A CARD TO INSPECT"

    key "game_menu" action (SetScreenVariable("mc_catalog_open", False) if mc_catalog_open else Hide("mc_collection", transition=enter_m_menu_doorway))
    key "K_ESCAPE" action (SetScreenVariable("mc_catalog_open", False) if mc_catalog_open else Hide("mc_collection", transition=enter_m_menu_doorway))
    key "K_c" action _mcb_catalog_toggle_action
    key "K_i" action _mcb_catalog_toggle_action

    if not mc_catalog_open:
        if _mcb_prev_ok:
            key "K_LEFT" action _mcb_prev_action
            key "K_PAGEUP" action _mcb_prev_action
        if _mcb_next_ok:
            key "K_RIGHT" action _mcb_next_action
            key "K_PAGEDOWN" action _mcb_next_action

    frame:
        style "archive_shell_frame"
        padding (24, 16)

        vbox:
            spacing 8

            use archive_header("CARD COLLECTION", Hide("mc_collection", transition=enter_m_menu_doorway), static=True)

            # Census strip. The right slot carries the wallet, because the
            # binder is the one place a player looks up "how close am I" and
            # "can I afford to keep going" in the same glance.
            use archive_readout(
                "THE BINDER / %d OF %d COLLECTED" % (_mcb_owned, _mcb_total),
                right_slot=True, static=True):

                use mc_balance_chip(15, light=True)

            # The binder is a real raster prop; pockets, cards, tabs and states
            # stay dynamic on top of its two blank leaves.
            fixed:
                xysize (1152, 520)

                add "assets/gui/menu/binder_spread.png"

                # Spread navigation. These are outer-edge page tabs now; the old
                # top-corner squares sat on the leather and fought the prop.
                if _mcb_prev_ok:
                    button:
                        style "mc_binder_nav_button"
                        xpos 12
                        ypos 228
                        sensitive (not mc_catalog_open)
                        keyboard_focus (not mc_catalog_open)
                        action _mcb_prev_action
                        text "<" style "mc_binder_nav_text" align (0.5, 0.5)

                if _mcb_next_ok:
                    button:
                        style "mc_binder_nav_button"
                        xpos 1088
                        ypos 228
                        sensitive (not mc_catalog_open)
                        keyboard_focus (not mc_catalog_open)
                        action _mcb_next_action
                        text ">" style "mc_binder_nav_text" align (0.5, 0.5)

                text "LEAF A" style "mc_binder_leaf_label" xpos 528 xanchor 1.0 ypos 42
                text "LEAF B" style "mc_binder_leaf_label" xpos 1064 xanchor 1.0 ypos 42

                # A page stamp is useful only when a category actually spans
                # multiple spreads. Single-spread categories stay visually quiet.
                if _mcb_page_count > 1:
                    text ("SPREAD %d / %d" % (mc_sel_page + 1, _mcb_page_count)):
                        style "mc_binder_spread_stamp"
                        xpos 1064
                        xanchor 1.0
                        ypos 8

                # Key the whole card layer to the divider. A subject change now
                # produces one short page motion rather than five independent
                # cards dropping into place.
                for _spread_key index _spread_key in ["%s-%d" % (_mcb_subject_id, mc_sel_page)]:
                    fixed:
                        xysize (1152, 520)
                        at mc_spread_enter(mc_page_direction)

                        grid MC_BINDER_COLS MC_BINDER_ROWS:
                            xpos _mcb_left_x
                            ypos MC_BINDER_GRID_Y
                            xspacing MC_POCKET_X_GAP
                            yspacing MC_POCKET_Y_GAP

                            for _slot_key, _card, _slot_number index _slot_key in _mcb_left_slots:
                                $ _mc_have = (_card is not None and _card.id in _mcb_owned_ids)
                                use mc_binder_slot(
                                    _card,
                                    have=_mc_have,
                                    is_new=(_card is not None and _card.id in _mcb_new_ids),
                                    lifted=(_card is not None and mc_hover_card == _card.id),
                                    hover_action=(SetScreenVariable("mc_hover_card", _card.id) if _card is not None else None),
                                    unhover_action=SetScreenVariable("mc_hover_card", None),
                                    open_action=([
                                        SetScreenVariable("mc_hover_card", None),
                                        Function(mc_card_seen, _card.id),
                                        Show("mc_card_detail", card=_card),
                                    ] if _mc_have else NullAction()),
                                    slot_number=_slot_number,
                                    allow_keyboard_focus=(not mc_catalog_open),
                                )

                        grid MC_BINDER_COLS MC_BINDER_ROWS:
                            xpos _mcb_right_x
                            ypos MC_BINDER_GRID_Y
                            xspacing MC_POCKET_X_GAP
                            yspacing MC_POCKET_Y_GAP

                            for _slot_key, _card, _slot_number index _slot_key in _mcb_right_slots:
                                $ _mc_have = (_card is not None and _card.id in _mcb_owned_ids)
                                use mc_binder_slot(
                                    _card,
                                    have=_mc_have,
                                    is_new=(_card is not None and _card.id in _mcb_new_ids),
                                    lifted=(_card is not None and mc_hover_card == _card.id),
                                    hover_action=(SetScreenVariable("mc_hover_card", _card.id) if _card is not None else None),
                                    unhover_action=SetScreenVariable("mc_hover_card", None),
                                    open_action=([
                                        SetScreenVariable("mc_hover_card", None),
                                        Function(mc_card_seen, _card.id),
                                        Show("mc_card_detail", card=_card),
                                    ] if _mc_have else NullAction()),
                                    slot_number=_slot_number,
                                    allow_keyboard_focus=(not mc_catalog_open),
                                )

                if mc_catalog_open:
                    button:
                        xysize (1152, 520)
                        background Solid("#01030894")
                        keyboard_focus False
                        action SetScreenVariable("mc_catalog_open", False)

                    # The accordion owns the left leaf while open. Its shield
                    # prevents blank panel clicks from closing through to the
                    # full-spread dimmer.
                    button:
                        xysize (420, MC_CATALOG_PANEL_H)
                        xpos 92
                        ypos 30
                        background Solid("#00000000")
                        keyboard_focus False
                        action NullAction()

                    frame:
                        style "mc_catalog_panel"
                        xpos 92
                        ypos 30
                        at mc_index_enter

                        vbox:
                            spacing 9

                            hbox:
                                xfill True
                                text "SELECT A CATEGORY" style "mc_binder_index_title" yalign 0.5
                                null width 1 xfill True
                                text "C / ESC  CLOSE" style "mc_binder_index_hint" yalign 0.5

                            add Solid("#d9cdb633") xysize (380, 1)

                            vbox:
                                spacing 3
                                for _idx, (_sid, _slabel) index _sid in enumerate(MC_SUBJECTS):
                                    $ _s_cards = MC_CARDS_BY_SUBJECT.get(_sid, ())
                                    $ _s_all = len(_s_cards)
                                    $ _s_done = sum(1 for card in _s_cards if card.id in _mcb_owned_ids)
                                    $ _s_new = any(card.id in _mcb_new_ids for card in _s_cards)

                                    button:
                                        style "mc_catalog_button"
                                        selected (_idx == mc_sel_subject)
                                        default_focus (_idx == mc_sel_subject)
                                        action (
                                            [SetScreenVariable("mc_catalog_open", False)]
                                            if _idx == mc_sel_subject else [
                                                SetScreenVariable("mc_page_direction", (-1 if _idx < mc_sel_subject else 1)),
                                                SetScreenVariable("mc_hover_card", None),
                                                SetScreenVariable("mc_sel_page", 0),
                                                SetScreenVariable("mc_sel_subject", _idx),
                                                SetScreenVariable("mc_catalog_open", False),
                                            ])

                                        fixed:
                                            xysize (376, 26)

                                            add Solid(IM_GOLD if _idx == mc_sel_subject else "#5a554f") xysize (4, 22) xpos 0 yalign 0.5

                                            hbox:
                                                spacing 6
                                                xpos 13
                                                yalign 0.5
                                                text _slabel style "mc_binder_index_name" yalign 0.5
                                                if _s_new:
                                                    add Solid("#ffb454") xysize (6, 6) yalign 0.5

                                            text ("%d/%d" % (_s_done, _s_all)):
                                                style "mc_binder_index_count"
                                                xanchor 1.0
                                                xpos 366
                                                yalign 0.5

                # One large, explicit divider tab replaces the ambiguous
                # CATALOG stub and the unrelated status plate. It remains above
                # the drawer dimmer, so the same control also closes the menu.
                button:
                    style "mc_binder_category_tab"
                    xpos 92
                    ypos -8
                    default_focus (not mc_catalog_open)
                    keyboard_focus (not mc_catalog_open)
                    action _mcb_catalog_toggle_action

                    fixed:
                        xysize (420, 38)
                        add Solid(IM_GOLD) xysize (4, 22) xpos 12 yalign 0.5

                        hbox:
                            spacing 10
                            xpos 26
                            yalign 0.5

                            text "CATEGORY" style "mc_binder_category_label" yalign 0.5
                            text _mcb_subject_label style "mc_binder_category_name" yalign 0.5
                            text ("%d/%d CARDS" % (_mcb_subject_owned, _mcb_subject_total)) style "mc_binder_category_meta" yalign 0.5
                        text ("CLOSE ^" if mc_catalog_open else "CHANGE >"):
                            style "mc_binder_category_action"
                            xanchor 1.0
                            xpos 405
                            yalign 0.5

            # Footer status line, matching the hub's.
            fixed:
                xsize 1150
                ysize 16

                add Solid(IM_PLUM) xysize (5, 5) xpos 0 yalign 0.5 rotate 45
                text _mcb_footer_text:
                    style "archive_footer_text"
                    xpos 13
                    yalign 0.5
                text ("PULLS %s" % mc_num(persistent.mc_pulls_total)):
                    style "archive_footer_text"
                    xanchor 1.0
                    xpos 1150
                    yalign 0.5

    use archive_shell_brackets()


# -----------------------------------------------------------------------------
# CARD DETAIL
# A card on its own, big, with its flavor line. Shown over the binder rather
# than inline so the complete two-page spread stays intact behind it.
# -----------------------------------------------------------------------------
screen mc_card_detail(card):
    modal True
    zorder 65

    python:
        _mc_ensure_cards()
        _mcd_subject = MC_SUBJECT_LABEL.get(card.subject, card.subject.upper())
        _mcd_owned = [
            candidate for candidate in MC_CARDS_BY_SUBJECT.get(card.subject, ())
            if candidate.id in persistent.mc_cards_owned
        ]
        _mcd_index = _mcd_owned.index(card) if card in _mcd_owned else 0
        _mcd_total = len(_mcd_owned)
        _mcd_prev = _mcd_owned[_mcd_index - 1] if _mcd_index > 0 else None
        _mcd_next = (_mcd_owned[_mcd_index + 1]
            if _mcd_index + 1 < len(_mcd_owned) else None)
        _mcd_prev_action = ([
            Function(mc_card_seen, _mcd_prev.id),
            Show("mc_card_detail", card=_mcd_prev),
        ] if _mcd_prev is not None else NullAction())
        _mcd_next_action = ([
            Function(mc_card_seen, _mcd_next.id),
            Show("mc_card_detail", card=_mcd_next),
        ] if _mcd_next is not None else NullAction())

    key "game_menu" action Hide("mc_card_detail")
    key "K_ESCAPE" action Hide("mc_card_detail")
    if _mcd_prev is not None:
        key "K_LEFT" action _mcd_prev_action
        key "K_PAGEUP" action _mcd_prev_action
    if _mcd_next is not None:
        key "K_RIGHT" action _mcd_next_action
        key "K_PAGEDOWN" action _mcd_next_action

    add Solid("#010308e6")

    # A transparent full-screen button closes the detail, while a second button
    # catches blank clicks inside the panel. A bare `dismiss` closed the card
    # when the player clicked non-interactive copy inside the detail itself.
    button:
        xfill True
        yfill True
        background Solid("#00000000")
        keyboard_focus False
        action Hide("mc_card_detail")

    button:
        xysize (920, 570)
        align (0.5, 0.5)
        background Solid("#00000000")
        keyboard_focus False
        action NullAction()

    frame:
        style "archive_panel"
        xalign 0.5
        yalign 0.5
        xysize (920, 570)
        padding (28, 24)
        at mc_detail_panel_in

        fixed:
            xysize (864, 522)

            # The generated shell is the object. The binder pocket remains
            # visible behind the modal, where it physically belongs.
            fixed:
                xysize (MC_DETAIL_CARD_W, MC_DETAIL_CARD_H)
                xpos 8
                yalign 0.5
                at mc_detail_card_in

                use mc_card_face(
                    card, MC_DETAIL_CARD_W, MC_DETAIL_CARD_H,
                    radius=11.0, show_title=True)

            add Solid(card.color + "66") xysize (2, 452) xpos 334 yalign 0.5

            vbox:
                xpos 364
                ypos 22
                xsize 486
                ysize 478
                spacing 11

                hbox:
                    xfill True
                    text ("THE BINDER  /  " + _mcd_subject):
                        style "mc_detail_kicker"
                        color IM_PLUM
                    null width 1 xfill True
                    text ("ENTRY %d / %d" % (_mcd_index + 1, _mcd_total)):
                        style "mc_detail_kicker"
                        color IM_PLUM

                hbox:
                    spacing 9
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

                text "ARCHIVE NOTES" style "mc_detail_section"

                add Solid(card.color + "aa") xysize (220, 2) at enter_m_accent_grow

                frame:
                    background IM_PAPER_PANEL
                    padding (18, 15)
                    xfill True

                    text card.flavor:
                        style "mc_detail_flavor"
                        xsize 454

                null height 2

                fixed:
                    xysize (486, 62)

                    vbox:
                        spacing 3
                        text "DUPLICATE VALUE" style "archive_meta_text"
                        hbox:
                            spacing 7
                            add MatsucoinIcon(13) yalign 0.5
                            text str(card.refund) style "mc_detail_stat" yalign 0.5

                # Keep navigation at the foot of the metadata column, aligned
                # with the physical card instead of floating below the notes.
                null height 1 yfill True

                add Solid("#d9cdb633") xysize (486, 1)

                hbox:
                    spacing 12
                    xalign 0.5

                    textbutton _("< Previous"):
                        style "mc_detail_nav_button"
                        sensitive (_mcd_prev is not None)
                        action _mcd_prev_action

                    textbutton _("Close"):
                        style "archive_return_button"
                        default_focus True
                        action Hide("mc_card_detail")

                    textbutton _("Next >"):
                        style "mc_detail_nav_button"
                        sensitive (_mcd_next is not None)
                        action _mcd_next_action

    use archive_bookplate_corners(180, 75, 920, 570)


# =============================================================================
# STYLES
# Archive chrome: the illustrated catalogue's dark panels, paper ink and cloth
# tabs. The coin and the NEW badge keep their own colours -- both are Arcade
# objects that have wandered in, and should read that way.
# =============================================================================
style mc_binder_nav_button:
    xysize (52, 64)
    padding (0, 0)
    background IM_TAB_IDLE
    hover_background IM_TAB_HOVER
    insensitive_background IM_TAB_IDLE
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mc_binder_nav_text is gui_text:
    font gui.interface_font
    size 28
    color IM_PAPER
    hover_color "#ffffff"
    insensitive_color "#6f6a63"
    outlines []

# The divider tab: a strip of the same cloth the Archive's index tabs are cut
# from, standing proud of the binder's pale leaf.
style mc_binder_category_tab:
    xysize (420, 38)
    padding (0, 0)
    background Frame("assets/gui/menu/illustrated/credits/section_tab_selected.svg", 12, 10, 12, 10)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

# These are deliberately standalone styles. Inheriting gui_text here lets
# unrelated global UI colour/state changes darken the tab's children.
style mc_binder_category_label:
    font gui.interface_font
    size 9
    color "#d9c9a8"
    kerning 1.6
    hover_color IM_PAPER
    outlines []

style mc_binder_category_name:
    font gui.default_font
    size 18
    color IM_PAPER
    xmaximum 150
    hover_color "#ffffff"
    outlines []

style mc_binder_category_meta:
    font gui.interface_font
    size 10
    color "#d9c9a8"
    kerning 1.0
    hover_color IM_PAPER
    outlines []

style mc_binder_category_action:
    font gui.interface_font
    size 10
    color IM_GOLD
    hover_color "#ffffff"
    kerning 1.0
    outlines []

style mc_binder_leaf_label is gui_text:
    font gui.interface_font
    size 10
    color "#233745"
    bold True
    kerning 2.0
    outlines [(1, "#dce4ea88", 0, 0)]

style mc_binder_spread_stamp is gui_text:
    font gui.interface_font
    size 10
    color "#233745"
    bold True
    kerning 1.4
    outlines [(1, "#dce4ea88", 0, 0)]

style mc_catalog_panel is empty:
    xysize (420, MC_CATALOG_PANEL_H)
    padding (20, 16)
    background IM_DARK_PANEL

style mc_binder_index_title is gui_text:
    font gui.default_font
    size 21
    color IM_PAPER
    outlines []

style mc_binder_index_hint is gui_text:
    font gui.interface_font
    size 9
    kerning 1.0
    color IM_PLUM
    outlines []

style mc_catalog_button:
    xysize (380, 28)
    padding (2, 1)
    background None
    hover_background Solid("#d9cdb614")
    selected_background Solid("#d9cdb622")
    selected_hover_background Solid("#d9cdb62e")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mc_binder_index_name is gui_text:
    font gui.default_font
    size 17
    color IM_PAPER
    xmaximum 255
    outlines []

style mc_binder_index_count is gui_text:
    font gui.interface_font
    size 11
    color "#bdb4a6"
    outlines []

style mc_thumb_button:
    background Solid("#07111d00")
    hover_background Solid("#07111d00")
    padding (0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

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

style mc_empty_slot_number is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 18
    color "#51667488"
    bold True
    outlines [(1, "#e9eef233", 0, 0)]

style mc_empty_slot_label is gui_text:
    font gui.interface_font
    size 8
    color "#53687699"
    kerning 1.5
    outlines [(1, "#eef2f433", 0, 0)]

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

style mc_detail_section:
    font gui.default_font
    size 22
    color IM_PAPER
    outlines []

style mc_detail_flavor is gui_text:
    font gui.default_font
    size 16
    color IM_INK
    line_spacing 3
    outlines []

style mc_detail_stat is gui_text:
    font gui.interface_font
    size 17
    color IM_PAPER
    outlines []

style mc_detail_nav_button is archive_return_button:
    xsize 140
    ysize 42
    padding (10, 8)

style mc_detail_nav_button_text is archive_return_button_text:
    size 16
