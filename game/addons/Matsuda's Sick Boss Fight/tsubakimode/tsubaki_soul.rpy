# =============================================================================
# tsubaki_soul.rpy -- "Tsubaki mode": the UNWRITTEN act you reach from
#                      cs_matsuda_02's roster ("I want to fight somebody else.").
# =============================================================================
#
# WHAT THIS IS
#   An Undertale/Deltarune-style box fight against Tsubaki Kareda -- FIGHT /
#   ACT / ITEM / MERCY turns, a red SOUL heart dodging bullet patterns inside a
#   white-bordered box, terse command readouts, the whole liturgy. Played over
#   a Deltarune-grid backdrop that scrolls DOWN hard, so the stage reads as
#   rising forever -- petals and speedlines rushing past like the whole theater
#   is being hoisted on cables. Because it is.
#
# THE CONCEIT (why this mode is allowed to reuse everything)
#   Matsuda never built Tsubaki's fight. The roster slot sat empty with a
#   sticky note on it -- and something else finished it: it grabbed the SOUL
#   sprite and bullet art from Kotonoha's cellar (kotonohamode/player.png
#   etc.), the genre whose debt that mode already acknowledged out loud, and
#   hung Tsubaki in the middle of it on marionette strings. The reuse is left
#   as ambient wrongness, never spelled out as software -- nobody in here
#   says "engine" or "asset." What's on the strings takes Tsubaki's single
#   worst hunger -- picked-last, decided-for, desperate to be somebody's
#   anything -- and gives it exactly what it asked for. She is FULLY
#   possessed: not lucidly resisting, not signalling for rescue, earnestly
#   glad to have been picked up at last. "It" is whatever picked her up;
#   being put back down is her only fear.
#
#   VOICE (rewritten 2026-07-20 -- read this before touching a line)
#   She sounds like a real person who is not okay, not like a bit. Plain
#   sentences, ordinary rhythm, aimed at subject matter nobody should be
#   discussing in that tone. Caps and exclamation marks are rationed to
#   roughly one a line, for the word a person would actually punch --
#   shouting everything reads as cartoon, and that was the failure mode this
#   pass removed. She NEVER names her own wound and never states the theme:
#   she mentions a small concrete thing (the cactus by the sink, the top of
#   her head, somebody's grandmother) and lets the player do the arithmetic.
#   If a line explains her, cut it. The theater lives in the staging -- marks,
#   lamps, the booth -- not in the vocabulary. In the back half she talks
#   about the thing on the other end of the strings the way people defend
#   someone who is bad for them: defensive, certain, keeping score of what it
#   does for her, warning you off the friend who'd talk her out of it. No
#   scripture, no chanting -- every sentence should be one a real person has
#   actually said about somebody.
#
# THREE ENDINGS, ONE PHASE SHIFT (first half / second half)
#   The fight can be resolved by VIOLENCE (FIGHT her HP down), PACIFISM
#   (ACTs build mercy; SPARE when it's earned -- in the second half every
#   earned SPARE spends the WHOLE bar to cut one thread while the grip is
#   lulled, and it clamps back down for the next), or BETRAYAL (pacifism until
#   exactly one string remains, then FIGHT -- which at that point is always
#   a one-hit kill; there is nothing left to resist the blow). Whichever
#   phase-shift threshold is crossed FIRST fires that route's mid-fight
#   cinematic -- and both shifts follow the same motif: it is completely out
#   of Tsubaki's control.
#     * Violence: at half HP she finally gets to fall -- and the strings YANK
#       her back upright mid-kneel. The fight isn't done with her.
#     * Pacifism: she strains toward the SPARE, arms almost down -- and the
#       strings SNAP TAUT and wrench her into the second half.
#   Either way: white flash, the wear-state sprite set crosses into phase 2,
#   and the music crossfades from the instrumental to the IDENTICAL vocal take
#   (tsubaphase1/2.ogg, twin synchro_start channels, Id Mode's trick).
#   After the shift ALL endings remain reachable; the shift only chooses the
#   cinematic and the tone of the back half.
#
#   AND THE OUTCOME IS THE SAME. All three endings converge on the VOID
#   FALL: every graphic in the room -- grid, box, HUD, bullets, strings,
#   bubble -- dies between one frame and the next, and her sprite free-falls
#   to the bottom of the screen under plain gravity (accelerating, crumpling,
#   one dead bounce). Same physics every route. Only the words differ:
#   violence gets NO words (hard cut, strike to drop); pacifist lets her
#   finish the thought; betrayal cuts her off mid-word on the same sentence.
#   The routes change what YOU did, never what happens to her.
#
# THE EMOTIONAL SCREW (kept in her mouth, never a lecture)
#   * ONE VOICE: she is all the way possessed, so the fight is a single
#     performance -- no lowercase "real her" pleading to be freed. Cracks
#     that show are the SHOW glitching (a repeat, a dropped word, a laugh she
#     didn't decide to make, a beat "not in the script"), never her waving
#     for rescue. Lowercase is reserved for the three thresholds where the
#     show isn't running: the intro (before it takes her), the freed ending,
#     and death. Matsuda -- who knew her before -- carries the grief.
#   * CHECK reads ATK 0 -- the readout measures HER, not the thing throwing
#     the volleys. The gap between her claimed authorship of the patterns
#     and that zero is the tell that none of this is hers.
#   * Green needles drift through patterns -- catch one to heal. She hands
#     them over on reflex and papers over it; the one habit the show never
#     managed to rewrite. (Her stories' "needle of noticing," played straight.)
#   * ACTs are off-script kindness, the one input the performance can't
#     parse: each use makes it stutter before it recovers. Mercy progress IS
#     how badly you've jammed the act.
#   * On the violence route the patterns don't escalate near the end -- they
#     fall apart, and she keeps cheering with less and less of her in it.
#   * Dying and retrying is witnessed: your deaths get replayed to her like a
#     highlight reel between shows, and she has to call the reruns a treat.
#   * Camellias everywhere, because tsubaki: they fall whole, head and all.
#   * AND THE ATTACKS ARE STAGE DIRECTIONS. The 2026-08-29 roster rebuild put
#     the theme in the mechanic instead of the names: the room tells you where
#     to stand (limelight, the overture's mark), when to be quiet (feedback),
#     and eventually just takes hold of the SOUL and moves it (marionette).
#     A player who never reads a line of her dialogue still spends the whole
#     fight being staged, which is the only thing that ever happened to her.
#
# ARCHITECTURE (kototouhou.rpy's 60fps pattern, smaller)
#   * TSBGame owns ALL simulation state -- turn machine, menus, bullets, box,
#     scripted cinematics. Pure python dicts/lists, zero displayables.
#   * TSBStage is ONE creator-defined displayable that steps the sim on a
#     fixed 1/60s accumulator inside render() and paints the whole frame as
#     cached-texture blits. The screen tree is static; only the CDD repaints.
#   * The backdrop is one GPU quad (shader tsb.grid): parallax grid layers +
#     hash speedline columns, all scrolling down; registered defensively, the
#     fight runs without it on failure.
#   * Bullet art is Kotonoha's four shipped pixel sprites plus the shared
#     atlas in asset_definitions/def_bullets.rpy -- 25 shapes, every one of
#     them named in TSBStage.KINDS for what it MEANS here (a pin, a stitch, a
#     word, a face in the house, a note off the baton) rather than for what
#     the ripped sheet calls it. All tint/rotation-bucket cached exactly like
#     KTStage; painted art (the notes, the wisp flame) is flagged
#     tintable=False and skips the TintMatrix.
#     SFX ride battle_logic's pooled one-shot channels.
#
# WIRING
#   cs_matsuda_02.rpy -> "I want to fight somebody else." -> "Tsubaki" ->
#   `jump tsubakimode`. Ends with `return`, unwinding back to the archive.
#
# PERSISTENT
#   persistent.tsubamode_attempts : runs started (door patter keys off this).
#   persistent.tsubamode_outcome  : None / "violence" / "pacifist" / "betrayal"
#                                   (last clear).
#   persistent.tsubamode_routes_cleared : exact set of every route cleared.
#   Achievements (catalog in achievements.rpy, all EXPLICIT ach_grant):
#     tsuba_spare     gold  pacifist clear
#     tsuba_violence  gold  violence clear
#     tsuba_betrayal  gold  betrayal clear
#
# READ THIS FIRST IF YOU ARE LOST
#   TSBGame.step() is a mode dispatcher. self.mode is one of:
#     intro   scripted opening (her arm snaps up; music slams in; then
#             CURTAIN UP -- the strongest move first, sans-style, and a
#             syllabus: it teaches every verb the roster will ask for, in
#             order, before the player ever sees the first menu. A house
#             gathers; a mark walks and you are expected to stand on it; a
#             string comes down and takes the SOUL; her five threads close
#             into a cage with one cell in it, and the number ends on a pose.)
#     menu    the four buttons; act/item/mercy submenus hang off it
#     fight   the sweeping accuracy gauge
#     ptext   terse typewriter status pages in the command box
#     etalk   her speech-bubble reply for the turn
#     dodge   the real-time bullet pattern (the only place you can be hit)
#     shift   phase 1 -> 2 cinematic (kind "v" or "p")
#     end_v / end_p / end_b / dead   terminal cinematics -> self.result
#   A turn is: menu -> (action) -> ptext -> etalk -> dodge -> menu.
#   Patterns are _pat_* methods keyed by TSB_TURNS_P1/P2; dialogue lives in
#   the TSB_* tables right above the class so the script is editable without
#   touching the machine.
#
#   Units: screen-space pixels (1280x720), speeds are px per 1/60s tick,
#   timers are ticks unless named _secs. The box is (cx, cy, w, h), floats,
#   lerping toward box_target every tick.
# =============================================================================

# --- AUDIO / STATE DEFAULTS --------------------------------------------------
# First half: instrumental. Second half: the IDENTICAL take with vocals.
# Both start together (synchro_start) on the twin track channels; the phase
# shift is a volume crossfade, never a restart -- Id Mode's phase-3 trick.
define -50 audio.tsb_inst = "<loop 0>assets/audio/bgm/tsubaphase1.ogg"
define -50 audio.tsb_vocal = "<loop 0>assets/audio/bgm/tsubaphase2.ogg"

default persistent.tsubamode_attempts = 0
default persistent.tsubamode_outcome = None
default persistent.tsubamode_routes_cleared = set()

init python:
    def tsb_record_route_clear(route):
        """Persist exact route history without mutating a saved set in place."""
        cleared = set(getattr(persistent, "tsubamode_routes_cleared", None) or ())
        cleared.add(route)
        persistent.tsubamode_routes_cleared = cleared

# Active fight object; only set while tsb_fight_screen runs.
default tsb_game = None

# Result snapshot copied out of TSBGame._finish() -- the interaction returns
# only a small string, so the labels read these to know what happened.
default tsb_last_route = None
default tsb_last_fought = 0
default tsb_last_fight_actions = 0
default tsb_last_deaths = 0
default tsb_last_turns = 0

# Per-visit run state (reset in label tsubakimode, carried across retries).
default tsb_run_deaths = 0
default tsb_retry = False
default tsb_debug = False

# --- SHADER (the rising Deltarune grid + electromagnetic field) --------------
# tsb.grid is one opaque full-screen quad, always the bottom visual layer. Its
# spatial vocabulary runs from long radio undulations through microwave rings,
# infrared heat-folds and the visible prism to fine UV/X-ray ribs and sparse
# gamma needles. Phase 1 lets visible light headline the show; phase 2 crushes
# that rainbow into a bruise-colored seam while the normally invisible bands
# become more legible, faster, and more locally contrasted -- and as the
# endgame closes (each cut thread most of all) every band floods back in at
# once, lifting the room to just short of white. Animation uses an
# accumulated simulation clock, so a changing pace never jumps a wave's phase.
# The two grid layers still scroll DOWNWARD at different speeds (parallax: the
# stage appears to rise), with hashed speedline columns like passing floors.
# Registered defensively like fx.rpy / kototouhou.rpy; on failure the fight
# plays over a plain dark backdrop.
init -9 python:
    TSB_SHADER_OK = False

    def _tsb_register_shaders():
        renpy.register_shader("tsb.grid", variables="""
            uniform vec2 u_tsb_res;
            uniform vec3 u_tsb_col;
            uniform float u_tsb_phase_mix;
            uniform float u_tsb_ems;
            uniform float u_tsb_ems_time;
            uniform float u_tsb_scroll;
            uniform float u_tsb_flash;
            uniform float u_tsb_dark;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float tsb_line(float coord, float spacing, float w) {
                float f = abs(fract(coord / spacing) - 0.5) * spacing;
                return 1.0 - smoothstep(0.0, w, f);
            }
            float tsb_hash(float n) {
                return fract(sin(n * 91.173) * 43758.5453);
            }
            vec3 tsb_spectrum(float h) {
                vec3 wheel = abs(fract(vec3(h) + vec3(0.0, 0.666667, 0.333333)) * 6.0 - 3.0);
                wheel = clamp(wheel - 1.0, 0.0, 1.0);
                return wheel * wheel * (3.0 - 2.0 * wheel);
            }
            float tsb_band(float x, float center, float width) {
                return 1.0 - smoothstep(width * 0.58, width, abs(x - center));
            }
            float tsb_ridge(float x) {
                float a = 0.5 + 0.5 * cos(x);
                a *= a;
                a *= a;
                return a * a;
            }
            float tsb_repeat_y(float y, float period) {
                return (fract(y / period + 0.5) - 0.5) * period;
            }
        """, fragment_300="""
            const float TSB_TAU = 6.2831853;
            vec2 uv0 = v_tex_coord;
            vec2 px = v_tex_coord * u_tsb_res;
            float mood = clamp(u_tsb_phase_mix, 0.0, 1.0);
            float ems = clamp(u_tsb_ems, 0.0, 1.0);
            float endgame = smoothstep(0.5, 1.0, ems);
            float blaze = endgame * endgame;
            float et = u_tsb_ems_time;
            float stage_scroll = max(u_tsb_scroll, 0.0);

            // One phase-safe world displacement unifies the illusion: the
            // stage/camera rises, so every field falls past it. Broad motifs
            // can travel farther per second; high-frequency X/gamma detail is
            // deliberately scaled down to keep line crossings restrained.
            // stage_scroll is the exact integral of the bg_speed scalar used
            // by the wind particles, in seconds-equivalent units.
            float broad_fall = stage_scroll * 0.018;
            float radio_fall = broad_fall * 0.60;
            float micro_fall = broad_fall * 0.75;
            float infra_fall = broad_fall * 0.90;
            float visible_fall = broad_fall;
            float ultra_fall = broad_fall;
            float xray_fall = stage_scroll * 0.0072;
            float gamma_fall = stage_scroll * 0.0045;

            // Wavelength is mapped to spatial scale, never literal flicker.
            // Left-to-right, the structures get finer as wavelength shortens.
            vec2 q = uv0 - vec2(0.5, 0.40);
            q.x *= u_tsb_res.x / u_tsb_res.y;
            float spectrum_x = uv0.x
                + 0.028 * sin(TSB_TAU * (uv0.y * 0.72 - et * 0.010));
            float radio_zone = tsb_band(spectrum_x, 0.04, 0.30);
            float micro_zone = tsb_band(spectrum_x, 0.22, 0.22);
            float infra_zone = tsb_band(spectrum_x, 0.39, 0.19);
            float ultra_zone = tsb_band(spectrum_x, 0.68, 0.18);
            float xray_zone  = tsb_band(spectrum_x, 0.84, 0.17);
            float gamma_zone = tsb_band(spectrum_x, 0.97, 0.18);

            vec2 radio_q = q;
            radio_q.y -= radio_fall;
            float radio = 0.5 + 0.5 * sin(
                TSB_TAU * (dot(radio_q, vec2(0.28, 0.96)) * 1.15 - et * 0.018)
                + 0.72 * sin(TSB_TAU * (radio_q.x * 0.38 + et * 0.008)));
            vec2 micro_q = vec2(q.x, tsb_repeat_y(q.y - micro_fall, 1.0));
            float micro = tsb_ridge(
                TSB_TAU * (length(micro_q) * 7.0 - et * 0.070)
                + 0.45 * sin(micro_q.x * 6.0 + et * 0.11));
            float infra_y = uv0.y - infra_fall;
            float infra = 0.5 + 0.5 * sin(
                TSB_TAU * (infra_y * 1.55 - et * 0.032)
                + 1.05 * sin(TSB_TAU * (uv0.x * 1.10 + et * 0.017)));
            infra = smoothstep(0.16, 0.90, infra);
            vec2 ultra_q = q;
            ultra_q.y -= ultra_fall;
            float ultra = tsb_ridge(
                TSB_TAU * (dot(ultra_q, vec2(5.2, -7.7)) + et * 0.135)
                + sin(ultra_q.x * 5.4 + et * 0.12));
            float xray_y = uv0.y - xray_fall;
            float xray = tsb_ridge(TSB_TAU * (xray_y * 18.0 - et * 0.205));
            xray *= 0.65 + 0.35 * sin(
                TSB_TAU * (uv0.x * 1.35 + et * 0.021));

            // A tiny, sparse false-color gamma scintillator. Randomness is
            // spatial only; time translates and breathes it continuously.
            vec2 gamma_grid = vec2(uv0.x, uv0.y - gamma_fall)
                            * vec2(42.0, 24.0);
            gamma_grid.y -= et * 0.42;
            vec2 gamma_cell = floor(gamma_grid);
            vec2 gamma_uv = fract(gamma_grid) - 0.5;
            float gamma_hash = tsb_hash(dot(gamma_cell, vec2(1.0, 57.0)));
            float gamma_dot = 1.0 - smoothstep(0.035, 0.15, length(gamma_uv));
            float gamma_needle =
                (1.0 - smoothstep(0.018, 0.052, abs(gamma_uv.x)))
                * (1.0 - smoothstep(0.18, 0.43, abs(gamma_uv.y)));
            float gamma = max(gamma_dot, gamma_needle * 0.42)
                * step(0.962 - 0.085 * endgame, gamma_hash)
                * (0.72 + 0.28 * sin(et * 0.42 + gamma_hash * TSB_TAU));

            // Phase 1: two slow spectra cross rather than merely sliding one
            // rainbow over the screen. Their interference supplies the extra
            // pearly cyan / magenta / gold beats between the familiar hues.
            float visible_y = uv0.y - visible_fall;
            float prism_coord = visible_y * 0.84 + uv0.x * 0.24
                            - et * 0.036;
            prism_coord += sin(visible_y * TSB_TAU + et * 0.17) * 0.035;
            vec3 prism_a = tsb_spectrum(prism_coord);
            vec3 prism_b = tsb_spectrum(uv0.x * 0.78
                                    - visible_y * 0.43
                                    + et * 0.025 + 0.17);
            float crossfade = 0.5 + 0.5 * sin((uv0.x - visible_y)
                                            * TSB_TAU + et * 0.14);
            vec3 radiant = vec3(0.014, 0.012, 0.030);
            radiant += prism_a * (0.135 + 0.045 * crossfade);
            radiant += prism_b * (0.035 + 0.025 * (1.0 - crossfade));

            // Even in phase 1 the rest of the spectrum is present, but it is
            // supporting orchestration beneath visible light. It gains force
            // continuously as either route approaches the phase shift.
            float p1_gain = 0.62 + 0.38 * smoothstep(0.0, 0.5, ems);
            vec3 invisible_p1 =
                vec3(0.045, 0.120, 0.340) * radio * radio_zone * 0.055
                + vec3(0.040, 0.400, 0.440) * micro * micro_zone * 0.035
                + vec3(0.620, 0.120, 0.080) * infra * infra_zone * 0.055
                + vec3(0.480, 0.075, 0.840) * ultra * ultra_zone * 0.025
                + vec3(0.250, 0.660, 0.820) * xray  * xray_zone  * 0.020
                + vec3(0.820, 0.780, 0.940) * gamma * gamma_zone * 0.045;
            radiant += invisible_p1 * p1_gain;

            // Phase 2 arrives dark but legible: the hidden spectrum becomes
            // the lead instrument at once, not after a slow warm-up. The
            // visible rainbow survives as a bruised seam -- and every cut
            // thread lets more of it back in, until the whole spectrum is
            // arriving together and the room is one breath short of white.
            float omen_y = uv0.y - infra_fall;
            float omen_a = 0.5 + 0.5 * sin((omen_y * 0.96
                                            + uv0.x * 0.18) * TSB_TAU
                                            - et * 0.33);
            float omen_b = 0.5 + 0.5 * sin((uv0.x * 0.54
                                            - omen_y * 0.47) * TSB_TAU
                                            + et * 0.24 + 1.8);
            vec3 stygian = mix(vec3(0.007, 0.008, 0.019),
                                vec3(0.058, 0.009, 0.024),
                                smoothstep(0.12, 0.92, omen_a));
            stygian += vec3(0.010, 0.018, 0.052)
                        * smoothstep(0.22, 0.96, omen_b);
            float altar = 1.0 - smoothstep(0.08, 0.68,
                length((v_tex_coord - vec2(0.5, 0.40)) * vec2(0.78, 1.0)));
            stygian += vec3(0.026, 0.004, 0.014) * altar;
            // The bruised seam of visible light widens as threads are cut:
            // freeing her literally lets the rainbow back into the room.
            float slit_y = tsb_repeat_y(q.y - visible_fall, 1.0);
            float visible_slit = 1.0 - smoothstep(0.025, 0.13 + 0.36 * endgame,
                abs(slit_y - 0.065 * sin(q.x * 7.0 - et * 0.16)));
            vec3 visible_current = prism_a * 0.135 + prism_b * 0.045;
            stygian += visible_current * vec3(0.34, 0.12, 0.42)
                        * (0.12 + 0.28 * visible_slit);
            stygian += (prism_a * 0.17 + prism_b * 0.06)
                        * (0.55 * endgame + 1.75 * blaze);

            vec3 invisible_p2 =
                    vec3(0.025, 0.045, 0.120) * radio * radio_zone
                    * (0.135 + 0.075 * endgame)
                + vec3(0.018, 0.110, 0.130) * micro * micro_zone
                    * (0.100 + 0.070 * endgame)
                + vec3(0.300, 0.045, 0.060) * infra * infra_zone
                    * (0.135 + 0.095 * endgame)
                + vec3(0.200, 0.035, 0.320) * ultra * ultra_zone
                    * (0.075 + 0.105 * endgame)
                + vec3(0.150, 0.200, 0.270) * xray * xray_zone
                    * (0.055 + 0.095 * endgame)
                + vec3(0.420, 0.470, 0.550) * gamma * gamma_zone
                    * (0.105 + 0.135 * endgame);
            // Exposure opens from ~2.6x at entry to ~4.8x at the finish.
            // Because the ingredients are localized ridges, rings, and
            // sparse points, this raises legibility and contrast without
            // turning the whole screen into a luminance pulse.
            float p2_exposure = 2.55 + 2.25 * endgame;
            stygian += invisible_p2 * p2_exposure;

            // The blaze: past the midpoint every band starts arriving at
            // once. The wash rides a slow spatial field, so brightness only
            // climbs monotonically with progress -- it never strobes.
            float blaze_field = 0.62 + 0.38
                * sin(TSB_TAU * (uv0.y * 0.42 - broad_fall * 0.6) + et * 0.11)
                * sin(TSB_TAU * (uv0.x * 0.31) + et * 0.07);
            stygian += vec3(0.92, 0.90, 0.97) * blaze * blaze_field * 0.85;

            // Local contrast may climb, but only the endgame blaze is allowed
            // to lift the ceiling -- and even then it stops short of white.
            radiant = min(radiant, vec3(0.34));
            stygian = min(stygian, vec3(0.34 + 0.60 * blaze));

            // The grid consumes the same integrated displacement. Coefficients
            // preserve its established far/near speeds at the opening while
            // allowing the route-driven climb to intensify without a teleport.
            float far_h  = tsb_line(px.y - stage_scroll * 260.0, 96.0, 1.4) * 0.10;
            float near_h = tsb_line(px.y - stage_scroll * 760.0, 152.0, 2.2) * 0.20;
            float wob = sin((px.y - stage_scroll * 260.0) * 0.006
                            + stage_scroll * 1.6) * 5.0;
            float far_v  = tsb_line(px.x + wob, 96.0, 1.4) * 0.075;
            float near_v = tsb_line(px.x, 152.0, 2.2) * 0.11;

            // Hashed speedline columns: sparse bright dashes falling fast.
            float col = floor(px.x / 22.0);
            float h = tsb_hash(col);
            float sy = fract(px.y / u_tsb_res.y
                            - stage_scroll * (1.45 + h * 2.25) - h * 7.31);
            float streak = smoothstep(0.88, 1.0, sy) * step(0.78, h) * 0.34;

            float glow = far_h + near_h + far_v + near_v + streak;
            vec3 base = mix(radiant, stygian, mood);
            // Prismatic grid-light in phase 1 resolves into the existing
            // heartbeat-red accent in phase 2. Camellia red remains the
            // through-line even while phase 1's local spectrum catches it.
            vec3 grid_prism = prism_a * 0.78 + prism_b * 0.22;
            vec3 grid_col = mix(u_tsb_col * 0.84 + grid_prism * 0.16,
                                u_tsb_col, mood);
            grid_col = mix(grid_col, vec3(0.95, 0.93, 0.99),
                            mood * blaze * 0.7);
            vec3 colr = base + grid_col * glow * mix(1.0, 0.80, mood);

            // Vignette, then the scripted white flash / ending darkness.
            vec2 uv = v_tex_coord - 0.5;
            float vig = 1.0 - dot(uv, uv)
                * mix(0.82, mix(1.12, 0.38, blaze), mood);
            colr *= max(vig, 0.0);
            colr = min(colr, vec3(0.58 + 0.34 * mood * blaze));
            colr = mix(colr, vec3(0.96, 0.95, 0.94), clamp(u_tsb_flash, 0.0, 1.0));
            colr *= (1.0 - clamp(u_tsb_dark, 0.0, 1.0));
            gl_FragColor = vec4(colr, 1.0);
        """)

    try:
        _tsb_register_shaders()
        TSB_SHADER_OK = True
    except Exception as _tsb_sh_e:
        TSB_SHADER_OK = False
        try:
            renpy.log("TSB FX: shader registration failed: %r" % _tsb_sh_e)
        except Exception:
            pass

