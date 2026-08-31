# =============================================================================
# ENTER-M :: fx.rpy  --  WHAT SURVIVED THE MOTION-FX TEARDOWN
# -----------------------------------------------------------------------------
# THIS FILE USED TO BE THE MOTION LIBRARY. It is not one any more.
#
# On 2026-08-08 the sprite-motion / ambient-camera system was dismantled on
# purpose, to be rebuilt from the ground up later. The whole gesture and idle
# vocabulary (fx_breathe, fx_point, fx_toss, fx_step_in, fx_bounce, ...), the
# ambient camera family (fx_hold / fx_pull / fx_drift / fx_breeze / fx_handheld
# / fx_camera_move), the shake and quake helpers, the strobes, the letterbox
# and the flash/blackout set were all DELETED along with every call site in
# game/story/season1/0515-0521.rpy. Do not go looking for them; they are gone,
# not moved. Anything you need, write fresh.
#
# WHY IT WAS TORN DOWN  --  READ THIS BEFORE REBUILDING, IT WILL SAVE YOU A DAY
#   The library worked. What did not work was leaving a transform attached to a
#   talking sprite, and the cause is in the engine, not in the effects:
#
#     * renpy/display/core.py SceneLists.add() only preserves a running
#       transform when a show passes NO at_list (the config.keep_running_transform
#       fast path, which swaps the child under the existing chain). Any show
#       that DOES pass an at_list falls through to transform_state(old, new),
#       whose `execution` parameter defaults to False -- so take_execution_state
#       is never called and the ATL restarts from frame zero.
#     * config.sticky_positions (switched on by addons/Autofocus) INJECTS the
#       previous at_list into every show that omits one -- see
#       renpy/exports.py show(), the `if renpy.config.sticky_positions:` branch.
#     * Every say line carrying image attributes ("m forward casual happ ...")
#       is such a show.
#
#   Net effect: any one-shot modifier on a sprite replays in full on every line
#   that character speaks, forever. Measured, not guessed -- an fx_toss(40.0)
#   ran its entire wind-up-and-throw on all five following lines, and it still
#   did so with Autofocus disabled completely, so the addon is not the culprit.
#   fx_breathe had always been restarting too; a looping idle just makes the
#   restart invisible, which is why this went unnoticed for so long.
#
#   Three ways out, none of them attempted yet. Pick one FIRST, next time:
#     1. Expire gestures centrally -- a character callback that removes a
#        one-shot from the at_list after the beat it was written for, so a
#        restart has nothing left to restart. Costs: "held" gestures cannot
#        hold.
#     2. Never leave a gesture attached -- re-show the sprite at an idle on the
#        very next beat, every time, no exceptions. Costs: verbose, and a
#        forgotten line silently reintroduces the bug.
#     3. Stop relying on sticky_positions so attribute shows take the
#        keep_running_transform path. Costs: SceneLists.add unconditionally
#        overwrites at_list, so Autofocus must stop reading it, and it changes
#        sprite handling for the whole game.
#   NOTE that ATL parameter defaults are evaluated when the `transform`
#   statement executes at INIT, not per show (renpy/ast.py:1298 ->
#   renpy/atl.py:341), so the get_time() stamp trick that fixes layer drivers
#   cannot be smuggled into a gesture's default argument.
#
# WHAT IS STILL HERE, AND WHY EACH PIECE EARNED ITS PLACE
#   1. Vanilla DDLC leftovers (noise / noise_alpha / vignette / yuripupils).
#      Used by ~20 files across the project. Never part of the motion system.
#   2. The scene-transition family (dissolve / dissolve_scene_full /
#      dissolve_scene_half / dissolve_scene_soft / wipeleft_scene) and the
#      fx_rack_* transforms they are built from. EVERY scene change in the game
#      goes through these. They are transitions, not sprite motion, and they
#      were never implicated in the bug above.
#   3. enter_m_rgba, the project's hex -> normalized-RGBA parser, which the
#      Arcade panels, the boss-fight FX layer and the PhonePanel toolkit all
#      import from here.
#   4. Exactly six motion pieces that two out-of-context scenes still call:
#      fx_push, fx_lean_in, fx_flinch, fx_punch_soft, fx_thud, fx_shake_screen.
#      They are kept ONLY for ooc_1030_uhoh.rpy and ooc_0604_out_of_ten.rpy.
#      If those scenes are ever rewritten, delete this section with them.
#
#   Lighting, colour and grade were never in this file and are untouched: see
#   atmosphere.rpy, and theater_fx.rpy for the cinema house-lights shader.
# =============================================================================


