# =============================================================================
# ui.rpy  --  MATSUDA'S SICK BOSS FIGHT :: SCREENS + PRESENTATION
# =============================================================================
#
# WHAT THIS FILE IS
#   The entire visual front-end for the boss fight. The rules/state live in
#   battle_logic.rpy (the MSBFBattleState object); this file is screens +
#   transforms + styles that DRAW that state and forward player input back into
#   it. The optional GPU polish (shader meters/auras, particles) is in fx.rpy.
#
# THE TWO SCREENS THE STORY ENTERS DIRECTLY (called from cs_matsuda_02.rpy)
#   screen msbf_party_select()        -> the 7-character party picker; Returns the
#                                        chosen id list (used by msbf_new_battle).
#   screen msbf_battle_screen(battle) -> THE fight. Reads `battle` (an
#                                        MSBFBattleState) every redraw, renders the
#                                        boss/party/press-turns/log/command menu,
#                                        and calls battle.player_use_skill(...) /
#                                        player_pass() / start_enemy_phase() / etc.
#                                        Returns "victory" (or other) when done.
#
# SUPPORTING SCREENS (composed into the above)
#   msbf_battle_backdrop          : per-phase animated background.
#   msbf_fx_layer(battle)         : polls battle.fx_event + battle.float_events
#                                   (the feeds from battle_logic) and draws hit
#                                   flashes + floating damage/heal numbers.
#   msbf_phase_transition_overlay : the bar-break / phase-change cinematic.
#   msbf_phase2_boom_overlay / msbf_phase3_rupture_overlay : phase ambiance.
#   msbf_shmup_overlay(battle)    : the phase-3 bullet-hell. Static chrome only;
#                                   MSBFShmupField steps the sim inside its own
#                                   render() at a fixed 30Hz and draws at 60fps.
#   msbf_press_turn_icon / _fx_icon, msbf_meter, msbf_party_card : small reusable
#                                   widgets (icons, HP/MP bars, party cards).
#
# FILE LAYOUT
#   1. boss sprite image defines + a couple of motion-fps constants.
#   2. a LARGE transform library (the msbf_* / msbf_phase*_ / msbf_boss_*
#      animations -- backgrounds, boss idle/hit/cast, phase FX, press-turn FX).
#   3. the screens listed above.
#   4. styles (msbf_*), the fight's cyan/red theme.
#
# NOTE: shares the battle_logic globals (msbf_battle_state, msbf_battle_menu_locked)
#   and the MSBF_* data tables/helpers; uses MSBF_FX_SHADERS (fx.rpy) to decide
#   whether to layer the shader meters/auras over the flat-Solid fallbacks.
# =============================================================================

# --- BOSS SPRITE IMAGES (one per phase) + the rupture backdrop art -----------
image msbf_matsuda_phase1 = Transform("addons/Matsuda's Sick Boss Fight/phase1.png", fit="contain", xysize=(620, 384))
image msbf_matsuda_phase2 = Transform("addons/Matsuda's Sick Boss Fight/phase2.png", fit="contain", xysize=(735, 384))
image msbf_matsuda_phase3 = Transform("addons/Matsuda's Sick Boss Fight/idmode/idphase.png", fit="contain", xysize=(735, 384))
image msbf_rupture_backdrop = Transform("addons/Matsuda's Sick Boss Fight/idmode/rupture.png", fit="cover", xysize=(1280, 720))

