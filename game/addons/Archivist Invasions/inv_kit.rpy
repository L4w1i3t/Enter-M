# Shared presentation kit for the Archivist Invasions (Oct 2 2026 makeover).
#
# What lives here, and why it is shared rather than per fight:
#   * THE FX ART. Original textures, drawn procedurally
#     into fx/. Nothing in the invasions crops a ripped sheet any more (user
#     decision, Oct 2 2026) -- beams, bolts, sparks, rings, smoke, shards,
#     paper scraps, ink, chalk glyphs, picture frames, corridor masses.
#   * InvFX, a particle system the GAME object owns and steps on its own
#     tick. Pause freezes it and every frame stays a pure function of the
#     simulation, which is the draw-rate-is-tick-rate rule every stage keeps.
#     Decoration only: nothing in here may ever own a hitbox.
#   * InvPaint, the per-frame painter the four stages draw through: one
#     render cache per frame, quantised texture quads for lines and rings
#     (canvas strokes are software rasterised and re-uploaded every frame;
#     quads are free on the GPU), and two targets -- WORLD and HUD.
#   * THE LENS. The whole world is rendered to one texture and finished in
#     one shader pass: grade, bloom sampled off the texture's own mip chain,
#     radial aberration, barrel, a travelling shockwave, row tear, grain,
#     vignette and flash. The HUD is drawn AFTER it, so text never smears.
#     This is what makes a sprite sit IN a room instead of on top of a
#     backdrop: one light response, one grain, one bloom over everything.
#   * Panel chrome, the turn LOG (the readouts no longer block on a key --
#     they stay on screen until the next turn replaces them, so a slow reader
#     loses nothing and nobody presses Z three times a turn), and the retry
#     overlay with a checkpoint at the tear.
#
# Shader names added here: inv.lens, inv.panel, inv.sheet. See invasions.rpy
# for the full namespace -- register_shader replaces a taken name silently.

