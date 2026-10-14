# Title-scene camera, grade, particles and shared menu lighting primitives.
# The grade works across the image; sidebar geometry is owned by
# main_menu_room.rpy. Ambient cycles are independent of music playback phase.
# Atmosphere Full animates the layer, Light holds the grade, and Off disables
# the shader layer. mmfx_lit() also requires model rendering and registration.
#
# Animated shader uniforms use ATL to request their own redraws. Shader
# transforms require mesh True and sit inside the camera transform.

define MMFX_HAZE_COL = (1.00, 0.86, 0.68)
define MMFX_LEAK_COL = (1.00, 0.72, 0.44)

# --- the sidebar's own light --------------------------------------------------
define MMFX_MARK_COL = (0.96, 0.55, 0.40)     # coral: this is the selected row
define MMFX_GLINT_COL = (1.00, 0.88, 0.74)
define MMFX_SEAM_COL = (0.44, 0.76, 0.72)     # teal: the seam down the edge
define MMFX_LOGO_COL = (0.44, 0.73, 0.70)

# Geometry the sidebar and this file both have to agree on. The row pitch is
# restated from main_menu_room.rpy on purpose -- these are the only two places
# that know it, and a marker that slides to the wrong row is obvious on sight.
define MMFX_ROW_Y0 = 140
define MMFX_ROW_PITCH = 48
define MMFX_ROW_W = 376
define MMFX_ROW_H = 42

# The seam Solid in main_menu_room.rpy runs y 24..696. Both ends of the
# travelling node are DERIVED from that span and the node's own height, so it
# can never hang off the end of the rail it is supposed to be riding.
define MMFX_SEAM_Y0 = 24
define MMFX_SEAM_H = 672
define MMFX_SEAM_NODE_H = 148

# The room is everything right of the sidebar. This is a UI number, not an art
# one -- it is where the panel ends, and it moves only if the panel does.
define MMFX_ROOM_X = 462


