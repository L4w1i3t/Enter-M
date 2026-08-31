# =============================================================================
# op.rpy  --  "SICK ASS ANIME OP" (the opening movie)
# =============================================================================
#
# WHAT THIS FILE IS
#   A fully hand-choreographed, beat-locked opening sequence set to opsong.ogg.
#   It's essentially a music video assembled from scene/show/pause statements,
#   with a large supporting library of timing constants, transforms, and FX
#   screens. The "real" GPU effects (shaders + particles) live in op_fx.rpy and
#   are layered on top via a few `show screen` hooks here.
#
# ENTRY POINTS
#   label enter_m_sick_ass_anime_op       -> plays the whole OP (line ~1242).
#   label enter_m_sick_ass_anime_op_skip  -> the SKIP target: stop music, run
#                                            cleanup, fade out, restore quick_menu.
#   enter_m_op_cleanup_screens()          -> hides every OP screen (call this
#                                            AFTER the label returns; archive.rpy
#                                            and the skip label both use it).
#
# WHO PLAYS IT (callers)
#   - game/splash.rpy : the OP on first boot / intro.
#   - game/archive.rpy: the "Replay OP" button (label enter_m_archive_replay_op).
#
# HOW THE TIMING WORKS
#   The song is 130 BPM. enter_m_op_beat/bar/etc. (below) convert beats->seconds
#   so every `renpy.pause(...)` and transform duration lands on the music. The
#   label's inline "0.00s - 14.50s" style comments mark where each section sits.
#
# FILE LAYOUT (top to bottom)
#   1. image aliases (enter_m_op_*)            -> all art/Solids used by the OP.
#   2. timing constants (beat/bar math) + tunables.
#   3. ENTER_M_OP_ACTIVE_SCREENS + cleanup     -> the screen registry teardown.
#   4. styles (title/credit/skip button).
#   5. the TRANSFORM LIBRARY (Ken-Burns BG moves, per-CG "stage" treatments,
#      cut/flash transitions, sweep/spark/line accents). This is most of the file.
#   6. FX SCREENS (overlay, signal bursts, stage flair, per-CG polish, BG cards,
#      cut FX, skip) -- the reusable visual building blocks the label `show`s.
#   7. the main label (the actual timeline) + the skip label.
#
# RELATED: op_fx.rpy registers enter_m_op_post_fx / _ambient_particles /
#   _spark_burst / _impact / etc. (also listed in ENTER_M_OP_ACTIVE_SCREENS so
#   cleanup catches them). ENTER_M_OP_SHADERS (set in op_fx.rpy) gates the
#   shader-based post-process.
# =============================================================================

define -50 audio.enter_m_op = "assets/audio/bgm/opsong.ogg"

# --- 1. IMAGE ALIASES -------------------------------------------------------
# Short names for every Solid/CG/background the OP uses, so the timeline below
# reads cleanly (e.g. `scene enter_m_op_mom_work`). enter_m_op_bg_* are the
# "dump"-folder location plates panned behind sprites.
image enter_m_op_blue = Solid("#75f7ff")
image enter_m_op_red = Solid("#d05f77")
image enter_m_op_amber = Solid("#d39a55")
image enter_m_op_dark = Solid("#02040b")
image enter_m_op_white = Solid("#ffffff")
image enter_m_op_warning_gray = "addons/Sick Ass Anime OP/warning.png"
image enter_m_op_warning_color = "addons/Sick Ass Anime OP/warning2.png"
image enter_m_op_console_tsubaki = "addons/Sick Ass Anime OP/consoletsubaki.png"
image enter_m_op_icecream = "addons/Sick Ass Anime OP/tsubakimatsudaicecream.png"
image enter_m_op_arguing = "addons/Sick Ass Anime OP/arguing.png"
image enter_m_op_asahina_poster = "addons/Sick Ass Anime OP/asahinaposter.png"
image enter_m_op_asahina_world_broken = "addons/Sick Ass Anime OP/asahinaworldbroken.png"
image enter_m_op_puppet = "addons/Sick Ass Anime OP/puppet.png"
image enter_m_op_storekoto = "addons/Sick Ass Anime OP/storekoto.png"
image enter_m_op_monika_club = "addons/Sick Ass Anime OP/monikaclub.png"
image enter_m_op_redshift = "addons/Sick Ass Anime OP/redshift.png"
image enter_m_op_blueshift = "addons/Sick Ass Anime OP/blueshift.png"
image enter_m_op_no_marks = "addons/Sick Ass Anime OP/nomarks.png"
image enter_m_op_missing = "addons/Sick Ass Anime OP/missing.png"
image enter_m_op_matsuda_wistful = "addons/Sick Ass Anime OP/matsuwistful.png"
image enter_m_op_mom_work = "addons/Sick Ass Anime OP/momwork.png"
image enter_m_op_sam_bus = "addons/Sick Ass Anime OP/sambus.png"
image enter_m_op_sam_villain = "addons/Sick Ass Anime OP/samvillain.png"
image enter_m_op_turmoil = "addons/Sick Ass Anime OP/turmoil.png"
image enter_m_op_title_drop = "addons/Sick Ass Anime OP/titledropalt.png"
image enter_m_op_bg_arcade = "assets/dump/arcade.png"
image enter_m_op_bg_cafe = "assets/dump/cafe.png"
image enter_m_op_bg_bookstore = "assets/dump/bookstore.png"
image enter_m_op_bg_courtyard = "assets/dump/courtyard.png"
image enter_m_op_bg_house_evening = "assets/backgrounds/house_evening.png"
image enter_m_op_bg_library = "assets/backgrounds/library.png"
image enter_m_op_bg_lightcorridor = "assets/dump/lightcorridor.png"
image enter_m_op_bg_lightresidential = "assets/backgrounds/residential.png"
image enter_m_op_bg_kitchen = "assets/backgrounds/kitchen.png"
image enter_m_op_bg_musicroom = "assets/dump/musicroom.png"
image enter_m_op_bg_stairs = "assets/dump/stairs.png"
image enter_m_op_bg_street = "assets/backgrounds/city_day.png"
image enter_m_op_bg_vending = "assets/dump/vendingmachine.png"

# --- 2. TIMING CONSTANTS ----------------------------------------------------
# Song = 130 BPM. beat = seconds per beat; bar = 4 beats; the fractions are
# common subdivisions used as pause/transform durations so visuals hit on-beat.
# audio_delay compensates for the gap before the track audibly starts; the
# monika_* constants are one-off framing tunables for her shot.
define enter_m_op_beat = 60.0 / 130.0
define enter_m_op_bar = enter_m_op_beat * 4.0
define enter_m_op_half_bar = enter_m_op_bar * 0.5
define enter_m_op_quarter_bar = enter_m_op_bar * 0.25
define enter_m_op_eighth_bar = enter_m_op_bar * 0.125
define enter_m_op_audio_delay = enter_m_op_beat * 0.2
define enter_m_op_monika_zoom = 0.62
define enter_m_op_monika_y = 852

# Saved quick_menu flag, restored when the OP ends/skips (the OP hides the quick menu).
default enter_m_op_prev_quick_menu = True

# --- 3. SCREEN REGISTRY + CLEANUP -------------------------------------------
# Every screen the OP can leave on-screen, in one tuple, so enter_m_op_cleanup_screens()
# can tear them ALL down in one call regardless of which shot was active. The
# second group (post_fx, particles, etc.) is registered in op_fx.rpy.
init python:
    ENTER_M_OP_ACTIVE_SCREENS = (
        "enter_m_op_overlay",
        "enter_m_op_skip",
        "enter_m_op_signal_burst",
        "enter_m_op_pressure_marks",
        "enter_m_op_stage_fx",
        "enter_m_op_matsuda_stage_flair",
        "enter_m_op_cg_polish",
        "enter_m_op_turmoil_fx",
        "enter_m_op_memory_glow",
        "enter_m_op_memory_loss",
        "enter_m_op_bg_plate",
        "enter_m_op_bg_motion_card",
        "enter_m_op_bg_pair_card",
        "enter_m_op_bg_hold_card",
        "enter_m_op_bg_step_card",
        "enter_m_op_bg_shadow_card",
        "enter_m_op_cut_fx",
        # FX upgrade layer (see op_fx.rpy)
        "enter_m_op_post_fx",
        "enter_m_op_ambient_particles",
        "enter_m_op_spark_burst",
        "enter_m_op_impact",
        "enter_m_op_meta_lineup",
        "enter_m_op_meta_monika",
        "enter_m_op_psyche_break",
        "enter_m_op_sludge_card",
        "enter_m_op_bg_impact_card",
        "enter_m_op_rays",
        "enter_m_op_freeze_frame",
        "enter_m_op_split_card",
        "enter_m_op_kinetic_credit",
        "enter_m_op_name_card",
    )

    def enter_m_op_cleanup_screens():
        for screen_name in ENTER_M_OP_ACTIVE_SCREENS:
            try:
                renpy.hide_screen(screen_name)
            except Exception:
                pass

    def enter_m_op_cg_unlock(*names):
        """Unlock a CG Gallery entry, but NEVER let the gallery break the OP.

        The OP owns its own art -- the PNGs beside this file, defined as
        enter_m_op_* images in section 1. The gallery is bookkeeping laid on
        top of that, not a dependency. cg_unlock raises under
        config.developer on a title that is not in cg_gallery_catalog, so
        pulling one CG out of the gallery used to take the whole OP down with
        it. Here a title that no longer exists -- or a gallery module that is
        not installed at all -- is simply a no-op.
        """
        for name in names:
            try:
                if cg_find(name) is not None:
                    cg_unlock(name)
            except Exception:
                pass

# --- 4. STYLES (title card, credit lines, skip button) ----------------------
style enter_m_op_title is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 88
    color "#f8fbff"
    outlines [(2, "#03060b", 0, 0), (10, "#75f7ff66", 0, 0)]
    xalign 0.5
    text_align 0.5

style enter_m_op_credit is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 26
    color "#f4fbff"
    outlines [(2, "#03060b", 0, 0), (6, "#75f7ff44", 0, 0)]

style enter_m_op_skip_button is button:
    background "#03060bcc"
    hover_background "#75f7ff66"
    xpadding 14
    ypadding 6

style enter_m_op_skip_button_text is gui_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 16
    color "#d6f8ff"
    hover_color "#ffffff"
    outlines [(1, "#03060b", 0, 0)]

# --- 5. TRANSFORM LIBRARY ---------------------------------------------------
# The bulk of the file. Reusable, parameterised motion presets the timeline
# applies with `at`. Rough families:
#   * enter_m_op_bg_*        : Ken-Burns-style background pans/zooms (push, sweep,
#                              snap_pan, breathe, oblique) for the location plates.
#   * *_stage / *_backplate  : per-CG "treatments" (color grade + handheld shake +
#                              zoom path) named after the shot they dress (e.g.
#                              sam_villain, monika_club, turmoil, redshift...).
#   * enter_m_op_cut_*       : quick transition flashes/fades/wipes between shots.
#   * sweep / spark / line / band / beam / glint: thin animated accent shapes
#                              (drawn as Solids) for idol-flair, speed lines, etc.
# Durations frequently reference the beat/bar constants above to stay on-tempo.
transform enter_m_op_bg_push(duration=4.0, start_zoom=1.04, end_zoom=1.12, xstart=0.5, xend=0.5, ystart=0.5, yend=0.5):
    subpixel True
    zoom start_zoom
    xalign xstart
    yalign ystart
    linear duration zoom end_zoom xalign xend yalign yend

