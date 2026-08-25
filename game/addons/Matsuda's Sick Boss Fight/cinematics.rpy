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
# She comes DOWN, hard, and the frame takes it. The old version drifted her up
# out of the dark on a slow fade, which is a ghost's entrance, not a fighter's.
transform msbf_intro_fall:
    subpixel True
    alpha 0.0
    yoffset -520
    zoom 1.22
    rotate -4.0
    pause 0.55
    alpha 1.0
    easein 0.42 yoffset 0 zoom 1.0 rotate 0.0
    # the landing: she compresses, then sets
    easeout 0.09 zoom 0.955 yoffset 14
    easeout 0.16 zoom 1.012 yoffset -4
    easeout 0.22 zoom 1.0 yoffset 0

# Two hard trails that only exist during the fall itself.
transform msbf_intro_fall_trail(delay=0.0, drop=180):
    subpixel True
    alpha 0.0
    yoffset -520 - drop
    zoom 1.30
    pause 0.55 + delay
    alpha 0.34
    easein 0.42 yoffset -drop zoom 1.04
    linear 0.10 alpha 0.0

# The deck answering the landing: a hard bloom that snaps and decays.
transform msbf_intro_landing_flash(delay=0.97):
    alpha 0.0
    pause delay
    alpha 0.92
    easeout 0.10 alpha 0.30
    easeout 0.46 alpha 0.0

transform msbf_intro_letterbox_in(h=96, delay=0.0):
    subpixel True
    ysize 0
    pause delay
    easeout 0.34 ysize h

transform msbf_intro_name_slam(delay=0.0):
    subpixel True
    alpha 0.0
    zoom 1.85
    pause delay
    alpha 1.0
    easein 0.11 zoom 1.0
    pause 2.2
    linear 0.30 alpha 0.0