# =============================================================================
# 1. INHERITED VANILLA PIECES
# =============================================================================
# Not original work -- these came out of vanilla DDLC's transforms.rpy, and they
# live here so that transforms.rpy can be nothing but the slot table.

image noise:
    truecenter
    "assets/backgrounds/noise1.jpg"
    pause 0.1
    "assets/backgrounds/noise2.jpg"
    pause 0.1
    "assets/backgrounds/noise3.jpg"
    pause 0.1
    "assets/backgrounds/noise4.jpg"
    pause 0.1
    xzoom -1
    "assets/backgrounds/noise1.jpg"
    pause 0.1
    "assets/backgrounds/noise2.jpg"
    pause 0.1
    "assets/backgrounds/noise3.jpg"
    pause 0.1
    "assets/backgrounds/noise4.jpg"
    pause 0.1
    yzoom -1
    "assets/backgrounds/noise1.jpg"
    pause 0.1
    "assets/backgrounds/noise2.jpg"
    pause 0.1
    "assets/backgrounds/noise3.jpg"
    pause 0.1
    "assets/backgrounds/noise4.jpg"
    pause 0.1
    xzoom 1
    "assets/backgrounds/noise1.jpg"
    pause 0.1
    "assets/backgrounds/noise2.jpg"
    pause 0.1
    "assets/backgrounds/noise3.jpg"
    pause 0.1
    "assets/backgrounds/noise4.jpg"
    pause 0.1
    yzoom 1
    repeat

transform noise_alpha:
    alpha 0.25

# THE project vignette. One definition, project-wide. atmosphere.rpy also draws
# a vignette, but as a term inside its grade shader rather than as a
# displayable -- that is not a duplicate and must not be "unified" with this.
#
# SOURCED AT 480x270 AND SCALED ON THE GPU. The full-size file is a pure alpha
# ramp -- RGB is zero across every pixel, and it is smooth enough that a 480px
# source reconstructs it to a MEASURED maximum error of 2/255, before the 0.34
# alpha every call site draws it at takes even that below one part in 255. At
# 1280x720 it cost 15.5ms to decode, which was the second largest single item
# in the Arcade hub's cold open; at 480x270 it is under 2ms, on all three
# screens that use it. assets/backgrounds/vignette.png is the original and is
# no longer loaded -- kept because it is the only copy, not because it is used.
image vignette:
    truecenter
    Transform("assets/backgrounds/vignette_soft.png", xysize=(1280, 720))

transform yuripupils_move:
    function yuripupils_function

init python:
    def yuripupils_function(trans, st, at):
        trans.xoffset = -1 + random.random() * 9 - 4
        trans.yoffset = 3 + random.random() * 6 - 3
        return random.random() * 1.2 + 0.3


