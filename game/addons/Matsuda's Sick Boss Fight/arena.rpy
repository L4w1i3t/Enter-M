# =============================================================================
# arena.rpy  --  MATSUDA'S SICK BOSS FIGHT :: THE 2.5D ARENA
# =============================================================================
#
# WHAT THIS FILE IS
#   The fight used to be three chrome boxes on a dead plate: the boss lived in
#   a 786x458 window with a visible seam around it, standing on nothing. This
#   file replaces that window with a PLACE -- a platform floating in the void,
#   drawn with a real perspective projection, that the boss and the party both
#   stand ON.
#
#   Nothing here knows the battle rules. It takes a phase, a handful of 0..1
#   intensities polled off MSBFBattleState, and draws a room.
#
# CURRENT ROOM
#   msbf_seer_environment owns the three illustrated arenas and their moving
#   light, wind and debris. This file supplies phase data and world staging.
#   The procedural shader below is retained for compatibility; its projection
#   notes describe that shader, not the active painted environment.
#
# THE RETAINED PROCEDURAL PROJECTION
#   The floor is the classic inverse-y pseudo-3D plane. For a pixel below the
#   horizon at `below = uv.y - h`:
#       z  = K / below                  -- depth; -> infinity at the horizon
#       wx = (uv.x - 0.5) * z * SPREAD   -- world x at that depth
#   Everything on the ground (grid, sigil, shockwaves, the light pooling under
#   her) is then just a function of (wx, z), which is why they all agree with
#   each other for free and converge correctly at the vanishing point.
#
#   The CEILING is the same math mirrored through the horizon with its own K,
#   which is nearly free and is the single biggest reason the space reads as an
#   interior rather than a backdrop.
#
#   Above the horizon the retained shader samples the phase's configured sky
#   plate and parallaxes it against the camera. These compatibility aliases
#   now point to the same cyan, gold and rupture paintings as the active room.
#
# WHAT MAKES THE BOSS STAND IN IT (rather than float over it)
#   msbf_ground_shadow   : a soft ellipse on the floor at her feet, squashed by
#                          the floor angle. Phases 2-3 hover, so their shadow
#                          sits LOWER on screen than their lowest pixel and
#                          shrinks -- which is what selling "airborne" costs.
#   msbf_ground_bounce   : her own key light pooled and rippling on the deck.
#   msbf_boss_reflection : a flipped, squashed, dimmed copy of the sprite.
#
# THE PARTY IS IN THE WORLD NOW
#   msbf_party_stage draws each member as a near-black silhouette standing
#   downstage, cropped by the bottom of the frame (the Persona read). Depth is
#   faked by eye, not by the formula -- see MSBF_STAGE_SLOTS for why.
#
# SHADERS REGISTERED HERE
#   msbf.arena   : the environment (sky plate + floor + ceiling + sigil + fog).
#   msbf.shadow  : soft dark ellipse; the only shader here that DARKENS.
#   msbf.smear   : one-pass directional ghosting -- replaces the 2-3 extra
#                  full-size boss sprite draws the old afterimages cost.
#   msbf.scrim   : a soft gradient wash for the HUD bands (replaces stacked
#                  Solids, and unlike them it has no visible top edge).
#
# NOTE: every shader path is guarded by MSBF_ARENA_SHADERS with a flat fallback,
#   matching fx.rpy's contract -- a refusing driver loses the room, not the fight.
# =============================================================================

