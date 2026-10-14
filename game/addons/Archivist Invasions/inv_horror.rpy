# Horror invasion: a turn-based dread/nerve bout followed by a corridor chase.
# HORGame owns simulation state; HORStage advances/render it at 60Hz. The
# chase's opening gap derives from act-one dread, and distance determines a win.
# Act-one aspect readouts can lie; flicker identifies the unreliable reading.
#
# The runner stays on HOR_PLANE_Y: obstacles collide when their depth crosses
# that plane, using horizontal position. Light spends a finite power reserve and
# attracts the pursuer; directional light also drives back watchers on its side.
# Look-back, wind, dread and the shrinking corridor govern the chase. Cosmetic
# structure and outside silhouettes do not add collision surfaces.
# Shared encounter presentation constraints live in invasions.rpy. Keep hazard
# telegraphs and collision geometry aligned when changing the projected scene.

init -9 python:
    HOR_PALL_OK = False
    HOR_DARK_OK = False
    HOR_WITHER_OK = False

    def _hor_register_shaders():
        # THE CORRIDOR, BOTH ACTS (Oct 2 2026).
        #
        # Act one used to be a drained pall over the hyperspace plate with the
        # thing floating in the middle of it, and act two a black screen with
        # line-drawn hoops and hollow boxes -- "a heart running down an empty
        # corridor". It is now ONE PLACE: a real corridor, floor, walls,
        # ceiling and ribs, solved per pixel against the SAME projection the
        # simulation uses (hor_project: persp = Z_NEAR / z, screen offsets
        # scale by persp about the vanishing point), so every mass, watcher
        # and strut drawn from Python stands exactly on the surfaces painted
        # here.
        #
        # In act one the corridor is at rest and the thing is standing in it,
        # as far down it as DREAD says -- the number that matters, made into
        # a distance you can see. In act two the same corridor moves.
        #
        # THE LANTERN IS A LIGHT. It is a point source carried at hip height by
        # whoever is running, with distance falloff, Lambert shading against
        # each surface and a wet specular glint -- so raising it gives you the
        # corridor back the way a lamp does, nearest first. It is the only
        # warm thing in either act.
        #
        # The far end is the old "drowned spectacle": the plate mapped into a
        # throat at the vanishing point, kept as the fog colour, so the
        # corridor still runs into the hyperspace it is made of.
        renpy.register_shader("inv.dark", variables="""
            uniform sampler2D tex0;
            uniform sampler2D tex1;
            uniform vec2 u_hor_res;
            uniform float u_hor_time;
            uniform vec4 u_hor_geo;
            uniform vec4 u_hor_lane;
            uniform vec4 u_hor_lamp;
            uniform vec4 u_hor_mood;
            uniform vec4 u_hor_hole;
            uniform float u_hor_near;
            uniform float u_hor_beat;
            uniform float u_hor_lurch;
            uniform float u_hor_blind;
            uniform float u_hor_glitch;
            uniform float u_hor_flash;
            uniform float u_hor_dark;
            uniform float u_hor_look;
            uniform float u_hor_vast;
            uniform float u_hor_close;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float dk_hash(vec2 p) {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
            }
            float dk_noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                f = f * f * (3.0 - 2.0 * f);
                float a = dk_hash(i);
                float b = dk_hash(i + vec2(1.0, 0.0));
                float c = dk_hash(i + vec2(0.0, 1.0));
                float d = dk_hash(i + vec2(1.0, 1.0));
                return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
            }
            float dk_fbm(vec2 p) {
                float v = 0.0;
                float a = 0.5;
                for (int i = 0; i < 3; i++) {
                    v += a * dk_noise(p);
                    p = p * 2.11 + vec2(11.7, 5.3);
                    a *= 0.5;
                }
                return v;
            }
        """, fragment_300="""
            const float DK_TAU = 6.2831853;
            const float DK_F = 900.0;           // focal length, px
            vec2 res = max(u_hor_res, vec2(1.0));
            vec2 px = v_tex_coord * res;
            float t = u_hor_time;
            float near = clamp(u_hor_near, 0.0, 1.0);
            float beat = clamp(u_hor_beat, 0.0, 1.0);
            float blind = clamp(u_hor_blind, 0.0, 1.0);
            float glitch = clamp(u_hor_glitch, 0.0, 1.0);
            float look = clamp(u_hor_look, 0.0, 1.0);
            float vast = clamp(u_hor_vast, 0.0, 1.0);
            float act = clamp(u_hor_mood.x, 0.0, 1.0);
            float dread = clamp(u_hor_mood.y, 0.0, 1.0);
            float spd = clamp(u_hor_mood.z, 0.0, 1.0);
            float lamp = clamp(u_hor_lamp.x, 0.0, 1.0);
            vec2 vp = u_hor_geo.xy;

            // --- the frame, before the geometry ------------------------------
            vec2 q = px - vp;
            // The heartbeat squeezes the corridor toward its own end.
            q *= 1.0 - 0.045 * beat * (0.5 + near) * act;
            q.x += u_hor_lurch * 26.0 * sin(px.y * 0.036 + t * 9.0);
            float grow = floor(px.y / 6.5);
            q.x += (dk_hash(vec2(grow, floor(t * 20.0))) - 0.5) * 200.0 * glitch;

            // The wormhole it comes through, same instrument as every arrival.
            float hs = clamp(u_hor_hole.w, 0.0, 1.0);
            vec2 hv = (vp + q) - u_hor_hole.xy;
            float hd = length(hv);
            float hr = max(u_hor_hole.z, 1.0);
            if (hs > 0.001) {
                float hinf = (1.0 - smoothstep(0.0, hr, hd)) * hs;
                float ha = hinf * hinf * 4.6 + t * 0.4 * hinf;
                vec2 hw = vec2(hv.x * cos(ha) - hv.y * sin(ha),
                               hv.x * sin(ha) + hv.y * cos(ha));
                q = (u_hor_hole.xy + hw * (1.0 - 0.62 * hinf)) - vp;
            }

            // --- THE CORRIDOR ------------------------------------------------
            float lo = u_hor_lane.x;
            float hi = u_hor_lane.y;
            float zn = max(u_hor_lane.z, 0.01);
            // TURNING ROUND REVERSES THE WORLD: everything that was coming at
            // you goes away. The cheapest convincing "you are facing the other
            // way" there is, and it costs no second camera.
            float zs = u_hor_lane.w * (1.0 - 2.0 * look);
            float fy = u_hor_geo.z - vp.y;
            float cy = u_hor_geo.w - vp.y;
            // The walls are not flat: their inner face breathes, out of step
            // with everything else, harder the closer it is behind you.
            float wig = (u_hor_mood.w + 60.0 * near) * (0.6 + 0.4 * sin(t * 1.3));
            float wl = (lo - vp.x) + wig * 0.12;
            float wr = (hi - vp.x) - wig * 0.12;

            float pf = q.y > 0.0 ? q.y / fy : 0.0;
            float pc = q.y < 0.0 ? q.y / cy : 0.0;
            float pl = q.x < 0.0 ? q.x / min(wl, -1.0) : 0.0;
            float pr = q.x > 0.0 ? q.x / max(wr, 1.0) : 0.0;
            float persp = max(max(pf, pc), max(pl, pr));
            persp = max(persp, 1e-4);
            float z = zn / persp;
            float zw = z + zs;
            float onwall = step(max(pf, pc), max(pl, pr));
            float onceil = step(pf, pc) * (1.0 - onwall);
            float xw = q.x / persp;
            float yw = q.y / persp;

            // A second, finer wriggle on the wall face itself, so the edges of
            // the corridor are never a ruled line.
            float face = dk_fbm(vec2(zw * 9.0, yw * 0.012 + t * 0.15));
            if (onwall > 0.5) {
                float pw = (q.x < 0.0 ? -1.0 : 1.0);
                xw += pw * (face - 0.5) * (18.0 + 30.0 * near);
            }

            vec2 tuv = mix(vec2(xw / 280.0, zw * 4.2), vec2(zw * 4.2, yw / 280.0), onwall);
            vec3 tx = texture2D(tex1, tuv).rgb;

            // RIBS: hoops round the corridor on the struts' own period, so the
            // painted ones and the drawn ones can never disagree.
            float ribp = fract(zw * 7.52);
            float rib = smoothstep(0.80, 0.90, ribp) * (1.0 - smoothstep(0.93, 1.0, ribp));
            float gap = smoothstep(0.62, 0.80, ribp) * (1.0 - smoothstep(0.80, 0.86, ribp));

            vec3 alb = vec3(0.28, 0.31, 0.29) * (0.45 + 1.05 * tx.r);
            alb = mix(alb, alb * vec3(0.78, 0.86, 0.80), onceil);
            alb *= 1.0 - 0.55 * gap;
            alb += vec3(0.16, 0.17, 0.16) * rib;
            // Growths on the walls: dark lumps riding the same depth phase.
            float lump = smoothstep(0.62, 0.86, dk_fbm(vec2(zw * 3.0, yw * 0.006)))
                       * onwall;
            alb = mix(alb, vec3(0.05, 0.05, 0.05), lump * 0.8);

            // --- light ---------------------------------------------------------
            vec3 P = vec3(xw, yw, z * DK_F / zn);
            vec3 N = mix(mix(vec3(0.0, -1.0, 0.0), vec3(0.0, 1.0, 0.0), onceil),
                         vec3(q.x < 0.0 ? 1.0 : -1.0, 0.0, 0.0), onwall);
            vec3 L = vec3(u_hor_lamp.y - vp.x, fy - 70.0, DK_F * 1.05);
            vec3 dL = L - P;
            float dist = length(dL);
            vec3 ld = dL / max(dist, 1.0);
            float lam = max(dot(N, ld), 0.0);
            float atten = 1.0 / (1.0 + (dist * dist) / (520.0 * 520.0));
            vec3 V = normalize(-P);
            vec3 H = normalize(ld + V);
            float wet = 0.35 + 0.65 * tx.g;
            float spec = pow(max(dot(N, H), 0.0), 28.0) * wet;
            float flick = 0.86 + 0.14 * dk_noise(vec2(t * 8.0, 3.0));
            flick = mix(flick, 1.0, clamp(u_hor_lamp.z, 0.0, 1.0));
            float light = lamp * flick * atten;
            vec3 warm = vec3(1.00, 0.86, 0.62);
            vec3 col = alb * (0.075 + 0.045 * act)
                     + alb * warm * lam * light * 2.6
                     + warm * spec * light * 1.4;
            // Without the lamp the corridor is not black -- it is lit, very
            // faintly and coldly, from the far end, so the walls are a shape
            // and not a void. Lowest near you, rising down the throat.
            float farlit = smoothstep(0.20, 1.2, z) * (1.0 - smoothstep(1.4, 3.2, z));
            col += alb * vec3(0.20, 0.26, 0.24) * farlit;
            // THE SEAMS. Where floor meets wall and wall meets ceiling a thin
            // cold line of light runs away to the vanishing point: the cheapest
            // way to keep a dark corridor reading as a corridor.
            float a1 = max(pf, pc);
            float a2 = max(pl, pr);
            float seam = 1.0 - smoothstep(0.0, 0.035, abs(a1 - a2) / max(persp, 0.02));
            col += vec3(0.11, 0.14, 0.13) * seam * (0.5 + 0.5 * farlit)
                 * (1.0 - smoothstep(1.6, 3.0, z));

            // --- the far end: the drowned spectacle ------------------------------
            vec2 c = q / res.y;
            float r = max(length(c), 0.0007);
            float ang = atan(c.y, c.x);
            float tdepth = 0.34 / r + zs * 1.15;
            vec2 tuv2 = vec2(ang / DK_TAU * 2.0 + sin(tdepth * 0.25) * 0.05, tdepth * 0.16);
            vec3 src = texture2D(tex0, fract(tuv2)).rgb;
            vec3 fogc = src * vec3(0.10, 0.13, 0.12) + vec3(0.012, 0.016, 0.015);
            float fogk = mix(1.45, 2.10, dread * (1.0 - act)) + 0.6 * blind;
            float fog = 1.0 - exp(-(max(z - zn, 0.0)) * fogk);
            col = mix(col, fogc, fog);

            // SOMETHING ENORMOUS crossing the far end of the corridor. It
            // occludes the throat and carries one cold rim, and it never
            // touches anything.
            if (vast > 0.001) {
                float body = sin(ang * 0.85 + t * 0.055) * 0.5 + 0.5;
                float sil = smoothstep(0.40, 0.60, body) * smoothstep(0.55, 1.0, fog);
                col = mix(col, col * 0.05, sil * vast);
                float rim2 = (1.0 - smoothstep(0.0, 0.055, abs(body - 0.50)))
                           * smoothstep(0.55, 1.0, fog);
                col += vec3(0.055, 0.095, 0.125) * rim2 * vast;
            }

            // SPEED: filaments streaking down the walls at the rate you are
            // actually running. Without them the corridor reads as wallpaper.
            float fil = dk_hash(vec2(floor(ang * 18.0), 7.0));
            float streak = smoothstep(0.92, 1.0, fil)
                         * smoothstep(0.55, 1.0, fract(tdepth * 0.5))
                         * spd * act * (1.0 - fog);
            col += vec3(0.10, 0.12, 0.11) * streak;

            // The hole's own mouth.
            if (hs > 0.001) {
                float core = 1.0 - smoothstep(hr * 0.12, hr * 0.52, hd);
                col *= mix(1.0, 0.02, core * hs);
                float lip = 1.0 - smoothstep(0.0, hr * 0.16, abs(hd - hr * 0.52));
                col += vec3(0.42, 0.46, 0.40) * lip * hs * 1.15;
            }

            // --- PRESSURE ---------------------------------------------------------
            // The edges come in as it closes, breathing faster the nearer it
            // is. A blackout slams them shut, the walls close over the run,
            // a stare shuts everything that is not the thing you are staring
            // at -- and the lantern holds them back a little.
            vec2 cc = (px - vp) / res.y;
            float squeeze = 0.62 + 1.60 * near + 3.0 * blind + 1.15 * u_hor_close
                          + 2.0 * look - 0.45 * lamp + 1.20 * dread * (1.0 - act)
                          + 0.10 * sin(t * (1.6 + 3.4 * near)) * (0.3 + near);
            col *= max(1.0 - dot(cc, cc) * squeeze, 0.0);

            // It is behind you, so the bottom of the frame is the worst place
            // to look -- until you turn round.
            float behind = smoothstep(0.62, 1.0, v_tex_coord.y) * near * (1.0 - look) * act;
            col *= 1.0 - 0.50 * behind;
            col += vec3(0.075, 0.012, 0.020) * behind * (0.35 + 0.65 * beat);
            col += vec3(0.090, 0.014, 0.024) * look * near * (0.30 + 0.70 * beat);

            col = mix(col, vec3(0.80, 0.82, 0.80), clamp(u_hor_flash, 0.0, 1.0));
            col *= 1.0 - clamp(u_hor_dark, 0.0, 1.0);
            gl_FragColor = vec4(col, 1.0);
        """)
    def _hor_register_wither():
        # HORROR'S OWN BODY. Every Archivist gets its own way of being wrong,
        # or they all read as the same puppet in different hats.
        #
        # Biography is MISREGISTRATION: fourteen hard bands sliding out of
        # sync, chromatic fringing, high frequency -- something assembled
        # incorrectly, and visibly digital about it.
        #
        # Horror is the opposite in every axis. LOW frequency and liquid: it
        # undulates rather than stutters, there is no colour fringing at all,
        # and instead of coming apart in bands it SWELLS from the inside (the
        # cavity in this thing is full of small figures, and they move) and
        # FRAYS at the silhouette, bleeding smoke off its own outline so it
        # never quite ends where it should. Nothing here is sharp; the whole
        # point is that you cannot find its edge.
        renpy.register_shader("inv.wither", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_wit_res;
            uniform float u_wit_t;
            uniform float u_wit_warp;
            uniform float u_wit_swell;
            uniform vec2 u_wit_stretch;
            uniform float u_wit_pivot;
            uniform float u_wit_reach;
            uniform float u_wit_diss;
            uniform float u_wit_near;
            uniform vec4 u_wit_tint;
            uniform vec4 u_wit_rim;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float wit_hash(vec2 p) {
                return fract(sin(dot(p, vec2(21.71, 91.13))) * 24634.6345);
            }
            float wit_noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                f = f * f * (3.0 - 2.0 * f);
                float a = wit_hash(i);
                float b = wit_hash(i + vec2(1.0, 0.0));
                float c = wit_hash(i + vec2(0.0, 1.0));
                float d = wit_hash(i + vec2(1.0, 1.0));
                return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
            }
            float wit_fbm(vec2 p) {
                float v = 0.0;
                float a = 0.5;
                for (int i = 0; i < 4; i++) {
                    v += a * wit_noise(p);
                    p = p * 2.07 + vec2(7.3, 3.1);
                    a *= 0.5;
                }
                return v;
            }
            // A cheap 5-tap blur of the source alpha. Horror's whole thesis is
            // that you cannot find its edge, and an edge is a high-frequency
            // thing -- so the silhouette is read through this rather than
            // sampled directly.
            float wit_soft(sampler2D tx, vec2 uv, float r) {
                float a = texture2D(tx, uv).a * 0.36;
                a += texture2D(tx, uv + vec2(r, 0.0)).a * 0.16;
                a += texture2D(tx, uv - vec2(r, 0.0)).a * 0.16;
                a += texture2D(tx, uv + vec2(0.0, r)).a * 0.16;
                a += texture2D(tx, uv - vec2(0.0, r)).a * 0.16;
                return a;
            }
        """, fragment_300="""
            vec2 plate_uv = v_tex_coord;
            vec2 uv = v_tex_coord;
            vec2 piv = vec2(0.5, clamp(u_wit_pivot, 0.0, 1.0));
            vec2 st = max(u_wit_stretch, vec2(0.08));
            uv = (uv - piv) / st + piv;

            float t = u_wit_t;
            float w = clamp(u_wit_warp, 0.0, 4.0);
            float near = clamp(u_wit_near, 0.0, 1.0);
            float swell = clamp(u_wit_swell, 0.0, 2.0);

            // LOW frequency, long wavelength: it sways and seeps. Nothing in
            // here is allowed to be a band or a step.
            uv.x += sin(uv.y * 3.1 + t * 0.55) * 0.020 * w;
            uv.x += sin(uv.y * 1.3 - t * 0.31) * 0.014 * w;
            uv.y += sin(uv.x * 2.2 + t * 0.42) * 0.010 * w;

            // ---- THE CAVITY, AND IT IS NOT EMPTY --------------------------
            // The old shader said "something inside is moving" in a comment
            // and then only pushed the surface outward, which is a swell and
            // not an occupant. Now the interior is genuinely a SECOND LAYER:
            // the body is sampled again, deeper in and on its own slow drift,
            // and bled through wherever the shell is thick. So what you see
            // inside the cavity is more of the thing, moving at a different
            // rate from the thing containing it -- and none of it ever
            // resolves, because both layers are read through wit_soft.
            //
            // This is Horror's answer to Mystery's apertures and it is
            // deliberately the opposite one: Mystery shows you MORE COAT
            // through a hard-edged hole, this shows you SOMETHING ELSE through
            // skin. Neither of them lets you see the room behind.
            vec2 d = uv - vec2(0.5, 0.55);
            vec2 dn = normalize(d + vec2(1e-5));
            float n = wit_fbm(vec2(uv.x * 3.0, uv.y * 3.0 - t * 0.25));
            uv += dn * (n - 0.5) * 0.05 * swell;

            vec4 col = texture2D(tex0, uv);
            float shell = wit_soft(tex0, uv, 0.010);

            // The occupant: same body, pushed inward, turning on its own
            // clock, and pressing OUT in slow peristaltic waves.
            float press = wit_fbm(vec2(uv.x * 2.4 + t * 0.09,
                                    uv.y * 2.4 - t * 0.19));
            vec2 iuv = vec2(0.5, 0.55) + d * (0.80 + 0.16 * press)
                    + dn * sin(t * 0.37 + press * 6.0) * 0.012;
            vec4 inner = texture2D(tex0, iuv);
            // Only where the shell is thick, and strongest away from the
            // silhouette's edge -- an occupant is a thing you see through a
            // body, not around one.
            float depth = smoothstep(0.35, 0.95, shell);
            float bleed = depth * (0.30 + 0.34 * swell)
                        * smoothstep(0.25, 0.75, press);
            col.rgb = mix(col.rgb, inner.rgb * 1.18, bleed);
            // ...and it distends the shell as it goes past.
            col.a = max(col.a, shell * bleed * 0.35);

            // ---- SOFT FOCUS, because an edge is a thing you could point at -
            // The further from the core, the less resolved. Nothing about this
            // body is ever in focus at its own outline.
            float soften = 0.30 + 0.45 * (1.0 - depth);
            if (soften > 0.02) {
                float blur_r = 0.004 + 0.014 * (1.0 - depth) + 0.006 * near;
                vec4 soft = texture2D(tex0, uv + vec2(blur_r, blur_r * 0.6));
                soft += texture2D(tex0, uv - vec2(blur_r, blur_r * 0.6));
                soft += texture2D(tex0, uv + vec2(-blur_r * 0.7, blur_r));
                soft += texture2D(tex0, uv + vec2(blur_r * 0.7, -blur_r));
                col = mix(col, soft * 0.25, soften);
            }

            // ---- FRAY. Now a real advected smoke field rather than 4 taps --
            // The dilation finds the ground just outside the silhouette; the
            // smoke that grows there DRIFTS -- upward and away, on two
            // counter-running octaves -- so the outline is not merely soft,
            // it is actively leaving.
            float reach = clamp(u_wit_reach, 0.0, 2.0);
            if (reach > 0.001) {
                // SIX SINGLE TAPS, NOT SIX SOFTENED ONES. The dilation only
                // has to answer "is there body within reach of here", and a
                // 5-tap soften per probe made that question cost thirty
                // texture fetches per pixel -- on a plate this size that is
                // tens of millions a frame for an answer that is then
                // thresholded through smoothstep anyway. The softness the
                // silhouette needs comes from `shell` and from the smoke
                // field, both of which are already soft.
                float halo = 0.0;
                halo = max(halo, texture2D(tex0, uv + vec2(0.021, 0.0)).a);
                halo = max(halo, texture2D(tex0, uv - vec2(0.021, 0.0)).a);
                halo = max(halo, texture2D(tex0, uv + vec2(0.0, 0.026)).a);
                halo = max(halo, texture2D(tex0, uv - vec2(0.0, 0.026)).a);
                halo = max(halo, texture2D(tex0, uv + vec2(0.015, 0.018)).a);
                halo = max(halo, texture2D(tex0, uv - vec2(0.015, 0.018)).a);
                float rim = clamp(halo - col.a, 0.0, 1.0);
                float s1 = wit_fbm(vec2(uv.x * 6.0 + t * 0.11,
                                        uv.y * 6.0 - t * 0.62));
                float s2 = wit_fbm(vec2(uv.x * 13.0 - t * 0.29,
                                        uv.y * 13.0 - t * 1.05));
                float smoke = smoothstep(0.28, 0.86, s1 * 0.65 + s2 * 0.35);
                rim *= smoke * reach;
                col.rgb += vec3(0.085, 0.105, 0.092) * rim * (1.0 + 0.9 * near);
                col.a += rim * 0.70;
            }

            // ---- IT BREATHES, and the skin lags what is under it ----------
            // Two rates: the interior swells on one period and the surface
            // catches up on a slower one, which is what separates "a thing
            // breathing" from "a picture scaling".
            float breath = sin(t * 0.41) * 0.5 + sin(t * 0.23 + 1.1) * 0.5;
            col.a *= 1.0 + 0.05 * breath * depth;

            // It does not erode in cells like Biography -- it drains, from the
            // bottom up, and the draining edge smokes as it goes.
            float diss = clamp(u_wit_diss, 0.0, 1.0);
            if (diss > 0.0) {
                float m = wit_fbm(vec2(uv.x * 5.0, uv.y * 5.0 + t * 0.2));
                float lvl = m * 0.55 + uv.y * 0.65;
                float keep = smoothstep(diss - 0.18, diss + 0.18, lvl);
                // The waterline itself frays instead of being a level.
                float line = 1.0 - smoothstep(0.0, 0.16, abs(lvl - diss));
                col.rgb += vec3(0.10, 0.12, 0.11) * line * col.a * 0.9;
                col *= keep;
            }


            // ---- THE CORRIDOR'S LIGHT ON IT (Oct 2 2026) --------------------
            // A key tint (the lantern, warm, by how near and how lit) and a
            // rim along its LOWER edges -- the lamp is held low, by whoever is
            // running, so that is the side of it the light finds.
            col.rgb *= mix(vec3(1.0), u_wit_tint.rgb, clamp(u_wit_tint.a, 0.0, 1.0));
            if (u_wit_rim.a > 0.001) {
                float below = min(texture2D(tex0, uv + vec2(0.006, 0.010)).a,
                                  texture2D(tex0, uv + vec2(-0.006, 0.010)).a);
                float rimv = clamp(col.a - below, 0.0, 1.0);
                col.rgb += u_wit_rim.rgb * rimv * u_wit_rim.a * col.a;
            }

            // ---- THE PLATE CONTRACT (shared by every Archivist body) -------
            // 1. PREMULTIPLIED ALPHA: RGB brighter than its own alpha ADDS
            //    light, and at alpha zero draws the plate's own rectangle as a
            //    glowing box. Clamping RGB to alpha is the fix.
            // 2. THE EDGE: a mesh shader is clipped dead at its plate
            //    rectangle, so the alpha is feathered in the plate's OWN
            //    untransformed coordinate.
            vec2 pe = min(plate_uv, vec2(1.0) - plate_uv);
            col *= smoothstep(0.0, 0.050, min(pe.x, pe.y));
            gl_FragColor = vec4(min(col.rgb, vec3(col.a)), col.a);
        """)

    try:
        _hor_register_shaders()
        HOR_PALL_OK = True
        HOR_DARK_OK = True
    except Exception as _hor_sh_e:
        HOR_PALL_OK = False
        HOR_DARK_OK = False
        try:
            renpy.log("INV FX: horror shaders failed: %r" % _hor_sh_e)
        except Exception:
            pass

    try:
        _hor_register_wither()
        HOR_WITHER_OK = True
    except Exception as _hor_wt_e:
        HOR_WITHER_OK = False
        try:
            renpy.log("INV FX: wither shader failed: %r" % _hor_wt_e)
        except Exception:
            pass


# --- CONSTANTS AND TUNING ----------------------------------------------------
init python:
    HOR_SOUP_IMG = INV_DIR + "hyperspace.png"
    HOR_SPRITE = INV_DIR + "horror.png"
    HOR_SPRITE_W, HOR_SPRITE_H = 1254, 1254
    # The figure does not sit in the middle of its own canvas (bbox is
    # 153,6 - 900,1228), so centring the plate would hang it off to one side.
    # These put the FIGURE where the code asks for it.
    HOR_FIG_DX, HOR_FIG_DY = 100.5, 10.0

    # The plate is rasterised at this zoom at most; anything larger is applied
    # to the finished mesh instead. 1254 * 0.62 * 1.6 padding = ~1244px, well
    # inside the 4096 texture ceiling, where 2.7 * 1254 was not.
    HOR_PLATE_MAX_ZOOM = 0.62

    # --- act one -------------------------------------------------------------
    HOR_HP_MAX = 240
    HOR_NERVE_MAX = 40
    HOR_RESOLVE_MAX = 1000
    HOR_SHIFT_RESOLVE = 520
    HOR_SHIFT_TURN_CAP = 14

    # --- THE LANTERN ---------------------------------------------------------
    # You cannot hurt it with your hands. The lantern is the only thing it
    # flinches from, and light costs NERVE -- so the resource that keeps it at
    # arm's length is the same one that keeps you sane. The real number on
    # screen is not its health, it is DREAD: how close it is standing.
    HOR_LIGHT_NERVE = 9
    HOR_LIGHT_LO, HOR_LIGHT_HI = 58, 78
    HOR_LIGHT_DREAD = 22
    HOR_LISTEN_NERVE = 6
    HOR_STEADY_NERVE = 14
    HOR_GUARD_MULT = 0.45
    HOR_READ_MULT = 0.60

    HOR_DREAD_MAX = 100
    HOR_DREAD_START = 15
    HOR_DREAD_STEP_LO, HOR_DREAD_STEP_HI = 7, 11
    HOR_DREAD_RECOIL = 58          # where it falls back to after it lunges

    # --- act two: the chase --------------------------------------------------
    HOR_GOAL = 6000.0              # distance units; ~75-90s of clean running
    HOR_SCROLL_PX = 4.6            # screen pixels per distance unit per tick

    HOR_WALK = 1.00
    HOR_SPRINT = 1.80
    HOR_LOOK_SPEED = 0.75          # while looking back
    # MODELLED, not guessed. At 1.20 base with this ramp: walking the whole
    # way is caught at ~71% of the distance (the premise holds), sloppy
    # running is caught at ~76%, clean running escapes with the gap bottoming
    # out near 46, and a run that fumbled act one badly escapes with it at 16.
    # Raise the base and the "bad act one" case stops being survivable; lower
    # it and walking starts winning, which kills the whole encounter.
    #
    # BARELY TOUCHED IN THE Aug 14 2026 NERF, AND THAT IS THE FINDING. The
    # complaint was "nigh-impossible and slightly RNG-dependent", and the
    # obvious lever -- slow the thing down -- was measured and was wrong twice
    # over. A sloppy bot at these numbers dies at HP 0 with sixteen stumbles
    # and a gap that was never once in danger: THE CHASE IS NOT LOST BY BEING
    # CAUGHT, IT IS LOST BY BLEEDING OUT. And at 1.14 the clean bot's gap
    # simply pinned at the ceiling for the entire run, which is not an easier
    # chase, it is no chase at all. So the speeds came back up and the real
    # fix went where the deaths were: see HOR_STUMBLE_HP and HOR_HP_NEARMISS
    # for the bleeding, and HOR_SPAWN_CLEAR_FRAC / HOR_LANE_NEAR /
    # HOR_REACH_W / HOR_MIN_WARN for the dice.
    HOR_THEIR_SPEED = 1.18
    HOR_THEIR_RAMP = 0.000031       # per tick, so ~1.31 by the finish
    HOR_LUNGE_MULT = 1.45

    HOR_STAM_MAX = 100.0
    HOR_STAM_DRAIN = 0.26          # per sprinting tick  (~6.4s of sprint)
    HOR_STAM_RECOVER = 0.30        # per non-sprinting tick (~5.6s to refill)
    HOR_STAM_NEARMISS = 7.5        # the entire skill curve lives here
    HOR_STAM_MIN_SPRINT = 6.0      # cannot start a sprint below this

    # WINDED. Emptying the tank is not merely "stop sprinting" -- it locks the
    # sprint out entirely and drops you BELOW a walk while it lasts. This is
    # the sprint cooldown, and it is why the skill is releasing early rather
    # than holding the key down.
    HOR_WINDED_TICKS = 130
    HOR_WINDED_SPEED = 0.86
    HOR_STAM_RELEASE_HINT = 14.0   # where a careful runner lets go

    # THE THREE FEARS, TURNED BACK ON YOU. In act one you spend them; in act
    # two it spends them on you, one at a time and never overlapping.
    #   GHOST -> a phantom of it, ahead of you, which is impossible
    #   DARK  -> the light fails outright for a moment
    #   BUG   -> the encounter itself faults: torn rows, lying readouts
    HOR_FEAR_EVERY = 620           # ticks between one fear and the next
    HOR_FEAR_JITTER = 180
    HOR_BLIND_LEN = 74
    HOR_GLITCH_LEN = 96
    HOR_SCRAMBLE_ON_GLITCH = 30

    HOR_GAP_MAX = 100.0
    HOR_GAP_K = 0.055              # gap units per (speed difference) per tick
    # 3.5, down from 6.0, and this is the largest single piece of the Aug 14
    # nerf. The curve here was a CLIFF rather than a slope: measured, a clean
    # run absorbs six stumbles without the gap ever dipping below its opening
    # value, and a sloppy run of fourteen dies every time. At 6.0 a mistake
    # cost more than a tenth of the whole runway, so the difference between
    # "fine" and "dead" was about four touches. At 3.5 it takes a genuinely
    # bad run to lose, which is what "hard" was supposed to mean.
    HOR_GAP_STUMBLE = 3.5

    # THE CORRIDOR CLOSES. It used to be a fixed 920px slot for the whole
    # chase, and that is most of why the second half read as EMPTY rather than
    # claustrophobic: nothing about the space itself ever got worse. It now
    # narrows continuously from FAR to NEAR across the run -- slowly enough
    # that no single moment announces it, which is the point. You are supposed
    # to notice you are cornered, not watch it happen.
    HOR_LANE_FAR = (180.0, 1100.0)     # 920 wide at the mouth
    # 544 by the end, up from 496. The last quarter of the run was where the
    # corridor stopped being dodgeable and started being rolled for: at 496,
    # a maximum reacher plus one mass could leave a gap you had to already be
    # standing in. Still down 41% from the mouth, which is what the closing
    # was ever for.
    HOR_LANE_NEAR = (368.0, 912.0)

    # THE POT COMES TO THE BOIL IN FOUR STEPS. Continuous pressure alone reads
    # as a flat difficulty curve, so the ramp carries four discrete rungs, each
    # of which adds a KIND of thing rather than more of the same, and each of
    # which announces itself once and then never again:
    #   0  the corridor
    #   1  the walls start reaching in
    #   2  something enormous is out there, and the light gets meaner
    #   3  it is close enough to be a constant presence, and the HUD goes
    HOR_PHASE_AT = (0.0, 0.24, 0.50, 0.76)

    # THE RUNNER DOES NOT MOVE VERTICALLY, and that is a correctness rule
    # rather than a design preference. Collision fires on the single frame an
    # obstacle's DEPTH crosses your plane and tests x only -- so a runner
    # floating 60px above the row still gets hit by a mass drawn well below
    # them, which reads as colliding with an invisible surface above the box.
    # The row is one line, that line is HOR_PLANE_Y, and the vertical keys do
    # something else entirely now (see THE LANTERN).
    # STRAFE HAS TO BEAT THE CLOSING SPEED. Measured: clearing a typical mass
    # means moving ~250px sideways. At 4.6 px/tick that is 54 ticks, while a
    # sprint eats 450px of runway in the same time -- more than you can see,
    # so the corridor was literally undodgeable and every test run died. At
    # 9.2 the same move costs 28 ticks (~230px of closing), which fits inside
    # the visible runway with room to react. Re-check this if HOR_SPRINT,
    # HOR_SCROLL_PX or the corridor width ever change.
    HOR_STRAFE = 8.0

    # --- FAIRNESS (this is a contract, not decoration) -----------------------
    # The dark is allowed to be oppressive; it is NOT allowed to be the reason
    # you died. Three rules hold that line:
    #
    #   1. MINIMUM WARNING TIME, not distance. Sight is measured in pixels but
    #      what matters is TICKS, and a sprint covers pixels faster. So the
    #      light radius is floored at (current pixels per tick * MIN_WARN), and
    #      running faster opens your eyes rather than blinding you.
    #   2. THE EDGE IS ALWAYS VISIBLE. An obstacle's leading edge is drawn at
    #      a floor alpha the moment it enters the frame, whatever the light is
    #      doing. You can always make out the line; the dark only hides the
    #      mass behind it.
    #   3. A GAP ALWAYS EXISTS. Spawns are refused if they would close the
    #      corridor against an obstacle already in play at a similar height.
    HOR_MIN_WARN = 60              # ticks of warning the light must always give
    HOR_EDGE_FLOOR = 0.62          # alpha an obstacle's outline never drops below
    # Verified with a dodging bot: at 36->20 a clean runner still gets
    # through, a fumbled act one (opening gap 30) wins about two runs in
    # three, and the three fears push a human well below the bot.
    # --- PERSPECTIVE ---------------------------------------------------------
    # Obstacles have DEPTH, not just a y position. They are born tiny at the
    # tunnel's vanishing point and swell as they close, which is the entire
    # difference between "rushing down a throat at speed" and "dodging falling
    # boxes". Screen position and size are projected from z every frame; the
    # only thing the simulation stores is depth and a world x.
    HOR_VP = (640.0, 331.0)        # matches the vanishing point in inv.dark
    HOR_PLANE_Y = 587.0            # where z == NEAR lands: the runner's row
    # A CORRIDOR NEEDS A CEILING. Without one there is nothing to hang
    # architecture off and the tunnel is a floor with a gradient over it --
    # which is a good part of why this act read as empty. Everything in the
    # STRUCTURE block below is drawn between this and HOR_PLANE_Y.
    HOR_CEIL_Y = 92.0
    HOR_Z_NEAR = 0.18              # depth of the runner's own plane
    HOR_Z_FAR = 1.00               # where a mass is born
    HOR_Z_RATE = 0.0065            # depth per tick per unit of speed
    HOR_Z_GONE = 0.085             # past the runner: cull

    HOR_SPAWN_FAR = 32             # ticks between masses at the start
    HOR_SPAWN_NEAR = 18            # ...and by the finish
    # PX OF CORRIDOR THAT MUST STAY OPEN -- as a FRACTION of the corridor, not
    # an absolute. The lane shrinks by nearly half over the run, so a fixed
    # 190px clearance would quietly become 38% of the available width and
    # start refusing almost every spawn, which is exactly how a closing
    # corridor turns into an empty one.
    #
    # 0.245, up from 0.207, and THIS is the answer to "slightly RNG-dependent"
    # rather than any of the speed numbers. The guarantee here is the width of
    # the opening a volley of spawns is allowed to leave you; at 0.207 of a
    # 544px lane that is 113px against a hit radius of 13 and a strafe of 8
    # per tick, which is a gap you have to have guessed right about rather
    # than one you can move into. At 0.245 it is 133px and it is reachable
    # from the middle of the lane inside the warning time.
    HOR_SPAWN_CLEAR_FRAC = 0.245

    # WALL REACHERS (phase 1+). Masses anchored to the corridor wall that grow
    # inward, so the walls stop being scenery and start being the hazard. They
    # are ordinary obstacles with their x pinned to an edge -- collision,
    # projection and the clearance check all work on them unchanged.
    HOR_REACH_CHANCE_P1 = 0.30
    HOR_REACH_CHANCE_P3 = 0.50
    # Capped at 265, down from 320: a maximum reacher used to be 65% of the
    # end-of-run corridor on its own, and whether it was survivable came down
    # to which side it grew from.
    HOR_REACH_W = (140.0, 265.0)

    # SOMETHING ENORMOUS, OUT PAST THE WALLS (phase 2+). Rare, brief, and it
    # never touches you -- the entire job is scale. A chase you can win is
    # frightening; a chase you can win while something the size of the sky
    # goes past is a different feeling, and it costs nothing mechanically.
    # Measured at 1150 with a phase-2 start: exactly ONE pass in a whole run,
    # which is not a motif, it is an anomaly you assume you imagined. From
    # phase 1 at this cadence it is three or four -- often enough to become a
    # thing that keeps happening, which is the feeling being aimed at.
    HOR_VAST_EVERY = 620
    HOR_VAST_LEN = 150

    # --- STRUCTURE (no mechanics; the corridor is a place now) ---------------
    # "A heart running down an empty corridor" was a fair description, and the
    # missing ingredient was ARCHITECTURE: struts hooping the tunnel and rails
    # running away to the vanishing point turn a dark gradient into somewhere
    # you are travelling THROUGH. All of it is projected off the same depth as
    # everything else, so it agrees with the obstacles instead of parallaxing
    # against them. None of it can touch you.
    #
    # HOR_STRUCT_PHASE is scroll -> depth-phase, and it is derived rather than
    # picked: obstacles cross the corridor at HOR_Z_RATE per unit of speed
    # while scroll climbs at HOR_SCROLL_PX, so structure travels at the same
    # apparent rate at HOR_Z_RATE / ((HOR_Z_FAR - HOR_Z_GONE) * HOR_SCROLL_PX).
    HOR_STRUCT_PHASE = HOR_Z_RATE / ((HOR_Z_FAR - HOR_Z_GONE) * HOR_SCROLL_PX)
    HOR_WALL_EYES = 5              # and things in them that are not masses

    # =========================================================================
    # THE LANTERN, IN THE CHASE
    # =========================================================================
    # Act one's entire kit is the lantern, and the first build of act two threw
    # it away at the tear -- which wasted the best joint in the encounter and
    # left the chase with nothing in it but steering. It comes back on the
    # vertical keys, which the plane rule above just freed up.
    #
    # AND IT IS THE OPPOSITE BARGAIN TO THE ONE IT WAS. In act one light PUSHES
    # IT BACK: dread falls, and the cost is nerve. In act two light SHOWS IT
    # WHERE YOU ARE: it closes faster the whole time you are lit, and the cost
    # is a tank of POWER that does not refill, ever, for the length of the run.
    # The same object, inverted by the genre shift, which is what a corruptive
    # state is supposed to do to everything it touches.
    #
    # What it buys: you can see (sight roughly doubles, and the corridor is
    # otherwise being taken off you as it closes), and it is the ONLY answer to
    # the watchers below.
    HOR_POWER_MAX = 100.0
    HOR_POWER_DRAIN = 0.115        # per lit tick -- ~14.5s of light, a whole run
    HOR_LAMP_SIGHT = 1.90          # sight multiplier while it is up
    HOR_LAMP_SEEN = 0.40           # added to ITS speed the whole time you are lit
    HOR_LAMP_WARM = 9              # ticks to come up, and to die back down
    # With the tank empty the corridor gets darker -- but never past fairness
    # rule 1, which is a floor on WARNING TIME and is applied after this.
    HOR_LAMP_DEAD_SIGHT = 0.80

    # =========================================================================
    # THE WATCHERS  (the cheap tactic, imported on purpose)
    # =========================================================================
    # Horror is a genre that has never been above a cheap trick, and refusing
    # to use one is its own kind of dishonesty. So: a thing in the wall that
    # ADVANCES WHEN YOU ARE NOT SHINING A LIGHT ON IT.
    #
    # It is not on the corridor's conveyor. Everything else out there is being
    # carried past you at the speed you are running; a watcher moves under its
    # own power, in HARD DISCRETE STEPS, and between them it does not move at
    # all. That stillness is the whole effect (and it is rule 3: it moves like
    # something that has seen a diagram of moving). Four steps and it is level
    # with you, at which point it comes off the wall.
    #
    # THE ANSWER IS DIRECTIONAL, which is what makes it a decision rather than
    # a chore: the lantern only drives back a watcher on the side of the
    # corridor YOU ARE STANDING ON. So answering it means crossing the lane
    # toward the thing coming for you and staying there -- against a corridor
    # that is spawning masses and growing reachers out of that same wall.
    #
    # ONE AT A TIME, EVER. Two on opposite walls is unanswerable and rule 5 is
    # not negotiable. They arrive more often as the run goes on instead.
    HOR_WATCH_FROM_PHASE = 1
    HOR_WATCH_EVERY_P1 = 560       # ticks between watchers, early
    HOR_WATCH_EVERY_P3 = 340       # ...and late
    HOR_WATCH_STAGES = 4           # 0,1,2,3 on the wall; 4 is on you
    HOR_WATCH_STEP = 132           # ticks per step while unlit
    HOR_WATCH_RECOVER = 60         # ticks per step back while lit, from your side
    # Where each stage stands, in depth. The last is nearer than your own plane
    # -- it has come past you before it turns.
    HOR_WATCH_Z = (0.86, 0.54, 0.32, 0.21)
    # WHAT A BITE TAKES. Measured against a bot that answers every watcher and
    # one that answers none: at a cost of 12 gap the ignoring bot was still
    # winning three runs in four and finishing on comparable health, i.e. the
    # answer cost more than the hazard did -- the exact failure the LOOK BACK
    # numbers were retuned for once already, and it is worse than not having
    # the mechanic, because the game is then inviting you to skip it. At 18
    # (plus its own health figure, above STUMBLE's) three bites is a run.
    HOR_BITE_GAP = 15.0
    HOR_BITE_HP = 24
    HOR_BITE_STAM = 36.0
    HOR_BITE_FREEZE = 26           # the stare, held, before the run resumes

    HOR_STUMBLE_TICKS = 18
    # 12, down from 18. Measured: the way a chase is actually lost is sixteen
    # stumbles at 240 health, not the gap -- a sloppy bot died at HP 0 six
    # runs out of six with the gap never once below its opening value. The
    # bleed WAS the difficulty and nothing on screen said so.
    HOR_STUMBLE_HP = 12
    # AND THERE IS A VALVE NOW, on exactly the skill the chase already asks
    # for. Threading an obstacle refunded wind and nothing else; it mends a
    # little as well, so a runner who weaves is buying their way back into the
    # run and one who plays it safe down the middle of the corridor is not.
    # Self-balancing by construction: a sloppy runner hits the things a clean
    # runner grazes, so they get fewer of these AND more of the stumbles, and
    # the two lines separate without either number being large.
    HOR_HP_NEARMISS = 4
    HOR_NEARMISS_R = 46.0
    HOR_HIT_R = 13.0

    HOR_LUNGE_EVERY = 900
    HOR_LUNGE_WARN = 70
    HOR_LUNGE_LEN = 100

    HOR_SCRAMBLE_TICKS = 72        # controls invert after touching a phantom

    # =========================================================================
    # LOOK BACK
    # =========================================================================
    # It used to print a number. Holding Z slowed you down and a figure
    # appeared saying how far away it was, which is a READOUT of the most
    # frightening thing in the encounter rather than the thing itself.
    #
    # NOW IT TURNS YOU ROUND. The camera swings, the tunnel reverses, the
    # forward view goes, and you are looking straight down the corridor at it
    # with nothing between you. The number is still there, but it is no longer
    # what you came for.
    #
    # AND IT IS A BARGAIN, WHICH IS THE WHOLE IDEA: exposing yourself to
    # something you have been refusing to look at costs you badly while you do
    # it -- speed, wind, and every scrap of warning about what is ahead -- and
    # leaves you STRONGER if you survive it. Release before it overwhelms you
    # and you keep RESOLVE: you run faster, tire slower and see further,
    # scaled by how long you held and how close it was when you did. Hold too
    # long and it takes you: a stumble, the distance gone, and the lockout
    # means you cannot go back for another look to fix it.
    #
    # The risk is real and it is not the lockout: LOOKING BACK BLINDS YOU
    # FORWARD. Obstacle outlines stay at a floor alpha (fairness rule 2 does
    # not get suspended because the player chose this) but everything else
    # about the runway is gone, and the corridor does not stop coming.
    HOR_LOOK_TURN = 15             # ticks for the camera to come round
    HOR_LOOK_MAX = 165             # hold past this and it has you
    HOR_LOOK_MIN = 22              # a glance below this pays nothing
    HOR_LOOK_DRAIN = 0.42          # wind per looking tick
    HOR_LOOK_SLOW = 0.28           # extra speed lost at a full stare

    # THE PAYOFF HAS TO BEAT THE PRICE, and at the first set of numbers it did
    # not: measured, a bot that stared well won 4 runs in 6 and a bot that
    # never looked back at all won 5. A full stare bleeds ~5 gap while you
    # hold it, so RESOLVE has to be worth clearly more than that or the whole
    # mechanic is a dare with no prize -- which is worse than not having it,
    # because the game is then inviting you to lose.
    HOR_RESOLVE_MAX = 620.0        # ticks of it you can be holding
    HOR_RESOLVE_SPRINT = 1.28      # sprint multiplier while it lasts
    HOR_RESOLVE_DRAIN = 0.46       # stamina drain multiplier
    HOR_LOOK_GAP_BACK = 10.0       # ground handed straight back on release
    HOR_RESOLVE_SIGHT = 1.38       # sight multiplier
    HOR_LOOK_LOCK = 150            # ticks you cannot look after being taken
    HOR_LOOK_STAM_BACK = 34.0      # wind handed back on a good release

    HOR_HEART_ZOOM = 2.6
    # Toned down to match Biography's: at 2.8 the avatar was the busiest thing
    # on a screen that is already deliberately hard to read, and losing track
    # of your own position is not the kind of difficulty this mode wants.
    HOR_HEART_WARP = 1.25

    # --- palette: almost nothing has colour ----------------------------------
    HOR_INK = "#e8ece8"
    HOR_DIM = "#7e8a84"
    HOR_FAINT = "#4e5a55"
    HOR_PALE = "#b8c4ba"
    HOR_WARN = "#c9b46a"
    HOR_BLOOD = "#8e1622"
    HOR_BLACK = "#020303"

    HOR_CMDS = (("light", "LIGHT"), ("listen", "LISTEN"),
                ("steady", "STEADY"), ("run", "RUN"))

    # --- ACT ONE STANDS IN THE CORRIDOR (Oct 2 2026) -------------------------
    # DREAD is how close it is standing, so in act one it is drawn as exactly
    # that: a figure on the corridor floor, further down the throat at low
    # dread and nearly on you at high dread. hor_a1_place(dread 0..1) gives
    # its perspective and where its feet meet the boards.
    HOR_A1_PERSP = (0.34, 0.60)
    HOR_A1_ZOOM = 0.30             # its zoom at persp 0.5
    HOR_FIG_H = 1222.0             # canvas px from the top of it to its feet
    HOR_A1_LANE = (150.0, 1130.0)  # act one's corridor: wide, nothing closing

    def hor_a1_place(dread):
        persp = inv_lerp(HOR_A1_PERSP[0], HOR_A1_PERSP[1], inv_clamp(dread, 0.0, 1.0))
        return (persp, HOR_VP[1] + (HOR_PLANE_Y - HOR_VP[1]) * persp)

    def hor_project(z):
        """Depth -> (scale, screen y). scale 1.0 is the runner's own plane."""
        z = max(z, 0.0001)
        persp = HOR_Z_NEAR / z
        return (persp, HOR_VP[1] + (HOR_PLANE_Y - HOR_VP[1]) * persp)

    def hor_screen_x(world_x, persp):
        return HOR_VP[0] + (world_x - HOR_VP[0]) * persp

    def hor_screen_y(world_y, persp):
        """The same projection for any world height, not just the plane. The
        corridor needs a ceiling before it can have architecture."""
        return HOR_VP[1] + (world_y - HOR_VP[1]) * persp


