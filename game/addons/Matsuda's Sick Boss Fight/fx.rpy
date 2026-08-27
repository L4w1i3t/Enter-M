# =============================================================================
# ENTER-M :: Matsuda's Sick Boss Fight -- FX UPGRADE LAYER
# -----------------------------------------------------------------------------
# The battle in ui.rpy / battle_logic.rpy is a genuinely deep SMT/EO/FF/Touhou
# press-turn engine, but every pixel of it is drawn with flat animated Solid()
# rectangles. That ceiling is why it can still read as "just Matsu'Py". This file
# brings the same real GPU toolkit the project already uses in the OP
# (see addons/Sick Ass Anime OP/op_fx.rpy) into the fight:
#
#   * Custom GLSL shaders  - gradient/energy meter fills with flowing light and
#                            low-HP pulse, soft radial bloom, expanding shock
#                            rings, a domain-warped boss aura, and a battle
#                            post-process (vignette + grain + scanlines + tint).
#   * Real particle fields - per-phase ambient drift (embers / motes / ash) and
#                            one-shot impact bursts, built on SpriteManager.
#   * Helper screens        - drop-in replacements the existing battle screens
#                            opt into with a single `use`, each with a Solid()
#                            fallback so a refusing driver loses polish, not the
#                            fight.
#
# Everything here is additive and self-contained. Nothing in this file runs
# until ui.rpy calls into it, and every shader path is guarded by
# MSBF_FX_SHADERS with a flat-Solid fallback. Names are msbf_fx_* / "msbf.*" to
# avoid colliding with the existing msbf_* battle code or the OP's enter_m.*.
# =============================================================================

