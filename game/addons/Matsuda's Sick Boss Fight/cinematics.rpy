# =============================================================================
# cinematics.rpy  --  MATSUDA'S SICK BOSS FIGHT :: THE ENTRANCES AND THE BREAKS
# =============================================================================
#
# WHAT THIS FILE IS
#   The four moments where the fight stops being a fight and becomes a shot.
#   All of them used to be built out of animated Solid() rectangles -- rotated
#   bars for light, squares for flashes -- which is why they read as diagrams of
#   spectacle rather than spectacle.
#
#     msbf_battle_intro      : phase 1. She arrives on the deck. (Called by
#                              cs_matsuda_02_battle before the HUD exists.)
#     msbf_idmode_intro      : Id Mode's opening. Same boss, opposite grammar --
#                              see the note above the screen.
#     msbf_phase_break_seq   : a bar breaking. Abrupt, and then over.
#     msbf_phase_reveal_seq  : what walks out of the break.
#
# THE ONE IDEA THEY SHARE
#   Each is built from a small number of BIG gestures on a clock, not a swarm of
#   small ones. A cinematic that layers thirty faint elements reads as busy; the
#   same beat with four elements at full strength reads as authored. So each
#   screen below is a timeline you can read top-to-bottom, and every element in
#   it is doing something you would miss if it were gone.
#
# TONE, WHICH IS THE ACTUAL BRIEF
#   phase 1  -- she is a person who has decided to fight you. Weight, wind, a
#               landing. The camera respects her.
#   phase 2  -- she is not a person any more. The roof opens and she DESCENDS.
#               Nothing in it is violent; it is the calm of something that has
#               already decided how this ends.
#   Id Mode  -- there is no arrival, because there was no journey. The image
#               simply fails to be anything else. Everything that is graceful in
#               the phase-2 entrance is broken here on purpose.
# =============================================================================

# -----------------------------------------------------------------------------
# 1. THE FRACTURE SHADER
# -----------------------------------------------------------------------------
init -10 python:

    def _msbf_register_cinematic_shaders():

        # ---- RADIAL FRACTURE ----------------------------------------------
        # The screen as a pane of glass taking a hit at (u_ck_cx, u_ck_cy).
        # u_ck_progress 0 -> 1 opens it: hairlines appear, brighten, then widen
        # into black gaps as the shards pull apart. Shards are cheap -- the
        # angular sector index is quantised and each sector gets its own hashed
        # opening rate, so no two pieces travel together.
        #
        # This is what a bar break needed. A flash says "something happened";
        # a pane of glass failing says WHAT happened, and it takes one frame.
        renpy.register_shader("msbf.crack", variables="""
            uniform float u_ck_progress;
            uniform float u_ck_cx;
            uniform float u_ck_cy;
            uniform vec3 u_ck_color;
            uniform float u_ck_shards;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float ck_hash(float n) {
                return fract(sin(n * 78.233) * 43758.5453);
            }
        """, fragment_300="""
            const float CK_TAU = 6.2831853;
            float p = clamp(u_ck_progress, 0.0, 1.0);

            vec2 d = v_tex_coord - vec2(u_ck_cx, u_ck_cy);
            d.x *= 1.7778;                       // square up a 16:9 frame
            float r = length(d);
            float ang = atan(d.y, d.x);

            // Which shard this pixel belongs to, and how fast that shard goes.
            float sect = floor((ang + 3.14159) / CK_TAU * u_ck_shards);
            float rate = 0.55 + 0.85 * ck_hash(sect);
            float wob = (ck_hash(sect + 41.0) - 0.5) * 0.30;

            // DISTANCE TO THE NEAREST SEAM, 0 AT the seam and 1 at the middle
            // of a shard. Getting this the wrong way round is what turned the
            // first version into a pinwheel: the crack was drawn down the
            // CENTRE of each shard and the gap opened across the whole sector,
            // so at full progress half the frame was a black fan.
            float f = fract((ang + 3.14159) / CK_TAU * u_ck_shards);
            float seam = min(f, 1.0 - f) * 2.0;

            // The crack front races outward, so the middle fails first.
            float front = p * rate * 1.6;
            float reached = smoothstep(front, front - 0.20, r);

            // A hairline while it is only cracked, a narrow gap once it opens.
            float open = clamp((p - 0.35) / 0.65, 0.0, 1.0) * rate;
            float lw = 0.05 + 0.02 * p;
            float gw = 0.085 * open;
            float line = smoothstep(lw, 0.0, seam) * reached;
            float gap = smoothstep(gw, 0.0, seam) * reached;

            // Concentric ring fractures crossing the radial ones.
            float rr = abs(fract(r * 3.2 - front * 0.6 + wob) - 0.5) * 2.0;
            line = max(line, smoothstep(0.07, 0.0, rr) * reached * 0.8);
            gap = max(gap, smoothstep(0.055 * open, 0.0, rr) * reached);

            // It must not still be sitting on the frame when the beat is over.
            float life = 1.0 - smoothstep(0.80, 1.0, p);

            vec3 col = u_ck_color * line * 1.9;
            float a = clamp(gap * 0.94 + line, 0.0, 1.0) * life;
            // The gaps are holes onto black; the lines are light.
            col *= (1.0 - gap);
            gl_FragColor = vec4(col * a, a);
        """)

    try:
        _msbf_register_cinematic_shaders()
        MSBF_CINE_SHADERS = True
    except Exception as _msbf_cine_e:
        MSBF_CINE_SHADERS = False
        if config.developer:
            renpy.log("MSBF CINE: shader registration failed: %r" % (_msbf_cine_e,))


