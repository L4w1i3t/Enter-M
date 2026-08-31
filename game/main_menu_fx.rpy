# =============================================================================
# ENTER-M :: MAIN MENU AMBIENT LAYER  ("the room is still awake")
# -----------------------------------------------------------------------------
# The title screen is a painting of Matsuda's bedroom at blue hour. The art
# already owns its grade, so nothing in here re-lights the room -- every quad
# below ADDS light where the painting says a light source already is, and the
# only thing that actually moves is the amount. A lamp that breathes, a laptop
# that flickers, dust hanging in the one beam, four windows across the street
# that change their minds: the room is doing nothing, and it is doing it live.
#
# WHAT LIVES WHERE
#   main_menu_fx.rpy   (here)  the ROOM -- shaders, lights, dust, grade.
#   main_menu_room.rpy         the SIDEBAR -- list, marker, glint, caret.
#
# THE BUDGET, AND WHY IT IS A SETTING
#
#     Settings -> Graphics -> Atmosphere
#       Full   every loop below runs. The room breathes.
#       Light  the lights are drawn but HELD -- no loops, no dust, no grain.
#              The screen comes to rest.
#       Off    nothing here draws at all. The painting, as painted.
#
#   MEASURED, idle on the title screen (240Hz panel, developer build):
#     Full 228.1 fps   Light 238.1 fps   Off 239.3 fps
#   i.e. the whole layer -- eleven shader quads, thirty-eight motes, the drift
#   and the grain -- costs about 0.2ms a frame. The setting is there for the
#   same reason the story's is, not to buy back anything expensive.
#
#   THE PREDICTION WORRY DOES NOT APPLY HERE, AND IT WAS CHECKED RATHER THAN
#   ASSUMED (Aug 31 2026). The known trap is real -- a screen that wants a
#   frame at every instant never reaches an "expensive" idle frame, and that is
#   the only kind Matsu'Py preloads on -- so an ambient title screen ought to
#   make the next menu hitch harder. It does not, because NOTHING ASKS FOR
#   THOSE MENUS TO BE PREDICTED IN THE FIRST PLACE: `_predict_screen` holds
#   exactly ['main_menu'], and Arcade/Archive/Settings/Credits/Records are
#   never queued at any quality. Measured, after four seconds sitting on the
#   title screen, opening the Arcade cost:
#     Full 100.2ms    Light 92.9ms    Off 95.3ms
#   -- one measurement, three settings, no difference. A menu's first open is
#   paid on first open whatever this file is doing.
#
#   (The screens.rpy comment block about warming those menus is still correct
#   about why it was reverted. Nothing here touches config.periodic_callbacks,
#   _predict_screen, or any other global that gameplay also lives in, which is
#   the line the Aug 27 experiment crossed and why the boss fights lagged.)
#
#   Note Light and Off measure at the panel's full rate above only because the
#   developer build's DEV pill (dev_hub_pill_lamp) is a perpetual 1.2s loop of
#   its own -- in a shipping build nothing is left animating at either setting.
#
# HOUSE RULES OBSERVED HERE
#   * Every animated shader value is an ATL-interpolated UNIFORM, never the
#     ambient u_time. A running `linear`/`ease` asks for a redraw on every
#     frame it runs, so an effect pays for its own smoothness; a u_time effect
#     renders at whatever cadence the rest of the screen happens to produce
#     and freezes solid the moment the screen stops asking for frames.
#   * Every `shader=` has `mesh True` next to it. Without the mesh the
#     fragment program never runs and the quad draws NOTHING -- silently,
#     lint-clean, no exception.
#   * The light quads live INSIDE the drifting fixed, not on top of it. They
#     are glued to the pixels they are lighting; if the room moves 12px and
#     the lamp glow does not, the laptop pane peels off the laptop.
#   * Additive output is `vec4(col * a, 0.0)`: alpha zero, so gl2's
#     `src + dst * (1 - a)` is a pure add and the quad can only ever brighten.
#     Every falloff is forced to exactly zero before the plate edge, because a
#     mesh is clipped dead at its rectangle and a glow that is still lit at
#     the boundary is a visible box.
#
# COORDINATES are the background's own pixels (1280x720), measured off
# assets/gui/menu/main_menu_matsuda_evening.png. The sidebar covers x < 430,
# so nothing here is placed to the left of it.
# =============================================================================