# -----------------------------------------------------------------------------
# 1. SHADERS (registered defensively; a bad driver must not break the battle)
# -----------------------------------------------------------------------------
init -10 python:
    import math as _msbf_fx_math

    def _msbf_register_fx_shaders():

        # ---- Energy meter fill -------------------------------------------
        # Draws an entire bar quad procedurally: a vertical gradient fill with
        # diagonal flowing light, a bright leading edge at the fill boundary,
        # a dim track for the empty remainder, and an optional whole-bar pulse
        # for danger states. u_fill is the 0..1 filled fraction.
        renpy.register_shader("msbf.bar", variables="""
            uniform float u_time;
            uniform float u_fill;
            uniform vec3 u_col_lo;
            uniform vec3 u_col_hi;
            uniform vec3 u_track;
            uniform float u_glow;
            uniform float u_pulse;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            float fill = clamp(u_fill, 0.0, 1.0);

            // Vertical gradient, brighter toward the top edge.
            vec3 grad = mix(u_col_lo, u_col_hi, 1.0 - uv.y);
            grad += vec3(1.0) * (1.0 - uv.y) * 0.10;

            // Diagonal energy flow scrolling along the fill.
            float flow = 0.5 + 0.5 * sin((uv.x * 26.0 - uv.y * 7.0) - u_time * 5.0);
            grad += grad * flow * 0.16;

            // Danger pulse (whole fill breathes when u_pulse > 0).
            float pulse = 1.0 + u_pulse * 0.30 * sin(u_time * 6.5);
            grad *= pulse;

            // Bright sheen riding the leading edge of the fill.
            float edge = smoothstep(0.05, 0.0, abs(uv.x - fill)) * u_glow;

            float inside = step(uv.x, fill);

            // Track for the spent portion, with a faint scrolling shimmer.
            vec3 track = u_track;
            track += u_track * (0.5 + 0.5 * sin(uv.x * 44.0 - u_time * 3.0)) * 0.18;

            vec3 fillcol = grad + vec3(1.0) * edge;
            vec3 col = mix(track, fillcol, inside);

            float a = mix(0.82, 1.0, inside);
            a = max(a, edge);                 // edge glow bleeds past the fill
            gl_FragColor = vec4(col * a, a);  // premultiplied
        """)

        # ---- Soft radial bloom -------------------------------------------
        # A premultiplied glow blob: bright core fading to nothing at the rim.
        # Used for boss backlight, impact light, and meter-break flashes so
        # light reads as light instead of a flat translucent rectangle.
        # DITHERED. Every shader in this family outputs one long, perfectly
        # smooth alpha ramp in a dark colour, which is precisely the signal an
        # 8-bit framebuffer cannot hold: a 600px bloom over a near-black room
        # quantizes into visible concentric rings, and the bigger and softer the
        # bloom the worse it is. Half a code value of noise added before the
        # quantization spreads each step's error across neighbouring pixels and
        # the rings disappear. It is the cheapest fidelity there is -- three
        # instructions, no texture, and it costs nothing at all on the frames
        # where there was no banding to fix.
        renpy.register_shader("msbf.glow", variables="""
            uniform vec3 u_color;
            uniform float u_intensity;
            uniform float u_softness;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            // Interleaved-gradient noise (Jimenez). Three instructions, no
            // texture and no transcendental, and it is stable per pixel rather
            // than per fragment-shader-invocation, which is what makes it read
            // as film rather than as fizz.
            float msbf_ign(vec2 p) {
                return fract(52.9829189 * fract(dot(p, vec2(0.06711056, 0.00583715))));
            }
        """, fragment_300="""
            vec2 d = v_tex_coord - vec2(0.5);
            float r = length(d) * 2.0;
            float core = pow(clamp(1.0 - r, 0.0, 1.0), u_softness);
            float a = core * u_intensity;
            a = clamp(a + (msbf_ign(gl_FragCoord.xy) - 0.5) * 0.0039, 0.0, 1.0);
            gl_FragColor = vec4(u_color * a, a);
        """)

        # ---- Expanding shock ring ----------------------------------------
        # A bright annulus that grows as u_progress 0->1 and fades out. Drawn
        # procedurally (no scene texture needed) so it composites over the live
        # battle; animate u_progress from ATL to land it on an impact.
        renpy.register_shader("msbf.ring", variables="""
            uniform float u_progress;
            uniform vec3 u_color;
            uniform float u_thickness;
            uniform float u_intensity;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            // Interleaved-gradient noise (Jimenez). Three instructions, no
            // texture and no transcendental, and it is stable per pixel rather
            // than per fragment-shader-invocation, which is what makes it read
            // as film rather than as fizz.
            float msbf_ign(vec2 p) {
                return fract(52.9829189 * fract(dot(p, vec2(0.06711056, 0.00583715))));
            }
        """, fragment_300="""
            vec2 d = v_tex_coord - vec2(0.5);
            float r = length(d) * 2.0;
            float radius = u_progress;
            float ring = smoothstep(u_thickness, 0.0, abs(r - radius));
            float a = ring * (1.0 - u_progress) * u_intensity;
            a = clamp(a + (msbf_ign(gl_FragCoord.xy) - 0.5) * 0.0039, 0.0, 1.0);
            gl_FragColor = vec4(u_color * a, a);
        """)

        # ---- Boss sigil halo -----------------------------------------------
        # A procedural ritual ring hung flat behind the boss sprite (SMT deity
        # halo): concentric rings, a dashed band rotating one way, soft spokes
        # sweeping the other. u_jitter > 0 snaps the rotation on a stepped
        # clock -- the phase-3 "corrupted sigil" look. u_time is Matsu'Py's
        # built-in frame clock, so the ring animates GPU-side while the screen
        # tree stays completely static.
        renpy.register_shader("msbf.sigil", variables="""
            uniform vec3 u_color;
            uniform float u_intensity;
            uniform float u_spin;
            uniform float u_jitter;
            uniform float u_time;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 d = v_tex_coord - vec2(0.5);
            float r = length(d) * 2.0;
            float ang = atan(d.y, d.x);
            float t = u_time * u_spin;
            if (u_jitter > 0.0) {
                float stept = floor(u_time * 9.0);
                float snap = fract(sin(stept * 12.9898) * 43758.5453);
                t += (snap - 0.5) * u_jitter * 2.4;
            }
            float a = 0.0;
            a += smoothstep(0.030, 0.0, abs(r - 0.94)) * 0.9;
            a += smoothstep(0.020, 0.0, abs(r - 0.66)) * 0.6;
            float dash = step(0.5, fract((ang - t) * 3.8197));
            a += smoothstep(0.075, 0.0, abs(r - 0.81)) * dash * 0.5;
            float spoke = pow(abs(cos((ang + t * 0.55) * 4.0)), 24.0);
            a += spoke * smoothstep(0.94, 0.35, r) * step(0.40, r) * 0.30;
            a *= u_intensity;
            gl_FragColor = vec4(u_color * a, a);
        """)

        # ---- Chrome glass panel --------------------------------------------
        # The battle UI's panel surface: a vertical gradient with a slow
        # diagonal sheen, faint scanlines, a soft top highlight, and a
        # corner-weighted accent frame (border segments brighten toward the
        # corners, reading as brackets). Replaces the flat Solid() rectangles
        # everywhere a panel is drawn. u_edge scales the frame (0 = frameless
        # glass band); u_model_size keeps border thickness in real pixels at
        # any panel size; u_time drifts the sheen.
        renpy.register_shader("msbf.panel", variables="""
            uniform vec3 u_col;
            uniform vec3 u_accent;
            uniform float u_alpha;
            uniform float u_edge;
            uniform vec2 u_model_size;
            uniform float u_time;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 px = v_tex_coord * u_model_size;
            vec2 dd = min(px, u_model_size - px);
            float edge = min(dd.x, dd.y);
            vec3 col = u_col * (1.12 - v_tex_coord.y * 0.40);
            float sheen = 0.5 + 0.5 * sin((px.x - px.y) * 0.014 - u_time * 0.30);
            col += u_col * sheen * 0.18;
            float scan = step(0.5, fract(px.y * 0.33333)) * 0.024;
            col = max(col - vec3(scan), vec3(0.0));
            float corner = smoothstep(30.0, 9.0, dd.x + dd.y);
            float lin = smoothstep(2.4, 0.9, edge) * u_edge * (0.40 + 0.60 * corner);
            float glow = smoothstep(11.0, 0.0, edge) * 0.16 * u_edge;
            col = mix(col, u_accent, clamp(lin, 0.0, 1.0));
            col += u_accent * glow;
            col += vec3(1.0) * smoothstep(2.0, 0.0, px.y) * 0.07;
            float a = clamp(u_alpha + lin * (1.0 - u_alpha), 0.0, 1.0);
            gl_FragColor = vec4(col * a, a);
        """)

        # ---- Domain-warped boss aura -------------------------------------
        # A churning radial energy field for behind the boss. Premultiplied and
        # radially masked so it glows out of the sprite without a hard edge.
        renpy.register_shader("msbf.aura", variables="""
            uniform float u_time;
            uniform vec3 u_color;
            uniform vec3 u_color2;
            uniform float u_intensity;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float msbf_hash(vec2 p) {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
            }
            float msbf_noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                vec2 u = f * f * (3.0 - 2.0 * f);
                float a = msbf_hash(i);
                float b = msbf_hash(i + vec2(1.0, 0.0));
                float c = msbf_hash(i + vec2(0.0, 1.0));
                float d = msbf_hash(i + vec2(1.0, 1.0));
                return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
            }
            float msbf_fbm(vec2 p) {
                float v = 0.0;
                float amp = 0.5;
                for (int i = 0; i < 3; i++) {
                    v += amp * msbf_noise(p);
                    p *= 2.0;
                    amp *= 0.5;
                }
                return v;
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            vec2 c = uv - 0.5;
            float r = length(c) * 2.0;
            float t = u_time * 0.6;
            vec2 p = uv * 3.0;
            vec2 q = vec2(msbf_fbm(p + vec2(0.0, t)), msbf_fbm(p + vec2(4.2, -t)));
            float f = msbf_fbm(p + 2.2 * q);
            float falloff = pow(clamp(1.0 - r, 0.0, 1.0), 1.8);
            vec3 col = mix(u_color, u_color2, clamp(f * 1.4, 0.0, 1.0));
            float a = falloff * (0.35 + 0.65 * f) * u_intensity;
            gl_FragColor = vec4(col * a, a);
        """)

        # ---- Battle post-process -----------------------------------------
        # Procedural vignette + scanlines + film grain + tint over the whole
        # screen. Premultiplied so it composites over anything. u_intensity
        # scales the lot; phase 3 pushes it harder for the Id Mode rupture.
        renpy.register_shader("msbf.postfx", variables="""
            uniform float u_time;
            uniform vec2 u_model_size;
            uniform float u_intensity;
            uniform vec3 u_tint;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            // Interleaved-gradient noise (Jimenez). Three instructions, no
            // texture and no transcendental, and it is stable per pixel rather
            // than per fragment-shader-invocation, which is what makes it read
            // as film rather than as fizz.
            float msbf_ign(vec2 p) {
                return fract(52.9829189 * fract(dot(p, vec2(0.06711056, 0.00583715))));
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            vec2 c = uv - 0.5;
            float vig = smoothstep(0.46, 0.98, length(c) * 1.30) * 0.60;
            float scan = (1.0 - (sin(uv.y * 1180.0) * 0.5 + 0.5)) * 0.045;
            // SIGNED grain. `max(n - 0.5, 0.0)` can only ever add, so the old
            // form quietly raised the mean of the whole grade by half its own
            // amplitude -- a permanent veil rather than a texture. Signing it
            // keeps the exact same grain and puts the mean back where the
            // vignette intended it.
            float n = fract(sin(dot(uv * u_model_size + vec2(u_time * 57.0), vec2(12.9898, 78.233))) * 43758.5453) - 0.5;
            float grain = n * 0.09;
            float a = clamp(vig + scan + grain, 0.0, 0.92) * u_intensity;
            a = clamp(a + (msbf_ign(gl_FragCoord.xy) - 0.5) * 0.0039, 0.0, 1.0);
            gl_FragColor = vec4(u_tint * a, a);
        """)

        # ---- Per-phase atmosphere ----------------------------------------
        # ONE generative full-screen (or stage-scoped) field that replaces the
        # old swarm of 30-60 individually-animated Solid() rectangles per phase:
        # a domain-warped flowing energy nebula + diagonal light streaks +
        # optional radial god-rays + scanlines + grain + vignette, all driven by
        # u_time on the GPU (so it costs ~one draw and never rebuilds the screen).
        # Palette + style come from uniforms so the same shader serves all three
        # phases: calm cyan (phase 1), divine gold/cyan god-rays (phase 2), and
        # black/red/white "collapsing signal" chaos (phase 3, via u_warp + u_jitter).
        renpy.register_shader("msbf.atmos", variables="""
            uniform float u_time;
            uniform vec2 u_model_size;
            uniform vec3 u_col_a;
            uniform vec3 u_col_b;
            uniform vec3 u_col_c;
            uniform float u_intensity;
            uniform float u_warp;
            uniform float u_rays;
            uniform float u_scan;
            uniform float u_flow;
            uniform float u_grain;
            uniform float u_vig;
            uniform float u_jitter;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float msbf_a_hash(vec2 p) {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
            }
            float msbf_a_noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                vec2 u = f * f * (3.0 - 2.0 * f);
                float a = msbf_a_hash(i);
                float b = msbf_a_hash(i + vec2(1.0, 0.0));
                float c = msbf_a_hash(i + vec2(0.0, 1.0));
                float d = msbf_a_hash(i + vec2(1.0, 1.0));
                return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
            }
            float msbf_a_fbm(vec2 p) {
                float v = 0.0;
                float amp = 0.5;
                for (int i = 0; i < 3; i++) {
                    v += amp * msbf_a_noise(p);
                    p *= 2.0;
                    amp *= 0.5;
                }
                return v;
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            vec2 cen = uv - 0.5;
            float t = u_time;

            // Flowing, domain-warped energy field -- the living atmosphere.
            vec2 p = uv * vec2(3.2, 2.4);
            p.x += t * u_flow * 0.12;
            vec2 q = vec2(msbf_a_fbm(p + vec2(0.0, t * 0.20)), msbf_a_fbm(p + vec2(5.2, -t * 0.18)));
            float f = clamp(msbf_a_fbm(p + u_warp * q), 0.0, 1.0);

            // Palette: low field -> a, mid -> b, chaotic peaks -> c.
            vec3 col = mix(u_col_a, u_col_b, smoothstep(0.20, 0.70, f));
            col = mix(col, u_col_c, smoothstep(0.62, 0.96, f) * clamp(u_warp * 0.5, 0.0, 1.0));
            float field = pow(f, 1.5);

            // Diagonal light streaks sweeping across.
            float sw = 0.5 + 0.5 * sin((uv.x * 6.0 - uv.y * 2.2) * 3.14159 - t * (1.0 + u_flow * 0.6));
            float streak = pow(sw, 8.0) * 0.6;

            // Radial god-rays from a high centre (divine phase-2 light).
            vec2 rc = uv - vec2(0.5, 0.28);
            float ray = 0.5 + 0.5 * sin(atan(rc.y, rc.x) * 16.0 - t * 0.5);
            ray = pow(ray, 4.0) * u_rays * smoothstep(0.0, 0.7, length(rc));

            // Scanlines. Calm phases: a slow, dense roll. Chaotic phases (u_jitter
            // high, phase 3): a quick, stepped "signal glitch" clock that jumps the
            // roll on sporadic frames, tightens the lines, and flashes white/grey
            // tear bands -- all cheap (no extra field sampling).
            float tj = floor(t * (7.0 + u_jitter * 7.0));
            float flick = fract(sin(tj * 91.73) * 3733.7);
            float glitchOn = step(0.72, flick) * u_jitter;
            float scanRoll = t * (0.6 + u_jitter * 8.0) + glitchOn * flick * 14.0;
            float scan = (0.5 - 0.5 * cos(uv.y * (540.0 + u_jitter * 300.0) - scanRoll)) * u_scan * 0.5;
            scan += glitchOn * 0.10;
            float band = step(0.5, fract(uv.y * 7.0 + glitchOn * flick * 5.0)) * glitchOn;
            float n = fract(sin(dot(uv * u_model_size + vec2(t * 53.0), vec2(12.9898, 78.233))) * 43758.5453);
            float grain = max(n - 0.5, 0.0) * u_grain;

            // Build brightness, then darken the rim with a vignette. The tear bands
            // add a desaturated white/grey flash (matches phase 3's mono palette).
            float bright = (field * 0.42 + streak + ray) * u_intensity + scan + grain;
            vec3 outcol = col * bright + vec3(1.0) * (streak * 0.45 + ray * 0.5 + band * 0.18);
            float vig = smoothstep(0.42, 1.06, length(cen) * 1.3) * u_vig;
            outcol = mix(outcol, vec3(0.0), vig);

            float a = clamp(bright + vig, 0.0, 0.88);
            gl_FragColor = vec4(outcol * a, a);
        """)

        # ---- Datamosh / glitch -------------------------------------------
        # Row-block horizontal displacement + per-channel tear on a rendered
        # child (mesh True). u_intensity 0..1 gates how many rows tear and how
        # hard; the phase-3 stage rides this so the "image" literally struggles
        # to hold itself together. Premultiplied-safe (samples a Matsu'Py texture).
        renpy.register_shader("msbf.glitch", variables="""
            uniform sampler2D tex0;
            uniform float u_time;
            uniform float u_intensity;
            uniform float u_blocks;
            uniform float u_speed;
            uniform float u_amount;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            float row = floor(uv.y * u_blocks);
            float seed = floor(u_time * u_speed);
            float rnd = fract(sin(row * 43.21 + seed * 7.137) * 1234.567);
            float gate = step(1.0 - u_intensity, rnd);
            uv.x += gate * (rnd - 0.5) * u_amount;
            float ca = 0.004 + u_intensity * 0.018;
            vec4 c;
            c.r = texture2D(tex0, uv + vec2(ca, 0.0)).r;
            c.g = texture2D(tex0, uv).g;
            c.b = texture2D(tex0, uv - vec2(ca, 0.0)).b;
            c.a = texture2D(tex0, uv).a;
            // Occasional dropped/blown-out scanlines for "signal loss".
            float drop = step(0.985, fract(sin((row + seed) * 12.9898) * 43758.5453)) * u_intensity;
            c.rgb += drop * 0.6;
            gl_FragColor = c;
        """)

        # ---- Chromatic aberration / RGB split ----------------------------
        # Splits R/B channels of a rendered child outward; u_amount in texels.
        # Used as a throbbing ghost on the phase-3 boss -- the identity refusing
        # to resolve into one image.
        renpy.register_shader("msbf.rgbsplit", variables="""
            uniform sampler2D tex0;
            uniform float u_time;
            uniform float u_amount;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            float wob = 1.0 + 0.35 * sin(u_time * 22.0);
            vec2 off = vec2(u_amount * wob * 0.0016, 0.0);
            vec4 cr = texture2D(tex0, v_tex_coord + off);
            vec4 cg = texture2D(tex0, v_tex_coord);
            vec4 cb = texture2D(tex0, v_tex_coord - off);
            gl_FragColor = vec4(cr.r, cg.g, cb.b, cg.a);
        """)

    try:
        _msbf_register_fx_shaders()
        MSBF_FX_SHADERS = True
    except Exception as _msbf_fx_e:
        MSBF_FX_SHADERS = False
        if config.developer:
            renpy.log("MSBF FX: shader registration failed: %r" % _msbf_fx_e)


