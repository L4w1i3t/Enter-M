# =============================================================================
# mm_ui.rpy  --  "A FINE DATE" :: THE SHELL SHE BUILT
# =============================================================================
#
# WHY THIS FILE EXISTS
#   The date used to be a visual novel with a health bar bolted on. Background,
#   sprite, the game's own dialogue box, a vertical list of buttons, a red bar
#   across the top -- every single element was the one the rest of ENTER-M uses,
#   which meant the mode's whole identity was carried by overlays laid on top of
#   a shape the player already knew. You could describe it accurately as "DDLC,
#   but there is a boss bar".
#
#   This file gives it a shape of its own. Not a skin on the VN -- a DIFFERENT
#   OBJECT that the fight happens inside.
#
# THE OBJECT
#   Monika is running a dating sim. She built it herself, out of memory, in a
#   room that does not want it, and it is the only thing she has. So the mode's
#   UI is HER dating sim: glossy pastel cards with rounded corners and a sheen
#   on them, an AFFECTION gauge with a heart on it, a scene counter, an evening
#   clock, sparkles drifting over a soft-focused CG. Every piece of chrome is
#   sweeter than anything else in this project, on purpose.
#
#   And every piece of it is FAILING. One uniform -- u_break -- runs through the
#   whole shell. At zero it is a mint-condition dating sim. As her gauge falls,
#   the same shader eats the card edges with noise, drains the gloss, pulls the
#   colour out toward ash, and lets the rims split. The cards do not get
#   REPLACED by corrupted cards; they are the same cards, deteriorating, which
#   is the difference between a glitch effect and a character arc.
#
# THE DISSONANCE, MADE LITERAL
#   There are now TWO grades fighting over the frame, and they are supposed to
#   be visibly incompatible:
#
#     mm.softfocus + mm.sparkle   HER filter. Warm, rose, bloomed, glittering.
#                                 It gets STRONGER each phase, not weaker --
#                                 she pushes harder as it stops working.
#     msbf.postfx (mm_corruption) THE ROOM's. Cold, dark red, grain, scanlines,
#                                 already in place before this file existed.
#
#   Her layer sits UNDER the room's, so the room is always the thing that wins
#   the pixel. What the player sees is a saccharine picture being pressed flat
#   by something that hates it. That contrast is the entire thesis of the mode
#   and it used to be carried by one vignette shader.
#
# WHAT REPLACED WHAT
#   mm_say            -> the game's dialogue box. A cream card with a heart
#                        nameplate overlapping its top edge and DARK text on a
#                        LIGHT ground, which is the single fastest way to say
#                        "you are not in the same game any more".
#   mm_timed_choice   -> was a vertical stack of textbuttons. Now three tilted
#                        cards fanned like a hand, under a HEART DIAL whose ring
#                        is the countdown -- the timer is a beating heart
#                        running out, not a bar draining.
#   mm_stage          -> was a 900px red boss bar. Now an AFFECTION gauge, a
#                        scene counter, and an evening clock that never moves.
#   mm_setpiece       -> was `scene x with mm_static`. The static is still
#                        there; the new background now also ARRIVES, tilted and
#                        oversized and settling, like a card being laid down.
#
# THE LABEL IS THE STORY
#   mm_gauge_label() walks AFFECTION -> ATTENTION -> ANYTHING -> PLEASE as she
#   falls. Nothing else in the mode states what is happening to her as plainly
#   as her own UI relabelling its meter.
#
# THE ONE STRUCTURAL RULE HERE
#   The mod's `style frame` is themed (a Frame() background plus border
#   padding), so a fixed-size `frame` shoves its own contents around. Every box
#   in this file is drawn as a shader card or a Solid with EXPLICITLY POSITIONED
#   text inside a `fixed`. See the custom say-UI project note.
# =============================================================================


