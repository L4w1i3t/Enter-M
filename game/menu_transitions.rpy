# Menu transitions and destination dispatch. Story transitions live in
# fx.rpy; options.rpy owns dialogue-window fades.
# EnterMChoreo composes outgoing/incoming frames and optional overlay plates.
# Overlay transforms are instantiated per move so each gets a fresh ATL clock.
# Focus is gated until arrival and dispatch choices stay latched through
# interaction rebuilds. The Scene Transitions preference disables transitions.
#
# Frames are blitted with focus=False during gated moves: blocking click events
# alone does not stop hovered actions from rebuilding a transition. A single
# restart at arrival restores pointer focus. See enter_m_move_is_new().

init offset = -5


# =============================================================================
# 1a. THE MOVE IS NOT THE PLAYER'S UNTIL IT LANDS
# =============================================================================
# WHAT WENT WRONG, BECAUSE IT IS NOT OBVIOUS FROM ANYTHING ELSE IN THIS FILE
#   Point at a card on the menu you are arriving at while the move is still
#   playing and the whole thing judders -- frames drop, and the menu you just
#   left flickers back over the one you asked for until the move finally ends.
#
#   The cause is two engine facts meeting:
#
#   1. A TRANSITION IS REBUILT FROM SCRATCH EVERY TIME THE INTERACTION
#      RESTARTS. Matsu'Py does not hold on to the object it is drawing: it keeps
#      the *recipe* and calls it again for a brand-new instance on every pass of
#      `interact_core` (`instantiate_transition`, core.py). A restart therefore
#      costs a full scene recompute, an image-prediction pass over both menus
#      and a `per_interact` walk of the lot -- mid-move, at 60Hz, over two of
#      the heaviest screens in the game.
#
#   2. HOVER IS NOT AN EVENT, SO `Transition.events` DOES NOT STOP IT. The
#      engine already refuses to hand CLICKS to a screen that has not landed
#      yet -- that is what `self.events = False` in the primitive below buys.
#      But focus is not dispatched through the displayable tree at all: it is
#      resolved off the RENDER tree by `focus.mouse_handler`, which calls
#      `Button.focus()` directly, which runs the button's `hovered` action. The
#      main menu's rail is `hovered SetScreenVariable("mm_sel", ...)`, and
#      SetScreenVariable ends in `renpy.restart_interaction()`.
#
#   So sweeping the pointer across the rail during a move fires a rebuild per
#   card, and each rebuild re-asks the dispatchers in section 5 what the move
#   should even BE -- against facts that have moved on. `EnterMMenuHome` was the
#   worst of them: it picks its choreography from whether a music handoff is
#   still in flight, that stops being true a third of the way in, and the move
#   swapped from the 0.62s cut to the 0.42s cycle halfway through itself.
#
# THE TWO RULES THAT COME OUT OF IT
#   * NOTHING UNDER A MOVE TAKES FOCUS. The frames are blitted with
#     `focus=False`, which is the switch `take_focuses` reads when it walks the
#     render tree -- so the pointer finds nothing to light up and nothing to
#     run, and no rebuild is provoked in the first place. Clicks were already
#     blocked, so this only makes the picture honest about it. When the move
#     lands we ask for ONE restart, so that a pointer already parked over a
#     button picks its hover up without having to be jiggled.
#   * A DISPATCHER DECIDES ONCE PER MOVE, NOT ONCE PER BUILD. Rebuilds can
#     still be provoked by things this file does not own (a toast, a timer), so
#     anything sampled from the world -- the music handoff, the destination
#     screen, the Arcade's interference plate -- is latched on the first build
#     and held for the rest of the move.

init python:

    def enter_m_move_is_new():
        """
        True on the FIRST build of a transition, False on every rebuild of one
        already in flight.

        `transition_time[None]` is the tell: the engine sets it to None when a
        transition is handed over and fills it in with the move's start time on
        the first frame it draws. So it is None exactly once per move.
        """

        interface = renpy.game.interface

        if interface is None:
            return True

        return interface.transition_time.get(None, None) is None

    class EnterMFocusGate(renpy.object.Object):
        """
        Mixin. Holds focus off both frames for the length of the move, then
        asks for one interaction restart on the frame it lands.

        The restart cannot loop: it is only ever asked for by an instance that
        actually DREW part of the move, and the instance the restart builds
        starts life already landed.

        THE BASE CLASS IS LOAD-BEARING. `object` inside a .rpy python block is
        store.object, which is RevertableObject -- and a mixin built on that
        lands BETWEEN this class and Transition in the MRO, so the primitive's
        `super().__init__(delay, ...)` reaches RevertableObject.__init__ and
        dies with "object() takes no parameters". `renpy.object.Object` is
        already Displayable's own base, so C3 defers it to the END of the MRO
        and `super()` finds the transition constructor it was aiming at.
        """

        # Does this transition gate at all? The story moves in fx.rpy are built
        # on the same primitive and can opt out with gate_focus=False.
        gate_focus = True

        # Has this instance drawn a frame of the move itself, as opposed to
        # having been built after the move had already finished?
        gate_moved = False

        gate_landed = False

        def gate_blit(self, surf, width, height):
            """
            Wrap a finished frame of the move so that nothing inside it can be
            focused, hovered or clicked.
            """

            rv = renpy.display.render.Render(width, height)

            if self.gate_focus:
                self.gate_moved = True
                rv.blit(surf, (0, 0), focus=False)
            else:
                rv.blit(surf, (0, 0))

            return rv

        def gate_land(self):
            """
            Called on the first frame after the move is over. Hands the screen
            back by restarting the interaction, which is what makes the engine
            re-resolve focus against the pointer where it is now.
            """

            if self.gate_moved and not self.gate_landed:
                self.gate_landed = True
                renpy.restart_interaction()


