# =============================================================================
# ENTER-M :: ATMOSPHERE / LIGHTING LAYER
# -----------------------------------------------------------------------------
# Public story API:
#
#     $ atmos("home")
#     $ atmos("night", particles="nightdrift")
#     $ atmos_hold()                         # backwards-compatible refresh
#     $ atmos_pressure()
#     $ atmos_pressure_clear()
#     $ atmos_clear()
#
# A master-layer scene callback restores the active base grade and particle
# field after every `scene`, so ordinary cuts no longer drop the atmosphere.
# Transient pressure is deliberately cleared by a scene change. Story calls to
# atmos_hold() remain valid, but are no longer required just to survive a cut.
#
# Authoring rules:
#   * Choose a new preset when time, place, or dramatic lighting changes.
#   * Saturation belongs to the preset table; story files do not set it alone.
#   * Ambient particles are opt-in, and the two fields are not interchangeable:
#       nightdrift  cold, blue, drifting -- OUTDOORS AT NIGHT only.
#       motes       warm cream dust, the kind you only see in a sunbeam. That
#                   makes it an INTERIOR field, for a room with a real key
#                   light in it: an afternoon classroom, the club room at four
#                   o'clock, a kitchen in the morning. It also reads as pollen
#                   outdoors in daylight, which is the one place it may go
#                   outside. Never at night, and never in a room whose preset
#                   has no direction to its light -- dust with no beam to hang
#                   in is just noise on the screen.
#     Both are opt-in per scene and neither is a default; a day with particles
#     in every shot has spent the effect.
#   * Call atmos_clear() before leaving an authored sequence for a assets/images/menu/tool.
#
# Quality is evaluated by ConditionSwitch at render time. This matters because
# Preferences runs in a copied Matsu'Py context: changing Full/Light/Off there now
# also changes the already-shown displayables in the gameplay context beneath
# it when that context renders again.
#
#   full  -> static lighting + animated signed grain + optional particles
#   light -> static lighting only
#   off   -> no grade, grain, or particles (authored saturation is retained)
#
# Shader registration catches malformed/unsupported registration paths. Actual
# driver compilation happens on first render, so it cannot honestly guarantee a
# recovery from every driver failure. ENTER-M otherwise requires the model/gl2
# renderer already used by the project's other effects.
# =============================================================================

default persistent.enter_m_atmos_quality = "full"


