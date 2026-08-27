# =============================================================================
# party_select.rpy  --  MATSUDA'S SICK BOSS FIGHT :: THE CYLINDER
# =============================================================================
#
# WHAT THIS IS
#   The seven-character party picker, rebuilt as a REVOLVER CYLINDER. It was a
#   scrolling list of seven rows with stat bars -- a spreadsheet with faces on
#   it. Nothing about that said anything about the fight it opens.
#
#   Now the roster is a machined steel cylinder with seven chambers. You index
#   it round, one click per press, and the chamber under the hammer is the one
#   you are reading. Confirm chambers that round; confirm again and you eject
#   it. Four loaded and the weapon is ready.
#
#   The metaphor is doing real work, not just decoration:
#     * A revolver indexes in DISCRETE CLICKS, which is exactly what a keyboard
#       cursor does. There is no smooth tween anywhere in here and there should
#       not be -- the snap IS the mechanism, and it is why this reads as solid
#       rather than as a carousel that happens to be round.
#     * A cylinder has a fixed number of chambers. Seven roster members, seven
#       chambers, and the "four of seven" limit becomes something you can see.
#     * There is exactly one reading position, so there is exactly one dossier
#       on screen instead of seven competing summaries.
#
# WHAT IT SHARES WITH THE OLD SCREEN
#   All of it, underneath. Same `picks` / `rows` state, same
#   msbf_select_member / msbf_remove_member / msbf_toggle_row / msbf_can_begin /
#   msbf_party_config helpers, same Return value. Nothing downstream of this
#   screen knows it changed.
#
# GEOMETRY WARNING
#   msbf.cylinder draws the seven BORES, and this file positions the seven
#   portraits into them. Those are two separate pieces of arithmetic that must
#   agree, so both read MSBF_CYL_RING / MSBF_CYL_BORE and the top-dead-centre
#   convention below. Change one without the other and the faces float off
#   their sockets.
# =============================================================================

# -----------------------------------------------------------------------------
# 1. THE CYLINDER SHADER
# -----------------------------------------------------------------------------
init -10 python:

    def _msbf_register_cylinder_shader():

        # One draw for the whole machined assembly: disc, brushed grain, the
        # concentric turning marks, a knurled rim, seven bored chambers with
        # bevels, brass in whichever ones are loaded, the index notch and the
        # centre pin.
        #
        # u_cy_loaded is a BITMASK OVER POSITIONS, not over roster members --
        # bit 0 is top-dead-centre and they run clockwise. Positions are what
        # the shader knows about; which member is currently sitting in which
        # position is the screen's business, and it hands the mask over already
        # rotated. That split is what lets the cylinder index without the
        # shader needing to know the roster exists.
        renpy.register_shader("msbf.cylinder", variables="""
            uniform float u_time;
            uniform float u_cy_loaded;
            uniform float u_cy_ring;
            uniform float u_cy_bore;
            uniform vec3 u_cy_accent;
            uniform float u_cy_ready;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            const float CY_TAU = 6.2831853;
            vec2 c = (v_tex_coord - vec2(0.5)) * 2.0;
            float r = length(c);
            float ang = atan(c.y, c.x);
            float t = u_time;

            // --- the disc ------------------------------------------------
            float body = smoothstep(1.0, 0.978, r);

            float grain = 0.5 + 0.5 * sin(ang * 150.0 + r * 9.0);
            float grain2 = 0.5 + 0.5 * sin(ang * 63.0 - r * 17.0);
            vec3 steel = mix(vec3(0.075, 0.088, 0.108),
                            vec3(0.215, 0.240, 0.280),
                            0.30 + 0.34 * grain + 0.22 * grain2);

            // lit from the upper left, like every piece of gunmetal ever shot
            vec2 nl = c / max(r, 0.0001);
            float lit = 0.5 + 0.5 * dot(nl, normalize(vec2(-0.62, -0.78)));
            steel *= 0.48 + 0.78 * lit;

            // concentric turning marks
            float turn = smoothstep(0.040, 0.0, abs(fract(r * 15.0) - 0.5) - 0.45);
            steel += vec3(0.055, 0.060, 0.070) * turn;

            // knurled outer rim
            float rimBand = smoothstep(0.855, 0.905, r) * smoothstep(1.0, 0.955, r);
            float knurl = 0.5 + 0.5 * sin(ang * 96.0);
            steel = mix(steel, vec3(0.30, 0.335, 0.395) * (0.55 + 0.62 * knurl), rimBand);
            // and a bright edge where the rim turns over
            steel += vec3(0.20) * smoothstep(0.010, 0.0, abs(r - 0.905)) * (0.4 + 0.6 * lit);

            // --- the seven bores -----------------------------------------
            float bore = 0.0;
            float bevel = 0.0;
            float brass = 0.0;
            float primer = 0.0;
            for (int p = 0; p < 7; p++) {
                float a = -1.5707963 + float(p) * (CY_TAU / 7.0);
                vec2 bc = vec2(cos(a), sin(a)) * u_cy_ring;
                vec2 dv = c - bc;
                float d = length(dv);

                bore = max(bore, smoothstep(u_cy_bore, u_cy_bore - 0.010, d));

                // bevel: bright on the lit side of the socket lip, dark opposite
                float lipmask = smoothstep(0.026, 0.0, abs(d - u_cy_bore));
                float lipdir = dot(dv / max(d, 0.0001), normalize(vec2(-0.62, -0.78)));
                bevel += lipmask * lipdir;

                // Bit p of u_cy_loaded. The epsilon is a float-precision guard
                // and must stay TINY: a rounding nudge of 0.5 shifts the bit
                // boundary a whole half-place, and with two rounds loaded that
                // lit a third, empty chamber in brass.
                float bit = mod(floor(u_cy_loaded / pow(2.0, float(p)) + 0.002), 2.0);
                brass = max(brass, smoothstep(0.020, 0.0, abs(d - u_cy_bore * 0.90)) * bit);
                primer = max(primer, smoothstep(u_cy_bore * 0.30, u_cy_bore * 0.24, d) * bit);
            }

            vec3 col = steel;
            col = mix(col, vec3(0.018, 0.022, 0.032), bore);
            col += vec3(0.26, 0.28, 0.33) * clamp(bevel, -1.0, 1.0);
            col += u_cy_accent * brass * 1.55;
            col += u_cy_accent * primer * 0.55;

            // NO index notch. It used to be drawn here at top dead centre,
            // which was fine while the disc was static -- but the disc turns
            // now, and a notch that turns with it is not a mark, it is just
            // another moving part. The hammer on the frame does that job.

            // --- centre pin ----------------------------------------------
            float pin = smoothstep(0.128, 0.112, r);
            float pinLip = smoothstep(0.014, 0.0, abs(r - 0.120));
            col = mix(col, vec3(0.16, 0.18, 0.215) * (0.5 + 0.9 * lit), pin);
            col += vec3(0.22) * pinLip * (0.3 + 0.7 * lit);
            // a slow bloom on the pin once the cylinder is full
            col += u_cy_accent * pin * u_cy_ready * (0.22 + 0.16 * sin(t * 2.4));

            gl_FragColor = vec4(col * body, body);
        """)

    try:
        _msbf_register_cylinder_shader()
        MSBF_CYL_SHADER = True
    except Exception as _msbf_cyl_e:
        MSBF_CYL_SHADER = False
        if config.developer:
            renpy.log("MSBF CYL: shader registration failed: %r" % (_msbf_cyl_e,))