# --- CONSTANTS / TUNING / SCRIPT TABLES --------------------------------------
init python:
    import math
    import random as tsb_random
    try:
        import pygame_sdl2 as tsb_pg
    except Exception:
        tsb_pg = None

    class TSBLineartMatrix(ColorMatrix):
        """Turn the shipped black-backed grayscale poses into true alpha.

        Unlike additive compositing, this color transform also works under
        Matsu'Py's software renderer and preserves tinted fall echoes.
        """
        def get(self, value):
            return Matrix([
                1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.2126, 0.7152, 0.0722, 0.0,
            ])

    TSB_LINEART_MATRIX = TSBLineartMatrix()

    TSB_DIR = "addons/Matsuda's Sick Boss Fight/tsubakimode/"
    # The reuse is the point: the SOUL heart and the bullet art are borrowed
    # deliberately as shared visual grammar. The bullet sprites now come from
    # assets/bullets/ via EMB_DIR (def_bullets.rpy); TSB_KT_DIR is only
    # still here for Kotonoha's SHIP sprite, which this mode draws as the soul.
    TSB_KT_DIR = "addons/Matsuda's Sick Boss Fight/kotonohamode/"
    TSB_KT_SE = "assets/audio/sfx/touhou/"
    TSB_MSBF_SFX = "assets/audio/sfx/msbf/"

    TSB_TICK = 1.0 / 60.0
    TSB_MAX_CATCHUP = 4
    TSB_PATTERN_WARMUP = 18

    # Board geometry (screen space). The box lerps between a wide menu shape
    # and per-pattern dodge shapes, UT-style.
    TSB_BOX_CX = 640.0
    TSB_BOX_CY = 442.0
    TSB_MENU_W = 640.0
    TSB_MENU_H = 152.0
    TSB_DODGE_W = 320.0
    TSB_DODGE_H = 264.0
    TSB_BORDER = 4          # box border thickness
    TSB_BOSS_X = 640.0      # boss sprite anchor (feet center)
    TSB_BOSS_FEET_Y = 352.0
    TSB_BOSS_ZOOM = 1.0
    # All five refreshed poses share one tightly cropped, four-tone pixel cell.
    # (92, 334) is the lower-body/sole registration point produced by
    # tools/process_tsubaki_boss_sprites.py.
    TSB_BOSS_NATIVE_SIZE = (184.0, 344.0)
    TSB_BOSS_BASELINE = (92.0, 334.0)
    TSB_BOSS_ASSETS = {
        "p1_clean":     ("phase1.png", 0),
        "p1_strained":  ("phase1_strained.png", 1),
        "p2_strained":  ("phase2.png", 2),
        "p2_exhausted": ("phase2_exhausted.png", 3),
        "p2_limp":      ("phase2_limp.png", 4),
    }
    # Per-pose pixel anchors: viewer-right wrist, viewer-left wrist, head,
    # shoulder, middle back. The external strings are drawn by the renderer.
    TSB_STRING_ANCHORS = {
        "p1_clean": [(141.0, 149.0), (54.0, 166.0), (97.0, 18.0),
                     (71.0, 79.0), (99.0, 106.0)],
        "p1_strained": [(142.0, 149.0), (52.0, 170.0), (91.0, 14.0),
                        (68.0, 71.0), (94.0, 100.0)],
        "p2_strained": [(145.0, 135.0), (60.0, 104.0), (69.0, 25.0),
                        (102.0, 67.0), (83.0, 103.0)],
        "p2_exhausted": [(133.0, 143.0), (60.0, 108.0), (65.0, 30.0),
                         (96.0, 70.0), (80.0, 105.0)],
        "p2_limp": [(128.0, 159.0), (65.0, 160.0), (61.0, 41.0),
                    (99.0, 73.0), (82.0, 111.0)],
    }

    # Player SOUL. 20 HP, UT-honest: five clean hits end you.
    TSB_PLAYER_R = 6.0
    TSB_MOVE = 3.7
    TSB_MOVE_SLOW = 1.85
    TSB_HP_MAX = 20.0
    TSB_INV_TICKS = 50

    # Boss / routes.  She is a superboss; violence should be a real grind
    # (~25-30 landed hits), so HP is high relative to the FIGHT gauge.  [TUNE]
    TSB_BOSS_HP = 1600.0
    TSB_PHASE2_HP = 800.0   # violence shift threshold (half)
    TSB_MERCY_NEED = 6      # phase-1 ACT progress needed before SPARE counts
    TSB_SPARES_NEED = 3     # counted phase-1 spares -> pacifist shift
    TSB_MERCY2_NEED = 3     # phase-2 ACT progress per thread; a SPARE spends it
    TSB_SPARES2_NEED = 5    # one committed SPARE per visible string
    TSB_LIMP_HP = 300.0     # below this the violence route stops fighting back

    def tsb_boss_asset_key(game):
        """Pick a non-regressing wear pose for every route and launch mode."""
        progress = max(0.0, min(1.0,
            float(getattr(game, "ems_progress", 0.0))))
        if int(getattr(game, "boss_img", 1)) == 1:
            return "p1_strained" if progress >= 0.20 else "p1_clean"

        mode = getattr(game, "mode", "")
        ending = (getattr(game, "end_flag", None) is not None
                  or mode in ("end_v", "end_p", "end_b")
                  or bool(getattr(game, "void", False)))
        cut_ids = getattr(game, "cut_string_ids", ()) or ()
        cuts = max(int(getattr(game, "strings_cut", 0)),
                   len(cut_ids))
        if (ending or cuts >= 4
                or (getattr(game, "phase", 1) == 2
                    and float(getattr(game, "boss_hp", TSB_BOSS_HP))
                    <= TSB_LIMP_HP)
                or progress >= 0.86):
            return "p2_limp"
        if cuts >= 2 or progress >= 0.68:
            return "p2_exhausted"
        return "p2_strained"

    def tsb_boss_motion(game):
        """Deterministic breathing and string-driven motion for one frame.

        Everything is derived from existing simulation state, so old saves and
        rollback do not need new serialized fields. Breathing is quantized to
        five steps to keep the Transform cache bounded and preserve pixel art.
        """
        asset_key = tsb_boss_asset_key(game)
        filename, wear = TSB_BOSS_ASSETS[asset_key]
        tick = int(getattr(game, "tick", 0))
        mode = getattr(game, "mode", "")
        pose_frozen = (mode in ("end_v", "end_p", "end_b", "dead")
                       or bool(getattr(game, "void", False))
                       or bool(getattr(game, "boss_fallen", False)))
        motion_frozen = pose_frozen or mode == "shift"

        breath_bucket = 0
        if not pose_frozen:
            periods = (173, 149, 127, 103, 91)
            period = periods[wear]
            phase = (tick % period) / float(period)
            if wear < 2:
                breath = 0.5 - 0.5 * math.cos(phase * math.pi * 2.0)
            elif phase < 0.24:
                u = phase / 0.24
                breath = u * u * (3.0 - 2.0 * u)
            else:
                u = (phase - 0.24) / 0.76
                u = u * u * (3.0 - 2.0 * u)
                breath = 1.0 - u
            # Late gasps interrupt the regular cycle without adding new art.
            if wear >= 3:
                gasp_age = (tick + 31 * wear) % 167
                if gasp_age < 17:
                    breath = max(breath,
                        math.sin(gasp_age / 17.0 * math.pi))
            breath_bucket = max(0, min(4, int(round(breath * 4.0))))

        breath = breath_bucket / 4.0
        x_amp = (0.004, 0.007, 0.009, 0.012, 0.007)[wear]
        y_amp = (0.006, 0.010, 0.013, 0.017, 0.010)[wear]
        scale_x = TSB_BOSS_ZOOM * (1.0 + x_amp * breath)
        scale_y = TSB_BOSS_ZOOM * (1.0 + y_amp * breath)

        puppet_dx = 0.0
        puppet_dy = 0.0
        puppet_rot = 0.0
        strings_live = float(getattr(game, "strings_alpha", 0.0)) > 0.06
        cut_ids = getattr(game, "cut_string_ids", ()) or ()
        if not motion_frozen and strings_live:
            periods = (281, 233, 197, 163, 137)
            period = periods[wear]
            offset_tick = tick + 37 * wear
            age = offset_tick % period
            pull = 0.0
            if age < 3:
                pull = 1.0 - age / 3.0
            elif age < 18:
                u = (age - 3) / 15.0
                pull = -0.28 * math.sin(u * math.pi) * (1.0 - u)
            cycle = offset_tick // period
            direction = -1.0 if cycle % 2 else 1.0
            held = max(0, 5 - len(cut_ids))
            control = 0.0 if held == 0 else 0.70 + 0.06 * held
            puppet_dx = direction * (0.6 + 0.65 * wear) * pull * control
            puppet_dy = -(1.4 + 1.55 * wear) * pull * control
            puppet_rot = direction * (0.8 + 0.72 * wear) * pull * control

        ending = mode in ("end_v", "end_p", "end_b")
        bob = 0.0 if motion_frozen or ending else (
            math.sin(tick * (0.026 if wear >= 2 else 0.031))
            * (0.65 if wear >= 2 else 0.45))
        idle_rot = 0.0 if motion_frozen else (
            math.sin(tick * 0.019) * (0.25 + 0.12 * wear))

        hit_age = tick - int(getattr(game, "slash_born", -9999))
        hit_rot = 0.0
        hit_dx = 0.0
        if 0 <= hit_age < 24 and not getattr(game, "boss_fallen", False):
            hit_pulse = math.sin(hit_age / 24.0 * math.pi)
            hit_rot = -7.0 * hit_pulse
            hit_dx = 15.0 * hit_pulse

        shake_x = 0.0
        shake_y = 0.0
        shake = int(getattr(game, "shake", 0))
        if shake > 0:
            shake_x = math.sin(tick * 1.7) * min(6.0, shake * 0.4)
            shake_y = math.cos(tick * 2.3) * min(4.0, shake * 0.3)

        native_w, native_h = TSB_BOSS_NATIVE_SIZE
        baseline_x, baseline_y = TSB_BOSS_BASELINE
        drawn_w = native_w * scale_x
        drawn_h = native_h * scale_y
        center_x = (TSB_BOSS_X + float(getattr(game, "boss_dx", 0.0))
                    + hit_dx + shake_x + puppet_dx
                    + drawn_w * 0.5 - baseline_x * scale_x)
        center_y = (TSB_BOSS_FEET_Y + float(getattr(game, "boss_dy", 0.0))
                    + bob + shake_y + puppet_dy
                    + drawn_h * 0.5 - baseline_y * scale_y)
        return {
            "asset_key": asset_key,
            "path": TSB_DIR + filename,
            "wear": wear,
            "breath_bucket": breath_bucket,
            "scale_x": scale_x,
            "scale_y": scale_y,
            "drawn_w": drawn_w,
            "drawn_h": drawn_h,
            "center_x": round(center_x),
            "center_y": round(center_y),
            # Quantize once so the sprite and all five string anchors rotate
            # by exactly the same pixel-art-friendly angle.
            "rotation": float(round(
                float(getattr(game, "boss_rot", 0.0))
                + idle_rot + hit_rot + puppet_rot)),
            "anchors": TSB_STRING_ANCHORS[asset_key],
        }

    # FIGHT gauge: sweep duration in ticks; damage from strike accuracy.
    TSB_FIGHT_SWEEP = 100
    TSB_DMG_BASE = 26
    TSB_DMG_SPAN = 44
    TSB_CRIT_ACC = 0.93

    # Bullets.
    # The new roster favors formations over raw curtains.  This ceiling is a
    # safety valve, not a target; the busiest pattern sits well below it.
    TSB_MAX_BULLETS = 340
    TSB_MAX_SPARKS = 180
    TSB_ROT_BUCKETS = 24
    TSB_ROT_DEG = 360.0 / TSB_ROT_BUCKETS
    TSB_HEAL_HP = 1.0   # she can only give you a stitch at a time

    # Palette (indexes are cache keys, same discipline as KT_PAL).
    TSB_PAL = [
        "#e13b4e",  # 0 camellia red
        "#ff8fb8",  # 1 pink
        "#f5f5f0",  # 2 bone white
        "#39d97e",  # 3 mend green
        "#ff9c3d",  # 4 UT button orange
        "#e8e4ff",  # 5 wire white-violet
        "#a01824",  # 6 deep red
        "#8a90a0",  # 7 grey
        "#ffe23d",  # 8 spare yellow
        "#5cd7ff",  # 9 cyan
    ]

    # Ambient petals/streaks use the same semantic indexes, but a lifted
    # presentation palette. Their old 30%-alpha gameplay tints let the opaque
    # shader show through so strongly that they read as being behind it even
    # though they are drawn afterward.
    TSB_AMB_PAL = [
        "#ff5265",  # 0 bright camellia
        "#ffb4cf",  # 1 petal pink
        "#ffffff",  # 2 white glint
        "#62f29d",  # 3 green
        "#ffb16a",  # 4 orange
        "#ffffff",  # 5 wire white
        "#d72b3e",  # 6 dark-phase red, lifted out of the background
        "#c0c8d8",  # 7 cold ash
        "#fff06a",  # 8 yellow
        "#7be5ff",  # 9 cyan
    ]

    TSB_FONT = "assets/fonts/Myanmar.otf"           # flavor / bubbles
    TSB_FONT_UI = "assets/fonts/NovaSquare-Regular.ttf"  # HUD / buttons

    # Music channels (registered in def_audio.rpy; Id Mode uses the same pair).
    TSB_INST_CH = "track1"
    TSB_VOCAL_CH = "track2"
    TSB_VOCAL_FADEIN = 0.9
    TSB_INST_BED = 0.18
    TSB_INST_DUCK_AT = 1.45

    def tsb_music_start():
        try:
            renpy.music.set_volume(1.0, delay=0.0, channel=TSB_INST_CH)
            renpy.music.set_volume(0.0, delay=0.0, channel=TSB_VOCAL_CH)
            renpy.music.play(audio.tsb_inst, channel=TSB_INST_CH, loop=True,
                            fadeout=0.0, fadein=0.0, synchro_start=True)
            renpy.music.play(audio.tsb_vocal, channel=TSB_VOCAL_CH, loop=True,
                            fadeout=0.0, fadein=0.0, synchro_start=True)
        except Exception:
            pass

    def tsb_music_vocal():
        # The crossfade: vocals swell in, the instrumental drops to a bed.
        try:
            renpy.music.set_volume(1.0, delay=TSB_VOCAL_FADEIN, channel=TSB_VOCAL_CH)
            renpy.music.set_volume(TSB_INST_BED, delay=TSB_INST_DUCK_AT, channel=TSB_INST_CH)
        except Exception:
            pass

    def tsb_music_stop(fadeout=1.5):
        for _ch in (TSB_INST_CH, TSB_VOCAL_CH):
            try:
                renpy.music.stop(channel=_ch, fadeout=fadeout)
            except Exception:
                pass

    # SFX: (path, base volume). One-shots ride battle_logic's pooled channels
    # so overlapping cues don't cut each other off.
    TSB_SFX = {
        "move":    (TSB_KT_SE + "se_select00.wav", 0.50),
        "confirm": (TSB_KT_SE + "se_ok00.wav", 0.65),
        "cancel":  (TSB_KT_SE + "se_cancel00.wav", 0.55),
        "denied":  (TSB_MSBF_SFX + "ui_denied.wav", 0.70),
        # Two voices, two blips: the machine's readouts vs. her bubbles.
        "blip":      (TSB_MSBF_SFX + "uiblip.wav", 0.50),
        "tsubablip": (TSB_MSBF_SFX + "tsubablip.wav", 0.55),
        "hurt":    (TSB_MSBF_SFX + "hit.wav", 0.90),
        "heal":    (TSB_MSBF_SFX + "heal.wav", 0.80),
        "slash":   (TSB_KT_SE + "se_slash.wav", 0.90),
        "crit":    (TSB_MSBF_SFX + "crit.wav", 0.90),
        "miss":    (TSB_MSBF_SFX + "miss.wav", 0.80),
        "wire":    (TSB_KT_SE + "se_lazer00.wav", 0.50),
        "bloom":   (TSB_KT_SE + "se_tan00.wav", 0.45),
        "dagger":  (TSB_KT_SE + "se_kira01.wav", 0.40),
        # Volley voices, so no pattern fires silently: "volley" is a wall/lane
        # launch, "volley2" an aimed commit, "throw" the metered tick of a
        # continuous stream (always rate-limited to every Nth emission),
        # "glint" a head or formation materializing, "release" a delayed
        # formation letting go (fired once per tick from _step_bullets).
        "volley":  (TSB_MSBF_SFX + "bullet01.ogg", 0.50),
        "volley2": (TSB_MSBF_SFX + "bullet02.ogg", 0.50),
        "throw":   (TSB_KT_SE + "se_gun00.wav", 0.34),
        "glint":   (TSB_KT_SE + "se_kira00.wav", 0.40),
        "release": (TSB_KT_SE + "se_kira02.wav", 0.50),
        "mend":    (TSB_KT_SE + "se_item00.wav", 0.40),
        "snap":    (TSB_KT_SE + "se_slash.wav", 1.00),
        "fall":    (TSB_MSBF_SFX + "down.wav", 0.90),
        "break":   (TSB_KT_SE + "se_pldead00.wav", 0.90),
        "phase":   (TSB_MSBF_SFX + "phase.wav", 0.90),
        "spare":   (TSB_KT_SE + "se_cardget.wav", 0.80),
        "pause":   (TSB_KT_SE + "se_pause.wav", 0.60),
    }

    def tsb_play(name, volume_scale=1.0):
        entry = TSB_SFX.get(name)
        if not entry:
            return
        try:
            msbf_play_pooled_sfx(entry[0], volume=entry[1] * volume_scale)
        except Exception:
            pass

    def tsb_clamp(v, lo, hi):
        return max(lo, min(hi, v))

    # ---- CHOREOGRAPHY --------------------------------------------------------
    # The difference between a volley and a dance is that a dance is SOMEWHERE
    # and going somewhere else. A random draw across the box tells the player
    # nothing about the next one, so the only correct play is to stand in the
    # emptiest place and react; a hazard that WALKS tells you where it will be
    # in a second, so the correct play is to walk with it. Everything in this
    # fight that used to pick a spawn out of a hat now rides one of these two.
    def tsb_tri(p):
        # Triangle wave: 0 -> 1 -> 0 over one unit of p. The bones of every
        # sweep in the fight -- there and back, so the figure closes.
        p = p % 1.0
        return p * 2.0 if p < 0.5 else (1.0 - p) * 2.0

    def tsb_sweep(t, period, lo, hi, phase=0.0):
        # A position that paces between lo and hi with period `period` ticks,
        # turning at each end. Feed it a spawn coordinate and a rain becomes a
        # curtain with a direction.
        return lo + (hi - lo) * tsb_tri(t / float(period) + phase)

    # Screen-poll helper (see kototouhou.rpy): a slow timer calls this; a
    # non-None return ends the interaction with that value.
    def tsb_poll_result(game):
        return game.result

    # ---- SCRIPT TABLES -------------------------------------------------------
    # All authored text lives here so the fight can be rewritten without
    # touching the state machine. The voice is one possessed performance (see
    # VOICE and THE EMOTIONAL SCREW in the header): a real person talking
    # calmly and specifically about things nobody should be calm about,
    # glitching when off-script kindness lands, never lucidly pleading for
    # rescue. Lowercase is only for the threshold beats.

    # THE ROSTER. Rebuilt 2026-08-29 -- see the long block above the _pat_*
    # methods for why, and for the rule every entry below is built on: a move
    # has to ask a VERB that isn't "avoid."
    #
    #   (pattern id, duration ticks, density multiplier)
    #
    # ORDER IS A SHUFFLE BAG, not a sequence (see _draw_pattern): every move
    # appears once per bag in a fresh random order, none repeats back to back
    # across a reshuffle, and a mild density creep rides each completed bag.
    # Dialogue is keyed to the TURN, not to the pattern, so the monologue
    # stays a monologue however the deck falls.
    #
    # PHASE 1 -- the production is competent. These moves repeat, they are
    # legible, and they can be LEARNED, which is the whole difference between
    # the two halves of this fight. Six of them come back in phase 2 damaged;
    # five play only here, while the show still runs clean.
    TSB_TURNS_P1 = [
        # -- shared: taught here, broken later ---------------------------
        ("camellia",    440, 1.06),  # heads on a rail; a travelling run
        ("hemline",     450, 1.06),  # a running stitch, and then the pull
        ("metronome",   450, 1.06),  # the baton, the tock, the downbeat
        ("limelight",   450, 1.08),  # the lit circle is the SAFE one
        ("ovation",     440, 1.06),  # claps off the rim; she flinches
        ("understudy",  450, 1.06),  # your reflection learns your part
        # -- phase 1 only ------------------------------------------------
        ("footlights",  440, 1.08),  # six lamps played as a repeating phrase
        ("programme",   460, 1.06),  # a page writes itself and strikes out
        ("curtaincall", 470, 1.06),  # the ceiling comes in; then the bow
        ("pincushion",  440, 1.08),  # a turning hedgehog, then the pull
        ("garland",     450, 1.06),  # one long rope, and the room silts up
    ]

    # PHASE 2 -- nothing back here repeats the same way twice, and every
    # single thing back here still telegraphs. That is the line: the second
    # half is DISORDER, never surprise damage. All of the disorder is decided
    # at telegraph time, so it reads as damage rather than as a cheat.
    TSB_TURNS_P2 = [
        # -- the six, damaged --------------------------------------------
        ("camellia",    460, 1.16),  # broken chord; the burst throws upward
        ("hemline",     470, 1.16),  # a cross seam, gathered onto your mark
        ("metronome",   470, 1.14),  # fermata, and the cutoff that holds
        ("limelight",   470, 1.16),  # the spot shrinks the whole time it is lit
        ("ovation",     460, 1.16),  # the flinch comes BEFORE the clap
        ("understudy",  470, 1.14),  # the reflection plays you back on a delay
        # -- phase 2 only ------------------------------------------------
        ("marionette",  470, 1.12),  # hooks take the SOUL. Pull to break them
        ("feedback",    460, 1.10),  # too loud to move. Hold still
        ("recast",      450, 1.16),  # the room will not hold a shape
        ("unravel",     460, 1.16),  # a zipper runs the seam of a half-room
        ("chandelier",  480, 1.14),  # one heavy thing on one fraying line
        ("blackout",    470, 1.10),  # the lights go. Go and fetch the light
        ("tableau",     470, 1.14),  # intermission: the frozen picture lets go
    ]

    # Her bubble for each phase-1 turn: (neutral line, line if you hit her
    # last turn). One entry per TSB_TURNS_P1 row, read as a single continuous
    # monologue. VOICE RULES, and they are load-bearing:
    #   * She is a person, not a bit. Ordinary sentences, ordinary rhythm,
    #     aimed at wildly inappropriate subject matter. The unhinged part is
    #     WHAT she says and how calmly she says it -- never the volume.
    #   * Caps and exclamation marks are rationed to roughly one a line, for
    #     the word a real person would actually punch. Shouting everything
    #     reads as cartoon, which is the failure mode this pass fixed.
    #   * She never names her own wound. No "nobody ever picked me," no
    #     "that's almost like being loved." She mentions a small concrete
    #     thing -- a coat, a bus, the top of her head -- and lets the player
    #     do the arithmetic. If a line explains her, cut it.
    #   * The theater stays in the staging (marks, lamps, the booth), not in
    #     the vocabulary. She can be "on" without saying "leading lady."
    #   * "It" is whatever picked her up. She talks about it the way people
    #     talk about someone who got them out of a bad stretch: defensive,
    #     grateful, faintly threatening if you push. Her one fear is being
    #     put back down.
    # Some entries are lists: extra bubbles she fires before the dodge (see
    # _bub). Hit variants are the worst of it -- she thanks you for it.
    TSB_BUBBLES_P1 = [
        (["We opened with the closer. The big one, first, everything at once -- I asked for that. I said do the big one first and it said okay. It says okay to me now.",
        "You're still standing there. Most people would be doing something else by now.",
        "Sorry. I'm talking a lot. I've had a very quiet couple of months and it's all coming out at the wrong speed."],
        "Ow. ...ow! No -- no, that's fine, that's the job, you're allowed. I wanted you to know you're allowed. In case you were being careful on my account."),
        ("Don't make that face at me. I know that face. That's the face people make right before they remember somewhere else they have to be.",
        "My eyes are doing a thing again. Ignore it. The lights are very close. They've been very close for a while now."),
        ("There was a girl in here before me who apologized for the weather. For other people's spilled drinks. For standing in a doorway. She doesn't come up anymore. I don't miss her. ...I don't.",
        "It told me this part gets easier. It's been right about everything else so far, so. So it's probably right about this. It's got a good record with me."),
        ("Matsu's shouting through the wall again. Tell her I'm fine. Tell her I got the thing I wanted -- she'll know the one, she made a face about it once and I never forgot the face.",
        "Why does she sound like that? She sounds like she did at her grandmother's. Tell her to stop. I can do her voice now, exactly, I've been practicing -- I'd still rather hear hers."),
        (["Five. Both wrists, the shoulder, the top of my head, and one through the back. I counted them in the dark the first night until they stopped being frightening.",
        "Nobody has ever needed the top of my head before. That's a first. I've been keeping a list of firsts."],
        "The left wrist comes a half-beat la-- no. No, forget that, I didn't say a number, there wasn't a number. Everything's on time. We're on time."),
        ("Look at all the flowers. I have never kept one thing alive, not a fish, not the little cactus by the sink, and these can't die. It checked for me. It checks things for me.",
        "You knocked some loose. That's all right. Nothing that falls in here goes to waste -- it collects them afterward. It keeps everything I drop."),
        (["Oh -- there's a green one in there. Take it. Take it quick, before the pattern closes up.",
        "...huh. I keep doing that. I don't decide to. Anyway -- eyes up. This next bit's worth watching."],
        "Take the green one, go on. I'm allowed to hand things to people. It's allowed. I checked twice, so it's allowed."),
        ("I've been watching your feet the whole time. I know where you're going about a half-second before you do. It's my one trick and nobody's ever had a use for it before.",
        "Your hands were shaking before you even swung. I see everything from up here. I never have to look away -- I couldn't if I wanted to, so it's lucky that I want to."),
        ("Nobody used to watch me do anything. Now you can't leave the room. I keep checking that you can't. Every few seconds. It's become sort of a hobby.",
        "From up here, hitting somebody and holding onto somebody look about the same. Same arms, same distance. I'm not being clever. They genuinely look the same."),
        ("I haven't said sorry in eleven turns. Eleven. It reached in and fixed that, it just -- sor-- oh. That one got out. Doesn't count. Restart the count. Eleven again.",
        "That didn't hurt. I'm not -- it didn't. Put a pin in it, we'll come back to it later. Nobody saw."),
        ("My hands don't shake anymore. Not even slightly. Steady hands and brave are basically the same thing from a distance, and everybody's at a distance.",
        "I know the difference. Between brave and held still, I -- I know it, I'm not -- what were we -- I know the difference. Next."),
        ("This next one's my favorite. I've never had a favorite anything, nobody asked, so I picked one myself and it's this one. Don't ruin it. Do your part properly.",
        "You're rushing my favorite part. Slow down. It comes around once a night and it's the only thing in this room I chose."),
    ]
    TSB_LOOP_P1 = [
        "There's room for one more up here. Loads of room. You wouldn't even have to talk, I'd handle the talking, I've got it covered.",
        "It's not that loud once you stop pulling against it. It is loud. But it's a good loud. It's the kind you can stand.",
        "Left wrist, back, both wrists, crown. There's a rhythm to it once you learn it. I can't stop counting it. I've tried stopping.",
        "If you're waiting for me to get tired -- no. It doesn't let me. I sleep standing up now, apparently. Apparently that's a thing I can do.",
    ]

    # Phase-2 bubbles: (neutral, lean when she's been hit / is low). The yank
    # doesn't make her louder, it makes her CERTAIN. Back half she talks about
    # the thing on the other end of the strings exactly the way a person
    # defends someone who is bad for them: you don't know it like I do, it's
    # not like that, everyone told me it was a mistake and look at me now.
    # No scripture, no chanting, no capital-letter fervor -- that was the old
    # register and it read as cosplay. The horror is that every sentence is
    # something a real person has actually said about someone. She isolates
    # herself from Matsuda, keeps score of what it does for her, and gets
    # defensive rather than devout. Lean variants dig in HARDER instead of
    # cracking; her one fear is being put back down, never being controlled.
    # Some entries are lists (extra bubbles).
    TSB_BUBBLES_P2 = [
        ("Did you see that? I went down and it caught me. It always catches me. Everybody kept telling me it wouldn't, and it does, every time, so who was right.",
        "Thank you. I'm saying it to it, not to you. I say it a lot now. I say it in my sleep, apparently. Matsu would think that was funny. She wouldn't think it was funny."),
        ("Five. I say them out loud every turn so it knows I've still got them all straight. Both wrists, shoulder, crown, back. I don't lose count. I have never lost count.",
        "Four -- no. Five. It's five. I don't get that wrong, I've never once gotten that wrong, don't look at me like I got it wrong."),
        (["It gave me a voice for the second half. Listen to it. That isn't a recording, that's a room full of -- I don't actually know what that is. It's lovely, though.",
        "There's more of it in me than me now. Which is fine. There wasn't much of the other thing and it wasn't doing anything with the space."],
        "There's more of it than me in here and I want that on the record as my idea. I asked for it. Nobody made me ask for it."),
        ("I remember the door with the light over it. I walked through on my own feet, chin up. ...I don't remember the walking part. But it was my idea. It was definitely my idea.",
        "It needs me to have picked it. And I did pick it. I'd pick it again. Ask me in the morning, ask me any morning, you'll get the same answer."),
        ("The middle one takes my whole weight so I don't have to. I've been holding myself up since I was about nine. You can't imagine what a rest this is.",
        "My knees keep going and it catches me every time. Every time, and it doesn't make a thing of it afterward. Name me one other person who doesn't make a thing of it."),
        ("Matsu keeps calling a name I don't really answer to now. Tell her the girl she's upset about is doing great. Tell her to come and see. She won't come and see.",
        "Don't let Matsu talk to me. She'll do the reasonable voice -- she's always been able to talk me out of things, [player], and I don't want to be talked out of this one."),
        ("It's loud in here. It's so loud. I sat in a quiet room for years wanting loud, and it turns out you can just get it. Be careful what you sit around wanting.",
        "One minute of quiet? No. No, thank you. I did quiet. I did years of quiet. I'd take this over that and I'm not saying it to be brave."),
        ("You keep pulling your swings for me. Stop that. That's the thing that got me here in the first place, being like that. Don't be like that. Take up some room.",
        "Move earlier. I can see them coming now, it gave me that. It likes it when you nearly get caught. So do I. That happened at some point, me liking that."),
        ("The green ones still come off my hands. It counts them and it doesn't mind -- it says it likes that about me, that I give things away. Take one. Go on.",
        "Take the green one, quick. I've never had anything to give anybody and now I've got a whole -- just take it. Please. Before I stop."),
        ("My left hand's gone cold and quiet and that's on purpose, it's being saved for something. I don't know what yet. I'll find out when it's time and I'll be ready.",
        "I can't feel about half of me. It isn't bad. It's like a foot falling asleep, if the foot were most of you, and if you'd agreed to it in advance."),
        ("Whatever you're going to do, do all of it. It's got no patience for people who half-do things. That's why it took me. I have never half-done anything in my life.",
        "If somebody's going to put their hands on me next, I'd rather it was you. That isn't a nice thing to say. I know it isn't. I'd still rather it was you."),
        ("This doesn't end, by the way. No last one, no going-home part. That's the good news. That's the actual good news, I'm not being -- that's the part I wanted.",
        "And if it does end. If there's a last one after all. Tell me I meant it the whole time. Even if I didn't. Especially then."),
        ("I'm still here. It still wants me here. Do you know how long a thing usually keeps me around for? Not this long. Not once, not this long.",
        "...still here. Still up. Still -- still fine. Still here."),
    ]

    # The command box has a voice: a quiet, human narrator who only ever
    # reports what's visibly off -- the fixed grin, the timing, the thanks
    # aimed at the ceiling -- and never once explains it. The player draws
    # their own conclusions; the horror is theirs to assemble. In phase 2
    # (every third turn, fixed order, see _pick_flavor) a colder line
    # surfaces in caps: overheard, fond, possessive, like something pleased
    # with its work. It never states the thing outright either. Trust the
    # reader -- do not narrate that she isn't the one in control.
    TSB_FLAVOR_P1 = [
        "Her mouth hasn't changed shape since you walked in. The hands keep opening and closing. The hands are doing something else entirely.",
        "She thanks the ceiling after every volley -- quick, automatic, the way you'd thank a bus driver. You don't think she hears herself do it.",
        "The flowers come off her more than they come at you. Shed, not thrown. Her hands never really aim.",
        "She watches your feet instead of the bullets. When she catches herself at it she looks pleased, and then does it more.",
        "She plays every line to a full house. There is no house. There's you, the lights, and a lot of empty.",
        "A green glint drifts through the pattern, off the beat, matching nothing else in the room.",
    ]
    TSB_FLAVOR_P2 = [
        "Between volleys she counts her strings out loud, by number, in order. She gets to five and starts again.",
        "The threads have begun to creak. She has started referring to the sound as music.",
        "She keeps starting to kneel. Each time she's upright again before her knees get anywhere. She thanks the ceiling for that, too.",
        "She comes in a half-second early on every line, like she's reading ahead.",
        "She looks at you the way people look at the last train.",
    ]
    # The colder line that surfaces between the human ones. Overheard, fond,
    # possessive -- the tone of something pleased with what it's keeping.
    # Keep these BANAL. An owner's private notes, not a thesis: the moment one
    # of them explains her situation ("she will not remember to be
    # FRIGHTENED") it stops being frightening. Say small administrative things
    # about a person and let the player supply the rest.
    TSB_FLAVOR_ENGINE = [
        "SHE IS DOING VERY WELL.",
        "SHE CAME WITH ALMOST NOTHING ATTACHED.",
        "SHE DID NOT ASK WHAT IT WAS FOR.",
        "SHE HAS NOT ASKED FOR ANYTHING BACK.",
        "SHE WILL NOT REMEMBER THIS PART.",
        "ALMOST.  AND STILL SMILING.",
    ]
    TSB_FLAVOR_LIMP = [
        "The arm still comes up on the beat. There's nothing behind it.",
        "She's still encouraging you. There's less of her in it every time.",
        "Nothing here is going to resolve. It just thins out -- fewer flowers, quieter voice -- and keeps not ending.",
    ]
    TSB_FLAVOR_LOWHP = "Green, at the edge of the pattern. It doesn't match anything else in here. Take it while you can."
    # The first menu after the overture. The narrator clocks the same thing
    # a certain skeleton once wondered about, from the receiving end.
    TSB_FLAVOR_OVERTURE = "It opened with a full house and a mark already chalked for you. Biggest number first, before anything had been established, before you'd earned it. Like it wanted to know straight away whether you'd stay."

    # ACT responses. Each entry: (pages list, her next bubble, mercy points).
    # The pages are the narrator being human about how absurd this is. ACTs
    # are the pressure MERCY runs on: ordinary, off-script kindness is the
    # one input the show can't parse, so every use makes the performance
    # stutter -- a repeat, a dropped word, a scene that isn't in the script,
    # a laugh it can't source -- before it papers back over. That stutter is
    # the show malfunctioning, not the real her surfacing. Mercy points = how
    # badly you've jammed the act. Bubbles may be lists (extra lines first).
    TSB_ACT_TALK_P1 = [
        (["You make small talk. Small talk, here, of all places. It's the only lever in reach, so you pull it."],
        "Small t-- nobody makes small talk with -- ...it was raining. When I left the house. It was raining, wasn't it. Why would you ask me that. Ask me a different one. Ask me another one.", 1),
        (["You keep your voice low and level, the way you'd talk to someone standing somewhere they shouldn't be."],
        ["Charlie talks like that. Slow voice, boring little topics on purpose. It says I don't need a Charlie anymore --",
        "-- don't you tell Charlie it said that. Don't. ...why do I care whether you -- moving on."], 1),
        (["You run out of topics. You describe your own shoes for a while."],
        "You're describing your shoes. To me. Right now. ...pff. Ha. I laughed, I didn't decide to do that, it just came out on its own. Huh. Do another one. Do the laces.", 1),
        (["You just talk. It's all either of you can do, so you do it."],
        "I'm listening. It's never once checked whether I'm listening. It's got my hands and my voice and my whole week, and it forgot to book the listening. Keep going. I've got nowhere to be.", 0),
    ]
    TSB_ACT_TALK_P2 = [
        (["You talk about after. You make most of it up. She lets you."],
        "There isn't an after. There doesn't need to be one, that's the whole -- ...say the made-up ones again, though. The after ones. Quietly, just to me. Don't say I asked.", 1),
        (["You bring up Matsuda's pen. The one she still owes her."],
        ["The pen -- I did mean to give the pen back -- it says I don't owe anybody from before, clean slate, all settled --",
        "-- but it's wrong about the pen. There. I said it can be wrong and nothing happened. Nothing happened at all."], 1),
        (["You keep talking. The words matter less than the sound of them now."],
        "Keep going. It's had my mouth all day. It never took the listening, though. That part's still mine. Say something true, I don't care what.", 1),
    ]

    # ITEM table: (key, name, heal, pages). One shelf, no restocks. Secondary
    # effects are intentionally small; the inventory widens the player's room
    # for error without replacing the need to learn a pattern.
    # Item pages are the narrator too: a beat of ordinary life used as a
    # combat consumable, which is exactly as wrong as it sounds. The cold
    # status lines _do_item appends after them are the fight's own flat
    # readout -- leave those robotic; the contrast is the point.
    TSB_ITEMS = [
        ("ramune", "Matsuda's Soda", 7.0,
        ["You drink Matsuda's imported soda. It's warm from riding around in a bag all day."]),
        ("bento", "Cold Lunch", 12.0,
        ["You eat the cold lunch in four bites, standing up, in the middle of all this."]),
        ("handkerchief", "Clean Handkerchief", 5.0,
        ["A folded handkerchief. Ironed, because of course it would be."]),
        ("tape", "Sports Tape", 6.0,
        ["You wrap your bad wrist the way the club taught you."]),
        ("coin", "Washed Coin", 0.0,
        ["A heavy coin, cleaner than any coin has a right to be."]),
        ("candy", "Sour Candy", 4.0,
        ["You eat the sour candy. Your entire face reboots."]),
        ("tea", "Paper Cup of Tea", 8.0,
        ["You drink the paper cup of tea, somehow still warm. You don't ask how."]),
        ("cracker", "Rice Crackers", 3.0,
        ["You eat the rice crackers, almost breaking your teeth in the process."]),
    ]
    TSB_ITEM_EFFECTS = {
        "handkerchief": "guard",
        "tape": "invuln",
        "coin": "mercy",
        "candy": "quick",
        "tea": "needles",
        "cracker": "guard",
    }
    TSB_ITEM_DESCS = {
        "ramune": "+7 HP",
        "bento": "+12 HP",
        "handkerchief": "+5 HP  /  softens one hit",
        "tape": "+6 HP  /  longer recovery after one hit",
        "coin": "+2 trust  /  softens one hit",
        "candy": "+4 HP  /  faster movement for two turns",
        "tea": "+8 HP  /  draws in more green needles",
        "cracker": "+3 HP  /  softens one hit",
    }
    TSB_ITEM_BUBBLES = {
        "ramune": "That's Matsu's, she writes her name on the label under the -- ...no. No, that's ours, that's provided. Drink it, stand up. Next one's my favorite and you shouldn't sit it out.",
        "bento": "You're eating? Now? In the middle of my -- ...my show. It gave me a whole show. Chew faster, it doesn't like being kept waiting, and I'm reliable now. I'm very reliable.",
        "handkerchief": "I used to iron those for people who never said anything about it. This one notices everything I do. Keep the cloth. Watch how fast it notices.",
        "tape": "Do the left one, you keep landing on it. I watch you land on it. I see everything from up here and I never have to look away -- which is lucky, because I can't.",
        "coin": "I washed that. I used to wash and label and sort everything, all of it, every single day. It got rid of that girl and kept the parts that were useful.",
        "candy": "Your face just -- ha! It laughed too, did you hear it? It laughs whenever I laugh now, exactly on time, never a beat off. Almost like it's me laughing. Almost.",
        "tea": "Small sips, we're on a clock. ...that's the last warm thing in this building, you know. I'd have made you one. I can't make things anymore.",
        "cracker": "The crunching -- oh, it hates the crunching. Eat more of them. Eat all of them. I didn't say that. That stays between us.",
    }

    # Booth interjections (Matsuda, watching, unable to help). She's the one
    # who knew Tsuba before any of this, so she's the first to clock the
    # wrong smile and the borrowed cadence -- her exact voice saying things
    # she'd never say. Matsuda talks in real sentences; she is the plain
    # counterweight to the glitching on the strings. She reports what she
    # sees and what it's doing to her; she does NOT diagnose Tsubaki out loud.
    TSB_BOOTH = {
        "intro":   "MATSUDA: Tsuba? Tsuba, it's me, I'm right here-- ...why is she smiling like that? She doesn't smile like that. She's never once smiled like that.",
        "reuse":   "MATSUDA: That's her voice. Exactly her voice, down to the-- but those aren't her words. She would never say any of that. Not in a hundred years.",
        "reuse2":  "MATSUDA: And she means it. That's the part I can't -- she means every word of it. She'd argue with me about it.",
        "ramune":  "MATSUDA: She just said my soda was 'provided.' She's been taking it off my shelf since we were nine. [player], she doesn't know it's mine anymore.",
        "shift_v": "MATSUDA: She was DOWN. She was finally, finally down-- and it hauled her back up by the wrists, and she is thanking it. Tsuba. Tsuba, don't. Don't you thank it.",
        "shift_p": "MATSUDA: She reached for it! Did you see-- her whole arm went for the way out, and it snapped her right back. That's the only thing in here that's worked. Whatever you did, do more of it. Please.",
        "death":   "MATSUDA: Hey-- HEY! [player], talk to me. Are you okay? Say something, please, just say something!",
        "limp":    "MATSUDA: Stop. Look at her-- it isn't even aiming anymore. It's moving her because the arm still moves. You're not fighting her. There's nothing there to fight.",
        "limp2":   "MATSUDA: You can put your hands down. Nobody in here is making you keep going except you.",
        "end_v":   "MATSUDA: ...no. No, no, no-- get up. Get up, get up--",
        "end_p":   "MATSUDA: You cut every one. Every single string, I counted them with you-- so why is she-- why isn't she getting up--",
        "end_b":   "MATSUDA: ...what did you just do. What did you DO?",
    }

    # Retry bubbles (she keeps every reset), keyed by deaths this visit. It
    # replays your deaths to her between attempts like a highlight reel, and
    # she has to call the reruns a treat. The cheer wears thinner each time --
    # never into a rescue plea, only into tiredness.
    TSB_RETRY_BUBBLES = [
        "You came back. Oh, you came back -- it kept the part where you dropped, it plays it for me while you're gone. It thinks I like it. And I -- I do. Again.",
        "Twice now. Two in one night. It's saving all the takes, building a little reel -- of you going down, mostly, but I'm in the background. Waving.",
        "It keeps showing me the part where you stop. Over and over, front row, no breaks. ...you don't have to keep giving it new footage, is all I'm -- who said that. Who said that. From the top.",
        "...one more. Slower this time. For me. It never minds another go, it always wants one more out of you. So do I. ...so do I.",
    ]
