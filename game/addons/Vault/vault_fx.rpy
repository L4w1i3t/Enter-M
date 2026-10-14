# =============================================================================
# ENTER-M :: THE VAULT, AMBIENT LAYER  ("nobody has been down here in years")
# -----------------------------------------------------------------------------
# The air, the light and the filth in the Vault. Everything the room does that
# is not a button.
#
# The brief for this room is the opposite of the title screen's. The bedroom is
# warm, lived in and still awake; this place has been shut since before anyone
# thought to write it down. So the grade here DESATURATES rather than tints,
# the light SAGS rather than breathes, and the air is thick enough to see.
#
# NOTHING IN HERE IS PINNED TO A PIXEL IN THE PAINTING.
#   Same rule as main_menu_fx.rpy, and it matters more here, not less: this
#   background has two fluorescent tubes, a vault door and a wall of drawers,
#   and every one of them is a tempting place to nail a light to. None of them
#   is nailed to. The tubes bloom because HALATION FINDS WHAT IS ALREADY
#   BRIGHT; the tubes stutter because the WHOLE FRAME's exposure stutters. Swap
#   the art for a different cellar and the room still fails its inspection.
#
# WHAT LIVES WHERE
#   vault_fx.rpy   (here)  the ROOM -- grade, flicker, air, filth.
#   vault.rpy              the DOOR and the UI -- the menu, the ledger, the
#                          greeting, and the one hook into the title screen.
#
# WHAT IS BORROWED RATHER THAN REBUILT
#   enter_m.atmos_static / enter_m.atmos_grain  (atmosphere.rpy)  vignette and
#       film grain. A vignette is a vignette; there was no reason to write a
#       second one, and the menu-family grade in main_menu_fx.rpy borrows the
#       same two parts for the same reason.
#   enter_m.mmfx_bloom + mmfx_quad  (main_menu_fx.rpy)  the soft radial plate
#       the drifting dust clouds are painted on.
#   EnterMMenuDust  (main_menu_fx.rpy)  the deterministic mote field. Three
#       instances here, tuned differently, instead of a fourth copy of the
#       class.
#   All four are reached through FUNCTIONS called at screen-build time, never
#   at init time: this file sorts BEFORE main_menu_fx.rpy inside any given init
#   priority, so nothing defined there exists yet while this file is loading.
#
# THE BUDGET
#     Settings -> Graphics -> Atmosphere
#       Full   the grade animates, the tube stutters, the air moves.
#       Light  the grade is drawn but HELD. The tube is steady, the air stops.
#       Off    nothing here draws at all. The painting, as painted.
#
# HOUSE RULES OBSERVED HERE
#   * Every animated shader value is an ATL-interpolated UNIFORM, never the
#     ambient u_time -- so an effect pays for its own frames instead of
#     freezing solid whenever the screen stops asking for them.
#   * Every `shader=` has `mesh True` next to it. Without the mesh the fragment
#     program never runs and the quad draws NOTHING -- silently, lint-clean.
#   * A mesh blits its child at (0,0) and never reads its pixels, so in an
#     at_list the shader transform goes FIRST (innermost) and the camera wraps
#     it.
#   * NOTHING HERE IS BEAT-LOCKED. dump.ogg is a slow, shapeless piece and the
#     flicker below is deliberately arrhythmic -- a light that stutters on the
#     downbeat is a music visualiser, and this one is supposed to be broken.
# =============================================================================


# --- the grade's palette ------------------------------------------------------
# Every colour here is cool, and the dust is the coolest surprise in it: lit
# dust is the colour of the LIGHT ON IT, not the colour of the dust, and the
# only light left in this room comes out of two failing fluorescent tubes. A
# warm dust tint was tried first and it turned the whole room pink.
#
# ALL FIVE ARE `define -11`, WHICH IS NOT DECORATION. A bare `define` runs at
# init priority 0, and section 5 below builds a real displayable at init -8 --
# eight priorities EARLIER -- out of VAULT_VIG_TINT. At offset 0 that is a
# NameError on startup, not a lint warning. -11 is one step ahead of the
# shader registration at -10, so the whole palette exists before anything in
# this file has run.
#
# (main_menu_fx.rpy sidesteps the same trap by repeating its vignette tint as a
# literal inside the init -8 dict. One number in one place is better.)
define -11 VAULT_LAMP_COL = (0.78, 0.87, 1.00)     # what the tubes throw
define -11 VAULT_HAZE_COL = (0.60, 0.63, 0.67)     # what is floating in it
define -11 VAULT_CLOUD_COL = (0.66, 0.70, 0.78)    # the drifting motes-in-a-beam