# -----------------------------------------------------------------------------
# 2. PALETTES + COLOUR HELPERS
# -----------------------------------------------------------------------------
init -1 python:
    def msbf_hex_rgb(hexstr):
        """'#rrggbb' or '#rrggbbaa' -> (r, g, b) floats in 0..1.
        The project parser (game/fx.rpy, init -5) with this layer's white
        fallback -- an unreadable colour should blow out, not go black."""
        return enter_m_rgba(hexstr, fallback=(1.0, 1.0, 1.0, 1.0))[:3]

    def msbf_rgb_scale(rgb, factor, add=0.0):
        return tuple(min(1.0, channel * factor + add) for channel in rgb)

    def msbf_rgb(color):
        """'#rrggbb' (or anything Color accepts) -> a vec3 tuple for uniforms."""
        try:
            return Color(color).rgb
        except Exception:
            return (1.0, 1.0, 1.0)

    def msbf_panel_bg(col=(0.028, 0.060, 0.105), accent=(0.33, 0.87, 1.0),
            alpha=0.94, edge=1.0, fallback="#06101cf2"):
        """A glassy chrome panel (msbf.panel shader): drop-in displayable for
        any `background` or `add` that used to be a flat Solid. `col`/`accent`
        take vec3 tuples or '#rrggbb' strings; `edge` scales the accent frame
        (0 = frameless glass band). Falls back to the old flat Solid when
        shaders are unavailable, so callers never need their own guard."""
        if not MSBF_FX_SHADERS:
            return Solid(fallback)
        if isinstance(col, str):
            col = msbf_rgb(col)
        if isinstance(accent, str):
            accent = msbf_rgb(accent)
        return Transform(Solid("#00000000"), mesh=True, shader="msbf.panel",
                u_col=tuple(col), u_accent=tuple(accent),
                u_alpha=float(alpha), u_edge=float(edge))

    def msbf_bar_palette_from_fill(fill_color, empty_color):
        """Derive a (lo, hi, track) gradient from a flat fill/empty pair so the
        shader bar matches whatever colour the old Solid bar used."""
        base = msbf_hex_rgb(fill_color)
        lo = msbf_rgb_scale(base, 0.42)
        hi = msbf_rgb_scale(base, 1.12, 0.10)
        track = msbf_rgb_scale(msbf_hex_rgb(empty_color), 1.0)
        return lo, hi, track