# -----------------------------------------------------------------------------
# 1. SHADERS
# -----------------------------------------------------------------------------
# Namespace `mm.` -- nothing else in the project claims it. register_shader
# SILENTLY replaces a name that is already taken, and the crash then surfaces in
# whatever OTHER file was using it, so the namespace matters.
init python:

    def _mm_register_shaders():

        # Shared helpers. Every card, dial and mote in the mode comes out of
        # these, so the shell has one grain and one dither rather than five.
        MM_LIB = """
            float mm_hash(vec2 p) {
                return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
            }
            float mm_noise(vec2 p) {
                vec2 i = floor(p);
                vec2 f = fract(p);
                f = f * f * (3.0 - 2.0 * f);
                float a = mm_hash(i);
                float b = mm_hash(i + vec2(1.0, 0.0));
                float c = mm_hash(i + vec2(0.0, 1.0));
                float d = mm_hash(i + vec2(1.0, 1.0));
                return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
            }
            // Interleaved-gradient noise, used as a half-code-value dither.
            // Everything in this file is a big smooth pastel ramp, which is
            // exactly the signal an 8-bit framebuffer bands on.
            float mm_ign(vec2 p) {
                return fract(52.9829189 * fract(dot(p, vec2(0.06711056, 0.00583715))));
            }
            // Rounded-rectangle signed distance, in pixels. Negative inside.
            float mm_box(vec2 p, vec2 half_size, float r) {
                vec2 d = abs(p) - (half_size - vec2(r));
                return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0) - r;
            }
        """

        # ---- THE CARD ------------------------------------------------------
        # One shader for every panel in the mode: the dialogue box, the option
        # cards, the nameplate, the gauge housing, the scene chip. They all
        # share a rounded body, a vertical pastel gradient, a gloss band across
        # the top third and a rim -- and they all break the same way, because
        # they are all the same object at different sizes.
        #
        # u_break is the whole degradation arc:
        #   the edge is eaten by noise (so the card stops being a clean shape),
        #   the gloss goes (so it stops being new),
        #   the fill desaturates toward ash (so it stops being sweet),
        #   and the rim splits into dashes (so it stops holding together).
        renpy.register_shader("mm.card", variables="""
            uniform vec2 u_model_size;
            uniform float u_time;
            uniform vec3 u_mm_top;
            uniform vec3 u_mm_bot;
            uniform vec3 u_mm_rim;
            uniform float u_mm_radius;
            uniform float u_mm_alpha;
            uniform float u_mm_break;
            uniform float u_mm_gloss;
            varying vec2 v_tex_coord;
        """, fragment_functions=MM_LIB, fragment_300="""
            vec2 size = u_model_size;
            vec2 p = (v_tex_coord - 0.5) * size;
            float brk = clamp(u_mm_break, 0.0, 1.0);

            float sd = mm_box(p, size * 0.5, max(1.0, u_mm_radius));

            // EROSION. A slow noise field pushed into the distance function, so
            // the card is not overlaid with damage -- its actual silhouette is
            // being eaten. Two frequencies: a coarse one that takes bites, and
            // a fine one that roughens what is left.
            float e1 = mm_noise(p * 0.055 + vec2(u_time * 0.06, u_time * 0.03));
            float e2 = mm_noise(p * 0.31 - vec2(0.0, u_time * 0.11));
            sd += brk * (1.5 + 7.0 * e1 + 2.5 * e2);

            float body = smoothstep(1.2, -1.2, sd);
            float rim = smoothstep(2.8, 0.4, abs(sd + 1.7));

            // The rim breaks into dashes rather than fading, so a failing card
            // reads as coming apart instead of as going transparent.
            float dash = mix(1.0, step(0.34, mm_noise(p * 0.5 + vec2(u_time * 0.2, 0.0))), brk);
            rim *= dash;

            vec3 fill = mix(u_mm_top, u_mm_bot, clamp(v_tex_coord.y, 0.0, 1.0));

            // The sheen. This is most of what makes the shell read as a dating
            // sim rather than as a UI panel, so it is the first thing u_break
            // takes away.
            float gloss = smoothstep(0.46, 0.0, v_tex_coord.y);
            fill += vec3(1.0) * gloss * 0.20 * u_mm_gloss * (1.0 - brk * 0.9);

            // Colour drains toward ash. Not to black -- to a dead neutral, so
            // the card looks bleached rather than shadowed.
            float lum = dot(fill, vec3(0.299, 0.587, 0.114));
            fill = mix(fill, vec3(lum * 0.62), brk * 0.86);
            vec3 rimc = mix(u_mm_rim, vec3(lum * 0.85), brk * 0.7);

            vec3 col = mix(fill, rimc, clamp(rim, 0.0, 1.0));
            float a = clamp(max(body * u_mm_alpha, rim), 0.0, 1.0);
            a = clamp(a + (mm_ign(gl_FragCoord.xy) - 0.5) * 0.0039, 0.0, 1.0);

            gl_FragColor = vec4(min(col * a, vec3(a)), a);
        """)

        # ---- THE HEART DIAL ------------------------------------------------
        # The quicktime countdown. It replaced a bar draining left to right,
        # which is the most generic timer there is and told the player nothing
        # about what was being spent. A ring unwinding clockwise from twelve
        # around a beating heart says the thing the mode is about: the time you
        # have is HER patience, and it is running out in a circle.
        #
        # u_mm_prog is time REMAINING, 1 -> 0, animated from ATL.
        renpy.register_shader("mm.dial", variables="""
            uniform float u_time;
            uniform vec3 u_mm_col;
            uniform vec3 u_mm_col2;
            uniform float u_mm_prog;
            uniform float u_mm_thick;
            varying vec2 v_tex_coord;
        """, fragment_functions=MM_LIB, fragment_300="""
            vec2 d = v_tex_coord - 0.5;
            float r = length(d) * 2.0;
            float prog = clamp(u_mm_prog, 0.0, 1.0);

            // Clockwise from twelve, 0..1.
            float t = atan(d.x, -d.y) / 6.2831853;
            if (t < 0.0) t += 1.0;

            float band = smoothstep(u_mm_thick, u_mm_thick * 0.35, abs(r - 0.76));

            // A full faint circle underneath, so the arc is read against the
            // time it started with rather than floating on its own.
            float track = band * 0.14;
            float arc = band * step(t, prog);

            // The leading tip, which is the part the eye actually tracks.
            float tip = band * smoothstep(0.030, 0.0, abs(t - prog)) * 1.6;

            // Rose while there is time, red when there is not, and it starts
            // flashing under a fifth left.
            vec3 col = mix(u_mm_col2, u_mm_col, clamp(prog * 1.7, 0.0, 1.0));
            float panic = (1.0 - smoothstep(0.0, 0.22, prog))
                        * (0.5 + 0.5 * sin(u_time * 22.0));

            float a = clamp(track + arc * (0.85 + 0.35 * panic) + tip, 0.0, 1.0);
            col += vec3(1.0, 0.55, 0.68) * panic * arc * 0.5;

            a = clamp(a + (mm_ign(gl_FragCoord.xy) - 0.5) * 0.0039, 0.0, 1.0);
            gl_FragColor = vec4(min(col * a, vec3(a)), a);
        """)

        # ---- HER FILTER, PART ONE: SOFT FOCUS ------------------------------
        # Applied to the BACKGROUND, so it has a texture to work on. A cheap
        # four-tap bloom lifted out of the bright end plus a rose warm grade:
        # the look every dating sim puts on its CGs, and the exact opposite of
        # what the arena's grade is doing to the same pixels a layer later.
        #
        # u_mm_sweet RISES with her desperation. That is deliberate and it is
        # the joke: the worse the evening goes, the harder she pushes the
        # romance filter, until the picture is glazed to the point of illness.
        renpy.register_shader("mm.softfocus", variables="""
            uniform sampler2D tex0;
            uniform float u_time;
            uniform float u_mm_sweet;
            uniform float u_mm_break;
            varying vec2 v_tex_coord;
        """, fragment_functions=MM_LIB, fragment_300="""
            vec2 uv = v_tex_coord;
            vec4 c = texture2D(tex0, uv);
            float sweet = clamp(u_mm_sweet, 0.0, 1.5);
            float brk = clamp(u_mm_break, 0.0, 1.0);

            vec2 e = vec2(0.0042, 0.0075) * (0.6 + sweet);
            vec3 b = texture2D(tex0, uv + vec2( e.x,  e.y)).rgb
                   + texture2D(tex0, uv + vec2(-e.x,  e.y)).rgb
                   + texture2D(tex0, uv + vec2( e.x, -e.y)).rgb
                   + texture2D(tex0, uv + vec2(-e.x, -e.y)).rgb;
            b *= 0.25;

            float lum = dot(b, vec3(0.299, 0.587, 0.114));
            vec3 bloom = b * smoothstep(0.38, 0.98, lum);

            vec3 col = c.rgb + bloom * (0.62 * sweet);

            // The rose grade, and a soft halo toward the middle of the frame.
            vec3 warm = col * vec3(1.10, 0.93, 1.02) + vec3(0.045, 0.006, 0.028);
            col = mix(col, warm, clamp(sweet, 0.0, 1.0));
            float halo = 1.0 - smoothstep(0.10, 0.85, length(uv - vec2(0.5, 0.46)));
            col += vec3(1.0, 0.72, 0.84) * halo * 0.06 * sweet;

            // What the room does to it: the filter survives, but the colour
            // underneath it does not.
            float glum = dot(col, vec3(0.299, 0.587, 0.114));
            col = mix(col, vec3(glum) * vec3(1.06, 0.90, 0.94), brk * 0.55);

            // tex0 is ALREADY premultiplied, so this clamps rather than
            // multiplies: the invariant a custom body shader has to hold is
            // col <= alpha (a pixel brighter than its own alpha ADDS light
            // under gl2's src + dst*(1-a) blend, which is how a sprite's
            // transparent plate rectangle turns into a glowing box). Scaling
            // by c.a a second time would instead darken every soft edge.
            gl_FragColor = vec4(min(col, vec3(c.a)), c.a);
        """)

        # ---- HER FILTER, PART TWO: SPARKLE ---------------------------------
        # Drifting bokeh motes over the scene, additive, three parallax layers
        # on a hashed grid. Pure decoration and completely unearned by anything
        # happening in the room, which is the point -- somebody is dressing this
        # evening up.
        renpy.register_shader("mm.sparkle", variables="""
            uniform float u_time;
            uniform vec3 u_mm_col;
            uniform float u_mm_sweet;
            uniform float u_mm_break;
            varying vec2 v_tex_coord;
        """, fragment_functions=MM_LIB, fragment_300="""
            vec2 uv = v_tex_coord;
            float sweet = clamp(u_mm_sweet, 0.0, 1.5);
            float brk = clamp(u_mm_break, 0.0, 1.0);

            float a = 0.0;
            for (int i = 0; i < 3; i++) {
                float fi = float(i);
                float sc = 5.0 + fi * 4.5;
                vec2 g = uv * vec2(sc * 1.78, sc);
                g.y -= u_time * (0.055 + 0.045 * fi);
                vec2 id = floor(g);
                vec2 f = fract(g) - 0.5;
                float h = mm_hash(id + fi * 37.0);
                float on = step(0.80, h);
                vec2 off = vec2(mm_hash(id + 11.3) - 0.5,
                                mm_hash(id + 23.7) - 0.5) * 0.62;
                float dd = length(f - off);
                float tw = 0.5 + 0.5 * sin(u_time * (1.8 + 3.4 * h) + h * 31.0);
                a += on * smoothstep(0.15, 0.0, dd) * (0.30 + 0.70 * tw)
                        * (0.55 - 0.13 * fi);
            }

            // A little lens veil across the upper left, so the motes read as
            // being IN a lens rather than painted on the glass.
            float veil = smoothstep(0.9, 0.0, length(uv - vec2(0.24, 0.20))) * 0.05;

            a = clamp((a + veil) * sweet * (1.0 - brk * 0.35), 0.0, 1.0);
            vec3 col = mix(u_mm_col, vec3(1.0, 0.86, 0.90), 0.35);
            a = clamp(a + (mm_ign(gl_FragCoord.xy) - 0.5) * 0.0039, 0.0, 1.0);
            gl_FragColor = vec4(min(col * a, vec3(a)), a);
        """)

    try:
        _mm_register_shaders()
        MM_SHADERS = True
    except Exception as _mm_shader_e:
        MM_SHADERS = False
        if config.developer:
            renpy.log("MM UI: shader registration failed: %r" % (_mm_shader_e,))


