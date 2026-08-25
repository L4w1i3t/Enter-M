# =============================================================================
# ENTER-M :: SPRITE SLOT TABLE
# -----------------------------------------------------------------------------
# Vanilla DDLC's sprite placement vocabulary and NOTHING ELSE. The generators
# (tcommon / tinstant / focus / sink / hop / hopfocus / leftin / leftfocus /
# thide) and the numbered slots built from them:
#
#     txx   arrive / move to slot          ixx   snap to slot, no animation
#     fxx   arrive, focused (nearer)       sxx   sink back
#     hxx   hop in place                   hfxx  hop, focused
#     lxx   slide in from the left         lfxx  slide in from the left, focused
#     thide leave
#
# The digits are <how many on stage><which position>: t42 is slot 2 of a
# four-person stage. Stages of ONE THROUGH SIX are defined. Retuned for this
# project (easing, timing, subpixel), but the names, the slot maths and the
# roles are vanilla.
#
# THE SLOT X *IS* THE PANEL CENTRE.
# game/stage_panels.rpy cuts the background into one panel per on-stage
# character, and these two tables are one piece of geometry read twice: an
# N-person stage divides the 1280px screen into N equal panels, and slot i
# stands in the middle of panel i --
#
#     x = (i - 0.5) / N * 1280
#
# -- so a character is never crowded against a gutter nor marooned at a screen
# edge, whichever way the room is split. (The 2-up slots used to sit at 400/880,
# 80px INSIDE their panel centres, which stood both characters shoulder to
# shoulder against the middle cut with the whole outer half of each panel
# empty.) The values are mirrored in ENTER_M_PANEL_SLOT_X over there because an
# ATL block's call arguments are not readable from Python. MOVE A SLOT HERE AND
# YOU MUST MOVE IT THERE TOO -- a stale entry does not crash, it just puts the
# cut in the wrong place.
#
# z FALLS AS THE STAGE FILLS. One panel is a whole screen; six panels are 213px
# apiece, and this cast's sprites are 300-440px wide. So past four people the
# staging scales down to keep each sprite inside its own frame -- a wider shot
# holds smaller subjects, which is what a camera would do anyway. Stages of 1-3
# keep the established z=0.80 and are pixel-identical to what they always were
# except for the x.
#
# EVERYTHING ELSE MOVED TO fx.rpy. Screen shakes, flashes, breathing idles,
# camera pushes, flinches, the scene transitions, and the inherited vanilla
# odds and ends (noise / vignette / yuripupils) all live there now, so that this
# file stays a table you can read at a glance. Add new sprite slots here; add
# effects there.
# =============================================================================

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

# The slide-in lives in `on show` and NOT in a bare body, so that a later
# attribute-only show cannot replay the entrance. config.sticky_positions
# (Autofocus) re-injects the previous at_list into every attribute-carrying
# show, which restarts the ATL from frame zero -- a bare body would re-run its
# absolute start values (off-screen left, alpha 0) and slide the character in
# a second time. `on replace` settles from wherever the sprite already is, the
# same way tcommon does. See fx.rpy's header for the engine detail.
transform leftin(x=640, z=0.80):
    subpixel True transform_anchor True
    on show:
        yanchor 1.0 ypos 1.03
        xcenter x - 90 xoffset 0
        yoffset 16
        zoom z*0.965 alpha 0.00
        parallel:
            easein_cubic .36 xcenter x zoom z*1.00
        parallel:
            easein_cubic .28 yoffset 0
        parallel:
            linear .18 alpha 1.00
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

# Same restart-proofing as leftin, settling to the focused pose.
transform leftfocus(x=640, z=0.80):
    subpixel True transform_anchor True
    on show:
        yanchor 1.0 ypos 1.03
        xcenter x - 90 xoffset 0
        yoffset 16
        zoom z*0.965 alpha 0.00
        parallel:
            easein_cubic .36 xcenter x zoom z*1.045
        parallel:
            easein_cubic .28 yoffset -5
        parallel:
            linear .18 alpha 1.00
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