# -----------------------------------------------------------------------------
# 1. SHADERS
# -----------------------------------------------------------------------------
init -10 python:

    def _msbf_register_arena_shaders():

        # ---- THE ARENA ----------------------------------------------------
        # One draw for the entire environment. See the projection note in the
        # file header; the uniforms are all polled off battle state by
        # msbf_arena_uniforms() below.
        renpy.register_shader("msbf.arena", variables="""
            uniform sampler2D tex0;
            uniform float u_time;
            uniform vec2 u_model_size;
            uniform float u_ar_phase;
            uniform float u_ar_horizon;
            uniform float u_ar_camx;
            uniform float u_ar_camy;
            uniform float u_ar_shock;
            uniform float u_ar_shock_amp;
            uniform float u_ar_charge;
            uniform float u_ar_danger;
            uniform float u_ar_break;
            uniform float u_ar_glitch;
            uniform float u_ar_flow;
            uniform float u_ar_bossz;
            uniform vec3 u_ar_key;
            uniform vec3 u_ar_fog;
            uniform vec3 u_ar_deck;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float ar_hash(vec2 p) {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
            }
            float ar_noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                f = f * f * (3.0 - 2.0 * f);
                float a = ar_hash(i);
                float b = ar_hash(i + vec2(1.0, 0.0));
                float c = ar_hash(i + vec2(0.0, 1.0));
                float d = ar_hash(i + vec2(1.0, 1.0));
                return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
            }
            float ar_fbm(vec2 p) {
                float v = 0.0;
                float a = 0.5;
                for (int i = 0; i < 3; i++) {
                    v += a * ar_noise(p);
                    p = p * 2.13 + vec2(7.3, 11.1);
                    a *= 0.5;
                }
                return v;
            }
            // Distance to the nearest integer boundary, as a 0..1 line mask.
            float ar_line(float x, float w) {
                return smoothstep(w, 0.0, abs(fract(x + 0.5) - 0.5));
            }
        """, fragment_300="""
            const float AR_TAU = 6.2831853;
            // SPREAD is the one number that decides whether a circle drawn on
            // the deck is visible at all. The frame only shows depths ~0.73 to
            // ~6, so if world-x is scaled much wider than that the ring around
            // her runs off both sides of the screen and all you ever see is its
            // far arc squeezed onto the horizon -- geometrically correct and
            // completely useless. 2.2 puts x and z on comparable scales, which
            // is why the seal reads as an ellipse she is standing inside.
            const float AR_SPREAD = 2.2;   // world-x units per unit depth
            const float AR_KF = 0.32;      // floor depth constant
            const float AR_KC = 0.52;      // ceiling depth constant (higher room)

            vec2 uv = v_tex_coord;
            float t = u_time;

            float ph = clamp(u_ar_phase, 1.0, 3.0);
            float p2 = clamp(ph - 1.0, 0.0, 1.0);   // 0 in phase 1, 1 by phase 2
            float p3 = clamp(ph - 2.0, 0.0, 1.0);   // 0 until phase 2, 1 in phase 3
            float brk = clamp(u_ar_break, 0.0, 1.0);
            float glt = clamp(u_ar_glitch, 0.0, 1.0);
            float chg = clamp(u_ar_charge, 0.0, 1.0);
            float dgr = clamp(u_ar_danger, 0.0, 1.0);

            float h = u_ar_horizon + u_ar_camy;
            float cx = uv.x - 0.5 - u_ar_camx;

            // Phase 3 tears whole rows sideways before anything is drawn, so
            // the floor, the sigil and the sky all break along the SAME seam.
            float rowSeed = floor(uv.y * 96.0);
            float tear = (ar_hash(vec2(rowSeed, floor(t * 18.0))) - 0.5)
                        * (0.055 * glt + 0.10 * brk);
            cx += tear;

            vec3 col = vec3(0.0);

            // ================= SKY (above the horizon) =====================
            // The plate, parallaxed and pushed back by fog. Sampled in a
            // squeezed band so the void reads as very far away rather than as
            // wallpaper hung a metre behind her.
            float above = h - uv.y;

            // SKY / CEILING and FLOOR are the two halves of one frame and they
            // are mutually exclusive, so they are written as one branch. They
            // used to be an unconditional block followed by `if (below > 0.0)`,
            // which meant every pixel BELOW the horizon still paid for the sky:
            // a dependent texture fetch, a three-octave fbm, and from phase 2
            // an atan + pow(x,5) shaft term -- all of it discarded one line
            // later when the floor assigned over col. That is a little under
            // half the frame doing double work on the most expensive shader in
            // the project.
            if (above > 0.0) {
                float skyT = clamp(above / max(h, 0.001), 0.0, 1.0);
                vec2 suv = vec2(0.5 + cx * 0.86 + sin(t * 0.05) * 0.006,
                                0.06 + (1.0 - skyT) * 0.62 - u_ar_camy * 0.5);
                vec3 plate = texture2D(tex0, clamp(suv, 0.001, 0.999)).rgb;

                // Exposure, not deletion: the void keeps its detail, it is just
                // a long way off and the arena's own light is brighter. Kept
                // deliberately under-exposed -- at full brightness the plate is
                // busier than the boss and the eye goes to the wrong thing.
                col = plate * (0.15 + 0.40 * skyT);
                col = mix(col, u_ar_fog, (1.0 - skyT) * 0.80);

                // Slow drift in the deep field, so the sky is never static.
                float neb = ar_fbm(vec2(cx * 2.2 + t * 0.012, uv.y * 2.6 - t * 0.008));
                col += u_ar_fog * smoothstep(0.55, 1.0, neb) * 0.16 * skyT;

                // Phase 2 opens the roof: shafts pouring down from high up.
                if (p2 > 0.001) {
                    vec2 rc = vec2(cx, uv.y - 0.02);
                    float ray = 0.5 + 0.5 * sin(atan(rc.x, max(rc.y, 0.001)) * 22.0 - t * 0.28);
                    ray = pow(ray, 5.0) * smoothstep(0.0, 0.55, length(rc));
                    col += u_ar_key * ray * 0.42 * p2 * (1.0 - p3 * 0.55) * skyT;
                }

            // ================= CEILING (just above the horizon) ============
            // Same projection mirrored. Struts hooping the room; they converge
            // on the vanishing point, which is most of why the space closes.
            // Inside the sky's branch -- there is no ceiling below the horizon.
                float ay = max(above, 0.0008);
                float zc = AR_KC / ay;
                float wxc = cx * zc * AR_SPREAD;
                float scroll = t * u_ar_flow * 0.16;

                // Near the horizon the struts converge past the pixel grid, so
                // they are faded out there -- that fade IS the depth fog.
                float cfog = smoothstep(0.0, 0.30, above) * smoothstep(0.86, 0.34, above);
                float lwc = 0.030 + 0.10 * (1.0 - cfog);

                // The RAILS are the ones doing the work: lines of constant
                // world-x converge on the vanishing point, and convergence is
                // what the eye reads as depth. The struts (constant depth) are
                // horizontal and, on their own, read as scanlines -- so they
                // are kept well under the rails rather than above them.
                float strut = ar_line(zc * 1.2 + scroll, lwc) * 0.55;
                float rail = ar_line(wxc * 1.5, lwc * 0.8);

                // Phase 3 shakes the ceiling apart on a stepped clock.
                float cjit = (ar_hash(vec2(floor(zc * 0.5 + scroll), floor(t * 7.0))) - 0.5)
                            * 2.2 * (glt + brk);
                strut *= 1.0 - clamp(abs(cjit), 0.0, 0.85) * p3;

                vec3 cc = mix(u_ar_fog, u_ar_key, 0.35);
                col += cc * (strut * 0.13 + rail * 0.21) * cfog;
                // A little of the key light caught on the underside.
                col += u_ar_key * rail * cfog * 0.12 * (0.6 + 0.8 * chg);

            // ================= FLOOR (below the horizon) ===================
            } else {
                float below = -above;
                float fy = max(below, 0.0008);
                float z = AR_KF / fy;
                float wx = cx * z * AR_SPREAD;
                float scroll = t * u_ar_flow * 0.22;

                // fog: 0 at the horizon (nothing resolves), 1 near the camera.
                float fog = smoothstep(0.0, 0.20, below);
                float lw = 0.028 + 0.13 * (1.0 - fog);

                // --- the deck itself ---
                vec3 deck = u_ar_deck * (0.55 + 0.75 * fog);
                // Brushed/veined material so it is a surface, not a colour.
                float vein = ar_fbm(vec2(wx * 0.42, z * 0.55 - scroll * 0.5));
                deck *= 0.80 + 0.55 * vein;

                // --- the grid ---
                float gz = ar_line(z * 1.2 + scroll, lw);
                float gx = ar_line(wx * 1.5, lw);
                float grid = max(gz, gx * 0.72);

                // Phase 3 displaces whole tiles out of true.
                float tile = ar_hash(vec2(floor(wx * 1.5), floor(z * 1.2 + scroll)));
                grid *= 1.0 - step(0.72, tile) * (glt * 0.9) * p3;

                vec3 fcol = deck + mix(u_ar_fog, u_ar_key, 0.55) * grid * (0.26 + 0.24 * fog);

                // --- the floor sigil, lying flat under her ---
                // This is the payoff of doing the projection properly: a ring
                // on the ground, in perspective, that she is standing inside.
                // Radii are in world units and the visible deck is only ~5 deep,
                // so these stay small -- see the AR_SPREAD note above.
                vec2 fp = vec2(wx, z - u_ar_bossz);
                float fr = length(fp);
                float fang = atan(fp.y, fp.x);

                float sig = 0.0;
                sig += smoothstep(0.13, 0.0, abs(fr - 1.12)) * 0.85;
                sig += smoothstep(0.09, 0.0, abs(fr - 1.72)) * 0.50;
                // A dashed band turning slowly between them.
                float dash = step(0.42, fract((fang / AR_TAU) * 20.0 + t * 0.06));
                sig += smoothstep(0.20, 0.0, abs(fr - 1.42)) * dash * 0.42;
                // Phase 2 adds a second, grander seal further out.
                sig += smoothstep(0.11, 0.0, abs(fr - 2.45)) * 0.55 * p2;
                // Phase 3 breaks it into arcs instead of rings.
                float arcs = step(0.30, fract(fang / AR_TAU * 7.0 + t * 0.02));
                sig *= mix(1.0, arcs, p3 * 0.85);

                // The seal is where the charge gathers before she casts.
                sig *= 0.55 + 1.30 * chg + 0.30 * dgr;
                fcol += u_ar_key * sig * fog * 1.15;

                // --- impact shockwave, travelling out along the deck -------
                float shk = clamp(u_ar_shock, 0.0, 1.0);
                if (shk > 0.001) {
                    // Radius, thickness and brightness all scale with how hard
                    // the blow landed, so a miss ripples and a crit slams.
                    float amp = clamp(u_ar_shock_amp, 0.2, 2.0);
                    float sr = shk * (2.2 + 1.4 * amp);
                    float ring = smoothstep(0.12 + 0.10 * amp, 0.0, abs(fr - sr));
                    fcol += vec3(1.0) * ring * (1.0 - shk) * (0.9 + 0.8 * amp) * fog;
                }

                // --- her light pooled on the deck ---------------------------
                // A wet, rippling column under her. This plus the shadow is
                // what stops the sprite reading as a sticker.
                float pool = exp(-abs(cx) * 5.5) * exp(-below * 2.6);
                pool *= 0.72 + 0.28 * sin(uv.y * 120.0 - t * 2.4);
                fcol += u_ar_key * pool * (0.34 + 0.60 * chg);

                // Depth fog swallows the far deck into the horizon colour.
                fcol = mix(u_ar_fog * 0.6, fcol, fog);

                col = fcol;
            }

            // ================= WHOLE-ROOM TREATMENT ========================
            // The horizon seam itself: a hot line where the deck meets the void.
            col += mix(u_ar_fog, u_ar_key, 0.7)
                    * exp(-abs(uv.y - h) * 150.0) * (0.55 + 0.9 * chg);

            // Phase 3: a second, offset copy of the room bleeding through, so
            // the space itself refuses to settle on one geometry.
            if (p3 > 0.001) {
                float ghost = ar_fbm(vec2(uv.x * 8.0, uv.y * 8.0 - t * 0.7));
                col += vec3(0.55, 0.08, 0.14) * smoothstep(0.62, 0.98, ghost)
                    * p3 * (0.25 + 0.75 * glt);
            }

            // Danger: the room itself starts to beat when she is nearly done.
            col *= 1.0 + dgr * 0.14 * sin(t * 5.2);
            // A phase break blows the whole room out. Kept modest: the
            // break and reveal cinematics bring their own light now, and
            // at 0.55 this lifted the entire arena into a flat haze that
            // the shaft had nothing left to stand out against.
            col += vec3(1.0) * brk * 0.30;

            // Grain + vignette. The vignette is doing real work here: it is the
            // only thing keeping the HUD legible over a full-bleed environment.
            //
            // The grain is SIGNED. `max(n - 0.5, 0.0)` is one-sided -- it can
            // only ever add light -- so it was raising the mean of every pixel
            // in the room by half its own amplitude, which is a veil laid over
            // the picture rather than a texture in it. The void above the
            // horizon is the deepest black in the fight and it was never
            // actually reaching black. Signing it keeps the identical grain
            // structure and puts the mean back where the lighting put it, and
            // the amplitude goes up a touch to compensate for now spending half
            // its range downward.
            //
            // It is also weighted DOWN in the darkest parts of the frame, where
            // grain is loudest against its background and reads as sensor noise
            // rather than as film. That weighting doubles as the dither for
            // every smooth gradient above it, which is why this shader needs no
            // separate dither the way the scrim and glow do.
            float n = ar_hash(uv * u_model_size + vec2(t * 61.0)) - 0.5;
            float glum = dot(col, vec3(0.299, 0.587, 0.114));
            col += vec3(n) * (0.075 + 0.06 * p3) * (0.40 + 0.60 * smoothstep(0.0, 0.28, glum));
            vec2 vc = uv - 0.5;
            float vig = smoothstep(0.40, 1.05, length(vc) * 1.32);
            col *= 1.0 - vig * 0.72;

            gl_FragColor = vec4(col, 1.0);
        """)

        # ---- GROUND SHADOW ------------------------------------------------
        # The only shader in the fight that DARKENS instead of adding light.
        # Premultiplied black: vec4(0,0,0,a) multiplies the destination by
        # (1-a), which is exactly a shadow. u_sh_soft pushes the penumbra out
        # as the caster gets further off the deck.
        renpy.register_shader("msbf.shadow", variables="""
            uniform float u_sh_strength;
            uniform float u_sh_soft;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 d = (v_tex_coord - vec2(0.5)) * 2.0;
            float r = length(d);
            float a = pow(clamp(1.0 - r, 0.0, 1.0), max(u_sh_soft, 0.05));
            a *= clamp(u_sh_strength, 0.0, 1.0);
            gl_FragColor = vec4(0.0, 0.0, 0.0, a);
        """)

        # ---- ONE-PASS MOTION SMEAR ----------------------------------------
        # The old afterimages drew the ENTIRE 735px boss sprite two or three
        # extra times per frame, which was the single most expensive thing on
        # screen. This does the same read in one pass: five taps along a
        # direction vector, weighted down, plus a per-channel split so the
        # phase-3 ghost comes free instead of costing another whole draw.
        renpy.register_shader("msbf.smear", variables="""
            uniform sampler2D tex0;
            uniform float u_time;
            uniform vec2 u_sm_dir;
            uniform float u_sm_amount;
            uniform float u_sm_split;
            uniform float u_sm_ghost;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            vec4 base = texture2D(tex0, uv);

            // u_sm_amount is in PERCENT OF THE SPRITE, not pixels: one unit is
            // a 1% step and the furthest tap is 4.6 steps out, so 1.0 already
            // trails ~4.6% of her width. Anything past ~3 stops being a trail
            // and becomes a smear across half the screen.
            vec2 step_ = u_sm_dir * u_sm_amount * 0.01;
            vec4 trail = vec4(0.0);
            trail += texture2D(tex0, uv - step_ * 1.0) * 0.34;
            trail += texture2D(tex0, uv - step_ * 2.0) * 0.26;
            trail += texture2D(tex0, uv - step_ * 3.2) * 0.18;
            trail += texture2D(tex0, uv - step_ * 4.6) * 0.12;

            // Chromatic split, wobbling -- the identity refusing to resolve.
            if (u_sm_split > 0.001) {
                float wob = 1.0 + 0.35 * sin(u_time * 19.0);
                vec2 off = vec2(u_sm_split * wob * 0.0016, 0.0);
                base.r = texture2D(tex0, uv + off).r;
                base.b = texture2D(tex0, uv - off).b;
            }

            gl_FragColor = base + trail * u_sm_ghost;
        """)

        # ---- HUD SCRIM ----------------------------------------------------
        # A gradient wash under the readouts. Stacked Solids always show their
        # own edge as a band across the art; this one reaches zero, so the HUD
        # sits on the room instead of on a plate laid over it.
        #
        # It has to fade on BOTH axes. A wash that only ramps vertically still
        # ends in a dead-straight vertical seam wherever its box stops, and a
        # 720px-wide panel over a live environment shows that seam immediately.
        #   u_sc_dir  :  0 = darkest at the bottom, 1 = darkest at the top.
        #   u_sc_xdir :  0 = full width, 1 = fades out rightward,
        #               -1 = fades out leftward (for a right-anchored readout).
        # DITHERED, for the same reason as msbf.glow: this is the largest,
        # smoothest, darkest ramp in the fight -- a 760x260 pow() falloff laid
        # straight over the room -- and it is the one the eye is most likely to
        # be resting on, since the boss's name and health sit on top of it.
        renpy.register_shader("msbf.scrim", variables="""
            uniform vec3 u_sc_col;
            uniform float u_sc_alpha;
            uniform float u_sc_dir;
            uniform float u_sc_xdir;
            uniform float u_sc_bias;
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
            float bias = max(u_sc_bias, 0.05);
            float y = mix(v_tex_coord.y, 1.0 - v_tex_coord.y, clamp(u_sc_dir, 0.0, 1.0));
            float a = pow(clamp(y, 0.0, 1.0), bias) * clamp(u_sc_alpha, 0.0, 1.0);

            float xf = 1.0;
            if (u_sc_xdir > 0.5) {
                xf = pow(clamp(1.0 - v_tex_coord.x, 0.0, 1.0), bias);
            } else if (u_sc_xdir < -0.5) {
                xf = pow(clamp(v_tex_coord.x, 0.0, 1.0), bias);
            }
            a *= xf;

            a = clamp(a + (msbf_ign(gl_FragCoord.xy) - 0.5) * 0.0039, 0.0, 1.0);
            gl_FragColor = vec4(u_sc_col * a, a);
        """)

    try:
        _msbf_register_arena_shaders()
        MSBF_ARENA_SHADERS = True
    except Exception as _msbf_arena_e:
        MSBF_ARENA_SHADERS = False
        if config.developer:
            renpy.log("MSBF ARENA: shader registration failed: %r" % (_msbf_arena_e,))