# -----------------------------------------------------------------------------
# 2. THE SKIN
# -----------------------------------------------------------------------------
# One table, four states, read by every screen below. Nothing in this file picks
# its own colours: the shell has exactly one palette at any moment and it is a
# function of how far she has fallen.
init -1 python:

    # break / gloss / sweet, plus the ink the text is set in and the two card
    # colours. Phase 1 is a mint-condition dating sim; the last-resort row is
    # what is left of it.
    MM_SKIN = {
        1: {
            "break": 0.00, "gloss": 1.00, "sweet": 0.55,
            "top": (1.00, 0.96, 0.97), "bot": (0.99, 0.86, 0.90),
            "rim": (1.00, 0.55, 0.71), "ink": "#4a1f33", "sub": "#96566e",
            "accent": "#ff5c8a",
        },
        2: {
            "break": 0.30, "gloss": 0.72, "sweet": 0.80,
            "top": (0.97, 0.90, 0.92), "bot": (0.88, 0.74, 0.79),
            "rim": (1.00, 0.42, 0.60), "ink": "#3a1826", "sub": "#8a4a60",
            "accent": "#ff4470",
        },
        3: {
            "break": 0.66, "gloss": 0.34, "sweet": 1.10,
            "top": (0.80, 0.74, 0.76), "bot": (0.60, 0.53, 0.56),
            "rim": (0.95, 0.24, 0.42), "ink": "#1e0d15", "sub": "#6b4150",
            "accent": "#ff2b55",
        },
        4: {
            "break": 0.94, "gloss": 0.10, "sweet": 1.40,
            "top": (0.62, 0.58, 0.60), "bot": (0.40, 0.36, 0.38),
            "rim": (1.00, 0.14, 0.30), "ink": "#120309", "sub": "#5a3340",
            "accent": "#ff0033",
        },
    }

    def mm_skin():
        """The live skin row. Row 4 is the last-resort barrage, which is not a
        phase -- it is what happens after phase 3 runs out."""
        if getattr(store, "mm_lr_active", False):
            return MM_SKIN[4]
        return MM_SKIN.get(getattr(store, "mm_phase", 1), MM_SKIN[1])

    # THE LABEL IS THE STORY. She built this gauge to measure how much you like
    # her. When that stops being a question she can afford to ask, the gauge
    # starts measuring something smaller, and it keeps doing that until it is
    # measuring whether you will give her anything at all.
    MM_GAUGE_LABELS = {1: "AFFECTION", 2: "ATTENTION", 3: "ANYTHING", 4: "PLEASE"}

    def mm_gauge_label():
        if getattr(store, "mm_lr_active", False):
            return MM_GAUGE_LABELS[4]
        return MM_GAUGE_LABELS.get(getattr(store, "mm_phase", 1), "AFFECTION")

    def mm_gauge_pct():
        try:
            return int(round(100.0 * store.mm_monika_hp / float(store.mm_monika_max)))
        except Exception:
            return 0

    def mm_card(w, h, radius=18, alpha=0.97, skin=None, gloss=None, brk=None):
        """
        The shell's one panel primitive.

        Returns a displayable already sized to (w, h). Falls back to a flat
        Solid without gl2 -- the mode stays entirely playable, it just loses the
        thing that makes it look like hers.
        """
        skin = skin or mm_skin()
        if not MM_SHADERS:
            return Transform(Solid("#f2dbe2f2" if skin["break"] < 0.5 else "#6a6265f2"),
                             xysize=(int(w), int(h)))
        return Transform(
            Solid("#00000000"),
            xysize=(int(w), int(h)),
            mesh=True,
            shader="mm.card",
            u_mm_top=skin["top"],
            u_mm_bot=skin["bot"],
            u_mm_rim=skin["rim"],
            u_mm_radius=float(radius),
            u_mm_alpha=float(alpha),
            u_mm_break=float(skin["break"] if brk is None else brk),
            u_mm_gloss=float(skin["gloss"] if gloss is None else gloss),
        )

    def mm_scene_no():
        return int(getattr(store, "mm_scene_count", 0) or 0)

    def mm_bg_at(deal=True):
        """
        The at_list every background in the date is shown with.

        ORDER IS THE ARGUMENT. Her soft focus goes on FIRST, so it is the
        innermost transform and it treats the raw plate: bloom, rose grade,
        halo. The room's datamosh goes on SECOND, from phase 2, so it chews on
        an image she has already made pretty. Reverse those and the mode says
        something else entirely -- that the room damages a picture and she
        prettifies the damage, which is not what is happening to her.

        mm_deal comes last because it is the only one that is not a filter: it
        is the motion of the plate being put down, and a modifier layered
        OUTSIDE a pose would take the pose's state with it (see the at_list /
        take_state note in the project memory).
        """
        skin = mm_skin()
        at = []
        if MM_SHADERS:
            at.append(store.mm_softfocus(skin["sweet"], skin["break"]))
        if ((getattr(store, "mm_phase", 1) >= 2 or getattr(store, "mm_lr_active", False))
                and getattr(store, "MSBF_FX_SHADERS", False)):
            ph = getattr(store, "mm_phase", 1)
            at.append(store.msbf_fx_glitch_pulse(0.08 + 0.04 * ph, 0.4 + 0.1 * ph, 18.0))
        if deal:
            at.append(store.mm_deal)
        return at


