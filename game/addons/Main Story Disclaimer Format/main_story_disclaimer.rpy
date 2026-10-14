# Main-story threshold: msd_enter -> msd_card(s) -> choice -> msd_exit.
# This system notice has its own red/black protocol, distinct from Nier prose
# and MC narration. Full atmosphere animates the signal field, Light holds it
# still, and Off/unsupported shaders use the flat readable composition.
# Shader uniforms animate through ATL on mesh quads with premultiplied alpha.
# Heartbeat-related periods share the audio loop length; card animation phase
# starts on show and is not synchronized to the already-playing audio loop.
# msd_finish_receiving() centralizes type completion and local SFX cleanup.

default msd_active = False
default msd_prev_quick_menu = True
default msd_card_ready = False
default msd_cover_phase = "none"
default msd_type_cursor = 0
default msd_type_channel_cursor = 0
default msd_last_title = ""
default msd_last_message = ""
default msd_last_page = 1
default msd_last_total = 1


# Keep the ominous bed off the ordinary sound channel. The opening can stop it
# cleanly without interrupting any UI or story effect that happens to follow.
init -20 python:
    renpy.music.register_channel("msd_ambience", mixer="sfx", loop=True)

    # This is the machine blip from Tsubaki's Soul terminal, not Tsubaki's
    # character cue. Keep it on a tiny local pool so quick successive blips do
    # not cut one another off or borrow the ordinary story sound channel.
    MSD_TYPE_BLIP = "assets/audio/sfx/msbf/uiblip.wav"
    MSD_TYPE_CHANNELS = tuple("msd_type_%d" % i for i in range(4))
    for _msd_type_channel in MSD_TYPE_CHANNELS:
        if not renpy.music.channel_defined(_msd_type_channel):
            renpy.music.register_channel(_msd_type_channel, mixer="sfx", loop=False)

    def msd_stop_type_blips():
        """Stop every local type-on cue before the notice changes state."""
        for channel in MSD_TYPE_CHANNELS:
            try:
                renpy.music.stop(channel=channel, fadeout=0.0)
            except Exception:
                # Audio is optional in renderer and stripped-down QA runs.
                pass

    def msd_finish_receiving(message):
        """Resolve the copy, cursor, and blips as one interaction state."""
        renpy.store.msd_type_cursor = len(message)
        renpy.store.msd_card_ready = True
        msd_stop_type_blips()
        renpy.restart_interaction()

    def msd_play_type_blip(message):
        """Advance the disclaimer typewriter and sound visible character beats."""
        if renpy.is_skipping():
            msd_finish_receiving(message)
            return

        cursor = int(getattr(renpy.store, "msd_type_cursor", 0))
        if cursor >= len(message):
            return

        # The copy runs at 42 cps. One cue per two characters keeps the sound
        # recognizably terminal-like without turning a long advisory into a
        # continuous click track. Whitespace still advances silently.
        next_cursor = min(len(message), cursor + 2)
        beat = message[cursor:next_cursor]
        renpy.store.msd_type_cursor = next_cursor
        if not any(character not in " \t\r\n" for character in beat):
            return

        channel_cursor = int(getattr(renpy.store, "msd_type_channel_cursor", 0))
        channel = MSD_TYPE_CHANNELS[channel_cursor % len(MSD_TYPE_CHANNELS)]
        renpy.store.msd_type_channel_cursor = channel_cursor + 1
        try:
            renpy.sound.play(MSD_TYPE_BLIP, channel=channel, relative_volume=0.22)
        except Exception:
            # The notice remains usable in stripped-down QA/audio-disabled
            # environments; sound is presentation, never route logic.
            pass