# -----------------------------------------------------------------------------
# 2. GEOMETRY
# -----------------------------------------------------------------------------
init -1 python:

    # The cylinder, in screen pixels, and the two ratios the shader shares.
    MSBF_CYL_CX = 356
    MSBF_CYL_CY = 402
    MSBF_CYL_R = 208
    MSBF_CYL_RING = 0.615      # chamber ring radius, in units of R
    MSBF_CYL_BORE = 0.208      # bore radius, in units of R
    MSBF_CYL_SLOTS = 7

    def msbf_cyl_chamber_pos(position):
        """Screen centre of the bore at `position`, 0 = top dead centre.

        Must stay in step with the identical loop in msbf.cylinder -- see the
        geometry warning at the top of this file.
        """
        import math
        a = -math.pi / 2.0 + (position * (2.0 * math.pi / MSBF_CYL_SLOTS))
        rr = MSBF_CYL_R * MSBF_CYL_RING
        return (int(MSBF_CYL_CX + rr * math.cos(a)),
                int(MSBF_CYL_CY + rr * math.sin(a)))

    def msbf_cyl_bore_px():
        return int(MSBF_CYL_R * MSBF_CYL_BORE)

    def msbf_cyl_position_of(roster_index, selected, count):
        """Where roster member `roster_index` currently sits on the cylinder.

        Indexing the cylinder does not move the members; it moves WHICH member
        is at top dead centre. So a member's position is simply how far round
        they are from the selection.
        """
        if not count:
            return 0
        return (roster_index - selected) % count

    def msbf_cyl_spin_to(new_sel, n):
        """Index the cylinder to `new_sel` and arm the swing that shows it.

        Writes three things into the live screen scope: the new selection, the
        angle the assembly should appear to have come FROM, and a token that
        forces the swing ATL to restart (it will not restart on its own when
        you index twice the same way -- see the note on msbf_cyl_swing).

        The delta is taken the SHORT way round, so stepping from chamber 6 to
        chamber 0 swings one click forward rather than six backward.
        """
        cs = renpy.current_screen()
        if cs is None or not n:
            return
        try:
            cur = int(cs.scope.get("sel", 0) or 0)
        except (TypeError, ValueError):
            cur = 0
        new_sel = int(new_sel) % n
        d = (new_sel - cur) % n
        if d > n // 2:
            d -= n
        cs.scope["sel"] = new_sel
        # Positions run (index - sel), so a HIGHER sel moves every face one
        # step towards top dead centre -- the wheel turns anticlockwise, and
        # the swing therefore starts clockwise of where it lands.
        cs.scope["spin"] = d * (360.0 / n)
        cs.scope["spin_tok"] = int(cs.scope.get("spin_tok", 0) or 0) + 1
        cs.scope["kb_active"] = True
        renpy.restart_interaction()

    def msbf_cyl_turn(delta, n):
        """Index by `delta` chambers from wherever the cylinder is now."""
        cs = renpy.current_screen()
        if cs is None or not n:
            return
        try:
            cur = int(cs.scope.get("sel", 0) or 0)
        except (TypeError, ValueError):
            cur = 0
        msbf_cyl_spin_to(cur + delta, n)

    def msbf_cyl_loaded_mask(picks, selected):
        """picks -> a bitmask over POSITIONS for u_cy_loaded.

        Rotated here rather than in the shader, because the roster order is
        this screen's concept and the shader only knows about seven holes.
        """
        total = 0
        n = len(MSBF_ROSTER)
        for idx, entry in enumerate(MSBF_ROSTER):
            if entry["id"] in picks:
                total += 1 << msbf_cyl_position_of(idx, selected, n)
        return float(total)


