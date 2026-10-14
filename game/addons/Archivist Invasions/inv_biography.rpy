# Biography invasion: a turn-based rolling-HP bout followed by open combat.
# BIOGame owns simulation state; BIOStage advances it at 60 ticks/second and
# renders cached displayables. Screens route input/results without frame timers.
#
# Act two has four recoverable daggers. Hits break poise before they can damage
# health during BUCKLE; dagger speed and the ENTRY meter make distance matter.
# The borrowed Matsuda silhouette already carries its glaive. Separate glaive
# art represents spectral thrown copies only. Cosmetic lightning has no hitbox.
# Shared encounter presentation constraints live in invasions.rpy.
#
# step() dispatches arrive, menu/sub, beat, enemy, shift, open and leave modes.
# In open combat b_state is idle/wind/act/recover/buckle. Beat readouts wait for
# input. Coordinates are 1280x720 screen pixels; speeds and timers use 60Hz ticks.
# Angles are degrees, clockwise from right in screen space (positive y down).

init -9 python:
    BIO_SHADER_OK = False
    BIO_MISREG_OK = False

    def _bio_register_shaders():
        # THE ROOM. One opaque full-screen quad hosted on the shipped
        # hyperspace plate, so the art is the substrate rather than a backdrop
        # behind an effect. Sample coordinates are domain-warped by layered
        # noise and a slow radial rush; a low-frequency barrel wobble
        # underneath is the nausea. u_bio_corrupt crushes it toward act two.
        # u_bio_hole is the wormhole: a spiral vortex around a point, with a
        # black core and a hot rim.
        #
        # THE STAGE IS THERE IN BOTH ACTS (Oct 2 2026). Act one used to float
        # the figure over a backdrop with nothing under it -- a picture on a
        # picture. The boards now exist from the first frame, unlit and seen
        # from a low camera (u_bio_stage.x is how lit they are), so the figure
        # stands on something; the tear lights them from its feet outward
        # (the wave) and the camera climbs to act two's proscenium.
        #
        # AND THE HAZARDS ARE PAINTED INTO THE FLOOR. Rings, sweeping bars,
        # the blade's footprint, the lunge telegraph, the poise arc and the
        # light pools are evaluated per pixel in the SIMULATION'S OWN WORLD
        # COORDINATES, recovered by inverting bio_project() -- so they are
        # perspective-correct by construction, glow, fog with depth, and can
        # never drift from the hitbox they draw. (They were canvas polylines
        # rasterised on the CPU and re-uploaded every frame.)
        renpy.register_shader("inv.soup", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_bio_res;
            uniform float u_bio_time;
            uniform float u_bio_corrupt;
            uniform float u_bio_pulse;
            uniform float u_bio_jolt;
            uniform float u_bio_flash;
            uniform float u_bio_dark;
            uniform float u_bio_rush;
            uniform float u_bio_spin;
            uniform float u_bio_floor;
            uniform float u_bio_horizon;
            uniform float u_bio_floork;
            uniform float u_bio_fscroll;
            uniform float u_bio_fury;
            uniform vec4 u_bio_cam;
            uniform vec4 u_bio_hole;
            uniform vec4 u_bio_stage;
            uniform vec4 u_bio_arena;
            uniform vec2 u_bio_persp;
            uniform vec4 u_bio_boss;
            uniform vec4 u_bio_plr;
            uniform vec4 u_bio_ring0;
            uniform vec4 u_bio_ring1;
            uniform vec4 u_bio_ring2;
            uniform vec4 u_bio_ring3;
            uniform vec4 u_bio_rings;
            uniform vec4 u_bio_bar0;
            uniform vec4 u_bio_bar1;
            uniform vec4 u_bio_bar2;
            uniform vec4 u_bio_blade;
            uniform vec4 u_bio_bladek;
            uniform vec4 u_bio_thrust;
            uniform vec4 u_bio_dag01;
            uniform vec4 u_bio_dag23;
            uniform vec4 u_bio_dagk;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float bio_hash(vec2 p) {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
            }
            float bio_noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                f = f * f * (3.0 - 2.0 * f);
                float a = bio_hash(i);
                float b = bio_hash(i + vec2(1.0, 0.0));
                float c = bio_hash(i + vec2(0.0, 1.0));
                float d = bio_hash(i + vec2(1.0, 1.0));
                return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
            }
            float bio_fbm(vec2 p) {
                float v = 0.0;
                float a = 0.5;
                for (int i = 0; i < 4; i++) {
                    v += a * bio_noise(p);
                    p = p * 2.03 + vec2(17.3, 9.1);
                    a *= 0.5;
                }
                return v;
            }
            vec2 bio_mirror(vec2 p) {
                return abs(fract(p * 0.5) * 2.0 - 1.0);
            }
            float bio_ad(float a, float b) {
                return mod(a - b + 180.0, 360.0) - 180.0;
            }
            // One telegraphed or live ring on the boards: a crisp core the
            // width of the hitbox, a soft halo, gold while it is a warning
            // and red once it moves.
            vec3 bio_ring(vec4 r, float state, vec2 wp, float px, float t) {
                if (state < 0.5) {
                    return vec3(0.0);
                }
                float d = abs(distance(wp, r.xy) - r.z);
                float w = max(r.w * 0.5, 1.0);
                float core = 1.0 - smoothstep(w - px, w + px, d);
                float halo = exp(-(d * d) / (w * w * 7.0));
                float live = step(1.5, state);
                vec3 c = mix(vec3(1.0, 0.80, 0.34), vec3(1.0, 0.16, 0.28), live);
                float k = mix(0.62 + 0.38 * sin(t * 16.0), 1.0, live);
                return c * (core * 1.25 + halo * 0.55) * k;
            }
            // A recital line sweeping across the boards.
            vec3 bio_bar(vec4 b, vec2 wp, float px, float t) {
                if (b.x < -0.5) {
                    return vec3(0.0);
                }
                float v = mix(wp.y, wp.x, step(0.5, b.x));
                float d = abs(v - b.y);
                float w = max(b.z * 0.5, 1.0);
                float core = 1.0 - smoothstep(w - px, w + px, d);
                float halo = exp(-(d * d) / (w * w * 9.0));
                float live = step(1.5, b.w);
                vec3 c = mix(vec3(1.0, 0.80, 0.34), vec3(1.0, 0.16, 0.28), live);
                float k = mix(0.55 + 0.45 * sin(t * 18.0), 1.0, live);
                return c * (core * 1.15 + halo * 0.60) * k;
            }
            float bio_spot(vec2 wp, vec2 c, float r) {
                vec2 d = (wp - c) / max(r, 1.0);
                return 1.0 / (1.0 + dot(d, d) * 3.0);
            }
        """, fragment_300="""
            const float BIO_TAU = 6.2831853;

            // --- THE CAMERA ---------------------------------------------------
            // Act two is shot through a camera that rolls, pans and breathes
            // on its focal length. This fragment knows where it landed on the
            // SENSOR; everything downstream (the horizon, the floor, the hole)
            // is reasoned about in the camera's own un-rolled frame, so the
            // shader and the projected entities agree exactly.
            vec2 cres = max(u_bio_res, vec2(1.0));
            vec2 cmid = cres * 0.5;
            vec2 cdd = v_tex_coord * cres - cmid - vec2(u_bio_cam.y, u_bio_cam.z);
            float ccr = cos(-u_bio_cam.x);
            float csr = sin(-u_bio_cam.x);
            cdd = vec2(cdd.x * ccr - cdd.y * csr, cdd.x * csr + cdd.y * ccr);
            vec2 cpu = cmid + cdd / max(u_bio_cam.w, 0.05);

            vec2 uv = cpu / cres;
            float t = u_bio_time;
            float corrupt = clamp(u_bio_corrupt, 0.0, 1.0);
            float pulse = clamp(u_bio_pulse, 0.0, 1.0);
            float fury = clamp(u_bio_fury, 0.0, 1.0);
            float lit = clamp(u_bio_stage.x, 0.0, 1.0);

            vec2 c = uv - 0.5;

            // --- the wormhole -------------------------------------------------
            vec2 hp = (u_bio_hole.xy / cres) - 0.5;
            float hr = max(u_bio_hole.z, 1.0) / cres.x;
            float hs = clamp(u_bio_hole.w, 0.0, 1.0);
            vec2 hv = c - hp;
            float hd = length(hv);
            float hinf = (1.0 - smoothstep(0.0, hr, hd)) * hs;
            if (hinf > 0.001) {
                float ha = hinf * hinf * 5.4 + t * 0.6 * hinf;
                float cs = cos(ha);
                float sn = sin(ha);
                hv = vec2(hv.x * cs - hv.y * sn, hv.x * sn + hv.y * cs);
                c = hp + hv * (1.0 - 0.62 * hinf);
            }

            // --- rotational momentum (integrated in the sim, see u_bio_spin)
            vec2 pivot = vec2(sin(t * 0.13) * 0.06, cos(t * 0.17) * 0.05);
            vec2 rc = c - pivot;
            float rr = length(rc);
            float twist = u_bio_spin
                        + sin(t * 0.19) * 1.15 * rr
                        + sin(t * 0.11 + rr * 4.0) * 0.45 * (1.0 + corrupt)
                        + sin(t * 0.53 + rr * 7.0) * 0.16 * (1.0 + corrupt);
            float tcs = cos(twist);
            float tsn = sin(twist);
            c = pivot + vec2(rc.x * tcs - rc.y * tsn, rc.x * tsn + rc.y * tcs);

            // --- nausea: a slow barrel wobble the whole frame breathes with --
            float r = length(c);
            float wob = sin(t * 0.37) * 0.055 + sin(t * 0.19 + 1.7) * 0.035;
            wob += (sin(t * 0.83 + 2.1) * 0.030 + sin(t * 1.29) * 0.018) * fury;
            c *= 1.0 + wob * (r * r) * (1.0 + 1.5 * corrupt + 0.9 * fury);
            c.x += sin(c.y * 3.1 + t * 0.61) * 0.022 * fury;
            c.y += sin(c.x * 2.7 - t * 0.47) * 0.014 * fury;

            // --- the rush -----------------------------------------------------
            float rush = u_bio_rush;
            c *= 1.0 + 0.20 * sin(rush * 0.9 + r * 5.0);
            c += normalize(c + vec2(1e-5)) * 0.035 * sin(rush * 1.3 - r * 8.0);

            // --- boiling: two warp fields at different scales and rates ------
            vec2 w1 = vec2(bio_fbm(c * 3.1 + vec2(t * 0.21, -t * 0.17)),
                        bio_fbm(c * 3.1 + vec2(9.2 - t * 0.13, 4.7 + t * 0.11)));
            float ct = -twist * 0.55;
            float ccs = cos(ct);
            float csn = sin(ct);
            vec2 c2 = vec2(c.x * ccs - c.y * csn, c.x * csn + c.y * ccs);
            vec2 w2 = vec2(bio_fbm(c2 * 7.7 - vec2(t * 0.41, t * 0.29)),
                        bio_fbm(c2 * 7.7 + vec2(2.4 + t * 0.33, 8.8 - t * 0.37)));
            float warp_amt = 0.085 + 0.055 * corrupt + 0.05 * pulse;
            vec2 sp = c + (w1 - 0.5) * warp_amt + (w2 - 0.5) * warp_amt * 0.45;

            float jolt = clamp(u_bio_jolt, 0.0, 1.0);
            float row = floor(uv.y * 96.0);
            sp.x += (bio_hash(vec2(row, floor(t * 24.0))) - 0.5) * 0.09 * jolt;
            float tearpos = fract(t * 0.21);
            float tearband = 1.0 - smoothstep(0.0, 0.055, abs(uv.y - tearpos));
            sp.x += (bio_hash(vec2(row, 5.0)) - 0.5) * 0.11 * tearband * fury;

            vec2 base_uv = bio_mirror(sp + 0.5);
            float split = (0.0018 + 0.010 * corrupt) * (1.0 + 2.2 * pulse + 3.0 * jolt);
            vec2 dir = normalize(c + vec2(1e-5));
            vec3 col;
            col.r = texture2D(tex0, bio_mirror(sp + dir * split + 0.5)).r;
            col.g = texture2D(tex0, base_uv).g;
            col.b = texture2D(tex0, bio_mirror(sp - dir * split + 0.5)).b;

            float veins = bio_fbm(c * 9.0 + vec2(t * 0.13, -t * 0.09));
            float wall = 1.0 - smoothstep(0.0, 0.09 + 0.05 * corrupt, abs(veins - 0.5));
            col += vec3(0.34, 0.42, 0.62) * wall * (0.16 + 0.10 * pulse) * (1.0 - corrupt);
            col += vec3(0.62, 0.10, 0.16) * wall * (0.20 + 0.26 * pulse) * corrupt;

            float lum = dot(col, vec3(0.299, 0.587, 0.114));
            vec3 bruise = vec3(lum * 1.32, lum * 0.20, lum * 0.34);
            bruise += vec3(0.42, 0.03, 0.09) * pow(clamp(lum, 0.0, 1.0), 2.2);
            col = mix(col, bruise, corrupt);
            col *= mix(1.0, 0.80 + 0.55 * pulse, corrupt);

            float ring = sin(r * 34.0 - t * 3.1 - pulse * 5.0);
            col += vec3(0.50, 0.08, 0.13) * smoothstep(0.90, 1.0, ring)
                * pulse * (0.25 + 0.75 * corrupt);

            float lines = 0.5 + 0.5 * sin(uv.y * u_bio_res.y * 1.57 + t * 6.0);
            col *= 1.0 - corrupt * 0.10 * lines;

            // --- the hole itself, drawn after the room it is eating -----------
            if (hs > 0.001) {
                float core = 1.0 - smoothstep(hr * 0.12, hr * 0.52, hd);
                col *= mix(1.0, 0.02, core * hs);
                float lip = (1.0 - smoothstep(0.0, hr * 0.16, abs(hd - hr * 0.52)));
                col += vec3(1.00, 0.22, 0.34) * lip * hs * 1.35;
                float halo = (1.0 - smoothstep(hr * 0.5, hr * 1.05, hd));
                col += vec3(0.55, 0.06, 0.14) * halo * hs * 0.55;
            }

            // --- THE STAGE ----------------------------------------------------
            if (u_bio_floor > 0.5) {
                float py = cpu.y;
                if (py > u_bio_horizon - 26.0) {
                    float persp = (py - u_bio_horizon) / max(u_bio_floork, 1.0);
                    persp = max(persp, 0.001);
                    float wz = 1.0 / persp;
                    float wx = (uv.x - 0.5) * u_bio_res.x / persp;

                    vec2 fuv = vec2(wx * 0.00085, wz * 0.30 + u_bio_fscroll);
                    vec3 fl = texture2D(tex0, bio_mirror(fuv)).rgb;
                    float flum = dot(fl, vec3(0.299, 0.587, 0.114));
                    vec3 act1c = vec3(flum * 0.40, flum * 0.46, flum * 0.66);
                    vec3 floorc = mix(mix(fl * 0.36, act1c, u_bio_stage.w),
                                      vec3(flum * 0.82, flum * 0.15, flum * 0.22),
                                      corrupt);
                    floorc *= 0.16 + 0.84 * lit;

                    // Rushing rings of depth and converging rails -- these ARE
                    // the floor; without them the plate reads as more sky.
                    // Unlit, they are a faint survey grid; lit, they burn.
                    float rings = abs(fract(wz * 1.15 - u_bio_fscroll * 2.2) * 2.0 - 1.0);
                    vec3 ringc = mix(vec3(0.42, 0.52, 0.80), vec3(0.85, 0.16, 0.24), corrupt);
                    floorc += ringc * smoothstep(0.74, 1.0, rings)
                            * (0.36 + 0.5 * pulse) * (0.16 + 0.84 * lit * lit);
                    float rails = abs(fract(wx * 0.0018) * 2.0 - 1.0);
                    floorc += vec3(0.42, 0.48, 0.62) * smoothstep(0.82, 1.0, rails)
                            * 0.40 * (0.22 + 0.78 * lit);

                    // GLOSS. The boards are a dark lacquer: near the horizon
                    // they mirror the soup above them (cheap -- the unwarped
                    // plate at the reflected row, Fresnel-weighted).
                    vec2 ruv = vec2(uv.x, (2.0 * u_bio_horizon - py) / cres.y);
                    vec3 refl = texture2D(tex0, bio_mirror(ruv * vec2(1.0, 1.4)
                                    + vec2(sin(t * 0.07) * 0.02, 0.0))).rgb;
                    float fres = exp(-persp * 4.2);
                    floorc += mix(refl * vec3(0.55, 0.62, 0.95), refl * vec3(0.95, 0.30, 0.38),
                                  corrupt) * fres * (0.12 + 0.22 * lit);

                    // --- THE SIMULATION'S WORLD, recovered per pixel ----------
                    // bio_project: pp = 1 / lerp(1/far, 1/near, u) and
                    // sx = 640 + (wx - 640) * pp. Inverted here, exactly.
                    float far = max(u_bio_persp.x, 0.01);
                    float nr = max(u_bio_persp.y, 0.01);
                    float uu = (1.0 / persp - 1.0 / far) / (1.0 / nr - 1.0 / far);
                    vec2 wp = vec2(cmid.x + (cpu.x - cmid.x) / persp,
                                   u_bio_arena.y + uu * (u_bio_arena.w - u_bio_arena.y));
                    float pxw = 1.3 / persp;
                    vec3 emit = vec3(0.0);

                    // Light pools: the Archivist is a red lamp standing on its
                    // own stage, you are a small teal one. This is most of
                    // what makes the bodies sit ON the boards.
                    emit += vec3(1.0, 0.16, 0.26) * bio_spot(wp, u_bio_boss.xy, 115.0)
                            * u_bio_boss.z;
                    emit += vec3(0.36, 0.92, 0.82) * bio_spot(wp, u_bio_plr.xy, 46.0)
                            * u_bio_plr.z;

                    // The stage lighting itself up from the figure's feet.
                    if (u_bio_stage.z > 0.001) {
                        float wq = (distance(wp, u_bio_boss.xy) - u_bio_stage.y) / 46.0;
                        float wv = exp(-wq * wq);
                        emit += vec3(1.0, 0.45, 0.55) * wv * u_bio_stage.z;
                    }

                    emit += bio_ring(u_bio_ring0, u_bio_rings.x, wp, pxw, t);
                    emit += bio_ring(u_bio_ring1, u_bio_rings.y, wp, pxw, t);
                    emit += bio_ring(u_bio_ring2, u_bio_rings.z, wp, pxw, t);
                    emit += bio_ring(u_bio_ring3, u_bio_rings.w, wp, pxw, t);
                    emit += bio_bar(u_bio_bar0, wp, pxw, t);
                    emit += bio_bar(u_bio_bar1, wp, pxw, t);
                    emit += bio_bar(u_bio_bar2, wp, pxw, t);

                    // THE BLADE'S FOOTPRINT: the annular sector it is sweeping
                    // right now, plus a fading wake behind it. The hitbox, drawn
                    // where the collision is.
                    if (u_bio_bladek.x > 0.5) {
                        vec2 dv = wp - u_bio_boss.xy;
                        float br = length(dv);
                        float inner = u_bio_blade.z;
                        float outer = u_bio_blade.w;
                        float band = smoothstep(inner - pxw, inner + pxw, br)
                                   * (1.0 - smoothstep(outer - pxw, outer + pxw, br));
                        if (band > 0.0) {
                            float ang = degrees(atan(dv.y, dv.x));
                            float arc = u_bio_bladek.z;
                            float hit = 0.0;
                            float wake = 0.0;
                            for (int k = 0; k < 2; k++) {
                                if (float(k) < u_bio_bladek.x - 0.5) {
                                    float arm = u_bio_blade.x + 180.0 * float(k);
                                    float da = bio_ad(ang, arm);
                                    hit = max(hit, 1.0 - smoothstep(arc - 2.5, arc + 2.5, abs(da)));
                                    float tr = u_bio_blade.y;
                                    if (abs(tr) > 0.5) {
                                        float tu = -da / tr;
                                        wake = max(wake, step(0.0, tu) * step(tu, 1.0)
                                                         * (1.0 - tu) * 0.55);
                                    }
                                }
                            }
                            float mid = 1.0 - abs((br - inner) / max(outer - inner, 1.0) - 0.5) * 1.2;
                            vec3 bc = mix(vec3(1.0, 0.80, 0.34), vec3(1.0, 0.22, 0.32),
                                          step(0.5, 1.0 - u_bio_bladek.w));
                            emit += bc * band * (hit * (0.85 + 0.35 * mid) + wake)
                                    * u_bio_bladek.y;
                        }
                    }

                    // The lunge, telegraphed on the boards along its line.
                    if (u_bio_thrust.z > 0.001) {
                        vec2 dv = wp - u_bio_boss.xy;
                        float a = radians(u_bio_thrust.x);
                        vec2 dirt = vec2(cos(a), sin(a));
                        float along = dot(dv, dirt);
                        float perp = abs(dv.x * dirt.y - dv.y * dirt.x);
                        float w = u_bio_thrust.w * 0.5;
                        float on = step(0.0, along) * (1.0 - smoothstep(u_bio_thrust.y - 40.0,
                                                                        u_bio_thrust.y, along));
                        float core = 1.0 - smoothstep(w - pxw, w + pxw, perp);
                        float halo = exp(-(perp * perp) / (w * w * 6.0));
                        float march = 0.6 + 0.4 * sin(along * 0.06 - t * 22.0);
                        emit += vec3(1.0, 0.80, 0.34) * on * (core * march + halo * 0.4)
                                * u_bio_thrust.z;
                    }

                    // POISE, as an arc of the player's colour at its feet.
                    if (u_bio_boss.w > -0.5) {
                        vec2 dv = wp - (u_bio_boss.xy + vec2(0.0, 14.0));
                        vec2 e = vec2(dv.x, dv.y / 0.72);
                        float er = length(e);
                        float on = 1.0 - smoothstep(2.4 - pxw, 2.4 + pxw, abs(er - 96.0));
                        float pa = mod(degrees(atan(e.y, e.x)) + 90.0, 360.0) / 360.0;
                        float fill = step(pa, u_bio_boss.w);
                        vec3 pc = mix(vec3(1.0, 0.82, 0.47), vec3(0.36, 0.91, 0.82),
                                      step(0.30, u_bio_boss.w));
                        emit += pc * on * (0.18 + 0.82 * fill) * 1.2;
                    }

                    // Daggers lying on the boards: small teal glints.
                    vec4 dk = u_bio_dagk;
                    emit += vec3(0.36, 0.91, 0.82) * bio_spot(wp, u_bio_dag01.xy, 16.0) * dk.x * 0.9;
                    emit += vec3(0.36, 0.91, 0.82) * bio_spot(wp, u_bio_dag01.zw, 16.0) * dk.y * 0.9;
                    emit += vec3(0.36, 0.91, 0.82) * bio_spot(wp, u_bio_dag23.xy, 16.0) * dk.z * 0.9;
                    emit += vec3(0.36, 0.91, 0.82) * bio_spot(wp, u_bio_dag23.zw, 16.0) * dk.w * 0.9;

                    // Fog: distant emission fades into the haze like the boards.
                    float haze = smoothstep(0.02, 0.55, persp);
                    floorc += emit * (0.35 + 0.65 * haze);
                    floorc = mix(col * 0.85, floorc, haze);
                    floorc *= 0.55 + 0.65 * haze;

                    float blend = smoothstep(u_bio_horizon - 26.0,
                                            u_bio_horizon + 34.0, py);
                    col = mix(col, floorc, blend);
                }
            }

            float vig = 1.0 - r * r * (mix(1.05, 1.65, corrupt) + 0.55 * fury);
            col *= max(vig, 0.0);
            col = mix(col, vec3(1.0, 0.96, 0.97), clamp(u_bio_flash, 0.0, 1.0));
            col *= 1.0 - clamp(u_bio_dark, 0.0, 1.0);
            gl_FragColor = vec4(col, 1.0);
        """)
    def _bio_register_misreg():
        # BIOGRAPHY'S OWN BODY, and until Aug 23 2026 it did not have one --
        # it borrowed inv.flesh, the shared shader that also draws the HEART in
        # all four corruptive states. That is why it was the least distinct of
        # the four: its body and the player's avatar were literally the same
        # effect at different amplitudes, and inv.flesh could never be pushed
        # because the user has twice dialled the heart's warp DOWN.
        #
        # So the axis gets taken seriously instead. Biography is
        # MISREGISTRATION -- something assembled incorrectly, and visibly
        # DIGITAL about it, against Horror's liquid undulation, Nonfiction's
        # flat reproduction and Mystery's sliding strata. Everything in here
        # is a different way for a plate to be out of register:
        #
        #   SLIPPED SLICES. The old shader slid bands sideways. This one has
        #   them sample from the WRONG PART OF THE BODY -- a band's source y is
        #   offset, so the figure is assembled out of slices that do not belong
        #   to each other. That is what misregistration actually means, and it
        #   is the single biggest step up: a sliding band is a wobble, a
        #   slipped slice is a thing that has been PUT TOGETHER WRONG.
        #
        #   PER-CHANNEL REGISTRATION. Red, green and blue each get their own
        #   band offset rather than one shared chromatic split, so the fringing
        #   is genuinely three plates failing to line up instead of one image
        #   with coloured edges.
        #
        #   MACROBLOCK HOLD. Quantised blocks lock onto a stale offset and hold
        #   it for a beat before releasing -- datamosh, the most digital
        #   artefact there is, and nothing else in the set has anything like
        #   it.
        #
        #   SEAM LIGHT. Where two neighbouring bands disagree badly the join
        #   burns, so the misassembly draws its own edges instead of relying on
        #   the viewer to notice it.
        #
        # It keeps Biography's erosion dissolve (cells, for coming through a
        # hole) and its squash/stretch pivot, because those are load-bearing
        # for the lunge smear and the arrival.
        renpy.register_shader("inv.misreg", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_mis_res;
            uniform float u_mis_t;
            uniform float u_mis_warp;
            uniform float u_mis_split;
            uniform float u_mis_slip;
            uniform float u_mis_mosh;
            uniform vec2 u_mis_stretch;
            uniform float u_mis_pivot;
            uniform float u_mis_hurt;
            uniform float u_mis_diss;
            uniform vec4 u_mis_tint;
            uniform vec4 u_mis_rim;
            uniform vec4 u_mis_scan;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float mis_hash(vec2 p) {
                return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
            }
            // One band's registration error: (x offset, y slice offset).
            vec2 mis_reg(float band, float step_i, float amp, float slip) {
                float hx = mis_hash(vec2(band, step_i)) - 0.5;
                float hy = mis_hash(vec2(band + 31.7, step_i * 1.37)) - 0.5;
                return vec2(hx * amp, hy * slip);
            }
        """, fragment_300="""
            vec2 plate_uv = v_tex_coord;

            vec2 uv = v_tex_coord;
            vec2 piv = vec2(0.5, clamp(u_mis_pivot, 0.0, 1.0));
            vec2 stv = max(u_mis_stretch, vec2(0.08));
            uv = (uv - piv) / stv + piv;

            float t = u_mis_t;
            float w = clamp(u_mis_warp, 0.0, 4.0);
            float slip = clamp(u_mis_slip, 0.0, 1.0);
            float mosh = clamp(u_mis_mosh, 0.0, 1.0);

            // --- BANDS, AND THEY STEP RATHER THAN SLIDE --------------------
            // A registration error is not a wave. The plate is set down in the
            // wrong place and HOLDS there until it is set down again, so the
            // offset is quantised in time as well as in space.
            const float BANDS = 18.0;
            float band = floor(uv.y * BANDS);
            float rate = 1.4 + mis_hash(vec2(band, 9.1)) * 2.6;
            float step_i = floor(t * rate + mis_hash(vec2(band, 3.3)) * 7.0);
            float amp = 0.010 + 0.055 * w;
            vec2 reg = mis_reg(band, step_i, amp, 0.075 * slip);

            // --- MACROBLOCK HOLD ------------------------------------------
            // Rectangular blocks lock onto a stale registration and keep it
            // after the rest of the plate has moved on.
            vec2 blk = floor(uv * vec2(14.0, 22.0));
            float bsel = mis_hash(blk + floor(t * 2.3) * 1.7);
            float held = step(1.0 - 0.34 * mosh, bsel);
            if (held > 0.5) {
                float stale = step_i - (1.0 + floor(mis_hash(blk) * 3.0));
                reg = mis_reg(band, stale, amp * 1.9, 0.14 * slip);
            }

            // --- PER-CHANNEL REGISTRATION ----------------------------------
            // Three plates, three errors. Not one image with coloured edges.
            float sp = u_mis_split * (0.004 + 0.013 * w);
            vec2 uvg = uv + reg;
            vec2 uvr = uv + reg * 1.35 + vec2(sp, reg.y * 0.6);
            vec2 uvb = uv + reg * 0.70 - vec2(sp, reg.y * 0.6);

            // Three taps and THREE taps only -- each plate is fetched once
            // and both its channel and its alpha come out of the same fetch.
            // Reading .r and .a as two separate texture2D calls is two
            // fetches for one texel and doubles the cost of the whole shader.
            vec4 cg = texture2D(tex0, uvg);
            vec4 cr = texture2D(tex0, uvr);
            vec4 cb = texture2D(tex0, uvb);
            // Alpha is the STRONGEST of the three plates, so a channel that
            // has slipped off the silhouette still prints instead of being
            // clipped to nothing -- that fringe is the whole effect, and it is
            // why this shader has to hold the premultiplied contract at the
            // end rather than by luck.
            float a = max(cg.a, max(cr.a, cb.a));
            vec3 col = vec3(cr.r, cg.g, cb.b);

            // --- SEAM LIGHT -------------------------------------------------
            // Where this band and the one above it disagree badly, the join
            // burns. The misassembly draws its own edges.
            float above = band - 1.0;
            vec2 reg2 = mis_reg(above, floor(t * (1.4 + mis_hash(vec2(above, 9.1))
                            * 2.6) + mis_hash(vec2(above, 3.3)) * 7.0),
                            amp, 0.075 * slip);
            float disagree = clamp(length(reg - reg2) / max(amp, 1e-4), 0.0, 2.0);
            float edge = 1.0 - smoothstep(0.0, 1.6 / BANDS,
                                        abs(uv.y * BANDS - band));
            col += vec3(0.55, 0.62, 0.85) * edge * disagree * 0.16 * a;

            // --- EROSION, kept: it comes through a hole in the world --------
            float diss = clamp(u_mis_diss, 0.0, 1.0);
            if (diss > 0.0) {
                vec2 cell = floor(uv * vec2(52.0, 74.0));
                float n = mis_hash(cell);
                float k = step(diss, n);
                col *= k;
                a *= k;
            }

            // THE ROOM'S LIGHT ON IT (Oct 2 2026). A key tint from whatever
            // it is standing in, and a RIM where the silhouette faces up and
            // out -- two extra taps of alpha, read as "how much body is above
            // and beside me". Without them the figure is lit by nothing and
            // reads as a picture laid on the room instead of a thing in it.
            col *= mix(vec3(1.0), u_mis_tint.rgb, clamp(u_mis_tint.a, 0.0, 1.0));
            if (u_mis_rim.a > 0.001) {
                float above = min(texture2D(tex0, uvg + vec2(0.007, -0.006)).a,
                                  texture2D(tex0, uvg + vec2(-0.007, -0.006)).a);
                float rim = clamp(cg.a - above, 0.0, 1.0);
                col += u_mis_rim.rgb * rim * u_mis_rim.a * a;
            }

            // CHECK: a reading band travelling up the body.
            if (u_mis_scan.y > 0.001) {
                float sd = abs(uv.y - u_mis_scan.x);
                float sb = 1.0 - smoothstep(0.0, max(u_mis_scan.z, 0.002), sd);
                col += vec3(0.36, 0.91, 0.82) * sb * u_mis_scan.y * a;
                col *= 1.0 - 0.35 * u_mis_scan.y * smoothstep(0.0, 0.25, uv.y - u_mis_scan.x);
            }

            float hurt = clamp(u_mis_hurt, 0.0, 1.0);
            col = mix(col, vec3(a), hurt);

            // THE PLATE CONTRACT -- see the note in invasions.rpy. RGB clamped
            // to alpha (this shader assembles colour from three DIFFERENT taps,
            // so it produces bright pixels at zero alpha constantly), and a
            // feather in the plate's own coordinate so no band can be cut off
            // in a straight line at the rectangle's edge.
            vec2 pe = min(plate_uv, vec2(1.0) - plate_uv);
            float fade = smoothstep(0.0, 0.045, min(pe.x, pe.y));
            a *= fade;
            gl_FragColor = vec4(min(col, vec3(a)), a);
        """)

    try:
        _bio_register_misreg()
        BIO_MISREG_OK = True
    except Exception as _bio_ms_e:
        BIO_MISREG_OK = False
        try:
            renpy.log("INV FX: misreg shader registration failed: %r"
                    % _bio_ms_e)
        except Exception:
            pass

    try:
        _bio_register_shaders()
        BIO_SHADER_OK = True
    except Exception as _bio_sh_e:
        BIO_SHADER_OK = False
        try:
            renpy.log("INV FX: soup shader registration failed: %r" % _bio_sh_e)
        except Exception:
            pass