# --- SIMULATION --------------------------------------------------------------
init python:
    class HORGame(object):
        """All of Horror's live state, stepped at a fixed 60Hz by HORStage."""

        def __init__(self, retry=False, deaths=0, debug=False, start_open=False,
                     resume=None):
            self.result = None
            self.paused = False
            self.debug = bool(debug)
            self.retry = bool(retry)
            self.deaths = int(deaths)
            self.god = inv_godmode_on()
            # THE CHECKPOINT carries the one thing act one hands the chase:
            # how close it was standing when the room turned.
            self.checkpoint = None

            self.tick = 0
            self.clock = 0.0
            self.spin = 0.0
            self.rng = inv_random.Random()
            self.rng_fx = inv_random.Random()

            # --- presentation (Oct 2 2026; decoration owned by the sim) ------
            self.fx = InvFX(cap=420)
            self.turn_log = []
            self.shock = [640.0, 360.0, 0.0, 0.0]
            self.ca = 0.0
            self.tear = 0.0
            self.panel_kick = 0.0
            self.windup = 0.0
            self.windup_col = HOR_BLOOD
            self.pending_move = None
            self.lamp1 = 0.62           # act one: the lantern you are holding
            self.lamp1_still = 0.0      # STEADY: the flame stops guttering
            self.dread_shown = float(HOR_DREAD_START)
            self.blink_t = 0            # "behind": it is not there for a beat
            self.lunge_k = 0.0          # act one: IT REACHES

            # --- the runner ----------------------------------------------------
            self.hp = HOR_HP_MAX
            self.hp_shown = float(HOR_HP_MAX)
            self.nerve = HOR_NERVE_MAX
            self.nerve_shown = float(HOR_NERVE_MAX)
            self.roll_cue = 0

            # --- it ------------------------------------------------------------
            self.resolve = HOR_RESOLVE_MAX
            self.dread = float(HOR_DREAD_START)

            # --- act one -------------------------------------------------------
            self.mode = "arrive"
            self.mtick = 0
            self.turn = 0
            self.cursor = 0
            self.guard = False
            self.read = False
            self.held = False               # `still` doubles the next one
            self.panic = False
            self.last_cmd = None
            self.last_enemy = None

            self.beat_label = ""
            self.beat_value = ""
            self.beat_after = "menu"

            # --- presentation ----------------------------------------------------
            self.flash = 0.0
            self.dark = 1.0
            self.shake = 0.0
            self.freeze = 0
            self.corrupt = 0.0
            # 1.0, not 0.0: the panels start OFF the bottom of the screen
            # and slide up once the bout actually begins (see _step_ambient).
            # They used to exist from frame one and simply go undrawn during
            # the arrival, which meant they appeared whole on a single frame,
            # at the same instant the body took its place -- one pop reading as
            # two things going wrong at once.
            self.panel_slide = 1.0
            self.hit_flash = 0.0
            self.floats = []
            self.hole = [640.0, 330.0, 250.0, 0.0]
            self.emerge = 1.0
            self.body_scale = 1.0
            self.body_sx = 1.0
            self.body_sy = 1.0
            self.beat = 0.0
            self.beat_pulse = 0.0

            # --- the chase -------------------------------------------------------
            self.gap = HOR_GAP_MAX
            self.dist = 0.0
            self.stam = HOR_STAM_MAX
            self.scroll = 0.0
            self.speed = HOR_WALK
            self.their_speed = HOR_THEIR_SPEED
            self.sprinting = False
            self.looking = False
            self.stumble = 0
            self.scramble = 0
            self.lurch = 0.0
            self.look_t = 0             # ticks held this stare
            self.look_view = 0.0        # 0 facing forward, 1 fully turned
            self.look_lock = 0
            self.resolve_t = 0.0        # what a survived stare leaves you
            self.phase = 0
            self.vast_t = 0
            self.vast = 0.0
            self.obstacles = []
            self.phantom = None
            self.spawn_t = 0
            self.lunge_t = 0
            self.lunge_state = "idle"       # idle / warn / live
            self.near_cd = 0
            self.caught = False
            self.winded = 0
            self.fear_t = 0
            self.fear_kind = None           # ghost / dark / bug, one at a time
            self.blind = 0.0                # how shut the light is right now
            self.blind_t = 0
            self.glitch = 0.0
            self.glitch_t = 0

            # --- the lantern, and what it is for ------------------------------
            self.power = HOR_POWER_MAX
            self.lamp = False           # is the key down
            self.lamp_lit = 0.0         # 0 dark, 1 full -- eased, never a cut
            self.lamp_dead = False
            self.watcher = None
            self.watch_t = 0
            self.bite_t = 0             # the stare after one reaches you
            # Has the player ever successfully driven one back this run. The
            # on-floor prompt removes itself the moment they have, because a
            # tutorial that is still up after it worked is a nag.
            self.watch_taught = False

            # --- the exit ---------------------------------------------------
            # Its position on screen is SMOOTHED STATE, never derived fresh
            # from `near` each frame -- deriving it meant a lunge starting or
            # ending teleported it, which read as the sprite bugging out.
            self.follow_x = 640.0
            self.follow_y = 1080.0
            self.follow_zoom = 0.22
            self.follow_alpha = 0.45

            self.exit_rush = 1.0        # how hard the tunnel is moving
            self.exit_zoom = 0.0        # its size once it stops pretending
            self.exit_y = 0.0
            self.exit_warp = 0.0
            self.heart_x = 0.0
            self.heart_y = 0.0
            self.heart_scale = 1.0
            self.heart_diss = 0.0
            self.hud_fade = 1.0

            self.px = (HOR_LANE_FAR[0] + HOR_LANE_FAR[1]) * 0.5
            self.py = HOR_PLANE_Y
            self.trail = []

            self.keys = MSBFKeyLatch()
            self._prev = {"left": False, "right": False, "up": False,
                        "down": False, "z": False, "x": False}

            if resume:
                self.dread = float(resume.get("dread", 55.0))
                self.dread_shown = self.dread
                self._begin_run(dev=True)
                self.dark = 1.0
            elif start_open:
                self.dread = 55.0
                self.dread_shown = self.dread
                self._begin_run(dev=True)

        # ----- helpers ---------------------------------------------------------

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

        def dread_frac(self):
            return inv_clamp(self.dread / HOR_DREAD_MAX, 0.0, 1.0)

        def near_frac(self):
            """0 = it is nowhere near, 1 = it is on you. The chase's one input
            to almost every visual."""
            return inv_clamp(1.0 - (self.gap / HOR_GAP_MAX), 0.0, 1.0)

        def run_frac(self):
            """How far down the corridor you are, 0 to 1."""
            return inv_clamp(self.dist / HOR_GOAL, 0.0, 1.0)

        def lane(self):
            """The corridor, RIGHT NOW. It is narrower than it was."""
            u = inv_smooth(self.run_frac())
            return (inv_lerp(HOR_LANE_FAR[0], HOR_LANE_NEAR[0], u),
                    inv_lerp(HOR_LANE_FAR[1], HOR_LANE_NEAR[1], u))

        def resolved(self):
            """0..1 of the buff a survived stare left behind."""
            return inv_clamp(self.resolve_t / HOR_RESOLVE_MAX, 0.0, 1.0)

        def look_frac(self):
            """How deep into a stare you are. 1 means it is about to have
            you."""
            return inv_clamp(self.look_t / float(HOR_LOOK_MAX), 0.0, 1.0)

        def power_frac(self):
            return inv_clamp(self.power / HOR_POWER_MAX, 0.0, 1.0)

        def lit(self):
            """Is the lantern actually up. Held-key state is `lamp`; this is
            the thing the world reacts to, and it eases, so nothing in the
            chase ever cuts to a new lighting state."""
            return self.lamp_lit > 0.5

        def watch_side_ok(self):
            """THE DIRECTIONAL RULE. A lantern held up in the middle of the
            corridor drives back nothing -- you have to be on the side the
            watcher is on, which means crossing toward it."""
            w = self.watcher
            if w is None:
                return False
            lo, hi = self.lane()
            mid = (lo + hi) * 0.5
            return (self.px < mid) if w["side"] == 0 else (self.px > mid)

        def _beat(self, label, value="", after="enemy", kind="you"):
            self.beat_label = label
            self.beat_value = value
            self.beat_after = after
            self.mode = "beat"
            self.mtick = 0
            if value or label:
                inv_log_push(self, label, value, kind)

        def _kick_lens(self, x, y, strength, ca=0.0):
            self.shock = [float(x), float(y), 8.0, float(strength)]
            self.ca = max(self.ca, ca)

        def _fx_strike(self, big=False):
            """Act one: something reaching out of the corridor at the window
            that is standing in for you."""
            fx = self.fx
            x1, y1 = 1004.0, 612.0
            fx.burst("smoke_%d" % self.rng_fx.randint(0, 3), x1, y1, 7 if big else 4,
                     speed=(0.6, 2.4), life=(26, 44), size=(0.6, 1.2), size1=1.7,
                     col="#1a0a0c", alpha=0.75, add=False, drag=0.95,
                     jitter=120.0, squash=0.35, layer="hud")
            fx.burst("spark", x1, y1, 12 if big else 6, speed=(2.0, 7.0),
                     life=(10, 20), size=(0.2, 0.4), col="#c94a5a", drag=0.86,
                     stretch=0.12, layer="hud")
            self.panel_kick = 1.0
            self._kick_lens(x1, y1, 0.8 if big else 0.4, 0.008 if big else 0.004)

        def float_text(self, x, y, text, color, big=False):
            self.floats.append({"x": x, "y": y, "vy": -1.6, "life": 52,
                                "text": text, "color": color, "big": big})

        def hurt(self, amount, x=None, y=None):
            amount = int(max(0, amount))
            if amount <= 0:
                return
            if not self.god:
                self.hp = int(max(0, self.hp - amount))
            self.shake = min(1.0, self.shake + 0.6)
            self.hit_flash = 1.0
            self.play("hurt")
            if x is not None:
                self.float_text(x, y, "-%d" % amount,
                                HOR_DIM if self.god else HOR_BLOOD, True)

        def spend_nerve(self, amount):
            self.nerve = int(max(0, self.nerve - amount))
            if self.nerve <= 0:
                self.panic = True

        def gain_nerve(self, amount):
            self.nerve = int(min(HOR_NERVE_MAX, self.nerve + amount))
            if self.nerve > 0:
                self.panic = False

        # ----- input ------------------------------------------------------------

        def _poll_input(self):
            pg = inv_pg
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

        # ----- dispatcher --------------------------------------------------------

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

            mode = self.mode
            if mode == "arrive":
                self._step_arrive()
            elif mode == "menu":
                self._step_menu(edges)
            elif mode == "beat":
                self._step_beat(edges)
            elif mode == "enemy":
                self._step_enemy()
            elif mode == "shift":
                self._step_shift()
            elif mode == "run":
                self._step_run(edges)
            elif mode in ("leave_w", "leave_l"):
                self._step_leave()

        def _step_ambient(self):
            self.tick += 1
            self.clock += INV_TICK
            self.spin += INV_TICK * (0.06 + 0.10 * self.dread_frac()
                                    + 0.85 * self.hole[3])

            # The pulse stops for good once it has you. Nothing beating is
            # the loudest thing in the encounter.
            if self.mode == "leave_l" and self.mtick > 140:
                self.beat_pulse *= 0.90
            else:
                self.beat += 1.0 / INV_BEAT_TICKS
                if self.beat >= 1.0:
                    self.beat -= 1.0
                    self.beat_pulse = 1.0
                self.beat_pulse *= 0.88

            self.flash *= 0.86
            self.shake *= 0.88

            # THE PANELS SEAT THEMSELVES once the bout begins. Guarded to the
            # act-one modes on purpose: the shift drives this same value the
            # other way (0 -> 1) to throw the panels off the screen, and a
            # decay running underneath that would fight it.
            if self.mode in ("menu", "beat", "enemy") and self.panel_slide > 0.0:
                self.panel_slide = max(0.0, self.panel_slide - 0.042)

            self.hit_flash *= 0.88
            self.lurch *= 0.90

            # --- presentation state ------------------------------------------
            self.fx.step()
            self.ca *= 0.86
            self.tear *= 0.88
            self.panel_kick *= 0.84
            self.windup *= 0.94
            self.lunge_k *= 0.92
            if self.shock[3] > 0.004:
                self.shock[2] += 15.0 + self.shock[2] * 0.05
                self.shock[3] *= 0.90
            else:
                self.shock[3] = 0.0
            if self.blink_t > 0:
                self.blink_t -= 1
            # The lantern in your hand: it gutters back to its resting level
            # after a flare, and STEADY stops it guttering for a while.
            self.lamp1 = inv_lerp(self.lamp1, 0.62 if not self.panic else 0.40, 0.03)
            self.lamp1_still = max(0.0, self.lamp1_still - 0.006)
            # DREAD IS A DISTANCE now, so it must never jump: the thing is
            # drawn from a smoothed copy and walks to the new value.
            self.dread_shown = inv_lerp(self.dread_shown, self.dread, 0.045)
            if self.dark > 0.0 and self.mode == "run" and self.mtick < 70:
                self.dark = max(0.0, self.dark - 0.03)

            for attr, real in (("hp_shown", self.hp),
                            ("nerve_shown", self.nerve)):
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
                f["y"] += f["vy"]
                f["vy"] += 0.055
                f["life"] -= 1
            self.floats = [f for f in self.floats if f["life"] > 0]

            if self.hp_shown <= 0.0 and self.mode not in ("leave_w", "leave_l",
                                                        "arrive"):
                self._begin_leave(False)

        # =====================================================================
        # ARRIVAL
        # =====================================================================

        def _step_arrive(self):
            self.mtick += 1
            t = self.mtick
            self.dark = inv_clamp(1.0 - t / 30.0, 0.0, 1.0)

            if t == 6:
                self.play("tear", 0.75)
            if t < 70:
                self.hole[3] = inv_smooth(t / 70.0)
                self.hole[2] = inv_lerp(40.0, 250.0, inv_smooth(t / 70.0))
            elif t < 190:
                # It does not burst out. It comes through at its own pace,
                # which is worse.
                u = (t - 70) / 120.0
                self.hole[3] = 1.0
                self.emerge = 1.0 - inv_smooth(u)
                self.body_scale = inv_lerp(1.45, 1.0, inv_smooth(u))
                if t == 74:
                    self.play("wind", 0.8)
            elif t < 250:
                u = (t - 190) / 60.0
                self.emerge = 0.0
                self.body_scale = 1.0
                self.hole[3] = 1.0 - inv_smooth(u)
                self.hole[2] = inv_lerp(250.0, 30.0, inv_smooth(u))
            elif t == 250:
                self.hole[3] = 0.0
                inv_music_survey()
                inv_heart_start(0.25)
            elif t >= 290:
                self._begin_player_turn()

        # =====================================================================
        # ACT ONE
        # =====================================================================

        def _begin_player_turn(self):
            self.mode = "menu"
            self.mtick = 0
            self.turn += 1
            self.guard = False
            if self.panic:
                # Nerve is gone: your hands are not yours this turn.
                self.cursor = self.rng.randrange(len(HOR_CMDS))
            # Otherwise the cursor stays where you left it.

        def _step_menu(self, edges):
            self.mtick += 1
            n = len(HOR_CMDS)

            if self.panic:
                # PANIC. The cursor wanders on its own and confirms itself.
                if self.mtick % 9 == 0:
                    self.cursor = (self.cursor + 1) % n
                if self.mtick >= 70:
                    self.play("cancel")
                    self._resolve_player(HOR_CMDS[self.cursor][0], forced=True)
                return

            if edges["up"]:
                self.cursor = (self.cursor - 1) % n
                self.play("cursor")
            elif edges["down"]:
                self.cursor = (self.cursor + 1) % n
                self.play("cursor")
            if edges["z"]:
                self.play("confirm")
                self._resolve_player(HOR_CMDS[self.cursor][0])

        def _step_beat(self, edges):
            # Holds, then moves on; the readout outlives it in the turn log.
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
                    self.mode = "shift"
                    self.mtick = 0
                else:
                    self._begin_player_turn()

        def _resolve_player(self, cmd, forced=False):
            self.last_cmd = cmd
            label = cmd.upper()
            if forced:
                label = "PANIC  " + label
            value = ""

            if cmd == "light":
                if self.nerve < HOR_LIGHT_NERVE:
                    self.play("cancel")
                    self._beat("LIGHT", "NO NERVE", "menu")
                    return
                self.spend_nerve(HOR_LIGHT_NERVE)
                dmg = self.rng.randint(HOR_LIGHT_LO, HOR_LIGHT_HI)
                self.resolve = int(max(0, self.resolve - dmg))
                self.dread = max(0.0, self.dread - HOR_LIGHT_DREAD)
                self.play("scan")
                self.flash = 0.18
                # The lantern flares: the corridor comes back to its far
                # walls, and the thing in it gives ground.
                self.lamp1 = 1.75
                self.fx.burst("dust", 640.0, 560.0, 34, speed=(0.8, 3.6),
                              life=(30, 70), size=(0.5, 1.3), col="#ffd9a0",
                              drag=0.975, ay=-0.02, angle=-90.0, spread=150.0,
                              jitter=200.0, squash=0.5, layer="front")
                hx, hy = self._a1_head()
                self.fx.emit("glow", hx, hy, life=24, size=2.6, size1=3.6,
                             col="#ffe2b0", alpha=0.5, layer="front", fade="out2")
                self._kick_lens(hx, hy, 0.5, 0.004)
                value = "-" + str(dmg)

            elif cmd == "listen":
                self.gain_nerve(HOR_LISTEN_NERVE)
                self.read = True
                self.play("tick", 0.8)
                # Holding still and listening: the light drops and the room
                # comes in as a ripple from where it is standing.
                self.lamp1 = min(self.lamp1, 0.38)
                hx, hy = self._a1_head()
                self.fx.ring(hx, hy + 120, 30.0, 420.0, life=40, col="#b8c4ba",
                             alpha=0.35, layer="front", tex="ring_soft",
                             squash=0.45)
                value = "+" + str(HOR_LISTEN_NERVE)

            elif cmd == "steady":
                self.gain_nerve(HOR_STEADY_NERVE)
                self.guard = True
                self.play("guard")
                self.lamp1_still = 1.0
                self.fx.burst("dust", 1004.0, 620.0, 16, speed=(0.4, 1.6),
                              life=(30, 60), size=(0.5, 1.1), col="#e8d6a8",
                              drag=0.97, ay=-0.04, angle=-90.0, spread=60.0,
                              jitter=130.0, squash=0.35, layer="hud")
                value = "+" + str(HOR_STEADY_NERVE)

            elif cmd == "run":
                # It never works in here. In the next half it is the only
                # thing that does.
                self.play("miss")
                self.lurch = max(self.lurch, 0.7)
                self.tear = max(self.tear, 0.4)
                value = "FAILED"

            after = "enemy"
            if self.resolve <= HOR_SHIFT_RESOLVE:
                after = "shift"
            self._beat(label, value, after)

        def _pick_enemy_move(self):
            pool = ["loom", "loom", "whisper", "behind"]
            if self.turn >= 2:
                pool.append("still")
            if self.last_cmd:
                pool.append("mimic")
            if self.last_enemy in pool and len(set(pool)) > 1:
                pool = [m for m in pool if m != self.last_enemy] or pool
            return self.rng.choice(pool)

        def _step_enemy(self):
            self.mtick += 1
            if self.mtick < 26:
                # Its turn: the flame gutters while it decides.
                self.windup = min(1.0, self.windup + 0.06)
                return

            # It is always closer than it was.
            self.dread = min(float(HOR_DREAD_MAX),
                            self.dread + self.rng.randint(HOR_DREAD_STEP_LO,
                                                        HOR_DREAD_STEP_HI))

            # At arm's length it takes its one big swing and steps back.
            if self.dread >= HOR_DREAD_MAX:
                self.dread = HOR_DREAD_RECOIL
                self.play("enemy", 1.0)
                self.shake = 1.0
                self.flash = 0.4
                dmg = 48
                if self.guard:
                    dmg = int(dmg * HOR_GUARD_MULT)
                self.hurt(dmg, 1004, 586)
                # IT REACHES: the whole of it comes at the lens, and then it
                # is standing back where it was, as if it never moved.
                self.lunge_k = 1.0
                self.lamp1 = 0.15
                self._fx_strike(big=True)
                self.tear = 0.9
                self.spend_nerve(14)
                self.read = False
                self.guard = False
                self.held = False
                self.last_enemy = "reach"
                self._beat("IT REACHES", "-" + str(dmg), self._after_enemy(),
                           kind="it")
                return

            move = self._pick_enemy_move()
            self.last_enemy = move
            label = "IT"
            value = ""
            dmg = 0
            nerve_dmg = 0

            if move == "loom":
                # The closer it is standing, the more it costs to be looked at.
                dmg = int(22 + 28 * self.dread_frac())
                self.lunge_k = max(self.lunge_k, 0.45)
            elif move == "whisper":
                nerve_dmg = 9
                hx, hy = self._a1_head()
                for k in range(3):
                    self.fx.ring(hx, hy, 12.0, 260.0 + 80.0 * k, life=34 + 8 * k,
                                 col="#9aa89e", alpha=0.30, layer="front",
                                 tex="ring_soft")
                self.tear = max(self.tear, 0.45)
            elif move == "still":
                # THE UNCANNY TURN. Nothing happens. Nothing is printed. The
                # only turn in this project that resolves to a blank -- and it
                # is why the next one lands twice as hard.
                self.held = True
                self.play("tick", 0.4)
                self.read = False
                self.guard = False
                self.lamp1_still = 1.0
                self._beat(label, "", self._after_enemy(), kind="it")
                return
            elif move == "behind":
                self.dread = min(float(HOR_DREAD_MAX), self.dread + 26)
                self.play("wind", 0.7)
                # It is not there -- and then it is, nearer. No walk between.
                self.blink_t = 26
                self.dread_shown = self.dread
                self.lamp1 = 0.22
                value = "CLOSER"
            elif move == "mimic":
                # It does what you just did, at you.
                if self.last_cmd == "light":
                    dmg = 30
                elif self.last_cmd == "listen":
                    nerve_dmg = 12
                elif self.last_cmd == "steady":
                    self.resolve = int(min(HOR_RESOLVE_MAX, self.resolve + 40))
                    value = "+40"
                else:
                    dmg = 20
                label = "IT COPIES"

            if self.held and (dmg or nerve_dmg):
                dmg *= 2
                nerve_dmg *= 2
                self.held = False

            if dmg > 0:
                if self.guard:
                    dmg = int(dmg * HOR_GUARD_MULT)
                if self.read:
                    dmg = int(dmg * HOR_READ_MULT)
                self.play("enemy", 0.8)
                self.hurt(dmg, 1004, 586)
                self._fx_strike(big=dmg >= 40)
                value = "-" + str(dmg)
            if nerve_dmg > 0:
                if self.read:
                    nerve_dmg = int(nerve_dmg * HOR_READ_MULT)
                self.spend_nerve(nerve_dmg)
                self.play("tick", 0.6)
                value = ("-" + str(nerve_dmg) + " NERVE") if not value else value

            self.read = False
            self.guard = False
            self._beat(label, value, self._after_enemy(), kind="it")

        def _a1_head(self):
            """Where its head is on screen in act one (for effects that come
            from it). Same placement the stage draws it at."""
            persp, feet = hor_a1_place(self.dread_shown / HOR_DREAD_MAX)
            zoom = HOR_A1_ZOOM * persp / 0.5
            return (640.0, feet - HOR_FIG_H * zoom * 0.86)

        def _after_enemy(self):
            if self.resolve <= HOR_SHIFT_RESOLVE or self.turn >= HOR_SHIFT_TURN_CAP:
                return "shift"
            return "menu"

        # =====================================================================
        # THE TEAR
        # =====================================================================

        def _step_shift(self):
            self.mtick += 1
            t = self.mtick

            if t == 1:
                inv_music_stop(0.3)
                self.play("tear")
                self.tear = 0.8
            if t == 24:
                # THE WINDOWS GO OUT LIKE A LIGHT: they do not slide away,
                # they crumble into the dark and the dark takes the pieces.
                self.panel_slide = 1.0
                for (bx0, by0, bw, bh) in (HORStage.PANEL_CMD, HORStage.PANEL_HUD):
                    for _k in range(30):
                        x = bx0 + self.rng_fx.uniform(0.0, bw)
                        y = by0 + self.rng_fx.uniform(0.0, bh)
                        self.fx.emit(INV_SHARDS[_k % 4], x, y,
                                     vx=self.rng_fx.uniform(-1.5, 1.5),
                                     vy=self.rng_fx.uniform(-2.5, 0.5),
                                     life=self.rng_fx.randint(40, 70),
                                     size=self.rng_fx.uniform(0.35, 0.8),
                                     rot=self.rng_fx.uniform(0, 360),
                                     vrot=self.rng_fx.uniform(-6, 6),
                                     col="#b8c4ba", alpha=0.85, add=False,
                                     drag=0.99, ay=0.16, layer="hud", fade="out")
                    self.fx.burst(INV_SMOKES, bx0 + bw * 0.5, by0 + bh * 0.5, 10,
                                  speed=(0.4, 1.6), life=(40, 70),
                                  size=(0.8, 1.6), size1=2.2, col="#05070a",
                                  alpha=0.8, add=False, drag=0.97,
                                  jitter=160.0, squash=0.4, layer="hud")
                self.play("break", 0.6)
            if 24 <= t < 110:
                self.shake = max(self.shake, 0.3)
                # The lantern gutters down to nothing on the way.
                self.lamp1 = min(self.lamp1, 0.62 * (1.0 - (t - 24) / 86.0))
            if t == 110:
                self.play("slam")
                self.flash = 0.9
                self.shake = 1.0
                self.tear = 1.0
                self.ca = max(self.ca, 0.02)
                inv_music_corruptive()
                # Whole again for the second half: act one's currency was
                # DREAD, and that is what carries.
                self.hp = HOR_HP_MAX
                self.nerve = HOR_NERVE_MAX
            if 110 <= t < 180:
                self.corrupt = inv_clamp((t - 110) / 70.0, 0.0, 1.0)
            if t == 180:
                self.corrupt = 1.0
                self._begin_run()

        # =====================================================================
        # ACT TWO -- THE CHASE
        # =====================================================================

        def _begin_run(self, dev=False):
            self.mode = "run"
            self.mtick = 0
            self.corrupt = 1.0
            self.dark = 0.0
            # THE JOINT: how close it was standing is how much room you get.
            self.gap = inv_clamp(HOR_GAP_MAX - self.dread, 30.0, 80.0)
            self.dist = 0.0
            self.stam = HOR_STAM_MAX
            self.their_speed = HOR_THEIR_SPEED
            self.obstacles = []
            self.phantom = None
            self.spawn_t = 40
            self.lunge_t = HOR_LUNGE_EVERY // 2
            self.lunge_state = "idle"
            self.winded = 0
            self.fear_t = HOR_FEAR_EVERY // 2
            self.fear_kind = None
            self.blind = 0.0
            self.blind_t = 0
            self.glitch = 0.0
            self.glitch_t = 0
            self.look_t = 0
            self.look_view = 0.0
            self.look_lock = 0
            self.resolve_t = 0.0
            self.phase = 0
            self.vast_t = HOR_VAST_EVERY
            self.vast = 0.0
            self.power = HOR_POWER_MAX
            self.lamp = False
            self.lamp_lit = 0.0
            self.lamp_dead = False
            self.watcher = None
            self.watch_t = HOR_WATCH_EVERY_P1
            self.bite_t = 0
            self.watch_taught = False
            self.px = (HOR_LANE_FAR[0] + HOR_LANE_FAR[1]) * 0.5
            # THE PLANE. One line, and the runner never leaves it -- see the
            # note on HOR_ROW.
            self.py = HOR_PLANE_Y
            self.follow_x = 640.0
            self.follow_y = inv_lerp(1080.0, 690.0, self.near_frac())
            self.follow_zoom = inv_lerp(0.22, 0.62, self.near_frac())
            self.follow_alpha = inv_clamp(0.45 + 0.55 * self.near_frac(), 0.0, 1.0)
            self.play("break", 0.8)
            # THE CHECKPOINT: a loss from here can be retried from the tear,
            # with the same distance act one handed over.
            self.checkpoint = {"slug": "horror", "dread": float(self.dread)}
            if dev:
                self.hp = HOR_HP_MAX
                self.hp_shown = float(HOR_HP_MAX)
                inv_music_corruptive()
                inv_heart_start(0.3)

        def _spawn_obstacle(self):
            """Place one mass, and REFUSE to place it if doing so would seal
            the corridor (fairness rule 3). Better a quiet moment than an
            unavoidable hit."""
            lo, hi = self.lane()
            clear = (hi - lo) * HOR_SPAWN_CLEAR_FRAC
            reach = None

            # A WALL REACHER, once the walls have started doing that. Pinned
            # to an edge and growing inward, so the corridor itself is what is
            # attacking you rather than something floating in it.
            chance = 0.0
            if self.phase >= 1:
                chance = inv_lerp(HOR_REACH_CHANCE_P1, HOR_REACH_CHANCE_P3,
                                inv_clamp((self.phase - 1) / 2.0, 0.0, 1.0))
            if self.rng.random() < chance:
                reach = self.rng.choice((0, 1))
                w = self.rng.uniform(*HOR_REACH_W)
            else:
                w = float(self.rng.choice((70, 90, 110, 140, 180)))
            w = min(w, (hi - lo) - clear)
            if w < 40.0:
                return

            # Anything already at a similar DEPTH constrains us.
            neighbours = [o for o in self.obstacles
                        if abs(o["z"] - HOR_Z_FAR) < 0.16]

            for _attempt in range(8):
                if reach is not None:
                    x = (lo + w * 0.5) if reach == 0 else (hi - w * 0.5)
                else:
                    x = self.rng.uniform(lo + w * 0.5, hi - w * 0.5)
                blocked = False
                for o in neighbours:
                    # Widest opening left between the two of them, on either
                    # side and between them.
                    left_edge = min(x - w * 0.5, o["x"] - o["w"] * 0.5)
                    right_edge = max(x + w * 0.5, o["x"] + o["w"] * 0.5)
                    between = abs(x - o["x"]) - (w + o["w"]) * 0.5
                    open_left = left_edge - lo
                    open_right = hi - right_edge
                    if (between < clear
                            and open_left < clear
                            and open_right < clear):
                        blocked = True
                        break
                if not blocked:
                    self.obstacles.append({
                        "x": x, "z": HOR_Z_FAR, "w": w,
                        "h": float(self.rng.choice((60, 80, 100))
                                if reach is None
                                else self.rng.choice((150, 210, 280))),
                        "passed": False, "grazed": False,
                        "reach": reach,
                        "seed": self.rng.random(),
                    })
                    return
            # Eight refusals means the corridor is genuinely busy. Skip.

        def _step_look(self, held):
            """LOOK BACK: the bargain.

            Holding Z turns you round. While you are turned you are slower,
            you are burning wind, and you cannot see a thing that is coming.
            What you get for it is RESOLVE -- and the payment scales with how
            long you managed to hold it AND how close the thing was, so the
            worst possible moment to look is also the most valuable one.

            Hold past HOR_LOOK_MAX and it has you instead."""
            self.looking = bool(held["z"]) and self.look_lock <= 0

            if self.look_lock > 0:
                self.look_lock -= 1

            if self.looking:
                self.look_t += 1
                self.look_view = min(1.0, self.look_view + 1.0 / HOR_LOOK_TURN)
                self.stam = max(0.0, self.stam - HOR_LOOK_DRAIN)
                if self.look_t == 1:
                    self.play("wind2", 0.55)
                # It gets worse the longer you hold it, and it says so.
                if self.look_t % 34 == 0:
                    self.play("note", 0.30 + 0.45 * self.look_frac())
                    inv_heart_level(inv_clamp(0.35 + 0.6 * self.look_frac(),
                                            0.0, 1.0))
                if self.look_t >= HOR_LOOK_MAX:
                    self._overwhelmed()
            else:
                if self.look_t > 0:
                    self._release_look()
                self.look_t = 0
                self.look_view = max(0.0,
                                    self.look_view - 1.0 / (HOR_LOOK_TURN * 0.7))

            if self.resolve_t > 0.0:
                self.resolve_t = max(0.0, self.resolve_t - 1.0)

        def _release_look(self):
            """You looked away in time."""
            frac = self.look_frac()
            if self.look_t < HOR_LOOK_MIN:
                # A glance is not a stare. It buys nothing, and it should not:
                # the whole point is that the payment is for the part that was
                # hard to keep doing.
                return
            near = self.near_frac()
            gain = HOR_RESOLVE_MAX * frac * (0.45 + 0.85 * near)
            self.resolve_t = min(HOR_RESOLVE_MAX, self.resolve_t + gain)
            self.stam = min(HOR_STAM_MAX,
                            self.stam + HOR_LOOK_STAM_BACK * frac)
            # AND THE GROUND BACK. Turning round costs you distance the whole
            # time you do it; coming out the other side is what buys it back,
            # which is why the bargain is worth making at all.
            self.gap = min(HOR_GAP_MAX, self.gap + HOR_LOOK_GAP_BACK * frac
                        * (0.5 + 0.5 * near))
            self.play("phase", 0.45 + 0.4 * frac)
            self.flash = max(self.flash, 0.18 + 0.25 * frac)
            self.float_text(self.px, self.py - 70, "RESOLVE", HOR_PALE, True)

        def _overwhelmed(self):
            """You held it too long. It does not attack you -- you simply stop
            being able to run, which is worse and takes longer."""
            self.look_lock = HOR_LOOK_LOCK
            self.looking = False
            self.look_t = 0
            self.look_view = 0.0
            self.resolve_t = 0.0
            self.stumble = HOR_STUMBLE_TICKS + 12
            self.gap = max(0.0, self.gap - HOR_GAP_STUMBLE * 2.2)
            self.stam = max(0.0, self.stam - 30.0)
            self.scramble = max(self.scramble, HOR_SCRAMBLE_TICKS)
            self.lurch = 1.0
            self.shake = 1.0
            self.freeze = 6
            self.hurt(HOR_STUMBLE_HP, self.px, self.py - 30)
            self.play("struck", 0.95)
            self.tear = 1.0
            self._kick_lens(640.0, 400.0, 1.2, 0.02)

        def _step_lamp(self, held):
            """THE LANTERN. Hold W (or UP) to raise it.

            It cannot be raised while you are turned round -- a lantern held
            up behind you is the one thing worse than either -- and it dies
            for good when the tank empties. Nothing refills it. That is the
            whole clock: one tank of light for one corridor."""
            want = (bool(held["up"]) and not self.lamp_dead
                    and self.power > 0.0 and self.look_view < 0.5)
            self.lamp = want
            rate = 1.0 / HOR_LAMP_WARM
            if want:
                self.lamp_lit = min(1.0, self.lamp_lit + rate)
                self.power = max(0.0, self.power - HOR_POWER_DRAIN)
                if self.power <= 0.0 and not self.lamp_dead:
                    self.lamp_dead = True
                    self.play("struck", 0.55)
                    self.shake = max(self.shake, 0.4)
                    self.float_text(self.px, self.py - 74, "OUT", HOR_BLOOD,
                                    True)
                    self.fx.burst("spark", self.px + 22.0, self.py - 16.0, 14,
                                  speed=(1.0, 4.0), life=(10, 26),
                                  size=(0.18, 0.34), col="#ffcf8a",
                                  drag=0.90, ay=0.12, stretch=0.10,
                                  layer="front")
                    self.fx.burst(INV_SMOKES, self.px + 22.0, self.py - 20.0, 4,
                                  speed=(0.3, 1.0), life=(30, 50),
                                  size=(0.3, 0.6), size1=1.8, col="#3a3a3a",
                                  alpha=0.5, add=False, drag=0.98, ay=-0.03,
                                  layer="front")
            else:
                self.lamp_lit = max(0.0, self.lamp_lit - rate)

        def _step_watcher(self):
            """A thing in the wall that advances whenever nobody is looking at
            it, and holds perfectly still the rest of the time.

            The clock is the only thing about it that is continuous. Position
            is not: it is at one of HOR_WATCH_Z and it stays there until the
            step timer fires, and then it is simply somewhere else."""
            w = self.watcher
            if w is None:
                if self.phase < HOR_WATCH_FROM_PHASE:
                    return
                # Never on top of a lunge; one bad thing at a time.
                if self.lunge_state != "idle":
                    return
                self.watch_t -= 1
                if self.watch_t <= 0:
                    lo, hi = self.lane()
                    self.watcher = {"side": self.rng.choice((0, 1)),
                                    "stage": 0, "p": 0.0,
                                    "z": HOR_WATCH_Z[0], "seen": 0.0,
                                    "moved": 0}
                    self.play("note", 0.55)
                return

            # Lit, and standing on its side of the corridor: it gives ground.
            pushing = self.lit() and self.watch_side_ok()

            # ONE SIGNED ACCUMULATOR, NOT TWO CLOCKS. The obvious build is a
            # countdown that resets whenever the answer changes, and it is
            # wrong both ways round: leave it running and half a push silently
            # becomes half an advance the moment a mass forces you off its
            # side of the corridor; reset it and a one-tick flick of the
            # lantern every hundred ticks freezes the thing forever for almost
            # no power. A single value that climbs while it is unwatched and
            # falls while it is, with a step fired at either end, has neither
            # failure -- and it is a more honest readout, because there is
            # exactly one number to draw.
            w["p"] += (-1.0 / HOR_WATCH_RECOVER) if pushing \
                else (1.0 / HOR_WATCH_STEP)
            w["seen"] = inv_clamp(w["seen"] + (0.06 if pushing else -0.05),
                                0.0, 1.0)
            # The jolt decays HERE, not in the renderer -- render() runs at
            # whatever the display feels like and the simulation does not.
            if w["moved"] > 0:
                w["moved"] -= 1

            if w["p"] <= -1.0:
                w["p"] = 0.0
                w["stage"] -= 1
                self.watch_taught = True
                if w["stage"] < 0:
                    # Driven back off the end of the corridor. It does not
                    # die; it simply stops being there.
                    self.watcher = None
                    self.watch_t = self._watch_gap()
                    self.play("wind2", 0.40)
                    return
                self.play("graze", 0.55)
            elif w["p"] >= 1.0:
                w["p"] = 0.0
                w["stage"] += 1
                if w["stage"] >= HOR_WATCH_STAGES:
                    self._bitten()
                    return
                w["moved"] = 12
                self.play("clash", 0.35 + 0.16 * w["stage"])
                self.shake = max(self.shake, 0.12 + 0.10 * w["stage"])
                # It comes off the wall in a hard step, and the wall gives up
                # a little of itself where it was.
                persp_w, wy_w = hor_project(w["z"])
                lo_w, hi_w = self.lane()
                wx_w = hor_screen_x(lo_w if w["side"] == 0 else hi_w, persp_w)
                self.fx.burst(INV_SMOKES, wx_w, wy_w - 140.0 * persp_w, 4,
                              speed=(0.3, 1.4), life=(30, 50),
                              size=(0.4, 0.8), size1=1.7, col="#1c1d1c",
                              alpha=0.6, add=False, drag=0.96,
                              jitter=40.0 * persp_w, layer="front")
                inv_heart_level(inv_clamp(0.4 + 0.18 * w["stage"], 0.0, 1.0))
            else:
                return
            w["z"] = HOR_WATCH_Z[int(inv_clamp(w["stage"], 0,
                                            HOR_WATCH_STAGES - 1))]

        def _watch_gap(self):
            base = inv_lerp(HOR_WATCH_EVERY_P1, HOR_WATCH_EVERY_P3,
                            inv_clamp((self.phase - HOR_WATCH_FROM_PHASE) / 2.0,
                                    0.0, 1.0))
            return int(base) + self.rng.randint(-70, 70)

        def _bitten(self):
            """It got all the way across the wall. This is the one moment in
            the chase that is allowed to be a cheap shock, and it is cheap on
            purpose -- the genre invented the move."""
            # IT DOES NOT GO AWAY. It falls back to where it was two steps
            # ago and starts again, which is the whole point of the mechanic
            # and the reason its numbers could come down: ignoring a watcher
            # is not a one-off tax you pay and forget, it is the same thing
            # arriving again on a shorter clock than the one you already
            # failed. The only way it stops is the lantern.
            w = self.watcher
            if w is not None:
                w["stage"] = 0
                w["p"] = 0.0
                w["moved"] = 12
                w["seen"] = 0.0
                w["z"] = HOR_WATCH_Z[w["stage"]]
            self.bite_t = HOR_BITE_FREEZE
            self.freeze = HOR_BITE_FREEZE
            self.stumble = HOR_STUMBLE_TICKS + 10
            self.gap = max(0.0, self.gap - HOR_BITE_GAP)
            self.stam = max(0.0, self.stam - HOR_BITE_STAM)
            self.scramble = max(self.scramble, HOR_SCRAMBLE_TICKS)
            self.shake = 1.0
            self.lurch = 1.0
            self.flash = max(self.flash, 0.55)
            self.hurt(HOR_BITE_HP, self.px, self.py - 30)
            self.play("struck", 1.0)
            self.play("clash", 0.9)
            self.tear = 1.0
            self._kick_lens(640.0, 470.0, 1.4, 0.022)

        def _step_atmos(self):
            """The pot coming to the boil. Each rung announces itself exactly
            once -- a jolt you feel rather than a caption you read -- and then
            the new layer is simply always there afterwards."""
            prog = self.run_frac()
            want = 0
            for i, at in enumerate(HOR_PHASE_AT):
                if prog >= at:
                    want = i
            if want > self.phase:
                self.phase = want
                self.shake = max(self.shake, 0.55)
                self.lurch = max(self.lurch, 0.8)
                self.play("slam", 0.45 + 0.12 * want)
                self.play("wind", 0.5)
                inv_heart_level(inv_clamp(0.3 + 0.2 * want, 0.0, 1.0))

            # SOMETHING ENORMOUS GOES PAST. It cannot hurt you. It is not for
            # that.
            if self.vast > 0.0 or self.vast_t <= 0:
                if self.vast_t <= 0:
                    self.vast_t = HOR_VAST_LEN
                    self.vast = 0.0001
                    self.play("wind", 0.85)
                self.vast_t -= 1
                u = 1.0 - abs((self.vast_t / float(HOR_VAST_LEN)) - 0.5) * 2.0
                self.vast = inv_clamp(u * 1.15, 0.0, 1.0)
                if self.vast_t <= 0:
                    self.vast = 0.0
                    self.vast_t = HOR_VAST_EVERY + self.rng.randint(-220, 220)
            elif self.phase >= 1:
                self.vast_t -= 1

        def _spawn_phantom(self):
            """It is ahead of you. It cannot be ahead of you."""
            lo, hi = self.lane()
            span = max(40.0, (hi - lo) * 0.5 - 40.0)
            mid = (lo + hi) * 0.5
            self.phantom = {"x": self.rng.uniform(mid - span, mid + span),
                            "z": HOR_Z_FAR, "life": 420, "touched": False}
            self.play("wind2", 0.5)

        def _step_run(self, edges):
            self.mtick += 1
            if self.bite_t > 0:
                self.bite_t -= 1
            if self.freeze > 0:
                self.freeze -= 1
                return

            held = edges["held"]
            lo, hi = self.lane()

            # --- what you are doing ------------------------------------------
            self._step_look(held)
            self._step_lamp(held)
            # STARTING a sprint needs a minimum in the tank; CONTINUING one
            # does not. That asymmetry is what makes WINDED reachable at all
            # -- gate the continuation too and stamina can never hit zero, the
            # lockout never fires, and the cooldown is dead code.
            if self.sprinting:
                want_sprint = bool(held["x"]) and self.winded <= 0
            else:
                want_sprint = (bool(held["x"]) and self.winded <= 0
                            and self.stam > HOR_STAM_MIN_SPRINT)
            if self.stumble > 0:
                self.stumble -= 1
                self.speed = 0.0
                self.sprinting = False
                self.stam = min(HOR_STAM_MAX, self.stam + HOR_STAM_RECOVER)
            elif self.winded > 0:
                # THE COOLDOWN. Emptying the tank does not merely end the
                # sprint -- it locks the sprint out and drops you BELOW a walk
                # until you have your wind back. The skill is letting go
                # early, not holding the key down.
                self.winded -= 1
                self.sprinting = False
                self.speed = HOR_WINDED_SPEED
                self.stam = min(HOR_STAM_MAX, self.stam + HOR_STAM_RECOVER)
            else:
                # RESOLVE is what a survived stare bought you: you run faster
                # and you tire slower, and both are worth more the worse
                # things already are.
                res = self.resolved()
                self.sprinting = want_sprint
                if self.sprinting:
                    self.speed = HOR_SPRINT * inv_lerp(1.0, HOR_RESOLVE_SPRINT,
                                                    res)
                    self.stam = max(0.0, self.stam - HOR_STAM_DRAIN
                                    * inv_lerp(1.0, HOR_RESOLVE_DRAIN, res))
                    if self.stam <= 0.0:
                        self.winded = HOR_WINDED_TICKS
                        self.play("struck", 0.5)
                else:
                    self.speed = HOR_WALK
                    self.stam = min(HOR_STAM_MAX, self.stam + HOR_STAM_RECOVER)

                # Turning round costs speed, and it costs MORE the longer you
                # keep looking -- the stare is not a stance you settle into,
                # it is something you are losing ground to the whole time.
                if self.look_view > 0.0:
                    stare = HOR_LOOK_SPEED - HOR_LOOK_SLOW * self.look_frac()
                    self.speed = inv_lerp(self.speed,
                                        min(self.speed, stare),
                                        self.look_view)

            # --- steering ------------------------------------------------------
            # ONE AXIS. The runner lives on the plane the collision test is
            # taken at, so there is no way to be visually clear of a mass and
            # struck by it anyway. Up and down belong to the lantern.
            sgn = -1.0 if self.scramble > 0 else 1.0
            if self.scramble > 0:
                self.scramble -= 1
            dx = ((1.0 if held["right"] else 0.0)
                - (1.0 if held["left"] else 0.0)) * sgn
            self.px = inv_clamp(self.px + dx * HOR_STRAFE, lo, hi)
            self.py = HOR_PLANE_Y

            self.trail.insert(0, (self.px, self.py, self.sprinting))
            if len(self.trail) > 12:
                self.trail.pop()

            # --- it never tires ------------------------------------------------
            self.their_speed += HOR_THEIR_RAMP
            their = self.their_speed
            if self.lunge_state == "live":
                their *= HOR_LUNGE_MULT
            # AND A LIT RUNNER IS AN EASY ONE TO FOLLOW. This is the whole
            # price of the lantern in the moment -- the tank is only the price
            # over the run -- and it is charged smoothly off how far up the
            # light actually is, so flicking it does not cost a full second.
            their += HOR_LAMP_SEEN * self.lamp_lit

            self.gap += (self.speed - their) * HOR_GAP_K
            self.gap = inv_clamp(self.gap, 0.0, HOR_GAP_MAX)
            self.dist += self.speed
            self.scroll += self.speed * HOR_SCROLL_PX

            inv_heart_level(0.20 + 0.65 * self.near_frac())

            if self.gap <= 0.0:
                self.caught = True
                self._begin_leave(False)
                return
            if self.dist >= HOR_GOAL:
                self._begin_leave(True)
                return

            # --- the lunge -----------------------------------------------------
            self.lunge_t -= 1
            if self.lunge_state == "idle" and self.lunge_t <= 0:
                self.lunge_state = "warn"
                self.lunge_t = HOR_LUNGE_WARN
                self.play("wind2", 0.9)
                inv_heart_level(0.9)
            elif self.lunge_state == "warn" and self.lunge_t <= 0:
                self.lunge_state = "live"
                self.lunge_t = HOR_LUNGE_LEN
                self.play("clash", 0.8)
                self.shake = 0.7
            elif self.lunge_state == "live" and self.lunge_t <= 0:
                self.lunge_state = "idle"
                self.lunge_t = HOR_LUNGE_EVERY + self.rng.randint(-120, 120)
                # It falls back a little, and it is not tired.
                self.gap = min(HOR_GAP_MAX, self.gap + 4.0)

            # --- obstacles -----------------------------------------------------
            self.spawn_t -= 1
            if self.spawn_t <= 0:
                prog = inv_clamp(self.dist / HOR_GOAL, 0.0, 1.0)
                base = int(inv_lerp(HOR_SPAWN_FAR, HOR_SPAWN_NEAR, prog))
                self.spawn_t = base + self.rng.randint(-6, 10)
                self._spawn_obstacle()

            step_px = self.speed * HOR_SCROLL_PX
            if self.near_cd > 0:
                self.near_cd -= 1

            keep = []
            dz = self.speed * HOR_Z_RATE
            for o in self.obstacles:
                was = o["z"]
                o["z"] -= dz
                # It only ever touches you at YOUR plane, so the test fires on
                # the frame it crosses -- no y-overlap fudging, no double hits.
                if not o["passed"] and o["z"] <= HOR_Z_NEAR < was + 1e-9:
                    o["passed"] = True
                    ddx = abs(o["x"] - self.px)
                    if ddx < (o["w"] * 0.5 + HOR_HIT_R):
                        self._stumble()
                    elif ddx < o["w"] * 0.5 + HOR_NEARMISS_R:
                        # THE SKILL CURVE. Threading it refunds wind, and
                        # mends a little -- the odometer rolls UP, which is
                        # the one time in either act that it does.
                        self.stam = min(HOR_STAM_MAX,
                                        self.stam + HOR_STAM_NEARMISS)
                        if self.hp < HOR_HP_MAX:
                            self.hp = int(min(HOR_HP_MAX,
                                            self.hp + HOR_HP_NEARMISS))
                        self.play("graze", 0.5)
                        side = 1.0 if o["x"] < self.px else -1.0
                        self.fx.burst("spark", self.px - side * 14.0, self.py - 8.0, 7,
                                      speed=(2.0, 6.0), life=(8, 14),
                                      size=(0.16, 0.30), col="#e8e0c0",
                                      angle=(0.0 if side > 0 else 180.0) - 90.0 * 0.4,
                                      spread=90.0, stretch=0.12, drag=0.85,
                                      layer="front")
                if o["z"] > HOR_Z_GONE:
                    keep.append(o)
            self.obstacles = keep

            # --- IT HUNTS ------------------------------------------------------
            # It does not float about behind you on a sine wave -- it comes
            # across into whatever lane you ran to, with a lag you can feel and
            # cannot out-turn. All of it is eased, so a lunge does not snap.
            lunging = (self.lunge_state == "live")
            near_now = self.near_frac()
            tx = inv_lerp(640.0, self.px, 0.85)
            self.follow_x += (tx - self.follow_x) * (0.075 if lunging else 0.038)
            self.follow_x += math.sin(self.clock * 1.7) * 1.1 * (1.0 - near_now)
            ty = inv_lerp(1080.0, 690.0, near_now) - (70.0 if lunging else 0.0)
            tz = inv_lerp(0.22, 0.62, near_now) * (1.14 if lunging else 1.0)
            self.follow_y += (ty - self.follow_y) * 0.075
            self.follow_zoom += (tz - self.follow_zoom) * 0.075
            ta = inv_clamp(0.45 + 0.55 * near_now, 0.0, 1.0)
            self.follow_alpha += (ta - self.follow_alpha) * 0.06

            # --- the three fears, turned back on you ----------------------------
            self._step_fears(step_px)
            self._step_watcher()
            self._step_atmos()

        def _step_fears(self, step_px):
            """One fear at a time, never overlapping, each with a tell.

            GHOST is a phantom of it standing AHEAD of you, which it cannot
            be. DARK puts the light out entirely for a moment. BUG faults the
            encounter itself -- rows tear, the readouts stop being true, and
            your hands come back wrong. None of the three can kill you on
            their own; each one costs you the thing that can."""
            if self.blind_t > 0:
                self.blind_t -= 1
                # In, hold, out -- never a hard cut to black.
                u = 1.0 - abs((self.blind_t / float(HOR_BLIND_LEN)) - 0.5) * 2.0
                self.blind = inv_clamp(u * 1.2, 0.0, 1.0)
            else:
                self.blind = max(0.0, self.blind - 0.05)

            if self.glitch_t > 0:
                if self.glitch_t == HOR_GLITCH_LEN:
                    self.scramble = max(self.scramble, HOR_SCRAMBLE_ON_GLITCH)
                self.glitch_t -= 1
                self.glitch = inv_clamp(self.glitch_t / 24.0, 0.0, 1.0)
            else:
                self.glitch = max(0.0, self.glitch - 0.08)

            if self.phantom is not None:
                p = self.phantom
                p["z"] -= self.speed * HOR_Z_RATE * 0.82
                p["life"] -= 1
                if (not p["touched"] and p["z"] <= HOR_Z_NEAR
                        and abs(p["x"] - self.px) < 74):
                    p["touched"] = True
                    self.scramble = HOR_SCRAMBLE_TICKS
                    self.stam = max(0.0, self.stam - 22.0)
                    self.play("struck", 0.7)
                    self.shake = 0.8
                    self.lurch = 1.0
                if p["life"] <= 0 or p["z"] <= HOR_Z_GONE:
                    self.phantom = None

            # Never stack a fear on a lunge, on another fear, or on a watcher
            # that has already started coming -- and DARK in particular must
            # never land while one is on the wall, because putting the light
            # out is the one thing you cannot answer it without.
            if (self.phantom is not None or self.blind_t > 0
                    or self.glitch_t > 0 or self.lunge_state != "idle"
                    or self.look_view > 0.05
                    or (self.watcher is not None
                        and self.watcher["stage"] >= 1)):
                return

            self.fear_t -= 1
            if self.fear_t > 0:
                return
            self.fear_t = HOR_FEAR_EVERY + self.rng.randint(-HOR_FEAR_JITTER,
                                                            HOR_FEAR_JITTER)
            kind = self.rng.choice(("ghost", "dark", "bug"))
            self.fear_kind = kind
            if kind == "ghost":
                self._spawn_phantom()
            elif kind == "dark":
                self.blind_t = HOR_BLIND_LEN
                self.play("wind", 0.85)
            else:
                self.glitch_t = HOR_GLITCH_LEN
                self.play("tear", 0.6)
                self.tear = 1.0

        def _stumble(self):
            self.stumble = HOR_STUMBLE_TICKS
            self.gap = max(0.0, self.gap - HOR_GAP_STUMBLE)
            self.hurt(HOR_STUMBLE_HP, self.px, self.py - 30)
            self.lurch = 1.0
            self.shake = 1.0
            self.freeze = 4
            self.play("cut_big", 0.8)
            # Into it at speed: grit and dark matter thrown up off the floor.
            self.fx.burst(INV_SMOKES, self.px, self.py, 5, speed=(1.0, 3.0),
                          life=(24, 40), size=(0.5, 0.9), size1=1.6,
                          col="#20171a", alpha=0.7, add=False, drag=0.94,
                          angle=-90.0, spread=160.0, layer="front", squash=0.5)
            self.fx.burst(INV_SHARDS, self.px, self.py - 10, 8, speed=(2.0, 6.0),
                          life=(16, 30), size=(0.2, 0.4), col="#4a3a3c",
                          add=False, drag=0.92, ay=0.30, angle=-90.0,
                          spread=150.0, vrot=(-12.0, 12.0), layer="front")
            self._kick_lens(self.px, self.py - 30, 0.7, 0.012)

        # =====================================================================
        # DEPARTURE
        # =====================================================================

        def _begin_leave(self, won):
            self.mode = "leave_w" if won else "leave_l"
            self.mtick = 0
            self.obstacles = []
            self.phantom = None
            self.watcher = None
            self.bite_t = 0
            self.lamp = False
            self.lamp_lit = 0.0
            self.blind_t = 0
            self.glitch_t = 0
            self.shake = 0.0
            self.heart_x = self.px
            self.heart_y = self.py
            self.heart_scale = 1.0
            self.heart_diss = 0.0
            self.hud_fade = 1.0
            self.exit_rush = 1.0
            self.exit_warp = 1.7
            # Captured, so every ramp below starts from where things ACTUALLY
            # are. Lerping from a constant is what made it jump.
            self.exit_from_y = self.follow_y
            self.exit_from_zoom = self.follow_zoom
            self.exit_from_alpha = self.follow_alpha
            inv_music_stop(3.0 if won else 1.6)
            # No sting either way. A victory chime would be the single
            # funniest thing in the encounter.

        def _step_leave(self):
            """THE WIN IS LOUD IN THE MIDDLE AND SILENT AT THE END.

            The first build of this ending was a portal-suck and the sprite
            scaling to 2.7x, and the user's verdict was "more hilarious than
            fear-inducing" -- so it was rebuilt out of pure stillness, and that
            stillness is still what it ENDS on. What it no longer does is skip
            the escape.

            The rule this sequence is written against (user, Aug 23 2026):
            BIG, BUT NEVER TRIUMPHANT. There is no portal, no sting, no
            flourish that could read as a win screen, and the loudest beat in
            it is the thing COMING AT YOU. What is spectacular here is what
            happens to the CORRIDOR -- because a chase can only end two ways,
            and the one where the ground gives out is not a celebration.

                SURGE     it does not accept it. One last close, the walls at
                          their tightest, the lantern gutters out entirely.
                BREAK     the corridor lets go. Everything that was
                          architecture goes past you backwards at a rate
                          nothing in the fight has moved at, and the enormous
                          thing outside the walls comes past ALL of it at once.
                TORN OFF  it is not sucked anywhere. The collapse takes it, and
                          it is still reaching while it goes.
                THE THROAT  everything stops dead. Straight, empty, much too
                          long.
                HELD      longer than is comfortable. Then the dark.

            LOST -- unchanged, and the opposite of a pounce. Everything STOPS.
            It does not grow, it does not lunge -- it closes the last of the
            distance at walking pace and stands there. The heart stops beating.
            The light goes out around it. And then nothing happens for a long
            time.
            """
            self.mtick += 1
            t = self.mtick
            won = (self.mode == "leave_w")

            if won:
                # ============ 1. THE SURGE (0-52) ==========================
                # It has lost and it comes anyway. This is the most
                # frightening moment in the encounter and it happens AFTER
                # you have won, which is the only joke this fight is allowed
                # and is not a funny one.
                if t < 52:
                    u = t / 52.0
                    if t == 2:
                        self.play("enemy", 1.0)
                        self.flash = 0.30
                        self.lurch = 1.0
                    self.exit_rush = 1.0
                    self.scroll += HOR_SPRINT * HOR_SCROLL_PX * 1.10
                    # It closes to nothing, and the lantern goes out.
                    self.gap = max(0.0, self.gap - 1.9)
                    self.blind = min(1.0, self.blind + 0.030)
                    self.lamp_lit = max(0.0, self.lamp_lit - 0.045)
                    self.follow_y = inv_lerp(self.exit_from_y, 660.0,
                                            inv_smooth(u))
                    self.follow_zoom = inv_lerp(self.exit_from_zoom, 0.92,
                                                inv_smooth(u))
                    self.follow_alpha = inv_lerp(self.exit_from_alpha, 1.0,
                                                inv_smooth(u))
                    self.follow_x += (640.0 - self.follow_x) * 0.05
                    self.exit_warp = inv_lerp(1.7, 3.1, inv_smooth(u))
                    inv_heart_level(inv_lerp(0.55, 1.0, u))
                    self.shake = max(self.shake, 0.25 + 0.55 * u)

                # ============ 2. THE CORRIDOR BREAKS (52-124) ==============
                elif t < 124:
                    u = (t - 52) / 72.0
                    su = inv_smooth(u)
                    if t == 52:
                        self.play("slam", 1.0)
                        self.play("tear", 0.95)
                        self.flash = 0.85
                        self.lurch = 1.0
                        self.shake = 1.0
                        # The enormous thing outside the walls, and this time
                        # it does not merely pass -- it is the whole reason
                        # the walls stop being walls.
                        # `vast` is re-asserted every tick below rather than
                        # latched, so it does not matter whether the corridor's
                        # own scheduler is still running underneath this.
                        self.vast = 1.0
                    # Nothing in this fight has ever moved at this rate.
                    self.exit_rush = inv_lerp(1.0, 4.6, su)
                    self.scroll += HOR_SPRINT * HOR_SCROLL_PX * self.exit_rush
                    self.vast = max(self.vast, 1.0 - u * 0.35)
                    self.blind = max(0.0, self.blind - 0.012)
                    self.exit_warp = inv_lerp(3.1, 4.4, su)
                    self.shake = max(self.shake, 0.85 * (1.0 - u * 0.5))
                    inv_heart_level(max(0.0, 1.0 - u * 1.3))
                    if t == 96:
                        inv_heart_stop(1.6)

                # ============ 3. TORN OFF (124-196) ========================
                elif t < 196:
                    u = (t - 124) / 72.0
                    su = inv_smooth(u)
                    if t == 124:
                        self.play("struck", 0.85)
                        self.flash = 0.42
                    # It is not sucked anywhere and nothing collects it. The
                    # corridor going means it goes with it, and it is still
                    # reaching the entire way out.
                    self.exit_rush = inv_lerp(4.6, 1.2, su)
                    self.scroll += HOR_SPRINT * HOR_SCROLL_PX * self.exit_rush
                    self.follow_y = inv_lerp(660.0, 1320.0, su)
                    self.follow_zoom = inv_lerp(0.92, 0.03, su * su)
                    self.follow_alpha = inv_lerp(1.0, 0.0, inv_smooth(
                        inv_clamp((u - 0.35) / 0.65, 0.0, 1.0)))
                    self.follow_x += (640.0 - self.follow_x) * 0.02
                    self.exit_warp = inv_lerp(4.4, 2.0, su)
                    self.vast = max(0.0, self.vast - 0.020)
                    self.hud_fade = 1.0 - su
                    self.gap = min(HOR_GAP_MAX, self.gap + 2.4)

                # ============ 4. THE THROAT (196-286) ======================
                elif t < 286:
                    # Everything stops dead. Nothing happens here and nothing
                    # is supposed to.
                    self.exit_rush = max(0.0, self.exit_rush - 0.045)
                    self.scroll += HOR_WALK * HOR_SCROLL_PX * self.exit_rush
                    self.follow_alpha = 0.0
                    self.vast = 0.0
                    self.blind = 0.0
                    self.hud_fade = 0.0
                    self.exit_warp = inv_lerp(self.exit_warp, 1.4, 0.03)

                # ============ 5. HELD (286+) ===============================
                else:
                    self.follow_alpha = 0.0
                    self.dark = inv_clamp(self.dark + 0.013, 0.0, 1.0)
                    if t > 386:
                        self.result = "victory"

            else:
                # 0-60    everything stops. The chase is simply over.
                # 40-160  it closes the last of the distance at walking pace
                # 120     the heart stops
                # 170-260 the light goes out around it
                # 260+    black, held
                self.exit_rush = inv_lerp(1.0, 0.0, inv_smooth(min(1.0, t / 60.0)))
                self.scroll += HOR_WALK * HOR_SCROLL_PX * self.exit_rush
                self.gap = 0.0

                if t < 120:
                    inv_heart_level(inv_lerp(0.75, 1.0, t / 120.0))
                elif t == 120:
                    inv_heart_stop(0.25)

                if 40 <= t < 160:
                    u = inv_smooth((t - 40) / 120.0)
                    # It is not bigger. It is just no longer far away.
                    self.follow_y = inv_lerp(self.exit_from_y, 700.0, u)
                    self.follow_zoom = inv_lerp(self.exit_from_zoom, 0.80, u)
                    self.follow_alpha = inv_lerp(self.exit_from_alpha, 1.0, u)
                    self.follow_x += (640.0 - self.follow_x) * 0.02
                    self.exit_warp = inv_lerp(1.7, 2.6, u)
                    self.hud_fade = 1.0 - u
                if 170 <= t < 260:
                    self.dark = inv_clamp(self.dark + 0.0085, 0.0, 1.0)
                elif t >= 260:
                    self.dark = inv_clamp(self.dark + 0.02, 0.0, 1.0)
                if t > 330:
                    self.result = "defeat"