transform enter_m_op_bg_sweep(duration=4.0, xstart=0.0, xend=1.0, ystart=0.5, yend=0.5):
    subpixel True
    zoom 1.12
    xalign xstart
    yalign ystart
    linear duration xalign xend yalign yend

transform enter_m_op_bg_snap_pan(duration=1.0, x1=0.46, x2=0.56, x3=0.50, y1=0.52, y2=0.46, y3=0.50):
    subpixel True
    zoom 1.075
    xalign x1
    yalign y1
    easeout duration * 0.28 zoom 1.145 xalign x2 yalign y2
    ease duration * 0.22 zoom 1.105 xalign x3 yalign y3
    linear duration * 0.36 zoom 1.165 xalign x3 + 0.025 yalign y3 - 0.020

transform enter_m_op_bg_breathe(duration=1.0, xstart=0.49, xend=0.51, ystart=0.51, yend=0.47):
    subpixel True
    zoom 1.045
    xalign xstart
    yalign ystart
    easeout duration * 0.24 zoom 1.085 xalign (xstart + xend) * 0.5 yalign yend
    linear duration * 0.54 zoom 1.125 xalign xend yalign yend
    easein duration * 0.16 zoom 1.145 xalign xend yalign yend

transform enter_m_op_bg_oblique(duration=1.0, xstart=0.45, xend=0.55, ystart=0.52, yend=0.46, rot=-0.25):
    subpixel True
    zoom 1.13
    xalign xstart
    yalign ystart
    rotate rot
    easeout duration * 0.18 zoom 1.18 xalign xstart + (xend - xstart) * 0.35 yalign yend rotate rot * 0.45
    linear duration * 0.58 zoom 1.22 xalign xend yalign yend rotate 0
    easein duration * 0.18 zoom 1.25 xalign xend yalign yend

transform enter_m_op_stage_tease:
    subpixel True
    zoom 1.10
    xalign 0.48
    yalign 0.48
    alpha 1.0
    easeout 0.12 alpha 1.0
    linear 1.28 zoom 1.16 xalign 0.52 yalign 0.50

transform enter_m_op_stage_hit:
    subpixel True
    zoom 1.22
    xalign 0.50
    yalign 0.50
    alpha 1.0
    matrixcolor BrightnessMatrix(0.04) * SaturationMatrix(1.12)
    easeout 0.08 alpha 1.0 zoom 1.06 xalign 0.50 yalign 0.50
    parallel:
        easeout 0.34 zoom 1.13 xalign 0.58 yalign 0.54
        ease 0.26 zoom 1.08 xalign 0.54 yalign 0.50
        linear 2.82 zoom 1.15 xalign 0.45 yalign 0.46
    parallel:
        block:
            linear 0.035 xoffset -8 yoffset 2
            linear 0.035 xoffset 7 yoffset -2
            linear 0.050 xoffset 0 yoffset 0
            pause 0.36
            repeat
    parallel:
        block:
            matrixcolor BrightnessMatrix(0.08) * SaturationMatrix(1.28)
            pause 0.12
            matrixcolor BrightnessMatrix(0.01) * SaturationMatrix(1.04)
            pause 0.34
            matrixcolor BrightnessMatrix(0.10) * SaturationMatrix(1.34)
            pause 0.07
            matrixcolor BrightnessMatrix(0.03) * SaturationMatrix(1.10)
            pause 0.70
            repeat

transform enter_m_op_idol_sweep(x=640, y=360, w=760, h=34, rot=-12, delay=0.0, direction=1, color_alpha=0.28):
    subpixel True
    xcenter x
    ycenter y
    xysize (w, h)
    rotate rot
    alpha 0.0
    xoffset -980 * direction
    pause delay
    linear 0.035 alpha color_alpha
    easeout 0.24 xoffset -80 * direction
    linear 0.40 xoffset 860 * direction
    linear 0.08 alpha 0.0

transform enter_m_op_hand_spark(x=640, y=360, w=220, h=7, rot=0, delay=0.0, color_alpha=0.42):
    subpixel True
    xcenter x
    ycenter y
    xysize (w, h)
    rotate rot
    zoom 0.45
    alpha 0.0
    pause delay
    easeout 0.055 alpha color_alpha zoom 1.0
    easein 0.20 alpha 0.0 zoom 1.42

transform enter_m_op_confetti_fall(x=640, y=360, delay=0.0, direction=1, rot=0, color_alpha=0.72):
    subpixel True
    xpos x
    ypos y
    xysize (18, 8)
    rotate rot
    alpha 0.0
    xoffset -180 * direction
    yoffset -80
    pause delay
    linear 0.035 alpha color_alpha
    linear 1.10 xoffset 260 * direction yoffset 210 rotate rot + 190 * direction
    linear 0.08 alpha 0.0

transform enter_m_op_title_plate:
    subpixel True
    zoom 1.02
    xalign 0.50
    yalign 0.50
    alpha 1.0
    easeout 0.20 alpha 1.0 zoom 1.00
    parallel:
        linear 6.80 zoom 1.06 xalign 0.52 yalign 0.48
    parallel:
        block:
            linear 0.05 xoffset -4
            linear 0.05 xoffset 3
            linear 0.05 xoffset 0
            pause 1.25
            repeat

transform enter_m_op_cg_drift(duration=2.0, start_zoom=1.04, end_zoom=1.10, xstart=0.5, xend=0.5, ystart=0.5, yend=0.5):
    subpixel True
    zoom start_zoom
    xalign xstart
    yalign ystart
    alpha 1.0
    rotate -0.18
    easeout 0.10 alpha 1.0 zoom start_zoom + 0.025
    ease 0.16 zoom start_zoom + 0.005
    parallel:
        linear duration zoom end_zoom xalign xend yalign yend
    parallel:
        block:
            ease 0.46 xoffset -4 yoffset 2 rotate -0.18
            ease 0.23 xoffset 3 yoffset -1 rotate 0.10
            pause 0.23
            repeat

transform enter_m_op_cg_impact(duration=1.4, start_zoom=1.12, end_zoom=1.04, xstart=0.5, xend=0.5, ystart=0.5, yend=0.5):
    subpixel True
    zoom start_zoom
    xalign xstart
    yalign ystart
    alpha 1.0
    linear 0.04 alpha 1.0
    parallel:
        easeout 0.16 zoom start_zoom + 0.035 xalign xstart yalign ystart
        ease 0.18 zoom start_zoom - 0.015
        linear duration zoom end_zoom xalign xend yalign yend
    parallel:
        block:
            linear 0.04 xoffset -12 yoffset 3
            linear 0.04 xoffset 10 yoffset -3
            linear 0.04 xoffset 0 yoffset 0
            pause 0.34
            repeat
    parallel:
        block:
            ease 0.16 rotate -0.30
            ease 0.16 rotate 0.26
            ease 0.16 rotate 0.0
            pause 0.48
            repeat

transform enter_m_op_puppet_stage(duration=3.23):
    subpixel True
    zoom 1.08
    xalign 0.50
    yalign 0.50
    rotate -0.35
    alpha 1.0
    linear 0.04 alpha 1.0 zoom 1.03 rotate 0.0
    parallel:
        easeout 0.23 zoom 1.10 xalign 0.51 yalign 0.49
        ease 0.23 zoom 1.05 xalign 0.50 yalign 0.50
        easeout 0.23 zoom 1.12 xalign 0.52 yalign 0.48
        linear duration zoom 1.16 xalign 0.54 yalign 0.46
    parallel:
        block:
            linear 0.05 xoffset -10 yoffset 3 rotate -0.20
            linear 0.05 xoffset 9 yoffset -3 rotate 0.16
            linear 0.08 xoffset 0 yoffset 0 rotate 0.0
            pause 0.28
            repeat

transform enter_m_op_turmoil_backplate(duration=3.7):
    subpixel True
    zoom 1.24
    xalign 0.50
    yalign 0.50
    alpha 0.58
    matrixcolor BrightnessMatrix(-0.30) * SaturationMatrix(0.04)
    linear 0.16 alpha 0.58
    linear duration zoom 1.32 xalign 0.49 yalign 0.50

transform enter_m_op_sam_villain_stage(duration=2.4):
    subpixel True
    zoom 1.04
    xalign 0.48
    yalign 0.50
    alpha 1.0
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.70) * TintMatrix("#e3b174")
    easeout 0.12 alpha 1.0 zoom 1.06
    parallel:
        easeout 0.24 zoom 1.11 xalign 0.54 yalign 0.50
        ease 0.22 zoom 1.08
        linear 1.386 zoom 1.15 xalign 0.59 yalign 0.50
        easeout 0.08 zoom 1.72 xalign 0.82 yalign 0.61
        ease 0.3815 zoom 1.78 xalign 0.86 yalign 0.63
        easeout 0.08 zoom 1.66 xalign 0.47 yalign 0.28
        ease 0.3815 zoom 1.72 xalign 0.44 yalign 0.27
        easeout 0.08 zoom 1.60 xalign 0.11 yalign 0.70
        ease 0.3815 zoom 1.66 xalign 0.09 yalign 0.72
        easeout 0.08 zoom 1.24 xalign 0.55 yalign 0.50
        ease 0.3815 zoom 1.28 xalign 0.58 yalign 0.49
    parallel:
        block:
            ease 0.46 xoffset -2 yoffset 1
            ease 0.46 xoffset 3 yoffset -1
            ease 0.24 xoffset 0 yoffset 0
            repeat
    parallel:
        block:
            matrixcolor BrightnessMatrix(-0.09) * SaturationMatrix(0.60) * TintMatrix("#c9965a")
            pause enter_m_op_bar
            matrixcolor BrightnessMatrix(0.04) * SaturationMatrix(1.06) * TintMatrix("#ffd4a1")
            pause 0.08
            matrixcolor BrightnessMatrix(-0.13) * SaturationMatrix(0.52) * TintMatrix("#b46a46")
            pause 0.3815
            matrixcolor BrightnessMatrix(0.00) * SaturationMatrix(0.92) * TintMatrix("#e4b071")
            pause 0.08
            matrixcolor BrightnessMatrix(-0.15) * SaturationMatrix(0.46) * TintMatrix("#a56343")
            pause 0.3815
            matrixcolor BrightnessMatrix(0.02) * SaturationMatrix(0.86) * TintMatrix("#d09758")
            pause 0.08
            matrixcolor BrightnessMatrix(-0.18) * SaturationMatrix(0.42) * TintMatrix("#7f5f46")
            pause 0.3815
            matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.60) * TintMatrix("#c9965a")
            pause 0.08
            matrixcolor BrightnessMatrix(-0.16) * SaturationMatrix(0.38) * TintMatrix("#5a4539")
            pause 0.3815

transform enter_m_op_sam_villain_backplate(duration=3.7):
    subpixel True
    zoom 1.23
    xalign 0.50
    yalign 0.50
    alpha 1.0
    matrixcolor BrightnessMatrix(-0.26) * SaturationMatrix(0.32) * TintMatrix("#8a6748")
    linear 0.04 alpha 1.0
    linear duration zoom 1.30 xalign 0.55 yalign 0.50

