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

transform msbf_phase_transition_blackout:
    alpha 1.0
    pause 0.74
    linear 0.035 alpha 0.72
    linear 0.045 alpha 1.0
    pause 0.25
    linear 0.055 alpha 0.54
    linear 0.040 alpha 0.92
    linear 0.42 alpha 0.0

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

# ---- Phase-1 boss entrance cinematic (msbf_battle_intro_overlay) -------------

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

# Compatibility entry point: all Seer backgrounds resolve to the same three
# illustrated rooms. Keep the existing signature for callers; phase-specific
# atmosphere is owned by the shared environment instead of old backdrop art.
screen msbf_battle_backdrop(dim="#02050ab8", phase=1, wind=False):
    use msbf_seer_environment(phase, getattr(store, "_msbf_id_mode", False))
    add Solid(dim)
screen msbf_phase2_boom_overlay(kind=0):
    $ _boom_kind = kind % 3
    $ _pressure_color = ["#000000", "#17030a", "#02131d"][_boom_kind]
    $ _accent_a = ["#ff3868", "#ffcf66", "#55ddff"][_boom_kind]
    $ _accent_b = ["#55ddff", "#ff3868", "#ffcf66"][_boom_kind]

    add Solid(_pressure_color) at msbf_t(msbf_phase2_boom_pressure, 0.48)
    add Solid("#000000") xysize (1280, 34) at msbf_t(msbf_phase2_boom_scan, 0.00, 0.30, 1.0):
        ypos 82
    add Solid("#000000") xysize (1280, 42) at msbf_t(msbf_phase2_boom_scan, 0.06, 0.26, -1.0):
        ypos 608
    add Solid(_accent_a) xysize (1280, 5) at msbf_t(msbf_phase2_boom_wave, -9.0, 0.02, 0.38):
        xcenter 640
        ycenter 338
    add Solid(_accent_b) xysize (1280, 4) at msbf_t(msbf_phase2_boom_wave, 13.0, 0.07, 0.32):
        xcenter 640
        ycenter 380
    add Solid("#000000") xysize (360, 900) at msbf_t(msbf_phase2_boom_slab, -18.0, 0.04, 0.34, 1.0):
        xcenter 640
        ycenter 360
    add Solid(_accent_a) xysize (180, 900) at msbf_t(msbf_phase2_boom_slab, 27.0, 0.10, 0.24, -1.0):
        xcenter 640
        ycenter 360
    add Solid(_accent_b) xysize (1040, 3) at msbf_t(msbf_phase2_boom_wave, -34.0, 0.15, 0.26):
        xcenter 640
        ycenter 360

screen msbf_phase3_rupture_overlay(kind=0):
    $ _rupture_kind = kind % 3
    $ _accent_a = ["#ff3868", "#ffffff", "#a66bff"][_rupture_kind]
    $ _accent_b = ["#f5fbff", "#ff3868", "#ff6b9f"][_rupture_kind]

    add Solid("#050007") at msbf_t(msbf_phase3_pressure, 0.0, 0.42)
    add Solid(_accent_a) xysize (1280, 5) at msbf_t(msbf_phase3_fault_line, -29.0, 0.00, 0.70, 1.0):
        xcenter 640
        ycenter 274
    add Solid(_accent_b) xysize (1280, 4) at msbf_t(msbf_phase3_fault_line, 17.0, 0.06, 0.58, -1.0):
        xcenter 640
        ycenter 398
    add Solid(_accent_b) xysize (760, 5) at msbf_t(msbf_phase3_tornado_streak, 640, 360, 620, 178, 0.02, 0.46, 1.0)
    add Solid(_accent_a) xysize (640, 5) at msbf_t(msbf_phase3_tornado_streak, 640, 382, 540, 206, 0.10, 0.38, -1.0)
    add Solid("#000000ee") xysize (58, 12) at msbf_t(msbf_phase3_tornado_debris, 640, 360, 640, 210, 0.00, 0.72, 1.0, 1.28)
    add Solid(_accent_a) xysize (42, 10) at msbf_t(msbf_phase3_tornado_debris, 640, 344, 540, 156, 0.08, 0.70, -1.0, 1.12)
    add Solid("#ffffffcc") xysize (28, 8) at msbf_t(msbf_phase3_tornado_debris, 640, 392, 600, 236, 0.16, 0.64, 1.0, 0.96)
    add Solid("#ffffff66") xysize (1280, 2) at msbf_t(msbf_phase3_static_slice, 0.02, 0.48, 1.0):
        ypos 98
    add Solid("#ff386866") xysize (1280, 5) at msbf_t(msbf_phase3_static_slice, 0.11, 0.44, -1.0):
        ypos 612

