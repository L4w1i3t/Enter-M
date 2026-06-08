

transform tcommon(x=640, z=0.80):
    subpixel True transform_anchor True
    on show:
        yanchor 1.0 ypos 1.03
        xcenter x + 36 xoffset 0
        yoffset 14
        zoom z*0.970 alpha 0.00
        parallel:
            easein_cubic .30 xcenter x zoom z*1.00
        parallel:
            easein_cubic .24 yoffset 0
        parallel:
            linear .16 alpha 1.00
    on replace:
        parallel:
            easein_cubic .30 xcenter x xoffset 0 zoom z*1.00
        parallel:
            easein_cubic .24 yanchor 1.0 ypos 1.03 yoffset 0
        parallel:
            linear .16 alpha 1.00
    on default:
        xcenter x xoffset 0
        yanchor 1.0 ypos 1.03 yoffset 0
        zoom z*1.00 alpha 1.00

transform tinstant(x=640, z=0.80):
    xcenter x xoffset 0 yoffset 0 zoom z*1.00 alpha 1.00 yanchor 1.0 ypos 1.03 subpixel True transform_anchor True

transform focus(x=640, z=0.80):
    subpixel True transform_anchor True
    on show:
        yanchor 1.0 ypos 1.03
        xcenter x + 30 xoffset 0
        yoffset 12
        zoom z*0.975 alpha 0.00
        parallel:
            easein_cubic .30 xcenter x zoom z*1.045
        parallel:
            easein_cubic .24 yoffset -5
        parallel:
            linear .14 alpha 1.00
    on replace:
        parallel:
            easein_cubic .28 xcenter x xoffset 0 zoom z*1.045
        parallel:
            easein_cubic .22 yanchor 1.0 ypos 1.03 yoffset -5
        parallel:
            linear .14 alpha 1.00
    on default:
        xcenter x xoffset 0
        yanchor 1.0 ypos 1.03 yoffset -5
        zoom z*1.045 alpha 1.00

transform sink(x=640, z=0.80):
    xcenter x xoffset 0 yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True transform_anchor True
    easein_quad .36 yoffset 12 alpha 0.88

transform hop(x=640, z=0.80):
    xcenter x xoffset 0 yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True transform_anchor True
    easein_cubic .10 yoffset -10 zoom z*1.012
    ease .12 yoffset 0 zoom z*1.00

transform hopfocus(x=640, z=0.80):
    xcenter x xoffset 0 yoffset -5 yanchor 1.0 ypos 1.03 zoom z*1.045 alpha 1.00 subpixel True transform_anchor True
    easein_cubic .10 yoffset -12 zoom z*1.055
    ease .12 yoffset -5 zoom z*1.045

transform dip(x=640, z=0.80):
    xcenter x xoffset 0 yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True transform_anchor True
    easein_quad .16 yoffset 14
    easeout_quad .22 yoffset 0

transform panic(x=640, z=0.80):
    xcenter x xoffset 0 yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True transform_anchor True
    parallel:
        ease 1.2 yoffset 18
        ease 1.2 yoffset 0
        repeat
    parallel:
        easein_quad .3 xoffset 14
        ease .6 xoffset -14
        easeout_quad .3 xoffset 0
        repeat

transform leftin(x=640, z=0.80):
    xcenter x - 90 xoffset 0 yoffset 16 yanchor 1.0 ypos 1.03 zoom z*0.965 alpha 0.00 subpixel True transform_anchor True
    parallel:
        easein_cubic .36 xcenter x zoom z*1.00
    parallel:
        easein_cubic .28 yoffset 0
    parallel:
        linear .18 alpha 1.00

transform leftfocus(x=640, z=0.80):
    xcenter x - 90 xoffset 0 yoffset 16 yanchor 1.0 ypos 1.03 zoom z*0.965 alpha 0.00 subpixel True transform_anchor True
    parallel:
        easein_cubic .36 xcenter x zoom z*1.045
    parallel:
        easein_cubic .28 yoffset -5
    parallel:
        linear .18 alpha 1.00


transform thide(z=0.80):
    subpixel True
    transform_anchor True
    on hide:

        easein_quad .24 zoom z*0.975 alpha 0.00 yoffset 12