# =============================================================================
# 1. THE PRIMITIVE
# =============================================================================

init python:

    class EnterMChoreoTransition(EnterMFocusGate, renpy.display.transition.Transition):
        """
        A transition that CHOREOGRAPHS the two frames instead of blending them.

        `delay`
            How long the whole move takes. When it elapses the incoming frame
            takes over verbatim, so every ATL below should finish by then.
        `old_at` / `new_at`
            The transform each frame is played through. Either may be None to
            leave that frame alone.
        `under`
            A displayable drawn behind both frames -- normally the void colour,
            so that a frame which fades or shrinks reveals something deliberate.
        `over`
            A list of (displayable, transform) pairs drawn over both frames:
            flash bars, sweep seams, curtains.
        `old_on_top`
            Which frame gets drawn last. The default (False) is the normal
            crossfade stacking -- the incoming frame lies over the outgoing one
            and carries the opacity ramp. Set it when the OUTGOING frame is the
            one doing the acting: a menu collapsing out of the way is invisible
            underneath a screen that is already opaque.
        `gate_focus`
            Whether the move holds focus off both frames until it lands
            (section 1a). The only reason to turn this off is a move the player
            is meant to be able to point through while it plays.
        """

        def __init__(
            self, delay, old_at=None, new_at=None, under=None, over=None,
            old_on_top=False, gate_focus=True, old_widget=None, new_widget=None,
            **properties
        ):

            super(EnterMChoreoTransition, self).__init__(delay, **properties)
            self.old_on_top = old_on_top
            self.gate_focus = gate_focus

            self.old_widget = old_widget
            self.new_widget = new_widget

            # Clicks belong to the incoming screen only once it has landed.
            # Hover is held off separately, by the gate -- section 1a.
            self.events = False

            self.stage = self.build_stage(under, old_at, new_at, over)

        def build_stage(self, under, old_at, new_at, over):
            """
            Assemble the layered scene the transition actually draws, or None
            if we were handed no frames to work with (which happens while
            Matsu'Py is predicting).
            """

            if (self.old_widget is None) or (self.new_widget is None):
                return None

            stage = renpy.display.layout.Fixed()

            if under is not None:
                stage.add(under)

            old = old_at(self.old_widget) if old_at else self.old_widget
            new = new_at(self.new_widget) if new_at else self.new_widget

            for frame in ((new, old) if self.old_on_top else (old, new)):
                stage.add(frame)

            for plate, plate_at in (over or []):
                stage.add(plate_at(plate) if plate_at else plate)

            return stage

        def visit(self):
            staged = (self.stage, self.old_widget, self.new_widget)
            return [d for d in staged if d is not None]

        def render(self, width, height, st, at):

            # Nothing to stage, or the player is on reduced motion: just cut.
            if (self.stage is None) or renpy.game.less_updates:
                return renpy.display.transition.null_render(self, width, height, st, at)

            if st >= self.delay:
                self.events = True
                self.gate_land()
                return renpy.display.render.render(self.new_widget, width, height, st, at)

            staged = renpy.display.render.render(self.stage, width, height, st, at)

            rv = self.gate_blit(staged, width, height)

            renpy.display.render.redraw(self, 0)

            return rv

    # Curried the same way the engine curries Dissolve/ImageDissolve/... so that
    # `EnterMChoreo(0.4, ...)` is a reusable recipe and the engine can finish it
    # off with old_widget/new_widget at the moment the transition actually runs.
    EnterMChoreo = renpy.curry(EnterMChoreoTransition)


# =============================================================================
# 2. SHARED PARTS
# =============================================================================

# The colour behind every menu move. Same deep blue-black the story transitions
# hold on, so a menu opening over a scene does not flash a different black.
define enter_m_menu_void = Solid("#02050a")

# --- overlay plates ---------------------------------------------------------

# The hot line that fires across the tube as a picture collapses or opens.
transform enter_m_ch_hotline:
    subpixel True
    additive 1.0
    xysize (1280, 3)
    xalign 0.5
    yalign 0.5
    alpha 1.0
    parallel:
        easeout 0.28 yzoom 30.0
    parallel:
        linear 0.04 alpha 0.9
        easeout 0.24 alpha 0.0