# -----------------------------------------------------------------------------
# 1. SHADER PARTS
# -----------------------------------------------------------------------------
# The static part performs three correctly premultiplied "over" composites:
# vertical ambient fill, a soft directional key, then the corner vignette. The
# grain part is separate, so Light does not merely hide particles -- it avoids
# u_time and the animated shader work entirely.
#
# All custom shader identifiers are prefixed. Matsu'Py 8.1.1 combines shader-part
# source into one scope and predates the newer l__ local-variable convention.
# The source stays within GLSL ES 1.00: no derivatives, dynamic loops, or newer
# syntax, and every smoothstep has ordered edges.
init -10 python:

    def _enter_m_atmos_register_shaders():
        renpy.register_shader("enter_m.atmos_static", variables="""
            uniform vec2  u_model_size;
            uniform float u_em_atmos_vig_strength;
            uniform float u_em_atmos_vig_inner;
            uniform float u_em_atmos_vig_outer;
            uniform vec3  u_em_atmos_vig_tint;
            uniform vec2  u_em_atmos_key_pos;
            uniform vec3  u_em_atmos_key_col;
            uniform vec3  u_em_atmos_fill_top;
            uniform vec3  u_em_atmos_fill_bottom;
            uniform float u_em_atmos_fill_amt;
            uniform float u_em_atmos_key_amt;
            uniform float u_em_atmos_key_size;
            uniform float u_em_atmos_key_softness;
            varying vec2  v_tex_coord;
        """, fragment_functions="""
            vec4 em_atmos_over(vec4 em_atmos_top, vec4 em_atmos_bottom) {
                return em_atmos_top + em_atmos_bottom * (1.0 - em_atmos_top.a);
            }
        """, fragment_300="""
            vec2 em_atmos_uv = v_tex_coord;
            float em_atmos_aspect = u_model_size.x / max(u_model_size.y, 1.0);

            // Ambient fill is gently brighter overhead. This establishes a
            // vertical light field even where the directional key does not hit.
            float em_atmos_fill_mix = smoothstep(0.0, 1.0, em_atmos_uv.y);
            vec3 em_atmos_fill_col = mix(
                u_em_atmos_fill_top,
                u_em_atmos_fill_bottom,
                em_atmos_fill_mix);
            float em_atmos_fill_a = clamp(
                u_em_atmos_fill_amt * mix(1.12, 0.82, em_atmos_fill_mix),
                0.0, 0.90);
            vec4 em_atmos_result = vec4(
                em_atmos_fill_col * em_atmos_fill_a,
                em_atmos_fill_a);

            // Key radius is aspect-correct, and softness is an explicit share
            // of that radius. edge0 is always strictly below edge1.
            vec2 em_atmos_key_delta = em_atmos_uv - u_em_atmos_key_pos;
            em_atmos_key_delta.x *= em_atmos_aspect;
            float em_atmos_key_dist = length(em_atmos_key_delta);
            float em_atmos_key_outer = max(u_em_atmos_key_size, 0.002);
            float em_atmos_key_width = max(
                em_atmos_key_outer * clamp(u_em_atmos_key_softness, 0.001, 1.0),
                0.001);
            float em_atmos_key_inner = max(
                em_atmos_key_outer - em_atmos_key_width,
                0.0);
            float em_atmos_key_mask = 1.0 - smoothstep(
                em_atmos_key_inner,
                em_atmos_key_outer,
                em_atmos_key_dist);
            float em_atmos_key_a = clamp(
                u_em_atmos_key_amt * em_atmos_key_mask,
                0.0, 0.90);
            vec4 em_atmos_key = vec4(
                u_em_atmos_key_col * em_atmos_key_a,
                em_atmos_key_a);
            em_atmos_result = em_atmos_over(em_atmos_key, em_atmos_result);

            // Aspect-correct vignette closes the physical corners rather than
            // stretching a circular falloff across the normalized texture.
            vec2 em_atmos_vig_delta = em_atmos_uv - vec2(0.5);
            em_atmos_vig_delta.x *= em_atmos_aspect;
            float em_atmos_vig_dist = length(em_atmos_vig_delta);
            float em_atmos_vig_outer = max(
                u_em_atmos_vig_outer,
                u_em_atmos_vig_inner + 0.001);
            float em_atmos_vig_a = smoothstep(
                u_em_atmos_vig_inner,
                em_atmos_vig_outer,
                em_atmos_vig_dist) * clamp(u_em_atmos_vig_strength, 0.0, 0.95);
            vec4 em_atmos_vig = vec4(
                u_em_atmos_vig_tint * em_atmos_vig_a,
                em_atmos_vig_a);
            gl_FragColor = em_atmos_over(em_atmos_vig, em_atmos_result);
        """)

        renpy.register_shader("enter_m.atmos_grain", variables="""
            uniform float u_time;
            uniform vec2  u_model_size;
            uniform float u_em_atmos_grain;
            uniform float u_em_atmos_grain_rate;
            uniform float u_em_atmos_pulse;
            uniform float u_em_atmos_pulse_rate;
            varying vec2  v_tex_coord;
        """, fragment_functions="""
            float em_atmos_igrad_hash(vec2 em_atmos_hash_p) {
                return fract(52.9829189 * fract(dot(
                    em_atmos_hash_p,
                    vec2(0.06711056, 0.00583715))));
            }
        """, fragment_320="""
            // Pressure/memory may breathe very slightly in Full. Scaling both
            // premultiplied RGB and alpha preserves the representation.
            float em_atmos_base_a = clamp(gl_FragColor.a, 0.0, 1.0);
            float em_atmos_pulse_scale = 1.0 +
                sin(u_time * u_em_atmos_pulse_rate) * u_em_atmos_pulse;
            float em_atmos_pulsed_a = clamp(
                em_atmos_base_a * em_atmos_pulse_scale,
                0.0, 0.98);
            float em_atmos_pulse_ratio = em_atmos_pulsed_a /
                max(em_atmos_base_a, 0.0001);
            gl_FragColor.rgb *= em_atmos_pulse_ratio;
            gl_FragColor.a = em_atmos_pulsed_a;

            // Quantized temporal phase prevents high-frequency shimmer. Signed
            // noise becomes a white or black premultiplied overlay, so bright
            // and dark grain affect RGB and alpha symmetrically and correctly.
            float em_atmos_tick = mod(floor(
                u_time * max(u_em_atmos_grain_rate, 1.0)), 127.0);
            vec2 em_atmos_pixel = floor(v_tex_coord * u_model_size);
            float em_atmos_noise = em_atmos_igrad_hash(
                em_atmos_pixel + vec2(
                    em_atmos_tick * 17.0,
                    em_atmos_tick * 43.0));
            float em_atmos_signed = (em_atmos_noise - 0.5) * 2.0;
            float em_atmos_grain_a = abs(em_atmos_signed) *
                clamp(u_em_atmos_grain, 0.0, 0.15);
            vec3 em_atmos_grain_rgb = vec3(
                em_atmos_grain_a * step(0.0, em_atmos_signed));
            vec4 em_atmos_grain_layer = vec4(
                em_atmos_grain_rgb,
                em_atmos_grain_a);
            gl_FragColor = em_atmos_grain_layer +
                gl_FragColor * (1.0 - em_atmos_grain_a);
        """)

    try:
        _enter_m_atmos_register_shaders()
        ENTER_M_ATMOS_SHADERS = True
    except Exception as _enter_m_atmos_shader_error:
        ENTER_M_ATMOS_SHADERS = False
        renpy.log("ENTER-M ATMOS: shader registration failed: %r" %
            _enter_m_atmos_shader_error)