# -----------------------------------------------------------------------------
# 1. SHADERS
# -----------------------------------------------------------------------------
#   enter_m.mmfx_lofi    the grade. Runs ON the background, sampling it.
#   enter_m.mmfx_bloom   a soft radial light. The light leak and the sidebar.
#   enter_m.mmfx_sweep   a specular band travelling across a quad. The glint
#                        that crosses whichever menu row you are on.
init -10 python:

    def _enter_m_mmfx_register_shaders():

        # THE GRADE. Four whole-frame operations, none of which needs to know
        # what it is looking at: tape wobble, chromatic aberration, halation,
        # and a warm haze in the shadows.
        #
        # tex0 is the background's own render target (mesh True makes one), so
        # v_tex_coord is a clean 0..1 over the picture and the source is fully
        # opaque -- which is why the taps below composite straight RGB without
        # un-premultiplying each one.
        renpy.register_shader("enter_m.mmfx_lofi", variables="""
            uniform sampler2D tex0;
            uniform float u_em_lofi_warp;
            uniform float u_em_lofi_phase;
            uniform float u_em_lofi_ca;
            uniform float u_em_lofi_bloom;
            uniform float u_em_lofi_haze;
            uniform vec3  u_em_lofi_tint;
            varying vec2  v_tex_coord;
        """, fragment_functions="""
            vec2 em_lofi_safe(vec2 em_lofi_uv) {
                return clamp(em_lofi_uv, vec2(0.0015), vec2(0.9985));
            }
        """, fragment_300="""
            vec2 em_lofi_uv = v_tex_coord;

            // TAPE WOBBLE. Two spatial frequencies, both advanced by the same
            // phase at INTEGER multiples so the pair wraps seamlessly when the
            // ATL resets the phase at 2*pi.
            float em_lofi_wob =
                sin(em_lofi_uv.y * 6.3 + u_em_lofi_phase) * 0.62 +
                sin(em_lofi_uv.y * 2.1 - u_em_lofi_phase * 3.0) * 0.38;
            em_lofi_uv.x += em_lofi_wob * u_em_lofi_warp;
            em_lofi_uv = em_lofi_safe(em_lofi_uv);

            // CHROMATIC ABERRATION, zero in the middle and growing with the
            // square of the radius, which is where a real lens puts it.
            vec2 em_lofi_rc = em_lofi_uv - vec2(0.5);
            vec2 em_lofi_off = em_lofi_rc * dot(em_lofi_rc, em_lofi_rc) *
                u_em_lofi_ca;

            vec4 em_lofi_base = texture2D(tex0, em_lofi_uv);
            vec3 em_lofi_col = vec3(
                texture2D(tex0, em_lofi_safe(em_lofi_uv + em_lofi_off)).r,
                em_lofi_base.g,
                texture2D(tex0, em_lofi_safe(em_lofi_uv - em_lofi_off)).b);

            // HALATION. Four taps, and only what is ALREADY bright blooms --
            // this is what makes the lamp and the laptop glow without anything
            // in this file knowing that a lamp or a laptop is there.
            vec3 em_lofi_blur =
                texture2D(tex0, em_lofi_safe(em_lofi_uv + vec2( 0.0052, 0.0))).rgb +
                texture2D(tex0, em_lofi_safe(em_lofi_uv + vec2(-0.0052, 0.0))).rgb +
                texture2D(tex0, em_lofi_safe(em_lofi_uv + vec2(0.0,  0.0092))).rgb +
                texture2D(tex0, em_lofi_safe(em_lofi_uv + vec2(0.0, -0.0092))).rgb;
            em_lofi_blur *= 0.25;

            vec3 em_lofi_hi = max(em_lofi_blur - vec3(0.52), vec3(0.0)) *
                (1.0 / 0.48);
            em_lofi_col += em_lofi_hi * u_em_lofi_tint * u_em_lofi_bloom;

            // WARM HAZE, weighted toward the SHADOWS. Lifting the floor toward
            // a warm tint is the "printed to tape" part; doing it everywhere
            // would just be a veil, and a veil costs the picture its colour.
            float em_lofi_lum = dot(em_lofi_col, vec3(0.299, 0.587, 0.114));
            em_lofi_col = mix(
                em_lofi_col,
                u_em_lofi_tint,
                u_em_lofi_haze * (1.0 - em_lofi_lum));

            float em_lofi_a = em_lofi_base.a;
            gl_FragColor = vec4(
                clamp(em_lofi_col, 0.0, 1.0) * em_lofi_a, em_lofi_a);
        """)

        renpy.register_shader("enter_m.mmfx_bloom", variables="""
            uniform vec3  u_em_mmfx_col;
            uniform float u_em_mmfx_gain;
            uniform float u_em_mmfx_core;
            uniform float u_em_mmfx_edge;
            uniform float u_em_mmfx_fall;
            varying vec2  v_tex_coord;
        """, fragment_300="""
            // uv is normalized to this quad, so the falloff is an ellipse in
            // the quad's own proportions -- a wide plate makes a wide pool
            // with no aspect maths at the call site.
            vec2 em_mmfx_d = (v_tex_coord - vec2(0.5)) * 2.0;
            float em_mmfx_r = min(length(em_mmfx_d), 1.0);

            float em_mmfx_outer = max(
                u_em_mmfx_edge, u_em_mmfx_core + 0.002);
            float em_mmfx_m = 1.0 - smoothstep(
                u_em_mmfx_core, em_mmfx_outer, em_mmfx_r);
            em_mmfx_m = pow(
                clamp(em_mmfx_m, 0.0, 1.0), max(u_em_mmfx_fall, 0.05));

            // Belt and braces: whatever the caller asked for, the light is
            // gone before the plate's own rectangle. A mesh is clipped dead
            // at its edge, and a glow still lit there IS a glowing box.
            em_mmfx_m *= 1.0 - smoothstep(0.86, 1.0, em_mmfx_r);

            float em_mmfx_a = clamp(
                em_mmfx_m * max(u_em_mmfx_gain, 0.0), 0.0, 1.0);
            gl_FragColor = vec4(u_em_mmfx_col * em_mmfx_a, 0.0);
        """)

        renpy.register_shader("enter_m.mmfx_sweep", variables="""
            uniform vec3  u_em_mmfx_sweep_col;
            uniform float u_em_mmfx_sweep;
            uniform float u_em_mmfx_sweep_w;
            uniform float u_em_mmfx_sweep_gain;
            uniform float u_em_mmfx_sweep_skew;
            varying vec2  v_tex_coord;
        """, fragment_300="""
            vec2 em_mmfx_uv = v_tex_coord;

            // Skew leans the band so it reads as a reflection crossing a
            // surface rather than a wipe crossing a rectangle.
            float em_mmfx_p = em_mmfx_uv.x +
                (em_mmfx_uv.y - 0.5) * u_em_mmfx_sweep_skew;
            float em_mmfx_w = max(u_em_mmfx_sweep_w, 0.01);
            float em_mmfx_band = 1.0 - smoothstep(
                0.0, em_mmfx_w, abs(em_mmfx_p - u_em_mmfx_sweep));
            em_mmfx_band *= em_mmfx_band;

            float em_mmfx_fade =
                smoothstep(0.0, 0.18, em_mmfx_uv.y) *
                (1.0 - smoothstep(0.82, 1.0, em_mmfx_uv.y)) *
                smoothstep(0.0, 0.06, em_mmfx_uv.x) *
                (1.0 - smoothstep(0.94, 1.0, em_mmfx_uv.x));

            float em_mmfx_a = clamp(
                em_mmfx_band * em_mmfx_fade *
                max(u_em_mmfx_sweep_gain, 0.0), 0.0, 1.0);
            gl_FragColor = vec4(u_em_mmfx_sweep_col * em_mmfx_a, 0.0);
        """)

    try:
        _enter_m_mmfx_register_shaders()
        ENTER_M_MMFX_SHADERS = True
    except Exception as _enter_m_mmfx_shader_error:
        ENTER_M_MMFX_SHADERS = False
        renpy.log("ENTER-M MMFX: shader registration failed: %r" %
            _enter_m_mmfx_shader_error)


