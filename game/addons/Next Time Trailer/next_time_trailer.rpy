# Chapter 0.5 closing trailer, called from season1/0531.rpy after the month turn.
# enter_m_prologue_trailer plays it; enter_m_prologue_trailer_skip and
# enter_m_tr_cleanup() restore the presentation after playback or skipping.
# Borrowed OP effects stage a decaying broadcast around cryptic story fragments.
# Preserve the cool, hollow palette and withheld explanations.
#
# Timing uses scamall at 75 BPM: 0.8s beats and 3.2s bars. The two SYNC pauses
# place authored hits near 25.5s and 50.75s; changing timing requires listening.
# Deliberate echoes (still / stop / look away / read / remember) build accusation
# and transfer agency across cards. Preserve those recurrences when editing prose.

define enter_m_tr_bpm = 75.0
define enter_m_tr_beat = 60.0 / enter_m_tr_bpm      # 0.80s
define enter_m_tr_bar = enter_m_tr_beat * 4.0       # 3.20s
define enter_m_tr_half = enter_m_tr_bar * 0.5       # 1.60s
define enter_m_tr_quarter = enter_m_tr_bar * 0.25   # 0.80s

# Saved quick_menu flag, restored when the trailer ends/skips.
default enter_m_tr_prev_quick_menu = True

# Off-white-teal "glow" and near-black, so the broadcast never flashes pure white.
image enter_m_tr_glow = Solid("#dfeee9")
image enter_m_tr_dark = Solid("#03070a")
# The shared title art, reused for the closing logo (same PNG the OP uses).
image enter_m_tr_titledrop = "addons/Sick Ass Anime OP/titledropalt.png"

# --- SCREEN REGISTRY + CLEANUP ----------------------------------------------
init python:
    ENTER_M_TR_ACTIVE_SCREENS = (
        "enter_m_tr_broadcast_overlay",
        "enter_m_tr_dropout",
        "enter_m_prologue_trailer_skip",
        "enter_m_tr_static",
        "enter_m_tr_caption",
        "enter_m_tr_announce",
        "enter_m_tr_cryptic",
        "enter_m_tr_stark",
        "enter_m_tr_vn",
        "enter_m_tr_meta_caption",
        "enter_m_tr_title_drop",
        "enter_m_tr_tag",
    )

    def enter_m_tr_cleanup():
        for _screen_name in ENTER_M_TR_ACTIVE_SCREENS:
            try:
                renpy.hide_screen(_screen_name)
            except Exception:
                pass
        # The trailer borrows the OP's generic fx screens; tear those down too.
        try:
            enter_m_op_cleanup_screens()
        except Exception:
            pass

# --- STYLES -----------------------------------------------------------------
# Cool, hollow palette. Matsuda keeps her cyan (#75f7ff); everything else leans
# toward a muted teal-green so nothing reads as warm or "heavenly."
style enter_m_tr_announce_big is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 78
    color "#eef7f4"
    outlines [(3, "#000000", 0, 0), (10, "#03070a99", 0, 0)]
    xalign 0.5
    text_align 0.5

style enter_m_tr_announce_small is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 27
    color "#79e6d2"
    kerning 9.0
    outlines [(2, "#000000", 0, 0)]
    xalign 0.5
    text_align 0.5

style enter_m_tr_caption_text is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 33
    color "#eaffff"
    outlines [(3, "#000000", 0, 0)]
    text_align 0.5

style enter_m_tr_cryptic_text is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 40
    color "#cfe6e0"
    italic True
    outlines [(3, "#000000", 0, 0), (8, "#03070a99", 0, 0)]
    xalign 0.5
    text_align 0.5

style enter_m_tr_stark_text is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 60
    color "#eaf6f2"
    kerning 4.0
    outlines [(3, "#000000", 0, 0), (12, "#03070a99", 0, 0)]
    xalign 0.5
    text_align 0.5

style enter_m_tr_vn_name is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 24
    color "#79e6d2"
    kerning 2.0
    outlines [(1, "#03060b", 0, 0)]

style enter_m_tr_vn_text is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 32
    color "#e9f3f0"
    outlines [(3, "#000000", 0, 0)]