transform lhide:
    subpixel True
    on hide:
        easein_quad .26 xoffset -64 alpha 0.00

# Reusable scene language for original VN direction: tone overlays and small
# character beats that can be applied without one-off ATL blocks.
transform ambient_overlay(a=0.22, fade=0.45):
    alpha 0.0
    linear fade alpha a

transform ambient_vignette(a=0.24):
    truecenter
    alpha 0.0
    easein_quad 0.45 alpha a

transform bg_slow_push(z=1.035, duration=18.0):
    subpixel True
    truecenter
    zoom z
    block:
        ease duration xoffset -18 yoffset 10
        ease duration xoffset 14 yoffset -8
        repeat

transform scene_breathe(a=0.10):
    alpha 0.0
    ease 1.2 alpha a
    block:
        ease 3.4 alpha a * 0.62
        ease 3.4 alpha a
        repeat


transform t41:
    tcommon(200)
transform t42:
    tcommon(493)
transform t43:
    tcommon(786)
transform t44:
    tcommon(1080)
transform t31:
    tcommon(240)
transform t32:
    tcommon(640)
transform t33:
    tcommon(1040)
transform t21:
    tcommon(400)
transform t22:
    tcommon(880)
transform t11:
    tcommon(640)

transform i41:
    tinstant(200)
transform i42:
    tinstant(493)
transform i43:
    tinstant(786)
transform i44:
    tinstant(1080)
transform i31:
    tinstant(240)
transform i32:
    tinstant(640)
transform i33:
    tinstant(1040)
transform i21:
    tinstant(400)
transform i22:
    tinstant(880)
transform i11:
    tinstant(640)

transform f41:
    focus(200)
transform f42:
    focus(493)
transform f43:
    focus(786)
transform f44:
    focus(1080)
transform f31:
    focus(240)
transform f32:
    focus(640)
transform f33:
    focus(1040)
transform f21:
    focus(400)
transform f22:
    focus(880)
transform f11:
    focus(640)

transform s41:
    sink(200)
transform s42:
    sink(493)
transform s43:
    sink(786)
transform s44:
    sink(1080)
transform s31:
    sink(240)
transform s32:
    sink(640)
transform s33:
    sink(1040)
transform s21:
    sink(400)
transform s22:
    sink(880)
transform s11:
    sink(640)

transform h41:
    hop(200)
transform h42:
    hop(493)
transform h43:
    hop(786)
transform h44:
    hop(1080)
transform h31:
    hop(240)
transform h32:
    hop(640)
transform h33:
    hop(1040)
transform h21:
    hop(400)
transform h22:
    hop(880)
transform h11:
    hop(640)

transform hf41:
    hopfocus(200)
transform hf42:
    hopfocus(493)
transform hf43:
    hopfocus(786)
transform hf44:
    hopfocus(1080)
transform hf31:
    hopfocus(240)
transform hf32:
    hopfocus(640)
transform hf33:
    hopfocus(1040)
transform hf21:
    hopfocus(400)
transform hf22:
    hopfocus(880)
transform hf11:
    hopfocus(640)

transform d41:
    dip(200)
transform d42:
    dip(493)
transform d43:
    dip(786)
transform d44:
    dip(1080)
transform d31:
    dip(240)
transform d32:
    dip(640)
transform d33:
    dip(1040)
transform d21:
    dip(400)
transform d22:
    dip(880)
transform d11:
    dip(640)

transform l41:
    leftin(200)
transform l42:
    leftin(493)
transform l43:
    leftin(786)
transform l44:
    leftin(1080)
transform l31:
    leftin(240)
transform l32:
    leftin(640)
transform l33:
    leftin(1040)
transform l21:
    leftin(400)
transform l22:
    leftin(880)
transform l11:
    leftin(640)

transform lf41:
    leftfocus(200)
transform lf42:
    leftfocus(493)
transform lf43:
    leftfocus(786)
transform lf44:
    leftfocus(1080)
transform lf31:
    leftfocus(240)
transform lf32:
    leftfocus(640)
transform lf33:
    leftfocus(1040)
transform lf21:
    leftfocus(400)
transform lf22:
    leftfocus(880)
transform lf11:
    leftfocus(640)

