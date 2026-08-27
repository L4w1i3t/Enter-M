# =============================================================================
# ENTER-M :: Sick Ass Anime OP -- FX UPGRADE LAYER
# -----------------------------------------------------------------------------
# Real GPU effects for the OP. The original op.rpy faked everything with
# Solid() rectangles and double-image overlays. This file adds the genuine
# article on top of Matsu'Py 8.1's gl2 model renderer:
#
#   * Custom GLSL shaders   - true RGB-split chromatic aberration, digital
#                             glitch / datamosh, radial zoom-blur, a beat-drop
#                             shockwave ripple, rotating god rays, and a manga
#                             halftone (freeze-frame) filter.
#   * A global post-process - procedural film grain + vignette + scanlines
#                             that run for the entire OP.
#   * Real particle systems - drifting dust / embers / petals plus spark
#                             bursts on the drops, built on SpriteManager.
#   * Set pieces            - halftone freeze frames, a 3-panel split-screen
#                             montage card, and kinetic fake-credit typography
#                             (section 4b), wired into the op.rpy timeline.
#
# Everything here is additive and self-contained. op.rpy only gains a handful
# of `show screen` / `at` hooks, so the carefully beat-locked timeline is
# untouched. If a GPU somehow refuses the shaders, registration is guarded and
# the OP still plays (it just loses the extra polish).
# =============================================================================

# -----------------------------------------------------------------------------
# 1. SHADERS
# -----------------------------------------------------------------------------
# Registered defensively: a bad driver shouldn't take the whole OP down with it.
init -10 python:
    import math

    def _enter_m_op_register_shaders():

        # ---- Chromatic aberration / RGB channel split --------------------
        # Splits the red and blue channels along an axis. u_amount is in pixels
        # at the model's native size; u_time adds a faint living wobble.
        renpy.register_shader("enter_m.rgbsplit", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_model_size;
            uniform float u_time;
            uniform float u_amount;
            uniform float u_angle;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 px = 1.0 / max(u_model_size, vec2(1.0));
            float wob = 1.0 + 0.30 * sin(u_time * 26.0);
            vec2 dir = vec2(cos(u_angle), sin(u_angle));
            vec2 off = dir * (u_amount * wob) * px;
            vec4 cr = texture2D(tex0, v_tex_coord + off);
            vec4 cg = texture2D(tex0, v_tex_coord);
            vec4 cb = texture2D(tex0, v_tex_coord - off);
            gl_FragColor = vec4(cr.r, cg.g, cb.b, cg.a);
        """)

        # ---- Digital glitch / datamosh -----------------------------------
        # Block row displacement + channel tearing. u_intensity 0..1 scales
        # how many rows tear and how hard; driven over time by u_time/u_speed.
        renpy.register_shader("enter_m.glitch", variables="""
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
            float ca = u_intensity * 0.012;
            vec4 c;
            c.r = texture2D(tex0, uv + vec2(ca, 0.0)).r;
            c.g = texture2D(tex0, uv).g;
            c.b = texture2D(tex0, uv - vec2(ca, 0.0)).b;
            c.a = texture2D(tex0, uv).a;
            gl_FragColor = c;
        """)

        # ---- Radial zoom blur --------------------------------------------
        # Smears the image outward from u_center. Great for punch-in impacts.
        renpy.register_shader("enter_m.zoomblur", variables="""
            uniform sampler2D tex0;
            uniform float u_strength;
            uniform vec2 u_center;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 dir = v_tex_coord - u_center;
            vec4 acc = vec4(0.0);
            for (int i = 0; i < 12; i++) {
                float t = float(i) / 11.0;
                acc += texture2D(tex0, v_tex_coord - dir * u_strength * t);
            }
            gl_FragColor = acc / 12.0;
        """)

        # ---- Shockwave ripple --------------------------------------------
        # A ring of displacement expands from u_center as u_progress 0->1.
        # Animated from ATL so it lands exactly on a beat.
        renpy.register_shader("enter_m.shockwave", variables="""
            uniform sampler2D tex0;
            uniform float u_progress;
            uniform float u_amplitude;
            uniform float u_thickness;
            uniform vec2 u_center;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 d = v_tex_coord - u_center;
            float dist = length(d);
            float radius = u_progress * 1.2;
            float ring = smoothstep(u_thickness, 0.0, abs(dist - radius)) * (1.0 - u_progress);
            vec2 disp = normalize(d + vec2(1e-5)) * ring * u_amplitude;
            gl_FragColor = texture2D(tex0, v_tex_coord - disp);
        """)

        # ---- Global post-process (procedural overlay) --------------------
        # No scene input needed: it draws premultiplied dark grain + vignette
        # + fine scanlines straight from v_tex_coord, so it composites over
        # whatever is on screen. u_intensity scales the whole thing.
        renpy.register_shader("enter_m.postfx", variables="""
            uniform float u_time;
            uniform vec2 u_model_size;
            uniform float u_intensity;
            uniform vec3 u_tint;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            vec2 c = uv - 0.5;
            float vig = smoothstep(0.42, 0.95, length(c) * 1.28) * 0.55;
            float scan = (1.0 - (sin(uv.y * 1130.0) * 0.5 + 0.5)) * 0.05;
            float n = fract(sin(dot(uv * u_model_size + vec2(u_time * 57.0), vec2(12.9898, 78.233))) * 43758.5453);
            float grain = max(n - 0.5, 0.0) * 0.10;
            float a = clamp(vig + scan + grain, 0.0, 0.90) * u_intensity;
            gl_FragColor = vec4(u_tint * a, a);
        """)

        # ---- Primordial chaotic sludge (procedural, opaque background) ----
        # Domain-warped fractal noise that churns over u_time -- a roiling,
        # viscous, primordial muck. Fully opaque; meant to BE the background.
        # Helper functions live in fragment_functions (global scope, outside main).
        renpy.register_shader("enter_m.sludge", variables="""
            uniform float u_time;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float enterm_hash(vec2 p) {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
            }
            float enterm_noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                vec2 u = f * f * (3.0 - 2.0 * f);
                float a = enterm_hash(i);
                float b = enterm_hash(i + vec2(1.0, 0.0));
                float c = enterm_hash(i + vec2(0.0, 1.0));
                float d = enterm_hash(i + vec2(1.0, 1.0));
                return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
            }
            float enterm_fbm(vec2 p) {
                float v = 0.0;
                float amp = 0.5;
                for (int i = 0; i < 5; i++) {
                    v += amp * enterm_noise(p);
                    p *= 2.0;
                    amp *= 0.5;
                }
                return v;
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            float t = u_time * 0.32;
            vec2 p = uv * 3.2;
            vec2 q = vec2(enterm_fbm(p + vec2(0.0, t)), enterm_fbm(p + vec2(5.2, -t)));
            vec2 r = vec2(enterm_fbm(p + 4.0 * q + vec2(1.7, 9.2) + 0.20 * t), enterm_fbm(p + 4.0 * q + vec2(8.3, 2.8) - 0.16 * t));
            float f = enterm_fbm(p + 4.0 * r);
            vec3 c1 = vec3(0.015, 0.022, 0.018);  // near-black ooze
            vec3 c2 = vec3(0.11, 0.15, 0.06);     // murky olive
            vec3 c3 = vec3(0.34, 0.30, 0.10);     // sickly amber-green crust
            vec3 col = mix(c1, c2, clamp(f * f * 2.2, 0.0, 1.0));
            col = mix(col, c3, clamp(length(r) * 0.55, 0.0, 1.0));
            col *= 0.55 + 0.85 * f;               // dark churning veins
            gl_FragColor = vec4(col, 1.0);
        """)

        # ---- Rotating god rays (procedural overlay) -----------------------
        # A sunburst of soft rays spinning around u_center. Premultiplied, so
        # it composites over anything; used behind hero frames, freeze frames,
        # and the title drop.
        renpy.register_shader("enter_m.rays", variables="""
            uniform float u_time;
            uniform vec2 u_center;
            uniform vec3 u_color;
            uniform float u_count;
            uniform float u_speed;
            uniform float u_strength;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 d = v_tex_coord - u_center;
            float ang = atan(d.y, d.x);
            float rad = length(d);
            float f = sin(ang * u_count + u_time * u_speed) * 0.5 + 0.5;
            f = pow(f, 3.0);
            float fall = (1.0 - smoothstep(0.05, 0.75, rad)) * 0.65 + 0.35;
            float core = smoothstep(0.0, 0.10, rad);
            float a = f * fall * core * u_strength;
            gl_FragColor = vec4(u_color * a, a);
        """)

        # ---- Cel posterize (animatic background look) ----------------------
        # Quantizes colour into flat painted bands + a small saturation lift,
        # so the photo-ish location plates read as hand-painted anime cels.
        # In-lore the OP is Matsuda's homemade animatic, so every bg card runs
        # through this.
        renpy.register_shader("enter_m.cel", variables="""
            uniform sampler2D tex0;
            uniform float u_levels;
            uniform float u_sat;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec4 c = texture2D(tex0, v_tex_coord);
            vec3 rgb = c.rgb / max(c.a, 0.0001);
            rgb = floor(rgb * u_levels + 0.5) / u_levels;
            float g = dot(rgb, vec3(0.299, 0.587, 0.114));
            rgb = clamp(mix(vec3(g), rgb, u_sat), 0.0, 1.0);
            gl_FragColor = vec4(rgb * c.a, c.a);
        """)

        # ---- Manga halftone ("impact frame" freeze) ------------------------
        # Re-renders the child as ink dots on paper, sized by darkness. u_mix
        # animates 0->1 to melt the halftone back into full colour.
        renpy.register_shader("enter_m.halftone", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_model_size;
            uniform float u_dot;
            uniform vec3 u_ink;
            uniform vec3 u_paper;
            uniform float u_mix;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec4 c = texture2D(tex0, v_tex_coord);
            float a = c.a;
            vec3 rgb = c.rgb / max(a, 0.0001);
            float g = dot(rgb, vec3(0.299, 0.587, 0.114));
            vec2 cell = fract(v_tex_coord * u_model_size / u_dot) - 0.5;
            float r = sqrt(max(1.0 - g, 0.0)) * 0.68;
            float m = smoothstep(r, r - 0.12, length(cell));
            vec3 col = mix(u_paper, u_ink, m);
            col = mix(col, rgb, u_mix);
            gl_FragColor = vec4(col * a, a);
        """)

        # ---- Radial speed lines (procedural overlay) ---------------------
        # Manga "action frame" lines streaking out from u_center, clear inside
        # u_inner so the subject reads. Premultiplied; composites over anything.
        renpy.register_shader("enter_m.speedlines", variables="""
            uniform float u_time;
            uniform vec2 u_center;
            uniform vec3 u_color;
            uniform float u_count;
            uniform float u_inner;
            uniform float u_strength;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float enterm_sl_hash(float n) { return fract(sin(n) * 43758.5453); }
        """, fragment_300="""
            vec2 d = v_tex_coord - u_center;
            float ang = atan(d.y, d.x);
            float rad = length(d);
            float pos = (ang / 6.2831853 + 0.5) * u_count;
            float idx = floor(pos);
            float lane = fract(pos);
            float jit = enterm_sl_hash(idx);
            float w = 0.10 + 0.32 * jit;
            float line = smoothstep(w, 0.0, abs(lane - 0.5));
            float flick = 0.55 + 0.45 * sin(u_time * 17.0 + idx * 1.7);
            float falloff = smoothstep(u_inner, 0.74, rad);
            float a = line * falloff * flick * u_strength;
            gl_FragColor = vec4(u_color * a, a);
        """)

    try:
        _enter_m_op_register_shaders()
        ENTER_M_OP_SHADERS = True
    except Exception as e:
        ENTER_M_OP_SHADERS = False
        if config.developer:
            renpy.log("ENTER-M OP: shader registration failed: %r" % e)