init -9 python:
    INV_LENS_OK = False
    INV_PANEL_OK = False

    def _inv_register_kit_shaders():
        renpy.register_shader("inv.lens", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_lens_res;
            uniform float u_lens_time;
            uniform vec4 u_lens_grade;
            uniform vec3 u_lens_lift;
            uniform vec3 u_lens_gain;
            uniform vec4 u_lens_fx;
            uniform vec4 u_lens_vig;
            uniform vec3 u_lens_flashc;
            uniform vec4 u_lens_shock;
            uniform vec4 u_lens_tear;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float lens_hash(vec2 p) {
                return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
            }
        """, fragment_300="""
            // u_lens_grade  (exposure, contrast, saturation, bloom tint mix)
            // u_lens_fx     (bloom, bloom threshold, aberration, grain)
            // u_lens_vig    (vignette, vignette radius, barrel, flash)
            // u_lens_shock  (x px, y px, radius px, strength)
            // u_lens_tear   (amount, seed, band centre 0..1, band width)
            vec2 res = max(u_lens_res, vec2(1.0));
            float asp = res.x / res.y;
            vec2 uv = v_tex_coord;
            vec2 c = uv - 0.5;

            // BARREL. A lens, not a filter: the frame bows a little, more at
            // the corners, and the amount is a uniform so a fight can lean on
            // it at its worst moments.
            vec2 ca2 = c * vec2(asp, 1.0);
            float r2 = dot(ca2, ca2);
            uv = 0.5 + c * (1.0 + u_lens_vig.z * r2);

            // A SHOCKWAVE travelling outward from an impact: a ring of
            // refraction, so a heavy hit moves the room rather than tinting it.
            if (u_lens_shock.w > 0.001) {
                vec2 sp = u_lens_shock.xy / res;
                vec2 d = (uv - sp) * vec2(asp, 1.0);
                float dist = length(d);
                float R = u_lens_shock.z / res.y;
                float w = 0.030 + R * 0.10;
                float band = exp(-((dist - R) * (dist - R)) / (w * w));
                uv -= (d / max(dist, 1e-4)) / vec2(asp, 1.0) * band * u_lens_shock.w * 0.035;
            }

            // ROW TEAR. Blocks of rows displaced sideways inside a band --
            // the encounter faulting, not the screen being rattled.
            if (u_lens_tear.x > 0.001) {
                float row = floor(uv.y * 72.0);
                float h = lens_hash(vec2(row, u_lens_tear.y));
                float inband = 1.0 - smoothstep(u_lens_tear.w * 0.5, u_lens_tear.w,
                                                abs(uv.y - u_lens_tear.z));
                uv.x += (h - 0.5) * 0.11 * u_lens_tear.x * step(0.55, h) * inband;
            }

            // RADIAL ABERRATION -- grows toward the corners.
            vec2 dir = (uv - 0.5);
            float ca = u_lens_fx.z * (0.35 + 1.30 * r2);
            vec3 col;
            col.r = texture2D(tex0, uv + dir * ca).r;
            col.g = texture2D(tex0, uv).g;
            col.b = texture2D(tex0, uv - dir * ca).b;

            // BLOOM off the texture's own mip chain: three blurred reads at
            // increasing radius, thresholded, added back. Three fetches for a
            // glow that would otherwise need a separate blur pass.
            if (u_lens_fx.x > 0.001) {
                vec3 b = texture2D(tex0, uv, 2.5).rgb * 0.30
                       + texture2D(tex0, uv, 4.0).rgb * 0.38
                       + texture2D(tex0, uv, 5.5).rgb * 0.32;
                float th = clamp(u_lens_fx.y, 0.0, 0.95);
                b = max(b - vec3(th), vec3(0.0)) / (1.0 - th);
                // A bloom keeps its colour, then leans toward white where it
                // is hottest -- light that is too bright to have a colour.
                float bl = dot(b, vec3(0.299, 0.587, 0.114));
                b = mix(b, vec3(bl), u_lens_grade.w * smoothstep(0.4, 1.4, bl));
                col += b * u_lens_fx.x;
            }

            // GRADE: exposure, contrast about mid-grey, saturation, then a
            // lift/gain pair that tints the shadows and the highlights.
            col *= u_lens_grade.x;
            col = (col - 0.5) * u_lens_grade.y + 0.5;
            float l = dot(col, vec3(0.299, 0.587, 0.114));
            col = mix(vec3(l), col, u_lens_grade.z);
            col = u_lens_lift + max(col, vec3(0.0)) * (u_lens_gain - u_lens_lift);

            // VIGNETTE.
            float vr = length(c * vec2(1.0, 0.86)) * 1.41421;
            float vig = 1.0 - smoothstep(u_lens_vig.y * 0.38, u_lens_vig.y, vr);
            col *= mix(1.0, vig, clamp(u_lens_vig.x, 0.0, 1.0));

            // GRAIN, signed (an unsigned grain only ever lifts the image and
            // reads as a veil), on drawable pixels, moving.
            float n = lens_hash(gl_FragCoord.xy + vec2(fract(u_lens_time * 7.13) * 413.0,
                                                       fract(u_lens_time * 3.71) * 271.0)) - 0.5;
            col += n * u_lens_fx.w;

            col = mix(col, u_lens_flashc, clamp(u_lens_vig.w, 0.0, 1.0));
            gl_FragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
        """)

        # PANEL CHROME. One quad, drawn in the shader: a cut-corner plate with
        # a vertical gradient, a border, an inset rule, optional scanlines and
        # a registration split on the border (Biography's). Premultiplied.
        renpy.register_shader("inv.panel", variables="""
            uniform vec2 u_pn_size;
            uniform vec4 u_pn_top;
            uniform vec4 u_pn_bot;
            uniform vec4 u_pn_edge;
            uniform vec4 u_pn_shape;
            uniform vec4 u_pn_tex;
            uniform vec4 u_pn_accent;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float pn_hash(vec2 p) {
                return fract(sin(dot(p, vec2(41.37, 289.11))) * 23421.631);
            }
            // Signed distance INTO a cut-corner rectangle (positive inside).
            float pn_dist(vec2 p, vec2 s, float cut) {
                float d = min(min(p.x, s.x - p.x), min(p.y, s.y - p.y));
                vec2 q = min(p, s - p);
                float dc = (q.x + q.y - cut) * 0.70710678;
                return min(d, dc);
            }
        """, fragment_300="""
            // u_pn_shape (border width, corner cut, inset rule distance, inset rule alpha)
            // u_pn_tex   (noise, scanlines, border split px, accent tick length)
            vec2 s = max(u_pn_size, vec2(4.0));
            vec2 p = v_tex_coord * s;
            float d = pn_dist(p, s, u_pn_shape.y);
            float inside = smoothstep(-0.6, 0.6, d);

            vec4 fill = mix(u_pn_top, u_pn_bot, clamp(p.y / s.y, 0.0, 1.0));
            float n = pn_hash(floor(p * 0.5));
            fill.rgb *= 1.0 + (n - 0.5) * u_pn_tex.x;
            fill.rgb *= 1.0 - u_pn_tex.y * step(0.5, fract(p.y * 0.5));

            vec3 rgb = fill.rgb * fill.a * inside;
            float a = fill.a * inside;

            // Inset rule.
            float il = (1.0 - smoothstep(0.0, 1.1, abs(d - u_pn_shape.z))) * inside
                     * u_pn_shape.w;
            rgb = rgb * (1.0 - il) + u_pn_accent.rgb * il;
            a = max(a, il);

            // Border, and its registration split (two offset copies in the
            // accent colour, one each side) when u_pn_tex.z is non-zero.
            float bw = u_pn_shape.x;
            float border = smoothstep(bw + 0.6, bw - 0.6, d) * inside;
            if (u_pn_tex.z > 0.01) {
                float dl = pn_dist(p - vec2(u_pn_tex.z, 0.0), s, u_pn_shape.y);
                float dr = pn_dist(p + vec2(u_pn_tex.z, 0.0), s, u_pn_shape.y);
                float bl = smoothstep(bw + 0.6, bw - 0.6, dl) * smoothstep(-0.6, 0.6, dl);
                float br = smoothstep(bw + 0.6, bw - 0.6, dr) * smoothstep(-0.6, 0.6, dr);
                float sa = max(bl, br) * (1.0 - border) * 0.75;
                vec3 sc = mix(u_pn_accent.rgb, vec3(1.0, 0.18, 0.30), step(bl, br));
                rgb = rgb * (1.0 - sa) + sc * sa;
                a = max(a, sa);
            }
            float ea = u_pn_edge.a * border;
            rgb = rgb * (1.0 - ea) + u_pn_edge.rgb * ea;
            a = a * (1.0 - ea) + ea;

            // Corner ticks: short accent strokes along each edge from the
            // corner cuts -- a case file's corners, a camera's frame lines.
            if (u_pn_tex.w > 0.5) {
                vec2 q = min(p, s - p);
                float along = max(q.x, q.y);
                float edge = min(q.x, q.y);
                float tick = step(along, u_pn_shape.y + u_pn_tex.w)
                           * (1.0 - smoothstep(bw + 2.0, bw + 3.4, edge))
                           * step(bw + 0.4, edge) * u_pn_accent.a;
                rgb = rgb * (1.0 - tick) + u_pn_accent.rgb * tick;
                a = max(a, tick);
            }
            gl_FragColor = vec4(rgb, a);
        """)

        # A FLAT THING IN 3D. Maps the child texture onto an arbitrary quad by
        # the inverse of a projective (square-to-quad) transform handed in as
        # three rows, so a sheet of paper can hang, sway and fall flat without
        # a 3D stage. Shades by how squarely it faces the light, darkens its
        # own torn edge, and is clipped exactly at the quad. Premultiplied.
        renpy.register_shader("inv.sheet", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_sh_size;
            uniform vec3 u_sh_r0;
            uniform vec3 u_sh_r1;
            uniform vec3 u_sh_r2;
            uniform vec4 u_sh_crop;
            uniform vec4 u_sh_light;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            // u_sh_crop  (u0, v0, u1, v1): where the sheet sits in tex0
            // u_sh_light (facing brightness, top-to-bottom falloff, edge dark, alpha)
            vec2 pxy = v_tex_coord * u_sh_size;
            vec3 q = vec3(dot(u_sh_r0, vec3(pxy, 1.0)),
                          dot(u_sh_r1, vec3(pxy, 1.0)),
                          dot(u_sh_r2, vec3(pxy, 1.0)));
            vec2 st = q.xy / (abs(q.z) < 1e-6 ? 1e-6 : q.z);
            float inside = step(0.0, st.x) * step(st.x, 1.0)
                         * step(0.0, st.y) * step(st.y, 1.0) * step(0.0, q.z);
            vec2 suv = mix(u_sh_crop.xy, u_sh_crop.zw, clamp(st, 0.0, 1.0));
            vec4 c = texture2D(tex0, suv) * inside;
            float edge = min(min(st.x, 1.0 - st.x), min(st.y, 1.0 - st.y));
            float rim = 1.0 - smoothstep(0.0, 0.018, edge);
            float shade = u_sh_light.x * (1.0 - u_sh_light.y * st.y);
            c.rgb *= shade * (1.0 - u_sh_light.z * rim);
            c *= u_sh_light.w;
            gl_FragColor = vec4(min(c.rgb, vec3(c.a)), c.a);
        """)

    try:
        _inv_register_kit_shaders()
        INV_LENS_OK = True
        INV_PANEL_OK = True
    except Exception as _inv_kit_e:
        INV_LENS_OK = False
        INV_PANEL_OK = False
        try:
            renpy.log("INV KIT: shader registration failed: %r" % _inv_kit_e)
        except Exception:
            pass