# The vignette's own tint. Colder and heavier than the title screen's: this is a
# basement, and the corners of a basement do not have any light in them.
define -11 VAULT_VIG_TINT = (0.010, 0.014, 0.022)


# -----------------------------------------------------------------------------
# 1. THE SHADER
# -----------------------------------------------------------------------------
#   enter_m.vault_grade   the whole room. Runs ON the background, sampling it.
#
# One pass does all five jobs, because all five want the same texture fetch and
# a second full-screen pass to do any of them separately would be paying twice
# for the same pixels:
#
#   EXPOSURE    the fluorescent stutter. Applied FIRST, so when the tube drops
#               the highlights fall under the halation threshold and the bloom
#               dies with the light instead of hanging in the air after it.
#   HALATION    four taps, and only what is ALREADY bright blooms. This is the
#               entire reason the tubes glow without this file being told where
#               a tube is.
#   DESATURATION toward luminance, and only slightly. The art is already
#               nearly monochrome; the rust on the door and the yellow of the
#               paper are the only warm things in it, and killing those kills
#               the age with them.
#   HAZE        the MID shadows lifted toward dust colour, modulated by a
#               two-octave blotch field so the air is UNEVEN. Even haze reads
#               as a veil over a photograph; uneven haze reads as a room with
#               something in the air. That unevenness is the whole trick, and
#               the band it is confined to is what keeps it from being milk --
#               see the long note at the haze itself.
#   GRIME       the same field at a higher frequency, darkening instead of
#               lifting. Dirt on the glass rather than dust in the room.
#   BLACK POINT last, and the only step that takes light away globally. Four
#               of the five steps above ADD; without a floor pulled back
#               underneath them the room has no black left in it at all.
init -10 python:

    def _enter_m_vault_register_shaders():

        # tex0 is the background's own render target (mesh True makes one), so
        # v_tex_coord is a clean 0..1 over the picture and the source is fully
        # opaque -- which is why the taps below composite straight RGB without
        # un-premultiplying each one.
        #
        # The hash is atmosphere.rpy's, deliberately: it is sin-free, and the
        # blotch field below evaluates it eight times per pixel. A textbook
        # sin-based hash would put eight transcendentals on every pixel of a
        # 1280x720 frame to draw a pattern that never changes.
        renpy.register_shader("enter_m.vault_grade", variables="""
            uniform sampler2D tex0;
            uniform float u_em_vault_exposure;
            uniform float u_em_vault_bloom;
            uniform float u_em_vault_desat;
            uniform float u_em_vault_haze;
            uniform float u_em_vault_grime;
            uniform float u_em_vault_drift;
            uniform float u_em_vault_crush;
            uniform float u_em_vault_gain;
            uniform vec3  u_em_vault_lamp;
            uniform vec3  u_em_vault_dust;
            varying vec2  v_tex_coord;
        """, fragment_functions="""
            vec2 em_vault_safe(vec2 em_vault_uv) {
                return clamp(em_vault_uv, vec2(0.0015), vec2(0.9985));
            }

            float em_vault_hash(vec2 em_vault_hp) {
                return fract(52.9829189 * fract(dot(
                    em_vault_hp,
                    vec2(0.06711056, 0.00583715))));
            }

            float em_vault_noise(vec2 em_vault_np) {
                vec2 em_vault_i = floor(em_vault_np);
                vec2 em_vault_f = fract(em_vault_np);
                em_vault_f = em_vault_f * em_vault_f *
                    (3.0 - 2.0 * em_vault_f);
                float em_vault_a = em_vault_hash(em_vault_i);
                float em_vault_b = em_vault_hash(
                    em_vault_i + vec2(1.0, 0.0));
                float em_vault_c = em_vault_hash(
                    em_vault_i + vec2(0.0, 1.0));
                float em_vault_d = em_vault_hash(
                    em_vault_i + vec2(1.0, 1.0));
                return mix(
                    mix(em_vault_a, em_vault_b, em_vault_f.x),
                    mix(em_vault_c, em_vault_d, em_vault_f.x),
                    em_vault_f.y);
            }
        """, fragment_300="""
            vec2 em_vault_uv = v_tex_coord;
            vec4 em_vault_base = texture2D(tex0, em_vault_uv);

            // EXPOSURE. The tube, whatever and wherever it is.
            float em_vault_ex = max(u_em_vault_exposure, 0.0);
            vec3 em_vault_col = em_vault_base.rgb * em_vault_ex;

            // HALATION, from the dimmed image, so the glow goes out with the
            // light rather than floating above a dark frame.
            vec3 em_vault_blur =
                texture2D(tex0, em_vault_safe(
                    em_vault_uv + vec2( 0.0058, 0.0))).rgb +
                texture2D(tex0, em_vault_safe(
                    em_vault_uv + vec2(-0.0058, 0.0))).rgb +
                texture2D(tex0, em_vault_safe(
                    em_vault_uv + vec2(0.0,  0.0102))).rgb +
                texture2D(tex0, em_vault_safe(
                    em_vault_uv + vec2(0.0, -0.0102))).rgb;
            em_vault_blur *= 0.25 * em_vault_ex;

            // The threshold is HIGH -- 0.70 -- and that number was measured
            // against this painting rather than guessed. Its concrete walls
            // sit around 0.35-0.50 and its floor around 0.40-0.55; a threshold
            // under about 0.6 blooms the entire room and the picture goes
            // milky. At 0.70 only the tubes and the hot patch of floor under
            // them are over the line, which is the whole intent.
            vec3 em_vault_hi = max(em_vault_blur - vec3(0.70), vec3(0.0)) *
                (1.0 / 0.30);
            em_vault_col += em_vault_hi * u_em_vault_lamp * u_em_vault_bloom;

            // DESATURATION. Partial, on purpose -- see the header.
            float em_vault_lum = dot(em_vault_col, vec3(0.299, 0.587, 0.114));
            em_vault_col = mix(
                em_vault_col,
                vec3(em_vault_lum),
                clamp(u_em_vault_desat, 0.0, 1.0));

            // THE BLOTCH FIELD. Two octaves, both slid by the same drift so
            // the air moves as one body instead of shearing against itself.
            vec2 em_vault_dp = em_vault_uv + vec2(u_em_vault_drift, 0.0);
            float em_vault_blot =
                em_vault_noise(em_vault_dp * 3.1) * 0.64 +
                em_vault_noise(em_vault_dp * 7.3 + vec2(11.3, 4.7)) * 0.36;

            // HAZE, on a BAND rather than on (1 - luminance). This is the one
            // line in the file that was got wrong first and had to be
            // measured: weighting haze by (1 - lum) means a dark painting gets
            // full haze absolutely everywhere, and this painting is dark
            // absolutely everywhere. The result was a room with no black in it
            // -- milk, and less atmospheric than the untouched art.
            //
            // The band keeps the true blacks black (the low smoothstep) and
            // stays out of the highlights (the high one), leaving the veil
            // exactly where airborne dust is actually legible: the mid
            // shadows, which here is most of the concrete.
            //
            // And it is SCALED BY EXPOSURE, because haze is scattered light.
            // Without that the room went flat grey when the tube dropped --
            // brightening, in effect, at the moment it was supposed to be
            // going dark.
            float em_vault_band =
                smoothstep(0.02, 0.14, em_vault_lum) *
                (1.0 - smoothstep(0.35, 0.95, em_vault_lum));
            float em_vault_hazeamt = clamp(
                u_em_vault_haze * (0.35 + 1.30 * em_vault_blot) *
                em_vault_band * em_vault_ex,
                0.0, 0.85);
            em_vault_col = mix(
                em_vault_col,
                u_em_vault_dust,
                em_vault_hazeamt);

            // GRIME. The same field, finer and inverted -- this one takes
            // light away, which is what dirt on a lens does.
            float em_vault_dirt = em_vault_noise(
                em_vault_uv * 15.7 + vec2(3.9, 8.1));
            em_vault_col *= 1.0 - clamp(
                u_em_vault_grime * (0.30 + 0.70 * em_vault_dirt),
                0.0, 0.60);

            // BLACK POINT, last. Everything above this line adds or veils, and
            // a picture that has only been added to has no floor left. This
            // pulls one back and puts the gain back on top of it, which is
            // what keeps the room reading as a dark basement with dust in it
            // rather than as a photograph of dust.
            em_vault_col = max(
                em_vault_col - vec3(u_em_vault_crush), vec3(0.0)) *
                max(u_em_vault_gain, 0.0);

            float em_vault_a = em_vault_base.a;
            gl_FragColor = vec4(
                clamp(em_vault_col, 0.0, 1.0) * em_vault_a, em_vault_a);
        """)

    try:
        _enter_m_vault_register_shaders()
        ENTER_M_VAULT_SHADERS = True
    except Exception as _enter_m_vault_shader_error:
        ENTER_M_VAULT_SHADERS = False
        renpy.log("ENTER-M VAULT: shader registration failed: %r" %
            _enter_m_vault_shader_error)