# -----------------------------------------------------------------------------
# 2. SHADER TRANSFORMS
# -----------------------------------------------------------------------------
# Each renders its child to a texture (mesh True) then runs a shader. Uniforms
# and alpha decay are animated in ATL so impacts stay synced to the beat grid.

transform enter_m_op_fx_rgb(duration=0.6, amount=16.0, angle=0.0, z=1.08, a=0.85):
    mesh True
    shader "enter_m.rgbsplit"
    u_amount amount
    u_angle angle
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom z
    alpha a
    linear duration alpha 0.0 u_amount 0.0

transform enter_m_op_fx_shock(duration=0.6, amplitude=0.045, thickness=0.08, z=1.06, a=0.95):
    mesh True
    shader "enter_m.shockwave"
    u_amplitude amplitude
    u_thickness thickness
    u_center (0.5, 0.5)
    u_progress 0.0
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom z
    alpha a
    parallel:
        linear duration u_progress 1.0
    parallel:
        linear duration alpha 0.0

transform enter_m_op_fx_zoomblur(duration=0.5, strength=0.16, z=1.05, a=0.9):
    mesh True
    shader "enter_m.zoomblur"
    u_strength strength
    u_center (0.5, 0.5)
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom z
    alpha a
    linear duration alpha 0.0 u_strength 0.0

transform enter_m_op_fx_glitch(duration=0.6, intensity=0.9, z=1.04, a=0.85):
    mesh True
    shader "enter_m.glitch"
    u_intensity intensity
    u_blocks 26.0
    u_speed 16.0
    u_amount 0.10
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom z
    alpha a
    linear duration alpha 0.0 u_intensity 0.0

# Subtle, motion-friendly aberration used to upgrade every CG cut at once.
transform enter_m_op_cg_aberr(strength=0.12, duration=1.0):
    mesh True
    shader "enter_m.rgbsplit"
    u_amount 2.0 + strength * 46.0
    u_angle 0.0
    subpixel True
    xalign 0.5
    yalign 0.5
    alpha 0.50
    easeout duration * 0.5 alpha 0.16 u_amount 1.0

# Cinematic, self-pulsing aberration for the title drop.
transform enter_m_op_title_glitch(duration=7.0):
    mesh True
    shader "enter_m.rgbsplit"
    u_amount 20.0
    u_angle 0.0
    subpixel True
    xalign 0.5
    yalign 0.80
    alpha 0.0
    zoom 1.18
    yoffset 26
    easeout 0.42 alpha 1.0 zoom 1.0 yoffset 0 u_amount 7.0
    block:
        easein 0.10 u_amount 15.0
        easeout 0.34 u_amount 4.0
        pause 1.5
        repeat


# -----------------------------------------------------------------------------
# 2b. CHARACTER SPRITE STAGING
# -----------------------------------------------------------------------------
# The bg-card screens were always handed sprite names (mc/matsuda/tsubaki/...)
# but never drew them -- every "character beat" was an empty room. These give
# the sprites a real entrance: slide-in with overshoot, a slow parallax drift
# against the background pan, and a breathing sway. Sprites are 640x960 (mod
# cast) or 960x960 (Monika), anchored bottom-centre so `y`/`z` from the cards
# frame them the way the author intended.

# Single sprite sliding in from `start` to `end`, then drifting (parallax).
transform enter_m_op_sprite_enter(start=-150, end=640, y=742, z=0.56, rot=-4.0, duration=1.0, direction=1):
    subpixel True
    anchor (0.5, 1.0)
    xpos start
    ypos y
    zoom z
    rotate rot
    alpha 0.0
    parallel:
        easeout 0.10 alpha 1.0
    parallel:
        easeout duration * 0.34 xpos (end + 22 * direction) zoom (z * 1.03)
        ease duration * 0.20 xpos end zoom z
        linear duration * 0.46 xpos (end + 26 * direction) ypos (y - 6)
    parallel:
        block:
            ease 1.1 yoffset -4 rotate (rot + 0.4)
            ease 1.1 yoffset 0 rotate rot
            repeat

# Variant entrance: swoops in along an upward arc (more kinetic than a slide).
transform enter_m_op_sprite_arc(start=-150, end=640, y=742, z=0.56, rot=-4.0, duration=1.0, direction=1):
    subpixel True
    anchor (0.5, 1.0)
    xpos start
    ypos (y + 64)
    zoom (z * 0.93)
    rotate (rot - 6 * direction)
    alpha 0.0
    parallel:
        easeout 0.12 alpha 1.0
    parallel:
        easeout duration * 0.42 xpos end ypos (y - 10) zoom (z * 1.02) rotate rot
        ease duration * 0.22 ypos y zoom z
        linear duration * 0.36 xpos (end + 20 * direction) ypos (y - 4)
    parallel:
        block:
            ease 1.0 rotate (rot + 0.5)
            ease 1.0 rotate rot
            repeat

# Variant entrance: drifts up gently from below (dreamy / slow beats).
transform enter_m_op_sprite_float(start=-150, end=640, y=742, z=0.56, rot=0.0, duration=1.0, direction=1):
    subpixel True
    anchor (0.5, 1.0)
    xpos start
    ypos (y + 46)
    zoom (z * 0.96)
    rotate rot
    alpha 0.0
    parallel:
        easeout 0.30 alpha 1.0
    parallel:
        easeout duration * 0.55 xpos end ypos y zoom z
        linear duration * 0.45 ypos (y - 8) xpos (end + 12 * direction)
    parallel:
        block:
            ease 1.4 yoffset -5 rotate (rot + 0.6)
            ease 1.4 yoffset 0 rotate rot
            repeat

# Centre-held sprite: gentle push-in + sway, no big slide.
transform enter_m_op_sprite_hold(x=640, y=742, z=0.56, rot=0.0, duration=1.0, side=1):
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos y
    zoom z
    rotate rot
    alpha 0.0
    easeout 0.18 alpha 1.0
    parallel:
        linear duration zoom (z * 1.045) ypos (y - 8)
    parallel:
        block:
            ease 1.3 xoffset (6 * side) rotate (rot + 0.5)
            ease 1.3 xoffset 0 rotate rot
            repeat

# Sprite snapping across in steps (mirrors the bg snap-pan beats).
transform enter_m_op_sprite_step(x1=340, x2=470, x3=610, y=742, z=0.56, rot=-4.0, duration=1.0):
    subpixel True
    anchor (0.5, 1.0)
    xpos x1
    ypos y
    zoom z
    rotate rot
    alpha 0.0
    easeout 0.08 alpha 1.0
    easeout duration * 0.30 xpos x2
    easeout duration * 0.30 xpos x3 zoom (z * 1.02)
    linear duration * 0.40 xpos (x3 + 18) zoom z

# Applied AFTER an entrance transform: turns the positioned sprite into a soft,
# motion-tracking drop-shadow / echo behind the real sprite.
transform enter_m_op_sprite_shadow_mod:
    matrixcolor BrightnessMatrix(-1.0)
    blur 7.0
    alpha 0.40
    xoffset 14
    yoffset 10

init python:
    # Picks an entrance transform from the card's own motion_style, so a slide,
    # an arc, and a float all read differently instead of every cut feeling the
    # same. Returns a configured Transform the screen can drop straight into `at`.
    def enter_m_op_stage_tf(style, start, end, y, z, rot, duration, direction):
        if style == "arc":
            return enter_m_op_sprite_arc(start, end, y, z, rot, duration, direction)
        elif style == "float":
            return enter_m_op_sprite_float(start, end, y, z, rot, duration, direction)
        return enter_m_op_sprite_enter(start, end, y, z, rot, duration, direction)


# -----------------------------------------------------------------------------
# 3. PARTICLE SYSTEMS
# -----------------------------------------------------------------------------
init python:
    import math as _enter_m_math

    class EnterMOpDrift(object):
        """An ambient field of drifting particles built on SpriteManager.

        Positions are derived purely from the sprite-manager time `st`, so the
        field is deterministic, rollback-safe, and recycles by wrapping the
        screen edges. The child displayable is shared by every sprite (Matsu'Py
        SpriteManager), so per-sprite spin/fade is intentionally avoided to keep
        the field from blinking in lockstep -- variety comes from position,
        velocity, and sway phase instead.
        """

        def __init__(self, child, count=40, W=1280, H=720, vy=14.0, vx=4.0, amp=22.0, spd=0.7):
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
                sp = self.spd * (0.6 + random.random() * 0.8)
                vyi = self.vy * (0.7 + random.random() * 0.6)
                vxi = self.vx * (0.5 + random.random() * 1.0)
                s.x = int(x0)
                s.y = int(y0)
                self.parts.append((s, x0, y0, vxi, vyi, ph, sp))

        def update(self, st):
            spanY = self.H + 80.0
            spanX = self.W + 80.0
            for s, x0, y0, vxi, vyi, ph, sp in self.parts:
                y = ((y0 + vyi * st) + 40.0) % spanY - 40.0
                x = ((x0 + vxi * st + self.amp * _enter_m_math.sin(st * sp + ph)) + 40.0) % spanX - 40.0
                s.x = int(x)
                s.y = int(y)
            return 0


# ---- Particle sprites -------------------------------------------------------
# Small bright Solids read as glints on the near-black OP background.
image enter_m_op_p_dust:
    Solid("#bfe9ff")
    subpixel True
    xysize (3, 3)
    alpha 0.30