# =============================================================================
#  SHADERS
# =============================================================================
#   enter_m.msd_field    the whole-frame signal field behind the panel
#   enter_m.msd_glass    the panel: translucent body, lit rim, sheen, hatch tab
#   enter_m.msd_meter    a segmented vertical signal meter
#   enter_m.msd_rule     a horizontal accent rule: fade, glint, partial fill
#   enter_m.msd_edge     a one-sided glow falloff (the shutter lips)
#   enter_m.msd_button   a glint crossing a choice plate (samples tex0)
#
# All identifiers carry msd_ because shader parts share one GLSL scope. GLSL ES
# 1.00 only: no derivatives, no loops, ordered smoothstep edges.
init -10 python:

    def _msd_register_shaders():

        renpy.register_shader("enter_m.msd_field", variables="""
            uniform float u_msd_drift;
            uniform float u_msd_sweep;
            uniform float u_msd_ping;
            uniform float u_msd_grain;
            uniform vec2  u_model_size;
            varying vec2  v_tex_coord;
        """, fragment_functions="""
            float msd_field_hash(vec2 msd_p) {
                vec3 msd_p3 = fract(vec3(msd_p.xyx) * 0.1031);
                msd_p3 += dot(msd_p3, msd_p3.yzx + 33.33);
                return fract((msd_p3.x + msd_p3.y) * msd_p3.z);
            }
            float msd_field_noise(vec2 msd_p) {
                vec2 msd_i = floor(msd_p);
                vec2 msd_f = fract(msd_p);
                vec2 msd_u = msd_f * msd_f * (3.0 - 2.0 * msd_f);
                float msd_a = msd_field_hash(msd_i);
                float msd_b = msd_field_hash(msd_i + vec2(1.0, 0.0));
                float msd_c = msd_field_hash(msd_i + vec2(0.0, 1.0));
                float msd_d = msd_field_hash(msd_i + vec2(1.0, 1.0));
                return mix(mix(msd_a, msd_b, msd_u.x), mix(msd_c, msd_d, msd_u.x), msd_u.y);
            }
        """, fragment_300="""
            vec2 msd_uv = v_tex_coord;
            vec2 msd_px = msd_uv * u_model_size;

            // Blue-black, a shade lifted toward the top of the frame.
            vec3 msd_col = mix(vec3(0.030, 0.018, 0.034), vec3(0.016, 0.014, 0.026), msd_uv.y);

            // A crimson bloom behind the panel, aspect-corrected to a circle.
            vec2 msd_c = (msd_uv - vec2(0.5, 0.47)) * vec2(1.7778, 1.0);
            float msd_r = length(msd_c);
            msd_col += vec3(0.20, 0.030, 0.070) * exp(-msd_r * msd_r * 4.0) * 0.60;

            // SIGNAL FOG. Three octaves advected around a closed circle, so the
            // drift wraps without a seam when the ATL resets u_msd_drift to 0.
            vec2 msd_loop = vec2(cos(6.28318530718 * u_msd_drift), sin(6.28318530718 * u_msd_drift));
            vec2 msd_q = msd_uv * vec2(4.0, 2.25);
            float msd_f =
                msd_field_noise(msd_q + msd_loop * 0.60) * 0.55 +
                msd_field_noise(msd_q * 2.03 - msd_loop * 0.90 + vec2(7.1, 2.3)) * 0.30 +
                msd_field_noise(msd_q * 4.01 + msd_loop.yx * 1.40 + vec2(3.7, 9.2)) * 0.15;
            msd_col += vec3(0.150, 0.022, 0.058) * smoothstep(0.42, 0.95, msd_f) * 0.55;

            // DOT LATTICE on a 32px grid, lit by a ring that expands from the
            // panel on the heartbeat. u_msd_ping runs 0..1 per ring.
            vec2 msd_g = mod(msd_px, 32.0) - vec2(16.0);
            float msd_dot = 1.0 - smoothstep(0.7, 1.5, length(msd_g));
            float msd_rd = (msd_r - u_msd_ping * 1.25) / 0.075;
            float msd_ring = exp(-msd_rd * msd_rd) * (1.0 - u_msd_ping);
            msd_col += vec3(0.62, 0.12, 0.20) * msd_dot * (0.07 + 0.55 * msd_ring);

            // INTERFERENCE BAND, top to bottom: a soft body with a 2px core.
            float msd_dy = msd_uv.y - (u_msd_sweep * 1.10 - 0.05);
            float msd_band = exp(-msd_dy * msd_dy / 0.0009);
            float msd_core = exp(-msd_dy * msd_dy / 0.000004);
            msd_col += vec3(0.55, 0.12, 0.20) * (msd_band * 0.10 + msd_core * 0.16);

            // CRT scanlines, 3px period, shallow.
            msd_col *= 0.92 + 0.08 * sin(msd_px.y * 2.0944);

            // Grain. u_msd_grain climbs continuously, so every frame reseeds.
            float msd_n = msd_field_hash(floor(msd_px) + vec2(u_msd_grain * 131.0, u_msd_grain * 71.0));
            msd_col += (msd_n - 0.5) * 0.022;

            // Vignette.
            vec2 msd_v = (msd_uv - vec2(0.5)) * vec2(1.15, 1.0);
            msd_col *= 1.0 - smoothstep(0.30, 0.78, length(msd_v)) * 0.70;

            gl_FragColor = vec4(max(msd_col, vec3(0.0)), 1.0);
        """)

        renpy.register_shader("enter_m.msd_glass", variables="""
            uniform float u_msd_rim;
            uniform float u_msd_sheen;
            uniform vec2  u_model_size;
            varying vec2  v_tex_coord;
        """, fragment_300="""
            vec2 msd_uv = v_tex_coord;
            vec2 msd_px = msd_uv * u_model_size;

            // Body: a translucent crimson-black, a little warmer at the top,
            // with a fine 4px ruling like a terminal's phosphor mask.
            vec3 msd_body = mix(vec3(0.095, 0.028, 0.050), vec3(0.050, 0.014, 0.028), msd_uv.y);
            msd_body *= 0.94 + 0.06 * step(0.5, fract(msd_px.y * 0.25));
            float msd_a = mix(0.80, 0.90, msd_uv.y);

            // Rim light INSIDE the border, falling off over ~9px.
            float msd_d = min(min(msd_px.x, msd_px.y),
                min(u_model_size.x - msd_px.x, u_model_size.y - msd_px.y));
            float msd_rim = exp(-msd_d / 9.0) * u_msd_rim;
            vec3 msd_rimc = vec3(0.79, 0.18, 0.29);

            // A diagonal sheen crossing the glass now and then.
            float msd_p = msd_uv.x + (msd_uv.y - 0.5) * 0.35;
            float msd_sh = 1.0 - smoothstep(0.0, 0.10, abs(msd_p - u_msd_sheen));
            msd_sh = msd_sh * msd_sh * 0.05;

            // Warning hatch tab, top right.
            float msd_tab =
                step(u_model_size.x - 172.0, msd_px.x) * step(msd_px.x, u_model_size.x - 24.0) *
                step(12.0, msd_px.y) * step(msd_px.y, 18.0);
            float msd_hatch = step(0.5, fract((msd_px.x + msd_px.y) / 12.0)) * msd_tab;

            float msd_out_a = clamp(msd_a + msd_rim * 0.5 + msd_hatch * 0.45, 0.0, 1.0);
            vec3 msd_col = msd_body * msd_a + msd_rimc * msd_rim +
                vec3(1.0, 0.55, 0.62) * msd_sh + msd_rimc * msd_hatch * 0.55;
            gl_FragColor = vec4(min(msd_col, vec3(msd_out_a)), msd_out_a);
        """)

        renpy.register_shader("enter_m.msd_meter", variables="""
            uniform float u_msd_level;
            varying vec2  v_tex_coord;
        """, fragment_300="""
            // 21 segments, filled from the bottom up to u_msd_level; the top
            // lit segment runs hot.
            float msd_seg = floor(v_tex_coord.y * 21.0);
            float msd_in = step(fract(v_tex_coord.y * 21.0), 0.68);
            float msd_h = 1.0 - (msd_seg + 0.5) / 21.0;
            float msd_on = step(msd_h, u_msd_level);
            float msd_top = msd_on * (1.0 - step(msd_h + 1.0 / 21.0, u_msd_level));
            vec3 msd_col = mix(vec3(0.71, 0.14, 0.26), vec3(1.0, 0.62, 0.68), msd_h * msd_h);
            msd_col = mix(msd_col, vec3(1.0, 0.86, 0.88), msd_top * 0.6);
            float msd_a = msd_in * mix(0.14, 0.95, msd_on);
            gl_FragColor = vec4(msd_col * msd_a, msd_a);
        """)

        renpy.register_shader("enter_m.msd_rule", variables="""
            uniform vec3  u_msd_col;
            uniform float u_msd_fill;
            uniform float u_msd_glint;
            uniform float u_msd_fade;
            varying vec2  v_tex_coord;
        """, fragment_300="""
            float msd_x = v_tex_coord.x;
            float msd_shown = step(msd_x, u_msd_fill);
            float msd_gd = (msd_x - u_msd_glint) / 0.05;
            float msd_gl = exp(-msd_gd * msd_gd);
            float msd_a = clamp(((1.0 - u_msd_fade * msd_x) + msd_gl * 0.6) * msd_shown, 0.0, 1.0);
            vec3 msd_col = mix(u_msd_col, vec3(1.0, 0.88, 0.90), msd_gl * 0.8);
            gl_FragColor = vec4(msd_col * msd_a, msd_a);
        """)

        renpy.register_shader("enter_m.msd_edge", variables="""
            uniform vec3  u_msd_col;
            uniform float u_msd_gain;
            uniform vec2  u_msd_from;
            uniform vec2  u_msd_dir;
            varying vec2  v_tex_coord;
        """, fragment_300="""
            // Brightest at the edge through u_msd_from, gone by the far side.
            float msd_t = clamp(dot(v_tex_coord - u_msd_from, u_msd_dir), 0.0, 1.0);
            float msd_k = 1.0 - msd_t;
            float msd_a = clamp(msd_k * msd_k * msd_k * u_msd_gain, 0.0, 1.0);
            gl_FragColor = vec4(u_msd_col * msd_a, msd_a);
        """)

        renpy.register_shader("enter_m.msd_button", variables="""
            uniform sampler2D tex0;
            uniform float u_msd_hover;
            uniform float u_msd_glint;
            varying vec2  v_tex_coord;
        """, fragment_300="""
            vec4 msd_base = texture2D(tex0, v_tex_coord);
            float msd_p = v_tex_coord.x + (v_tex_coord.y - 0.5) * 0.30;
            float msd_band = 1.0 - smoothstep(0.0, 0.12, abs(msd_p - u_msd_glint));
            msd_band = msd_band * msd_band * u_msd_hover;
            vec3 msd_col = msd_base.rgb + vec3(1.0, 0.70, 0.76) * msd_band * 0.22 * msd_base.a;
            gl_FragColor = vec4(min(msd_col, vec3(msd_base.a)), msd_base.a);
        """)

    try:
        _msd_register_shaders()
        MSD_SHADERS = True
    except Exception as _msd_shader_error:
        MSD_SHADERS = False
        renpy.log("ENTER-M MSD: shader registration failed: %r" % _msd_shader_error)