# The exit carries NO zoom. `on hide` interpolates from wherever the sprite
# already is, so an absolute target here would be read as "scale to 0.78"
# rather than "shrink a little" -- which on a five- or six-person stage, where
# the staging z is 0.68 or 0.63, made a leaving sprite balloon by a quarter on
# its way out. Sinking and fading reads the same and is scale-agnostic.
transform thide(z=0.80):
    subpixel True
    transform_anchor True
    on hide:

        easein_quad .24 alpha 0.00 yoffset 12
transform t61:
    tcommon(107, 0.63)
transform t62:
    tcommon(320, 0.63)
transform t63:
    tcommon(533, 0.63)
transform t64:
    tcommon(747, 0.63)
transform t65:
    tcommon(960, 0.63)
transform t66:
    tcommon(1173, 0.63)
transform t51:
    tcommon(128, 0.68)
transform t52:
    tcommon(384, 0.68)
transform t53:
    tcommon(640, 0.68)
transform t54:
    tcommon(896, 0.68)
transform t55:
    tcommon(1152, 0.68)
transform t41:
    tcommon(160, 0.74)
transform t42:
    tcommon(480, 0.74)
transform t43:
    tcommon(800, 0.74)
transform t44:
    tcommon(1120, 0.74)
transform t31:
    tcommon(213)
transform t32:
    tcommon(640)
transform t33:
    tcommon(1067)
transform t21:
    tcommon(320)
transform t22:
    tcommon(960)
transform t11:
    tcommon(640)

transform i61:
    tinstant(107, 0.63)
transform i62:
    tinstant(320, 0.63)
transform i63:
    tinstant(533, 0.63)
transform i64:
    tinstant(747, 0.63)
transform i65:
    tinstant(960, 0.63)
transform i66:
    tinstant(1173, 0.63)
transform i51:
    tinstant(128, 0.68)
transform i52:
    tinstant(384, 0.68)
transform i53:
    tinstant(640, 0.68)
transform i54:
    tinstant(896, 0.68)
transform i55:
    tinstant(1152, 0.68)
transform i41:
    tinstant(160, 0.74)
transform i42:
    tinstant(480, 0.74)
transform i43:
    tinstant(800, 0.74)
transform i44:
    tinstant(1120, 0.74)
transform i31:
    tinstant(213)
transform i32:
    tinstant(640)
transform i33:
    tinstant(1067)
transform i21:
    tinstant(320)
transform i22:
    tinstant(960)
transform i11:
    tinstant(640)

transform f61:
    focus(107, 0.63)
transform f62:
    focus(320, 0.63)
transform f63:
    focus(533, 0.63)
transform f64:
    focus(747, 0.63)
transform f65:
    focus(960, 0.63)
transform f66:
    focus(1173, 0.63)
transform f51:
    focus(128, 0.68)
transform f52:
    focus(384, 0.68)
transform f53:
    focus(640, 0.68)
transform f54:
    focus(896, 0.68)
transform f55:
    focus(1152, 0.68)
transform f41:
    focus(160, 0.74)
transform f42:
    focus(480, 0.74)
transform f43:
    focus(800, 0.74)
transform f44:
    focus(1120, 0.74)
transform f31:
    focus(213)
transform f32:
    focus(640)
transform f33:
    focus(1067)
transform f21:
    focus(320)
transform f22:
    focus(960)
transform f11:
    focus(640)

# Only slot 11 of the sink family is used (ch_mika); the rest were dead.
transform s11:
    sink(640)

transform h61:
    hop(107, 0.63)
transform h62:
    hop(320, 0.63)
transform h63:
    hop(533, 0.63)
transform h64:
    hop(747, 0.63)
transform h65:
    hop(960, 0.63)
transform h66:
    hop(1173, 0.63)
transform h51:
    hop(128, 0.68)