style enter_m_tr_meta_text is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 42
    color "#f0fbf8"
    outlines [(3, "#000000", 0, 0), (10, "#03070a99", 0, 0)]
    xalign 0.5
    text_align 0.5

style enter_m_tr_bug_text is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 18
    color "#dfeee9"
    kerning 3.0
    outlines [(1, "#03060b", 0, 0)]

style enter_m_tr_title is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 108
    color "#eef7f4"
    kerning 6.0
    outlines [(2, "#03060b", 0, 0), (12, "#79e6d255", 0, 0)]
    xalign 0.5
    text_align 0.5

style enter_m_tr_tag_big is enter_m_tr_announce_big:
    size 60

style enter_m_tr_tag_small is enter_m_tr_announce_small:
    color "#9fb4ae"
    kerning 5.0
    size 22

# --- TRANSFORMS -------------------------------------------------------------
# Shared fade-in / hold / fade-out envelope for every timed text element.
# Hold = duration - 0.56; always call with duration >= ~0.9.
transform enter_m_tr_caption_life(duration=2.0):
    alpha 0.0
    yoffset 12
    easeout 0.30 alpha 1.0 yoffset 0
    pause duration - 0.58
    easein 0.28 alpha 0.0 yoffset -8

# CRT power-on: a bright line snaps open to a full frame, then fades.
transform enter_m_tr_crt_on(duration=0.9):
    subpixel True
    xalign 0.5
    yalign 0.5
    yzoom 0.004
    alpha 1.0
    easeout duration * 0.45 yzoom 1.0
    easein duration * 0.30 alpha 0.0

# CRT power-off collapse to a center line, into black.
transform enter_m_tr_crt_off(duration=0.5):
    subpixel True
    xalign 0.5
    yalign 0.5
    yzoom 1.0
    alpha 1.0
    easein duration * 0.7 yzoom 0.004
    easein duration * 0.3 alpha 0.0 xzoom 0.0

# The "live" channel bug pulse, top-left, held for the whole trailer.
transform enter_m_tr_bug_pulse:
    alpha 0.85
    block:
        ease 1.2 alpha 0.40
        ease 1.2 alpha 0.85
        repeat

# A single horizontal "signal dropout" band that slips sideways on a loop.
transform enter_m_tr_tear(y=200, slip=40, period=1.3, delay=0.0):
    ypos y
    xoffset 0
    alpha 0.0
    pause delay
    block:
        linear 0.03 alpha 0.5 xoffset slip
        linear 0.08 xoffset 0
        linear 0.05 alpha 0.0
        pause period
        repeat

# Title-in (plain) + title-in (glitch, shaders only).
transform enter_m_tr_title_plain(duration=3.2):
    subpixel True
    xalign 0.5
    yalign 0.5
    alpha 0.0
    zoom 1.08
    yoffset 16
    easeout 0.6 alpha 1.0 zoom 1.0 yoffset 0
    block:
        ease 1.7 yoffset -4
        ease 1.7 yoffset 0
        repeat

transform enter_m_tr_title_glitch(duration=3.2):
    mesh True
    shader "enter_m.rgbsplit"
    u_amount 26.0
    u_angle 0.0
    subpixel True
    xalign 0.5
    yalign 0.5
    alpha 0.0
    zoom 1.1
    easeout 0.55 alpha 1.0 zoom 1.0 u_amount 6.0
    block:
        easein 0.12 u_amount 16.0
        easeout 0.5 u_amount 4.0
        pause 1.5
        repeat

# Closing-logo reveal: a soft settle + slow drift (chroma added via impact).
transform enter_m_tr_titledrop_in(duration=4.0):
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.06
    alpha 0.0
    easeout 0.5 alpha 1.0 zoom 1.0
    linear duration zoom 1.035

# --- PERSISTENT BROADCAST DRESSING ------------------------------------------
# Channel bug + thin letterbox.
screen enter_m_tr_broadcast_overlay():
    zorder 90
    add Solid("#03060b") xysize (1280, 40) ypos 0
    add Solid("#03060b") xysize (1280, 40) ypos 680
    hbox:
        xpos 30
        ypos 54
        spacing 9
        at enter_m_tr_bug_pulse
        add Solid("#79e6d2") xysize (13, 13) yalign 0.5
        text "ENTER M" style "enter_m_tr_bug_text" yalign 0.5

