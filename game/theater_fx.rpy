# =============================================================================
# ENTER-M :: THEATER HOUSE LIGHTS  --  the cinema-only lighting shader
# -----------------------------------------------------------------------------
# Public story API (see the worked example at the bottom of this header):
#
#     $ theater_lights(0.55)             # house lights down to half
#     $ theater_lights(1.00, secs=2.4)   # ...and out; the film is running
#     $ theater_lights(0.00, secs=1.6)   # house lights up for the credits
#     $ theater_clear()                  # take the whole thing off
#
# WHAT IT DOES, AND WHY IT IS NOT IN atmosphere.rpy
#   atmosphere.rpy grades a scene: one preset, one look, held. This is the
#   opposite kind of effect -- it is a single location doing a single thing,
#   over time, once. The room goes dark AND the screen becomes the only light
#   source in it, which means the darkness has a hole in it that has to sit
#   exactly where the screen is drawn in mod_assets/bg/theater_inside.png. A
#   preset table cannot express "dark everywhere except this rectangle", and
#   nothing outside a movie theater would ever want it to.
#
#   It is not in fx.rpy for the reason stated in that file's header: fx.rpy is
#   deliberately shader-free, and a shader belongs to whatever owns it. Here
#   that owner is a place rather than a game mode, which is the only difference
#   from the per-addon fx layers.
#
# HOW THE LOOK IS BUILT  (one fragment pass, three terms)
#   room   A dark premultiplied layer over everything. Its alpha is highest far
#          from the screen and drops to nothing on the screen itself, so the
#          seats, walls and sconces go out while the plate stays lit.
#   spill  The same falloff, much wider and much softer: light from the screen
#          landing on the first rows, the aisle, and the people in them.
#   beat   The film's OWN brightness, which is the thing that actually sells it.
#          A cinema is never at a constant light level -- it swings a stop and a
#          half every time the movie cuts -- so `beat` rides on top of both
#          terms above and keeps the room breathing without ever flickering.
#
# WHY THE ANIMATION IS ATL AND NOT u_time
#   Because we already learned this one the expensive way (see the note in the
#   OP/menu work): a shader whose motion is keyed to ambient u_time only moves
#   while something ELSE is asking for redraws, so it stutters and then freezes
#   on any screen that goes quiet -- which a dialogue scene does, between every
#   single click. Animating the uniforms from ATL instead makes the transform
#   itself the thing requesting frames, so the beat is continuous by
#   construction. `u_time` appears nowhere below.
#
# WHERE IT SITS
#   Its own tag on the "cinematic" layer at zorder -10, above every sprite, so
#   Monika in the next seat goes dark with the room. The negative zorder keeps
#   room for anything that should sit OVER the dim on the same layer -- there
#   is nothing there today, but letterbox bars used to be at zorder 0 and a
#   rebuild will likely want them back. Dialogue, the calendar and the quick
#   menu are all
#   on "screens", which is above "cinematic", so none of them are touched.
#   `scene` clears "master" only, so this survives the cuts between beats of
#   the movie -- which is wanted; the film does not stop for the narration.
#   That also means it MUST be turned off on the way out. theater_clear() is
#   not optional politeness, it is how the lobby stops being dark.
#
# QUALITY
#   Honours persistent.enter_m_atmos_quality, evaluated when a call is made:
#     full  -> shader, with the beat animating
#     light -> shader, held at one brightness (no per-frame redraw)
#     off   -> no shader at all; a plain dark Solid ramps in its place
#   A quality change made mid-scene applies from the next call rather than
#   retroactively, which for a five-minute sequence is a trade worth taking
#   over rebuilding this as a ConditionSwitch.
#
# WORKED EXAMPLE  (May 18, and the shape any theater scene should follow)
#     scene bg theater_inside
#     $ theater_lights(0.55)              # ads; the room is already low
#     ...
#     $ theater_lights(1.00, secs=2.6)    # trailers end, the feature starts
#     ...
#     $ theater_lights(0.00, secs=1.8)    # credits, house lights up
#     $ theater_clear()
# =============================================================================