# -----------------------------------------------------------------------------
# 2. ARENA GEOMETRY + PER-PHASE DRESSING
# -----------------------------------------------------------------------------
init -1 python:

    # --- WHERE THE BOSS STANDS ------------------------------------------------
    # Per phase: (sprite w, sprite h, centre x, centre y, floor-contact y,
    # shadow width, shadow strength). ALL THREE PHASES ARE AIRBORNE -- the
    # phase-1 art is a mid-leap pose, not a standing one, and giving it a
    # tight contact shadow at the sprite's own bottom edge just made her look
    # pasted onto the deck. So the contact point sits further downstage (a
    # LOWER screen y than her lowest pixel) and the shadow is wide and soft;
    # that offset is the entire cost of selling "hovering".
    MSBF_BOSS_STAGE = {
        1: {"w": 700, "h": 435, "cx": 640, "cy": 296, "foot": 566,
            "shadow_w": 330, "shadow_a": 0.62, "airborne": True},
        2: {"w": 880, "h": 462, "cx": 640, "cy": 286, "foot": 596,
            "shadow_w": 400, "shadow_a": 0.56, "airborne": True},
        3: {"w": 880, "h": 462, "cx": 640, "cy": 282, "foot": 610,
            "shadow_w": 430, "shadow_a": 0.50, "airborne": True},
    }

    def msbf_boss_stage(phase):
        try:
            phase = int(phase)
        except (TypeError, ValueError):
            phase = 1
        return MSBF_BOSS_STAGE.get(min(3, max(1, phase)), MSBF_BOSS_STAGE[1])

    # --- PER-PHASE ROOM -------------------------------------------------------
    # key  : the arena's light. Everything the room emits is this colour.
    # fog  : what distance turns into -- also the horizon and the far deck.
    # deck : the platform's own material colour, unlit.
    # sky  : the plate hung in the void behind it all.
    MSBF_ARENA_PHASE = {
        # Phase 1: a cold obsidian deck in deep space. Restrained on purpose --
        # there is nowhere to escalate to if the first bar is already loud.
        1: {
            "key":  (0.30, 0.78, 1.00),
            "fog":  (0.045, 0.085, 0.150),
            "deck": (0.030, 0.052, 0.082),
            "sky":  MSBF_SEER_PLATES[1],
            "flow": 0.85,
        },
        # Phase 2: the deck turns to gold and the roof opens. Same room, lit
        # like a cathedral instead of a hangar.
        2: {
            "key":  (1.00, 0.80, 0.38),
            "fog":  (0.100, 0.085, 0.075),
            "deck": (0.062, 0.052, 0.038),
            "sky":  MSBF_SEER_PLATES[2],
            "flow": 1.15,
        },
        # Phase 3: the room stops agreeing with itself. Red, white and black
        # only -- the palette is doing the "this is not a place any more" work.
        3: {
            "key":  (1.00, 0.24, 0.34),
            "fog":  (0.085, 0.030, 0.045),
            "deck": (0.055, 0.030, 0.038),
            "sky":  MSBF_SEER_PLATES[3],
            "flow": 1.85,
        },
    }

    def msbf_arena_cfg(phase):
        try:
            phase = int(phase)
        except (TypeError, ValueError):
            phase = 1
        return MSBF_ARENA_PHASE.get(min(3, max(1, phase)), MSBF_ARENA_PHASE[1])

    def msbf_stage_anchor(i, n=4):
        """Where FX aimed at member i should land -- their pixel sprite's chest.

        Since the Sep 30 2026 facelift the party stands in the room as pixel
        sprites (pixel_stage.rpy), so everything aimed at a member -- floating
        numbers, KO bursts, a heal -- lands on the FIGURE, read from the same
        formation function the stage draws them with. The live battle supplies
        the member's id and row; the acting member stands a step forward.
        """
        b = getattr(store, "msbf_battle_state", None)
        try:
            party = b.party if b is not None else None
            if party and 0 <= i < len(party):
                m = party[i]
                act = (b.turn_phase == "player" and m.alive and party[b.actor_index % len(party)] is m)
                return msbf_px_member_point(m.id, i, len(party), getattr(m, "row", "front"), "chest", act)
        except Exception:
            pass
        x, y = msbf_px_slot(i, n)
        return (int(x), int(y - 110))

    def msbf_boss_anchor(phase):
        """Where FX aimed at the boss should land -- her pixel sprite's core."""
        return msbf_px_boss_point(phase, "core")

    # Her staging box, re-derived from the pixel sprite so the cinematics and
    # anything else that reads msbf_boss_stage agree with what is on screen.
    def _msbf_px_stage_box(phase):
        meta = msbf_px_boss_meta(phase)
        if not meta:
            return None
        sc = meta["scale"]
        bx0, by0, bx1, by1 = meta["bbox"]
        cx, cy = msbf_px_boss_point(phase, "core")
        fx, fy = msbf_px_boss_point(phase, "foot")
        w = int((bx1 - bx0 + 1) * sc)
        return {"w": w, "h": int((by1 - by0 + 1) * sc), "cx": cx, "cy": cy,
                "foot": fy + MSBF_PX_BOSS_HOVER.get(phase, 30),
                "shadow_w": int(w * (0.45 if phase == 1 else 0.55)),
                "shadow_a": 0.55, "airborne": True}

    for _msbf_ph in (1, 2, 3):
        _msbf_box = _msbf_px_stage_box(_msbf_ph)
        if _msbf_box:
            MSBF_BOSS_STAGE[_msbf_ph] = _msbf_box

    # --- THE ARCHETYPES ------------------------------------------------------
    # The fight has its own cast art now: seven full-body pieces in battle
    # costume, one per roster archetype, in addons/.../archetypes/. Everything
    # that draws a party member here reads THESE and not the VN sprites.
    #
    # Why it matters beyond looking better: the story sprites are school
    # uniforms and casual clothes photographed from the front, so a Spellblade
    # and a Berserker were the same two people in the same hoodie, and the
    # silhouettes had to be crushed hard enough to hide that they were
    # front-facing portraits. These read as their class at silhouette size --
    # the greatsword, the halberd, the witch's hat, the staff -- which is the
    # whole reason to put the party in the world in the first place.
    #
    # Native dimensions are individual. Weapons and action poses determine
    # each canvas; neither stage rendering nor portrait crops distort them.
    MSBF_ARCH_SIZES = {
        "seeker": (1060, 1484), "monika": (1375, 1144),
        "kotonoha": (1024, 1536), "asahina": (1024, 1536),
        "sam": (1024, 1536), "tsubaki": (1024, 1536),
        "himeko": (1024, 1536),
    }

    def msbf_arch_aspect(member_id):
        w, h = MSBF_ARCH_SIZES.get(member_id, (1024, 1536))
        return float(w) / h

    MSBF_SIL_SPRITE = {
        "seeker":   "msbf_arch_seeker",
        "monika":   "msbf_arch_monika",
        "kotonoha": "msbf_arch_kotonoha",
        "asahina":  "msbf_arch_asahina",
        "sam":      "msbf_arch_sam",
        "tsubaki":  "msbf_arch_tsubaki",
        "himeko":   "msbf_arch_himeko",
    }

    # The same seven, uncrushed, for the party-select dossier.
    # (image, source aspect, subject scale, vertical focus).
    MSBF_ROSTER_PORTRAIT = dict(
        (member_id, (image_name, msbf_arch_aspect(member_id), 1.0, 0.0))
        for member_id, image_name in MSBF_SIL_SPRITE.items()
    )

    # Per-character head framing for the chamber mug: (scale, yfocus, xfocus).
    # A mug CANNOT reuse the dossier's subject scale -- a cover fit of a 2:3
    # source into a square still shows two thirds of a whole standing figure,
    # which makes the "mug shot" a picture of somebody's waist.
    #
    # XFOCUS IS THE ONE THAT IS NOT OBVIOUS. At this crop the mug shows about
    # 42% of the source's width, and these figures are not centred inside their
    # own art: Sam is shifted left under a raised axe, Seeker stands right of
    # centre with his sword out to the side. Cropping dead centre put Sam's head
    # in the corner of his chamber and left half of it empty. Values are solved
    # from measured head positions rather than nudged -- see the note below.
    #
    #   yfocus = (head_y - band_h/2) / (1 - band_h)
    #   xfocus = (head_x - band_w/2) / (1 - band_w)
    #
    # ...where head_x/head_y are the head's centre as a fraction of the source
    # and band_w/band_h are what the crop shows (0.417 x 0.277 at scale 2.4).
    # A zero yfocus means the head already sits above the band's centre with the
    # crop pinned to the top of the frame, which is true for most of the cast.
    MSBF_ROSTER_HEADS = {
        "seeker": (0.622, 0.150, 3.00), "monika": (0.378, 0.195, 2.75),
        "kotonoha": (0.474, 0.180, 3.00), "asahina": (0.537, 0.157, 3.00),
        "sam": (0.455, 0.153, 3.00), "tsubaki": (0.574, 0.221, 3.00),
        "himeko": (0.532, 0.104, 3.00),
    }

    def msbf_arch_mug_frame(member_id):
        hx, hy, scale = MSBF_ROSTER_HEADS[member_id]
        band_h = 1.0 / (1.5 * scale)
        band_w = band_h / msbf_arch_aspect(member_id)
        clamp = lambda value: min(1.0, max(0.0, value))
        return (scale, clamp((hy - band_h * 0.5) / (1.0 - band_h)),
                clamp((hx - band_w * 0.5) / (1.0 - band_w)))

    MSBF_ROSTER_MUG = {member_id: msbf_arch_mug_frame(member_id) for member_id in MSBF_ROSTER_HEADS}

    def msbf_roster_portrait(member_id):
        """-> (image, aspect, scale, focus) or None if we have no art."""
        meta = MSBF_ROSTER_PORTRAIT.get(member_id)
        if not meta:
            return None
        try:
            if not renpy.has_image(meta[0], exact=False):
                return None
        except Exception:
            return None
        return meta

    def msbf_roster_mug(member_id):
        """Framed as a head shot -> (image, aspect, scale, yfocus, xfocus)."""
        meta = msbf_roster_portrait(member_id)
        if meta is None:
            return None
        mug = MSBF_ROSTER_MUG.get(member_id, (2.40, 0.0, 0.5))
        return (meta[0], meta[1], meta[2] * mug[0], mug[1], mug[2])

    def msbf_sil_image(member_id):
        """The silhouette source for a roster id, or None if we have no art.

        NOT exact=True. Monika's entry is a layeredimage tag plus nine
        attributes, which is a perfectly displayable name and is not a
        registered image, so an exact check rejected it and she was the one
        party member who silently never appeared on the deck.
        """
        name = MSBF_SIL_SPRITE.get(member_id)
        if not name:
            return None
        try:
            if not renpy.has_image(name, exact=False):
                return None
        except Exception:
            return None
        return name

    # --- Poll the battle for the room's intensities ---------------------------
    # The arena takes five 0..1 numbers and nothing else. Keeping the mapping
    # in ONE function is what stops the room's reactions drifting out of step
    # with the fight the way the old per-panel FX flags did.
    # --- HOW HARD DOES THIS LAND? -------------------------------------------
    # ONE table, and every combat event is in it. This replaced a membership
    # tuple (does this event shake the screen: yes/no) plus a separate one-line
    # ternary for strength, and between them they were the whole reason the
    # fight's impact felt arbitrary: a player weakness hit shook at 1.6 while
    # the boss hitting YOUR weakness shook at 1.0, and a resist, a miss, a
    # guard and a shuffle were simply not in the tuple, so they landed with no
    # weight at all. Whether an action had punch depended on whether somebody
    # had remembered to list it.
    #
    # Now the weight IS the hierarchy, it reads top to bottom, and it drives
    # every consumer -- camera punch, floor shockwave, and the reaction on
    # whoever got hit -- so those three can never disagree about how big a
    # moment this is. 0.0 means "no impact", which is a decision, not an
    # omission. Anything unlisted defaults to 0.0 and is therefore visible as
    # missing the moment somebody adds a new event.
    MSBF_IMPACT_WEIGHT = {
        # the two bar breaks and the two finales -- the loudest things there are
        "phase": 2.00,
        "final_victory": 2.00,
        "final_defeat": 2.00,
        # landing a weakness or a crit is the whole point of the press-turn
        # system, so it hits hardest of the ordinary actions -- and it hits
        # exactly as hard when SHE does it to you.
        "crit": 1.70,
        "enemy_crit": 1.70,
        "weak": 1.45,
        "enemy_weak": 1.45,
        "enemy_aoe": 1.25,
        # a clean ordinary hit is the unit everything else is measured against
        "hit": 1.00,
        "enemy_hit": 1.00,
        "enemy": 0.85,
        # glancing outcomes: felt, but as a thud rather than a blow
        "shuffle": 0.60,
        "resist": 0.55,
        "enemy_resist": 0.55,
        "enemy_guard": 0.45,
        "enemy_buff": 0.45,
        "miss": 0.30,
    }

    def msbf_impact_weight(fx_event):
        """How hard `fx_event` lands, 0.0 = not an impact at all."""
        return MSBF_IMPACT_WEIGHT.get(fx_event, 0.0)

    def msbf_arena_uniforms(battle):
        """-> (phase_float, charge, danger, break_, glitch) for msbf_arena()."""
        phase = getattr(battle, "phase", 1)
        try:
            phase = float(min(3, max(1, int(phase))))
        except (TypeError, ValueError):
            phase = 1.0

        fx = getattr(battle, "fx_event", None)

        # Charge: she is winding something up, or the party is committing.
        charge = 0.0
        if fx in ("enemy", "enemy_buff", "enemy_guard", "shuffle"):
            charge = 0.85
        elif getattr(battle, "enemy_phase_active", False):
            charge = 0.30

        # Danger: the current bar is nearly gone.
        try:
            danger = 1.0 - min(1.0, getattr(battle.boss, "hp_ratio", 1.0) / 0.28)
        except Exception:
            danger = 0.0
        danger = max(0.0, min(1.0, danger))

        # Break: the bar-break / victory cinematics own the room outright.
        # Only the BLOWOUT frame gets a big lift. The reveal that follows is
        # lit by its own shaft, so the room stays dark under it and the shaft
        # has something to read against.
        break_ = 0.0
        if getattr(battle, "phase_transition_active", False):
            break_ = 0.12
        if fx == "phase_blackout":
            break_ = 0.85

        # Glitch: phase 3 is always coming apart; the microgames push it.
        glitch = 0.0
        if phase >= 3.0:
            glitch = 0.45
            if getattr(battle, "microgame_active", False):
                glitch = 0.80
        elif getattr(battle, "id_mode", False):
            glitch = 0.12

        return (phase, charge, danger, break_, glitch)