# Held signal-decay layer over everything: dropout bands, scanline, fine noise.
# intensity scales how aggressive the decay reads.
screen enter_m_tr_dropout(intensity=1.0):
    zorder 84
    add Solid("#05090c66")
    add Solid("#0a1410") xysize (1280, 6) at enter_m_tr_tear(180, 60 * intensity, 1.4, 0.0)
    add Solid("#16241f") xysize (1280, 3) at enter_m_tr_tear(430, -40 * intensity, 1.1, 0.5)
    add Solid("#0d1a16") xysize (1280, 8) at enter_m_tr_tear(560, 34 * intensity, 1.7, 0.9)
    add Solid("#79e6d210") xysize (1280, 2) at enter_m_op_scanline
    add "noise":
        alpha 0.04 * intensity

# --- TEXT / MESSAGE SCREENS -------------------------------------------------
# Full-screen channel static. duration <= 0 holds until manually hidden.
screen enter_m_tr_static(amount=0.5, duration=0.0):
    zorder 97
    add "noise":
        alpha amount
    if duration > 0:
        timer duration action Hide("enter_m_tr_static")

# Matsuda the HOST: a lower-third caption with her cyan chyron bar.
screen enter_m_tr_caption(msg="", duration=2.0):
    zorder 95
    fixed:
        at enter_m_tr_caption_life(duration)
        add Solid("#03070ad9") xysize (1280, 96) ypos 560
        hbox:
            xalign 0.5
            ypos 584
            spacing 16
            add Solid("#75f7ff") xysize (6, 44) yalign 0.5
            text msg style "enter_m_tr_caption_text" yalign 0.5
    timer duration action Hide("enter_m_tr_caption")

# Center broadcast bumper: small kicker over a big line (the NEXT TIME card).
screen enter_m_tr_announce(line1="NEXT TIME", line2="ON ENTER M", duration=2.0):
    zorder 95
    fixed:
        at enter_m_tr_caption_life(duration)
        add Solid("#03070acc") xysize (1280, 240) yalign 0.5
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 10
            text line1 style "enter_m_tr_announce_small"
            text line2 style "enter_m_tr_announce_big"
    timer duration action Hide("enter_m_tr_announce")

# A cryptic line, centered, with a thin rule above it -- quiet, unsettling.
screen enter_m_tr_cryptic(msg="", duration=2.4):
    zorder 95
    fixed:
        at enter_m_tr_caption_life(duration)
        add Solid("#03070acc") xysize (1280, 220) yalign 0.5
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 18
            add Solid("#79e6d255") xysize (200, 2) xalign 0.5
            text msg style "enter_m_tr_cryptic_text"
    timer duration action Hide("enter_m_tr_cryptic")

# A stark statement for the musical hits -- big, caps, lands on the downbeat.
screen enter_m_tr_stark(msg="", duration=2.4):
    zorder 96
    fixed:
        at enter_m_tr_caption_life(duration)
        add Solid("#03070ae0") xysize (1280, 250) yalign 0.5
        text msg style "enter_m_tr_stark_text" xalign 0.5 yalign 0.5
    timer duration action Hide("enter_m_tr_stark")

# Out-of-context VN fragment: a textbox-like bar with an optional speaker name
# and one stray line, ripped from a future scene with no setup.
screen enter_m_tr_vn(who="", msg="", duration=2.6):
    zorder 95
    fixed:
        at enter_m_tr_caption_life(duration)
        add Solid("#03070ae0") xysize (1180, 150) xalign 0.5 ypos 466
        vbox:
            xpos 130
            ypos 488
            spacing 8
            if who:
                text who style "enter_m_tr_vn_name"
            text msg style "enter_m_tr_vn_text"
    timer duration action Hide("enter_m_tr_vn")

# The meta-crack: Matsuda speaking THROUGH the screen. The glitch lives in the
# surrounding visuals; the text stays legible.
screen enter_m_tr_meta_caption(msg="", duration=2.4):
    zorder 96
    fixed:
        at enter_m_tr_caption_life(duration)
        add Solid("#03070ae0") xysize (1280, 220) yalign 0.5
        text msg style "enter_m_tr_meta_text" xalign 0.5 yalign 0.5
    timer duration action Hide("enter_m_tr_meta_caption")