# --- the room's light sources, as the painting has them ----------------------
define MMFX_LAMP_COL = (1.00, 0.74, 0.42)     # desk lamp, tungsten
define MMFX_SCREEN_COL = (0.40, 0.72, 1.00)   # the laptop's editor
define MMFX_WAVE_COL = (0.48, 0.86, 1.00)     # the waveform print
define MMFX_CITY_COL = (1.00, 0.68, 0.34)     # somebody else's kitchen

# --- the sidebar's own light -------------------------------------------------
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


# -----------------------------------------------------------------------------
# 1. SHADERS
# -----------------------------------------------------------------------------
# Three parts, one job each. All output premultiplied-additive (alpha 0), all
# stay inside GLSL ES 1.00, and every smoothstep has strictly ordered edges.
#
#   enter_m.mmfx_bloom   a soft radial light. Every lamp, spill and window.
#   enter_m.mmfx_pane    a soft-edged emissive rectangle with a scan band.
#                        The laptop screen -- a display, not a lamp.
#   enter_m.mmfx_sweep   a specular band travelling across a quad. The glint
#                        that crosses whichever menu row you are on.
init -10 python:

    def _enter_m_mmfx_register_shaders():

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

        renpy.register_shader("enter_m.mmfx_pane", variables="""
            uniform vec3  u_em_mmfx_pane_col;
            uniform float u_em_mmfx_pane_gain;
            uniform float u_em_mmfx_pane_scan;
            uniform float u_em_mmfx_pane_phase;
            uniform float u_em_mmfx_pane_soft;
            varying vec2  v_tex_coord;
        """, fragment_300="""
            vec2 em_mmfx_uv = v_tex_coord;
            float em_mmfx_s = clamp(u_em_mmfx_pane_soft, 0.02, 0.48);

            float em_mmfx_edge =
                smoothstep(0.0, em_mmfx_s, em_mmfx_uv.x) *
                (1.0 - smoothstep(1.0 - em_mmfx_s, 1.0, em_mmfx_uv.x)) *
                smoothstep(0.0, em_mmfx_s, em_mmfx_uv.y) *
                (1.0 - smoothstep(1.0 - em_mmfx_s, 1.0, em_mmfx_uv.y));

            // A slow horizontal banding, scrolled by u_..._phase. This is the
            // difference between "a blue rectangle" and "a screen that is on".
            float em_mmfx_band = 0.5 + 0.5 * sin(
                (em_mmfx_uv.y * 9.0 + u_em_mmfx_pane_phase) * 6.28318530718);
            float em_mmfx_scan = clamp(u_em_mmfx_pane_scan, 0.0, 1.0);

            float em_mmfx_a = clamp(
                max(u_em_mmfx_pane_gain, 0.0) * em_mmfx_edge *
                (1.0 - em_mmfx_scan + em_mmfx_scan * em_mmfx_band),
                0.0, 1.0);
            gl_FragColor = vec4(u_em_mmfx_pane_col * em_mmfx_a, 0.0);
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
# One dial, already in Settings, already understood by the player: Atmosphere.
# The title screen reads it the same way the story does -- Full animates,
# Light holds, Off abstains -- so a machine that cannot afford a live menu is
# fixed in the same place a machine that cannot afford a live scene is.
init -9 python:

    def mmfx_level():
        """Full / Light / Off, as the Atmosphere preference has it."""

        _enter_m_q = getattr(persistent, "enter_m_atmos_quality", "full")
        if _enter_m_q not in ("full", "light", "off"):
            return "full"
        return _enter_m_q

    def mmfx_lit():
        """True when the additive light layer can actually be drawn.

        Off opts out; so does a machine with no model renderer, or a driver
        that refused the shader source. In every one of those cases the room
        simply looks the way the painting looks, which is already finished.
        """

        return (mmfx_level() != "off"
            and ENTER_M_MMFX_SHADERS
            and renpy.display.render.models)

    def mmfx_alive():
        """True when the ambient loops may run: breath, dust, drift, grain."""

        return mmfx_level() == "full"


init python:

    @renpy.pure
    def mmfx_quad(w, h):
        """A transparent plate for a shader to paint light onto."""

        return Solid("#00000000", xysize=(int(w), int(h)))


# -----------------------------------------------------------------------------
# 3. THE ROOM'S OWN MOTION
# -----------------------------------------------------------------------------
# A very slow push around the frame. This is the single cheapest thing that
# stops a painting reading as a screenshot, and it is why the light quads live
# inside this transform rather than over it -- the whole room, glows included,
# is one moving object.
#
# zoom 1.028 buys 17.9px of overscan per side at 1280 wide, so the +/-12px of
# travel never exposes an edge.
transform mmfx_room_breathe:
    subpixel True
    zoom 1.028
    xalign 0.5
    yalign 0.5
    block:
        ease 21.0 xoffset -12 yoffset 7
        ease 23.0 xoffset 11 yoffset -6
        repeat


transform mmfx_room_still:
    subpixel True
    zoom 1.028
    xalign 0.5
    yalign 0.5


# -----------------------------------------------------------------------------
# 4. THE LIGHTS
# -----------------------------------------------------------------------------
# Held variants first: Light quality wants the lamp lit, not the lamp alive.
transform mmfx_bloom_still(col=(1.0, 1.0, 1.0), gain=0.2, core=0.0, edge=1.0, fall=2.0):
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col col
    u_em_mmfx_gain gain
    u_em_mmfx_core core
    u_em_mmfx_edge edge
    u_em_mmfx_fall fall


transform mmfx_pane_still(col=(1.0, 1.0, 1.0), gain=0.2, scan=0.3, soft=0.24):
    mesh True
    shader "enter_m.mmfx_pane"
    u_em_mmfx_pane_col col
    u_em_mmfx_pane_gain gain
    u_em_mmfx_pane_scan scan
    u_em_mmfx_pane_soft soft
    u_em_mmfx_pane_phase 0.0


# The bulb. Long uneven breaths -- no two legs the same length, so the eye
# never finds the loop -- and once every ~21s the filament stumbles. The
# stumble is four near-instant steps, not an ease: a flicker that eases is a
# dimmer, and a bedside lamp does not have one.
transform mmfx_lamp_bulb:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_LAMP_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 0.94
    u_em_mmfx_fall 2.4
    u_em_mmfx_gain 0.26
    block:
        ease 3.6 u_em_mmfx_gain 0.310
        ease 4.2 u_em_mmfx_gain 0.238
        ease 3.0 u_em_mmfx_gain 0.284
        ease 5.4 u_em_mmfx_gain 0.252
        linear 0.05 u_em_mmfx_gain 0.150
        linear 0.06 u_em_mmfx_gain 0.295
        linear 0.04 u_em_mmfx_gain 0.192
        linear 0.10 u_em_mmfx_gain 0.262
        ease 4.6 u_em_mmfx_gain 0.300
        repeat


# The pool the bulb throws onto the wall and the desk. Deliberately out of
# phase with the bulb and much lower: this is bounce, and bounce is slower to
# answer than the source.
transform mmfx_lamp_pool:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_LAMP_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 2.0
    u_em_mmfx_gain 0.085
    block:
        ease 5.2 u_em_mmfx_gain 0.106
        ease 6.4 u_em_mmfx_gain 0.072
        ease 4.1 u_em_mmfx_gain 0.094
        repeat


# The laptop. Two concurrent branches on DISJOINT properties -- phase scrolls
# the scan band, gain does the content flicker -- because two branches touching
# the same property fight over it and the loser's value is simply gone.
transform mmfx_laptop_pane:
    mesh True
    shader "enter_m.mmfx_pane"
    u_em_mmfx_pane_col MMFX_SCREEN_COL
    u_em_mmfx_pane_soft 0.26
    u_em_mmfx_pane_scan 0.30
    u_em_mmfx_pane_phase 0.0
    u_em_mmfx_pane_gain 0.19
    parallel:
        linear 9.0 u_em_mmfx_pane_phase 1.0
        u_em_mmfx_pane_phase 0.0
        repeat
    parallel:
        ease 1.9 u_em_mmfx_pane_gain 0.230
        ease 1.3 u_em_mmfx_pane_gain 0.168
        ease 2.6 u_em_mmfx_pane_gain 0.212
        linear 0.08 u_em_mmfx_pane_gain 0.268
        linear 0.12 u_em_mmfx_pane_gain 0.178
        ease 2.2 u_em_mmfx_pane_gain 0.198
        repeat


transform mmfx_laptop_spill:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_SCREEN_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 2.2
    u_em_mmfx_gain 0.055
    block:
        ease 3.1 u_em_mmfx_gain 0.071
        ease 2.4 u_em_mmfx_gain 0.047
        ease 3.8 u_em_mmfx_gain 0.062
        repeat


# The waveform print. It is paper, so it does not emit -- what breathes here
# is lamp light sitting on a glossy surface, which is why the rhythm is the
# lamp's kind of slow and not a music visualiser's kind of fast.
transform mmfx_poster_wave:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_WAVE_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 1.8
    u_em_mmfx_gain 0.060
    block:
        ease 2.3 u_em_mmfx_gain 0.128
        ease 2.9 u_em_mmfx_gain 0.045
        ease 1.7 u_em_mmfx_gain 0.098
        ease 3.3 u_em_mmfx_gain 0.055
        repeat


# A window across the street. The `pause` legs are the point: nothing is
# moving during them, so each costs ONE scheduled redraw instead of one per
# frame, and four windows on four different periods never sync up.
transform mmfx_window_light(peak=0.30, up=1.6, hold=9.0, down=2.4, dark=13.0, delay=0.0):
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_CITY_COL
    u_em_mmfx_core 0.0
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 1.7
    u_em_mmfx_gain 0.0
    pause delay
    block:
        ease up u_em_mmfx_gain peak
        pause hold
        ease down u_em_mmfx_gain 0.0
        pause dark
        repeat


# -----------------------------------------------------------------------------
# 5. DUST
# -----------------------------------------------------------------------------
# Dust with no beam to hang in is just noise on the screen, so brightness here
# is a FUNCTION OF DISTANCE to the lamp pool: a mote is only visible while it
# is passing through the light, and the far corners of the room stay empty.
# Five pre-made children and set_child() rather than thirty alpha tweens -- a
# Sprite has x, y and zorder, and nothing else to animate.

image mmfx_dust_0:
    Solid("#fff0d6")
    subpixel True
    additive 1.0
    xysize (2, 2)
    alpha 0.05

image mmfx_dust_1:
    Solid("#fff0d6")
    subpixel True
    additive 1.0
    xysize (2, 2)
    alpha 0.11

image mmfx_dust_2:
    Solid("#fff3de")
    subpixel True
    additive 1.0
    xysize (3, 3)
    alpha 0.18

image mmfx_dust_3:
    Solid("#fff6e6")
    subpixel True
    additive 1.0
    xysize (3, 3)
    alpha 0.26

image mmfx_dust_4:
    Solid("#fffaf0")
    subpixel True
    additive 1.0
    xysize (4, 4)
    alpha 0.34


init python:
    import math as _enter_m_mmfx_math

    class EnterMMenuDust(object):
        """A small deterministic mote field confined to the visible room.

        Motion is derived from the SpriteManager's own st, so the field has no
        state to desync and no dependence on frame rate. The seed drives a
        local LCG: building the field must never advance Matsu'Py's
        rollback-aware global RNG.
        """

        def __init__(self, children, count, seed, bounds, vy, vx, amp,
                speed, lamp, radius):

            self.children = list(children)
            self.x0, self.y0, self.x1, self.y1 = [float(v) for v in bounds]
            self.span_x = max(self.x1 - self.x0, 1.0)
            self.span_y = max(self.y1 - self.y0, 1.0)
            self.vy = float(vy)
            self.vx = float(vx)
            self.amp = float(amp)
            self.speed = float(speed)
            self.lamp_x, self.lamp_y = [float(v) for v in lamp]
            self.radius = max(float(radius), 1.0)
            self.parts = []
            self.manager = SpriteManager(
                update=self.update,
                ignore_time=True)

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
                    0.55 + _enter_m_next() * 0.75,           # twinkle rate
                    -1,                                      # current child
                ])

        def update(self, st):
            _enter_m_top = len(self.children) - 1

            for _enter_m_p in self.parts:
                (_enter_m_sprite, _enter_m_px0, _enter_m_py0, _enter_m_vx,
                    _enter_m_vy, _enter_m_sway, _enter_m_sp, _enter_m_tph,
                    _enter_m_tr, _enter_m_cur) = _enter_m_p

                _enter_m_y = self.y0 + (
                    (_enter_m_py0 - self.y0 + _enter_m_vy * st) % self.span_y)
                _enter_m_x = self.x0 + (
                    (_enter_m_px0 - self.x0 + _enter_m_vx * st +
                        self.amp * _enter_m_mmfx_math.sin(
                            st * _enter_m_sp + _enter_m_sway))
                    % self.span_x)

                _enter_m_sprite.x = _enter_m_x
                _enter_m_sprite.y = _enter_m_y

                # How much of the lamp's light is falling on this mote. The
                # y radius is tighter than the x radius because the pool on
                # the desk is wider than it is deep.
                _enter_m_dx = (_enter_m_x - self.lamp_x) / self.radius
                _enter_m_dy = (_enter_m_y - self.lamp_y) / (self.radius * 0.72)
                _enter_m_lit = 1.0 - min(
                    _enter_m_mmfx_math.sqrt(
                        _enter_m_dx * _enter_m_dx + _enter_m_dy * _enter_m_dy),
                    1.0)
                _enter_m_lit = _enter_m_lit ** 1.3

                _enter_m_b = _enter_m_lit * (0.55 + 0.45 *
                    _enter_m_mmfx_math.sin(st * _enter_m_tr + _enter_m_tph))
                _enter_m_idx = int(_enter_m_b * (_enter_m_top + 0.999))
                if _enter_m_idx < 0:
                    _enter_m_idx = 0
                elif _enter_m_idx > _enter_m_top:
                    _enter_m_idx = _enter_m_top

                if _enter_m_idx != _enter_m_cur:
                    _enter_m_sprite.set_child(self.children[_enter_m_idx])
                    _enter_m_p[9] = _enter_m_idx

            return 1.0 / 30.0

    _MMFX_DUST_FIELD = [None]

    def mmfx_dust_field():
        """The mote field, built once and reused for the life of the process."""

        if _MMFX_DUST_FIELD[0] is None:
            # BOUNDS ARE THE BEAM, NOT THE ROOM. Spread over the whole visible
            # room, thirty motes put barely one inside the lamp's falloff at
            # any moment and the field read as empty -- measured on the first
            # pass. Confined to the desk, the same thirty-eight are ~16 lit at
            # once, and because the falloff is already zero at every edge of
            # this box, a mote wrapping around it is invisible.
            _MMFX_DUST_FIELD[0] = EnterMMenuDust(
                children=(
                    "mmfx_dust_0", "mmfx_dust_1", "mmfx_dust_2",
                    "mmfx_dust_3", "mmfx_dust_4"),
                count=38,
                seed=0x4d4d4658,
                bounds=(620.0, 180.0, 1140.0, 580.0),
                vy=4.6, vx=1.8, amp=19.0, speed=0.40,
                lamp=(858.0, 372.0), radius=290.0).manager

        return _MMFX_DUST_FIELD[0]


# -----------------------------------------------------------------------------
# 6. GRADE
# -----------------------------------------------------------------------------
# Borrowed wholesale from the story's atmosphere layer -- same shader parts,
# menu-tuned uniforms. fill and key are BOTH ZERO here: the painting is already
# lit, and the one rule that layer learned the hard way is that added light
# costs colour. What is left is a vignette (which darkens, so it costs no
# colour and gains contrast) and, at Full, the signed grain that keeps a flat
# digital painting from reading as a flat digital painting.
init -8 python:

    _MMFX_GRADE_BASE = dict(
        u_em_atmos_vig_strength=0.24,
        u_em_atmos_vig_inner=0.60,
        u_em_atmos_vig_outer=1.12,
        u_em_atmos_vig_tint=(0.018, 0.024, 0.044),
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
                u_em_atmos_grain=0.011,
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
# Draw order is the physical one: the painting, then the light already in it,
# then the air, then the glass the whole thing is being watched through. The
# grade is the only part left OUTSIDE the drifting fixed -- a vignette belongs
# to the frame, not to the room.
screen mmfx_room_layer():

    python:
        _mmfx_alive = mmfx_alive()
        _mmfx_lit = mmfx_lit()

        _mmfx_room_at = [mm_room_bg_arrive,
            mmfx_room_breathe if _mmfx_alive else mmfx_room_still]

        # The held stand-ins carry the same base numbers as the animated
        # versions, so Light is this room with its breath held -- not a
        # dimmer, flatter one.
        _mmfx_lamp = (mmfx_lamp_bulb if _mmfx_alive
            else mmfx_bloom_still(MMFX_LAMP_COL, 0.26, 0.0, 0.94, 2.4))
        _mmfx_pool = (mmfx_lamp_pool if _mmfx_alive
            else mmfx_bloom_still(MMFX_LAMP_COL, 0.085, 0.0, 1.0, 2.0))
        _mmfx_screen = (mmfx_laptop_pane if _mmfx_alive
            else mmfx_pane_still(MMFX_SCREEN_COL, 0.19, 0.30, 0.26))
        _mmfx_spill = (mmfx_laptop_spill if _mmfx_alive
            else mmfx_bloom_still(MMFX_SCREEN_COL, 0.055, 0.0, 1.0, 2.2))
        _mmfx_wave = (mmfx_poster_wave if _mmfx_alive
            else mmfx_bloom_still(MMFX_WAVE_COL, 0.075, 0.0, 1.0, 1.8))

    fixed:
        xysize (config.screen_width, config.screen_height)
        at _mmfx_room_at

        add gui.main_menu_background

        if _mmfx_lit:

            # The desk lamp: bulb at (905, 300), and the pool it throws onto
            # the wall and across the desk, centred (850, 400).
            add mmfx_quad(160, 140) xpos 825 ypos 230 at _mmfx_lamp
            add mmfx_quad(440, 300) xpos 630 ypos 250 at _mmfx_pool

            # The laptop: the panel itself, then what it puts on the desk.
            add mmfx_quad(104, 82) xpos 980 ypos 334 at _mmfx_screen
            add mmfx_quad(300, 230) xpos 890 ypos 275 at _mmfx_spill

            # The waveform print, x 605..738, on its bright centre line.
            add mmfx_quad(170, 74) xpos 585 ypos 260 at _mmfx_wave

            # Four apartments across the street, on four different clocks.
            if _mmfx_alive:
                add mmfx_quad(26, 22) xpos 1021 ypos 266 at mmfx_window_light(0.30, 1.6, 9.0, 2.4, 13.0, 2.0)
                add mmfx_quad(26, 22) xpos 1125 ypos 276 at mmfx_window_light(0.24, 2.2, 15.0, 1.8, 8.0, 11.0)
                add mmfx_quad(24, 20) xpos 1236 ypos 225 at mmfx_window_light(0.34, 1.1, 6.0, 3.1, 19.0, 6.5)
                add mmfx_quad(22, 20) xpos 921 ypos 235 at mmfx_window_light(0.22, 2.8, 12.0, 2.6, 16.0, 17.0)

        if _mmfx_alive:
            add mmfx_dust_field()

    if _mmfx_lit:
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
# the 3.0s pause at the top of the loop is a genuine rest, not a slow move.
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
        repeat


# A halo has to survive the thing it is behind. The logo plate is 108px on a
# 210px quad, so everything inside r = 0.51 is hidden -- and a plain
# core 0 / fall 2.8 falloff has decayed to under 1% of its gain by then, which
# is why the first pass drew a halo that measured (9, 15, 14) against a (10,
# 19, 22) panel and could not be seen at all. `core` holds the light out to
# the plate's own edge before it starts falling.
transform mmfx_logo_halo:
    mesh True
    shader "enter_m.mmfx_bloom"
    u_em_mmfx_col MMFX_LOGO_COL
    u_em_mmfx_core 0.26
    u_em_mmfx_edge 1.0
    u_em_mmfx_fall 1.2
    u_em_mmfx_gain 0.30
    block:
        ease 4.4 u_em_mmfx_gain 0.46
        ease 5.8 u_em_mmfx_gain 0.28
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
# nothing in between, which is as close to free as a blinking thing gets.
transform mmfx_caret_blink:
    alpha 1.0
    pause 0.62
    alpha 0.10
    pause 0.44
    repeat
