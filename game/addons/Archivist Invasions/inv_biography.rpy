# =============================================================================
# ARCHIVIST INVASION 01 -- BIOGRAPHY
# =============================================================================
#
# WHAT THIS IS
#   The first Archivist Invasion, playable end to end. An interruption fought
#   in the soup: a hyperspace that has not finished deciding what matter is.
#   Two acts, no warning, no explanation.
#
#   ACT ONE -- windows. A turn-based bout in EarthBound's furniture: hard
#   bordered panels, ONE nondescript party member, a set kit. HP does not drop
#   when you are hit -- it starts ROLLING toward the new number, and you are
#   only dead when the counter arrives.
#
#   ACT TWO -- the CORRUPTIVE STATE. Past a damage threshold the panels are
#   torn off the screen and it fights in its own genre: open combat on a
#   stage, shot through a camera that will not hold still, you dodging with a
#   held dash and answering with four thrown daggers and no fifth one.
#
# HOW ACT TWO WORKS, IN FOUR SENTENCES
#   There are FOUR daggers. Throwing one spends it, a thrown one sheds speed
#   the whole way (so what it does on arrival is a function of how close you
#   were standing), and one that lands is lying on the boards until you walk
#   over it -- which means the ammunition is always somewhere near the thing
#   swinging at you. Daggers do not take health while it is composed, they
#   take POISE, and double that while it is committed to a move; run poise out
#   and it BUCKLES, and that window is the only time damage is real. Meanwhile
#   the ENTRY bar fills on its own and fills faster the further away you keep
#   yourself, because it is not trying to kill you, it is trying to finish
#   writing you down, and it can do that from anywhere you are not.
#
#   THE PROBLEM THIS SHAPE EXISTS TO SOLVE (2026-08-11). The first version was
#   a homing dagger on a 16-tick cooldown against an Archivist that was
#   OVER-EXTENDED for 31% of every cycle for free -- its whole throw plus all
#   six recovery windows. Nothing about it read distance, aim or timing, so
#   the entire fight was one button held from the back of the stage, and it
#   was over in under twenty seconds. Every number below is chosen against
#   that: measured on eight seeded bot runs, a bot doing exactly that now
#   deals 20 damage out of 520 and dies, and a bot actually playing the loop
#   wins eight times in eight at 26-48 seconds with 54-95% of its health left.
#
#   THE DIFFICULTY IS DELIBERATELY SET SOFT. Two rounds of playtesting said
#   this fight was punishing before it was fun, and the harness bot is a
#   MEDIOCRE pilot (crude threat model, dashes away rather than through), so
#   tuning until it struggles tunes past a real player. If it wants to bite
#   harder the knobs, in order: BIO_DMG_* (magnitude), BIO_MOVE_HIT_CAP
#   (burst), BIO_DAGGER_HEAL (sustain), _open_idle_len (frequency).
#
#   RUNTIME IS DELIBERATELY THE SHORTEST OF THE THREE. Horror's chase is
#   75-90s and Nonfiction's page is roughly 40-60s; this is 33-53s, because
#   Biography is the densest of them -- it is the only one asking you to
#   manage ammunition, break composure, dodge, AND stay close all at once.
#   Density times duration is what should match across the set, not duration.
#
#   AND THE FELT LENGTH IS THE NUMBER OF REPETITIONS, NOT THE CLOCK. The
#   first tuning of this rebuild ran 39-68s and read as far longer than it
#   was, because breaking poise once took fourteen daggers and three separate
#   retrieval trips. It is eight or nine daggers and two trips now, for the
#   same wall time -- see BIO_POISE_REGEN_IDLE, which was most of it.
#
#   DISCHARGE (2026-08-12). The hyperspace only ever said "matter has not been
#   decided" in its shaders; now it says it out loud. Cosmetic lightning from
#   the shared atlas (asset_definitions/def_bullets.rpy, EMB_ARCS) crackles ambiently
#   through act two -- rarely, and harder the further along the fight is --
#   and BURSTS across the Archivist on a buckle, which is the one moment it is
#   not composed. It has no mechanics and cannot touch the player. In the same
#   pass the sweeping "bar" hazard stopped being a flat canvas line and became
#   a real beam (the `lens` art), drawn between the same projected endpoints
#   and through the floor_layer so it still passes UNDER anyone standing on it.
#
# THE FIVE RULES THIS FILE IS WRITTEN AGAINST (set 2026-08-09, read before editing)
#
#   1. NO FLAVOR TEXT. Not one line of narration, not one spoken word, not one
#      quip. Everything on screen is either a control, a number, or a state
#      word. The horror is supposed to arrive through the thing happening to
#      the player, not through a caption telling them it is happening. An
#      invasion should leave someone asking what that WAS -- a narrator
#      answers the question before they can ask it.
#
#   2. NOTHING IS ALLOWED TO BE FUNNY. Every element gets checked against
#      this. A PNG sliding across a backdrop is funny. A caption that
#      editorialises is funny. Big cheerful labels crowding the sprite are
#      funny. Oppressive means the screen is busy, close, and never quite
#      still, and the Archivist is never legible as a costume.
#
#   3. IT MOVES LIKE SOMETHING THAT HAS SEEN A DIAGRAM OF A PERSON. Biography
#      is never a static image being translated. The body contorts, stretches
#      and slips out of sync with itself (shader inv.flesh: independent
#      horizontal bands, so limbs lengthen and lag separately), it banks into
#      its own momentum, it rotates BODILY through its swings, and it smears
#      into afterimages when it moves fast.
#
#   4. IT ARRIVES AND LEAVES THROUGH A HOLE. Never a fade, never a walk-on.
#      The soup ruptures at a point, spirals into a wormhole, and it is
#      extruded out of it -- and at the end it is dragged back in and the hole
#      shuts. That rupture is the whole of the "what was that" feeling.
#
#   5. EVERY PATTERN MUST BE BEATABLE HITLESS. Shockwaves and sweeping lines
#      have no authored gap to stand in (the project rule), so the dash IS the
#      answer -- which means no two dash-answerable hazards may ever land
#      closer together than the dash cooldown. If you retune a spacing, check
#      it against BIO_DASH_CD, and check it in the HARNESS rather than by
#      eye: shortening throw's copies to 36 ticks against a 46-tick cooldown
#      looked completely fine while playing and was caught in one audit run.
#      Currently measured -- 54 ticks between rings/bars, 48 between anything.
#
# THE SIXTH RULE, ADDED 2026-08-11
#   6. THE ROOM MAY BE HARD TO LOOK AT, BUT IT MAY NEVER BE INCOHERENT.
#      Oppressive is not the same as noisy, and nausea made of random numbers
#      reads as a broken renderer rather than as a place. So every unsettling
#      thing on screen is a physical model being solved: the camera is a
#      damped spring on roll, pan and focal length that heavy events push and
#      that recovers by itself; the suspended matter has a world position, a
#      height off the boards and a velocity, and is depth-sorted with the
#      bodies; the orbiting copies are on real circles about a moving centre
#      and are released on the tangent. Nothing in act two adds a constant to
#      a coordinate, and nothing shakes for the sake of shaking.
#
# THE ARCHIVIST
#   It is wearing Matsuda. It is not Matsuda, it never speaks in her voice,
#   and it never speaks at all. The shape is a filing decision. It is not
#   trying to kill the party member; it is trying to finish the entry, and the
#   party member is what the entry is about.
#
#   THE SPRITE ALREADY HOLDS ITS GLAIVE. Nothing may draw a second one in its
#   hands -- an unattached weapon sliding around beside it is the exact
#   failure rule 2 exists to catch. glaive_biography.png is used ONLY for the
#   spectral COPIES it throws, which are visibly not the real one (tinted,
#   translucent, trailing).
#
# ARCHITECTURE (kototouhou.rpy / tsubaki_soul.rpy's proven 60fps pattern)
#   * BIOGame owns ALL simulation state; plain dicts and lists, zero
#     displayables, no rendering.
#   * BIOStage is ONE creator-defined displayable that steps the sim on a
#     fixed 1/60s accumulator inside render() and paints from cached-texture
#     blits. The screen tree is static; only the CDD repaints.
#   * Two shaders. inv.soup is the room: an opaque quad hosted ON
#     hyperspace.png with mesh True, domain-warped, boiled, and carrying the
#     wormhole vortex. inv.flesh is the body: band-warp, chromatic split,
#     squash/stretch about a pivot, and an erosion dissolve for materializing.
#     Both registered defensively; the fight degrades rather than dying.
#
# READ THIS FIRST IF YOU ARE LOST
#   BIOGame.step() is a mode dispatcher. self.mode is one of:
#     arrive  the rupture and the extrusion
#     menu / sub    act one commands
#     beat    the one-line mechanical readout for a resolved action; it WAITS
#             for a keypress, it never auto-advances (nobody gets left behind)
#     enemy   its turn
#     shift   the corruptive tear
#     open    act two, real time
#   and in act two self.b_state is one of idle / wind / act / recover /
#   BUCKLE, where buckle is the earned exposure and the only state in which a
#   dagger takes real health.
#     leave_w / leave_l   dragged back into the hole / the hole closing over you
#   Units: screen pixels (1280x720), speeds are px per 1/60s tick, timers are
#   ticks. Angles are DEGREES, clockwise, 0 = right (screen space, y down).
# =============================================================================