transform enter_m_op_monika_club_stage(duration=2.4):
    subpixel True
    zoom 1.04
    xalign 0.50
    yalign 0.50
    alpha 1.0
    matrixcolor BrightnessMatrix(-0.04) * SaturationMatrix(0.82)
    easeout 0.12 alpha 1.0 zoom 1.06
    parallel:
        easeout 0.28 zoom 1.10 xalign 0.51 yalign 0.49
        ease 0.18 zoom 1.06
        easeout 0.34 zoom 1.11 xalign 0.50 yalign 0.47
        linear duration zoom 1.13 xalign 0.52 yalign 0.46
    parallel:
        block:
            ease 0.52 xoffset -3 yoffset 2
            ease 0.52 xoffset 3 yoffset -2
            ease 0.22 xoffset 0 yoffset 0
            repeat
    parallel:
        block:
            matrixcolor BrightnessMatrix(-0.05) * SaturationMatrix(0.76)
            pause 1.12
            matrixcolor BrightnessMatrix(0.02) * SaturationMatrix(0.92)
            pause 0.16
            repeat

transform enter_m_op_asahina_poster_stage(duration=2.0):
    subpixel True
    zoom 1.06
    xalign 0.38
    yalign 0.56
    alpha 1.0
    matrixcolor BrightnessMatrix(0.00) * SaturationMatrix(0.88)
    easeout 0.12 alpha 1.0 zoom 1.08
    parallel:
        easeout 0.22 zoom 1.13 xalign 0.48 yalign 0.48
        ease 0.14 zoom 1.09
        linear duration zoom 1.17 xalign 0.60 yalign 0.40
    parallel:
        block:
            linear 0.04 xoffset -5 yoffset 2
            linear 0.04 xoffset 4 yoffset -2
            linear 0.08 xoffset 0 yoffset 0
            pause 0.38
            repeat
    parallel:
        block:
            matrixcolor BrightnessMatrix(-0.02) * SaturationMatrix(0.82)
            pause 0.74
            matrixcolor BrightnessMatrix(0.04) * SaturationMatrix(1.00)
            pause 0.12
            repeat

transform enter_m_op_redshift_stage(duration=2.0):
    subpixel True
    zoom 1.18
    xalign 0.43
    yalign 0.52
    alpha 1.0
    matrixcolor BrightnessMatrix(-0.06) * SaturationMatrix(1.08)
    linear 0.08 alpha 1.0
    parallel:
        linear duration zoom 1.06 xalign 0.57 yalign 0.47
    parallel:
        block:
            ease 0.50 xoffset -3 yoffset 2
            ease 0.50 xoffset 3 yoffset -1
            ease 0.25 xoffset 0 yoffset 0
            repeat
    parallel:
        block:
            matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(1.02)
            pause 0.52
            matrixcolor BrightnessMatrix(0.06) * SaturationMatrix(1.28)
            pause 0.10
            repeat

transform enter_m_op_blueshift_stage(duration=1.2):
    subpixel True
    zoom 1.08
    xalign 0.50
    yalign 0.49
    alpha 1.0
    matrixcolor BrightnessMatrix(-0.04) * SaturationMatrix(1.04)
    linear 0.04 alpha 1.0 zoom 1.10
    parallel:
        easeout 0.23 zoom 1.18 xalign 0.50 yalign 0.46
        ease 0.23 zoom 1.13
        linear duration zoom 1.20 xalign 0.50 yalign 0.44
    parallel:
        block:
            linear 0.035 xoffset -4 yoffset 1
            linear 0.035 xoffset 4 yoffset -1
            linear 0.050 xoffset 0 yoffset 0
            pause 0.18
            repeat
    parallel:
        block:
            matrixcolor BrightnessMatrix(-0.06) * SaturationMatrix(0.98)
            pause 0.22
            matrixcolor BrightnessMatrix(0.10) * SaturationMatrix(1.26)
            pause 0.05
            repeat

transform enter_m_op_no_marks_stage(duration=2.6):
    subpixel True
    zoom 1.04
    xalign 0.50
    yalign 0.50
    alpha 1.0
    matrixcolor BrightnessMatrix(-0.04) * SaturationMatrix(0.72)
    easeout 0.18 alpha 1.0 zoom 1.05
    parallel:
        ease 0.46 zoom 1.07 xalign 0.505 yalign 0.48
        ease 0.23 zoom 1.055
        linear duration zoom 1.10 xalign 0.515 yalign 0.45
    parallel:
        block:
            ease 0.82 xoffset -2 yoffset 1
            ease 0.82 xoffset 2 yoffset -1
            ease 0.36 xoffset 0 yoffset 0
            repeat
    parallel:
        block:
            matrixcolor BrightnessMatrix(-0.06) * SaturationMatrix(0.64)
            pause 1.05
            matrixcolor BrightnessMatrix(0.02) * SaturationMatrix(0.86)
            pause 0.12
            repeat

transform enter_m_op_missing_stage(duration=2.3):
    subpixel True
    zoom 1.05
    xalign 0.50
    yalign 0.50
    alpha 1.0
    matrixcolor BrightnessMatrix(-0.06) * SaturationMatrix(0.62)
    linear 0.04 alpha 1.0
    parallel:
        easeout 0.23 zoom 1.11 xalign 0.49 yalign 0.50
        ease 0.23 zoom 1.07 xalign 0.50
        linear duration zoom 1.14 xalign 0.52 yalign 0.47
    parallel:
        block:
            linear 0.035 xoffset -7 yoffset 2
            linear 0.035 xoffset 6 yoffset -2
            linear 0.045 xoffset 0 yoffset 0
            pause 0.115
            repeat
    parallel:
        block:
            matrixcolor BrightnessMatrix(-0.10) * SaturationMatrix(0.46)
            pause 0.23
            matrixcolor BrightnessMatrix(0.06) * SaturationMatrix(0.82)
            pause 0.05
            repeat

transform enter_m_op_reminisce_stage(duration=3.0):
    subpixel True
    zoom 1.015
    xalign 0.52
    yalign 0.50
    alpha 1.0
    matrixcolor BrightnessMatrix(0.02) * SaturationMatrix(0.82) * TintMatrix("#f3d2a1")
    linear duration zoom 1.065 xalign 0.47 yalign 0.48

transform enter_m_op_icecream_memory_stage(duration=1.8):
    subpixel True
    zoom 1.015
    xalign 0.53
    yalign 0.50
    alpha 1.0
    matrixcolor BrightnessMatrix(0.09) * SaturationMatrix(1.22) * TintMatrix("#fff0bf")
    easeout 0.20 zoom 1.035 xalign 0.51 yalign 0.49
    linear duration zoom 1.085 xalign 0.47 yalign 0.48

transform enter_m_op_consolation_stage(duration=1.4):
    subpixel True
    zoom 1.08
    xalign 0.62
    yalign 0.51
    alpha 1.0
    matrixcolor BrightnessMatrix(-0.13) * SaturationMatrix(0.48) * TintMatrix("#b8c7df")
    parallel:
        linear duration zoom 1.17 xalign 0.66 yalign 0.50
    parallel:
        block:
            pause 0.20
            linear 0.045 xoffset -4
            linear 0.045 xoffset 3
            linear 0.060 xoffset 0
            pause 0.42
            repeat

transform enter_m_op_scanline:
    subpixel True
    ypos -4
    alpha 0.0
    pause 0.15
    block:
        ypos -4
        alpha 0.0
        linear 0.08 alpha 0.50
        linear 1.15 ypos 724
        linear 0.08 alpha 0.0
        pause 0.35
        repeat

transform enter_m_op_flash(color_alpha=0.78):
    alpha 0.0
    linear 0.05 alpha color_alpha
    linear 0.22 alpha 0.0

transform enter_m_op_cut_fade(strength=0.38, duration=0.22):
    alpha strength
    linear duration alpha 0.0

transform enter_m_op_cut_flash(strength=0.42, duration=0.18):
    alpha 0.0
    linear 0.03 alpha strength
    linear duration alpha 0.0

transform enter_m_op_cut_wipe(strength=0.42, duration=0.22, start=-1280, end=1280):
    xoffset start
    alpha strength
    linear duration xoffset end alpha 0.0

# Diagonal slash wipe (90s-OP scene change): a wide rotated band sweeping
# corner-to-corner.
transform enter_m_op_cut_diag(strength=0.5, duration=0.26, direction=1):
    subpixel True
    xysize (560, 2200)
    anchor (0.5, 0.5)
    ypos 360
    rotate (24 * direction)
    alpha strength
    xpos (-700 if direction > 0 else 1980)
    linear duration xpos (1980 if direction > 0 else -700)
    alpha 0.0

transform enter_m_op_credit_in:
    subpixel True
    truecenter
    alpha 0.0
    yoffset 12
    pause 0.16
    easeout 0.26 alpha 0.92 yoffset 0
    pause 0.72
    easein 0.20 alpha 0.0 yoffset -8

# Letterbox bars slide in, then breathe on the 130 BPM grid -- the frame itself
# pumps with the song. The bars are 68px tall but rest 4px past the screen edge,
# so the pump squeezes INWARD and never exposes a sliver of scene at the edges.
transform enter_m_op_letterbox_top:
    ypos -68
    easeout 0.35 ypos -4
    block:
        easeout (enter_m_op_beat * 0.22) yoffset 4
        easein (enter_m_op_beat * 0.78) yoffset 0
        pause enter_m_op_beat
        repeat

transform enter_m_op_letterbox_bottom:
    ypos 720
    easeout 0.35 ypos 656
    block:
        easeout (enter_m_op_beat * 0.22) yoffset -4
        easein (enter_m_op_beat * 0.78) yoffset 0
        pause enter_m_op_beat
        repeat

transform enter_m_op_chroma_layer(xshift=6, yshift=0, tint="#75f7ff", strength=0.12, duration=1.0):
    subpixel True
    truecenter
    xoffset xshift
    yoffset yshift
    alpha 0.0
    matrixcolor TintMatrix(tint) * SaturationMatrix(0.0)
    parallel:
        linear 0.04 alpha strength
        pause duration * 0.66
        linear duration * 0.10 alpha 0.0
    parallel:
        block:
            linear enter_m_op_eighth_bar xoffset xshift yoffset yshift - 1
            linear enter_m_op_eighth_bar xoffset -xshift yoffset yshift + 1
            linear enter_m_op_eighth_bar xoffset xshift * 0.45 yoffset yshift
            pause enter_m_op_quarter_bar
            repeat

transform enter_m_op_cg_glint(x=640, y=360, w=760, h=18, rot=-10, delay=0.0, color_alpha=0.24, direction=1):
    subpixel True
    xcenter x
    ycenter y
    xysize (w, h)
    rotate rot
    alpha 0.0
    xoffset -1180 * direction
    pause delay
    linear 0.04 alpha color_alpha
    linear enter_m_op_half_bar xoffset 1180 * direction
    linear 0.08 alpha 0.0

transform enter_m_op_turmoil_shadow(delay=0.0, strength=0.28):
    alpha 0.0
    pause delay
    linear 0.08 alpha strength
    linear enter_m_op_beat * 0.64 alpha 0.0

transform enter_m_op_choke_rect(x0=0, y0=0, x1=0, y1=0, w=1280, h=180, duration=3.7, alpha_end=0.64):
    subpixel True
    xpos x0
    ypos y0
    xysize (w, h)
    alpha 0.0
    linear enter_m_op_bar alpha alpha_end * 0.34 xpos x0 + (x1 - x0) * 0.38 ypos y0 + (y1 - y0) * 0.38
    linear enter_m_op_bar alpha alpha_end xpos x1 ypos y1