init -5 python:

    def msd_lit():
        """True when the lit look can draw: Atmosphere is not Off, the shaders
        registered, and the model renderer is running."""
        quality = getattr(persistent, "enter_m_atmos_quality", "full")
        return (quality != "off"
            and MSD_SHADERS
            and renpy.display.render.models)

    def msd_alive():
        """True when the lit look may animate (Atmosphere Full)."""
        return getattr(persistent, "enter_m_atmos_quality", "full") not in ("light", "off")

    @renpy.pure
    def msd_quad(w, h):
        """A transparent plate for a shader to paint onto."""
        return Solid("#00000000", xysize=(int(w), int(h)))

    @renpy.pure
    def msd_shutter(top, lit):
        """One terminal shutter. Lit, its inner edge glows as if the signal
        were leaking through the seam."""
        parts = [Solid("#020208", xysize=(1280, 362))]
        if lit:
            parts.append(Transform(
                Solid("#00000000", xysize=(1280, 44)),
                mesh=True, shader="enter_m.msd_edge",
                u_msd_col=(0.80, 0.16, 0.28), u_msd_gain=0.55,
                u_msd_from=(0.0, 1.0) if top else (0.0, 0.0),
                u_msd_dir=(0.0, -1.0) if top else (0.0, 1.0),
                ypos=(362 - 44) if top else 0))
            parts.append(Solid("#ca2d4a", xysize=(1280, 2), ypos=360 if top else 0))
        return Fixed(*parts, xysize=(1280, 362))

    @renpy.pure
    def msd_button_plate(hover):
        """Choice plate: a dark body, a left accent that thickens and heats up
        on hover, and a hairline underneath."""
        if hover:
            return Fixed(
                Solid("#3b0f1f"),
                Solid("#ff4163", xsize=4),
                Solid("#ca2d4a88", ysize=1, yalign=1.0))
        return Fixed(
            Solid("#1c0911"),
            Solid("#7e2038", xsize=2),
            Solid("#7e203855", ysize=1, yalign=1.0))