# -----------------------------------------------------------------------------
# 2. PRESETS
# -----------------------------------------------------------------------------
# `fill` and `key` are independent opacity/energy controls. `ksoft` is the
# fraction of the key radius used for its falloff. `grate` is the Full-quality
# grain refresh rate; `pulse` is normally zero and remains subtle when enabled.
#
# THE GRADE ONLY ADDS LIGHT, AND ADDED LIGHT COSTS COLOUR.
#   This layer composites OVER the finished frame. It can never multiply or
#   pull a pixel down except by painting something darker on top of it, so
#   every point of `fill`/`key` alpha is paint -- and near-white paint is the
#   one kind that flattens a picture, because it lifts the black floor and
#   drags every hue toward its own. Measured over the shipped backgrounds, the
#   pre-2026-08-20 numbers (`home` at fill 0.075 + key 0.105 across a 0.76
#   radius, i.e. an 18% white veil over most of the frame) raised the
#   1st-percentile black from 0.109 to 0.151 and took 17% of the frame's
#   chroma with it -- while every one of those presets still declared
#   sat=1.00. The world read as drained a chapter and a half before the story
#   is supposed to drain it.
#
#   Mood is therefore bought in this order:
#     1. the VIGNETTE -- it darkens, so it costs no colour and gains contrast;
#     2. a CHROMATIC key -- a saturated warm or blue light tints the frame
#        where a white one only bleaches it;
#     3. fill/key alpha, last and sparingly.
#   Daylight presets live around fill 0.02-0.03 / key 0.03-0.05. Only a dark
#   room, where the fill IS the ambient light that makes the scene readable at
#   all, is allowed above that.
#
# Saturation grammar:
#   1.00  normal story colour
#   0.85  Chapter 4 winter
#   0.55  Chapter 5 January (present-tense floor)
#   0.12  reserved flashback/memory grammar
init -9 python:

    ATMOS_PRESETS = {
        #                 vignette                       key                         vertical ambient fill                         energy/shape                         animation             sat
        "home":           dict(vig=0.32, inner=0.52, outer=1.05, vtint=(0.030, 0.036, 0.058), kpos=(0.27, 0.21), kcol=(1.00, 0.88, 0.66), ftop=(0.86, 0.90, 1.00), fbottom=(0.40, 0.46, 0.62), fill=0.030, key=0.048, ksize=0.62, ksoft=0.70, grain=0.014, grate=16.0, pulse=0.000, prate=1.0, sat=1.00),
        "morning":        dict(vig=0.24, inner=0.60, outer=1.10, vtint=(0.026, 0.034, 0.052), kpos=(0.22, 0.18), kcol=(1.00, 0.94, 0.78), ftop=(0.88, 0.94, 1.00), fbottom=(0.52, 0.60, 0.72), fill=0.020, key=0.032, ksize=0.68, ksoft=0.75, grain=0.011, grate=15.0, pulse=0.000, prate=1.0, sat=1.00),
        "afternoon":      dict(vig=0.28, inner=0.56, outer=1.08, vtint=(0.036, 0.036, 0.050), kpos=(0.31, 0.19), kcol=(1.00, 0.93, 0.74), ftop=(0.90, 0.93, 1.00), fbottom=(0.48, 0.54, 0.68), fill=0.022, key=0.036, ksize=0.66, ksoft=0.74, grain=0.012, grate=15.0, pulse=0.000, prate=1.0, sat=1.00),
        "evening":        dict(vig=0.42, inner=0.46, outer=1.00, vtint=(0.070, 0.038, 0.034), kpos=(0.77, 0.27), kcol=(1.00, 0.62, 0.30), ftop=(0.60, 0.50, 0.60), fbottom=(0.22, 0.24, 0.36), fill=0.045, key=0.075, ksize=0.58, ksoft=0.66, grain=0.017, grate=16.0, pulse=0.000, prate=1.0, sat=1.00),
        "night":          dict(vig=0.54, inner=0.38, outer=0.96, vtint=(0.010, 0.016, 0.042), kpos=(0.50, 0.13), kcol=(0.44, 0.60, 1.00), ftop=(0.12, 0.20, 0.42), fbottom=(0.04, 0.07, 0.16), fill=0.058, key=0.048, ksize=0.66, ksoft=0.78, grain=0.024, grate=18.0, pulse=0.000, prate=1.0, sat=1.00),
        "home_night":     dict(vig=0.48, inner=0.43, outer=0.98, vtint=(0.026, 0.024, 0.052), kpos=(0.29, 0.20), kcol=(1.00, 0.72, 0.36), ftop=(0.24, 0.27, 0.40), fbottom=(0.08, 0.11, 0.21), fill=0.044, key=0.054, ksize=0.58, ksoft=0.68, grain=0.020, grate=17.0, pulse=0.000, prate=1.0, sat=1.00),
        "overcast":       dict(vig=0.38, inner=0.50, outer=1.04, vtint=(0.040, 0.046, 0.060), kpos=(0.50, 0.16), kcol=(0.74, 0.84, 1.00), ftop=(0.68, 0.77, 0.90), fbottom=(0.36, 0.44, 0.56), fill=0.029, key=0.024, ksize=0.80, ksoft=0.90, grain=0.015, grate=15.0, pulse=0.000, prate=1.0, sat=1.00),

        # This row is valid both as atmos("pressure") and as the independent
        # atmos_pressure() overlay. The transient helper intentionally ignores
        # this row's saturation; as a base preset it explicitly returns to 1.0.
        "pressure":       dict(vig=0.70, inner=0.25, outer=0.90, vtint=(0.014, 0.020, 0.052), kpos=(0.50, 0.46), kcol=(0.26, 0.36, 0.58), ftop=(0.09, 0.13, 0.26), fbottom=(0.02, 0.03, 0.08), fill=0.055, key=0.026, ksize=0.50, ksoft=0.82, grain=0.032, grate=18.0, pulse=0.035, prate=1.8, sat=1.00),

        # Late Act 1: one saturation baseline, three lighting conditions.
        "winter":         dict(vig=0.50, inner=0.41, outer=0.98, vtint=(0.026, 0.034, 0.058), kpos=(0.62, 0.14), kcol=(0.70, 0.83, 1.00), ftop=(0.52, 0.62, 0.80), fbottom=(0.22, 0.29, 0.42), fill=0.052, key=0.050, ksize=0.60, ksoft=0.62, grain=0.021, grate=16.0, pulse=0.000, prate=1.0, sat=0.85),
        "winter_dim":     dict(vig=0.60, inner=0.31, outer=0.94, vtint=(0.018, 0.024, 0.046), kpos=(0.50, 0.08), kcol=(0.54, 0.66, 0.86), ftop=(0.32, 0.40, 0.54), fbottom=(0.12, 0.17, 0.26), fill=0.062, key=0.040, ksize=0.55, ksoft=0.68, grain=0.027, grate=17.0, pulse=0.000, prate=1.0, sat=0.85),
        "winter_evening": dict(vig=0.56, inner=0.35, outer=0.95, vtint=(0.034, 0.024, 0.052), kpos=(0.76, 0.24), kcol=(0.94, 0.50, 0.30), ftop=(0.34, 0.37, 0.55), fbottom=(0.12, 0.15, 0.26), fill=0.058, key=0.050, ksize=0.60, ksoft=0.68, grain=0.025, grate=17.0, pulse=0.000, prate=1.0, sat=0.85),

        # Chapter 5 removes direction more than it removes light. Broad keys and
        # neutral fills make the space feel exposed instead of theatrically blue.
        "january":        dict(vig=0.58, inner=0.33, outer=0.96, vtint=(0.032, 0.032, 0.040), kpos=(0.50, 0.18), kcol=(0.72, 0.73, 0.77), ftop=(0.46, 0.48, 0.53), fbottom=(0.21, 0.23, 0.26), fill=0.050, key=0.024, ksize=0.96, ksoft=0.96, grain=0.031, grate=17.0, pulse=0.000, prate=1.0, sat=0.55),
        "january_night":  dict(vig=0.66, inner=0.25, outer=0.92, vtint=(0.012, 0.012, 0.020), kpos=(0.42, 0.24), kcol=(0.64, 0.60, 0.55), ftop=(0.22, 0.22, 0.24), fbottom=(0.07, 0.08, 0.11), fill=0.070, key=0.036, ksize=0.82, ksoft=0.90, grain=0.037, grate=18.0, pulse=0.000, prate=1.0, sat=0.55),

        # Reserved flashback grammar. No present-tense preset goes below 0.55.
        "memory":         dict(vig=0.72, inner=0.22, outer=0.88, vtint=(0.018, 0.018, 0.018), kpos=(0.50, 0.32), kcol=(0.90, 0.87, 0.80), ftop=(0.46, 0.45, 0.43), fbottom=(0.20, 0.20, 0.21), fill=0.072, key=0.046, ksize=0.98, ksoft=0.98, grain=0.046, grate=18.0, pulse=0.012, prate=1.1, sat=0.12),
    }

    # Registration/model-renderer fallback. This is intentionally simpler than
    # the shader look, but keeps the frame readable if the static part is not in
    # use. It is not a promise to catch first-render driver compilation errors.
    #
    # Same rule as the presets: a pale solid at a high alpha is a white veil
    # with no shape to justify it, so the light-coloured rows stay thin and the
    # dark rows -- which darken rather than bleach -- keep their weight.
    ATMOS_FALLBACK = {
        "home":           "#cdecc814",
        "morning":        "#ffe3a30d",
        "afternoon":      "#ffd88a0e",
        "evening":        "#d7864a1c",
        "night":          "#07163350",
        "home_night":     "#0a142d44",
        "overcast":       "#8fb0c916",
        "pressure":       "#101528aa",
        "winter":         "#5f7a9a2a",
        "winter_dim":     "#26303f5c",
        "winter_evening": "#30304f58",
        "january":        "#4a4b4e30",
        "january_night":  "#15161a60",
        "memory":         "#5a5a5a55",
    }