transform enter_m_op_turmoil_static_rise(duration=3.7):
    alpha 0.045
    linear enter_m_op_bar alpha 0.075
    linear enter_m_op_bar alpha 0.18

transform enter_m_op_turmoil_suffocate_line(x=0, y=0, w=1280, delay=0.0, color_alpha=0.32):
    subpixel True
    xpos x
    ypos y
    xsize w
    ysize 5
    alpha 0.0
    xoffset -160
    pause delay
    linear 0.035 alpha color_alpha xoffset 0
    linear 0.11 xoffset 90
    linear 0.05 alpha 0.0 xoffset 220

transform enter_m_op_memory_haze_line(x=0, y=0, w=1280, delay=0.0, color_alpha=0.16):
    subpixel True
    xpos x
    ypos y
    xsize w
    ysize 14
    alpha 0.0
    xoffset -320
    pause delay
    easeout 0.18 alpha color_alpha xoffset 0
    linear 0.62 xoffset 380
    easein 0.16 alpha 0.0 xoffset 620

transform enter_m_op_loss_bar(x=0, y=0, w=1280, h=16, delay=0.0, direction=1, color_alpha=0.24):
    subpixel True
    xpos x
    ypos y
    xsize w
    ysize h
    alpha 0.0
    xoffset -900 * direction
    pause delay
    linear 0.04 alpha color_alpha
    linear 0.32 xoffset 920 * direction
    linear 0.06 alpha 0.0

transform enter_m_op_motion_band(x=640, y=360, w=760, h=34, rot=-8, delay=0.0, direction=1, alpha_value=0.22):
    subpixel True
    xcenter x
    ycenter y
    xysize (w, h)
    rotate rot
    alpha 0.0
    xoffset -900 * direction
    pause delay
    linear 0.06 alpha alpha_value
    easeout 0.30 xoffset 0
    linear 0.46 xoffset 980 * direction
    linear 0.08 alpha 0.0

transform enter_m_op_panel_sweep(x=640, color_delay=0.0, direction=1, rot=-12, alpha_value=0.34):
    subpixel True
    xpos x
    ypos -160
    xsize 360
    ysize 1040
    rotate rot
    alpha 0.0
    xoffset -760 * direction
    pause color_delay
    easeout 0.18 alpha alpha_value xoffset -80 * direction
    linear 0.70 xoffset 140 * direction
    easein 0.18 alpha 0.0 xoffset 620 * direction

transform enter_m_op_world_crumble_stage(duration=1.85):
    subpixel True
    zoom 1.04
    xalign 0.49
    yalign 0.50
    alpha 1.0
    matrixcolor BrightnessMatrix(-0.08) * SaturationMatrix(0.46)
    linear 0.04 alpha 1.0
    parallel:
        easeout 0.20 zoom 1.10 xalign 0.48 yalign 0.49
        ease 0.18 zoom 1.06
        linear duration zoom 1.16 xalign 0.55 yalign 0.43
    parallel:
        block:
            linear 0.04 xoffset -8 yoffset 2 rotate -0.18
            linear 0.04 xoffset 8 yoffset -2 rotate 0.14
            linear 0.05 xoffset 0 yoffset 0 rotate 0.0
            pause 0.28
            repeat
    parallel:
        block:
            matrixcolor BrightnessMatrix(-0.11) * SaturationMatrix(0.38)
            pause 0.32
            matrixcolor BrightnessMatrix(0.02) * SaturationMatrix(0.62)
            pause 0.06
            repeat

transform enter_m_op_signal_line(x=0, y=0, w=260, delay=0.0):
    subpixel True
    xpos x
    ypos y
    xsize w
    ysize 10
    alpha 0.0
    xoffset -90
    pause delay
    easeout 0.16 alpha 0.75 xoffset 0
    pause 0.22
    easein 0.14 alpha 0.0 xoffset 90

transform enter_m_op_speed_line(x=0, y=0, w=420, delay=0.0, rot=-11):
    subpixel True
    xpos x
    ypos y
    xsize w
    ysize 7
    rotate rot
    alpha 0.0
    xoffset -720
    pause delay
    linear 0.08 alpha 0.70
    linear 0.42 xoffset 1480
    linear 0.08 alpha 0.0

transform enter_m_op_stage_beam(x=0, color_delay=0.0, rot=0):
    subpixel True
    xpos x
    ypos -110
    xsize 230
    ysize 940
    rotate rot
    alpha 0.0
    pause color_delay
    easeout 0.22 alpha 0.28
    block:
        ease 1.1 xoffset 52 rotate rot + 3
        ease 1.1 xoffset -52 rotate rot - 3
        repeat

# --- 6. FX SCREENS ----------------------------------------------------------
# The reusable visual building blocks the timeline `show screen`s. enter_m_op_overlay
# is the constant frame (letterbox + scanline); the *_card screens compose a BG
# plate + sprite(s) + accent sweeps for a single shot; enter_m_op_cut_fx draws an
# inter-shot transition; enter_m_op_cg_polish dresses a CG with glints/chroma.
# (The shader/particle screens with matching names are defined in op_fx.rpy.)
screen enter_m_op_overlay():
    zorder 90
    add Solid("#0000000c")
    add Solid("#75f7ff26") xysize (1280, 2) at enter_m_op_scanline
    add Solid("#070a0d") xysize (1280, 68) at enter_m_op_letterbox_top
    add Solid("#070a0d") xysize (1280, 68) at enter_m_op_letterbox_bottom

screen enter_m_op_signal_burst():
    zorder 92
    add Solid("#75f7ff88") at enter_m_op_signal_line(130, 150, 310, 0.00)
    add Solid("#ffffff99") at enter_m_op_signal_line(102, 185, 210, 0.08)
    add Solid("#75f7ff77") at enter_m_op_signal_line(930, 174, 260, 0.04)
    add Solid("#d39a5566") at enter_m_op_signal_line(850, 214, 330, 0.12)
    add Solid("#ffffff88") at enter_m_op_signal_line(180, 520, 360, 0.16)
    add Solid("#75f7ff66") at enter_m_op_signal_line(760, 548, 280, 0.20)

screen enter_m_op_pressure_marks():
    zorder 92
    add Solid("#d05f7778") at enter_m_op_speed_line(-380, 126, 740, 0.00, -6)
    add Solid("#ffffff70") at enter_m_op_speed_line(-220, 254, 520, 0.07, 7)
    add Solid("#75f7ff66") at enter_m_op_speed_line(-500, 392, 680, 0.14, -8)
    add Solid("#d39a5570") at enter_m_op_speed_line(-260, 548, 560, 0.21, 5)

screen enter_m_op_stage_fx():
    zorder 91
    add Solid("#75f7ff") at enter_m_op_stage_beam(70, 0.00, -16)
    add Solid("#d39a55") at enter_m_op_stage_beam(930, 0.08, 14)
    add Solid("#ffffff") at enter_m_op_stage_beam(520, 0.16, 0)

screen enter_m_op_matsuda_stage_flair(duration=3.5):
    zorder 92
    add Solid("#ff4fb8") at enter_m_op_idol_sweep(330, 186, 920, 28, -12, 0.02, 1, 0.30)
    add Solid("#75f7ff") at enter_m_op_idol_sweep(940, 548, 760, 22, 8, 0.14, -1, 0.24)
    add Solid("#ffffff") at enter_m_op_idol_sweep(680, 344, 1080, 12, -4, 0.30, 1, 0.20)
    add Solid("#ffffff") at enter_m_op_hand_spark(1000, 506, 260, 7, -18, 0.04, 0.48)
    add Solid("#75f7ff") at enter_m_op_hand_spark(1000, 506, 220, 6, 22, 0.08, 0.34)
    add Solid("#ff4fb8") at enter_m_op_hand_spark(1000, 506, 190, 6, 64, 0.12, 0.30)
    add Solid("#ffffff") at enter_m_op_hand_spark(1000, 506, 170, 5, 112, 0.18, 0.28)
    add Solid("#ffffff") at enter_m_op_confetti_fall(160, 70, 0.08, 1, -18, 0.74)
    add Solid("#75f7ff") at enter_m_op_confetti_fall(460, 52, 0.18, -1, 12, 0.68)
    add Solid("#ff4fb8") at enter_m_op_confetti_fall(740, 86, 0.26, 1, 34, 0.66)
    add Solid("#ffffff") at enter_m_op_confetti_fall(1020, 64, 0.34, -1, -26, 0.72)
    add Solid("#75f7ff") at enter_m_op_confetti_fall(260, 210, 0.54, -1, 42, 0.56)
    add Solid("#ff4fb8") at enter_m_op_confetti_fall(890, 190, 0.66, 1, -36, 0.58)
    add Solid("#ffffff") at enter_m_op_confetti_fall(560, 32, 0.90, 1, 20, 0.50)
    add "noise":
        alpha 0.020
    timer duration action Hide("enter_m_op_matsuda_stage_flair")

screen enter_m_op_cg_polish(cg_image, strength=0.12, duration=1.0, color_a="#75f7ff", color_b="#d05f77", glint=True):
    zorder 89
    # FX upgrade: genuine GPU chromatic aberration on top of the legacy
    # tinted-overlay chroma. Decays from a hard split into a faint fringe.
    if ENTER_M_OP_SHADERS:
        add cg_image at enter_m_op_cg_aberr(strength, duration)
    add cg_image at enter_m_op_chroma_layer(-7, -1, color_a, strength, duration)
    add cg_image at enter_m_op_chroma_layer(7, 1, color_b, strength * 0.82, duration)
    if glint:
        add Solid(color_a) at enter_m_op_cg_glint(300, 176, 620, 12, -7, 0.04, strength * 1.15, 1)
        add Solid("#ffffff") at enter_m_op_cg_glint(950, 512, 560, 9, 6, 0.16, strength * 0.95, -1)
    add "noise":
        alpha strength * 0.16
    timer duration action Hide("enter_m_op_cg_polish")

screen enter_m_op_turmoil_fx(duration=3.7):
    zorder 91
    add Solid("#02040b") at enter_m_op_choke_rect(0, -410, 0, -250, 1280, 430, duration, 0.72)
    add Solid("#02040b") at enter_m_op_choke_rect(0, 704, 0, 592, 1280, 430, duration, 0.70)
    add Solid("#02040b") at enter_m_op_choke_rect(-430, 0, -292, 0, 430, 720, duration, 0.48)
    add Solid("#02040b") at enter_m_op_choke_rect(1280, 0, 1148, 0, 430, 720, duration, 0.48)
    add Solid("#000000") at enter_m_op_turmoil_shadow(0.00, 0.16)
    add Solid("#000000") at enter_m_op_turmoil_shadow(enter_m_op_bar * 0.86, 0.22)
    add Solid("#000000") at enter_m_op_turmoil_shadow(enter_m_op_bar * 1.46, 0.32)
    add Solid("#ffffff") at enter_m_op_turmoil_suffocate_line(-40, 168, 1160, enter_m_op_bar + 0.07, 0.28)
    add Solid("#d05f77") at enter_m_op_turmoil_suffocate_line(80, 236, 980, enter_m_op_bar + 0.19, 0.24)
    add Solid("#75f7ff") at enter_m_op_turmoil_suffocate_line(0, 314, 1280, enter_m_op_bar + 0.31, 0.20)
    add Solid("#ffffff") at enter_m_op_turmoil_suffocate_line(260, 412, 760, enter_m_op_bar + 0.46, 0.26)
    add Solid("#d05f77") at enter_m_op_turmoil_suffocate_line(-80, 506, 1360, enter_m_op_bar + 0.63, 0.22)
    add Solid("#75f7ff") at enter_m_op_turmoil_suffocate_line(120, 122, 1040, enter_m_op_bar + 0.82, 0.18)
    add Solid("#ffffff") at enter_m_op_turmoil_suffocate_line(40, 346, 1200, enter_m_op_bar + 1.02, 0.26)
    add Solid("#d05f77") at enter_m_op_turmoil_suffocate_line(160, 468, 820, enter_m_op_bar + 1.24, 0.22)
    add "noise" at enter_m_op_turmoil_static_rise(duration)
    timer duration action Hide("enter_m_op_turmoil_fx")