transform h52:
    hop(384, 0.68)
transform h53:
    hop(640, 0.68)
transform h54:
    hop(896, 0.68)
transform h55:
    hop(1152, 0.68)
transform h41:
    hop(160, 0.74)
transform h42:
    hop(480, 0.74)
transform h43:
    hop(800, 0.74)
transform h44:
    hop(1120, 0.74)
transform h31:
    hop(213)
transform h32:
    hop(640)
transform h33:
    hop(1067)
transform h21:
    hop(320)
transform h22:
    hop(960)
transform h11:
    hop(640)

transform hf61:
    hopfocus(107, 0.63)
transform hf62:
    hopfocus(320, 0.63)
transform hf63:
    hopfocus(533, 0.63)
transform hf64:
    hopfocus(747, 0.63)
transform hf65:
    hopfocus(960, 0.63)
transform hf66:
    hopfocus(1173, 0.63)
transform hf51:
    hopfocus(128, 0.68)
transform hf52:
    hopfocus(384, 0.68)
transform hf53:
    hopfocus(640, 0.68)
transform hf54:
    hopfocus(896, 0.68)
transform hf55:
    hopfocus(1152, 0.68)
transform hf41:
    hopfocus(160, 0.74)
transform hf42:
    hopfocus(480, 0.74)
transform hf43:
    hopfocus(800, 0.74)
transform hf44:
    hopfocus(1120, 0.74)
transform hf31:
    hopfocus(213)
transform hf32:
    hopfocus(640)
transform hf33:
    hopfocus(1067)
transform hf21:
    hopfocus(320)
transform hf22:
    hopfocus(960)
transform hf11:
    hopfocus(640)

transform l61:
    leftin(107, 0.63)
transform l62:
    leftin(320, 0.63)
transform l63:
    leftin(533, 0.63)
transform l64:
    leftin(747, 0.63)
transform l65:
    leftin(960, 0.63)
transform l66:
    leftin(1173, 0.63)
transform l51:
    leftin(128, 0.68)
transform l52:
    leftin(384, 0.68)
transform l53:
    leftin(640, 0.68)
transform l54:
    leftin(896, 0.68)
transform l55:
    leftin(1152, 0.68)
transform l41:
    leftin(160, 0.74)
transform l42:
    leftin(480, 0.74)
transform l43:
    leftin(800, 0.74)
transform l44:
    leftin(1120, 0.74)
transform l31:
    leftin(213)
transform l32:
    leftin(640)
transform l33:
    leftin(1067)
transform l21:
    leftin(320)
transform l22:
    leftin(960)
transform l11:
    leftin(640)

transform lf61:
    leftfocus(107, 0.63)
transform lf62:
    leftfocus(320, 0.63)
transform lf63:
    leftfocus(533, 0.63)
transform lf64:
    leftfocus(747, 0.63)
transform lf65:
    leftfocus(960, 0.63)
transform lf66:
    leftfocus(1173, 0.63)
transform lf51:
    leftfocus(128, 0.68)
transform lf52:
    leftfocus(384, 0.68)
transform lf53:
    leftfocus(640, 0.68)
transform lf54:
    leftfocus(896, 0.68)
transform lf55:
    leftfocus(1152, 0.68)
transform lf41:
    leftfocus(160, 0.74)
transform lf42:
    leftfocus(480, 0.74)
transform lf43:
    leftfocus(800, 0.74)
transform lf44:
    leftfocus(1120, 0.74)
transform lf31:
    leftfocus(213)
transform lf32:
    leftfocus(640)
transform lf33:
    leftfocus(1067)
transform lf21:
    leftfocus(320)
transform lf22:
    leftfocus(960)
transform lf11:
    leftfocus(640)

# Everything that used to follow this line -- the dissolve/wipe scene
# transitions, `image noise` / `noise_alpha`, `image vignette`, and
# `yuripupils_move` -- now lives in fx.rpy. Nothing was dropped or duplicated.