# -----------------------------------------------------------------------------
# 2. TRANSFORMS
# -----------------------------------------------------------------------------

transform msbf_crack_t(delay=0.0, dur=0.9, cx=0.5, cy=0.44, color=(1.0, 1.0, 1.0), shards=14.0):
    mesh True
    shader "msbf.crack"
    u_ck_cx cx
    u_ck_cy cy
    u_ck_color color
    u_ck_shards shards
    u_ck_progress 0.0
    alpha 0.0
    pause delay
    alpha 1.0
    linear dur u_ck_progress 1.0

# --- PHASE 1 ENTRANCE --------------------------------------------------------

transform msbf_intro_letterbox_in(h=96, delay=0.0):
    subpixel True
    ysize 0
    pause delay
    easeout 0.34 ysize h

# --- PHASE 2 ENTRANCE (the descent) ------------------------------------------
# Everything slow. Nothing snaps. The only fast thing in the whole beat is the
# instant the light opens, and that is a cut, not a hit.
transform msbf_desc_shaft(delay=0.0):
    subpixel True
    xalign 0.5
    ypos 0
    yanchor 0.0
    alpha 0.0
    xzoom 0.02
    pause delay
    linear 0.06 alpha 0.9 xzoom 0.10
    easeout 1.5 xzoom 1.0 alpha 0.62
    pause 1.6
    linear 1.5 alpha 0.0

transform msbf_desc_halo(delay=0.0, size=1.0):
    subpixel True
    alpha 0.0
    zoom size * 0.2
    rotate 0.0
    pause delay
    linear 0.7 alpha 0.55
    easeout 2.4 zoom size rotate 26.0
    linear 0.9 alpha 0.0

transform msbf_desc_touchdown(delay=3.1):
    alpha 0.0
    pause delay
    easeout 0.30 alpha 0.32
    easein 1.10 alpha 0.0

transform msbf_desc_ring(delay=3.1, color=(1.0, 0.85, 0.48)):
    mesh True
    shader "msbf.ring"
    u_color color
    u_thickness 0.035
    u_intensity 2.2
    u_progress 0.02
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    pause delay
    alpha 1.0
    linear 1.30 u_progress 0.98

# --- ID MODE ENTRANCE (the failure to be anything else) ----------------------

transform msbf_id_bar(y=0, h=26, delay=0.0, life=0.09):
    subpixel True
    alpha 0.0
    ypos y
    pause delay
    alpha 1.0
    xoffset 0
    pause 0.02
    xoffset 46
    pause 0.03
    xoffset -30
    pause life
    alpha 0.0

# --- THE BAR BREAK -----------------------------------------------------------
# ABRUPT. The old break spent 3.4 seconds on black with a slow charge in it,
# which is the pacing of a summoning, not of something being broken off a boss.
# This one is done in well under two: blowout, fracture, one held silence.
transform msbf_brk_blowout:
    alpha 1.0
    pause 0.05
    linear 0.06 alpha 0.0