# -----------------------------------------------------------------------------
# 2. QUALITY
# -----------------------------------------------------------------------------
init -9 python:

    def mmfx_level():
        """Full / Light / Off, as the Atmosphere preference has it."""

        _enter_m_q = getattr(persistent, "enter_m_atmos_quality", "full")
        if _enter_m_q not in ("full", "light", "off"):
            return "full"
        return _enter_m_q

    def mmfx_lit():
        """True when the shader layer can actually be drawn.

        Off opts out; so does a machine with no model renderer, or a driver
        that refused the shader source. In every one of those cases the room
        simply looks the way the painting looks, which is already finished.
        """

        return (mmfx_level() != "off"
            and ENTER_M_MMFX_SHADERS
            and renpy.display.render.models)

    def mmfx_alive():
        """True when the ambient loops may run: camera, grade, air, grain."""

        return mmfx_level() == "full"


init python:

    @renpy.pure
    def mmfx_quad(w, h):
        """A transparent plate for a shader to paint light onto."""

        return Solid("#00000000", xysize=(int(w), int(h)))


# -----------------------------------------------------------------------------
# 2b. THE SCENE
# -----------------------------------------------------------------------------
# Not a place: an engraved orrery of the calendar -- a month ring, a day ring,
# crossed orbits -- floating in a night field with a few constellations, in the
# illustrated menu family's gold, plum, teal and paper. The game is told in
# dates; this is where the dates are kept between stories.
#
# The rings are separate layers so Full can turn them. Light and Off use the
# composite, which has every ring at the angle the turning starts from, so the
# two agree on their first frame. Engravings: assets/gui/menu/illustrated/title/.
image mmfx_title_field = "assets/gui/menu/illustrated/title/field.svg"
image mmfx_title_months = "assets/gui/menu/illustrated/title/ring_months.svg"
image mmfx_title_days = "assets/gui/menu/illustrated/title/ring_days.svg"
image mmfx_title_orbits = "assets/gui/menu/illustrated/title/ring_orbits.svg"
image enter_m_title_scene = Composite(
    (1280, 720),
    (0, 0), "mmfx_title_field",
    (535, 40), "mmfx_title_months",
    (535, 40), "mmfx_title_days",
    (535, 40), "mmfx_title_orbits")

