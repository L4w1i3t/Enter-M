# Painted architecture and phase-specific motion shared by both Seer fights.
# This is presentation only: battle timers, RNG, action economy and saves live
# in their existing owners. UI materials are initialized after this path.
init -15 python:
    MSBF_SEER_ART = "addons/Matsuda's Sick Boss Fight/art/seer/"
    MSBF_SEER_PLATES = {
        1: MSBF_SEER_ART + "arena_cyan.webp",
        2: MSBF_SEER_ART + "arena_gold.webp",
        3: MSBF_SEER_ART + "arena_rupture.webp",
    }

    def msbf_seer_plate(phase=1):
        return MSBF_SEER_PLATES.get(min(3, max(1, int(phase))), MSBF_SEER_PLATES[1])

    # Author-supplied tempo. The instrumental keeps playing under the vocal
    # crossfade, so it is the stable clock for the film's fracture accents.
    MSBF_SEER_RUPTURE_BPM = 107.0
    # The local stems' first strong waveform onset is ~1.26 s after file start.
    # This anchors the tempo grid; it is not a hand-scored map of every drum hit.
    MSBF_SEER_RUPTURE_DOWNBEAT = 1.26

    def msbf_seer_score_clock(trans, st, at):
        # Presentation-only read: no music transport, battle RNG or store writes.
        # A missing/muted device still gets animated, tempo-matched scenery.
        position = renpy.music.get_pos(channel=MSBF_IDMODE_PHASE3_INST_CHANNEL)
        trans.u_seer_score = st if position is None else position - MSBF_SEER_RUPTURE_DOWNBEAT
        return 1.0 / 60.0

    # Authored paths only. No screen-time randomness or gameplay clock writes.
    # x, y, travel-x, travel-y, seconds, stagger, native display size.
    MSBF_SEER_PATHS = {
        1: ((1320,220,-1450,120,2.2,0.0,18), (1410,355,-1510,-70,2.7,0.3,27),
            (1360,465,-1470,-155,2.0,0.8,15), (1290,165,-1380,130,3.0,0.1,13),
            (1330,555,-1420,-140,2.4,0.6,25), (1370,302,-1490,54,1.8,1.0,11),
            (1390,410,-1500,-35,2.9,1.1,20), (1340,92,-1450,192,2.5,0.5,12),
            (1320,510,-1440,-40,1.9,0.2,14), (1400,260,-1530,60,2.6,1.3,23)),
        2: ((205,620,55,-650,4.8,0.0,10), (382,575,75,-610,4.0,0.3,8),
            (735,640,-65,-670,4.5,0.6,12), (1085,590,-70,-630,4.3,0.1,10),
            (565,580,40,-650,5.0,0.8,7), (920,625,-50,-670,3.8,1.0,9),
            (95,540,95,-560,4.9,1.2,8), (1200,570,-85,-610,4.1,0.5,11),
            (450,645,45,-700,4.6,1.4,8), (800,610,-25,-640,3.9,0.2,10)),
        3: ((1390,205,-1570,240,1.45,0.0,30), (-120,420,1490,-255,1.65,0.2,26),
            (1300,590,-1450,-375,1.25,0.45,22), (-80,180,1440,310,1.9,0.1,18),
            (1360,360,-1480,35,1.35,0.65,34), (-95,560,1480,-390,1.55,0.35,15),
            (1380,95,-1490,350,1.7,0.8,19), (-110,315,1520,225,1.2,0.55,13),
            (1400,475,-1540,-260,1.8,0.3,28), (-90,90,1460,420,1.4,0.9,21)),
    }

    try:
        renpy.register_shader("msbf.seer_environment", variables="""
            uniform sampler2D tex0;
            uniform float u_time;
            uniform float u_seer_charge;
            uniform float u_seer_danger;
            uniform float u_seer_phase;
            uniform float u_seer_wave;
            uniform float u_seer_amp;
            uniform float u_seer_score;
            uniform float u_seer_bps;
            uniform float u_seer_id;
            uniform float u_seer_detail;
            uniform vec3 u_seer_key;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float seer_hash(float n) {
                return fract(sin(n * 127.1 + 311.7) * 43758.5453);
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            float t = u_time;
            float sky = 1.0 - smoothstep(0.48, 0.60, uv.y);
            float aperture = smoothstep(0.20, 0.33, uv.x) * (1.0 - smoothstep(0.68, 0.80, uv.x));
            float depth = 1.0 - smoothstep(0.43, 0.64, uv.y);
            float side = (1.0 - aperture) * depth;
            float bank = step(0.5, uv.x);
            // Move the PAINTING before lighting it. The foreground contact
            // plane stays anchored; sky and suspended ruins have different
            // travel, so this reads as a living place rather than camera shake.
            vec2 filmuv = uv;
            float beat = max(0.0, u_seer_score) * u_seer_bps;
            float hit = 0.0;
            float split = 0.0;
            float wound = 0.0;
            float lip = 0.0;
            if (u_seer_phase < 1.5) {
                filmuv += vec2(sin(t * 0.61 + bank * 2.2) * 0.006,
                    cos(t * 0.73 + bank * 1.8) * 0.010) * side;
                filmuv += vec2(sin(t * 0.53 + uv.y * 2.0) * 0.026,
                    cos(t * 0.41 + uv.x * 2.0) * 0.012) * sky * aperture;
            } else if (u_seer_phase < 2.5) {
                // The vault opens and lifts, with a slower contrary drift in
                // its hanging stone. Gold retains its divine arrival grammar.
                filmuv += (uv - vec2(0.5, 0.26)) * sin(t * 0.72) * -0.048 * sky * aperture;
                filmuv.y += sin(t * 0.58) * 0.020 * sky * aperture;
                filmuv += vec2(sin(t * 0.43 + bank * 2.0) * 0.004,
                    sin(t * 0.66 + bank * 2.4) * 0.013) * side;
                // Id's opening is still gold, with tension beneath the lift.
                filmuv.x += sin(t * 2.3 + uv.y * 3.0) * 0.0025 * depth * u_seer_id;
            } else {
                float count = floor(beat);
                float halfcount = floor(beat * 2.0);
                float strike = exp(-fract(beat) * 7.5) * (0.48 + 0.52 * seer_hash(count));
                float interruption = exp(-fract(beat * 2.0) * 9.0)
                    * step(0.57, seer_hash(halfcount + 81.0)) * 0.62;
                hit = min(1.25, strike + interruption) * (0.72 + 0.28 * u_seer_id)
                    * step(0.0, u_seer_score);
                // A torn film has uneven edges and displaced pieces of the
                // image, not smooth lightning drawn on an intact photograph.
                float cut = floor(beat * 0.5);
                float tooth = abs(fract(uv.y * 6.3 + seer_hash(cut) * 0.8) - 0.5);
                float spine = 0.46 + (seer_hash(cut + 4.0) - 0.5) * 0.29
                    + (uv.y - 0.25) * (seer_hash(cut + 7.0) - 0.5) * 0.48
                    + tooth * 0.13;
                float distance = uv.x - spine;
                float localtear = 1.0 - smoothstep(0.10, 0.29, abs(distance));
                float recoil = sin(fract(beat) * 19.0) * exp(-fract(beat) * 5.5);
                float opening = max(0.0001, (0.006 + hit * 0.024) * depth);
                split = sign(distance) * localtear * (0.009 + hit * 0.035 + recoil * 0.009) * depth;
                filmuv.x += split;
                filmuv.y += sign(distance) * localtear * (hit * 0.016 + recoil * 0.008) * depth;
                // Adjacent strips lose registration on selected half beats.
                float strip = floor(uv.y * 11.0 + uv.x * 1.7);
                float slip = (seer_hash(strip + halfcount * 13.0) - 0.5)
                    * step(0.53, seer_hash(strip + halfcount * 7.0)) * hit;
                filmuv.x += slip * 0.070 * depth;
                filmuv += vec2(sin(t * 1.8 + bank * 2.1) * 0.009,
                    cos(t * 2.3 + bank * 2.7) * 0.016) * side;
                filmuv += vec2(sin(t * 1.17 + uv.y * 3.0) * 0.018,
                    cos(t * 1.49 + uv.x * 3.0) * 0.015) * aperture * sky;
                wound = (1.0 - smoothstep(opening * 0.58, opening, abs(distance))) * depth;
                lip = (1.0 - smoothstep(0.001, 0.005, abs(abs(distance) - opening))) * depth;
            }
            // Fade displacement at the texture border, avoiding exposed edges
            // without cropping or scaling away any of the native painting.
            vec2 border = smoothstep(vec2(0.0), vec2(0.055), uv)
                * (1.0 - smoothstep(vec2(0.945), vec2(1.0), uv));
            filmuv = uv + (filmuv - uv) * border.x * border.y;
            vec4 plate = texture2D(tex0, clamp(filmuv, 0.001, 0.999));
            vec3 col = plate.rgb * 0.86;
            if (u_seer_phase > 2.5) {
                // A brief exposed, misregistered image persists at the torn
                // edge. Only this phase/high detail needs a second texture tap.
                if (u_seer_detail > 0.5) {
                    vec3 echo = texture2D(tex0, clamp(filmuv - vec2(split * 0.75, hit * 0.009 * depth), 0.001, 0.999)).rgb;
                    col = mix(col, vec3(echo.r, col.g, echo.b), min(0.55, hit * depth * 0.48));
                }
                col = mix(col, vec3(0.018, 0.003, 0.025), wound * 0.91);
                col += vec3(0.90, 0.19, 0.29) * lip * (0.14 + hit * 0.38);
                // Existing painted fissures answer locally, never as a white
                // frame flash or an exposure pulse across the interface.
                float ember = max(0.0, plate.r - max(plate.g, plate.b) * 0.95);
                col += vec3(0.46, 0.07, 0.10) * ember * hit * (0.3 + depth);
            }
            float flow = 0.0;
            float radiance = 0.0;
            if (u_seer_phase < 1.5) {
                // Long wind fronts sweep the open sky; each has a moving crest.
                for (int i = 0; i < 4; i++) {
                    float n = float(i);
                    float y = 0.14 + n * 0.105 + sin(uv.x * 4.5 + t * 1.7 + n) * 0.032;
                    float line = 1.0 - smoothstep(0.0015, 0.009, abs(uv.y - y));
                    float crest = pow(max(0.0, sin(uv.x * 6.0 + t * (3.0 + n * 0.12) + n)), 5.0);
                    flow += line * crest;
                }
                col += u_seer_key * flow * sky * (0.10 + aperture * 0.24);
                float aurora = 0.5 + 0.5 * sin(uv.x * 16.0 + uv.y * 8.0 - t * 0.95 + sin(uv.y * 11.0 + t * 0.7));
                col += vec3(0.12, 0.30, 0.52) * pow(aurora, 5.0) * sky * aperture * 0.15;
            } else if (u_seer_phase < 2.5) {
                // Broad divine shafts breathe sideways while bright knots
                // travel UP them, following the lifting painted vault.
                float beamx = uv.x + sin(uv.y * 5.0 + t * 0.45) * 0.028;
                float beams = pow(max(0.0, sin(beamx * 31.0 + t * 0.40)), 10.0);
                float rising = 0.45 + 0.55 * pow(0.5 + 0.5 * sin(uv.y * 17.0 + t * 3.4 + uv.x * 12.0), 3.0);
                radiance = beams * rising * aperture * (1.0 - smoothstep(0.57, 0.82, uv.y));
                col += vec3(1.0, 0.83, 0.47) * radiance * 0.38;
                float veil = 0.5 + 0.5 * sin(uv.x * 15.0 - uv.y * 8.0 + t * 1.1 + sin(uv.y * 6.0 - t));
                col += vec3(0.38, 0.52, 0.68) * pow(veil, 6.0) * sky * aperture * 0.16;
            } else {
                // Secondary currents catch the edges of the moving film.
                for (int i = 0; i < 3; i++) {
                    float n = float(i);
                    float jag = abs(fract(uv.y * (7.0 + n) + t * (0.21 + n * 0.04)) - 0.5);
                    float spine = 0.38 + n * 0.12 + sin(uv.y * 8.0 + t * (1.2 + n * 0.37) + n) * 0.10 + jag * 0.055;
                    float distance = abs(uv.x - spine);
                    float core = 1.0 - smoothstep(0.001, 0.0035, distance);
                    float haze = 1.0 - smoothstep(0.003, 0.026, distance);
                    float surge = 0.35 + 0.65 * pow(0.5 + 0.5 * sin(uv.y * 23.0 - t * (4.7 + n) + sin(t * 1.9 + n)), 3.0);
                    flow += (core * 0.66 + haze * 0.16) * surge;
                }
                col += vec3(1.0, 0.22, 0.36) * flow * sky * (0.48 + hit * 0.64);
                float shear = pow(max(0.0, sin(uv.y * 46.0 + uv.x * 13.0 + t * 5.1 + sin(t * 2.2))), 24.0);
                col += vec3(0.50, 0.08, 0.18) * shear * sky * aperture * 0.17;
            }

            // Projected light follows the painting's inlaid floor circle.
            vec2 flooruv = (uv - vec2(0.5, 0.668)) * vec2(1.0, 4.15);
            float floorr = length(flooruv);
            float floora = atan(flooruv.y, flooruv.x);
            float floorband = 1.0 - smoothstep(0.003, 0.010, abs(floorr - 0.29));
            floorband += (1.0 - smoothstep(0.003, 0.008, abs(floorr - 0.40))) * 0.55;
            float turn = 0.50 + 0.50 * sin(floora * 3.0 - t * (u_seer_phase > 2.5 ? 3.7 : 1.5));
            float floorlight = floorband * pow(turn, 4.0) * smoothstep(0.55, 0.61, uv.y);
            col += u_seer_key * floorlight * (0.28 + u_seer_charge * 0.25);
            // A projected shock ellipse follows the same boss ground anchor.
            vec2 waveuv = (uv - vec2(0.5, 0.79)) * vec2(1.0, 3.2);
            float radius = length(waveuv);
            float ring = 1.0 - smoothstep(0.008, 0.026, abs(radius - u_seer_wave * 0.9));
            float wave = ring * (1.0 - u_seer_wave) * step(0.001, u_seer_wave);
            col += u_seer_key * wave * u_seer_amp * 0.45;
            float edge = smoothstep(0.24, 0.72, length((uv - 0.5) * vec2(1.0, 0.8)));
            col *= 1.0 - edge * 0.18;
            col += vec3(0.24, 0.01, 0.025) * edge * u_seer_danger * 0.22;
            gl_FragColor = vec4(col, plate.a);
        """)
        MSBF_SEER_SHADER = True
    except Exception:
        MSBF_SEER_SHADER = False