init -8 python:
    def bio_misreg(plate, W, H, t, warp=1.0, split=1.0, slip=1.0, mosh=0.0,
                stretch=(1.0, 1.0), pivot=0.86, hurt=0.0, diss=0.0,
                tint=(1.0, 1.0, 1.0, 0.0), rim=(0.0, 0.0, 0.0, 0.0),
                scan=(0.0, 0.0, 0.02, 0.0)):
        """Wrap a padded plate in BIOGRAPHY'S OWN body shader.

        Mirrors inv_flesh()'s signature so the call site reads the same, plus
        the two knobs that are this shader's own: SLIP (how far a band samples
        from the wrong part of the body) and MOSH (how much of the plate is
        holding a stale registration in macroblocks). TINT and RIM are the
        room's light on it; SCAN is CHECK's reading band.
        """
        return Transform(
            plate, mesh=True, shader="inv.misreg",
            u_mis_res=(float(W), float(H)),
            u_mis_t=float(t),
            u_mis_warp=float(warp),
            u_mis_split=float(split),
            u_mis_slip=float(slip),
            u_mis_mosh=float(mosh),
            u_mis_stretch=(float(stretch[0]), float(stretch[1])),
            u_mis_pivot=float(pivot),
            u_mis_hurt=float(hurt),
            u_mis_diss=float(diss),
            u_mis_tint=tuple(float(v) for v in tint),
            u_mis_rim=tuple(float(v) for v in rim),
            u_mis_scan=tuple(float(v) for v in scan))


# --- CONSTANTS AND TUNING ----------------------------------------------------
init python:
    import math

    try:
        import pygame_sdl2 as bio_pg
    except Exception:
        bio_pg = None

    BIO_SOUP_IMG = INV_DIR + "hyperspace.png"
    BIO_SPRITE = INV_DIR + "biography.png"          # 1023 x 1537, holds its own glaive
    BIO_GLAIVE = INV_DIR + "glaive_biography.png"   # 174 x 228, SPECTRAL COPIES ONLY
    # The party member's thrown daggers. Shipped pixel art borrowed from
    # Kotonoha mode (9x15, resting point-up), tinted so it reads as yours.
    # Bullet art lives in the shared assets/bullets/ (see def_bullets.rpy).
    BIO_DAGGER = EMB_DIR + "dagger.png"

    BIO_SPRITE_W, BIO_SPRITE_H = 1023, 1537

    # The glaive art rests on the anti-diagonal: shaft up-left, blade
    # down-right. Rotation is therefore `heading - REST`.
    BIO_GLAIVE_REST_DEG = 45.0
    BIO_GLAIVE_ZOOM = 1.1
    BIO_DAGGER_REST_DEG = -90.0                     # the art points up
    BIO_DAGGER_ZOOM = 1.7

    BIO_ROT_STEP = 3.0
    BIO_ROT_BUCKETS = int(round(360.0 / BIO_ROT_STEP))

    BIO_BOSS_ZOOM_ACT1 = 0.30

    # --- ACT ONE STANDS ON THE STAGE (Oct 2 2026) ---------------------------
    # The bout is fought on the same boards as act two, unlit, from a low
    # camera: a horizon at chest height instead of act two's high proscenium.
    # BIO_A1_FIGURE is where its FEET stand on screen. The tear climbs the
    # camera to act two's horizon and lights the boards from those feet.
    BIO_A1_FIGURE = (640.0, 534.0)
    BIO_A1_HORIZON = 300.0
    BIO_A1_FLOORK = 394.0
    BIO_A1_CHEST = 300.0            # feet minus this is the chest, roughly
    inv_fx_register(INV_DIR + "glaive_biography.png", 174, 228)
    # Multiplied by perspective at draw time, so this is its size DOWNSTAGE.
    # It was small enough upstage that the warp shader ate the whole figure.
    BIO_BOSS_ZOOM_ACT2 = 0.27

    # The player's heart. 12x10 pixel art, so the zoom is large and `nearest`
    # keeps it crisp; the warp is deliberately far past what any Archivist
    # gets, because the thing standing in for you should look worst of all.
    BIO_HEART_ZOOM = 2.6
    # Toned down: at 2.6 warp the avatar was the busiest object on screen and
    # you could lose track of your own position in the noise. Enough to look
    # wrong, not enough to hide.
    BIO_HEART_WARP = 1.15

    # --- balance: act one ----------------------------------------------------
    BIO_HP_MAX = 260
    BIO_PP_MAX = 40
    BIO_BOSS_HP_MAX = 1000
    BIO_SHIFT_HP = 520
    BIO_LAST_PAGE_HP = 180
    BIO_SHIFT_TURN_CAP = 15
    # THE CORRUPTIVE STATE STARTS YOU WHOLE. Act one is hyper-aggressive on
    # purpose, so by the threshold the counter is usually near the floor --
    # and act two is a different game with a different defence. Carrying the
    # wreckage across meant the second half was lost before it began, so the
    # shift hands the counter all of it back and lets it roll up on screen.
    BIO_SHIFT_RESET = True

    BIO_BASH_LO, BIO_BASH_HI = 46, 61
    BIO_CRIT_CHANCE = 0.125
    BIO_CRIT_MULT = 2.4
    BIO_MEND_PP, BIO_MEND_HEAL = 8, 78
    BIO_REFUSE_PP, BIO_REFUSE_DMG = 12, 96
    BIO_CHECK_PP_GAIN = 4
    BIO_DEFEND_PP_GAIN = 7
    BIO_GUARD_MULT = 0.45
    BIO_READ_MULT = 0.60

    # --- balance: act two ----------------------------------------------------
    BIO_ARENA = (72, 186, 1208, 664)        # x0, y0, x1, y1
    BIO_PLR_SPEED = 4.0
    BIO_PLR_HIT_R = 9.0

    # THE DASH. Held, not tapped: it runs for as long as the key is down up to
    # a hard ceiling, then a fixed cooldown -- so a wide hazard is answered by
    # committing to a long dash, and there is a real cost to spending it early.
    # Invulnerability covers the whole dash plus a grace tail.
    BIO_DASH_SPEED = 10.5
    BIO_DASH_MAX = 30
    BIO_DASH_MIN = 8
    BIO_DASH_GRACE = 7
    BIO_DASH_CD = 46
    BIO_DASH_STEER = 0.16                   # how sharply a dash can be aimed

    # THE DAGGERS. There are FOUR of them and that is all there is. A dagger
    # is a physical object in exactly one of three states -- in your hand, in
    # the air, or lying on the boards where it came to rest -- so the fight has
    # no fire rate to hide behind. Throwing is spending; getting them back
    # means walking to where they landed, and where they landed is wherever the
    # Archivist was standing.
    #
    # THIS IS THE WHOLE ANSWER TO SPRAY-AND-PRAY. There is no cooldown long
    # enough to stop someone holding a button; there is no way at all to hold a
    # button when the ammunition is on the floor next to the thing swinging at
    # you.
    BIO_DAGGER_COUNT = 4
    BIO_DAGGER_CD = 11                      # between throws, not between hits
    BIO_DAGGER_V0 = 12.4                    # launch speed
    BIO_DAGGER_DRAG = 0.981                 # per tick -- gives a ~470px reach
    BIO_DAGGER_STOP = 3.4                   # below this it drops and sticks
    BIO_DAGGER_TURN = 2.0                   # a guided lob, NOT a lock-on
    BIO_DAGGER_SCATTER = 8.0
    BIO_DAGGER_FLIGHT = 150                 # hard ceiling, safety only
    BIO_PICKUP_R = 40.0                     # walk over it, no key press

    # DAMAGE IS IMPACT SPEED. A dagger sheds speed the whole way, so what it
    # does on arrival is what it had left -- which makes the distance you were
    # standing at the number that matters, and it is legible on screen because
    # you can watch the thing slow down.
    # CHIP IS NOT MEANT TO BE INVISIBLE. It was 3, which put a "3" on screen
    # for a throw that had just cost a run into the blade -- and since the
    # POISE it took was drawn only as a thin arc on the floor, the loop read
    # as doing nothing at all. See _dagger_hit: the number that floats is now
    # the poise figure, and this one moves the bar enough to be seen.
    BIO_DAGGER_DMG = 7                      # chip, at launch speed
    BIO_DAGGER_DMG_OPEN = 15                # into a buckled Archivist
    # AGGRESSION IS THE HEAL. A bot takes ~0.24 hits a second no matter what
    # it does, so the fight costs far more health than the bar holds and the
    # only thing that closes the gap is the burst window paying for itself. A
    # buckle worth five daggers hands back about a tenth of the bar; a player
    # who never takes one gets nothing at all. It was 9 briefly and the bot
    # stopped being able to die -- 8/8 finishing with two thirds of its health.
    BIO_DAGGER_HEAL = 5
    BIO_SPEED_FLOOR = 0.30                  # a long throw still counts a little
    BIO_HURT_IFRAMES = 58

    # What each thing on the stage costs. These were priced for the old fight,
    # where you could answer everything from the back of the stage; the rebuild
    # requires you to stand at 110-150 units, which is the dead centre of the
    # blade's own annulus, so the same numbers turned close range into a
    # blender. Roughly a third off, and see BIO_MOVE_HIT_CAP below -- lowering
    # the numbers alone would not have fixed it.
    BIO_DMG_SWEEP = 21
    BIO_DMG_TWIRL = 17
    BIO_DMG_THRUST = 29
    BIO_DMG_RING = 19
    BIO_DMG_BAR = 21
    BIO_DMG_COPY = 19
    BIO_DMG_ORBIT = 16

    # ONE ATTACK MAY NOT DELETE YOU. A twirl runs 150 ticks with two arms
    # sweeping at up to 15 degrees a tick; against 46 ticks of invulnerability
    # that is FOUR separate hits from a single move, and standing in the band
    # the fight now requires you to stand in cost a third of the bar per
    # attack. Sustained hazards are capped: a sweep, twirl, thrust or orbit
    # gets at most this many hits on you, however long you spend inside it.
    # Rings, bars and thrown copies are discrete and already hit once each.
    BIO_MOVE_HIT_CAP = 2

    # A dagger that connects DEFLECTS and carries on -- it does not drop
    # obediently at your target's feet. Measured: dropping them at the point of
    # impact made the buckle window a free re-arm (a bot cleared 260 damage in
    # one, and the whole fight in two), because the ammunition was always
    # exactly where the next throw wanted to be thrown from.
    BIO_DAGGER_KICK = 110.0
    BIO_DAGGER_SPREAD = 28.0

    # POISE, AND THE BUCKLE. Health is not what a dagger takes first. While the
    # Archivist is composed it barely notices one -- what a hit costs it is
    # POISE, and poise only really goes while it is COMMITTED to something
    # (winding or swinging), which is exactly when standing near it is worst.
    # Run poise out and it BUCKLES: it stops, drops what is in it, and for that
    # window alone a dagger does real damage.
    #
    # So the exposure is EARNED. It used to be handed over 31% of every cycle
    # for free -- recovery frames plus the whole of its throw -- which is why
    # 520 health went down in under twenty seconds to a player who never moved.
    #
    # AND EVERY PAGE COSTS MORE THAN THE LAST. Poise does not reset to what it
    # was, it resets HIGHER -- it is further through the entry each time, and
    # it has seen this done to it before. That is the escalation that gives
    # act two a shape: the first break takes about eight seconds of work, the
    # fifth takes closer to twenty, and the player is worse off by then.
    BIO_POISE_MAX = 155.0
    BIO_POISE_GROWTH = 0.18                 # per buckle already taken
    BIO_POISE_GROWTH_CAP = 2.6
    BIO_POISE_HIT = 15.0                    # doubled if it is committed
    BIO_POISE_COMMIT_MULT = 2.0
    # REGENERATION IS THE THING THAT MAKES A HIT FEEL LIKE NOTHING. At 0.50 a
    # tick while idle it was clawing back ~135 poise per cycle -- more than
    # half the pool -- so breaking it took thirteen or fourteen daggers and
    # three separate retrieval trips, and no single throw could be felt. It is
    # a fifth of that now: the pool is what you are fighting, not the trickle.
    BIO_POISE_REGEN_IDLE = 0.16
    BIO_POISE_REGEN = 0.05
    BIO_POISE_REGEN_RECOVER = 0.05
    BIO_BUCKLE_LEN = 96

    # THE ENTRY. It is not trying to kill you, it is trying to finish writing
    # you down, and it can do that from anywhere you are not. The bar fills on
    # its own, fills FASTER the further away you keep yourself, stops dead
    # while it is buckled, and is knocked back every time you break it open or
    # slip past a blade. Fill it and the entry is finished, which is a loss
    # with your health bar still full.
    #
    # Modelled: engaged play adds ~0.010/tick against 15 knocked off per
    # buckle, so it never threatens a fight that is being fought. Keeping the
    # length of the stage between you is ~0.030/tick -- 56 seconds, and nothing
    # to show for them. A player who dodges perfectly and never commits has
    # about two minutes, which is the only population this bar is aimed at:
    # the health clock already kills anyone who is simply standing still.
    BIO_ENTRY_MAX = 100.0
    BIO_ENTRY_RATE = 0.018
    BIO_ENTRY_NEAR = 260.0
    BIO_ENTRY_FAR = 760.0
    BIO_ENTRY_BUCKLE = 15.0
    BIO_ENTRY_GRAZE = 1.2

    # THE CAMERA IS A BODY. Not a shake -- a damped spring on four axes (roll,
    # two pans, focal length) with a slow unrest driving it and an impulse on
    # every heavy thing that happens. Nausea that obeys a physical model reads
    # as a room you are standing in; nausea made of noise reads as a bug.
    BIO_CAM_ROLL_MAX = 4.6                  # degrees
    BIO_CAM_PAN_MAX = 30.0                  # pixels
    BIO_CAM_ZOOM_LO, BIO_CAM_ZOOM_HI = 0.955, 1.075
    BIO_CAM_K = 0.014                       # spring constant
    BIO_CAM_DAMP = 0.90

    # --- THE STAGE CAMERA ----------------------------------------------------
    # Act two's arena was always a flat plane; nothing about the simulation
    # changes to put a camera on it. World y is DEPTH (small = upstage, far),
    # and only rendering is projected -- so every hitbox, pattern, spacing
    # rule and balance figure verified for the top-down version still holds
    # exactly.
    #
    # Deliberately NOT Horror's camera. Horror is a corridor you flee down
    # with the vanishing point in your face and no way to reach it. This is a
    # STAGE: a fixed proscenium you circle on, where closing the distance is
    # the whole job. 1/persp is linear in depth, which is what makes rows
    # bunch up toward the horizon instead of sliding by at a constant rate.
    BIO_CAM_HORIZON = 182.0
    BIO_CAM_FLOOR = 694.0
    BIO_PERSP_NEAR = 1.00          # downstage edge
    BIO_PERSP_FAR = 0.58           # upstage edge
    BIO_FLOOR_K = (BIO_CAM_FLOOR - BIO_CAM_HORIZON) / BIO_PERSP_NEAR

    BIO_BOSS_HURT_R = 74.0
    # THE BLADE RIDES AT HAND HEIGHT, NOT ANKLE HEIGHT. The hitbox is a
    # footprint on the floor (that is what you dodge, and it is drawn there),
    # but the WEAPON has to be drawn where a swung polearm would actually be
    # or the swing reads as happening at the Archivist's feet -- dissonant,
    # and it feels like a cheat when it connects. Screen lift is scaled by
    # perspective, same as everything else standing on the boards.
    BIO_BLADE_LIFT = 190.0

    # THE POCKET. A polearm cannot hit what is inside its own haft, and at 44
    # that pocket was too small to aim for, so close range was all cost and no
    # technique. At 68 there is somewhere to BE: the very close is under the
    # swing, the middle distance is where the blade lives, and getting from one
    # to the other is the skill. It is not a free ride -- rings spawn at its
    # feet and the thrust starts there.
    BIO_BLADE_INNER = 68.0
    BIO_BLADE_OUTER = 248.0
    BIO_BLADE_ARC = 15.0

    # RULE 5: no two dash-answerable hazards closer together than BIO_DASH_CD.
    BIO_RING_GAP = 62                       # ticks between shockwave rings
    BIO_RING_SPEED = 3.6
    BIO_RING_WIDTH = 34.0
    BIO_RING_WARN = 30                      # telegraph before it starts moving
    BIO_COPY_GAP = 48                       # ticks between thrown copies
    BIO_BAR_GAP = 54                        # ticks between recital lines
    BIO_BAR_SPEED = 3.4
    BIO_BAR_WARN = 30

    # --- palette -------------------------------------------------------------
    BIO_INK = "#f2f4ff"
    BIO_DIM = "#8f96b4"
    BIO_FAINT = "#5d6580"
    BIO_RED = "#ff2d4e"
    BIO_RED_DEEP = "#7c0f22"
    BIO_WARN = "#ffcf5c"
    BIO_TEAL = "#5ce8d0"
    BIO_BLACK = "#04030a"

    # THE ONLY STRINGS IN THIS FIGHT. Controls, numbers and state words. If
    # you are about to add a sentence here, read rule 1 at the top of the file.
    BIO_CMDS = (("bash", "BASH"), ("recall", "RECALL"),
                ("defend", "DEFEND"), ("run", "RUN"))
    BIO_RECALLS = (("mend", "MEND", BIO_MEND_PP),
                ("refuse", "REFUSE", BIO_REFUSE_PP),
                ("check", "CHECK", 0))