# -----------------------------------------------------------------------------
# 1. SHADER
# -----------------------------------------------------------------------------
# GLSL ES 1.00 only, matching atmosphere.rpy: no derivatives, no dynamic loops,
# every smoothstep with edge0 strictly below edge1, and every identifier
# prefixed because Matsu'Py 8.1.1 combines shader-part source into one scope.
init -10 python:

    def _enter_m_theater_register_shader():
        renpy.register_shader("enter_m.theater_room", variables="""
            uniform vec2  u_model_size;
            uniform float u_em_theater_dim;
            uniform float u_em_theater_spill;
            uniform float u_em_theater_beat;
            uniform vec4  u_em_theater_screen;
            uniform float u_em_theater_edge;
            uniform float u_em_theater_reach;
            uniform vec3  u_em_theater_dark;
            uniform vec3  u_em_theater_light;
            varying vec2  v_tex_coord;
        """, fragment_functions="""
            vec4 em_theater_over(vec4 em_theater_top, vec4 em_theater_bot) {
                return em_theater_top +
                    em_theater_bot * (1.0 - em_theater_top.a);
            }
        """, fragment_300="""
            vec2 em_theater_uv = v_tex_coord;
            float em_theater_aspect =
                u_model_size.x / max(u_model_size.y, 1.0);

            // Distance to the SCREEN RECTANGLE rather than to its centre: a
            // radial falloff from a point would put the brightest spot in the
            // middle of the plate and leave its corners as dark as the walls.
            // Zero everywhere inside the rectangle, growing outward from its
            // nearest edge, and aspect-corrected so the light does not turn
            // into an ellipse when the frame is not square.
            vec2 em_theater_delta =
                abs(em_theater_uv - u_em_theater_screen.xy) -
                u_em_theater_screen.zw;
            em_theater_delta.x *= em_theater_aspect;
            float em_theater_dist = length(max(em_theater_delta, vec2(0.0)));

            // Two falloffs off the same distance. `panel` is the plate plus a
            // hairline of bleed; `spill` is the throw across the room.
            float em_theater_panel = 1.0 - smoothstep(
                0.0, max(u_em_theater_edge, 0.001), em_theater_dist);
            float em_theater_spill = 1.0 - smoothstep(
                0.0, max(u_em_theater_reach, 0.002), em_theater_dist);

            // How bright the film happens to be right now reaches into the
            // room but never off the plate: the screen is lit even on a dark
            // frame, which is why `panel` is not multiplied by the beat here.
            float em_theater_lit = clamp(
                em_theater_panel +
                em_theater_spill * (0.30 + 0.70 * u_em_theater_beat) * 0.85,
                0.0, 1.0);

            // The room goes out. Slightly harder low in frame, where the seats
            // and the carpet are and where a real auditorium has no fixtures
            // at all once the house lights drop.
            float em_theater_floor = mix(
                1.06, 0.90, smoothstep(0.0, 1.0, em_theater_uv.y));
            float em_theater_room_a = clamp(
                u_em_theater_dim * em_theater_floor *
                (1.0 - em_theater_lit * 0.97),
                0.0, 0.97);
            vec4 em_theater_room = vec4(
                u_em_theater_dark * em_theater_room_a, em_theater_room_a);

            // ...and the screen light lands back on top of it. Weighted toward
            // the plate so the wash reads as coming FROM somewhere.
            float em_theater_wash_a = clamp(
                u_em_theater_spill * u_em_theater_beat *
                (em_theater_panel * 0.42 + em_theater_spill * 0.58),
                0.0, 0.62);
            vec4 em_theater_wash = vec4(
                u_em_theater_light * em_theater_wash_a, em_theater_wash_a);

            gl_FragColor = em_theater_over(em_theater_wash, em_theater_room);
        """)

    try:
        _enter_m_theater_register_shader()
        ENTER_M_THEATER_SHADER = True
    except Exception as _enter_m_theater_error:
        ENTER_M_THEATER_SHADER = False
        renpy.log("ENTER-M THEATER: shader registration failed: %r" %
            _enter_m_theater_error)


