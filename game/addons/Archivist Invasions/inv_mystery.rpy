# Mystery invasion: narrow the FIELD in act one, then find the subject in a
# lineup in the dark. The field cannot reach one; the readings still open at
# the tear walk into act two as suspects, each under its own frame and glyph.
# MYGame owns simulation state; MYStage advances it at 60Hz and draws through
# the shared kit (inv_kit.rpy: InvPaint, InvFX, the lens). inv.lamp draws the
# room in both acts; inv.lacuna draws the body. Shared systems: invasions.rpy.
#
# ACT TWO'S RULES (rebuilt Oct 2 2026 -- the old rings-and-belief-field act was
# too loose to read as a deduction): a BELL on a visible countdown reports
# whether the subject's FEET are inside your lamp's drawn rim, and every open
# suspect whose own state does not match is crossed off. Never below two: at
# two it says TWO REMAIN, and a verdict that would leave one is withheld.
# Dread (heartbeat, lamp flicker, closing frame) is the last split's channel
# and the only damage warning. ACCUSE (hold Z) on the subject SOLVES and
# reopens the case; on a bystander it RULES OUT and costs time. Every few
# strokes the bell reopens instead of answering, and its arc runs red first.
# The honesty contract (no subject crossed, no false verdict, never below two)
# is counted in MYGame.audit.
# Coordinates use 1280x720 screen pixels; speeds and timers use 60Hz ticks.
init -9 python:
    MY_LAMP_OK = False
    MY_LACUNA_OK = False

    def _my_register_lamp():
        # THE ROOM, BOTH ACTS (rebuilt Oct 2 2026).
        #
        # NAMED inv.lamp AND NOT inv.dark: Horror owns "inv.dark", and
        # register_shader silently REPLACES a taken name (the later file wins)
        # -- which once crashed Horror on its own room draw. Check the list in
        # invasions.rpy before adding a shader to any invasion.
        #
        # ACT ONE (u_my_open 0) is an interrogation room seen from the front:
        # a wall, a floor, and ONE LAMP hanging on a cord, swinging slowly.
        # Its cone comes down through the dust and puts a pool on the boards;
        # everything outside the pool is the room seen badly -- the substrate,
        # cold and underlit, resolving only where the light is. The old
        # drifting "pool of focus" is that lamp now, a physical one.
        #
        # ACT TWO (u_my_open 1) puts every light out and looks straight down.
        # What is left: the floor, almost black; YOUR lamp, one pool around
        # u_my_lamp that resolves the substrate where it falls; the BELL, a
        # ring of light that runs out from the edge of your pool when the
        # verdict lands; the bell's countdown, drawn on that same edge; and
        # the frame closing in with dread (the fairness channel -- it must
        # never be subtle). The suspects are drawn from Python, standing on
        # this floor.
        renpy.register_shader("inv.lamp", variables="""
            uniform sampler2D tex0;
            uniform sampler2D tex1;
            uniform vec2 u_my_res;
            uniform float u_my_time;
            uniform float u_my_open;
            uniform float u_my_dark;
            uniform float u_my_flash;
            uniform float u_my_dread;
            uniform float u_my_reopen;
            uniform float u_my_heat;
            uniform vec4 u_my_hole;
            uniform vec4 u_my_lamp;
            uniform vec4 u_my_hang;
            uniform vec4 u_my_bell;
            uniform vec4 u_my_count;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float my_hash(vec2 p) {
                return fract(sin(dot(p, vec2(23.71, 141.29))) * 31771.913);
            }
            vec2 my_mirror(vec2 p) {
                return abs(fract(p * 0.5) * 2.0 - 1.0);
            }
            float my_lum(sampler2D tx, vec2 q) {
                return dot(texture2D(tx, my_mirror(q)).rgb, vec3(0.299, 0.587, 0.114));
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            vec2 res = max(u_my_res, vec2(1.0));
            vec2 px = uv * res;
            float t = u_my_time;
            float open = clamp(u_my_open, 0.0, 1.0);
            float dread = clamp(u_my_dread, 0.0, 1.0);
            float heat = clamp(u_my_heat, 0.0, 1.0);
            float reop = clamp(u_my_reopen, 0.0, 1.0);

            vec2 c = uv - 0.5;

            // The rupture: a hole the LIGHT falls into.
            vec2 hp = (u_my_hole.xy / res) - 0.5;
            float hr = max(u_my_hole.z, 1.0) / res.x;
            float hs = clamp(u_my_hole.w, 0.0, 1.0);
            vec2 hv = c - hp;
            float hd = length(hv);
            float hinf = (1.0 - smoothstep(0.0, hr, hd)) * hs;
            if (hinf > 0.001) {
                float ha = hinf * hinf * 3.1;
                hv = vec2(hv.x * cos(ha) - hv.y * sin(ha), hv.x * sin(ha) + hv.y * cos(ha));
                c = hp + hv * (1.0 - 0.66 * hinf);
            }

            // --- ACT ONE: the room, the cord, the cone, the pool ---------------
            vec3 room1 = vec3(0.0);
            if (open < 0.999) {
                float hz = 372.0;
                vec2 bulb = u_my_hang.xy;
                vec2 sp1 = c + vec2(sin(t * 0.13), cos(t * 0.11)) * 0.010;
                vec2 q1 = floor((sp1 + 0.5) * 560.0) / 560.0;
                float lumw = my_lum(tex0, q1);
                vec3 wall = mix(vec3(0.040, 0.050, 0.068), vec3(0.32, 0.38, 0.46), lumw);
                // The wall, lit by the bulb with distance.
                float bd = distance(px, bulb);
                float wlight = 1.0 / (1.0 + bd * bd / (260.0 * 260.0));
                vec3 colw = wall * (0.20 + 0.85 * wlight);
                // The floor: BOARDS (tex1), in perspective below the horizon
                // -- the same boards act two looks down on. Depth from the
                // row, width from depth, one tile a unit; the substrate is
                // what they are resolved through.
                float fz = max(px.y - hz, 1.0);
                float wz = 330.0 / fz;
                float wx = (px.x - 640.0) / fz;
                float bl = dot(texture2D(tex1, vec2(wx, wz) + vec2(0.37, 0.11)).rgb, vec3(0.3333));
                vec2 fuv = vec2(wx * 0.36, wz * 0.21);
                float lumf = my_lum(tex0, floor(fuv * 220.0) / 220.0);
                float fl = clamp(bl * 1.25 * (0.80 + 0.40 * lumf), 0.0, 1.3);
                vec3 floorc = mix(vec3(0.026, 0.031, 0.042), vec3(0.30, 0.31, 0.34), fl);
                // The pool: an ellipse on the boards under the cone.
                vec2 pool = vec2(u_my_hang.z, 528.0);
                vec2 pd = (px - pool) / vec2(250.0, 66.0);
                float pl = exp(-dot(pd, pd) * 1.6);
                vec3 colf = floorc * (0.18 + 1.25 * pl) + vec3(0.30, 0.34, 0.40) * pl * 0.22;
                float fb = smoothstep(hz - 6.0, hz + 10.0, px.y);
                room1 = mix(colw, colf, fb);
                // A skirting line where the wall meets the floor.
                room1 *= 1.0 - 0.45 * (1.0 - smoothstep(0.0, 3.0, abs(px.y - hz)));
                // THE CONE, from the bulb to the pool: light in the dust.
                vec2 axis = pool - bulb;
                float alen = max(length(axis), 1.0);
                vec2 ad = axis / alen;
                vec2 rel = px - bulb;
                float along = dot(rel, ad);
                float perp = abs(rel.x * ad.y - rel.y * ad.x);
                float u = clamp(along / alen, 0.0, 1.2);
                float cwid = mix(12.0, 250.0, u);
                float cone = step(0.0, along) * (1.0 - smoothstep(cwid * 0.55, cwid, perp))
                           * (1.0 - smoothstep(1.0, 1.15, u));
                float dust = 0.65 + 0.35 * my_hash(floor(px * 0.25) + floor(t * 8.0));
                room1 += vec3(0.34, 0.38, 0.44) * cone * (0.22 - 0.12 * u) * dust * u_my_hang.w;
                // The bulb's own halo.
                room1 += vec3(0.95, 0.96, 1.00) * exp(-bd * bd / (22.0 * 22.0)) * 0.9 * u_my_hang.w;
                room1 += vec3(0.40, 0.44, 0.52) * exp(-bd * bd / (90.0 * 90.0)) * 0.22 * u_my_hang.w;
            }

            // --- ACT TWO: the dark, from above ---------------------------------
            vec3 room2 = vec3(0.0);
            if (open > 0.001) {
                vec2 sp2 = c + vec2(sin(t * 0.07), cos(t * 0.05)) * 0.006;
                vec2 q2 = floor((sp2 + 0.5) * 300.0) / 300.0;
                float lum2 = my_lum(tex0, q2);
                // The same boards, from above, resolved through the substrate
                // -- which is what this room has instead of a surface. Read
                // through the hole's swirl, so the rupture takes the floor too.
                vec2 pw = (c + 0.5) * res;
                float bl2 = dot(texture2D(tex1, pw / 420.0 + vec2(0.13, 0.71)).rgb, vec3(0.3333));
                float fl2 = clamp(bl2 * 1.20 * (0.72 + 0.56 * lum2), 0.0, 1.3);
                vec3 substrate = mix(vec3(0.044, 0.056, 0.078), vec3(0.42, 0.47, 0.55), fl2);
                // Not black: a floor in the dark is a shape, very faintly.
                room2 = substrate * 0.085 + vec3(0.010, 0.012, 0.018);
                vec2 lp = u_my_lamp.xy;
                float lr = max(u_my_lamp.z, 8.0);
                float ls = clamp(u_my_lamp.w, 0.0, 1.0);
                float ld = distance(px, lp);
                float lamp = (1.0 - smoothstep(lr * 0.50, lr * 1.04, ld)) * ls;
                float flick = 0.55 + 0.45 * sin(t * 41.0 + sin(t * 9.7) * 3.4);
                lamp *= mix(1.0, mix(1.0, flick, 0.72), dread);
                room2 += substrate * lamp * 0.95 + vec3(0.30, 0.36, 0.44) * lamp * 0.18;
                // THE EDGE OF THE LIGHT is the instrument the bell reads, so it
                // is drawn: a thin chalk rim exactly at the lamp's radius.
                float rim = 1.0 - smoothstep(0.0, 2.2, abs(ld - lr));
                room2 += vec3(0.62, 0.68, 0.76) * rim * 0.30 * ls;
                // The bell's countdown, on that rim: an arc that closes clockwise
                // from twelve o'clock, gold as it nears the stroke.
                if (u_my_count.w > 0.001) {
                    float a = atan(px.x - lp.x, -(px.y - lp.y));
                    float af = (a < 0.0 ? a + 6.2831853 : a) / 6.2831853;
                    float arcr = 1.0 - smoothstep(0.0, 3.2, abs(ld - (lr + 7.0)));
                    float on = step(af, u_my_count.w);
                    vec3 cc = mix(vec3(0.60, 0.66, 0.74), vec3(0.95, 0.76, 0.36),
                                  smoothstep(0.65, 1.0, u_my_count.w));
                    // .x: the stroke this arc is counting down to REOPENS the
                    // case instead of answering, and the arc says so in red.
                    cc = mix(cc, vec3(0.94, 0.22, 0.28), clamp(u_my_count.x, 0.0, 1.0));
                    room2 += cc * arcr * on * (0.55 + 0.30 * smoothstep(0.70, 1.0, u_my_count.w)) * ls;
                }
                // The bell itself: a ring of light running out from the rim.
                if (u_my_bell.w > 0.001) {
                    float bdd = abs(distance(px, u_my_bell.xy) - u_my_bell.z);
                    float br = exp(-bdd * bdd / (9.0 * 9.0));
                    room2 += vec3(0.95, 0.80, 0.45) * br * u_my_bell.w;
                }
            }

            vec3 col = mix(room1, room2, open);

            // --- REOPENING: the edges go red and come inward ---------------------
            if (reop > 0.002) {
                float vgr = length(c);
                col = mix(col, vec3(0.26, 0.035, 0.070),
                        reop * smoothstep(0.62 - 0.42 * reop, 0.78, vgr) * 0.92);
            }

            if (hs > 0.001) {
                float core = 1.0 - smoothstep(hr * 0.12, hr * 0.56, hd);
                col *= mix(1.0, 0.010, core * hs);
                float lip = 1.0 - smoothstep(0.0, hr * 0.09, abs(hd - hr * 0.56));
                col = mix(col, vec3(0.72, 0.78, 0.86), lip * hs * 0.85);
            }

            // Grain: this room has no surface, it has a resolution.
            float tooth = my_hash(floor(px * 0.5) + floor(t * 24.0) * 0.013);
            col *= 1.0 - (0.055 + 0.045 * open + 0.050 * heat) * tooth;

            // The frame closes with dread, and it closes hard.
            float vg = length(c);
            float vin = vg * vg * mix(0.86, 0.62 + 2.30 * dread, open);
            col *= max(0.0, 1.0 - vin);

            col = mix(col, vec3(0.86, 0.90, 0.96), clamp(u_my_flash, 0.0, 1.0));
            col *= 1.0 - clamp(u_my_dark, 0.0, 1.0);
            gl_FragColor = vec4(col, 1.0);
        """)
    def _my_register_lacuna():
        # MYSTERY'S OWN BODY -- the fourth axis. Every Archivist gets its own
        # way of being wrong or they all read as the same puppet in hats.
        #
        #   Biography  MISREGISTRATION. Fourteen hard bands sliding out of
        #              sync, chromatic fringing, high frequency. Digital.
        #   Horror     UNDULATION. Low frequency, liquid, no colour split, a
        #              swell from inside, a silhouette that frays into smoke.
        #   Nonfiction REPRODUCTION. It does not deform at all -- it is
        #              printed, posterized, screened, and its bands JUMP to a
        #              new offset and hold rather than travelling.
        #   Mystery    STRATIFICATION AND APERTURE, and it is the fourth thing
        #              rather than a blend of the other three.
        #
        # STRATIFICATION: it is not one body, it is a stack of layers sorted by
        # depth, and they slide against each other continuously and slowly on
        # unrelated clocks. Nothing about it ever jitters and nothing about it
        # ever settles. You never see the whole of it in one arrangement, so
        # there is no arrangement of it to remember.
        #
        # APERTURE: holes open and drift across it -- and what is inside a hole
        # is NOT the room behind it. It is more of the same coat, sampled from
        # somewhere else entirely. You cannot see through this thing. There is
        # only ever more of it. (The source art has the holes in it already;
        # this makes them behave.)
        #
        # THE LIT SLIVER: only a band of it is ever lit, and the band travels.
        # In an encounter whose second half is a dark room, a figure that is
        # fully and evenly lit is a figure from a different fight. u_lac_lit
        # widens the band to the whole body, which happens exactly once, at
        # the end of the winning ending, and is the only time it is all there.
        #
        # And it does not erode in cells, drain bottom-up, or get struck out.
        # IT LEAVES BY BECOMING ALL HOLES: u_lac_diss grows the apertures until
        # there is nothing between them.
        renpy.register_shader("inv.lacuna", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_lac_res;
            uniform float u_lac_t;
            uniform float u_lac_shear;
            uniform float u_lac_ap;
            uniform float u_lac_band;
            uniform float u_lac_lit;
            uniform vec2 u_lac_stretch;
            uniform float u_lac_pivot;
            uniform float u_lac_hurt;
            uniform float u_lac_diss;
            uniform vec4 u_lac_tint;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float lac_hash(vec2 p) {
                return fract(sin(dot(p, vec2(27.19, 93.41))) * 21643.317);
            }
        """, fragment_300="""
            // The plate's OWN coordinate, kept before anything warps it. The
            // mesh is clipped at this rectangle, so the feather at the bottom
            // of this shader has to be measured in it and not in the warped
            // space the rest of the effect works in.
            vec2 plate_uv = v_tex_coord;

            vec2 uv = v_tex_coord;
            vec2 piv = vec2(0.5, clamp(u_lac_pivot, 0.0, 1.0));
            vec2 stv = max(u_lac_stretch, vec2(0.08));
            uv = (uv - piv) / stv + piv;

            float t = u_lac_t;
            float shear = clamp(u_lac_shear, 0.0, 3.0);
            float ap = clamp(u_lac_ap, 0.0, 1.0);
            float diss = clamp(u_lac_diss, 0.0, 1.0);
            vec2 res = max(u_lac_res, vec2(1.0));

            // STRATA. Probe once to find out how deep this pixel is, then
            // sample again through that stratum's own drift. Seven layers,
            // seven unrelated clocks, and the deeper a layer is the further it
            // has wandered from the one in front of it.
            vec4 probe = texture2D(tex0, uv);
            float plum = dot(probe.rgb, vec3(0.299, 0.587, 0.114));
            float layer = floor(clamp(plum, 0.0, 0.999) * 7.0);
            float lph = lac_hash(vec2(layer, 4.1)) * 6.2831853;
            float lrt = 0.55 + lac_hash(vec2(layer, 8.3)) * 0.9;
            vec2 drift = vec2(cos(t * 0.21 * lrt + lph),
                            sin(t * 0.17 * lrt + lph * 1.7))
                        * (0.003 + 0.026 * shear)
                        * (0.30 + 0.70 * (layer / 6.0));
            vec2 suv = uv + drift;

            vec4 src = texture2D(tex0, suv);
            float a = src.a;
            vec3 col = src.rgb;

            // The deeper strata have less colour in them. Nothing under the
            // coat was ever painted.
            float g = dot(col, vec3(0.299, 0.587, 0.114));
            col = mix(vec3(g), col, 0.28 + 0.60 * (layer / 6.0));

            // APERTURES.
            vec2 P = uv * res;
            float hole = 0.0;
            float lipv = 0.0;
            for (int i = 0; i < 5; i++) {
                float fi = float(i);
                float ph = lac_hash(vec2(fi, 13.0)) * 6.2831853;
                vec2 hc = vec2(0.50 + 0.26 * sin(t * (0.09 + 0.06
                                * lac_hash(vec2(fi, 17.0))) + ph),
                            0.14 + 0.70 * lac_hash(vec2(fi, 23.0))
                                + 0.07 * cos(t * 0.13 + ph));
                // Clamped, because at the old 0.62 * diss a departing
                // aperture was wider than the plate and its lip came off the
                // silhouette as a hard rectangle.
                float R = min((0.030 + 0.044 * lac_hash(vec2(fi, 29.0)))
                        * (0.30 + 1.25 * ap) + 0.34 * diss, 0.44) * res.x;
                float d = distance(P, hc * res);
                hole = max(hole, 1.0 - smoothstep(R * 0.84, R, d));
                lipv = max(lipv, 1.0 - smoothstep(0.0, max(R * 0.11, 1.0),
                                                abs(d - R * 0.88)));
            }

            // What is in a hole is more of the coat, not the room.
            vec4 inner = texture2D(tex0, fract(suv + vec2(0.17, -0.11)));
            float ig = dot(inner.rgb, vec3(0.299, 0.587, 0.114));
            col = mix(col, vec3(ig) * 0.34, hole * 0.90);
            col = mix(col, vec3(0.78, 0.82, 0.88), lipv * (0.22 + 0.40 * ap));

            // THE LIT SLIVER, raking across it.
            float axis = uv.y * 0.84 + uv.x * 0.46;
            float w = mix(0.085, 1.90, clamp(u_lac_lit, 0.0, 1.0));
            float lit = 1.0 - smoothstep(0.0, w, abs(axis - u_lac_band));
            col *= mix(0.085, 1.0, clamp(lit + 0.06, 0.0, 1.0));

            col = mix(col, vec3(1.0), clamp(u_lac_hurt, 0.0, 1.0) * 0.85);
            // The light it is standing in (Oct 2 2026): a key tint, so a
            // figure in your lamp and one at the edge of the dark are not lit
            // by the same nothing.
            col *= mix(vec3(1.0), u_lac_tint.rgb, clamp(u_lac_tint.a, 0.0, 1.0));

            // It leaves by becoming all holes.
            float gone = smoothstep(0.74, 1.0, diss);
            a *= (1.0 - hole * mix(0.50, 1.0, diss)) * (1.0 - gone);
            // 0.85 rather than 0.55: with RGB now clamped to alpha, a
            // lip is only as bright as it is opaque, so an alpha this
            // low was quietly dimming the rim it exists to draw.
            a = max(a, lipv * probe.a * (1.0 - gone) * 0.85);

            // FEATHER THE PLATE. A mesh shader is clipped dead at the
            // rectangle it is drawn on, so anything still opaque when it
            // reaches the boundary is cut off in a straight line -- and a
            // straight line across a figure made of torn paper reads as a
            // container, which is exactly what it is and exactly what the
            // player must never see. The aperture lips are the worst
            // offenders because they are bright rings that get large during
            // an arrival or a departure.
            //
            // This makes the cut impossible rather than unlikely: whatever
            // the strata, the apertures or the stretch do, alpha is already
            // zero before the edge, so the plate can never draw its own
            // outline. It is the guarantee, not the padding -- the padding
            // just decides how much room the effect gets first.
            vec2 pe = min(plate_uv, vec2(1.0) - plate_uv);
            a *= smoothstep(0.0, 0.055, min(pe.x, pe.y));

            // PREMULTIPLIED ALPHA, AND THIS IS THE ONE THAT ACTUALLY DREW THE
            // BOX. Ren'Py's model renderer blends premultiplied: the result is
            // src + dst * (1 - a). So a pixel whose RGB is brighter than its
            // own alpha ADDS light to whatever is behind it, and a pixel at
            // alpha ZERO with bright RGB adds light while claiming to be
            // invisible.
            //
            // Everything in this shader that pushes colour around does it
            // without reference to alpha -- the aperture lips mix toward a
            // near-white, the hurt flash mixes toward white, and the hole
            // samples the coat from somewhere the coat is opaque and paints it
            // where this pixel is transparent. All three write bright RGB
            // across the plate's transparent margin, which is why the plate's
            // own RECTANGLE was visible on screen as a glowing box with hard
            // vertical and horizontal edges.
            //
            // Feathering alpha does not fix it and did not: the feather scales
            // `a` and leaves `col` exactly as bright as it was. Clamping RGB to
            // alpha is the fix, and it is the invariant every one of these body
            // shaders has to hold at its last line -- inv.flesh gets it for
            // free because it only ever scales the whole vec4 at once.
            gl_FragColor = vec4(min(col, vec3(a)), a);
        """)

    try:
        _my_register_lamp()
        MY_LAMP_OK = True
    except Exception as _my_lp_e:
        MY_LAMP_OK = False
        try:
            renpy.log("INV FX: lamp shader failed: %r" % _my_lp_e)
        except Exception:
            pass

    try:
        _my_register_lacuna()
        MY_LACUNA_OK = True
    except Exception as _my_lc_e:
        MY_LACUNA_OK = False
        try:
            renpy.log("INV FX: lacuna shader failed: %r" % _my_lc_e)
        except Exception:
            pass


# --- CONSTANTS AND TUNING ----------------------------------------------------
init python:
    from renpy.uguu import GL_REPEAT as _MY_GL_REPEAT

    MY_SOUP_IMG = INV_DIR + "hyperspace.png"
    MY_SPRITE = INV_DIR + "mystery.png"

    MY_SPRITE_W, MY_SPRITE_H = 1024, 1536
    # The figure very nearly fills its own canvas (alpha bbox 59,5 - 981,1527),
    # so the correction is small -- but it is applied the same way as the other
    # fights, because the formula is what future art has to be measured with.
    # FORMULA: MY_FIG_D* = (canvas centre) - (bbox centre), per axis.
    MY_FIG_DX, MY_FIG_DY = -8.0, 2.0
    # Standing a figure up from its FEET (Oct 2 2026): the bbox centre sits
    # MY_FIG_SOLE above the soles at zoom 1, and the figure is MY_FIG_H tall.
    MY_FIG_SOLE = 761.0
    MY_FIG_H = 1522.0

    # 0.245 with the soles on the boards at the pool (MY_A1_FEET) puts the head
    # near y 155: under the lamp rather than wearing it, clear of the chrome,
    # clear of the panels.
    MY_ZOOM_ACT1 = 0.245
    # A plate is a TEXTURE and textures cap at 4096px here. 1536 * 0.90 * 1.30
    # padding is ~1797px, comfortably inside; anything above this zoom is
    # applied to the finished mesh instead of rasterised into the plate.
    MY_PLATE_MAX_ZOOM = 0.90

    # =========================================================================
    # ACT ONE -- THE ROOM (presentation, Oct 2 2026)
    # =========================================================================
    # An interrogation room: a wall, the boards, and one lamp on a cord. The
    # cord hangs from above the frame; the bulb swings on a slow pendulum and
    # takes a kick from anything heavy; its cone comes down through the dust
    # and its pool lands on the boards where the figure stands. inv.lamp draws
    # the room, the cone and the pool; the floor's horizon (372) and the pool's
    # line (528) are fixed in it.
    MY_A1_FEET = 528.0
    MY_HANG_PIVOT = (640.0, -150.0)
    MY_HANG_LEN = 215.0             # the bulb rests at y 65, well above its head
    MY_HANG_SWING = 0.20            # radians, the idle swing
    MY_HANG_PERIOD = 3.6            # seconds
    # THE LINEUP. Act one's FIELD drawn as what it is: twelve empty picture
    # frames, one per reading, each marked with its own glyph -- crossed off
    # when a reading is ruled out, uncrossed when one is reopened. The frames
    # still open at the tear are what walks into the dark, glyphs and all.
    MY_LINEUP_X0 = 874.0            # the first frame's centre
    MY_LINEUP_Y = 46.0
    MY_LINEUP_STEP = 31.5
    MY_PLACARD = 0.30               # a frame drawn at this scale is 29x36
    MY_PLACARD2 = 0.32              # ...and over a suspect's head in the dark

    # =========================================================================
    # ACT ONE -- THE FIELD
    # =========================================================================
    MY_HP_MAX = 280
    MY_LEADS_MAX = 40
    MY_CASE_MAX = 1000
    # 420 and 20, not 520 and 18. THE TEAR SHOULD LAND ON THE CASE, NOT ON
    # THE CLOCK, and that is a joint requirement rather than a pacing one:
    # the field that carries is the field at the instant of the tear, an
    # ACCUSE only reopens by MY_ACCUSE_REOPEN, and so a bout finished by
    # accusing hands over (the field you accused at + 2). A bout finished by
    # the turn cap hands over whatever the field happened to be, which is
    # usually near the ceiling -- measured, at 520/18 three runs in four
    # ended on the cap and every one of them handed over the maximum
    # population regardless of how well the bout had gone.
    MY_SHIFT_CASE = 420
    MY_SHIFT_TURN_CAP = 20

    # THE FIELD. How many readings of the case are still open, and the only
    # number in act one that matters. Everything else in the bout is a way of
    # pushing it in one direction or the other.
    #
    # MY_FIELD_MIN IS TWO AND IT IS NEVER ONE. NARROW is refused there,
    # forever, with no explanation offered -- which is the Archivist's whole
    # nature delivered as an unavailable menu option and learned for free in
    # one turn. Do not "fix" this. It is also load-bearing for act two, where
    # the field becomes a lineup and the bell refuses the same way, in the
    # same two words.
    MY_FIELD_START = 7
    MY_FIELD_MIN = 2
    MY_FIELD_MAX = 12

    # NARROW TAKES TWO OFF, NOT ONE, AND THIS IS THE NUMBER THE WHOLE ACT
    # TURNS ON. The first build had it at one, and the field only ever went
    # UP: the player has a single lever moving it down and the Archivist has
    # three moving it up (INTRODUCE, SOLUTION, REOPENED), so measured over
    # four seeds a bot that narrowed on every available turn went 7 -> 12 and
    # dealt LITERALLY ZERO damage in eighteen turns. A tug of war with one
    # rope on one side and three on the other is not a tug of war.
    MY_NARROW_COST = 5             # leads
    MY_NARROW_FIELD = 2
    MY_NARROW_DOUBT = 7

    # ACCUSE. Worth more the narrower the field is, and the command panel
    # prints the live figure next to the word -- that readout is the entire
    # tutorial for the act and it is a number, not a sentence.
    #   field 12 -> 22      field 7 -> 82      field 4 -> 118    field 2 -> 142
    MY_ACCUSE_BASE = 22
    MY_ACCUSE_PER = 12
    # ...and it reopens the case, because everything a failed accusation ruled
    # out is on the table again. This is the whole rhythm of act one: build a
    # position, spend it, watch it come back.
    MY_ACCUSE_REOPEN = 2
    MY_ACCUSE_DOUBT = 8

    # RECHECK is the honest move and honesty costs. Health, leads and quiet,
    # in exchange for going back over ground you had already covered -- which
    # opens a line of inquiry you had closed.
    MY_RECHECK_HEAL = 68
    MY_RECHECK_LEADS = 14
    MY_RECHECK_DOUBT = 30
    MY_RECHECK_FIELD = 1
    MY_GUARD_MULT = 0.45

    # DOUBT does not climb toward failure. It climbs toward CERTAINTY, which
    # is the thing this Archivist cannot permit, so it is what fires the
    # capstone.
    MY_DOUBT_MAX = 100
    MY_DOUBT_START = 10
    MY_DOUBT_STEP_LO, MY_DOUBT_STEP_HI = 3, 6
    MY_DOUBT_FLOOR = 30

    MY_TEST_BASE = 14
    MY_TEST_PER = 3.2              # being close is what hurts
    MY_INTRO_DMG = 16
    # IT IS AS GOOD AT NARROWING THE CASE AS YOU ARE, and it does it for
    # nothing, unprompted, on more of its turns than any other move. The
    # price is entirely in the other column: a disclosure is the single
    # biggest contributor to DOUBT in the fight, which is to say EVERY
    # KINDNESS IT DOES YOU MOVES YOU CLOSER TO THE CASE BEING REOPENED. That
    # relationship is the character of this Archivist expressed as two
    # numbers, and it is the reason DISCLOSE is not simply a gift.
    MY_DISCLOSE_FIELD = 2
    MY_DISCLOSE_DOUBT = 12
    MY_ALIBI_BACK = 24
    # DENOUEMENT: announced a full turn ahead, always. It is the decision the
    # act is built around -- cash your position in now, or keep narrowing and
    # eat it.
    MY_DN_DMG_BASE = 24
    MY_DN_DMG_PER = 4.5
    MY_DN_FIELD = 3
    MY_REOPEN_DMG = 54
    MY_REOPEN_FIELD = 4
    MY_REOPEN_CASE = 90

    # RUN never works. It is the one joke the form allows and it is played
    # completely straight: every refusal is a true statement about the state of
    # the case, and it is a different true statement each time.
    MY_RUN_WORDS = ("STILL OPEN", "NOT RULED OUT", "INCONCLUSIVE",
                    "SEE FIELD", "PENDING")

    MY_CMDS = (("narrow", "NARROW"), ("accuse", "ACCUSE"),
            ("recheck", "RECHECK"), ("run", "RUN"))

    def my_accuse_damage(field):
        """What ACCUSE is worth at this field. Printed live in the menu."""
        field = int(inv_clamp(field, MY_FIELD_MIN, MY_FIELD_MAX))
        return int(MY_ACCUSE_BASE + MY_ACCUSE_PER * (MY_FIELD_MAX - field))

    # =========================================================================
    # ACT TWO -- THE LINEUP IN THE DARK (rebuilt Oct 2 2026)
    # =========================================================================
    # The user found the old act two loose as a detective puzzle, and it was:
    # its evidence was anonymous rings from invisible bodies that crossed into
    # knots meaning nothing in particular, and the heartbeat ended up doing the
    # real work. It is now a WITNESS LINEUP (user's choice, Oct 2 2026):
    #
    #   * The suspects STAND IN THE ROOM. They are the field act one carried --
    #     one figure per reading still open, each under its own frame and
    #     glyph -- seen faintly in the dark and fully only in your lamp. One
    #     of them is the subject. They all look alike: it wears THE
    #     INVESTIGATOR, every reading of it does.
    #   * THE BELL. On a countdown drawn round the edge of your light, a bell
    #     reports one true thing: whether the subject is inside your lamp right
    #     now. SEEN, or UNSEEN. Every suspect whose own state does not match is
    #     CROSSED OFF. The verdict is binary and the deduction exact, so
    #     positioning the light at the stroke is the whole skill: light half
    #     the field, learn half the field.
    #   * NEVER ONE. At two it says TWO REMAIN, act one's refusal word for
    #     word, and crosses no one. If a verdict would leave one it withholds
    #     the verdict and leaves two -- crossing every mismatch but the one
    #     nearest the rim. (Whoever watched which side the crosses fell on
    #     can still work out the last step. The Archivist will not add it up
    #     for you; it never stops you adding it up.) Otherwise the last split
    #     is dread's: the heartbeat and the failing lamp say which of two you
    #     are standing near.
    #   * ACCUSE (hold Z on a suspect): the subject is SOLVED -- and the case
    #     REOPENS (crosses lift, it is someone else now, and the field widens
    #     by one: act one's law). A bystander is RULED OUT and leaves through
    #     a hole; a new reading walks in later. Wrong answers cost TIME.
    #   * Health has one source and it is not the puzzle: the subject touching
    #     you. It drifts toward your light; so, in fits, do the others.
    #   * The case also reopens ON THE BELL: every few strokes one of them is
    #     a reopening instead of a verdict, and the countdown arc runs red for
    #     it. Spend the position you have or lose it.
    #
    # THE HONESTY CONTRACT: the subject is never crossed off, a verdict is
    # never false, and the bell never leaves fewer than two. MYGame.audit
    # counts violations; any count above zero is a bug.
    # A stroke is computed from FEET positions against the drawn rim.
    MY_AR_X, MY_AR_Y = 130, 236
    MY_AR_W, MY_AR_H = 1020, 416    # where FEET can be; figures stand up from it

    MY_SPEED = 3.9                  # px per tick
    MY_PLAYER_R = 13.0

    MY_HP2_MAX = 280
    MY_HIT_HP = 22                  # thirteen contacts
    MY_IFRAMES = 72

    # THE LAMP. Its rim is the instrument the bell reads, so it is drawn.
    MY_LAMP_R = 168.0
    MY_LAMP_MIN = 58.0              # what SWEEP leaves you with
    # SWEEP: seeing more at the price of your eyes. Timed to a stroke it
    # lights most of the room -- the right play exactly when dread says the
    # subject is far away (UNSEEN then crosses off everything you lit). The
    # lamp comes back over exactly MY_SWEEP_BLIND ticks: the rate is derived,
    # so the two can never disagree (Horror's HOR_STRUCT_PHASE lesson).
    MY_SWEEP_R = 340.0
    MY_SWEEP_TICKS = 30
    MY_SWEEP_BLIND = 108
    MY_SWEEP_CD = 220

    # THE BELL.
    MY_BELL_EVERY = 255             # ticks between strokes, early
    MY_BELL_EVERY_HOT = 210         # ...and late
    MY_BELL_WARN = 84               # the ticking before the stroke
    MY_BELL_FIRST = 230             # the first stroke after the lights go out
    MY_BELL_RING = 46               # the ring running out from the rim
    # Every MY_REOPEN_STROKES-th stroke reopens the case instead of answering
    # (one fewer once the case has gone cold).
    MY_REOPEN_STROKES = 4
    MY_REOPEN_STROKES_HOT = 3
    MY_STROKE_KEEP = 3              # chalk rings left where the light was

    # THE POPULATION.
    MY_BODIES_MIN, MY_BODIES_MAX = 2, 6
    MY_BODY_HARDCAP = 7
    MY_REPLACE_DELAY = 96
    MY_ARRIVE_TICKS = 46            # rising out of a hole in the boards
    MY_LEAVE_TICKS = 40             # becoming all holes
    MY_LINE_HOLD = 110              # they stand in a line, then break it
    MY_SEP = 58.0                   # suspects keep this far apart

    MY_SUB_SPEED = 0.95
    MY_SUB_SPEED_HOT = 1.25
    MY_BYS_SPEED_LO, MY_BYS_SPEED_HI = 0.60, 1.10
    # CURIOSITY: every suspect, in fits, drifts toward your light -- moths to a
    # lamp -- so "the one that keeps coming closer" is not a free answer. The
    # subject's pull is steady; a bystander's comes and goes.
    # Measured (Oct 2): at a subject pull of 0.42 against bystanders curious
    # 1 tick in 520, "accuse whatever is nearest" hit the subject well above
    # chance and a bot doing nothing else won every run. The tell has to be
    # a tendency over time, never a free answer.
    MY_SUB_PULL = 0.28
    MY_CURIOUS_PULL = 0.34
    MY_CURIOUS_CHANCE = 1.0 / 340.0
    MY_CURIOUS_LEN = (150, 330)
    MY_BREAK_SPEED = 13.0
    MY_TOUCH_R = 26.0

    # ACCUSE, act two. Act one's word, and the player has spent a whole act
    # learning what it means.
    MY_NAME_TICKS = 40
    # TWO COOLDOWNS, AND THE DIFFERENCE BETWEEN THEM IS WHAT A WIDE FIELD
    # COSTS: more things in the room means more of your accusations land on
    # the wrong one, and the bill arrives as time rather than as damage --
    # the only currency the puzzle is allowed to charge in.
    MY_NAME_CD = 46
    MY_NAME_CD_MISS = 100
    # A WRONG ACCUSATION TURNS THE ROOM ON YOU. Every suspect closes on your
    # light at once for a moment -- all of them, so the charge identifies
    # nobody -- and the one that can hurt you is in the crowd. Avoidable
    # (you are faster than all of them, and dread still says which one is
    # near), and it is what makes guessing cost: measured, with time as the
    # only price a bot accusing at random won as fast as one deducing.
    MY_CLOSE_TICKS = 150
    MY_CLOSE_PULL = 0.72
    MY_CLOSE_SPEED = 1.45
    MY_NAME_R = 96.0
    MY_NAME_DRIFT = 1.05            # you may creep this much per tick, no more

    MY_SOLVE_MAX = 100.0
    MY_SOLVE_GAIN = 25.0            # four landed accusations
    # ...and a wrong one takes half a pip back. Act one's rule in act two's
    # terms: an accusation is worth something only once the field is narrow.
    # Measured (Oct 2), with time as the only price, accusing whatever was in
    # reach won as fast as deducing; at -12 guessing into a field of four or
    # more loses ground on average, and a guess between two still pays.
    MY_SOLVE_MISS = 12.0
    # GETTING IT RIGHT IS WHAT KEEPS YOU IN THE ROOM: Biography's rule --
    # aggression is the heal -- in this fight's own terms.
    MY_SOLVE_HEAL = 30

    # DREAD: the fairness channel, and the last split's instrument. Analogue,
    # felt, never printed: it can say "not here" without ever saying "there".
    # It drives the heartbeat, the lamp's flicker and the frame closing in.
    MY_DREAD_NEAR = 230.0
    MY_DREAD_FULL = 46.0

    MY_FIG_ZOOM2 = 0.086            # a suspect, standing (about 131px)
    MY_HEART_ZOOM = 2.6
    # The same figure the user pulled twice on the other two: it has to look
    # wrong without becoming the busiest object on screen.
    MY_HEART_WARP = 1.15

    # --- palette: black, chalk, and exactly one warm thing -------------------
    MY_BLACK = "#04050a"
    MY_PALE = "#dce4ee"
    MY_DIM = "#7d8794"
    MY_FAINT = "#4a525e"
    MY_CHALK = "#9aa6b4"
    MY_GOLD = "#e6b855"             # the light, the verdict, the answer
    MY_RED = "#c22a3c"              # contact, and the case reopening
    MY_WARN = "#c8913a"
    MY_LAMPC = "#bcd2e4"

    def my_arena_clamp(x, y, r=0.0):
        return (inv_clamp(x, MY_AR_X + r, MY_AR_X + MY_AR_W - r),
                inv_clamp(y, MY_AR_Y + r, MY_AR_Y + MY_AR_H - r))

    def my_arena_center():
        return (MY_AR_X + MY_AR_W * 0.5, MY_AR_Y + MY_AR_H * 0.5)

    def my_fig_cy(feet, zoom):
        """The bbox centre _draw_body takes, for a figure whose soles are at
        `feet`."""
        return feet - MY_FIG_SOLE * zoom

    def my_glyph(i):
        return INV_GLYPHS[int(i) % len(INV_GLYPHS)]

# --- SIMULATION --------------------------------------------------------------
init python:
    class MYGame(object):
        """All of Mystery's live state, stepped at a fixed 60Hz by MYStage.
        Owns zero rendering."""

        def __init__(self, retry=False, deaths=0, debug=False, start_open=False,
                     resume=None, seed=None):
            self.result = None
            self.paused = False
            self.debug = bool(debug)
            self.retry = bool(retry)
            self.deaths = int(deaths)
            self.god = inv_godmode_on()
            # THE CHECKPOINT carries the field: what act one failed to rule
            # out is what is standing in the dark, glyph for glyph.
            self.checkpoint = None

            self.tick = 0
            self.clock = 0.0
            self.rng = inv_random.Random(seed)
            # Decoration draws from its OWN stream. Respawning grain out of the
            # gameplay RNG costs a whole round of results and reads as a
            # balance swing that is not there (the lesson is Biography's).
            self.rng_fx = inv_random.Random(None if seed is None else seed * 7 + 3)

            # --- presentation (Oct 2 2026; decoration owned by the sim) ------
            self.fx = InvFX(cap=380)
            self.turn_log = []
            self.shock = [640.0, 360.0, 0.0, 0.0]
            self.ca = 0.0
            self.tear = 0.0
            self.panel_kick = 0.0
            self.windup = 0.0
            self.body_hit = 0.0            # the figure struck by ACCUSE
            self.case_flash = 0.0          # ALIBI: the bar growing back
            # THE LAMP ON THE CORD: an idle swing on a fixed period, plus a
            # kicked pendulum on top of it for anything heavy.
            self.hang_th = 0.0
            self.hang_w = 0.0
            self.hang_idle = 1.0           # DENOUEMENT stills it
            self.bulb_dip = 0.0            # gutters
            self.bulb_flare = 0.0          # flares
            self.bulb_fall = None          # the tear: the cord goes
            self.bulb_gone = False
            # THE LINEUP: twelve frames, one glyph each, FIELD of them open.
            self.lineup = []
            open_set = set(self.rng_fx.sample(range(MY_FIELD_MAX), MY_FIELD_START))
            for i in range(MY_FIELD_MAX):
                self.lineup.append({"glyph": i, "open": i in open_set,
                                    "t": -999, "how": "", "carry": False})
            self.carried = []              # the glyphs that walk into the dark

            # --- the party member ------------------------------------------
            self.hp = MY_HP_MAX
            self.hp_shown = float(MY_HP_MAX)
            self.leads = MY_LEADS_MAX
            self.leads_shown = float(MY_LEADS_MAX)
            self.roll_cue = 0

            # --- the case ---------------------------------------------------
            # case  what you have taken off its account of itself.
            # field how many readings are still open. THE number in act one.
            self.case = 0
            self.case_shown = 0.0
            self.field = MY_FIELD_START
            self.field_shown = float(MY_FIELD_START)
            self.doubt = float(MY_DOUBT_START)

            # --- act one ------------------------------------------------------
            self.mode = "arrive"
            self.mtick = 0
            self.turn = 0
            self.cursor = 0
            self.guard = False
            self.dn_pending = False        # DENOUEMENT announced, not landed
            self.last_cmd = None
            self.last_enemy = None
            self.run_i = 0

            self.beat_label = ""
            self.beat_value = ""
            self.beat_after = "menu"

            # --- presentation --------------------------------------------------
            self.flash = 0.0
            self.dark = 1.0
            self.shake = 0.0
            self.open = 0.0                # 0 = the room, 1 = the dark
            # 1.0, not 0.0: the panels start OFF the bottom of the screen
            # and slide up once the bout actually begins (see _step_ambient).
            self.panel_slide = 1.0
            self.hit_flash = 0.0
            self.floats = []
            self.hole = [640.0, 330.0, 240.0, 0.0]
            self.emerge = 1.0
            self.body_ap = 0.35            # aperture size on the body
            self.body_diss = 1.0           # it leaves by becoming all holes
            self.body_lit = 0.0            # how much of it is lit at once
            self.body_band = 0.30          # where the lit sliver is
            self.beat = 0.0
            self.beat_pulse = 0.0
            self.field_carried = MY_FIELD_START

            # --- act two --------------------------------------------------------
            self.px, self.py = my_arena_center()
            self.trail = []
            self.lamp_r = MY_LAMP_R
            self.lamp_s = 0.0              # lamp strength, ramps at the tear
            self.lamp_dip = 0.0            # contact: the lamp gutters
            self.sweep_t = 0
            self.sweep_cd = 0
            self.solve = 0.0
            self.solve_shown = 0.0
            self.solve_flash = 0.0         # SOLVED taken back
            self.solves = 0
            self.iframes = 0
            self.dist = 0.0                # ticks survived, for the ramp

            self.bodies = []
            self.body_seq = 0
            self.replace_q = []            # ticks until a new reading walks in
            self.hold = 0                  # the lineup holds its line

            self.bell_t = MY_BELL_FIRST
            self.bell_period = MY_BELL_EVERY
            self.bell_ring = 1.0           # 0 -> 1 as the ring runs out
            self.bell_at = (0.0, 0.0, 0.0)
            self.strokes_left = MY_REOPEN_STROKES
            self.strokes = []              # chalk rings: where the light was
            self.verdict = ""
            self.verdict_t = 999
            self.last_stroke = None

            self.naming = False
            self.name_t = 0
            self.name_cd = 0
            self.name_target = None
            self.closing = 0               # a wrong accusation: they close in
            self.reopen_warn = 0.0
            self.reopen_flash = 0.0
            self.dread_v = 0.0
            self.ruleouts = []             # chalk crosses where you were wrong
            self.solved_id = None

            # THE HONESTY CONTRACT, counted. The bot harness fails on any
            # nonzero violation (see the act-two header in the constants).
            self.audit = {"strokes": 0, "refusals": 0, "withheld": 0,
                          "crossed": 0, "bad_cross": 0, "below_two": 0,
                          "reopens": 0, "solves": 0, "ruled_out": 0,
                          "contacts": 0, "accuse_none": 0}

            self.hud_fade = 1.0
            self.field_fade = 1.0
            self.end_close = 0.0           # the loss: the lamp going out
            self.lattice_off = 0.0         # the loss: the chalk going with it
            self.end_show = 0.0            # the win: it is finally all lit
            self.end_order = []

            self.keys = MSBFKeyLatch()
            self._prev = {"left": False, "right": False, "up": False,
                        "down": False, "z": False, "x": False}

            if resume:
                # A RETRY FROM THE TEAR: the field act one handed over, with
                # the same glyphs on the same frames.
                self.carried = [int(v) for v in resume.get("glyphs", [])][:MY_BODIES_MAX]
                self.field = int(inv_clamp(resume.get("field", len(self.carried) or 4),
                                           MY_FIELD_MIN, MY_FIELD_MAX))
                self._begin_dark(dev=True)
                self.dark = 1.0
            elif start_open:
                # Dev entry skips the bout, so hand over a middling field --
                # a bout that never happened cannot have ruled anything out.
                self.field = 4
                self.case = 300
                self._begin_dark(dev=True)

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

        def standing(self):
            """What is left of its account of itself."""
            return max(0, MY_CASE_MAX - self.case)

        def standing_frac(self):
            return inv_clamp(self.standing() / float(MY_CASE_MAX), 0.0, 1.0)

        def doubt_frac(self):
            return inv_clamp(self.doubt / float(MY_DOUBT_MAX), 0.0, 1.0)

        def solve_frac(self):
            return inv_clamp(self.solve / MY_SOLVE_MAX, 0.0, 1.0)

        def progress(self):
            """0 at the tear, 1 by the time act two should be over."""
            return inv_clamp(self.dist / 5400.0, 0.0, 1.0)

        def heat(self):
            """HOW COLD THE CASE HAS GOT, 0 to 1 -- half how long you have been
            in the dark, half how far onto the answer you have got, so a slow
            run and a fast one arrive at the same pressure."""
            return inv_clamp(0.5 * self.progress() + 0.5 * self.solve_frac(),
                            0.0, 1.0)

        def subject(self):
            for b in self.bodies:
                if b["subject"]:
                    return b
            return None

        def dread(self):
            return self.dread_v

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
                col = MY_DIM if self.god else MY_RED
                self.float_text(x, y, "-%d" % amount, col, True)

        def _deal(self, amount):
            """Take something off its account of itself."""
            amount = int(max(0, amount))
            self.case = int(min(MY_CASE_MAX, self.case + amount))
            return amount

        # ----- the lamp on the cord ---------------------------------------------

        def hang_angle(self):
            idle = MY_HANG_SWING * self.hang_idle * math.sin(
                self.clock * 6.2831853 / MY_HANG_PERIOD)
            return idle + self.hang_th

        def bulb_pos(self):
            if self.bulb_fall is not None:
                return (self.bulb_fall["x"], self.bulb_fall["y"])
            th = self.hang_angle()
            return (MY_HANG_PIVOT[0] + MY_HANG_LEN * math.sin(th),
                    MY_HANG_PIVOT[1] + MY_HANG_LEN * math.cos(th))

        def pool_x(self):
            """Where its light lands on the boards. The cone tilts with the
            cord, so the pool sweeps further than the bulb does."""
            bx, by = self.bulb_pos()
            if self.bulb_fall is not None:
                return bx
            return bx + (MY_A1_FEET - by) * math.tan(self.hang_angle()) * 0.8

        def bulb_level(self):
            if self.bulb_gone:
                return 0.0
            lv = (1.0 - inv_clamp(self.bulb_dip, 0.0, 1.0)) + self.bulb_flare
            return inv_clamp(lv, 0.0, 1.8)

        def _kick_lamp(self, w, dip=0.0, flare=0.0):
            self.hang_w += w
            self.bulb_dip = max(self.bulb_dip, dip)
            self.bulb_flare = max(self.bulb_flare, flare)

        def _step_hang(self):
            # A pendulum on top of the idle swing: k from the period, a little
            # air resistance, nothing else.
            k = (6.2831853 / (MY_HANG_PERIOD * 60.0)) ** 2
            self.hang_w += -k * self.hang_th - 0.012 * self.hang_w
            self.hang_th = inv_clamp(self.hang_th + self.hang_w, -0.9, 0.9)
            target = 0.0 if self.dn_pending else 1.0
            self.hang_idle = inv_approach(self.hang_idle, target, 0.012)
            self.bulb_dip *= 0.90
            self.bulb_flare *= 0.90
            if self.mode == "enemy" and self.mtick < 26:
                # Its turn: the filament stutters while it decides.
                if self.rng_fx.random() < 0.18 * self.windup:
                    self.bulb_dip = max(self.bulb_dip, self.rng_fx.uniform(0.2, 0.5))

            if self.bulb_fall is not None:
                f = self.bulb_fall
                f["vy"] += 0.85
                f["x"] += f["vx"]
                f["y"] += f["vy"]
                f["vx"] *= 0.99
                if f["y"] >= MY_A1_FEET - 6.0 and not self.bulb_gone:
                    self._shatter_bulb(f["x"], MY_A1_FEET - 6.0)

        def _cone_dust(self):
            """Dust in the cone. Decoration, from the decoration stream."""
            bx, by = self.bulb_pos()
            pool = self.pool_x()
            u = self.rng_fx.uniform(0.12, 1.0)
            ax = bx + (pool - bx) * u
            ay = by + (MY_A1_FEET - by) * u
            w = inv_lerp(12.0, 250.0, u) * 0.42
            x = ax + self.rng_fx.uniform(-w, w)
            layer = "front" if self.rng_fx.random() < 0.35 else "back"
            self.fx.emit("dust", x, ay, vx=self.rng_fx.uniform(-0.18, 0.18),
                         vy=self.rng_fx.uniform(-0.10, 0.12),
                         life=self.rng_fx.randint(90, 170),
                         size=self.rng_fx.uniform(0.45, 1.15), col="#d6dfec",
                         alpha=self.rng_fx.uniform(0.22, 0.50) * self.bulb_level(),
                         add=True, drag=0.995, fade="inout", layer=layer)

        def _shatter_bulb(self, x, y):
            self.bulb_gone = True
            # The dust was only ever visible in its light.
            for q in self.fx.parts:
                if q["t"] == "dust":
                    q["life"] = min(q["life"], max(q["age"], 0) + 8)
            self.play("break", 0.85)
            self.flash = max(self.flash, 0.45)
            self.shake = 0.8
            self._kick_lens(x, y, 0.8, 0.006)
            self.tear = 0.6
            self.fx.burst(INV_SHARDS, x, y, 18, speed=(2.0, 8.5), life=(28, 56),
                          size=(0.25, 0.65), col="#e8eef6", alpha=0.95, add=False,
                          drag=0.93, ay=0.32, angle=-90.0, spread=170.0,
                          vrot=(-14.0, 14.0), fade="late", layer="front")
            self.fx.burst("spark", x, y, 22, speed=(3.0, 11.0), life=(10, 24),
                          size=(0.25, 0.6), col="#fff3d8", alpha=1.0, add=True,
                          drag=0.86, angle=-90.0, spread=200.0, stretch=0.35,
                          layer="front")
            self.fx.emit("glow", x, y, life=26, size=3.4, size1=5.5, col="#f4ecd8",
                         alpha=0.9, add=True, fade="out2", layer="front")

        # ----- the lineup -------------------------------------------------------

        def lineup_pos(self, i):
            return (MY_LINEUP_X0 + i * MY_LINEUP_STEP, MY_LINEUP_Y)

        def _set_field(self, value, how="you"):
            self.field = int(inv_clamp(value, MY_FIELD_MIN, MY_FIELD_MAX))
            self._sync_lineup(how)

        def _sync_lineup(self, how):
            """The frames follow the number: crossed off as it falls, reopened
            as it climbs -- which frames is decoration, how many never is."""
            opened = [f for f in self.lineup if f["open"]]
            closed = [f for f in self.lineup if not f["open"]]
            while len(opened) > self.field and opened:
                f = self.rng_fx.choice(opened)
                opened.remove(f)
                f["open"] = False
                f["t"] = self.tick
                f["how"] = how
                x, y = self.lineup_pos(f["glyph"])
                self.fx.burst("dust", x, y, 7, speed=(0.4, 1.8), life=(14, 28),
                              size=(0.6, 1.3),
                              col=(MY_GOLD if how == "it" else MY_PALE), alpha=0.8,
                              add=True, drag=0.9, layer="hud")
            while len(opened) < self.field and closed:
                f = self.rng_fx.choice(closed)
                closed.remove(f)
                opened.append(f)
                f["open"] = True
                f["t"] = self.tick
                f["how"] = "reopen"
                x, y = self.lineup_pos(f["glyph"])
                self.fx.ring(x, y, 6.0, 26.0, life=22, col=MY_RED, alpha=0.8,
                             layer="hud")

        # ----- input -----------------------------------------------------------

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
            elif mode == "dark":
                self._step_dark(edges)
            elif mode in ("leave_w", "leave_l"):
                self._step_leave()

        def _step_ambient(self):
            self.tick += 1
            self.clock += INV_TICK

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
            self.body_hit *= 0.86
            self.case_flash *= 0.90
            self.reopen_flash *= 0.94
            self.solve_flash *= 0.92

            # --- presentation state ------------------------------------------
            self.fx.step()
            self.ca *= 0.86
            self.tear *= 0.88
            self.panel_kick *= 0.84
            self.windup *= 0.94
            if self.shock[3] > 0.004:
                self.shock[2] += 15.0 + self.shock[2] * 0.05
                self.shock[3] *= 0.90
            else:
                self.shock[3] = 0.0
            if self.open < 0.5:
                self._step_hang()
                if self.tick % 2 == 0 and not self.bulb_gone and self.mode != "arrive":
                    self._cone_dust()
            elif self.mode == "dark" and self.tick % 3 == 0:
                self._lamp_dust()

            # The lit sliver never stops travelling across it. Nothing on this
            # body is ever held still and nothing on it ever jumps.
            self.body_band = 0.30 + 0.62 * (0.5 + 0.5 * math.sin(
                self.clock * 0.37))

            for attr, real in (("hp_shown", self.hp), ("leads_shown", self.leads)):
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

            gap = abs(self.case_shown - self.case)
            if gap > 0.01:
                self.case_shown = inv_approach(self.case_shown, float(self.case),
                                            inv_clamp(gap * 0.10, 0.6, 9.0))
            else:
                self.case_shown = float(self.case)

            # THE FIELD ROLLS TOO, and slowly -- in act one it is the number
            # the fight is about, in act two it counts what is not crossed off.
            want = self.field if self.open < 0.5 else self.field_now()
            gap = abs(self.field_shown - want)
            if gap > 0.005:
                self.field_shown = inv_approach(self.field_shown, float(want),
                                                inv_clamp(gap * 0.10, 0.012, 0.09))
            else:
                self.field_shown = float(want)

            gap = abs(self.solve_shown - self.solve)
            if gap > 0.005:
                self.solve_shown = inv_approach(self.solve_shown, self.solve,
                                                inv_clamp(gap * 0.12, 0.05, 1.4))
            else:
                self.solve_shown = self.solve

            for f in self.floats:
                f["y"] += f["vy"]
                f["vy"] += 0.055
                f["life"] -= 1
            self.floats = [f for f in self.floats if f["life"] > 0]

            if self.hp_shown <= 0.0 and self.mode not in ("leave_w", "leave_l",
                                                        "arrive"):
                self._begin_leave(False)

        # =====================================================================
        # ARRIVAL -- the light fails, three times
        # =====================================================================
        # It is never seen arriving. Nothing walks out of the rupture and
        # nothing is assembled in front of you: the bulb simply goes out, and
        # when it comes back there is more of it standing there than there was.
        # Rule 4 is honoured by what the hole TAKES rather than by what it gives.

        def _step_arrive(self):
            self.mtick += 1
            t = self.mtick
            self.dark = inv_clamp(1.0 - t / 30.0, 0.0, 1.0)

            if t == 6:
                self.play("tear", 0.75)
            if t < 70:
                self.hole[3] = inv_smooth(t / 70.0)
                self.hole[2] = inv_lerp(30.0, 240.0, inv_smooth(t / 70.0))
                self.body_diss = 1.0
                self.body_lit = 0.0
                self.emerge = 1.0
            elif t < 250:
                self.hole[3] = 1.0
                # THREE FAILURES OF THE LIGHT. Each one is the bulb going out
                # and a slower recovery, and each recovery brings back more of
                # it than the last.
                if t in (76, 136, 196):
                    self.play("phase", 0.5)
                    self._kick_lamp(0.004, dip=1.0)
                    self.dark = 1.0
                    self.shake = 0.30
                step_i = 0 if t < 136 else (1 if t < 196 else 2)
                since = t - (76, 136, 196)[step_i]
                if since >= 0:
                    self.dark = max(self.dark,
                                    inv_clamp(1.0 - since / 34.0, 0.0, 1.0))
                self.body_diss = (0.74, 0.42, 0.12)[step_i]
                self.body_ap = (0.85, 0.62, 0.42)[step_i]
                self.body_lit = (0.06, 0.14, 0.24)[step_i]
                self.emerge = 1.0 - inv_clamp((t - 76) / 170.0, 0.0, 1.0)
            elif t < 300:
                u = (t - 250) / 50.0
                self.body_diss = inv_lerp(0.12, 0.0, inv_smooth(u))
                self.body_ap = inv_lerp(0.42, 0.34, inv_smooth(u))
                self.hole[3] = 1.0 - inv_smooth(u)
                self.hole[2] = inv_lerp(240.0, 24.0, inv_smooth(u))
            elif t == 300:
                self.hole[3] = 0.0
                self.body_diss = 0.0
                inv_music_survey()
            elif t >= 324:
                self._begin_player_turn()

        # =====================================================================
        # ACT ONE -- THE FIELD
        # =====================================================================

        def _begin_player_turn(self):
            # The cursor stays where you left it.
            self.mode = "menu"
            self.mtick = 0
            self.turn += 1
            self.guard = False

        def _step_menu(self, edges):
            self.mtick += 1
            n = len(MY_CMDS)
            if edges["up"]:
                self.cursor = (self.cursor - 1) % n
                self.play("cursor")
            elif edges["down"]:
                self.cursor = (self.cursor + 1) % n
                self.play("cursor")
            if edges["z"]:
                self.play("confirm")
                self._resolve_player(MY_CMDS[self.cursor][0])

        def _step_beat(self, edges):
            # Holds, then moves on; the readout outlives it in the turn log.
            self.mtick += 1
            if (self.mtick >= INV_BEAT_HOLD
                    or (self.mtick > INV_BEAT_SKIP and (edges["z"] or edges["x"]))):
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

        def _resolve_player(self, cmd):
            self.last_cmd = cmd
            label, value = cmd.upper(), ""

            if cmd == "narrow":
                # THE REFUSAL. Two is the floor and it is the floor forever,
                # and the game does not say why. One turn spent finding this
                # out is the cheapest and most complete piece of
                # characterisation in the encounter -- do not add a line of
                # text explaining it and do not lift the floor.
                if self.field <= MY_FIELD_MIN:
                    self.play("cancel")
                    self._beat("NARROW", "TWO REMAIN", "menu")
                    return
                if self.leads < MY_NARROW_COST:
                    self.play("cancel")
                    self._beat("NARROW", "NO LEADS", "menu")
                    return
                self.leads -= MY_NARROW_COST
                self._set_field(self.field - MY_NARROW_FIELD, "you")
                self.doubt = min(float(MY_DOUBT_MAX),
                                self.doubt + MY_NARROW_DOUBT)
                self.play("scan", 0.7)
                self.flash = 0.10
                self._kick_lamp(0.003)
                value = "FIELD  %d" % self.field

            elif cmd == "accuse":
                dealt = self._deal(my_accuse_damage(self.field))
                self.doubt = min(float(MY_DOUBT_MAX),
                                self.doubt + MY_ACCUSE_DOUBT)
                self.play("bash")
                self.shake = 0.34
                self.flash = 0.18
                self.body_hit = 1.0
                self.tear = 0.35
                self._kick_lamp(0.010, dip=0.5)
                self._kick_lens(640.0, 300.0, 0.6, 0.004)
                self.fx.burst("spark", 640.0, 300.0, 14, speed=(3.0, 9.0),
                              life=(10, 22), size=(0.25, 0.6), col="#dfe6f0",
                              alpha=0.9, add=True, drag=0.86, stretch=0.35,
                              layer="front")
                self.fx.burst(INV_SMOKES, 640.0, 330.0, 4, speed=(0.3, 1.2),
                              life=(30, 50), size=(0.5, 0.9), col="#9aa6b4",
                              alpha=0.22, add=False, drag=0.95, layer="front")
                value = "-%d" % dealt
                # ...and the case reopens, because everything that accusation
                # ruled out is on the table again.
                before = self.field
                self._set_field(self.field + MY_ACCUSE_REOPEN, "reopen")
                if self.field != before:
                    value += "   FIELD  %d" % self.field

            elif cmd == "recheck":
                self.hp = int(min(MY_HP_MAX, self.hp + MY_RECHECK_HEAL))
                self.leads = int(min(MY_LEADS_MAX,
                                    self.leads + MY_RECHECK_LEADS))
                self.doubt = max(0.0, self.doubt - MY_RECHECK_DOUBT)
                self.guard = True
                before = self.field
                self._set_field(self.field + MY_RECHECK_FIELD, "reopen")
                self.play("heal")
                # The light steadied: the swing taken out of it, the pool
                # brighter, a slow ring going out across the boards.
                self.hang_w *= 0.3
                self.hang_th *= 0.5
                self.bulb_flare = 0.35
                self.fx.ring(self.pool_x(), MY_A1_FEET, 40.0, 270.0, life=44,
                             col="#cfe0f0", alpha=0.45, layer="back",
                             tex="ring_soft", squash=0.26)
                value = "+%d" % MY_RECHECK_HEAL
                if self.field != before:
                    value += "   FIELD  %d" % self.field

            elif cmd == "run":
                # It never works, and the reason is different every time --
                # and every reason is a true statement about the case.
                self.play("miss")
                self.bulb_dip = 0.7
                value = MY_RUN_WORDS[self.run_i % len(MY_RUN_WORDS)]
                self.run_i += 1

            after = "enemy"
            if self.case >= MY_SHIFT_CASE:
                after = "shift"
            self._beat(label, value, after)

        def _pick_enemy_move(self):
            if self.dn_pending:
                return "solution"
            # DISCLOSE is its commonest move and that is the character: the
            # thing you are fighting spends most of its turns HELPING you, for
            # free, correctly.
            pool = ["disclose", "disclose", "testimony", "introduce"]
            if self.field <= 4:
                # The narrower you are, the more it wants to announce an
                # ending -- which is the decision the act is built around.
                pool += ["denouement", "denouement", "testimony"]
            elif self.turn >= 4:
                pool.append("denouement")
            if self.field <= MY_FIELD_MIN:
                pool = [m for m in pool if m != "disclose"] or ["testimony"]
            if self.case > 180:
                pool.append("alibi")
            if self.last_enemy in pool and len(set(pool)) > 1:
                pool = [m for m in pool if m != self.last_enemy] or pool
            return self.rng.choice(pool)

        def _fx_testimony(self, big=False):
            """Act one: a statement lands on the window that stands in for
            you -- the panel jolts, the light ripples out from it."""
            self.panel_kick = 1.0
            self._kick_lens(1004.0, 620.0, 0.7 if big else 0.4,
                            0.005 if big else 0.002)
            self.tear = max(self.tear, 0.45 if big else 0.25)

        def _step_enemy(self):
            self.mtick += 1
            if self.mtick < 26:
                self.windup = min(1.0, self.windup + 0.06)
                return

            self.doubt = min(float(MY_DOUBT_MAX),
                            self.doubt + self.rng.randint(MY_DOUBT_STEP_LO,
                                                        MY_DOUBT_STEP_HI))

            # THE CAPSTONE. Doubt full: certainty is the one thing it cannot
            # allow, so the case is REOPENED and the whole position goes.
            if self.doubt >= MY_DOUBT_MAX:
                self.doubt = float(MY_DOUBT_FLOOR)
                self.dn_pending = False
                self.last_enemy = "reopened"
                back = min(self.case, MY_REOPEN_CASE)
                self.case -= back
                before = self.field
                self._set_field(self.field + MY_REOPEN_FIELD, "reopen")
                self.play("break", 0.95)
                self.flash = 0.40
                self.shake = 1.0
                self.tear = 0.7
                # The bulb blows, and swings.
                self._kick_lamp(0.014, dip=1.0)
                dmg = MY_REOPEN_DMG
                if self.guard:
                    dmg = int(dmg * MY_GUARD_MULT)
                self.hurt(dmg, 1004, 600)
                self._fx_testimony(big=True)
                self.guard = False
                value = "FIELD  %d" % self.field
                if back:
                    value += "   +%d" % back
                self._beat("REOPENED", value, self._after_enemy(), kind="it")
                return

            move = self._pick_enemy_move()
            self.last_enemy = move
            label = move.upper()
            value = ""
            dmg = 0

            if move == "disclose":
                # It rules one out for you. Free, correct, and it costs you
                # nothing but the certainty it buys.
                before = self.field
                self._set_field(self.field - MY_DISCLOSE_FIELD, "it")
                self.doubt = min(float(MY_DOUBT_MAX),
                                self.doubt + MY_DISCLOSE_DOUBT)
                self.play("note", 0.85)
                self.flash = 0.10
                self.bulb_flare = 0.20
                value = "FIELD  %d" % self.field
                if self.field == before:
                    value = "TWO REMAIN"

            elif move == "testimony":
                # The narrower you are, the more it costs to hold it there.
                dmg = int(MY_TEST_BASE
                        + MY_TEST_PER * (MY_FIELD_MAX - self.field))

            elif move == "introduce":
                before = self.field
                self._set_field(self.field + (2 if self.turn >= 10 else 1), "reopen")
                dmg = MY_INTRO_DMG
                self.play("refuse", 0.7)
                self._kick_lamp(0.004)
                if self.field != before:
                    value = "FIELD  %d   " % self.field

            elif move == "alibi":
                back = min(self.case, MY_ALIBI_BACK)
                self.case -= back
                self.case_flash = 1.0
                self.play("refuse", 0.65)
                value = "+%d" % back

            elif move == "denouement":
                # Announced a full turn in advance, because it always is. The
                # lamp goes still for it (_step_hang reads dn_pending).
                self.dn_pending = True
                self.play("note", 0.95)
                self.flash = 0.12
                self.bulb_flare = 0.15
                value = "PENDING"

            elif move == "solution":
                # ...and it is not one. It costs most when you are closest to
                # having your own, and it puts the field back.
                self.dn_pending = False
                label = "SOLUTION"
                dmg = int(MY_DN_DMG_BASE
                        + MY_DN_DMG_PER * (MY_FIELD_MAX - self.field))
                before = self.field
                self._set_field(self.field + MY_DN_FIELD, "reopen")
                self.play("cut_big", 0.9)
                self.flash = 0.30
                self.shake = 0.8
                self._kick_lamp(0.012, flare=0.9)
                self._kick_lens(640.0, 300.0, 0.7, 0.005)
                if self.field != before:
                    value = "FIELD  %d   " % self.field

            if dmg > 0:
                if self.guard:
                    dmg = int(dmg * MY_GUARD_MULT)
                self.play("enemy", 0.8)
                self.hurt(dmg, 1004, 600)
                self._fx_testimony(big=(move == "solution"))
                value += "-%d" % dmg

            self.guard = False
            self._beat(label, value, self._after_enemy(), kind="it")

        def _after_enemy(self):
            if self.case >= MY_SHIFT_CASE or self.turn >= MY_SHIFT_TURN_CAP:
                return "shift"
            return "menu"

        # =====================================================================
        # THE TEAR -- the cord goes, and the field walks into the dark
        # =====================================================================
        #   1     WHAT CARRIES: the open frames, up to MY_BODIES_MAX of them
        #   24    FIELD n, and the frames that carry pulse
        #   40    the cord snaps; the bulb falls and breaks on the boards
        #   60    the panels go; the frames drop out of the lineup
        #   ~92   the figure becomes all holes, and the hole takes it
        #   170   the slam; act two's music; the lamp you carry comes up
        #   170+  the lineup is standing there, in a line, in the dark

        def _step_shift(self):
            self.mtick += 1
            t = self.mtick

            if t == 1:
                inv_music_stop(0.3)
                self.play("tear")
                # WHAT CARRIES. Not health, not leads -- the FIELD. Everything
                # you failed to rule out is about to be a thing in the room.
                opened = [f for f in self.lineup if f["open"]]
                take = opened[:MY_BODIES_MAX]
                for f in take:
                    f["carry"] = True
                self.carried = [f["glyph"] for f in take]
                self.field_carried = int(inv_clamp(len(self.carried),
                                                   MY_BODIES_MIN, MY_BODIES_MAX))
                # The readout says what walks in, not what was open: a frame
                # past MY_BODIES_MAX goes out with the crossed ones.
                self.field = self.field_carried
            if t == 24:
                # Off to the side: the bulb falls straight down the middle.
                self.float_text(930, 250, "FIELD  %d" % self.field_carried,
                                MY_PALE, True)
                self.play("scan", 0.9)
            if t == 40:
                # The cord goes.
                # It leaves on the tangent it was swinging along.
                bx, by = self.bulb_pos()
                th = self.hang_angle()
                w = 6.2831853 / MY_HANG_PERIOD
                omega = (MY_HANG_SWING * self.hang_idle * math.cos(self.clock * w)
                         * w * INV_TICK + self.hang_w)
                self.bulb_fall = {"x": bx, "y": by,
                                  "vx": math.cos(th) * omega * MY_HANG_LEN,
                                  "vy": -math.sin(th) * omega * MY_HANG_LEN}
                self.play("cut", 0.7)
            if 60 <= t < 150:
                self.panel_slide = inv_smooth((t - 60) / 90.0)
                self.shake = max(self.shake, 0.18)
            if t == 64:
                # The frames that carry drop out of the lineup into the dark;
                # the rest simply go out.
                for f in self.lineup:
                    if not f["carry"]:
                        continue
                    x, y = self.lineup_pos(f["glyph"])
                    vx = self.rng_fx.uniform(-1.6, 0.6)
                    vy = self.rng_fx.uniform(-2.5, -0.8)
                    vr = self.rng_fx.uniform(-5.0, 5.0)
                    d = self.rng_fx.randint(0, 14)
                    for tex, s in (("frame", MY_PLACARD), (my_glyph(f["glyph"]), MY_PLACARD * 0.92)):
                        self.fx.emit(tex, x, y, vx=vx, vy=vy, life=80, size=s,
                                     rot=0.0, vrot=vr, col=MY_PALE if tex != "frame" else MY_CHALK,
                                     alpha=0.95, add=False, ay=0.32, fade="late",
                                     delay=d, layer="hud")
            if self.bulb_gone:
                # Every light in the room is out.
                self.dark = inv_approach(self.dark, 0.88, 0.03)
                self.body_lit = max(0.0, self.body_lit - 0.01)
            if self.bulb_gone and t < 170:
                # It goes the way it came: the hole opens on it and it becomes
                # all holes.
                self.body_diss = min(1.0, self.body_diss + 1.0 / 60.0)
                self.body_ap = min(0.95, self.body_ap + 0.01)
                k = inv_clamp(self.body_diss * 1.6, 0.0, 1.0)
                self.hole[0], self.hole[1] = 640.0, 330.0
                self.hole[3] = k * (1.0 - inv_clamp((self.body_diss - 0.75) * 4.0, 0.0, 1.0))
                self.hole[2] = inv_lerp(40.0, 230.0, k)
            if t == 170:
                self.play("slam")
                self.play("phase", 0.9)
                self.shake = 1.0
                self.hole[3] = 0.0
                inv_music_corruptive()
                inv_heart_start(0.0)
                # Whole again for the second half: act one's currency was the
                # FIELD, and that is what carries.
                self.hp = MY_HP2_MAX
                self.leads = MY_LEADS_MAX
                self._populate()
            if 170 <= t < 250:
                self.open = inv_clamp((t - 170) / 80.0, 0.0, 1.0)
                # The room is not lit again. Only the lamp comes up.
                self.dark = inv_clamp(1.0 - (t - 170) / 80.0, 0.0, 1.0)
                self.lamp_s = inv_smooth((t - 170) / 80.0)
            if t == 250:
                self.open = 1.0
                self.dark = 0.0
                self.lamp_s = 1.0
                self._begin_dark()

        # =====================================================================
        # ACT TWO -- THE LINEUP IN THE DARK
        # =====================================================================

        def alive(self):
            return [b for b in self.bodies if b["leave"] <= 0.0]

        def uncrossed(self):
            return [b for b in self.bodies
                    if b["leave"] <= 0.0 and not b["crossed"]]

        def field_now(self):
            """How many readings are still open: the suspects not crossed off
            and not on their way out. Act one's word, act one's meaning."""
            return len(self.uncrossed())

        def _body(self, body_id):
            for b in self.bodies:
                if b["id"] == body_id:
                    return b
            return None

        def _dist(self, b):
            return math.hypot(b["x"] - self.px, b["y"] - self.py)

        def inside(self, b):
            """THE BELL'S OWN TEST: its feet inside the drawn rim."""
            return self._dist(b) <= self.lamp_r

        def lamp_level(self):
            return inv_clamp(self.lamp_s * (1.0 - 0.72 * self.lamp_dip), 0.0, 1.0)

        def light_at(self, x, y):
            """How much of your lamp falls on a point -- the shader's own
            falloff, so a figure is lit exactly as the boards under it."""
            d = math.hypot(x - self.px, y - self.py)
            r = max(self.lamp_r, 8.0)
            k = inv_clamp((d - r * 0.50) / (r * 0.54), 0.0, 1.0)
            return (1.0 - k * k * (3.0 - 2.0 * k)) * self.lamp_level()

        def bell_uniform(self):
            if self.mode != "dark" or self.bell_ring >= 1.0:
                return (0.0, 0.0, 0.0, 0.0)
            u = self.bell_ring
            x, y, r = self.bell_at
            return (float(x), float(y), float(r + 280.0 * inv_smooth(u)),
                    float((1.0 - u) * (1.0 - u) * 0.85))

        def count_uniform(self):
            """The countdown, drawn on the rim: .w how far round it has come,
            .x 1 when the stroke it is counting to reopens the case."""
            if self.mode != "dark":
                return (0.0, 0.0, 0.0, 0.0)
            frac = 1.0 - self.bell_t / float(max(1, self.bell_period))
            return (1.0 if self.strokes_left <= 1 else 0.0, 0.0, 0.0,
                    float(inv_clamp(frac, 0.002, 1.0)))

        def bell_warn(self):
            """0 until the ticking starts, 1 at the stroke."""
            if self.mode != "dark" or self.bell_t > MY_BELL_WARN:
                return 0.0
            return inv_clamp(1.0 - self.bell_t / float(MY_BELL_WARN), 0.0, 1.0)

        def _lamp_dust(self):
            """Dust hanging in your light. The stage draws it only where the
            light is (layer w_dust)."""
            ang = self.rng_fx.uniform(0.0, 6.2831853)
            rr = self.lamp_r * math.sqrt(self.rng_fx.random()) * 0.95
            self.fx.emit("dust", self.px + math.cos(ang) * rr,
                         self.py + math.sin(ang) * rr - self.rng_fx.uniform(0.0, 70.0),
                         vx=self.rng_fx.uniform(-0.15, 0.15),
                         vy=self.rng_fx.uniform(-0.12, 0.05),
                         life=self.rng_fx.randint(70, 130),
                         size=self.rng_fx.uniform(0.4, 1.0), col="#d2dcea",
                         alpha=self.rng_fx.uniform(0.25, 0.55), add=True,
                         drag=0.995, fade="inout", layer="w_dust")

        def _begin_dark(self, dev=False):
            self.mode = "dark"
            self.mtick = 0
            self.open = 1.0
            self.dark = 0.0
            self.lamp_s = 1.0
            self.lamp_r = MY_LAMP_R
            self.hp = MY_HP2_MAX
            self.hp_shown = float(MY_HP2_MAX)
            self.panel_slide = 1.0
            self.hole[3] = 0.0
            self.bulb_gone = True
            self.bell_t = MY_BELL_FIRST
            self.bell_period = MY_BELL_FIRST
            self.bell_ring = 1.0
            self.strokes_left = MY_REOPEN_STROKES

            if dev:
                if not self.carried:
                    n = int(inv_clamp(self.field, MY_BODIES_MIN, MY_BODIES_MAX))
                    pool = ([f["glyph"] for f in self.lineup if f["open"]]
                            + [f["glyph"] for f in self.lineup if not f["open"]])
                    self.carried = pool[:n]
                self.field_carried = int(inv_clamp(len(self.carried),
                                                   MY_BODIES_MIN, MY_BODIES_MAX))
                inv_music_corruptive()
                inv_heart_start(0.0)
                self._populate()
            # THE CHECKPOINT: a loss from here may be retried from here.
            self.checkpoint = {"slug": "mystery", "field": int(self.field_carried),
                               "glyphs": [int(v) for v in self.carried]}

        def _populate(self):
            """THE JOINT. Act one's field, standing in a line, facing you."""
            self.bodies = []
            self.body_seq = 0
            self.replace_q = []
            glyphs = list(self.carried)
            while len(glyphs) < MY_BODIES_MIN:
                glyphs.append(self._free_glyph(glyphs))
            n = len(glyphs)
            cx, cy = my_arena_center()
            gap = min(150.0, (MY_AR_W - 160.0) / max(1, n - 1))
            y = MY_AR_Y + 110.0
            for i, gl in enumerate(glyphs):
                self._add_body(gl, at=(cx + (i - (n - 1) * 0.5) * gap, y), rise=False)
            self.rng.choice(self.bodies)["subject"] = True
            self.hold = MY_LINE_HOLD
            self.px, self.py = cx, MY_AR_Y + MY_AR_H - 46.0
            self.trail = []

        def _free_glyph(self, extra=()):
            used = set(b["glyph"] for b in self.bodies) | set(extra)
            free = [i for i in range(len(INV_GLYPHS)) if i not in used]
            if free:
                return self.rng_fx.choice(free)
            return self.rng_fx.randrange(len(INV_GLYPHS))

        def _entry_point(self):
            """A point at the edge of the room, as far from you as can be had
            in a few tries -- a new reading never walks in on top of you."""
            best = None
            for _i in range(12):
                side = self.rng.randrange(4)
                if side == 0:
                    x, y = MY_AR_X + 24.0, self.rng.uniform(MY_AR_Y + 20, MY_AR_Y + MY_AR_H - 20)
                elif side == 1:
                    x, y = MY_AR_X + MY_AR_W - 24.0, self.rng.uniform(MY_AR_Y + 20, MY_AR_Y + MY_AR_H - 20)
                elif side == 2:
                    x, y = self.rng.uniform(MY_AR_X + 30, MY_AR_X + MY_AR_W - 30), MY_AR_Y + 20.0
                else:
                    x, y = self.rng.uniform(MY_AR_X + 30, MY_AR_X + MY_AR_W - 30), MY_AR_Y + MY_AR_H - 20.0
                d = math.hypot(x - self.px, y - self.py)
                if best is None or d > best[0]:
                    best = (d, x, y)
                if d >= 300.0:
                    break
            return (best[1], best[2])

        def _add_body(self, glyph=None, at=None, rise=True):
            self.body_seq += 1
            if glyph is None:
                glyph = self._free_glyph()
            if at is None:
                at = self._entry_point()
            x, y = at
            b = {"id": self.body_seq, "glyph": int(glyph), "subject": False,
                 "x": float(x), "y": float(y), "vx": 0.0, "vy": 0.0,
                 "ph": self.rng.uniform(0.0, 6.283),
                 "rate": self.rng.uniform(0.0035, 0.0068),
                 "seed": self.rng.uniform(0.0, 6.283),
                 "bspeed": self.rng.uniform(MY_BYS_SPEED_LO, MY_BYS_SPEED_HI),
                 "curious": 0, "crossed": False, "cross_t": -999,
                 "lift_t": -999, "solved_t": -999,
                 "break": 0, "bvx": 0.0, "bvy": 0.0, "touch_cd": 0,
                 "arrive": 0.0 if rise else 1.0, "leave": 0.0, "hurt": 0.0,
                 "step": self.rng_fx.random(), "born": self.tick}
            self.bodies.append(b)
            if rise:
                # It comes up through a hole in the boards (rule 4).
                self.fx.emit("glow", x, y, life=MY_ARRIVE_TICKS, size=0.55,
                             size1=0.25, col="#000000", alpha=0.9, add=False,
                             fade="inout", layer="w_floor", sq=0.36)
                self.fx.ring(x, y, 8.0, 34.0, life=MY_ARRIVE_TICKS, col=MY_CHALK,
                             alpha=0.55, layer="w_floor", tex="ring_soft",
                             squash=0.36)
                self.play("phase", 0.35)
            return b

        # ----- the population ---------------------------------------------------

        def _step_bodies(self):
            cx, cy = my_arena_center()
            heat = self.heat()
            alive = self.alive()
            gone = []
            for b in self.bodies:
                if b["hurt"] > 0.0:
                    b["hurt"] *= 0.90
                if b["leave"] > 0.0:
                    b["leave"] += 1.0 / MY_LEAVE_TICKS
                    if b["leave"] >= 1.0:
                        gone.append(b)
                    continue
                if b["arrive"] < 1.0:
                    b["arrive"] = min(1.0, b["arrive"] + 1.0 / MY_ARRIVE_TICKS)
                if b["touch_cd"] > 0:
                    b["touch_cd"] -= 1

                if b["break"] > 0:
                    # THE BREAK-AWAY. One impulse under friction, never a pan.
                    b["break"] -= 1
                    b["x"] += b["bvx"]
                    b["y"] += b["bvy"]
                    b["step"] += math.hypot(b["bvx"], b["bvy"]) / 34.0
                    b["bvx"] *= 0.905
                    b["bvy"] *= 0.905
                    b["x"], b["y"] = my_arena_clamp(b["x"], b["y"], 10.0)
                    continue
                if self.hold > 0 or b["arrive"] < 1.0:
                    # Standing in the line; rising out of the floor.
                    continue

                # The wander target rides a lissajous, so even an approach
                # never traces a line (the motion rule).
                ph = b["ph"] + self.tick * b["rate"]
                tx = cx + math.sin(ph) * MY_AR_W * 0.38 \
                    + math.sin(ph * 0.53 + b["seed"]) * 118.0
                ty = cy + math.cos(ph * 0.81 + b["seed"]) * MY_AR_H * 0.36 \
                    + math.sin(ph * 1.29) * 40.0
                if self.closing > 0:
                    # A wrong accusation: all of them, at once, at your light.
                    spd = (inv_lerp(MY_SUB_SPEED, MY_SUB_SPEED_HOT, heat)
                           if b["subject"] else b["bspeed"]) * MY_CLOSE_SPEED
                    tx = inv_lerp(tx, self.px, MY_CLOSE_PULL)
                    ty = inv_lerp(ty, self.py, MY_CLOSE_PULL)
                elif b["subject"]:
                    # It drifts toward your light. It does not charge and it
                    # never will -- it is slower than you are and it is not in
                    # a hurry.
                    spd = inv_lerp(MY_SUB_SPEED, MY_SUB_SPEED_HOT, heat)
                    tx = inv_lerp(tx, self.px, MY_SUB_PULL)
                    ty = inv_lerp(ty, self.py, MY_SUB_PULL)
                else:
                    spd = b["bspeed"]
                    if b["curious"] > 0:
                        b["curious"] -= 1
                        tx = inv_lerp(tx, self.px, MY_CURIOUS_PULL)
                        ty = inv_lerp(ty, self.py, MY_CURIOUS_PULL)
                    elif self.rng.random() < MY_CURIOUS_CHANCE:
                        b["curious"] = self.rng.randint(MY_CURIOUS_LEN[0],
                                                        MY_CURIOUS_LEN[1])

                dx, dy = tx - b["x"], ty - b["y"]
                d = math.hypot(dx, dy) or 1.0
                b["vx"] += (dx / d) * spd * 0.085
                b["vy"] += (dy / d) * spd * 0.085
                # A LINEUP KEEPS ITS SPACING: two suspects never stand close
                # enough that the rim could not be put between them.
                for o in alive:
                    if o is b:
                        continue
                    ox, oy = b["x"] - o["x"], b["y"] - o["y"]
                    od = math.hypot(ox, oy)
                    if 0.01 < od < MY_SEP:
                        push = (MY_SEP - od) / MY_SEP * 0.12
                        b["vx"] += ox / od * push
                        b["vy"] += oy / od * push
                b["vx"] *= 0.94
                b["vy"] *= 0.94
                sp = math.hypot(b["vx"], b["vy"])
                cap = spd * 1.2
                if sp > cap:
                    k = cap / sp
                    b["vx"] *= k
                    b["vy"] *= k
                    sp = cap
                b["x"] += b["vx"]
                b["y"] += b["vy"]
                b["x"], b["y"] = my_arena_clamp(b["x"], b["y"], 10.0)
                b["step"] += sp / 34.0

            if gone:
                self.bodies = [b for b in self.bodies if b not in gone]

            # A ruled-out reading is REPLACED, not removed: there is always
            # somebody else in the room -- act one's floor of two, honoured for
            # the whole of act two.
            if self.replace_q:
                self.replace_q = [n - 1 for n in self.replace_q]
                ready = [n for n in self.replace_q if n <= 0]
                self.replace_q = [n for n in self.replace_q if n > 0]
                for _r in ready:
                    if len(self.alive()) < MY_BODY_HARDCAP:
                        self._add_body()

        def _name_target(self):
            """Who an accusation would be aimed at: the nearest suspect in
            reach that is NOT crossed off, or failing that the nearest that
            is. Pure -- the stage calls it to draw the brackets."""
            best, bd = None, MY_NAME_R
            best_c, bdc = None, MY_NAME_R
            for b in self.bodies:
                if b["leave"] > 0.0 or b["arrive"] < 1.0:
                    continue
                d = self._dist(b)
                if b["crossed"]:
                    if d <= bdc:
                        best_c, bdc = b, d
                elif d <= bd:
                    best, bd = b, d
            return best or best_c

        # ----- act two's turn ----------------------------------------------------

        def _step_dark(self, edges):
            self.mtick += 1
            self.dist += 1.0
            held = edges["held"]

            if self.iframes > 0:
                self.iframes -= 1
            if self.name_cd > 0:
                self.name_cd -= 1
            if self.sweep_cd > 0:
                self.sweep_cd -= 1
            if self.hold > 0:
                self.hold -= 1
            if self.closing > 0:
                self.closing -= 1
            self.lamp_dip *= 0.93

            # --- THE LAMP -------------------------------------------------
            if edges["x"] and self.sweep_t <= 0 and self.sweep_cd <= 0:
                self.sweep_t = MY_SWEEP_TICKS
                self.sweep_cd = MY_SWEEP_CD
                self.play("scan", 0.85)
                self.flash = 0.08
                self.fx.ring(self.px, self.py, self.lamp_r, MY_SWEEP_R, life=16,
                             col=MY_LAMPC, alpha=0.45, layer="w_floor",
                             tex="ring_soft")
            if self.sweep_t > 0:
                self.sweep_t -= 1
                self.lamp_r = min(MY_SWEEP_R, self.lamp_r + 44.0)
                if self.sweep_t <= 0:
                    # ...and then your eyes are gone.
                    self.lamp_r = MY_LAMP_MIN
                    self.play("cancel", 0.4)
            else:
                self.lamp_r = min(MY_LAMP_R, self.lamp_r
                                + (MY_LAMP_R - MY_LAMP_MIN) / float(MY_SWEEP_BLIND))

            # --- ACCUSE ---------------------------------------------------
            # Aimed at the press and held on that one suspect: walking past a
            # second one mid-hold never changes who you are accusing.
            if edges["z"] and not self.naming and self.name_cd <= 0:
                tgt = self._name_target()
                if tgt is None:
                    self.play("cancel", 0.45)
                    self.name_cd = 12
                    self.audit["accuse_none"] += 1
                else:
                    self.naming = True
                    self.name_t = 0
                    self.name_target = tgt["id"]
                    self.play("wind", 0.5)
            if self.naming:
                b = self._body(self.name_target)
                if (not held["z"] or b is None or b["leave"] > 0.0
                        or self._dist(b) > MY_NAME_R * 1.35):
                    self.naming = False
                    self.name_t = 0
                    self.name_target = None
                    self.name_cd = 14
                else:
                    self.name_t += 1
                    if self.name_t >= MY_NAME_TICKS:
                        self.naming = False
                        self.name_t = 0
                        self.name_target = None
                        self._resolve_accuse(b)
                        if self.mode != "dark":
                            return

            # --- moving ----------------------------------------------------
            mx = (1 if held["right"] else 0) - (1 if held["left"] else 0)
            my = (1 if held["down"] else 0) - (1 if held["up"] else 0)
            if mx or my:
                # Naming roots you. It does not freeze you -- a fight that
                # takes the controls away is a fight that is doing something
                # to you rather than with you -- but you creep.
                spd = MY_NAME_DRIFT if self.naming else MY_SPEED
                n = math.hypot(mx, my) or 1.0
                self.px += (mx / n) * spd
                self.py += (my / n) * spd
                self.px, self.py = my_arena_clamp(self.px, self.py, MY_PLAYER_R)
                self.trail.append((self.px, self.py))
                if len(self.trail) > 26:
                    self.trail.pop(0)

            self._step_bodies()
            self._step_contact()
            self._step_dread()
            self._step_bell()

        # ----- the bell ----------------------------------------------------------

        def _bell_period(self):
            return int(inv_lerp(MY_BELL_EVERY, MY_BELL_EVERY_HOT, self.heat()))

        def _reopen_strokes(self):
            return MY_REOPEN_STROKES if self.heat() < 0.5 else MY_REOPEN_STROKES_HOT

        def _step_bell(self):
            if self.bell_ring < 1.0:
                self.bell_ring = min(1.0, self.bell_ring + 1.0 / MY_BELL_RING)
            self.verdict_t += 1
            self.bell_t -= 1
            # THE REOPENING IS ON THE BELL, and it is announced from the edges
            # of the room inward for the whole of its last 150 ticks.
            if self.strokes_left <= 1 and self.bell_t <= 150:
                self.reopen_warn = inv_clamp(1.0 - self.bell_t / 150.0, 0.0, 1.0)
                if self.bell_t == 150:
                    self.play("wind2", 0.7)
            else:
                self.reopen_warn = 0.0
            if 0 < self.bell_t <= MY_BELL_WARN and self.bell_t % 21 == 0:
                self.play("text", 2.0)
            if self.bell_t > 0:
                return
            self.bell_period = self._bell_period()
            self.bell_t = self.bell_period
            self.strokes_left -= 1
            if self.strokes_left <= 0:
                self._reopen_case()
            else:
                self._ring_bell()

        def _ring_bell(self):
            """ONE TRUE THING: whether the subject's feet are inside your rim.

            Every suspect still open whose own state does not match is crossed
            off. Never below two: at two it refuses outright, and a verdict that
            would leave one is withheld, leaving the mismatch nearest the rim
            uncrossed -- which side the other crosses fell on still says what
            the verdict was, to anyone who watched."""
            sub = self.subject()
            U = self.uncrossed()
            r = self.lamp_r
            self.bell_at = (self.px, self.py, r)
            self.bell_ring = 0.0
            self.audit["strokes"] += 1
            self.strokes.append({"x": self.px, "y": self.py, "r": r,
                                 "t": self.tick, "void": False})
            del self.strokes[:-MY_STROKE_KEEP]

            crossed = []
            truth = None if sub is None else self.inside(sub)
            if sub is None or len(U) <= 1:
                verdict = "STILL OPEN"
            elif len(U) == 2:
                verdict = "TWO REMAIN"
                self.audit["refusals"] += 1
            else:
                M = [b for b in U if self.inside(b) != truth]
                if len(U) - len(M) <= 1:
                    keep = min(M, key=lambda b: abs(self._dist(b) - r))
                    M = [b for b in M if b is not keep]
                    verdict = "TWO REMAIN"
                    self.audit["withheld"] += 1
                else:
                    verdict = "SEEN" if truth else "UNSEEN"
                for b in M:
                    b["crossed"] = True
                    b["cross_t"] = self.tick
                    crossed.append(b["id"])
                    if b["subject"]:
                        self.audit["bad_cross"] += 1
                self.audit["crossed"] += len(M)
            if self.field_now() < min(2, len(U)):
                self.audit["below_two"] += 1
            self.last_stroke = {"tick": self.tick, "verdict": verdict,
                                "truth": truth, "U": [b["id"] for b in U],
                                "crossed": crossed, "r": r,
                                "inside": [b["id"] for b in U if self.inside(b)]}
            self.verdict = verdict
            self.verdict_t = 0

            self.play("note", 0.95)
            if verdict in ("TWO REMAIN", "STILL OPEN"):
                self.play("cancel", 0.5)
            elif crossed:
                self.play("graze", 0.55)
            self._kick_lens(self.px, self.py, 0.22)
            col = {"SEEN": MY_GOLD, "UNSEEN": MY_PALE,
                   "TWO REMAIN": MY_WARN}.get(verdict, MY_DIM)
            # Over the light, where the eyes are -- or under it when the light
            # is up against the top of the room and the chrome.
            fy = self.py - min(r, 150.0) - 34.0
            if fy < 104.0:
                fy = self.py + min(r, 150.0) + 34.0
            self.float_text(self.px, fy, verdict, col, True)
            fh = MY_FIG_H * MY_FIG_ZOOM2
            for bid in crossed:
                b = self._body(bid)
                if b is None:
                    continue
                self.fx.burst("dust", b["x"], b["y"] - fh - 18.0, 8,
                              speed=(0.4, 1.8), life=(14, 28), size=(0.6, 1.3),
                              col=MY_PALE, alpha=0.75, add=True, drag=0.9,
                              layer="w_front")

        def _reopen_case(self, exclude=None, quiet=False):
            """Every cross lifts, and it is somebody else now."""
            for b in self.bodies:
                if b["crossed"]:
                    b["crossed"] = False
                    b["lift_t"] = self.tick
            for s in self.strokes:
                s["void"] = True
            self._reroll_subject(exclude)
            self.reopen_warn = 0.0
            self.reopen_flash = 1.0
            self.audit["reopens"] += 1
            self.strokes_left = self._reopen_strokes()
            self.verdict = "REOPENED"
            self.verdict_t = 0
            if not quiet:
                self.play("break", 0.7)
                self.flash = max(self.flash, 0.20)
                self.shake = max(self.shake, 0.45)
                self.tear = max(self.tear, 0.45)
                self._kick_lens(self.px, self.py, 0.5, 0.004)

        def _reroll_subject(self, exclude=None):
            cur = self.subject()
            alive = self.alive()
            pool = [b for b in alive if b["id"] != exclude and b is not cur]
            if not pool:
                pool = [b for b in alive if b["id"] != exclude] or alive
            if not pool:
                return
            if cur is not None:
                cur["subject"] = False
            self.rng.choice(pool)["subject"] = True

        # ----- contact, dread, accusation ---------------------------------------

        def _step_contact(self):
            """THE ONE THING IN HERE THAT HURTS: the subject reaching you. A
            bystander only startles and goes."""
            for b in self.bodies:
                if (b["leave"] > 0.0 or b["arrive"] < 1.0 or b["touch_cd"] > 0
                        or b["break"] > 0):
                    continue
                d = self._dist(b)
                if d > MY_TOUCH_R + MY_PLAYER_R:
                    continue
                b["touch_cd"] = 44
                dx, dy = b["x"] - self.px, b["y"] - self.py
                n = math.hypot(dx, dy) or 1.0
                if b["subject"]:
                    if self.iframes > 0:
                        continue
                    self.audit["contacts"] += 1
                    self.iframes = MY_IFRAMES
                    self.hurt(MY_HIT_HP, self.px, self.py - 60)
                    self.play("struck", 0.7)
                    self.px -= (dx / n) * 26.0
                    self.py -= (dy / n) * 26.0
                    self.px, self.py = my_arena_clamp(self.px, self.py, MY_PLAYER_R)
                    self.lamp_dip = 1.0
                    b["hurt"] = 1.0
                    self.tear = max(self.tear, 0.35)
                    self._kick_lens(self.px, self.py, 0.7, 0.006)
                    self.fx.burst("spark", self.px + dx / n * 14.0,
                                  self.py + dy / n * 14.0 - 10.0, 14,
                                  speed=(2.0, 7.0), life=(10, 20), size=(0.25, 0.55),
                                  col="#ff5a6a", alpha=0.95, add=True, drag=0.86,
                                  stretch=0.35, layer="w_front")
                    # AND THEN IT LEAVES. It is not attacking you, it is
                    # passing through you -- and without the break-away a
                    # player who stops moving is farmed through the i-frames.
                    ang = math.atan2(dy, dx)
                    b["break"] = 34
                    b["bvx"] = math.cos(ang) * MY_BREAK_SPEED * 0.62
                    b["bvy"] = math.sin(ang) * MY_BREAK_SPEED * 0.62
                else:
                    b["break"] = 22
                    b["bvx"] = (dx / n) * 5.4
                    b["bvy"] = (dy / n) * 5.4
                    self.play("graze", 0.6)
                    self.fx.burst("dust", b["x"], b["y"] - 30.0, 6,
                                  speed=(0.4, 1.6), life=(14, 26), size=(0.6, 1.2),
                                  col=MY_CHALK, alpha=0.6, add=True, drag=0.9,
                                  layer="w_front")

        def _step_dread(self):
            sub = self.subject()
            target = 0.0
            if sub is not None and sub["break"] <= 0 and sub["leave"] <= 0.0:
                d = self._dist(sub)
                target = inv_clamp(
                    (MY_DREAD_NEAR - d) / (MY_DREAD_NEAR - MY_DREAD_FULL),
                    0.0, 1.0)
            # It has to LAG -- an instantaneous readout would be a distance
            # meter with a number filed off -- but it also has to answer the
            # question it is asked, "is it this one", inside a second.
            self.dread_v = inv_approach(self.dread_v, target, 0.05)
            inv_heart_level(0.14 + 0.62 * self.dread_v)

        def _resolve_accuse(self, b):
            """Act one's verb, resolved against what is actually there. There
            is no wasted accusation and there is no final one until the last."""
            fh = MY_FIG_H * MY_FIG_ZOOM2
            hx, hy = b["x"], b["y"] - fh - 18.0
            if b["subject"]:
                self.solve = min(MY_SOLVE_MAX, self.solve + MY_SOLVE_GAIN)
                self.solves += 1
                self.audit["solves"] += 1
                if self.hp < MY_HP2_MAX:
                    healed = min(MY_SOLVE_HEAL, MY_HP2_MAX - self.hp)
                    self.hp += healed
                    self.float_text(self.px + 54, self.py - 48, "+%d" % healed,
                                    MY_PALE)
                self.play("crit", 0.95)
                self.flash = 0.40
                self.shake = 0.75
                b["hurt"] = 1.0
                b["solved_t"] = self.tick
                self._kick_lens(b["x"], b["y"] - fh * 0.5, 0.8, 0.006)
                self.fx.ring(b["x"], b["y"], 10.0, 130.0, life=30, col=MY_GOLD,
                             alpha=0.9, layer="w_floor", squash=0.36)
                self.fx.burst("spark", b["x"], b["y"] - fh * 0.5, 20,
                              speed=(3.0, 10.0), life=(12, 26), size=(0.3, 0.7),
                              col="#f2d491", alpha=1.0, add=True, drag=0.87,
                              stretch=0.4, layer="w_front")
                self.float_text(hx, hy - 26, "SOLVED", MY_GOLD, True)
                if self.solve >= MY_SOLVE_MAX:
                    self.solved_id = b["id"]
                    self._begin_leave(True)
                    return
                # It breaks away, and the case reopens -- the same rule act
                # one taught, and the reason a landed hit does not simplify
                # the room.
                ang = (math.atan2(b["y"] - self.py, b["x"] - self.px)
                       + self.rng.uniform(-0.6, 0.6))
                b["break"] = 46
                b["bvx"] = math.cos(ang) * MY_BREAK_SPEED
                b["bvy"] = math.sin(ang) * MY_BREAK_SPEED
                self._reopen_case(exclude=b["id"], quiet=True)
                # THE FIELD WIDENS BY ONE -- act one's law.
                if len(self.alive()) + len(self.replace_q) < MY_BODY_HARDCAP:
                    self.replace_q.append(70)
                self.name_cd = MY_NAME_CD
            else:
                # RULED OUT. True, permanent, and not the win. It leaves the
                # way it came; a new reading walks in later.
                self.audit["ruled_out"] += 1
                b["leave"] = 0.001
                self.ruleouts.append({"x": b["x"], "y": b["y"], "t": self.tick})
                del self.ruleouts[:-8]
                self.replace_q.append(MY_REPLACE_DELAY)
                self.name_cd = MY_NAME_CD_MISS
                self.play("refuse", 0.85)
                self.play("wind2", 0.6)
                self.flash = 0.10
                self.tear = max(self.tear, 0.4)
                self.float_text(hx, hy - 26, "RULED OUT", MY_CHALK, True)
                back = min(self.solve, MY_SOLVE_MISS)
                if back > 0.0:
                    self.solve -= back
                    self.solve_flash = 1.0
                    self.float_text(hx, hy - 2, "-%d" % int(back), MY_RED)
                # ...and the room turns on you. Every one of them flinches
                # toward the light at once.
                self.closing = MY_CLOSE_TICKS
                for o in self.alive():
                    o["hurt"] = max(o["hurt"], 0.5)
                    o["curious"] = 0
                self.fx.burst("dust", b["x"], b["y"] - fh * 0.5, 12,
                              speed=(0.5, 2.4), life=(20, 40), size=(0.7, 1.5),
                              col=MY_PALE, alpha=0.7, add=True, drag=0.92,
                              jitter=14.0, layer="w_front")

        # =====================================================================
        # DEPARTURE
        # =====================================================================

        def _begin_leave(self, won):
            self.mode = "leave_w" if won else "leave_l"
            self.mtick = 0
            self.closing = 0
            self.naming = False
            self.name_t = 0
            self.name_target = None
            self.shake = 0.0
            self.reopen_warn = 0.0
            self.hud_fade = 1.0
            self.field_fade = 1.0
            self.end_close = 0.0
            self.lattice_off = 0.0
            self.end_show = 0.0
            self.body_diss = 0.0
            self.dread_v = 0.0
            self.bell_ring = 1.0
            self.sweep_t = 0
            self.end_order = []
            if won:
                sub = self._body(self.solved_id) or self.subject()
                if sub is not None:
                    self.solved_id = sub["id"]
                    others = [b for b in self.alive() if b is not sub]
                    others.sort(key=lambda o: -math.hypot(o["x"] - sub["x"],
                                                          o["y"] - sub["y"]))
                    self.end_order = [o["id"] for o in others]
            inv_music_stop(3.0 if won else 1.8)
            # No sting either way. A victory chime would be the funniest thing
            # in the encounter.

        def _step_leave(self):
            """Neither ending is a spectacle and neither one settles anything.

            WON -- the rest of the field goes, one at a time, until the readout
            says the one thing it never would: FIELD 1. For the first and only
            time the thing is fully lit, standing where you said it was. Then
            it opens -- the apertures grow until there is nothing between them
            -- and the hole takes it, and what is left for a long moment is the
            chalk on the boards: where your light was, every time the bell
            rang, none of it meeting anything.

            LOST -- you are not killed. THE LAMP GOES OUT. The radius closes,
            the last thing inside it is the subject standing next to you, every
            cross lifts, and then the room is black for longer than is
            comfortable.
            """
            self.mtick += 1
            t = self.mtick
            won = (self.mode == "leave_w")

            # Whatever was already on its way out keeps going.
            gone = []
            for b in self.bodies:
                if b["hurt"] > 0.0:
                    b["hurt"] *= 0.90
                if b["leave"] > 0.0:
                    b["leave"] += 1.0 / MY_LEAVE_TICKS
                    if b["leave"] >= 1.0:
                        gone.append(b)
                elif b["break"] > 0:
                    b["break"] -= 1
                    b["x"] += b["bvx"]
                    b["y"] += b["bvy"]
                    b["bvx"] *= 0.905
                    b["bvy"] *= 0.905
                    b["x"], b["y"] = my_arena_clamp(b["x"], b["y"], 10.0)
            if gone:
                self.bodies = [b for b in self.bodies if b not in gone]

            if won:
                # 0-90     the rest of the field goes, one by one: FIELD 1
                # 90-180   it is lit, all of it, once
                # 180-270  it opens, and the hole takes the rest
                # 270-430  the chalk alone, in an empty room
                sub = self._body(self.solved_id)
                if t == 1:
                    self.play("phase", 0.7)
                    inv_heart_stop(1.4)
                for i, bid in enumerate(self.end_order):
                    if t == 8 + i * 12:
                        b = self._body(bid)
                        if b is not None and b["leave"] <= 0.0:
                            b["leave"] = 0.001
                            self.play("graze", 0.5)
                self.hud_fade = max(0.0, 1.0 - t / 50.0)
                if t < 90:
                    self.lamp_r = inv_lerp(self.lamp_r, 230.0, 0.04)
                    if sub is not None:
                        # Your light comes to rest on it.
                        self.px = inv_lerp(self.px, sub["x"], 0.035)
                        self.py = inv_lerp(self.py, sub["y"] + 34.0, 0.035)
                elif t < 180:
                    self.end_show = inv_smooth((t - 90) / 90.0)
                    if t == 94:
                        self.play("scan", 0.9)
                        self.flash = 0.25
                elif t < 270:
                    u = inv_smooth((t - 180) / 90.0)
                    self.end_show = 1.0
                    self.body_diss = u
                    if sub is not None:
                        self.hole[0] = sub["x"]
                        self.hole[1] = sub["y"] - MY_FIG_H * MY_FIG_ZOOM2 * 0.5
                    self.hole[3] = 1.0 - abs(u - 0.5) * 2.0
                    self.hole[2] = inv_lerp(30.0, 170.0, u)
                    self.field_fade = max(0.0, 1.0 - u)
                    if t == 182:
                        self.play("break", 0.55)
                else:
                    self.hole[3] = 0.0
                    self.end_show = 0.0
                    if sub is not None:
                        self.bodies = [b for b in self.bodies if b is not sub]
                    # THE CHALK ALONE. Held a beat and a half longer than is
                    # comfortable, which is the house rule for these endings.
                    self.lamp_s = max(0.0, self.lamp_s - 0.020)
                    if t > 340:
                        self.dark = inv_clamp(self.dark + 0.013, 0.0, 1.0)
                if t > 430:
                    self.result = "victory"

            else:
                # 0-40     everything stops
                # 40-260   the lamp closes, and the last thing in it is near
                # 260-400  every cross lifts; the chalk goes out
                # 400+     black, held far longer than is comfortable
                if t == 1:
                    self.play("cut", 0.6)
                if 40 <= t < 260:
                    u = (t - 40) / 220.0
                    self.end_close = u
                    self.lamp_r = inv_lerp(MY_LAMP_R, 14.0, inv_smooth(u))
                    self.hud_fade = max(0.0, 1.0 - u * 1.5)
                    self.field_fade = self.hud_fade
                    # The subject closes the last of the distance at walking
                    # pace, and then simply stands there.
                    sub = self.subject()
                    if sub is not None and u < 0.72:
                        dx, dy = self.px - sub["x"], self.py - sub["y"]
                        n = math.hypot(dx, dy) or 1.0
                        if n > 46.0:
                            sub["x"] += (dx / n) * 0.9
                            sub["y"] += (dy / n) * 0.9
                            sub["step"] += 0.9 / 34.0
                    if t == 250:
                        inv_heart_stop(0.5)
                if t == 260:
                    self.play("slam", 0.45)
                    for b in self.bodies:
                        if b["crossed"]:
                            b["crossed"] = False
                            b["lift_t"] = self.tick
                if t >= 260:
                    self.end_close = 1.0
                    self.lamp_s = max(0.0, self.lamp_s - 0.035)
                    self.lattice_off = inv_clamp((t - 260) / 140.0, 0.0, 1.0)
                if t >= 400:
                    self.dark = inv_clamp(self.dark + 0.011, 0.0, 1.0)
                if t > 500:
                    self.result = "defeat"

# --- THE STAGE ---------------------------------------------------------------
init python:
    class MYStage(renpy.Displayable):
        """One CDD. Steps MYGame at a fixed 60Hz inside render() and paints the
        whole encounter through InvPaint and the shared lens (inv_kit.rpy)."""

        _tf_cache = {}

        PANEL_CMD = (40, 548, 470, 148)
        PANEL_HUD = (770, 548, 470, 148)

        # A case file: chalk on black, ticked corners, a faint ruled inset.
        STYLE_PANEL = {"top": "#0a0c12e8", "bot": "#05060af2",
                       "edge": "#9aa6b4c8", "accent": "#dce4eeff",
                       "border": 1.2, "cut": 6.0, "inset": 6.0,
                       "inset_a": 0.10, "noise": 0.10, "scan": 0.0,
                       "split": 0.0, "ticks": 1.0}
        STYLE_PLATE = {"top": "#05060ab4", "bot": "#05060ad4",
                       "edge": "#9aa6b460", "accent": "#dce4eeff",
                       "border": 1.0, "cut": 4.0, "inset": 4.0,
                       "inset_a": 0.0, "noise": 0.08, "scan": 0.0,
                       "split": 0.0, "ticks": 1.0}

        def __init__(self, game, **kwargs):
            super(MYStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0

        def _tf(self, key, builder):
            tf = MYStage._tf_cache.get(key)
            if tf is None:
                if len(MYStage._tf_cache) > 600:
                    MYStage._tf_cache.clear()
                tf = builder()
                MYStage._tf_cache[key] = tf
            return tf

        def _body_plain(self, zoom, alpha=1.0):
            ab = int(inv_clamp(alpha, 0.0, 1.0) * 6)
            key = ("plain", round(zoom, 3), ab)

            def build():
                kw = dict(zoom=zoom, subpixel=True)
                if ab < 6:
                    kw["alpha"] = ab / 6.0
                return Transform(MY_SPRITE, **kw)
            return self._tf(key, build)

        def event(self, ev, x, y, st):
            self.game.keys.handle_event(ev)
            return None

        # ----- render ------------------------------------------------------------

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

            in_dark = (g.open > 0.5)

            self._room(g, p, sx, sy)
            if in_dark:
                self._dark_world(g, p, sx, sy)
            else:
                self._room_world(g, p, sx, sy)

            p.to_hud()
            if in_dark:
                self._dark_hud(g, p)
            else:
                self._room_hud(g, p, sx, sy)
            self._floats(g, p, sx, sy)
            inv_fx_paint(p, g.fx, "hud")
            if g.paused:
                self._pause(g, p)

            rv = inv_compose(p, self._look(g), g.clock)

            # THE DRAW RATE IS THE TICK RATE. Every pixel above is a pure
            # function of the simulation state, so between two 1/60s ticks
            # this stage paints a byte-identical picture; asking for the next
            # frame at once made a high-refresh panel draw everything two to
            # four times a tick and throw the extras away. Same governor as
            # every stage (kototouhou.rpy has the long note).
            if g.result is None and not g.paused:
                renpy.redraw(self, max(0.0, INV_TICK - self.acc))
            return rv

        def _look(self, g):
            """Cold chalk and one warm thing. The bulb and the bell are what
            bloom; dread closes the frame and pulls the colour out."""
            o = inv_clamp(g.open, 0.0, 1.0)
            d = inv_clamp(g.dread_v, 0.0, 1.0)
            shock = (0.0, 0.0, 0.0, 0.0)
            if g.shock[3] > 0.004:
                shock = (g.shock[0], g.shock[1], g.shock[2], g.shock[3])
            return {
                "grade": (1.0 + 0.04 * o, inv_lerp(1.06, 1.10, o) + 0.08 * d,
                          inv_lerp(0.66, 0.74, o) - 0.16 * d, 0.30),
                "lift": (inv_lerp(0.010, 0.006, o), inv_lerp(0.012, 0.008, o),
                         inv_lerp(0.020, 0.016, o)),
                "gain": (1.0, 1.0, inv_lerp(1.04, 1.0, o)),
                "bloom": inv_lerp(0.50, 0.40, o),
                "thresh": inv_lerp(0.55, 0.52, o),
                "ca": 0.0012 + 0.003 * d + g.ca,
                "grain": inv_lerp(0.045, 0.055, o) + 0.02 * d,
                "vig": inv_lerp(0.45, 0.30, o),
                "vigr": 1.05,
                "barrel": inv_lerp(0.018, 0.010, o),
                "shock": shock,
                "tear": (inv_clamp(g.tear, 0.0, 1.0), float(g.tick // 3),
                         0.5 + 0.3 * math.sin(g.clock * 2.3), 0.5),
            }

        # ----- the room ------------------------------------------------------------

        def _room(self, g, p, sx, sy):
            global MY_LAMP_OK
            if MY_LAMP_OK:
                try:
                    bx, by = g.bulb_pos()
                    bell = g.bell_uniform()
                    if bell[3] > 0.0:
                        bell = (bell[0] + sx, bell[1] + sy, bell[2], bell[3])
                    # Two textures: the substrate (tex0) and the boards (tex1,
                    # repeating) -- a Model, as Horror's and Nonfiction's rooms.
                    m = (Model((1280, 720))
                         .texture(inv_disp(MY_SOUP_IMG))
                         .texture(inv_disp(inv_fx_img("tex_boards")),
                                  texture_wrap=(_MY_GL_REPEAT, _MY_GL_REPEAT))
                         .shader("renpy.texture")
                         .shader("inv.lamp")
                         .uniform("u_my_res", (1280.0, 720.0))
                         .uniform("u_my_time", float(g.clock))
                         .uniform("u_my_open", float(g.open))
                         .uniform("u_my_dark", float(g.dark))
                         .uniform("u_my_flash", float(g.flash))
                         .uniform("u_my_dread", float(g.dread_v))
                         .uniform("u_my_reopen", float(g.reopen_warn))
                         .uniform("u_my_heat", float(g.heat()))
                         .uniform("u_my_hole", (float(g.hole[0]), float(g.hole[1]),
                                                float(g.hole[2]), float(g.hole[3])))
                         .uniform("u_my_lamp", (float(g.px + sx), float(g.py + sy),
                                                float(g.lamp_r), float(g.lamp_level())))
                         .uniform("u_my_hang", (float(bx + sx), float(by + sy),
                                                float(g.pool_x() + sx), float(g.bulb_level())))
                         .uniform("u_my_bell", tuple(float(v) for v in bell))
                         .uniform("u_my_count", tuple(float(v) for v in g.count_uniform())))
                    r = renpy.render(m, 1280, 720, p.st, p.at)
                    p.blit(r, (0, 0))
                    return
                except Exception as e:
                    MY_LAMP_OK = False
                    try:
                        renpy.log("INV FX: lamp render failed: %r" % e)
                    except Exception:
                        pass
            p.fill(MY_BLACK, 0, 0, 1280, 720)

        # ----- the body --------------------------------------------------------

        def _lacuna(self, g, zoom, t, shear=1.0, ap=0.35, lit=0.2, band=0.4,
                    diss=0.0, hurt=0.0, tint=(1.0, 1.0, 1.0, 0.0),
                    stretch=(1.0, 1.0)):
            """The figure through inv.lacuna, as a displayable plus the padded
            plate's size."""
            plate_zoom = min(zoom, MY_PLATE_MAX_ZOOM)
            extra = zoom / plate_zoom
            # A WIDE MARGIN, because this body does not stay inside its own
            # silhouette: the strata slide sideways and the apertures
            # overshoot it.
            plate, W, H = inv_body_plate(MY_SPRITE, MY_SPRITE_W, MY_SPRITE_H,
                                        plate_zoom, pad_x=1.90, pad_y=1.50)
            body = None
            if MY_LACUNA_OK:
                try:
                    body = Transform(
                        plate, mesh=True, shader="inv.lacuna",
                        u_lac_res=(float(W), float(H)),
                        u_lac_t=float(t),
                        u_lac_shear=float(shear),
                        u_lac_ap=float(ap),
                        u_lac_band=float(band),
                        u_lac_lit=float(lit),
                        u_lac_stretch=(float(stretch[0]), float(stretch[1])),
                        u_lac_pivot=0.90,
                        u_lac_hurt=float(hurt),
                        u_lac_diss=float(diss),
                        u_lac_tint=tuple(float(v) for v in tint))
                    if extra > 1.01:
                        body = Transform(body, zoom=extra, subpixel=True)
                except Exception:
                    body = None
            if body is None:
                body = self._body_plain(zoom)
            return body, int(W * extra), int(H * extra)

        def _draw_body(self, g, p, cx, cy, zoom, t=None, alpha=1.0, **kw):
            body, w, h = self._lacuna(g, zoom, g.clock if t is None else t, **kw)
            if alpha < 0.99:
                body = Transform(body, alpha=inv_clamp(alpha, 0.0, 1.0))
            # The figure is off-centre in its own canvas; put the FIGURE where
            # the caller asked, not the canvas.
            cx = cx + MY_FIG_DX * zoom
            cy = cy + MY_FIG_DY * zoom
            try:
                r = renpy.render(body, w + 8, h + 8, p.st, p.at)
                rw, rh = r.get_size()
                p.sblit(r, (cx - rw * 0.5, cy - rh * 0.5))
            except Exception:
                pass

        def _draw_heart(self, g, p, cx, cy, alpha=1.0):
            """You. The same SOUL heart as every other corruptive state -- and
            in here the only object you can always find."""
            plate, W, H = inv_body_plate(INV_HEART, INV_HEART_W, INV_HEART_H,
                                        MY_HEART_ZOOM, pad_x=2.2, pad_y=2.2,
                                        nearest=True)
            squeeze = 1.0 - 0.20 * g.beat_pulse
            if INV_FLESH_OK:
                try:
                    d = inv_flesh(plate, W, H, g.clock * 2.6,
                                warp=MY_HEART_WARP, split=0.9,
                                stretch=(1.0 / max(0.5, squeeze), squeeze),
                                pivot=0.5, hurt=0.0, diss=0.05)
                    if alpha < 0.99:
                        d = Transform(d, alpha=alpha)
                    r = renpy.render(d, W, H, p.st, p.at)
                    w, h = r.get_size()
                    p.sblit(r, (cx - w * 0.5, cy - h * 0.5))
                    return
                except Exception:
                    pass
            heart = self._tf(("heartplain",),
                             lambda: Transform(INV_HEART, zoom=MY_HEART_ZOOM,
                                               nearest=True, subpixel=True))
            r, (w, h) = p.tex(("heartplain",), heart, 160, 160)
            p.sblit(r, (cx - w * 0.5, cy - h * 0.5))

        def _placard(self, p, x, y, glyph, s, alpha, crossed=False, cross_age=999,
                     how="you", lift_age=999, inside=0.0):
            """An empty picture frame with a reading's glyph in it -- the one
            object both acts share. Crossed off in chalk (gold when the
            Archivist did it), a red flash when a cross lifts, and a gold frame
            while its feet are inside your rim."""
            if alpha <= 0.02:
                return
            fa = alpha * (0.42 if crossed else 1.0)
            if inside > 0.01 and not crossed:
                p.glow(x, y, 24.0, 28.0, col=MY_GOLD, alpha=0.32 * inside * alpha,
                       add=True)
            fcol = MY_GOLD if (inside > 0.01 and not crossed) else MY_CHALK
            p.quad("frame", x, y, s, s, col=fcol, alpha=fa, add=False)
            p.quad(my_glyph(glyph), x, y, s * 0.92, s * 0.92,
                   col=(MY_FAINT if crossed else MY_PALE), alpha=fa, add=False)
            if crossed:
                k = inv_clamp(cross_age / 8.0, 0.0, 1.0)
                cs = s * 1.9 * (1.45 - 0.45 * k)
                ccol = MY_GOLD if how == "it" else MY_PALE
                p.quad("chalk_x", x, y, cs, cs, col=ccol, alpha=alpha * 0.92,
                       add=False)
                if cross_age < 14:
                    p.glow(x, y, 26.0, col=ccol,
                           alpha=0.6 * (1.0 - cross_age / 14.0) * alpha, add=True)
            elif lift_age < 40:
                u = lift_age / 40.0
                p.glow(x, y, 24.0, col=MY_RED, alpha=0.75 * (1.0 - u) * alpha,
                       add=True)
                if lift_age < 20:
                    cs = s * 1.9
                    p.quad("chalk_x", x, y, cs, cs, col=MY_RED,
                           alpha=alpha * (1.0 - lift_age / 20.0), add=False)

        def _plate(self, p, x, y, w, h, style, alpha=1.0):
            """inv_draw_panel with an alpha, for chrome that fades."""
            if alpha <= 0.02:
                return
            if alpha >= 0.98:
                inv_draw_panel(p, x, y, w, h, style)
                return
            aq = int(alpha * 16.0 + 0.5) / 16.0
            base = inv_panel(w, h, style)
            key = ("plate", id(base), aq)
            d = self._tf(key, lambda: Transform(base, alpha=aq))
            r, _sz = p.tex(key, d, int(w), int(h))
            p.blit(r, (x, y))

        # ----- ACT ONE: the room -------------------------------------------------

        def _room_world(self, g, p, sx, sy):
            arriving = (g.mode == "arrive")
            doubt = g.doubt_frac()
            bx, by = g.bulb_pos()
            pool = g.pool_x()
            bulb = inv_clamp(g.bulb_level(), 0.0, 1.0)
            light = bulb * math.exp(-((pool - 640.0) / 190.0) ** 2)

            # THE CORD and the shade, tilted with the swing.
            if g.bulb_fall is None:
                k = (0.0 - MY_HANG_PIVOT[1]) / max(1.0, by - MY_HANG_PIVOT[1])
                x0 = MY_HANG_PIVOT[0] + (bx - MY_HANG_PIVOT[0]) * k
                p.line(x0 + sx, -2.0 + sy, bx + sx, by - 10.0 + sy, width=1.0,
                       col="#3a404c", alpha=0.95, add=False)
            # The lamp hangs between you and it, so while it hangs it is drawn
            # first (it is above the head) -- and once the cord goes it falls
            # IN FRONT of the figure, so it is drawn after it.
            if not g.bulb_gone and g.bulb_fall is None:
                self._draw_bulb(g, p, bx, by, sx, sy, bulb)

            inv_fx_paint(p, g.fx, "back", sx, sy)

            # ITS SHADOW on the boards, thrown away from the light.
            if not arriving:
                p.shadow(640.0 + (640.0 - pool) * 0.55 + sx, MY_A1_FEET + 4.0 + sy,
                         130.0, 22.0, alpha=0.18 + 0.45 * light)

            # It stands where it is and the strata do the moving. There is no
            # bob and no breath: everything about this figure that is in motion
            # is INSIDE it -- and the light swinging across it.
            zoom = MY_ZOOM_ACT1
            tint = inv_lerp_tint((0.40, 0.46, 0.60), (1.06, 1.02, 0.96),
                                 inv_clamp(light, 0.0, 1.0), 1.0)
            lit = (g.body_lit if arriving
                   else inv_clamp(0.12 + 0.10 * doubt + 0.32 * light, 0.0, 1.0))
            self._draw_body(g, p, 640 + sx, my_fig_cy(MY_A1_FEET, zoom) + sy, zoom,
                            shear=0.70 + 0.85 * doubt + 1.3 * g.body_hit + 0.6 * g.windup,
                            ap=g.body_ap + 0.22 * doubt + 0.30 * g.body_hit,
                            lit=lit, band=g.body_band, diss=g.body_diss,
                            hurt=0.35 * g.body_hit, tint=tint)

            if not g.bulb_gone and g.bulb_fall is not None:
                self._draw_bulb(g, p, bx, by, sx, sy, bulb, falling=True)

            inv_fx_paint(p, g.fx, "front", sx, sy)

        def _draw_bulb(self, g, p, bx, by, sx, sy, bulb, falling=False):
            """The shade and the bulb: line work for the shade, tilted with
            the cord (or tumbling, once there is no cord), and the hot point."""
            th = g.hang_angle() if not falling else g.mtick * 0.21
            ux, uy = math.sin(th), math.cos(th)        # down the cord
            qx, qy = math.cos(th), -math.sin(th)       # across it
            tx, ty = bx - ux * 5.0 + sx, by - uy * 5.0 + sy
            apx, apy = tx - ux * 13.0, ty - uy * 13.0
            lx, ly = tx - qx * 17.0, ty - qy * 17.0
            rx, ry = tx + qx * 17.0, ty + qy * 17.0
            p.line(apx, apy, lx, ly, width=1.6, col="#1a1e26", alpha=0.95, add=False)
            p.line(apx, apy, rx, ry, width=1.6, col="#1a1e26", alpha=0.95, add=False)
            p.line(lx, ly, rx, ry, width=1.2, col="#c8d2de", alpha=0.55 * bulb, add=True)
            p.glow(bx + sx, by + sy, 11.0, col="#fff6e2", alpha=0.85 * bulb, add=True)
            if falling:
                p.glow(bx + sx, by + sy, 46.0, col="#cfdcea", alpha=0.35 * bulb, add=True)

        def _room_hud(self, g, p, sx, sy):
            if g.mode == "arrive":
                return
            # The top chrome rides the same slide as the panels: it comes down
            # when the bout starts and goes back up at the tear.
            oy = -int(round(110.0 * g.panel_slide))
            doubt = g.doubt_frac()

            inv_draw_panel(p, 24, 14 + oy, 420, 70, MYStage.STYLE_PLATE)
            p.text("MYSTERY", 15, MY_PALE, 40, 20 + oy, bold=True, w=300, h=30,
                   outline=MY_BLACK)
            # ITS ACCOUNT OF ITSELF: a plain bar, and a tick where the tear lands.
            bar_w = 388
            p.fill("#141820", 40, 46 + oy, bar_w, 8)
            left = int(bar_w * inv_clamp(
                (MY_CASE_MAX - g.case_shown) / float(MY_CASE_MAX), 0.0, 1.0))
            if left > 0:
                p.fill(MY_PALE, 40, 46 + oy, left, 8)
                p.fill("#ffffff40", 40, 46 + oy, left, 1)
            if g.case_flash > 0.02:
                p.fill(inv_hex(MY_GOLD, 0.7 * g.case_flash), 40 + max(0, left - 28),
                       44 + oy, 28, 12)
            mark = 40 + int(bar_w * (1.0 - MY_SHIFT_CASE / float(MY_CASE_MAX)))
            p.fill(inv_hex(MY_PALE, 0.55), mark, 43 + oy, 1, 14)
            # DOUBT: not a danger meter -- a CERTAINTY meter, which is why it
            # is the thing that fires the capstone.
            p.fill("#141820", 40, 60 + oy, bar_w, 4)
            dv = int(bar_w * doubt)
            if dv > 0:
                p.fill(MY_WARN if doubt < 0.85 else MY_RED, 40, 60 + oy, dv, 4)
            p.text("DOUBT", 10, MY_DIM, 40, 66 + oy, w=200, h=20)

            inv_draw_log(p, g, 40, 100 + oy, 388,
                         {"you": (MY_PALE, MY_WARN), "it": (MY_DIM, MY_RED)})
            self._lineup_hud(g, p, oy)

            slide = int(g.panel_slide * 200)
            if g.panel_slide < 1.0:
                kick = g.panel_kick
                kx = int(math.sin(g.tick * 2.9) * 8.0 * max(0.0, kick))
                ky = int(abs(kick) * 4.0)
                self._panel(g, p, MYStage.PANEL_CMD, sx, sy + slide)
                self._panel(g, p, MYStage.PANEL_HUD, sx + kx, sy + slide + ky, hit=kick)
                self._panel_contents(g, p, sx, sy + slide, kx, ky)

        def _lineup_hud(self, g, p, oy):
            """THE FIELD, as the number and as the frames: the same integer
            said twice, so what ACCUSE is worth reads without arithmetic."""
            fcol = MY_GOLD if g.field <= 3 else MY_PALE
            p.text("FIELD", 12, MY_DIM, 848, 18 + oy, bold=True, anchor=(1.0, 0.0),
                   w=140, h=24, outline=MY_BLACK)
            p.text("%d" % int(round(g.field_shown)), 40, fcol, 848, 30 + oy,
                   bold=True, anchor=(1.0, 0.0), w=140, h=60, outline=MY_BLACK)
            shifting = (g.mode == "shift")
            for i, f in enumerate(g.lineup):
                x, y = g.lineup_pos(i)
                y += oy
                age = g.tick - f["t"]
                a = 1.0
                if shifting:
                    if f["carry"]:
                        if g.mtick >= 64:
                            continue
                        if g.mtick >= 24:
                            p.glow(x, y, 26.0, 30.0, col=MY_PALE,
                                   alpha=0.25 + 0.25 * math.sin(g.tick * 0.5),
                                   add=True)
                    else:
                        a = max(0.0, 1.0 - max(0, g.mtick - 30) / 30.0)
                self._placard(p, x, y, f["glyph"], MY_PLACARD, a,
                              crossed=not f["open"], cross_age=age, how=f["how"],
                              lift_age=(age if f["how"] == "reopen" else 999))

        def _panel(self, g, p, box, sx, sy, hit=0.0):
            x, y, w, h = box
            inv_draw_panel(p, x + sx, y + sy, w, h, MYStage.STYLE_PANEL)
            if hit > 0.05:
                p.fill(inv_hex(MY_RED, 0.30 * hit), x + sx, y + sy, w, h)

        def _panel_contents(self, g, p, sx, sy, kx=0, ky=0):
            cx, cy, cw, ch = MYStage.PANEL_CMD
            cx += sx
            cy += sy

            if g.mode == "menu":
                for i, row in enumerate(MY_CMDS):
                    live = (i == g.cursor)
                    ry = cy + 18 + i * 30
                    dead = (row[0] == "narrow"
                            and (g.field <= MY_FIELD_MIN
                                 or g.leads < MY_NARROW_COST))
                    if live:
                        p.fill(MY_PALE + "18", cx + 14, ry - 4, cw - 28, 27)
                        p.fill(MY_PALE, cx + 14, ry - 4, 3, 27)
                        p.fill(MY_PALE, cx + 26, ry + 5, 8, 8)
                    col = MY_FAINT if dead else (MY_PALE if live else MY_DIM)
                    p.text(row[1], 20, col, cx + 46, ry, bold=live, w=260, h=30)
                    # THE ONE READOUT THAT TEACHES THE ACT. ACCUSE prints what
                    # it is worth RIGHT NOW, so the player watches that number
                    # climb every time they narrow and works the rule out.
                    if row[0] == "accuse":
                        p.text("%d" % my_accuse_damage(g.field), 17,
                               MY_GOLD if g.field <= 4 else col,
                               cx + cw - 22, ry + 2, anchor=(1.0, 0.0), bold=True,
                               w=120, h=26)
                    elif row[0] == "narrow":
                        p.text("%d" % MY_NARROW_COST, 14, col, cx + cw - 22,
                               ry + 4, anchor=(1.0, 0.0), w=120, h=26)
                p.text("Z  OK      ESC  PAUSE", 12, MY_FAINT, cx + cw - 16,
                       cy + ch - 22, anchor=(1.0, 0.0), w=420, h=24)

            elif g.mode == "beat":
                u = inv_clamp(g.mtick / 6.0, 0.0, 1.0)
                p.text(g.beat_label, 22, MY_PALE, cx + 22, cy + 28, bold=True,
                       w=cw - 40, h=40)
                if g.beat_value:
                    p.text(g.beat_value, int(22 + 4 * u), MY_WARN, cx + 22, cy + 62,
                           bold=True, w=cw - 40, h=44)
                hold = inv_clamp(g.mtick / float(INV_BEAT_HOLD), 0.0, 1.0)
                p.fill(MY_FAINT + "60", cx + 22, cy + ch - 18, cw - 44, 2)
                p.fill(MY_PALE, cx + 22, cy + ch - 18, int((cw - 44) * hold), 2)

            elif g.mode == "enemy":
                u = inv_clamp(g.mtick / 26.0, 0.0, 1.0)
                p.text("MYSTERY", 18, MY_DIM, cx + 22, cy + 30, bold=True,
                       w=cw - 40, h=34)
                p.fill(MY_DIM + "50", cx + 22, cy + 70, cw - 44, 2)
                p.fill(MY_PALE, cx + 22, cy + 70, int((cw - 44) * u), 2)

            hx, hy, hw, hh = MYStage.PANEL_HUD
            hx += sx + kx
            hy += sy + ky
            p.text(inv_player_name(), 19, MY_PALE, hx + 22, hy + 12,
                   bold=True, w=hw - 40, h=32)
            self._odometer(g, p, "HP", g.hp_shown, g.hp, hx + 22, hy + 44, MY_PALE)
            self._odometer(g, p, "LEADS", g.leads_shown, g.leads, hx + 22, hy + 96,
                           MY_DIM, small=True)
            if g.dn_pending:
                p.text("DENOUEMENT", 13, MY_RED, hx + hw - 22, hy + 16,
                       anchor=(1.0, 0.0), w=260, h=26, bold=True)
                p.text("PENDING", 13, MY_WARN, hx + hw - 22, hy + 38,
                       anchor=(1.0, 0.0), w=260, h=26)
            if g.god:
                p.text("GOD", 12, MY_WARN + "aa", hx + hw - 22,
                       hy + hh - 24, anchor=(1.0, 0.0), w=120, h=24)

        def _odometer(self, g, p, label, shown, real, x, y, color, small=False,
                      alpha=1.0):
            """An EarthBound counter: fixed-width cells, and the digits that
            are moving are drawn mid-roll rather than swapped."""
            size = 22 if small else 30
            cell_w = 22 if small else 28
            cell_h = 32 if small else 42
            p.text(label, 14, inv_hex(color, alpha), x, y + (6 if small else 12),
                   bold=True, w=90, h=28)
            value = int(math.ceil(shown - 0.0001)) if shown > 0 else 0
            rolling = abs(shown - real) > 0.05
            digits = "%03d" % inv_clamp(value, 0, 999)
            frac = shown - math.floor(shown)
            base_x = x + (62 if small else 50)
            for i, ch in enumerate(digits):
                dx = base_x + i * cell_w
                p.fill(inv_hex("#08090e", 0.88 * alpha), dx, y, cell_w - 4, cell_h)
                if rolling:
                    off = int(frac * cell_h * (1 if real < shown else -1))
                    nxt = str((int(ch) + (1 if real > shown else -1)) % 10)
                    p.text(nxt, size, inv_hex(color, 0.45 * alpha),
                           dx + (cell_w - 4) // 2,
                           y + off - (cell_h if real < shown else -cell_h) + 2,
                           anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)
                    p.text(ch, size, inv_hex(color, alpha), dx + (cell_w - 4) // 2,
                           y + off + 2, anchor=(0.5, 0.0), w=cell_w, h=cell_h,
                           bold=True)
                else:
                    p.text(ch, size, inv_hex(color, alpha), dx + (cell_w - 4) // 2,
                           y + 2, anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)

        # ----- ACT TWO: the lineup in the dark -----------------------------------

        def _dark_world(self, g, p, sx, sy):
            fade = inv_clamp((g.open - 0.5) * 2.0, 0.0, 1.0)
            latt = 1.0 - g.lattice_off

            self._walls(g, p, sx, sy, fade)

            # --- THE CHALK ON THE BOARDS --------------------------------------
            # Where your light was each time the bell rang, and a cross wherever
            # you ruled somebody out. All of it true; most of it stale by the
            # next stroke, and stale rings go faint the moment the case reopens.
            for s in g.strokes:
                age = g.tick - s["t"]
                a = 0.20 * fade * latt * inv_clamp(1.0 - age / 1100.0, 0.0, 1.0)
                if s["void"]:
                    a *= 0.35
                if a > 0.01:
                    p.ring(s["x"] + sx, s["y"] + sy, s["r"], col=MY_CHALK,
                           alpha=a, add=True)
            for ro in g.ruleouts:
                p.quad("chalk_x", ro["x"] + sx, ro["y"] + sy, 0.62, 0.30,
                       col=MY_CHALK, alpha=0.30 * fade * latt, add=False)
            inv_fx_paint(p, g.fx, "w_floor", sx, sy)

            # --- the dust in your light, and only there --------------------
            for part in g.fx.parts:
                if part["L"] != "w_dust" or part["age"] <= 0:
                    continue
                u = part["age"] / float(part["life"])
                a = (part["a"] * inv_fx_fade(u, part["f"]) * fade
                     * g.light_at(part["x"], part["y"] + 40.0))
                if a < 0.02:
                    continue
                p.quad(part["t"], part["x"] + sx, part["y"] + sy, part["s0"],
                       col=part["c"], alpha=a, add=True)

            # --- FIGURES AND YOU, BY DEPTH -----------------------------------
            items = [(b["y"], 0, b) for b in g.bodies]
            items.append((g.py, 1, None))
            items.sort(key=lambda e: (e[0], e[1]))
            for _y, kind, b in items:
                if kind == 1:
                    self._draw_you(g, p, sx, sy, fade)
                else:
                    self._suspect(g, p, b, sx, sy, fade)

            # --- THE PLACARDS, over everything: a frame is never hidden ---
            warn = g.bell_warn()
            for b in g.bodies:
                self._suspect_placard(g, p, b, sx, sy, fade, warn)

            self._accuse_ui(g, p, sx, sy, fade)

            inv_fx_paint(p, g.fx, "w_front", sx, sy)
            inv_fx_paint(p, g.fx, "front", sx, sy)

        def _walls(self, g, p, sx, sy, fade):
            """You can feel a wall without having established it, so the edge
            of the room is drawn where you are standing near it -- dashed, in
            chalk, gone a few steps away. (Drawn round the whole room it read
            as a box, and its top edge ran straight through the suspects.)"""
            reach = 240.0
            lv = g.lamp_level() * fade
            if lv < 0.02:
                return
            x0, y0 = MY_AR_X - 14, MY_AR_Y - 14
            x1, y1 = MY_AR_X + MY_AR_W + 14, MY_AR_Y + MY_AR_H + 14

            def dash(x, y, w, h, d):
                k = 1.0 - d / reach
                if k <= 0.0:
                    return
                a = int(k * 6.0 + 0.5) / 6.0 * 0.40 * lv
                if a > 0.02:
                    p.fill(inv_hex(MY_CHALK, a), x + sx, y + sy, w, h)

            if g.py - y0 < reach or y1 - g.py < reach:
                for k in range(0, int(x1 - x0), 26):
                    w = min(13, int(x1 - x0) - k)
                    xm = x0 + k + w * 0.5
                    dash(x0 + k, y0, w, 1, math.hypot(xm - g.px, y0 - g.py))
                    dash(x0 + k, y1, w, 1, math.hypot(xm - g.px, y1 - g.py))
            if g.px - x0 < reach or x1 - g.px < reach:
                for k in range(0, int(y1 - y0), 26):
                    h = min(13, int(y1 - y0) - k)
                    ym = y0 + k + h * 0.5
                    dash(x0, y0 + k, 1, h, math.hypot(x0 - g.px, ym - g.py))
                    dash(x1, y0 + k, 1, h, math.hypot(x1 - g.px, ym - g.py))

        def _stride(self, b):
            # A STRIDE WITH A HITCH IN IT: it rises over most of the step and
            # drops all at once -- a walk learned from a diagram.
            ph = b["step"] % 1.0
            return ph, (ph ** 3) * 3.5

        def _suspect(self, g, p, b, sx, sy, fade):
            zoom = MY_FIG_ZOOM2
            fh = MY_FIG_H * zoom
            x, feet = b["x"], b["y"]
            L = g.light_at(x, feet)
            rise = inv_smooth(b["arrive"])
            leave = b["leave"]
            won = (g.mode == "leave_w" and b["id"] == g.solved_id)
            ph, bob = self._stride(b)
            alpha = fade * (0.62 if b["crossed"] else 1.0)

            # The hole it came up through, or is going down into.
            hk = 0.0
            if b["arrive"] < 1.0:
                hk = math.sin(math.pi * b["arrive"])
            if leave > 0.0:
                hk = max(hk, math.sin(math.pi * min(1.0, leave)))
            if hk > 0.02:
                p.glow(x + sx, feet + sy, 34.0 * hk, 11.0 * hk, col="#000000",
                       alpha=0.9 * hk * fade, add=False)
                p.ring(x + sx, feet + sy, 30.0 * hk, 10.0 * hk, col=MY_CHALK,
                       alpha=0.45 * hk * fade, add=True)

            # In the dark it is a shape, barely; in the light it is all there.
            if L < 0.95:
                p.glow(x + sx, feet - fh * 0.5 + sy, 32.0, 74.0, col="#34466a",
                       alpha=0.30 * (1.0 - L) * alpha * (1.0 - leave), add=True)
            if L > 0.05:
                ox, oy = x - g.px, feet - g.py
                n = math.hypot(ox, oy) or 1.0
                p.shadow(x + sx + ox / n * 9.0, feet + sy + oy / n * 4.0 + 1.0,
                         24.0, 7.0, alpha=0.6 * L * alpha)

            tint = inv_lerp_tint((0.56, 0.64, 0.90), (1.04, 1.00, 0.94), L, 1.0)
            if b["crossed"]:
                tint = (tint[0] * 0.70, tint[1] * 0.70, tint[2] * 0.74, 1.0)
            lit = 0.22 + 0.74 * L
            diss = max(1.0 - rise, leave)
            ap = 0.28 + 0.62 * leave
            if won:
                lit = max(lit, g.end_show)
                diss = max(diss, g.body_diss)
                ap += 0.6 * g.body_diss
            if g.tick - b["solved_t"] < 30:
                lit = max(lit, 1.0 - (g.tick - b["solved_t"]) / 30.0)
            stretch = (1.0, (0.25 + 0.75 * rise)
                       * (1.0 + 0.025 * math.sin(ph * 6.2831853)))
            band = 0.30 + 0.62 * (0.5 + 0.5 * math.sin(g.clock * 0.37 + b["seed"] * 3.0))
            self._draw_body(g, p, x + sx, my_fig_cy(feet, zoom) - bob + sy, zoom,
                            t=g.clock + b["seed"] * 7.0, alpha=alpha,
                            shear=0.55 + 0.6 * b["hurt"] + (0.4 if b["break"] > 0 else 0.0),
                            ap=ap, lit=inv_clamp(lit, 0.0, 1.0), band=band,
                            diss=inv_clamp(diss, 0.0, 1.0), hurt=0.85 * b["hurt"],
                            tint=tint, stretch=stretch)

        def _suspect_placard(self, g, p, b, sx, sy, fade, warn):
            fh = MY_FIG_H * MY_FIG_ZOOM2
            x, feet = b["x"], b["y"]
            _ph, bob = self._stride(b)
            L = g.light_at(x, feet)
            a = (fade * (0.50 + 0.50 * L) * (1.0 - min(1.0, b["leave"]))
                 * inv_smooth(b["arrive"]))
            if g.mode == "leave_w" and b["id"] == g.solved_id:
                a *= (1.0 - g.body_diss)
            ins = 0.0
            if g.mode == "dark" and not b["crossed"] and g.inside(b):
                ins = 0.45 + 0.55 * warn
            py_ = feet - fh - 18.0 - bob + sy
            if g.tick - b["solved_t"] < 30:
                p.glow(x + sx, py_, 30.0, col=MY_GOLD,
                       alpha=0.8 * (1.0 - (g.tick - b["solved_t"]) / 30.0), add=True)
            self._placard(p, x + sx, py_, b["glyph"], MY_PLACARD2, a,
                          crossed=b["crossed"], cross_age=g.tick - b["cross_t"],
                          how="bell", lift_age=g.tick - b["lift_t"], inside=ins)
            # Where it is standing -- which is what the bell measures.
            p.glow(x + sx, feet + sy, 5.0, 2.0, col=MY_CHALK,
                   alpha=0.35 * fade * (1.0 - min(1.0, b["leave"])), add=True)

        def _draw_you(self, g, p, sx, sy, fade):
            if g.iframes > 0 and (g.tick // 4) % 2 == 1:
                return
            p.shadow(g.px + sx, g.py + sy + 2.0, 12.0, 4.0, alpha=0.5 * g.lamp_level())
            self._draw_heart(g, p, g.px + sx, g.py - 12.0 + sy,
                             alpha=fade if g.mode == "dark" else 0.85 * fade)

        def _accuse_ui(self, g, p, sx, sy, fade):
            """Brackets on whoever an accusation would be aimed at, so "is it
            in reach, and is it that one" is never a guess -- and, while Z is
            held, a ring closing round its frame."""
            if g.mode != "dark":
                return
            b = g._body(g.name_target) if g.naming else g._name_target()
            if b is None:
                return
            fh = MY_FIG_H * MY_FIG_ZOOM2
            x, feet = b["x"] + sx, b["y"] + sy
            x0, x1 = x - 30.0, x + 30.0
            y0, y1 = feet - fh - 2.0, feet + 6.0
            col = inv_hex(MY_GOLD if g.naming else MY_PALE,
                          (0.90 if g.naming else 0.50) * fade)
            for (hx, hy, vx, vy) in ((x0, y0, x0, y0), (x1 - 9, y0, x1 - 2, y0),
                                     (x0, y1 - 2, x0, y1 - 9), (x1 - 9, y1 - 2, x1 - 2, y1 - 9)):
                p.fill(col, hx, hy, 9, 2)
                p.fill(col, vx, vy, 2, 9)
            if g.naming:
                frac = inv_clamp(g.name_t / float(MY_NAME_TICKS), 0.0, 1.0)
                hx, hy = x, feet - fh - 18.0
                R = 24.0
                steps = max(2, int(28 * frac))
                prev = None
                for i in range(steps + 1):
                    ang = -1.5708 + 6.28318 * frac * (i / float(steps))
                    pt = (hx + math.cos(ang) * R, hy + math.sin(ang) * R)
                    if prev is not None:
                        p.line(prev[0], prev[1], pt[0], pt[1], width=2.4,
                               col=MY_GOLD, alpha=0.95 * fade, add=True)
                    prev = pt
                p.ring(g.px + sx, g.py + sy, MY_NAME_R, col=MY_PALE,
                       alpha=0.10 * fade, add=True)

        def _dark_hud(self, g, p):
            fade = g.hud_fade * inv_clamp((g.open - 0.5) * 2.0, 0.0, 1.0)
            ffade = g.field_fade * inv_clamp((g.open - 0.5) * 2.0, 0.0, 1.0)

            if fade > 0.02:
                # SOLVED -- and the pips make a bar of 100 read as "four landed
                # accusations" without a word.
                self._plate(p, 24, 14, 340, 58, MYStage.STYLE_PLATE, fade)
                p.text("SOLVED", 12, inv_hex(MY_DIM, fade), 40, 20, bold=True,
                       w=160, h=24)
                pips = int(math.ceil(MY_SOLVE_MAX / MY_SOLVE_GAIN))
                p.text("%d / %d" % (g.solves, pips), 12, inv_hex(MY_DIM, fade),
                       348, 20, bold=True, anchor=(1.0, 0.0), w=120, h=24)
                bar_w = 308
                p.fill(inv_hex("#141820", fade), 40, 44, bar_w, 10)
                fw = int(bar_w * inv_clamp(g.solve_shown / MY_SOLVE_MAX, 0.0, 1.0))
                if fw > 0:
                    p.fill(inv_hex(MY_GOLD, fade), 40, 44, fw, 10)
                    p.fill(inv_hex("#ffffff", 0.3 * fade), 40, 44, fw, 1)
                if g.solve_flash > 0.02:
                    p.fill(inv_hex(MY_RED, 0.8 * g.solve_flash * fade), 40, 44, bar_w, 10)
                for i in range(1, pips):
                    p.fill(inv_hex(MY_BLACK, 0.85 * fade),
                           40 + int(bar_w * i / float(pips)), 44, 2, 10)

                # THE VERDICT, and the reopening when one is coming.
                if g.reopen_warn > 0.01 and g.mode == "dark":
                    a = fade * (0.45 + 0.55 * (0.5 + 0.5 * math.sin(g.tick * 0.32)))
                    p.text("REOPENING", 24, inv_hex(MY_RED, a), 640, 20, bold=True,
                           anchor=(0.5, 0.0), w=420, h=40, outline=MY_BLACK)
                elif g.verdict and g.verdict_t < 170:
                    vcol = {"SEEN": MY_GOLD, "UNSEEN": MY_PALE,
                            "TWO REMAIN": MY_WARN, "REOPENED": MY_RED}.get(g.verdict, MY_DIM)
                    a = fade * inv_clamp((170 - g.verdict_t) / 40.0, 0.0, 1.0)
                    pop = 1.0 + 0.25 * inv_clamp(1.0 - g.verdict_t / 8.0, 0.0, 1.0)
                    p.text(g.verdict, int(26 * pop), inv_hex(vcol, a), 640, 18,
                           bold=True, anchor=(0.5, 0.0), w=520, h=52,
                           outline=MY_BLACK)
                # THE NEXT STROKE, as a rule filling under it -- the same count
                # the arc on your rim is drawing.
                if g.mode == "dark":
                    frac = g.count_uniform()[3]
                    reop = g.strokes_left <= 1
                    rcol = MY_RED if reop else (MY_GOLD if g.bell_warn() > 0.0 else MY_DIM)
                    p.fill(inv_hex("#141820", 0.9 * fade), 560, 62, 160, 3)
                    p.fill(inv_hex(rcol, fade), 560, 62, int(160 * frac), 3)

                # HP and SWEEP, small, at the bottom corners.
                self._plate(p, 24, 648, 172, 54, MYStage.STYLE_PLATE, fade)
                self._odometer(g, p, "HP", g.hp_shown, g.hp, 36, 659,
                               MY_RED if g.hp < 90 else MY_PALE, small=True,
                               alpha=fade)
                ready = (g.sweep_cd <= 0 and g.sweep_t <= 0)
                self._plate(p, 1084, 648, 172, 54, MYStage.STYLE_PLATE, fade)
                p.text("SWEEP", 12, inv_hex(MY_LAMPC if ready else MY_FAINT, fade),
                       1098, 658, bold=True, w=120, h=22)
                p.fill(inv_hex("#141820", fade), 1098, 682, 144, 4)
                cdw = int(144 * (1.0 - inv_clamp(g.sweep_cd / float(MY_SWEEP_CD),
                                                0.0, 1.0)))
                if cdw > 0:
                    p.fill(inv_hex(MY_LAMPC if ready else MY_DIM, fade), 1098, 682,
                           cdw, 4)
                p.text("MOVE  WASD      Z  ACCUSE (HOLD)      X  SWEEP", 12,
                       inv_hex(MY_FAINT, fade), 640, 692, anchor=(0.5, 0.0),
                       w=760, h=24, outline=MY_BLACK)
                if g.god:
                    p.text("GOD", 12, inv_hex(MY_WARN, 0.7 * fade), 1240, 624,
                           anchor=(1.0, 0.0), w=120, h=24)

            # THE LINEUP, top right: every suspect in the room by its frame,
            # crossed or not, and FIELD -- how many are still open. Act one's
            # word with act one's meaning, and in the winning ending the one
            # place it ever reads 1.
            if ffade > 0.02:
                alive = sorted(g.alive(), key=lambda b: b["id"])
                n = len(alive)
                step = 32
                x_r = 1236
                warn = g.bell_warn()
                for i, b in enumerate(alive):
                    x = x_r - (n - 1 - i) * step
                    ins = 0.0
                    if g.mode == "dark" and not b["crossed"] and g.inside(b):
                        ins = 0.45 + 0.55 * warn
                    self._placard(p, x, 44, b["glyph"], MY_PLACARD,
                                  ffade * inv_smooth(b["arrive"]),
                                  crossed=b["crossed"], cross_age=g.tick - b["cross_t"],
                                  how="bell", lift_age=g.tick - b["lift_t"],
                                  inside=ins)
                x_l = x_r - (n - 1) * step - 26
                fcol = MY_GOLD if g.field_now() <= 2 else MY_PALE
                p.text("FIELD", 12, inv_hex(MY_DIM, ffade), x_l, 16, bold=True,
                       anchor=(1.0, 0.0), w=120, h=24, outline=MY_BLACK)
                p.text("%d" % int(round(g.field_shown)), 34, inv_hex(fcol, ffade),
                       x_l, 30, bold=True, anchor=(1.0, 0.0), w=120, h=52,
                       outline=MY_BLACK)

        # ----- numbers and pause -----------------------------------------------

        def _floats(self, g, p, sx, sy):
            for f in g.floats:
                a = inv_clamp(f["life"] / 26.0, 0.0, 1.0)
                age = 52 - f["life"]
                pop = 1.0 + 0.30 * inv_clamp(1.0 - age / 6.0, 0.0, 1.0)
                p.text(f["text"], int((26 if f["big"] else 20) * pop),
                       inv_hex(f["color"], a), int(f["x"]) + sx, int(f["y"]) + sy,
                       bold=f["big"], anchor=(0.5, 0.5), w=380, h=70,
                       outline=MY_BLACK)

        def _pause(self, g, p):
            p.fill("#04050ad2", 0, 0, 1280, 720)
            inv_draw_panel(p, 440, 270, 400, 150, MYStage.STYLE_PANEL)
            p.text("PAUSED", 40, MY_PALE, 640, 322, bold=True, anchor=(0.5, 0.5),
                   w=600, h=70)
            p.text("ESC  RESUME        Q  QUIT", 16, MY_DIM, 640, 378,
                   anchor=(0.5, 0.5), w=800, h=44)


# --- THE SCREEN --------------------------------------------------------------
screen inv_mystery_screen(game):
    modal True
    use enter_m_input_lock()

    add Solid("#04050a")
    add MYStage(game)

    key "K_ESCAPE" action Function(game.toggle_pause)
    key "mouseup_3" action Function(game.toggle_pause)
    if game.paused:
        key "K_q" action Function(game.give_up)

    if config.developer:
        key "K_g" action Function(game.toggle_god)

    timer 0.25 repeat True action Function(inv_poll_result, game, _update_screens=False)


# --- WRAPPER -----------------------------------------------------------------
default my_game = None
default my_deaths = 0
default my_retry = False
# A RETRY FROM THE TEAR, carrying the field act one handed over, glyphs too.
default my_resume = None

label archivist_invasion_mystery:
    $ my_deaths = 0
    $ my_retry = False
    $ my_resume = None

label inv_mystery_fight:
    $ renpy.block_rollback()

    $ my_game = MYGame(retry=my_retry, deaths=my_deaths,
                    debug=config.developer, start_open=inv_dev_start_open,
                    resume=my_resume)
    $ my_resume = None

    $ _my_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ _my_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None
    scene black

    call screen inv_mystery_screen(my_game)
    $ _my_result = _return
    $ _my_checkpoint = my_game.checkpoint

    $ my_game = None
    $ quick_menu = _my_prev_quick_menu
    $ _game_menu_screen = _my_prev_game_menu
    $ inv_music_stop(1.0)
    $ inv_heart_stop(0.6)
    $ inv_stop_sfx(0.2)
    scene black

    if _my_result == "victory":
        $ inv_record_result("mystery", True)
        jump inv_mystery_victory
    elif _my_result == "quit":
        jump inv_mystery_quit

    $ inv_record_result("mystery", False)
    jump inv_mystery_defeat

label inv_mystery_victory:
    if inv_dev_test:
        $ renpy.notify("MYSTERY: named. Still open.")
        return
    # STORY PLACEMENT: DRAWING BOARD.
    return

label inv_mystery_defeat:
    $ my_deaths += 1
    $ my_retry = True

    call screen inv_retry_screen("MYSTERY", "UNSOLVED",
                                 inv_retry_options(_my_checkpoint),
                                 ink=MY_PALE, dim=MY_DIM, accent=MY_RED,
                                 bg=MY_BLACK)
    if _return == "tear":
        $ my_resume = _my_checkpoint
        scene black
        jump inv_mystery_fight
    elif _return == "start":
        scene black
        jump inv_mystery_fight
    if inv_dev_test:
        $ renpy.notify("MYSTERY: unsolved. Recorded.")
    return

label inv_mystery_quit:
    $ my_retry = True
    if inv_dev_test:
        $ renpy.notify("MYSTERY: withdrawn.")
    return