transform msbf_intro_kicker_wipe(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset -40
    pause delay
    easeout 0.30 alpha 1.0 xoffset 0
    pause 1.9
    linear 0.28 alpha 0.0 xoffset 26

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

transform msbf_desc_boss(delay=0.5):
    subpixel True
    alpha 0.0
    yoffset -430
    zoom 0.72
    pause delay
    linear 0.5 alpha 1.0
    easeout 2.6 yoffset 0 zoom 1.0

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

transform msbf_desc_ring(delay=3.1):
    mesh True
    shader "msbf.ring"
    u_color (1.0, 0.85, 0.48)
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

transform msbf_desc_title(delay=0.0):
    subpixel True
    alpha 0.0
    yoffset 18
    pause delay
    easeout 0.85 alpha 1.0 yoffset 0
    pause 1.5
    linear 0.6 alpha 0.0

# --- ID MODE ENTRANCE (the failure to be anything else) ----------------------
# No easing anywhere. Every value is a cut. The screen behaves like a file that
# will not decode: it holds, tears, holds a different way, and one of the holds
# happens to have her in it.
transform msbf_id_seek(delay=0.0):
    subpixel True
    alpha 0.0
    pause delay
    alpha 1.0
    pause 0.06
    alpha 0.0
    pause 0.11
    alpha 1.0
    pause 0.03
    alpha 0.0
    pause 0.22
    alpha 1.0
    pause 0.09
    alpha 0.0
    pause 0.07
    alpha 1.0

transform msbf_id_boss(delay=0.0):
    mesh True
    shader "msbf.smear"
    u_sm_dir (1.0, 0.0)
    u_sm_ghost 0.6
    u_sm_amount 0.0
    u_sm_split 26.0
    subpixel True
    alpha 0.0
    zoom 1.16
    pause delay
    # it does not fade in. it is simply there, wrong, and then less wrong.
    alpha 1.0
    zoom 1.0
    pause 0.10
    u_sm_split 3.0
    pause 0.05
    u_sm_split 20.0
    xoffset 22
    pause 0.07
    u_sm_split 1.5
    xoffset -14
    pause 0.13
    xoffset 0
    u_sm_split 12.0
    pause 0.05
    u_sm_split 0.8

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

transform msbf_id_title(delay=0.0):
    subpixel True
    alpha 0.0
    pause delay
    alpha 1.0
    xoffset 0
    pause 0.05
    xoffset 9
    pause 0.04
    xoffset -6
    pause 0.05
    xoffset 0
    pause 1.9
    alpha 0.0
    pause 0.05
    alpha 1.0
    pause 0.5
    linear 0.35 alpha 0.0

# --- THE BAR BREAK -----------------------------------------------------------
# ABRUPT. The old break spent 3.4 seconds on black with a slow charge in it,
# which is the pacing of a summoning, not of something being broken off a boss.
# This one is done in well under two: blowout, fracture, one held silence.
transform msbf_brk_blowout:
    alpha 1.0
    pause 0.05
    linear 0.06 alpha 0.0

transform msbf_brk_afterimage:
    # her shape burned into the frame for a beat after the light goes
    subpixel True
    alpha 0.0
    pause 0.06
    alpha 0.55
    linear 0.55 alpha 0.0

transform msbf_brk_slam:
    subpixel True
    zoom 1.14
    xoffset 0
    easeout 0.05 zoom 1.09 xoffset 22
    easeout 0.05 zoom 1.06 xoffset -16
    easeout 0.07 zoom 1.03 xoffset 9
    easeout 0.34 zoom 1.0 xoffset 0

transform msbf_brk_hold:
    # the silence after: pure black, held just long enough to be felt
    alpha 0.0
    pause 0.62
    linear 0.18 alpha 1.0


# -----------------------------------------------------------------------------
# 3. SCREENS
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# msbf_battle_intro: PHASE 1. Played BEFORE the battle UI and before the phase-1
# music by cs_matsuda_02_battle via `call screen`, over the already-scened
# arena. The heartbeat + wind LOOPS are owned by the calling label, so the music
# only starts after this returns. Skippable by click or key.
#
# The shape: wind and pressure in the dark -> she DROPS into frame and lands ->
# the deck answers -> the name hits on the boom. The old version faded her up
# out of the floor over two seconds, which gave the biggest entrance in the
# game the body language of a cutscene transition.
# -----------------------------------------------------------------------------
screen msbf_battle_intro():
    modal True
    use enter_m_input_lock()

    $ _intro_name = "MATSUDA, CRIMSON-AZURE"
    $ _intro_stage = msbf_boss_stage(1)

    # One-shot stingers, cued to the landing rather than to the name card.
    timer 0.95 action Function(renpy.sound.play, MSBF_INTRO_BOOM, channel="sound")
    timer 1.02 action Function(renpy.sound.play, MSBF_INTRO_THUNDER, channel="sfxtrack1")
    timer 4.30 action Return(True)

    # The room, pre-lit and dark, taking the impact with the rest of the frame.
    fixed:
        xysize (1280, 720)
        at msbf_brk_slam

        add "bg battle_setpiece" at msbf_arena_t(1, 0.55, 0.0, 0.0, 0.0):
            xysize (1280, 720)
        add Solid("#02040bd8") xysize (1280, 720) at msbf_intro_dim(0.62)

        use msbf_ground_shadow(_intro_stage["cx"], _intro_stage["foot"], _intro_stage["shadow_w"], _intro_stage["shadow_a"], True)

        # Two hard trails, then her. All three only exist during the fall.
        add "msbf_matsuda_phase1" at msbf_intro_fall_trail(0.05, 210):
            xcenter _intro_stage["cx"]
            ycenter _intro_stage["cy"]
            xysize (_intro_stage["w"], _intro_stage["h"])
            fit "contain"
        add "msbf_matsuda_phase1" at msbf_intro_fall_trail(0.10, 110):
            xcenter _intro_stage["cx"]
            ycenter _intro_stage["cy"]
            xysize (_intro_stage["w"], _intro_stage["h"])
            fit "contain"
        add "msbf_matsuda_phase1" at msbf_intro_fall:
            xcenter _intro_stage["cx"]
            ycenter _intro_stage["cy"]
            xysize (_intro_stage["w"], _intro_stage["h"])
            fit "contain"

    # The deck answering: bloom at her feet + a ring travelling out along it.
    if MSBF_FX_SHADERS:
        add Solid("#00000000") xysize (900, 320) at msbf_fx_glow_t((0.42, 0.86, 1.0), 1.0, 1.7), msbf_intro_landing_flash(0.97):
            xcenter _intro_stage["cx"]
            ycenter _intro_stage["foot"]
        add Solid("#00000000") xysize (1900, 1900) at msbf_big_shock_r(0.98, (0.55, 0.92, 1.0), 0.85):
            xcenter _intro_stage["cx"]
            ycenter _intro_stage["foot"]
    add Solid("#dff4ff") at msbf_intro_landing_flash(0.96)

    # Letterbox opens on the landing, not before it.
    add Solid("#000000") xysize (1280, 96) at msbf_intro_letterbox_in(84, 0.98):
        ypos 0
    add Solid("#000000") xysize (1280, 118) at msbf_intro_letterbox_in(112, 0.98):
        ypos 720
        yanchor 1.0

    # The card sits BELOW her feet (she lands with her lowest pixel around
    # y 513), so the title never crosses her legs.
    text "THE STAGE PRESENTS" style "msbf_intro_kicker" at msbf_intro_kicker_wipe(1.16):
        xalign 0.5
        ypos 528
        yanchor 0.5
    text _intro_name style "msbf_intro_title_text" at msbf_intro_name_slam(1.30):
        xalign 0.5
        ypos 578
        yanchor 0.5
    text "THE CURTAIN RISES" style "msbf_phase_transition_subtitle" at msbf_intro_kicker_wipe(1.72):
        xalign 0.5
        ypos 634
        yanchor 0.5

    button:
        xysize (1280, 720)
        background Solid("#00000000")
        action Return(True)
    key "K_RETURN" action Return(True)
    key "K_SPACE" action Return(True)
    key "game_menu" action Return(True)
    key "dismiss" action Return(True)

    text "CLICK TO SKIP" style "msbf_intro_skip_hint" at msbf_intro_caption(1.6, 4, 12.0):
        xpos 1264
        xanchor 1.0
        ypos 690


# -----------------------------------------------------------------------------
# msbf_idmode_intro: ID MODE'S OPENING. Id Mode starts on the second bar, so it
# never had an entrance at all -- the fight simply began. It gets one now, and
# it is the deliberate opposite of the phase-2 descent the normal route earns.
#
# Normal phase 2 is an ARRIVAL: the roof opens, light pours in, she comes down
# through it on a four-second ease, and the title settles. Every one of those is
# a promise that this is a performance with a running order.
#
# Id Mode makes none of those promises. There is no descent because there is no
# above; the image just fails to be anything else, several times, and one of the
# failures has her standing in it. Nothing eases. The title mis-renders. The
# only thing the two entrances share is the boss.
# -----------------------------------------------------------------------------
screen msbf_idmode_intro():
    modal True
    use enter_m_input_lock()

    $ _id_stage = msbf_boss_stage(2)

    timer 0.30 action Function(renpy.sound.play, MSBF_SFX["explode"], channel="sound")
    timer 1.05 action Function(renpy.sound.play, MSBF_INTRO_THUNDER, channel="sfxtrack1")
    timer 3.90 action Return(True)

    add Solid("#000000")

    # The room, seeking. It appears in the wrong order, several times, before it
    # holds -- and it is the phase-3 room, not phase 2's, because whatever this
    # is has already been what it is going to be.
    fixed:
        xysize (1280, 720)
        at msbf_id_seek(0.18)
        add "msbf_rupture_sky" at msbf_arena_t(3, 0.0, 0.0, 0.0, 0.85):
            xysize (1280, 720)

    # Tear bars: whole rows of the frame arriving displaced.
    add Solid("#ff2f55") xysize (1280, 34) at msbf_id_bar(196, 34, 0.22, 0.06)
    add Solid("#e8e8ee") xysize (1280, 18) at msbf_id_bar(388, 18, 0.31, 0.05)
    add Solid("#ff2f55") xysize (1280, 46) at msbf_id_bar(120, 46, 0.44, 0.07)
    add Solid("#0a0a0e") xysize (1280, 90) at msbf_id_bar(470, 90, 0.52, 0.09)
    add Solid("#e8e8ee") xysize (1280, 12) at msbf_id_bar(300, 12, 0.71, 0.04)
    add Solid("#ff2f55") xysize (1280, 28) at msbf_id_bar(556, 28, 0.88, 0.06)

    # She is in one of the holds. Not descending, not rising -- present.
    add "msbf_matsuda_phase2" at msbf_id_boss(0.40):
        xcenter _id_stage["cx"]
        ycenter _id_stage["cy"]
        xysize (_id_stage["w"], _id_stage["h"])
        fit "contain"

    # NO fracture here, deliberately. Glass breaking is the bar-break's
    # metaphor -- something solid taking a hit -- and Id Mode's whole premise is
    # that there was never anything solid to break. It tears like a signal
    # instead, which is what the bars above are doing.
    add Solid("#ffffff") at msbf_brk_blowout
    add Solid("#12000a") at msbf_id_seek(1.02)

    text "NO SUCH BAR" style "msbf_intro_kicker" at msbf_id_title(1.35):
        xalign 0.5
        yalign 0.635
    text "TOHU IMAGO" style "msbf_intro_title_text" at msbf_id_title(1.42):
        xalign 0.5
        yalign 0.715
    text "IT WAS ALWAYS AWAKE" style "msbf_phase_transition_subtitle" at msbf_id_title(1.86):
        xalign 0.5
        yalign 0.80

    button:
        xysize (1280, 720)
        background Solid("#00000000")
        action Return(True)
    key "K_RETURN" action Return(True)
    key "K_SPACE" action Return(True)
    key "game_menu" action Return(True)
    key "dismiss" action Return(True)

    text "CLICK TO SKIP" style "msbf_intro_skip_hint" at msbf_intro_caption(1.6, 4, 12.0):
        xpos 1264
        xanchor 1.0
        ypos 690


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
        add Solid("#00000000") xysize (1280, 720) at msbf_crack_t(0.02, 0.72, _bk_cx, _bk_cy, _bk_col, 15.0)
    if MSBF_FX_SHADERS:
        add Solid("#00000000") xysize (2200, 2200) at msbf_big_shock_r(0.03, _bk_col, 1.0):
            xcenter _bk_x
            ycenter _bk_y
        add Solid("#00000000") xysize (760, 760) at msbf_fx_glow_pop(_bk_col, 1.0, 1.5, 0.55):
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
# PHASE 3 keeps the same skeleton and corrupts every joint of it -- the shaft
# is red and stutters, the descent is a series of cuts, and the card arrives
# already wrong.
# -----------------------------------------------------------------------------
screen msbf_phase_reveal_seq(battle):
    $ _rv_p3 = battle.phase >= 3
    $ _rv_stage = msbf_boss_stage(battle.phase)
    $ _rv_title = getattr(battle, "phase_transition_title", "THE STAGE BEGINS ANEW")
    $ _rv_sub = getattr(battle, "phase_transition_subtitle", "A WINGED ANGEL REWRITES THE SCRIPT")
    $ _rv_key = (1.0, 0.30, 0.40) if _rv_p3 else (1.0, 0.85, 0.48)
    $ _rv_hex = "#ff3b52" if _rv_p3 else "#ffd98a"

    add Solid("#000000") at msbf_phase_transition_blackout

    # THE SHAFT. One tall soft column that opens from a slit. Everything else in
    # the beat hangs off it, which is why it is the first thing to move.
    if MSBF_FX_SHADERS:
        add Solid("#00000000") xysize (400, 980) at msbf_fx_glow_t(_rv_key, 0.95, 1.05), msbf_desc_shaft(0.10):
            xalign 0.5
            ypos 0
    else:
        add Solid(_rv_hex) xysize (400, 980) at msbf_desc_shaft(0.10):
            xalign 0.5
            ypos 0

    # Halo rings lying around the shaft, opening as she comes down through it.
    if MSBF_FX_SHADERS:
        add Solid("#00000000") xysize (1100, 1100) at msbf_fx_ring_t(_rv_key, 0.05, 1.4, 2.6), msbf_desc_halo(0.55, 1.0):
            xcenter 640
            ycenter _rv_stage["cy"]
        add Solid("#00000000") xysize (760, 760) at msbf_fx_ring_t((1.0, 1.0, 1.0), 0.04, 1.1, 2.6), msbf_desc_halo(0.95, 1.0):
            xcenter 640
            ycenter _rv_stage["cy"]

    # HER. In phase 2 this is one long ease and nothing else; in phase 3 the
    # same descent is run through the datamosh so it arrives in pieces.
    if _rv_p3 and MSBF_FX_SHADERS:
        add battle.boss_art at msbf_fx_glitch_pulse(0.35, 0.95, 30.0), msbf_desc_boss(0.45):
            xcenter _rv_stage["cx"]
            ycenter _rv_stage["cy"]
            xysize (_rv_stage["w"], _rv_stage["h"])
            fit "contain"
    else:
        add battle.boss_art at msbf_desc_boss(0.55):
            xcenter _rv_stage["cx"]
            ycenter _rv_stage["cy"]
            xysize (_rv_stage["w"], _rv_stage["h"])
            fit "contain"

    # TOUCHDOWN. One soft bloom and one ring along the deck. Not an explosion.
    add Solid(_rv_hex) at msbf_desc_touchdown(3.05)
    if MSBF_FX_SHADERS:
        add Solid("#00000000") xysize (2000, 2000) at msbf_desc_ring(3.05):
            xcenter _rv_stage["cx"]
            ycenter _rv_stage["foot"]

    # Phase 3 only: the frame refusing to hold the new form.
    if _rv_p3:
        add Solid("#ff2f55") xysize (1280, 26) at msbf_id_bar(210, 26, 3.20, 0.06)
        add Solid("#e8e8ee") xysize (1280, 14) at msbf_id_bar(432, 14, 3.34, 0.05)
        add Solid("#ff2f55") xysize (1280, 38) at msbf_id_bar(148, 38, 3.52, 0.06)

    # The card sits in the DARK lower third. Centred on the frame it landed
    # squarely on the phase-2 sprite -- white text with a white outline over
    # a wall of white wings, which is nearly invisible in the one shot the
    # whole beat is building to.
    text _rv_title style "msbf_phase_transition_title" at (msbf_id_title(3.35) if _rv_p3 else msbf_desc_title(3.30)):
        xalign 0.5
        ypos 598
        yanchor 0.5
    text _rv_sub style "msbf_phase_transition_subtitle" at (msbf_id_title(3.55) if _rv_p3 else msbf_desc_title(3.62)):
        xalign 0.5
        ypos 654
        yanchor 0.5