# -----------------------------------------------------------------------------
# 2. QUALITY
# -----------------------------------------------------------------------------
# The Vault answers to the same Atmosphere preference as everything else, and
# it asks main_menu_fx.rpy rather than re-reading the setting -- one place in
# the game decides what "Light" means.
#
# These are FUNCTIONS, not values: mmfx_level() is defined at init -9 in a file
# that sorts after this one, so calling it while this file loads would fail.
# Nothing below runs before the first frame of the Vault.
init -9 python:

    def vaultfx_lit():
        """True when the room's shader layer can actually be drawn.

        Off opts out; so does a machine with no model renderer, a driver that
        refused the source, or a build with atmosphere.rpy's parts missing. In
        every one of those cases the Vault is simply the painting, which is
        already a dusty room -- it just stops being a dusty room that moves.
        """

        return (mmfx_level() != "off"
            and ENTER_M_VAULT_SHADERS
            and ENTER_M_ATMOS_SHADERS
            and renpy.display.render.models)

    def vaultfx_alive():
        """True when the loops may run: the stutter, the drift, the air."""

        return mmfx_level() == "full"


# -----------------------------------------------------------------------------
# 3. THE CAMERA
# -----------------------------------------------------------------------------
# Almost nothing. The title screen's room drifts because somebody lives in it;
# this one is a photograph of a place that has stopped happening, and the only
# reason it moves at all is that a completely locked frame reads as a JPEG
# rather than as a room.
#
# 47s and 39s are coprime in seconds, so the pair does not return to its start
# for just over half an hour. zoom 1.032 buys 20.5px of overscan per side
# across and 11.5px down; the pan uses 11 of the first and the lift 6 of the
# second, so an edge can never crawl into frame.
transform vault_camera:
    subpixel True
    zoom 1.032
    xalign 0.5
    yalign 0.5
    parallel:
        ease 47.0 xoffset -11
        ease 47.0 xoffset 11
        repeat
    parallel:
        ease 39.0 yoffset 6
        ease 39.0 yoffset -6
        repeat


