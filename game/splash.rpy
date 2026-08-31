init python:
    menu_trans_time = 1
    splash_message_default = "This game is not suitable for the faint\nof heart or the sensitive."

    def enter_m_cleanup_unpickleable_store_values():
        leaked_file = globals().get("f", None)
        if leaked_file is None:
            return

        if not (hasattr(leaked_file, "read") or hasattr(leaked_file, "write") or hasattr(leaked_file, "close")):
            return

        globals().pop("f", None)
        try:
            leaked_file.close()
        except Exception:
            pass

    def splash_hold(mark):
        """
        Hold the cold open until `mark` seconds after `starttime`.

        The cold open is scheduled against absolute wall-clock marks rather than
        relative waits, so a machine that stalls on one beat rejoins the
        schedule on the next instead of pushing every later beat back. A mark
        that has already gone past is simply not waited on.
        """

        remaining = mark - (datetime.datetime.now() - store.starttime).total_seconds()

        if remaining > 0:
            renpy.pause(remaining)

    def enter_m_fresh_run():
        """
        True when Matsu'Py launched this run as a brand new install.

        The install marker lives in the game directory rather than the save
        directory, and deliberately so: it is what distinguishes a reinstall
        from a save wipe, which is the whole point of the prompt below. That
        also puts it out of reach of a throwaway save directory, so the
        launcher signals its intent with MATSU_FRESH_RUN and this game honours
        it. Nothing sets the variable for a player.
        """

        return bool(os.environ.get("MATSU_FRESH_RUN"))

    def enter_m_read_firstrun():
        # A fresh run has never been installed, by definition.
        if enter_m_fresh_run():
            return ""

        try:
            return renpy.file("firstrun").read(1)
        except Exception:
            with open(config.basedir + "/game/firstrun", "wb"):
                pass
            return ""

    def enter_m_write_firstrun():
        # ...and it must not leave a mark on the real install on the way out.
        if enter_m_fresh_run():
            return

        with open(config.basedir + "/game/firstrun", "w") as firstrun_file:
            firstrun_file.write("1")

# Set by the `splashscreen` label; splash_hold() schedules the cold open
# against it. Defaulted so it exists before the label ever runs.
default starttime = None

image splash_warning = ParameterizedText(style="splash_text", xalign=0.5, yalign=0.5)

image menu_bg:
    topleft
    "assets/gui/menu/main_menu_matsuda_evening.png"
    menu_bg_drift

image game_menu_bg:
    topleft
    "assets/gui/menu/game_menu_vn.png"
    menu_bg_drift

# Dedicated menu artwork. Keep these separate from ``menu_bg`` above: that
# image is also part of the authored cold-open plates, while these two belong
# only to the interactive main/game-menu UI.
image enter_m_main_menu_bg:
    topleft
    "assets/gui/menu/main_menu_matsuda_evening.png"

image enter_m_game_menu_bg:
    topleft
    "assets/gui/menu/game_menu_vn.png"

image menu_nav:
    #"assets/gui/overlay/main_menu.png"
    #menu_nav_move

transform menu_bg_drift:
    subpixel True
    zoom 1.035
    xalign 0.5
    yalign 0.5
    block:
        ease 16.0 xoffset -18 yoffset 10
        ease 16.0 xoffset 14 yoffset -8
        repeat

transform menu_logo_reveal:
    subpixel True
    xcenter 984
    ycenter 284
    zoom 0.54
    alpha 0.0
    yoffset 24
    pause 0.10
    easeout 0.70 alpha 1.0 yoffset 0
    block:
        ease 4.5 yoffset -5
        ease 4.5 yoffset 5
        repeat

transform menu_panel_enter(delay=0.0, xoff=-42, yoff=0):
    subpixel True
    alpha 0.0
    xoffset xoff
    yoffset yoff
    pause delay
    easeout 0.45 alpha 1.0 xoffset 0 yoffset 0

transform menu_button_enter(delay=0.0):
    subpixel True
    on show:
        alpha 0.0
        xoffset -18
        pause delay
        easeout 0.35 alpha 1.0 xoffset 0
    on hover:
        easeout 0.12 xoffset 10
    on idle:
        easeout 0.16 xoffset 0

transform menu_scanline_slow:
    subpixel True
    ypos -24
    alpha 0.0
    pause 0.45
    block:
        alpha 0.0
        ypos -24
        linear 0.12 alpha 0.55
        linear 4.0 ypos 744
        linear 0.18 alpha 0.0
        pause 2.2
        repeat