image enter_m_op_p_ember:
    Solid("#ffd28a")
    subpixel True
    xysize (4, 4)
    alpha 0.46

image enter_m_op_p_petal:
    Solid("#ffb3d1")
    subpixel True
    xysize (12, 7)
    rotate 18
    alpha 0.55

# Spark for one-shot bursts: shrinks + fades within the burst lifetime.
image enter_m_op_p_spark:
    Solid("#dffaff")
    subpixel True
    xysize (5, 5)
    zoom 1.0
    alpha 0.95
    parallel:
        linear 0.55 zoom 0.0
    parallel:
        linear 0.55 alpha 0.0

# ---- Ambient drift fields (one instance each; deferred to first show) --------
image enter_m_op_field_dust:
    EnterMOpDrift("enter_m_op_p_dust", count=48, W=1280, H=720, vy=14.0, vx=4.0, amp=22.0, spd=0.7).sm
    pos (0, 0)

image enter_m_op_field_ember:
    EnterMOpDrift("enter_m_op_p_ember", count=36, W=1280, H=720, vy=-48.0, vx=6.0, amp=20.0, spd=1.1).sm
    pos (0, 0)

image enter_m_op_field_petal:
    EnterMOpDrift("enter_m_op_p_petal", count=30, W=1280, H=720, vy=42.0, vx=-10.0, amp=34.0, spd=0.9).sm
    pos (0, 0)


# -----------------------------------------------------------------------------
# 4. FX SCREENS
# -----------------------------------------------------------------------------

# Global post-process: grain + vignette + scanlines for the whole OP.
# Uniforms must live in an ATL transform (the screen `add` block doesn't accept
# custom u_ properties), so the shader is applied via `at`.
transform enter_m_op_postfx_t(intensity=0.62, tint=(0.02, 0.05, 0.08)):
    mesh True
    shader "enter_m.postfx"
    u_intensity intensity
    u_tint tint

screen enter_m_op_post_fx(intensity=0.62, tint=(0.02, 0.05, 0.08)):
    zorder 86
    add Solid("#00000000") xysize (1280, 720) at enter_m_op_postfx_t(intensity, tint)

# Primordial chaotic sludge as a full-screen animated background (no sprites).
transform enter_m_op_sludge_t(duration=1.0):
    mesh True
    shader "enter_m.sludge"
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.06
    linear duration zoom 1.14

screen enter_m_op_sludge_card(duration=1.0):
    zorder 80
    add Solid("#000000") xysize (1280, 720) at enter_m_op_sludge_t(duration)
    add "noise":
        alpha 0.05

# ---- Impact / hero frame --------------------------------------------------
# A "money shot": one character punched in huge over a duotone limbo with
# radial speed lines converging on them -- the opposite of a slow pan. Used to
# break up the montage.
transform enter_m_op_speedlines_t(cx=0.5, cy=0.45, color=(0.82, 0.96, 1.0), count=48.0, inner=0.13, strength=0.7):
    mesh True
    shader "enter_m.speedlines"
    u_center (cx, cy)
    u_color color
    u_count count
    u_inner inner
    u_strength strength

transform enter_m_op_hero_in(x=640, y=742, z=0.74, rot=0.0, duration=1.0):
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos y
    zoom (z * 1.20)
    rotate rot
    alpha 0.0
    easeout 0.10 alpha 1.0 zoom (z * 1.02)
    ease 0.14 zoom z
    parallel:
        linear duration zoom (z * 1.06) ypos (y - 8)
    parallel:
        block:
            ease 0.9 xoffset 4 rotate (rot + 0.4)
            ease 0.9 xoffset 0 rotate rot
            repeat

# Chroma ghost: layered over the hero (same framing) for an aberrated edge.
transform enter_m_op_rgb_mod(x=640, y=742, z=0.74, rot=0.0, duration=1.0, amount=12.0):
    mesh True
    shader "enter_m.rgbsplit"
    u_amount amount
    u_angle 0.0
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos y
    zoom z
    rotate rot
    alpha 0.0
    easeout 0.10 alpha 0.38
    linear duration alpha 0.22 u_amount (amount * 0.4)

# White-hot silhouette that flashes over the hero for a couple of frames, then
# burns off to reveal the coloured sprite underneath (anime impact-frame pop).
transform enter_m_op_hero_flash_mod:
    matrixcolor BrightnessMatrix(1.0)
    alpha 0.9
    pause 0.08
    linear 0.20 alpha 0.0

screen enter_m_op_bg_impact_card(sprite, bg_color="#0a1622", line_color=(0.82, 0.96, 1.0), accent="#75f7ff", x=640, z=0.74, y=742, rot=0, duration=1.0, focus_x=0.5):
    zorder 80
    add Solid(bg_color)
    add Solid(accent) at enter_m_op_panel_sweep(220, 0.00, 1, -12, 0.18)
    add Solid("#ffffff44") at enter_m_op_panel_sweep(980, enter_m_op_eighth_bar, -1, 10, 0.12)
    if ENTER_M_OP_SHADERS:
        add Solid("#000000") xysize (1280, 720) at enter_m_op_speedlines_t(focus_x, 0.44, line_color, 54.0, 0.10, 0.55)
        add Solid("#00000000") xysize (1280, 720) at enter_m_op_rays_t(focus_x, 0.40, line_color, 16.0, 1.2, 0.26)
    add sprite at enter_m_op_hero_in(x, y, z, rot, duration), enter_m_op_sprite_shadow_mod
    add sprite at enter_m_op_hero_in(x, y, z, rot, duration)
    if ENTER_M_OP_SHADERS:
        add sprite at enter_m_op_rgb_mod(x, y, z, rot, duration, 12.0)
    add sprite at enter_m_op_hero_in(x, y, z, rot, duration), enter_m_op_hero_flash_mod
    if ENTER_M_OP_SHADERS:
        add Solid("#ffffff") xysize (1280, 720) at enter_m_op_speedlines_t(focus_x, 0.42, line_color, 46.0, 0.16, 0.42)
    add Solid("#00000022")
    add "noise":
        alpha 0.02

# -----------------------------------------------------------------------------
# 4b. SET PIECES (freeze frames, split panels, god rays, kinetic credits)
# -----------------------------------------------------------------------------
# Bigger structural shots so the OP is more than pans: manga halftone freeze
# frames, a three-panel split-screen montage card, rotating god rays for the
# drops/title, and anime-style kinetic credit typography.

init python:
    def enter_m_op_rgb(hexcolor):
        """'#rrggbb' -> (r, g, b) floats for shader uniforms."""
        c = Color(hexcolor)
        return (c.rgb[0], c.rgb[1], c.rgb[2])

    def enter_m_op_celbg(bg_image, move_tf):
        """A bg plate wrapped in its motion transform, plus the cel-posterize
        pass when shaders are available. Every montage card runs its bg
        through this so the plates read as painted animatic cels."""
        d = At(renpy.displayable(bg_image), move_tf)
        if ENTER_M_OP_SHADERS:
            d = At(d, enter_m_op_cel_mod)
        return d

# The cel pass itself (see enter_m.cel). Applied OUTSIDE the motion transform,
# so the moving plate is re-rendered to a texture and posterized per frame.
transform enter_m_op_cel_mod:
    mesh True
    shader "enter_m.cel"
    u_levels 7.0
    u_sat 1.18

# ---- 90s-OP composite layers -------------------------------------------------
# Giant duotone "ghost portrait": a huge flat-tinted copy of the character
# looming behind the scene (the classic Gundam/90s-OP double-exposure bust).
# gz/gy come from the card (gy places the HEAD in frame; sprites are 960 tall).
transform enter_m_op_ghost_echo(x=1000, gz=1.85, gy=1736, tint="#75f7ff", duration=1.0, drift=1):
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos gy
    zoom gz
    alpha 0.0
    matrixcolor ColorizeMatrix("#04060b", tint)
    parallel:
        easeout 0.30 alpha 0.24
    parallel:
        linear duration xoffset (-22 * drift) yoffset -14

# White rim-flash the instant a sprite lands from its entrance -- an extra
# copy of the sprite (same motion transform) that pops and burns off.
transform enter_m_op_sprite_flash_mod(delay=0.30):
    matrixcolor BrightnessMatrix(1.0)
    alpha 0.0
    pause delay
    linear 0.05 alpha 0.55
    linear 0.22 alpha 0.0

# ---- Character name cards ------------------------------------------------------
# Earnest 90s-OP cast captions: accent block + big name + rule, snapping in
# from the shot's edge and retreating before the cut.
transform enter_m_op_name_pop(delay=0.0, edge=1, duration=1.0):
    alpha 0.0
    yzoom 0.0
    pause delay
    easeout_quad 0.16 alpha 1.0 yzoom 1.0
    pause (max(duration - delay - 0.34, 0.05))
    easein_quad 0.16 alpha 0.0

transform enter_m_op_name_slide(delay=0.0, edge=1, duration=1.0):
    alpha 0.0
    xoffset (-46 * edge)
    pause delay
    easeout_quad 0.20 alpha 1.0 xoffset 0
    pause (max(duration - delay - 0.40, 0.05))
    easein_quad 0.18 alpha 0.0 xoffset (18 * edge)

transform enter_m_op_name_rule(delay=0.0, edge=1, duration=1.0):
    xzoom 0.0
    pause delay
    easeout_quad 0.20 xzoom 1.0
    pause (max(duration - delay - 0.38, 0.05))
    easein_quad 0.16 xzoom 0.0

screen enter_m_op_name_card(char_name, x=170, y=552, accent="#75f7ff", duration=1.0, edge=1):
    zorder 95
    $ _nc_anchor = 0.0 if edge >= 0 else 1.0
    add Solid(accent) xysize (10, 46) pos (x - 22 * edge, y - 1) anchor (_nc_anchor, 0.0) at enter_m_op_name_pop(0.0, edge, duration)
    text char_name style "enter_m_op_name_card_text" pos (x, y) anchor (_nc_anchor, 0.0) at enter_m_op_name_slide(0.04, edge, duration)
    add Solid("#ffffffd0") xysize (300, 2) pos (x, y + 52) anchor (_nc_anchor, 0.0) at enter_m_op_name_rule(0.10, edge, duration)
    timer duration action Hide("enter_m_op_name_card")

style enter_m_op_name_card_text is enter_m_op_credit:
    size 44
    kerning 6

# ---- God rays ---------------------------------------------------------------
transform enter_m_op_rays_t(cx=0.5, cy=0.45, color=(1.0, 0.92, 0.6), count=22.0, speed=0.6, strength=0.4):
    mesh True
    shader "enter_m.rays"
    u_center (cx, cy)
    u_color color
    u_count count
    u_speed speed
    u_strength strength