# The evening never actually gets anywhere. Matsuda gave her one evening, and
# this clock has been reading the same minute since the first scene -- it is set
# once, at the top, and no code ever advances it. Nobody will notice on the
# first run and everybody notices on the second.
define MM_CLOCK = "7:41 PM"

# How many scenes she has staged. Incremented by mm_setpiece, so it counts what
# the player has actually been shown rather than what the loop has run.
default mm_scene_count = 0


# -----------------------------------------------------------------------------
# 3. TRANSFORMS
# -----------------------------------------------------------------------------

# Her filter, on the background plate.
transform mm_softfocus(sweet=0.55, brk=0.0):
    mesh True
    shader "mm.softfocus"
    u_mm_sweet sweet
    u_mm_break brk

# The heart dial's countdown. The ring is animated by ATL rather than by a
# screen timer for the same reason the last-resort meter is: a repeating timer
# would restart the interaction twenty times a second and reset the very
# countdown it was drawing.
transform mm_dial_t(secs=2.8, col=(1.0, 0.36, 0.54), col2=(1.0, 0.10, 0.22)):
    mesh True
    shader "mm.dial"
    u_mm_col col
    u_mm_col2 col2
    u_mm_thick 0.085
    u_mm_prog 1.0
    linear secs u_mm_prog 0.0