transform msbf_brk_hold:
    # the silence after: pure black, held just long enough to be felt
    alpha 0.0
    pause 0.62
    linear 0.18 alpha 1.0


transform msbf_cine_rule(delay=0.0):
    subpixel True
    alpha 0.0
    xzoom 0.08
    pause delay
    easeout 0.55 alpha 0.85 xzoom 1.0

transform msbf_cine_seal(delay=0.0, reverse=False):
    subpixel True
    alpha 0.0
    zoom 0.92
    rotate (10 if reverse else -10)
    pause delay
    parallel:
        easeout 1.0 alpha 0.22
        pause 1.6
        easein 1.0 alpha 0.0
    parallel:
        linear 4.0 rotate (-8 if reverse else 8) zoom 1.06

transform msbf_cine_reveal_blackout:
    alpha 1.0
    pause 0.20
    easeout 1.30 alpha 0.0


# -----------------------------------------------------------------------------
# 3. SCREENS
# -----------------------------------------------------------------------------


screen msbf_cine_border(delay=0.0):
    add Solid("#030811") xysize (1280, 56) at msbf_t(msbf_intro_letterbox_in, 56, delay):
        ypos 0
    add Solid("#030811") xysize (1280, 28) at msbf_t(msbf_intro_letterbox_in, 28, delay):
        ypos 720
        yanchor 1.0
    add (MSBF_SEER_ART + "title_rule.png") at msbf_t(msbf_cine_rule, delay + 0.15):
        xcenter 640
        ycenter 55
        xysize (720, 20)

# -----------------------------------------------------------------------------
# THE ENTRANCES (rebuilt Sep 30 2026 on the pixel stage)
#
# The figures are the fight's own pixel sprites, choreographed by
# MSBFPixelStage in its "intro" / "id_intro" modes (pixel_stage.rpy) on the
# running orders MSBF_PX_INTRO / MSBF_PX_ID_INTRO. This file adds what is not
# a figure: the camera, the light, the letterbox, the eye cut-in, the name
# card and the stingers -- all keyed to those same numbers, so retiming a beat
# is one edit.
#
# NORMAL (phase 1, Nahobino) -- an ARRIVAL with weight:
#   the deck in the dark -> the party runs in and plants -> a glint high in the
#   sky -> she FALLS and slams the deck (shockwave, the party is shoved back a
#   step) -> she rises -> her eyes, cut in from her official art -> the glaive
#   sweep cuts the frame -> the name card slams down.
# ID MODE (phase 2, Tohu Imago) -- NO arrival:
#   the room and the party decode into place in torn frames -> she is simply
#   there, enormous -> her wings open tier by tier anyway -> the light comes ->
#   the card arrives already wrong.
# -----------------------------------------------------------------------------

transform msbf_ix_cam(look=60, land=2.5):
    # Starts tilted up at the sky she falls out of, comes down with her.
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 640
    ypos 360
    zoom 1.10
    yoffset look
    pause max(0.0, land - 1.15)
    easein 1.10 yoffset 0 zoom 1.06
    # the landing hits the camera
    linear 0.03 xoffset -14 yoffset 10
    linear 0.03 xoffset 12 yoffset -8
    linear 0.04 xoffset -9 yoffset 6
    linear 0.05 xoffset 6 yoffset -4
    linear 0.06 xoffset -3 yoffset 2
    easeout 0.40 xoffset 0 yoffset 0 zoom 1.03
    ease 2.6 zoom 1.0

transform msbf_ix_dim(lift=0.4, land=2.5):
    # The deck starts in darkness; the party's arrival brings it up a little,
    # the landing blows it open.
    alpha 0.88
    linear lift alpha 0.62
    pause max(0.0, land - lift - 0.02)
    alpha 0.0
    pause 0.10
    linear 0.45 alpha 0.30

transform msbf_ix_flash(at_=2.5, peak=0.95):
    alpha 0.0
    pause at_
    alpha peak
    easeout 0.42 alpha 0.0