# --- SHADERS -----------------------------------------------------------------
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
        """, fragment_300="""
            const float BIO_TAU = 6.2831853;

            // --- THE CAMERA ---------------------------------------------------
            // Act two is shot through a camera that rolls, pans and breathes
            // on its focal length. This fragment knows where it landed on the
            // SENSOR; everything downstream (the horizon, the floor, the hole)
            // is reasoned about in the camera's own un-rolled frame, so the
            // shader and the projected entities agree exactly. Every term is
            // an honest camera move -- a roll is an image rotation, a focal
            // change is a scale about the principal point -- which is what
            // keeps the nausea from reading as a rendering fault.
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

            vec2 c = uv - 0.5;

            // --- the wormhole -------------------------------------------------
            // Everything within its reach is dragged around the point and
            // pulled inward; the core goes black and the lip burns.
            vec2 hp = (u_bio_hole.xy / max(u_bio_res, vec2(1.0))) - 0.5;
            float hr = max(u_bio_hole.z, 1.0) / max(u_bio_res.x, 1.0);
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

            // --- rotational momentum -----------------------------------------
            // The soup does not only breathe in and out -- it TURNS, and it
            // turns at a different rate at every radius, so the field is
            // permanently shearing against itself rather than spinning like a
            // picture on a spindle. The base angle is INTEGRATED in the sim
            // (u_bio_spin), so changing the rate never jumps the phase; the
            // differential term oscillates, so the twist winds and unwinds
            // instead of degenerating into smear. The pivot drifts, so there
            // is no fixed centre to read the rotation against.
            vec2 pivot = vec2(sin(t * 0.13) * 0.06, cos(t * 0.17) * 0.05);
            vec2 rc = c - pivot;
            float rr = length(rc);
            // Three timescales, because one reads as a mechanism: a slow wind
            // (~33s) that twists the outside against the inside, a slower
            // counter-rock, and a short ripple that keeps the contortion
            // legible from moment to moment instead of only in hindsight.
            float twist = u_bio_spin
                        + sin(t * 0.19) * 1.15 * rr
                        + sin(t * 0.11 + rr * 4.0) * 0.45 * (1.0 + corrupt)
                        + sin(t * 0.53 + rr * 7.0) * 0.16 * (1.0 + corrupt);
            float tcs = cos(twist);
            float tsn = sin(twist);
            c = pivot + vec2(rc.x * tcs - rc.y * tsn, rc.x * tsn + rc.y * tcs);

            // --- nausea: a slow barrel wobble the whole frame breathes with --
            // FURY is how far through the entry it has got. It does not add a
            // new effect, it leans on the ones already here: the barrel
            // breathes harder, a second lens term fights the first at a
            // different rate (so the distortion never settles into a loop the
            // eye can pre-empt), and the whole frame shears on a slow drift.
            float r = length(c);
            float wob = sin(t * 0.37) * 0.055 + sin(t * 0.19 + 1.7) * 0.035;
            wob += (sin(t * 0.83 + 2.1) * 0.030 + sin(t * 1.29) * 0.018) * fury;
            c *= 1.0 + wob * (r * r) * (1.0 + 1.5 * corrupt + 0.9 * fury);
            c.x += sin(c.y * 3.1 + t * 0.61) * 0.022 * fury;
            c.y += sin(c.x * 2.7 - t * 0.47) * 0.014 * fury;

            // --- the rush: everything falls into (or out of) the middle ------
            float rush = u_bio_rush;
            c *= 1.0 + 0.20 * sin(rush * 0.9 + r * 5.0);
            c += normalize(c + vec2(1e-5)) * 0.035 * sin(rush * 1.3 - r * 8.0);

            // --- boiling: two warp fields at different scales and rates ------
            vec2 w1 = vec2(bio_fbm(c * 3.1 + vec2(t * 0.21, -t * 0.17)),
                        bio_fbm(c * 3.1 + vec2(9.2 - t * 0.13, 4.7 + t * 0.11)));
            // The fine layer runs COUNTER to the coarse one, so the two boils
            // grind against each other instead of travelling together -- this
            // is what stops the rotation reading as one turning image.
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

            // A tear that sweeps down the frame rather than sitting still --
            // one band of rows displaced, travelling, so the room reads as
            // being read off a surface that is slipping.
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
            // Act two is fought on a floor, not in a void. Everything below
            // the horizon is inverse-projected back into world space and
            // sampled from the same plate as the sky, so the ground is made
            // of the same unfinished matter -- and it RUSHES, which is where
            // the momentum comes from.
            if (u_bio_floor > 0.5) {
                float py = cpu.y;
                if (py > u_bio_horizon - 26.0) {
                    float persp = (py - u_bio_horizon) / max(u_bio_floork, 1.0);
                    persp = max(persp, 0.001);
                    float wz = 1.0 / persp;
                    float wx = (uv.x - 0.5) * u_bio_res.x / persp;

                    vec2 fuv = vec2(wx * 0.00085,
                                    wz * 0.30 + u_bio_fscroll);
                    vec3 fl = texture2D(tex0, bio_mirror(fuv)).rgb;
                    float flum = dot(fl, vec3(0.299, 0.587, 0.114));
                    vec3 floorc = mix(fl * 0.42,
                                    vec3(flum * 1.20, flum * 0.22, flum * 0.30),
                                    corrupt);

                    // Rushing rings of depth and converging rails. These
                    // ARE the floor -- without them the plate reads as more
                    // sky and the whole stage collapses back into 2D, so they
                    // are deliberately bright enough to see through the murk.
                    float rings = abs(fract(wz * 1.15 - u_bio_fscroll * 2.2)
                                    * 2.0 - 1.0);
                    floorc += vec3(0.85, 0.16, 0.24)
                            * smoothstep(0.72, 1.0, rings) * (0.55 + 0.7 * pulse);
                    float rails = abs(fract(wx * 0.0018) * 2.0 - 1.0);
                    floorc += vec3(0.42, 0.48, 0.62)
                            * smoothstep(0.80, 1.0, rails) * 0.55;

                    // Haze toward the horizon, so distance actually reads.
                    float haze = smoothstep(0.02, 0.55, persp);
                    floorc = mix(col * 0.85, floorc, haze);
                    floorc *= 0.55 + 0.65 * haze;

                    // Feather the horizon instead of cutting it -- a hard
                    // seam across the frame looked like a rendering error
                    // rather than a distance.
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
                stretch=(1.0, 1.0), pivot=0.86, hurt=0.0, diss=0.0):
        """Wrap a padded plate in BIOGRAPHY'S OWN body shader.

        Mirrors inv_flesh()'s signature so the call site reads the same, plus
        the two knobs that are this shader's own: SLIP (how far a band samples
        from the wrong part of the body) and MOSH (how much of the plate is
        holding a stale registration in macroblocks).
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
            u_mis_diss=float(diss))


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
    BIO_WIN = "#05040be8"
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

        def __init__(self, retry=False, deaths=0, debug=False, start_open=False):
            self.result = None
            self.paused = False
            self.debug = bool(debug)
            self.retry = bool(retry)
            self.deaths = int(deaths)
            self.god = inv_godmode_on()

            self.tick = 0
            self.clock = 0.0
            self.rush = 0.0
            self.spin = 0.0             # integrated rotation of the whole room
            self.rng = inv_random.Random()
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

        def _beat(self, label, value="", after="enemy"):
            """Queue the mechanical readout for one resolved action."""
            self.beat_label = label
            self.beat_value = value
            self.beat_after = after
            self.mode = "beat"
            self.mtick = 0

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

        def damage_boss(self, amount, x=None, y=None, big=False, quiet=False):
            """`quiet` takes the health off without printing it -- act two's
            composed hits print their POISE figure instead, which is the thing
            the throw was actually for."""
            amount = int(max(0, amount))
            self.boss_hp = int(max(0, self.boss_hp - amount))
            self.boss_pose = -1.0
            if x is not None and not quiet:
                self.float_text(x, y, str(amount), BIO_WARN if big else BIO_INK, big)

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
            self.mode = "menu"
            self.mtick = 0
            self.cursor = 0
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
            # WAITS. Never advances on its own -- rule for slow readers.
            self.mtick += 1
            if self.mtick > 12 and (edges["z"] or edges["x"]):
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
                    self.flash = 0.5
                    self.shake = 0.8
                    label = "BASH  CRITICAL"
                else:
                    self.play("bash")
                    self.shake = 0.35
                self.damage_boss(dmg, 640, 300, crit)
                value = "-" + str(dmg)

            elif cmd == "mend":
                if self.pp < BIO_MEND_PP:
                    self.play("cancel")
                    self._beat("MEND", "NO PP", "menu")
                    return
                self.pp -= BIO_MEND_PP
                self.hp = int(min(BIO_HP_MAX, self.hp + BIO_MEND_HEAL))
                self.play("heal")
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
                value = "-" + str(BIO_REFUSE_DMG)
                if self.telegraph:
                    self.telegraph = False
                    value += "   BROKEN"

            elif cmd == "check":
                self.pp = int(min(BIO_PP_MAX, self.pp + BIO_CHECK_PP_GAIN))
                self.read = True
                self.boss_known = True
                self.play("scan")
                value = str(self.boss_hp) + " / " + str(BIO_BOSS_HP_MAX)

            elif cmd == "defend":
                self.guard = True
                self.pp = int(min(BIO_PP_MAX, self.pp + BIO_DEFEND_PP_GAIN))
                self.play("guard")
                value = "+" + str(BIO_DEFEND_PP_GAIN) + " PP"

            elif cmd == "run":
                # It never works. It is never explained.
                self.play("miss")
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
            if self.mtick < 26:
                return

            move = self._pick_enemy_move()
            self.last_enemy = move
            self.boss_pose = 1.0
            dmg = 0
            value = ""

            if move == "read":
                dmg = 34
            elif move == "cross":
                dmg = 26
                drain = min(self.pp, 6)
                self.pp -= drain
                if drain:
                    value = "-" + str(drain) + " PP  "
            elif move == "margin":
                dmg = 14
                self.bleed = 3
            elif move == "thumb":
                self.telegraph = True
                value = "WINDING UP"
            elif move == "page":
                dmg = 76
                self.telegraph = False
                self.flash = 0.6
                self.jolt = 0.9
            elif move == "glaive":
                dmg = 42
            elif move == "correct":
                self.boss_hp = int(min(BIO_BOSS_HP_MAX, self.boss_hp + 25))
                value = "+25"

            if dmg > 0:
                if self.guard:
                    dmg = int(dmg * BIO_GUARD_MULT)
                if self.read:
                    dmg = int(dmg * BIO_READ_MULT)
                self.play("enemy", 0.8)
                self.hurt(dmg, 640, 470)
                value += "-" + str(dmg)

            if self.bleed > 0 and move != "margin":
                self.bleed -= 1
                self.hurt(11, 640, 500)
                value += "   -11"

            self.read = False
            self.guard = False

            after = "menu"
            if self.corrupt <= 0.0 and (self.boss_hp <= BIO_SHIFT_HP
                                        or self.turn >= BIO_SHIFT_TURN_CAP):
                after = "shift"
            self._beat("BIOGRAPHY", value, after)

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
            if 20 <= t < 110:
                self.panel_slide = bio_smooth((t - 20) / 90.0)
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

        # ----- discharge (cosmetic lightning) --------------------------------
        # The hyperspace "has not finished deciding what matter is", and until
        # now it only ever said so in the shaders. These are the arcs from the
        # shared atlas (asset_definitions/def_bullets.rpy, EMB_ARCS): four hand-drawn
        # bolts that get stretched, rotated and cycled. They have NO mechanics
        # -- nothing here can touch the player -- so they are free to be loud
        # at exactly the moments that have earned it.

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

    def bio_persp_free(wy):
        """bio_persp WITHOUT the clamp, for things that are not standing on the
        stage -- suspended matter drifts past both edges of it, and a clamped
        perspective would freeze a piece of debris in place at the bottom of
        the frame instead of letting it come past the lens."""
        ax0, ay0, ax1, ay1 = BIO_ARENA
        u = (wy - ay0) / float(ay1 - ay0)
        den = inv_lerp(1.0 / BIO_PERSP_FAR, 1.0 / BIO_PERSP_NEAR, u)
        return 1.0 / max(den, 0.12)

    def bio_project_free(wx, wy):
        pp = bio_persp_free(wy)
        return (640.0 + (wx - 640.0) * pp,
                BIO_CAM_HORIZON + BIO_FLOOR_K * pp,
                pp)

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
init python:
    class BIOStage(renpy.Displayable):
        """One creator-defined displayable. Steps BIOGame on a fixed 60Hz
        accumulator inside render() and paints from cached-texture blits."""

        _tf_cache = {}
        _misc_cache = {}
        _text_cache = {}

        # Act one panels. Deliberately short and pushed to the bottom corners
        # so the Archivist is never boxed in by furniture (rule 2).
        PANEL_CMD = (40, 548, 470, 148)
        PANEL_HUD = (770, 548, 470, 148)

        def __init__(self, game, **kwargs):
            super(BIOStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0

        # ----- cached factories ------------------------------------------------

        def _misc(self, key, builder):
            d = BIOStage._misc_cache.get(key)
            if d is None:
                if len(BIOStage._misc_cache) > 700:
                    BIOStage._misc_cache.clear()
                d = builder()
                BIOStage._misc_cache[key] = d
            return d

        def _text(self, text, size, color, font=INV_FONT, bold=False, outline=True):
            key = (text, size, color, font, bold, outline)
            t = BIOStage._text_cache.get(key)
            if t is None:
                if len(BIOStage._text_cache) > 220:
                    BIOStage._text_cache.clear()
                outl = [(2, "#04030a", 0, 0)] if outline else []
                t = Text(text, size=size, color=color, bold=bold, font=font,
                        outlines=outl, substitute=False)
                BIOStage._text_cache[key] = t
            return t

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
            tf = BIOStage._tf_cache.get(key)
            if tf is None:
                kw = dict(zoom=zoom, subpixel=True)
                if ab < 6:
                    kw["alpha"] = ab / 6.0
                if tint:
                    kw["matrixcolor"] = TintMatrix(tint)
                tf = Transform(BIO_SPRITE, **kw)
                BIOStage._tf_cache[key] = tf
            return tf

        def _zbucket(self, persp):
            """Quantised perspective, so a sprite that scales continuously with
            depth still shares a small, bounded set of cached transforms."""
            return int(inv_clamp(persp, 0.20, 1.40) * 8.0)

        def _zscale(self, zb):
            return zb / 8.0

        def _copy_tf(self, deg, zb=8):
            """A spectral duplicate of the glaive. Never the real one."""
            bucket = int(round(deg / BIO_ROT_STEP)) % BIO_ROT_BUCKETS
            key = ("copy", bucket, zb)
            tf = BIOStage._tf_cache.get(key)
            if tf is None:
                tf = Transform(BIO_GLAIVE,
                            zoom=BIO_GLAIVE_ZOOM * self._zscale(zb),
                            rotate=bucket * BIO_ROT_STEP - BIO_GLAIVE_REST_DEG,
                            alpha=0.72, matrixcolor=TintMatrix("#ff5a6e"),
                            subpixel=True)
                BIOStage._tf_cache[key] = tf
            return tf

        def _blade_tf(self, deg, zb=8, fade=0):
            """The swung blade: a spectral pass of the glaive rather than a
            drawn line. `fade` indexes its after-images along the arc, which is
            what turns one blade into a swing."""
            bucket = int(round(deg / BIO_ROT_STEP)) % BIO_ROT_BUCKETS
            key = ("blade", bucket, zb, fade)
            tf = BIOStage._tf_cache.get(key)
            if tf is None:
                alpha = (0.92, 0.46, 0.24, 0.13)[min(fade, 3)]
                tint = ("#ffd8de", "#ff8496", "#ff5a6e", "#ff3d54")[min(fade, 3)]
                tf = Transform(BIO_GLAIVE,
                            zoom=BIO_GLAIVE_ZOOM * self._zscale(zb) * 1.25,
                            rotate=bucket * BIO_ROT_STEP - BIO_GLAIVE_REST_DEG,
                            alpha=alpha, matrixcolor=TintMatrix(tint),
                            subpixel=True)
                BIOStage._tf_cache[key] = tf
            return tf

        def _dagger_tf(self, deg, zb=8):
            bucket = int(round(deg / BIO_ROT_STEP)) % BIO_ROT_BUCKETS
            key = ("dag", bucket, zb)
            tf = BIOStage._tf_cache.get(key)
            if tf is None:
                tf = Transform(BIO_DAGGER,
                            zoom=BIO_DAGGER_ZOOM * self._zscale(zb),
                            nearest=True,
                            rotate=bucket * BIO_ROT_STEP - BIO_DAGGER_REST_DEG,
                            matrixcolor=TintMatrix(BIO_TEAL), subpixel=True)
                BIOStage._tf_cache[key] = tf
            return tf

        # ----- input -----------------------------------------------------------

        def event(self, ev, x, y, st):
            self.game.keys.handle_event(ev)
            return None

        # ----- render ----------------------------------------------------------

        def render(self, width, height, st, at):
            global BIO_SHADER_OK
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

            rv = renpy.Render(1280, 720)
            frame_tex = {}

            def tex(key, disp, w=1280, h=720):
                entry = frame_tex.get(key)
                if entry is None:
                    r = renpy.render(disp, w, h, st, at)
                    rv.depends_on(r)
                    entry = (r, r.get_size())
                    frame_tex[key] = entry
                return entry

            def rect(color, w, h):
                w = max(1, int(w))
                h = max(1, int(h))
                key = ("rect", color, w, h)
                entry = frame_tex.get(key)
                if entry is None:
                    solid = self._misc(("solid", color), lambda c=color: Solid(c))
                    r = renpy.render(solid, w, h, st, at)
                    rv.depends_on(r)
                    entry = r
                    frame_tex[key] = entry
                return entry

            def qa(a):
                return "%02x" % (int(inv_clamp(a, 0.0, 1.0) * 7.0) * 34 + 6)

            def blit_text(disp_text, size, color, x, y, font=INV_FONT, bold=False,
                        anchor=(0.0, 0.0), w=1200, h=200, key=None, outline=True):
                t = self._text(disp_text, size, color, font=font, bold=bold,
                            outline=outline)
                r, (tw, th) = tex(key or ("t", disp_text, size, color, font, bold, w),
                                t, w, h)
                rv.blit(r, (int(x - tw * anchor[0]), int(y - th * anchor[1])))
                return (tw, th)

            canvas_layer = [None]

            def canvas():
                if canvas_layer[0] is None:
                    layer = renpy.Render(1280, 720)
                    canvas_layer[0] = layer.canvas()
                    rv.blit(layer, (0, 0))
                return canvas_layer[0]

            # A sprite layer for the FLOOR. Matsu'Py fixes a layer's z-order at
            # the moment it is first blitted into rv, and the floor canvas
            # claims its slot before any figure is drawn -- so sprite art that
            # belongs on the boards cannot just go through sblit, or it would
            # draw on top of the people standing on it. This layer is created
            # on first use, which happens inside the floor-hazard pass, i.e.
            # after the canvas and before the bodies. Exactly where a hazard
            # lives.
            #
            # NOTE: this is a closure over `render`'s locals, so it MUST be
            # handed to _render_open explicitly -- that is a separate method
            # and only sees what it is passed. Forgetting that raises a
            # NameError which the hazard's own try/except swallows, and the
            # bars simply stop drawing with no error anywhere.
            floor_layer = [None]

            def fblit(r, pos):
                if floor_layer[0] is None:
                    layer = renpy.Render(1280, 720)
                    floor_layer[0] = layer
                    rv.blit(layer, (0, 0))
                floor_layer[0].subpixel_blit(r, pos)

            sblit = rv.subpixel_blit

            shake_x = shake_y = 0
            if g.shake > 0.01:
                amp = 13.0 * g.shake
                shake_x = int(math.sin(g.tick * 1.9) * amp)
                shake_y = int(math.cos(g.tick * 2.7) * amp * 0.6)

            # The camera body, resolved once per frame and handed to the soup
            # shader and to every projection below, so the two never disagree.
            cam = g.cam_tuple()

            # --- 1. THE SOUP (and the hole in it) ------------------------------
            if BIO_SHADER_OK:
                try:
                    quad = Transform(
                        BIO_SOUP_IMG, xysize=(1280, 720), mesh=True,
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
                        u_bio_floor=(1.0 if g.corrupt > 0.55 else 0.0),
                        u_bio_horizon=BIO_CAM_HORIZON,
                        u_bio_floork=BIO_FLOOR_K,
                        u_bio_fscroll=g.rush * 0.35,
                        u_bio_fury=g.fury,
                        u_bio_cam=cam,
                        u_bio_hole=(float(g.hole[0]), float(g.hole[1]),
                                    float(g.hole[2]), float(g.hole[3])))
                    qr = renpy.render(quad, 1280, 720, st, at)
                    rv.depends_on(qr)
                    rv.blit(qr, (0, 0))
                except Exception as soup_e:
                    BIO_SHADER_OK = False
                    try:
                        renpy.log("INV FX: soup render failed: %r" % soup_e)
                    except Exception:
                        pass
                    rv.blit(rect(BIO_BLACK, 1280, 720), (0, 0))
            else:
                rv.blit(rect(BIO_BLACK, 1280, 720), (0, 0))

            # --- 2. suspended matter -------------------------------------------
            # SCREEN SPACE, so it hands over to the world-space debris as the
            # stage comes up. Confetti painted flat across a perspective floor
            # reads as dirt on the lens and undoes the depth the rest of the
            # frame is working for; act one has no stage, so there it is fine.
            flat = 1.0 - inv_clamp((g.corrupt - 0.35) / 0.45, 0.0, 1.0)
            if g.dark < 0.95 and flat > 0.03:
                mote_col = ("#dfe9ff" if g.corrupt < 0.5 else "#ffb9c6")
                for m in g.motes:
                    a = (0.10 + 0.35 * m["z"]) * flat
                    if a < 0.145:
                        continue
                    s = m["s"]
                    rv.blit(rect(mote_col + qa(a), s, s),
                            (int(m["x"]) + shake_x, int(m["y"]) + shake_y))
                ring_a = int((42 if g.corrupt < 0.5 else 46) * flat)
                if ring_a > 5:
                    ring_col = ((90, 140, 255, ring_a) if g.corrupt < 0.5
                                else (255, 60, 90, ring_a))
                    cv = canvas()
                    for b in g.bubbles:
                        try:
                            cv.circle(ring_col,
                                    (int(b["x"]) + shake_x, int(b["y"]) + shake_y),
                                    int(max(4, b["r"])), 2)
                        except Exception:
                            pass

            # --- 3. the fight ---------------------------------------------------
            if g.mode == "open" or (g.mode in ("leave_w", "leave_l") and g.corrupt > 0.4):
                self._render_open(g, rv, tex, rect, qa, blit_text, canvas,
                                sblit, shake_x, shake_y, st, at, cam, fblit)
            else:
                self._render_act_one(g, rv, tex, rect, qa, blit_text, canvas,
                                    sblit, shake_x, shake_y, st, at)

            # --- 4. floating numbers --------------------------------------------
            for f in g.floats:
                a = inv_clamp(f["life"] / 26.0, 0.0, 1.0)
                if f.get("world"):
                    fx, fy, fpp = bio_project(f["x"], f["y"])
                    fx, fy = bio_cam_apply(fx, fy, cam)
                    size = int((30 if f["big"] else 21) * (0.62 + 0.38 * fpp))
                else:
                    fx, fy = f["x"], f["y"]
                    size = 30 if f["big"] else 21
                blit_text(f["text"], size,
                        f["color"] + qa(a), int(fx) + shake_x,
                        int(fy) + shake_y, bold=f["big"], anchor=(0.5, 0.5),
                        w=260, h=60)

            # --- 5. pause --------------------------------------------------------
            if g.paused:
                rv.blit(rect("#04030ac4", 1280, 720), (0, 0))
                blit_text("PAUSED", 40, BIO_INK, 640, 316, bold=True,
                        anchor=(0.5, 0.5), w=600, h=70)
                blit_text("ESC  RESUME        Q  QUIT", 16, BIO_DIM,
                        640, 372, anchor=(0.5, 0.5), w=800, h=44)

            # THE DRAW RATE IS THE TICK RATE. Every pixel above is a pure
            # function of the simulation state: nothing in this method reads
            # self.acc and nothing interpolates between ticks, so between two
            # 1/60s ticks this stage paints a byte-identical picture. Asking
            # for the next frame IMMEDIATELY meant a 165Hz or 240Hz panel ran
            # the entire draw -- every python-side blit, every full-screen
            # shader pass, and the mark-and-sweep over every Render they make
            # -- two to four times per tick and threw the extra frames away.
            #
            # Handing redraw() the time remaining until the next tick lets the
            # engine's scheduler wake us exactly when there is something new to
            # draw. It wakes at the first vblank at or after the delay, so a
            # 60Hz display is unaffected and only a high-refresh one stops
            # paying. Input is unchanged: the key latch is polled inside
            # step(), on the tick. Same governor as kototouhou.rpy.
            if g.result is None and not g.paused:
                renpy.redraw(self, max(0.0, INV_TICK - self.acc))
            return rv

        # ----- the body --------------------------------------------------------

        def _draw_body(self, g, rv, tex, sblit, cx, cy, zoom, sx, sy,
                    st, at, warp=1.0, rot=0.0, stretch=(1.0, 1.0),
                    diss=0.0, hurt=0.0):
            """Rule 3 lives here. One warped, contorting, banking body."""
            plate, W, H = self._body_plate(zoom)

            # THE MISREGISTRATION CLIMBS WITH THE ENTRY. Act one is a plate
            # that is very slightly out; by the corruptive state it is being
            # assembled out of slices that do not belong to each other, and
            # blocks of it are holding a registration from a second ago. Both
            # knobs ride g.corrupt and g.fury rather than a clock, so the body
            # comes apart at exactly the rate the fight does.
            slip = 0.30 + 0.60 * g.corrupt + 0.35 * g.fury
            mosh = 0.06 + 0.44 * g.corrupt + 0.34 * g.fury

            if BIO_MISREG_OK:
                try:
                    body = bio_misreg(plate, W, H, g.clock, warp=warp,
                                    split=1.0, slip=slip, mosh=mosh,
                                    stretch=stretch, pivot=0.86, hurt=hurt,
                                    diss=diss)
                    if abs(rot) > 0.05:
                        body = Transform(body, rotate=rot, subpixel=True)
                    r = renpy.render(body, W, H, st, at)
                    rv.depends_on(r)
                    w, h = r.get_size()
                    sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))
                    return
                except Exception as misreg_e:
                    try:
                        renpy.log("INV FX: misreg render failed: %r" % misreg_e)
                    except Exception:
                        pass

            if INV_FLESH_OK:
                try:
                    body = inv_flesh(plate, W, H, g.clock, warp=warp,
                                    stretch=stretch, pivot=0.86, hurt=hurt,
                                    diss=diss)
                    if abs(rot) > 0.05:
                        body = Transform(body, rotate=rot, subpixel=True)
                    r = renpy.render(body, W, H, st, at)
                    rv.depends_on(r)
                    w, h = r.get_size()
                    sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))
                    return
                except Exception as flesh_e:
                    try:
                        renpy.log("INV FX: flesh render failed: %r" % flesh_e)
                    except Exception:
                        pass

            r, (w, h) = tex(("plainbody", round(zoom, 3)),
                            self._body_plain(zoom), 900, 900)
            sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))

        def _draw_heart(self, g, rv, tex, sblit, cx, cy, sx, sy, st, at,
                    scale=1.0):
            """The player's avatar in a corruptive state: the SOUL heart the
            other game modes run on, put through the same shader as the
            Archivist and warped harder than anything else on screen. It beats
            -- squashing on the downbeat -- and it is never drawn clean."""
            plate, W, H = inv_body_plate(INV_HEART, INV_HEART_W, INV_HEART_H,
                                        BIO_HEART_ZOOM * max(0.18, scale),
                                        pad_x=2.2, pad_y=2.2, nearest=True)
            beat = 1.0 - 0.16 * g.beat_pulse
            if INV_FLESH_OK:
                try:
                    d = inv_flesh(plate, W, H, g.clock * 2.3,
                                warp=BIO_HEART_WARP, split=0.85,
                                stretch=(1.0 / max(0.5, beat), beat),
                                pivot=0.5, hurt=0.0,
                                diss=0.04 + 0.04 * math.sin(g.clock * 3.1))
                    r = renpy.render(d, W, H, st, at)
                    rv.depends_on(r)
                    w, h = r.get_size()
                    sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))
                    return
                except Exception:
                    pass
            hz = BIO_HEART_ZOOM * max(0.18, scale)
            heart = self._misc(("heartplain", round(hz, 2)),
                            lambda z=hz: Transform(INV_HEART, zoom=z,
                                                nearest=True, subpixel=True))
            r, (w, h) = tex(("heartplain", round(hz, 2)), heart, 160, 160)
            sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))

        # ----- ACT ONE ---------------------------------------------------------

        def _render_act_one(self, g, rv, tex, rect, qa, blit_text, canvas,
                            sblit, sx, sy, st, at):
            arriving = (g.mode == "arrive")
            bob = math.sin(g.clock * 1.15) * 9.0
            zoom = BIO_BOSS_ZOOM_ACT1
            cy = 300 + bob

            if arriving:
                # Comes out of the hole: too tall for the room, still eroding.
                # IT ARRIVES AT ITS RESTING POSITION. This used to place the
                # body relative to the HOLE for the whole arrival and then
                # switch to an absolute resting cy the instant the bout began,
                # so the last frame of the entrance and the first frame of act
                # one were 60-80px apart and the figure visibly jumped as the
                # panels came up. (Mystery never had the bug because it uses
                # one expression throughout -- that is the fix, generalised.)
                #
                # Lerping the REST position toward the hole by `emerge` makes
                # the seam impossible rather than merely unlikely: emerge is
                # driven to exactly 0.0 at the end of the arrival, so the last
                # arrival frame IS the resting frame, whatever either value is
                # tuned to later.
                cy = inv_lerp(cy, g.hole[1] + 40.0, g.emerge)
                stretch = (1.0 / max(0.35, g.body_scale) ** 0.4, g.body_scale)
                warp = 1.0 + 1.0 * g.emerge
                diss = g.emerge * 0.85
            else:
                stretch = (getattr(g, "body_sx", 1.0), getattr(g, "body_sy", 1.0))
                warp = 0.55 + 0.35 * math.sin(g.clock * 0.7)
                diss = 0.0

            self._draw_body(g, rv, tex, sblit, 640, cy, zoom, sx, sy, st, at,
                            warp=warp, rot=g.boss_pose * 3.0, stretch=stretch,
                            diss=diss, hurt=0.85 if g.hit_flash > 0.4 else 0.0)

            if arriving:
                return

            # --- the only chrome act one gets ------------------------------------
            # A name and a bar, both small, both far from the sprite. The bar is
            # empty until CHECK has been used.
            blit_text("BIOGRAPHY", 15, BIO_RED, 380, 28, bold=True, w=300, h=30)
            bar_w = 520
            rv.blit(rect("#04030ab4", bar_w + 4, 12), (380 - 2, 52))
            if g.boss_known:
                rv.blit(rect(BIO_RED_DEEP, bar_w, 8), (380, 54))
                fill = int(bar_w * inv_clamp(g.boss_shown / float(BIO_BOSS_HP_MAX),
                                            0.0, 1.0))
                if fill > 0:
                    rv.blit(rect(BIO_RED, fill, 8), (380, 54))

            slide = int(g.panel_slide * 200)
            if g.panel_slide < 1.0:
                self._panel(rv, rect, BIOStage.PANEL_CMD, sx, sy + slide)
                self._panel(rv, rect, BIOStage.PANEL_HUD, sx, sy + slide)
                self._panel_contents(g, rv, tex, rect, qa, blit_text, sx, sy + slide)

        def _panel(self, rv, rect, box, sx, sy):
            x, y, w, h = box
            x += sx
            y += sy
            rv.blit(rect(BIO_INK, w + 6, h + 6), (x - 3, y - 3))
            rv.blit(rect(BIO_BLACK, w + 2, h + 2), (x - 1, y - 1))
            rv.blit(rect(BIO_WIN, w, h), (x, y))

        def _panel_contents(self, g, rv, tex, rect, qa, blit_text, sx, sy):
            cx, cy, cw, ch = BIOStage.PANEL_CMD
            cx += sx
            cy += sy

            if g.mode in ("menu", "sub"):
                rows = BIO_CMDS if g.mode == "menu" else BIO_RECALLS
                cursor = g.cursor if g.mode == "menu" else g.sub_cursor
                for i, row in enumerate(rows):
                    live = (i == cursor)
                    ry = cy + 16 + i * 30
                    if live:
                        rv.blit(rect(BIO_INK + qa(0.13), cw - 28, 26), (cx + 14, ry - 3))
                        rv.blit(rect(BIO_TEAL, 9, 9), (cx + 22, ry + 6))
                    blit_text(row[1], 20, BIO_INK if live else BIO_FAINT,
                            cx + 42, ry, bold=live, w=260, h=30)
                    if g.mode == "sub" and row[2]:
                        blit_text(str(row[2]) + " PP", 14,
                                BIO_TEAL if live else BIO_FAINT,
                                cx + cw - 22, ry + 4, anchor=(1.0, 0.0), w=120, h=26)
                # Tucked into the bottom-right corner rather than sitting
                # directly under the last command, where it reads as a fifth
                # entry in the list.
                blit_text("Z  OK      X  BACK      ESC  PAUSE", 12, BIO_FAINT,
                        cx + cw - 16, cy + ch - 22, anchor=(1.0, 0.0),
                        w=420, h=24)

            elif g.mode == "beat":
                blit_text(g.beat_label, 22, BIO_INK, cx + 20, cy + 30, bold=True,
                        w=cw - 40, h=40)
                if g.beat_value:
                    blit_text(g.beat_value, 30, BIO_WARN, cx + 20, cy + 62,
                            bold=True, w=cw - 40, h=44)
                if g.mtick > 12 and (g.tick // 20) % 2 == 0:
                    rv.blit(rect(BIO_INK, 14, 4), (cx + cw - 36, cy + ch - 26))

            # --- status ---------------------------------------------------------
            hx, hy, hw, hh = BIOStage.PANEL_HUD
            hx += sx
            hy += sy
            blit_text(inv_player_name(), 19, BIO_INK, hx + 20, hy + 12,
                    bold=True, w=hw - 40, h=32)
            self._odometer(g, rv, tex, rect, qa, blit_text, "HP", g.hp_shown,
                        g.hp, hx + 20, hy + 44, BIO_INK)
            self._odometer(g, rv, tex, rect, qa, blit_text, "PP", g.pp_shown,
                        g.pp, hx + 20, hy + 96, BIO_TEAL, small=True)
            if g.telegraph:
                blit_text("INCOMING", 13, BIO_WARN, hx + hw - 20, hy + 16,
                        anchor=(1.0, 0.0), w=200, h=26)
            if g.god:
                blit_text("GOD", 12, BIO_WARN + "aa", hx + hw - 20, hy + hh - 24,
                        anchor=(1.0, 0.0), w=120, h=24)

        def _odometer(self, g, rv, tex, rect, qa, blit_text, label, shown, real,
                    x, y, color, small=False):
            """An EarthBound counter: fixed-width cells, and the digits that are
            moving are drawn mid-roll rather than swapped."""
            size = 22 if small else 30
            cell_w = 22 if small else 28
            cell_h = 32 if small else 42
            blit_text(label, 14, color, x, y + (6 if small else 12), bold=True,
                    w=50, h=28)

            value = int(math.ceil(shown - 0.0001)) if shown > 0 else 0
            rolling = abs(shown - real) > 0.05
            digits = "%03d" % inv_clamp(value, 0, 999)
            frac = shown - math.floor(shown)
            base_x = x + 40

            for i, ch in enumerate(digits):
                dx = base_x + i * cell_w
                rv.blit(rect("#0a0812e0", cell_w - 4, cell_h), (dx, y))
                if rolling:
                    off = int(frac * cell_h * (1 if real < shown else -1))
                    nxt = str((int(ch) + (1 if real > shown else -1)) % 10)
                    blit_text(nxt, size, color + qa(0.45), dx + (cell_w - 4) // 2,
                            y + off - (cell_h if real < shown else -cell_h) + 2,
                            anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)
                    blit_text(ch, size, color, dx + (cell_w - 4) // 2, y + off + 2,
                            anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)
                else:
                    blit_text(ch, size, color, dx + (cell_w - 4) // 2, y + 2,
                            anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)

        # ----- ACT TWO ---------------------------------------------------------

        def _render_open(self, g, rv, tex, rect, qa, blit_text, canvas,
                        sblit, sx, sy, st, at, cam=None, fblit=None):
            """Act two, drawn on a stage.

            The simulation is still the flat plane it always was -- world y is
            depth, and only this function knows that. Everything is projected
            through bio_project(), pushed through the camera body, and then
            drawn FAR FIRST, because depth sorting is what actually sells the
            third dimension; without it a perspective arena is just a picture
            of one.
            """
            ax0, ay0, ax1, ay1 = BIO_ARENA
            cv = canvas()

            def proj(wx, wy):
                px_, py_, pp = bio_project(wx, wy)
                px_, py_ = bio_cam_apply(px_, py_, cam)
                return (px_ + sx, py_ + sy, pp)

            def proj_h(wx, wy, height):
                """Same, for something suspended off the boards rather than
                standing on them: unclamped in depth, and lifted by a HEIGHT
                that foreshortens like everything else."""
                px_, py_, pp = bio_project_free(wx, wy)
                px_, py_ = bio_cam_apply(px_, py_ - height * pp, cam)
                return (px_ + sx, py_ + sy, pp)

            exposed = g._open_exposed()
            leaving = g.mode in ("leave_w", "leave_l")

            # --- the boards ------------------------------------------------------
            # The arena is a trapezoid now, so its edge is four projected
            # corners rather than four screen-aligned bars.
            c_fl = proj(ax0, ay0)
            c_fr = proj(ax1, ay0)
            c_nl = proj(ax0, ay1)
            c_nr = proj(ax1, ay1)
            try:
                cv.lines((255, 45, 78, 90), True,
                        [(int(c_fl[0]), int(c_fl[1])), (int(c_fr[0]), int(c_fr[1])),
                        (int(c_nr[0]), int(c_nr[1])), (int(c_nl[0]), int(c_nl[1]))],
                        2)
            except Exception:
                pass

            # --- floor hazards, which live UNDER everything that stands on it ---
            for h in g.hazards:
                kind = h["kind"]
                if kind == "ring":
                    # A circle on the floor is a chain of projected points --
                    # rows bunch toward the horizon, so an ellipse would float.
                    # Points outside the stage are DROPPED AND THE CHAIN IS
                    # BROKEN; joining across the gap is what turned a shockwave
                    # into a red lump on screen.
                    warn = h["warn"] > 0
                    col = ((255, 207, 92, 150) if warn else (255, 45, 78, 200))
                    thick = 2 if warn else max(2, int(h["w"] * 0.22))
                    runs = []
                    run = []
                    steps = 44
                    for k in range(steps + 1):
                        a2 = k * 6.2831853 / steps
                        wx = h["x"] + math.cos(a2) * h["r"]
                        wy = h["y"] + math.sin(a2) * h["r"]
                        ok = (ax0 - 90 < wx < ax1 + 90
                            and ay0 - 40 < wy < ay1 + 90)
                        if ok:
                            sxx, syy, _pp = proj(wx, wy)
                            if -400 < sxx < 1700 and 0 < syy < 1100:
                                run.append((int(sxx), int(syy)))
                                continue
                        if len(run) > 1:
                            runs.append(run)
                        run = []
                    if len(run) > 1:
                        runs.append(run)
                    for r_ in runs:
                        try:
                            cv.lines(col, False, r_, thick)
                        except Exception:
                            pass

                elif kind == "bar":
                    # A sweeping wall. This used to be a flat canvas line; it
                    # is now the `lens` beam art from the shared atlas, drawn
                    # between the SAME two projected endpoints, so it keeps the
                    # perspective exactly and gains the hot core + falloff that
                    # a hazard this lethal should have had all along. It goes
                    # through fblit, not sblit -- see floor_layer.
                    warning = h["warn"] > 0
                    bcol = "#ffcf5c" if warning else "#ff2d4e"
                    if h["axis"] == "h":
                        wy = h["p"] if not warning else (ay0 if h["spd"] > 0 else ay1)
                        a_, b_, _p1 = proj(ax0, wy)
                        c_, d_, _p2 = proj(ax1, wy)
                        bthick = max(3, int(h["th"] * bio_persp(wy) * 1.05))
                    else:
                        wx = h["p"] if not warning else (ax0 if h["spd"] > 0 else ax1)
                        a_, b_, _p1 = proj(wx, ay0)
                        c_, d_, _p2 = proj(wx, ay1)
                        bthick = max(3, int(h["th"] * 0.95))
                    blen = max(8, int(math.hypot(c_ - a_, d_ - b_)))
                    bbkt = int(math.degrees(math.atan2(d_ - b_, c_ - a_)) / 6.0) % 60
                    baq = 3 if warning else 5
                    bkey = ("biobar", bcol, blen // 10, bthick, bbkt, baq)
                    bar_d = self._misc(bkey, (lambda c=bcol, L=blen, T=bthick,
                                                bk=bbkt, aq=baq: Transform(
                        emb_cell("lens"),
                        xzoom=L / float(emb_size("lens")[0]),
                        yzoom=T / float(emb_size("lens")[1]),
                        rotate=bk * 6.0, subpixel=True,
                        matrixcolor=TintMatrix(c), alpha=(aq + 0.5) / 6.0)))
                    try:
                        bquad = blen + bthick + 24
                        brr_, (brw_, brh_) = tex(bkey, bar_d, bquad, bquad)
                        fblit(brr_, ((a_ + c_) * 0.5 - brw_ * 0.5,
                                    (b_ + d_) * 0.5 - brh_ * 0.5))
                    except Exception:
                        pass

                elif kind == "orbit":
                    # The orbit is DRAWN, as the track on the boards plus a
                    # tether back to the hand holding it. Without the track you
                    # cannot see where the next revolution is going and the
                    # move is a guess; with it, it is a pattern to walk through.
                    runs = []
                    run = []
                    for k in range(37):
                        a2 = k * 6.2831853 / 36.0
                        rr = h["r"] * h["grow"]
                        wx = g.bx + math.cos(a2) * rr
                        wy = g.by + math.sin(a2) * rr * 0.72
                        if ax0 - 90 < wx < ax1 + 90 and ay0 - 60 < wy < ay1 + 90:
                            pt = proj(wx, wy)
                            run.append((int(pt[0]), int(pt[1])))
                            continue
                        if len(run) > 1:
                            runs.append(run)
                        run = []
                    if len(run) > 1:
                        runs.append(run)
                    for r_ in runs:
                        try:
                            cv.lines((255, 90, 118, 60), False, r_, 1)
                        except Exception:
                            pass
                    a_, b_, _p1 = proj(g.bx, g.by)
                    c_, d_, _p2 = proj(h["x"], h["y"])
                    try:
                        cv.line((255, 90, 118, 46), (int(a_), int(b_)),
                                (int(c_), int(d_)), 1)
                    except Exception:
                        pass

            # --- telegraphs, also on the floor ----------------------------------
            if g.b_state == "wind":
                warn_a = inv_clamp(g.b_t / float(max(1, g.b_len)), 0.0, 1.0)
                if g.b_move == "thrust":
                    rad = math.radians(math.degrees(math.atan2(
                        g.py - g.by, g.px - g.bx)))
                    a_, b_, _p = proj(g.bx, g.by)
                    c_, d_, _p2 = proj(g.bx + math.cos(rad) * 600,
                                    g.by + math.sin(rad) * 600)
                    try:
                        cv.line((255, 207, 92, int(120 + 110 * warn_a)),
                                (int(a_), int(b_)), (int(c_), int(d_)),
                                int(3 + 5 * warn_a))
                    except Exception:
                        pass
                elif g.b_move in ("sweep", "twirl"):
                    rad = math.radians(g.blade)
                    a_, b_, _p = proj(g.bx + math.cos(rad) * BIO_BLADE_INNER,
                                    g.by + math.sin(rad) * BIO_BLADE_INNER)
                    c_, d_, _p2 = proj(g.bx + math.cos(rad) * BIO_BLADE_OUTER,
                                    g.by + math.sin(rad) * BIO_BLADE_OUTER)
                    try:
                        cv.line((255, 207, 92, 150), (int(a_), int(b_)),
                                (int(c_), int(d_)), 2)
                    except Exception:
                        pass

            # --- THE SWEEP, IN TWO PARTS ----------------------------------------
            # 1. The FOOTPRINT on the boards. This is the hitbox and the only
            #    thing you actually have to read, so it is drawn on the floor
            #    where the collision really is.
            for i, ang in enumerate(g.blade_arc):
                a_al = int(130 * (1.0 - i / float(len(g.blade_arc) + 1)))
                arms = (ang,) if g.b_move == "sweep" else (ang, ang + 180.0)
                for arm in arms:
                    rad = math.radians(arm)
                    a_, b_, _p = proj(g.bx + math.cos(rad) * BIO_BLADE_INNER,
                                    g.by + math.sin(rad) * BIO_BLADE_INNER)
                    c_, d_, pp2 = proj(g.bx + math.cos(rad) * BIO_BLADE_OUTER,
                                    g.by + math.sin(rad) * BIO_BLADE_OUTER)
                    try:
                        cv.line((255, 60, 90, a_al), (int(a_), int(b_)),
                                (int(c_), int(d_)), max(2, int(7 * pp2)))
                    except Exception:
                        pass

            # 2. The BLADE ITSELF, riding at hand height above that footprint:
            #    a spectral pass of the glaive per arm, with after-images
            #    trailing back along the arc so a sweep is a sweep and not a
            #    line. Billboarded -- its on-screen angle is measured from the
            #    projected inner and outer points, because a blade pointing
            #    away from the camera has to foreshorten like everything else.
            if g.b_state == "act" and g.b_move in ("sweep", "twirl"):
                trail_angs = [g.blade] + list(g.blade_arc[:3])
                for fade, ang in enumerate(trail_angs):
                    arms = ((ang,) if g.b_move == "sweep"
                            else (ang, ang + 180.0))
                    for arm in arms:
                        rad = math.radians(arm)
                        ix, iy, ip = proj(
                            g.bx + math.cos(rad) * BIO_BLADE_INNER,
                            g.by + math.sin(rad) * BIO_BLADE_INNER)
                        ox, oy, op = proj(
                            g.bx + math.cos(rad) * BIO_BLADE_OUTER,
                            g.by + math.sin(rad) * BIO_BLADE_OUTER)
                        pmid = (ip + op) * 0.5
                        sang = math.degrees(math.atan2(oy - iy, ox - ix))
                        zb = self._zbucket(pmid * 1.2)
                        bucket = (int(round(sang / BIO_ROT_STEP))
                                % BIO_ROT_BUCKETS)
                        br, (bw2, bh2) = tex(("blade", bucket, zb, fade),
                                            self._blade_tf(sang, zb, fade),
                                            560, 560)
                        sblit(br, ((ix + ox) * 0.5 - bw2 * 0.5,
                                (iy + oy) * 0.5 - BIO_BLADE_LIFT * pmid
                                - bh2 * 0.5))

            # --- POISE, DRAWN ON THE BOARDS -------------------------------------
            # There is no bar for it and no word anywhere near the sprite. It is
            # an arc of light on the floor at its feet, teal because teal is the
            # player's colour in this fight -- so what the ring says is "this
            # much of it is yours", and it is read in the same glance as where
            # its feet are. A crowded label over the sprite would break rule 2
            # and would be read half a second later than this is.
            if not leaving and g.b_state != "buckle":
                pf = inv_clamp(g.poise_shown / g._poise_cap(), 0.0, 1.0)
                if pf < 0.999:
                    seg = 40
                    lit = int(seg * pf)
                    run = []
                    for k in range(seg + 1):
                        a2 = (k / float(seg)) * 6.2831853 - 1.5708
                        wx = g.bx + math.cos(a2) * 96.0
                        wy = g.by + math.sin(a2) * 96.0 * 0.72 + 14.0
                        pt = proj(wx, wy)
                        if k <= lit:
                            run.append((int(pt[0]), int(pt[1])))
                        elif len(run) > 1:
                            break
                    if len(run) > 1:
                        low = pf < 0.30
                        a_ = 175 + int(80 * (1.0 - pf))
                        col = ((255, 210, 120, min(255, a_)) if low
                            else (92, 232, 208, min(255, a_)))
                        try:
                            cv.lines(col, False, run, 5 if low else 4)
                        except Exception:
                            pass

            # --- everything that STANDS on the floor, sorted far to near --------
            draw = []

            for h in g.hazards:
                if h["kind"] in ("copy", "orbit"):
                    draw.append((h["y"], "copy", h))
                elif h["kind"] == "note":
                    draw.append((h["y"], "note", h))
            for d in g.daggers:
                if d["state"] == "flight":
                    draw.append((d["y"], "dagger", d))
                elif d["state"] == "ground":
                    draw.append((d["y"], "grounded", d))
            for d in g.debris:
                draw.append((d["y"], "debris", d))
            draw.append((g.by, "boss", None))
            draw.append((g.py, "player", None))
            draw.sort(key=lambda e: e[0])

            def contact(wx, wy, radius, alpha):
                """A shadow on the boards. Ellipse, because a circle on the
                floor is one -- wider than it is tall, and both scaled by how
                far away the floor is at that depth."""
                cxp, cyp, pp = proj(wx, wy)
                rw = max(3, int(radius * pp))
                rh = max(2, int(radius * pp * 0.34))
                try:
                    cv.ellipse((0, 0, 0, int(alpha * 255)),
                            (int(cxp - rw), int(cyp - rh), rw * 2, rh * 2), 0)
                except Exception:
                    pass

            # Shadows go down before any body does, so every figure is drawn
            # standing on its own.
            contact(g.bx, g.by, 96.0, 0.42)
            contact(g.px, g.py, 26.0, 0.38)
            for h in g.hazards:
                if h["kind"] in ("copy", "orbit"):
                    contact(h["x"], h["y"], 34.0, 0.26)
            for d in g.daggers:
                if d["state"] == "ground":
                    contact(d["x"], d["y"], 15.0, 0.30)

            for _wy, kind, item in draw:
                if kind == "debris":
                    # Suspended matter, standing off the boards at its own
                    # height. It gets brighter and bigger as it comes downstage
                    # and simply blows past the lens -- which is the cue that
                    # does most of the work of making the room a volume.
                    dxp, dyp, pp = proj_h(item["x"], item["y"], item["h"])
                    if not (-90 < dxp < 1370 and -90 < dyp < 810):
                        continue
                    size = max(1, int(item["s"] * pp
                                    * (0.55 + 0.45 * item["w"])))
                    # THE FLOOR GOES ON THE FINAL VALUE. qa() quantizes to
                    # eight levels, so anything under ~0.143 collapses to
                    # 6/255 and is simply not there -- multiplying a fade into
                    # a fade is how a whole particle layer goes invisible.
                    a = inv_clamp((0.10 + 0.40 * pp) * item["w"]
                                * (0.7 + 0.3 * math.sin(g.clock * 1.7
                                                        + item["p"])),
                                0.16, 0.62)
                    col = "#ffb9c6" if g.corrupt > 0.5 else "#dfe9ff"
                    rv.blit(rect(col + qa(a), size, size),
                            (int(dxp) - size // 2, int(dyp) - size // 2))
                    # The close ones smear, because at that size and speed they
                    # would.
                    if pp > 0.86 and size > 4:
                        streak = max(2, int(abs(item["vy"]) * 7.0 * pp))
                        rv.blit(rect(col + qa(a * 0.45), max(1, size // 2),
                                    streak),
                                (int(dxp) - size // 4,
                                int(dyp) - size // 2 - streak))

                elif kind == "grounded":
                    # A dagger lying where it came to rest: half-buried, small,
                    # and ringed so it can be found across a loud floor. This
                    # is the ammunition, and it is over there.
                    gx_, gy_, pp = proj(item["x"], item["y"])
                    puls = 0.5 + 0.5 * math.sin(g.clock * 3.2
                                                + item["x"] * 0.03)
                    rr = int(max(4, (13 + 5 * puls) * pp))
                    try:
                        cv.ellipse((92, 232, 208,
                                    int(70 + 60 * puls)),
                                (int(gx_ - rr), int(gy_ - rr * 0.4),
                                    rr * 2, max(2, int(rr * 0.8))), 1)
                    except Exception:
                        pass
                    zb = self._zbucket(pp * 0.8)
                    dr, (dw, dh) = tex(("dag",
                                        int(round(-58.0 / BIO_ROT_STEP))
                                        % BIO_ROT_BUCKETS, zb),
                                    self._dagger_tf(-58.0, zb), 140, 140)
                    sblit(dr, (gx_ - dw * 0.5, gy_ - dh * 0.5 - 9 * pp))

                elif kind == "copy":
                    cx_, cy_, pp = proj(item["x"], item["y"])
                    zb = self._zbucket(pp)
                    cr, (cw2, ch2) = tex(("copy",
                                        int(round(item["spin"] / BIO_ROT_STEP))
                                        % BIO_ROT_BUCKETS, zb),
                                        self._copy_tf(item["spin"], zb),
                                        520, 520)
                    sblit(cr, (cx_ - cw2 * 0.5, cy_ - ch2 * 0.5 - 30 * pp))

                elif kind == "note":
                    nx, ny, pp = proj(item["x"], item["y"])
                    sz = max(4, int(10 * pp))
                    rv.blit(rect(BIO_WARN + qa(0.85), sz, sz),
                            (int(nx) - sz // 2, int(ny) - sz // 2))
                    rv.blit(rect(BIO_RED + qa(0.45), int(sz * 1.8), 2),
                            (int(nx) - sz, int(ny)))

                elif kind == "dagger":
                    dx_, dy_, pp = proj(item["x"], item["y"])
                    zb = self._zbucket(pp)
                    dr, (dw, dh) = tex(("dag",
                                        int(round(item["ang"] / BIO_ROT_STEP))
                                        % BIO_ROT_BUCKETS, zb),
                                    self._dagger_tf(item["ang"], zb), 140, 140)
                    sblit(dr, (dx_ - dw * 0.5, dy_ - dh * 0.5 - 18 * pp))

                elif kind == "boss":
                    bx_, by_, pp = proj(g.bx, g.by)
                    zoom = BIO_BOSS_ZOOM_ACT2 * (0.55 + 0.45 * pp)
                    tint = ("#ffffff" if g.hit_flash > 0.4
                            else ("#ffb0c0" if exposed else None))
                    # Afterimages first, so the live body sits on top of them.
                    for i, (gx, gy, grot, gsc) in enumerate(g.ghosts):
                        a = 0.20 * (1.0 - i / float(len(g.ghosts) + 1))
                        ggx, ggy, gpp = proj(gx, gy)
                        gz = BIO_BOSS_ZOOM_ACT2 * (0.55 + 0.45 * gpp)
                        gr, (gw, gh) = tex(("ghost", round(gz, 3), i),
                                        self._body_plain(gz, alpha=a,
                                                        tint="#ff6a7e"),
                                        900, 900)
                        sblit(gr, (ggx - gw * 0.5, ggy - gh))
                    body_h = BIO_SPRITE_H * zoom
                    self._draw_body(g, rv, tex, sblit, bx_,
                                    by_ - body_h * 0.5, zoom, 0, 0, st, at,
                                    warp=(0.85 if not g.last_page else 1.25),
                                    rot=inv_clamp(
                                        math.sin(math.radians(g.body_rot)) * 11.0,
                                        -11.0, 11.0),
                                    stretch=(getattr(g, "body_sx", 1.0),
                                            getattr(g, "body_sy", 1.0)),
                                    diss=(g.emerge if leaving else 0.0),
                                    hurt=0.9 if g.hit_flash > 0.45 else 0.0)

                elif kind == "player":
                    px_, py_, pp = proj(g.px, g.py)
                    for i, (tx, ty, dashing) in enumerate(g.trail):
                        if i == 0:
                            continue
                        a = 0.30 * (1.0 - i / float(len(g.trail)))
                        if dashing:
                            a *= 1.8
                        ttx, tty, tpp = proj(tx, ty)
                        size = max(2, int((11 - i) * tpp))
                        rv.blit(rect("#ff4a5e" + qa(a), size, size),
                                (int(ttx) - size // 2, int(tty) - size // 2))
                    blink = (g.iframe > 0 and (g.tick // 3) % 2 == 0)
                    if not blink:
                        self._draw_heart(g, rv, tex, sblit, px_,
                                        py_ - 26 * pp, 0, 0, st, at,
                                        scale=pp)

            # --- OCCLUSION. Depth sorting means standing upstage of it puts
            # its body between you and the camera, and losing your own avatar
            # behind the boss is not a difficulty, it is a defect. If it is in
            # front of you and overlapping, a ghost of the heart is drawn on
            # top so your position is never in question.
            if g.py < g.by:
                pxs, pys, ppp = proj(g.px, g.py)
                bxs, bys, bpp = proj(g.bx, g.by)
                body_w = BIO_SPRITE_W * BIO_BOSS_ZOOM_ACT2 * (0.55 + 0.45 * bpp)
                body_h = BIO_SPRITE_H * BIO_BOSS_ZOOM_ACT2 * (0.55 + 0.45 * bpp)
                if (abs(pxs - bxs) < body_w * 0.42
                        and bys - body_h < pys < bys + 40):
                    ghost = self._misc(("occl",), lambda: Transform(
                        Solid(BIO_TEAL), xysize=(13, 13), rotate=45,
                        alpha=0.85, subpixel=True))
                    gr2, (gw2, gh2) = tex(("occl",), ghost, 60, 60)
                    sblit(gr2, (pxs - gw2 * 0.5,
                                pys - 26 * ppp - gh2 * 0.5))

            # --- DISCHARGE. Drawn over the figures on purpose: a bolt is light,
            # and light does not queue behind the thing it is lighting. The art
            # is the four lightning arcs from the shared atlas
            # (asset_definitions/def_bullets.rpy); the frame is CYCLED per tick so a
            # bolt crackles instead of sitting there.
            for a_ in g.arcs:
                a_age = g.tick - a_["born"]
                if a_age < 0 or a_age >= a_["ttl"]:
                    continue
                axp, ayp, app_ = proj_h(a_["x"], a_["y"], a_["h"])
                if not (-260 < axp < 1540 and -160 < ayp < 880):
                    continue
                # Bolts snap on bright and drop off fast -- the decay is what
                # makes it read as a discharge and not a ribbon.
                a_fr = 1.0 - (a_age / float(a_["ttl"]))
                a_al = 0.45 + 0.55 * a_fr
                # Everything the cache keys on is an int. Thickness is derived
                # from LENGTH rather than set independently, because the art is
                # a 252x32 jagged bolt -- squash that ratio and the jaggedness
                # flattens into a smooth bar, which is the one thing lightning
                # must not look like.
                a_len = max(40, int(a_["len"] * app_))
                a_th = max(6, int(a_len * 0.15 * a_["w"]))
                a_bkt = int(math.degrees(a_["ang"]) / 12.0) % 30
                a_frame = EMB_ARCS[(a_["seed"] + a_age // 2) % len(EMB_ARCS)]
                a_aq = int(a_al * 5.999)
                a_key = ("bioarc", a_frame, a_len // 12, a_th, a_bkt, a_aq)
                arc_d = self._misc(a_key, (lambda nm=a_frame, L=a_len, T=a_th,
                                            bk=a_bkt, aq=a_aq: Transform(
                    emb_cell(nm),
                    xzoom=L / float(emb_size(nm)[0]),
                    yzoom=T / float(emb_size(nm)[1]),
                    rotate=bk * 12.0, subpixel=True,
                    matrixcolor=TintMatrix(BIO_TEAL),
                    alpha=(aq + 0.5) / 6.0)))
                try:
                    a_quad = a_len + a_th + 24
                    arr_, (arw_, arh_) = tex(a_key, arc_d, a_quad, a_quad)
                    sblit(arr_, (axp - arw_ * 0.5, ayp - arh_ * 0.5))
                except Exception:
                    pass

            if exposed:
                bx_, by_, pp = proj(g.bx, g.by)
                pulse = 0.5 + 0.5 * math.sin(g.tick * 0.45)
                blit_text("OVER-EXTENDED", 15,
                        BIO_WARN + qa(0.55 + 0.45 * pulse),
                        int(bx_), int(by_ - BIO_SPRITE_H * BIO_BOSS_ZOOM_ACT2
                                    * (0.55 + 0.45 * pp)) - 26,
                        bold=True, anchor=(0.5, 0.0), w=340, h=34)

            # --- HUD: as little as will still do the job --------------------------
            bar_w = 620
            bx0 = 640 - bar_w // 2
            rv.blit(rect("#04030ac8", bar_w + 4, 32), (bx0 - 2, 28))
            rv.blit(rect(BIO_RED_DEEP, bar_w, 10), (bx0, 30))
            fill = int(bar_w * inv_clamp(g.boss_shown / float(BIO_BOSS_HP_MAX),
                                        0.0, 1.0))
            if fill > 0:
                rv.blit(rect(BIO_RED, fill, 10), (bx0, 30))

            # POISE, DIRECTLY UNDER ITS HEALTH, in the player's colour. The
            # arc on the boards says where; this says how much, and it is the
            # bar you are actually playing against between buckles. Without it
            # the loop has no visible progress at all -- the whole reason the
            # daggers read as doing nothing.
            pf = inv_clamp(g.poise_shown / g._poise_cap(), 0.0, 1.0)
            rv.blit(rect("#0d1a1a", bar_w, 6), (bx0, 42))
            if g.b_state == "buckle":
                # Broken: it drains away and stays empty for the window.
                flick = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(g.tick * 0.9))
                rv.blit(rect(BIO_WARN + qa(flick), bar_w, 6), (bx0, 42))
            else:
                pfill = int(bar_w * pf)
                if pfill > 0:
                    rv.blit(rect(BIO_TEAL if pf > 0.30 else BIO_WARN,
                                pfill, 6), (bx0, 42))

            # THE ENTRY, under both, because it is the third way this ends and
            # the only one that is not yours.
            ef = inv_clamp(g.entry_shown / BIO_ENTRY_MAX, 0.0, 1.0)
            rv.blit(rect("#1b1420", bar_w, 4), (bx0, 52))
            efill = int(bar_w * ef)
            if efill > 0:
                hot = ef > 0.72
                ecol = BIO_WARN if not hot else (
                    "#ffffff" if (g.tick // 8) % 2 == 0 else BIO_WARN)
                rv.blit(rect(ecol, efill, 4), (bx0, 52))
            blit_text("BIOGRAPHY", 13, BIO_RED, bx0, 10, bold=True, w=300, h=26)
            blit_text("ENTRY", 10, BIO_WARN + qa(0.30 + 0.55 * ef),
                    bx0 + bar_w + 8, 50, anchor=(0.0, 0.0), w=140, h=22)
            if exposed:
                pulse = 0.5 + 0.5 * math.sin(g.tick * 0.4)
                blit_text("EXPOSED", 13, BIO_WARN + qa(0.4 + 0.6 * pulse),
                        bx0 + bar_w, 10, bold=True, anchor=(1.0, 0.0), w=220, h=26)

            hud = (24, 620, 300, 76)
            self._panel(rv, rect, hud, 0, 0)
            self._odometer(g, rv, tex, rect, qa, blit_text, "HP", g.hp_shown,
                        g.hp, hud[0] + 16, hud[1] + 16, BIO_INK)

            # Dash charge, because it is the only defence there is.
            px0, py0 = 344, 654
            blit_text("DASH", 11, BIO_FAINT, px0, py0 - 16, w=90, h=22)
            pw = 150
            rv.blit(rect("#0a0812c8", pw, 8), (px0, py0))
            if g.dashing:
                frac = 1.0 - (g.dash_t / float(BIO_DASH_MAX))
                col = BIO_INK
            elif g.dash_cd > 0:
                frac = 1.0 - (g.dash_cd / float(BIO_DASH_CD))
                col = "#2f7d72"
            else:
                frac = 1.0
                col = BIO_TEAL
            rv.blit(rect(col, max(0, int(pw * frac)), 8), (px0, py0))

            # THE FOUR DAGGERS, as four pips: filled if it is in your hand,
            # hollow if it is out there somewhere. No count, no word -- the
            # thing you need to know is how many are left, and four shapes say
            # that faster than a number does.
            qx0, qy0 = 344, 616
            for i, d in enumerate(g.daggers):
                x_ = qx0 + i * 17
                if d["state"] == "held":
                    rv.blit(rect(BIO_TEAL, 9, 14), (x_, qy0))
                else:
                    flying = d["state"] == "flight"
                    a = 0.62 if flying else 0.34
                    rv.blit(rect(BIO_TEAL + qa(a), 9, 1), (x_, qy0))
                    rv.blit(rect(BIO_TEAL + qa(a), 9, 1), (x_, qy0 + 13))
                    rv.blit(rect(BIO_TEAL + qa(a), 1, 14), (x_, qy0))
                    rv.blit(rect(BIO_TEAL + qa(a), 1, 14), (x_ + 8, qy0))

            blit_text("MOVE  WASD      Z  THROW      X  DASH  (HOLD)", 12,
                    BIO_FAINT, 1256, 690, anchor=(1.0, 1.0), w=760, h=28)
            if g.god:
                blit_text("GOD", 12, BIO_WARN + "aa", 1256, 664,
                        anchor=(1.0, 1.0), w=120, h=24)


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

label archivist_invasion_biography:
    $ bio_deaths = 0
    $ bio_retry = False

label inv_biography_fight:
    $ renpy.block_rollback()

    $ bio_game = BIOGame(retry=bio_retry, deaths=bio_deaths,
                        debug=config.developer, start_open=inv_dev_start_open)

    $ _bio_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ _bio_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None
    scene black

    call screen inv_biography_screen(bio_game)
    $ _bio_result = _return

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

    menu:
        "AGAIN":
            scene black
            jump inv_biography_fight

        "STOP":
            if inv_dev_test:
                $ renpy.notify("BIOGRAPHY: lost. Recorded.")
            return

label inv_biography_quit:
    $ bio_retry = True
    if inv_dev_test:
        $ renpy.notify("BIOGRAPHY: withdrawn.")
    return