# -----------------------------------------------------------------------------
# 3. DYNAMIC BASE/PRESSURE DISPLAYABLES
# -----------------------------------------------------------------------------
init -8 python:

    _ATMOS_WIDTH = int(config.screen_width)
    _ATMOS_HEIGHT = int(config.screen_height)
    _ATMOS_SIZE = (_ATMOS_WIDTH, _ATMOS_HEIGHT)

    _ATMOS_REQUIRED_FIELDS = (
        "vig", "inner", "outer", "vtint", "kpos", "kcol", "ftop",
        "fbottom", "fill", "key", "ksize", "ksoft", "grain",
        "grate", "pulse", "prate", "sat")

    def _enter_m_atmos_validate_presets():
        for _enter_m_name, _enter_m_preset in ATMOS_PRESETS.items():
            _enter_m_missing = [
                _enter_m_key for _enter_m_key in _ATMOS_REQUIRED_FIELDS
                if _enter_m_key not in _enter_m_preset]
            if _enter_m_missing:
                raise Exception(
                    "ENTER-M ATMOS: preset %r is missing %s." %
                    (_enter_m_name, ", ".join(_enter_m_missing)))
            if not (0.0 <= _enter_m_preset["inner"] < _enter_m_preset["outer"]):
                raise Exception(
                    "ENTER-M ATMOS: preset %r has invalid vignette edges." %
                    _enter_m_name)
            if _enter_m_preset["ksize"] <= 0.0 or not (
                    0.0 < _enter_m_preset["ksoft"] <= 1.0):
                raise Exception(
                    "ENTER-M ATMOS: preset %r has invalid key geometry." %
                    _enter_m_name)
            if _enter_m_name != "memory" and _enter_m_preset["sat"] < 0.55:
                raise Exception(
                    "ENTER-M ATMOS: present-tense preset %r is below the saturation floor." %
                    _enter_m_name)
            if _enter_m_name not in ATMOS_FALLBACK:
                raise Exception(
                    "ENTER-M ATMOS: preset %r has no fallback colour." %
                    _enter_m_name)

    def _enter_m_atmos_shader_displayable(_enter_m_preset, _enter_m_animated):
        _enter_m_shader = (
            ("enter_m.atmos_static", "enter_m.atmos_grain")
            if _enter_m_animated else "enter_m.atmos_static")

        _enter_m_kwargs = dict(
            xysize=_ATMOS_SIZE,
            mesh=True,
            shader=_enter_m_shader,
            u_em_atmos_vig_strength=_enter_m_preset["vig"],
            u_em_atmos_vig_inner=_enter_m_preset["inner"],
            u_em_atmos_vig_outer=_enter_m_preset["outer"],
            u_em_atmos_vig_tint=_enter_m_preset["vtint"],
            u_em_atmos_key_pos=_enter_m_preset["kpos"],
            u_em_atmos_key_col=_enter_m_preset["kcol"],
            u_em_atmos_fill_top=_enter_m_preset["ftop"],
            u_em_atmos_fill_bottom=_enter_m_preset["fbottom"],
            u_em_atmos_fill_amt=_enter_m_preset["fill"],
            u_em_atmos_key_amt=_enter_m_preset["key"],
            u_em_atmos_key_size=_enter_m_preset["ksize"],
            u_em_atmos_key_softness=_enter_m_preset["ksoft"])

        if _enter_m_animated:
            _enter_m_kwargs.update(
                u_em_atmos_grain=_enter_m_preset["grain"],
                u_em_atmos_grain_rate=_enter_m_preset["grate"],
                u_em_atmos_pulse=_enter_m_preset["pulse"],
                u_em_atmos_pulse_rate=_enter_m_preset["prate"])

        return Transform(
            Solid("#00000000", xysize=_ATMOS_SIZE),
            **_enter_m_kwargs)

    def _enter_m_atmos_quality_switch(_enter_m_name, _enter_m_preset):
        _enter_m_full = _enter_m_atmos_shader_displayable(
            _enter_m_preset, True)
        _enter_m_light = _enter_m_atmos_shader_displayable(
            _enter_m_preset, False)
        _enter_m_fallback = Solid(
            ATMOS_FALLBACK[_enter_m_name],
            xysize=_ATMOS_SIZE)
        _enter_m_null = Null(
            width=_ATMOS_WIDTH,
            height=_ATMOS_HEIGHT)

        return ConditionSwitch(
            "persistent.enter_m_atmos_quality == 'full' and ENTER_M_ATMOS_SHADERS and renpy.display.render.models",
            _enter_m_full,
            "persistent.enter_m_atmos_quality == 'light' and ENTER_M_ATMOS_SHADERS and renpy.display.render.models",
            _enter_m_light,
            "persistent.enter_m_atmos_quality in ('full', 'light')",
            _enter_m_fallback,
            "True",
            _enter_m_null,
            predict_all=False)

    _enter_m_atmos_validate_presets()
    _ATMOS_GRADE_SWITCHES = {
        _enter_m_name: _enter_m_atmos_quality_switch(
            _enter_m_name, _enter_m_preset)
        for _enter_m_name, _enter_m_preset in ATMOS_PRESETS.items()
    }
    # A second instance lets atmos("pressure") and atmos_pressure() coexist
    # without sharing DynamicDisplayable timing/state.
    _ATMOS_PRESSURE_SWITCH = _enter_m_atmos_quality_switch(
        "pressure", ATMOS_PRESETS["pressure"])