transform splash_bg_push:
    subpixel True
    zoom 1.08
    xalign 0.5
    yalign 0.5
    alpha 0.0
    easeout 0.55 alpha 0.55
    block:
        ease 10.0 xoffset -14 yoffset 7
        ease 10.0 xoffset 10 yoffset -6
        repeat

# =============================================================================
# THE COLD OPEN  --  presenter logos, then the content warning, then the OP
# -----------------------------------------------------------------------------
# WHAT THIS IS
#   The first eight seconds of the game. Two plates: the presenter logos, and
#   the content warning. Neither of them fades. Both are BROADCAST HARDWARE
#   doing something -- a tube hunting for a signal, locking it, holding it, and
#   dropping it -- because that is the vocabulary the rest of the interface is
#   written in (see menu_transitions.rpy, which powers menus off the same idea).
#
# THE ONE STRUCTURAL RULE: EACH PLATE ANIMATES ITSELF, IN AND OUT.
#   These used to be static screens pushed on and pulled off with Dissolve(),
#   which is why the whole cold open read as "three things faded at me". Now the
#   label shows and hides them with NO transition at all and every frame of
#   movement -- entrance, hold and exit -- lives in the screen's own ATL. That
#   also means the timings are readable as a storyboard rather than smeared
#   across a stack of `with Dissolve(max(0, ...))` calls.
#
#   The cost of that rule is that the ATL below and the deadlines in the
#   `splashscreen` label have to agree. THE TIMELINE IS THE CONTRACT:
#
#     LOGO PLATE                          WARNING PLATE
#       0.00  rails slam, tube ignites      0.00  red wash, alert rails drive in
#       0.30  logo A slams + blooms         0.20  panel wipes open from its axis
#       0.62  logo B slams + blooms         0.38  heading converges out of RGB
#       0.95  divider + underlines snap     0.62  message snaps in under a sweep
#       1.20  caption converges out of RGB  0.85  hold, rails breathing
#       1.45  hold, scanlines + grain       2.98  signal skids
#       2.60  signal drops (glitch burst)   3.05  shutter blades slam shut
#       2.80  picture collapses to a line   3.20  picture collapses to a line
#       3.05  gone                          3.45  gone
#
#   The label shows each plate, waits out its whole run, and cuts. A plate's
#   `st` starts on its first RENDER, which is a frame or so after the label
#   shows it, so the label's marks carry ~0.15s of slack past "gone" -- see
#   splash_hold() and the marks in `label splashscreen`.
#
#   Change a number here and change its partner in the label. Nothing else in
#   the game reads these.
#
# WHY THERE IS STILL NO SHADER IN HERE
#   This runs at COLD START, before any shader-bearing scene has been loaded and
#   while the loader is still warming up. Everything below is ATL over Solids
#   and Text -- no matrixcolor, no register_shader, nothing that compiles a GPU
#   program on the first frame the player ever sees. The chromatic separation is
#   done the honest way, by drawing the same text three times in three colours
#   and sliding the copies together; the logo bloom is an additive copy of the
#   logo itself. Both are free. Keep it that way.
# =============================================================================

# -----------------------------------------------------------------------------
# SHARED PARTS
# -----------------------------------------------------------------------------

# Matsu'Py's `easeout_*` warpers ACCELERATE (slow start, fast finish) and the
# `easein_*` ones DECELERATE -- the suffixes are inverted from the CSS
# convention (renpy/common/000atl.rpy says so in as many words). So every slam
# below is `easein_expo`: full speed on frame one, dead stop on the mark.

# The hot line that ignites the tube: snaps on, blooms open, is gone.
transform splash_ignite:
    subpixel True
    additive 1.0
    xysize (1280, 3)
    xalign 0.5
    yalign 0.5
    alpha 0.0
    linear 0.04 alpha 1.0
    parallel:
        easeout_expo 0.30 yzoom 260.0
    parallel:
        pause 0.08
        linear 0.24 alpha 0.0

# A full-frame hit of light. Up in two frames, gone in four -- any longer or any
# brighter and it stops reading as an impact and starts washing the logo out,
# which is the opposite of what an impact is for.
transform splash_impact(delay=0.0, peak=0.34):
    subpixel True
    alpha 0.0
    pause delay
    linear 0.02 alpha peak
    easeout_quad 0.12 alpha 0.0