init -7 python:
    import math
    import json as _inv_json

    # --- THE FX ART ----------------------------------------------------------
    INV_FX_DIR = INV_DIR + "fx/"
    INV_FX_OK = True
    try:
        with renpy.open_file(INV_FX_DIR + "fx_sizes.json") as _inv_fh:
            INV_FX_SIZES = dict((k, tuple(v)) for k, v in
                                _inv_json.loads(_inv_fh.read().decode("utf-8")).items())
    except Exception as _inv_fx_e:
        INV_FX_SIZES = {}
        INV_FX_OK = False
        try:
            renpy.log("INV KIT: fx_sizes.json unreadable: %r" % _inv_fx_e)
        except Exception:
            pass

    INV_BOLTS = ("bolt_0", "bolt_1", "bolt_2", "bolt_3")
    INV_SMOKES = ("smoke_0", "smoke_1", "smoke_2", "smoke_3")
    INV_SHARDS = ("shard_0", "shard_1", "shard_2", "shard_3")
    INV_SCRAPS = ("scrap_0", "scrap_1", "scrap_2", "scrap_3")
    INV_INKS = ("ink_0", "ink_1", "ink_2", "ink_3")
    INV_MASSES = ("mass_0", "mass_1", "mass_2", "mass_3", "mass_4", "mass_5")
    INV_GLYPHS = tuple("glyph_%02d" % i for i in range(12))

    def inv_fx_img(name):
        """An fx/ texture by name -- or any image path (a fight's own art,
        e.g. Biography's spectral glaive) passed through as-is."""
        if name.endswith(".png") or name.endswith(".webp"):
            return name
        return INV_FX_DIR + name + ".png"

    def inv_fx_size(name):
        return INV_FX_SIZES.get(name, (64, 64))

    # ONE displayable object per image path, for the life of the process.
    # A room's Model (or mesh Transform) is rebuilt every frame because its
    # uniforms move every frame, and the engine reuses a texture it already
    # made only while it can match the child to last frame's render.
    # renpy.displayable(path) returns a new Image on every call; here the
    # engine's Image equality happened to match them anyway (measured Oct 9
    # 2026: no change), so this makes the reuse guaranteed rather than
    # incidental. In the Matsuda fight's pixel stage the same pattern was NOT
    # matched and cost 42% of the GPU frame -- see msbf_px_disp.
    # Not saved: init-time dict, filled lazily.
    _INV_DISPS = {}

    def inv_disp(path):
        d = _INV_DISPS.get(path)
        if d is None:
            d = _INV_DISPS[path] = renpy.displayable(path)
        return d

    def inv_fx_register(path, w, h):
        """Let a fight's own image be drawn as a particle at its true size."""
        INV_FX_SIZES[path] = (int(w), int(h))

    def inv_lerp_tuple(a, b, t):
        return tuple(inv_lerp(float(x), float(y), t) for x, y in zip(a, b))

    def inv_lerp_tint(a, b, t, amount=1.0):
        """Two RGB key tints blended -> the (r, g, b, amount) a body shader
        takes."""
        r, g_, b_ = inv_lerp_tuple(a, b, t)
        return (r, g_, b_, float(amount))

    def inv_lerp_rim(a, b, t):
        return inv_lerp_tuple(a, b, t)

    def inv_hex(col, alpha=None):
        """'#rrggbb' (+ optional alpha 0..1) -> '#rrggbbaa'."""
        if alpha is None:
            return col
        return col[:7] + "%02x" % int(inv_clamp(alpha, 0.0, 1.0) * 255)

    # --- THE PARTICLES -------------------------------------------------------
    class InvFX(object):
        """Decorative particles, stepped by the game object that owns them.

        A particle is a plain dict (cheap to step, trivially picklable):
          t     texture name in fx/
          x y   position -- SCREEN space, or WORLD space when the drawing
                stage hands inv_fx_paint a projection
          h     height above the boards (world-space users only)
          life/age (age < 0 is a delay before it appears)
          s0 s1 start/end scale, r/vr rotation, c tint, a alpha, add blend,
          k     stretch: >0 aligns the quad to its velocity and lengthens it
                with speed (sparks, streaks)
          L     layer name -- each stage decides what each layer sits on
                (under the bodies, over them, on the floor...)
        """

        def __init__(self, cap=380, seed=None):
            self.parts = []
            self.cap = int(cap)
            self.rng = inv_random.Random(seed)

        def clear(self, layer=None):
            if layer is None:
                self.parts = []
            else:
                self.parts = [p for p in self.parts if p["L"] != layer]

        def emit(self, tex, x, y, vx=0.0, vy=0.0, life=30, size=1.0,
                 size1=None, rot=0.0, vrot=0.0, col="#ffffff", alpha=1.0,
                 add=True, drag=1.0, ay=0.0, layer="front", stretch=0.0,
                 fade="out", h=0.0, vh=0.0, delay=0, ah=0.0, sq=None):
            if len(self.parts) >= self.cap:
                self.parts.pop(0)
            p = {"t": tex, "x": float(x), "y": float(y), "vx": float(vx),
                 "vy": float(vy), "life": max(1, int(life)),
                 "age": -int(delay), "s0": float(size),
                 "s1": float(size if size1 is None else size1),
                 "r": float(rot), "vr": float(vrot), "c": col,
                 "a": float(alpha), "add": bool(add), "drag": float(drag),
                 "ay": float(ay), "L": layer, "k": float(stretch),
                 "f": fade, "h": float(h), "vh": float(vh), "ah": float(ah)}
            if sq is not None:
                p["sq"] = float(sq)
            self.parts.append(p)
            return p

        def burst(self, tex, x, y, n, speed=(1.0, 4.0), life=(18, 34),
                  size=(0.4, 1.0), size1=None, col="#ffffff", alpha=1.0,
                  add=True, drag=0.92, ay=0.0, layer="front", angle=0.0,
                  spread=360.0, stretch=0.0, rot=None, vrot=(0.0, 0.0),
                  fade="out", h=0.0, vh=(0.0, 0.0), jitter=0.0, ah=0.0,
                  delay=(0, 0), squash=1.0):
            rng = self.rng
            texs = tex if isinstance(tex, (tuple, list)) else (tex,)
            for _i in range(int(n)):
                a = math.radians(angle + rng.uniform(-spread * 0.5, spread * 0.5))
                sp = rng.uniform(speed[0], speed[1])
                s = rng.uniform(size[0], size[1])
                s1 = None
                if size1 is not None:
                    s1 = s * size1
                self.emit(texs[rng.randrange(len(texs))],
                          x + rng.uniform(-jitter, jitter),
                          y + rng.uniform(-jitter, jitter) * squash,
                          math.cos(a) * sp, math.sin(a) * sp * squash,
                          life=rng.randint(int(life[0]), int(life[1])),
                          size=s, size1=s1,
                          rot=(rng.uniform(0.0, 360.0) if rot is None else rot),
                          vrot=rng.uniform(vrot[0], vrot[1]), col=col,
                          alpha=alpha, add=add, drag=drag, ay=ay, layer=layer,
                          stretch=stretch, fade=fade, h=h,
                          vh=rng.uniform(vh[0], vh[1]), ah=ah,
                          delay=rng.randint(int(delay[0]), int(delay[1])))

        def ring(self, x, y, r0, r1, life=24, col="#ffffff", alpha=0.9,
                 add=True, layer="front", tex="ring", squash=1.0, h=0.0):
            """An expanding ring. Scale is expressed in PIXELS of radius."""
            w = float(inv_fx_size(tex)[0])
            p = self.emit(tex, x, y, life=life, size=(r0 * 2.0) / w,
                          size1=(r1 * 2.0) / w, col=col, alpha=alpha, add=add,
                          layer=layer, fade="out", h=h)
            p["sq"] = float(squash)
            return p

        def step(self):
            keep = []
            for p in self.parts:
                p["age"] += 1
                if p["age"] <= 0:
                    keep.append(p)
                    continue
                if p["age"] >= p["life"]:
                    continue
                dr = p["drag"]
                if dr != 1.0:
                    p["vx"] *= dr
                    p["vy"] *= dr
                    p["vh"] *= dr
                p["vy"] += p["ay"]
                p["vh"] += p["ah"]
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["h"] += p["vh"]
                p["r"] += p["vr"]
                keep.append(p)
            self.parts = keep

    def inv_fx_fade(u, kind):
        if kind == "out":
            return 1.0 - u
        if kind == "out2":
            return (1.0 - u) * (1.0 - u)
        if kind == "pop":
            # Snaps on, holds, falls off late -- a flash, a hit spark.
            return 1.0 if u < 0.25 else max(0.0, 1.0 - (u - 0.25) / 0.75)
        if kind == "inout":
            return math.sin(math.pi * u)
        if kind == "late":
            return 1.0 if u < 0.6 else max(0.0, 1.0 - (u - 0.6) / 0.4)
        return 1.0

    # --- PER-FRAME PAINTER ---------------------------------------------------
    _INV_TF = {}
    _INV_TXT = {}

    def _inv_tf(key, builder):
        d = _INV_TF.get(key)
        if d is None:
            if len(_INV_TF) > 4000:
                _INV_TF.clear()
            d = builder()
            _INV_TF[key] = d
        return d

    def inv_text_disp(text, size, color, font=None, bold=False, outline=None,
                      outline_w=2, kern=None):
        key = (text, size, color, font, bold, outline, outline_w, kern)
        t = _INV_TXT.get(key)
        if t is None:
            if len(_INV_TXT) > 600:
                _INV_TXT.clear()
            kw = dict(size=size, color=color, bold=bold,
                      font=(font or INV_FONT), substitute=False)
            if outline:
                kw["outlines"] = [(outline_w, outline, 0, 0)]
            if kern is not None:
                kw["kerning"] = kern
            t = Text(text, **kw)
            _INV_TXT[key] = t
        return t

    class InvRenderHolder(renpy.Displayable):
        """Hands an already-built Render to a Transform, so a whole frame can
        be put through a mesh shader. A new one is made every frame -- reusing
        one would let the render cache hand back last frame's world."""

        def __init__(self, r, **kw):
            super(InvRenderHolder, self).__init__(**kw)
            self.r = r

        def render(self, width, height, st, at):
            return self.r

    class InvPaint(object):
        """One frame's drawing context. Two targets: `world` (goes through the
        lens) and `hud` (drawn after it, crisp). `target` is whichever is
        current; every helper draws into it."""

        def __init__(self, st, at, w=1280, h=720):
            self.st = st
            self.at = at
            self.w = w
            self.h = h
            self.frame = {}
            self.world = renpy.Render(w, h)
            self.hud = renpy.Render(w, h)
            self.target = self.world
            self._layers = {}

        def to_world(self):
            self.target = self.world

        def to_hud(self):
            self.target = self.hud

        def layer(self, name):
            """A named sub-layer of the current target, created (and so
            z-ordered) on first use -- the floor layer under the bodies, the
            glow layer over them."""
            key = (id(self.target), name)
            lay = self._layers.get(key)
            if lay is None:
                lay = renpy.Render(self.w, self.h)
                self.target.blit(lay, (0, 0))
                self._layers[key] = lay
            return lay

        def tex(self, key, disp, w=1280, h=720):
            e = self.frame.get(key)
            if e is None:
                r = renpy.render(disp, w, h, self.st, self.at)
                e = (r, r.get_size())
                self.frame[key] = e
            return e

        def rect(self, color, w, h):
            w = max(1, int(w))
            h = max(1, int(h))
            key = ("rect", color, w, h)
            e = self.frame.get(key)
            if e is None:
                solid = _inv_tf(("solid", color), lambda c=color: Solid(c))
                e = renpy.render(solid, w, h, self.st, self.at)
                self.frame[key] = e
            return e

        def fill(self, color, x, y, w, h, into=None):
            if w < 1 or h < 1:
                return
            (into or self.target).blit(self.rect(color, w, h), (int(x), int(y)))

        def blit(self, r, pos, into=None):
            (into or self.target).blit(r, (int(pos[0]), int(pos[1])))

        def sblit(self, r, pos, into=None):
            (into or self.target).subpixel_blit(r, pos)

        def text(self, s, size, color, x, y, font=None, bold=False,
                 anchor=(0.0, 0.0), outline=None, w=1200, h=200, into=None,
                 outline_w=2, kern=None):
            t = inv_text_disp(s, size, color, font=font, bold=bold,
                              outline=outline, outline_w=outline_w, kern=kern)
            r, (tw, th) = self.tex(("t", s, size, color, font, bold, outline,
                                    outline_w, kern, w), t, w, h)
            (into or self.target).blit(r, (int(x - tw * anchor[0]),
                                           int(y - th * anchor[1])))
            return (tw, th)

        def quad(self, name, x, y, sx, sy=None, rot=0.0, col="#ffffff",
                 alpha=1.0, add=False, into=None, rstep=3.0, zq=32.0):
            """A texture from fx/, centred on (x, y), scaled by (sx, sy),
            rotated, tinted, alpha'd, normal or additive. Every float that keys
            the cache is quantised, so a swarm costs a handful of textures."""
            if alpha <= 0.01 or sx <= 0.0:
                return
            if sy is None:
                sy = sx
            xq = max(1, int(round(sx * zq)))
            yq = max(1, int(round(abs(sy) * zq)))
            flip = sy < 0.0
            rq = int(round(rot / rstep)) % int(round(360.0 / rstep)) if rot else 0
            aq = max(1, min(32, int(alpha * 32.0 + 0.5)))
            key = ("q", name, xq, yq, flip, rq, aq, col, add, rstep, zq)
            d = _INV_TF.get(key)
            if d is None:
                kw = dict(xzoom=xq / zq, yzoom=(-1.0 if flip else 1.0) * yq / zq,
                          subpixel=True)
                if rq:
                    kw["rotate"] = rq * rstep
                if aq < 32:
                    kw["alpha"] = aq / 32.0
                if col and col.lower() not in ("#ffffff", "#fff"):
                    kw["matrixcolor"] = TintMatrix(col)
                if add:
                    kw["blend"] = "add"
                d = _inv_tf(key, lambda n=name, k=kw: Transform(inv_fx_img(n), **k))
            fw, fh = inv_fx_size(name)
            span = int(max(fw * xq, fh * yq) / zq * 1.5) + 8
            r, (w, h) = self.tex(key, d, span, span)
            (into or self.target).subpixel_blit(r, (x - w * 0.5, y - h * 0.5))

        def line(self, x0, y0, x1, y1, width=2.0, col="#ffffff", alpha=1.0,
                 add=True, tex="beam", into=None, lstep=4.0):
            """A stroke between two points, drawn with a stretched texture."""
            dx = x1 - x0
            dy = y1 - y0
            L = math.hypot(dx, dy)
            if L < 1.0:
                return
            tw, th = inv_fx_size(tex)
            Lq = max(lstep, round(L / lstep) * lstep)
            ang = math.degrees(math.atan2(dy, dx))
            self.quad(tex, (x0 + x1) * 0.5, (y0 + y1) * 0.5, Lq / float(tw),
                      max(0.05, width * 2.6 / float(th)), rot=ang, col=col,
                      alpha=alpha, add=add, into=into, rstep=1.0, zq=64.0)

        def ring(self, x, y, rx, ry=None, col="#ffffff", alpha=1.0, add=True,
                 tex="ring", into=None):
            if ry is None:
                ry = rx
            tw, th = inv_fx_size(tex)
            # The texture's ring sits at 0.86 of its half-width.
            self.quad(tex, x, y, (rx * 2.0 / 0.86) / tw, (ry * 2.0 / 0.86) / th,
                      col=col, alpha=alpha, add=add, into=into, zq=48.0)

        def glow(self, x, y, rx, ry=None, col="#ffffff", alpha=1.0, add=True,
                 into=None, tex="glow"):
            if ry is None:
                ry = rx
            tw, th = inv_fx_size(tex)
            self.quad(tex, x, y, rx * 2.0 / tw, ry * 2.0 / th, col=col,
                      alpha=alpha, add=add, into=into, zq=24.0)

        def shadow(self, x, y, rx, ry, alpha=0.5, into=None):
            """A contact shadow: a soft dark ellipse. The cheapest and by far
            the strongest cue that a figure is standing somewhere."""
            self.glow(x, y, rx, ry, col="#000000", alpha=alpha, add=False,
                      into=into)

    def inv_fx_paint(paint, fx, layer, ox=0.0, oy=0.0, proj=None, scale=1.0,
                     into=None, cull=True):
        """Draw one layer of an InvFX. `proj(x, y, h)` -> (sx, sy, scale) puts
        a world-space particle on screen; without it particles are screen
        space.

        LOW DETAIL (graphics_detail.rpy) draws half of them. These are the
        decorative particles; the half is chosen by a hash of each dict's
        identity, which is stable for its whole life -- a stride over the
        list would flicker as particles die out of the middle of it."""
        low = enter_m_low_detail()
        for p in fx.parts:
            if p["L"] != layer or p["age"] <= 0:
                continue
            if low and ((id(p) * 2654435761) >> 21) & 1:
                continue
            u = p["age"] / float(p["life"])
            a = p["a"] * inv_fx_fade(u, p["f"])
            if a < 0.02:
                continue
            s = (p["s0"] + (p["s1"] - p["s0"]) * (1.0 - (1.0 - u) * (1.0 - u))) * scale
            x, y = p["x"], p["y"]
            pp = 1.0
            if proj is not None:
                x, y, pp = proj(p["x"], p["y"], p["h"])
                s *= pp
            x += ox
            y += oy
            if cull and not (-200.0 < x < 1480.0 and -200.0 < y < 920.0):
                continue
            sx = sy = s
            rot = p["r"]
            if p["k"] > 0.0:
                if proj is not None:
                    # A streak in WORLD space has to be aimed in SCREEN space:
                    # project one tick of its motion and measure that.
                    x2, y2, _pp2 = proj(p["x"] + p["vx"], p["y"] + p["vy"],
                                        p["h"] + p["vh"])
                    dx = x2 + ox - x
                    dy = y2 + oy - y
                else:
                    dx = p["vx"]
                    dy = p["vy"]
                sp = math.hypot(dx, dy)
                if sp > 0.01:
                    rot = math.degrees(math.atan2(dy, dx))
                sx = s * (1.0 + p["k"] * sp / max(pp, 0.2))
            sq = p.get("sq")
            if sq is not None:
                sy = s * sq
            paint.quad(p["t"], x, y, sx, sy, rot=rot, col=p["c"], alpha=a,
                       add=p["add"], into=into)

    # --- THE LENS ------------------------------------------------------------
    # Per-fight defaults; a stage passes overrides each frame.
    INV_LENS_BASE = {
        "grade": (1.0, 1.0, 1.0, 0.35),
        "lift": (0.0, 0.0, 0.0),
        "gain": (1.0, 1.0, 1.0),
        "bloom": 0.0, "thresh": 0.70, "ca": 0.0, "grain": 0.0,
        "vig": 0.0, "vigr": 1.0, "barrel": 0.0, "flash": 0.0,
        "flashc": (1.0, 1.0, 1.0),
        "shock": (0.0, 0.0, 0.0, 0.0),
        "tear": (0.0, 0.0, 0.5, 0.0),
    }

    def inv_lens(paint, look, t=0.0):
        """Put the world through the lens. Returns the Render to blit; falls
        back to the raw world (and stays there) if the pass ever fails."""
        global INV_LENS_OK
        if not INV_LENS_OK or look is None:
            return paint.world
        L = dict(INV_LENS_BASE)
        L.update(look)
        if enter_m_low_detail():
            # Low Detail: no bloom. It is the lens's one glow (three extra
            # mip-chain reads a pixel) and pure decoration; the grade,
            # vignette, aberration, grain and every hit's flash, shockwave
            # and tear -- the fight's look and its feedback -- all stay.
            L["bloom"] = 0.0
        try:
            d = Transform(
                InvRenderHolder(paint.world), mesh=True, shader="inv.lens",
                u_lens_res=(float(paint.w), float(paint.h)),
                u_lens_time=float(t),
                u_lens_grade=tuple(float(v) for v in L["grade"]),
                u_lens_lift=tuple(float(v) for v in L["lift"]),
                u_lens_gain=tuple(float(v) for v in L["gain"]),
                u_lens_fx=(float(L["bloom"]), float(L["thresh"]),
                           float(L["ca"]), float(L["grain"])),
                u_lens_vig=(float(L["vig"]), float(L["vigr"]),
                            float(L["barrel"]), float(L["flash"])),
                u_lens_flashc=tuple(float(v) for v in L["flashc"]),
                u_lens_shock=tuple(float(v) for v in L["shock"]),
                u_lens_tear=tuple(float(v) for v in L["tear"]))
            return renpy.render(d, paint.w, paint.h, paint.st, paint.at)
        except Exception as e:
            INV_LENS_OK = False
            try:
                renpy.log("INV KIT: lens failed, drawing raw: %r" % e)
            except Exception:
                pass
            return paint.world

    def inv_compose(paint, look, t=0.0):
        """World through the lens, HUD on top. The stage's whole return."""
        rv = renpy.Render(paint.w, paint.h)
        rv.blit(inv_lens(paint, look, t), (0, 0))
        rv.blit(paint.hud, (0, 0))
        return rv

    # --- PANEL CHROME --------------------------------------------------------
    def _inv_rgba(col, a=None):
        c = col.lstrip("#")
        r = int(c[0:2], 16) / 255.0
        g = int(c[2:4], 16) / 255.0
        b = int(c[4:6], 16) / 255.0
        if a is None:
            a = int(c[6:8], 16) / 255.0 if len(c) >= 8 else 1.0
        return (r, g, b, float(a))

    def inv_panel(w, h, style):
        """A cached chrome plate. style keys: top, bot, edge (#rrggbbaa),
        accent, border, cut, inset, inset_a, noise, scan, split, ticks."""
        key = ("panel", int(w), int(h), tuple(sorted(style.items())))
        def build():
            if not INV_PANEL_OK:
                return Solid(style.get("bot", "#000000c0"), xysize=(int(w), int(h)))
            return Transform(
                Solid("#00000000"), xysize=(int(w), int(h)), mesh=True,
                shader="inv.panel",
                u_pn_size=(float(w), float(h)),
                u_pn_top=_inv_rgba(style.get("top", "#000000d0")),
                u_pn_bot=_inv_rgba(style.get("bot", "#000000e8")),
                u_pn_edge=_inv_rgba(style.get("edge", "#ffffffff")),
                u_pn_shape=(float(style.get("border", 2.0)),
                            float(style.get("cut", 8.0)),
                            float(style.get("inset", 6.0)),
                            float(style.get("inset_a", 0.0))),
                u_pn_tex=(float(style.get("noise", 0.0)),
                          float(style.get("scan", 0.0)),
                          float(style.get("split", 0.0)),
                          float(style.get("ticks", 0.0))),
                u_pn_accent=_inv_rgba(style.get("accent", "#ffffffff")))
        return _inv_tf(key, build)

    # --- A SHEET IN 3D ------------------------------------------------------
    def inv_sheet_corners(w, h, cx, top, yaw=0.0, pitch=0.0, focal=900.0):
        """A w x h sheet hanging from its top edge, centred on cx with that
        edge at `top`. Pitch tips its bottom toward the camera about the top
        edge (radians, positive = toward you); yaw turns it about the vertical
        through its centre. Returns the projected TL, TR, BR, BL."""
        cy_, sy_ = math.cos(yaw), math.sin(yaw)
        cp, spp = math.cos(pitch), math.sin(pitch)
        out = []
        for (u, v) in ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)):
            x = (u - 0.5) * w
            y = v * h
            y2 = y * cp
            z2 = y * spp
            x3 = x * cy_ + z2 * sy_
            z3 = -x * sy_ + z2 * cy_
            k = focal / max(focal - z3, 1.0)
            out.append((cx + x3 * k, top + y2 * k))
        return out

    def inv_sq2quad_inverse(c):
        """Rows of the inverse projective map taking a point in the quad c
        (TL, TR, BR, BL) back to the unit square -- Heckbert's square-to-quad,
        inverted by its adjugate."""
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = c
        sx = x0 - x1 + x2 - x3
        sy = y0 - y1 + y2 - y3
        if abs(sx) < 1e-7 and abs(sy) < 1e-7:
            a, b, cc = x1 - x0, x3 - x0, x0
            d, e, f = y1 - y0, y3 - y0, y0
            g = h = 0.0
        else:
            dx1, dx2 = x1 - x2, x3 - x2
            dy1, dy2 = y1 - y2, y3 - y2
            den = dx1 * dy2 - dx2 * dy1
            if abs(den) < 1e-9:
                den = 1e-9
            g = (sx * dy2 - dx2 * sy) / den
            h = (dx1 * sy - sx * dy1) / den
            a, b, cc = x1 - x0 + g * x1, x3 - x0 + h * x3, x0
            d, e, f = y1 - y0 + g * y1, y3 - y0 + h * y3, y0
        i = 1.0
        A = e * i - f * h
        B = -(d * i - f * g)
        C = d * h - e * g
        D = -(b * i - cc * h)
        E = a * i - cc * g
        F = -(a * h - b * g)
        G = b * f - cc * e
        H = -(a * f - cc * d)
        I = a * e - b * d
        det = a * A + b * B + cc * C
        if abs(det) < 1e-12:
            det = 1e-12
        return ((A / det, D / det, G / det),
                (B / det, E / det, H / det),
                (C / det, F / det, I / det))

    def inv_draw_sheet(paint, content, cw, ch, sw, sh, corners, light=(1.0, 0.0, 0.3, 1.0),
                       into=None):
        """Draw `content` (a displayable cw x ch with the sheet's sw x sh image
        centred in it) mapped onto the screen quad `corners`. The canvas is
        centred on the quad's bounding box; returns False if the shader is
        unavailable so the caller can draw it flat."""
        if not INV_PANEL_OK:
            return False
        xs = [c[0] for c in corners]
        ys = [c[1] for c in corners]
        ox = (min(xs) + max(xs)) * 0.5 - cw * 0.5
        oy = (min(ys) + max(ys)) * 0.5 - ch * 0.5
        local = [(c[0] - ox, c[1] - oy) for c in corners]
        r0, r1, r2 = inv_sq2quad_inverse(local)
        u0 = (cw - sw) * 0.5 / cw
        v0 = (ch - sh) * 0.5 / ch
        try:
            d = Transform(content, mesh=True, shader="inv.sheet",
                          u_sh_size=(float(cw), float(ch)),
                          u_sh_r0=tuple(float(v) for v in r0),
                          u_sh_r1=tuple(float(v) for v in r1),
                          u_sh_r2=tuple(float(v) for v in r2),
                          u_sh_crop=(u0, v0, 1.0 - u0, 1.0 - v0),
                          u_sh_light=tuple(float(v) for v in light))
            r = renpy.render(d, cw, ch, paint.st, paint.at)
            (into or paint.target).subpixel_blit(r, (ox, oy))
            return True
        except Exception as e:
            try:
                renpy.log("INV KIT: sheet failed: %r" % e)
            except Exception:
                pass
            return False

    def inv_draw_panel(paint, x, y, w, h, style, into=None):
        d = inv_panel(w, h, style)
        r, _sz = paint.tex(("panelr", int(w), int(h), id(d)), d, int(w), int(h))
        (into or paint.target).blit(r, (int(x), int(y)))

    # --- THE TURN LOG --------------------------------------------------------
    # Act one's readouts used to be a modal beat: one label and one value that
    # sat in the command window until Z was pressed, twice a turn. They are a
    # log now. A line lands when its action resolves and STAYS until the next
    # turn's lines push it down -- so a slow reader can read it while choosing
    # the next command, and the turn itself never stops to wait.
    INV_BEAT_HOLD = 30          # ticks a resolved action is held before play moves on
    INV_BEAT_SKIP = 8           # ...and how soon a key press may cut that short
    INV_LOG_MAX = 4

    def inv_log_push(g, label, value="", kind="you"):
        log = getattr(g, "turn_log", None)
        if log is None:
            log = []
            g.turn_log = log
        log.insert(0, {"label": label, "value": value, "kind": kind,
                       "tick": g.tick, "turn": getattr(g, "turn", 0)})
        del log[INV_LOG_MAX:]

    def inv_draw_log(paint, g, x, y, w, cols, line_h=24):
        """cols: dict kind -> (label colour, value colour)."""
        log = getattr(g, "turn_log", None) or []
        cur = getattr(g, "turn", 0)
        for i, e in enumerate(log):
            age = g.tick - e["tick"]
            fresh = inv_clamp(age / 10.0, 0.0, 1.0)
            old = 1.0 if e["turn"] >= cur else 0.55
            a = (0.55 + 0.45 * fresh) * old * (1.0 - 0.16 * i)
            lc, vc = cols.get(e["kind"], cols.get("you"))
            yy = y + i * line_h + (1.0 - fresh) * 6.0
            paint.text(e["label"], 15, inv_hex(lc, a), x, yy, bold=True,
                       w=w, h=line_h + 6, outline="#000000a0")
            if e["value"]:
                paint.text(e["value"], 15, inv_hex(vc, a), x + w, yy, bold=True,
                           anchor=(1.0, 0.0), w=w, h=line_h + 6,
                           outline="#000000a0")

    # --- RETRY ---------------------------------------------------------------
    def inv_retry_options(checkpoint):
        """What the overlay offers. A loss in the corruptive state may be
        retried FROM THE TEAR -- act one already decided what carries, and
        replaying fifteen turns to get back to a chase is not difficulty, it is
        a toll."""
        if checkpoint:
            return [("tear", "RETRY"), ("start", "RESTART"), ("stop", "STOP")]
        return [("start", "RETRY"), ("stop", "STOP")]