transform msbf_seer_shader_idle:
    # Keep the continuous background moving even while input is idle.
    pause 1.0 / 30.0
    repeat


transform msbf_seer_shader_score:
    function msbf_seer_score_clock


transform msbf_seer_environment_t(phase=1, charge=0.0, danger=0.0, shock=False, amp=1.0, id_mode=False, detail=True):
    mesh True
    shader "msbf.seer_environment"
    u_seer_charge charge
    u_seer_danger danger
    u_seer_phase float(phase)
    u_seer_key msbf_arena_cfg(phase)["key"]
    u_seer_amp amp
    u_seer_score 0.0
    u_seer_bps MSBF_SEER_RUPTURE_BPM / 60.0
    u_seer_id float(id_mode)
    u_seer_detail float(detail)
    u_seer_wave 0.0
    parallel:
        linear (0.68 if shock else 0.0) u_seer_wave (1.0 if shock else 0.0)
    parallel:
        (msbf_seer_shader_score if phase >= 3 else msbf_seer_shader_idle)


transform msbf_seer_plate_drift(phase=1):
    ease (2.8 if phase == 2 else 1.8) xoffset -9 yoffset (-6 if phase == 2 else 3)
    ease (3.2 if phase == 2 else 2.1) xoffset 9 yoffset (6 if phase == 2 else -3)
    repeat