transform present41:
    present(200)
transform present42:
    present(493)
transform present43:
    present(786)
transform present44:
    present(1080)
transform present31:
    present(240)
transform present32:
    present(640)
transform present33:
    present(1040)
transform present21:
    present(400)
transform present22:
    present(880)
transform present11:
    present(640)

transform nod41:
    small_nod(200)
transform nod42:
    small_nod(493)
transform nod43:
    small_nod(786)
transform nod44:
    small_nod(1080)
transform nod31:
    small_nod(240)
transform nod32:
    small_nod(640)
transform nod33:
    small_nod(1040)
transform nod21:
    small_nod(400)
transform nod22:
    small_nod(880)
transform nod11:
    small_nod(640)

transform flinch41:
    flinch(200)
transform flinch42:
    flinch(493)
transform flinch43:
    flinch(786)
transform flinch44:
    flinch(1080)
transform flinch31:
    flinch(240)
transform flinch32:
    flinch(640)
transform flinch33:
    flinch(1040)
transform flinch21:
    flinch(400)
transform flinch22:
    flinch(880)
transform flinch11:
    flinch(640)

transform stepback41:
    step_back(200)
transform stepback42:
    step_back(493)
transform stepback43:
    step_back(786)
transform stepback44:
    step_back(1080)
transform stepback31:
    step_back(240)
transform stepback32:
    step_back(640)
transform stepback33:
    step_back(1040)
transform stepback21:
    step_back(400)
transform stepback22:
    step_back(880)
transform stepback11:
    step_back(640)

transform bow41:
    bow(200)
transform bow42:
    bow(493)
transform bow43:
    bow(786)
transform bow44:
    bow(1080)
transform bow31:
    bow(240)
transform bow32:
    bow(640)
transform bow33:
    bow(1040)
transform bow21:
    bow(400)
transform bow22:
    bow(880)
transform bow11:
    bow(640)

transform idle41:
    idle_breathe(200)
transform idle42:
    idle_breathe(493)
transform idle43:
    idle_breathe(786)
transform idle44:
    idle_breathe(1080)
transform idle31:
    idle_breathe(240)
transform idle32:
    idle_breathe(640)
transform idle33:
    idle_breathe(1040)
transform idle21:
    idle_breathe(400)
transform idle22:
    idle_breathe(880)
transform idle11:
    idle_breathe(640)


transform face(z=0.80, y=500):
    subpixel True
    xcenter 640
    yanchor 1.0 ypos 1.03
    yoffset y
    zoom z*2.00

transform cgfade:
    on show:
        alpha 0.0
        linear 0.5 alpha 1.0
    on hide:
        alpha 1.0
        linear 0.5 alpha 0.0

transform n_cg2_wiggle:
    subpixel True
    xoffset 0
    easein 0.15 xoffset 20
    easeout 0.15 xoffset 0
    easein 0.15 xoffset -15
    easeout 0.15 xoffset 0
    easein 0.15 xoffset 10
    easeout 0.15 xoffset 0
    easein 0.15 xoffset -5
    ease 0.15 xoffset 0

transform n_cg2_wiggle_loop:
    n_cg2_wiggle
    1.0
    repeat

transform n_cg2_zoom:
    subpixel True
    truecenter
    xoffset 0
    easeout 0.20 zoom 2.5 xoffset 200


define dissolve = Dissolve(0.28)

define dissolve_cg = Dissolve(0.70)
define dissolve_scene = Dissolve(0.85)

define dissolve_scene_full = MultipleTransition([
    False, Dissolve(0.45),
    Solid("#02050a"), Pause(0.28),
    Solid("#02050a"), Dissolve(0.58),
    True])

define dissolve_scene_half = MultipleTransition([
    Solid("#02050a"), Pause(0.22),
    Solid("#02050a"), Dissolve(0.48),
    True])

define close_eyes = MultipleTransition([
    False, Dissolve(0.36),
    Solid("#02050a"), Pause(0.18),
    True])

define open_eyes = MultipleTransition([
    False, Dissolve(0.42),
    True])

define trueblack = MultipleTransition([
    Solid("#02050a"), Pause(0.25),
    Solid("#02050a")
    ])


define wipeleft = CropMove(0.46, "slideleft")