# A card being laid down. The background does not cut in any more -- it arrives
# slightly too big and slightly off-square and settles, which is the difference
# between a scene change and somebody SETTING A SCENE.
transform mm_deal:
    subpixel True
    align (0.5, 0.5)
    zoom 1.075
    rotate 1.4
    alpha 0.0
    parallel:
        easeout 0.44 zoom 1.0
    parallel:
        easeout 0.52 rotate 0.0
    parallel:
        linear 0.16 alpha 1.0

# The option cards' resting tilt. Each card in the fan gets its own, so the
# three of them read as a hand rather than as a list. rotate_pad is left at its
# default True: the padding is symmetric about the centre and the call site
# re-centres the result, so nothing is clipped and nothing moves.
transform mm_fan(deg=0.0):
    subpixel True
    rotate deg

# Hover: the card lifts out of the fan, the way a card you are about to play
# does. No rotation in here -- see the note at the call site.
transform mm_fan_lift:
    subpixel True
    yoffset 0
    zoom 1.0
    on hover:
        easeout 0.16 yoffset -16 zoom 1.04
    on idle:
        easeout 0.22 yoffset 0 zoom 1.0

# The gauge's fill, which does not snap. A number that moves instantly reads as
# a variable; a number that eases reads as something being taken.
transform mm_gauge_ease:
    subpixel True

# The nameplate's small constant unsteadiness, once she is past pretending.
transform mm_plate_slip(amount=0.0):
    subpixel True
    block:
        ease 1.7 xoffset amount yoffset (amount * 0.35)
        ease 1.9 xoffset (-amount) yoffset (-amount * 0.2)
        repeat

# Continue-marker heart at the corner of the dialogue card.
transform mm_ctc_beat:
    subpixel True
    transform_anchor True
    anchor (0.5, 0.5)
    alpha 0.0
    block:
        pause 0.28
        linear 0.18 alpha 1.0
        block:
            easeout 0.10 zoom 1.18
            easein 0.16 zoom 1.0
            pause 0.62
            repeat


# -----------------------------------------------------------------------------
# 4. HER FILTER AS A SCREEN LAYER
# -----------------------------------------------------------------------------
# The sparkles. zorder -8 puts them over the scene and the sprite but UNDER
# mm_corruption (-5), which is the whole stacking argument of the mode: she gets
# to dress the evening, and then the room gets the last word on every pixel.
transform mm_sparkle_t(sweet=0.55, brk=0.0):
    mesh True
    shader "mm.sparkle"
    u_mm_col (1.0, 0.62, 0.76)
    u_mm_sweet sweet
    u_mm_break brk