transform msbf_seer_plate_kick:
    xoffset -12
    yoffset 4
    pause 0.07
    ease 0.21 xoffset 3 yoffset -2
    xoffset 10
    yoffset -5
    ease 0.280748 xoffset 0 yoffset 0
    pause 0.560748
    xoffset 12
    yoffset 5
    pause 0.05
    xoffset -8
    yoffset -4
    ease 0.510748 xoffset 0 yoffset 0
    pause 0.560748
    repeat


transform msbf_seer_plate_fallback(phase=1):
    # No custom shader: gently move the plate itself inside a clipped stage.
    subpixel True
    align (0.5, 0.5)
    zoom 1.035
    (msbf_seer_plate_kick if phase >= 3 else msbf_seer_plate_drift(phase))


transform msbf_seer_floor_seal(phase=1, reverse=False):
    subpixel True
    align (0.5, 0.5)
    matrixcolor TintMatrix(msbf_phase_accent(phase)[0])
    alpha 0.48
    rotate 0
    linear (24.0 if phase == 2 else 11.0 if phase >= 3 else 18.0) rotate (-360 if reverse else 360)
    repeat


transform msbf_seer_fragment(x, y, dx, dy, duration, delay, phase=1):
    subpixel True
    pos (x, y)
    alpha 0.0
    pause delay
    block:
        pos (x, y)
        rotate 0
        alpha 0.0
        parallel:
            linear duration xpos x + dx ypos y + dy rotate (540 if phase >= 3 else 120 if phase == 2 else -250)
        parallel:
            linear 0.15 alpha (0.82 if phase >= 3 else 0.76 if phase == 2 else 0.70)
            pause duration - 0.40
            linear 0.25 alpha 0.0
        repeat


