# =============================================================================
# ARCHIVIST INVASION 02 -- HORROR
# =============================================================================
#
# WHAT THIS IS
#   The second Archivist Invasion. Same two-act shape as Biography, built out
#   of the opposite materials: where Biography is a thing that wants to finish
#   something, Horror is a thing that wants to be near you.
#
#   ACT ONE -- the room. Turn-based, EarthBound furniture, same odometer. But
#   the kit is inverted: YOU CANNOT HURT IT WITH YOUR HANDS. The lantern is
#   the only thing it flinches from, and light costs NERVE. The real number on
#   screen is not its health, it is DREAD -- how close it is standing. Dread
#   climbs every single turn and light is the only thing that pushes it back.
#
#   ACT TWO -- the CORRUPTIVE STATE: a chase. There is nothing to attack, no
#   invulnerability to dodge behind, and no boss health bar. You run, it
#   follows, and the only win condition in the entire fight is DISTANCE.
#
#   THE CORRIDOR COMES TO THE BOIL (rebuilt Aug 11 2026). The first version of
#   this act read as EMPTY rather than claustrophobic, and the reason was
#   structural rather than decorative: the corridor was a fixed 920px slot
#   with two thin wriggling lines at the sides of it, and nothing about the
#   SPACE ever got worse -- only the spawn rate did. A corridor with nothing
#   at its edges is a field. So:
#     * THE WALLS CLOSE, continuously, 920px down to 496px across the run,
#       and they are solid mass now with the wriggle on their inner face.
#       Slowly enough that no single moment announces it -- you are meant to
#       notice you are cornered, not watch it happen.
#     * FOUR RUNGS (HOR_PHASE_AT), each adding a KIND of thing rather than
#       more of the same, each announcing itself once with a jolt and never
#       again: the corridor / the walls start reaching in / something
#       enormous is out there / it is close enough to be constant.
#     * WALL REACHERS grow inward off the edges and are drawn joined to the
#       wall they came from, so the corridor itself becomes the hazard.
#     * SOMETHING ENORMOUS goes past outside the walls, three or four times a
#       run. It cannot touch you and it has no mechanics at all. Its entire
#       job is scale -- a chase you can win is frightening; a chase you can
#       win while something the size of the sky goes by is a different
#       feeling, and it costs nothing.
#
#   THE CORRIDOR GETS A KIT AND A CEILING (Aug 14 2026). Two complaints, one
#   root: "a heart running down an empty corridor avoiding boxes", and a
#   runner who could drift vertically off the collision plane and then be hit
#   by a mass drawn well below them. Both are fixed by taking the vertical
#   axis away from steering and spending it on something worth having:
#
#     * THE PLANE. The runner is pinned to HOR_PLANE_Y for good. Collision
#       fires on the frame an obstacle's DEPTH crosses that plane and tests x
#       only -- so anything that lets the avatar leave the plane is a promise
#       the hit test does not keep, and it read exactly as advertised: a
#       collision with an invisible surface above the actual box.
#     * THE LANTERN COMES BACK, on the freed keys, INVERTED by the genre
#       shift. In act one light pushes it away and costs nerve; in the chase
#       light SHOWS IT WHERE YOU ARE -- it closes faster the whole time you
#       are lit -- and the tank never refills. See the block above
#       HOR_POWER_MAX.
#     * THE WATCHERS, and they are a cheap trick on purpose. A thing set into
#       the corridor wall that advances in hard discrete steps whenever
#       nobody is shining a light on it, and holds perfectly still otherwise.
#       The lantern is the only answer and the answer is DIRECTIONAL: it only
#       drives back a watcher on the side of the corridor you are standing
#       on, so answering one means crossing toward it. A bite does not make
#       it go away -- it drops back to the far end of the wall and starts
#       again, so ignoring one is not a tax you pay once. See HOR_WATCH_*.
#       The half of the corridor it can be answered from is bracketed on the
#       floor and headed with act one's own command word, which stops
#       printing the moment the player drives one back for the first time.
#     * STRUCTURE. Struts hooping the tunnel, rails running away to the
#       vanishing point, masses growing off the walls, and pairs of points in
#       them that open as they go past. No mechanics, no hitboxes, and no
#       colour -- the act is meant to stay shrill, it was just meant to stay
#       shrill somewhere rather than nowhere. See HOR_STRUCT_PHASE.
#
# THE JOINT BETWEEN THE ACTS (the thing that makes act one matter)
#   How close it is when the room turns is exactly how much head start you get.
#   Dread at the shift sets the chase's opening gap. Playing act one badly does
#   not cost you health -- health is handed back -- it costs you the only
#   currency act two spends.
#
# THE KIT: A PSYCHIC TYPE IS WEAK TO GHOST, DARK AND BUG
#   Horror is a psychic type, and those three weaknesses are themselves FEARS.
#   So there is no sword in this fight -- the only things that touch it are
#   the three things that frighten it, and each answers one aspect it wears:
#
#       PRESENCE  it is HERE, solid, close        -> GHOST  stop being there
#       GAZE      it is looking at you            -> DARK   put the light out
#       PATTERN   it is exact, ordered, endless   -> BUG    introduce a fault
#
#   Act one is therefore not a damage race, it is a READING. The aspect is
#   printed in the middle of the room every turn -- AND THE READOUT LIES, more
#   often the closer it gets. The only tell is that a lying word flickers.
#   Catching a lie never tells you the right answer, it only takes one of the
#   three off the table, which is the difference between a puzzle and a fear.
#
#   And in act two it spends all three back on you: GHOST is a phantom of it
#   standing ahead of you (impossible), DARK puts the light out mid-run, BUG
#   faults the encounter itself. None of the three can kill you. Each one
#   costs you the thing that can.
#
# THE THREE HORRORS, ONE ENCOUNTER
#   UNCANNY -- it does things a pursuer should not. It stands still and
#     nothing happens (`still`, the only turn in this project that prints no
#     number). It copies the move you just made and uses it (`mimic`). The
#     room misreports what it is. In the chase it appears AHEAD of you, which
#     is impossible, and it is not real, and it still scrambles your hands.
#   PSYCHOLOGICAL -- nerve is a resource and running out of it takes your
#     commands away from you for a turn (PANIC). Wind is the same bargain:
#     the greedy runner empties the tank and gets WINDED, which is slower
#     than walking. And LOOK BACK is the biggest bargain in the encounter --
#     see the block above HOR_LOOK_TURN, it is the centrepiece of act two.
#   THRILLING -- it lunges. Telegraphed, survivable, and it will take every
#     scrap of wind you were saving.
#
# THE RULES (from the invasion spec -- restated because they bind here too)
#   1. NO FLAVOR TEXT. Controls, numbers and state words only.
#   2. NOTHING MAY BE FUNNY.
#   3. IT MOVES LIKE SOMETHING THAT HAS SEEN A DIAGRAM. Drawn through
#      inv.flesh, same as every Archivist.
#   4. IT ARRIVES AND LEAVES THROUGH A HOLE.
#   5. BEATABLE. The chase is brutal ON PURPOSE, but the maths has to close:
#      see the BALANCE block below, which is the proof that it can be outrun.
#
# BALANCE, WRITTEN OUT (change one number here and re-check the others)
#   Your walk is 1.00 and its speed starts at 1.20, so walking loses from the
#   first frame -- modelled, a walked run is caught at ~71% of the distance.
#   Your sprint is 1.80 and wind funds roughly a 54% duty cycle. Modelled
#   outcomes at these numbers:
#       clean running, wind released early  -> escapes, gap bottoms out ~60
#       one stumble every 6s                -> escapes, gap bottoms out ~24
#       one stumble every 4s                -> CAUGHT at ~76%
#       greedy (sprints to empty, winded)   -> escapes at a gap of 9
#       walked the whole way                -> CAUGHT at ~71%
#   The slack that makes it winnable is NEAR MISSES: threading close to an
#   obstacle without touching it refunds wind, so a runner who weaves buys a
#   higher duty cycle than one who plays safe. That is the whole skill curve.
#   Retune HOR_THEIR_SPEED and every one of those outcomes moves.
#
#   WHAT THE LANTERN COSTS, ARITHMETICALLY. A full tank is 770 lit ticks
#   (HOR_POWER_MAX / HOR_POWER_DRAIN) and being lit adds HOR_LAMP_SEEN to its
#   speed, so spending the entire tank costs 770 * 0.40 * HOR_GAP_K = ~17 gap
#   across the whole run, against an opening gap of 30-80 and a sprint that
#   buys 0.033/tick back. It is a real price and it is a payable one. The
#   watchers are what it is FOR: driving one off from stage 0 is 70 lit ticks
#   (9 power), from stage 2 it is 210 (27), and from stage 3 you cannot
#   finish before it arrives -- you can only push it back to 2 and start
#   again. Deal with them early is the whole lesson, and the maths says it
#   rather than a caption.
#
#   RE-MEASURED AFTER THE Aug 14 NERF (6 seeded runs a line). `slop` is how
#   late the bot reacts -- 0.22 is a competent pilot, 0.42 is someone not
#   really looking, and the bot is pessimistic against a human either way
#   because it only starts moving at a fixed depth while a player can move
#   the moment the outline lights:
#       clean, answers the watchers   6/6, 70-73s, gap floor 45 (its opening
#                                     value -- it never loses ground at all)
#       slop 0.22                     6/6, 71-74s, gap floor 45
#       slop 0.32                     2/6, ~21 stumbles
#       slop 0.42                     0/6, ~20 stumbles
#       never raises the lantern      5/6, 75-78s, gap floor 2-32, 4-5 bites
#       holds the lantern down        0/3, dead at 47-51s with an empty tank
#   READ THE FLOOR, NOT THE WIN COUNT -- the same reading LOOK BACK was tuned
#   on. The lantern is not required to finish (5/6 without it) and it is the
#   difference between a safety margin of 45 and one of 2: it does not win
#   you the chase, it wins you room. And the last line is why the tank exists
#   -- a light you can simply leave on is not a bargain.
#
#   WHAT THE NERF ACTUALLY WAS, because the obvious lever was wrong twice.
#   "Nigh-impossible" was NOT the chase being fast: a sloppy bot died at HP 0
#   with sixteen stumbles and a gap that had never once been in danger. The
#   chase was being lost by BLEEDING OUT, silently, on a bar nobody watches
#   during a chase. And slowing the pursuer down to compensate pinned the
#   clean bot's gap at the ceiling for a whole run, which is not an easier
#   chase, it is no chase. So the speeds went nearly back to where they were
#   and the fix landed on the bleed (HOR_STUMBLE_HP 18->12, HOR_GAP_STUMBLE
#   6.0->3.5, and HOR_HP_NEARMISS, a mend on the skill the act already asks
#   for) and on the dice (HOR_SPAWN_CLEAR_FRAC, HOR_LANE_NEAR, HOR_REACH_W,
#   HOR_MIN_WARN, all widened). Measure the thing that is actually killing
#   people before touching the thing that looks like it is.
#
#   LOOK BACK, MEASURED (6 seeded runs each, bots -- so a floor, not a human):
#       never looks back    6/6, 64-69s, gap bottoming out at  9-45
#       stares and releases 5/6, 63-67s, gap bottoming out at 21-41
#       stares until taken  0/6, dead in 9-13s
#   Read the MIDDLE column, not the first: the win counts are inside seed
#   noise at this sample size, but the safety FLOOR more than doubles. A
#   runner who takes the bargain is not finishing faster, they are finishing
#   with room to spare -- which is the whole promise of the mechanic. And it
#   is never REQUIRED: a runner who refuses it still gets out.
#   At the first set of numbers the stare bot won 4/6 against the refuser's
#   5/6 -- i.e. the bargain cost more than it paid, which is worse than not
#   having it, because the game was then inviting the player to lose.
#
# ARCHITECTURE
#   Same as every invasion: HORGame owns the simulation, HORStage is one CDD
#   stepping it at a fixed 60Hz inside render(). Two shaders of its own --
#   inv.pall (act one: the soup with the colour drained out of it) and
#   inv.dark (the chase: near-black, wriggling, breathing). The body shader
#   and the padded plate come from invasions.rpy.
#
# READ THIS FIRST IF YOU ARE LOST
#   HORGame.step() dispatches on self.mode:
#     arrive   the rupture; it comes through and does not hurry
#     menu     act one commands
#     beat     the one-line readout; WAITS for a key, never auto-advances
#     enemy    its turn
#     shift    the corruptive tear
#     run      the chase
#     leave_w  you got away / leave_l  it reached you
# =============================================================================