# --- SIMULATION CORE ---------------------------------------------------------
init python:
    class TSBGame(object):
        """All of Tsubaki mode's live state: the turn machine, the box, the
        bullets, the scripted cinematics. Stepped at a fixed 60Hz by TSBStage;
        owns zero rendering. Everything is plain python data."""

        BUTTONS = ["FIGHT", "ACT", "ITEM", "MERCY"]

        # Modes where the fight is actually being fought -- the phase-2
        # turmoil layer (sag/yank, anchor drips, whiplash decay) only runs
        # here, never over cinematics.
        ACTIVE_MODES = ("menu", "act", "item", "mercy", "fight", "strike",
                        "ptext", "etalk", "dodge")

        def __init__(self, retry=False, visit_deaths=0, debug=False):
            self.result = None
            self.paused = False
            self.debug = debug
            self.retry = retry
            self.visit_deaths = visit_deaths
            self.rng = tsb_random.Random()

            # Player name leaks into her dialogue (lowercase: it's her voice).
            try:
                self.pname = (getattr(store, "player", None) or "you")
            except Exception:
                self.pname = "you"

            # Clocks. tick is authoritative; mtick resets on each mode change.
            self.tick = 0
            self.mtick = 0
            self.mode = "intro"

            # SOUL.
            self.px = TSB_BOX_CX
            self.py = TSB_BOX_CY
            self.hp = TSB_HP_MAX
            self.inv_until = -999
            self.slow = False

            # WHAT THE SHOW DOES TO THE SOUL. None of these five is a hazard;
            # all five are instructions, and the moves that set them are the
            # reason the rebuilt roster is not a shooting gallery. The block
            # at the head of the patterns section is the full argument.
            self.drag_x = 0.0        # displacement added AFTER the player's
            self.drag_y = 0.0        # own input; re-asserted every tick
            self.move_vx = 0.0       # the player's INPUT direction, kept
            self.move_vy = 0.0       # separate so being dragged never reads
            self.move_amt = 0.0      # as disobeying a hold-still cue
            self.hooks = []          # visible strings tied to the SOUL
            self.mark = None         # a lit place on the boards, good/bad
            self.blackout = 0.0      # 0..1, how dark the room is
            self.light_src = None    # the loose worklight, if one is out
            self.loud = 0.0          # 0..1, how loud the room is

            # Boss / routes.
            self.boss_hp = TSB_BOSS_HP
            self.boss_hp_show_until = -999
            self.phase = 1
            self.route = None            # "v"/"p", set by whichever shift fires
            self.turn = -1               # -1 = the intro volley
            self.fought = 0              # landed FIGHTs (route + achievements)
            self.fight_actions = 0       # selections, including a timed-out miss
            self.fought_last = False     # hit landed since her last line
            self.flinch = False          # blocks REACH OUT the turn after a hit
            self.flinch_clear_turn = None
            self.mercy = 0
            self.spares = 0
            self.mercy2 = 0
            self.spares2 = 0
            self.mercy_seen = False      # she noticed the first spare attempt
            self.talk_n = 0
            self.talk2_n = 0
            self.checked = False
            self.checked2 = False
            self.reach_n = 0
            self.name_n = 0
            self.steady_n = 0
            self.stay_n = 0
            self.flee_n = 0
            self.items = list(range(len(TSB_ITEMS)))
            self.guard_charges = 0
            self.invuln_bonus = 0
            self.quick_turns = 0
            self.needle_turns = 0
            self.next_dodge_dens = 1.0
            self.pending = None          # "shift_v"/"shift_p"/"end_v" queued
            self.turns_taken = 0
            self.betrayed = False        # FIGHT landed with one string left

            # Box (center, size) lerping toward a target.
            self.box = [TSB_BOX_CX, TSB_BOX_CY, TSB_MENU_W, TSB_MENU_H]
            self.box_target = [TSB_BOX_CX, TSB_BOX_CY, TSB_MENU_W, TSB_MENU_H]
            self.box_alpha = 0.0         # box materializes during the intro

            # Menu state.
            self.menu_i = 0
            self.sub = None              # "act"/"item"/"mercy" option lists
            self.sub_i = 0
            self.flavor = TSB_FLAVOR_P1[0]

            # FIGHT gauge.
            self.fight_t = 0
            self.strike_acc = None

            # Typewriter state: box pages + her bubble.
            self.pages = []
            self.page_i = 0
            self.page_shown = 0.0
            self.after_text = "etalk"
            self.bubble = None           # current bubble text
            self.bub_shown = 0.0
            self.bub_hold = 0
            self.next_bubble = None      # ACT responses override her turn line
            self.bubble_queue = []       # extra bubbles queued before the dodge
            self.bub_started = 0         # etalk mtick baseline for auto-advance
            self._bub_hold = 60          # hold reused for each queued bubble

            # Bullets & friends.
            self.bullets = []
            self.wires = []
            self.blooms = []
            self.sparks = []
            self.dmg_pops = []
            self.pattern = None
            self.pat_t = 0
            self.pat_dur = 0
            self.pat_dens = 1.0
            self.pat_lead = 0
            self.camp_x = 0.0
            self.camp_y = 0.0
            self.camp_since = 0
            self.camp_at = None
            self.spiral_a = 0.0
            self.spiral_dir = 1.0
            self.pat_scratch = {}
            self.fading_out = False
            # Pattern selection is a per-phase shuffle bag (see _draw_pattern),
            # not a fixed sequence: order varies run to run while coverage and
            # anti-repeat stay guaranteed.
            self.pat_bag_p1 = []
            self.pat_bag_p2 = []
            self.pat_bags_done_p1 = 0
            self.pat_bags_done_p2 = 0
            self._last_pat_i = None

            # Presentation state the renderer reads.
            self.flash = 0.0             # white flash 0..1
            self.dark = 0.0              # ending fade 0..1
            self.fade_in = 1.0           # opening fade from black
            self.room_live = bool(retry) # first run: the genre snaps in on MOVE--
            self.bg_speed = 1.0
            # Route-neutral EMS escalation. ems_target is a high-water mark,
            # ems_progress eases toward it, and ems_clock integrates the pace
            # so accelerating never jumps the shader to a new wave phase.
            # stage_scroll separately integrates the exact bg_speed scalar
            # used by the wind particles, keeping the whole room in one world.
            self.ems_target = 0.0
            self.ems_progress = 0.0
            self.ems_clock = 0.0
            self.stage_scroll = 0.0
            self.phase2_start_hp = TSB_BOSS_HP
            self.strings_alpha = 0.0
            self.strings_cut = 0         # 0..5, kept for HUD/progress reads
            self.cut_string_ids = []     # actual cut order is not left-to-right
            self.string_snap_fx = []
            self.boss_img = 1
            self.boss_dx = 0.0
            self.boss_dy = 0.0
            self.boss_rot = 0.0
            self.boss_alpha = 1.0
            self.boss_fallen = False
            # The void fall (all endings): the room's graphics die and her
            # sprite free-falls to the bottom of the screen under gravity.
            self.void = False
            self.fall_vy = 0.0
            self.fall_landed = False
            self.fall_bounced = False
            self.land_tick = None
            self.shake = 0
            self.slash_born = -9999
            self.heart_break = None      # tick the SOUL shattered
            self.hud_alpha = 0.0
            self.booth = None            # {"key", "born"}
            self.booth_fired = set()     # one-shot booth keys already shown
            self.end_flag = None         # terminal kind while cinematic runs

            # Ambient upward-rush layers (screen-wide, behind the box).
            self.amb_petals = []
            for _i in range(26):
                self.amb_petals.append(self._new_amb_petal(True))
            self.streaks = []
            for _i in range(44):
                self.streaks.append(self._new_streak(True))

            # Input edges, plus the shared release latch that keeps a swallowed
            # key-up from gluing the SOUL to one direction (MSBFKeyLatch, in
            # battle_logic.rpy -- see the SHARED KEY LATCH block there).
            self._prev = {"z": False, "x": False, "left": False, "right": False,
                        "up": False, "down": False}
            self.keys = MSBFKeyLatch()

        # ----- small factories -------------------------------------------------

        def _new_amb_petal(self, anywhere=False):
            # Phase 2 recycles petals darker and faster: deep red and grey,
            # falling like the room is coming apart around her.
            r = self.rng
            if self.phase == 2:
                ci = r.choice([6, 6, 0, 7])
                vy = r.uniform(3.2, 6.4)
            else:
                ci = r.choice([0, 1, 6])
                vy = r.uniform(2.2, 5.0)
            return {"x": r.uniform(0, 1280.0),
                    "y": r.uniform(0, 720.0) if anywhere else -20.0,
                    "vy": vy, "ph": r.uniform(0, 6.28),
                    "ci": ci, "scb": r.randint(0, 2),
                    "rb": r.randint(0, TSB_ROT_BUCKETS - 1),
                    "rs": r.choice([-1, 1]) * r.uniform(0.05, 0.16)}

        def _new_streak(self, anywhere=False):
            r = self.rng
            if self.phase == 2:
                ci = r.choice([6, 7, 0])
                spd = r.uniform(30.0, 52.0)
            else:
                ci = r.choice([2, 0, 7])
                spd = r.uniform(24.0, 40.0)
            return {"x": r.uniform(0, 1280.0),
                    "y": r.uniform(0, 720.0) if anywhere else -90.0,
                    "spd": spd, "len": r.uniform(70.0, 180.0),
                    "ci": ci}

        # ----- mode / text plumbing --------------------------------------------

        def _set_mode(self, mode):
            self.mode = mode
            self.mtick = 0

        def _say(self, pages, after="etalk"):
            self.pages = list(pages)
            self.page_i = 0
            self.page_shown = 0.0
            self.after_text = after
            self._set_mode("ptext")

        def _load_bubble(self, text, hold):
            if text is not None:
                text = str(text).replace("[player]", str(self.pname))
            self.bubble = text
            self.bub_shown = 0.0
            self.bub_hold = hold
            self.bub_started = self.mtick

        def _bub(self, text, hold=60):
            # text may be a single string or a list/tuple of strings shown one
            # after another. In etalk the extra lines drain from a queue before
            # the dodge, so an action can land more than one bubble without a
            # mode change. Cinematics pass single strings and never touch the
            # queue. None entries are dropped.
            self._bub_hold = hold
            if isinstance(text, (list, tuple)):
                seq = [t for t in text if t is not None]
                self.bubble_queue = seq[1:]
                self._load_bubble(seq[0] if seq else None, hold)
            else:
                self.bubble_queue = []
                self._load_bubble(text, hold)

        def _booth(self, key, once=True):
            # Booth lines are beats, not chatter: by default each key fires
            # exactly once per fight instance ("limp" would otherwise nag
            # every collapsed turn).
            if once and key in self.booth_fired:
                return
            if TSB_BOOTH.get(key):
                self.booth_fired.add(key)
                txt = TSB_BOOTH[key].replace("[player]", str(self.pname))
                self.booth = {"key": key, "text": txt, "born": self.tick}

        def _pop(self, x, y, txt, ci=0, big=False):
            self.dmg_pops.append({"x": x, "y": y, "txt": txt, "born": self.tick,
                                "ci": ci, "big": big})

        def _spark_burst(self, x, y, n, ci, speed=3.4, ttl=38, up=0.0):
            r = self.rng
            for _i in range(n):
                if len(self.sparks) >= TSB_MAX_SPARKS:
                    break
                a = r.uniform(0, 6.28318)
                s = r.uniform(0.35, 1.0) * speed
                self.sparks.append({"x": x, "y": y,
                                    "vx": math.cos(a) * s,
                                    "vy": math.sin(a) * s - up,
                                    "age": 0, "ttl": ttl, "ci": ci})

        def _anchor_pos(self, index):
            """Screen position of a string's body anchor, tracking the
            sprite's breathing, puppet jerk, rotation, and offset."""
            motion = tsb_boss_motion(self)
            anchor_x, anchor_y = motion["anchors"][index]
            rax = (anchor_x * motion["scale_x"]
                   - motion["drawn_w"] * 0.5)
            ray = (anchor_y * motion["scale_y"]
                   - motion["drawn_h"] * 0.5)
            rr = math.radians(motion["rotation"])
            rc = math.cos(rr)
            rs = math.sin(rr)
            return (motion["center_x"] + rax * rc - ray * rs,
                    motion["center_y"] + rax * rs + ray * rc)

        def _cut_string(self, index, violent=False):
            if index in self.cut_string_ids or index < 0 or index > 4:
                return False
            x, y = self._anchor_pos(index)
            self.cut_string_ids.append(index)
            self.strings_cut = len(self.cut_string_ids)
            self.string_snap_fx.append({"index": index, "born": self.tick,
                                        "x": x, "y": y,
                                        "violent": bool(violent)})
            self._spark_burst(x, y, 12 if violent else 9, 0 if violent else 5, 4.6 if violent else 3.4, 45, 1.8)
            tsb_play("snap")
            return True

        def _finish(self, kind):
            if self.result is not None:
                return
            self.result = kind
            try:
                # Persist the ending the player actually reached, not the
                # internal one-letter phase marker used during the fight.
                if kind == "victory_p":
                    store.tsb_last_route = "pacifist"
                elif kind == "victory_v":
                    store.tsb_last_route = "violence"
                elif kind == "victory_b":
                    store.tsb_last_route = "betrayal"
                else:
                    store.tsb_last_route = self.route
                store.tsb_last_fought = self.fought
                store.tsb_last_fight_actions = self.fight_actions
                store.tsb_last_turns = self.turns_taken
                store.tsb_last_deaths = self.visit_deaths
            except Exception:
                pass

        def toggle_pause(self):
            if self.result is not None or self.mode in ("end_v", "end_p",
                                                        "end_b", "dead"):
                return
            self.paused = not self.paused
            for channel in (TSB_INST_CH, TSB_VOCAL_CH):
                try:
                    renpy.music.set_pause(self.paused, channel=channel)
                except Exception:
                    pass
            tsb_play("pause")
            renpy.restart_interaction()

        def give_up(self):
            if self.result is None:
                self.paused = False
                for channel in (TSB_INST_CH, TSB_VOCAL_CH):
                    try:
                        renpy.music.set_pause(False, channel=channel)
                    except Exception:
                        pass
                self._finish("quit")
                renpy.restart_interaction()

        # ----- input -----------------------------------------------------------

        def _poll_input(self):
            pg = tsb_pg
            if pg is None:
                return None
            try:
                keys = pg.key.get_pressed()
            except Exception:
                return None

            # Another window owns the keyboard: report everything at rest rather
            # than coasting on whatever SDL last saw.
            if not self.keys.focused():
                self.slow = False
                blank = {"left": False, "right": False, "up": False,
                        "down": False, "z": False, "x": False}
                self.keys.clear()
                self._prev.update(blank)
                edges = dict((k, False) for k in blank)
                edges["held"] = blank
                return edges

            # Every read goes through the latch, so a key whose release never
            # reached SDL cannot leave the SOUL drifting.
            cur = {
                "left": self.keys.pressed(keys, pg.K_LEFT, pg.K_a),
                "right": self.keys.pressed(keys, pg.K_RIGHT, pg.K_d),
                "up": self.keys.pressed(keys, pg.K_UP, pg.K_w),
                "down": self.keys.pressed(keys, pg.K_DOWN, pg.K_s),
                "z": self.keys.pressed(keys, pg.K_z, pg.K_RETURN),
                "x": self.keys.pressed(keys, pg.K_x),
            }
            self.slow = self.keys.pressed(keys, pg.K_LSHIFT, pg.K_RSHIFT)
            edges = {}
            for k in ("z", "x", "left", "right", "up", "down"):
                edges[k] = cur[k] and not self._prev[k]
                self._prev[k] = cur[k]
            edges["held"] = cur
            return edges

        # ----- per-tick housekeeping (runs in every mode) ----------------------

        def _step_ambient(self):
            spd = self.bg_speed
            # Position is integrated rather than `absolute_time * speed`, so
            # shift/hit/limp speed changes alter velocity without teleporting
            # the grid or EMS motifs. This advances on the same fixed ticks and
            # with the same scalar as the petals and streaks immediately below.
            self.stage_scroll = (float(getattr(self, "stage_scroll", 0.0))
                                + spd * TSB_TICK)
            for m in self.amb_petals:
                m["y"] += m["vy"] * spd
                m["ph"] += 0.06
                m["x"] += math.sin(m["ph"]) * 0.5
                m["ra"] = (m.get("ra", 0.0) + m["rs"] * 6.0) % 360.0
                if m["y"] > 740.0:
                    nm = self._new_amb_petal()
                    m.update(nm)
            for s in self.streaks:
                s["y"] += s["spd"] * spd
                if s["y"] > 720.0 + s["len"]:
                    ns = self._new_streak()
                    s.update(ns)
            kept = []
            for sp in self.sparks:
                sp["age"] += 1
                if sp["age"] <= sp["ttl"]:
                    sp["x"] += sp["vx"]
                    sp["y"] += sp["vy"]
                    sp["vy"] += 0.06
                    kept.append(sp)
            self.sparks = kept
            self.dmg_pops = [p for p in self.dmg_pops if self.tick - p["born"] < 70]
            self.string_snap_fx = [s for s in self.string_snap_fx
                                    if self.tick - s["born"] < 72]
            if self.flash > 0.0:
                self.flash = max(0.0, self.flash - 0.05)
            if self.fade_in > 0.0 and self.mode != "dead":
                self.fade_in = max(0.0, self.fade_in - 0.02)
            if self.shake > 0:
                self.shake -= 1
            # Box eases toward its target.
            for i in range(4):
                self.box[i] += (self.box_target[i] - self.box[i]) * 0.14

            # Phase-2 turmoil layer: the room itself starts to struggle.
            # Gated to live-fight modes so it never talks over a cinematic.
            if (self.phase == 2 and not self.boss_fallen
                    and self.mode in TSBGame.ACTIVE_MODES):
                # Strike whiplash bleeds back down to the phase-2 baseline.
                if self.bg_speed > 1.6:
                    self.bg_speed = max(1.6, self.bg_speed - 0.02)
                # After a cut the remaining strings re-tighten in view: the
                # slack the SPARE bought fades as the grip resumes.
                if self.strings_alpha < 0.74:
                    self.strings_alpha = min(0.74, self.strings_alpha + 0.004)
                # The held strings bite: red light drips from an anchor.
                if self.tick % 84 == 0:
                    held = [i for i in range(5) if i not in self.cut_string_ids]
                    if held:
                        ax, ay = self._anchor_pos(self.rng.choice(held))
                        self._spark_burst(ax, ay, 3, 6, 1.1, 60, -1.2)
                # Sag-and-yank: she droops toward the floor she never gets,
                # and the strings snap her back up without asking.
                sag = self.tick % 460
                if sag < 90:
                    self.boss_dy = 7.0 * math.sin((sag / 90.0) * math.pi * 0.5)
                elif sag == 90:
                    self.boss_dy = 0.0
                    self.flash = max(self.flash, 0.10)
                    self.shake = max(self.shake, 6)
                    tsb_play("wire", 0.3)

        def _ems_progress_target(self):
            """How close either route is to finishing, expressed as 0..1.

            Phase 1 owns 0..0.42, the involuntary shift bridges 0.42..0.50,
            and phase 2 owns 0.50..1.00. Mixing FIGHT and MERCY is allowed;
            _update_ems latches the greatest value so a later route change can
            only intensify the field, never make it retreat. (The violence
            route's limp collapse is the one sanctioned retreat; _update_ems
            caps the shown value there so the room sags with her.)
            """
            if self.end_flag is not None or self.mode in ("end_v", "end_p", "end_b"):
                return 1.0

            if self.mode == "shift":
                duration = 470.0 if self.shift_kind == "v" else 500.0
                p = tsb_clamp(self.mtick / duration, 0.0, 1.0)
                p = p * p * (3.0 - 2.0 * p)
                return 0.42 + 0.08 * p

            if self.phase == 1:
                hp_span = max(1.0, TSB_BOSS_HP - TSB_PHASE2_HP)
                violence = tsb_clamp((TSB_BOSS_HP - self.boss_hp) / hp_span,
                                    0.0, 1.0)
                mercy_need = float(1 if self.debug else TSB_MERCY_NEED)
                spare_need = float(1 if self.debug else TSB_SPARES_NEED)
                pacifism = (
                    0.55 * tsb_clamp(self.mercy / mercy_need, 0.0, 1.0)
                    + 0.45 * tsb_clamp(self.spares / spare_need, 0.0, 1.0))
                return 0.42 * max(violence, pacifism)

            # Capture the actual phase-2 entry HP: a pacifist shift can happen
            # at full health, while a violent shift happens near half health.
            # In either case, every later hit advances immediately from 0.50.
            fallback_hp = (TSB_PHASE2_HP if self.route == "v" else TSB_BOSS_HP)
            start_hp = max(1.0, float(getattr(self, "phase2_start_hp", fallback_hp)))
            violence = tsb_clamp((start_hp - self.boss_hp) / start_hp, 0.0, 1.0)
            mercy_need = float(1 if self.debug else TSB_MERCY2_NEED)
            cuts = max(float(self.strings_cut), float(len(self.cut_string_ids)))
            # Each SPARE spends the whole mercy bar on one cut, so progress
            # is counted in threads, with a half-step of credit for the lull
            # currently being built. The latch in _update_ems absorbs the
            # bar emptying after each cut.
            pacifism = tsb_clamp(
                (cuts + 0.5 * tsb_clamp(self.mercy2 / mercy_need, 0.0, 1.0))
                / float(TSB_SPARES2_NEED), 0.0, 1.0)
            return 0.50 + 0.50 * max(violence, pacifism)

        def _update_ems(self):
            # Save-compatible getattr fallbacks also make old mid-fight saves
            # acquire the new field without a migration step.
            drive = tsb_clamp(float(getattr(self, "ems_progress", 0.0)), 0.0, 1.0)
            target = max(float(getattr(self, "ems_target", 0.0)),
                        drive, self._ems_progress_target())
            target = tsb_clamp(target, 0.0, 1.0)
            self.ems_target = target
            # One sanctioned retreat: the violence route's limp collapse.
            # The spectrum sags with her instead of blazing to the finish.
            shown = target
            if (self.end_flag is None and self.phase == 2
                    and self.boss_hp <= TSB_LIMP_HP):
                shown = min(shown, 0.66)
            drive += (shown - drive) * 0.018
            if abs(shown - drive) < 0.00001:
                drive = shown
            self.ems_progress = drive

            # Opening -> finale is roughly a 3x tempo rise. The phase boundary
            # is itself eased, and only spatial features move at that tempo;
            # there are no full-field flashes or time-stepped polarity changes.
            p1_pace = 0.58 + 0.20 * tsb_clamp(drive / 0.50, 0.0, 1.0)
            local2 = tsb_clamp((drive - 0.50) * 2.0, 0.0, 1.0)
            local2 = local2 * local2 * (3.0 - 2.0 * local2)
            p2_pace = 1.02 + 0.72 * local2
            phase_blend = tsb_clamp((drive - 0.46) / 0.08, 0.0, 1.0)
            phase_blend = phase_blend * phase_blend * (3.0 - 2.0 * phase_blend)
            pace = p1_pace * (1.0 - phase_blend) + p2_pace * phase_blend
            self.ems_clock = float(getattr(self, "ems_clock", 0.0)) + pace * TSB_TICK

        def _box_rect(self):
            cx, cy, w, h = self.box
            return (cx - w / 2.0, cy - h / 2.0, w, h)

        def _reveal_page(self):
            # Typewriter for box pages; returns True when the page is done.
            page = self.pages[self.page_i] if self.page_i < len(self.pages) else ""
            if self.page_shown < len(page):
                old = int(self.page_shown)
                self.page_shown = min(len(page), self.page_shown + 0.8)
                if int(self.page_shown) != old and int(self.page_shown) % 3 == 0:
                    tsb_play("blip")
                return False
            return True

        def _reveal_bubble(self):
            if self.bubble is None:
                return True
            if self.bub_shown < len(self.bubble):
                old = int(self.bub_shown)
                self.bub_shown = min(len(self.bubble), self.bub_shown + 0.7)
                if int(self.bub_shown) != old and int(self.bub_shown) % 3 == 0:
                    tsb_play("tsubablip")
                return False
            return True

        # ----- THE STEP ---------------------------------------------------------

        def step(self):
            self.tick += 1
            self.mtick += 1
            edges = self._poll_input() or {"z": False, "x": False, "left": False,
                                            "right": False, "up": False, "down": False,
                                            "held": {"left": False, "right": False,
                                                    "up": False, "down": False}}
            self._step_ambient()

            if self.result is not None:
                return

            mode = self.mode
            if mode == "intro":
                self._step_intro(edges)
            elif mode == "menu":
                self._step_menu(edges)
            elif mode in ("act", "item", "mercy"):
                self._step_submenu(edges)
            elif mode == "fight":
                self._step_fight(edges)
            elif mode == "strike":
                self._step_strike()
            elif mode == "ptext":
                self._step_ptext(edges)
            elif mode == "etalk":
                self._step_etalk(edges)
            elif mode == "dodge":
                self._step_dodge(edges)
            elif mode == "shift":
                self._step_shift()
            elif mode == "end_v":
                self._step_end_v()
            elif mode == "end_p":
                self._step_end_p()
            elif mode == "end_b":
                self._step_end_b()
            elif mode == "dead":
                self._step_dead()

            # Run after the mode action so a hit, ACT, or cut affects the very
            # next rendered frame. The target is latched inside this method.
            self._update_ems()

        # ----- intro ------------------------------------------------------------

        def _step_intro(self, edges):
            t = self.mtick
            if self.retry:
                # Short re-entry: she saw the reset; the machine skips its pomp.
                if t == 20:
                    tsb_music_start()
                if t == 40:
                    self.room_live = True
                    self.box_alpha = 1.0
                    self.hud_alpha = 1.0
                    self.strings_alpha = 0.72 if self.phase == 2 else 0.18
                    idx = min(max(self.visit_deaths, 1), len(TSB_RETRY_BUBBLES)) - 1
                    self._bub(TSB_RETRY_BUBBLES[idx], hold=80)
                if t > 40 and self._reveal_bubble() and (t > 220 or edges["z"]):
                    self.bubble = None
                    self._menu_in()
                return
            if t == 30:
                self._bub("...%s?" % self.pname, hold=70)
            elif t == 150:
                # The last thing she says before it takes her -- lowercase,
                # the small pre-show voice. After this she is all performance.
                self._bub("wait-- there's something in my-- it's got my arms, it's pulling them up-- run. run, [player], don't let it get its hands in y--", hold=40)
            elif t == 360:
                # The arm snaps up. The genre arrives all at once.
                self.room_live = True
                tsb_play("phase")
                tsb_play("wire")
                self.flash = 1.0
                self.strings_alpha = 0.9
                self.shake = 30
                self.box_alpha = 1.0
                self.hud_alpha = 1.0
                tsb_music_start()
                self._booth("intro")
                # No announcement, no patter: her lowercase warning cuts
                # straight to the one word that matters, and the overture
                # is already falling while she says it.
                self._bub("MOVE--", hold=20)
            elif t == 385:
                self.strings_alpha = 0.18
                self._begin_dodge(("overture", 780, 1.0))
                return
            if t > 30:
                self._reveal_bubble()

        # ----- menu -------------------------------------------------------------

        def _menu_in(self):
            self.bubble = None
            self.bubble_queue = []
            self.bub_shown = 0.0
            self.box_target = [TSB_BOX_CX, TSB_BOX_CY, TSB_MENU_W, TSB_MENU_H]
            self.menu_i = 0
            self.sub = None
            self.flavor = self._pick_flavor()
            self._set_mode("menu")

        def _submenu_in(self, kind, options):
            self.sub = list(options)
            self.sub_i = 0
            h = TSB_MENU_H
            if kind == "item":
                rows = ((len(self.sub) + 1) // 2
                        if len(self.sub) >= 4 else len(self.sub))
                # Reserve a description line below every possible item row,
                # including the awkward 3/5/6-item inventory sizes.
                h = max(TSB_MENU_H, 110.0 + 36.0 * max(0, rows - 1))
            self.box_target = [TSB_BOX_CX, TSB_BOX_CY, TSB_MENU_W, h]
            if kind == "item" and self.box[3] < h:
                # Options render on the first submenu frame, so expansion
                # cannot safely trail them through the regular box lerp.
                self.box[3] = h
            self._set_mode(kind)

        def _pick_flavor(self):
            if self.phase == 2 and self.boss_hp <= TSB_LIMP_HP:
                return TSB_FLAVOR_LIMP[self.turns_taken % len(TSB_FLAVOR_LIMP)]
            if self.hp <= 5.0:
                return TSB_FLAVOR_LOWHP
            # turns_taken is exactly 1 only at the first menu after the
            # overture (the retry intro skips the volley and arrives at 0).
            if self.phase == 1 and self.turns_taken == 1 and not self.retry:
                return TSB_FLAVOR_OVERTURE
            if self.phase == 2:
                # Every third turn the thing's own voice shoulders the
                # narrator aside -- in fixed order, each line stating a
                # little more plainly what it has done to her.
                t = max(self.turn, 0)
                if t % 3 == 2:
                    idx = min(t // 3, len(TSB_FLAVOR_ENGINE) - 1)
                    return TSB_FLAVOR_ENGINE[idx]
                pool = TSB_FLAVOR_P2
            else:
                pool = TSB_FLAVOR_P1
            return pool[self.turns_taken % len(pool)]

        def _step_menu(self, edges):
            if edges["left"]:
                self.menu_i = (self.menu_i - 1) % 4
                tsb_play("move")
            if edges["right"]:
                self.menu_i = (self.menu_i + 1) % 4
                tsb_play("move")
            if not edges["z"]:
                return
            tsb_play("confirm")
            b = TSBGame.BUTTONS[self.menu_i]
            if b == "FIGHT":
                self.fight_actions += 1
                self.fight_t = 0
                self.strike_acc = None
                self._set_mode("fight")
            elif b == "ACT":
                self._submenu_in("act", self._act_options())
            elif b == "ITEM":
                if not self.items:
                    self._say(["Your pockets are empty. You've already shared everything you had."], after="menu")
                else:
                    self._submenu_in("item", [TSB_ITEMS[i][1] for i in self.items])
            elif b == "MERCY":
                self._submenu_in("mercy", self._mercy_options())

        def _act_options(self):
            if self.phase == 1:
                return ["CHECK", "TALK", "REACH OUT", "SAY HER NAME"]
            return ["CHECK", "TALK", "MATCH BREATHING", "STAY"]

        def _mercy_options(self):
            return ["SPARE", "FLEE"]

        def _step_submenu(self, edges):
            n = len(self.sub)
            old_i = self.sub_i
            if n >= 4:
                # The renderer is a row-major two-column grid. Preserve the
                # visual column on vertical moves and never land on a missing
                # bottom-right cell.
                row = self.sub_i // 2
                col = self.sub_i % 2
                rows = (n + 1) // 2
                if edges["left"] or edges["right"]:
                    other = row * 2 + (1 - col)
                    if other < n:
                        self.sub_i = other
                elif edges["up"] or edges["down"]:
                    step = -1 if edges["up"] else 1
                    for off in range(1, rows + 1):
                        nr = (row + step * off) % rows
                        candidate = nr * 2 + col
                        if candidate < n:
                            self.sub_i = candidate
                            break
            else:
                if edges["up"] or edges["left"]:
                    self.sub_i = (self.sub_i - 1) % n
                elif edges["down"] or edges["right"]:
                    self.sub_i = (self.sub_i + 1) % n
            if self.sub_i != old_i:
                tsb_play("move")
            if edges["x"]:
                tsb_play("cancel")
                self.sub = None
                self._menu_in()
                return
            if not edges["z"]:
                return
            tsb_play("confirm")
            if self.mode == "act":
                self._do_act(self.sub_i)
            elif self.mode == "item":
                self._do_item(self.sub_i)
            elif self.mode == "mercy":
                self._do_mercy(self.sub_i)

        # ----- actions ----------------------------------------------------------

        def _mercy_add(self, pts):
            if self.phase == 1:
                self.mercy = min(self.mercy + pts * (2 if self.debug else 1), 9)
            else:
                self.mercy2 = min(self.mercy2 + pts * (2 if self.debug else 1), 9)

        def _do_act(self, i):
            # ACTs escalate use over use. The pages are the narrator being
            # honest about how absurd this is; her replies are the exorcism
            # working in real time. CHECK's ATK 0 measures HER, not the
            # thing throwing the volleys -- and the zero embarrasses the
            # zealot, because it means the fight was never hers either.
            name = self.sub[i]
            self.sub = None
            if name == "CHECK":
                if self.phase == 1:
                    if not self.checked:
                        self.checked = True
                        self.next_bubble = "You're checking me? Reading my numbers out loud? I've got numbers, I'm on a -- ...oh. Why is the big one a zero. Cover that up. Nobody needs to see the zero."
                        self._say(["TSUBAKI KAREDA -- ATK 0.  DEF 1.", "ATK zero. For someone filling the room with knives, that number has very little to say."])
                    else:
                        self.next_bubble = "Stop reading me. The zero's a typo. It's a placeholder, it's getting fixed, they're fixing it. Don't look at it."
                        self._say(["The readout hasn't budged. ATK 0.", "She keeps calling the pattern hers. The number keeps disagreeing with her."])
                else:
                    if not self.checked2:
                        self.checked2 = True
                        # The question rattles the act: the first CHECK of the
                        # second half jams it the way any off-script beat does.
                        self._mercy_add(1)
                        self.next_bubble = "Read it out. All of it, I don't mind. ...ask it which of the five is me, though. It knows. It knows everything. It just won't say. Why won't it say."
                        self._say(["TSUBAKI KAREDA -- ATK 0.  DEF 0.", "FIVE THREADS.  ONE BEARS ALL THE WEIGHT."])
                    else:
                        self.next_bubble = "..."
                        self._say(["ATK 0. DEF 0. You already knew.", "You keep asking. The answer keeps being the same girl and the same zero."])
            elif name == "TALK":
                table = TSB_ACT_TALK_P1 if self.phase == 1 else TSB_ACT_TALK_P2
                n = self.talk_n if self.phase == 1 else self.talk2_n
                entry = table[min(n, len(table) - 1)]
                if self.phase == 1:
                    self.talk_n += 1
                else:
                    self.talk2_n += 1
                self._mercy_add(entry[2])
                self.next_bubble = entry[1]
                self._say(list(entry[0]))
            elif name == "REACH OUT":
                if self.flinch:
                    self.flinch = False
                    self.flinch_clear_turn = None
                    self.next_bubble = "It says you'll swing again. It read you on the way in, put you down as the swinging sort -- ...be wrong. Be wrong about me once. ...try again? If you want."
                    self._say(["Her whole body snaps away from your hand before she can answer -- faster than a person decides to move."])
                else:
                    self.reach_n += 1
                    if self.reach_n == 1:
                        self._mercy_add(1)
                        self.next_bubble = "The shoulder went slack. That isn't -- there's no part of this where I go slack. ...huh. Do it again. I want to watch that happen again."
                    elif self.reach_n == 2:
                        self.next_bubble = "You keep putting your hand in there. With the knives. For a shoulder. It can't work out what you're after and neither can I -- there isn't anything, is there. Ha. There isn't."
                    else:
                        self.next_bubble = "I stopped bracing. Did you feel me stop? My body was doing that without me. Keep going. Nobody wrote this bit and I want to see where it goes."
                    self.next_dodge_dens = min(self.next_dodge_dens, 0.88)
                    self._say(["You reach in past the pattern. Slowly. Palm open, nothing in it."])
            elif name == "SAY HER NAME":
                self.name_n += 1
                if self.name_n == 1:
                    self._mercy_add(2)
                    self.next_bubble = "...Tsubaki? It doesn't call me that. It's got a number for me, numbers are tidier, numbers don't drag a whole girl along behind them. ...say the other one again. The name one."
                    self._say(["You say her name -- the one she had long before this room existed."])
                elif self.name_n == 2:
                    self.next_bubble = "Tsubaki Kareda. Both halves. I kept the whole name, surname and everything. Don't let it talk me into a shorter one. I like the one I came in with."
                    self._say(["Tsubaki."])
                else:
                    self.next_bubble = "You keep saying it like it costs something. Like the room might take it off me if I set it down. Say it again. Keep it up where it can't reach."
                    self._say(["Tsubaki. Tsubaki. Tsubaki."])
            elif name == "MATCH BREATHING":
                self.steady_n += 1
                # Her old rhythm keeps jamming the act no matter how often
                # you return to it -- the mercy loop leans on that.
                self._mercy_add(1)
                self.guard_charges = min(2, self.guard_charges + 1)
                if self.steady_n == 1:
                    self.next_bubble = "Four in, six out -- no, that's the quiet girl's counting, I retired her -- ...four in. Six out. ...oh. There it is. Body remembers. That's strange. Do it with me?"
                    self._say(["Four counts in. Six counts out. Her old rhythm -- the one habit in here that came in with her, not with the room."])
                elif self.steady_n == 2:
                    self.next_bubble = "It's looking for what you're doing to me and it can't find it. There's no cue for this. Three... four... this isn't in the show at all, is it."
                    self._say(["You find her rhythm again. Easier this time."])
                else:
                    self.next_bubble = "I can't always get to four now. Count louder. Count for both of us -- one of us has to keep time and it isn't going to be the strings."
                    self._say(["In. Out. You keep the count for both of you."])
            elif name == "STAY":
                self.stay_n += 1
                if self.stay_n == 1:
                    self._mercy_add(2)
                    self.next_bubble = "You're staying? For the -- for the fight? ...no. Not for the fight. There isn't a word on the schedule for what you're -- I used to have a word for it. It's around here somewhere."
                    self._say(["You plant your feet. You're not going anywhere."])
                else:
                    self._mercy_add(1)
                    self.next_bubble = "Still here. ...okay. Okay. People aren't usually still here. I'll allow it. Best view's up here, but yours isn't bad."
                    self._say(["You keep your feet where they are. She can see that you mean it."])

        def _do_item(self, i):
            idx = self.items.pop(i)
            key, label, heal, pages = TSB_ITEMS[idx]
            self.sub = None
            old_hp = self.hp
            self.hp = min(TSB_HP_MAX, self.hp + heal)
            gained = self.hp - old_hp
            if gained > 0.0:
                tsb_play("heal")
            if key == "ramune":
                self._booth("ramune")
            effect = TSB_ITEM_EFFECTS.get(key)
            status = []
            if effect == "guard":
                self.guard_charges = min(2, self.guard_charges + 1)
                status.append("GUARD  /  READY")
            elif effect == "invuln":
                self.invuln_bonus = max(self.invuln_bonus, 34)
                status.append("RECOVERY WINDOW  /  EXTENDED")
            elif effect == "mercy":
                self._mercy_add(2)
                self.guard_charges = min(2, self.guard_charges + 1)
                status.append("THREAD TENSION  /  -2")
            elif effect == "quick":
                self.quick_turns = max(self.quick_turns, 2)
                status.append("MOVEMENT  /  +16%  /  2 TURNS")
            elif effect == "needles":
                self.needle_turns = max(self.needle_turns, 2)
                status.append("MEND SIGNAL  /  AMPLIFIED")
            if gained > 0.0:
                status.append("HP  /  +%d" % int(gained))
            self.next_bubble = TSB_ITEM_BUBBLES.get(key)
            self._say(list(pages) + status)

        def _do_mercy(self, i):
            name = self.sub[i]
            self.sub = None
            if name == "FLEE":
                self.flee_n += 1
                if self.flee_n == 1:
                    self.next_bubble = "Leave? But it picked you. Nobody gets picked twice, that's not how it -- ...if there is a door. If you find one. Take me with you. ...I didn't say that. Forget it."
                    self._say(["You look for the way you came in. The room's given up pretending it ever had one."])
                elif self.phase == 2:
                    self.next_bubble = None
                    self._say(["There's no door.", "There was never a door."])
                else:
                    self.next_bubble = None
                    self._say(["Still no door."])
                return
            # SPARE.
            need = 1 if self.debug else TSB_MERCY_NEED
            need2 = 1 if self.debug else TSB_MERCY2_NEED
            if self.phase == 1:
                if self.mercy < need:
                    if not self.mercy_seen:
                        self.mercy_seen = True
                        self.next_bubble = "What are you doing? You have to pick something. When you just stand there it goes quiet, and I can hear the -- pick a button. Any of them. Fill it in."
                    else:
                        self.next_bubble = None
                    self._say(["You lower your guard. Above her, something tightens its grip."])
                else:
                    self.spares += 1
                    if self.spares >= (1 if self.debug else TSB_SPARES_NEED):
                        self.pending = "shift_p"
                        self.next_bubble = None
                        self._say(["You keep not moving.", "Something above her loses its patience -- and, for a moment, its grip."],
                                    after="pending")
                    else:
                        self.next_bubble = ("Something let go just then. I had my own whole weight for a second. It was awful. ...do it again, though. I want the awful thing again."
                                            if self.spares == 1 else
                                            "Stop -- you've got a mark to hit and standing there isn't -- there's no cue for somebody just offering. It's checking. It's actually checking. Keep offering.")
                        self._say(["You hold out the choice. The strings... hesitate?"])
            else:
                if self.mercy2 < need2:
                    self.next_bubble = None
                    if self.spares2:
                        self._say(["MERCY  /  THREADS LOCKED",
                                    "The remaining strings have cinched tight since the last cut. It's watching your hands now. It will have to be lulled all over again."])
                    else:
                        self._say(["MERCY  /  THREADS LOCKED"])
                else:
                    self.spares2 += 1
                    order = [0, 1, 3, 2, 4]
                    # Debug still cuts one string per SPARE (mercy need is 1
                    # above) so the betrayal window -- exactly one string
                    # left -- stays reachable for testing.
                    string_i = order[min(self.spares2 - 1, len(order) - 1)]
                    self._cut_string(string_i)
                    self.flash = 0.44 + min(self.spares2, 5) * 0.07
                    self.shake = 12 + min(self.spares2, 5) * 2
                    # The whole lull is spent on the one cut: the mercy bar
                    # empties with the thread, the freed slack shows on the
                    # strings for a moment, and the grip clamps back down.
                    # Rinse and repeat -- every thread has to be stolen off
                    # a boss caught unawares.
                    self.mercy2 = 0
                    self.strings_alpha = min(self.strings_alpha, 0.42)
                    if self.spares2 >= TSB_SPARES2_NEED:
                        self.pending = "end_p"
                        self.next_bubble = None
                        self._say(["THREAD 5 / 5  /  CUT"], after="pending")
                    else:
                        # The pacifist route's cruelty: freeing her feels
                        # like hurting her. Every cut takes away something
                        # she believes is holding her together. She never
                        # asks to be freed -- she asks not to be put down,
                        # and she asks it in plain, panicked, human words.
                        replies = [
                            "My hand -- you've taken my hand off me, that one was holding it on -- put it back, I was fine, I was held, don't leave me half like this --",
                            "Both arms. They're shaking. They shake the way they used to, the way they did before -- no, put them back, don't send me back to being her --",
                            "My head turned on its own. I can see too far now, I can see all the way out to the edges and there's nothing out there -- stop, you're letting it back in --",
                            "One left. That's the last one holding. Cut it and I'm on my own, and I never learned how to be on my own, I was never any good at it -- [player], don't --",
                        ]
                        self.next_bubble = replies[min(self.spares2 - 1,
                                                        len(replies) - 1)]
                        self._say(["THREAD %d / 5  /  CUT" % self.spares2,
                                    "GRIP  /  RETIGHTENED"])

        # ----- FIGHT gauge / strike --------------------------------------------

        def _last_string(self):
            # The betrayal window: four threads cut, one left holding her.
            return self.phase == 2 and len(self.cut_string_ids) == 4

        def _step_fight(self, edges):
            self.fight_t += 1
            last = self._last_string()
            # With one string left there is nothing in her to resist the
            # blow: any swing lands, even letting the gauge run out. The
            # game does not let you half-commit to this.
            if edges["z"] or (last and self.fight_t >= TSB_FIGHT_SWEEP):
                pos = self.fight_t / float(TSB_FIGHT_SWEEP)
                acc = tsb_clamp(1.0 - abs(pos - 0.5) * 2.0, 0.0, 1.0)
                self.strike_acc = acc
                if last:
                    dmg = int(math.ceil(self.boss_hp))
                    crit = True
                    self.betrayed = True
                else:
                    dmg = TSB_DMG_BASE + int(TSB_DMG_SPAN * acc)
                    crit = acc >= TSB_CRIT_ACC
                    if crit:
                        dmg += 8
                    if self.debug:
                        dmg = 999
                self.boss_hp = max(0.0, self.boss_hp - dmg)
                self.fought += 1
                self.fought_last = True
                self.flinch = True
                self.flinch_clear_turn = self.turns_taken + 2
                self.spares = 0
                # A swing snaps the act back to attention: whatever lull the
                # phase-2 mercy bar was holding is spent on nothing.
                self.mercy2 = 0
                self.slash_born = self.tick
                self.shake = 34 if last else 26
                if self.phase == 2:
                    # Whiplash: the whole rising stage lurches with the blow,
                    # then bleeds back down to speed (see _step_ambient).
                    self.bg_speed = max(self.bg_speed, 2.8)
                self.boss_hp_show_until = self.tick + 110
                tsb_play("crit" if crit else "slash")
                self._pop(TSB_BOSS_X + 30, TSB_BOSS_FEET_Y - 210, str(dmg), 0, True)
                self._spark_burst(TSB_BOSS_X, TSB_BOSS_FEET_Y - 150, 22 if last else 14, 0, 3.6, 36)
                self._set_mode("strike")
                return
            if self.fight_t >= TSB_FIGHT_SWEEP:
                tsb_play("miss")
                self.next_bubble = None
                if self.phase == 2:
                    self._say(["You swing at where she was. The strings had already moved her."])
                else:
                    self._say(["You swing at the air. She looks disappointed. You wish she hadn't."])

        def _step_strike(self):
            if self.mtick < 55:
                return
            if self.betrayed:
                self._begin_end_b()
            elif self.phase == 1 and self.boss_hp <= TSB_PHASE2_HP:
                self._begin_shift("v")
            elif self.phase == 2 and self.boss_hp <= 0.0:
                self._begin_end_v()
            else:
                self._begin_etalk()

        # ----- box pages / her bubble --------------------------------------------

        def _step_ptext(self, edges):
            done = self._reveal_page()
            if not edges["z"]:
                return
            if not done:
                self.page_shown = float(len(self.pages[self.page_i]))
                return
            tsb_play("confirm", 0.6)
            self.page_i += 1
            if self.page_i < len(self.pages):
                self.page_shown = 0.0
                return
            # Pages exhausted: route by after_text.
            if self.after_text == "menu":
                self._menu_in()
            elif self.after_text == "pending":
                if self.pending == "shift_p":
                    self.pending = None
                    self._begin_shift("p")
                elif self.pending == "end_p":
                    self.pending = None
                    self._begin_end_p()
                else:
                    self._begin_etalk()
            else:
                self._begin_etalk()

        def _begin_etalk(self):
            line = self.next_bubble
            self.next_bubble = None
            # Mode first so the bubble's auto-advance baseline (bub_started)
            # is measured from a fresh mtick of 0.
            self._set_mode("etalk")
            if line is None:
                line = self._turn_bubble()
            self._bub(line, hold=70)

        def _turn_bubble(self):
            t = max(self.turn, 0)
            if self.phase == 1:
                if t < len(TSB_BUBBLES_P1):
                    pair = TSB_BUBBLES_P1[t]
                else:
                    return TSB_LOOP_P1[t % len(TSB_LOOP_P1)]
                return pair[1] if self.fought_last else pair[0]
            pool = TSB_BUBBLES_P2
            pair = pool[min(t, len(pool) - 1)]
            lean = self.fought_last or self.boss_hp <= TSB_LIMP_HP * 1.4
            return pair[1] if lean else pair[0]

        def _step_etalk(self, edges):
            done = self._reveal_bubble()
            if edges["z"] and not done:
                self.bub_shown = float(len(self.bubble or ""))
                return
            # Auto-advance only after the line has had reading time past the
            # typing itself (reveal is 0.7 chars/tick, so ~1.43 ticks/char).
            elapsed = self.mtick - self.bub_started
            if done and (elapsed > len(self.bubble or "") * 1.6 + self.bub_hold + 60
                        or edges["z"]):
                if self.bubble_queue:
                    # More of the same turn: load her next line in place.
                    self._load_bubble(self.bubble_queue.pop(0), self._bub_hold)
                    tsb_play("tsubablip", 0.5)
                    return
                self.fought_last = False
                self.bubble = None
                self._begin_dodge()

        # ----- dodge ------------------------------------------------------------

        DODGE_BOX = {
            "overture":    (420.0, 290.0),
            # shared
            "camellia":    (410.0, 272.0),
            "hemline":     (430.0, 250.0),
            "metronome":   (380.0, 264.0),
            "limelight":   (400.0, 272.0),
            "ovation":     (400.0, 258.0),
            "understudy":  (400.0, 264.0),
            # phase 1 only
            "footlights":  (430.0, 240.0),
            "programme":   (420.0, 262.0),
            "curtaincall": (420.0, 258.0),
            "pincushion":  (380.0, 272.0),
            "garland":     (400.0, 272.0),
            # phase 2 only
            "marionette":  (400.0, 270.0),
            "feedback":    (400.0, 264.0),
            "recast":      (390.0, 260.0),
            "unravel":     (420.0, 256.0),
            "chandelier":  (390.0, 272.0),
            "blackout":    (400.0, 272.0),
            "tableau":     (400.0, 272.0),
            "limp":        (300.0, 240.0),
        }

        # A count-in, per move. The box finishes contracting (WARMUP) and then
        # these moves wait a beat longer before their first event, because
        # their opening beat lands ON the SOUL: a ring that closes on where
        # you're standing, a throw through the middle of the room, a band laid
        # over your mark. Those are fair once you've SEEN the move -- but the
        # first rep arrives while the player is still finding the box, and a
        # telegraph you haven't learned to read yet is not a telegraph. The
        # count-in is added to the move's duration, so nobody loses a rep for
        # it; it only delays the downbeat, not each repetition.
        LEAD_IN = {
            "marionette":  40,  # the first hook lands on the SOUL itself
            "limelight":   40,  # the spot has to be lit before it can shelter
            "blackout":    36,  # the lights go out before anything comes in
            "pincushion":  36,  # the arms grow out of the middle of the room
            "understudy":  34,  # your reflection arrives standing on you
            "unravel":     30,  # the seam is laid through where you stand
            "garland":     30,
            "feedback":    30,
            "tableau":     30,
        }

        def _turn_entry(self):
            # The violence route's collapse overrides the roster: past the
            # limp threshold the fight stops pretending to be one.
            if self.phase == 2 and self.boss_hp <= TSB_LIMP_HP:
                # Both fire once: first the plea, then -- if the player is
                # still swinging -- the flat, colder read of what that means.
                if self.boss_hp <= TSB_LIMP_HP * 0.30:
                    self._booth("limp2")
                elif self.boss_hp <= TSB_LIMP_HP * 0.55:
                    self._booth("limp")
                # The stage's climb slackens with her. The room is giving up.
                self.bg_speed = min(self.bg_speed, 0.9)
                return ("limp", 380, 1.0)
            return self._draw_pattern()

        def _draw_pattern(self):
            # Shuffle-bag selection: the phase's roster is drawn in a fresh
            # random order each pass, so no two runs meet the same sequence,
            # but every pattern still appears once per bag and none repeats
            # back-to-back across a reshuffle. A mild density creep rides each
            # completed bag, so a player who neither fights nor acts keeps
            # facing rising pressure instead of a flat loop.
            if self.phase == 1:
                table, bag = TSB_TURNS_P1, self.pat_bag_p1
            else:
                table, bag = TSB_TURNS_P2, self.pat_bag_p2
            if not bag:
                order = list(range(len(table)))
                self.rng.shuffle(order)
                if (self._last_pat_i is not None and len(order) > 1
                        and order[0] == self._last_pat_i):
                    order[0], order[1] = order[1], order[0]
                bag.extend(order)
                if self.phase == 1:
                    self.pat_bags_done_p1 += 1
                else:
                    self.pat_bags_done_p2 += 1
            idx = bag.pop(0)
            self._last_pat_i = idx
            pid, dur, dens = table[idx]
            bags_done = (self.pat_bags_done_p1 if self.phase == 1
                        else self.pat_bags_done_p2)
            if bags_done > 1:
                dens = min(dens + 0.06 * (bags_done - 1), 1.7)
            return (pid, dur, dens)

        def _begin_dodge(self, forced=None):
            pid, dur, dens = forced if forced is not None else self._turn_entry()
            # Matsuda catches the wrong voice early, then names what the thing
            # has actually done to her once the second half is underway.
            if forced is None:
                if self.phase == 1 and self.turn == 1:
                    self._booth("reuse")
                elif self.phase == 2 and self.turn == 2:
                    self._booth("reuse2")
            self.pattern = pid
            self.pat_t = 0
            self.pat_lead = TSBGame.LEAD_IN.get(pid, 0)
            self.pat_dur = dur + self.pat_lead
            self.pat_dens = dens * self.next_dodge_dens
            self.next_dodge_dens = 1.0
            self.pat_scratch = {}
            self.fading_out = False
            # Every move starts in an unlit, unstrung, quiet room and has to
            # ask for anything else itself.
            self.drag_x = 0.0
            self.drag_y = 0.0
            self.hooks = []
            self.mark = None
            self.blackout = 0.0
            self.loud = 0.0
            self.light_src = None
            self.spiral_a = self.rng.uniform(0, 6.28)
            self.spiral_dir = -self.spiral_dir
            # The camp clock starts fresh each move, anchored where the SOUL
            # is re-centered, so a move never inherits the last one's count.
            self.camp_x = TSB_BOX_CX
            self.camp_y = TSB_BOX_CY
            self.camp_since = 0
            w, h = TSBGame.DODGE_BOX.get(pid, (TSB_DODGE_W, TSB_DODGE_H))
            self.box_target = [TSB_BOX_CX, TSB_BOX_CY, w, h]
            self.px = TSB_BOX_CX
            self.py = TSB_BOX_CY
            self._set_mode("dodge")

        def _step_dodge(self, edges):
            held = edges["held"]
            self.pat_t += 1
            # SOUL movement, clamped inside the CURRENT box.
            dx = (1.0 if held["right"] else 0.0) - (1.0 if held["left"] else 0.0)
            dy = (1.0 if held["down"] else 0.0) - (1.0 if held["up"] else 0.0)
            if dx != 0.0 and dy != 0.0:
                dx *= 0.70710678
                dy *= 0.70710678
            spd = TSB_MOVE_SLOW if self.slow else TSB_MOVE
            if self.quick_turns > 0:
                spd *= 1.16
            bx, by, bw, bh = self._box_rect()
            pad = TSB_PLAYER_R + TSB_BORDER
            # Record what the PLAYER asked for before anything is done to the
            # SOUL. A move that wants you to hold still (feedback) or to pull
            # against a string (marionette) has to read intent: if it read
            # displacement instead, being dragged would count as moving and
            # the cue would be unanswerable.
            self.move_vx = dx
            self.move_vy = dy
            self.move_amt = math.hypot(dx, dy) * spd
            self.px = tsb_clamp(self.px + dx * spd + self.drag_x,
                                bx + pad, bx + bw - pad)
            self.py = tsb_clamp(self.py + dy * spd + self.drag_y,
                                by + pad, by + bh - pad)
            # Drag is re-asserted by whatever is pulling on every tick it
            # pulls, so it expires the instant that thing lets go.
            self.drag_x = 0.0
            self.drag_y = 0.0

            active_t = self.pat_t - TSB_PATTERN_WARMUP - self.pat_lead
            if (not self.fading_out
                    and self.pat_t <= self.pat_dur + TSB_PATTERN_WARMUP):
                # Let the menu box finish contracting before an authored
                # emitter reads its bounds. The SOUL remains controllable.
                if active_t > 0:
                    fn = getattr(self, "_pat_" + self.pattern, None)
                    if fn is not None:
                        fn(active_t, self.pat_dens)
                    self._dodge_common(active_t)
            elif not self.fading_out:
                self.fading_out = True
                for b in self.bullets:
                    b["fz"] = 18
                self.blooms = []
                self._kill_wires()
                # The room's instructions end with the move that gave them:
                # no mark, no strings, house lights back up, volume down.
                self.hooks = []
                self.mark = None
                self.blackout = 0.0
                self.loud = 0.0
                self.light_src = None

            self._step_bullets()

            if self.fading_out and not self.bullets and not self.wires:
                self._end_turn()

        def _end_turn(self):
            self.turn += 1
            self.turns_taken += 1
            if (self.flinch and self.flinch_clear_turn is not None
                    and self.turns_taken >= self.flinch_clear_turn):
                self.flinch = False
                self.flinch_clear_turn = None
            if self.quick_turns > 0:
                self.quick_turns -= 1
            if self.needle_turns > 0:
                self.needle_turns -= 1
            self._menu_in()
        # ----- bullets ----------------------------------------------------------
        # bullet: x/y/vx/vy, kind, ci, sq (scale quarters), rb (rot bucket),
        #         rs (spin), sway/ph, ay, age, fz, optional delayed turn/orbit
        #         and a cosmetic tether. `armed_at` makes held formations fair.
        # wire:   orient "h"/"v" plus pos, or "d" plus two endpoints; every
        #         damaging line has the same telegraph -> live -> gone cadence.

        # Hit radii stay UNDER the drawn body -- house rule, same as Kotonoha's:
        # what you see is bigger than what cuts you. `needle` is the mend, and
        # its radius is generous on purpose because catching it is the reward.
        BULLET_R = {"petal": 5.0, "pellet": 5.0, "dagger": 5.0,
                    "bigpetal": 9.0, "needle": 16.0,
                    "pin": 5.0, "page": 6.0, "soul": 7.0, "spark": 5.5,
                    "lamp": 6.5, "houselamp": 10.0, "bead": 6.0,
                    "face": 6.0, "stitch": 5.0, "thread": 4.0, "word": 4.5,
                    "hoop": 7.0, "clap": 5.5, "seed": 4.0, "blob": 8.0,
                    "chip": 6.0, "bolt": 5.0, "note": 6.0, "rest": 6.0,
                    "flame": 6.5}
        BULLET_DMG = {"petal": 3.0, "pellet": 3.0, "dagger": 4.0, "bigpetal": 4.0,
                    "pin": 4.0, "page": 4.0, "soul": 4.0, "spark": 3.0,
                    "lamp": 4.0, "houselamp": 5.0, "bead": 3.0,
                    "face": 3.0, "stitch": 4.0, "thread": 3.0, "word": 3.0,
                    "hoop": 4.0, "clap": 3.0, "seed": 3.0, "blob": 4.0,
                    "chip": 3.0, "bolt": 5.0, "note": 3.0, "rest": 3.0,
                    "flame": 4.0}

        def _add_bullet(self, x, y, vx, vy, kind="petal", ci=0, sq=4, ay=0.0,
                        sway=0.0, heal=False, ttl=1200, curve=0.0,
                        split=None, turn=None, orbit=None, tether=None,
                        armed_at=0):
            if len(self.bullets) >= TSB_MAX_BULLETS:
                return None
            rb = self.rng.randint(0, TSB_ROT_BUCKETS - 1)
            b = {"x": x, "y": y, "vx": vx, "vy": vy, "kind": kind, "ci": ci,
                "sq": sq, "rb": rb, "ra": rb * TSB_ROT_DEG,
                "rs": self.rng.choice([-1, 1]) * self.rng.uniform(0.6, 1.6),
                "sway": sway, "ph": self.rng.uniform(0, 6.28), "ay": ay,
                "curve": curve, "split": split,
                "turn": turn, "orbit": orbit, "tether": tether,
                "armed_at": max(0, int(armed_at)),
                "age": 0, "fz": 0, "heal": heal, "ttl": ttl}
            self.bullets.append(b)
            return b

        def _add_aimed(self, x, y, tx, ty, speed, **kwargs):
            a = math.atan2(ty - y, tx - x)
            return self._add_bullet(x, y, math.cos(a) * speed,
                                    math.sin(a) * speed, **kwargs)

        def _add_orbit_petal(self, cx, cy, radius, angle, omega, radial=0.0,
                            hold=180, ci=0, sq=4, release=1.5, armed_at=0,
                            kind="petal"):
            # armed_at grace so a formation can MATERIALIZE on its circle
            # without instantly clipping a SOUL that was standing there.
            # A NEGATIVE release sends the body back down its own radius when
            # the orbit ends -- which is how the pincushion's arms retract
            # through the cushion instead of simply switching off.
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            orbit = {"cx": cx, "cy": cy, "radius": radius, "angle": angle,
                    "omega": omega, "radial": radial, "until": hold,
                    "release": release}
            return self._add_bullet(x, y, 0.0, 0.0, kind=kind, ci=ci,
                                    sq=sq, orbit=orbit, ttl=hold + 260,
                                    armed_at=armed_at)

        # Axis wires are the old loom primitive, consolidated into HEMLINE.
        # Diagonal threads let later attacks make cat's-cradle geometry rather
        # than disguising another horizontal/vertical wire sequence.
        def _add_wire(self, orient, pos, ci=5, tel=38, on=24, vol=0.8):
            # vol scales the pluck cue; 0 silences it so simultaneous wires
            # (the overture's chords) sound once instead of stacking copies.
            self.wires.append({"orient": orient, "pos": pos, "born": self.tick,
                                "tel": tel, "on": on, "ci": ci,
                                "killed": False})
            if vol > 0.0:
                tsb_play("wire", vol)

        def _add_thread(self, x1, y1, x2, y2, ci=5, tel=42, on=20,
                        width=5.0):
            self.wires.append({"orient": "d", "x1": x1, "y1": y1,
                                "x2": x2, "y2": y2,
                                "born": self.tick, "tel": tel, "on": on,
                                "ci": ci, "width": float(width),
                                "killed": False})
            tsb_play("wire", 0.72)

        def _kill_wires(self):
            # Stamp the kill moment so the renderer can fade a line out
            # instead of blinking it away mid-frame.
            for w in self.wires:
                if not w.get("killed"):
                    w["killed"] = True
                    w["kill_t"] = self.tick

        def _add_bloom(self, x, y, fuse=42, n=12, ci=0, speed=1.5, spin=0.0):
            self.blooms.append({"x": x, "y": y, "born": self.tick, "fuse": fuse,
                                "n": n, "ci": ci, "speed": speed,
                                "spin": spin})

        def _spawn_needle(self):
            # Her mending, threaded through the attack: a green needle drifts
            # across the box. Catching it heals. More arrive when you're low.
            bx, by, bw, bh = self._box_rect()
            side = self.rng.choice([-1, 1])
            x = bx - 16 if side < 0 else bx + bw + 16
            y = self.rng.uniform(by + 20, by + bh - 20)
            tsb_play("mend")
            self._add_bullet(x, y, -side * self.rng.uniform(0.9, 1.3), 0.0,
                            kind="needle", ci=3, sq=4, sway=0.4, heal=True)

        def _step_bullets(self):
            bx, by, bw, bh = self._box_rect()
            margin = 60.0
            kept = []
            split_specs = []
            hurt = False
            heal_hit = False
            turn_fired = False
            orbit_freed = False
            for b in self.bullets:
                # HOLD: the world stops for this body, and its clock stops
                # with it, so a conductor's cutoff or a curtain-call bow
                # resumes the exact picture the player already read instead
                # of a new one. Nothing on hold can collide -- a frozen
                # bullet sitting on top of you would be a hit that never had
                # an answer.
                if b.get("hold", 0) > 0:
                    b["hold"] -= 1
                    kept.append(b)
                    continue
                b["age"] += 1
                if b["fz"]:
                    b["fz"] -= 1
                    if b["fz"] <= 0:
                        continue
                split = b.get("split")
                if split and b["age"] >= split.get("at", 60):
                    n = max(3, int(split.get("n", 8)))
                    base = split.get("base", self.rng.uniform(0.0, 6.28318))
                    arc = float(split.get("arc", 6.28318))
                    if split.get("aim") is not None:
                        aimx, aimy = split["aim"]
                        base = math.atan2(aimy - b["y"], aimx - b["x"])
                        base -= arc * 0.5
                    for si in range(n):
                        denom = float(n if arc >= 6.28 else max(1, n - 1))
                        a = base + arc * si / denom
                        a += self.rng.uniform(-split.get("jitter", 0.0),
                                            split.get("jitter", 0.0))
                        split_specs.append((b["x"], b["y"], a,
                                            split.get("speed", 1.7),
                                            split.get("ci", b["ci"])))
                    self._spark_burst(b["x"], b["y"], 8, b["ci"], 2.2, 28)
                    continue
                turn = b.get("turn")
                if turn and b["age"] >= int(turn.get("at", 1)):
                    if turn.get("target") is not None:
                        tx, ty = turn["target"]
                        a = math.atan2(ty - b["y"], tx - b["x"])
                        speed = float(turn.get("speed", 2.0))
                        b["vx"] = math.cos(a) * speed
                        b["vy"] = math.sin(a) * speed
                    else:
                        b["vx"] = float(turn.get("vx", b["vx"]))
                        b["vy"] = float(turn.get("vy", b["vy"]))
                    b["ay"] = float(turn.get("ay", b["ay"]))
                    b["curve"] = float(turn.get("curve", b["curve"]))
                    b["turn"] = None
                    b["tether"] = None
                    turn_fired = True
                    self._spark_burst(b["x"], b["y"], 3, b["ci"], 1.2, 20)

                orbit = b.get("orbit")
                if orbit is not None and b["age"] <= int(orbit["until"]):
                    orbit["angle"] += orbit["omega"]
                    orbit["radius"] += orbit["radial"]
                    oa = orbit["angle"]
                    b["x"] = orbit["cx"] + math.cos(oa) * orbit["radius"]
                    b["y"] = orbit["cy"] + math.sin(oa) * orbit["radius"]
                    if b["age"] == int(orbit["until"]):
                        release = float(orbit.get("release", 1.5))
                        b["vx"] = math.cos(oa) * release
                        b["vy"] = math.sin(oa) * release
                        b["orbit"] = None
                        orbit_freed = True
                else:
                    b["vy"] += b["ay"]
                    if b.get("curve"):
                        ca = b["curve"]
                        cs = math.cos(ca)
                        sn = math.sin(ca)
                        ovx = b["vx"]
                        b["vx"] = ovx * cs - b["vy"] * sn
                        b["vy"] = ovx * sn + b["vy"] * cs
                    b["x"] += b["vx"] + (math.sin(b["age"] * 0.07 + b["ph"]) * b["sway"])
                    b["y"] += b["vy"]
                b["ra"] = (b.get("ra", b["rb"] * TSB_ROT_DEG) + b["rs"] * 6.0) % 360.0
                b["rb"] = int(b["ra"] / TSB_ROT_DEG) % TSB_ROT_BUCKETS
                if b["age"] > b["ttl"]:
                    continue
                if (b["x"] < bx - margin or b["x"] > bx + bw + margin
                        or b["y"] < by - margin or b["y"] > by + bh + margin):
                    if b["age"] > 20:
                        continue
                # Collision only while a live pattern is running.
                if (self.mode == "dodge" and not b["fz"]
                        and b["age"] >= b.get("armed_at", 0)):
                    dx = b["x"] - self.px
                    dy = b["y"] - self.py
                    rr = TSBGame.BULLET_R[b["kind"]] + TSB_PLAYER_R
                    if dx * dx + dy * dy <= rr * rr:
                        if b["heal"]:
                            heal_hit = True
                            self._spark_burst(b["x"], b["y"], 8, 3, 2.4, 30)
                            continue
                        if self.tick >= self.inv_until:
                            hurt = TSBGame.BULLET_DMG[b["kind"]]
                kept.append(b)
            self.bullets = kept
            # One cue per tick no matter how many bullets shared the beat --
            # pressed releases four at once, snarl eight -- and only while a
            # live pattern is running, so fade-outs and cinematics stay quiet.
            if self.mode == "dodge":
                if turn_fired:
                    tsb_play("release")
                if orbit_freed:
                    tsb_play("release", 0.7)
                if split_specs:
                    tsb_play("bloom", 0.55)
            for sx, sy, sa, ss, sci in split_specs:
                self._add_bullet(sx, sy, math.cos(sa) * ss,
                                math.sin(sa) * ss, kind="petal",
                                ci=sci, sq=4, curve=0.002 * self.spiral_dir)

            # Wires: telegraph -> live -> cooling fade. The extra retention
            # ticks are VISUAL ONLY -- the renderer's fade-out -- and both
            # collision gates below still end exactly at tel + on.
            wkept = []
            for w in self.wires:
                age = self.tick - w["born"]
                if w["killed"]:
                    if self.tick - w.get("kill_t", w["born"]) > 8:
                        continue
                elif age > w["tel"] + w["on"] + 10:
                    continue
                if (self.mode == "dodge" and not w["killed"]
                        and w["tel"] <= age <= w["tel"] + w["on"]
                        and self.tick >= self.inv_until):
                    if w["orient"] == "h":
                        if abs(self.py - w["pos"]) <= 5.0 + TSB_PLAYER_R:
                            hurt = 4.0
                    elif w["orient"] == "v":
                        if abs(self.px - w["pos"]) <= 5.0 + TSB_PLAYER_R:
                            hurt = 4.0
                    else:
                        # Squared point-to-segment distance.  Diagonal threads
                        # use the same generous SOUL radius as axis wires.
                        x1, y1 = w["x1"], w["y1"]
                        dx = w["x2"] - x1
                        dy = w["y2"] - y1
                        seg2 = dx * dx + dy * dy
                        if seg2 > 0.0001:
                            u = ((self.px - x1) * dx +
                                (self.py - y1) * dy) / seg2
                            u = tsb_clamp(u, 0.0, 1.0)
                            qx = x1 + dx * u
                            qy = y1 + dy * u
                            rr = w.get("width", 5.0) + TSB_PLAYER_R
                            if ((self.px - qx) ** 2 +
                                    (self.py - qy) ** 2 <= rr * rr):
                                hurt = 4.0
                wkept.append(w)
            self.wires = wkept

            # Blooms: a telegraphed point bursts into a FULL ring. You dodge
            # the ring by not being near it, or by slipping between spokes.
            bkept = []
            for bl in self.blooms:
                if self.tick - bl["born"] >= bl["fuse"]:
                    tsb_play("bloom")
                    # The head bursts with a petal shower behind the ring --
                    # cosmetic, but it makes every detonation read as a flower
                    # coming apart rather than a ring appearing.
                    self._spark_burst(bl["x"], bl["y"], 9, bl["ci"], 2.4, 26)
                    n = bl["n"]
                    for i in range(n):
                        a = ((6.28318 / n) * i + bl.get("spin", 0.0) +
                            self.rng.uniform(-0.035, 0.035))
                        self._add_bullet(bl["x"], bl["y"],
                                        math.cos(a) * bl["speed"],
                                        math.sin(a) * bl["speed"],
                                        kind="pellet", ci=bl["ci"], sq=4)
                else:
                    bkept.append(bl)
            self.blooms = bkept

            if heal_hit:
                self.hp = min(TSB_HP_MAX, self.hp + TSB_HEAL_HP)
                tsb_play("heal", 0.9)
                self._pop(self.px, self.py - 16, "+%d" % int(TSB_HEAL_HP), 3)
            if hurt:
                self._take_hit(hurt)

        def _take_hit(self, dmg):
            if self.guard_charges > 0:
                self.guard_charges -= 1
                dmg = max(1.0, math.ceil(dmg * 0.5))
                self._pop(self.px, self.py - 22, "GUARD", 9)
            self.hp = max(0.0, self.hp - dmg)
            self.inv_until = self.tick + TSB_INV_TICKS + self.invuln_bonus
            self.invuln_bonus = 0
            tsb_play("hurt")
            self._spark_burst(self.px, self.py, 10, 0, 3.0, 32)
            if self.hp <= 0.0:
                self.heart_break = self.tick
                tsb_play("break")
                self._set_mode("dead")

        def _dodge_common(self, t):
            # ---- THE HOUSE LIGHT: the fight's one universal anti-camp ------
            # Every move here can be read once and then answered by finding
            # the emptiest corner and living in it, which is both the least
            # interesting way to play and the exact opposite of what this
            # fight is about. So the room notices. Hold still inside a small
            # circle for two and a half seconds and the light finds you --
            # sparks and a glint on your own feet -- and a whole ring opens
            # off that mark a beat later.
            # Contract, so this never becomes the thing it's fixing:
            #   * It can only fire at someone who ISN'T dodging. Any real
            #     movement resets the clock, so a player being walked around
            #     the room by the pattern never sees it once.
            #   * The mark is STALE and the ring is WHOLE -- no gap, no aim,
            #     no chase. Walking away is always the answer and is always
            #     possible; the ring opens behind you.
            #   * Off during the overture, whose coda deliberately asks you
            #     to hold a pose, and off during the collapse, which is not
            #     supposed to be a threat at all.
            # FEEDBACK is excluded because holding still is what it is
            # ASKING for; catching a player out for obeying a cue would be
            # the exact opposite of a backstop.
            if self.pattern not in ("overture", "limp", "feedback"):
                if (abs(self.px - self.camp_x) > 26.0
                        or abs(self.py - self.camp_y) > 26.0):
                    self.camp_x = self.px
                    self.camp_y = self.py
                    self.camp_since = t
                elif t - self.camp_since >= 150:
                    # Cooldown is folded into the anchor: a player who plants
                    # again gets found again, on the same unhurried count.
                    self.camp_since = t + 60
                    self._spark_burst(self.px, self.py, 8, 8, 1.7, 30)
                    tsb_play("glint", 0.95)
                    self._add_bloom(self.px, self.py, fuse=46, n=12, ci=8,
                                    speed=1.9, spin=self.spiral_a)

            # Her mending, threaded through the attack. Each needle is worth
            # a single stitch (TSB_HEAL_HP = 1), so even the boosted low-HP
            # cadence is triage, not sustain.
            if self.turn >= 1 or self.phase == 2:
                every = 120 if (self.hp <= 8.0 or self.needle_turns > 0) else 220
                if t >= 90 and (t - 90) % every == 0:
                    self._spawn_needle()
            # Phase-2 string spasms, layered over whatever pattern is running:
            # off the beat, a stray handful tears loose from above the box.
            # Always telegraphed -- a twang and a spark shower half a second
            # ahead at the exact release point -- and worse the fewer threads
            # are holding her, because what's left carries more of the load.
            #
            # Deliberately NOT aimed at the SOUL: a homing volley on top of a
            # wall or the twin drifts pincers the player against bullets they
            # were already committed to dodging. Instead it drops a fixed
            # downward fan at the telegraphed column -- a hazard you route
            # around, so it raises the read without closing the pattern's
            # own safe path.
            # ...and the spasm layer stays off feedback for the same
            # reason: its loud window forbids moving, and a fan arriving
            # inside that window would have no answer at all.
            if self.phase == 2 and self.pattern not in ("limp", "feedback"):
                sc = self.pat_scratch
                if "spasm_next" not in sc:
                    sc["spasm_next"] = self.rng.randint(180, 260)
                if t == sc["spasm_next"]:
                    bx, by, bw, bh = self._box_rect()
                    x = self.rng.uniform(bx + 30, bx + bw - 30)
                    sc["spasm_x"] = x
                    sc["spasm_at"] = t + 36
                    self._spark_burst(x, by - 8, 7, 5, 1.6, 34, 1.2)
                    tsb_play("wire", 0.5)
                    gap = max(132, 220 - 16 * self.strings_cut)
                    sc["spasm_next"] = t + gap + self.rng.randint(0, 70)
                if sc.get("spasm_at") == t:
                    tsb_play("throw", 0.8)
                    bx, by, bw, bh = self._box_rect()
                    x = sc.get("spasm_x", bx + bw * 0.5)
                    n = 2 + min(2, self.strings_cut)
                    spread = 0.20 + 0.05 * self.strings_cut
                    for k in range(n):
                        a = math.pi * 0.5 + (k - (n - 1) * 0.5) * spread
                        s = 2.4
                        self._add_bullet(x, by - 8, math.cos(a) * s,
                                        math.sin(a) * s, kind="petal",
                                        ci=5, sq=3)

        # ----- patterns ---------------------------------------------------------
        # Rebuilt from a blank slate 2026-08-29. The roster this replaced was
        # competently made and completely generic: strip the theater names off
        # it and what was left was rain from an edge, ranks crossing the box,
        # rings opening, and shots aimed at a stale mark -- danmaku grammar in
        # a marionette's costume. Every move asked the player the same
        # question, which is "where are the bullets not," and that question
        # has nothing to do with this fight.
        #
        # THE RULE THIS PASS IS BUILT ON:
        #   EVERY MOVE MUST ASK A VERB THAT ISN'T "AVOID."
        # Walk through a crowd. Stand on the mark. Hold still. Pull against
        # the string until it breaks. Learn the phrase and get there first.
        # Read the line before the pen finishes it. Stay in the light. Go and
        # fetch the light. Don't cross the axis your reflection is on. If the
        # honest answer to a move is "stand where nothing is going," the move
        # is not finished, no matter how good its name is.
        #
        # It is also what makes the roster read as HERS. She is somebody who
        # was told where to stand, told when to be quiet, and taken in at the
        # seams until she fit -- so the attacks are marks, cues, seams,
        # strings and lights, and the player spends the fight being STAGED.
        # The theming lives in the mechanic. No line of dialogue explains it.
        #
        # THE FAIRNESS CONTRACT (unchanged; it survived the rebuild intact):
        #   * One idea per move. A secondary emitter exists only to answer
        #     camping, and stays sparse (40+ tick cadence).
        #   * Streams keep real daylight between consecutive bullets unless
        #     the stream IS the object (metronome's baton), in which case its
        #     lateral sweep stays under the SOUL's 3.7 px/tick.
        #   * Ranks are evenly spaced -- 42px+ between centers, no missing-
        #     lane doors -- and two ranks NEVER interpenetrate with
        #     mismatched offsets.
        #   * Anything aimed commits to a STALE position sampled at telegraph
        #     time, and every telegraph is visible AND audible.
        #   * Randomness is spent at telegraph time -- placement, order,
        #     timing -- never on a bullet already in flight.
        #   * dens tightens cadence toward per-move floors; it is never
        #     allowed to break the spacing contracts above.
        #   * NO MOVE MAY CONTAIN A SPOT THAT SURVIVES THE WHOLE MOVE. A
        #     quiet region may exist; it may not STAY. Something visits it on
        #     a readable schedule. The house light in _dodge_common is the
        #     BACKSTOP for this, never the plan.
        #   * A move whose opening beat lands ON the SOUL gets a count-in
        #     (LEAD_IN). Stale aim is fair once you know the move; on rep one
        #     it arrives while the player is still finding the box.
        #
        # THE FOUR VERBS THE ENGINE LEARNED FOR THIS PASS, and the state each
        # costs (set up in __init__, applied in _step_dodge, cleared per move
        # in _begin_dodge):
        #   drag_x/drag_y    a per-tick displacement added to the SOUL AFTER
        #                    its own input. This is the fight in one variable:
        #                    something else has a say in where you are.
        #   move_vx/move_vy  the player's INPUT direction and magnitude, so a
        #   move_amt         move can ask you to push against a pull, or to
        #                    hold still, without reading the drag back out.
        #   mark             a lit place on the boards the show wants you on
        #                    (good=True) or off (good=False).
        #   blackout/loud    the two states of the room: too dark, too loud.
        # None of the four is a hazard. All four are instructions.

        # -- INTRO: CURTAIN UP ------------------------------------------------
        # The opening number, and the only move allowed to be a medley,
        # because it is a syllabus: it teaches every verb the fight will ask
        # for, in the order it will ask them, before the first menu.
        #   I.   HOUSE LIGHTS DOWN -- an audience gathers and drifts up
        #        through the room. None of it is aimed at you. Walk through a
        #        crowd. (VERB: navigate)
        #   II.  YOUR MARK -- a spike-tape cross snaps onto the boards and
        #        then WALKS. On it, you are fine. Off it, the boards where
        #        you are standing light up. (VERB: be somewhere specific)
        #   III. THE STRINGS FIND YOU -- a hook comes down, takes the SOUL,
        #        and pulls. You can still walk. The room walks you further.
        #        (VERB: lean against it)
        #   IV.  TAKE YOUR BOW -- her five threads come down across the room
        #        into a cage one cell wide, with the mark standing in the
        #        cell she means, on the longest tell in the fight. The number
        #        ends on a held pose. (VERB: stand still, on purpose)
        # Forced by the intro by name; in neither turn table; never returns.

        def _pat_overture(self, t, dens):
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            cx = bx + bw * 0.5
            cy = by + bh * 0.5

            # --- I. HOUSE LIGHTS DOWN (0..190, and the house never empties) -
            # Nine columns, and consecutive faces step one column over, so
            # the room fills as readable diagonals instead of static. They
            # drift UP with the stage, at a third of walking speed.
            if t < 700 and t % (7 if t < 190 else 15) == 0:
                col = (t // 7) % 9
                self._add_bullet(bx + bw * (col + 0.5) / 9.0
                                + self.rng.uniform(-4, 4),
                                by + bh + 14, 0.0, -1.15, kind="face",
                                ci=7, sq=3, sway=0.22, ttl=400)
                if t % 63 == 0:
                    tsb_play("glint", 0.25)

            # --- II. YOUR MARK (190..400) -----------------------------------
            if t == 190:
                tsb_play("wire", 0.7)
                sc["mark_i"] = -1
            if 190 <= t < 400:
                # Four stops and home, each announced by a ghost cross 26
                # ticks before the light actually moves.
                stops = ((0.50, 0.50), (0.26, 0.30), (0.74, 0.34),
                        (0.70, 0.72), (0.28, 0.68))
                step = min((t - 190) // 42, len(stops) - 1)
                if step != sc.get("mark_i"):
                    sc["mark_i"] = step
                    fx, fy = stops[step]
                    self.mark = {"x": bx + bw * fx, "y": by + bh * fy,
                                "r": 36.0, "good": True}
                    tsb_play("glint", 0.85)
                    self._spark_burst(self.mark["x"], self.mark["y"],
                                        6, 8, 1.3, 26)
                nxt = step + 1
                if self.mark is not None:
                    if nxt < len(stops) and (t - 190) % 42 >= 26:
                        fx, fy = stops[nxt]
                        self.mark["gx"] = bx + bw * fx
                        self.mark["gy"] = by + bh * fy
                    else:
                        self.mark.pop("gx", None)
                        self.mark.pop("gy", None)
                # Off the mark, the boards under you notice. Stale spot,
                # whole ring, and it opens behind an audience member who is
                # already walking.
                if (t - 190) % 30 == 20 and self.mark is not None:
                    dx = self.px - self.mark["x"]
                    dy = self.py - self.mark["y"]
                    if dx * dx + dy * dy > self.mark["r"] ** 2:
                        self._spark_burst(self.px, self.py, 7, 8, 1.5, 28)
                        tsb_play("glint", 0.7)
                        self._add_bloom(self.px, self.py, fuse=40, n=10,
                                        ci=8, speed=1.9, spin=self.spiral_a)
            if t == 400:
                self.mark = None

            # --- III. THE STRINGS FIND YOU (400..646) -----------------------
            if t == 400:
                tsb_play("wire", 1.0)
                self._spark_burst(cx, by - 6, 10, 5, 1.8, 36, 1.4)
            if t == 520:
                tsb_play("wire", 0.9)
                self._spark_burst(cx, by + bh + 6, 10, 5, 1.8, 36, -1.4)
            if 400 <= t < 646:
                hooks = []
                hooks.append({"ax": bx + bw * tsb_sweep(t - 400, 300,
                                                        0.12, 0.88),
                            "ay": by - 26.0, "ci": 5})
                if t >= 520:
                    hooks.append({"ax": bx + bw * tsb_sweep(t - 520, 260,
                                                            0.86, 0.14),
                                "ay": by + bh + 26.0, "ci": 5})
                self.hooks = hooks
                pull = 0.30 if t < 520 else 0.26
                for hk in hooks:
                    hx = hk["ax"] - self.px
                    hy = hk["ay"] - self.py
                    d = math.hypot(hx, hy) or 1.0
                    self.drag_x += hx / d * pull
                    self.drag_y += hy / d * pull
                # An honest comb crossing underneath it, so the pull is
                # something you spend movement fighting and not a mood.
                if t % 17 == 0:
                    self._add_bullet(bx + bw * tsb_sweep(t, 190, 0.06, 0.94),
                                    by - 12, 0.0, 2.0, kind="petal",
                                    ci=1, sq=3, sway=0.28)
            if t == 646:
                self.hooks = []
                tsb_play("snap", 0.8)
                self._spark_burst(self.px, self.py, 12, 2, 2.6, 30)

            # --- IV. TAKE YOUR BOW (650..780) -------------------------------
            if t == 650:
                tsb_play("wire", 1.0)
                for k in (1, 2, 3, 4, 5):
                    self._add_wire("v", bx + bw * (k / 6.0), tel=76, on=54,
                                    vol=(0.9 if k == 1 else 0.0))
                for k in (1, 2):
                    self._add_wire("h", by + bh * (k / 3.0), tel=88, on=42,
                                    vol=0.0)
                self.mark = {"x": bx + bw * (2.5 / 6.0),
                            "y": by + bh * 0.5, "r": 30.0, "good": True}
            if 650 <= t < 760 and t % 6 == 0:
                # Sparks running down the live threads: the cage is a thing
                # under tension, not a decal.
                k = ((t - 650) // 6) % 5 + 1
                self._spark_burst(bx + bw * (k / 6.0),
                                by + self.rng.uniform(10, bh - 10),
                                2, 5, 0.9, 18)
            if t == 762:
                self.mark = None
                self._kill_wires()
                tsb_play("release", 1.0)

            # In the rests she still slips you a green one -- mid-overture,
            # mid-possession; the habit the show never managed to rewrite.
            if t in (300, 600):
                self._spawn_needle()

        # ============ SHARED: taught clean, returned damaged =================

        def _pat_camellia(self, t, dens):
            """THE FLOWER THAT FALLS WHOLE.

            A camellia does not shed. The whole head comes off at once, which
            is why people used to call it an unlucky flower to give a soldier,
            and it is why this fight is full of them. So: seven heads hang
            from the rigging on visible drop-lines and let go in a travelling
            run you can count -- left to right, then back, half a lane over.
            A head that LANDS bursts along the boards, so the floor is denied
            in a wave that walks the room while the ceiling is still full of
            the ones that haven't gone yet.

            VERB: travel with a run, and never own the floor.
            Phase 2 breaks the run into a broken chord -- two heads arriving
            together, out of order -- and throws the burst UP instead of out,
            so the middle band stops being a refuge."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            lanes = 7
            lane_w = bw / float(lanes)
            cycle = max(150, int(200 / dens))
            # A move's first tick is active_t 1, not 0, so the count
            # starts at (t - 1): otherwise the opening measure -- and
            # the setup that hangs off its downbeat -- is skipped.
            beat = (t - 1) % cycle
            drop = 2.5 + 0.25 * dens
            if beat == 0:
                # Re-hang the rail. Every pass is offset half a lane from the
                # last, so the column that was clear is the column that isn't.
                run = (t - 1) // cycle
                off = 0.5 if run % 2 else 0.0
                order = list(range(lanes))
                if run % 2:
                    order.reverse()
                if self.phase == 2:
                    for i in range(lanes - 1):
                        if self.rng.random() < 0.34:
                            order[i], order[i + 1] = order[i + 1], order[i]
                sc["hung"] = []
                tsb_play("glint", 0.9)
                gap = max(11, int(15 / dens))
                for slot, lane in enumerate(order):
                    x = bx + (lane + 0.5 + off) * lane_w
                    if x > bx + bw - 10:
                        x -= bw
                    at = 44 + slot * gap
                    if self.phase == 2 and slot % 3 == 2:
                        at -= gap // 2
                    b = self._add_bullet(x, by + 16, 0.0, 0.0,
                                        kind="bigpetal", ci=0, sq=4,
                                        turn={"at": at, "vx": 0.0,
                                                "vy": drop},
                                        tether={"x": x, "y": by + bh - 8,
                                                "until": at},
                                        armed_at=at - 6, ttl=at + 220)
                    if b is not None:
                        sc["hung"].append(
                            (t + at + int((bh - 30.0) / drop), x))
            # The landing. A head that reaches the boards comes apart along
            # them; back here it comes apart upward instead.
            due = [d for d in sc.get("hung", ()) if d[0] <= t]
            if due:
                sc["hung"] = [d for d in sc["hung"] if d[0] > t]
                for _at, x in due:
                    tsb_play("bloom", 0.55)
                    self._spark_burst(x, by + bh - 8, 7, 0, 2.0, 24, 1.2)
                    if self.phase == 1:
                        for s in (-1.0, 1.0):
                            for j in range(2):
                                self._add_bullet(x, by + bh - 10,
                                                s * (2.0 + 0.4 * j),
                                                -0.55 - 0.35 * j,
                                                kind="petal", ci=1, sq=3,
                                                ay=0.030)
                    else:
                        for j in range(5):
                            a = -math.pi * (0.24 + 0.13 * j)
                            self._add_bullet(x, by + bh - 10,
                                            math.cos(a) * 2.3,
                                            math.sin(a) * 2.3,
                                            kind="petal", ci=6, sq=3,
                                            ay=0.014)
            # The rail is at the ceiling and the bursts are at the floor, so
            # the middle band would otherwise be a home. One bead paces it.
            if beat % 46 == 24:
                self._add_bullet(bx - 12,
                                by + bh * tsb_sweep(t, 240, 0.28, 0.72),
                                1.9, 0.0, kind="bead", ci=7, sq=3)

        def _pat_hemline(self, t, dens):
            """TAKEN IN.

            A running stitch sews itself across the room, one stitch every
            few ticks, harmless while the needle is still going -- and then
            the thread is PULLED. Every stitch on that seam snaps toward the
            middle of the line at once, gathering the cloth, and the box is
            gathered with it: the room is taken in by exactly what the seam
            took up, holds there, and eases back out.

            VERB: read a line while it is being drawn, be off it when it
            pulls, and then live in a smaller room than you agreed to.
            Phase 2 lays a second seam on the other axis, gathers both toward
            YOUR stale mark instead of the seam's middle, and does not give
            the room all the way back."""
            bx, by, bw, bh = self._box_rect()
            base_w, base_h = TSBGame.DODGE_BOX["hemline"]
            sc = self.pat_scratch
            cycle = max(168, int(210 / dens))
            # A move's first tick is active_t 1, not 0, so the count
            # starts at (t - 1): otherwise the opening measure -- and
            # the setup that hangs off its downbeat -- is skipped.
            beat = (t - 1) % cycle
            n = 15
            lay_every = 4
            pull_at = 4 + n * lay_every + 16

            if beat == 0:
                sc["pass"] = (t - 1) // cycle
                sc["frac"] = tsb_sweep(t, 620, 0.24, 0.76)
                sc["gather"] = 0.0
                sc["horiz"] = (self.phase == 1 or sc["pass"] % 2 == 0)
                if self.phase == 2:
                    sc["keep"] = min(0.50, sc.get("keep", 0.0) + 0.16)
                else:
                    sc["keep"] = 0.0
                tsb_play("wire", 0.5)
            horiz = sc.get("horiz", True)
            if 4 <= beat < 4 + n * lay_every and (beat - 4) % lay_every == 0:
                i = (beat - 4) // lay_every
                if horiz:
                    y = by + bh * sc["frac"]
                    x = bx + (i + 0.5) * bw / float(n)
                    tx, ty = bx + bw * 0.5, y
                else:
                    x = bx + bw * sc["frac"]
                    y = by + (i + 0.5) * bh / float(n)
                    tx, ty = x, by + bh * 0.5
                if self.phase == 2:
                    tx = tsb_clamp(self.px, bx + 30, bx + bw - 30)
                    ty = tsb_clamp(self.py, by + 26, by + bh - 26)
                at = pull_at - (4 + i * lay_every)
                self._add_bullet(x, y, 0.0, 0.0, kind="stitch", ci=5, sq=4,
                                turn={"at": at, "target": (tx, ty),
                                        "speed": 3.1},
                                tether={"x": tx, "y": ty, "until": at},
                                armed_at=at - 5, ttl=at + 200)
                if i % 4 == 0:
                    tsb_play("throw", 0.45)
                if self.phase == 2 and i == n // 2:
                    # The cross seam, laid all at once. Both gather on the
                    # same tick, toward the same mark.
                    for j in range(n):
                        if horiz:
                            x2 = bx + bw * (1.0 - sc["frac"])
                            y2 = by + (j + 0.5) * bh / float(n)
                        else:
                            x2 = bx + (j + 0.5) * bw / float(n)
                            y2 = by + bh * (1.0 - sc["frac"])
                        self._add_bullet(x2, y2, 0.0, 0.0, kind="stitch",
                                        ci=6, sq=3,
                                        turn={"at": at, "target": (tx, ty),
                                                "speed": 2.9},
                                        tether={"x": tx, "y": ty,
                                                "until": at},
                                        armed_at=at - 5, ttl=at + 200)
            if beat == pull_at:
                tsb_play("snap", 0.75)
                self._spark_burst(bx + bw * 0.5, by + bh * 0.5, 10, 5,
                                    2.4, 30)
                sc["gather"] = 1.0
            # The room is gathered with the cloth: it comes in on the axis
            # the seam ran along, holds, and eases back out.
            if sc.get("gather", 0.0) > 0.0:
                held = beat - pull_at
                if held < 34:
                    amt = 1.0
                else:
                    amt = max(sc.get("keep", 0.0), 1.0 - (held - 34) / 46.0)
                take = 62.0 * amt
                if horiz:
                    self.box_target = [TSB_BOX_CX, TSB_BOX_CY,
                                        base_w, base_h - take]
                else:
                    self.box_target = [TSB_BOX_CX, TSB_BOX_CY,
                                        base_w - take, base_h]
            # Loose thread: whatever the gather squeezes out has to go
            # somewhere, and it paces the width on the way.
            if beat > pull_at and beat % 22 == 3:
                self._add_bullet(bx + bw * tsb_sweep(t, 210, 0.08, 0.92),
                                by - 10, 0.0, 1.75, kind="thread", ci=7,
                                sq=3, sway=0.45)

        def _pat_metronome(self, t, dens):
            """THE CONDUCTOR.

            The one sanctioned solid stream in the fight, because here the
            stream IS the object: a baton swung from the top of the room,
            throwing a line of notes whose landing point sweeps the boards
            slower than you walk. It runs an accelerando you can hear, and on
            each counted tock the tip flicks a whole camellia head into the
            corner it is pointing at -- which is exactly where a player who
            has decided to outrun it ends up standing. Every fourth tock is a
            DOWNBEAT: the arm comes up, and the middle of the room goes.

            VERB: stay ahead of a sweep you cannot outrun forever, and clear
            the middle when the arm comes up.
            Phase 2 conducts a fermata (the beam freezes mid-swing and
            resumes REVERSED) and a CUTOFF: every note already in the air
            hangs motionless for half a second, then carries on from where it
            hung. The picture you read is still the picture. Only later."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            if "ph" not in sc:
                sc["ph"] = 1.5708 * self.spiral_dir
                sc["dir"] = self.spiral_dir
                sc["freeze"] = 0
                sc["side"] = 0
                sc["tocks"] = 0
                sc["cut"] = (self.rng.randint(150, 210)
                            if self.phase == 2 else 10 ** 9)
            # Accelerando, capped: at bh 264 and amp 0.55 the fastest lateral
            # travel of the landing point is 3.6 px/tick, under the SOUL's
            # 3.7. That ceiling is this move's whole fairness argument.
            rate = min(0.0250,
                        0.0195 + 0.0000135 * t + 0.0016 * (dens - 1.0))
            if self.phase == 2:
                if sc["freeze"] > 0:
                    sc["freeze"] -= 1
                    if sc["freeze"] == 0:
                        sc["dir"] *= -1.0
                        tsb_play("glint", 0.8)
                elif (t > 90 and abs(math.sin(sc["ph"])) < 0.7
                        and self.rng.random() < 0.006):
                    sc["freeze"] = 34
                    self._spark_burst(bx + bw * 0.5, by + 6, 8, 5, 1.5, 30)
                    tsb_play("wire", 0.4)
                if t == sc["cut"]:
                    tsb_play("wire", 0.9)
                    for b in self.bullets:
                        if not b.get("heal"):
                            b["hold"] = 34
                    sc["cut"] = t + self.rng.randint(170, 240)
            if sc["freeze"] == 0:
                sc["ph"] += rate * sc["dir"]
            swing = math.sin(sc["ph"])
            amp = 0.55
            ang = math.pi * 0.5 + amp * swing
            if sc["freeze"] == 0 and t % 4 == 0:
                emit = t // 4
                self._add_bullet(bx + bw * 0.5, by + 4,
                                math.cos(ang) * 2.5, math.sin(ang) * 2.5,
                                kind="note" if emit % 3 else "rest",
                                ci=5, sq=3)
                if emit % 9 == 0:
                    tsb_play("throw", 0.5)
            side = 1 if swing > 0.985 else (-1 if swing < -0.985 else 0)
            if side != 0 and side != sc["side"]:
                sc["side"] = side
                sc["tocks"] += 1
                if sc["tocks"] % 4 == 0:
                    # THE DOWNBEAT: five evenly spaced heads, 44px apart, the
                    # outer ones released higher so the shape arrives as a
                    # chevron and reads a beat before it is dangerous.
                    tsb_play("volley", 1.0)
                    self._spark_burst(bx + bw * 0.5, by + 8, 10, 6, 2.0, 30)
                    for i in range(5):
                        self._add_bullet(bx + bw * 0.5 + (i - 2) * 44.0,
                                        by - 16 - abs(i - 2) * 12.0,
                                        0.0, 2.9, kind="bigpetal",
                                        ci=6, sq=4, ttl=220)
                else:
                    tipx = tsb_clamp(bx + bw * 0.5
                                    + math.tan(amp * side) * bh,
                                    bx + 16, bx + bw - 16)
                    self._spark_burst(tipx, by + 12, 5, 6, 1.2, 24)
                    tsb_play("volley2", 0.75)
                    self._add_bullet(tipx, by - 12, 0.0, 0.5,
                                    kind="bigpetal", ci=6, sq=4,
                                    ay=0.065, ttl=260)
            elif abs(swing) < 0.9:
                sc["side"] = 0

        def _pat_limelight(self, t, dens):
            """THE SPOT.

            Inverted, and the inversion is what makes it hers: the lit circle
            is the SAFE place. It walks a slow circuit and it BURNS what
            falls into it -- anything entering the spot goes out with a spark
            -- while everywhere else the room rains. So the move is not
            "dodge the rain." It is "be where the show wants you," which is
            the sentence this whole fight is about.

            And then the lamp fails. Every so often the spot gutters out for
            a couple of seconds, the rain owns the room, and it relights
            somewhere else, and you have to get there.

            VERB: ride a moving shelter, and survive its failures.
            Phase 2 shrinks the spot the entire time it is lit, down to a
            pinpoint, before it gives out."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            if "lit" not in sc:
                sc["lit"] = True
                sc["at"] = 0
                sc["span"] = max(150, int(210 / dens))
            age = t - sc["at"]
            if age >= sc["span"]:
                sc["at"] = t
                sc["lit"] = not sc["lit"]
                if sc["lit"]:
                    sc["span"] = max(150, int(210 / dens))
                    tsb_play("glint", 1.0)
                else:
                    sc["span"] = 96 if self.phase == 1 else 108
                    tsb_play("wire", 0.55)
                    if self.mark is not None:
                        self._spark_burst(self.mark["x"], self.mark["y"],
                                            10, 7, 2.0, 30)
                    self.mark = None
                age = 0
            if sc["lit"]:
                # The circuit: a wide, unhurried lissajous that visits every
                # quarter of the room inside one lit period.
                a = t * 0.0135
                r0 = 54.0 if self.phase == 1 else 50.0
                if self.phase == 2:
                    r0 *= max(0.34, 1.0 - age / float(sc["span"]) * 0.72)
                mx = bx + bw * (0.5 + 0.30 * math.sin(a))
                my = by + bh * (0.5 + 0.26 * math.sin(a * 1.43 + 1.1))
                self.mark = {"x": mx, "y": my, "r": r0, "good": True}
                r2 = r0 * r0
                for b in self.bullets:
                    if b.get("heal") or b.get("burnt"):
                        continue
                    if (b["x"] - mx) ** 2 + (b["y"] - my) ** 2 <= r2:
                        b["burnt"] = True
                        b["ttl"] = 0
                        self._spark_burst(b["x"], b["y"], 3, 8, 1.2, 16)
            # The rain, paced, so the dark part of the room is a curtain with
            # a direction and not a hat.
            period = max(6, int((9 if sc["lit"] else 7) / dens))
            if t % period == 0:
                self._add_bullet(bx + bw * tsb_sweep(t, 230, 0.05, 0.95),
                                by - 12, 0.0, 2.2 + 0.2 * dens,
                                kind="spark", ci=7, sq=3, sway=0.30)
            if not sc["lit"] and t % max(14, int(19 / dens)) == 9:
                # Dark, so the room gets its second axis back as well.
                left = (t // 26) % 2 == 0
                self._add_bullet(bx - 12 if left else bx + bw + 12,
                                by + bh * tsb_sweep(t, 170, 0.10, 0.90),
                                2.3 if left else -2.3, 0.0,
                                kind="spark", ci=7, sq=3)

        def _pat_ovation(self, t, dens):
            """THE HOUSE APPLAUDS.

            She hates loud noises. So the house claps.

            Each clap is a shockwave off the rim: two dozen bodies placed
            evenly all the way around the box, every one of them travelling
            inward. They converge, cross the middle, and open out the far
            side -- which means the center is where they are densest and the
            rim is where they have just left. The place to be is the place
            the last clap came FROM. Between claps there is nothing at all,
            silence you can hear, and every third clap makes her FLINCH,
            which moves the walls under your feet.

            VERB: count a rhythm, live off-center, ride the lurch.
            Phase 2 puts the flinch BEFORE the clap, so the room moving is
            the count-in, and the applause never quite stops."""
            bx, by, bw, bh = self._box_rect()
            base_w, base_h = TSBGame.DODGE_BOX["ovation"]
            sc = self.pat_scratch
            if "next" not in sc:
                sc["next"] = 34
                sc["n"] = 0
                sc["lurch"] = 0
                sc["lx"] = 0.0
            gap = max(64, int((104 if self.phase == 1 else 88) / dens))
            if self.phase == 2 and t == sc["next"] - 26:
                sc["lurch"] = t
                sc["lx"] = self.rng.choice([-1.0, 1.0]) * 24.0
                tsb_play("wire", 0.4)
            if t == sc["next"]:
                sc["n"] += 1
                sc["next"] = t + gap - (6 if sc["n"] % 3 == 0 else 0)
                tsb_play("volley", 1.0)
                cx = bx + bw * 0.5
                cy = by + bh * 0.5
                count = 22 if self.phase == 1 else 24
                seam = 0.5 * sc["n"]
                speed = 2.0 + 0.16 * dens
                per = 2.0 * (bw + bh)
                for i in range(count):
                    # Placed by PERIMETER, not by angle, so the spacing along
                    # the rim stays even in a rectangle instead of bunching
                    # up at the corners.
                    p = ((i + seam) % count) / float(count) * per
                    if p < bw:
                        x, y = bx + p, by - 10
                    elif p < bw + bh:
                        x, y = bx + bw + 10, by + (p - bw)
                    elif p < 2 * bw + bh:
                        x, y = bx + bw - (p - bw - bh), by + bh + 10
                    else:
                        x, y = bx - 10, by + bh - (p - 2 * bw - bh)
                    self._add_aimed(x, y, cx, cy, speed, kind="clap",
                                    ci=0 if i % 2 else 1, sq=3, ttl=320)
                if self.phase == 1 and sc["n"] % 3 == 0:
                    sc["lurch"] = t
                    sc["lx"] = self.rng.choice([-1.0, 1.0]) * 22.0
                    self.shake = max(self.shake, 16)
                elif self.phase == 2:
                    self.shake = max(self.shake, 12)
            # The flinch: the room jolts and eases back. She is the one being
            # applauded, and she cannot stand it.
            lurch_age = t - sc["lurch"]
            if sc["lurch"] and lurch_age < 44:
                u = 1.0 - lurch_age / 44.0
                self.box_target = [TSB_BOX_CX + sc["lx"] * u * u,
                                    TSB_BOX_CY, base_w, base_h]
            else:
                self.box_target = [TSB_BOX_CX, TSB_BOX_CY, base_w, base_h]
            # One slow flower crosses the silences, so a rest is a rest and
            # not a break.
            if t > 60 and (t + gap // 2) % gap == 0:
                left = (t // gap) % 2 == 0
                self._add_bullet(bx - 14 if left else bx + bw + 14,
                                by + bh * tsb_sweep(t, 260, 0.14, 0.86),
                                1.5 if left else -1.5, 0.0,
                                kind="petal", ci=7, sq=3, sway=0.5)

        def _pat_understudy(self, t, dens):
            """THE UNDERSTUDY.

            Somebody else is learning your part. A second SOUL comes in and
            copies you -- exactly, mirrored across the middle of the room --
            so the axis between the two of you is a place neither can be, and
            the room becomes two rooms with a wall you are drawing yourself.
            Watching the mirror is watching your own movement from outside,
            which is the closest this fight gets to saying out loud what
            happened to her, and it never says it.

            Then it has the part. The copy stops copying, comes for you once,
            and goes. The next one mirrors the OTHER axis.

            VERB: keep off the axis your reflection is on.
            Phase 2 mirrors you on a DELAY -- it plays back where you were
            half a second ago -- which is far worse, because it can no longer
            be solved by standing still."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            cx = bx + bw * 0.5
            cy = by + bh * 0.5
            if "axis" not in sc:
                sc["axis"] = 0
                sc["cast"] = None
                sc["born"] = 26
                sc["hist"] = []
            sc["hist"].append((self.px, self.py))
            if len(sc["hist"]) > 60:
                sc["hist"].pop(0)
            learn = 190 if self.phase == 1 else 168
            if sc["cast"] is None and t >= sc["born"]:
                sc["cast"] = self._add_bullet(cx, cy, 0.0, 0.0, kind="soul",
                                            ci=1, sq=4, ttl=learn + 260,
                                            armed_at=34)
                sc["cast_at"] = t
                sc["taken"] = False
                tsb_play("glint", 0.9)
            cast = sc.get("cast")
            if cast is not None and not sc.get("taken"):
                age = t - sc["cast_at"]
                if age >= learn:
                    # It has the part. One committed charge, telegraphed on
                    # its own thread, and then it is somebody else's problem.
                    sc["taken"] = True
                    cast["vx"] = 0.0
                    cast["vy"] = 0.0
                    cast["turn"] = {"at": cast["age"] + 26,
                                    "target": (self.px, self.py),
                                    "speed": 2.7}
                    cast["tether"] = {"x": self.px, "y": self.py,
                                        "until": cast["age"] + 26}
                    self._spark_burst(cast["x"], cast["y"], 8, 1, 2.0, 28)
                    tsb_play("volley2", 0.9)
                    sc["axis"] = (sc["axis"] + 1) % 3
                    sc["born"] = t + 92
                    sc["cast"] = None
                else:
                    if self.phase == 1:
                        sx, sy = self.px, self.py
                    else:
                        sx, sy = sc["hist"][-min(len(sc["hist"]), 34)]
                    ax = sc["axis"]
                    tx = (2.0 * cx - sx) if ax in (0, 2) else sx
                    ty = (2.0 * cy - sy) if ax in (1, 2) else sy
                    # It EASES onto its reflection instead of snapping to it.
                    # A copy has to catch up, and that lag is what makes
                    # crossing the axis survivable if you commit to it.
                    k = 0.30 if self.phase == 1 else 0.22
                    cast["x"] += (tx - cast["x"]) * k
                    cast["y"] += (ty - cast["y"]) * k
            # The drizzle, evenly spaced across the FULL width: the mirror
            # only rules one axis, and nobody gets to park on the other.
            if t % max(13, int(18 / dens)) == 0:
                k = (t // 7) % 9
                self._add_bullet(bx + bw * (k + 0.5) / 9.0, by - 10,
                                0.0, 1.45, kind="bead", ci=5, sq=3, ttl=300)
        # ============ PHASE 1 ONLY: the show still running clean =============
        # These are the moves where the production is competent. They are
        # legible, they repeat, and they can be LEARNED -- which is the whole
        # difference between the two halves of the fight. Nothing back here
        # comes apart.

        def _pat_footlights(self, t, dens):
            """THE APRON.

            Six lamps along the front of the stage, played like six keys. A
            PHRASE of eight notes is decided once at the top of the move, and
            then it repeats -- the same eight lamps, in the same order, at the
            same tempo, for as long as the move lasts. Each lit lamp shows a
            flame for twenty ticks and then sends up a column of light.

            The phrase is the point. The first time through you react to it.
            The second time through it comes back transposed one lamp over,
            and if you were listening you are already standing where it isn't.

            VERB: learn a phrase and get there before it does."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            lamp_w = bw / 6.0
            if "phrase" not in sc:
                # A real phrase, not a shuffle: it steps, it turns around,
                # and it comes home, so it is memorable after one hearing.
                sc["phrase"] = [0, 2, 4, 2, 5, 3, 1, 3]
                sc["lit"] = None
            beat = max(28, int(34 / dens))
            if t % beat == 4:
                idx = t // beat
                bar = idx // 8
                lamp = (sc["phrase"][idx % 8] + bar) % 6
                sc["lit"] = lamp
                sc["lit_at"] = t + 22
                lx = bx + (lamp + 0.5) * lamp_w
                self._spark_burst(lx, by + bh - 4, 6, 4, 1.4, 26, 1.6)
                tsb_play("glint", 0.7)
                # The flame sits ON the glass for the whole tell, so the
                # count-in is a thing you can see and not just hear.
                self._add_bullet(lx, by + bh - 10, 0.0, 0.0, kind="flame",
                                ci=4, sq=4, ttl=44, armed_at=10 ** 6)
                if idx % 8 == 7:
                    # A bar's rest: one full-width rank drifts up out of the
                    # boards, evenly spaced, so the phrase never leaves a
                    # column that is safe for the whole move.
                    tsb_play("volley", 0.7)
                    for i in range(7):
                        self._add_bullet(bx + bw * (i + 0.5) / 7.0,
                                        by + bh + 12, 0.0, -1.55,
                                        kind="lamp", ci=8, sq=3, ttl=280)
            if (sc.get("lit") is not None and sc.get("lit_at") is not None
                    and t >= sc["lit_at"] and (t - sc["lit_at"]) % 6 == 0
                    and t - sc["lit_at"] < 30):
                lx = bx + (sc["lit"] + 0.5) * lamp_w
                self._add_bullet(lx + self.rng.uniform(-3, 3),
                                by + bh + 10, 0.0, -2.35,
                                kind="lamp", ci=4, sq=4)
                tsb_play("throw", 0.55)

        def _pat_programme(self, t, dens):
            """THE PROGRAMME.

            She writes things down. It is the first thing anybody who has met
            her would tell you about her, and it has never once been an
            attack until now.

            A page fills, top line down: words appear one at a time, left to
            right, at reading speed, and they are perfectly harmless while
            they are being written. Thirty ticks after a line finishes, it is
            STRUCK THROUGH -- a rule drawn the width of the room at that
            line's height -- and the words on it fall off the page. So the
            page fills downward and pushes you down with it, line by line,
            until there is nowhere lower, and then it turns over and starts
            again from the top.

            VERB: read ahead of the pen. The line being written now is the
            line that is about to be crossed out, and you can see how long it
            is going to be before it gets there."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            lines = 5
            lead = bh / float(lines + 1)
            page_len = max(300, int(340 / dens))
            # A move's first tick is active_t 1, not 0, so the count
            # starts at (t - 1): otherwise the opening measure -- and
            # the setup that hangs off its downbeat -- is skipped.
            beat = (t - 1) % page_len
            if beat == 0:
                # A page of a real list is ragged. Decided here, at the top,
                # so the lengths are readable the whole way down.
                sc["lens"] = [self.rng.randint(6, 12) for _ in range(lines)]
                if t > 1:
                    tsb_play("wire", 0.6)
                    # The page turns: everything on it goes over the edge.
                    for b in self.bullets:
                        if b["kind"] == "word":
                            b["vy"] = 3.2
                            b["turn"] = None
                            b["tether"] = None
                            b["armed_at"] = 0
            row_every = max(40, int(48 / dens))
            for i in range(lines):
                start = 8 + i * row_every
                y = by + lead * (i + 1)
                n = sc.get("lens", [10] * lines)[i]
                if start <= beat < start + n * 3 and (beat - start) % 3 == 0:
                    k = (beat - start) // 3
                    # The rule for this line is added strike_in ticks
                    # from now and draws itself for 26 more, so the word
                    # falls -- and only then becomes lethal -- on the tick
                    # the pen actually reaches it.
                    strike_in = (n - k) * 3 + 30
                    self._add_bullet(bx + 16 + k * 20.0, y, 0.0, 0.0,
                                    kind="word", ci=7, sq=3,
                                    turn={"at": strike_in + 28, "vx": 0.0,
                                            "vy": 2.5},
                                    armed_at=strike_in + 24, ttl=400)
                    if k % 4 == 0:
                        tsb_play("blip", 0.35)
                if beat == start + n * 3 + 30:
                    # The rule. Same telegraph as every other line in the
                    # fight; what is new is that you have been watching its
                    # length get decided for two seconds.
                    self._add_wire("h", y, tel=26, on=20, vol=0.8)
            # Between pages, the edge of the paper comes up past you, so the
            # bottom of the box is not a place to wait out a page.
            if beat == page_len - 30:
                tsb_play("volley", 0.75)
                for i in range(8):
                    self._add_bullet(bx + bw * (i + 0.5) / 8.0,
                                    by + bh + 12, 0.0, -2.1, kind="thread",
                                    ci=5, sq=3, ttl=260)

        def _pat_curtaincall(self, t, dens):
            """CURTAIN CALL.

            The house curtain comes IN -- the ceiling lowers and the floor
            stays where it is, so the room you are playing in becomes a slot
            the height of three lanes, and the ranks that cross it are fast
            and evenly spaced and there is not much of anywhere to be.

            Then it stops. The curtain goes back up, and she BOWS: the
            strings go slack, everything already in the air stops dead, and
            the house throws flowers -- whole camellias, lobbed in on real
            arcs, which land on the boards and sit there for a moment before
            they burst.

            VERB: work in a room somebody else keeps deciding the size of,
            and spend the bow getting clear of where the flowers landed."""
            base_w, base_h = TSBGame.DODGE_BOX["curtaincall"]
            sc = self.pat_scratch
            cycle = 244
            # A move's first tick is active_t 1, not 0, so the count
            # starts at (t - 1): otherwise the opening measure -- and
            # the setup that hangs off its downbeat -- is skipped.
            beat = (t - 1) % cycle
            # 1. THE CURTAIN IN (0..76) and the slot (76..140).
            if beat < 76:
                p = 0.5 - 0.5 * math.cos(beat / 76.0 * math.pi)
            elif beat < 148:
                p = 1.0
            elif beat < 184:
                p = max(0.0, 1.0 - (beat - 148) / 36.0)
            else:
                p = 0.0
            take = 118.0 * p
            self.box_target = [TSB_BOX_CX, TSB_BOX_CY + take * 0.5,
                                base_w, base_h - take]
            bx, by, bw, bh = self._box_rect()
            if 78 <= beat < 146 and (beat - 78) % max(26, int(34 / dens)) == 0:
                tsb_play("volley", 0.8)
                left = ((beat - 78) // 34) % 2 == 0
                spacing = 46.0
                count = max(2, int(bh / spacing))
                y0 = by + (bh - (count - 1) * spacing) * 0.5
                for i in range(count):
                    self._add_bullet(bx - 12 if left else bx + bw + 12,
                                    y0 + i * spacing,
                                    3.0 if left else -3.0, 0.0,
                                    kind="pellet", ci=0 if left else 1, sq=4)
            # 2. THE BOW (150). Everything in the air holds its breath.
            if beat == 150:
                tsb_play("wire", 0.9)
                self.shake = max(self.shake, 14)
                for b in self.bullets:
                    if not b.get("heal"):
                        b["hold"] = 30
            # 3. THE FLOWERS (162). Lobbed on honest parabolas onto the
            #    boards, where they sit -- visibly -- before they open.
            if beat == 162:
                tsb_play("volley2", 1.0)
                grav = 0.10
                for i in range(5):
                    left = i % 2 == 0
                    x0 = bx + (8.0 if left else bw - 8.0)
                    y0 = by + bh + 10.0
                    vy0 = -5.2 - 0.5 * (i % 3)
                    flight = 2.0 * abs(vy0) / grav
                    tx = bx + bw * (0.16 + 0.17 * i)
                    b = self._add_bullet(x0, y0, (tx - x0) / flight, vy0,
                                        kind="bigpetal", ci=0 if i % 2 else 6,
                                        sq=4, ay=grav, ttl=int(flight) + 6)
                    if b is not None:
                        sc.setdefault("lands", []).append(
                            (t + int(flight) + 4, tx))
            due = [d for d in sc.get("lands", ()) if d[0] <= t]
            if due:
                sc["lands"] = [d for d in sc["lands"] if d[0] > t]
                for _at, x in due:
                    self._spark_burst(x, by + bh - 10, 6, 1, 1.6, 26, 1.2)
                    self._add_bloom(x, by + bh - 14, fuse=44, n=11, ci=1,
                                    speed=1.9, spin=self.spiral_a)

        def _pat_pincushion(self, t, dens):
            """THE PINCUSHION.

            A hedgehog, turning. Five rigid arms of pins are stuck into a
            cushion at the middle of the room and the whole assembly rotates,
            slowly, one way. It is not a volley. It is FURNITURE: an obstacle
            with a shape you can see all of at once, and the only question is
            which side of it you want to be on in four seconds' time.

            Then somebody pulls the pins out. They retract into the cushion,
            all together, and come straight back out as a whole ring.

            VERB: circle a rotating obstacle, and be off the radius when it
            lets go. A wall-walker runs the rim between pulls, because the
            corners are outside the arms' reach and a corner is not a plan."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            cx = bx + bw * 0.5
            cy = by + bh * 0.5
            cycle = max(160, int(196 / dens))
            # A move's first tick is active_t 1, not 0, so the count
            # starts at (t - 1): otherwise the opening measure -- and
            # the setup that hangs off its downbeat -- is skipped.
            beat = (t - 1) % cycle
            if beat == 0:
                sc["spin"] = -sc.get("spin", -1.0)
                omega = 0.0115 * sc["spin"] * (0.9 + 0.1 * dens)
                hold = cycle - 46
                tsb_play("glint", 0.85)
                self._add_bullet(cx, cy, 0.0, 0.0, kind="hoop", ci=6, sq=4,
                                ttl=hold + 20, armed_at=24)
                for arm in range(5):
                    a0 = self.spiral_a + 6.28318 * arm / 5.0
                    for r in (36.0, 62.0, 88.0, 114.0):
                        self._add_orbit_petal(cx, cy, r, a0, omega,
                                            hold=hold, ci=5, sq=4,
                                            release=0.0, armed_at=24,
                                            kind="pin")
            if beat == cycle - 46:
                # THE PULL. The arms come home...
                tsb_play("wire", 0.8)
                self._spark_burst(cx, cy, 10, 5, 2.2, 30)
            if beat == cycle - 20:
                # ...and go straight back out as one ring. Sixteen spokes on
                # a 380-wide box is 74px of arc at the rim: honest.
                tsb_play("bloom", 1.0)
                for i in range(16):
                    a = self.spiral_a + 6.28318 * i / 16.0
                    self._add_bullet(cx, cy, math.cos(a) * 2.15,
                                    math.sin(a) * 2.15, kind="pin",
                                    ci=5, sq=3, armed_at=8, ttl=300)
            # The wall-walker. The arms reach 114px; the corners of the box
            # are 230 out. Somebody has to go and look in them.
            if t % max(48, int(62 / dens)) == 20:
                wall = (t // 62) % 4
                s = 2.5
                if wall == 0:
                    self._add_bullet(bx + 6, by + 8, s, 0.0, kind="thread",
                                    ci=7, sq=3, ttl=300)
                elif wall == 1:
                    self._add_bullet(bx + bw - 6, by + 8, 0.0, s,
                                    kind="thread", ci=7, sq=3, ttl=300)
                elif wall == 2:
                    self._add_bullet(bx + bw - 6, by + bh - 8, -s, 0.0,
                                    kind="thread", ci=7, sq=3, ttl=300)
                else:
                    self._add_bullet(bx + 6, by + bh - 8, 0.0, -s,
                                    kind="thread", ci=7, sq=3, ttl=300)

        def _pat_garland(self, t, dens):
            """THE GARLAND.

            One long chain of flowers, strung head to tail, dragged around
            the room on a figure that closes. It is a rope, not a curtain:
            fourteen bodies you can see the whole shape of, moving as one
            thing, so the read is never "where is the gap" -- it is "which
            side of the rope do I want to be on when it comes back around."

            And it drops. Every so often the tail sheds a flower, which stays
            where it fell and drifts down out of the way in its own time, so
            the room silts up behind the chain and the last third of the move
            is spent threading both.

            VERB: pick a side of a moving rope, early."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            cx = bx + bw * 0.5
            cy = by + bh * 0.5
            if "body" not in sc:
                sc["a"] = self.spiral_a
                sc["hist"] = []
                sc["body"] = []
                sc["chain"] = 14
                for i in range(sc["chain"]):
                    b = self._add_bullet(cx, cy, 0.0, 0.0, kind="bead",
                                        ci=1 if i % 3 else 0, sq=4,
                                        ttl=10 ** 6, armed_at=40)
                    sc["body"].append(b)
                tsb_play("glint", 0.9)
            sc["a"] += 0.0210 + 0.0028 * (dens - 1.0)
            a = sc["a"]
            hx = cx + bw * 0.40 * math.sin(a)
            hy = cy + bh * 0.36 * math.sin(a * 1.37 + 0.7)
            sc["hist"].append((hx, hy))
            if len(sc["hist"]) > 96:
                sc["hist"].pop(0)
            hist = sc["hist"]
            for i, b in enumerate(sc["body"]):
                if b is None:
                    continue
                k = len(hist) - 1 - i * 6
                if k < 0:
                    k = 0
                b["x"], b["y"] = hist[k]
            # The shed. Its tail hands one over and the room keeps it.
            if t > 120 and t % max(74, int(96 / dens)) == 0 and sc["body"]:
                tail = sc["body"].pop()
                if tail is not None:
                    tail["vy"] = 0.75
                    tail["sway"] = 0.5
                    tail["ttl"] = 420
                    tail["kind"] = "seed"
                    tsb_play("release", 0.6)
                sc["body"].insert(0, self._add_bullet(hx, hy, 0.0, 0.0,
                                                    kind="bead", ci=0, sq=4,
                                                    ttl=10 ** 6, armed_at=20))
            # A second, shorter chain counter-rotating in the back half, so
            # the figure's own quiet lobe stops being one.
            if t == 230:
                sc["body2"] = []
                sc["hist2"] = []
                tsb_play("glint", 0.9)
                for i in range(8):
                    sc["body2"].append(
                        self._add_bullet(cx, cy, 0.0, 0.0, kind="bead",
                                        ci=6, sq=3, ttl=10 ** 6,
                                        armed_at=40))
            if t > 230 and "body2" in sc:
                a2 = -a * 1.31
                h2 = (cx + bw * 0.30 * math.sin(a2 + 2.1),
                        cy + bh * 0.30 * math.sin(a2 * 0.83))
                sc["hist2"].append(h2)
                if len(sc["hist2"]) > 64:
                    sc["hist2"].pop(0)
                for i, b in enumerate(sc["body2"]):
                    if b is None:
                        continue
                    k = len(sc["hist2"]) - 1 - i * 6
                    if k < 0:
                        k = 0
                    b["x"], b["y"] = sc["hist2"][k]

        # ============ PHASE 2 ONLY: the show coming apart =====================
        # Nothing back here can be learned, because nothing back here repeats
        # the same way twice -- but every single one of them still telegraphs.
        # That is the line: phase 2 is disorder, never surprise damage.

        def _pat_marionette(self, t, dens):
            """STRINGS.

            The one the whole fight has been about.

            Hooks come down and take the SOUL. Each one is a visible line
            from a walking anchor on the rim to you, and each one PULLS -- not
            hard, but constantly, and they stack. Two of them and the room is
            steering. Three and you are being walked.

            You get them off by pulling AWAY. Hold against a string long
            enough and it goes taut and breaks, with a snap and a spray of
            what it was holding -- so cutting a thread costs you something,
            here, the same way it costs her.

            VERB: fight the pull. Break the string. The rain underneath is
            deliberately thin: this move is not asking you to dodge, it is
            asking you what you are willing to spend to stand still."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            if "hooks" not in sc:
                sc["hooks"] = []
                sc["next"] = 24
                sc["n"] = 0
            if t >= sc["next"] and len(sc["hooks"]) < 3:
                sc["n"] += 1
                sc["next"] = t + max(96, int(128 / dens))
                side = self.rng.randrange(4)
                sc["hooks"].append({"side": side, "ph": self.rng.random(),
                                    "born": t, "ten": 0.0,
                                    "life": self.rng.randint(230, 320)})
                tsb_play("wire", 0.95)
                self._spark_burst(self.px, self.py, 9, 5, 1.9, 30)
            live = []
            hooks = []
            for hk in sc["hooks"]:
                age = t - hk["born"]
                side = hk["side"]
                # The anchor paces its own wall, so a hook is never a fixed
                # direction you can settle into leaning against.
                u = tsb_sweep(t, 260, 0.10, 0.90, hk["ph"])
                if side == 0:
                    ax, ay = bx + bw * u, by - 30.0
                elif side == 1:
                    ax, ay = bx + bw + 30.0, by + bh * u
                elif side == 2:
                    ax, ay = bx + bw * u, by + bh + 30.0
                else:
                    ax, ay = bx - 30.0, by + bh * u
                dxh = ax - self.px
                dyh = ay - self.py
                d = math.hypot(dxh, dyh) or 1.0
                ux, uy = dxh / d, dyh / d
                if age > 20:
                    pull = 0.30 + 0.03 * self.strings_cut
                    self.drag_x += ux * pull
                    self.drag_y += uy * pull
                # Tension: pushing away from the anchor loads the line. It
                # bleeds off fast if you stop, so a break has to be committed
                # to -- which is the entire point of the move.
                push = -(self.move_vx * ux + self.move_vy * uy)
                if push > 0.25:
                    hk["ten"] += push
                else:
                    hk["ten"] = max(0.0, hk["ten"] - 1.4)
                need = 74.0
                if hk["ten"] >= need or age >= hk["life"]:
                    snapped = hk["ten"] >= need
                    tsb_play("snap" if snapped else "release",
                            1.0 if snapped else 0.7)
                    self._spark_burst(self.px, self.py, 12 if snapped else 6,
                                        2 if snapped else 5, 2.6, 32)
                    if snapped:
                        # It was holding something. Armed late, so the recoil
                        # is a cost and not an ambush.
                        for i in range(8):
                            a = self.spiral_a + 6.28318 * i / 8.0
                            self._add_bullet(self.px, self.py,
                                            math.cos(a) * 2.0,
                                            math.sin(a) * 2.0, kind="thread",
                                            ci=5, sq=3, armed_at=16, ttl=260)
                    continue
                live.append(hk)
                hooks.append({"ax": ax, "ay": ay, "ci": 5,
                            "ten": min(1.0, hk["ten"] / need)})
            sc["hooks"] = live
            self.hooks = hooks
            # Thin, paced rain. It exists so that being walked into a corner
            # is a real loss and not just an indignity.
            if t % max(20, int(27 / dens)) == 0:
                self._add_bullet(bx + bw * tsb_sweep(t, 250, 0.07, 0.93),
                                by - 12, 0.0, 2.0, kind="petal", ci=6,
                                sq=3, sway=0.35)
            if t % max(38, int(50 / dens)) == 17:
                left = (t // 50) % 2 == 0
                self._add_bullet(bx - 12 if left else bx + bw + 12,
                                by + bh * tsb_sweep(t, 210, 0.12, 0.88),
                                2.1 if left else -2.1, 0.0, kind="petal",
                                ci=6, sq=3)

        def _pat_feedback(self, t, dens):
            """FEEDBACK.

            She hates loud noises. Everything else in this fight lets you
            move. This one takes it away.

            The room has two states and it tells you which one is coming. In
            the QUIET, a slow field creeps toward you and you have to keep
            walking out of it. Then the whine starts -- half a second of
            rising level, the rim going bright, and you can hear it -- and on
            the peak the room goes LOUD, and everything in the air stops dead
            where it is, and so must you. Move during the loud and it costs
            you. Then it passes, and everything picks up exactly where it
            hung, and the field is still coming.

            VERB: hold still on cue. It is the only move in the fight where
            standing perfectly still is the correct answer, and it is the one
            she would have found hardest to sit through."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            quiet = max(108, int(140 / dens))
            whine = 40
            loud = 38
            cycle = quiet + whine + loud
            # A move's first tick is active_t 1, not 0, so the count
            # starts at (t - 1): otherwise the opening measure -- and
            # the setup that hangs off its downbeat -- is skipped.
            beat = (t - 1) % cycle
            if beat < quiet:
                self.loud = 0.0
                # The field. Aimed at a stale mark, slow enough to walk away
                # from, dense enough that walking away has to go somewhere.
                if beat % max(15, int(20 / dens)) == 0:
                    per = 2.0 * (bw + bh)
                    p = per * tsb_sweep(t, 300, 0.0, 1.0)
                    if p < bw:
                        x, y = bx + p, by - 12
                    elif p < bw + bh:
                        x, y = bx + bw + 12, by + (p - bw)
                    elif p < 2 * bw + bh:
                        x, y = bx + bw - (p - bw - bh), by + bh + 12
                    else:
                        x, y = bx - 12, by + bh - (p - 2 * bw - bh)
                    self._add_aimed(x, y, self.px, self.py, 1.05,
                                    kind="blob", ci=7, sq=4, ttl=460)
                    tsb_play("throw", 0.4)
            elif beat < quiet + whine:
                # THE WHINE. Nothing new is fired; the whole telegraph is
                # that the room is getting brighter and louder.
                u = (beat - quiet) / float(whine)
                self.loud = u * 0.85
                if (beat - quiet) % 8 == 0:
                    per = self.rng.random()
                    self._spark_burst(bx + bw * per, by - 4, 3, 2,
                                        1.2 + 2.0 * u, 22, 1.0)
                    self._spark_burst(bx + bw * (1.0 - per), by + bh + 4,
                                        3, 2, 1.2 + 2.0 * u, 22, -1.0)
                if beat == quiet:
                    tsb_play("wire", 0.5)
                elif beat == quiet + whine - 14:
                    tsb_play("wire", 0.85)
            else:
                self.loud = 1.0
                if beat == quiet + whine:
                    tsb_play("phase", 0.55)
                    self.shake = max(self.shake, 20)
                    for b in self.bullets:
                        if not b.get("heal"):
                            b["hold"] = loud + 2
                # And if you move, it finds you. One hit per window: the
                # invuln window is longer than the loud is.
                if self.move_amt > 0.6 and self.tick >= self.inv_until:
                    self._spark_burst(self.px, self.py, 10, 0, 2.8, 30)
                    self._take_hit(3.0)
            if beat == cycle - 1:
                self.loud = 0.0
                tsb_play("release", 0.8)

        def _pat_recast(self, t, dens):
            """RECAST.

            The stage will not hold a shape. On a rigging groan the room is
            pulled to a new proportion -- and the new proportion comes with
            its OWN attack, one that only makes sense in a room that shape.
            Wide and shallow gets a rank down its long axis. Tall and narrow
            gets heads dropped down the well. Square gets a ring.

            VERB: re-read the room every three seconds, and know what each
            shape means before it finishes moving."""
            sc = self.pat_scratch
            shapes = (
                ([TSB_BOX_CX, TSB_BOX_CY, 434.0, 188.0], "rank"),
                ([TSB_BOX_CX + 30.0, TSB_BOX_CY, 254.0, 288.0], "well"),
                ([TSB_BOX_CX - 30.0, TSB_BOX_CY, 296.0, 286.0], "ring"),
                ([TSB_BOX_CX, TSB_BOX_CY, 392.0, 226.0], "rank"),
            )
            if "shape" not in sc:
                sc["shape"] = 2
                sc["next"] = 24
                sc["fire_at"] = None
            bx, by, bw, bh = self._box_rect()
            if t >= sc["next"]:
                sc["shape"] = (sc["shape"] + self.rng.randint(1, 3)) % 4
                sc["next"] = t + self.rng.randint(172, 208)
                sc["fire_at"] = t + 44
                self.box_target = list(shapes[sc["shape"]][0])
                self._spark_burst(bx + bw * 0.5, by + 4, 6, 5, 1.4, 26)
                self._spark_burst(bx + bw * 0.5, by + bh - 4, 6, 5, 1.4, 26)
                tsb_play("wire", 0.45)
            if sc["fire_at"] is not None and t == sc["fire_at"]:
                sc["fire_at"] = None
                job = shapes[sc["shape"]][1]
                if job == "rank":
                    tsb_play("volley", 0.85)
                    spacing = 46.0
                    left = self.rng.random() < 0.5
                    count = int(bh / spacing) + 1
                    y0 = by + (bh - (count - 1) * spacing) * 0.5
                    for i in range(count):
                        self._add_bullet(bx - 12 if left else bx + bw + 12,
                                        y0 + i * spacing,
                                        2.7 if left else -2.7, 0.0,
                                        kind="chip", ci=0 if left else 1,
                                        sq=4)
                elif job == "well":
                    tsb_play("volley2", 0.85)
                    for i in range(4):
                        x = bx + bw * (i + 0.5) / 4.0
                        self._add_bullet(x, by - 16 - i % 2 * 22.0, 0.0,
                                        2.6, kind="bigpetal", ci=6, sq=4,
                                        ttl=220)
                else:
                    tsb_play("bloom", 0.9)
                    self._add_bloom(bx + bw * 0.5, by + bh * 0.5, fuse=40,
                                    n=15, ci=1, speed=2.0,
                                    spin=self.spiral_a)
            # Dust that paces whatever width the room currently has, so no
            # new proportion ever arrives with a free corner in it.
            if t % 26 == 13:
                self._add_bullet(bx + bw * tsb_sweep(t, 220, 0.07, 0.93),
                                by - 12, 0.0, 1.9, kind="chip", ci=7,
                                sq=3, sway=0.35)

        def _pat_unravel(self, t, dens):
            """UNRAVEL.

            The seam gives.

            A stitched line is laid all the way across the room -- solid, not
            a curtain, a wall -- and it divides the box into two rooms with
            you in one of them. Then it pops, one stitch at a time, travelling
            from one end to the other, and every stitch that lets go throws
            two loose threads perpendicular to the seam, into both rooms. When
            the rip reaches the far wall the seam is gone, the rooms are one
            room again, and the next seam is laid somewhere else.

            VERB: outrun a zipper in half a room. Which half you are in is
            decided by where you were standing, so the seam is telegraphed as
            a ghost line and you get to choose."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            n = 16
            rip_every = max(4, int(6 / dens))
            cycle = 60 + n * rip_every + 40
            # A move's first tick is active_t 1, not 0, so the count
            # starts at (t - 1): otherwise the opening measure -- and
            # the setup that hangs off its downbeat -- is skipped.
            beat = (t - 1) % cycle
            if beat == 0:
                # The seam always crosses the room the long way, so a rip is
                # always a real journey. Its position paces between passes.
                sc["horiz"] = bw >= bh
                sc["frac"] = tsb_sweep(t, 470, 0.26, 0.74)
                sc["dir"] = self.rng.choice([1, -1])
                sc["seam"] = []
                tsb_play("wire", 0.7)
                for i in range(n):
                    if sc["horiz"]:
                        x = bx + (i + 0.5) * bw / float(n)
                        y = by + bh * sc["frac"]
                    else:
                        x = bx + bw * sc["frac"]
                        y = by + (i + 0.5) * bh / float(n)
                    b = self._add_bullet(x, y, 0.0, 0.0, kind="stitch",
                                        ci=5, sq=4, ttl=cycle + 20,
                                        armed_at=54)
                    sc["seam"].append(b)
            if beat == 40:
                # A spark at the end the rip is going to start from: which
                # way the zipper runs is the only thing you need to know and
                # the only thing you are told.
                near = sc["dir"] > 0
                if sc["horiz"]:
                    sx = bx + (8.0 if near else bw - 8.0)
                    sy = by + bh * sc["frac"]
                else:
                    sx = bx + bw * sc["frac"]
                    sy = by + (8.0 if near else bh - 8.0)
                self._spark_burst(sx, sy, 8, 0, 2.0, 30)
                tsb_play("glint", 0.9)
                sc["rip_from"] = (sx, sy)
            if beat == 58:
                # THE RIPPER. Not an invisible travelling index -- a blade,
                # moving along the seam at exactly the speed the stitches pop,
                # so the thing taking the room apart is a thing you can watch
                # coming. It cannot be outrun and does not need to be: it runs
                # ON the seam, and the seam is a wall. What it punishes is
                # sheltering flat against the wall you are hiding behind.
                sx, sy = sc.get("rip_from", (bx, by))
                step = (bw if sc["horiz"] else bh) / float(n)
                sp = step / float(rip_every)
                d = float(sc["dir"])
                self._add_bullet(sx, sy,
                                sp * d if sc["horiz"] else 0.0,
                                0.0 if sc["horiz"] else sp * d,
                                kind="dagger", ci=2, sq=4,
                                ttl=n * rip_every + 30)
                tsb_play("dagger", 1.0)
            if 60 <= beat < 60 + n * rip_every and (beat - 60) % rip_every == 0:
                i = (beat - 60) // rip_every
                if sc.get("dir", 1) < 0:
                    i = n - 1 - i
                seam = sc.get("seam") or []
                if 0 <= i < len(seam) and seam[i] is not None:
                    b = seam[i]
                    bxp, byp = b["x"], b["y"]
                    b["ttl"] = 0
                    seam[i] = None
                    tsb_play("volley2", 0.35)
                    self._spark_burst(bxp, byp, 4, 5, 1.6, 20)
                    if sc["horiz"]:
                        for s in (-1.0, 1.0):
                            self._add_bullet(bxp, byp, 0.0, s * 2.05,
                                            kind="thread", ci=6, sq=3,
                                            ttl=260)
                    else:
                        for s in (-1.0, 1.0):
                            self._add_bullet(bxp, byp, s * 2.05, 0.0,
                                            kind="thread", ci=6, sq=3,
                                            ttl=260)
            if beat == 60 + n * rip_every + 6:
                # Whatever is left of the seam simply falls.
                for b in (sc.get("seam") or []):
                    if b is not None:
                        b["vy"] = 2.2
                        b["armed_at"] = 0
                tsb_play("release", 0.8)

        def _pat_chandelier(self, t, dens):
            """THE CHANDELIER.

            One heavy thing on one line.

            The house lamp is lowered into the room and it hangs there, and
            every few seconds it sheds a whole ring of stage-lights -- no door
            in the ring, ever; the spacing between neighbours is the dodge and
            it opens as the ring travels. Meanwhile the line it is hanging on
            is fraying, visibly, and when it goes the lamp comes down: fast,
            under real gravity, into the boards, where it throws everything it
            was carrying along the floor in both directions.

            VERB: manage a hanging object, and be somewhere else when the
            rigging finally gives."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            period = max(250, int(320 / dens))
            beat = t % period
            fall_at = period - 96
            if beat == 1:
                sc["lamp"] = self._add_bullet(bx + bw * 0.5, by - 24, 0.0,
                                            1.15, kind="houselamp", ci=8,
                                            sq=4, ttl=period - 6,
                                            armed_at=12)
                sc["rings"] = 0
                sc["fallen"] = False
                tsb_play("bloom", 0.8)
            lamp = sc.get("lamp")
            if lamp is None:
                return
            if beat == 74:
                lamp["vy"] = 0.0
            if 96 <= beat < fall_at - 10:
                if (beat - 96) % max(38, int(52 / dens)) == 0:
                    sc["rings"] = sc.get("rings", 0) + 1
                    n = 12 if dens < 1.2 else 14
                    off = sc["rings"] * 0.21
                    tsb_play("volley2", 0.65)
                    for i in range(n):
                        a = off + 6.2831853 * i / float(n)
                        self._add_bullet(lamp["x"], lamp["y"],
                                        math.cos(a) * 1.6,
                                        math.sin(a) * 1.6, kind="lamp",
                                        ci=8, sq=3, ttl=300)
                # The line frays where you can see it fray.
                if beat % 12 == 0:
                    u = (beat - 96) / float(max(1, fall_at - 106))
                    self._spark_burst(lamp["x"],
                                    by - 10 - self.rng.uniform(0, 14),
                                    2, 5, 1.0 + 2.0 * u, 20, 1.4)
            if beat == fall_at - 10:
                tsb_play("wire", 1.0)
                self._spark_burst(lamp["x"], by - 12, 12, 5, 3.0, 34, 1.6)
            if beat == fall_at and not sc.get("fallen"):
                sc["fallen"] = True
                lamp["vy"] = 1.2
                lamp["ay"] = 0.26
                tsb_play("fall", 0.8)
                # Solve 0.13n^2 + 1.33n = drop for the landing tick, so the
                # floor burst arrives exactly under the lamp, not near it.
                drop = max(1.0, (by + bh - 14.0) - lamp["y"])
                n = (-1.33 + math.sqrt(1.7689 + 0.52 * drop)) / 0.26
                sc["land"] = t + max(6, int(n))
                sc["land_x"] = lamp["x"]
            if sc.get("land") and t == sc["land"]:
                self.shake = max(self.shake, 22)
                tsb_play("bloom", 1.0)
                x = sc.get("land_x", bx + bw * 0.5)
                self._spark_burst(x, by + bh - 10, 14, 8, 3.0, 32, 1.2)
                for s in (-1.0, 1.0):
                    for j in range(4):
                        self._add_bullet(x, by + bh - 12,
                                        s * (1.7 + 0.5 * j),
                                        -0.5 - 0.28 * j, kind="bolt",
                                        ci=8, sq=3, ay=0.026, ttl=280)
                sc["land"] = None

        def _pat_blackout(self, t, dens):
            """BLACKOUT.

            Somebody kills the house lights with the number still running.

            The room goes dark and stays dark, and you can only see as far as
            the SOUL's own glow -- everything further out is a rumour. What is
            in here with you is slow and heavy and few, and every single one
            of them announces its entry with a spark and a sound at the wall
            it comes in through, so the move is played by EAR and by memory:
            something came in at the top left eleven seconds ago and has not
            gone past yet.

            And there is a worklight loose in the room. It drifts where it
            wants. Stand near it and you can see properly -- which is a much
            larger promise than it sounds, and it is never quite where you
            need it to be.

            VERB: navigate blind, and go and fetch the light."""
            bx, by, bw, bh = self._box_rect()
            sc = self.pat_scratch
            if "wl" not in sc:
                sc["wl"] = self._add_bullet(bx + bw * 0.5, by + bh * 0.35,
                                            0.0, 0.0, kind="flame", ci=4,
                                            sq=4, ttl=10 ** 6,
                                            armed_at=10 ** 6)
                sc["wa"] = self.rng.uniform(0, 6.28)
                sc["next"] = 40
                sc["bloom"] = 150
            self.blackout = min(1.0, t / 60.0)
            wl = sc.get("wl")
            if wl is not None:
                sc["wa"] += 0.0135
                wl["x"] = bx + bw * (0.5 + 0.33 * math.sin(sc["wa"]))
                wl["y"] = by + bh * (0.5 + 0.29 * math.sin(sc["wa"] * 1.61))
                self.light_src = (wl["x"], wl["y"])
            if t >= sc["next"]:
                sc["next"] = t + max(38, int(50 / dens))
                per = 2.0 * (bw + bh)
                p = per * tsb_sweep(t, 340, 0.02, 0.98)
                if p < bw:
                    x, y = bx + p, by - 14
                elif p < bw + bh:
                    x, y = bx + bw + 14, by + (p - bw)
                elif p < 2 * bw + bh:
                    x, y = bx + bw - (p - bw - bh), by + bh + 14
                else:
                    x, y = bx - 14, by + bh - (p - 2 * bw - bh)
                # The entry is LOUD and BRIGHT, because it is the only look
                # at it you are going to get.
                self._spark_burst(x, y, 9, 6, 2.2, 34)
                tsb_play("volley2", 0.9)
                self._add_aimed(x, y, bx + bw - (x - bx), by + bh - (y - by),
                                1.35, kind="bigpetal", ci=6, sq=4, ttl=520)
            if t >= sc["bloom"]:
                # Blooms carry their own light, so they are the one thing in
                # here that reads at range. Placed on a stale mark.
                sc["bloom"] = t + max(140, int(186 / dens))
                self._add_bloom(tsb_clamp(self.px, bx + 40, bx + bw - 40),
                                tsb_clamp(self.py, by + 34, by + bh - 34),
                                fuse=56, n=13, ci=8, speed=1.85,
                                spin=self.spiral_a)
                tsb_play("glint", 0.9)
            # And then somebody finds the switch.
            if t == self.pat_dur - self.pat_lead - 70:
                self.blackout = 0.0
                sc["off"] = True
                tsb_play("phase", 0.5)
                self._spark_burst(bx + bw * 0.5, by + bh * 0.5, 14, 2,
                                    3.2, 34)
            if sc.get("off"):
                self.blackout = 0.0

        def _pat_tableau(self, t, dens):
            """TABLEAU.

            Intermission. The room goes still and a picture fades up in it --
            the whole company, held: souls and pins and pages, every one of
            them showing the line it is going to take, all of them parallel,
            alleys guaranteed between the tracks and nothing placed on top of
            you. One figure in the picture is a green needle, which is worth
            reading the picture for.

            When the count arrives the tableau lets go all at once, leading
            edge first.

            VERB: find your alley while it is still a picture."""
            bx, by, bw, bh = self._box_rect()
            beat = t % max(180, int(224 / dens))
            if beat != 1:
                return
            ang = self.rng.uniform(0.0, 6.28318)
            dx = math.cos(ang)
            dy = math.sin(ang)
            hold = 78
            placed = []
            tries = 0
            want = 10 if dens >= 1.2 else 9
            while len(placed) < want and tries < 220:
                tries += 1
                x = self.rng.uniform(bx + 26, bx + bw - 26)
                y = self.rng.uniform(by + 24, by + bh - 24)
                proj = -x * dy + y * dx
                if any(abs(proj - q) < 48.0 for _x, _y, q in placed):
                    continue
                if (x - self.px) ** 2 + (y - self.py) ** 2 < 80.0 ** 2:
                    continue
                placed.append((x, y, proj))
            tsb_play("glint", 0.9)
            placed.sort(key=lambda p: p[0] * dx + p[1] * dy)
            company = ("soul", "pin", "page", "pin", "page")
            gift = self.rng.randrange(len(placed)) if placed else -1
            for i, (x, y, _proj) in enumerate(placed):
                at = hold + i * 4
                if i == gift:
                    self._add_bullet(x, y, 0.0, 0.0, kind="needle", ci=3,
                                    sq=4, heal=True,
                                    turn={"at": at, "target": (x + dx * 620.0,
                                                                y + dy * 620.0),
                                            "speed": 2.2},
                                    tether={"x": x + dx * 90.0,
                                            "y": y + dy * 90.0, "until": at},
                                    ttl=at + 260)
                    continue
                self._add_bullet(x, y, 0.0, 0.0,
                                kind=company[i % len(company)], ci=2, sq=4,
                                turn={"at": at,
                                        "target": (x + dx * 620.0,
                                                    y + dy * 620.0),
                                        "speed": 3.0},
                                tether={"x": x + dx * 90.0,
                                        "y": y + dy * 90.0, "until": at},
                                armed_at=at - 4, ttl=at + 240)

        def _pat_limp(self, t, dens):
            # The collapse. Sparse, slow, barely aimed. This is not a threat;
            # that is the point you are meant to feel in your hands.
            bx, by, bw, bh = self._box_rect()
            if t % 44 == 0:
                x = self.rng.uniform(bx + 8, bx + bw - 8)
                self._add_bullet(x, by - 12, 0.0, 1.0, kind="petal", ci=7,
                                sq=3, sway=0.4)
            if t % 100 == 0:
                self._spawn_needle()

        # ----- phase shift (both flavors: it is NOT her choice) ------------------

        def _begin_shift(self, kind):
            self.route = kind
            self.shift_kind = kind
            self.bubble = None
            for b in self.bullets:
                b["fz"] = 14
            self.blooms = []
            self._kill_wires()
            self._set_mode("shift")

        def _step_shift(self):
            t = self.mtick
            self._step_bullets()
            k = self.shift_kind
            if k == "v":
                # She's dropped at half HP -- and reads it as being put back
                # down, her worst fear -- then it hauls her up again and she
                # is grateful for the catch.
                if t == 30:
                    self._bub("am I dropping? did I do it wrong? no-- no, I did it right, I did all of it right, don't put me back, please don't put me back--", hold=55)
                if 60 <= t < 200:
                    p = tsb_clamp((t - 60) / 140.0, 0.0, 1.0)
                    e = p * p * (3.0 - 2.0 * p)
                    self.boss_dy = 28.0 * e
                    self.boss_rot = 4.0 * e
                if t == 200:
                    tsb_play("phase")
                    tsb_play("wire")
                    self.flash = 1.0
                    self.strings_alpha = 1.0
                    self.shake = 34
                    self._booth("shift_v")
                    self._bub("No--!", hold=24)
                if 200 <= t < 224:
                    p = (t - 200) / 24.0
                    self.boss_dy = 28.0 - 36.0 * min(1.0, p)
                    self.boss_rot = 4.0 - 12.0 * math.sin(min(1.0, p) * math.pi)
                if t == 224:
                    self.boss_img = 2
                    self.boss_dy = 0.0
                    self.boss_rot = 0.0
                    tsb_music_vocal()
                    self.bg_speed = 1.6
                if t == 270:
                    self._bub("Did you see it catch me? It caught me. It always catches me, it's never once let me hit the ground-- say thank you. Say it because it's true. Say it so it hears you--", hold=65)
                if t >= 470:
                    self._after_shift()
            else:
                # She strains toward the SPARE almost involuntarily -- and
                # panics at having gone off-script before the strings wrench
                # her back and she apologizes for nearly leaving.
                if t == 30:
                    self._bub("why are my arms going down. I didn't do that. I didn't ask for that, I don't know who-- that isn't-- stop it, hands, we're working--", hold=55)
                if 90 <= t < 210:
                    self.strings_alpha = min(0.85, self.strings_alpha + 0.012)
                    p = tsb_clamp((t - 90) / 120.0, 0.0, 1.0)
                    e = p * p * (3.0 - 2.0 * p)
                    self.boss_dy = 14.0 * e
                    self.boss_rot = -3.0 * e
                if t == 210:
                    tsb_play("phase")
                    tsb_play("wire")
                    self.flash = 1.0
                    self.strings_alpha = 1.0
                    self.shake = 34
                    self._booth("shift_p")
                    self._bub("Ah--!", hold=24)
                if 210 <= t < 234:
                    p = (t - 210) / 24.0
                    self.boss_dy = 14.0 - 24.0 * min(1.0, p)
                    self.boss_rot = -3.0 + 10.0 * math.sin(min(1.0, p) * math.pi)
                if t == 234:
                    self.boss_img = 2
                    self.boss_dy = 0.0
                    self.boss_rot = 0.0
                    tsb_music_vocal()
                    self.bg_speed = 1.6
                if t == 280:
                    self._bub("I'm sorry-- I'm sorry, that wasn't me changing my mind, I would never-- tell it I didn't mean it. Tell it I'm still all in. Tell it right now--", hold=50)
                if t == 355:
                    self._bub("Don't let it think I wavered. Please. Something that picks you up can put you back down again, it'll find somebody more grateful and I'd have to go back to-- tell it I'm grateful. Tell it.", hold=55)
                if t >= 500:
                    self._after_shift()
            if t > 30:
                self._reveal_bubble()

        def _after_shift(self):
            self.phase2_start_hp = max(1.0, self.boss_hp)
            self.phase = 2
            self.turn = 0
            # P1 and P2 table indices aren't comparable; clear the anti-repeat
            # marker so the first phase-2 draw isn't skewed by a P1 index.
            self._last_pat_i = None
            self.strings_alpha = 0.74
            self.bubble = None
            self.boss_rot = 0.0
            self.flinch = False
            self.flinch_clear_turn = None
            self.fought_last = False
            # The back half rains harder and darker (the factories are
            # phase-aware); the extra bodies recycle in at phase-2 colors.
            for _i in range(12):
                self.amb_petals.append(self._new_amb_petal(True))
            for _i in range(8):
                self.streaks.append(self._new_streak(True))
            self._menu_in()

        # ----- endings ------------------------------------------------------------
        # THE POINT: all three routes end with the exact same death. The
        # room's every graphic -- grid, box, HUD, bullets, strings, bubble --
        # dies at once (the void), and her sprite free-falls to the bottom
        # of the screen under plain gravity. Same physics, same thud, every
        # time. What differs is only the words around it:
        #   violence  -- none. Hard cut between the strike and the drop.
        #   pacifist  -- she gets to finish the thought. Then the room goes.
        #   betrayal  -- she starts the same thought and never finishes it.

        VOID_GRAV = 0.34
        VOID_FLOOR_DY = 430.0   # phase-2 sprite crumpled at the bottom edge

        def _end_common(self, flag):
            self.end_flag = flag
            self.bubble = None
            self.boss_fallen = False
            self.boss_rot = 0.0
            self.land_tick = None
            for b in self.bullets:
                b["fz"] = 12
            self.blooms = []
            self._kill_wires()

        def _void_cut(self):
            # The hard cut. Everything that was ever interface is gone
            # between one frame and the next. No flash, no transition --
            # just black, and her, and nothing holding her up.
            self.void = True
            self.flash = 0.0
            self.fade_in = 0.0
            self.dark = 0.0
            self.box_alpha = 0.0
            self.hud_alpha = 0.0
            self.bubble = None
            self.strings_alpha = 0.0
            self.string_snap_fx = []
            self.bullets = []
            self.wires = []
            self.blooms = []
            self.dmg_pops = []
            self.sparks = []
            self.bg_speed = 0.0
            self.shake = 0
            self.fall_vy = 0.0
            self.fall_landed = False
            self.fall_bounced = False

        def _step_void_fall(self):
            """Gravity, not choreography. She accelerates, crumples, hits
            the bottom of the screen, gives one dead bounce, and is still."""
            if self.fall_landed:
                return
            self.fall_vy += TSBGame.VOID_GRAV
            self.boss_dy += self.fall_vy
            # She folds as she drops; by the floor she's sideways.
            p = tsb_clamp(self.boss_dy / TSBGame.VOID_FLOOR_DY, 0.0, 1.0)
            self.boss_rot = 86.0 * p * p
            if self.boss_dy >= TSBGame.VOID_FLOOR_DY:
                self.boss_dy = TSBGame.VOID_FLOOR_DY
                if not self.fall_bounced and self.fall_vy > 6.0:
                    self.fall_bounced = True
                    self.fall_vy = -self.fall_vy * 0.16
                    tsb_play("fall")
                    tsb_play("break", 0.6)
                    self.shake = 40
                    impact_x = TSB_BOSS_X + self.boss_dx
                    self._spark_burst(impact_x, 690.0, 40, 0, 4.2, 80, 2.0)
                    self._spark_burst(impact_x - 70.0, 700.0, 22, 7, 2.8, 90, 1.0)
                    self._spark_burst(impact_x + 64.0, 696.0, 20, 6, 3.0, 85, 1.4)
                else:
                    self.fall_vy = 0.0
                    self.fall_landed = True
                    self.boss_fallen = True

        def _step_end_epilogue(self, t, booth_key, finish_kind):
            # Shared post-landing beat: Matsuda's voice arrives in the dark,
            # then the dark takes the rest.
            if self.fall_landed and self.land_tick is None:
                self.land_tick = t
            lt = self.land_tick
            if lt is None:
                return
            if t == lt + 50:
                self._booth(booth_key)
            if t > lt + 140:
                self.dark = min(1.0, self.dark + 0.008)
            if t >= lt + 330:
                self._finish(finish_kind)

        def _begin_end_v(self):
            self._end_common("victory_v")
            self._set_mode("end_v")

        def _step_end_v(self):
            # Violence: no last words. The strike lands, and between one
            # frame and the next the whole room is simply gone.
            t = self.mtick
            self._step_bullets()
            if t == 2:
                tsb_music_stop(0.05)
                self._void_cut()
            # She hangs in the black for a beat -- long enough to register
            # that nothing is holding her -- then gravity notices.
            if t >= 36:
                self._step_void_fall()
            self._step_end_epilogue(t, "end_v", "victory_v")

        def _begin_end_p(self):
            self._end_common("victory_p")
            self._set_mode("end_p")

        def _step_end_p(self):
            # Pacifist: she is unheld, unhurt -- and the show simply stops.
            # No fervor, no caps, no house to sell to: after a whole fight of
            # manufactured noise, the quiet comes down, and what's left of her
            # gets one small, ambiguous line before the room takes it anyway.
            t = self.mtick
            self._step_bullets()
            if t == 15:
                self._bub("Oh.", hold=34)
            if 15 <= t < 90:
                self.strings_alpha = max(0.0, self.strings_alpha - 0.04)
            if t == 72:
                self._bub("...oh. it's finally quiet.", hold=60)
            if t == 148:
                # No resolving cue. The song loses power with the lights.
                tsb_music_stop(0.25)
            if t == 150:
                self._void_cut()
            if t >= 172:
                self._step_void_fall()
            self._step_end_epilogue(t, "end_p", "victory_p")
            if 15 <= t < 150:
                self._reveal_bubble()

        def _begin_end_b(self):
            self._end_common("victory_b")
            self.booth = None
            # The song doesn't fade for this one. It's cut off mid-note,
            # the way everything else in here is about to be.
            tsb_music_stop(0.05)
            self._set_mode("end_b")

        def _step_end_b(self):
            # Betrayal: she starts the pacifist's sentence. The room cuts
            # her off mid-word, and the same fall happens anyway.
            t = self.mtick
            self._step_bullets()
            if t == 8:
                # The one thread still holding her takes the whole swing.
                for i in range(5):
                    if i not in self.cut_string_ids:
                        self._cut_string(i, violent=True)
                self.flash = 1.0
                self.shake = 36
                self.box_alpha = 0.0
                self.hud_alpha = 0.0
            if t == 30:
                self._bub("...oh. it's f--", hold=30)
            if t == 52:
                self._void_cut()
            if t >= 74:
                self._step_void_fall()
            self._step_end_epilogue(t, "end_b", "victory_b")
            if 30 <= t < 52:
                self._reveal_bubble()

        def _step_dead(self):
            t = self.mtick
            # Bullets freeze mid-air; only the shatter advances.
            if t == 30:
                self._spark_burst(self.px, self.py, 18, 0, 4.2, 55, 1.0)
                tsb_play("hurt", 0.8)
            if t == 40 and self.visit_deaths >= 1:
                self._bub("Get up. We're not finished-- it hates an empty chair-- get up, get up, I need somebody in the room, [player], you can't leave me up here on my own--", hold=40)
            if t > 40:
                self._reveal_bubble()
            if t > 120:
                self.dark = min(1.0, self.dark + 0.015)
            if t == 130:
                tsb_music_stop(1.0)
                self._booth("death")
            if t >= 220:
                self._finish("defeat")
# --- RENDERER ------------------------------------------------------------------
init python:
    class TSBStage(renpy.Displayable):
        """One creator-defined displayable that steps TSBGame on a fixed 60Hz
        accumulator inside render() and paints the whole fight as cached-
        texture blits. Same discipline as KTStage: displayable FACTORIES are
        cached across frames; renpy.Render objects live only inside one
        render() call."""

        _tf_cache = {}
        _misc_cache = {}
        _text_cache = {}

        # kind -> (sprite, base zoom, rotates-to-heading?, pixel art?).
        # The first four are the shipped 16px pixel sprites and want `nearest`.
        # The art is Kotonoha's. The mode knows. The mode is not sorry.
        #
        # Everything below them comes from the shared atlas
        # (asset_definitions/def_bullets.rpy) and is anti-aliased at 16-62px, so it
        # wants SMOOTH scaling instead -- see _bullet_tf. They are named for
        # what they mean in this fight, not for what the sheet calls them: a
        # pin, a page of the script, a soul, and the lamps over a stage.
        # (sprite, base zoom, rotates-to-heading?, pixel art?, tintable?)
        # The first four are the shipped 16px pixel sprites and want
        # `nearest`. The art is Kotonoha's. The mode knows. The mode is not
        # sorry. Everything under them comes from the shared atlas
        # (asset_definitions/def_bullets.rpy), is anti-aliased at 9-62px, and
        # wants SMOOTH scaling instead -- see _bullet_tf.
        #
        # Every one of these is named for what it MEANS in this fight, never
        # for what the sheet calls it, because a roster where the shapes are
        # arbitrary is a roster the player reads as noise. A pin is a pin. A
        # stitch is a stitch. The stream a conductor throws is made of notes,
        # the audience is made of faces, and the thing that lands on the mark
        # after the applause is a whole camellia head.
        #
        # tintable=False is painted art with its own corona (the wisp flame,
        # the notes): tinting those only crushes the colour they were drawn
        # with, so _bullet_tf skips the TintMatrix and `ci` becomes nothing
        # but a cache key for them.
        KINDS = {
            "petal":     (EMB_DIR + "pellet.png", 1.5, True, True, True),
            "bigpetal":  (EMB_DIR + "pellet.png", 2.6, True, True, True),
            "pellet":    (EMB_DIR + "bullet.png", 1.35, False, True, True),
            "dagger":    (EMB_DIR + "dagger.png", 1.8, True, True, True),
            "pin":       (emb_cell("kunai"),     1.25, True,  False, True),
            "page":      (emb_cell("ofuda"),     1.30, False, False, True),
            "soul":      (emb_cell("heart"),     0.75, False, False, True),
            "spark":     (emb_cell("ministar"),  1.25, False, False, True),
            "lamp":      (emb_cell("sunburst"),  0.80, False, False, True),
            "houselamp": (emb_cell("moon"),      0.50, False, False, True),
            "bead":      (emb_cell("gloss"),     1.30, False, False, True),
            # --- added with the 2026-08-29 volley rebuild -------------------
            "face":      (emb_cell("dot"),       0.95, False, False, True),
            "stitch":    (emb_cell("bar"),       1.15, True,  False, True),
            "thread":    (emb_cell("rice"),      1.15, True,  False, True),
            "word":      (emb_cell("slug"),      1.10, False, False, True),
            "hoop":      (emb_cell("hoop"),      1.90, False, False, True),
            "clap":      (emb_cell("ball"),      1.35, False, False, True),
            "seed":      (emb_cell("seed"),      1.05, True,  False, True),
            "blob":      (emb_cell("haze"),      1.00, False, False, True),
            "chip":      (emb_cell("frost"),     0.85, True,  False, True),
            "bolt":      (emb_cell("boltarrow"), 0.90, True,  False, True),
            "note":      (emb_cell("note", 0),   1.00, False, False, False),
            "rest":      (emb_cell("note", 2),   1.00, False, False, False),
            "flame":     (emb_cell("wisp", 1),   0.95, False, False, False),
        }

        STRING_TOPS = [140.0, -140.0, -60.0, 60.0, 0.0]

        def __init__(self, game, **kwargs):
            super(TSBStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0

        # ----- cached factories ------------------------------------------------

        def _bullet_tf(self, kind, ci, bucket, sq, ab):
            path, base_zoom, rotates, pixel, tint = TSBStage.KINDS[kind]
            # Pellets are rotationally symmetric. Sharing one transform keeps
            # their factory cache from multiplying across needless buckets.
            if not rotates:
                bucket = 0
            key = (kind, ci, bucket, sq, ab)
            tf = TSBStage._tf_cache.get(key)
            if tf is None:
                kw = dict(zoom=base_zoom * (sq / 4.0), nearest=pixel,
                            subpixel=True)
                if tint:
                    kw["matrixcolor"] = TintMatrix(TSB_PAL[ci])
                if ab < 3:
                    kw["alpha"] = 0.25 + 0.25 * ab
                if rotates:
                    kw["rotate"] = bucket * TSB_ROT_DEG
                tf = Transform(path, **kw)
                TSBStage._tf_cache[key] = tf
            return tf

        def _misc(self, key, builder):
            d = TSBStage._misc_cache.get(key)
            if d is None:
                if len(TSBStage._misc_cache) > 900:
                    TSBStage._misc_cache.clear()
                d = builder()
                TSBStage._misc_cache[key] = d
            return d

        def _text(self, text, size, color, font=TSB_FONT, bold=False, outline=True):
            key = (text, size, color, font, bold, outline)
            t = TSBStage._text_cache.get(key)
            if t is None:
                if len(TSBStage._text_cache) > 160:
                    TSBStage._text_cache.clear()
                outl = [(2, "#05060e", 0, 0)] if outline else []
                t = Text(text, size=size, color=color, bold=bold, font=font,
                        outlines=outl)
                TSBStage._text_cache[key] = t
            return t

        # ----- input events --------------------------------------------------

        def event(self, ev, x, y, st):
            # The sim POLLS the keyboard (see TSBGame._poll_input), so this is the
            # only place a key RELEASE is ever seen as an event. Hand it to the
            # latch, which uses it to unstick a key SDL still believes is held.
            # Always returns None so the screen's own `key` bindings (Escape,
            # give-up) and everything under us keep receiving the event.
            self.game.keys.handle_event(ev)
            return None

        # ----- render ------------------------------------------------------------

        def render(self, width, height, st, at):
            global TSB_SHADER_OK
            g = self.game

            # F3 profiler (perf.rpy) -- see the note in KTStage.render.
            _perf = MSBF_PERF.on
            _t = msbf_perf_t0() if _perf else 0.0

            if self.last_st is None:
                self.last_st = st
            dt = st - self.last_st
            self.last_st = st
            if dt < 0.0:
                dt = 0.0
            elif dt > 0.25:
                dt = 0.25
            if g.paused:
                self.acc = 0.0
            else:
                self.acc += dt
                steps = 0
                while self.acc >= TSB_TICK and steps < TSB_MAX_CATCHUP:
                    g.step()
                    self.acc -= TSB_TICK
                    steps += 1
                if steps >= TSB_MAX_CATCHUP:
                    self.acc = 0.0

            if _perf:
                msbf_perf_t1("sim", _t)
                MSBF_PERF.note("bullets", len(getattr(g, "bullets", ())))
                _t = msbf_perf_t0()

            rv = renpy.Render(1280, 720)
            frame_tex = {}

            def tex(key, disp, w=128, h=128):
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
                # Quantized alpha suffix: eight levels, so animated fades
                # reuse a small, bounded set of cached Solids.
                return "%02x" % (int(tsb_clamp(a, 0.0, 1.0) * 7.0) * 36 + 3)

            def beam(color, length, thick, vertical=False):
                # A wire body drawn from the shared atlas `lens` hairline
                # (asset_definitions/def_bullets.rpy) instead of two stacked Solids.
                # The art already carries a hot white core inside a soft
                # coloured falloff, which is exactly the glow+core pair this
                # used to hand-build -- one texture, and a real beam profile
                # rather than two hard-edged bars.
                # Returns (Render, (w, h)); blit it CENTRED on the wire.
                length = max(2, int(length))
                thick = max(2, int(thick))
                key = ("beam", color, length, thick, vertical)
                entry = frame_tex.get(key)
                if entry is None:
                    d = self._misc(key, (lambda c=color, L=length, T=thick, v=vertical: Transform(
                        emb_cell("lens"), xzoom=L / 248.0, yzoom=T / 8.0,
                        subpixel=True, matrixcolor=TintMatrix(c),
                        rotate=(90 if v else 0))))
                    quad = length + thick + 8
                    r = renpy.render(d, quad, quad, st, at)
                    rv.depends_on(r)
                    entry = (r, r.get_size())
                    frame_tex[key] = entry
                return entry

            def beam_at(color, cx_, cy_, length, thick, vertical=False):
                br, (bw_, bh_) = beam(color, length, thick, vertical)
                hazard_blit(br, (int(cx_ - bw_ * 0.5), int(cy_ - bh_ * 0.5)))

            string_canvas = [None]

            def get_string_canvas():
                if string_canvas[0] is None:
                    # One small raster layer replaces up to ninety dynamic
                    # rotated-Solid factories per frame.
                    layer = renpy.Render(1280, 420)
                    canvas = layer.canvas()
                    rv.blit(layer, (0, 0))
                    string_canvas[0] = canvas
                return string_canvas[0]

            def line(x1, y1, x2, y2, color, thickness=2):
                get_string_canvas().line(
                    color,
                    (int(round(x1)), int(round(y1))),
                    (int(round(x2)), int(round(y2))),
                    max(1, int(thickness)))

            def polyline(points, color, thickness=2):
                if len(points) >= 2:
                    pts = [(int(round(x)), int(round(y))) for x, y in points]
                    get_string_canvas().lines(
                        color, False, pts, max(1, int(thickness)))

            sblit = rv.subpixel_blit
            ending_bg = g.mode in ("end_v", "end_p", "end_b")

            # --- 1. backdrop: the rising grid ---------------------------------
            if g.void:
                # The hard cut: no grid, no ambience, no interface. Black,
                # and whatever is left of her.
                rv.blit(rect("#000000", 1280, 720), (0, 0))
            elif not g.room_live:
                rv.blit(rect("#000000", 1280, 720), (0, 0))
            elif TSB_SHADER_OK:
                if g.mode == "end_p":
                    # No victory-green: the room drains with the body.
                    accent = (0.22, 0.20, 0.30)
                elif g.phase == 2 and g.boss_hp <= TSB_LIMP_HP:
                    # The color itself gives up before she does.
                    accent = (0.30, 0.27, 0.29)
                elif g.phase == 2:
                    # A two-beat heartbeat drives the red: lub, dub, silence.
                    hb = g.tick % 96
                    if hb < 10:
                        beat = math.sin(hb / 10.0 * math.pi)
                    elif 26 <= hb < 34:
                        beat = 0.6 * math.sin((hb - 26) / 8.0 * math.pi)
                    else:
                        beat = 0.0
                    accent = (0.62 + 0.24 * beat, 0.14, 0.26 + 0.05 * beat)
                else:
                    accent = (0.45, 0.13, 0.19)
                breath = 0.0
                if g.phase == 2 and not ending_bg and g.mode != "dead":
                    # Shallow, uneven attenuation only; the EMS motion carries
                    # the escalation without a full-screen luminance pulse.
                    breath = 0.015 + 0.025 * (0.5 + 0.5 * math.sin(g.tick * 0.011))
                phase_mix = 1.0 if g.phase == 2 else 0.0
                if g.mode == "shift":
                    # Start starving the spectrum beneath the white impact,
                    # not at _after_shift (which lands several spoken beats
                    # after the pose and vocal track have already changed).
                    impact = 200 if g.shift_kind == "v" else 210
                    raw_mix = tsb_clamp((g.mtick - impact) / 36.0, 0.0, 1.0)
                    phase_mix = raw_mix * raw_mix * (3.0 - 2.0 * raw_mix)
                try:
                    # mesh True + an OPAQUE base: the proven combo for a
                    # procedural shader-on-Solid quad in this project (the
                    # calendar dial found the transparent-base trap first).
                    quad = Transform(Solid("#000000ff"), xysize=(1280, 720),
                                    mesh=True, shader="tsb.grid",
                                    u_tsb_res=(1280.0, 720.0),
                                    u_tsb_col=accent,
                                    u_tsb_phase_mix=phase_mix,
                                    u_tsb_ems=getattr(g, "ems_progress",
                                                    0.5 if g.phase == 2 else 0.0),
                                    u_tsb_ems_time=getattr(g, "ems_clock", 0.0),
                                    u_tsb_scroll=getattr(g, "stage_scroll", 0.0),
                                    u_tsb_flash=0.0,
                                    u_tsb_dark=breath)
                    qr = renpy.render(quad, 1280, 720, st, at)
                    rv.depends_on(qr)
                    rv.blit(qr, (0, 0))
                except Exception as shader_e:
                    TSB_SHADER_OK = False
                    try:
                        renpy.log("TSB FX: backdrop shader render failed: %r" % shader_e)
                    except Exception:
                        pass
                    rv.blit(rect("#05060e", 1280, 720), (0, 0))
            else:
                rv.blit(rect("#05060e", 1280, 720), (0, 0))

            # --- 2. upward-rush ambience (streaks + petals, full screen) ------
            if not g.void and g.room_live:
                streak_alpha = "46" if g.phase == 2 else "38"
                for s in g.streaks:
                    lq = int(s["len"] // 20) * 20
                    rv.blit(rect(TSB_AMB_PAL[s["ci"]] + streak_alpha,
                                2, max(20, lq)),
                            (int(s["x"]), int(s["y"] - s["len"])))
                amb_phase = 1 if g.phase == 2 else 0
                for m in g.amb_petals:
                    rb = int(m.get("ra", 0.0) / TSB_ROT_DEG) % TSB_ROT_BUCKETS
                    shadow_key = ("ambshadow", m["scb"], rb)
                    shadow_d = self._misc(shadow_key, (lambda s=m["scb"], b=rb: Transform(
                        EMB_DIR + "pellet.png", zoom=0.9 + 0.35 * s,
                        nearest=True, subpixel=True, rotate=b * TSB_ROT_DEG,
                        matrixcolor=TintMatrix("#050611"), alpha=0.78)))
                    sr, (sw, sh) = tex(shadow_key, shadow_d, 40, 40)
                    sblit(sr, (m["x"] - sw / 2.0 + 2.0,
                                m["y"] - sh / 2.0 + 2.0))

                    akey = ("amb", m["ci"], m["scb"], rb, amb_phase)
                    amb_d = self._misc(akey, (lambda ci=m["ci"], s=m["scb"], b=rb, ap=amb_phase: Transform(
                        EMB_DIR + "pellet.png", zoom=0.9 + 0.35 * s,
                        nearest=True, subpixel=True, rotate=b * TSB_ROT_DEG,
                        matrixcolor=TintMatrix(TSB_AMB_PAL[ci]),
                        alpha=(0.68 if ap else 0.58))))
                    ar, (aw, ah) = tex(akey, amb_d, 40, 40)
                    sblit(ar, (m["x"] - aw / 2.0, m["y"] - ah / 2.0))

            # --- 3. boss sprite + strings --------------------------------------
            motion = tsb_boss_motion(g)
            asset_key = motion["asset_key"]
            img_path = motion["path"]
            bw_ = motion["drawn_w"]
            bh_ = motion["drawn_h"]
            center_x = motion["center_x"]
            center_y = motion["center_y"]
            rot = motion["rotation"]

            def boss_variant(angle, alpha_bucket=10, tint=None):
                aq = float(round(angle))
                ab = max(0, min(10, int(alpha_bucket)))
                key = ("boss_pose", asset_key, motion["breath_bucket"],
                       aq, ab, tint)
                props = dict(xzoom=motion["scale_x"],
                            yzoom=motion["scale_y"], nearest=True,
                            subpixel=False, rotate=aq, rotate_pad=False,
                            matrixcolor=TSB_LINEART_MATRIX,
                            alpha=ab / 10.0)
                if tint is not None:
                    props["matrixcolor"] = (TintMatrix(tint) *
                                            TSB_LINEART_MATRIX)
                disp = self._misc(key, (lambda p=img_path, kw=props: Transform(p, **kw)))
                return key, disp

            # Body anchors are rotated around the sprite center, so the strings
            # stay attached through hit recoil, phase yanks, and both falls.
            rel_anchors = [
                (px * motion["scale_x"] - bw_ * 0.5,
                 py * motion["scale_y"] - bh_ * 0.5)
                for px, py in motion["anchors"]
            ]
            rr = math.radians(rot)
            rc = math.cos(rr)
            rs = math.sin(rr)
            anchors = []
            for rax, ray in rel_anchors:
                anchors.append((center_x + rax * rc - ray * rs,
                                center_y + rax * rs + ray * rc))

            if g.strings_alpha > 0.02 and not g.boss_fallen:
                alpha = tsb_clamp(g.strings_alpha, 0.0, 1.0)
                core_a = int((0.26 + 0.56 * alpha) * 255)
                glow_a = int((0.05 + 0.16 * alpha) * 255)
                core_col = "#e8e4ff%02x" % core_a
                glow_col = "#8f83ff%02x" % glow_a
                for i in range(5):
                    if i in g.cut_string_ids:
                        continue
                    ax, ay = anchors[i]
                    tx = (TSB_BOSS_X + TSBStage.STRING_TOPS[i] +
                        math.sin(g.tick * 0.026 + i * 1.7) * (4.0 + 4.0 * alpha))
                    ty = -14.0
                    bow = math.sin(g.tick * 0.035 + i * 1.31) * (5.0 + 8.0 * alpha)
                    if g.phase == 2:
                        # High-frequency shiver: the strings are under more
                        # load than they want anyone to know.
                        bow += math.sin(g.tick * 0.9 + i * 2.3) * 2.4
                    points = [(tx, ty)]
                    segments = 9
                    for seg in range(1, segments + 1):
                        u = seg / float(segments)
                        nx = tx + (ax - tx) * u + math.sin(math.pi * u) * bow
                        ny = ty + (ay - ty) * u
                        points.append((nx, ny))
                    polyline(points, glow_col, 5)
                    polyline(points, core_col, 2)

            # Severed ends recoil upward and leave a short lower tail. These
            # persist just long enough for each individual cut to read.
            for snap in g.string_snap_fx:
                age = g.tick - snap["born"]
                if age < 0 or age >= 72:
                    continue
                frac = age / 72.0
                col = ("#ff4f6f" if snap.get("violent") else "#e8e4ff")
                ahex = "%02x" % int(max(0.0, 1.0 - frac) * 210)
                sx = snap["x"]
                sy = snap["y"]
                curl = math.sin(age * 0.28 + snap["index"]) * 12.0
                line(sx, sy - age * 3.6, sx + curl, sy - 58.0 - age * 5.0,
                    col + ahex, 2)
                line(sx, sy, sx - curl * 0.45, sy + 24.0 + age * 1.1,
                    col + ahex, 2)

            # While she's actually falling, line-art echoes trail above her:
            # the drop reads as speed and weight, not choreography.
            if g.void and not g.fall_landed and g.fall_vy > 3.0:
                ghost_col = "#8a90a0" if g.mode == "end_p" else "#e13b4e"
                for gi in (2, 1):
                    old_rot = max(0.0, rot - gi * 6.0)
                    gkey, gd = boss_variant(old_rot, 1, ghost_col)
                    gr, (gw, gh) = tex(gkey, gd, 520, 520)
                    rv.blit(gr, (int(round(center_x - gw * 0.5)),
                                 int(round(center_y - g.fall_vy * gi * 2.0
                                           - gh * 0.5))))

            if g.boss_alpha > 0.0:
                main_ab = int(tsb_clamp(g.boss_alpha, 0.0, 1.0) * 10)
                pose_key, pose_d = boss_variant(rot, main_ab)
                pose_r, (pose_w, pose_h) = tex(pose_key, pose_d, 520, 520)
                rv.blit(pose_r, (int(round(center_x - pose_w * 0.5)),
                                 int(round(center_y - pose_h * 0.5))))

            # Slash arc on a landed FIGHT.
            if g.tick - g.slash_born < 10:
                p = (g.tick - g.slash_born) / 10.0
                skey2 = ("slash", int(p * 3))
                sl_d = self._misc(skey2, (lambda a=int(p * 3): Transform(
                    EMB_DIR + "bullet.png", xzoom=7.0, yzoom=0.5,
                    rotate=-38, matrixcolor=TintMatrix("#f5f5f0"),
                    alpha=0.85 - 0.25 * a)))
                slr, (slw, slh) = tex(skey2, sl_d, 220, 220)
                sblit(slr, (TSB_BOSS_X - slw / 2.0 - 30 + p * 60,
                            TSB_BOSS_FEET_Y - 210 - slh / 2.0 + p * 40))

            # Her HP bar, only shown briefly after a hit (UT-style tell).
            # It slides in and dissolves away instead of blinking.
            if g.tick < g.boss_hp_show_until and not g.void:
                remain = g.boss_hp_show_until - g.tick
                bar_a = tsb_clamp(min((110 - remain) / 7.0, remain / 22.0),
                                0.0, 1.0)
                frac = tsb_clamp(g.boss_hp / TSB_BOSS_HP, 0.0, 1.0)
                bbx = int(TSB_BOSS_X - 120)
                # Fixed near the top of the battle stage: the shared 184x344
                # cell includes a little transparent breathing room above the
                # differently hunched poses, so its canvas top is not her head.
                bby = 6 - int((1.0 - bar_a) * 6)
                rv.blit(rect("#f5f5f0" + qa(0.95 * bar_a), 244, 18),
                        (bbx - 2, bby - 2))
                rv.blit(rect("#3a0a10" + qa(bar_a), 240, 14), (bbx, bby))
                if frac > 0.0:
                    rv.blit(rect(("#39d97e" if frac > 0.35 else "#ffe23d")
                                + qa(bar_a), int(240 * frac), 14),
                            (bbx, bby))

            # --- 3b. mercy gauge ------------------------------------------------
            # A persistent readout pinned to the sprite's lower right so the
            # player can read SPARE readiness without opening ACT/MERCY. Fills
            # toward the threshold, then goes spare-yellow and relabels itself
            # the moment SPARE will actually do something. Hidden during the
            # dodge (bullets own the box then) and during cinematics. Anchored
            # to the sprite's static right edge, so it never jitters with the
            # sag/yank or hit recoil.
            m_hide = ("dodge", "intro", "shift", "end_v", "end_p", "end_b", "dead")
            if g.hud_alpha > 0.02 and not g.void and g.mode not in m_hide:
                if g.phase == 1:
                    m_cur, m_need = g.mercy, (1 if g.debug else TSB_MERCY_NEED)
                else:
                    m_cur, m_need = g.mercy2, (1 if g.debug else TSB_MERCY2_NEED)
                m_frac = tsb_clamp(m_cur / float(m_need), 0.0, 1.0)
                m_ready = m_cur >= m_need
                mgw = 14
                mgh = 66
                base_boss_w = TSB_BOSS_NATIVE_SIZE[0] * TSB_BOSS_ZOOM
                mgx = int(TSB_BOSS_X + base_boss_w * 0.5 + 12)
                mgy = int(TSB_BOSS_FEET_Y - 6 - mgh)
                rv.blit(rect("#101014", mgw + 4, mgh + 4), (mgx - 2, mgy - 2))
                rv.blit(rect("#3a2e12" if m_ready else "#241d33", mgw, mgh),
                        (mgx, mgy))
                m_fh = int(mgh * m_frac)
                if m_fh > 0:
                    if m_ready:
                        m_fill = "#ffe23d" if (g.tick // 6) % 2 == 0 else "#fff2a0"
                    else:
                        m_fill = "#ff8fb8"
                    rv.blit(rect(m_fill, mgw, m_fh), (mgx, mgy + mgh - m_fh))
                if m_ready:
                    rv.blit(rect("#fff6c0", mgw, 3), (mgx, mgy))
                m_lbl = "SPARE" if m_ready else "MERCY"
                m_lcol = "#ffe23d" if m_ready else "#9aa0b0"
                mlt, (mlw, mlh) = tex(("mercylbl", m_lbl),
                                    self._text(m_lbl, 13, m_lcol,
                                                font=TSB_FONT_UI, bold=True),
                                    140, 30)
                sblit(mlt, (mgx + mgw * 0.5 - mlw * 0.5, mgy - mlh - 3))

            # --- 4. the box ----------------------------------------------------
            bxr, byr, bwr, bhr = g._box_rect()
            if g.box_alpha > 0.02:
                bd = TSB_BORDER
                if g.phase == 2:
                    # The box strains at its seams: a red under-glow pulsing
                    # on the same heartbeat as the room. (Quantized alpha
                    # buckets keep the solid cache small.)
                    ga = ("26", "3a", "4e", "3a")[(g.tick // 7) % 4]
                    rv.blit(rect("#e13b4e" + ga, bwr + bd * 2 + 10, bhr + bd * 2 + 10),
                            (int(bxr - bd - 5), int(byr - bd - 5)))
                rv.blit(rect("#f5f5f0", bwr + bd * 2, bhr + bd * 2),
                        (int(bxr - bd), int(byr - bd)))
                rv.blit(rect("#000000", bwr, bhr), (int(bxr), int(byr)))

                # --- 5. in-box content ----------------------------------------
                pad = 22
                if g.mode == "menu":
                    # UT exactly: the flavor line owns the box while the four
                    # buttons are live; submenus replace it with options.
                    fl, (flw, flh) = tex(("flavor", g.flavor),
                                        self._text(g.flavor, 21, "#f5f5f0",
                                                    outline=False),
                                        int(bwr - pad * 2), 200)
                    rv.blit(fl, (int(bxr + pad), int(byr + pad - 4)))
                if g.mode in ("act", "item", "mercy") and g.sub:
                    two_col = len(g.sub) >= 4
                    oy = byr + pad + 8
                    for i, opt in enumerate(g.sub):
                        if two_col:
                            ox = bxr + pad + 34 + (i % 2) * (bwr / 2.0 - pad)
                            oyy = oy + (i // 2) * 36
                        else:
                            ox = bxr + pad + 34
                            oyy = oy + i * 36
                        col = "#f5f5f0"
                        if opt == "SPARE":
                            ready = (g.mercy >= (1 if g.debug else TSB_MERCY_NEED)
                                    if g.phase == 1 else
                                    g.mercy2 >= (1 if g.debug else TSB_MERCY2_NEED))
                            if ready:
                                col = TSB_PAL[8]
                        ot, (otw, oth) = tex(("opt", opt, col),
                                            self._text("* " + opt, 21, col,
                                                        outline=False), 300, 40)
                        rv.blit(ot, (int(ox), int(oyy)))
                        if i == g.sub_i:
                            hk = ("heart_cursor",)
                            hd = self._misc(hk, (lambda: Transform(
                                TSB_KT_DIR + "player.png", zoom=1.6,
                                nearest=True)))
                            hr3, (hw3, hh3) = tex(hk, hd, 40, 40)
                            # Vertically centered on the option's text line.
                            sblit(hr3, (ox - 28.0, oyy + oth / 2.0 - hh3 / 2.0))
                    if g.mode == "item" and g.items and g.sub_i < len(g.items):
                        item_key = TSB_ITEMS[g.items[g.sub_i]][0]
                        desc = TSB_ITEM_DESCS.get(item_key, "")
                        if desc:
                            dt, (dtw, dth) = tex(("item_desc", item_key),
                                                self._text(desc, 15, "#8a90a0",
                                                            font=TSB_FONT_UI,
                                                            outline=False),
                                                int(bwr - pad * 2), 28)
                            # A hairline rules the description off from the
                            # option grid so it reads as a status footer.
                            rv.blit(rect("#8a90a055", int(bwr - pad * 2), 1),
                                    (int(bxr + pad), int(byr + bhr - dth - 16)))
                            rv.blit(dt, (int(bxr + pad),
                                        int(byr + bhr - dth - 10)))
                elif g.mode == "ptext" and g.page_i < len(g.pages):
                    page = g.pages[g.page_i]
                    shown = page[:int(g.page_shown)]
                    if shown:
                        pt, (ptw, pth) = tex(("page", g.page_i, len(shown), page),
                                            self._text(shown, 21, "#f5f5f0",
                                                        outline=False),
                                            int(bwr - pad * 2), 200)
                        rv.blit(pt, (int(bxr + pad), int(byr + pad)))
                elif g.mode in ("fight", "strike"):
                    # The accuracy gauge: a sweeping line, a center band.
                    gy = int(byr + bhr / 2.0 - 16)
                    rv.blit(rect("#101018", bwr - 16, 32), (int(bxr + 8), gy))
                    rv.blit(rect("#2a2a3a", 4, 32), (int(bxr + bwr / 2.0 - 2), gy))
                    rv.blit(rect("#f5f5f033", 26, 32), (int(bxr + bwr / 2.0 - 13), gy))
                    pos = tsb_clamp(g.fight_t / float(TSB_FIGHT_SWEEP), 0.0, 1.0)
                    lx = bxr + 10 + pos * (bwr - 24)
                    lcol = "#ffe23d" if g.mode == "strike" else "#ff9c3d"
                    rv.blit(rect(lcol, 5, 44), (int(lx), gy - 6))

            # --- 6. bullets / wires / blooms (drawn over the box) --------------
            hazard_layer = renpy.Render(1280, 720)
            hazard_blit = hazard_layer.blit
            hazard_sblit = hazard_layer.subpixel_blit
            # One canvas carries diagonal live threads and the hairline
            # previews attached to held bullets. It is inserted before sprite
            # blits so petals/needles stay legible on top of their lines.
            hazard_lines = renpy.Render(1280, 720)
            hazard_canvas = hazard_lines.canvas()
            hazard_blit(hazard_lines, (0, 0))
            hazard_tick = (g.heart_break if g.mode == "dead" and
                            g.heart_break >= 0 else g.tick)

            # BLACKOUT. The room is only as big as what you can see: a dark
            # film over the boards (clipped to the box at the end of this
            # section, so it never leaks onto the HUD) and a per-bullet fade
            # by distance from the two light sources -- the SOUL's own glow,
            # and the loose worklight that drifts around the room. Sparks,
            # blooms and telegraph glints are deliberately NOT dimmed: they
            # carry their own light, and they are how the move is played.
            blk = float(getattr(g, "blackout", 0.0))
            lights = None
            if blk > 0.02:
                hazard_blit(rect("#04040a" + qa(0.88 * blk), 1280, 720),
                            (0, 0))
                lights = [(g.px, g.py, 84.0)]
                lsrc = getattr(g, "light_src", None)
                if lsrc is not None:
                    lights.append((lsrc[0], lsrc[1], 136.0))

            for bl in g.blooms:
                p = tsb_clamp((hazard_tick - bl["born"]) /
                                float(bl["fuse"]), 0.0, 1.0)
                # Eased growth: the core swells faster as the fuse burns.
                zb = int(p * p * 6)
                tkey = ("bloomtel", bl["ci"], zb)
                tel_d = self._misc(tkey, (lambda c=bl["ci"], z=zb: Transform(
                    EMB_DIR + "bullet.png", zoom=0.6 + z * 0.35,
                    subpixel=True, matrixcolor=TintMatrix(TSB_PAL[c]),
                    alpha=0.16 + 0.05 * z)))
                tr2, (tw2, th2) = tex(tkey, tel_d, 120, 120)
                hazard_sblit(tr2, (bl["x"] - tw2 / 2.0,
                                    bl["y"] - th2 / 2.0))
                # And a faint outer ring GATHERS inward as it does, so a
                # bloom reads as a flower closing its fist, not a decal.
                zo = 6 - zb
                okey = ("bloomtel_in", bl["ci"], zo)
                o_d = self._misc(okey, (lambda c=bl["ci"], z=zo: Transform(
                    EMB_DIR + "bullet.png", zoom=0.9 + z * 0.45,
                    subpixel=True, matrixcolor=TintMatrix(TSB_PAL[c]),
                    alpha=0.07 + 0.02 * z)))
                or2, (ow2, oh2) = tex(okey, o_d, 160, 160)
                hazard_sblit(or2, (bl["x"] - ow2 / 2.0,
                                    bl["y"] - oh2 / 2.0))

            # Wires and threads live a full animated life: the telegraph
            # DRAWS itself across the box behind a bright tip, breathes and
            # brightens toward the pluck, snaps taut with a brief overshoot
            # flash, then cools out as a dimming filament. Phase 2 adds
            # perpendicular jitter, a live shimmer, and sometimes draws a
            # line from both ends at once -- unstable, sporadic, and still
            # honest: collision stays exactly inside [tel, tel + on].
            p2live = g.phase == 2 and not g.void
            for w in g.wires:
                age = hazard_tick - w["born"]
                tel = w["tel"]
                on = w["on"]
                ci = w["ci"]
                if w.get("killed"):
                    kfade = max(0.0, 1.0 - (hazard_tick
                                            - w.get("kill_t", w["born"])) / 8.0)
                    if kfade <= 0.0:
                        continue
                    wmode, aa = "fade", kfade
                elif age < tel:
                    wmode, aa = "tel", 1.0
                elif age <= tel + on:
                    wmode, aa = "live", 1.0
                else:
                    aa = max(0.0, 1.0 - (age - tel - on) / 10.0)
                    wmode = "fade"
                sweep_len = max(6.0, tel * 0.45)
                prog = tsb_clamp(age / sweep_len, 0.0, 1.0)
                prog = prog * prog * (3.0 - 2.0 * prog)
                breathe = 0.5 + 0.5 * math.sin(age * 0.23 + w["born"] * 0.1)
                urgency = tsb_clamp((age / float(max(tel, 1)) - 0.55) / 0.45,
                                    0.0, 1.0)
                tel_a = 0.13 + 0.10 * breathe + 0.25 * urgency
                snap_k = age - tel
                jig = (math.sin(hazard_tick * 0.9 + w["born"] * 0.7) * 1.6
                    if p2live else 0.0)
                both_ends = p2live and (w["born"] % 3 == 0)
                from_start = (w["born"] % 2 == 0)
                if w["orient"] == "h":
                    yy = w["pos"]
                    sw = int(max(0.0, bwr - 8))
                    if sw <= 1:
                        continue
                    x0 = int(bxr + 4)
                    if wmode == "live":
                        glow_h = 10 + max(0, 8 - snap_k * 2)
                        beam_at(TSB_PAL[ci], x0 + sw * 0.5, yy + jig,
                                sw, glow_h)
                        if snap_k < 5:
                            # Strike flash: the beam again, white and wider,
                            # for the first few frames of the snap.
                            beam_at("#f5f5f0", x0 + sw * 0.5, yy,
                                    sw, glow_h + 4)
                        # Phase 2 strobes the hot core; the beam art carries
                        # its own core, so this is the flicker on top of it.
                        if not p2live or (age // 5) % 2:
                            hazard_blit(rect("#f5f5f0", sw, 3), (x0, int(yy - 1)))
                    elif wmode == "tel":
                        dl = int(sw * prog)
                        col = TSB_PAL[ci] + qa(tel_a)
                        if dl > 1:
                            if both_ends:
                                half = max(1, dl // 2)
                                hazard_blit(rect(col, half, 2),
                                            (x0, int(yy + jig - 1)))
                                hazard_blit(rect(col, half, 2),
                                            (x0 + sw - half,
                                            int(yy + jig - 1)))
                            elif from_start:
                                hazard_blit(rect(col, dl, 2),
                                            (x0, int(yy + jig - 1)))
                            else:
                                hazard_blit(rect(col, dl, 2),
                                            (x0 + sw - dl,
                                            int(yy + jig - 1)))
                        if prog < 1.0:
                            if both_ends:
                                tips = (x0 + dl // 2 - 3,
                                        x0 + sw - dl // 2 - 3)
                            else:
                                tips = ((x0 + dl - 3,) if from_start
                                        else (x0 + sw - dl - 3,))
                            for tip in tips:
                                hazard_blit(rect("#f5f5f0" + qa(0.7), 7, 4),
                                            (tip, int(yy + jig - 2)))
                    else:
                        hazard_blit(rect(TSB_PAL[ci] + qa(0.30 * aa),
                                        sw, 3 if aa > 0.5 else 2),
                                    (x0, int(yy - 1)))
                        hazard_blit(rect("#f5f5f0" + qa(0.5 * aa), sw, 1),
                                    (x0, int(yy)))
                elif w["orient"] == "v":
                    xx = w["pos"]
                    sh = int(max(0.0, bhr - 8))
                    if sh <= 1:
                        continue
                    y0 = int(byr + 4)
                    if wmode == "live":
                        glow_w = 10 + max(0, 8 - snap_k * 2)
                        beam_at(TSB_PAL[ci], xx + jig, y0 + sh * 0.5,
                                sh, glow_w, vertical=True)
                        if snap_k < 5:
                            beam_at("#f5f5f0", xx, y0 + sh * 0.5,
                                    sh, glow_w + 4, vertical=True)
                        if not p2live or (age // 5) % 2:
                            hazard_blit(rect("#f5f5f0", 3, sh), (int(xx - 1), y0))
                    elif wmode == "tel":
                        dl = int(sh * prog)
                        col = TSB_PAL[ci] + qa(tel_a)
                        if dl > 1:
                            if both_ends:
                                half = max(1, dl // 2)
                                hazard_blit(rect(col, 2, half),
                                            (int(xx + jig - 1), y0))
                                hazard_blit(rect(col, 2, half),
                                            (int(xx + jig - 1),
                                            y0 + sh - half))
                            elif from_start:
                                hazard_blit(rect(col, 2, dl),
                                            (int(xx + jig - 1), y0))
                            else:
                                hazard_blit(rect(col, 2, dl),
                                            (int(xx + jig - 1),
                                            y0 + sh - dl))
                        if prog < 1.0:
                            if both_ends:
                                tips = (y0 + dl // 2 - 3,
                                        y0 + sh - dl // 2 - 3)
                            else:
                                tips = ((y0 + dl - 3,) if from_start
                                        else (y0 + sh - dl - 3,))
                            for tip in tips:
                                hazard_blit(rect("#f5f5f0" + qa(0.7), 4, 7),
                                            (int(xx + jig - 2), tip))
                    else:
                        hazard_blit(rect(TSB_PAL[ci] + qa(0.30 * aa),
                                        3 if aa > 0.5 else 2, sh),
                                    (int(xx - 1), y0))
                        hazard_blit(rect("#f5f5f0" + qa(0.5 * aa), 1, sh),
                                    (int(xx), y0))
                else:
                    x1, y1 = w["x1"], w["y1"]
                    x2, y2 = w["x2"], w["y2"]
                    width2 = max(2, int(round(w.get("width", 5.0))))
                    if wmode == "live":
                        pa = (int(round(x1)), int(round(y1)))
                        pb = (int(round(x2)), int(round(y2)))
                        hazard_canvas.line(TSB_PAL[ci] + "55",
                                            (pa[0], pa[1] + int(jig)),
                                            (pb[0], pb[1] + int(jig)),
                                            width2 * 2)
                        if snap_k < 5:
                            hazard_canvas.line("#f5f5f0"
                                                + qa(0.5 - snap_k * 0.09),
                                                pa, pb, width2 * 2 + 3)
                        hazard_canvas.line("#f5f5f0", pa, pb,
                                            max(2, width2 // 2))
                    elif wmode == "tel":
                        ex = x1 + (x2 - x1) * prog
                        ey = y1 + (y2 - y1) * prog
                        hazard_canvas.line(TSB_PAL[ci] + qa(tel_a),
                                            (int(x1), int(y1 + jig)),
                                            (int(ex), int(ey + jig)), 2)
                        if prog < 1.0:
                            hazard_canvas.circle("#f5f5f0" + qa(0.75),
                                                (int(ex), int(ey + jig)), 3)
                    else:
                        hazard_canvas.line(TSB_PAL[ci] + qa(0.30 * aa),
                                            (int(x1), int(y1)),
                                            (int(x2), int(y2)), 2)

            # THE MARK. Spike tape on the boards: two crossed strips and
            # a soft ring, in spare-yellow when the show wants you standing
            # on it and camellia red when it wants you off. A faint ghost
            # ring is where the mark is about to move to -- the count-in for
            # a light that walks.
            mk = getattr(g, "mark", None)
            if mk is not None and g.mode == "dodge":
                mr = float(mk.get("r", 32.0))
                mcol = TSB_PAL[8] if mk.get("good", True) else TSB_PAL[0]
                mx = int(round(mk["x"]))
                my = int(round(mk["y"]))
                puls = 0.55 + 0.25 * math.sin(hazard_tick * 0.10)
                for ma in (0.7854, -0.7854):
                    ex = int(round(mr * 0.74 * math.cos(ma)))
                    ey = int(round(mr * 0.74 * math.sin(ma)))
                    hazard_canvas.line(mcol + qa(puls),
                                        (mx - ex, my - ey),
                                        (mx + ex, my + ey), 3)
                ring = []
                for mi in range(18):
                    ma = 6.28318 * mi / 18.0
                    ring.append((int(round(mx + math.cos(ma) * mr)),
                                int(round(my + math.sin(ma) * mr))))
                hazard_canvas.lines(mcol + qa(0.28 + 0.24 * puls), True,
                                    ring, 2)
                gx = mk.get("gx")
                if gx is not None:
                    gy = mk.get("gy", mk["y"])
                    ghost = []
                    for mi in range(18):
                        ma = 6.28318 * mi / 18.0
                        ghost.append((int(round(gx + math.cos(ma) * mr)),
                                    int(round(gy + math.sin(ma) * mr))))
                    hazard_canvas.lines(mcol + qa(0.20), True, ghost, 1)

            # THE STRINGS ON YOU. One line per hook, from its walking anchor
            # to the SOUL. It thickens and whitens as tension loads, so a
            # string about to break is a thing you can SEE about to break --
            # which is the only feedback the marionette card gives you, and
            # all it needs.
            for hk in (getattr(g, "hooks", None) or ()):
                ten = float(hk.get("ten", 0.0))
                hcol = TSB_PAL[int(hk.get("ci", 5))]
                hax = int(round(hk["ax"]))
                hay = int(round(hk["ay"]))
                hpx = int(round(g.px))
                hpy = int(round(g.py))
                # Loud on purpose. This is the single most important line the
                # renderer draws -- a player who cannot see the string on them
                # is just being shoved by an invisible hand -- so it is drawn
                # as a soft wide body under a hot core, both of which thicken
                # and whiten as the line loads toward breaking.
                hazard_canvas.line(hcol + qa(0.30 + 0.28 * ten),
                                    (hax, hay), (hpx, hpy),
                                    5 + int(ten * 4.0))
                hazard_canvas.line(hcol + qa(0.86),
                                    (hax, hay), (hpx, hpy),
                                    2 + int(ten * 2.0))
                if ten > 0.28:
                    hazard_canvas.line("#ffffff" + qa(0.35 + 0.65 * ten),
                                        (hax, hay), (hpx, hpy), 1)
                # A bead runs the line toward the SOUL, so a string reads as
                # something actively pulling rather than something attached.
                bt = ((hazard_tick * 0.02) % 1.0)
                hazard_canvas.circle(
                    "#ffffff" + qa(0.45 + 0.45 * ten),
                    (int(hax + (hpx - hax) * bt),
                        int(hay + (hpy - hay) * bt)), 3)
                hazard_canvas.circle(hcol + qa(0.90), (hax, hay), 5)
                hazard_canvas.circle("#ffffff" + qa(0.55), (hax, hay), 2)

            # TOO LOUD. The rim closes in and brightens as the level rises,
            # so the hold-still cue is spatial as well as audible.
            loudv = float(getattr(g, "loud", 0.0))
            if loudv > 0.02:
                # Drawn as SOLID BARS, not a canvas outline: Canvas.lines
                # honours the colour but flattens the width to a hairline, and
                # this particular cue cannot afford to be subtle -- it is the
                # one moment in the fight where the correct answer is to take
                # your hands off the keys, and it has to be legible in
                # peripheral vision, from a dark room, mid-panic.
                ins = int(4 + 10 * (1.0 - loudv))
                lw = int(bwr) - 2 * ins
                lh = int(bhr) - 2 * ins
                if lw > 8 and lh > 8:
                    band = int(3 + 13 * loudv)
                    lx0 = int(bxr) + ins
                    ly0 = int(byr) + ins
                    lc = "#fff3d0" + qa(0.18 + 0.66 * loudv)
                    hazard_blit(rect(lc, lw, band), (lx0, ly0))
                    hazard_blit(rect(lc, lw, band), (lx0, ly0 + lh - band))
                    hazard_blit(rect(lc, band, lh), (lx0, ly0))
                    hazard_blit(rect(lc, band, lh), (lx0 + lw - band, ly0))
                    # and the whole room warms with it, under the bullets.
                    hazard_blit(rect("#ffe9b0" + qa(0.04 + 0.14 * loudv),
                                    lw, lh), (lx0, ly0))

            for b in g.bullets:
                tether = b.get("tether")
                if tether is not None and b["age"] < tether.get("until", 0):
                    # These lines never collide; they are a promise about the
                    # delayed release. Their restraint keeps the control motif
                    # present without putting a label on it.
                    ta = b["age"] / float(max(1, tether.get("until", 1)))
                    alpha = 52 + int(92 * ta)
                    hazard_canvas.line(
                        "#e8e4ff%02x" % min(190, alpha),
                        (int(round(b["x"])), int(round(b["y"]))),
                        (int(round(tether["x"])), int(round(tether["y"]))),
                        1 if ta < 0.65 else 2)
                    # A runner dot flows down the promise line and arrives
                    # exactly at the release tick -- the countdown is the
                    # motion itself.
                    rx = b["x"] + (tether["x"] - b["x"]) * ta
                    ry = b["y"] + (tether["y"] - b["y"]) * ta
                    hazard_canvas.circle("#f5f5f0" + qa(0.35 + 0.5 * ta),
                                        (int(rx), int(ry)), 2)
                ab = 3
                if b["fz"]:
                    ab = min(2, int(b["fz"] / 7))
                elif b["age"] < 6:
                    # Materialize in three quick alpha steps -- nothing in
                    # the box pops in at full presence anymore.
                    ab = 1 + b["age"] // 3
                if lights is not None and not b.get("heal"):
                    seen = 0.0
                    for lx_, ly_, lr_ in lights:
                        ld = math.hypot(b["x"] - lx_, b["y"] - ly_)
                        seen = max(seen, 1.0 - tsb_clamp(
                            (ld - lr_ * 0.55) / (lr_ * 0.80), 0.0, 1.0))
                    ab = min(ab, int(round(3.0 * (1.0 - blk * (1.0 - seen)))))
                sq_draw = b["sq"]
                if not b["fz"] and b["age"] < 6:
                    sq_draw = max(2, b["sq"] - (2 - b["age"] // 3))
                if b["kind"] == "needle":
                    nkey = ("needle", 1 if b["vx"] > 0 else 0, ab)
                    nd = self._misc(nkey, (lambda d=(1 if b["vx"] > 0 else 0), a=ab: Transform(
                        EMB_DIR + "dagger.png", zoom=1.6, nearest=True,
                        subpixel=True, rotate=(90 if d else -90),
                        matrixcolor=TintMatrix(TSB_PAL[3]),
                        alpha=(1.0 if a >= 3 else 0.25 + 0.25 * a))))
                    nr2, (nw2, nh2) = tex(nkey, nd, 60, 60)
                    hazard_sblit(nr2, (b["x"] - nw2 / 2.0,
                                        b["y"] - nh2 / 2.0))
                    continue
                render_bucket = (b["rb"] if TSBStage.KINDS[b["kind"]][2]
                                else 0)
                bd2 = self._bullet_tf(b["kind"], b["ci"], render_bucket,
                                    sq_draw, ab)
                br2, (bw2, bh2) = tex((b["kind"], b["ci"], render_bucket,
                                        sq_draw, ab),
                                        bd2, 64, 64)
                hazard_sblit(br2, (b["x"] - bw2 / 2.0,
                                    b["y"] - bh2 / 2.0))

            # Crop the hazard canvas to the box. This is a CLIP FLAG on a one-
            # child wrapper, not Render.subsurface: subsurface walks every child
            # of the layer, computes two sublines apiece and builds a fresh
            # cropped Render around each (recursing once more into the blitted
            # texture's own Render). With TSB_MAX_BULLETS at 340 that was well
            # over a thousand throwaway Render objects a frame -- every one of
            # them a python object with two lists and a set, appended to
            # renpy.display.render.live_renders and walked and killed again by
            # the next frame's mark_sweep -- to produce pixels identical to
            # these three lines. gl2 turns xclipping/yclipping into a clip
            # polygon and crops the quads on its own side for free.
            clip_x = int(bxr)
            clip_y = int(byr)
            clip_w = max(1, int(bwr))
            clip_h = max(1, int(bhr))
            clipped_hazards = renpy.Render(clip_w, clip_h)
            clipped_hazards.xclipping = True
            clipped_hazards.yclipping = True
            clipped_hazards.blit(hazard_layer, (-clip_x, -clip_y))
            rv.blit(clipped_hazards, (clip_x, clip_y))

            # --- 7. sparks ------------------------------------------------------
            for sp in g.sparks:
                frac = sp["age"] / float(sp["ttl"])
                ab2 = 2 - min(2, int(frac * 3))
                skey3 = ("spark", sp["ci"], ab2)
                sp_d = self._misc(skey3, (lambda c=sp["ci"], a=ab2: Transform(
                    EMB_DIR + "bullet.png", zoom=0.4, subpixel=True,
                    matrixcolor=TintMatrix(TSB_PAL[c]), alpha=0.25 + 0.3 * a)))
                spr, (spw, sph) = tex(skey3, sp_d, 32, 32)
                sblit(spr, (sp["x"] - spw / 2.0, sp["y"] - sph / 2.0))

            # --- 8. the SOUL ----------------------------------------------------
            if g.mode == "dodge" and g.heart_break is None:
                blink = g.tick < g.inv_until and (g.tick // 4) % 2 == 0
                if not blink:
                    hk2 = ("soul",)
                    hd2 = self._misc(hk2, (lambda: Transform(
                        TSB_KT_DIR + "player.png", zoom=2.0, nearest=True,
                        subpixel=True)))
                    hr4, (hw4, hh4) = tex(hk2, hd2, 40, 40)
                    sblit(hr4, (g.px - hw4 / 2.0, g.py - hh4 / 2.0))
            elif g.heart_break is not None and g.tick - g.heart_break < 30:
                # The crack before the shatter: the heart, stuttering.
                if (g.tick // 3) % 2 == 0:
                    hk2 = ("soul",)
                    hd2 = self._misc(hk2, (lambda: Transform(
                        TSB_KT_DIR + "player.png", zoom=2.0, nearest=True,
                        subpixel=True)))
                    hr4, (hw4, hh4) = tex(hk2, hd2, 40, 40)
                    sblit(hr4, (g.px - hw4 / 2.0, g.py - hh4 / 2.0))

            # --- 9. damage pops -------------------------------------------------
            for p in g.dmg_pops:
                age = g.tick - p["born"]
                py2 = p["y"] - age * 0.55
                dt2, (dw2, dh2) = tex(("pop", p["txt"], p["ci"], p["big"]),
                                        self._text(p["txt"], 30 if p["big"] else 18,
                                                TSB_PAL[p["ci"]], font=TSB_FONT_UI,
                                                bold=True), 220, 60)
                sblit(dt2, (p["x"] - dw2 / 2.0, py2))

            # --- 10. her speech bubble -----------------------------------------
            # A real comic textbox: drop shadow, dark border on all four
            # sides, white fill, and an outlined tail pointing back at her --
            # not two floating rectangles.
            if g.bubble is not None:
                shown = g.bubble[:int(g.bub_shown)]
                if shown:
                    bt, (btw, bth) = tex(("bub", len(shown), g.bubble),
                                        self._text(shown, 19, "#101014",
                                                    outline=False), 300, 400)
                    bub_w = 344
                    bub_h = bth + 30
                    bub_x = 806
                    bub_y = 96
                    rv.blit(rect("#00000066", bub_w, bub_h), (bub_x + 4, bub_y + 5))
                    rv.blit(rect("#101014", bub_w, bub_h), (bub_x, bub_y))
                    rv.blit(rect("#f5f5f0", bub_w - 6, bub_h - 6),
                            (bub_x + 3, bub_y + 3))
                    # The tail: an outlined triangle whose base merges with
                    # the white fill so the bubble reads as one shape.
                    tail = renpy.Render(22, 28)
                    tc = tail.canvas()
                    tc.polygon("#101014", [(22, 0), (0, 14), (22, 28)])
                    tc.polygon("#f5f5f0", [(22, 5), (7, 14), (22, 23)])
                    rv.blit(tail, (bub_x - 19, bub_y + 22))
                    rv.blit(bt, (bub_x + 20, bub_y + 15))

            # --- 11. HUD --------------------------------------------------------
            if g.hud_alpha > 0.02:
                if (not g.void and
                        g.mode not in ("intro", "end_v", "end_p", "end_b", "dead")):
                    ctrl_text = "ARROWS / WASD MOVE   Z CONFIRM   X CANCEL   SHIFT WALK   ESC PAUSE"
                    ct, (ctw, cth) = tex(("controls_hint",),
                                        self._misc(("controls_hint",),
                                                    lambda: Text(ctrl_text,
                                                                style="msbf_shmup_controls_small")),
                                        900, 28)
                    rv.blit(ct, (int(640 - ctw / 2.0), 702))

                nm = ("%s   LV 1" % (str(g.pname).upper()))
                nt, (ntw, nth) = tex(("hudname", nm),
                                    self._text(nm, 17, "#f5f5f0",
                                                font=TSB_FONT_UI, bold=True),
                                    400, 30)
                rv.blit(nt, (150, 586))
                ht, (htw, hth) = tex(("hudhp",),
                                    self._text("HP", 13, "#f5f5f0",
                                                font=TSB_FONT_UI, bold=True), 60, 24)
                rv.blit(ht, (520, 590))
                rv.blit(rect("#a01824", 120, 18), (552, 586))
                frac2 = tsb_clamp(g.hp / TSB_HP_MAX, 0.0, 1.0)
                if frac2 > 0.0:
                    rv.blit(rect("#ffe23d", int(120 * frac2), 18), (552, 586))
                hpt = "%d / %d" % (int(math.ceil(g.hp)), int(TSB_HP_MAX))
                h2t, (h2w, h2h) = tex(("hudhpv", hpt),
                                    self._text(hpt, 15, "#f5f5f0",
                                                font=TSB_FONT_UI, bold=True),
                                    140, 26)
                rv.blit(h2t, (688, 587))

                # The four buttons. You know the four buttons.
                btn_w, btn_h, gap = 232, 54, 30
                total = btn_w * 4 + gap * 3
                x0 = (1280 - total) / 2.0
                y0 = 626
                in_btn_row = g.mode == "menu"
                for i, label in enumerate(TSBGame.BUTTONS):
                    bx3 = x0 + i * (btn_w + gap)
                    sel = in_btn_row and i == g.menu_i
                    border = "#ffe23d" if sel else "#ff9c3d"
                    rv.blit(rect(border, btn_w, btn_h), (int(bx3), y0))
                    rv.blit(rect("#000000", btn_w - 6, btn_h - 6),
                            (int(bx3 + 3), y0 + 3))
                    lcol2 = "#ffe23d" if sel else "#ff9c3d"
                    lt, (ltw, lth) = tex(("btn", label, sel),
                                        self._text(label, 22, lcol2,
                                                    font=TSB_FONT_UI, bold=True),
                                        220, 40)
                    # Labels stay put on selection; only the SOUL cursor and
                    # the highlight color move. (The old +12px hop read as a
                    # layout bug, not a cursor.)
                    rv.blit(lt, (int(bx3 + btn_w / 2.0 - ltw / 2.0),
                                int(y0 + btn_h / 2.0 - lth / 2.0)))
                    if sel:
                        hk5 = ("heart_cursor",)
                        hd5 = self._misc(hk5, (lambda: Transform(
                            TSB_KT_DIR + "player.png", zoom=1.6, nearest=True)))
                        hr5, (hw5, hh5) = tex(hk5, hd5, 40, 40)
                        sblit(hr5, (bx3 + 18.0, y0 + btn_h / 2.0 - hh5 / 2.0))

            # --- 12. booth line (Matsuda, watching) -----------------------------
            if g.booth is not None:
                bage = g.tick - g.booth["born"]
                if bage < 300:
                    txt = g.booth.get("text", TSB_BOOTH.get(g.booth["key"], ""))
                    if txt:
                        fade = 1.0 if bage < 240 else max(0.0, 1.0 - (bage - 240) / 60.0)
                        fb = int(fade * 2.999)
                        bt2, (bt2w, bt2h) = tex(("booth", txt, fb),
                                                self._text(txt, 15,
                                                            "#ffe23d" if fb >= 2 else "#8a7a20",
                                                            font=TSB_FONT_UI,
                                                            bold=True), 900, 30)
                        rv.blit(bt2, (26, 18))

            # --- 13. overlays ----------------------------------------------------
            if g.flash > 0.0:
                rv.blit(rect("#f5f5f0" + ("%02x" % int(g.flash * 210)), 1280, 720),
                        (0, 0))
            if g.fade_in > 0.0:
                rv.blit(rect("#000000" + ("%02x" % int(g.fade_in * 255)), 1280, 720),
                        (0, 0))
            if g.dark > 0.0:
                rv.blit(rect("#000000" + ("%02x" % int(g.dark * 255)), 1280, 720),
                        (0, 0))

            # The pause plate used to be drawn HERE, as two centred blits. It is
            # a screen (tsb_pause_panel) now, because a CDD cannot hold a
            # draggable widget and the panel carries the audio mixer: the volume
            # moves without leaving the box. The wash below is all that is left.
            if g.paused:
                rv.blit(rect("#000000b8", 1280, 720), (0, 0))

            # THE DRAW RATE IS THE TICK RATE.
            #
            # Every pixel this method produces is a pure function of g.tick:
            # nothing here reads the accumulator, so between two simulation
            # ticks the stage draws a byte-identical picture. `renpy.redraw(
            # self, 0)` asked for the next frame IMMEDIATELY, so on a 144Hz or
            # 240Hz panel this loop ran two to four times per tick and threw
            # the extra frames away -- several hundred python-level blits each,
            # on the most expensive draw in the project.
            #
            # Handing redraw() the time until the NEXT tick instead lets the
            # engine's own scheduler wake us exactly when there is something
            # new to draw. On a 60Hz display nothing changes. Above it, the
            # cost of this stage stops scaling with the refresh rate.
            #
            # (Side effect, and a good one: the HP-bar chip ghost eases per
            # RENDER, so it used to catch up four times faster on a 240Hz
            # panel than on a 60Hz one. Now it is the same everywhere.)
            if _perf:
                msbf_perf_t1("draw", _t)

            if g.result is None and not g.paused:
                renpy.redraw(self, max(0.0, TSB_TICK - self.acc))
            return rv
# --- THE PAUSE PANEL -----------------------------------------------------------
# Screen language, not CDD blits, for one reason: the AUDIO block. A mixer slider
# is a draggable widget, and a Creator-Defined Displayable can draw one but can
# never be one -- so the whole plate moved out here when the volume did.
#
# These are the SAME `Preference("... volume")` bars the Settings screen and the
# Matsuda fight's pause menu use, so this is the game's one persistent mix being
# nudged mid-fight, not a per-fight copy of it. Her instrumental and vocal stems
# ride `track1`/`track2`, both registered on the `music` mixer, and every hit,
# blip and text cue rides `sfx` -- so both bars are live in here.
#
# Her palette, so it reads as part of the box: bone white on black, NovaSquare,
# hard 2px rules. The wash behind it is still drawn inside TSBStage.
screen tsb_pause_panel(game):

    # An outer frame that is nothing but 2px of bone white, sized by the inner
    # one: that is how you get a real UT/DR box border without hardcoding a
    # height the content could outgrow.
    frame:
        style "tsb_pause_border"
        xalign 0.5
        yalign 0.5

        frame:
            style "tsb_pause_frame"

            vbox:
                spacing 12
                xsize 400

                text "PAUSED" style "tsb_pause_title" xalign 0.5

                add Solid("#f5f5f0") xysize (400, 2)

                text "AUDIO" style "tsb_pause_section"

                vbox:
                    spacing 5

                    if config.has_music:
                        text "MUSIC" style "tsb_pause_small"
                        bar value Preference("music volume") style "tsb_pause_slider"
                        null height 8

                    if config.has_sound:
                        text "SOUND" style "tsb_pause_small"
                        bar value Preference("sound volume") style "tsb_pause_slider"
                        null height 8

                    if config.has_voice:
                        text "VOICE" style "tsb_pause_small"
                        bar value Preference("voice volume") style "tsb_pause_slider"
                        null height 8

                    if config.has_music or config.has_sound or config.has_voice:
                        textbutton _("MUTE ALL"):
                            style "tsb_pause_button"
                            action Preference("all mute", "toggle")

                add Solid("#4a4f5a") xysize (400, 2)

                hbox:
                    xalign 0.5
                    spacing 24

                    textbutton _("RESUME"):
                        style "tsb_pause_button"
                        action Function(game.toggle_pause)

                    textbutton _("LEAVE"):
                        style "tsb_pause_quit_button"
                        action Function(game.give_up)

                text "ESC  RESUME        Q  LEAVE HER HANGING":
                    style "tsb_pause_hint"
                    xalign 0.5


# --- THE SCREEN ----------------------------------------------------------------
# Static tree: one CDD does everything, plus the pause panel above when the
# fight is stopped. The 0.25s timer only polls for a terminal result
# (_update_screens=False so a None poll never rebuilds the interaction and
# bleeds the sim's accumulator).
screen tsb_fight_screen(game):
    modal True
    use enter_m_input_lock()

    add Solid("#05060e")
    add TSBStage(game)

    if game.paused:
        use tsb_pause_panel(game)

    key "K_ESCAPE" action Function(game.toggle_pause)
    key "mouseup_3" action Function(game.toggle_pause)
    if game.paused:
        key "K_q" action Function(game.give_up)

    timer 0.25 repeat True action Function(tsb_poll_result, game, _update_screens=False)

# --- STORY WRAPPER ---------------------------------------------------------------
# Entry point -- jumped from cs_matsuda_02's roster menu (Matsuda is on screen,
# bg ether, enterm playing). The old placeholder line ("I don't even know what
# Tsubaki's fight IS yet") is canon now: she never wrote it. Something did.
label tsubakimode:
    $ tsb_run_deaths = 0
    $ tsb_retry = False
    $ tsb_debug = False

    menu:
        "Open the door.":
            pass
        "Open the door. {size=-8}(DEV: fast routes){/size}" if config.developer:
            $ tsb_debug = True
            ma "{size=-8}Fine, but the record's in pencil.{/size}"
        "Leave it shut.":
            if persistent.tsubamode_attempts == 0:
                ma "Yeah. Yeah, good call. Great call, even."
                ma "The light stays on, though. ...I'll keep an eye on it. Who else?"
            else:
                ma "Smart. I'll keep watching it. Who else?"
            jump msbf_roster_choice

    if persistent.tsubamode_attempts == 0:
        ma "The switch isn't connected. I'm going to keep trying it."
        ma "Arrows or WASD move. Z confirms. X backs out. Hold Shift when you need smaller steps."
        ma "And [player]... keep her talking, okay?"
    else:
        ma "You know the controls. I'll be here."

    $ persistent.tsubamode_attempts += 1

    show matsuda at thide
    hide matsuda
    stop music fadeout 1.0
    scene black with dissolve_scene_full
    pause 0.8

    call screen koto_keyboard_notice

label tsubamode_fight:
    # Rollback through a live real-time minigame is nonsense (see kototouhou).
    $ renpy.block_rollback()

    $ tsb_game = TSBGame(retry=tsb_retry, visit_deaths=tsb_run_deaths, debug=tsb_debug)

    $ _tsb_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ _tsb_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None
    scene black

    call screen tsb_fight_screen(tsb_game)
    $ _tsb_result = _return

    $ tsb_game = None
    $ quick_menu = _tsb_prev_quick_menu
    $ _game_menu_screen = _tsb_prev_game_menu
    $ tsb_music_stop(1.5)
    $ msbf_stop_pooled_sfx(0.1)
    scene black with dissolve_scene_full

    # THE ENDING THIS RUN REACHED, RECORDED ABOVE THE ARCADE/STORY SPLIT, so
    # both paths record and grant identically and the result labels below only
    # play their dialogue. (The story's NieR true-reset stays down there --
    # that's a flourish, not an award.)
    if _tsb_result == "victory_v":
        $ persistent.tsubamode_outcome = "violence"
        $ tsb_record_route_clear("violence")
        $ ach_grant("tsuba_violence")
    elif _tsb_result == "victory_p":
        $ persistent.tsubamode_outcome = "pacifist"
        $ tsb_record_route_clear("pacifist")
        $ ach_grant("tsuba_spare")
    elif _tsb_result == "victory_b":
        $ persistent.tsubamode_outcome = "betrayal"
        $ tsb_record_route_clear("betrayal")
        $ ach_grant("tsuba_betrayal")
    if _tsb_result in ("victory_v", "victory_p", "victory_b"):
        $ ach_sync()

    # ARCADE: skip all VN result dialogue (and the story's NieR true-reset) ->
    # shared arcade results card. Inert in the in-story path.
    if arcade_active:
        jump arcade_tsuba_result

    if _tsb_result == "victory_p":
        jump tsubamode_victory_p
    elif _tsb_result == "victory_v":
        jump tsubamode_victory_v
    elif _tsb_result == "victory_b":
        jump tsubamode_victory_b
    elif _tsb_result == "quit":
        jump tsubamode_quit
    jump tsubamode_defeat

label tsubamode_defeat:
    $ tsb_run_deaths += 1
    $ tsb_retry = True
    pause 1.0

    if tsb_run_deaths == 1:
        ma "Hey. HEY. You're out. You're back. Look at me a second."
        ma "The room reset the moment you came through. ...She was still staring at the door when it did."
    elif tsb_run_deaths == 2:
        ma "Again. Okay. Breathe. You're here."
        ma "She said your name before the light came up. Not the loud voice she's using in there-- just... your name. Quiet. Then it started the whole thing over."
    else:
        ma "She was already watching the door before it opened. She knew you'd be back."
        ma "I don't know how many times she can sit through that. I really don't want to find out."

    menu:
        "Send me back in.":
            ma "Booth's still hot. Go."
            scene black with dissolve_scene_full
            jump tsubamode_fight
        "I need to stop.":
            ma "Honestly? Might be the sane pick."
            ma "The light's still on. I'll stay with it for a while."
            return

label tsubamode_quit:
    $ tsb_retry = True
    pause 0.5
    ma "Out by the side door, huh."
    ma "No shame in it. That's the only exit in there I actually installed."
    ma "...She's still on the strings, though. I'll keep working the breaker."

    menu:
        "Put me back in.":
            ma "Yeah. Okay. GO!"
            scene black with dissolve_scene_full
            jump tsubamode_fight
        "I can't look at it right now.":
            ma "Then don't. I'll stay here."
            ma "I'll call you if the light changes."
            return

label tsubamode_victory_v:
    pause 2.0
    scene bg ether with dissolve_scene_full
    show matsuda neut at t11 zorder 2

    ma "..."
    ma "I keep waiting for that to turn out not to have happened. It happened, though. I watched the whole thing."
    ma "You had four buttons. FOUR. And you hit the same one, over and over, until she stopped moving. Like it was the only one that was even real to you."
    ma "By the end she wasn't fighting. It was barely throwing anything-- it had nothing left, it wasn't even aiming-- and your hand kept coming up. I kept thinking, okay, this is the swing where you stop. And it just... never was."
    ma "And she thanked you. Every time. It made her thank you, and you let her, and you kept going anyway."
    ma "I genuinely don't understand what I just watched. Her attack was ZERO. You CHECKED it. You knew."
    ma "..."
    ma "The restore point's clean. I can put her back together. She won't remember any of it."
    ma "I'm going to remember all of it."
    ma "[player]. Get out. Please. I can't look at you right now."

    stop music fadeout 2.0
    scene black with dissolve_scene_full
    pause 1.5
    nier "{cps=5}TRUE RESET APPLIED{/cps}"
    call nier_clear from _call_nier_clear_truereset1
    pause 1.0
    return

label tsubamode_victory_p:
    scene black
    pause 1.0
    ma "Tsuba? Hey-- hey, you're off, they're all off, it's OUT of you, you can get up now, you can--"
    ma "Tsuba?"
    pause 1.0
    ma "...Why isn't she getting up."
    ma "You cut every string. Every single one, I counted them with you. I watched you do it exactly, perfectly right. You got all of it off her."
    ma "And she went down anyway. Same as-- ...same as if you'd never even tried."
    ma "...It was always going to end here. However you did it. Whatever you picked."
    ma "It let us choose the route. It just never let us change the ending. It let us pick the font."
    pause 1.5
    ma "...Leave the door open. In case there's ever anything left to come back to it."

    stop music fadeout 2.0
    scene black with dissolve_scene_full
    pause 1.5
    nier "{cps=5}TRUE RESET APPLIED{/cps}"
    call nier_clear from _call_nier_clear_truereset2
    pause 1.0
    return

label tsubamode_victory_b:
    scene black
    pause 2.5
    ma "..."
    ma "Four strings. You cut four strings."
    ma "Do you get what that took? What you had to do to reach that point? By the fourth cut it was barely holding her-- the whole act was coming apart, she'd lost her lines, she was scared and confused and almost-- almost somebody again."
    ma "And you did every bit of that on PURPOSE. You spent the whole fight being gentle just to walk her right up to the edge of out."
    ma "Then you wound up and put everything you had through the last thread holding her together."
    ma "At least the loud way, I could tell myself you never actually met her. That you only ever swung at the thing wearing her face."
    ma "But you met her. You did the WORK. You dragged her almost all the way out-- and THAT is the version of her you picked to kill. At the finish line. On purpose."
    ma "What is WRONG with you? What is actually, genuinely wrong with you?"
    pause 1.5
    ma "And she fell the exact same way she always does. Every route, every time, no matter what anyone does-- she just falls. So you did all of THAT for nothing. You were cruel for NOTHING."
    ma "..."
    ma "Get out. I'm not doing the wrap-up with you. Get out of my booth."
    stop music fadeout 0.35
    window hide(None)
    show white zorder 200
    play sound interjection
    pause 0.06
    hide white
    ma "GET OOOOOOOOOOOOOOOOOOUUUUUT!!!!!!!!!!!!!!!!!!!!!!!!!" with hpunch

    stop music fadeout 2.0
    scene black with dissolve_scene_full
    pause 1.5
    nier "{cps=5}TRUE RESET APPLIED{/cps}"
    call nier_clear from _call_nier_clear_truereset3
    pause 1.0
    return


# =============================================================================
# PAUSE PANEL STYLES
# =============================================================================
# The box's own vocabulary: bone white on black, NovaSquare, hard 2px rules, no
# glow. Font paths are spelled out rather than read from TSB_FONT_UI -- style
# statements and the init python block that defines it share init priority 0.

style tsb_pause_border:
    background Solid("#f5f5f0")
    padding (2, 2)

style tsb_pause_frame:
    background Solid("#000000")
    padding (24, 20)

style tsb_pause_title:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 34
    color "#f5f5f0"
    bold True
    kerning 3.0

style tsb_pause_section:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 17
    color "#f5f5f0"
    bold True
    kerning 3.0

style tsb_pause_small:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 13
    color "#8a90a0"
    kerning 3.0

style tsb_pause_hint:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 14
    color "#8a90a0"
    kerning 1.0

# is slider_slider so the drag feel and the log scale match Settings and the
# Matsuda pause menu exactly; only the width and the trim colour differ.
style tsb_pause_slider is slider_slider:
    xsize 400
    ysize 12
    base_bar Solid("#22242c")
    thumb Solid("#f5f5f0")
    hover_thumb Solid("#ffef5e")

style tsb_pause_button:
    xsize 172
    ysize 36
    background Solid("#12141b")
    hover_background Solid("#2b2e3a")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (10, 6)

style tsb_pause_button_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 16
    color "#8a90a0"
    hover_color "#ffef5e"
    bold True
    kerning 2.0
    xalign 0.5
    yalign 0.5

style tsb_pause_quit_button is tsb_pause_button

style tsb_pause_quit_button_text is tsb_pause_button_text:
    hover_color "#ff4d4d"
