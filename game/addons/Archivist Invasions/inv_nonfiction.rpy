# Nonfiction invasion: source claims in the turn-based bout, then carry evidence
# across a shrinking page. STATE creates unsourced claims; CITE banks the ledger.
# Banked act-one progress becomes VERIFIED; unsourced progress is lost at shift.
#
# Act two fills PENDING at the entry, carries it to column-zero margins and files
# it on an available row. VERIFIED is permanent. ATTEST roots the player while
# protecting the carried evidence and current cell; it is an optional bargain.
# The margin remains traversable and never hosts the entry. All readouts are
# truthful. Halftone registration follows its own schedule rather than the music.
#
# NFGame owns simulation state; NFStage advances it at 60Hz and paints the flat
# overhead page. Shared encounter constraints and audio live in invasions.rpy.
# Sprite framing comes from NF_SPRITE_W/H and NF_FIG_DX/DY; shaders render the
# current portrait as printed matter. Rendering-only texture has no hitbox.

init -9 python:
    NF_PLAIN_OK = False
    NF_STRIKE_OK = False

    def _nf_register_plain():
        # THE ROOM, BOTH ACTS. The same hyperspace plate every invasion is
        # fought over -- printed. There is no domain warp anywhere in this
        # shader and that is deliberate: Biography's room boils and Horror's
        # room rushes, and nothing in Nonfiction's room is allowed to FLOW,
        # because flowing is a thing an image does when something is inventing
        # the next frame of it. This room is re-set instead: it samples on a
        # quantised grid, posterizes to a handful of levels, screens the result
        # into halftone dots, and jumps to a new registration in hard steps.
        # It is never still and it is never moving.
        #
        # u_nf_open is the whole corruptive shift in one number. At 0 the plate
        # is a photographic negative in a dark room. At 1 the room is a sheet
        # of paper: bone white, ruled, with the printing almost entirely gone
        # off it. Nonfiction does not drag you into a different room at the
        # tear -- it empties the one you are already in.
        renpy.register_shader("inv.plain", variables="""
            uniform sampler2D tex0;
            uniform sampler2D tex1;
            uniform vec4 u_nf_spot;
            uniform float u_nf_platen;
            uniform vec2 u_nf_res;
            uniform float u_nf_time;
            uniform float u_nf_open;
            uniform float u_nf_press;
            uniform float u_nf_reg;
            uniform float u_nf_scrut;
            uniform float u_nf_flash;
            uniform float u_nf_dark;
            uniform float u_nf_churn;
            uniform vec4 u_nf_hole;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float nf_hash(vec2 p) {
                return fract(sin(dot(p, vec2(41.13, 289.7))) * 27183.3141);
            }
            vec2 nf_mirror(vec2 p) {
                return abs(fract(p * 0.5) * 2.0 - 1.0);
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            float t = u_nf_time;
            float open = clamp(u_nf_open, 0.0, 1.0);
            float scrut = clamp(u_nf_scrut, 0.0, 1.0);
            float press = clamp(u_nf_press, 0.0, 1.0);
            // How hard the page is being worked. Zero at the tear; by the end
            // the sheet has been through the press enough times to show it.
            float churn = clamp(u_nf_churn, 0.0, 1.0) * open;

            vec2 c = uv - 0.5;

            // The rupture, same instrument as every arrival -- but a hole in a
            // page rather than in a fluid, so the lip is a hard rule.
            vec2 hp = (u_nf_hole.xy / max(u_nf_res, vec2(1.0))) - 0.5;
            float hr = max(u_nf_hole.z, 1.0) / max(u_nf_res.x, 1.0);
            float hs = clamp(u_nf_hole.w, 0.0, 1.0);
            vec2 hv = c - hp;
            float hd = length(hv);
            float hinf = (1.0 - smoothstep(0.0, hr, hd)) * hs;
            if (hinf > 0.001) {
                float ha = hinf * hinf * 4.2;
                float ccs = cos(ha);
                float csn = sin(ha);
                hv = vec2(hv.x * ccs - hv.y * csn, hv.x * csn + hv.y * ccs);
                c = hp + hv * (1.0 - 0.60 * hinf);
            }

            // REGISTRATION. Not a wave -- a STEP. The plate is re-set on the
            // page at a discrete offset and HOLDS there until the next pass.
            float sstep = floor(t * 0.75 + u_nf_reg);
            vec2 reg = vec2(nf_hash(vec2(sstep, 1.0)) - 0.5,
                            nf_hash(vec2(sstep, 7.0)) - 0.5)
                    * (0.006 + 0.055 * press + 0.014 * churn);
            vec2 sp = c + reg;

            // Quantised sampling: the substrate has a resolution, and you can
            // see it.
            float cells = mix(340.0, 148.0, open);
            sp = floor(sp * cells) / cells;
            float lum = dot(texture2D(tex0, nf_mirror(sp + 0.5)).rgb,
                            vec3(0.299, 0.587, 0.114));

            // POSTERIZE, then SCREEN. Ink is a dot or it is nothing.
            float levels = mix(6.0, 3.0, open);
            lum = floor(lum * levels) / levels;
            vec2 rot = vec2(uv.x * 0.7071 - uv.y * 0.7071,
                            uv.x * 0.7071 + uv.y * 0.7071);
            vec2 dc = fract(rot * mix(300.0, 205.0, open)) - 0.5;
            float dens = clamp(1.0 - lum, 0.0, 1.0);
            float rad = 0.53 * sqrt(dens);
            float ink = 1.0 - smoothstep(rad - 0.08, rad + 0.08, length(dc));

            // Almost all of the printing comes off the sheet at the tear.
            ink *= mix(1.0, 0.20, open);

            vec3 paper = mix(vec3(0.031, 0.033, 0.038),
                            vec3(0.906, 0.898, 0.876), open);
            vec3 inkc = mix(vec3(0.50 + 0.22 * scrut,
                                0.52 + 0.22 * scrut,
                                0.50 + 0.20 * scrut),
                            vec3(0.055, 0.052, 0.050), open);
            vec3 col = mix(paper, inkc, ink);

            // A SECOND SCREEN, AT A FIGHTING ANGLE. This is the whole
            // escalation and it is the correct one for this fight: a page
            // that has been run through the press again and again picks up
            // another halftone out of register with the first, and two
            // screens at slightly different angles is where MOIRE comes
            // from. So the sheet gets harder and harder to look at without
            // one new object being added to it, without anything flowing, and
            // without inventing a single frame of anything.
            // It carries its OWN density rather than the plate's: at open the
            // plate is nearly blank, so a second screen keyed to it would be
            // invisible exactly where it is wanted. Held to a third of full
            // weight -- the page has to become hard to look at, never hard to
            // read, and the redactions and the one red thing on it both have
            // to stay findable.
            if (churn > 0.002) {
                float ang2 = 0.7854 + 0.22 * churn;
                vec2 rot2 = vec2(uv.x * cos(ang2) - uv.y * sin(ang2),
                                uv.x * sin(ang2) + uv.y * cos(ang2));
                vec2 dc2 = fract(rot2 * mix(214.0, 176.0, churn)) - 0.5;
                float rad2 = 0.53 * sqrt(clamp(1.0 - lum * 0.74, 0.0, 1.0));
                float ink2 = 1.0 - smoothstep(rad2 - 0.10, rad2 + 0.10,
                                            length(dc2));
                col = mix(col, inkc, ink2 * churn * 0.34);
            }

            // RULED. Horizontal rules the whole way down, and one vertical
            // margin rule, because this is a page and it has always been a
            // page. The margin rule sits exactly on the edge of the margin
            // COLUMN in act two -- the shader draws the boundary the fight is
            // played against, rather than a decorative line near it.
            float ly = uv.y * u_nf_res.y;
            float rule = 1.0 - smoothstep(0.0, 0.055, fract(ly / 26.0));
            col = mix(col, inkc, rule * (0.09 + 0.26 * open + 0.16 * churn));
            // ...and a second set of rules between them once the page has
            // been worked, half-height and half-weight: ruled twice as close
            // and never quite lining up with the first set.
            float rule2 = 1.0 - smoothstep(0.0, 0.075, fract(ly / 13.0 + 0.5));
            col = mix(col, inkc, rule2 * 0.14 * churn);
            float mx = mix(0.113, 0.249, open);
            float marg = 1.0 - smoothstep(0.0, 1.6 / u_nf_res.x,
                                        abs(uv.x - mx));
            col = mix(col, inkc, marg * (0.10 + 0.34 * open));

            // Act one is a DARK room: the negative sits low so the hanging
            // sheet and the light falling on it are what you see first.
            col *= mix(0.42, 1.0, open);

            // REAL STOCK (Oct 2 2026). Act two's page is paper, not a flat
            // grey: long fibres and a slight cockle from tex1, lit from the
            // top left so the relief reads -- still, never flowing.
            if (open > 0.01) {
                vec2 puv = uv * u_nf_res / 512.0;
                float p0 = texture2D(tex1, puv).r;
                float pxs = texture2D(tex1, puv + vec2(1.5 / 512.0, 0.0)).r;
                float pys = texture2D(tex1, puv + vec2(0.0, 1.5 / 512.0)).r;
                float relief = (p0 - pxs) * 2.4 + (p0 - pys) * 1.8;
                vec3 stock = vec3(p0 * 1.020, p0 * 1.000, p0 * 0.962) / 0.86;
                col = mix(col, col * stock * (1.0 + relief * 0.85), open);
            }
            // Act one: a cold light from above spilling past the hanging
            // sheet onto the dark behind it.
            if (u_nf_spot.w > 0.001) {
                float sd = distance(uv * u_nf_res, u_nf_spot.xy);
                float sp2 = 1.0 - smoothstep(u_nf_spot.z * 0.15, u_nf_spot.z, sd);
                col += vec3(0.16, 0.165, 0.17) * sp2 * sp2 * u_nf_spot.w * (1.0 - open);
            }
            // THE PLATEN coming down: a shadow from the top of the sheet,
            // there and gone with the press.
            float plat = clamp(u_nf_platen, 0.0, 1.0);
            col *= 1.0 - plat * 0.55 * (1.0 - smoothstep(0.0, 0.9, uv.y - plat * 0.6));

            // Tooth. Paper has a surface; a negative has grain -- and paper
            // that has been through a press this many times has more of it.
            float tooth = nf_hash(floor(uv * u_nf_res * 0.5));
            col *= 1.0 - (0.030 + 0.028 * open + 0.055 * churn) * tooth;
            // And it is not white any more. Nothing dramatic: the stock goes
            // a shade grey and a shade warm, the way a sheet does.
            col = mix(col, col * vec3(0.90, 0.885, 0.855), churn * open);

            if (hs > 0.001) {
                float core = 1.0 - smoothstep(hr * 0.14, hr * 0.54, hd);
                col *= mix(1.0, 0.015, core * hs);
                float lip = 1.0 - smoothstep(0.0, hr * 0.10,
                                            abs(hd - hr * 0.54));
                col = mix(col, mix(vec3(0.86, 0.87, 0.84), vec3(0.02),
                                open), lip * hs);
            }

            // Act one is a room and rooms have corners. A page does not, so
            // the vignette leaves entirely at the tear.
            float r = length(c);
            float vig = 1.0 - r * r * (0.85 + 0.95 * scrut);
            col *= mix(max(vig, 0.0), 1.0, open);

            // THE PRESS COMING DOWN. A brief inversion, not a glow.
            col = mix(col, vec3(1.0) - col, press * 0.30);

            col = mix(col, vec3(0.97, 0.97, 0.95), clamp(u_nf_flash, 0.0, 1.0));
            col *= 1.0 - clamp(u_nf_dark, 0.0, 1.0);
            gl_FragColor = vec4(col, 1.0);
        """)

    def _nf_register_strike():
        # NONFICTION'S OWN BODY. Every Archivist gets its own way of being
        # wrong, or they all read as the same puppet in different hats.
        #
        #   Biography  MISREGISTRATION -- fourteen hard bands sliding out of
        #              sync, chromatic fringing, high frequency. Digital.
        #   Horror     UNDULATION -- low frequency, liquid, no colour split, a
        #              swell from inside and a silhouette that frays into
        #              smoke. You cannot find its edge.
        #   Nonfiction REPRODUCTION -- and it is the opposite of both, because
        #              it does not deform at all. It is PRINTED. Luminance
        #              only, posterized, screened into halftone dots, ruled
        #              across like typeset copy. Its bands do not travel
        #              between positions: they JUMP to a new offset and hold
        #              there, the way a plate is re-set rather than moved.
        #              It has no colour because it does not invent one.
        #
        # And it is REDACTED: u_st_bars grows solid black rules across it that
        # overshoot its own silhouette. That is its dissolve too -- it does
        # not erode in cells like Biography or drain bottom-up like Horror. It
        # is struck out.
        #
        # NOTE ON THE FLAT SOURCE: the tone ramp below is what lets a
        # featureless grey silhouette resolve into a plate with real tonal
        # structure instead of one uniform field of identical dots. Keep it
        # when the finished portrait arrives; it flatters that too.
        renpy.register_shader("inv.strike", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_st_res;
            uniform float u_st_t;
            uniform float u_st_jump;
            uniform float u_st_reg;
            uniform vec2 u_st_stretch;
            uniform float u_st_pivot;
            uniform float u_st_ink;
            uniform float u_st_paper;
            uniform float u_st_bars;
            uniform float u_st_churn;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float st_hash(vec2 p) {
                return fract(sin(dot(p, vec2(63.71, 11.29))) * 19317.7193);
            }
            // ONE SCREEN OF A PROCESS SEPARATION. `ang` is the screen angle,
            // `freq` its ruling, `tone` the density it is carrying. Returns
            // dot coverage 0..1. Real process printing runs each separation at
            // a DIFFERENT angle for exactly one reason -- so the rosettes
            // interlock instead of beating against each other -- and running
            // three of them is what makes this read as a printed plate rather
            // than as a filter with a dot pattern in it.
            float st_screen(vec2 uv, float ang, float freq, float tone,
                            float gain) {
                float ca = cos(ang);
                float sa = sin(ang);
                vec2 r = vec2(uv.x * ca - uv.y * sa, uv.x * sa + uv.y * ca);
                vec2 d = fract(r * freq) - 0.5;
                // DOT GAIN: ink spreads on absorbent stock, so a dot prints
                // bigger than it was screened, and it spreads MORE in the
                // midtones than at either end. This is the single detail that
                // separates "halftoned" from "printed".
                float cov = clamp(tone, 0.0, 1.0);
                cov += gain * cov * (1.0 - cov) * 1.6;
                float rad = 0.55 * sqrt(clamp(cov, 0.0, 1.0));
                return 1.0 - smoothstep(rad - 0.085, rad + 0.085, length(d));
            }
        """, fragment_300="""
            vec2 plate_uv = v_tex_coord;
            vec2 uv = v_tex_coord;
            vec2 piv = vec2(0.5, clamp(u_st_pivot, 0.0, 1.0));
            vec2 st = max(u_st_stretch, vec2(0.08));
            uv = (uv - piv) / st + piv;

            float t = u_st_t;
            float jump = clamp(u_st_jump, 0.0, 3.0);

            // RE-SET, NOT WARPED. Nine bands, each holding a fixed offset for
            // the whole of a registration step and then cutting to another.
            float sstep = floor(t * 3.0 + u_st_reg);
            float band = floor(uv.y * 9.0);
            uv.x += (st_hash(vec2(band, sstep)) - 0.5) * 0.032 * jump;
            uv += vec2(st_hash(vec2(sstep, 3.0)) - 0.5,
                    st_hash(vec2(sstep, 11.0)) - 0.5) * 0.009 * jump;

            vec4 src = texture2D(tex0, uv);
            float a = src.a;
            float churn = clamp(u_st_churn, 0.0, 1.0);

            // PRINTED, AND NOW ACTUALLY PRINTED. It used to be one 45-degree
            // screen over a posterized luminance, which is a halftone FILTER.
            // A plate is three separations, each screened at its own angle,
            // each carrying a different part of the tone range, and each very
            // slightly out of register with the others -- so this runs the
            // real process angles (15 / 75 / 45, the last one for the heavy
            // separation because that is where it goes) and lets the rosettes
            // interlock.
            //
            // NOTE THIS IS NOT BIOGRAPHY'S AXIS. Biography's plates fail to
            // line up and that is its whole character; these three line up
            // CORRECTLY and merely reveal that the thing was reproduced. The
            // difference is discipline, and it is the difference between the
            // two Archivists.
            float lum = dot(src.rgb, vec3(0.299, 0.587, 0.114));
            lum = clamp(lum * (0.58 + 0.66 * (1.0 - uv.y)), 0.0, 1.0);
            // Posterized, but on more levels than before and with the step
            // itself softened, so the tone ramp survives being screened.
            float levels = mix(5.0, 7.0, churn);
            lum = floor(lum * levels) / levels;
            float tone = clamp(1.0 - lum, 0.0, 1.0);

            // The three separations. Light / mid / heavy, each screened
            // separately, so a midtone is carried by two plates at once and a
            // shadow by all three -- which is where the density comes from.
            float gain = 0.18 + 0.34 * churn;
            float freq = mix(150.0, 196.0, churn);
            float s_lt = st_screen(uv, 0.2618, freq * 1.00,
                                clamp(tone * 1.35, 0.0, 1.0), gain);
            float s_md = st_screen(uv, 1.3090, freq * 0.88,
                                clamp(tone * 1.05 - 0.16, 0.0, 1.0), gain);
            float s_hv = st_screen(uv, 0.7854, freq * 0.74,
                                clamp(tone * 0.95 - 0.42, 0.0, 1.0), gain);
            float dotv = clamp(s_lt * 0.44 + s_md * 0.36 + s_hv * 0.42,
                            0.0, 1.0);

            vec3 stock = mix(vec3(0.74, 0.75, 0.72), vec3(0.94, 0.93, 0.91),
                            clamp(u_st_paper, 0.0, 1.0));
            vec3 inkc = mix(vec3(0.085, 0.085, 0.095), vec3(0.04, 0.04, 0.04),
                            clamp(u_st_paper, 0.0, 1.0));

            // PAPER FIBRE. Stock has a grain and it takes ink unevenly, so the
            // coverage is modulated by the sheet rather than being uniform.
            float fibre = st_hash(floor(plate_uv * u_st_res * 0.65));
            dotv *= 1.0 - (0.10 + 0.16 * churn) * fibre;

            vec3 printed = mix(stock, inkc, dotv);

            // SHOW-THROUGH. Something is printed on the other side of the
            // sheet and thin stock does not hide it: the body sampled from
            // behind, mirrored, very faint, and fainter still where this side
            // is already heavily inked.
            float back = dot(texture2D(tex0, vec2(1.0 - uv.x, uv.y)).rgb,
                            vec3(0.299, 0.587, 0.114));
            printed = mix(printed, printed * (0.90 - 0.14 * back),
                        (0.30 + 0.35 * churn) * (1.0 - dotv));

            float pr = clamp(u_st_ink, 0.0, 1.0);
            vec3 col = mix(src.rgb, printed, pr);

            // Typeset: rules run across it the same as they run across the
            // page it is printed on -- and a second, closer set once the sheet
            // has been through the press enough times to show it.
            float ly = uv.y * u_st_res.y;
            col = mix(col, inkc,
                    (1.0 - smoothstep(0.0, 0.07, fract(ly / 21.0))) * 0.20 * pr);
            col = mix(col, inkc,
                    (1.0 - smoothstep(0.0, 0.09, fract(ly / 10.5 + 0.5)))
                    * 0.13 * pr * churn);

            // REDACTED. Six rules, each growing from its own left edge and
            // overshooting the silhouette, because a redaction always covers
            // more than the thing it covers.
            float bars = clamp(u_st_bars, 0.0, 1.0);
            float bar = 0.0;
            float baredge = 0.0;
            for (int i = 0; i < 6; i++) {
                float fi = float(i);
                float on = smoothstep(fi / 7.0, fi / 7.0 + 0.20, bars);
                float by = 0.10 + 0.80 * st_hash(vec2(fi, 21.0));
                float bh = (0.017 + 0.030 * st_hash(vec2(fi, 33.0)))
                        * (0.7 + 2.9 * bars);
                float x0 = 0.08 + 0.14 * st_hash(vec2(fi, 45.0));
                float x1 = x0 + (0.90 - x0) * on;
                float band_y = step(abs(uv.y - by), bh * 0.5);
                float band_x = step(x0, uv.x) * step(uv.x, x1);
                bar = max(bar, band_y * band_x * step(0.001, on));
                float ey = step(abs(uv.y - by), bh * 0.5 + 0.010);
                float ex = step(x0 - 0.008, uv.x) * step(uv.x, x1 + 0.008);
                baredge = max(baredge, ey * ex * step(0.001, on));
            }

            col = mix(col, vec3(0.0), bar);
            // A bar is WET INK, not a black rectangle: it pools at its own
            // edge and darkens the stock just outside itself.
            col = mix(col, inkc * 0.55, clamp(baredge - bar, 0.0, 1.0) * 0.75);
            float gone = smoothstep(0.88, 1.0, bars);
            a = max(a, bar) * (1.0 - gone);

            // ---- THE PLATE CONTRACT (shared by every Archivist body) -------
            // Two things every one of these shaders has to do on its last
            // line, and none of them did until Aug 23 2026.
            //
            // 1. PREMULTIPLIED ALPHA. gl2 blends src + dst * (1 - a), so a
            //    pixel whose RGB is brighter than its own alpha ADDS light --
            //    and at alpha zero with bright RGB it adds light while
            //    claiming to be invisible. Every one of these shaders moves
            //    colour around without reference to alpha somewhere, so all of
            //    them were painting the transparent MARGIN of the padded plate
            //    and drawing the plate's own rectangle on screen as a faint
            //    glowing box. Clamping RGB to alpha is the fix.
            //
            // 2. THE EDGE. A mesh shader is clipped dead at its plate
            //    rectangle, so anything still opaque at the boundary is cut in
            //    a straight line. Padding buys room; it guarantees nothing.
            //    The feather is measured in the plate's OWN untransformed
            //    coordinate, so warps, swells and strays cannot escape it.
            // Nonfiction was the worst offender of the three: `printed`
            // is a bright paper STOCK, mixed in wherever u_st_ink is up and
            // entirely regardless of alpha, so the whole transparent margin
            // sat at roughly 0.74 grey with an alpha of zero -- a lit box the
            // size of the plate, on a dark room.
            vec2 pe = min(plate_uv, vec2(1.0) - plate_uv);
            a *= smoothstep(0.0, 0.050, min(pe.x, pe.y));

            gl_FragColor = vec4(min(col, vec3(a)), a);
        """)

    try:
        _nf_register_plain()
        NF_PLAIN_OK = True
    except Exception as _nf_pl_e:
        NF_PLAIN_OK = False
        try:
            renpy.log("INV FX: plain shader failed: %r" % _nf_pl_e)
        except Exception:
            pass

    try:
        _nf_register_strike()
        NF_STRIKE_OK = True
    except Exception as _nf_st_e:
        NF_STRIKE_OK = False
        try:
            renpy.log("INV FX: strike shader failed: %r" % _nf_st_e)
        except Exception:
            pass


# --- CONSTANTS AND TUNING ----------------------------------------------------
init python:
    NF_SOUP_IMG = INV_DIR + "hyperspace.png"
    NF_SPRITE = INV_DIR + "nonfiction.png"

    # PLACEHOLDER ART. nonfiction.png is a stand-in; these three lines are the
    # only thing that has to change when the finished portrait lands.
    NF_SPRITE_W, NF_SPRITE_H = 1024, 1536
    # The figure does not sit in the middle of its own canvas (alpha bbox is
    # 115,63 - 804,1536), so centring the plate would hang it off to one side.
    # FORMULA: NF_FIG_D* = (canvas centre) - (bbox centre), per axis.
    NF_FIG_DX, NF_FIG_DY = 52.5, -31.5

    NF_ZOOM_ACT1 = 0.28
    # A plate is a TEXTURE and textures cap at 4096px here. 1536 * 0.90 * 1.5
    # padding is ~2074px, comfortably inside; anything above this zoom is
    # applied to the finished mesh instead of rasterised into the plate.
    NF_PLATE_MAX_ZOOM = 0.90
    # Act two: it stops being a figure standing in the room and becomes the
    # WATERMARK ON THE PAGE -- large, faint, behind everything, and it never
    # walks anywhere. It only ever re-registers.
    NF_ZOOM_MARK = 0.62
    NF_MARK_ALPHA = 0.16

    # --- act one -------------------------------------------------------------
    NF_HP_MAX = 280
    NF_SRC_MAX = 40
    NF_STANDING_MAX = 1000
    NF_SHIFT_LEDGER = 480
    # 18, not 15. Measured: the STATE STATE CITE loop plus the AMEND turns
    # that pay for it lands on ~480 sourced around turn 16-18, so a cap of 15
    # was ending the bout on the clock instead of on the ledger and quietly
    # holding the hand-off below its own ceiling (measured 34 where 45 was
    # available).
    NF_SHIFT_TURN_CAP = 18

    # THE ESCROW. STATE puts a claim on the board UNSOURCED; only CITE moves
    # it onto the ledger, and only the ledger is real.
    NF_STATE_LO, NF_STATE_HI = 56, 84
    NF_STATE_SCRUT = 9
    NF_CITE_COST = 10
    NF_CITE_SCRUT = 20
    NF_AMEND_HEAL = 70
    NF_AMEND_SRC = 12
    NF_AMEND_SCRUT = 26
    NF_AMEND_PENDING = 0.34        # your own retraction, taken willingly
    NF_GUARD_MULT = 0.45           # AMEND is the guard as well as the heal

    NF_SCRUT_MAX = 100
    NF_SCRUT_START = 12
    NF_SCRUT_STEP_LO, NF_SCRUT_STEP_HI = 6, 10
    NF_SCRUT_FLOOR = 45            # where it falls back to after an erratum

    NF_QUERY_BASE = 18
    NF_QUERY_PER_PENDING = 0.22    # carrying a pile is what makes this hurt
    NF_FOOTNOTE_DMG = 14
    NF_FOOTNOTE_BLEED = 3
    NF_STRIKE_DMG = 24
    NF_CORROBORATE = 22
    NF_ERRATUM_LEDGER = 90         # it corrects something you already sourced
    NF_ERRATUM_DMG = 52

    # --- act two: the page ---------------------------------------------------
    # Flat, orthographic, overhead. No projection helpers in this file at all,
    # which is the point.
    NF_COLS, NF_ROWS = 8, 5
    NF_CELL_W, NF_CELL_H = 107, 92
    NF_PLANE_X, NF_PLANE_Y = 212, 176
    NF_PLANE_W = NF_COLS * NF_CELL_W          # 856
    NF_PLANE_H = NF_ROWS * NF_CELL_H          # 460

    NF_SPEED = 4.2                 # px per tick; one cell is ~26 ticks
    NF_PLAYER_R = 13.0

    # =========================================================================
    # THE ESCROW, CARRIED THROUGH THE TEAR
    # =========================================================================
    # The first build of act two dropped act one's one good idea at the door.
    # Act one is an escrow -- a claim is worth nothing until it is SOURCED --
    # and act two replaced that with a single bar that filled while you stood
    # somewhere. Which is a fine picture and a thin loop: go to the box, stand
    # in the box, dodge the walls. Nothing you did was ever at risk, so
    # nothing you did was ever a decision.
    #
    # SO THE ESCROW COMES WITH YOU. Standing on the entry fills PENDING, and
    # pending is not on the record. Pending is taken by a retraction, taken by
    # a redaction landing on you, and capped -- so you cannot fill the whole
    # bar in one sitting even if the page lets you. It becomes VERIFIED only
    # when you walk it into THE MARGIN, which is where a citation goes.
    #
    # The loop is now FILL, CARRY, FILE, and every part of it is exposed to a
    # different thing: filling is exposed to the volleys landing around you,
    # carrying is exposed to the page having closed behind you while you
    # stood there, and filing is exposed to which margin rows are still open.
    # And VERIFIED cannot be taken by anything, which is the act-one rule
    # ("only the ledger is real") honoured rather than restated -- it also
    # means there is no death spiral, only lost time.
    NF_VERIFY_MAX = 100.0
    # 0.100, up from 0.065, which was itself up from 0.048. The escrow adds a
    # walk to every fill, so the fill itself has to come in faster or the act
    # doubles in length -- measured, at 0.085 the naive bot ran 69-165s
    # against the old build's 48-69s, and half of that was time and half was
    # eating a retraction it could have avoided. At 0.100 a full pending is
    # 340 ticks, which fits INSIDE NF_RETRACT_EVERY: a player who starts a
    # fill on a clean clock can finish it, and only a player who starts one
    # late has a decision to make. That relationship is the tuning, not the
    # number.
    NF_FILL = 0.100                # standing still on the anchor
    NF_FILL_ATTEST = 0.200
    NF_VERIFY_FLOOR, NF_VERIFY_CEIL = 8.0, 45.0   # what act one can hand over
    # HOW MUCH YOU CAN CARRY AT ONCE. This is the whole pacing dial: raise it
    # and the act becomes two long sittings, lower it and it becomes a
    # shuttle. It is also the size of the thing a retraction can take, which
    # is the other reason it cannot be large.
    NF_PEND_MAX = 34.0

    # THE MARGIN. Column 0 of the grid, and it is not part of the maze: no
    # redaction may ever touch it (a redaction covers text, and the margin is
    # not text), the entry is never placed in it, and standing anywhere in it
    # files whatever you are carrying.
    #
    # ONE ROW AT A TIME, THOUGH. A citation is printed where it was filed and
    # the ink is wet, so that row will not take another for a while -- which
    # keeps the route from the entry to the margin from being the same walk
    # three times running.
    NF_MARGIN_COL = 0
    NF_MARGIN_REOPEN = 520
    NF_BANK_MIN = 3.0              # not worth the walk below this

    NF_HP2_MAX = 280
    # 22, down from 26. Health is now the ONLY loss condition in the act --
    # the record cannot be taken back any more, so a slow player no longer
    # bleeds out on the bar, they only lose time. Which means every death is
    # a death by redaction, and thirteen of them is a fairer number than ten
    # for a player who is still learning where the page closes.
    NF_HIT_HP = 22
    NF_HIT_PEND = 12.0             # being struck takes what is not filed yet
    # 54, up from 44. Aimed squarely at the population it exists for: it
    # changes nothing for a player who is not being hit, and it stops a player
    # who has just lost the thread from being hit twice on the way out.
    NF_IFRAMES = 54

    # CREDIT. What ATTEST costs.
    #
    # EVERY USE OF ATTEST IS OPT-IN. An earlier pass built a full-height sweep
    # that could only be answered by attesting, and then funded attesting at a
    # regen of 0.075 -- below what that sweep demanded, with the shortfall
    # only repayable through a near miss nothing on screen teaches. The result
    # was a hazard that always connected and a verb nobody could afford: the
    # act was arithmetically unwinnable for anyone not playing it perfectly.
    # The sweep is gone (see the note in _plan_volley) and the three things
    # ATTEST now does are all things you choose: fill at double rate, refuse a
    # retraction, and refuse ink on the cell you are standing in. Nothing in
    # the act REQUIRES it, so the regen only has to make it a live option.
    NF_CREDIT_MAX = 100.0
    NF_ATTEST_DRAIN = 1.35         # per held tick  (40 ticks = 54)
    NF_ATTEST_REGEN = 0.14         # per idle tick -- one attest per ~390
    NF_ATTEST_NEARMISS = 16.0      # threading a volley buys another
    NF_ATTEST_MIN = 18.0           # cannot start below this
    NF_ATTEST_MAX_TICKS = 40
    NF_ATTEST_CD = 55

    # THE PRESS. Redaction PERSISTS inside a cycle -- the floor genuinely
    # shrinks -- and then the page is re-printed and comes back whole. That
    # rhythm is the fight: pressure builds for seven seconds, snaps clean, and
    # builds again a little faster.
    #
    # AND THE CYCLE LENGTHENS. That is the difficulty ramp for the second
    # half, and it is a better one than "more marks faster" because it does
    # not touch the fairness contract at all -- NF_MIN_ROOM still caps how
    # much ink can exist, so a longer cycle means the page spends longer AT
    # that cap rather than exceeding it. It goes from a clean sheet every six
    # seconds to a clean sheet every twelve, and near the end the press stops
    # lifting everything: the oldest marks come off and the rest stay, so the
    # page is never quite blank again.
    NF_PRESS_CYCLE = 340
    NF_PRESS_CYCLE_LATE = 700
    NF_PRESS_PARTIAL_AT = 0.62     # progress past which a press only half lifts
    NF_PRESS_KEEP = 0.45           # ...and how much of it stays
    NF_VOLLEY_FAR = 96             # ticks between volleys at the start
    NF_VOLLEY_NEAR = 58            # ...and by the finish
    NF_VOLLEY_WARN = 46            # telegraph: ~2 cells of travel at NF_SPEED
    NF_VOLLEY_MARKS_FAR = 2
    NF_VOLLEY_MARKS_NEAR = 5
    # A REDACTION COVERS A PHRASE, NOT A LINE. Strikes used to take out whole
    # rows and columns, which is 20% and 12.5% of the page each, and with four
    # of them stacking inside a press cycle the board went almost entirely
    # black -- "the moving walls would always hit because they swiped past the
    # whole screen". They are contiguous runs of this many cells now, which is
    # both fairer and a much better picture of the thing they are.
    NF_SEG_LEN_H = (2, 4)
    NF_SEG_LEN_V = (2, 3)
    NF_INK_RATE = 0.14             # a strike sweeps in like a marker
    # Open cells the fairness check will not go below, of NF_COLS * NF_ROWS.
    # At 8 of 40 the guarantee was technically met and practically worthless:
    # a page that is 80% ink is one you are walled into whether or not a path
    # exists. 18 keeps the page navigable rather than merely connected.
    NF_MIN_ROOM = 18

    NF_ANCHOR_LIFE = (240, 340)
    NF_ANCHOR_MIN_DIST = 3         # cells; a new anchor is always a run away

    # THE WARNING HAS TO BE LONG ENOUGH TO RUN ON. At 60 ticks it was not:
    # the entry is placed at least NF_ANCHOR_MIN_DIST cells from wherever you
    # were, so the walk to the margin is 76-178 ticks, and a 60-tick telegraph
    # left exactly one answer to a retraction -- ATTEST -- which is rationed.
    # That is the toll this act was rebuilt once already to stop being (see
    # the note above NF_CREDIT_MAX; the sweep died of the same disease). At
    # 140 there are two ungated answers and they cost different things: hold
    # your ground and spend credit, or abandon the rest of the fill and go
    # and file what you have got. Measured: the naive bot -- fills to the cap,
    # never attests, never reacts to a telegraph -- went from 82-212s and one
    # loss in six to the figures in BALANCE.
    NF_RETRACT_EVERY = 560
    NF_RETRACT_WARN = 140
    # IT RETRACTS WHAT IS NOT SOURCED, which is the whole point of it and was
    # not what it used to do. It took a percentage of the RECORD -- chosen
    # over a flat sum because a flat drain is a treadmill (measured at a flat
    # 9, a hesitant bot took 318-536s and then died), but a percentage of the
    # record is still the wrong object: an Archivist that can take back a
    # thing you sourced contradicts the only rule act one taught. It takes
    # most of what you are CARRYING now. That cannot spiral either -- there is
    # nothing to take from a player who just filed -- and it is legible in a
    # way a percentage never was, because you can see the pile it took.
    NF_RETRACT_PEND = 0.50
    NF_RETRACT_MIN = 6.0

    NF_FACT_EVERY = 150            # ticks between readout rows appearing

    NF_HEART_ZOOM = 2.6
    # Same figure the user pulled twice on the other two: it has to look
    # wrong without becoming the busiest object on screen.
    NF_HEART_WARP = 1.15

    # --- palette: ink, paper, and exactly one colour -------------------------
    NF_INK = "#0d0d10"             # act two: ink on paper
    NF_PAPER = "#e8e6de"
    NF_PALE = "#dcded6"            # act one: light on the dark room
    NF_DIM = "#8d918a"
    NF_FAINT = "#5a5f59"
    NF_RED = "#c2202f"             # the only colour anywhere in act two
    NF_WARN = "#c8a13c"
    NF_BLACK = "#050506"
    NF_RULE_COL = "#a9a89e"

    NF_CMDS = (("state", "STATE"), ("cite", "CITE"),
            ("amend", "AMEND"), ("run", "RUN"))

    def nf_cell_center(c, r):
        return (NF_PLANE_X + c * NF_CELL_W + NF_CELL_W * 0.5,
                NF_PLANE_Y + r * NF_CELL_H + NF_CELL_H * 0.5)

    def nf_cell_box(c, r):
        return (NF_PLANE_X + c * NF_CELL_W, NF_PLANE_Y + r * NF_CELL_H,
                NF_CELL_W, NF_CELL_H)

    # --- THE READOUT ---------------------------------------------------------
    # The corruptive state's signature: the numbers on screen stop being about
    # the person played and start being about the person playing.
    #
    # NOTHING HERE IS INVENTED. That is not a stylistic preference, it is the
    # only version of this idea that Nonfiction is allowed to do -- every row
    # is a figure the engine genuinely knows, read straight out of Matsu'Py's own
    # state, and a value that cannot be read honestly is OMITTED rather than
    # guessed at. No filesystem, no machine, no user: the game's own record.
    def nf_true_readouts(deaths=0):
        rows = []

        def add(key, value):
            if value:
                rows.append((key, value))

        try:
            rt = int(renpy.get_game_runtime())
            add("RUNTIME", "%d:%02d:%02d" % (rt // 3600, (rt // 60) % 60,
                                            rt % 60))
        except Exception:
            pass
        try:
            add("SEEN", "%d" % len(getattr(persistent, "_seen_ever", None) or {}))
        except Exception:
            pass
        try:
            add("SAVES", "%d" % len(renpy.list_saved_games(fast=True)))
        except Exception:
            pass
        try:
            add("RUNS", "%d" % int(getattr(persistent, "playthrough", 0) or 0))
        except Exception:
            pass
        try:
            losses = getattr(persistent, "inv_losses", None) or {}
            add("RETRACTED", "%d" % (int(losses.get("nonfiction", 0))
                                    + int(deaths)))
        except Exception:
            pass
        try:
            add("FENDED", "%d/%d" % (len(inv_fended()), len(INV_ARCHIVISTS)))
        except Exception:
            pass
        try:
            now = datetime.datetime.now()
            add("DATE", now.strftime("%Y-%m-%d"))
            add("LOCAL", now.strftime("%H:%M"))
        except Exception:
            pass
        try:
            info = renpy.get_renderer_info() or {}
            add("DRAWN", str(info.get("renderer", "")).upper())
        except Exception:
            pass

        return rows


# --- SIMULATION --------------------------------------------------------------
init python:
    class NFGame(object):
        """All of Nonfiction's live state, stepped at a fixed 60Hz by
        NFStage. Owns zero rendering."""

        def __init__(self, retry=False, deaths=0, debug=False, start_open=False,
                     resume=None):
            self.result = None
            self.paused = False
            self.debug = bool(debug)
            self.retry = bool(retry)
            self.deaths = int(deaths)
            self.god = inv_godmode_on()
            # THE CHECKPOINT carries the ledger: what act one sourced is what
            # the page starts with on record.
            self.checkpoint = None

            self.tick = 0
            self.clock = 0.0
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
            # The sheet it is printed on: it hangs, and it is struck.
            self.sheet_yaw = 0.0
            self.sheet_yawv = 0.0
            self.sheet_fall = 0.0       # the tear lays it flat: 0 hanging, 1 down

            # --- the party member ----------------------------------------------
            self.hp = NF_HP_MAX
            self.hp_shown = float(NF_HP_MAX)
            self.src = NF_SRC_MAX
            self.src_shown = float(NF_SRC_MAX)
            self.roll_cue = 0

            # --- the account ----------------------------------------------------
            # ledger  what you have SOURCED. Permanent. The only real number.
            # pending what you have merely STATED. It can all be taken back.
            self.ledger = 0
            self.pending = 0
            self.ledger_shown = 0.0
            self.pending_shown = 0.0
            self.scrutiny = float(NF_SCRUT_START)

            # --- act one ---------------------------------------------------------
            self.mode = "arrive"
            self.mtick = 0
            self.turn = 0
            self.cursor = 0
            self.guard = False
            self.bleed = 0
            self.marked = False
            self.last_cmd = None
            self.last_enemy = None

            self.beat_label = ""
            self.beat_value = ""
            self.beat_after = "menu"

            # --- presentation ------------------------------------------------------
            self.flash = 0.0
            self.dark = 1.0
            self.shake = 0.0
            self.freeze = 0
            self.open = 0.0            # 0 = the room, 1 = the page
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
            self.press = 0.0           # the press coming down
            self.reg = 0.0             # registration seed; steps, never slides
            self.body_bars = 1.0       # how much of it is struck out
            self.body_ink = 0.0        # how much of it has been printed
            self.beat = 0.0
            self.beat_pulse = 0.0
            self.struck_out = 0        # the pile the tear takes back

            # --- act two ------------------------------------------------------------
            self.px = 640.0
            self.py = 400.0
            self.trail = []
            self.verify = 0.0
            self.verify_shown = 0.0
            self.pend2 = 0.0           # act two's escrow: filled, not filed
            self.pend2_shown = 0.0
            self.margin_cd = {}        # row -> ticks until it takes another
            self.credit = NF_CREDIT_MAX
            self.attest = 0            # ticks held so far
            self.attest_cd = 0
            self.attesting = False
            self.iframes = 0
            self.still = 0             # consecutive ticks without moving

            self.struck = {}           # (c, r) -> {"ink": 0..1, "dir": "h"/"v"}
            self.pending_lines = []    # telegraphed, not yet inked
            self.volley_t = 0
            self.volley_warn = 0
            self.press_t = NF_PRESS_CYCLE
            self.dist = 0.0            # ticks survived, for the difficulty ramp

            self.anchor = None         # (c, r)
            self.anchor_life = 0
            self.retract_t = 0
            self.retract_warn = 0

            self.facts = []
            self.facts_shown = 0
            self.fact_t = 0

            self.hud_fade = 1.0
            self.end_wipe = 0.0        # the loss: the page filling in
            self.end_bar = 0.0         # the loss: the bar drawn over you
            self.leave_bars = 0.0      # the win: the bars going across IT
            self.bank_flash = 0.0      # a citation just went into the margin

            self.keys = MSBFKeyLatch()
            self._prev = {"left": False, "right": False, "up": False,
                        "down": False, "z": False, "x": False}

            if resume:
                self.ledger = int(resume.get("ledger", 300))
                self._begin_page(dev=True)
                self.dark = 1.0
            elif start_open:
                # Dev entry skips the bout, so hand over a middling account --
                # a shift that never happened cannot have sourced anything.
                self.ledger = 300
                self._begin_page(dev=True)

        # ----- helpers -----------------------------------------------------------

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
            """What is left of its account of you."""
            return max(0, NF_STANDING_MAX - self.ledger - self.pending)

        def standing_frac(self):
            return inv_clamp(self.standing() / float(NF_STANDING_MAX), 0.0, 1.0)

        def scrut_frac(self):
            return inv_clamp(self.scrutiny / float(NF_SCRUT_MAX), 0.0, 1.0)

        def verify_frac(self):
            return inv_clamp(self.verify / NF_VERIFY_MAX, 0.0, 1.0)

        def progress(self):
            """0 at the tear, 1 by the time act two should be over."""
            return inv_clamp(self.dist / 5400.0, 0.0, 1.0)

        def churn(self):
            """HOW HARD THE PAGE IS BEING WORKED, 0 to 1.

            The single input to every escalating decoration in act two, and it
            is deliberately ONE number rather than a set of thresholds: the
            act should get busier the way a page gets busier, continuously and
            without a moment where a new layer switches on. Half of it is how
            long you have been on the page and half is how far onto the record
            you have got, so a slow run and a fast one both arrive at the same
            noise by the end.
            """
            return inv_clamp(0.5 * self.progress()
                            + 0.5 * (self.verify / NF_VERIFY_MAX), 0.0, 1.0)

        def pend_frac(self):
            return inv_clamp(self.pend2 / NF_PEND_MAX, 0.0, 1.0)

        def margin_open(self, r):
            """Is that row of the margin dry enough to take a citation."""
            return self.margin_cd.get(r, 0) <= 0

        def _reprint(self, strength=1.0):
            """A registration pass. Everything printed jumps at once."""
            self.press = max(self.press, inv_clamp(strength, 0.0, 1.0))
            self.reg += 1.0 + self.rng.random()

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

        def _fx_ink(self, x, y, n=3, size=(0.25, 0.55), layer="front",
                    col="#0b0b0d", alpha=0.92):
            """Wet ink thrown off a strike: splats that land and stay a while."""
            self.fx.burst(INV_INKS, x, y, n, speed=(0.0, 0.6), life=(50, 90),
                          size=size, col=col, alpha=alpha, add=False, drag=0.9,
                          jitter=18.0, fade="late", layer=layer)

        def _fx_scraps(self, x, y, n=8, layer="front", col="#e6e2d6",
                       spread=(1.5, 5.0)):
            """Paper coming off: torn scraps that flutter and fall."""
            self.fx.burst(INV_SCRAPS, x, y, n, speed=spread, life=(40, 75),
                          size=(0.25, 0.55), col=col, alpha=0.95, add=False,
                          drag=0.95, ay=0.10, vrot=(-9.0, 9.0), layer=layer,
                          fade="late")

        def _fx_strike_window(self, big=False):
            """Act one: something struck out of the window that stands in for
            you -- a bar of ink across it, and the spatter."""
            x1, y1 = 1004.0, 612.0
            self.fx.emit("beam", x1, y1, life=26 if big else 18, size=1.9,
                         size1=1.9, col="#050506", alpha=0.95, add=False,
                         layer="hud", fade="late", sq=0.34)
            self._fx_ink(x1 + self.rng_fx.uniform(-120, 120), y1, 3 if big else 2,
                         layer="hud")
            self.panel_kick = 1.0
            self._kick_lens(x1, y1, 0.7 if big else 0.35, 0.005 if big else 0.002)

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
                col = NF_DIM if self.god else (NF_RED if self.open > 0.5
                                            else NF_WARN)
                self.float_text(x, y, "-%d" % amount, col, True)

        def bank(self):
            """Move the unsourced pile onto the ledger. The only thing in this
            fight that makes damage permanent."""
            moved = self.pending
            self.ledger = int(min(NF_STANDING_MAX, self.ledger + moved))
            self.pending = 0
            return moved

        # ----- input ---------------------------------------------------------------

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

        # ----- dispatcher ------------------------------------------------------------

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
            elif mode == "page":
                self._step_page(edges)
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
            self.press *= 0.83

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
            # The sheet hangs on a spring: struck, it swings, and settles.
            # Its idle sway is the room's air, on two unrelated periods.
            idle = (0.045 * math.sin(self.clock * 0.41)
                    + 0.020 * math.sin(self.clock * 0.67 + 1.3))
            self.sheet_yawv += (idle - self.sheet_yaw) * 0.020
            self.sheet_yawv *= 0.94
            self.sheet_yaw += self.sheet_yawv
            if self.dark > 0.0 and self.mode == "page" and self.mtick < 70:
                self.dark = max(0.0, self.dark - 0.03)

            for attr, real in (("hp_shown", self.hp), ("src_shown", self.src)):
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

            # The account rolls too -- a retraction has to be watched arriving.
            for attr, real in (("ledger_shown", self.ledger),
                            ("pending_shown", self.pending)):
                shown = getattr(self, attr)
                gap = abs(shown - real)
                if gap > 0.01:
                    setattr(self, attr,
                            inv_approach(shown, float(real),
                                        inv_clamp(gap * 0.10, 0.6, 9.0)))
                else:
                    setattr(self, attr, float(real))

            gap = abs(self.verify_shown - self.verify)
            if gap > 0.005:
                self.verify_shown = inv_approach(self.verify_shown, self.verify,
                                                inv_clamp(gap * 0.12, 0.05, 1.4))
            else:
                self.verify_shown = self.verify

            # The escrow rolls too, and a bit faster -- a retraction taking it
            # has to be watched arriving, but a filing should feel like a
            # decision landing rather than a needle drifting.
            gap = abs(self.pend2_shown - self.pend2)
            if gap > 0.005:
                self.pend2_shown = inv_approach(self.pend2_shown, self.pend2,
                                                inv_clamp(gap * 0.18, 0.05, 2.2))
            else:
                self.pend2_shown = self.pend2
            self.bank_flash *= 0.90

            for f in self.floats:
                f["y"] += f["vy"]
                f["vy"] += 0.055
                f["life"] -= 1
            self.floats = [f for f in self.floats if f["life"] > 0]

            if self.hp_shown <= 0.0 and self.mode not in ("leave_w", "leave_l",
                                                        "arrive"):
                self._begin_leave(False)

        # =====================================================================
        # ARRIVAL -- it does not climb out, it is PRINTED
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
                self.body_bars = 1.0
                self.body_ink = 0.0
            elif t < 220:
                # THREE PASSES. Nothing moves between them; each one simply has
                # more of it on the page than the one before.
                self.hole[3] = 1.0
                self.emerge = 1.0 - inv_clamp((t - 70) / 150.0, 0.0, 1.0)
                if t in (74, 124, 174):
                    self._reprint(1.0)
                    self.play("phase", 0.55)
                    self.flash = 0.30
                    self.shake = 0.35
                step_i = 0 if t < 124 else (1 if t < 174 else 2)
                self.body_bars = (0.82, 0.52, 0.16)[step_i]
                self.body_ink = (0.35, 0.72, 1.0)[step_i]
            elif t < 275:
                u = (t - 220) / 55.0
                self.emerge = 0.0
                self.body_bars = inv_lerp(0.16, 0.0, inv_smooth(u))
                self.body_ink = 1.0
                self.hole[3] = 1.0 - inv_smooth(u)
                self.hole[2] = inv_lerp(250.0, 30.0, inv_smooth(u))
            elif t == 275:
                self.hole[3] = 0.0
                self.body_bars = 0.0
                inv_music_survey()
            elif t >= 310:
                self._begin_player_turn()

        # =====================================================================
        # ACT ONE -- THE SOURCING BOUT
        # =====================================================================

        def _begin_player_turn(self):
            # The cursor stays where you left it.
            self.mode = "menu"
            self.mtick = 0
            self.turn += 1
            self.guard = False

        def _step_menu(self, edges):
            self.mtick += 1
            n = len(NF_CMDS)
            if edges["up"]:
                self.cursor = (self.cursor - 1) % n
                self.play("cursor")
            elif edges["down"]:
                self.cursor = (self.cursor + 1) % n
                self.play("cursor")
            if edges["z"]:
                self.play("confirm")
                self._resolve_player(NF_CMDS[self.cursor][0])

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

        def _resolve_player(self, cmd):
            self.last_cmd = cmd
            label, value = cmd.upper(), ""

            if cmd == "state":
                claim = self.rng.randint(NF_STATE_LO, NF_STATE_HI)
                room = max(0, NF_STANDING_MAX - self.ledger - self.pending)
                claim = min(claim, room)
                self.pending += claim
                self.scrutiny = min(float(NF_SCRUT_MAX),
                                    self.scrutiny + NF_STATE_SCRUT)
                self.play("bash")
                self.shake = 0.30
                self._reprint(0.45)
                # A claim is SET: a slug of type struck into the sheet.
                hx = 640.0 + self.rng_fx.uniform(-70.0, 70.0)
                hy = 250.0 + self.rng_fx.uniform(-60.0, 90.0)
                self._fx_ink(hx, hy, 2)
                self.fx.burst("spark", hx, hy, 8, speed=(2.0, 6.0), life=(8, 14),
                              size=(0.18, 0.30), col="#dcded6", stretch=0.12,
                              drag=0.85, layer="front")
                self.sheet_yawv += 0.020 * (1.0 if self.rng_fx.random() < 0.5 else -1.0)
                self._kick_lens(hx, hy, 0.35, 0.003)
                value = "-" + str(claim) + " UNSOURCED"

            elif cmd == "cite":
                if self.src < NF_CITE_COST:
                    self.play("cancel")
                    self._beat("CITE", "NO SOURCES", "menu")
                    return
                if self.pending <= 0:
                    self.play("cancel")
                    self._beat("CITE", "UNSOURCED  0", "menu")
                    return
                self.src -= NF_CITE_COST
                moved = self.bank()
                self.scrutiny = max(0.0, self.scrutiny - NF_CITE_SCRUT)
                self.play("scan")
                self.flash = 0.20
                self._reprint(0.8)
                # SOURCED: a stamp comes down on it. Dry ink, no spatter.
                self.fx.ring(640.0, 300.0, 120.0, 150.0, life=22, col="#0b0b0d",
                             alpha=0.75, add=False, layer="front")
                self.fx.ring(640.0, 300.0, 108.0, 136.0, life=22, col="#0b0b0d",
                             alpha=0.55, add=False, layer="front")
                self.sheet_yawv += 0.035
                self._kick_lens(640.0, 300.0, 0.6, 0.004)
                value = "-" + str(moved)

            elif cmd == "amend":
                # The honest move, and honesty costs. You take back a third of
                # everything you have not sourced yet, and in exchange you get
                # the turn off, the health, the sources and the quiet.
                given = int(self.pending * NF_AMEND_PENDING)
                self.pending = max(0, self.pending - given)
                self.hp = int(min(NF_HP_MAX, self.hp + NF_AMEND_HEAL))
                self.src = int(min(NF_SRC_MAX, self.src + NF_AMEND_SRC))
                self.scrutiny = max(0.0, self.scrutiny - NF_AMEND_SCRUT)
                self.guard = True
                self.play("heal")
                # Correction tape drawn across it, and the claim coming off.
                self.fx.emit("beam", 640.0, 300.0, life=30, size=1.7, size1=1.8,
                             col="#f2f0e8", alpha=0.85, add=False, layer="front",
                             fade="late", sq=0.45)
                self._fx_scraps(640.0, 300.0, 6)
                value = "+" + str(NF_AMEND_HEAL)
                if given:
                    value += "   +" + str(given) + " UNSOURCED"

            elif cmd == "run":
                # It never works, and it is never explained.
                self.play("miss")
                self.shake = max(self.shake, 0.4)
                self._reprint(0.6)
                value = "UNRECORDED"

            after = "enemy"
            if self.ledger >= NF_SHIFT_LEDGER:
                after = "shift"
            self._beat(label, value, after)

        def _pick_enemy_move(self):
            if self.marked:
                return "strike"
            pool = ["query", "query", "footnote"]
            if self.pending >= 90:
                pool.append("mark")
                pool.append("mark")
            elif self.turn >= 3:
                pool.append("mark")
            if self.standing_frac() < 0.70:
                pool.append("corroborate")
            if self.last_enemy in pool and len(set(pool)) > 1:
                pool = [m for m in pool if m != self.last_enemy] or pool
            return self.rng.choice(pool)

        def _step_enemy(self):
            self.mtick += 1
            if self.mtick < 26:
                # Its turn: the sheet trembles on its line.
                self.windup = min(1.0, self.windup + 0.06)
                return

            self.scrutiny = min(float(NF_SCRUT_MAX),
                                self.scrutiny + self.rng.randint(
                                    NF_SCRUT_STEP_LO, NF_SCRUT_STEP_HI))

            # THE CAPSTONE. Scrutiny full: it does not merely erase what you
            # never sourced, it corrects something you did.
            if self.scrutiny >= NF_SCRUT_MAX:
                self.scrutiny = float(NF_SCRUT_FLOOR)
                lost = self.pending
                self.pending = 0
                back = min(self.ledger, NF_ERRATUM_LEDGER)
                self.ledger -= back
                self.marked = False
                self.last_enemy = "erratum"
                self.play("break", 0.95)
                self.flash = 0.75
                self.shake = 1.0
                self._reprint(1.0)
                dmg = NF_ERRATUM_DMG
                if self.guard:
                    dmg = int(dmg * NF_GUARD_MULT)
                self.hurt(dmg, 1004, 586)
                self._fx_strike_window(big=True)
                for k in range(4):
                    self.fx.emit("beam", 640.0, 200.0 + k * 62.0, life=40,
                                 size=1.6, size1=1.7, col="#050506",
                                 alpha=0.95, add=False, layer="front",
                                 fade="late", delay=k * 4, sq=0.30)
                self._fx_scraps(640.0, 300.0, 12)
                self.tear = 0.8
                self.guard = False
                value = "+" + str(back)
                if lost:
                    value += "   +" + str(lost) + " UNSOURCED"
                self._beat("ERRATUM", value, self._after_enemy(), kind="it")
                return

            move = self._pick_enemy_move()
            self.last_enemy = move
            label = move.upper()
            value = ""
            dmg = 0

            if move == "query":
                # Carrying a pile is what makes this hurt.
                dmg = int(NF_QUERY_BASE + NF_QUERY_PER_PENDING * self.pending)
                self.fx.ring(1004.0, 612.0, 80.0, 70.0, life=26, col="#0b0b0d",
                             alpha=0.8, add=False, layer="hud", squash=0.45)
            elif move == "footnote":
                dmg = NF_FOOTNOTE_DMG
                self.bleed = NF_FOOTNOTE_BLEED
                self.fx.burst("drip", 1004.0, 562.0, 5, speed=(0.0, 0.4),
                              life=(30, 50), size=(0.4, 0.8), col="#0b0b0d",
                              alpha=0.9, add=False, drag=1.0, ay=0.18,
                              angle=90.0, spread=10.0, jitter=150.0,
                              squash=0.1, rot=0.0, layer="hud", delay=(0, 10))
            elif move == "mark":
                # It says so a full turn in advance, because it always does.
                self.marked = True
                self.play("note", 0.9)
                self._reprint(0.5)
                for a in (40.0, -40.0):
                    self.fx.emit("beam", 1004.0, 612.0, life=60, size=0.55,
                                 size1=0.55, rot=a, col="#c2202f", alpha=0.85,
                                 add=False, layer="hud", fade="late", sq=0.6)
                value = "MARKED"
            elif move == "strike":
                lost = self.pending
                self.pending = 0
                self.marked = False
                dmg = NF_STRIKE_DMG
                self.play("cut_big", 0.9)
                self.flash = 0.25
                self.shake = 0.8
                self._reprint(1.0)
                self._fx_scraps(1004.0, 612.0, 10, layer="hud")
                if lost:
                    value = "+" + str(lost) + " UNSOURCED   "
            elif move == "corroborate":
                back = min(self.ledger, NF_CORROBORATE)
                self.ledger -= back
                label = "CORRECTION"
                self.play("refuse", 0.7)
                self.fx.emit("glyph_01", 520.0, 120.0, life=50, size=0.8,
                             col="#c2202f", alpha=0.9, add=False, layer="hud",
                             fade="late")
                value = "+" + str(back)

            if dmg > 0:
                if self.guard:
                    dmg = int(dmg * NF_GUARD_MULT)
                self.play("enemy", 0.8)
                self.hurt(dmg, 1004, 586)
                self._fx_strike_window(big=dmg >= 40)
                value += "-" + str(dmg)

            if self.bleed > 0 and move != "footnote":
                self.bleed -= 1
                self.hurt(11, 1004, 610)
                value += "   -11"

            self.guard = False
            self._beat(label, value, self._after_enemy(), kind="it")

        def _after_enemy(self):
            if self.ledger >= NF_SHIFT_LEDGER or self.turn >= NF_SHIFT_TURN_CAP:
                return "shift"
            return "menu"

        # =====================================================================
        # THE TEAR -- the unsourced pile is struck out and the room whitens
        # =====================================================================

        def _step_shift(self):
            self.mtick += 1
            t = self.mtick

            if t == 1:
                inv_music_stop(0.3)
                self.play("tear")
                # THE LESSON, ADMINISTERED ONCE. Everything still unsourced
                # goes, in front of you, before anything else happens.
                self.struck_out = self.pending
            if t == 30 and self.struck_out:
                self.pending = 0
                self.play("cut_big", 0.9)
                self.flash = 0.25
                self.shake = 0.9
                self._reprint(1.0)
                self.float_text(640, 300, "+" + str(self.struck_out)
                                + " UNSOURCED", NF_WARN, True)
                for k in range(3):
                    self.fx.emit("beam", 640.0, 220.0 + k * 70.0, life=60,
                                 size=1.5, size1=1.6, col="#050506", alpha=0.95,
                                 add=False, layer="front", fade="late",
                                 delay=k * 5, sq=0.30)
            if t == 60:
                # THE WINDOWS ARE TORN UP like the paper they are ruled on.
                self.panel_slide = 1.0
                for (bx0, by0, bw, bh) in (NFStage.PANEL_CMD, NFStage.PANEL_HUD):
                    for _k in range(26):
                        x = bx0 + self.rng_fx.uniform(0.0, bw)
                        y = by0 + self.rng_fx.uniform(0.0, bh)
                        self.fx.emit(INV_SCRAPS[_k % 4], x, y,
                                     vx=self.rng_fx.uniform(-2.0, 2.0),
                                     vy=self.rng_fx.uniform(-4.0, -0.5),
                                     life=self.rng_fx.randint(50, 80),
                                     size=self.rng_fx.uniform(0.45, 0.95),
                                     rot=self.rng_fx.uniform(0, 360),
                                     vrot=self.rng_fx.uniform(-8, 8),
                                     col=("#1a1b1e" if _k % 3 else "#dcded6"),
                                     add=False, drag=0.985, ay=0.14,
                                     layer="hud", fade="late")
                self.play("break", 0.6)
            if 60 <= t < 150:
                self.shake = max(self.shake, 0.3)
                self.sheet_yawv += 0.002 * math.sin(t * 0.9)
            if t == 150:
                self.play("slam")
                self.play("phase", 0.9)
                self.flash = 1.0
                self.shake = 1.0
                self._reprint(1.0)
                inv_music_corruptive()
                # Whole again for the second half: act one's currency was the
                # LEDGER, and that is what carries.
                self.hp = NF_HP2_MAX
                self.src = NF_SRC_MAX
            if 150 <= t < 230:
                # Every light in the room coming up at once -- and the sheet
                # comes down off its line and lies flat. It is the page.
                self.open = inv_clamp((t - 150) / 80.0, 0.0, 1.0)
                self.sheet_fall = inv_smooth(inv_clamp((t - 150) / 46.0, 0.0, 1.0))
            if t == 230:
                self.open = 1.0
                self._begin_page()

        # =====================================================================
        # ACT TWO -- THE PAGE
        # =====================================================================

        def _begin_page(self, dev=False):
            self.mode = "page"
            self.mtick = 0
            self.open = 1.0
            self.dark = 0.0
            self.hp = NF_HP2_MAX
            self.hp_shown = float(NF_HP2_MAX)

            # THE JOINT: what you sourced is what you start with on record.
            # It arrives as VERIFIED, not as pending: it was sourced in act
            # one, and a sourced thing is already on the record.
            self.verify = inv_clamp(
                NF_VERIFY_CEIL * (self.ledger / float(NF_SHIFT_LEDGER)),
                NF_VERIFY_FLOOR, NF_VERIFY_CEIL)
            self.verify_shown = self.verify
            self.pend2 = 0.0
            self.pend2_shown = 0.0
            self.margin_cd = {}

            self.credit = NF_CREDIT_MAX
            self.attest = 0
            self.attest_cd = 0
            self.attesting = False
            self.iframes = 0
            self.still = 0
            self.dist = 0.0

            self.px, self.py = nf_cell_center(NF_COLS // 2, NF_ROWS // 2)
            self.bank_flash = 0.0
            self.trail = []
            self.struck = {}
            self.pending_lines = []
            self.volley_t = 120
            self.volley_warn = 0
            self.press_t = NF_PRESS_CYCLE
            self.retract_t = NF_RETRACT_EVERY
            self.retract_warn = 0

            self.facts = nf_true_readouts(self.deaths)
            self.facts_shown = 0
            self.fact_t = NF_FACT_EVERY

            self._place_anchor(first=True)
            self.play("break", 0.8)
            self.sheet_fall = 1.0
            # THE CHECKPOINT: a loss from here can be retried from the tear,
            # with the same ledger act one sourced.
            self.checkpoint = {"slug": "nonfiction", "ledger": int(self.ledger)}
            if dev:
                inv_music_corruptive()

        # ----- the grid ------------------------------------------------------------

        def cell_of(self, x, y):
            c = int((x - NF_PLANE_X) // NF_CELL_W)
            r = int((y - NF_PLANE_Y) // NF_CELL_H)
            return (int(inv_clamp(c, 0, NF_COLS - 1)),
                    int(inv_clamp(r, 0, NF_ROWS - 1)))

        def _protected(self):
            """Cells no redaction may ever touch.

            THE MARGIN, first and unconditionally: a redaction covers text,
            and the margin is not text. That is the fiction and it is also the
            fairness rule that makes the escrow safe to build on -- the place
            you file a citation can never be inked out from under you, and
            since the margin runs the full height of the page there is always
            a way to reach it from anywhere the flood fill allows.

            And then the anchor and its four neighbours, as before: there is
            always somewhere to stand."""
            out = set((NF_MARGIN_COL, r) for r in range(NF_ROWS))
            if self.anchor is None:
                return out
            c, r = self.anchor
            out.add((c, r))
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c + dc, r + dr)
                if 0 <= n[0] < NF_COLS and 0 <= n[1] < NF_ROWS:
                    out.add(n)
            return out

        def _component(self, start, blocked):
            """Flood fill of open cells reachable from `start`. This is the
            whole fairness contract: nothing is committed until this says the
            page is still a place you can move around in."""
            if start in blocked:
                return set()
            seen = set([start])
            stack = [start]
            while stack:
                c, r = stack.pop()
                for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (c + dc, r + dr)
                    if not (0 <= n[0] < NF_COLS and 0 <= n[1] < NF_ROWS):
                        continue
                    if n in seen or n in blocked:
                        continue
                    seen.add(n)
                    stack.append(n)
            return seen

        def _roll_mark(self):
            """One redaction: a contiguous run of cells, horizontal or
            vertical. Never a whole row, never a whole column, and never in
            the margin -- rolling one there would only be filtered out again
            and would quietly eat a try off the budget in _plan_volley."""
            first = NF_MARGIN_COL + 1
            if self.rng.random() < 0.62:
                n = self.rng.randint(*NF_SEG_LEN_H)
                c0 = self.rng.randint(first, max(first, NF_COLS - n))
                r = self.rng.randrange(NF_ROWS)
                return ("h", set((c0 + i, r) for i in range(n)))
            n = self.rng.randint(*NF_SEG_LEN_V)
            r0 = self.rng.randint(0, max(0, NF_ROWS - n))
            c = self.rng.randrange(first, NF_COLS)
            return ("v", set((c, r0 + i) for i in range(n)))

        def _margin_in(self, comp):
            """Does this open component actually touch the margin.

            The margin can never be inked, but it CAN be walled off -- five
            marks down column 1 and the filing strip is on the other side of
            the page from you, which is not a hard fight, it is a stalled one.
            Nothing commits ink without this returning True."""
            return any((NF_MARGIN_COL, r) in comp for r in range(NF_ROWS))

        def _place_anchor(self, first=False):
            """Somewhere corroborated, and never where you already are.

            THE HARD PART IS NOT PICKING A CELL, IT IS GUARANTEEING YOU CAN
            REACH IT. Dropping the anchor into a pocket the player happens to
            be walled out of makes the whole fight unwinnable in complete
            silence -- there is no death, no message, just a run that can
            never end. So it is chosen out of the player's OWN open component,
            and then ink is LIFTED off the edge of that component until there
            is enough page around it to fight in. Which is also the fiction:
            the sheet is re-set around a corroborated fact, and as much of the
            sheet as that takes."""
            blocked = set(self.struck.keys())
            pc = self.cell_of(self.px, self.py)
            reach = self._component(pc, blocked)
            if not reach:
                self.struck.pop(pc, None)
                reach = set([pc])

            # NEVER IN THE MARGIN. The margin is where a citation is filed,
            # not where a claim is made, and an entry sitting in it would
            # collapse the whole loop into standing in one cell again.
            reach = set(cell for cell in reach if cell[0] != NF_MARGIN_COL)
            if not reach:
                reach = set([pc]) if pc[0] != NF_MARGIN_COL else \
                    set([(NF_MARGIN_COL + 1, pc[1])])

            far = [cell for cell in reach
                if max(abs(cell[0] - pc[0]), abs(cell[1] - pc[1]))
                >= NF_ANCHOR_MIN_DIST]
            if first:
                pool = sorted(reach)
            else:
                pool = far or sorted(reach - set([pc])) or sorted(reach)
            self.anchor = self.rng.choice(sorted(pool))
            self.anchor_life = self.rng.randint(*NF_ANCHOR_LIFE)

            # The neighbourhood of a corroborated fact is never struck...
            for cell in self._protected():
                self.struck.pop(cell, None)

            # ...and neither is enough of the page around it to move in, NOR
            # the route out to the margin. Both conditions lift ink off the
            # edge of the component until they hold.
            guard = 0
            while guard < NF_COLS * NF_ROWS:
                guard += 1
                comp = self._component(self.anchor, set(self.struck.keys()))
                if len(comp) >= NF_MIN_ROOM and self._margin_in(comp):
                    break
                edge = [cell for cell in self.struck
                        if any((cell[0] + dc, cell[1] + dr) in comp
                            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
                if not edge:
                    break
                self.struck.pop(self.rng.choice(sorted(edge)), None)

            # A telegraph aimed at what is now protected ground is dropped.
            prot = self._protected()
            for line in self.pending_lines:
                line["cells"] = [x for x in line["cells"] if x not in prot]
            self.pending_lines = [l for l in self.pending_lines if l["cells"]]
            self.play("note", 0.55)

        # ----- redaction -----------------------------------------------------------

        def _plan_volley(self):
            """Choose the marks to strike, refusing any that would seal the
            page.

            THE ONLY HAZARD IN THIS ACT IS THE PAGE CLOSING. There was a
            full-height rule sweeping across as well, and it was cut: it
            spanned the whole frame, so it could not be walked around, which
            left exactly one answer to it, and that answer was rationed. A
            hazard with a single gated answer is not difficulty, it is a
            toll. Everything here is dodgeable on foot.

            Refusal is silent and deliberate: a quiet volley is a better
            failure than an impossible one."""
            prog = self.churn()
            want = int(round(inv_lerp(NF_VOLLEY_MARKS_FAR,
                                    NF_VOLLEY_MARKS_NEAR, prog)))
            prot = self._protected()
            blocked = set(self.struck.keys())
            pc = self.cell_of(self.px, self.py)

            accepted = []
            tries = 0
            while len(accepted) < want and tries < 24:
                tries += 1
                direction, cells = self._roll_mark()
                cells = cells - prot - blocked
                if not cells:
                    continue
                trial = blocked | cells
                anchor_comp = self._component(self.anchor, trial)
                if len(anchor_comp) < NF_MIN_ROOM:
                    continue
                if not self._margin_in(anchor_comp):
                    continue
                if pc in cells:
                    # It may land on you -- you get ejected -- but only if
                    # there is somewhere in the anchor's component to be
                    # ejected TO.
                    if not any((pc[0] + dc, pc[1] + dr) in anchor_comp
                            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        continue
                elif pc not in anchor_comp:
                    continue
                blocked = trial
                accepted.append({"dir": direction, "cells": sorted(cells)})

            if not accepted:
                return
            self.pending_lines = accepted
            self.volley_warn = NF_VOLLEY_WARN
            self.play("wind", 0.45)

        def _commit_volley(self):
            """Ink everything telegraphed, hit whoever is standing in it, and
            re-check the page one last time."""
            # ATTEST REFUSES INK ON THE CELL YOU ARE STANDING IN. You are on
            # record for as long as you can back it, and a redaction cannot
            # cover something that is on record.
            here_now = self.cell_of(self.px, self.py)
            spared = here_now if self.attesting else None
            if spared is not None:
                self.play("refuse", 0.6)

            order = []
            for line in self.pending_lines:
                direction = line["dir"]
                for cell in line["cells"]:
                    if cell in self._protected() or cell == spared:
                        continue
                    self.struck[cell] = {"ink": 0.0, "dir": direction}
                    order.append(cell)
            self.pending_lines = []
            if not order:
                return

            self.play("cut", 0.7)
            self._reprint(0.55)
            self.shake = max(self.shake, 0.25)
            # Wet ink thrown off the end of every stroke that just landed.
            seen = 0
            for cell in order:
                if seen >= 6:
                    break
                if self.rng_fx.random() < 0.45:
                    cx_, cy_ = nf_cell_center(*cell)
                    self._fx_ink(cx_, cy_, 1, size=(0.18, 0.34))
                    seen += 1

            # LAST-RESORT RE-CHECK. You had NF_VOLLEY_WARN ticks to move and
            # may have moved somewhere the plan did not expect, so the whole
            # contract is proved again against the real board rather than the
            # predicted one: the anchor's open component has to be big enough
            # to fight in, and you have to be in it (or standing in ink, which
            # ejects you into it). The newest lines lift until both hold.
            guard = 0
            while order and guard < 12:
                guard += 1
                blocked = set(self.struck.keys())
                comp = self._component(self.anchor, blocked)
                here = self.cell_of(self.px, self.py)
                if (len(comp) >= NF_MIN_ROOM and self._margin_in(comp)
                        and (here in comp or here in blocked)):
                    break
                self.struck.pop(order.pop(), None)

            here = self.cell_of(self.px, self.py)
            if here in self.struck:
                self._struck_by_ink()
                return

            # THE SKILL CURVE, and it is paid at the moment it is earned: ink
            # landing in a cell NEXT to you buys back the credit that
            # attesting costs. A player who threads a volley can afford to
            # stand still when it counts; one who retreats to the emptiest
            # corner of the page cannot.
            close = 0
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if (here[0] + dc, here[1] + dr) in self.struck:
                    close += 1
            if close:
                self.credit = min(NF_CREDIT_MAX,
                                self.credit + NF_ATTEST_NEARMISS
                                * min(close, 2))
                self.play("graze", 0.5)

        def _struck_by_ink(self):
            """A redaction landed on the cell you were standing in."""
            if self.iframes > 0:
                return
            self._eject()
            self._take_hit(NF_HIT_HP)

        def _eject(self):
            """Redaction pushes you out of the text. It does not bury you."""
            blocked = set(self.struck.keys())
            comp = self._component(self.anchor, blocked) if self.anchor else set()
            pc = self.cell_of(self.px, self.py)
            best = None
            best_d = None
            for c in range(NF_COLS):
                for r in range(NF_ROWS):
                    if (c, r) in blocked:
                        continue
                    d = abs(c - pc[0]) + abs(r - pc[1])
                    if (c, r) not in comp:
                        d += 100          # prefer the anchor's side of the page
                    if best_d is None or d < best_d:
                        best_d = d
                        best = (c, r)
            if best is not None:
                self.px, self.py = nf_cell_center(*best)
                self.trail = []

        def _take_hit(self, amount):
            self.hurt(amount, self.px, self.py - 34)
            # It does not only cost health -- but what it takes is the
            # unsourced pile, same as everything else in this fight.
            before = self.pend2
            self.pend2 = max(0.0, self.pend2 - NF_HIT_PEND)
            if self.pend2 < before:
                self.float_text(self.px, self.py - 62,
                                "-%d" % int(before - self.pend2), NF_INK)
            self.iframes = NF_IFRAMES
            self.freeze = 4
            self.play("struck", 0.75)
            self._fx_ink(self.px, self.py, 3, size=(0.25, 0.5))
            self._fx_scraps(self.px, self.py, 5)
            self._kick_lens(self.px, self.py, 0.6, 0.006)

        # ----- the page's turn ------------------------------------------------------

        def _step_page(self, edges):
            self.mtick += 1
            self.dist += 1.0
            if self.freeze > 0:
                self.freeze -= 1
                return

            held = edges["held"]
            if self.iframes > 0:
                self.iframes -= 1

            # --- ATTEST ----------------------------------------------------------
            # The only verb. It roots you, it makes you unstrikeable, it fills
            # twice as fast, and it is the only answer to the rule and the only
            # refusal of a retraction. It costs CREDIT, and credit is bought by
            # dodging on your feet.
            if self.attest_cd > 0:
                self.attest_cd -= 1
            want = bool(held["z"]) and self.attest_cd <= 0
            if self.attesting:
                if (not want or self.credit <= 0.0
                        or self.attest >= NF_ATTEST_MAX_TICKS):
                    self.attesting = False
                    self.attest = 0
                    self.attest_cd = NF_ATTEST_CD
                else:
                    self.attest += 1
                    self.credit = max(0.0, self.credit - NF_ATTEST_DRAIN)
            elif want and self.credit >= NF_ATTEST_MIN:
                self.attesting = True
                self.attest = 0
                self.play("guard", 0.6)
            if not self.attesting:
                self.credit = min(NF_CREDIT_MAX, self.credit + NF_ATTEST_REGEN)

            # --- moving ---------------------------------------------------------
            dx = ((1.0 if held["right"] else 0.0)
                - (1.0 if held["left"] else 0.0))
            dy = ((1.0 if held["down"] else 0.0)
                - (1.0 if held["up"] else 0.0))
            if self.attesting:
                dx = dy = 0.0
            if dx and dy:
                dx *= 0.7071
                dy *= 0.7071

            moved = False
            if dx or dy:
                moved = self._move(dx * NF_SPEED, dy * NF_SPEED)
            self.still = 0 if moved else self.still + 1

            self.trail.insert(0, (self.px, self.py))
            if len(self.trail) > 9:
                self.trail.pop()

            # --- MAKING A CLAIM ----------------------------------------------------
            # Standing still on the entry fills PENDING, and pending is not on
            # the record. It stops dead at the cap: the page will not let you
            # sit in one cell and win, which is the thing the first build of
            # this act allowed and the reason it only had one decision in it.
            here_cell = self.cell_of(self.px, self.py)
            on_anchor = (self.anchor is not None and here_cell == self.anchor)
            filling = (on_anchor and (self.attesting or self.still > 4)
                    and self.pend2 < NF_PEND_MAX)
            if filling:
                rate = NF_FILL_ATTEST if self.attesting else NF_FILL
                self.pend2 = min(NF_PEND_MAX, self.pend2 + rate)
                if self.tick % 16 == 0:
                    self.play("tick", 0.30)

            # --- FILING IT ----------------------------------------------------------
            # A citation goes in the margin. Walk what you are carrying into
            # column zero and it stops being takeable -- and the row you filed
            # it on will not take another until the ink is dry, so the walk is
            # a different walk every time.
            if (here_cell[0] == NF_MARGIN_COL and self.pend2 >= NF_BANK_MIN
                    and self.margin_open(here_cell[1])):
                self._file(here_cell[1])

            if self.verify >= NF_VERIFY_MAX:
                self._begin_leave(True)
                return

            self._step_anchor()
            self._step_margin()
            self._step_press()
            self._step_facts()

        def _file(self, row):
            """The escrow closes. Whatever you were carrying becomes VERIFIED,
            and nothing in the encounter can take it back afterwards."""
            moved = self.pend2
            self.verify = min(NF_VERIFY_MAX, self.verify + moved)
            self.pend2 = 0.0
            self.margin_cd[row] = NF_MARGIN_REOPEN
            self.bank_flash = 1.0
            self.flash = max(self.flash, 0.10)
            self._reprint(0.5)
            self.play("confirm", 0.7)
            cx, cy = nf_cell_center(NF_MARGIN_COL, row)
            self.fx.ring(cx, cy, 30.0, 58.0, life=20, col="#0b0b0d", alpha=0.75,
                         add=False, layer="front")
            self._kick_lens(cx, cy, 0.4, 0.002)
            self.float_text(cx, cy - 30, "+%d" % int(moved), NF_INK, True)

        def _step_margin(self):
            for r in list(self.margin_cd.keys()):
                if self.margin_cd[r] > 0:
                    self.margin_cd[r] -= 1

        def _move(self, mx, my):
            """Ink is solid. Axis-separated so you slide along a redaction
            instead of sticking to it."""
            moved = False
            x0 = NF_PLANE_X + NF_PLAYER_R
            x1 = NF_PLANE_X + NF_PLANE_W - NF_PLAYER_R
            y0 = NF_PLANE_Y + NF_PLAYER_R
            y1 = NF_PLANE_Y + NF_PLANE_H - NF_PLAYER_R

            if mx:
                nx = inv_clamp(self.px + mx, x0, x1)
                if self.cell_of(nx, self.py) not in self.struck:
                    if nx != self.px:
                        moved = True
                    self.px = nx
            if my:
                ny = inv_clamp(self.py + my, y0, y1)
                if self.cell_of(self.px, ny) not in self.struck:
                    if ny != self.py:
                        moved = True
                    self.py = ny
            return moved

        def _step_anchor(self):
            self.anchor_life -= 1
            if self.anchor_life <= 0:
                self._place_anchor()

            # RETRACTION. It takes back the thing it granted -- unless you are
            # standing on it saying otherwise.
            if self.retract_warn > 0:
                self.retract_warn -= 1
                if self.retract_warn == 0:
                    if self.attesting:
                        self.play("refuse", 0.85)
                        self.flash = 0.30
                        self.float_text(self.px, self.py - 62, "REFUSED",
                                        NF_INK)
                    else:
                        # IT TAKES WHAT IS NOT SOURCED. Never the record --
                        # the record is the one thing in either act that is
                        # real, and an Archivist that can un-file a citation
                        # is contradicting the rule act one spent eighteen
                        # turns teaching. If you are carrying nothing it does
                        # nothing, and that is correct: it is not a punishment
                        # for existing, it is a reason to file.
                        before = self.pend2
                        take = max(NF_RETRACT_MIN,
                                self.pend2 * NF_RETRACT_PEND)
                        self.pend2 = max(0.0, self.pend2 - take)
                        self.play("cut_big", 0.75)
                        self.shake = max(self.shake, 0.5)
                        self._reprint(0.7)
                        if before > 0.0:
                            cx, cy = nf_cell_center(*self.anchor)
                            self.float_text(cx, cy - 30,
                                            "-%d" % int(before - self.pend2),
                                            NF_INK, True)
                        self._place_anchor()
                    self.retract_t = NF_RETRACT_EVERY + self.rng.randint(-90, 90)
            else:
                self.retract_t -= 1
                if self.retract_t <= 0:
                    self.retract_warn = NF_RETRACT_WARN
                    self.play("wind2", 0.7)

        def _step_press(self):
            """Ink is applied and it STAYS. The floor genuinely shrinks across
            a cycle, and then the page is re-printed and comes back whole."""
            for cell, data in self.struck.items():
                if data["ink"] < 1.0:
                    data["ink"] = min(1.0, data["ink"] + NF_INK_RATE)

            if self.volley_warn > 0:
                self.volley_warn -= 1
                if self.volley_warn == 0:
                    self._commit_volley()
                    prog = self.churn()
                    self.volley_t = int(inv_lerp(NF_VOLLEY_FAR, NF_VOLLEY_NEAR,
                                                prog)) + self.rng.randint(-8, 12)
                return

            self.volley_t -= 1
            if self.volley_t <= 0:
                self._plan_volley()
                if not self.pending_lines:
                    self.volley_t = 40

            self.press_t -= 1
            if self.press_t <= 0:
                # CHURN, NOT THE CLOCK. Driving the escalation off elapsed
                # time alone rebuilds the treadmill this act was fixed for
                # once already, just in a new costume: a player who is
                # struggling takes longer, and taking longer was making the
                # page permanently worse, which made them struggle. churn()
                # is half clock and half RECORD, so the page gets harder as
                # you get further onto it and a stuck player is left fighting
                # a page they can actually still fight.
                prog = self.churn()
                self.press_t = int(inv_lerp(NF_PRESS_CYCLE,
                                            NF_PRESS_CYCLE_LATE, prog))
                if self.struck:
                    # THE PRESS COMES DOWN. Everything struck lifts at once and
                    # the sheet is whole again for exactly as long as it takes
                    # to start filling in.
                    #
                    # LATE ON IT STOPS LIFTING EVERYTHING. The oldest marks
                    # come off and the newest stay, so the sheet is never
                    # quite blank again and the last third of the act is
                    # fought on a page that has been worked over. Ordering by
                    # ink is ordering by age -- a mark that has finished
                    # sweeping in has been there longest.
                    if prog >= NF_PRESS_PARTIAL_AT:
                        keep_n = int(len(self.struck) * NF_PRESS_KEEP)
                        newest = sorted(self.struck.items(),
                                        key=lambda kv: kv[1]["ink"])[:keep_n]
                        self.struck = dict(newest)
                        # The contract is re-proved against what is left, the
                        # same as anywhere else ink survives a decision.
                        guard = 0
                        while self.struck and guard < NF_COLS * NF_ROWS:
                            guard += 1
                            comp = self._component(self.anchor,
                                                set(self.struck.keys())) \
                                if self.anchor else set()
                            if (len(comp) >= NF_MIN_ROOM
                                    and self._margin_in(comp)):
                                break
                            self.struck.pop(
                                sorted(self.struck.keys())[0], None)
                    else:
                        self.struck = {}
                    self.play("slam", 0.6)
                    self.flash = 0.14
                    self._fx_scraps(640.0, 400.0, 10, spread=(2.0, 6.0))
                    self._kick_lens(640.0, 400.0, 0.8, 0.004)
                self._reprint(1.0)

        def _step_facts(self):
            if self.facts_shown >= len(self.facts):
                return
            self.fact_t -= 1
            if self.fact_t <= 0:
                self.fact_t = NF_FACT_EVERY
                self.facts_shown += 1
                self.play("tick", 0.45)

        # =====================================================================
        # DEPARTURE
        # =====================================================================

        def _begin_leave(self, won):
            self.mode = "leave_w" if won else "leave_l"
            self.mtick = 0
            self.pending_lines = []
            self.retract_warn = 0
            self.shake = 0.0
            self.attesting = False
            self.hud_fade = 1.0
            self.end_wipe = 0.0
            self.end_bar = 0.0
            self.leave_bars = 0.0
            inv_music_stop(3.0 if won else 1.8)
            # No sting either way. A victory chime would be the funniest thing
            # in the encounter.

        def _step_leave(self):
            """Neither ending is a spectacle.

            WON -- you are on record, and a thing that is on record cannot be
            taken back. So it stops. Every redaction on the page LIFTS, the
            sheet comes back whole, and then the bars go across IT instead: it
            files itself as unverifiable, in the same three passes it arrived
            in, and the hole takes what is left.

            LOST -- you are not killed. You are RETRACTED. The page keeps
            being struck out, cell by cell, in order, at the same unhurried
            rate it has used all along, until there is nothing left of it but
            ink -- and the last thing struck out is you. Then the sheet is
            blank, and nothing happens for a long time.
            """
            self.mtick += 1
            t = self.mtick
            won = (self.mode == "leave_w")

            if won:
                # THE PRESS TURNS ON THE THING THAT HAS BEEN OPERATING IT.
                #
                # Nonfiction does not die and it is not beaten off -- it is
                # PROCESSED, by exactly the apparatus it spent the whole
                # encounter pointing at you. Every beat below is a thing this
                # fight has already done TO the player, done back, at full
                # volume:
                #
                #   0-56     THE SHEET COMES BACK WHOLE. Every redaction on
                #            the page lifts at once and the room goes blank.
                #   56-206   THREE IMPRESSIONS, and the press slamming is the
                #            loudest thing in the encounter. Less of it is
                #            present after each one.
                #   206-268  ERRATUM. The entire page is struck out around it,
                #            in reading order, at the same unhurried rate it
                #            used on you -- and then lifted, leaving only it.
                #   268-338  IT IS REDACTED. The bars close over it until it is
                #            one solid rectangle, and then the rectangle is
                #            lifted too, and there is nothing underneath.
                #   338+     A blank sheet. Held.
                if t < 56:
                    for cell in list(self.struck.keys()):
                        data = self.struck[cell]
                        data["ink"] = max(0.0, data["ink"] - 0.055)
                        if data["ink"] <= 0.0:
                            self.struck.pop(cell, None)
                    self.hud_fade = max(0.0, 1.0 - t / 56.0)
                    if t == 54:
                        self._reprint(0.5)

                elif t < 206:
                    # Three impressions. Each one is a real slam rather than a
                    # registration tick: the room inverts, the sheet jumps, and
                    # more of it is gone when the platen comes back up.
                    if t in (58, 108, 158):
                        self._reprint(1.0)
                        self.play("slam", 0.95)
                        self.play("phase", 0.75)
                        self.flash = 0.85
                        self.shake = 1.0
                    step_i = 0 if t < 108 else (1 if t < 158 else 2)
                    since = t - (58, 108, 158)[step_i]
                    # It is taken in a HARD STEP on the impression and then
                    # eaten a little further while the platen is down, so the
                    # bars are not a smooth ramp -- a press is not smooth.
                    base = (0.34, 0.66, 0.92)[step_i]
                    self.leave_bars = base + 0.05 * inv_clamp(since / 44.0,
                                                            0.0, 1.0)
                    if since < 8:
                        self.press = max(self.press, 1.0 - since / 8.0)

                elif t < 268:
                    # ERRATUM, and it is administered to the page rather than
                    # to you for the first and only time.
                    u = (t - 206) / 62.0
                    if t == 206:
                        self.play("break", 0.9)
                        self.flash = 0.4
                        self._reprint(1.0)
                    target = int(u * NF_COLS * NF_ROWS)
                    idx = 0
                    for r in range(NF_ROWS):
                        for c in range(NF_COLS):
                            if idx >= target:
                                break
                            if (c, r) not in self.struck:
                                self.struck[(c, r)] = {"ink": 0.0, "dir": "h"}
                                if idx % 5 == 0:
                                    self.play("text", 0.5)
                            idx += 1
                        if idx >= target:
                            break
                    for data in self.struck.values():
                        data["ink"] = min(1.0, data["ink"] + NF_INK_RATE * 1.5)
                    self.leave_bars = 0.97

                elif t < 338:
                    u = inv_smooth((t - 268) / 70.0)
                    if t == 268:
                        self.play("cut_big", 0.95)
                        self._reprint(1.0)
                        self.flash = 0.5
                        self.shake = 0.8
                    # The page is lifted back off around it...
                    for cell in list(self.struck.keys()):
                        data = self.struck[cell]
                        data["ink"] = max(0.0, data["ink"] - 0.030)
                        if data["ink"] <= 0.0:
                            self.struck.pop(cell, None)
                    # ...leaving one solid rectangle where it was standing, and
                    # then that is lifted too.
                    self.leave_bars = inv_lerp(0.97, 1.0, u)
                    self.hole[0] = 640.0
                    self.hole[1] = 330.0
                    self.hole[3] = 1.0 - abs(u - 0.5) * 2.0
                    self.hole[2] = inv_lerp(50.0, 250.0, u)
                    if t == 330:
                        self.play("slam", 0.45)
                        self._reprint(0.8)

                else:
                    self.hole[3] = 0.0
                    self.struck = {}
                    if t > 380:
                        self.dark = inv_clamp(self.dark + 0.016, 0.0, 1.0)
                if t > 450:
                    self.result = "victory"

            else:
                # 0-30    everything stops
                # 30-210  the page is struck out cell by cell, in reading order
                # 210-260 the bar goes across you
                # 260+    a blank sheet, held far longer than is comfortable
                if t == 1:
                    self.play("cut", 0.6)
                if 30 <= t < 210:
                    u = (t - 30) / 180.0
                    target = int(u * NF_COLS * NF_ROWS)
                    idx = 0
                    for r in range(NF_ROWS):
                        for c in range(NF_COLS):
                            if idx >= target:
                                break
                            if (c, r) not in self.struck:
                                self.struck[(c, r)] = {"ink": 0.0, "dir": "h"}
                                if idx % 4 == 0:
                                    self.play("tick", 0.35)
                            idx += 1
                        if idx >= target:
                            break
                    for data in self.struck.values():
                        data["ink"] = min(1.0, data["ink"] + NF_INK_RATE)
                    self.hud_fade = max(0.0, 1.0 - u * 1.4)
                if 210 <= t < 262:
                    self.end_bar = inv_smooth((t - 210) / 52.0)
                    if t == 212:
                        self.play("cut_big", 0.85)
                if t == 262:
                    self._reprint(1.0)
                    self.play("slam", 0.5)
                if t >= 262:
                    self.end_wipe = inv_clamp((t - 262) / 40.0, 0.0, 1.0)
                if t >= 400:
                    self.dark = inv_clamp(self.dark + 0.012, 0.0, 1.0)
                if t > 470:
                    self.result = "defeat"


# --- THE STAGE ---------------------------------------------------------------
# Oct 2 2026: act one's figure is PRINTED ON A SHEET hanging in the dark --
# the printed thing made physical, swaying on its line in perspective under a
# cold light -- and at the tear the sheet swings at you as the room goes white
# and becomes the page. Act two stays flat and overhead (it invents no camera)
# but the page is paper now and the ink is wet. Drawn through the shared kit;
# the world goes through the lens, the HUD after it.
init python:
    from renpy.uguu import GL_REPEAT as _NF_GL_REPEAT

    NF_SHEET_W, NF_SHEET_H = 330, 470      # the sheet the figure is printed on
    NF_SHEET_TOP = 76.0                    # where its top edge hangs
    NF_SHEET_CANVAS = (980, 760)           # room for it to swing in

    class NFStage(renpy.Displayable):
        """One CDD. Steps NFGame at a fixed 60Hz inside render() and paints the
        whole encounter from cached-texture blits."""

        _tf_cache = {}

        PANEL_CMD = (40, 548, 470, 148)
        PANEL_HUD = (770, 548, 470, 148)

        # Index cards: ruled, pale-edged, no colour.
        STYLE_PANEL = {"top": "#0b0b0ce8", "bot": "#060607f0",
                       "edge": "#dcded6d0", "accent": "#dcded6ff",
                       "border": 1.2, "cut": 0.0, "inset": 7.0,
                       "inset_a": 0.10, "noise": 0.14, "scan": 0.0,
                       "split": 0.0, "ticks": 0.0}
        STYLE_PLATE = {"top": "#070708b0", "bot": "#070708d0",
                       "edge": "#dcded660", "accent": "#dcded6ff",
                       "border": 1.0, "cut": 0.0, "inset": 4.0,
                       "inset_a": 0.0, "noise": 0.10, "scan": 0.0,
                       "split": 0.0, "ticks": 0.0}
        STYLE_CARD = {"top": "#ece9e0f0", "bot": "#e4e1d6f4",
                      "edge": "#0d0d10c0", "accent": "#0d0d10ff",
                      "border": 1.0, "cut": 0.0, "inset": 5.0,
                      "inset_a": 0.10, "noise": 0.12, "scan": 0.0,
                      "split": 0.0, "ticks": 0.0}

        def __init__(self, game, **kwargs):
            super(NFStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0

        def _tf(self, key, builder):
            tf = NFStage._tf_cache.get(key)
            if tf is None:
                if len(NFStage._tf_cache) > 600:
                    NFStage._tf_cache.clear()
                tf = builder()
                NFStage._tf_cache[key] = tf
            return tf

        def _body_plain(self, zoom, alpha=1.0):
            ab = int(inv_clamp(alpha, 0.0, 1.0) * 6)
            key = ("plain", round(zoom, 3), ab)

            def build():
                kw = dict(zoom=zoom, subpixel=True)
                if ab < 6:
                    kw["alpha"] = ab / 6.0
                return Transform(NF_SPRITE, **kw)
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
                # A press does not rattle, it JUMPS: the shake is quantised to
                # whole registration steps.
                sx = int(round(math.sin(g.tick * 1.9) * amp / 3.0)) * 3
                sy = int(round(math.cos(g.tick * 2.7) * amp * 0.6 / 3.0)) * 3

            on_page = (g.open > 0.5)

            self._room(g, p)
            if on_page:
                self._page_world(g, p, sx, sy)
            else:
                self._room_world(g, p, sx, sy)
            inv_fx_paint(p, g.fx, "front", sx, sy)

            p.to_hud()
            if on_page:
                if g.hud_fade > 0.02:
                    self._page_hud(g, p, sx, sy)
            else:
                self._room_hud(g, p, sx, sy)
            self._floats(g, p, sx, sy)
            inv_fx_paint(p, g.fx, "hud")
            if g.paused:
                self._pause(g, p, on_page)

            rv = inv_compose(p, self._look(g, on_page), g.clock)

            # THE DRAW RATE IS THE TICK RATE (same governor as every stage).
            if g.result is None and not g.paused:
                renpy.redraw(self, max(0.0, INV_TICK - self.acc))
            return rv

        def _look(self, g, on_page):
            """A photographic negative in a dark room, then a white page. No
            colour either way -- the one red thing on the page is you."""
            shock = (0.0, 0.0, 0.0, 0.0)
            if g.shock[3] > 0.004:
                shock = (g.shock[0], g.shock[1], g.shock[2], g.shock[3])
            o = inv_clamp(g.open, 0.0, 1.0)
            return {
                "grade": (1.0, inv_lerp(1.10, 1.04, o), inv_lerp(0.20, 1.0, o), 0.0),
                "lift": (inv_lerp(0.012, 0.0, o),) * 3,
                "gain": (1.0, 1.0, 1.0),
                "bloom": inv_lerp(0.42, 0.10, o),
                "thresh": inv_lerp(0.55, 0.90, o),
                "ca": inv_lerp(0.0015, 0.0006, o) + g.ca,
                "grain": inv_lerp(0.050, 0.020, o),
                "vig": inv_lerp(0.62, 0.10, o),
                "vigr": 1.06,
                "barrel": inv_lerp(0.015, 0.0, o),
                "shock": shock,
                "tear": (inv_clamp(g.tear, 0.0, 1.0), float(g.tick // 4), 0.5, 0.6),
            }

        # ----- the room / the page --------------------------------------------------

        def _room(self, g, p):
            global NF_PLAIN_OK
            if NF_PLAIN_OK:
                try:
                    m = (Model((1280, 720))
                         .texture(inv_disp(NF_SOUP_IMG))
                         .texture(inv_disp(inv_fx_img("tex_paper")),
                                  texture_wrap=(_NF_GL_REPEAT, _NF_GL_REPEAT))
                         .shader("renpy.texture")
                         .shader("inv.plain")
                         .uniform("u_nf_res", (1280.0, 720.0))
                         .uniform("u_nf_time", g.clock)
                         .uniform("u_nf_open", g.open)
                         .uniform("u_nf_press", g.press)
                         .uniform("u_nf_reg", g.reg)
                         .uniform("u_nf_scrut", g.scrut_frac())
                         .uniform("u_nf_flash", g.flash)
                         .uniform("u_nf_dark", g.dark)
                         .uniform("u_nf_churn", g.churn())
                         .uniform("u_nf_hole", (float(g.hole[0]), float(g.hole[1]),
                                                float(g.hole[2]), float(g.hole[3])))
                         .uniform("u_nf_spot", (640.0, 300.0, 520.0,
                                                0.0 if g.mode == "arrive" else 1.0))
                         .uniform("u_nf_platen", float(inv_clamp(g.press * 1.2, 0.0, 1.0))))
                    r = renpy.render(m, 1280, 720, p.st, p.at)
                    p.blit(r, (0, 0))
                    return
                except Exception as e:
                    NF_PLAIN_OK = False
                    try:
                        renpy.log("INV FX: plain render failed: %r" % e)
                    except Exception:
                        pass
            p.fill(NF_PAPER if g.open > 0.5 else NF_BLACK, 0, 0, 1280, 720)

        # ----- the body --------------------------------------------------------

        def _strike_body(self, g, zoom, bars=0.0, ink=1.0, jump=1.0, paper=0.0):
            """The figure, put through the press (inv.strike), as a displayable
            plus its padded plate size."""
            plate_zoom = min(zoom, NF_PLATE_MAX_ZOOM)
            extra = zoom / plate_zoom
            plate, W, H = inv_body_plate(NF_SPRITE, NF_SPRITE_W, NF_SPRITE_H,
                                        plate_zoom, pad_x=1.55, pad_y=1.30)
            body = None
            if NF_STRIKE_OK:
                try:
                    body = Transform(
                        plate, mesh=True, shader="inv.strike",
                        u_st_res=(float(W), float(H)),
                        u_st_t=g.clock,
                        u_st_jump=float(jump),
                        u_st_reg=float(g.reg),
                        u_st_stretch=(1.0, 1.0),
                        u_st_pivot=0.90,
                        u_st_ink=float(ink),
                        u_st_paper=float(paper),
                        u_st_churn=float(g.churn()),
                        u_st_bars=float(bars))
                    if extra > 1.01:
                        body = Transform(body, zoom=extra, subpixel=True)
                except Exception:
                    body = None
            if body is None:
                body = self._body_plain(zoom)
            return body, int(W * extra), int(H * extra)

        def _draw_body(self, g, p, cx, cy, zoom, bars=0.0, ink=1.0, jump=1.0,
                       alpha=1.0, paper=0.0):
            body, w, h = self._strike_body(g, zoom, bars, ink, jump, paper)
            if alpha < 0.99:
                body = Transform(body, alpha=alpha)
            cx = cx + NF_FIG_DX * zoom
            cy = cy + NF_FIG_DY * zoom
            try:
                r = renpy.render(body, w + 8, h + 8, p.st, p.at)
                rw, rh = r.get_size()
                p.sblit(r, (cx - rw * 0.5, cy - rh * 0.5))
            except Exception:
                pass

        def _draw_heart(self, g, p, cx, cy, alpha=1.0):
            """You. The same SOUL heart as the other modes, and in the second
            half the only thing anywhere on the page that has a colour."""
            plate, W, H = inv_body_plate(INV_HEART, INV_HEART_W, INV_HEART_H,
                                        NF_HEART_ZOOM, pad_x=2.2, pad_y=2.2,
                                        nearest=True)
            squeeze = 1.0 - 0.20 * g.beat_pulse
            if INV_FLESH_OK:
                try:
                    d = inv_flesh(plate, W, H, g.clock * 2.6,
                                warp=NF_HEART_WARP, split=0.9,
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
                             lambda: Transform(INV_HEART, zoom=NF_HEART_ZOOM,
                                               nearest=True, subpixel=True))
            r, (w, h) = p.tex(("heartplain",), heart, 160, 160)
            p.sblit(r, (cx - w * 0.5, cy - h * 0.5))

        # ----- ACT ONE: the sheet ----------------------------------------------

        def _room_world(self, g, p, sx, sy):
            arriving = (g.mode == "arrive")
            scrut = g.scrut_frac()

            if arriving:
                # Printed into the room in three registration passes: it
                # appears where it is going to be, never walks there.
                bars = g.body_bars
                ink = g.body_ink
            else:
                bars = 0.10 * g.hit_flash
                ink = 1.0
            jump = 0.6 + 1.8 * g.press + 0.5 * scrut

            # The sheet's motion: its own sway, a tremor on its turn, a jolt
            # with the press -- and at the tear, the swing at you.
            yaw = g.sheet_yaw + 0.010 * math.sin(g.tick * 1.7) * g.windup
            pitch = 1.15 * g.sheet_fall + 0.04 * g.press
            top = NF_SHEET_TOP + sy + 3.0 * g.press + 40.0 * g.sheet_fall
            cxs = 640.0 + sx
            corners = inv_sheet_corners(NF_SHEET_W, NF_SHEET_H, cxs, top,
                                        yaw=yaw, pitch=pitch)

            # The line it hangs from, sagging a little between the clips.
            if g.sheet_fall < 0.98:
                la = 0.65 * (1.0 - g.sheet_fall)
                p.line(0.0, top - 4.0, corners[0][0], corners[0][1] - 1.0, width=0.8,
                       col="#8d918a", alpha=la, add=False)
                p.line(corners[0][0], corners[0][1] - 1.0, corners[1][0],
                       corners[1][1] - 1.0, width=0.8, col="#8d918a", alpha=la,
                       add=False)
                p.line(corners[1][0], corners[1][1] - 1.0, 1280.0, top - 4.0,
                       width=0.8, col="#8d918a", alpha=la, add=False)

            # Its shadow on the dark behind it, offset away from the light.
            xs = [c[0] for c in corners]
            ys = [c[1] for c in corners]
            shw = (max(xs) - min(xs)) * 0.62
            shh = (max(ys) - min(ys)) * 0.60
            p.glow((min(xs) + max(xs)) * 0.5 + 22.0, (min(ys) + max(ys)) * 0.5 + 26.0,
                   shw, shh, col="#000000", alpha=0.55 * (1.0 - g.sheet_fall),
                   add=False)

            # THE SHEET: stock, and the figure printed on it.
            cw, ch = NF_SHEET_CANVAS
            body, bw, bh = self._strike_body(g, NF_ZOOM_ACT1, bars=bars, ink=ink,
                                             jump=jump, paper=1.0)
            stock = self._tf(("stock",), lambda: Transform(
                inv_fx_img("tex_paper"), xysize=(NF_SHEET_W, NF_SHEET_H),
                matrixcolor=TintMatrix("#f3efe2")))
            fx_ = cw * 0.5 + NF_FIG_DX * NF_ZOOM_ACT1
            fy_ = ch * 0.5 + 14.0 + NF_FIG_DY * NF_ZOOM_ACT1
            content = Fixed(
                Transform(stock, xpos=(cw - NF_SHEET_W) // 2, ypos=(ch - NF_SHEET_H) // 2),
                Transform(body, xpos=int(fx_ - bw * 0.5), ypos=int(fy_ - bh * 0.5)),
                xysize=(cw, ch))
            facing = 0.86 + 0.14 * math.cos(yaw * 3.0) - 0.10 * g.sheet_fall
            ok = inv_draw_sheet(p, content, cw, ch, NF_SHEET_W, NF_SHEET_H, corners,
                                light=(facing, 0.22, 0.45, 1.0))
            if not ok:
                self._draw_body(g, p, 640 + sx, 300 + sy, NF_ZOOM_ACT1, bars=bars,
                                ink=ink, jump=jump)

            # The clips.
            if g.sheet_fall < 0.98:
                for c in (corners[0], corners[1]):
                    p.fill("#1a1b1e", c[0] - 5 + (12 if c is corners[0] else -12), c[1] - 9, 10, 18)

        def _room_hud(self, g, p, sx, sy):
            if g.mode == "arrive":
                return
            scrut = g.scrut_frac()
            inv_draw_panel(p, 370, 14, 540, 66, NFStage.STYLE_PLATE)
            p.text("NONFICTION", 15, NF_PALE, 386, 20, bold=True, w=320, h=30)

            # ITS ACCOUNT. One bar, two materials: solid for what you have
            # SOURCED, hatched for what you have merely stated.
            bar_w = 508
            p.fill("#1b1c1f", 386, 46, bar_w, 8)
            led = int(bar_w * inv_clamp(g.ledger_shown / float(NF_STANDING_MAX), 0.0, 1.0))
            pend = int(bar_w * inv_clamp(g.pending_shown / float(NF_STANDING_MAX), 0.0, 1.0))
            if led > 0:
                p.fill(NF_PALE, 386, 46, led, 8)
            if pend > 0:
                x = 386 + led
                for k in range(0, pend, 6):
                    p.fill(inv_hex(NF_PALE, 0.40), x + k, 46, min(3, pend - k), 8)
            mark = 386 + int(bar_w * NF_SHIFT_LEDGER / float(NF_STANDING_MAX))
            p.fill(inv_hex(NF_PALE, 0.55), mark, 43, 1, 14)
            p.fill("#1b1c1f", 386, 60, bar_w, 4)
            sc = int(bar_w * scrut)
            if sc > 0:
                p.fill(NF_WARN if scrut < 0.85 else NF_RED, 386, 60, sc, 4)
            p.text("SCRUTINY", 10, NF_DIM, 386, 66, w=200, h=20)

            inv_draw_log(p, g, 930, 20, 310,
                         {"you": (NF_PALE, NF_WARN), "it": (NF_DIM, NF_RED)})

            slide = int(g.panel_slide * 200)
            if g.panel_slide < 1.0:
                kick = g.panel_kick
                kx = int(round(math.sin(g.tick * 2.3) * 8.0 * max(0.0, kick) / 3.0)) * 3
                ky = int(abs(kick) * 4.0)
                self._panel(g, p, NFStage.PANEL_CMD, sx, sy + slide)
                self._panel(g, p, NFStage.PANEL_HUD, sx + kx, sy + slide + ky, hit=kick)
                self._panel_contents(g, p, sx, sy + slide, kx, ky)

        def _panel(self, g, p, box, sx, sy, hit=0.0):
            x, y, w, h = box
            inv_draw_panel(p, x + sx, y + sy, w, h, NFStage.STYLE_PANEL)
            # A ruled page, not a game window.
            for k in range(1, 5):
                p.fill("#dcded616", x + sx + 12, y + sy + 12 + k * 30, w - 24, 1)
            if hit > 0.05:
                p.fill(inv_hex("#dcded6", 0.10 * hit), x + sx, y + sy, w, h)

        def _panel_contents(self, g, p, sx, sy, kx=0, ky=0):
            cx, cy, cw, ch = NFStage.PANEL_CMD
            cx += sx
            cy += sy

            if g.mode == "menu":
                for i, row in enumerate(NF_CMDS):
                    live = (i == g.cursor)
                    ry = cy + 18 + i * 30
                    if live:
                        p.fill(NF_PALE + "18", cx + 14, ry - 4, cw - 28, 27)
                        p.fill(NF_PALE, cx + 14, ry - 4, 3, 27)
                        p.fill(NF_PALE, cx + 26, ry + 5, 8, 8)
                    p.text(row[1], 20, NF_PALE if live else NF_FAINT,
                           cx + 46, ry, bold=live, w=260, h=30)
                    if row[0] == "cite":
                        p.text(str(NF_CITE_COST), 14, NF_PALE if live else NF_FAINT,
                               cx + cw - 22, ry + 4, anchor=(1.0, 0.0), w=120, h=26)
                p.text("Z  OK      ESC  PAUSE", 12, NF_FAINT,
                       cx + cw - 16, cy + ch - 22, anchor=(1.0, 0.0), w=420, h=24)

            elif g.mode == "beat":
                u = inv_clamp(g.mtick / 6.0, 0.0, 1.0)
                p.text(g.beat_label, 22, NF_PALE, cx + 22, cy + 28, bold=True,
                       w=cw - 40, h=40)
                if g.beat_value:
                    p.text(g.beat_value, int(22 + 4 * u), NF_WARN, cx + 22, cy + 62,
                           bold=True, w=cw - 40, h=44)
                hold = inv_clamp(g.mtick / float(INV_BEAT_HOLD), 0.0, 1.0)
                p.fill(NF_FAINT + "60", cx + 22, cy + ch - 18, cw - 44, 2)
                p.fill(NF_PALE, cx + 22, cy + ch - 18, int((cw - 44) * hold), 2)

            elif g.mode == "enemy":
                u = inv_clamp(g.mtick / 26.0, 0.0, 1.0)
                p.text("NONFICTION", 18, NF_DIM, cx + 22, cy + 30, bold=True,
                       w=cw - 40, h=34)
                p.fill(NF_DIM + "50", cx + 22, cy + 70, cw - 44, 2)
                p.fill(NF_PALE, cx + 22, cy + 70, int((cw - 44) * u), 2)

            hx, hy, hw, hh = NFStage.PANEL_HUD
            hx += sx + kx
            hy += sy + ky
            p.text(inv_player_name(), 19, NF_PALE, hx + 22, hy + 12,
                   bold=True, w=hw - 40, h=32)
            self._odometer(g, p, "HP", g.hp_shown, g.hp, hx + 22, hy + 44, NF_PALE)
            self._odometer(g, p, "SRC", g.src_shown, g.src, hx + 22, hy + 96, NF_DIM,
                           small=True)
            if g.pending > 0:
                p.text("UNSOURCED  %d" % g.pending, 13,
                       NF_WARN if not g.marked else NF_RED,
                       hx + hw - 22, hy + 16, anchor=(1.0, 0.0), w=260, h=26)
            if g.marked:
                p.text("MARKED", 13, NF_RED, hx + hw - 22, hy + 40,
                       anchor=(1.0, 0.0), w=200, h=26, bold=True)
            if g.god:
                p.text("GOD", 12, NF_WARN + "aa", hx + hw - 22,
                       hy + hh - 24, anchor=(1.0, 0.0), w=120, h=24)

        def _odometer(self, g, p, label, shown, real, x, y, color, small=False,
                      invert=False):
            """An EarthBound counter: fixed-width cells, and the digits that
            are moving are drawn mid-roll rather than swapped."""
            size = 22 if small else 30
            cell_w = 22 if small else 28
            cell_h = 32 if small else 42
            cell_col = "#dcded655" if invert else "#0a0a0ce0"
            p.text(label, 14, color, x, y + (6 if small else 12), bold=True,
                   w=60, h=28)
            value = int(math.ceil(shown - 0.0001)) if shown > 0 else 0
            rolling = abs(shown - real) > 0.05
            digits = "%03d" % inv_clamp(value, 0, 999)
            frac = shown - math.floor(shown)
            base_x = x + 44
            for i, ch in enumerate(digits):
                dx = base_x + i * cell_w
                p.fill(cell_col, dx, y, cell_w - 4, cell_h)
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

        # ----- ACT TWO: THE PAGE -----------------------------------------------

        def _page_world(self, g, p, sx, sy):
            leaving = g.mode in ("leave_w", "leave_l")
            churn = g.churn()

            # --- the watermark: IN the paper, large and faint, re-registering
            # only on its own passes -- never on the beat (user, Aug 14 2026).
            self._draw_body(g, p, 640 + sx, 380 + sy, NF_ZOOM_MARK,
                            bars=(g.leave_bars if g.mode == "leave_w" else 0.0),
                            ink=1.0, jump=0.5 + 2.2 * g.press,
                            alpha=NF_MARK_ALPHA * (1.0 + 1.6 * g.press), paper=1.0)

            # --- the grid: ruled, like ledger stock ------------------------------
            px0, py0 = NF_PLANE_X + sx, NF_PLANE_Y + sy
            rc = NF_RULE_COL
            p.fill(inv_hex(rc, 0.60), px0 - 2, py0 - 2, NF_PLANE_W + 4, 2)
            p.fill(inv_hex(rc, 0.60), px0 - 2, py0 + NF_PLANE_H, NF_PLANE_W + 4, 2)
            p.fill(inv_hex(rc, 0.60), px0 - 2, py0 - 2, 2, NF_PLANE_H + 4)
            p.fill(inv_hex(rc, 0.60), px0 + NF_PLANE_W, py0 - 2, 2, NF_PLANE_H + 4)
            for c in range(1, NF_COLS):
                p.fill(inv_hex(rc, 0.30), px0 + c * NF_CELL_W, py0, 1, NF_PLANE_H)
            for r in range(1, NF_ROWS):
                p.fill(inv_hex(rc, 0.30), px0, py0 + r * NF_CELL_H, NF_PLANE_W, 1)
            # A page under a press has a shadow round its edge.
            p.glow(640 + sx, py0 + NF_PLANE_H + 10, NF_PLANE_W * 0.55, 16.0,
                   col="#000000", alpha=0.10, add=False)

            # --- THE MARGIN --------------------------------------------------------
            mgx = px0 + (NF_MARGIN_COL + 1) * NF_CELL_W
            p.fill(inv_hex(rc, 0.75), mgx - 4, py0, 2, NF_PLANE_H)
            p.fill(inv_hex(rc, 0.75), mgx, py0, 2, NF_PLANE_H)
            carrying = g.pend2 >= NF_BANK_MIN and not leaving
            if not leaving:
                p.text("CITE", 13, inv_hex(NF_INK, 0.85 if carrying else 0.30),
                       NF_PLANE_X + NF_CELL_W // 2 + sx, 148 + sy, bold=carrying,
                       anchor=(0.5, 0.5), w=200, h=28)
            for r in range(NF_ROWS):
                bx, by, bw, bh = nf_cell_box(NF_MARGIN_COL, r)
                bx += sx
                by += sy
                if carrying and g.margin_open(r):
                    p.fill(inv_hex(NF_INK, 0.07 + 0.05 * g.pend_frac()),
                           bx + 4, by + 4, bw - 8, bh - 8)
                if not g.margin_open(r):
                    # A citation, filed and still wet: a reference mark and
                    # two short rules -- the shape of an entry, not an entry.
                    dry = 1.0 - g.margin_cd.get(r, 0) / float(NF_MARGIN_REOPEN)
                    a = 0.22 + 0.50 * dry
                    p.fill(inv_hex(NF_INK, a), bx + 16, by + bh * 0.36, bw * 0.44, 3)
                    p.fill(inv_hex(NF_INK, a * 0.75), bx + 16, by + bh * 0.36 + 12,
                           bw * 0.30, 3)
                    p.fill(inv_hex(NF_INK, a), bx + 8, by + bh * 0.36 - 4, 4, 22)
                    p.text("%d" % (r + 1), 11, inv_hex(NF_INK, a), bx + bw - 14,
                           by + 8, anchor=(1.0, 0.0), w=40, h=20)
                elif carrying:
                    puls = 0.5 + 0.5 * math.sin(g.tick * 0.11 + r * 0.9)
                    a = 0.16 + 0.30 * puls * g.pend_frac()
                    p.fill(inv_hex(NF_INK, a), bx + 16, by + bh * 0.36, bw * 0.44, 2)
                    p.fill(inv_hex(NF_INK, a), bx + 16, by + bh * 0.36 + 14, bw * 0.44, 2)

            # --- printer's correction marks accumulating in the open cells ------
            if churn > 0.04 and not leaving:
                n_marks = int(2 + 20 * churn)
                for k in range(n_marks):
                    seed = ((k * 2654435761) % 1013) / 1013.0
                    c = int(seed * (NF_COLS - 1)) + 1
                    r = int((((k * 40503) % 977) / 977.0) * NF_ROWS)
                    if (c, r) in g.struck or (c, r) == g.anchor:
                        continue
                    bx, by, bw, bh = nf_cell_box(c, r)
                    ox = int(bx + 14 + seed * (bw - 40)) + sx
                    oy = int(by + 12 + ((k * 7919) % 100) / 100.0 * (bh - 34)) + sy
                    a = 0.10 + 0.26 * churn
                    kind = k % 3
                    if kind == 0:
                        for i in range(6):
                            p.fill(inv_hex(NF_INK, a), ox + i * 2, oy + 10 - abs(i - 2) * 3, 2, 2)
                            p.fill(inv_hex(NF_INK, a), ox + 10 - i * 2, oy + 10 - abs(i - 2) * 3, 2, 2)
                    elif kind == 1:
                        p.ring(ox + 6, oy + 4, 7.0, 5.0, col=NF_INK, alpha=a,
                               add=False, tex="ring")
                    else:
                        p.fill(inv_hex(NF_INK, a), ox, oy, 14, 2)
                        p.fill(inv_hex(NF_INK, a), ox + 12, oy, 2, 8)
                        p.fill(inv_hex(NF_INK, a), ox + 2, oy + 8, 10, 2)

            # --- what has been struck out: WET INK --------------------------------
            # A redaction sweeps in from one edge like a marker and OVERSHOOTS
            # its cell. It is ink, so it has a sheen along the stroke and a
            # bead at its leading edge while it is still being laid down.
            for (c, r), data in g.struck.items():
                bx, by, bw, bh = nf_cell_box(c, r)
                bx += sx
                by += sy
                ink = data["ink"]
                if data["dir"] == "v":
                    h = max(2, int(bh * ink))
                    p.fill("#050506", bx - 2, by - 1, bw + 4, h + 3)
                    p.fill("#2a2a31", bx + bw * 0.30, by, 2, h)
                    if ink < 0.999:
                        p.quad(INV_INKS[(c + r) % 4], bx + bw * 0.5, by + h,
                               0.30, col="#050506", alpha=0.9, add=False)
                else:
                    w = max(2, int(bw * ink))
                    p.fill("#050506", bx - 1, by - 2, w + 3, bh + 4)
                    p.fill("#2a2a31", bx, by + bh * 0.30, w, 2)
                    if ink < 0.999:
                        p.quad(INV_INKS[(c + r) % 4], bx + w, by + bh * 0.5,
                               0.30, col="#050506", alpha=0.9, add=False)

            # --- what is about to be: blue-pencil strokes (in grey) --------------
            if g.pending_lines and g.volley_warn > 0:
                u = 1.0 - g.volley_warn / float(NF_VOLLEY_WARN)
                puls = 0.5 + 0.5 * math.sin(g.tick * 0.42)
                for line in g.pending_lines:
                    for (c, r) in line["cells"]:
                        bx, by, bw, bh = nf_cell_box(c, r)
                        bx += sx
                        by += sy
                        a = 0.30 + 0.45 * u * puls
                        t_ = 1.0 + 3.0 * u
                        if line["dir"] == "v":
                            p.line(bx + bw * 0.5, by + 4, bx + bw * 0.5 + 2, by + bh - 4,
                                   width=t_, col="#26262c", alpha=a, add=False)
                        else:
                            p.line(bx + 4, by + bh * 0.5, bx + bw - 4, by + bh * 0.5 - 2,
                                   width=t_, col="#26262c", alpha=a, add=False)

            # --- the anchor: a corroborated fact, stamped -------------------------
            if g.anchor is not None and not leaving:
                bx, by, bw, bh = nf_cell_box(*g.anchor)
                bx += sx
                by += sy
                expiring = g.anchor_life < 90 and (g.tick // 6) % 2 == 0
                acol = inv_hex(NF_INK, 0.20 if expiring else 0.62)
                p.fill(inv_hex(NF_INK, 0.10), bx + 3, by + 3, bw - 6, bh - 6)
                for inset in (4, 9):
                    p.fill(acol, bx + inset, by + inset, bw - inset * 2, 2)
                    p.fill(acol, bx + inset, by + bh - inset - 2, bw - inset * 2, 2)
                    p.fill(acol, bx + inset, by + inset, 2, bh - inset * 2)
                    p.fill(acol, bx + bw - inset - 2, by + inset, 2, bh - inset * 2)
                if g.retract_warn > 0:
                    puls = 0.5 + 0.5 * math.sin(g.tick * 0.55)
                    p.fill(inv_hex(NF_INK, 0.25 + 0.50 * puls), bx + 8, by + bh * 0.5 - 4,
                           bw - 16, max(3, int(10 * puls)))

            # --- WHERE TO GO: a dashed leader line ---------------------------------
            target = None
            if not leaving:
                if carrying:
                    rows = [r for r in range(NF_ROWS) if g.margin_open(r)]
                    if rows and g.cell_of(g.px, g.py)[0] != NF_MARGIN_COL:
                        best_r = min(rows, key=lambda r: abs(
                            nf_cell_center(NF_MARGIN_COL, r)[1] - g.py))
                        target = nf_cell_center(NF_MARGIN_COL, best_r)
                elif g.anchor is not None and g.cell_of(g.px, g.py) != g.anchor:
                    target = nf_cell_center(*g.anchor)
            if target is not None:
                vx = target[0] - g.px
                vy = target[1] - g.py
                dist = math.hypot(vx, vy)
                if dist > 46.0:
                    ux = vx / dist
                    uy = vy / dist
                    k = 34.0
                    while k < dist - 30.0:
                        a = 0.34 * (1.0 - k / max(dist, 1.0)) + 0.12
                        p.fill(inv_hex(NF_INK, a), g.px + ux * k + sx, g.py + uy * k + sy, 5, 5)
                        k += 15.0

            # --- you ----------------------------------------------------------------
            if not (g.mode == "leave_l" and g.mtick > 262):
                # Your trail is the only colour on the page: red ink.
                for i, (tx, ty) in enumerate(g.trail):
                    if i == 0:
                        continue
                    a = 0.30 * (1.0 - i / float(len(g.trail)))
                    p.quad("dust", tx + sx, ty + sy, 0.9 - i * 0.07, col=NF_RED,
                           alpha=a, add=False)
                blink = (g.iframes > 0 and (g.tick // 3) % 2 == 0)
                if not blink:
                    p.shadow(g.px + sx + 3, g.py + sy + 14, 14.0, 5.0, alpha=0.25)
                    self._draw_heart(g, p, g.px + sx, g.py + sy)

                # WHAT YOU ARE CARRYING, drawn ON you: an arc closing round the
                # heart as the escrow fills, whole and pulsing once full.
                if not leaving and g.pend2 > 0.0:
                    pf = g.pend_frac()
                    full = pf >= 0.999
                    segs = 20
                    lit = int(round(segs * pf))
                    puls = 0.5 + 0.5 * math.sin(g.tick * 0.16)
                    a = 0.55 + (0.35 * puls if full else 0.0)
                    for k in range(lit):
                        ang = -1.5708 + (k / float(segs)) * 6.2831853
                        p.fill(inv_hex(NF_INK, a), g.px + math.cos(ang) * 25.0 + sx - 2,
                               g.py + math.sin(ang) * 25.0 + sy - 2, 4, 4)

                # ON RECORD: the ring only closes when you stop.
                if g.anchor is not None and not leaving:
                    if g.cell_of(g.px, g.py) == g.anchor:
                        filling = g.attesting or g.still > 4
                        segs = 24
                        size = 5 if filling else 3
                        for k in range(segs):
                            if not filling and k % 2:
                                continue
                            ang = -1.5708 + (k / float(segs)) * 6.2831853
                            p.fill(inv_hex(NF_INK, 0.90 if filling else 0.26),
                                   g.px + math.cos(ang) * 36.0 + sx - size // 2,
                                   g.py + math.sin(ang) * 36.0 + sy - size // 2, size, size)
                        if g.attesting:
                            for k in range(segs):
                                ang = -1.5708 + ((k + 0.5) / segs) * 6.2831853
                                p.fill(inv_hex(NF_INK, 0.55),
                                       g.px + math.cos(ang) * 46.0 + sx - 1,
                                       g.py + math.sin(ang) * 46.0 + sy - 1, 3, 3)

            # THE LAST THING STRUCK OUT IS YOU.
            if g.end_bar > 0.0:
                w = int(240 * g.end_bar)
                p.fill("#000000", g.px - 120 + sx, g.py - 13 + sy, w, 26)
            if g.end_wipe > 0.0:
                p.fill(inv_hex("#000000", g.end_wipe), 0, 0, 1280, 720)

        def _page_hud(self, g, p, sx, sy):
            # --- VERIFIED, AND WHAT IS NOT VERIFIED YET ----------------------------
            bw = NF_PLANE_W
            bx = NF_PLANE_X
            p.fill(inv_hex(NF_INK, 0.55), bx - 2, 96, bw + 4, 20)
            p.fill(NF_PAPER, bx, 98, bw, 16)
            fill = int(bw * inv_clamp(g.verify_shown / NF_VERIFY_MAX, 0.0, 1.0))
            if fill > 0:
                p.fill(NF_INK, bx, 98, fill, 16)
                p.fill("#2a2a31", bx, 101, fill, 2)
            pend_w = int(bw * inv_clamp(g.pend2_shown / NF_VERIFY_MAX, 0.0, 1.0))
            if pend_w > 0:
                x_p = bx + fill
                for k in range(0, min(pend_w, bw - fill), 6):
                    p.fill(inv_hex(NF_INK, 0.75), x_p + k, 98, 3, 16)
                p.fill(inv_hex(NF_INK, 0.85), min(x_p + pend_w, bx + bw - 2), 95, 2, 22)
            if g.bank_flash > 0.02:
                p.fill(inv_hex(NF_INK, 0.55 * g.bank_flash), bx - 4, 93, bw + 8, 26)
            p.text("VERIFIED", 13, NF_INK, bx, 74, bold=True, w=200, h=26)
            p.text("%d" % int(g.verify), 15, NF_INK, bx + bw, 74, bold=True,
                   anchor=(1.0, 0.0), w=140, h=26)
            if g.pend2 >= 1.0:
                p.text("UNSOURCED", 11,
                       inv_hex(NF_INK, 0.55 if g.pend_frac() < 0.999 else 0.95),
                       min(bx + fill + 6, bx + bw - 90), 118, w=200, h=22)
                p.text("%d" % int(g.pend2), 13,
                       inv_hex(NF_INK, 0.62 if g.pend_frac() < 0.999 else 0.95),
                       bx + bw, 118, anchor=(1.0, 0.0), w=120, h=22)

            # --- HP and CREDIT -------------------------------------------------------
            inv_draw_panel(p, 30, 598, 300, 106, NFStage.STYLE_CARD)
            self._odometer(g, p, "HP", g.hp_shown, g.hp, 44, 646, NF_INK, invert=True)
            cw = 220
            p.fill(inv_hex(NF_INK, 0.45), 42, 622, cw + 4, 12)
            p.fill(NF_PAPER, 44, 624, cw, 8)
            ccol = NF_INK if g.credit >= NF_ATTEST_MIN else NF_RED
            cf = int(cw * inv_clamp(g.credit / NF_CREDIT_MAX, 0.0, 1.0))
            if cf > 0:
                p.fill(ccol, 44, 624, cf, 8)
            p.fill(inv_hex(NF_INK, 0.55), 44 + int(cw * (NF_ATTEST_MIN / NF_CREDIT_MAX)), 621, 2, 14)
            p.text("CREDIT", 11, NF_FAINT, 44, 606, w=160, h=22)
            if g.attesting:
                p.text("ATTEST", 13, NF_INK, 44 + cw + 12, 620, bold=True, w=180, h=26)

            # --- THE READOUT: the margin stops reporting the person played ---------
            for i in range(min(g.facts_shown, len(g.facts))):
                key, value = g.facts[i]
                ry = 176 + i * 26
                a = 0.75
                if i == g.facts_shown - 1 and g.fact_t > NF_FACT_EVERY - 20:
                    a = 0.75 * ((NF_FACT_EVERY - g.fact_t) / 20.0)
                p.text(key, 11, inv_hex(NF_FAINT, a), 1092, ry, w=170, h=22)
                p.text(value, 13, inv_hex(NF_INK, a), 1256, ry - 2,
                       anchor=(1.0, 0.0), w=190, h=24)

            p.text("MOVE  WASD      Z  ATTEST  (HOLD)", 12, NF_FAINT,
                   1256, 690, anchor=(1.0, 1.0), w=760, h=28)
            if g.god:
                p.text("GOD", 12, NF_RED, 1256, 664, anchor=(1.0, 1.0), w=120, h=24)

        # ----- numbers and pause -----------------------------------------------

        def _floats(self, g, p, sx, sy):
            on_page = g.open > 0.5
            for f in g.floats:
                a = inv_clamp(f["life"] / 26.0, 0.0, 1.0)
                age = 52 - f["life"]
                pop = 1.0 + 0.30 * inv_clamp(1.0 - age / 6.0, 0.0, 1.0)
                p.text(f["text"], int((28 if f["big"] else 20) * pop),
                       inv_hex(f["color"], a), int(f["x"]) + sx, int(f["y"]) + sy,
                       bold=f["big"], anchor=(0.5, 0.5), w=340, h=70,
                       outline=(None if on_page else "#050506"))

        def _pause(self, g, p, on_page):
            p.fill("#050506c8" if not on_page else "#e8e6dec8", 0, 0, 1280, 720)
            inv_draw_panel(p, 440, 270, 400, 150,
                           NFStage.STYLE_CARD if on_page else NFStage.STYLE_PANEL)
            pcol = NF_PALE if not on_page else NF_INK
            p.text("PAUSED", 40, pcol, 640, 322, bold=True, anchor=(0.5, 0.5), w=600, h=70)
            p.text("ESC  RESUME        Q  QUIT", 16, NF_DIM if not on_page else NF_FAINT,
                   640, 378, anchor=(0.5, 0.5), w=800, h=44)
# --- THE SCREEN --------------------------------------------------------------
screen inv_nonfiction_screen(game):
    modal True
    use enter_m_input_lock()

    add Solid("#050506")
    add NFStage(game)

    key "K_ESCAPE" action Function(game.toggle_pause)
    key "mouseup_3" action Function(game.toggle_pause)
    if game.paused:
        key "K_q" action Function(game.give_up)

    if config.developer:
        key "K_g" action Function(game.toggle_god)

    timer 0.25 repeat True action Function(inv_poll_result, game, _update_screens=False)


# --- WRAPPER -----------------------------------------------------------------
default nf_game = None
default nf_deaths = 0
default nf_retry = False
# A RETRY FROM THE TEAR, carrying the ledger act one sourced.
default nf_resume = None

label archivist_invasion_nonfiction:
    $ nf_deaths = 0
    $ nf_retry = False
    $ nf_resume = None

label inv_nonfiction_fight:
    $ renpy.block_rollback()

    $ nf_game = NFGame(retry=nf_retry, deaths=nf_deaths,
                    debug=config.developer, start_open=inv_dev_start_open,
                    resume=nf_resume)
    $ nf_resume = None

    $ _nf_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ _nf_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None
    scene black

    call screen inv_nonfiction_screen(nf_game)
    $ _nf_result = _return
    $ _nf_checkpoint = nf_game.checkpoint

    $ nf_game = None
    $ quick_menu = _nf_prev_quick_menu
    $ _game_menu_screen = _nf_prev_game_menu
    $ inv_music_stop(1.0)
    $ inv_heart_stop(0.6)
    $ inv_stop_sfx(0.2)
    scene black

    if _nf_result == "victory":
        $ inv_record_result("nonfiction", True)
        jump inv_nonfiction_victory
    elif _nf_result == "quit":
        jump inv_nonfiction_quit

    $ inv_record_result("nonfiction", False)
    jump inv_nonfiction_defeat

label inv_nonfiction_victory:
    if inv_dev_test:
        $ renpy.notify("NONFICTION: on record.")
        return
    # STORY PLACEMENT: DRAWING BOARD.
    return

label inv_nonfiction_defeat:
    $ nf_deaths += 1
    $ nf_retry = True

    call screen inv_retry_screen("NONFICTION", "RETRACTED",
                                 inv_retry_options(_nf_checkpoint),
                                 ink=NF_PALE, dim=NF_DIM, accent=NF_RED,
                                 bg=NF_BLACK)
    if _return == "tear":
        $ nf_resume = _nf_checkpoint
        scene black
        jump inv_nonfiction_fight
    elif _return == "start":
        scene black
        jump inv_nonfiction_fight
    if inv_dev_test:
        $ renpy.notify("NONFICTION: retracted. Recorded.")
    return

label inv_nonfiction_quit:
    $ nf_retry = True
    if inv_dev_test:
        $ renpy.notify("NONFICTION: withdrawn.")
    return