# One ring turning about the orrery's centre (855, 360). Negative period turns
# it the other way. A whole turn takes minutes: this is a clock nobody is
# meant to read, and `rotate 0` after a full turn is the same angle, so the
# loop has no seam.
transform mmfx_orrery_spin(period=300.0):
    subpixel True
    anchor (0.5, 0.5)
    transform_anchor True
    pos (855, 360)
    rotate 0
    block:
        linear abs(period) rotate (360.0 if period > 0 else -360.0)
        rotate 0
        repeat

# A warm light at the heart of the mechanism. A gain ramp in, then a slow
# breath; held at Light. Additive, so it lifts the gold engraving it sits on.
transform mmfx_orrery_glow:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_LEAK_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 2.0
    u_em_mmfx_gain 0.0
    linear 1.2 u_em_mmfx_gain 0.30
    block:
        ease 7.0 u_em_mmfx_gain 0.40
        ease 7.0 u_em_mmfx_gain 0.26
        repeat

transform mmfx_orrery_glow_still:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_LEAK_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 2.0
    u_em_mmfx_gain 0.30


# -----------------------------------------------------------------------------
# 3. THE CAMERA
# -----------------------------------------------------------------------------
# Three independent moves on three coprime bar counts -- 8, 5 and 7 -- so the
# composite path takes 1120s to come back to where it started. Each is its own
# `parallel` branch touching ONE property, because two branches that both
# touch xoffset fight over it and the loser's value is simply gone.
#
# zoom bottoms out at 1.045, which buys 28.8px of overscan per side across and
# 16.2px down. The pan uses 18 of the first and the lift 10 of the second, so
# an edge can never crawl into frame at the extremes of the move.
transform mmfx_room_camera:
    subpixel True
    zoom 1.045
    xalign 0.5
    yalign 0.5
    parallel:
        ease 32.0 xoffset -18
        ease 32.0 xoffset 18
        repeat
    parallel:
        ease 20.0 yoffset 10
        ease 20.0 yoffset -10
        repeat
    parallel:
        ease 28.0 zoom 1.062
        ease 28.0 zoom 1.045
        repeat


transform mmfx_room_still:
    subpixel True
    zoom 1.045
    xalign 0.5
    yalign 0.5


# -----------------------------------------------------------------------------
# 4. THE GRADE
# -----------------------------------------------------------------------------
# Held first: Light wants the look, not the motion.
transform mmfx_lofi_still:
    mesh True
    shader "enter_m.mmfx_lofi"
    u_em_lofi_tint MMFX_HAZE_COL
    u_em_lofi_warp 0.0
    u_em_lofi_phase 0.0
    u_em_lofi_ca 0.0060
    u_em_lofi_bloom 0.55
    u_em_lofi_haze 0.070


# The wobble phase resets at 2*pi, where both of the shader's sine terms are
# back where they started, so the loop has no seam. 8s is two bars.
transform mmfx_lofi:
    mesh True
    shader "enter_m.mmfx_lofi"
    u_em_lofi_tint MMFX_HAZE_COL
    u_em_lofi_warp 0.0013
    u_em_lofi_ca 0.0060
    u_em_lofi_phase 0.0
    u_em_lofi_bloom 0.50
    u_em_lofi_haze 0.060
    parallel:
        linear 8.0 u_em_lofi_phase 6.28318530718
        u_em_lofi_phase 0.0
        repeat
    parallel:
        ease 16.0 u_em_lofi_haze 0.086
        ease 16.0 u_em_lofi_haze 0.052
        repeat
    parallel:
        ease 16.0 u_em_lofi_bloom 0.62
        ease 32.0 u_em_lofi_bloom 0.44
        ease 16.0 u_em_lofi_bloom 0.56
        repeat