# --- THE PARTY'S BATTLE ART --------------------------------------------------
# One per roster archetype. Declared as images (rather than referenced as raw
# paths) so renpy.has_image can gate on them the way msbf_sil_image expects,
# and so lint accounts for them.
image msbf_arch_seeker = "addons/Matsuda's Sick Boss Fight/archetypes/v2/seeker.png"
image msbf_arch_monika = "addons/Matsuda's Sick Boss Fight/archetypes/v2/monika.png"
image msbf_arch_kotonoha = "addons/Matsuda's Sick Boss Fight/archetypes/v2/kotonoha.png"
image msbf_arch_asahina = "addons/Matsuda's Sick Boss Fight/archetypes/v2/asahina.png"
image msbf_arch_sam = "addons/Matsuda's Sick Boss Fight/archetypes/v2/sam.png"
image msbf_arch_tsubaki = "addons/Matsuda's Sick Boss Fight/archetypes/v2/tsubaki.png"
image msbf_arch_himeko = "addons/Matsuda's Sick Boss Fight/archetypes/v2/himeko.png"


# -----------------------------------------------------------------------------
# 3. TRANSFORMS
# -----------------------------------------------------------------------------

transform msbf_shadow_t(strength=0.7, soft=1.5):
    mesh True
    shader "msbf.shadow"
    u_sh_strength strength
    u_sh_soft soft

