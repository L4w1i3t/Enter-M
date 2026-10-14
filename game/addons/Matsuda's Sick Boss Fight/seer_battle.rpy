# =============================================================================
# seer_battle.rpy  --  ONTOLOGICAL SEER :: THE BATTLE SCREEN + HUD
# =============================================================================
#
# msbf_battle_screen(battle) is THE fight, Normal and Id Mode alike. The rules
# live in battle_logic.rpy; the world (Matsuda and the party as pixel sprites)
# is MSBFPixelStage in pixel_stage.rpy; this file is the frame around them.
#
# THE BRIEF: Final Fantasy x Shin Megami Tensei x Etrian Odyssey.
#   FF  -- side-view party in formation, a party status list bottom-right, a
#          command window bottom-left with the pointing-glove cursor, the
#          action's name announced in a banner as it happens.
#   SMT -- press turns as large emblems top-right, slanted plates, the boss
#          named in big type with her form, affinities read off a Scan.
#   EO  -- the acting member's official portrait in the command window, the
#          front row physically standing a step nearer to her.
#
# DECLUTTER RULES (carried over from the Aug facelift, and pushed further)
#   * Nothing permanent sits over the middle of the frame. She lives there.
#   * The command window exists only on your turn -- its absence is the
#     information that it is not.
#   * The log is a ticker under the banner, not a panel. The full record and
#     the control reference are behind two small chips.
# =============================================================================

init -10 python:

    def _msbf_register_plate_shader():
        # ---- THE SLANTED PLATE -------------------------------------------
        # Every HUD plate is one of these: a parallelogram (u_pl_slant px of
        # horizontal lean, + = top edge shifted right), a vertical gradient,
        # a one-pixel lit edge, an accent rail parallel to the left side, and
        # an optional fade toward the right end so a plate can dissolve into
        # the room instead of stopping on a hard seam.
        renpy.register_shader("msbf.plate", variables="""
            uniform vec2 u_model_size;
            uniform float u_pl_slant;
            uniform vec4 u_pl_top;
            uniform vec4 u_pl_bottom;
            uniform vec4 u_pl_edge;
            uniform vec4 u_pl_accent;
            uniform float u_pl_fade;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 sz = u_model_size;
            vec2 p = v_tex_coord * sz;
            float yt = p.y / max(1.0, sz.y);
            float sl = u_pl_slant;
            float xl = max(sl, 0.0) * (1.0 - yt) + max(-sl, 0.0) * yt;
            float xr = sz.x - (max(-sl, 0.0) * (1.0 - yt) + max(sl, 0.0) * yt);
            float inside = smoothstep(xl - 0.5, xl + 0.5, p.x) * (1.0 - smoothstep(xr - 0.5, xr + 0.5, p.x));
            vec4 col = mix(u_pl_top, u_pl_bottom, yt);
            float dl = p.x - xl;
            float dr = xr - p.x;
            float de = min(min(dl, dr), min(p.y, sz.y - p.y));
            float edge = 1.0 - smoothstep(0.6, 1.4, de);
            col = mix(col, u_pl_edge, edge * u_pl_edge.a);
            float rail = (1.0 - smoothstep(2.0, 3.0, dl)) * step(1.5, dl);
            col = mix(col, u_pl_accent, rail * u_pl_accent.a);
            float fade = 1.0;
            if (u_pl_fade > 0.0) {
                fade = 1.0 - smoothstep(1.0 - u_pl_fade, 1.0, p.x / sz.x);
            }
            float a = col.a * inside * fade;
            gl_FragColor = vec4(col.rgb * a, a);
        """)

    try:
        _msbf_register_plate_shader()
        MSBF_PLATE_SHADER = True
    except Exception as _msbf_plate_e:
        MSBF_PLATE_SHADER = False
        if config.developer:
            renpy.log("MSBF PLATE: shader registration failed: %r" % (_msbf_plate_e,))