# The light leak: one soft warm blob wandering the frame on eight bars across
# and five down. It is screen-locked, not room-locked -- a leak happens in the
# lens, not in the bedroom -- and it is the only element here that is pure
# invention rather than something the picture already had.
transform mmfx_leak_drift:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_LEAK_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 2.3
    u_em_mmfx_gain 0.0
    parallel:
        ease 32.0 xpos 900
        ease 32.0 xpos 340
        repeat
    parallel:
        ease 20.0 ypos 150
        ease 20.0 ypos -180
        repeat
    parallel:
        linear 6.0 u_em_mmfx_gain 0.075
        ease 16.0 u_em_mmfx_gain 0.115
        ease 16.0 u_em_mmfx_gain 0.045
        repeat


# -----------------------------------------------------------------------------
# 5. AIR
# -----------------------------------------------------------------------------
# Motes, spread evenly over the visible room and lit ONLY by their own slow
# twinkle. The first version weighted brightness by distance to the desk lamp,
# which looked lovely and was another coordinate pinned to one painting; this
# version assumes nothing except that the room has air in it.

image mmfx_dust_0:
    Solid("#fff0d6")
    subpixel True
    additive 1.0
    xysize (2, 2)
    alpha 0.04

image mmfx_dust_1:
    Solid("#fff0d6")
    subpixel True
    additive 1.0
    xysize (2, 2)
    alpha 0.08

image mmfx_dust_2:
    Solid("#fff3de")
    subpixel True
    additive 1.0
    xysize (3, 3)
    alpha 0.13

image mmfx_dust_3:
    Solid("#fff6e6")
    subpixel True
    additive 1.0
    xysize (3, 3)
    alpha 0.18

image mmfx_dust_4:
    Solid("#fffaf0")
    subpixel True
    additive 1.0
    xysize (4, 4)
    alpha 0.24