# Torn sync: a band of picture that skids to the wrong place for a frame at a
# time. Deliberately UNWARPED -- every step is an instant set followed by a
# pause, because a glitch that eases is not a glitch.
transform splash_tear(y0=180, delay=0.0, h=10):
    subpixel True
    additive 1.0
    xysize (1280, h)
    xpos 0
    ypos y0
    alpha 0.0
    pause delay
    alpha 0.55
    pause 0.035
    ypos y0 + 130
    alpha 0.28
    pause 0.030
    ypos y0 - 80
    alpha 0.50
    pause 0.035
    ypos y0 + 240
    alpha 0.20
    pause 0.030
    alpha 0.0

# The chromatic split. `dx` is which side this copy comes in from (-1 red,
# +1 cyan, 0 the white master), and it lands two pixels short of home so a
# fringe survives the convergence.
transform splash_split(dx=0.0, delay=0.0, spread=18):
    subpixel True
    alpha 0.0
    xoffset dx * spread
    pause delay
    linear 0.04 alpha 1.0
    easein_expo 0.26 xoffset dx * 2.0

# A status light: holds off until its beat, then breathes. The plain
# console_blink is alive from frame one, which put "SIGNAL LOCKED" on screen
# before the tube it is reporting on had ignited.
transform splash_micro_blink(delay=0.0):
    subpixel True
    alpha 0.0
    pause delay
    linear 0.04 alpha 1.0
    block:
        easeout 0.75 alpha 0.25
        easein 0.75 alpha 1.0
        repeat

# Hard snap into place from below. No fade -- the alpha step is four hundredths
# of a second, which reads as a cut.
transform splash_snap_in(delay=0.0, rise=16):
    subpixel True
    alpha 0.0
    yoffset rise
    pause delay
    linear 0.04 alpha 1.0
    easein_expo 0.22 yoffset 0

# A bright bar that crosses the frame once, left to right, and does not return.
transform splash_sweep_once(delay=0.0, y=0, h=2, travel=0.34):
    subpixel True
    additive 1.0
    xysize (1280, h)
    ypos y
    xpos -1300
    alpha 0.0
    pause delay
    linear 0.03 alpha 0.9
    parallel:
        easein_expo travel xpos 1300
    parallel:
        pause travel
        linear 0.06 alpha 0.0

# Faint rolling grain, kept low so the logos stay crisp.
transform splash_grain:
    subpixel True
    alpha 0.0
    easeout 0.7 alpha 0.05

# Scanline sweeps, one each way, for layered motion during the holds.
transform splash_sweep:
    subpixel True
    ypos -16
    alpha 0.0
    pause 0.30
    block:
        alpha 0.0
        ypos -16
        linear 0.08 alpha 0.75
        linear 1.6 ypos 736
        linear 0.12 alpha 0.0
        pause 0.7
        repeat

transform splash_sweep2:
    subpixel True
    ypos 760
    alpha 0.0
    pause 0.55
    block:
        alpha 0.0
        ypos 760
        linear 0.1 alpha 0.55
        linear 2.4 ypos -20
        linear 0.15 alpha 0.0
        pause 1.1
        repeat

# -----------------------------------------------------------------------------
# PLATE 1: THE PRESENTER LOGOS
# -----------------------------------------------------------------------------

# Letterbox rails. They slam the frame shut to a cinema crop, hold for a beat,
# then withdraw to a hairline that stays as chrome for the rest of the plate.
transform splash_rail_top:
    subpixel True
    xysize (1280, 96)
    xpos 0
    ypos -96
    easein_expo 0.20 ypos 0
    pause 0.24
    easein_cubic 0.28 ypos -90

transform splash_rail_bottom:
    subpixel True
    xysize (1280, 96)
    xpos 0
    ypos 720
    easein_expo 0.20 ypos 624
    pause 0.24
    easein_cubic 0.28 ypos 714

# The logo slam: in from three times its size at full speed, a dead stop just
# under the mark, then a spring out to it. `easein_back` overshoots on arrival
# and settles, which is the recoil.
transform splash_logo_slam(xc=640, yc=320, z=0.30, delay=0.0):
    subpixel True
    xcenter xc
    ycenter yc
    zoom z * 3.2
    alpha 0.0
    pause delay
    parallel:
        easein_expo 0.22 zoom z * 0.955
    parallel:
        linear 0.05 alpha 1.0
    easein_back 0.18 zoom z
    # Locked. A slow idle float so the plate is never actually still.
    block:
        ease 3.4 yoffset -5
        ease 3.4 yoffset 5
        repeat