transform vault_camera_still:
    subpixel True
    zoom 1.032
    xalign 0.5
    yalign 0.5


# -----------------------------------------------------------------------------
# 4. THE GRADE, AND THE TUBE THAT IS GOING
# -----------------------------------------------------------------------------
# Held first: Light wants the look of the room, not its faults.
transform vault_grade_still:
    mesh True
    shader "enter_m.vault_grade"
    u_em_vault_lamp VAULT_LAMP_COL
    u_em_vault_dust VAULT_HAZE_COL
    u_em_vault_exposure 1.0
    u_em_vault_bloom 0.55
    u_em_vault_desat 0.18
    u_em_vault_haze 0.085
    u_em_vault_grime 0.075
    u_em_vault_crush 0.014
    u_em_vault_gain 1.07
    u_em_vault_drift 0.0


# THE STUTTER. This is the single effect that carries the whole "this place
# needs work" idea, so it is worth being precise about why it is shaped the way
# it is.
#
# A failing fluorescent does not blink on a timer. It sags for a long time,
# coughs two or three times in under half a second, and then behaves itself for
# long enough that you stop waiting for it -- which is exactly when it is worth
# doing again. So: long eased sags, short LINEAR coughs (a cough that eases is
# a fade, and a fade reads as a dimmer, not as a fault), and dead air between
# the bursts that is longer than anybody's patience for watching a light.
#
# The cycle runs about 40.6s and is built out of deliberately unroundable
# numbers. dump.ogg is under it the whole time and the two must never appear to
# agree about anything.
#
# The overshoot past 1.0 in each burst is not decoration: a tube that restrikes
# comes back brighter than it was for an instant, and without it the coughs
# read as the picture being dipped rather than the light being lost.
#
# The drift ramp lives in the same transform because it is the same air. It
# runs one way only and resets, which is invisible: the blotch field it slides
# has no landmarks in it to notice the jump.
transform vault_grade:
    mesh True
    shader "enter_m.vault_grade"
    u_em_vault_lamp VAULT_LAMP_COL
    u_em_vault_dust VAULT_HAZE_COL
    u_em_vault_exposure 1.0
    u_em_vault_bloom 0.55
    u_em_vault_desat 0.18
    u_em_vault_haze 0.085
    u_em_vault_grime 0.075
    u_em_vault_crush 0.014
    u_em_vault_gain 1.07
    u_em_vault_drift 0.0
    parallel:
        ease 53.0 u_em_vault_drift 0.34
        u_em_vault_drift 0.0
        repeat
    parallel:
        ease 17.0 u_em_vault_haze 0.115
        ease 23.0 u_em_vault_haze 0.064
        repeat
    parallel:
        block:
            # settling
            ease 6.5 u_em_vault_exposure 0.93
            ease 5.2 u_em_vault_exposure 1.00
            pause 2.1
            # first cough
            linear 0.04 u_em_vault_exposure 0.44
            linear 0.05 u_em_vault_exposure 1.07
            linear 0.03 u_em_vault_exposure 0.37
            linear 0.07 u_em_vault_exposure 0.97
            pause 0.23
            linear 0.03 u_em_vault_exposure 0.55
            linear 0.06 u_em_vault_exposure 1.00
            # long enough that you stop waiting for it
            pause 4.7
            ease 7.3 u_em_vault_exposure 0.89
            ease 4.4 u_em_vault_exposure 1.00
            pause 3.4
            # second cough, weaker
            linear 0.05 u_em_vault_exposure 0.61
            linear 0.04 u_em_vault_exposure 1.04
            linear 0.06 u_em_vault_exposure 0.90
            linear 0.05 u_em_vault_exposure 1.00
            pause 6.1
            repeat