# =============================================================================
# 2. SCENE TRANSITIONS  --  the rack-focus family
# =============================================================================
# THE CALL PATTERN THESE ARE BUILT AROUND (every story file does this):
#     scene black with wipeleft_scene     # old scene -> black
#     <re-dress the stage>
#     with wipeleft_scene                 # black -> new scene
# So each of these runs TWICE per scene change: once with the REAL scene as the
# outgoing frame and black as the incoming one, then once the other way round.
#
# THE BLACK PROBLEM, AND HOW THIS SET SOLVES IT
#   These used to be MultipleTransition sandwiches -- fade out, HOLD on a black
#   plate, fade in -- run twice. Half of every scene change was therefore a flat
#   black card the player could sit and look at: roughly a second of nothing,
#   twice as long as any of the motion around it.
#
#   Each transition is now a single one-directional move with NO HOLD, staging
#   both frames at once (see EnterMChoreo in menu_transitions.rpy):
#
#     the outgoing frame  keeps its brightness and loses its FOCUS -- it blurs
#                         and drifts, and never fades at all.
#     the incoming frame  is drawn over it, racking INTO focus as its opacity
#                         crosses on a dead-linear ramp over the FULL duration.
#
#   Linear is the whole trick. An eased opacity curve dwells near both ends, so
#   the last quarter of the outgoing pass and the first quarter of the incoming
#   one are both effectively black. A straight ramp reaches black at exactly one
#   instant -- the junction between the two calls -- so a scene change now reads
#   as one continuous defocus through darkness rather than as a card you wait
#   out.
#
# PACING  (why these numbers and not shorter ones)
#   The first cut of this family was tuned purely against the black card it
#   replaced, and overshot: at 0.44s a scene change was over before the player
#   had finished the last line of the old one. The durations below are that
#   first pass slowed by about 5:3, which is the smallest change that reads as a
#   breath rather than a cut. Remember the doubling when tuning: the numbers
#   here are ONE pass and the call pattern above runs two.
#
# `blur` is a model-renderer property. On a driver without gl2 it is ignored and
# these degrade to a drift-and-crossfade, which still works and still has no
# black hold.
#
# EVERY ONE OF THEM PASSES gate_focus=False, AND MEANS IT
#   The primitive holds focus off both frames while it plays -- that is what
#   stops a hover from provoking a rebuild mid-move, and on a menu it is exactly
#   right, because the screen you are arriving at is not yours until you get
#   there (see section 1a of menu_transitions.rpy). These are not menus. Run one
#   pass at 0.90 and the call pattern doubles it, so gating here would leave the
#   quick menu dead to the pointer for the better part of two seconds in the
#   middle of the prose, which is a worse fault than the one it prevents.
# -----------------------------------------------------------------------------

# The engine's own `dissolve`, shortened from its 0.5 default. This is the one
# the prose reaches for between beats of a scene that is already running.
define dissolve = Dissolve(0.40)

# WHY EVERY RACK TRANSFORM BELOW CARRIES gl_texture_scaling
#   Matsu'Py's `blur` is not a convolution -- it is a WEIGHTED SUM OF MIPMAP
#   LEVELS. renpy/common/_shaders.rpym registers "renpy.blur" as
#
#       for (i = 1..13) gl_FragColor += w(i) * texture2D(tex0, uv, i);
#
#   where the third argument is an LOD bias and w() is a gaussian centred on
#   log2(blur). So the whole effect is built out of fractional mip levels, and
#   what the sampler does BETWEEN two levels decides what a fractional blur
#   radius actually looks like.
#
#   The engine's default minification filter is GL_LINEAR_MIPMAP_NEAREST
#   (renpy/gl2/gl2shader.pyx restores exactly that after every draw): bilinear
#   inside a level, and NEAREST between levels. Every one of those thirteen
#   taps therefore snaps to a whole mip. A held blur just lands on the wrong
#   radius by up to half a level; an ANIMATED one -- which is what all six of
#   these are, ramping 0 -> 20 and back over the length of the move -- crosses
#   mip boundaries as it goes, and each crossing is a visible step in the
#   defocus rather than part of a ramp. That staircase was running on every
#   scene change in the game, twice (see the call pattern above).
#
#   "linear_mipmap_linear" is trilinear: it interpolates BETWEEN levels, which
#   is what the gaussian was written expecting. The rack becomes continuous.
#
#   It costs two glTexParameteri calls per draw and no extra memory -- the mip
#   chain already exists. from_render() defaults `mipmap` to True and calls
#   mipmap_texture() with GL_GENERATE_MIPMAP_HINT/GL_NICEST, so the pyramid is
#   built for these render targets whether or not anything samples it properly.
#
#   The property must sit on the SAME transform as the blur. Transform gl_*
#   properties are attached to the mesh render when one exists
#   (renpy/display/accelerator.pyx: `if self.mr: self.mr.add_property(...)`),
#   and `blur` is what creates that mesh render -- so declaring it here puts
#   trilinear on precisely the pass that runs renpy.blur. On a driver without
#   gl2 it is ignored, exactly like `blur` itself.