define wipeleft_scene = MultipleTransition([
    False, CropMove(0.42, "slideleft"),
    Solid("#02050a"), Pause(0.14),
    Solid("#02050a"), CropMove(0.42, "slideright"),
    True])

define dissolve_scene_soft = MultipleTransition([
    False, Dissolve(0.38),
    Solid("#02050a"), Pause(0.12),
    Solid("#02050a"), Dissolve(0.48),
    True])

define fade_scene_night = Fade(0.40, 0.18, 0.50, color="#02050a")

define tpause = Pause(0.25)

image mood_afternoon = Solid("#ffd88a18")
image mood_evening = Solid("#d7864a20")
image mood_night = Solid("#07163350")
image mood_home = Solid("#cdecc820")
image mood_overcast = Solid("#8fb0c926")
image mood_pressure = Solid("#10152866")

image noise:
    truecenter
    "images/bg/noise1.jpg"
    pause 0.1
    "images/bg/noise2.jpg"
    pause 0.1
    "images/bg/noise3.jpg"
    pause 0.1
    "images/bg/noise4.jpg"
    pause 0.1
    xzoom -1
    "images/bg/noise1.jpg"
    pause 0.1
    "images/bg/noise2.jpg"
    pause 0.1
    "images/bg/noise3.jpg"
    pause 0.1
    "images/bg/noise4.jpg"
    pause 0.1
    yzoom -1
    "images/bg/noise1.jpg"
    pause 0.1
    "images/bg/noise2.jpg"
    pause 0.1
    "images/bg/noise3.jpg"
    pause 0.1
    "images/bg/noise4.jpg"
    pause 0.1
    xzoom 1
    "images/bg/noise1.jpg"
    pause 0.1
    "images/bg/noise2.jpg"
    pause 0.1
    "images/bg/noise3.jpg"
    pause 0.1
    "images/bg/noise4.jpg"
    pause 0.1
    yzoom 1
    repeat

transform noise_alpha:
    alpha 0.25

transform noisefade(t=0):
    alpha 0.0
    t
    linear 5.0 alpha 0.40

image vignette:
    truecenter
    "images/bg/vignette.png"

transform vignettefade(t=0):
    alpha 0.0
    t
    linear 25.0 alpha 1.00

transform vignetteflicker(t=0):
    alpha 0.0
    t + 2.030
    parallel:
        alpha 1.00
        linear 0.2 alpha 0.8
        0.1
        alpha 0.7
        linear 0.1 alpha 1.00
        alpha 0.0
        1.19
        repeat
    parallel:
        easeout 20 zoom 3.0

transform layerflicker(t=0):
    truecenter
    t + 2.030
    parallel:
        zoom 1.05
        linear 0.2 zoom 1.04
        0.1
        zoom 1.035
        linear 0.1 zoom 1.05
        zoom 1.0
        1.19
        repeat
    parallel:
        easeout_bounce 0.3 xalign 0.6
        easeout_bounce 0.3 xalign 0.4
        repeat

transform rewind:
    truecenter
    zoom 1.20
    parallel:
        easeout_bounce 0.2 xalign 0.55
        easeout_bounce 0.2 xalign 0.45
        repeat
    parallel:
        easeout_bounce 0.33 yalign 0.55
        easeout_bounce 0.33 yalign 0.45
        repeat

transform heartbeat:
    heartbeat2(1)

transform heartbeat2(m):
    truecenter
    parallel:
        0.144
        zoom 1.00 + 0.07 * m
        easein 0.250 zoom 1.00 + 0.04 * m
        easeout 0.269 zoom 1.00 + 0.07 * m
        zoom 1.00
        1.479
        repeat
    parallel:
        easeout_bounce 0.3 xalign 0.5 + 0.02 * m
        easeout_bounce 0.3 xalign 0.5 - 0.02 * m
        repeat

transform yuripupils_move:
    function yuripupils_function

init python:
    def yuripupils_function(trans, st, at):
        trans.xoffset = -1 + random.random() * 9 - 4
        trans.yoffset = 3 + random.random() * 6 - 3
        return random.random() * 1.2 + 0.3

transform malpha(a=1.00):
    i11
    alpha a
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