# The same idea on the way out: bright at the moment of collapse, gone fast.
transform enter_m_ch_hotline_short:
    subpixel True
    additive 1.0
    xysize (1280, 3)
    xalign 0.5
    yalign 0.5
    alpha 0.0
    pause 0.13
    alpha 1.0
    parallel:
        easeout 0.15 yzoom 18.0
    parallel:
        linear 0.03 alpha 0.85
        easeout 0.12 alpha 0.0

# Twin seams that chase the sliding frames across, cyan first then red.
transform enter_m_ch_seam_lead:
    subpixel True
    additive 1.0
    xysize (3, 720)
    xpos 1292
    ypos 0
    alpha 0.0
    linear 0.03 alpha 1.0
    easeout 0.23 xpos -16
    linear 0.04 alpha 0.0

transform enter_m_ch_seam_trail:
    subpixel True
    additive 1.0
    xysize (2, 720)
    xpos 1316
    ypos 0
    alpha 0.0
    pause 0.04
    linear 0.03 alpha 0.75
    easeout 0.20 xpos -44
    linear 0.03 alpha 0.0

# Stage curtains, for the one screen that deserves them.
transform enter_m_ch_curtain_left:
    subpixel True
    xysize (652, 720)
    xanchor 1.0
    xpos 0
    ypos 0
    easeout_quad 0.20 xpos 652
    pause 0.03
    easein_quad 0.20 xpos 0

transform enter_m_ch_curtain_right:
    subpixel True
    xysize (652, 720)
    xanchor 0.0
    xpos 1280
    ypos 0
    easeout_quad 0.20 xpos 628
    pause 0.03
    easein_quad 0.20 xpos 1280

transform enter_m_ch_curtain_edge_left:
    subpixel True
    xysize (3, 720)
    xanchor 1.0
    xpos 0
    ypos 0
    easeout_quad 0.20 xpos 652
    pause 0.03
    easein_quad 0.20 xpos 0

transform enter_m_ch_curtain_edge_right:
    subpixel True
    xysize (3, 720)
    xanchor 0.0
    xpos 1280
    ypos 0
    easeout_quad 0.20 xpos 628
    pause 0.03
    easein_quad 0.20 xpos 1280

# The plate the Arcade tears through: void, rolling grain, and two bands of
# signal skidding up and down it. It only ever shows for a tenth of a second,
# which is exactly why it can afford to be this loud.
#
# The two bands are declared as TRANSFORMS rather than baked into an `image`,
# for the same reason the overlay plates up the page are passed as pairs: an
# `image` block is ONE displayable that lives for the whole run, and its ATL
# keeps running between uses. `renpy.easy.displayable()` -- which is how
# MultipleTransition resolves an image name -- hands back that one shared
# instance rather than a copy, so the first channel change played the loop from
# the top and every one after it picked the bands up wherever the previous
# change had abandoned them. See enter_m_menu_glitch for where they get built.
transform enter_m_ch_glitch_band_cyan:
    subpixel True
    additive 1.0
    xysize (1280, 24)
    ypos 188
    alpha 0.26
    block:
        linear 0.06 ypos 428 alpha 0.10
        linear 0.05 ypos 96 alpha 0.30
        repeat

transform enter_m_ch_glitch_band_red:
    subpixel True
    additive 1.0
    xysize (1280, 10)
    ypos 470
    alpha 0.34
    block:
        linear 0.07 ypos 246 alpha 0.14
        linear 0.05 ypos 566 alpha 0.38
        repeat


# =============================================================================
# 3. THE CHOREOGRAPHIES
# =============================================================================

# THE ONE RULE EVERY CHOREOGRAPHY BELOW OBEYS
#   ONLY THE TOP FRAME CARRIES OPACITY.
#
#   A black flash is not a colour anyone chose. It is the void showing through
#   two frames that were each on their way somewhere, and it is what you get
#   the moment BOTH of them are partly transparent -- fade one out to 0.5 under
#   another that has only reached 0.5 and the screen is a quarter dark in the
#   middle of the move, which is exactly the dip that reads as a flicker.
#
#   So each move picks one frame to act with:
#     the one underneath stays FULLY OPAQUE for the whole move and only ever
#     drifts, zooms or blurs, and
#     the one on top crosses over it, or shrinks off it.
#   Nothing fades out on its own timetable. Where the OUTGOING frame is the
#   actor -- a menu snapping shut over a scene that is already whole -- it is
#   raised with old_on_top instead of the incoming one being faded up.

# --- opening a menu: the tube powers on ------------------------------------
# The screen we came from stays lit and just falls back; the one we asked for
# arrives over it as a hairline that snaps out to full width and then opens.
# Because the incoming frame is opaque from its first frame, the hairline is
# already covering something rather than revealing a hole.