# -----------------------------------------------------------------------------
# 5. VIGNETTE + GRAIN
# -----------------------------------------------------------------------------
# atmosphere.rpy's parts, Vault-tuned. fill and key are BOTH ZERO, same as the
# title screen's: the grade above already owns every photon in this room, and
# the one lesson that layer learned the hard way is that ADDED LIGHT COSTS
# COLOUR. What is left is a vignette -- which darkens, so it costs no colour
# and gains contrast -- and, at Full, the signed grain.
#
# The vignette is heavier and its inner edge is tighter than the menu family's:
# a basement should be closing in slightly, and a wide soft vignette on a room
# this dark is invisible anyway.
#
# Both are SCREEN-LOCKED, outside the camera. A vignette and film grain belong
# to the lens, not to the room, and would give the whole trick away if they
# slid about with the picture.
init -8 python:

    _VAULT_GRADE_BASE = dict(
        u_em_atmos_vig_strength=0.42,
        u_em_atmos_vig_inner=0.44,
        u_em_atmos_vig_outer=1.06,
        u_em_atmos_vig_tint=VAULT_VIG_TINT,
        u_em_atmos_key_pos=(0.5, 0.5),
        u_em_atmos_key_col=(1.0, 1.0, 1.0),
        u_em_atmos_fill_top=(0.5, 0.5, 0.5),
        u_em_atmos_fill_bottom=(0.5, 0.5, 0.5),
        u_em_atmos_fill_amt=0.0,
        u_em_atmos_key_amt=0.0,
        u_em_atmos_key_size=0.62,
        u_em_atmos_key_softness=0.70)

    def _enter_m_vault_grade(_enter_m_grain):
        _enter_m_kw = dict(_VAULT_GRADE_BASE)
        _enter_m_kw.update(
            mesh=True,
            shader=(("enter_m.atmos_static", "enter_m.atmos_grain")
                if _enter_m_grain else "enter_m.atmos_static"))

        if _enter_m_grain:
            # Coarser than the title screen's 0.013. This is meant to look
            # like a room nobody has cleaned, photographed by a camera nobody
            # has cleaned either.
            _enter_m_kw.update(
                u_em_atmos_grain=0.019,
                u_em_atmos_grain_rate=12.0,
                u_em_atmos_pulse=0.0,
                u_em_atmos_pulse_rate=1.0)

        return Transform(
            Solid("#00000000", xysize=(
                config.screen_width, config.screen_height)),
            **_enter_m_kw)

    VAULT_GRADE_FULL = _enter_m_vault_grade(True)
    VAULT_GRADE_LIGHT = _enter_m_vault_grade(False)