# A hovering caster's shadow breathes with them rather than sitting rigid.
transform msbf_shadow_hover(strength=0.45, soft=1.9):
    mesh True
    shader "msbf.shadow"
    u_sh_soft soft
    u_sh_strength strength
    subpixel True
    block:
        easein 2.6 u_sh_strength strength * 0.72 zoom 0.94
        easeout 2.6 u_sh_strength strength zoom 1.0
        repeat

transform msbf_scrim_t(col=(0.01, 0.02, 0.04), alpha=0.9, dirn=0.0, bias=2.0, xdir=0.0):
    mesh True
    shader "msbf.scrim"
    u_sc_col col
    u_sc_alpha alpha
    u_sc_dir dirn
    u_sc_xdir xdir
    u_sc_bias bias


# -----------------------------------------------------------------------------
# 4. SCREENS
# -----------------------------------------------------------------------------

# The room. One draw, full frame, behind everything.
screen msbf_arena(battle, shock=False, amp=1.0):
    $ _ar_ph, _ar_chg, _ar_dgr, _ar_brk, _ar_glt = msbf_arena_uniforms(battle)
    use msbf_seer_environment(_ar_ph, getattr(battle, "id_mode", False), _ar_chg, _ar_dgr, shock, amp)


screen msbf_arena_static(phase=1, dim=0.40):
    use msbf_seer_environment(phase, getattr(store, "_msbf_id_mode", False))
    add Solid("#02060c") xysize (1280, 720):
        alpha dim


# A soft ellipse of shadow on the deck. w is the ellipse's screen width; the
# height comes from the floor angle, so it is always the same squash as the
# grid it is lying on.
screen msbf_ground_shadow(cx, foot_y, w, strength=0.7, hover=False):
    $ _sh_h = max(10, int(w * 0.26))
    if MSBF_ARENA_SHADERS:
        if hover:
            add Solid("#00000000") at msbf_t(msbf_shadow_hover, strength, 2.1):
                xcenter int(cx)
                ycenter int(foot_y)
                xysize (int(w), _sh_h)
        else:
            add Solid("#00000000") at msbf_t(msbf_shadow_t, strength, 1.5):
                xcenter int(cx)
                ycenter int(foot_y)
                xysize (int(w), _sh_h)