# The bloom that lands with it: the same logo, additive, still expanding as it
# burns off. This is the whole reason the slam has weight.
transform splash_logo_bloom(xc=640, yc=320, z=0.30, delay=0.0):
    subpixel True
    additive 1.0
    xcenter xc
    ycenter yc
    zoom z * 3.2
    alpha 0.0
    pause delay
    linear 0.04 alpha 0.7
    parallel:
        easein_expo 0.30 zoom z * 1.16
    parallel:
        pause 0.06
        linear 0.26 alpha 0.0

# Accent underline that snaps out from its centre beneath a logo, then dims.
transform splash_underline(xc=640, yc=452, delay=0.0):
    subpixel True
    xcenter xc
    ycenter yc
    xanchor 0.5
    xzoom 0.0
    alpha 0.0
    pause delay
    parallel:
        easein_expo 0.20 xzoom 1.0
    parallel:
        linear 0.05 alpha 1.0
    pause 0.7
    linear 1.6 alpha 0.4

# Central hairline divider, punched out from its midpoint.
transform splash_divider(delay=0.95):
    subpixel True
    yzoom 0.0
    alpha 0.0
    pause delay
    parallel:
        easein_circ 0.18 yzoom 1.0
    parallel:
        linear 0.05 alpha 1.0

# Corner brackets, snapped in rather than faded up.
transform splash_bracket_snap(delay=0.0):
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.06
    alpha 0.0
    pause delay
    linear 0.04 alpha 1.0
    easein_expo 0.24 zoom 1.0

# THE PLATE ITSELF, and how it dies: at 3.15 the signal starts to go -- the
# picture skids sideways a few times -- and then the tube gives up, squashing
# to a hairline and pinching out. Same power-off the pause menu uses on the way
# back to a scene, which is not a coincidence.
transform splash_signal_drop:
    subpixel True
    xalign 0.5
    yalign 0.5
    pause 2.60
    linear 0.03 xoffset 14
    linear 0.03 xoffset -10
    linear 0.03 xoffset 6
    linear 0.03 xoffset -4
    linear 0.03 xoffset 0
    pause 0.04
    easein_expo 0.16 yzoom 0.012
    parallel:
        easein_expo 0.09 xzoom 0.0
    parallel:
        linear 0.09 alpha 0.0