transform msbf_ix_glint(at_=1.6, dur=0.5):
    alpha 0.0
    zoom 0.4
    pause at_
    easeout 0.12 alpha 1.0 zoom 1.0
    linear (dur - 0.12) alpha 0.0 zoom 1.6

transform msbf_ix_bars(h=78, at_=0.0):
    subpixel True
    ysize 0
    pause at_
    easeout 0.40 ysize h

transform msbf_ix_cutin(at_=2.95, dur=0.38):
    # A slit opens across the frame with her eyes in it, then shuts.
    subpixel True
    alpha 0.0
    yzoom 0.0
    pause at_
    alpha 1.0
    easeout 0.07 yzoom 1.0
    pause dur
    easein 0.06 yzoom 0.0

transform msbf_ix_cutin_slide(at_=2.95, dur=0.5):
    subpixel True
    xoffset 70
    pause at_
    linear dur xoffset -30

transform msbf_ix_split(at_=3.42):
    # The sweep cuts the frame: a white line drawn across it at speed.
    subpixel True
    alpha 0.0
    xzoom 0.0
    pause at_
    alpha 1.0
    easeout 0.10 xzoom 1.0
    pause 0.06
    easein 0.22 alpha 0.0

transform msbf_ix_card_plate(at_=3.62):
    subpixel True
    alpha 0.0
    xoffset -260
    pause at_
    easeout 0.18 alpha 1.0 xoffset 0
    pause 2.15
    easein 0.28 alpha 0.0 xoffset 160

transform msbf_ix_card_name(at_=3.62, corrupted=False):
    subpixel True
    alpha 0.0
    zoom 1.55
    pause at_ + 0.04
    alpha 1.0
    easein 0.10 zoom 1.0
    # the slam
    linear 0.03 xoffset 6
    linear 0.03 xoffset -4
    linear 0.04 xoffset 0
    pause (0.14 if corrupted else 1.90)
    xoffset (14 if corrupted else 0)
    pause (0.05 if corrupted else 0.0)
    xoffset 0
    pause (1.70 if corrupted else 0.0)
    linear 0.24 alpha 0.0

transform msbf_ix_card_line(at_=3.62, life=2.2):
    subpixel True
    alpha 0.0
    xoffset -40
    pause at_
    easeout 0.30 alpha 1.0 xoffset 0
    pause life
    linear 0.24 alpha 0.0

transform msbf_ix_card_rule(at_=3.62):
    subpixel True
    xzoom 0.0
    pause at_ + 0.08
    easeout 0.45 xzoom 1.0
    pause 1.95
    linear 0.24 alpha 0.0

transform msbf_ix_room_seek(at_=0.10):
    # Id: the room decodes in torn holds; nothing eases.
    alpha 0.0
    pause at_
    alpha 1.0
    pause 0.05
    alpha 0.0
    pause 0.09
    alpha 1.0
    pause 0.03
    alpha 0.0
    pause 0.16
    alpha 1.0


# The SMT-style boss card: a slanted band across the lower third, the name in
# huge serif caps, the form in a tag, the epithet above. One screen for the
# entrances and the phase reveals, so every manifestation is announced alike.
screen msbf_px_name_card(name_main, name_sub, kicker, form, accent="#8fe6ff", at_=3.62, corrupted=False, life=2.2):
    $ _acc = _pl_rgba(accent, 1.0)
    fixed:
        xysize (1280, 720)
        add msbf_plate(1460, 168, 46, (0.02, 0.03, 0.07, 0.92), (0.0, 0.01, 0.03, 0.96), _pl_rgba(accent, 0.75), _acc) at msbf_t(msbf_ix_card_plate, at_):
            xpos -90
            ypos 438
        add Solid(accent) xysize (1180, 2) at msbf_t(msbf_ix_card_rule, at_):
            xpos 96
            ypos 562
        text kicker style "msbf_ix_kicker" color accent at msbf_t(msbf_ix_card_line, at_ + 0.10, life):
            xpos 104
            ypos 450
        text name_main style "msbf_ix_name" at msbf_t(msbf_ix_card_name, at_, corrupted):
            xpos 96
            ypos 464
        text name_sub style "msbf_ix_sub" color accent at msbf_t(msbf_ix_card_line, at_ + 0.18, life):
            xpos 104
            ypos 570
        if form:
            fixed:
                xpos 1180
                xanchor 1.0
                ypos 450
                xysize (260, 30)
                at msbf_t(msbf_ix_card_line, at_ + 0.22, life)
                add msbf_plate(260, 30, 10, (0.02, 0.03, 0.06, 0.0), (0.02, 0.03, 0.06, 0.0), _pl_rgba(accent, 0.9))
                text form style "msbf_ix_form" color accent:
                    xalign 0.5
                    yalign 0.5