# -----------------------------------------------------------------------------
# 6. THE AIR
# -----------------------------------------------------------------------------
# Three mote fields rather than one, because "dusty" is three different things
# happening at three different speeds and a single field can only be one of
# them:
#
#   HAZE   big, dim, nearly still. The suspended load that has been hanging
#          here since the door shut. Drifts sideways more than down.
#   MOTES  small, brighter, the ones catching what light there is. These are
#          the ones the eye actually reads as "dust".
#   GRIT   few, fast, straight down, no sway. Ceiling dust shaking loose.
#          Rare enough to register as an event rather than as weather.
#
# All three are EnterMMenuDust from main_menu_fx.rpy. The class already does
# the two hard parts -- motion derived from the SpriteManager's own st, so
# there is no state to desync and no dependence on frame rate, and a local LCG
# so building a field never advances the rollback-aware global RNG.
#
# WHY THESE ARE SHADER DOTS AND NOT COLOURED SQUARES
#   The first version used the title screen's approach directly: 2-4px Solids
#   at additive alpha. Measured over a flat plate they were unmistakably there
#   -- 110 changed pixels, peak delta 84 -- and over the actual painting they
#   were invisible at 1:1 and still invisible enlarged three times. Two reasons,
#   and both of them are about this room rather than about the technique:
#
#   1. The title screen's motes sit over a dark bedroom at night. These sit
#      over lit concrete at roughly 0.35-0.50 luminance, which is the worst
#      possible ground for a faint additive dot.
#   2. A hard-edged 3px square does not read as dust at any brightness. It
#      reads as a stuck pixel. Real airborne dust is out of focus, because it
#      is centimetres from the lens and the room is metres away.
#
#   So the two suspended fields are soft radial dots -- enter_m.mmfx_bloom on a
#   small transparent quad, the same part the dust clouds and the title screen's
#   row marker are painted with. The quad is 3-4x the visible dot: the falloff
#   reaches zero well inside its own edge, which is what stops a mesh from
#   showing its rectangle.
#
#   GRIT stays a Solid, deliberately. It is falling fast enough to streak, and a
#   streak has an edge.
#
# The palette is grey-cool, not white: lit dust is the colour of the light on
# it, and the only light in this room comes out of two fluorescent tubes.
init -9 python:

    def _vault_mote(w, h, gain, col=(0.86, 0.88, 0.92), fall=2.2):
        """One soft, out-of-focus speck.

        `w` and `h` are the QUAD, not the dot: the falloff reaches zero well
        inside the plate, which is what stops a mesh from showing its own
        rectangle. They also set the speck's SHAPE -- mmfx_bloom normalises to
        the quad, so a square plate gives a round mote and a tall thin one
        gives the soft vertical streak a falling speck leaves.

        `gain` is the peak brightness added at its centre. mesh=True is not
        optional: without it the fragment program never runs and the quad draws
        nothing at all, silently.
        """

        return Transform(
            Solid("#00000000", xysize=(int(w), int(h))),
            mesh=True,
            shader="enter_m.mmfx_bloom",
            u_em_mmfx_col=col,
            u_em_mmfx_core=0.0,
            u_em_mmfx_edge=1.0,
            u_em_mmfx_fall=fall,
            u_em_mmfx_gain=gain)