screen enter_m_splash_intro():

    fixed:
        at splash_signal_drop

        add Solid("#02040b")
        add "assets/gui/menu/main_menu_matsuda_evening.png" at splash_bg_push
        add Solid("#000000aa")
        add "vignette":
            alpha 0.5
        add "noise" at splash_grain

        # Layered scanline sweeps -- motion without a heavy per-line field.
        add Solid("#75f7ff30") xysize (1280, 2) at splash_sweep
        add Solid("#ff2f5f18") xysize (1280, 1) at splash_sweep2

        # Cinema crop, slammed shut and withdrawn.
        add Solid("#02040b") at splash_rail_top
        add Solid("#02040b") at splash_rail_bottom

        # Ignition, and the torn sync it drags in with it.
        add Solid("#bdf6ff") at splash_ignite
        add Solid("#56d7ff") at splash_tear(196, 0.20, 12)
        add Solid("#ff315b") at splash_tear(408, 0.24, 7)

        # THE PRESENTER TRIANGLE -- two marks up top, one centred beneath them.
        # Each lands on its own beat with its own bloom, impact and tear, read
        # left-to-right across the top row and then down onto the anchor.
        #
        # Zooms are chosen so all three render to roughly the same 310px width
        # despite very different source sizes, and so the whole group clears the
        # console bracket at (160, 116)-(1120, 542):
        #     TRM       1200x600   @0.225 -> 270 x 135
        #     MATSU'PY  1920x1080  @0.141 -> 271 x 152 (art is a 2.17:1 band
        #               inside a 16:9 canvas, so zoom against the CANVAS width)
        #     TS_SF     1280x720   @0.211 -> 270 x 152
        #
        # Vertically the group runs 174..506 between the caption (y=150) and the
        # bracket floor (y=542), with the two underline bands at 338 and 520.
        # Everything must be landed before splash_signal_drop starts collapsing
        # the plate at 2.60s; the last beat here is the third underline at 1.42.

        # Hairline between the top pair only -- the bottom mark is the apex and
        # is not divided from anything.
        add Solid("#56d7ff3a") xysize (2, 130) xcenter 640 ycenter 250 at splash_divider(1.26)

        add "assets/gui/TRM_splash.png" at splash_logo_bloom(430, 250, 0.225, 0.30)
        add "assets/gui/TRM_splash.png" at splash_logo_slam(430, 250, 0.225, 0.30)
        add Solid("#bdf6ff") at splash_impact(0.52, 0.42)
        add Solid("#ff315b") at splash_tear(268, 0.52, 6)

        add "assets/gui/matsupy_splash.png" at splash_logo_bloom(850, 250, 0.141, 0.62)
        add "assets/gui/matsupy_splash.png" at splash_logo_slam(850, 250, 0.141, 0.62)
        add Solid("#bdf6ff") at splash_impact(0.84, 0.42)
        add Solid("#56d7ff") at splash_tear(300, 0.84, 9)

        add "assets/gui/TS_SF_splash.png" at splash_logo_bloom(640, 430, 0.211, 0.94)
        add "assets/gui/TS_SF_splash.png" at splash_logo_slam(640, 430, 0.211, 0.94)
        add Solid("#bdf6ff") at splash_impact(1.16, 0.42)
        add Solid("#ff315b") at splash_tear(214, 1.16, 8)

        # Underline accents that snap out beneath each mark. The bottom one sits
        # at y=520 between SIGNAL LOCKED and BUILD, which are pinned to the left
        # and right edges, so it passes cleanly between them.
        add Solid("#56d7ff") xysize (230, 2) at splash_underline(430, 338, 1.30)
        add Solid("#56d7ff") xysize (230, 2) at splash_underline(850, 338, 1.36)
        add Solid("#56d7ff") xysize (230, 2) at splash_underline(640, 520, 1.42)

        # The presenter caption, converged out of an RGB separation: red and
        # cyan ghosts drive in from either side and land two pixels off the
        # white master, so the fringe survives.
        text "N O W   P R E S E N T I N G":
            style "splash_boot_caption"
            color "#ff315b"
            xalign 0.5
            ypos 150
            at splash_split(-1, 1.20, 22)

        text "N O W   P R E S E N T I N G":
            style "splash_boot_caption"
            color "#56d7ff"
            xalign 0.5
            ypos 150
            at splash_split(1, 1.20, 22)

        text "N O W   P R E S E N T I N G":
            style "splash_boot_caption"
            xalign 0.5
            ypos 150
            at splash_split(0, 1.20, 22)

        # One bright pass across the caption as it lands.
        add Solid("#bdf6ff") at splash_sweep_once(1.24, 148, 3, 0.30)

        # Console microtext, snapped rather than faded.
        text "ENTER-M // SYSTEM BOOT 0x4D":
            style "splash_boot_micro"
            xpos 168
            ypos 132
            at splash_snap_in(1.34, 10)

        text "SIGNAL LOCKED":
            style "splash_boot_micro"
            xpos 168
            ypos 522
            at splash_micro_blink(1.40)

        text "BUILD [config.version]":
            style "splash_boot_micro"
            xanchor 1.0
            xpos 1112
            ypos 522
            at splash_snap_in(1.44, 10)

        # Console brackets framing the presentation, matching the game-wide HUD.
        fixed:
            at splash_bracket_snap(1.10)
            use console_brackets(160, 116, 960, 426, "#56d7ff6e", 26, 2)

# -----------------------------------------------------------------------------
# PLATE 2: THE CONTENT WARNING
# -----------------------------------------------------------------------------
# Same hardware, different mood: this one is an ALERT, so it arrives red and
# horizontal and it closes like a shutter rather than drifting away.

# The wash that announces it -- one hit of red across the whole frame.
transform splash_alert_wash:
    subpixel True
    alpha 0.0
    linear 0.03 alpha 0.38
    easeout_quad 0.30 alpha 0.0

# Alert rails: driven in from off-frame, then left breathing for the hold.
transform splash_alert_rail(y=196, xstart=-1300, delay=0.0, h=5):
    subpixel True
    xysize (1280, h)
    ypos y
    xpos xstart
    alpha 0.0
    pause delay
    linear 0.03 alpha 0.9
    easein_expo 0.26 xpos 0
    block:
        easeout 0.8 alpha 0.42
        easein 0.8 alpha 0.9
        repeat