init python:
    import math as _enter_m_mmfx_math

    class EnterMMenuDust(object):
        """A small deterministic mote field over the visible room.

        Motion is derived from the SpriteManager's own st, so the field has no
        state to desync and no dependence on frame rate. The seed drives a
        local LCG: building the field must never advance Matsu'Py's
        rollback-aware global RNG.
        """

        def __init__(self, children, count, seed, bounds, vy, vx, amp, speed):

            self.children = list(children)
            self.x0, self.y0, self.x1, self.y1 = [float(v) for v in bounds]
            self.span_x = max(self.x1 - self.x0, 1.0)
            self.span_y = max(self.y1 - self.y0, 1.0)
            self.vy = float(vy)
            self.vx = float(vx)
            self.amp = float(amp)
            self.speed = float(speed)
            self.parts = []
            self.manager = SpriteManager(
                update=self.update,
                ignore_time=True)

            # THE FIELD DOES NOT DRAW WITHOUT THIS LINE. Measured on 8.6.0
            # gl2, September 2026, after the field had been silently invisible
            # for some time.
            #
            # SpriteManager sets `_duplicatable = True`, and its `_duplicate()`
            # copies the update, event and predict functions into a BRAND NEW
            # manager -- and nothing else. Not `children`, which is where every
            # sprite lives. So the moment a screen `add`s one, the engine
            # duplicates it and draws the duplicate: a manager with an empty
            # sprite list. No exception, no lint warning, no missing-image
            # placeholder. Just nothing, on a transparent layer, which is
            # indistinguishable from a field tuned too dim to see.
            #
            # Proven rather than reasoned: 24 sprites of 8x8 over a flat plate
            # rendered 0 changed pixels with the flag left alone and exactly
            # 1536 (24 * 64) with it cleared. Bare managers, custom update
            # functions and mesh-wrapped children all rendered nothing; only
            # the flag mattered.
            #
            # Clearing it is also what these fields actually want. Both callers
            # build ONE manager and reuse it for the life of the process (see
            # mmfx_dust_field below, and vault_fx.rpy's three), so per-use
            # duplication was never the intent. The update function derives
            # every position from `st` alone and keeps no state, so sharing one
            # manager between two screens on screen at once is safe: each pass
            # recomputes the same positions from the same clock.
            self.manager._duplicatable = False

            _enter_m_state = int(seed) & 0xffffffff

            def _enter_m_next():
                # Numerical Recipes LCG, local state.
                nonlocal _enter_m_state
                _enter_m_state = (
                    1664525 * _enter_m_state + 1013904223) & 0xffffffff
                return _enter_m_state / 4294967296.0

            for _enter_m_i in range(int(count)):
                _enter_m_sprite = self.manager.create(self.children[0])
                _enter_m_sprite.x = self.x0 + _enter_m_next() * self.span_x
                _enter_m_sprite.y = self.y0 + _enter_m_next() * self.span_y
                self.parts.append([
                    _enter_m_sprite,
                    _enter_m_sprite.x,                       # x0
                    _enter_m_sprite.y,                       # y0
                    self.vx * (0.55 + _enter_m_next() * 0.90),
                    self.vy * (0.70 + _enter_m_next() * 0.60),
                    _enter_m_next() * 6.28318530718,         # sway phase
                    self.speed * (0.70 + _enter_m_next() * 0.60),
                    _enter_m_next() * 6.28318530718,         # twinkle phase
                    0.16 + _enter_m_next() * 0.34,           # twinkle rate
                    0.35 + _enter_m_next() * 0.65,           # how near it is
                    -1,                                      # current child
                ])

        def update(self, st):
            _enter_m_top = len(self.children) - 1

            for _enter_m_p in self.parts:
                (_enter_m_sprite, _enter_m_px0, _enter_m_py0, _enter_m_vx,
                    _enter_m_vy, _enter_m_sway, _enter_m_sp, _enter_m_tph,
                    _enter_m_tr, _enter_m_near, _enter_m_cur) = _enter_m_p

                _enter_m_y = self.y0 + (
                    (_enter_m_py0 - self.y0 + _enter_m_vy * st) % self.span_y)
                _enter_m_x = self.x0 + (
                    (_enter_m_px0 - self.x0 + _enter_m_vx * st +
                        self.amp * _enter_m_mmfx_math.sin(
                            st * _enter_m_sp + _enter_m_sway))
                    % self.span_x)

                _enter_m_sprite.x = _enter_m_x
                _enter_m_sprite.y = _enter_m_y

                # Brightness is depth times a slow twinkle -- nothing spatial,
                # so the field does not care what is painted behind it.
                _enter_m_b = _enter_m_near * (0.55 + 0.45 *
                    _enter_m_mmfx_math.sin(st * _enter_m_tr + _enter_m_tph))
                _enter_m_idx = int(_enter_m_b * (_enter_m_top + 0.999))
                if _enter_m_idx < 0:
                    _enter_m_idx = 0
                elif _enter_m_idx > _enter_m_top:
                    _enter_m_idx = _enter_m_top

                if _enter_m_idx != _enter_m_cur:
                    _enter_m_sprite.set_child(self.children[_enter_m_idx])
                    _enter_m_p[10] = _enter_m_idx

            return 1.0 / 30.0

    _MMFX_DUST_FIELD = [None]

    def mmfx_dust_field():
        """The mote field, built once and reused for the life of the process."""

        if _MMFX_DUST_FIELD[0] is None:
            _MMFX_DUST_FIELD[0] = EnterMMenuDust(
                children=(
                    "mmfx_dust_0", "mmfx_dust_1", "mmfx_dust_2",
                    "mmfx_dust_3", "mmfx_dust_4"),
                count=34,
                seed=0x4d4d4658,
                bounds=(MMFX_ROOM_X - 40.0, 60.0, 1320.0, 700.0),
                vy=4.6, vx=1.8, amp=19.0, speed=0.40).manager

        return _MMFX_DUST_FIELD[0]