# Standalone rays overlay for drops/title. Auto-hides after `duration` if > 0.
screen enter_m_op_rays(cx=0.5, cy=0.45, color=(1.0, 0.92, 0.6), count=22.0, speed=0.6, strength=0.4, duration=0.0):
    zorder 87
    if ENTER_M_OP_SHADERS:
        add Solid("#00000000") xysize (1280, 720) at enter_m_op_rays_t(cx, cy, color, count, speed, strength)
    if duration > 0:
        timer duration action Hide("enter_m_op_rays")

# ---- Manga freeze frame -----------------------------------------------------
# The pose: three hard snap positions (freeze-frame jump cuts), shared by the
# halftone hero and its flat-colour offset silhouette so they stay in sync.
transform enter_m_op_freeze_pose(x=640, y=742, z=0.80, rot=0.0, duration=1.0):
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos y
    zoom (z * 1.18)
    rotate (rot - 2.4)
    xoffset 18
    pause (duration * 0.30)
    zoom (z * 1.07) rotate (rot + 1.4) xoffset -12
    pause (duration * 0.28)
    zoom z rotate rot xoffset 0

# Same pose, rendered through the halftone shader; melts to colour at the end.
transform enter_m_op_halftone_pop(x=640, y=742, z=0.80, rot=0.0, duration=1.0, ink=(0.07, 0.06, 0.09), paper=(0.97, 0.95, 0.91), dot=7.0):
    mesh True
    shader "enter_m.halftone"
    u_dot dot
    u_ink ink
    u_paper paper
    u_mix 0.0
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos y
    zoom (z * 1.18)
    rotate (rot - 2.4)
    xoffset 18
    pause (duration * 0.30)
    zoom (z * 1.07) rotate (rot + 1.4) xoffset -12
    pause (duration * 0.28)
    zoom z rotate rot xoffset 0
    easeout (duration * 0.32) u_mix 1.0

# Flattens a sprite copy to one solid colour (the offset "print misregistration"
# silhouette behind the halftone hero).
transform enter_m_op_flat_mod(flat_color="#d05f77"):
    matrixcolor ColorizeMatrix(flat_color, flat_color)
    alpha 0.85

screen enter_m_op_freeze_frame(sprite, paper="#f2e9d8", ink="#241016", accent="#d05f77", x=640, y=742, z=0.80, rot=0.0, duration=1.0):
    zorder 80
    add Solid(paper)
    if ENTER_M_OP_SHADERS:
        add Solid("#00000000") xysize (1280, 720) at enter_m_op_rays_t(0.5, 0.40, enter_m_op_rgb(ink), 26.0, 0.32, 0.16)
    add Solid(ink) at enter_m_op_panel_sweep(250, 0.00, 1, -14, 0.16)
    add Solid(accent) at enter_m_op_panel_sweep(990, 0.08, -1, 12, 0.22)
    add sprite at enter_m_op_freeze_pose(x + 16, y + 10, z, rot, duration), enter_m_op_flat_mod(accent)
    if ENTER_M_OP_SHADERS:
        add sprite at enter_m_op_halftone_pop(x, y, z, rot, duration, enter_m_op_rgb(ink), enter_m_op_rgb(paper))
    else:
        add sprite at enter_m_op_freeze_pose(x, y, z, rot, duration)
    add Solid("#ffffff") at enter_m_op_flash(0.34)
    add "noise":
        alpha 0.03

# ---- Split-screen montage card ----------------------------------------------
# Three vertical panels, each its own crop of the bg with its own character,
# sliding in from alternating edges (classic anime-OP ensemble shot).
transform enter_m_op_split_panel_in(i=0, duration=1.0):
    subpixel True
    yoffset (-760 if i % 2 == 0 else 760)
    pause (0.06 * i)
    easeout_quad 0.30 yoffset 0

transform enter_m_op_split_bg(i=0, duration=1.0):
    subpixel True
    anchor (0.5, 0.5)
    pos (210, 360)
    zoom 1.24
    xoffset ((i - 1) * -120)
    linear duration xoffset ((i - 1) * -120 + (16 if i % 2 else -16))

transform enter_m_op_split_sprite(i=0, y=742, z=0.56, duration=1.0):
    subpixel True
    anchor (0.5, 1.0)
    xpos 210
    ypos (y + 44)
    zoom z
    alpha 0.0
    pause (0.10 + 0.07 * i)
    easeout_quad 0.30 alpha 1.0 ypos y
    parallel:
        linear duration zoom (z * 1.035)
    parallel:
        block:
            ease 1.2 xoffset (4 if i % 2 else -4)
            ease 1.2 xoffset 0
            repeat

transform enter_m_op_split_gap(delay=0.0):
    yanchor 0.5
    ypos 360
    yzoom 0.0
    pause delay
    easeout_quad 0.28 yzoom 1.0

screen enter_m_op_split_panel(bg_image, sprite, px, i, y, z, overlay, duration):
    viewport:
        xpos px
        ypos 0
        xysize (420, 720)
        at enter_m_op_split_panel_in(i, duration)
        fixed:
            xysize (420, 720)
            add enter_m_op_celbg(bg_image, enter_m_op_split_bg(i, duration))
            add Solid(overlay)
            add sprite at enter_m_op_split_sprite(i, y, z, duration), enter_m_op_sprite_shadow_mod
            add sprite at enter_m_op_split_sprite(i, y, z, duration)
            add Solid("#00000026")

screen enter_m_op_split_card(bg_image, s1, s2, s3, y1=742, z1=0.56, y2=742, z2=0.56, y3=742, z3=0.56, overlay="#ffffff22", accent="#75f7ff", accent2="#d05f77", duration=1.0):
    zorder 80
    add Solid("#05070d")
    use enter_m_op_split_panel(bg_image, s1, 0, 0, y1, z1, overlay, duration)
    use enter_m_op_split_panel(bg_image, s2, 430, 1, y2, z2, overlay, duration)
    use enter_m_op_split_panel(bg_image, s3, 860, 2, y3, z3, overlay, duration)
    add Solid(accent) xysize (10, 720) xpos 420 at enter_m_op_split_gap(0.05)
    add Solid(accent2) xysize (10, 720) xpos 850 at enter_m_op_split_gap(0.12)
    add "noise":
        alpha 0.015

# ---- Kinetic credits ----------------------------------------------------------
# Anime-OP staff typography: a small role line, a big name line, and an accent
# rule, sliding in from the shot's leading edge and retreating before the cut.
transform enter_m_op_credit_rule(edge=1, duration=2.0):
    xzoom 0.0
    easeout_quad 0.28 xzoom 1.0
    pause (max(duration - 0.62, 0.1))
    easein_quad 0.22 xzoom 0.0

transform enter_m_op_credit_text_in(delay=0.0, edge=1, duration=2.0):
    alpha 0.0
    xoffset (-30 * edge)
    pause delay
    easeout_quad 0.30 alpha 1.0 xoffset 0
    pause (max(duration - delay - 0.64, 0.1))
    easein_quad 0.26 alpha 0.0 xoffset (16 * edge)

screen enter_m_op_kinetic_credit(role_text, name_text, x=170, y=520, accent="#75f7ff", duration=2.0, edge=1):
    zorder 95
    $ _credit_anchor = 0.0 if edge >= 0 else 1.0
    add Solid(accent) xysize (250, 2) pos (x, y + 27) anchor (_credit_anchor, 0.0) at enter_m_op_credit_rule(edge, duration)
    text role_text style "enter_m_op_credit_role" pos (x, y) anchor (_credit_anchor, 0.0) at enter_m_op_credit_text_in(0.05, edge, duration)
    text name_text style "enter_m_op_credit_name" pos (x, y + 34) anchor (_credit_anchor, 0.0) at enter_m_op_credit_text_in(0.14, edge, duration)
    timer duration action Hide("enter_m_op_kinetic_credit")

style enter_m_op_credit_role is enter_m_op_credit:
    size 15
    color "#9fdcef"
    kerning 4

style enter_m_op_credit_name is enter_m_op_credit:
    size 30

# Ambient particle field. kind = "dust" | "ember" | "petal".
screen enter_m_op_ambient_particles(kind="dust", duration=0.0):
    zorder 88
    if kind == "ember":
        add "enter_m_op_field_ember"
    elif kind == "petal":
        add "enter_m_op_field_petal"
    else:
        add "enter_m_op_field_dust"
    if duration > 0:
        timer duration action Hide("enter_m_op_ambient_particles")

# One-shot spark burst at a point. Reuses the project's ParticleBurst.
screen enter_m_op_spark_burst(x=640, y=360, count=46, life=0.7, sx=8.0, sy=10.0):
    zorder 93
    add ParticleBurst("enter_m_op_p_spark", numParticles=count, particleTime=life, particleXSpeed=sx, particleYSpeed=sy).sm:
        pos (x, y)
    timer life + 0.15 action Hide("enter_m_op_spark_burst")

# One-shot shader impact: overlays a shader-distorted copy of `img` whose alpha
# (and shader uniforms) decay over `duration`, leaving the clean scene behind.
# kind = "rgb" | "shock" | "zoom" | "glitch".
screen enter_m_op_impact(img, kind="rgb", duration=0.6, amount=18.0, z=1.08):
    zorder 93
    if kind == "shock":
        add img at enter_m_op_fx_shock(duration, 0.05, 0.08, z)
    elif kind == "zoom":
        add img at enter_m_op_fx_zoomblur(duration, 0.18, z)
    elif kind == "glitch":
        add img at enter_m_op_fx_glitch(duration, 0.9, z)
    else:
        add img at enter_m_op_fx_rgb(duration, amount, 0.0, z)
    timer duration + 0.08 action Hide("enter_m_op_impact")


# -----------------------------------------------------------------------------
# 4c. 90s ANIME EDITORIAL SET PIECES
# -----------------------------------------------------------------------------
# These are deliberately structural shots rather than more background pans.
# Cropped CG inserts use Matsu'Py's live Crop(rect, child) displayable (rect is
# x/y/width/height), then fit the result into a fixed editorial frame. Sprite
# strips are clipped by viewports. Every public screen owns a final timer so it
# is safe both in the beat-locked timeline and when interrupted by the OP skip.

# A phase visible from frame zero. Assignments are instantaneous on purpose:
# these screens cut like edited film rather than crossfading between layouts.
transform enter_m_op_phase_first(hold=1.0):
    alpha 1.0
    pause max(hold, 0.01)
    alpha 0.0