init -1 python:
    import math

    # (The phase 2/3 boss float used to be computed here from a screen tick; it now
    # lives entirely in the idle ATL transforms, so no per-tick anchor is needed.)

    # -------------------------------------------------------------------------
    # THE FIGHT'S PHASE PALETTE
    # phase -> (primary accent, secondary accent). Every panel rail, banner,
    # deck edge and turn banner in this file reads its colour from here, so
    # re-theming a phase is a one-line edit instead of eight scattered inline
    # ternaries that were already drifting out of step with each other.
    # -------------------------------------------------------------------------
    MSBF_PHASE_ACCENT = {
        1: ("#55ddff", "#ffcf66"),
        2: ("#ffcf66", "#ff3868"),
        3: ("#ff3868", "#a66bff"),
    }

    def msbf_phase_accent(phase):
        """Return (primary, secondary) for a phase, clamped to the table."""
        try:
            phase = int(phase)
        except (TypeError, ValueError):
            phase = 1
        return MSBF_PHASE_ACCENT.get(min(3, max(1, phase)), MSBF_PHASE_ACCENT[1])

    # -------------------------------------------------------------------------
    # WHERE PARTY CARD `i` SITS
    # Floating numbers, HP-bar chips, cast wind-ups, ally targeting and KO
    # bursts all have to land on the same card, and each one used to re-derive
    # the position from the raw deck constants -- so the +12 / +7 insets were
    # baked into five places and retuning the grid meant finding all of them.
    # `geom` is the tuple the battle screen builds once (_deck_geom).
    # -------------------------------------------------------------------------
    def msbf_card_origin(i, geom):
        """Top-left of card `i`, in screen px."""
        ox, oy, cols, step_x, step_y = geom[:5]
        return (ox + (i % cols) * step_x, oy + (i // cols) * step_y)

    def msbf_card_center(i, geom):
        """Centre of card `i`, in whole screen px."""
        x, y = msbf_card_origin(i, geom)
        return (int(x + geom[5] // 2), int(y + geom[6] // 2))

# =============================================================================
# --- 2. TRANSFORM LIBRARY ---------------------------------------------------
# The bulk of this file: parameterised animations the screens apply with `at`.
# Naming groups roughly by purpose:
#   msbf_bg_* / msbf_phase2_bg_* / msbf_phase3_bg_*  : animated backgrounds.
#   msbf_boss_* / msbf_boss_phase_* / msbf_boss_rupture_* : boss idle/hit/cast/
#                                                     echo motion, one set per phase.
#   msbf_phase_transition_* / msbf_phase_break_*      : the bar-break cinematic.
#   msbf_final_victory_*                              : the finishing whiteout.
#   msbf_press_turn_*                                 : press-turn icon FX.
#   msbf_fx_* / msbf_stage_*                          : hit flashes, slashes, sweeps.
# These are pure presentation; none of them touch battle rules.
# =============================================================================
transform msbf_bg_drift:
    subpixel True
    zoom 1.08
    xalign 0.50
    yalign 0.50
    ease 6.0 xalign 0.47 yalign 0.48
    ease 7.0 xalign 0.53 yalign 0.52
    ease 5.5 xalign 0.50 yalign 0.50
    repeat

transform msbf_phase2_bg_dizzy:
    subpixel True
    zoom 1.42
    xalign 0.50
    yalign 0.50
    rotate 0.0
    parallel:
        ease 7.0 xalign 0.45 yalign 0.46
        ease 8.4 xalign 0.55 yalign 0.54
        ease 6.2 xalign 0.48 yalign 0.56
        ease 7.6 xalign 0.50 yalign 0.50
        repeat
    parallel:
        ease 10.0 rotate 0.48
        ease 12.0 rotate -0.42
        repeat

transform msbf_phase2_bg_veil(delay=0.0, alpha_max=0.18, direction=1.0):
    subpixel True
    alpha 0.0
    zoom 1.58
    xalign 0.50
    yalign 0.50
    rotate -0.8 * direction
    pause delay
    parallel:
        block:
            ease 1.4 alpha alpha_max
            ease 4.2 alpha alpha_max * 0.42
            ease 1.8 alpha alpha_max
            repeat
    parallel:
        block:
            ease 9.0 xalign 0.44 yalign 0.54 rotate 1.05 * direction
            ease 11.0 xalign 0.56 yalign 0.46 rotate -0.90 * direction
            ease 7.0 xalign 0.50 yalign 0.50 rotate 0.20 * direction
            repeat


transform msbf_phase2_boom_pressure(peak=0.46):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 640
    ypos 360
    alpha 0.0
    zoom 1.0
    linear 0.035 alpha peak zoom 1.025
    linear 0.080 alpha peak * 0.45 zoom 1.060
    linear 0.360 alpha 0.0 zoom 1.140

transform msbf_phase2_boom_wave(angle=0.0, delay=0.0, alpha_max=0.46):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    rotate angle
    alpha 0.0
    xzoom 0.18
    yzoom 0.70
    pause delay
    linear 0.045 alpha alpha_max xzoom 0.90 yzoom 1.0
    linear 0.220 alpha 0.0 xzoom 1.58 yzoom 1.50

transform msbf_phase2_boom_slab(angle=0.0, delay=0.0, alpha_max=0.34, direction=1.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 640 - (820 * direction)
    ypos 360
    rotate angle
    alpha 0.0
    zoom 0.90
    pause delay
    linear 0.040 alpha alpha_max xpos 640 - (80 * direction) zoom 1.0
    linear 0.180 alpha 0.0 xpos 640 + (760 * direction) zoom 1.12

transform msbf_phase2_boom_scan(delay=0.0, alpha_max=0.32, direction=1.0):
    subpixel True
    xoffset -24 * direction
    alpha 0.0
    pause delay
    linear 0.035 alpha alpha_max xoffset 18 * direction
    linear 0.060 alpha alpha_max * 0.32 xoffset -12 * direction
    linear 0.160 alpha 0.0 xoffset 0

transform msbf_phase_break_flash(delay=0.0, peak=0.90):
    alpha 0.0
    pause delay
    linear 0.025 alpha peak
    linear 0.070 alpha peak * 0.36
    linear 0.120 alpha 0.0

transform msbf_phase_break_lance(angle=0.0, delay=0.0, alpha_max=0.90):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    rotate angle
    alpha 0.0
    zoom 0.22
    pause delay
    linear 0.035 alpha alpha_max zoom 1.0
    linear 0.105 alpha 0.0 zoom 1.58

transform msbf_phase_reveal_bloom(delay=0.0, peak=0.56):
    alpha 0.0
    pause delay
    linear 0.035 alpha peak
    linear 0.12 alpha 0.0
    pause 0.18
    linear 0.025 alpha peak * 0.42
    linear 0.18 alpha 0.0

transform msbf_phase_reveal_cut(angle=0.0, delay=0.0, alpha_max=0.84):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    rotate angle
    alpha 0.0
    xzoom 0.20
    pause delay
    linear 0.06 alpha alpha_max xzoom 1.0
    linear 0.28 alpha 0.0 xzoom 1.24

transform msbf_phase_transition_blackout:
    alpha 1.0
    pause 0.74
    linear 0.035 alpha 0.72
    linear 0.045 alpha 1.0
    pause 0.25
    linear 0.055 alpha 0.54
    linear 0.040 alpha 0.92
    linear 0.42 alpha 0.0

transform msbf_phase_transition_curtain:
    alpha 0.0
    linear 0.16 alpha 0.78
    pause 0.72
    linear 0.58 alpha 0.42
    pause 1.24
    linear 0.78 alpha 0.0

transform msbf_phase_transition_burst(delay=0.0, peak=0.72):
    alpha 0.0
    pause delay
    linear 0.06 alpha peak
    linear 0.12 alpha 0.0
    pause 0.16
    linear 0.04 alpha peak * 0.54
    linear 0.20 alpha 0.0

transform msbf_phase_transition_ring(delay=0.0, spin=1.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom 0.30
    rotate 0.0
    pause delay
    parallel:
        easeout 1.20 alpha 0.58 zoom 1.32
        linear 0.46 alpha 0.0 zoom 1.58
    parallel:
        linear 1.66 rotate 180.0 * spin

transform msbf_phase_transition_lance(angle=0.0, delay=0.0, alpha_max=0.78):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    rotate angle
    alpha 0.0
    zoom 0.72
    pause delay
    linear 0.06 alpha alpha_max zoom 1.0
    linear 0.30 alpha 0.0 zoom 1.38

transform msbf_phase_transition_title(delay=0.0):
    alpha 0.0
    yoffset 22
    zoom 0.90
    pause delay
    linear 0.16 alpha 1.0 yoffset 0 zoom 1.04
    pause 2.55
    linear 0.45 alpha 0.0 yoffset -18 zoom 1.12

transform msbf_phase_transition_subtitle(delay=0.0):
    alpha 0.0
    yoffset 10
    pause delay
    linear 0.22 alpha 1.0 yoffset 0
    pause 3.20
    linear 0.50 alpha 0.0 yoffset -8

# Hypernova rumble: a tremor that BUILDS as the boss destabilises, a held
# breath at the implosion, then a violent slam at detonation that decays out.
# Timed to msbf_boss_collapse + the nova overlay.
transform msbf_final_victory_rumble(strength=1.0, delay=0.0):
    subpixel True
    xoffset 0
    yoffset 0
    # building tremor (0 -> ~0.63)
    linear 0.05 xoffset -1 * strength yoffset 1 * strength
    linear 0.05 xoffset 1 * strength yoffset -1 * strength
    linear 0.05 xoffset -2 * strength yoffset 1 * strength
    linear 0.05 xoffset 2 * strength yoffset -2 * strength
    linear 0.045 xoffset -3 * strength yoffset 2 * strength
    linear 0.045 xoffset 3 * strength yoffset -2 * strength
    linear 0.04 xoffset -4 * strength yoffset 3 * strength
    linear 0.04 xoffset 4 * strength yoffset -3 * strength
    linear 0.04 xoffset -5 * strength yoffset 3 * strength
    linear 0.04 xoffset 5 * strength yoffset -4 * strength
    linear 0.035 xoffset -7 * strength yoffset 4 * strength
    linear 0.035 xoffset 7 * strength yoffset -5 * strength
    linear 0.03 xoffset -8 * strength yoffset 5 * strength
    linear 0.03 xoffset 8 * strength yoffset -6 * strength
    # implosion suck-in: snap still
    easeout 0.16 xoffset 0 yoffset 0
    # DETONATION slam + decaying aftershock
    linear 0.02 xoffset -24 * strength yoffset 15 * strength
    linear 0.02 xoffset 21 * strength yoffset -17 * strength
    linear 0.025 xoffset -19 * strength yoffset 12 * strength
    linear 0.025 xoffset 16 * strength yoffset -10 * strength
    linear 0.03 xoffset -12 * strength yoffset 8 * strength
    linear 0.03 xoffset 10 * strength yoffset -6 * strength
    linear 0.04 xoffset -7 * strength yoffset 4 * strength
    linear 0.04 xoffset 5 * strength yoffset -3 * strength
    linear 0.05 xoffset -3 * strength yoffset 2 * strength
    easeout 0.30 xoffset 0 yoffset 0

transform msbf_final_victory_white_pressure:
    alpha 0.0
    pause 1.46
    linear 0.06 alpha 0.28
    linear 0.16 alpha 0.0
    pause 0.42
    linear 0.05 alpha 0.38
    linear 0.14 alpha 0.0
    pause 0.34
    linear 0.05 alpha 0.52
    linear 0.22 alpha 0.0

transform msbf_phase3_bg_rupture:
    subpixel True
    zoom 1.045
    xalign 0.50
    yalign 0.50
    rotate 0.0
    xoffset 0
    yoffset 0
    parallel:
        block:
            pause 0.92
            linear 0.025 xoffset -8 yoffset 3 rotate -0.06
            linear 0.035 xoffset 6 yoffset -2 rotate 0.05
            easeout 0.09 xoffset 0 yoffset 0 rotate 0.0
            pause 1.25
            linear 0.020 xoffset 5 yoffset 4 rotate 0.04
            linear 0.030 xoffset -4 yoffset -3 rotate -0.04
            easeout 0.08 xoffset 0 yoffset 0 rotate 0.0
            repeat
    parallel:
        block:
            pause 1.80
            linear 0.035 zoom 1.060
            linear 0.075 zoom 1.045
            pause 1.40
            linear 0.025 zoom 1.055
            linear 0.060 zoom 1.045
            repeat

transform msbf_phase3_bg_echo(delay=0.0, alpha_max=0.28, direction=1.0):
    subpixel True
    alpha 0.0
    zoom 1.060
    xoffset -18 * direction
    yoffset 0
    rotate -0.08 * direction
    pause delay
    block:
        linear 0.030 alpha alpha_max xoffset 20 * direction
        linear 0.055 alpha 0.0 xoffset -12 * direction yoffset -5
        pause 0.52
        linear 0.022 alpha alpha_max * 0.75 xoffset 16 * direction
        linear 0.045 alpha 0.0 xoffset -20 * direction yoffset 4
        pause 1.35
        repeat

transform msbf_phase3_fault_line(angle=0.0, delay=0.0, alpha_max=0.62, direction=1.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 640 - (980 * direction)
    ypos 360
    rotate angle
    alpha 0.0
    zoom 0.92
    pause delay
    block:
        xpos 640 - (980 * direction)
        alpha 0.0
        linear 0.035 alpha alpha_max zoom 1.0
        linear 0.22 xpos 640 + (980 * direction) alpha 0.0 zoom 1.28
        pause 0.38
        repeat

transform msbf_phase3_tornado_debris(cx=640, cy=360, rx=480, ry=150, delay=0.0, alpha_max=0.48, direction=1.0, scale=1.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos cx + (rx * direction)
    ypos cy + (ry * 0.24)
    rotate -30.0 * direction
    alpha 0.0
    zoom scale
    pause delay
    block:
        xpos cx + (rx * direction)
        ypos cy + (ry * 0.24)
        rotate -30.0 * direction
        alpha 0.0
        zoom scale
        linear 0.040 alpha alpha_max
        linear 0.150 xpos cx + (rx * 0.28 * direction) ypos cy - ry rotate 82.0 * direction zoom scale * 1.08
        linear 0.180 xpos cx - (rx * 0.76 * direction) ypos cy - (ry * 0.36) rotate 174.0 * direction zoom scale * 1.16
        linear 0.160 xpos cx - (rx * 0.44 * direction) ypos cy + (ry * 0.78) rotate 266.0 * direction zoom scale * 1.05
        linear 0.150 xpos cx + (rx * 0.58 * direction) ypos cy + (ry * 0.34) rotate 348.0 * direction alpha alpha_max * 0.72
        linear 0.070 xpos cx + (rx * 1.05 * direction) ypos cy - (ry * 0.10) rotate 424.0 * direction alpha 0.0
        pause 0.12
        repeat

transform msbf_phase3_tornado_streak(cx=640, cy=360, rx=500, ry=170, delay=0.0, alpha_max=0.28, direction=1.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos cx - (rx * 0.92 * direction)
    ypos cy + (ry * 0.46)
    rotate -18.0 * direction
    alpha 0.0
    xzoom 0.35
    pause delay
    block:
        xpos cx - (rx * 0.92 * direction)
        ypos cy + (ry * 0.46)
        rotate -18.0 * direction
        xzoom 0.35
        alpha 0.0
        linear 0.060 alpha alpha_max xzoom 0.85
        linear 0.260 xpos cx + (rx * 0.80 * direction) ypos cy - (ry * 0.32) rotate 22.0 * direction xzoom 1.18 alpha 0.0
        pause 0.42
        repeat

transform msbf_phase3_static_slice(delay=0.0, alpha_max=0.34, direction=1.0):
    subpixel True
    alpha 0.0
    xoffset -42 * direction
    pause delay
    block:
        xoffset -42 * direction
        linear 0.035 alpha alpha_max xoffset 22 * direction
        linear 0.055 alpha 0.0 xoffset -18 * direction
        pause 0.22
        linear 0.025 alpha alpha_max * 0.70 xoffset 36 * direction
        linear 0.040 alpha 0.0 xoffset 0
        pause 0.64
        repeat

transform msbf_phase3_pressure(delay=0.0, peak=0.32):
    subpixel True
    alpha 0.0
    zoom 1.0
    pause delay
    block:
        linear 0.035 alpha peak zoom 1.025
        linear 0.080 alpha 0.0 zoom 1.075
        pause 0.30
        linear 0.025 alpha peak * 0.74 zoom 1.040
        linear 0.070 alpha 0.0 zoom 1.090
        pause 1.10
        repeat

transform msbf_boss_backlight:
    subpixel True
    alpha 0.08
    zoom 1.0
    rotate 0.0
    parallel:
        ease 0.9 alpha 0.28 zoom 1.08
        ease 1.1 alpha 0.08 zoom 1.0
        repeat
    parallel:
        linear 2.0 rotate 2.0
        linear 2.0 rotate -2.0
        repeat


transform msbf_boss_intro:
    subpixel True
    alpha 0.0
    xoffset 0
    yoffset 150
    zoom 1.0
    rotate 0.0
    # loom up out of the dark, growing as he advances...
    parallel:
        easeout 1.05 alpha 1.0
    parallel:
        easeout 1.25 yoffset 0
    parallel:
        easeout 1.25 zoom 1.14
    # ...land hard, then settle into a slow ominous breath.
    block:
        easeout 0.10 yoffset 12 zoom 1.16
        easein 0.34 yoffset 0 zoom 1.14
    block:
        easein 1.5 yoffset -7
        easeout 1.5 yoffset 0
        repeat

transform msbf_boss_intro_ghost(delay=0.0, ydrift=80):
    subpixel True
    alpha 0.0
    yoffset ydrift + 60
    zoom 1.22
    pause delay
    parallel:
        linear 0.12 alpha 0.28
        linear 0.7 alpha 0.0
    parallel:
        easeout 0.9 yoffset 0
    parallel:
        easeout 0.9 zoom 1.14
















transform msbf_press_turn_pulse(delay=0.0):
    alpha 0.58
    pause delay
    block:
        ease 0.45 alpha 0.92
        ease 0.55 alpha 0.42
        repeat

transform msbf_press_turn_shimmer(delay=0.0, travel=32):
    subpixel True
    alpha 0.0
    xoffset 0
    pause delay
    block:
        xoffset 0
        linear 0.12 alpha 0.0
        linear 0.18 alpha 0.62 xoffset travel * 0.45
        linear 0.22 alpha 0.0 xoffset travel
        pause 0.86
        repeat

transform msbf_press_turn_edge(delay=0.0):
    alpha 0.32
    pause delay
    block:
        ease 0.36 alpha 0.82
        ease 0.64 alpha 0.28
        pause 0.18
        repeat

transform msbf_press_turn_spend_fx(delay=0.0):
    subpixel True
    alpha 0.92
    xoffset 0
    yoffset 0
    pause delay
    parallel:
        linear 0.08 alpha 1.0
        linear 0.34 alpha 0.0
    parallel:
        easeout 0.42 xoffset 7 yoffset -12

transform msbf_press_turn_convert_fx(delay=0.0):
    subpixel True
    alpha 0.88
    xoffset 0
    pause delay
    linear 0.06 alpha 1.0 xoffset -2
    linear 0.26 alpha 0.0 xoffset -14

transform msbf_press_turn_gain_fx(delay=0.0):
    subpixel True
    alpha 0.0
    yoffset 10
    pause delay
    linear 0.12 alpha 0.92 yoffset 0
    linear 0.30 alpha 0.0 yoffset -9

transform msbf_button_focus:
    on hover:
        linear 0.08 xoffset 2
    on idle:
        linear 0.08 xoffset 0

transform msbf_panel_enter(delay=0.0):
    alpha 0.0
    yoffset 16
    pause delay
    easeout_quad 0.25 alpha 1.0 yoffset 0

transform msbf_fx_flash(color="#ffffff", max_alpha=0.22):
    alpha max_alpha
    linear 0.35 alpha 0.0

transform msbf_fx_text:
    alpha 0.0
    yoffset 16
    zoom 0.98
    parallel:
        linear 0.10 alpha 1.0
        pause 0.36
        linear 0.22 alpha 0.0
    parallel:
        easeout 0.68 yoffset -16 zoom 1.03

transform msbf_fx_text_big:
    alpha 0.0
    yoffset 28
    zoom 0.92
    parallel:
        linear 0.08 alpha 1.0
        pause 0.38
        linear 0.22 alpha 0.0
    parallel:
        easeout 0.68 yoffset -24 zoom 1.12

transform msbf_fx_slash(angle=0.0, delay=0.0):
    rotate angle
    alpha 0.0
    zoom 0.7
    pause delay
    linear 0.06 alpha 0.88 zoom 1.0
    linear 0.20 alpha 0.0 zoom 1.25

# -----------------------------------------------------------------------------
# Howling wind (phase 1). A gust streak: a thin band that sweeps across from
# x0->x1 with a smooth ease, fades in then trails off, waits `gap`, and repeats.
# Used many times at varied y / delay / dur / gap so the gusts overlap unevenly
# and read as turbulent wind rather than a metronome. The same transform drives
# the soft, slow "moving air" haze sheets (just fed a tall, low-alpha Solid).
transform msbf_wind_streak(y=0, delay=0.0, alpha_max=0.16, dur=1.2, x0=-360, x1=1360, gap=0.0):
    subpixel True
    ypos y
    block:
        xpos x0
        alpha 0.0
        pause delay
        parallel:
            ease dur xpos x1
        parallel:
            linear dur * 0.20 alpha alpha_max
            linear dur * 0.46 alpha alpha_max
            linear dur * 0.34 alpha 0.0
        pause gap
        repeat

# ---- Phase-1 boss entrance cinematic (msbf_battle_intro_overlay) -------------
# Dark wash that holds while the boss looms in, then lifts as he sets.
transform msbf_intro_dim(peak=0.5):
    alpha peak
    pause 1.55
    linear 0.95 alpha 0.0

# Letterbox bars: slide in, hold through the reveal, then lift away.
transform msbf_intro_letterbox_top(h=88):
    ypos 0
    yanchor 0.0
    yoffset -h
    ease 0.5 yoffset 0
    pause 1.95
    ease 0.55 yoffset -h

transform msbf_intro_letterbox_bottom(h=88):
    ypos 720
    yanchor 1.0
    yoffset h
    ease 0.5 yoffset 0
    pause 1.95
    ease 0.55 yoffset h

# The name card slams in big, overshoots slightly, settles, then fades.
transform msbf_intro_title(delay=1.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom 1.5
    pause delay
    parallel:
        easeout 0.32 zoom 0.96
        easein 0.12 zoom 1.0
    parallel:
        linear 0.12 alpha 1.0
        pause 1.2
        linear 0.5 alpha 0.0

# Kicker / tagline: rise + fade in, hold `life`, fade out.
transform msbf_intro_caption(delay=0.0, rise=18, life=1.4):
    subpixel True
    alpha 0.0
    yoffset rise
    pause delay
    parallel:
        ease 0.6 yoffset 0
    parallel:
        ease 0.4 alpha 1.0
        pause life
        linear 0.45 alpha 0.0

# Detonation flash the instant he lands.
transform msbf_intro_flash(delay=1.7, peak=0.8):
    alpha 0.0
    pause delay
    linear 0.05 alpha peak
    linear 0.42 alpha 0.0

# Per-phase animated battle background (the bg art + drifting overlays/scanlines).
# `phase` swaps which ambient FX set is layered in. `wind` adds the phase-1
# howling-wind layer -- it is opt-in (only the live phase-1 battle passes it) so
# it does NOT bleed into phase 2, Id Mode, or the party-select screen, all of
# which also draw this backdrop.
screen msbf_battle_backdrop(dim="#02050ab8", phase=1, wind=False):
    if phase == 3:
        if MSBF_FX_SHADERS:
            add "msbf_rupture_backdrop" at msbf_fx_glitch_pulse(0.1, 0.55, 32.0), msbf_phase3_bg_rupture
        else:
            add "msbf_rupture_backdrop" at msbf_phase3_bg_rupture
        add "msbf_rupture_backdrop" at msbf_phase3_bg_echo(0.16, 0.18, 1.0)
    elif phase >= 2:
        add "bg battle_setpiece" at msbf_phase2_bg_dizzy
        add "bg battle_setpiece" at msbf_phase2_bg_veil(0.0, 0.18, 1.0)
    else:
        add "bg battle_setpiece" at msbf_bg_drift
    add Solid(dim)
    # Procedural per-phase atmosphere -- ONE GPU draw replacing the old
    # crossbeam / scanline / fault / tornado / static-slice Solid swarm.
    use msbf_atmos_field(phase, "screen")
    # Howling wind: drifting "moving air" haze, gust streaks ripping across at
    # staggered cadences, and a field of wind-borne motes. Phase-1 battle only
    # (opt-in via `wind`), so it never shows in phase 2 / Id Mode / party select.
    if wind:
        add Solid("#3a5f86") xysize (760, 220) at msbf_wind_streak(96, 0.0, 0.06, 4.4, -820, 2120, 0.0)
        add Solid("#22405e") xysize (640, 250) at msbf_wind_streak(404, 1.9, 0.05, 5.0, -820, 2120, 0.0)
        add Solid("#cfe9ff") xysize (560, 2) at msbf_wind_streak(92, 0.0, 0.16, 1.5, -440, 1440, 0.7)
        add Solid("#9fd2ff") xysize (430, 2) at msbf_wind_streak(226, 0.6, 0.13, 1.2, -440, 1440, 1.1)
        add Solid("#ffffff") xysize (660, 1) at msbf_wind_streak(348, 0.25, 0.11, 1.0, -460, 1460, 0.9)
        add Solid("#bfe3ff") xysize (500, 2) at msbf_wind_streak(486, 1.0, 0.14, 1.6, -440, 1440, 0.6)
        add Solid("#dff2ff") xysize (380, 1) at msbf_wind_streak(604, 0.4, 0.10, 1.3, -440, 1440, 1.4)
        add Solid("#9fd2ff") xysize (320, 1) at msbf_wind_streak(540, 1.5, 0.10, 0.9, -420, 1420, 1.7)
        if msbf_fx_particles_on():
            add "msbf_fx_field_wind"

screen msbf_phase2_boom_overlay(kind=0):
    $ _boom_kind = kind % 3
    $ _pressure_color = ["#000000", "#17030a", "#02131d"][_boom_kind]
    $ _accent_a = ["#ff3868", "#ffcf66", "#55ddff"][_boom_kind]
    $ _accent_b = ["#55ddff", "#ff3868", "#ffcf66"][_boom_kind]

    add Solid(_pressure_color) at msbf_phase2_boom_pressure(0.48)
    add Solid("#000000") xysize (1280, 34) at msbf_phase2_boom_scan(0.00, 0.30, 1.0):
        ypos 82
    add Solid("#000000") xysize (1280, 42) at msbf_phase2_boom_scan(0.06, 0.26, -1.0):
        ypos 608
    add Solid(_accent_a) xysize (1280, 5) at msbf_phase2_boom_wave(-9.0, 0.02, 0.38):
        xcenter 640
        ycenter 338
    add Solid(_accent_b) xysize (1280, 4) at msbf_phase2_boom_wave(13.0, 0.07, 0.32):
        xcenter 640
        ycenter 380
    add Solid("#000000") xysize (360, 900) at msbf_phase2_boom_slab(-18.0, 0.04, 0.34, 1.0):
        xcenter 640
        ycenter 360
    add Solid(_accent_a) xysize (180, 900) at msbf_phase2_boom_slab(27.0, 0.10, 0.24, -1.0):
        xcenter 640
        ycenter 360
    add Solid(_accent_b) xysize (1040, 3) at msbf_phase2_boom_wave(-34.0, 0.15, 0.26):
        xcenter 640
        ycenter 360

screen msbf_phase3_rupture_overlay(kind=0):
    $ _rupture_kind = kind % 3
    $ _accent_a = ["#ff3868", "#ffffff", "#a66bff"][_rupture_kind]
    $ _accent_b = ["#f5fbff", "#ff3868", "#ff6b9f"][_rupture_kind]

    add Solid("#050007") at msbf_phase3_pressure(0.0, 0.42)
    add Solid(_accent_a) xysize (1280, 5) at msbf_phase3_fault_line(-29.0, 0.00, 0.70, 1.0):
        xcenter 640
        ycenter 274
    add Solid(_accent_b) xysize (1280, 4) at msbf_phase3_fault_line(17.0, 0.06, 0.58, -1.0):
        xcenter 640
        ycenter 398
    add Solid(_accent_b) xysize (760, 5) at msbf_phase3_tornado_streak(640, 360, 620, 178, 0.02, 0.46, 1.0)
    add Solid(_accent_a) xysize (640, 5) at msbf_phase3_tornado_streak(640, 382, 540, 206, 0.10, 0.38, -1.0)
    add Solid("#000000ee") xysize (58, 12) at msbf_phase3_tornado_debris(640, 360, 640, 210, 0.00, 0.72, 1.0, 1.28)
    add Solid(_accent_a) xysize (42, 10) at msbf_phase3_tornado_debris(640, 344, 540, 156, 0.08, 0.70, -1.0, 1.12)
    add Solid("#ffffffcc") xysize (28, 8) at msbf_phase3_tornado_debris(640, 392, 600, 236, 0.16, 0.64, 1.0, 0.96)
    add Solid("#ffffff66") xysize (1280, 2) at msbf_phase3_static_slice(0.02, 0.48, 1.0):
        ypos 98
    add Solid("#ff386866") xysize (1280, 5) at msbf_phase3_static_slice(0.11, 0.44, -1.0):
        ypos 612

# --- Extra "breathing + flair" transforms for breaks / reveals / death. ---
# A charge core that swells and throbs while the screen is black -- turns the
# dead hold before a reveal into a visible build-up of pressure.
transform msbf_phase_charge(delay=0.0, peak=0.5):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom 0.18
    rotate 45
    pause delay
    parallel:
        easein 2.0 alpha peak zoom 1.0
    parallel:
        block:
            ease 0.16 alpha peak
            ease 0.16 alpha peak * 0.45
            repeat

# Rings collapsing inward -- "energy gathering" for the charge beat.
transform msbf_phase_charge_ring(delay=0.0, spin=1.0, alpha_max=0.5):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    block:
        alpha 0.0
        zoom 1.75
        rotate 0.0
        pause delay
        linear 0.10 alpha alpha_max
        linear 0.66 zoom 0.16 alpha 0.0 rotate 70.0 * spin
        pause 0.16
        repeat

# A single hard shockwave ring punching outward (reveals + killing blow).
transform msbf_big_shock(delay=0.0, alpha_max=0.85):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom 0.16
    pause delay
    linear 0.05 alpha alpha_max
    linear 0.44 zoom 1.95 alpha 0.0

# Sustained low rumble that any displayable can ride during a transition.
transform msbf_transition_quake(strength=1.0, delay=0.0):
    subpixel True
    pause delay
    block:
        linear 0.028 xoffset -6 * strength yoffset 4 * strength
        linear 0.028 xoffset 7 * strength yoffset -3 * strength
        linear 0.032 xoffset -4 * strength yoffset -4 * strength
        linear 0.028 xoffset 5 * strength yoffset 3 * strength
        linear 0.030 xoffset -2 * strength yoffset 2 * strength
        repeat

screen msbf_phase_transition_overlay(battle):
    $ _phase_transition_title = getattr(battle, "phase_transition_title", "THE STAGE BEGINS ANEW")
    $ _phase_transition_subtitle = getattr(battle, "phase_transition_subtitle", "A WINGED ANGEL REWRITES THE SCRIPT")

    if battle.final_victory_active:
        # HYPERNOVA. Centred on the boss: the arena stays visible while she
        # implodes (msbf_boss_collapse), rings collapse inward + a core gathers,
        # then it DETONATES at ~0.85s and the whiteout blooms outward from the
        # blast. The boom sfx is timed to the detonation.
        #
        # The centre is READ from her staging, not stated. It used to be the
        # literal (845, 290) -- the boss's position back when she lived inside a
        # 786px stage box at x452 -- and moving her to the middle of a full-bleed
        # arena left the entire explosion happening off to her right.
        $ _nx, _ny = msbf_boss_anchor(battle.phase)
        timer MSBF_FINAL_VICTORY_EXPLODE_DELAY action Function(battle.play_final_victory_explosion)
        # gathering darkness so the imploding light reads (kept light, lifts at blast)
        add Solid("#03060c") at msbf_nova_predark
        # inward-collapsing rings -- the star eating itself
        if MSBF_FX_SHADERS:
            add Solid("#00000000") xysize (1500, 1500) at msbf_nova_inring_r(0.00, (1.0, 1.0, 1.0), 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (1500, 1500) at msbf_nova_inring_r(0.12, (1.0, 0.22, 0.41), 0.6):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (1500, 1500) at msbf_nova_inring_r(0.24, (0.65, 0.42, 1.0), 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (1500, 1500) at msbf_nova_inring_r(0.38, (0.33, 0.87, 1.0), 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (1500, 1500) at msbf_nova_inring_r(0.52, (1.0, 0.81, 0.40), 0.55):
                xcenter _nx
                ycenter _ny
        else:
            add Solid("#ffffff") xysize (1400, 4) at msbf_nova_inring(0.00, 1.0, 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#ff3868") xysize (1400, 5) at msbf_nova_inring(0.12, -1.0, 0.6):
                xcenter _nx
                ycenter _ny
            add Solid("#a66bff") xysize (1400, 4) at msbf_nova_inring(0.24, 1.0, 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#55ddff") xysize (1400, 3) at msbf_nova_inring(0.38, -1.0, 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#ffcf66") xysize (1400, 4) at msbf_nova_inring(0.52, 1.0, 0.55):
                xcenter _nx
                ycenter _ny
        # gathering core
        if MSBF_FX_SHADERS:
            add Solid("#00000000") xysize (520, 520) at msbf_nova_core_glow(0.04, (1.0, 1.0, 1.0)):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (300, 300) at msbf_nova_core_glow(0.09, (1.0, 0.90, 0.75)):
                xcenter _nx
                ycenter _ny
        else:
            add Solid("#ffffff") xysize (520, 520) at msbf_nova_core(0.04):
                xcenter _nx
                ycenter _ny
            add Solid("#ffe6c0") xysize (300, 300) at msbf_nova_core(0.09):
                xcenter _nx
                ycenter _ny
        # DETONATION flash
        add Solid("#ffffff") at msbf_nova_flash(0.84, 1.0)
        add Solid("#fff4dc") at msbf_nova_flash(0.90, 0.7)
        add Solid("#ff3868") at msbf_nova_flash(0.86, 0.45)
        # outward shockwaves
        if MSBF_FX_SHADERS:
            add Solid("#00000000") xysize (2000, 2000) at msbf_big_shock_r(0.84, (1.0, 1.0, 1.0), 0.95):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (2000, 2000) at msbf_big_shock_r(0.92, (1.0, 0.22, 0.41), 0.72):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (2000, 2000) at msbf_big_shock_r(1.05, (1.0, 0.81, 0.40), 0.5):
                xcenter _nx
                ycenter _ny
        else:
            add Solid("#ffffff") xysize (1500, 1500) at msbf_big_shock(0.84, 0.95):
                xcenter _nx
                ycenter _ny
            add Solid("#ff3868") xysize (1500, 1500) at msbf_big_shock(0.92, 0.72):
                xcenter _nx
                ycenter _ny
            add Solid("#ffcf66") xysize (1500, 1500) at msbf_big_shock(1.05, 0.5):
                xcenter _nx
                ycenter _ny
        # blast jets firing out of the detonation
        add Solid("#ffffff") xysize (1500, 13) at msbf_phase_break_lance(-7.0, 0.85, 1.0):
            xcenter _nx
            ycenter _ny
        add Solid("#ff3868") xysize (1400, 10) at msbf_phase_break_lance(20.0, 0.88, 0.82):
            xcenter _nx
            ycenter _ny
        add Solid("#a66bff") xysize (1320, 7) at msbf_phase_transition_lance(-30.0, 0.95, 0.7):
            xcenter _nx
            ycenter _ny
        # whiteout blooms out from the detonation point and fills the screen
        add Solid("#ffffff") xysize (1600, 1600) at msbf_nova_whiteout(0.86):
            xcenter _nx
            ycenter _ny
        add Solid("#ffffff") at msbf_final_victory_white_pressure
    elif battle.defeat_sequence_active:
        # PARTY WIPE. Not a flat fade: the final blow concusses, colour drains
        # into a dark-red wash, the boss looms over a heartbeat pulse, the
        # verdict trembles in, then darkness letterboxes shut and crushes black.
        $ _dnx, _dny = msbf_boss_anchor(battle.phase)
        add Solid("#7a0a18") at msbf_defeat_flash
        if MSBF_FX_SHADERS:
            add Solid("#00000000") xysize (1280, 720) at msbf_defeat_postfx((0.17, 0.015, 0.04))
            add Solid("#00000000") xysize (920, 780) at msbf_defeat_loom_glow((0.82, 0.10, 0.20)):
                xcenter _dnx
                ycenter _dny
        add Solid("#12000a") at msbf_defeat_pulse
        add Solid("#000000") xysize (1280, 460) at msbf_defeat_letterbox_top(1.75):
            ypos 0
            yanchor 0.0
        add Solid("#000000") xysize (1280, 460) at msbf_defeat_letterbox_bottom(1.75):
            ypos 720
            yanchor 1.0
        add Solid("#000000") at msbf_defeat_blackout
    elif getattr(battle, "defeat_blackout", False):
        add Solid("#000000")
    elif getattr(battle, "final_victory_whiteout", False):
        add Solid("#ffffff")
    elif battle.phase_transition_active:
        # The bar break and the arrival that follows it both live in
        # cinematics.rpy now. They used to be ~70 `add Solid(...)` lines right
        # here -- rotated bars standing in for light, squares standing in for
        # flashes -- and reading which beat happened when meant tracing four
        # different delay arguments through a list of rectangles.
        if battle.fx_event == "phase_blackout":
            use msbf_phase_break_seq(battle)
        elif battle.fx_event == "phase":
            use msbf_phase_reveal_seq(battle)
        elif not battle.phase2_reveal_started:
            add Solid("#000000")

# -----------------------------------------------------------------------------
# enter_m_input_lock: shared "hands off the wheel" key-eater for the game modes.
# Put `use enter_m_input_lock()` as the FIRST line inside any gameplay screen.
#
# HOW IT STAYS OUT OF THE WAY: Matsu'Py dispatches key events to a screen's
# children in REVERSE source order, so eaters inserted FIRST sit at the LOWEST
# priority. Any explicit `key` the mode binds later (movement, confirm, its own
# Escape/pause) still wins; only the leftover default binds that would otherwise
# fall through to config.underlay get swallowed here.
#
# WHAT IT KILLS (and only this): rollback / roll-forward (mouse wheel + PageUp),
# skip (Ctrl / Tab / >), the accessibility menu (A -- collides with "left"),
# self-voicing (V), hide-windows (H / middle-click), screenshot (S -- collides
# with "down"), help (F1) and the progress screen (F2). Verified against the
# 8.1.1 default keymap (00keymap.rpy).
#
# WHAT IT LEAVES ALONE (on purpose): dismiss/activate + arrow focus, because
# Monika's date drives its buttons with them; `game_menu` (each mode routes
# Escape to its own pause / disables the menu via _game_menu_screen); and
# fullscreen. Text `input` widgets (the phase-3 typing microgame) out-priority
# these eaters too, so typing 's'/'a'/'v'/'h' still types rather than triggers.
# -----------------------------------------------------------------------------
screen enter_m_input_lock():
    # F3 -- the frame profiler (perf.rpy). Bound HERE because this screen is the
    # one thing every fight in this folder already uses, so the profiler follows
    # the modes around without any of them knowing about it. It is deliberately
    # NOT in the kill-list below: this is the one default-adjacent key a fight
    # is meant to keep.
    key "K_F3" action Function(msbf_perf_toggle)

    key "rollback" action NullAction()
    key "rollforward" action NullAction()
    key "skip" action NullAction()
    key "toggle_skip" action NullAction()
    key "fast_skip" action NullAction()
    key "hide_windows" action NullAction()
    key "self_voicing" action NullAction()
    key "screenshot" action NullAction()
    key "accessibility" action NullAction()
    key "help" action NullAction()
    key "progress_screen" action NullAction()


# -----------------------------------------------------------------------------
# msbf_nav_keys: THE fight's keyboard scheme, in one place.
# Arrows + WASD move, Z / Enter / Numpad-Enter confirm, X / Shift go back --
# and each binding plays its pooled UI cue. Party select, the battle command
# menu and the quiz overlay each used to hand-bind the same thirteen keys, so
# adding a binding (or a gamepad) meant three edits that could silently drift.
init python:

    def msbf_kb_step(name, delta, count):
        """Move a screen cursor RELATIVE to its LIVE value.

        SetScreenVariable is handed a value computed the last time the screen
        EXECUTED. Hold an arrow down and the key repeats faster than the screen
        re-executes, so every repeat inside that window recomputes from the
        same stale index and writes the same destination: the cursor stalls,
        then jumps several places at once when the screen finally catches up.
        That is the "holding a key desyncs the selection" bug.

        Reading renpy.current_screen().scope here is the same place
        SetScreenVariable writes to, so each repeat steps exactly one place no
        matter how far behind the redraw is.
        """
        cs = renpy.current_screen()
        if cs is None or not count:
            return
        try:
            cur = int(cs.scope.get(name, 0) or 0)
        except (TypeError, ValueError):
            cur = 0
        cs.scope[name] = (cur + delta) % count
        # Moving with the keyboard takes ownership of the highlight away from
        # the mouse -- see the kb_active note in msbf_battle_screen.
        cs.scope["kb_active"] = True
        renpy.restart_interaction()


# Pass None for a direction the screen doesn't use; it simply isn't bound.
#
# IT ALSO EATS REN'PY'S OWN ARROW FOCUS, and it has to.
#   The 8.1.1 default keymap binds focus_left/right/up/down to the very same
#   arrow keys (00keymap.rpy:73-76). enter_m_input_lock deliberately leaves
#   those alone -- Monika's date mode drives its buttons with them -- so any
#   screen that ALSO runs its own cursor on the arrows was running two cursors
#   at once: mine (kb_index) and Matsu'Py's internal button focus, which paints
#   hover_background. Two highlighted boxes, and because Matsu'Py's focus order is
#   geometric and mine is grid arithmetic, holding a key walked them apart.
#
#   Using this screen IS the declaration that the screen owns the arrows, so
#   killing the built-in focus movement belongs here rather than in the shared
#   lock. `dismiss`/activate are untouched -- Enter and clicks still work.
# -----------------------------------------------------------------------------
screen msbf_nav_keys(up=None, down=None, left=None, right=None, confirm=None, back=None):
    key "focus_left" action NullAction()
    key "focus_right" action NullAction()
    key "focus_up" action NullAction()
    key "focus_down" action NullAction()

    if up is not None:
        key "K_UP" action [MSBF_NAV_SFX["move"], up]
        key "K_w" action [MSBF_NAV_SFX["move"], up]
    if down is not None:
        key "K_DOWN" action [MSBF_NAV_SFX["move"], down]
        key "K_s" action [MSBF_NAV_SFX["move"], down]
    if left is not None:
        key "K_LEFT" action [MSBF_NAV_SFX["move"], left]
        key "K_a" action [MSBF_NAV_SFX["move"], left]
    if right is not None:
        key "K_RIGHT" action [MSBF_NAV_SFX["move"], right]
        key "K_d" action [MSBF_NAV_SFX["move"], right]
    if confirm is not None:
        key "K_z" action [MSBF_NAV_SFX["ok"], confirm]
        key "K_RETURN" action [MSBF_NAV_SFX["ok"], confirm]
        key "K_KP_ENTER" action [MSBF_NAV_SFX["ok"], confirm]
    if back is not None:
        key "K_x" action [MSBF_NAV_SFX["no"], back]
        key "K_LSHIFT" action [MSBF_NAV_SFX["no"], back]

# =============================================================================
# --- 3. SCREENS -------------------------------------------------------------
# =============================================================================
# msbf_fx_layer: the hit-flash + floating-number layer. It polls the battle's
# fx feeds -- fx_event/fx_serial (a one-shot cue like "weak"/"crit"/"phase") and
# float_events (the damage/heal numbers emitted by emit_float in battle_logic) --
# and animates them. Serial numbers let it detect "a new event happened".
screen msbf_fx_layer(battle):
    if battle.fx_event and battle.fx_event not in ("phase_blackout", "phase", "final_victory", "final_defeat"):
        timer battle.fx_clear_delay action Function(battle.clear_fx)

        # EVERY POSITION IN HERE IS DERIVED, not typed. This layer was still
        # firing at (875, 258) / (850, 240) / xalign 0.70 -- the boss's centre
        # and the party deck's corner from back when the fight was three panels
        # and the stage box started at x452. On the full-bleed arena that puts
        # the whole impact package, AFFINITY SHIFT included, a couple of hundred
        # pixels to the right of whatever it is supposed to be hitting.
        $ _fxb_x, _fxb_y = msbf_boss_anchor(battle.phase)
        # Where the party lives: the centre of the tag row, which is the one
        # place on screen that means "the party" regardless of party size.
        $ _fxp_n = len(battle.party)
        $ _fxp_x = 640
        $ _fxp_y = msbf_stage_anchor(0, _fxp_n)[1] + 30
        # Call-outs sit just off her centre so they never cover her face.
        $ _fxt_x = _fxb_x + 210
        $ _fxt_y = _fxb_y - 130

        # Tint the impact bloom by the element the party just cast (player hits
        # only -- enemy strikes use the enemy_* events below).
        if battle.fx_event in ("hit", "weak", "crit") and getattr(battle, "last_cast_element", None):
            $ _imp_rgb = msbf_hex_rgb(msbf_element_color(battle.last_cast_element))
            use msbf_glow_pop(_fxb_x, _fxb_y, 300, 300, _imp_rgb, 0.7, 1.7, 0.45)

        if battle.fx_event in ("weak", "enemy_weak"):
            add Solid("#ffcf6640") at msbf_fx_flash("#ffcf66", 0.24)
            use msbf_glow_pop(_fxb_x, _fxb_y, 380, 380, (1.0, 0.81, 0.40), 0.85, 1.5, 0.5)
            add Solid("#ffcf66") xysize (440, 16) at msbf_fx_slash(-12.0, 0.02):
                xcenter _fxb_x
                ycenter _fxb_y
            text "WEAK" style "msbf_fx_weak" at msbf_fx_text:
                xcenter _fxt_x
                ycenter _fxt_y
        elif battle.fx_event in ("crit", "enemy_crit"):
            add Solid("#ffffff4c") at msbf_fx_flash("#ffffff", 0.28)
            use msbf_glow_pop(_fxb_x, _fxb_y, 480, 480, (1.0, 0.96, 0.88), 1.0, 1.3, 0.55)
            use msbf_shock_ring(_fxb_x, _fxb_y, 560, (1.0, 0.30, 0.45), 0.12, 1.15, 0.55)
            add Solid("#ffffff") xysize (520, 18) at msbf_fx_slash(-18.0, 0.0):
                xcenter _fxb_x
                ycenter _fxb_y - 12
            add Solid("#ff3868") xysize (420, 12) at msbf_fx_slash(12.0, 0.05):
                xcenter _fxb_x
                ycenter _fxb_y + 48
            text "CRITICAL" style "msbf_fx_crit" at msbf_fx_text_big:
                xcenter _fxt_x
                ycenter _fxt_y
        elif battle.fx_event == "miss":
            add Solid("#54637844") at msbf_fx_flash("#546378", 0.20)
            text "MISS" style "msbf_fx_resist" at msbf_fx_text:
                xcenter _fxt_x
                ycenter _fxt_y
        elif battle.fx_event in ("resist", "enemy_resist"):
            add Solid("#54637844") at msbf_fx_flash("#546378", 0.20)
            text "RESIST" style "msbf_fx_resist" at msbf_fx_text:
                xcenter _fxt_x
                ycenter _fxt_y
        elif battle.fx_event in ("heal", "enemy_heal"):
            add Solid("#66e08a33") at msbf_fx_flash("#66e08a", 0.18)
            use msbf_glow_pop(_fxp_x, _fxp_y, 620, 260, (0.40, 0.88, 0.54), 0.7, 1.6, 0.5)
            text "RECOVER" style "msbf_fx_heal" at msbf_fx_text:
                xcenter _fxp_x
                ycenter _fxp_y - 96
        elif battle.fx_event == "revive":
            add Solid("#66e08a44") at msbf_fx_flash("#66e08a", 0.24)
            use msbf_glow_pop(_fxp_x, _fxp_y, 680, 300, (0.45, 1.0, 0.60), 0.9, 1.4, 0.6)
            text "REVIVE" style "msbf_fx_heal" at msbf_fx_text:
                xcenter _fxp_x
                ycenter _fxp_y - 96
        elif battle.fx_event == "shuffle":
            add Solid("#55ddff48") at msbf_fx_flash("#55ddff", 0.34)
            use msbf_glow_pop(_fxb_x, _fxb_y, 460, 420, (0.33, 0.87, 1.0), 0.9, 1.4, 0.55)
            use msbf_shock_ring(_fxb_x, _fxb_y, 520, (0.33, 0.87, 1.0), 0.10, 0.95, 0.55)
            use msbf_shock_ring(_fxb_x, _fxb_y, 700, (1.0, 0.81, 0.40), 0.08, 0.8, 0.62)
            add Solid("#55ddff") xysize (660, 8) at msbf_fx_slash(0.0, 0.03):
                xcenter _fxb_x
                ycenter _fxb_y - 60
            add Solid("#ffffffcc") xysize (1280, 3) at msbf_phase3_static_slice(0.00, 0.5, 1.0):
                ypos _fxb_y - 40
            add Solid("#ff3868aa") xysize (1280, 4) at msbf_phase3_static_slice(0.06, 0.5, -1.0):
                ypos _fxb_y + 16
            text "AFFINITY SHIFT" style "msbf_fx_scan" at msbf_fx_text_big:
                xcenter _fxb_x
                ycenter _fxb_y - 190
        elif battle.fx_event == "victory":
            add Solid("#55ddff4a") at msbf_fx_flash("#55ddff", 0.30)
            use msbf_shock_ring(640, 360, 1000, (0.33, 0.87, 1.0), 0.10, 1.2, 0.7)
            use msbf_glow_pop(_fxb_x, _fxb_y, 700, 600, (0.60, 0.95, 1.0), 0.9, 1.3, 0.7)
            add Solid("#55ddff") xysize (720, 14) at msbf_fx_slash(-4.0, 0.0):
                xcenter _fxb_x
                ycenter _fxb_y - 45
            text "CLEAR" style "msbf_fx_scan" at msbf_fx_text_big:
                xcenter _fxb_x
                ycenter _fxb_y - 190
        elif battle.fx_event == "defeat":
            add Solid("#1a0206") at msbf_fx_flash("#1a0206", 0.62)
            add Solid("#ff38684f") at msbf_fx_flash("#ff3868", 0.34)
            use msbf_shock_ring(640, 360, 1100, (0.75, 0.10, 0.22), 0.10, 1.0, 0.6)
            text "DOWN" style "msbf_fx_phase" at msbf_fx_text_big:
                xcenter _fxb_x
                ycenter _fxb_y - 190
        elif battle.fx_event in ("enemy", "enemy_hit", "enemy_aoe", "enemy_guard"):
            add Solid("#ff38682c") at msbf_fx_flash("#ff3868", 0.20)
            add Solid("#ff3868") xysize (440, 10) at msbf_fx_slash(10.0, 0.0):
                xcenter _fxb_x
                ycenter _fxb_y + 12
        elif battle.fx_event in ("hit", "guard", "buff", "debuff", "scan", "pass", "enemy_buff"):
            add Solid("#55ddff22") at msbf_fx_flash("#55ddff", 0.14)


# -----------------------------------------------------------------------------
# msbf_keyboard_notice: pre-fight input notice. Styled after Hina's World content
# notice: black matte, Win9x-style title bar, white body, gray button tray.
# -----------------------------------------------------------------------------
screen msbf_keyboard_notice():
    style_prefix "hw"
    modal True
    use enter_m_input_lock()
    add Solid("#000000")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 720
        padding (0, 0, 0, 0)
        background "#d4d0c8"

        vbox:
            spacing 0

            frame:
                xsize 720
                ysize 26
                padding (8, 4, 8, 4)
                background "#0a246a"
                text "Keyboard Notice":
                    color "#ffffff"
                    bold True
                    size 12
                    yalign 0.5

            frame:
                xsize 720
                padding (24, 22, 24, 18)
                background "#ffffff"
                vbox:
                    spacing 14
                    text "This mode is best played with a keyboard.":
                        color "#000000"
                        bold True
                        size 15
                        xsize 672
                    text "Mouse input works for menus, but certain elements expect direct keyboard input.":
                        color "#000000"
                        size 15
                        xsize 672
                    text "The control map is shown on the party select screen and remains available during the fight.":
                        color "#000000"
                        size 15
                        xsize 672

            frame:
                xsize 720
                padding (0, 8, 18, 16)
                background "#d4d0c8"
                hbox:
                    xalign 1.0
                    spacing 10
                    button:
                        background "#0a246a"
                        hover_background "#245edb"
                        padding (18, 6, 18, 6)
                        hover_sound gui.hover_sound
                        activate_sound gui.activate_sound
                        action Return("continue")
                        text "Continue":
                            color "#ffffff"
                            bold True
                            size 13


screen msbf_select_stat_bar(label, value, max_value, fill_color):
    fixed:
        xysize (64, 14)
        use msbf_energy_bar(value, max_value, 64, 14, fill_color, "#152333", danger=False)
        text label style "msbf_select_stat_label":
            xpos 4
            yalign 0.5

# -----------------------------------------------------------------------------
# msbf_shmup_overlay: the phase-3 bullet-hell. The screen itself is STATIC
# chrome (dimmer, stage frame, card texts, fallback keys); everything that
# moves lives in MSBFShmupField below.
#
# MSBFShmupField is the whole Curtain Script stage in ONE creator-defined
# displayable, mirroring Kotonoha mode's KTStage (the 60fps architecture):
#   * the simulation is stepped on a fixed 0.033s accumulator INSIDE render()
#     and the displayable asks for an immediate redraw -- no screen timer, no
#     per-tick renpy.restart_interaction() (the churn that capped the old
#     overlay at 30fps by rebuilding the entire battle screen every tick);
#   * the ship is polled per FRAME (battle._poll_shmup_movement scaled by the
#     frame delta) and bullets are drawn with sub-tick extrapolation
#     (x + vx * acc/tick), so motion is display-framerate smooth while the
#     danmaku stays deterministic in the 30Hz tick;
#   * bullets are the same pixel sprites as Kotonoha mode (bullet/dagger.png,
#     colour-tinted via cached TintMatrix transforms, rotation-bucketed), so
#     Id Mode's curtain reads as a miniature of the full Touhou stage;
#   * the per-tick HUD (timer bar + countdown, clip pips, card declare, hit
#     rings, sparks, source node, player marker) is blitted in the same pass.
# battle_logic still owns spawn/advance/collision; balance is unchanged.
# -----------------------------------------------------------------------------
init python:
    # `key` bindings skip the hover/activate sounds a mouse gets, so the nav
    # screen plays the UI cues by hand: move -> hover, confirm -> accept,
    # back -> denied. Pooled (msbf_play_pooled_sfx) so fast nav overlaps
    # instead of cutting off the previous cue. Built ONCE here rather than in
    # each screen body: they carry no per-frame state, and three screens were
    # re-constructing the identical three actions on every redraw.
    # (init python, not init -1: MSBF_UI_SFX comes from battle_logic.rpy.)
    MSBF_NAV_SFX = {
        "move": Function(msbf_play_pooled_sfx, MSBF_UI_SFX["hover"], _update_screens=False),
        "ok":   Function(msbf_play_pooled_sfx, MSBF_UI_SFX["accept"], _update_screens=False),
        "no":   Function(msbf_play_pooled_sfx, MSBF_UI_SFX["denied"], _update_screens=False),
    }

    # Only the SHIP comes from Kotonoha's folder now; every bullet sprite lives
    # in the shared assets/bullets/ and is reached through EMB_DIR
    # (asset_definitions/def_bullets.rpy).
    MSBF_SHMUP_SPRITE_DIR = "addons/Matsuda's Sick Boss Fight/kotonohamode/"
    MSBF_SHMUP_FONT = "assets/fonts/SF Automaton Extended.ttf"

    class MSBFShmupField(renpy.Displayable):

        # Class-level caches persist across frames and interactions.
        _tf_cache = {}
        _text_cache = {}
        _misc_cache = {}

        # (sprite file, base zoom at size 9, rotates-to-heading?)
        KINDS = {
            "orb":    ("bullet.png", 1.30, False),
            "needle": ("dagger.png", 1.55, True),
        }

        def __init__(self, battle, **kwargs):
            super(MSBFShmupField, self).__init__(**kwargs)
            self.battle = battle
            self.last_st = None
            self.acc = 0.0
            # Keep transient keyboard state on the displayable, not the
            # rollback-managed battle object. This is the same release latch
            # used by KTStage/TSBStage to prevent swallowed KEYUP events from
            # leaving a movement key stuck down.
            self.input_latch = MSBFKeyLatch()

        # ----- input events -------------------------------------------------

        def event(self, ev, x, y, st):
            # Movement itself remains polling-based for smooth held input. The
            # event path exists solely to give the latch authoritative KEYUP /
            # KEYDOWN events; returning None leaves the screen's key bindings
            # and anything below this displayable free to handle the event.
            self.input_latch.handle_event(ev)
            return None

        # ----- cached displayable factories ---------------------------------

        def _bullet_tf(self, shape, color, bucket, size):
            key = (shape, color, bucket, size)
            tf = MSBFShmupField._tf_cache.get(key)
            if tf is None:
                path, base_zoom, rotates = MSBFShmupField.KINDS[shape]
                kw = dict(zoom=base_zoom * (size / 9.0), nearest=True, subpixel=True,
                            matrixcolor=TintMatrix(color))
                if rotates:
                    kw["rotate"] = bucket * MSBF_SHMUP_ROT_BUCKET_DEG
                tf = Transform(EMB_DIR + path, **kw)
                MSBFShmupField._tf_cache[key] = tf
            return tf

        def _misc(self, key, builder):
            d = MSBFShmupField._misc_cache.get(key)
            if d is None:
                d = builder()
                MSBFShmupField._misc_cache[key] = d
            return d

        def _text(self, text, size, color, bold=False):
            key = (text, size, color, bold)
            t = MSBFShmupField._text_cache.get(key)
            if t is None:
                if len(MSBFShmupField._text_cache) > 96:
                    MSBFShmupField._text_cache.clear()
                t = Text(text, size=size, color=color, bold=bold,
                        font=MSBF_SHMUP_FONT, outlines=[(2, "#02040b", 0, 0)])
                MSBFShmupField._text_cache[key] = t
            return t

        # ----- render --------------------------------------------------------

        def render(self, width, height, st, at):
            battle = self.battle
            W = MSBF_SHMUP_STAGE_WIDTH
            H = MSBF_SHMUP_STAGE_HEIGHT

            # F3 profiler (perf.rpy) -- see the note in KTStage.render.
            _perf = MSBF_PERF.on
            _t = msbf_perf_t0() if _perf else 0.0

            # Fixed-timestep simulation (KTStage pattern): clamp big st jumps
            # (a hitch, the preferences menu) and never run more than 4 ticks
            # in one frame.
            if self.last_st is None:
                self.last_st = st
            dt = st - self.last_st
            self.last_st = st
            if dt < 0.0:
                dt = 0.0
            elif dt > 0.25:
                dt = 0.25

            active = battle.shmup_segment_active
            if active:
                # Ship movement is polled per FRAME (scaled so held keys cover
                # the same px/sec as the old 30Hz poll, just smoother).
                battle._poll_shmup_movement(
                    self.input_latch,
                    dt / MSBF_SHMUP_TICK_SECONDS,
                )
                self.acc += dt
                steps = 0
                while self.acc >= MSBF_SHMUP_TICK_SECONDS and steps < 4:
                    battle.update_shmup_segment()
                    self.acc -= MSBF_SHMUP_TICK_SECONDS
                    steps += 1
                    if not battle.shmup_segment_active:
                        self.acc = 0.0
                        break
                if steps >= 4:
                    self.acc = 0.0
            # Sub-tick extrapolation fraction for bullet draw positions.
            frac = min(1.0, self.acc / MSBF_SHMUP_TICK_SECONDS)

            if _perf:
                msbf_perf_t1("sim", _t)
                MSBF_PERF.note("bullets", len(getattr(battle, "shmup_bullets", ())))
                _t = msbf_perf_t0()

            rv = renpy.Render(W, H)
            stage = renpy.Render(W, H)
            sblit = stage.subpixel_blit
            frame_tex = {}

            def tex(key, disp, w=128, h=128):
                entry = frame_tex.get(key)
                if entry is None:
                    r = renpy.render(disp, w, h, st, at)
                    rv.depends_on(r)
                    entry = (r, r.get_size())
                    frame_tex[key] = entry
                return entry

            def rect(color, w, h):
                w = max(1, int(w))
                h = max(1, int(h))
                key = ("rect", color, w, h)
                entry = frame_tex.get(key)
                if entry is None:
                    solid = self._misc(("solid", color), lambda c=color: Solid(c))
                    r = renpy.render(solid, w, h, st, at)
                    rv.depends_on(r)
                    entry = r
                    frame_tex[key] = entry
                return entry

            tick = battle.shmup_tick
            ft = tick + frac

            # --- bullet source: Matsuda's casting node (glow + spinning
            #     diamond), recomputed sub-tick so its drift is 60fps too. ----
            if active:
                sx = W * 0.5 + math.sin(ft * 0.030) * (W * 0.28)
                sy = 60.0
                if MSBF_FX_SHADERS:
                    ib = int((0.5 + 0.5 * math.sin(tick * 0.11)) * 3.999)
                    gkey = ("srcglow", ib)
                    glow = self._misc(gkey, (lambda k=ib: Transform(
                        Solid("#00000000"), xysize=(96, 96), shader="msbf.glow",
                        u_color=(1.0, 0.28, 0.45), u_intensity=0.5 + 0.14 * k,
                        u_softness=1.8)))
                    try:
                        gr, (gw, gh) = tex(gkey, glow, 96, 96)
                        sblit(gr, (sx - gw / 2.0, sy - gh / 2.0))
                    except Exception:
                        pass
                db = (tick // 3) % 6
                dkey = ("srcdiam", db)
                diam = self._misc(dkey, (lambda k=db: Transform(
                    Solid("#ff3868d0"), xysize=(22, 22), rotate=45.0 + k * 15.0)))
                dr, (dw, dh) = tex(dkey, diam, 48, 48)
                sblit(dr, (sx - dw / 2.0, sy - dh / 2.0))
                core = self._misc("srccore", lambda: Transform(
                    Solid("#ffffffee"), xysize=(11, 11), rotate=45.0))
                cr, (cw, ch) = tex("srccore", core, 32, 32)
                sblit(cr, (sx - cw / 2.0, sy - ch / 2.0))

            # --- sparks (hit feedback) ----------------------------------------
            for s in (getattr(battle, "shmup_sparks", None) or ()):
                sfrac = s["age"] / float(s["ttl"])
                ab = 2 - min(2, int(sfrac * 3.0))
                skey = ("spark", s["color"], ab)
                spark_d = self._misc(skey, (lambda c=s["color"], a=ab: Transform(
                    EMB_DIR + "bullet.png", zoom=0.55, subpixel=True,
                    matrixcolor=TintMatrix(c), alpha=0.30 + 0.28 * a)))
                spr, (spw, sph) = tex(skey, spark_d, 32, 32)
                sblit(spr, (s["x"] - spw / 2.0, s["y"] - sph / 2.0))

            # --- enemy bullets: THE hot loop ----------------------------------
            bullets = getattr(battle, "shmup_bullets", ())
            draw_cores = len(bullets) <= 200
            for bullet in bullets:
                shape = bullet.get("shape", "orb")
                bx = bullet["x"] + bullet.get("vx", 0.0) * frac
                by = bullet["y"] + bullet.get("vy", 0.0) * frac
                # Newborn bullets flash white for a beat -- the spawn telegraph.
                color = "#ffffffee" if bullet.get("age", 0) < 5 else bullet.get("color", "#ff3868dd")
                size = int(bullet.get("size", 9))
                if shape == "needle":
                    bucket = int(round(bullet.get("rot", 0.0) / MSBF_SHMUP_ROT_BUCKET_DEG)) % MSBF_SHMUP_ROT_BUCKETS
                else:
                    bucket = 0
                    shape = "orb"
                # Frame memo first -- see the same note in KTStage's loop.
                bkey = (shape, color, bucket, size)
                bgot = frame_tex.get(bkey)
                if bgot is None:
                    bgot = tex(bkey, self._bullet_tf(shape, color, bucket, size))
                br, (bw, bh) = bgot
                sblit(br, (bx - bw / 2.0, by - bh / 2.0))
                if draw_cores and shape == "orb" and color != "#ffffffee":
                    ckey = ("orb", "#f5fbffea", 0, max(4, size // 2))
                    cgot = frame_tex.get(ckey)
                    if cgot is None:
                        cgot = tex(ckey, self._bullet_tf("orb", "#f5fbffea", 0, max(4, size // 2)))
                    cr2, (cw3, ch3) = cgot
                    sblit(cr2, (bx - cw3 / 2.0, by - ch3 / 2.0))

            # --- clip rings (msbf.ring shader; skipped without shaders) --------
            if MSBF_FX_SHADERS:
                for hfx in (getattr(battle, "shmup_hit_fx", None) or ()):
                    aged = tick - hfx["tick"]
                    if not (0 <= aged < 36):
                        continue
                    pb = int(aged / 36.0 * 15.999)
                    rkey = ("clipring", pb)
                    ring_d = self._misc(rkey, (lambda p=pb: Transform(
                        Solid("#00000000"), xysize=(360, 360), shader="msbf.ring",
                        u_progress=(p + 0.5) / 16.0, u_color=(1.0, 0.36, 0.48),
                        u_thickness=0.16, u_intensity=1.3)))
                    try:
                        rr, (rw, rh) = tex(rkey, ring_d, 360, 360)
                        sblit(rr, (hfx["x"] - rw / 2.0, hfx["y"] - rh / 2.0))
                    except Exception:
                        pass

            # --- player ship ----------------------------------------------------
            if active:
                px = battle.shmup_player_x
                py = battle.shmup_player_y
                inv = tick < getattr(battle, "shmup_invuln_until_tick", 0)
                blink_off = inv and (tick // MSBF_SHMUP_IFRAME_BLINK_TICKS) % 2 == 1
                if not blink_off:
                    if inv:
                        ship = self._misc("ship_hit", lambda: Transform(
                            MSBF_SHMUP_SPRITE_DIR + "player.png", zoom=2.6, nearest=True,
                            subpixel=True, matrixcolor=BrightnessMatrix(0.7)))
                        pkey = "ship_hit"
                    else:
                        ship = self._misc("ship", lambda: Transform(
                            MSBF_SHMUP_SPRITE_DIR + "player.png", zoom=2.6, nearest=True,
                            subpixel=True))
                        pkey = "ship"
                    shr, (shw, shh) = tex(pkey, ship, 64, 64)
                    sblit(shr, (px - shw / 2.0, py - shh / 2.0))
                else:
                    # Dim core dot on the off-beat so position stays trackable.
                    dot = self._misc("ship_dot", lambda: Transform(
                        EMB_DIR + "bullet.png", zoom=0.4, subpixel=True,
                        alpha=0.5))
                    dtr, (dtw, dth) = tex("ship_dot", dot, 16, 16)
                    sblit(dtr, (px - dtw / 2.0, py - dth / 2.0))
                if battle.shmup_focus and not blink_off:
                    fring = self._misc("focus_ring", lambda: Transform(
                        EMB_DIR + "bullet.png", zoom=1.5, subpixel=True,
                        matrixcolor=TintMatrix("#55ddff"), alpha=0.5))
                    fr, (fw2, fh2) = tex("focus_ring", fring, 48, 48)
                    sblit(fr, (px - fw2 / 2.0, py - fh2 / 2.0))
                    hbd = self._misc("hitbox", lambda: Transform(
                        EMB_DIR + "bullet.png", zoom=0.75, subpixel=True))
                    hbr, (hbw, hbh) = tex("hitbox", hbd, 24, 24)
                    sblit(hbr, (px - hbw / 2.0, py - hbh / 2.0))
                if inv:
                    sblit(rect("#ff38681e", W, H), (0, 0))

            # --- HUD: survival bar + countdown + clip pips ----------------------
            fill_w = int(W * min(1.0, tick / float(MSBF_SHMUP_DURATION_TICKS)))
            sblit(rect("#02040b88", W, 4), (0, 0))
            if fill_w > 0:
                sblit(rect("#ffcf66", fill_w, 4), (0, 0))
                sblit(rect("#f5fbff", 2, 4), (max(0, fill_w - 2), 0))
            secs = max(0, (MSBF_SHMUP_DURATION_TICKS - tick) // 30)
            tcol = "#ff5c6a" if secs <= 5 else "#f5fbff"
            tr, (tw, th) = tex(("timer", secs, tcol), self._text("%02d" % secs, 20, tcol, True), 72, 34)
            sblit(tr, (W - tw - 12, 12))
            for i in range(MSBF_SHMUP_HIT_LIMIT):
                taken = i < battle.shmup_hits
                pkey2 = ("pip", taken)
                pip = self._misc(pkey2, (lambda t2=taken: Transform(
                    Solid("#ff3868" if t2 else "#ffffff30"), xysize=(10, 10), rotate=45.0)))
                pr2, (pw2, ph2) = tex(pkey2, pip, 24, 24)
                sblit(pr2, (12 + i * 22, 16 - ph2 / 2.0 + 5))

            # --- card declare: big centred name for the opening beat, with the
            #     Touhou blink-in and a brief white flash. ----------------------
            if active and tick < 66:
                pt = tick
                if (pt // 3) % 4 != 0 or pt > 24:
                    a = min(1.0, pt / 14.0)
                    yy = H * 0.34 - (1.0 - a) * 20.0
                    kick, (kw, kh) = tex(("t", "declare_kick"),
                                        self._text("CURTAIN SCRIPT DECLARES", 13, "#ff6b8f", True), 320, 26)
                    sblit(kick, (W / 2.0 - kw / 2.0, yy - 28.0))
                    name = battle.shmup_pattern_name
                    nr, (nw, nh) = tex(("declare_name", name),
                                        self._text(name, 30, "#f5fbff", True), W - 60, 52)
                    sblit(nr, (W / 2.0 - nw / 2.0, yy))
                flash = max(0.0, (8 - pt) / 8.0)
                if flash > 0.0:
                    sblit(rect("#f5fbff" + ("%02x" % int(flash * 100)), W, H), (0, 0))

            # Clip to the stage (bullets live 64px past the lip) and mount it.
            # The clip is a FLAG, not a subsurface: Render.subsurface walks every
            # child, computes two sublines apiece and wraps each in a fresh
            # cropped Render (recursing once more into the blitted texture's own
            # Render), so a busy cast was minting a four-figure count of
            # throwaway Render objects per frame -- each one appended to
            # renpy.display.render.live_renders and walked and killed again by
            # the next mark_sweep -- for pixels identical to these two lines.
            # gl2 turns xclipping/yclipping into a clip polygon on its own side.
            stage.xclipping = True
            stage.yclipping = True
            rv.blit(stage, (0, 0))

            # DRAW RATE CEILING. Unlike the Kotonoha and Tsubaki stages this one
            # DOES interpolate -- bullets are drawn at x + vx * frac -- so it
            # genuinely wants more frames than its 30Hz tick and cannot simply
            # be pinned to the tick boundary. What it does not want is to scale
            # with the panel: three interpolated frames per tick is already past
            # the point anyone can see, and asking for a frame IMMEDIATELY meant
            # a 240Hz display ran this loop (three hundred bullets, python-side)
            # eight times per tick.
            #
            # A period rather than a rate, because that is what the engine's
            # scheduler takes: it wakes at the first vblank at or after the
            # delay, so a 60Hz display still draws every single frame and only a
            # high-refresh one is capped.
            if _perf:
                msbf_perf_t1("draw", _t)

            if active:
                renpy.redraw(self, MSBF_DRAW_PERIOD)
            return rv

screen msbf_shmup_overlay(battle):
    use enter_m_input_lock()
    # Fallback movement only: shmup_nudge no-ops while the field's per-frame
    # keyboard polling is healthy, so these never double-step the ship.
    key "K_LEFT" action Function(battle.shmup_nudge, -22, 0)
    key "K_RIGHT" action Function(battle.shmup_nudge, 22, 0)
    key "K_UP" action Function(battle.shmup_nudge, 0, -22)
    key "K_DOWN" action Function(battle.shmup_nudge, 0, 22)
    key "K_a" action Function(battle.shmup_nudge, -22, 0)
    key "K_d" action Function(battle.shmup_nudge, 22, 0)
    key "K_w" action Function(battle.shmup_nudge, 0, -22)
    key "K_s" action Function(battle.shmup_nudge, 0, 22)

    fixed:
        add Solid("#00000078")

        frame:
            xpos MSBF_SHMUP_STAGE_X
            ypos MSBF_SHMUP_STAGE_Y
            xsize MSBF_SHMUP_STAGE_WIDTH
            ysize MSBF_SHMUP_STAGE_HEIGHT
            background Solid("#02040bea")
            padding (0, 0)

            fixed:
                xysize (MSBF_SHMUP_STAGE_WIDTH, MSBF_SHMUP_STAGE_HEIGHT)

                add Solid("#55ddff18") xysize (MSBF_SHMUP_STAGE_WIDTH, 2)
                add Solid("#ff386830") xysize (MSBF_SHMUP_STAGE_WIDTH, 2):
                    yalign 1.0

                # THE game: sim step + bullets + source + ship + sparks + HUD,
                # all inside one self-redrawing displayable (see above).
                add MSBFShmupField(battle)

        # Static HUD. The spell-card title used to be printed here AND again by
        # the field itself a hundred pixels lower -- two copies of the same two
        # lines, which only survived because the old stage box put enough space
        # between them to read as decoration. The field's own banner is the one
        # that animates with the cast, so this keeps that and drops the copy.
        #
        # The movement hint is anchored to the STAGE, not to the screen: at a
        # fixed y it landed straight on top of the field's banner the moment the
        # playfield moved. It also fades out now -- it is an opening instruction,
        # and leaving it burned across the middle of a bullet hell for the whole
        # cast was the single most cluttered thing left in the fight.
        text "W A S D  /  ARROW KEYS  TO  MOVE        HOLD  SHIFT  TO  FOCUS" style "msbf_shmup_controls_big" at msbf_shmup_hint:
            xalign 0.5
            ypos MSBF_SHMUP_STAGE_Y + 296

        text "KEYBOARD ONLY  ||  WASD / ARROWS  ||  SHIFT = SLOW, PRECISE" style "msbf_shmup_controls_small":
            xalign 0.5
            ypos MSBF_SHMUP_STAGE_Y + MSBF_SHMUP_STAGE_HEIGHT + 12

# A full-width countdown bar that drains over `dur` seconds. Timer/transform state
# persists across screen updates, so the typing input's keystrokes don't reset it.
transform msbf_qte_drain(dur):
    xsize 1280
    linear dur xsize 0

transform msbf_qte_timer_throb:
    alpha 1.0
    block:
        easein 0.4 alpha 0.3
        easeout 0.4 alpha 1.0
        repeat

# -----------------------------------------------------------------------------
# msbf_typing_overlay: phase-3 "Rewrite Order" typing QTE. The script demands a
# word; type it before the drain bar empties. An exact (case-insensitive) match
# wins (chips the boss); the timeout is a single-target loss. Runs as an overlay
# inside msbf_battle_screen, driven by battle.typing_segment_active.
# -----------------------------------------------------------------------------
screen msbf_typing_overlay(battle):
    modal True
    zorder 60
    use enter_m_input_lock()

    $ _word = battle.typing_word
    $ _match = battle.typing_input.strip().upper() == _word.upper()

    # Per-letter feedback: the target word lights up green as far as your input
    # matches it; the moment you typo, the remainder burns red until you fix it.
    python:
        _typed = battle.typing_input.strip().upper()
        _wu = _word.upper()
        _pref = 0
        for _ca, _cb in zip(_typed, _wu):
            if _ca != _cb:
                break
            _pref += 1
        _mistake = len(_typed) > _pref
        _rest_col = "#ff5c6a" if _mistake else "#55ddff"
        _word_markup = ("{color=#8affb0}" + _word[:_pref] + "{/color}"
                        + "{color=" + _rest_col + "}" + _word[_pref:] + "{/color}")

    # Timeout = fail. finish_phase_three_typing guards against a double-fire, so
    # whichever of these lands first wins and the other no-ops.
    timer battle.typing_time_limit action Function(battle.finish_phase_three_typing, False)
    if _match:
        timer 0.02 action Function(battle.finish_phase_three_typing, True)

    add Solid("#00000ad6")

    # Prominent top countdown bar.
    add Solid("#12060c") xpos 0 ypos 0 xsize 1280 ysize 14
    add Solid("#ff3868") xpos 0 ypos 0 ysize 14 at msbf_qte_drain(battle.typing_time_limit)
    add Solid("#ff3868") xpos 0 ypos 14 xsize 1280 ysize 2 at msbf_qte_timer_throb

    frame:
        xalign 0.5
        yalign 0.5
        xsize 880
        background msbf_panel_bg(col="#0b1424", accent="#ff3868", alpha=0.96, edge=1.0, fallback="#06101cf6")
        padding (44, 34)

        vbox:
            xalign 0.5
            spacing 16

            text "GENRE SHIFT || TEXT PARSER" xalign 0.5 size 20 color "#ff8fb0" outlines [(2, "#000000cc", 0, 0)]
            text "REWRITE ORDER — TYPE THE WORD" xalign 0.5 size 26 color "#e6e9ef" outlines [(2, "#000000cc", 0, 0)]

            frame:
                xalign 0.5
                background msbf_panel_bg(col="#030910", accent=("#8affb0" if _match else ("#ff5c6a" if _mistake else "#2a4258")), alpha=0.88, edge=0.6, fallback="#02060cf0")
                padding (28, 16)
                text _word_markup xalign 0.5 size 58 outlines [(3, "#000000dd", 0, 0)]

            frame:
                xalign 0.5
                xsize 520
                background msbf_panel_bg(col="#030910", accent="#2a4258", alpha=0.88, edge=0.5, fallback="#02060cf0")
                padding (18, 12)
                input:
                    value FieldInputValue(battle, "typing_input")
                    length (len(_word) + 4)
                    xalign 0.5
                    size 40
                    color ("#8affb0" if _match else ("#ff5c6a" if _mistake else "#ffffff"))

            if _mistake:
                text "The script rejects the word — backspace and retype." xalign 0.5 size 18 color "#ff8fa0"
            else:
                text "Type it before the ink dries." xalign 0.5 size 18 color "#9fb4c4"

# -----------------------------------------------------------------------------
# msbf_quiz_overlay: phase-3 "Multiple Choice Interrupt" quiz QTE. Pick the
# correct answer before the timer runs out. Correct wins (chips the boss); wrong
# or timeout is a party-wide loss. Modeled on the Monika-mode timed choice.
# -----------------------------------------------------------------------------
screen msbf_quiz_overlay(battle):
    modal True
    zorder 60
    use enter_m_input_lock()

    $ _q_count = len(battle.quiz_options)
    $ _q_cur = max(0, min(battle.quiz_cursor, _q_count - 1)) if _q_count else 0

    timer battle.quiz_time_limit action Function(battle.finish_phase_three_quiz, False)

    # Keyboard: arrows / WASD move the cursor, Z / Enter answers. The cursor lives
    # on the battle object (battle.quiz_cursor) -- screen vars misresolve here
    # because this overlay is `use`d inside msbf_battle_screen.
    if _q_count:
        $ _q_prev = Function(battle.quiz_move, -1)
        $ _q_next = Function(battle.quiz_move, 1)
        use msbf_nav_keys(_q_prev, _q_next, _q_prev, _q_next, Function(battle.quiz_confirm))
        # Direct answer: number row 1..4 picks and confirms in one press.
        for _qk in range(min(_q_count, 4)):
            key ("K_%d" % (_qk + 1)) action [MSBF_NAV_SFX["ok"], SetField(battle, "quiz_cursor", _qk), Function(battle.quiz_confirm)]

    add Solid("#00000ad6")

    add Solid("#12060c") xpos 0 ypos 0 xsize 1280 ysize 14
    add Solid("#ff3868") xpos 0 ypos 0 ysize 14 at msbf_qte_drain(battle.quiz_time_limit)
    add Solid("#ff3868") xpos 0 ypos 14 xsize 1280 ysize 2 at msbf_qte_timer_throb

    vbox:
        xalign 0.5
        yalign 0.5
        xsize 940
        spacing 14

        text "GENRE SHIFT || MULTIPLE CHOICE" xalign 0.5 size 20 color "#ff8fb0" outlines [(2, "#000000cc", 0, 0)]

        frame:
            xfill True
            background msbf_panel_bg(col="#0b1424", accent="#ff3868", alpha=0.96, edge=1.0, fallback="#06101cf6")
            padding (34, 22)
            text battle.quiz_prompt xalign 0.5 size 28 color "#e6e9ef" text_align 0.5 outlines [(2, "#000000cc", 0, 0)] xmaximum 860

        vbox:
            xalign 0.5
            spacing 10
            for _qi, _opt in enumerate(battle.quiz_options):
                $ _q_sel = (_qi == _q_cur)
                button:
                    xsize 820
                    xalign 0.5
                    background msbf_panel_bg(col=("#124060" if _q_sel else "#081220"), accent=("#9becff" if _q_sel else "#2a4258"), alpha=0.94, edge=(1.0 if _q_sel else 0.4), fallback=("#1d5c82ee" if _q_sel else "#0b1728ee"))
                    hover_background msbf_panel_bg(col="#124060", accent="#9becff", alpha=0.94, edge=1.0, fallback="#1d5c82ee")
                    padding (18, 12)
                    hover_sound MSBF_UI_SFX["hover"]
                    activate_sound MSBF_UI_SFX["accept"]
                    hovered SetField(battle, "quiz_cursor", _qi)
                    action Function(battle.answer_phase_three_quiz, _opt[1])

                    hbox:
                        spacing 16
                        yalign 0.5
                        frame:
                            xysize (34, 34)
                            yalign 0.5
                            padding (0, 0)
                            background msbf_panel_bg(col=("#1a5a82" if _q_sel else "#0c1c30"), accent=("#9becff" if _q_sel else "#2a4258"), alpha=0.95, edge=0.9, fallback=("#2c7fac" if _q_sel else "#102338"))
                            text ("%d" % (_qi + 1)) size 18 color ("#f5fbff" if _q_sel else "#7fa6bd") bold True xalign 0.5 yalign 0.5
                        text _opt[0] size 22 color ("#f5fbff" if _q_sel else "#c4d6e2") yalign 0.5 xmaximum 720

        text "Arrows / WASD move || Z / Enter answer || 1-4 quick-pick || beat the timer." xalign 0.5 size 18 color "#9fb4c4"

# -----------------------------------------------------------------------------
# msbf_battle_screen: THE fight (the screen cs_matsuda_02.rpy `call screen`s).
# It composes the backdrop + boss + party cards + press-turn row + battle log +
# the command menu, layering msbf_fx_layer / phase overlays / msbf_shmup_overlay
# as the battle's turn_phase dictates. Every button action calls into the
# `battle` (MSBFBattleState) -- player_use_skill / player_pass / target selection
# / start_enemy_phase / advance_enemy_phase -- and the screen redraws from the
# resulting state. It Returns battle.result ("victory"/...) when the fight ends.
# Enemy turns and the shmup advance on timers so the action plays out hands-free.
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# msbf_battle_screen: THE FIGHT.
#
# LAYOUT, AND WHY IT IS SHAPED LIKE THIS
#   The fight used to be three chrome-edged panels -- a left rail, a boxed
#   stage, and a bottom deck -- always on screen, always at full strength. The
#   boss lived inside the middle box with a visible seam around her, and the
#   log box held one line of text in three hundred pixels of black.
#
#   Now there are two layers and no boxes:
#
#   THE WORLD (arena.rpy) fills the frame and never moves out of the way: the
#   projected deck, the void, the boss standing in it with a shadow and a
#   reflection, and the party downstage as silhouettes. All of it hangs off one
#   camera rig so a hit can shove the entire room without anything drifting out
#   of register.
#
#   THE HUD floats over it, unframed, and RETREATS WHEN IT IS NOT NEEDED. The
#   command deck only materialises on the acting character's turn; during the
#   enemy phase, the cinematics and the microgames the screen is just the
#   fight. Readouts are grouped by what they answer:
#       top-left     -- what is happening (boss, her health, the last 3 lines)
#       top-right    -- whose tempo it is (press turns)
#       over a head  -- that member's own state
#       bottom band  -- what YOU can do, and only while you can do it
#
# WHAT THIS SCREEN OWNS vs WHAT IT READS
#   It still owns no rules. It reads `battle` (an MSBFBattleState) every redraw
#   and calls battle.player_use_skill / player_pass / advance_enemy_phase; the
#   arena reads the same object through msbf_arena_uniforms(). Positions for
#   anything that has to LAND on someone come from arena.rpy's
#   msbf_stage_anchor / msbf_boss_anchor, so the FX and the figures cannot
#   disagree about where a character is.
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
    # WHO OWNS THE HIGHLIGHT. The mouse pointer does not move when you use the
    # keyboard, so a pointer parked over a skill chip kept painting that chip's
    # hover_background while the keyboard cursor lit a different one -- two
    # highlighted boxes, neither obviously the real selection. Whichever device
    # moved last owns the highlight; the other one stops painting.
    default kb_active = False
    default show_controls = False
    default show_log = False
    default cam_token = None
    default cam_seen = None
    default cam_strength = 1.0
    default ambient_wave = False
    default ambient_delay = renpy.random.uniform(3.4, 6.6)

    $ _actor = battle.current_actor
    $ _actor_name = battle.active_actor_label
    $ _actor_idx = battle.party.index(_actor) if (_actor is not None and _actor in battle.party) else None

    # The room's geometry, resolved once. Everything below positions against
    # these rather than against literals, so retuning the staging in arena.rpy
    # moves the HUD's anchors with it.
    $ _stage = msbf_boss_stage(battle.phase)
    $ _boss_x, _boss_y = msbf_boss_anchor(battle.phase)
    $ _accent, _accent2 = msbf_phase_accent(battle.phase)
    $ _key_rgb = msbf_arena_cfg(battle.phase)["key"]

    # The party is FOUR for most of the fight and SEVEN from the moment phase 3
    # summons the full roster, so every position on the deck is derived from the
    # live count rather than from a fixed table.
    $ _party_n = len(battle.party)
    $ _tag_w, _tag_h, _tag_bar_y = msbf_stage_tag_metrics(_party_n)

    # WHO JUST TOOK A HIT. float_events already carries the damage numbers and
    # each one is anchored to a party index, so the set of indices in the
    # current batch IS the set of people who were just struck -- no new state
    # in the battle object, and it cannot drift out of step with the numbers
    # because it is the same feed drawing them.
    python:
        # The impact weight is resolved HERE, before anything reads it: the
        # hit-set below scales off it and is computed early, while the camera
        # and shockwave that also read it are set up further down.
        _impact_w = msbf_impact_weight(battle.fx_event)
        _impact_token = battle.fx_serial if _impact_w > 0.0 else None

        _hit_set = set()
        if battle.float_events:
            for _fe_h in battle.float_events:
                _fa_h = _fe_h.get("anchor", "boss")
                if isinstance(_fa_h, int) and _fe_h.get("kind") in ("enemy", "dmg", "crit", "weak"):
                    _hit_set.add(_fa_h)
        _hit_tok = battle.float_serial
        _hit_w = max(0.45, _impact_w) if _hit_set else 0.0

    # When the HUD gets out of the way. The command deck is the only thing on
    # screen the player can act through, so it is also the only thing whose
    # absence is information: if it is not there, it is not your turn.
    $ _cinematic = battle.phase_transition_active or battle.final_victory_active or battle.defeat_sequence_active or bool(battle.result)
    $ _hud_on = not (_cinematic or battle.microgame_active)

    # NOTHING DRAWS UNDER AN OPAQUE COVER. Three states in this fight lay a
    # full-screen, fully-opaque Solid over the entire frame -- the defeat
    # blackout, the victory whiteout, and the beat of a phase transition before
    # the reveal cinematic takes over. The world layer underneath was still
    # being built and drawn through all of them: the arena shader over the
    # whole frame, plus one silhouette per party member, for a picture that is
    # by definition invisible. Phase transitions are also the moment the
    # cinematics are at their most expensive, so this is the cull that lands on
    # the worst frames rather than the average ones.
    #
    # Only these three, and only because each is a bare `add Solid(...)` with
    # no alpha: the break and reveal sequences animate their cover and the room
    # legitimately shows through them.
    $ _world_on = not (getattr(battle, "defeat_blackout", False)
                    or getattr(battle, "final_victory_whiteout", False)
                    or (battle.phase_transition_active and not battle.fx_event
                        and not getattr(battle, "phase2_reveal_started", False)))
    $ _deck_on = _hud_on and _actor is not None and battle.turn_phase == "player"

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
    # NOTE: the shmup segment has no timer branch -- MSBFShmupField steps the
    # simulation inside its own render() and hands control back via
    # _finish_microgame_turn's single restart_interaction when the cast ends.
    elif battle.handover_active and not battle.fx_event:
        # The tempo changes here, a beat AFTER the action that ended the phase
        # has finished playing -- see MSBFBattleState.handover_active.
        timer battle.handover_delay action Function(battle.finish_handover)
    elif battle.enemy_phase_active and not battle.fx_event:
        timer battle.enemy_step_delay action Function(battle.advance_enemy_phase)

    # --- THE IMPACT ---------------------------------------------------------
    # ONE weight, from ONE table (MSBF_IMPACT_WEIGHT in arena.rpy), driving
    # every consumer: the camera punch, the floor shockwave, and the reaction
    # on whoever got hit. They cannot disagree about how big a moment this is
    # because they are all reading the same number.
    #
    # THE TOKEN IS fx_serial, and that is the whole fix for the double-fire.
    # It used to be (fx_event, log_serial), on the reasoning that fx_event
    # alone repeats across consecutive identical actions -- but a single action
    # writes SEVERAL log lines ("Matsuda uses X for 40 damage." then "Weakness
    # hit." then "Seeker is downed."), so the pair changed two or three times
    # per strike and fired an impact for each. fx_serial is incremented exactly
    # once, inside set_fx, which is precisely "a new FX cue happened".
    # TWO variables, and they are not redundant. `cam_seen` is the last token we
    # have ever fired for and is never cleared; `cam_token` is the live one and
    # clears itself to drop the shock branch. Testing the fire condition against
    # the LIVE token instead played the impact twice: the clear-timer put
    # cam_token back to None while battle.fx_event was still sitting on "hit",
    # so the next redraw saw token != None and fired the whole thing again.
    if _impact_token is not None and _impact_token != cam_seen:
        timer 0.01 action [SetScreenVariable("cam_seen", _impact_token), SetScreenVariable("cam_token", _impact_token), SetScreenVariable("cam_strength", _impact_w)]
    if cam_token is not None:
        timer 0.70 action SetScreenVariable("cam_token", None)

    # Ambient pressure pulse in phases 2-3: the room itself throws a wave every
    # few seconds. This replaces the old msbf_phase2_boom_overlay / phase3
    # rupture overlays, which were ~20 individually-animated Solid rectangles
    # each; it is now one uniform on a shader that is already drawing.
    #
    # The flag has to go back DOWN between waves. Matsu'Py carries an ATL's
    # execution state across screen re-executions when it is the same block at
    # the same position, so the only thing that actually restarts the wave is
    # the `if shock:` branch below flipping and rebuilding the node. A latching
    # "have we ever pulsed" counter therefore fires exactly one wave, ever.
    if battle.phase >= 2 and _hud_on and committing is None:
        timer ambient_delay repeat True action [SetScreenVariable("ambient_wave", True), SetScreenVariable("ambient_delay", renpy.random.uniform(1.8, 3.4) if battle.phase == 3 else renpy.random.uniform(3.8, 7.0))]
    if ambient_wave:
        timer 0.70 action SetScreenVariable("ambient_wave", False)

    if battle.float_events and float_seen_serial != battle.float_serial:
        timer 1.15 action [Function(battle.clear_float_events), SetScreenVariable("float_seen_serial", battle.float_serial)]

    # Dedicated fight pause menu (bare essentials + audio, no Main Menu/Save/
    # Load) -- see pause_menu.rpy. Shown as a plain modal OVERLAY (Show, not
    # ShowMenu): entering the game-menu context here made its Return/Escape
    # unwind a call_in_new_context fight all the way to the main menu (and, in
    # dev builds, the dev scene selector). Suppressed during the real-time
    # microgames so it can't overlay a live shmup/typing/quiz cast.
    if not battle.microgame_active:
        key "game_menu" action Show("msbf_pause_menu")
        key "K_ESCAPE" action Show("msbf_pause_menu")

    # --- Keyboard command deck (Z/Enter confirm, X/LShift back, arrows + WASD
    #     to move the cursor). Active only on the player's turn so it never eats
    #     the typing-QTE input or the shmup's own movement keys. The cursor
    #     navigates the skill grid, or the valid targets while choosing an ally
    #     target. ---
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

        # RELATIVE steps, not precomputed destinations -- see msbf_kb_step.
        _kb_left = Function(msbf_kb_step, "kb_index", -1, _kb_count) if _kb_count else NullAction()
        _kb_right = Function(msbf_kb_step, "kb_index", 1, _kb_count) if _kb_count else NullAction()
        if _kb_targeting or _kb_count <= 4:
            _kb_up = _kb_left
            _kb_down = _kb_right
        else:
            _kb_up = Function(msbf_kb_step, "kb_index", -4, _kb_count)
            _kb_down = Function(msbf_kb_step, "kb_index", 4, _kb_count)

        # Confirm/back depend on the focused item; precompute so the key actions
        # fire the exact same behaviour as clicking.
        _kb_confirm = None
        _kb_back = None
        if _kb_on and _kb_count:
            _focus = _kb_items[_kb_cur]
            if _kb_targeting:
                _kb_confirm = [SetScreenVariable("hovered_skill", None), SetScreenVariable("pending_skill", None), SetScreenVariable("committing", {"skill": pending_skill, "target": _focus, "actor_index": _actor_idx, "element": pending_skill.element, "ally": True})]
                _kb_back = [SetScreenVariable("pending_skill", None), SetScreenVariable("hovered_skill", None)]
            else:
                if battle.can_use(_focus) and battle.skill_needs_ally_target(_focus):
                    _kb_confirm = [SetScreenVariable("hovered_skill", _focus), SetScreenVariable("pending_skill", _focus), SetScreenVariable("kb_index", 0)]
                elif battle.can_use(_focus):
                    _kb_confirm = [SetScreenVariable("hovered_skill", None), SetScreenVariable("pending_skill", None), SetScreenVariable("committing", {"skill": _focus, "actor_index": _actor_idx, "element": _focus.element})]
                _kb_back = Function(battle.player_pass)

    if _kb_on:
        use msbf_nav_keys(_kb_up, _kb_down, _kb_left, _kb_right, _kb_confirm, _kb_back)

    # =========================================================================
    # LAYER 1 -- THE WORLD
    # One container, one camera. At rest msbf_cam_rest is the identity, so
    # swapping in the punch on an impact costs nothing when nothing is hitting.
    # =========================================================================
    python:
        if battle.final_victory_active:
            _cam_at = msbf_cam_victory
        elif battle.defeat_sequence_active:
            _cam_at = msbf_cam_defeat
        elif cam_token is not None:
            _cam_at = msbf_cam_punch(cam_strength, cam_token)
        else:
            _cam_at = msbf_cam_rest

    fixed:
        xysize (1280, 720)
        at _cam_at

        if _world_on:
            use msbf_arena(battle, (cam_token is not None) or ambient_wave, (cam_strength if cam_token is not None else 0.8))

        # THE CINEMATIC OWNS HER DURING A PHASE TRANSITION. msbf_phase_reveal_seq
        # draws its own descending copy of the boss, so leaving the resting one
        # here put two of her on screen at once -- one arriving from above and
        # one already standing where she was about to land.
        $ _world_boss = _world_on and not battle.shmup_segment_active and not battle.phase_transition_active

        if _world_boss:
            use msbf_ground_reflection(battle.boss_art, _stage["cx"], _stage["foot"], _stage["w"], _stage["h"])
            use msbf_ground_shadow(_stage["cx"], _stage["foot"], _stage["shadow_w"], _stage["shadow_a"], _stage["airborne"])

        # --- THE BOSS ------------------------------------------------------
        # ONE sprite draw in every state. The old screen drew the full 735px
        # sprite two to four times per frame (a base plus afterimages plus, in
        # phase 3, a chromatic ghost) purely for the trailing look; msbf.smear
        # does the trail and the channel split in a single pass, so the boss
        # costs a quarter of what she used to and looks like more.
        if _world_boss:
            $ _smear = msbf_boss_smear_for(battle)
            add battle.boss_art:
                at _smear
                xcenter _boss_x
                ycenter _boss_y
                xysize (_stage["w"], _stage["h"])
                fit "contain"

        # --- THE PARTY, IN THE ROOM ----------------------------------------
        if _world_on and not battle.shmup_segment_active:
            for _pi, _pm in enumerate(battle.party):
                use msbf_party_silhouette(_pm, _pi, _party_n, _key_rgb, (_actor is not None and _pm.id == _actor.id), (not _pm.alive), (_hit_w if _pi in _hit_set else 0.0), _hit_tok)

    # =========================================================================
    # LAYER 2 -- THE HUD
    # =========================================================================

    # --- Boss readout: name, bar, and the last three lines of the log -------
    # No frame, no box. The scrim behind it is a gradient that actually reaches
    # zero, so this reads as text lying on the room rather than a panel over it.
    if _hud_on and not battle.shmup_segment_active:
        $ _bn_danger = battle.boss.hp_ratio < 0.25
        use msbf_hud_scrim(0, 0, 760, 260, 1.0, 0.62, 1.0)

        text battle.boss.name style "msbf_boss_name":
            xpos 48
            ypos 34
            xmaximum 600

        fixed:
            xpos 48
            ypos 74
            use msbf_energy_bar(battle.boss.hp, battle.boss.max_hp, 470, 11, "#ff3868", "#131722", danger=_bn_danger)

        if battle.analyzed:
            $ _bn_weak = msbf_affinity_label(battle.boss.weaknesses)
            $ _bn_resist = msbf_affinity_label(battle.boss.resists)
            text "WEAK  [_bn_weak]" style "msbf_affinity_weak":
                xpos 48
                ypos 92
                xmaximum 470
            text "RESIST  [_bn_resist]" style "msbf_affinity_resist":
                xpos 48
                ypos 108
                xmaximum 470
        else:
            text "AFFINITIES UNKNOWN" style "msbf_affinity_unknown":
                xpos 48
                ypos 93

        # The log, as three fading lines. Oldest at the top and nearly gone;
        # the newest is the only one at full strength, which is the whole point
        # -- a combat log is read for its last line and skimmed for the rest.
        $ _log_tail = list(battle.log)[-3:]
        $ _log_n = len(_log_tail)
        for _li, _line in enumerate(_log_tail):
            $ _log_age = (_log_n - 1) - _li
            text _line style MSBF_LOG_LINE_STYLE[min(_log_age, 2)]:
                xpos 48
                ypos 138 + (_li * 22)
                xmaximum 610

    # --- Tempo: the press-turn track, top-right, unframed -------------------
    if _hud_on and not battle.shmup_segment_active:
        use msbf_hud_scrim(840, 0, 440, 170, 1.0, 0.7, -1.0)

        text battle.press_turn_label style "msbf_tempo_kicker":
            xanchor 1.0
            xpos 1232
            ypos 36
        text "[battle.active_actions_this_phase]/[battle.active_action_cap]" style "msbf_tempo_count":
            xanchor 1.0
            xpos 1232
            ypos 54

        # The pip row is RIGHT-ALIGNED as a block but LEFT-ALIGNED inside it.
        # msbf_press_turn_fx_icon positions itself absolutely from the slot
        # index (battle_logic's press_turn_slot_x), so the row's own origin has
        # to be slot 0 -- right-aligning the hbox itself instead left the spend/
        # gain flashes stranded to the right of the pips they belonged to.
        $ _pt_n = len(battle.active_press_turn_icons)
        $ _pt_w = MSBF_PRESS_TURN_ROW_X + max(1, _pt_n) * (MSBF_PRESS_TURN_SLOT_WIDTH + MSBF_PRESS_TURN_SLOT_SPACING)
        fixed:
            xpos 1232 - _pt_w
            ypos 82
            xysize (_pt_w, 20)

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
                timer 0.58 action Function(battle.clear_press_turn_fx)

    # --- Party tags, floating over their heads ------------------------------
    if _hud_on and not battle.shmup_segment_active:
        for _pi, _pm in enumerate(battle.party):
            $ _tg_active = _actor is not None and _pm.id == _actor.id
            $ _tg_targeting = pending_skill is not None
            $ _tg_targetable = _tg_targeting and battle.can_target(pending_skill, _pm)
            $ _tg_x, _tg_y = msbf_stage_tag_origin(_pi, _party_n)
            if _tg_targeting:
                button:
                    style "msbf_party_target_button"
                    xpos _tg_x
                    ypos _tg_y
                    xsize _tag_w
                    ysize _tag_h
                    sensitive _tg_targetable and committing is None
                    hover_sound MSBF_UI_SFX["hover"]
                    activate_sound MSBF_UI_SFX["accept"]
                    hovered SetScreenVariable("kb_active", False)
                    action [SetScreenVariable("hovered_skill", None), SetScreenVariable("pending_skill", None), SetScreenVariable("committing", {"skill": pending_skill, "target": _pm, "actor_index": _actor_idx, "element": pending_skill.element, "ally": True})]

                    use msbf_party_tag(_pm, _party_n, _tg_active, _tg_targetable, (_pm is _kb_focus_member))
            else:
                fixed:
                    xpos _tg_x
                    ypos _tg_y
                    xysize (_tag_w, _tag_h)
                    if _pi in _hit_set:
                        at msbf_tag_shake(_hit_w, _hit_tok)
                    use msbf_party_tag(_pm, _party_n, _tg_active, False, False)

    # The blow, on the person it happened to. Tinted by severity: a weakness or
    # a crit against you comes in gold-white rather than the ordinary red, so
    # the thing that just cost you a press turn is legible at a glance.
    if _hit_set and not _cinematic:
        $ _hit_col = (1.0, 0.86, 0.42) if battle.fx_event in ("enemy_weak", "enemy_crit") else (1.0, 0.30, 0.42)
        for _hi in _hit_set:
            if _hi < _party_n:
                $ _hx, _hy = msbf_stage_anchor(_hi, _party_n)
                use msbf_party_hit_burst(_hx, _hy + 18, _hit_w, _hit_col)

    use msbf_fx_layer(battle)

    if battle.shmup_segment_active:
        use msbf_shmup_overlay(battle)

    # =========================================================================
    # THE COMMAND DECK -- present only while you can act
    # =========================================================================
    if _deck_on:
        use msbf_hud_scrim(0, 500, 1280, 220, 0.0, 1.5)

        text "ACT" style "msbf_command_kicker":
            xpos 48
            ypos 572
        text _actor.name style "msbf_command_actor":
            xpos 48
            ypos 588
            xmaximum 210
        text "HP [_actor.hp]/[_actor.max_hp]" style "msbf_command_stats":
            xpos 48
            ypos 622
        text "MP [_actor.mp]/[_actor.max_mp]" style "msbf_command_stats":
            xpos 48
            ypos 640

        # The eight skills, as unframed chips. The element rail down the left of
        # each is the only colour on them, so the grid reads as a palette of
        # options rather than eight competing buttons.
        grid 4 2:
            xpos 286
            ypos 570
            spacing 8

            for _skill_idx, skill in enumerate(_actor.skills):
                $ _enabled = battle.can_use(skill)
                $ _skill_color = msbf_element_color(skill.element) if _enabled else "#3a4654"
                $ _kb_focused = _kb_on and pending_skill is None and _skill_idx == _kb_cur
                $ _skill_pending = pending_skill is skill

                button:
                    style "msbf_skill_button"
                    xsize 176
                    ysize 42
                    sensitive _enabled and committing is None
                    hover_sound MSBF_UI_SFX["hover"]
                    activate_sound MSBF_UI_SFX["accept"]
                    hovered [SetScreenVariable("hovered_skill", skill), SetScreenVariable("kb_active", False)]
                    unhovered SetScreenVariable("hovered_skill", None)
                    # While the keyboard owns the highlight the mouse stops
                    # painting: hover_background is pinned to the resting one so
                    # a parked pointer cannot light a second chip.
                    if kb_active:
                        hover_background Solid("#0a172699")
                    if _skill_pending:
                        background Solid("#155f88e8")
                        if kb_active:
                            hover_background Solid("#155f88e8")
                    elif _kb_focused:
                        background Solid("#0e3c58d8")
                        if kb_active:
                            hover_background Solid("#0e3c58d8")
                    if battle.skill_needs_ally_target(skill):
                        action [SetScreenVariable("hovered_skill", skill), SetScreenVariable("pending_skill", skill)]
                    else:
                        action [SetScreenVariable("hovered_skill", None), SetScreenVariable("pending_skill", None), SetScreenVariable("committing", {"skill": skill, "actor_index": _actor_idx, "element": skill.element})]
                    at msbf_button_focus

                    fixed:
                        xysize (176, 42)
                        add Solid(_skill_color) xysize (3, 26):
                            ypos 8
                        text skill.name style ("msbf_skill_name" if _enabled else "msbf_skill_name_disabled"):
                            xpos 14
                            yalign 0.5
                            xmaximum 108
                        text "[skill.cost]MP" style ("msbf_skill_cost" if _enabled else "msbf_skill_cost_disabled"):
                            xanchor 1.0
                            xpos 168
                            yalign 0.5

            for _i in range(max(0, 8 - len(_actor.skills))):
                null xsize 176 ysize 42

        if pending_skill:
            button:
                style "msbf_pass_button"
                xpos 1030
                ypos 572
                sensitive committing is None
                hover_sound MSBF_UI_SFX["hover"]
                activate_sound MSBF_UI_SFX["denied"]
                action [SetScreenVariable("pending_skill", None), SetScreenVariable("hovered_skill", None)]
                at msbf_button_focus

                text "CANCEL" style "msbf_pass_button_text"
        else:
            button:
                style "msbf_pass_button"
                xpos 1030
                ypos 572
                sensitive committing is None
                hover_sound MSBF_UI_SFX["hover"]
                action [SetScreenVariable("hovered_skill", None), Function(battle.player_pass)]
                at msbf_button_focus

                text "PASS" style "msbf_pass_button_text"

        # The tooltip follows whichever device owns the highlight, for the same
        # reason the backgrounds do: a parked pointer should not keep describing
        # a chip the keyboard cursor has already left.
        $ _kb_tip_skill = _kb_items[_kb_cur] if (_kb_on and not _kb_targeting and _kb_count) else None
        $ _tip_hover = None if kb_active else hovered_skill
        if pending_skill and not battle.result:
            text "Choose a target for [pending_skill.name]." style "msbf_tooltip":
                xpos 286
                ypos 670
                xmaximum 720
        elif _tip_hover and not battle.result:
            text _tip_hover.description style "msbf_tooltip":
                xpos 286
                ypos 670
                xmaximum 720
        elif _kb_tip_skill is not None and not battle.result:
            text _kb_tip_skill.description style "msbf_tooltip":
                xpos 286
                ypos 670
                xmaximum 720
        else:
            text "Pass spends half a turn. Haste can steal one half-turn before Matsuda changes rhythm." style "msbf_hint":
                xpos 286
                ypos 670
                xmaximum 720

    # --- Floating combat numbers, anchored to the boss or to a silhouette ----
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
                # Lifted clear of the tag: anchored dead centre the number
                # printed straight across the member's own name.
                $ _fxp, _fyp = msbf_stage_anchor(_fanchor, _party_n)
                $ _fyp = _fyp - 20
            else:
                $ _fxp = _boss_x
                $ _fyp = _boss_y - 40
            use msbf_float_number(_flabel, _fstyle, _fxp, _fyp, _fdx, _fcrit)

    # --- HP-bar damage/heal trail: a draining chip per bar change ------------
    # Polls battle.bar_events (fed by MSBFBattleState._sync_bars). The fill and
    # the numbers already snap to the true value; this bright slice over the
    # changed region drains/fades so the bar reads as animating, not snapping.
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
                $ _cbx = 48
                $ _cby = 74
                $ _cbw = 470
                $ _cbh = 11
            elif isinstance(_ba, int) and _ba < len(battle.party):
                # These MUST match the bar msbf_party_tag actually draws
                # (xpos 10, ypos = the bar offset from msbf_stage_tag_metrics,
                # width TAG_W-20, 5 tall). They used to be hand-copied literals
                # and the y drifted 10px low, which put every heal's bright fill
                # slice UNDERNEATH the bar instead of on it. Both now read the
                # same metrics function the tag itself does.
                $ _tag_ox, _tag_oy = msbf_stage_tag_origin(_ba, _party_n)
                $ _cbx = _tag_ox + 10
                $ _cby = _tag_oy + _tag_bar_y
                $ _cbw = _tag_w - 20
                $ _cbh = 5
            if _cbx is not None:
                $ _clo = min(_bfrm, _bto)
                $ _chi = max(_bfrm, _bto)
                $ _chip_x = int(_cbx + _cbw * _clo)
                $ _chip_w = max(2, int(_cbw * (_chi - _clo)))
                if _bgain:
                    add Solid("#bfffd6") xysize (_chip_w, _cbh) at msbf_bar_flash(0.5):
                        subpixel True
                        xpos _chip_x
                        ypos _cby
                else:
                    add Solid("#ffffff") xysize (_chip_w, _cbh) at msbf_bar_chip(0.5):
                        subpixel True
                        xpos _chip_x
                        ypos _cby

    # --- Player action wind-up: cast -> projectile -> impact ----------------
    # The resolve is deferred a beat so a move reads as an authored cast (charge
    # under the caster, an element-tinted bolt to the target) that LANDS on the
    # boss, instead of damage appearing on the same frame as the click.
    if committing is not None and not battle.result:
        $ _cw = 0.26
        timer _cw action [Function(battle.player_use_skill, committing["skill"], committing.get("target")), SetScreenVariable("committing", None)]

        $ _ci = committing.get("actor_index", None)
        if _ci is not None:
            $ _ccx, _ccy = msbf_stage_anchor(_ci, _party_n)
        else:
            $ _ccx = 640
            $ _ccy = 600

        $ _cel = committing.get("element", "slash")
        $ _ccolor = msbf_element_color(_cel)
        $ _crgb = msbf_hex_rgb(_ccolor)

        # Where the cast READS as going, decided by the skill's behaviour:
        #   ally -> one wounded/downed ally (single-target heal/revive)
        #   boss -> offence, debuffs, and scan (all cast AT Matsuda)
        #   self -> self/party support (buffs, guard, focus, party heals): a
        #           flare radiating from the caster, never a bolt at the boss.
        $ _ckind = committing["skill"].kind
        if _ckind in ("heal", "revive") and committing.get("target") is not None:
            $ _cdest = "ally"
        elif _ckind in ("damage", "true_damage", "fixed_damage", "dev_cleave", "debuff_defense", "debuff_attack", "blue_debuff", "analyze"):
            $ _cdest = "boss"
        else:
            $ _cdest = "self"

        use msbf_glow_pop(_ccx, _ccy, 220, 140, _crgb, 0.9, 1.7, _cw)

        if _cdest == "self":
            # Support flare radiating from the caster -- no projectile.
            use msbf_shock_ring(_ccx, _ccy, 280, _crgb, 0.12, 0.9, _cw)
        else:
            if _cdest == "ally":
                $ _ctgt = committing.get("target")
                $ _cti = battle.party.index(_ctgt) if (_ctgt is not None and _ctgt in battle.party) else None
                if _cti is not None:
                    $ _ctx, _cty = msbf_stage_anchor(_cti, _party_n)
                else:
                    $ _ctx = _ccx
                    $ _cty = _ccy
            else:
                $ _ctx = _boss_x
                $ _cty = _boss_y

            if MSBF_FX_SHADERS:
                add Solid("#00000000") xysize (104, 104) at msbf_fx_glow_t(_crgb, 0.6, 1.9), msbf_cast_projectile(_ccx, _ccy, _ctx, _cty, _cw)
                add Solid("#00000000") xysize (60, 60) at msbf_fx_glow_t(_crgb, 1.0, 1.5), msbf_cast_projectile(_ccx, _ccy, _ctx, _cty, _cw)
                add Solid("#00000000") xysize (26, 26) at msbf_fx_glow_t((1.0, 1.0, 1.0), 1.0, 2.0), msbf_cast_projectile(_ccx, _ccy, _ctx, _cty, _cw)
            else:
                add Solid(_ccolor) xysize (18, 18) at msbf_cast_projectile(_ccx, _ccy, _ctx, _cty, _cw)

    # --- THE HANDOVER BEAT ---------------------------------------------------
    # ONE screen, ONE lifetime. The directional sweep and the tempo card used to
    # be separate things on separate clocks -- the card was a screen variable
    # cleared by its own 1.30s timer while the sweep lived on handover_active --
    # so they drifted apart and the card was still up after the next side had
    # started acting.
    #
    # It is also gated on fx_event being CLEAR. handover_active goes true the
    # instant the phase's last action resolves, which is while that action is
    # still playing; drawing the sweep then put the turnover straight on top of
    # the hit that caused it. Now the impact finishes, THEN the tempo changes
    # hands, and only then does finish_handover start counting.
    if battle.handover_active and not battle.fx_event:
        use msbf_turnover_sweep(battle.handover_to or "enemy", battle.phase, battle.round_number, battle.boss.name, battle.handover_serial, getattr(battle, "handover_mp_restored", False))

    # --- KO bursts: one-shot per death, polled by serial --------------------
    if battle.death_events and not _cinematic:
        if death_seen_serial != battle.death_serial:
            timer 1.40 action [Function(battle.clear_death_events), SetScreenVariable("death_seen_serial", battle.death_serial)]
        for _de in battle.death_events:
            $ _da = _de.get("anchor", 0)
            if isinstance(_da, int):
                $ _dxp, _dyp = msbf_stage_anchor(_da, _party_n)
                use msbf_death_burst(_dxp, _dyp, "#ff3868", False)

    # Typing / quiz genre-shift QTEs render on top of the whole fight (the boss
    # scene stays visible behind their panels, unlike the bullet-hell stage).
    if battle.typing_segment_active:
        use msbf_typing_overlay(battle)
    elif battle.quiz_segment_active:
        use msbf_quiz_overlay(battle)

    # --- The two things kept behind a click ---------------------------------
    # The full log and the control reference are both reference material, not
    # live information, so neither gets to occupy the frame by default. This is
    # the whole declutter in miniature: nothing is gone, it is just not shouting.
    if _hud_on:
        if show_log:
            frame:
                xpos 48
                ypos 200
                xsize 560
                ysize 300
                background Solid("#03080ff2")
                padding (18, 14)
                viewport:
                    id "msbf_log_viewport"
                    yadjustment log_yadj
                    mousewheel True
                    draggable True
                    yinitial 1.0
                    vbox:
                        spacing 6
                        for _line in battle.log:
                            text _line style "msbf_log_line":
                                xmaximum 508

        textbutton ("HIDE LOG" if show_log else "LOG"):
            xpos 48
            ypos 712
            yanchor 1.0
            background None
            padding (0, 4)
            text_style "msbf_corner_chip"
            hover_sound MSBF_UI_SFX["hover"]
            action ToggleScreenVariable("show_log")

        if show_controls:
            frame:
                xpos 1232
                ypos 674
                xanchor 1.0
                yanchor 1.0
                background Solid("#03080ff2")
                padding (16, 12)
                vbox:
                    spacing 5
                    text "CONTROLS" size 15 color _accent outlines [(1, "#000000cc", 0, 0)]
                    text "Mouse: click any skill, target, or button." size 14 color "#c9d4df"
                    text "Z / Enter — confirm    X / L-Shift — back / pass" size 14 color "#c9d4df"
                    text "Arrows / WASD — move the command cursor" size 14 color "#c9d4df"

        textbutton ("HIDE CONTROLS" if show_controls else "CONTROLS"):
            xpos 1232
            ypos 712
            xanchor 1.0
            yanchor 1.0
            background None
            padding (0, 4)
            text_style "msbf_corner_chip"
            hover_sound MSBF_UI_SFX["hover"]
            action ToggleScreenVariable("show_controls")

    use msbf_phase_transition_overlay(battle)


screen msbf_press_turn_icon(icon, slot=0):
    $ _icon_width = 36 if icon == "full" else 18
    $ _slot_width = MSBF_PRESS_TURN_SLOT_WIDTH
    $ _icon_x = 2 if icon == "full" else int((MSBF_PRESS_TURN_SLOT_WIDTH - _icon_width) / 2)
    $ _icon_color = "#55ddff" if icon == "full" else "#55ddff99"
    $ _shimmer_travel = max(0, _icon_width - 4)
    fixed:
        xysize (_slot_width, 20)

        add Solid("#081624") xysize (_slot_width, 20)
        add Solid("#55ddff30") xysize (_slot_width, 1)
        add Solid("#ffffff10") xysize (_slot_width, 1):
            ypos 19

        if MSBF_FX_SHADERS:
            add Solid("#00000000") at msbf_fx_glow_t((0.33, 0.87, 1.0), 0.55 if icon == "full" else 0.4, 1.9):
                xcenter (_icon_x + _icon_width // 2)
                ycenter 10
                xysize (_icon_width + 18, 30)

        add Solid(_icon_color) xysize (_icon_width, 16):
            xpos _icon_x
            ypos 2
        add Solid("#ffffff24") xysize (_icon_width, 16) at msbf_press_turn_pulse(slot * 0.07):
            xpos _icon_x
            ypos 2
        add Solid("#f5fbff8a") xysize (4, 16) at msbf_press_turn_shimmer(slot * 0.10, _shimmer_travel):
            xpos _icon_x
            ypos 2
        add Solid("#ffffff70") xysize (_icon_width, 2):
            xpos _icon_x
            ypos 3
        add Solid("#ffcf6670") xysize (_icon_width, 1) at msbf_press_turn_edge(slot * 0.06):
            xpos _icon_x
            ypos 17

screen msbf_press_turn_fx_icon(event):
    $ _kind = event.get("kind", "spend")
    $ _icon_width = event.get("width", 36)
    $ _icon_x = event.get("icon_x", 2)
    $ _x = event.get("x", MSBF_PRESS_TURN_ROW_X)
    $ _base_color = "#55ddff" if event.get("icon") == "full" else "#55ddff99"

    fixed:
        xpos _x
        ypos 0
        xysize (MSBF_PRESS_TURN_SLOT_WIDTH, 20)

        if _kind == "convert":
            add Solid("#ffcf66cc") xysize (36, 16) at msbf_press_turn_convert_fx():
                xpos 2
                ypos 2
            add Solid("#f5fbffb0") xysize (18, 16) at msbf_press_turn_gain_fx(0.08):
                xpos int((MSBF_PRESS_TURN_SLOT_WIDTH - 18) / 2)
                ypos 2
        elif _kind == "gain":
            add Solid("#ffcf66aa") xysize (_icon_width, 16) at msbf_press_turn_gain_fx():
                xpos _icon_x
                ypos 2
            add Solid("#f5fbff90") xysize (MSBF_PRESS_TURN_SLOT_WIDTH, 2) at msbf_press_turn_gain_fx(0.04):
                xpos 0
                ypos 9
        else:
            add Solid(_base_color) xysize (_icon_width, 16) at msbf_press_turn_spend_fx():
                xpos _icon_x
                ypos 2
            add Solid("#ff3868b0") xysize (_icon_width, 2) at msbf_press_turn_spend_fx(0.02):
                xpos _icon_x
                ypos 9



# =============================================================================
# --- 4. STYLES --------------------------------------------------------------
# The fight's visual theme (panels, command buttons, bars, labels). Cyan/red on
# near-black, matching the rest of the mod's UI.
# =============================================================================
style msbf_title:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 32
    color "#f5fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#55ddff88", 1, 1)]

style msbf_subtitle:
    size 14
    color "#b7d8e8"
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_count_label:
    size 10
    color "#8fb1c0"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_count:
    size 28
    color "#55ddff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_roster_button is button:
    xsize 384
    ysize 96
    padding (10, 8)
    insensitive_background Solid("#050910d8")

style msbf_roster_name:
    size 18
    color "#f5fbff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_roster_role:
    size 12
    color "#55ddff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_roster_summary:
    size 11
    color "#c5d8e4"
    line_spacing 1
    outlines [(1, "#02040b", 0, 0)]

style msbf_select_panel_label:
    size 13
    color "#55ddff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_select_panel_count:
    size 12
    color "#8fb1c0"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_select_footnote:
    size 11
    color "#6f8796"
    outlines [(1, "#02040b", 0, 0)]

style msbf_order_num:
    size 18
    color "#55ddff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_order_empty_num:
    size 18
    color "#3f5060"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_order_name:
    size 16
    color "#f5fbff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_order_role:
    size 10
    color "#8fb1c0"
    outlines [(1, "#02040b", 0, 0)]

style msbf_order_empty:
    size 12
    color "#5c6c7a"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_row_button is button:
    xsize 58
    ysize 28
    background Solid("#102338")
    hover_background Solid("#1d5c82")
    insensitive_background Solid("#101923")
    padding (5, 3)

style msbf_row_button_text:
    size 10
    color "#55ddff"
    insensitive_color "#596674"
    bold True
    xalign 0.5
    yalign 0.5

style msbf_remove_button is button:
    xsize 30
    ysize 28
    background Solid("#30141e")
    hover_background Solid("#75304b")
    padding (4, 3)

style msbf_remove_button_text:
    size 12
    color "#ffd7e2"
    bold True
    xalign 0.5
    yalign 0.5

style msbf_roster_order_badge:
    size 11
    color "#55ddff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_roster_row_tag:
    size 10
    color "#ffcf66"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_roster_selected:
    size 9
    color "#55ddff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_roster_available:
    size 9
    color "#8fb1c0"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_roster_locked:
    size 9
    color "#65727c"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_select_stat_label:
    size 8
    color "#f5fbff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_hint:
    size 12
    color "#8fb1c0"
    outlines [(1, "#02040b", 0, 0)]

style msbf_begin_button is button:
    xsize 190
    ysize 48
    background Solid("#1d5c82")
    hover_background Solid("#2c7fac")
    insensitive_background Solid("#1a2630")
    padding (12, 8)

style msbf_begin_button_text:
    size 18
    color "#f5fbff"
    bold True
    xalign 0.5
    yalign 0.5

# The boss's name carries the top-left corner on its own now that there is no
# banner frame around it, so it is bigger and spaced out -- with a heavier
# outline, because it is sitting on a live environment rather than on a panel.
style msbf_boss_name:
    size 31
    color "#f5fbff"
    bold True
    kerning 1.6
    outlines [(2, "#02040bcc", 0, 0)]

# --- The unframed HUD -------------------------------------------------------
# Everything below draws directly onto the arena, so every one of these carries
# its own outline. That outline is not decoration: it is the only thing keeping
# the readout legible when the room behind it goes white on a phase break.

# The log's three lines, newest first. The fade is baked into the styles rather
# than applied as an alpha: `text` takes no alpha property, and three named
# styles say what is going on more plainly than a transform would.
style msbf_log_line_new:
    size 13
    color "#f5fbff"
    bold True
    line_spacing 2
    outlines [(2, "#02040bdd", 0, 0)]

style msbf_log_line:
    size 13
    color "#8fa6b4"
    line_spacing 2
    outlines [(2, "#02040bbb", 0, 0)]

style msbf_log_line_old:
    size 13
    color "#5b6f7d"
    line_spacing 2
    outlines [(2, "#02040b99", 0, 0)]

style msbf_tempo_kicker:
    size 13
    color "#9fb4c4"
    bold True
    kerning 1.4
    outlines [(2, "#02040bdd", 0, 0)]

style msbf_tempo_count:
    size 19
    color "#f5fbff"
    bold True
    outlines [(2, "#02040bdd", 0, 0)]

style msbf_command_kicker:
    size 11
    color "#7fa6b7"
    bold True
    kerning 1.8
    outlines [(2, "#02040bdd", 0, 0)]

# The two corner chips (LOG / CONTROLS). Deliberately the quietest text on
# screen: they are the handle on reference material, not information.
style msbf_corner_chip:
    size 12
    color "#5f7688"
    bold True
    kerning 1.2
    hover_color "#9fb4c4"
    outlines [(2, "#02040bdd", 0, 0)]

style msbf_round_badge:
    size 12
    color "#55ddff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_boss_phase:
    size 13
    color "#ff6b8e"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_stage_phase:
    size 13
    color "#ff6b8e"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_turn_actor:
    size 12
    color "#55ddff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_turn_cap:
    size 12
    color "#8fb1c0"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_turn_empty:
    size 11
    color "#8fb1c0"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_meter_text:
    size 12
    color "#c5d8e4"
    outlines [(1, "#02040b", 0, 0)]

style msbf_affinity_weak:
    size 12
    color "#ffcf66"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_affinity_resist:
    size 12
    color "#82a6ff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_affinity_unknown:
    size 12
    color "#8fb1c0"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_panel_label:
    size 12
    color "#55ddff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_deck_count:
    size 9
    color "#8fb1c0"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_log_hint:
    size 9
    color "#7fa6b7"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_log_text:
    size 11
    color "#c7dbe6"
    line_spacing 3
    outlines [(1, "#02040b", 0, 0)]

style msbf_log_text_latest:
    size 11
    color "#f5fbff"
    bold True
    line_spacing 3
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_name:
    size 14
    color "#f5fbff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_name_down:
    size 14
    color "#6b727a"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_name_compact:
    size 13
    color "#f5fbff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_name_down_compact:
    size 13
    color "#6b727a"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_role:
    size 9
    color "#8fb1c0"
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_role_compact:
    size 8
    color "#8fb1c0"
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_row_tag:
    size 9
    color "#ffcf66"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_row_tag_compact:
    size 8
    color "#ffcf66"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_stat:
    size 8
    color "#c5d8e4"
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_stat_compact:
    size 8
    color "#c5d8e4"
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_note:
    size 10
    color "#8fb1c0"
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_affinity:
    size 10
    color "#8fb1c0"
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_target_button is button:
    xsize 215
    ysize 61
    background Solid("#00000000")
    hover_background Solid("#55ddff22")
    insensitive_background Solid("#00000000")
    padding (0, 0)

style msbf_guard_tag:
    size 9
    color "#66e08a"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_guard_tag_compact:
    size 8
    color "#66e08a"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_focus_tag:
    size 9
    color "#ffcf66"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_focus_tag_compact:
    size 8
    color "#ffcf66"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_down_text:
    size 9
    color "#ff3868"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_down_text_compact:
    size 8
    color "#ff3868"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_command_actor:
    size 20
    color "#f5fbff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_command_stats:
    size 12
    color "#c5d8e4"
    outlines [(1, "#02040b", 0, 0)]

# The skill chips lost their bracketed frames. On the old boxed deck the frame
# was what separated a button from the panel behind it; on the arena the scrim
# already does that, so a border here just adds a second edge for the eye to
# trip over. A flat wash, a brighter wash on hover, and the element rail the
# screen draws down the left are the whole of it.
style msbf_skill_button is button:
    xsize 176
    ysize 42
    background Solid("#0a172699")
    hover_background Solid("#164a6ce6")
    insensitive_background Solid("#06090f77")
    padding (8, 5)

style msbf_skill_button_text:
    size 11
    color "#f5fbff"
    insensitive_color "#596674"
    bold True
    xalign 0.5
    yalign 0.5

style msbf_skill_name:
    size 11
    color "#f5fbff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_skill_cost:
    size 10
    color "#d9ecf5"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_skill_name_disabled:
    size 11
    color "#596674"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_skill_cost_disabled:
    size 10
    color "#46515d"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_pass_button is button:
    xsize 108
    ysize 42
    background Solid("#12354e99")
    hover_background Solid("#1e6690e6")
    padding (10, 4)

style msbf_pass_button_text:
    size 13
    color "#f5fbff"
    bold True
    xalign 0.5
    yalign 0.5

style msbf_tooltip:
    size 12
    color "#d9ecf5"
    outlines [(1, "#02040b", 0, 0)]

style msbf_fx_weak:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 42
    color "#ffcf66"
    bold True
    outlines [(3, "#02040b", 0, 0), (1, "#ffffffcc", 0, 0)]

style msbf_fx_crit:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 42
    color "#ffffff"
    bold True
    outlines [(3, "#02040b", 0, 0), (1, "#ff3868cc", 0, 0)]

style msbf_fx_resist:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 38
    color "#9aa7b7"
    bold True
    outlines [(3, "#02040b", 0, 0)]

style msbf_fx_heal:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 36
    color "#66e08a"
    bold True
    outlines [(3, "#02040b", 0, 0)]

style msbf_fx_scan:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 38
    color "#55ddff"
    bold True
    outlines [(3, "#02040b", 0, 0), (1, "#ffffffaa", 0, 0)]

style msbf_fx_phase:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 50
    color "#ff3868"
    bold True
    outlines [(4, "#02040b", 0, 0), (1, "#ffffffaa", 0, 0)]

style msbf_phase_transition_title:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 56
    color "#ffffff"
    bold True
    outlines [(5, "#02040b", 0, 0), (2, "#ff3868cc", 0, 0), (1, "#ffcf66aa", 0, 0)]

style msbf_phase_transition_subtitle:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 25
    color "#f5fbff"
    bold True
    outlines [(3, "#02040b", 0, 0), (1, "#55ddffaa", 0, 0)]

# ---- Phase-1 entrance cinematic ----------------------------------------------
# Title uses the default (narrower) font on purpose: the full name
# "Matsuda, Crimson-Azure" overflows in the wide Extended face.
style msbf_intro_kicker:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 20
    color "#ffcf66"
    bold True
    kerning 6.0
    outlines [(3, "#02040b", 0, 0), (1, "#ff3868aa", 0, 0)]

style msbf_intro_title_text:
    size 52
    color "#ffffff"
    bold True
    kerning 1.0
    outlines [(5, "#02040b", 0, 0), (2, "#ff3868cc", 0, 0), (1, "#ffcf66aa", 0, 0)]

style msbf_intro_skip_hint:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 13
    color "#7c93ad"
    bold True
    kerning 2.0
    outlines [(2, "#02040b", 0, 0)]

# ---- Floating combat numbers -------------------------------------------------
style msbf_float_dmg:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 27
    color "#f5fbff"
    bold True
    outlines [(3, "#02040b", 0, 0)]

style msbf_float_crit:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 40
    color "#ffffff"
    bold True
    outlines [(4, "#02040b", 0, 0), (2, "#ff3868dd", 0, 0)]

style msbf_float_weak:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 33
    color "#ffcf66"
    bold True
    outlines [(3, "#02040b", 0, 0), (1, "#ffffffcc", 0, 0)]

style msbf_float_resist:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 22
    color "#9aa7b7"
    bold True
    outlines [(3, "#02040b", 0, 0)]

style msbf_float_heal:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 27
    color "#66e08a"
    bold True
    outlines [(3, "#02040b", 0, 0), (1, "#ffffff88", 0, 0)]

style msbf_float_enemy:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 27
    color "#ff6b8e"
    bold True
    outlines [(3, "#02040b", 0, 0)]

style msbf_float_miss:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 23
    color "#c4d4e0"
    bold True
    outlines [(3, "#02040b", 0, 0)]