# -----------------------------------------------------------------------------
# 3. SHADER TRANSFORMS
# -----------------------------------------------------------------------------
transform msbf_fx_bar_t(frac=1.0, lo=(0.18, 0.55, 0.30), hi=(0.45, 1.0, 0.55), track=(0.06, 0.10, 0.14), glow=0.9, pulse=0.0):
    mesh True
    shader "msbf.bar"
    u_fill frac
    u_col_lo lo
    u_col_hi hi
    u_track track
    u_glow glow
    u_pulse pulse

transform msbf_fx_glow_t(color=(0.33, 0.87, 1.0), intensity=0.6, softness=1.6):
    mesh True
    shader "msbf.glow"
    u_color color
    u_intensity intensity
    u_softness softness

# Soft glow that blooms in and decays -- for one-shot impact light.
transform msbf_fx_glow_pop(color=(1.0, 1.0, 1.0), intensity=0.85, softness=1.4, duration=0.5):
    mesh True
    shader "msbf.glow"
    u_color color
    u_softness softness
    u_intensity intensity
    alpha 1.0
    easeout duration u_intensity 0.0

transform msbf_fx_ring_t(color=(1.0, 0.22, 0.41), thickness=0.10, intensity=1.0, duration=0.55):
    mesh True
    shader "msbf.ring"
    u_color color
    u_thickness thickness
    u_intensity intensity
    u_progress 0.0
    linear duration u_progress 1.0

transform msbf_fx_glow_pulse(color=(0.33, 0.87, 1.0), lo=0.18, hi=0.40, softness=2.2):
    mesh True
    shader "msbf.glow"
    u_color color
    u_softness softness
    u_intensity lo
    block:
        easein 0.7 u_intensity hi
        easeout 0.7 u_intensity lo
        repeat

transform msbf_fx_aura_t(color=(0.20, 0.65, 1.0), color2=(0.65, 0.30, 1.0), intensity=0.55):
    mesh True
    shader "msbf.aura"
    u_color color
    u_color2 color2
    u_intensity intensity
    subpixel True

# Boss sigil halo (msbf.sigil): rotation runs on u_time GPU-side; the ATL
# block only breathes the intensity, so the screen tree never rebuilds for it.
transform msbf_fx_sigil_t(color=(0.35, 0.86, 1.0), intensity=0.30, spin=0.30, jitter=0.0):
    mesh True
    shader "msbf.sigil"
    u_color color
    u_spin spin
    u_jitter jitter
    u_intensity intensity
    block:
        easein 2.3 u_intensity intensity * 1.22
        easeout 2.3 u_intensity intensity * 0.85
        repeat

transform msbf_fx_postfx_t(intensity=0.5, tint=(0.02, 0.05, 0.09)):
    mesh True
    shader "msbf.postfx"
    u_intensity intensity
    u_tint tint

# Per-phase generative atmosphere (replaces the old Solid() decoration swarm).
transform msbf_fx_atmos_t(col_a, col_b, col_c, intensity=0.5, warp=1.0, rays=0.0, scan=0.45, flow=0.7, grain=0.05, vig=0.5, jitter=0.0):
    mesh True
    shader "msbf.atmos"
    u_col_a col_a
    u_col_b col_b
    u_col_c col_c
    u_intensity intensity
    u_warp warp
    u_rays rays
    u_scan scan
    u_flow flow
    u_grain grain
    u_vig vig
    u_jitter jitter
    subpixel True

# Sporadic datamosh: a low baseline that erupts into hard tears on an uneven
# rhythm -- the phase-3 image fighting (and failing) to hold its form.
transform msbf_fx_glitch_pulse(base=0.14, peak=0.78, blocks=26.0):
    mesh True
    shader "msbf.glitch"
    u_blocks blocks
    u_speed 22.0
    u_amount 0.14
    u_intensity base
    block:
        pause 0.85
        easein 0.04 u_intensity peak
        easeout 0.22 u_intensity base
        pause 0.45
        easein 0.03 u_intensity peak * 0.55
        easeout 0.30 u_intensity base
        pause 1.35
        easein 0.05 u_intensity peak
        easeout 0.16 u_intensity base * 1.4
        pause 0.30
        easein 0.03 u_intensity peak * 0.7
        easeout 0.40 u_intensity base
        repeat

# Throbbing chromatic split for the phase-3 boss ghost (identity won't resolve).
transform msbf_fx_rgbsplit_pulse(base=6.0, peak=22.0):
    mesh True
    shader "msbf.rgbsplit"
    u_amount base
    block:
        easein 0.10 u_amount peak
        easeout 0.34 u_amount base
        pause 0.8
        easein 0.06 u_amount peak * 0.6
        easeout 0.40 u_amount base
        pause 1.2
        repeat

# Floating combat number: pop in, rise, fade. dx jitters stacked numbers.
transform msbf_float_rise(dx=0.0):
    subpixel True
    xoffset dx
    alpha 0.0
    yoffset 6
    zoom 0.78
    easeout 0.14 alpha 1.0 yoffset -8 zoom 1.05
    ease 0.10 zoom 1.0
    parallel:
        linear 0.66 yoffset -46
    parallel:
        block:
            pause 0.42
            linear 0.34 alpha 0.0

# Heavier punch for crits: bigger overshoot before the rise.
transform msbf_float_rise_crit(dx=0.0):
    subpixel True
    xoffset dx
    alpha 0.0
    yoffset 4
    zoom 1.55
    easeout 0.10 alpha 1.0 zoom 0.94
    easein 0.08 zoom 1.08
    ease 0.08 zoom 1.0
    parallel:
        linear 0.66 yoffset -50
    parallel:
        block:
            pause 0.46
            linear 0.34 alpha 0.0


# -----------------------------------------------------------------------------
# 4. PARTICLE FIELDS (SpriteManager; deterministic + rollback-safe)
# -----------------------------------------------------------------------------
init python:
    import math as _msbf_pm_math

    class MSBFDrift(object):
        """An ambient field of drifting particles. Position is derived from the
        sprite-manager time `st`, so it is deterministic and recycles by wrapping
        the screen edges -- no per-frame allocation, rollback-safe."""

        def __init__(self, child, count=40, W=1280, H=720, vy=-26.0, vx=5.0, amp=22.0, spd=0.7):
            self.sm = SpriteManager(update=self.update)
            self.W = float(W)
            self.H = float(H)
            self.vy = float(vy)
            self.vx = float(vx)
            self.amp = float(amp)
            self.spd = float(spd)
            self.parts = []
            for _ in range(count):
                s = self.sm.create(child)
                x0 = random.random() * (self.W + 80.0) - 40.0
                y0 = random.random() * (self.H + 80.0) - 40.0
                ph = random.random() * 6.2832
                vyi = self.vy * (0.7 + random.random() * 0.6)
                vxi = self.vx * (0.5 + random.random() * 1.0)
                sp = self.spd * (0.6 + random.random() * 0.8)
                s.x = int(x0)
                s.y = int(y0)
                self.parts.append((s, x0, y0, vxi, vyi, ph, sp))

        def update(self, st):
            spanY = self.H + 80.0
            spanX = self.W + 80.0
            for s, x0, y0, vxi, vyi, ph, sp in self.parts:
                y = ((y0 + vyi * st) + 40.0) % spanY - 40.0
                x = ((x0 + vxi * st + self.amp * _msbf_pm_math.sin(st * sp + ph)) + 40.0) % spanX - 40.0
                s.x = int(x)
                s.y = int(y)
            return 0


# ---- Particle sprites -------------------------------------------------------
image msbf_fx_p_ember:
    Solid("#79e7ff")
    subpixel True
    xysize (3, 3)
    alpha 0.42

image msbf_fx_p_mote:
    Solid("#ffe6a8")
    subpixel True
    xysize (4, 4)
    alpha 0.40

image msbf_fx_p_ash:
    Solid("#ff6b8e")
    subpixel True
    xysize (4, 4)
    alpha 0.50