# -----------------------------------------------------------------------------
# 5. THE BOSS'S MOTION + GHOSTING
# -----------------------------------------------------------------------------
# Each of these is ONE draw. The screen used to stack the full-size sprite two
# to four times (a base, one or two afterimages, and in phase 3 a chromatic
# ghost on top) to get a trailing look, which meant redrawing an 880px sprite
# up to four times every frame for a purely cosmetic read. msbf.smear does the
# trail and the channel split inside the single pass, so the same look costs a
# quarter as much -- and it can smear along an arbitrary direction, which the
# stacked-copy version could only fake with hand-placed offsets.
#
# They are looked up as SHARED objects (see MSBF_BOSS_TF below) rather than
# rebuilt per redraw: a transform that is a new object every screen execution
# restarts its ATL every time the fight's state changes, which turns the idle
# float into a stutter. Swapping between them on an fx_event does restart the
# ATL, but that is exactly when a restart is wanted.

# --- THE THREE IDLES ---------------------------------------------------------
# One per form, and they are the character work: the same sprite bouncing on a
# single sine says nothing about what it IS, and that is exactly what the old
# shared idle did for all three bars.
#
# ONE RULE MAKES THESE WORK: inside a transform, each `parallel` block owns a
# DISJOINT set of properties. Two blocks animating yoffset do not blend, they
# fight -- last writer per frame wins and the motion stutters. So the channels
# below are split strictly: breath owns yoffset+zoom, sway owns xoffset, and
# tilt owns rotate. Anything a channel needs to do, it does inside its channel.
#
# The second thing that makes them read as alive is that the channels run on
# lengths that do not divide into each other (1.9+0.28+2.2 against 3.1 against
# 5.4/7.1). They drift out of phase and the idle never visibly repeats.

# PHASE 1 -- the Nahobino. Still a person in there, so this is a fighter's idle
# and not a float: she carries her weight, settles hip to hip, and resets her
# stance every few seconds with one small sharp adjustment a breathing loop
# could never produce on its own.
transform msbf_boss_hover_a:
    mesh True
    shader "msbf.smear"
    u_sm_dir (1.0, 0.30)
    u_sm_amount 0.65
    u_sm_split 0.0
    u_sm_ghost 0.30
    subpixel True
    parallel:
        block:
            easein 1.9 yoffset -9 zoom 1.007
            pause 0.28
            easeout 2.2 yoffset 2 zoom 0.998
            repeat
    parallel:
        block:
            easein 3.1 xoffset 7
            easeout 3.1 xoffset -7
            repeat
    parallel:
        block:
            easein 2.6 rotate 0.5
            easeout 2.6 rotate -0.5
            pause 0.9
            # the stance reset
            easeout 0.13 rotate 1.4
            easein 0.46 rotate 0.0
            pause 3.8
            easeout 0.11 rotate -1.2
            easein 0.42 rotate 0.0
            repeat

# PHASE 2 -- the angel. Serene on the surface: a very long, very wide float
# with almost no lateral motion at all, so she reads as HELD in the air rather
# than swimming through it. The intensity is underneath, in the zoom channel --
# a slow double-beat, like something enormous with a pulse, that never once
# breaks the calm of the float above it.
transform msbf_boss_hover_b:
    mesh True
    shader "msbf.smear"
    u_sm_dir (0.0, 0.55)
    u_sm_amount 0.42
    u_sm_split 0.0
    u_sm_ghost 0.34
    subpixel True
    parallel:
        block:
            easein 4.6 yoffset -22
            easeout 4.6 yoffset 0
            repeat
    parallel:
        block:
            # the pulse: two beats, then a long rest. Deliberately shallow --
            # at any real amplitude it stops reading as composure.
            pause 1.1
            easeout 0.22 zoom 1.013
            easein 0.62 zoom 1.0
            pause 0.24
            easeout 0.20 zoom 1.009
            easein 0.70 zoom 1.0
            pause 2.9
            repeat
    parallel:
        block:
            # a barely-there roll, long enough that you never catch it turning
            easein 7.3 rotate 0.9
            easeout 7.3 rotate -0.9
            repeat
    parallel:
        block:
            easein 5.9 xoffset 4
            easeout 5.9 xoffset -4
            repeat

# PHASE 3 -- Id Mode. The body will not hold its own shape. Nothing here eases
# into anything: every move is a hard cut to a new offset and a hold, so the
# form reads as being RE-DRAWN wrong rather than as moving. The one slow
# channel is a sagging drift that the snaps keep yanking her back out of, which
# is what stops it looking like a simple vibration.
transform msbf_boss_hover_c:
    mesh True
    shader "msbf.smear"
    u_sm_dir (1.0, 0.22)
    u_sm_amount 0.42
    u_sm_ghost 0.28
    u_sm_split 0.8
    subpixel True
    parallel:
        block:
            # vertical: a slow sink, punctuated by hard rupture-jerks upward
            easein 2.4 yoffset 14
            pause 0.06
            linear 0.03 yoffset -18
            pause 0.10
            linear 0.02 yoffset -4
            pause 0.34
            easein 1.1 yoffset 9
            linear 0.03 yoffset -13
            pause 0.22
            linear 0.02 yoffset 0
            pause 0.7
            repeat
    parallel:
        block:
            # lateral: irregular hard steps, never centred for long
            linear 0.02 xoffset 9
            pause 0.19
            linear 0.02 xoffset -13
            pause 0.11
            linear 0.02 xoffset 4
            pause 0.42
            linear 0.02 xoffset -6
            pause 0.14
            linear 0.02 xoffset 15
            pause 0.08
            linear 0.02 xoffset 0
            pause 0.61
            repeat
    parallel:
        block:
            # the form losing its footing entirely, twice a cycle
            pause 1.3
            linear 0.03 rotate -2.6
            pause 0.09
            linear 0.03 rotate 1.9
            easein 0.5 rotate 0.0
            pause 2.2
            linear 0.02 rotate 3.1
            pause 0.06
            linear 0.03 rotate -1.4
            easein 0.6 rotate 0.0
            pause 1.6
            repeat
    parallel:
        block:
            # scale stutter -- the silhouette itself refusing to settle
            pause 0.8
            linear 0.02 zoom 1.028
            pause 0.05
            linear 0.02 zoom 0.984
            pause 0.04
            linear 0.03 zoom 1.0
            pause 1.9
            linear 0.02 zoom 0.972
            pause 0.07
            linear 0.02 zoom 1.021
            pause 0.04
            linear 0.03 zoom 1.0
            pause 2.6
            repeat
    parallel:
        block:
            easein 0.10 u_sm_split 3.0
            easeout 0.34 u_sm_split 0.8
            pause 0.8
            easein 0.06 u_sm_split 2.0
            easeout 0.40 u_sm_split 0.8
            pause 1.2
            repeat

transform msbf_boss_recoil_a:
    mesh True
    shader "msbf.smear"
    u_sm_dir (1.0, 0.0)
    u_sm_split 0.0
    u_sm_ghost 0.70
    u_sm_amount 1.40
    subpixel True
    parallel:
        easeout 0.05 xoffset 26 zoom 1.030
        easeout 0.10 xoffset -14 zoom 0.992
        easeout 0.12 xoffset 6 zoom 1.006
        easeout 0.16 xoffset 0 zoom 1.0
    parallel:
        easeout 0.44 u_sm_amount 0.0

transform msbf_boss_recoil_b:
    mesh True
    shader "msbf.smear"
    u_sm_dir (1.0, 0.0)
    u_sm_ghost 0.70
    u_sm_split 4.0
    u_sm_amount 1.70
    subpixel True
    parallel:
        easeout 0.05 xoffset 34 zoom 1.036
        easeout 0.10 xoffset -19 zoom 0.990
        easeout 0.12 xoffset 8 zoom 1.008
        easeout 0.16 xoffset 0 zoom 1.0
    parallel:
        easeout 0.50 u_sm_amount 0.0
    parallel:
        easeout 0.50 u_sm_split 1.2