screen enter_m_op_memory_glow(duration=1.8, strength=0.12):
    zorder 91
    add Solid("#ffe6a8") at enter_m_op_memory_haze_line(-120, 116, 980, 0.04, strength)
    add Solid("#ffffff") at enter_m_op_memory_haze_line(240, 272, 760, 0.22, strength * 0.82)
    add Solid("#ffd47a") at enter_m_op_memory_haze_line(-80, 548, 1200, 0.40, strength * 0.76)
    add Solid("#fff4d0"):
        alpha strength * 0.18
    add "noise":
        alpha strength * 0.09
    timer duration action Hide("enter_m_op_memory_glow")

screen enter_m_op_memory_loss(duration=1.4):
    zorder 91
    add Solid("#06101d58")
    add Solid("#75f7ff") at enter_m_op_loss_bar(-160, 158, 960, 11, 0.04, 1, 0.20)
    add Solid("#ffffff") at enter_m_op_loss_bar(180, 304, 780, 7, 0.14, -1, 0.16)
    add Solid("#d05f77") at enter_m_op_loss_bar(-120, 512, 1160, 12, 0.27, 1, 0.14)
    add "noise":
        alpha 0.060
    timer duration action Hide("enter_m_op_memory_loss")

screen enter_m_op_bg_plate(bg_image, overlay="#ffffff24", panel="#75f7ff", accent="#d39a55", duration=1.0, xstart=0.48, xend=0.52):
    add enter_m_op_celbg(bg_image, enter_m_op_bg_push(duration, 1.025, 1.105, xstart, xend, 0.51, 0.47))
    add Solid(overlay)
    add Solid(panel) at enter_m_op_panel_sweep(260, 0.00, 1, -11, 0.16)
    add Solid(accent) at enter_m_op_panel_sweep(720, enter_m_op_quarter_bar, -1, 9, 0.11)
    add Solid(accent) at enter_m_op_motion_band(970, 548, 620, 16, 8, 0.12, -1, 0.18)
    add Solid("#ffffff70") at enter_m_op_motion_band(260, 178, 520, 12, -6, 0.20, 1, 0.16)
    add Solid("#00000022")

screen enter_m_op_bg_motion_card(bg_image, sprite, overlay="#ffffff24", panel="#75f7ff", accent="#d39a55", start=-150, end=640, z=0.58, y=742, rot=-4, direction=1, duration=1.0, motion_style="dash"):
    zorder 80
    if motion_style == "arc":
        add enter_m_op_celbg(bg_image, enter_m_op_bg_oblique(duration, 0.57 if direction < 0 else 0.43, 0.43 if direction < 0 else 0.57, 0.54, 0.45, 0.28 * direction))
    elif motion_style == "float":
        add enter_m_op_celbg(bg_image, enter_m_op_bg_breathe(duration, 0.54 if direction < 0 else 0.46, 0.48 if direction < 0 else 0.52, 0.53, 0.45))
    else:
        add enter_m_op_celbg(bg_image, enter_m_op_bg_snap_pan(duration, 0.45 if direction > 0 else 0.55, 0.58 if direction > 0 else 0.42, 0.50, 0.52, 0.46, 0.49))
    add Solid(overlay)
    # 90s-OP double exposure: a giant duotone bust of the same character
    # looming on the opposite side of the frame.
    $ _gz = z * 3.3
    $ _gy = int(960 * _gz) - 40
    add sprite at enter_m_op_ghost_echo(640 - 430 * direction, _gz, _gy, panel, duration, direction)
    add Solid(panel) at enter_m_op_panel_sweep(220 if direction > 0 else 960, 0.00, direction, -12 * direction, 0.18)
    add Solid(accent) at enter_m_op_motion_band(870 if direction > 0 else 320, 214, 720, 18, -7 * direction, enter_m_op_eighth_bar, direction, 0.20)
    add Solid("#ffffff66") at enter_m_op_motion_band(330 if direction > 0 else 940, 548, 580, 11, 5 * direction, enter_m_op_quarter_bar, -direction, 0.14)
    add sprite at enter_m_op_stage_tf(motion_style, start, end, y, z, rot, duration, direction), enter_m_op_sprite_shadow_mod
    add sprite at enter_m_op_stage_tf(motion_style, start, end, y, z, rot, duration, direction)
    add sprite at enter_m_op_stage_tf(motion_style, start, end, y, z, rot, duration, direction), enter_m_op_sprite_flash_mod(duration * 0.34)
    add Solid("#00000024")
    add "noise":
        alpha 0.014

screen enter_m_op_bg_pair_card(bg_image, left_sprite, right_sprite, overlay="#ffffff24", panel="#75f7ff", accent="#d39a55", left_start=-150, left_end=430, right_start=1430, right_end=850, left_z=0.56, right_z=0.58, duration=1.0, left_y=742, right_y=742, left_style="dash", right_style="dash"):
    zorder 80
    if left_style == "arc" or right_style == "arc":
        add enter_m_op_celbg(bg_image, enter_m_op_bg_oblique(duration, 0.43, 0.57, 0.53, 0.45, -0.22))
    else:
        add enter_m_op_celbg(bg_image, enter_m_op_bg_breathe(duration, 0.43, 0.57, 0.51, 0.47))
    add Solid(overlay)
    add Solid(panel) at enter_m_op_panel_sweep(190, 0.00, 1, -14, 0.16)
    add Solid(accent) at enter_m_op_panel_sweep(1010, enter_m_op_eighth_bar, -1, 12, 0.14)
    add Solid("#ffffff66") at enter_m_op_motion_band(640, 170, 860, 12, -4, enter_m_op_quarter_bar, 1, 0.13)
    add Solid(accent) at enter_m_op_motion_band(640, 560, 760, 16, 6, enter_m_op_half_bar, -1, 0.15)
    add left_sprite at enter_m_op_stage_tf(left_style, left_start, left_end, left_y, left_z, -3.0, duration, 1), enter_m_op_sprite_shadow_mod
    add right_sprite at enter_m_op_stage_tf(right_style, right_start, right_end, right_y, right_z, 3.0, duration, -1), enter_m_op_sprite_shadow_mod
    add left_sprite at enter_m_op_stage_tf(left_style, left_start, left_end, left_y, left_z, -3.0, duration, 1)
    add right_sprite at enter_m_op_stage_tf(right_style, right_start, right_end, right_y, right_z, 3.0, duration, -1)
    add left_sprite at enter_m_op_stage_tf(left_style, left_start, left_end, left_y, left_z, -3.0, duration, 1), enter_m_op_sprite_flash_mod(duration * 0.34)
    add right_sprite at enter_m_op_stage_tf(right_style, right_start, right_end, right_y, right_z, 3.0, duration, -1), enter_m_op_sprite_flash_mod(duration * 0.40)
    add Solid("#00000026")
    add "noise":
        alpha 0.014

screen enter_m_op_bg_hold_card(bg_image, sprite, overlay="#ffffff24", panel="#ffffff", accent="#75f7ff", x=640, z=0.56, y=742, rot=0, duration=1.0, motion_style="hold", side=1):
    zorder 80
    if motion_style == "arc":
        add enter_m_op_celbg(bg_image, enter_m_op_bg_oblique(duration, 0.50 - 0.05 * side, 0.50 + 0.06 * side, 0.53, 0.46, 0.18 * side))
    else:
        add enter_m_op_celbg(bg_image, enter_m_op_bg_breathe(duration, 0.50 - 0.035 * side, 0.50 + 0.035 * side, 0.52, 0.47))
    add Solid(overlay)
    $ _gz = z * 3.3
    $ _gy = int(960 * _gz) - 40
    add sprite at enter_m_op_ghost_echo(640 - 430 * side, _gz, _gy, accent, duration, side)
    add Solid(panel) at enter_m_op_motion_band(640, 356, 1080, 24, -4 * side, 0.00, side, 0.16)
    add Solid(accent) at enter_m_op_panel_sweep(450 if side > 0 else 830, enter_m_op_eighth_bar, -side, 7 * side, 0.12)
    add Solid("#ffffff5c") at enter_m_op_motion_band(730 if side > 0 else 550, 188, 520, 9, 6 * side, enter_m_op_quarter_bar, -side, 0.12)
    add sprite at enter_m_op_sprite_hold(x, y, z, rot, duration, side), enter_m_op_sprite_shadow_mod
    add sprite at enter_m_op_sprite_hold(x, y, z, rot, duration, side)
    add sprite at enter_m_op_sprite_hold(x, y, z, rot, duration, side), enter_m_op_sprite_flash_mod(0.22)
    add Solid("#00000022")
    add "noise":
        alpha 0.012

screen enter_m_op_bg_step_card(bg_image, sprite, overlay="#ffffff24", panel="#d39a55", accent="#75f7ff", x1=340, x2=470, x3=610, z=0.56, y=742, rot=-4, duration=1.0, motion_style="step"):
    zorder 80
    add enter_m_op_celbg(bg_image, enter_m_op_bg_snap_pan(duration, 0.42 if x3 > x1 else 0.58, 0.56 if x3 > x1 else 0.44, 0.50, 0.53, 0.46, 0.49))
    add Solid(overlay)
    $ _step_dir = 1 if x3 > x1 else -1
    $ _gz = z * 3.3
    $ _gy = int(960 * _gz) - 40
    add sprite at enter_m_op_ghost_echo(640 - 430 * _step_dir, _gz, _gy, panel, duration, _step_dir)
    add Solid(panel) at enter_m_op_motion_band(260, 214, 580, 14, -9, 0.00, 1, 0.16)
    add Solid(accent) at enter_m_op_motion_band(980, 386, 620, 18, 7, enter_m_op_eighth_bar, -1, 0.18)
    add Solid("#ffffff66") at enter_m_op_panel_sweep(630, enter_m_op_quarter_bar, 1 if x3 > x1 else -1, -8, 0.10)
    add sprite at enter_m_op_sprite_step(x1, x2, x3, y, z, rot, duration), enter_m_op_sprite_shadow_mod
    add sprite at enter_m_op_sprite_step(x1, x2, x3, y, z, rot, duration)
    add sprite at enter_m_op_sprite_step(x1, x2, x3, y, z, rot, duration), enter_m_op_sprite_flash_mod(duration * 0.62)
    add Solid("#00000024")
    add "noise":
        alpha 0.014