# A later hard-cut phase. The one-frame overlap risk of fades is avoided by
# switching alpha directly at the requested boundary.
transform enter_m_op_phase_after(delay=0.0, hold=1.0):
    alpha 0.0
    pause max(delay, 0.0)
    alpha 1.0
    pause max(hold, 0.01)
    alpha 0.0

# Aspect-preserving scale for a Crop displayable. fit "cover" is available in
# Matsu'Py 8.1.1; the crop tuple itself stays in absolute source-image pixels.
transform enter_m_op_crop_cover(w=1280, h=720):
    xysize (w, h)
    fit "cover"

# Full-composition fit used where preserving the entire 16:9 image matters.
transform enter_m_op_image_fit(w=640, h=360):
    xysize (w, h)
    fit "contain"

transform enter_m_op_fixed_alpha(value=1.0):
    alpha value

transform enter_m_op_editorial_in(delay=0.0, xoff=0, yoff=0, settle=0.16):
    alpha 0.0
    xoffset xoff
    yoffset yoff
    pause max(delay, 0.0)
    alpha 1.0
    easeout_quad max(settle, 0.01) xoffset 0 yoffset 0

transform enter_m_op_pilot_face(side=1, crop_shift=120, duration=1.2):
    subpixel True
    anchor (0.5, 1.0)
    xpos 310
    ypos (892 + crop_shift)
    zoom 1.0
    rotate (0.7 * side)
    xoffset (180 * side)
    alpha 0.0
    easeout_quad 0.14 alpha 1.0 xoffset 0
    linear max(duration - 0.14, 0.01) xoffset (-12 * side)

transform enter_m_op_hud_snap(delay=0.0, direction=1, duration=1.0):
    alpha 0.0
    xzoom 0.0
    xanchor (0.0 if direction > 0 else 1.0)
    pause delay
    easeout_quad 0.12 alpha 0.82 xzoom 1.0
    pause max(duration - delay - 0.22, 0.02)
    alpha 0.0

transform enter_m_op_duel_pose(x=320, y=754, z=0.68, rot=-3.0, direction=1, delay=0.0, duration=1.5):
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos y
    zoom (z * 0.94)
    rotate (rot - 4.0 * direction)
    xoffset (-130 * direction)
    alpha 0.0
    pause delay
    easeout_quad 0.18 alpha 1.0 xoffset 0 zoom z rotate rot
    linear max(duration - delay - 0.18, 0.01) xoffset (9 * direction) zoom (z * 1.025)

transform enter_m_op_duel_echo(x=1000, y=1440, z=1.42, direction=1, duration=1.5):
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos y
    zoom z
    alpha 0.18
    xoffset (24 * direction)
    linear duration xoffset (-18 * direction) yoffset -10

transform enter_m_op_spotlight_pose(y=852, z=0.62, duration=1.0):
    subpixel True
    anchor (0.5, 1.0)
    xpos 640
    ypos y
    zoom (z * 1.12)
    alpha 0.0
    easeout_quad 0.16 alpha 1.0 zoom z
    linear max(duration - 0.16, 0.01) zoom (z * 1.025) ypos (y - 5)

transform enter_m_op_roll_freeze(x=640, y=742, z=0.72, delay=0.0, duration=0.8, rot=0.0):
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos y
    zoom (z * 1.16)
    rotate (rot - 2.0)
    xoffset 16
    alpha 0.0
    pause delay
    alpha 1.0
    pause (duration * 0.32)
    zoom (z * 1.07) rotate (rot + 1.2) xoffset -10
    pause (duration * 0.28)
    zoom z rotate rot xoffset 0

# Two opposing clipped eye/face strips plus launch-HUD geometry. crop_a/crop_b
# are vertical sprite framing offsets in local strip coordinates.
screen enter_m_op_pilot_split(sprite_a, sprite_b, duration=1.2, accent_a="#75f7ff", accent_b="#d05f77", crop_a=120, crop_b=120):
    zorder 80
    add Solid("#04070d")
    add Solid("#0b1824") xysize (1280, 218) ypos 92
    add Solid("#1b0b13") xysize (1280, 218) ypos 410

    viewport:
        xpos 0
        ypos 92
        xysize (620, 218)
        fixed:
            xysize (620, 218)
            add sprite_a at enter_m_op_pilot_face(-1, crop_a, duration)

    viewport:
        xpos 660
        ypos 410
        xysize (620, 218)
        fixed:
            xysize (620, 218)
            add sprite_b at enter_m_op_pilot_face(1, crop_b, duration)

    add Solid(accent_a) xysize (520, 4) pos (28, 82) at enter_m_op_hud_snap(0.00, 1, duration)
    add Solid(accent_b) xysize (520, 4) pos (732, 638) at enter_m_op_hud_snap(0.05, -1, duration)
    add Solid("#ffffffb8") xysize (2, 214) pos (639, 253)
    add Solid("#ffffff9c") xysize (214, 2) pos (533, 359)
    add Solid(accent_a) xysize (18, 170) pos (622, 275) rotate 38
    add Solid(accent_b) xysize (18, 170) pos (640, 275) rotate 38
    add Solid("#ffffff66") xysize (110, 2) pos (76, 340) at enter_m_op_hud_snap(0.10, 1, duration)
    add Solid("#ffffff66") xysize (110, 2) pos (1094, 378) at enter_m_op_hud_snap(0.14, -1, duration)
    add "noise":
        alpha 0.015
    timer max(duration, 0.01) action Hide("enter_m_op_pilot_split")

# Abstract opposing-character tableau: two giant duotone echoes, two clean
# figures, and a central slash/reticle. There is intentionally no location BG.
screen enter_m_op_graphic_duel(sprite_a, sprite_b, duration=1.5, accent_a="#75f7ff", accent_b="#d39a55"):
    zorder 80
    add Solid("#03060b")
    add Solid(accent_a) xysize (640, 720) alpha 0.10
    add Solid(accent_b) xysize (640, 720) xpos 640 alpha 0.10
    add sprite_a at enter_m_op_duel_echo(210, 1430, 1.42, -1, duration), enter_m_op_flat_mod(accent_a)
    add sprite_b at enter_m_op_duel_echo(1070, 1430, 1.42, 1, duration), enter_m_op_flat_mod(accent_b)
    add sprite_a at enter_m_op_duel_pose(320, 754, 0.68, -3.0, 1, 0.00, duration), enter_m_op_sprite_shadow_mod
    add sprite_b at enter_m_op_duel_pose(960, 754, 0.68, 3.0, -1, 0.05, duration), enter_m_op_sprite_shadow_mod
    add sprite_a at enter_m_op_duel_pose(320, 754, 0.68, -3.0, 1, 0.00, duration)
    add sprite_b at enter_m_op_duel_pose(960, 754, 0.68, 3.0, -1, 0.05, duration)
    add Solid("#ffffffd8") xysize (16, 860) pos (632, -70) rotate 18
    add Solid(accent_a) xysize (4, 250) pos (592, 235) rotate 18
    add Solid(accent_b) xysize (4, 250) pos (684, 235) rotate 18
    add Solid("#ffffff8c") xysize (180, 2) pos (550, 359)
    add Solid("#ffffff8c") xysize (2, 180) pos (639, 270)
    add "noise":
        alpha 0.016
    timer max(duration, 0.01) action Hide("enter_m_op_graphic_duel")

# Isolated iconic character portrait with a typographic sun disc and a simple
# light-window halo. Only one full-colour sprite is rendered.
screen enter_m_op_spotlight(sprite, duration=1.0, accent="#75f7ff", y=852, z=0.62):
    zorder 80
    add Solid("#02040b")
    add Solid(accent) xysize (420, 720) xpos 430 alpha 0.07
    text "●":
        font "DejaVuSans.ttf"
        size 520
        color accent
        xalign 0.5
        yalign 0.47
        at enter_m_op_fixed_alpha(0.24)
    if ENTER_M_OP_SHADERS:
        add Solid("#00000000") xysize (1280, 720) at enter_m_op_rays_t(0.5, 0.46, enter_m_op_rgb(accent), 20.0, 0.34, 0.16)
    add Solid("#ffffff24") xysize (2, 560) pos (426, 80)
    add Solid("#ffffff24") xysize (2, 560) pos (852, 80)
    add sprite at enter_m_op_spotlight_pose(y, z, duration), enter_m_op_sprite_shadow_mod
    add sprite at enter_m_op_spotlight_pose(y, z, duration)
    add Solid(accent) xysize (260, 3) pos (510, 628) at enter_m_op_hud_snap(0.08, 1, duration)
    timer max(duration, 0.01) action Hide("enter_m_op_spotlight")

# Three editorial grammars in one timed screen: eye strip, sun silhouette, then
# a snapped graphic freeze. At duration 2.2 the phases are 0.7 / 0.7 / 0.8.
screen enter_m_op_character_roll(s1, s2, s3, duration=2.2, a1="#75f7ff", a2="#d39a55", a3="#d05f77"):
    zorder 80
    $ _r1 = duration * (7.0 / 22.0)
    $ _r2 = duration * (7.0 / 22.0)
    $ _r3 = max(duration - _r1 - _r2, 0.01)

    fixed:
        at enter_m_op_phase_first(_r1)
        add Solid("#03060b")
        add Solid(a1) xysize (1280, 210) ypos 255 alpha 0.16
        viewport:
            xpos 0
            ypos 255
            xysize (1280, 210)
            fixed:
                xysize (1280, 210)
                add s1 at enter_m_op_pilot_face(-1, 118, _r1):
                    xpos 640
        add Solid("#ffffffb0") xysize (900, 3) pos (190, 244)
        add Solid(a1) xysize (460, 6) pos (410, 474)

    fixed:
        at enter_m_op_phase_after(_r1, _r2)
        add Solid("#080603")
        text "●":
            font "DejaVuSans.ttf"
            size 560
            color a2
            xalign 0.5
            yalign 0.48
            at enter_m_op_fixed_alpha(0.82)
        if ENTER_M_OP_SHADERS:
            add Solid("#00000000") xysize (1280, 720) at enter_m_op_rays_t(0.5, 0.47, enter_m_op_rgb(a2), 24.0, 0.30, 0.18)
        add s2 at enter_m_op_spotlight_pose(790, 0.64, _r2), enter_m_op_flat_mod("#05070b")

    fixed:
        at enter_m_op_phase_after(_r1 + _r2, _r3)
        add Solid("#f1eee6")
        add Solid(a3) xysize (390, 900) pos (760, -80) rotate -13 alpha 0.36
        add s3 at enter_m_op_roll_freeze(656, 748, 0.74, _r1 + _r2, _r3, -1.0), enter_m_op_flat_mod(a3):
            xoffset 18
            yoffset 10
        add s3 at enter_m_op_roll_freeze(640, 742, 0.74, _r1 + _r2, _r3, -1.0)
        add Solid("#171019") xysize (760, 8) pos (260, 608) rotate -3
        add "noise":
            alpha 0.025

    timer max(duration, 0.01) action Hide("enter_m_op_character_roll")

