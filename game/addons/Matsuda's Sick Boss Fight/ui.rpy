image msbf_matsuda_phase1 = Transform("addons/Matsuda's Sick Boss Fight/phase1.png", fit="contain", xysize=(620, 430))
image msbf_matsuda_phase2 = Transform("addons/Matsuda's Sick Boss Fight/phase2.png", fit="contain", xysize=(735, 430))
image msbf_matsuda_phase3 = Transform("addons/Matsuda's Sick Boss Fight/idmode/idphase.png", fit="contain", xysize=(735, 430))
image msbf_rupture_backdrop = Transform("addons/Matsuda's Sick Boss Fight/idmode/rupture.png", fit="cover", xysize=(1280, 720))
image msbf_rupture_stage = Transform("addons/Matsuda's Sick Boss Fight/idmode/rupture.png", fit="cover", xysize=(786, 458))

init -1 python:
    import math

    MSBF_PHASE2_BOSS_MOTION_FPS = 20.0
    MSBF_PHASE3_BOSS_MOTION_FPS = 24.0

    def msbf_phase2_boss_anchor(tick):
        t = float(tick) / MSBF_PHASE2_BOSS_MOTION_FPS
        x = 393 + int(round(math.sin(t * 0.52) * 36.0 + math.sin(t * 0.21 + 1.0) * 10.0))
        y = 240 + int(round(math.sin(t * 0.74 + 0.6) * 4.0 + math.sin(t * 0.31) * 2.0))
        return x, y

    def msbf_phase3_boss_anchor(tick):
        t = float(tick) / MSBF_PHASE3_BOSS_MOTION_FPS
        x = 393 + int(round(
            math.sin(t * 0.83 + 0.4) * 46.0 +
            math.sin(t * 1.91 + 1.2) * 23.0 +
            math.sin(t * 3.27) * 9.0
        ))
        y = 234 + int(round(
            math.sin(t * 1.12 + 0.7) * 20.0 +
            math.sin(t * 2.42 + 1.9) * 10.0 +
            math.sin(t * 4.10) * 4.0
        ))
        return x, y

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

transform msbf_phase2_starstream(angle=0.0, delay=0.0, alpha_max=0.20, direction=1.0, speed=4.0, y=360):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 640 - (1060 * direction)
    ypos y
    rotate angle
    alpha 0.0
    pause delay
    block:
        xpos 640 - (1060 * direction)
        alpha 0.0
        linear 0.28 alpha alpha_max
        linear speed xpos 640 + (1060 * direction) alpha 0.0
        pause 0.80
        repeat

transform msbf_scanline(delay=0.0, alpha_max=0.18):
    xpos 0
    ypos 0
    alpha 0.0
    pause delay
    block:
        ypos 0
        alpha 0.0
        linear 0.18 alpha alpha_max
        linear 2.2 ypos 720
        linear 0.18 alpha 0.0
        pause 1.4
        repeat

transform msbf_bg_crossbeam(angle=-12.0, delay=0.0, alpha_max=0.15):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos -180
    ypos 360
    rotate angle
    alpha 0.0
    pause delay
    block:
        xpos -180
        alpha 0.0
        linear 0.40 alpha alpha_max
        linear 4.20 xpos 1460 alpha 0.0
        pause 2.10
        repeat

transform msbf_phase2_bg_pulse(delay=0.0, alpha_max=0.14):
    alpha 0.0
    pause delay
    block:
        linear 0.06 alpha alpha_max
        linear 0.18 alpha 0.0
        pause 0.42
        linear 0.04 alpha alpha_max * 0.62
        linear 0.12 alpha 0.0
        pause 1.05
        repeat