screen enter_m_op_bg_shadow_card(bg_image, fg_sprite, shadow_sprite, overlay="#ffffff20", panel="#75f7ff", accent="#d05f77", fg_start=-130, fg_end=430, shadow_start=1420, shadow_end=850, fg_z=0.56, shadow_z=0.62, duration=1.0, fg_style="arc", shadow_style="float"):
    zorder 80
    add enter_m_op_celbg(bg_image, enter_m_op_bg_oblique(duration, 0.44, 0.56, 0.54, 0.45, -0.30))
    add Solid(overlay)
    add Solid("#00000030")
    add Solid(panel) at enter_m_op_panel_sweep(160, 0.00, 1, -16, 0.13)
    add Solid(accent) at enter_m_op_panel_sweep(960, enter_m_op_eighth_bar, -1, 13, 0.18)
    add Solid("#ffffff58") at enter_m_op_motion_band(420, 220, 620, 11, -8, enter_m_op_quarter_bar, 1, 0.12)
    # Both characters render normally -- the moody background lighting carries the
    # drama. (Previously the rear sprite was a dark silhouette, which read as
    # "looming villain" and telegraphed Sam's role; that's gone now.)
    add shadow_sprite at enter_m_op_stage_tf(shadow_style, shadow_start, shadow_end, 742, shadow_z, 3.0, duration, -1), enter_m_op_sprite_shadow_mod
    add shadow_sprite at enter_m_op_stage_tf(shadow_style, shadow_start, shadow_end, 742, shadow_z, 3.0, duration, -1)
    add Solid(accent) at enter_m_op_motion_band(850, 506, 780, 20, 8, enter_m_op_half_bar, -1, 0.16)
    add fg_sprite at enter_m_op_stage_tf(fg_style, fg_start, fg_end, 742, fg_z, -3.0, duration, 1), enter_m_op_sprite_shadow_mod
    add fg_sprite at enter_m_op_stage_tf(fg_style, fg_start, fg_end, 742, fg_z, -3.0, duration, 1)
    add "noise":
        alpha 0.014

screen enter_m_op_cut_fx(kind="dark", strength=0.38):
    zorder 94

    if kind == "white":
        add Solid("#ffffff") at enter_m_op_cut_flash(strength, 0.18)
    elif kind == "red":
        add Solid("#d05f77") at enter_m_op_cut_flash(strength, 0.16)
    elif kind == "blue":
        add Solid("#75f7ff") at enter_m_op_cut_flash(strength, 0.16)
    elif kind == "amber":
        add Solid("#d39a55") at enter_m_op_cut_flash(strength, 0.20)
    elif kind == "wipe_red":
        add Solid("#d05f77") at enter_m_op_cut_wipe(strength, 0.22, -1280, 1280)
    elif kind == "wipe_blue":
        add Solid("#75f7ff") at enter_m_op_cut_wipe(strength, 0.22, 1280, -1280)
    elif kind == "wipe_diag":
        add Solid("#ffffff") at enter_m_op_cut_diag(strength, 0.26, 1)
    elif kind == "wipe_diag_blue":
        add Solid("#75f7ff") at enter_m_op_cut_diag(strength, 0.26, -1)
    elif kind == "wipe_diag_red":
        add Solid("#d05f77") at enter_m_op_cut_diag(strength, 0.26, 1)
    else:
        add Solid("#17202a") at enter_m_op_cut_fade(strength, 0.24)

    timer 0.34 action Hide("enter_m_op_cut_fx")

# The persistent SKIP affordance: a corner button + Esc/Space/Enter all jump to
# the skip label (which cleans up and returns). Shown for the whole OP.
screen enter_m_op_skip():
    zorder 100
    key "K_ESCAPE" action Jump("enter_m_sick_ass_anime_op_skip")
    key "K_SPACE" action Jump("enter_m_sick_ass_anime_op_skip")
    key "K_RETURN" action Jump("enter_m_sick_ass_anime_op_skip")
    key "K_KP_ENTER" action Jump("enter_m_sick_ass_anime_op_skip")

    textbutton "SKIP":
        style "enter_m_op_skip_button"
        xalign 0.985
        yalign 0.025
        action Jump("enter_m_sick_ass_anime_op_skip")