# -----------------------------------------------------------------------------
# 6. VIGNETTE + GRAIN
# -----------------------------------------------------------------------------
# Borrowed wholesale from the story's atmosphere layer -- same shader parts,
# menu-tuned uniforms. fill and key are BOTH ZERO here: the lo-fi grade already
# owns the light, and the one rule that layer learned the hard way is that
# added light costs colour. What is left is a vignette (which darkens, so it
# costs no colour and gains contrast) and, at Full, the signed grain that keeps
# a flat digital painting from reading as a flat digital painting.
#
# These two are SCREEN-LOCKED, outside the camera: a vignette and film grain
# belong to the lens, not to the room, and would give the whole trick away if
# they slid about with the picture.
init -8 python:

    _MMFX_GRADE_BASE = dict(
        u_em_atmos_vig_strength=0.26,
        u_em_atmos_vig_inner=0.58,
        u_em_atmos_vig_outer=1.12,
        u_em_atmos_vig_tint=(0.016, 0.020, 0.038),
        u_em_atmos_key_pos=(0.68, 0.42),
        u_em_atmos_key_col=(1.0, 0.78, 0.48),
        u_em_atmos_fill_top=(0.50, 0.56, 0.70),
        u_em_atmos_fill_bottom=(0.20, 0.24, 0.34),
        u_em_atmos_fill_amt=0.0,
        u_em_atmos_key_amt=0.0,
        u_em_atmos_key_size=0.62,
        u_em_atmos_key_softness=0.70)

    def _enter_m_mmfx_grade(_enter_m_grain):
        _enter_m_kw = dict(_MMFX_GRADE_BASE)
        _enter_m_kw.update(
            mesh=True,
            shader=(("enter_m.atmos_static", "enter_m.atmos_grain")
                if _enter_m_grain else "enter_m.atmos_static"))

        if _enter_m_grain:
            _enter_m_kw.update(
                u_em_atmos_grain=0.013,
                u_em_atmos_grain_rate=15.0,
                u_em_atmos_pulse=0.0,
                u_em_atmos_pulse_rate=1.0)

        return Transform(
            Solid("#00000000", xysize=(
                config.screen_width, config.screen_height)),
            **_enter_m_kw)

    MMFX_GRADE_FULL = _enter_m_mmfx_grade(True)
    MMFX_GRADE_LIGHT = _enter_m_mmfx_grade(False)


# -----------------------------------------------------------------------------
# 7. THE ROOM, ASSEMBLED
# -----------------------------------------------------------------------------
# The camera wraps the graded picture, the air drifts inside the camera with
# it, and the lens effects sit outside where they cannot be panned around.
screen mmfx_room_layer():

    python:
        _mmfx_alive = mmfx_alive()
        _mmfx_lit = mmfx_lit()

        _mmfx_camera_at = [mm_room_bg_arrive,
            mmfx_room_camera if _mmfx_alive else mmfx_room_still]
        _mmfx_grade = mmfx_lofi if _mmfx_alive else mmfx_lofi_still

    fixed:
        xysize (config.screen_width, config.screen_height)
        at _mmfx_camera_at

        if _mmfx_lit and _mmfx_alive:
            # Full: the rings turn, each at its own pace, under the grade --
            # the grade wraps the whole scene, so halation lights the gold
            # wherever it has turned to.
            fixed:
                xysize (config.screen_width, config.screen_height)
                at _mmfx_grade
                add "mmfx_title_field"
                add "mmfx_title_months" at mmfx_orrery_spin(360.0)
                add "mmfx_title_days" at mmfx_orrery_spin(-240.0)
                add "mmfx_title_orbits" at mmfx_orrery_spin(150.0)
        elif _mmfx_lit:
            add gui.main_menu_background at _mmfx_grade
        else:
            add gui.main_menu_background

        if _mmfx_lit:
            add mmfx_quad(300, 300) xpos 705 ypos 210 at (mmfx_orrery_glow if _mmfx_alive else mmfx_orrery_glow_still)

        if _mmfx_alive:
            add mmfx_dust_field()

    if _mmfx_lit:
        if _mmfx_alive:
            add mmfx_quad(680, 680) at mmfx_leak_drift
        add (MMFX_GRADE_FULL if _mmfx_alive else MMFX_GRADE_LIGHT)


# -----------------------------------------------------------------------------
# 8. THE SIDEBAR'S LIGHT
# -----------------------------------------------------------------------------
# Everything below is EVENT-DRIVEN and comes to rest. The marker slides when
# the selection moves and then stops; the glint crosses once per move and then
# stops. That is deliberate: the list is the part of this screen the player is
# actually reading, and a permanent animation under text is a permanent
# distraction from it.
#
# Both are rebuilt by a CHANGED ARGUMENT. A screen transform whose arguments
# are unchanged is the same object across executions, so the ATL keeps
# running from wherever it was; change one and Matsu'Py builds a new transform,
# take_state hands it the old pose, and the block plays again from there. That
# is the whole mechanism -- there is no event to hook, because hover/idle only
# reach a button's DIRECT child and these are not it.

