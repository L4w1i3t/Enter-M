# Tsubaki's SOUL-box fight, reached through cs_matsuda_02's alternate roster.
# FIGHT / ACT / ITEM / MERCY feed a turn machine; the SOUL dodges authored
# set-pieces in a moving box, each one a stop on her itinerary. All art is the
# mode's own pixel atlas; pooled SFX and the
# rising grid shader support the marionette staging.
#
# Story: "ASK TSUBAKI FIRST." Matsuda would not write her an act; something
# else did, and it improves her -- fewer apologies, braver, louder, the one who
# goes first. It runs like Sans's fight: she takes your first turn, then one
# beat per turn in fixed order; phase two crosses her lines out mid-bubble
# while she fights to keep the flaws. The full notes head the script tables.
#
# Violence, pacifism and betrayal remain reachable after either phase shift.
# The first crossed threshold chooses the shift cinematic. Earned phase-two
# SPARE spends the mercy bar on a thread; FIGHT with one thread left betrays her.
# Every ending converges on the same void fall; the route changes the words.
# Synchronized instrumental/vocal channels crossfade at the shift without restart.
#
# TSBGame owns state; TSBStage advances it at 60Hz and renders cached displayables.
# step() dispatches intro, menu, fight, ptext, etalk, dodge, shift and ending modes.
# Turn flow: menu -> action -> ptext -> etalk -> dodge -> menu. Dialogue and
# TSB_TURNS_P1/P2 tables sit above the class. Only dodge hazards can hit the player.
# Coordinates use 1280x720 screen pixels, speeds/timers use ticks unless _secs;
# box geometry is (center_x, center_y, width, height), eased toward box_target.
# Persistent attempts/outcome/cleared-route keys and explicit achievement grants
# retain completion history. Do not rename these save-facing fields.

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
            // (2026-09-29: run at about half their old strength over a
            // deeper violet, so the box and its pixel art own the frame the
            // way a Deltarune board owns its dark background.)
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
            vec3 radiant = vec3(0.022, 0.012, 0.046);
            radiant += prism_a * (0.068 + 0.024 * crossfade);
            radiant += prism_b * (0.020 + 0.014 * (1.0 - crossfade));

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

    # The grid's base: ONE object for the whole fight. Built fresh each frame
    # (the old Solid(...) inside the quad), it made the grid's mesh pass
    # render a new full-screen texture every frame: measured Oct 9 2026,
    # phase two's GPU time went 0.50 -> 0.38ms at full clocks with this.
    TSB_GRID_BASE = Solid("#000000ff")

    # Rasterize her strings into a canvas only as big as they are (see HER
    # STRINGS in TSBStage.render). A switch only so the result can be checked
    # against the full-width layer.
    TSB_STRINGS_BBOX = True

    # tsb.alive: bends her pose image along her height -- see SHE BREATHES in
    # the constants block. Output pixel p shows the image at p - d(p), so the
    # content at a row is carried by d; tsb_boss_warp_at() is the Python
    # mirror (keep the two identical). It only resamples tex0 at fragment_300,
    # so renpy.matrixcolor (400: the lineart-to-alpha matrix, a hit's tint)
    # and renpy.alpha (500) still run after it, unchanged. On its own flag, so
    # a failure here leaves the backdrop grid alone and she simply draws rigid.
    TSB_ALIVE_OK = False
    try:
        renpy.register_shader("tsb.alive", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_tsa_size;
            uniform vec4 u_tsa_bands;
            uniform vec2 u_tsa_legs;
            uniform float u_tsa_breath;
            uniform float u_tsa_sway;
            uniform vec2 u_tsa_head;
            uniform float u_tsa_tilt;
            uniform float u_tsa_stretch;
            uniform float u_tsa_tremor;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 p = v_tex_coord * u_tsa_size;
            float crown = u_tsa_bands.x;
            float neck = u_tsa_bands.y;
            float chest = u_tsa_bands.z;
            float waist = u_tsa_bands.w;
            float knee = u_tsa_legs.x;
            float sole = u_tsa_legs.y;
            float up = clamp((sole - p.y) / max(1.0, sole - crown), 0.0, 1.0);
            float w_upper = 1.0 - smoothstep(chest, waist, p.y);
            float w_head = 1.0 - smoothstep(neck - 5.0, neck + 7.0, p.y);
            float w_str = clamp((knee - p.y) / max(1.0, knee - crown), 0.0, 1.0);
            float above = clamp((neck - p.y) / max(1.0, neck - crown), 0.0, 1.0);
            vec2 d;
            d.x = u_tsa_sway * pow(up, 1.35)
                + u_tsa_tremor * w_upper
                + u_tsa_head.x * w_head
                + u_tsa_tilt * w_head * above;
            d.y = -u_tsa_breath * w_upper
                - u_tsa_stretch * w_str * w_str
                + u_tsa_head.y * w_head;
            gl_FragColor = texture2D(tex0, (p - d) / u_tsa_size);
        """)
        TSB_ALIVE_OK = True
    except Exception as _tsb_alive_e:
        TSB_ALIVE_OK = False
        try:
            renpy.log("TSB FX: tsb.alive registration failed: %r" % _tsb_alive_e)
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
    # The SOUL is Kotonoha's heart, on purpose: kotonohamode/player.png
    # recoloured into the three SOUL modes, so the one borrowed sprite is
    # shared grammar and everything else is this mode's own.
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
    # (92, 334) is the lower-body/sole registration point.
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
        "p1_strained": [(140.0, 156.0), (54.0, 177.0), (91.0, 27.0),
                        (69.0, 82.0), (94.0, 109.0)],
        "p2_strained": [(145.0, 135.0), (60.0, 104.0), (69.0, 25.0),
                        (102.0, 67.0), (83.0, 103.0)],
        "p2_exhausted": [(133.0, 143.0), (60.0, 108.0), (65.0, 30.0),
                         (96.0, 70.0), (80.0, 105.0)],
        "p2_limp": [(116.0, 175.0), (54.0, 173.0), (61.0, 41.0),
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

    # --- SHE BREATHES (2026-09-30) ----------------------------------------------
    # One still image per stage, and no new art: the life comes from the
    # tsb.alive shader, which BENDS that image along her height instead of
    # moving it as one rigid card. Her soles never move; the chest rises on the
    # breath while the legs stay planted; her weight shifts side to side from
    # the ankles up, so the crown travels furthest; the head trails the body
    # and nods on its own; a string yank stretches her from above and settles
    # with a bounce; phase 2's twitch snaps the HEAD over; the late stages
    # shiver. Every number is a pure function of the tick and the fight state
    # (no new serialized fields), and the string anchors are pushed through
    # the same bend (tsb_boss_warp_at) so the knots stay tied on.
    #
    # Rows are native pixels of each pose image, measured off the art:
    # (crown, neck, chest, waist, knee, sole).
    TSB_BOSS_BANDS = {
        "p1_clean":     (18.0, 62.0, 106.0, 150.0, 250.0, 333.0),
        "p1_strained":  (17.0, 64.0, 109.0, 152.0, 250.0, 333.0),
        "p2_strained":  (15.0, 62.0, 103.0, 150.0, 248.0, 333.0),
        "p2_exhausted": (20.0, 66.0, 105.0, 155.0, 250.0, 333.0),
        "p2_limp":      (24.0, 76.0, 111.0, 160.0, 252.0, 333.0),
    }

    def _tsb_smooth(e0, e1, x):
        t = (x - e0) / (e1 - e0)
        t = 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)
        return t * t * (3.0 - 2.0 * t)

    def tsb_boss_warp_at(warp, x, y):
        """Where tsb.alive carries the pixel at native (x, y): (dx, dy).

        The exact mirror of the shader's displacement, so anything tied to
        her body (the five string knots) rides the same bend."""
        if not warp:
            return 0.0, 0.0
        crown, neck, chest, waist, knee, sole = warp["bands"]
        up = max(0.0, min(1.0, (sole - y) / max(1.0, sole - crown)))
        w_upper = 1.0 - _tsb_smooth(chest, waist, y)
        w_head = 1.0 - _tsb_smooth(neck - 5.0, neck + 7.0, y)
        w_str = max(0.0, min(1.0, (knee - y) / max(1.0, knee - crown)))
        above = max(0.0, min(1.0, (neck - y) / max(1.0, neck - crown)))
        dx = (warp["sway"] * up ** 1.35 + warp["tremor"] * w_upper
              + warp["head"][0] * w_head + warp["tilt"] * w_head * above)
        dy = (-warp["breath"] * w_upper - warp["stretch"] * w_str * w_str
              + warp["head"][1] * w_head)
        return dx, dy

    def _tsb_breath_curve(tick, wear):
        """0..1: phase 1 an even cosine; phase 2 a short gasp in and a long
        sag out, with late ragged catches that interrupt the cycle."""
        period = (173, 149, 127, 103, 91)[wear]
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
        if wear >= 3:
            gasp_age = (tick + 31 * wear) % 167
            if gasp_age < 17:
                breath = max(breath, math.sin(gasp_age / 17.0 * math.pi))
        return breath

    def _tsb_sway_at(tick, wear):
        """Weight shifting from foot to foot, in native px at the crown. Two
        incommensurate periods, so it never settles into a metronome; heavier
        and slower as she wears, and on the limp stage she swings like a
        weight on the strings."""
        amp = (1.8, 2.0, 2.4, 2.7, 3.2)[wear]
        if wear == 4:
            return amp * math.sin(tick * 2.0 * math.pi / 283.0)
        return amp * (math.sin(tick * 2.0 * math.pi / 347.0)
                      + 0.35 * math.sin(tick * 2.0 * math.pi / 211.0 + 1.3)) / 1.35

    def tsb_boss_motion(game):
        """Deterministic breathing and string-driven motion for one frame.

        Everything is derived from existing simulation state, so old saves and
        rollback do not need new serialized fields. With tsb.alive the body
        bends (see SHE BREATHES above) and the zoom stays a whole 1.0; without
        it the old fallback breathes by a zoom quantized to five steps."""
        asset_key = tsb_boss_asset_key(game)
        filename, wear = TSB_BOSS_ASSETS[asset_key]
        tick = int(getattr(game, "tick", 0))
        mode = getattr(game, "mode", "")
        pose_frozen = (mode in ("end_v", "end_p", "end_b", "dead")
                       or bool(getattr(game, "void", False))
                       or bool(getattr(game, "boss_fallen", False)))
        motion_frozen = pose_frozen or mode == "shift"
        alive = TSB_ALIVE_OK

        breath_raw = 0.0
        breath_bucket = 0
        if not pose_frozen:
            breath_raw = _tsb_breath_curve(tick, wear)
            breath_bucket = max(0, min(4, int(round(breath_raw * 4.0))))

        if alive:
            scale_x = scale_y = TSB_BOSS_ZOOM
        else:
            breath = breath_bucket / 4.0
            x_amp = (0.004, 0.007, 0.009, 0.012, 0.007)[wear]
            y_amp = (0.006, 0.010, 0.013, 0.017, 0.010)[wear]
            scale_x = TSB_BOSS_ZOOM * (1.0 + x_amp * breath)
            scale_y = TSB_BOSS_ZOOM * (1.0 + y_amp * breath)

        puppet_dx = 0.0
        puppet_dy = 0.0
        puppet_rot = 0.0
        yank = 0.0
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
            if alive:
                # The yank is ELASTIC now: the strings haul the top of her up
                # (the stretch), and she rings down over half a second with
                # two small bounces instead of stopping dead. The rigid lift
                # is halved, since the stretch carries most of it.
                puppet_dy *= 0.5
                if age < 45:
                    yank = ((2.5 + 1.8 * wear) * control
                            * math.exp(-age / 7.0) * math.cos(age * 0.55))

        # Phase 2: every few seconds the strings jerk her -- a hard snap of
        # the head and shoulders that nothing in the room asked for. Pure
        # function of the tick, like everything else here.
        twitch = 0.0
        twitch_k = 999
        twitch_sign = 1.0
        if (not motion_frozen and getattr(game, "phase", 1) == 2
                and mode not in ("end_v", "end_p", "end_b")):
            twitch_k = (tick + 41) % 173
            twitch_sign = 1.0 if ((tick + 41) // 173) % 2 else -1.0
            if twitch_k < 5:
                twitch = twitch_sign
        # With the bend on, the HEAD carries most of the snap (tilt below),
        # so the whole-body wrench is eased from 7 degrees to 4.
        puppet_rot += twitch * (4.0 if alive else 7.0)
        puppet_dx += twitch * 5.0

        ending = mode in ("end_v", "end_p", "end_b")
        bob = 0.0 if motion_frozen or ending else (
            math.sin(tick * (0.026 if wear >= 2 else 0.031))
            * (0.65 if wear >= 2 else 0.45))
        # The old idle sway was a whole-sprite rotation that could only land on
        # whole degrees; with the bend doing the swaying it is retired (a
        # rotated card is exactly the stiffness this replaces).
        idle_rot = 0.0 if (motion_frozen or alive) else (
            math.sin(tick * 0.019) * (0.25 + 0.12 * wear))

        hit_age = tick - int(getattr(game, "slash_born", -9999))
        hit_rot = 0.0
        hit_dx = 0.0
        hit_pulse = 0.0
        if 0 <= hit_age < 24 and not getattr(game, "boss_fallen", False):
            hit_pulse = math.sin(hit_age / 24.0 * math.pi)
            hit_rot = -7.0 * hit_pulse
            hit_dx = 15.0 * hit_pulse

        warp = None
        if alive and not motion_frozen:
            sway = _tsb_sway_at(tick, wear)
            breath_amp = (1.8, 2.1, 2.4, 2.8, 1.8)[wear]
            # the head trails the body's sway by a third of a second...
            head_x = (_tsb_sway_at(tick - 20, wear) - sway) * 0.9
            # ...and rides the breath a beat behind the chest (it sits where
            # the chest put it nine ticks ago)
            head_y = -breath_amp * 0.8 * (_tsb_breath_curve(tick - 9, wear)
                                          - _tsb_breath_curve(tick, wear))
            # ...and, once in a long while in phase 1, tips a little, the way
            # someone listening does.
            tilt = 0.0
            if wear < 2:
                tilt = 0.9 * math.sin(tick * 2.0 * math.pi / 523.0) ** 3
            # The twitch belongs to the HEAD: it snaps over, then swings back
            # past centre and settles.
            # (Half as far on the limp stage: her hanging head sits four
            # pixels off the image's left edge, and the bend cannot draw
            # past it.)
            snap = 0.5 if wear == 4 else 1.0
            if twitch_k < 5:
                tilt += twitch_sign * 6.0 * snap
                head_x += twitch_sign * 2.0 * snap
            elif twitch_k < 26:
                a = twitch_k - 5
                tilt += -twitch_sign * 2.5 * snap * math.exp(-a / 5.0) * math.cos(a * 0.6)
            # A landed hit knocks the wind out of her: the chest drops and the
            # head is flung the way the body went.
            breath_px = breath_amp * breath_raw
            breath_px -= 2.5 * hit_pulse
            head_x += 2.5 * hit_pulse
            tremor = 0.0
            if wear >= 2:
                amp = (0.0, 0.0, 0.3, 0.55, 0.8)[wear]
                tremor = amp * (math.sin(tick * 1.9) + 0.6 * math.sin(tick * 3.3 + 1.0)) / 1.6
            warp = {
                "bands": TSB_BOSS_BANDS[asset_key],
                "breath": breath_px,
                "sway": sway,
                "head": (head_x, head_y),
                "tilt": tilt,
                "stretch": yank,
                "tremor": tremor,
            }

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
        anchors = TSB_STRING_ANCHORS[asset_key]
        if warp is not None:
            moved = []
            for ax, ay in anchors:
                wx, wy = tsb_boss_warp_at(warp, ax, ay)
                moved.append((ax + wx, ay + wy))
            anchors = moved
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
            "anchors": anchors,
            "twitch": twitch,
            "warp": warp,
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
    # Raised from 180 (2026-09-01): the polish pass measured every move in
    # the roster pinned at the old cap, which meant _spark_burst was
    # silently dropping the loud ones -- an impact that lands on a full
    # list simply does not draw. Sparks are a flat list of dicts blitted
    # from one cached transform, so the headroom is close to free.
    TSB_MAX_SPARKS = 420
    TSB_ROT_BUCKETS = 24
    TSB_ROT_DEG = 360.0 / TSB_ROT_BUCKETS
    TSB_HEAL_HP = 2.0   # a stitch at a time (raised from 1 with the items)

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

    TSB_FONT_UI = "assets/fonts/NovaSquare-Regular.ttf"  # pause panel

    # --- THE ART (2026-09-29) ------------------------------------------------
    # Everything in the box and on the HUD is this mode's own pixel art, drawn
    # procedurally into assets/bullets/tsubaki/: the stops on her itinerary
    # (books and the
    # shelf, the inflatable sword, the list's pen and blue clip, the arcade
    # critters and coins, both bags, the station clock and its hands, the
    # STAND HERE card, lunch), the FIGHT target and slash, the four button
    # icons, the SOUL in its three modes plus its broken halves -- and Kareda
    # Mono, the 5x9 face every word in the fight is set in.
    #
    # Art is authored at native size and always drawn at an integer scale
    # with nearest sampling, so a pixel is a square of screen pixels. Colour
    # is baked; a key ending ":w" is a whitened copy for the cyan/orange rule
    # tint (and the font is white, tinted per use). ts_atlas.json is the
    # only map from a name to a rect: rebuild the art and this follows.
    TSB_ART_DIR = "assets/bullets/tsubaki/"

    def _tsb_load_atlas():
        import json as _tsb_json
        with renpy.open_file(TSB_ART_DIR + "ts_atlas.json", encoding="utf-8") as fh:
            return _tsb_json.load(fh)

    TSB_ATLAS = _tsb_load_atlas()
    _tsb_art_cells = {}

    def tsb_art(key):
        """One atlas cell as a shared Crop (one texture, many subsurfaces)."""
        d = _tsb_art_cells.get(key)
        if d is None:
            info = TSB_ATLAS["sprites"]
            d = Crop(tuple(info["cells"][key]), TSB_ART_DIR + info["file"])
            _tsb_art_cells[key] = d
        return d

    def tsb_art_size(key):
        return tuple(TSB_ATLAS["sprites"]["cells"][key][2:4])

    def tsb_has_art(key):
        return key in TSB_ATLAS["sprites"]["cells"]

    TSB_GLYPH_W = int(TSB_ATLAS["font"]["w"])
    TSB_GLYPH_H = int(TSB_ATLAS["font"]["h"])
    TSB_GLYPH_ADV = int(TSB_ATLAS["font"]["adv"])

    def tsb_glyph(ch):
        key = "g%d" % ord(ch)
        d = _tsb_art_cells.get(key)
        if d is None:
            info = TSB_ATLAS["font"]
            rect = info["cells"].get(key) or info["cells"]["g63"]
            d = Crop(tuple(rect), TSB_ART_DIR + info["file"])
            _tsb_art_cells[key] = d
        return d

    _tsb_wrap_cache = {}

    def tsb_wrap(text, cols):
        """Greedy word wrap by character count (the face is monospaced).

        Wrapped once per (text, width), so a typewriter never re-flows a word
        it has already started to type.
        """
        key = (text, cols)
        out = _tsb_wrap_cache.get(key)
        if out is None:
            if len(_tsb_wrap_cache) > 400:
                _tsb_wrap_cache.clear()
            out = []
            for para in text.split("\n"):
                line = ""
                for word in para.split(" "):
                    while len(word) > cols:
                        if line:
                            out.append(line)
                            line = ""
                        out.append(word[:cols])
                        word = word[cols:]
                    if not line:
                        line = word
                    elif len(line) + 1 + len(word) <= cols:
                        line += " " + word
                    else:
                        out.append(line)
                        line = word
                out.append(line)
            _tsb_wrap_cache[key] = out
        return out

    _tsb_strike_cache = {}

    def tsb_strike_parse(text):
        """Split a bubble's ~struck~ spans out of its text.

        Returns (plain, struck, ends): the text without the markers, a flag per
        character, and for each struck character the index of the last
        character of its span (the strike lands once the span is typed).
        """
        out = _tsb_strike_cache.get(text)
        if out is None:
            if len(_tsb_strike_cache) > 300:
                _tsb_strike_cache.clear()
            plain, struck = [], []
            on = False
            for ch in text:
                if ch == "~":
                    on = not on
                    continue
                plain.append(ch)
                struck.append(on)
            ends = [0] * len(plain)
            end = -1
            for i in range(len(plain) - 1, -1, -1):
                if struck[i]:
                    if end < 0:
                        end = i
                    ends[i] = end
                else:
                    end = -1
            out = ("".join(plain), struck, ends)
            _tsb_strike_cache[text] = out
        return out

    def tsb_mix(a, b, u):
        u = max(0.0, min(1.0, float(u)))
        ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
        cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
        return "#%02x%02x%02x" % tuple(int(round(x + (y - x) * u)) for x, y in zip(ca, cb))

    # Undertale's two movement colours, as this fight draws them.
    TSB_RULE_COL = {"cyan": "#42c8ff", "orange": "#ffa12e"}
    # The SOUL's three modes.
    TSB_SOUL_ART = {"red": "soul_red", "blue": "soul_blue",
                    "strung": "soul_strung"}
    TSB_SOUL_COL = {"red": "#ff2a2a", "blue": "#3f7bff", "strung": "#c38cff"}

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
            # Heard from here on; the Music Room's scan skips a stem at volume 0.
            music_unlock(audio.tsb_vocal, save=False)
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
        # The 2026-09-29 roster's physical voices: a SOUL changing mode, and
        # the things her itinerary is made of hitting the boards.
        "soul":    (TSB_KT_SE + "se_power1.wav", 0.60),
        "stick":   (TSB_KT_SE + "se_tan01.wav", 0.30),
        "bounce":  (TSB_KT_SE + "se_tan02.wav", 0.30),
        "crack":   (TSB_KT_SE + "se_damage01.wav", 0.35),
        "fizz":    (TSB_KT_SE + "se_graze.wav", 0.45),
        "coin":    (TSB_KT_SE + "se_item00.wav", 0.35),
        "loud":    (TSB_MSBF_SFX + "debuff.wav", 0.55),
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

    # Screen-poll helper (see kototouhou.rpy): a slow timer calls this; a
    # non-None return ends the interaction with that value.
    def tsb_poll_result(game):
        return game.result

    # ---- SCRIPT TABLES -------------------------------------------------------
    # THE STORY (rebuilt 2026-09-30). "ASK TSUBAKI FIRST." Matsuda would not
    # write Tsubaki an act, because every draft was Matsuda putting words in
    # her mouth; she left that card on the door instead. Something took the card
    # down and wrote the act anyway, and the act IMPROVES her: fewer apologies,
    # braver, louder, the one who goes first. What it cuts away falls like a
    # camellia -- whole, never wilting -- and she keeps the pieces.
    #
    # It runs like Sans's fight: one beat per turn, in fixed order, a
    # conversation with YOU that goes somewhere. Phase 1 is her, dry and
    # noticing, telling you small true things about herself while the act gets
    # the details uncomfortably right -- until the card that says STAND HERE
    # turns out to be in her own handwriting, and the last page says she gets
    # better, and she admits she'd like that. Phase 2 (either route) is the
    # act winning ground: her lines are crossed out and rewritten mid-bubble
    # (text between ~tildes~ is drawn struck through), she restarts, loops,
    # snaps at the room, at Matsu, at you, and fights to keep the flaws,
    # because the flaws are the part that is her. The pacifist ending is her
    # saying her own want first.
    #
    # VOICE. She restarts (--), keeps sentences short, puts an apology-shaped
    # preamble before the point, and her jokes are flat corrections. She never
    # delivers a polished setup line -- the act's replacements do, which is how
    # you can tell them apart. She notices things and says the small concrete
    # detail (the magazine tables, the 7:18, the good tape) instead of naming
    # a wound; the player does the arithmetic. The act is never named, never
    # software, never explained. Caps and "!" are rationed in phase 1 and
    # spill in phase 2. No "fuck".
    #
    # THE ROSTER. The attack under each line is the thing the line is about.
    #   (move id, active duration ticks, authored pressure)
    # `authored pressure` stays in the tuple for old save compatibility and is
    # always 1.0. Reprise/late variants key on pattern_slot.
    TSB_TURNS_P1 = [
        ("shelves",     400, 1.0),  # it put her in the bookstore first
        ("sword",       450, 1.0),  # the hurt she never told anyone about
        ("translation", 420, 1.0),  # NEW: Matsu, loud; Tsubaki, the quiet
        ("list",        430, 1.0),  # it reads her notes out loud
        ("arcade",      410, 1.0),  # the high score nobody saw
        ("claw",        480, 1.0),  # NEW: one try; it needed eleven
        ("bags",        400, 1.0),  # half her bag is for other people
        ("clock",       420, 1.0),  # early, so nobody watches her walk in
        ("crowd",       420, 1.0),  # STAND HERE: she's good at being told
        ("crowd",       420, 1.0),  # the card is in her handwriting (reprise)
        ("lunch",       410, 1.0),  # green, your left: care as reflex
        ("itinerary",   460, 1.0),  # the last page says she gets better
    ]

    # PHASE 2 is the same objects losing their order plus the moves that go
    # inside her: `noticing` (her attention, turned on you), `apology` (the
    # sentence she can't finish), `tin` (where the cut pieces go), `strung`
    # (the strings move first) and `revision`. Late slots (list 13, clock 14,
    # strung 15) play their move's "late" variant.
    TSB_TURNS_P2 = [
        ("list",        410, 1.0), # her notes, improved by someone else
        ("noticing",    420, 1.0), # NEW: it uses her noticing on you
        ("crowd",       400, 1.0), # it moved the card while she read it
        ("shelves",     420, 1.0), # her shelves, out of order
        ("apology",     420, 1.0), # NEW: I'm s-- I'm so--
        ("sword",       450, 1.0), # the small things, made the size of the room
        ("clock",       430, 1.0), # early, reversed into late
        ("tin",         430, 1.0), # NEW: washed, labeled, dated
        ("bags",        420, 1.0), # useful is not the same thing
        ("strung",      420, 1.0), # which of us wanted to reach for you
        ("lunch",       410, 1.0), # that one's mine
        ("revision",    430, 1.0), # it rewinds to before it hurt
        ("arcade",      410, 1.0), # it copies whoever's in front of it
        ("list",        410, 1.0), # it can't strike bookstore
        ("clock",       430, 1.0), # ASK TSUBAKI FIRST
        ("strung",      430, 1.0), # no next page
    ]

    # Each entry is (unhurt, hit-last-turn): "hit" means YOU landed a FIGHT
    # on her since her last line. Both variants carry the same beat, so a
    # violence run cannot replace the story with disconnected hit reactions.
    # An entry may be a list of bubbles shown one after another. Action
    # replies are queued before this beat in _begin_etalk.
    TSB_BUBBLES_P1 = [
        ("Sorry about that. I always let everyone go first. I wanted to know what it feels like.",
         ["Ow. Okay. I went first, so I probably had that coming.",
          "It put me in the bookstore first, though. It even got the magazine tables right. That's the part that scares me."]),
        (["Last time I was there, somebody hit me with an inflatable sword. It was the size of a paper-towel roll.",
          "I made it a joke. That's what you do with small things. ...It didn't make it a joke."],
         "That one I'm not making a joke about. The sword I did. It was small, so I made it smaller. It made it the size of the room."),
        (["Usually I translate Matsu. 'Behold' means look. 'The Azure Eye' means her contacts.",
          "In here there's nobody to translate. So it's just loud. I hate loud."],
         "Matsu would've yelled at you for that. I'd have told you what she meant. ...She'd have meant it."),
        ("I write things down so nobody has to tell me twice. It's reading my notes out loud. Those aren't for out loud.",
         "Write that down. No--I will. Nobody else writes in there. That was the rule."),
        ("I got the high score on the shooting game. TSK, right at the top. Somebody asked to see it. I think about that more than I should.",
         "That was a hit. I'm putting it under hits. It's getting to be a long column."),
        (["There was a yellow bird in the claw machine. I told Matsu one try. She did one try.",
          "It needed eleven. I wanted her to do eleven. I didn't say that. ...I'm saying it now."],
         "I said one try. I always say one try. I want someone to hear 'one' and do eleven anyway. ...That's not about the claw machine."),
        ("Half of my bag is for other people. Tissues. The good tape. A pen for whoever forgets theirs. I don't use any of it.",
         "Take whatever you need out of the bag. Everybody does. I don't mind. I'm--checking if I mind."),
        ("I'm early to everything. If you're early, you never have to walk in while everybody's already looking at the door.",
         "Nobody's ever early for me. That's fine. I'm writing it down as fine."),
        ("It keeps putting cards down. STAND HERE. I'm really good at standing where I'm told. It might be the thing I'm best at.",
         "STAND HERE. Okay. I'll stand here and you can do that again. ...Why did I offer that?"),
        (["The card didn't even bend. Nobody's ever put a card down for me before.",
          "...It's in my handwriting. I don't remember writing it. I'd remember. I'm careful with my handwriting."],
         "The card's in my handwriting. I didn't write it. Somebody's using my hand, and they're neater than I am."),
        ("Green, your left--take it. I don't know why I'm helping. It's what I do when I don't know what to do. Eat real food later. Please.",
         "Green by your left. Take it anyway. You hitting me doesn't change whether you should eat."),
        (["I read ahead. The next part says I get better. Braver. Louder. It says I stop apologizing.",
          "...I'd like that. Is that bad? That I'd like that?"],
         ["I read ahead. The next part says I stop flinching when people do that.",
          "It says I get better. I'd like to be better. I'd like to be-- sorry. I'd like to be."]),
    ]
    # Past the last beat (a pacifist who keeps talking, a slow violence run),
    # the act rehearses her. She notices the takes getting cleaner.
    TSB_LOOP_P1 = [
        ("Again? Okay. From the top. It's making me say it better every time.",
         "From the top. I don't flinch as much on the second take. I hate that I noticed."),
        ("Same page again. I don't mind. I like knowing what comes next.",
         "Same page. Same hit. I know where it lands now. That's worse."),
        ("It keeps saying everybody gets a second take. I never asked for the first one.",
         "Take three. Take four. I'm counting. Somebody should be counting."),
        ("Still here. You're still here. Nobody's asking what I want, which is normal, so this is--normal.",
         "Still here. You can stop checking. I'm always still here."),
    ]

    # Phase 2 keeps the conversation and loses the connective tissue. The
    # act's replacements arrive struck-and-rewritten inside her own bubbles;
    # she restarts, catches the revision, and argues with it out loud. Worn
    # variants (a hit, or the exhausted/limp sprite) are sharper, not quieter.
    TSB_BUBBLES_P2_OPEN = {
        "v": ("You knocked me down and it ~helped me up~ stood me up. Stood! Say it stood me up. Somebody say it right!",
              "Down, up, down, up--it keeps fixing the part where I fall. I wanted to fall! Let me have ONE thing!"),
        "p": ("You were kind to me, and it ~took notes~ got nervous. It's rewriting the part of me that liked it. Don't let it!",
              "It's crossing out the nice part! Say it again, the nice thing, before it finishes the sentence for me!"),
    }
    TSB_BUBBLES_P2 = [
        ("I notice things. It's the only--I notice you. You go left when you're scared. Everybody does. It's using that! I'm sorry! ~I'm not sorry.~ Stop taking the sorries!",
         "I notice everything, and it's making me watch you! I don't want to know which way you'll go! I already know! Stop!"),
        ("Stand here. No, there. It moved the card while I was reading it! I READ it! I read it right, I always read it right!",
         "STAND HERE, it says, and then it moves the here. Where am I supposed to be? Somebody point!"),
        ("The shelves are out of order. I'd never-- I shelve by printer, not by title, so the covers-- nobody cares. Nobody ever-- care for ONE second!",
         "It put my books in the wrong order! That's how I know which ones I've read! That's MINE!"),
        ("I'm s-- I'm so-- it keeps cutting the end off! I just want to finish one-- I'm sorry. There! I finished one! Did you hear it?",
         "I'm s-- no. No, I'm not saying it for that. You don't get a sorry for that. ...See? It let that one through. It LIKES that one."),
        ("The sword didn't even hurt! It was stupid and inflatable, and I made it a JOKE, and it's the size of the ROOM! Why does it want the small things?!",
         "It's taking the things I made small on purpose! I made them small so they'd fit!"),
        ("Early. I'm early, I'm always-- it's running backward! Now I'm late, everybody's already there, they're all looking at the door--",
         "Late! I'm late! I'm never late! Who moved the-- don't look at the door! Nobody look at the door!"),
        (["This is where I put them. The parts it cuts off.",
          "Washed. Labeled. Dated. ...Don't laugh. Somebody has to keep them."],
         "Everything it cuts off goes in the tin. I'm running out of tin! What happens when I run out of tin?!"),
        ("Everybody reaches into my bag. That's fine. That's what it's for! I'm what it's for-- ~I'm useful~ --that's NOT the same thing! Tell me it's not the same thing!",
         "Take it. Take whatever. You were going to anyway. Everybody-- no. NO. Ask. Ask first!"),
        ("The strings move first now. I can't tell which of us wanted to reach for you. Did I? I think I did! Let me have that one!",
         "It's moving me toward you, and I can't tell if I'm scared of you or it is! Which one of us is scared?!"),
        ("Take it! Take it, take it! I made that one. Nobody told me to. That one's mine! That one's MINE!",
         "Green! By your-- I don't care that you hit me! Take it! That's the one thing I'm not letting it have!"),
        ("It wants me to say something braver. ~I'm not afraid.~ I'm afraid! I'm afraid, and I'm saying so. That's braver, isn't it? ISN'T it?!",
         "It keeps rewinding to before I got hurt! I don't want the version where it didn't happen! It happened! Leave it in!"),
        ("It copies whoever's in front of it. That's what I do. I copy Matsu, I copy you, I-- oh. Oh, no. Is there anything under the copying?",
         "Say it exactly like her! Like him! Like you! I can do anybody! Ask me to do me! I can't! I CAN'T!"),
        (["It can strike out everything. The sorry. The early. The quiet. The notebook.",
          "It can't strike bookstore. I wanted bookstore. And there's a name I don't say. It doesn't get that either. That's how you know it's mine."],
         "Bookstore! It can't cross out bookstore! Nobody told me to want it! I wanted it FIRST!"),
        ("Matsu put a card on the door. ASK TSUBAKI FIRST. It took the card down. Nobody asks first! Ask me something. Anything. First!",
         "Ask me later-- no! Ask me NOW! Ask me before it answers for me!"),
        ("It's out of lines for me. There's no next page. I think that means-- I think I have to say the next thing myself. ...I don't know how.",
         "No next page. No next cue. Just me. ...Is that allowed? Somebody tell me that's allowed!"),
    ]
    TSB_LOOP_P2 = [
        ("Again. It wants it again! ~I'm fine~ I'm-- stop finishing my sentences!",
         "Again! Every take I'm a little less-- a little less-- what was I?"),
        ("Say my name. Not the whole thing. The one Matsu uses. So I know which draft I'm in.",
         "Tsuba. Tsuba. That's the old draft. Keep calling me the old draft!"),
        ("The camellias keep falling. I tried to catch one. You can't. They just let go.",
         "They let go all at once! Why can't I let go all at once?!"),
        ("I'm still here! I'm still-- check! Somebody check!",
         "Still here. Still. Here. Don't stop checking."),
    ]

    # The command box reports what can be seen and nothing else. Every third
    # phase-2 turn, the act inserts its own editor's note instead.
    TSB_FLAVOR_FIRST = "Tsubaki Kareda waits for you to go first."
    TSB_FLAVOR_P1 = [
        "Her notebook is closed. Her thumb is on the page she wants.",
        "The strings adjust her posture. She adjusts it back, a little.",
        "A camellia drops from somewhere above. Whole. Nobody picks it up.",
        "She checks the ceiling before every correction, then makes it anyway.",
        "Her lips move. She is rehearsing something she will not say.",
        "She smells like hand soap and printer paper.",
    ]
    TSB_FLAVOR_P2 = [
        "She says sorry. The sorry is crossed out. She says it again, smaller.",
        "Two handwritings are arguing across the cover of her notebook.",
        "She flinches at a noise nobody else heard.",
        "The camellias fall faster now. She tries to count them and loses count.",
        "Her face gets the line right. Her hands don't.",
    ]
    TSB_FLAVOR_ENGINE = [
        "DRAFT 2  /  FEWER APOLOGIES",
        "DRAFT 3  /  SHE SPEAKS FIRST",
        "DRAFT 4  /  VOLUME INCREASED",
        "DRAFT 5  /  NOTEBOOK REMOVED",
        "DRAFT 6  /  NAME UNCHANGED, FOR NOW",
        "FINAL DRAFT.  NO FURTHER CHANGES.",
    ]
    TSB_FLAVOR_LIMP = [
        "Her arm rises after her eyes have closed.",
        "She waits for your expression before deciding whether the last hit hurt.",
        "The notebook slides out of her hand. The strings don't bother catching it.",
    ]
    TSB_FLAVOR_LOWHP = "Green at the edge of the pattern. She lets it go before the strings notice."
    TSB_FLAVOR_OVERTURE = "She looks surprised that worked."
    # A clean dodge gets written down. (Shown in place of the turn's flavor
    # every third turn after a move that never touched you.)
    TSB_FLAVOR_NOTED = [
        "She writes something down. It's about you.",
        "She underlines something twice.",
        "She turns the notebook so you can't see the page.",
    ]

    # TALK interrupts the room with ordinary questions. The short reply is
    # followed by the current story beat.
    TSB_ACT_TALK_P1 = [
        (["You ask what she'd be doing right now."],
         "Reshelving poetry magazines. The store sorts them by SIZE. Size! ...Sorry. It's a thing.", 1),
        (["You ask who wrote this."],
         "Not Matsu. Matsu asks first. Whoever this is didn't ask. That's how I can tell.", 1),
        (["You ask if she's okay."],
         "I-- nobody asks me that first. They ask Matsu, then me, so I've had time to think of an answer. I don't have one yet.", 1),
        (["You keep talking after the useful questions run out."],
         "Keep going. It doesn't have to be useful. I like hearing somebody who isn't reading from a page.", 0),
    ]
    TSB_ACT_TALK_P2 = [
        (["You ask what she wants."],
         "I want-- let me answer. Don't help! I want the bookstore. I want ~to be better~ --NO. I want the bookstore.", 1),
        (["You ask about the tin."],
         "It's for the pieces. Somebody has to keep them. If I keep them, they're not really gone, right? Right?", 1),
        (["You ask her to say something, any way she wants."],
         "Any way? Sorry-- sorry, I'm starting over-- that's the way. That's how I talk. It keeps cutting that out.", 1),
    ]

    # ITEM table: (key, name, heal, pages). One shelf, no restocks. Buffed
    # 2026-09-30 (user: the fight asks for skill, and the old 3-12 HP items
    # barely registered against 3-5 damage hits): every item now puts back
    # between a third of your HP and all of it, so an item is a real second
    # chance at a move you are still learning. Secondary effects stay small.
    # Item pages are the narrator too: a beat of ordinary life used as a
    # combat consumable, which is exactly as wrong as it sounds. The cold
    # status lines _do_item appends after them are the fight's own flat
    # readout -- leave those robotic; the contrast is the point.
    TSB_ITEMS = [
        ("ramune", "Matsuda's Soda", 14.0,
        ["You drink Matsuda's imported soda. It's warm from riding around in a bag all day."]),
        ("bento", "Cold Lunch", 20.0,
        ["You eat the cold lunch in four bites, standing up, in the middle of all this."]),
        ("handkerchief", "Clean Handkerchief", 10.0,
        ["A folded handkerchief. Ironed, because of course it would be."]),
        ("tape", "Sports Tape", 12.0,
        ["You wrap your bad wrist the way the club taught you."]),
        ("coin", "Washed Coin", 6.0,
        ["A heavy coin, cleaner than any coin has a right to be."]),
        ("candy", "Sour Candy", 10.0,
        ["You eat the sour candy. Your entire face reboots."]),
        ("tea", "Paper Cup of Tea", 14.0,
        ["You drink the paper cup of tea, somehow still warm. You don't ask how."]),
        ("cracker", "Rice Crackers", 8.0,
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
        "ramune": "+14 HP",
        "bento": "HP fully restored",
        "handkerchief": "+10 HP  /  softens one hit",
        "tape": "+12 HP  /  longer recovery after one hit",
        "coin": "+6 HP  /  +2 trust  /  softens one hit",
        "candy": "+10 HP  /  faster movement for two turns",
        "tea": "+14 HP  /  draws in more green needles",
        "cracker": "+8 HP  /  softens one hit",
    }
    # Item reactions are phase-aware. In phase 1 she identifies and sorts; in
    # phase 2 she asks the listener to supply the missing ownership or order.
    TSB_ITEM_BUBBLES = {
        "ramune": ("That's Matsu's. Orange label, back pocket of her bag. I put it on the inventory.",
                   "Matsu's, I think. If she says it isn't, believe her."),
        "bento": ("Food was third, after the arcade. You're early, but go ahead.",
                  "Is this the food stop? Tell me when it is and I'll eat too."),
        "handkerchief": ("The folded corner means that one's mine. Keep it. I have another.",
                         "Which fold means mine? You can choose. Just be consistent."),
        "tape": ("Left wrist. You keep landing on it, so wrap that one first.",
                 "Tell me which wrist hurts. I can't use your face to work it out right now."),
        "coin": ("I washed that before it went in my pencil case. Don't put it on the floor.",
                 "Heads bookstore, tails arcade. Catch it, but don't show me. Just tell me."),
        "candy": ("Matsu bought those for the train. She'll complain if you finish them, then buy more.",
                  "Sour means you like it, right? Make the face again so I know."),
        "tea": ("Careful. The lid never sits straight on those paper cups.",
                "It's warm. Is warm good here? Nod if it is."),
        "cracker": ("Those are mine. Matsu takes them without asking, which is different from losing them.",
                    "Matsu usually takes those. I think that means you can too."),
    }

    # Booth interjections (Matsuda, watching, unable to help). She contributes
    # facts Tsubaki is losing, but never in an analyst's voice: she is trying
    # to reach her friend through a dead channel and getting angrier each time
    # the room answers first.
    TSB_BOOTH = {
        "intro":   "MATSUDA: Tsuba! Look left--look at me! ...No. She always looks. Even when she's pissed at me, she looks.",
        "reuse":   "MATSUDA: The sword thing was a JOKE. She made it one herself! Tsuba, why does it get to decide it wasn't funny?!",
        "reuse2":  "MATSUDA: Don't answer for her! Give her one second. ONE. She takes a second and then she says the right thing. She always does!",
        "ramune":  "MATSUDA: That soda is mine because she bought it for me! She hates orange soda. Tsuba, you complained the whole walk home--remember?",
        "shift_v": "MATSUDA: She was DOWN! She was finally down and it-- Tsuba, that wasn't help! You didn't ask it to pull you back up!",
        "shift_p": "MATSUDA: Her hand moved first! Did you see that?! Tsuba, do it again. Reach for them again--please!",
        "death":   "MATSUDA: HEY! Answer me! I don't care what you say, just answer--please, please answer!",
        "limp":    "MATSUDA: STOP! Her eyes are closed! Tsuba watches everything--she isn't even looking anymore!",
        "limp2":   "MATSUDA: PUT YOUR HANDS DOWN! The room isn't making you choose FIGHT. That's you!",
        "end_v":   "MATSUDA: Tsuba? No--no, no, look left! Tsuba, LOOK AT ME!",
        "end_p":   "MATSUDA: They're down! I counted every one, so get up--Tsuba, they're DOWN! Why aren't you getting up?!",
        "end_b":   "MATSUDA: You waited until she trusted you. What did you DO?!",
        "card":    "MATSUDA: That's her handwriting. That's-- I'd know it anywhere. She never wrote that. She'd never write STAND HERE for herself!",
        "drift":   "MATSUDA: Your cursor's moving on its own. Don't let it! That's what it does to her!",
    }

    # Retry bubbles: like a notebook, she keeps count. The first lines of the
    # fight still end on her going first.
    TSB_RETRY_BUBBLES = [
        "You came back. I wrote down where it got you. I'm not going to show you. That'd be mean.",
        "Second time. It moved the part that got you. I noticed. I'm not supposed to notice.",
        "Third. You don't have to keep doing this. ...I'd like it if you did. Sorry. Forget I said that.",
        "You keep coming back. Nobody comes back for the second take. I don't know what to do with my hands.",
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

            # WHAT THE ROOM DOES TO THE SOUL. drag_x/drag_y are a shove added
            # AFTER the player's own input, re-asserted every tick; move_* is
            # the player's INPUT, kept separate so being shoved never reads
            # as disobeying a cyan/orange rule.
            self.drag_x = 0.0
            self.drag_y = 0.0
            self.move_vx = 0.0
            self.move_vy = 0.0
            self.move_amt = 0.0
            # The SOUL's mode (2026-09-29): "red" walks free, "blue" falls
            # under gravity and jumps on UP, "strung" rides her strings.
            self.soul = "red"
            self.soul_born = -999        # tick of the last mode change
            self.soul_vy = 0.0
            self.soul_ground = False
            self.string_k = 0            # which string the strung SOUL rides
            self.hop = None              # {"y0", "t0"} while hopping strings
            self.strings_on = []         # the strings a strung SOUL can ride
            self.arena_circle = None     # (cx, cy, r): a round room (the clock)
            self.rewinding = False       # the tape is running backward
            self.shards = []             # the broken SOUL, after a death
            self.hp_shown = TSB_HP_MAX   # the HUD bar's drain ghost
            # Her first move is owed until she takes it: the first button
            # press in the menu is interrupted (see _step_menu).
            self.opener_pending = True
            self.opener_go = None        # menu tick the opener starts on
            self.drift_next = None       # phase 2: the menu helps your hand
            self.shelter = None          # (x, y, r): her translation bubble
            self.trail = []              # the SOUL's recent path (noticing)
            self.hits_at_dodge = 0
            self.last_clean = False      # the last move never touched you

            # Boss / routes.
            self.boss_hp = TSB_BOSS_HP
            self.boss_hp_show_until = -999
            self.boss_hp_shown = TSB_BOSS_HP  # the drain the HP bar animates
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
            self.next_bubble = None      # action reply queued before turn line
            self.bubble_queue = []       # extra bubbles queued before the dodge
            self.bub_started = 0         # etalk mtick baseline for auto-advance
            self._bub_hold = 60          # hold reused for each queued bubble

            # Bullets & friends.
            self.bullets = []
            self.wires = []
            self.blooms = []
            # Large, authored set-piece geometry. Unlike bullets, these
            # primitives are rebuilt by the active pattern every tick, so
            # their visible shape and collision shape cannot drift apart.
            self.scene_props = []
            self.pattern_slot = 0
            self.pattern_cycle = 0
            self.pattern_hits = 0
            self.sparks = []
            self.dmg_pops = []
            self.pattern = None
            self.pat_t = 0
            self.pat_dur = 0
            self.pat_dens = 1.0
            self.pat_lead = 0
            self.pat_scratch = {}
            self.fading_out = False

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
                text = str(text)
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
                txt = TSB_BOOTH[key]
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

        # ----- IMPACT -------------------------------------------------------
        # The set-piece roster collides with authored geometry, never with
        # bodies, so it arrived with no reason to spawn anything -- and a
        # room where nothing is ever THROWN reads as a slideshow no matter
        # how sharp its timings are. These three put weight back on the
        # authored edges without putting a single new hazard in the box:
        # every body they spawn is armed a million ticks in the future, so
        # it is pure wreckage and the fairness contract is untouched.

        def _debris(self, x, y, n, kind="chip", ci=0, speed=2.6, ttl=80,
                    up=0.0, sq=3, aim=None, spread=6.28318, ay=0.0):
            r = self.rng
            for _i in range(n):
                if aim is None:
                    a = r.uniform(0.0, 6.28318)
                else:
                    a = aim + r.uniform(-0.5, 0.5) * spread
                sp = r.uniform(0.35, 1.0) * speed
                b = self._add_bullet(x + r.uniform(-7.0, 7.0),
                                     y + r.uniform(-7.0, 7.0),
                                     math.cos(a) * sp,
                                     math.sin(a) * sp - up,
                                     kind=kind, ci=ci, sq=sq, ay=ay,
                                     ttl=10 ** 6, armed_at=10 ** 6)
                if b is not None:
                    # `fz` is a lifetime that dims on its way out and does
                    # not stop the body moving, so wreckage settles instead
                    # of blinking off -- and it double-locks the collision
                    # check, which already refuses anything frozen. It also
                    # means the turn's fade-out sweeps debris up with
                    # everything else and _end_turn can never stall on it.
                    b["fz"] = max(6, int(ttl))

        def _slam(self, x, y, power=1.0, ci=0, kind="chip", sfx=None,
                  vol=0.9, flash=0.0, aim=None, spread=6.28318, shake=True):
            """One authored edge becoming real, given a body.

            Every set-piece used to announce its dangerous frame with a
            single sound cue and nothing else, which is why a roster that
            hits hard still felt inert. A live edge now costs the room
            something: sparks off the contact, grit thrown off it, and a
            kick in the frame scaled to how big the thing is.
            """
            p = max(0.15, float(power))
            self._spark_burst(x, y, int(5 + 13 * p), ci,
                              2.0 + 1.9 * p, int(24 + 18 * p), 0.5)
            self._debris(x, y, int(1 + 4 * p), kind=kind, ci=ci,
                         speed=1.7 + 1.7 * p, ttl=46 + 34 * p, sq=3,
                         aim=aim, spread=spread, ay=0.03)
            if shake:
                self.shake = max(self.shake, 4.0 + 12.0 * p)
            if flash > 0.0:
                self.flash = max(self.flash, flash)
            if sfx:
                tsb_play(sfx, vol)

        def _slam_line(self, x1, y1, x2, y2, power=1.0, ci=0, kind="chip",
                       n=4, sfx=None, vol=0.9, flash=0.0, aim=None):
            """A whole EDGE going live.

            A wall that closes across the entire room must not spark at one
            dot in the middle of itself; the impact is sampled along the
            contact line so the eye reads the edge, not a firework.
            """
            n = max(1, int(n))
            for i in range(n):
                u = (i + 0.5) / float(n)
                self._slam(x1 + (x2 - x1) * u, y1 + (y2 - y1) * u,
                           power * 0.62, ci=ci, kind=kind,
                           sfx=sfx if i == 0 else None, vol=vol,
                           flash=flash if i == 0 else 0.0, aim=aim,
                           spread=1.5 if aim is not None else 6.28318)

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
            # Both HP bars drain toward the truth instead of snapping to it.
            bhs = float(getattr(self, "boss_hp_shown", self.boss_hp))
            self.boss_hp_shown = bhs + (self.boss_hp - bhs) * 0.07
            hs = float(getattr(self, "hp_shown", self.hp))
            if hs > self.hp:
                hs = max(self.hp, hs - 0.25)
            else:
                hs = self.hp
            self.hp_shown = hs
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
                    self.strings_alpha = 0.72 if self.phase == 2 else 0.45
                    idx = min(max(self.visit_deaths, 1), len(TSB_RETRY_BUBBLES)) - 1
                    self._bub(TSB_RETRY_BUBBLES[idx], hold=80)
                if t > 40 and self._reveal_bubble() and (t > 220 or edges["z"]):
                    self.bubble = None
                    # Both entries reach the menu with her first move still
                    # owed; the first button press is hers (see _step_menu),
                    # which rewinds the cursor to -1 for the opener so that
                    # this turn-0 beat is the one that follows it.
                    self.turn = 0
                    self._menu_in()
                return
            if t == 30:
                self._bub("Oh. Hi. You came through Matsu's door.", hold=60)
            elif t == 170:
                self._bub("She told you she didn't write me one of these, right? She didn't. She always asks first.", hold=50)
            elif t == 320:
                # Something takes up the slack.
                self.strings_alpha = 0.35
                self.shake = 6
                tsb_play("wire", 0.5)
                self._bub("...Somebody else didn't.", hold=30)
            elif t == 430:
                # The genre arrives all at once -- and hands you the menu.
                self.room_live = True
                tsb_play("phase")
                tsb_play("wire")
                self.flash = 1.0
                self.strings_alpha = 0.45
                self.shake = 30
                self.box_alpha = 1.0
                self.hud_alpha = 1.0
                tsb_music_start()
                self._booth("intro")
                self.turn = 0
                self._menu_in()
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
            self.drift_next = None
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
            if getattr(self, "opener_pending", False):
                return TSB_FLAVOR_FIRST
            t = max(self.turn, 0)
            # Keep the command-box prose on the same wear contract as the
            # sprite: four cut strings can produce the limp pose even when a
            # pacifist route has not lowered HP.
            if self.phase == 2 and tsb_boss_asset_key(self) == "p2_limp":
                return TSB_FLAVOR_LIMP[t % len(TSB_FLAVOR_LIMP)]
            if self.hp <= 5.0:
                return TSB_FLAVOR_LOWHP
            # turns_taken is exactly 1 only at the first menu after the
            # overture (the retry intro skips the volley and arrives at 0).
            if self.phase == 1 and self.turns_taken == 1 and not self.retry:
                return TSB_FLAVOR_OVERTURE
            if (self.turns_taken > 1 and self.turns_taken % 3 == 0
                    and getattr(self, "last_clean", False)):
                return TSB_FLAVOR_NOTED[(self.turns_taken // 3) % len(TSB_FLAVOR_NOTED)]
            if self.phase == 2:
                # Every third phase-local turn, the room inserts its next
                # administrative revision into the same itinerary.
                if t % 3 == 2:
                    idx = min(t // 3, len(TSB_FLAVOR_ENGINE) - 1)
                    return TSB_FLAVOR_ENGINE[idx]
                pool = TSB_FLAVOR_P2
            else:
                pool = TSB_FLAVOR_P1
            return pool[t % len(pool)]

        def _step_menu(self, edges):
            n = int(self.mtick * 1.1)
            if n <= len(self.flavor or "") and self.mtick % 3 == 0:
                tsb_play("blip", 0.45)
            # ME FIRST. The menu comes up and the flavor says she is waiting
            # for you to go first; the first button you press is interrupted
            # and she takes the turn. (If you only wait, she goes anyway.)
            if self.opener_go is not None:
                self._reveal_bubble()
                if self.mtick >= self.opener_go:
                    self.opener_go = None
                    self.opener_pending = False
                    self.bubble = None
                    self.turn = -1
                    self._begin_dodge(("first", 600, 1.0))
                return
            if self.opener_pending:
                if edges["z"] or self.mtick >= 540:
                    if edges["z"]:
                        tsb_play("confirm")
                        self._bub("Actually-- no. Sorry. Me first.", hold=10)
                    else:
                        self._bub("You're taking a while. That's okay. I'll go first.", hold=10)
                    self.opener_go = self.mtick + (48 if edges["z"] else 76)
                    self.shake = max(self.shake, 8)
                    tsb_play("wire", 0.8)
                    return
            # PHASE 2, late: the menu starts helping your hand -- one step at
            # a time toward FIGHT. It is only ever a suggestion; Z is yours.
            if (self.phase == 2 and self.turn >= 9 and not self.boss_fallen
                    and self.boss_hp > TSB_LIMP_HP):
                if self.drift_next is None:
                    self.drift_next = self.mtick + 80
                elif self.mtick >= self.drift_next:
                    self.drift_next = self.mtick + 60
                    if self.menu_i != 0:
                        self.menu_i -= 1
                        tsb_play("move", 0.9)
                        tsb_play("wire", 0.3)
                        self._booth("drift")
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
                    self._say(["Your pockets are empty. The last item is already off the list."], after="menu")
                else:
                    self._submenu_in("item", [TSB_ITEMS[i][1] for i in self.items])
            elif b == "MERCY":
                self._submenu_in("mercy", self._mercy_options())

        def _act_options(self):
            if self.phase == 1:
                return ["CHECK", "TALK", "REACH OUT", "ASK HER FIRST"]
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
            # ACT replies stay compact because _begin_etalk queues the current
            # story beat behind them. CHECK's ATK 0 measures Tsubaki, not the
            # act already assembling the next volley.
            name = self.sub[i]
            self.sub = None
            if name == "CHECK":
                if self.phase == 1:
                    if not self.checked:
                        self.checked = True
                        self.next_bubble = "Zero? Good. I'd hate for any of this to be my fault. ...That came out wrong."
                        self._say(["TSUBAKI KAREDA  -  ATK 0  DEF 1", "Didn't write this. Is in it anyway."])
                    else:
                        self.next_bubble = "Still zero. You can stop checking. I'm not getting any scarier."
                        self._say(["The readout has not moved. ATK 0."])
                else:
                    if not self.checked2:
                        self.checked2 = True
                        self._mercy_add(1)
                        self.next_bubble = "Zero. You look relieved. Should I be relieved? Tell me what your face means. I can't read it through the revisions."
                        self._say(["TSUBAKI KAREDA  -  ATK 0  DEF 0", "FIVE THREADS.  TWO HANDWRITINGS."])
                    else:
                        self.next_bubble = "Same numbers. It keeps trying to raise them. It can't. That part's still me."
                        self._say(["ATK 0.  DEF 0.", "She looks at your face instead of the readout."])
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
                    self.next_bubble = "Sorry! Sorry-- I thought you were going to-- you just did, a second ago. Try again. Please try again."
                    self._say(["Her whole body snaps away before your hand reaches her shoulder."])
                else:
                    self.reach_n += 1
                    if self.reach_n == 1:
                        self._mercy_add(1)
                        self.next_bubble = "My shoulder dropped before you touched me. Did you see? The strings didn't do that. I did."
                    elif self.reach_n == 2:
                        self.next_bubble = "You're still there. Okay. Give me one more second. I'm not used to people staying for the second try."
                    else:
                        self.next_bubble = "I stopped bracing first. That was me. Matsu, that was me."
                    self.next_dodge_dens = min(self.next_dodge_dens, 0.88)
                    self._say(["You reach past the pattern with an open hand."])
            elif name == "ASK HER FIRST":
                self.name_n += 1
                if self.name_n == 1:
                    self._mercy_add(2)
                    self.next_bubble = "...Me? You're asking me? First? Nobody-- okay. Okay. The bookstore. I'd like to go to the bookstore."
                    self._say(["Before anything else, you ask her what she wants to do next."])
                elif self.name_n == 2:
                    self.next_bubble = "Twice. You asked twice. I'm writing that down. I'm writing down that somebody asked."
                    self._say(["You ask her first again."])
                else:
                    self.next_bubble = "Same answer. Bookstore. It's still my answer. Nobody changed it."
                    self._say(["You ask first."])
            elif name == "MATCH BREATHING":
                self.steady_n += 1
                # Her old rhythm keeps jamming the act no matter how often
                # you return to it -- the mercy loop leans on that.
                self._mercy_add(1)
                self.guard_charges = min(2, self.guard_charges + 1)
                if self.steady_n == 1:
                    self.next_bubble = "Four in. Six out. Count louder-- no, not louder. Quieter. It's so loud in here. Just don't stop."
                    self._say(["Four counts in. Six counts out."])
                elif self.steady_n == 2:
                    self.next_bubble = "I got to four first! Was I supposed to wait? I'm always waiting. Don't make me wait."
                    self._say(["You find the same rhythm again."])
                else:
                    self.next_bubble = "I lost count. It's too loud. Start over. Please. I'll follow the quiet one."
                    self._say(["In. Out. You count where she can hear it over the room."])
            elif name == "STAY":
                self.stay_n += 1
                if self.stay_n == 1:
                    self._mercy_add(2)
                    self.next_bubble = "You're staying. Nobody stays for the second draft. ...Stay for the bad one. Please. The bad one's me."
                    self._say(["You keep your feet where they are."])
                else:
                    self._mercy_add(1)
                    self.next_bubble = "Still here. Tell me before you leave. You have to tell me. Nobody tells me."
                    self._say(["You stay."])

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
                status.append("HP  /  MAX" if self.hp >= TSB_HP_MAX
                              else "HP  /  +%d" % int(gained))
            reactions = TSB_ITEM_BUBBLES.get(key)
            self.next_bubble = (reactions[1 if self.phase == 2 else 0]
                                if reactions is not None else None)
            self._say(list(pages) + status)

        def _do_mercy(self, i):
            name = self.sub[i]
            self.sub = None
            if name == "FLEE":
                self.flee_n += 1
                if self.flee_n == 1:
                    if self.phase == 1:
                        self.next_bubble = "If you find a door, take it. Don't wait for me. I'm used to being the one who stays."
                    else:
                        self.next_bubble = "The door? Wait. Was I supposed to follow you? I never know if I'm invited. Don't go yet."
                    self._say(["You look for the way you came in. There is no handle on this side."])
                elif self.phase == 2:
                    self.next_bubble = None
                    self._say(["Still no handle.", "She waits for you to say whether that means stay."])
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
                        self.next_bubble = "You're not fighting? Oh. I don't know what to do when people don't. Let me try something."
                    else:
                        self.next_bubble = None
                    self._say(["You lower your guard. One thread draws tight."])
                else:
                    self.spares += 1
                    if self.spares >= (1 if self.debug else TSB_SPARES_NEED):
                        self.pending = "shift_p"
                        self.next_bubble = None
                        self._say(["You lower your hands.", "Her right hand drops half an inch."],
                                    after="pending")
                    else:
                        self.next_bubble = ("The strings loosened when you did that. Do it again. I want to see if it's you or me."
                                            if self.spares == 1 else
                                            "Looser. Wait. I can move before it tells me to.")
                        self._say(["You lower your hands. Her wrists follow by a fraction."])
            else:
                if self.mercy2 < need2:
                    self.next_bubble = None
                    if self.spares2:
                        self._say(["MERCY  /  THREADS LOCKED",
                                    "TENSION RESET  /  BUILD MERCY AGAIN"])
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
                        # Every cut removes one physical instruction. Her
                        # reaction follows the released limb and the same lost
                        # itinerary instead of turning into a thematic speech.
                        replies = [
                            "My hand came down. It's heavier than I remember. That's what my hand weighs. Huh.",
                            "Both hands. I could carry something now. I could carry my own bag.",
                            "My shoulder dropped. That's where I keep all the flinching. It fell right out.",
                            "I can turn my head. I can look where I want. I'm looking at you. Is that okay? I'm asking first.",
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
                self._pop(TSB_BOSS_X, TSB_BOSS_FEET_Y - 236, "MISS", 7, True)
                self.next_bubble = None
                if self.phase == 2:
                    self._say(["You swing through the space the strings just vacated."])
                else:
                    self._say(["The slash passes under one lifted shoe. She follows it with her eyes."])

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
            action_line = self.next_bubble
            self.next_bubble = None
            story_line = self._turn_bubble()

            # An action reaction is an interruption, not a replacement. Queue
            # the phase-local story beat behind it so FIGHT, ACT, ITEM and
            # MERCY all advance one continuous conversation.
            seq = []
            if isinstance(action_line, (list, tuple)):
                seq.extend(action_line)
            elif action_line is not None:
                seq.append(action_line)
            if isinstance(story_line, (list, tuple)):
                seq.extend(story_line)
            elif story_line is not None:
                seq.append(story_line)

            # Mode first so the bubble's auto-advance baseline (bub_started)
            # is measured from a fresh mtick of 0.
            self._set_mode("etalk")
            self._bub(seq if len(seq) > 1 else (seq[0] if seq else None), hold=70)

        def _turn_bubble(self):
            t = max(self.turn, 0)
            if self.phase == 1:
                if t < len(TSB_BUBBLES_P1):
                    pair = TSB_BUBBLES_P1[t]
                else:
                    pair = TSB_LOOP_P1[(t - len(TSB_BUBBLES_P1))
                                       % len(TSB_LOOP_P1)]
                return pair[1] if self.fought_last else pair[0]

            if t == 0:
                pair = TSB_BUBBLES_P2_OPEN.get(
                    self.route, TSB_BUBBLES_P2_OPEN["p"])
            else:
                idx = t - 1
                if idx < len(TSB_BUBBLES_P2):
                    pair = TSB_BUBBLES_P2[idx]
                else:
                    pair = TSB_LOOP_P2[(idx - len(TSB_BUBBLES_P2))
                                       % len(TSB_LOOP_P2)]
            wear = tsb_boss_asset_key(self)
            lean = (self.fought_last
                    or wear in ("p2_exhausted", "p2_limp"))
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
            "first":      (640.0, 152.0),  # the menu box itself (TSB_MENU_W x H)
            "translation": (430.0, 262.0),
            "claw":       (400.0, 262.0),
            "noticing":   (420.0, 262.0),
            "apology":    (430.0, 262.0),
            "tin":        (420.0, 262.0),
            "shelves":    (430.0, 264.0),
            "sword":      (440.0, 270.0),
            "list":       (420.0, 258.0),
            "arcade":     (400.0, 250.0),
            "bags":       (420.0, 258.0),
            "clock":      (264.0, 264.0),
            "crowd":      (430.0, 252.0),
            "lunch":      (420.0, 258.0),
            "strung":     (400.0, 270.0),
            "itinerary":  (430.0, 262.0),
            "revision":   (430.0, 264.0),
            "limp":       (300.0, 240.0),
        }

        # A count-in, per move: extra ticks before its first event, added to
        # the move's duration so nobody loses a rep for it. The rebuilt roster
        # opens every move off the SOUL, so none needs one; the hook stays.
        LEAD_IN = {}

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
            # Fixed authored order: the attack underneath a line belongs to
            # that line. Long pacifist loops replay the same readable score;
            # they do not silently accelerate or reshuffle its meaning.
            table = TSB_TURNS_P1 if self.phase == 1 else TSB_TURNS_P2
            idx = max(0, self.turn) % len(table)
            self.pattern_slot = idx
            self.pattern_cycle = max(0, self.turn) // len(table)
            return table[idx]

        def _begin_dodge(self, forced=None):
            pid, dur, dens = forced if forced is not None else self._turn_entry()
            # Matsuda catches the wrong voice early, then names what the thing
            # has actually done to her once the second half is underway.
            if forced is None:
                if self.phase == 1 and self.turn == 1:
                    self._booth("reuse")
                elif self.phase == 1 and self.turn == 9:
                    self._booth("card")
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
            # Every move starts with a red SOUL in a square, unstrung room
            # and has to ask for anything else itself.
            self.drag_x = 0.0
            self.drag_y = 0.0
            self.scene_props = []
            self._set_soul("red", quiet=True)
            self.strings_on = []
            self.arena_circle = None
            self.rewinding = False
            self.shelter = None
            self.trail = []
            self.hits_at_dodge = self.pattern_hits
            w, h = TSBGame.DODGE_BOX.get(pid, (TSB_DODGE_W, TSB_DODGE_H))
            self.box_target = [TSB_BOX_CX, TSB_BOX_CY, w, h]
            self.px = TSB_BOX_CX
            self.py = TSB_BOX_CY
            self._set_mode("dodge")
            if pid == "first":
                # The flavor line you were reading becomes the first attack
                # on the very frame the menu goes away.
                self.py = TSB_BOX_CY + 30
                self._first_letters()

        def _step_dodge(self, edges):
            held = edges["held"]
            self.pat_t += 1
            # Set-piece geometry is a frame description. Rebuilding it here
            # keeps collision and rendering on the same authoritative data.
            self.scene_props = []
            self._move_soul(edges, held)
            self.trail.append((self.px, self.py))
            if len(self.trail) > 420:
                del self.trail[0]

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
                    self._step_scene_props()
            elif not self.fading_out:
                self.fading_out = True
                for b in self.bullets:
                    b["fz"] = 18
                self.blooms = []
                self._kill_wires()
                # The room's instructions end with the move that gave them:
                # the SOUL goes back to red, the strings and the round room go.
                self.scene_props = []
                self._set_soul("red")
                self.strings_on = []
                self.arena_circle = None
                self.rewinding = False
                self.shelter = None

            self._step_bullets()

            if self.fading_out and not self.bullets and not self.wires:
                self._end_turn()

        # ----- the SOUL -----------------------------------------------------------
        # Three modes, all Undertale's, each one asked for by a move that means
        # something by it:
        #   red     walks free (and, in the clock, inside a round room).
        #   blue    the arcade's: gravity, UP to jump; let go early for a hop.
        #   strung  hers: the SOUL rides one of the strings across the room --
        #           left/right slides along it, up/down hops to the next.
        # drag_x/drag_y are a per-tick shove added AFTER the player's input, and
        # move_amt is the player's INPUT, so a cyan/orange rule reads intent
        # rather than whatever else moved the SOUL.

        SOUL_GRAV_UP = 0.30
        SOUL_GRAV_DOWN = 0.40
        SOUL_JUMP = 6.4
        SOUL_JUMP_CUT = 2.0
        SOUL_HOP_TICKS = 7

        def _set_soul(self, mode, quiet=False):
            if mode == getattr(self, "soul", "red"):
                return
            self.soul = mode
            self.soul_vy = 0.0
            self.soul_ground = False
            self.hop = None
            if not quiet:
                self.soul_born = self.tick
                tsb_play("soul", 0.9)
                self._spark_burst(self.px, self.py, 12,
                                  {"blue": 9, "strung": 5}.get(mode, 0), 2.4, 26)
            if mode == "strung" and self.strings_on:
                self.string_k = min(range(len(self.strings_on)),
                                    key=lambda k: abs(self.strings_on[k]["base"] - self.py))
                self.hop = {"y0": self.py, "t0": self.tick}

        def _string_y(self, s, x):
            bx, by, bw, bh = self._arena()
            u = tsb_clamp((x - bx) / max(1.0, bw), 0.0, 1.0)
            return s["y0"] + (s["y1"] - s["y0"]) * u

        def _hop_to(self, k):
            if k == self.string_k and self.hop is None:
                return
            self.hop = {"y0": self.py, "t0": self.tick}
            self.string_k = k

        def _move_soul(self, edges, held):
            dx = (1.0 if held["right"] else 0.0) - (1.0 if held["left"] else 0.0)
            dy = (1.0 if held["down"] else 0.0) - (1.0 if held["up"] else 0.0)
            spd = TSB_MOVE_SLOW if self.slow else TSB_MOVE
            if self.quick_turns > 0:
                spd *= 1.16
            bx, by, bw, bh = self._box_rect()
            pad = TSB_PLAYER_R + TSB_BORDER
            soul = getattr(self, "soul", "red")
            if soul == "blue":
                # Gravity. UP jumps from the floor; letting go of UP early cuts
                # the rise short, so a short hop and a long one are both yours.
                floor = by + bh - pad
                if held["up"] and self.soul_ground:
                    self.soul_vy = -TSBGame.SOUL_JUMP
                    self.soul_ground = False
                if not held["up"] and self.soul_vy < -TSBGame.SOUL_JUMP_CUT:
                    self.soul_vy = -TSBGame.SOUL_JUMP_CUT
                self.soul_vy += (TSBGame.SOUL_GRAV_UP if self.soul_vy < 0.0
                                 else TSBGame.SOUL_GRAV_DOWN)
                self.soul_vy = min(self.soul_vy, 7.5)
                self.move_vx, self.move_vy = dx, 0.0
                # In the air counts as moving: a cyan shot will not forgive a
                # jump, exactly as Undertale's does not.
                self.move_amt = abs(dx) * spd + (0.0 if self.soul_ground else 1.0)
                self.px = tsb_clamp(self.px + dx * spd + self.drag_x,
                                    bx + pad, bx + bw - pad)
                self.py += self.soul_vy
                if self.py >= floor:
                    self.py = floor
                    self.soul_vy = 0.0
                    self.soul_ground = True
                else:
                    self.soul_ground = False
                    if self.py <= by + pad:
                        self.py = by + pad
                        self.soul_vy = max(0.0, self.soul_vy)
            elif soul == "strung" and self.strings_on:
                strings = self.strings_on
                alive = [k for k, s in enumerate(strings) if s.get("alive", True)]
                if alive:
                    if self.string_k not in alive:
                        # The string under you went: drop to the next one down.
                        base = strings[min(self.string_k, len(strings) - 1)]["base"]
                        below = [k for k in alive if strings[k]["base"] > base]
                        self._hop_to(below[0] if below else alive[-1])
                    elif self.hop is None and (edges["up"] or edges["down"]):
                        i = alive.index(self.string_k)
                        j = i + (-1 if edges["up"] else 1)
                        if 0 <= j < len(alive):
                            self._hop_to(alive[j])
                            tsb_play("move", 0.5)
                self.move_vx, self.move_vy = dx, 0.0
                self.move_amt = abs(dx) * spd
                self.px = tsb_clamp(self.px + dx * spd + self.drag_x,
                                    bx + pad, bx + bw - pad)
                ty = self._string_y(strings[min(self.string_k, len(strings) - 1)],
                                    self.px)
                if self.hop is not None:
                    u = (self.tick - self.hop["t0"]) / float(TSBGame.SOUL_HOP_TICKS)
                    if u >= 1.0:
                        self.hop = None
                        self.py = ty
                    else:
                        e = u * u * (3.0 - 2.0 * u)
                        self.py = (self.hop["y0"] + (ty - self.hop["y0"]) * e
                                   - math.sin(u * math.pi) * 5.0)
                        self.move_amt += 1.0
                else:
                    self.py = ty
            else:
                if dx != 0.0 and dy != 0.0:
                    dx *= 0.70710678
                    dy *= 0.70710678
                # Record what the PLAYER asked for before anything is done to
                # the SOUL, so being shoved never reads as disobeying a rule.
                self.move_vx = dx
                self.move_vy = dy
                self.move_amt = math.hypot(dx, dy) * spd
                self.px = tsb_clamp(self.px + dx * spd + self.drag_x,
                                    bx + pad, bx + bw - pad)
                self.py = tsb_clamp(self.py + dy * spd + self.drag_y,
                                    by + pad, by + bh - pad)
                circ = getattr(self, "arena_circle", None)
                if circ is not None:
                    ccx, ccy, cr = circ
                    ddx, ddy = self.px - ccx, self.py - ccy
                    d = math.hypot(ddx, ddy)
                    lim = cr - TSB_PLAYER_R
                    if d > lim > 0.0:
                        self.px = ccx + ddx / d * lim
                        self.py = ccy + ddy / d * lim
            # Drag is re-asserted by whatever is pulling on every tick it
            # pulls, so it expires the instant that thing lets go.
            self.drag_x = 0.0
            self.drag_y = 0.0

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
            self.last_clean = self.pattern_hits == self.hits_at_dodge
            self._menu_in()

        # ----- bullets ----------------------------------------------------------
        # bullet: x/y/vx/vy, kind, ci, sq, rb/ra (tumble), sway/ph, ay, curve,
        #         age, fz (fade-out: harmless while it dims), heal, ttl,
        #         armed_at, and `rule` -- None, "cyan" (hurts a MOVING SOUL) or
        #         "orange" (hurts a STILL one).
        # Behaviours are optional keys the roster sets on the body it spawned:
        #   land    {"do": bloom/open/fizz/crack} when it reaches the boards
        #   bounce  {"n", "rest"} floor bounces before it lands
        #   walls   bounces off the side walls
        #   stick   ticks it stays stuck where it hits a wall
        #   slide   {"ty", "left"} walks to a new height at a bounded speed
        #   dash    {"at", "stop", "vx"} stops dead, shivers, then runs
        #   on_string  rides string k of a strung room
        #   jit / flicker  cosmetic: a shiver; a rule about to change
        # wire:   orient "h"/"v" plus pos, or "d" plus two endpoints; every
        #         damaging line has the same telegraph -> live -> gone cadence.

        # Hit radii stay UNDER the drawn body -- what you see is bigger than
        # what cuts you. `needle` is the mend, and its radius is generous on
        # purpose because catching it is the reward.
        BULLET_R = {"petal": 4.5, "camellia": 10.0, "needle": 14.0,
                    "book_r": 6.5, "book_b": 6.5, "book_g": 6.5,
                    "book_y": 6.5, "book_n": 6.5, "book_v": 6.5,
                    "book_open": 6.5, "page": 5.0, "glyph": 7.0, "pen": 3.5,
                    "can": 6.0, "drop": 3.5, "coin": 6.0, "critter": 8.0,
                    "commuter": 8.0, "bell": 6.0, "rice": 3.5,
                    "cracker": 7.0, "crumb": 3.0, "chip": 3.0, "spark": 3.0,
                    "tag": 7.0, "bird": 7.0}
        BULLET_DMG = {"petal": 3.0, "camellia": 5.0, "needle": 0.0,
                      "book_r": 4.0, "book_b": 4.0, "book_g": 4.0,
                      "book_y": 4.0, "book_n": 4.0, "book_v": 4.0,
                      "book_open": 4.0, "page": 3.0, "glyph": 3.0, "pen": 4.0,
                      "can": 4.0, "drop": 3.0, "coin": 3.0, "critter": 4.0,
                      "commuter": 4.0, "bell": 3.0, "rice": 3.0,
                      "cracker": 4.0, "crumb": 2.0, "chip": 2.0, "spark": 2.0,
                      "tag": 3.0, "bird": 3.0}
        # Long bodies collide as capsules: ("head", half) runs along the
        # flight (or where it stuck), ("v", half) stands upright.
        BULLET_CAP = {"pen": ("head", 12.0), "commuter": ("v", 11.0),
                      "tag": ("h", 26.0)}

        def _add_bullet(self, x, y, vx, vy, kind="petal", ci=0, sq=4, ay=0.0,
                        sway=0.0, heal=False, ttl=1200, curve=0.0, armed_at=0,
                        rule=None):
            if len(self.bullets) >= TSB_MAX_BULLETS:
                return None
            rb = self.rng.randint(0, TSB_ROT_BUCKETS - 1)
            b = {"x": x, "y": y, "vx": vx, "vy": vy, "kind": kind, "ci": ci,
                "sq": sq, "rb": rb, "ra": rb * TSB_ROT_DEG,
                "rs": self.rng.choice([-1, 1]) * self.rng.uniform(0.6, 1.6),
                "sway": sway, "ph": self.rng.uniform(0, 6.28), "ay": ay,
                "curve": curve, "rule": rule,
                "armed_at": max(0, int(armed_at)),
                "age": 0, "fz": 0, "heal": heal, "ttl": ttl}
            self.bullets.append(b)
            return b

        def _add_aimed(self, x, y, tx, ty, speed, **kwargs):
            a = math.atan2(ty - y, tx - x)
            return self._add_bullet(x, y, math.cos(a) * speed,
                                    math.sin(a) * speed, **kwargs)

        # Axis wires: a line across the whole box, telegraphed pale.
        def _add_wire(self, orient, pos, ci=5, tel=38, on=24, vol=0.8):
            # vol scales the pluck cue; 0 silences it so simultaneous wires
            # sound once instead of stacking copies.
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

        # ----- authored set-piece geometry ---------------------------------
        # Props are rebuilt by the active pattern every tick, so what is drawn
        # and what collides cannot drift apart. `ghost` props are drawn and
        # never collide; `hidden` props collide and are never drawn -- the
        # hazard is a sprite (a sword, a clock hand), the prop is its blade.
        # Cyan and orange use Undertale's movement rules.

        def _scene_rect(self, x, y, w, h, ci=2, harm=False, ghost=False,
                        rule=None, label=None, alpha=1.0, outline=False,
                        hidden=False):
            self.scene_props.append({"shape": "rect", "x": float(x),
                "y": float(y), "w": max(0.0, float(w)),
                "h": max(0.0, float(h)), "ci": int(ci),
                "harm": bool(harm), "ghost": bool(ghost), "rule": rule,
                "label": label, "alpha": float(alpha),
                "outline": bool(outline), "hidden": bool(hidden)})

        def _scene_circle(self, x, y, r, ci=2, harm=False, ghost=False,
                          rule=None, label=None, alpha=1.0, outline=False,
                          hidden=False):
            self.scene_props.append({"shape": "circle", "x": float(x),
                "y": float(y), "r": max(0.0, float(r)), "ci": int(ci),
                "harm": bool(harm), "ghost": bool(ghost), "rule": rule,
                "label": label, "alpha": float(alpha),
                "outline": bool(outline), "hidden": bool(hidden)})

        def _scene_line(self, x1, y1, x2, y2, width=8.0, ci=2,
                        harm=False, ghost=False, rule=None, alpha=1.0,
                        hidden=False):
            self.scene_props.append({"shape": "line", "x1": float(x1),
                "y1": float(y1), "x2": float(x2), "y2": float(y2),
                "width": max(1.0, float(width)), "ci": int(ci),
                "harm": bool(harm), "ghost": bool(ghost), "rule": rule,
                "alpha": float(alpha), "hidden": bool(hidden)})

        def _scene_sprite(self, key, x, y, rot=0.0, alpha=1.0, sc=2,
                          flip=False, tint=None):
            # Scenery drawn from the atlas. Always a ghost: anything a sprite
            # can hurt you with is a hidden prop laid over it.
            self.scene_props.append({"shape": "sprite", "key": str(key),
                "x": float(x), "y": float(y), "rot": float(rot),
                "alpha": float(alpha), "sc": int(sc), "flip": bool(flip),
                "tint": tint, "ghost": True, "harm": False})

        def _scene_text(self, text, x, y, ci=2, sc=2, alpha=1.0):
            # Words written in the room, top-left anchored, in Kareda Mono.
            self.scene_props.append({"shape": "text", "text": str(text),
                "x": float(x), "y": float(y), "ci": int(ci), "sc": int(sc),
                "alpha": float(alpha), "ghost": True, "harm": False})

        def _scene_ellipse(self, x, y, rx, ry, ci=0, alpha=0.4):
            # A shadow on the boards: where something is going to land.
            self.scene_props.append({"shape": "ellipse", "x": float(x),
                "y": float(y), "rx": max(1.0, float(rx)),
                "ry": max(1.0, float(ry)), "ci": int(ci),
                "alpha": float(alpha), "ghost": True, "harm": False})

        def _scene_ring(self, x, y, r, width=6.0, ci=4, rule=None, loud=False,
                        ghost=False, alpha=1.0):
            # An expanding wave: it is the band |d - r| < width / 2 that cuts.
            self.scene_props.append({"shape": "ring", "x": float(x),
                "y": float(y), "r": max(0.0, float(r)),
                "width": max(1.0, float(width)), "ci": int(ci),
                "harm": not ghost, "ghost": bool(ghost), "rule": rule,
                "loud": bool(loud), "alpha": float(alpha)})

        def _scene_bubble(self, x, y, r, text="", alpha=1.0):
            # Tsubaki's small speech bubble (her translation), with the
            # quiet version of whatever was just shouted written inside.
            self.scene_props.append({"shape": "bubble", "x": float(x),
                "y": float(y), "r": float(r), "text": str(text),
                "alpha": float(alpha), "ghost": True, "harm": False})

        def _sheltered(self):
            sh = getattr(self, "shelter", None)
            if sh is None:
                return False
            return math.hypot(self.px - sh[0], self.py - sh[1]) <= sh[2] - TSB_PLAYER_R

        def _scene_rule_live(self, prop):
            if not prop.get("harm") or prop.get("ghost"):
                return False
            if prop.get("loud") and self._sheltered():
                return False
            rule = prop.get("rule")
            if rule == "cyan":
                return self.move_amt > 0.05
            if rule == "orange":
                return self.move_amt <= 0.05
            return True

        def _step_scene_props(self):
            if self.mode != "dodge" or self.tick < self.inv_until:
                return
            hurt = 0.0
            for prop in self.scene_props:
                if not self._scene_rule_live(prop):
                    continue
                shape = prop.get("shape")
                hit = False
                if shape == "rect":
                    hit = (prop["x"] - TSB_PLAYER_R <= self.px <=
                           prop["x"] + prop["w"] + TSB_PLAYER_R and
                           prop["y"] - TSB_PLAYER_R <= self.py <=
                           prop["y"] + prop["h"] + TSB_PLAYER_R)
                elif shape == "circle":
                    rr = prop["r"] + TSB_PLAYER_R
                    hit = ((self.px - prop["x"]) ** 2 +
                           (self.py - prop["y"]) ** 2 <= rr * rr)
                elif shape == "ring":
                    d = math.hypot(self.px - prop["x"], self.py - prop["y"])
                    hit = abs(d - prop["r"]) <= prop["width"] * 0.5 + TSB_PLAYER_R
                elif shape == "line":
                    x1, y1 = prop["x1"], prop["y1"]
                    dx = prop["x2"] - x1
                    dy = prop["y2"] - y1
                    seg2 = dx * dx + dy * dy
                    if seg2 > 0.0001:
                        u = tsb_clamp(((self.px - x1) * dx +
                                      (self.py - y1) * dy) / seg2, 0.0, 1.0)
                        qx, qy = x1 + dx * u, y1 + dy * u
                        rr = prop["width"] * 0.5 + TSB_PLAYER_R
                        hit = ((self.px - qx) ** 2 +
                               (self.py - qy) ** 2 <= rr * rr)
                if hit:
                    hurt = max(hurt, float(prop.get("dmg", 4.0)))
            if hurt:
                self._take_hit(hurt)

        def _land(self, b, floor_y, spawn, sfx):
            """What a body does when it reaches the boards. Returns False if
            the body itself is used up."""
            do = (b.get("land") or {}).get("do")
            x = b["x"]
            if do == "bloom":
                # A whole flower hits the boards and bursts into a full ring.
                spec = b["land"]
                n = int(spec.get("n", 12))
                base = self.rng.uniform(0.0, 6.28318)
                for i in range(n):
                    a = base + 6.28318 * i / n
                    spawn.append((x, floor_y - 4.0,
                                  math.cos(a) * spec.get("speed", 1.5),
                                  math.sin(a) * spec.get("speed", 1.5),
                                  spec.get("kind", "petal"), {}))
                self._spark_burst(x, floor_y, 10, 0, 2.4, 26)
                sfx.add("bloom")
                return False
            if do == "open":
                # A dropped book flops open and its pages skid both ways.
                for sgn in (-1.0, 1.0):
                    spawn.append((x + sgn * 6.0, floor_y - 2.0, sgn * 1.7,
                                  0.0, "page", {"ttl": 90}))
                b["kind"] = "book_open"
                b["y"] = floor_y
                b["vx"] = b["vy"] = b["ay"] = 0.0
                b["land"] = None
                b["fz"] = 26
                sfx.add("bounce")
                return True
            if do == "fizz":
                # The can hits, and a fan of soda sprays straight up.
                for i in range(5):
                    a = -math.pi * 0.5 + (i - 2) * 0.36
                    spawn.append((x, floor_y - 6.0, math.cos(a) * 2.9,
                                  math.sin(a) * 2.9, "drop",
                                  {"ay": 0.12, "ttl": 90}))
                b["vx"] = b["vy"] = b["ay"] = 0.0
                b["y"] = floor_y
                b["land"] = None
                b["fz"] = 22
                sfx.add("fizz")
                return True
            if do == "tag":
                # A piece of her lands and becomes its label, then goes to
                # the tin: sliding along the boards, or leaping there.
                spec = b["land"]
                ax, ay_, aw, ah = self._arena()
                tx = ax + aw * 0.5
                if spec.get("leap"):
                    ticks = 44.0
                    g = 0.2
                    vy = ((floor_y - 18.0) - (floor_y - 6.0) - 0.5 * g * ticks * ticks) / ticks
                    spawn.append((x, floor_y - 6.0, (tx - x) / ticks, vy, "tag",
                                  {"ay": g, "ttl": 200, "label": spec.get("label", "")}))
                else:
                    spawn.append((x, floor_y - 4.0, 1.7 if x < tx else -1.7, 0.0,
                                  "tag", {"ttl": 320, "label": spec.get("label", "")}))
                self._spark_burst(x, floor_y, 8, 0, 2.0, 24)
                sfx.add("bounce")
                return False
            if do == "crack":
                for i in range(5):
                    a = -math.pi * 0.5 + (i - 2) * 0.42
                    s = 2.2 + 0.25 * abs(i - 2)
                    spawn.append((x, floor_y - 4.0, math.cos(a) * s,
                                  math.sin(a) * s, "crumb",
                                  {"ay": 0.12, "ttl": 80}))
                self._spark_burst(x, floor_y, 5, 4, 1.6, 20)
                sfx.add("crack")
                return False
            # Nothing to do: it settles where it fell and fades.
            b["vx"] = b["vy"] = b["ay"] = 0.0
            b["y"] = floor_y
            b["fz"] = 24
            return True

        def _step_bullets(self):
            bx, by, bw, bh = self._box_rect()
            margin = 60.0
            kept = []
            spawn = []
            sfx = set()
            hurt = 0.0
            heal_hit = False
            live = self.mode == "dodge"
            still = self.move_amt <= 0.05
            strings = getattr(self, "strings_on", None) or []
            sheltered = self._sheltered()
            for b in self.bullets:
                # HOLD: the world stops for this body, and its clock stops
                # with it. Nothing on hold can collide.
                if b.get("hold", 0) > 0:
                    b["hold"] -= 1
                    kept.append(b)
                    continue
                b["age"] += 1
                if b["fz"]:
                    b["fz"] -= 1
                    if b["fz"] <= 0:
                        continue
                elif b["ttl"] - b["age"] == 10:
                    # Everything leaves by fading, never by blinking out.
                    b["fz"] = 10
                kind = b["kind"]
                r = TSBGame.BULLET_R.get(kind, 4.0)
                if kind == "glyph":
                    r = 2.4 * b.get("sc", 3)
                floor_y = by + bh - TSB_BORDER - r

                dash = b.get("dash")
                if dash is not None:
                    k = b["age"] - dash["at"]
                    if k == 0:
                        b["vx"] = 0.0
                        b["jit"] = 2
                        sfx.add("glint")
                    elif k == dash["stop"]:
                        b["vx"] = dash["vx"]
                        b["jit"] = 0
                        b["dash"] = None

                slide = b.get("slide")
                if slide is not None:
                    left = max(1, int(slide["left"]))
                    b["y"] += (slide["ty"] - b["y"]) / float(left)
                    slide["left"] = left - 1
                    if slide["left"] <= 0:
                        b["y"] = slide["ty"]
                        b["slide"] = None

                if not b.get("stuck"):
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

                sk = b.get("on_string")
                if sk is not None and 0 <= sk < len(strings):
                    s = strings[sk]
                    if s.get("alive", True):
                        b["y"] = self._string_y(s, b["x"])
                    else:
                        # Its string was cut: it falls.
                        b["on_string"] = None
                        b["ay"] = 0.18

                if b.get("walls") and not b["fz"]:
                    lw = bx + TSB_BORDER + r
                    rw = bx + bw - TSB_BORDER - r
                    if (b["x"] < lw and b["vx"] < 0) or (b["x"] > rw and b["vx"] > 0):
                        b["vx"] = -b["vx"]
                        b["x"] = tsb_clamp(b["x"], lw, rw)
                        sfx.add("bounce")

                stick = b.get("stick")
                if stick and not b.get("stuck") and not b["fz"]:
                    lw, rw = bx + TSB_BORDER, bx + bw - TSB_BORDER
                    tw, fw = by + TSB_BORDER, by + bh - TSB_BORDER
                    if not (lw <= b["x"] <= rw and tw <= b["y"] <= fw):
                        # Buried to the hilt in the wall it hit.
                        sp = max(0.001, math.hypot(b["vx"], b["vy"]))
                        b["dir"] = (b["vx"] / sp, b["vy"] / sp)
                        b["x"] = tsb_clamp(b["x"], lw, rw)
                        b["y"] = tsb_clamp(b["y"], tw, fw)
                        b["vx"] = b["vy"] = b["ay"] = 0.0
                        b["stuck"] = True
                        b["ttl"] = b["age"] + int(stick)
                        sfx.add("stick")

                if (b.get("land") is not None or b.get("bounce")) and not b["fz"]:
                    if b["y"] >= floor_y and b["vy"] > 0.0:
                        bounce = b.get("bounce")
                        if bounce and bounce.get("n", 0) > 0:
                            bounce["n"] -= 1
                            b["y"] = floor_y
                            b["vy"] = -abs(b["vy"]) * float(bounce.get("rest", 0.5))
                            sfx.add("coin" if kind == "coin" else "bounce")
                        elif not self._land(b, floor_y, spawn, sfx):
                            continue

                b["ra"] = (b.get("ra", b["rb"] * TSB_ROT_DEG) + b["rs"] * 6.0) % 360.0
                b["rb"] = int(b["ra"] / TSB_ROT_DEG) % TSB_ROT_BUCKETS
                if b["age"] > b["ttl"]:
                    continue
                if (b["x"] < bx - margin or b["x"] > bx + bw + margin
                        or b["y"] < by - margin or b["y"] > by + bh + margin):
                    if b["age"] > 20:
                        continue
                # Collision only while a live pattern is running.
                if (live and not b["fz"]
                        and b["age"] >= b.get("armed_at", 0)):
                    rule = b.get("rule")
                    if b.get("loud") and sheltered:
                        pass
                    elif rule is None or (rule == "cyan" and not still) or (
                            rule == "orange" and still):
                        dx = self.px - b["x"]
                        dy = self.py - b["y"]
                        cap = TSBGame.BULLET_CAP.get(kind)
                        if cap is not None:
                            if cap[0] == "v":
                                ux, uy = 0.0, 1.0
                            elif cap[0] == "h":
                                ux, uy = 1.0, 0.0
                            else:
                                hx, hy = b.get("dir") or (b["vx"], b["vy"])
                                hn = max(0.001, math.hypot(hx, hy))
                                ux, uy = hx / hn, hy / hn
                            along = tsb_clamp(dx * ux + dy * uy, -cap[1], cap[1])
                            dx -= ux * along
                            dy -= uy * along
                        rr = r + TSB_PLAYER_R
                        if dx * dx + dy * dy <= rr * rr:
                            if b["heal"]:
                                heal_hit = True
                                self._spark_burst(b["x"], b["y"], 8, 3, 2.4, 30)
                                continue
                            if self.tick >= self.inv_until:
                                hurt = max(hurt, TSBGame.BULLET_DMG.get(kind, 3.0))
                kept.append(b)
            self.bullets = kept
            for (x, y, vx, vy, kind, extra) in spawn:
                nb = self._add_bullet(x, y, vx, vy, kind=kind,
                                      ay=extra.get("ay", 0.0),
                                      ttl=extra.get("ttl", 200))
                if nb is not None and extra.get("label"):
                    nb["label"] = extra["label"]
            # One cue per kind per tick, however many bodies shared the beat.
            if live:
                for name in sfx:
                    tsb_play(name, 0.7)

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
                if (live and not w["killed"]
                        and w["tel"] <= age <= w["tel"] + w["on"]
                        and self.tick >= self.inv_until):
                    if w["orient"] == "h":
                        if abs(self.py - w["pos"]) <= 5.0 + TSB_PLAYER_R:
                            hurt = max(hurt, 4.0)
                    elif w["orient"] == "v":
                        if abs(self.px - w["pos"]) <= 5.0 + TSB_PLAYER_R:
                            hurt = max(hurt, 4.0)
                    else:
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
                                hurt = max(hurt, 4.0)
                wkept.append(w)
            self.wires = wkept

            # Blooms: a telegraphed point bursts into a FULL ring.
            bkept = []
            for bl in self.blooms:
                if self.tick - bl["born"] >= bl["fuse"]:
                    tsb_play("bloom")
                    self._spark_burst(bl["x"], bl["y"], 9, bl["ci"], 2.4, 26)
                    n = bl["n"]
                    for i in range(n):
                        a = ((6.28318 / n) * i + bl.get("spin", 0.0))
                        self._add_bullet(bl["x"], bl["y"],
                                        math.cos(a) * bl["speed"],
                                        math.sin(a) * bl["speed"],
                                        kind="petal")
                else:
                    bkept.append(bl)
            self.blooms = bkept

            if heal_hit:
                self.hp = min(TSB_HP_MAX, self.hp + TSB_HEAL_HP)
                self.pat_scratch["healed_at"] = self.tick
                tsb_play("heal", 0.9)
                self._pop(self.px, self.py - 16, "+%d" % int(TSB_HEAL_HP), 3)
            if hurt:
                self._take_hit(hurt)

        def _take_hit(self, dmg):
            if self.mode == "dodge":
                self.pattern_hits += 1
            if self.guard_charges > 0:
                self.guard_charges -= 1
                dmg = max(1.0, math.ceil(dmg * 0.5))
                self._pop(self.px, self.py - 22, "GUARD", 9)
            self.hp = max(0.0, self.hp - dmg)
            self.inv_until = self.tick + TSB_INV_TICKS + self.invuln_bonus
            self.invuln_bonus = 0
            self.shake = max(self.shake, 7)
            tsb_play("hurt")
            self._spark_burst(self.px, self.py, 10, 0, 3.0, 32)
            if self.hp <= 0.0:
                # UT/DR: the music does not fade. It stops.
                tsb_music_stop(0.0)
                self.heart_break = self.tick
                self.shards = []
                tsb_play("break")
                self._set_mode("dead")

        def _dodge_common(self, t):
            # There is intentionally no universal HAZARD layer. What IS
            # universal is the weather: the eye needs something small and
            # quick in frame to believe the room is running, so dust always
            # climbs through the box -- ghost geometry, the word this fight
            # taught for "cannot touch you" in its first seconds. It is
            # computed straight off the clock (no list, nothing to leak
            # between moves), each mote on its own rate and phase so the
            # field never pulses in unison, which would read as an attack.
            bx, by, bw, bh = self._box_rect()
            p2 = self.phase == 2
            # The violence collapse earns its silence by contrast.
            if self.pattern == "limp":
                if t % 47 == 0:
                    self._spark_burst(
                        bx + 18.0 + self.rng.random() * (bw - 36.0),
                        by + 8.0, 1, 7, 0.7, 70, -0.5)
                return
            motes = 12 if p2 else 8
            rise = 0.85 if p2 else 0.44
            span = bh + 52.0
            tint = "#a01824" if p2 else "#8a90a0"
            for i in range(motes):
                h = (i * 2654435761 + 17) % 1000003
                sx = (h % 997) / 997.0
                sp = 0.55 + ((h // 997) % 89) / 89.0 * 0.9
                ph = ((h // 91) % 628) / 100.0
                u = ((t * rise * sp + h % 617) % span) / span
                mx = (bx + 14.0 + (bw - 28.0) * sx
                      + math.sin(t * 0.014 + ph) * (16.0 if p2 else 10.0))
                my = by + bh + 22.0 - span * u
                fade = min(1.0, min(u, 1.0 - u) * 6.0)
                if fade <= 0.05:
                    continue
                self._scene_sprite("spark_s" if h % 3 else "crumb:w", mx, my,
                                   sc=2, tint=tint,
                                   alpha=(0.5 if p2 else 0.4) * fade)
            # And in the second half the room is actively shedding: grit off
            # the ceiling on an off-beat that belongs to no set-piece.
            if p2 and t % 23 == 0:
                self._spark_burst(bx + 18.0 + self.rng.random() * (bw - 36.0),
                                  by + 6.0, 3, 6, 1.1, 46, -0.9)

        # =====================================================================
        # THE ROSTER  (rebuilt from zero 2026-09-29)
        # =====================================================================
        # Every attack is made of one stop on her itinerary -- the used
        # bookstore, the inflatable sword at the magazine tables, the list she
        # clipped in blue, the arcade, the two mixed-up bags, the station
        # clock, the card that said STAND HERE, lunch -- and asks the player
        # for one Undertale / Deltarune verb: read the wall, get out of the
        # arc, go where the line is short, JUMP (the arcade turns the SOUL
        # blue), keep moving through orange, stand still through cyan, meet
        # beneath the hand, follow the card, ride the strings (phase two ties
        # the SOUL to them). The attack is the object doing what it does.
        #
        # PHASE 1 is the day as she planned it: every stop in order, each move
        # repeating a readable rhythm the player can learn. PHASE 2 is the same
        # objects losing their order -- gaps that slide mid-flight, a sword
        # that bounces back, hands that run backward, crowds that change their
        # minds, bags that come to you, a room that rewinds and revises -- and
        # two moves of its own, `strung` and `revision`. Erratic is never
        # blind: every change is announced before it lands.
        #
        # THE FAIRNESS CONTRACT (inherited, and still the law):
        #   * Rings burst whole; circles never carry authored doors. The only
        #     lanes are gaps in full-height WALLS (book columns, crowds, text
        #     lines), which UT's own bone walls use -- and moving windows.
        #   * A wall's lane is at least 46px of centre travel for a 12px SOUL.
        #   * Anything aimed commits to a STALE position sampled at telegraph
        #     time, and every telegraph is visible AND audible.
        #   * A lane that moves never moves faster than 2.4 px/tick; the SOUL
        #     walks at 3.7.
        #   * Randomness is spent at telegraph time, never on a body in flight.
        #   * Nothing lands on the SOUL on a move's first beat.
        # Collision is bodies (bullets) and authored geometry (hidden props);
        # everything drawn only is a ghost. Healing needles are green, always.

        BOOK_KINDS = ("book_r", "book_b", "book_g", "book_y", "book_n", "book_v")

        # ----- shared building blocks -----------------------------------------

        def _arena(self):
            # The box the move ASKED for. Patterns lay out against the target
            # rect, not the easing one, so geometry never drifts with the lerp.
            cx, cy, w, h = self.box_target
            return (cx - w * 0.5, cy - h * 0.5, w, h)

        def _floor_y(self):
            bx, by, bw, bh = self._arena()
            return by + bh - TSB_PLAYER_R - TSB_BORDER

        def _needle(self, x, y, vx, vy=0.0, ttl=280):
            # Her mending: a green needle, generous to catch. Always green.
            # The paper cup of tea (needle_turns) draws a second one in
            # behind it, a little lower.
            tsb_play("mend", 0.8)
            self._spark_burst(x, y, 6, 3, 1.6, 26)
            b = self._add_bullet(x, y, vx, vy, kind="needle", heal=True,
                                 ttl=ttl)
            if self.needle_turns > 0:
                bx, by, bw, bh = self._arena()
                self._add_bullet(x - vx * 22.0, tsb_clamp(y + 34.0, by + 16,
                                 by + bh - 16), vx, vy, kind="needle",
                                 heal=True, ttl=ttl)
            return b

        def _ease(self, u):
            u = tsb_clamp(float(u), 0.0, 1.0)
            return u * u * (3.0 - 2.0 * u)

        # Book walls ---------------------------------------------------------
        def _book_rows(self):
            # The stack runs from 16px under the ceiling to 16px over the
            # floor, so the top and bottom books reach the walls: a SOUL
            # pressed against either wall is still inside the column, and the
            # only way through is the lane.
            bx, by, bw, bh = self._arena()
            top, bot = by + 16.0, by + bh - 16.0
            n = int(round((bot - top) / 17.8)) + 1
            pitch = (bot - top) / float(n - 1)
            return [top + pitch * k for k in range(n)]

        def _book_pitch(self):
            rows = self._book_rows()
            return rows[1] - rows[0]

        def _book_kind(self, k, x):
            return TSBGame.BOOK_KINDS[(k * 5 + int(abs(x)) // 7) % 6]

        def _book_column(self, x, vx, gap, gap_n=3, tag=None, rule=None):
            # A column of books shoved off a shelf, with one missing run of
            # gap_n books: the lane. Books sit ~17.8px apart with a 6.5px
            # hit radius, so a column is solid (a 5px chink, and the SOUL is
            # 12px wide); three missing books leave 46px of centre travel.
            out = []
            for k, y in enumerate(self._book_rows()):
                if gap <= k < gap + gap_n:
                    continue
                b = self._add_bullet(x, y, vx, 0.0, kind=self._book_kind(k, x),
                                     ttl=420, rule=rule)
                if b is not None:
                    b["tag"] = tag
                    b["row"] = k
                    b["gap"] = gap
                    out.append(b)
            return out

        def _book_telegraph(self, x, gap, u, gap_n=3, ci=8):
            # The books about to be shoved peek out of the shelf, brightening
            # with u (0..1), and the empty run is bracketed in yellow.
            rows = self._book_rows()
            pitch = rows[1] - rows[0]
            for k, y in enumerate(rows):
                if gap <= k < gap + gap_n:
                    continue
                self._scene_sprite(self._book_kind(k, x), x, y,
                                   alpha=0.18 + 0.52 * u)
            if 0 <= gap < len(rows):
                top = rows[gap] - pitch * 0.5
                self._scene_rect(x - 18, top, 36, pitch * gap_n, ci=ci,
                                 ghost=True, alpha=0.30 + 0.45 * u, outline=True)

        def _slide_gap(self, tag, new_gap, ticks, gap_n=3):
            # Re-stack a live column so its lane moves to new_gap. Every book
            # walks to its new slot, and the whole shuffle takes long enough
            # that the LANE never travels faster than 2.25 px/tick.
            rows = self._book_rows()
            pitch = rows[1] - rows[0]
            books = sorted([b for b in self.bullets if b.get("tag") == tag],
                           key=lambda b: b["y"])
            if not books:
                return
            old_gap = books[0].get("gap", new_gap)
            ticks = max(int(ticks), int(abs(new_gap - old_gap) * pitch / 2.25) + 1)
            slots = [k for k in range(len(rows))
                     if not (new_gap <= k < new_gap + gap_n)]
            for b, k in zip(books, slots):
                b["slide"] = {"ty": rows[k], "left": ticks}
                b["gap"] = new_gap
            tsb_play("glint", 0.7)

        # Text walls (the list) ------------------------------------------------
        def _text_line(self, text, x0, y, rule=None, tag=None, armed=0, sc=3):
            # One written line of the list: every non-space glyph is a body.
            # Glyphs sit 18px apart at 3x with a 7px radius, so a word is
            # solid; the lane is where the line ENDS.
            out = []
            adv = 6.0 * sc
            for i, ch in enumerate(text):
                if ch == " ":
                    continue
                b = self._add_bullet(x0 + adv * i + 2.5 * sc, y, 0.0, 0.0,
                                     kind="glyph", ttl=900, rule=rule,
                                     armed_at=armed)
                if b is not None:
                    b["ch"] = ch
                    b["sc"] = sc
                    b["tag"] = tag
                    b["col"] = i
                    b["hold"] = 0
                    out.append(b)
            return out

        def _tag_set(self, tag, **fields):
            for b in self.bullets:
                if b.get("tag") == tag:
                    b.update(fields)

        # Crowd walls (the station) --------------------------------------------
        def _crowd_rows(self):
            # Five commuters from wall to wall. A commuter collides as an
            # upright capsule (+-11, radius 8), so neighbours ~48px apart
            # leave a chink the 12px SOUL cannot fit, and one missing person
            # opens 47px of centre travel.
            bx, by, bw, bh = self._arena()
            n = 5
            pitch = (bh - 58.0) / (n - 1)
            return [by + 29.0 + pitch * k for k in range(n)]

        def _crowd_column(self, x, vx, lane=None, rule=None, tag=None):
            out = []
            for k, y in enumerate(self._crowd_rows()):
                if lane is not None and k == lane:
                    continue
                b = self._add_bullet(x, y, vx, 0.0, kind="commuter",
                                     ttl=460, rule=rule)
                if b is not None:
                    b["tag"] = tag
                    b["row"] = k
                    out.append(b)
            return out

        # Aimed lobs -------------------------------------------------------------
        def _lob(self, x0, y0, tx, ty, ticks, g, kind, **kw):
            # A parabola that lands exactly on (tx, ty) after `ticks`.
            ticks = max(1.0, float(ticks))
            vx = (tx - x0) / ticks
            vy = (ty - y0 - 0.5 * g * ticks * ticks) / ticks
            return self._add_bullet(x0, y0, vx, vy, kind=kind, ay=g, **kw)

        # ======================================================================
        # SHELVES -- "USED BOOKS"  (the bookstore: read the wall)
        # ======================================================================
        # Two bookcases stand at the walls and shove whole columns of books
        # across the room, one missing run of three per column -- that run is
        # the lane. Opposite columns cross, and in phase 1 their lanes always
        # share a row, so even standing where they meet is survivable. Books
        # also fall from the top where you WERE, flop open on the boards and
        # skid their pages along the floor. The finale shoves both cases at
        # once.
        # PHASE 2 -- "out of order": columns come from both sides and faster,
        # their lanes no longer line up, and a column marked with TWO brackets
        # (its lane now, and a blinking one where the lane is going) shuffles
        # its books just after it leaves the shelf -- the lane walks at most
        # four books, never faster than 2.25 px/tick, and has finished moving
        # before the column is a third of the way across the room.

        def _pat_shelves(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            floor = self._floor_y()
            p2 = self.phase == 2
            sc = self.pat_scratch
            rows = self._book_rows()
            n_rows = len(rows)
            lean = math.sin(t * 0.05) * 2.0 if p2 else 0.0
            self._scene_sprite("shelf", bx + 18, cy, alpha=0.95, rot=lean)
            self._scene_sprite("shelf", bx + bw - 18, cy, alpha=0.95,
                               flip=True, rot=-lean)
            if p2:
                sched = [(30, "L", 2, 6), (80, "R", 9, None), (130, "L", 6, 2),
                         (180, "R", 3, 7), (230, "L", 8, None), (262, "R", 1, 5),
                         (306, "L", 4, None), (306, "R", 9, None)]
            else:
                sched = [(40, "L", 4, None), (110, "R", 5, None),
                         (180, "L", 7, None), (250, "R", 6, None),
                         (330, "L", 4, None), (330, "R", 4, None)]
            tel = 40
            for si, (launch, side, gap, slide_to) in enumerate(sched):
                gap = min(gap, n_rows - 3)
                x0 = bx + 38 if side == "L" else bx + bw - 38
                spd = (2.2 if slide_to is not None else 2.7) if p2 else 2.3
                vx = spd if side == "L" else -spd
                tag = "col%d" % si
                if launch - tel <= t < launch:
                    u = (t - launch + tel) / float(tel)
                    self._book_telegraph(x0, gap, u)
                    if slide_to is not None and (t // 5) % 2 == 0:
                        dest = min(slide_to, n_rows - 3)
                        pitch = rows[1] - rows[0]
                        self._scene_rect(x0 - 14, rows[dest] - pitch * 0.5,
                                         28, pitch * 3, ci=8, ghost=True,
                                         alpha=0.30 + 0.4 * u, outline=True)
                    if t == launch - tel:
                        tsb_play("glint", 0.55)
                if t == launch:
                    self._book_column(x0, vx, gap, tag=tag)
                    tsb_play("volley", 0.75)
                    self._slam_line(x0, by + 10, x0, by + bh - 10, 0.55, 7,
                                    "page", 3, None)
                if slide_to is not None:
                    dest = min(slide_to, n_rows - 3)
                    at = launch + 10
                    if at <= t < at + 36:
                        # Where the lane is going, riding the column.
                        books = [b for b in self.bullets if b.get("tag") == tag]
                        if books:
                            pitch = rows[1] - rows[0]
                            self._scene_rect(books[0]["x"] - 18,
                                             rows[dest] - pitch * 0.5,
                                             36, pitch * 3, ci=8, ghost=True,
                                             alpha=0.62, outline=True)
                    if t == at:
                        self._slide_gap(tag, dest, 24)
            # The finale crash: both cases' columns meet in the middle.
            if not p2 and t == 330 + int((bw * 0.5 - 38) / 2.3):
                self._slam(cx, cy, 1.3, 7, "page", "snap", 0.8, flash=0.12)
            # Falling books, dropped where you stood.
            drop_every = 58 if p2 else 82
            first = 70
            if t >= first and (t - first) % drop_every == 0 and t < 360:
                n_drop = 2 if p2 else 1
                picks = []
                for j in range(n_drop):
                    picks.append(tsb_clamp(self.px + (j * 2 - (n_drop - 1)) * 70.0,
                                           bx + 64, bx + bw - 64))
                sc.setdefault("drops", []).append((t, tuple(picks)))
                tsb_play("glint", 0.6)
            for entry in list(sc.get("drops", [])):
                t0, picks = entry
                age = t - t0
                for tx in picks:
                    if age < 34:
                        u = age / 34.0
                        self._scene_sprite("book_y", tx, by + 10,
                                           alpha=0.3 + 0.6 * u)
                        self._scene_ellipse(tx, floor + 5, 10 + 8 * u, 4, 0,
                                            alpha=0.18 + 0.32 * u)
                    if age == 34:
                        b = self._add_bullet(tx, by + 10, 0.0, 2.0,
                                             kind="book_y", ay=0.18, ttl=160)
                        if b is not None:
                            b["land"] = {"do": "open"}
                if age > 40:
                    sc["drops"].remove(entry)
            if t == (200 if p2 else 236):
                self._needle(bx - 10, rows[5] if n_rows > 5 else cy, 1.3)

        # ======================================================================
        # SWORD -- "THE INFLATABLE SWORD"  (the magazine tables: get out of it)
        # ======================================================================
        # The inflatable sword from the magazine tables, the size of the room.
        # It SWINGS through a pale arc drawn a second ahead (be outside it),
        # SLAMS where you were and bounces into a second slam (step aside,
        # twice), THRUSTS in from the walls at your old height (duck the
        # line), and ends SPINNING in the middle (get to the edges -- its
        # reach stops short of every wall). Where a slam lands, a red bruise
        # sits on the boards for a moment. Magazine pages flutter down.
        # PHASE 2 -- "the bruise": swings bounce off the far wall and come
        # back through the same arc, slams chain three deep with offsets
        # chosen at telegraph time, thrusts come from either wall at a
        # sharper cadence, and the spin reverses once. Bruises linger.

        SWORD_LEN = 240.0            # the sprite at 2x, handle to tip
        SWORD_BLADE0 = 56.0          # handle + guard: harmless
        SWORD_HALF_W = 7.0           # the blade is 18px thick; it cuts at 14

        def _sword(self, px_, py_, ang, live, alpha=1.0):
            # The sprite points RIGHT from its handle; its centre sits half a
            # length along the heading. The blade is the only hazard.
            ca, sa = math.cos(ang), math.sin(ang)
            L = TSBGame.SWORD_LEN
            self._scene_sprite("sword", px_ + ca * L * 0.5, py_ + sa * L * 0.5,
                               rot=math.degrees(ang), alpha=alpha)
            if live:
                b0 = TSBGame.SWORD_BLADE0
                self._scene_line(px_ + ca * b0, py_ + sa * b0,
                                 px_ + ca * (L - 6), py_ + sa * (L - 6),
                                 TSBGame.SWORD_HALF_W * 2.0, 1, harm=True,
                                 hidden=True)

        def _arc_ghost(self, px_, py_, a0, a1, ci=1, alpha=0.3):
            L = TSBGame.SWORD_LEN
            steps = 8
            for i in range(steps + 1):
                a = a0 + (a1 - a0) * i / float(steps)
                self._scene_line(px_ + math.cos(a) * TSBGame.SWORD_BLADE0,
                                 py_ + math.sin(a) * TSBGame.SWORD_BLADE0,
                                 px_ + math.cos(a) * L, py_ + math.sin(a) * L,
                                 3, ci, ghost=True, alpha=alpha)

        def _pat_sword(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            floor = self._floor_y()
            p2 = self.phase == 2
            sc = self.pat_scratch
            L = TSBGame.SWORD_LEN
            # Pages from the magazine tables, slow and swaying.
            if t % (22 if p2 else 30) == 5 and t < 380:
                x = bx + 30 + ((t * 67) % int(bw - 60))
                self._add_bullet(x, by - 8, 0.0, 0.85, kind="page", sway=1.2,
                                 ttl=400)
            # Bruises: where a slam landed, the boards stay sore a moment.
            life = 80 if p2 else 50
            for entry in list(sc.get("bruises", [])):
                bt, bxx = entry
                age = t - bt
                if age < life:
                    self._scene_ellipse(bxx, floor + 3, 16, 5, 0,
                                        alpha=0.75 * (1.0 - age / float(life)))
                    self._scene_circle(bxx, floor, 9, ci=0, harm=True,
                                       hidden=True)
                else:
                    sc["bruises"].remove(entry)

            # ---- SWINGS: up from a floor corner, down through a pale arc --------
            # Held upright against the wall it stands by, it leans back,
            # then comes down like a door slamming: the quarter-disc drawn a
            # second ahead is exactly what it sweeps.
            swings = [(20, "L", -math.pi * 0.5, -0.06),
                      (100, "R", -math.pi * 0.5, -math.pi + 0.06)]
            for (s0, side, a0, a1) in swings:
                piv_x = bx + 14 if side == "L" else bx + bw - 14
                piv_y = by + bh + 14
                tel, sw = 44, 16
                back = 26 if p2 else 0
                lean = -0.14 if side == "L" else 0.14
                if s0 <= t < s0 + tel:
                    u = (t - s0) / float(tel)
                    # the wind-up: it leans back past its start, shivering
                    self._sword(piv_x, piv_y, a0 + lean * u
                                + math.sin(t * 0.9) * 0.02, False, alpha=0.9)
                    self._arc_ghost(piv_x, piv_y, a0, a1, alpha=0.25 + 0.35 * u)
                    if t == s0:
                        tsb_play("glint", 0.8)
                elif s0 + tel <= t < s0 + tel + sw:
                    u = self._ease((t - s0 - tel) / float(sw))
                    self._sword(piv_x, piv_y, a0 + (a1 - a0) * u, True)
                    if t == s0 + tel:
                        tsb_play("slash", 0.8)
                elif s0 + tel + sw <= t < s0 + tel + sw + max(back, 12):
                    k = t - s0 - tel - sw
                    if k < back:
                        # PHASE 2: it hits the far wall and comes back through
                        # the arc it just drew.
                        u = self._ease(k / float(back))
                        self._sword(piv_x, piv_y, a1 + (a0 - a1) * u * 0.9, True)
                        if k == 0:
                            self._slam(piv_x + math.cos(a1) * 200,
                                       piv_y + math.sin(a1) * 200, 0.8, 1,
                                       "spark", "wire", 0.6)
                    else:
                        self._sword(piv_x, piv_y, a1, False,
                                    alpha=0.6 * (1.0 - k / 12.0))

            # ---- SLAMS: stale-aimed, bouncing into the next -------------------
            if t == 176:
                n = 3 if p2 else 2
                xs = [tsb_clamp(self.px, bx + 40, bx + bw - 40)]
                for i in range(1, n):
                    if p2:
                        step = self.rng.choice((-1, 1)) * self.rng.uniform(56, 88)
                    else:
                        step = 70.0 if xs[-1] < cx else -70.0
                    xs.append(tsb_clamp(xs[-1] + step, bx + 40, bx + bw - 40))
                sc["slams"] = xs
            period = 40
            slams = sc.get("slams") or ()
            for i, sx in enumerate(slams):
                s0 = 176 + i * period
                tel = 34 if i == 0 else 22
                early = 0 if i == 0 else 18
                raised = by - 150.0
                landed = floor + 6.0 - L
                if s0 - early <= t < s0 + tel:
                    u = tsb_clamp((t - s0 + early) / float(tel + early), 0.0, 1.0)
                    self._scene_rect(sx - 16, by + 4, 32, bh - 8, ci=1,
                                     ghost=True, alpha=0.10 + 0.14 * u)
                    self._scene_rect(sx - 16, by + 4, 32, bh - 8, ci=1,
                                     ghost=True, alpha=0.3 + 0.4 * u,
                                     outline=True)
                if s0 <= t < s0 + tel:
                    lift = 60.0 * (1.0 - (t - s0) / float(tel)) if i else 0.0
                    self._sword(sx, raised - lift, math.pi * 0.5, False, alpha=0.9)
                elif s0 + tel <= t < s0 + tel + 8:
                    k = t - s0 - tel
                    top = raised + (landed - raised) * self._ease(k / 7.0)
                    self._sword(sx, top, math.pi * 0.5, True)
                    if k == 6:
                        self._slam(sx, floor, 1.2, 1, "crumb", "fall", 0.7)
                        sc.setdefault("bruises", []).append((t, sx))
                elif s0 + tel + 8 <= t < s0 + tel + 18:
                    # the bounce back up, harmless
                    k = t - s0 - tel - 8
                    self._sword(sx, landed - 40.0 * self._ease(k / 10.0),
                                math.pi * 0.5, False, alpha=0.5)

            # ---- THRUSTS from the walls at your old height -------------------
            th0 = 300 if p2 else 280
            th_every = 26 if p2 else 34
            for i in range(3):
                s0 = th0 + i * th_every
                if t == s0:
                    side = (self.rng.choice(("L", "R")) if p2 else
                            ("R" if i % 2 == 0 else "L"))
                    sc["thrust_%d" % i] = (side, tsb_clamp(self.py, by + 24,
                                                           by + bh - 24))
                    tsb_play("glint", 0.7)
                spec = sc.get("thrust_%d" % i)
                if spec is None:
                    continue
                side, ty = spec
                tel = 28
                if s0 <= t < s0 + tel:
                    u = (t - s0) / float(tel)
                    self._scene_rect(bx + 4, ty - 14, bw - 8, 28, ci=1,
                                     ghost=True, alpha=0.1 + 0.2 * u)
                    peek = 30 * u
                    if side == "R":
                        self._sword(bx + bw + 20 - peek, ty, math.pi, False)
                    else:
                        self._sword(bx - 20 + peek, ty, 0.0, False)
                elif s0 + tel <= t < s0 + tel + 18:
                    k = t - s0 - tel
                    if k < 12:
                        reach = (bw - 70) * self._ease(min(1.0, k / 6.0))
                    else:
                        reach = (bw - 70) * (1.0 - self._ease((k - 12) / 6.0))
                    if side == "R":
                        self._sword(bx + bw - 10 - reach, ty, math.pi, k < 14)
                    else:
                        self._sword(bx + 10 + reach, ty, 0.0, k < 14)
                    if k == 2:
                        tsb_play("slash", 0.7)

            # ---- SPIN finale: get to the far ends ------------------------------
            # The blade spans the centre, so everything within 127px of it is
            # swept; the ring drawn a second ahead is exactly that line, and
            # both short ends of the room lie outside it.
            sp0 = 386 if p2 else 380
            spin_tel = 56
            half = L * 0.5
            if sp0 - spin_tel <= t < sp0:
                u = (t - sp0 + spin_tel) / float(spin_tel)
                ang = t * 0.05
                self._scene_circle(cx, cy, 127, ci=1, ghost=True,
                                   alpha=0.1 + 0.3 * u, outline=True)
                self._sword(cx - math.cos(ang) * half, cy - math.sin(ang) * half,
                            ang, False, alpha=0.8)
                if t == sp0 - spin_tel:
                    tsb_play("glint", 0.9)
                sc["spin_a"] = ang
            elif sp0 <= t < sp0 + 60:
                k = t - sp0
                direction = -1.0 if (p2 and k >= 30) else 1.0
                ang = sc.get("spin_a", 0.0) + direction * 0.105
                sc["spin_a"] = ang
                self._sword(cx - math.cos(ang) * half, cy - math.sin(ang) * half,
                            ang, True)
                if k == 0:
                    tsb_play("wire", 0.8)
                if p2 and k == 30:
                    tsb_play("snap", 0.7)
                    self._spark_burst(cx, cy, 16, 1, 3.0, 30)
            elif sp0 + 60 <= t < sp0 + 76:
                ang = sc.get("spin_a", 0.0)
                self._sword(cx - math.cos(ang) * half, cy - math.sin(ang) * half,
                            ang, False, alpha=1.0 - (t - sp0 - 60) / 16.0)
            if t == (150 if p2 else 164):
                self._needle(bx + bw + 10, floor - 30, -1.2)

        # ======================================================================
        # LIST -- "THE LIST, CLIPPED IN BLUE"  (go where the line is short)
        # ======================================================================
        # She writes the list line by line at the top of the page -- the pen
        # draws each letter, the letters are harmless while wet -- and then
        # the line drops down the page as a wall. Lines alternate left- and
        # right-aligned, so the lane is wherever the line is SHORT. Then
        # Matsu's addition arrives in orange -- GLORY -- a full-width line
        # you can only pass by moving through it, and Tsubaki crosses it out,
        # twice. The blue clip closes the page on your column, twice.
        # PHASE 2 -- "the second stop": line 2 is a row of blanks; halfway
        # down, its letters SLIDE across to the other margin (the lane moves),
        # and the numbers stay pinned down the left margin the whole time.
        # PHASE 2 LATE -- "strike": she keeps striking lines out; a struck
        # line's letters fall apart, but BOOKSTORE refuses and stays whole.

        def _pat_list(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            p2 = self.phase == 2
            late = p2 and self.pattern_slot >= 13
            sc = self.pat_scratch
            # The page: faint ruled lines.
            for k in range(1, 6):
                yy = by + bh * k / 6.0
                self._scene_line(bx + 8, yy, bx + bw - 8, yy, 2, 9, ghost=True,
                                 alpha=0.30)
            self._scene_line(bx + 40, by + 4, bx + 40, by + bh - 4, 2, 0,
                             ghost=True, alpha=0.40)
            adv = 18.0
            if not p2:
                lines = [("1.BOOKSTORE", "L", None), ("2.ARCADE", "R", None),
                         ("GLORY!GLORY!GLORY!GLORY!", "F", "orange"),
                         ("3.FOOD", "L", None), ("BOOKSTORE", "R", None)]
            elif not late:
                lines = [("1.BOOKSTORE", "L", None), ("2.______", "L", "blank"),
                         ("3.FOOD", "R", None), ("2.?", "C", None)]
            else:
                lines = [("1.BOOKSTORE", "L", "keep"), ("2.ARCADE", "R", "strike"),
                         ("3.FOOD", "L", "strike"), ("BOOKSTORE!", "R", "keep")]
            write_at = 10
            per = 76 if not p2 else 70
            vy = 1.30 if not p2 else 1.45
            for li, (text, align, note) in enumerate(lines):
                w0 = write_at + li * per
                n = len(text)
                if align == "L":
                    x0 = bx + 12
                elif align == "R":
                    x0 = bx + bw - 12 - adv * n
                elif align == "C":
                    x0 = cx - adv * n * 0.5
                else:   # full width: repeat to fill
                    x0 = bx + 6
                y_line = by + 16
                write_ticks = min(40, n * 2)
                tag = "line%d" % li
                if w0 <= t < w0 + write_ticks:
                    k = int((t - w0) / 2.0) + 1
                    shown = text[:k]
                    self._scene_text(shown, x0, y_line - 13, 8 if note != "orange" else 4,
                                     sc=3, alpha=0.55)
                    self._scene_sprite("pen", x0 + adv * min(k, n) + 10, y_line - 16,
                                       rot=120, alpha=0.95)
                    if (t - w0) % 4 == 0:
                        tsb_play("blip", 0.45)
                if t == w0 + write_ticks:
                    rule = "orange" if note == "orange" else None
                    self._text_line(text, x0, y_line, rule=rule, tag=tag)
                    self._tag_set(tag, vy=vy)
                    tsb_play("volley", 0.6)
                    if note == "orange":
                        tsb_play("wire", 0.5)
                # PHASE 2: the blank line's letters walk to the other margin.
                if note == "blank":
                    at = w0 + write_ticks + 70
                    if at - 24 <= t < at:
                        self._tag_set(tag, jit=2)
                    if t == at:
                        # The lane walks with it, so it walks no faster than
                        # 2.3 px/tick.
                        shift = (bx + bw - 12 - adv * n) - x0
                        ticks = max(60, int(abs(shift) / 2.3) + 1)
                        self._tag_set(tag, vx=shift / float(ticks), jit=0)
                        sc["blank_stop"] = t + ticks
                        tsb_play("glint", 0.7)
                    if t == sc.get("blank_stop"):
                        self._tag_set(tag, vx=0.0)
                # The orange line is struck out after it has passed you.
                if note == "orange":
                    st = w0 + write_ticks + 120
                    for rep in range(2):
                        if st + rep * 12 <= t < st + rep * 12 + 10:
                            books = [b for b in self.bullets if b.get("tag") == tag]
                            if books:
                                yy = books[0]["y"] + (rep * 6 - 3)
                                u = (t - st - rep * 12) / 10.0
                                self._scene_line(bx + 6, yy, bx + 6 + (bw - 12) * u, yy,
                                                 5, 0, ghost=True, alpha=0.9)
                        if t == st + rep * 12 + 10:
                            tsb_play("slash", 0.5)
                    if t == st + 34:
                        for b in self.bullets:
                            if b.get("tag") == tag:
                                b["rule"] = None
                                b["armed_at"] = 10 ** 6
                                b["fz"] = 40
                                b["vx"] = self.rng.uniform(-1.0, 1.0)
                                b["ay"] = 0.12
            # PHASE 2: the numbers stay -- pinned down the left margin.
            if p2 and not late and t == 6:
                for k, ch in enumerate("123"):
                    b = self._add_bullet(bx + 16, by + 40 + k * 78, 0.0, 0.0,
                                         kind="glyph", ttl=420)
                    if b is not None:
                        b["ch"] = ch
                        b["sc"] = 3
            # PHASE 2 LATE: strike wires across the page at your old height;
            # a struck line comes apart -- unless it is BOOKSTORE.
            if late:
                for k, s0 in enumerate((96, 176, 256, 316)):
                    if t == s0:
                        self._add_wire("h", tsb_clamp(self.py, by + 20, by + bh - 20),
                                       ci=0, tel=34, on=12)
                        sc["strike_%d" % k] = (s0 + 34, tsb_clamp(self.py, by + 20, by + bh - 20))
                    spec = sc.get("strike_%d" % k)
                    if spec and t == spec[0]:
                        for li, (text, align, note) in enumerate(lines):
                            tag = "line%d" % li
                            body = [b for b in self.bullets if b.get("tag") == tag]
                            if not body or abs(body[0]["y"] - spec[1]) > 20:
                                continue
                            if note == "keep":
                                for b in body:
                                    b["jit"] = 3
                                tsb_play("denied", 0.6)
                            else:
                                for b in body:
                                    b["tag"] = None
                                    b["vx"] = self.rng.uniform(-1.4, 1.4)
                                    b["vy"] = self.rng.uniform(-2.2, -0.6)
                                    b["ay"] = 0.10
                                tsb_play("snap", 0.6)
            # The clip closes on your column, twice.
            for k, s0 in enumerate((330, 372)):
                if t == s0:
                    sc["clip_%d" % k] = tsb_clamp(self.px, bx + 30, bx + bw - 30)
                    tsb_play("glint", 0.8)
                xk = sc.get("clip_%d" % k)
                if xk is None:
                    continue
                if s0 <= t < s0 + 34:
                    u = (t - s0) / 34.0
                    self._scene_rect(xk - 22, by + 4, 44, bh - 8, ci=9,
                                     ghost=True, alpha=0.1 + 0.22 * u)
                    self._scene_sprite("clip", xk, by + 14, sc=4, alpha=0.95)
                elif s0 + 34 <= t < s0 + 50:
                    self._scene_rect(xk - 20, by, 40, bh, ci=9, harm=True,
                                     alpha=0.9)
                    self._scene_sprite("clip", xk, by + bh - 20, sc=4)
                    if t == s0 + 34:
                        self._slam_line(xk, by + 10, xk, by + bh - 10, 0.9, 9,
                                        "crumb", 3, "snap", 0.8)
            if t == (262 if not p2 else 236):
                self._needle(bx + bw + 10, cy + 40, -1.2)

        # ======================================================================
        # ARCADE -- "CONTINUE?"  (the SOUL turns BLUE: jump)
        # ======================================================================
        # The arcade stop, played as an arcade game. The SOUL turns blue --
        # gravity on, UP to jump -- and little critters waddle along the
        # floor to be hopped; a formation of them marches across the top on a
        # four-beat phrase (step, step, step, FIRE) and drops a shot from each
        # on the fourth; coins bounce across the boards; and the CONTINUE?
        # countdown falls on you as enormous digits, 3, 2, 1.
        # PHASE 2 -- "say it exactly like her": the formation's shots are cyan
        # and orange, and the four lamps show the phrase -- except the third
        # lamp, which copies whatever YOU were doing when it lit. Walkers stop
        # and then dash.

        def _pat_arcade(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            floor = self._floor_y()
            p2 = self.phase == 2
            sc = self.pat_scratch
            if t == 1:
                self._set_soul("blue")
            # cabinet dressing: scanlines + marquee
            for k in range(0, int(bh), 8):
                self._scene_rect(bx + 2, by + k, bw - 4, 1, ci=9, ghost=True,
                                 alpha=0.06)
            credit = 9 - min(9, t // 45)
            self._scene_text("CONTINUE? %d" % max(credit, 0), bx + 10, by + 8,
                             8, sc=2, alpha=0.85)
            # Walkers on the floor ---------------------------------------------
            walk = ((24, "L"), (84, "R"), (136, "L"), (176, "R"), (206, "R"),
                    (262, "L"), (292, "L"))
            for i, (w0, side) in enumerate(walk):
                if t == w0:
                    x0 = bx - 14 if side == "L" else bx + bw + 14
                    vx = (1.9 if side == "L" else -1.9) * (1.1 if p2 else 1.0)
                    b = self._add_bullet(x0, floor - 4, vx, 0.0, kind="critter",
                                         ttl=420)
                    if b is not None and p2 and i % 2 == 1:
                        # stop-and-dash: pause mid-floor, flash, then run
                        b["dash"] = {"at": 70, "stop": 24, "vx": vx * 1.9}
            # The formation ----------------------------------------------------
            if 90 <= t < 330:
                ft = t - 90
                beat = ft // 20
                step = beat % 4
                phrase_x = (beat // 4) % 2
                off = (step * 16 if phrase_x == 0 else (3 - step) * 16) - 24
                n = 5
                gap = 58.0
                xs = [cx - gap * (n - 1) * 0.5 + gap * j + off for j in range(n)]
                fy = by + 40
                firing = step == 3 and (ft % 20) < 10
                lamp_rules = None
                if p2:
                    # One lamp per bar, lit for the bar it governs: the
                    # colour the formation's shot will be. The third lamp is
                    # grey until halfway through its bar, then COPIES you --
                    # orange if you were moving, cyan if you were still --
                    # and the shot comes thirty ticks later in that colour.
                    bar = beat // 4
                    base = ["cyan", "orange", None, "orange"]
                    if bar % 4 == 2 and (ft % 80) == 40:
                        sc["echo_%d" % bar] = ("orange" if self.move_amt > 0.05
                                               else "cyan")
                        tsb_play("blip", 0.7)
                    if bar % 4 == 2:
                        base[2] = sc.get("echo_%d" % bar)
                    lamp_rules = base
                    for j in range(4):
                        col = {"cyan": 9, "orange": 4, None: 7}[base[j]]
                        on = j == bar % 4
                        lx = bx + bw - 80 + j * 20
                        self._scene_circle(lx, by + 17, 5, ci=col, ghost=True,
                                           alpha=1.0 if on else 0.55)
                        if on:
                            self._scene_circle(lx, by + 17, 8, ci=2, ghost=True,
                                               alpha=0.9, outline=True)
                for j, x in enumerate(xs):
                    frame = "critter_b" if beat % 2 else "critter_a"
                    self._scene_sprite(frame, x, fy, alpha=1.0,
                                       tint=("#ffe23d" if firing else None))
                    self._scene_circle(x, fy, 9, ci=2, harm=True, hidden=True)
                if ft % 80 == 70:
                    rule = None
                    if p2:
                        bar = beat // 4
                        rule = (lamp_rules or [None] * 4)[bar % 4]
                    for j, x in enumerate(xs):
                        self._add_bullet(x, fy + 14, 0.0, 2.6, kind="rice",
                                         ttl=200, rule=rule)
                    tsb_play("volley2", 0.6)
            # Coins ----------------------------------------------------------------
            for i, c0 in enumerate((200, 268)):
                if t == c0:
                    left = i % 2 == 0
                    b = self._add_bullet(bx + 20 if left else bx + bw - 20,
                                         by + 30, 1.6 if left else -1.6, 0.0,
                                         kind="coin", ay=0.16, ttl=320)
                    if b is not None:
                        b["bounce"] = {"n": 6, "rest": 0.78}
                    tsb_play("coin", 0.6)
            # CONTINUE? 3 2 1 ------------------------------------------------------
            for k, (d0, ch) in enumerate(((318, "3"), (344, "2"), (370, "1"))):
                if t == d0:
                    sc["digit_%d" % k] = tsb_clamp(self.px, bx + 34, bx + bw - 34)
                    tsb_play("glint", 0.8)
                dx = sc.get("digit_%d" % k)
                if dx is None:
                    continue
                if d0 <= t < d0 + 22:
                    u = (t - d0) / 22.0
                    self._scene_text(ch, dx - 12, by + 4, 8, sc=5, alpha=0.3 + 0.5 * u)
                    self._scene_ellipse(dx, floor + 6, 16, 5, 8, alpha=0.2 + 0.3 * u)
                if t == d0 + 22:
                    b = self._add_bullet(dx, by + 20, 0.0, 3.0, kind="glyph",
                                         ay=0.22, ttl=160)
                    if b is not None:
                        b["ch"] = ch
                        b["sc"] = 5
                        b["bounce"] = {"n": 1, "rest": 0.4}
            if t == 398:
                self._set_soul("red")
            if t == 150:
                self._needle(bx - 10, floor - 40, 1.1)

        # ======================================================================
        # BAGS -- "SHARED INVENTORY"  (read the throw, then the swap)
        # ======================================================================
        # Her blue bag and Matsu's orange bag hang in the top corners and
        # throw what is in them. Blue pens fly straight at where you were and
        # stick where they land; orange cans are lobbed onto a shadow on the
        # boards, bounce, and fizz a fan of spray upward. Halfway through the
        # bags swap places -- and throw each other's things.
        # REPRISE ("she gave every pen back"): the pens stay stuck, and at the
        # end every one of them flies back to its bag in a straight line.
        # PHASE 2 -- "whose hand is opening it": the bags drift after you, the
        # one nearest you does the throwing, and they swap twice.

        def _bag_pos(self, which, t):
            bx, by, bw, bh = self._arena()
            sc = self.pat_scratch
            p2 = self.phase == 2
            home = {"blue": bx + 44, "orange": bx + bw - 44}
            swaps = sc.get("swaps", ())
            x = home[which]
            for (s0, dur) in swaps:
                if t >= s0:
                    u = self._ease((t - s0) / float(dur))
                    other = bx + bw - 44 if x < bx + bw * 0.5 else bx + 44
                    x = x + (other - x) * u
            if p2:
                follow = sc.get("follow_" + which, 0.0)
                x = tsb_clamp(x + follow, bx + 34, bx + bw - 34)
            y = by + 30 + math.sin(t * 0.08 + (0 if which == "blue" else 2.0)) * 3.0
            return x, y

        def _pat_bags(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            floor = self._floor_y()
            p2 = self.phase == 2
            # Phase 1's bags always end with every pen going home.
            reprise = not p2
            sc = self.pat_scratch
            if t == 1:
                sc["swaps"] = [(190, 50)] if not p2 else [(150, 44), (286, 44)]
            # P2: the bags drift after you.
            if p2:
                for which in ("blue", "orange"):
                    bxx, _ = self._bag_pos(which, t)
                    f = sc.get("follow_" + which, 0.0)
                    f += tsb_clamp(self.px - bxx, -0.7, 0.7)
                    sc["follow_" + which] = tsb_clamp(f, -160.0, 160.0)
            pos = {w: self._bag_pos(w, t) for w in ("blue", "orange")}
            swapped = sum(1 for (s0, d) in sc.get("swaps", ()) if t >= s0 + d * 0.5) % 2 == 1
            for which in ("blue", "orange"):
                x, y = pos[which]
                hop = sc.get("hop_" + which, -99)
                dy = -6.0 * max(0.0, 1.0 - (t - hop) / 8.0) if t - hop < 8 else 0.0
                self._scene_sprite("bag_" + which, x, y + dy, alpha=1.0)
            # What each bag throws (swapped after the exchange).
            def thrower(which):
                natural = "pen" if which == "blue" else "can"
                if swapped:
                    natural = "can" if natural == "pen" else "pen"
                return natural
            throws = []
            if p2:
                near = min(("blue", "orange"), key=lambda w: abs(pos[w][0] - self.px))
                for k in range(0, 380, 26):
                    throws.append((20 + k, near if k % 52 else
                                   ("orange" if near == "blue" else "blue")))
            else:
                for k in range(0, 370, 34):
                    throws.append((24 + k, "blue"))
                for k in range(0, 370, 52):
                    throws.append((44 + k, "orange"))
            for (t0, which) in throws:
                if t0 > 350:
                    continue
                if p2:
                    # Whose hand, and what is in it, is decided once -- when
                    # the item shows in the bag's mouth -- and then kept.
                    if t == t0 - 20:
                        sc["who_%d" % t0] = which
                        sc["pick_%d" % t0] = self.rng.choice(("pen", "can"))
                    which = sc.get("who_%d" % t0, which)
                x, y = pos[which]
                item = thrower(which)
                if p2:
                    item = sc.get("pick_%d" % t0, item)
                if t0 - 20 <= t < t0:
                    # The item shows in the bag's mouth, pointing where it's going.
                    tgt = sc.get("aim_%d" % t0)
                    if t == t0 - 20:
                        sc["aim_%d" % t0] = (tsb_clamp(self.px, bx + 20, bx + bw - 20),
                                             tsb_clamp(self.py, by + 30, floor))
                        tgt = sc["aim_%d" % t0]
                    if tgt is not None:
                        ang = math.degrees(math.atan2(tgt[1] - y, tgt[0] - x))
                        self._scene_sprite(item, x, y + 10,
                                           rot=(ang if item == "pen" else 0.0),
                                           alpha=0.4 + 0.6 * (t - t0 + 20) / 20.0)
                        if item == "pen":
                            self._scene_line(x, y + 10, tgt[0], tgt[1], 1, 9,
                                             ghost=True, alpha=0.22)
                        else:
                            self._scene_ellipse(tgt[0], floor + 5, 14, 5, 4,
                                                alpha=0.35)
                if t == t0:
                    tgt = sc.get("aim_%d" % t0, (self.px, self.py))
                    sc["hop_" + which] = t
                    if item == "pen":
                        dxx, dyy = tgt[0] - x, tgt[1] - (y + 10)
                        d = max(1.0, math.hypot(dxx, dyy))
                        b = self._add_bullet(x, y + 10, dxx / d * 3.7, dyy / d * 3.7,
                                             kind="pen", ttl=400)
                        if b is not None:
                            b["stick"] = 400 if reprise else 60
                        tsb_play("throw", 0.5)
                    else:
                        b = self._lob(x, y + 10, tgt[0], floor - 2, 58, 0.10,
                                      "can", ttl=300)
                        if b is not None:
                            b["bounce"] = {"n": 1, "rest": 0.45}
                            b["land"] = {"do": "fizz"}
                        tsb_play("throw", 0.45)
            # The swap itself trails a little of both bags' contents.
            for (s0, dur) in sc.get("swaps", ()):
                if s0 <= t < s0 + dur and t % 6 == 0:
                    for which in ("blue", "orange"):
                        x, y = pos[which]
                        self._debris(x, y + 14, 1, "crumb", 9 if which == "blue" else 4,
                                     1.2, 50, sq=2, ay=0.08)
                if t == s0:
                    tsb_play("wire", 0.6)
            # REPRISE: every stuck pen goes home.
            if reprise:
                if 316 <= t < 340:
                    for b in self.bullets:
                        if b.get("kind") == "pen" and b.get("stuck"):
                            b["jit"] = 2
                            hx, hy = pos["blue"]
                            self._scene_line(b["x"], b["y"], hx, hy + 10, 1, 9,
                                             ghost=True, alpha=0.3)
                if t == 340:
                    hx, hy = pos["blue"]
                    for b in self.bullets:
                        if b.get("kind") == "pen" and b.get("stuck"):
                            dxx, dyy = hx - b["x"], hy + 10 - b["y"]
                            d = max(1.0, math.hypot(dxx, dyy))
                            b["stuck"] = False
                            b["stick"] = 0
                            b["jit"] = 0
                            b["vx"], b["vy"] = dxx / d * 3.4, dyy / d * 3.4
                            b["ttl"] = b["age"] + int(d / 3.4) + 2
                    tsb_play("release", 0.9)
            if t == (210 if not p2 else 180):
                self._needle(bx - 10, cy + 30, 1.2)

        # ======================================================================
        # CLOCK -- "UNDER THE STATION CLOCK"  (the room is the clock face)
        # ======================================================================
        # The station clock IS the room: the SOUL is confined to its face, and
        # it asks two things, one at a time.
        #   KEEP AHEAD OF THE MINUTE HAND. It is the only hand that cuts: a
        #   steady sweep round the face (about two px/tick at the rim, well
        #   under your walk). The hour hand crawls and the red second hand
        #   ticks the time; both are the clock's furniture and harmless.
        #   SIDESTEP THE CHIMES. On the hour the clock chimes, and bells fall
        #   straight down the face where you were standing, a walkable gap
        #   between each (their columns show first).
        # Rebuilt 2026-09-30 (user: the first cut was unintuitive and its
        # rim-to-centre bell ring closed too tightly).
        # The finale is "meet beneath the hand": both hands swing up to twelve
        # and wait there while the STAND HERE card settles on the hub, then
        # they spin round once, fast. The card is exactly the place they can't
        # reach. PHASE 2 -- "clock or mark": the minute hand shudders and runs
        # backward, then leaps a quarter turn (its ghost waits there first);
        # the chimes come more often. LATE -- "the hand has to wait": it stops
        # dead for stretches and trembles before it starts again.

        CLOCK_R = 112.0

        def _hand(self, cx, cy, ang, length, width, key, live, alpha=1.0, r0=30.0):
            # A hand's art points RIGHT from the hub and is as long as it is
            # drawn (the `length` argument is only a reading aid at the call
            # site). It cuts from r0 to its tip, so the hub is always safe.
            length = tsb_art_size(key)[0] * 2.0
            ca, sa = math.cos(ang), math.sin(ang)
            self._scene_sprite(key, cx + ca * length * 0.5, cy + sa * length * 0.5,
                               rot=math.degrees(ang), alpha=alpha)
            if live:
                self._scene_line(cx + ca * r0, cy + sa * r0,
                                 cx + ca * (length - 4.0), cy + sa * (length - 4.0),
                                 width, 2, harm=True, hidden=True)

        def _pat_clock(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            p2 = self.phase == 2
            late = p2 and self.pattern_slot >= 14
            sc = self.pat_scratch
            R = TSBGame.CLOCK_R
            up = -math.pi * 0.5
            if t == 1:
                self.arena_circle = (cx, cy, R - 4.0)
                sc["m_ang"] = up + 2.1          # about four o'clock
                sc["m_dir"] = 1.0
            self._scene_sprite("clock", cx, cy)
            finale = 336
            gather = 70
            # ---- the furniture: hour hand crawls, second hand ticks --------
            h_ang = up + 2.8 + t * 0.0015
            s_ang = up + (t // 30) * math.pi / 6.0
            if t % 30 == 0:
                tsb_play("blip", 0.3)
            # ---- the minute hand -----------------------------------------------
            w = 0.019 * sc.get("m_dir", 1.0)
            shudder = False
            if t < 40:
                w = 0.0
                shudder = t >= 16
            if p2 and not late:
                for rv_t in (130, 250):
                    if rv_t - 30 <= t < rv_t:
                        w = 0.0
                        shudder = True
                    if t == rv_t:
                        sc["m_dir"] = -sc.get("m_dir", 1.0)
                        tsb_play("snap", 0.5)
                jump_t = 190
                if jump_t - 36 <= t < jump_t:
                    self._hand(cx, cy, sc["m_ang"] + math.pi * 0.5, 0, 10,
                               "hand_min", False, alpha=0.35)
                if t == jump_t:
                    sc["m_ang"] += math.pi * 0.5
                    tsb_play("dagger", 0.8)
                    self._spark_burst(cx, cy, 12, 2, 2.6, 24)
            if late:
                for (w0, w1) in ((90, 150), (210, 270)):
                    if w0 <= t < w1:
                        w = 0.0
                    if w1 - 24 <= t < w1:
                        shudder = True
                    if t == w1:
                        tsb_play("snap", 0.5)
            if t < finale - gather:
                sc["m_ang"] = sc.get("m_ang", 0.0) + w
                m_ang = sc["m_ang"] + (math.sin(t * 1.3) * 0.03 if shudder else 0.0)
                self._hand(cx, cy, h_ang, 0, 14, "hand_hour", False)
                self._hand(cx, cy, s_ang, 0, 4, "hand_sec", False, alpha=0.9)
                self._hand(cx, cy, m_ang, 0, 10, "hand_min", t >= 40)
            # ---- the chimes: bells fall down the face where you were ---------
            chimes = (104, 220) if not p2 else (84, 168, 252)
            n_b = 4 if p2 else 3
            top = cy - R + 16
            for c, c0 in enumerate(chimes):
                if t == c0 - 30:
                    base = tsb_clamp(self.px, cx - R + 30, cx + R - 30)
                    sc["bells_%d" % c] = [base + (j - (n_b - 1) * 0.5) * 52.0
                                          for j in range(n_b)]
                    tsb_play("glint", 0.6)
                xs = sc.get("bells_%d" % c)
                if xs is None:
                    continue
                if c0 - 30 <= t < c0:
                    u = (t - c0 + 30) / 30.0
                    for x in xs:
                        self._scene_sprite("bell", x, top, alpha=0.3 + 0.6 * u,
                                           rot=math.sin(t * 0.5) * 12.0)
                        self._scene_rect(x - 8, top + 10, 16, R * 2 - 30, ci=8,
                                         ghost=True, alpha=0.05 + 0.10 * u)
                if t == c0:
                    tsb_play("bloom", 0.8)
                    for x in xs:
                        self._add_bullet(x, top, 0.0, 1.2, kind="bell", ay=0.1,
                                         ttl=110)
            # ---- "meet beneath the hand" -----------------------------------------
            if finale - gather <= t < finale:
                u = self._ease((t - finale + gather) / float(gather))
                # both hands swing up to twelve and wait there, harmless
                m0 = sc.get("m_ang", up)
                target = up + math.pi * 2.0 * round((m0 - up) / (math.pi * 2.0))
                self._hand(cx, cy, m0 + (target - m0) * u, 0, 10, "hand_min", False)
                self._hand(cx, cy, h_ang + (up - h_ang) * u, 0, 14, "hand_hour", False)
                self._scene_circle(cx, cy, 34, ci=8, ghost=True,
                                   alpha=0.3 + 0.6 * u, outline=True)
                self._scene_sprite("card", cx, cy, alpha=u, sc=1)
                if t == finale - gather:
                    tsb_play("glint", 0.9)
            if finale <= t < finale + 60:
                k = t - finale
                a = up + (k / 60.0) * math.pi * 2.0 * (1.0 if not p2 else -1.0)
                self._scene_sprite("card", cx, cy, sc=1)
                self._hand(cx, cy, a, 0, 10, "hand_min", True, r0=46.0)
                self._hand(cx, cy, a + math.pi, 0, 10, "hand_min", True, r0=46.0)
                self._hand(cx, cy, up + (a - up) * 0.5, 0, 14, "hand_hour", False)
                if k % 10 == 0:
                    tsb_play("blip", 0.5)
            if t >= finale + 60:
                # Eleven o'clock. They stop.
                self._hand(cx, cy, up, 0, 10, "hand_min", False)
                self._hand(cx, cy, up - math.pi / 6.0, 0, 14, "hand_hour", False)
                if t == finale + 60:
                    self._slam(cx, cy, 1.0, 8, "spark", "confirm", 0.8)
            self._scene_sprite("hub", cx, cy, sc=3)
            if t == (130 if not p2 else 110):
                a = self.rng.uniform(0, 6.28)
                self._needle(cx + math.cos(a) * 80, cy + math.sin(a) * 80,
                             -math.cos(a) * 0.9, -math.sin(a) * 0.9, ttl=150)

        # ======================================================================
        # CROWD -- "STAND HERE"  (the station: cyan, stand still; orange, move)
        # ======================================================================
        # Commuters cross the concourse in columns. A white column has one
        # missing person: walk into that place (a yellow bracket names it at
        # the wall before the column steps out). A CYAN column is full -- the
        # card that said STAND HERE drops in to say what it means: hold still
        # and the crowd walks through you. An ORANGE column is full too: keep
        # moving and you slip through it.
        # REPRISE ("the place holds through a revision"): the card itself
        # rides in every column's missing place. Follow the card.
        # PHASE 2 -- "clip or card": columns come from both walls at once,
        # traffic stops and surges, and two columns change colour mid-
        # crossing (they flicker between both colours for half a second, and
        # the missing commuter steps back into the lane as they turn).
        # LATE ("once"): the card appears for the first cyan column only.

        def _pat_crowd(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            p2 = self.phase == 2
            reprise = (not p2) and self.pattern_slot == 9
            late = p2 and self.pattern_slot >= 10
            sc = self.pat_scratch
            rows = self._crowd_rows()
            # the platform edge
            self._scene_line(bx + 8, by + bh - 7, bx + bw - 8, by + bh - 7, 2, 8,
                             ghost=True, alpha=0.35)
            spd = 2.2
            surge = ()
            if reprise:
                sched = [(20, "L", 2, None), (74, "R", 0, None),
                         (128, "L", 3, None), (182, "R", None, "cyan"),
                         (236, "L", 1, None), (290, "R", 4, None)]
            elif not p2:
                # Cyan and orange columns only ever travel the SAME way, so
                # the time between them is the same everywhere in the room.
                sched = [(20, "L", 2, None), (70, "R", 1, None),
                         (120, "L", None, "cyan"), (170, "L", 3, None),
                         (200, "R", 2, None), (240, "L", None, "orange"),
                         (282, "L", None, "cyan"), (320, "L", 3, None)]
            else:
                # A cyan era, then an orange one; a column that changes color
                # only ever joins the era it changes into, from the same side.
                sched = [(20, "L", 1, None), (20, "R", 3, None),
                         (60, "L", None, "cyan"), (110, "R", 2, None),
                         (150, "L", 3, "flip_cyan"), (280, "L", None, "orange"),
                         (300, "R", 1, "flip_orange")]
                surge = (1, 3)
            first_cyan = None
            for si, (s0, side, lane, rule) in enumerate(sched):
                if rule == "cyan" and first_cyan is None:
                    first_cyan = si
                tag = "crowd%d" % si
                x0 = bx - 16 if side == "L" else bx + bw + 16
                vx = spd if side == "L" else -spd
                real_rule = rule if rule in ("cyan", "orange") else None
                if s0 - 34 <= t < s0:
                    u = (t - s0 + 34) / 34.0
                    ex = bx + 10 if side == "L" else bx + bw - 10
                    col = {"cyan": 9, "orange": 4}.get(real_rule, 2)
                    self._scene_rect(ex - 3, by + 6, 6, bh - 12, ci=col, ghost=True,
                                     alpha=0.2 + 0.5 * u)
                    if lane is not None and real_rule is None:
                        self._scene_rect(ex - 12, rows[lane] - 23, 24, 46, ci=8,
                                         ghost=True, alpha=0.3 + 0.5 * u, outline=True)
                        if reprise:
                            self._scene_sprite("card", ex + (40 if side == "L" else -40),
                                               rows[lane], sc=1, alpha=u)
                    if real_rule == "cyan" and (not late or si == first_cyan):
                        self._scene_sprite("card", cx, by + 26, sc=2,
                                           alpha=0.4 + 0.6 * u)
                    if t == s0 - 34:
                        tsb_play("glint", 0.6)
                if t == s0:
                    self._crowd_column(x0, vx, lane if real_rule is None else None,
                                       rule=real_rule, tag=tag)
                    tsb_play("volley", 0.55)
                if reprise and lane is not None and t > s0:
                    # The card rides in the missing place.
                    body = [b for b in self.bullets if b.get("tag") == tag]
                    if body:
                        self._scene_sprite("card", body[0]["x"], rows[lane], sc=1)
                if rule in ("flip_orange", "flip_cyan"):
                    new = "orange" if rule == "flip_orange" else "cyan"
                    at = s0 + 70
                    body = [b for b in self.bullets if b.get("tag") == tag]
                    if at - 30 <= t < at and body:
                        for b in body:
                            b["flicker"] = new
                    if t == at and body:
                        # Close the lane first: the missing commuter steps in.
                        for b in body:
                            b["rule"] = new
                            b["flicker"] = None
                        if lane is not None:
                            nb = self._add_bullet(body[0]["x"], rows[lane], vx, 0.0,
                                                  kind="commuter", ttl=460, rule=new)
                            if nb is not None:
                                nb["tag"] = tag
                        tsb_play("denied", 0.5)
                if si in surge:
                    # Stop-and-surge traffic: it halts (and shivers), then
                    # hurries on at 1.6x -- still slower than the SOUL.
                    k = t - s0
                    body = [b for b in self.bullets if b.get("tag") == tag]
                    if body and k == 60:
                        for b in body:
                            b["vx"] = 0.0
                            b["jit"] = 1
                        tsb_play("glint", 0.5)
                    if body and k == 84:
                        for b in body:
                            b["vx"] = vx * 1.6
                            b["jit"] = 0
            if t == 150:
                self._needle(cx, by - 8, 0.0, 1.0, ttl=260)

        # ======================================================================
        # LUNCH -- "THE THIRD STOP"  (food: read the bounce, dodge the pinch)
        # ======================================================================
        # Rice crackers are tossed in, bounce off the walls, and CRACK into
        # crumbs when they hit the boards. Chopsticks hover over where you
        # were -- their closed position drawn pale -- and pinch. The bento on
        # the floor spills rice now and then. "Green, to your left!": a needle
        # appears beside you, and it is yours. The lunch-box lid comes down
        # over the top half of the room to finish.
        # PHASE 2 -- "take it, take it": three needles, and whichever you take,
        # the chopsticks come for the place you took it; crackers come three
        # at a time; the lid comes down twice, top half then bottom half.

        def _chopsticks(self, tx, ty, u, live):
            # Two sticks pivoting from high corners so their tips meet at the
            # target. u is the close: 0 open, 1 shut.
            L = 204.0
            out = []
            for sgn in (-1.0, 1.0):
                pvx = tx + sgn * 150.0
                pvy = ty - 140.0
                final = math.atan2(ty - pvy, tx - pvx)
                ang = final + sgn * (-0.55) * (1.0 - u)
                ca, sa = math.cos(ang), math.sin(ang)
                self._scene_sprite("chopstick", pvx + ca * L * 0.5, pvy + sa * L * 0.5,
                                   rot=math.degrees(ang), alpha=1.0 if live else 0.55)
                if live:
                    self._scene_line(pvx + ca * 20, pvy + sa * 20, pvx + ca * L,
                                     pvy + sa * L, 8, 7, harm=True, hidden=True)
            return out

        def _pat_lunch(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            floor = self._floor_y()
            p2 = self.phase == 2
            sc = self.pat_scratch
            rattle = 14 <= t % 60 < 30 and t < 330
            self._scene_sprite("bento", cx + ((t % 4) - 1.5 if rattle else 0.0),
                               floor - 4, alpha=0.95)
            # Crackers --------------------------------------------------------
            every = 44 if p2 else 30
            if 10 <= t < 330 and t % every == 10:
                n = 3 if p2 else 1
                for j in range(n):
                    k = (t // every) * 3 + j
                    x = bx + 40 + ((k * 97) % int(bw - 80))
                    vx = (1.4 if k % 2 else -1.4) * (1.0 + 0.2 * j)
                    b = self._add_bullet(x, by - 8, vx, 1.2, kind="cracker",
                                         ay=0.06, ttl=400)
                    if b is not None:
                        b["walls"] = True
                        b["land"] = {"do": "crack"}
                tsb_play("throw", 0.4)
            # Chopsticks ------------------------------------------------------
            pinches = [(80,), (170,), (260,)] if not p2 else [(70,), (150,)]
            for k, (p0,) in enumerate(pinches):
                if t == p0:
                    sc["pinch_%d" % k] = (tsb_clamp(self.px, bx + 30, bx + bw - 30),
                                          tsb_clamp(self.py, by + 30, floor - 10))
                    tsb_play("glint", 0.8)
                spec = sc.get("pinch_%d" % k)
                if spec is None:
                    continue
                tx, ty = spec
                if p0 <= t < p0 + 36:
                    self._chopsticks(tx, ty, 0.0, False)
                    self._chopsticks(tx, ty, 1.0, False)
                    self._scene_circle(tx, ty, 8, ci=8, ghost=True, alpha=0.8, outline=True)
                elif p0 + 36 <= t < p0 + 60:
                    u = self._ease((t - p0 - 36) / 8.0)
                    self._chopsticks(tx, ty, u, True)
                    if t == p0 + 44:
                        self._slam(tx, ty, 0.8, 7, "crumb", "snap", 0.8)
            # P2: needles, and the chopsticks come for where you took one.
            if p2:
                for k, (n0, ox, oy) in enumerate(((200, -90, 0), (214, 90, 0), (228, 0, -80))):
                    if t == n0:
                        b = self._needle(tsb_clamp(self.px + ox, bx + 20, bx + bw - 20),
                                         tsb_clamp(self.py + oy, by + 20, floor - 10),
                                         0.0, 0.0, ttl=120)
                        if b is not None:
                            b["tag"] = "gift"
                if 200 <= t < 330 and "gift_taken" not in sc:
                    if sc.get("healed_at") is not None:
                        sc["gift_taken"] = (self.px, self.py, t)
                taken = sc.get("gift_taken")
                if taken:
                    tx, ty, t0 = taken
                    if t0 <= t < t0 + 30:
                        self._chopsticks(tx, ty, 1.0, False)
                        self._scene_circle(tx, ty, 8, ci=0, ghost=True, alpha=0.9,
                                           outline=True)
                    elif t0 + 30 <= t < t0 + 52:
                        self._chopsticks(tx, ty, self._ease((t - t0 - 30) / 8.0), True)
            else:
                if t == 200:
                    self._needle(tsb_clamp(self.px - 80, bx + 16, bx + bw - 16),
                                 tsb_clamp(self.py, by + 20, floor - 10), 0.35,
                                 0.0, ttl=180)
            # Rice spill --------------------------------------------------------
            if t % 60 == 30 and t < 330:
                for j in range(3):
                    self._add_bullet(cx + (j - 1) * 6, floor - 12,
                                     (j - 1) * 0.7, -3.4 - 0.2 * j, kind="rice",
                                     ay=0.11, ttl=120)
            # The lid -------------------------------------------------------------
            lids = [(340, "top")] if not p2 else [(330, "top"), (374, "bottom")]
            for (l0, half) in lids:
                y0 = by if half == "top" else cy
                if l0 - 40 <= t < l0:
                    u = (t - l0 + 40) / 40.0
                    self._scene_rect(bx + 2, y0, bw - 4, bh * 0.5, ci=0, ghost=True,
                                     alpha=0.06 + 0.14 * u)
                    if (t // 5) % 2 == 0:
                        self._scene_rect(bx + 4, y0 + 2, bw - 8, bh * 0.5 - 4,
                                         ci=0, ghost=True, alpha=0.5 + 0.4 * u,
                                         outline=True)
                    if t == l0 - 40:
                        tsb_play("glint", 0.8)
                elif l0 <= t < l0 + 20:
                    self._scene_rect(bx, y0, bw, bh * 0.5, ci=6, harm=True, alpha=0.85)
                    self._scene_rect(cx - 50, y0 + bh * 0.25 - 5, 100, 10, ci=8,
                                     ghost=True, alpha=0.9)
                    if t == l0:
                        self._slam_line(bx + 10, cy, bx + bw - 10, cy, 1.1, 6, "rice", 5,
                                        "fall", 0.7)

        # ======================================================================
        # STRUNG -- "THE STRINGS MOVE FIRST"  (phase 2 only: the SOUL is strung)
        # ======================================================================
        # Her strings come down across the room and the SOUL is tied to them:
        # slide along a string with left/right, hop to the next with up/down
        # (the Undertale purple-soul rule, and here it means something).
        # Petals crawl along the strings from their pins; petals drop across
        # them where you were; a string trembles and is YANKED, carrying you
        # with it. Then the strings tilt.
        # LATE ("no next cue arrives on its own"): the strings fray and are cut
        # one by one -- you drop to the next -- until the last one goes and
        # the SOUL falls free, into silence.

        def _pat_strung(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            late = self.pattern_slot >= 15
            sc = self.pat_scratch
            n = 4
            if t == 1:
                self.strings_on = []
                for k in range(n):
                    y = by + bh * (k + 1) / float(n + 1)
                    self.strings_on.append({"id": k, "y0": y, "y1": y,
                                            "base": y, "alive": True, "yank": 0.0,
                                            "tremble": 0})
                self._set_soul("strung")
            strings = self.strings_on
            # tilt (non-late second half)
            if not late and t >= 230:
                u = self._ease((t - 230) / 60.0)
                for s in strings:
                    tilt = (14.0 if s["id"] % 2 == 0 else -14.0) * u
                    s["y0"] = s["base"] - tilt + s["yank"]
                    s["y1"] = s["base"] + tilt + s["yank"]
            else:
                for s in strings:
                    s["y0"] = s["base"] + s["yank"]
                    s["y1"] = s["base"] + s["yank"]
            # yanks
            yanks = ((110, 1), (170, 2), (300, 0)) if not late else ((90, 2), (200, 1))
            for (y0, k) in yanks:
                if k >= len(strings):
                    continue
                s = strings[k]
                if y0 - 30 <= t < y0:
                    s["tremble"] = 2
                if y0 <= t < y0 + 8:
                    s["tremble"] = 0
                    s["yank"] = -26.0 * self._ease((t - y0) / 8.0)
                elif y0 + 8 <= t < y0 + 40:
                    s["yank"] = -26.0 * (1.0 - self._ease((t - y0 - 8) / 32.0))
                if t == y0:
                    tsb_play("wire", 0.8)
            # crawlers along strings
            crawl = [(40, 0, "L"), (64, 2, "R"), (96, 1, "L"), (128, 3, "R"),
                     (150, 0, "R"), (150, 2, "L"), (206, 1, "R"), (240, 3, "L"),
                     (262, 0, "L"), (290, 2, "R"), (318, 1, "L"), (340, 3, "R")]
            if late:
                crawl = [(40, 0, "L"), (70, 3, "R"), (110, 2, "L"), (150, 1, "R"),
                         (190, 3, "L"), (240, 0, "R"), (280, 2, "L")]
            for (c0, k, side) in crawl:
                if k >= len(strings) or not strings[k]["alive"]:
                    continue
                s = strings[k]
                ex = bx + 6 if side == "L" else bx + bw - 6
                if c0 - 30 <= t < c0:
                    u = (t - c0 + 30) / 30.0
                    yy = s["y0"] if side == "L" else s["y1"]
                    self._scene_sprite("petal", ex, yy, alpha=0.3 + 0.6 * u)
                    self._scene_circle(ex, yy, 10, ci=8, ghost=True, alpha=0.5 * u,
                                       outline=True)
                if t == c0:
                    b = self._add_bullet(ex, s["y0"] if side == "L" else s["y1"],
                                         2.3 if side == "L" else -2.3, 0.0,
                                         kind="petal", ttl=240)
                    if b is not None:
                        b["on_string"] = k
                    tsb_play("throw", 0.35)
            # drops across the strings
            drops = (80, 140, 196, 256, 320) if not late else (60, 130, 170, 230, 270)
            for d0 in drops:
                if t == d0:
                    sc["drop_%d" % d0] = tsb_clamp(self.px, bx + 20, bx + bw - 20)
                    tsb_play("glint", 0.5)
                dx = sc.get("drop_%d" % d0)
                if dx is None:
                    continue
                if d0 <= t < d0 + 24:
                    self._scene_rect(dx - 10, by + 4, 20, bh - 8, ci=0, ghost=True,
                                     alpha=0.18)
                if t == d0 + 24:
                    for j in range(2):
                        self._add_bullet(dx + (j - 0.5) * 12, by - 6 - j * 18, 0.0, 2.6,
                                         kind="petal", ttl=200)
            # cuts (late): each string frays red, then snaps
            if late:
                for k, c0 in enumerate((120, 220, 310, 390)):
                    order = (0, 3, 1, 2)
                    sid = order[k]
                    if sid >= len(strings):
                        continue
                    s = strings[sid]
                    if c0 - 40 <= t < c0 and s["alive"]:
                        s["fray"] = True
                    if t == c0 and s["alive"]:
                        s["alive"] = False
                        s["fray"] = False
                        self._spark_burst(cx, s["base"], 18, 5, 3.4, 40)
                        tsb_play("snap", 0.9)
                        self.flash = max(self.flash, 0.12)
                if t >= 392:
                    self._set_soul("red")
            if t == 180 and len(strings) > 1 and strings[1]["alive"]:
                nb = self._needle(bx - 10, strings[1]["y0"], 1.2)
                if nb is not None:
                    nb["on_string"] = 1
            if not late and t == 408:
                self._set_soul("red")

        # ======================================================================
        # ITINERARY -- "BOOKSTORE, ARCADE, FOOD"  (phase 1's last turn)
        # ======================================================================
        # The whole day, in order, one stop at a time -- and then the only
        # item on today's list.

        def _pat_itinerary(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            floor = self._floor_y()
            sc = self.pat_scratch
            names = ((1, "1.BOOKSTORE"), (118, "2.ARCADE"), (236, "3.FOOD"),
                     (300, "TODAY: STAND HERE"))
            for (n0, label) in names:
                if n0 <= t < n0 + 40:
                    a = 1.0 - max(0.0, (t - n0 - 26) / 14.0)
                    self._scene_text(label, cx - len(label) * 6, by + 8, 8, sc=2,
                                     alpha=a)
                if t == n0:
                    tsb_play("confirm", 0.6)
                    self.flash = max(self.flash, 0.10)
            # 1. books from both cases, one lane
            if 10 <= t < 40:
                self._book_telegraph(bx + 38, 5, (t - 10) / 30.0)
                self._book_telegraph(bx + bw - 38, 5, (t - 10) / 30.0)
            if t == 40:
                self._book_column(bx + 38, 2.4, 5, tag="i1")
                self._book_column(bx + bw - 38, -2.4, 5, tag="i2")
                tsb_play("volley", 0.7)
            self._scene_sprite("shelf", bx + 18, cy, alpha=0.5 if t < 118 else 0.2)
            self._scene_sprite("shelf", bx + bw - 18, cy, alpha=0.5 if t < 118 else 0.2,
                               flip=True)
            # 2. the arcade, blue soul
            if t == 124:
                self._set_soul("blue")
            if t in (140, 176, 206):
                side = "L" if t != 176 else "R"
                self._add_bullet(bx - 12 if side == "L" else bx + bw + 12, floor - 4,
                                 2.0 if side == "L" else -2.0, 0.0, kind="critter",
                                 ttl=300)
            if t == 190:
                for j in range(5):
                    self._add_bullet(cx - 116 + j * 58, by + 40, 0.0, 2.6,
                                     kind="rice", ttl=200)
                tsb_play("volley2", 0.6)
            if 170 <= t < 190:
                for j in range(5):
                    self._scene_sprite("critter_a", cx - 116 + j * 58, by + 34,
                                       tint="#ffe23d" if t > 180 else None)
            if t == 236:
                self._set_soul("red")
            # 3. food
            if t in (244, 260, 276, 292):
                k = (t - 244) // 16
                x = bx + 60 + ((k * 131) % int(bw - 120))
                b = self._add_bullet(x, by - 8, 1.3 if k % 2 else -1.3, 1.3,
                                     kind="cracker", ay=0.06, ttl=300)
                if b is not None:
                    b["walls"] = True
                    b["land"] = {"do": "crack"}
            if t == 262:
                sc["pinch"] = (tsb_clamp(self.px, bx + 30, bx + bw - 30),
                               tsb_clamp(self.py, by + 30, floor - 10))
            if sc.get("pinch"):
                tx, ty = sc["pinch"]
                if 262 <= t < 294:
                    self._chopsticks(tx, ty, 1.0, False)
                elif 294 <= t < 314:
                    self._chopsticks(tx, ty, self._ease((t - 294) / 8.0), True)
            # 4. today: stand here
            if 300 <= t < 334:
                u = (t - 300) / 34.0
                self._scene_sprite("card", cx, by + 26, sc=2, alpha=0.4 + 0.6 * u)
                self._scene_rect(bx + 7, by + 6, 6, bh - 12, ci=9, ghost=True,
                                 alpha=0.2 + 0.5 * u)
            if t == 334:
                self._crowd_column(bx - 16, 2.6, None, rule="cyan", tag="today")
            if t == 250:
                self._needle(bx + bw + 10, cy, -1.2)

        # ======================================================================
        # REVISION -- "REVISED"  (phase 2 only: the room rewinds, and edits)
        # ======================================================================
        # Someone else's memory writes over hers. Something happens -- a book
        # column crosses, a line of the list drops, the sword thrusts -- and
        # then the tape REWINDS: everything in the room runs backward along
        # the path you just watched it take (so the answer is the one you
        # already found), and then a REVISED stamp slams down and it happens
        # again, differently.

        def _rewind(self, tags=None, on=True):
            for b in self.bullets:
                if tags is None or b.get("tag") in tags:
                    b["vx"] = -b["vx"]
                    b["vy"] = -b["vy"]
            self.rewinding = on
            tsb_play("wire" if on else "confirm", 0.7)

        def _pat_revision(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            sc = self.pat_scratch
            n_rows = len(self._book_rows())
            self._scene_sprite("shelf", bx + 18, cy, alpha=0.6)
            # A: a column crosses, rewinds, is revised
            if 8 <= t < 40:
                self._book_telegraph(bx + 38, 7, (t - 8) / 32.0)
            if t == 40:
                self._book_column(bx + 38, 2.6, min(7, n_rows - 3), tag="rA")
                tsb_play("volley", 0.7)
            if t == 116:
                self._rewind(("rA",))
                sc["rw_until"] = 176
            if t == 176:
                self._rewind(("rA",), on=False)
                for b in self.bullets:
                    if b.get("tag") == "rA":
                        b["fz"] = 14
                sc["stamp"] = t
            if 176 <= t < 206:
                self._book_telegraph(bx + 38, 1, (t - 176) / 30.0)
            if t == 206:
                self._book_column(bx + 38, 2.8, 1, tag="rA2")
            # B: a line drops, rewinds up, is revised
            if 130 <= t < 150:
                self._scene_text("2.ARCADE"[:1 + (t - 130) // 2],
                                 bx + bw - 12 - 18 * 8, by + 3, 8, sc=3, alpha=0.55)
            if 280 <= t < 300:
                self._scene_text("2.FOOD"[:1 + (t - 280) // 3],
                                 bx + 12, by + 3, 8, sc=3, alpha=0.55)
            if t == 150:
                self._text_line("2.ARCADE", bx + bw - 12 - 18 * 8, by + 16, tag="rB")
                self._tag_set("rB", vy=1.5)
            if t == 260:
                self._rewind(("rB",))
            if t == 300:
                self._rewind(("rB",), on=False)
                for b in self.bullets:
                    if b.get("tag") == "rB":
                        b["fz"] = 14
                sc["stamp"] = t
                self._text_line("2.FOOD", bx + 12, by + 16, tag="rB2")
                self._tag_set("rB2", vy=1.6)
            # C: the sword thrusts at your old height, rewinds, revised from
            # the other wall
            if t == 318:
                sc["thr"] = tsb_clamp(self.py, by + 24, by + bh - 24)
            thr = sc.get("thr")
            if thr is not None:
                if 318 <= t < 346:
                    self._scene_rect(bx + 4, thr - 14, bw - 8, 28, ci=1, ghost=True,
                                     alpha=0.2)
                    self._sword(bx + bw + 20 - 30 * (t - 318) / 28.0, thr, math.pi, False)
                elif 346 <= t < 366:
                    k = t - 346
                    reach = (bw - 70) * self._ease(min(1.0, k / 6.0))
                    self._sword(bx + bw - 10 - reach, thr, math.pi, True)
                elif 366 <= t < 380:
                    # The tape runs back: the blade withdraws along its line.
                    k = t - 366
                    reach = (bw - 70) * (1.0 - self._ease(k / 14.0))
                    self._sword(bx + bw - 10 - reach, thr, math.pi, False, alpha=0.6)
                    if k == 0:
                        self.rewinding = True
                        tsb_play("wire", 0.6)
                if t == 380:
                    self.rewinding = False
                    sc["stamp"] = t
                    sc["thr2"] = tsb_clamp(self.py, by + 24, by + bh - 24)
            thr2 = sc.get("thr2")
            if thr2 is not None:
                if 380 <= t < 404:
                    self._scene_rect(bx + 4, thr2 - 14, bw - 8, 28, ci=1, ghost=True,
                                     alpha=0.2)
                    self._sword(bx - 20 + 30 * (t - 380) / 24.0, thr2, 0.0, False)
                elif 404 <= t < 422:
                    k = t - 404
                    reach = (bw - 70) * self._ease(min(1.0, k / 6.0))
                    self._sword(bx + 10 + reach, thr2, 0.0, k < 14)
            st = sc.get("stamp")
            if st is not None and st <= t < st + 30:
                self._scene_sprite("stamp_revised", cx, cy - 40, sc=3,
                                   alpha=1.0 - max(0.0, (t - st - 20) / 10.0))
                if t == st:
                    self._slam(cx, cy - 40, 1.0, 0, "crumb", "snap", 0.9,
                               flash=0.14)
            if t == 230:
                self._needle(bx - 10, cy + 50, 1.2)

        # ======================================================================
        # FIRST -- "ME FIRST"  (forced: she takes your first turn)
        # ======================================================================
        # Undertale's oldest joke on the player, told her way. The menu comes
        # up, the flavor line says she is waiting for you to go first, you
        # press a button -- and she cuts in. She always lets everyone go
        # first; this once she doesn't, and she opens with everything:
        #   I.   the flavor line you were reading falls apart on you, word by
        #        word, inside the wide menu box (each word shivers first);
        #   II.  the box snaps shut to a small square;
        #   III. book columns from alternating walls, each lane sharing a row
        #        with the last, so a crossing always has somewhere to go;
        #   IV.  the inflatable sword spins in a room barely bigger than it
        #        -- the corners are the only places it can't reach;
        #   V.   four whole camellias fall where you were and burst;
        #   VI.  a green needle, which is her apologizing.
        # Hard on purpose, and it can be finished untouched.

        FIRST_SQUARE = 250.0

        def _first_letters(self):
            # The exact glyphs the menu was showing, as bodies: "* " at the
            # box's text margin and the flavor two cells after it.
            bx, by, bw, bh = self._arena()
            line = "* " + TSB_FLAVOR_FIRST
            x0 = bx + 22.0
            y = by + 20.0 + TSB_GLYPH_H
            word = 0
            words = 1
            for i, ch in enumerate(line):
                if ch == " ":
                    if i > 0 and line[i - 1] != " ":
                        word += 1
                        words += 1
                    continue
                b = self._add_bullet(x0 + i * 12.0 + 5.0, y, 0.0, 0.0,
                                     kind="glyph", ttl=900, armed_at=10 ** 6)
                if b is not None:
                    b["ch"] = ch
                    b["sc"] = 2
                    b["word"] = word
            order = list(range(words))
            self.rng.shuffle(order)
            self.pat_scratch["word_order"] = order

        def _pat_first(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            sc = self.pat_scratch
            # I. the flavor line falls apart, one shivering word at a time.
            for k, w in enumerate(sc.get("word_order", ())):
                d0 = 36 + k * 13
                if t == d0 - 20:
                    self._tag_word(w, jit=2)
                    tsb_play("glint", 0.5)
                if t == d0:
                    for b in self.bullets:
                        if b.get("word") == w and b["kind"] == "glyph":
                            b["jit"] = 0
                            b["armed_at"] = b["age"]
                            b["vy"] = 0.6
                            b["vx"] = self.rng.uniform(-0.25, 0.25)
                            b["ay"] = 0.2
                            b["bounce"] = {"n": 0}
                    tsb_play("throw", 0.5)
            # II. the squeeze.
            if t == 160:
                side = TSBGame.FIRST_SQUARE
                self.box_target = [TSB_BOX_CX, TSB_BOX_CY, side, side]
                self.shake = max(self.shake, 10)
                tsb_play("snap", 0.9)
                for b in self.bullets:
                    if b["kind"] == "glyph":
                        b["fz"] = min(b["fz"] or 12, 12)
            if t < 186:
                return
            # III. books, alternating walls; consecutive lanes share a row.
            rows = self._book_rows()
            n_rows = len(rows)
            for si, (launch, side, gap) in enumerate(((220, "L", 2), (254, "R", 3),
                                                      (288, "L", 5), (322, "R", 6))):
                gap = min(gap, n_rows - 3)
                x0 = bx + 30 if side == "L" else bx + bw - 30
                vx = 3.0 if side == "L" else -3.0
                if launch - 30 <= t < launch:
                    self._book_telegraph(x0, gap, (t - launch + 30) / 30.0)
                    if t == launch - 30:
                        tsb_play("glint", 0.55)
                if t == launch:
                    self._book_column(x0, vx, gap, tag="f%d" % si)
                    tsb_play("volley", 0.75)
            # IV. the sword in a room barely bigger than it.
            L = TSBGame.SWORD_LEN
            half = L * 0.5
            sp0, spin_tel = 420, 64
            if sp0 - spin_tel <= t < sp0:
                u = (t - sp0 + spin_tel) / float(spin_tel)
                ang = t * 0.05
                self._scene_circle(cx, cy, 127, ci=1, ghost=True,
                                   alpha=0.12 + 0.35 * u, outline=True)
                self._sword(cx - math.cos(ang) * half, cy - math.sin(ang) * half,
                            ang, False, alpha=0.8)
                sc["spin_a"] = ang
                if t == sp0 - spin_tel:
                    tsb_play("glint", 0.9)
            elif sp0 <= t < sp0 + 50:
                ang = sc.get("spin_a", 0.0) + 0.12
                sc["spin_a"] = ang
                self._sword(cx - math.cos(ang) * half, cy - math.sin(ang) * half,
                            ang, True)
                if t == sp0:
                    tsb_play("wire", 0.9)
            elif sp0 + 50 <= t < sp0 + 64:
                ang = sc.get("spin_a", 0.0)
                self._sword(cx - math.cos(ang) * half, cy - math.sin(ang) * half,
                            ang, False, alpha=1.0 - (t - sp0 - 50) / 14.0)
            # V. whole camellias, where you were.
            floor = self._floor_y()
            for k, d0 in enumerate((490, 518, 546, 574)):
                if t == d0 - 26:
                    sc["cam_%d" % k] = tsb_clamp(self.px, bx + 26, bx + bw - 26)
                    tsb_play("glint", 0.6)
                dx = sc.get("cam_%d" % k)
                if dx is None:
                    continue
                if d0 - 26 <= t < d0:
                    u = (t - d0 + 26) / 26.0
                    self._scene_sprite("camellia", dx, by + 14, alpha=0.3 + 0.6 * u,
                                       rot=math.sin(t * 0.3) * 10.0)
                    self._scene_ellipse(dx, floor + 4, 10 + 10 * u, 5, 0,
                                        alpha=0.2 + 0.35 * u)
                if t == d0:
                    b = self._add_bullet(dx, by + 14, 0.0, 1.0, kind="camellia",
                                         ay=0.3, ttl=160)
                    if b is not None:
                        b["land"] = {"do": "bloom", "n": 10, "speed": 1.3,
                                     "kind": "petal"}
            # VI. her apology.
            if t == 596:
                self._needle(bx - 10, cy - 20, 1.3, ttl=200)

        def _tag_word(self, word, **fields):
            for b in self.bullets:
                if b.get("word") == word:
                    b.update(fields)

        # ======================================================================
        # TRANSLATION -- "WHAT SHE MEANS"  (Matsu is loud; Tsubaki is the quiet)
        # ======================================================================
        # Matsu's voice fills the room from a megaphone: her proclamations
        # come down as walls of huge ORANGE letters and every one of them
        # rings out as an ORANGE wave -- you can survive Matsu by keeping up
        # with her (keep moving). Tsubaki's own small bubble drifts through
        # the room on a slow figure-eight, and inside it nothing loud can
        # reach you: it translates. The bubble shows what the shout meant
        # ("BEHOLD!" -- "look."). Now and then the bubble goes quiet and pops
        # for a moment; the room rests with it. Once, Matsu stops performing
        # and says her name for real: that wave is CYAN, and you hold still.
        # What the bubble does NOT stop is what Matsu throws: white "!"
        # marks, aimed at where you were.

        MATSU_WORDS = (("BEHOLD!", "look."), ("HEAR ME!", "listen?"),
                       ("KAREDA!", "that's me."), ("WITNESS!", "watch this."),
                       ("THE AZURE EYE!", "her contacts."), ("FEAR NOT!", "it's okay."))

        def _pat_translation(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            sc = self.pat_scratch
            left = (t // 140) % 2 == 0 or t >= 280
            mx = bx + 30 if left else bx + bw - 30
            my = by + 22
            shake = 0.0
            # Tsubaki's translation: a small bubble on a slow figure-eight
            # (never faster than 2 px/tick).
            sx = cx + math.sin(t * 0.011) * (bw * 0.30)
            sy = cy + 16 + math.sin(t * 0.022) * (bh * 0.20)
            popped = (t % 140) >= 118
            self.shelter = None if popped else (sx, sy, 36.0)
            words = TSBGame.MATSU_WORDS
            quiet = t >= 286
            for k, s0 in enumerate(range(24, 260, 70)):
                word, tr = words[k % len(words)]
                if s0 - 26 <= t < s0:
                    u = (t - s0 + 26) / 26.0
                    shake = 2.0 * u
                    self._scene_text(word, cx - len(word) * 12, by + 4, 4, sc=4,
                                     alpha=0.15 + 0.3 * u)
                    if t == s0 - 26:
                        tsb_play("glint", 0.5)
                if t == s0:
                    x0 = cx - len(word) * 12
                    for i, ch in enumerate(word):
                        if ch == " ":
                            continue
                        b = self._add_bullet(x0 + i * 24 + 10, by + 20, 0.0, 1.75,
                                             kind="glyph", ttl=260, rule="orange")
                        if b is not None:
                            b["ch"] = ch
                            b["sc"] = 4
                            b["loud"] = True
                    sc["tr"] = tr
                    sc.setdefault("rings", []).append((t, mx, my, "orange"))
                    tsb_play("volley", 0.8)
                    tsb_play("bloom", 0.5)
            # At the end, Matsu stops performing. Everything loud stops first
            # -- the words and the "!" fade and the orange waves are gone --
            # and only then does the one cyan wave come: hold still. A cyan
            # and an orange hazard are never live together, anywhere: one
            # asks you to move and the other to stop, and both at once is
            # not a pattern, it's a trap.
            if t == 286:
                sc["rings"] = []
                for b in self.bullets:
                    if not b.get("heal"):
                        b["fz"] = 12
                sc["tr"] = "..."
                tsb_play("mend", 0.6)
            if 286 <= t < 312:
                self._scene_circle(mx, my, 20 + (t - 286) * 0.8, ci=9, ghost=True,
                                   alpha=0.5, outline=True)
            if t == 312:
                sc.setdefault("rings", []).append((t, mx, my, "cyan"))
                sc["tr"] = "...Tsuba?"
            for entry in list(sc.get("rings", ())):
                t0, rx, ry, rule = entry
                r = (t - t0) * 2.6 + 8.0
                if r > 520:
                    sc["rings"].remove(entry)
                    continue
                self._scene_ring(rx, ry, r, width=8.0, rule=rule, loud=True)
            # What she throws, the bubble doesn't stop: "!", aimed and stale.
            for k, d0 in enumerate(range(70, 260, 46)):
                if t == d0 - 18:
                    sc["aim_%d" % k] = (tsb_clamp(self.px, bx + 10, bx + bw - 10),
                                        tsb_clamp(self.py, by + 10, by + bh - 10))
                aim = sc.get("aim_%d" % k)
                if aim is None:
                    continue
                if d0 - 18 <= t < d0:
                    self._scene_line(mx, my, aim[0], aim[1], 1, 2, ghost=True,
                                     alpha=0.35)
                if t == d0:
                    b = self._add_aimed(mx, my, aim[0], aim[1], 3.2, kind="glyph",
                                        ttl=240)
                    if b is not None:
                        b["ch"] = "!"
                        b["sc"] = 3
                    tsb_play("throw", 0.45)
            self._scene_sprite("megaphone", mx + (math.sin(t * 1.9) * shake),
                               my, sc=2, flip=not left)
            self._scene_bubble(sx, sy, 36.0, "..." if popped else sc.get("tr", "..."),
                               alpha=0.45 if popped else 1.0)
            if t == 190:
                self._needle(bx - 10, cy + 40, 1.2)

        # ======================================================================
        # CLAW -- "ELEVEN TRIES"  (the claw machine; one try was never enough)
        # ======================================================================
        # The room is the claw cabinet and the SOUL is a prize among the
        # cloth birds. The claw tries for you eleven times. Every try: it
        # slides to where you were (its column is drawn under it), drops,
        # closes, lifts. Where it lands in the pile, a bird is knocked loose
        # and bounces around the glass. The first tries take their time; the
        # later ones don't. On the eleventh, it finally gets the pale yellow
        # bird -- and drops it to you, glowing green. Eleven would have done it.

        # One claw, eleven tries, and a try never starts before the last one
        # has let go: slide (its column drawn), drop, grab. The lift back up
        # happens during the next try's slide, so nothing live is ever left
        # somewhere the claw isn't.
        CLAW_TRIES = (16, 64, 112, 160, 200, 240, 280, 320, 354, 388, 422)

        def _claw_tel(self, k):
            return 30 if k < 3 else (22 if k < 7 else 16)

        def _pat_claw(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            floor = self._floor_y()
            sc = self.pat_scratch
            top = by + 24.0
            if t == 1:
                sc["pile"] = [bx + 30 + k * (bw - 60) / 7.0 for k in range(8)]
                sc["claw_x"] = cx
                sc["claw_y"] = top
            # the gantry and the glass
            self._scene_line(bx + 6, by + 10, bx + bw - 6, by + 10, 3, 7,
                             ghost=True, alpha=0.6)
            for k, x in enumerate(sc.get("pile", ())):
                self._scene_sprite("bird", x, floor + 2, alpha=0.75,
                                   flip=k % 2 == 1)
            tries = TSBGame.CLAW_TRIES
            cur = None
            for k, s0 in enumerate(tries):
                if t == s0:
                    sc["target_%d" % k] = tsb_clamp(self.px, bx + 22, bx + bw - 22)
                    tsb_play("glint", 0.5)
                if s0 <= t:
                    cur = k
            claw_x = sc.get("claw_x", cx)
            claw_y = sc.get("claw_y", top)
            shut = sc.get("shut", False)
            if cur is not None:
                k = cur
                tel = self._claw_tel(k)
                tx = sc["target_%d" % k]
                k_t = t - tries[k]
                if k_t < tel:
                    # sliding over (and up), its column pale under it
                    u = k_t / float(tel)
                    claw_x += tsb_clamp(tx - claw_x, -10.0, 10.0)
                    claw_y += tsb_clamp(top - claw_y, -7.0, 7.0)
                    shut = False
                    self._scene_rect(tx - 14, by + 12, 28, bh - 16, ci=7,
                                     ghost=True, alpha=0.10 + 0.20 * u)
                elif k_t < tel + 10:
                    # the drop: the claw and its cable are live
                    claw_x = tx
                    u = (k_t - tel) / 9.0
                    claw_y = top + (floor - 16.0 - top) * self._ease(u)
                    self._scene_line(tx, by + 10, tx, claw_y - 10, 4, 7, harm=True,
                                     hidden=True)
                    self._scene_circle(tx, claw_y, 10, ci=7, harm=True, hidden=True)
                    if k_t == tel:
                        tsb_play("throw", 0.6)
                elif k_t < tel + 18:
                    # the grab
                    claw_y = floor - 16.0
                    shut = k_t >= tel + 13
                    self._scene_circle(tx, claw_y + 2, 9 if shut else 15, ci=7,
                                       harm=True, hidden=True)
                    if k_t == tel + 13:
                        tsb_play("snap", 0.6)
                        self._grab_pile(tx, floor, k == len(tries) - 1)
                else:
                    claw_y += tsb_clamp(top - claw_y, -4.0, 4.0)
                    shut = True
            sc["claw_x"], sc["claw_y"], sc["shut"] = claw_x, claw_y, shut
            self._scene_line(claw_x, by + 10, claw_x, claw_y - 10, 2, 7, ghost=True,
                             alpha=0.9)
            self._scene_sprite("claw_shut" if shut else "claw_open", claw_x, claw_y,
                               sc=2)
            self._scene_text("TRY %d/11" % ((cur or 0) + 1), bx + 10, by + 16, 8,
                             sc=2, alpha=0.85)

        def _grab_pile(self, x, floor, last):
            sc = self.pat_scratch
            pile = sc.get("pile", [])
            if last:
                # The eleventh try. It gets the bird, and it gives it to you.
                b = self._add_bullet(x, floor - 30, 0.0, -2.0, kind="bird",
                                     heal=True, ay=0.05, ttl=300)
                if b is not None:
                    b["sway"] = 0.6
                    b["mend"] = True
                tsb_play("spare", 0.8)
                self.flash = max(self.flash, 0.12)
                return
            near = [p for p in pile if abs(p - x) < 34]
            if near:
                p = min(near, key=lambda p: abs(p - x))
                pile.remove(p)
                pile.append(self._arena()[0] + 30 + self.rng.random()
                            * (self._arena()[2] - 60))
                b = self._add_bullet(p, floor - 6, (2.0 if p < x else -2.0), -3.2,
                                     kind="bird", ay=0.16, ttl=240)
                if b is not None:
                    b["bounce"] = {"n": 3, "rest": 0.62}
                    b["walls"] = True

        # ======================================================================
        # NOTICING -- "THE NEEDLE OF NOTICING"  (phase 2: she can't not notice)
        # ======================================================================
        # She notices everything, and the act turns it on you. A silver
        # needle follows your own path a second behind you, and the red
        # thread it lays is live: your last two seconds are a wall. Keep
        # moving -- stand still and it arrives -- and don't cross your own
        # trail. Where you lingered it writes a small x in the margin, and the
        # x stays. Halfway, a second needle starts further back, and the first
        # one closes the distance.

        def _pat_noticing(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            sc = self.pat_scratch
            trail = self.trail
            n = len(trail)
            late = t >= 230
            needles = [(58 if late else 72, 100)]
            if late:
                needles.append((150, 70))
            if t < 60:
                # First it only watches: your path, drawn in pencil.
                for i in range(max(0, n - 60), n - 3, 3):
                    x1, y1 = trail[i]
                    x2, y2 = trail[i + 3]
                    self._scene_line(x1, y1, x2, y2, 2, 7, ghost=True,
                                     alpha=0.35 * (i - n + 60) / 60.0)
                if t == 40:
                    tsb_play("glint", 0.6)
            else:
                for (delay, length) in needles:
                    if n <= delay + 2:
                        continue
                    head = trail[n - 1 - delay]
                    tail_i = max(0, n - 1 - delay - length)
                    for i in range(tail_i, n - 1 - delay - 3, 3):
                        x1, y1 = trail[i]
                        x2, y2 = trail[i + 3]
                        fade = (i - tail_i) / float(max(1, length))
                        self._scene_line(x1, y1, x2, y2, 3, 0, ghost=True,
                                         alpha=0.35 + 0.6 * fade)
                        # the thread is live a few ticks behind the needle
                        if i < n - 1 - delay - 9:
                            self._scene_line(x1, y1, x2, y2, 3, 0, harm=True,
                                             hidden=True)
                    prev = trail[max(0, n - 1 - delay - 4)]
                    ang = math.degrees(math.atan2(head[1] - prev[1], head[0] - prev[0]))
                    self._scene_sprite("needle_x", head[0], head[1], rot=ang, sc=2)
                    self._scene_circle(head[0], head[1], 6, ci=2, harm=True,
                                       hidden=True)
                    if t % 24 == 0:
                        tsb_play("blip", 0.3)
                if late and t == 230:
                    tsb_play("snap", 0.7)
                    self.flash = max(self.flash, 0.08)
            # The margin notes: an x where you were a second ago, every so often.
            for k, d0 in enumerate(range(80, 400, 44)):
                if t == d0 and n > 40:
                    sc["note_%d" % k] = trail[n - 40]
                note = sc.get("note_%d" % k)
                if note is None:
                    continue
                if d0 <= t < d0 + 22:
                    self._scene_text("x", note[0] - 5, note[1] - 9, 0, sc=2,
                                     alpha=0.3 + 0.03 * (t - d0))
                if t == d0 + 22:
                    b = self._add_bullet(note[0], note[1], 0.0, 0.0, kind="glyph",
                                         ttl=150)
                    if b is not None:
                        b["ch"] = "x"
                        b["sc"] = 2
                    tsb_play("blip", 0.5)
            if t == 200:
                self._needle(bx - 10, cy, 1.1)

        # ======================================================================
        # APOLOGY -- "I'M S--"  (phase 2: the sentence she can't finish)
        # ======================================================================
        # She tries to apologize and the act keeps cutting the end off. Each
        # attempt is written across the top of the room, drops as a wall,
        # and is struck out -- its letters fall apart -- and she starts over,
        # a little further each time. The lane is always where the sentence
        # hasn't reached yet, and every attempt pushes it toward the wall.
        # When she finally gets it all out, the act strikes the whole thing
        # and writes its own line over it, huge and ORANGE (keep moving
        # through it). Under that, small, in her hand, she writes it back.

        APOLOGY = ("I'M S-", "I'M SOR-", "I'M SORRY, I-", "I'M SORRY, I DIDN'T-",
                   "I'M SORRY, I DIDN'T MEAN TO.")

        def _pat_apology(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            sc = self.pat_scratch
            for k, text in enumerate(TSBGame.APOLOGY):
                w0 = 8 + k * 62
                gsc = 3 if k < 4 else 2
                adv = 6.0 * gsc
                x0 = bx + 8
                y_line = by + 16
                n = len(text)
                write_ticks = min(40, n * 2)
                tag = "ap%d" % k
                if w0 <= t < w0 + write_ticks:
                    kk = int((t - w0) / 2.0) + 1
                    self._scene_text(text[:kk], x0, y_line - 4.5 * gsc, 8, sc=gsc,
                                     alpha=0.55)
                    self._scene_sprite("pen", x0 + adv * min(kk, n) + 10, y_line - 12,
                                       rot=120)
                    if (t - w0) % 4 == 0:
                        tsb_play("blip", 0.45)
                if t == w0 + write_ticks:
                    self._text_line(text, x0, y_line, tag=tag, sc=gsc)
                    self._tag_set(tag, vy=1.5)
                    tsb_play("volley", 0.6)
                st = w0 + write_ticks + 56
                if st <= t < st + 10:
                    body = [b for b in self.bullets if b.get("tag") == tag]
                    if body:
                        yy = body[0]["y"]
                        u = (t - st) / 10.0
                        self._scene_line(x0 - 4, yy, x0 - 4 + (adv * n + 8) * u, yy,
                                         4, 0, ghost=True, alpha=0.95)
                if t == st + 10:
                    for b in self.bullets:
                        if b.get("tag") == tag:
                            b["tag"] = None
                            b["vx"] = self.rng.uniform(-0.7, 0.7)
                            b["ay"] = 0.18
                    tsb_play("snap", 0.6)
            # The act's line, over all of it.
            if 320 <= t < 344:
                u = (t - 320) / 24.0
                self._scene_text("I'M NOT SORRY.", cx - 14 * 12, by + 4, 4, sc=4,
                                 alpha=0.15 + 0.35 * u)
            if t == 344:
                self._text_line("I'M NOT SORRY.", cx - 14 * 12, by + 22, rule="orange",
                                tag="notsorry", sc=4)
                self._tag_set("notsorry", vy=1.8)
                tsb_play("wire", 0.8)
                self.flash = max(self.flash, 0.08)
            # ...and hers, under it: small, harmless, hand-written.
            if 372 <= t < 420:
                kk = min(6, (t - 372) // 3 + 1)
                self._scene_text("(i am)"[:kk], cx - 18, by + 30, 2, sc=2, alpha=0.9)
            if t == 200:
                self._needle(bx + bw + 10, cy + 60, -1.2)

        # ======================================================================
        # TIN -- "WASHED, LABELED, DATED"  (phase 2: where the pieces go)
        # ======================================================================
        # The act cuts pieces off her, and they come down whole, the way a
        # camellia does -- where you were standing. Each one lands and turns
        # into what it was: a paper tag with a word on it. SORRY. EARLY.
        # QUIET. The tags slide along the boards (or leap) to the tin in the
        # middle of the floor, and she keeps them. The open tin PULLS -- on
        # the tags, and on you -- and its mouth is not somewhere to be. Lean
        # away. The lid comes down at the end.

        FLAW_TAGS = ("SORRY", "EARLY", "QUIET", "NOTES", "7:18", "SPARE PEN",
                     "AVERAGE", "ONE TRY", "SIZE", "FINE", "SECOND", "ASK")

        def _pat_tin(self, t, dens):
            bx, by, bw, bh = self._arena()
            cx, cy = bx + bw * 0.5, by + bh * 0.5
            floor = self._floor_y()
            sc = self.pat_scratch
            tx, ty = cx, floor - 8
            open_ = 30 <= t < 384
            self._scene_sprite("tin_open" if open_ else "tin", tx, ty - 2, sc=2)
            if open_:
                # the pull, on the SOUL and in the air
                pull = 0.8 if t < 230 else 1.1
                dx, dy = tx - self.px, (ty - 10) - self.py
                d = math.hypot(dx, dy)
                if d > 24:
                    self.drag_x += dx / d * pull
                    self.drag_y += dy / d * pull
                for k in range(3):
                    r = 20 + ((t * 1.4 + k * 30) % 90)
                    self._scene_circle(tx, ty - 10, r, ci=7, ghost=True,
                                       alpha=0.3 * (1.0 - r / 110.0), outline=True)
                self._scene_circle(tx, ty - 10, 13, ci=0, harm=True, hidden=True)
            if t == 384:
                self._slam(tx, ty - 10, 1.0, 7, "crumb", "snap", 0.9, flash=0.14)
            every = 34 if t < 230 else 26
            if 16 <= t < 360 and (t - 16) % every == 0:
                k = sc.get("n_cam", 0)
                sc["n_cam"] = k + 1
                x = tsb_clamp(self.px + self.rng.uniform(-40, 40), bx + 24, bx + bw - 24)
                sc.setdefault("cams", []).append((t, x, k))
                tsb_play("glint", 0.5)
            for entry in list(sc.get("cams", ())):
                t0, x, k = entry
                age = t - t0
                if age < 24:
                    u = age / 24.0
                    self._scene_sprite("camellia", x, by + 12, alpha=0.3 + 0.6 * u)
                    self._scene_ellipse(x, floor + 4, 8 + 8 * u, 4, 0,
                                        alpha=0.2 + 0.3 * u)
                elif age == 24:
                    b = self._add_bullet(x, by + 12, 0.0, 1.2, kind="camellia",
                                         ay=0.26, ttl=200)
                    if b is not None:
                        b["land"] = {"do": "tag", "label": TSBGame.FLAW_TAGS[
                            k % len(TSBGame.FLAW_TAGS)], "leap": k % 3 == 2}
                    sc["cams"].remove(entry)
            # tags that reach the tin go in
            for b in self.bullets:
                if b["kind"] == "tag" and not b["fz"] and abs(b["x"] - tx) < 14:
                    b["fz"] = 8
                    b["vx"] = b["vy"] = b["ay"] = 0.0
                    tsb_play("coin", 0.4)
            if t == 200:
                self._needle(bx - 10, by + 60, 1.2)

        # ======================================================================
        # LIMP  (the violence route's collapse: nothing left to fight with)
        # ======================================================================
        def _pat_limp(self, t, dens):
            # One slack thread fails to lift, one flower fails to open, and the
            # player is left alone with how little resistance remains.
            bx, by, bw, bh = self._arena()
            fall = self._ease((t - 40) / 210.0)
            fx = bx + bw * 0.62
            fy = by - 20 + (bh + 32) * fall
            self._scene_line(fx, by - 18, fx + 18 * fall, fy - 16,
                             2, 7, ghost=True, alpha=0.38 * (1.0 - fall))
            self._scene_sprite("camellia", fx + 18 * fall, fy, rot=12 * fall,
                               alpha=0.55, tint="#8a90a0")
            if t == 150:
                self._needle(bx - 10, by + bh * 0.55, 0.72, ttl=240)

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
                # At half HP she loses the orderly thread with her footing.
                # The yank restores her position, not her certainty.
                if t == 30:
                    self._bub("Okay. Okay, I'm down. That's-- I'm allowed to be down. Let me stay down a second.", hold=55)
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
                    self._bub("No--DON'T!", hold=24)
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
                    self._bub("It stood me back up. ~I didn't want~ I'm fine. I'm FINE. Why does my mouth keep finishing things?", hold=65)
                if t >= 470:
                    self._after_shift()
            else:
                # Her hand moves toward the open choice before the strings do.
                # The correction leaves her unsure whose decision it was.
                if t == 30:
                    self._bub("My hand moved. Toward you. Before it told me to. Did you see that? I did that.", hold=55)
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
                    self._bub("WAIT--NO!", hold=24)
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
                    self._bub("That wasn't in the script. ~I'm sorry~ --no. Don't cross that out. I meant that one.", hold=50)
                if t == 355:
                    self._bub("It's rewriting me faster now. Talk to me. Say anything. I'll correct it. I'm good at correcting!", hold=55)
                if t >= 500:
                    self._after_shift()
            if t > 30:
                self._reveal_bubble()

        def _after_shift(self):
            self.phase2_start_hp = max(1.0, self.boss_hp)
            self.phase = 2
            self.turn = 0
            self.strings_alpha = 0.74
            self.bubble = None
            self.boss_rot = 0.0
            self.flinch = False
            self.flinch_clear_turn = None
            self.fought_last = False
            # The stage picture grows more crowded in phase 2; the authored
            # attack score itself keeps the same readable rules and spacing.
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
            # Pacifist: the last thread is down. In the sudden quiet she has
            # just enough room to insist on one choice in her own voice.
            t = self.mtick
            self._step_bullets()
            if t == 15:
                self._bub("Wait--wait. Don't answer for me.", hold=34)
            if 15 <= t < 90:
                self.strings_alpha = max(0.0, self.strings_alpha - 0.04)
            if t == 72:
                self._bub("Bookstore first. I wanted bookstore first. Matsu, don't you dare move it.", hold=60)
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
                self._bub("Bookstore first. I wanted--Matsu, don't you da--", hold=30)
            if t == 52:
                self._void_cut()
            if t >= 74:
                self._step_void_fall()
            self._step_end_epilogue(t, "end_b", "victory_b")
            if 30 <= t < 52:
                self._reveal_bubble()

        def _step_dead(self):
            t = self.mtick
            # Everything but the SOUL is gone (the renderer blacks the room
            # out); bullets freeze mid-air and only the shatter advances. The
            # heart shudders, cracks down the middle, and at 46 comes apart
            # into shards that fall out of the black.
            if t == 46:
                self.shards = []
                for i in range(6):
                    self.shards.append({
                        "x": self.px + (i - 2.5) * 2.0, "y": self.py,
                        "vx": self.rng.uniform(-2.4, 2.4),
                        "vy": self.rng.uniform(-3.8, -1.2),
                        "k": "shard_r" if i % 2 else "shard_c"})
                self._spark_burst(self.px, self.py, 18, 0, 4.2, 55, 1.0)
                tsb_play("hurt", 0.8)
            for sh in self.shards:
                sh["x"] += sh["vx"]
                sh["y"] += sh["vy"]
                sh["vy"] += 0.16
            if t == 96 and self.visit_deaths >= 1:
                self._bub("Get up! You were just-- no. I don't know what comes after this part. Get up and show me. Please.", hold=40)
            if t > 96:
                self._reveal_bubble()
            if t == 150:
                self._booth("death")
            if t > 200:
                self.dark = min(1.0, self.dark + 0.015)
            if t >= 270:
                self._finish("defeat")
# --- RENDERER ------------------------------------------------------------------
init python:
    class TSBStage(renpy.Displayable):
        """One creator-defined displayable that steps TSBGame on a fixed 60Hz
        accumulator inside render() and paints the whole fight as cached-
        texture blits. Displayable FACTORIES are cached across frames;
        renpy.Render objects live only inside one render() call.

        THE LOOK (2026-09-29). Undertale's grammar -- the black box, the four
        orange buttons with their icons and the SOUL as the cursor, "* " box
        text that types itself, the FIGHT target and its bar -- in
        Deltarune's clothes: the rising grid behind everything, a mercy gauge
        on her, a speech bubble with a pixel border, and every word set in
        Kareda Mono, the fight's own pixel face. All of it is atlas art drawn
        at integer scale (see THE ART in the constants block); the only
        things still drawn as flat colour are light (wires, strings, flashes)
        and the telegraph ghosts, which are meant to look like light.
        """

        _misc_cache = {}
        _art_cache = {}

        # kind -> (art, scale, turn). art is an atlas key, or a tuple of keys
        # the body walks or spins through (FRAME_TICKS apart); turn is None
        # (upright), "spin" (its own tumble) or "head" (along its flight, or
        # the way it stuck). A cyan/orange rule swaps in the ":w" copy.
        KINDS = {
            "petal":     ("petal", 2, "spin"),
            "camellia":  ("camellia", 2, "spin"),
            "needle":    ("needle", 2, "head"),
            "book_r":    ("book_r", 2, None),
            "book_b":    ("book_b", 2, None),
            "book_g":    ("book_g", 2, None),
            "book_y":    ("book_y", 2, None),
            "book_n":    ("book_n", 2, None),
            "book_v":    ("book_v", 2, None),
            "book_open": (("book_open_a", "book_open_b"), 2, None),
            "page":      ("page", 2, "spin"),
            "pen":       ("pen", 2, "head"),
            "can":       ("can", 2, "spin"),
            "drop":      ("drop", 2, None),
            "coin":      (("coin_a", "coin_b"), 2, None),
            "critter":   (("critter_a", "critter_b"), 2, None),
            "commuter":  (("commuter_a", "commuter_b"), 2, None),
            "bell":      ("bell", 2, None),
            "rice":      ("rice", 2, None),
            "cracker":   ("cracker", 2, "spin"),
            "crumb":     ("crumb", 2, None),
            "chip":      ("crumb", 2, None),
            "spark":     ("spark", 2, None),
            "tag":       ("tag", 2, None),
            "bird":      ("bird", 2, None),
        }
        FRAME_TICKS = {"coin": 6, "critter": 8, "commuter": 10,
                       "book_open": 12}
        FLIPS = ("critter", "commuter")
        BUTTON_ICONS = ("icon_fight", "icon_act", "icon_item", "icon_mercy")
        STRING_TOPS = [140.0, -140.0, -60.0, 60.0, 0.0]

        def __init__(self, game, **kwargs):
            super(TSBStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0

        # ----- cached factories ------------------------------------------------

        def _misc(self, key, builder):
            d = TSBStage._misc_cache.get(key)
            if d is None:
                if len(TSBStage._misc_cache) > 900:
                    TSBStage._misc_cache.clear()
                d = builder()
                TSBStage._misc_cache[key] = d
            return d

        def _art_tf(self, key, sc, rot, flip, tint, ab):
            k = (key, sc, rot, flip, tint, ab)
            d = TSBStage._art_cache.get(k)
            if d is None:
                if len(TSBStage._art_cache) > 1800:
                    TSBStage._art_cache.clear()
                kw = dict(xzoom=(-sc if flip else sc), yzoom=sc, nearest=True)
                if rot:
                    kw["rotate"] = rot
                if tint:
                    kw["matrixcolor"] = TintMatrix(tint)
                if ab < 8:
                    kw["alpha"] = ab / 8.0
                d = Transform(tsb_art(key), **kw)
                TSBStage._art_cache[k] = d
            return d

        def _glyph_tf(self, ch, sc, color, ab):
            k = ("glyph", ch, sc, color, ab)
            d = TSBStage._art_cache.get(k)
            if d is None:
                if len(TSBStage._art_cache) > 1800:
                    TSBStage._art_cache.clear()
                kw = dict(zoom=sc, nearest=True, matrixcolor=TintMatrix(color))
                if ab < 8:
                    kw["alpha"] = ab / 8.0
                d = Transform(tsb_glyph(ch), **kw)
                TSBStage._art_cache[k] = d
            return d

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
            global TSB_SHADER_OK, TSB_ALIVE_OK
            g = self.game

            # F3 profiler (perf.rpy) -- see the note in KTStage.render.
            _perf = MSBF_PERF.on
            _t = msbf_perf_t0() if _perf else 0.0

            # LOW DETAIL (graphics_detail.rpy), read once per frame: the
            # rising streaks and drifting petals go, and the falling camellias
            # hold at phase one's three. The box, the SOUL, every attack, her,
            # her strings and the whole interface draw exactly as on Full.
            low = enter_m_low_detail()

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
                    entry = renpy.render(solid, w, h, st, at)
                    frame_tex[key] = entry
                return entry

            def qa(a):
                # Quantized alpha suffix: sixteen levels, so animated fades
                # reuse a small, bounded set of cached Solids -- and a 0.1
                # ghost still shows instead of rounding down to nothing.
                return "%02x" % (int(round(tsb_clamp(a, 0.0, 1.0) * 15.0)) * 17)

            def outline(layer, color, x, y, w, h, t=2):
                x, y, w, h = int(x), int(y), int(w), int(h)
                if w <= 0 or h <= 0:
                    return
                layer.blit(rect(color, w, t), (x, y))
                layer.blit(rect(color, w, t), (x, y + h - t))
                layer.blit(rect(color, t, h), (x, y))
                layer.blit(rect(color, t, h), (x + w - t, y))

            def art(key, sc=2, rot=0.0, flip=False, tint=None, alpha=1.0):
                ab = int(round(tsb_clamp(alpha, 0.0, 1.0) * 8.0))
                if ab <= 0:
                    return None, (0, 0)
                rq = (int(round(rot / 2.0)) * 2) % 360 if rot else 0
                k = ("art", key, sc, rq, flip, tint, ab)
                entry = frame_tex.get(k)
                if entry is None:
                    r = renpy.render(self._art_tf(key, sc, rq, flip, tint, ab),
                                     1024, 1024, st, at)
                    entry = (r, r.get_size())
                    frame_tex[k] = entry
                return entry

            def art_at(layer, key, x, y, sc=2, rot=0.0, flip=False, tint=None,
                       alpha=1.0):
                r, (w, h) = art(key, sc, rot, flip, tint, alpha)
                if r is not None:
                    layer.blit(r, (int(round(x - w * 0.5)), int(round(y - h * 0.5))))

            def glyph(ch, sc, color, ab):
                k = ("gl", ch, sc, color, ab)
                r = frame_tex.get(k)
                if r is None:
                    r = renpy.render(self._glyph_tf(ch, sc, color, ab),
                                     64, 64, st, at)
                    frame_tex[k] = r
                return r

            def ptext(layer, text, x, y, sc=2, color="#ffffff", alpha=1.0,
                      cols=None, lh=None, shown=None, shadow=None):
                """Kareda Mono. Top-left anchored; `shown` types it out."""
                ab = int(round(tsb_clamp(alpha, 0.0, 1.0) * 8.0))
                if ab <= 0 or not text:
                    return (0, 0)
                lines = tsb_wrap(text, cols) if cols else text.split("\n")
                adv = TSB_GLYPH_ADV * sc
                if lh is None:
                    lh = (TSB_GLYPH_H + 3) * sc
                left = len(text) if shown is None else int(shown)
                for li, ln in enumerate(lines):
                    if left <= 0:
                        break
                    seg = ln[:left]
                    left -= len(ln) + 1
                    yy = int(y + li * lh)
                    for i, ch in enumerate(seg):
                        if ch == " ":
                            continue
                        xx = int(x + i * adv)
                        if shadow:
                            layer.blit(glyph(ch, sc, shadow, ab), (xx + sc, yy + sc))
                        layer.blit(glyph(ch, sc, color, ab), (xx, yy))
                wmax = max(len(ln) for ln in lines) if lines else 0
                return (wmax * adv - sc, len(lines) * lh)

            # HER STRINGS are raster lines on a software Canvas, and a Canvas
            # is drawn on the CPU and uploaded as a texture EVERY frame. It
            # used to be a fixed 1280x420 layer; measured Oct 9 2026, bounding
            # it took phase two from 0.86 to 0.37ms of GPU time at full clocks
            # and from 5.1 to 4.4ms of CPU, for five threads that cover a small
            # part of it. So the commands are COLLECTED and rasterized at the
            # end of the frame into a canvas only as big as what they touch,
            # placed at the same offset inside a holder that keeps the old
            # layer's place in the draw order. Integer offsets do not change
            # what pygame rasterizes, so the picture is the same pixel for
            # pixel (checked against the old path); the old 1280x420 bounds
            # still clip it exactly as before.
            string_cmds = []
            string_holder = [None]

            def string_layer():
                if string_holder[0] is None:
                    layer = renpy.Render(1280, 420)
                    rv.blit(layer, (0, 0))
                    string_holder[0] = layer
                return string_holder[0]

            def line(x1, y1, x2, y2, color, thickness=2):
                string_layer()
                string_cmds.append((False, color, [
                    (int(round(x1)), int(round(y1))),
                    (int(round(x2)), int(round(y2)))],
                    max(1, int(thickness))))

            def polyline(points, color, thickness=2):
                if len(points) >= 2:
                    string_layer()
                    string_cmds.append((True, color,
                        [(int(round(x)), int(round(y))) for x, y in points],
                        max(1, int(thickness))))

            def flush_strings():
                if not string_cmds:
                    return
                if not TSB_STRINGS_BBOX:
                    cv = string_holder[0].canvas()
                    for multi, color, pts, wd in string_cmds:
                        if multi:
                            cv.lines(color, False, pts, wd)
                        else:
                            cv.line(color, pts[0], pts[1], wd)
                    return
                pad = 2 + max(c[3] for c in string_cmds)
                xs = [p[0] for c in string_cmds for p in c[2]]
                ys = [p[1] for c in string_cmds for p in c[2]]
                bx0 = max(0, min(xs) - pad)
                by0 = max(0, min(ys) - pad)
                bx1 = min(1280, max(xs) + pad + 1)
                by1 = min(420, max(ys) + pad + 1)
                if bx1 <= bx0 or by1 <= by0:
                    return
                small = renpy.Render(bx1 - bx0, by1 - by0)
                cv = small.canvas()
                for multi, color, pts, wd in string_cmds:
                    loc = [(x - bx0, y - by0) for x, y in pts]
                    if multi:
                        cv.lines(color, False, loc, wd)
                    else:
                        cv.line(color, loc[0], loc[1], wd)
                string_holder[0].blit(small, (bx0, by0))

            sblit = rv.subpixel_blit
            ending_bg = g.mode in ("end_v", "end_p", "end_b")
            soul_mode = getattr(g, "soul", "red")
            # CHAOS: phase 2 comes apart on screen as it comes apart in her,
            # whichever route is driving it. 0 in phase 1; 0.3 on arrival,
            # climbing to 1.0 with the fight's progress. `glitch` marks the
            # ticks on which things misprint.
            chaos = 0.0
            if g.phase == 2 and not g.void and not ending_bg:
                chaos = 0.3 + 0.7 * tsb_clamp(
                    (float(getattr(g, "ems_progress", 0.5)) - 0.5) * 2.0, 0.0, 1.0)
            elif g.mode == "shift":
                chaos = 0.3 * tsb_clamp((g.mtick - 200) / 60.0, 0.0, 1.0)
            glitch = chaos > 0.0 and (g.tick // 3) % max(3, int(14 - chaos * 9)) == 0

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
                    # The base is the shared TSB_GRID_BASE -- see its note.
                    quad = Transform(TSB_GRID_BASE, xysize=(1280, 720),
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
                for s in (() if low else g.streaks):
                    lq = int(s["len"] // 20) * 20
                    rv.blit(rect(TSB_AMB_PAL[s["ci"]] + streak_alpha,
                                2, max(20, lq)),
                            (int(s["x"]), int(s["y"] - s["len"])))
                amb_a = 0.66 if g.phase == 2 else 0.58
                for m in (() if low else g.amb_petals):
                    quarter = int(m.get("ra", 0.0) // 90.0) % 4
                    art_at(rv, "petal:w", m["x"], m["y"], sc=(2, 2, 3)[m["scb"]],
                           rot=quarter * 90.0, flip=quarter % 2 == 1,
                           tint=TSB_AMB_PAL[m["ci"]], alpha=amb_a)
                # Her flower. A camellia does not wilt; it lets go of the
                # branch all at once and falls whole. A few always are; in
                # phase 2 more of them, faster.
                n_cam = 3 if (g.phase == 1 or low) else 3 + int(round(5 * chaos))
                for k in range(n_cam):
                    hh = (k * 7919 + 13) % 1009
                    spd = 0.35 + (hh % 7) * 0.05 + (0.6 * chaos)
                    yk = ((g.tick * spd + hh * 3.1) % 820.0) - 50.0
                    xk = 40 + (hh * 37) % 1200 + math.sin(g.tick * 0.01 + hh) * 14.0
                    rq = ((g.tick * (1 + hh % 3)) // 14 % 4) * 90.0
                    art_at(rv, "camellia", xk, yk, sc=2, rot=rq,
                           tint=("#a0405a" if (g.phase == 2 and k % 2) else None),
                           alpha=0.5 if g.phase == 1 else 0.62)

            # --- 3. boss sprite + strings --------------------------------------
            motion = tsb_boss_motion(g)
            asset_key = motion["asset_key"]
            img_path = motion["path"]
            bw_ = motion["drawn_w"]
            bh_ = motion["drawn_h"]
            center_x = motion["center_x"]
            center_y = motion["center_y"]
            rot = motion["rotation"]

            warp = motion.get("warp")

            def boss_variant(angle, alpha_bucket=10, tint=None):
                aq = float(round(angle))
                ab = max(0, min(10, int(alpha_bucket)))
                props = dict(xzoom=motion["scale_x"],
                            yzoom=motion["scale_y"], nearest=True,
                            subpixel=False, rotate=aq, rotate_pad=False,
                            matrixcolor=TSB_LINEART_MATRIX,
                            alpha=ab / 10.0)
                if tint is not None:
                    props["matrixcolor"] = (TintMatrix(tint) *
                                            TSB_LINEART_MATRIX)
                if warp is not None and TSB_ALIVE_OK:
                    # Built fresh every frame, never cached: the bend is a set
                    # of uniforms that move continuously, and caching a value
                    # that animates is what quantized the old zoom-breath into
                    # five visible steps. The image's texture is cached by the
                    # engine either way; this is a handful of objects.
                    bands = warp["bands"]
                    props.update(
                        mesh=True, shader="tsb.alive",
                        u_tsa_size=TSB_BOSS_NATIVE_SIZE,
                        u_tsa_bands=(bands[0], bands[1], bands[2], bands[3]),
                        u_tsa_legs=(bands[4], bands[5]),
                        u_tsa_breath=float(warp["breath"]),
                        u_tsa_sway=float(warp["sway"]),
                        u_tsa_head=(float(warp["head"][0]), float(warp["head"][1])),
                        u_tsa_tilt=float(warp["tilt"]),
                        u_tsa_stretch=float(warp["stretch"]),
                        u_tsa_tremor=float(warp["tremor"]))
                    key = ("boss_live", asset_key, aq, ab, tint)
                    # The CHILD is one cached object per image, though, so
                    # the texture the mesh renders it into is reused by
                    # construction (a path string makes a new Image each call;
                    # measured, the engine matched those anyway here -- in
                    # the Matsuda pixel stage it did not; see msbf_px_disp).
                    src = self._misc(("disp", img_path),
                                     (lambda p=img_path: renpy.displayable(p)))
                    return key, Transform(src, **props)
                key = ("boss_pose", asset_key, motion["breath_bucket"],
                       aq, ab, tint)
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

            # THE STRINGS (2026-09-30). Her five threads run up out of the
            # top of the frame to whoever is holding them -- nobody you can
            # see, and nothing in the room ever shows you. They tie on at
            # camellia knots (wrists, head, shoulder, back), a glint runs
            # down each live one, and in phase 2 they redden and fray with
            # the room. A cut thread's lower end hangs from above, loose,
            # and its knot falls, whole.
            twitch = float(motion.get("twitch", 0.0))
            tops = [(TSB_BOSS_X + TSBStage.STRING_TOPS[i]
                     + math.sin(g.tick * 0.026 + i * 1.7) * 6.0 + twitch * 12.0,
                     -40.0) for i in range(5)]
            show_strings = g.strings_alpha > 0.02 and not g.boss_fallen
            if show_strings:
                alpha = tsb_clamp(g.strings_alpha, 0.0, 1.0)
                core_rgb = tsb_mix("#efe8ff", "#ffc8d2", chaos)
                glow_rgb = tsb_mix("#9d8cff", "#ff4f6f", chaos)
                core_col = core_rgb + "%02x" % int((0.35 + 0.6 * alpha) * 255)
                glow_col = glow_rgb + "%02x" % int((0.08 + 0.2 * alpha) * 255)
                for i in range(5):
                    tx, ty = tops[i]
                    if i in g.cut_string_ids:
                        sway = math.sin(g.tick * 0.05 + i * 1.7) * 8.0
                        dangle = [(tx, ty), (tx + sway * 0.4, ty + 60.0),
                                  (tx + sway, ty + 110.0)]
                        polyline(dangle, glow_col, 3)
                        polyline(dangle, core_col, 1)
                        continue
                    ax, ay = anchors[i]
                    bow = math.sin(g.tick * 0.035 + i * 1.31) * (4.0 + 6.0 * alpha)
                    if g.phase == 2:
                        # High-frequency shiver: more load than it admits.
                        bow += math.sin(g.tick * 0.9 + i * 2.3) * (1.5 + 3.0 * chaos)
                    points = [(tx, ty)]
                    segments = 9
                    for seg in range(1, segments + 1):
                        u = seg / float(segments)
                        points.append((tx + (ax - tx) * u + math.sin(math.pi * u) * bow,
                                       ty + (ay - ty) * u))
                    polyline(points, glow_col, 4)
                    polyline(points, core_col, 2)
                    gu = (g.tick * 0.011 + i * 0.23) % 1.0
                    gk = min(segments - 1, int(gu * segments))
                    gp, gq = points[gk], points[gk + 1]
                    line(gp[0], gp[1], gq[0], gq[1], "#ffffffc8", 2)
                    if g.phase == 2 and chaos > 0.35:
                        for fk in range(2):
                            fu = ((i * 0.37 + fk * 0.41 + (g.tick // 20) * 0.13) % 0.8) + 0.1
                            fp = points[min(segments, int(fu * segments))]
                            fl = 4.0 + 5.0 * chaos
                            line(fp[0], fp[1], fp[0] + fl, fp[1] - fl * 0.6,
                                 glow_rgb + "a0", 1)
                            line(fp[0], fp[1], fp[0] - fl * 0.7, fp[1] + fl * 0.4,
                                 glow_rgb + "a0", 1)

            # Severed ends recoil upward and leave a short lower tail, and the
            # knot that tied it falls, whole.
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
                ky = sy + 0.11 * age * age
                if ky < 740.0:
                    art_at(rv, "camellia_s", sx + curl * 0.3, ky, sc=2,
                           rot=((age // 6) % 4) * 90.0)

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

            hit_age = g.tick - g.slash_born
            if g.boss_alpha > 0.0 and twitch and not g.void:
                # The jerk leaves her behind for a frame, misregistered.
                # (Guarded like the main pose: an echo is not worth a crash.)
                try:
                    for off, tcol in ((-7, "#ff4f6f"), (7, "#5cd7ff")):
                        gkey, gd = boss_variant(rot - twitch * 5.0, 3, tcol)
                        gr, (gw, gh) = tex(gkey, gd, 520, 520)
                        rv.blit(gr, (int(round(center_x + off - gw * 0.5)),
                                     int(round(center_y - gh * 0.5))))
                except Exception:
                    pass
            if g.boss_alpha > 0.0:
                main_ab = int(tsb_clamp(g.boss_alpha, 0.0, 1.0) * 10)
                # A landed FIGHT flushes her line art red for a moment.
                tint = None
                if 0 <= hit_age < 8 and not g.void:
                    tint = "#ff6a78"
                pose_key, pose_d = boss_variant(rot, main_ab, tint)
                try:
                    pose_r, (pose_w, pose_h) = tex(pose_key, pose_d, 520, 520)
                except Exception as alive_e:
                    if not (warp is not None and TSB_ALIVE_OK):
                        raise
                    TSB_ALIVE_OK = False
                    try:
                        renpy.log("TSB FX: tsb.alive render failed: %r" % alive_e)
                    except Exception:
                        pass
                    warp = None
                    pose_key, pose_d = boss_variant(rot, main_ab, tint)
                    pose_r, (pose_w, pose_h) = tex(pose_key, pose_d, 520, 520)
                rv.blit(pose_r, (int(round(center_x - pose_w * 0.5)),
                                 int(round(center_y - pose_h * 0.5))))

            # The knots: a small camellia where each live thread ties on.
            if show_strings:
                for i in range(5):
                    if i not in g.cut_string_ids:
                        art_at(rv, "camellia_s", anchors[i][0], anchors[i][1], sc=1)

            # The slash: three frames of a cut across her, and petals.
            if 0 <= hit_age < 18 and not g.void:
                art_at(rv, "slash_%d" % min(2, hit_age // 6),
                       TSB_BOSS_X + 6, TSB_BOSS_FEET_Y - 196, sc=3,
                       alpha=1.0 - max(0.0, (hit_age - 12) / 6.0))
            if 0 <= hit_age < 44 and not g.void:
                for k in range(10):
                    pa_ = k * 0.628 + g.slash_born * 0.37
                    ps_ = 2.0 + (k % 3) * 0.7
                    px_ = TSB_BOSS_X + math.cos(pa_) * ps_ * hit_age
                    py_ = (TSB_BOSS_FEET_Y - 196 + math.sin(pa_) * ps_ * hit_age
                           + 0.06 * hit_age * hit_age)
                    art_at(rv, "petal", px_, py_, sc=2,
                           rot=((hit_age // 5 + k) % 4) * 90.0,
                           alpha=1.0 - hit_age / 44.0)

            # After every fall, one camellia comes down after her, whole, and
            # lands beside her. Same flower, every route.
            if g.void and g.fall_landed and getattr(g, "land_tick", None) is not None:
                cage = g.mtick - g.land_tick - 24
                if cage > 0:
                    cu = tsb_clamp(cage / 80.0, 0.0, 1.0)
                    cyy = -30.0 + (676.0 + 30.0) * (cu * cu)
                    cxx = (TSB_BOSS_X + float(getattr(g, "boss_dx", 0.0)) + 92.0
                           + math.sin(cage * 0.05) * 10.0 * (1.0 - cu))
                    art_at(rv, "camellia", cxx, cyy, sc=2,
                           rot=0.0 if cu >= 1.0 else ((cage // 8) % 4) * 90.0)

            # Her HP bar, only shown after a hit: green over red, and the green
            # DRAINS to the new value instead of snapping (UT's tell).
            if g.tick < g.boss_hp_show_until and not g.void:
                remain = g.boss_hp_show_until - g.tick
                bar_a = tsb_clamp(min((110 - remain) / 7.0, remain / 22.0),
                                0.0, 1.0)
                shown_hp = float(getattr(g, "boss_hp_shown", g.boss_hp))
                frac = tsb_clamp(shown_hp / TSB_BOSS_HP, 0.0, 1.0)
                bbw = 220
                bbx = int(TSB_BOSS_X - bbw * 0.5)
                bby = 8 - int((1.0 - bar_a) * 6)
                rv.blit(rect("#000000" + qa(bar_a), bbw + 4, 18), (bbx - 2, bby - 2))
                rv.blit(rect("#c01020" + qa(bar_a), bbw, 14), (bbx, bby))
                if frac > 0.0:
                    rv.blit(rect("#39e05a" + qa(bar_a), int(bbw * frac), 14),
                            (bbx, bby))

            # --- 3b. mercy gauge (Deltarune's, on her) --------------------------
            # Fills toward the SPARE threshold, then goes yellow and says so.
            # Hidden while the box owns the screen (dodge) and in cinematics.
            m_hide = ("dodge", "intro", "shift", "end_v", "end_p", "end_b", "dead")
            if g.hud_alpha > 0.02 and not g.void and g.mode not in m_hide:
                if g.phase == 1:
                    m_cur, m_need = g.mercy, (1 if g.debug else TSB_MERCY_NEED)
                else:
                    m_cur, m_need = g.mercy2, (1 if g.debug else TSB_MERCY2_NEED)
                m_frac = tsb_clamp(m_cur / float(m_need), 0.0, 1.0)
                m_ready = m_cur >= m_need
                base_boss_w = TSB_BOSS_NATIVE_SIZE[0] * TSB_BOSS_ZOOM
                mgx = int(TSB_BOSS_X + base_boss_w * 0.5 + 16)
                mgy = int(TSB_BOSS_FEET_Y - 50)
                mgw, mgh = 104, 12
                if m_ready:
                    lbl, lcol = "SPARE!", ("#ffff40" if (g.tick // 8) % 2 == 0 else "#fff6c0")
                else:
                    lbl, lcol = "MERCY", "#ffb14a"
                art_at(rv, "camellia_s", mgx - 14, mgy - 15, sc=2)
                ptext(rv, lbl, mgx, mgy - 24, 2, lcol, shadow="#000000")
                pct = "%d%%" % int(round(m_frac * 100))
                ptext(rv, pct, mgx + mgw - len(pct) * 12 + 2, mgy - 24, 2,
                      "#ffffff", shadow="#000000")
                rv.blit(rect("#000000", mgw + 4, mgh + 4), (mgx - 2, mgy - 2))
                rv.blit(rect("#6a3200", mgw, mgh), (mgx, mgy))
                m_fw = int(mgw * m_frac)
                if m_fw > 0:
                    rv.blit(rect("#ffff40" if m_ready else "#ff9d1a", m_fw, mgh),
                            (mgx, mgy))
                    rv.blit(rect("#ffffff60", m_fw, 2), (mgx, mgy))

            # --- 4. the box ----------------------------------------------------
            bxr, byr, bwr, bhr = g._box_rect()
            # Phase shifts use the speech bubble; the empty arena must not
            # cover her feet during the authored downward yank.
            if g.box_alpha > 0.02 and g.mode != "shift":
                bd = TSB_BORDER
                ix, iy, iw, ih = int(bxr), int(byr), int(bwr), int(bhr)
                if g.phase == 2:
                    # The box strains at its seams: a red under-glow on the
                    # same heartbeat as the room.
                    ga = ("26", "3a", "4e", "3a")[(g.tick // 7) % 4]
                    rv.blit(rect("#e13b4e" + ga, iw + bd * 2 + 10, ih + bd * 2 + 10),
                            (ix - bd - 5, iy - bd - 5))
                border = "#ffffff"
                sage = g.tick - getattr(g, "soul_born", -999)
                if g.mode == "dodge" and 0 <= sage < 24 and (sage // 4) % 2 == 0:
                    # A mode change flashes the whole box in the SOUL's colour.
                    border = TSB_SOUL_COL.get(soul_mode, "#ffffff")
                rv.blit(rect(border, iw + bd * 2, ih + bd * 2), (ix - bd, iy - bd))
                rv.blit(rect("#000000", iw, ih), (ix, iy))
                # Deltarune's inner hairline, in her colour.
                outline(rv, ("#ff8fb8" if g.phase == 1 else "#e13b4e") + "38",
                        ix + 3, iy + 3, iw - 6, ih - 6, 1)
                if glitch:
                    dx_ = 2 + int(3 * chaos)
                    outline(rv, "#ff3048a0", ix - bd + dx_, iy - bd, iw + bd * 2,
                            ih + bd * 2, 2)
                    outline(rv, "#30d0ffa0", ix - bd - dx_, iy - bd, iw + bd * 2,
                            ih + bd * 2, 2)
                # A camellia on each corner. In phase 2 they come off, one at
                # a time, as she does.
                lost = 0
                if g.phase == 2:
                    lost = min(4, max(len(g.cut_string_ids), int(
                        (float(getattr(g, "ems_progress", 0.5)) - 0.5) * 9.0)))
                for k, (qx, qy) in enumerate(((ix - bd, iy - bd),
                                              (ix + iw + bd, iy - bd),
                                              (ix + iw + bd, iy + ih + bd),
                                              (ix - bd, iy + ih + bd))):
                    if k >= lost:
                        art_at(rv, "camellia_s", qx, qy, sc=2)

                # --- 5. in-box content ----------------------------------------
                pad = 22
                cols = max(8, int((bwr - pad * 2) / 12) - 2)
                tx0, ty0 = ix + pad, iy + pad - 2
                if g.mode == "menu":
                    # UT exactly: the flavor line owns the box while the four
                    # buttons are live, and it types itself out.
                    fl = g.flavor or ""
                    shown = int(g.mtick * 1.1)
                    if fl in TSB_FLAVOR_ENGINE:
                        # The room's own revision notes: no asterisk, cold.
                        ptext(rv, fl, tx0, ty0, 2, "#8fd3e6", cols=cols + 2,
                              shown=shown)
                    else:
                        ptext(rv, "*", tx0, ty0, 2, "#ffffff")
                        ptext(rv, fl, tx0 + 24, ty0, 2, "#ffffff", cols=cols,
                              shown=shown)
                if g.mode in ("act", "item", "mercy") and g.sub:
                    two_col = len(g.sub) >= 4
                    for i, opt in enumerate(g.sub):
                        if two_col:
                            ox = ix + pad + 18 + (i % 2) * (iw / 2.0 - pad)
                            oyy = ty0 + 2 + (i // 2) * 34
                        else:
                            ox = ix + pad + 18
                            oyy = ty0 + 2 + i * 34
                        col = "#ffffff"
                        if opt == "SPARE":
                            ready = (g.mercy >= (1 if g.debug else TSB_MERCY_NEED)
                                    if g.phase == 1 else
                                    g.mercy2 >= (1 if g.debug else TSB_MERCY2_NEED))
                            if ready:
                                col = "#ffff40"
                        if i == g.sub_i:
                            art_at(rv, "soul_red", ox + 5, oyy + 9, sc=2)
                        else:
                            ptext(rv, "*", ox, oyy, 2, col)
                        ptext(rv, opt, ox + 24, oyy, 2, col)
                    if g.mode == "item" and g.items and g.sub_i < len(g.items):
                        item_key = TSB_ITEMS[g.items[g.sub_i]][0]
                        desc = TSB_ITEM_DESCS.get(item_key, "")
                        if desc:
                            # A hairline rules the description off from the
                            # option grid so it reads as a status footer.
                            rv.blit(rect("#8a90a055", iw - pad * 2, 2),
                                    (ix + pad, iy + ih - 40))
                            ptext(rv, desc, ix + pad, iy + ih - 30, 2, "#9aa0b0")
                elif g.mode == "ptext" and g.page_i < len(g.pages):
                    page = g.pages[g.page_i]
                    shown = int(g.page_shown)
                    if page.isupper() or "  /  " in page:
                        # Readouts stay robotic: no asterisk, cold.
                        ptext(rv, page, tx0, ty0, 2, "#8fd3e6", cols=cols + 2,
                              shown=shown)
                    elif shown > 0:
                        ptext(rv, "*", tx0, ty0, 2, "#ffffff")
                        ptext(rv, page, tx0 + 24, ty0, 2, "#ffffff", cols=cols,
                              shown=shown)
                elif g.mode in ("fight", "strike"):
                    # The target, and the bar that crosses it.
                    tcx, tcy = ix + iw * 0.5, iy + ih * 0.5
                    ta = 1.0
                    if g.mode == "strike":
                        ta = 1.0 - tsb_clamp((g.mtick - 30) / 24.0, 0.0, 1.0)
                    art_at(rv, "target", tcx, tcy, sc=2, alpha=ta)
                    pos = tsb_clamp(g.fight_t / float(TSB_FIGHT_SWEEP), 0.0, 1.0)
                    lx = int(ix + 18 + pos * (iw - 36))
                    core = "#ffffff"
                    if g.mode == "strike" and (g.mtick // 4) % 2 == 1:
                        core = "#000000"
                    if ta > 0.05:
                        rv.blit(rect("#000000", 12, 132), (lx - 6, int(tcy - 66)))
                        rv.blit(rect(core, 8, 128), (lx - 4, int(tcy - 64)))
                        if core == "#000000":
                            outline(rv, "#ffffff", lx - 6, int(tcy - 66), 12, 132, 2)

            # --- 6. the room's contents (drawn over the box, clipped to it) -----
            hazard_layer = renpy.Render(1280, 720)
            hazard_blit = hazard_layer.blit
            hazard_tick = (g.heart_break if g.mode == "dead" and
                            g.heart_break is not None and
                            g.heart_break >= 0 else g.tick)
            clip_x = int(bxr)
            clip_y = int(byr)
            clip_w = max(1, int(bwr))
            clip_h = max(1, int(bhr))
            # One canvas carries every line, ring and shadow in the box. It is
            # reserved first, so all of it sits UNDER the sprites.
            canvas_layer = renpy.Render(clip_w, clip_h)
            hazard_blit(canvas_layer, (clip_x, clip_y))
            cvs = [None]

            def hcv():
                if cvs[0] is None:
                    cvs[0] = canvas_layer.canvas()
                return cvs[0]

            def cpt(x, y):
                return (int(round(x - clip_x)), int(round(y - clip_y)))

            def prop_col(prop, pa):
                rule = prop.get("rule")
                if rule in TSB_RULE_COL:
                    return TSB_RULE_COL[rule] + qa(pa)
                return TSB_PAL[int(prop.get("ci", 2))] + qa(pa)

            scene_props = getattr(g, "scene_props", ()) or ()
            box_floor = byr + bhr - TSB_BORDER

            # Shadows first: where things are going to land.
            for prop in scene_props:
                if prop.get("shape") == "ellipse":
                    rx, ry = prop["rx"], prop["ry"]
                    hcv().ellipse(TSB_PAL[int(prop.get("ci", 0))]
                                  + qa(prop.get("alpha", 0.4)),
                                  (int(prop["x"] - rx - clip_x),
                                   int(prop["y"] - ry - clip_y),
                                   int(rx * 2), int(ry * 2)))
            for b in g.bullets:
                if (b.get("land") is not None or b.get("bounce")) and not b["fz"]:
                    h = box_floor - b["y"]
                    if 0.0 < h < 240.0:
                        u = 1.0 - h / 240.0
                        rx = 4 + int(8 * u)
                        hcv().ellipse("#000000" + qa(0.25 + 0.45 * u),
                                      (int(b["x"] - rx - clip_x),
                                       int(box_floor - 6 - clip_y), rx * 2, 5))
                        hcv().ellipse(TSB_PAL[0] + qa(0.15 + 0.35 * u),
                                      (int(b["x"] - rx - clip_x),
                                       int(box_floor - 6 - clip_y), rx * 2, 5), 1)

            for prop in scene_props:
                if prop.get("shape") != "rect" or prop.get("hidden"):
                    continue
                pw = int(round(prop.get("w", 1)))
                ph = int(round(prop.get("h", 1)))
                if pw <= 0 or ph <= 0:
                    continue
                pa = float(prop.get("alpha", 1.0))
                live = prop.get("harm") and not prop.get("ghost")
                if live:
                    pa = min(1.0, pa + 0.08 *
                             (0.5 + 0.5 * math.sin(hazard_tick * 0.32)))
                x0 = int(round(prop.get("x", 0)))
                y0 = int(round(prop.get("y", 0)))
                if prop.get("outline"):
                    outline(hazard_layer, prop_col(prop, pa), x0, y0, pw, ph, 2)
                else:
                    hazard_blit(rect(prop_col(prop, pa), pw, ph), (x0, y0))
                    if live:
                        outline(hazard_layer, "#ffffff" + qa(0.55 + 0.3 * pa),
                                x0, y0, pw, ph, 2)

            for prop in scene_props:
                shape = prop.get("shape")
                if prop.get("hidden") or shape not in ("line", "circle", "ring"):
                    continue
                if shape == "ring":
                    cr = int(round(prop.get("r", 1.0)))
                    if 1 < cr < 900:
                        hcv().circle(prop_col(prop, 0.85 * float(prop.get("alpha", 1.0))),
                                     cpt(prop["x"], prop["y"]), cr,
                                     max(1, int(round(prop.get("width", 2.0)))))
                    continue
                pa = float(prop.get("alpha", 1.0))
                if prop.get("harm") and not prop.get("ghost"):
                    pa = min(1.0, pa + 0.08 *
                             (0.5 + 0.5 * math.sin(hazard_tick * 0.32)))
                col = prop_col(prop, pa)
                if shape == "line":
                    hcv().line(col, cpt(prop["x1"], prop["y1"]),
                               cpt(prop["x2"], prop["y2"]),
                               max(1, int(round(prop.get("width", 1.0)))))
                else:
                    cr = max(1, int(round(prop.get("r", 1.0))))
                    if prop.get("outline"):
                        hcv().circle(col, cpt(prop["x"], prop["y"]), cr, 2)
                    else:
                        hcv().circle(col, cpt(prop["x"], prop["y"]), cr)

            # Her strings across a strung room: purple, pinned at both walls.
            for s in (getattr(g, "strings_on", None) or ()):
                if not s.get("alive", True):
                    continue
                off = math.sin(hazard_tick * 1.7 + s["id"] * 2.1) * s.get("tremble", 0)
                y0, y1 = s["y0"] + off, s["y1"] + off
                if s.get("fray") and (hazard_tick // 3) % 2 == 0:
                    col = "#ff4f6f"
                else:
                    col = "#c38cff"
                hcv().line(col + "50", cpt(bxr + 4, y0), cpt(bxr + bwr - 4, y1), 6)
                hcv().line(col, cpt(bxr + 4, y0), cpt(bxr + bwr - 4, y1), 2)
                art_at(hazard_layer, "hook", bxr + 9, y0, sc=2)
                art_at(hazard_layer, "hook", bxr + bwr - 9, y1, sc=2, flip=True)

            # Wires: telegraph draws itself across the box behind a bright tip,
            # snaps live with a flash, then cools. Collision stays exactly
            # inside [tel, tel + on].
            p2live = g.phase == 2 and not g.void
            for w in g.wires:
                age = hazard_tick - w["born"]
                tel = w["tel"]
                on = w["on"]
                wc = TSB_PAL[w["ci"]]
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
                prog = tsb_clamp(age / max(6.0, tel * 0.45), 0.0, 1.0)
                prog = prog * prog * (3.0 - 2.0 * prog)
                urgency = tsb_clamp((age / float(max(tel, 1)) - 0.55) / 0.45,
                                    0.0, 1.0)
                tel_a = 0.18 + 0.12 * (0.5 + 0.5 * math.sin(age * 0.23)) + 0.3 * urgency
                snap_k = age - tel
                jig = (math.sin(hazard_tick * 0.9 + w["born"] * 0.7) * 1.6
                       if p2live else 0.0)
                if w["orient"] in ("h", "v"):
                    vert = w["orient"] == "v"
                    span = int(max(0.0, (bhr if vert else bwr) - 8))
                    if span <= 1:
                        continue
                    a0 = int((byr if vert else bxr) + 4)
                    c = w["pos"] + jig

                    def bar(thick, col, start=0, length=span):
                        thick = max(1, int(thick))
                        if vert:
                            hazard_blit(rect(col, thick, length),
                                        (int(c - thick * 0.5), a0 + start))
                        else:
                            hazard_blit(rect(col, length, thick),
                                        (a0 + start, int(c - thick * 0.5)))
                    if wmode == "live":
                        bar(10 + max(0, 8 - snap_k * 2), wc + "66")
                        if snap_k < 5:
                            bar(16, "#ffffff" + qa(0.8 - snap_k * 0.15))
                        if not p2live or (age // 5) % 2:
                            bar(3, "#ffffff")
                    elif wmode == "tel":
                        dl = int(span * prog)
                        if dl > 1:
                            if w["born"] % 2 == 0:
                                bar(2, wc + qa(tel_a), 0, dl)
                            else:
                                bar(2, wc + qa(tel_a), span - dl, dl)
                        if prog < 1.0:
                            tip = dl if w["born"] % 2 == 0 else span - dl
                            bar(6, "#ffffff" + qa(0.75), max(0, tip - 3), 6)
                    else:
                        bar(3 if aa > 0.5 else 2, wc + qa(0.30 * aa))
                        bar(1, "#ffffff" + qa(0.5 * aa))
                else:
                    x1, y1 = w["x1"], w["y1"]
                    x2, y2 = w["x2"], w["y2"]
                    width2 = max(2, int(round(w.get("width", 5.0))))
                    if wmode == "live":
                        hcv().line(wc + "55", cpt(x1, y1 + jig), cpt(x2, y2 + jig),
                                   width2 * 2)
                        hcv().line("#ffffff", cpt(x1, y1), cpt(x2, y2),
                                   max(2, width2 // 2))
                    elif wmode == "tel":
                        ex = x1 + (x2 - x1) * prog
                        ey = y1 + (y2 - y1) * prog
                        hcv().line(wc + qa(tel_a), cpt(x1, y1 + jig),
                                   cpt(ex, ey + jig), 2)
                    else:
                        hcv().line(wc + qa(0.30 * aa), cpt(x1, y1), cpt(x2, y2), 2)

            # Scenery sprites (the shelf, the sword, the clock, a card...).
            for prop in scene_props:
                if prop.get("shape") != "sprite":
                    continue
                key = prop["key"]
                if not tsb_has_art(key):
                    continue
                art_at(hazard_layer, key, prop["x"], prop["y"],
                       sc=prop.get("sc", 2), rot=prop.get("rot", 0.0),
                       flip=prop.get("flip", False), tint=prop.get("tint"),
                       alpha=prop.get("alpha", 1.0))
            # Her small bubble: the translation, and the quiet inside it.
            for prop in scene_props:
                if prop.get("shape") != "bubble":
                    continue
                pa = float(prop.get("alpha", 1.0))
                bxp, byp, br = prop["x"], prop["y"], prop["r"]
                c0 = cpt(bxp, byp)
                hcv().circle("#ffffff" + qa(0.13 * pa), c0, int(br))
                hcv().circle("#ffffff" + qa(0.9 * pa), c0, int(br), 2)
                hcv().polygon("#ffffff" + qa(0.9 * pa),
                              [cpt(bxp - br * 0.5, byp + br * 0.8),
                               cpt(bxp - br * 0.2, byp + br * 0.96),
                               cpt(bxp - br * 0.9, byp + br * 1.3)])
                txt = prop.get("text", "")
                if txt:
                    ptext(hazard_layer, txt, bxp - len(txt) * 3 + 1, byp - 4, 1,
                          "#ffffff", alpha=pa)

            # Words written in the room (the list's pen, CONTINUE?, a stop).
            for prop in scene_props:
                if prop.get("shape") == "text":
                    ptext(hazard_layer, prop["text"], prop["x"], prop["y"],
                          prop.get("sc", 2), TSB_PAL[int(prop.get("ci", 2))],
                          alpha=prop.get("alpha", 1.0))

            for bl in g.blooms:
                p = tsb_clamp((hazard_tick - bl["born"]) /
                                float(bl["fuse"]), 0.0, 1.0)
                art_at(hazard_layer, "camellia", bl["x"], bl["y"],
                       sc=1 + int(p * 2.0), rot=p * 90.0, alpha=0.3 + 0.6 * p)

            # The bodies.
            for b in g.bullets:
                if b.get("heal") and not b["fz"]:
                    hcv().circle("#39d97e" + qa(0.20 + 0.10 * math.sin(
                        hazard_tick * 0.2 + b["ph"])), cpt(b["x"], b["y"]), 15)
            for b in g.bullets:
                kind = b["kind"]
                a = 1.0
                if b["fz"]:
                    a = min(1.0, b["fz"] / 12.0)
                elif b["age"] < 6:
                    # Materialize in quick steps; nothing pops in at full
                    # presence.
                    a = 0.35 + b["age"] * 0.11
                rule = b.get("rule")
                flick = b.get("flicker")
                if flick and (hazard_tick // 4) % 2 == 0:
                    rule = flick
                jit = b.get("jit", 0)
                jx = jy = 0
                if jit:
                    jx = ((hazard_tick * 7 + int(b["ph"] * 10)) % 3 - 1) * jit
                    jy = ((hazard_tick * 5 + int(b["ph"] * 17)) % 3 - 1) * jit
                bxp, byp = b["x"] + jx, b["y"] + jy
                if kind == "glyph":
                    gsc = int(b.get("sc", 3))
                    gcol = TSB_RULE_COL.get(rule, "#ffffff")
                    ptext(hazard_layer, b.get("ch", "?"),
                          bxp - TSB_GLYPH_W * gsc * 0.5,
                          byp - TSB_GLYPH_H * gsc * 0.5, gsc, gcol, alpha=a)
                    continue
                spec = TSBStage.KINDS.get(kind) or TSBStage.KINDS["crumb"]
                akey, sc, turn = spec
                if isinstance(akey, tuple):
                    ft = TSBStage.FRAME_TICKS.get(kind, 8)
                    akey = akey[(b["age"] // ft) % len(akey)]
                rot_ = 0.0
                if turn == "spin":
                    rot_ = b["rb"] * TSB_ROT_DEG
                elif turn == "head":
                    hx, hy = b.get("dir") or (b["vx"], b["vy"])
                    if hx or hy:
                        rot_ = (int(round(math.degrees(math.atan2(hy, hx))
                                          / TSB_ROT_DEG)) * TSB_ROT_DEG)
                flip = kind in TSBStage.FLIPS and b["vx"] < 0.0
                tint = None
                if rule in TSB_RULE_COL:
                    tint = TSB_RULE_COL[rule]
                    if tsb_has_art(akey + ":w"):
                        akey = akey + ":w"
                elif b.get("tint") is not None and tsb_has_art(akey + ":w"):
                    akey = akey + ":w"
                    tint = TSB_AMB_PAL[int(b["tint"])]
                art_at(hazard_layer, akey, bxp, byp, sc=sc, rot=rot_, flip=flip,
                       tint=tint, alpha=a)
                if kind == "tag" and b.get("label"):
                    lab = b["label"]
                    ptext(hazard_layer, lab, bxp + 4 - len(lab) * 3, byp - 4, 1,
                          "#3a2a10", alpha=a)
                if kind == "needle" and (hazard_tick + int(b["ph"] * 10)) % 24 < 6:
                    # Her mending glints at the eye.
                    art_at(hazard_layer, "sparkle", bxp - 12.0 * (1 if b["vx"] >= 0 else -1),
                           byp, sc=2, tint="#9dffc0", alpha=0.9 * a)

            # The tape runs backward: scan bars climb the box, and the whole
            # room takes a cold cast, until the stamp comes down.
            if getattr(g, "rewinding", False) and g.mode == "dodge":
                hazard_blit(rect("#5cd7ff" + qa(0.07), clip_w, clip_h),
                            (clip_x, clip_y))
                for i in range(5):
                    yy = clip_y + (clip_h - ((hazard_tick * 7 + i * 61) % clip_h))
                    hazard_blit(rect("#ffffff" + qa(0.10), clip_w, 3),
                                (clip_x, int(yy)))
                if (hazard_tick // 10) % 2 == 0:
                    art_at(hazard_layer, "rewind", clip_x + 24, clip_y + 18, sc=3)
                    ptext(hazard_layer, "REW", clip_x + 42, clip_y + 9, 2, "#ffffff")

            # Crop the hazard canvas to the box. This is a CLIP FLAG on a one-
            # child wrapper, not Render.subsurface: subsurface walks every child
            # of the layer and builds a fresh cropped Render around each (over a
            # thousand throwaway Render objects a frame at the bullet cap) to
            # produce pixels identical to these three lines. gl2 turns
            # xclipping/yclipping into a clip polygon for free.
            clipped_hazards = renpy.Render(clip_w, clip_h)
            clipped_hazards.xclipping = True
            clipped_hazards.yclipping = True
            clipped_hazards.blit(hazard_layer, (-clip_x, -clip_y))
            rv.blit(clipped_hazards, (clip_x, clip_y))

            # --- 7. sparks ------------------------------------------------------
            for sp in g.sparks:
                frac = sp["age"] / float(sp["ttl"])
                art_at(rv, "spark" if frac < 0.5 else "spark_s", sp["x"], sp["y"],
                       sc=2, tint=TSB_AMB_PAL[sp["ci"]],
                       alpha=0.95 - 0.7 * frac)

            # --- 8. the SOUL ----------------------------------------------------
            skey = TSB_SOUL_ART.get(soul_mode, "soul_red")
            if g.mode == "dodge" and g.heart_break is None:
                blink = g.tick < g.inv_until and (g.tick // 4) % 2 == 0
                if not blink:
                    art_at(rv, skey, g.px, g.py, sc=2)
                sage = g.tick - getattr(g, "soul_born", -999)
                if 0 <= sage < 18:
                    # A mode change rings out from the SOUL.
                    ring = renpy.Render(96, 96)
                    ring.canvas().circle(TSB_SOUL_COL.get(soul_mode, "#ffffff")
                                         + qa(1.0 - sage / 18.0), (48, 48),
                                         int(8 + sage * 2.2), 2)
                    rv.blit(ring, (int(g.px - 48), int(g.py - 48)))

            # --- 9. damage pops -------------------------------------------------
            for p in g.dmg_pops:
                age = g.tick - p["born"]
                # Up fast, a little settle, hold, then fade.
                rise = min(age, 12) * 2.0 - max(0, min(age, 20) - 12) * 0.5
                pa = 1.0 - tsb_clamp((age - 50) / 20.0, 0.0, 1.0)
                psc = 3 if p["big"] else 2
                txt = p["txt"]
                ptext(rv, txt, p["x"] - len(txt) * TSB_GLYPH_ADV * psc * 0.5,
                      p["y"] - rise, psc, TSB_PAL[p["ci"]], alpha=pa,
                      shadow="#000000")

            # --- 10. her speech bubble -----------------------------------------
            # White, a 2px pixel border with notched corners, and a stepped
            # tail pointing back at her. Text between ~tildes~ is her line
            # being revised: it types, and then it is struck out in red. In
            # phase 2 the bubble misprints (a red and a cyan ghost of every
            # letter, off register) and jumps when the room glitches.
            def draw_bubble_text(text, x, y, cols, lh, shown, color, ghosts):
                plain, struck, ends = tsb_strike_parse(text)
                lines = tsb_wrap(plain, cols)
                adv = TSB_GLYPH_ADV * 2
                idx = 0
                left = shown
                for li, ln in enumerate(lines):
                    if left <= 0:
                        break
                    yy = int(y + li * lh)
                    for i, ch in enumerate(ln[:left]):
                        gi = idx + i
                        xx = int(x + i * adv)
                        hit = gi < len(struck) and struck[gi]
                        if ch != " ":
                            for gdx, gcol in ghosts:
                                rv.blit(glyph(ch, 2, gcol, 3), (xx + gdx, yy))
                            rv.blit(glyph(ch, 2, "#b0303e" if hit else color, 8),
                                    (xx, yy))
                        if hit and shown > ends[gi] + 3:
                            rv.blit(rect("#e13b4e", adv, 3), (xx - 1, yy + 8))
                    idx += len(ln) + 1
                    left -= len(ln) + 1

            if g.bubble is not None and g.mode != "dead":
                shown = int(g.bub_shown)
                if shown > 0:
                    bub_w = 352
                    bcols = (bub_w - 32) // 12
                    blines = tsb_wrap(tsb_strike_parse(g.bubble)[0], bcols)
                    blh = 22
                    bub_h = len(blines) * blh + 26
                    bub_x = 800
                    bub_y = 92
                    if glitch:
                        bub_x += int(math.sin(g.tick * 1.3) * 7.0 * chaos)
                        bub_y += int(math.cos(g.tick * 1.1) * 4.0 * chaos)
                    rv.blit(rect("#00000070", bub_w, bub_h), (bub_x + 5, bub_y + 6))
                    rv.blit(rect("#000000", bub_w - 4, bub_h), (bub_x + 2, bub_y))
                    rv.blit(rect("#000000", bub_w, bub_h - 4), (bub_x, bub_y + 2))
                    rv.blit(rect("#ffffff", bub_w - 8, bub_h - 4), (bub_x + 4, bub_y + 2))
                    rv.blit(rect("#ffffff", bub_w - 4, bub_h - 8), (bub_x + 2, bub_y + 4))
                    # The tail: rows of a left-pointing triangle, each row's
                    # first two pixels black, so its edge is a pixel stair.
                    tail_y = bub_y + 30
                    for r in range(-7, 8):
                        tl = 16 - abs(r) * 2
                        yy = tail_y + r * 2
                        rv.blit(rect("#000000", tl + 2, 2), (bub_x - tl, yy))
                        if abs(r) < 7:
                            rv.blit(rect("#ffffff", tl + 2, 2), (bub_x - tl + 2, yy))
                    rv.blit(rect("#ffffff", 4, 26), (bub_x, tail_y - 12))
                    ghosts = ()
                    if chaos > 0.0:
                        m_ = 1 + int(round(2 * chaos)) + (2 if glitch else 0)
                        ghosts = ((-m_, "#ff3048"), (m_, "#20c8ff"))
                    draw_bubble_text(g.bubble, bub_x + 16, bub_y + 14, bcols, blh,
                                     shown, "#101014", ghosts)

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

                nm = "YOU   LV 1"
                if glitch:
                    ptext(rv, nm, 152 + int(2 * chaos), 590, 2, "#ff3048", alpha=0.6)
                ptext(rv, nm, 150, 590, 2, "#ffffff")
                ptext(rv, "HP", 506, 594, 2, "#ffffff")
                hp_w = 120
                rv.blit(rect("#c80000", hp_w, 20), (546, 590))
                ghost = tsb_clamp(float(getattr(g, "hp_shown", g.hp)) / TSB_HP_MAX,
                                  0.0, 1.0)
                frac2 = tsb_clamp(g.hp / TSB_HP_MAX, 0.0, 1.0)
                if ghost > frac2:
                    # What the last hit took, draining after it.
                    rv.blit(rect("#ff8fb8", int(hp_w * ghost), 20), (546, 590))
                if frac2 > 0.0:
                    rv.blit(rect("#ffff40", int(hp_w * frac2), 20), (546, 590))
                hpt = "%d / %d" % (int(math.ceil(g.hp)), int(TSB_HP_MAX))
                ptext(rv, hpt, 682, 591, 2, "#ffffff")

                # The four buttons. You know the four buttons.
                btn_w, btn_h, gap = 232, 54, 30
                total = btn_w * 4 + gap * 3
                x0 = (1280 - total) // 2
                y0 = 626
                in_btn_row = g.mode == "menu"
                for i, label in enumerate(TSBGame.BUTTONS):
                    bx3 = x0 + i * (btn_w + gap)
                    sel = in_btn_row and i == g.menu_i
                    col = "#ffff40" if sel else "#ff8c2e"
                    if sel:
                        rv.blit(rect("#ffff4024", btn_w + 10, btn_h + 10),
                                (bx3 - 5, y0 - 5))
                    rv.blit(rect(col, btn_w, btn_h), (bx3, y0))
                    rv.blit(rect("#000000", btn_w - 6, btn_h - 6), (bx3 + 3, y0 + 3))
                    icx, icy = bx3 + 32, y0 + btn_h * 0.5
                    if sel:
                        # UT exactly: the SOUL takes the icon's place.
                        art_at(rv, "soul_red", icx, icy, sc=3)
                    else:
                        art_at(rv, TSBStage.BUTTON_ICONS[i], icx, icy, sc=3,
                               tint=col)
                    lw = len(label) * TSB_GLYPH_ADV * 3 - 3
                    lx = bx3 + 58 + (btn_w - 58 - 10 - lw) // 2
                    ptext(rv, label, lx, y0 + (btn_h - TSB_GLYPH_H * 3) // 2, 3, col)

            # --- 12. booth line (Matsuda, watching) -----------------------------
            # Left of her, the way her bubble is right of her: two people
            # talking past the girl in the middle.
            def draw_booth():
                if g.booth is None:
                    return
                bage = g.tick - g.booth["born"]
                if bage >= 300:
                    return
                txt = g.booth.get("text", TSB_BOOTH.get(g.booth["key"], ""))
                if not txt:
                    return
                fade = 1.0 if bage < 240 else max(0.0, 1.0 - (bage - 240) / 60.0)
                name, body = (txt.split(": ", 1) if ": " in txt else ("", txt))
                if name:
                    ptext(rv, name, 26, 18, 2, "#ff9c3d", alpha=fade,
                          shadow="#000000")
                ptext(rv, body, 26, 44, 2, "#ffe23d", alpha=fade,
                      cols=40, lh=22, shown=int(bage * 1.6), shadow="#000000")

            if g.mode != "dead":
                draw_booth()

            # PHASE 2 TEARS. On the worst glitch ticks a band of the whole
            # picture slips sideways, the way a bad print tears off register.
            if chaos > 0.45 and g.mode != "dead" and not g.paused:
                period = int(190 - 120 * chaos)
                ph_ = g.tick % max(40, period)
                if ph_ < 5:
                    seed = (g.tick // max(40, period)) * 2654435761
                    ty0 = 60 + seed % 560
                    th_ = 18 + (seed // 7) % 46
                    tdx = (8 + (seed // 11) % 16) * (1 if seed % 2 else -1)
                    root = renpy.Render(1280, 720)
                    root.blit(rv, (0, 0))
                    band = renpy.Render(1280, th_)
                    band.xclipping = True
                    band.yclipping = True
                    band.blit(rv, (int(tdx * chaos), -ty0))
                    root.blit(band, (0, ty0))
                    rv = root

            # THE DEATH. Undertale's: the room goes black at once -- grid,
            # box, her, everything -- and the only thing left is the SOUL,
            # cracking, then breaking. Then the words, and GAME OVER.
            if g.mode == "dead" and g.heart_break is not None:
                rv.blit(rect("#000000", 1280, 720), (0, 0))
                age = g.tick - g.heart_break
                if age < 16:
                    art_at(rv, "soul_red", g.px + ((age % 2) * 2 - 1), g.py, sc=2)
                elif age < 46:
                    art_at(rv, "soul_left", g.px - 2, g.py, sc=2)
                    art_at(rv, "soul_right", g.px + 2, g.py, sc=2)
                for sh in (getattr(g, "shards", None) or ()):
                    art_at(rv, sh["k"], sh["x"], sh["y"], sc=3)
                if age > 110:
                    ga_ = tsb_clamp((age - 110) / 40.0, 0.0, 1.0)
                    ptext(rv, "GAME", 548, 180, 8, "#ffffff", alpha=ga_)
                    ptext(rv, "OVER", 548, 270, 8, "#ffffff", alpha=ga_)
                if g.bubble is not None and int(g.bub_shown) > 0:
                    ptext(rv, g.bubble, 360, 470, 2, "#ffffff", cols=46, lh=24,
                          shown=int(g.bub_shown))
                draw_booth()

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

            # The pause plate is a screen (tsb_pause_panel), because a CDD
            # cannot hold a draggable widget and the panel carries the audio
            # mixer. The wash below is all that is left of it in here.
            if g.paused:
                rv.blit(rect("#000000b8", 1280, 720), (0, 0))

            # Rasterize the strings collected above (see HER STRINGS).
            flush_strings()

            # THE DRAW RATE IS THE TICK RATE. Every pixel this method produces
            # is a pure function of g.tick, so between two simulation ticks the
            # stage draws a byte-identical picture. Handing redraw() the time
            # until the NEXT tick lets the engine wake us exactly when there is
            # something new to draw, so above 60Hz the cost of this stage stops
            # scaling with the refresh rate.
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
# These are the SAME `Preference("...volume")` bars the Settings screen and the
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

    if persistent.tsubamode_attempts == 0:
        ma "She's in there. Tsuba, look at me. Just turn your head."
        ma "...Nothing. Damn it."
        ma "That handle wasn't there five seconds ago. I don't know what it wants you to do, and I hate that it gave you a choice before it gave me one."
    else:
        ma "Same light. Same silhouette. She's still not looking at me."
        ma "And the handle's back. Of course it is."

    menu:
        "Open the door.":
            pass
        "Open the door. {size=-8}(DEV: fast routes){/size}" if config.developer:
            $ tsb_debug = True
            ma "{size=-8}Fine, but the record's in pencil.{/size}"
        "Leave it shut.":
            if persistent.tsubamode_attempts == 0:
                ma "Yeah. Okay. Good. I mean--no, I don't know if it's good. Just don't open it."
                ma "The light's staying on. I'll be right here. Pick somebody else."
            else:
                ma "Okay. Don't touch it. I'll keep watching her. Who else?"
            jump msbf_roster_choice

    if persistent.tsubamode_attempts == 0:
        ma "Breaker won't answer. Booth won't answer. Nothing in there will answer me."
        ma "Arrows or WASD move. Z confirms. X backs out. Hold Shift when you need smaller steps."
        ma "Keep her talking, okay? Tsuba corrects people when she's scared and still following."
        ma "If she stops--no. Don't tell me. Just make her argue with you. Make her tell somebody they're wrong."
    else:
        ma "You know the controls. Make her argue with you. Make her say I'm wrong about something. I'll be here."

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
        ma "The room reset before the door even shut. She said sorry to the empty box. Then she said it again, neater."
    elif tsb_run_deaths == 2:
        ma "Again. Okay. Breathe. You're here."
        ma "While you were out, she asked the ceiling what came next. It answered before she finished asking."
    else:
        ma "She was watching the door before it opened. Damn it, I don't know whether she was waiting for you or for the cue."
        ma "I am not teaching her those are the same thing."

    menu:
        "Send me back in.":
            ma "Booth's still live. Make her argue with you in there. Go."
            scene black with dissolve_scene_full
            jump tsubamode_fight
        "I need to stop.":
            ma "Okay. Stop means stop."
            ma "The light is still on. I'll stay with it and work the breaker."
            return

label tsubamode_quit:
    $ tsb_retry = True
    pause 0.5
    ma "You found my side door. Good. That's the only exit in there I recognize."
    ma "She's still inside, practicing going first. I'll keep working the breaker."

    menu:
        "Put me back in.":
            ma "All right. Ask her something first this time. Go."
            scene black with dissolve_scene_full
            jump tsubamode_fight
        "I can't look at it right now.":
            ma "Then don't. I'll stay here."
            ma "I'll call if the light or her silhouette changes."
            return

label tsubamode_victory_v:
    pause 2.0
    scene bg matsudavr with dissolve_scene_full
    show matsuda shocked at t11 zorder 2

    ma "..."
    ma "No. I--no. I watched you swing after she stopped aiming."
    ma "I kept waiting for the hit that would make sense of the one before it. There wasn't one."
    show matsuda worried
    ma "Maybe the strings looked like the target from inside. Maybe you thought one more hit would reach past her."
    ma "I don't know. I wasn't in the box. So I'm giving you that. I'm trying really, really hard to give you that."
    show matsuda angry
    ma "But her attack was ZERO! You saw it! And by the end her eyes were closed while her hands kept moving!"
    ma "Don't explain it right now. If I hear the wrong word, I am going to say something I can't reset."
    show matsuda sad
    ma "Let me put her back together. Then get out of my booth. Please."

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
    ma "Tsuba? Hey--hey, they're down! All five, I counted! You can move now!"
    ma "Tsuba?"
    pause 1.0
    ma "...Why isn't she getting up?"
    ma "No. Her legs gave out. That's all. Give her a second."
    pause 1.0
    ma "No strings. No marks. Nothing is touching her."
    ma "You did it right. We did it right. I counted every cut!"
    ma "So this is NOT the same. Don't--don't look at me like it's the same!"
    pause 1.5
    ma "The reset will give her the second we didn't get. She'll stand up there. She has to."
    ma "Leave the door open. Don't you dare close it."

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
    ma "Four strings."
    ma "You cut four strings, waited until she was asking you what came next, and then chose FIGHT."
    ma "Do NOT tell me you slipped. The menu asked you twice. You had to move your hand there."
    ma "You made her trust the quiet. You made me trust it! Then you used the exact second she reached for you."
    pause 1.0
    ma "There is no version of this I can misunderstand for you. No strings looked like the target. No last hit was meant to save her."
    ma "You wanted to see what would happen."
    ma "Well, you saw it. She fell. Same as every other route. You did all of that for NOTHING!"
    ma "Get out. I'm not resetting her with you standing there. Get out of my booth."
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