# =============================================================================
# --- 7. THE TIMELINE (main label) ------------------------------------------
# The actual choreographed sequence. Pattern repeated for each "shot":
#   scene <background or CG image name> at <some _stage/_drift transform>
#   show screen <cut_fx / cg_polish / bg_*_card>     # dress the shot
#   $ renpy.pause(<beat-derived seconds>, hard=True) # hold on-beat
#   hide screen ...                                  # tear the shot down
# Inline "0.00s - 14.50s" comments mark section boundaries against the song.
# On entry it saves+disables quick_menu and shows the persistent overlay/skip/
# post-fx; the CALLER is responsible for enter_m_op_cleanup_screens() afterward
# (the skip label does it itself). ENTER_M_OP_SHADERS gates the GPU post-process.
# =============================================================================
label enter_m_sick_ass_anime_op:
    $ enter_m_op_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ renpy.music.stop(fadeout=0.2)
    scene black
    show screen enter_m_op_overlay
    show screen enter_m_op_skip
    # FX upgrade: global grain/vignette/scanline post-process + ambient dust,
    # held for the entire OP (cleaned up with the other OP screens).
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_post_fx
    show screen enter_m_op_ambient_particles("dust")

    # 0.00s - 14.50s: quiet setup before the first drop.
    scene enter_m_op_dark
    show image "assets/dump/finalbg.png" at enter_m_op_bg_push(1.5, 1.00, 1.07, 0.48, 0.53)
    show expression Text("Yo check out this edit (this won't be in the full release lmao)", style="enter_m_op_credit") as enter_m_op_production at enter_m_op_credit_in
    $ renpy.pause(enter_m_op_audio_delay, hard=True)
    play music enter_m_op noloop
    $ renpy.pause(1.5 - enter_m_op_audio_delay, hard=True)

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("dark", 0.34)
    show screen enter_m_op_bg_pair_card("enter_m_op_bg_lightcorridor", "mc neut", "matsuda neut", "#ffffff30", "#75f7ff", "#d39a55", -150, 420, 1430, 860, 0.56, 0.60, 1.2, left_style="arc", right_style="float")
    $ renpy.pause(1.2, hard=True)
    hide screen enter_m_op_bg_pair_card

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("wipe_diag_blue", 0.40)
    show screen enter_m_op_bg_shadow_card("enter_m_op_bg_street", "asahina neut", "sam neut", "#ffffff34", "#75f7ff", "#d05f77", -140, 420, 1420, 850, 0.56, 0.62, 1.5)
    $ renpy.pause(1.5, hard=True)
    hide screen enter_m_op_bg_shadow_card

    # Every CG shot in this montage is also a CG Gallery entry, and the `$
    # enter_m_op_cg_unlock(...)` under each one is what puts it there -- the
    # gallery's "Opening" act fills in as the OP plays, in the order the OP
    # plays it. The unlock sits AFTER the scene rather than before so a CG only
    # counts once it is actually on screen.
    #
    # The dependency runs ONE WAY: the OP draws its own art and the unlock is
    # bookkeeping on top, so a title later pulled out of cg_gallery_catalog is
    # skipped and the OP plays on. Never call cg_unlock directly from here --
    # it raises on an unknown title under config.developer. See
    # enter_m_op_cg_unlock() in section 3.
    scene enter_m_op_mom_work at enter_m_op_cg_drift(1.2, 1.02, 1.06, 0.52, 0.49, 0.50, 0.49)
    $ enter_m_op_cg_unlock("Mom at Work")
    show screen enter_m_op_cg_polish("enter_m_op_mom_work", 0.075, 1.2, "#d39a55", "#75f7ff")
    show screen enter_m_op_cut_fx("amber", 0.24)
    show noise:
        alpha 0.025
    show enter_m_op_amber:
        alpha 0.0
        linear 0.18 alpha 0.10
        linear 0.56 alpha 0.0
    $ renpy.pause(1.2, hard=True)

    scene enter_m_op_storekoto at enter_m_op_cg_drift(1.2, 1.02, 1.06, 0.46, 0.48, 0.50, 0.49)
    $ enter_m_op_cg_unlock("Cashier Kotonoha")
    show screen enter_m_op_cg_polish("enter_m_op_storekoto", 0.08, 1.2, "#75f7ff", "#d39a55")
    show screen enter_m_op_cut_fx("white", 0.22)
    show screen enter_m_op_kinetic_credit("CREATED & WRITTEN BY", "LAWLIET", 170, 132, "#75f7ff", 1.15, 1)
    $ renpy.pause(1.2, hard=True)

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("dark", 0.32)
    show screen enter_m_op_bg_hold_card("enter_m_op_bg_library", "monika 2c", "#ffffff2e", "#ffffff", "#75f7ff", 604, enter_m_op_monika_zoom, enter_m_op_monika_y, -2, 1.0, motion_style="float", side=-1)
    show screen enter_m_op_name_card("MONIKA", 1110, 552, "#75f7ff", 0.95, -1)
    $ renpy.pause(1.0, hard=True)
    hide screen enter_m_op_bg_hold_card

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("wipe_red", 0.28)
    show screen enter_m_op_bg_pair_card("enter_m_op_bg_cafe", "matsuda neut", "tsubaki neut", "#ffffff28", "#d39a55", "#75f7ff", -150, 430, 1430, 850, 0.60, 0.56, 2.0, left_style="float", right_style="arc")
    show screen enter_m_op_kinetic_credit("SPECIAL THANKS", "MODCEN", 1110, 540, "#d39a55", 1.9, -1)
    $ renpy.pause(2.0, hard=True)
    hide screen enter_m_op_bg_pair_card

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("blue", 0.26)
    show screen enter_m_op_bg_step_card("enter_m_op_bg_kitchen", "asahina neut", "#ffffff2a", "#75f7ff", "#ffffff", 330, 486, 640, 0.56, 742, -5, 0.7, motion_style="float")
    show screen enter_m_op_name_card("ASAHINA", 170, 552, "#75f7ff", 0.68, 1)
    $ renpy.pause(0.7, hard=True)
    hide screen enter_m_op_bg_step_card

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("amber", 0.22)
    show screen enter_m_op_bg_motion_card("enter_m_op_bg_lightresidential", "sam neut", "#ffffff22", "#d39a55", "#d05f77", 1430, 710, 0.58, 742, 4, -1, 0.7, motion_style="arc")
    show screen enter_m_op_name_card("SAM", 170, 552, "#d05f77", 0.68, 1)
    $ renpy.pause(0.7, hard=True)
    hide screen enter_m_op_bg_motion_card

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("dark", 0.22)
    show screen enter_m_op_bg_hold_card("enter_m_op_bg_stairs", "tsubaki neut", "#ffffff1e", "#ffffff", "#d05f77", 642, 0.56, 742, -3, 0.8, motion_style="float", side=-1)
    show screen enter_m_op_name_card("TSUBAKI", 1110, 552, "#d05f77", 0.78, -1)
    $ renpy.pause(0.8, hard=True)
    hide screen enter_m_op_bg_hold_card

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("wipe_blue", 0.30)
    show screen enter_m_op_bg_pair_card("enter_m_op_bg_courtyard", "mc neut", "monika 1p", "#ffffff30", "#75f7ff", "#ffffff", -150, 424, 1430, 846, 0.56, enter_m_op_monika_zoom, 1.3, 742, enter_m_op_monika_y, left_style="arc", right_style="float")
    show screen enter_m_op_kinetic_credit("ORIGINAL WORK", "DOKI DOKI LITERATURE CLUB", 170, 132, "#ffffff", 1.25, 1)
    $ renpy.pause(1.3, hard=True)
    hide screen enter_m_op_bg_pair_card

    scene enter_m_op_warning_gray at enter_m_op_stage_tease
    show screen enter_m_op_cut_fx("dark", 0.46)
    show noise:
        alpha 0.05
    $ renpy.pause(1.4, hard=True)

    # 14.50s first drop.
    scene enter_m_op_warning_color at enter_m_op_stage_hit
    $ enter_m_op_cg_unlock("Matsuda Performing")
    show screen enter_m_op_cg_polish("enter_m_op_warning_color", 0.105, 3.5, "#75f7ff", "#ff4fb8")
    show screen enter_m_op_cut_fx("white", 0.52)
    show enter_m_op_white at enter_m_op_flash(0.58)
    show screen enter_m_op_signal_burst
    show screen enter_m_op_stage_fx
    show screen enter_m_op_matsuda_stage_flair(3.5)
    # FX upgrade: shockwave ripple + real spark burst slammed onto the drop,
    # with rotating god rays sweeping the whole hold.
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_impact("enter_m_op_warning_color", "shock", 0.62, z=1.12)
        show screen enter_m_op_rays(0.5, 0.46, (1.0, 0.78, 0.86), 22.0, 0.8, 0.22, 3.5)
    show screen enter_m_op_spark_burst(640, 358, 60, 0.85, 11.0, 13.0)
    $ renpy.pause(3.5, hard=True)
    hide screen enter_m_op_signal_burst
    hide screen enter_m_op_stage_fx
    hide screen enter_m_op_matsuda_stage_flair

    # 18.00s - 44.00s: ensemble montage between drops.
    scene enter_m_op_monika_club at enter_m_op_monika_club_stage(2.4)
    $ enter_m_op_cg_unlock("Club President")
    show screen enter_m_op_cg_polish("enter_m_op_monika_club", 0.06, 2.4, "#75f7ff", "#ffffff")
    show screen enter_m_op_cut_fx("amber", 0.30)
    show noise:
        alpha 0.025
    show enter_m_op_amber:
        alpha 0.0
        linear 0.34 alpha 0.14
        linear 1.20 alpha 0.0
    show screen enter_m_op_kinetic_credit("DIRECTION", "LAWLIET", 170, 128, "#75f7ff", 2.3, 1)
    $ renpy.pause(2.4, hard=True)

    # Split-screen ensemble panel (was a samey pair card): three crops of the
    # bookstore, three characters, alternating slide directions.
    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("wipe_diag", 0.36)
    show screen enter_m_op_split_card("enter_m_op_bg_bookstore", "matsuda neut", "monika 2g", "kotonoha neut", y1=742, z1=0.58, y2=enter_m_op_monika_y, z2=enter_m_op_monika_zoom, y3=742, z3=0.54, accent="#75f7ff", accent2="#d05f77", duration=1.8)
    $ renpy.pause(1.8, hard=True)
    hide screen enter_m_op_split_card

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("dark", 0.22)
    show screen enter_m_op_bg_hold_card("enter_m_op_bg_house_evening", "mc neut", "#ffffff20", "#ffffff", "#75f7ff", 610, 0.56, 742, -2, 1.8, motion_style="arc", side=-1)
    show screen enter_m_op_kinetic_credit("STORYBOARDS & ANIMATICS", "MATSUDA AKAI", 170, 540, "#75f7ff", 1.7, 1)
    $ renpy.pause(1.8, hard=True)
    hide screen enter_m_op_bg_hold_card

    scene enter_m_op_arguing at enter_m_op_cg_impact(2.8, 1.06, 1.11, 0.50, 0.48, 0.50, 0.49)
    $ enter_m_op_cg_unlock("Argue")
    show screen enter_m_op_cg_polish("enter_m_op_arguing", 0.12, 2.8, "#d05f77", "#75f7ff")
    show screen enter_m_op_cut_fx("red", 0.34)
    show screen enter_m_op_pressure_marks
    $ renpy.pause(2.8, hard=True)
    hide screen enter_m_op_pressure_marks

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("amber", 0.24)
    show screen enter_m_op_bg_shadow_card("enter_m_op_bg_musicroom", "tsubaki neut", "sam neut", "#ffffff18", "#d05f77", "#d39a55", -140, 406, 1420, 846, 0.56, 0.62, 2.2)
    $ renpy.pause(2.2, hard=True)
    hide screen enter_m_op_bg_shadow_card

    scene enter_m_op_sam_bus at enter_m_op_cg_drift(2.2, 1.03, 1.08, 0.52, 0.49, 0.50, 0.48)
    $ enter_m_op_cg_unlock("Sam Bus")
    show screen enter_m_op_cg_polish("enter_m_op_sam_bus", 0.07, 2.2, "#d39a55", "#ffffff")
    show screen enter_m_op_cut_fx("white", 0.22)
    show enter_m_op_amber:
        alpha 0.0
        linear 0.22 alpha 0.08
        linear 0.90 alpha 0.0
    $ renpy.pause(2.2, hard=True)

    scene enter_m_op_asahina_poster at enter_m_op_asahina_poster_stage(2.0)
    $ enter_m_op_cg_unlock("Poster Session")
    show screen enter_m_op_cg_polish("enter_m_op_asahina_poster", 0.08, 2.0, "#d39a55", "#75f7ff")
    show screen enter_m_op_cut_fx("amber", 0.30)
    show noise:
        alpha 0.02
    show enter_m_op_amber:
        alpha 0.0
        linear 0.20 alpha 0.12
        linear 0.72 alpha 0.0
    $ renpy.pause(2.0, hard=True)

    # Manga freeze frame (was another step card): Asahina snaps through three
    # halftone poses on amber paper, then melts back to colour.
    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("wipe_diag_red", 0.38)
    show screen enter_m_op_freeze_frame("asahina neut", paper="#f4e8cf", ink="#2a1a10", accent="#d39a55", x=640, y=742, z=0.82, rot=-2.0, duration=1.4)
    $ renpy.pause(1.4, hard=True)
    hide screen enter_m_op_freeze_frame

    scene enter_m_op_matsuda_wistful at enter_m_op_reminisce_stage(3.0)
    $ enter_m_op_cg_unlock("Matsuda Wistful")
    show screen enter_m_op_cg_polish("enter_m_op_matsuda_wistful", 0.040, 3.0, "#d39a55", "#ffffff", glint=False)
    show screen enter_m_op_memory_glow(3.0, 0.070)
    show screen enter_m_op_cut_fx("amber", 0.24)
    # Played straight: the in-lore animator gets her credit on her own shot.
    show screen enter_m_op_kinetic_credit("OPENING ANIMATION", "MATSUDA AKAI", 170, 540, "#d39a55", 2.8, 1)
    show enter_m_op_amber:
        alpha 0.0
        linear 0.46 alpha 0.12
        linear 1.40 alpha 0.0
    $ renpy.pause(3.0, hard=True)

    scene enter_m_op_icecream at enter_m_op_icecream_memory_stage(1.8)
    $ enter_m_op_cg_unlock("Ice Cream")
    show screen enter_m_op_cg_polish("enter_m_op_icecream", 0.040, 1.8, "#ffffff", "#d39a55", glint=False)
    show screen enter_m_op_memory_glow(1.8, 0.155)
    show screen enter_m_op_cut_fx("white", 0.28)
    show noise:
        alpha 0.012
    show enter_m_op_amber:
        alpha 0.0
        linear 0.18 alpha 0.18
        linear 0.90 alpha 0.0
    $ renpy.pause(1.8, hard=True)

    scene enter_m_op_console_tsubaki at enter_m_op_consolation_stage(1.4)
    $ enter_m_op_cg_unlock("Consoling Tsubaki")
    show screen enter_m_op_cg_polish("enter_m_op_console_tsubaki", 0.070, 1.4, "#75f7ff", "#ffffff", glint=False)
    show screen enter_m_op_memory_loss(1.4)
    show screen enter_m_op_cut_fx("blue", 0.34)
    show noise:
        alpha 0.050
    show enter_m_op_dark:
        alpha 0.0
        linear 0.18 alpha 0.20
        linear 0.80 alpha 0.0
    $ renpy.pause(1.4, hard=True)

    scene enter_m_op_redshift at enter_m_op_redshift_stage(2.0)
    $ enter_m_op_cg_unlock("Redshift")
    show screen enter_m_op_cg_polish("enter_m_op_redshift", 0.10, 2.0, "#d05f77", "#ffffff")
    show screen enter_m_op_cut_fx("red", 0.36)
    show noise:
        alpha 0.035
    show enter_m_op_red:
        alpha 0.0
        block:
            linear 0.12 alpha 0.16
            linear 0.44 alpha 0.0
            pause 0.36
            repeat
    $ renpy.pause(2.0, hard=True)

    scene enter_m_op_blueshift at enter_m_op_blueshift_stage(1.2)
    $ enter_m_op_cg_unlock("Blueshift")
    show screen enter_m_op_cg_polish("enter_m_op_blueshift", 0.12, 1.2, "#75f7ff", "#ffffff")
    show screen enter_m_op_cut_fx("wipe_blue", 0.46)
    show noise:
        alpha 0.03
    show enter_m_op_blue:
        alpha 0.0
        block:
            linear 0.04 alpha 0.22
            linear 0.12 alpha 0.0
            pause 0.20
            repeat
    show screen enter_m_op_signal_burst
    $ renpy.pause(1.2, hard=True)
    hide screen enter_m_op_signal_burst

    # 44.00s second drop. The post-drop montage locks to 4-beat bars.
    scene enter_m_op_puppet at enter_m_op_puppet_stage(enter_m_op_bar)
    $ enter_m_op_cg_unlock("Puppet")
    show screen enter_m_op_cg_polish("enter_m_op_puppet", 0.10, enter_m_op_bar, "#ffffff", "#d05f77")
    show screen enter_m_op_cut_fx("white", 0.48)
    show noise:
        alpha 0.035
    show enter_m_op_white at enter_m_op_flash(0.62)
    show screen enter_m_op_signal_burst
    # FX upgrade: zoom-blur punch-in + spark burst on the second drop.
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_impact("enter_m_op_puppet", "zoom", enter_m_op_half_bar, z=1.10)
    show screen enter_m_op_spark_burst(640, 360, 54, 0.8, 12.0, 13.0)
    $ renpy.pause(enter_m_op_bar, hard=True)
    hide screen enter_m_op_signal_burst

    scene enter_m_op_asahina_world_broken at enter_m_op_world_crumble_stage(enter_m_op_bar):
        zoom 1.50
    $ enter_m_op_cg_unlock("World Broken")
    show screen enter_m_op_cg_polish("enter_m_op_asahina_world_broken", 0.09, enter_m_op_bar, "#d05f77", "#75f7ff")
    show screen enter_m_op_cut_fx("wipe_red", 0.36)
    show noise:
        alpha 0.055
    show enter_m_op_red:
        alpha 0.0
        block:
            linear 0.05 alpha 0.16
            linear 0.16 alpha 0.0
            pause 0.44
            repeat
    $ renpy.pause(enter_m_op_bar, hard=True)

    scene enter_m_op_no_marks at enter_m_op_no_marks_stage(enter_m_op_bar)
    $ enter_m_op_cg_unlock("No Marks")
    show screen enter_m_op_cg_polish("enter_m_op_no_marks", 0.075, enter_m_op_bar, "#75f7ff", "#ffffff")
    show screen enter_m_op_cut_fx("wipe_blue", 0.30)
    show noise:
        alpha 0.025
    show enter_m_op_blue:
        alpha 0.0
        block:
            pause 0.16
            linear 0.05 alpha 0.16
            linear 0.18 alpha 0.0
            pause 0.74
            repeat
    $ renpy.pause(enter_m_op_bar, hard=True)

    scene enter_m_op_dark
    show enter_m_op_turmoil as enter_m_op_turmoil_back at enter_m_op_turmoil_backplate(enter_m_op_bar * 2.0)
    show enter_m_op_turmoil as enter_m_op_turmoil_front at enter_m_op_turmoil_chaos(enter_m_op_bar * 2.0)
    $ enter_m_op_cg_unlock("Turmoil")
    show screen enter_m_op_cut_fx("red", 0.55)
    show screen enter_m_op_turmoil_fx(enter_m_op_bar * 2.0)
    # FX upgrade: MC's psyche fracturing -- sustained datamosh + chromatic tear,
    # with off-beat strobes so the whole break feels unstable.
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_psyche_break("enter_m_op_turmoil", enter_m_op_bar * 2.0)
    show noise:
        alpha 0.075
    show enter_m_op_dark:
        alpha 0.0
        linear enter_m_op_bar alpha 0.14
    $ renpy.pause(enter_m_op_beat, hard=True)
    show screen enter_m_op_cut_fx("white", 0.42)
    $ renpy.pause(enter_m_op_beat * 0.5, hard=True)
    show screen enter_m_op_cut_fx("red", 0.40)
    $ renpy.pause(enter_m_op_beat * 1.5, hard=True)
    show screen enter_m_op_cut_fx("wipe_red", 0.46)
    $ renpy.pause(enter_m_op_beat, hard=True)
    show screen enter_m_op_cut_fx("white", 0.30)
    $ renpy.pause(enter_m_op_beat * 0.5, hard=True)
    show screen enter_m_op_cut_fx("blue", 0.34)
    $ renpy.pause(enter_m_op_beat * 1.5, hard=True)
    show screen enter_m_op_cut_fx("white", 0.50)
    $ renpy.pause(enter_m_op_beat * 2.0, hard=True)
    hide screen enter_m_op_turmoil_fx
    hide screen enter_m_op_psyche_break

    # Bars 5-10: half-bar character motion fragments, locked to the 130 BPM grid.
    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("dark", 0.20)
    show screen enter_m_op_bg_hold_card("bg theater_lobby", "mc neut", "#ffffff1a", "#ffffff", "#75f7ff", 612, 0.56, 742, -4, enter_m_op_half_bar, motion_style="float", side=1)
    $ renpy.pause(enter_m_op_half_bar, hard=True)
    hide screen enter_m_op_bg_hold_card

    # Impact frame instead of another pan: Matsuda punched in over a red limbo.
    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("wipe_red", 0.34)
    show screen enter_m_op_bg_impact_card("matsuda neut", "#241016", (1.0, 0.62, 0.74), "#d05f77", 640, 0.74, 742, -2, enter_m_op_half_bar, 0.5)
    show screen enter_m_op_name_card("MATSUDA", 1110, 552, "#d05f77", enter_m_op_half_bar - 0.05, -1)
    $ renpy.pause(enter_m_op_half_bar, hard=True)
    hide screen enter_m_op_bg_impact_card

    # Freeze frame on the half-bar grid: Monika in cyan halftone.
    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("blue", 0.24)
    show screen enter_m_op_freeze_frame("monika 1p", paper="#e8f6fa", ink="#0d1c26", accent="#75f7ff", x=640, y=enter_m_op_monika_y, z=0.66, rot=2.0, duration=enter_m_op_half_bar)
    $ renpy.pause(enter_m_op_half_bar, hard=True)
    hide screen enter_m_op_freeze_frame

    # Impact frame: Asahina punched in over an amber limbo.
    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("amber", 0.30)
    show screen enter_m_op_bg_impact_card("asahina neut", "#1a1208", (1.0, 0.85, 0.5), "#d39a55", 640, 0.74, 742, 2, enter_m_op_half_bar, 0.5)
    $ renpy.pause(enter_m_op_half_bar, hard=True)
    hide screen enter_m_op_bg_impact_card

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("wipe_diag_blue", 0.38)
    show screen enter_m_op_bg_hold_card("enter_m_op_bg_arcade", "tsubaki neut", "#ffffff16", "#ffffff", "#75f7ff", 630, 0.56, 742, -3, enter_m_op_half_bar, motion_style="arc", side=-1)
    $ renpy.pause(enter_m_op_half_bar, hard=True)
    hide screen enter_m_op_bg_hold_card

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("white", 0.22)
    show screen enter_m_op_bg_step_card("enter_m_op_bg_vending", "kotonoha neut", "#ffffff1a", "#d39a55", "#75f7ff", 1120, 900, 670, 0.54, 742, 3, enter_m_op_half_bar)
    show screen enter_m_op_name_card("KOTONOHA", 170, 552, "#d39a55", enter_m_op_half_bar - 0.05, 1)
    $ renpy.pause(enter_m_op_half_bar, hard=True)
    hide screen enter_m_op_bg_step_card

    # Meta-commentary beat (replaces the back half of the character montage --
    # six samey cards): the whole original cast lined up under "is this even a
    # DDLC mod?", then everyone but Monika vanishes for the deadpan "barely."
    # Total duration = bar * 3, exactly the six half-bar cards it stands in for,
    # so the title drop still lands on the grid.
    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("white", 0.40)
    show screen enter_m_op_meta_lineup(enter_m_op_bar * 1.5)
    $ renpy.pause(enter_m_op_bar * 1.5, hard=True)
    hide screen enter_m_op_meta_lineup

    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("dark", 0.34)
    show screen enter_m_op_meta_monika(enter_m_op_bar * 1.5)
    $ renpy.pause(enter_m_op_bar * 1.5, hard=True)
    hide screen enter_m_op_meta_monika

    scene enter_m_op_dark
    show enter_m_op_sam_villain as enter_m_op_sam_villain_back at enter_m_op_sam_villain_backplate(enter_m_op_bar * 2.0)
    show enter_m_op_sam_villain as enter_m_op_sam_villain_front at enter_m_op_sam_villain_stage(enter_m_op_bar * 2.0)
    $ enter_m_op_cg_unlock("Smug Sam")
    show screen enter_m_op_cut_fx("amber", 0.34)
    show noise:
        alpha 0.045
    show enter_m_op_amber:
        alpha 0.0
        block:
            pause 0.16
            linear 0.08 alpha 0.15
            linear 0.24 alpha 0.0
            pause 1.10
            repeat
    show enter_m_op_red as enter_m_op_sam_heat:
        alpha 0.0
        pause enter_m_op_bar
        block:
            linear 0.04 alpha 0.10
            linear 0.16 alpha 0.0
            pause 0.26
            repeat
    show enter_m_op_dark:
        alpha 0.0
        linear 0.34 alpha 0.20
    $ renpy.pause(enter_m_op_bar, hard=True)
    show screen enter_m_op_cut_fx("amber", 0.22)
    $ renpy.pause(enter_m_op_beat, hard=True)
    show screen enter_m_op_cut_fx("white", 0.16)
    $ renpy.pause(enter_m_op_beat, hard=True)
    show screen enter_m_op_cut_fx("amber", 0.18)
    $ renpy.pause(enter_m_op_beat, hard=True)
    show screen enter_m_op_cut_fx("dark", 0.26)
    $ renpy.pause(enter_m_op_beat, hard=True)

    # Primordial chaotic sludge -- no sprites, just churning muck before the
    # "missing" beat. Falls back to a dark, sprite-less plate without shaders.
    scene enter_m_op_dark
    show screen enter_m_op_cut_fx("dark", 0.22)
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_sludge_card(enter_m_op_bar)
    else:
        show screen enter_m_op_bg_plate("assets/dump/finalbg.png", "#0a0f06cc", "#3a3210", "#16240a", enter_m_op_bar, 0.46, 0.54)
    $ renpy.pause(enter_m_op_bar, hard=True)
    if ENTER_M_OP_SHADERS:
        hide screen enter_m_op_sludge_card
    else:
        hide screen enter_m_op_bg_plate

    scene enter_m_op_missing at enter_m_op_missing_stage(enter_m_op_bar * 2.0)
    $ enter_m_op_cg_unlock("Next Line Missing")
    show screen enter_m_op_cg_polish("enter_m_op_missing", 0.13, enter_m_op_bar * 2.0, "#75f7ff", "#d05f77")
    show screen enter_m_op_cut_fx("white", 0.42)
    show noise:
        alpha 0.075
    show enter_m_op_blue:
        alpha 0.0
        block:
            linear 0.04 alpha 0.16
            linear 0.10 alpha 0.0
            pause 0.32
            repeat
    show enter_m_op_red:
        alpha 0.0
        block:
            pause 0.115
            linear 0.035 alpha 0.12
            linear 0.08 alpha 0.0
            pause 0.23
            repeat
    $ renpy.pause(enter_m_op_bar * 2.0, hard=True)

    # 73.54s title drop, sixteen 4-beat bars after the second drop.
    scene enter_m_op_title_drop at enter_m_op_title_plate
    $ enter_m_op_cg_unlock("Title Drop")
    show screen enter_m_op_cg_polish("enter_m_op_title_drop", 0.08, 6.8, "#ffffff", "#75f7ff")
    show screen enter_m_op_cut_fx("white", 0.58)
    show noise:
        alpha 0.045
    show screen enter_m_op_signal_burst
    # FX upgrade: logo shockwave, spark burst, petal fall, and an aberration-
    # pulsed kinetic title. Falls back to the plain fade without shaders.
    show screen enter_m_op_ambient_particles("petal")
    show screen enter_m_op_spark_burst(640, 300, 72, 1.0, 12.0, 14.0)
    if ENTER_M_OP_SHADERS:
        show screen enter_m_op_impact("enter_m_op_title_drop", "shock", 0.7, z=1.05)
        show screen enter_m_op_rays(0.5, 0.44, (0.65, 0.93, 1.0), 26.0, 0.45, 0.30, 7.0)
        show expression Text("ENTER_M", style="enter_m_op_title") as enter_m_op_title at enter_m_op_title_glitch(7.0)
    else:
        show expression Text("ENTER_M", style="enter_m_op_title") as enter_m_op_title:
            xalign 0.5
            yalign 0.80
            alpha 0.0
            yoffset 24
            pause 0.30
            easeout 0.45 alpha 1.0 yoffset 0
    $ renpy.pause(7.0, hard=True)
    hide screen enter_m_op_signal_burst

    $ enter_m_op_cleanup_screens()
    scene black with Dissolve(0.7)
    stop music fadeout 1.0
    $ renpy.pause(1.0, hard=True)
    $ quick_menu = enter_m_op_prev_quick_menu
    return

# SKIP target (jumped to from the skip screen). Stop music, tear down all OP
# screens, fade to black, restore the saved quick_menu, and return to the caller.
label enter_m_sick_ass_anime_op_skip:
    $ quick_menu = False
    stop music fadeout 0.25
    $ enter_m_op_cleanup_screens()
    scene black with Dissolve(0.25)
    $ renpy.pause(0.25, hard=True)
    $ quick_menu = enter_m_op_prev_quick_menu
    return