transform enter_m_ch_recede:
    subpixel True
    xalign 0.5
    yalign 0.5
    easein_quad 0.34 zoom 1.05

transform enter_m_ch_crt_on:
    subpixel True
    xalign 0.5
    yalign 0.5
    xzoom 0.36
    yzoom 0.012
    easeout_quad 0.08 xzoom 1.0
    easeout_cubic 0.26 yzoom 1.0

# --- closing a menu: the tube powers off -----------------------------------
# Drawn old-on-top: the scene underneath is already whole, and the menu snaps
# shut over it. This is the one move where the OUTGOING frame is the actor.

transform enter_m_ch_crt_off:
    subpixel True
    xalign 0.5
    yalign 0.5
    easein_quad 0.16 yzoom 0.014
    parallel:
        easein_quad 0.08 xzoom 0.0
    parallel:
        linear 0.08 alpha 0.0

transform enter_m_ch_hold_still:
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.02
    easeout_cubic 0.26 zoom 1.0

# --- page to page: the rack slides -----------------------------------------
# Used inside the pause menu, where the chrome does not change and only the
# content panel does. The two opacity ramps are exact complements, so the pair
# always sums to a full picture.

transform enter_m_ch_rack_out:
    subpixel True
    xalign 0.5
    yalign 0.5
    easein_quad 0.30 xoffset -110 zoom 1.04

transform enter_m_ch_rack_in:
    subpixel True
    xalign 0.5
    yalign 0.5
    alpha 0.0
    xoffset 130
    parallel:
        easeout_cubic 0.30 xoffset 0
    parallel:
        linear 0.30 alpha 1.0

# --- back to the main terminal: a power cycle ------------------------------
# The biggest gesture in the set, and the one that used to be worst: the old
# version collapsed the outgoing screen to a hairline and then parked on black
# for a third of a second before the terminal came back. Now the terminal opens
# OVER the retreating screen, so the frame is covered end to end -- and it is a
# third shorter besides. The flash is what sells the cycle, not the darkness.

transform enter_m_ch_cycle_down:
    subpixel True
    xalign 0.5
    yalign 0.5
    easein_quad 0.42 zoom 1.09

transform enter_m_ch_cycle_up:
    subpixel True
    xalign 0.5
    yalign 0.5
    xzoom 0.22
    yzoom 0.008
    pause 0.12
    easeout_quad 0.10 xzoom 1.0
    easeout_cubic 0.20 yzoom 1.0

transform enter_m_ch_cycle_line:
    subpixel True
    additive 1.0
    xysize (1280, 3)
    xalign 0.5
    yalign 0.5
    alpha 0.0
    pause 0.14
    linear 0.04 alpha 1.0
    parallel:
        easeout 0.24 yzoom 30.0
    parallel:
        easeout 0.22 alpha 0.0

# --- CUTTING THROUGH BLACK: the moves that carry a music handoff -----------
#
# THE ONE PLACE THE "NO BLACK" RULE IS DELIBERATELY BROKEN, AND WHY.
#   Everything above works to keep the frame covered end to end, because a menu
#   move that parks on black reads as a load. These three do the opposite on
#   purpose: the Archive, the Arcade, and the way back off either of them are
#   the only moves in the game that also hand the MUSIC over, and sound cannot
#   be cross-faded into place the way a picture can. Something has to give, and
#   a deliberate beat of black reads as an edit; a track that arrives late over
#   a settled menu reads as a fault.
#
#   So these moves are cut in three: the old screen leaves, the frame holds on
#   the void while the outgoing track fades all the way out, and the new screen
#   arrives at the same instant the new track does -- at full volume, no fade
#   in, because it is starting on a cut rather than sliding under something.
#
# THE CONTRACT
#   ENTER_M_MENU_REVEAL (section 6) is the moment the incoming screen appears,
#   and it is the SAME number the music handoff uses as its fade-out length --
#   `renpy.music.play(fadeout=X)` starts the queued track exactly X seconds
#   later (measured: 0.337s for X=0.34). Every `pause` below is that constant.
#   Change it in one place and you must change it in the other, or the picture
#   and the sound stop landing together.
#
#   Any decoder cold-start therefore happens during the black hold, where there
#   is nothing on screen to stutter -- which is the other half of why this
#   works at all.

# The Archive's drawer, cut. Out and gone by 0.20, back from 0.34.
transform enter_m_ch_cut_drawer_out:
    subpixel True
    xalign 0.5
    yalign 0.5
    parallel:
        easein_quad 0.20 zoom 1.05 yoffset -30
    parallel:
        linear 0.13 alpha 1.0
        easein_quad 0.07 alpha 0.0

transform enter_m_ch_cut_drawer_in:
    subpixel True
    xalign 0.5
    yalign 0.5
    alpha 0.0
    yoffset 44
    pause 0.34
    parallel:
        easeout_cubic 0.28 yoffset 0
    parallel:
        linear 0.06 alpha 1.0