# --- SHADERS -----------------------------------------------------------------
init -9 python:
    HOR_PALL_OK = False
    HOR_DARK_OK = False
    HOR_WITHER_OK = False

    def _hor_register_shaders():
        # ACT ONE. The same hyperspace plate every invasion is fought over,
        # with the colour pulled out of it and something standing in it. Dread
        # does not tint the room -- it DARKENS it, closing the vignette and
        # thickening a slow crawl over everything, so the room gets smaller as
        # it gets nearer without ever announcing itself.
        renpy.register_shader("inv.pall", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_hor_res;
            uniform float u_hor_time;
            uniform float u_hor_dread;
            uniform float u_hor_pulse;
            uniform float u_hor_flash;
            uniform float u_hor_dark;
            uniform float u_hor_spin;
            uniform vec4 u_hor_hole;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float hor_hash(vec2 p) {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
            }
            float hor_noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                f = f * f * (3.0 - 2.0 * f);
                float a = hor_hash(i);
                float b = hor_hash(i + vec2(1.0, 0.0));
                float c = hor_hash(i + vec2(0.0, 1.0));
                float d = hor_hash(i + vec2(1.0, 1.0));
                return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
            }
            float hor_fbm(vec2 p) {
                float v = 0.0;
                float a = 0.5;
                for (int i = 0; i < 4; i++) {
                    v += a * hor_noise(p);
                    p = p * 2.03 + vec2(17.3, 9.1);
                    a *= 0.5;
                }
                return v;
            }
            vec2 hor_mirror(vec2 p) {
                return abs(fract(p * 0.5) * 2.0 - 1.0);
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            float t = u_hor_time;
            float dread = clamp(u_hor_dread, 0.0, 1.0);

            vec2 c = uv - 0.5;

            // The wormhole it comes through, same instrument as every arrival.
            vec2 hp = (u_hor_hole.xy / max(u_hor_res, vec2(1.0))) - 0.5;
            float hr = max(u_hor_hole.z, 1.0) / max(u_hor_res.x, 1.0);
            float hs = clamp(u_hor_hole.w, 0.0, 1.0);
            vec2 hv = c - hp;
            float hd = length(hv);
            float hinf = (1.0 - smoothstep(0.0, hr, hd)) * hs;
            if (hinf > 0.001) {
                float ha = hinf * hinf * 4.6 + t * 0.4 * hinf;
                float ccs = cos(ha);
                float csn = sin(ha);
                hv = vec2(hv.x * ccs - hv.y * csn, hv.x * csn + hv.y * ccs);
                c = hp + hv * (1.0 - 0.62 * hinf);
            }

            // Rotational momentum, but sluggish -- this room turns like
            // something too big to be turning.
            vec2 pivot = vec2(sin(t * 0.09) * 0.05, cos(t * 0.11) * 0.04);
            vec2 rc = c - pivot;
            float rr = length(rc);
            float twist = u_hor_spin + sin(t * 0.13) * 0.75 * rr;
            float tcs = cos(twist);
            float tsn = sin(twist);
            c = pivot + vec2(rc.x * tcs - rc.y * tsn, rc.x * tsn + rc.y * tcs);

            float r = length(c);
            c *= 1.0 + (sin(t * 0.23) * 0.03) * r * r;

            vec2 w1 = vec2(hor_fbm(c * 2.6 + vec2(t * 0.09, -t * 0.07)),
                        hor_fbm(c * 2.6 + vec2(4.1 - t * 0.06, 8.3 + t * 0.05)));
            vec2 sp = c + (w1 - 0.5) * (0.06 + 0.05 * dread);
            vec3 src = texture2D(tex0, hor_mirror(sp + 0.5)).rgb;

            // Drained. What is left is a wet grey-green, and dread takes even
            // that away.
            float lum = dot(src, vec3(0.299, 0.587, 0.114));
            vec3 col = mix(vec3(lum * 0.72, lum * 0.86, lum * 0.74),
                        vec3(lum * 0.30, lum * 0.34, lum * 0.31), dread);
            col *= 0.42 - 0.16 * dread;

            // Something moving under the surface, slowly, never resolving.
            float crawl = hor_fbm(c * 6.0 + vec2(-t * 0.05, t * 0.04));
            col += vec3(0.06, 0.09, 0.07) * smoothstep(0.55, 0.95, crawl)
                * (0.5 + 1.4 * dread);

            // A single slow breath, the room's, not yours.
            col *= 1.0 + 0.05 * sin(t * 0.9) * (0.4 + dread);
            col += vec3(0.05, 0.02, 0.03) * u_hor_pulse * dread;

            if (hs > 0.001) {
                float core = 1.0 - smoothstep(hr * 0.12, hr * 0.52, hd);
                col *= mix(1.0, 0.02, core * hs);
                float lip = 1.0 - smoothstep(0.0, hr * 0.16, abs(hd - hr * 0.52));
                col += vec3(0.42, 0.46, 0.40) * lip * hs * 1.15;
            }

            float vig = 1.0 - r * r * (1.35 + 1.55 * dread);
            col *= max(vig, 0.0);
            col = mix(col, vec3(0.86, 0.88, 0.84), clamp(u_hor_flash, 0.0, 1.0));
            col *= 1.0 - clamp(u_hor_dark, 0.0, 1.0);
            gl_FragColor = vec4(col, 1.0);
        """)

        # ACT TWO. NOT a black screen -- a hyperspace you are being driven
        # down. The plate is remapped into a TUNNEL (polar around a vanishing
        # point, radius inverted into depth) so the whole room rushes past you
        # and there is somewhere to be running TO. It is kept dark by
        # exposure, not by deletion: the spectacle is all there, drowned.
        #
        # Over that: filaments streaming past to sell speed, a wriggle that
        # never settles, arcs of far-off light, a heartbeat that squeezes the
        # frame, and a pressure closing from the edges keyed to exactly one
        # thing -- u_hor_near, 0 = it is nowhere, 1 = it is on you.
        renpy.register_shader("inv.dark", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_hor_res;
            uniform float u_hor_time;
            uniform float u_hor_scroll;
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
            uniform float u_hor_lamp;
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
                for (int i = 0; i < 4; i++) {
                    v += a * dk_noise(p);
                    p = p * 2.11 + vec2(11.7, 5.3);
                    a *= 0.5;
                }
                return v;
            }
        """, fragment_300="""
            const float DK_TAU = 6.2831853;
            vec2 uv = v_tex_coord;
            float t = u_hor_time;
            float near = clamp(u_hor_near, 0.0, 1.0);
            float beat = clamp(u_hor_beat, 0.0, 1.0);
            float blind = clamp(u_hor_blind, 0.0, 1.0);
            float glitch = clamp(u_hor_glitch, 0.0, 1.0);
            float look = clamp(u_hor_look, 0.0, 1.0);
            float vast = clamp(u_hor_vast, 0.0, 1.0);
            float close = clamp(u_hor_close, 0.0, 1.0);
            float lamp = clamp(u_hor_lamp, 0.0, 1.0);

            vec2 c = uv - vec2(0.5, 0.46);
            c.x *= u_hor_res.x / max(u_hor_res.y, 1.0);

            // The heartbeat squeezes the frame itself.
            c *= 1.0 - 0.045 * beat * (0.5 + near);
            c.x += u_hor_lurch * 0.05 * sin(uv.y * 26.0 + t * 9.0);
            // A bug tears rows sideways.
            float grow = floor(uv.y * 110.0);
            c.x += (dk_hash(vec2(grow, floor(t * 20.0))) - 0.5) * 0.16 * glitch;

            float r = max(length(c), 0.0007);
            float ang = atan(c.y, c.x);

            // THE TUNNEL. Radius inverted into depth, angle into the wrap, so
            // the plate becomes a throat you are being pulled down.
            // TURNING ROUND REVERSES THE WORLD. Everything that was rushing
            // at you is now rushing away from you, which is the cheapest and
            // by far the most convincing way to say "you are facing the other
            // direction" without building a second camera.
            float depth = 0.34 / r + u_hor_scroll * 1.15 * (1.0 - 2.0 * look);
            vec2 tuv = vec2(ang / DK_TAU * 2.0 + sin(depth * 0.25) * 0.05,
                            depth * 0.16);
            vec3 src = texture2D(tex0, fract(tuv)).rgb;

            // Drowned, not deleted. Depth fog eats the far end.
            float fog = smoothstep(0.02, 0.42, r);
            vec3 col = src * (0.030 + 0.135 * fog);
            col *= vec3(0.80, 0.94, 0.86);

            // Structure in the walls: long ribs rushing past.
            float ribs = sin(depth * 3.1 + ang * 3.0) * 0.5 + 0.5;
            col += vec3(0.045, 0.055, 0.052) * pow(ribs, 6.0) * fog
                * (0.7 + 0.8 * near);

            // FILAMENTS streaming past -- keyed to scroll, so they are what
            // tells the eye how fast it is going.
            float fx = ang * 3.4;
            float jitter = dk_hash(vec2(floor(fx * 2.0), 1.0));
            float band = dk_fbm(vec2(fx * 1.6 + jitter * 9.0,
                                    depth * 0.55 + jitter * 4.0));
            col += vec3(0.055, 0.064, 0.070) * smoothstep(0.60, 0.95, band)
                * fog * (0.6 + 0.9 * near);

            // WRIGGLE, out of step with everything else.
            float wr = dk_fbm(vec2(c.x * 4.5 + sin(t * 0.4) * 0.8,
                                c.y * 4.5 - t * 0.16));
            col += vec3(0.030, 0.026, 0.034) * smoothstep(0.58, 0.98, wr)
                * (0.5 + 1.6 * near);

            // THE LANTERN. It is being carried by the thing doing the
            // running, so it lights the near walls hardest and gives out
            // somewhere up the throat -- one lamp in a corridor, never a
            // floodlight, and it flickers because it always has. It is the
            // only warm thing in either act.
            if (lamp > 0.001) {
                float flick = 0.84 + 0.16 * dk_noise(vec2(t * 8.0, 3.0));
                float reach = smoothstep(0.03, 0.34, r);
                float down = smoothstep(-0.60, 0.30, c.y / max(r, 0.0007));
                col += vec3(0.145, 0.136, 0.108) * lamp * flick * reach
                    * (0.30 + 0.70 * down) * (0.45 + 0.55 * fog);
                // And it picks the ribs out of the walls, which is most of
                // why raising it feels like being given the corridor back.
                col += vec3(0.070, 0.074, 0.066) * lamp * flick
                    * pow(ribs, 3.0) * reach * 0.8;
            }

            // Far-off discharges, rare and cold.
            float bolt = dk_hash(vec2(floor(t * 2.3), 7.0));
            if (bolt > 0.955) {
                float bx = dk_hash(vec2(floor(t * 2.3), 9.0));
                float line = 1.0 - smoothstep(0.0, 0.03,
                    abs(uv.x - bx) + abs(sin(uv.y * 8.0 + bx * 20.0)) * 0.02);
                col += vec3(0.30, 0.36, 0.40) * line * 0.5;
            }

            // SOMETHING ENORMOUS, OUT PAST THE WALLS. Only ever at large
            // radius -- outside the corridor, where you cannot go and it does
            // not need to come. It occludes the far structure and carries one
            // cold rim, and it never interacts with anything.
            if (vast > 0.001) {
                float far_mask = smoothstep(0.28, 0.56, r);
                float body = sin(ang * 0.85 + t * 0.055) * 0.5 + 0.5;
                float sil = smoothstep(0.40, 0.60, body);
                col = mix(col, col * 0.04, sil * far_mask * vast);
                float rim2 = 1.0 - smoothstep(0.0, 0.055, abs(body - 0.50));
                col += vec3(0.055, 0.095, 0.125) * rim2 * far_mask * vast;
            }

            // PRESSURE. The edges come in as it closes, breathing faster the
            // nearer it is. A blackout slams it shut for a moment, the walls
            // themselves close over the run, and a stare shuts everything
            // that is not the thing you are staring at.
            float squeeze = 0.80 + 1.75 * near + 3.2 * blind + 1.45 * close
                        + 2.10 * look - 0.55 * lamp
                        + 0.10 * sin(t * (1.6 + 3.4 * near)) * (0.3 + near);
            float vig = 1.0 - dot(c, c) * squeeze;
            col *= max(vig, 0.0);

            // It is behind you, so the bottom of the frame is the worst place
            // to be looking -- until you turn round, at which point the worst
            // place to be looking is straight ahead.
            float behind = smoothstep(0.30, 1.0, uv.y) * near * (1.0 - look);
            col *= 1.0 - 0.50 * behind;
            col += vec3(0.075, 0.012, 0.020) * behind * (0.35 + 0.65 * beat);
            col += vec3(0.090, 0.014, 0.024) * look * near
                * (0.30 + 0.70 * beat);

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

    HOR_ZOOM_ACT1 = 0.34
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
    HOR_BLIND_WARN = 26
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
    HOR_STRUTS = 7                 # hoops in flight at once
    HOR_GROWTHS = 6                # masses clinging to the walls
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
    HOR_RESOLVE_CALM = 0.62        # how much of the pressure it takes off
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
    HOR_WIN = "#040605e8"
    HOR_PALE = "#b8c4ba"
    HOR_WARN = "#c9b46a"
    HOR_BLOOD = "#8e1622"
    HOR_BLACK = "#020303"

    HOR_CMDS = (("light", "LIGHT"), ("listen", "LISTEN"),
                ("steady", "STEADY"), ("run", "RUN"))

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

        def __init__(self, retry=False, deaths=0, debug=False, start_open=False):
            self.result = None
            self.paused = False
            self.debug = bool(debug)
            self.retry = bool(retry)
            self.deaths = int(deaths)
            self.god = inv_godmode_on()

            self.tick = 0
            self.clock = 0.0
            self.spin = 0.0
            self.rng = inv_random.Random()

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

            if start_open:
                self.dread = 55.0
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

        def _beat(self, label, value="", after="enemy"):
            self.beat_label = label
            self.beat_value = value
            self.beat_after = after
            self.mode = "beat"
            self.mtick = 0

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
            else:
                self.cursor = 0

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
                self.flash = 0.55
                value = "-" + str(dmg)

            elif cmd == "listen":
                self.gain_nerve(HOR_LISTEN_NERVE)
                self.read = True
                self.play("tick", 0.8)
                value = "+" + str(HOR_LISTEN_NERVE)

            elif cmd == "steady":
                self.gain_nerve(HOR_STEADY_NERVE)
                self.guard = True
                self.play("guard")
                value = "+" + str(HOR_STEADY_NERVE)

            elif cmd == "run":
                # It never works in here. In the next half it is the only
                # thing that does.
                self.play("miss")
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
                self.hurt(dmg, 640, 470)
                self.spend_nerve(14)
                self.read = False
                self.guard = False
                self.held = False
                self.last_enemy = "reach"
                self._beat("IT REACHES", "-" + str(dmg), self._after_enemy())
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
            elif move == "whisper":
                nerve_dmg = 9
            elif move == "still":
                # THE UNCANNY TURN. Nothing happens. Nothing is printed. The
                # only turn in this project that resolves to a blank -- and it
                # is why the next one lands twice as hard.
                self.held = True
                self.play("tick", 0.4)
                self.read = False
                self.guard = False
                self._beat(label, "", self._after_enemy())
                return
            elif move == "behind":
                self.dread = min(float(HOR_DREAD_MAX), self.dread + 26)
                self.play("wind", 0.7)
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
                self.hurt(dmg, 640, 470)
                value = "-" + str(dmg)
            if nerve_dmg > 0:
                if self.read:
                    nerve_dmg = int(nerve_dmg * HOR_READ_MULT)
                self.spend_nerve(nerve_dmg)
                self.play("tick", 0.6)
                value = ("-" + str(nerve_dmg) + " NERVE") if not value else value

            self.read = False
            self.guard = False
            self._beat(label, value, self._after_enemy())

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
            if 20 <= t < 110:
                self.panel_slide = inv_smooth((t - 20) / 90.0)
                self.shake = max(self.shake, 0.3)
            if t == 110:
                self.play("slam")
                self.flash = 0.9
                self.shake = 1.0
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

        def _stumble(self):
            self.stumble = HOR_STUMBLE_TICKS
            self.gap = max(0.0, self.gap - HOR_GAP_STUMBLE)
            self.hurt(HOR_STUMBLE_HP, self.px, self.py - 30)
            self.lurch = 1.0
            self.shake = 1.0
            self.freeze = 4
            self.play("cut_big", 0.8)

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
init python:
    class HORStage(renpy.Displayable):
        """One CDD. Steps HORGame at a fixed 60Hz inside render() and paints
        the whole encounter from cached-texture blits."""

        _tf_cache = {}
        _misc_cache = {}
        _text_cache = {}

        PANEL_CMD = (40, 548, 470, 148)
        PANEL_HUD = (770, 548, 470, 148)

        def __init__(self, game, **kwargs):
            super(HORStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0

        def _misc(self, key, builder):
            d = HORStage._misc_cache.get(key)
            if d is None:
                if len(HORStage._misc_cache) > 600:
                    HORStage._misc_cache.clear()
                d = builder()
                HORStage._misc_cache[key] = d
            return d

        def _text(self, text, size, color, font=INV_FONT, bold=False, outline=True):
            key = (text, size, color, font, bold, outline)
            t = HORStage._text_cache.get(key)
            if t is None:
                if len(HORStage._text_cache) > 200:
                    HORStage._text_cache.clear()
                outl = [(2, "#020303", 0, 0)] if outline else []
                t = Text(text, size=size, color=color, bold=bold, font=font,
                        outlines=outl, substitute=False)
                HORStage._text_cache[key] = t
            return t

        def _body_plain(self, zoom, alpha=1.0, tint=None):
            ab = int(inv_clamp(alpha, 0.0, 1.0) * 6)
            key = ("plain", round(zoom, 3), ab, tint)
            tf = HORStage._tf_cache.get(key)
            if tf is None:
                kw = dict(zoom=zoom, subpixel=True)
                if ab < 6:
                    kw["alpha"] = ab / 6.0
                if tint:
                    kw["matrixcolor"] = TintMatrix(tint)
                tf = Transform(HOR_SPRITE, **kw)
                HORStage._tf_cache[key] = tf
            return tf

        def event(self, ev, x, y, st):
            self.game.keys.handle_event(ev)
            return None

        # ----- render ----------------------------------------------------------

        def render(self, width, height, st, at):
            global HOR_PALL_OK, HOR_DARK_OK
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

            sblit = rv.subpixel_blit

            shake_x = shake_y = 0
            if g.shake > 0.01:
                amp = 12.0 * g.shake
                shake_x = int(math.sin(g.tick * 1.9) * amp)
                shake_y = int(math.cos(g.tick * 2.7) * amp * 0.6)

            chasing = g.mode == "run" or (g.mode in ("leave_w", "leave_l")
                                        and g.corrupt > 0.4)

            # --- 1. the room ----------------------------------------------------
            if chasing:
                self._render_dark(g, rv, rect, st, at)
            else:
                self._render_pall(g, rv, rect, st, at)

            # --- 2. the encounter ------------------------------------------------
            if chasing:
                self._render_chase(g, rv, tex, rect, qa, blit_text, canvas,
                                sblit, shake_x, shake_y, st, at)
            else:
                self._render_room(g, rv, tex, rect, qa, blit_text, canvas,
                                sblit, shake_x, shake_y, st, at)

            # --- 3. numbers ------------------------------------------------------
            for f in g.floats:
                a = inv_clamp(f["life"] / 26.0, 0.0, 1.0)
                blit_text(f["text"], 30 if f["big"] else 21,
                        f["color"] + qa(a), int(f["x"]) + shake_x,
                        int(f["y"]) + shake_y, bold=f["big"], anchor=(0.5, 0.5),
                        w=260, h=60)

            if g.paused:
                rv.blit(rect("#020303c8", 1280, 720), (0, 0))
                blit_text("PAUSED", 40, HOR_INK, 640, 316, bold=True,
                        anchor=(0.5, 0.5), w=600, h=70)
                blit_text("ESC  RESUME        Q  QUIT", 16, HOR_DIM,
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

        # ----- backdrops -------------------------------------------------------

        def _render_pall(self, g, rv, rect, st, at):
            global HOR_PALL_OK
            if HOR_PALL_OK:
                try:
                    quad = Transform(
                        HOR_SOUP_IMG, xysize=(1280, 720), mesh=True,
                        shader="inv.pall",
                        u_hor_res=(1280.0, 720.0),
                        u_hor_time=g.clock,
                        u_hor_dread=g.dread_frac(),
                        u_hor_pulse=g.beat_pulse,
                        u_hor_flash=g.flash,
                        u_hor_dark=g.dark,
                        u_hor_spin=g.spin,
                        u_hor_hole=(float(g.hole[0]), float(g.hole[1]),
                                    float(g.hole[2]), float(g.hole[3])))
                    qr = renpy.render(quad, 1280, 720, st, at)
                    rv.depends_on(qr)
                    rv.blit(qr, (0, 0))
                    return
                except Exception as e:
                    HOR_PALL_OK = False
                    try:
                        renpy.log("INV FX: pall render failed: %r" % e)
                    except Exception:
                        pass
            rv.blit(rect(HOR_BLACK, 1280, 720), (0, 0))

        def _render_dark(self, g, rv, rect, st, at):
            global HOR_DARK_OK
            if HOR_DARK_OK:
                try:
                    quad = Transform(
                        HOR_SOUP_IMG, xysize=(1280, 720), mesh=True,
                        shader="inv.dark",
                        u_hor_res=(1280.0, 720.0),
                        u_hor_time=g.clock,
                        u_hor_scroll=g.scroll * 0.004,
                        u_hor_near=g.near_frac(),
                        u_hor_beat=g.beat_pulse,
                        u_hor_lurch=g.lurch,
                        u_hor_blind=g.blind,
                        u_hor_glitch=g.glitch,
                        u_hor_flash=g.flash,
                        u_hor_dark=g.dark,
                        u_hor_look=g.look_view,
                        u_hor_vast=g.vast,
                        u_hor_close=g.run_frac(),
                        u_hor_lamp=g.lamp_lit)
                    qr = renpy.render(quad, 1280, 720, st, at)
                    rv.depends_on(qr)
                    rv.blit(qr, (0, 0))
                    return
                except Exception as e:
                    HOR_DARK_OK = False
                    try:
                        renpy.log("INV FX: dark render failed: %r" % e)
                    except Exception:
                        pass
            rv.blit(rect(HOR_BLACK, 1280, 720), (0, 0))

        # ----- the body --------------------------------------------------------

        def _draw_body(self, g, rv, tex, sblit, cx, cy, zoom, sx, sy, st, at,
                    warp=1.0, stretch=(1.0, 1.0), diss=0.0, hurt=0.0,
                    alpha=1.0, swell=1.0, reach=1.0):
            # Generous margin: the warp displaces pixels outward and the
            # fray grows smoke past the silhouette, and anything that leaves
            # the plate is simply cut off.
            plate_zoom = min(zoom, HOR_PLATE_MAX_ZOOM)
            extra = zoom / plate_zoom
            plate, W, H = inv_body_plate(HOR_SPRITE, HOR_SPRITE_W, HOR_SPRITE_H,
                                        plate_zoom, pad_x=1.60, pad_y=1.55)
            # The figure is off-centre in its own canvas; put the FIGURE where
            # the caller asked, not the canvas.
            cx = cx + HOR_FIG_DX * zoom
            cy = cy + HOR_FIG_DY * zoom
            zoom = float(zoom)

            if HOR_WITHER_OK or INV_FLESH_OK:
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
                            # Act one measures how CLOSE it is standing (dread),
                            # act two measures how little runway is left (near).
                            # The body only cares that it is near you, so it takes
                            # whichever of the two is currently saying so.
                            u_wit_near=float(max(g.dread_frac(),
                                                g.near_frac())),
                            u_wit_diss=float(diss))
                    else:
                        body = inv_flesh(plate, W, H, g.clock, warp=warp,
                                        stretch=stretch, pivot=0.90,
                                        hurt=hurt, diss=diss)
                    if extra > 1.01:
                        body = Transform(body, zoom=extra, subpixel=True)
                    if alpha < 0.99:
                        body = Transform(body, alpha=alpha)
                    r = renpy.render(body, int(W * extra) + 8,
                                    int(H * extra) + 8, st, at)
                    rv.depends_on(r)
                    w, h = r.get_size()
                    sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))
                    return
                except Exception:
                    pass

            r, (w, h) = tex(("plainbody", round(zoom, 3), alpha),
                            self._body_plain(zoom, alpha=alpha), 900, 900)
            sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))

        def _draw_heart(self, g, rv, tex, sblit, cx, cy, sx, sy, st, at,
                    scale=1.0, diss=0.0):
            """The runner. Same SOUL heart as the other modes, warped harder
            than anything else on screen and beating out of time."""
            plate, W, H = inv_body_plate(INV_HEART, INV_HEART_W, INV_HEART_H,
                                        HOR_HEART_ZOOM * max(0.05, scale),
                                        pad_x=2.2, pad_y=2.2, nearest=True)
            squeeze = 1.0 - 0.20 * g.beat_pulse
            warp = HOR_HEART_WARP * (1.0 + 0.35 * g.near_frac())
            if INV_FLESH_OK:
                try:
                    d = inv_flesh(plate, W, H, g.clock * 2.6, warp=warp,
                                split=0.9,
                                stretch=(1.0 / max(0.5, squeeze), squeeze),
                                pivot=0.5, hurt=0.0,
                                diss=inv_clamp(0.04 + 0.05 * g.near_frac()
                                            + 0.85 * diss, 0.0, 1.0))
                    r = renpy.render(d, W, H, st, at)
                    rv.depends_on(r)
                    w, h = r.get_size()
                    sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))
                    return
                except Exception:
                    pass
            hz = HOR_HEART_ZOOM * max(0.05, scale)
            heart = self._misc(("heartplain", round(hz, 2)),
                            lambda z=hz: Transform(INV_HEART, zoom=z,
                                                nearest=True, subpixel=True))
            r, (w, h) = tex(("heartplain", round(hz, 2)), heart, 160, 160)
            sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))

        # ----- ACT ONE ---------------------------------------------------------

        def _render_room(self, g, rv, tex, rect, qa, blit_text, canvas,
                        sblit, sx, sy, st, at):
            arriving = (g.mode == "arrive")
            dread = g.dread_frac()

            # It stands closer as dread climbs: bigger, lower, and it stops
            # bobbing -- the stillness is the tell.
            zoom = HOR_ZOOM_ACT1 * (1.0 + 0.30 * dread)
            bob = math.sin(g.clock * 0.7) * (7.0 * (1.0 - dread))
            cy = 300 + bob + 40 * dread

            if arriving:
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
                cy = inv_lerp(cy, g.hole[1] + 30.0, g.emerge)
                stretch = (1.0, g.body_scale)
                warp = 0.9 + 1.1 * g.emerge
                diss = g.emerge * 0.9
            else:
                stretch = (1.0 - 0.03 * math.sin(g.clock * 0.9),
                        1.0 + 0.04 * math.sin(g.clock * 0.62))
                warp = 0.7 + 0.9 * dread
                diss = 0.0

            self._draw_body(g, rv, tex, sblit, 640, cy, zoom, sx, sy, st, at,
                            warp=warp, stretch=stretch, diss=diss,
                            hurt=0.7 if g.hit_flash > 0.4 else 0.0,
                            swell=0.7 + 1.1 * dread,
                            reach=0.5 + 1.1 * dread)

            if arriving:
                return

            blit_text("HORROR", 15, HOR_PALE, 380, 28, bold=True, w=300, h=30)
            bar_w = 520
            rv.blit(rect("#020303b4", bar_w + 4, 12), (380 - 2, 52))
            rv.blit(rect("#2a1d20", bar_w, 8), (380, 54))
            # The bar is DREAD, not its health. Its health is not your business.
            fill = int(bar_w * dread)
            if fill > 0:
                rv.blit(rect(HOR_BLOOD if dread < 0.8 else "#d3283c", fill, 8),
                        (380, 54))

            slide = int(g.panel_slide * 200)
            if g.panel_slide < 1.0:
                self._panel(rv, rect, HORStage.PANEL_CMD, sx, sy + slide)
                self._panel(rv, rect, HORStage.PANEL_HUD, sx, sy + slide)
                self._panel_contents(g, rv, tex, rect, qa, blit_text, sx,
                                    sy + slide)

        def _panel(self, rv, rect, box, sx, sy):
            x, y, w, h = box
            x += sx
            y += sy
            rv.blit(rect(HOR_PALE, w + 6, h + 6), (x - 3, y - 3))
            rv.blit(rect(HOR_BLACK, w + 2, h + 2), (x - 1, y - 1))
            rv.blit(rect(HOR_WIN, w, h), (x, y))

        def _panel_contents(self, g, rv, tex, rect, qa, blit_text, sx, sy):
            cx, cy, cw, ch = HORStage.PANEL_CMD
            cx += sx
            cy += sy

            if g.mode == "menu":
                for i, row in enumerate(HOR_CMDS):
                    live = (i == g.cursor)
                    ry = cy + 16 + i * 30
                    if live:
                        rv.blit(rect(HOR_PALE + qa(0.12), cw - 28, 26),
                                (cx + 14, ry - 3))
                        rv.blit(rect(HOR_BLOOD if g.panic else HOR_PALE, 9, 9),
                                (cx + 22, ry + 6))
                    blit_text(row[1], 20, HOR_INK if live else HOR_FAINT,
                            cx + 42, ry, bold=live, w=260, h=30)
                    if row[0] == "light":
                        blit_text(str(HOR_LIGHT_NERVE), 14,
                                HOR_PALE if live else HOR_FAINT,
                                cx + cw - 22, ry + 4, anchor=(1.0, 0.0),
                                w=120, h=26)
                blit_text("Z  OK      ESC  PAUSE", 12, HOR_FAINT,
                        cx + cw - 16, cy + ch - 22, anchor=(1.0, 0.0),
                        w=420, h=24)

            elif g.mode == "beat":
                blit_text(g.beat_label, 22, HOR_INK, cx + 20, cy + 30,
                        bold=True, w=cw - 40, h=40)
                if g.beat_value:
                    blit_text(g.beat_value, 30, HOR_WARN, cx + 20, cy + 62,
                            bold=True, w=cw - 40, h=44)
                if g.mtick > 12 and (g.tick // 20) % 2 == 0:
                    rv.blit(rect(HOR_INK, 14, 4), (cx + cw - 36, cy + ch - 26))

            hx, hy, hw, hh = HORStage.PANEL_HUD
            hx += sx
            hy += sy
            blit_text(inv_player_name(), 19, HOR_INK, hx + 20, hy + 12,
                    bold=True, w=hw - 40, h=32)
            self._odometer(g, rv, tex, rect, qa, blit_text, "HP", g.hp_shown,
                        g.hp, hx + 20, hy + 44, HOR_INK)
            self._odometer(g, rv, tex, rect, qa, blit_text, "NV",
                        g.nerve_shown, g.nerve, hx + 20, hy + 96, HOR_PALE,
                        small=True)
            if g.panic:
                blit_text("PANIC", 13, HOR_BLOOD, hx + hw - 20, hy + 16,
                        anchor=(1.0, 0.0), w=200, h=26)
            if g.god:
                blit_text("GOD", 12, HOR_WARN + "aa", hx + hw - 20,
                        hy + hh - 24, anchor=(1.0, 0.0), w=120, h=24)

        def _odometer(self, g, rv, tex, rect, qa, blit_text, label, shown, real,
                    x, y, color, small=False):
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
                rv.blit(rect("#07090880", cell_w - 4, cell_h), (dx, y))
                if rolling:
                    off = int(frac * cell_h * (1 if real < shown else -1))
                    nxt = str((int(ch) + (1 if real > shown else -1)) % 10)
                    blit_text(nxt, size, color + qa(0.45),
                            dx + (cell_w - 4) // 2,
                            y + off - (cell_h if real < shown else -cell_h) + 2,
                            anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)
                    blit_text(ch, size, color, dx + (cell_w - 4) // 2,
                            y + off + 2, anchor=(0.5, 0.0), w=cell_w,
                            h=cell_h, bold=True)
                else:
                    blit_text(ch, size, color, dx + (cell_w - 4) // 2, y + 2,
                            anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)

        # ----- ACT TWO: THE CHASE ----------------------------------------------

        def _render_chase(self, g, rv, tex, rect, qa, blit_text, canvas,
                        sblit, sx, sy, st, at):
            near = g.near_frac()
            lookv = inv_clamp(g.look_view, 0.0, 1.0)
            cv = canvas()

            # HOW MUCH YOU ARE ALLOWED TO SEE. The radius closes as it gets
            # nearer -- being chased down takes your eyes first -- but it is
            # FLOORED at however far the corridor travels in HOR_MIN_WARN
            # ticks. Sprinting therefore widens the light instead of
            # outrunning it, which is the difference between oppressive and
            # unfair (fairness rule 1).
            # Sight is now a DEPTH window, and it is still floored by warning
            # time: whatever else happens, a mass is lit for at least
            # HOR_MIN_WARN ticks before it reaches your plane.
            dz_tick = max(g.speed, HOR_WALK) * HOR_Z_RATE
            # THE LANTERN IS THE BIG TERM and the dead tank is the small one,
            # and BOTH are inside the max() -- so raising it is a real gift and
            # losing it is a real loss, while the warning-time floor underneath
            # is never negotiated with either way.
            sight_z = max(inv_lerp(0.62, 0.26, near) * (1.0 - 0.55 * g.blind)
                        * inv_lerp(1.0, HOR_RESOLVE_SIGHT, g.resolved())
                        * inv_lerp(1.0, HOR_LAMP_SIGHT, g.lamp_lit)
                        * (HOR_LAMP_DEAD_SIGHT if g.lamp_dead else 1.0),
                        dz_tick * HOR_MIN_WARN)

            # --- SPEED. Radial streaks off the vanishing point, length and
            # brightness driven by how fast you are actually going. Without
            # these the tunnel reads as wallpaper and the masses read as
            # falling boxes.
            rush = inv_clamp((g.speed - HOR_WINDED_SPEED)
                            / (HOR_SPRINT - HOR_WINDED_SPEED), 0.0, 1.0)

            # --- RAILS. Four lines running away to the vanishing point, two
            # along the foot of each wall and two along the head of it. They
            # do not move -- they are where the corridor GOES -- and having
            # somewhere for everything else to converge on is most of what
            # tells the eye this is a throat rather than a gradient.
            lo, hi = g.lane()
            rail_a = int(38 + 46 * g.lamp_lit + 22 * rush)
            for wx in (lo, hi):
                for wy in (HOR_PLANE_Y, HOR_CEIL_Y):
                    try:
                        cv.line((146, 158, 152, rail_a),
                                (int(HOR_VP[0]) + sx, int(HOR_VP[1]) + sy),
                                (int(wx) + sx, int(wy) + sy), 1)
                    except Exception:
                        pass

            n_streak = 26
            for k in range(n_streak):
                seed = (k * 2654435761) % 1000 / 1000.0
                ang = (seed * 6.2831853
                    + math.sin(g.clock * 0.13 + k) * 0.05)
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
                a_st = int((26 + 92 * rush) * inv_clamp(p0 * 2.4, 0.0, 1.0))
                try:
                    cv.line((176, 190, 182, a_st),
                            (int(HOR_VP[0] + math.cos(ang) * r0) + sx,
                            int(HOR_VP[1] + math.sin(ang) * r0) + sy),
                            (int(HOR_VP[0] + math.cos(ang) * r1) + sx,
                            int(HOR_VP[1] + math.sin(ang) * r1) + sy),
                            1 + int(2 * rush))
                except Exception:
                    pass

            # --- the corridor's edges ------------------------------------------
            # THE WALLS ARE THE PRESSURE. They were two thin wriggling lines
            # over open black, which is what made the whole act read as empty:
            # a corridor with nothing at the sides of it is a field. They are
            # solid mass now, they come inward as the run goes on, and the
            # wriggle rides on their inner face.
            wrig = 26.0 + 60.0 * near
            wall_a = 0.30 + 0.45 * g.run_frac()
            for side in (0, 1):
                base_x = lo if side == 0 else hi
                pts = []
                for k in range(13):
                    yy = 96 + k * 52
                    ph = g.clock * 1.3 + k * 0.7 + side * 2.1
                    off = math.sin(ph) * wrig + math.sin(ph * 0.47) * wrig * 0.5
                    ex = base_x + (off if side == 0 else -off)
                    pts.append((int(ex) + sx, int(yy) + sy))
                    # Fill everything outboard of the edge, so there is
                    # somewhere the corridor stops being.
                    if side == 0:
                        w = max(1, int(ex))
                        rv.blit(rect("#05070699", w, 54), (sx, int(yy) - 2 + sy))
                    else:
                        w = max(1, int(1280 - ex))
                        rv.blit(rect("#05070699", w, 54),
                                (int(ex) + sx, int(yy) - 2 + sy))
                try:
                    cv.lines((150, 160, 155, int(60 + 120 * wall_a)), False,
                            pts, 3)
                except Exception:
                    pass

            # --- STRUCTURE ---------------------------------------------------
            # Hoops around the corridor and things growing off the walls, all
            # of it on the same depth phase as the masses so nothing
            # parallaxes against anything. None of it is a hazard; the entire
            # job is to make the corridor a PLACE, because a corridor with
            # nothing in it is the same picture at every speed.
            phase0 = g.scroll * HOR_STRUCT_PHASE
            lamp = g.lamp_lit

            for k in range(HOR_STRUTS):
                ph = (phase0 + k / float(HOR_STRUTS)) % 1.0
                z = HOR_Z_FAR - ph * (HOR_Z_FAR - 0.07)
                if z <= 0.055:
                    continue
                persp, _fy = hor_project(z)
                x0 = int(hor_screen_x(lo, persp)) + sx
                x1 = int(hor_screen_x(hi, persp)) + sx
                y0 = int(hor_screen_y(HOR_CEIL_Y, persp)) + sy
                y1 = int(hor_screen_y(HOR_PLANE_Y, persp)) + sy
                w = max(2, x1 - x0)
                h = max(2, y1 - y0)
                # Fades in out of the far dark and out again as it goes past
                # the lens, so nothing ever pops.
                a = (inv_clamp(persp * 2.6, 0.0, 1.0)
                    * inv_clamp((1.0 - ph) * 5.0, 0.0, 1.0)
                    * (0.34 + 0.46 * lamp))
                if a < 0.03:
                    continue
                col = HOR_FAINT + qa(a)
                t_ = max(1, int(2 * persp) + 1)
                rv.blit(rect(col, w, t_), (x0, y0))
                rv.blit(rect(col, w, t_), (x0, y1 - t_))
                rv.blit(rect(col, t_, h), (x0, y0))
                rv.blit(rect(col, t_, h), (x1 - t_, y0))

            for k in range(HOR_GROWTHS):
                seed = ((k * 2246822519) % 997) / 997.0
                ph = (phase0 * (0.94 + 0.12 * seed) + seed) % 1.0
                z = HOR_Z_FAR - ph * (HOR_Z_FAR - 0.07)
                if z <= 0.055:
                    continue
                persp, _fy = hor_project(z)
                side = k % 2
                wx = lo if side == 0 else hi
                gw = max(2, int((30.0 + 70.0 * seed) * persp))
                gh = max(2, int((90.0 + 180.0 * seed) * persp))
                gy = int(hor_screen_y(inv_lerp(HOR_CEIL_Y + 40.0,
                                            HOR_PLANE_Y - 60.0, seed),
                                    persp)) + sy
                gx = int(hor_screen_x(wx, persp)) + sx
                if side == 1:
                    gx -= gw
                a = (inv_clamp(persp * 2.2, 0.0, 1.0)
                    * inv_clamp((1.0 - ph) * 5.0, 0.0, 1.0))
                if a < 0.03:
                    continue
                rv.blit(rect("#000000" + qa(0.80 * a), gw, gh), (gx, gy))
                rv.blit(rect(HOR_FAINT + qa((0.24 + 0.34 * lamp) * a),
                            max(1, int(2 * persp) + 1), gh),
                        (gx if side == 1 else gx + gw - 1, gy))

            # THINGS IN THE WALLS THAT ARE NOT MASSES. Pairs of points, mostly
            # shut, that open for a moment as they go past. No mechanics and
            # no tell -- they are not the watchers and they never become them,
            # which is exactly why the watchers work.
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
                ex = int(hor_screen_x(lo if side == 0 else hi, persp)) + sx
                ey = int(hor_screen_y(inv_lerp(HOR_CEIL_Y + 60.0,
                                            HOR_PLANE_Y - 90.0, seed),
                                    persp)) + sy
                a = (0.34 + 0.40 * lamp) * inv_clamp(persp * 2.4, 0.0, 1.0) \
                    * ((open_u - 0.72) / 0.28)
                sz = max(1, int(5 * persp) + 1)
                dx_e = max(2, int(16 * persp))
                rv.blit(rect(HOR_PALE + qa(a), sz, sz),
                        (ex - (dx_e if side == 1 else 0), ey))
                rv.blit(rect(HOR_PALE + qa(a), sz, sz),
                        (ex + (0 if side == 1 else dx_e), ey))

            # --- THE LANTERN'S OWN LIGHT ---------------------------------------
            # A strip of corridor, lit from where you are actually standing,
            # narrowing up the throat. It moves when you steer, which is the
            # whole graphic affordance for the directional rule on the
            # watchers -- you can see the light is not on the thing.
            if lamp > 0.02:
                steps = 15
                flick = 0.86 + 0.14 * math.sin(g.clock * 21.0) \
                    * math.sin(g.clock * 7.3)
                prev_y = None
                for k in range(steps + 1):
                    u = k / float(steps)
                    z = inv_lerp(HOR_Z_NEAR, HOR_Z_NEAR + 0.66, u)
                    persp, yy = hor_project(z)
                    if prev_y is None:
                        prev_y = yy
                        continue
                    hw = max(2, int(inv_lerp(210.0, 470.0, u) * persp))
                    cxp = int(hor_screen_x(g.px, persp))
                    hgt = max(1, int(prev_y - yy) + 1)
                    a = 0.115 * lamp * flick * ((1.0 - u) ** 1.5)
                    rv.blit(rect(HOR_PALE + qa(a), hw * 2, hgt),
                            (cxp - hw + sx, int(yy) + sy))
                    prev_y = yy
                # The lamp itself, held out to one side of the runner.
                lampx = int(g.px) + 22 + sx
                lampy = int(g.py) - 16 + sy
                rv.blit(rect("#e8e4c8" + qa(0.55 * lamp * flick), 7, 7),
                        (lampx, lampy))
                rv.blit(rect("#e8e4c8" + qa(0.20 * lamp * flick), 19, 19),
                        (lampx - 6, lampy - 6))

            # --- obstacles -------------------------------------------------------
            for o in g.obstacles:
                persp, oy = hor_project(o["z"])
                ox = hor_screen_x(o["x"], persp)
                # Nearness in DEPTH is what the light gates on now.
                a = inv_clamp(1.0 - (o["z"] - HOR_Z_NEAR) / max(0.05, sight_z),
                            0.0, 1.0)
                w = max(4, int(o["w"] * persp))
                h = max(3, int(o["h"] * persp))
                x0 = int(ox - w * 0.5) + sx
                y0 = int(oy - h * 0.5) + sy

                # THE OUTLINE IS ALWAYS LEGIBLE (fairness rule 2). A full box,
                # not a hairline: from the moment it is in the frame you can
                # read where it is and how wide, and the dark only ever hides
                # the mass INSIDE it.
                #
                # NOTE the alpha floor is applied to the FINAL value, not
                # multiplied into it. qa() quantizes to eight levels, so a
                # floor of 0.34 scaled by 0.42 lands on 6/255 -- which is what
                # "the edges are not even visible" looked like.
                # A blackout dims the outline hard but never puts it out --
                # the fear of the dark is allowed to terrify, not to kill.
                # A STARE BLINDS YOU FORWARD -- but the outline never goes
                # out entirely, because fairness rule 2 is not suspended just
                # because the player chose this.
                edge_a = (max(HOR_EDGE_FLOOR, a) * (1.0 - 0.55 * g.blind)
                        * (1.0 - 0.42 * lookv))
                edge = HOR_PALE + qa(edge_a)
                rv.blit(rect(edge, w, 3), (x0, y0))
                rv.blit(rect(edge, w, 3), (x0, y0 + h - 3))
                rv.blit(rect(edge, 3, h), (x0, y0))
                rv.blit(rect(edge, 3, h), (x0 + w - 3, y0))

                # The mass itself: blacker than the black, with a wet underside.
                am = a * (1.0 - 0.85 * lookv)
                if am > 0.02:
                    rv.blit(rect("#000000" + qa(0.85 * am), w - 6, h - 6),
                            (x0 + 3, y0 + 3))
                    rv.blit(rect("#3a2126" + qa(0.55 * am), w - 6, 3),
                            (x0 + 3, y0 + h - 6))
                # A REACHER is part of the wall it grew out of, so it is drawn
                # joined to it. Nothing in this corridor should look like it is
                # floating in the middle of the air.
                if o.get("reach") is not None and am > 0.02:
                    if o["reach"] == 0:
                        rv.blit(rect("#000000" + qa(0.75 * am),
                                    max(1, x0), h - 8),
                                (sx, y0 + 4))
                    else:
                        rv.blit(rect("#000000" + qa(0.75 * am),
                                    max(1, 1280 - (x0 + w)), h - 8),
                                (x0 + w, y0 + 4))

            # --- THE WATCHER ---------------------------------------------------
            # It is drawn where it IS and nowhere in between, because it does
            # not travel between stages -- it is somewhere, and then it is
            # somewhere nearer. Two things are readable about it at any
            # moment: how far across the wall it has come (its size), and how
            # long you have until it comes further (the bar beside it).
            wch = g.watcher
            if wch is not None:
                persp, wy = hor_project(wch["z"])
                wx = hor_screen_x(lo if wch["side"] == 0 else hi, persp)
                # Set INTO the wall, not standing beside it.
                wx += (26.0 if wch["side"] == 0 else -26.0) * persp
                stage_u = wch["stage"] / float(HOR_WATCH_STAGES - 1)
                pushing = g.lit() and g.watch_side_ok()
                # It jolts on the frame it arrives and then is perfectly
                # still, which is the entire effect.
                jolt = wch["moved"] / 12.0
                # Everything hung off it is measured in BODY units, not depth
                # units -- the sprite is 1254px tall and its head is in the
                # top eighth of that, so eye points placed off `persp` alone
                # land on its chest and the clock beside it ends up level with
                # its knees.
                bz = inv_clamp(0.62 * persp, 0.02, 0.62)
                bcy = wy - 96.0 * persp
                self._draw_body(g, rv, tex, sblit, wx, bcy, bz,
                                sx, sy, st, at,
                                warp=0.35 + 1.9 * jolt,
                                stretch=(1.0 + 0.20 * jolt,
                                        1.0 - 0.14 * jolt),
                                diss=0.0,
                                alpha=inv_clamp(0.30 + 0.62 * stage_u, 0.0, 1.0),
                                swell=0.2 + 1.4 * jolt,
                                reach=0.5 + 1.1 * stage_u)
                # ITS EYES, which are the only part of it that is bright, and
                # which go out while the light is on it.
                eye_a = (0.30 + 0.60 * stage_u) * (1.0 - 0.75 * wch["seen"])
                esz = max(2, int(30.0 * bz))
                egap = max(4, int(132.0 * bz))
                eye_y = int(bcy - 470.0 * bz) + sy
                for side_dx in (-egap // 2, egap // 2):
                    rv.blit(rect((HOR_PALE if not pushing else HOR_WARN)
                                + qa(eye_a), esz, esz),
                            (int(wx) + side_dx + sx, eye_y))
                # THE ACCUMULATOR, drawn on the wall beside it, reading BOTH
                # WAYS off a centre line: up in blood toward the next step
                # toward you, down in pale toward the step back. That is the
                # whole tutorial for the directional rule and it costs rule 1
                # nothing -- cross to its side with the lantern up and you
                # watch the bar reverse, which no sentence would teach faster.
                pw = inv_clamp(wch["p"], -1.0, 1.0)
                bh = max(22, int(320.0 * bz))
                half = bh // 2
                bx_ = int(hor_screen_x(lo if wch["side"] == 0 else hi, persp)) \
                    + (4 if wch["side"] == 0 else -8) + sx
                by_ = int(bcy - 470.0 * bz - bh * 0.5) + sy
                rv.blit(rect("#05070699", 4, bh), (bx_, by_))
                rv.blit(rect(HOR_FAINT + qa(0.60), 8, 1), (bx_ - 2, by_ + half))
                fill = max(1, int(half * abs(pw)))
                if pw >= 0.0:
                    rv.blit(rect(HOR_BLOOD + qa(0.40 + 0.50 * stage_u),
                                4, fill), (bx_, by_ + half - fill))
                else:
                    rv.blit(rect(HOR_PALE + qa(0.75), 4, fill),
                            (bx_, by_ + half))

                # WHERE TO STAND, drawn on the boards. The directional rule is
                # the one thing about a watcher that cannot be worked out by
                # looking at it -- everything else (it is there, it is coming,
                # it stops while lit) is legible from the picture, but "and
                # only from that half of the corridor" is not. So the half it
                # can be answered from is bracketed on the floor, brightest
                # while you are outside it and while the lamp is down.
                #
                # AND IT IS HEADED WITH ACT ONE'S OWN COMMAND. LIGHT is the
                # word this player already used on this creature for a whole
                # act; rule 1 allows a state word and refuses a sentence, and
                # this says which key without ever saying press it. It stops
                # printing the moment the player drives one back for the first
                # time -- a prompt still up after it worked is a nag.
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
                    rv.blit(rect(HOR_PALE + qa(za), min(14, zw - seg), 2),
                            (zx0 + seg, zy))
                rv.blit(rect(HOR_PALE + qa(za), 2, 15), (zx0, zy - 13))
                rv.blit(rect(HOR_PALE + qa(za), 2, 15), (zx0 + zw - 2, zy - 13))
                if not g.watch_taught:
                    blit_text("LIGHT", 13,
                            HOR_WARN + qa(0.30 + 0.60 * need),
                            zx0 + zw // 2, zy + 16, bold=True,
                            anchor=(0.5, 0.0), w=200, h=26)

            # --- the thing that is ahead of you ----------------------------------
            if g.phantom is not None:
                p = g.phantom
                pp, pyy = hor_project(p["z"])
                a = 0.55 * inv_clamp(p["life"] / 90.0, 0.0, 1.0)
                self._draw_body(g, rv, tex, sblit,
                                hor_screen_x(p["x"], pp), pyy,
                                inv_clamp(0.34 * pp, 0.03, 0.50),
                                sx, sy, st, at, warp=2.4,
                                stretch=(1.0, 1.25), diss=0.35, alpha=a,
                                swell=1.6, reach=1.8)

            # --- the runner --------------------------------------------------------
            for i, (tx, ty, sprinting) in enumerate(g.trail):
                if i == 0:
                    continue
                a = 0.26 * (1.0 - i / float(len(g.trail)))
                if sprinting:
                    a *= 1.7
                size = max(3, 11 - i)
                rv.blit(rect("#ff4a5e" + qa(a * (1.0 - 0.7 * lookv)),
                            size, size),
                        (int(tx) - size // 2 + sx, int(ty) - size // 2 + sy))
            leaving = g.mode in ("leave_w", "leave_l")
            if leaving:
                self._draw_heart(g, rv, tex, sblit, g.heart_x, g.heart_y,
                                sx, sy, st, at, scale=g.heart_scale,
                                diss=g.heart_diss)
            elif not (g.stumble > 0 and (g.tick // 3) % 2 == 0):
                self._draw_heart(g, rv, tex, sblit, g.px, g.py, sx, sy, st, at)

            # --- IT ----------------------------------------------------------------
            # Rising out of the bottom of the frame. At full distance only the
            # top of its head is in the world at all; on your heels it owns a
            # third of the screen.
            self._draw_body(g, rv, tex, sblit,
                            g.follow_x, g.follow_y, g.follow_zoom, sx, sy,
                            st, at,
                            warp=(g.exit_warp if leaving else 1.6 + 1.6 * near),
                            stretch=(1.0 + 0.10 * math.sin(g.clock * 1.7),
                                    1.0 + 0.16 * math.sin(g.clock * 1.1)),
                            diss=0.0,
                            alpha=g.follow_alpha * (1.0 - lookv),
                            swell=(1.9 if leaving else 0.6 + 1.3 * near),
                            reach=(1.9 if leaving else 0.4 + 1.4 * near))

            # --- THE STARE ---------------------------------------------------
            if lookv > 0.01:
                self._render_stare(g, rv, tex, rect, qa, blit_text, sblit,
                                lookv, sx, sy, st, at)

            # THE BITE. A watcher got all the way across the wall. A held
            # frame with it filling the corridor, and then the run simply goes
            # on. The genre invented this move and there is no honest reason
            # to be above it -- but it is a SHOCK, not a gag: nothing zooms,
            # nothing squeals, it is suddenly all there is and then it is not.
            # Drawn last of the world layers, because for those few ticks it
            # IS the world.
            if g.bite_t > 0:
                bu = g.bite_t / float(HOR_BITE_FREEZE)
                rv.blit(rect("#000000" + qa(0.55 * bu), 1280, 720), (0, 0))
                self._draw_body(g, rv, tex, sblit, 640, 470,
                                1.10 + 0.10 * (1.0 - bu), sx, sy, st, at,
                                warp=2.6, stretch=(1.06, 0.97), diss=0.0,
                                alpha=inv_clamp(bu * 1.6, 0.0, 1.0),
                                swell=2.2, reach=2.2)
                rv.blit(rect(HOR_BLOOD + qa(0.22 * bu), 1280, 720), (0, 0))

            # A warning that costs nothing to read and everything to ignore.
            if g.lunge_state == "warn":
                puls = 0.5 + 0.5 * math.sin(g.tick * 0.5)
                rv.blit(rect("#8e1622" + qa(0.10 + 0.22 * puls), 1280, 720),
                        (0, 0))

            # --- HUD: a bar, a bar, and nothing else -------------------------------
            # It fades out through the ending -- an outcome should not be read
            # off a meter.
            if g.hud_fade <= 0.02:
                return
            prog = inv_clamp(g.dist / HOR_GOAL, 0.0, 1.0)
            bw = 620
            bx0 = 640 - bw // 2
            rv.blit(rect("#02030380", bw + 4, 10), (bx0 - 2, 26))
            rv.blit(rect("#1c2422", bw, 6), (bx0, 28))
            rv.blit(rect(HOR_PALE, int(bw * prog), 6), (bx0, 28))

            sw = 220
            rv.blit(rect("#02030380", sw + 4, 10), (34, 676))
            rv.blit(rect("#241c1e", sw, 6), (36, 678))
            if g.winded > 0:
                # Winded reads as a bar that is REFUSING you, not one that is
                # merely low.
                puls = 0.5 + 0.5 * math.sin(g.tick * 0.5)
                rv.blit(rect(HOR_BLOOD + qa(0.45 + 0.55 * puls),
                            int(sw * (1.0 - g.winded / float(HOR_WINDED_TICKS))),
                            6), (36, 678))
            else:
                stam_col = (HOR_PALE if g.stam > HOR_STAM_RELEASE_HINT
                            else HOR_WARN)
                rv.blit(rect(stam_col, int(sw * (g.stam / HOR_STAM_MAX)), 6),
                        (36, 678))
                # A mark at the point a careful runner lets go.
                rv.blit(rect(HOR_FAINT, 2, 10),
                        (36 + int(sw * (HOR_STAM_RELEASE_HINT / HOR_STAM_MAX)),
                        676))
            blit_text("WIND", 11, HOR_FAINT, 264, 674, w=160, h=22)

            # THE TANK. It only ever goes one way, so it is the one number in
            # the encounter that says how much run you have left in you rather
            # than how you are doing right now.
            rv.blit(rect("#02030380", sw + 4, 10), (34, 658))
            rv.blit(rect("#241c1e", sw, 6), (36, 660))
            if g.lamp_dead:
                puls = 0.5 + 0.5 * math.sin(g.tick * 0.35)
                rv.blit(rect(HOR_BLOOD + qa(0.16 + 0.20 * puls), sw, 6),
                        (36, 660))
            else:
                pf = g.power_frac()
                lamp_col = (HOR_WARN if g.lamp_lit > 0.5
                            else (HOR_PALE if pf > 0.25 else HOR_WARN))
                rv.blit(rect(lamp_col, int(sw * pf), 6), (36, 660))
            blit_text("LAMP", 11, HOR_FAINT, 264, 656, w=160, h=22)

            # A BUG in the encounter: the readouts stop being true. The bars
            # jitter and the frame tears -- but the corridor never lies, so
            # this costs composure and never a life.
            if g.glitch > 0.02:
                for k in range(5):
                    gy = int(120 + (g.tick * 37 + k * 130) % 520)
                    gh2 = 4 + ((g.tick + k * 7) % 9)
                    gx = int(math.sin(g.tick * 0.7 + k) * 60 * g.glitch)
                    rv.blit(rect(HOR_PALE + qa(0.20 * g.glitch), 1280, gh2),
                            (gx, gy))
                rv.blit(rect(HOR_BLOOD + qa(0.10 * g.glitch), 1280, 720), (0, 0))

            # HOW LONG YOU HAVE BEEN LOOKING. This one is not decoration and
            # it is not optional: a stare that can take you has to be a stare
            # you can see coming to its end, or holding the key is a coin
            # flip. It fills as you look and it is the only thing on screen
            # that turns red.
            if lookv > 0.01 or g.look_lock > 0:
                lw = 300
                lx = 640 - lw // 2
                lf = g.look_frac()
                rv.blit(rect("#02030390", lw + 4, 12), (lx - 2, 646))
                rv.blit(rect("#241c1e", lw, 8), (lx, 648))
                if g.look_lock > 0:
                    puls = 0.5 + 0.5 * math.sin(g.tick * 0.5)
                    rv.blit(rect(HOR_BLOOD + qa(0.30 + 0.45 * puls),
                                int(lw * (1.0 - g.look_lock
                                        / float(HOR_LOOK_LOCK))), 8),
                            (lx, 648))
                else:
                    col = HOR_PALE if lf < 0.62 else (
                        HOR_WARN if lf < 0.85 else HOR_BLOOD)
                    rv.blit(rect(col, int(lw * lf), 8), (lx, 648))
                    # Where a glance stops being worth nothing.
                    rv.blit(rect(HOR_FAINT, 2, 14),
                            (lx + int(lw * (HOR_LOOK_MIN
                                            / float(HOR_LOOK_MAX))), 645))
                # The distance, still -- but it is no longer why you looked.
                blit_text("%d" % int(g.gap), 30, HOR_INK, 640, 620,
                        bold=True, anchor=(0.5, 0.5), w=200, h=48)

            # WHAT THE STARE LEFT BEHIND.
            if g.resolve_t > 0.0:
                rw = 220
                rv.blit(rect("#02030380", rw + 4, 10), (34, 638))
                rv.blit(rect("#1c2422", rw, 6), (36, 640))
                rv.blit(rect(HOR_INK, int(rw * g.resolved()), 6), (36, 640))
                blit_text("RESOLVE", 11, HOR_PALE, 264, 636, w=180, h=22)

            if g.scramble > 0 and (g.tick // 6) % 2 == 0:
                blit_text("?", 40, HOR_BLOOD, g.px + sx, g.py - 54 + sy,
                        bold=True, anchor=(0.5, 0.5), w=80, h=60)

            # THE HINT LINE POINTS. It is drawn in two pieces so the lantern's
            # half can come up out of the murk on its own while a watcher is
            # on the wall -- a control hint is rule-1 legal, and one that
            # brightens exactly when the control matters is the difference
            # between a legend and a nudge.
            lamp_hot = (g.watcher is not None and not g.watch_taught)
            lw2, _lh2 = blit_text("X  SPRINT      Z  LOOK BACK   (ALL HOLD)",
                                12, HOR_FAINT, 1256, 690, anchor=(1.0, 1.0),
                                w=520, h=28)
            blit_text("A D  MOVE      W  LANTERN", 12,
                    (HOR_WARN + qa(0.55 + 0.40
                                * (0.5 + 0.5 * math.sin(g.tick * 0.13)))
                    if lamp_hot else HOR_FAINT),
                    1256 - lw2 - 22, 690, anchor=(1.0, 1.0), w=340, h=28)
            if g.god:
                blit_text("GOD", 12, HOR_WARN + "aa", 1256, 664,
                        anchor=(1.0, 1.0), w=120, h=24)

        # ----- THE STARE -------------------------------------------------------

        def _render_stare(self, g, rv, tex, rect, qa, blit_text, sblit,
                        lookv, sx, sy, st, at):
            """You turned round.

            This is the whole reason LOOK BACK exists. It used to print a
            number -- a readout OF the most frightening thing in the
            encounter, standing in for the thing itself. Now the camera comes
            about, the corridor reverses behind the shader, and it is simply
            there, in the middle of the frame, with nothing in the way and
            nothing to do about it but decide how long you can keep doing this.

            Everything here scales off two values and they pull in opposite
            directions: NEAR (how close it actually is -- the payment) and
            LOOK_FRAC (how long you have held -- the risk).
            """
            near = g.near_frac()
            lf = g.look_frac()

            # THE WHIP. The turn is 15 ticks and it has to cost the eye
            # something, or the camera reads as a cut rather than a head
            # moving. Streaks peak halfway through the swing and are gone by
            # the time it settles.
            swing = 1.0 - abs(lookv - 0.5) * 2.0
            if swing > 0.02 and lookv < 0.995:
                for k in range(9):
                    yy = int((g.tick * 23 + k * 149) % 720)
                    hh = 3 + (k * 7) % 12
                    rv.blit(rect(HOR_PALE + qa(0.10 * swing), 1280, hh),
                            (int(math.sin(k * 1.7) * 120 * swing), yy))

            rv.blit(rect("#000000" + qa(0.62 * lookv), 1280, 720), (0, 0))

            # IT. At arm's length it owns the frame; at a full corridor's
            # distance it is a shape down the far end -- which is its own kind
            # of bad, because you can see how much of it there is.
            zoom = inv_lerp(0.30, 1.05, near) * (1.0 + 0.32 * lf)
            cy = inv_lerp(292.0, 452.0, near) + 26.0 * lf
            self._draw_body(g, rv, tex, sblit, 640, cy, zoom, sx, sy, st, at,
                            warp=1.5 + 1.9 * near + 1.7 * lf,
                            stretch=(1.0 + 0.07 * math.sin(g.clock * 2.1),
                                    1.0 + 0.11 * math.sin(g.clock * 1.3)),
                            diss=0.0, alpha=lookv,
                            swell=0.9 + 1.5 * near + 1.1 * lf,
                            reach=0.8 + 1.4 * near + 1.4 * lf)

            # IT IS GETTING WORSE THE LONGER YOU DO THIS, and it says so with
            # the frame rather than with a word: rings closing on the middle,
            # then the picture starting to come apart.
            if lf > 0.25:
                puls = 0.5 + 0.5 * math.sin(g.tick * (0.22 + 0.5 * lf))
                rings = 3 + int(4 * lf)
                for k in range(rings):
                    rr = 120 + k * 46 - int(70.0 * lf * puls)
                    if rr < 8:
                        continue
                    a = 0.05 + 0.16 * lf * (1.0 - k / float(rings))
                    rv.blit(rect(HOR_BLOOD + qa(a), rr * 2, 2),
                            (640 - rr + sx, 400 - rr + sy))
                    rv.blit(rect(HOR_BLOOD + qa(a), rr * 2, 2),
                            (640 - rr + sx, 400 + rr + sy))
            if lf > 0.55:
                tear = (lf - 0.55) / 0.45
                for k in range(7):
                    yy = int((g.tick * 31 + k * 173) % 720)
                    hh = 2 + int((g.tick + k * 5) % 11)
                    ox = int(math.sin(g.tick * 0.6 + k) * 90 * tear)
                    rv.blit(rect(HOR_PALE + qa(0.16 * tear), 1280, hh),
                            (ox, yy))
                rv.blit(rect(HOR_BLOOD + qa(0.05 + 0.20 * tear), 1280, 720),
                        (0, 0))


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

label archivist_invasion_horror:
    $ hor_deaths = 0
    $ hor_retry = False

label inv_horror_fight:
    $ renpy.block_rollback()

    $ hor_game = HORGame(retry=hor_retry, deaths=hor_deaths,
                        debug=config.developer, start_open=inv_dev_start_open)

    $ _hor_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ _hor_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None
    scene black

    call screen inv_horror_screen(hor_game)
    $ _hor_result = _return

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

    menu:
        "AGAIN":
            scene black
            jump inv_horror_fight

        "STOP":
            if inv_dev_test:
                $ renpy.notify("HORROR: lost. Recorded.")
            return

label inv_horror_quit:
    $ hor_retry = True
    if inv_dev_test:
        $ renpy.notify("HORROR: withdrawn.")
    return