# --- the chapter break ------------------------------------------------------
# The longest of the set, for when a scene change is also a change of time or
# place. Deepest defocus, and the only one that pushes in rather than drifting.

transform fx_rack_out_full:
    subpixel True
    gl_texture_scaling "linear_mipmap_linear"
    xalign 0.5
    yalign 0.5
    blur 0.0
    zoom 1.0
    parallel:
        easein_quad 0.90 blur 20.0
    parallel:
        easein_quad 0.90 zoom 1.05

transform fx_rack_in_full:
    subpixel True
    gl_texture_scaling "linear_mipmap_linear"
    xalign 0.5
    yalign 0.5
    blur 20.0
    zoom 1.05
    alpha 0.0
    parallel:
        linear 0.90 alpha 1.0
    parallel:
        easeout_quad 0.90 blur 0.0
    parallel:
        easeout_quad 0.90 zoom 1.0

define dissolve_scene_full = EnterMChoreo(
    0.90, old_at=fx_rack_out_full, new_at=fx_rack_in_full, gate_focus=False)

# "We are already dark" -- the outgoing frame is black, so this only ever reads
# as the arrival. Given a bit longer, because a lone rack-up out of real
# darkness is the one place in the set where haste shows.
transform fx_rack_in_dark:
    subpixel True
    gl_texture_scaling "linear_mipmap_linear"
    xalign 0.5
    yalign 0.5
    blur 22.0
    zoom 1.06
    alpha 0.0
    parallel:
        linear 1.00 alpha 1.0
    parallel:
        easeout_quad 1.00 blur 0.0
    parallel:
        easeout_quad 1.00 zoom 1.0

define dissolve_scene_half = EnterMChoreo(
    1.00, new_at=fx_rack_in_dark, gate_focus=False)

# --- the workhorse ----------------------------------------------------------
# Still a leftward sweep, but the frame travels rather than a hard edge crossing
# it. The zoom is not decoration: it buys enough overscan that the drift never
# exposes the screen edge, which is what a plain xoffset would do.

transform fx_rack_out_wipe:
    subpixel True
    gl_texture_scaling "linear_mipmap_linear"
    xalign 0.5
    yalign 0.5
    blur 0.0
    zoom 1.0
    xoffset 0
    parallel:
        easein_quad 0.75 blur 15.0
    parallel:
        easein_quad 0.75 zoom 1.08 xoffset -40

transform fx_rack_in_wipe:
    subpixel True
    gl_texture_scaling "linear_mipmap_linear"
    xalign 0.5
    yalign 0.5
    blur 15.0
    zoom 1.08
    xoffset 40
    alpha 0.0
    parallel:
        linear 0.75 alpha 1.0
    parallel:
        easeout_quad 0.75 blur 0.0
    parallel:
        easeout_quad 0.75 zoom 1.0 xoffset 0

define wipeleft_scene = EnterMChoreo(
    0.75, old_at=fx_rack_out_wipe, new_at=fx_rack_in_wipe, gate_focus=False)

# --- the gentle one ---------------------------------------------------------
# A beat-to-beat change inside a continuous scene. Meant to read as a breath,
# so it barely defocuses and barely moves.

transform fx_rack_out_soft:
    subpixel True
    gl_texture_scaling "linear_mipmap_linear"
    xalign 0.5
    yalign 0.5
    blur 0.0
    zoom 1.0
    parallel:
        easein_quad 0.55 blur 9.0
    parallel:
        easein_quad 0.55 zoom 1.02