transform enter_m_ch_cut_drawer_edge:
    subpixel True
    additive 1.0
    xysize (1280, 2)
    xalign 0.5
    yalign 0.5
    yoffset 44
    alpha 0.0
    pause 0.34
    linear 0.04 alpha 0.9
    parallel:
        easeout_cubic 0.26 yoffset 0
    parallel:
        pause 0.10
        linear 0.16 alpha 0.0

# The power cycle, cut. The tube genuinely goes dark before it comes back,
# which is what this gesture always wanted to be -- the old version had to fake
# it by opening the terminal over the retreating screen to avoid the black.
transform enter_m_ch_cut_cycle_down:
    subpixel True
    xalign 0.5
    yalign 0.5
    parallel:
        easein_quad 0.20 zoom 1.07
    parallel:
        linear 0.13 alpha 1.0
        easein_quad 0.07 alpha 0.0

transform enter_m_ch_cut_cycle_up:
    subpixel True
    xalign 0.5
    yalign 0.5
    alpha 0.0
    xzoom 0.22
    yzoom 0.008
    pause 0.34
    alpha 1.0
    parallel:
        easeout_quad 0.10 xzoom 1.0
    parallel:
        easeout_cubic 0.28 yzoom 1.0

transform enter_m_ch_cut_cycle_line:
    subpixel True
    additive 1.0
    xysize (1280, 3)
    xalign 0.5
    yalign 0.5
    alpha 0.0
    pause 0.34
    linear 0.03 alpha 1.0
    parallel:
        easeout 0.26 yzoom 30.0
    parallel:
        easeout 0.24 alpha 0.0

# --- the curtain: for the Credits ------------------------------------------
# The only move in the set that is ALLOWED to cover the screen, because a
# curtain that does not is not a curtain. The swap happens behind it.

transform enter_m_ch_behind_curtain_out:
    subpixel True
    xalign 0.5
    yalign 0.5
    pause 0.23
    alpha 0.0

transform enter_m_ch_behind_curtain_in:
    subpixel True
    xalign 0.5
    yalign 0.5
    alpha 0.0
    pause 0.23
    alpha 1.0


# =============================================================================
# 4. THE TRANSITIONS
# =============================================================================

# Gameplay -> pause menu, and main menu -> any sub-screen. The default for
# anything that does not ask for a flavour of its own.
define enter_m_menu_open = EnterMChoreo(
    0.34,
    old_at=enter_m_ch_recede,
    new_at=enter_m_ch_crt_on,
    under=enter_m_menu_void,
    over=[(Solid("#bdf6ff"), enter_m_ch_hotline)])

# Pause menu -> back into the scene. The scene is whole underneath from the
# first frame; the menu snaps shut on top of it.
define enter_m_menu_close = EnterMChoreo(
    0.28,
    old_at=enter_m_ch_crt_off,
    new_at=enter_m_ch_hold_still,
    under=enter_m_menu_void,
    over=[(Solid("#bdf6ff"), enter_m_ch_hotline_short)],
    old_on_top=True)

# One menu page to the next.
define ENTER_M_SEAM_PLATES = [
    (Solid("#bdf6ff"), enter_m_ch_seam_lead),
    (Solid("#ff315b"), enter_m_ch_seam_trail),
]

define enter_m_menu_swap = EnterMChoreo(
    0.30,
    old_at=enter_m_ch_rack_out,
    new_at=enter_m_ch_rack_in,
    under=enter_m_menu_void,
    over=ENTER_M_SEAM_PLATES)

# Anywhere -> the main terminal, when the music is NOT changing (Credits,
# Settings, Save, Load). Stays covered end to end; no black, no waiting.
define enter_m_menu_home = EnterMChoreo(
    0.42,
    old_at=enter_m_ch_cycle_down,
    new_at=enter_m_ch_cycle_up,
    under=enter_m_menu_void,
    over=[(Solid("#bdf6ff"), enter_m_ch_cycle_line)])

# ...and when it IS changing (off the Archive or the Arcade): cut through black
# so the outgoing track has somewhere to fade. Picked per use, see section 5.
define enter_m_menu_home_cut = EnterMChoreo(
    0.62,
    old_at=enter_m_ch_cut_cycle_down,
    new_at=enter_m_ch_cut_cycle_up,
    under=enter_m_menu_void,
    over=[(Solid("#bdf6ff"), enter_m_ch_cut_cycle_line)])

# Main menu -> Archive. Always cuts through black: the Archive always brings
# its own track.
define enter_m_menu_shutter = EnterMChoreo(
    0.62,
    old_at=enter_m_ch_cut_drawer_out,
    new_at=enter_m_ch_cut_drawer_in,
    under=enter_m_menu_void,
    over=[(Solid("#bdf6ff"), enter_m_ch_cut_drawer_edge)])