# Her wind-up: she gathers, rises, and the trail runs UPWARD -- the opposite
# axis to a recoil, so a cast never reads as her being hit.
transform msbf_boss_cast_a:
    mesh True
    shader "msbf.smear"
    u_sm_dir (0.0, 1.0)
    u_sm_split 0.0
    u_sm_ghost 0.85
    u_sm_amount 1.10
    subpixel True
    parallel:
        easein 0.16 yoffset -30 zoom 1.045
        easeout 0.40 yoffset 0 zoom 1.0
    parallel:
        easeout 0.56 u_sm_amount 0.4

transform msbf_boss_cast_b:
    mesh True
    shader "msbf.smear"
    u_sm_dir (0.0, 1.0)
    u_sm_ghost 0.90
    u_sm_split 5.0
    u_sm_amount 1.40
    subpixel True
    parallel:
        easein 0.14 yoffset -38 zoom 1.055
        easeout 0.40 yoffset 0 zoom 1.0
    parallel:
        easeout 0.60 u_sm_amount 0.8
    parallel:
        easeout 0.60 u_sm_split 1.2

# A bar break: she is thrown, hard, and the smear runs both ways.
transform msbf_boss_break_a:
    mesh True
    shader "msbf.smear"
    u_sm_dir (1.0, -0.55)
    u_sm_split 0.0
    u_sm_ghost 0.80
    u_sm_amount 2.20
    subpixel True
    parallel:
        easeout 0.10 xoffset 48 yoffset -20 zoom 1.06
        easeout 0.18 xoffset -26 yoffset 10 zoom 0.98
        easeout 0.22 xoffset 10 yoffset -4 zoom 1.01
        easeout 0.30 xoffset 0 yoffset 0 zoom 1.0
    parallel:
        easeout 0.80 u_sm_amount 0.0

transform msbf_boss_break_b:
    mesh True
    shader "msbf.smear"
    u_sm_dir (1.0, -0.55)
    u_sm_ghost 0.80
    u_sm_split 5.0
    u_sm_amount 2.60
    subpixel True
    parallel:
        easeout 0.10 xoffset 58 yoffset -24 zoom 1.07
        easeout 0.18 xoffset -32 yoffset 12 zoom 0.975
        easeout 0.22 xoffset 12 yoffset -5 zoom 1.012
        easeout 0.30 xoffset 0 yoffset 0 zoom 1.0
    parallel:
        easeout 0.90 u_sm_amount 0.0
    parallel:
        easeout 0.90 u_sm_split 1.2


# --- THE CAMERA -------------------------------------------------------------
# One rig the whole world hangs off (arena + boss + shadow + reflection +
# silhouettes) so nothing can drift out of register with the room.
#
# The rig only ever zooms IN. An xoffset on a child that exactly fills the
# frame would otherwise drag a black edge in from one side, so every keyframe
# below keeps zoom high enough that the crop margin (640 * (zoom - 1) px per
# side) still exceeds that frame's offset.
transform msbf_cam_rest:
    subpixel True
    zoom 1.0
    xoffset 0
    yoffset 0

transform msbf_cam_punch(strength=1.0, token=0):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 640
    ypos 360
    zoom 1.0 + 0.034 * strength
    xoffset 0
    yoffset 0
    easeout 0.09 zoom 1.0 + 0.026 * strength xoffset int(11 * strength) * (1 if (token % 2) else -1) yoffset int(-5 * strength)
    easeout 0.08 zoom 1.0 + 0.018 * strength xoffset int(-8 * strength) * (1 if (token % 2) else -1) yoffset int(4 * strength)
    easeout 0.10 zoom 1.0 + 0.010 * strength xoffset int(5 * strength) * (1 if (token % 2) else -1) yoffset int(-2 * strength)
    easeout 0.22 zoom 1.0 xoffset 0 yoffset 0

# --- The two finales shake the ROOM ------------------------------------------
# msbf_final_victory_rumble / msbf_defeat_rumble used to be applied to each of
# the three HUD panels, so a party wipe concussed the furniture and left the
# fight behind it perfectly still. There is no furniture now, so the same
# profiles drive the camera and the whole world moves -- which is what they
# were always describing.
#
# They are re-stated here rather than reused because the originals carry no
# zoom, and a bare 24px offset on a child that exactly fills the frame drags a
# black edge in from one side. The zoom hold below is sized to the largest
# offset in each profile (640 * (zoom - 1) must exceed it).
transform msbf_cam_victory:
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 640
    ypos 360
    zoom 1.062
    xoffset 0
    yoffset 0
    # building tremor (0 -> ~0.63)
    linear 0.05 xoffset -1 yoffset 1
    linear 0.05 xoffset 1 yoffset -1
    linear 0.05 xoffset -2 yoffset 1
    linear 0.05 xoffset 2 yoffset -2
    linear 0.045 xoffset -3 yoffset 2
    linear 0.045 xoffset 3 yoffset -2
    linear 0.04 xoffset -4 yoffset 3
    linear 0.04 xoffset 4 yoffset -3
    linear 0.04 xoffset -5 yoffset 3
    linear 0.04 xoffset 5 yoffset -4
    linear 0.035 xoffset -7 yoffset 4
    linear 0.035 xoffset 7 yoffset -5
    linear 0.03 xoffset -8 yoffset 5
    linear 0.03 xoffset 8 yoffset -6
    # implosion suck-in: snap still, and the camera leans in with it
    easeout 0.16 xoffset 0 yoffset 0 zoom 1.085
    # DETONATION slam + decaying aftershock
    linear 0.02 xoffset -24 yoffset 15
    linear 0.02 xoffset 21 yoffset -17
    linear 0.025 xoffset -19 yoffset 12
    linear 0.025 xoffset 16 yoffset -10
    linear 0.03 xoffset -12 yoffset 8
    linear 0.03 xoffset 10 yoffset -6
    linear 0.04 xoffset -7 yoffset 4
    linear 0.04 xoffset 5 yoffset -3
    linear 0.05 xoffset -3 yoffset 2
    easeout 0.30 xoffset 0 yoffset 0 zoom 1.062

transform msbf_cam_defeat:
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 640
    ypos 360
    zoom 1.040
    xoffset 0
    yoffset 0
    linear 0.03 xoffset -11 yoffset 6
    linear 0.03 xoffset 10 yoffset -5
    linear 0.04 xoffset -8 yoffset 5
    linear 0.04 xoffset 7 yoffset -3
    linear 0.06 xoffset -5 yoffset 3
    linear 0.06 xoffset 4 yoffset -2
    linear 0.09 xoffset -2 yoffset 1
    easeout 0.5 xoffset 0 yoffset 0


# --- Which motion the boss is in ---------------------------------------------
# Built once, at init 1, so every lookup hands back the SAME transform object.
# See the note above msbf_boss_hover_a for why that matters.
init 1 python:

    # Keyed by (kind, PHASE) rather than (kind, is-phase-3). The idle is the one
    # place all three forms genuinely differ -- Nahobino, angel, and whatever Id
    # Mode is -- so phases 1 and 2 can no longer share a row. The reaction
    # animations still only split corrupt/not, so those repeat across 1 and 2.
    #
    # The two finale beats keep their own bespoke animations and are NOT given a
    # smear: msbf_boss_collapse's timing is matched frame-for-frame to the
    # hypernova overlay, and both want her crisp, not trailing.
    MSBF_BOSS_TF = {
        ("hover", 1):  msbf_boss_hover_a,
        ("hover", 2):  msbf_boss_hover_b,
        ("hover", 3):  msbf_boss_hover_c,
        ("recoil", 1): msbf_boss_recoil_a,
        ("recoil", 2): msbf_boss_recoil_a,
        ("recoil", 3): msbf_boss_recoil_b,
        ("cast", 1):   msbf_boss_cast_a,
        ("cast", 2):   msbf_boss_cast_a,
        ("cast", 3):   msbf_boss_cast_b,
        ("break", 1):  msbf_boss_break_a,
        ("break", 2):  msbf_boss_break_a,
        ("break", 3):  msbf_boss_break_b,
        ("collapse", 1): msbf_boss_collapse,
        ("collapse", 2): msbf_boss_collapse,
        ("collapse", 3): msbf_boss_collapse,
        ("loom", 1):     msbf_boss_loom,
        ("loom", 2):     msbf_boss_loom,
        ("loom", 3):     msbf_boss_loom,
    }

    MSBF_BOSS_RECOIL_EVENTS = ("hit", "weak", "crit")
    MSBF_BOSS_CAST_EVENTS = ("enemy", "enemy_hit", "enemy_aoe", "enemy_buff", "enemy_guard", "enemy_weak", "enemy_crit", "enemy_resist", "shuffle", "resist")
    MSBF_BOSS_BREAK_EVENTS = ("phase",)

    def msbf_boss_smear_for(battle):
        """The boss's current motion -- a shared transform, never a new one."""
        fx = getattr(battle, "fx_event", None)
        try:
            phase = min(3, max(1, int(getattr(battle, "phase", 1))))
        except (TypeError, ValueError):
            phase = 1
        if fx == "final_victory":
            kind = "collapse"
        elif fx == "final_defeat":
            kind = "loom"
        elif fx in MSBF_BOSS_BREAK_EVENTS:
            kind = "break"
        elif fx in MSBF_BOSS_RECOIL_EVENTS:
            kind = "recoil"
        elif fx in MSBF_BOSS_CAST_EVENTS:
            kind = "cast"
        else:
            kind = "hover"
        return MSBF_BOSS_TF[(kind, phase)]