init -2 python:

    MSBF_HUD_FONT_NAME = "assets/fonts/Myanmar.otf"
    MSBF_HUD_FONT_TECH = "assets/fonts/NovaSquare-Regular.ttf"
    MSBF_HUD_FONT_BODY = "assets/gui/font/Aller_Rg.ttf"
    MSBF_HUD_UI = "addons/Matsuda's Sick Boss Fight/pixel/ui/"

    # Form names for the kicker over her name. Her NAME is the battle's own
    # (boss.name), which already changes per phase.
    MSBF_HUD_FORM = {1: "PHASE I  ·  NAHOBINO", 2: "PHASE II  ·  TOHU IMAGO", 3: "PHASE III  ·  IMAGO RUPTA"}

    def _pl_rgba(c, a=None):
        if isinstance(c, str):
            r, g, b = msbf_hex_rgb(c)
            return (r, g, b, 1.0 if a is None else a)
        if len(c) == 3:
            return (c[0], c[1], c[2], 1.0 if a is None else a)
        return tuple(c)

    def _msbf_plate_build(w, h, slant, top, bottom, edge, accent, fade):
        if not MSBF_PLATE_SHADER:
            return Solid("#050a14dd", xysize=(w, h))
        return Transform(Solid("#00000000"), xysize=(w, h), mesh=True, shader="msbf.plate",
            u_pl_slant=slant, u_pl_top=top, u_pl_bottom=bottom,
            u_pl_edge=edge, u_pl_accent=accent, u_pl_fade=fade)

    def msbf_plate(w, h, slant=12, top=(0.03, 0.05, 0.10, 0.86), bottom=(0.01, 0.02, 0.05, 0.92),
            edge=(0.55, 0.70, 0.85, 0.35), accent=(0.33, 0.87, 1.0, 0.0), fade=0.0):
        """One slanted HUD plate. Colours are (r, g, b, a) or '#rrggbb'.
        One object per look (msbf_memo), so a screen that re-executes reuses
        the node instead of rebuilding it."""
        return msbf_memo(_msbf_plate_build, int(w), int(h), float(slant), _pl_rgba(top), _pl_rgba(bottom),
            _pl_rgba(edge), _pl_rgba(accent), float(fade))

    # --- REUSE: one object per argument tuple ---------------------------------
    # Screen language REUSES a node only when its arguments compare equal to
    # the previous execution's -- and a Transform (ATL included) is equal only
    # to itself. So `at some_atl(args)` builds a new transform on EVERY
    # execution, and every build copies every transform property (~490 in this
    # project: each uniform any file registers becomes one) and deep-compares
    # its ATL context. A helper that returns a new displayable per call
    # defeats reuse of the node the same way. Measured Oct 2 2026 on the
    # FORMATION screen: ~370 transforms rebuilt per keypress, ~37 ms of
    # execution plus a ~26 ms re-render -- the "stutter when navigating".
    #
    # msbf_t / msbf_memo hand back the SAME object for the same arguments, so
    # a re-execution rebuilds only what actually changed, and a transform
    # whose arguments did change still restarts exactly as before.
    # Arguments must be hashable (tuples, not lists).
    MSBF_MEMO = {}

    def msbf_t(t, *args):
        """`at msbf_t(some_atl, a, b)` behaves as `at some_atl(a, b)`, reusably.
        Unhashable arguments (a list, a dict) fall back to a plain call."""
        key = (0, id(t), args)
        try:
            rv = MSBF_MEMO.get(key)
        except TypeError:
            return t(*args)
        if rv is None:
            if len(MSBF_MEMO) > 6000:
                MSBF_MEMO.clear()
            rv = MSBF_MEMO[key] = t(*args)
        return rv

    def msbf_memo(factory, *args):
        """factory(*args), built once per argument tuple (unhashable
        arguments fall back to a plain call)."""
        key = (1, id(factory), args)
        try:
            rv = MSBF_MEMO.get(key)
        except TypeError:
            return factory(*args)
        if rv is None:
            if len(MSBF_MEMO) > 6000:
                MSBF_MEMO.clear()
            rv = MSBF_MEMO[key] = factory(*args)
        return rv

    def _msbf_blank(w, h):
        return Solid("#00000000", xysize=(int(w), int(h)))

    def msbf_blank(w, h):
        """A transparent w x h base for a mesh-shader transform, reusable."""
        return msbf_memo(_msbf_blank, int(w), int(h))

    # --- THE PARTY STATUS LIST (bottom left, under the party) ----------------
    # FF's party window. Row height is a function of party size: four rows are
    # roomy, seven (phase 3 summons everyone) go compact.
    MSBF_STATUS_X = 52
    MSBF_STATUS_W = 520
    MSBF_STATUS_ACTIVE_SHIFT = 14     # the acting row steps toward her

    def msbf_status_rowh(n):
        return 31 if n <= 4 else (24 if n <= 5 else 19)

    def msbf_status_row_origin(i, n):
        rh = msbf_status_rowh(n)
        top = 712 - n * rh
        return (MSBF_STATUS_X + i * 3, top + i * rh)

    def msbf_status_bar_rect(i, n):
        """The HP bar of row i -- the bar-trail chips land exactly on it."""
        x, y = msbf_status_row_origin(i, n)
        rh = msbf_status_rowh(n)
        bh = 6 if n <= 4 else 4
        return (x + 262, y + rh // 2 - bh // 2 + (2 if n <= 4 else 1), 136, bh)

    MSBF_BOSS_BAR = (758, 98, 488, 10)


# -----------------------------------------------------------------------------
# TRANSFORMS
# -----------------------------------------------------------------------------
transform msbf_hud_in(delay=0.0, dx=0, dy=8):
    alpha 0.0
    xoffset dx
    yoffset dy
    pause delay
    easeout 0.22 alpha 1.0 xoffset 0 yoffset 0

transform msbf_banner_pop(token=0):
    # The token is READ (it picks the slide direction), so a new action
    # restarts the banner even when it repeats the previous one's name.
    alpha 0.0
    xoffset (-26 if token % 2 else 26)
    easeout 0.14 alpha 1.0 xoffset 0
    pause 1.15
    easein 0.25 alpha 0.0

transform msbf_ticker_pop(token=0):
    alpha 0.0
    yoffset (4 if token % 2 else 5)
    easeout 0.18 alpha 1.0 yoffset 0
    pause 3.2
    linear 0.6 alpha 0.55

transform msbf_cursor_bob:
    yoffset 0
    block:
        easein 0.26 yoffset -6
        easeout 0.26 yoffset 0
        repeat

transform msbf_hand_bob:
    xoffset 0
    block:
        easein 0.22 xoffset -4
        easeout 0.22 xoffset 0
        repeat

transform msbf_hud_pulse:
    alpha 0.75
    block:
        ease 0.7 alpha 1.0
        ease 0.7 alpha 0.75
        repeat

transform msbf_turns_scale:
    zoom 1.2


# -----------------------------------------------------------------------------
# THE PIECES
# -----------------------------------------------------------------------------

# Top-right, over her: who she is right now, and how much of this bar is left.
screen msbf_hud_boss(battle):
    $ _ph = min(3, max(1, int(battle.phase)))
    $ _acc = msbf_phase_accent(_ph)[0]
    $ _danger = battle.boss.hp_ratio < 0.25
    $ _bx, _by, _bw, _bh = MSBF_BOSS_BAR
    use msbf_hud_scrim(560, 0, 720, 190, 1.0, 1.4, -1.0, 0.82)

    text MSBF_HUD_FORM.get(_ph, "") style "msbf_hud_kicker" color _acc:
        xpos _bx + _bw
        xanchor 1.0
        ypos 18
    text battle.boss.name.upper() style "msbf_hud_bossname":
        xpos _bx + _bw + 2
        xanchor 1.0
        ypos 36
        xmaximum 640

    add msbf_plate(_bw + 18, _bh + 10, -9, (0.02, 0.03, 0.06, 0.92), (0.01, 0.01, 0.03, 0.95), _pl_rgba(_acc, 0.55)):
        xpos _bx - 9
        ypos _by - 5
    fixed:
        xpos _bx
        ypos _by
        xysize (_bw, _bh)
        use msbf_energy_bar(battle.boss.hp, battle.boss.max_hp, _bw, _bh, "#ff3868", "#141722", danger=_danger)
    text "[battle.boss.hp] / [battle.boss.max_hp]" style "msbf_hud_bosshp":
        xpos _bx + _bw
        xanchor 1.0
        ypos _by + 16

    if battle.analyzed:
        hbox:
            xpos _bx
            ypos _by + 20
            spacing 7
            text "WEAK" style "msbf_hud_small" color "#ffcf66"
            for _el in battle.boss.weaknesses:
                text _el.upper() style "msbf_hud_el" color msbf_element_color(_el)
            null width 10
            text "RESIST" style "msbf_hud_small" color "#8fa3b8"
            for _el in battle.boss.resists:
                text _el.upper() style "msbf_hud_el" color msbf_element_color(_el)
    else:
        text "AFFINITIES UNREAD  \u00b7  SCAN TO REVEAL" style "msbf_hud_small":
            xpos _bx
            ypos _by + 21
            color "#7f8da3"


# Top-left, over the party: the press turns, SMT-sized. They are the party's
# tempo -- and hers, in red, while she holds it.
screen msbf_hud_turns(battle):
    $ _enemy = battle.enemy_display_active
    $ _col = "#ff5a7a" if _enemy else msbf_phase_accent(battle.phase)[0]
    $ _pt_n = len(battle.active_press_turn_icons)
    $ _pt_w = MSBF_PRESS_TURN_ROW_X + max(1, _pt_n) * (MSBF_PRESS_TURN_SLOT_WIDTH + MSBF_PRESS_TURN_SLOT_SPACING)
    use msbf_hud_scrim(0, 0, 520, 150, 1.0, 1.5, 1.0, 0.80)

    text ("%s'S TURN" % battle.boss.name.split(",")[0].upper() if _enemy else "PRESS TURN") style "msbf_hud_kicker" color _col:
        xpos 30
        ypos 18
    text ("ROUND %02d   \u00b7   %d / %d" % (battle.round_number, battle.active_actions_this_phase, battle.active_action_cap)) style "msbf_hud_small":
        xpos 30
        ypos 88
        color "#9aa8bd"

    fixed:
        xpos 22
        ypos 36
        xysize (int(_pt_w * 1.2), 44)
        fixed:
            xysize (_pt_w, 34)
            at msbf_turns_scale
            if battle.active_press_turn_icons:
                hbox:
                    xpos MSBF_PRESS_TURN_ROW_X
                    spacing MSBF_PRESS_TURN_SLOT_SPACING
                    for _idx, icon in enumerate(battle.active_press_turn_icons):
                        use msbf_press_turn_icon(icon, _idx)
            $ _turn_fx_side = "enemy" if battle.enemy_phase_active else "player"
            $ _turn_fx_events = getattr(battle, "press_turn_fx_events", [])
            if _turn_fx_events:
                for _turn_fx in _turn_fx_events:
                    if _turn_fx.get("side") == _turn_fx_side:
                        use msbf_press_turn_fx_icon(_turn_fx)


# Top-centre: the action as it happens (FF's battle message), with the latest
# log line ticking underneath it.
screen msbf_hud_banner(battle, token):
    $ _bn = getattr(battle, "action_banner", None)
    if _bn and _bn[0] == token:
        $ _enemy = _bn[4] == "enemy"
        $ _ecol = "#ff5a7a" if _enemy else msbf_element_color(_bn[3])
        fixed:
            xysize (440, 58)
            xcenter 520
            ypos 14
            at msbf_t(msbf_banner_pop, token)
            add msbf_plate(440, 50, 14, (0.03, 0.04, 0.08, 0.90), (0.01, 0.01, 0.03, 0.94), _pl_rgba(_ecol, 0.75), _pl_rgba(_ecol, 1.0))
            text _bn[1].upper() style "msbf_hud_kicker" color _ecol:
                xalign 0.5
                ypos 5
            text _bn[2].upper() style "msbf_hud_action":
                xalign 0.5
                ypos 17


screen msbf_hud_ticker(battle):
    if battle.log:
        text battle.log[-1] style "msbf_hud_ticker" at msbf_t(msbf_ticker_pop, battle.log_serial):
            xcenter 520
            ypos 70
            xmaximum 420
            textalign 0.5


# Bottom-right: the party, FF's status window.
screen msbf_hud_party(battle, actor_id=None, pending=None, kb_member=None, committing=None, actor_idx=None):
    $ _n = len(battle.party)
    $ _rh = msbf_status_rowh(_n)
    $ _tight = _n > 4
    for _i, _m in enumerate(battle.party):
        $ _rx, _ry = msbf_status_row_origin(_i, _n)
        $ _act = actor_id is not None and _m.id == actor_id
        $ _tgt = pending is not None and battle.can_target(pending, _m)
        $ _kbf = kb_member is not None and _m is kb_member
        $ _edge = (0.45, 1.0, 0.6, 0.85) if (_tgt and _kbf) else ((0.40, 0.88, 0.55, 0.55) if _tgt else (_pl_rgba(msbf_phase_accent(battle.phase)[0], 0.85) if _act else (0.45, 0.55, 0.70, 0.22)))
        $ _top = (0.06, 0.10, 0.17, 0.92) if (_act or _kbf) else (0.02, 0.04, 0.08, 0.80)
        $ _rail = _pl_rgba("#ffcf66" if _m.row == "front" else "#5d7a92", 0.9)
        $ _shift = MSBF_STATUS_ACTIVE_SHIFT if (_act or _kbf) else 0
        if pending is not None:
            button:
                style "msbf_status_button"
                xpos _rx + _shift
                ypos _ry
                xysize (MSBF_STATUS_W, _rh - 2)
                sensitive _tgt and committing is None
                hover_sound MSBF_UI_SFX["hover"]
                activate_sound MSBF_UI_SFX["accept"]
                action [Function(msbf_px_cue_commit, actor_idx, pending.id, _i), SetScreenVariable("hovered_skill", None), SetScreenVariable("pending_skill", None), SetScreenVariable("committing", {"skill": pending, "target": _m, "actor_index": actor_idx, "element": pending.element, "ally": True})]
                use msbf_hud_party_row(_m, _n, _rh, _tight, _top, _edge, _rail, _act, _tgt, _kbf)
        else:
            fixed:
                xpos _rx + _shift
                ypos _ry
                xysize (MSBF_STATUS_W, _rh - 2)
                use msbf_hud_party_row(_m, _n, _rh, _tight, _top, _edge, _rail, _act, False, _kbf)


screen msbf_hud_party_row(m, n, rh, tight, top, edge, rail, act, tgt, kbf):
    add msbf_plate(MSBF_STATUS_W, rh - 2, 8, top, (0.01, 0.02, 0.04, 0.88), edge, rail)
    if kbf:
        add (MSBF_HUD_UI + "cursor_hand.png") at msbf_hand_bob:
            zoom 2
            nearest True
            xpos -34
            yalign 0.5
    text m.name style ("msbf_hud_pname_tight" if tight else "msbf_hud_pname"):
        xpos 18
        yalign 0.5
        color ("#ffffff" if m.alive else "#ff6b80")
    if not m.alive:
        text "DOWN" style "msbf_hud_tag" color "#ff5a7a":
            xpos 142
            yalign 0.5
    elif m.guard:
        text "GUARD" style "msbf_hud_tag" color "#8fd6ff":
            xpos 142
            yalign 0.5
    elif m.focus:
        text "FOCUS" style "msbf_hud_tag" color "#ffcf66":
            xpos 142
            yalign 0.5
    elif tgt:
        text "TARGET" style "msbf_hud_tag" color "#7dffa0" at msbf_hud_pulse:
            xpos 142
            yalign 0.5
    $ _hpcol = "#ff5a7a" if m.hp_ratio < 0.25 else ("#ffd970" if m.hp_ratio < 0.5 else "#ffffff")
    text "[m.hp]" style ("msbf_hud_num_tight" if tight else "msbf_hud_num"):
        xpos 254
        xanchor 1.0
        yalign 0.5
        color _hpcol
    fixed:
        xpos 262
        yalign 0.5
        yoffset (2 if not tight else 1)
        xysize (136, (6 if not tight else 4))
        use msbf_energy_bar(m.hp, m.max_hp, 136, (6 if not tight else 4), "#66e08a", "#121a24")
    text "[m.mp]" style ("msbf_hud_mp_tight" if tight else "msbf_hud_mp"):
        xpos 444
        xanchor 1.0
        yalign 0.5
    fixed:
        xpos 450
        yalign 0.5
        yoffset (2 if not tight else 1)
        xysize (52, (4 if not tight else 3))
        use msbf_energy_bar(m.mp, m.max_mp, 52, (4 if not tight else 3), "#7fa8ff", "#121a24", danger=False)


# The acting member's mug: their OFFICIAL portrait, the same art the party
# select shows -- the one place the illustrated design is in the fight.
screen msbf_hud_mug(member_id, size=52):
    $ _mg = msbf_roster_mug(member_id)
    fixed:
        xysize (size, size)
        add Solid("#0b1220") xysize (size, size) at msbf_t(phone_round, size // 2)
        if _mg is not None:
            add msbf_memo(ArchivePortraitCrop, _mg[0], size, size, _mg[3], _mg[2], _mg[1], _mg[4]):
                at msbf_t(phone_round, size // 2)


# -----------------------------------------------------------------------------
# THE BATTLE SCREEN
# -----------------------------------------------------------------------------
screen msbf_battle_screen(battle):
    modal True
    use enter_m_input_lock()

    default hovered_skill = None
    default pending_skill = None
    default log_yadj = ui.adjustment()
    default float_seen_serial = -1
    default committing = None
    default death_seen_serial = -1
    default bar_seen_serial = -1
    default kb_index = 0
    # WHO OWNS THE HIGHLIGHT -- whichever device moved last (see the note on
    # msbf_kb_step). The mouse pointer does not move when you use the keyboard.
    default kb_active = False
    default show_controls = False
    default show_log = False
    default cam_token = None
    default cam_seen = None
    default cam_strength = 1.0
    default ambient_wave = False
    default ambient_delay = renpy.random.uniform(3.4, 6.6)
    default banner_seen = 0
    default banner_live = 0

    $ _actor = battle.current_actor
    $ _actor_idx = battle.party.index(_actor) if (_actor is not None and _actor in battle.party) else None
    $ _boss_x, _boss_y = msbf_boss_anchor(battle.phase)
    $ _accent, _accent2 = msbf_phase_accent(battle.phase)
    $ _party_n = len(battle.party)

    python:
        # One impact weight drives the camera, the deck wave and the reaction
        # on whoever was hit -- see MSBF_IMPACT_WEIGHT in arena.rpy.
        _impact_w = msbf_impact_weight(battle.fx_event)
        _impact_token = battle.fx_serial if _impact_w > 0.0 else None
        _hit_set = set()
        if battle.float_events:
            for _fe_h in battle.float_events:
                _fa_h = _fe_h.get("anchor", "boss")
                if isinstance(_fa_h, int) and _fe_h.get("kind") in ("enemy", "dmg", "crit", "weak"):
                    _hit_set.add(_fa_h)
        _hit_w = max(0.45, _impact_w) if _hit_set else 0.0

    $ _cinematic = battle.phase_transition_active or battle.final_victory_active or battle.defeat_sequence_active or bool(battle.result)
    $ _hud_on = not (_cinematic or battle.microgame_active)
    # Nothing draws under an opaque cover (defeat blackout, victory whiteout,
    # the beat of a transition before its reveal takes over).
    $ _world_on = not (getattr(battle, "defeat_blackout", False) or getattr(battle, "final_victory_whiteout", False) or (battle.phase_transition_active and not battle.fx_event and not getattr(battle, "phase2_reveal_started", False)))
    $ _deck_on = _hud_on and _actor is not None and battle.turn_phase == "player"

    # --- The fight's clock -----------------------------------------------------
    if battle.result:
        timer 0.5 action Return(battle.result)
    elif battle.final_victory_active:
        timer battle.fx_clear_delay action Function(battle.finish_final_victory)
    elif battle.defeat_sequence_active:
        timer battle.fx_clear_delay action Function(battle.finish_defeat)
    elif battle.phase_transition_active and battle.fx_event == "phase_blackout":
        timer battle.fx_clear_delay action Function(battle.begin_phase_two_reveal)
    elif battle.phase_transition_active and battle.fx_event == "phase":
        timer battle.fx_clear_delay action Function(battle.finish_phase_transition)
    elif battle.phase_transition_active and not battle.fx_event:
        timer battle.phase_transition_delay action Function(battle.finish_phase_transition)
    elif battle.handover_active and not battle.fx_event:
        timer battle.handover_delay action Function(battle.finish_handover)
    elif battle.enemy_phase_active and not battle.fx_event:
        # Her wind-up is drawn by the stage during this beat, so it is held
        # long enough to read as a coil before each strike.
        timer max(battle.enemy_step_delay, 0.52) action Function(battle.advance_enemy_phase)

    # --- One-shot impact token (two variables, see Aug facelift fact 6) -------
    if _impact_token is not None and _impact_token != cam_seen:
        timer 0.01 action [SetScreenVariable("cam_seen", _impact_token), SetScreenVariable("cam_token", _impact_token), SetScreenVariable("cam_strength", _impact_w)]
    if cam_token is not None:
        timer 0.70 action SetScreenVariable("cam_token", None)

    # The action banner: same two-variable shape.
    $ _bn = getattr(battle, "action_banner", None)
    if _bn and _bn[0] != banner_seen:
        timer 0.01 action [SetScreenVariable("banner_seen", _bn[0]), SetScreenVariable("banner_live", _bn[0])]
    if banner_live:
        timer 1.55 action SetScreenVariable("banner_live", 0)

    if battle.phase >= 2 and _hud_on and committing is None:
        timer ambient_delay repeat True action [SetScreenVariable("ambient_wave", True), SetScreenVariable("ambient_delay", renpy.random.uniform(1.8, 3.4) if battle.phase == 3 else renpy.random.uniform(3.8, 7.0))]
    if ambient_wave:
        timer 0.70 action SetScreenVariable("ambient_wave", False)

    if battle.float_events and float_seen_serial != battle.float_serial:
        timer 1.15 action [Function(battle.clear_float_events), SetScreenVariable("float_seen_serial", battle.float_serial)]

    if not battle.microgame_active:
        key "game_menu" action Show("msbf_pause_menu")
        key "K_ESCAPE" action Show("msbf_pause_menu")

    # --- Keyboard: Z/Enter confirm, X/LShift back, arrows + WASD move ----------
    python:
        _kb_on = (_actor is not None and battle.turn_phase == "player" and committing is None and not battle.result)
        _kb_targeting = pending_skill is not None
        if _kb_targeting:
            _kb_items = [m for m in battle.party if battle.can_target(pending_skill, m)]
        elif _actor is not None:
            _kb_items = list(_actor.skills)
        else:
            _kb_items = []
        _kb_count = len(_kb_items)
        _kb_cur = min(kb_index, _kb_count - 1) if _kb_count else 0
        _kb_focus_member = _kb_items[_kb_cur] if (_kb_targeting and _kb_count) else None

        # The skill window is two columns of four, laid out row-major: LEFT/
        # RIGHT step one, UP/DOWN step a row (two). Targets are a list.
        _kb_left = Function(msbf_kb_step, "kb_index", -1, _kb_count) if _kb_count else NullAction()
        _kb_right = Function(msbf_kb_step, "kb_index", 1, _kb_count) if _kb_count else NullAction()
        if _kb_targeting:
            _kb_up = _kb_left
            _kb_down = _kb_right
        else:
            _kb_up = Function(msbf_kb_step, "kb_index", -2, _kb_count) if _kb_count else NullAction()
            _kb_down = Function(msbf_kb_step, "kb_index", 2, _kb_count) if _kb_count else NullAction()

        _kb_confirm = None
        _kb_back = None
        if _kb_on and _kb_count:
            _focus = _kb_items[_kb_cur]
            if _kb_targeting:
                _ti = battle.party.index(_focus) if _focus in battle.party else None
                _kb_confirm = [Function(msbf_px_cue_commit, _actor_idx, pending_skill.id, _ti), SetScreenVariable("hovered_skill", None), SetScreenVariable("pending_skill", None), SetScreenVariable("committing", {"skill": pending_skill, "target": _focus, "actor_index": _actor_idx, "element": pending_skill.element, "ally": True})]
                _kb_back = [SetScreenVariable("pending_skill", None), SetScreenVariable("hovered_skill", None)]
            else:
                if battle.can_use(_focus) and battle.skill_needs_ally_target(_focus):
                    _kb_confirm = [SetScreenVariable("hovered_skill", _focus), SetScreenVariable("pending_skill", _focus), SetScreenVariable("kb_index", 0)]
                elif battle.can_use(_focus):
                    _kb_confirm = [Function(msbf_px_cue_commit, _actor_idx, _focus.id, None), SetScreenVariable("hovered_skill", None), SetScreenVariable("pending_skill", None), SetScreenVariable("committing", {"skill": _focus, "actor_index": _actor_idx, "element": _focus.element})]
                _kb_back = Function(battle.player_pass)

    if _kb_on:
        use msbf_nav_keys(_kb_up, _kb_down, _kb_left, _kb_right, _kb_confirm, _kb_back)

    # =========================================================================
    # LAYER 1 -- THE WORLD (one container, one camera)
    # =========================================================================
    python:
        if battle.final_victory_active:
            _cam_at = msbf_cam_victory
        elif battle.defeat_sequence_active:
            _cam_at = msbf_cam_defeat
        elif cam_token is not None:
            _cam_at = msbf_t(msbf_cam_punch, cam_strength, cam_token)
        else:
            _cam_at = msbf_cam_rest

    fixed:
        xysize (1280, 720)
        at _cam_at
        if _world_on:
            use msbf_arena(battle, (cam_token is not None) or ambient_wave, (cam_strength if cam_token is not None else 0.8))
        # A reveal's light belongs BEHIND the form it is revealing.
        if _world_on and battle.phase_transition_active and battle.fx_event == "phase":
            use msbf_phase_reveal_world(battle)
        if _world_on:
            add msbf_px_stage(battle)

    # =========================================================================
    # LAYER 2 -- THE HUD
    # =========================================================================
    if _hud_on and not battle.shmup_segment_active:
        use msbf_hud_scrim(0, 470, 1280, 250, 0.0, 1.7, 0.0, 0.88)
        use msbf_hud_boss(battle)
        use msbf_hud_turns(battle)
        if banner_live:
            use msbf_hud_banner(battle, banner_live)
        else:
            use msbf_hud_ticker(battle)
        use msbf_hud_party(battle, (_actor.id if _actor is not None else None), pending_skill, _kb_focus_member, committing, _actor_idx)

        # The cursor over a sprite: the acting member on your turn, the
        # focused target while choosing an ally.
        if _deck_on:
            if pending_skill is not None and _kb_focus_member is not None:
                $ _ci = battle.party.index(_kb_focus_member)
                $ _cmx, _cmy = msbf_px_member_point(_kb_focus_member.id, _ci, _party_n, _kb_focus_member.row, "head", _kb_focus_member is _actor)
                add (MSBF_HUD_UI + "cursor_down.png") at msbf_cursor_bob:
                    zoom 3
                    nearest True
                    xcenter _cmx
                    ypos _cmy - 52
                    matrixcolor TintMatrix("#7dffa0")
            elif _actor_idx is not None and committing is None:
                $ _cmx, _cmy = msbf_px_member_point(_actor.id, _actor_idx, _party_n, _actor.row, "head", True)
                add (MSBF_HUD_UI + "cursor_down.png") at msbf_cursor_bob:
                    zoom 3
                    nearest True
                    xcenter _cmx
                    ypos _cmy - 52

            # Click a sprite to target it, too.
            if pending_skill is not None:
                for _ti, _tm in enumerate(battle.party):
                    if battle.can_target(pending_skill, _tm):
                        $ _tcx, _tcy = msbf_px_member_point(_tm.id, _ti, _party_n, _tm.row, "chest", _tm is _actor)
                        button:
                            style "msbf_status_button"
                            xcenter _tcx
                            ycenter _tcy
                            xysize (96, 190)
                            sensitive committing is None
                            hover_sound MSBF_UI_SFX["hover"]
                            activate_sound MSBF_UI_SFX["accept"]
                            hovered SetScreenVariable("kb_active", False)
                            action [Function(msbf_px_cue_commit, _actor_idx, pending_skill.id, _ti), SetScreenVariable("hovered_skill", None), SetScreenVariable("pending_skill", None), SetScreenVariable("committing", {"skill": pending_skill, "target": _tm, "actor_index": _actor_idx, "element": pending_skill.element, "ally": True})]

    use msbf_fx_layer(battle)

    if battle.shmup_segment_active:
        use msbf_shmup_overlay(battle)

    # =========================================================================
    # THE COMMAND WINDOW -- present only while you can act
    # =========================================================================
    if _deck_on:
        $ _cw_x, _cw_y, _cw_w, _cw_h = 594, 552, 668, 156
        $ _tip_hover = None if kb_active else hovered_skill
        $ _kb_tip_skill = _kb_items[_kb_cur] if (_kb_on and not _kb_targeting and _kb_count) else None
        if pending_skill and not battle.result:
            $ _tip = "Choose who receives %s." % pending_skill.name
        elif _tip_hover is not None:
            $ _tip = _tip_hover.description
        elif _kb_tip_skill is not None:
            $ _tip = _kb_tip_skill.description
        else:
            $ _tip = "Pass spends half a turn."

        # Help strip, FF style: what the highlighted command does.
        fixed:
            xpos _cw_x + 10
            ypos _cw_y - 30
            xysize (_cw_w - 20, 26)
            at msbf_t(msbf_hud_in, 0.0, 0, 6)
            add msbf_plate(_cw_w - 20, 26, 10, (0.02, 0.03, 0.06, 0.82), (0.01, 0.02, 0.04, 0.86), (0.5, 0.6, 0.75, 0.25), _pl_rgba(_accent, 0.0), 0.12)
            text _tip style "msbf_hud_help":
                xpos 18
                yalign 0.5
                xmaximum _cw_w - 60

        fixed:
            xpos _cw_x
            ypos _cw_y
            xysize (_cw_w, _cw_h)
            at msbf_t(msbf_hud_in, 0.0, 10, 0)
            add msbf_plate(_cw_w, _cw_h, 18, (0.04, 0.07, 0.13, 0.94), (0.01, 0.02, 0.05, 0.96), _pl_rgba(_accent, 0.55), _pl_rgba(_accent, 1.0))

            # Header: who is acting.
            fixed:
                xpos 26
                ypos 8
                xysize (52, 52)
                use msbf_hud_mug(_actor.id, 48)
            text _actor.name.upper() style "msbf_hud_actor":
                xpos 86
                ypos 7
            text getattr(_actor, "role", "").upper() style "msbf_hud_kicker" color _accent:
                xpos 88
                ypos 40
            text "HP" style "msbf_hud_small":
                xpos 312
                ypos 16
            text "[_actor.hp]/[_actor.max_hp]" style "msbf_hud_num":
                xpos 336
                ypos 9
            text "MP" style "msbf_hud_small":
                xpos 312
                ypos 39
            text "[_actor.mp]/[_actor.max_mp]" style "msbf_hud_mp":
                xpos 336
                ypos 34

            if pending_skill:
                textbutton "CANCEL":
                    style "msbf_hud_chip"
                    text_style "msbf_hud_chip_text"
                    xpos 536
                    ypos 14
                    sensitive committing is None
                    hover_sound MSBF_UI_SFX["hover"]
                    activate_sound MSBF_UI_SFX["denied"]
                    action [SetScreenVariable("pending_skill", None), SetScreenVariable("hovered_skill", None)]
            else:
                textbutton "PASS":
                    style "msbf_hud_chip"
                    text_style "msbf_hud_chip_text"
                    xpos 536
                    ypos 14
                    sensitive committing is None
                    hover_sound MSBF_UI_SFX["hover"]
                    action [SetScreenVariable("hovered_skill", None), Function(battle.player_pass)]
            text ("X  BACK" if pending_skill else "X  HALF TURN") style "msbf_hud_small":
                xpos 544
                ypos 44
                color "#7f8da3"

            add Solid("#9fb4c42a") xpos 24 ypos 62 xysize (_cw_w - 60, 1)

            # The commands: two columns of four, row-major.
            for _skill_idx, skill in enumerate(_actor.skills):
                $ _col = _skill_idx % 2
                $ _row = _skill_idx // 2
                $ _sx = 44 + _col * 312 - _row * 4
                $ _sy = 70 + _row * 21
                $ _enabled = battle.can_use(skill)
                $ _kb_focused = _kb_on and pending_skill is None and _skill_idx == _kb_cur and (kb_active or hovered_skill is None)
                $ _skill_pending = pending_skill is skill
                $ _lit = _skill_pending or _kb_focused or (not kb_active and hovered_skill is skill)
                button:
                    style "msbf_cmd_button"
                    xpos _sx
                    ypos _sy
                    xysize (296, 21)
                    sensitive _enabled and committing is None
                    hover_sound MSBF_UI_SFX["hover"]
                    activate_sound MSBF_UI_SFX["accept"]
                    hovered [SetScreenVariable("hovered_skill", skill), SetScreenVariable("kb_active", False), SetScreenVariable("kb_index", _skill_idx)]
                    unhovered SetScreenVariable("hovered_skill", None)
                    if battle.skill_needs_ally_target(skill):
                        action [SetScreenVariable("hovered_skill", skill), SetScreenVariable("pending_skill", skill), SetScreenVariable("kb_index", 0)]
                    else:
                        action [Function(msbf_px_cue_commit, _actor_idx, skill.id, None), SetScreenVariable("hovered_skill", None), SetScreenVariable("pending_skill", None), SetScreenVariable("committing", {"skill": skill, "actor_index": _actor_idx, "element": skill.element})]

                    if _lit:
                        add msbf_plate(296, 21, 6, _pl_rgba(_accent, 0.22), _pl_rgba(_accent, 0.08), _pl_rgba(_accent, 0.6))
                    add (MSBF_HUD_UI + "diamond.png"):
                        zoom 2
                        nearest True
                        xpos 4
                        yalign 0.5
                        matrixcolor TintMatrix(msbf_element_color(skill.element) if _enabled else "#3a4654")
                    text skill.name style ("msbf_hud_cmd" if _enabled else "msbf_hud_cmd_off"):
                        xpos 28
                        yalign 0.5
                    if skill.cost:
                        text "[skill.cost]" style ("msbf_hud_cost" if _enabled else "msbf_hud_cost_off"):
                            xpos 288
                            xanchor 1.0
                            yalign 0.5

                if _lit and pending_skill is None:
                    add (MSBF_HUD_UI + "cursor_hand.png") at msbf_hand_bob:
                        zoom 2
                        nearest True
                        xpos _sx - 34
                        ypos _sy + 1

    # --- Floating combat numbers -------------------------------------------
    if battle.float_events and not _cinematic:
        for _fe in battle.float_events:
            $ _fkind = _fe.get("kind", "dmg")
            $ _fstyle = MSBF_FLOAT_STYLE.get(_fkind, "msbf_float_dmg")
            $ _flabel = msbf_float_label(_fe.get("amount", ""), _fkind)
            $ _fserial = _fe.get("serial", 0)
            $ _fdx = ((_fserial % 5) - 2) * 16
            $ _fcrit = (_fkind == "crit")
            $ _fanchor = _fe.get("anchor", "boss")
            if isinstance(_fanchor, int):
                $ _fxp, _fyp = msbf_stage_anchor(_fanchor, _party_n)
                $ _fyp = _fyp - 46
            else:
                $ _fxp = _boss_x
                $ _fyp = _boss_y - 40
            use msbf_float_number(_flabel, _fstyle, _fxp, _fyp, _fdx, _fcrit)

    # --- Bar trails: a draining chip on whichever bar just changed -----------
    if battle.bar_events and not _cinematic and not battle.microgame_active:
        if bar_seen_serial != battle.bar_serial:
            timer 0.6 action [Function(battle.clear_bar_events), SetScreenVariable("bar_seen_serial", battle.bar_serial)]
        for _be in battle.bar_events:
            $ _ba = _be.get("anchor", "boss")
            $ _bfrm = _be.get("frm", 0.0)
            $ _bto = _be.get("to", 0.0)
            $ _bgain = _be.get("gain", False)
            $ _cbx = None
            if _ba == "boss":
                $ _cbx, _cby, _cbw, _cbh = MSBF_BOSS_BAR
            elif isinstance(_ba, int) and _ba < _party_n:
                $ _cbx, _cby, _cbw, _cbh = msbf_status_bar_rect(_ba, _party_n)
                $ _cbx += (MSBF_STATUS_ACTIVE_SHIFT if ((_actor is not None and battle.party[_ba].id == _actor.id) or (_kb_focus_member is battle.party[_ba])) else 0)
            if _cbx is not None:
                $ _clo = min(_bfrm, _bto)
                $ _chi = max(_bfrm, _bto)
                $ _chip_x = int(_cbx + _cbw * _clo)
                $ _chip_w = max(2, int(_cbw * (_chi - _clo)))
                if _bgain:
                    add Solid("#bfffd6") xysize (_chip_w, _cbh) at msbf_t(msbf_bar_flash, 0.5):
                        xpos _chip_x
                        ypos _cby
                else:
                    add Solid("#ffffff") xysize (_chip_w, _cbh) at msbf_t(msbf_bar_chip, 0.5):
                        xpos _chip_x
                        ypos _cby

    # --- The wind-up: the stage plays the choreography; this resolves it on
    #     the frame the choreography strikes. -----------------------------------
    if committing is not None and not battle.result:
        $ _cact = battle.party[committing["actor_index"]] if committing.get("actor_index") is not None and committing["actor_index"] < _party_n else None
        $ _cw = msbf_px_commit_time(_cact.id if _cact is not None else None, committing["skill"])
        timer _cw action [Function(battle.player_use_skill, committing["skill"], committing.get("target")), SetScreenVariable("committing", None)]

        $ _cstyle = msbf_px_move_style(_cact.id if _cact is not None else None, committing["skill"])
        $ _ci = committing.get("actor_index", None)
        if _ci is not None and _cstyle in ("cast", "throw"):
            $ _ccx, _ccy = msbf_stage_anchor(_ci, _party_n)
            $ _crgb = msbf_hex_rgb(msbf_element_color(committing.get("element", "slash")))
            if MSBF_FX_SHADERS:
                add Solid("#00000000") xysize (84, 84) at msbf_t(msbf_fx_glow_t, _crgb, 0.7, 1.9), msbf_t(msbf_cast_projectile, _ccx, _ccy, _boss_x, _boss_y, _cw)
                add Solid("#00000000") xysize (24, 24) at msbf_t(msbf_fx_glow_t, (1.0, 1.0, 1.0), 1.0, 2.0), msbf_t(msbf_cast_projectile, _ccx, _ccy, _boss_x, _boss_y, _cw)

    # --- The handover beat --------------------------------------------------
    if battle.handover_active and not battle.fx_event:
        use msbf_turnover_sweep(battle.handover_to or "enemy", battle.phase, battle.round_number, battle.boss.name, battle.handover_serial, getattr(battle, "handover_mp_restored", False))

    # --- KO bursts ----------------------------------------------------------
    if battle.death_events and not _cinematic:
        if death_seen_serial != battle.death_serial:
            timer 1.40 action [Function(battle.clear_death_events), SetScreenVariable("death_seen_serial", battle.death_serial)]
        for _de in battle.death_events:
            $ _da = _de.get("anchor", 0)
            if isinstance(_da, int):
                $ _dxp, _dyp = msbf_stage_anchor(_da, _party_n)
                use msbf_death_burst(_dxp, _dyp, "#ff3868", False)

    if battle.typing_segment_active:
        use msbf_typing_overlay(battle)
    elif battle.quiz_segment_active:
        use msbf_quiz_overlay(battle)

    # --- Reference, kept behind two chips under the press turns --------------
    if _hud_on:
        if show_log:
            frame:
                style "empty"
                xpos 26
                ypos 132
                xsize 520
                ysize 300
                background msbf_plate(520, 300, 14, (0.03, 0.05, 0.09, 0.94), (0.01, 0.02, 0.04, 0.96), _pl_rgba(_accent, 0.5))
                padding (26, 16)
                at msbf_t(msbf_hud_in)
                vbox:
                    spacing 8
                    text "BATTLE RECORD" style "msbf_hud_kicker" color _accent
                    viewport:
                        id "msbf_log_viewport"
                        xysize (470, 240)
                        yadjustment log_yadj
                        mousewheel True
                        draggable True
                        yinitial 1.0
                        vbox:
                            spacing 7
                            for _line in battle.log:
                                text _line style "msbf_hud_logline"
        if show_controls:
            frame:
                style "empty"
                xpos 26
                ypos 132
                background msbf_plate(470, 120, 14, (0.03, 0.05, 0.09, 0.94), (0.01, 0.02, 0.04, 0.96), _pl_rgba(_accent, 0.5))
                padding (28, 16)
                at msbf_t(msbf_hud_in)
                vbox:
                    spacing 5
                    text "CONTROLS" style "msbf_hud_kicker" color _accent
                    text "Mouse: click a command, a target, or a fighter." style "msbf_hud_help"
                    text "Z / Enter  confirm     X / L-Shift  back or pass" style "msbf_hud_help"
                    text "Arrows / WASD  move the cursor     Esc  pause" style "msbf_hud_help"
        hbox:
            xpos 30
            ypos 106
            spacing 18
            textbutton ("HIDE LOG" if show_log else "LOG"):
                id "msbf_log_toggle"
                style "msbf_seer_reference_button"
                text_style "msbf_hud_ref"
                hover_sound MSBF_UI_SFX["hover"]
                action [ToggleScreenVariable("show_log"), SetScreenVariable("show_controls", False)]
            textbutton ("HIDE CONTROLS" if show_controls else "CONTROLS"):
                id "msbf_controls_toggle"
                style "msbf_seer_reference_button"
                text_style "msbf_hud_ref"
                hover_sound MSBF_UI_SFX["hover"]
                action [ToggleScreenVariable("show_controls"), SetScreenVariable("show_log", False)]

    use msbf_phase_transition_overlay(battle)


# -----------------------------------------------------------------------------
# STYLES
# -----------------------------------------------------------------------------
style msbf_status_button is button:
    background None
    hover_background None
    insensitive_background None
    padding (0, 0)

style msbf_cmd_button is button:
    background None
    hover_background None
    insensitive_background None
    padding (0, 0)

style msbf_hud_chip is button:
    background Frame(Solid("#0e1a2bcc"), 0, 0)
    hover_background Frame(Solid("#21406acc"), 0, 0)
    padding (16, 5)

style msbf_hud_chip_text is default:
    font MSBF_HUD_FONT_TECH
    size 15
    color "#e8f1ff"
    hover_color "#ffffff"
    insensitive_color "#5b6678"
    kerning 2.0

style msbf_hud_kicker is default:
    font MSBF_HUD_FONT_TECH
    size 13
    kerning 2.4
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_hud_bossname is default:
    font MSBF_HUD_FONT_NAME
    size 38
    color "#fbf6ec"
    kerning 1.6
    outlines [(3, "#02040acc", 0, 1)]

style msbf_hud_bosshp is default:
    font MSBF_HUD_FONT_TECH
    size 19
    color "#ffffff"
    kerning 1.0
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_hud_small is default:
    font MSBF_HUD_FONT_TECH
    size 12
    color "#b9c6d8"
    kerning 1.4
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_hud_el is default:
    font MSBF_HUD_FONT_TECH
    size 12
    kerning 1.2
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_hud_action is default:
    font MSBF_HUD_FONT_NAME
    size 25
    color "#ffffff"
    kerning 2.0
    outlines [(2, "#02040ae6", 0, 1)]

style msbf_hud_ticker is default:
    font MSBF_HUD_FONT_BODY
    size 15
    color "#d6dfeb"
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_hud_pname is default:
    font MSBF_HUD_FONT_BODY
    size 18
    bold True
    color "#ffffff"
    outlines [(2, "#02040acc", 0, 0)]

style msbf_hud_pname_tight is msbf_hud_pname:
    size 14

style msbf_hud_tag is default:
    font MSBF_HUD_FONT_TECH
    size 11
    kerning 1.6
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_hud_num is default:
    font MSBF_HUD_FONT_TECH
    size 19
    color "#ffffff"
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_hud_num_tight is msbf_hud_num:
    size 14

style msbf_hud_mp is default:
    font MSBF_HUD_FONT_TECH
    size 14
    color "#a9c2ff"
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_hud_mp_tight is msbf_hud_mp:
    size 11

style msbf_hud_actor is default:
    font MSBF_HUD_FONT_NAME
    size 28
    color "#ffffff"
    kerning 1.5
    outlines [(2, "#02040ae6", 0, 1)]

style msbf_hud_cmd is default:
    font MSBF_HUD_FONT_BODY
    size 16
    color "#eef3fb"
    outlines [(1, "#02040acc", 0, 0)]

style msbf_hud_cmd_off is msbf_hud_cmd:
    color "#4f5b6c"

style msbf_hud_cost is default:
    font MSBF_HUD_FONT_TECH
    size 14
    color "#a9c2ff"
    outlines [(1, "#02040acc", 0, 0)]

style msbf_hud_cost_off is msbf_hud_cost:
    color "#3f4a5a"

style msbf_hud_help is default:
    font MSBF_HUD_FONT_BODY
    size 14
    color "#cfd9e6"
    outlines [(1, "#02040acc", 0, 0)]

style msbf_hud_logline is default:
    font MSBF_HUD_FONT_BODY
    size 14
    color "#c2d0d8"
    xmaximum 460

style msbf_hud_ref is default:
    font MSBF_HUD_FONT_TECH
    size 12
    color "#8fa3b8"
    hover_color "#ffffff"
    kerning 2.0
    outlines [(2, "#02040ae6", 0, 0)]