transform fx_rack_in_soft:
    subpixel True
    gl_texture_scaling "linear_mipmap_linear"
    xalign 0.5
    yalign 0.5
    blur 9.0
    zoom 1.02
    alpha 0.0
    parallel:
        linear 0.55 alpha 1.0
    parallel:
        easeout_quad 0.55 blur 0.0
    parallel:
        easeout_quad 0.55 zoom 1.0

define dissolve_scene_soft = EnterMChoreo(
    0.55, old_at=fx_rack_out_soft, new_at=fx_rack_in_soft, gate_focus=False)


# =============================================================================
# 3. SHARED HELPER  --  enter_m_rgba
# =============================================================================
# Not an effect. It lives here because it predates the teardown and three
# unrelated subsystems import it from this file; moving it would be a rename
# across the Arcade panels, the boss-fight FX layer and the PhonePanel toolkit
# for no benefit. init -5 so it is defined before the init -2 shader factories
# that call it.
#
#   value    : "#rgb" / "#rgba" / "#rrggbb" / "#rrggbbaa", or an (r,g,b[,a])
#              tuple already in 0..1 (passed through).
#   alpha    : overrides the parsed alpha when not None.
#   fallback : returned (with `alpha` still applied) if the string is junk.
init -5 python:
    import math
    import random

    def enter_m_rgba(value, alpha=None, fallback=(0.0, 0.0, 0.0, 1.0)):
        if isinstance(value, (tuple, list)) and len(value) >= 3:
            r, g, b = float(value[0]), float(value[1]), float(value[2])
            a = float(value[3]) if len(value) > 3 else 1.0
            return (r, g, b, a if alpha is None else float(alpha))

        s = str(value).strip().lstrip("#")
        if len(s) in (3, 4):
            s = "".join(ch * 2 for ch in s)
        if len(s) == 6:
            s += "ff"

        try:
            r = int(s[0:2], 16) / 255.0
            g = int(s[2:4], 16) / 255.0
            b = int(s[4:6], 16) / 255.0
            a = int(s[6:8], 16) / 255.0
        except Exception:
            r, g, b, a = fallback

        return (r, g, b, a if alpha is None else float(alpha))


# =============================================================================
# 4. OUT-OF-CONTEXT SCENE SUPPORT  --  the last six motion pieces
# =============================================================================
# The ONLY survivors of the motion library, kept because two authored
# out-of-context scenes still call them:
#     ooc_1030_uhoh.rpy       fx_push, fx_lean_in, fx_flinch, fx_punch_soft,
#                             fx_thud, fx_shake_screen
#     ooc_0604_out_of_ten.rpy fx_lean_in
# They are NOT a library and must not be treated as the start of one -- the
# rebuild gets its own file. If those two scenes are ever re-staged, this whole
# section goes with them.
#
# Note that fx_lean_in and fx_flinch are subject to the replay behaviour
# described in the header: both scenes leave them on a sprite that then keeps
# talking. They have always done that, and it reads as a held lean / a repeated
# twitch rather than as a bug, which is why those scenes were left alone.

# --- one-shot screen punches (TRANSITIONS -- use with `with`) ----------------
# Same construction as vanilla hpunch/vpunch. Horizontal = punch (a hit, a
# shout). Vertical = thud (weight landing, a chair going over).
define fx_punch_soft = Move((6, 0), (-6, 0), .07, bounce=True, repeat=True, delay=.14)
define fx_thud = Move((0, 13), (0, -13), .085, bounce=True, repeat=True, delay=.22)

# --- sprite modifiers -------------------------------------------------------
# These go FIRST in an at_list so they stay INNERMOST; placement is decided by
# the outermost transform, and if a modifier ends up outer, take_state copies
# the pose's zoom onto it and the sprite shrinks.
#     show matsuda uniform neut at fx_lean_in, i42