screen msbf_ix_skip(end_t):
    timer end_t action Return(True)
    button:
        xysize (1280, 720)
        background Solid("#00000000")
        action Return(True)
    key "K_RETURN" action Return(True)
    key "K_SPACE" action Return(True)
    key "K_z" action Return(True)
    key "game_menu" action Return(True)
    key "dismiss" action Return(True)
    text "CLICK / ENTER TO SKIP" style "msbf_cine_skip" at msbf_t(msbf_intro_caption, 1.6, 4, 12.0):
        xpos 1264
        xanchor 1.0
        ypos 700


# -----------------------------------------------------------------------------
# msbf_battle_intro: PHASE 1. Called by cs_matsuda_02_battle (and the Arcade)
# BEFORE the HUD and before the phase-1 music; the heartbeat + wind loops are
# owned by that label. The live battle (msbf_battle_state) is already built,
# so the party that runs in is the party the player picked.
# -----------------------------------------------------------------------------
screen msbf_battle_intro():
    modal True
    use enter_m_input_lock()

    $ _ib = getattr(store, "msbf_battle_state", None)
    $ _T = MSBF_PX_INTRO
    $ _bx, _by = msbf_px_boss_point(1, "head")

    timer _T["fall"] - 0.05 action Function(msbf_play_pooled_sfx, MSBF_SFX["phase"], _update_screens=False)
    timer _T["land"] - 0.02 action Function(renpy.sound.play, MSBF_INTRO_BOOM, channel="sound")
    timer _T["land"] + 0.06 action Function(renpy.sound.play, MSBF_INTRO_THUNDER, channel="sfxtrack1")
    timer _T["sweep"] + 0.10 action Function(msbf_play_pooled_sfx, MSBF_SFX["crit"], _update_screens=False)
    timer _T["card"] + 0.04 action Function(msbf_play_pooled_sfx, MSBF_SFX["weak"], _update_screens=False)

    add Solid("#000000")
    fixed:
        xysize (1280, 720)
        at msbf_t(msbf_ix_cam, 64, _T["land"])
        use msbf_seer_environment(phase=1, charge=0.55)
        add Solid("#02040b") at msbf_t(msbf_ix_dim, _T["run"] + 0.5, _T["land"])
        if _ib is not None:
            add msbf_px_stage(_ib, "intro")

    # A glint high in the sky, exactly where she falls from.
    if MSBF_PX_SHADERS:
        add Transform(Solid("#00000000"), xysize=(120, 120), mesh=True, shader="msbf.pxfx", u_fx_kind=0.0, u_fx_p=0.15, u_fx_cell=3.0, u_fx_c1=(1.0, 1.0, 1.0), u_fx_c2=(0.6, 0.95, 1.0), u_fx_c3=(0.2, 0.5, 0.9), u_fx_seed=3.0, u_fx_angle=0.0, u_fx_solid=0.9) at msbf_t(msbf_ix_glint, _T["fall"] - 0.55, 0.6):
            xcenter _bx
            ycenter 70
    add Solid("#e8fbff") at msbf_t(msbf_ix_flash, _T["land"], 0.95)

    # Her eyes, from her official art, in a slit across the frame.
    fixed:
        xysize (1280, 210)
        ycenter 318
        at msbf_t(msbf_ix_cutin, _T["land"] + 0.42, 0.30)
        add Solid("#050a14") xysize (1280, 210)
        add Transform("addons/Matsuda's Sick Boss Fight/phase1.png", crop=(250, 200, 520, 104)) at msbf_t(msbf_ix_cutin_slide, _T["land"] + 0.42, 0.45):
            xysize (1060, 212)
            xcenter 640
            yalign 0.5
        add Solid("#8fe6ff") xysize (1280, 2)
        add Solid("#8fe6ff") xysize (1280, 2) yalign 1.0

    # The sweep cuts the frame.
    add Solid("#ffffff") xysize (1500, 5) at msbf_t(msbf_ix_split, _T["sweep"] + 0.10):
        xcenter 640
        ycenter 352
        rotate -8
    add Solid("#dff8ff") at msbf_t(msbf_ix_flash, _T["sweep"] + 0.12, 0.45)

    add Solid("#000000") xysize (1280, 78) at msbf_t(msbf_ix_bars, 78, 0.0)
    add Solid("#000000") xysize (1280, 78) at msbf_t(msbf_ix_bars, 78, 0.0):
        ypos 720
        yanchor 1.0

    use msbf_px_name_card("MATSUDA", "CRIMSON-AZURE", "THE ONTOLOGICAL SEER  ·  PHASE I", "NAHOBINO", "#8fe6ff", _T["card"])
    use msbf_ix_skip(_T["end"])