# -----------------------------------------------------------------------------
# 4. DETERMINISTIC AMBIENT PARTICLES
# -----------------------------------------------------------------------------
# The field is local to this subsystem (no OP-addon dependency), uses fixed LCG
# seeds rather than the global random stream, derives motion from SpriteManager
# time, and retains floating-point positions for subpixel motion.

image enter_m_atmos_p_mote_small:
    Solid("#fff4d8")
    subpixel True
    xysize (2, 2)
    alpha 0.18

image enter_m_atmos_p_mote_medium:
    Solid("#fff7e8")
    subpixel True
    xysize (4, 4)
    alpha 0.12

image enter_m_atmos_p_night_small:
    Solid("#c9d8ff")
    subpixel True
    xysize (2, 2)
    alpha 0.15

image enter_m_atmos_p_night_medium:
    Solid("#aac5ff")
    subpixel True
    xysize (3, 3)
    alpha 0.11

init python:
    import math as _enter_m_atmos_math

    class EnterMAtmosDrift(object):
        """Low-count deterministic SpriteManager field for atmosphere only."""

        def __init__(self, children, count, seed, vy, vx, amp, speed):
            self.width = float(config.screen_width)
            self.height = float(config.screen_height)
            self.vy = float(vy)
            self.vx = float(vx)
            self.amp = float(amp)
            self.speed = float(speed)
            self.parts = []
            self.manager = SpriteManager(
                update=self.update,
                ignore_time=True)

            _enter_m_seed = int(seed) & 0xffffffff

            def _enter_m_next():
                # Numerical Recipes LCG. Local fixed state means constructing a
                # field never advances Matsu'Py's rollback-aware/global RNG.
                nonlocal _enter_m_seed
                _enter_m_seed = (
                    1664525 * _enter_m_seed + 1013904223) & 0xffffffff
                return _enter_m_seed / 4294967296.0

            for _enter_m_index in range(int(count)):
                _enter_m_child = children[
                    int(_enter_m_next() * len(children)) % len(children)]
                _enter_m_sprite = self.manager.create(_enter_m_child)
                _enter_m_x0 = _enter_m_next() * (self.width + 80.0) - 40.0
                _enter_m_y0 = _enter_m_next() * (self.height + 80.0) - 40.0
                _enter_m_phase = _enter_m_next() * 6.28318530718
                _enter_m_speed = self.speed * (0.70 + _enter_m_next() * 0.60)
                _enter_m_vy = self.vy * (0.72 + _enter_m_next() * 0.56)
                _enter_m_vx = self.vx * (0.55 + _enter_m_next() * 0.90)
                _enter_m_sprite.x = _enter_m_x0
                _enter_m_sprite.y = _enter_m_y0
                self.parts.append((
                    _enter_m_sprite,
                    _enter_m_x0,
                    _enter_m_y0,
                    _enter_m_vx,
                    _enter_m_vy,
                    _enter_m_phase,
                    _enter_m_speed))

        def update(self, st):
            _enter_m_span_y = self.height + 80.0
            _enter_m_span_x = self.width + 80.0

            for (_enter_m_sprite, _enter_m_x0, _enter_m_y0,
                    _enter_m_vx, _enter_m_vy, _enter_m_phase,
                    _enter_m_speed) in self.parts:
                _enter_m_y = ((_enter_m_y0 + _enter_m_vy * st) + 40.0) % \
                    _enter_m_span_y - 40.0
                _enter_m_x = ((_enter_m_x0 + _enter_m_vx * st +
                    self.amp * _enter_m_atmos_math.sin(
                        st * _enter_m_speed + _enter_m_phase)) + 40.0) % \
                    _enter_m_span_x - 40.0
                _enter_m_sprite.x = _enter_m_x
                _enter_m_sprite.y = _enter_m_y

            return 1.0 / 30.0

    # ONE table describes every particle field: the constructor reads it, and
    # _ATMOS_PARTICLE_VALUES (the public API's validator) is derived from its
    # keys. Previously the name list and the if/elif chain were two structures
    # that had to agree -- add a field to only one and you either got a public
    # API that rejected it or one that accepted it and then raised at show time.
    # Adding a field is now a single entry here.
    _ATMOS_FIELD_SPECS = {
        "nightdrift": dict(
            children=("enter_m_atmos_p_night_small", "enter_m_atmos_p_night_medium"),
            count=24, seed=0x4e494748, vy=6.5, vx=2.2, amp=15.0, speed=0.42),
        "motes": dict(
            children=("enter_m_atmos_p_mote_small", "enter_m_atmos_p_mote_medium"),
            count=22, seed=0x4d4f5445, vy=7.5, vx=2.6, amp=17.0, speed=0.50),
    }

    _ATMOS_FIELDS = {}
    _ATMOS_PARTICLE_SWITCHES = {}

    def _atmos_field(kind):
        if kind not in _ATMOS_FIELDS:
            spec = _ATMOS_FIELD_SPECS.get(kind)
            if spec is None:
                raise Exception(
                    "ENTER-M ATMOS: unknown particle field %r." % kind)
            spec = dict(spec)
            children = spec.pop("children")
            _ATMOS_FIELDS[kind] = EnterMAtmosDrift(children, **spec).manager

        return _ATMOS_FIELDS[kind]

    def _atmos_particle_switch(kind):
        if kind not in _ATMOS_PARTICLE_SWITCHES:
            _ATMOS_PARTICLE_SWITCHES[kind] = ConditionSwitch(
                "persistent.enter_m_atmos_quality == 'full'",
                _atmos_field(kind),
                "True",
                Null(width=_ATMOS_WIDTH, height=_ATMOS_HEIGHT),
                predict_all=False)
        return _ATMOS_PARTICLE_SWITCHES[kind]