# HAZE: big, soft, dim. The suspended load, too diffuse to have edges.
image vault_dust_0 = _vault_mote(26, 26, 0.045, (0.74, 0.77, 0.82), 2.9)
image vault_dust_1 = _vault_mote(30, 30, 0.070, (0.76, 0.79, 0.84), 2.9)
image vault_dust_2 = _vault_mote(34, 34, 0.098, (0.79, 0.82, 0.86), 2.7)
image vault_dust_3 = _vault_mote(38, 38, 0.130, (0.82, 0.85, 0.89), 2.6)

# MOTES: the ones the eye actually reads as dust. Small, near, bright enough to
# survive being drawn over lit concrete.
image vault_mote_0 = _vault_mote(10, 10, 0.20)
image vault_mote_1 = _vault_mote(12, 12, 0.32)
image vault_mote_2 = _vault_mote(14, 14, 0.45, (0.90, 0.91, 0.94))
image vault_mote_3 = _vault_mote(16, 16, 0.58, (0.94, 0.94, 0.96))

# GRIT: ceiling dust on its way down. Tall thin quads, so the same bloom that
# rounds a mote stretches these into a soft vertical streak.
#
# These were hard-edged Solids for one build and it was a mistake worth
# recording: at 34px/s a 2x5 additive rectangle does not read as falling dust,
# it reads as a stuck pixel or a UI artefact -- the eye finds the one thing on
# a painted screen with perfectly straight sides and locks onto it. Nothing in
# a room made of dust is allowed a hard edge.
image vault_grit_0 = _vault_mote(7, 20, 0.26, (0.84, 0.85, 0.87), 2.4)
image vault_grit_1 = _vault_mote(9, 26, 0.38, (0.88, 0.89, 0.90), 2.4)


init python:

    # Built once and reused for the life of the process, exactly like the title
    # screen's. A SpriteManager is not cheap to assemble and the Vault is a
    # place the player will open more than once.
    #
    # The bounds run past every edge of the frame so no field has a visible
    # boundary the motes wrap at. Vertical spans are deliberately taller than
    # the screen for the same reason: EnterMMenuDust wraps modulo the span, and
    # a span equal to the screen puts every wrap on the same two rows.
    _VAULT_AIR = {}

    def _vault_field(key, **kwargs):
        if key not in _VAULT_AIR:
            _VAULT_AIR[key] = EnterMMenuDust(**kwargs).manager
        return _VAULT_AIR[key]

    def vault_haze_field():
        """The suspended load. Slow, sideways, barely there."""

        return _vault_field(
            "haze",
            children=("vault_dust_0", "vault_dust_1",
                "vault_dust_2", "vault_dust_3"),
            count=26,
            seed=0x5641554c,
            bounds=(-70.0, -60.0, 1350.0, 800.0),
            vy=2.1, vx=5.4, amp=26.0, speed=0.21)

    def vault_mote_field():
        """The ones catching the light. Faster, brighter, more of them."""

        return _vault_field(
            "motes",
            children=("vault_mote_0", "vault_mote_1",
                "vault_mote_2", "vault_mote_3"),
            count=46,
            seed=0x54484556,
            bounds=(-40.0, -40.0, 1330.0, 780.0),
            vy=6.8, vx=2.6, amp=17.0, speed=0.46)

    def vault_grit_field():
        """Ceiling dust. Straight down, no sway, and not many of them."""

        return _vault_field(
            "grit",
            children=("vault_grit_0", "vault_grit_1"),
            count=12,
            seed=0x47524954,
            bounds=(0.0, -220.0, 1280.0, 960.0),
            vy=34.0, vx=0.0, amp=2.0, speed=0.11)