# -----------------------------------------------------------------------------
# msbf_idmode_intro: ID MODE. Starts on the second bar, so there is no fall and
# no build: the image fails to be anything else until it contains her.
# -----------------------------------------------------------------------------
screen msbf_idmode_intro():
    modal True
    use enter_m_input_lock()

    $ _ib = getattr(store, "msbf_battle_state", None)
    $ _T = MSBF_PX_ID_INTRO

    timer _T["boss"] action Function(renpy.sound.play, MSBF_SFX["explode"], channel="sound")
    timer _T["light"] action Function(renpy.sound.play, MSBF_INTRO_THUNDER, channel="sfxtrack1")
    timer _T["card"] + 0.04 action Function(msbf_play_pooled_sfx, MSBF_SFX["phase"], _update_screens=False)

    add Solid("#000000")
    fixed:
        xysize (1280, 720)
        at msbf_t(msbf_ix_room_seek, 0.10)
        use msbf_seer_environment(phase=2, id_mode=True, danger=0.35)
        if _ib is not None:
            add msbf_px_stage(_ib, "id_intro")

    # Whole rows of the frame arriving displaced.
    add Solid("#ff2f55") xysize (1280, 30) at msbf_t(msbf_id_bar, 196, 30, 0.22, 0.06)
    add Solid("#e8e8ee") xysize (1280, 16) at msbf_t(msbf_id_bar, 388, 16, 0.33, 0.05)
    add Solid("#ff2f55") xysize (1280, 44) at msbf_t(msbf_id_bar, 120, 44, 0.80, 0.07)
    add Solid("#0a0a0e") xysize (1280, 80) at msbf_t(msbf_id_bar, 470, 80, 0.86, 0.09)
    add Solid("#e8e8ee") xysize (1280, 12) at msbf_t(msbf_id_bar, 300, 12, 1.12, 0.04)

    # Her eyes -- the halo's gaze -- for one torn hold.
    fixed:
        xysize (1280, 190)
        ycenter 330
        at msbf_t(msbf_ix_cutin, _T["light"] - 0.30, 0.20)
        add Solid("#120208") xysize (1280, 190)
        add Transform("addons/Matsuda's Sick Boss Fight/phase2.png", crop=(588, 270, 304, 64)) at msbf_t(msbf_ix_cutin_slide, _T["light"] - 0.30, 0.30):
            xysize (900, 190)
            xcenter 640
            yalign 0.5
        add Solid("#ff5a7a") xysize (1280, 2)
        add Solid("#ff5a7a") xysize (1280, 2) yalign 1.0

    add Solid("#fff6e0") at msbf_t(msbf_ix_flash, _T["light"], 0.75)

    add Solid("#000000") xysize (1280, 78) at msbf_t(msbf_ix_bars, 78, 0.0)
    add Solid("#000000") xysize (1280, 78) at msbf_t(msbf_ix_bars, 78, 0.0):
        ypos 720
        yanchor 1.0

    use msbf_px_name_card("TOHU IMAGO", "IT WAS ALWAYS AWAKE", "NO SUCH BAR  ·  PHASE II", "FORMLESS IMAGE", "#ffd98a", _T["card"], True)
    use msbf_ix_skip(_T["end"])