# -----------------------------------------------------------------------------
# 4.5 MASTER-CAMERA SATURATION
# -----------------------------------------------------------------------------
# The procedural grade only draws over a frame, so preset saturation remains a
# separate matrix on the master layer. It now uses the CAMERA transform stack:
# unlike `show layer`, that stack survives `scene`, and it is independent of the
# regular master-layer transforms used by battle shakes and other authored FX.
# Screens/UI remain unaffected. Atmosphere quality deliberately does not disable
# story saturation.

transform atmos_sat_to(s0=1.0, s1=1.0, secs=0.0):
    matrixcolor SaturationMatrix(s0)
    linear secs matrixcolor SaturationMatrix(s1)


# -----------------------------------------------------------------------------
# 4.6 BACKGROUND-ONLY DRAIN
# -----------------------------------------------------------------------------
# Authored OOC effect: the background loses colour while cast sprites retain
# theirs. The start/end expressions have identical ColorMatrix structure, so
# Matsu'Py interpolates them safely. Mild contrast, cool tint, and brightness loss
# now support the drain without forcing the sequence below its saturation floor.
transform atmos_bg_drain(s0=1.0, s1=1.0, secs=40.0, zoom_to=1.06, zoom_secs=65.0):
    subpixel True
    align (0.5, 0.5)
    zoom 1.0
    matrixcolor SaturationMatrix(s0) * ContrastMatrix(1.00) * TintMatrix("#ffffff") * BrightnessMatrix(0.0)
    parallel:
        easein_quad secs matrixcolor SaturationMatrix(s1) * ContrastMatrix(1.04) * TintMatrix("#edf3ff") * BrightnessMatrix(-0.015)
    parallel:
        easein_quad zoom_secs zoom zoom_to