# -----------------------------------------------------------------------------
# 2. WHERE THE SCREEN IS
# -----------------------------------------------------------------------------
# Normalized (centre x, centre y, half width, half height), measured off
# mod_assets/bg/theater_inside.png. If that background is ever repainted, this
# is the one line to re-measure -- everything else is falloff maths that does
# not care where the rectangle sits.
#
# It does not need to be exact, and should not be made so. If a camera move is
# ever put back on this background the plate will drift by a few percent while
# the shader stays put; the falloffs are soft enough that a couple of percent
# of slip is invisible, and being roughly right beats being brittle.
define ENTER_M_THEATER_SCREEN_RECT = (0.575, 0.330, 0.222, 0.212)

# The bleed off the edge of the plate, and the throw into the room. Both in the
# same aspect-corrected units as the rect above.
define ENTER_M_THEATER_EDGE = 0.035
define ENTER_M_THEATER_REACH = 0.560

# Not black. A cinema at rest is a warm-neutral dark because the room is red
# and the exit signs never go off; true black reads as a rendering failure.
define ENTER_M_THEATER_DARK = (0.020, 0.016, 0.030)

# And not white. Cold, faintly blue-green, which is what a projector actually
# throws once the ambient warmth is gone.
define ENTER_M_THEATER_LIGHT = (0.72, 0.80, 0.96)

# How far `spill` gets to go at full darkness. Kept well under the dim so the
# room can never end up brighter with the lights off than with them on.
define ENTER_M_THEATER_SPILL = 0.34

# The deepest the room is allowed to go. 0.88 rather than 1.0 on purpose: at
# full opacity the sprites stop being readable, and a scene where you cannot
# see the person you are on a date with is not atmosphere, it is a bug report.
define ENTER_M_THEATER_DIM = 0.88


# -----------------------------------------------------------------------------
# 3. THE ANIMATED LAYERS
# -----------------------------------------------------------------------------
# `level` is the story-facing number: 0.0 is house lights up, 1.0 is the film
# running in the dark. Everything below converts it into the two uniforms that
# actually matter and ramps between the old value and the new one.

# Full quality. The dim/spill ramp and the beat loop are separate `parallel`
# branches, so the film keeps playing through a lights change instead of
# waiting politely for it to finish.
#
# The beat timings are the load-bearing part. They are long (0.7s to 2.6s),
# irregular, and never reach either end of the range -- that is a movie cutting
# between scenes. Anything faster is a fault in the projector, which is a
# completely different and much less pleasant effect.
transform enter_m_theater_room(level_from=0.0, level_to=1.0, secs=2.0):
    mesh True
    shader "enter_m.theater_room"
    u_em_theater_screen ENTER_M_THEATER_SCREEN_RECT
    u_em_theater_edge ENTER_M_THEATER_EDGE
    u_em_theater_reach ENTER_M_THEATER_REACH
    u_em_theater_dark ENTER_M_THEATER_DARK
    u_em_theater_light ENTER_M_THEATER_LIGHT
    u_em_theater_dim (ENTER_M_THEATER_DIM * level_from)
    u_em_theater_spill (ENTER_M_THEATER_SPILL * level_from)
    u_em_theater_beat 0.55
    parallel:
        easein_quad (secs) u_em_theater_dim (ENTER_M_THEATER_DIM * level_to)
    parallel:
        easein_quad (secs) u_em_theater_spill (ENTER_M_THEATER_SPILL * level_to)
    parallel:
        block:
            linear 1.10 u_em_theater_beat 0.84
            linear 2.60 u_em_theater_beat 0.38
            linear 0.70 u_em_theater_beat 0.66
            linear 1.90 u_em_theater_beat 0.30
            linear 0.90 u_em_theater_beat 0.78
            linear 2.20 u_em_theater_beat 0.46
            repeat