style msbf_ix_name:
    font MSBF_HUD_FONT_NAME
    size 88
    color "#fffaf0"
    kerning 6.0
    outlines [(3, "#02040acc", 0, 2)]

style msbf_ix_sub:
    font MSBF_HUD_FONT_NAME
    size 26
    kerning 5.0
    outlines [(2, "#02040acc", 0, 1)]

style msbf_ix_kicker:
    font MSBF_HUD_FONT_TECH
    size 14
    kerning 3.6
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_ix_form:
    font MSBF_HUD_FONT_TECH
    size 15
    kerning 3.0
    outlines [(2, "#02040ae6", 0, 0)]



# -----------------------------------------------------------------------------
# msbf_phase_break_seq: A BAR COMING OFF HER. Composited over the live arena by
# msbf_phase_transition_overlay, so the room is still there underneath and the
# break is happening TO something.
#
# The whole thing is 1.6s and it has three beats and no more: the frame blows
# out white, the frame fractures and the pieces go, and then there is nothing at
# all for a held half-second. The silence is the point -- it is the only moment
# in the fight where the screen has nothing on it, and it is what makes the
# reveal that follows land.
# -----------------------------------------------------------------------------
screen msbf_phase_break_seq(battle):
    $ _bk_x, _bk_y = msbf_boss_anchor(battle.phase)
    $ _bk_cx = _bk_x / 1280.0
    $ _bk_cy = _bk_y / 720.0
    $ _bk_col = (1.0, 0.30, 0.40) if battle.phase >= 3 else (1.0, 0.86, 0.52)

    # 1. BLOWOUT -- one frame of pure white, then gone.
    add Solid("#ffffff") at msbf_brk_blowout

    # 2. FRACTURE -- the frame is a pane and it just took the hit.
    if MSBF_CINE_SHADERS:
        add Solid("#00000000") xysize (1280, 720) at msbf_t(msbf_crack_t, 0.02, 0.72, _bk_cx, _bk_cy, _bk_col, 15.0)
    if MSBF_FX_SHADERS:
        add Solid("#00000000") xysize (2200, 2200) at msbf_t(msbf_big_shock_r, 0.03, _bk_col, 1.0):
            xcenter _bk_x
            ycenter _bk_y
        add Solid("#00000000") xysize (760, 760) at msbf_t(msbf_fx_glow_pop, _bk_col, 1.0, 1.5, 0.55):
            xcenter _bk_x
            ycenter _bk_y

    # 3. SILENCE -- black closes over the wreckage and holds.
    add Solid("#000000") at msbf_brk_hold