transform msbf_phase2_bg_shard(angle=-18.0, delay=0.0, alpha_max=0.20, direction=1.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 640 - (920 * direction)
    ypos 360
    rotate angle
    alpha 0.0
    pause delay
    block:
        xpos 640 - (920 * direction)
        alpha 0.0
        linear 0.06 alpha alpha_max
        linear 0.46 xpos 640 + (920 * direction) alpha 0.0
        pause 0.55
        repeat

transform msbf_phase2_scanline_burst(delay=0.0):
    subpixel True
    xoffset -18
    alpha 0.0
    pause delay
    block:
        xoffset -18
        linear 0.04 alpha 0.34 xoffset 16
        linear 0.06 alpha 0.0 xoffset -8
        pause 0.36
        linear 0.03 alpha 0.24 xoffset 22
        linear 0.05 alpha 0.0 xoffset 0
        pause 1.10
        repeat

transform msbf_phase2_white_rift(angle=0.0, delay=0.0, alpha_max=0.34):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    rotate angle
    alpha 0.0
    zoom 0.82
    pause delay
    block:
        linear 0.05 alpha alpha_max zoom 1.0
        linear 0.07 alpha 0.04 zoom 1.22
        pause 0.14
        linear 0.04 alpha alpha_max * 0.74
        linear 0.18 alpha 0.0 zoom 1.42
        pause 2.15
        repeat

transform msbf_phase2_collapse_bar(angle=0.0, delay=0.0, alpha_max=0.24, direction=1.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 640 - (900 * direction)
    ypos 360
    rotate angle
    alpha 0.0
    zoom 0.94
    pause delay
    block:
        xpos 640 - (900 * direction)
        alpha 0.0
        zoom 0.94
        linear 0.08 alpha alpha_max zoom 1.0
        linear 0.62 xpos 640 + (900 * direction) alpha 0.0 zoom 1.15
        pause 0.95
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

transform msbf_phase_break_blackout:
    alpha 0.0
    pause 0.18
    linear 0.07 alpha 1.0

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

transform msbf_phase_transition_breathe:
    alpha 0.0
    zoom 0.96
    linear 0.22 alpha 0.92 zoom 1.0
    pause 0.64
    linear 0.42 alpha 0.0 zoom 1.04

transform msbf_final_victory_rumble(strength=1.0, delay=1.42):
    subpixel True
    xoffset 0
    yoffset 0
    pause delay
    block:
        linear 0.030 xoffset -5 * strength yoffset 3 * strength
        linear 0.030 xoffset 6 * strength yoffset -2 * strength
        linear 0.035 xoffset -4 * strength yoffset -3 * strength
        linear 0.030 xoffset 5 * strength yoffset 2 * strength
        linear 0.045 xoffset -2 * strength yoffset 1 * strength
        repeat

transform msbf_final_victory_whiteout:
    alpha 0.0
    pause 1.64
    easein_quad 5.10 alpha 1.0

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

transform msbf_phase3_debris(angle=0.0, delay=0.0, alpha_max=0.36, direction=1.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 640 - (760 * direction)
    ypos 360
    rotate angle
    alpha 0.0
    zoom 0.78
    pause delay
    block:
        xpos 640 - (760 * direction)
        yoffset 80
        alpha 0.0
        linear 0.06 alpha alpha_max zoom 1.02 yoffset -16
        linear 0.54 xpos 640 + (760 * direction) yoffset -118 alpha 0.0 zoom 1.24 rotate angle + (18.0 * direction)
        pause 0.46
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

transform msbf_boss_idle:
    subpixel True
    alpha 1.0
    xoffset 0
    yoffset 0
    zoom 1.0
    rotate 0.0
    parallel:
        easein 1.35 yoffset -8
        easeout 1.35 yoffset 2
        ease 0.70 yoffset 0
        repeat
    parallel:
        ease 1.80 xoffset -4 rotate -0.35
        ease 2.10 xoffset 4 rotate 0.35
        ease 1.20 xoffset 0 rotate 0.0
        repeat
    parallel:
        ease 1.70 zoom 1.012
        ease 1.70 zoom 0.998
        repeat

transform msbf_boss_hit:
    subpixel True
    alpha 1.0
    xoffset 0
    yoffset 0
    zoom 1.0
    rotate 0.0
    linear 0.03 xoffset -24 yoffset 8 zoom 1.035 rotate -1.8
    linear 0.04 xoffset 22 yoffset -5 rotate 1.2
    linear 0.05 xoffset -10 yoffset 2 rotate -0.6
    easeout 0.12 xoffset 0 yoffset 0 zoom 1.0 rotate 0.0

transform msbf_boss_cast:
    subpixel True
    alpha 1.0
    xoffset 0
    zoom 1.0
    yoffset 0
    rotate 0.0
    easeout 0.10 zoom 1.075 yoffset -26 rotate -1.0 alpha 0.92
    linear 0.04 xoffset -8
    linear 0.04 xoffset 10
    easein 0.16 xoffset 0 zoom 1.0 yoffset 0 rotate 0.0 alpha 1.0

transform msbf_boss_phase_idle:
    subpixel True
    alpha 1.0
    xoffset 0
    yoffset 0
    zoom 1.0
    rotate 0.0
    parallel:
        ease 4.2 zoom 1.018
        ease 5.0 zoom 0.998
        ease 3.8 zoom 1.010
        repeat
    parallel:
        pause 1.40
        linear 0.035 alpha 0.78
        linear 0.070 alpha 1.0
        pause 2.20
        linear 0.025 alpha 0.88
        linear 0.055 alpha 1.0
        pause 1.35
        repeat

transform msbf_boss_phase_break:
    subpixel True
    alpha 0.0
    xoffset 0
    yoffset 34
    zoom 0.92
    rotate 0.0
    linear 0.08 alpha 1.0 yoffset -24 zoom 1.12 rotate -1.2
    linear 0.05 xoffset -22 alpha 0.82
    linear 0.05 xoffset 22 alpha 1.0
    linear 0.06 xoffset -12 rotate 1.0
    easeout 0.18 xoffset 0 yoffset 0 zoom 1.035 rotate 0.0
    ease 0.28 zoom 1.0

transform msbf_boss_shuffle:
    subpixel True
    alpha 0.68
    xoffset -34
    yoffset 0
    zoom 1.025
    rotate -0.8
    linear 0.04 alpha 0.24 xoffset 28
    linear 0.04 alpha 0.90 xoffset -16 rotate 0.7
    linear 0.05 alpha 0.38 xoffset 18
    easeout 0.16 alpha 1.0 xoffset 0 zoom 1.0 rotate 0.0

transform msbf_boss_echo(side=1, delay=0.0):
    subpixel True
    alpha 0.0
    xoffset side * 14
    yoffset 4
    zoom 1.02
    pause delay
    linear 0.05 alpha 0.22
    linear 0.18 alpha 0.0 xoffset side * 38 yoffset -6 zoom 1.06

transform msbf_boss_phase_echo(side=1, delay=0.0):
    subpixel True
    alpha 0.0
    xoffset side * 18
    yoffset 0
    zoom 1.01
    pause delay
    block:
        alpha 0.0
        xoffset side * 18
        yoffset 0
        zoom 1.01
        linear 0.20 alpha 0.16
        linear 0.42 alpha 0.0 xoffset side * 30 yoffset -10 zoom 1.055
        pause 1.10
        repeat

transform msbf_boss_phase_afterimage(xdrift=24, ydrift=-12, delay=0.0, alpha_max=0.16):
    subpixel True
    alpha 0.0
    xoffset 0
    yoffset 0
    zoom 1.018
    rotate 0.0
    pause delay
    block:
        alpha 0.0
        xoffset 0
        yoffset 0
        zoom 1.018
        rotate 0.0
        linear 0.06 alpha alpha_max xoffset xdrift * 0.28 yoffset ydrift * 0.28
        linear 0.30 alpha 0.0 xoffset xdrift yoffset ydrift zoom 1.075 rotate xdrift * 0.025
        pause 0.64
        repeat

transform msbf_boss_rupture_backlight:
    subpixel True
    alpha 0.0
    zoom 1.0
    rotate 0.0
    parallel:
        block:
            linear 0.05 alpha 0.32 zoom 1.08
            linear 0.09 alpha 0.08 zoom 1.18
            pause 0.20
            linear 0.04 alpha 0.24
            linear 0.14 alpha 0.05 zoom 1.04
            pause 0.66
            repeat
    parallel:
        linear 0.44 rotate -4.0
        linear 0.32 rotate 6.0
        linear 0.58 rotate -2.0
        repeat

transform msbf_boss_rupture_idle:
    subpixel True
    alpha 1.0
    xoffset 0
    yoffset 0
    zoom 1.0
    rotate 0.0
    parallel:
        block:
            ease 0.22 xoffset -12 yoffset 6 rotate -0.8
            ease 0.18 xoffset 9 yoffset -7 rotate 0.7
            easeout 0.30 xoffset -3 yoffset 2 rotate -0.25
            pause 0.12
            ease 0.20 xoffset 13 yoffset -3 rotate 0.9
            ease 0.34 xoffset 0 yoffset 0 rotate 0.0
            pause 0.18
            repeat
    parallel:
        block:
            linear 0.05 alpha 0.76
            linear 0.10 alpha 1.0
            pause 0.34
            linear 0.04 alpha 0.84
            linear 0.08 alpha 1.0
            pause 0.78
            repeat
    parallel:
        block:
            ease 0.42 zoom 1.045
            linear 0.04 zoom 0.982
            ease 0.50 zoom 1.018
            pause 0.28
            repeat

transform msbf_boss_rupture_afterimage(xdrift=42, ydrift=-28, delay=0.0, alpha_max=0.22):
    subpixel True
    alpha 0.0
    xoffset 0
    yoffset 0
    zoom 1.02
    rotate 0.0
    pause delay
    block:
        linear 0.035 alpha alpha_max xoffset xdrift * 0.28 yoffset ydrift * 0.28 rotate xdrift * 0.018
        linear 0.18 alpha 0.0 xoffset xdrift yoffset ydrift zoom 1.11 rotate xdrift * 0.045
        pause 0.22
        repeat

transform msbf_boss_rupture_hit:
    subpixel True
    alpha 1.0
    xoffset 0
    yoffset 0
    zoom 1.0
    rotate 0.0
    linear 0.025 xoffset -42 yoffset 18 zoom 1.075 rotate -4.0 alpha 0.68
    linear 0.035 xoffset 38 yoffset -16 rotate 3.2 alpha 1.0
    linear 0.025 xoffset -24 yoffset 8 rotate -2.2 alpha 0.54
    linear 0.045 xoffset 18 yoffset -6 rotate 1.4 alpha 1.0
    easeout 0.16 xoffset 0 yoffset 0 zoom 1.0 rotate 0.0

transform msbf_boss_rupture_cast:
    subpixel True
    alpha 1.0
    xoffset 0
    yoffset 0
    zoom 1.0
    rotate 0.0
    linear 0.05 zoom 1.12 yoffset -34 xoffset -16 rotate -2.6 alpha 0.78
    linear 0.04 xoffset 26 yoffset -18 rotate 2.1 alpha 1.0
    linear 0.035 xoffset -22 yoffset -42 rotate -1.8 alpha 0.72
    linear 0.055 xoffset 18 yoffset -26 rotate 1.3 alpha 1.0
    easein 0.16 xoffset 0 yoffset 0 zoom 1.0 rotate 0.0

transform msbf_phase2_halo_line(delay=0.0, spin=1.0, alpha_max=0.28):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom 0.98
    rotate 0.0
    pause delay
    parallel:
        block:
            ease 0.80 alpha alpha_max zoom 1.03
            ease 1.10 alpha 0.10 zoom 0.98
            repeat
    parallel:
        linear 7.0 rotate 360.0 * spin
        repeat

transform msbf_phase2_ray(angle=0.0, delay=0.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    rotate angle
    alpha 0.0
    zoom 0.94
    pause delay
    block:
        linear 0.16 alpha 0.26 zoom 1.0
        linear 0.70 alpha 0.04 zoom 1.10
        pause 0.80
        repeat

transform msbf_phase2_eye(delay=0.0):
    subpixel True
    alpha 0.0
    yoffset 0
    pause delay
    block:
        ease 0.22 alpha 0.78 yoffset -3
        ease 0.48 alpha 0.22 yoffset 2
        pause 0.65
        repeat

transform msbf_phase2_eye_sweep(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset -16
    pause delay
    block:
        xoffset -16
        linear 0.07 alpha 0.72 xoffset 0
        linear 0.16 alpha 0.16 xoffset 18
        linear 0.10 alpha 0.0 xoffset 26
        pause 0.85
        repeat

transform msbf_phase2_stage_fault(angle=0.0, delay=0.0, alpha_max=0.42):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    rotate angle
    alpha 0.0
    zoom 0.78
    pause delay
    block:
        linear 0.05 alpha alpha_max zoom 1.0
        linear 0.16 alpha 0.0 zoom 1.16
        pause 0.74
        repeat

transform msbf_phase2_stage_lance(delay=0.0, alpha_max=0.46):
    subpixel True
    alpha 0.0
    yoffset -88
    pause delay
    block:
        yoffset -88
        linear 0.07 alpha alpha_max yoffset -12
        linear 0.28 alpha 0.0 yoffset 92
        pause 0.82
        repeat

transform msbf_phase2_stage_bg_pan(delay=0.0, alpha_max=0.30, direction=1.0):
    subpixel True
    alpha alpha_max
    xoffset -36 * direction
    yoffset -18
    zoom 1.14
    rotate -0.16 * direction
    pause delay
    parallel:
        ease 6.6 xoffset 34 * direction yoffset 16
        ease 7.4 xoffset -20 * direction yoffset 22
        ease 5.8 xoffset -36 * direction yoffset -18
        repeat
    parallel:
        ease 9.0 rotate 0.18 * direction
        ease 8.0 rotate -0.14 * direction
        repeat

transform msbf_phase2_stage_mist(angle=0.0, delay=0.0, alpha_max=0.18, direction=1.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 393 - (650 * direction)
    ypos 229
    rotate angle
    alpha 0.0
    pause delay
    block:
        xpos 393 - (650 * direction)
        alpha 0.0
        linear 1.10 alpha alpha_max
        linear 6.40 xpos 393 + (650 * direction) alpha 0.0
        pause 1.20
        repeat

transform msbf_stage_sweep(delay=0.0):
    subpixel True
    xpos 20
    alpha 0.0
    pause delay
    block:
        xpos 20
        alpha 0.0
        linear 0.16 alpha 0.42
        linear 1.2 xpos 540 alpha 0.0
        pause 1.0
        repeat

transform msbf_stage_sweep_fast(delay=0.0):
    subpixel True
    xpos 28
    alpha 0.0
    pause delay
    block:
        xpos 28
        alpha 0.0
        linear 0.08 alpha 0.62
        linear 0.42 xpos 640 alpha 0.0
        pause 1.8
        repeat

transform msbf_stage_spark(delay=0.0):
    subpixel True
    alpha 0.0
    yoffset 20
    pause delay
    block:
        alpha 0.0
        yoffset 20
        linear 0.18 alpha 0.65
        linear 1.4 yoffset -70 alpha 0.0
        pause 0.8
        repeat

transform msbf_stage_glitch(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset 0
    pause delay
    block:
        alpha 0.0
        xoffset -8
        linear 0.04 alpha 0.34
        linear 0.05 xoffset 8 alpha 0.18
        linear 0.05 xoffset 0 alpha 0.0
        pause 2.1
        repeat

transform msbf_target_tick(delay=0.0):
    subpixel True
    alpha 0.12
    pause delay
    block:
        ease 0.42 alpha 0.54
        ease 0.58 alpha 0.12
        pause 0.6
        repeat

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

screen msbf_battle_backdrop(dim="#02050ab8", phase=1):
    if phase == 3:
        add "msbf_rupture_backdrop" at msbf_phase3_bg_rupture
        add "msbf_rupture_backdrop" at msbf_phase3_bg_echo(0.16, 0.18, 1.0)
        add "msbf_rupture_backdrop" at msbf_phase3_bg_echo(0.72, 0.13, -1.0)
    elif phase >= 2:
        add "bg battle_setpiece" at msbf_phase2_bg_dizzy
        add "bg battle_setpiece" at msbf_phase2_bg_veil(0.0, 0.18, 1.0)
        add "bg battle_setpiece" at msbf_phase2_bg_veil(1.8, 0.12, -1.0)
    else:
        add "bg battle_setpiece" at msbf_bg_drift
    add Solid(dim)
    if phase == 3:
        add Solid("#1a0209a0") at msbf_phase3_pressure(0.00, 0.30)
        add Solid("#ffffff54") xysize (1180, 3) at msbf_phase3_fault_line(-24.0, 0.00, 0.52, 1.0):
            xcenter 640
            ycenter 318
        add Solid("#ff38686a") xysize (1100, 4) at msbf_phase3_fault_line(34.0, 0.18, 0.62, -1.0):
            xcenter 640
            ycenter 388
        add Solid("#f5fbff48") xysize (920, 2) at msbf_phase3_fault_line(-7.0, 0.44, 0.42, 1.0):
            xcenter 640
            ycenter 216
        add Solid("#ffffff42") xysize (760, 3) at msbf_phase3_tornado_streak(640, 360, 570, 190, 0.00, 0.30, 1.0)
        add Solid("#ff386858") xysize (680, 4) at msbf_phase3_tornado_streak(640, 350, 520, 150, 0.22, 0.36, -1.0)
        add Solid("#a66bff42") xysize (620, 3) at msbf_phase3_tornado_streak(640, 374, 470, 216, 0.46, 0.26, 1.0)
        add Solid("#ffffffb0") xysize (34, 7) at msbf_phase3_tornado_debris(640, 360, 560, 170, 0.04, 0.62, 1.0, 1.0)
        add Solid("#ff3868c0") xysize (26, 9) at msbf_phase3_tornado_debris(640, 354, 500, 138, 0.18, 0.66, -1.0, 1.10)
        add Solid("#12060cdd") xysize (52, 11) at msbf_phase3_tornado_debris(640, 372, 610, 204, 0.34, 0.58, 1.0, 1.24)
        add Solid("#a66bffb8") xysize (22, 7) at msbf_phase3_tornado_debris(640, 340, 430, 120, 0.51, 0.54, -1.0, 0.92)
        add Solid("#f5fbffcc") xysize (42, 8) at msbf_phase3_tornado_debris(640, 386, 660, 232, 0.70, 0.50, 1.0, 1.18)
        add Solid("#ff6b9fcc") xysize (30, 10) at msbf_phase3_tornado_debris(640, 362, 540, 190, 0.88, 0.58, -1.0, 1.05)
        add Solid("#a66bff22") xysize (380, 920) at msbf_phase3_debris(-22.0, 0.10, 0.16, 1.0):
            xcenter 640
            ycenter 360
        add Solid("#ff386824") xysize (260, 920) at msbf_phase3_debris(31.0, 0.44, 0.18, -1.0):
            xcenter 640
            ycenter 360
        add Solid("#ffffff2e") xysize (1280, 2) at msbf_phase3_static_slice(0.04, 0.30, 1.0):
            ypos 128
        add Solid("#ff386840") xysize (1280, 4) at msbf_phase3_static_slice(0.30, 0.38, -1.0):
            ypos 504
        add Solid("#a66bff30") xysize (1280, 3) at msbf_phase3_static_slice(0.74, 0.28, 1.0):
            ypos 342
    else:
        add Solid("#55ddff16") xysize (270, 900) at msbf_bg_crossbeam(-14.0, 0.0, 0.15)
        add Solid("#ff386812") xysize (220, 900) at msbf_bg_crossbeam(11.0, 1.4, 0.12)
        add Solid("#ffcf6610") xysize (180, 900) at msbf_bg_crossbeam(-4.0, 2.6, 0.10)
        add Solid("#55ddff22") xysize (1280, 2) at msbf_scanline(0.0, 0.14)
        add Solid("#ff386822") xysize (1280, 3) at msbf_scanline(1.1, 0.16)
        add Solid("#ffffff18") xysize (1280, 1) at msbf_scanline(2.0, 0.12)
    if phase >= 2 and phase != 3:
        add Solid("#ffcf6614") at msbf_phase2_bg_pulse(0.00, 0.16)
        add Solid("#55ddff12") at msbf_phase2_bg_pulse(0.42, 0.13)
        add Solid("#ff386814") at msbf_phase2_bg_pulse(0.78, 0.12)
        add Solid("#00000028") at msbf_phase2_bg_pulse(1.10, 0.18)
        add Solid("#00000044") xysize (520, 920) at msbf_phase2_collapse_bar(-18.0, 0.10, 0.22, 1.0)
        add Solid("#19040a3e") xysize (420, 920) at msbf_phase2_collapse_bar(28.0, 0.82, 0.20, -1.0)
        add Solid("#03142136") xysize (360, 920) at msbf_phase2_collapse_bar(6.0, 1.54, 0.16, 1.0)
        add Solid("#ffffff28") xysize (900, 920) at msbf_phase2_white_rift(-46.0, 0.18, 0.30):
            xcenter 640
            ycenter 360
        add Solid("#fff2bf24") xysize (760, 920) at msbf_phase2_white_rift(36.0, 1.05, 0.26):
            xcenter 640
            ycenter 360
        add Solid("#dff9ff22") xysize (580, 920) at msbf_phase2_white_rift(4.0, 1.72, 0.24):
            xcenter 640
            ycenter 360
        add Solid("#f5fbff30") xysize (420, 920) at msbf_phase2_bg_shard(-31.0, 0.00, 0.22, 1.0)
        add Solid("#ffcf6632") xysize (300, 920) at msbf_phase2_bg_shard(23.0, 0.24, 0.20, -1.0)
        add Solid("#55ddff30") xysize (220, 920) at msbf_phase2_bg_shard(-8.0, 0.50, 0.18, 1.0)
        add Solid("#f5fbff48") xysize (860, 2) at msbf_phase2_starstream(-22.0, 0.20, 0.30, 1.0, 5.0, 164)
        add Solid("#55ddff38") xysize (720, 2) at msbf_phase2_starstream(16.0, 1.10, 0.24, -1.0, 4.6, 514)
        add Solid("#ffcf6632") xysize (560, 3) at msbf_phase2_starstream(34.0, 2.20, 0.22, 1.0, 3.9, 356)
        add Solid("#ffffff36") xysize (980, 1) at msbf_phase2_starstream(-6.0, 3.00, 0.22, -1.0, 5.8, 252)
        add Solid("#ffffff30") xysize (1280, 2) at msbf_phase2_scanline_burst(0.04)
        add Solid("#ff38683a") xysize (1280, 3) at msbf_phase2_scanline_burst(0.38):
            ypos 214
        add Solid("#55ddff35") xysize (1280, 2) at msbf_phase2_scanline_burst(0.70):
            ypos 486

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

screen msbf_phase_transition_overlay(battle):
    $ _phase_transition_title = getattr(battle, "phase_transition_title", "THE STAGE BEGINS ANEW")
    $ _phase_transition_subtitle = getattr(battle, "phase_transition_subtitle", "A WINGED ANGEL REWRITES THE SCRIPT")

    if battle.final_victory_active:
        add Solid("#000000") at msbf_phase_transition_blackout
        use msbf_phase2_boom_overlay(2)
        add Solid("#fff4dc") at msbf_phase_break_flash(0.00, 1.0)
        add Solid("#ff3868") at msbf_phase_break_flash(0.04, 0.78)
        add Solid("#55ddff") at msbf_phase_break_flash(0.11, 0.52)
        add Solid("#ffffff") at msbf_phase_transition_burst(0.18, 0.86)
        add Solid("#ffcf66") at msbf_phase_transition_burst(0.82, 0.56)
        add Solid("#ffffff") at msbf_phase_reveal_bloom(1.64, 0.50)
        add Solid("#ffffff") xysize (1240, 14) at msbf_phase_break_lance(-7.0, 0.00, 1.0):
            xcenter 640
            ycenter 274
        add Solid("#ff3868") xysize (1180, 11) at msbf_phase_break_lance(18.0, 0.05, 0.88):
            xcenter 640
            ycenter 344
        add Solid("#ffcf66") xysize (1040, 8) at msbf_phase_transition_lance(-28.0, 0.34, 0.76):
            xcenter 640
            ycenter 216
        add Solid("#55ddff") xysize (1120, 6) at msbf_phase_transition_lance(31.0, 0.58, 0.72):
            xcenter 640
            ycenter 432
        add Solid("#ffffff82") xysize (980, 3) at msbf_phase_transition_ring(0.24, 1.0):
            xcenter 640
            ycenter 320
        add Solid("#ff386870") xysize (2, 650) at msbf_phase_transition_ring(0.52, -0.8):
            xcenter 640
            ycenter 320
        add Solid("#ffffff") at msbf_final_victory_white_pressure
        add Solid("#ffffff") at msbf_final_victory_whiteout
    elif getattr(battle, "final_victory_whiteout", False):
        add Solid("#ffffff")
    elif battle.phase_transition_active:
        if battle.fx_event == "phase_blackout":
            add Solid("#000000")
            add Solid("#fff4dc") at msbf_phase_break_flash(0.00, 0.96)
            add Solid("#ff3868") at msbf_phase_break_flash(0.035, 0.54)
            add Solid("#ffcf66") at msbf_phase_break_flash(0.075, 0.40)
            add Solid("#ffffff") xysize (1180, 12) at msbf_phase_break_lance(-10.0, 0.00, 0.96):
                xcenter 640
                ycenter 270
            add Solid("#ff3868") xysize (1120, 9) at msbf_phase_break_lance(16.0, 0.04, 0.78):
                xcenter 640
                ycenter 348
            add Solid("#ffcf66") xysize (980, 7) at msbf_phase_break_lance(-34.0, 0.08, 0.64):
                xcenter 640
                ycenter 224
            add Solid("#55ddff") xysize (900, 5) at msbf_phase_break_lance(38.0, 0.12, 0.54):
                xcenter 640
                ycenter 430
        elif battle.fx_event == "phase":
            if battle.phase == 3:
                add "msbf_rupture_backdrop" at msbf_phase3_bg_rupture
                add "msbf_rupture_backdrop" at msbf_phase3_bg_echo(0.10, 0.30, 1.0)
                add Solid("#050007d8")
                use msbf_phase3_rupture_overlay(2)
                add Solid("#ffffff") xysize (1280, 3) at msbf_phase3_fault_line(-33.0, 0.05, 0.78, 1.0):
                    xcenter 640
                    ycenter 238
                add Solid("#ff3868") xysize (1280, 5) at msbf_phase3_fault_line(24.0, 0.16, 0.82, -1.0):
                    xcenter 640
                    ycenter 374
                add Solid("#a66bff") xysize (1280, 3) at msbf_phase3_fault_line(-8.0, 0.34, 0.58, 1.0):
                    xcenter 640
                    ycenter 456
            add Solid("#000000") at msbf_phase_transition_blackout
            add Solid("#ffffff") at msbf_phase_reveal_bloom(0.00, 0.58)
            add Solid("#ffcf66") at msbf_phase_reveal_bloom(0.34, 0.28)
            add Solid("#55ddff") xysize (1280, 5) at msbf_phase_reveal_cut(-18.0, 0.18, 0.72):
                xcenter 640
                ycenter 214
            add Solid("#ffffff") xysize (1280, 7) at msbf_phase_reveal_cut(9.0, 0.48, 0.86):
                xcenter 640
                ycenter 366
            add Solid("#ff3868") xysize (1280, 4) at msbf_phase_reveal_cut(31.0, 0.78, 0.62):
                xcenter 640
                ycenter 286
            add Solid("#ffcf66") at msbf_phase_reveal_bloom(1.58, 0.22)
            add Solid("#ffffff") xysize (1280, 5) at msbf_phase_reveal_cut(-7.0, 2.18, 0.44):
                xcenter 640
                ycenter 426
            add Solid("#ffffff") at msbf_phase_transition_burst(0.00, 0.88)
            add Solid("#ff3868") at msbf_phase_transition_burst(0.24, 0.42)
            add Solid("#fff2bf") at msbf_phase_transition_burst(0.86, 0.36)
            add Solid("#ffffff5c") xysize (860, 4) at msbf_phase_transition_lance(-12.0, 0.08, 0.72):
                xcenter 640
                ycenter 252
            add Solid("#ff38686e") xysize (980, 5) at msbf_phase_transition_lance(9.0, 0.30, 0.62):
                xcenter 640
                ycenter 342
            add Solid("#ffcf6662") xysize (760, 4) at msbf_phase_transition_lance(-28.0, 0.66, 0.54):
                xcenter 640
                ycenter 412
            add Solid("#55ddff5a") xysize (700, 3) at msbf_phase_transition_lance(31.0, 1.02, 0.46):
                xcenter 640
                ycenter 196
            add Solid("#ffcf6680") xysize (900, 2) at msbf_phase_transition_ring(0.16, 1.0):
                xcenter 640
                ycenter 320
            add Solid("#f5fbff70") xysize (760, 2) at msbf_phase_transition_ring(0.40, -1.0):
                xcenter 640
                ycenter 320
            add Solid("#ff386858") xysize (2, 620) at msbf_phase_transition_ring(0.62, 0.7):
                xcenter 640
                ycenter 320
            text _phase_transition_title style "msbf_phase_transition_title" at msbf_phase_transition_title(0.00):
                xalign 0.5
                yalign 0.34
            text _phase_transition_subtitle style "msbf_phase_transition_subtitle" at msbf_phase_transition_subtitle(0.72):
                xalign 0.5
                yalign 0.47
        elif not battle.phase2_reveal_started:
            if battle.phase == 3:
                use msbf_phase3_rupture_overlay(1)
            else:
                use msbf_phase2_boom_overlay(1)
            add Solid("#02040b80") at msbf_phase_transition_curtain
            text "BRACE" style "msbf_phase_transition_breathe_text" at msbf_phase_transition_breathe:
                xalign 0.5
                yalign 0.42
            text "A NEW TEMPO BEGINS" style "msbf_phase_transition_subtitle" at msbf_phase_transition_breathe:
                xalign 0.5
                yalign 0.53

screen msbf_fx_layer(battle):
    if battle.fx_event and battle.fx_event not in ("phase_blackout", "phase", "final_victory"):
        timer battle.fx_clear_delay action Function(battle.clear_fx)

        if battle.fx_event in ("weak", "enemy_weak"):
            add Solid("#ffcf6640") at msbf_fx_flash("#ffcf66", 0.24)
            add Solid("#ffcf66") xysize (440, 16) at msbf_fx_slash(-12.0, 0.02):
                xcenter 875
                ycenter 260
            text "WEAK" style "msbf_fx_weak" at msbf_fx_text:
                xalign 0.70
                yalign 0.35
        elif battle.fx_event in ("crit", "enemy_crit"):
            add Solid("#ffffff4c") at msbf_fx_flash("#ffffff", 0.28)
            add Solid("#ffffff") xysize (520, 18) at msbf_fx_slash(-18.0, 0.0):
                xcenter 875
                ycenter 250
            add Solid("#ff3868") xysize (420, 12) at msbf_fx_slash(12.0, 0.05):
                xcenter 875
                ycenter 310
            text "CRITICAL" style "msbf_fx_crit" at msbf_fx_text_big:
                xalign 0.70
                yalign 0.34
        elif battle.fx_event == "miss":
            add Solid("#54637844") at msbf_fx_flash("#546378", 0.20)
            text "MISS" style "msbf_fx_resist" at msbf_fx_text:
                xalign 0.70
                yalign 0.36
        elif battle.fx_event in ("resist", "enemy_resist"):
            add Solid("#54637844") at msbf_fx_flash("#546378", 0.20)
            text "RESIST" style "msbf_fx_resist" at msbf_fx_text:
                xalign 0.70
                yalign 0.36
        elif battle.fx_event in ("heal", "enemy_heal"):
            add Solid("#66e08a33") at msbf_fx_flash("#66e08a", 0.18)
            text "RECOVER" style "msbf_fx_heal" at msbf_fx_text:
                xalign 0.23
                yalign 0.52
        elif battle.fx_event == "revive":
            add Solid("#66e08a44") at msbf_fx_flash("#66e08a", 0.24)
            text "REVIVE" style "msbf_fx_heal" at msbf_fx_text:
                xalign 0.23
                yalign 0.52
        elif battle.fx_event == "recover_mp":
            add Solid("#55ddff26") at msbf_fx_flash("#55ddff", 0.16)
        elif battle.fx_event == "shuffle":
            add Solid("#55ddff3a") at msbf_fx_flash("#55ddff", 0.24)
            add Solid("#55ddff") xysize (660, 8) at msbf_fx_slash(0.0, 0.03):
                xcenter 850
                ycenter 190
            text "AFFINITY SHIFT" style "msbf_fx_scan" at msbf_fx_text_big:
                xalign 0.66
                yalign 0.30
        elif battle.fx_event == "phase":
            add Solid("#ff386866") at msbf_fx_flash("#ff3868", 0.34)
            add Solid("#ff3868") xysize (720, 18) at msbf_fx_slash(-6.0, 0.0):
                xcenter 850
                ycenter 245
            add Solid("#ffffff") xysize (540, 10) at msbf_fx_slash(17.0, 0.10):
                xcenter 812
                ycenter 312
        elif battle.fx_event == "victory":
            add Solid("#55ddff4a") at msbf_fx_flash("#55ddff", 0.30)
            add Solid("#55ddff") xysize (720, 14) at msbf_fx_slash(-4.0, 0.0):
                xcenter 850
                ycenter 245
            text "CLEAR" style "msbf_fx_scan" at msbf_fx_text_big:
                xalign 0.66
                yalign 0.32
        elif battle.fx_event == "defeat":
            add Solid("#ff38684f") at msbf_fx_flash("#ff3868", 0.30)
            text "DOWN" style "msbf_fx_phase" at msbf_fx_text_big:
                xalign 0.66
                yalign 0.32
        elif battle.fx_event in ("enemy", "enemy_hit", "enemy_aoe", "enemy_guard"):
            add Solid("#ff38682c") at msbf_fx_flash("#ff3868", 0.20)
            add Solid("#ff3868") xysize (440, 10) at msbf_fx_slash(10.0, 0.0):
                xcenter 860
                ycenter 300
        elif battle.fx_event in ("hit", "guard", "buff", "debuff", "scan", "pass", "enemy_buff"):
            add Solid("#55ddff22") at msbf_fx_flash("#55ddff", 0.14)

screen msbf_party_select():
    modal True

    default picks = []
    default rows = msbf_default_rows(picks)

    $ _pick_count = len(picks)
    $ _front_count = msbf_front_count(picks, rows)

    use msbf_battle_backdrop("#03060eee")

    key "game_menu" action ShowMenu("save")
    key "K_ESCAPE" action ShowMenu("save")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1180
        ysize 660
        background Solid("#050d18f2")
        padding (22, 20)
        at msbf_panel_enter()

        fixed:
            xysize (1136, 620)

            hbox:
                xpos 0
                ypos 0
                xsize 1136
                xfill True

                vbox:
                    spacing 4
                    xsize 790
                    text "A SICK BOSS FIGHT" style "msbf_title"
                    text "Build a four-person party, set rows, then open the setpiece." style "msbf_subtitle"

                null xfill True

                frame:
                    xalign 1.0
                    yalign 0.5
                    xsize 142
                    ysize 62
                    background Solid("#0b2637ee")
                    padding (10, 7)

                    vbox:
                        spacing 0
                        xfill True
                        text "PARTY" style "msbf_party_count_label":
                            xalign 0.5
                        text "[_pick_count] / 4" style "msbf_party_count":
                            xalign 0.5

            add Solid("#55ddff66") xpos 0 ypos 98 xysize (1136, 2)
            add Solid("#ff386850") xpos 0 ypos 102 xysize (208, 2)

            hbox:
                xpos 0
                ypos 118
                spacing 16
                xsize 1136

                frame:
                    xsize 344
                    ysize 436
                    background Solid("#07111ee8")
                    padding (14, 12)

                    vbox:
                        spacing 9

                        hbox:
                            xfill True
                            text "FORMATION" style "msbf_select_panel_label"
                            null xfill True
                            text "FRONT [_front_count]" style "msbf_select_panel_count":
                                yalign 0.5

                        for slot_idx in range(4):
                            $ _slot_num = slot_idx + 1
                            if slot_idx < len(picks):
                                $ _slot_entry = MSBF_ROSTER_BY_ID[picks[slot_idx]]
                                $ _slot_id = _slot_entry["id"]
                                $ _slot_row = rows.get(_slot_id, "front")
                                $ _slot_row_label = msbf_row_label(_slot_row)

                                frame:
                                    xfill True
                                    ysize 68
                                    padding (8, 7)
                                    background Solid("#12314af0")

                                    hbox:
                                        spacing 7
                                        yalign 0.5

                                        frame:
                                            xysize (36, 36)
                                            background Solid("#1d5c82")
                                            padding (0, 0)
                                            text "[_slot_num]" style "msbf_order_num":
                                                xalign 0.5
                                                yalign 0.5

                                        vbox:
                                            spacing 2
                                            xsize 132
                                            yalign 0.5
                                            text _slot_entry["name"] style "msbf_order_name"
                                            text _slot_entry["role"] style "msbf_order_role"

                                        textbutton _slot_row_label:
                                            style "msbf_row_button"
                                            hover_sound MSBF_UI_SFX["hover"]
                                            activate_sound MSBF_UI_SFX["accept"]
                                            action SetScreenVariable("rows", msbf_toggle_row(picks, rows, _slot_id))

                                        textbutton "X":
                                            style "msbf_remove_button"
                                            hover_sound MSBF_UI_SFX["hover"]
                                            activate_sound MSBF_UI_SFX["denied"]
                                            action [SetScreenVariable("picks", msbf_remove_member(picks, rows, _slot_id)[0]), SetScreenVariable("rows", msbf_remove_member(picks, rows, _slot_id)[1])]
                            else:
                                frame:
                                    xfill True
                                    ysize 68
                                    background Solid("#03070daa")
                                    padding (8, 7)

                                    hbox:
                                        spacing 8
                                        yalign 0.5

                                        frame:
                                            xysize (36, 36)
                                            background Solid("#1a263055")
                                            padding (0, 0)
                                            text "[_slot_num]" style "msbf_order_empty_num":
                                                xalign 0.5
                                                yalign 0.5

                                        vbox:
                                            spacing 1
                                            yalign 0.5
                                            text "EMPTY SLOT" style "msbf_order_empty"
                                            text "Choose from roster" style "msbf_order_role"

                        add Solid("#55ddff33") xysize (316, 1)
                        text "Slot order controls turn order. Front draws more single-target pressure." style "msbf_select_footnote":
                            xmaximum 314

                vbox:
                    xsize 776
                    spacing 8

                    hbox:
                        xfill True
                        text "PARTY ROSTER" style "msbf_select_panel_label"
                        null xfill True
                        text "CLICK TO ADD / REMOVE" style "msbf_select_panel_count":
                            yalign 0.5

                    grid 2 4:
                        xsize 776
                        spacing 8

                        for entry in MSBF_ROSTER:
                            $ _selected = entry["id"] in picks
                            $ _locked = (not _selected) and len(picks) >= 4
                            $ _order_num = picks.index(entry["id"]) + 1 if _selected else 0
                            $ _row_text = msbf_row_label(rows.get(entry["id"], "front")) if _selected else ""

                            button:
                                style "msbf_roster_button"
                                hover_sound MSBF_UI_SFX["hover"]
                                activate_sound MSBF_UI_SFX["accept"]
                                sensitive not _locked

                                if _selected:
                                    background Solid("#143d59f0")
                                    hover_background Solid("#1f5c83f8")
                                    action [SetScreenVariable("picks", msbf_select_member(picks, rows, entry["id"])[0]), SetScreenVariable("rows", msbf_select_member(picks, rows, entry["id"])[1])]
                                elif _locked:
                                    background Solid("#050910d8")
                                    hover_background Solid("#050910d8")
                                else:
                                    background Solid("#081421e8")
                                    hover_background Solid("#12314af0")
                                    action [SetScreenVariable("picks", msbf_select_member(picks, rows, entry["id"])[0]), SetScreenVariable("rows", msbf_select_member(picks, rows, entry["id"])[1])]

                                fixed:
                                    xysize (366, 80)

                                    add Solid("#66e08a" if _selected else ("#293546" if _locked else "#55ddff")) xysize (4, 80)

                                    hbox:
                                        xpos 14
                                        ypos -2
                                        xsize 346
                                        spacing 7

                                        if _selected:
                                            text "#[_order_num]" style "msbf_roster_order_badge":
                                                yalign 0.5
                                        text entry["name"] style "msbf_roster_name":
                                            yalign 0.5
                                            xmaximum 116
                                        text entry["role"] style "msbf_roster_role":
                                            yalign 0.5
                                            xmaximum 128
                                        null xfill True
                                        if _selected:
                                            text _row_text style "msbf_roster_row_tag":
                                                yalign 0.5

                                    text entry["summary"] style "msbf_roster_summary":
                                        xpos 14
                                        ypos 26
                                        xmaximum 346

                                    hbox:
                                        xpos 14
                                        ypos 62
                                        spacing 5
                                        use msbf_select_stat_bar("HP", entry["max_hp"], 700, "#66e08a")
                                        use msbf_select_stat_bar("ATK", entry["offense"], 90, "#ffcf66")
                                        use msbf_select_stat_bar("MAG", entry["magic"], 80, "#82a6ff")
                                        use msbf_select_stat_bar("SPD", entry["agility"], 76, "#ff6b8e")

                                    if _selected:
                                        text "SELECTED" style "msbf_roster_selected":
                                            xpos 286
                                            ypos 61
                                    elif _locked:
                                        text "PARTY FULL" style "msbf_roster_locked":
                                            xpos 286
                                            ypos 61
                                    else:
                                        text "AVAILABLE" style "msbf_roster_available":
                                            xpos 286
                                            ypos 61

                        null xsize 384 ysize 96

            hbox:
                xpos 0
                ypos 572
                xsize 1136
                ysize 48

                text "Pick at least one frontliner. Rear members take less pressure from physical hits." style "msbf_select_footnote":
                    yalign 0.5
                    xmaximum 650

                null xfill True

                textbutton "BEGIN":
                    style "msbf_begin_button"
                    hover_sound MSBF_UI_SFX["hover"]
                    activate_sound MSBF_UI_SFX["accept"]
                    sensitive msbf_can_begin(picks, rows)
                    action Return(msbf_party_config(picks, rows))
                    yalign 0.5

screen msbf_select_stat_bar(label, value, max_value, fill_color):
    frame:
        xsize 64
        ysize 14
        background Solid("#03070daa")
        padding (0, 0)

        add Solid("#152333") xysize (64, 14)
        add Solid(fill_color) xysize (msbf_bar_width(value, max_value, 64), 14)
        text label style "msbf_select_stat_label":
            xpos 4
            yalign 0.5

screen msbf_shmup_overlay(battle):
    key "K_LEFT" action Function(battle.shmup_nudge, -22, 0)
    key "K_RIGHT" action Function(battle.shmup_nudge, 22, 0)
    key "K_UP" action Function(battle.shmup_nudge, 0, -22)
    key "K_DOWN" action Function(battle.shmup_nudge, 0, 22)
    key "a" action Function(battle.shmup_nudge, -22, 0)
    key "d" action Function(battle.shmup_nudge, 22, 0)
    key "w" action Function(battle.shmup_nudge, 0, -22)
    key "s" action Function(battle.shmup_nudge, 0, 22)

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

                $ _progress = min(1.0, float(battle.shmup_tick) / float(MSBF_SHMUP_DURATION_TICKS))
                add Solid("#ffcf66") xysize (int(MSBF_SHMUP_STAGE_WIDTH * _progress), 4):
                    xpos 0
                    ypos 0

                for _hit_index in range(MSBF_SHMUP_HIT_LIMIT):
                    add Solid("#ff3868" if _hit_index < battle.shmup_hits else "#ffffff38") xysize (18, 4):
                        xpos 10 + _hit_index * 24
                        ypos 10

                for bullet in battle.shmup_bullets:
                    $ _size = int(bullet.get("size", 10))
                    $ _shape = bullet.get("shape", "orb")
                    if _shape == "beam":
                        $ _beam_w = int(bullet.get("w", _size))
                        $ _beam_h = int(bullet.get("h", _size))
                        $ _beam_x = bullet.get("x", 0.0) - (_beam_w / 2.0)
                        $ _beam_y = bullet.get("y", 0.0) - (_beam_h / 2.0)
                        $ _armed = bullet.get("age", 0) >= bullet.get("arm_age", 0)
                        $ _beam_color = bullet.get("color", "#ff3868dd") if _armed else "#ffffff42"
                        add Solid(_beam_color) xysize (_beam_w, _beam_h):
                            subpixel True
                            xpos absolute(_beam_x)
                            ypos absolute(_beam_y)
                        add Solid("#ffffff70" if _armed else "#ffcf6690") xysize (_beam_w, max(2, _beam_h // 3)):
                            subpixel True
                            xpos absolute(_beam_x)
                            ypos absolute(bullet.get("y", 0.0) - max(2, _beam_h // 3) / 2.0)
                    elif _shape == "needle":
                        $ _bullet_w = max(3, int(_size * 0.48))
                        $ _bullet_h = max(12, int(_size * 2.15))
                        $ _bullet_x = bullet.get("x", 0.0) - (_bullet_w / 2.0)
                        $ _bullet_y = bullet.get("y", 0.0) - (_bullet_h / 2.0)
                        add Solid(bullet.get("color", "#f5fbffdd")) xysize (_bullet_w, _bullet_h):
                            subpixel True
                            xpos absolute(_bullet_x)
                            ypos absolute(_bullet_y)
                            rotate bullet.get("rot", 0.0)
                        add Solid("#ffffff90") xysize (max(2, _bullet_w - 1), max(5, int(_bullet_h * 0.42))):
                            subpixel True
                            xpos absolute(bullet.get("x", 0.0) - max(2, _bullet_w - 1) / 2.0)
                            ypos absolute(bullet.get("y", 0.0) - max(5, int(_bullet_h * 0.42)) / 2.0)
                            rotate bullet.get("rot", 0.0)
                    else:
                        $ _bullet_x = bullet.get("x", 0.0) - (_size / 2.0)
                        $ _bullet_y = bullet.get("y", 0.0) - (_size / 2.0)
                        add Solid(bullet.get("color", "#ff3868dd")) xysize (_size, _size):
                            subpixel True
                            xpos absolute(_bullet_x)
                            ypos absolute(_bullet_y)
                        add Solid("#ffffff70") xysize (max(3, _size // 3), max(3, _size // 3)):
                            subpixel True
                            xpos absolute(bullet.get("x", 0.0) - max(3, _size // 3) / 2.0)
                            ypos absolute(bullet.get("y", 0.0) - max(3, _size // 3) / 2.0)

                $ _player_size = MSBF_SHMUP_PLAYER_RADIUS * 2
                $ _player_x = battle.shmup_player_x - MSBF_SHMUP_PLAYER_RADIUS
                $ _player_y = battle.shmup_player_y - MSBF_SHMUP_PLAYER_RADIUS
                $ _player_flash = battle.shmup_tick < getattr(battle, "shmup_invuln_until_tick", 0)
                add Solid("#ffffff" if _player_flash else "#55ddff") xysize (_player_size, _player_size):
                    subpixel True
                    xpos absolute(_player_x)
                    ypos absolute(_player_y)
                add Solid("#55ddff" if _player_flash else "#ffffff") xysize (4, 4):
                    subpixel True
                    xpos absolute(battle.shmup_player_x - 2.0)
                    ypos absolute(battle.shmup_player_y - 2.0)

        text "CURTAIN SCRIPT" style "msbf_phase_transition_subtitle":
            xalign 0.5
            ypos 42

screen msbf_battle_screen(battle):
    modal True

    default hovered_skill = None
    default pending_skill = None
    default log_yadj = ui.adjustment()
    default log_seen_serial = -1
    default phase2_boom_active = False
    default phase2_boom_delay = renpy.random.uniform(2.8, 5.6)
    default phase2_boom_kind = 0
    default phase2_boss_motion_tick = 0

    $ _actor = battle.current_actor
    $ _actor_name = battle.active_actor_label
    $ _boss_sprite_x = 393
    $ _boss_sprite_y = 240
    if battle.phase == 3:
        $ _boss_sprite_x, _boss_sprite_y = msbf_phase3_boss_anchor(phase2_boss_motion_tick)
    elif battle.phase >= 2:
        $ _boss_sprite_x, _boss_sprite_y = msbf_phase2_boss_anchor(phase2_boss_motion_tick)

    if battle.result:
        timer 0.5 action Return(battle.result)
    elif battle.final_victory_active:
        timer battle.fx_clear_delay action Function(battle.finish_final_victory)
    elif battle.phase_transition_active and battle.fx_event == "phase_blackout":
        timer battle.fx_clear_delay action Function(battle.begin_phase_two_reveal)
    elif battle.phase_transition_active and battle.fx_event == "phase":
        timer battle.fx_clear_delay action Function(battle.finish_phase_transition)
    elif battle.phase_transition_active and not battle.fx_event:
        timer battle.phase_transition_delay action Function(battle.finish_phase_transition)
    elif battle.shmup_segment_active:
        timer MSBF_SHMUP_TICK_SECONDS repeat True action Function(battle.update_shmup_segment)
    elif battle.enemy_phase_active and not battle.fx_event:
        timer battle.enemy_step_delay action Function(battle.advance_enemy_phase)

    if battle.phase >= 2 and not battle.result and not battle.phase_transition_active and not battle.final_victory_active:
        timer 0.05 repeat True action SetScreenVariable("phase2_boss_motion_tick", phase2_boss_motion_tick + 1)
        timer phase2_boom_delay repeat True action [
            SetScreenVariable("phase2_boom_active", True),
            SetScreenVariable("phase2_boom_kind", renpy.random.randint(0, 2)),
            SetScreenVariable("phase2_boom_delay", renpy.random.uniform(1.1, 2.8) if battle.phase == 3 else renpy.random.uniform(3.0, 6.4))
        ]

    if log_seen_serial != battle.log_serial:
        timer 0.01 action [Function(msbf_scroll_adjustment_to_bottom, log_yadj), SetScreenVariable("log_seen_serial", battle.log_serial)]

    use msbf_battle_backdrop("#02050ab8", battle.phase)

    key "game_menu" action ShowMenu("preferences")
    key "K_ESCAPE" action ShowMenu("preferences")

    # Boss status.
    frame:
        xpos 40
        ypos 30
        xsize 392
        ysize 145
        background Solid("#07111ef0")
        padding (14, 12)
        at msbf_panel_enter(), msbf_final_victory_rumble(1.0 if battle.final_victory_active else 0.0)

        vbox:
            spacing 6

            hbox:
                xfill True
                text battle.boss.name style "msbf_boss_name"

            use msbf_meter(battle.boss.hp, battle.boss.max_hp, 360, 13, "#ff3868", "#141923")

            hbox:
                spacing 12
                text "HP [battle.boss.hp]/[battle.boss.max_hp]" style "msbf_meter_text"

            hbox:
                spacing 12
                if battle.analyzed:
                    $ _boss_weak_label = msbf_affinity_label(battle.boss.weaknesses)
                    $ _boss_resist_label = msbf_affinity_label(battle.boss.resists)
                    text "WEAK [_boss_weak_label]" style "msbf_affinity_weak":
                        xmaximum 168
                    text "RESIST [_boss_resist_label]" style "msbf_affinity_resist":
                        xmaximum 180
                else:
                    text "AFFINITIES UNKNOWN" style "msbf_affinity_unknown"

    # Battle readout.
    frame:
        xpos 40
        ypos 196
        xsize 392
        ysize 292
        background Solid("#07111ee8")
        padding (14, 10)
        at msbf_panel_enter(0.04), msbf_final_victory_rumble(1.0 if battle.final_victory_active else 0.0)

        fixed:
            xysize (364, 272)

            add Solid("#030914d8") xysize (364, 54)
            add Solid("#ffcf6640") xysize (3, 54)
            add Solid("#55ddff44") xysize (364, 1)
            add Solid("#55ddff18") xysize (364, 1):
                ypos 53

            hbox:
                xpos 10
                ypos 6
                xsize 344
                ysize 17

                text battle.press_turn_label style "msbf_panel_label"
                null xfill True
                text "[battle.active_actions_this_phase]/[battle.active_action_cap]" style "msbf_turn_cap":
                    yalign 0.5

            fixed:
                xpos 10
                ypos 28
                xysize (344, 20)

                add Solid("#02060faa") xysize (344, 20)
                add Solid("#55ddff18") xysize (344, 1)
                add Solid("#ffffff10") xysize (344, 1):
                    ypos 19

                if battle.active_press_turn_icons:
                    hbox:
                        xpos MSBF_PRESS_TURN_ROW_X
                        ypos 0
                        spacing MSBF_PRESS_TURN_SLOT_SPACING
                        for _idx, icon in enumerate(battle.active_press_turn_icons):
                            use msbf_press_turn_icon(icon, _idx)
                else:
                    text battle.press_turn_empty_label style "msbf_turn_empty":
                        xpos 8
                        yalign 0.5

                $ _turn_fx_side = "enemy" if battle.enemy_phase_active else "player"
                $ _turn_fx_events = getattr(battle, "press_turn_fx_events", [])
                if _turn_fx_events:
                    for _turn_fx in _turn_fx_events:
                        if _turn_fx.get("side") == _turn_fx_side:
                            use msbf_press_turn_fx_icon(_turn_fx)
                    timer 0.58 action Function(battle.clear_press_turn_fx)

            add Solid("#55ddff3a") xysize (364, 1):
                ypos 62
            add Solid("#ff38682e") xysize (146, 1):
                xpos 218
                ypos 62

            add Solid("#02060cf4") xysize (364, 202):
                ypos 70
            add Solid("#55ddff4a") xysize (3, 202):
                ypos 70
            add Solid("#55ddff24") xysize (364, 1):
                ypos 70
            add Solid("#ffcf6630") xysize (92, 1):
                xpos 3
                ypos 98
            add Solid("#ffffff10") xysize (340, 1):
                xpos 12
                ypos 104

            hbox:
                xpos 12
                ypos 80
                xsize 340
                ysize 16

                text "COMBAT LOG" style "msbf_panel_label"
                null xfill True
                text "WHEEL / DRAG" style "msbf_log_hint":
                    yalign 0.5

            $ _log_last_index = len(battle.log) - 1

            viewport:
                id "msbf_log_viewport"
                xpos 12
                ypos 110
                xsize 340
                ysize 150
                yadjustment log_yadj
                mousewheel True
                draggable True
                yinitial 1.0

                vbox:
                    spacing 6
                    for _log_idx, line in enumerate(battle.log):
                        text line style ("msbf_log_text_latest" if _log_idx == _log_last_index else "msbf_log_text"):
                            xmaximum 330

    # Boss stage.
    frame:
        xpos 452
        ypos 30
        xsize 786
        ysize 458
        background Solid("#030912bb")
        padding (0, 0)
        at msbf_panel_enter(0.06), msbf_final_victory_rumble(1.0 if battle.final_victory_active else 0.0)

        fixed:
            xysize (786, 458)

            if battle.phase == 3:
                viewport:
                    xysize (786, 458)

                    add "msbf_rupture_stage" at msbf_phase3_bg_rupture:
                        xcenter 393
                        ycenter 229
                    add "msbf_rupture_stage" at msbf_phase3_bg_echo(0.12, 0.18, 1.0):
                        xcenter 393
                        ycenter 229
                    add "msbf_rupture_stage" at msbf_phase3_bg_echo(0.72, 0.12, -1.0):
                        xcenter 393
                        ycenter 229
                    add Solid("#09020cd0") xysize (786, 458)
                    add Solid("#ff38681f") xysize (786, 458) at msbf_phase3_pressure(0.08, 0.12)
            elif battle.phase >= 2:
                viewport:
                    xysize (786, 458)

                    add "bg battle_setpiece" at msbf_phase2_stage_bg_pan(0.0, 0.30, 1.0):
                        xcenter 393
                        ycenter 229
                    add "bg battle_setpiece" at msbf_phase2_stage_bg_pan(2.2, 0.18, -1.0):
                        xcenter 393
                        ycenter 229
                    add Solid("#02081290") xysize (786, 458)
                    add Solid("#0e314058") xysize (1280, 180) at msbf_phase2_stage_mist(-10.0, 0.00, 0.13, 1.0)
                    add Solid("#55ddff2a") xysize (1280, 130) at msbf_phase2_stage_mist(16.0, 1.80, 0.11, -1.0)
                    add Solid("#ffcf661f") xysize (1280, 118) at msbf_phase2_stage_mist(-28.0, 3.10, 0.10, 1.0)
                    add Solid("#00000034") xysize (1280, 126) at msbf_phase2_stage_mist(24.0, 0.92, 0.15, -1.0)

            if battle.phase == 3:
                add Solid("#ff386824") xysize (786, 458)
                add Solid("#ff386888") xysize (786, 2)
                add Solid("#a66bff54") xysize (786, 2):
                    yalign 1.0
            else:
                add Solid("#55ddff10") xysize (786, 458)
                add Solid("#55ddff5a") xysize (786, 2)
                add Solid("#55ddff30") xysize (786, 2):
                    yalign 1.0

            if battle.phase == 3:
                add Solid("#ffffff42") xysize (720, 3) at msbf_phase3_fault_line(-16.0, 0.00, 0.42, 1.0):
                    xcenter 393
                    ycenter 134
                add Solid("#ff386870") xysize (760, 4) at msbf_phase3_fault_line(31.0, 0.22, 0.54, -1.0):
                    xcenter 393
                    ycenter 318
                add Solid("#a66bff42") xysize (680, 3) at msbf_phase3_fault_line(-42.0, 0.54, 0.34, 1.0):
                    xcenter 393
                    ycenter 228
                add Solid("#ffffff70") xysize (470, 3) at msbf_phase3_tornado_streak(393, 229, 330, 84, 0.00, 0.44, 1.0)
                add Solid("#ff3868a0") xysize (420, 4) at msbf_phase3_tornado_streak(393, 236, 290, 112, 0.18, 0.52, -1.0)
                add Solid("#a66bff76") xysize (360, 3) at msbf_phase3_tornado_streak(393, 218, 250, 72, 0.36, 0.36, 1.0)
                add Solid("#ffffffd0") xysize (24, 6) at msbf_phase3_tornado_debris(393, 229, 330, 92, 0.03, 0.78, 1.0, 0.92)
                add Solid("#ff3868dc") xysize (18, 8) at msbf_phase3_tornado_debris(393, 226, 292, 76, 0.15, 0.82, -1.0, 1.0)
                add Solid("#050006e8") xysize (34, 8) at msbf_phase3_tornado_debris(393, 238, 358, 122, 0.30, 0.72, 1.0, 1.12)
                add Solid("#a66bffcc") xysize (16, 6) at msbf_phase3_tornado_debris(393, 216, 240, 64, 0.48, 0.64, -1.0, 0.86)
                add Solid("#f5fbffcc") xysize (30, 7) at msbf_phase3_tornado_debris(393, 250, 370, 136, 0.66, 0.62, 1.0, 1.04)
                add Solid("#ffffff44") xysize (786, 2) at msbf_phase3_static_slice(0.08, 0.34, 1.0):
                    ypos 92
                add Solid("#ff38685a") xysize (786, 4) at msbf_phase3_static_slice(0.28, 0.42, -1.0):
                    ypos 372
            else:
                add Solid("#55ddff18") xysize (1, 428):
                    xpos 72
                    ypos 14
                add Solid("#55ddff18") xysize (1, 428):
                    xpos 714
                    ypos 14
                add Solid("#55ddff18") xysize (746, 1):
                    xpos 20
                    ypos 86
                add Solid("#55ddff18") xysize (746, 1):
                    xpos 20
                    ypos 372

            if battle.phase == 3:
                add Solid("#ff3868") xysize (340, 4) at msbf_stage_sweep_fast(0.0):
                    ypos 104
                add Solid("#ffffff") xysize (740, 3) at msbf_stage_glitch(0.20):
                    xpos 24
                    ypos 178
                add Solid("#a66bff") xysize (280, 3) at msbf_stage_sweep_fast(0.52):
                    ypos 326
            else:
                add Solid("#55ddff") xysize (210, 3) at msbf_stage_sweep(0.0)
                add Solid("#ff3868") xysize (160, 3) at msbf_stage_sweep(0.7)
                add Solid("#ffffff") xysize (700, 2) at msbf_stage_glitch(0.45):
                    xpos 44
                    ypos 128
                add Solid("#55ddff") xysize (120, 2) at msbf_stage_sweep_fast(1.15):
                    ypos 330

            if battle.phase == 3:
                add Solid("#ff3868") xysize (4, 58) at msbf_stage_spark(0.0):
                    xpos 120
                    ypos 360
                add Solid("#ffffff") xysize (4, 52) at msbf_stage_spark(0.25):
                    xpos 612
                    ypos 362
                add Solid("#a66bff") xysize (4, 44) at msbf_stage_spark(0.68):
                    xpos 384
                    ypos 386
                add Solid("#ff3868aa") xysize (124, 3) at msbf_target_tick(0.0):
                    xcenter 393
                    ycenter 230
                add Solid("#ff3868aa") xysize (3, 124) at msbf_target_tick(0.12):
                    xcenter 393
                    ycenter 230
            else:
                add Solid("#55ddff") xysize (3, 38) at msbf_stage_spark(0.0):
                    xpos 90
                    ypos 378
                add Solid("#ff3868") xysize (3, 34) at msbf_stage_spark(0.4):
                    xpos 628
                    ypos 374
                add Solid("#ffcf66") xysize (3, 30) at msbf_stage_spark(0.9):
                    xpos 378
                    ypos 388

                add Solid("#55ddff66") xysize (92, 2) at msbf_target_tick(0.0):
                    xcenter 393
                    ycenter 230
                add Solid("#55ddff66") xysize (2, 92) at msbf_target_tick(0.2):
                    xcenter 393
                    ycenter 230

            if battle.phase == 3:
                add Solid("#ffffff40") xysize (560, 2) at msbf_phase3_tornado_streak(393, 229, 306, 46, 0.06, 0.30, 1.0)
                add Solid("#ff386866") xysize (610, 3) at msbf_phase3_tornado_streak(393, 229, 348, 132, 0.20, 0.42, -1.0)
                add Solid("#a66bff4a") xysize (500, 2) at msbf_phase3_tornado_streak(393, 229, 270, 156, 0.42, 0.28, 1.0)
                add Solid("#ffffff66") xysize (18, 4) at msbf_phase3_tornado_debris(393, 229, 210, 42, 0.10, 0.56, -1.0, 0.74)
                add Solid("#ff3868a8") xysize (26, 6) at msbf_phase3_tornado_debris(393, 229, 278, 118, 0.58, 0.68, 1.0, 0.92)
            elif battle.phase >= 2:
                add Solid("#ffcf6618") at msbf_phase2_bg_pulse(0.12, 0.13)
                add Solid("#00000050") xysize (760, 6) at msbf_phase2_stage_fault(-4.0, 0.14, 0.34):
                    xcenter 392
                    ycenter 92
                add Solid("#0314215a") xysize (690, 7) at msbf_phase2_stage_fault(21.0, 0.38, 0.30):
                    xcenter 402
                    ycenter 354
                add Solid("#19040a4c") xysize (640, 5) at msbf_phase2_stage_fault(-37.0, 0.68, 0.28):
                    xcenter 380
                    ycenter 246
                add Solid("#f5fbff64") xysize (720, 4) at msbf_phase2_stage_fault(-18.0, 0.02, 0.46):
                    xcenter 393
                    ycenter 126
                add Solid("#ff386858") xysize (660, 3) at msbf_phase2_stage_fault(14.0, 0.26, 0.38):
                    xcenter 396
                    ycenter 300
                add Solid("#ffcf6660") xysize (560, 3) at msbf_phase2_stage_fault(32.0, 0.52, 0.34):
                    xcenter 402
                    ycenter 214
                add Solid("#55ddff66") xysize (4, 350) at msbf_phase2_stage_lance(0.00, 0.48):
                    xpos 156
                    ypos 48
                add Solid("#f5fbff5c") xysize (5, 390) at msbf_phase2_stage_lance(0.22, 0.42):
                    xpos 392
                    ypos 20
                add Solid("#ffcf6658") xysize (4, 330) at msbf_phase2_stage_lance(0.44, 0.44):
                    xpos 624
                    ypos 72
                add Solid("#ff38684c") xysize (2, 428) at msbf_phase2_stage_lance(0.66, 0.34):
                    xpos 724
                    ypos 14
                add Solid("#ffcf6648") xysize (610, 2) at msbf_phase2_halo_line(0.0, 1.0, 0.34):
                    xcenter 393
                    ycenter 232
                add Solid("#f5fbff40") xysize (520, 2) at msbf_phase2_halo_line(0.25, -1.0, 0.24):
                    xcenter 393
                    ycenter 232
                add Solid("#ffcf6638") xysize (2, 345) at msbf_phase2_halo_line(0.10, -0.7, 0.28):
                    xcenter 393
                    ycenter 232
                add Solid("#55ddff34") xysize (690, 2) at msbf_phase2_halo_line(0.48, 1.35, 0.22):
                    xcenter 393
                    ycenter 232
                add Solid("#ff38682c") xysize (2, 402) at msbf_phase2_halo_line(0.64, -1.15, 0.20):
                    xcenter 393
                    ycenter 232
                add Solid("#f5fbff36") xysize (520, 3) at msbf_phase2_ray(-28.0, 0.0):
                    xcenter 393
                    ycenter 232
                add Solid("#ffcf6640") xysize (520, 3) at msbf_phase2_ray(24.0, 0.35):
                    xcenter 393
                    ycenter 232
                add Solid("#55ddff34") xysize (470, 3) at msbf_phase2_ray(58.0, 0.18):
                    xcenter 393
                    ycenter 232
                add Solid("#ff386830") xysize (480, 3) at msbf_phase2_ray(-62.0, 0.58):
                    xcenter 393
                    ycenter 232
                add Solid("#f5fbff50") xysize (38, 7) at msbf_phase2_eye(0.0):
                    xpos 118
                    ypos 124
                add Solid("#55ddffaa") xysize (12, 4) at msbf_phase2_eye(0.0):
                    xpos 131
                    ypos 126
                add Solid("#f5fbff50") xysize (42, 7) at msbf_phase2_eye(0.38):
                    xpos 625
                    ypos 140
                add Solid("#55ddffaa") xysize (12, 4) at msbf_phase2_eye(0.38):
                    xpos 640
                    ypos 142
                add Solid("#f5fbff44") xysize (34, 6) at msbf_phase2_eye(0.72):
                    xpos 210
                    ypos 332
                add Solid("#55ddff99") xysize (10, 3) at msbf_phase2_eye(0.72):
                    xpos 222
                    ypos 334
                add Solid("#f5fbff44") xysize (34, 6) at msbf_phase2_eye(1.05):
                    xpos 548
                    ypos 330
                add Solid("#55ddff99") xysize (10, 3) at msbf_phase2_eye(1.05):
                    xpos 560
                    ypos 332
                add Solid("#f5fbff50") xysize (48, 8) at msbf_phase2_eye(0.20):
                    xpos 368
                    ypos 74
                add Solid("#ffcf66aa") xysize (14, 4) at msbf_phase2_eye_sweep(0.20):
                    xpos 385
                    ypos 76
                add Solid("#f5fbff40") xysize (36, 6) at msbf_phase2_eye(0.86):
                    xpos 72
                    ypos 250
                add Solid("#ff386895") xysize (10, 3) at msbf_phase2_eye_sweep(0.86):
                    xpos 85
                    ypos 252
                add Solid("#f5fbff40") xysize (36, 6) at msbf_phase2_eye(1.18):
                    xpos 688
                    ypos 252
                add Solid("#ff386895") xysize (10, 3) at msbf_phase2_eye_sweep(1.18):
                    xpos 701
                    ypos 254

            if battle.phase == 3:
                add Solid("#ff3868") at msbf_boss_rupture_backlight:
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y - 2
                    xysize (570, 388)
                add Solid("#ffffff") at msbf_boss_rupture_backlight:
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y - 2
                    xysize (390, 300)
            else:
                add Solid("#55ddff") at msbf_boss_backlight:
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y - 2
                    xysize (520, 368)

            if battle.phase == 3:
                if battle.fx_event in ("final_victory", "phase"):
                    add battle.boss_art at msbf_boss_rupture_afterimage(-72, 38, 0.00, 0.30):
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                    add battle.boss_art at msbf_boss_rupture_afterimage(68, -44, 0.05, 0.26):
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                    add battle.boss_art at msbf_boss_rupture_hit:
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                elif battle.fx_event in ("hit", "weak", "crit"):
                    add battle.boss_art at msbf_boss_rupture_afterimage(-64, 24, 0.00, 0.30):
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                    add battle.boss_art at msbf_boss_rupture_afterimage(52, -34, 0.03, 0.24):
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                    add battle.boss_art at msbf_boss_rupture_hit:
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                elif battle.fx_event in ("enemy", "enemy_hit", "enemy_aoe", "enemy_buff", "enemy_guard", "enemy_weak", "enemy_crit", "enemy_resist", "shuffle", "resist"):
                    add battle.boss_art at msbf_boss_rupture_afterimage(-46, -30, 0.00, 0.24):
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                    add battle.boss_art at msbf_boss_rupture_afterimage(54, 28, 0.04, 0.22):
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                    add battle.boss_art at msbf_boss_rupture_cast:
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                else:
                    add battle.boss_art at msbf_boss_rupture_afterimage(-60, -20, 0.00, 0.24):
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                    add battle.boss_art at msbf_boss_rupture_afterimage(58, 32, 0.12, 0.20):
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                    add battle.boss_art at msbf_boss_rupture_afterimage(8, -56, 0.26, 0.16):
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
                    add battle.boss_art at msbf_boss_rupture_idle:
                        xcenter _boss_sprite_x
                        ycenter _boss_sprite_y
            elif battle.fx_event == "final_victory":
                add battle.boss_art at msbf_boss_echo(-1, 0.0):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_echo(1, 0.04):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_phase_break:
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
            elif battle.fx_event == "phase":
                add battle.boss_art at msbf_boss_echo(-1, 0.0):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_echo(1, 0.04):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_phase_break:
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
            elif battle.fx_event in ("shuffle", "resist"):
                add battle.boss_art at msbf_boss_echo(-1, 0.0):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_echo(1, 0.03):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_shuffle:
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
            elif battle.fx_event in ("hit", "weak", "crit"):
                add battle.boss_art at msbf_boss_echo(-1, 0.0):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_echo(1, 0.02):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_hit:
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
            elif battle.fx_event in ("enemy", "enemy_hit", "enemy_aoe", "enemy_buff", "enemy_guard", "enemy_weak", "enemy_crit", "enemy_resist"):
                add battle.boss_art at msbf_boss_echo(-1, 0.0):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_echo(1, 0.05):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_cast:
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
            elif battle.phase >= 2:
                add battle.boss_art at msbf_boss_phase_afterimage(-38, -18, 0.00, 0.18):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_phase_afterimage(34, 14, 0.24, 0.15):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_phase_afterimage(4, -34, 0.54, 0.13):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_phase_echo(-1, 0.80):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_phase_echo(1, 1.12):
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
                add battle.boss_art at msbf_boss_phase_idle:
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y
            else:
                add battle.boss_art at msbf_boss_idle:
                    xcenter _boss_sprite_x
                    ycenter _boss_sprite_y

    use msbf_fx_layer(battle)

    if battle.shmup_segment_active:
        use msbf_shmup_overlay(battle)

    if battle.phase >= 2 and not battle.phase_transition_active and not battle.final_victory_active and phase2_boom_active:
        if battle.phase == 3:
            use msbf_phase3_rupture_overlay(phase2_boom_kind)
        else:
            use msbf_phase2_boom_overlay(phase2_boom_kind)
        timer 0.68 action SetScreenVariable("phase2_boom_active", False)

    # Party and command deck.
    $ _party_compact = len(battle.party) > 4
    $ _party_grid_cols = 3 if _party_compact else 2
    $ _party_grid_rows = 3 if _party_compact else 2
    $ _party_grid_spacing = 5 if _party_compact else 7
    $ _party_card_w = 138 if _party_compact else 215
    $ _party_card_h = 48 if _party_compact else 61
    $ _party_frame_h = 198 if _party_compact else 184
    $ _party_sep_h = 174 if _party_compact else 160

    frame:
        xpos 40
        ypos 502
        xsize 1198
        ysize _party_frame_h
        background Solid("#07111ef2")
        padding (12, 10)
        at msbf_panel_enter(0.10), msbf_final_victory_rumble(1.0 if battle.final_victory_active else 0.0)

        hbox:
            spacing 12

            vbox:
                xsize 438
                spacing 7

                hbox:
                    xfill True
                    text "PARTY" style "msbf_panel_label"

                grid _party_grid_cols _party_grid_rows:
                    spacing _party_grid_spacing

                    for member in battle.party:
                        $ _active = _actor is not None and member.id == _actor.id
                        $ _targeting = pending_skill is not None
                        $ _targetable = _targeting and battle.can_target(pending_skill, member)
                        if _targeting:
                            button:
                                style "msbf_party_target_button"
                                xsize _party_card_w
                                ysize _party_card_h
                                sensitive _targetable
                                hover_sound MSBF_UI_SFX["hover"]
                                activate_sound MSBF_UI_SFX["accept"]
                                action [SetScreenVariable("pending_skill", None), SetScreenVariable("hovered_skill", None), Function(battle.player_use_skill, pending_skill, member)]

                                use msbf_party_card(member, _active, _targetable, _party_compact)
                        else:
                            use msbf_party_card(member, _active, False, _party_compact)

                    for _i in range(max(0, (_party_grid_cols * _party_grid_rows) - len(battle.party))):
                        null xsize _party_card_w ysize _party_card_h

            add Solid("#55ddff3a") xysize (1, _party_sep_h)

            vbox:
                xsize 701
                spacing 8

                if _actor:
                    hbox:
                        xfill True
                        vbox:
                            spacing 0
                            text "ACT: [_actor.name]" style "msbf_command_actor"
                            text "HP [_actor.hp]/[_actor.max_hp]   MP [_actor.mp]/[_actor.max_mp]" style "msbf_command_stats"

                        null xfill True

                        if pending_skill:
                            button:
                                style "msbf_pass_button"
                                hover_sound MSBF_UI_SFX["hover"]
                                activate_sound MSBF_UI_SFX["denied"]
                                action [SetScreenVariable("pending_skill", None), SetScreenVariable("hovered_skill", None)]
                                yalign 0.5
                                at msbf_button_focus

                                text "CANCEL" style "msbf_pass_button_text"
                        else:
                            button:
                                style "msbf_pass_button"
                                hover_sound MSBF_UI_SFX["hover"]
                                action [SetScreenVariable("hovered_skill", None), Function(battle.player_pass)]
                                yalign 0.5
                                at msbf_button_focus

                                text "PASS" style "msbf_pass_button_text"

                    grid 4 2:
                        spacing 7
                        xfill True

                        for skill in _actor.skills:
                            $ _enabled = battle.can_use(skill)

                            button:
                                style "msbf_skill_button"
                                sensitive _enabled
                                hover_sound MSBF_UI_SFX["hover"]
                                activate_sound MSBF_UI_SFX["accept"]
                                hovered SetScreenVariable("hovered_skill", skill)
                                unhovered SetScreenVariable("hovered_skill", None)
                                if pending_skill is skill:
                                    background Solid("#1d5c82ee")
                                if battle.skill_needs_ally_target(skill):
                                    action [SetScreenVariable("hovered_skill", skill), SetScreenVariable("pending_skill", skill)]
                                else:
                                    action [SetScreenVariable("hovered_skill", None), SetScreenVariable("pending_skill", None), Function(battle.player_use_skill, skill)]
                                at msbf_button_focus

                                hbox:
                                    spacing 6
                                    xfill True
                                    yalign 0.5
                                    text skill.name style ("msbf_skill_name" if _enabled else "msbf_skill_name_disabled"):
                                        xmaximum 116
                                        yalign 0.5
                                    text "[skill.cost]MP" style ("msbf_skill_cost" if _enabled else "msbf_skill_cost_disabled"):
                                        xalign 1.0
                                        yalign 0.5

                        for _i in range(max(0, 8 - len(_actor.skills))):
                            null xsize 170 ysize 38

                    if pending_skill and not battle.result:
                        text "Choose a target for [pending_skill.name]." style "msbf_tooltip":
                            xmaximum 700
                    elif hovered_skill and not battle.result:
                        text hovered_skill.description style "msbf_tooltip":
                            xmaximum 700
                    else:
                        text "Pass spends half a turn. Haste can steal one half-turn before Matsuda changes rhythm." style "msbf_hint":
                            xmaximum 700

                else:
                    text "Resolving..." style "msbf_command_actor"

    if battle.phase >= 2:
        add Solid("#ffcf6630") xysize (392, 2) at msbf_phase2_scanline_burst(0.12):
            xpos 40
            ypos 34
        add Solid("#ff38682c") xysize (392, 2) at msbf_phase2_scanline_burst(0.56):
            xpos 40
            ypos 486
        add Solid("#55ddff30") xysize (1198, 2) at msbf_phase2_scanline_burst(0.28):
            xpos 40
            ypos 504
        add Solid("#ffcf6628") xysize (1198, 2) at msbf_phase2_scanline_burst(0.74):
            xpos 40
            ypos 684
        add Solid("#ffffff20") xysize (420, 3) at msbf_phase2_stage_fault(-8.0, 0.20, 0.28):
            xcenter 230
            ycenter 352
        add Solid("#ff386820") xysize (760, 3) at msbf_phase2_stage_fault(5.0, 0.48, 0.24):
            xcenter 842
            ycenter 594
        add Solid("#55ddff20") xysize (4, 170) at msbf_phase2_stage_lance(0.36, 0.24):
            xpos 452
            ypos 506
        add Solid("#ffcf6624") xysize (4, 170) at msbf_phase2_stage_lance(0.62, 0.22):
            xpos 1236
            ypos 506
        if battle.phase == 3:
            add Solid("#ff386840") xysize (1198, 3) at msbf_phase3_static_slice(0.04, 0.34, 1.0):
                xpos 40
                ypos 512
            add Solid("#ffffff24") xysize (1198, 2) at msbf_phase3_static_slice(0.26, 0.26, -1.0):
                xpos 40
                ypos 692
            add Solid("#a66bff20") xysize (392, 3) at msbf_phase3_fault_line(-8.0, 0.12, 0.24, 1.0):
                xcenter 236
                ycenter 486
            add Solid("#ff386826") xysize (760, 3) at msbf_phase3_fault_line(11.0, 0.32, 0.28, -1.0):
                xcenter 844
                ycenter 604

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

screen msbf_meter(value, max_value, width, height, fill_color, empty_color):
    frame:
        xysize (width, height)
        padding (0, 0)
        background Solid(empty_color)
        add Solid(fill_color) xysize (msbf_bar_width(value, max_value, width), height)

screen msbf_party_card(member, active=False, targetable=False, compact=False):
    $ _card_w = 138 if compact else 215
    $ _card_h = 48 if compact else 61
    $ _inner_w = _card_w - 14
    $ _inner_h = _card_h - 12
    $ _bar_w = _inner_w - 21
    $ _name_max = 72 if compact else 118
    $ _bar_y = 19 if compact else 22
    $ _stat_y = 26 if compact else 31
    $ _note_y = 36 if compact else 41

    frame:
        xsize _card_w
        ysize _card_h
        background Solid("#1f5c83f0" if targetable else ("#153f5ef0" if active else "#091523e4"))
        padding (7, 6)

        fixed:
            xysize (_inner_w, _inner_h)

            add Solid("#66e08a" if targetable else ("#55ddff" if active else ("#ffcf66" if member.row == "front" else "#4d6f85"))) xysize (4 if compact else 5, _inner_h)

            text member.name style (("msbf_party_name_compact" if member.alive else "msbf_party_name_down_compact") if compact else ("msbf_party_name" if member.alive else "msbf_party_name_down")):
                xpos 14
                ypos -1
                xmaximum _name_max

            text msbf_row_label(member.row) style ("msbf_party_row_tag_compact" if compact else "msbf_party_row_tag"):
                xalign 1.0
                ypos 1

            frame:
                xpos 14
                ypos _bar_y
                xysize (_bar_w, 6 if not compact else 5)
                padding (0, 0)
                background Solid("#141923")
                add Solid("#66e08a") xysize (msbf_bar_width(member.hp, member.max_hp, _bar_w), 6 if not compact else 5)

            text "HP [member.hp]/[member.max_hp]" style ("msbf_party_stat_compact" if compact else "msbf_party_stat"):
                xpos 14
                ypos _stat_y

            text ("MP [member.mp]" if compact else "MP [member.mp]/[member.max_mp]") style ("msbf_party_stat_compact" if compact else "msbf_party_stat"):
                xalign 1.0
                ypos _stat_y

            if not member.alive:
                text "DOWN" style ("msbf_down_text_compact" if compact else "msbf_down_text"):
                    xpos 14
                    ypos _note_y
            elif member.guard:
                text "GUARD" style ("msbf_guard_tag_compact" if compact else "msbf_guard_tag"):
                    xpos 14
                    ypos _note_y
            elif member.focus:
                text "FOCUS" style ("msbf_focus_tag_compact" if compact else "msbf_focus_tag"):
                    xpos 14
                    ypos _note_y
            else:
                text getattr(member, "role", "") style ("msbf_party_role_compact" if compact else "msbf_party_role"):
                    xpos 14
                    ypos _note_y
                    xmaximum _bar_w

style msbf_title:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
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

style msbf_boss_name:
    size 24
    color "#f5fbff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

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
    size 12
    color "#f5fbff"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_name_down_compact:
    size 12
    color "#6b727a"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_role:
    size 9
    color "#8fb1c0"
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_role_compact:
    size 7
    color "#8fb1c0"
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_row_tag:
    size 9
    color "#ffcf66"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_row_tag_compact:
    size 7
    color "#ffcf66"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_stat:
    size 8
    color "#c5d8e4"
    outlines [(1, "#02040b", 0, 0)]

style msbf_party_stat_compact:
    size 7
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
    size 7
    color "#66e08a"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_focus_tag:
    size 9
    color "#ffcf66"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_focus_tag_compact:
    size 7
    color "#ffcf66"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_down_text:
    size 9
    color "#ff3868"
    bold True
    outlines [(1, "#02040b", 0, 0)]

style msbf_down_text_compact:
    size 7
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

style msbf_skill_button is button:
    xsize 170
    ysize 38
    background Solid("#102338")
    hover_background Solid("#1d5c82")
    insensitive_background Solid("#0b1118")
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
    xsize 96
    ysize 32
    background Solid("#1d5c82")
    hover_background Solid("#2c7fac")
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
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 42
    color "#ffcf66"
    bold True
    outlines [(3, "#02040b", 0, 0), (1, "#ffffffcc", 0, 0)]

style msbf_fx_crit:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 42
    color "#ffffff"
    bold True
    outlines [(3, "#02040b", 0, 0), (1, "#ff3868cc", 0, 0)]

style msbf_fx_resist:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 38
    color "#9aa7b7"
    bold True
    outlines [(3, "#02040b", 0, 0)]

style msbf_fx_heal:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 36
    color "#66e08a"
    bold True
    outlines [(3, "#02040b", 0, 0)]

style msbf_fx_scan:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 38
    color "#55ddff"
    bold True
    outlines [(3, "#02040b", 0, 0), (1, "#ffffffaa", 0, 0)]

style msbf_fx_phase:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 50
    color "#ff3868"
    bold True
    outlines [(4, "#02040b", 0, 0), (1, "#ffffffaa", 0, 0)]

style msbf_phase_transition_title:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 56
    color "#ffffff"
    bold True
    outlines [(5, "#02040b", 0, 0), (2, "#ff3868cc", 0, 0), (1, "#ffcf66aa", 0, 0)]

style msbf_phase_transition_subtitle:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 25
    color "#f5fbff"
    bold True
    outlines [(3, "#02040b", 0, 0), (1, "#55ddffaa", 0, 0)]

style msbf_phase_transition_breathe_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 48
    color "#ffffff"
    bold True
    outlines [(4, "#02040b", 0, 0), (1, "#ffcf66dd", 0, 0)]