image msbf_fx_p_spark:
    Solid("#dffaff")
    subpixel True
    xysize (5, 5)
    zoom 1.0
    alpha 0.95
    parallel:
        linear 0.55 zoom 0.0
    parallel:
        linear 0.55 alpha 0.0

# Stage-scoped fields (786x458) for atmosphere right around the boss. Counts are
# kept modest -- each particle is a per-frame displayable, so this is the part
# of the FX budget most worth keeping lean.
image msbf_fx_stage_phase1:
    MSBFDrift("msbf_fx_p_ember", count=16, W=786, H=458, vy=-26.0, vx=4.0, amp=20.0, spd=0.9).sm
    pos (0, 0)

image msbf_fx_stage_phase2:
    MSBFDrift("msbf_fx_p_mote", count=10, W=786, H=458, vy=-16.0, vx=7.0, amp=26.0, spd=1.0).sm
    pos (0, 0)

image msbf_fx_stage_phase3:
    MSBFDrift("msbf_fx_p_ash", count=12, W=786, H=458, vy=40.0, vx=-11.0, amp=30.0, spd=1.3).sm
    pos (0, 0)

# Phase-1 "howling wind": motes torn sideways across the scene. Big horizontal
# velocity, only a faint upward lift, a short elongated sprite -- so each particle
# reads as a streak of wind-borne dust rather than a drifting ember.
image msbf_fx_p_windmote:
    Solid("#c4e2ff")
    subpixel True
    xysize (8, 2)
    alpha 0.32

image msbf_fx_field_wind:
    MSBFDrift("msbf_fx_p_windmote", count=26, W=1280, H=720, vy=-7.0, vx=128.0, amp=11.0, spd=1.7).sm
    pos (0, 0)


# ---- Per-phase colour config ------------------------------------------------
init -1 python:
    # Aura inner/outer colours, post-process tint+intensity, and ambient field
    # key, all keyed by phase so the battle screen wires with one lookup.
    MSBF_FX_PHASE = {
        1: {
            "aura":   ((0.14, 0.55, 1.0), (0.42, 0.30, 1.0)),
            "aura_i": 0.50,
            "postfx": ((0.02, 0.05, 0.10), 0.34),
        },
        2: {
            "aura":   ((1.0, 0.81, 0.40), (0.33, 0.87, 1.0)),
            "aura_i": 0.58,
            "postfx": ((0.05, 0.04, 0.07), 0.44),
        },
        3: {
            "aura":   ((1.0, 0.22, 0.41), (0.65, 0.22, 1.0)),
            "aura_i": 0.70,
            "postfx": ((0.09, 0.02, 0.05), 0.56),
        },
    }

    def msbf_fx_phase_cfg(phase):
        return MSBF_FX_PHASE.get(phase if phase in MSBF_FX_PHASE else (3 if phase >= 3 else 1), MSBF_FX_PHASE[1])

    # msbf.atmos uniform sets per phase. Keeps each phase's identity: phase 1 calm
    # cyan, phase 2 divine gold/cyan with god-rays, phase 3 crimson-violet chaos
    # (high warp + harsher scan/grain). Used full-screen (backdrop) and stage-scoped.
    MSBF_ATMOS_PHASE = {
        1: {
            "a": (0.05, 0.12, 0.24), "b": (0.16, 0.55, 0.95), "c": (0.55, 0.85, 1.0),
            "intensity": 0.50, "warp": 0.85, "rays": 0.0, "scan": 0.45, "flow": 0.7, "grain": 0.05, "vig": 0.55, "jitter": 0.0,
        },
        2: {
            "a": (0.10, 0.16, 0.26), "b": (1.0, 0.78, 0.36), "c": (0.40, 0.85, 1.0),
            "intensity": 0.58, "warp": 1.25, "rays": 0.55, "scan": 0.40, "flow": 1.0, "grain": 0.06, "vig": 0.50, "jitter": 0.0,
        },
        # Phase 3: mono chaos -- black -> red -> white/grey (no violet), with the
        # sporadic quick-glitch scanlines (jitter) doing the "collapsing signal".
        3: {
            "a": (0.05, 0.05, 0.06), "b": (0.86, 0.12, 0.16), "c": (0.90, 0.92, 0.95),
            "intensity": 0.64, "warp": 2.2, "rays": 0.12, "scan": 0.68, "flow": 1.4, "grain": 0.12, "vig": 0.62, "jitter": 1.0,
        },
    }

    def msbf_atmos_cfg(phase):
        return MSBF_ATMOS_PHASE.get(phase if phase in MSBF_ATMOS_PHASE else (3 if phase >= 3 else 1), MSBF_ATMOS_PHASE[1])


# ---- Quality (fixed: "balanced") ---------------------------------------------
# The fight runs at one universal quality level: the domain-warped boss aura and
# ambient particle fields are on, the full-screen post-process and the per-bullet
# glow halo (the heaviest, lowest-value passes) are off. These helpers are kept
# as the single source of truth that the screens gate on.
init -1 python:
    def msbf_fx_aura_on():
        return True

    def msbf_fx_particles_on():
        return True

    def msbf_fx_postfx_on():
        return False

    # Per-element accent colours so skills read at a glance (SMT/Persona habit).
    MSBF_ELEMENT_COLORS = {
        "slash": "#d7e0ea",
        "weapon": "#d7e0ea",
        "pierce": "#aebfff",
        "fire": "#ff6b3d",
        "ice": "#5fd0ff",
        "lightning": "#ffd84d",
        "wind": "#7be0a0",
        "psychic": "#c87bff",
        "almighty": "#ff5fa8",
        "healing": "#66e08a",
        "support": "#9fb4c4",
    }

    def msbf_element_color(element):
        return MSBF_ELEMENT_COLORS.get(element, "#9fb4c4")

    # Distinct dossier accents so the roster reads as a cast, not a spreadsheet.
    MSBF_ROSTER_ACCENTS = ["#55ddff", "#c87bff", "#5fd0ff", "#aebfff", "#ff6b3d", "#66e08a", "#ffd84d", "#ff6b8e"]

    def msbf_roster_accent(index):
        return MSBF_ROSTER_ACCENTS[index % len(MSBF_ROSTER_ACCENTS)]


# -----------------------------------------------------------------------------
# 5. DROP-IN SCREENS (each shader path has a Solid() fallback)
# -----------------------------------------------------------------------------

# Energy meter. Signature-compatible intent with the existing msbf_meter so the
# battle code can delegate to it: same value/max/size + fill/empty colours.
screen msbf_energy_bar(value, max_value, width, height, fill_color="#66e08a", empty_color="#141923", danger=True):
    $ _frac = (float(value) / float(max_value)) if max_value > 0 else 0.0
    $ _frac = max(0.0, min(1.0, _frac))
    if MSBF_FX_SHADERS:
        $ _lo, _hi, _track = msbf_bar_palette_from_fill(fill_color, empty_color)
        $ _pulse = 1.0 if (danger and 0.0 < _frac < 0.30) else 0.0
        $ _glow = 1.05 if _frac > 0.0 else 0.0
        add Solid(fill_color) xysize (width, height) at msbf_fx_bar_t(_frac, _lo, _hi, _track, _glow, _pulse)
    else:
        add Solid(empty_color) xysize (width, height)
        add Solid(fill_color) xysize (msbf_bar_width(value, max_value, width), height)

# Static boss aura field placed behind the sprite. color/color2 are vec3 tuples.
screen msbf_boss_aura(cx, cy, w, h, color, color2, intensity=0.55):
    if MSBF_FX_SHADERS:
        add Solid("#00000000") at msbf_fx_aura_t(color, color2, intensity):
            xcenter cx
            ycenter cy
            xysize (int(w), int(h))