# The marker inherits its ypos from the outgoing transform, so this eases FROM
# the old row TO the new one. No opening `ypos` statement: that would snap.
# `off` is the marker's own top edge relative to its row -- a 64px bloom plate
# and a 26px fallback bar do not hang from the same hook -- and it is constant
# per call site, so only `idx` ever forces the rebuild.
transform mmfx_row_marker(idx=0, off=-11):
    subpixel True
    easeout_cubic 0.22 ypos (MMFX_ROW_Y0 + idx * MMFX_ROW_PITCH + off)


# The entrance for the shader marker is a GAIN ramp, not an alpha one, and it
# lives in the same transform as the shader. Two reasons, both load-bearing:
# a mesh ignores its child's pixels entirely, so an `alpha` applied further in
# than the shader fades a transparent plate and changes nothing; and this
# transform takes no arguments, so it is never rebuilt and the ramp cannot
# replay every time the selection moves.
transform mmfx_marker_bloom:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_MARK_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 2.6
    u_em_mmfx_gain 0.0
    pause 0.34
    easeout 0.42 u_em_mmfx_gain 0.62


# The fallback marker has no shader to ramp, so it fades the ordinary way.
transform mmfx_marker_in:
    subpixel True
    alpha 0.0
    pause 0.34
    easeout 0.42 alpha 1.0


# The glint SNAPS to the new row and washes across it, against the marker,
# which slides. One thing arrives, one thing travels; if both travelled the
# move would read as a smear.
transform mmfx_row_glint(idx=0):
    mesh True
    shader "enter_m.mmfx_sweep"
    subpixel True
    u_em_mmfx_sweep_col MMFX_GLINT_COL
    u_em_mmfx_sweep_w 0.30
    u_em_mmfx_sweep_skew 0.34
    ypos (MMFX_ROW_Y0 + idx * MMFX_ROW_PITCH)
    u_em_mmfx_sweep -0.32
    u_em_mmfx_sweep_gain 0.0
    parallel:
        linear 0.08 u_em_mmfx_sweep_gain 0.46
        pause 0.20
        linear 0.44 u_em_mmfx_sweep_gain 0.0
    parallel:
        easeout_quad 0.74 u_em_mmfx_sweep 1.32


# A node riding the seam between the sidebar and the room. Both ends are
# derived from the seam's own span so the node cannot overshoot the rail, and
# the whole cycle is eight bars: 3s of rest, then a 4.6s fall, then 0.4s more
# rest to land it on the downbeat of the ninth.
transform mmfx_seam_scan:
    subpixel True
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_SEAM_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 2.2
    u_em_mmfx_gain 0.0
    ypos MMFX_SEAM_Y0
    block:
        pause 3.0
        parallel:
            linear 0.55 u_em_mmfx_gain 0.34
            pause 3.30
            linear 0.75 u_em_mmfx_gain 0.0
        parallel:
            ease 4.6 ypos (MMFX_SEAM_Y0 + MMFX_SEAM_H - MMFX_SEAM_NODE_H)
        ypos MMFX_SEAM_Y0
        pause 0.4
        repeat


transform mmfx_logo_halo:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_LOGO_COL
    u_em_mmfx_core 0.26
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 1.2
    u_em_mmfx_gain 0.30
    block:
        ease 16.0 u_em_mmfx_gain 0.46
        ease 16.0 u_em_mmfx_gain 0.28
        repeat


transform mmfx_logo_halo_still:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_LOGO_COL
    u_em_mmfx_core 0.26
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 1.2
    u_em_mmfx_gain 0.36


# Instant alpha steps with real pauses between them: two redraws a second and
# nothing in between, which is as close to free as a blinking thing gets. One
# second is also exactly one beat, which is the only place anything here is
# allowed to agree with the drums.
transform mmfx_caret_blink:
    alpha 1.0
    pause 0.62
    alpha 0.10
    pause 0.38
    repeat