# The panel does not fade up: it is wiped open along its own horizontal axis,
# which squashes the text inside it for a fifth of a second. That squash is the
# effect -- it is what a picture tube opening looks like.
transform splash_alert_open(delay=0.20):
    subpixel True
    yzoom 0.0
    pause delay
    easein_circ 0.24 yzoom 1.0

# The shutter that closes the plate: two blades meeting in the middle.
transform splash_shutter_top(delay=3.05):
    subpixel True
    xysize (1280, 362)
    xpos 0
    ypos -362
    pause delay
    easein_expo 0.20 ypos 0

transform splash_shutter_bottom(delay=3.05):
    subpixel True
    xysize (1280, 362)
    xpos 0
    ypos 720
    pause delay
    easein_expo 0.20 ypos 358

# THE PLATE, and how it dies: the shutter lands at 3.25, and the tube pinches
# out from under it.
transform splash_alert_shutdown:
    subpixel True
    xalign 0.5
    yalign 0.5
    pause 2.98
    linear 0.03 xoffset -12
    linear 0.03 xoffset 9
    linear 0.03 xoffset -5
    linear 0.03 xoffset 0
    pause 0.17
    easein_expo 0.16 yzoom 0.010
    parallel:
        easein_expo 0.09 xzoom 0.0
    parallel:
        linear 0.09 alpha 0.0

screen enter_m_splash_warning(message):

    fixed:
        at splash_alert_shutdown

        add Solid("#02040b")
        add "assets/gui/menu/main_menu_matsuda_evening.png" at splash_bg_push
        add Solid("#000000cc")
        add Solid("#ff2f5f18") xysize (1280, 1) at splash_sweep2

        # The hit of red that announces the plate.
        add Solid("#ff2f5f") at splash_alert_wash

        # Rails above and below the panel, driving in from opposite sides.
        add Solid("#ff4968") at splash_alert_rail(214, -1300, 0.02, 5)
        add Solid("#ff4968") at splash_alert_rail(500, 1300, 0.08, 5)
        add Solid("#ff315b") at splash_alert_rail(222, -1300, 0.02, 1)

        frame:
            style "splash_warning_panel"
            at splash_alert_open(0.20)

            vbox:
                xalign 0.5
                yalign 0.5
                spacing 18

                null height 4

                text message:
                    style "splash_text"
                    at splash_snap_in(0.62, 18)

        # The heading rides OVER the panel so the panel's wipe does not squash
        # it, converged out of the same RGB separation the logo plate uses.
        text "CONTENT WARNING":
            style "splash_warning_heading"
            color "#ff0040"
            xalign 0.5
            ypos 262
            at splash_split(-1, 0.38, 26)

        text "CONTENT WARNING":
            style "splash_warning_heading"
            color "#56d7ff"
            xalign 0.5
            ypos 262
            at splash_split(1, 0.38, 26)

        text "CONTENT WARNING":
            style "splash_warning_heading"
            xalign 0.5
            ypos 262
            at splash_split(0, 0.38, 26)

        # One pass of light across the plate as the message snaps in. It rides
        # ABOVE the text, not through it -- crossing the words at their own
        # height reads as a strike-through rather than a scan.
        add Solid("#ffd8e2") at splash_sweep_once(0.64, 306, 2, 0.32)

        # The shutter, and the flash of its blades meeting.
        add Solid("#02040b") at splash_shutter_top(3.05)
        add Solid("#02040b") at splash_shutter_bottom(3.05)
        add Solid("#ffe6ec") at splash_impact(3.24, 0.45)

image intro:
    truecenter
    "white"
    0.5
    "assets/backgrounds/splash.png" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

image warning:
    truecenter
    "white"
    "splash_warning" with Dissolve(0.5, alpha=True)
    2.5
    "white" with Dissolve(0.5, alpha=True)
    0.5

image tos = "assets/gui/warning.png"
image tos2 = "assets/gui/warning2.png"

