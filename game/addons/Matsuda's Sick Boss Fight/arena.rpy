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
# THE PROJECTION (the whole trick, in three lines)
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
#   Above the horizon the shader samples tex0 -- the phase's sky plate (the
#   cosmic void of bg battle_setpiece, or the rupture plate in phase 3) -- and
#   parallaxes it against the camera. So the art is still doing work; it is
#   just doing it as a SKY instead of as a wall behind a cutout.
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

    # --- The one set of numbers the room and everything standing in it share.
    #     Change the horizon here and the floor, ceiling, sigil, shadows and
    #     reflections all move together, because they are all derived from it.
    MSBF_ARENA_HORIZON = 0.5611          # uv y of the vanishing point (~404px)
    MSBF_ARENA_HORIZON_PX = int(720 * MSBF_ARENA_HORIZON)
    MSBF_ARENA_KF = 0.32                 # must match AR_KF in the shader
    MSBF_ARENA_SPREAD = 2.2              # must match AR_SPREAD in the shader

    def msbf_arena_depth_at(y_px):
        """Screen y (px) -> floor depth z. Above the horizon returns None."""
        below = (float(y_px) / 720.0) - MSBF_ARENA_HORIZON
        if below <= 0.0008:
            return None
        return MSBF_ARENA_KF / below

    def msbf_arena_floor_y(z):
        """Floor depth z -> screen y (px). The inverse of the above."""
        if z <= 0.0:
            return 720
        return int(720.0 * (MSBF_ARENA_HORIZON + (MSBF_ARENA_KF / float(z))))

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

    def msbf_arena_bossz(phase):
        """Floor depth of the boss's contact point -- where the sigil centres.

        Derived from her stage placement rather than stated twice, so moving
        her on screen moves the seal she is standing in without a second edit.
        """
        return msbf_arena_depth_at(msbf_boss_stage(phase)["foot"]) or 2.04

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
            "sky":  "bg battle_setpiece",
            "flow": 0.85,
        },
        # Phase 2: the deck turns to gold and the roof opens. Same room, lit
        # like a cathedral instead of a hangar.
        2: {
            "key":  (1.00, 0.80, 0.38),
            "fog":  (0.100, 0.085, 0.075),
            "deck": (0.062, 0.052, 0.038),
            "sky":  "bg battle_setpiece",
            "flow": 1.15,
        },
        # Phase 3: the room stops agreeing with itself. Red, white and black
        # only -- the palette is doing the "this is not a place any more" work.
        3: {
            "key":  (1.00, 0.24, 0.34),
            "fog":  (0.085, 0.030, 0.045),
            "deck": (0.055, 0.030, 0.038),
            "sky":  "msbf_rupture_sky",
            "flow": 1.85,
        },
    }

    def msbf_arena_cfg(phase):
        try:
            phase = int(phase)
        except (TypeError, ValueError):
            phase = 1
        return MSBF_ARENA_PHASE.get(min(3, max(1, phase)), MSBF_ARENA_PHASE[1])

    # --- WHERE THE PARTY STANDS ----------------------------------------------
    # Placed BY EYE, not by msbf_arena_floor_y. Run honestly, the projection
    # puts a human standing this close at three screen-heights tall; the
    # Persona read wants them cropped at the chest instead. So depth here is
    # sold the way it actually reads -- nearer means bigger, darker and lower --
    # and the formula is left to govern the things the eye can actually check
    # against the grid (the boss, her shadow, the sigil).
    #
    # (x centre, head-top y, height px, alpha, blur) for slots 0..5. The two
    # outer slots are nearest; the inner pair sit back and smaller so the
    # centre of the deck stays clear for the boss and her seal. Heads sit low
    # enough that only head-and-shoulders clear the frame -- any higher and the
    # front-facing source sprites start reading as faces watching the camera
    # instead of as backs watching her.
    # The command deck lands at y 530 and runs to the bottom edge, so a head
    # top much below ~470 leaves nothing of that member on screen at all -- the
    # first pass put the inner pair at 512 and they vanished entirely behind
    # the skill grid. Heads sit high enough that head-and-shoulders always
    # clears the deck, and the pair is spread wide enough to stay out of the
    # boss's silhouette.
    #
    # THE LAYOUT IS A FUNCTION OF PARTY SIZE, not a fixed table. Phase 3 calls
    # _summon_full_roster_for_phase_three and the party becomes all SEVEN
    # members; a six-entry table indexed with `i % len(...)` therefore stacked
    # the seventh member exactly on top of the first. Every count from 1 to 7
    # now has its own row of x centres, and the depth is arced off those.

    def _msbf_arc_slots(xs):
        """x centres -> full slot tuples, with depth arced across the row.

        NEARER = BIGGER AND HIGHER-HEADED. That reads backwards until you
        remember every one of these figures has their feet well below the
        bottom of the frame, so growing them pushes the head UP, not down.
        """
        n = len(xs)
        half = max(1.0, (n - 1) / 2.0)
        out = []
        for i, x in enumerate(xs):
            t = abs(i - (n - 1) / 2.0) / half        # 0 at the centre, 1 at the ends
            out.append((int(x),
                        int(504 - 54 * t),           # head top
                        int(552 + 148 * t),          # height
                        round(0.82 + 0.14 * t, 3),   # alpha
                        round(3.4 - 1.4 * t, 2)))    # blur
        return out

    # Counts 4 and 7 are the ones that actually occur (a chosen deck, and the
    # full roster phase 3 summons). The rest are here so nothing can index off
    # the end. Wherever possible the centre of the deck is left EMPTY so the
    # boss and her seal are never stood in front of; at 5 and 7 there are too
    # many bodies for that and the middle slot takes the hit.
    MSBF_STAGE_LAYOUT = {
        1: _msbf_arc_slots([640]),
        2: _msbf_arc_slots([340, 940]),
        3: _msbf_arc_slots([180, 640, 1100]),
        4: _msbf_arc_slots([120, 372, 908, 1160]),
        5: _msbf_arc_slots([104, 336, 640, 944, 1176]),
        6: _msbf_arc_slots([92, 288, 484, 796, 992, 1188]),
        7: _msbf_arc_slots([82, 268, 454, 640, 826, 1012, 1198]),
    }

    def msbf_stage_layout(n):
        try:
            n = int(n)
        except (TypeError, ValueError):
            n = 4
        return MSBF_STAGE_LAYOUT.get(max(1, min(7, n)), MSBF_STAGE_LAYOUT[4])

    def msbf_stage_slot(i, n=4):
        slots = msbf_stage_layout(n)
        return slots[i % len(slots)]

    # The tag that floats over a member's head, and the point damage lands on.
    # Everything aimed at a party member -- floating numbers, HP-bar chips, KO
    # bursts, a healing bolt -- reads its position from here, so moving a
    # silhouette moves everything attached to them.
    #
    # Five or more members and the tag goes COMPACT: at seven across, a 186px
    # tag is wider than the 186px of room each member has, so they would sit
    # edge to edge in a solid band of readout. The compact tag drops the MP
    # line and the max-HP denominator -- the acting member's full numbers are
    # in the command deck's ACT block anyway, and that is the only member whose
    # exact MP you can spend this turn.
    MSBF_STAGE_TAG_W = 186          # the roomy (<=4 members) tag
    MSBF_STAGE_TAG_H = 46

    def msbf_stage_tag_metrics(n):
        """-> (width, height, bar y-offset) for a party of n."""
        try:
            n = int(n)
        except (TypeError, ValueError):
            n = 4
        if n >= 5:
            return (170, 34, 18)
        return (MSBF_STAGE_TAG_W, MSBF_STAGE_TAG_H, 20)

    def msbf_stage_tag_origin(i, n=4):
        """Top-left of member i's floating tag, in screen px.

        The tags sit on ONE BASELINE even though the silhouettes under them are
        arced in depth. Hanging each tag off its own member's head instead put
        the seven-member row in a chevron -- correct as perspective, and
        genuinely hard to read as a rank of health bars, which is the only job
        the row has. Depth stays in the figures where the eye enjoys it.

        The x is clamped into the frame as well: the outermost slot at a party
        of seven sits close enough to the edge that a centred tag hangs off it.
        """
        slots = msbf_stage_layout(n)
        sx = slots[i % len(slots)][0]
        tw, th, _bar = msbf_stage_tag_metrics(n)
        baseline = min(s[1] for s in slots) - th - 16
        x = int(sx - tw // 2)
        x = max(6, min(x, 1280 - tw - 6))
        return (x, int(baseline))

    def msbf_stage_anchor(i, n=4):
        """Where FX aimed at member i should land -- the centre of their tag."""
        x, y = msbf_stage_tag_origin(i, n)
        tw, th, _bar = msbf_stage_tag_metrics(n)
        return (int(x + tw // 2), int(y + th // 2))

    def msbf_boss_anchor(phase):
        """Where FX aimed at the boss should land -- her sprite's centre."""
        st = msbf_boss_stage(phase)
        return (int(st["cx"]), int(st["cy"]))

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
    # All seven are 1023x1537, so ONE aspect and one set of framing numbers
    # covers the roster; the per-character variance that the VN sprites forced
    # is gone. MSBF_ARCH_ASPECT is that shared ratio.
    MSBF_ARCH_ASPECT = 1023.0 / 1537.0

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
        (member_id, (image_name, MSBF_ARCH_ASPECT, 1.0, 0.0))
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
    MSBF_ROSTER_MUG = {
        "seeker":   (2.40, 0.000, 0.578),
        "monika":   (2.40, 0.045, 0.420),
        "kotonoha": (2.40, 0.000, 0.491),
        "asahina":  (2.40, 0.000, 0.491),
        "sam":      (2.70, 0.067, 0.454),
        "tsubaki":  (2.40, 0.000, 0.445),
        "himeko":   (2.40, 0.000, 0.479),
    }

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

    # Crushing the sprite to a silhouette. Not a plain black fill: a little of
    # the arena's key light is left on them so they catch the room, which is
    # the difference between "party member lit from behind" and "hole".
    def msbf_sil_matrix(key, lift=0.16):
        r, g, b = key
        return (TintMatrix(Color((int(r * 255 * lift), int(g * 255 * lift),
                                    int(b * 255 * lift), 255)))
                * BrightnessMatrix(-0.55)
                * SaturationMatrix(0.0))

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
image msbf_arch_seeker = "addons/Matsuda's Sick Boss Fight/archetypes/mcspellblade.png"
image msbf_arch_monika = "addons/Matsuda's Sick Boss Fight/archetypes/monikamage.png"
image msbf_arch_kotonoha = "addons/Matsuda's Sick Boss Fight/archetypes/kotomage.png"
image msbf_arch_asahina = "addons/Matsuda's Sick Boss Fight/archetypes/asahalberdier.png"
image msbf_arch_sam = "addons/Matsuda's Sick Boss Fight/archetypes/samberserker.png"
image msbf_arch_tsubaki = "addons/Matsuda's Sick Boss Fight/archetypes/tsubakimage.png"
image msbf_arch_himeko = "addons/Matsuda's Sick Boss Fight/archetypes/himekotrickster.png"

# The phase-3 sky. The rupture plate was previously stretched to fill a 786px
# window; out here it is the void itself, so it is fitted to the full frame.
image msbf_rupture_sky = Transform(
    "addons/Matsuda's Sick Boss Fight/idmode/rupture.png",
    fit="cover", xysize=(1280, 720))


# -----------------------------------------------------------------------------
# 3. TRANSFORMS
# -----------------------------------------------------------------------------

# The arena itself.
#
# The palette is looked up from the phase INSIDE the transform rather than
# passed in. ATL property expressions are evaluated in a scope that can see the
# transform's own parameters, so `msbf_arena_cfg(phase)["key"]` resolves once
# when the transform is built -- which means the room's colour and the room's
# geometry can never be handed different phases by two different call sites.
#
# Note what is NOT animated here: the floor scroll, the sigil rotation and the
# sky drift all run off u_time inside the shader, so the room never rebuilds the
# screen tree to move. Only the state-driven uniforms are passed in, and they
# only change when the fight itself changes.
transform msbf_arena_t(phase=1, charge=0.0, danger=0.0, break_=0.0, glitch=0.0, amp=1.0):
    mesh True
    shader "msbf.arena"
    u_ar_shock_amp amp
    u_ar_phase float(phase)
    u_ar_horizon MSBF_ARENA_HORIZON
    u_ar_camx 0.0
    u_ar_camy 0.0
    u_ar_shock 0.0
    u_ar_charge charge
    u_ar_danger danger
    u_ar_break break_
    u_ar_glitch glitch
    u_ar_flow msbf_arena_cfg(phase)["flow"]
    u_ar_bossz msbf_arena_bossz(phase)
    u_ar_key msbf_arena_cfg(phase)["key"]
    u_ar_fog msbf_arena_cfg(phase)["fog"]
    u_ar_deck msbf_arena_cfg(phase)["deck"]

# The same room, plus one shockwave rolling out from under her. Split from the
# resting transform so the wave restarts cleanly on each impact instead of
# inheriting a half-spent progress from the previous one.
transform msbf_arena_shock_t(phase=1, charge=0.0, danger=0.0, break_=0.0, glitch=0.0, amp=1.0):
    mesh True
    shader "msbf.arena"
    u_ar_shock_amp amp
    u_ar_phase float(phase)
    u_ar_horizon MSBF_ARENA_HORIZON
    u_ar_camx 0.0
    u_ar_camy 0.0
    u_ar_charge charge
    u_ar_danger danger
    u_ar_break break_
    u_ar_glitch glitch
    u_ar_flow msbf_arena_cfg(phase)["flow"]
    u_ar_bossz msbf_arena_bossz(phase)
    u_ar_key msbf_arena_cfg(phase)["key"]
    u_ar_fog msbf_arena_cfg(phase)["fog"]
    u_ar_deck msbf_arena_cfg(phase)["deck"]
    u_ar_shock 0.0
    linear 0.62 u_ar_shock 1.0

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
    $ _ar_cfg = msbf_arena_cfg(battle.phase)
    $ _ar_ph, _ar_chg, _ar_dgr, _ar_brk, _ar_glt = msbf_arena_uniforms(battle)

    if MSBF_ARENA_SHADERS:
        # msbf_fx_scaled owns the sizing (see perf.rpy) -- do NOT add an xysize
        # here, or the graphics budget loses the one lever it has on the most
        # expensive pass in the fight. At the default `ultra` stop this is
        # exactly the transform it always was, wrapped in a sizing Transform.
        if shock:
            add msbf_fx_scaled(At(_ar_cfg["sky"], msbf_arena_shock_t(_ar_ph, _ar_chg, _ar_dgr, _ar_brk, _ar_glt, amp)), 1280, 720, True)
        else:
            add msbf_fx_scaled(At(_ar_cfg["sky"], msbf_arena_t(_ar_ph, _ar_chg, _ar_dgr, _ar_brk, _ar_glt, amp)), 1280, 720, True)
    else:
        # No shaders: the plate alone, dimmed, with a flat deck under it. The
        # fight is entirely playable; it just happens somewhere less specific.
        add _ar_cfg["sky"] xysize (1280, 720)
        add Solid("#02060cc0") xysize (1280, 720)
        add Solid("#04080f") xysize (1280, 720 - MSBF_ARENA_HORIZON_PX):
            ypos MSBF_ARENA_HORIZON_PX

# The room with no fight in it, for screens that happen before or beside the
# battle (party select). Takes a phase instead of an MSBFBattleState so it does
# not need a fight to exist yet.
screen msbf_arena_static(phase=1, dim=0.55):
    $ _as_cfg = msbf_arena_cfg(phase)
    if MSBF_ARENA_SHADERS:
        add msbf_fx_scaled(At(_as_cfg["sky"], msbf_arena_t(phase, 0.0, 0.0, 0.0, 0.0)), 1280, 720, True)
    else:
        add _as_cfg["sky"] xysize (1280, 720)
    add Solid("#02060c") xysize (1280, 720):
        alpha dim

# A soft ellipse of shadow on the deck. w is the ellipse's screen width; the
# height comes from the floor angle, so it is always the same squash as the
# grid it is lying on.
screen msbf_ground_shadow(cx, foot_y, w, strength=0.7, hover=False):
    $ _sh_h = max(10, int(w * 0.26))
    if MSBF_ARENA_SHADERS:
        if hover:
            add Solid("#00000000") at msbf_shadow_hover(strength, 2.1):
                xcenter int(cx)
                ycenter int(foot_y)
                xysize (int(w), _sh_h)
        else:
            add Solid("#00000000") at msbf_shadow_t(strength, 1.5):
                xcenter int(cx)
                ycenter int(foot_y)
                xysize (int(w), _sh_h)

# A flipped, squashed, dimmed copy of a sprite, standing in for a reflection in
# the deck. Cheap and completely convincing at this opacity -- the eye only
# wants the colours to be in the right place, not the geometry to be correct.
screen msbf_ground_reflection(img, cx, foot_y, w, h, alpha=0.16, squash=0.42):
    add img:
        xcenter int(cx)
        ypos int(foot_y)
        yanchor 0.0
        xysize (int(w), int(h * squash))
        yzoom -1.0
        alpha alpha
        blur 3.0

# --- THE PARTY, STANDING IN THE ROOM ----------------------------------------
# Silhouettes only. The acting member lifts, brightens and catches a rim of the
# arena's key light; a downed one slumps and desaturates out. Everything else
# about them (name, HP, MP) lives in the floating tag drawn by the battle
# screen, so this stays purely a picture.
screen msbf_party_silhouette(member, slot, count, key, active=False, downed=False, hit=0.0, hit_token=0):
    $ _sx, _sy, _sh, _sa, _sb = msbf_stage_slot(slot, count)
    $ _img = msbf_sil_image(getattr(member, "id", None))

    if _img is not None:
        # Being struck lifts them out of the crush for the length of the
        # flinch. A figure that recoils without also brightening reads as
        # drifting; the two together read as taking a hit.
        $ _lift = 0.30 if active else (0.06 if downed else 0.16)
        $ _lift = _lift + (0.14 if hit > 0.0 else 0.0)
        $ _amat = msbf_sil_matrix(key, _lift)
        add _img:
            if hit > 0.0:
                at msbf_sil_flinch(hit, hit_token)
            matrixcolor _amat
            xcenter _sx
            ypos (_sy + (18 if downed else (-10 if active else 0)))
            yanchor 0.0
            xysize (int(_sh * MSBF_ARCH_ASPECT), _sh)
            fit "contain"
            alpha (_sa * (0.55 if downed else 1.0))
            blur (_sb + (1.4 if downed else 0.0))
    else:
        # No sprite for this member: a plain plinth of shadow, so the slot is
        # still occupied and the deck does not read as short-handed.
        add Solid("#00000000") at msbf_shadow_t(0.55, 1.2):
            xcenter _sx
            ypos _sy
            yanchor 0.0
            xysize (int(_sh * 0.42), _sh)


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

    # Log line styles by age: 0 = newest.
    MSBF_LOG_LINE_STYLE = ("msbf_log_line_new", "msbf_log_line", "msbf_log_line_old")

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
        add Solid("#00000000") at msbf_scrim_t((0.006, 0.013, 0.026), alpha, dirn, bias, xdir):
            xpos int(x)
            ypos int(y)
            xysize (int(w), int(h))
    else:
        add Solid("#03080fbb"):
            xpos int(x)
            ypos int(y)
            xysize (int(w), int(h))

# The tag that floats over a party member's head. This is all that is left of
# the old 215x61 party card: name, the bar, the two numbers, and one status
# word. Everything the card used to say about them that was NOT changing turn
# to turn (role, row, portrait chrome) was reference, and reference does not
# get to occupy the frame -- it lives in the party-select roster instead.
screen msbf_party_tag(member, count=4, active=False, targetable=False, kb_focus=False):
    $ _tw, _th, _bar_y = msbf_stage_tag_metrics(count)
    $ _tight = count >= 5
    $ _rail = "#66e08a" if targetable else ("#55ddff" if active else ("#ffcf66" if member.row == "front" else "#4d6f85"))

    fixed:
        xysize (_tw, _th)

        if active:
            add Solid("#55ddff14") xysize (_tw, _th)
            if MSBF_FX_SHADERS:
                add Solid("#00000000") xysize (_tw, _th) at msbf_fx_glow_pulse((0.33, 0.87, 1.0), 0.10, 0.24, 2.4)
        elif targetable:
            add Solid("#66e08a1c") xysize (_tw, _th)

        add Solid(_rail) xysize (3, _th)

        if kb_focus:
            add Solid("#9becff") xysize (_tw, 2)
            add Solid("#9becff") xysize (_tw, 2):
                ypos _th - 2

        text member.name style ("msbf_party_name_compact" if member.alive else "msbf_party_name_down_compact"):
            xpos 11
            ypos -1
            xmaximum _tw - (66 if _tight else 58)

        # Top-right corner: the status word if there is one, otherwise (tight
        # only) the HP number, which the roomy tag has space to put on its own
        # line underneath instead.
        if not member.alive:
            text "DOWN" style "msbf_down_text_compact":
                xanchor 1.0
                xpos _tw - 4
                ypos 1
        elif member.guard:
            text "GUARD" style "msbf_guard_tag_compact":
                xanchor 1.0
                xpos _tw - 4
                ypos 1
        elif member.focus:
            text "FOCUS" style "msbf_focus_tag_compact":
                xanchor 1.0
                xpos _tw - 4
                ypos 1
        elif _tight:
            text "[member.hp]" style "msbf_party_stat_compact":
                xanchor 1.0
                xpos _tw - 4
                ypos 2

        fixed:
            xpos 10
            ypos _bar_y
            xysize (_tw - 20, 5)
            use msbf_energy_bar(member.hp, member.max_hp, _tw - 20, 5, "#66e08a", "#131722")

        if not _tight:
            text "[member.hp]/[member.max_hp]" style "msbf_party_stat_compact":
                xpos 11
                ypos _bar_y + 8
            text "MP [member.mp]" style "msbf_party_stat_compact":
                xanchor 1.0
                xpos _tw - 4
                ypos _bar_y + 8


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

transform msbf_turnover_band(up=True, delay=0.0, thick=90, col="#ff3868"):
    subpixel True
    xsize 1600
    ysize thick
    xcenter 640
    ycenter (820 if up else -100)
    alpha 0.0
    rotate (-7.0 if up else 7.0)
    pause delay
    alpha 0.75
    easeout 0.42 ycenter (-120 if up else 840)
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

    add Solid(_tv_col) at msbf_turnover_wash(_tv_col)

    # Kept translucent on purpose: the handover is a beat, not a curtain, and
    # the fight underneath has to stay legible through it.
    add Solid(_tv_col + "9e") xysize (1600, 72) at msbf_turnover_band(_to_boss, 0.00, 72, _tv_col)
    add Solid("#ffffff6a") xysize (1600, 20) at msbf_turnover_band(_to_boss, 0.07, 20, "#ffffff")
    add Solid(_tv_col + "4e") xysize (1600, 120) at msbf_turnover_band(_to_boss, 0.13, 120, _tv_col)

    add Solid("#ffffff") xysize (1400, 3) at msbf_turnover_rule(_to_boss)

    # The side receiving the tempo gets lit from the direction it is arriving.
    if MSBF_FX_SHADERS:
        if _to_boss:
            $ _tv_x, _tv_y = msbf_boss_anchor(phase)
            add Solid("#00000000") xysize (900, 700) at msbf_fx_glow_pop(_tv_rgb, 0.75, 1.5, 0.72):
                xcenter _tv_x
                ycenter _tv_y
        else:
            add Solid("#00000000") xysize (1280, 460) at msbf_fx_glow_pop(_tv_rgb, 0.62, 1.7, 0.72):
                xcenter 640
                ycenter 620

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


# -----------------------------------------------------------------------------
# 7. GETTING HIT
# -----------------------------------------------------------------------------
# The boss landing a blow on a party member had no reaction at all. She had a
# recoil, the room had a shockwave, the number floated up -- and the person it
# happened to did not move. All the weight was on the side dealing damage,
# which is exactly backwards for the half of the fight you are supposed to be
# afraid of.
#
# Everything here scales off the SAME MSBF_IMPACT_WEIGHT the camera and the
# deck wave read, so a weakness hit on you lands as hard as a weakness hit on
# her -- which it did not before: the boss's side of the table was pinned at
# 1.0 while the player's crits and weaknesses got 1.6.

# The struck figure snaps back and returns. Hard out, soft in: a flinch that
# eases both ways reads as swaying, not as being hit.
transform msbf_sil_flinch(strength=1.0, token=0):
    subpixel True
    xoffset 0
    yoffset 0
    easeout 0.045 xoffset int(-13 * strength) * (1 if (token % 2) else -1) yoffset int(5 * strength)
    easein 0.26 xoffset 0 yoffset 0

# The tag over their head takes the same hit, a beat tighter.
transform msbf_tag_shake(strength=1.0, token=0):
    subpixel True
    xoffset 0
    easeout 0.04 xoffset int(-8 * strength) * (1 if (token % 2) else -1)
    easeout 0.06 xoffset int(5 * strength) * (1 if (token % 2) else -1)
    easein 0.16 xoffset 0

# The blow itself, at the point of contact.
screen msbf_party_hit_burst(x, y, strength=1.0, color=(1.0, 0.30, 0.42)):
    if MSBF_FX_SHADERS:
        $ _hb_s = max(0.3, min(2.0, strength))
        add Solid("#00000000") at msbf_fx_glow_pop(color, 0.55 + 0.45 * _hb_s, 1.5, 0.34):
            xcenter int(x)
            ycenter int(y)
            xysize (int(150 * _hb_s), int(150 * _hb_s))
        use msbf_shock_ring(int(x), int(y), int(200 * _hb_s), color, 0.14, 0.7 + 0.6 * _hb_s, 0.40)