screen mm_sparkle():
    zorder -8
    if MM_SHADERS:
        $ _mms = mm_skin()
        add Solid("#00000000") xysize (1280, 720) at mm_sparkle_t(_mms["sweet"], _mms["break"])


# -----------------------------------------------------------------------------
# 5. THE CHASSIS
# -----------------------------------------------------------------------------
# Everything that is always on screen during the date: the AFFECTION gauge, the
# scene counter, the evening clock, and four corner flourishes. This replaced
# mm_hud, which was a 900px red boss bar -- correct information, entirely the
# wrong object. A boss bar says "this is a fight". A gauge with a heart on it
# says "this is a date", and then empties when you are kind to her.
screen mm_stage():
    zorder 88

    $ _mms = mm_skin()
    $ _mm_pct = mm_gauge_pct()
    $ _mm_frac = max(0.0, min(1.0, _mm_pct / 100.0))
    $ _mm_low = _mm_frac < 0.28

    # --- the gauge ----------------------------------------------------------
    fixed:
        xpos 36
        ypos 28
        xysize (444, 84)

        add mm_card(444, 84, 20, 0.95, _mms)

        # The heart is the gauge's icon AND its pulse: steady while she is
        # composed, arrhythmic once she is not (mm_heartbeat_arr lives in
        # monika_date.rpy with the rest of the motif).
        if _mms["break"] > 0.55:
            add "mm_heart" at mm_heartbeat_arr(42, 42, 0.42, 0.18):
                xcenter 78
                ycenter 70
        else:
            add "mm_heart" at mm_heartbeat(42, 42, (0.70 if _mms["break"] > 0.1 else 1.1)):
                xcenter 78
                ycenter 70

        text mm_gauge_label():
            style "mm_gauge_label"
            color _mms["sub"]
            xpos 112
            ypos 20

        text "[_mm_pct]%":
            style "mm_gauge_pct"
            color (_mms["accent"] if _mm_low else _mms["ink"])
            xpos 412
            ypos 16
            xanchor 1.0

        # The fill. Drawn as plain Solids on purpose: it is a small, hard-edged,
        # high-contrast readout and it should stay crisp while everything around
        # it decays -- the one piece of the shell that never lies.
        # The card is 84 tall, so the bar's bottom edge has to clear y=84 or it
        # is cut off by its own housing.
        add Solid("#00000038") xpos 112 ypos 50 xysize (300, 14)
        if _mm_frac > 0.0:
            add Solid(_mms["accent"]) xpos 112 ypos 50 xysize (max(2, int(300 * _mm_frac)), 14)
            add Solid("#ffffff5c") xpos 112 ypos 50 xysize (max(2, int(300 * _mm_frac)), 5)

    # --- the evening -------------------------------------------------------
    fixed:
        xpos 1004
        ypos 28
        xysize (240, 84)

        add mm_card(240, 84, 20, 0.95, _mms)

        text "SCENE [mm_scene_count:02d]":
            style "mm_gauge_label"
            color _mms["sub"]
            xpos 22
            ypos 20

        text MM_CLOCK:
            style "mm_clock"
            color _mms["ink"]
            xpos 22
            ypos 44

    # --- corner flourishes --------------------------------------------------
    # Four small rose brackets. They are pure ornament, which is exactly why
    # they belong: nothing else in this project decorates its own edges, so
    # having them at all marks the frame as somebody's.
    $ _mm_corner = _mms["accent"]
    $ _mm_ca = 0.85 - 0.5 * _mms["break"]
    add Solid(_mm_corner) xpos 22 ypos 132 xysize (2, 54) alpha _mm_ca
    add Solid(_mm_corner) xpos 22 ypos 132 xysize (54, 2) alpha _mm_ca
    add Solid(_mm_corner) xpos 1256 ypos 132 xysize (2, 54) alpha _mm_ca
    add Solid(_mm_corner) xpos 1204 ypos 132 xysize (54, 2) alpha _mm_ca
    add Solid(_mm_corner) xpos 22 ypos 640 xysize (2, 54) alpha _mm_ca
    add Solid(_mm_corner) xpos 22 ypos 692 xysize (54, 2) alpha _mm_ca
    add Solid(_mm_corner) xpos 1256 ypos 640 xysize (2, 54) alpha _mm_ca
    add Solid(_mm_corner) xpos 1204 ypos 692 xysize (54, 2) alpha _mm_ca