# -----------------------------------------------------------------------------
# 5. HELPER API AND LIFECYCLE
# -----------------------------------------------------------------------------
init python:

    _ATMOS_BASE_TAG = "enter_m_atmos_base"
    _ATMOS_PARTICLES_TAG = "enter_m_atmos_particles"
    _ATMOS_PRESSURE_TAG = "enter_m_atmos_pressure"
    _ATMOS_PARTICLE_Z_OFFSET = 6
    _ATMOS_QUALITY_VALUES = ("full", "light", "off")
    # Derived from the field table above -- the validator and the constructor
    # can no longer disagree about which fields exist.
    _ATMOS_PARTICLE_VALUES = tuple(sorted(_ATMOS_FIELD_SPECS))

    def _atmos_default_state():
        return {
            "preset": None,
            "particles": None,
            "zorder": 50,
            "sat": 1.0,
            "pressure_active": False,
            "pressure_zorder": 60,
        }

    # Pre-`default` fallback only, so the name always resolves even if something
    # touches it before the default statements run. The AUTHORITATIVE binding is
    # the `default _atmos_state` at the bottom of this file -- see the note there
    # before changing either of them.
    _atmos_state = _atmos_default_state()

    def _atmos_reject(message):
        _enter_m_message = "ENTER-M ATMOS: " + message
        if config.developer:
            raise Exception(_enter_m_message)
        renpy.log(_enter_m_message)

    def _atmos_quality():
        _enter_m_quality = getattr(
            persistent, "enter_m_atmos_quality", "full")
        if _enter_m_quality not in _ATMOS_QUALITY_VALUES:
            renpy.log(
                "ENTER-M ATMOS: invalid saved quality %r; using 'full'." %
                _enter_m_quality)
            _enter_m_quality = "full"
            persistent.enter_m_atmos_quality = _enter_m_quality
        return _enter_m_quality

    def _atmos_valid_zorder(value, label):
        try:
            return int(value)
        except (TypeError, ValueError, OverflowError):
            _atmos_reject("%s must be an integer, got %r." % (label, value))
            return None

    def _atmos_valid_secs(value):
        try:
            _enter_m_secs = float(value)
        except (TypeError, ValueError, OverflowError):
            _atmos_reject("secs must be a non-negative number, got %r." % value)
            return None
        if not _enter_m_atmos_math.isfinite(_enter_m_secs) or _enter_m_secs < 0.0:
            _atmos_reject("secs must be a finite non-negative number, got %r." % value)
            return None
        return _enter_m_secs

    def _atmos_hide_current_tags():
        renpy.hide(_ATMOS_BASE_TAG, layer="master")
        renpy.hide(_ATMOS_PARTICLES_TAG, layer="master")
        renpy.hide(_ATMOS_PRESSURE_TAG, layer="master")

    def _atmos_hide_legacy_tags():
        # Tags used by the original implementation and its fallback path.
        renpy.hide("atmos", layer="master")
        renpy.hide("atmosfx", layer="master")
        renpy.hide("atmos_pressure_fb", layer="master")

    def _atmos_show_base_and_particles():
        _enter_m_preset = _atmos_state.get("preset")
        if _enter_m_preset not in ATMOS_PRESETS:
            renpy.hide(_ATMOS_BASE_TAG, layer="master")
            renpy.hide(_ATMOS_PARTICLES_TAG, layer="master")
            return

        _enter_m_zorder = int(_atmos_state.get("zorder", 50))
        renpy.show(
            _ATMOS_BASE_TAG,
            what=_ATMOS_GRADE_SWITCHES[_enter_m_preset],
            layer="master",
            zorder=_enter_m_zorder)

        _enter_m_particles = _atmos_state.get("particles")
        if _enter_m_particles in _ATMOS_PARTICLE_VALUES:
            renpy.show(
                _ATMOS_PARTICLES_TAG,
                what=_atmos_particle_switch(_enter_m_particles),
                layer="master",
                zorder=_enter_m_zorder + _ATMOS_PARTICLE_Z_OFFSET)
        else:
            renpy.hide(_ATMOS_PARTICLES_TAG, layer="master")

    def _atmos_show_pressure_if_active():
        if _atmos_state.get("pressure_active", False):
            renpy.show(
                _ATMOS_PRESSURE_TAG,
                what=_ATMOS_PRESSURE_SWITCH,
                layer="master",
                zorder=int(_atmos_state.get("pressure_zorder", 60)))
        else:
            renpy.hide(_ATMOS_PRESSURE_TAG, layer="master")

    def _atmos_set_sat(to, secs=0.0):
        """Internal: update only the master CAMERA transform list."""
        if to is None:
            return

        _enter_m_to = float(to)
        if _atmos_state.get("preset") != "memory":
            _enter_m_to = max(_enter_m_to, 0.55)

        _enter_m_start = float(_atmos_state.get("sat", 1.0))
        renpy.show_layer_at(
            [atmos_sat_to(_enter_m_start, _enter_m_to, float(secs))],
            layer="master",
            camera=True,
            reset=False)
        _atmos_state["sat"] = _enter_m_to

    def atmos(preset, particles=None, zorder=50, secs=0.0):
        """Set base grade, preset saturation, and optional particles together."""
        _atmos_quality()

        # Validate every public argument before changing scene state.
        if not isinstance(preset, str) or preset not in ATMOS_PRESETS:
            _atmos_reject("unknown preset %r." % preset)
            return
        if particles is not None and particles not in _ATMOS_PARTICLE_VALUES:
            _atmos_reject(
                "particles must be None, 'motes', or 'nightdrift'; got %r." %
                particles)
            return

        _enter_m_zorder = _atmos_valid_zorder(zorder, "zorder")
        _enter_m_secs = _atmos_valid_secs(secs)
        if _enter_m_zorder is None or _enter_m_secs is None:
            return

        _atmos_state["preset"] = preset
        _atmos_state["particles"] = particles
        _atmos_state["zorder"] = _enter_m_zorder

        # A base-look change ends any transient overlay. This preserves the old
        # API's effective replacement semantics while using independent tags.
        _atmos_state["pressure_active"] = False
        renpy.hide(_ATMOS_PRESSURE_TAG, layer="master")
        _atmos_hide_legacy_tags()

        _atmos_set_sat(ATMOS_PRESETS[preset]["sat"], _enter_m_secs)
        _atmos_show_base_and_particles()

    def atmos_hold():
        """Backwards-compatible idempotent refresh of the current look."""
        _atmos_quality()
        _enter_m_preset = _atmos_state.get("preset")
        if _enter_m_preset not in ATMOS_PRESETS:
            return
        _atmos_set_sat(ATMOS_PRESETS[_enter_m_preset]["sat"], 0.0)
        _atmos_show_base_and_particles()
        _atmos_show_pressure_if_active()

    def atmos_clear():
        """Remove atmosphere and restore world colour without touching `show layer`."""
        renpy.show_layer_at(
            [], layer="master", camera=True, reset=False)
        _atmos_hide_current_tags()
        _atmos_hide_legacy_tags()
        _atmos_state.clear()
        _atmos_state.update(_atmos_default_state())

    def atmos_pressure(zorder=60):
        """Show the transient pressure overlay above the persistent base grade."""
        _atmos_quality()
        _enter_m_zorder = _atmos_valid_zorder(zorder, "pressure zorder")
        if _enter_m_zorder is None:
            return

        _atmos_state["pressure_active"] = True
        _atmos_state["pressure_zorder"] = _enter_m_zorder
        renpy.hide("atmos_pressure_fb", layer="master")
        _atmos_show_pressure_if_active()

    def atmos_pressure_clear():
        """Remove transient pressure while leaving the base look intact."""
        _atmos_state["pressure_active"] = False
        renpy.hide(_ATMOS_PRESSURE_TAG, layer="master")
        renpy.hide("atmos_pressure_fb", layer="master")

    def atmos_refresh():
        """Refresh dynamic tags after a live Preferences quality change."""
        _atmos_quality()
        _atmos_hide_legacy_tags()
        if _atmos_state.get("preset") in ATMOS_PRESETS:
            _atmos_show_base_and_particles()
        else:
            renpy.hide(_ATMOS_BASE_TAG, layer="master")
            renpy.hide(_ATMOS_PARTICLES_TAG, layer="master")
        _atmos_show_pressure_if_active()
        # ConditionSwitch performs the cross-context quality update on render.
        renpy.restart_interaction()

    def _atmos_scene_callback(layer):
        """Restore persistent master tags after scene; pressure is one-shot."""
        if layer != "master":
            return

        # Never carry authored story colour into the actual main-menu context.
        if getattr(renpy.context(), "_main_menu", False):
            renpy.show_layer_at(
                [], layer="master", camera=True, reset=False)
            _atmos_state.clear()
            _atmos_state.update(_atmos_default_state())
            return

        _atmos_state["pressure_active"] = False
        _atmos_state["pressure_zorder"] = 60
        _atmos_show_base_and_particles()

    def _atmos_remove_legacy_layer_saturation():
        """After-load migration: remove only this file's old `show layer` ATL."""
        try:
            _enter_m_lists = renpy.game.context().scene_lists
            _enter_m_pair = _enter_m_lists.layer_at_list.get("master")
            if not _enter_m_pair:
                return

            _enter_m_transforms = list(_enter_m_pair[1])
            _enter_m_kept = []
            for _enter_m_transform in _enter_m_transforms:
                _enter_m_atl = getattr(_enter_m_transform, "atl", None)
                _enter_m_loc = getattr(_enter_m_atl, "loc", None)
                _enter_m_filename = ""
                if _enter_m_loc:
                    _enter_m_filename = str(_enter_m_loc[0]).replace("\\", "/")
                if _enter_m_filename.endswith("/atmosphere.rpy") or \
                        _enter_m_filename == "atmosphere.rpy":
                    continue
                _enter_m_kept.append(_enter_m_transform)

            if len(_enter_m_kept) != len(_enter_m_transforms):
                renpy.show_layer_at(
                    _enter_m_kept,
                    layer="master",
                    reset=False,
                    camera=False)
        except Exception as _enter_m_migration_error:
            renpy.log(
                "ENTER-M ATMOS: legacy layer migration skipped: %r" %
                _enter_m_migration_error)

    def _atmos_after_load():
        """Normalize old state/tags and reconstruct the current authored look."""
        global _atmos_state

        _atmos_quality()
        _enter_m_old = _atmos_state
        if not hasattr(_enter_m_old, "get"):
            _enter_m_old = {}

        _enter_m_preset = _enter_m_old.get("preset")
        if _enter_m_preset not in ATMOS_PRESETS:
            _enter_m_preset = None

        _enter_m_particles = _enter_m_old.get("particles")
        if _enter_m_particles not in _ATMOS_PARTICLE_VALUES:
            _enter_m_particles = None

        try:
            _enter_m_zorder = int(_enter_m_old.get("zorder", 50))
        except (TypeError, ValueError, OverflowError):
            _enter_m_zorder = 50
        try:
            _enter_m_pressure_zorder = int(
                _enter_m_old.get("pressure_zorder", 60))
        except (TypeError, ValueError, OverflowError):
            _enter_m_pressure_zorder = 60

        _enter_m_pressure_active = bool(
            _enter_m_old.get("pressure_active", False))
        try:
            _enter_m_old_sat = float(_enter_m_old.get("sat", 1.0))
        except (TypeError, ValueError, OverflowError):
            _enter_m_old_sat = 1.0
        if not _enter_m_atmos_math.isfinite(_enter_m_old_sat):
            _enter_m_old_sat = 1.0
        _enter_m_sat = (
            ATMOS_PRESETS[_enter_m_preset]["sat"]
            if _enter_m_preset is not None else 1.0)

        if not hasattr(_atmos_state, "clear"):
            _atmos_state = _atmos_default_state()
        else:
            _atmos_state.clear()
        _atmos_state.update({
            "preset": _enter_m_preset,
            "particles": _enter_m_particles,
            "zorder": _enter_m_zorder,
            "sat": _enter_m_old_sat,
            "pressure_active": _enter_m_pressure_active,
            "pressure_zorder": _enter_m_pressure_zorder,
        })

        _atmos_hide_current_tags()
        _atmos_hide_legacy_tags()
        _atmos_remove_legacy_layer_saturation()

        if _enter_m_preset is None:
            renpy.show_layer_at(
                [], layer="master", camera=True, reset=False)
            _atmos_state["sat"] = 1.0
            _atmos_show_pressure_if_active()
            return

        _atmos_set_sat(_enter_m_sat, 0.0)
        _atmos_show_base_and_particles()
        _atmos_show_pressure_if_active()

    if _atmos_scene_callback not in config.scene_callbacks:
        config.scene_callbacks.append(_atmos_scene_callback)

    if _atmos_after_load not in config.after_load_callbacks:
        config.after_load_callbacks.append(_atmos_after_load)