# -----------------------------------------------------------------------------
# msbf_phase_reveal_seq: WHAT WALKS OUT OF THE BREAK.
#
# PHASE 2 (the angel) is a DESCENT and it is the calmest thing in the fight.
# A single shaft of light opens out of the black, widens, and she comes down
# through it over two and a half seconds with nothing snapping anywhere. She
# touches down, the deck answers with one soft ring, and the card settles. The
# restraint is the characterisation: she is not trying to frighten anyone.
#
# PHASE 3 corrupts that grammar: the shaft is red, the boss tears into place
# through channel splits and abrupt cuts, and the card arrives already wrong.
# -----------------------------------------------------------------------------
screen msbf_phase_reveal_world(battle):
    $ _rv_p3 = battle.phase >= 3
    $ _rv_stage = msbf_boss_stage(battle.phase)
    $ _rv_title = getattr(battle, "phase_transition_title", "THE STAGE BEGINS ANEW")
    $ _rv_sub = getattr(battle, "phase_transition_subtitle", "A WINGED ANGEL REWRITES THE SCRIPT")
    $ _rv_key = (1.0, 0.30, 0.40) if _rv_p3 else (1.0, 0.85, 0.48)
    $ _rv_hex = "#ff3b52" if _rv_p3 else "#ffd98a"

    add Solid("#000000") at (msbf_phase_transition_blackout if _rv_p3 else msbf_cine_reveal_blackout)

    add (MSBF_SEER_ART + "seal.png") at msbf_t(msbf_cine_seal, 0.45, _rv_p3):
        xcenter _rv_stage["cx"]
        ycenter _rv_stage["cy"]
        xysize (550, 550)

    # THE SHAFT. One tall soft column that opens from a slit. Everything else in
    # the beat hangs off it, which is why it is the first thing to move.
    if MSBF_FX_SHADERS:
        add Solid("#00000000") xysize (400, 980) at msbf_t(msbf_fx_glow_t, _rv_key, 0.95, 1.05), msbf_t(msbf_desc_shaft, 0.10):
            xalign 0.5
            ypos 0
    else:
        add Solid(_rv_hex) xysize (400, 980) at msbf_t(msbf_desc_shaft, 0.10):
            xalign 0.5
            ypos 0

    # Halo rings lying around the shaft, opening as she comes down through it.
    if MSBF_FX_SHADERS:
        add Solid("#00000000") xysize (1100, 1100) at msbf_t(msbf_fx_ring_t, _rv_key, 0.05, 1.4, 2.6), msbf_t(msbf_desc_halo, 0.55, 1.0):
            xcenter 640
            ycenter _rv_stage["cy"]
        add Solid("#00000000") xysize (760, 760) at msbf_t(msbf_fx_ring_t, (1.0, 1.0, 1.0), 0.04, 1.1, 2.6), msbf_t(msbf_desc_halo, 0.95, 1.0):
            xcenter 640
            ycenter _rv_stage["cy"]

    # The arriving form herself is drawn by the pixel stage (pixel_stage.rpy,
    # MSBFPixelStage._boss_pose's reveal branch), in front of this light and
    # behind the party: the descent for Tohu Imago, the genre failing into
    # place for Imago Rupta.


screen msbf_phase_reveal_seq(battle):
    # Only light and the title sit above the party. The world screen owns the
    # actual arrival, so Imago Rupta cannot cover the nearer cast portraits.
    $ _rv_p3 = battle.phase >= 3
    $ _rv_stage = msbf_boss_stage(battle.phase)
    $ _rv_title = getattr(battle, "phase_transition_title", "THE STAGE BEGINS ANEW")
    $ _rv_sub = getattr(battle, "phase_transition_subtitle", "A WINGED ANGEL REWRITES THE SCRIPT")
    $ _rv_key = (1.0, 0.30, 0.40) if _rv_p3 else (1.0, 0.85, 0.48)
    $ _rv_hex = "#ff3b52" if _rv_p3 else "#ffd98a"

    # TOUCHDOWN. One soft bloom and one ring along the deck. Not an explosion.
    add Solid(_rv_hex) at msbf_t(msbf_desc_touchdown, 3.05)
    if MSBF_FX_SHADERS:
        add Solid("#00000000") xysize (2000, 2000) at msbf_t(msbf_desc_ring, 3.05, _rv_key):
            xcenter _rv_stage["cx"]
            ycenter _rv_stage["foot"]

    # Phase 3 only: the frame refusing to hold the new form.
    if _rv_p3:
        add Solid("#ff2f55") xysize (1280, 26) at msbf_t(msbf_id_bar, 210, 26, 3.20, 0.06)
        add Solid("#e8e8ee") xysize (1280, 14) at msbf_t(msbf_id_bar, 432, 14, 3.34, 0.05)
        add Solid("#ff2f55") xysize (1280, 38) at msbf_t(msbf_id_bar, 148, 38, 3.52, 0.06)

    # The card sits in the DARK lower third. Centred on the frame it landed
    # squarely on the phase-2 sprite -- white text with a white outline over
    # a wall of white wings, which is nearly invisible in the one shot the
    # whole beat is building to.
    use msbf_cine_border(2.70)
    if _rv_p3:
        use msbf_px_name_card("IMAGO RUPTA", _rv_sub, "THE GENRE FAILS  ·  PHASE III", "RUPTURED IMAGE", _rv_hex, 3.10, True)
    else:
        use msbf_px_name_card("TOHU IMAGO", _rv_sub, _rv_title + "  ·  PHASE II", "FORMLESS IMAGE", _rv_hex, 3.10, False)


style msbf_cine_skip:
    font gui.default_font
    size 12
    color "#bdc5d2"
    kerning 1.2
    outlines [(1, "#050b14", 0, 1)]