# -----------------------------------------------------------------------------
# 3. TRANSFORMS
# -----------------------------------------------------------------------------

transform msbf_cyl_t(loaded=0.0, accent=(1.0, 0.78, 0.42), ready=0.0):
    mesh True
    shader "msbf.cylinder"
    u_cy_loaded loaded
    u_cy_ring MSBF_CYL_RING
    u_cy_bore MSBF_CYL_BORE
    u_cy_accent accent
    u_cy_ready ready

# --- THE TURN ----------------------------------------------------------------
# The cylinder has to be SEEN to rotate. Without it the faces simply teleport
# between sockets and the whole mechanism stops being legible -- you cannot tell
# a wheel that turned from a list that redrew.
#
# The chambers are laid out for the position they have ALREADY indexed to, and
# the assembly then swings from one chamber-step behind back to zero. So the
# rest state is exactly the static layout (nothing to keep in sync) and the
# animation is a pure one-shot that always starts and ends at known values.
#
# WHY `tok` IS USED RATHER THAN JUST PASSED. Matsu'Py restarts an ATL in a screen
# only when a variable the block actually REFERENCES changes value
# (atl.py take_execution_state -> variables_equal over find_loaded_variables).
# Index twice in the same direction and `step` is identical both times, so an
# unreferenced token would not force the restart and the second click would not
# animate at all. Here `tok` picks which way the settle overshoots, so it is a
# genuinely loaded variable -- and the alternating bounce is a better mechanism
# noise than a symmetrical one anyway.
transform msbf_cyl_swing(step=0.0, tok=0):
    subpixel True
    rotate step
    easeout 0.19 rotate (0.7 if (tok % 2) else -0.7)
    easeout 0.09 rotate 0.0

# The faces ride the assembly round but must stay upright, so each one takes the
# exact inverse of the swing about its own centre.
transform msbf_cyl_unswing(step=0.0, tok=0):
    subpixel True
    rotate -step
    easeout 0.19 rotate (-0.7 if (tok % 2) else 0.7)
    easeout 0.09 rotate 0.0

# The chamber arriving at top dead centre. A revolver does not glide into
# battery, it SEATS -- so this is a hard scale overshoot and a flash, keyed on
# the selection so it restarts every click.
transform msbf_cyl_seat(token=0):
    subpixel True
    zoom 1.18
    alpha 0.35
    easeout 0.09 zoom 0.97 alpha 1.0
    easeout 0.11 zoom 1.0

transform msbf_cyl_seat_flash(token=0):
    alpha 0.85
    easeout 0.34 alpha 0.0

# The hammer above the chamber: it drops a hair on each index and comes back.
transform msbf_cyl_hammer(token=0):
    subpixel True
    yoffset -7
    easeout 0.07 yoffset 2
    easeout 0.18 yoffset 0

# A chamber that is neither selected nor loaded sits back in the dark.
transform msbf_cyl_rest:
    subpixel True
    zoom 1.0