# -----------------------------------------------------------------------------
# 6. SAVED STATE  --  DO NOT MOVE THIS BACK INTO init python
# -----------------------------------------------------------------------------
# `_atmos_state` MUST be declared with `default`, and this is load-bearing.
#
# Matsu'Py only writes a store variable into a save if that variable is in the
# store's `ever_been_changed` set (see Rollback.get_roots: "A variable is only in
# this map if it has ever been changed since the init phase finished"). That set
# is populated by REBINDING a name -- `find_changes` diffs the store dict's
# name -> object mapping. Everything this file does to the state
# (`_atmos_state["preset"] = ...`, `.clear()`, `.update()`) mutates the dict IN
# PLACE, so the binding never changes, the name never enters
# `ever_been_changed`, and the dict is never saved.
#
# What that caused: on load the scene lists came back correctly -- and then
# `_atmos_after_load` read a state dict that had been reset to the init default,
# saw `preset is None`, and actively TORE DOWN the grade it had just restored.
# Hot reload / autoreload has the same shape, because reload is a save+load
# round trip. Result: the story ran unlit after every load until the next
# `atmos(...)` call, which is often a whole scene later.
#
# `default` fixes it by adding the name to `ever_been_changed` itself
# (ast.Default.execute_default), which makes it a save root. It also does the
# right thing in both directions afterwards: on a NEW game it installs a fresh
# state, and after a LOAD it leaves the restored dict alone, because it only
# assigns when `start` is true or the name is absent from `ever_been_changed`.
# Saves written before this existed simply get the fresh default, exactly as
# they behave today.
#
# The `_atmos_state = _atmos_default_state()` up in `init python` is kept purely
# so the name resolves if anything reaches for it before defaults run. It is
# overwritten by this statement at game start.
default _atmos_state = _atmos_default_state()