# The actual title drop. The plain layer keeps the logo readable on systems
# without shader support; the second layer supplies the unstable RGB echo.
screen enter_m_tr_title_drop(duration=4.8):
    zorder 96
    text "ENTER M":
        style "enter_m_tr_title"
        at enter_m_tr_title_plain(duration)
    if ENTER_M_OP_SHADERS:
        text "ENTER M":
            style "enter_m_tr_title"
            at enter_m_tr_title_glitch(duration)

# Final tag card (kicker + big line).
screen enter_m_tr_tag(line1="", line2="", duration=2.6):
    zorder 95
    vbox:
        at enter_m_tr_caption_life(duration)
        xalign 0.5
        yalign 0.5
        spacing 10
        text line1 style "enter_m_tr_tag_small"
        text line2 style "enter_m_tr_tag_big"
    timer duration action Hide("enter_m_tr_tag")

# The persistent SKIP affordance.
screen enter_m_prologue_trailer_skip():
    zorder 100
    key "K_ESCAPE" action Jump("enter_m_prologue_trailer_skip")
    key "K_SPACE" action Jump("enter_m_prologue_trailer_skip")
    key "K_RETURN" action Jump("enter_m_prologue_trailer_skip")
    key "K_KP_ENTER" action Jump("enter_m_prologue_trailer_skip")
    textbutton "SKIP":
        style "enter_m_op_skip_button"
        xalign 0.985
        yalign 0.045
        action Jump("enter_m_prologue_trailer_skip")