# -----------------------------------------------------------------------------
# 6. THE DIALOGUE CARD
# -----------------------------------------------------------------------------
# DARK TEXT ON A LIGHT GROUND. That one decision does more to separate this mode
# from the rest of the game than every shader in this file: the player has read
# a hundred thousand words out of a dark box with pale text, and the instant the
# polarity flips they are somewhere else.
#
# Built from a shader card plus explicitly positioned text rather than a `frame`
# -- the mod's themed `style frame` injects a Frame() background and border
# padding that shoves the contents of a fixed-size box around.
screen mm_say(who, what):

    $ _mms = mm_skin()

    fixed:
        xpos 0
        ypos 0
        xysize (1280, 720)

        # The card.
        add mm_card(1088, 178, 22, 0.96, _mms):
            xpos 96
            ypos 508

        # The nameplate, overlapping the card's top edge -- the dating-sim
        # convention, and a shape the rest of the game never uses. Once she is
        # breaking it will not sit still on the box any more.
        fixed:
            xpos 130
            ypos 470
            xysize (296, 56)
            # Applied unconditionally with a scaled amount rather than switched
            # on by an `if`: a conditional `at` in the middle of a property
            # block is a different displayable tree on either side of the
            # branch, so the plate would restart its drift every time her phase
            # moved. At break 0 the amount is 0 and it simply sits still.
            at mm_plate_slip(11.0 * _mms["break"])

            add mm_card(296, 56, 18, 0.98, _mms, gloss=1.0)

            add "mm_heart" at mm_heartbeat(26, 26, (0.66 if _mms["break"] > 0.3 else 1.1)):
                xcenter 34
                ycenter 28

            if who is not None:
                text who:
                    style "mm_name"
                    color _mms["ink"]
                    xpos 60
                    ypos 14
                    xmaximum 220

        text what id "what":
            style "mm_dialogue"
            color _mms["ink"]
            xpos 140
            ypos 548
            xmaximum 1000

        # Continue marker: a small heart at the low corner of the card, beating
        # once the line has finished typing.
        add "mm_heart" at mm_ctc_beat:
            xysize (22, 22)
            fit "contain"
            xcenter 1146
            ycenter 660