# Generic hard-cut CG relay. Callers pass three absolute-pixel Crop rectangles;
# the third is normally a wide/full reveal. No pan or interpolated crop occurs.
screen enter_m_op_crop_relay(cg_image, crop1, crop2, crop3, duration=2.4, accent="#75f7ff"):
    zorder 80
    $ _c1 = duration * 0.28
    $ _c2 = duration * 0.28
    $ _c3 = max(duration - _c1 - _c2, 0.01)
    add Solid("#02040b")
    add Crop(crop1, cg_image) at enter_m_op_crop_cover(1280, 720), enter_m_op_phase_first(_c1)
    add Crop(crop2, cg_image) at enter_m_op_crop_cover(1280, 720), enter_m_op_phase_after(_c1, _c2)
    add Crop(crop3, cg_image) at enter_m_op_crop_cover(1280, 720), enter_m_op_phase_after(_c1 + _c2, _c3)
    add Solid(accent) xysize (1280, 7) ypos 0 at enter_m_op_phase_after(_c1 - 0.03, 0.06)
    add Solid("#ffffff") xysize (1280, 5) ypos 715 at enter_m_op_phase_after(_c1 + _c2 - 0.03, 0.06)
    add Solid("#0000002c")
    add "noise":
        alpha 0.012
    timer max(duration, 0.01) action Hide("enter_m_op_crop_relay")


# The living-room argument edited as character coverage: MC, Asahina, mother,
# then the unbroken three-person wide. Crop rectangles match arguing.png.
screen enter_m_op_argument_triptych(cg_image, duration=2.8):
    zorder 80
    $ _a1 = duration * 0.19
    $ _a2 = duration * 0.19
    $ _a3 = duration * 0.19
    $ _a4 = max(duration - _a1 - _a2 - _a3, 0.01)
    add Solid("#08070a")

    add Crop((0, 72, 520, 585), cg_image) at enter_m_op_crop_cover(1280, 720), enter_m_op_phase_first(_a1)
    add Solid("#75f7ff") xysize (18, 720) xpos 0 at enter_m_op_phase_first(_a1)

    add Crop((410, 58, 520, 600), cg_image) at enter_m_op_crop_cover(1280, 720), enter_m_op_phase_after(_a1, _a2)
    add Solid("#d05f77") xysize (18, 720) xpos 1262 at enter_m_op_phase_after(_a1, _a2)

    add Crop((880, 36, 400, 620), cg_image) at enter_m_op_crop_cover(1280, 720), enter_m_op_phase_after(_a1 + _a2, _a3)
    add Solid("#d39a55") xysize (1280, 7) ypos 0 at enter_m_op_phase_after(_a1 + _a2, _a3)

    fixed:
        at enter_m_op_phase_after(_a1 + _a2 + _a3, _a4)
        add Crop((0, 0, 1280, 720), cg_image) at enter_m_op_crop_cover(1280, 720)
        add Solid("#75f7ffb0") xysize (5, 720) xpos 420
        add Solid("#d05f77b0") xysize (5, 720) xpos 858
        add Solid("#ffffff72") xysize (1280, 3) ypos 622

    add "noise":
        alpha 0.014
    timer max(duration, 0.01) action Hide("enter_m_op_argument_triptych")

# Daylight bus memory as a perforated filmstrip. Only one cropped/full CG layer
# is visible per phase; the warm stock and white perforations provide the frame.
screen enter_m_op_memory_filmstrip(cg_image, duration=2.2):
    zorder 80
    $ _f1 = duration * 0.28
    $ _f2 = duration * 0.28
    $ _f3 = max(duration - _f1 - _f2, 0.01)
    add Solid("#171008")
    add Solid("#f1d39a") xysize (1180, 610) pos (50, 55) alpha 0.96
    add Solid("#0c0906") xysize (1120, 520) pos (80, 100)

    viewport:
        xpos 90
        ypos 110
        xysize (1100, 500)
        at enter_m_op_phase_first(_f1)
        fixed:
            xysize (1100, 500)
            add Crop((0, 35, 660, 620), cg_image) at enter_m_op_crop_cover(1100, 500)

    viewport:
        xpos 90
        ypos 110
        xysize (1100, 500)
        at enter_m_op_phase_after(_f1, _f2)
        fixed:
            xysize (1100, 500)
            add Crop((570, 30, 710, 625), cg_image) at enter_m_op_crop_cover(1100, 500)

    viewport:
        xpos 90
        ypos 110
        xysize (1100, 500)
        at enter_m_op_phase_after(_f1 + _f2, _f3)
        fixed:
            xysize (1100, 500)
            add Crop((0, 0, 1280, 720), cg_image) at enter_m_op_image_fit(1100, 500)

    for _film_x in range(16):
        add Solid("#fff3d8") xysize (42, 18) pos (70 + _film_x * 72, 68)
        add Solid("#fff3d8") xysize (42, 18) pos (70 + _film_x * 72, 634)
    add Solid("#ffffff9c") xysize (170, 3) pos (92, 92)
    add Solid("#d39a55c8") xysize (170, 3) pos (1018, 625)
    add "noise":
        alpha 0.018
    timer max(duration, 0.01) action Hide("enter_m_op_memory_filmstrip")

# The two reaching POV CGs become one match-cut sentence: red hand detail, blue
# hand detail, then two intact 16:9 compositions meeting at a white seam.
screen enter_m_op_reach_match(red_img, blue_img, duration=3.2):
    zorder 80
    $ _m1 = duration * 0.25
    $ _m2 = duration * 0.25
    $ _m3 = max(duration - _m1 - _m2, 0.01)
    add Solid("#02040b")

    add Crop((250, 105, 760, 428), red_img) at enter_m_op_crop_cover(1280, 720), enter_m_op_phase_first(_m1)
    add Solid("#d05f77") xysize (1280, 6) ypos 714 at enter_m_op_phase_first(_m1)

    add Crop((330, 155, 720, 405), blue_img) at enter_m_op_crop_cover(1280, 720), enter_m_op_phase_after(_m1, _m2)
    add Solid("#75f7ff") xysize (1280, 6) ypos 0 at enter_m_op_phase_after(_m1, _m2)

    fixed:
        at enter_m_op_phase_after(_m1 + _m2, _m3)
        add Solid("#16070d") xysize (640, 720)
        add Solid("#061221") xysize (640, 720) xpos 640
        add Crop((0, 0, 1280, 720), red_img) at enter_m_op_image_fit(620, 349):
            xpos 10
            ypos 185
        add Crop((0, 0, 1280, 720), blue_img) at enter_m_op_image_fit(620, 349):
            xpos 650
            ypos 185
        add Solid("#ffffffec") xysize (18, 860) pos (631, -70) rotate -4
        add Solid("#d05f77a0") xysize (3, 270) pos (616, 225) rotate -4
        add Solid("#75f7ffa0") xysize (3, 270) pos (661, 225) rotate -4
        add Solid("#ffffff90") xysize (230, 2) pos (525, 359)
        add Solid("#ffffff90") xysize (2, 190) pos (639, 265)

    add "noise":
        alpha 0.014
    timer max(duration, 0.01) action Hide("enter_m_op_reach_match")

# Musical-drop edit. Frame zero is ALWAYS the colour art. The gray image only
# interrupts it for about two 30-fps frames after the first colour impact.
screen enter_m_op_first_drop(gray_img, color_img, duration=3.5):
    zorder 80
    $ _d1 = duration * 0.18
    $ _dg = min(0.066, duration * 0.025)
    $ _d2 = duration * 0.20
    $ _d3 = duration * 0.18
    $ _d4 = max(duration - _d1 - _dg - _d2 - _d3, 0.01)
    $ _s2 = _d1 + _dg
    $ _s3 = _s2 + _d2
    $ _s4 = _s3 + _d3
    add Solid("#02040b")

    # Colour face/microphone impact is visible on the very first frame.
    fixed:
        at enter_m_op_phase_first(_d1)
        add Crop((250, 48, 710, 400), color_img) at enter_m_op_crop_cover(1280, 720)
        if ENTER_M_OP_SHADERS:
            add Solid("#ffffff") xysize (1280, 720) at enter_m_op_speedlines_t(0.54, 0.43, (0.82, 0.96, 1.0), 48.0, 0.12, 0.34)
        add Solid("#ffffff86") xysize (1280, 5) ypos 716

    # One/two-frame monochrome negative insert, never a pre-roll.
    fixed:
        at enter_m_op_phase_after(_d1, _dg)
        add Crop((610, 180, 670, 377), gray_img) at enter_m_op_crop_cover(1280, 720)
        add Solid("#ffffff42")
        add Solid("#75f7ff") xysize (14, 720) xpos 618
        add Solid("#ff4fb8") xysize (14, 720) xpos 648

    fixed:
        at enter_m_op_phase_after(_s2, _d2)
        add Crop((660, 190, 620, 349), color_img) at enter_m_op_crop_cover(1280, 720)
        add Solid("#ff4fb8") xysize (1280, 7) ypos 0

    fixed:
        at enter_m_op_phase_after(_s3, _d3)
        add Crop((170, 35, 650, 366), color_img) at enter_m_op_crop_cover(1280, 720)
        add Solid("#75f7ff") xysize (12, 720) xpos 0

    # Resolve on a clean, intact hero wide with only restrained corner rules.
    fixed:
        at enter_m_op_phase_after(_s4, _d4)
        add Crop((0, 0, 1280, 720), color_img) at enter_m_op_crop_cover(1280, 720)
        add Solid("#75f7ffb0") xysize (260, 4) pos (28, 28)
        add Solid("#ff4fb8b0") xysize (260, 4) pos (992, 688)

    add "noise":
        alpha 0.012
    timer max(duration, 0.01) action Hide("enter_m_op_first_drop")

transform enter_m_op_zero_g_float(duration=1.8):
    subpixel True
    anchor (0.5, 1.0)
    xpos 610
    ypos 650
    zoom 0.32
    rotate -18
    alpha 0.0
    easeout_quad 0.18 alpha 1.0
    parallel:
        ease duration xpos 685 ypos 560 rotate 12 zoom 0.35
    parallel:
        block:
            ease 0.72 xoffset -8 yoffset 5
            ease 0.72 xoffset 8 yoffset -5
            repeat