# =============================================================================
# THE TIMELINE  (cumulative music time noted at each beat, locked to 75 BPM)
# Idiom: scene bg <X> at <pan> -> optional one-shot glitch impact -> a text
# screen (cryptic / vn / caption) -> renpy.pause(<bar-derived>, hard=True). The
# held overlays (broadcast / dropout / post_fx / dust) carry the distortion;
# scene changes cross-dissolve for an ethereal, signal-bleed feel.
# =============================================================================
label enter_m_prologue_trailer:
    $ enter_m_tr_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ renpy.music.stop(fadeout=0.3)
    scene black
    show screen enter_m_tr_broadcast_overlay
    show screen enter_m_tr_dropout(1.0)
    show screen enter_m_prologue_trailer_skip
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_post_fx(0.55, (0.02, 0.06, 0.05))
    show screen enter_m_op_ambient_particles("dust")

    # --- PHASE 0 :: CHANNEL ON  (0.0 -> 6.4s) ----------------------------
    play music scamall noloop
    # The last lamplit frame of Chapter 0.5, already wrong: held, drifting, decayed.
    scene bg bedroom_night at enter_m_op_bg_breathe(enter_m_tr_bar, 0.49, 0.51, 0.52, 0.47)
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_impact("bg bedroom_night", "rgb", enter_m_tr_quarter, amount=14.0, z=1.02)
    show screen enter_m_tr_static(0.10)
    $ renpy.pause(enter_m_tr_quarter, hard=True)

    # Channel change -> CRT snap -> the NEXT TIME bumper.
    scene black
    show screen enter_m_tr_static(0.8, enter_m_tr_quarter)
    $ renpy.pause(enter_m_tr_quarter, hard=True)
    hide screen enter_m_tr_static
    scene enter_m_tr_dark
    show enter_m_tr_glow at enter_m_tr_crt_on(enter_m_tr_half)
    show screen enter_m_tr_announce("NEXT TIME", "ON  ENTER M", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    # The host. Mysterious, unhurried -- not the OP's hype.
    show screen enter_m_tr_caption("Don't mind the dark. It's only a preview.", enter_m_tr_bar - 0.8)
    $ renpy.pause(enter_m_tr_bar - 0.8, hard=True)

    # --- PHASE 1 :: THE BUILD  (6.4 -> 25.5s) ----------------------------
    # Cryptic cards + out-of-context VN fragments, slowly accumulating wrongness.
    scene bg hollow at enter_m_op_bg_breathe(enter_m_tr_bar, 0.47, 0.53, 0.50, 0.46) with Dissolve(0.5)
    # "Still smiling" -> "still here" -> "still happy here" deliberately escalates.
    show screen enter_m_tr_cryptic("Everyone is still smiling.", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    scene bg cafe at enter_m_op_bg_oblique(enter_m_tr_bar, 0.46, 0.54, 0.52, 0.47, -0.18) with Dissolve(0.5)
    # "You can stop" returns as "I couldn't stop it either," transferring agency.
    show screen enter_m_tr_vn("???", "You can stop whenever you want, you know.", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    scene bg classroom_purg at enter_m_op_bg_sweep(enter_m_tr_bar, 0.40, 0.60, 0.50, 0.48) with Dissolve(0.5)
    show screen enter_m_tr_cryptic("Look at all of them, while they're still here.", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    scene bg park_winter at enter_m_op_bg_breathe(enter_m_tr_bar, 0.52, 0.46, 0.50, 0.47) with Dissolve(0.5)
    show screen enter_m_tr_vn("???", "What do you even have to gain from it?!", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    scene bg matsudavr at enter_m_op_bg_push(enter_m_tr_bar, 1.04, 1.13, 0.50, 0.52, 0.50, 0.47) with Dissolve(0.6)
    show screen enter_m_tr_cryptic("None of it had to happen like this.", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    # Bar 8 :: rising tension into the first hit. SYNC: shaved so the HIT below
    # lands at ~25.5s.
    scene bg glitch at enter_m_op_bg_snap_pan(enter_m_tr_bar)
    show screen enter_m_tr_static(0.18, enter_m_tr_bar)
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_impact("bg glitch", "glitch", enter_m_tr_half, z=1.04)
    # Permission to "look away" returns as an accusation.
    show screen enter_m_tr_cryptic("You're allowed to look away here.", enter_m_tr_bar - 0.5)
    $ renpy.pause(enter_m_tr_bar - 0.1, hard=True)

    # --- PHASE 2 :: FIRST HIT  (~25.5s, the buildup peak) ----------------
    scene bg glitch at enter_m_op_bg_push(enter_m_tr_bar, 1.10, 1.02, 0.50, 0.50, 0.48, 0.50)
    show screen enter_m_op_cut_fx("white", 0.42)
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_psyche_break("bg glitch", enter_m_tr_bar)
    show screen enter_m_tr_static(0.22, enter_m_tr_half)
    show screen enter_m_tr_stark("WE WERE STILL HAPPY HERE.", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    # --- PHASE 3 :: THE SECOND SECTION  (28.7 -> 50.75s) -----------------
    # Darker fragments. Each thread teased once, cryptically, never explained.
    scene bg club_day at enter_m_op_bg_breathe(enter_m_tr_bar, 0.50, 0.46, 0.51, 0.47) with Dissolve(0.5)
    show screen enter_m_tr_cryptic("Some of this is already behind us.", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    scene bg kitchen_evening at enter_m_op_bg_oblique(enter_m_tr_bar, 0.54, 0.46, 0.51, 0.47, 0.16) with Dissolve(0.5)
    show screen enter_m_tr_vn("???", "I-It doesn't hurt yet...", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    scene bg track_day at enter_m_op_bg_sweep(enter_m_tr_bar, 0.58, 0.42, 0.50, 0.48) with Dissolve(0.5)
    show screen enter_m_tr_vn("???", "You...you promised you'd remember this!!!", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    scene bg park_washed at enter_m_op_bg_breathe(enter_m_tr_bar, 0.46, 0.54, 0.50, 0.46) with Dissolve(0.6)
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_impact("bg park_washed", "rgb", enter_m_tr_half, amount=10.0, z=1.03)
    show screen enter_m_tr_cryptic("Spring looks different from here.", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    scene bg sam_room_night at enter_m_op_bg_oblique(enter_m_tr_bar, 0.44, 0.56, 0.52, 0.47, -0.20) with Dissolve(0.5)
    show screen enter_m_tr_vn("???", "Hey, nobody has to know about this, you're fine.", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    scene bg courtyard_purg at enter_m_op_bg_push(enter_m_tr_bar, 1.05, 1.15, 0.50, 0.48, 0.50, 0.45) with Dissolve(0.6)
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_impact("bg courtyard_purg", "rgb", enter_m_tr_half, amount=12.0, z=1.03)
    show screen enter_m_tr_cryptic("Everyone knew. Everyone looked away.", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    # Bar 16 :: rising distortion into the drop. SYNC: shaved so the DROP below
    # lands at ~50.75s.
    scene bg matsudavr at enter_m_op_bg_push(enter_m_tr_bar, 1.06, 1.18, 0.50, 0.50, 0.50, 0.46)
    show screen enter_m_tr_static(0.25, enter_m_tr_bar)
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_impact("bg ether", "glitch", enter_m_tr_half, z=1.05)
    show screen enter_m_tr_cryptic("I couldn't stop it either.", enter_m_tr_bar - 0.6)
    $ renpy.pause(enter_m_tr_bar - 0.35, hard=True)

    # --- PHASE 4 :: THE DROP / META-CRACK  (~50.75s) ---------------------
    # The signal can't hold her. She steps through.
    scene black
    show screen enter_m_op_cut_fx("blue", 0.5)
    show screen enter_m_tr_static(0.5, enter_m_tr_quarter)
    show screen enter_m_op_signal_burst
    $ renpy.pause(enter_m_tr_quarter, hard=True)
    hide screen enter_m_op_signal_burst
    hide screen enter_m_tr_static

    scene bg hollow at enter_m_op_bg_push(enter_m_tr_bar * 1.5, 1.14, 1.04, 0.50, 0.50, 0.46, 0.50)
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_psyche_break("bg hollow", enter_m_tr_bar)
    # "Can read" -> "always could" -> "remember" deliberately develops the same claim.
    show screen enter_m_tr_meta_caption("You can read every one of these, can't you?", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    show screen enter_m_op_cut_fx("dark", 0.3)
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_impact("bg hollow", "rgb", 0.5, amount=20.0, z=1.03)
    $ _tr_meta_line = "You always could, " + player + "."
    show screen enter_m_tr_meta_caption(_tr_meta_line, enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)

    scene black
    show screen enter_m_tr_static(0.4, enter_m_tr_bar)
    show screen enter_m_tr_meta_caption("Then do you remember how it ends?", enter_m_tr_bar)
    $ renpy.pause(enter_m_tr_bar, hard=True)
    hide screen enter_m_tr_static

    # --- PHASE 5 :: TITLE LOGO / SIGN-OFF --------------------------------
    # The titledropalt logo is both the ENTER M reveal and the sign-off; it clears
    # to clean black before the broadcast powers down.
    scene black
    show screen enter_m_op_cut_fx("white", 0.4)
    scene enter_m_tr_titledrop at enter_m_tr_titledrop_in(enter_m_tr_bar * 1.5)
    show screen enter_m_op_signal_burst
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_impact("enter_m_tr_titledrop", "shock", 0.7, z=1.04)
    show screen enter_m_tr_title_drop(enter_m_tr_bar * 1.5)
    $ renpy.pause(enter_m_tr_bar * 1.5, hard=True)
    hide screen enter_m_op_signal_burst

    # The NEXT TIME bumper already promised continuation. Let the logo sign off
    # without explaining the chapter boundary a second time.
    hide screen enter_m_tr_title_drop
    scene black
    with Dissolve(0.6)

    # Power off.
    show enter_m_tr_dark at enter_m_tr_crt_off(0.5)
    $ renpy.pause(0.5, hard=True)
    $ enter_m_tr_cleanup()
    scene black with Dissolve(0.6)
    stop music fadeout 2.0
    pause 2.0
    $ renpy.pause(2.0, hard=True)
    $ quick_menu = enter_m_tr_prev_quick_menu
    return

# SKIP target: stop music, tear down everything, fade to black, restore state.
label enter_m_prologue_trailer_skip:
    $ quick_menu = False
    stop music fadeout 0.25
    $ enter_m_tr_cleanup()
    scene black with Dissolve(0.25)
    $ renpy.pause(0.25, hard=True)
    $ quick_menu = enter_m_tr_prev_quick_menu
    return