# --- SIMULATION --------------------------------------------------------------
init python:
    class BIOGame(object):
        """All of Biography's live state, stepped at a fixed 60Hz by BIOStage.
        Owns zero rendering."""

        def __init__(self, retry=False, deaths=0, debug=False, start_open=False,
                     resume=None):
            self.result = None
            self.paused = False
            self.debug = bool(debug)
            self.retry = bool(retry)
            self.deaths = int(deaths)
            self.god = inv_godmode_on()
            # A loss in act two can be retried FROM THE TEAR. Biography carries
            # nothing across it but the fact of having got there, so the
            # checkpoint is just that fact.
            self.checkpoint = None
            if resume:
                start_open = True

            self.tick = 0
            self.clock = 0.0
            self.rush = 0.0
            self.spin = 0.0             # integrated rotation of the whole room
            self.rng = inv_random.Random()

            # --- presentation (Oct 2 2026) ----------------------------------
            # Everything below is DECORATION owned by the sim, so a paused
            # fight freezes it and every frame stays a pure function of state.
            self.fx = InvFX(cap=440)
            self.turn_log = []
            self.stage_lit = 1.0 if start_open else 0.0
            self.wave = [0.0, 0.0]          # floor wave: radius, strength
            self.shock = [640.0, 360.0, 0.0, 0.0]   # lens shockwave
            self.ca = 0.0                   # aberration spike
            self.tear = 0.0                 # lens row tear
            self.scan = -1.0                # CHECK's reading band, -1 = off
            self.panel_kick = 0.0           # the status window taking a hit
            self.react = 0.0                # the figure's knockback (px)
            self.reactv = 0.0
            self.windup = 0.0               # act-one enemy telegraph glow
            self.windup_col = "#ff2d4e"
            self.bar_reveal = 1.0 if start_open else 0.0
            self.boss_flash = 0.0           # the BODY's hurt flash (not yours)
            self.shock_world = False
            self.pending_move = None        # act one: picked at the wind-up
            # Decoration draws from its OWN stream. Motes, bubbles and debris
            # respawn constantly, and pulling those numbers out of the same
            # generator the fight uses means the fight is no longer reproducible
            # from a seed -- which quietly cost a whole round of harness results
            # that looked like a balance swing and were noise.
            self.rng_fx = inv_random.Random()

            # --- party member ------------------------------------------------
            self.hp = BIO_HP_MAX
            self.hp_shown = float(BIO_HP_MAX)
            self.pp = BIO_PP_MAX
            self.pp_shown = float(BIO_PP_MAX)
            self.roll_cue = 0

            # --- the Archivist -----------------------------------------------
            self.boss_hp = BIO_BOSS_HP_MAX
            self.boss_shown = float(BIO_BOSS_HP_MAX)
            self.boss_known = False

            # --- act one -------------------------------------------------------
            self.mode = "arrive"
            self.mtick = 0
            self.turn = 0
            self.cursor = 0
            self.sub_cursor = 0
            self.guard = False
            self.read = False
            self.bleed = 0
            self.telegraph = False
            self.last_enemy = None

            # The one-line mechanical readout. Never a sentence; never
            # auto-advances (rule 1, and nobody gets left behind).
            self.beat_label = ""
            self.beat_value = ""
            self.beat_after = "menu"

            # --- presentation ----------------------------------------------------
            self.flash = 0.0
            self.jolt = 0.0
            self.dark = 1.0
            self.shake = 0.0
            self.freeze = 0
            self.corrupt = 1.0 if start_open else 0.0
            # 1.0, not 0.0: the panels start OFF the bottom of the screen
            # and slide up once the bout actually begins (see _step_ambient).
            # They used to exist from frame one and simply go undrawn during
            # the arrival, which meant they appeared whole on a single frame,
            # at the same instant the body took its place -- one pop reading as
            # two things going wrong at once.
            self.panel_slide = 1.0
            self.boss_pose = 0.0
            self.hit_flash = 0.0
            self.floats = []
            self.motes = self._make_motes()
            self.bubbles = self._make_bubbles()
            self.debris = self._make_debris()

            # The camera body. cam_amt gates the whole thing off in act one,
            # where the fight is held in windows and a rolling frame would only
            # make the panels hard to read.
            self.cam_amt = 1.0 if start_open else 0.0
            self.cam_roll = 0.0
            self.cam_rollv = 0.0
            self.cam_px = 0.0
            self.cam_pxv = 0.0
            self.cam_py = 0.0
            self.cam_pyv = 0.0
            self.cam_zoom = 1.0
            self.cam_zoomv = 0.0
            self.fury = 0.0

            # The wormhole: (x, y, radius, strength). Strength 0 means closed.
            self.hole = [640.0, 330.0, 250.0, 0.0]
            self.hole_wx = 640.0
            self.hole_wy = 330.0
            self.emerge = 1.0 if not start_open else 0.0   # 1 = not through yet
            self.body_scale = 1.0
            # Captured at _begin_leave so the ending lerps from where the
            # fight actually stopped; defaulted here so the attributes always
            # exist even if something reaches the ending by an odd path.
            self.leave_rot0 = 0.0
            self.leave_scale0 = 1.0
            self.leave_by0 = 0.0
            self.body_sx = 1.0
            self.body_sy = 1.0

            # --- act two ---------------------------------------------------------
            ax0, ay0, ax1, ay1 = BIO_ARENA
            self.px = (ax0 + ax1) * 0.5
            self.py = ay1 - 90.0
            self.face = -90.0
            self.dash_t = 0
            self.dash_cd = 0
            self.dash_dir = -90.0
            self.dashing = False
            self.iframe = 0
            self.fire_cd = 0
            self.trail = []
            # FOUR daggers, for the whole fight. Each one is a dict that
            # changes state rather than a spawn that gets destroyed, so the
            # count on screen is always exactly BIO_DAGGER_COUNT and the player
            # can find every one of them.
            self.daggers = [{"state": "held", "x": 0.0, "y": 0.0, "ang": 0.0,
                            "spd": 0.0, "t": 0, "rest": 0.0}
                            for _d in range(BIO_DAGGER_COUNT)]
            self.pickup_cue = 0

            self.bx = (ax0 + ax1) * 0.5
            self.by = ay0 + 150.0
            self.bvx = 0.0
            self.bvy = 0.0
            self.ghosts = []
            self.b_state = "idle"
            self.b_move = None
            self.b_t = 0
            self.b_hits = 0
            self.b_len = 60
            self.b_idle = 46
            self.blade = 0.0
            self.blade_prev = 0.0
            self.wind_from = 0.0
            self.wind_to = 0.0
            self.blade_arc = []
            self.body_rot = 0.0
            self.aim = 90.0
            self.bag = []
            self.wander = (self.bx, self.by)
            self.hazards = []
            # Discharge FX: purely cosmetic lightning, owned by the sim so it
            # freezes with everything else on pause. See _spawn_arc.
            self.arcs = []
            self.last_page = False
            self.graze_cd = 0
            self.beat = 0.0
            self.beat_pulse = 0.0
            self.hits_taken = 0
            self.punishes = 0

            self.poise = BIO_POISE_MAX
            self.poise_shown = BIO_POISE_MAX
            self.buckles = 0
            self.entry = 0.0
            self.entry_shown = 0.0
            self.entry_cue = 0
            self.chain = 0

            self.keys = MSBFKeyLatch()
            self._prev = {"left": False, "right": False, "up": False,
                        "down": False, "z": False, "x": False}

            if start_open:
                self.boss_hp = BIO_SHIFT_HP
                self.boss_shown = float(BIO_SHIFT_HP)
                self.boss_known = True
                self.panel_slide = 1.0
                self.dark = 0.0
                self.mode = "open"
                self.checkpoint = {"slug": "biography"}
                if resume:
                    # Back in through the tear: a beat of black, then the
                    # stage comes up lit from its feet.
                    self.dark = 1.0
                    self.wave = [0.0, 1.0]
                    self.iframe = 70
                inv_music_corruptive()

        # ----- tiny helpers ---------------------------------------------------

        def play(self, name, volume_scale=1.0):
            inv_play(name, volume_scale)

        def toggle_pause(self):
            if self.result is None:
                self.paused = not self.paused
                self.play("cancel" if self.paused else "confirm", 0.6)

        def give_up(self):
            if self.result is None:
                self.result = "quit"

        def toggle_god(self):
            if not config.developer:
                return
            inv_toggle_godmode()
            self.god = inv_godmode_on()
            self.play("scan", 0.7)
            renpy.notify("GODMODE " + ("ON" if self.god else "OFF"))

        def boss_frac(self):
            return inv_clamp(self.boss_hp / float(BIO_BOSS_HP_MAX), 0.0, 1.0)

        def in_act_two(self):
            return self.corrupt > 0.5

        def _beat(self, label, value="", after="enemy", kind="you"):
            """Queue the mechanical readout for one resolved action -- and log
            it, because the beat no longer waits for a key: the line stays in
            the turn log until the next turn pushes it down."""
            self.beat_label = label
            self.beat_value = value
            self.beat_after = after
            self.mode = "beat"
            self.mtick = 0
            if value or label:
                inv_log_push(self, label, value, kind)

        # ----- ambience -------------------------------------------------------

        def _make_motes(self):
            motes = []
            for _i in range(64):
                motes.append({
                    "x": self.rng_fx.uniform(-40, 1320),
                    "y": self.rng_fx.uniform(-40, 760),
                    "z": self.rng_fx.uniform(0.25, 1.0),
                    "s": self.rng_fx.choice((2, 2, 3, 4, 5)),
                    "p": self.rng_fx.uniform(0.0, 6.28),
                })
            return motes

        def _make_bubbles(self):
            bubbles = []
            for _i in range(9):
                bubbles.append({
                    "x": self.rng_fx.uniform(60, 1220),
                    "y": self.rng_fx.uniform(0, 720),
                    "r": self.rng_fx.uniform(28, 96),
                    "v": self.rng_fx.uniform(0.25, 0.75),
                    "p": self.rng_fx.uniform(0.0, 6.28),
                })
            return bubbles

        def _make_debris(self):
            """Matter that is actually IN the room rather than painted over it.

            The motes above are screen-space confetti -- fine behind act one's
            windows, but drifting across a stage they read as dirt on the lens
            and flatten the whole thing back out. Debris has a world position,
            a HEIGHT off the boards and a velocity, so it is projected and
            depth-sorted with the bodies: it passes behind the Archivist, it
            swells as it comes downstage, and the pieces that get close blow
            past the camera. That is where the volume comes from.
            """
            ax0, ay0, ax1, ay1 = BIO_ARENA
            out = []
            for _i in range(44):
                out.append(self._respawn_debris({
                    "x": self.rng_fx.uniform(ax0 - 300, ax1 + 300),
                    "y": self.rng_fx.uniform(ay0 - 60, ay1 + 120),
                }, fresh=False))
            return out

        def _respawn_debris(self, d, fresh=True):
            ax0, ay0, ax1, ay1 = BIO_ARENA
            if fresh:
                d["x"] = self.rng_fx.uniform(ax0 - 340, ax1 + 340)
                d["y"] = self.rng_fx.uniform(ay0 - 90, ay0 + 120)
            d["h"] = self.rng_fx.uniform(-30.0, 340.0)
            d["vx"] = self.rng_fx.uniform(-0.5, 0.5)
            d["vy"] = self.rng_fx.uniform(0.55, 2.30)
            d["vh"] = self.rng_fx.uniform(-0.85, 0.55)
            d["s"] = self.rng_fx.choice((3, 4, 4, 5, 7, 10))
            d["p"] = self.rng_fx.uniform(0.0, 6.2831853)
            d["w"] = self.rng_fx.uniform(0.4, 1.0)
            return d

        def _step_ambient(self):
            self.tick += 1
            self.clock += INV_TICK
            self.rush += INV_TICK * (0.55 + 1.15 * self.corrupt)

            # THE PANELS SEAT THEMSELVES once the bout begins. Guarded to the
            # act-one modes on purpose: the shift drives this same value the
            # other way (0 -> 1) to throw the panels off the screen, and a
            # decay running underneath that would fight it.
            if self.mode in ("menu", "beat", "enemy") and self.panel_slide > 0.0:
                self.panel_slide = max(0.0, self.panel_slide - 0.042)


            # Rotational momentum, integrated rather than derived from the
            # clock: the rate swells and slackens (and act two turns harder),
            # and a wormhole drags the entire room around itself while it is
            # open -- none of which may jump the angle when it changes.
            spin_rate = ((0.20 + 0.34 * self.corrupt)
                        * (0.55 + 0.45 * math.sin(self.clock * 0.13)))
            spin_rate += 0.95 * self.hole[3]
            self.spin += INV_TICK * spin_rate

            # FURY: how far through the fight it is, by whichever of the two
            # clocks is running hotter -- the health it has lost or the entry
            # it has written. The room leans on it (see u_bio_fury), the
            # camera's unrest scales with it, and the debris runs faster.
            prog = inv_clamp((BIO_SHIFT_HP - self.boss_hp)
                            / float(max(1, BIO_SHIFT_HP)), 0.0, 1.0)
            ent = inv_clamp(self.entry / BIO_ENTRY_MAX, 0.0, 1.0)
            self.fury = inv_lerp(self.fury,
                                self.corrupt * inv_clamp(
                                    0.14 + 0.86 * max(prog, ent), 0.0, 1.0),
                                0.02)

            self.beat += 1.0 / INV_BEAT_TICKS
            if self.beat >= 1.0:
                self.beat -= 1.0
                self.beat_pulse = 1.0
            self.beat_pulse *= 0.86

            self.flash *= 0.86
            self.jolt *= 0.82
            self.shake *= 0.88
            self.hit_flash *= 0.88

            # --- presentation state (decoration; owned here, see __init__) --
            self.fx.step()
            self.boss_flash *= 0.84
            self.ca *= 0.86
            self.tear *= 0.88
            self.panel_kick *= 0.84
            self.windup *= 0.94
            if self.shock[3] > 0.004:
                self.shock[2] += 16.0 + self.shock[2] * 0.05
                self.shock[3] *= 0.90
            else:
                self.shock[3] = 0.0
            if self.wave[1] > 0.004:
                self.wave[0] += 9.0
                self.wave[1] *= 0.975
            else:
                self.wave[1] = 0.0
            if self.scan >= 0.0:
                self.scan += 0.020
                if self.scan > 1.25:
                    self.scan = -1.0
            if self.boss_known and self.bar_reveal < 1.0:
                self.bar_reveal = min(1.0, self.bar_reveal + 0.035)
            # The figure's knockback is a spring: hit, overshoot, settle.
            self.reactv += -self.react * 0.16
            self.reactv *= 0.78
            self.react += self.reactv
            want_lit = 1.0 if self.corrupt > 0.5 else 0.0
            self.stage_lit = inv_approach(self.stage_lit, want_lit, 0.012)
            if self.dark > 0.0 and self.mode == "open" and self.mtick < 60:
                self.dark = max(0.0, self.dark - 0.03)

            speed = 1.0 + 2.4 * self.corrupt
            for m in self.motes:
                m["y"] += (0.35 + 1.9 * m["z"]) * speed
                m["x"] += math.sin(self.clock * 0.7 + m["p"]) * 0.45 * m["z"]
                if m["y"] > 764:
                    m["y"] = -40
                    m["x"] = self.rng_fx.uniform(-40, 1320)
            for b in self.bubbles:
                b["y"] -= b["v"] * (0.6 + 1.2 * self.corrupt)
                b["r"] += math.sin(self.clock * 0.9 + b["p"]) * 0.12
                if b["y"] + b["r"] < -20:
                    b["y"] = 760 + b["r"]
                    b["x"] = self.rng_fx.uniform(60, 1220)

            self._step_debris()
            self._step_camera()
            self._step_arcs()

            # AMBIENT CRACKLE. The soup discharges on its own, and it does it
            # harder the further along the fight is (fury), so the room gets
            # visibly less settled as the Archivist gets closer to finishing.
            # Rare and short by design -- this is weather, not an attack.
            # (corrupt > 0.5 == act two; act one is the windowed bout, which
            # has no world for a bolt to cross.)
            if self.corrupt > 0.5:
                if self.rng_fx.random() < 0.010 + 0.030 * self.fury:
                    _ax0, _ay0, _ax1, _ay1 = BIO_ARENA
                    self._spawn_arc(
                        self.rng_fx.uniform(_ax0 - 60, _ax1 + 60),
                        self.rng_fx.uniform(_ay0 - 40, _ay1),
                        self.rng_fx.uniform(0.0, 6.2831853),
                        self.rng_fx.uniform(230, 460),
                        ttl=self.rng_fx.randint(5, 9),
                        width=self.rng_fx.uniform(0.75, 1.1),
                        h=self.rng_fx.uniform(10.0, 190.0))

            self.poise_shown = inv_lerp(self.poise_shown, self.poise, 0.22)
            self.entry_shown = inv_lerp(self.entry_shown, self.entry, 0.14)

            for attr, real in (("hp_shown", self.hp), ("pp_shown", self.pp),
                            ("boss_shown", self.boss_hp)):
                shown = getattr(self, attr)
                gap = abs(shown - real)
                if gap > 0.01:
                    rate = inv_clamp(gap * 0.02, 0.25, 1.7)
                    setattr(self, attr, inv_approach(shown, float(real), rate))
                    if attr == "hp_shown":
                        self.roll_cue += 1
                        if self.roll_cue % 7 == 0:
                            self.play("roll", 0.5)
                else:
                    setattr(self, attr, float(real))

            for f in self.floats:
                # A world-space number drifts UPSTAGE, which is a much smaller
                # move on screen, so it rises at a fraction of the rate.
                f["y"] += f["vy"] * (0.35 if f.get("world") else 1.0)
                f["vy"] += 0.055
                f["life"] -= 1
            self.floats = [f for f in self.floats if f["life"] > 0]

            # Ghost trail of the body, for anything moving fast.
            if self.mode == "open":
                sp = math.hypot(self.bvx, self.bvy)
                if sp > 2.4 or self.b_state == "act":
                    self.ghosts.insert(0, (self.bx, self.by, self.body_rot,
                                        self.body_scale))
                    if len(self.ghosts) > 6:
                        self.ghosts.pop()
                elif self.ghosts:
                    self.ghosts.pop()

            if self.hp_shown <= 0.0 and self.mode not in ("leave_w", "leave_l",
                                                        "arrive"):
                self._begin_leave(False)

        # ----- the room as a volume -------------------------------------------

        def _step_debris(self):
            """Suspended matter, integrated in WORLD space.

            The soup turns, so the matter in it turns with it: a slow swirl
            about the middle of the stage plus each piece's own drift. Nothing
            here is a constant added to a coordinate (rule 3 applies to the
            room, not only to the body) and nothing is culled at the edge of
            the screen -- pieces run all the way downstage and past the lens.
            """
            if self.corrupt < 0.35:
                return
            ax0, ay0, ax1, ay1 = BIO_ARENA
            midx = (ax0 + ax1) * 0.5
            midy = (ay0 + ay1) * 0.5
            rush = 0.55 + 1.25 * self.fury
            swirl = 0.0016 * (0.5 + 0.5 * math.sin(self.clock * 0.17))
            for d in self.debris:
                # Swirl: a tangential nudge about the middle of the boards, so
                # the whole volume shares the room's rotation.
                rx = d["x"] - midx
                ry = (d["y"] - midy) * 2.2       # depth is short, so weight it
                d["vx"] += -ry * swirl
                d["vy"] += rx * swirl * 0.22

                d["vx"] += math.sin(self.clock * 0.8 + d["p"]) * 0.035
                d["vh"] += math.sin(self.clock * 0.53 + d["p"] * 1.7) * 0.022
                d["vx"] *= 0.995
                d["vy"] *= 0.997
                d["vh"] *= 0.992

                d["x"] += d["vx"] * rush
                d["y"] += d["vy"] * rush
                d["h"] += d["vh"] * rush

                if (d["y"] > ay1 + 420 or d["h"] < -140.0 or d["h"] > 700.0
                        or not (ax0 - 900 < d["x"] < ax1 + 900)):
                    self._respawn_debris(d)

        def _step_camera(self):
            """A damped spring on roll, both pans and focal length.

            Every heavy event in the fight pushes it (see cam_kick) and it
            settles on its own; underneath, a slow unrest keeps it from ever
            being level. It is gated by cam_amt so act one is shot flat.
            """
            want = 1.0 if self.mode in ("open", "shift") else (
                0.35 if self.mode in ("leave_w", "leave_l") else 0.0)
            if self.mode == "shift":
                want = inv_clamp((self.mtick - 90) / 100.0, 0.0, 1.0)
            self.cam_amt = inv_lerp(self.cam_amt, want, 0.03)

            t = self.clock
            unrest = 0.35 + 0.65 * self.fury
            # Three incommensurate rates per axis, so the drift never repeats
            # inside a fight and the eye cannot learn it.
            t_roll = (math.sin(t * 0.23) * 0.55 + math.sin(t * 0.41 + 1.9) * 0.30
                    + math.sin(t * 0.09 + 0.4) * 0.45) * BIO_CAM_ROLL_MAX * unrest
            t_px = (math.sin(t * 0.19 + 2.3) * 0.6
                    + math.sin(t * 0.37) * 0.35) * BIO_CAM_PAN_MAX * unrest
            t_py = (math.sin(t * 0.27 + 1.1) * 0.5
                    + math.sin(t * 0.13 + 4.0) * 0.4) * BIO_CAM_PAN_MAX * 0.55 * unrest
            t_zoom = 1.0 + (math.sin(t * 0.21 + 0.7) * 0.026
                            + math.sin(t * 0.47) * 0.014) * (0.4 + 0.6 * self.fury)
            # It frames the fight as well as wobbling in it: a gentle lean
            # toward whatever is between the two bodies.
            if self.mode == "open":
                t_px += inv_clamp(((self.bx + self.px) * 0.5 - 640.0) * 0.045,
                                -34.0, 34.0)
                t_zoom += 0.030 * self.beat_pulse * (0.3 + 0.7 * self.fury)

            for tgt, pos, vel, lo, hi in (
                    (t_roll, "cam_roll", "cam_rollv",
                    -BIO_CAM_ROLL_MAX * 2.2, BIO_CAM_ROLL_MAX * 2.2),
                    (t_px, "cam_px", "cam_pxv",
                    -BIO_CAM_PAN_MAX * 2.6, BIO_CAM_PAN_MAX * 2.6),
                    (t_py, "cam_py", "cam_pyv",
                    -BIO_CAM_PAN_MAX * 1.8, BIO_CAM_PAN_MAX * 1.8),
                    (t_zoom, "cam_zoom", "cam_zoomv",
                    BIO_CAM_ZOOM_LO, BIO_CAM_ZOOM_HI)):
                p = getattr(self, pos)
                v = getattr(self, vel)
                v += (tgt - p) * BIO_CAM_K
                v *= BIO_CAM_DAMP
                p = inv_clamp(p + v, lo, hi)
                setattr(self, pos, p)
                setattr(self, vel, v)

        def cam_kick(self, roll=0.0, px=0.0, py=0.0, zoom=0.0):
            """An impulse into the camera body. Heavy things push it; it
            recovers by itself, which is why a slam reads as weight rather
            than as the screen being rattled at random."""
            self.cam_rollv += roll
            self.cam_pxv += px
            self.cam_pyv += py
            self.cam_zoomv += zoom

        def cam_tuple(self):
            """(roll radians, pan x, pan y, zoom), already gated by cam_amt."""
            a = inv_clamp(self.cam_amt, 0.0, 1.0)
            return (math.radians(self.cam_roll * a),
                    self.cam_px * a, self.cam_py * a,
                    1.0 + (self.cam_zoom - 1.0) * a)

        # ----- damage ---------------------------------------------------------

        def float_text(self, x, y, text, color, big=False):
            # `world` marks a number written in stage coordinates; act one's
            # are already in screen space.
            self.floats.append({"x": x, "y": y, "vy": -1.6, "life": 52,
                                "text": text, "color": color, "big": big,
                                "world": self.mode in ("open", "leave_w",
                                                    "leave_l")})

        def hurt(self, amount, x=None, y=None):
            amount = int(max(0, amount))
            if amount <= 0:
                return
            if not self.god:
                self.hp = int(max(0, self.hp - amount))
            self.hits_taken += 1
            self.jolt = min(1.0, self.jolt + 0.55)
            self.shake = min(1.0, self.shake + 0.7)
            self.hit_flash = 1.0
            self.play("struck" if self.in_act_two() else "hurt")
            if x is not None:
                self.float_text(x, y, "-%d" % amount,
                                BIO_DIM if self.god else BIO_RED, True)
            if self.mode == "open":
                self._fx_world_burst(self.px, self.py, 26.0, "#ff2d4e", 18, True)
                self.fx.burst(INV_SHARDS, self.px, self.py, 6, speed=(2.0, 5.0),
                              life=(16, 30), size=(0.16, 0.30), col="#ff6f86",
                              add=False, drag=0.92, layer="w_front", h=26.0,
                              vh=(1.0, 5.0), ah=-0.25, vrot=(-12.0, 12.0),
                              squash=0.45)
                self._kick_lens(self.px, self.py, 0.6, 0.010, world=True)

        def damage_boss(self, amount, x=None, y=None, big=False, quiet=False):
            """`quiet` takes the health off without printing it -- act two's
            composed hits print their POISE figure instead, which is the thing
            the throw was actually for."""
            amount = int(max(0, amount))
            self.boss_hp = int(max(0, self.boss_hp - amount))
            self.boss_pose = -1.0
            self.boss_flash = 1.0
            if x is not None and not quiet:
                self.float_text(x, y, str(amount), BIO_WARN if big else BIO_INK, big)

        # ----- VFX events (decoration only; nothing here touches a rule) ------
        # Act one is screen space: the figure stands at BIO_A1_FIGURE, the
        # status window is where an attack lands. Act two is WORLD space on
        # the boards (x, depth, height) and the stage projects it.

        def _kick_lens(self, x, y, strength, ca=0.0, world=False):
            self.shock = [float(x), float(y), 8.0, float(strength)]
            self.shock_world = bool(world)
            self.ca = max(self.ca, ca)

        def _fx_cut(self, x, y, big=False):
            """BASH landing: a cut across the figure, sparks, the lens kicked."""
            fx = self.fx
            ang = self.rng_fx.uniform(-38.0, -18.0)
            fx.emit("spark", x, y, life=12 if big else 9, size=3.8 if big else 2.8,
                    size1=4.8 if big else 3.3, rot=ang, col="#ffffff", layer="front",
                    fade="pop")
            if big:
                fx.emit("spark", x, y, life=13, size=3.6, size1=4.6,
                        rot=ang + 78.0, col="#ff8aa0", layer="front", fade="pop")
                fx.emit("flare", x, y, life=20, size=3.4, size1=5.0,
                        col="#ffe3e8", alpha=0.9, layer="front", fade="pop")
            fx.burst("spark", x, y, 26 if big else 14, speed=(5.0, 14.0),
                     life=(10, 22), size=(0.22, 0.50), col="#ffd2da", drag=0.86,
                     stretch=0.11, layer="front", fade="out2")
            fx.burst("spark", x, y, 10 if big else 5, speed=(3.0, 8.0),
                     life=(14, 26), size=(0.18, 0.36), col="#5ce8d0", drag=0.88,
                     stretch=0.11, layer="front")
            fx.burst(INV_SHARDS, x, y, 8 if big else 4, speed=(2.0, 6.5),
                     life=(18, 34), size=(0.20, 0.42), col="#ff6f86", alpha=0.85,
                     add=False, drag=0.93, ay=0.22, vrot=(-14.0, 14.0),
                     layer="front")
            fx.emit("glow", x, y, life=18, size=1.6 if big else 1.1,
                    size1=2.6 if big else 1.7, col="#ff3b5c", alpha=0.85,
                    layer="front", fade="out2")
            self._kick_lens(x, y, 0.9 if big else 0.45, 0.012 if big else 0.006)
            self.reactv += (16.0 if big else 9.0) * (1.0 if self.rng_fx.random() < 0.5 else -1.0)

        def _fx_strike(self, col="#ff2d4e", big=False):
            """An act-one attack ARRIVING: a cut from the figure to the status
            window, which takes the hit. You have no avatar in a windowed
            bout, so the window is what gets struck."""
            fx = self.fx
            x0, y0 = BIO_A1_FIGURE[0], BIO_A1_FIGURE[1] - BIO_A1_CHEST
            x1, y1 = 1004.0, 612.0
            ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
            for i in range(9):
                u = i / 8.0
                fx.emit("spark", inv_lerp(x0, x1, u), inv_lerp(y0, y1, u),
                        life=9, size=2.0 if big else 1.4, rot=ang, col=col,
                        layer="hud", fade="pop", delay=int(i * 0.6))
            fx.burst("spark", x1, y1, 18 if big else 10, speed=(3.0, 11.0),
                     life=(10, 22), size=(0.22, 0.48), col="#ff8a9c",
                     drag=0.86, stretch=0.11, layer="hud", delay=(5, 6))
            fx.emit("glow", x1, y1, life=20, size=2.4, size1=3.6, col=col,
                    alpha=0.75, layer="hud", fade="out2", delay=5)
            self.panel_kick = 1.0
            self._kick_lens(x1, y1, 0.75 if big else 0.4, 0.010 if big else 0.005)

        def _fx_rise(self, col, n=18, x0=1004.0, y0=620.0):
            """Motes rising off the status window -- a mend, a guard."""
            self.fx.burst("dust", x0, y0, n, speed=(0.6, 2.2), life=(30, 60),
                          size=(0.6, 1.4), col=col, drag=0.97, ay=-0.05,
                          angle=-90.0, spread=70.0, jitter=120.0, squash=0.4,
                          layer="hud")
            self.fx.emit("glow", x0, y0, life=26, size=3.4, size1=4.2, col=col,
                         alpha=0.45, layer="hud", fade="inout")

        def _fx_world_burst(self, wx, wy, h, col, n=16, big=False):
            """Act two: a burst on the boards, at a height above them."""
            fx = self.fx
            fx.burst("spark", wx, wy, n, speed=(3.0, 10.0 if big else 7.0),
                     life=(10, 24), size=(0.22, 0.50), col=col, drag=0.87,
                     stretch=0.10, layer="w_front", h=h, vh=(-2.5, 5.5),
                     ah=-0.18, squash=0.45)
            fx.emit("glow", wx, wy, life=16, size=1.4 if big else 0.9,
                    size1=2.4 if big else 1.4, col=col, alpha=0.85,
                    layer="w_front", fade="out2", h=h)

        # ----- input ----------------------------------------------------------

        def _poll_input(self):
            pg = bio_pg
            if pg is None:
                return None
            try:
                keys = pg.key.get_pressed()
            except Exception:
                return None

            blank = {"left": False, "right": False, "up": False,
                    "down": False, "z": False, "x": False}

            if not self.keys.focused():
                self.keys.stuck = set()
                self._prev.update(blank)
                edges = dict((k, False) for k in blank)
                edges["held"] = blank
                return edges

            cur = {
                "left": self.keys.pressed(keys, pg.K_LEFT, pg.K_a),
                "right": self.keys.pressed(keys, pg.K_RIGHT, pg.K_d),
                "up": self.keys.pressed(keys, pg.K_UP, pg.K_w),
                "down": self.keys.pressed(keys, pg.K_DOWN, pg.K_s),
                "z": self.keys.pressed(keys, pg.K_z, pg.K_RETURN, pg.K_KP_ENTER),
                "x": self.keys.pressed(keys, pg.K_x, pg.K_LSHIFT, pg.K_RSHIFT),
            }
            edges = {}
            for k in ("z", "x", "left", "right", "up", "down"):
                edges[k] = cur[k] and not self._prev[k]
                self._prev[k] = cur[k]
            edges["held"] = cur
            return edges

        # ----- the dispatcher -------------------------------------------------

        def step(self):
            edges = self._poll_input() or {
                "z": False, "x": False, "left": False, "right": False,
                "up": False, "down": False,
                "held": {"left": False, "right": False, "up": False,
                        "down": False, "z": False, "x": False},
            }
            self._step_ambient()
            if self.result is not None:
                return

            self.boss_pose = inv_approach(self.boss_pose, 0.0, 0.06)

            mode = self.mode
            if mode == "arrive":
                self._step_arrive()
            elif mode == "menu":
                self._step_menu(edges)
            elif mode == "sub":
                self._step_sub(edges)
            elif mode == "beat":
                self._step_beat(edges)
            elif mode == "enemy":
                self._step_enemy()
            elif mode == "shift":
                self._step_shift()
            elif mode == "open":
                self._step_open(edges)
            elif mode in ("leave_w", "leave_l"):
                self._step_leave()

        # =====================================================================
        # ARRIVAL -- the rupture (rule 4). No text, no warning, three seconds.
        # =====================================================================

        def _step_arrive(self):
            self.mtick += 1
            t = self.mtick

            self.dark = inv_clamp(1.0 - t / 24.0, 0.0, 1.0)

            # 1. the soup tears open at a point and spirals
            if t == 6:
                self.play("tear", 0.9)
            if t < 60:
                self.hole[3] = bio_smooth(t / 60.0)
                self.hole[2] = inv_lerp(40.0, 250.0, bio_smooth(t / 60.0))
                self.jolt = max(self.jolt, 0.25 * (t / 60.0))
            # 2. it is extruded out of the hole, still coming apart
            elif t < 140:
                u = (t - 60) / 80.0
                self.hole[3] = 1.0
                self.emerge = 1.0 - bio_smooth(u)
                # Comes through too tall for the space, then settles.
                self.body_scale = inv_lerp(1.85, 1.0, bio_smooth(u))
                if t == 62:
                    self.play("wind2", 1.0)
                if t == 116:
                    self.play("slam")
                    self.flash = 0.55
                    self.shake = 1.0
                    self.jolt = 0.9
            # 3. the hole shuts behind it
            elif t < 190:
                u = (t - 140) / 50.0
                self.emerge = 0.0
                self.body_scale = 1.0
                self.hole[3] = 1.0 - bio_smooth(u)
                self.hole[2] = inv_lerp(250.0, 30.0, bio_smooth(u))
            elif t == 190:
                self.hole[3] = 0.0
                inv_music_survey()
            elif t >= 226:
                self._begin_player_turn()

        # =====================================================================
        # ACT ONE
        # =====================================================================

        def _begin_player_turn(self):
            # The cursor stays where you left it: repeating a command is the
            # commonest thing a player does, and re-navigating to it every
            # turn was friction with no decision in it.
            self.mode = "menu"
            self.mtick = 0
            self.turn += 1
            self.guard = False

        def _step_menu(self, edges):
            self.mtick += 1
            n = len(BIO_CMDS)
            if edges["up"]:
                self.cursor = (self.cursor - 1) % n
                self.play("cursor")
            elif edges["down"]:
                self.cursor = (self.cursor + 1) % n
                self.play("cursor")
            if edges["z"]:
                cmd = BIO_CMDS[self.cursor][0]
                self.play("confirm")
                if cmd == "recall":
                    self.mode = "sub"
                    self.sub_cursor = 0
                    return
                self._resolve_player(cmd)

        def _step_sub(self, edges):
            n = len(BIO_RECALLS)
            if edges["up"]:
                self.sub_cursor = (self.sub_cursor - 1) % n
                self.play("cursor")
            elif edges["down"]:
                self.sub_cursor = (self.sub_cursor + 1) % n
                self.play("cursor")
            if edges["x"]:
                self.play("cancel")
                self.mode = "menu"
                return
            if edges["z"]:
                self.play("confirm")
                self._resolve_player(BIO_RECALLS[self.sub_cursor][0])

        def _step_beat(self, edges):
            # HOLDS, THEN MOVES ON. It used to wait for a key, twice a turn,
            # because the first build's typewriter outran slow readers. The
            # readout now outlives the beat in the turn log, so nobody loses
            # it -- and nobody presses Z three times to take one turn.
            self.mtick += 1
            if (self.mtick >= INV_BEAT_HOLD
                    or (self.mtick > INV_BEAT_SKIP and (edges["z"] or edges["x"]))):
                self.play("confirm", 0.7)
                after = self.beat_after
                self.beat_label = ""
                self.beat_value = ""
                if after == "enemy":
                    self.mode = "enemy"
                    self.mtick = 0
                elif after == "shift":
                    self._begin_shift()
                else:
                    self._begin_player_turn()

        def _resolve_player(self, cmd):
            after = "enemy"
            label, value = cmd.upper(), ""

            if cmd == "bash":
                dmg = self.rng.randint(BIO_BASH_LO, BIO_BASH_HI)
                crit = self.rng.random() < BIO_CRIT_CHANCE
                if crit:
                    dmg = int(dmg * BIO_CRIT_MULT)
                    self.play("crit")
                    self.flash = 0.22
                    self.shake = 0.8
                    label = "BASH  CRITICAL"
                else:
                    self.play("bash")
                    self.shake = 0.35
                self.damage_boss(dmg, 640, 300, crit)
                self._fx_cut(BIO_A1_FIGURE[0] + self.rng_fx.uniform(-30, 30),
                             BIO_A1_FIGURE[1] - BIO_A1_CHEST
                             + self.rng_fx.uniform(-50, 60), big=crit)
                value = "-" + str(dmg)

            elif cmd == "mend":
                if self.pp < BIO_MEND_PP:
                    self.play("cancel")
                    self._beat("MEND", "NO PP", "menu")
                    return
                self.pp -= BIO_MEND_PP
                self.hp = int(min(BIO_HP_MAX, self.hp + BIO_MEND_HEAL))
                self.play("heal")
                self._fx_rise(BIO_TEAL, 26)
                value = "+" + str(BIO_MEND_HEAL)

            elif cmd == "refuse":
                if self.pp < BIO_REFUSE_PP:
                    self.play("cancel")
                    self._beat("REFUSE", "NO PP", "menu")
                    return
                self.pp -= BIO_REFUSE_PP
                self.play("refuse")
                self.flash = 0.4
                self.shake = 0.6
                self.damage_boss(BIO_REFUSE_DMG, 640, 280, True)
                fx_x, fx_y = BIO_A1_FIGURE[0], BIO_A1_FIGURE[1] - 250
                self.fx.ring(fx_x, fx_y, 20.0, 330.0, life=26, col="#5ce8d0",
                             alpha=0.9, layer="front")
                self.fx.ring(fx_x, fx_y, 10.0, 210.0, life=20, col="#ffffff",
                             alpha=0.7, layer="front", tex="ring_soft")
                for _k in range(5):
                    self.fx.emit(INV_BOLTS[_k % 4], fx_x + self.rng_fx.uniform(-60, 60),
                                 fx_y + self.rng_fx.uniform(-140, 140), life=8,
                                 size=self.rng_fx.uniform(0.7, 1.2),
                                 rot=self.rng_fx.uniform(0, 360), col="#5ce8d0",
                                 layer="front", fade="pop",
                                 delay=self.rng_fx.randint(0, 6))
                self._kick_lens(fx_x, fx_y, 1.0, 0.014)
                self.reactv += 12.0
                value = "-" + str(BIO_REFUSE_DMG)
                if self.telegraph:
                    self.telegraph = False
                    value += "   BROKEN"

            elif cmd == "check":
                self.pp = int(min(BIO_PP_MAX, self.pp + BIO_CHECK_PP_GAIN))
                self.read = True
                self.boss_known = True
                self.play("scan")
                self.scan = 0.0
                value = str(self.boss_hp) + " / " + str(BIO_BOSS_HP_MAX)

            elif cmd == "defend":
                self.guard = True
                self.pp = int(min(BIO_PP_MAX, self.pp + BIO_DEFEND_PP_GAIN))
                self.play("guard")
                self._fx_rise("#9fb6ff", 12)
                self.panel_kick = -0.6
                value = "+" + str(BIO_DEFEND_PP_GAIN) + " PP"

            elif cmd == "run":
                # It never works. It is never explained.
                self.play("miss")
                self.shake = max(self.shake, 0.45)
                self.tear = max(self.tear, 0.5)
                value = "FAILED"

            if self.boss_hp <= BIO_SHIFT_HP and self.corrupt <= 0.0:
                after = "shift"
            self._beat(label, value, after)

        def _pick_enemy_move(self):
            if self.telegraph:
                return "page"
            pool = ["read", "read", "cross", "margin", "glaive", "glaive"]
            if self.turn >= 3:
                pool.append("thumb")
                pool.append("thumb")
            if self.boss_frac() < 0.7:
                pool.append("correct")
            if self.last_enemy in pool and len(set(pool)) > 1:
                pool = [m for m in pool if m != self.last_enemy] or pool
            return self.rng.choice(pool)

        def _step_enemy(self):
            self.mtick += 1
            if self.mtick == 1:
                # CHOSEN AT THE WIND-UP, so the wind-up can say which it is:
                # gold for the moves that are not an attack this turn, red for
                # the ones that are. (One RNG draw either way, same order.)
                self.pending_move = self._pick_enemy_move()
                self.windup_col = (BIO_WARN if self.pending_move in
                                   ("thumb", "correct") else BIO_RED)
                self.play("wind", 0.40)
            if self.mtick < 26:
                self.windup = min(1.0, self.windup + 0.07)
                return

            move = self.pending_move or self._pick_enemy_move()
            self.pending_move = None
            self.last_enemy = move
            self.boss_pose = 1.0
            dmg = 0
            value = ""
            fx = self.fx
            hx, hy = BIO_A1_FIGURE[0], BIO_A1_FIGURE[1] - 395.0

            if move == "read":
                dmg = 34
                fx.emit("flare", hx, hy, life=16, size=2.2, size1=3.0,
                        col="#ff6f86", alpha=0.95, layer="front", fade="pop")
                self._fx_strike(BIO_RED)
            elif move == "cross":
                dmg = 26
                drain = min(self.pp, 6)
                self.pp -= drain
                if drain:
                    value = "-" + str(drain) + " PP  "
                self._fx_strike(BIO_RED)
                for a in (38.0, -38.0):
                    fx.emit("spark", 1004.0, 612.0, life=12, size=3.2,
                            size1=3.8, rot=a, col="#ff8a9c", layer="hud",
                            fade="pop", delay=5)
            elif move == "margin":
                dmg = 14
                self.bleed = 3
                self._fx_strike(BIO_RED)
                fx.burst("drip", 1004.0, 560.0, 7, speed=(0.0, 0.6),
                         life=(30, 50), size=(0.5, 0.9), col="#c0182f",
                         alpha=0.9, add=False, drag=1.0, ay=0.20, angle=90.0,
                         spread=20.0, jitter=150.0, squash=0.15, rot=0.0,
                         layer="hud", delay=(4, 14))
            elif move == "thumb":
                self.telegraph = True
                value = "WINDING UP"
                fx.ring(BIO_A1_FIGURE[0], BIO_A1_FIGURE[1] - 200, 260.0, 60.0,
                        life=30, col=BIO_WARN, alpha=0.8, layer="front")
                self.play("wind2", 0.7)
            elif move == "page":
                dmg = 76
                self.telegraph = False
                self.flash = 0.6
                self.jolt = 0.9
                fx.emit("spark", 640.0, 360.0, life=16, size=9.0, size1=10.5,
                        rot=-62.0, col="#ffffff", layer="hud", fade="pop")
                fx.emit("flare", 640.0, 360.0, life=22, size=5.0, size1=7.0,
                        col="#ff9aab", alpha=0.9, layer="hud", fade="pop")
                self._fx_strike(BIO_RED, big=True)
                fx.burst(INV_SHARDS, 1004.0, 612.0, 14, speed=(3.0, 9.0),
                         life=(20, 40), size=(0.3, 0.6), col="#f2f4ff",
                         add=False, drag=0.94, ay=0.30, vrot=(-16.0, 16.0),
                         layer="hud", delay=(5, 7))
                self._kick_lens(1004.0, 612.0, 1.2, 0.018)
                self.tear = 0.8
            elif move == "glaive":
                dmg = 42
                # A spectral copy, thrown at the window. Never the real one.
                for i in range(6):
                    u = i / 5.0
                    fx.emit(BIO_GLAIVE, inv_lerp(560.0, 1004.0, u),
                            inv_lerp(330.0, 600.0, u), life=7,
                            size=0.8 + 0.7 * u, rot=i * 61.0, col="#ff5a6e",
                            alpha=0.55 + 0.4 * u, layer="hud", fade="pop",
                            delay=int(i * 1.4))
                self._fx_strike(BIO_RED)
            elif move == "correct":
                self.boss_hp = int(min(BIO_BOSS_HP_MAX, self.boss_hp + 25))
                value = "+25"
                cx, cy = BIO_A1_FIGURE[0], BIO_A1_FIGURE[1] - 200
                for i in range(22):
                    a = i * 0.2856
                    r0 = self.rng_fx.uniform(220.0, 300.0)
                    fx.emit("spark", cx + math.cos(a) * r0, cy + math.sin(a) * r0,
                            vx=-math.cos(a) * r0 / 18.0, vy=-math.sin(a) * r0 / 18.0,
                            life=18, size=0.4, stretch=0.06,
                            col=("#5ce8d0" if i % 2 else "#ff2d4e"),
                            layer="front", fade="inout")
                self.boss_flash = 0.6
                self.play("phase", 0.5)

            if dmg > 0:
                if self.guard:
                    dmg = int(dmg * BIO_GUARD_MULT)
                if self.read:
                    dmg = int(dmg * BIO_READ_MULT)
                self.play("enemy", 0.8)
                self.hurt(dmg, 1004, 586)
                value += "-" + str(dmg)

            if self.bleed > 0 and move != "margin":
                self.bleed -= 1
                self.hurt(11, 1004, 610)
                value += "   -11"

            self.read = False
            self.guard = False

            after = "menu"
            if self.corrupt <= 0.0 and (self.boss_hp <= BIO_SHIFT_HP
                                        or self.turn >= BIO_SHIFT_TURN_CAP):
                after = "shift"
            self._beat("BIOGRAPHY", value, after, kind="it")

        # =====================================================================
        # THE CORRUPTIVE TEAR
        # =====================================================================

        def _begin_shift(self):
            self.mode = "shift"
            self.mtick = 0

        def _step_shift(self):
            self.mtick += 1
            t = self.mtick

            if t == 1:
                inv_music_stop(0.3)
                self.play("tear")
                self.tear = 1.0
                self.ca = max(self.ca, 0.016)
            if t == 24:
                # THE WINDOWS BREAK. They used to slide politely off the
                # bottom of the screen; a corruptive tear is not polite. The
                # two panels go to pieces where they stand and the pieces fall
                # out of the frame.
                self.panel_slide = 1.0
                self.play("break", 0.7)
                for (bx0, by0, bw, bh) in (BIOStage.PANEL_CMD, BIOStage.PANEL_HUD):
                    for _k in range(34):
                        x = bx0 + self.rng_fx.uniform(0.0, bw)
                        y = by0 + self.rng_fx.uniform(0.0, bh)
                        ang = math.atan2(y - 360.0, x - 640.0)
                        sp = self.rng_fx.uniform(2.0, 7.0)
                        self.fx.emit(INV_SHARDS[_k % 4], x, y,
                                     vx=math.cos(ang) * sp, vy=math.sin(ang) * sp - 3.0,
                                     life=self.rng_fx.randint(36, 64),
                                     size=self.rng_fx.uniform(0.35, 0.85),
                                     rot=self.rng_fx.uniform(0, 360),
                                     vrot=self.rng_fx.uniform(-12, 12),
                                     col=("#f2f4ff" if _k % 3 else "#5ce8d0"),
                                     alpha=0.9, add=False, drag=0.985, ay=0.28,
                                     layer="hud", fade="late")
                    self.fx.burst("dust", bx0 + bw * 0.5, by0 + bh * 0.5, 30,
                                  speed=(1.0, 5.0), life=(20, 40),
                                  size=(0.6, 1.4), col="#ff2d4e", drag=0.92,
                                  jitter=180.0, squash=0.35, layer="hud")
                self.tear = 1.0
                self.ca = max(self.ca, 0.020)
            if 24 <= t < 110:
                self.jolt = max(self.jolt, 0.4)
                self.shake = max(self.shake, 0.35)
            if t == 110:
                self.play("slam")
                self.flash = 1.0
                self.shake = 1.0
                self.jolt = 1.0
                # The camera is knocked loose here and never settles again.
                self.cam_kick(roll=4.5, py=7.0, zoom=0.055)
                inv_music_corruptive()
                # The stage comes on from its feet outward.
                self.wave = [0.0, 1.5]
                self._kick_lens(BIO_A1_FIGURE[0], BIO_A1_FIGURE[1], 1.4, 0.024)
                for _k in range(8):
                    self.fx.emit(INV_BOLTS[_k % 4],
                                 BIO_A1_FIGURE[0] + self.rng_fx.uniform(-260, 260),
                                 BIO_A1_FIGURE[1] + self.rng_fx.uniform(-60, 30),
                                 life=9, size=self.rng_fx.uniform(1.0, 1.8),
                                 rot=self.rng_fx.uniform(-20, 20), col="#ff6f86",
                                 layer="front", fade="pop",
                                 delay=self.rng_fx.randint(0, 10))
                # Whole again for the second half -- see BIO_SHIFT_RESET.
                if BIO_SHIFT_RESET:
                    self.hp = BIO_HP_MAX
                    self.pp = BIO_PP_MAX
            if 110 <= t < 190:
                self.corrupt = inv_clamp((t - 110) / 80.0, 0.0, 1.0)
            if t == 190:
                self.corrupt = 1.0
                self._begin_open()

        # =====================================================================
        # ACT TWO
        # =====================================================================

        def _begin_open(self):
            ax0, ay0, ax1, ay1 = BIO_ARENA
            self.mode = "open"
            self.mtick = 0
            self.px = (ax0 + ax1) * 0.5
            self.py = ay1 - 90.0
            self.bx = (ax0 + ax1) * 0.5
            self.by = ay0 + 150.0
            self.b_state = "idle"
            self.b_t = 0
            self.b_idle = 60
            self.hazards = []
            self.arcs = []
            for d in self.daggers:
                d["state"] = "held"
                d["spd"] = 0.0
                d["t"] = 0
            self.poise = BIO_POISE_MAX
            self.poise_shown = BIO_POISE_MAX
            self.entry = 0.0
            self.entry_shown = 0.0
            self.entry_cue = 0
            self.chain = 0
            self.boss_known = True
            self.iframe = 40
            self.play("break")
            # The checkpoint. A loss from here on can be retried from the tear.
            self.checkpoint = {"slug": "biography"}

        # --- motion model -------------------------------------------------------

        def _boss_integrate(self, friction=0.94):
            self.bvx *= friction
            self.bvy *= friction
            self.bx += self.bvx
            self.by += self.bvy

        def _boss_seek(self, target, k=0.010, friction=0.90, maxspd=6.0):
            tx, ty = target
            self.bvx += (tx - self.bx) * k
            self.bvy += (ty - self.by) * k
            sp = math.hypot(self.bvx, self.bvy)
            if sp > maxspd:
                self.bvx *= maxspd / sp
                self.bvy *= maxspd / sp
            self._boss_integrate(friction)

        def _wander_point(self):
            tx, ty = self.wander
            if (abs(self.bx - tx) < 40 and abs(self.by - ty) < 40) or self.tick % 190 == 0:
                ax0, ay0, ax1, ay1 = BIO_ARENA
                self.wander = (self.rng.uniform(ax0 + 120, ax1 - 120),
                            self.rng.uniform(ay0 + 40, ay1 - 160))
                tx, ty = self.wander
            return (tx + math.sin(self.clock * 0.53) * 46.0,
                    ty + math.sin(self.clock * 0.71 + 1.3) * 26.0)

        # --- the player ---------------------------------------------------------

        def _open_player(self, edges):
            ax0, ay0, ax1, ay1 = BIO_ARENA
            held = edges["held"]

            dx = (1.0 if held["right"] else 0.0) - (1.0 if held["left"] else 0.0)
            dy = (1.0 if held["down"] else 0.0) - (1.0 if held["up"] else 0.0)
            if dx or dy:
                mag = math.hypot(dx, dy) or 1.0
                dx, dy = dx / mag, dy / mag
                # THE CAMERA ROLLS, SO THE INPUT IS COUNTER-ROLLED. Pressing
                # right has to mean right ON SCREEN however far over the frame
                # has tipped -- a control scheme that leans with the lens is
                # the fastest way to make a moving camera unbearable. This is
                # the same principle as bio_screen_rate below: hands read the
                # screen, so the screen is what the input is expressed in.
                roll = math.radians(self.cam_roll * inv_clamp(self.cam_amt,
                                                            0.0, 1.0))
                cr, sr = math.cos(-roll), math.sin(-roll)
                dx, dy = dx * cr - dy * sr, dx * sr + dy * cr
                self.face = math.degrees(math.atan2(dy, dx))
            # Input is aimed at the SCREEN and converted into world units, so a
            # step feels identical wherever you are standing (bio_screen_rate).
            rate_x, rate_y = bio_screen_rate(self.py)

            if self.dash_cd > 0:
                self.dash_cd -= 1
            if self.fire_cd > 0:
                self.fire_cd -= 1
            if self.iframe > 0:
                self.iframe -= 1

            # THE HELD DASH. Starts on the press, continues while the key is
            # down up to the ceiling, then a flat cooldown. Steerable, so a
            # long dash can be aimed along a wall rather than straight through.
            if edges["x"] and not self.dashing and self.dash_cd <= 0:
                self.dashing = True
                self.dash_t = 0
                self.dash_dir = self.face
                self.play("dash", 0.8)

            if self.dashing:
                self.dash_t += 1
                if dx or dy:
                    want = math.degrees(math.atan2(dy, dx))
                    self.dash_dir += bio_angdiff(want, self.dash_dir) * BIO_DASH_STEER
                rad = math.radians(self.dash_dir)
                self.px += math.cos(rad) * BIO_DASH_SPEED / rate_x
                self.py += math.sin(rad) * BIO_DASH_SPEED / rate_y
                self.iframe = max(self.iframe, BIO_DASH_GRACE)
                spent = self.dash_t >= BIO_DASH_MAX
                let_go = (not held["x"]) and self.dash_t >= BIO_DASH_MIN
                if spent or let_go:
                    self.dashing = False
                    self.dash_cd = BIO_DASH_CD
                    self.iframe = max(self.iframe, BIO_DASH_GRACE)
            else:
                self.px += dx * BIO_PLR_SPEED / rate_x
                self.py += dy * BIO_PLR_SPEED / rate_y

            self.px = inv_clamp(self.px, ax0, ax1)
            self.py = inv_clamp(self.py, ay0, ay1)

            self.trail.insert(0, (self.px, self.py, self.dashing))
            if len(self.trail) > 14:
                self.trail.pop()

            # PICKING THEM BACK UP. No key, no prompt: walk over it, or dash
            # through it. A retrieval that needs a button press turns the best
            # part of the loop -- sprinting into the Archivist's reach because
            # that is where your knives are -- into paperwork.
            for d in self.daggers:
                if d["state"] != "ground":
                    continue
                if math.hypot(self.px - d["x"], self.py - d["y"]) < BIO_PICKUP_R:
                    d["state"] = "held"
                    self.pickup_cue += 1
                    self.play("cursor", 0.55)

            # THROWING. One per press, and only if you are holding one.
            if edges["z"] and self.fire_cd <= 0:
                self._throw_dagger()

        def _held_count(self):
            return sum(1 for d in self.daggers if d["state"] == "held")

        def _throw_dagger(self):
            spare = None
            for d in self.daggers:
                if d["state"] == "held":
                    spare = d
                    break
            if spare is None:
                # Empty-handed. Say so once, quietly, and let the sound be the
                # whole message (rule 1).
                self.play("cancel", 0.35)
                self.fire_cd = 10
                return

            self.fire_cd = BIO_DAGGER_CD
            # LED, not locked on. Aimed at where it will be by the time a
            # dagger could get there, then left to its own weak homing -- so a
            # throw at something that is about to lunge is a throw that misses.
            dist = math.hypot(self.bx - self.px, self.by - self.py)
            lead = inv_clamp(dist / max(BIO_DAGGER_V0, 0.1), 0.0, 42.0)
            tx = self.bx + self.bvx * lead * 0.55
            ty = self.by + self.bvy * lead * 0.55
            ang = math.degrees(math.atan2(ty - self.py, tx - self.px))
            ang += self.rng.uniform(-BIO_DAGGER_SCATTER, BIO_DAGGER_SCATTER)

            spare["state"] = "flight"
            spare["x"] = self.px
            spare["y"] = self.py
            spare["ang"] = ang
            spare["spd"] = BIO_DAGGER_V0
            spare["t"] = 0
            self.play("note", 0.55)
            rad = math.radians(ang)
            self.fx.burst("spark", self.px, self.py, 5, speed=(1.5, 4.5),
                          life=(6, 12), size=(0.18, 0.32), col=BIO_TEAL,
                          angle=ang, spread=50.0, stretch=0.12, drag=0.85,
                          layer="w_front", h=20.0)

        def _open_daggers(self):
            ax0, ay0, ax1, ay1 = BIO_ARENA
            for d in self.daggers:
                if d["state"] != "flight":
                    if d["state"] == "ground":
                        d["rest"] += 1.0
                    continue

                d["t"] += 1
                want = math.degrees(math.atan2(self.by - d["y"], self.bx - d["x"]))
                d["ang"] += inv_clamp(bio_angdiff(want, d["ang"]),
                                    -BIO_DAGGER_TURN, BIO_DAGGER_TURN)
                # DRAG. The whole range and damage model is this one line: it
                # sheds speed the entire way, so a throw from across the stage
                # arrives as a tap and a throw from inside its reach arrives
                # with everything it left with.
                d["spd"] *= BIO_DAGGER_DRAG
                rad = math.radians(d["ang"])
                d["x"] += math.cos(rad) * d["spd"]
                d["y"] += math.sin(rad) * d["spd"]
                # A wake, so a throw reads as a throw at speed and you can
                # watch it lose that speed -- which is the damage model.
                self.fx.emit("spark", d["x"], d["y"],
                             vx=math.cos(rad) * d["spd"] * 0.25,
                             vy=math.sin(rad) * d["spd"] * 0.25,
                             life=9, size=0.34, size1=0.10, col=BIO_TEAL,
                             alpha=0.30 + 0.55 * (d["spd"] / BIO_DAGGER_V0),
                             stretch=0.35, layer="w_front", h=20.0)

                if math.hypot(self.bx - d["x"], self.by - d["y"]) < BIO_BOSS_HURT_R:
                    self._dagger_hit(d)
                    continue

                # It cannot leave the boards, so it can never be lost: it hits
                # the edge of the stage and drops there.
                edge = False
                if not (ax0 - 10 < d["x"] < ax1 + 10):
                    d["x"] = inv_clamp(d["x"], ax0 + 6, ax1 - 6)
                    edge = True
                if not (ay0 - 10 < d["y"] < ay1 + 10):
                    d["y"] = inv_clamp(d["y"], ay0 + 6, ay1 - 6)
                    edge = True

                if edge or d["spd"] < BIO_DAGGER_STOP or d["t"] > BIO_DAGGER_FLIGHT:
                    self._dagger_land(d)

        def _dagger_land(self, d, quiet=False):
            ax0, ay0, ax1, ay1 = BIO_ARENA
            d["state"] = "ground"
            d["x"] = inv_clamp(d["x"], ax0 + 6, ax1 - 6)
            d["y"] = inv_clamp(d["y"], ay0 + 6, ay1 - 6)
            d["spd"] = 0.0
            d["rest"] = 0.0
            if not quiet:
                self.play("graze", 0.30)

        def _speed_frac(self, d):
            return inv_clamp(d["spd"] / BIO_DAGGER_V0, BIO_SPEED_FLOOR, 1.0)

        def _dagger_hit(self, d):
            frac = self._speed_frac(d)
            if self.b_state == "buckle":
                self.punishes += 1
                self.damage_boss(int(round(BIO_DAGGER_DMG_OPEN * frac)),
                                d["x"], d["y"], True)
                self.hp = int(min(BIO_HP_MAX, self.hp + BIO_DAGGER_HEAL))
                self.play("cut_big", 0.8)
                self.freeze = 5
                self.shake = 0.5
                self.cam_kick(zoom=0.010, py=-2.2)
                self._fx_world_burst(d["x"], d["y"], 80.0, "#ffffff", 20, True)
                self._fx_world_burst(d["x"], d["y"], 80.0, BIO_RED, 10, True)
                self._kick_lens(d["x"], d["y"], 0.55, 0.008, world=True)
            else:
                # POISE, NOT HEALTH -- and double while it is committed to a
                # move, which is the reason to stand where the blade is.
                committed = self.b_state in ("wind", "act")
                take = BIO_POISE_HIT * frac * (BIO_POISE_COMMIT_MULT
                                            if committed else 1.0)
                self.poise = max(0.0, self.poise - take)
                self.damage_boss(int(round(BIO_DAGGER_DMG * frac)),
                                d["x"], d["y"], quiet=True)
                # THE NUMBER THAT FLOATS IS THE ONE THE HIT WAS FOR. While it
                # is composed you are not fighting the entry, you are fighting
                # its composure -- so that is the figure, in the player's own
                # colour, and it is a 30 rather than a 3. Printing the health
                # chip here instead was the single reason the loop read as
                # "the daggers do nothing": the game was reporting the
                # smallest of the two things every throw actually did.
                self.float_text(d["x"], d["y"] - 18,
                                str(int(round(take))), BIO_TEAL,
                                committed)
                self.play("cut", 0.55 + 0.35 * frac)
                self.freeze = 2
                self._fx_world_burst(d["x"], d["y"], 80.0, BIO_TEAL,
                                     6 + int(8 * frac), committed)
                if self.poise <= 0.0:
                    self._begin_buckle()

            # IT DEFLECTS AND CARRIES ON. Whatever is left of the throw is
            # spent going past, which puts the ammunition on the far side of
            # the thing that just took it -- so the burst window is worth
            # exactly as much of it as you are willing to run through.
            rad = math.radians(d["ang"])
            d["x"] += (math.cos(rad) * BIO_DAGGER_KICK * frac
                    + self.rng.uniform(-BIO_DAGGER_SPREAD, BIO_DAGGER_SPREAD))
            d["y"] += (math.sin(rad) * BIO_DAGGER_KICK * frac * 0.70
                    + self.rng.uniform(-BIO_DAGGER_SPREAD, BIO_DAGGER_SPREAD)
                    * 0.55)
            self._dagger_land(d, quiet=True)
            self.hit_flash = 1.0
            if self.boss_hp <= 0:
                self._begin_leave(True)

        def _open_exposed(self):
            return self.b_state == "buckle"

        # --- the Archivist -------------------------------------------------------

        def _open_pick_move(self):
            if not self.bag:
                moves = ["sweep", "twirl", "thrust", "plant", "throw",
                        "recital", "orbit"]
                self.rng.shuffle(moves)
                if self.b_move and moves[0] == self.b_move and len(moves) > 1:
                    moves[0], moves[1] = moves[1], moves[0]
                self.bag = moves
            return self.bag.pop(0)

        # ----- the buckle: the only window that does real damage -------------

        def _begin_buckle(self):
            """Poise gone. It stops, it sags, and for BIO_BUCKLE_LEN ticks a
            dagger means something -- but every dagger you spent breaking it
            open is lying at its feet, so the window is only worth what you
            are willing to walk into."""
            self.b_state = "buckle"
            self.b_move = None
            self.b_t = 0
            self.b_len = BIO_BUCKLE_LEN
            self.blade_arc = []
            self.buckles += 1
            self.poise = 0.0
            self.entry = max(0.0, self.entry - BIO_ENTRY_BUCKLE)
            self.play("break", 0.8)
            self.play("phase", 0.45)
            self.flash = 0.30
            self.shake = 0.85
            self.jolt = max(self.jolt, 0.55)
            self.freeze = 9
            self.cam_kick(roll=self.rng_fx.uniform(-1.5, 1.5), py=3.0, zoom=0.022)
            # THE DISCHARGE. Poise breaking is the one moment in the fight
            # where the thing is not composed, and it should not be a quiet
            # one -- the soup lets go across it.
            self._burst_arcs(self.bx, self.by, 7, 430.0, ttl=13, width=1.15,
                            h=95.0)
            self._release_orbits()
            # ...and the composure it was holding comes off it as matter: the
            # body's own registration plates, shed in pieces.
            self._fx_world_burst(self.bx, self.by, 120.0, "#ffffff", 26, True)
            self.fx.burst(INV_SHARDS, self.bx, self.by, 18, speed=(2.5, 8.0),
                          life=(26, 48), size=(0.30, 0.65), col="#ff6f86",
                          add=False, drag=0.95, layer="w_front", h=120.0,
                          vh=(2.0, 9.0), ah=-0.32, vrot=(-14.0, 14.0),
                          squash=0.5)
            self.fx.burst(INV_SHARDS, self.bx, self.by, 10, speed=(2.0, 6.0),
                          life=(26, 48), size=(0.25, 0.5), col=BIO_TEAL,
                          add=False, drag=0.95, layer="w_front", h=120.0,
                          vh=(2.0, 9.0), ah=-0.32, vrot=(-14.0, 14.0),
                          squash=0.5)
            self._kick_lens(self.bx, self.by, 1.3, 0.020, world=True)

        # ----- discharge (cosmetic lightning) --------------------------------
        # The hyperspace "has not finished deciding what matter is", and until
        # now it only ever said so in the shaders. These are bolts from the
        # invasions' OWN fx art (INV_BOLTS -- they were cut out of a ripped
        # sheet until Oct 2 2026): four bolts that get stretched, rotated and
        # cycled. They have NO mechanics -- nothing here can touch the player
        # -- so they are free to be loud at exactly the moments that earned it.

        def _spawn_arc(self, x, y, ang, length, ttl=9, width=1.0, h=40.0):
            # x/y are WORLD coordinates on the boards and h is the height above
            # them, exactly like every other floating thing here -- the
            # renderer projects them, so a bolt near the horizon is short and
            # one at your feet is huge. `length` is in world units for the
            # same reason.
            if len(self.arcs) >= 24:
                return
            self.arcs.append({
                "x": x, "y": y, "h": h, "ang": ang, "len": length,
                "born": self.tick, "ttl": ttl, "w": width,
                # Frame offset so simultaneous bolts are not the same shape.
                "seed": self.rng_fx.randint(0, 3),
            })

        def _burst_arcs(self, x, y, n, length, ttl=9, width=1.0, h=40.0):
            # A radial spray of bolts. Angles are jittered off an even fan so
            # a burst never reads as a wheel, and the ORIGINS are scattered too
            # -- fired from a single point they stack into one bright blob
            # instead of reading as several separate discharges.
            for i in range(n):
                a = (6.2831853 * i / float(n)) + self.rng_fx.uniform(-0.35, 0.35)
                self._spawn_arc(x + self.rng_fx.uniform(-70.0, 70.0),
                                y + self.rng_fx.uniform(-40.0, 40.0),
                                a, length * self.rng_fx.uniform(0.7, 1.15),
                                ttl, width, h + self.rng_fx.uniform(-40.0, 60.0))

        def _step_arcs(self):
            if self.arcs:
                self.arcs = [a for a in self.arcs
                            if self.tick - a["born"] < a["ttl"]]

        def _release_orbits(self):
            """Anything it was holding in orbit is let go ON THE TANGENT it was
            travelling, because that is where a released orbit goes. Deleting
            them outright would be the cheaper fix and it would look like the
            hazard had been switched off."""
            for h in self.hazards:
                if h["kind"] != "orbit":
                    continue
                h["kind"] = "copy"
                rad = math.radians(h["a"] + (90.0 if h["rate"] > 0 else -90.0))
                h["vx"] = math.cos(rad) * 7.2
                h["vy"] = math.sin(rad) * 7.2 * 0.72
                h["phase"] = "out"
                h["t"] = 0
                h["life"] = min(h["life"], 170)

        def _poise_cap(self):
            return BIO_POISE_MAX * min(BIO_POISE_GROWTH_CAP,
                                    1.0 + BIO_POISE_GROWTH * self.buckles)

        def _end_buckle(self):
            self.poise = self._poise_cap()
            self.b_state = "idle"
            self.b_t = 0
            self.b_idle = max(20, self._open_idle_len() - 14)
            self.play("wind", 0.7)
            self.cam_kick(zoom=-0.014)

        def _open_start_move(self):
            move = self._open_pick_move()
            self.b_move = move
            self.b_state = "wind"
            self.b_t = 0
            self.blade_arc = []

            hard = 1.0 - 0.25 * (1.0 - self.boss_frac())
            if self.last_page:
                hard *= 0.8
            winds = {"sweep": 34, "twirl": 30, "thrust": 42,
                    "plant": 30, "throw": 30, "recital": 28, "orbit": 32}
            self.b_len = max(12, int(winds[move] * hard))

            ang = math.degrees(math.atan2(self.py - self.by, self.px - self.bx))
            self.aim = ang
            if move == "sweep":
                self.wind_from = self.body_rot
                self.wind_to = ang - 165.0
                self.blade = self.wind_from
            elif move == "twirl":
                self.wind_from = self.body_rot
                self.wind_to = ang + 200.0
                self.blade = self.wind_from

            self.play("wind2" if move in ("thrust", "plant") else "wind", 0.9)

        def _open_idle_len(self):
            base = 54 if not self.last_page else 34
            base -= int(18 * (1.0 - self.boss_frac()))
            # CHAINING. Past halfway it starts running moves together with
            # barely a breath between them, so the retrieval trips have to be
            # taken during a pattern rather than between two of them.
            if self.chain > 0:
                base = int(base * 0.34)
            return max(12, base)

        def _open_boss(self):
            ax0, ay0, ax1, ay1 = BIO_ARENA
            self.b_t += 1

            # POISE RECOVERS, so chip has to be concentrated to mean anything.
            # It comes back fastest while it is standing about composing and
            # slowest while it is mid-swing -- which is the same statement as
            # "hit it while it is committed", written from its side.
            if self.b_state != "buckle":
                regen = (BIO_POISE_REGEN_IDLE if self.b_state == "idle"
                        else BIO_POISE_REGEN)
                if self.b_state == "recover":
                    regen = BIO_POISE_REGEN_RECOVER
                self.poise = min(self._poise_cap(), self.poise + regen)

            if self.b_state == "buckle":
                # Dead weight. It does not steer, it does not seek, it slides
                # to a stop under friction alone.
                self._boss_integrate(0.88)
                if self.b_t >= self.b_len:
                    self._end_buckle()

            elif self.b_state == "idle":
                self._boss_seek(self._wander_point(), 0.010, 0.90, 5.0)
                if self.b_t >= self.b_idle:
                    self._open_start_move()

            elif self.b_state == "wind":
                u = bio_smooth(inv_clamp(self.b_t / float(max(1, self.b_len)), 0.0, 1.0))
                if self.b_move in ("sweep", "twirl"):
                    self.blade = self.wind_from + bio_angdiff(
                        self.wind_to, self.wind_from) * u
                if self.b_move == "thrust":
                    rad = math.radians(self.aim)
                    self.bvx -= math.cos(rad) * 0.11
                    self.bvy -= math.sin(rad) * 0.11
                    self._boss_integrate(0.90)
                else:
                    self._boss_seek(self._wander_point(), 0.005, 0.90, 2.2)
                if self.b_t >= self.b_len:
                    self._open_begin_act()

            elif self.b_state == "act":
                self._open_act()

            elif self.b_state == "recover":
                self._boss_integrate(0.90)
                if self.b_t >= self.b_len:
                    # Past halfway it runs a second move straight off the back
                    # of the first, then takes its breath.
                    if self.chain > 0:
                        self.chain -= 1
                    elif (self.boss_hp <= BIO_BOSS_HP_MAX * 0.34
                            and self.rng.random() < (0.55 if self.last_page
                                                    else 0.30)):
                        self.chain = 1
                    self.b_state = "idle"
                    self.b_t = 0
                    self.b_idle = self._open_idle_len()

            self.bx = inv_clamp(self.bx, ax0 + 40, ax1 - 40)
            self.by = inv_clamp(self.by, ay0 + 20, ay1 - 60)

            if not self.last_page and self.boss_hp <= BIO_LAST_PAGE_HP:
                self.last_page = True
                self.play("phase")
                self.flash = 0.5
                self.cam_kick(roll=2.4, zoom=0.03)
                self._burst_arcs(self.bx, self.by, 5, 380.0, ttl=12, width=1.0,
                                 h=110.0)
                self._kick_lens(self.bx, self.by, 1.0, 0.016, world=True)

            self._body_pose()

        def _body_pose(self):
            """RULE 3. The body is never a rigid image being translated: it
            rotates bodily through its swings, and squashes and stretches along
            whatever it is doing."""
            st, mv = self.b_state, self.b_move
            tgt_rot = 0.0
            tgt_sx, tgt_sy = 1.0, 1.0
            snap = False

            if st == "act" and mv in ("sweep", "twirl"):
                tgt_rot, snap = self.blade, True
                tgt_sx, tgt_sy = 1.10, 0.94
            elif st == "wind" and mv in ("sweep", "twirl"):
                tgt_rot, snap = self.blade, True
                tgt_sx, tgt_sy = 0.94, 1.06
            elif st == "act" and mv == "thrust":
                # Smeared along the lunge.
                tgt_sx, tgt_sy = 1.34, 0.86
                tgt_rot = inv_clamp(bio_angdiff(self.aim, -90.0), -34.0, 34.0) * 0.5
            elif st == "wind" and mv == "thrust":
                tgt_sx, tgt_sy = 0.80, 1.16          # coiled
            elif st == "wind" and mv == "plant":
                tgt_sx, tgt_sy = 0.88, 1.22          # drawn up tall
            elif st == "act" and mv == "plant":
                tgt_sx, tgt_sy = 1.26, 0.78          # slammed down
            elif st == "act" and mv == "recital":
                tgt_sy = 1.0 + 0.10 * math.sin(self.b_t * 0.09)
                tgt_sx = 1.0 - 0.06 * math.sin(self.b_t * 0.09)
            elif st == "act" and mv == "orbit":
                # Holding the copies out at arm's length, turning with them.
                tgt_rot, snap = self.blade, True
                tgt_sx, tgt_sy = 0.92, 1.12
            elif st == "buckle":
                # Folded. It keeps enough of the rotation it went down with to
                # look struck rather than switched off, and the sag deepens
                # over the window instead of arriving all at once.
                u = bio_smooth(inv_clamp(self.b_t / 26.0, 0.0, 1.0))
                tgt_sx = inv_lerp(1.10, 1.30, u)
                tgt_sy = inv_lerp(0.90, 0.68, u)
                tgt_rot = self.body_rot * 0.94
            elif st == "recover":
                tgt_sx, tgt_sy = 1.06, 0.92          # sagging
            else:
                # Idle is never still, and never symmetrical.
                tgt_sy = 1.0 + 0.035 * math.sin(self.clock * 1.31)
                tgt_sx = 1.0 - 0.025 * math.sin(self.clock * 0.97 + 1.1)

            if snap:
                self.body_rot = tgt_rot
            else:
                step = bio_angdiff(tgt_rot, self.body_rot) * 0.12
                self.body_rot += inv_clamp(step, -9.0, 9.0)
            self.body_sx = inv_lerp(getattr(self, "body_sx", 1.0), tgt_sx, 0.18)
            self.body_sy = inv_lerp(getattr(self, "body_sy", 1.0), tgt_sy, 0.18)

        def _open_begin_act(self):
            move = self.b_move
            self.b_state = "act"
            self.b_t = 0
            self.b_hits = 0                  # see BIO_MOVE_HIT_CAP
            hard = 1.0 - 0.2 * (1.0 - self.boss_frac())
            ang = math.degrees(math.atan2(self.py - self.by, self.px - self.bx))
            self.aim = ang

            if move == "sweep":
                self.b_len = max(16, int(28 * hard))
                self.wind_from = self.blade
                self.wind_to = self.blade + 300.0
                self.play("swing")
                self.cam_kick(roll=0.9 * (1.0 if math.cos(math.radians(ang)) > 0
                                        else -1.0))
            elif move == "twirl":
                self.b_len = 150
                self.play("swing", 0.8)
            elif move == "thrust":
                self.b_len = 30
                rad = math.radians(ang)
                self.bvx = math.cos(rad) * 21.0
                self.bvy = math.sin(rad) * 21.0
                self.play("clash", 0.8)
                self.cam_kick(zoom=0.016, px=math.cos(rad) * 2.6)
            elif move == "plant":
                self.b_len = 2 * BIO_RING_GAP + 30
                self._spawn_ring()
                self.play("ring")
                self.shake = 0.6
                self.cam_kick(py=4.2, zoom=-0.012)
            elif move == "throw":
                # Shorter than it was, and it throws three. The whole of this
                # move used to count as an exposure -- 150 free ticks of
                # over-extension every cycle, which is most of why act two
                # could be won without moving. The three copies are spaced at
                # BIO_COPY_GAP, not packed: the harness caught them landing 36
                # ticks apart against a 46-tick dash cooldown, which is exactly
                # the rule-5 spacing constraint this file is written against.
                self.b_len = 2 * BIO_COPY_GAP + 32
                self.play("throw")
                self._spawn_copy()
            elif move == "recital":
                self.b_len = 3 * BIO_BAR_GAP
                self.play("note", 0.9)
                self._spawn_bar()
            elif move == "orbit":
                # THE ANSWER TO RETRIEVAL. It sets spectral copies turning
                # around itself at three radii and three rates, so the ground
                # immediately around it -- which is exactly where your daggers
                # are lying -- stops being free to walk across. No gap is
                # authored into it: the copies are at different radii and
                # different speeds, so what you weave through is a moving
                # pattern, never a door left open.
                self.b_len = 320
                self.play("wind2", 0.85)
                self.play("throw", 0.5)
                self.cam_kick(roll=-1.1, zoom=0.010)
                base = self.rng.uniform(0.0, 360.0)
                for i, (rad_, rate, sgn) in enumerate((
                        (108.0, 2.35, 1.0), (172.0, -1.62, -1.0),
                        (246.0, 1.18, 1.0))):
                    self._spawn_orbit(base + i * 137.0, rad_, rate * sgn)

        def _open_act(self):
            move = self.b_move
            t = self.b_t
            self.blade_prev = self.blade

            if move == "sweep":
                u = bio_smooth(inv_clamp(t / float(self.b_len), 0.0, 1.0))
                self.blade = self.wind_from + (self.wind_to - self.wind_from) * u
                rad = math.radians(self.blade + 90.0)
                self.bvx += math.cos(rad) * 0.30
                self.bvy += math.sin(rad) * 0.30
                self._boss_integrate(0.88)
                self.blade_arc.insert(0, self.blade)
                if len(self.blade_arc) > 10:
                    self.blade_arc.pop()
                if t >= self.b_len:
                    self._open_recover(46)

            elif move == "twirl":
                u = inv_clamp(t / float(self.b_len), 0.0, 1.0)
                speed = inv_lerp(3.2, 15.5, bio_smooth(min(1.0, u * 2.0)))
                if u > 0.86:
                    speed *= inv_lerp(1.0, 0.45, (u - 0.86) / 0.14)
                self.blade += speed
                self.blade_arc.insert(0, self.blade)
                if len(self.blade_arc) > 8:
                    self.blade_arc.pop()
                self._boss_seek((self.px, self.py), 0.0045, 0.94, 3.0)
                if t % 34 == 0:
                    self.play("swing", 0.45)
                if t >= self.b_len:
                    self._open_recover(50)

            elif move == "thrust":
                self._boss_integrate(0.955)
                self.blade = self.aim
                if t >= self.b_len:
                    self._open_recover(76)

            elif move == "plant":
                if t in (BIO_RING_GAP, 2 * BIO_RING_GAP):
                    self._spawn_ring()
                    self.play("ring", 0.8)
                self._boss_integrate(0.86)
                if t >= self.b_len:
                    self._open_recover(48)

            elif move == "throw":
                if t in (BIO_COPY_GAP, 2 * BIO_COPY_GAP):
                    self._spawn_copy()
                self._boss_seek(self._wander_point(), 0.006, 0.92, 3.4)
                if t >= self.b_len:
                    self._open_recover(30)

            elif move == "recital":
                if t in (BIO_BAR_GAP, 2 * BIO_BAR_GAP):
                    self._spawn_bar()
                self._boss_seek(self._wander_point(), 0.007, 0.92, 3.8)
                if t >= self.b_len:
                    self._open_recover(44)

            elif move == "orbit":
                # It turns with them and drifts, so the hazard field travels
                # across the boards rather than sitting on one spot.
                self.blade += 1.9
                self._boss_seek(self._wander_point(), 0.0035, 0.94, 2.4)
                if t % 52 == 0:
                    self.play("note", 0.35)
                if t >= self.b_len:
                    self._open_recover(56)

        def _open_recover(self, ticks):
            if self.b_move == "orbit":
                self._release_orbits()
            self.b_state = "recover"
            self.b_t = 0
            self.b_len = max(14, int(ticks * (0.8 if self.last_page else 1.0)))
            self.blade_arc = []

        def _blade_hits(self, ang):
            """Swept test: covers everything the blade passed through this
            tick, at any speed. A fixed window silently starts stepping over
            the player once the eased sweep peaks above its width."""
            arms = (0.0,) if self.b_move == "sweep" else (0.0, 180.0)
            for arm in arms:
                a1 = self.blade + arm
                if abs(bio_angdiff(ang, a1)) < BIO_BLADE_ARC:
                    return True
                span = (self.blade - self.blade_prev)
                if abs(span) < 0.01:
                    continue
                rel = bio_angdiff(ang, self.blade_prev + arm)
                if span > 0:
                    if -BIO_BLADE_ARC <= rel <= span + BIO_BLADE_ARC:
                        return True
                else:
                    if span - BIO_BLADE_ARC <= rel <= BIO_BLADE_ARC:
                        return True
            return False

        # --- hazards ------------------------------------------------------------
        # No authored gaps: rings are whole rings, recital lines span the arena.
        # The dash is the answer, so spacing is bound to BIO_DASH_CD (rule 5).

        def _spawn_ring(self):
            self.hazards.append({"kind": "ring", "x": self.bx, "y": self.by + 30,
                                "r": 40.0, "w": BIO_RING_WIDTH,
                                "spd": BIO_RING_SPEED,
                                "warn": BIO_RING_WARN, "life": 400})
            self.shake = max(self.shake, 0.45)
            # The plant: the boards crack and throw dust where it lands.
            self.fx.burst(INV_SMOKES, self.bx, self.by + 30, 8, speed=(1.0, 3.5),
                          life=(30, 54), size=(0.5, 1.0), size1=1.6,
                          col="#ff7a90", alpha=0.35, add=False, drag=0.93,
                          layer="w_front", h=8.0, vh=(0.3, 1.6), squash=0.4)
            self.fx.burst("spark", self.bx, self.by + 30, 12, speed=(3.0, 8.0),
                          life=(8, 16), size=(0.2, 0.4), col=BIO_WARN,
                          stretch=0.10, drag=0.86, layer="w_front", h=6.0,
                          vh=(1.0, 4.0), squash=0.4)

        def _spawn_bar(self):
            ax0, ay0, ax1, ay1 = BIO_ARENA
            horizontal = self.rng.random() < 0.5
            if horizontal:
                from_top = self.rng.random() < 0.5
                pos = ay0 - 30.0 if from_top else ay1 + 30.0
                self.hazards.append({"kind": "bar", "axis": "h", "p": pos,
                                    "spd": BIO_BAR_SPEED if from_top else -BIO_BAR_SPEED,
                                    "th": 26.0, "warn": BIO_BAR_WARN, "life": 500})
            else:
                from_left = self.rng.random() < 0.5
                pos = ax0 - 30.0 if from_left else ax1 + 30.0
                self.hazards.append({"kind": "bar", "axis": "v", "p": pos,
                                    "spd": BIO_BAR_SPEED if from_left else -BIO_BAR_SPEED,
                                    "th": 26.0, "warn": BIO_BAR_WARN, "life": 500})

        def _spawn_copy(self):
            """A SPECTRAL COPY of the glaive -- it keeps its own. Filed, not
            thrown."""
            rad = math.radians(self.aim + self.rng.uniform(-18.0, 18.0))
            self.hazards.append({"kind": "copy", "x": self.bx, "y": self.by,
                                "vx": math.cos(rad) * 9.0,
                                "vy": math.sin(rad) * 9.0,
                                "spin": self.rng.uniform(0, 360),
                                "phase": "out", "t": 0, "life": 260})
            self._fx_world_burst(self.bx, self.by, 90.0, "#ff5a6e", 8)

        def _spawn_orbit(self, ang, radius, rate):
            """A copy held in orbit around it. Position is DERIVED from the
            angle every tick and the angle only ever integrates, so the thing
            travels on a real circle about a moving centre -- no coordinate
            anywhere gets a constant added to it."""
            self.hazards.append({"kind": "orbit", "x": self.bx, "y": self.by,
                                "a": ang, "r": radius, "rate": rate,
                                "grow": 0.0, "spin": self.rng.uniform(0, 360),
                                "t": 0, "life": 400})

        def _open_hazards(self):
            ax0, ay0, ax1, ay1 = BIO_ARENA
            keep = []
            for h in self.hazards:
                kind = h["kind"]
                h["life"] -= 1
                alive = h["life"] > 0

                if kind == "ring":
                    if h["warn"] > 0:
                        h["warn"] -= 1
                        if h["warn"] == 0:
                            self.play("ring", 0.7)
                    else:
                        h["r"] += h["spd"]
                        if h["r"] > 980:
                            alive = False

                elif kind == "bar":
                    if h["warn"] > 0:
                        h["warn"] -= 1
                    else:
                        h["p"] += h["spd"]
                        lo = (ay0 - 80) if h["axis"] == "h" else (ax0 - 80)
                        hi = (ay1 + 80) if h["axis"] == "h" else (ax1 + 80)
                        if not (lo < h["p"] < hi):
                            alive = False

                elif kind == "orbit":
                    h["t"] += 1
                    h["spin"] += 9.0
                    h["a"] += h["rate"]
                    # Eases out to its radius rather than snapping there, so
                    # the first revolution is the telegraph.
                    h["grow"] = inv_lerp(h["grow"], 1.0, 0.045)
                    rr = h["r"] * h["grow"]
                    ra = math.radians(h["a"])
                    h["x"] = self.bx + math.cos(ra) * rr
                    h["y"] = self.by + math.sin(ra) * rr * 0.72

                elif kind == "copy":
                    h["t"] += 1
                    h["spin"] += 13.0
                    if h["phase"] == "out":
                        h["vx"] *= 0.968
                        h["vy"] *= 0.968
                        h["x"] += h["vx"]
                        h["y"] += h["vy"]
                        if h["t"] > 70 or math.hypot(h["vx"], h["vy"]) < 1.6:
                            h["phase"] = "hunt"
                    else:
                        # Then it comes looking, slowly and inevitably.
                        ang = math.atan2(self.py - h["y"], self.px - h["x"])
                        h["vx"] += math.cos(ang) * 0.16
                        h["vy"] += math.sin(ang) * 0.16
                        sp = math.hypot(h["vx"], h["vy"])
                        if sp > 4.2:
                            h["vx"] *= 4.2 / sp
                            h["vy"] *= 4.2 / sp
                        h["x"] += h["vx"]
                        h["y"] += h["vy"]

                if alive:
                    keep.append(h)
            self.hazards = keep

        def _open_collide(self):
            if self.graze_cd > 0:
                self.graze_cd -= 1
            invuln = self.iframe > 0

            def strike(amount):
                if not invuln:
                    self.hurt(amount, self.px, self.py - 30)
                    self.iframe = BIO_HURT_IFRAMES
                    self.freeze = 5
                    self.cam_kick(roll=self.rng_fx.uniform(-1.9, 1.9),
                                px=self.rng_fx.uniform(-3.4, 3.4),
                                py=self.rng_fx.uniform(-2.6, 2.6),
                                zoom=-0.016)
                    return True
                return False

            def sustained(amount):
                """A hit from a hazard that STAYS ON for a while -- the blade,
                the lunge, the orbiting copies. Capped per attack so spending
                two seconds inside a twirl costs you twice, not four times."""
                if self.b_hits >= BIO_MOVE_HIT_CAP:
                    return False
                if strike(amount):
                    self.b_hits += 1
                    return True
                return False

            def graze():
                """A near miss is worth something now. Being in the way of the
                blade is the one thing that stops it writing, so the entry is
                knocked back by exactly the amount of danger you stood in."""
                self.graze_cd = 16
                self.entry = max(0.0, self.entry - BIO_ENTRY_GRAZE)
                self.play("graze", 0.5)
                self.fx.burst("spark", self.px, self.py, 6, speed=(2.0, 5.0),
                              life=(6, 12), size=(0.16, 0.28), col=BIO_WARN,
                              stretch=0.12, drag=0.84, layer="w_front", h=24.0,
                              squash=0.45)

            if self.b_state == "act" and self.b_move in ("sweep", "twirl"):
                dx = self.px - self.bx
                dy = self.py - self.by
                dist = math.hypot(dx, dy)
                if BIO_BLADE_INNER - BIO_PLR_HIT_R < dist < BIO_BLADE_OUTER + BIO_PLR_HIT_R:
                    ang = math.degrees(math.atan2(dy, dx))
                    if self._blade_hits(ang):
                        sustained(BIO_DMG_SWEEP if self.b_move == "sweep"
                                else BIO_DMG_TWIRL)
                    elif self.graze_cd <= 0 and not invuln:
                        arms = (self.blade,) if self.b_move == "sweep" else (self.blade, self.blade + 180.0)
                        near = min(abs(bio_angdiff(ang, arm)) for arm in arms)
                        if near < BIO_BLADE_ARC + 9:
                            graze()

            if self.b_state == "act" and self.b_move == "thrust":
                rad = math.radians(self.aim)
                tipx = self.bx + math.cos(rad) * 200.0
                tipy = self.by + math.sin(rad) * 200.0
                if bio_point_seg(self.px, self.py, self.bx, self.by,
                                tipx, tipy) < 34 + BIO_PLR_HIT_R:
                    sustained(BIO_DMG_THRUST)

            for h in self.hazards:
                kind = h["kind"]
                if kind == "ring" and h["warn"] <= 0:
                    d = abs(math.hypot(self.px - h["x"], self.py - h["y"]) - h["r"])
                    if d < h["w"] * 0.5 + BIO_PLR_HIT_R:
                        strike(BIO_DMG_RING)
                    elif d < h["w"] * 0.5 + 26 and self.graze_cd <= 0 and not invuln:
                        graze()
                elif kind == "bar" and h["warn"] <= 0:
                    v = self.py if h["axis"] == "h" else self.px
                    if abs(v - h["p"]) < h["th"] * 0.5 + BIO_PLR_HIT_R:
                        strike(BIO_DMG_BAR)
                elif kind == "copy":
                    if math.hypot(self.px - h["x"], self.py - h["y"]) < 28 + BIO_PLR_HIT_R:
                        if strike(BIO_DMG_COPY):
                            h["life"] = 0
                elif kind == "orbit":
                    dd = math.hypot(self.px - h["x"], self.py - h["y"])
                    if dd < 30 + BIO_PLR_HIT_R:
                        sustained(BIO_DMG_ORBIT)
                    elif dd < 30 + 26 and self.graze_cd <= 0 and not invuln:
                        graze()

        def _step_entry(self):
            """It is not trying to kill you. It is trying to finish writing you
            down, and it can do that from anywhere you are not."""
            # A dagger landing the killing blow ends the fight from inside
            # _open_daggers, and the rest of this tick still runs -- without
            # this line the entry could complete on the same frame and turn a
            # win into a loss.
            if self.mode != "open" or self.b_state == "buckle":
                return
            dist = math.hypot(self.bx - self.px, self.by - self.py)
            far = inv_clamp((dist - BIO_ENTRY_NEAR)
                            / float(BIO_ENTRY_FAR - BIO_ENTRY_NEAR), 0.0, 1.0)
            rate = BIO_ENTRY_RATE * (0.55 + 1.10 * far)
            if self.b_state == "recover":
                rate *= 0.5
            self.entry = min(BIO_ENTRY_MAX, self.entry + rate)

            # One cue per tenth, so the pace of it is audible without a
            # countdown being drawn anywhere.
            step = int(self.entry / 10.0)
            if step > self.entry_cue:
                self.entry_cue = step
                self.play("text", 0.55 + 0.05 * step)

            if self.entry >= BIO_ENTRY_MAX:
                if self.god:
                    # Godmode takes the subtraction out of every clock, not
                    # only the health one -- the point is to be able to sit in
                    # a pattern and read it. The bar still pins at full so a
                    # godmode run is never mistaken for a clear.
                    self.entry = BIO_ENTRY_MAX
                    return
                self.flash = 1.0
                self.cam_kick(zoom=0.05)
                self._begin_leave(False)

        def _step_open(self, edges):
            self.mtick += 1
            if self.freeze > 0:
                self.freeze -= 1
                return
            self._open_player(edges)
            self._open_daggers()
            self._open_boss()
            self._open_hazards()
            self._open_collide()
            self._step_entry()

        # =====================================================================
        # DEPARTURE -- back through the hole (rule 4)
        # =====================================================================

        def _begin_leave(self, won):
            self.mode = "leave_w" if won else "leave_l"
            self.mtick = 0
            self.hazards = []
            # The daggers are an INVENTORY of four objects, not a spawn list --
            # emptying it would delete them off the boards on the frame the
            # fight ends. Anything still in the air simply comes down.
            for d in self.daggers:
                if d["state"] == "flight":
                    self._dagger_land(d, quiet=True)
            self.flash = 1.0
            self.shake = 1.0
            self.play("break" if won else "struck")
            inv_music_stop(1.8)
            # Captured for the win sequence, which lerps from where the fight
            # actually ended rather than from constants -- the same rule the
            # other endings learned the hard way (Horror's used to snap).
            self.leave_rot0 = self.body_rot
            self.leave_scale0 = self.body_scale
            self.leave_by0 = self.by
            # The wormhole is a SCREEN-space effect but bx/by are world
            # coordinates on the stage floor now, so it has to be projected.
            # Keep the world anchor too, because the body is dragged toward it
            # in world space and only then projected.
            self.hole_wx = self.bx if won else self.px
            self.hole_wy = self.by if won else self.py
            hx, hy, _hp = bio_project(self.hole_wx, self.hole_wy)
            self.hole[0] = hx
            self.hole[1] = hy - 110.0

        def _step_leave(self):
            """THE WIN IS NOT A VICTORY, IT IS AN ENTRY THAT CANNOT BE CLOSED.

            Biography is not trying to kill the party member and never was --
            it is trying to FINISH THE ENTRY -- so beating it cannot be drawn
            as a thing dying. It is drawn as the filing failing, and the six
            beats below are that, in order:

                BUCKLE      it goes down, and this time it does not get the
                            beat back. Everything stops with it.
                RISE        and it tries to finish anyway. It draws itself up
                            taller than it has stood all fight.
                THE SWEEP   one enormous last pass, all the way round, with
                            the whole trail behind it -- and it lands on
                            nothing, because there is nothing left to file.
                REGISTER    the plate comes apart. Its own misregistration
                            runs away with it and takes the room with it.
                THE BOARDS  the hole opens UNDERNEATH rather than behind, and
                            the stage it has been fighting on gives way.
                UNFINISHED  black, held, with nothing filed.

            The loss is untouched: it does not leave, the room closes over you.
            """
            self.mtick += 1
            t = self.mtick
            won = (self.mode == "leave_w")

            if not won:
                # --- unchanged: it does not leave, the room closes over you --
                if t < 46:
                    self.hole[3] = bio_smooth(t / 46.0)
                    self.hole[2] = inv_lerp(30.0, 290.0, bio_smooth(t / 46.0))
                    if t == 8:
                        self.play("tear", 0.85)
                        self.tear = 0.8
                elif t < 120:
                    u = (t - 46) / 74.0
                    self.hole[3] = 1.0
                    self.hole[2] = inv_lerp(290.0, 900.0, bio_smooth(u))
                elif t < 170:
                    self.hole[3] = 1.0
                    self.hole[2] = 900.0
                    self.dark = inv_clamp(self.dark + 0.02, 0.0, 1.0)
                else:
                    self.dark = inv_clamp(self.dark + 0.03, 0.0, 1.0)
                    if t > 210:
                        self.result = "defeat"
                return

            # ================= 1. THE BUCKLE (0-44) =======================
            if t < 44:
                u = t / 44.0
                if t == 2:
                    self.jolt = 1.0
                    self.cam_kick(roll=-7.0, py=11.0, zoom=0.085)
                    self.play("cut_big", 0.95)
                # It sags onto the boards, and the sag is a real squash about
                # the feet rather than a drop in y.
                self.body_rot = inv_lerp(self.leave_rot0, 15.0, bio_smooth(u))
                self.body_scale = inv_lerp(self.leave_scale0, 0.88,
                                        bio_smooth(u))
                self.jolt = max(self.jolt, 0.35 * (1.0 - u))
                self.rush += INV_TICK * 0.4

            # ================= 2. IT TRIES ANYWAY (44-150) ================
            elif t < 150:
                u = (t - 44) / 106.0
                su = bio_smooth(u)
                if t == 46:
                    self.play("wind2", 0.85)
                if t == 104:
                    self.play("wind", 0.9)
                    self.cam_kick(roll=2.5, zoom=0.03)
                # Drawn up taller than it has stood all fight, and coiling
                # backward for the swing.
                self.body_rot = inv_lerp(15.0, -14.0, su)
                self.body_scale = inv_lerp(0.88, 1.26, su)
                self.fury = min(1.0, self.fury + 0.012)
                self.rush += INV_TICK * (0.6 + 1.4 * su)
                # The room leans in with it.
                if t % 18 == 0:
                    self.cam_kick(zoom=0.012, py=-1.2)

            # ================= 3. THE LAST SWEEP (150-206) ================
            elif t < 206:
                u = (t - 150) / 56.0
                su = bio_smooth(u)
                if t == 150:
                    self.play("swing", 1.0)
                    self.play("clash", 0.7)
                    self.jolt = 1.0
                    self.flash = 0.75
                    self.shake = 1.0
                    self.cam_kick(roll=10.0, px=-16.0, zoom=0.13)
                    self._kick_lens(self.bx, self.by, 1.6, 0.03, world=True)
                    self._burst_arcs(self.bx, self.by, 9, 520.0, ttl=16,
                                     width=1.3, h=110.0)
                # A full pass and a half, smeared along its own axis, with the
                # whole trail behind it. This is the only time in the fight the
                # body goes all the way round.
                self.body_rot = inv_lerp(-14.0, 526.0, su)
                self.body_scale = inv_lerp(1.26, 1.10, su)
                self.ghosts.insert(0, (self.bx, self.by, self.body_rot,
                                    self.body_scale))
                if len(self.ghosts) > 11:
                    self.ghosts.pop()
                self.fury = 1.0
                self.jolt = max(self.jolt, 0.55 * (1.0 - u))
                self.rush += INV_TICK * 2.2

            # ================= 4. LOSS OF REGISTER (206-286) ==============
            elif t < 286:
                u = (t - 206) / 80.0
                su = bio_smooth(u)
                if t == 208:
                    self.play("break", 0.9)
                    self.cam_kick(roll=-6.0, px=9.0)
                    self.tear = 1.0
                if t % 6 == 0:
                    self.fx.burst(INV_SHARDS, self.bx, self.by, 3,
                                  speed=(1.5, 5.0), life=(30, 50),
                                  size=(0.25, 0.55),
                                  col=("#ff6f86", "#5ce8d0", "#f2f4ff")[t % 3],
                                  add=False, drag=0.96, layer="w_front",
                                  h=self.rng_fx.uniform(40.0, 300.0),
                                  vh=(-1.0, 3.0), vrot=(-10.0, 10.0),
                                  squash=0.5)
                # ...and it lands on nothing. The plate that has been very
                # slightly out all fight stops being able to hold itself in
                # register at all: the slices drift off it and do not come
                # back. `emerge` is the erosion, so this is Biography's own
                # dissolve running away with it rather than a new effect.
                self.body_rot = inv_lerp(526.0, 548.0, su)
                self.body_scale = inv_lerp(1.10, 1.02, su)
                self.emerge = 0.62 * su
                self.fury = 1.0
                self.jolt = max(self.jolt, 0.20 + 0.45 * su)
                self.rush += INV_TICK * (2.2 - 1.2 * su)
                if t % 9 == 0:
                    self.ghosts.insert(0, (self.bx, self.by, self.body_rot,
                                        self.body_scale))
                    if len(self.ghosts) > 11:
                        self.ghosts.pop()
                elif self.ghosts and t % 3 == 0:
                    self.ghosts.pop()
                if t % 22 == 0:
                    self.cam_kick(roll=self.rng_fx.uniform(-4.0, 4.0),
                                px=self.rng_fx.uniform(-7.0, 7.0))

            # ================= 5. THE BOARDS GIVE WAY (286-370) ===========
            elif t < 370:
                u = (t - 286) / 84.0
                su = bio_smooth(u)
                if t == 286:
                    self.play("slam", 1.0)
                    self.play("tear", 0.9)
                    self.flash = 0.55
                    self.shake = 1.0
                    self.cam_kick(roll=4.0, py=14.0, zoom=0.10)
                    self._kick_lens(self.bx, self.by, 1.5, 0.026, world=True)
                    # The boards go: pieces of the stage itself, falling up
                    # out of the hole and then down into it.
                    self.fx.burst(INV_SHARDS, self.bx, self.by, 40,
                                  speed=(2.0, 9.0), life=(40, 70),
                                  size=(0.4, 1.0), col="#7c0f22", add=False,
                                  drag=0.97, layer="w_front", h=4.0,
                                  vh=(3.0, 11.0), ah=-0.35,
                                  vrot=(-12.0, 12.0), squash=0.45)
                # THE HOLE OPENS UNDERNEATH IT. Not behind it and not beside
                # it -- the stage it has spent the whole act standing on is
                # what fails, so the mouth is on the boards at its own feet and
                # it goes DOWN through them.
                hx, hy, _hp = bio_project(self.bx, self.by)
                self.hole[0] = hx
                self.hole[1] = hy - 16.0
                self.hole[3] = min(1.0, su * 1.8)
                self.hole[2] = inv_lerp(26.0, 430.0, su)
                self.by = inv_lerp(self.leave_by0, self.leave_by0 + 46.0, su)
                self.body_scale = inv_lerp(1.02, 0.10, su * su)
                self.emerge = inv_lerp(0.62, 1.0, su)
                self.body_rot = inv_lerp(548.0, 600.0, su)
                self.jolt = max(self.jolt, 0.30 * (1.0 - u))
                if self.ghosts and t % 4 == 0:
                    self.ghosts.pop()

            # ================= 6. UNFINISHED (370+) =======================
            else:
                u = inv_clamp((t - 370) / 60.0, 0.0, 1.0)
                self.hole[3] = 1.0 - bio_smooth(u)
                self.hole[2] = inv_lerp(430.0, 18.0, bio_smooth(u))
                self.ghosts = []
                if t > 400:
                    self.dark = inv_clamp(self.dark + 0.016, 0.0, 1.0)
                if t > 470:
                    self.result = "victory"

    # --- the camera ----------------------------------------------------------
    def bio_persp(wy):
        """Foreshortening at a given depth. 1.0 downstage, small upstage."""
        ax0, ay0, ax1, ay1 = BIO_ARENA
        u = inv_clamp((wy - ay0) / float(ay1 - ay0), 0.0, 1.0)
        return 1.0 / inv_lerp(1.0 / BIO_PERSP_FAR, 1.0 / BIO_PERSP_NEAR, u)

    def bio_project(wx, wy):
        """World point -> (screen x, screen y on the floor, scale)."""
        pp = bio_persp(wy)
        return (640.0 + (wx - 640.0) * pp,
                BIO_CAM_HORIZON + BIO_FLOOR_K * pp,
                pp)

    def bio_project_hk(wx, wy, hz, fk):
        """bio_project with an arbitrary horizon and floor scale -- act one's
        low camera, and the tear's climb from it to act two's proscenium."""
        pp = bio_persp(wy)
        return (640.0 + (wx - 640.0) * pp, hz + fk * pp, pp)

    def bio_unproject(sx, sy, hz=None, fk=None):
        """A (pre-camera) screen point on the boards -> world (wx, wy). The
        exact inverse the soup shader runs per pixel, so a light pool placed
        from Python lands where the floor says it is."""
        ax0, ay0, ax1, ay1 = BIO_ARENA
        hz = BIO_CAM_HORIZON if hz is None else hz
        fk = BIO_FLOOR_K if fk is None else fk
        pp = max(0.001, (sy - hz) / max(fk, 1.0))
        u = ((1.0 / pp - 1.0 / BIO_PERSP_FAR)
             / (1.0 / BIO_PERSP_NEAR - 1.0 / BIO_PERSP_FAR))
        return (640.0 + (sx - 640.0) / pp, ay0 + u * (ay1 - ay0))

    def bio_persp_free(wy):
        """bio_persp WITHOUT the clamp, for things that are not standing on the
        stage -- suspended matter drifts past both edges of it, and a clamped
        perspective would freeze a piece of debris in place at the bottom of
        the frame instead of letting it come past the lens."""
        ax0, ay0, ax1, ay1 = BIO_ARENA
        u = (wy - ay0) / float(ay1 - ay0)
        den = inv_lerp(1.0 / BIO_PERSP_FAR, 1.0 / BIO_PERSP_NEAR, u)
        return 1.0 / max(den, 0.12)

    def bio_screen_rate(wy):
        """How many screen pixels one world unit is worth here, per axis.

        THE CONTROL FIX. Moving in world units under a perspective camera
        means the same key press travels a wildly different distance on
        screen depending on where you are standing -- upstage a step is
        nearly invisible, downstage it lurches. Hands read the SCREEN, so
        input is divided by these and the avatar moves at a constant apparent
        speed everywhere on the floor. The player already has enough to think
        about without also compensating for the lens.
        """
        ax0, ay0, ax1, ay1 = BIO_ARENA
        pp = bio_persp(wy)
        # d(screen x)/d(world x) is just the foreshortening.
        rate_x = pp
        # d(screen y)/d(world y), from p = 1 / (A + (B-A)u).
        a_inv = 1.0 / BIO_PERSP_FAR
        b_inv = 1.0 / BIO_PERSP_NEAR
        rate_y = BIO_FLOOR_K * (a_inv - b_inv) / float(ay1 - ay0) * pp * pp
        return (max(rate_x, 0.18), max(rate_y, 0.18))

    def bio_cam_apply(x, y, cam):
        """Un-rolled screen point -> the frame the player is actually looking at.

        bio_project() answers "where is this on the sensor"; this answers
        "where did the camera put the sensor". Keeping the two apart is what
        lets the soup shader run the exact inverse of this on its own fragment
        coordinate, so the painted floor and the projected bodies standing on
        it can never drift out of register.

        Every term is an honest camera move: a roll is an image rotation about
        the principal point, a focal change is a scale about it, a pan is a
        sensor shift. None of them is noise, which is why the room can be made
        genuinely hard to look at without reading as broken.
        """
        if not cam:
            return (x, y)
        roll, panx, pany, zoom = cam
        dx = (x - 640.0) * zoom
        dy = (y - 360.0) * zoom
        cs = math.cos(roll)
        sn = math.sin(roll)
        return (640.0 + dx * cs - dy * sn + panx,
                360.0 + dx * sn + dy * cs + pany)

    # --- geometry helpers ----------------------------------------------------
    def bio_smooth(u):
        """Smootherstep: zero velocity AND acceleration at both ends."""
        u = inv_clamp(u, 0.0, 1.0)
        return u * u * u * (u * (u * 6.0 - 15.0) + 10.0)

    def bio_angdiff(a, b):
        d = (a - b) % 360.0
        if d > 180.0:
            d -= 360.0
        return d

    def bio_point_seg(px, py, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        den = dx * dx + dy * dy
        if den <= 0.0001:
            return math.hypot(px - x1, py - y1)
        t = inv_clamp(((px - x1) * dx + (py - y1) * dy) / den, 0.0, 1.0)
        return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


# --- THE STAGE ---------------------------------------------------------------
# Oct 2 2026: the renderer draws through the shared kit (inv_kit.rpy). The
# WORLD -- room shader, bodies, hazards, particles -- goes through the lens
# pass; the HUD is drawn after it. Nothing in here owns a rule: every value it
# reads is simulation state, and a frame is a pure function of it.
init python:
    class BIOStage(renpy.Displayable):
        """One creator-defined displayable. Steps BIOGame on a fixed 60Hz
        accumulator inside render() and paints from cached-texture blits."""

        _tf_cache = {}

        # Act one panels. Deliberately short and pushed to the bottom corners
        # so the Archivist is never boxed in by furniture (rule 2).
        PANEL_CMD = (40, 548, 470, 148)
        PANEL_HUD = (770, 548, 470, 148)

        # CHROME. Biography's windows are out of register like everything
        # else it touches: the border carries a red and a teal ghost of itself
        # two pixels either side, and the plate has scanlines.
        STYLE_PANEL = {"top": "#0d0a18e8", "bot": "#05030aee",
                       "edge": "#f2f4ffe0", "accent": "#5ce8d0ff",
                       "border": 1.6, "cut": 10.0, "inset": 6.0,
                       "inset_a": 0.16, "noise": 0.10, "scan": 0.12,
                       "split": 2.0, "ticks": 16.0}
        STYLE_PLATE = {"top": "#0b0814c8", "bot": "#05030ad8",
                       "edge": "#f2f4ff70", "accent": "#ff2d4eff",
                       "border": 1.0, "cut": 7.0, "inset": 4.0,
                       "inset_a": 0.0, "noise": 0.08, "scan": 0.10,
                       "split": 1.0, "ticks": 0.0}

        def __init__(self, game, **kwargs):
            super(BIOStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0

        # ----- cached factories ------------------------------------------------

        def _tf(self, key, builder):
            tf = BIOStage._tf_cache.get(key)
            if tf is None:
                if len(BIOStage._tf_cache) > 900:
                    BIOStage._tf_cache.clear()
                tf = builder()
                BIOStage._tf_cache[key] = tf
            return tf

        def _body_plate(self, zoom):
            # Shared with every other invasion -- see inv_body_plate(). The
            # margin is explicit and wide because inv.misreg pushes whole
            # colour channels off the silhouette; on the default padding the
            # red plate reached the rectangle and was cut in a straight line.
            return inv_body_plate(BIO_SPRITE, BIO_SPRITE_W, BIO_SPRITE_H, zoom,
                                pad_x=1.85, pad_y=1.45)

        def _body_plain(self, zoom, alpha=1.0, tint=None):
            """Ghost/afterimage copies, and the no-shader fallback."""
            ab = int(inv_clamp(alpha, 0.0, 1.0) * 6)
            key = ("plain", round(zoom, 3), ab, tint)

            def build():
                kw = dict(zoom=zoom, subpixel=True)
                if ab < 6:
                    kw["alpha"] = ab / 6.0
                if tint:
                    kw["matrixcolor"] = TintMatrix(tint)
                return Transform(BIO_SPRITE, **kw)
            return self._tf(key, build)

        def _zbucket(self, persp):
            """Quantised perspective, so a sprite that scales continuously with
            depth still shares a small, bounded set of cached transforms."""
            return int(inv_clamp(persp, 0.20, 1.40) * 8.0)

        def _zscale(self, zb):
            return zb / 8.0

        def _copy_tf(self, deg, zb=8):
            """A spectral duplicate of the glaive. Never the real one."""
            bucket = int(round(deg / BIO_ROT_STEP)) % BIO_ROT_BUCKETS
            return self._tf(("copy", bucket, zb), lambda: Transform(
                BIO_GLAIVE, zoom=BIO_GLAIVE_ZOOM * self._zscale(zb),
                rotate=bucket * BIO_ROT_STEP - BIO_GLAIVE_REST_DEG,
                alpha=0.78, matrixcolor=TintMatrix("#ff5a6e"), subpixel=True))

        def _blade_tf(self, deg, zb=8, fade=0):
            """The swung blade: a spectral pass of the glaive rather than a
            drawn line. `fade` indexes its after-images along the arc, which is
            what turns one blade into a swing."""
            bucket = int(round(deg / BIO_ROT_STEP)) % BIO_ROT_BUCKETS
            alpha = (0.92, 0.46, 0.24, 0.13)[min(fade, 3)]
            tint = ("#ffd8de", "#ff8496", "#ff5a6e", "#ff3d54")[min(fade, 3)]
            return self._tf(("blade", bucket, zb, fade), lambda: Transform(
                BIO_GLAIVE, zoom=BIO_GLAIVE_ZOOM * self._zscale(zb) * 1.25,
                rotate=bucket * BIO_ROT_STEP - BIO_GLAIVE_REST_DEG,
                alpha=alpha, matrixcolor=TintMatrix(tint), subpixel=True,
                blend=("add" if fade else None)))

        def _dagger_tf(self, deg, zb=8, alpha=1.0):
            bucket = int(round(deg / BIO_ROT_STEP)) % BIO_ROT_BUCKETS
            aq = int(inv_clamp(alpha, 0.0, 1.0) * 8)
            return self._tf(("dag", bucket, zb, aq), lambda: Transform(
                BIO_DAGGER, zoom=BIO_DAGGER_ZOOM * self._zscale(zb),
                nearest=True,
                rotate=bucket * BIO_ROT_STEP - BIO_DAGGER_REST_DEG,
                matrixcolor=TintMatrix(BIO_TEAL), alpha=aq / 8.0,
                subpixel=True))

        # ----- input -----------------------------------------------------------

        def event(self, ev, x, y, st):
            self.game.keys.handle_event(ev)
            return None

        # ----- the camera and the boards ---------------------------------------

        def _stage(self, g, sx, sy):
            """Where the camera is and how the boards are projected THIS frame.
            Act one is a low camera on the unlit stage, act two the proscenium,
            and the tear (g.corrupt) carries one into the other -- the horizon
            climbs, the floor flattens out, and the figure walks with it."""
            s = bio_smooth(inv_clamp(g.corrupt, 0.0, 1.0))
            hz = inv_lerp(BIO_A1_HORIZON, BIO_CAM_HORIZON, s)
            fk = inv_lerp(BIO_A1_FLOORK, BIO_FLOOR_K, s)
            c2 = g.cam_tuple()
            w = 1.0 - s
            t = g.clock
            # Act one has no camera body, but a dead-still lens over a living
            # room reads as a still picture. A slow sway on three unrelated
            # periods: the eye cannot learn it, and it carries the figure
            # with the floor it is standing on.
            roll = math.radians(0.50 * math.sin(t * 0.21) + 0.28 * math.sin(t * 0.37 + 1.3)) * w
            px = 10.0 * math.sin(t * 0.17 + 0.4) * w
            py = 4.0 * math.sin(t * 0.23 + 2.0) * w
            zm = 1.0 + 0.014 * math.sin(t * 0.19) * w
            cam = (c2[0] + roll, c2[1] + px, c2[2] + py, c2[3] * zm)
            return {"s": s, "hz": hz, "fk": fk, "cam": cam, "sx": sx, "sy": sy}

        def _proj(self, sp, wx, wy):
            x_, y_, pp = bio_project_hk(wx, wy, sp["hz"], sp["fk"])
            x_, y_ = bio_cam_apply(x_, y_, sp["cam"])
            return (x_ + sp["sx"], y_ + sp["sy"], pp)

        def _proj_h(self, sp, wx, wy, h):
            """For things off the boards (debris, sparks): unclamped depth and
            a height that foreshortens like everything else."""
            pp = bio_persp_free(wy)
            x_ = 640.0 + (wx - 640.0) * pp
            y_ = sp["hz"] + sp["fk"] * pp - h * pp
            x_, y_ = bio_cam_apply(x_, y_, sp["cam"])
            return (x_ + sp["sx"], y_ + sp["sy"], pp)

        def _figure(self, g, sp):
            """Act one / the tear: the figure's FEET on screen (pre-camera) and
            its zoom. It stands at BIO_A1_FIGURE in act one and walks to its
            act-two mark on the boards as the camera climbs."""
            s = sp["s"]
            fx1, fy1 = BIO_A1_FIGURE
            x2, y2, pp2 = bio_project_hk(g.bx, g.by, BIO_CAM_HORIZON, BIO_FLOOR_K)
            z2 = BIO_BOSS_ZOOM_ACT2 * (0.55 + 0.45 * pp2)
            return (inv_lerp(fx1, x2, s) + g.react, inv_lerp(fy1, y2, s),
                    inv_lerp(BIO_BOSS_ZOOM_ACT1, z2, s))

        # ----- the room --------------------------------------------------------

        def _room(self, g, p, sp, act_two):
            global BIO_SHADER_OK
            ax0, ay0, ax1, ay1 = BIO_ARENA
            u = {}
            off4 = (0.0, 0.0, 0.0, 0.0)
            rings = [off4] * 4
            rk = [0.0, 0.0, 0.0, 0.0]
            bars = [(-1.0, 0.0, 0.0, 0.0)] * 3
            blade = off4
            bladek = off4
            thrust = off4
            dag = [0.0] * 8
            dagk = [0.0] * 4
            poise = -1.0

            if act_two:
                bx, by = g.bx, g.by
                bglow = 0.50 + (0.45 if g._open_exposed() else 0.0)
                pglow = 0.55 + (0.35 if g.dashing else 0.0)
                ri = 0
                bi = 0
                for h in g.hazards:
                    if h["kind"] == "ring" and ri < 4:
                        rings[ri] = (float(h["x"]), float(h["y"]),
                                     float(h["r"]), float(h["w"]))
                        rk[ri] = 1.0 if h["warn"] > 0 else 2.0
                        ri += 1
                    elif h["kind"] == "bar" and bi < 3:
                        warning = h["warn"] > 0
                        if h["axis"] == "h":
                            pos = h["p"] if not warning else (ay0 if h["spd"] > 0 else ay1)
                        else:
                            pos = h["p"] if not warning else (ax0 if h["spd"] > 0 else ax1)
                        bars[bi] = (0.0 if h["axis"] == "h" else 1.0, float(pos),
                                    float(h["th"]), 1.0 if warning else 2.0)
                        bi += 1
                if g.b_move in ("sweep", "twirl") and g.b_state in ("wind", "act"):
                    arms = 1.0 if g.b_move == "sweep" else 2.0
                    if g.b_state == "act":
                        trail = 0.0
                        if g.blade_arc:
                            trail = bio_angdiff(g.blade, g.blade_arc[-1])
                        blade = (float(g.blade), float(trail), BIO_BLADE_INNER,
                                 BIO_BLADE_OUTER)
                        bladek = (arms, 1.0, BIO_BLADE_ARC, 0.0)
                    else:
                        warn_a = inv_clamp(g.b_t / float(max(1, g.b_len)), 0.0, 1.0)
                        blade = (float(g.blade), 0.0, BIO_BLADE_INNER, BIO_BLADE_OUTER)
                        bladek = (arms, 0.35 + 0.55 * warn_a, 5.0, 1.0)
                if g.b_move == "thrust" and g.b_state == "wind":
                    warn_a = inv_clamp(g.b_t / float(max(1, g.b_len)), 0.0, 1.0)
                    ang = math.degrees(math.atan2(g.py - g.by, g.px - g.bx))
                    thrust = (ang, 600.0, 0.35 + 0.65 * warn_a, 62.0)
                elif g.b_move == "thrust" and g.b_state == "act":
                    thrust = (float(g.aim), 220.0, 1.0, 86.0)
                leaving = g.mode in ("leave_w", "leave_l")
                if not leaving and g.b_state != "buckle":
                    poise = inv_clamp(g.poise_shown / g._poise_cap(), 0.0, 1.0)
                k = 0
                for d in g.daggers:
                    if d["state"] == "ground" and k < 4:
                        dag[k * 2] = float(d["x"])
                        dag[k * 2 + 1] = float(d["y"])
                        dagk[k] = 0.6 + 0.4 * math.sin(g.clock * 3.2 + d["x"] * 0.03)
                        k += 1
                pxw, pyw = g.px, g.py
            else:
                fx_, fy_, _z = self._figure(g, sp)
                bx, by = bio_unproject(fx_, fy_, sp["hz"], sp["fk"])
                bglow = 0.22 + 0.22 * g.windup + 0.28 * sp["s"]
                pxw, pyw = 0.0, 0.0
                pglow = 0.0

            if BIO_SHADER_OK:
                try:
                    quad = Transform(
                        inv_disp(BIO_SOUP_IMG), xysize=(1280, 720), mesh=True,
                        shader="inv.soup",
                        u_bio_res=(1280.0, 720.0),
                        u_bio_time=g.clock,
                        u_bio_corrupt=g.corrupt,
                        u_bio_pulse=inv_clamp(g.beat_pulse * (0.45 + 0.55 * g.corrupt), 0.0, 1.0),
                        u_bio_jolt=g.jolt,
                        u_bio_flash=g.flash,
                        u_bio_dark=g.dark,
                        u_bio_rush=g.rush,
                        u_bio_spin=g.spin,
                        u_bio_floor=1.0,
                        u_bio_horizon=sp["hz"],
                        u_bio_floork=sp["fk"],
                        u_bio_fscroll=g.rush * 0.35,
                        u_bio_fury=g.fury,
                        u_bio_cam=sp["cam"],
                        u_bio_hole=(float(g.hole[0]), float(g.hole[1]),
                                    float(g.hole[2]), float(g.hole[3])),
                        u_bio_stage=(float(inv_clamp(0.32 + 0.68 * g.stage_lit, 0.0, 1.0)),
                                     float(g.wave[0]), float(g.wave[1]),
                                     float(1.0 - sp["s"])),
                        u_bio_arena=(float(ax0), float(ay0), float(ax1), float(ay1)),
                        u_bio_persp=(BIO_PERSP_FAR, BIO_PERSP_NEAR),
                        u_bio_boss=(float(bx), float(by), float(bglow), float(poise)),
                        u_bio_plr=(float(pxw), float(pyw), float(pglow), 0.0),
                        u_bio_ring0=rings[0], u_bio_ring1=rings[1],
                        u_bio_ring2=rings[2], u_bio_ring3=rings[3],
                        u_bio_rings=tuple(rk),
                        u_bio_bar0=bars[0], u_bio_bar1=bars[1], u_bio_bar2=bars[2],
                        u_bio_blade=tuple(float(v) for v in blade),
                        u_bio_bladek=tuple(float(v) for v in bladek),
                        u_bio_thrust=tuple(float(v) for v in thrust),
                        u_bio_dag01=tuple(dag[0:4]),
                        u_bio_dag23=tuple(dag[4:8]),
                        u_bio_dagk=tuple(dagk))
                    # Through the Effects Resolution dial (perf.rpy). The one
                    # backdrop measured to pay for the capped pass's own
                    # render (Oct 9 2026, 1739x978 window, GPU per frame:
                    # 0.69ms native, 0.63ms at 720p, 0.48ms at 540p). The
                    # shader works in v_tex_coord and its own res uniform, so
                    # only the sampling density changes, never the layout.
                    r = renpy.render(msbf_fx_scaled(quad, 1280, 720, high_freq=True),
                                     1280, 720, p.st, p.at)
                    p.blit(r, (0, 0))
                    return
                except Exception as soup_e:
                    BIO_SHADER_OK = False
                    try:
                        renpy.log("INV FX: soup render failed: %r" % soup_e)
                    except Exception:
                        pass
            p.fill(BIO_BLACK, 0, 0, 1280, 720)

        def _look(self, g, sp):
            """The lens, per act. Act one is cold and a little soft; act two
            leans on everything as the entry fills (fury)."""
            s = sp["s"]
            fury = g.fury
            shock = (0.0, 0.0, 0.0, 0.0)
            if g.shock[3] > 0.004:
                if getattr(g, "shock_world", False):
                    hx, hy, _pp = self._proj_h(sp, g.shock[0], g.shock[1], 60.0)
                else:
                    hx, hy = g.shock[0] + sp["sx"], g.shock[1] + sp["sy"]
                shock = (hx, hy, g.shock[2], g.shock[3])
            return {
                "grade": (inv_lerp(1.02, 1.00, s), inv_lerp(1.05, 1.05, s),
                          inv_lerp(1.02, 0.94, s), 0.45),
                "lift": (inv_lerp(0.004, 0.018, s), 0.0, inv_lerp(0.018, 0.008, s)),
                "gain": (inv_lerp(0.98, 1.00, s), inv_lerp(1.00, 0.95, s),
                         inv_lerp(1.06, 0.98, s)),
                "bloom": inv_lerp(0.42, 0.40, s) + 0.20 * fury,
                "thresh": inv_lerp(0.62, 0.68, s),
                "ca": 0.0022 + 0.004 * s + 0.006 * fury + g.ca,
                "grain": 0.035 + 0.015 * s,
                "vig": 0.55 + 0.15 * s,
                "vigr": 1.08,
                "barrel": 0.020 + 0.030 * s + 0.040 * fury,
                "shock": shock,
                "tear": (inv_clamp(g.tear, 0.0, 1.0), float(g.tick // 3),
                         0.5 + 0.35 * math.sin(g.clock * 2.3), 0.45),
            }

        # ----- render ----------------------------------------------------------

        def render(self, width, height, st, at):
            g = self.game

            if self.last_st is None:
                self.last_st = st
            dt = st - self.last_st
            self.last_st = st
            dt = 0.0 if dt < 0.0 else (0.25 if dt > 0.25 else dt)

            if g.paused:
                self.acc = 0.0
            else:
                self.acc += dt
                steps = 0
                while self.acc >= INV_TICK and steps < INV_MAX_CATCHUP:
                    g.step()
                    self.acc -= INV_TICK
                    steps += 1
                if steps >= INV_MAX_CATCHUP:
                    self.acc = 0.0

            p = InvPaint(st, at)

            sx = sy = 0
            if g.shake > 0.01:
                amp = 13.0 * g.shake
                sx = int(math.sin(g.tick * 1.9) * amp)
                sy = int(math.cos(g.tick * 2.7) * amp * 0.6)

            sp = self._stage(g, sx, sy)
            act_two = (g.mode == "open"
                       or (g.mode in ("leave_w", "leave_l") and g.corrupt > 0.4))

            # --- the world (through the lens) -------------------------------
            self._room(g, p, sp, act_two)
            if act_two:
                self._open_world(g, p, sp)
            else:
                self._act_one_world(g, p, sp)
            inv_fx_paint(p, g.fx, "front", sx, sy)

            # --- the HUD (crisp, after the lens) ----------------------------
            p.to_hud()
            if act_two:
                self._open_hud(g, p, sp)
            else:
                self._act_one_hud(g, p, sx, sy)
            self._floats(g, p, sp)
            inv_fx_paint(p, g.fx, "hud")
            if g.paused:
                self._pause(g, p)

            rv = inv_compose(p, self._look(g, sp), g.clock)

            # THE DRAW RATE IS THE TICK RATE. Every pixel above is a pure
            # function of the simulation state, so between two 1/60s ticks
            # this stage paints a byte-identical picture -- asking for the
            # next frame immediately only made a high-refresh panel run the
            # whole draw two to four times per tick. Same governor as
            # kototouhou.rpy.
            if g.result is None and not g.paused:
                renpy.redraw(self, max(0.0, INV_TICK - self.acc))
            return rv

        # ----- the body --------------------------------------------------------

        def _draw_body(self, g, p, cx, cy, zoom, warp=1.0, rot=0.0,
                       stretch=(1.0, 1.0), diss=0.0, hurt=0.0,
                       tint=(1.0, 1.0, 1.0, 0.0), rim=(0.0, 0.0, 0.0, 0.0),
                       scan=(0.0, 0.0, 0.02, 0.0), reflect=0.0, feet=None):
            """Rule 3 lives here. One warped, contorting, banking body -- and,
            when it is standing on lacquered boards, its reflection."""
            plate, W, H = self._body_plate(zoom)
            slip = 0.30 + 0.60 * g.corrupt + 0.35 * g.fury
            mosh = 0.06 + 0.44 * g.corrupt + 0.34 * g.fury
            body = None
            if BIO_MISREG_OK:
                try:
                    body = bio_misreg(plate, W, H, g.clock, warp=warp, split=1.0,
                                      slip=slip, mosh=mosh, stretch=stretch,
                                      pivot=0.86, hurt=hurt, diss=diss,
                                      tint=tint, rim=rim, scan=scan)
                except Exception:
                    body = None
            if body is None and INV_FLESH_OK:
                body = inv_flesh(plate, W, H, g.clock, warp=warp, stretch=stretch,
                                 pivot=0.86, hurt=hurt, diss=diss)
            if body is None:
                body = self._body_plain(zoom)
            if abs(rot) > 0.05:
                body = Transform(body, rotate=rot, subpixel=True)
            try:
                if reflect > 0.01 and feet is not None:
                    # THE GLOSS. The same body, flipped about its own feet,
                    # foreshortened and faint. The plate centres the sprite,
                    # so its feet sit (H - h) / 2 above the plate's bottom.
                    k = 0.56
                    rd = Transform(body, yzoom=-k, alpha=reflect, subpixel=True)
                    rr = renpy.render(rd, W, int(H * k) + 4, p.st, p.at)
                    rw, rh = rr.get_size()
                    h_body = BIO_SPRITE_H * zoom
                    p.sblit(rr, (cx - rw * 0.5, feet - k * (H - h_body) * 0.5))
                r = renpy.render(body, W, H, p.st, p.at)
                w, h = r.get_size()
                p.sblit(r, (cx - w * 0.5, cy - h * 0.5))
            except Exception as e:
                try:
                    renpy.log("INV FX: body render failed: %r" % e)
                except Exception:
                    pass
            return body

        def _draw_heart(self, g, p, cx, cy, scale=1.0):
            """The player's avatar in a corruptive state: the SOUL heart the
            other game modes run on, put through the shared shader and warped
            harder than anything else on screen. It beats -- squashing on the
            downbeat -- and it is never drawn clean."""
            plate, W, H = inv_body_plate(INV_HEART, INV_HEART_W, INV_HEART_H,
                                        BIO_HEART_ZOOM * max(0.18, scale),
                                        pad_x=2.2, pad_y=2.2, nearest=True)
            beat = 1.0 - 0.16 * g.beat_pulse
            p.glow(cx, cy, 30 * scale, 30 * scale, col="#ff3a56", alpha=0.35)
            if INV_FLESH_OK:
                try:
                    d = inv_flesh(plate, W, H, g.clock * 2.3,
                                warp=BIO_HEART_WARP, split=0.85,
                                stretch=(1.0 / max(0.5, beat), beat),
                                pivot=0.5, hurt=0.0,
                                diss=0.04 + 0.04 * math.sin(g.clock * 3.1))
                    r = renpy.render(d, W, H, p.st, p.at)
                    w, h = r.get_size()
                    p.sblit(r, (cx - w * 0.5, cy - h * 0.5))
                    return
                except Exception:
                    pass
            hz = BIO_HEART_ZOOM * max(0.18, scale)
            heart = self._tf(("heartplain", round(hz, 2)),
                             lambda z=hz: Transform(INV_HEART, zoom=z,
                                                    nearest=True, subpixel=True))
            r, (w, h) = p.tex(("heartplain", round(hz, 2)), heart, 160, 160)
            p.sblit(r, (cx - w * 0.5, cy - h * 0.5))

        # ----- ACT ONE ---------------------------------------------------------

        def _act_one_world(self, g, p, sp):
            """The figure stands on its stage. The boards are unlit; the room's
            own light rims it; a shadow and a reflection put it ON the floor
            rather than in front of the picture of one."""
            arriving = (g.mode == "arrive")
            fx_, fy_, zoom = self._figure(g, sp)
            cam = sp["cam"]
            czoom = cam[3]
            zoom *= czoom
            body_h = BIO_SPRITE_H * zoom
            # It hovers -- it always has -- a little, and the shadow says so.
            bob = (math.sin(g.clock * 1.15) * 6.0 - 6.0) * (1.0 - sp["s"])
            feet_x, feet_y = bio_cam_apply(fx_, fy_, cam)
            feet_x += sp["sx"]
            feet_y += sp["sy"]
            cy = feet_y - body_h * 0.5 + bob
            if arriving:
                # IT ARRIVES AT ITS RESTING POSITION: the rest pose lerped
                # toward the hole by `emerge`, which is driven to exactly 0 at
                # the end of the arrival -- the last arrival frame IS the
                # resting frame, whatever either value is later tuned to.
                cy = inv_lerp(cy, g.hole[1] + 40.0, g.emerge)
                stretch = (1.0 / max(0.35, g.body_scale) ** 0.4, g.body_scale)
                warp = 1.0 + 1.0 * g.emerge
                diss = g.emerge * 0.85
            else:
                stretch = (g.body_sx, g.body_sy)
                # Act one is a plate VERY SLIGHTLY out of register; a hit or a
                # wind-up throws it further, and act two is where it comes
                # apart.
                warp = (0.30 + 0.18 * math.sin(g.clock * 0.7)
                        + 0.9 * g.boss_flash + 0.5 * g.windup)
                diss = 0.0

            inv_fx_paint(p, g.fx, "back", sp["sx"], sp["sy"])

            # Its own light under it, and the shadow it casts.
            standing = 1.0 - (g.emerge if arriving else 0.0)
            if standing > 0.02:
                p.shadow(feet_x, feet_y + 3.0, 150.0 * zoom / 0.30,
                         26.0 * zoom / 0.30, alpha=0.62 * standing)

            # The wind-up: a glow gathering behind it, in the colour of what
            # it is about to do (gold: not an attack this turn; red: one).
            glow_a = g.windup * 0.55
            if g.telegraph:
                glow_a = max(glow_a, 0.30 + 0.20 * math.sin(g.clock * 6.0))
            if glow_a > 0.02:
                col = BIO_WARN if (g.telegraph or g.windup_col == BIO_WARN) else BIO_RED
                p.glow(feet_x, cy, 230.0 * zoom / 0.30, 300.0 * zoom / 0.30,
                       col=col, alpha=glow_a)

            scan = (0.0, 0.0, 0.02, 0.0)
            if g.scan >= 0.0:
                scan = (1.0 - g.scan, 0.9 * inv_clamp(1.25 - g.scan, 0.0, 1.0), 0.03, 0.0)
            pull = -g.windup * 4.0
            self._draw_body(
                g, p, feet_x, cy, zoom, warp=warp,
                rot=g.boss_pose * 3.0 + pull,
                stretch=(stretch[0] * (1.0 - 0.05 * g.windup),
                         stretch[1] * (1.0 + 0.06 * g.windup)),
                diss=diss, hurt=0.85 if g.boss_flash > 0.4 else 0.0,
                tint=inv_lerp_tint((0.86, 0.92, 1.10), (1.06, 0.86, 0.90), sp["s"]),
                rim=inv_lerp_rim((0.45, 0.62, 1.0, 0.55), (1.0, 0.25, 0.38, 0.70), sp["s"]),
                scan=scan, reflect=(0.20 * standing if not arriving else 0.0),
                feet=feet_y)

        def _act_one_hud(self, g, p, sx, sy):
            if g.mode == "arrive":
                return

            # --- the only chrome act one gets ------------------------------------
            # A name and a bar, both small, both far from the sprite. The bar is
            # empty until CHECK has been used -- and then it is READ in, left to
            # right, the way a scan would find it.
            inv_draw_panel(p, 370, 16, 540, 54, BIOStage.STYLE_PLATE)
            p.text("BIOGRAPHY", 15, BIO_RED, 386, 22, bold=True, w=300, h=30,
                   outline="#04030a")
            bar_w = 508
            p.fill("#1a0610", 386, 48, bar_w, 9)
            if g.boss_known:
                p.fill(BIO_RED_DEEP, 386, 48, int(bar_w * g.bar_reveal), 9)
                fill = int(bar_w * g.bar_reveal * inv_clamp(
                    g.boss_shown / float(BIO_BOSS_HP_MAX), 0.0, 1.0))
                if fill > 0:
                    p.fill(BIO_RED, 386, 48, fill, 9)
                    p.fill("#ffffff60", 386, 48, fill, 2)
                for k in range(1, 10):
                    p.fill("#04030ab0", 386 + int(bar_w * k / 10.0), 48, 1, 9)
                mark = 386 + int(bar_w * BIO_SHIFT_HP / float(BIO_BOSS_HP_MAX))
                p.fill(BIO_WARN + "c0", mark, 45, 2, 15)
            else:
                for k in range(0, bar_w, 12):
                    p.fill("#ff2d4e22", 386 + k, 51, 6, 3)

            # THE TURN LOG. Top right, clear of the figure; it is where a slow
            # reader finds what the last turn did while choosing this one.
            inv_draw_log(p, g, 930, 20, 310,
                         {"you": (BIO_INK, BIO_TEAL), "it": (BIO_RED, BIO_WARN)})

            slide = int(g.panel_slide * 200)
            if g.panel_slide < 1.0:
                kick = g.panel_kick
                kx = int(math.sin(g.tick * 2.3) * 9.0 * max(0.0, kick))
                ky = int(abs(kick) * 4.0)
                self._panel(g, p, BIOStage.PANEL_CMD, sx, sy + slide)
                self._panel(g, p, BIOStage.PANEL_HUD, sx + kx, sy + slide + ky,
                            hit=kick)
                self._panel_contents(g, p, sx, sy + slide, kx, ky)

        def _panel(self, g, p, box, sx, sy, hit=0.0):
            x, y, w, h = box
            inv_draw_panel(p, x + sx, y + sy, w, h, BIOStage.STYLE_PANEL)
            if hit > 0.05:
                p.fill(inv_hex(BIO_RED, 0.45 * hit), x + sx, y + sy, w, h)
            elif hit < -0.05:
                p.fill(inv_hex(BIO_TEAL, 0.30 * -hit), x + sx, y + sy, w, h)

        def _panel_contents(self, g, p, sx, sy, kx=0, ky=0):
            cx, cy, cw, ch = BIOStage.PANEL_CMD
            cx += sx
            cy += sy

            if g.mode in ("menu", "sub"):
                rows = BIO_CMDS if g.mode == "menu" else BIO_RECALLS
                cursor = g.cursor if g.mode == "menu" else g.sub_cursor
                for i, row in enumerate(rows):
                    live = (i == cursor)
                    ry = cy + 18 + i * 30
                    if live:
                        p.fill(BIO_INK + "1c", cx + 14, ry - 4, cw - 28, 27)
                        p.fill(BIO_TEAL, cx + 14, ry - 4, 3, 27)
                        p.quad("glow", cx + 30, ry + 9, 0.16, col=BIO_TEAL,
                               alpha=0.8, add=True)
                        p.fill(BIO_TEAL, cx + 26, ry + 5, 8, 8)
                    p.text(row[1], 20, BIO_INK if live else BIO_FAINT,
                           cx + 46, ry, bold=live, w=260, h=30, outline="#04030a")
                    if g.mode == "sub" and row[2]:
                        p.text(str(row[2]) + " PP", 14,
                               BIO_TEAL if live else BIO_FAINT,
                               cx + cw - 22, ry + 4, anchor=(1.0, 0.0), w=120, h=26)
                p.text("Z  OK      X  BACK      ESC  PAUSE", 12, BIO_FAINT,
                       cx + cw - 16, cy + ch - 22, anchor=(1.0, 0.0), w=420, h=24)

            elif g.mode == "beat":
                # The resolved action, large -- for exactly as long as the
                # beat holds. It is in the log after that.
                u = inv_clamp(g.mtick / 6.0, 0.0, 1.0)
                p.text(g.beat_label, 22, BIO_INK, cx + 22, cy + 28, bold=True,
                       w=cw - 40, h=40, outline="#04030a")
                if g.beat_value:
                    p.text(g.beat_value, int(24 + 8 * u), BIO_WARN, cx + 22,
                           cy + 62, bold=True, w=cw - 40, h=48, outline="#04030a")
                hold = inv_clamp(g.mtick / float(INV_BEAT_HOLD), 0.0, 1.0)
                p.fill(BIO_FAINT + "60", cx + 22, cy + ch - 18, cw - 44, 2)
                p.fill(BIO_TEAL, cx + 22, cy + ch - 18, int((cw - 44) * hold), 2)

            elif g.mode == "enemy":
                # Its turn: no readout, the figure is the readout. A thin
                # gathering line says something is coming.
                u = inv_clamp(g.mtick / 26.0, 0.0, 1.0)
                col = BIO_WARN if g.windup_col == BIO_WARN else BIO_RED
                p.text("BIOGRAPHY", 18, col, cx + 22, cy + 30, bold=True,
                       w=cw - 40, h=34, outline="#04030a")
                p.fill(col + "50", cx + 22, cy + 70, cw - 44, 2)
                p.fill(col, cx + 22, cy + 70, int((cw - 44) * u), 2)

            # --- status ---------------------------------------------------------
            hx, hy, hw, hh = BIOStage.PANEL_HUD
            hx += sx + kx
            hy += sy + ky
            p.text(inv_player_name(), 19, BIO_INK, hx + 22, hy + 12,
                   bold=True, w=hw - 40, h=32, outline="#04030a")
            self._odometer(g, p, "HP", g.hp_shown, g.hp, hx + 22, hy + 44,
                           BIO_INK)
            self._odometer(g, p, "PP", g.pp_shown, g.pp, hx + 22, hy + 96,
                           BIO_TEAL, small=True)
            if g.telegraph:
                a = 0.6 + 0.4 * math.sin(g.clock * 7.0)
                p.text("INCOMING", 13, inv_hex(BIO_WARN, a), hx + hw - 22, hy + 16,
                       anchor=(1.0, 0.0), w=200, h=26, bold=True)
            if g.guard:
                p.text("GUARD", 12, BIO_TEAL, hx + hw - 22, hy + 40,
                       anchor=(1.0, 0.0), w=200, h=24)
            if g.god:
                p.text("GOD", 12, BIO_WARN + "aa", hx + hw - 22, hy + hh - 24,
                       anchor=(1.0, 0.0), w=120, h=24)

        def _odometer(self, g, p, label, shown, real, x, y, color, small=False):
            """An EarthBound counter: fixed-width cells, and the digits that are
            moving are drawn mid-roll rather than swapped."""
            size = 22 if small else 30
            cell_w = 22 if small else 28
            cell_h = 32 if small else 42
            p.text(label, 14, color, x, y + (6 if small else 12), bold=True,
                   w=50, h=28)
            value = int(math.ceil(shown - 0.0001)) if shown > 0 else 0
            rolling = abs(shown - real) > 0.05
            digits = "%03d" % inv_clamp(value, 0, 999)
            frac = shown - math.floor(shown)
            base_x = x + 40
            for i, ch in enumerate(digits):
                dx = base_x + i * cell_w
                p.fill("#120d1ee8", dx, y, cell_w - 4, cell_h)
                p.fill("#ffffff10", dx, y, cell_w - 4, 1)
                if rolling:
                    off = int(frac * cell_h * (1 if real < shown else -1))
                    nxt = str((int(ch) + (1 if real > shown else -1)) % 10)
                    p.text(nxt, size, inv_hex(color, 0.45), dx + (cell_w - 4) // 2,
                           y + off - (cell_h if real < shown else -cell_h) + 2,
                           anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)
                    p.text(ch, size, color, dx + (cell_w - 4) // 2, y + off + 2,
                           anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)
                else:
                    p.text(ch, size, color, dx + (cell_w - 4) // 2, y + 2,
                           anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)

        # ----- ACT TWO ---------------------------------------------------------

        def _open_world(self, g, p, sp):
            """Act two, drawn on a stage. The simulation is still the flat
            plane it always was -- world y is depth, and only the renderer
            knows that. The hazards are already on the boards (the room
            shader paints them); everything that STANDS is projected and drawn
            far first, because depth sorting is what sells the third
            dimension."""
            ax0, ay0, ax1, ay1 = BIO_ARENA
            proj = lambda wx, wy: self._proj(sp, wx, wy)
            projh = lambda wx, wy, h: self._proj_h(sp, wx, wy, h)
            exposed = g._open_exposed()
            leaving = g.mode in ("leave_w", "leave_l")

            # --- the boards' edge: four projected corners, a thin red line --
            c = [proj(ax0, ay0), proj(ax1, ay0), proj(ax1, ay1), proj(ax0, ay1)]
            for i in range(4):
                a_, b_ = c[i], c[(i + 1) % 4]
                p.line(a_[0], a_[1], b_[0], b_[1], width=1.4, col=BIO_RED,
                       alpha=0.45, add=True)

            # --- the bars rise as CURTAINS of light off their floor line ----
            for h in g.hazards:
                if h["kind"] != "bar":
                    continue
                warning = h["warn"] > 0
                col = BIO_WARN if warning else BIO_RED
                a = (0.14 + 0.12 * math.sin(g.tick * 0.6)) if warning else 0.30
                for k in range(7):
                    u = (k + 0.5) / 7.0
                    if h["axis"] == "h":
                        wy = h["p"] if not warning else (ay0 if h["spd"] > 0 else ay1)
                        wx = inv_lerp(ax0, ax1, u)
                    else:
                        wx = h["p"] if not warning else (ax0 if h["spd"] > 0 else ax1)
                        wy = inv_lerp(ay0, ay1, u)
                    x0_, y0_, pp = projh(wx, wy, 0.0)
                    x1_, y1_, _pp = projh(wx, wy, 120.0)
                    p.line(x0_, y0_, x1_, y1_, width=4.0 * pp + 1.0, col=col,
                           alpha=a * (0.5 + 0.5 * pp), add=True, tex="beam")

            inv_fx_paint(p, g.fx, "w_floor", proj=projh)

            # --- the blade itself, riding at hand height ---------------------
            # Spectral passes of the glaive per arm, after-images trailing back
            # along the arc, billboarded: its on-screen angle is measured from
            # the projected inner and outer points, so a blade pointing away
            # from the camera foreshortens like everything else. (The
            # FOOTPRINT -- the hitbox -- is on the boards, in the shader.)
            if g.b_state == "act" and g.b_move in ("sweep", "twirl"):
                trail_angs = [g.blade] + list(g.blade_arc[:3])
                for fade, ang in enumerate(trail_angs):
                    arms = ((ang,) if g.b_move == "sweep" else (ang, ang + 180.0))
                    for arm in arms:
                        rad = math.radians(arm)
                        ix, iy, ip = proj(g.bx + math.cos(rad) * BIO_BLADE_INNER,
                                          g.by + math.sin(rad) * BIO_BLADE_INNER)
                        ox, oy, op = proj(g.bx + math.cos(rad) * BIO_BLADE_OUTER,
                                          g.by + math.sin(rad) * BIO_BLADE_OUTER)
                        pmid = (ip + op) * 0.5
                        sang = math.degrees(math.atan2(oy - iy, ox - ix))
                        zb = self._zbucket(pmid * 1.2)
                        bucket = int(round(sang / BIO_ROT_STEP)) % BIO_ROT_BUCKETS
                        br, (bw2, bh2) = p.tex(("blade", bucket, zb, fade),
                                               self._blade_tf(sang, zb, fade), 560, 560)
                        bxm = (ix + ox) * 0.5
                        bym = (iy + oy) * 0.5 - BIO_BLADE_LIFT * pmid
                        if fade == 0:
                            p.glow(bxm, bym, 120 * pmid, 60 * pmid, col=BIO_RED,
                                   alpha=0.5)
                        p.sblit(br, (bxm - bw2 * 0.5, bym - bh2 * 0.5))

            # --- everything that STANDS on the floor, sorted far to near -----
            draw = []
            for h in g.hazards:
                if h["kind"] in ("copy", "orbit"):
                    draw.append((h["y"], 0, h))
            for d in g.daggers:
                if d["state"] == "flight":
                    draw.append((d["y"], 1, d))
                elif d["state"] == "ground":
                    draw.append((d["y"], 2, d))
            for d in g.debris:
                draw.append((d["y"], 3, d))
            draw.append((g.by, 4, None))
            draw.append((g.py, 5, None))
            draw.sort(key=lambda e: e[0])

            # Shadows go down before any body does, so every figure is drawn
            # standing on its own.
            def contact(wx, wy, radius, alpha):
                cxp, cyp, pp = proj(wx, wy)
                p.shadow(cxp, cyp, radius * pp, radius * pp * 0.34, alpha=alpha)

            contact(g.bx, g.by, 104.0, 0.55)
            contact(g.px, g.py, 26.0, 0.45)
            for h in g.hazards:
                if h["kind"] in ("copy", "orbit"):
                    contact(h["x"], h["y"], 34.0, 0.30)
            for d in g.daggers:
                if d["state"] == "ground":
                    contact(d["x"], d["y"], 15.0, 0.34)

            debris_col = "#ffb9c6" if g.corrupt > 0.5 else "#dfe9ff"
            for _wy, kind, item in draw:
                if kind == 3:
                    # Suspended matter, standing off the boards at its own
                    # height: brighter and bigger as it comes downstage, and it
                    # blows past the lens -- the cue that makes the room a
                    # volume.
                    dxp, dyp, pp = projh(item["x"], item["y"], item["h"])
                    if not (-90 < dxp < 1370 and -90 < dyp < 810):
                        continue
                    size = item["s"] * pp * (0.55 + 0.45 * item["w"])
                    a = inv_clamp((0.12 + 0.48 * pp) * item["w"]
                                  * (0.7 + 0.3 * math.sin(g.clock * 1.7 + item["p"])),
                                  0.0, 0.85)
                    p.quad("dust", dxp, dyp, size * 0.22, col=debris_col,
                           alpha=a, add=True)
                    if pp > 0.86 and size > 4:
                        streak = max(2.0, abs(item["vy"]) * 7.0 * pp)
                        p.quad("spark", dxp, dyp - streak * 0.5, size * 0.02 + streak / 128.0,
                               0.06 + size * 0.008, rot=90.0, col=debris_col,
                               alpha=a * 0.6, add=True)

                elif kind == 2:
                    # A dagger lying where it came to rest, with a beacon of
                    # the player's colour standing up off it so the
                    # ammunition can be found across a loud floor.
                    gx_, gy_, pp = proj(item["x"], item["y"])
                    puls = 0.5 + 0.5 * math.sin(g.clock * 3.2 + item["x"] * 0.03)
                    p.line(gx_, gy_, gx_, gy_ - (46.0 + 18.0 * puls) * pp,
                           width=3.0 * pp + 1.0, col=BIO_TEAL,
                           alpha=0.35 + 0.30 * puls, add=True)
                    p.glow(gx_, gy_, 20.0 * pp, 8.0 * pp, col=BIO_TEAL,
                           alpha=0.6 + 0.3 * puls)
                    zb = self._zbucket(pp * 0.8)
                    dr, (dw, dh) = p.tex(("dag", int(round(-58.0 / BIO_ROT_STEP))
                                          % BIO_ROT_BUCKETS, zb, 8),
                                         self._dagger_tf(-58.0, zb), 140, 140)
                    p.sblit(dr, (gx_ - dw * 0.5, gy_ - dh * 0.5 - 9 * pp))

                elif kind == 0:
                    cx_, cy_, pp = proj(item["x"], item["y"])
                    zb = self._zbucket(pp)
                    p.glow(cx_, cy_ - 30 * pp, 64.0 * pp, 64.0 * pp,
                           col="#ff3a56", alpha=0.45)
                    cr, (cw2, ch2) = p.tex(("copy", int(round(item["spin"] / BIO_ROT_STEP))
                                            % BIO_ROT_BUCKETS, zb),
                                           self._copy_tf(item["spin"], zb), 520, 520)
                    p.sblit(cr, (cx_ - cw2 * 0.5, cy_ - ch2 * 0.5 - 30 * pp))

                elif kind == 1:
                    dx_, dy_, pp = projh(item["x"], item["y"], 20.0)
                    zb = self._zbucket(pp)
                    p.glow(dx_, dy_, 18.0 * pp, 18.0 * pp, col=BIO_TEAL, alpha=0.7)
                    dr, (dw, dh) = p.tex(("dag", int(round(item["ang"] / BIO_ROT_STEP))
                                          % BIO_ROT_BUCKETS, zb, 8),
                                         self._dagger_tf(item["ang"], zb), 140, 140)
                    p.sblit(dr, (dx_ - dw * 0.5, dy_ - dh * 0.5))

                elif kind == 4:
                    bx_, by_, pp = proj(g.bx, g.by)
                    zoom = BIO_BOSS_ZOOM_ACT2 * (0.55 + 0.45 * pp) * sp["cam"][3]
                    # Afterimages first, so the live body sits on top of them.
                    for i, (gx, gy, grot, gsc) in enumerate(g.ghosts):
                        a = 0.22 * (1.0 - i / float(len(g.ghosts) + 1))
                        ggx, ggy, gpp = proj(gx, gy)
                        gz = BIO_BOSS_ZOOM_ACT2 * (0.55 + 0.45 * gpp) * sp["cam"][3]
                        gr, (gw, gh) = p.tex(("ghost", round(gz, 3), i),
                                             self._body_plain(gz, alpha=a,
                                                              tint="#ff6a7e"),
                                             900, 900)
                        p.sblit(gr, (ggx - gw * 0.5, ggy - gh))
                    body_h = BIO_SPRITE_H * zoom
                    if exposed:
                        p.glow(bx_, by_ - body_h * 0.45, 170.0 * pp, 230.0 * pp,
                               col=BIO_WARN, alpha=0.30 + 0.15 * math.sin(g.tick * 0.45))
                    self._draw_body(
                        g, p, bx_, by_ - body_h * 0.5, zoom,
                        warp=(0.70 if not g.last_page else 1.10),
                        rot=inv_clamp(math.sin(math.radians(g.body_rot)) * 11.0,
                                      -11.0, 11.0),
                        stretch=(g.body_sx, g.body_sy),
                        diss=(g.emerge if leaving else 0.0),
                        hurt=0.9 if g.boss_flash > 0.45 else 0.0,
                        tint=((1.10, 0.92, 0.80, 1.0) if exposed
                              else (1.06, 0.84, 0.90, 1.0)),
                        rim=(1.0, 0.25, 0.40, 0.75 + 0.5 * g.fury),
                        reflect=0.18 * (1.0 - (g.emerge if leaving else 0.0)),
                        feet=by_)

                elif kind == 5:
                    px_, py_, pp = proj(g.px, g.py)
                    for i, (tx, ty, dashing) in enumerate(g.trail):
                        if i == 0:
                            continue
                        a = 0.34 * (1.0 - i / float(len(g.trail)))
                        if dashing:
                            a *= 1.8
                        ttx, tty, tpp = proj(tx, ty)
                        p.quad("core", ttx, tty - 26 * tpp, (0.34 - i * 0.02) * tpp,
                               col="#ff4a5e", alpha=a, add=True)
                    blink = (g.iframe > 0 and (g.tick // 3) % 2 == 0)
                    if not blink:
                        self._draw_heart(g, p, px_, py_ - 26 * pp, scale=pp)

            # --- OCCLUSION. Standing upstage of it puts its body between you
            # and the camera, and losing your own avatar behind the boss is a
            # defect, not a difficulty: a ghost of the heart is drawn on top.
            if g.py < g.by:
                pxs, pys, ppp = proj(g.px, g.py)
                bxs, bys, bpp = proj(g.bx, g.by)
                body_w = BIO_SPRITE_W * BIO_BOSS_ZOOM_ACT2 * (0.55 + 0.45 * bpp)
                body_h = BIO_SPRITE_H * BIO_BOSS_ZOOM_ACT2 * (0.55 + 0.45 * bpp)
                if (abs(pxs - bxs) < body_w * 0.42 and bys - body_h < pys < bys + 40):
                    p.quad("core", pxs, pys - 26 * ppp, 0.55, col=BIO_TEAL,
                           alpha=0.9, add=True)
                    p.ring(pxs, pys - 26 * ppp, 14.0, col=BIO_TEAL, alpha=0.9)

            # --- DISCHARGE. Drawn over the figures on purpose: a bolt is light,
            # and light does not queue behind the thing it is lighting.
            for a_ in g.arcs:
                age = g.tick - a_["born"]
                if age < 0 or age >= a_["ttl"]:
                    continue
                axp, ayp, app_ = projh(a_["x"], a_["y"], a_["h"])
                if not (-260 < axp < 1540 and -160 < ayp < 880):
                    continue
                fr = 1.0 - (age / float(a_["ttl"]))
                L = max(40.0, a_["len"] * app_)
                frame = INV_BOLTS[(a_["seed"] + age // 2) % len(INV_BOLTS)]
                bw, bh = inv_fx_size(frame)
                p.quad(frame, axp, ayp, L / bw, max(0.4, L * 0.16 * a_["w"] / bh),
                       rot=math.degrees(a_["ang"]), col=BIO_TEAL,
                       alpha=0.45 + 0.55 * fr, add=True, rstep=6.0)
                p.glow(axp, ayp, L * 0.35, L * 0.12, col=BIO_TEAL, alpha=0.18 * fr)

            inv_fx_paint(p, g.fx, "w_front", proj=projh)

        def _open_hud(self, g, p, sp):
            exposed = g._open_exposed()
            fade = 1.0
            if g.mode in ("leave_w", "leave_l"):
                fade = inv_clamp(1.0 - g.mtick / 60.0, 0.0, 1.0)
            if fade <= 0.02:
                return

            if exposed:
                bx_, by_, pp = self._proj(sp, g.bx, g.by)
                pulse = 0.5 + 0.5 * math.sin(g.tick * 0.45)
                p.text("OVER-EXTENDED", 15, inv_hex(BIO_WARN, (0.55 + 0.45 * pulse) * fade),
                       int(bx_), int(by_ - BIO_SPRITE_H * BIO_BOSS_ZOOM_ACT2
                                     * (0.55 + 0.45 * pp)) - 26,
                       bold=True, anchor=(0.5, 0.0), w=340, h=34, outline="#04030a")

            # --- the top plate: health, composure, the entry -----------------
            bar_w = 620
            bx0 = 640 - bar_w // 2
            inv_draw_panel(p, bx0 - 16, 6, bar_w + 32, 66, BIOStage.STYLE_PLATE)
            p.text("BIOGRAPHY", 13, BIO_RED, bx0, 12, bold=True, w=300, h=26,
                   outline="#04030a")
            p.fill("#2a0712", bx0, 32, bar_w, 10)
            fill = int(bar_w * inv_clamp(g.boss_shown / float(BIO_BOSS_HP_MAX), 0.0, 1.0))
            if fill > 0:
                p.fill(BIO_RED, bx0, 32, fill, 10)
                p.fill("#ffffff55", bx0, 32, fill, 2)
            for k in range(1, 10):
                p.fill("#04030ac0", bx0 + int(bar_w * k / 10.0), 32, 1, 10)
            last = bx0 + int(bar_w * BIO_LAST_PAGE_HP / float(BIO_BOSS_HP_MAX))
            p.fill(BIO_WARN + "b0", last, 29, 2, 16)

            # POISE, directly under its health, in the player's colour: the bar
            # you are actually playing against between buckles.
            pf = inv_clamp(g.poise_shown / g._poise_cap(), 0.0, 1.0)
            p.fill("#0d1a1a", bx0, 46, bar_w, 6)
            if g.b_state == "buckle":
                flick = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(g.tick * 0.9))
                p.fill(inv_hex(BIO_WARN, flick), bx0, 46, bar_w, 6)
            else:
                pfill = int(bar_w * pf)
                if pfill > 0:
                    p.fill(BIO_TEAL if pf > 0.30 else BIO_WARN, bx0, 46, pfill, 6)

            # THE ENTRY: the third way this ends, and the only one not yours.
            ef = inv_clamp(g.entry_shown / BIO_ENTRY_MAX, 0.0, 1.0)
            p.fill("#1b1420", bx0, 56, bar_w, 4)
            efill = int(bar_w * ef)
            if efill > 0:
                hot = ef > 0.72
                ecol = BIO_WARN if not hot else ("#ffffff" if (g.tick // 8) % 2 == 0 else BIO_WARN)
                p.fill(ecol, bx0, 56, efill, 4)
            p.text("ENTRY", 10, inv_hex(BIO_WARN, 0.30 + 0.55 * ef),
                   bx0 + bar_w + 8, 53, w=140, h=22)
            if exposed:
                pulse = 0.5 + 0.5 * math.sin(g.tick * 0.4)
                p.text("EXPOSED", 13, inv_hex(BIO_WARN, 0.4 + 0.6 * pulse),
                       bx0 + bar_w, 12, bold=True, anchor=(1.0, 0.0), w=220, h=26)
            if ef > 0.72:
                # The edges of the frame warm as the entry nears completion.
                hot_a = (ef - 0.72) / 0.28 * (0.5 + 0.5 * math.sin(g.tick * 0.25))
                p.fill(inv_hex(BIO_WARN, 0.10 * hot_a), 0, 0, 1280, 6)
                p.fill(inv_hex(BIO_WARN, 0.10 * hot_a), 0, 714, 1280, 6)

            # --- you ---------------------------------------------------------
            hud = (24, 618, 300, 80)
            inv_draw_panel(p, hud[0], hud[1], hud[2], hud[3], BIOStage.STYLE_PANEL)
            self._odometer(g, p, "HP", g.hp_shown, g.hp, hud[0] + 18, hud[1] + 18,
                           BIO_INK)

            px0, py0 = 344, 660
            p.text("DASH", 11, BIO_FAINT, px0, py0 - 17, w=90, h=22)
            pw = 150
            p.fill("#0a0812c8", px0, py0, pw, 8)
            if g.dashing:
                frac = 1.0 - (g.dash_t / float(BIO_DASH_MAX))
                col = BIO_INK
            elif g.dash_cd > 0:
                frac = 1.0 - (g.dash_cd / float(BIO_DASH_CD))
                col = "#2f7d72"
            else:
                frac = 1.0
                col = BIO_TEAL
            p.fill(col, px0, py0, max(0, int(pw * frac)), 8)

            # THE FOUR DAGGERS, as four small daggers: bright in your hand, dim
            # if they are out there somewhere.
            qx0, qy0 = 352, 622
            for i, d in enumerate(g.daggers):
                held = d["state"] == "held"
                a = 1.0 if held else (0.40 if d["state"] == "flight" else 0.22)
                dr, (dw, dh) = p.tex(("daghud", held, int(a * 8)),
                                     self._dagger_tf(-90.0, 8, a), 80, 80)
                p.sblit(dr, (qx0 + i * 20 - dw * 0.5, qy0 - dh * 0.5 + 6))
                if held:
                    p.quad("glow", qx0 + i * 20, qy0 + 6, 0.16, col=BIO_TEAL,
                           alpha=0.35, add=True)

            p.text("MOVE  WASD      Z  THROW      X  DASH  (HOLD)", 12,
                   BIO_FAINT, 1256, 690, anchor=(1.0, 1.0), w=760, h=28,
                   outline="#04030a")
            if g.god:
                p.text("GOD", 12, BIO_WARN + "aa", 1256, 664, anchor=(1.0, 1.0),
                       w=120, h=24)

        # ----- numbers and pause -----------------------------------------------

        def _floats(self, g, p, sp):
            for f in g.floats:
                a = inv_clamp(f["life"] / 26.0, 0.0, 1.0)
                age = 52 - f["life"]
                pop = 1.0 + 0.35 * inv_clamp(1.0 - age / 6.0, 0.0, 1.0)
                if f.get("world"):
                    fx_, fy_, fpp = self._proj_h(sp, f["x"], f["y"], 0.0)
                    size = int((30 if f["big"] else 21) * (0.62 + 0.38 * fpp) * pop)
                else:
                    fx_, fy_ = f["x"] + sp["sx"], f["y"] + sp["sy"]
                    size = int((30 if f["big"] else 21) * pop)
                p.text(f["text"], size, inv_hex(f["color"], a), int(fx_), int(fy_),
                       bold=f["big"], anchor=(0.5, 0.5), w=260, h=70,
                       outline="#04030a")

        def _pause(self, g, p):
            p.fill("#04030ac8", 0, 0, 1280, 720)
            inv_draw_panel(p, 440, 270, 400, 150, BIOStage.STYLE_PANEL)
            p.text("PAUSED", 40, BIO_INK, 640, 322, bold=True,
                   anchor=(0.5, 0.5), w=600, h=70)
            p.text("ESC  RESUME        Q  QUIT", 16, BIO_DIM,
                   640, 378, anchor=(0.5, 0.5), w=800, h=44)
# --- THE SCREEN --------------------------------------------------------------
screen inv_biography_screen(game):
    modal True
    use enter_m_input_lock()

    add Solid("#04030a")
    add BIOStage(game)

    key "K_ESCAPE" action Function(game.toggle_pause)
    key "mouseup_3" action Function(game.toggle_pause)
    if game.paused:
        key "K_q" action Function(game.give_up)

    if config.developer:
        key "K_g" action Function(game.toggle_god)

    timer 0.25 repeat True action Function(inv_poll_result, game, _update_screens=False)


# --- WRAPPER -----------------------------------------------------------------
# No notices, no preamble, no debrief. An invasion begins on the frame it
# begins and ends on the frame it ends.
default bio_game = None
default bio_deaths = 0
default bio_retry = False
# A RETRY FROM THE TEAR. Set by the retry overlay when a loss happened after
# the checkpoint; the fight reads it once and starts in the corruptive state.
default bio_resume = None

label archivist_invasion_biography:
    $ bio_deaths = 0
    $ bio_retry = False
    $ bio_resume = None

label inv_biography_fight:
    $ renpy.block_rollback()

    $ bio_game = BIOGame(retry=bio_retry, deaths=bio_deaths,
                        debug=config.developer, start_open=inv_dev_start_open,
                        resume=bio_resume)
    $ bio_resume = None

    $ _bio_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ _bio_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None
    scene black

    call screen inv_biography_screen(bio_game)
    $ _bio_result = _return
    $ _bio_checkpoint = bio_game.checkpoint

    $ bio_game = None
    $ quick_menu = _bio_prev_quick_menu
    $ _game_menu_screen = _bio_prev_game_menu
    $ inv_music_stop(1.0)
    $ inv_stop_sfx(0.2)
    scene black

    if _bio_result == "victory":
        $ inv_record_result("biography", True)
        jump inv_biography_victory
    elif _bio_result == "quit":
        jump inv_biography_quit

    $ inv_record_result("biography", False)
    jump inv_biography_defeat

label inv_biography_victory:
    if inv_dev_test:
        $ renpy.notify("BIOGRAPHY fended off.")
        return
    # STORY PLACEMENT: DRAWING BOARD. An invasion is an interruption, so this
    # is where the interrupted day resumes -- with nothing said about it.
    return

label inv_biography_defeat:
    $ bio_deaths += 1
    $ bio_retry = True

    # The overlay is the fight's own -- its font, its colours, its words --
    # rather than the game's choice menu, which was a style break at the worst
    # possible moment. RETRY from the tear when the loss came after it.
    call screen inv_retry_screen("BIOGRAPHY", "FILED",
                                 inv_retry_options(_bio_checkpoint),
                                 ink=BIO_INK, dim=BIO_DIM, accent=BIO_RED,
                                 bg=BIO_BLACK)
    if _return == "tear":
        $ bio_resume = _bio_checkpoint
        scene black
        jump inv_biography_fight
    elif _return == "start":
        scene black
        jump inv_biography_fight
    if inv_dev_test:
        $ renpy.notify("BIOGRAPHY: lost. Recorded.")
    return

label inv_biography_quit:
    $ bio_retry = True
    if inv_dev_test:
        $ renpy.notify("BIOGRAPHY: withdrawn.")
    return