# --- Extra "breathing + flair" transforms for breaks / reveals / death. ---

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
            add Solid("#00000000") xysize (1500, 1500) at msbf_t(msbf_nova_inring_r, 0.00, (1.0, 1.0, 1.0), 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (1500, 1500) at msbf_t(msbf_nova_inring_r, 0.12, (1.0, 0.22, 0.41), 0.6):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (1500, 1500) at msbf_t(msbf_nova_inring_r, 0.24, (0.65, 0.42, 1.0), 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (1500, 1500) at msbf_t(msbf_nova_inring_r, 0.38, (0.33, 0.87, 1.0), 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (1500, 1500) at msbf_t(msbf_nova_inring_r, 0.52, (1.0, 0.81, 0.40), 0.55):
                xcenter _nx
                ycenter _ny
        else:
            add Solid("#ffffff") xysize (1400, 4) at msbf_t(msbf_nova_inring, 0.00, 1.0, 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#ff3868") xysize (1400, 5) at msbf_t(msbf_nova_inring, 0.12, -1.0, 0.6):
                xcenter _nx
                ycenter _ny
            add Solid("#a66bff") xysize (1400, 4) at msbf_t(msbf_nova_inring, 0.24, 1.0, 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#55ddff") xysize (1400, 3) at msbf_t(msbf_nova_inring, 0.38, -1.0, 0.5):
                xcenter _nx
                ycenter _ny
            add Solid("#ffcf66") xysize (1400, 4) at msbf_t(msbf_nova_inring, 0.52, 1.0, 0.55):
                xcenter _nx
                ycenter _ny
        # gathering core
        if MSBF_FX_SHADERS:
            add Solid("#00000000") xysize (520, 520) at msbf_t(msbf_nova_core_glow, 0.04, (1.0, 1.0, 1.0)):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (300, 300) at msbf_t(msbf_nova_core_glow, 0.09, (1.0, 0.90, 0.75)):
                xcenter _nx
                ycenter _ny
        else:
            add Solid("#ffffff") xysize (520, 520) at msbf_t(msbf_nova_core, 0.04):
                xcenter _nx
                ycenter _ny
            add Solid("#ffe6c0") xysize (300, 300) at msbf_t(msbf_nova_core, 0.09):
                xcenter _nx
                ycenter _ny
        # DETONATION flash
        add Solid("#ffffff") at msbf_t(msbf_nova_flash, 0.84, 1.0)
        add Solid("#fff4dc") at msbf_t(msbf_nova_flash, 0.90, 0.7)
        add Solid("#ff3868") at msbf_t(msbf_nova_flash, 0.86, 0.45)
        # outward shockwaves
        if MSBF_FX_SHADERS:
            add Solid("#00000000") xysize (2000, 2000) at msbf_t(msbf_big_shock_r, 0.84, (1.0, 1.0, 1.0), 0.95):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (2000, 2000) at msbf_t(msbf_big_shock_r, 0.92, (1.0, 0.22, 0.41), 0.72):
                xcenter _nx
                ycenter _ny
            add Solid("#00000000") xysize (2000, 2000) at msbf_t(msbf_big_shock_r, 1.05, (1.0, 0.81, 0.40), 0.5):
                xcenter _nx
                ycenter _ny
        else:
            add Solid("#ffffff") xysize (1500, 1500) at msbf_t(msbf_big_shock, 0.84, 0.95):
                xcenter _nx
                ycenter _ny
            add Solid("#ff3868") xysize (1500, 1500) at msbf_t(msbf_big_shock, 0.92, 0.72):
                xcenter _nx
                ycenter _ny
            add Solid("#ffcf66") xysize (1500, 1500) at msbf_t(msbf_big_shock, 1.05, 0.5):
                xcenter _nx
                ycenter _ny
        # blast jets firing out of the detonation
        add Solid("#ffffff") xysize (1500, 13) at msbf_t(msbf_phase_break_lance, -7.0, 0.85, 1.0):
            xcenter _nx
            ycenter _ny
        add Solid("#ff3868") xysize (1400, 10) at msbf_t(msbf_phase_break_lance, 20.0, 0.88, 0.82):
            xcenter _nx
            ycenter _ny
        add Solid("#a66bff") xysize (1320, 7) at msbf_t(msbf_phase_transition_lance, -30.0, 0.95, 0.7):
            xcenter _nx
            ycenter _ny
        # whiteout blooms out from the detonation point and fills the screen
        add Solid("#ffffff") xysize (1600, 1600) at msbf_t(msbf_nova_whiteout, 0.86):
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
            add Solid("#00000000") xysize (1280, 720) at msbf_t(msbf_defeat_postfx, (0.17, 0.015, 0.04))
            add Solid("#00000000") xysize (920, 780) at msbf_t(msbf_defeat_loom_glow, (0.82, 0.10, 0.20)):
                xcenter _dnx
                ycenter _dny
        add Solid("#12000a") at msbf_defeat_pulse
        add Solid("#000000") xysize (1280, 460) at msbf_t(msbf_defeat_letterbox_top, 1.75):
            ypos 0
            yanchor 0.0
        add Solid("#000000") xysize (1280, 460) at msbf_t(msbf_defeat_letterbox_bottom, 1.75):
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
# with "down"), help (F1) and the progress screen (F2). Bindings below use
# named keymap actions, so their physical keys follow the active configuration.
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
# This screen consumes focus_left/right/up/down before applying its own cursor
# movement, preventing a second engine focus highlight. enter_m_input_lock leaves
# those actions available for screens such as Monika's date that use native focus.
# Dismiss/activate remain available; Enter and clicks still work.
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
    # Since the Sep 30 2026 facelift the IMPACT itself -- the burst, the
    # slash, the ring, the element -- is drawn by the pixel stage on the same
    # pixel grid as the sprites it lands on (MSBFPixelStage._on_event). The
    # smooth glow pops and the Solid "slash" bars that used to live here sat
    # on top of the pixel art, washed the boss out entirely on a crit and
    # read as a different game. What is left is the screen-wide flash and the
    # call-out word, which are interface, not world.
    if battle.fx_event and battle.fx_event not in ("phase_blackout", "phase", "final_victory", "final_defeat"):
        timer battle.fx_clear_delay action Function(battle.clear_fx)

        $ _fxb_x, _fxb_y = msbf_boss_anchor(battle.phase)
        # Call-outs sit up and to her LEFT -- toward the party, clear of her
        # face and of the nameplate over her.
        $ _fxt_x = _fxb_x - 250
        $ _fxt_y = _fxb_y - 120
        $ _fxp_x, _fxp_y = msbf_stage_anchor(0, len(battle.party))

        if battle.fx_event in ("weak", "enemy_weak"):
            add Solid("#ffcf6630") at msbf_t(msbf_fx_flash, "#ffcf66", 0.18)
            text "WEAK" style "msbf_fx_weak" at msbf_fx_text:
                xcenter (_fxt_x if battle.fx_event == "weak" else _fxp_x + 120)
                ycenter (_fxt_y if battle.fx_event == "weak" else _fxp_y - 150)
        elif battle.fx_event in ("crit", "enemy_crit"):
            add Solid("#ffffff3c") at msbf_t(msbf_fx_flash, "#ffffff", 0.22)
            text "CRITICAL" style "msbf_fx_crit" at msbf_fx_text_big:
                xcenter (_fxt_x if battle.fx_event == "crit" else _fxp_x + 140)
                ycenter (_fxt_y if battle.fx_event == "crit" else _fxp_y - 150)
        elif battle.fx_event == "miss":
            text "MISS" style "msbf_fx_resist" at msbf_fx_text:
                xcenter _fxt_x
                ycenter _fxt_y
        elif battle.fx_event in ("resist", "enemy_resist"):
            text "RESIST" style "msbf_fx_resist" at msbf_fx_text:
                xcenter _fxt_x
                ycenter _fxt_y
        elif battle.fx_event == "revive":
            add Solid("#66e08a30") at msbf_t(msbf_fx_flash, "#66e08a", 0.18)
            text "REVIVE" style "msbf_fx_heal" at msbf_fx_text:
                xcenter _fxp_x + 60
                ycenter _fxp_y - 170
        elif battle.fx_event == "shuffle":
            add Solid("#55ddff38") at msbf_t(msbf_fx_flash, "#55ddff", 0.26)
            text "AFFINITY SHIFT" style "msbf_fx_scan" at msbf_fx_text_big:
                xcenter _fxt_x
                ycenter _fxt_y - 40
        elif battle.fx_event == "victory":
            add Solid("#55ddff3a") at msbf_t(msbf_fx_flash, "#55ddff", 0.26)
            text "CLEAR" style "msbf_fx_scan" at msbf_fx_text_big:
                xcenter _fxt_x
                ycenter _fxt_y - 40
        elif battle.fx_event == "defeat":
            add Solid("#1a0206") at msbf_t(msbf_fx_flash, "#1a0206", 0.50)
            text "DOWN" style "msbf_fx_phase" at msbf_fx_text_big:
                xcenter _fxt_x
                ycenter _fxt_y - 40
        elif battle.fx_event in ("enemy_aoe",):
            add Solid("#ff386824") at msbf_t(msbf_fx_flash, "#ff3868", 0.18)
        elif battle.fx_event in ("enemy", "enemy_hit", "enemy_guard"):
            add Solid("#ff38681c") at msbf_t(msbf_fx_flash, "#ff3868", 0.12)


# -----------------------------------------------------------------------------
# msbf_keyboard_notice: pre-fight input notice. Styled after Hina's World content
# notice: black matte, Win9x-style title bar, white body, gray button tray.
# -----------------------------------------------------------------------------
screen msbf_keyboard_notice():
    style_prefix "hw"
    modal True
    use enter_m_input_lock()
    key "game_menu" action Show("msbf_pause_menu", prefight=True)
    key "K_ESCAPE" action Show("msbf_pause_menu", prefight=True)
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
                        id "msbf_notice_continue"
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
#   * bullets are the shared pixel sprites in assets/bullets/ (dagger.png,
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

    add Solid("#040710b8")

    # Prominent top countdown bar.
    add Solid("#12060c") xpos 0 ypos 0 xsize 1280 ysize 14
    add Solid("#ff3868") xpos 0 ypos 0 ysize 14 at msbf_t(msbf_qte_drain, battle.typing_time_limit)
    add Solid("#ff3868") xpos 0 ypos 14 xsize 1280 ysize 2 at msbf_qte_timer_throb

    frame:
        xalign 0.5
        yalign 0.5
        xsize 880
        background msbf_seer_frame()
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

    add Solid("#040710b8")

    add Solid("#12060c") xpos 0 ypos 0 xsize 1280 ysize 14
    add Solid("#ff3868") xpos 0 ypos 0 ysize 14 at msbf_t(msbf_qte_drain, battle.quiz_time_limit)
    add Solid("#ff3868") xpos 0 ypos 14 xsize 1280 ysize 2 at msbf_qte_timer_throb

    vbox:
        xalign 0.5
        yalign 0.5
        xsize 940
        spacing 14

        text "GENRE SHIFT || MULTIPLE CHOICE" xalign 0.5 size 20 color "#ff8fb0" outlines [(2, "#000000cc", 0, 0)]

        frame:
            xfill True
            background msbf_seer_frame()
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
                    background msbf_seer_frame(_q_sel, True)
                    hover_background msbf_seer_frame(True, True)
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
# msbf_battle_screen(battle) -- THE fight -- lives in seer_battle.rpy since the
# Sep 30 2026 Seer facelift, beside the pixel stage it draws the world through
# (pixel_stage.rpy). The pre-facelift screen is preserved in the snapshot
# ENTER-M-backups/20260930-seer-facelift-before for reference.
# -----------------------------------------------------------------------------


# These emblems retain the battle's 40px slot and 4px spacing. A half turn is
# one dark facet inside the same bezel, rather than a resized rectangular bar.
transform msbf_press_turn_luster(delay=0.0):
    alpha 0.88
    pause delay
    block:
        ease 1.1 alpha 1.0
        ease 1.3 alpha 0.88
        repeat

screen msbf_press_turn_icon(icon, slot=0):
    $ _turn_asset = "turn_full.png" if icon == "full" else "turn_half.png"
    fixed:
        xysize (MSBF_PRESS_TURN_SLOT_WIDTH, 32)
        add (MSBF_SEER_ART + _turn_asset) at msbf_t(msbf_press_turn_luster, slot * 0.07):
            xpos 2
            ypos 0
            xysize (36, 32)

screen msbf_press_turn_fx_icon(event):
    $ _kind = event.get("kind", "spend")
    $ _x = event.get("x", MSBF_PRESS_TURN_ROW_X)
    fixed:
        xpos _x
        ypos 0
        xysize (MSBF_PRESS_TURN_SLOT_WIDTH, 32)
        # Event slot coordinates and the original one-shot lifetimes remain
        # authoritative. Only their pictures change; no new game-state timer.
        if _kind == "convert":
            add (MSBF_SEER_ART + "turn_full.png") at msbf_t(msbf_press_turn_convert_fx):
                xpos 2
                xysize (36, 32)
            add (MSBF_SEER_ART + "turn_half.png") at msbf_t(msbf_press_turn_gain_fx, 0.08):
                xpos 2
                xysize (36, 32)
        elif _kind == "gain":
            add (MSBF_SEER_ART + "turn_gain.png") at msbf_t(msbf_press_turn_gain_fx):
                xpos 2
                xysize (36, 32)
        else:
            add (MSBF_SEER_ART + "turn_spent.png") at msbf_t(msbf_press_turn_spend_fx):
                xpos 2
                xysize (36, 32)


# =============================================================================
# --- 4. STYLES --------------------------------------------------------------
# The fight's visual theme (panels, command buttons, bars, labels). Cyan/red on
# near-black, matching the rest of the mod's UI.
# =============================================================================

# --- HUD readouts -----------------------------------------------------------
# Modest outlines retain legibility where tags and action FX cross the world.

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