# Light quality. Identical geometry, one held brightness, and -- the entire
# point -- no repeating block, so the transform stops asking for frames the
# moment the ramp finishes.
transform enter_m_theater_room_still(level_from=0.0, level_to=1.0, secs=2.0):
    mesh True
    shader "enter_m.theater_room"
    u_em_theater_screen ENTER_M_THEATER_SCREEN_RECT
    u_em_theater_edge ENTER_M_THEATER_EDGE
    u_em_theater_reach ENTER_M_THEATER_REACH
    u_em_theater_dark ENTER_M_THEATER_DARK
    u_em_theater_light ENTER_M_THEATER_LIGHT
    u_em_theater_beat 0.58
    u_em_theater_dim (ENTER_M_THEATER_DIM * level_from)
    u_em_theater_spill (ENTER_M_THEATER_SPILL * level_from)
    parallel:
        easein_quad (secs) u_em_theater_dim (ENTER_M_THEATER_DIM * level_to)
    parallel:
        easein_quad (secs) u_em_theater_spill (ENTER_M_THEATER_SPILL * level_to)

# No-shader fallback: an honest dark wash with no hole in it for the screen.
# Less of a trick, still legibly "the lights went down".
transform enter_m_theater_flat(level_from=0.0, level_to=1.0, secs=2.0):
    alpha (0.62 * level_from)
    easein_quad (secs) alpha (0.62 * level_to)


# -----------------------------------------------------------------------------
# 4. STORY-FACING API
# -----------------------------------------------------------------------------
# The current level lives in a `default` and not in an init-python global. See
# the long note at the bottom of atmosphere.rpy for the full reasoning: a name
# that is only ever mutated in place never enters the store's changed set and
# is therefore never written into a save, so a player who saves halfway through
# the movie and loads it back would come in with the level reset to 0.0 and the
# next call would ramp the room UP out of a darkness it thinks isn't there.
default enter_m_theater_level = 0.0

init python:

    _ENTER_M_THEATER_TAG = "enter_m_theater_room"
    _ENTER_M_THEATER_LAYER = "cinematic"
    # Negative so anything added to this layer later sits over the dim.
    _ENTER_M_THEATER_ZORDER = -10

    def _enter_m_theater_quality():
        """'full' / 'light' / 'off', shared with the atmosphere setting."""
        quality = getattr(persistent, "enter_m_atmos_quality", "full")
        if quality not in ("full", "light", "off"):
            return "full"
        return quality

    def theater_lights(level, secs=2.0):
        """Ramp the auditorium to `level` over `secs`.

        0.0 is house lights up and 1.0 is the feature running in the dark;
        anything between is a real state a cinema sits in, and the one that
        matters is the half-light during the ads. The ramp always starts from
        wherever the room actually is, so calls chain without a jump and a
        change of mind mid-fade is a legal thing to write.
        """
        level = max(0.0, min(1.0, float(level)))
        secs = max(0.0, float(secs))

        level_from = float(store.enter_m_theater_level)
        store.enter_m_theater_level = level

        quality = _enter_m_theater_quality()
        shader_ok = (
            ENTER_M_THEATER_SHADER and renpy.display.render.models)

        if quality == "off" or not shader_ok:
            what = Solid(
                "#000000",
                xysize=(config.screen_width, config.screen_height))
            at_list = [enter_m_theater_flat(level_from, level, secs)]
        else:
            what = Solid(
                "#00000000",
                xysize=(config.screen_width, config.screen_height))
            builder = (
                enter_m_theater_room if quality == "full"
                else enter_m_theater_room_still)
            at_list = [builder(level_from, level, secs)]

        renpy.show(
            _ENTER_M_THEATER_TAG,
            what=what,
            at_list=at_list,
            layer=_ENTER_M_THEATER_LAYER,
            zorder=_ENTER_M_THEATER_ZORDER)

    def theater_clear():
        """Remove the overlay outright and forget the level.

        Call this on the way out of the auditorium. `scene` does not clear the
        cinematic layer, so without it the lobby, the street and everything
        after them stay lit by a projector that is two rooms away.
        """
        store.enter_m_theater_level = 0.0
        renpy.hide(_ENTER_M_THEATER_TAG, layer=_ENTER_M_THEATER_LAYER)