# -----------------------------------------------------------------------------
# 7. THE QUICKTIME
# -----------------------------------------------------------------------------
# The single biggest change in the mode. This was a vertical stack of three
# textbuttons under a draining bar: the exact shape of every choice in every
# visual novel ever written, which meant the one moment the player is under
# real-time pressure looked identical to the one moment they are not.
#
# Now: three cards fanned like a hand, under a heart with a countdown ring
# wound round it. The pressure is legible without reading anything -- the ring
# is visibly shorter than it was, and the heart is going faster.
#
# The rig is unchanged. `shuffle` still decides whether the deck is dealt in
# order, and the last-resort barrage still passes shuffle=False so the correct
# answer is always the top -- which here means the LEFTMOST card.
screen mm_timed_choice(prompt, options, time_limit=3.0, shuffle=True):
    zorder 250
    modal True
    use enter_m_input_lock()

    default shuffled = (mm_shuffled(options) if shuffle else list(options))

    $ _mms = mm_skin()
    $ _mm_n = len(shuffled)

    # --- the dial -----------------------------------------------------------
    # 236px of ring with the heart inside it, centred over the fan. The heart
    # beats on the phase's rhythm and goes arrhythmic when she does, so the two
    # halves of the timer disagree with each other on purpose.
    fixed:
        xpos 522
        ypos 296
        xysize (236, 236)

        if MM_SHADERS:
            # The ring takes the phase's own rim colour, so it bleaches along
            # with every other piece of her chrome instead of staying mint while
            # the cards around it come apart.
            add Solid("#00000000") xysize (236, 236) at mm_dial_t(time_limit, _mms["rim"], (1.0, 0.10, 0.22))
        else:
            add Solid("#0a0c16") xpos 0 ypos 232 xsize 236 ysize 8
            add Solid("#ff2b55") xpos 0 ypos 232 ysize 8 at mm_drain_ring(time_limit)

        if _mms["break"] > 0.55:
            add "mm_heart" at mm_heartbeat_arr(104, 104, 0.34, 0.20):
                xcenter 118
                ycenter 118
        else:
            add "mm_heart" at mm_heartbeat(104, 104, (0.62 if _mms["break"] > 0.1 else 0.95)):
                xcenter 118
                ycenter 118

    # --- the prompt ---------------------------------------------------------
    # Above the dial, unboxed. It is her voice, not a piece of her UI, so it
    # does not get a card.
    text prompt:
        style "mm_prompt"
        color "#ffe6ee"
        xcenter 640
        ypos 246
        xmaximum 1080
        text_align 0.5

    # --- the fan ------------------------------------------------------------
    # Three cards, tilted outward from the middle and dropped slightly at the
    # edges so they sit on an arc. Ren'Py's own arrow focus moves between them
    # (enter_m_input_lock deliberately leaves focus_left/right alone for this
    # mode), and 1/2/3 pick one outright.
    #
    # TWO LAYOUT RULES ARE LOAD-BEARING HERE.
    #
    # 1. THE TILT IS ON THE INNER BOX, NOT ON THE BUTTON. `rotate` pads its
    #    render out to a SQUARE of the child's diagonal (rotate_pad defaults
    #    True), so rotating a 348x132 card makes a ~372x372 render. Rotating the
    #    BUTTON therefore resizes the button, which moves its hit box and its
    #    contents; rotating an inner box that is re-centred with xcenter/ycenter
    #    keeps the growth symmetric about the centre and nothing moves. The
    #    button gets a square MM_FAN_BOX so the padded card always fits inside
    #    the thing you are clicking.
    #
    # 2. HOVER ONLY REACHES A BUTTON'S DIRECT CHILD, so the lift transform goes
    #    on the button itself and carries no rotation -- if it rotated, every
    #    hover would resize the button under the pointer.
    $ _mm_slots = MM_FAN_SLOTS.get(_mm_n, MM_FAN_SLOTS[3])
    $ _mm_half = MM_FAN_BOX // 2

    for _mi, _opt in enumerate(shuffled):
        $ _mm_cx, _mm_deg, _mm_dy = _mm_slots[min(_mi, len(_mm_slots) - 1)]

        button:
            style "mm_option_button"
            xcenter _mm_cx
            ycenter (596 + _mm_dy)
            xysize (MM_FAN_BOX, MM_FAN_BOX)
            action Return(_opt[1])
            hover_sound MSBF_UI_SFX["hover"]
            activate_sound MSBF_UI_SFX["accept"]
            at mm_fan_lift

            fixed:
                xysize (MM_FAN_BOX, MM_FAN_BOX)

                fixed:
                    xysize (MM_FAN_W, MM_FAN_H)
                    xcenter _mm_half
                    ycenter _mm_half
                    at mm_fan(_mm_deg)

                    add mm_card(MM_FAN_W, MM_FAN_H, 16, 1.0, _mms)

                    # INTEGERS. A float position in Ren'Py is a FRACTION of the
                    # parent, not a pixel count, and Python 3 makes `w / 2` a
                    # float -- which is why these labels were being placed a
                    # hundred and eighty parent-widths off screen and the fan
                    # rendered as three blank cards.
                    text _opt[0]:
                        style "mm_option"
                        color _mms["ink"]
                        xcenter (MM_FAN_W // 2)
                        ycenter (MM_FAN_H // 2)
                        xmaximum (MM_FAN_W - 44)
                        text_align 0.5

    # Number keys, for the barrage. At 0.55s a prompt nobody is finding a card
    # with a pointer, and the deck is rigged to the leftmost anyway.
    key "K_1" action Return(shuffled[0][1])
    if _mm_n > 1:
        key "K_2" action Return(shuffled[1][1])
    if _mm_n > 2:
        key "K_3" action Return(shuffled[2][1])

    on "show" action Function(renpy.play, audio.sfx_beep, channel="sound")
    timer time_limit action Return("__timeout__")
    timer (time_limit * 0.5) action Function(renpy.play, audio.heartbeat, channel="sound")
    timer (time_limit * 0.8) action Function(renpy.play, audio.heartbeat, channel="sound")


# Fan geometry. (centre x, tilt in degrees, y drop) per slot, keyed by how many
# options the prompt carries. Kept as a table rather than computed so a deck of
# two never has to be a special case in the middle of the screen loop.
define MM_FAN_W = 348
define MM_FAN_H = 132

# The square the card is rotated inside. Has to clear the card's diagonal
# (sqrt(348^2 + 132^2) = 372) or `rotate`'s padding would be bigger than the
# button holding it.
define MM_FAN_BOX = 380

# (centre x, tilt in degrees, y drop) per slot. Spaced so the BUTTONS never
# overlap -- three 380px boxes at 250 / 640 / 1030 leave a clean 40px between
# each hit area, which matters because a mis-click at 1.5 seconds is a heal.
define MM_FAN_SLOTS = {
    1: [(640, 0.0, 0)],
    2: [(444, -4.5, 8), (836, 4.5, 8)],
    3: [(250, -6.5, 16), (640, 0.0, 0), (1030, 6.5, 16)],
    4: [(196, -8.0, 24), (444, -3.0, 6), (836, 3.0, 6), (1084, 8.0, 24)],
}

# Shaderless fallback for the dial: a plain bar under where the ring would be.
transform mm_drain_ring(t):
    xsize 236
    linear t xsize 0


# -----------------------------------------------------------------------------
# 8. STYLES
# -----------------------------------------------------------------------------
# The prose keeps the game's reading font. The chrome does not use NovaSquare
# even though it is the project's interface face: this shell is meant to look
# hand-made and sweet, and a squared-off technical face would make it read as a
# system panel. Numbers are the exception and always will be -- the display font
# draws a 1 as a bare vertical bar.

style mm_dialogue is default:
    font gui.default_font
    size 25
    line_spacing 3
    outlines []

style mm_name is default:
    font gui.default_font
    size 24
    bold True
    outlines []

style mm_gauge_label is default:
    font gui.default_font
    size 17
    bold True
    outlines []

style mm_gauge_pct is default:
    font "mod_assets/fonts/NovaSquare-Regular.ttf"
    size 26
    outlines []

style mm_clock is default:
    font "mod_assets/fonts/NovaSquare-Regular.ttf"
    size 24
    outlines []

style mm_prompt is default:
    font gui.default_font
    size 27
    color "#ffe6ee"
    outlines [(3, "#2a0010cc", 0, 0), (1, "#00000099", 1, 1)]

style mm_option is default:
    font gui.default_font
    size 23
    line_spacing 2
    outlines []

style mm_option_button is default:
    background None
    padding (0, 0)