# =============================================================================
#  MOTION
# =============================================================================

transform msd_scanline:
    subpixel True
    ypos -4
    alpha 0.0
    linear 0.55 alpha 0.16
    linear 2.10 ypos 724 alpha 0.0
    repeat


transform msd_signal_pulse:
    alpha 0.18
    linear 0.80 alpha 0.66
    linear 0.24 alpha 0.28
    linear 0.94 alpha 0.48
    linear 0.30 alpha 0.16
    repeat


transform msd_panel_breath:
    alpha 0.16
    linear 1.30 alpha 0.30
    linear 1.80 alpha 0.12
    repeat


transform msd_title_reveal:
    subpixel True
    alpha 0.0
    yoffset 14
    easeout 0.46 alpha 1.0 yoffset 0


transform msd_title_idle_signal:
    subpixel True
    alpha 1.0
    block:
        # The signal only breaks after the card has finished receiving its
        # copy. During the type-on pass the title stays settled and readable.
        pause 2.20
        linear 0.035 xoffset -4
        linear 0.035 xoffset 5
        linear 0.035 xoffset 0
        pause 2.60
        repeat


# The chromatic split under the title. Both ghosts converge from a wide split
# onto a faint 1.5px fringe as the title lands, then spike on exactly the beats
# msd_title_idle_signal glitches on -- same pauses, same 35ms steps.
transform msd_ghost_reveal(dx):
    subpixel True
    alpha 0.0
    xoffset (dx * 8.0)
    yoffset 14
    easeout 0.46 alpha 0.22 xoffset dx yoffset 0


transform msd_ghost_idle(dx):
    subpixel True
    alpha 0.22
    xoffset dx
    block:
        pause 2.20
        linear 0.035 xoffset (dx * -3.5) alpha 0.80
        linear 0.035 xoffset (dx * 4.5)
        linear 0.035 xoffset dx alpha 0.22
        pause 2.60
        repeat


transform msd_copy_reveal:
    alpha 0.0
    xoffset -14
    easeout 0.62 alpha 1.0 xoffset 0


transform msd_prompt_blink:
    alpha 0.30
    linear 0.70 alpha 0.92
    linear 0.70 alpha 0.30
    repeat


# Lub-dub on the 1.087s heartbeat loop (0.10 + 0.28 + 0.08 + 0.627).
transform msd_pip_beat:
    alpha 0.35
    block:
        easeout 0.10 alpha 1.0
        easein 0.28 alpha 0.45
        easeout 0.08 alpha 0.85
        easein 0.627 alpha 0.35
        repeat


# --- the lit layer --------------------------------------------------------------
# Fog 32 beats, band 4 beats, lattice ring 2 beats.
transform msd_field_live:
    mesh True
    shader "enter_m.msd_field"
    u_msd_drift 0.0
    u_msd_sweep 0.0
    u_msd_ping 1.0
    u_msd_grain 0.0
    parallel:
        linear 34.784 u_msd_drift 1.0
        u_msd_drift 0.0
        repeat
    parallel:
        pause 0.55
        linear 3.798 u_msd_sweep 1.0
        u_msd_sweep 0.0
        repeat
    parallel:
        u_msd_ping 0.0
        linear 1.40 u_msd_ping 1.0
        pause 0.774
        repeat
    parallel:
        linear 60.0 u_msd_grain 600.0
        u_msd_grain 0.0
        repeat


transform msd_field_still:
    mesh True
    shader "enter_m.msd_field"
    u_msd_drift 0.18
    u_msd_sweep 0.0
    u_msd_ping 1.0
    u_msd_grain 0.0