# Main menu -> Arcade. Cabinet hardware, so it changes channel like cabinet
# hardware: the picture is decimated into blocks, takes a hit of static, and is
# rebuilt on the other side. The plate is deliberately NOT dark -- a black hold
# here would read as a hitch, a bright one reads as interference.
#
# Built per CHANGE rather than `define`d once, so the interference plate is a
# new displayable on every channel change and its bands always roll from the top
# of their loop. The same plate object is reused for both halves of the move,
# which is deliberate: within ONE change the bands should keep rolling across
# the Pause rather than restarting midway -- and for the same reason it is
# latched (section 1a) rather than rebuilt, or a rebuild provoked halfway
# through would snap the bands back to the top of their loop.
init python:

    class EnterMGatedMultipleTransition(
        EnterMFocusGate, renpy.display.transition.MultipleTransition
    ):
        """
        MultipleTransition wearing the same focus gate the choreographies have.
        The channel change is assembled out of stock engine parts, and stock
        parts hand focus straight through to whatever they are drawing.
        """

        def render(self, width, height, st, at):

            surf = renpy.display.transition.MultipleTransition.render(
                self, width, height, st, at)

            # Reduced motion draws the incoming frame verbatim, so there is no
            # move to hold anything off.
            if renpy.game.less_updates:
                return surf

            if st >= self.delay:
                self.gate_land()
                return surf

            return self.gate_blit(surf, surf.width, surf.height)

    EnterMGatedMultiple = renpy.curry(EnterMGatedMultipleTransition)

    class EnterMChannelChange(renpy.object.Object):
        """
        The Arcade's channel change. A transition in its own right, not a
        recipe -- Matsu'Py calls it with the two frames and it assembles the
        whole MultipleTransition on the spot.
        """

        plate = None

        def build_plate(self):
            return Fixed(
                Solid("#14242f"),
                Transform("noise", alpha=0.55),
                At(Solid("#56d7ff"), enter_m_ch_glitch_band_cyan),
                At(Solid("#ff315b"), enter_m_ch_glitch_band_red),
            )

        def __call__(self, old_widget=None, new_widget=None):

            if enter_m_move_is_new() or (self.plate is None):
                self.plate = self.build_plate()

            plate = self.plate

            # Beats: decimate to interference (0.10), hold it (0.04), let the
            # interference burn down to the void (0.04), then rebuild the
            # picture out of the void (0.32). The dead channel is the Arcade's
            # version of the black beat every music-carrying move gets; it just
            # gets to be loud on the way in.
            #
            # There is NO separate black pause, and adding one is the mistake to
            # avoid: Pixellate splits its time in half (`quantum = time / (2 *
            # steps)`), pixellating the OLD out before the new comes in -- and a
            # pixellated void is still just black. So the first half of that
            # last 0.32 IS the black hold, and the picture starts rebuilding at
            # 0.18 + 0.16 = 0.34, which is ENTER_M_MENU_REVEAL. Putting a Pause
            # in front of it as well made the picture arrive a tenth of a second
            # after the music -- the whole thing this file exists to prevent.
            return EnterMGatedMultiple([
                False, Pixellate(0.10, 4),
                plate, Pause(0.04),
                plate, Dissolve(0.04),
                enter_m_menu_void, Pixellate(0.32, 4),
                True,
            ])(old_widget=old_widget, new_widget=new_widget)

define enter_m_menu_glitch = EnterMChannelChange()

# Main menu -> Credits. Matsuda would not let a curtain call happen without a
# curtain. The choreography remains theatrical, but its cloth and edge colours
# now belong to the domestic menu family instead of the retired cyan terminal.
define ENTER_M_CURTAIN_PLATES = [
    (Solid("#10191e"), enter_m_ch_curtain_left),
    (Solid("#10191e"), enter_m_ch_curtain_right),
    (Solid("#d87b6d"), enter_m_ch_curtain_edge_left),
    (Solid("#70bbb3"), enter_m_ch_curtain_edge_right),
]

define enter_m_menu_curtain = EnterMChoreo(
    0.43,
    old_at=enter_m_ch_behind_curtain_out,
    new_at=enter_m_ch_behind_curtain_in,
    under=enter_m_menu_void,
    over=ENTER_M_CURTAIN_PLATES)

# Settings and Records do not power up like hardware. Their short dissolve is
# quiet enough to feel continuous with the bedroom while still giving Ren'Py a
# clean interaction boundary. Credits keeps the character-specific curtain.
define enter_m_menu_room = Dissolve(0.30)

define ENTER_M_MENU_ROOM_SCREENS = (
    "preferences",
    "data_bank",
    "save",
    "load",
    "credits_menu",
    "history",
    "calendar_menu",
    "about",
)