# Small drifting protagonist against one huge duotone echo and cheap orbit-line
# geometry. The abstract field is static; only the figure floats.
screen enter_m_op_zero_g(sprite, duration=1.8, accent="#75f7ff"):
    zorder 80
    add Solid("#02040b")
    if ENTER_M_OP_SHADERS:
        add Solid("#00000000") xysize (1280, 720) at enter_m_op_rays_t(0.5, 0.48, enter_m_op_rgb(accent), 28.0, 0.18, 0.12)
    add Solid(accent) xysize (940, 2) pos (170, 359) rotate -12 alpha 0.34
    add Solid("#ffffff70") xysize (760, 2) pos (260, 359) rotate 24 alpha 0.38
    add Solid(accent) xysize (560, 2) pos (360, 359) rotate 58 alpha 0.30
    add Solid("#ffffff48") xysize (420, 2) pos (430, 359) rotate -62 alpha 0.32
    add Solid(accent) xysize (330, 3) pos (475, 358) rotate 90 alpha 0.22
    add sprite at enter_m_op_duel_echo(990, 1510, 1.55, 1, duration), enter_m_op_flat_mod(accent)
    add sprite at enter_m_op_zero_g_float(duration), enter_m_op_sprite_shadow_mod
    add sprite at enter_m_op_zero_g_float(duration)
    add Solid("#ffffff82") xysize (180, 2) pos (550, 359)
    add Solid("#ffffff82") xysize (2, 180) pos (639, 270)
    add "noise":
        alpha 0.016
    timer max(duration, 0.01) action Hide("enter_m_op_zero_g")


transform enter_m_op_strip_pose(i=0, duration=0.923):
    subpixel True
    anchor (0.5, 1.0)
    xpos 640
    ypos (940 if i == 0 else (760 if i == 1 else 650))
    zoom (1.02 if i == 0 else (0.82 if i == 1 else 0.68))
    rotate (-1.0 if i == 0 else (1.0 if i == 1 else -0.4))
    alpha 0.0
    xoffset (-240 if i % 2 == 0 else 240)
    pause (0.055 * i)
    easeout_quad 0.13 alpha 1.0 xoffset 0
    linear max(duration - 0.13 - 0.055 * i, 0.01) xoffset (-10 if i % 2 == 0 else 10)

# A half-bar character beat made from three clipped framings of one sprite.
screen enter_m_op_strip_triptych(sprite, duration=0.923, accent="#75f7ff"):
    zorder 80
    add Solid("#02040b")
    for _strip_i in range(3):
        viewport:
            xpos 0
            ypos (42 + _strip_i * 222)
            xysize (1280, 180)
            fixed:
                xysize (1280, 180)
                add sprite at enter_m_op_strip_pose(_strip_i, duration)
        add Solid(accent if _strip_i != 1 else "#ffffff") xysize (1280, 4) pos (0, 38 + _strip_i * 222) alpha (0.78 if _strip_i == 0 else 0.48)
    add Solid(accent) xysize (230, 720) pos (900, 0) rotate -14 alpha 0.09
    add "noise":
        alpha 0.014
    timer max(duration, 0.01) action Hide("enter_m_op_strip_triptych")

transform enter_m_op_emblem_pose(y=742, z=0.58, duration=0.923):
    subpixel True
    anchor (0.5, 1.0)
    xpos 640
    ypos y
    zoom (z * 1.14)
    alpha 0.0
    easeout_quad 0.12 alpha 1.0 zoom z
    linear max(duration - 0.12, 0.01) zoom (z * 1.035) ypos (y - 4)

# One iconic silhouette against a literal typographic sun disc and optional
# shader rays. It is a held emblem, not a location pan.
screen enter_m_op_sun_emblem(sprite, duration=0.923, accent="#d39a55", y=742, z=0.58):
    zorder 80
    add Solid("#080603")
    text "●":
        font "DejaVuSans.ttf"
        size 610
        color accent
        xalign 0.5
        yalign 0.47
    if ENTER_M_OP_SHADERS:
        add Solid("#00000000") xysize (1280, 720) at enter_m_op_rays_t(0.5, 0.47, enter_m_op_rgb(accent), 28.0, 0.26, 0.26)
    add Solid("#fff4d0") xysize (900, 3) pos (190, 359) alpha 0.48
    add Solid(accent) xysize (3, 620) pos (639, 50) alpha 0.44
    add sprite at enter_m_op_emblem_pose(y, z, duration), enter_m_op_flat_mod("#02040b")
    add Solid("#ffffffa0") xysize (310, 4) pos (485, 632) at enter_m_op_hud_snap(0.05, 1, duration)
    add "noise":
        alpha 0.012
    timer max(duration, 0.01) action Hide("enter_m_op_sun_emblem")

transform enter_m_op_ensemble_pose(x=640, y=724, z=0.28, delay=0.0, direction=1, duration=1.8, rot=0.0):
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos (y + 42)
    zoom (z * 0.92)
    rotate (rot - 2.0 * direction)
    alpha 0.0
    xoffset (-26 * direction)
    pause delay
    easeout_quad 0.17 alpha 1.0 xpos x ypos y zoom z rotate rot xoffset 0
    linear max(duration - delay - 0.17, 0.01) ypos (y - 3) zoom (z * 1.015)

transform enter_m_op_constellation_rule(delay=0.0, duration=1.8, direction=1):
    alpha 0.0
    xzoom 0.0
    xanchor (0.0 if direction > 0 else 1.0)
    pause delay
    easeout_quad 0.16 alpha 0.62 xzoom 1.0
    pause max(duration - delay - 0.24, 0.02)
    alpha 0.0

# Sincere seven-character ensemble. All seven use the same scale, timing, and
# visual weight in every phase; Monika is one equal member of the group.
screen enter_m_op_ensemble_constellation(duration=5.538):
    zorder 80
    $ _e1 = duration / 3.0
    $ _e2 = duration / 3.0
    $ _e3 = max(duration - _e1 - _e2, 0.01)
    $ _ensemble = (
        ("matsuda neut", "#d05f77"),
        ("tsubaki neut", "#75f7ff"),
        ("asahina neut", "#d39a55"),
        ("mc neut", "#ffffff"),
        ("kotonoha neut", "#d39a55"),
        ("sam neut", "#75f7ff"),
        ("monika 1a", "#d05f77"),
    )

    # Phase one: evenly spaced staggered launch-lineup.
    fixed:
        at enter_m_op_phase_first(_e1)
        add Solid("#03060b")
        add Solid("#ffffff18") xysize (1280, 240) ypos 480
        for _ei, _entry in enumerate(_ensemble):
            $ _ex = 92 + _ei * 183
            $ _edir = -1 if _ei % 2 == 0 else 1
            add Solid(_entry[1]) xysize (132, 720) pos (_ex - 66, 0) alpha 0.055
            add _entry[0] at enter_m_op_ensemble_pose(_ex, 724, 0.28, _ei * 0.045, _edir, _e1, _edir * 0.8)
        add Solid("#ffffffa0") xysize (1160, 3) pos (60, 642)

    # Phase two: seven equal portrait wedges tied by constellation rules.
    fixed:
        at enter_m_op_phase_after(_e1, _e2)
        add Solid("#050711")
        for _ei, _entry in enumerate(_ensemble):
            $ _px = _ei * 183
            viewport:
                xpos _px
                ypos 0
                xysize (180, 720)
                fixed:
                    xysize (180, 720)
                    add Solid(_entry[1]) alpha 0.12
                    add _entry[0] at enter_m_op_ensemble_pose(90, 790, 0.48, _e1 + _ei * 0.035, -1 if _ei % 2 == 0 else 1, _e2, -3 + _ei)
            add Solid(_entry[1]) xysize (3, 720) xpos (_px + 179) alpha 0.58
        add Solid("#ffffff94") xysize (220, 2) pos (70, 214) rotate 12 at enter_m_op_constellation_rule(_e1 + 0.05, _e2, 1)
        add Solid("#75f7ff94") xysize (220, 2) pos (255, 350) rotate -14 at enter_m_op_constellation_rule(_e1 + 0.10, _e2, -1)
        add Solid("#d39a5594") xysize (220, 2) pos (440, 254) rotate 10 at enter_m_op_constellation_rule(_e1 + 0.15, _e2, 1)
        add Solid("#ffffff94") xysize (220, 2) pos (625, 382) rotate -12 at enter_m_op_constellation_rule(_e1 + 0.20, _e2, -1)
        add Solid("#75f7ff94") xysize (220, 2) pos (810, 270) rotate 13 at enter_m_op_constellation_rule(_e1 + 0.25, _e2, 1)
        add Solid("#d05f7794") xysize (220, 2) pos (995, 394) rotate -11 at enter_m_op_constellation_rule(_e1 + 0.30, _e2, -1)

    # Phase three: unified, full-colour hero tableau at one common scale.
    fixed:
        at enter_m_op_phase_after(_e1 + _e2, _e3)
        add Solid("#07101a")
        if ENTER_M_OP_SHADERS:
            add Solid("#00000000") xysize (1280, 720) at enter_m_op_rays_t(0.5, 0.46, (0.72, 0.93, 1.0), 24.0, 0.20, 0.14)
        for _ei, _entry in enumerate(_ensemble):
            $ _hx = 92 + _ei * 183
            $ _hdir = -1 if _ei % 2 == 0 else 1
            add Solid(_entry[1]) xysize (124, 390) pos (_hx - 62, 250) alpha 0.09
            add _entry[0] at enter_m_op_ensemble_pose(_hx, 724, 0.30, _e1 + _e2 + _ei * 0.035, _hdir, _e3, 0.0), enter_m_op_sprite_shadow_mod
            add _entry[0] at enter_m_op_ensemble_pose(_hx, 724, 0.30, _e1 + _e2 + _ei * 0.035, _hdir, _e3, 0.0)
        add Solid("#ffffffc0") xysize (1180, 3) pos (50, 646)
        add Solid("#75f7ff90") xysize (360, 5) pos (70, 662)
        add Solid("#d39a5590") xysize (360, 5) pos (460, 662)
        add Solid("#d05f7790") xysize (360, 5) pos (850, 662)

    add "noise":
        alpha 0.014
    timer max(duration, 0.01) action Hide("enter_m_op_ensemble_constellation")

transform enter_m_op_bus_pole(delay=0.0, direction=1):
    subpixel True
    xoffset (-1480 * direction)
    alpha 0.0
    pause delay
    alpha 0.86
    linear 0.30 xoffset (1480 * direction)
    alpha 0.0

transform enter_m_op_bus_reflection(w=1280, h=180):
    xysize (w, h)
    fit "cover"
    yzoom -1.0
    alpha 0.28