# One-shot soft light bloom at a point.
screen msbf_glow_pop(cx, cy, w, h, color=(1.0, 1.0, 1.0), intensity=0.85, softness=1.4, duration=0.5):
    if MSBF_FX_SHADERS:
        add Solid("#00000000") at msbf_fx_glow_pop(color, intensity, softness, duration):
            xcenter cx
            ycenter cy
            xysize (int(w), int(h))

# One-shot expanding shock ring at a point.
screen msbf_shock_ring(cx, cy, size, color=(1.0, 0.22, 0.41), thickness=0.10, intensity=1.0, duration=0.55):
    if MSBF_FX_SHADERS:
        add Solid("#00000000") at msbf_fx_ring_t(color, thickness, intensity, duration):
            xcenter cx
            ycenter cy
            xysize (int(size), int(size))


# Per-phase generative atmosphere field. scope "screen" (1280x720, full backdrop)
# or "stage" (786x458, boss arena). One GPU draw replaces the old Solid swarm; a
# no-op without shaders (the bg art + dim still carry the scene).
screen msbf_atmos_field(phase=1, scope="screen"):
    if MSBF_FX_SHADERS:
        $ _acfg = msbf_atmos_cfg(phase)
        $ _stage = (scope == "stage")
        $ _aw, _ah = (786, 458) if _stage else (1280, 720)
        $ _ai = _acfg["intensity"] * (0.85 if _stage else 1.0)
        $ _av = _acfg["vig"] * (0.45 if _stage else 1.0)
        # Sized by msbf_fx_scaled, not here -- see perf.rpy. Three fbm samples
        # per pixel over the whole frame makes this the most expensive shader
        # per unit area in the file, and its signal is a handful of soft blobs,
        # so it is the one that loses least by being rendered small.
        add msbf_fx_scaled(At(Solid("#00000000"), msbf_fx_atmos_t(_acfg["a"], _acfg["b"], _acfg["c"], _ai, _acfg["warp"], _acfg["rays"], _acfg["scan"], _acfg["flow"], _acfg["grain"], _av, _acfg["jitter"])), _aw, _ah)


# One floating combat number positioned at (x, y) centre.
screen msbf_float_number(ftext, fstyle, x, y, dx=0.0, crit=False):
    $ _fnx = int(x)
    $ _fny = int(y)
    if crit:
        text ftext style fstyle at msbf_float_rise_crit(dx):
            xpos _fnx
            ypos _fny
            xanchor 0.5
            yanchor 0.5
    else:
        text ftext style fstyle at msbf_float_rise(dx):
            xpos _fnx
            ypos _fny
            xanchor 0.5
            yanchor 0.5

# Formats a floating amount for display (heals get a leading +).
init -1 python:
    def msbf_float_label(amount, kind):
        if kind == "heal":
            return "+%s" % amount
        return "%s" % amount

    MSBF_FLOAT_STYLE = {
        "dmg": "msbf_float_dmg",
        "crit": "msbf_float_crit",
        "weak": "msbf_float_weak",
        "resist": "msbf_float_resist",
        "heal": "msbf_float_heal",
        "enemy": "msbf_float_enemy",
        "miss": "msbf_float_miss",
    }

# One-shot spark burst at a point (uses the project's ParticleBurst).
screen msbf_spark_burst(x=640, y=360, count=40, life=0.65, sx=8.0, sy=9.0):
    add ParticleBurst("msbf_fx_p_spark", numParticles=count, particleTime=life, particleXSpeed=sx, particleYSpeed=sy).sm:
        pos (x, y)
    timer life + 0.15 action Hide("msbf_spark_burst")


# -----------------------------------------------------------------------------
# Bullet-hell HUD: spell-card banner + keyboard-control indicator.
# -----------------------------------------------------------------------------
# The shmup overlay rebuilds every tick, but Matsu'Py preserves an at-transform's
# timebase across same-identity re-runs, so this one-shot fade plays once at the
# start of each Curtain Script cast (and replays on the next cast, since the
# overlay is hidden in between).
transform msbf_shmup_hint:
    subpixel True
    alpha 0.0
    yoffset 10
    easein 0.30 alpha 1.0 yoffset 0
    pause 2.1
    easeout 0.55 alpha 0.0
    pause 2.7
    easeout 0.65 alpha 0.0 yoffset -8

style msbf_shmup_card_kicker:
    size 13
    color "#ff6b8f"
    bold True
    kerning 4.0
    outlines [(2, "#02040b", 0, 0)]

style msbf_shmup_card_name:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 30
    color "#f5fbff"
    bold True
    kerning 2.0
    outlines [(3, "#02040b", 0, 0), (1, "#ff386899", 1, 1)]

style msbf_shmup_controls_big:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 22
    color "#bfe9ff"
    bold True
    kerning 2.0
    outlines [(3, "#02040b", 0, 0)]

style msbf_shmup_controls_small:
    size 12
    color "#7fa6bd"
    bold True
    kerning 2.0
    outlines [(1, "#02040b", 0, 0)]


# -----------------------------------------------------------------------------
# Battle HUD styles (SMT/Persona banner + left tempo rail).
# -----------------------------------------------------------------------------
style msbf_rail_kicker:
    size 12
    color "#6f93a8"
    bold True
    kerning 4.0
    outlines [(1, "#02040b", 0, 0)]

style msbf_rail_actor:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 23
    color "#f5fbff"
    bold True
    kerning 1.0
    outlines [(2, "#02040b", 0, 0)]

style msbf_banner_phase:
    size 13
    color "#bfe9ff"
    bold True
    kerning 3.0
    outlines [(2, "#02040b", 0, 0)]

style msbf_banner_name:
    size 20
    color "#ffffff"
    bold True
    kerning 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#ff386aaa", 1, 1)]


# -----------------------------------------------------------------------------
# Party-select dossier styles.
# -----------------------------------------------------------------------------
style msbf_dossier_button is button:
    xsize 712
    ysize 60
    padding (0, 0)
    insensitive_background Solid("#070d15e0")

style msbf_dossier_mug:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 28
    color "#ffffff"
    bold True
    outlines [(2, "#02040b", 0, 0)]

style msbf_dossier_name:
    size 19
    color "#f5fbff"
    bold True
    outlines [(2, "#02040b", 0, 0)]

style msbf_dossier_role:
    size 12
    color "#55ddff"
    bold True
    kerning 1.5
    outlines [(1, "#02040b", 0, 0)]

style msbf_dossier_summary:
    size 11
    color "#9fb6c6"
    outlines [(1, "#02040b", 0, 0)]

style msbf_dossier_order:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 20
    color "#ffcf66"
    bold True
    outlines [(2, "#02040b", 0, 0)]


# =============================================================================
# 6. DRAMA LAYER -- cast wind-up, turn-handoff banners, and KO sequences.
# -----------------------------------------------------------------------------
# Built on top of the existing cue bus; NONE of this changes combat rules. The
# battle screen (ui.rpy) drives it: a short deferred "commit" on player actions
# (cast -> projectile -> impact), a one-shot banner whenever the turn changes,
# and a serial-polled death feed (battle.death_events) that bursts on each KO.
# =============================================================================

# No-op transform so screens can branch: `at (X if cond else msbf_identity)`.
transform msbf_identity:
    alpha 1.0

# A downed party card: just dimmed. The card already marks death with red "DOWN"
# text + a down-styled name, so the dim reinforces it. Deliberately NO rotate
# (a grid frame rotates around its top-left corner and breaks alignment) and NO
# matrixcolor (the card embeds the msbf.bar shader/mesh HP bar, and wrapping a
# mesh child in a colour matrix can mis-composite in gl2).
transform msbf_card_downed:
    subpixel True
    alpha 0.5

# The current actor's card: a soft breathing highlight for its accent frame.
# Alpha-only on purpose -- a grid cell can't be scaled/rotated without breaking
# alignment (same reason as msbf_card_downed above), so the "pulse" the TODO asks
# for is carried by the accent edges fading in and out rather than by geometry.
transform msbf_active_pulse:
    subpixel True
    alpha 0.30
    block:
        easein 0.55 alpha 0.95
        easeout 0.55 alpha 0.30
        repeat