# =============================================================================
# 5. WIRING
# =============================================================================
# Which screen gets which flavour. The dispatcher below reads the screen name
# out of the store rather than taking it as an argument, which is what makes
# the flavours work from the MAIN MENU at all: ShowMenu only honours its
# `_transition` argument when it is already inside the game menu, and from the
# title screen it is not -- it goes off to `_game_menu` instead, which is
# hardwired to config.enter_transition. But `_game_menu` is a label whose
# `_game_menu_screen` parameter lands in the global store before it calls
# `_enter_game_menu`, so by the time our transition is asked for a displayable,
# the destination is sitting right there.
#
# Adding a flavour to a new screen is one line in this table and nothing else.

define ENTER_M_MENU_FLAVOUR = {
    "archive": enter_m_menu_shutter,
    "arcade_hub": enter_m_menu_glitch,
    "credits_menu": enter_m_menu_curtain,
    "preferences": enter_m_menu_room,
    "data_bank": enter_m_menu_room,
    "save": enter_m_menu_room,
    "load": enter_m_menu_room,
    "history": enter_m_menu_room,
    "calendar_menu": enter_m_menu_room,
    "about": enter_m_menu_room,
}

init python:

    class EnterMMenuEnter(renpy.object.Object):
        """
        config.enter_transition. Picks the flavour that matches the screen we
        are on our way to, and falls back to the plain terminal boot.

        Decided once per move and then held -- see section 1a.
        """

        flavour = None

        def __call__(self, old_widget=None, new_widget=None):

            if enter_m_move_is_new() or (self.flavour is None):
                destination = getattr(store, "_game_menu_screen", None)
                self.flavour = ENTER_M_MENU_FLAVOUR.get(destination, enter_m_menu_open)

            return self.flavour(old_widget=old_widget, new_widget=new_widget)

    class EnterMMenuHome(renpy.object.Object):
        """
        config.game_main_transition. The way back to the title, choosing the
        quiet room dissolve, the legacy covered cycle, or the longer cut that
        gives a music handoff somewhere to happen.

        A music handoff still takes precedence. Otherwise the source screen
        selects the domestic dissolve or the legacy cycle. The ordering works
        because the screens ask for `canyoufeel` in the SAME action list as
        Return(), and the action list runs before `_return` reaches
        renpy.transition().

        THE LATCH IS NOT OPTIONAL HERE. A handoff stops being "in flight" one
        ENTER_M_MENU_REVEAL in, which is barely half of the cut move -- so
        without it, a rebuild provoked partway through this move (section 1a)
        answered the question a second time, got the other answer, and swapped
        the 0.62s cut for the 0.42s cycle mid-flight.
        """

        flavour = None

        def __call__(self, old_widget=None, new_widget=None):

            if enter_m_move_is_new() or (self.flavour is None):
                if enter_m_menu_music_is_switching():
                    self.flavour = enter_m_menu_home_cut
                elif getattr(store, "_game_menu_screen", None) in ENTER_M_MENU_ROOM_SCREENS:
                    self.flavour = enter_m_menu_room
                else:
                    self.flavour = enter_m_menu_home

            return self.flavour(old_widget=old_widget, new_widget=new_widget)

    class EnterMMenuExit(renpy.object.Object):
        """Leave room-family pause screens without replaying the CRT collapse."""

        flavour = None

        def __call__(self, old_widget=None, new_widget=None):

            if enter_m_move_is_new() or (self.flavour is None):
                if getattr(store, "_game_menu_screen", None) in ENTER_M_MENU_ROOM_SCREENS:
                    self.flavour = enter_m_menu_room
                else:
                    self.flavour = enter_m_menu_close

            return self.flavour(old_widget=old_widget, new_widget=new_widget)

    class EnterMMenuIntra(renpy.object.Object):
        """Use the quiet move only when the destination belongs to this family."""

        flavour = None

        def __call__(self, old_widget=None, new_widget=None):

            if enter_m_move_is_new() or (self.flavour is None):
                destination = getattr(store, "_game_menu_screen", None)
                if destination == "credits_menu":
                    self.flavour = enter_m_menu_curtain
                elif destination in ENTER_M_MENU_ROOM_SCREENS:
                    self.flavour = enter_m_menu_room
                else:
                    self.flavour = enter_m_menu_swap

            return self.flavour(old_widget=old_widget, new_widget=new_widget)

define config.enter_transition = EnterMMenuEnter()
define config.exit_transition = EnterMMenuExit()
define config.intra_transition = EnterMMenuIntra()
define config.game_main_transition = EnterMMenuHome()
define config.end_game_transition = EnterMMenuHome()
define config.after_load_transition = None