transform msd_glass_live:
    mesh True
    shader "enter_m.msd_glass"
    u_msd_rim 0.30
    u_msd_sheen -0.4
    parallel:
        ease 1.30 u_msd_rim 0.46
        ease 1.80 u_msd_rim 0.24
        repeat
    parallel:
        pause 3.0
        linear 2.2 u_msd_sheen 1.4
        u_msd_sheen -0.4
        pause 3.5
        repeat


transform msd_glass_still:
    mesh True
    shader "enter_m.msd_glass"
    u_msd_rim 0.34
    u_msd_sheen -0.4


transform msd_meter_live(delay=0.0):
    mesh True
    shader "enter_m.msd_meter"
    u_msd_level 0.22
    pause delay
    block:
        easeout 0.10 u_msd_level 0.92
        easein 0.28 u_msd_level 0.40
        easeout 0.08 u_msd_level 0.72
        easein 0.627 u_msd_level 0.22
        repeat


transform msd_meter_still:
    mesh True
    shader "enter_m.msd_meter"
    u_msd_level 0.45


transform msd_rule_live:
    mesh True
    shader "enter_m.msd_rule"
    u_msd_col (0.79, 0.18, 0.29)
    u_msd_fill 1.0
    u_msd_fade 0.85
    u_msd_glint -0.3
    block:
        pause 1.2
        linear 0.9 u_msd_glint 1.3
        u_msd_glint -0.3
        pause 2.248
        repeat


transform msd_rule_still:
    mesh True
    shader "enter_m.msd_rule"
    u_msd_col (0.79, 0.18, 0.29)
    u_msd_fill 1.0
    u_msd_fade 0.85
    u_msd_glint -1.0


# The receiving rule fills over exactly the typewriter's run (len / 42 cps).
transform msd_progress_lit(d):
    mesh True
    shader "enter_m.msd_rule"
    u_msd_col (0.79, 0.18, 0.29)
    u_msd_fade 0.0
    u_msd_glint -1.0
    u_msd_fill 0.0
    linear d u_msd_fill 1.0


transform msd_progress_flat(d):
    xzoom 0.0
    linear d xzoom 1.0


transform msd_progress_done:
    mesh True
    shader "enter_m.msd_rule"
    u_msd_col (0.79, 0.18, 0.29)
    u_msd_fade 0.0
    u_msd_fill 1.0
    u_msd_glint -0.3
    block:
        linear 0.9 u_msd_glint 1.3
        u_msd_glint -0.3
        pause 1.274
        repeat


transform msd_choice_fx:
    mesh True
    shader "enter_m.msd_button"
    u_msd_hover 0.0
    u_msd_glint -0.4
    on idle:
        linear 0.16 u_msd_hover 0.0
    on hover:
        parallel:
            linear 0.16 u_msd_hover 1.0
        parallel:
            u_msd_glint -0.4
            linear 0.85 u_msd_glint 1.4
            pause 1.324
            repeat


transform msd_noop:
    pass


# The disclaimer enters and leaves like a terminal aperture: both shutters
# start together at the center seam, then carry the signal away from the
# screen. The card is rendered underneath the opening cover, so its copy and
# heartbeat are already alive when the aperture reveals it.
transform msd_terminal_top_open:
    ypos 0
    easein_cubic 0.72 ypos -362


transform msd_terminal_bottom_open:
    ypos 358
    easein_cubic 0.72 ypos 720


transform msd_terminal_top_close:
    ypos -362
    easein_cubic 0.72 ypos 0


transform msd_terminal_bottom_close:
    ypos 720
    easein_cubic 0.72 ypos 358


transform msd_terminal_status:
    alpha 0.0
    linear 0.12 alpha 0.72
    pause 0.28
    linear 0.26 alpha 0.0


transform msd_terminal_seam_open:
    alpha 0.0
    linear 0.10 alpha 0.90
    linear 0.54 alpha 0.0


transform msd_terminal_seam_close:
    alpha 0.0
    pause 0.42
    linear 0.14 alpha 0.90
    linear 0.16 alpha 0.0


# =============================================================================
#  BACKDROP
# =============================================================================