# Canon-safe Sam/MC bus edit. Every grade stays daylight cyan/amber/white; the
# sequence never references the separate samvillain art or any noir/red coding.
screen enter_m_op_sam_reflection(cg_image, duration=3.692):
    zorder 80
    $ _b1 = duration * 0.23
    $ _b2 = duration * 0.19
    $ _b3 = duration * 0.19
    $ _b4 = duration * 0.19
    $ _b5 = max(duration - _b1 - _b2 - _b3 - _b4, 0.01)
    $ _bs2 = _b1
    $ _bs3 = _b1 + _b2
    $ _bs4 = _b1 + _b2 + _b3
    $ _bs5 = _b1 + _b2 + _b3 + _b4
    add Solid("#08131c")

    # Daylight two-shot establishes their easy friendship.
    add Crop((0, 0, 1280, 720), cg_image) at enter_m_op_crop_cover(1280, 720), enter_m_op_phase_first(_b1)

    # MC's glance, then Sam's open smile; neither crop changes the grade.
    add Crop((0, 35, 650, 610), cg_image) at enter_m_op_crop_cover(1280, 720), enter_m_op_phase_after(_bs2, _b2)
    add Solid("#75f7ff") xysize (10, 720) xpos 0 at enter_m_op_phase_after(_bs2, _b2)

    add Crop((565, 25, 715, 620), cg_image) at enter_m_op_crop_cover(1280, 720), enter_m_op_phase_after(_bs3, _b3)
    add Solid("#d39a55") xysize (10, 720) xpos 1270 at enter_m_op_phase_after(_bs3, _b3)

    # Window/reflection split with bus-pole wipes crossing the edit.
    fixed:
        at enter_m_op_phase_after(_bs4, _b4)
        add Solid("#d9f1ff")
        viewport:
            xpos 0
            ypos 0
            xysize (630, 540)
            fixed:
                xysize (630, 540)
                add Crop((0, 35, 650, 610), cg_image) at enter_m_op_crop_cover(630, 540)
                add Solid("#75f7ff24")
        viewport:
            xpos 650
            ypos 0
            xysize (630, 540)
            fixed:
                xysize (630, 540)
                add Crop((565, 25, 715, 620), cg_image) at enter_m_op_crop_cover(630, 540)
                add Solid("#d39a5524")
        viewport:
            xpos 0
            ypos 550
            xysize (1280, 170)
            fixed:
                xysize (1280, 170)
                add Crop((0, 0, 1280, 720), cg_image) at enter_m_op_bus_reflection(1280, 170)
        add Solid("#fff4c8") xysize (18, 900) pos (420, -90) rotate 5 at enter_m_op_bus_pole(_bs4, 1)
        add Solid("#d5edff") xysize (14, 900) pos (850, -90) rotate 5 at enter_m_op_bus_pole(_bs4 + 0.08, -1)
        add Solid("#ffffffd0") xysize (8, 720) xpos 636

    # Resolve to the untouched daylight two-shot.
    fixed:
        at enter_m_op_phase_after(_bs5, _b5)
        add Crop((0, 0, 1280, 720), cg_image) at enter_m_op_crop_cover(1280, 720)
        add Solid("#ffffffa0") xysize (280, 3) pos (30, 30)
        add Solid("#75f7ff80") xysize (280, 3) pos (970, 687)

    add "noise":
        alpha 0.010
    timer max(duration, 0.01) action Hide("enter_m_op_sam_reflection")


# -----------------------------------------------------------------------------
# 5. META-COMMENTARY BEAT
# -----------------------------------------------------------------------------
# A self-aware gag: present the wholly-original cast, then reveal the punchline
# that the ONLY thing making this a DDLC mod is Monika standing there. Edit the
# on-screen copy below to taste.

transform enter_m_op_meta_pose(x=640, y=716, z=0.34, delay=0.0, rot=0.0):
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos y
    zoom (z * 0.9)
    rotate rot
    alpha 0.0
    pause delay
    easeout 0.18 alpha 1.0 zoom (z * 1.04)
    ease 0.12 zoom z
    block:
        ease 1.0 yoffset -3
        ease 1.0 yoffset 0
        repeat

transform enter_m_op_meta_solo(x=640, y=852, z=0.62):
    subpixel True
    anchor (0.5, 1.0)
    xpos x
    ypos y
    zoom z
    alpha 0.0
    easeout 0.22 alpha 1.0
    parallel:
        linear 2.0 zoom (z * 1.04) ypos (y - 6)
    parallel:
        block:
            ease 1.2 xoffset 4
            ease 1.2 xoffset 0
            repeat

transform enter_m_op_meta_text_in2:
    alpha 0.0
    yoffset -10
    pause 0.38
    easeout 0.30 alpha 1.0 yoffset 0

# Demotes a sprite to a dim, desaturated "placeholder" behind Monika.
transform enter_m_op_meta_dim_mod:
    matrixcolor SaturationMatrix(0.15) * BrightnessMatrix(-0.45)
    alpha 0.55

# The original cast lined up, presented straight -- no caption, let it read as
# "here's the show."
screen enter_m_op_meta_lineup(duration=1.5):
    zorder 80
    add "assets/dump/finalbg.png" at enter_m_op_bg_breathe(duration, 0.46, 0.54, 0.5, 0.46)
    add Solid("#03060bcc")
    add Solid("#75f7ff") at enter_m_op_stage_beam(190, 0.00, -8)
    add Solid("#d39a55") at enter_m_op_stage_beam(900, 0.10, 8)
    add "matsuda neut"  at enter_m_op_meta_pose(150, 716, 0.34, 0.00, -2)
    add "tsubaki neut"  at enter_m_op_meta_pose(335, 716, 0.34, 0.05, 2)
    add "asahina neut"  at enter_m_op_meta_pose(520, 716, 0.34, 0.10, -2)
    add "mc neut"       at enter_m_op_meta_pose(705, 716, 0.34, 0.15, 1)
    add "kotonoha neut" at enter_m_op_meta_pose(890, 716, 0.34, 0.20, -1)
    add "sam neut"      at enter_m_op_meta_pose(1075, 716, 0.34, 0.25, 2)
    add "noise":
        alpha 0.02

# The reveal, played dry: the cast dims to placeholders while Monika steps
# forward in full colour. The only words are a fine-print footnote.
screen enter_m_op_meta_monika(duration=1.5):
    zorder 80
    add "assets/dump/finalbg.png" at enter_m_op_bg_breathe(duration, 0.54, 0.46, 0.5, 0.46)
    add Solid("#03060be6")
    add "matsuda neut"  at enter_m_op_meta_pose(150, 716, 0.34, 0.00, -2), enter_m_op_meta_dim_mod
    add "tsubaki neut"  at enter_m_op_meta_pose(335, 716, 0.34, 0.00, 2), enter_m_op_meta_dim_mod
    add "asahina neut"  at enter_m_op_meta_pose(520, 716, 0.34, 0.00, -2), enter_m_op_meta_dim_mod
    add "kotonoha neut" at enter_m_op_meta_pose(890, 716, 0.34, 0.00, -1), enter_m_op_meta_dim_mod
    add "sam neut"      at enter_m_op_meta_pose(1075, 716, 0.34, 0.00, 2), enter_m_op_meta_dim_mod
    add Solid("#ffffff") at enter_m_op_stage_beam(640, 0.00, 0)
    add "monika 1a" at enter_m_op_meta_solo(640, enter_m_op_monika_y, enter_m_op_monika_zoom)
    text "* technically a doki doki literature club mod":
        style "enter_m_op_credit"
        size 24
        xalign 0.5
        yalign 0.5
        at enter_m_op_meta_text_in2
    add "noise":
        alpha 0.02


# -----------------------------------------------------------------------------
# 6. TURMOIL :: BREAKING PSYCHE
# -----------------------------------------------------------------------------
# The original turmoil beat was a slow, controlled zoom. This is MC's mind
# coming apart: erratic zoom swells, hard jitter, rotation kicks, colour
# flicker, and a sustained datamosh + chromatic tear layered over the top.

transform enter_m_op_turmoil_chaos(duration=2.6):
    subpixel True
    zoom 1.08
    xalign 0.5
    yalign 0.48
    rotate 0
    matrixcolor BrightnessMatrix(-0.10) * SaturationMatrix(0.30)
    easeout 0.10 zoom 1.12
    parallel:
        block:
            easeout 0.30 zoom 1.24
            ease 0.22 zoom 1.10
            easeout 0.16 zoom 1.32
            ease 0.24 zoom 1.14
            easeout 0.12 zoom 1.38
            ease 0.28 zoom 1.18
            repeat
    parallel:
        block:
            linear 0.022 xoffset -8 yoffset 4
            linear 0.022 xoffset 7 yoffset -5
            linear 0.026 xoffset -5 yoffset 2
            linear 0.022 xoffset 6 yoffset -3
            pause 0.028
            repeat
    parallel:
        block:
            ease 0.50 rotate -1.3
            ease 0.42 rotate 1.1
            ease 0.34 rotate -0.8
            ease 0.30 rotate 1.0
            repeat
    parallel:
        block:
            matrixcolor BrightnessMatrix(-0.12) * SaturationMatrix(0.26)
            pause 0.18
            matrixcolor BrightnessMatrix(0.07) * SaturationMatrix(0.92)
            pause 0.05
            matrixcolor BrightnessMatrix(-0.24) * SaturationMatrix(0.14)
            pause 0.12
            repeat

# Sustained, pulsing datamosh for the whole break (vs. the one-shot impact).
transform enter_m_op_fx_glitch_loop(duration=2.6):
    mesh True
    shader "enter_m.glitch"
    u_blocks 30.0
    u_speed 22.0
    u_amount 0.16
    u_intensity 0.55
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.10
    alpha 0.55
    block:
        easein 0.10 u_intensity 0.95 alpha 0.82
        easeout 0.22 u_intensity 0.40 alpha 0.42
        pause 0.12
        repeat

# Hard, pulsing chromatic tear that never quite settles.
transform enter_m_op_fx_rgb_loop(duration=2.6):
    mesh True
    shader "enter_m.rgbsplit"
    u_angle 0.0
    u_amount 6.0
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.10
    alpha 0.5
    block:
        easein 0.08 u_amount 24.0
        easeout 0.30 u_amount 5.0
        pause 0.16
        repeat

screen enter_m_op_psyche_break(img, duration=2.6):
    zorder 91
    add img at enter_m_op_fx_glitch_loop(duration)
    add img at enter_m_op_fx_rgb_loop(duration)
    timer duration action Hide("enter_m_op_psyche_break")