# -----------------------------------------------------------------------------
# 6. HUD PIECES THAT BELONG TO THE ROOM
# -----------------------------------------------------------------------------

# A gradient wash under a readout. The old HUD sat on stacked Solid() rectangles
# and every one of them showed its own top edge as a visible band across the
# art; this reaches zero, so text lies ON the room instead of on a plate over it.
screen msbf_hud_scrim(x, y, w, h, dirn=0.0, bias=1.5, xdir=0.0, alpha=0.86):
    if MSBF_ARENA_SHADERS:
        # msbf_t: reused across executions instead of rebuilt (seer_battle.rpy).
        add Solid("#00000000") at msbf_t(msbf_scrim_t, (0.006, 0.013, 0.026), alpha, dirn, bias, xdir):
            xpos int(x)
            ypos int(y)
            xysize (int(w), int(h))
    else:
        add Solid("#03080fbb"):
            xpos int(x)
            ypos int(y)
            xysize (int(w), int(h))


# -----------------------------------------------------------------------------
# 7. THE TURNOVER
# -----------------------------------------------------------------------------
# The beat where the tempo changes hands. It exists because the fight used to
# swap sides on the same frame that resolved the final action of a phase: the
# hit landed, and the enemy banner plus the entire HUD swap arrived on top of
# it, cutting the impact off with its own consequence.
#
# MSBFBattleState.handover_active now holds the frame for ~0.95s first. This is
# what fills it -- a band travelling in the direction the tempo is going. Up the
# deck toward her when she seizes it, back down toward the party when they take
# it. Direction is the whole idea: a symmetrical flash would say "something
# changed", and the one thing worth saying here is WHO IT WENT TO.

transform msbf_turnover_hband(to_right=True, delay=0.0):
    subpixel True
    ycenter 360
    xcenter (-500 if to_right else 1780)
    alpha 0.0
    pause delay
    alpha 1.0
    easeout 0.46 xcenter (1780 if to_right else -500)
    alpha 0.0

transform msbf_turnover_wash(col="#ff3868"):
    alpha 0.0
    easeout 0.10 alpha 0.20
    easein 0.55 alpha 0.0

# A hard rule that snaps across at the moment of the change.
transform msbf_turnover_rule(up=True):
    subpixel True
    xsize 0
    xcenter 640
    ycenter (392 if up else 392)
    alpha 0.0
    pause 0.14
    alpha 1.0
    easeout 0.20 xsize 1400
    pause 0.18
    easein 0.24 alpha 0.0

screen msbf_turnover_sweep(to_side="enemy", phase=1, round_number=1, boss_name="", serial=0, mp_restored=False):
    # THE HANDOVER'S SOUND LIVES HERE, not in begin_handover. This screen only
    # exists once fx_event has cleared, so it is the first moment that is
    # genuinely "the tempo is changing" rather than "the last action is still
    # playing". Raised in begin_handover instead, the cue fired on the same
    # frame as whatever ended the phase -- stepping on that action's own sound,
    # and going off early any time the phase ended on an affinity shuffle.
    timer 0.01 action Function(msbf_play_pooled_sfx, MSBF_SFX["turn"], _update_screens=False)

    # The party catching its breath is a handover event too. It used to raise
    # its own set_fx at the end of the player phase, which overwrote the last
    # action's cue and cancelled its whole impact -- see _restore_party_mp.
    # Offset well clear of the tempo cue so the two do not stack. Sound only:
    # the flash it used to draw was a 0.16-alpha wash that nothing could see
    # against the sweep already crossing the screen behind it.
    if mp_restored:
        timer 0.42 action Function(msbf_play_pooled_sfx, MSBF_SFX["recover"], _update_screens=False)

    $ _to_boss = (to_side == "enemy")
    $ _tv_col = "#ff3868" if _to_boss else msbf_phase_accent(phase)[0]
    $ _tv_rgb = msbf_hex_rgb(_tv_col)

    add Solid(_tv_col) at msbf_t(msbf_turnover_wash, _tv_col)

    # Kept translucent on purpose: the handover is a beat, not a curtain, and
    # the fight underneath has to stay legible through it. Since the Sep 30
    # facelift the two sides face each other across the frame, so the beat
    # travels SIDEWAYS: rightward toward her when she seizes the tempo,
    # leftward back to the party when they take it.
    add msbf_plate(520, 760, 160, _pl_rgba(_tv_col, 0.42), _pl_rgba(_tv_col, 0.18), _pl_rgba("#ffffff", 0.0)) at msbf_t(msbf_turnover_hband, _to_boss, 0.00)
    add msbf_plate(120, 760, 160, (1.0, 1.0, 1.0, 0.30), (1.0, 1.0, 1.0, 0.10), _pl_rgba("#ffffff", 0.0)) at msbf_t(msbf_turnover_hband, _to_boss, 0.07)
    add msbf_plate(760, 760, 160, _pl_rgba(_tv_col, 0.20), _pl_rgba(_tv_col, 0.06), _pl_rgba("#ffffff", 0.0)) at msbf_t(msbf_turnover_hband, _to_boss, 0.13)

    add Solid("#ffffff") xysize (1400, 3) at msbf_t(msbf_turnover_rule, _to_boss)

    # The side receiving the tempo gets lit from the direction it is arriving.
    if MSBF_FX_SHADERS:
        if _to_boss:
            $ _tv_x, _tv_y = msbf_boss_anchor(phase)
            add Solid("#00000000") xysize (900, 700) at msbf_t(msbf_fx_glow_pop, _tv_rgb, 0.75, 1.5, 0.72):
                xcenter _tv_x
                ycenter _tv_y
        else:
            add Solid("#00000000") xysize (760, 600) at msbf_t(msbf_fx_glow_pop, _tv_rgb, 0.62, 1.7, 0.72):
                xcenter 310
                ycenter 430

    # THE TEMPO CARD, drawn HERE rather than by the battle screen. It is part of
    # the same beat as the sweep, so it has to share the beat's lifetime -- kept
    # separate it ran on its own timer and was still on screen after the next
    # side had begun acting, and it fired twice on a handover to the party
    # (once for the handover, once more when start_player_turn bumped the round
    # number and changed the token underneath it).
    if _to_boss:
        $ _tv_label = boss_name.upper()
        $ _tv_accent2 = "#a66bff" if phase == 3 else "#ffcf66"
        use msbf_turn_banner("H%d" % serial, _tv_label, "#ff3868", _tv_accent2, "SEIZES THE TEMPO", "ENEMY TURN")
    else:
        # NOT the palette's secondary: the party card deliberately holds red
        # until phase 3 rather than stepping cyan -> gold -> red.
        $ _tv_accent2 = "#a66bff" if phase == 3 else "#ff3868"
        $ _tv_sub = "ROUND %d" % (round_number + 1)
        use msbf_turn_banner("H%d" % serial, "PARTY TURN", msbf_phase_accent(phase)[0], _tv_accent2, _tv_sub, "YOUR MOVE")