screen main_story_disclaimer_backdrop():
    if msd_lit():
        $ msd_live = msd_alive()

        add msd_quad(1280, 720) at (msd_field_live if msd_live else msd_field_still)

        # The glass panel, its hairline border and the breathing top bar.
        add msd_quad(1064, 536) pos (108, 92) at (msd_glass_live if msd_live else msd_glass_still)
        add Solid("#7e203888") xpos 108 ypos 92 xsize 1064 ysize 1
        add Solid("#7e203888") xpos 108 ypos 627 xsize 1064 ysize 1
        add Solid("#7e203888") xpos 108 ypos 92 xsize 1 ysize 536
        add Solid("#7e203888") xpos 1171 ypos 92 xsize 1 ysize 536
        add Solid("#ca2d4a") xpos 108 ypos 92 xsize 1064 ysize 2 at msd_panel_breath
        add enter_m_brackets(1084, 556, "#ca2d4ab0", 26, 2) pos (98, 82)

        # Signal meters where the plain side markers were. The right one runs
        # half a beat behind the left, keeping the pair asymmetrical.
        add msd_quad(4, 420) pos (81, 150) at (msd_meter_live(0.0) if msd_live else msd_meter_still)
        add msd_quad(4, 420) pos (1195, 150) at (msd_meter_live(0.5435) if msd_live else msd_meter_still)
        add Solid("#b62442") xpos 82 ypos 150 xsize 11 ysize 1
        add Solid("#b62442") xpos 1187 ypos 570 xsize 11 ysize 1
        add Solid("#b62442") xpos 82 ypos 570 xsize 11 ysize 1
        add Solid("#b62442") xpos 1187 ypos 150 xsize 11 ysize 1

    else:
        add Solid("#06060a")

        # A barely visible center field keeps the text readable without
        # becoming a conventional dialogue box. The animated wash makes the
        # threshold feel active even while the player is deciding whether to
        # continue.
        add Solid("#180911") xpos 108 ypos 92 xsize 1064 ysize 536
        add Solid("#7e2038") xpos 108 ypos 92 xsize 1064 ysize 1
        add Solid("#7e2038") xpos 108 ypos 627 xsize 1064 ysize 1
        add Solid("#7e2038") xpos 108 ypos 92 xsize 1 ysize 536
        add Solid("#7e2038") xpos 1171 ypos 92 xsize 1 ysize 536
        add Solid("#ca2d4a") xpos 108 ypos 92 xsize 1064 ysize 2 at msd_panel_breath

        # The side markers are intentionally asymmetrical; they read as a
        # monitor or warning instrument instead of a second prose page.
        add Solid("#b62442") xpos 82 ypos 150 xsize 2 ysize 420 at msd_signal_pulse
        add Solid("#b62442") xpos 1196 ypos 150 xsize 2 ysize 420 at msd_signal_pulse
        add Solid("#b62442") xpos 82 ypos 150 xsize 11 ysize 1
        add Solid("#b62442") xpos 1187 ypos 570 xsize 11 ysize 1
        add Solid("#b62442") xpos 82 ypos 570 xsize 11 ysize 1
        add Solid("#b62442") xpos 1187 ypos 150 xsize 11 ysize 1

        # Thin moving interference. It is subtle enough not to compete with
        # the copy, but it prevents the screen from feeling like a static
        # warning card.
        add Solid("#d24a6328") xsize 1280 ysize 2 at msd_scanline


screen main_story_disclaimer_terminal_cover(msd_phase="open"):
    # These shutters are deliberately almost black rather than pure black, so
    # the red seam and status signal remain legible during the handoff.
    $ msd_shutter_lit = msd_lit()
    if msd_phase == "open":
        add msd_shutter(True, msd_shutter_lit) at msd_terminal_top_open
        add msd_shutter(False, msd_shutter_lit) at msd_terminal_bottom_open
        add Solid("#ca2d4a") xpos 128 ypos 359 xsize 1024 ysize 2 at msd_terminal_seam_open
    else:
        add msd_shutter(True, msd_shutter_lit) at msd_terminal_top_close
        add msd_shutter(False, msd_shutter_lit) at msd_terminal_bottom_close
        add Solid("#ca2d4a") xpos 128 ypos 359 xsize 1024 ysize 2 at msd_terminal_seam_close

    text ("SIGNAL CONNECTING" if msd_phase == "open" else "SIGNAL SEALED"):
        style "msd_terminal_status"
        xalign 0.5
        yalign 0.5


screen main_story_disclaimer_closing():
    # Keep the last card alive beneath the closing shutter. This removes the
    # perceptual gap between "the player finished reading" and "the signal is
    # sealed"; the notice itself is what disappears, not an empty replacement.
    use main_story_disclaimer_static_card(msd_last_title, msd_last_message, msd_last_page, msd_last_total)
    use main_story_disclaimer_terminal_cover("close")


# =============================================================================
#  SHARED PIECES
# =============================================================================

# Masthead row: a status pip on the heartbeat, the eyebrow, and -- on a paged
# card -- the page count with one pip per page, the current one lit.
screen msd_header(msd_page=1, msd_total=1, msd_eyebrow="THRESHOLD NOTICE", msd_paged=True):
    hbox:
        spacing 14
        add Solid("#ca2d4a") xysize (7, 7) yalign 0.5 at msd_pip_beat
        text msd_eyebrow style "msd_eyebrow"
        if msd_paged:
            text "PAGE %02d / %02d" % (msd_page, msd_total) style "msd_page_count"
            hbox:
                spacing 4
                yalign 0.5
                for msd_i in range(msd_total):
                    add Solid("#ff4163" if msd_i + 1 == msd_page else "#5a1c2c") xysize (16, 3)