# The standard recoil: struck, or spoken to like that.
transform fx_flinch(reach=7.0):
    subpixel True
    linear 0.05 xoffset (-reach)
    linear 0.06 xoffset (reach * 0.7)
    linear 0.07 xoffset (-reach * 0.28)
    linear 0.05 xoffset 0

# Leaning in. Relative zoom, so it composes with any pose.
transform fx_lean_in(z=1.05, secs=0.5):
    subpixel True
    zoom 1.0
    easeout_quad (secs) zoom (z) yoffset 4

# --- the slow closing-in, for a BACKGROUND ----------------------------------
# Long on purpose. A five-minute push is invisible frame to frame; what the
# player notices is that the room feels smaller than it did when the scene
# started, and they cannot say why.
transform fx_push(z=1.07, secs=60.0):
    subpixel True
    align (0.5, 0.5)
    zoom 1.0
    easein_quad (secs) zoom (z)

# --- the decaying screen shake ----------------------------------------------
# WHY THIS TAKES A `start` AND DOES NOT TRUST `st`
#   A transform in a LAYER at-list (which is what fx_shake_screen installs) is
#   REBUILT FROM SCRATCH on every interaction: renpy/display/core.py
#   transform_layer does `rv = a(child=rv)` per interaction, and the handoff
#   that follows copies position and the hide/replace flags but NOT `st`. So on
#   a layer, `st` restarts at 0.0 every time the player clicks, and any driver
#   that reads `st` replays itself once per line forever. Measuring against a
#   wall clock captured when the shake STARTED is what makes it fire once.
#   get_time() rather than time.time() because it honours Matsu'Py's time warp.
init -5 python:
    _FX_LAYER = "master"

    def _fx_elapsed(start, st):
        """Seconds since the effect began, safe on a layer at-list."""
        if start is None:
            return st
        return renpy.display.core.get_time() - start

    def _fx_shake_decay(amp, secs, curve, over, start, trans, st, at):
        """One-shot shake that dies out. The whole point is the DECAY: a
        constant-amplitude shake reads as a broken monitor, while one that
        falls off reads as an impact that the room absorbs.

        The overscan decays with the shake instead of being pinned by the ATL,
        so the effect leaves NOTHING behind. Holding `zoom over` after the
        offsets had settled used to strand the whole layer 6% zoomed in until
        the next `scene` -- an invisible bug, because a still frame that is
        quietly cropped looks like art direction."""
        elapsed = _fx_elapsed(start, st)

        if secs <= 0.0 or elapsed >= secs:
            trans.xoffset = 0
            trans.yoffset = 0
            trans.zoom = 1.0
            return None

        falloff = (1.0 - (elapsed / secs)) ** curve
        reach = amp * falloff
        trans.xoffset = random.uniform(-reach, reach)
        trans.yoffset = random.uniform(-reach, reach)
        trans.zoom = 1.0 + (over - 1.0) * falloff
        return 0.0

    def fx_shake_screen(amp=16.0, secs=0.9, over=1.06, curve=2.0,
                        layer=_FX_LAYER, snd=None):
        """One-shot decaying shake on `layer`. Does NOT block: the shake runs
        underneath whatever comes next.

        Because it rides the master layer, the background and sprites convulse
        while the textbox, menus and buttons stay still and clickable. It
        settles to zero offset AND zoom 1.0 on its own, and the transform is
        dropped by the next `scene`."""
        if snd is not None:
            renpy.sound.play(snd)
        _fx_start = renpy.display.core.get_time()
        renpy.show_layer_at(
            [fx_shake_decay(
                float(amp), float(secs), float(over), float(curve), _fx_start)],
            layer=layer, reset=True)

# `start` is a get_time() stamp and is what makes this fire ONCE on a layer.
# There is deliberately no `zoom over` here: the driver owns zoom so the
# overscan can decay out with the shake instead of being stranded on the layer.
transform fx_shake_decay(amp=16.0, secs=0.9, over=1.06, curve=2.0, start=None):
    subpixel True
    align (0.5, 0.5)
    function renpy.curry(_fx_shake_decay)(amp, secs, curve, over, start)