# --- THE STAGE ---------------------------------------------------------------
# Oct 2 2026: the corridor is one place in both acts (see inv.dark), the
# renderer draws through the shared kit, the world goes through the lens and
# the HUD is drawn after it. Every value read here is simulation state.
init python:
    from renpy.uguu import GL_REPEAT as _HOR_GL_REPEAT

    class HORStage(renpy.Displayable):
        """One CDD. Steps HORGame at a fixed 60Hz inside render() and paints
        the whole encounter from cached-texture blits."""

        _tf_cache = {}

        PANEL_CMD = (40, 548, 470, 148)
        PANEL_HUD = (770, 548, 470, 148)

        # Bone and soot. No split, no scanlines: a thing seen by lamplight.
        STYLE_PANEL = {"top": "#0a0c0bd8", "bot": "#030404ee",
                       "edge": "#b8c4bab0", "accent": "#8e1622ff",
                       "border": 1.4, "cut": 4.0, "inset": 6.0,
                       "inset_a": 0.12, "noise": 0.22, "scan": 0.0,
                       "split": 0.0, "ticks": 0.0}
        STYLE_PLATE = {"top": "#020303a0", "bot": "#020303c8",
                       "edge": "#b8c4ba50", "accent": "#8e1622ff",
                       "border": 1.0, "cut": 3.0, "inset": 4.0,
                       "inset_a": 0.0, "noise": 0.25, "scan": 0.0,
                       "split": 0.0, "ticks": 0.0}

        def __init__(self, game, **kwargs):
            super(HORStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0

        def _tf(self, key, builder):
            tf = HORStage._tf_cache.get(key)
            if tf is None:
                if len(HORStage._tf_cache) > 600:
                    HORStage._tf_cache.clear()
                tf = builder()
                HORStage._tf_cache[key] = tf
            return tf

        def _body_plain(self, zoom, alpha=1.0, tint=None):
            ab = int(inv_clamp(alpha, 0.0, 1.0) * 6)
            key = ("plain", round(zoom, 3), ab, tint)

            def build():
                kw = dict(zoom=zoom, subpixel=True)
                if ab < 6:
                    kw["alpha"] = ab / 6.0
                if tint:
                    kw["matrixcolor"] = TintMatrix(tint)
                return Transform(HOR_SPRITE, **kw)
            return self._tf(key, build)

        def event(self, ev, x, y, st):
            self.game.keys.handle_event(ev)
            return None

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
                amp = 12.0 * g.shake
                sx = int(math.sin(g.tick * 1.9) * amp)
                sy = int(math.cos(g.tick * 2.7) * amp * 0.6)

            chasing = g.mode == "run" or (g.mode in ("leave_w", "leave_l")
                                         and g.corrupt > 0.4)

            self._room(g, p, chasing)
            if chasing:
                self._chase_world(g, p, sx, sy)
            else:
                self._room_world(g, p, sx, sy)
            inv_fx_paint(p, g.fx, "front", sx, sy)

            p.to_hud()
            if chasing:
                self._chase_hud(g, p, sx, sy)
            else:
                self._room_hud(g, p, sx, sy)
            self._floats(g, p, sx, sy)
            inv_fx_paint(p, g.fx, "hud")
            if g.paused:
                self._pause(g, p)

            rv = inv_compose(p, self._look(g, chasing), g.clock)

            # THE DRAW RATE IS THE TICK RATE (same governor as every stage).
            if g.result is None and not g.paused:
                renpy.redraw(self, max(0.0, INV_TICK - self.acc))
            return rv

        def _look(self, g, chasing):
            """Almost no colour, a lot of grain, and the lantern is the only
            thing allowed to bloom. Dread (act one) and nearness (the chase)
            close the frame."""
            near = g.near_frac() if chasing else g.dread_frac()
            shock = (0.0, 0.0, 0.0, 0.0)
            if g.shock[3] > 0.004:
                shock = (g.shock[0], g.shock[1], g.shock[2], g.shock[3])
            look = inv_clamp(g.look_view, 0.0, 1.0) if chasing else 0.0
            return {
                "grade": (1.04, 1.08 + 0.10 * near, 0.62 - 0.22 * near, 0.20),
                "lift": (0.010, 0.014, 0.012),
                "gain": (1.02, 1.00, 0.96),
                "bloom": 0.55 + 0.25 * near,
                "thresh": 0.40,
                "ca": 0.0012 + 0.004 * near + 0.006 * look + g.ca,
                "grain": 0.060 + 0.030 * near,
                "vig": 0.55 + 0.25 * near,
                "vigr": 1.02,
                "barrel": 0.018 + 0.045 * look,
                "shock": shock,
                "tear": (inv_clamp(max(g.tear, g.glitch * 0.8), 0.0, 1.0),
                         float(g.tick // 2), 0.5 + 0.4 * math.sin(g.clock * 3.1),
                         0.55),
            }

        # ----- the corridor ------------------------------------------------------

        def _room(self, g, p, chasing):
            global HOR_DARK_OK
            if chasing:
                lo, hi = g.lane()
                act = 1.0
                lamp_x = g.px + 22.0
                lamp = g.lamp_lit * (0.0 if g.lamp_dead else 1.0)
                # Even with the lamp down you can see a little of the floor
                # right under you -- the fairness floor on sight lives in the
                # masses' outlines, this only keeps the room a room.
                lamp = max(lamp, 0.10 * (1.0 - g.blind))
                spd = inv_clamp((g.speed - HOR_WINDED_SPEED)
                                / (HOR_SPRINT - HOR_WINDED_SPEED), 0.0, 1.0)
                near = g.near_frac()
                wig = 26.0
                still = 0.0
                dread = 0.0
            else:
                lo, hi = HOR_A1_LANE
                act = 0.0
                lamp_x = 640.0
                lamp = g.lamp1 * (1.0 - 0.55 * g.windup) * (1.0 - g.dark)
                spd = 0.0
                near = 0.0
                wig = 10.0 + 20.0 * g.dread_frac()
                still = g.lamp1_still
                dread = g.dread_frac()
            zs = g.scroll * (HOR_Z_RATE / HOR_SCROLL_PX)
            if HOR_DARK_OK:
                try:
                    m = (Model((1280, 720))
                         .texture(inv_disp(HOR_SOUP_IMG))
                         .texture(inv_disp(inv_fx_img("tex_corridor")),
                                  texture_wrap=(_HOR_GL_REPEAT, _HOR_GL_REPEAT))
                         .shader("renpy.texture")
                         .shader("inv.dark")
                         .uniform("u_hor_res", (1280.0, 720.0))
                         .uniform("u_hor_time", g.clock)
                         .uniform("u_hor_geo", (HOR_VP[0], HOR_VP[1],
                                                HOR_PLANE_Y, HOR_CEIL_Y))
                         .uniform("u_hor_lane", (float(lo), float(hi),
                                                 HOR_Z_NEAR, float(zs)))
                         .uniform("u_hor_lamp", (float(inv_clamp(lamp, 0.0, 2.0)),
                                                 float(lamp_x), float(still), 0.0))
                         .uniform("u_hor_mood", (act, float(dread), float(spd), float(wig)))
                         .uniform("u_hor_hole", (float(g.hole[0]), float(g.hole[1]),
                                                 float(g.hole[2]), float(g.hole[3])))
                         .uniform("u_hor_near", float(near))
                         .uniform("u_hor_beat", float(g.beat_pulse))
                         .uniform("u_hor_lurch", float(g.lurch))
                         .uniform("u_hor_blind", float(g.blind))
                         .uniform("u_hor_glitch", float(g.glitch))
                         .uniform("u_hor_flash", float(g.flash))
                         .uniform("u_hor_dark", float(g.dark))
                         .uniform("u_hor_look", float(g.look_view))
                         .uniform("u_hor_vast", float(g.vast))
                         .uniform("u_hor_close", float(g.run_frac() if chasing else 0.0)))
                    r = renpy.render(m, 1280, 720, p.st, p.at)
                    p.blit(r, (0, 0))
                    return
                except Exception as e:
                    HOR_DARK_OK = False
                    try:
                        renpy.log("INV FX: corridor render failed: %r" % e)
                    except Exception:
                        pass
            p.fill(HOR_BLACK, 0, 0, 1280, 720)

        # ----- the body --------------------------------------------------------

        def _draw_body(self, g, p, cx, cy, zoom, warp=1.0, stretch=(1.0, 1.0),
                       diss=0.0, hurt=0.0, alpha=1.0, swell=1.0, reach=1.0,
                       tint=(1.0, 1.0, 1.0, 0.0), rim=(0.0, 0.0, 0.0, 0.0)):
            plate_zoom = min(zoom, HOR_PLATE_MAX_ZOOM)
            extra = zoom / plate_zoom
            plate, W, H = inv_body_plate(HOR_SPRITE, HOR_SPRITE_W, HOR_SPRITE_H,
                                        plate_zoom, pad_x=1.60, pad_y=1.55)
            cx = cx + HOR_FIG_DX * zoom
            cy = cy + HOR_FIG_DY * zoom
            zoom = float(zoom)
            body = None
            try:
                if HOR_WITHER_OK:
                    body = Transform(
                        plate, mesh=True, shader="inv.wither",
                        u_wit_res=(float(W), float(H)),
                        u_wit_t=g.clock,
                        u_wit_warp=float(warp),
                        u_wit_swell=float(swell),
                        u_wit_stretch=(float(stretch[0]), float(stretch[1])),
                        u_wit_pivot=0.90,
                        u_wit_reach=float(reach),
                        u_wit_near=float(max(g.dread_frac(), g.near_frac())),
                        u_wit_diss=float(diss),
                        u_wit_tint=tuple(float(v) for v in tint),
                        u_wit_rim=tuple(float(v) for v in rim))
                elif INV_FLESH_OK:
                    body = inv_flesh(plate, W, H, g.clock, warp=warp,
                                     stretch=stretch, pivot=0.90, hurt=hurt,
                                     diss=diss)
                if body is not None:
                    if extra > 1.01:
                        body = Transform(body, zoom=extra, subpixel=True)
                    if alpha < 0.99:
                        body = Transform(body, alpha=alpha)
                    r = renpy.render(body, int(W * extra) + 8,
                                     int(H * extra) + 8, p.st, p.at)
                    w, h = r.get_size()
                    p.sblit(r, (cx - w * 0.5, cy - h * 0.5))
                    return
            except Exception:
                pass
            r, (w, h) = p.tex(("plainbody", round(zoom, 3), alpha),
                              self._body_plain(zoom, alpha=alpha), 900, 900)
            p.sblit(r, (cx - w * 0.5, cy - h * 0.5))

        def _draw_heart(self, g, p, cx, cy, scale=1.0, diss=0.0):
            """The runner. Same SOUL heart as the other modes, warped harder
            than anything else on screen and beating out of time."""
            plate, W, H = inv_body_plate(INV_HEART, INV_HEART_W, INV_HEART_H,
                                        HOR_HEART_ZOOM * max(0.05, scale),
                                        pad_x=2.2, pad_y=2.2, nearest=True)
            squeeze = 1.0 - 0.20 * g.beat_pulse
            warp = HOR_HEART_WARP * (1.0 + 0.35 * g.near_frac())
            p.glow(cx, cy, 34 * scale, 30 * scale, col="#ff4058", alpha=0.32)
            if INV_FLESH_OK:
                try:
                    d = inv_flesh(plate, W, H, g.clock * 2.6, warp=warp,
                                split=0.9,
                                stretch=(1.0 / max(0.5, squeeze), squeeze),
                                pivot=0.5, hurt=0.0,
                                diss=inv_clamp(0.04 + 0.05 * g.near_frac()
                                            + 0.85 * diss, 0.0, 1.0))
                    r = renpy.render(d, W, H, p.st, p.at)
                    w, h = r.get_size()
                    p.sblit(r, (cx - w * 0.5, cy - h * 0.5))
                    return
                except Exception:
                    pass
            hz = HOR_HEART_ZOOM * max(0.05, scale)
            heart = self._tf(("heartplain", round(hz, 2)),
                             lambda z=hz: Transform(INV_HEART, zoom=z,
                                                    nearest=True, subpixel=True))
            r, (w, h) = p.tex(("heartplain", round(hz, 2)), heart, 160, 160)
            p.sblit(r, (cx - w * 0.5, cy - h * 0.5))

        # ----- ACT ONE ---------------------------------------------------------

        def _room_world(self, g, p, sx, sy):
            """It is standing in the corridor, as far down it as DREAD says.
            The lantern is yours; the light it throws finds it by distance."""
            arriving = (g.mode == "arrive")
            dread = inv_clamp(g.dread_shown / HOR_DREAD_MAX, 0.0, 1.0)
            persp, feet = hor_a1_place(dread)
            zoom = HOR_A1_ZOOM * persp / 0.5
            # IT REACHES / it looms: the whole of it comes at the lens.
            surge = g.lunge_k
            zoom *= 1.0 + 0.55 * surge
            feet += 70.0 * surge
            body_h = HOR_FIG_H * zoom
            # It does not bob. It breathes, from the inside (inv.wither); the
            # stillness of the outline is the tell.
            cy = feet - body_h * 0.5
            if arriving:
                cy = inv_lerp(cy, g.hole[1] + 30.0, g.emerge)
                stretch = (1.0, g.body_scale)
                warp = 0.9 + 1.1 * g.emerge
                diss = g.emerge * 0.9
            else:
                breathe = 0.0 if g.lamp1_still > 0.5 and g.last_enemy == "still" else 1.0
                stretch = (1.0 - 0.03 * math.sin(g.clock * 0.9) * breathe,
                           1.0 + 0.04 * math.sin(g.clock * 0.62) * breathe)
                warp = 0.7 + 0.9 * dread + 1.2 * surge
                diss = 0.0
            if g.blink_t > 0:
                # "behind": it is not there. It will be, nearer.
                return

            lamp = g.lamp1 * (1.0 - 0.55 * g.windup)
            lit = inv_clamp(lamp * (0.25 + 0.95 * persp), 0.0, 1.0)
            # Its shadow, thrown AWAY from the lantern -- down the corridor,
            # behind it -- long when the lamp is up, gone when it is not.
            if not arriving and lit > 0.05:
                p.shadow(640 + sx, feet + sy - 8.0 * persp, 150.0 * persp,
                         26.0 * persp + 60.0 * lit * persp, alpha=0.55 * lit)
            self._draw_body(g, p, 640 + sx, cy + sy, zoom, warp=warp,
                            stretch=stretch, diss=diss,
                            hurt=0.7 if g.hit_flash > 0.4 else 0.0,
                            swell=0.7 + 1.1 * dread + 0.8 * surge,
                            reach=0.5 + 1.1 * dread + 0.8 * surge,
                            tint=(inv_lerp(0.42, 1.10, lit), inv_lerp(0.48, 0.96, lit),
                                  inv_lerp(0.46, 0.78, lit), 1.0),
                            rim=(1.0, 0.82, 0.55, 0.9 * lit))

        def _room_hud(self, g, p, sx, sy):
            if g.mode == "arrive":
                return
            dread = g.dread_frac()
            inv_draw_panel(p, 370, 16, 540, 54, HORStage.STYLE_PLATE)
            p.text("HORROR", 15, HOR_PALE, 386, 22, bold=True, w=300, h=30,
                   outline="#020303")
            bar_w = 508
            p.fill("#2a1d20", 386, 48, bar_w, 8)
            # The bar is DREAD, not its health. Its health is not your business.
            fill = int(bar_w * inv_clamp(g.dread_shown / HOR_DREAD_MAX, 0.0, 1.0))
            if fill > 0:
                p.fill(HOR_BLOOD if dread < 0.8 else "#d3283c", 386, 48, fill, 8)
                p.fill("#ffffff30", 386, 48, fill, 1)
            inv_draw_log(p, g, 930, 20, 310,
                         {"you": (HOR_INK, HOR_PALE), "it": (HOR_BLOOD, HOR_WARN)})

            slide = int(g.panel_slide * 200)
            if g.panel_slide < 1.0:
                kick = g.panel_kick
                kx = int(math.sin(g.tick * 2.9) * 8.0 * max(0.0, kick))
                ky = int(abs(kick) * 4.0)
                self._panel(g, p, HORStage.PANEL_CMD, sx, sy + slide)
                self._panel(g, p, HORStage.PANEL_HUD, sx + kx, sy + slide + ky, hit=kick)
                self._panel_contents(g, p, sx, sy + slide, kx, ky)

        def _panel(self, g, p, box, sx, sy, hit=0.0):
            x, y, w, h = box
            inv_draw_panel(p, x + sx, y + sy, w, h, HORStage.STYLE_PANEL)
            if hit > 0.05:
                p.fill(inv_hex(HOR_BLOOD, 0.40 * hit), x + sx, y + sy, w, h)

        def _panel_contents(self, g, p, sx, sy, kx=0, ky=0):
            cx, cy, cw, ch = HORStage.PANEL_CMD
            cx += sx
            cy += sy

            if g.mode == "menu":
                for i, row in enumerate(HOR_CMDS):
                    live = (i == g.cursor)
                    ry = cy + 18 + i * 30
                    if live:
                        p.fill(HOR_PALE + "1a", cx + 14, ry - 4, cw - 28, 27)
                        col = HOR_BLOOD if g.panic else HOR_PALE
                        p.fill(col, cx + 14, ry - 4, 3, 27)
                        p.fill(col, cx + 26, ry + 5, 8, 8)
                    p.text(row[1], 20, HOR_INK if live else HOR_FAINT,
                           cx + 46, ry, bold=live, w=260, h=30, outline="#020303")
                    if row[0] == "light":
                        p.text(str(HOR_LIGHT_NERVE), 14,
                               HOR_PALE if live else HOR_FAINT,
                               cx + cw - 22, ry + 4, anchor=(1.0, 0.0), w=120, h=26)
                p.text("Z  OK      ESC  PAUSE", 12, HOR_FAINT,
                       cx + cw - 16, cy + ch - 22, anchor=(1.0, 0.0), w=420, h=24)

            elif g.mode == "beat":
                u = inv_clamp(g.mtick / 6.0, 0.0, 1.0)
                p.text(g.beat_label, 22, HOR_INK, cx + 22, cy + 28, bold=True,
                       w=cw - 40, h=40, outline="#020303")
                if g.beat_value:
                    p.text(g.beat_value, int(24 + 6 * u), HOR_WARN, cx + 22, cy + 62,
                           bold=True, w=cw - 40, h=48, outline="#020303")
                hold = inv_clamp(g.mtick / float(INV_BEAT_HOLD), 0.0, 1.0)
                p.fill(HOR_FAINT + "60", cx + 22, cy + ch - 18, cw - 44, 2)
                p.fill(HOR_PALE, cx + 22, cy + ch - 18, int((cw - 44) * hold), 2)

            elif g.mode == "enemy":
                u = inv_clamp(g.mtick / 26.0, 0.0, 1.0)
                p.text("IT", 18, HOR_BLOOD, cx + 22, cy + 30, bold=True,
                       w=cw - 40, h=34, outline="#020303")
                p.fill(HOR_BLOOD + "50", cx + 22, cy + 70, cw - 44, 2)
                p.fill(HOR_BLOOD, cx + 22, cy + 70, int((cw - 44) * u), 2)

            hx, hy, hw, hh = HORStage.PANEL_HUD
            hx += sx + kx
            hy += sy + ky
            p.text(inv_player_name(), 19, HOR_INK, hx + 22, hy + 12,
                   bold=True, w=hw - 40, h=32, outline="#020303")
            self._odometer(g, p, "HP", g.hp_shown, g.hp, hx + 22, hy + 44, HOR_INK)
            self._odometer(g, p, "NV", g.nerve_shown, g.nerve, hx + 22, hy + 96,
                           HOR_PALE, small=True)
            if g.panic:
                a = 0.6 + 0.4 * math.sin(g.clock * 9.0)
                p.text("PANIC", 13, inv_hex(HOR_BLOOD, a), hx + hw - 22, hy + 16,
                       anchor=(1.0, 0.0), w=200, h=26, bold=True)
            if g.god:
                p.text("GOD", 12, HOR_WARN + "aa", hx + hw - 22,
                       hy + hh - 24, anchor=(1.0, 0.0), w=120, h=24)

        def _odometer(self, g, p, label, shown, real, x, y, color, small=False):
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
                p.fill("#07090880", dx, y, cell_w - 4, cell_h)
                if rolling:
                    off = int(frac * cell_h * (1 if real < shown else -1))
                    nxt = str((int(ch) + (1 if real > shown else -1)) % 10)
                    p.text(nxt, size, inv_hex(color, 0.45), dx + (cell_w - 4) // 2,
                           y + off - (cell_h if real < shown else -cell_h) + 2,
                           anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)
                    p.text(ch, size, color, dx + (cell_w - 4) // 2,
                           y + off + 2, anchor=(0.5, 0.0), w=cell_w,
                           h=cell_h, bold=True)
                else:
                    p.text(ch, size, color, dx + (cell_w - 4) // 2, y + 2,
                           anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)

        # ----- ACT TWO: THE CHASE ----------------------------------------------

        def _chase_world(self, g, p, sx, sy):
            near = g.near_frac()
            lookv = inv_clamp(g.look_view, 0.0, 1.0)
            lo, hi = g.lane()

            # HOW MUCH YOU ARE ALLOWED TO SEE: a depth window, closing as it
            # gets nearer -- but FLOORED at however far the corridor travels in
            # HOR_MIN_WARN ticks, so sprinting widens your eyes instead of
            # outrunning them (fairness rule 1).
            dz_tick = max(g.speed, HOR_WALK) * HOR_Z_RATE
            sight_z = max(inv_lerp(0.62, 0.26, near) * (1.0 - 0.55 * g.blind)
                          * inv_lerp(1.0, HOR_RESOLVE_SIGHT, g.resolved())
                          * inv_lerp(1.0, HOR_LAMP_SIGHT, g.lamp_lit)
                          * (HOR_LAMP_DEAD_SIGHT if g.lamp_dead else 1.0),
                          dz_tick * HOR_MIN_WARN)

            rush = inv_clamp((g.speed - HOR_WINDED_SPEED)
                             / (HOR_SPRINT - HOR_WINDED_SPEED), 0.0, 1.0)

            # SPEED: streaks off the vanishing point, their length and weight
            # set by how fast you are actually going.
            for k in range(22):
                seed = (k * 2654435761) % 1000 / 1000.0
                ang = seed * 6.2831853 + math.sin(g.clock * 0.13 + k) * 0.05
                phase = (g.scroll * (0.0016 + 0.0011 * seed) + seed) % 1.0
                z0 = 1.0 - phase
                if z0 < 0.06:
                    continue
                p0, _ = hor_project(z0)
                p1, _ = hor_project(max(0.05, z0 - 0.10 - 0.16 * rush))
                r0 = 70.0 * p0 * (1.0 + 5.0 * seed)
                r1 = 70.0 * p1 * (1.0 + 5.0 * seed)
                if r1 < r0:
                    continue
                a_st = (0.10 + 0.40 * rush) * inv_clamp(p0 * 2.4, 0.0, 1.0)
                p.line(HOR_VP[0] + math.cos(ang) * r0 + sx,
                       HOR_VP[1] + math.sin(ang) * r0 + sy,
                       HOR_VP[0] + math.cos(ang) * r1 + sx,
                       HOR_VP[1] + math.sin(ang) * r1 + sy,
                       width=1.0 + 1.6 * rush, col="#b0beb6", alpha=a_st, add=True)

            # THINGS IN THE WALLS THAT ARE NOT MASSES. Pairs of points, mostly
            # shut, that open for a moment as they go past. No mechanics and
            # no tell -- they are not the watchers and never become them,
            # which is exactly why the watchers work.
            phase0 = g.scroll * HOR_STRUCT_PHASE
            for k in range(HOR_WALL_EYES):
                seed = ((k * 3266489917) % 1009) / 1009.0
                ph = (phase0 * (0.90 + 0.2 * seed) + seed * 0.77) % 1.0
                z = HOR_Z_FAR - ph * (HOR_Z_FAR - 0.10)
                if z <= 0.08:
                    continue
                open_u = math.sin(g.clock * (0.5 + 0.4 * seed) + seed * 9.0)
                if open_u < 0.72:
                    continue
                persp, _fy = hor_project(z)
                side = k % 2
                ex = hor_screen_x(lo if side == 0 else hi, persp) + sx
                ey = hor_screen_y(inv_lerp(HOR_CEIL_Y + 60.0, HOR_PLANE_Y - 90.0, seed),
                                  persp) + sy
                a = ((0.34 + 0.40 * g.lamp_lit) * inv_clamp(persp * 2.4, 0.0, 1.0)
                     * ((open_u - 0.72) / 0.28))
                dx_e = max(2.0, 16.0 * persp)
                for ox_ in ((-dx_e, 0.0) if side == 1 else (0.0, dx_e)):
                    p.quad("core", ex + ox_, ey, 0.10 + 0.20 * persp, col="#d8e4da",
                           alpha=a, add=True)

            # --- obstacles: masses standing on the floor ----------------------
            for o in sorted(g.obstacles, key=lambda e: -e["z"]):
                persp, oy = hor_project(o["z"])
                ox = hor_screen_x(o["x"], persp)
                a = inv_clamp(1.0 - (o["z"] - HOR_Z_NEAR) / max(0.05, sight_z),
                              0.0, 1.0)
                w = max(4.0, o["w"] * persp)
                h = max(3.0, o["h"] * persp * 1.35)
                x0 = ox - w * 0.5 + sx
                yb = oy + sy
                # The mass itself: dark, organic, lit along its top by the
                # lantern the nearer it comes. Hidden by the dark the further
                # away it is -- but see the outline below.
                # The dark hides what is IN it, never that it is there: the
                # silhouette keeps a floor, the detail needs the lamp.
                am = max(a, 0.30 * inv_clamp(persp * 2.0, 0.0, 1.0)) * (1.0 - 0.85 * lookv)
                lit = inv_clamp(g.lamp_lit * (0.2 + 0.9 * persp), 0.0, 1.0)
                lit = int(lit * 8.0 + 0.5) / 8.0
                if am > 0.02:
                    tex = INV_MASSES[int(o["seed"] * 997) % len(INV_MASSES)]
                    tw, th = inv_fx_size(tex)
                    col = "#%02x%02x%02x" % (int(inv_lerp(70, 160, lit)),
                                             int(inv_lerp(66, 132, lit)),
                                             int(inv_lerp(68, 112, lit)))
                    p.quad(tex, ox + sx, yb - h * 0.5, w / tw, h / th, col=col,
                           alpha=min(1.0, am * 1.15), add=False, zq=48.0)
                    if o.get("reach") is not None:
                        wall_x = hor_screen_x(lo if o["reach"] == 0 else hi, persp) + sx
                        if o["reach"] == 0:
                            p.fill(inv_hex("#050606", 0.85 * am), wall_x, yb - h * 0.85,
                                   max(1, x0 - wall_x + 4), h * 0.85)
                        else:
                            p.fill(inv_hex("#050606", 0.85 * am), x0 + w - 4, yb - h * 0.85,
                                   max(1, wall_x - (x0 + w) + 4), h * 0.85)
                # THE EDGE IS ALWAYS LEGIBLE (fairness rule 2): the exact width
                # it occupies at your row, drawn as two pale uprights and a
                # base line at an alpha that never drops below the floor --
                # applied to the FINAL value, never multiplied into it.
                edge_a = (max(HOR_EDGE_FLOOR, a) * (1.0 - 0.55 * g.blind)
                          * (1.0 - 0.42 * lookv))
                ec = inv_hex(HOR_PALE, edge_a)
                et = max(2, int(2.5 * persp + 1))
                # The footprint, full width, where it meets the boards -- that
                # is the hitbox -- and its two edges carried up a third of the
                # way, so it reads as a THING with a width, not a box.
                p.fill(ec, x0, yb - et, w, et)
                p.fill(ec, x0, yb - h * 0.34, et, h * 0.34)
                p.fill(ec, x0 + w - et, yb - h * 0.34, et, h * 0.34)
                p.glow(ox + sx, yb, w * 0.62, 10.0 * persp + 3.0, col=HOR_PALE,
                       alpha=0.18 * edge_a)

            # --- THE WATCHER --------------------------------------------------
            wch = g.watcher
            if wch is not None:
                persp, wy = hor_project(wch["z"])
                wx = hor_screen_x(lo if wch["side"] == 0 else hi, persp)
                wx += (26.0 if wch["side"] == 0 else -26.0) * persp
                stage_u = wch["stage"] / float(HOR_WATCH_STAGES - 1)
                pushing = g.lit() and g.watch_side_ok()
                jolt = wch["moved"] / 12.0
                bz = inv_clamp(0.62 * persp, 0.02, 0.62)
                bcy = wy - 96.0 * persp
                lit = inv_clamp(g.lamp_lit * (0.3 + 0.8 * persp)
                                * (1.0 if g.watch_side_ok() else 0.35), 0.0, 1.0)
                self._draw_body(g, p, wx + sx, bcy + sy, bz,
                                warp=0.35 + 1.9 * jolt,
                                stretch=(1.0 + 0.20 * jolt, 1.0 - 0.14 * jolt),
                                diss=0.0,
                                alpha=inv_clamp(0.30 + 0.62 * stage_u, 0.0, 1.0),
                                swell=0.2 + 1.4 * jolt,
                                reach=0.5 + 1.1 * stage_u,
                                tint=(inv_lerp(0.40, 1.05, lit), inv_lerp(0.44, 0.92, lit),
                                      inv_lerp(0.42, 0.76, lit), 1.0),
                                rim=(1.0, 0.82, 0.55, 0.8 * lit))
                # ITS EYES: the only part of it that is bright, and they go
                # out while the light is on it.
                eye_a = (0.30 + 0.60 * stage_u) * (1.0 - 0.75 * wch["seen"])
                egap = max(4.0, 132.0 * bz)
                eye_y = bcy - 470.0 * bz + sy
                for side_dx in (-egap * 0.5, egap * 0.5):
                    p.quad("core", wx + side_dx + sx, eye_y, 0.10 + 0.5 * bz,
                           col=(HOR_PALE if not pushing else HOR_WARN), alpha=eye_a,
                           add=True)
                # THE ACCUMULATOR, on the wall beside it, reading BOTH WAYS off
                # a centre line -- the whole tutorial for the directional rule.
                pw = inv_clamp(wch["p"], -1.0, 1.0)
                bh = max(22, int(320.0 * bz))
                half = bh // 2
                bx_ = int(hor_screen_x(lo if wch["side"] == 0 else hi, persp)) \
                    + (4 if wch["side"] == 0 else -8) + sx
                by_ = int(bcy - 470.0 * bz - bh * 0.5) + sy
                p.fill("#05070699", bx_, by_, 4, bh)
                p.fill(inv_hex(HOR_FAINT, 0.60), bx_ - 2, by_ + half, 8, 1)
                fill = max(1, int(half * abs(pw)))
                if pw >= 0.0:
                    p.fill(inv_hex(HOR_BLOOD, 0.40 + 0.50 * stage_u), bx_,
                           by_ + half - fill, 4, fill)
                else:
                    p.fill(inv_hex(HOR_PALE, 0.75), bx_, by_ + half, 4, fill)

                # WHERE TO STAND, on the boards: the half of the corridor it can
                # be answered from, headed with act one's own word while it has
                # never yet been driven back.
                zlo = lo if wch["side"] == 0 else (lo + hi) * 0.5
                zhi = (lo + hi) * 0.5 if wch["side"] == 0 else hi
                inside = zlo <= g.px <= zhi
                need = (0.0 if (inside and g.lit()) else 1.0)
                zp = 0.5 + 0.5 * math.sin(g.tick * 0.13)
                za = 0.14 + (0.34 + 0.22 * zp) * need
                zy = int(HOR_PLANE_Y) + 62 + sy
                zx0 = int(zlo) + sx
                zw = max(6, int(zhi - zlo))
                for seg in range(0, zw, 26):
                    p.fill(inv_hex(HOR_PALE, za), zx0 + seg, zy, min(14, zw - seg), 2)
                p.fill(inv_hex(HOR_PALE, za), zx0, zy - 13, 2, 15)
                p.fill(inv_hex(HOR_PALE, za), zx0 + zw - 2, zy - 13, 2, 15)
                if not g.watch_taught:
                    p.text("LIGHT", 13, inv_hex(HOR_WARN, 0.30 + 0.60 * need),
                           zx0 + zw // 2, zy + 16, bold=True, anchor=(0.5, 0.0),
                           w=200, h=26)

            # --- the thing that is ahead of you --------------------------------
            if g.phantom is not None:
                ph_ = g.phantom
                pp, pyy = hor_project(ph_["z"])
                a = 0.55 * inv_clamp(ph_["life"] / 90.0, 0.0, 1.0)
                self._draw_body(g, p, hor_screen_x(ph_["x"], pp) + sx, pyy + sy,
                                inv_clamp(0.34 * pp, 0.03, 0.50),
                                warp=2.4, stretch=(1.0, 1.25), diss=0.35, alpha=a,
                                swell=1.6, reach=1.8,
                                tint=(0.55, 0.62, 0.66, 1.0),
                                rim=(0.6, 0.8, 0.9, 0.6))

            # --- the runner -----------------------------------------------------
            for i, (tx, ty, sprinting) in enumerate(g.trail):
                if i == 0:
                    continue
                a = 0.30 * (1.0 - i / float(len(g.trail)))
                if sprinting:
                    a *= 1.7
                p.quad("core", tx + sx, ty + sy, 0.34 - i * 0.022, col="#ff4a5e",
                       alpha=a * (1.0 - 0.7 * lookv), add=True)
            leaving = g.mode in ("leave_w", "leave_l")
            if leaving:
                self._draw_heart(g, p, g.heart_x + sx, g.heart_y + sy,
                                 scale=g.heart_scale, diss=g.heart_diss)
            elif not (g.stumble > 0 and (g.tick // 3) % 2 == 0):
                self._draw_heart(g, p, g.px + sx, g.py + sy)
            # The lamp itself, held out to one side, and the warm circle it
            # throws on the boards under you.
            if g.lamp_lit > 0.02 and not leaving:
                flick = 0.86 + 0.14 * math.sin(g.clock * 21.0) * math.sin(g.clock * 7.3)
                lx, ly = g.px + 22.0 + sx, g.py - 16.0 + sy
                p.glow(g.px + sx, g.py + 22.0 + sy, 120.0, 30.0, col="#ffcf8a",
                       alpha=0.32 * g.lamp_lit * flick)
                p.quad("core", lx, ly, 0.26, col="#fff0c8", alpha=0.9 * g.lamp_lit * flick,
                       add=True)
                p.glow(lx, ly, 40.0, 40.0, col="#ffb35a", alpha=0.45 * g.lamp_lit * flick)

            # --- IT ----------------------------------------------------------------
            # Rising out of the bottom of the frame. At full distance only the
            # top of its head is in the world at all; on your heels it owns a
            # third of the screen.
            red = 0.30 + 0.50 * near
            self._draw_body(g, p, g.follow_x + sx, g.follow_y + sy, g.follow_zoom,
                            warp=(g.exit_warp if leaving else 1.6 + 1.6 * near),
                            stretch=(1.0 + 0.10 * math.sin(g.clock * 1.7),
                                     1.0 + 0.16 * math.sin(g.clock * 1.1)),
                            diss=0.0,
                            alpha=g.follow_alpha * (1.0 - lookv),
                            swell=(1.9 if leaving else 0.6 + 1.3 * near),
                            reach=(1.9 if leaving else 0.4 + 1.4 * near),
                            tint=(0.55 + 0.35 * red, 0.48, 0.48, 1.0),
                            rim=(1.0, 0.82, 0.55, 0.65 * g.lamp_lit))

            if lookv > 0.01:
                self._render_stare(g, p, lookv, sx, sy)

            # THE BITE. A held frame with it filling the corridor, and then the
            # run simply goes on. A shock, not a gag: nothing zooms, nothing
            # squeals, it is suddenly all there is and then it is not.
            if g.bite_t > 0:
                bu = g.bite_t / float(HOR_BITE_FREEZE)
                p.fill(inv_hex("#000000", 0.55 * bu), 0, 0, 1280, 720)
                self._draw_body(g, p, 640 + sx, 470 + sy, 1.10 + 0.10 * (1.0 - bu),
                                warp=2.6, stretch=(1.06, 0.97), diss=0.0,
                                alpha=inv_clamp(bu * 1.6, 0.0, 1.0),
                                swell=2.2, reach=2.2,
                                tint=(0.70, 0.60, 0.58, 1.0))
                p.fill(inv_hex(HOR_BLOOD, 0.22 * bu), 0, 0, 1280, 720)

            if g.lunge_state == "warn":
                puls = 0.5 + 0.5 * math.sin(g.tick * 0.5)
                p.fill(inv_hex(HOR_BLOOD, 0.08 + 0.18 * puls), 0, 0, 1280, 720)

        def _render_stare(self, g, p, lookv, sx, sy):
            """You turned round. The camera comes about, the corridor reverses
            in the shader, and it is simply there, in the middle of the frame,
            with nothing in the way. NEAR is the payment, LOOK_FRAC the risk."""
            near = g.near_frac()
            lf = g.look_frac()
            swing = 1.0 - abs(lookv - 0.5) * 2.0
            if swing > 0.02 and lookv < 0.995:
                for k in range(9):
                    yy = (g.tick * 23 + k * 149) % 720
                    hh = 3 + (k * 7) % 12
                    p.fill(inv_hex(HOR_PALE, 0.10 * swing), int(math.sin(k * 1.7) * 120 * swing),
                           yy, 1280, hh)
            p.fill(inv_hex("#000000", 0.62 * lookv), 0, 0, 1280, 720)
            zoom = inv_lerp(0.30, 1.05, near) * (1.0 + 0.32 * lf)
            cy = inv_lerp(292.0, 452.0, near) + 26.0 * lf
            self._draw_body(g, p, 640 + sx, cy + sy, zoom,
                            warp=1.5 + 1.9 * near + 1.7 * lf,
                            stretch=(1.0 + 0.07 * math.sin(g.clock * 2.1),
                                     1.0 + 0.11 * math.sin(g.clock * 1.3)),
                            diss=0.0, alpha=lookv,
                            swell=0.9 + 1.5 * near + 1.1 * lf,
                            reach=0.8 + 1.4 * near + 1.4 * lf,
                            tint=(0.62 + 0.3 * near, 0.50, 0.50, 1.0))
            # IT IS GETTING WORSE THE LONGER YOU DO THIS: rings closing on the
            # middle, then the picture starting to come apart.
            if lf > 0.25:
                puls = 0.5 + 0.5 * math.sin(g.tick * (0.22 + 0.5 * lf))
                rings = 3 + int(4 * lf)
                for k in range(rings):
                    rr = 120 + k * 46 - int(70.0 * lf * puls)
                    if rr < 8:
                        continue
                    a = 0.10 + 0.24 * lf * (1.0 - k / float(rings))
                    p.ring(640 + sx, 400 + sy, rr, rr, col=HOR_BLOOD, alpha=a,
                           add=True)
            if lf > 0.55:
                tear = (lf - 0.55) / 0.45
                p.fill(inv_hex(HOR_BLOOD, 0.05 + 0.20 * tear), 0, 0, 1280, 720)

        def _chase_hud(self, g, p, sx, sy):
            if g.hud_fade <= 0.02:
                return
            lookv = inv_clamp(g.look_view, 0.0, 1.0)
            prog = inv_clamp(g.dist / HOR_GOAL, 0.0, 1.0)
            bw = 620
            bx0 = 640 - bw // 2
            inv_draw_panel(p, bx0 - 12, 14, bw + 24, 26, HORStage.STYLE_PLATE)
            p.fill("#1c2422", bx0, 24, bw, 6)
            p.fill(HOR_PALE, bx0, 24, int(bw * prog), 6)
            for k, at in enumerate(HOR_PHASE_AT[1:]):
                p.fill(inv_hex(HOR_PALE, 0.35 if prog < at else 0.15),
                       bx0 + int(bw * at), 20, 1, 14)

            plate = (24, 628, 300, 72)
            inv_draw_panel(p, plate[0], plate[1], plate[2], plate[3], HORStage.STYLE_PANEL)
            sw = 220
            # THE TANK. It only ever goes one way.
            p.fill("#241c1e", 38, 646, sw, 6)
            if g.lamp_dead:
                puls = 0.5 + 0.5 * math.sin(g.tick * 0.35)
                p.fill(inv_hex(HOR_BLOOD, 0.16 + 0.20 * puls), 38, 646, sw, 6)
            else:
                pf = g.power_frac()
                lamp_col = (HOR_WARN if g.lamp_lit > 0.5
                            else (HOR_PALE if pf > 0.25 else HOR_WARN))
                p.fill(lamp_col, 38, 646, int(sw * pf), 6)
            p.text("LAMP", 11, HOR_FAINT, 266, 641, w=160, h=22)
            # WIND.
            p.fill("#241c1e", 38, 668, sw, 6)
            if g.winded > 0:
                puls = 0.5 + 0.5 * math.sin(g.tick * 0.5)
                p.fill(inv_hex(HOR_BLOOD, 0.45 + 0.55 * puls), 38, 668,
                       int(sw * (1.0 - g.winded / float(HOR_WINDED_TICKS))), 6)
            else:
                stam_col = HOR_PALE if g.stam > HOR_STAM_RELEASE_HINT else HOR_WARN
                p.fill(stam_col, 38, 668, int(sw * (g.stam / HOR_STAM_MAX)), 6)
                p.fill(HOR_FAINT, 38 + int(sw * (HOR_STAM_RELEASE_HINT / HOR_STAM_MAX)),
                       665, 2, 12)
            p.text("WIND", 11, HOR_FAINT, 266, 663, w=160, h=22)
            # WHAT THE STARE LEFT BEHIND.
            if g.resolve_t > 0.0:
                p.fill("#1c2422", 38, 686, sw, 4)
                p.fill(HOR_INK, 38, 686, int(sw * g.resolved()), 4)
                p.text("RESOLVE", 10, HOR_PALE, 266, 681, w=180, h=22)

            # HOW LONG YOU HAVE BEEN LOOKING -- mandatory, not decoration: a
            # stare that can take you must be one you can see ending.
            if lookv > 0.01 or g.look_lock > 0:
                lw = 300
                lx = 640 - lw // 2
                lf = g.look_frac()
                p.fill("#02030390", lx - 2, 646, lw + 4, 12)
                p.fill("#241c1e", lx, 648, lw, 8)
                if g.look_lock > 0:
                    puls = 0.5 + 0.5 * math.sin(g.tick * 0.5)
                    p.fill(inv_hex(HOR_BLOOD, 0.30 + 0.45 * puls), lx, 648,
                           int(lw * (1.0 - g.look_lock / float(HOR_LOOK_LOCK))), 8)
                else:
                    col = HOR_PALE if lf < 0.62 else (HOR_WARN if lf < 0.85 else HOR_BLOOD)
                    p.fill(col, lx, 648, int(lw * lf), 8)
                    p.fill(HOR_FAINT, lx + int(lw * (HOR_LOOK_MIN / float(HOR_LOOK_MAX))),
                           645, 2, 14)
                p.text("%d" % int(g.gap), 30, HOR_INK, 640, 620, bold=True,
                       anchor=(0.5, 0.5), w=200, h=48, outline="#020303")

            if g.scramble > 0 and (g.tick // 6) % 2 == 0:
                p.text("?", 40, HOR_BLOOD, g.px + sx, g.py - 54 + sy, bold=True,
                       anchor=(0.5, 0.5), w=80, h=60)

            lamp_hot = (g.watcher is not None and not g.watch_taught)
            lw2, _lh2 = p.text("X  SPRINT      Z  LOOK BACK   (ALL HOLD)", 12, HOR_FAINT,
                               1256, 690, anchor=(1.0, 1.0), w=520, h=28,
                               outline="#020303")
            p.text("A D  MOVE      W  LANTERN", 12,
                   (inv_hex(HOR_WARN, 0.55 + 0.40 * (0.5 + 0.5 * math.sin(g.tick * 0.13)))
                    if lamp_hot else HOR_FAINT),
                   1256 - lw2 - 22, 690, anchor=(1.0, 1.0), w=340, h=28,
                   outline="#020303")
            if g.god:
                p.text("GOD", 12, HOR_WARN + "aa", 1256, 664, anchor=(1.0, 1.0),
                       w=120, h=24)

        # ----- numbers and pause -----------------------------------------------

        def _floats(self, g, p, sx, sy):
            for f in g.floats:
                a = inv_clamp(f["life"] / 26.0, 0.0, 1.0)
                age = 52 - f["life"]
                pop = 1.0 + 0.30 * inv_clamp(1.0 - age / 6.0, 0.0, 1.0)
                p.text(f["text"], int((30 if f["big"] else 21) * pop),
                       inv_hex(f["color"], a), int(f["x"]) + sx, int(f["y"]) + sy,
                       bold=f["big"], anchor=(0.5, 0.5), w=260, h=70,
                       outline="#020303")

        def _pause(self, g, p):
            p.fill("#020303c8", 0, 0, 1280, 720)
            inv_draw_panel(p, 440, 270, 400, 150, HORStage.STYLE_PANEL)
            p.text("PAUSED", 40, HOR_INK, 640, 322, bold=True,
                   anchor=(0.5, 0.5), w=600, h=70)
            p.text("ESC  RESUME        Q  QUIT", 16, HOR_DIM,
                   640, 378, anchor=(0.5, 0.5), w=800, h=44)
# --- THE SCREEN --------------------------------------------------------------
screen inv_horror_screen(game):
    modal True
    use enter_m_input_lock()

    add Solid("#020303")
    add HORStage(game)

    key "K_ESCAPE" action Function(game.toggle_pause)
    key "mouseup_3" action Function(game.toggle_pause)
    if game.paused:
        key "K_q" action Function(game.give_up)

    if config.developer:
        key "K_g" action Function(game.toggle_god)

    timer 0.25 repeat True action Function(inv_poll_result, game, _update_screens=False)


# --- WRAPPER -----------------------------------------------------------------
default hor_game = None
default hor_deaths = 0
default hor_retry = False
# A RETRY FROM THE TEAR, carrying the dread act one handed the chase.
default hor_resume = None

label archivist_invasion_horror:
    $ hor_deaths = 0
    $ hor_retry = False
    $ hor_resume = None

label inv_horror_fight:
    $ renpy.block_rollback()

    $ hor_game = HORGame(retry=hor_retry, deaths=hor_deaths,
                        debug=config.developer, start_open=inv_dev_start_open,
                        resume=hor_resume)
    $ hor_resume = None

    $ _hor_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ _hor_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None
    scene black

    call screen inv_horror_screen(hor_game)
    $ _hor_result = _return
    $ _hor_checkpoint = hor_game.checkpoint

    $ hor_game = None
    $ quick_menu = _hor_prev_quick_menu
    $ _game_menu_screen = _hor_prev_game_menu
    $ inv_music_stop(1.0)
    $ inv_heart_stop(0.6)
    $ inv_stop_sfx(0.2)
    scene black

    if _hor_result == "victory":
        $ inv_record_result("horror", True)
        jump inv_horror_victory
    elif _hor_result == "quit":
        jump inv_horror_quit

    $ inv_record_result("horror", False)
    jump inv_horror_defeat

label inv_horror_victory:
    if inv_dev_test:
        $ renpy.notify("HORROR outrun.")
        return
    # STORY PLACEMENT: DRAWING BOARD.
    return

label inv_horror_defeat:
    $ hor_deaths += 1
    $ hor_retry = True

    call screen inv_retry_screen("HORROR", "CAUGHT",
                                 inv_retry_options(_hor_checkpoint),
                                 ink=HOR_INK, dim=HOR_DIM, accent=HOR_BLOOD,
                                 bg=HOR_BLACK)
    if _return == "tear":
        $ hor_resume = _hor_checkpoint
        scene black
        jump inv_horror_fight
    elif _return == "start":
        scene black
        jump inv_horror_fight
    if inv_dev_test:
        $ renpy.notify("HORROR: lost. Recorded.")
    return

label inv_horror_quit:
    $ hor_retry = True
    if inv_dev_test:
        $ renpy.notify("HORROR: withdrawn.")
    return