# The title with its chromatic ghosts. `reveal` lands it; anything else holds
# it on the idle glitch. The flat look draws the title alone, as before.
#
# xfit/yfit, NOT fit_first: fit_first sizes the box to the first child and then
# lays the rest out inside that width. The ghosts have no outline, so they are
# 2px narrower than the real title, and the real title wrapped onto a second
# line over the rule and the copy. xfit renders every child at full width and
# fits the box to all of them.
screen msd_title_block(msd_title, msd_state="idle"):
    if msd_lit():
        fixed:
            xfit True
            yfit True
            if msd_state == "reveal":
                text msd_title style "msd_card_title_ghost" color "#ff2a4d" at msd_ghost_reveal(-1.5)
                text msd_title style "msd_card_title_ghost" color "#4fc8ff" at msd_ghost_reveal(1.5)
                text msd_title style "msd_card_title" at msd_title_reveal
            else:
                text msd_title style "msd_card_title_ghost" color "#ff2a4d" at msd_ghost_idle(-1.5)
                text msd_title style "msd_card_title_ghost" color "#4fc8ff" at msd_ghost_idle(1.5)
                text msd_title style "msd_card_title" at msd_title_idle_signal
    elif msd_state == "reveal":
        text msd_title style "msd_card_title" at msd_title_reveal
    else:
        text msd_title style "msd_card_title" at msd_title_idle_signal


screen msd_title_rule():
    if msd_lit():
        add msd_quad(230, 2) at (msd_rule_live if msd_alive() else msd_rule_still)
    else:
        add Solid("#ca2d4a") xsize 230 ysize 2


screen msd_side_panel():
    vbox:
        xpos 876
        ypos 164
        spacing 11

        text "STORY ENTRY" style "msd_side_label"
        add Solid("#9c2943") xsize 196 ysize 1
        text "NO ASSUMPTIONS" style "msd_side_value"
        text "NO SAFE DISTANCE" style "msd_side_value"
        text "READ THE NOTICE" style "msd_side_value"


# The bottom prompt, flanked by short rules, and the receiving rule under it.
#   state "receiving": dim prompt, rule fills over `msd_secs`
#   state "ready":     blinking prompt, full rule with a travelling glint
#   state "closing":   dim prompt, full rule, still
screen msd_prompt(msd_label, msd_state, msd_secs=0.0):
    hbox at (msd_prompt_blink if msd_state == "ready" else msd_noop):
        xpos 640
        xanchor 0.5
        ypos 668
        spacing 12
        add Solid("#ca2d4a" if msd_state == "ready" else "#6d4c56") xysize (28, 1) yalign 0.5
        text msd_label style ("msd_prompt" if msd_state == "ready" else "msd_prompt_wait")
        add Solid("#ca2d4a" if msd_state == "ready" else "#6d4c56") xysize (28, 1) yalign 0.5

    add Solid("#3a1520") xpos 520 ypos 694 xysize (240, 1)
    if msd_state == "receiving":
        if msd_lit():
            add msd_quad(240, 1) xpos 520 ypos 694 at msd_progress_lit(msd_secs)
        else:
            add Solid("#ca2d4a") xpos 520 ypos 694 xysize (240, 1) at msd_progress_flat(msd_secs)
    elif msd_state == "ready" and msd_lit() and msd_alive():
        add msd_quad(240, 1) xpos 520 ypos 694 at msd_progress_done
    else:
        add Solid("#ca2d4a") xpos 520 ypos 694 xysize (240, 1)


screen main_story_disclaimer_static_card(msd_title="", msd_message="", msd_page=1, msd_total=1):
    use main_story_disclaimer_backdrop

    vbox:
        xpos 164
        ypos 126
        spacing 14

        text "ENTER M // MAIN STORY" style "msd_masthead"
        use msd_header(msd_page, msd_total)
        use msd_title_block(msd_title, "idle")
        use msd_title_rule
        text msd_message style "msd_card_copy"

    use msd_side_panel
    use msd_prompt("SIGNAL CLOSING", "closing")


# =============================================================================
#  CARD SCREEN
# =============================================================================

screen main_story_disclaimer_card(msd_title="", msd_message="", msd_page=1, msd_total=1):
    modal True
    use main_story_disclaimer_backdrop

    vbox:
        xpos 164
        ypos 126
        spacing 14

        text "ENTER M // MAIN STORY" style "msd_masthead"
        use msd_header(msd_page, msd_total)
        use msd_title_block(msd_title, "idle" if msd_card_ready else "reveal")
        use msd_title_rule

        if msd_card_ready:
            # Rebuild the Text displayable without slow_cps when an early
            # advance resolves the card, so the visible copy cannot lag behind
            # the cursor and blip cleanup.
            text msd_message:
                style "msd_card_copy"
        else:
            text msd_message:
                style "msd_card_copy"
                slow_cps 42
                at msd_copy_reveal

    use msd_side_panel

    if msd_card_ready:
        use msd_prompt("CLICK TO CONTINUE", "ready")
    else:
        use msd_prompt("RECEIVING...", "receiving", len(msd_message) / 42.0)

    if msd_cover_phase == "open":
        use main_story_disclaimer_terminal_cover(msd_cover_phase)
        timer 0.78 action SetVariable("msd_cover_phase", "none")

    if msd_type_cursor < len(msd_message):
        timer (2.0 / 42.0) action Function(msd_play_type_blip, msd_message) repeat True

    # Unlock after the copy has finished its type-on pass, not merely after a
    # fixed entrance beat. An early dismiss uses the same finish path, so the
    # copy, cursor, and audio all resolve together instead of racing ahead.
    timer (0.72 + len(msd_message) / 42.0 + 0.10) action Function(msd_finish_receiving, msd_message)
    key "dismiss" action (Return() if msd_card_ready else Function(msd_finish_receiving, msd_message))