# -----------------------------------------------------------------------------
# 4. THE SCREEN
# -----------------------------------------------------------------------------
# NAVIGATION -- ONE VERTICAL FOCUS RING AND ONE WHEEL. There are no zones.
#
#   LEFT / RIGHT (A/D)  index the cylinder. ALWAYS, from anywhere. It is the
#                       wheel; it is never not the wheel.
#   UP / DOWN (W/S)     walk a single top-to-bottom list of everything you can
#                       act on: the cylinder, then each loaded round, then
#                       READY. It wraps.
#   Z                   acts on whatever the focus is sitting on -- chamber or
#                       eject on the cylinder, flip the row on a round, start
#                       the fight on READY.
#   X                   ejects. The focused member from the cylinder, or that
#                       round from the list.
#
# The first version had a three-zone graph where left/right sometimes indexed
# the cylinder and sometimes moved between rounds, and UP from the cylinder
# went to READY -- which is drawn BELOW it. Every direction key meant something
# different depending on invisible state, which is exactly the "maps very
# weirdly" complaint. Now each axis has exactly one job: horizontal turns the
# wheel, vertical walks the list, and the list runs down the screen in the
# order the eye already reads it.
# -----------------------------------------------------------------------------
screen msbf_party_select():
    modal True
    use enter_m_input_lock()

    default picks = []
    default rows = msbf_default_rows(picks)
    default sel = 0
    # focus 0 = the cylinder, 1..4 = the loaded rounds, 5 = READY.
    default focus = 0
    # The swing: how far the assembly appears to have come, and a token that
    # makes the ATL replay even when you index the same way twice.
    default spin = 0.0
    default spin_tok = 0
    # Which chamber the POINTER is over. The hit layer is invisible and static
    # while the faces ride a rotating container, so the button cannot light
    # itself -- it reports here and the visual layer does the lighting.
    default hover_ri = None

    $ _n = len(MSBF_ROSTER)
    $ _sel = max(0, min(sel, _n - 1))
    $ _pick_count = len(picks)
    $ _front_count = msbf_front_count(picks, rows)
    $ _ready = msbf_can_begin(picks, rows)

    # The focus ring, built from what actually exists right now: the cylinder,
    # one stop per LOADED round, and READY. Ejecting a round shortens the ring,
    # so the focus is clamped into it rather than left pointing at a gone slot.
    $ _stops = [0] + [1 + _i for _i in range(_pick_count)] + [5]
    $ _focus = focus if focus in _stops else 0
    $ _slot = (_focus - 1) if 1 <= _focus <= 4 else 0

    $ _entry = MSBF_ROSTER[_sel]
    $ _id = _entry["id"]
    $ _in_deck = _id in picks
    $ _locked = (not _in_deck) and _pick_count >= 4
    $ _accent = msbf_roster_accent(_sel)
    $ _accent_rgb = msbf_hex_rgb(_accent)
    $ _bore = msbf_cyl_bore_px()
    # The face sits INSIDE the bore, so the machined lip and the brass of a
    # loaded round stay visible as a ring around it.
    $ _face = int(_bore * 1.66)
    $ _slot_id = picks[_slot] if _pick_count else None

    # --- actions -------------------------------------------------------------
    $ _act_load = [SetScreenVariable("picks", msbf_select_member(picks, rows, _id)[0]), SetScreenVariable("rows", msbf_select_member(picks, rows, _id)[1])]
    $ _act_eject_sel = [SetScreenVariable("picks", msbf_remove_member(picks, rows, _id)[0]), SetScreenVariable("rows", msbf_remove_member(picks, rows, _id)[1])]
    $ _act_slot_row = SetScreenVariable("rows", msbf_toggle_row(picks, rows, _slot_id)) if _slot_id else NullAction()
    $ _act_slot_eject = [SetScreenVariable("picks", msbf_remove_member(picks, rows, _slot_id)[0]), SetScreenVariable("rows", msbf_remove_member(picks, rows, _slot_id)[1]), SetScreenVariable("focus", 0 if _pick_count <= 1 else min(_focus, _pick_count - 1))] if _slot_id else NullAction()
    $ _act_begin = Return(msbf_party_config(picks, rows)) if _ready else NullAction()

    # Indexing is RELATIVE off the live scope for the same reason the battle
    # deck's cursor is -- holding a key repeats faster than the screen
    # re-executes, and a precomputed destination makes the cylinder stall and
    # then jump several chambers at once. See msbf_kb_step in ui.rpy.
    # The wheel. Relative off the live scope, so holding the key steps one
    # chamber per repeat instead of stalling and jumping (see msbf_kb_step).
    $ _nav_prev = Function(msbf_cyl_turn, -1, _n)
    $ _nav_next = Function(msbf_cyl_turn, 1, _n)

    # The vertical ring. Walked by INDEX INTO _stops rather than by value, so
    # "the next thing down" is always the next thing that exists.
    $ _fi = _stops.index(_focus)
    $ _nav_up = SetScreenVariable("focus", _stops[(_fi - 1) % len(_stops)])
    $ _nav_down = SetScreenVariable("focus", _stops[(_fi + 1) % len(_stops)])

    $ _act_confirm = _act_begin if _focus == 5 else (_act_slot_row if _focus else (_act_load if not _locked else NullAction()))
    $ _act_back = _act_slot_eject if (1 <= _focus <= 4) else ((_act_eject_sel if _in_deck else NullAction()) if _focus == 0 else NullAction())

    use msbf_arena_static(1, 0.68)

    key "game_menu" action ShowMenu("save")
    key "K_ESCAPE" action ShowMenu("save")
    use msbf_nav_keys(_nav_up, _nav_down, _nav_prev, _nav_next, _act_confirm, _act_back)

    # =========================================================================
    # HEADER
    # =========================================================================
    use msbf_hud_scrim(0, 0, 900, 190, 1.0, 0.66, 1.0)

    text "VS. ONTOLOGICAL SEER" style "msbf_title":
        xpos 48
        ypos 28
    text "Select a party of four. One of them has to take the front." style "msbf_subtitle":
        xpos 50
        ypos 74

    use msbf_hud_scrim(940, 0, 340, 150, 1.0, 0.7, -1.0)
    text "SELECTED" style "msbf_tempo_kicker":
        xanchor 1.0
        xpos 1232
        ypos 30
    text "[_pick_count] / 4" style "msbf_cyl_count":
        xanchor 1.0
        xpos 1232
        ypos 48

    # =========================================================================
    # THE CYLINDER
    #
    # TWO LAYERS, and the split is deliberate. The ROTATING layer is the disc
    # and the faces and is purely visual; the HIT layer is seven invisible
    # buttons at the settled positions and never moves. Rotating a container in
    # Matsu'Py moves its children's pixels, but hit-testing through a rotation is
    # not something to stake a click on -- and during a 0.28s swing nobody is
    # aiming at a moving chamber anyway.
    # =========================================================================
    $ _cyl_x0 = MSBF_CYL_CX - MSBF_CYL_R
    $ _cyl_y0 = MSBF_CYL_CY - MSBF_CYL_R

    # ANCHORED BY ITS CENTRE, not its top-left. Matsu'Py pads a rotated render out
    # to the rotated bounding box, so a container pinned by its top-left walks
    # down and to the right as it turns -- the whole assembly slid out from
    # under the hammer. A centre anchor grows the padding symmetrically and the
    # axle stays where the axle is.
    fixed:
        xcenter MSBF_CYL_CX
        ycenter MSBF_CYL_CY
        xysize (MSBF_CYL_R * 2, MSBF_CYL_R * 2)
        at msbf_cyl_swing(spin, spin_tok)

        if MSBF_CYL_SHADER:
            add Solid("#00000000") at msbf_cyl_t(msbf_cyl_loaded_mask(picks, _sel), (1.0, 0.78, 0.42), (1.0 if _ready else 0.0)):
                xysize (MSBF_CYL_R * 2, MSBF_CYL_R * 2)
        else:
            add Solid("#12161cf0") xysize (MSBF_CYL_R * 2, MSBF_CYL_R * 2)

        for _ri, _rentry in enumerate(MSBF_ROSTER):
            $ _pos = msbf_cyl_position_of(_ri, _sel, _n)
            $ _px, _py = msbf_cyl_chamber_pos(_pos)
            $ _rid = _rentry["id"]
            $ _rloaded = _rid in picks
            $ _rtop = (_pos == 0)
            $ _rmug = msbf_roster_mug(_rid)
            $ _rorder = picks.index(_rid) if _rloaded else -1
            $ _rhover = (hover_ri == _ri) and not kb_active and not _rtop

            fixed:
                xcenter (_px - _cyl_x0)
                ycenter (_py - _cyl_y0)
                xysize (_face, _face)
                # The faces ride the wheel round but stay upright.
                at msbf_cyl_unswing(spin, spin_tok)

                fixed:
                    xysize (_face, _face)
                    at (msbf_cyl_seat(_sel) if _rtop else msbf_cyl_rest)

                    # ROUND, because the sockets are round. phone_round applies
                    # enter_m.roundmask (the phone system's corner rounder) at a
                    # radius of half the box -- a square crop dropped into a
                    # bored hole shows four hard corners sticking out of the
                    # steel and the assembly stops reading as machined.
                    if _rmug is not None:
                        add ArchivePortraitCrop(_rmug[0], _face, _face, _rmug[3], _rmug[2], _rmug[1], _rmug[4]):
                            at phone_round(_face // 2)
                            alpha (1.0 if (_rtop or _rloaded) else 0.55)
                            matrixcolor (SaturationMatrix(1.0) if (_rtop or _rloaded) else SaturationMatrix(0.2))
                    else:
                        add Solid("#0a1018") xysize (_face, _face) at phone_round(_face // 2)

                    if _rloaded:
                        add Solid("#ffcf6626") xysize (_face, _face) at phone_round(_face // 2)
                    if not _rtop and not _rloaded:
                        add Solid("#02060c77") xysize (_face, _face) at phone_round(_face // 2)

                    # POINTER HOVER. Only while the mouse owns the highlight --
                    # a pointer parked on a chamber must not keep lighting it
                    # while the keyboard indexes somewhere else.
                    if _rhover:
                        add Solid("#9becff3a") xysize (_face, _face) at phone_round(_face // 2)
                        if MSBF_FX_SHADERS:
                            add Solid("#00000000") xysize (_face + 26, _face + 26) at msbf_fx_glow_pulse((0.61, 0.93, 1.0), 0.32, 0.66, 2.0):
                                xcenter _face // 2
                                ycenter _face // 2

                # Turn order, so the firing sequence is readable on the wheel
                # itself. Inside the unswung box, so it stays upright too.
                if _rloaded:
                    fixed:
                        xpos _face - 14
                        ypos _face - 16
                        xysize (20, 20)
                        add Solid("#0a0d12ee") xysize (20, 20)
                        add Solid("#ffcf66") xysize (20, 2)
                        text "[_rorder]" style "msbf_cyl_pip":
                            xalign 0.5
                            yalign 0.5

    # The hit layer: static, invisible, and always at the settled positions.
    for _ri, _rentry in enumerate(MSBF_ROSTER):
        $ _hpos = msbf_cyl_position_of(_ri, _sel, _n)
        $ _hpx, _hpy = msbf_cyl_chamber_pos(_hpos)
        button:
            xcenter _hpx
            ycenter _hpy
            xysize (_face, _face)
            background None
            padding (0, 0)
            hover_sound MSBF_UI_SFX["hover"]
            activate_sound MSBF_UI_SFX["accept"]
            hovered [SetScreenVariable("hover_ri", _ri), SetScreenVariable("kb_active", False)]
            unhovered SetScreenVariable("hover_ri", None)
            action [SetScreenVariable("focus", 0), SetScreenVariable("kb_active", False), Function(msbf_cyl_spin_to, _ri, _n)]

    # The seating flash on whichever chamber just arrived.
    if MSBF_FX_SHADERS:
        $ _tx, _ty = msbf_cyl_chamber_pos(0)
        add Solid("#00000000") xysize (_bore * 3, _bore * 3) at msbf_fx_glow_t((1.0, 0.86, 0.55), 0.9, 1.6), msbf_cyl_seat_flash(_sel):
            xcenter _tx
            ycenter _ty

    # The hammer. On the FRAME, not on the cylinder, so it does not turn -- it
    # is the fixed mark the chambers index up to.
    $ _hx, _hy = msbf_cyl_chamber_pos(0)
    fixed:
        xcenter _hx
        ycenter (_hy - _bore - 26)
        xysize (44, 44)
        at msbf_cyl_hammer(spin_tok)
        # a stepped wedge -- the project's fonts have no usable triangle glyph
        # (every arrow character renders as tofu), so the pointer is built.
        add Solid("#e6edf4") xysize (30, 5):
            xalign 0.5
            ypos 6
        add Solid("#cdd7e0") xysize (22, 5):
            xalign 0.5
            ypos 11
        add Solid("#aeb9c4") xysize (14, 5):
            xalign 0.5
            ypos 16
        add Solid("#ffcf66") xysize (7, 6):
            xalign 0.5
            ypos 21


    # =========================================================================
    # THE DOSSIER -- one member, the one under the hammer
    # =========================================================================
    use msbf_hud_scrim(600, 112, 680, 300, 1.0, 0.5, 0.0, 0.82)

    $ _hero = msbf_roster_portrait(_id)
    if _hero is not None:
        add ArchivePortraitCrop(_hero[0], 196, 252, 0.0, _hero[2], _hero[1]):
            xpos 622
            ypos 126
        add Solid(_accent) xysize (196, 3):
            xpos 622
            ypos 126

    text _entry["name"] style "msbf_cyl_name":
        xpos 844
        ypos 126
        xmaximum 380
    text _entry["role"] style "msbf_cyl_role":
        color _accent
        xpos 846
        ypos 168
    text _entry["summary"] style "msbf_cyl_summary":
        xpos 846
        ypos 194
        xmaximum 372

    grid 2 2:
        xpos 846
        ypos 238
        spacing 8
        use msbf_select_stat_bar("HP", _entry["max_hp"], 700, "#66e08a")
        use msbf_select_stat_bar("ATK", _entry["offense"], 90, "#ffcf66")
        use msbf_select_stat_bar("MAG", _entry["magic"], 80, "#82a6ff")
        use msbf_select_stat_bar("SPD", _entry["agility"], 76, "#ff6b8e")

    if _in_deck:
        # Precomputed: Matsu'Py's text interpolation reads "[picks.index(_id)]" as
        # an ATTRIBUTE called "index(_id)", not as a call.
        $ _deck_pos = picks.index(_id)
        text "SELECTED  #[_deck_pos]" style "msbf_cyl_state_in":
            xpos 846
            ypos 302
    elif _locked:
        text "CYLINDER FULL" style "msbf_cyl_state_lock":
            xpos 846
            ypos 302
    else:
        text "READY TO SELECT" style "msbf_cyl_state_free":
            xpos 846
            ypos 302

    textbutton (("EJECT" if _in_deck else "SELECT")):
        style "msbf_cyl_action"
        keyboard_focus False
        xpos 846
        ypos 334
        sensitive (_in_deck or not _locked)
        hover_sound MSBF_UI_SFX["hover"]
        activate_sound (MSBF_UI_SFX["denied"] if _in_deck else MSBF_UI_SFX["accept"])
        action [SetScreenVariable("focus", 0), SetScreenVariable("kb_active", False)] + (_act_eject_sel if _in_deck else _act_load)

    # =========================================================================
    # THE LOADED ROUNDS
    # =========================================================================
    use msbf_hud_scrim(600, 420, 680, 300, 0.0, 1.1, 0.0, 0.84)

    text "FIRING ORDER" style "msbf_tempo_kicker":
        xpos 622
        ypos 432
    text "FRONT [_front_count]" style "msbf_cyl_front":
        xanchor 1.0
        xpos 1256
        ypos 432

    for _si in range(4):
        $ _sy = 458 + _si * 44
        $ _has = _si < _pick_count
        $ _sid = picks[_si] if _has else None
        $ _sfocus = (_focus == _si + 1)

        if _has:
            $ _sentry = MSBF_ROSTER_BY_ID[_sid]
            $ _smug = msbf_roster_mug(_sid)
            $ _srow = rows.get(_sid, "front")
            button:
                xpos 622
                ypos _sy
                xysize (634, 40)
                # padding MUST be zero. The default button style pads, and the
                # background is drawn at the padded size while the focus border
                # inside is drawn at 634x40 -- so the highlight sat a few pixels
                # off the row it belonged to on every edge.
                padding (0, 0)
                background Solid("#0d1a26cc" if _sfocus else "#070f1899")
                hover_background Solid("#14314acc")
                hover_sound MSBF_UI_SFX["hover"]
                activate_sound MSBF_UI_SFX["accept"]
                action [SetScreenVariable("focus", _si + 1), SetScreenVariable("kb_active", False), SetScreenVariable("rows", msbf_toggle_row(picks, rows, _sid))]

                fixed:
                    xysize (634, 40)
                    add Solid("#ffcf66" if _srow == "front" else "#4d6f85") xysize (3, 40)
                    if _sfocus:
                        add Solid("#9becff") xysize (634, 2)
                        add Solid("#9becff") xysize (634, 2):
                            ypos 38
                    text "[_si]" style "msbf_cyl_pip":
                        xpos 14
                        yalign 0.5
                    if _smug is not None:
                        add ArchivePortraitCrop(_smug[0], 32, 32, _smug[3], _smug[2], _smug[1], _smug[4]):
                            at phone_round(16)
                            xpos 34
                            ypos 4
                    text _sentry["name"] style "msbf_cyl_slot_name":
                        xpos 76
                        ypos 4
                        xmaximum 150
                    text _sentry["role"] style "msbf_cyl_slot_role":
                        xpos 76
                        ypos 22
                        xmaximum 150
                    text ("FRONT" if _srow == "front" else "REAR") style ("msbf_cyl_row_front" if _srow == "front" else "msbf_cyl_row_rear"):
                        xpos 250
                        yalign 0.5
                    text "Z flips row    X ejects" style "msbf_cyl_slot_hint":
                        xanchor 1.0
                        xpos 620
                        yalign 0.5
        else:
            fixed:
                xpos 622
                ypos _sy
                xysize (634, 40)
                add Solid("#04080c88") xysize (634, 40)
                add Solid("#1a2630") xysize (3, 40)
                text "[_si]" style "msbf_cyl_pip_empty":
                    xpos 14
                    yalign 0.5
                text "NONE SELECTED" style "msbf_cyl_slot_empty":
                    xpos 76
                    yalign 0.5

    # =========================================================================
    # BEGIN
    # =========================================================================
    # READY LIVES AT THE FOOT OF THE FIRING ORDER, not under the cylinder.
    # UP/DOWN walks one vertical list -- cylinder, then each round, then this --
    # so the last stop has to be the one physically at the bottom of that list.
    # Parked under the cylinder it was the only stop in the whole ring that sat
    # in the other column, and pressing DOWN off the last round jumped the eye
    # across the screen.
    if _focus == 5:
        add Solid(_accent) xysize (320, 2):
            xcenter 939
            ypos 634
        add Solid(_accent) xysize (320, 2):
            xcenter 939
            ypos 696

    textbutton ("READY" if _ready else "SELECT FOUR"):
        style "msbf_cyl_begin"
        keyboard_focus False
        xcenter 939
        ypos 640
        sensitive _ready
        hover_sound MSBF_UI_SFX["hover"]
        activate_sound MSBF_UI_SFX["accept"]
        action [SetScreenVariable("focus", 5), SetScreenVariable("kb_active", False)] + ([_act_begin] if _ready else [NullAction()])

    text "Arrows index  |  Z select / flip row  |  X eject  |  Up/Down move" style "msbf_cyl_keys":
        xcenter MSBF_CYL_CX
        ypos 640


# -----------------------------------------------------------------------------
# 5. STYLES
# -----------------------------------------------------------------------------
style msbf_cyl_count:
    size 30
    color "#ffcf66"
    bold True
    outlines [(2, "#02040bdd", 0, 0)]

style msbf_cyl_name:
    size 36
    color "#f5fbff"
    bold True
    kerning 1.2
    outlines [(2, "#02040bcc", 0, 0)]

style msbf_cyl_role:
    size 16
    color "#ffcf66"
    bold True
    kerning 2.0
    outlines [(2, "#02040bcc", 0, 0)]

style msbf_cyl_summary:
    size 14
    color "#c7dbe6"
    line_spacing 3
    outlines [(1, "#02040bcc", 0, 0)]

style msbf_cyl_state_in:
    size 14
    color "#ffcf66"
    bold True
    kerning 1.4
    outlines [(2, "#02040bdd", 0, 0)]

style msbf_cyl_state_lock:
    size 14
    color "#7a5a5a"
    bold True
    kerning 1.4
    outlines [(2, "#02040bdd", 0, 0)]

style msbf_cyl_state_free:
    size 14
    color "#66e08a"
    bold True
    kerning 1.4
    outlines [(2, "#02040bdd", 0, 0)]

style msbf_cyl_action is button:
    xsize 250
    ysize 40
    background Solid("#13243499")
    hover_background Solid("#1f4f6ee6")
    insensitive_background Solid("#0a0f1466")
    padding (12, 8)

style msbf_cyl_action_text:
    size 15
    color "#f5fbff"
    insensitive_color "#55606c"
    bold True
    kerning 1.6
    xalign 0.5

style msbf_cyl_pip:
    size 13
    color "#ffcf66"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_cyl_pip_empty:
    size 13
    color "#3a4654"
    bold True

style msbf_cyl_front:
    size 13
    color "#9fb4c4"
    bold True
    kerning 1.2
    outlines [(2, "#02040bdd", 0, 0)]

style msbf_cyl_slot_name:
    size 15
    color "#f5fbff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_cyl_slot_role:
    size 11
    color "#8fa6b4"
    outlines [(1, "#02040b", 0, 0)]

style msbf_cyl_slot_empty:
    size 13
    color "#3f4c58"
    bold True
    kerning 1.4

style msbf_cyl_slot_hint:
    size 10
    color "#5f7688"
    outlines [(1, "#02040b", 0, 0)]

style msbf_cyl_row_front:
    size 12
    color "#ffcf66"
    bold True
    kerning 1.2
    outlines [(1, "#02040b", 0, 0)]

style msbf_cyl_row_rear:
    size 12
    color "#7f9bb0"
    bold True
    kerning 1.2
    outlines [(1, "#02040b", 0, 0)]

style msbf_cyl_hint:
    size 13
    color "#7f9bb0"
    bold True
    kerning 3.0
    outlines [(2, "#02040bdd", 0, 0)]

style msbf_cyl_begin is button:
    xsize 300
    ysize 52
    background Solid("#13243499")
    hover_background Solid("#22617fe6")
    insensitive_background Solid("#0a0f1466")
    padding (12, 10)

style msbf_cyl_begin_text:
    size 22
    color "#f5fbff"
    insensitive_color "#4a5560"
    bold True
    kerning 3.0
    xalign 0.5

style msbf_cyl_keys:
    size 11
    color "#5f7688"
    outlines [(2, "#02040bdd", 0, 0)]