# HP-bar damage trail: a bright slice drawn over the just-lost portion of a bar
# (the UI sizes/places it from the bar_event's frm/to fractions). Anchored to its
# left edge (= the new HP position) and shrunk to zero, so the lost chunk "drains"
# toward the new fill while fading -- the bar reads as animating, not snapping.
transform msbf_bar_chip(dur=0.5):
    subpixel True
    xanchor 0.0
    alpha 0.9
    parallel:
        easeout dur xzoom 0.0
    parallel:
        pause dur * 0.5
        easeout dur * 0.5 alpha 0.0

# HP-bar heal trail: a soft flash over the newly-filled portion. No drain (the
# region just gained HP), just a fade so heals get a matching beat.
transform msbf_bar_flash(dur=0.5):
    subpixel True
    alpha 0.0
    easein dur * 0.25 alpha 0.75
    easeout dur * 0.75 alpha 0.0

# Element-coloured projectile flung caster -> target across the wind-up window,
# so a move reads as cast -> travel -> impact instead of one instant frame.
transform msbf_cast_projectile(x0=0, y0=0, x1=0, y1=0, dur=0.2):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos x0
    ypos y0
    alpha 0.0
    zoom 0.45
    parallel:
        easeout 0.06 alpha 1.0 zoom 1.0
    parallel:
        easein dur xpos x1 ypos y1
    parallel:
        block:
            pause dur * 0.74
            linear dur * 0.26 alpha 0.0



# --- Final blow: HYPERNOVA collapse -----------------------------------------
# The boss does NOT quietly fade. It destabilises -- an escalating tremor that
# squeezes it inward -- then implodes to a single white-hot point, which is
# detonated by the overlay (msbf_nova_*) a beat later. The vanish at the end is
# hidden by the detonation flash, so it reads as the boss being consumed by the
# blast, not disappearing first. Timeline matched to the overlay: tremor to
# ~0.63, implode to a point by ~0.79, point-hold, consumed ~0.85.
transform msbf_boss_collapse:
    subpixel True
    alpha 1.0
    xoffset 0
    yoffset 0
    zoom 1.0
    rotate 0.0
    # destabilise: tremor that escalates while the boss is pulled inward
    linear 0.05 xoffset -9 yoffset 5 rotate -1.8 zoom 0.995
    linear 0.05 xoffset 11 yoffset -5 rotate 2.1 zoom 0.99
    linear 0.045 xoffset -13 yoffset 6 rotate -2.4 zoom 0.985
    linear 0.045 xoffset 14 yoffset -7 rotate 2.7 zoom 0.975
    linear 0.04 xoffset -16 yoffset 8 rotate -3.0 zoom 0.965
    linear 0.04 xoffset 17 yoffset -8 rotate 3.3 zoom 0.95
    linear 0.035 xoffset -20 yoffset 9 rotate -3.8 zoom 0.935
    linear 0.035 xoffset 21 yoffset -10 rotate 4.1 zoom 0.92
    linear 0.03 xoffset -24 rotate -4.6 zoom 0.90
    linear 0.03 xoffset 25 rotate 4.9 zoom 0.88
    linear 0.028 xoffset -28 rotate -5.4 zoom 0.85
    linear 0.028 xoffset 29 rotate 5.8 zoom 0.82
    linear 0.025 xoffset -32 rotate -6.2 zoom 0.78
    linear 0.025 xoffset 33 rotate 6.6 zoom 0.74
    # implosion: snap to a single white-hot point
    easein 0.16 xoffset 0 yoffset 0 rotate 0.0 zoom 0.05
    # hold the point, then get consumed by the detonation flash
    pause 0.06
    linear 0.05 alpha 0.0 zoom 0.0

# --- HYPERNOVA overlay pieces (used by the final-victory overlay) -----------
# Gathering darkness: light drains toward the implosion, then is irrelevant once
# the detonation flash + whiteout take over.
transform msbf_nova_predark:
    alpha 0.0
    easein 0.74 alpha 0.42
    pause 0.06
    linear 0.10 alpha 0.0

# Rings that start huge and collapse INWARD to the boss -- the star eating
# itself before it blows. Stagger several for a continuous suck-in.
transform msbf_nova_inring(delay=0.0, spin=1.0, amax=0.6):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom 2.0
    rotate 0.0
    pause delay
    linear 0.08 alpha amax
    easein 0.60 zoom 0.12 rotate 90.0 * spin
    linear 0.06 alpha 0.0 zoom 0.05