transform msbf_seer_wind_lane(y=260, delay=0.0, phase=1):
    subpixel True
    xpos 1200
    ypos y
    alpha 0.0
    rotate (-68 if phase == 2 else -12 if phase >= 3 else -5)
    pause delay
    block:
        xpos (200 if phase == 2 else 1200)
        ypos y
        alpha 0.0
        parallel:
            linear (3.1 if phase == 2 else 1.15 if phase >= 3 else 1.7) xpos (560 if phase == 2 else -850) ypos (y - 680 if phase == 2 else y + 180 if phase >= 3 else y + 70)
        parallel:
            linear 0.18 alpha (0.48 if phase == 2 else 0.66)
            pause (2.57 if phase == 2 else 0.62 if phase >= 3 else 1.17)
            linear 0.35 alpha 0.0
        repeat



# The floor seals' projection (was an inline `at transform:`, which a screen
# re-instantiates on every execution; a named one is reused, see msbf_t).
transform msbf_seer_floor_squash(z=0.24):
    yzoom z


screen msbf_seer_environment(phase=1, id_mode=False, charge=0.0, danger=0.0, shock=False, amp=1.0):
    $ _seer_garnish = msbf_gfx_garnish()
    if MSBF_SEER_SHADER:
        add msbf_seer_plate(phase) at msbf_t(msbf_seer_environment_t, phase, charge, danger, shock, amp, id_mode, _seer_garnish):
            xysize (1280, 720)
    else:
        fixed:
            xysize (1280, 720)
            clipping True
            add msbf_seer_plate(phase) at msbf_t(msbf_seer_plate_fallback, phase):
                xysize (1280, 720)
        add Solid("#04081730") xysize (1280, 720)

    # Moving air and a reduced fragment set remain on the performance stop.
    # Optional orbit/ribbon duplication is omitted there, with no extra
    # full-screen render target and no change to battle simulation frequency.
    $ _seer_paths = MSBF_SEER_PATHS.get(phase, MSBF_SEER_PATHS[1])
    $ _seer_fragment = "mote.png" if phase == 2 else "debris_rupture.png" if phase >= 3 else "debris_cyan.png"
    for _sf_x, _sf_y, _sf_dx, _sf_dy, _sf_dur, _sf_delay, _sf_size in _seer_paths[:10 if _seer_garnish else 4]:
        add (MSBF_SEER_ART + _seer_fragment) at msbf_t(msbf_seer_fragment, _sf_x, _sf_y, _sf_dx, _sf_dy, _sf_dur, _sf_delay, phase):
            xysize (_sf_size, _sf_size)
            matrixcolor TintMatrix("#fff0c5" if phase == 2 else "#ffffff")
    for _sw_y, _sw_delay in ((240,0.0), (400,0.55), (560,1.1))[:3 if _seer_garnish else 1]:
        add (MSBF_SEER_ART + "wind_current.png") at msbf_t(msbf_seer_wind_lane, _sw_y, _sw_delay, phase):
            xysize (768, 128)
            matrixcolor TintMatrix(msbf_phase_accent(phase)[0])

    if _seer_garnish:
        # Rotation takes place in the circle's plane before it is projected
        # into the floor ellipse; rotating an already squashed ring wobbles.
        fixed:
            xcenter 640
            ycenter 481
            xysize (720, 720)
            at msbf_t(msbf_seer_floor_squash, 0.24)
            add MSBF_SEER_ART + "orbit_current.png" at msbf_t(msbf_seer_floor_seal, phase):
                xysize (720, 720)
        fixed:
            xcenter 640
            ycenter 78
            xysize (206, 206)
            at msbf_t(msbf_seer_floor_squash, 0.32)
            add MSBF_SEER_ART + "orbit_current.png" at msbf_t(msbf_seer_floor_seal, phase, True):
                xysize (206, 206)

    if id_mode and phase == 2:
        # The Id entry is the awakened golden room, with its own faint red
        # underlight; phase progression remains wholly battle-controlled.
        add Solid("#3b07151a") xysize (1280, 720)