screen inv_retry_screen(name, word, options, ink="#e8ecf2", dim="#6d7686", accent="#ff2d4e", bg="#04050a"):
    modal True
    default sel = 0
    add Solid(bg)
    add Solid(accent + "18") ysize 2 ypos 0.5 yoffset -86
    add Solid(accent + "18") ysize 2 ypos 0.5 yoffset 120
    vbox:
        xalign 0.5
        yalign 0.5
        yoffset -10
        spacing 6
        text name size 15 color dim font INV_FONT bold True xalign 0.5 kerning 6
        text word size 44 color ink font INV_FONT bold True xalign 0.5 kerning 4
        null height 26
        for i, opt in enumerate(options):
            textbutton opt[1]:
                xalign 0.5
                action Return(opt[0])
                hovered SetScreenVariable("sel", i)
                text_font INV_FONT
                text_size 22
                text_bold True
                text_kerning 3
                text_color (ink if i == sel else dim)
                text_hover_color ink
                text_outlines [(2, "#00000080", 0, 0)]
                background (Solid(accent + "33") if i == sel else None)
                xpadding 26
                ypadding 6
    text "Z  OK      X  STOP" size 12 color dim font INV_FONT xalign 0.5 yalign 0.93
    key "K_UP" action SetScreenVariable("sel", (sel - 1) % len(options))
    key "K_w" action SetScreenVariable("sel", (sel - 1) % len(options))
    key "K_DOWN" action SetScreenVariable("sel", (sel + 1) % len(options))
    key "K_s" action SetScreenVariable("sel", (sel + 1) % len(options))
    key "K_z" action Return(options[sel][0])
    key "K_RETURN" action Return(options[sel][0])
    key "K_KP_ENTER" action Return(options[sel][0])
    key "K_x" action Return("stop")
    key "K_ESCAPE" action Return("stop")