label splashscreen:

    $ enter_m_cleanup_unpickleable_store_values()

    python:
        firstrun = enter_m_read_firstrun()
    if not firstrun:
        if persistent.first_run and config.version == persistent.oldversion:
            $ quick_menu = False
            scene black
            menu:
                "A previous save file has been found. Would you like to delete your save data and start over?"
                "Yes, delete my existing data.":
                    "Deleting save data...{nw}"
                    python:
                        delete_all_saves()
                        renpy.loadsave.location.unlink_persistent()
                        renpy.persistent.should_save_persistent = False
                        renpy.utter_restart()
                "No, continue where I left off.":
                    pass

        python:
            if not firstrun:
                try:
                    enter_m_write_firstrun()
                except:
                    renpy.jump("readonly")

    if config.version != persistent.oldversion:
        $ persistent.oldversion = config.version
        $ renpy.save_persistent()

    if not persistent.first_run:
        $ quick_menu = False
        scene white
        pause 0.5
        scene tos
        with Dissolve(1.0)
        pause 1.0

        # ==================================================================================================================================================
        # CHANGE THIS TO YOUR OWN TERMS OF SERVICE
        # ==================================================================================================================================================

        "This is an early demo build of ENTER-M."
        "This build contains placeholder art, temporary audio, unfinished systems, and experimental scenes."
        "Some presentation, story flow, and archive features may change before a later release."
        "{b}Personal note: some placeholder artwork in this demo was created using Stable Diffusion (with my own trained generation models and pipelines).{/b}"
        "{b}They're PLACEHOLDERS. This game is being developed by one person who can't draw worth anything, nor can a dedicated artist be afforded.{/b}"
        "{b}If that upsets you or gives you tunnel vision that automatically invalidates the rest of the game, then I'm sorry for being a talentless hack.{/b}"
        "{b}All I ask is that you don't antagonize me for it, and at least give the game a shot.{/b}"
        "{b}Anyway...{/b}"
        "The full story is planned to include mature topics."
        "By playing this game, you agree that you are of sufficient age and mental state to handle the contents within."
        $ persistent.first_run = True
        scene tos2
        with Dissolve(1.5)
        pause 1.0
        scene white

    $ config.allow_skipping = False


    # THE COLD OPEN. Every mark below is wall-clock seconds from `starttime`, and
    # every one of them is a HARD CUT: each plate performs its own entrance and
    # its own exit (see the timeline contract at the top of this file), so a
    # transition here would only smear an animation that has already finished.
    # The marks are absolute rather than relative so a slow machine that spends
    # too long on one beat catches up on the next instead of drifting; `pause`
    # is floored at zero for the same reason.
    scene black
    $ starttime = datetime.datetime.now()

    show screen enter_m_splash_intro
    $ splash_hold(3.25)             # plate has collapsed and gone by ~3.15
    hide screen enter_m_splash_intro

    show screen enter_m_splash_warning(splash_message_default)
    $ splash_hold(6.95)             # plate has collapsed and gone by ~6.85
    hide screen enter_m_splash_warning

    $ splash_hold(7.10)             # one black beat before the OP hits
    scene black
    call enter_m_sick_ass_anime_op from _call_enter_m_sick_ass_anime_op_1
    $ config.allow_skipping = True
    return

label after_load:
    $ enter_m_cleanup_unpickleable_store_values()
    if exam_guard_rejects_restart_load():
        jump exam_guard_bad_ending_locked_load
    if exam_guard_requires_exam_restart():
        $ exam_guard_accept_restart_load()
    $ exam_guard_prepare_after_load()
    if exam_guard_has_mismatch():
        jump expression exam_guard_caught_label()
    $ config.allow_skipping = allow_skipping
    $ _dismiss_pause = config.developer

    if anticheat != persistent.anticheat:
        stop music
        $ atmos_clear()
        scene black
        "The save file could not be loaded."
        "Are you trying to cheat?"
        $ m_name = "Monika"
        show monika forward uniform happ cm oe nobl rdown ldown at t11
        if persistent.playername == "":
            m "You're so funny."
        else:
            m "You're so funny, [persistent.playername]."
        $ renpy.utter_restart()
    else:
        if persistent.playthrough == 0 and not persistent.first_load and not config.developer:
            $ persistent.first_load = True
            call screen dialog("Hint: You can use the \"Skip\" button to\nfast-forward through text you've already read.", ok_action=Return())
    return

label before_main_menu:
    $ config.main_menu_music = audio.mainmenu
    $ enter_m_menu_music(config.main_menu_music)
    return

label readonly:
    scene black
    "The game cannot be run because you are trying to run it from a read-only location."
    "Please move ENTER-M to your desktop or another writable location and try again."
    $ renpy.quit()
    return