# =============================================================================
# 6. THE SOUNDTRACK HANDOFF
# =============================================================================
# The Archive and the Arcade are the only two menus in the game that bring their
# own music, and that is the whole reason they are the only two that ever felt
# wrong to move between. Credits, Settings, Save and Load travel between the
# same heavy screens through the same choreographies and have always been fine.
#
# THE HISTORY, BECAUSE EACH FIX EXPOSED THE NEXT PROBLEM
#
#   1. They started with a bare `Play("music", ...)` -- an unconditional HARD
#      CUT that tears the stream down and cold-starts a fresh Ogg decoder on the
#      spot, in the same interaction that starts the transition. The decoder
#      opened on the move's first frames, which is a visible hitch. "Worse the
#      second time" fell straight out of it: the FIRST main menu of a session
#      gets its music at boot with no transition running to disturb.
#
#   2. Fading instead of cutting fixed that, but only for the way in. The fade
#      was 0.35s and the way home is a 0.42s move, so the cold start still
#      landed inside it. And `before_main_menu` -- which the engine runs on
#      EVERY return to the title screen, not once -- was still hard-cutting
#      underneath the fade. Both fixed; see splash.rpy.
#
#   3. Pushing the handoff clear of the move fixed the stutter and bought a lag
#      instead: you arrived in the Archive and sat in the wrong music for half a
#      second while the old track fade out. A fade long enough to be safe is
#      long enough to be noticed.
#
# WHERE IT LANDED: DON'T CROSS-FADE. CUT, AND PUT BLACK IN THE GAP.
#   A picture can be covered end to end while it changes. Sound cannot -- two
#   tracks over each other is mush, and one arriving late over a settled menu is
#   a fault. So the moves that carry a handoff stop trying: the old screen
#   leaves, the frame holds on the void while the outgoing track fades all the
#   way down, and the new screen and the new track arrive together on the same
#   frame. The new track gets NO fade-in, because it is starting on a cut.
#
#   The black hold is also where the decoder cold-start now happens, which is
#   the best place for it in the whole game: nothing is moving, so nothing can
#   stutter.
#
# THE CONTRACT, IN ONE NUMBER
#   ENTER_M_MENU_REVEAL is both the moment the incoming screen appears (every
#   `pause` in the cut choreographies, section 3) and the fade-out handed to
#   renpy.music.play. That works because `play(fadeout=X)` starts the queued
#   track exactly X seconds later -- verified against the engine, not assumed:
#   asking with fadeout=0.34 reported the new track playing at 0.337s.
#   Change this number and change those pauses with it.

init python:

    # The beat the picture and the sound both land on. Long enough to read as a
    # deliberate cut to black rather than a dropped frame, short enough that the
    # menu is not "loading".
    ENTER_M_MENU_REVEAL = 0.34

    class _EnterMMenuMusicIntent(NoRollback):
        """
        The track the menu system last ASKED the music channel for, and the
        moment that ask stops being trusted.

        NoRollback for the same reason the achievement toast queue is: this is
        session bookkeeping about a hardware channel, and it has no business
        being written into saves or being rewound by a rollback.
        """

        def __init__(self):
            self.track = None
            self.until = 0.0

        def already_asked(self, track):
            return (track == self.track) and (time.time() < self.until)

        def pending(self):
            """Is an ask still in flight -- asked for, not yet playing?"""

            if (self.track is None) or (time.time() >= self.until):
                return False

            return renpy.music.get_playing(channel="music") != self.track

        def record(self, track, window):
            self.track = track
            self.until = time.time() + window

    _enter_m_menu_music_intent = _EnterMMenuMusicIntent()

    def enter_m_menu_music(track, fade=None):
        """
        Hand the music channel over to `track` as part of a menu move.

        `fade`
            How long the outgoing track takes to fade out, and therefore how
            long until the new one starts. Defaults to ENTER_M_MENU_REVEAL so
            the new track lands on the frame the new screen appears.
        """

        if fade is None:
            fade = ENTER_M_MENU_REVEAL

        # We already asked for this and it has not landed yet. Both these
        # screens fire `show` AND `replace`, so this is the common case, not an
        # edge one. The window expires on its own, so anything that changes the
        # music behind our back (a game mode, the OP) is never shadowed by a
        # stale intent.
        if _enter_m_menu_music_intent.already_asked(track):
            return

        # ...and it may have landed long ago, which `if_changed` would answer by
        # queueing a redundant extra loop. `before_main_menu` runs on EVERY
        # return to the title screen (see splash.rpy), so "the track you want is
        # the track you have" is the common case there and it should cost
        # nothing at all.
        if renpy.music.get_playing(channel="music") == track:
            return

        _enter_m_menu_music_intent.record(track, fade)

        # fadein=0 is the point: the new track starts at full volume on the cut,
        # rather than swelling up underneath a menu that is already there.
        renpy.music.play(track, channel="music", fadeout=fade, fadein=0, if_changed=True)

    def enter_m_menu_music_is_switching():
        """
        True while a handoff is in flight. EnterMMenuHome (section 5) reads this
        to decide whether the way home needs to cut through black or can take
        the fast covered cycle.
        """

        return _enter_m_menu_music_intent.pending()

    # Action form, for the `show`/`replace` and `key` handlers in the menu
    # screens. It has to be asked for in the SAME interaction that starts the
    # move -- that is what makes the two land together.
    def EnterMMenuMusic(track, fade=None):
        return Function(enter_m_menu_music, track, fade)