# The gathering core: swells through the implosion, crushes to a pinpoint, then
# blows out as the detonation begins.
transform msbf_nova_core(delay=0.0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom 0.12
    pause delay
    easein 0.66 alpha 0.92 zoom 0.55
    easein 0.07 alpha 1.0 zoom 0.20
    pause 0.04
    linear 0.10 alpha 0.0 zoom 2.6

# --- Shader-backed hypernova pieces -----------------------------------------
# Same timelines to the frame as the Solid versions above (the detonation sfx
# is cued off these delays, so they must not move); only the RENDERING changes.
#
# It mattered most for the core. A white RECTANGLE scaling up is unmistakably a
# rectangle for the whole ~0.5s it spends gathering before the blast, and that
# half-second is the one the player actually looks at -- everything after it is
# hidden under the whiteout. The collapsing rings had the same problem in a
# different form: they were 1400x4 bars rotating 90 degrees, which reads as a
# spinning line, not a ring rushing inward.

# The gathering core, as real light.
transform msbf_nova_core_glow(delay=0.0, color=(1.0, 1.0, 1.0)):
    mesh True
    shader "msbf.glow"
    u_color color
    u_softness 1.5
    u_intensity 1.0
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom 0.12
    pause delay
    easein 0.66 alpha 0.92 zoom 0.55
    easein 0.07 alpha 1.0 zoom 0.20
    pause 0.04
    linear 0.10 alpha 0.0 zoom 2.6

# Rings collapsing INWARD. msbf.ring fades as u_progress rises, so driving it
# backwards (0.98 -> 0.06) gives exactly the read the beat wants for free: the
# ring rushes in and brightens as it goes.
transform msbf_nova_inring_r(delay=0.0, color=(1.0, 1.0, 1.0), amax=0.6):
    mesh True
    shader "msbf.ring"
    u_color color
    u_thickness 0.055
    u_intensity amax * 2.8
    u_progress 0.98
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    pause delay
    linear 0.08 alpha 1.0
    easein 0.60 u_progress 0.06
    linear 0.06 alpha 0.0

# The outward blast waves. Here the shader's built-in fade is already the right
# way round, so progress just runs forward.
transform msbf_big_shock_r(delay=0.0, color=(1.0, 1.0, 1.0), amax=0.85):
    mesh True
    shader "msbf.ring"
    u_color color
    u_thickness 0.048
    u_intensity amax * 2.4
    u_progress 0.02
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    pause delay
    linear 0.05 alpha 1.0
    linear 0.44 u_progress 0.98

# The detonation flash: a hard, fast full-screen white spike.
transform msbf_nova_flash(delay=0.0, peak=1.0):
    alpha 0.0
    pause delay
    linear 0.03 alpha peak
    linear 0.24 alpha 0.0

# The whiteout BLOOMS outward from the detonation point and fills the screen
# fast, instead of a slow flat fade -- the shockwave of light reaching the lens.
transform msbf_nova_whiteout(delay=0.85):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    zoom 0.0
    alpha 0.0
    pause delay
    easeout 0.04 alpha 1.0 zoom 0.3
    easein 0.52 zoom 3.4

# --- DEFEAT sequence pieces (party wipe) ------------------------------------
# A party wipe is no longer a flat fade: the final blow concusses the UI, the
# colour drains into a dark-red filmic wash, the boss looms with an oppressive
# glow over a heartbeat pulse, a verdict title trembles in, then darkness
# letterboxes shut and crushes to black. Timeline ~3.4s -> finish_defeat.

# Concussion shake for the battle frames on the killing blow.
transform msbf_defeat_rumble(strength=1.0):
    subpixel True
    xoffset 0
    yoffset 0
    linear 0.03 xoffset -11 * strength yoffset 6 * strength
    linear 0.03 xoffset 10 * strength yoffset -5 * strength
    linear 0.04 xoffset -8 * strength yoffset 5 * strength
    linear 0.04 xoffset 7 * strength yoffset -3 * strength
    linear 0.06 xoffset -5 * strength yoffset 3 * strength
    linear 0.06 xoffset 4 * strength yoffset -2 * strength
    linear 0.09 xoffset -2 * strength yoffset 1 * strength
    easeout 0.5 xoffset 0 yoffset 0

# Red concussion flash on the final blow.
transform msbf_defeat_flash:
    alpha 0.0
    easeout 0.04 alpha 0.72
    easein 0.55 alpha 0.0

# Strength drains: a dark-red filmic vignette/grain that ramps in (shader).
transform msbf_defeat_postfx(tint=(0.17, 0.015, 0.04)):
    mesh True
    shader "msbf.postfx"
    u_tint tint
    u_intensity 0.0
    easein 2.0 u_intensity 1.7

# Oppressive red loom swelling from the boss (shader glow, then a slow throb).
transform msbf_defeat_loom_glow(color=(0.82, 0.10, 0.20)):
    mesh True
    shader "msbf.glow"
    u_color color
    u_softness 1.5
    u_intensity 0.0
    easein 1.5 u_intensity 0.85
    block:
        easein 0.7 u_intensity 0.62
        easeout 0.7 u_intensity 0.9
        repeat

# Heartbeat pulse of darkness.
transform msbf_defeat_pulse:
    alpha 0.0
    block:
        easein 0.55 alpha 0.20
        easeout 0.55 alpha 0.05
        repeat

# The boss towers over the fallen party.
transform msbf_boss_loom:
    subpixel True
    alpha 1.0
    zoom 1.0
    xoffset 0
    yoffset 0
    rotate 0.0
    easein 1.6 zoom 1.13 yoffset -12
    block:
        easein 0.85 zoom 1.155 yoffset -16
        easeout 0.85 zoom 1.125 yoffset -10
        repeat

# Darkness closes in -- top/bottom letterbox bars slide to meet, then a full
# blackout guarantees a clean black hand-off to the story's game-over.
transform msbf_defeat_letterbox_top(delay=0.0):
    subpixel True
    yoffset -460
    pause delay
    easein 1.1 yoffset 0

transform msbf_defeat_letterbox_bottom(delay=0.0):
    subpixel True
    yoffset 460
    pause delay
    easein 1.1 yoffset 0

transform msbf_defeat_blackout:
    alpha 0.0
    pause 2.4
    easein 0.95 alpha 1.0

# --- Turn-handoff banner -----------------------------------------------------
transform msbf_turn_banner_card:
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    xoffset -54
    zoom 1.04
    easeout 0.18 alpha 1.0 xoffset 0 zoom 1.0
    pause 0.62
    easein 0.30 alpha 0.0 xoffset 46 zoom 1.02

# The sweep bars behind the turn card. They animate xOFFSET, not xpos: the
# screen positions them with `xcenter 640`, and a transform that sets xpos wins
# over that, so animating xpos to 0 parked both bars centred on the screen's
# LEFT EDGE -- half off-frame, nowhere near the card they belong to.
transform msbf_turn_banner_bar(delay=0.0, w=720, dirn=1.0):
    subpixel True
    xoffset -w * dirn
    alpha 0.0
    pause delay
    linear 0.16 alpha 1.0 xoffset 0
    pause 0.52
    linear 0.26 alpha 0.0 xoffset w * dirn

transform msbf_turn_banner_flash:
    alpha 0.0
    easeout 0.08 alpha 0.30
    easein 0.34 alpha 0.0

# --- KO burst ----------------------------------------------------------------
transform msbf_death_shard(dx=0.0, dy=0.0, dur=0.62):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    zoom 0.5
    rotate 0.0
    parallel:
        easeout 0.07 alpha 1.0 zoom 1.0
        block:
            pause dur * 0.4
            linear dur * 0.6 alpha 0.0
    parallel:
        easeout dur xoffset dx yoffset dy rotate dx * 0.5

transform msbf_death_label:
    subpixel True
    xanchor 0.5
    yanchor 0.5
    alpha 0.0
    yoffset 6
    zoom 0.8
    easeout 0.12 alpha 1.0 yoffset -10 zoom 1.05
    ease 0.10 zoom 1.0
    pause 0.55
    linear 0.32 alpha 0.0 yoffset -26

# One-shot KO burst at a card/sprite centre: an implosion ring, a fan of shards,
# a spark pop, and a rising tag. color keys party (red) vs boss (white-gold).
screen msbf_death_burst(x=0, y=0, color="#ff3868", boss=False):
    $ _dcx = int(x)
    $ _dcy = int(y)
    $ _dcol = msbf_hex_rgb(color)
    $ _dsize = 360 if boss else 150
    use msbf_glow_pop(_dcx, _dcy, _dsize, _dsize, _dcol, 0.9, 1.4, 0.5)
    if MSBF_FX_SHADERS:
        add Solid("#00000000") at msbf_fx_ring_t(_dcol, 0.12, 1.0, 0.5):
            xcenter _dcx
            ycenter _dcy
            xysize (_dsize, _dsize)
    $ _shard_n = 10 if boss else 7
    for _si in range(_shard_n):
        $ _sang = (6.2832 * _si / float(_shard_n)) + (_dcx % 7) * 0.11
        $ _sdist = (90.0 if boss else 52.0) * (0.7 + (_si % 3) * 0.2)
        $ _sdx = _sdist * math.cos(_sang)
        $ _sdy = _sdist * math.sin(_sang) - (10.0 if not boss else 0.0)
        add Solid(color) xysize ((9 if boss else 6), (3 if boss else 2)) at msbf_death_shard(_sdx, _sdy, 0.6):
            xpos _dcx
            ypos _dcy
    if not boss:
        text "DOWN" style "msbf_death_tag" at msbf_death_label:
            xpos _dcx
            ypos _dcy - 14

style msbf_death_tag:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 20
    color "#ff6b8f"
    bold True
    kerning 2.0
    outlines [(3, "#02040b", 0, 0), (1, "#ff3868", 1, 1)]

style msbf_turn_banner_kicker:
    size 12
    color "#cfe8f5"
    bold True
    kerning 6.0
    outlines [(2, "#02040b", 0, 0)]

style msbf_turn_banner_name:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 40
    color "#f5fbff"
    bold True
    kerning 3.0
    outlines [(3, "#02040b", 0, 0), (1, "#00000088", 2, 2)]

style msbf_turn_banner_sub:
    size 14
    color "#bfe9ff"
    bold True
    kerning 2.0
    outlines [(2, "#02040b", 0, 0)]

# The banner itself: a centred name plate with sweeping accent bars. `token` is
# only here to force a fresh transform timebase when the turn changes.
screen msbf_turn_banner(token, label, accent="#55ddff", accent2="#ff3868", sub="", kicker="TEMPO"):
    add Solid(accent) xysize (1280, 86) at msbf_turn_banner_flash:
        ycenter 300
    fixed:
        xysize (1280, 720)
        add Solid(accent + "ee") xysize (560, 6) at msbf_turn_banner_bar(0.0, 760, 1.0):
            xcenter 640
            ycenter 262
        add Solid(accent2 + "cc") xysize (420, 4) at msbf_turn_banner_bar(0.05, 760, -1.0):
            xcenter 640
            ycenter 340
        vbox:
            xcenter 640
            ycenter 300
            spacing 0
            at msbf_turn_banner_card
            text kicker style "msbf_turn_banner_kicker" xalign 0.5
            text label style "msbf_turn_banner_name" xalign 0.5
            if sub:
                text sub style "msbf_turn_banner_sub" xalign 0.5