# -----------------------------------------------------------------------------
# 7. THE CLOUDS
# -----------------------------------------------------------------------------
# Two very large, very dim warm-grey pools wandering the frame on long, coprime
# cycles. They are the "dust cloud" half of the brief, and they are pure
# invention -- the one thing in this file that is not something the painting
# already had.
#
# They are additive and enormous, which is the only way this reads correctly:
# a dust cloud is not an object with an edge, it is a region where the air is
# thicker, and the moment you can see where one stops it turns into a smudge on
# the screen. Hence gains in the low hundredths and a falloff exponent that
# keeps almost all the energy in the middle third of the plate.
#
# 43s / 31s and 37s / 29s: four periods, no two of which share a factor, so
# neither cloud repeats its path and the two never pace each other.
transform vault_cloud_a:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col VAULT_CLOUD_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 2.8
    u_em_mmfx_gain 0.0
    parallel:
        ease 43.0 xpos 760
        ease 43.0 xpos 120
        repeat
    parallel:
        ease 31.0 ypos 60
        ease 31.0 ypos -190
        repeat
    parallel:
        linear 4.0 u_em_mmfx_gain 0.030
        ease 21.0 u_em_mmfx_gain 0.055
        ease 27.0 u_em_mmfx_gain 0.020
        repeat


transform vault_cloud_b:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col VAULT_CLOUD_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 3.4
    u_em_mmfx_gain 0.0
    parallel:
        ease 37.0 xpos 250
        ease 37.0 xpos 880
        repeat
    parallel:
        ease 29.0 ypos -140
        ease 29.0 ypos 100
        repeat
    parallel:
        linear 6.0 u_em_mmfx_gain 0.019
        ease 25.0 u_em_mmfx_gain 0.041
        ease 19.0 u_em_mmfx_gain 0.014
        repeat


# -----------------------------------------------------------------------------
# 8. THE ROOM, ASSEMBLED
# -----------------------------------------------------------------------------
# Two entry points, because the Vault is looked at from two different places:
#
#   vault_room_layer   the whole room INCLUDING the background. What the menu
#                      screen uses.
#   vault_air_layer    everything EXCEPT the background. What the greeting
#                      scene uses, because there the background is on the
#                      master layer under a sprite and the grade has to be
#                      applied to it by the `scene` statement instead.
#
# The split is what keeps the two views identical without either one owning the
# other: the air, the clouds, the vignette and the grain are declared once and
# both callers get the same room.
#
# The air rides INSIDE the camera with the picture -- dust is in the room. The
# vignette and grain sit OUTSIDE it -- those are in the lens. The clouds are
# outside too, and that is deliberate rather than sloppy: at these gains a
# cloud is a change in the air between the room and the viewer, and pinning it
# to the room would make it a fog bank sitting on the floor.
screen vault_air_layer():

    python:
        _vault_alive = vaultfx_alive()
        _vault_lit = vaultfx_lit()

    # The air needs BOTH gates, not just `alive`. Two of the three fields are
    # made of mesh-and-shader dots, and on a machine with no model renderer a
    # mesh is ignored and its child -- a transparent quad -- is what draws. That
    # is not a dim field, it is an invisible one, and it would cost a full
    # sprite pass to produce nothing. Where the shaders cannot run, the Vault is
    # the painting, which is already a dusty room.
    if _vault_alive and _vault_lit:
        fixed:
            xysize (config.screen_width, config.screen_height)
            at vault_camera

            add vault_haze_field()
            add vault_mote_field()
            add vault_grit_field()

    if _vault_lit:
        if _vault_alive:
            add mmfx_quad(900, 780) at vault_cloud_a
            add mmfx_quad(760, 660) at vault_cloud_b
        add (VAULT_GRADE_FULL if _vault_alive else VAULT_GRADE_LIGHT)


screen vault_room_layer():

    python:
        _vault_room_alive = vaultfx_alive()
        _vault_room_lit = vaultfx_lit()

        # Shader innermost, camera outermost. A mesh blits its child at (0, 0)
        # and never looks at its pixels, so a camera on the INSIDE would be
        # graded through a stationary lens instead of moving under one.
        _vault_room_at = ([
            (vault_grade if _vault_room_alive else vault_grade_still),
            (vault_camera if _vault_room_alive else vault_camera_still)]
            if _vault_room_lit else
            [vault_camera if _vault_room_alive else vault_camera_still])

    add "bg vault" at _vault_room_at

    use vault_air_layer