# =============================================================================
#  CHOICE SCREEN
# =============================================================================

screen main_story_disclaimer_choice(items):
    modal True
    use main_story_disclaimer_backdrop

    vbox:
        xpos 164
        ypos 126
        spacing 14

        text "ENTER M // MAIN STORY" style "msd_masthead"
        use msd_header(1, 1, "AWAITING RESPONSE", False)
        use msd_title_block("CONSENT REQUIRED", "idle")
        use msd_title_rule
        text "By proceeding, you agree to the contents within." style "msd_card_copy" at msd_copy_reveal

    vbox:
        xpos 164
        ypos 455
        spacing 12

        if items:
            for i in items:
                textbutton i.caption:
                    style "msd_choice_button"
                    action i.action
                    at (msd_choice_fx if msd_lit() else msd_noop)
        else:
            # This fallback keeps the screen self-describing if a caller opens
            # it as a preview instead of through a Ren'Py menu statement.
            textbutton "Proceed":
                style "msd_choice_button"
                action NullAction()
                at (msd_choice_fx if msd_lit() else msd_noop)
            textbutton "Do not proceed":
                style "msd_choice_button"
                action NullAction()
                at (msd_choice_fx if msd_lit() else msd_noop)

    text "SELECT AN OPTION" style "msd_side_label" xpos 876 ypos 455
    text "THE SIGNAL WILL WAIT" style "msd_side_value" xpos 876 ypos 487


# =============================================================================
#  STYLES
# =============================================================================

style msd_masthead is default:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 17
    color "#d7b8bf"
    kerning 1.0
    outlines []

style msd_eyebrow is default:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 17
    color "#c5334e"
    kerning 1.0
    outlines []

style msd_page_count is default:
    font "assets/gui/font/VerilySerifMono.otf"
    size 17
    color "#806c73"
    outlines []

style msd_card_title is default:
    font "assets/gui/font/F25_Bank_Printer.ttf"
    size 43
    color "#f1e6e7"
    kerning 1.0
    outlines [(1, "#761c35", 0, 0)]

# The chromatic ghosts: the title's own metrics, no outline, colored per call.
style msd_card_title_ghost is msd_card_title:
    outlines []

style msd_card_copy is default:
    font "assets/gui/font/VerilySerifMono.otf"
    size 28
    color "#e4d8dc"
    line_spacing 8
    xmaximum 680
    # The screen owns early-advance behavior so Text cannot reveal itself
    # without also resolving the cursor and stopping its blip channels.
    slow_abortable False
    outlines []

style msd_side_label is default:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 15
    color "#c5334e"
    kerning 1.0
    outlines []

style msd_side_value is default:
    font "assets/gui/font/VerilySerifMono.otf"
    size 14
    color "#927984"
    outlines []

style msd_prompt is default:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 16
    color "#ca2d4a"
    kerning 1.0
    outlines []

style msd_prompt_wait is default:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 16
    color "#6d4c56"
    kerning 1.0
    outlines []

style msd_terminal_status is default:
    font "assets/gui/font/F25_Bank_Printer.ttf"
    size 18
    color "#e4a3ad"
    kerning 1.0
    outlines [(1, "#260812", 0, 1)]

style msd_choice_button:
    background msd_button_plate(False)
    hover_background msd_button_plate(True)
    padding (24, 10, 22, 10)
    xsize 470
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style msd_choice_button_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 19
    color "#d5bdc3"
    hover_color "#ffffff"
    kerning 0.5
    outlines []


# =============================================================================
#  LABELS
# =============================================================================

label msd_enter:
    $ msd_stop_type_blips()
    $ msd_prev_quick_menu = quick_menu
    $ msd_active = True
    $ msd_cover_phase = "open" if _preferences.transitions != 0 else "none"
    $ quick_menu = False
    scene black with Dissolve(0.45)
    $ renpy.music.set_volume(0.28, delay=0.0, channel="msd_ambience")
    $ renpy.music.play(audio.heartbeat_ominous, channel="msd_ambience", loop=True, fadein=0.8)
    $ renpy.pause(0.12)
    return


label msd_card(msd_title="", msd_message="", msd_page=1, msd_total=1):
    $ msd_stop_type_blips()
    $ msd_card_ready = False
    $ msd_type_cursor = 0
    $ msd_type_channel_cursor = 0
    $ msd_last_title = msd_title
    $ msd_last_message = msd_message
    $ msd_last_page = msd_page
    $ msd_last_total = msd_total
    call screen main_story_disclaimer_card(msd_title, msd_message, msd_page, msd_total)
    $ msd_card_ready = False
    return


label msd_exit:
    $ msd_stop_type_blips()
    $ msd_active = False
    $ quick_menu = msd_prev_quick_menu
    if _preferences.transitions != 0:
        show screen main_story_disclaimer_closing
        $ renpy.pause(0.78, hard=True)
        hide screen main_story_disclaimer_closing
    $ msd_cover_phase = "none"
    $ renpy.music.stop(channel="msd_ambience", fadeout=0.65)
    scene black with Dissolve(0.35)
    return
