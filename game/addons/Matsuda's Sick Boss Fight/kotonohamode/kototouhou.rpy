# Kotonoha danmaku mode, reached through cs_matsuda_02's alternate roster.
# Eight standard bars each progress nonspell -> declare -> spell -> break.
# Endless draws nonspells, Mask cards and Soul cards without immediate repeats.
# Practice and developer readings provide unlimited lives and do not earn records.
# Controls: arrows move, Z shoots, X bombs, Shift focuses/shows the hitbox.
#
# KTGame owns simulation state. Pattern functions are attached to the class in
# their own block. KTStage advances the simulation at fixed 60Hz inside render()
# and draws cached displayables; screen code routes pause/quit/result input.
# Coordinates are local to the 620x680 playfield mounted at (KT_SX, KT_SY).
# Speeds are pixels/tick and timers are ticks unless explicitly named seconds.
# Lasers are separate telegraph/fire/fade segments with segment collision.
#
# Keep Render objects frame-local. Bound rotation/tint/scale cache keys and obey
# KT_MAX_BULLETS. New art needs KINDS, KT_KIND_HR and, when directional, KT_SPIN.
# Every sprite is this mode's own art (assets/bullets/kotonoha/, mapped by
# kt_atlas.json); rapid SFX use this file's own channel pools.
# Preserve persistent.kotomode_* record keys across source/asset cleanup.

image koto_backdrop = "addons/Matsuda's Sick Boss Fight/kotonohamode/kotobackdrop.png"

define -50 audio.kt_boss_theme = "<loop 0>assets/audio/bgm/kotobossmusic.ogg"
# Endless Mode gets its own loop -- a different, no-ending survival theme.
define -50 audio.kt_endless_theme = "<loop 0>assets/audio/bgm/kotoendlessmode.ogg"

# Persistent values live in Matsu'Py's save-independent persistent store. The
# rest are normal rollback-managed defaults used as script/displayable handoff
# state. The fight blocks rollback while running, but defaults are still the
# right declaration form so a fresh game has known values.
default persistent.kotomode_cleared = False
default persistent.kotomode_hiscore = 0
# Endless Mode keeps its OWN records: scores/waves there are not comparable to
# the fixed 8-bar run, so they live apart and never touch kotomode_cleared.
default persistent.kotomode_endless_hiscore = 0
default persistent.kotomode_endless_wave = 0
# Spell card HISTORY (the modern Touhou "History 03/12" line): card name ->
# [captures, attempts], counted on real readings only (never practice, debug
# or the wave viewer). Always REASSIGNED, never mutated in place, so the
# change is seen by the persistent save.
default persistent.kotomode_card_history = {}

# Active fight object. This is set only while kototouhou_screen is running and
# cleared immediately after call screen returns. Nothing outside the fight
# should expect this to survive.
default kt_game = None

# Result snapshot copied out of KTGame._finish(). The screen interaction returns
# only a small string ("victory", "defeat", "quit"), so these fields are how the
# story labels know what happened after the displayable is destroyed.
default kt_last_score = 0
default kt_last_graze = 0
default kt_last_captures = 0
default kt_last_bars = 0
default kt_last_bar_index = 0
default kt_last_practice = False
default kt_last_debug = False
default kt_last_deaths = 0
default kt_last_endless = False
default kt_last_endless_wave = 0

# Mode selection chosen in the VN menu before the screen is called. These feed
# KTGame.__init__ and then become immutable for that run.
default kt_practice = False
default kt_debug = False
# Endless Mode: same lives as a normal run, but the fight never ends -- random
# nonspells + spell cards escalate until you die. Set in kototouhou_mode_select.
default kt_endless = False
# kt_practice AND kt_endless together = Endless Practice: the endless hat of
# cards with practice rules (unlimited lives, no records of any kind). Nothing
# else encodes it; KTGame reads the two flags and the labels branch on both.

# Debug wave viewer (DEV ONLY): force one (nonspell, spell) pairing so a
# specific card/pattern can be tested without playing a whole run. The grid
# picker (kt_wave_picker) fills the indexes; the run reads that ONE bar and
# then finishes with "wave_done", which routes back to the mode selector.
# Both the entry label and the mode selector reset the flag.
default kt_debug_wave = False
default kt_dbwave_ns = 0
default kt_dbwave_sp = 0

# Continue support is intentionally conservative: current menus reset these to
# zero because Kotonoha asked for whole-fight restarts. They remain separate
# knobs so a future checkpoint/practice selector can start from a later bar
# without rewriting KTGame.
default kt_continue_bar = 0
default kt_continues = 0

# The whole arena breathes very slowly so the backdrop never reads as a JPEG.
#
# THIS IS NOT AN ATL TRANSFORM ANY MORE, AND IT MUST NOT BECOME ONE AGAIN.
# An ATL interpolation returns a redraw delay of ZERO for every frame it runs
# (renpy/atl.py, Interpolation.execute -> "continue", state, 0), which is a
# standing request for a new frame AS FAST AS THE PANEL WILL GIVE ONE. Parked
# on the fight screen, an 18-second zoom loop therefore pinned the whole
# interaction -- KTStage's several hundred blits included -- to the display's
# refresh rate, which is exactly what KTStage's own `renpy.redraw(self,
# KT_TICK - acc)` governor at the bottom of render() exists to prevent. On a
# 165Hz laptop panel that was ~2.75x the draw work for a picture that, between
# two simulation ticks, is byte-identical.
#
# So the breath lives INSIDE the displayable now (see the backdrop block at the
# top of KTStage.render), driven off g.tick instead of wall time, and the whole
# fight screen is static: KTStage is the only thing on it that ever asks for a
# frame. The curve is unchanged -- two 9-second `ease`s back to back are
# algebraically the raised cosine below, which is why this reads identically:
#
#     ease 9s 1.0 -> 1.035   ==   1.0 + 0.0175 * (1 - cos(pi * t / 9))
#     ease 9s 1.035 -> 1.0   ==   ...the second half of the same cosine.
define KT_BREATHE_PERIOD = 1080.0   # ticks for the full round trip (18s at 60Hz)
define KT_BREATHE_AMOUNT = 0.035    # peak zoom over rest
define KT_BREATHE_STEPS = 128       # zoom quantization (~0.35px a step: invisible)

# --- SHADERS (spell 5 darkness + the boss spell circle) ----------------------
# koto.spotlight: a GPU spotlight -- the stage goes dark except for a soft
# window around the player and a dimmer one around Kotonoha.
# koto.circle: a procedural Touhou "spell circle" -- concentric rings, a dashed
# band rotating one way, ticked and runed bands sweeping the other, and the
# whole sigil breathing in and out. Drawn behind the boss (her float anchor)
# and, small and fast, under the player while focused.
# Registered defensively like fx.rpy; on failure the fight plays without them.
#
# EVERY SHADER QUAD IN THIS FILE MUST PASS `mesh=True`. A `shader=` property on
# a Transform whose child is a Solid is IGNORED without it -- the child is a
# plain quad, not a mesh, so the shader never runs and the Solid draws exactly
# what it says it is: nothing. There is no warning, no exception, and the blits
# below are wrapped in `except Exception: pass`, so the failure mode is an
# effect that simply is not on screen. All nine quads here (veil, spell circle,
# boss aura, the four msbf.ring shockwaves, the focus sigil, the spell-5
# spotlight) shipped without it and none of them had ever drawn -- verified by
# rendering the same Transform with and without `mesh` side by side. If a GPU
# effect in this fight is missing, check this first.
init -9 python:
    KT_SHADER_OK = False

    def _kt_register_shaders():
        # GLSL note: v_tex_coord is normalized 0..1 across the quad. The shader
        # converts it back to stage pixels so "distance from player/boss" can be
        # expressed in the same pixel units as the rest of the fight.
        renpy.register_shader("koto.spotlight", variables="""
            uniform vec2 u_koto_p;
            uniform vec2 u_koto_b;
            uniform float u_koto_dark;
            uniform vec2 u_koto_res;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 px = v_tex_coord * u_koto_res;
            float dp = distance(px, u_koto_p);
            float db = distance(px, u_koto_b);
            // smoothstep(edge0, edge1, x) eases from 0 to 1 over a radius.
            // Inverting it makes a soft circular light: 1 near the subject,
            // 0 outside the feathered edge.
            float lp = 1.0 - smoothstep(96.0, 210.0, dp);
            float lb = (1.0 - smoothstep(60.0, 150.0, db)) * 0.75;
            // max(lp, lb) keeps whichever light is stronger at this pixel.
            // The final alpha is black everywhere EXCEPT those light cones.
            float a = u_koto_dark * (1.0 - max(lp, lb));
            gl_FragColor = vec4(0.0, 0.0, 0.0, a);
        """)

        # u_time is Matsu'Py's built-in frame clock, so the circle spins AND
        # breathes on the GPU with no per-frame python. Premultiplied output.
        # GLSL note: the circle shader is just polar-coordinate math:
        #   r   = distance from center of the quad
        #   ang = angle around that center
        # Then it layers thin rings, dashed arcs, spokes, and a center glow.
        #
        # WHY THE BREATH LIVES IN HERE and not in the python that builds the
        # quad: the quad's pixel size is a cache key (see the _misc note in
        # KTStage), so a python pulse that scaled it could only move in the 4px
        # steps that key quantizes to -- five discrete sizes cycling under every
        # spell card, which snapped instead of swelling. Dividing r by a breath
        # factor grows the pattern INSIDE a quad whose size never changes, so
        # there is nothing left to quantize and the swell is continuous.
        renpy.register_shader("koto.circle", variables="""
            uniform vec3 u_koto_col;
            uniform float u_koto_alpha;
            uniform float u_koto_spin;
            uniform float u_koto_breath;
            uniform float u_koto_scale;
            uniform float u_time;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 d = v_tex_coord - vec2(0.5);
            float ang = atan(d.y, d.x);
            float t = u_time * u_koto_spin;
            // Two sines at unrelated rates so the swell never lands on a
            // metronome beat. br > 1 pushes every feature outward.
            float br = 1.0 + u_koto_breath *
                (0.62 * sin(u_time * 0.85) + 0.38 * sin(u_time * 0.31 + 1.7));
            // u_koto_scale is the sigil's SIZE, continuous, on a quad whose
            // pixel dimensions never change. Dividing r scales the pattern
            // uniformly -- band widths included -- so this is pixel-identical
            // to having sized the quad itself, minus the quantization that
            // sizing a cached quad forces. Unset it reads as 1.0 rather than
            // dividing by zero and drawing nothing.
            float sc = (u_koto_scale > 0.0) ? u_koto_scale : 1.0;
            float r = (length(d) * 2.0) / (br * sc);
            // -1..1 swell, for the brightness lift that rides the breath.
            float swell = (br - 1.0) / max(u_koto_breath, 0.0001);
            float a = 0.0;
            // Outer ring. Held at 0.915 rather than out at the rim so a full
            // breath still has somewhere to expand before the quad clips it.
            a += smoothstep(0.035, 0.0, abs(r - 0.915)) * 0.9;
            // Inner ring, ticked into 15 segments turning WITH the spokes and
            // against the dash -- a plain circle here read as a static decal
            // no matter how fast everything around it moved.
            float tick = 0.55 + 0.45 * step(0.42, fract((ang + t * 0.45) * 2.3873));
            a += smoothstep(0.025, 0.0, abs(r - 0.60)) * 0.65 * tick;
            // Dashed band: fract() repeats around the circle, step() turns
            // every other segment on/off, and subtracting t rotates it.
            float dash = step(0.5, fract((ang - t) * 3.8197));
            a += smoothstep(0.09, 0.0, abs(r - 0.775)) * dash * 0.55;
            // Runes: six stubby marks orbiting just inside the outer ring on a
            // third rate again, so the sigil has three parts visibly moving at
            // three speeds instead of one band sliding past two circles.
            // abs(fract - 0.5) folds each segment around its own centre, which
            // is what keeps a mark a MARK -- a bare fract() ramp feathers one
            // edge and guillotines the other, and six comets is not the read.
            float rf = abs(fract((ang + t * 0.27) * 0.9549) - 0.5);
            float rune = smoothstep(0.155, 0.105, rf);
            a += rune * smoothstep(0.045, 0.0, abs(r - 0.845)) * 0.5;
            // Soft spokes: high exponent makes narrow bright rays; the radial
            // masks stop them from filling the center or leaking past the ring.
            float spoke = pow(abs(cos((ang + t * 0.6) * 3.0)), 24.0);
            a += spoke * smoothstep(0.93, 0.30, r) * step(0.34, r) * 0.4;
            // Faint center fill so the sigil reads as one object, not just
            // disconnected lines.
            a += (1.0 - smoothstep(0.0, 0.55, r)) * 0.10;
            // Light swells with the size, so the breath reads as a pulse of
            // brightness and not as a rubber band.
            a *= u_koto_alpha * (1.0 + 0.18 * swell);
            gl_FragColor = vec4(u_koto_col * a, a);
        """)

        # koto.veil: the stage's living backdrop -- six soft rays sweeping
        # around Kotonoha's anchor point plus ripple rings breathing outward,
        # tinted to the current card colour. All math, one quad per frame,
        # and VERY low alpha: it must never fight the danmaku for attention,
        # only stop the arena reading as a static picture.
        renpy.register_shader("koto.veil", variables="""
            uniform vec3 u_koto_col;
            uniform float u_koto_alpha;
            uniform float u_time;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 d = v_tex_coord - vec2(0.5, 0.30);
            d.x *= 0.91;
            float r = length(d) * 2.0;
            float ang = atan(d.y, d.x);
            // Six soft rays turning slowly. Integer harmonic keeps the atan
            // seam invisible; the radial mask keeps her anchor point clear.
            float ray = pow(abs(sin(ang * 3.0 + u_time * 0.21)), 6.0);
            ray *= smoothstep(0.10, 0.55, r);
            // Ripples drifting outward from the same centre.
            float rip = smoothstep(0.35, 1.0, sin(r * 9.0 - u_time * 0.9) * 0.5 + 0.5);
            float a = (ray * 0.6 + rip * 0.4) * smoothstep(1.30, 0.35, r) * u_koto_alpha;
            gl_FragColor = vec4(u_koto_col * a, a);
        """)

        # koto.cutin: the interior of the spell-card declaration band -- dark
        # glass for the type to sit on, a fan of speed lines rushing out of
        # Kotonoha, and one diagonal sheen crossing the whole ribbon. Drawn
        # into a CLIPPED sub-render whose height is what opens and shuts, so
        # this quad's own pixel size never changes and nothing here has to be
        # rebuilt while the band flies apart (same rule as koto.circle's
        # u_koto_scale: animate a uniform, never a cached quad's dimensions).
        #
        # u_koto_focus is in THIS quad's normalized space, and the quad is a
        # wide ribbon, so u_koto_aspect puts x back into square units before
        # the polar math -- without it the "rays" are ellipse segments that
        # visibly pinch at the top and bottom rails.
        renpy.register_shader("koto.cutin", variables="""
            uniform vec3 u_koto_col;
            uniform float u_koto_alpha;
            uniform vec2 u_koto_focus;
            uniform float u_koto_aspect;
            uniform float u_koto_rush;
            uniform float u_koto_rushamp;
            uniform float u_koto_sheen;
            uniform float u_time;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            // -1..1 across the ribbon, so every vertical falloff below reads
            // the same no matter what the band's pixel height happens to be.
            float by = (uv.y - 0.5) * 2.0;
            float aby = abs(by);
            // Glass: a dark pane that thins toward the rails. The type needs a
            // ground to sit on, but a flat rectangle of grey is exactly the
            // "just a bar" this replaces -- so it falls off quadratically and
            // never actually reaches the edge.
            float band = 1.0 - smoothstep(0.82, 1.0, aby);
            float glass = band * (0.74 - 0.30 * aby * aby);
            // Speed lines out of her anchor. jag varies each ray's WIDTH as
            // well as its phase; a fan of identical rays reads as a clock
            // face, and the whole point is that this looks thrown.
            vec2 d = uv - u_koto_focus;
            d.x *= u_koto_aspect;
            float rr = length(d);
            float ang = atan(d.y, d.x);
            float jag = fract(sin(floor(ang * 7.6394) * 97.31) * 43758.5453);
            float ray = pow(abs(sin(ang * 22.0 + jag * 2.4 + u_time * 0.09)),
                            9.0 + 7.0 * jag);
            // travel is the leading edge sweeping outward: everything inside
            // u_koto_rush is lit, everything past it has not arrived yet. The
            // inner smoothstep keeps the fan off her own anchor point.
            float travel = smoothstep(u_koto_rush + 0.10, u_koto_rush - 0.60, rr)
                         * smoothstep(0.05, 0.34, rr);
            float rush = ray * travel * band * u_koto_rushamp;
            // One diagonal sheen crossing the ribbon. The shear ties x to y so
            // it lands as a slash of light and not a vertical shutter.
            float sheen = smoothstep(0.22, 0.0, abs(uv.x + by * 0.09 - u_koto_sheen))
                        * band;
            float ag = glass * u_koto_alpha;
            // The fan is a BED, not the subject. At 0.70 it out-read the card
            // name it exists to introduce -- the type sat in a searchlight and
            // the whole beat became rays.
            float ac = clamp(rush * 0.44 + sheen * 0.55, 0.0, 1.0) * u_koto_alpha;
            float a = clamp(ag + ac, 0.0, 1.0);
            // Premultiplied, and the coloured term is deliberately allowed to
            // outrun the alpha: that is what makes the rush lines read as
            // light thrown ONTO the glass rather than paint mixed into it.
            gl_FragColor = vec4(vec3(0.012, 0.018, 0.042) * ag + u_koto_col * ac, a);
        """)

        # koto.lifering: the boss's life gauge as a RING around her (the modern
        # Touhou layout; the flat bar across the top of the stage is the old
        # one). Angle is measured clockwise from twelve o'clock, 0..1, and the
        # lit arc runs from the top to u_koto_fill, so damage eats it back
        # anticlockwise toward the top. u_koto_ghost is the chip ghost (a pale
        # arc lagging behind the fill so a burst reads as a bite); u_koto_split
        # is the nonspell/spell threshold, drawn as a white notch and as the
        # boundary between the brighter nonspell arc and the card-colour spell
        # arc (negative = no split, i.e. the spell is already running). The
        # ring is drawn in r units (r = 1 at the quad's edge) so the quad's
        # pixel size is the only scale, and it never changes.
        renpy.register_shader("koto.lifering", variables="""
            uniform vec3 u_koto_col;
            uniform float u_koto_fill;
            uniform float u_koto_ghost;
            uniform float u_koto_split;
            uniform float u_koto_alpha;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 d = v_tex_coord - vec2(0.5);
            float r = length(d) * 2.0;
            float u = fract(atan(d.x, -d.y) / 6.2831853 + 1.0);
            float R = 0.84;
            float w = 0.030;
            float aa = 0.020;
            float rr = abs(r - R);
            float band = 1.0 - smoothstep(w, w + aa, rr);
            float core = 1.0 - smoothstep(w * 0.30, w * 0.30 + aa, rr);
            float glow = exp(-pow(rr / (w * 3.6), 2.0));
            float lit = step(u, u_koto_fill);
            float gh = step(u, u_koto_ghost) * (1.0 - lit);
            float has_split = step(0.0, u_koto_split);
            // The nonspell arc (past the split) burns a step brighter, so the
            // half that is about to become a spell card is visibly different.
            vec3 fc = mix(u_koto_col, vec3(1.0), step(u_koto_split, u) * has_split * 0.38);
            // Dark track, then the ghost, then the lit arc and its hot core.
            vec4 o = vec4(vec3(0.02, 0.03, 0.07) * 0.62, 0.62) * band;
            o = mix(o, vec4(vec3(0.85), 0.85), band * gh * 0.55);
            o = mix(o, vec4(fc, 1.0), band * lit);
            o.rgb += vec3(1.0) * core * lit * 0.55;
            o += vec4(fc * glow * lit * 0.34, glow * lit * 0.22);
            // The split notch: a white tick straddling the ring.
            float dn = abs(fract(u - u_koto_split + 0.5) - 0.5) * 6.2831853 * r;
            float notch = (1.0 - smoothstep(0.010, 0.022, dn))
                        * (1.0 - smoothstep(w * 2.4, w * 2.4 + aa, rr)) * has_split;
            o = mix(o, vec4(1.0), notch);
            // The leading edge of the fill, a bead of light.
            float dl = abs(fract(u - u_koto_fill + 0.5) - 0.5) * 6.2831853 * r;
            float tip = (1.0 - smoothstep(0.0, 0.05, dl)) * band * step(0.001, u_koto_fill);
            o.rgb += vec3(1.0) * tip * 0.8;
            o.a = max(o.a, tip * 0.8);
            gl_FragColor = o * u_koto_alpha;
        """)

        # koto.spellbg: the SPELL CARD BACKGROUND (modern Touhou replaces the
        # stage behind a spell with the card's own moving backdrop). One quad
        # over the whole stage, one of nine procedural styles picked by
        # u_koto_style (KT_SPELL_BG maps each card to one), painted in the
        # card colour as dim LIGHT over the already-dimmed shrine -- it has to
        # change the room without ever competing with a bullet, so every style
        # tops out well under the bullets' brightness and is mostly dark.
        # p is aspect-correct, centred just above her float anchor.
        renpy.register_shader("koto.spellbg", variables="""
            uniform vec3 u_koto_col;
            uniform float u_koto_alpha;
            uniform float u_koto_style;
            uniform vec2 u_koto_res;
            uniform float u_time;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float kt_h1(float n) { return fract(sin(n * 127.1) * 43758.5453); }
            float kt_h2(vec2 q) { return fract(sin(dot(q, vec2(127.1, 311.7))) * 43758.5453); }
            float kt_noise(vec2 q) {
                vec2 i = floor(q);
                vec2 f = fract(q);
                f = f * f * (3.0 - 2.0 * f);
                return mix(mix(kt_h2(i), kt_h2(i + vec2(1.0, 0.0)), f.x),
                           mix(kt_h2(i + vec2(0.0, 1.0)), kt_h2(i + vec2(1.0, 1.0)), f.x), f.y);
            }
            float kt_fbm(vec2 q) {
                float v = 0.0;
                float a = 0.5;
                for (int k = 0; k < 4; k++) {
                    v += a * kt_noise(q);
                    q = q * 2.03 + vec2(1.7, 9.2);
                    a *= 0.5;
                }
                return v;
            }
            float kt_line(float d, float w) { return 1.0 - smoothstep(0.0, w, abs(d)); }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            vec2 p = (uv - vec2(0.5, 0.26)) * u_koto_res / u_koto_res.y;
            float t = u_time;
            float r = length(p);
            float ang = atan(p.y, p.x);
            float I = 0.0;
            float s = u_koto_style;
            if (s < 0.5) {
                // 0 FACETS: a kaleidoscope folded into six wedges, turning,
                // over a triangular lattice that drifts outward.
                float a = abs(mod(ang + t * 0.06, 1.0472) - 0.5236);
                vec2 q = vec2(cos(a), sin(a)) * r * 7.0;
                float g1 = kt_line(fract(q.x - t * 0.15) - 0.5, 0.05);
                float g2 = kt_line(fract(q.x * 0.5 + q.y * 0.866) - 0.5, 0.05);
                float g3 = kt_line(fract(q.x * 0.5 - q.y * 0.866) - 0.5, 0.05);
                I = max(g1, max(g2, g3)) * 0.55 + kt_line(fract(r * 3.0 - t * 0.12) - 0.5, 0.03) * 0.35;
                I *= smoothstep(1.4, 0.2, r);
            } else if (s < 1.5) {
                // 1 INBOX: rows of unread lines scrolling down, each row a
                // run of message bars of its own length, a bright badge now
                // and then.
                vec2 g = vec2(uv.x * 7.0, uv.y * 26.0 - t * 0.9);
                float row = floor(g.y);
                float cell = floor(g.x);
                float fy = fract(g.y);
                float fx = fract(g.x);
                float len = 0.25 + 0.7 * kt_h2(vec2(row, cell));
                float bar = step(fx, len) * (1.0 - smoothstep(0.14, 0.24, abs(fy - 0.5)));
                float badge = step(0.93, kt_h2(vec2(row * 3.1, cell))) *
                              (1.0 - smoothstep(0.05, 0.12, length(vec2(fx - len - 0.06, fy - 0.5) * vec2(1.0, 0.5))));
                I = bar * (0.12 + 0.18 * kt_h2(vec2(cell, row + 7.0))) + badge * 0.8;
            } else if (s < 2.5) {
                // 2 WATER: dark water, slow bands of swell and a glint line.
                float y = p.y * 10.0 + sin(p.x * 4.0 + t * 0.7) * 0.6 + sin(p.x * 9.0 - t * 1.1) * 0.25;
                I = kt_line(fract(y - t * 0.25) - 0.5, 0.10) * (0.35 + 0.35 * kt_noise(vec2(p.x * 3.0, y * 0.5 + t * 0.2)));
                I += pow(kt_noise(vec2(p.x * 14.0 + t * 0.4, y * 1.5)), 6.0) * 1.2;
                I *= smoothstep(-0.3, 0.6, p.y + 0.2);
            } else if (s < 3.5) {
                // 3 RAIN: slanted streaks falling fast, three depths.
                for (int k = 0; k < 3; k++) {
                    float fk = float(k);
                    vec2 q = uv * vec2(28.0 + fk * 14.0, 3.0 + fk);
                    q.x += q.y * 0.35;
                    q.y += t * (1.6 + fk * 0.9) + kt_h1(floor(q.x) + fk * 13.0) * 7.0;
                    float col = floor(q.x);
                    float drop = step(0.72, kt_h1(col * 1.7 + fk)) * smoothstep(0.0, 0.8, fract(q.y)) *
                                 (1.0 - smoothstep(0.08, 0.16, abs(fract(q.x) - 0.5)));
                    I += drop * (0.45 - fk * 0.1);
                }
            } else if (s < 4.5) {
                // 4 FOG: drifting mist, and the odd pale shape in it.
                vec2 q = p * 2.6 + vec2(t * 0.05, -t * 0.03);
                float f = kt_fbm(q + kt_fbm(q + t * 0.04));
                I = smoothstep(0.35, 0.95, f) * 0.55;
            } else if (s < 5.5) {
                // 5 MOSAIC: tesserae, mirrored down the middle of the stage --
                // both halves of one picture. Cell edges glow; cells breathe.
                vec2 q = vec2(abs(uv.x - 0.5), uv.y) * vec2(9.0, 10.0);
                vec2 i = floor(q);
                vec2 f = fract(q);
                float d1 = 8.0;
                float d2 = 8.0;
                float id = 0.0;
                for (int yy = -1; yy <= 1; yy++) {
                    for (int xx = -1; xx <= 1; xx++) {
                        vec2 o = vec2(float(xx), float(yy));
                        vec2 c = o + 0.5 + 0.38 * sin(t * 0.3 + 6.2831 * vec2(kt_h2(i + o), kt_h2(i + o + 3.3)));
                        float d = length(f - c);
                        if (d < d1) { d2 = d1; d1 = d; id = kt_h2(i + o + 9.1); }
                        else if (d < d2) { d2 = d; }
                    }
                }
                I = kt_line(d2 - d1, 0.07) * 0.6 + (0.12 + 0.18 * sin(t * 0.8 + id * 6.2831)) * 0.5;
            } else if (s < 6.5) {
                // 6 SAW: teeth spinning around her, a sawblade the size of the
                // room, over slow red scratches.
                float a = ang + t * 0.55;
                float saw = fract(a * 12.0 / 6.2831);
                I = kt_line(r * 5.0 - (1.0 + saw * 0.35) - floor(r * 5.0 - saw * 0.35), 0.06) * 0.25;
                I += pow(abs(sin(a * 12.0)), 30.0) * smoothstep(1.6, 0.2, r) * 0.45;
                I += kt_line(fract(p.x * 3.0 + p.y * 7.0 + kt_noise(p * 5.0) * 0.4) - 0.5, 0.02) * 0.15;
            } else if (s < 7.5) {
                // 7 SIGILS: every self -- rings of runes counter-turning at
                // three depths around her, under a slow hexagram.
                for (int k = 0; k < 3; k++) {
                    float fk = float(k);
                    float rr = 0.35 + fk * 0.38;
                    float a = ang * (1.0 - 2.0 * mod(fk, 2.0)) + t * (0.12 + fk * 0.05);
                    float ticks = step(0.55, fract(a * (18.0 + fk * 10.0) / 6.2831));
                    I += kt_line(r - rr, 0.012) * 0.5 + kt_line(r - rr - 0.04, 0.02) * ticks * 0.4;
                }
                float hx = 0.0;
                for (int k = 0; k < 3; k++) {
                    float a = float(k) * 1.0472 + t * 0.03;
                    hx = max(hx, kt_line(dot(p, vec2(cos(a), sin(a))) - 0.6, 0.01));
                    hx = max(hx, kt_line(dot(p, vec2(cos(a), sin(a))) + 0.6, 0.01));
                }
                I += hx * 0.5 * smoothstep(1.3, 0.3, r);
            } else {
                // 8 PETALS: rose-curve rings blooming outward from her.
                float k5 = abs(cos(2.5 * (ang + t * 0.05)));
                float rr = r / (0.55 + 0.45 * k5);
                I = kt_line(fract(rr * 3.0 - t * 0.2) - 0.5, 0.06) * 0.5 * smoothstep(1.5, 0.1, r);
                I += pow(kt_noise(p * 6.0 + t * 0.1), 4.0) * 0.4;
            }
            I = clamp(I, 0.0, 1.0);
            // Vignette: the frame's edges stay darker than her side of it.
            float vig = 1.0 - 0.45 * smoothstep(0.35, 0.95, length((uv - vec2(0.5, 0.4)) * vec2(1.1, 0.9)));
            // Quiet on purpose: the pattern is a room, not a hazard. Lines top
            // out around 40% of the card colour and the dark ground only
            // half-covers the shrine behind it.
            float a = u_koto_alpha * (0.22 + 0.26 * I) * vig;
            vec3 c = mix(u_koto_col, vec3(1.0), 0.12 * I) * I * 0.62 * u_koto_alpha * vig;
            gl_FragColor = vec4(c + vec3(0.004, 0.006, 0.02) * a, a);
        """)

    try:
        _kt_register_shaders()
        KT_SHADER_OK = True
    except Exception as _kt_sh_e:
        KT_SHADER_OK = False
        if config.developer:
            renpy.log("KOTO FX: shader registration failed: %r" % _kt_sh_e)

# --- CONSTANTS / TUNING ------------------------------------------------------
init python:
    import math
    import random as kt_random   # Endless-mode pattern/card rolls + ambient motes.

    # KT_DIR holds the art that belongs to the mode's STAGE: the boss sheet
    # and the two backdrops. Every sprite drawn ON the stage -- bullets,
    # lasers, FX, the soul, HUD icons, seals, the frame -- lives in
    # assets/bullets/kotonoha/ (KT_ART_DIR, below) with the project's other
    # bullet art.
    KT_DIR = "addons/Matsuda's Sick Boss Fight/kotonohamode/"
    KT_SE_DIR = "assets/audio/sfx/touhou/"

    # Kotonoha's boss sheet was rendered from
    # ONE procedural pixel-art rig (her stage costume: white bell sleeves, a
    # slate pinafore dipped in violet ink, the name-plate brooch, the brush
    # kanzashi, the book she reads from). The 2026-09-20 image-generator sheet
    # it replaced is kept at archive/kotoboss_sheet_2026-09-20_casual.png.
    #
    # LAYOUT: KT_BOSS_NROWS rows of KT_BOSS_PHASES columns, KT_BOSS_CELL px.
    #   ROWS are POSES: idle; the lean left and right at three depths; the
    #   cast at three arm spreads; the declaration at three stages of lifting
    #   the card; the recoil. The in-between depths ARE the transitions.
    #   COLUMNS are one shared secondary-motion loop (hair, sleeves, sash
    #   tails, skirt hem, the book) -- every row at column N has its cloth at
    #   the same point of the loop, so changing pose never pops the hair.
    # The rig script reads the three layout numbers below and refuses to
    # write a sheet that disagrees with them.
    #
    # HOW IT PLAYS. The column is the clock: (tick // KT_BOSS_PHASE_TICKS) % 8,
    # always, in every pose -- nothing she holds is ever a statue. The row is
    # a POSE LEVEL per action (lean / cast / declare, 0..3) that steps ONE
    # depth at a time at most every few ticks, so every change of pose plays
    # its in-betweens on the way instead of snapping to the extreme. That is
    # the Touhou read; the old sheet had four cells per action and could only
    # hold one or flap between two.
    KT_BOSS_SHEET = KT_DIR + "kotoboss_sheet.png"
    KT_BOSS_CELL = 96
    KT_BOSS_PHASES = 8
    KT_BOSS_NROWS = 14
    # Integer zoom, and it matters: at 1.35 the old art drew its pixels one
    # and two screen pixels wide in alternation, so every drift of her position
    # shimmered the whole sprite. At 2.0 every art pixel is a 2x2 block.
    KT_BOSS_ZOOM = 2.0
    KT_BOSS_IDLE = 0
    KT_BOSS_LEFT = (1, 2, 3)        # lean depth 1..3, travelling left
    KT_BOSS_RIGHT = (4, 5, 6)       # ...travelling right
    KT_BOSS_CAST = (7, 8, 9)        # arms spreading 1..3
    KT_BOSS_DECLARE = (10, 11, 12)  # the card lifting 1..3 (card shows from 2)
    KT_BOSS_HURT = 13
    # One loop frame per this many ticks: 8 x 7 = a 56-tick (~0.93s) cycle.
    KT_BOSS_PHASE_TICKS = 7

    # Lean. KTStage keeps an eased, SIGNED travel speed; its magnitude asks
    # for a depth through a rise/fall hysteresis band (so a boss cruising near
    # a threshold cannot chatter) and its sign latches the facing. The facing
    # latch sits BELOW the first rise, and the first fall below the latch, so
    # a visible lean can never show the wrong direction: to reverse, the ease
    # has to pass through depth 0 first.
    KT_BOSS_LEAN_FULL = 1.35    # px/tick of travel that reads as a full lean
    KT_BOSS_LEAN_EASE = 0.12    # per-tick ease toward current travel speed
    KT_BOSS_LEAN_RISE = (0.26, 0.48, 0.70)  # depth 0->1, 1->2, 2->3
    KT_BOSS_LEAN_FALL = (0.16, 0.38, 0.60)  # ...and back down again
    KT_BOSS_FACE_LATCH = 0.22   # signed lean that commits a left/right facing
    KT_BOSS_LEAN_STEP = 4       # min ticks between two lean depth steps

    # Cast: a PULSE. A fire cue raises the arms (one depth every
    # KT_BOSS_CAST_UP ticks), later cues keep them out for KT_BOSS_CAST_HOLD
    # ticks past the last one, and a pulse never runs past
    # KT_BOSS_CAST_SPREAD_MAX: cards that fire every 6 ticks would otherwise
    # freeze her arms out for the whole pattern. Then the arms lower (one depth
    # every KT_BOSS_CAST_DOWN) and the next cue winds up again, so sustained
    # fire reads as her conducting it rather than as a statue.
    KT_BOSS_CAST_UP = 3
    KT_BOSS_CAST_DOWN = 4
    KT_BOSS_CAST_HOLD = 16
    KT_BOSS_CAST_SPREAD_MAX = 52
    # ...and after a pulse the arms stay down at least this long, so a card
    # that never stops firing still leaves her time to hover and to lean.
    # Measured on a 6-10 tick fire cadence: arms out ~55% of the time when
    # she is stationary, far less on the travelling moves.
    KT_BOSS_CAST_REST = 40
    # A pulse only starts from a body travelling at this lean depth or less;
    # at a deeper lean the tilt IS the read, and the muzzle flare still sells
    # the volley. Tearing her out of a full lean for half a second is the
    # flicker the old sheet had every time a pattern fired mid-sweep. (A hard
    # lean that starts DURING a pulse ends it early -- travel wins.)
    KT_BOSS_CAST_MAX_LEAN = 1
    # Declaration: she draws the card from her book and lifts it, one depth
    # every KT_BOSS_DECL_UP ticks, and holds it up for the banner. On the far
    # side of the phase flip it lowers again at KT_BOSS_DECL_DOWN.
    KT_BOSS_DECL_UP = 6
    KT_BOSS_DECL_DOWN = 5
    # Recoil: the first ticks of a break, and the whole victory cinematic.
    KT_BOSS_HURT_TICKS = 40
    # No shown row changes faster than this (the declaration's first step is
    # exempt -- it lands on its beat).
    KT_BOSS_ROW_MIN = 4

    def kt_boss_cell(row, col):
        return Crop((col * KT_BOSS_CELL, row * KT_BOSS_CELL,
                     KT_BOSS_CELL, KT_BOSS_CELL), KT_BOSS_SHEET)

    KT_BOSS_FRAMES = tuple(
        tuple(kt_boss_cell(row, col) for col in range(KT_BOSS_PHASES))
        for row in range(KT_BOSS_NROWS)
    )

    # Stage rect (in screen space) and simulation timing. The playfield sits
    # left-of-centre with the score panel to its right, Touhou layout.
    KT_SX = 48
    KT_SY = 20
    KT_W = 620
    KT_H = 680
    KT_TICK = 1.0 / 60.0
    KT_MAX_CATCHUP = 4          # max sim ticks per frame (menu / hitch recovery)

    # Player.
    KT_PLAYER_R = 3.5           # true hitbox radius (shown while focused)
    KT_GRAZE_PAD = 15.0         # extra radius that counts as a graze
    KT_MOVE = 4.4               # px/tick unfocused (~264 px/s)
    KT_FOCUS = 2.0              # px/tick focused
    KT_SHOT_EVERY = 5           # ticks between volleys while Z is held
    KT_SHOT_SPEED = 16.0
    KT_SHOT_DMG = 1.0
    KT_START_LIVES = 5
    KT_START_BOMBS = 3
    KT_MAX_LIVES = 8
    KT_MAX_BOMBS = 8
    KT_DEATHBOMB_TICKS = 9      # grace window to X out of a hit
    KT_RESPAWN_INVULN = 180
    KT_BOMB_INVULN = 150
    KT_BOMB_WAVE_TICKS = 60     # wave reaches full radius here
    KT_BOMB_DAMAGE = 110.0      # total chip a bomb deals to the active bar

    # The soul's drawn zoom (its art is 48px with a ~29px heart in it, so this
    # lands it near the old pixel heart's 36px without covering the hitbox).
    KT_SOUL_ZOOM = 1.1

    # Bullets.
    KT_MAX_BULLETS = 480
    KT_MAX_SHOTS = 64
    KT_MAX_SPARKS = 170
    # Bullet cancels: the cosmetic stars a cleared bullet leaves behind (see
    # KTGame._update_cancels). They hang for KT_CANCEL_HANG ticks, then home
    # into the soul; anything still flying at KT_CANCEL_TTL simply goes out.
    KT_MAX_CANCELS = 260
    KT_CANCEL_HANG = 18
    KT_CANCEL_TTL = 110
    KT_ROT_BUCKETS = 60
    KT_ROT_DEG = 360.0 / KT_ROT_BUCKETS
    # Radians straight to a bucket index, so a pointed bullet never converts to
    # degrees at all: bucket = round(atan2(vy, vx) * KT_ROT_K + KT_ROT_Q). The
    # quarter-turn offset is the sprites' "points up at 0" convention, which used
    # to be written as a literal "+ 90.0" degrees.
    KT_ROT_K = KT_ROT_BUCKETS / (2.0 * math.pi)
    KT_ROT_Q = KT_ROT_BUCKETS // 4

    # Scoring. Extends are score thresholds; a bomb is stocked per bar break.
    KT_EXTEND_SCORES = [2000000, 5000000, 9000000, 14000000, 20000000]
    KT_SCORE_HIT = 10
    KT_SCORE_GRAZE = 500
    KT_SCORE_CLEAR = 100        # per bullet wiped by a bomb / bar break
    KT_SCORE_NONSPELL = 60000   # + 2000 per second left on the clock

    # Palette. Bullets carry an INDEX into this (never a hex string) so the
    # renderer can key its texture cache on a small int.
    KT_PAL = [
        "#ff4a5c",  # 0 red
        "#ff8fc8",  # 1 pink
        "#ff5cff",  # 2 magenta
        "#b06cff",  # 3 purple
        "#7d5cff",  # 4 violet
        "#5c7dff",  # 5 blue
        "#5cd7ff",  # 6 cyan
        "#5cffd7",  # 7 teal
        "#6cff7d",  # 8 green
        "#c8ff5c",  # 9 lime
        "#ffe65c",  # 10 yellow
        "#ffb84a",  # 11 amber
        "#ff7d3d",  # 12 orange
        "#f5faff",  # 13 white
        "#9aa8bd",  # 14 grey
    ]

    # --- THE ART -----------------------------------------------------------
    # Every sprite on this stage is this mode's own, drawn procedurally into
    # the atlases in assets/bullets/kotonoha/ -- bullets, lasers, sparks and
    # glows, the soul
    # and its shots, the HUD icons, and one summoning seal per spell card.
    # Nothing here comes from a Touhou sheet any more.
    #
    # COLOUR IS BAKED. Each colourable sprite exists once per KT_PAL entry, so
    # a bullet's palette index picks its CELL rather than tinting a white one.
    # Tinting flattened the white-hot core every bullet is drawn around into
    # the tint colour, and every new TintMatrix compiled a GL program on the
    # frame it first appeared. The generator checks its palette against
    # KT_PAL, so the column order can be trusted.
    #
    # kt_atlas.json is the only map from a name to a rect. Rebuild the art
    # and this picks the new layout up with no code change.
    KT_ART_DIR = EMB_DIR + "kotonoha/"

    def _kt_load_atlas():
        import json as _kt_json
        with renpy.open_file(KT_ART_DIR + "kt_atlas.json", encoding="utf-8") as fh:
            return _kt_json.load(fh)

    KT_ATLAS = _kt_load_atlas()
    _kt_art_cells = {}

    def kt_art(sheet, key):
        """One cell of one of this mode's atlases, as a shared Crop.

        A live Crop, not a copy: each atlas is one texture and every cell is a
        subsurface of it, so a hundred bullets of one kind are one upload.
        """
        d = _kt_art_cells.get((sheet, key))
        if d is None:
            info = KT_ATLAS[sheet]
            d = Crop(tuple(info["cells"][key]), KT_ART_DIR + info["file"])
            _kt_art_cells[(sheet, key)] = d
        return d

    # Which koto.spellbg style each spell card's background wears, by SPELL
    # PATTERN (the same index as the seals). 0 facets, 1 inbox, 2 water,
    # 3 rain, 4 fog, 5 mosaic, 6 saw, 7 sigils, 8 petals.
    KT_SPELL_BG = [
        0,  # Facet "First Impressions"      -- a turning kaleidoscope
        1,  # Overtime "999+ Unread"         -- rows of mail scrolling in
        2,  # Blade "Nice Boat, Cruel Wake"  -- dark water
        3,  # Diligence "Rain or Shine"      -- rain
        4,  # Ghost "Nobody's Looking"       -- fog (under the spotlight)
        5,  # Mosaic "Both of Me Are Real"   -- a mirrored mosaic
        6,  # Severance "The Scene..."       -- a sawblade the size of the room
        7,  # Chameleon "Every Self..."      -- every sigil at once
        8,  # Mask of the Bloom              -- petals
        7,  # Mask of the Hunter             -- sigils (the reticle's rings)
        4,  # Mask of the Keeper             -- steam
        1,  # Mask of the Prodigy            -- a feed of windows
        3,  # Mask of the Abandoner          -- a storm she ran out into
        1,  # Mask of the Interloper         -- lines, struck through
        5,  # Mask of You                    -- mirrored
        7,  # Mask of the Seer               -- borders and rings
        2,  # Patience "Faded Ribbon"        -- still water
        6,  # Bravery "Tough Glove"          -- impacts
        8,  # Integrity "Ballet Shoes"       -- arcs
        1,  # Perseverance "Torn Notebook"   -- ruled lines
        4,  # Kindness "Burnt Pan"           -- steam
        6,  # Justice "Empty Gun"            -- the cylinder turning
    ]

    # The summoning seal is picked by SPELL PATTERN, not by colour: every card
    # has its own drawn in its own colour (the knives of "Nice Boat", the clock
    # of unread mail, the Seer's nested borders, Justice's six chambers). The
    # table in the generator is indexed the same way and checked against the
    # card colours below.
    KT_SEAL_PX = 256.0

    # How fast the summoning seal turns, in degrees per SIM TICK (60/sec), so
    # it stops and starts with the sim rather than with wall time. Slow on
    # purpose: it is the heavy stone ring under the shader circle's fast light
    # ring, and it turns the other way. Anything past ~20 deg/sec here starts
    # reading as a spinner instead of a sigil.
    KT_SEAL_SPIN = 11.0 / 60.0

    # --- cosmetic FX envelope ------------------------------------------------
    # Phases flip on a single tick, so any level read straight off g.phase is a
    # HARD CUT: the seal used to drop 0.85 -> 0.34 in one frame at declare ->
    # spell and then vanish outright when the card ended, and the stage dim
    # snapped between two constants. Every such level is now eased toward its
    # phase target once per SIM TICK in KTStage._advance_fx_env.
    #
    # Attack is fast and release is slow on purpose. A declaration still has to
    # SLAM -- softening the attack is what would make this feel mushy -- but
    # nothing should ever pop out of existence.
    KT_FX_ATTACK = 0.20         # per tick, level rising
    KT_FX_RELEASE = 0.055       # per tick, level falling (~50 ticks to fade)
    KT_FX_SEAL_ATTACK = 0.35    # the slam keeps its punch
    KT_FX_SEAL_RELEASE = 0.05
    KT_FX_SIZE_EASE = 0.30      # sizes, both directions
    KT_FX_DIM_EASE = 0.10       # stage dim, slow enough to read as the lights
    KT_FX_COL_EASE = 0.05       # card-colour crossfade across the whole stage
    KT_FX_FOCUS_ATTACK = 0.34   # the hitbox sigil has to feel instant
    KT_FX_FOCUS_RELEASE = 0.20

    # The spell circle's quad is FIXED and its size is a shader uniform, so the
    # size can move continuously without ever re-keying a cached quad. Sized for
    # the declare peak (330px) plus the breath and the ring's own band.
    KT_FX_CIRCLE_QUAD = 344

    # --- SPELL-CARD DECLARATION (the cut-in) ---------------------------------
    # The declaration used to be one flat sprite panning right-to-left at a
    # constant 10.5 px/tick between two hairlines, for its whole 85 ticks. It
    # is a staged cut-in now: a ribbon that flies open, a portrait that arrives
    # and settles, type that cascades in, and -- the part that makes the
    # handover seamless -- a card name that FLIES into its HUD slot across the
    # declare/spell boundary instead of vanishing from the middle of the stage
    # and reappearing in the corner one frame later.
    #
    # Every beat below is a tick mark inside the declare phase:
    #
    #   0            slam: white kick, the seam splits, the ribbon starts open
    #   0  -> 18     ribbon flies apart (ease-out); rails ride its edges
    #   0  -> 26     portrait arrives from the right and decelerates hard
    #   6  -> 40     speed lines sweep out of her; one sheen crosses the ribbon
    #   6 / 12 / 18  kick label, then card name line 0, then line 1, cascade in
    #   26 -> 44     the rule draws out from under the name
    #   78 -> 104    ribbon shuts (ease-in) and the name leaves for the HUD
    #
    # ...and then KT_CARD_FLIGHT more ticks on the far side of the phase flip,
    # where the small HUD name finishes the same journey. See _card_flight.
    KT_DECLARE_TICKS = 104      # total length of the declare phase
    KT_DECL_OPEN = 18           # ticks the ribbon takes to fly apart
    KT_DECL_CLOSE = 78          # tick the ribbon starts shutting
    KT_DECL_PORT_IN = 26        # ticks the portrait takes to arrive
    KT_DECL_RULE_AT = 26        # tick the rule under the name starts drawing
    KT_DECL_RULE_LEN = 18       # ...and how long it takes to reach full width
    KT_CARD_FLIGHT = 18         # spell ticks the HUD name takes to land

    # Ribbon geometry, stage-local. HALF is what animates; the shader quad
    # underneath is always the full KT_DECL_BAND_H tall and gets clipped.
    KT_DECL_BAND_MID = 250.0
    KT_DECL_BAND_HALF = 104.0
    KT_DECL_BAND_H = int(KT_DECL_BAND_HALF * 2.0)

    # Type block, RIGHT-aligned inside the ribbon. The alignment is not a
    # style choice: the card's HUD slot is right-aligned in the top-right
    # corner (the modern Touhou layout), and matching alignments at both ends
    # are what let the flight between them be a plain lerp of the right edge
    # and still look concentric.
    KT_DECL_TEXT_R = 576.0
    KT_DECL_KICK_Y = 168.0
    KT_DECL_TEXT_Y = 196.0

    # The spell card's HUD slot: right edge and the top of its first line,
    # under the timer. The flight lands exactly here.
    KT_HUD_R = 608.0
    KT_HUD_NAME_Y = 34.0

    # The boss life ring's quad (fixed; see koto.lifering). Its ring sits at
    # 0.84 of the half-size, ~66px out from her centre.
    KT_LIFE_RING_QUAD = 158

    # Portrait: the card-raised cell (KT_BOSS_DECLARE[-1]) at an INTEGER zoom,
    # so its pixels stay square blocks. CY is the blit centre of the whole
    # cell; the rig puts her head ~22 native px above that centre, so this
    # lands her face in the upper half of the ribbon (y 146..354) with the
    # raised card inside the top rail and the band cutting her at the skirt.
    KT_DECL_PORT_ZOOM = 4.0
    KT_DECL_PORT_CY = 303.0
    # She arrives from the LEFT now, opposite the right-aligned type.
    KT_DECL_PORT_X0 = -300.0    # off the left lip, where she comes from
    KT_DECL_PORT_X1 = 118.0     # where she settles
    KT_DECL_PORT_X2 = 150.0     # ...and drifts to, slowly, over the hold

    # The eight health bars: hp is the FULL bar (nonspell burns the top half,
    # the spell card the bottom half), timers are in ticks, value is the spell
    # capture bonus, color indexes KT_PAL for the bar/aura accent.
    #
    # THEME: the eight cards are eight LIVES she's worn --
    # multifaceted living, perseverance as a blessing and a curse. Each card is
    # one of the masks from her character stories ("The Girl with Every Face" /
    # "The Void Hunter"): the diligent worker, the ghost nobody notices, the
    # mosaic of selves, the blade looking for a worthy ending. Bars 3 and 7
    # keep their names -- those two scenes ARE her story.
    # HP LADDER (2026-07 rebalance): every bar climbs one even +80 step so the
    # fight escalates wave over wave, then bar 8 SPIKES -- the last resort
    # barrage should feel like a last resort, not a short fuse. Every half-bar
    # stays burnable inside its clock at the ~15-20 dmg/sec a competent run
    # sustains (worst case: bar 8's nonspell half, 850 in 45s = 18.9/s, and
    # the finale spell is survival-captured on timeout anyway).
    KT_BARS = [
        dict(hp=700,  card='Facet Sign "First Impressions"',             color=1,  ns_time=40 * 60, sp_time=50 * 60, value=200000),
        dict(hp=780,  card='Overtime Sign "999+ Unread"',                color=11, ns_time=40 * 60, sp_time=50 * 60, value=350000),
        dict(hp=860,  card='Blade Sign "Nice Boat, Cruel Wake"',         color=0,  ns_time=40 * 60, sp_time=50 * 60, value=500000),
        dict(hp=940,  card='Diligence Sign "Rain or Shine"',             color=8,  ns_time=40 * 60, sp_time=52 * 60, value=650000),
        dict(hp=1020, card='Ghost Sign "Nobody\'s Looking"',             color=4,  ns_time=40 * 60, sp_time=52 * 60, value=800000),
        dict(hp=1100, card='Mosaic Sign "Both of Me Are Real"',          color=6,  ns_time=42 * 60, sp_time=55 * 60, value=950000),
        dict(hp=1180, card='Severance Sign "The Scene Everyone Remembers"', color=0, ns_time=42 * 60, sp_time=55 * 60, value=1100000),
        dict(hp=1700, card='Chameleon Sign "Every Self But Her Own"',      color=2,  ns_time=45 * 60, sp_time=75 * 60, value=2000000),
    ]

    # ---- ENDLESS-ONLY CONTENT TABLES ----------------------------------------
    # Endless Mode's extra hat entries. The pattern functions live with the
    # other patterns below (_ns9.._ns12 / _sp9.._sp16); indexes here continue
    # straight past KT_BARS, so nonspell index 8 is KT_ENDLESS_NS[0] and spell
    # index 8 is KT_ENDLESS_CARDS[0]. Every entry rolls with EQUAL probability
    # against the fixed-run patterns -- the only rule is no immediate repeats.

    # The four Endless-only nonspells (pattern + opening movement only; the
    # wave's identity always follows its spell card).
    KT_ENDLESS_NS = [
        dict(move="high",   ns_time=40 * 60),   # _ns9  twin lattice
        dict(move="sway",   ns_time=40 * 60),   # _ns10 meteor drift
        dict(move="center", ns_time=40 * 60),   # _ns11 pincer spirals
        dict(move="dart",   ns_time=40 * 60),   # _ns12 scatter snipe
    ]

    # ENDLESS HP LADDER: every endless bar is UNIFORM for its wave -- the
    # pattern you rolled is the difficulty, never an HP lottery -- and the
    # ladder climbs one step per wave, CAPPING at wave 8 (index 7). Cap math:
    # 1280 HP means the worst nonspell half is 640 in a 40s clock = 16 dmg/s,
    # firmly inside "doable without nerfing any move".
    KT_EHP_BASE = 860
    KT_EHP_STEP = 60
    KT_EHP_CAP_WAVE = 7

    # THE MASKS. The eight fixed cards are the lives KOTONOHA has worn; the
    # Endless-only cards are everyone else's -- each one a cast member's style
    # read back in bullets. (No hp field: endless HP comes from the uniform
    # ladder above.) `special` flags plumb card-specific mechanics:
    #   "seer" -- border gaps + the time stop (Yukari's pretty gaps crossed
    #            with Sakuya's stopped clock, per the design brief);
    #   "you"  -- the phantom mirrors the PLAYER through the stage centre.
    #
    # MASK ASSIGNMENTS (2026-07 rework): the Seer is MATSUDA's motif -- her
    # character story is literally "Ontological Seer" -- so "Every Border Is
    # a Door" is her mask now (the 4th-wall keeper, watching from the booth;
    # bright red + aqua, chimerical glints across the spectrum). Kotonoha,
    # undisguised, is the VOID HUNTER ("The Void Hunter", cs_kotonoha_02):
    # the old Ringmaster fireworks are repurposed as her hunting flares --
    # same move, same one-girl finale, violet through and through.
    #
    # COLOR MOTIFS (per the character bible):
    #   Matsuda   bright red + aqua/light blue, chimerical hints    (Seer)
    #   Sam       orange + blond yellow                             (Abandoner)
    #   Monika    emerald green, sly blue/violet/pink nods          (Interloper)
    #   MC        gray and white                                    (You)
    #   Asahina   "impossible colors": magenta + stygian blue       (Prodigy)
    #   Kotonoha  violet and other shades of purple                 (Hunter)
    #   Himeko    anything goes                                     (Keeper)
    KT_ENDLESS_CARDS = [
        # Tsubaki
        dict(card='Mask of the Bloom "Camellias Fall Whole"', color=0, sp_time=50 * 60, value=1200000, move="center", special=None),
        # Kotonoha, undisguised -- the Void Hunter
        dict(card='Mask of the Hunter "One-Girl Grand Finale"', color=3, sp_time=52 * 60, value=1300000, move="high", special=None),
        # Mom
        dict(card='Mask of the Keeper "Dinner Gets Cold"', color=10, sp_time=52 * 60, value=1400000, move="center", special=None),
        # Hina
        dict(card='Mask of the Prodigy "A Room of Closing Windows"', color=2, sp_time=55 * 60, value=1500000, move="sway", special=None),
        # Sam
        dict(card='Mask of the Abandoner "Reckless Abandon"', color=12, sp_time=55 * 60, value=1600000, move="wild", special=None),
        # her.
        dict(card='Mask of the Interloper "Delete As Appropriate"', color=8, sp_time=55 * 60, value=1750000, move="blink", special=None),
        # you
        dict(card='Mask of You "The Reader, Read Back"', color=14, sp_time=58 * 60, value=1900000, move="sweep", special="you"),
        # Matsuda -- the Ontological Seer, wearing her own motif openly
        dict(card='Mask of the Seer "Every Border Is a Door"', color=0, sp_time=62 * 60, value=2400000, move="center", special="seer"),

        # THE SOULS. Six more Endless-only cards, each a quiet callback to
        # the six fallen souls (this whole mode's diegesis owes Undertale /
        # Deltarune, and Endless is where the cut content lives). Titles are
        # the souls' items; `group="soul"` swaps the declare kick to SOUL
        # CARD and the wave splash to its own tell.
        # Aqua -- Patience
        dict(card='Patience Sign "Faded Ribbon"', color=6, sp_time=52 * 60, value=1350000, move="center", special=None, group="soul"),
        # Orange -- Bravery
        dict(card='Bravery Sign "Tough Glove"', color=12, sp_time=50 * 60, value=1400000, move="wild", special=None, group="soul"),
        # Blue -- Integrity
        dict(card='Integrity Sign "Ballet Shoes"', color=5, sp_time=52 * 60, value=1450000, move="sway", special=None, group="soul"),
        # Purple -- Perseverance
        dict(card='Perseverance Sign "Torn Notebook"', color=4, sp_time=52 * 60, value=1500000, move="high", special=None, group="soul"),
        # Green -- Kindness
        dict(card='Kindness Sign "Burnt Pan"', color=8, sp_time=52 * 60, value=1550000, move="center", special=None, group="soul"),
        # Yellow -- Justice
        dict(card='Justice Sign "Empty Gun"', color=10, sp_time=55 * 60, value=1650000, move="dart", special=None, group="soul"),
    ]

    # Short human labels for the nonspells (the DEV-ONLY debug wave viewer's
    # picker; spell cards list under their real names).
    KT_NS_LABELS = [
        "Bar 1 opener -- aimed fans, lazy rings",
        "Bar 2 opener -- crossing curtains",
        "Bar 3 opener -- double helix",
        "Bar 4 opener -- leaning rain",
        "Bar 5 opener -- layered flowers, first homing",
        "Bar 6 opener -- ricochet fans",
        "Bar 7 opener -- pressure fans and snipes",
        "Bar 8 opener -- the remix breather",
        "Endless -- twin lattice",
        "Endless -- meteor drift",
        "Endless -- pincer spirals",
        "Endless -- scatter snipe",
    ]

    def kt_wvp_title(card):
        # 'Facet Sign "First Impressions"' -> "First Impressions" (grid
        # buttons show the quoted title; the footer shows the full name).
        q = card.find('"')
        if q >= 0:
            return card[q:].strip().strip('"')
        return card

    def kt_wvp_ns_entries():
        # (index, tag, short label) rows for the picker's opener column.
        rows = []
        for i, lbl in enumerate(KT_NS_LABELS):
            part = lbl.split("--", 1)[1].strip() if "--" in lbl else lbl
            rows.append((i, ("B%d" % (i + 1)) if i < 8 else "EX", part))
        return rows

    def kt_wvp_sp_groups():
        # Three (header, [(index, color, title), ...]) groups for the
        # picker's card columns: her eight, the Masks, the Souls.
        her = [(i, KT_BARS[i]["color"], kt_wvp_title(KT_BARS[i]["card"]))
                for i in range(len(KT_BARS))]
        masks = []
        souls = []
        for j, meta in enumerate(KT_ENDLESS_CARDS):
            entry = (len(KT_BARS) + j, meta["color"], kt_wvp_title(meta["card"]))
            (souls if meta.get("group") == "soul" else masks).append(entry)
        return (("HER EIGHT", her), ("THE MASKS", masks), ("THE SOULS", souls))

    def kt_wvp_sp_full(idx):
        # Full card name for the picker footer.
        if idx < len(KT_BARS):
            return KT_BARS[idx]["card"]
        return KT_ENDLESS_CARDS[idx - len(KT_BARS)]["card"]

    # SFX table (ZUN-standard cue names, shipped in assets/audio/sfx/touhou/). Volumes are
    # relative; playback rides MSBF's pooled channels so cues overlap cleanly.
    def kt_se(name):
        return KT_SE_DIR + name + ".wav"

    KT_SFX = {
        "shot":      (kt_se("se_plst00"), 0.16),
        "hit":       (kt_se("se_damage00"), 0.30),
        "hit_low":   (kt_se("se_damage01"), 0.38),
        "fire":      (kt_se("se_tan00"), 0.42),
        "fire2":     (kt_se("se_tan01"), 0.42),
        "fire3":     (kt_se("se_tan02"), 0.42),
        "gun":       (kt_se("se_gun00"), 0.45),
        "laser":     (kt_se("se_lazer00"), 0.5),
        "laser2":    (kt_se("se_lazer01"), 0.5),
        "graze":     (kt_se("se_graze"), 0.5),
        "death":     (kt_se("se_pldead00"), 0.9),
        "bomb":      (kt_se("se_slash"), 0.9),
        "bomb2":     (kt_se("se_nice"), 0.5),
        "declare":   (kt_se("se_cat00"), 0.8),
        "charge":    (kt_se("se_ch00"), 0.55),
        "charge2":   (kt_se("se_ch01"), 0.6),
        "capture":   (kt_se("se_cardget"), 0.9),
        "break":     (kt_se("se_enep01"), 0.9),
        "break_sm":  (kt_se("se_enep00"), 0.85),
        "extend":    (kt_se("se_powerup"), 0.9),
        "bomb_up":   (kt_se("se_power1"), 0.8),
        "warn":      (kt_se("se_timeout"), 0.7),
        "warn2":     (kt_se("se_timeout2"), 0.8),
        "kira":      (kt_se("se_kira01"), 0.3),
        "pause":     (kt_se("se_pause"), 0.7),
        "ok":        (kt_se("se_ok00"), 0.6),
        "invalid":   (kt_se("se_invalid"), 0.7),
    }

    # Channel layout. MSBF's shared 8-channel round-robin is NOT enough here:
    # at 60fps danmaku density (player shot + pattern fire + graze can exceed
    # 30 cues/sec) the rotation wraps in ~0.2s and cuts off every longer cue,
    # which reads as "monophonic". So Kotonoha mode gets its own channels,
    # split by role:
    #   * SOLO channels for the three constant spammers (player shot, graze,
    #     boss-damage tink). Each retriggers only ITSELF -- the authentic
    #     Touhou sound -- and never churns a pool.
    #   * A small round-robin for pattern-fire cues (tan/gun/lazer).
    #   * A wide round-robin for everything that must NEVER be cut (death,
    #     bomb, declare, capture, extend, warnings...), which now sees only a
    #     few cues a second.
    # Both pools allocate through msbf_pick_pool_channel (battle_logic.rpy),
    # which prefers a channel that is actually idle over the next one in
    # rotation -- splitting by role reduced how often the cursor lapped a live
    # cue, but only checking before writing removed the truncation outright.
    KT_SOLO_CHANNELS = {
        "shot": "kt_solo_shot",
        "graze": "kt_solo_graze",
        "hit": "kt_solo_hit",
        "hit_low": "kt_solo_hit",
    }
    KT_FIRE_NAMES = ("fire", "fire2", "fire3", "gun", "laser", "laser2")
    KT_FIRE_POOL = ["kt_fire_%d" % i for i in range(4)]
    KT_SFX_POOL = ["kt_sfx_%d" % i for i in range(10)]
    for _kt_ch in KT_SFX_POOL + KT_FIRE_POOL + list(set(KT_SOLO_CHANNELS.values())):
        if not renpy.music.channel_defined(_kt_ch):
            renpy.music.register_channel(_kt_ch, mixer="sfx", loop=False)

    def kt_play(name, volume_scale=1.0):
        entry = KT_SFX.get(name)
        if not entry:
            return
        vol = entry[1] * volume_scale
        try:
            solo = KT_SOLO_CHANNELS.get(name)
            if solo:
                channel = solo
            elif name in KT_FIRE_NAMES:
                channel = msbf_pick_pool_channel(KT_FIRE_POOL, "fire_cursor", kt_play)
            else:
                # The wide pool exists so a long cue (declare, capture, extend,
                # the death roar) can ring out under the constant chatter. A blind
                # cursor still cut them the moment the rotation lapped, so the
                # picker looks for an IDLE channel first and only evicts the
                # oldest cue when all eight really are busy. See the POOL
                # ALLOCATION block in battle_logic.rpy.
                channel = msbf_pick_pool_channel(KT_SFX_POOL, "cursor", kt_play)
            if channel is None:
                return
            renpy.sound.play(entry[0], channel=channel, relative_volume=vol)
        except Exception:
            pass

    def kt_clamp(v, lo, hi):
        return max(lo, min(hi, v))

    # Screen-poll helper: the fight screen runs a slow 0.25s timer on this; a
    # non-None return ends the interaction with that value (Function() action
    # semantics), which is how the CDD hands "victory"/"defeat"/"quit" (or the
    # wave viewer's "wave_done") back to the script without any per-tick
    # interaction restarts.
    def kt_poll_result(game):
        return game.result

# --- SIMULATION CORE ---------------------------------------------------------
init python:
    class KTGame(object):
        """All of Kotonoha mode's live state. Stepped at a fixed 60Hz by the
        KTStage displayable; owns zero rendering. Bullets/shots/sparks are
        plain dicts in plain lists -- the hot loops stay tight python."""

        def __init__(self, start_bar=0, continues_used=0, practice=False, debug=False, endless=False,
                    debug_wave=None):
            # KTGame is intentionally plain-data heavy. Keep Matsu'Py displayables,
            # Text objects, Render objects, and Transform objects out of here;
            # the simulation should be cheap to mutate and easy to snapshot.
            self.result = None
            self.paused = False
            self.practice = practice     # unlimited lives; hiscore/clear don't count
            self.debug = debug           # DEV ONLY: one-shot bars + unlimited lives, no records
            self.endless = endless       # random cards forever, real lives, own records, no victory
            # (practice AND endless = Endless Practice: the same hat, practice
            # rules -- unlimited lives, and NO record of either kind.)
            # DEV ONLY wave viewer: a forced (ns_index, sp_index) pair, read
            # exactly once -- its break finishes with "wave_done" (back to the
            # mode selector). No victory, no records (callers pair it with
            # practice=True for infinite lives).
            self.debug_wave = debug_wave

            # Run counters. tick is the authoritative clock for deterministic
            # gameplay. phase_tick is reset on each state-machine transition.
            self.deaths = 0
            self.tick = 0
            self.score = 0
            self.graze = 0
            self.lives = KT_START_LIVES
            self.bombs = KT_START_BOMBS
            self.captures = 0
            self.bars_broken = 0
            self.continues_used = continues_used
            self.extend_index = 0
            self.start_bar = start_bar
            self.bar_index = start_bar

            # Endless bookkeeping. endless_wave counts survived waves; ns_pat /
            # sp_pat decouple which pattern runs from bar_index so a wave can
            # pair ANY nonspell with ANY spell card. In a normal fight these
            # always equal bar_index, so the fixed run is unchanged. speed_mul
            # is a gentle global bullet-speed ramp applied in _add (1.0 normal).
            self.endless_wave = 0
            self.ns_pat = start_bar
            self.sp_pat = start_bar
            self._last_sp = -1
            self._last_ns = -1
            self.speed_mul = 1.0
            # "Current bar" presentation: card name/accent-colour/capture value/
            # timers/movement. _start_bar fills these -- from KT_BARS in a normal
            # run, or from a random roll in endless.
            _b0 = KT_BARS[start_bar]
            self.cur_card = _b0["card"]
            self.cur_color = _b0["color"]
            self.cur_value = _b0["value"]
            self.cur_ns_time = _b0["ns_time"]
            self.cur_sp_time = _b0["sp_time"]
            self.cur_moves = KT_BAR_MOVES[start_bar]
            # Mask/Soul-card plumbing (endless): special mechanic tag +
            # presentation flags. A normal fight leaves all three at rest.
            self.cur_special = None
            self.cur_is_mask = False
            self.cur_is_soul = False
            # The running card's (captures, attempts) for the HUD's HISTORY
            # line, set when the spell starts (see _record_attempt).
            self.cur_hist = (0, 0)

            # Player. px/py are stage-local coordinates. invuln_until and
            # dying_tick are absolute ticks, not durations; comparing them to
            # self.tick avoids drift when the renderer catches up after hitches.
            self.px = KT_W * 0.5
            self.py = KT_H - 80.0
            self.focus = False
            self.shooting = False
            self.shot_cd = 0
            self.invuln_until = 0
            self.dying_tick = None      # deathbomb window opens here
            # Patience rule (calm bullets, _sp17): consecutive ticks the soul
            # has not displaced. still_ticks > 0 means "still" -- a calm blade
            # cannot cut a still soul. Updated in step() right after input.
            self.still_ticks = 0
            self._still_px = self.px
            self._still_py = self.py

            # Boss. bx/by is the current drawn gameplay position, btx/bty is
            # the soft target for movement interpolation. Patterns fire from
            # bx/by; the renderer adds only cosmetic bob/shake afterward.
            self.bx = KT_W * 0.5
            self.by = -90.0
            self.btx = KT_W * 0.5
            self.bty = 118.0
            self.bmove = "center"
            self.boss_hp = 1.0
            self.boss_hp_max = 1.0
            self.boss_flash = 0
            self.mirror_on = False
            self.dark = 0.0             # koto.spotlight strength (spell 5)
            self.stop_until = 0         # Seer mask: enemy time is frozen while tick < this
            self.portals = []           # Seer mask: border "gap" seams the renderer draws
            self.graze_tick = -999      # last graze tick (renderer pulses the ship)

            # Phase machine: intro -> (nonspell -> declare -> spell -> break) x8
            # -> victory; defeat can interrupt anywhere.
            self.phase = "intro"
            self.phase_tick = 0
            self.time_left = 0
            self.spell_ok = True        # no death/bomb yet this card
            self.warned = set()
            self.scratch = {}           # per-pattern state (wind, waves, spokes)

            # Entities + juice. These lists are the whole active scene graph
            # from the simulation's point of view. Rendering code may read them
            # but should not own their lifetime.
            self.bullets = []
            self.shots = []
            self.sparks = []
            self.cancels = []           # cleared bullets' stars, flying home
            self.banners = []
            self.lasers = []            # Touhou beams: telegraph -> fire -> fade
            self.death_fx = []          # recent deaths, for the pichun ring
            self.bomb_tick = None
            self.over_tick = None

            # Cosmetic FX the renderer reads. Owned by the sim so they freeze on
            # pause and step at the fixed 60Hz like everything else:
            #   ambient      -- a fixed pool of drifting atmosphere motes that
            #                   wraps forever (the stage always breathes).
            #   muzzle       -- tick of the last "boss cast" flare (+ strength).
            #   screen_flash -- a decaying full-stage colour wash for big events.
            #   ring_fx      -- expanding msbf.ring shockwaves on declare/break/
            #                   capture.
            self.ambient = []
            self.muzzle = -999
            self.muzzle_str = 0.0
            self.screen_flash = None
            self.ring_fx = []
            self._init_ambient()

            # Input edge/cooldown bookkeeping. _prev_x lets bombs trigger on
            # press rather than every tick X is held. _se_cd is per-run SFX
            # throttling on top of kt_play's channel pools. `keys` is the shared
            # release latch that keeps a swallowed key-up from gluing the ship to
            # one direction (MSBFKeyLatch, battle_logic.rpy).
            self._prev_x = False
            self._se_cd = {}
            self.keys = MSBFKeyLatch()

        # ----- tiny helpers ---------------------------------------------------

        def _se(self, name, cd=0, vol=1.0):
            # cd is a tick cooldown per logical cue name. This keeps patterns
            # that spawn many bullets in one burst from also spawning many
            # identical sound instances in that same burst.
            if cd:
                last = self._se_cd.get(name, -999)
                if self.tick - last < cd:
                    return
                self._se_cd[name] = self.tick
            # Muzzle flare: every boss fire cue lights a flash at Kotonoha, so a
            # volley reads as HER casting rather than bullets appearing from air.
            # Riding the cd-gated cue means it pulses at the pattern's cadence.
            if name in KT_FIRE_NAMES:
                self.muzzle = self.tick
                self.muzzle_str = 1.0 if name in ("gun", "laser", "laser2", "fire3") else 0.55
            kt_play(name, vol)

        def _banner(self, text, ci=13, size=26, ttl=150, y=None):
            # Popups STACK: each new banner takes the first free row among the
            # ones still alive, so a bar break that pays out capture bonus +
            # EXTEND + bomb stock in the same tick prints three tidy rows
            # instead of overprinting one spot.
            live = [b for b in self.banners if self.tick - b["born"] <= b["ttl"]]
            used = set(b.get("slot", 0) for b in live)
            slot = 0
            while slot in used:
                slot += 1
            live.append({
                "text": text, "ci": ci, "size": size,
                "born": self.tick, "ttl": ttl, "slot": slot,
                "y": (KT_H * 0.38 + slot * 46.0) if y is None else y,
            })
            self.banners = live[-6:]

        def _add_score(self, amount):
            # All scoring funnels through here so extends cannot be missed.
            # This is also why graze/hit/bullet-clear code does not directly
            # alter lives: score thresholds are the single source of extends.
            self.score += amount
            # Endless Mode grants NO extra lives (Kotonoha's rule) -- you still
            # earn bombs on every bar break, just never a new life. So the
            # score-threshold extends are skipped entirely there.
            if self.endless:
                return
            while (self.extend_index < len(KT_EXTEND_SCORES)
                    and self.score >= KT_EXTEND_SCORES[self.extend_index]):
                self.extend_index += 1
                if self.lives < KT_MAX_LIVES:
                    self.lives += 1
                self._se("extend", 0, 1.0)
                self._banner("EXTEND!", 8, 40, 170)

        def _spark_burst(self, x, y, n, ci, spd=2.6, ttl=34):
            room = KT_MAX_SPARKS - len(self.sparks)
            for i in range(min(n, max(0, room))):
                a = (math.pi * 2.0 * i / max(1, n)) + (self.tick * 0.13)
                s = spd * (0.55 + 0.45 * ((i * 7) % 3) / 2.0)
                self.sparks.append({
                    "x": x, "y": y,
                    "vx": math.cos(a) * s, "vy": math.sin(a) * s,
                    "age": 0, "ttl": ttl, "ci": ci,
                })

        # ----- cosmetic juice (ambient motes, screen flash, shockwaves) --------

        def _init_ambient(self):
            # A CONSTANT-size pool of soft motes drifting up over the shrine so
            # the arena always feels alive, independent of the danmaku. They wrap
            # around the playfield forever -- no spawning, no cap churn, so the
            # per-tick cost is fixed. Purely cosmetic; random init is fine
            # because the fight blocks rollback.
            self.ambient = []
            # Weighted toward pink/white with a little cyan/yellow; a few "big"
            # ones become slow drifting petals in the renderer.
            soft = (13, 1, 1, 6, 10, 13, 1, 13)
            for i in range(46):
                self.ambient.append({
                    "x": kt_random.uniform(0.0, KT_W),
                    "y": kt_random.uniform(0.0, KT_H),
                    "vx": kt_random.uniform(-0.11, 0.11),
                    "vy": kt_random.uniform(-0.60, -0.18),
                    "ci": soft[i % len(soft)],
                    "scb": 1 if (i % 3 == 0) else 0,      # 2 size buckets
                    "ph": kt_random.uniform(0.0, 6.28),
                    "big": (i % 11 == 0),
                })

        def _update_ambient(self):
            # Drift + wrap. Runs every step (even intro/victory/defeat) so the
            # atmosphere never stalls; only pause freezes it (step() returns).
            for m in self.ambient:
                m["x"] += m["vx"]
                m["y"] += m["vy"]
                m["ph"] += 0.045
                if m["y"] < -14.0:
                    m["y"] = KT_H + 10.0
                    m["x"] = (m["x"] * 1.7 + self.tick * 11.0) % KT_W
                if m["x"] < -14.0:
                    m["x"] = KT_W + 10.0
                elif m["x"] > KT_W + 14.0:
                    m["x"] = -10.0

        def _flash(self, col, ttl=26, peak=90):
            # Full-stage colour wash the renderer decays from peak alpha to 0
            # over ttl ticks. Used for the loud beats (declare / capture / break).
            self.screen_flash = {"col": col, "born": self.tick, "ttl": ttl, "peak": peak}

        def _ring_fx(self, x, y, rgb, quad=520):
            # Queue an expanding msbf.ring shockwave (same shader the bomb and
            # victory booms use). rgb is a 0..1 tuple. Capped so a frantic run
            # can't stack unbounded rings.
            self.ring_fx.append({"x": x, "y": y, "col": rgb, "quad": quad, "born": self.tick})
            if len(self.ring_fx) > 5:
                del self.ring_fx[0]

        def _clear_bullets(self, score_each=KT_SCORE_CLEAR, center=None, radius=None):
            """Wipe bullets (all, or within radius of center) into sparkles.
            Returns how many went. Sparkles are stride-limited so a 400-bullet
            wipe doesn't blow the spark cap in one tick."""
            kept = []
            gone = 0
            r2 = (radius * radius) if radius is not None else None
            cx, cy = center if center else (0.0, 0.0)
            for b in self.bullets:
                if r2 is not None:
                    dx = b["x"] - cx
                    dy = b["y"] - cy
                    if dx * dx + dy * dy > r2:
                        kept.append(b)
                        continue
                gone += 1
                # Every cleared bullet leaves a cancel star of its own colour
                # (the modern read: the field POURS into you rather than just
                # vanishing), kicked a little off its own heading along the
                # golden angle so a dense wipe blooms instead of stacking.
                if len(self.cancels) < KT_MAX_CANCELS:
                    ga = gone * 2.39996
                    self.cancels.append({
                        "x": b["x"], "y": b["y"],
                        "vx": b["vx"] * 0.25 + math.cos(ga) * 0.9,
                        "vy": b["vy"] * 0.25 + math.sin(ga) * 0.9 - 1.1,
                        "age": 0, "ci": b["ci"], "ph": gone % 2,
                    })
                if gone % 5 == 1 and len(self.sparks) < KT_MAX_SPARKS:
                    self.sparks.append({
                        "x": b["x"], "y": b["y"],
                        "vx": b["vx"] * 0.3, "vy": b["vy"] * 0.3 - 0.8,
                        "age": 0, "ttl": 30, "ci": b["ci"],
                    })
            self.bullets = kept
            # Beams go with the bullets. A radius-limited wipe (the bomb's
            # growing circle) only cuts beams whose ORIGIN is inside it, so a
            # bomb cannot silently delete a laser that is still crossing the
            # far side of the stage.
            if self.lasers:
                if r2 is None:
                    self.lasers = []
                else:
                    self.lasers = [L for L in self.lasers
                                    if (L["x"] - cx) ** 2 + (L["y"] - cy) ** 2 > r2]
            if gone and score_each:
                self._add_score(gone * score_each)
            return gone

        # ----- input ----------------------------------------------------------

        def _poll_input(self):
            # Poll continuous keyboard state directly from pygame_sdl2 instead
            # of handling Matsu'Py key events. Arrow movement, focus, and held-Z
            # shooting are all "current state every tick" controls; event
            # callbacks are better for menus, not a 60Hz shmup.
            #
            # Every read goes through self.keys (MSBFKeyLatch, battle_logic.rpy)
            # rather than indexing the state array directly, so a key whose
            # release never reached SDL cannot leave the ship gliding -- see the
            # SHARED KEY LATCH block there for why that happens and why the latch
            # can only ever unstick a key, never fake one. KTStage.event() is what
            # feeds it the real key events.
            try:
                import pygame_sdl2 as pg
                keys = pg.key.get_pressed()
            except Exception:
                return

            # Another window owns the keyboard: hold everything at rest instead of
            # coasting on whatever SDL last saw.
            if not self.keys.focused():
                self.focus = False
                self.shooting = False
                self._prev_x = False
                self.keys.clear()
                return

            self.focus = self.keys.pressed(keys, pg.K_LSHIFT, pg.K_RSHIFT)
            self.shooting = self.keys.pressed(keys, pg.K_z)
            x_now = self.keys.pressed(keys, pg.K_x)
            if x_now and not self._prev_x:
                self._try_bomb()
            self._prev_x = x_now

            # Movement stops once a terminal result exists, but focus/shooting
            # flags above are still updated so visual state does not get stuck
            # if the player releases keys during the end-card.
            if self.result is not None or self.phase in ("victory", "defeat"):
                return
            dx = dy = 0.0
            if self.keys.pressed(keys, pg.K_LEFT):
                dx -= 1.0
            if self.keys.pressed(keys, pg.K_RIGHT):
                dx += 1.0
            if self.keys.pressed(keys, pg.K_UP):
                dy -= 1.0
            if self.keys.pressed(keys, pg.K_DOWN):
                dy += 1.0
            if dx == 0.0 and dy == 0.0:
                return
            if dx != 0.0 and dy != 0.0:
                dx *= 0.70710678
                dy *= 0.70710678
            speed = KT_FOCUS if self.focus else KT_MOVE
            self.px = kt_clamp(self.px + dx * speed, 10.0, KT_W - 10.0)
            self.py = kt_clamp(self.py + dy * speed, 10.0, KT_H - 10.0)

        def toggle_pause(self):
            if self.result is not None:
                return
            self.paused = not self.paused
            kt_play("pause")
            renpy.restart_interaction()

        def give_up(self):
            if self.result is None:
                self.paused = False
                self._finish("quit")
                renpy.restart_interaction()

        # ----- player: shots, bomb, death -------------------------------------

        def _update_player(self):
            # Player shots are intentionally simple projectiles: no collision
            # against bullets, no item collection, no power meter. That keeps
            # the hot path readable and lets pattern density be the difficulty.
            if self.shot_cd > 0:
                self.shot_cd -= 1
            can_shoot = (self.result is None and self.dying_tick is None
                            and self.phase not in ("victory", "defeat"))
            if can_shoot and self.shooting and self.shot_cd <= 0:
                self.shot_cd = KT_SHOT_EVERY
                # Debug reading (dev only): every shot one-shots the current
                # pattern, so a full clear takes seconds instead of minutes.
                dmg = 1.0e9 if self.debug else KT_SHOT_DMG
                # "f" marks a focused shot for the renderer (it draws a longer,
                # whiter needle); the sim never reads it.
                if len(self.shots) < KT_MAX_SHOTS:
                    if self.focus:
                        for ox in (-7.0, 7.0):
                            self.shots.append({"x": self.px + ox, "y": self.py - 12.0,
                                                "vx": 0.0, "vy": -KT_SHOT_SPEED, "dmg": dmg * 1.3,
                                                "f": True})
                    else:
                        for ang in (-0.13, 0.0, 0.13):
                            self.shots.append({"x": self.px, "y": self.py - 12.0,
                                                "vx": math.sin(ang) * KT_SHOT_SPEED,
                                                "vy": -math.cos(ang) * KT_SHOT_SPEED, "dmg": dmg,
                                                "f": False})
                self._se("shot", 5)

        def _try_bomb(self):
            # Bombs are denied during intro/break/end states because there is
            # nothing meaningful to save or damage there. During nonspell/spell
            # they clear bullets, grant invuln, and chip the active HP bar over
            # the expanding wave's lifetime.
            if self.result is not None or self.phase in ("victory", "defeat", "intro", "break"):
                return
            if self.bomb_tick is not None and self.tick - self.bomb_tick < KT_BOMB_WAVE_TICKS:
                return
            if self.bombs <= 0:
                self._se("invalid", 10)
                return
            self.bombs -= 1
            self.bomb_tick = self.tick
            self.dying_tick = None      # the deathbomb: X inside the window saves you
            self.invuln_until = max(self.invuln_until, self.tick + KT_BOMB_INVULN)
            if self.phase == "spell":
                self.spell_ok = False
            self._se("bomb", 0, 1.0)
            self._se("bomb2", 0, 1.0)
            self._spark_burst(self.px, self.py, 18, 1, 5.2, 44)
            self._spark_burst(self.px, self.py, 10, 13, 3.2, 36)

        def _update_bomb(self):
            # The bomb is a timed radial sweep, not an instant full-screen wipe.
            # Each tick expands the clear radius from the player's position.
            # This gives the visual shockwave and the bullet removal the same
            # rhythm, so the animation explains the mechanic.
            if self.bomb_tick is None:
                return
            t = self.tick - self.bomb_tick
            if t > int(KT_BOMB_WAVE_TICKS * 1.5):
                self.bomb_tick = None
                return
            if t <= KT_BOMB_WAVE_TICKS:
                radius = 90.0 + (760.0 - 90.0) * (t / float(KT_BOMB_WAVE_TICKS))
                self._clear_bullets(KT_SCORE_CLEAR, (self.px, self.py), radius)
                self._se("kira", 9, 0.8)
                # Wavefront glitter: sparks ride the expanding sweep so the
                # "spray and pray" visibly scrubs the screen (Touhou flair).
                if t % 2 == 0 and len(self.sparks) < KT_MAX_SPARKS - 6:
                    for k in range(3):
                        a = t * 0.53 + k * 2.0944
                        self.sparks.append({
                            "x": self.px + math.cos(a) * radius,
                            "y": self.py + math.sin(a) * radius,
                            "vx": math.cos(a) * 1.9, "vy": math.sin(a) * 1.9,
                            "age": 0, "ttl": 24, "ci": 1 if k % 2 == 0 else 13,
                        })
                if self.phase in ("nonspell", "spell"):
                    self._damage_boss(KT_BOMB_DAMAGE / float(KT_BOMB_WAVE_TICKS))

        def _register_player_hit(self):
            # A collision does not kill immediately. It opens the deathbomb
            # window; _check_deathbomb_window finalizes the hit if X was not
            # pressed quickly enough.
            if self.dying_tick is None and self.tick >= self.invuln_until:
                self.dying_tick = self.tick

        def _check_deathbomb_window(self):
            # The window is deliberately tiny (Touhou-style panic save), but it
            # is measured in simulation ticks so it remains consistent across
            # machines and renderer catch-up.
            if self.dying_tick is None:
                return
            if self.tick - self.dying_tick >= KT_DEATHBOMB_TICKS:
                self._die()

        def _die(self):
            self.dying_tick = None
            self.deaths += 1
            self.spell_ok = False
            if not (self.practice or self.debug):
                self.lives -= 1
            self._se("death", 0, 1.0)
            # The pichun: ring + flare at the death spot (renderer reads
            # death_fx). NO area wipe -- only the culprit pellet was consumed
            # (in _advance_bullets); the respawn iframes carry you back out.
            self.death_fx.append({"x": self.px, "y": self.py, "born": self.tick})
            if len(self.death_fx) > 3:
                del self.death_fx[0]
            self._spark_burst(self.px, self.py, 22, 1, 4.6, 46)
            self._spark_burst(self.px, self.py, 12, 13, 2.8, 36)
            self.px = KT_W * 0.5
            self.py = KT_H - 64.0
            if not (self.practice or self.debug) and self.lives <= 0:
                self.phase = "defeat"
                self.phase_tick = 0
                self.banners = []
                self.over_tick = self.tick + 170
            else:
                self.invuln_until = self.tick + KT_RESPAWN_INVULN

        # ----- boss ------------------------------------------------------------

        def _damage_boss(self, dmg):
            # One HP bar has two gameplay halves. Dropping from full to 50%
            # completes the nonspell and triggers the spell-card declaration;
            # dropping from 50% to 0 completes the named spell.
            if self.phase not in ("nonspell", "spell"):
                return
            self.boss_hp = max(0.0, self.boss_hp - dmg)
            self.boss_flash = 3
            half = self.boss_hp_max * 0.5
            if self.phase == "nonspell" and self.boss_hp <= half:
                seconds_left = self.time_left // 60
                self._add_score(KT_SCORE_NONSPELL + 2000 * seconds_left)
                self._se("break_sm", 0, 1.0)
                self._start_declare()
            elif self.phase == "spell" and self.boss_hp <= 0.0:
                self._end_spell(captured=self.spell_ok, timeout=False)

        def _move_boss(self):
            # Movement modes only set target positions. The final interpolation
            # at the bottom makes transitions readable and keeps pattern origins
            # smooth even when "dart" chooses a new random-looking anchor.
            t = self.tick
            mode = self.bmove
            if mode == "sway":
                self.btx = KT_W * 0.5 + math.sin(t * 0.008) * 170.0
                self.bty = 112.0 + math.sin(t * 0.013) * 24.0
            elif mode == "sweep":
                self.btx = KT_W * 0.5 + math.sin(t * 0.004) * 232.0
                self.bty = 104.0 + math.sin(t * 0.009) * 16.0
            elif mode == "dart":
                if (self.phase_tick % 150) == 0:
                    k = (self.phase_tick // 150) * 53 + self.bar_index * 17
                    self.btx = 90.0 + ((k * 97) % 441)
                    self.bty = 80.0 + ((k * 61) % 90)
            elif mode == "high":
                self.btx = KT_W * 0.5 + math.sin(t * 0.006) * 90.0
                self.bty = 84.0
            elif mode == "wild":
                # Abandoner mask: dart's reckless cousin -- new anchor twice as
                # often, wider range, and a hungrier lerp below. She is never
                # where she was.
                if (self.phase_tick % 80) == 0:
                    k = (self.phase_tick // 80) * 41 + self.endless_wave * 13
                    self.btx = 70.0 + ((k * 113) % 481)
                    self.bty = 70.0 + ((k * 71) % 150)
            elif mode == "blink":
                # Interloper mask: no travel at all. She is HERE, then she is
                # THERE, with a green tear of sparks at both ends of the edit.
                if (self.phase_tick % 110) == 0 and self.phase_tick > 0:
                    k = (self.phase_tick // 110) * 29 + self.endless_wave * 7
                    nx = 90.0 + ((k * 131) % 441)
                    ny = 76.0 + ((k * 53) % 120)
                    self._spark_burst(self.bx, self.by, 10, 8, 3.0, 24)
                    self.bx = self.btx = nx
                    self.by = self.bty = ny
                    self._spark_burst(nx, ny, 10, 8, 3.0, 24)
                    self._se("kira", 0, 0.8)
            else:  # center
                self.btx = KT_W * 0.5
                self.bty = 118.0
            k_lerp = 0.10 if mode == "wild" else 0.045
            self.bx += (self.btx - self.bx) * k_lerp
            self.by += (self.bty - self.by) * k_lerp
            if self.boss_flash > 0:
                self.boss_flash -= 1

        # ----- bar / spell-card state machine ----------------------------------

        def _start_bar(self, index):
            # New bar, new nonspell: reset per-pattern scratch state and pick
            # the nonspell movement mode. HP starts at the FULL bar value even
            # though nonspell only needs to burn it down to half.
            #
            # `index` is the bar number in a normal fight and the WAVE number in
            # endless. A normal fight reads KT_BARS straight (ns_pat == sp_pat ==
            # bar_index, so nothing about the fixed run changes); endless rolls
            # a random nonspell + spell card and scales HP/value by the wave.
            if self.endless:
                self._roll_endless_wave(index)
            elif self.debug_wave is not None:
                # Wave viewer: one forced pairing at wave-0 HP, read ONCE --
                # the break after its spell finishes with "wave_done".
                self._apply_wave_identity(self.debug_wave[0], self.debug_wave[1], 0)
            else:
                bar = KT_BARS[index]
                self.bar_index = index
                self.ns_pat = index
                self.sp_pat = index
                self.cur_card = bar["card"]
                self.cur_color = bar["color"]
                self.cur_value = bar["value"]
                self.cur_ns_time = bar["ns_time"]
                self.cur_sp_time = bar["sp_time"]
                self.cur_moves = KT_BAR_MOVES[index]
                self.cur_special = None
                self.cur_is_mask = False
                self.cur_is_soul = False
                self.boss_hp_max = float(bar["hp"])
                self.boss_hp = float(bar["hp"])
            self.phase = "nonspell"
            self.phase_tick = 0
            self.time_left = self.cur_ns_time
            self.spell_ok = True
            self.warned = set()
            self.scratch = {}
            self.mirror_on = False
            self.bmove = self.cur_moves[0]

        def _apply_wave_identity(self, ns, sp, wave):
            # Resolve a (nonspell, spell) index pair into every cur_* field.
            # Shared by endless rolls and the debug wave viewer. Identity
            # (card name / accent colour / value / spell movement / special
            # mechanics) follows the SPELL; the nonspell only lends its own
            # pattern and opening movement.
            #
            # HP is the UNIFORM endless ladder: one step per wave, capped at
            # wave 8 (KT_EHP_CAP_WAVE) -- the pattern you rolled is the
            # difficulty, never an HP lottery, and every half-bar stays
            # burnable inside its clock at the cap.
            self.ns_pat = ns
            if ns >= len(KT_BARS):
                ns_meta = KT_ENDLESS_NS[ns - len(KT_BARS)]
                ns_move = ns_meta["move"]
                self.cur_ns_time = ns_meta["ns_time"]
            else:
                ns_move = KT_BAR_MOVES[ns][0]
                self.cur_ns_time = KT_BARS[ns]["ns_time"]
            self.sp_pat = sp
            if sp >= len(KT_BARS):
                meta = KT_ENDLESS_CARDS[sp - len(KT_BARS)]
                self.cur_special = meta["special"]
                grp = meta.get("group", "mask")
                self.cur_is_mask = (grp == "mask")
                self.cur_is_soul = (grp == "soul")
                sp_move = meta["move"]
            else:
                meta = KT_BARS[sp]
                self.cur_special = None
                self.cur_is_mask = False
                self.cur_is_soul = False
                sp_move = KT_BAR_MOVES[sp][1]
            self.cur_card = meta["card"]
            self.cur_color = meta["color"]
            self.cur_sp_time = meta["sp_time"]
            self.cur_value = int(meta["value"] * (1.0 + wave * 0.12))
            self.cur_moves = (ns_move, sp_move)
            self.boss_hp_max = float(KT_EHP_BASE + KT_EHP_STEP * min(wave, KT_EHP_CAP_WAVE))
            self.boss_hp = self.boss_hp_max
            self.speed_mul = 1.0 + min(0.30, wave * 0.02)

        def _roll_endless_wave(self, wave):
            # Roll a fresh random wave. HOUSE RULE: the WHOLE hat is in play
            # from wave one -- all 8 fixed-bar nonspells + the 4 Endless-only
            # ones, all 8 fixed spell cards + the 8 Mask cards -- and every
            # entry is EQUALLY likely. The only constraint is no immediate
            # repeat: never the same nonspell or the same spell card twice
            # running. The wave never ends in victory -- _run_phase just rolls
            # the next one after each break.
            self.endless_wave = wave
            self.bar_index = self.start_bar     # kept stable; endless tracks waves

            # Uniform draws over everything except last wave's picks.
            ns_opts = [i for i in range(len(KT_BARS) + len(KT_ENDLESS_NS))
                        if i != self._last_ns]
            ns = ns_opts[kt_random.randrange(0, len(ns_opts))]
            self._last_ns = ns
            sp_opts = [i for i in range(len(KT_BARS) + len(KT_ENDLESS_CARDS))
                        if i != self._last_sp]
            sp = sp_opts[kt_random.randrange(0, len(sp_opts))]
            self._last_sp = sp
            self._apply_wave_identity(ns, sp, wave)

            # Wave splash: call the wave out loud (and the mask or soul, when
            # she reaches for one -- the extra banner is the player's tell
            # that an Endless-exclusive card is coming).
            self._banner("WAVE %d" % (wave + 1), self.cur_color, 30, 140)
            if self.cur_is_mask:
                self._banner("A MASK SLIPS ON...", 13, 20, 160)
                self._flash(KT_PAL[self.cur_color], 20, 60)
            elif self.cur_is_soul:
                self._banner("AN OLD SOUL RESONATES...", 13, 20, 160)
                self._flash(KT_PAL[self.cur_color], 20, 60)

        def _start_declare(self):
            # Declaration is a short non-damaging breather. It clears the old
            # bullet field, recenters Kotonoha, plays the spell-card tell, and
            # gives the renderer time to show the card banner before patterns
            # resume.
            self._clear_bullets(KT_SCORE_CLEAR)
            self.phase = "declare"
            self.phase_tick = 0
            self.bmove = "center"
            self.portals = []           # any Seer gaps close with the old pattern
            self.stop_until = 0
            self._se("declare", 0, 1.0)
            self._se("charge", 0, 1.0)
            # Loud declaration: a card-colour wash + an outgoing shockwave.
            self._flash(KT_PAL[self.cur_color], 22, 78)
            self._ring_fx(self.bx, self.by, Color(KT_PAL[self.cur_color]).rgb, 520)
            # Charge implosion: sparks rush INTO Kotonoha.
            for i in range(16):
                a = math.pi * 2.0 * i / 16.0
                if len(self.sparks) < KT_MAX_SPARKS:
                    self.sparks.append({
                        "x": self.bx + math.cos(a) * 170.0,
                        "y": self.by + math.sin(a) * 170.0,
                        "vx": -math.cos(a) * 4.2, "vy": -math.sin(a) * 4.2,
                        "age": 0, "ttl": 40, "ci": self.cur_color,
                    })
            # Seam split: the ribbon opens from a hairline, so the hairline
            # throws sparks sideways as it goes. Spawned here rather than left
            # to the renderer because sparks are simulation state -- they have
            # to keep drifting after the cut-in has shut, and they have to
            # freeze with everything else under the pause overlay.
            for i in range(14):
                if len(self.sparks) >= KT_MAX_SPARKS:
                    break
                side = -1.0 if i % 2 else 1.0
                self.sparks.append({
                    "x": KT_W * 0.5 + side * (18.0 + i * 9.0),
                    "y": KT_DECL_BAND_MID + (i % 3 - 1) * 2.0,
                    "vx": side * (5.0 + (i % 4) * 1.4), "vy": (i % 3 - 1) * 0.35,
                    "age": 0, "ttl": 34, "ci": self.cur_color,
                })

        def _records_history(self):
            # Only a real reading writes history -- the same rule that keeps
            # practice, debug and the wave viewer out of the hi-score.
            return not (self.practice or self.debug or self.debug_wave is not None)

        def _record_attempt(self):
            try:
                hist = persistent.kotomode_card_history or {}
                cap, att = hist.get(self.cur_card, (0, 0))
                if self._records_history():
                    att += 1
                    hist = dict(hist)
                    hist[self.cur_card] = [cap, att]
                    persistent.kotomode_card_history = hist
                self.cur_hist = (cap, att)
            except Exception:
                self.cur_hist = (0, 0)

        def _record_capture(self):
            if not self._records_history():
                return
            try:
                hist = dict(persistent.kotomode_card_history or {})
                cap, att = hist.get(self.cur_card, (0, 1))
                hist[self.cur_card] = [cap + 1, max(att, cap + 1)]
                persistent.kotomode_card_history = hist
                self.cur_hist = (cap + 1, max(att, cap + 1))
            except Exception:
                pass

        def _start_spell(self):
            # Spell state starts from the remaining half-bar HP. spell_ok is
            # reset here because capture eligibility belongs to the named card,
            # not to the preceding nonspell/declaration. The mosaic mirror keys
            # off the SPELL pattern (sp_pat 5) so it works in endless too.
            self.phase = "spell"
            self.phase_tick = 0
            self.time_left = self.cur_sp_time
            self.warned = set()
            self.scratch = {}
            self.spell_ok = True
            # The mosaic mirror (sp_pat 5) and the Mask of You both put a
            # phantom on the stage; the renderer picks WHICH phantom by
            # cur_special ("you" mirrors the player's own ship).
            self.mirror_on = (self.sp_pat == 5) or (self.cur_special == "you")
            self.bmove = self.cur_moves[1]
            self._record_attempt()

        def _end_spell(self, captured, timeout):
            # "captured" means the card ended with no bomb and no death during
            # this spell. Timeouts usually fail the capture, except the final
            # card, whose design is explicitly a survival spell.
            self.mirror_on = False
            # The FINAL survival card (sp_pat 7) is part survival: lasting the
            # whole clock without a death or bomb counts as the capture. Keying
            # off the pattern (not bar_index) keeps that true in endless too.
            if timeout and self.sp_pat == len(KT_BARS) - 1 and self.spell_ok:
                captured = True
            if captured:
                self.captures += 1
                self._record_capture()
                self._add_score(self.cur_value)
                self._se("capture", 0, 1.0)
                self._banner("SPELL CARD CAPTURED!  +" + format(self.cur_value, ","), 10, 30, 190)
                self._flash(KT_PAL[self.cur_color], 30, 120)
                self._ring_fx(self.bx, self.by, Color(KT_PAL[self.cur_color]).rgb, 640)
            elif timeout:
                self._add_score(self.cur_value // 10)
                self._banner("TIME OUT...", 14, 26, 150)
            else:
                self._banner("BONUS FAILED...", 14, 26, 150)
            self._start_break(timeout)

        def _start_break(self, timeout=False):
            # Break is the payout/transition beat after a spell. It clears
            # bullets, pays the bar bonus, stocks one bomb if possible, and
            # gives the renderer a short celebration before the next bar starts.
            self.phase = "break"
            self.phase_tick = 0
            self.bars_broken = max(self.bars_broken, self.bar_index + 1)
            self.portals = []
            self.stop_until = 0
            self._clear_bullets(KT_SCORE_CLEAR)
            self._se("break", 0, 1.0)
            self._spark_burst(self.bx, self.by, 30, self.cur_color, 5.2, 52)
            self._spark_burst(self.bx, self.by, 16, 13, 3.2, 44)
            # Warm gold burst-flash + a fat send-off shockwave for the break.
            self._flash("#fff0c8", 24, 88)
            self._ring_fx(self.bx, self.by, (1.0, 0.9, 0.68), 720)
            tier = self.endless_wave if self.endless else self.bar_index
            bonus = 80000 * (tier + 1)
            if not timeout:
                bonus += 2000 * (self.time_left // 60)
            self._add_score(bonus)
            if self.bombs < KT_MAX_BOMBS:
                self.bombs += 1
                self._se("bomb_up", 0, 1.0)
                self._banner("+1 BOMB", 11, 22, 130)

        def _run_phase(self):
            # This is the only place that advances the high-level fight state.
            # Keep state transitions here; helper methods should set up states,
            # not secretly skip to unrelated phases.
            if self.phase == "intro":
                if self.phase_tick >= 170:
                    self._start_bar(self.bar_index)
                return

            if self.phase == "declare":
                # Three cues across the beat, not one: the charge swells while
                # the ribbon holds, and the shut gets its own tick so the card
                # does not simply stop being declared.
                if self.phase_tick == 46:
                    self._se("charge2", 0, 0.9)
                elif self.phase_tick == KT_DECL_CLOSE:
                    self._se("kira", 0, 0.85)
                if self.phase_tick >= KT_DECLARE_TICKS:
                    self._start_spell()
                return

            if self.phase == "break":
                if self.phase_tick == 30 or self.phase_tick == 55:
                    self._spark_burst(self.bx + math.sin(self.tick) * 40.0,
                                    self.by + math.cos(self.tick * 0.7) * 30.0,
                                    10, 13, 3.4, 30)
                    self._se("break_sm", 0, 0.7)
                if self.phase_tick >= 105:
                    if self.endless:
                        # Endless never wins -- just roll the next, harder wave.
                        self._start_bar(self.endless_wave + 1)
                    elif self.debug_wave is not None:
                        # Wave viewer: one full bar was the deal. Hand control
                        # back to the mode selector instead of rereading the
                        # same page forever.
                        self._finish("wave_done")
                    elif self.bar_index + 1 >= len(KT_BARS):
                        self.phase = "victory"
                        self.phase_tick = 0
                        self.banners = []
                        self.over_tick = self.tick + 400
                        self._se("charge", 0, 1.0)
                    else:
                        self._start_bar(self.bar_index + 1)
                return

            if self.phase == "victory":
                # Boss-death cinematic: escalating detonations rock her sprite
                # (the renderer adds shake/flicker + shock rings keyed off
                # phase_tick), one final white-out boom at 96, then celebratory
                # twinkles under the results text.
                pt = self.phase_tick
                if pt in (14, 34, 52, 68, 82):
                    # Stagger small explosions around the boss using sine/cosine
                    # offsets from the current phase tick. The exact positions
                    # are deterministic but feel irregular.
                    ox = math.sin(pt * 3.1) * 34.0
                    oy = math.cos(pt * 2.3) * 24.0
                    self._spark_burst(self.bx + ox, self.by + oy, 16,
                        2 if pt % 4 == 2 else 13, 4.6, 40)
                    self._se("break_sm", 0, 0.8)
                if pt == 96:
                    self._spark_burst(self.bx, self.by, 30, 1, 6.0, 55)
                    self._spark_burst(self.bx, self.by, 18, 13, 3.6, 60)
                    self._se("break", 0, 1.0)
                    self._se("laser2", 0, 0.7)
                if pt == 150:
                    self._se("capture", 0, 1.0)
                if pt > 130 and pt % 7 == 0 and len(self.sparks) < KT_MAX_SPARKS - 4:
                    # Cheap deterministic confetti: multiplying by primes and
                    # modding by the playfield scatters twinkles without random.
                    k = pt * 37
                    self.sparks.append({"x": float(k % KT_W), "y": float((k * 29) % KT_H),
                        "vx": 0.0, "vy": -0.35,
                        "age": 0, "ttl": 56, "ci": (1, 10, 13, 2)[pt % 4]})
                    self._se("kira", 20, 0.5)
                return

            if self.phase == "defeat":
                return

            # nonspell / spell: run the pattern + the clock.
            # Pattern names are convention-based: bar 1 nonspell is _ns1,
            # bar 1 spell is _sp1, and so on. The functions are attached below
            # the class as KTGame._ns1, KTGame._sp1, etc. The index is ns_pat /
            # sp_pat (== bar_index in a normal fight, random in endless).
            idx = self.ns_pat if self.phase == "nonspell" else self.sp_pat
            fn = getattr(self, ("_ns%d" if self.phase == "nonspell" else "_sp%d") % (idx + 1))
            fn(self.phase_tick)

            # Spell-5 darkness (sp_pat 4) eases back out whenever its card isn't
            # running -- gated on the pattern so endless can raise it correctly.
            if not (self.phase == "spell" and self.sp_pat == 4):
                self.dark *= 0.94

            self.time_left -= 1
            seconds = self.time_left // 60
            if seconds <= 10 and seconds >= 0 and seconds not in self.warned:
                self.warned.add(seconds)
                self._se("warn2" if seconds <= 5 else "warn", 0, 1.0)
            if self.time_left <= 0:
                if self.phase == "nonspell":
                    self.boss_hp = self.boss_hp_max * 0.5
                    self._start_declare()
                else:
                    self._end_spell(captured=False, timeout=True)

        # ----- entity advancement + collision ----------------------------------

        def _advance_shots(self):
            # Advance player bullets before enemy bullets so a shot that breaks
            # a phase can clear the enemy field before collision checks continue.
            if not self.shots:
                return
            vulnerable = self.phase in ("nonspell", "spell")
            kept = []
            for s in self.shots:
                s["x"] += s["vx"]
                s["y"] += s["vy"]
                if s["y"] < -24.0:
                    continue
                if vulnerable and abs(s["x"] - self.bx) < 40.0 and abs(s["y"] - self.by) < 54.0:
                    self._damage_boss(s["dmg"])
                    self._add_score(KT_SCORE_HIT)
                    self._se("hit_low" if self.boss_hp < self.boss_hp_max * 0.25 else "hit", 5, 1.0)
                    if len(self.sparks) < KT_MAX_SPARKS:
                        self.sparks.append({"x": s["x"], "y": s["y"] + 6.0, "vx": 0.0, "vy": -1.4,
                                            "age": 0, "ttl": 12, "ci": 13})
                    continue
                kept.append(s)
            self.shots = kept

        def _advance_bullets(self):
            # Bullet advancement owns lifetime, movement modifiers, wall bounces,
            # collision, graze, and offscreen culling in one pass. This is the
            # hottest simulation loop in the file; keep new work branch-light.
            #
            # Seer mask, the stopped clock: while tick < stop_until, enemy time
            # simply does not pass. No aging, no movement, no collision -- the
            # field hangs in the air (and knives placed DURING the stop hang
            # with it, still wearing their newborn spawn-flash as the tell).
            # The player, her shots, and the boss all keep moving.
            if self.tick < self.stop_until:
                return
            margin = 70.0
            can_hit = (self.result is None and self.dying_tick is None
                        and self.tick >= self.invuln_until
                        and self.phase in ("nonspell", "spell"))
            px = self.px
            py = self.py
            hit_pad = KT_PLAYER_R
            graze_r = KT_PLAYER_R + KT_GRAZE_PAD
            kept = []
            for b in self.bullets:
                # age is the bullet-local clock. fz ("freeze") delays movement
                # and collision but keeps the bullet in the list so the renderer
                # can show a staged/telegraphed spawn if needed.
                age = b["age"] + 1
                b["age"] = age
                fz = b["fz"]
                if age <= fz:
                    kept.append(b)
                    continue
                ttl = b["ttl"]
                if ttl is not None and age > ttl:
                    continue
                # Interloper mask, stutter-step: a blk bullet moves for half its
                # blink period and HOLDS for the other half (still deadly while
                # held -- it is a lag artifact, not a courtesy). Spawn these
                # about twice as fast as the intended average speed.
                stalled = b["blk"] and (age % b["blk"]) >= (b["blk"] >> 1)
                if stalled:
                    x = b["x"]
                    y = b["y"]
                else:
                    # Discrete re-aim homing (spell 5 et al): snap velocity toward
                    # the player a limited number of times, never continuously.
                    # The speed is preserved with hypot(); only the direction is
                    # replaced, which makes homing readable instead of rubbery.
                    if b["home"] > 0 and age % b["home_t"] == 0:
                        b["home"] -= 1
                        ang = math.atan2(py - b["y"], px - b["x"])
                        spd = math.hypot(b["vx"], b["vy"]) or 1.0
                        b["vx"] = math.cos(ang) * spd
                        b["vy"] = math.sin(ang) * spd
                    b["vx"] += b["ax"]
                    b["vy"] += b["ay"]
                    # Movement is velocity + optional sideways sine sway. The sway
                    # is not stored back into vx, so it wiggles the path without
                    # permanently steering the bullet.
                    x = b["x"] + b["vx"] + (math.sin((age + b["ph"]) * 0.20) * b["sway"] if b["sway"] else 0.0)
                    y = b["y"] + b["vy"]
                    # One wall bounce for mirror/ricochet patterns.
                    if b["bnc"] > 0 and (x < 6.0 or x > KT_W - 6.0):
                        b["bnc"] -= 1
                        b["vx"] = -b["vx"]
                        x = kt_clamp(x, 6.0, KT_W - 6.0)
                    b["x"] = x
                    b["y"] = y
                    # Keep bullets alive briefly outside the visible playfield so
                    # fast diagonals and border-born attacks do not pop on/off at
                    # the exact stage edge.
                    if not (-margin <= x <= KT_W + margin and -margin <= y <= KT_H + margin):
                        continue
                    if b["kind"] in KT_SPIN:
                        # Pointed sprites rotate to face travel direction. Round
                        # ones skip it so they all share one rotation bucket.
                        #
                        # The BUCKET is what gets stored, not the angle: the
                        # renderer only ever wanted the bucket, and computing it
                        # here means the draw loop reads one int out of the dict
                        # instead of doing a divide, a round and a modulo on
                        # every pointed bullet on the stage, every frame. Same
                        # field ("rb") and same reasoning as tsubaki_soul.rpy.
                        b["rb"] = int(round(math.atan2(b["vy"], b["vx"])
                                            * KT_ROT_K + KT_ROT_Q)) % KT_ROT_BUCKETS
                if can_hit:
                    # Cheap broad-phase square before the expensive radius
                    # checks. Almost every bullet is far from the player, so
                    # this avoids hundreds of multiply/add comparisons per tick.
                    dx = x - px
                    if -42.0 < dx < 42.0:
                        dy = y - py
                        if -42.0 < dy < 42.0:
                            # Squared-distance collision avoids sqrt. hr/gr are
                            # sums of the player's radius and the bullet's
                            # pre-scaled radius.
                            d2 = dx * dx + dy * dy
                            hr = hit_pad + b["hr"]
                            # Patience rule: a calm bullet only cuts a MOVING
                            # soul. Held still, it passes straight through --
                            # and falls through to the graze branch below, so
                            # standing your ground inside a ribbon is paid.
                            if d2 <= hr * hr and not (b["calm"] and self.still_ticks > 0):
                                self._register_player_hit()
                                can_hit = False
                                # Only the pellet that clipped you is consumed;
                                # the rest of the pattern stays on the stage.
                                continue
                            elif not b["gz"]:
                                gr = graze_r + b["hr"]
                                if d2 <= gr * gr:
                                    b["gz"] = True
                                    # Each bullet can graze once. The bonus
                                    # grows with total graze count, which rewards
                                    # sustained close play without needing items.
                                    self.graze += 1
                                    self.graze_tick = self.tick
                                    self._add_score(KT_SCORE_GRAZE + 10 * self.graze)
                                    self._se("graze", 4, 1.0)
                                    if len(self.sparks) < KT_MAX_SPARKS:
                                        self.sparks.append({"x": px + dx * 0.5, "y": py + dy * 0.5,
                                                            "vx": dx * 0.08, "vy": dy * 0.08,
                                                            "age": 0, "ttl": 10, "ci": 13})
                kept.append(b)
            self.bullets = kept

        def _update_cancels(self):
            # Bullet cancels are cosmetic stars left by cleared bullets. For
            # KT_CANCEL_HANG ticks they lift and slow (a beat for the eye to see
            # the field come apart), then they are drawn into the soul -- speed
            # ramping, steering eased so they curve in rather than snap -- and
            # vanish on arrival. Nothing here scores or collides: the clear
            # already paid. Sim-side only so it freezes with the pause.
            if not self.cancels:
                return
            px, py = self.px, self.py
            homing = self.phase != "defeat"
            kept = []
            for c in self.cancels:
                a = c["age"] + 1
                c["age"] = a
                if a > KT_CANCEL_TTL:
                    continue
                if a < KT_CANCEL_HANG or not homing:
                    c["vx"] *= 0.90
                    c["vy"] = c["vy"] * 0.90 - 0.03
                else:
                    dx = px - c["x"]
                    dy = py - c["y"]
                    d = math.hypot(dx, dy) or 1.0
                    if d < 12.0:
                        continue
                    spd = min(12.0, 1.5 + (a - KT_CANCEL_HANG) * 0.35)
                    c["vx"] += (dx / d * spd - c["vx"]) * 0.25
                    c["vy"] += (dy / d * spd - c["vy"]) * 0.25
                c["x"] += c["vx"]
                c["y"] += c["vy"]
                kept.append(c)
            self.cancels = kept

        def _advance_sparks(self):
            # Sparks are cosmetic particles with simple drag + gravity. They
            # have no collision and are capped globally so bomb/bar wipes do not
            # turn into unbounded particle storms.
            if not self.sparks:
                return
            kept = []
            for s in self.sparks:
                s["age"] += 1
                if s["age"] > s["ttl"]:
                    continue
                s["x"] += s["vx"]
                s["y"] += s["vy"]
                s["vx"] *= 0.96
                s["vy"] = s["vy"] * 0.96 + 0.05
                kept.append(s)
            self.sparks = kept

        def _finish(self, kind):
            # Copy everything the VN script needs before the screen destroys the
            # KTGame object. The labels after call screen should read kt_last_*,
            # never fields on kt_game.
            self.result = kind
            store.kt_last_score = self.score
            store.kt_last_graze = self.graze
            store.kt_last_captures = self.captures
            store.kt_last_bars = self.bars_broken
            store.kt_last_bar_index = self.bar_index
            store.kt_last_practice = self.practice
            store.kt_last_debug = self.debug
            store.kt_last_deaths = self.deaths
            store.kt_last_endless = self.endless
            store.kt_last_endless_wave = self.endless_wave
            # Practice runs are for learning and debug runs are for devving:
            # no hiscore, no clear flag from either -- and that includes
            # Endless Practice, whose unlimited lives would otherwise walk
            # straight into the Endless records. Real Endless keeps its OWN
            # records (best score + furthest wave), never the clear flag.
            try:
                if self.practice or self.debug:
                    pass
                elif self.endless:
                    if self.score > (persistent.kotomode_endless_hiscore or 0):
                        persistent.kotomode_endless_hiscore = self.score
                    if self.endless_wave > (persistent.kotomode_endless_wave or 0):
                        persistent.kotomode_endless_wave = self.endless_wave
                else:
                    if self.score > (persistent.kotomode_hiscore or 0):
                        persistent.kotomode_hiscore = self.score
                    if kind == "victory":
                        persistent.kotomode_cleared = True
            except Exception:
                pass

        # ----- the master tick --------------------------------------------------

        def step(self):
            # Tick order matters:
            #   1. poll input and maybe spawn player shots/bombs
            #   2. move boss so patterns fire from the updated position
            #   3. run phase/pattern logic
            #   4. advance shots, then bullets, then cosmetics
            #   5. resolve bomb/death/end timers
            # Reordering these changes feel and can affect capture/deathbomb
            # edge cases, even if the code still "works."
            if self.paused or self.result is not None:
                return
            self.tick += 1
            self.phase_tick += 1
            self._poll_input()
            # Patience bookkeeping: input has just been applied, so comparing
            # against last tick's position captures this tick's movement
            # exactly (wall-pushes that produce no displacement count as
            # still, which is the fair reading).
            if self.px == self._still_px and self.py == self._still_py:
                self.still_ticks += 1
            else:
                self.still_ticks = 0
            self._still_px = self.px
            self._still_py = self.py
            self._update_player()
            self._move_boss()
            # Idle glimmer: Kotonoha constantly sheds soft motes while she
            # floats (part of the boss presentation). Deterministic in the
            # tick, throttled, and always leaves spark-cap headroom.
            if (self.phase in ("nonspell", "spell", "declare") and self.tick % 24 == 0
                    and len(self.sparks) < KT_MAX_SPARKS - 12):
                k = self.tick // 24
                self.sparks.append({
                    # 2.39996 is close to the golden angle in radians; using it
                    # keeps repeated motes from lining up in obvious columns.
                    "x": self.bx + math.sin(k * 2.39996) * 34.0,
                    "y": self.by + 14.0 + ((k * 13) % 26),
                    "vx": math.sin(k * 1.7) * 0.22, "vy": -0.62,
                    "age": 0, "ttl": 52,
                    "ci": self.cur_color if (k % 3) else 13,
                })
            self._run_phase()
            self._advance_shots()
            self._advance_bullets()
            self._advance_lasers()
            self._advance_sparks()
            self._update_cancels()
            self._update_bomb()
            self._check_deathbomb_window()
            # Cosmetic layers: atmosphere motes drift every tick, and expired
            # shockwaves are pruned so ring_fx stays tiny.
            self._update_ambient()
            if self.ring_fx:
                self.ring_fx = [r for r in self.ring_fx if self.tick - r["born"] < 46]
            if self.portals:
                self.portals = [p for p in self.portals if self.tick - p["born"] < p["ttl"]]
            if self.over_tick is not None and self.tick >= self.over_tick and self.result is None:
                self._finish("victory" if self.phase == "victory" else "defeat")

# --- PATTERNS ------------------------------------------------------------------
# Spawn primitives + the 16 patterns (8 nonspells, 8 spell cards), defined as
# free functions and attached to KTGame so the class body above stays readable.
# Everything is deterministic in the tick (aim excepted), Id-Mode house style:
# memorizable danmaku, and every card has ONE loud visual signature.
#
# PATTERN AUTHORING NOTES
#   A pattern function receives t, the phase-local tick. Use t for all timing so
#   the card restarts cleanly and remains deterministic.
#
#   Naming convention:
#       _kt_ns1 -> KTGame._ns1 -> bar 1 nonspell
#       _kt_sp1 -> KTGame._sp1 -> bar 1 spell
#       ...
#
#   Spawn through _add/_ring/_fan/_bloom instead of appending to self.bullets by
#   hand. That keeps hit radii, rotation, graze flags, and caps consistent.
#
#   Pick the `kind` for what the card MEANS, not for variety's sake -- every
#   card should have a shape you could name it by (bar 2 is unread ofuda, bar 3
#   and bar 7 are her knife, bar 4 is raindrops, the Seer pours butterflies,
#   Justice fires eyes). The art is drawn FOR the cards now (see the thematic
#   kinds in KT_KIND_HR: drop, camellia, butterfly, tile, blot); that
#   is an invitation to name a card BETTER, not to make every card different. Two
#   shapes that overlap in a pattern should be tellable apart mid-dodge; that
#   is the whole reason ns5's three flower ranks each wear a different one.
#   Two standing exceptions, both deliberate: Mask of You fires plain pellets
#   and daggers because the reader has no shape of their own, and Patience's
#   real bullets are plain orbs so they cannot be mistaken for the calm ones.
#
#   Do not use random.random() in live patterns unless you also deliberately
#   seed it. Current "random-looking" behavior is formulaic, which means a
#   player can learn it and a dev can reproduce bugs by tick/bar.
#
#   If a pattern needs memory, store it in self.scratch. _start_bar() and
#   _start_spell() clear scratch so stale state cannot leak into the next phase.
#
#   A PATTERN NEVER SEES t = 0. step() advances phase_tick before the pattern
#   runs, so the first call is t = 1 -- and an event keyed on `cyc == 0` first
#   fires a whole cycle late. That is harmless for a volley that merely starts
#   at t = N, but not for a cycle START that later beats depend on (a snapshot,
#   a set of gaps): fire it on the first call too, with
#   `if cyc == 0 or <its scratch key> not in self.scratch`. Four cards had this
#   bug until Sep 29 2026 (Rain or Shine, the Prodigy, the Seer, Patience).
init python:
    # Boss movement per bar: (nonspell move, spell move).
    KT_BAR_MOVES = [
        ("sway", "center"),
        ("high", "high"),
        ("sway", "center"),
        ("dart", "high"),
        ("sway", "center"),
        ("sweep", "sweep"),
        ("dart", "center"),
        ("sway", "center"),
    ]

    # Forgiving-by-kind hit radii (scaled by the bullet's scale). Every radius
    # is roughly 55-65% of the sprite's drawn body, Touhou house rule: what you
    # see is bigger than what kills you.
    #
    # The KIND names are the pattern code's vocabulary and did not change when
    # the art did; the sprite behind each one is this mode's own now (see
    # KTStage.KINDS). The radii did not
    # change either -- every new sprite was drawn to land its body where the
    # old one's did, so no card was retuned by the redraw.
    KT_KIND_HR = {
        "orb": 6.0,         # pearl, 20px body -- the workhorse round
        "big": 15.0,        # moon, 46px -- the large slow orb
        "pellet": 4.5,      # grain, 12x21 -- a lens-shaped seed
        "dagger": 4.5,      # quill, 10x24 -- a pen nib, point first
        "star": 6.5,        # facet, 24px -- a cut gem, spins
        "sphere": 6.0,      # bubble, 22px -- the soft twin of the pearl
        "ring": 5.0,        # winged halo, 16px ring -- the wings are faint
        "knife": 5.0,       # her knife, 12x33 -- bars 3, 7 and the finale
        "oval": 4.5,        # petal, 12x21 -- leans with its heading
        "spark": 5.0,       # ember, 14px core under long rays -- twinkles
        "eye": 15.0,        # watching eye, 47px
        # Unread letter, 22x16, stays UPRIGHT (see KT_SPIN). A shade under its
        # drawn body: it inherited bar 2's ring role and the finale quotes it
        # 26 at a time, so a true 6.0 would have retuned a card nobody asked
        # to retune.
        "ofuda": 5.5,
        "rice": 4.0,        # raindrop, 12x19 -- bar 4's rain, points ahead
        # THEMATIC KINDS added with the redraw. Each one replaces an older
        # shape in exactly one card and takes THAT shape's radius, so the
        # swap is visual only:
        "drop": 4.5,        # Rain or Shine's storm (was oval)
        "camellia": 6.0,    # Bloom's whole flowers (was sphere)
        "butterfly": 5.0,   # the Seer's braid (was ring)
        "tile": 5.0,        # Mosaic's mirrored fans (was ring)
        "blot": 6.0,        # Perseverance's ink rain (was sphere)
    }

    # Kinds whose sprite points along its heading. Everything else stays in
    # rotation bucket 0, which is what keeps a round bullet at one texture per
    # (colour, scale) instead of sixty. Keep this set small for that reason --
    # `ofuda` is deliberately NOT in it (a letter hangs upright), and neither
    # are any of the radially symmetric shapes.
    KT_SPIN = frozenset((
        "pellet", "dagger", "knife", "oval", "rice", "drop", "butterfly",
    ))

    # Kinds that TURN on their own clock instead (modern Touhou's stars spin).
    # kind: (buckets in one symmetric turn, ticks per bucket). A five-point
    # shape repeats every 72 degrees, so 12 of the 6-degree rotation buckets
    # are a whole cycle; a four-fold one repeats every 90, so 15. That symmetry
    # is what keeps a spinning star at 12 textures per colour, not 60. The
    # renderer derives the bucket from the bullet's age (plus its ring phase,
    # so a ring of stars does not turn in lockstep); the sim never sees it.
    KT_TWIRL = {
        "star": (12, 2),
        "camellia": (12, 5),
        "spark": (15, 2),
        "tile": (15, 4),
    }

    # --- SPAWN MATERIALIZE -----------------------------------------------------
    # Bullets used to arrive at full size and full opacity on their very first
    # drawn tick, which reads as them popping into existence -- worst on the
    # knives, whose long blade appears all at once and out of nowhere. Now every
    # bullet MATERIALIZES the way modern Touhou's do: over KT_SPAWN_TICKS it
    # fades up through a few alpha steps from a little under size, while a
    # faint ring of its own colour closes down onto it from well outside. (The
    # first version grew each bullet from a pinpoint under a white flare, the
    # older games' read.) It doubles as an honest telegraph -- for those few
    # ticks you can see where a wall is about to be before it is one -- and it
    # is the Seer's time-stop tell: a knife placed while the clock is stopped
    # never ages, so it hangs in its ring until time resumes.
    #
    # It stays cheap because it is expressed entirely in bucketed keys: the fade
    # is KT_SPAWN_STEPS discrete alpha values, the growth reuses the quantized
    # scale key, and the ring is one texture per (colour, tick, body size). So a
    # 40-bullet ring materializing still draws out of a handful of textures.
    # Both ride the frozen (fz) window unchanged, since a bullet's age advances
    # while it is held.
    KT_SPAWN_TICKS = 8            # length of the materialize, in ticks
    KT_SPAWN_STEPS = 3            # discrete alpha steps (index KT_SPAWN_STEPS = opaque)
    KT_SPAWN_ALPHA = (0.16, 0.42, 0.72)

    def _kt_add(self, x, y, vx, vy, kind="orb", ci=13, scale=1.0, sway=0.0,
                ph=0.0, ax=0.0, ay=0.0, ttl=None, fz=0, home=0, home_t=50, bnc=0,
                blk=0, calm=0):
        # Core bullet constructor. Field meanings:
        #   x/y      current stage-local position
        #   vx/vy    velocity applied every tick
        #   kind     sprite + hit-radius family (KT_KIND_HR / KTStage.KINDS)
        #   ci       palette index into KT_PAL
        #   scale    visual scale and hit-radius multiplier
        #   sway/ph  sinusoidal x wobble and its phase
        #   ax/ay    acceleration per tick
        #   ttl      optional lifetime after unfrozen age starts
        #   fz       "freeze" frames: visible lifetime does not move/collide yet
        #   home     remaining discrete re-aim snaps
        #   home_t   ticks between homing snaps
        #   bnc      remaining side-wall bounces
        #   blk      glitch blink period: moves half of it, HOLDS the other half
        #   calm     Patience rule (Undertale light-blue): only cuts a MOVING
        #            soul; passes through (and grazes) a still one. The
        #            renderer ghosts calm bullets while the player is still.
        #   rb       renderer heading, pre-bucketed (see KT_ROT_K)
        #   sq       renderer scale key, pre-quantized to quarters
        #   gz       whether this bullet has already paid graze once
        #   hr       cached hit radius, pre-scaled for collision speed
        # Returns the live bullet dict (or None at the cap) so patterns that
        # need to revisit a bullet later -- the Hunter's flare shells, the
        # Kindness servings -- can keep a handle instead of scanning the list.
        if len(self.bullets) >= KT_MAX_BULLETS:
            return None
        rb = 0
        if kind in KT_SPIN:
            rb = int(round(math.atan2(vy, vx) * KT_ROT_K + KT_ROT_Q)) % KT_ROT_BUCKETS
        b = {
            # speed_mul is 1.0 in every normal run (identical trajectories); in
            # endless it climbs gently with the wave to keep late play tense.
            # Only the initial velocity is scaled, so aim/heading are preserved.
            "x": float(x), "y": float(y),
            "vx": float(vx) * self.speed_mul, "vy": float(vy) * self.speed_mul,
            "kind": kind, "ci": ci, "scale": scale, "sway": sway, "ph": ph,
            "ax": ax, "ay": ay, "ttl": ttl, "fz": fz,
            "home": home, "home_t": home_t, "bnc": bnc, "blk": blk,
            "calm": calm,
            "rb": rb, "age": 0, "gz": False,
            "hr": KT_KIND_HR[kind] * scale,
            # Quantized scale, cached: `scale` is fixed for a bullet's whole
            # life, so rounding it to quarter-steps once here saves the draw
            # loop an int(round(...)) per bullet per frame.
            "sq": max(1, int(round(scale * 4.0))),
        }
        self.bullets.append(b)
        return b
    KTGame._add = _kt_add

    def _kt_aim(self, x, y):
        # Aiming reads the player's CURRENT position. Everything else in the
        # pattern system should be tick-deterministic; aimed shots are the only
        # deliberate player-dependent branch.
        return math.atan2(self.py - y, self.px - x)
    KTGame._aim = _kt_aim

    def _kt_ring(self, x, y, n, spd, offset=0.0, kind="orb", ci=13, scale=1.0,
                fz=0, bnc=0):
        # Evenly spaced FULL radial burst. Rings carry NO authored gaps at all
        # (2026-07 ruling, round two: the old modulo skip left symmetric
        # parked lanes, and the "contiguous door" rework still read as an
        # obvious free exit -- so doors are gone entirely). The dodge is the
        # natural spacing between neighbours, which widens as the ring
        # expands; difficulty comes from density, speed, and layering.
        # A ring that cannot fully spawn is skipped outright: a cap-truncated
        # circle is just a giant accidental gap wearing a uniform.
        if len(self.bullets) + n > KT_MAX_BULLETS:
            return
        for i in range(n):
            a = offset + math.pi * 2.0 * i / float(n)
            self._add(x, y, math.cos(a) * spd, math.sin(a) * spd,
                    kind, ci, scale, ph=i * 0.37, fz=fz, bnc=bnc)
    KTGame._ring = _kt_ring

    def _kt_fan(self, x, y, n, ang, spread, spd, kind="orb", ci=13, scale=1.0, fz_step=0, bnc=0):
        # Symmetric fan centered on ang. fz_step staggers activation outward,
        # useful for readable volleys that do not become instant walls.
        for i in range(n):
            off = (i - (n - 1) / 2.0) * spread
            self._add(x, y, math.cos(ang + off) * spd, math.sin(ang + off) * spd,
                    kind, ci, scale, ph=off * 8.0, fz=i * fz_step, bnc=bnc)
    KTGame._fan = _kt_fan

    def _kt_bloom(self, x, y, spd, ci=1, n=34, tilt=0.0, scale=1.0, petals=4, kind="star"):
        # A petaled "facet" burst: velocity follows a rose curve (r scaled by
        # |cos(petals/2 * theta)|), so the formation blossoms outward as a
        # flower of distinct petals -- one core, many faces. Replaces the old
        # heart burst after the theme rework (the cards are lives, not love).
        # Blooms default to STARS: a facet of a life, one point per face.
        ct = math.cos(tilt)
        st = math.sin(tilt)
        for i in range(n):
            th = math.pi * 2.0 * i / float(n)
            r = 0.35 + 0.65 * abs(math.cos(th * petals * 0.5))
            hx = math.cos(th) * r
            hy = math.sin(th) * r
            rx = hx * ct - hy * st
            ry = hx * st + hy * ct
            self._add(x, y, rx * spd, ry * spd, kind, ci, scale, ph=i * 0.3)
    KTGame._bloom = _kt_bloom

    # --- LASERS ---------------------------------------------------------------
    # A Touhou laser is not a bullet -- it is a SEGMENT with a three-beat life:
    #
    #   1. TELEGRAPH (`warn` ticks)  a hairline. Harmless. This is the promise.
    #   2. FIRE (`live` ticks)       full thickness. Lethal along its length.
    #   3. FADE (KT_LASER_FADE)      thickness collapses back to nothing.
    #
    # The telegraph is the whole reason lasers are fair: the player is told
    # exactly where the wall will be, and for how long they have to not be
    # there. Never spawn one already firing unless the pattern has just moved
    # the player somewhere safe -- `warn=0` is a trap, not a difficulty knob.
    #
    # A laser is drawn from this mode's beam art (kt_lasers.png: a 256x32 body
    # with a hot white core), stretched to length and rotated. Collision is
    # point-to-segment distance, so a sweeping beam is exact rather than
    # approximated by a row of bullets.
    KT_LASER_FADE = 10          # ticks the beam takes to collapse after firing
    KT_LASER_HIT_FRAC = 0.34    # lethal half-width as a fraction of drawn width
    KT_LASER_GRAZE_PAD = 7.0    # extra half-width that counts as a graze
    KT_MAX_LASERS = 28

    def _kt_laser(self, x, y, ang, length=520.0, w=15.0, ci=13, warn=45, live=70,
                spin=0.0, follow=False, calm=0):
        # Fire one beam. `spin` is radians PER TICK -- a sweeping laser is the
        # single most useful thing this primitive does, so it is a first-class
        # field rather than something a pattern re-implements. `follow` re-anchors
        # the origin to the boss every tick (a beam she carries), otherwise the
        # origin is frozen where it was fired.
        # Returns the live dict so a pattern can keep steering it.
        if len(self.lasers) >= KT_MAX_LASERS:
            return None
        L = {
            "x": float(x), "y": float(y), "ang": float(ang),
            "len": float(length), "w": float(w), "ci": ci,
            "born": self.tick, "warn": int(warn), "live": int(live),
            "spin": float(spin), "follow": bool(follow), "calm": calm,
            "gz": False,
        }
        self.lasers.append(L)
        return L
    KTGame._laser = _kt_laser

    def _kt_laser_phase(self, L, tick):
        # (stage, 0..1 through that stage). stage is "warn", "live", "fade" or
        # None once the beam is finished. One place decides this so the renderer
        # and the collider can never disagree about whether a beam is lethal.
        age = tick - L["born"]
        if age < L["warn"]:
            return ("warn", age / float(max(1, L["warn"])))
        age -= L["warn"]
        if age < L["live"]:
            return ("live", age / float(max(1, L["live"])))
        age -= L["live"]
        if age < KT_LASER_FADE:
            return ("fade", age / float(KT_LASER_FADE))
        return (None, 1.0)
    KTGame._laser_phase = _kt_laser_phase

    def _kt_laser_width(self, L, tick):
        # Drawn half-width at this tick. The telegraph is a hairline that swells
        # over its last third, so the fire lands as a snap rather than a fade-in.
        stage, p = self._laser_phase(L, tick)
        if stage == "warn":
            return 0.9 + (L["w"] * 0.5 - 0.9) * kt_clamp((p - 0.66) / 0.34, 0.0, 1.0) * 0.35
        if stage == "live":
            # Tiny throb so a long beam does not read as a static decal.
            return L["w"] * 0.5 * (0.94 + 0.06 * math.sin(tick * 0.5))
        if stage == "fade":
            return L["w"] * 0.5 * (1.0 - p)
        return 0.0
    KTGame._laser_width = _kt_laser_width

    def _kt_advance_lasers(self):
        # Step every beam, then collide the live ones against the player.
        if not self.lasers:
            return
        can_hit = (self.result is None and self.dying_tick is None
                    and self.tick >= self.invuln_until
                    and self.phase in ("nonspell", "spell"))
        px, py = self.px, self.py
        kept = []
        for L in self.lasers:
            stage, _p = self._laser_phase(L, self.tick)
            if stage is None:
                continue
            if L["spin"]:
                L["ang"] += L["spin"]
            if L["follow"]:
                L["x"], L["y"] = self.bx, self.by
            kept.append(L)
            if not can_hit or stage != "live":
                continue
            # Point-to-segment distance, clamped to the segment so the beam
            # stops dead at its tip instead of killing along an infinite line.
            ca = math.cos(L["ang"])
            sa = math.sin(L["ang"])
            rx = px - L["x"]
            ry = py - L["y"]
            proj = kt_clamp(rx * ca + ry * sa, 0.0, L["len"])
            ox = rx - ca * proj
            oy = ry - sa * proj
            d2 = ox * ox + oy * oy
            half = self._laser_width(L, self.tick) * KT_LASER_HIT_FRAC * 2.0
            hr = KT_PLAYER_R + half
            if d2 <= hr * hr and not (L["calm"] and self.still_ticks > 0):
                self._register_player_hit()
                can_hit = False
                continue
            if not L["gz"]:
                gr = hr + KT_LASER_GRAZE_PAD
                if d2 <= gr * gr:
                    L["gz"] = True
                    self.graze += 1
                    self.graze_tick = self.tick
                    self._add_score(KT_SCORE_GRAZE + 10 * self.graze)
                    self._se("graze", 4, 1.0)
        self.lasers = kept
    KTGame._advance_lasers = _kt_advance_lasers

    # ===== BAR 1: first impressions ==========================================

    def _kt_ns1(self, t):
        # Gentle opener: aimed pellet fans + lazy rings of soft white spheres.
        if t >= 40 and t % 50 == 0:
            self._fan(self.bx, self.by, 5, self._aim(self.bx, self.by), 0.16, 2.2, "pellet", 1)
            self._se("fire", 8, 0.9)
        if t % 96 == 0:
            self._ring(self.bx, self.by, 18, 1.6, t * 0.01, "sphere", 13)
            self._se("fire2", 8, 0.8)
    KTGame._ns1 = _kt_ns1

    def _kt_sp1(self, t):
        # FACET SIGN "FIRST IMPRESSIONS" -- petaled blooms of STARS tilting side
        # to side like a face trying on angles for a first meeting, over an
        # aimed drizzle. Every bloom is the same core wearing a different tilt --
        # and the tilt WALKS cast over cast (gap fix: a fixed +/-0.25 parked
        # the between-petal lanes in the same two spots forever).
        if t % 100 == 20:
            cast = t // 100
            tilt = (0.25 + (cast // 2) * 0.61) * (1.0 if cast % 2 == 0 else -1.0)
            self._bloom(self.bx, self.by + 12.0, 2.0,
                        1 if cast % 2 == 0 else 0, 34, tilt, petals=4)
            self._se("gun", 0, 1.0)
        if t % 26 == 13:
            a = self._aim(self.bx, self.by)
            self._add(self.bx, self.by, math.cos(a) * 2.5, math.sin(a) * 2.5, "pellet", 2)
            self._se("fire", 12, 0.7)
    KTGame._sp1 = _kt_sp1

    # ===== BAR 2: the inbox ====================================================

    def _kt_ns2(self, t):
        # Crossing curtains from the top corners; a weave you stream through.
        # Ovals for the curtain threads -- they lean into their heading, so the
        # two streams visibly cross rather than merely overlap.
        if t >= 30 and t % 9 == 0:
            if (t // 9) % 2 == 0:
                self._add(40.0, 26.0, math.cos(0.95) * 2.4, math.sin(0.95) * 2.4,
                        "oval", 6, 1.0, sway=0.4, ph=t * 0.2)
            else:
                self._add(KT_W - 40.0, 26.0, math.cos(math.pi - 0.95) * 2.4,
                        math.sin(math.pi - 0.95) * 2.4, "oval", 2, 1.0, sway=0.4, ph=t * 0.2)
            self._se("fire", 16, 0.6)
        if t % 140 == 70:
            self._ring(self.bx, self.by, 20, 1.8, t * 0.02, "orb", 5)
            self._se("fire2", 10, 0.8)
    KTGame._ns2 = _kt_ns2

    def _kt_sp2(self, t):
        # OVERTIME SIGN "999+ UNREAD" -- the office face. Rows of tasks cascade
        # down the screen; read the moving gap. Accelerating, like a workload
        # that refills faster than it clears. Each task is an OFUDA -- a paper
        # slip with a face printed on it. It is the one shape in the set that
        # is literally a message you have not read yet, and it hangs UPRIGHT
        # (never rotates to heading), so a falling column of them reads as a
        # stack of paper coming down rather than a volley of darts.
        if t % 36 == 0:
            row = t // 36
            gap = (row * 4) % 9
            gap2 = (gap + 4) % 9 if row % 3 == 0 else gap
            colw = KT_W / 9.0
            for col in range(9):
                if col == gap or col == gap2:
                    continue
                self._add(colw * (col + 0.5), -12.0, 0.0, 1.2, "ofuda", 11, 1.0,
                        ay=0.035, fz=(col % 3) * 4)
            self._se("fire2", 10, 0.8)
        if t % 70 == 35:
            self._fan(self.bx, self.by, 3, self._aim(self.bx, self.by), 0.22, 2.3, "orb", 13)
            self._se("fire", 10, 0.8)
    KTGame._sp2 = _kt_sp2

    # ===== BAR 3: the knives come out =========================================

    def _kt_ns3(self, t):
        # Double helix: knife spiral one way, orb spiral the other. Bar 3 is
        # where the blades come out, so its arms carry the heavier sprite.
        if t >= 24 and t % 4 == 0:
            base = t * 0.11
            for arm in (0.0, math.pi):
                a = base + arm
                self._add(self.bx, self.by, math.cos(a) * 2.1, math.sin(a) * 2.1, "knife", 0)
            self._se("fire3", 14, 0.6)
        if t >= 24 and t % 4 == 2:
            base = -t * 0.087 + 0.8
            for arm in (0.0, math.pi):
                a = base + arm
                self._add(self.bx, self.by, math.cos(a) * 1.8, math.sin(a) * 1.8, "orb", 5)
    KTGame._ns3 = _kt_ns3

    def _kt_sp3(self, t):
        # BLADE SIGN "NICE BOAT, CRUEL WAKE" -- braided dagger wakes sweep the
        # stage broadside while a big slow "boat" orb crosses, shedding blades.
        # BUFFED (per TODO -- "way too easy"): wakes come 16% faster with a
        # wider braid and quicker blades, the boat sheds on a tighter clock,
        # and she snipes an aimed dagger fan between waves so the open water
        # can't be camped.
        # FLAIR PASS (the card looked barren next to its siblings): the water
        # tears open FIRST -- a red seam glows at the entry edge for the whole
        # pass, doubling as the broadside telegraph -- the stage stings with
        # each launch, the boat makes a proper splash on entry and churns
        # white foam off its hull the whole crossing.
        # LASER PASS: the tear is now an actual BEAM across the wake line
        # (see _laser), telegraphed then burned off before the knives arrive.
        # This is the one place in the fixed fight that fires a laser, and it
        # went here because the card was flagged "way too easy" twice and was
        # already playing the laser SFX over a wall of knives.
        # SPRITES: the broadside is KNIVES, the biggest blade in the set, and
        # the boat itself is an EYE -- white hull, red heart, dark centre. The
        # blades it sheds stay small daggers so the wake reads as debris.
        # 2026-07 SECOND BUFF PASS (TODO): broadside wakes on a tighter clock
        # with a longer braid and +10% pan speed, the boat crosses ~20% faster
        # and sheds on a faster clock -- the "dagger sources that pan across
        # the screen" no longer amble.
        if t % 112 == 0:
            wave = t // 112
            from_left = (wave % 2 == 0)
            y0 = 110.0 + ((wave * 97) % 400)
            x0 = -20.0 if from_left else KT_W + 20.0
            vx = 3.2 if from_left else -3.2
            self._portal(8.0 if from_left else KT_W - 8.0, y0 - 22.0,
                        0.0 if from_left else math.pi, 96, 0)
            self._flash("#ff4a5c", 10, 24)
            # THE CUT. This card always played the laser SFX for its broadside
            # but never actually drew one; now the tear in the water is a real
            # beam, fired along the wake line the knives are about to occupy.
            # It telegraphs for 34 ticks and only burns for 20, so it is spent
            # BEFORE the braid arrives (the first knife lands at fz=0 and the
            # last at fz=81) -- the laser is the warning shot, not a second
            # wall stacked on the first.
            self._laser(0.0 if from_left else KT_W, y0 - 22.0,
                        0.0 if from_left else math.pi,
                        length=KT_W, w=13.0, ci=0, warn=34, live=20)
            for i in range(27):
                yoff = math.sin(i * 0.55) * 30.0
                self._add(x0, y0 + yoff, vx, 0.0, "knife", 0, 1.0, fz=i * 3)
                self._add(x0, y0 - yoff - 44.0, vx, 0.0, "knife", 12, 1.0, fz=i * 3 + 1)
            self._se("laser", 0, 1.0)
        if t % 64 == 40:
            self._fan(self.bx, self.by, 3, self._aim(self.bx, self.by), 0.14, 2.8, "knife", 13)
            self._se("fire3", 10, 0.8)
        boat_t = t % 300
        if boat_t == 80:
            wave = t // 300
            self.scratch["boat_y"] = 90.0 + ((wave * 131) % 300)
            self.scratch["boat_left"] = (wave % 2 == 0)
            self._se("gun", 0, 1.0)
        if boat_t == 81:
            from_left = self.scratch.get("boat_left", True)
            by0 = self.scratch.get("boat_y", 200.0)
            self._add(-24.0 if from_left else KT_W + 24.0, by0,
                    1.4 if from_left else -1.4, 0.0, "eye", 13, 1.3)
            # Launch splash: a shockwave + spray where the hull hits the water.
            sx0 = kt_clamp(-24.0 if from_left else KT_W + 24.0, 10.0, KT_W - 10.0)
            self._ring_fx(sx0, by0, (1.0, 0.45, 0.55), 300)
            self._spark_burst(sx0, by0, 10, 13, 3.0, 30)
        if boat_t > 81 and boat_t % 8 == 0 and "boat_y" in self.scratch:
            from_left = self.scratch.get("boat_left", True)
            bxx = (-24.0 if from_left else KT_W + 24.0) + (1.4 if from_left else -1.4) * (boat_t - 81)
            if -20.0 < bxx < KT_W + 20.0:
                self._add(bxx, self.scratch.get("boat_y", 200.0) + 10.0, 0.0, 1.5, "dagger", 0)
                # White foam churns off the hull as it sheds.
                if len(self.sparks) < KT_MAX_SPARKS - 2:
                    self.sparks.append({
                        "x": bxx, "y": self.scratch.get("boat_y", 200.0) - 6.0,
                        "vx": (-0.8 if from_left else 0.8), "vy": -0.9,
                        "age": 0, "ttl": 26,
                        "ci": 13 if (boat_t // 8) % 2 else 6,
                    })
    KTGame._sp3 = _kt_sp3

    # ===== BAR 4: the weather turns ============================================

    def _kt_ns4(self, t):
        # Green rain leaning with a slow wind + aimed knife triples. RICE for
        # the rain: a thin grain that points along its heading, so the wind is
        # legible in the drops themselves and not just in where they land. It
        # is narrower than the oval this used to use, which is the whole point
        # -- a raindrop should read as a streak, not a bead.
        wind = math.sin(t * 0.013) * 0.9
        if t % 6 == 0:
            self._add((t * 73) % KT_W, -12.0, wind, 2.5, "rice", 8)
            self._add((t * 137 + 311) % KT_W, -12.0, wind, 2.3, "rice", 7)
            self._se("fire", 20, 0.5)
        if t % 80 == 40:
            self._fan(self.bx, self.by, 3, self._aim(self.bx, self.by), 0.09, 3.0, "knife", 9)
            self._se("fire3", 10, 0.8)
    KTGame._ns4 = _kt_ns4

    def _kt_sp4(self, t):
        # DILIGENCE SIGN "RAIN OR SHINE" -- the errand-runner face: the girl
        # who never once complained about the cold. A whole-screen storm; the
        # rain leans harder and flips with the wind, and lightning daggers
        # strike the column you were standing in (telegraphed by a sparkle
        # warning) -- the schedule always finds you. The storm is RAINDROPS,
        # her nonspell's rain grown to the old oval's size (and its 4.5
        # radius, so the redraw changed nothing about the dodge); the strikes
        # are knives, because they are not rain.
        wind = math.sin(t * 0.016) * 1.5
        if t % 3 == 0:
            # Pseudo-random x via modular arithmetic: deterministic coverage of
            # the width without calling random every three ticks.
            ci = 8 if (t // 3) % 2 == 0 else 9
            self._add((t * 97) % KT_W, -12.0, wind, 2.9, "drop", ci)
            self._se("fire", 26, 0.45)
        cyc = t % 170
        if cyc == 0 or "lx" not in self.scratch:
            # Snapshot the player's x at warning time. The strike uses this
            # saved column 30 ticks later, so the player gets a fair tell.
            # (`or not in scratch`: the pattern never sees t = 0, so the FIRST
            # strike used to fall on the default centre column with no tell.)
            self.scratch["lx"] = self.px
            for i in range(6):
                if len(self.sparks) < KT_MAX_SPARKS:
                    self.sparks.append({"x": self.px, "y": 40.0 + i * 100.0,
                                        "vx": 0.0, "vy": 0.6, "age": 0, "ttl": 30, "ci": 10})
            self._se("charge2", 0, 0.7)
        if cyc == 30:
            lx = self.scratch.get("lx", KT_W * 0.5)
            for i in range(12):
                self._add(lx, -20.0 - i * 34.0, 0.0, 5.4, "knife", 10)
            self._se("laser", 0, 1.0)
    KTGame._sp4 = _kt_sp4

    # ===== BAR 5: lights out ===================================================

    def _kt_ns5(self, t):
        # Triple-layered full flower rings + the first taste of homing orbs.
        # Each rank wears a different shape, so the three layers stay tellable
        # apart once they overlap -- which is the whole dodge here.
        if t % 100 == 0:
            for r, spd in enumerate((1.5, 1.9, 2.3)):
                self._ring(self.bx, self.by, 22, spd, t * 0.013,
                            ("orb", "star", "sphere")[r], 3, fz=r * 6)
            self._se("fire2", 10, 0.9)
        if t % 120 == 60:
            for ox in (-30.0, 30.0):
                self._add(self.bx + ox, self.by, 0.0, 2.1, "sphere", 4, 1.2, home=2, home_t=55)
            self._se("gun", 10, 0.8)
    KTGame._ns5 = _kt_ns5

    def _kt_sp5(self, t):
        # GHOST SIGN "NOBODY'S LOOKING" -- the face nobody notices. The stage
        # goes DARK except a spotlight around you (and her). Sparse bullets,
        # but you can't see far -- and the big violet orbs keep re-finding you
        # in the black, because the one nobody watches sees everything.
        # So the hunters are EYES, literally: the card finally says out loud
        # what it always meant. The rings around them are winged, ghost-pale.
        self.dark = min(0.82, self.dark + 0.01)
        if t % 90 == 0:
            for ox in (-42.0, 42.0):
                self._add(self.bx + ox, self.by, 0.0, 1.7, "eye", 4, 1.0, home=3, home_t=55)
            self._se("gun", 0, 0.9)
        if t % 130 == 65:
            self._ring(self.bx, self.by, 16, 1.45, t * 0.017, "ring", 3)
            self._se("fire2", 10, 0.7)
        if t % 40 == 20:
            a = self._aim(self.bx, self.by)
            for off in (-0.06, 0.06):
                self._add(self.bx, self.by, math.cos(a + off) * 2.3, math.sin(a + off) * 2.3, "pellet", 2)
            self._se("fire", 14, 0.6)
    KTGame._sp5 = _kt_sp5

    # ===== BAR 6: the mosaic ===================================================

    def _kt_ns6(self, t):
        # Ricochet fans: amber spheres that bank once off the side walls (round
        # things bounce -- the sprite should agree), chased by a star volley.
        if t % 64 == 0:
            self._fan(self.bx, self.by, 7, self._aim(self.bx, self.by), 0.117, 2.5, "sphere", 11, bnc=1)
            self._se("fire", 8, 0.9)
        if t % 90 == 45:
            self._fan(self.bx, self.by, 5, self._aim(self.bx, self.by), 0.0, 2.9, "star", 12, fz_step=5)
            self._se("fire3", 10, 0.8)
    KTGame._ns6 = _kt_ns6

    def _kt_sp6(self, t):
        # MOSAIC SIGN "BOTH OF ME ARE REAL" -- a second Kotonoha mirrors her
        # across the stage axis; both fire, both bank shots off the walls, and
        # the two patterns interleave into one crossfire. Not a rival, not a
        # fake: another tile of the mosaic, and it shoots like it means it.
        # Both halves fire the SAME shapes in different colours -- the tell is
        # never which bullet, only which side of the mirror threw it. The fans
        # are TILES: two halves of one mosaic thrown at each other (ring's
        # radius, so the swap is visual only).
        mx = KT_W - self.bx
        if t % 80 == 0:
            # Mirrored boss x: not a separate entity, just the reflected firing
            # origin. The renderer draws the phantom while mirror_on is true.
            down = math.pi * 0.5
            self._fan(self.bx, self.by, 12, down, 0.20, 2.15, "tile", 6)
            self._fan(mx, self.by, 12, down, 0.20, 2.15, "tile", 2)
            self._se("fire2", 0, 0.9)
        if t % 56 == 28:
            self._fan(self.bx, self.by, 3, self._aim(self.bx, self.by), 0.12, 2.75, "knife", 13, bnc=1)
            self._fan(mx, self.by, 3, self._aim(mx, self.by), 0.12, 2.75, "knife", 13, bnc=1)
            self._se("fire3", 8, 0.8)
        if t % 200 == 100:
            self._ring(KT_W * 0.5, self.by + 40.0, 24, 1.7, t * 0.01, "star", 14)
            self._se("gun", 0, 0.8)
    KTGame._sp6 = _kt_sp6

    # ===== BAR 7: the snap =====================================================

    def _kt_ns7(self, t):
        # Pressure: fast aimed knife fans, full oval rings, lone snipes. Every
        # shape here points somewhere, which is the point -- bar 7 is the snap.
        if t >= 24 and t % 30 == 0:
            self._fan(self.bx, self.by, 5, self._aim(self.bx, self.by), 0.125, 3.1, "knife", 0)
            self._se("fire", 10, 0.8)
        if t % 48 == 24:
            self._ring(self.bx, self.by, 20, 2.0, t * 0.021, "oval", 13)
            self._se("fire2", 10, 0.7)
        if t % 90 == 70:
            a = self._aim(self.bx, self.by)
            self._add(self.bx, self.by, math.cos(a) * 4.2, math.sin(a) * 4.2, "knife", 0, 1.3)
            self._se("laser2", 0, 0.9)
    KTGame._ns7 = _kt_ns7

    def _kt_sp7(self, t):
        # SEVERANCE SIGN "THE SCENE EVERYONE REMEMBERS" -- a sawblade of KNIFE
        # spokes centred on Kotonoha. Two fairness valves keep it deathless-able
        # (the first cut was a solid one-way blender with zero windows):
        #   * the rotation is a PENDULUM (integrated triangle wave), so the
        #     wedge you're riding always comes back -- you never get cornered
        #     against a wall with nowhere to orbit;
        #   * each arm skips 2 of every 9 volleys, staggered per spoke, so
        #     door-gaps travel outward along every arm -- when you ARE pinned,
        #     there is always a window sliding toward you.
        if t % 6 == 0:
            v = t // 6
            cyc = t % 900
            # Triangle wave: 0->450->0 over 900 ticks. Multiplying tri by a
            # small scalar produces a sawblade that swings back and forth
            # instead of rotating forever in one direction.
            tri = cyc if cyc < 450 else 900 - cyc
            base = tri * 0.005
            for k in range(6):
                # Skip rule: two volleys out of every nine are missing on each
                # arm, staggered per arm, creating moving doorways.
                if (v + k * 3) % 9 >= 7:
                    continue
                a = base + k * (math.pi * 2.0 / 6.0)
                self._add(self.bx, self.by, math.cos(a) * 2.6, math.sin(a) * 2.6, "knife", 0)
            self._se("fire3", 20, 0.5)
        if t % 64 == 32:
            self._fan(self.bx, self.by, 3, self._aim(self.bx, self.by), 0.17, 2.2, "orb", 13)
            self._se("fire", 10, 0.8)
    KTGame._sp7 = _kt_sp7

    # ===== BAR 8: everything she has ==========================================

    def _kt_ns8(self, t):
        # A remix breather before the finale: small blooms, corner curtains,
        # steady rings. Nothing new -- one last recital of the whole fight, so
        # it quotes bar 1's spheres, bar 2's ovals and the facet stars intact.
        if t % 130 == 30:
            self._bloom(self.bx, self.by + 10.0, 1.8, 1, 20, petals=3)
            self._se("gun", 0, 0.8)
        if t >= 30 and t % 10 == 0:
            if (t // 10) % 2 == 0:
                self._add(30.0, 22.0, math.cos(0.9) * 2.5, math.sin(0.9) * 2.5, "oval", 6)
            else:
                self._add(KT_W - 30.0, 22.0, math.cos(math.pi - 0.9) * 2.5,
                        math.sin(math.pi - 0.9) * 2.5, "oval", 2)
        if t % 100 == 50:
            self._ring(self.bx, self.by, 18, 1.85, t * 0.015, "sphere", 13)
            self._se("fire2", 10, 0.7)
    KTGame._ns8 = _kt_ns8

    def _kt_sp8(self, t):
        # PERSEVERANCE "EVERY SELF BUT HER OWN" -- the finale, in three swells
        # (every 25 seconds another life joins in): five-petal facet blooms +
        # border rings that collapse through the centre; then counter-rotating
        # dagger helixes (the blade that remembers); then violet rain and
        # snipes. Perseverance as blessing AND curse: she cannot stop, so
        # survive the whole clock unbroken and the timeout itself counts as
        # the capture.
        # Each segment is 1500 ticks = 25 seconds at 60Hz.
        # SPRITES: every self she has worn shows up here -- facet stars, bar
        # 2's unread OFUDA closing in off the border, both blades of bar 3 and
        # bar 7, and bar 4's RICE rain. That inventory IS the card's argument,
        # so if you re-dress one of those bars, re-dress its quote here too or
        # the finale stops quoting anything.
        seg = t // 1500
        if t % 110 == 20:
            cast = t // 110
            # Walking tilt (gap fix): the five-petal lanes never park.
            tilt = (0.35 + (cast // 2) * 0.53) * (1.0 if cast % 2 == 0 else -1.0)
            self._bloom(self.bx, self.by + 12.0, 1.7, 1 if cast % 2 == 0 else 0, 30,
                        tilt, petals=5)
            self._se("gun", 0, 0.9)
        if t % 90 == 45:
            # Border collapse: a ring born ON the stage edge, falling inward.
            # per is the perimeter length of the stage rectangle. d walks each
            # bullet around that perimeter; the if/elif chain converts the
            # 1D perimeter coordinate back into an edge x/y point.
            n = 26
            per = 2.0 * (KT_W + KT_H)
            ccx = KT_W * 0.5
            ccy = KT_H * 0.45
            for i in range(n):
                d = (per * i / float(n) + t * 3.1) % per
                if d < KT_W:
                    ex, ey = d, -8.0
                elif d < KT_W + KT_H:
                    ex, ey = KT_W + 8.0, d - KT_W
                elif d < 2 * KT_W + KT_H:
                    ex, ey = d - KT_W - KT_H, KT_H + 8.0
                else:
                    ex, ey = -8.0, d - 2 * KT_W - KT_H
                # Aim every edge-born bullet at the same off-center point so
                # the ring collapses through the middle instead of simply
                # falling straight inward from each edge.
                a = math.atan2(ccy - ey, ccx - ex)
                self._add(ex, ey, math.cos(a) * 1.5, math.sin(a) * 1.5, "ofuda", 0)
            self._se("fire3", 0, 0.8)
        if seg >= 1 and t % 6 == 0:
            base = t * 0.09
            self._add(self.bx, self.by, math.cos(base) * 2.2, math.sin(base) * 2.2, "knife", 0)
            # Counter-helix: negative angular velocity and non-1.0 multiplier
            # keep the white dagger stream from perfectly retracing the red one
            # -- and the two arms carry different blades, so the braid reads.
            a2 = -base * 1.13 + 1.7
            self._add(self.bx, self.by, math.cos(a2) * 2.2, math.sin(a2) * 2.2, "dagger", 13)
            self._se("fire", 24, 0.5)
        if seg >= 2:
            if t % 5 == 0:
                self._add((t * 89) % KT_W, -12.0, 0.0, 3.0, "rice", 4, 1.0, sway=0.8, ph=t * 0.1)
            if t % 70 == 35:
                a = self._aim(self.bx, self.by)
                self._add(self.bx, self.by, math.cos(a) * 4.0, math.sin(a) * 4.0, "knife", 2, 1.3)
                self._se("laser2", 0, 0.9)
    KTGame._sp8 = _kt_sp8

    # ===== ENDLESS EXCLUSIVES ==================================================
    # Everything below only ever rolls in Endless Mode: four extra nonspells
    # (_ns9.._ns12), the eight MASK cards (_sp9.._sp16), and the six SOUL
    # cards (_sp17.._sp22, further down). The masks are the other people in
    # her life -- Endless is Kotonoha wearing everyone else's face, one wave
    # at a time. House rules still apply: deterministic in t, spawn through
    # the helpers, one loud signature per card.

    def _kt_portal(self, x, y, ang, ttl, ci=3):
        # A Seer "gap": a glowing border seam the renderer draws (and bullets
        # pour from). ang is the EMISSION direction; the seam itself is drawn
        # perpendicular to it, Yakumo-style.
        self.portals.append({"x": x, "y": y, "ang": ang, "born": self.tick,
                            "ttl": ttl, "ci": ci})
        if len(self.portals) > 6:
            del self.portals[0]
    KTGame._portal = _kt_portal

    def _kt_ns9(self, t):
        # ENDLESS NONSPELL: twin lattice -- both corner curtains at once with a
        # slowly breathing crossing angle, over a gapped drift ring. BUFFED
        # (TODO: "I can literally just chill at the bottom"): the streams
        # diverge below their crossing point, leaving a safe V at the floor --
        # so she now snipes an aimed dagger pair into whoever parks there, the
        # curtains come a beat faster, and the ring is denser.
        if t >= 24 and t % 8 == 0:
            k = t // 8
            lean = math.sin(k * 0.35) * 0.18
            for x0, aa in ((36.0, 0.85 + lean), (KT_W - 36.0, math.pi - 0.85 - lean)):
                self._add(x0, 22.0, math.cos(aa) * 2.5, math.sin(aa) * 2.5, "oval", 5)
            self._se("fire", 18, 0.5)
        if t % 100 == 50:
            self._ring(self.bx, self.by, 20, 1.8, t * 0.02, "star", 6)
            self._se("fire2", 8, 0.7)
        if t % 88 == 66:
            a = self._aim(self.bx, self.by)
            for off in (-0.05, 0.05):
                self._add(self.bx, self.by, math.cos(a + off) * 3.3,
                        math.sin(a + off) * 3.3, "knife", 5)
            self._se("fire3", 10, 0.7)
    KTGame._ns9 = _kt_ns9

    def _kt_ns10(self, t):
        # ENDLESS NONSPELL: meteor drift -- big slow shells cross the field
        # shedding a wake of rising-then-falling rain. Shed positions are
        # recomputed from each shell's launch parameters, so no bullet scans.
        # BUFFED (TODO): shells and shed rain both come on a tighter clock.
        # The shells are EYES and their wake is SPARKS: burning things falling,
        # throwing embers that hang before they drop.
        ms = self.scratch.setdefault("meteors", [])
        if t % 72 == 0:
            k = t // 72
            x = 60.0 + ((k * 211) % (KT_W - 120))
            vx = math.sin(k * 1.9) * 0.4
            self._add(x, -20.0, vx, 1.35, "eye", 12)
            ms.append((t, x, vx, 1.35))
            if len(ms) > 6:
                del ms[0]
            self._se("gun", 0, 0.7)
        if t % 12 == 8:
            for t0, x0, vx0, vy0 in ms:
                dtk = t - t0
                my = -20.0 + vy0 * dtk
                if 0.0 < my < KT_H - 40.0:
                    self._add(x0 + vx0 * dtk, my, -vx0 * 0.6, -0.15, "spark", 12,
                            1.0, ay=0.028)
            self._se("fire", 24, 0.4)
    KTGame._ns10 = _kt_ns10

    def _kt_ns11(self, t):
        # ENDLESS NONSPELL: pincer spirals -- flank emitters sweep fans into
        # the field from both sides while she snipes from above. BUFFED
        # (TODO: "I can literally just chill at the bottom"): a second, LOWER
        # emitter pair scissors the floor band, the upper pair fires a shade
        # faster, and the snipe fan is wider.
        if t >= 20 and t % 4 == 0:
            aa = math.sin(t * 0.045) * 0.9
            self._add(24.0, 190.0, math.cos(aa) * 2.1, math.sin(aa) * 1.5 + 0.7, "sphere", 2)
            self._add(KT_W - 24.0, 190.0, -math.cos(aa) * 2.1, math.sin(aa) * 1.5 + 0.7, "sphere", 4)
            self._se("fire", 22, 0.45)
        if t >= 20 and t % 8 == 2:
            # The floor pair wears rings, not spheres: the scissor that closes
            # under you should never be mistaken for the wash coming over it.
            ab = math.sin(t * 0.038 + 2.1) * 0.7
            self._add(24.0, 470.0, math.cos(ab) * 2.0, math.sin(ab) * 1.1 - 0.25, "ring", 3)
            self._add(KT_W - 24.0, 470.0, -math.cos(ab) * 2.0, math.sin(ab) * 1.1 - 0.25, "ring", 3)
        if t % 66 == 33:
            self._fan(self.bx, self.by, 5, self._aim(self.bx, self.by), 0.13, 2.8, "knife", 13)
            self._se("fire3", 10, 0.7)
    KTGame._ns11 = _kt_ns11

    def _kt_ns12(self, t):
        # ENDLESS NONSPELL: scatter snipe -- lone hard daggers from shifting
        # shoulder offsets on a fast clock, threaded through full rings.
        if t >= 20 and t % 22 == 0:
            k = t // 22
            ox = math.sin(k * 1.3) * 120.0
            a = self._aim(self.bx + ox, self.by)
            self._add(self.bx + ox, self.by, math.cos(a) * 3.6, math.sin(a) * 3.6, "knife", 14)
            self._se("fire3", 10, 0.6)
        if t % 66 == 33:
            self._ring(self.bx, self.by, 18, 2.1, t * 0.017, "oval", 13)
            self._se("fire2", 8, 0.7)
    KTGame._ns12 = _kt_ns12

    def _kt_sp9(self, t):
        # MASK OF THE BLOOM "Camellias Fall Whole" -- Tsubaki. A petal storm
        # that never hurries; every four seconds one whole flower drops
        # unscattered. (Camellias fall intact. That is why they are the death
        # flower.) The storm is OVALS -- an ellipse turning as it falls is a
        # petal -- and the whole flowers that follow are CAMELLIAS, heads
        # intact (sphere's radius, so they dodge exactly as the spheres did).
        if t % 7 == 0:
            self._add((t * 113) % KT_W, -12.0, 0.0, 1.6,
                    "oval", 1 if (t // 7) % 3 else 0, 1.0, sway=1.3, ph=t * 0.17)
            self._se("fire", 30, 0.4)
        if t % 120 == 30:
            cast = t // 120
            # Walking tilt (gap fix): the petal lanes drift cast over cast.
            tilt = (0.3 + (cast // 2) * 0.57) * (1.0 if cast % 2 else -1.0)
            self._bloom(self.bx, self.by + 10.0, 1.9, 0 if cast % 2 else 1, 30,
                        tilt, petals=5)
            self._se("gun", 0, 0.9)
        if t % 240 == 150:
            self._bloom(self.bx, self.by + 16.0, 1.05, 0, 26, (t // 240) * 0.5, petals=6)
            for i in range(6):
                a = math.pi * 2.0 * i / 6.0 + 0.3
                self._add(self.bx + math.cos(a) * 26.0, self.by + 16.0 + math.sin(a) * 26.0,
                        math.cos(a) * 0.5, math.sin(a) * 0.5 + 1.1, "camellia", 0, 1.3)
            self._se("charge", 0, 0.6)
    KTGame._sp9 = _kt_sp9

    def _kt_sp10(self, t):
        # MASK OF THE HUNTER "One-Girl Grand Finale" -- Kotonoha, undisguised:
        # the Void Hunter (cs_kotonoha_02), running her own hunt AND her own
        # send-off. Same move it always was -- shells arc up off her hands and
        # burst into rings wherever gravity carried them -- but read as
        # hunting flares flushing the sky, violet through and through, with a
        # three-ring encore every five seconds. One girl, one finale.
        # (Formerly "Mask of the Ringmaster": the Seer card is Matsuda's now.)
        # SPARKS are this card's signature: the shells go up as eyes and come
        # apart into a ring of flare-burn and a slower ring of embers.
        fw = self.scratch.setdefault("fw", [])
        if t % 100 == 10:
            k = t // 100
            for j in (-1.0, 1.0):
                sh = self._add(self.bx, self.by, j * (0.9 + 0.3 * (k % 3)), -2.6,
                            "eye", 3, 1.0, ay=0.05)
                if sh is not None:
                    fw.append((t + 64, sh))
            self._se("gun", 0, 1.0)
        while fw and fw[0][0] <= t:
            _, sh = fw.pop(0)
            sx, sy = sh["x"], sh["y"]
            # Flares that drifted out of the frame just don't burst -- they
            # fall back through as duds. Even the hunter wastes a shot.
            if -20.0 < sx < KT_W + 20.0 and -60.0 < sy < KT_H:
                sh["ttl"] = sh["age"]        # the flare is consumed by its burst
                self._ring(sx, sy, 16, 1.9, sx * 0.013, "spark", 4)
                self._ring(sx, sy, 8, 1.1, 0.3, "sphere", 3)
                self._spark_burst(sx, sy, 10, 3, 3.0, 30)
                self._se("break_sm", 0, 0.9)
        if t % 48 == 24:
            self._fan(self.bx, self.by, 2, self._aim(self.bx, self.by), 0.24, 2.7, "knife", 2)
            self._se("fire3", 10, 0.7)
        enc = t % 300
        if enc in (200, 212, 224):
            self._ring(self.bx, self.by, 20, 1.6 + (enc - 200) * 0.03,
                    t * 0.01 + enc, "spark", 2 if enc == 212 else 3)
            self._se("fire2", 0, 0.9)
    KTGame._sp10 = _kt_sp10

    def _kt_sp11(self, t):
        # MASK OF THE KEEPER "Dinner Gets Cold" -- Mom. Nothing here is fast.
        # Everything here arrives anyway.
        #
        # NERFED from the first cut, which was literally unwinnable rather
        # than hard: gapless 22-orb rings converged on the player from ALL
        # borders every 110t while 1.25-speed bullets lingered 8+ seconds, so
        # the field saturated into a noose with no exit. The surviving fix is
        # count + clocks, NOT doors (no-authored-gaps ruling): 16 sparse orbs
        # on a slow 150t clock, crossing quicker (less lingering = less
        # saturation), all aimed at your SNAPSHOT position -- the dodge is
        # repositioning before the noose closes, and the wide natural spacing
        # of 16 points around the whole perimeter. The walls keep one lane;
        # the fans breathe longer. Nothing sharp in the whole card -- soft
        # spheres closing in, and the wall arriving as a row of set plates.
        if t % 150 == 0:
            n = 16
            per = 2.0 * (KT_W + KT_H)
            tx, ty = self.px, self.py
            for i in range(n):
                d = (per * i / float(n) + t * 1.7) % per
                if d < KT_W:
                    ex, ey = d, -8.0
                elif d < KT_W + KT_H:
                    ex, ey = KT_W + 8.0, d - KT_W
                elif d < 2 * KT_W + KT_H:
                    ex, ey = d - KT_W - KT_H, KT_H + 8.0
                else:
                    ex, ey = -8.0, d - 2 * KT_W - KT_H
                a = math.atan2(ty - ey, tx - ex)
                self._add(ex, ey, math.cos(a) * 1.4, math.sin(a) * 1.4, "sphere", 10)
            self._se("fire2", 0, 0.8)
        if t % 130 == 55:
            row = t // 130
            gap = (row * 5) % 11
            colw = KT_W / 11.0
            for c in range(11):
                if c == gap or c == (gap + 1) % 11 or c == (gap + 2) % 11:
                    continue
                self._add(colw * (c + 0.5), -10.0, 0.0, 1.3, "ring", 11, 1.0,
                        sway=0.3, ph=c * 0.7)
            self._se("fire", 12, 0.6)
        if t % 90 == 20:
            self._fan(self.bx, self.by, 4, self._aim(self.bx, self.by), 0.32, 1.5, "sphere", 10)
            self._se("fire2", 16, 0.5)
    KTGame._sp11 = _kt_sp11

    def _kt_sp12(self, t):
        # MASK OF THE PRODIGY "A Room of Closing Windows" -- Hina. Pop-ups: a
        # pellet window-frame opens somewhere (frozen, harmless, readable),
        # then snaps shut through its own centre. Do not be inside the window
        # when it closes. A cursor keeps re-finding you; spam trickles from
        # the top of the feed the whole time. Colour motif: "impossible
        # colors" -- the frames strobe magenta/violet, the feed runs stygian
        # blue (the darkest blue a screen can lie about). The frames stay
        # PELLETS: they have to read as a drawn rectangle, and only a small
        # squared-off sprite does. Around them the feed pops in as rings and
        # the cursor is a star that keeps re-finding you.
        cyc = t % 130
        # `or not in scratch`: the pattern never sees t = 0, so the first
        # window used to open a whole cycle late -- while its "snaps shut" cue
        # at cyc 62 still played, over an empty stage.
        if cyc == 0 or "win" not in self.scratch:
            self.scratch["win"] = True
            k = t // 130
            wx = (110.0, KT_W * 0.5, KT_W - 110.0)[k % 3]
            wy = 170.0 + ((k * 83) % 3) * 140.0
            hw, hh = 80.0, 58.0
            pts = []
            for i in range(7):
                u = i / 6.0
                pts.append((wx - hw + 2.0 * hw * u, wy - hh))
                pts.append((wx - hw + 2.0 * hw * u, wy + hh))
            for i in range(1, 4):
                u = i / 4.0
                pts.append((wx - hw, wy - hh + 2.0 * hh * u))
                pts.append((wx + hw, wy - hh + 2.0 * hh * u))
            for pi, (bxp, byp) in enumerate(pts):
                aa = math.atan2(wy - byp, wx - bxp)
                self._add(bxp, byp, math.cos(aa) * 2.2, math.sin(aa) * 2.2,
                        "pellet", 2 if pi % 2 == 0 else 4, 1.0, fz=62)
            self._se("ok", 0, 0.7)
        if cyc == 62:
            self._se("fire3", 0, 0.8)      # the window snaps shut
        if t % 80 == 40:
            self._add(self.bx, self.by, 0.0, 1.8, "star", 2, 1.2, home=2, home_t=50)
            self._se("gun", 8, 0.7)
        if t % 12 == 6:
            self._add((t * 61) % KT_W, -12.0, 0.0, 2.0, "ring", 5)
            self._se("fire", 30, 0.35)
    KTGame._sp12 = _kt_sp12

    def _kt_sp13(self, t):
        # MASK OF THE ABANDONER "Reckless Abandon" -- Sam. No rhythm you can
        # set a metronome to: lopsided double-beats in pseudo-random directions,
        # rings thrown from wherever the dash left her, mines shed in her wake,
        # everything accelerating somewhere else. The chaos is the pattern --
        # and so is the sprite roulette: this card is the only one that never
        # commits to a single shape.
        v = t % 14
        if v == 0 or v == 5:
            k = t // 7
            a = ((k * 197) % 628) / 100.0
            spr = 0.22 + ((k * 43) % 5) * 0.05
            spd = 2.0 + ((k * 61) % 7) * 0.18
            for off in (-spr, 0.0, spr):
                # Even the SPRITE is unreliable: each double-beat picks a
                # different shape off the same pseudo-random key. All three sit
                # within half a pixel of hit radius, so the roulette is pure
                # look -- reading a shape here must never mean reading a size.
                self._add(self.bx, self.by, math.cos(a + off) * spd, math.sin(a + off) * spd,
                        ("pellet", "spark", "oval")[k % 3], 12 if k % 3 else 11, 1.0,
                        ax=math.cos(a + off) * 0.014, ay=math.sin(a + off) * 0.014)
            self._se("fire3", 10, 0.6)
        if t % 74 == 30:
            for i in range(18):
                aa = math.pi * 2.0 * i / 18.0 + t * 0.01
                sp2 = 1.5 + ((i * 7) % 5) * 0.28
                self._add(self.bx, self.by, math.cos(aa) * sp2, math.sin(aa) * sp2, "star", 12)
            self._se("gun", 0, 0.9)
        if t % 160 < 36 and t % 3 == 0:
            self._add(self.bx, self.by + 8.0, 0.0, 0.55, "spark", 11, 1.15, fz=46)
            self._se("kira", 12, 0.4)
        if t % 130 == 90:
            a2 = self._aim(self.bx, self.by)
            self._add(self.bx, self.by, math.cos(a2) * 4.6, math.sin(a2) * 4.6, "knife", 12, 1.2)
            self._se("laser", 0, 0.8)
    KTGame._sp13 = _kt_sp13

    def _kt_sp14(self, t):
        # MASK OF THE INTERLOPER "Delete As Appropriate" -- the green one. The
        # bullets have editing artifacts: they stutter-step (move, hold, move;
        # the blk field), she BLINKS across the stage instead of flying, and
        # every so often a whole line of the sky gets crossed out.
        if t % 44 == 0:
            shf = (t // 44) * 0.37
            for i in range(14):
                a = math.pi * 2.0 * i / 14.0 + shf
                self._add(self.bx, self.by, math.cos(a) * 3.2, math.sin(a) * 3.2,
                        "star", 8, blk=24)
            self._se("fire2", 0, 0.8)
        if t % 58 == 29:
            a = self._aim(self.bx, self.by)
            # Every third volley, the emerald slips: one pellet each of blue,
            # violet, and pink -- a quiet nod to three girls who are not in
            # this game. Blink and you miss them, which is rather the point.
            nod = ((t // 58) % 3 == 0)
            for oi, off in enumerate((-0.14, 0.0, 0.14)):
                self._add(self.bx, self.by, math.cos(a + off) * 3.6, math.sin(a + off) * 3.6,
                        "pellet", (5, 4, 1)[oi] if nod else 8, blk=16)
            self._se("fire3", 8, 0.7)
        if t % 176 == 88:
            # The scanline: daggers all spawn AT the lip with staggered freeze
            # frames (spawning them further out would trip the offscreen cull),
            # so they emerge single-file like a line being struck through.
            y0 = 120.0 + (((t // 176) * 167) % 380)
            for i in range(12):
                self._add(-14.0, y0, 3.8, 0.0, "knife", 8, fz=i * 8)
            self._flash("#6cff7d", 8, 26)
            self._se("laser2", 0, 0.8)
    KTGame._sp14 = _kt_sp14

    def _kt_sp15(self, t):
        # MASK OF YOU "The Reader, Read Back" -- yours. A phantom of YOUR ship
        # mirrors your position through the stage centre and fires your own
        # loadout at you: the triple spread, the focused twin needles, even a
        # bomb-ring echo. Fighting your reflection means standing still is
        # aiming. The 130px guard keeps the mirror from ever firing point-blank
        # when you hover near the centre of the stage. Colour motif: gray and
        # white -- the reader has no colour of their own. It has no SHAPE of
        # its own either: the phantom fires the same plain pellets and daggers
        # your ship does, the one card in Endless that borrows nothing from the
        # sheet but the grey ring it echoes your bomb with.
        rx = KT_W - self.px
        ry = KT_H - self.py
        dx = self.px - rx
        dy = self.py - ry
        far = (dx * dx + dy * dy) > 16900.0
        if far and t % 11 == 0:
            a = math.atan2(dy, dx)
            for off in (-0.13, 0.0, 0.13):
                self._add(rx, ry, math.cos(a + off) * 3.0, math.sin(a + off) * 3.0, "pellet", 14)
            self._se("fire", 14, 0.5)
        if far and t % 90 == 30:
            a2 = math.atan2(dy, dx)
            nx = math.cos(a2 + math.pi * 0.5) * 8.0
            ny = math.sin(a2 + math.pi * 0.5) * 8.0
            for s2 in (-1.0, 1.0):
                self._add(rx + nx * s2, ry + ny * s2,
                        math.cos(a2) * 4.2, math.sin(a2) * 4.2, "dagger", 13)
            self._se("fire3", 8, 0.7)
        if t % 150 == 75:
            self._ring(rx if far else self.bx, ry if far else self.by, 20, 1.35,
                    t * 0.01, "ring", 14)
            self._se("bomb2", 0, 0.6)
        if t % 64 == 32:
            self._ring(self.bx, self.by, 10, 1.6, t * 0.02, "orb", 13)
            self._se("fire2", 12, 0.5)
    KTGame._sp15 = _kt_sp15

    def _kt_sp16(self, t):
        # MASK OF THE SEER "Every Border Is a Door" -- MATSUDA's mask now (her
        # story is "Ontological Seer"; the one who watches from the booth and
        # treats every border, fourth wall included, as a door). Same move it
        # always was: gaps tear open along the borders and pour braided
        # butterflies while double flowers turn underneath. Then the watch
        # clicks -- TIME STOPS -- a knife lattice assembles around your frozen
        # moment (each blade aimed at where you WERE when it appeared), and
        # the world resumes all at once. Homing eyes follow through the gaps
        # for good measure. 460-tick cycle. Colour motif: bright red + aqua,
        # with chimerical glints across the spectrum (the second butterfly of
        # every braid cycles amber/magenta/green/violet).
        # This card finally gets to mean its own comments: the braid pours
        # BUTTERFLIES through the gaps (ring's radius -- it poured winged rings
        # before the redraw), the lattice is knives, and what comes through the
        # gaps at the end are EYES.
        cyc = t % 460
        gaps = self.scratch.get("gaps")
        # `or gaps is None`: the pattern never sees t = 0, so without it the
        # first cycle opened no gaps at all -- no butterflies, and no eyes
        # through the gaps at cyc 420 -- for the card's first 7.7 seconds.
        if cyc == 0 or gaps is None:
            k = t // 460
            gaps = []
            for i in range(4):
                r1 = (k * 61 + i * 97) % 3
                u = ((k * 89 + i * 173) % 100) / 100.0
                if r1 == 0:
                    gx, gy, ga = 50.0 + u * (KT_W - 100.0), 30.0, math.pi * 0.5
                elif r1 == 1:
                    gx, gy, ga = 28.0, 60.0 + u * 240.0, 0.35
                else:
                    gx, gy, ga = KT_W - 28.0, 60.0 + u * 240.0, math.pi - 0.35
                gaps.append((gx, gy, ga))
                self._portal(gx, gy, ga, 300, 0 if i % 2 == 0 else 6)
            self.scratch["gaps"] = gaps
            self._se("charge", 0, 0.8)
        if gaps and cyc < 300 and cyc % 9 == 0:
            gi = (cyc // 9) % len(gaps)
            gx, gy, ga = gaps[gi]
            wob = math.sin(cyc * 0.11 + gi) * 0.5
            self._add(gx, gy, math.cos(ga + wob) * 1.9, math.sin(ga + wob) * 1.9,
                    "butterfly", 0 if gi % 2 == 0 else 6, 1.0, sway=0.7, ph=cyc * 0.3)
            self._add(gx, gy, math.cos(ga - wob) * 1.6, math.sin(ga - wob) * 1.6,
                    "butterfly", (11, 2, 8, 4)[(cyc // 9) % 4], 1.0, sway=0.5, ph=cyc * 0.2)
            self._se("fire", 18, 0.5)
        if cyc in (90, 210):
            self._ring(self.bx, self.by, 24, 1.55, t * 0.011, "star", 0)
            self._ring(self.bx, self.by, 24, 1.15, -t * 0.011, "star", 6)
            self._se("fire2", 0, 0.9)
        if cyc == 300:
            # The stopped clock: 96 ticks where enemy time does not pass.
            self.stop_until = self.tick + 96
            self._flash("#c8dcff", 20, 80)
            self._se("charge2", 0, 1.0)
        if 306 <= cyc < 378 and cyc % 6 == 0:
            i = (cyc - 306) // 6
            a = i * (math.pi / 6.0) + (t // 460) * 0.35
            d = 120.0 + 40.0 * (i % 3)
            kx = self.px + math.cos(a) * d
            ky = self.py + math.sin(a) * d
            if 10.0 < kx < KT_W - 10.0 and 10.0 < ky < KT_H - 10.0:
                aim = math.atan2(self.py - ky, self.px - kx)
                # BUFFED (TODO): the stopped-clock blades leave faster --
                # 2.9 -> 4.7 -- so the resume moment actually demands the
                # repositioning the freeze telegraphs.
                self._add(kx, ky, math.cos(aim) * 4.7, math.sin(aim) * 4.7, "knife", 13)
                self._se("kira", 5, 0.5)
        if cyc == 396:
            # ...and the world resumes all at once (stop_until just lapsed).
            self._flash("#f5faff", 12, 60)
            self._se("laser2", 0, 0.9)
        if cyc == 420 and gaps:
            for gi in (0, 2):
                gx, gy, ga = gaps[gi % len(gaps)]
                self._add(gx, gy, math.cos(ga) * 1.6, math.sin(ga) * 1.6,
                        "eye", 0, 1.0, home=2, home_t=48)
            self._se("gun", 0, 0.9)
    KTGame._sp16 = _kt_sp16

    # ===== THE SIX SOULS =======================================================
    # Endless-only spell cards _sp17.._sp22: quiet callbacks to the six fallen
    # souls (the mode's Undertale/Deltarune debt, acknowledged in the cellar
    # where the cut content lives). Each card is titled after its soul's item,
    # wears its soul's colour, and plays its soul's LESSON as a mechanic:
    # patience waits, bravery keeps moving, integrity respects the arc,
    # perseverance stays on the lines, kindness overfeeds, justice counts
    # its shots. House rules still apply: deterministic in t, spawn through
    # the helpers, one loud signature per card -- and NO authored doors.

    def _kt_sp17(self, t):
        # PATIENCE (aqua) -- "Faded Ribbon". Knives for the trap that assembles
        # around you and ovals for the ribbons themselves; both ghost out while
        # you hold still, which is the card. 2026-07-11 REWORK. Two density
        # nerfs still left this the hardest soul card by a mile, and none of
        # that difficulty played the LESSON -- so the card now runs the
        # soul's own rule instead of raw threading. The ribbons are CALM
        # bullets (Undertale light blue): they only cut a MOVING soul. Held
        # still, they pass straight through you -- ghosting visibly, paying
        # graze -- so the trap that assembles around your snapshot is
        # survived by standing exactly where it aimed and trusting it.
        # Camping forever is broken by a handful of REAL amber bullets fired
        # into the lull, timed to arrive during the NEXT cycle's stillness:
        # one honest step, taken in the seam between ribbon washes, and the
        # next snapshot re-arms around wherever you stopped. Density is
        # spectacle now; the difficulty is discipline. House rules hold:
        # full rings, no authored doors -- the opening is temporal (be
        # still), not spatial.
        cyc = t % 288
        # `or not in scratch`: the pattern never sees t = 0, so the first trap
        # used to assemble around the stage-centre default instead of you.
        if cyc == 0 or "rx" not in self.scratch:
            self.scratch["rx"] = self.px
            self.scratch["ry"] = kt_clamp(self.py, 120.0, KT_H - 60.0)
            self._se("charge", 0, 0.7)
        if cyc == 20:
            rx = self.scratch.get("rx", KT_W * 0.5)
            ry = self.scratch.get("ry", KT_H * 0.6)
            shf = t // 288
            for rank in range(3):
                r = 105.0 + rank * 55.0
                # 14/18/22 knives -- denser than either nerf dared, because
                # the answer is stillness, not a seam. Ranks release at cyc
                # 78/102/126 and wash over the snapshot at ~126/175/224: a
                # slow, countable heartbeat of blades.
                n = 14 + rank * 4
                for i in range(n):
                    a = math.pi * 2.0 * i / float(n) + shf * 0.61 + rank * 0.35
                    kx = rx + math.cos(a) * r
                    ky = ry + math.sin(a) * r
                    if -20.0 < kx < KT_W + 20.0 and -20.0 < ky < KT_H + 20.0:
                        aim = math.atan2(ry - ky, rx - kx)
                        self._add(kx, ky, math.cos(aim) * 2.2, math.sin(aim) * 2.2,
                                "knife", 6 if rank % 2 == 0 else 7, 1.0,
                                fz=58 + rank * 24, calm=1)
            self._se("kira", 0, 0.7)
        if cyc in (78, 102, 126):
            self._se("fire3", 0, 0.55)      # each rank releases
        # The falling ribbons stay (the card's look), calm like the rings:
        # (t*49, every 12) traces ~37px-pitch diagonals that wash over a
        # still soul and only matter mid-step.
        if t % 12 == 4:
            self._add((t * 49) % KT_W, -12.0, 0.0, 1.5, "oval",
                    6 if (t // 12) % 3 else 7, 1.0, sway=0.5, ph=t * 0.13, calm=1)
            self._se("fire", 30, 0.3)
        # The REAL bullets -- plain amber ORBS, deliberately the most ordinary
        # sprite in the mode, unmistakable against a field of ice. Fired into
        # the post-wash lull at speeds tuned to arrive mid-NEXT-cycle: the
        # ring's broom (1.3 px/t) sweeps your camp right before the new
        # snapshot, and the aimed pair lands in the seam between washes.
        if cyc == 236:
            self._ring(self.bx, self.by, 14, 1.3, t * 0.013, "orb", 11)
            self._se("fire2", 0, 0.8)
        if cyc == 258:
            a = self._aim(self.bx, self.by)
            for off in (-0.10, 0.10):
                self._add(self.bx, self.by, math.cos(a + off) * 2.4,
                        math.sin(a + off) * 2.4, "orb", 11)
            self._se("gun", 6, 0.7)
    KTGame._sp17 = _kt_sp17

    def _kt_sp18(self, t):
        # BRAVERY (orange) -- "Tough Glove". Everything leads with its chin:
        # one-two punch fans that START slow and accelerate hard, a haymaker
        # orb that re-aims once mid-flight, and a lopsided hook of a ring.
        # Orange means KEEP MOVING; standing your ground is how you get hit.
        # Round sprites throughout -- every punch in this card lands as an
        # impact, not a projectile. (Sparks, not spheres: a sphere's 6.0 hit
        # radius against the old pellet's 4.5 would have been a stealth buff to
        # an already-tuned card. Sprites change here; hitboxes do not.)
        v = t % 56
        if v == 0 or v == 9:
            a = self._aim(self.bx, self.by) + (0.22 if v else -0.22)
            for off in (-0.16, 0.0, 0.16):
                self._add(self.bx, self.by, math.cos(a + off) * 1.1, math.sin(a + off) * 1.1,
                        "spark", 12, 1.0,
                        ax=math.cos(a + off) * 0.05, ay=math.sin(a + off) * 0.05)
            self._se("fire3", 0, 0.7)
        if t % 130 == 60:
            self._add(self.bx, self.by, 0.0, 2.2, "big", 12, 1.1, home=1, home_t=40)
            self._se("gun", 0, 0.9)
        if t % 90 == 45:
            self._ring(self.bx, self.by, 14, 2.3, (t // 90) * 0.83, "star", 11)
            self._se("fire2", 8, 0.7)
    KTGame._sp18 = _kt_sp18

    def _kt_sp19(self, t):
        # INTEGRITY (blue) -- "Ballet Shoes". Leaps: fountains of blue pellets
        # thrown UP from the stage floor that hang at the top of the jump and
        # come down as arcs -- gravity is the choreography, and the arc never
        # lies. Under it, a slow two-colour pirouette turns from her hands.
        # Ovals for the leap: the sprite tips over with the trajectory, so the
        # arc is drawn in the bullets and not just implied by them.
        if t % 46 == 0:
            k = t // 46
            fx = 70.0 + ((k * 173) % (KT_W - 140))
            vy0 = -3.6 - ((k * 7) % 3) * 0.3
            for off in (-0.5, -0.25, 0.0, 0.25, 0.5):
                self._add(fx, KT_H + 10.0, off * 1.6, vy0 + abs(off) * 0.4,
                        "oval", 5, 1.0, ay=0.022)
            self._se("fire2", 0, 0.7)
        if t % 8 == 4:
            base = t * 0.055
            self._add(self.bx, self.by, math.cos(base) * 1.7, math.sin(base) * 1.7, "sphere", 5)
            self._add(self.bx, self.by, math.cos(base + math.pi) * 1.7,
                    math.sin(base + math.pi) * 1.7, "sphere", 6)
        if t % 120 == 80:
            self._fan(self.bx, self.by, 3, self._aim(self.bx, self.by), 0.2, 2.4, "star", 13)
            self._se("fire", 10, 0.6)
    KTGame._sp19 = _kt_sp19

    def _kt_sp20(self, t):
        # PERSEVERANCE (purple) -- "Torn Notebook". Ruled lines: violet ink
        # writes itself across the page row after row (single-file dagger
        # streams, staggered freeze frames, like sp14's scanline grown into
        # handwriting), each written line sinking into the one below it. The
        # tear in each line is ONE missing beat -- a crossing window, not a
        # parking spot. (2026-07 severe buff: rows on a 44t clock so six-plus
        # lines share the page, longer lines, faster ink, heavier blot rain,
        # and the nib snipes whoever reads too slow.) The lines stay thin
        # daggers -- quills: handwriting, not blades -- while the blots are
        # INK BLOTS (sphere's radius) and the nib is the one real knife on the
        # page.
        if t % 44 == 0:
            row = t // 44
            y0 = 84.0 + (row % 7) * 76.0
            from_left = (row % 2 == 0)
            tear = (row * 137) % 20
            for i in range(20):
                if i == tear:
                    continue        # the torn beat of this line
                self._add(-14.0 if from_left else KT_W + 14.0, y0,
                        3.4 if from_left else -3.4, 0.22, "dagger",
                        3 if i % 3 else 4, 1.0, fz=i * 5)
            self._se("laser2", 0, 0.7)
        if t % 22 == 11:
            k = t // 22
            self._add((k * 149) % KT_W, -12.0, 0.0, 1.7 + 0.5 * (k % 3), "blot",
                    3 if k % 2 else 4, 1.0 + 0.15 * (k % 2))   # ink blot rain
            self._se("fire", 20, 0.45)
        if t % 56 == 28:
            a = self._aim(self.bx, self.by)
            self._add(self.bx, self.by, math.cos(a) * 3.6, math.sin(a) * 3.6,
                    "knife", 2, 1.2)                           # the nib
            self._se("fire3", 8, 0.7)
    KTGame._sp20 = _kt_sp20

    def _kt_sp21(self, t):
        # KINDNESS (green) -- "Burnt Pan". Servings lob off her hands, arc
        # like a ladle swing, and burst into FULL double rings -- a fast
        # course and a slow one from every pan, layering into moire as they
        # cross. No merciful door anymore (it made getting hit an act of
        # will): she is trying to share, there is simply so much of it, and
        # seconds arrive before you finish firsts -- gentle homing helpings
        # included. (Same shell-handle trick as the Hunter's flares.)
        pans = self.scratch.setdefault("pans", [])
        if t % 70 == 20:
            k = t // 70
            sh = self._add(self.bx, self.by, math.sin(k * 1.7) * 1.6, -1.9,
                        "big", 8, 1.1, ay=0.045)
            if sh is not None:
                pans.append((t + 64, sh))
            self._se("gun", 0, 0.8)
        while pans and pans[0][0] <= t:
            _, sh = pans.pop(0)
            sx, sy = sh["x"], sh["y"]
            if -20.0 < sx < KT_W + 20.0 and -20.0 < sy < KT_H:
                sh["ttl"] = sh["age"]        # the serving is dished out
                self._ring(sx, sy, 20, 1.9, sx * 0.011, "sphere", 8)
                self._ring(sx, sy, 12, 1.15, sx * 0.011 + 0.26, "star", 9)
                self._spark_burst(sx, sy, 8, 8, 2.6, 26)
                self._se("break_sm", 0, 0.7)
        if t % 130 == 65:
            # Second helpings: a pair of slow homing servings, one per hand.
            for ox in (-36.0, 36.0):
                self._add(self.bx + ox, self.by, 0.0, 1.9, "big", 8, 1.0,
                        home=1, home_t=46)
            self._se("gun", 8, 0.8)
        if t % 6 == 3:
            self._add((t * 83) % KT_W, -12.0, 0.0, 1.7, "oval",
                    9 if (t // 6) % 3 else 8, 1.0, sway=0.9, ph=t * 0.12)
            self._se("fire", 28, 0.35)
    KTGame._sp21 = _kt_sp21

    def _kt_sp22(self, t):
        # JUSTICE (yellow) -- "Empty Gun". Six chambers, fanned THREE deep:
        # every pull throws a triple-layered six-round volley (half a chamber
        # offset per layer, three speeds -- an expanding twelve-spoke star).
        # Every SIXTH pull is still the empty chamber, but the click is a
        # RELOAD, not a rest: six spent casings eject and rain back down with
        # gravity. The marksman's snap-shot telegraphs, then rides your saved
        # position with a five-round burst. (2026-07 severe buff.)
        # The lead round of each pull is an EYE -- a chamber seen down the
        # barrel is a bright ring with a dark hole in it -- the casings are
        # ovals tumbling out, and the fast third layer is the muzzle flash.
        # Only ONE of the three layers gets eyes: the sprite is fully opaque
        # (no alpha falloff at all, unlike every other bullet here), and three
        # 6-round layers of it, three volleys deep, whites out the playfield.
        cyc = t % 54
        if cyc == 0:
            k = t // 54
            if k % 6 == 5:
                self._se("invalid", 0, 0.9)      # the empty chamber...
                for i in range(6):
                    a = -math.pi * 0.5 + (i - 2.5) * 0.3
                    self._add(self.bx, self.by, math.cos(a) * 1.6,
                            math.sin(a) * 1.6 - 0.6, "oval", 11, 1.0,
                            ay=0.05)             # ...ejects its casings
            else:
                base = k * 0.55
                self._ring(self.bx, self.by, 6, 2.7, base, "eye", 10, 0.8)
                self._ring(self.bx, self.by, 6, 2.2, base + 0.5236, "big", 10, 0.7)
                self._ring(self.bx, self.by, 6, 3.2, base + 0.2618, "spark", 11)
                self._se("gun", 0, 0.9)
        snp = t % 110
        if snp == 50:
            self.scratch["jx"] = self.px
            self.scratch["jy"] = self.py
            for i in range(4):
                if len(self.sparks) < KT_MAX_SPARKS:
                    self.sparks.append({"x": self.px, "y": self.py - 30.0 - i * 22.0,
                                        "vx": 0.0, "vy": 0.8, "age": 0, "ttl": 20, "ci": 10})
            self._se("charge2", 0, 0.6)
        if snp == 70:
            jx = self.scratch.get("jx", self.px)
            jy = self.scratch.get("jy", self.py)
            a = math.atan2(jy - self.by, jx - self.bx)
            for d in (0, 9, 18, 27, 36):
                self._add(self.bx, self.by, math.cos(a) * 5.6, math.sin(a) * 5.6,
                        "knife", 10, 1.1, fz=d)
            self._se("laser", 0, 0.9)
    KTGame._sp22 = _kt_sp22

# --- RENDERER ------------------------------------------------------------------
# KTStage: ONE creator-defined displayable that (a) steps the simulation on a
# fixed 1/60s accumulator and (b) paints the whole mode -- stage, bullets, boss,
# player, sparkles, HUD, banners -- as cached-texture blits. It requests an
# immediate redraw every frame, so the screen tree around it never rebuilds.
init python:
    KT_FONT = "assets/fonts/SF Automaton Extended.ttf"

    class KTStage(renpy.Displayable):

        # Class-level displayable caches (persist across frames + interactions).
        # These cache Transform/Text/Solid displayables, NOT renpy.Render
        # objects. Matsu'Py Render objects are frame products and should not be
        # retained on a creator-defined displayable. The frame_tex memo inside
        # render() handles per-frame Render reuse safely.
        _tf_cache = {}
        _text_cache = {}
        _misc_cache = {}
        # Art-cell Transforms (_art). Kept apart from _misc so the churn of FX
        # buckets (spawn rings, muzzles, sparks in every colour an Endless run
        # reads) can never evict text or shader entries -- and given a roomier
        # cap, because every key here is a cheap rebuild of a shared Crop.
        _art_cache = {}
        # One Text per (character, size, colour) -- see _draw_glyphs. A few
        # dozen entries for the whole fight, so it is never wiped.
        _glyph_cache = {}
        # Boss sprite Transforms, keyed (variant, row, col). The sheet has 112
        # cells and five draw variants (plain, victory flash, hit glint, travel
        # ghost, mirror phantom), which is too many to share _misc's 1200-key
        # budget with the text and shader quads -- so it gets its own, sized to
        # hold every combination without ever wiping mid-fight.
        _boss_cache = {}

        # kind: (atlas row, base zoom, turns?)
        # Adding a bullet family starts in the atlas art
        # (draw it once per palette colour), then here, then KT_KIND_HR -- and
        # KT_SPIN if it points along its heading, or KT_TWIRL if it spins. The
        # cache key is (kind, colour index, rotation bucket, scale quarter).
        #
        # Every sprite is drawn at its true size for scale 1.0, so the base zoom
        # is 1.0 almost everywhere; `drop` is the raindrop grown to the old
        # oval's size, because that is the radius it inherited. `turns` means
        # the Transform takes a rotation at all -- pointed kinds use the
        # sim's heading bucket, twirling kinds the renderer's own clock.
        # `butterfly_b` is not a kind the sim ever spawns: it is the butterfly's
        # second wing-beat frame, swapped in by the draw loop.
        KINDS = {
            "orb":         ("orb", 1.0, False),
            "big":         ("big", 1.0, False),
            "pellet":      ("pellet", 1.0, True),
            "dagger":      ("dagger", 1.0, True),
            "knife":       ("knife", 1.0, True),
            "star":        ("star", 1.0, True),
            "sphere":      ("sphere", 1.0, False),
            "ring":        ("ring", 1.0, False),
            "oval":        ("oval", 1.0, True),
            "spark":       ("spark", 1.0, True),
            "eye":         ("eye", 1.0, False),
            "ofuda":       ("ofuda", 1.0, False),
            "rice":        ("rice", 1.0, True),
            "drop":        ("rice", 1.12, True),
            "camellia":    ("camellia", 1.0, True),
            "butterfly":   ("butterfly", 1.0, True),
            "butterfly_b": ("butterfly_b", 1.0, True),
            "tile":        ("tile", 1.0, True),
            "blot":        ("blot", 1.0, False),
        }

        # The spawn ring (see SPAWN MATERIALIZE) closes onto a bullet's BODY,
        # so it needs each kind's rough drawn diameter at scale 1.0.
        SPAWN_BODY = {
            "big": 46.0, "eye": 46.0, "knife": 26.0, "star": 24.0,
            "camellia": 24.0, "butterfly": 24.0, "blot": 24.0, "ofuda": 22.0,
        }

        def __init__(self, game, **kwargs):
            super(KTStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0
            # Boss motion history (renderer-side, cosmetic): recent draw
            # positions for the travel afterimages on dart/sweep moves.
            self.trail = []
            self._trail_tick = -99
            # Boss animation state, advanced only when the simulation tick
            # changes. Duplicate render calls must not double-step it and
            # pause must freeze it with the rest of the fight.
            self._boss_motion_tick = game.tick
            self._boss_last_x = game.bx
            # Eased, signed travel speed in KT_BOSS_LEAN_FULL units: magnitude
            # asks for a lean depth, sign latches the facing.
            self._boss_lean = 0.0
            self._boss_face = 0
            # Pose LEVELS (0..3), each stepped one depth at a time toward what
            # the fight asks for, so every pose change plays its in-betweens.
            # [level, tick of its last step] per action.
            self._lean_want = 0
            self._lvl = {"lean": [0, -999], "cast": [0, -999], "decl": [0, -999]}
            # Cast pulse: when it started, when its arms may come down, and
            # when the next one is allowed to start.
            self._cast_start = -999
            self._cast_end = -999
            self._cast_rest_until = -999
            self._cast_muzzle = game.muzzle
            # The row picked for the current tick (the column is the clock),
            # and the tick it was entered.
            self._boss_row = KT_BOSS_IDLE
            self._row_since = game.tick
            # Player dash afterimages (renderer-side): sampled while the ship
            # moves unfocused, drawn as faint ghosts behind it.
            self.ptrail = []
            self._ptrail_tick = -99
            # HP-bar chip ghost (renderer-side, cosmetic): a pale segment that
            # lags behind the real fill so burst damage reads as a bite.
            self._hp_ghost = 1.0
            # Cosmetic FX envelope (see KT_FX_* and _advance_fx_env). Every
            # boss-layer level lives here and is eased toward its phase target
            # once per simulation tick, so nothing on this stage changes opacity
            # or size in a single frame. Seeded at the targets for the opening
            # phase so the fight does not fade up from nothing on frame one.
            self._fx_tick = game.tick
            self._fx_circle_a = 0.0
            self._fx_circle_px = 228.0
            self._fx_circle_breath = 0.022
            self._fx_circle_spin = 0.55
            self._fx_seal_a = 0.0
            self._fx_seal_px = 210.0
            self._fx_veil_a = 0.04
            self._fx_aura_a = 1.0
            self._fx_focus_a = 0.0
            self._fx_opt = 0.0          # 0 = options spread, 1 = tucked in (focus)
            self._fx_ring_a = 0.0       # the life ring's level
            self._fx_sbg_a = 0.0        # the spell background's level
            self._fx_sbg_style = KT_SPELL_BG[game.sp_pat % len(KT_SPELL_BG)]
            self._fx_dim = 0x55
            self._fx_col = list(Color(KT_PAL[game.cur_color]).rgb)
            # Which card's seal is latched (a spell pattern index; see
            # _advance_fx_env for why it is latched at all).
            self._fx_seal_idx = game.sp_pat

        # ----- prediction ----------------------------------------------------

        def visit(self):
            # Matsu'Py preloads what a displayable REPORTS as its children, and
            # everything this stage draws is built on demand inside render()
            # where nothing can see it. That is fine for the sprite sheets --
            # they are small and they are wanted on frame one anyway -- but the
            # backdrop is a full 1280x720 plate, and it used to be an `add` on
            # the screen, which meant the screen's own prediction pass decoded
            # it before the fight began. Naming it here keeps that: without it
            # the first frame of a run pays for the decode inline. The art
            # atlases are named for the same reason -- they are this stage's
            # whole sprite set, and the seals alone are a 1550px sheet.
            return [renpy.easy.displayable(
                KT_DIR + ("endless.png" if self.game.endless else "kotobackdrop.png"))] + [
                renpy.easy.displayable(KT_ART_DIR + info["file"])
                for info in KT_ATLAS.values()]

        # ----- input events --------------------------------------------------

        def event(self, ev, x, y, st):
            # The sim POLLS the keyboard (see KTGame._poll_input), so this is the
            # only place a key RELEASE is ever seen as an event. Hand it to the
            # latch, which uses it to unstick a key SDL still believes is held.
            # Always returns None so the screen's own `key` bindings (Escape,
            # give-up) and everything under us keep receiving the event.
            self.game.keys.handle_event(ev)
            return None

        # ----- cached displayable factories ---------------------------------

        def _bullet_tf(self, kind, ci, bucket, sq, ghost=0, ab=KT_SPAWN_STEPS):
            # Bullet texture cache. Rotation is bucketed, scale is quantized to
            # quarters (sq = scale * 4), and color is a palette index. Those
            # small integer keys are the reason hundreds of bullets still draw
            # as repeated blits of a few textures.
            # ghost=1 is the Patience tell: the same bullet at low alpha, used
            # for calm bullets while the soul is still (they cannot cut you,
            # and the field visibly says so). One extra cache dimension.
            # ab is the spawn fade step (see KT_SPAWN_ALPHA): KT_SPAWN_STEPS
            # means fully materialized, i.e. no alpha at all, which is what
            # every bullet past its first few ticks asks for.
            key = (kind, ci, bucket, sq, ghost, ab)
            tf = KTStage._tf_cache.get(key)
            if tf is None:
                row, base_zoom, rotates = KTStage.KINDS[kind]
                # The colour is the CELL: baked per palette entry, so there is
                # no matrixcolor here and the white core stays white.
                src = kt_art("kt_bullets", "%s:%d" % (row, ci))
                kw = dict(zoom=base_zoom * (sq / 4.0), subpixel=True)
                if ghost:
                    kw["alpha"] = 0.34
                elif ab < KT_SPAWN_STEPS:
                    kw["alpha"] = KT_SPAWN_ALPHA[ab]
                if rotates:
                    kw["rotate"] = bucket * KT_ROT_DEG
                tf = Transform(src, **kw)
                KTStage._tf_cache[key] = tf
            return tf

        def _art(self, sheet, cell, zoom=1.0, alpha=1.0, rotate=None, add=True):
            """One art cell as a cached Transform -- drawn as LIGHT by default.

            Glows, sparks, spawn rings, lasers, portals, motes and shots are all
            additive (Transform additive=1.0: premultiplied colour is added and
            nothing underneath is dimmed), which is what lets a dense field of
            them brighten where they overlap instead of stacking into mud.
            Callers pass BUCKETED zoom/alpha/rotate -- those floats are the
            cache key, so an unbucketed one would mint a Transform per frame.
            """
            key = (sheet, cell, zoom, alpha, rotate, add)
            d = KTStage._art_cache.get(key)
            if d is None:
                if len(KTStage._art_cache) > 2400:
                    KTStage._art_cache.clear()
                kw = dict(zoom=zoom, alpha=alpha, subpixel=True)
                if add:
                    kw["additive"] = 1.0
                if rotate is not None:
                    kw["rotate"] = rotate
                d = Transform(kt_art(sheet, cell), **kw)
                KTStage._art_cache[key] = d
            return d

        def _glyph(self, ch, size, color):
            key = (ch, size, color)
            t = KTStage._glyph_cache.get(key)
            if t is None:
                t = Text(ch, size=size, color=color, font=KT_FONT,
                         outlines=[(2, "#02040b", 0, 0)])
                KTStage._glyph_cache[key] = t
            return t

        def _draw_glyphs(self, dest, tex, text, x, y, size, color, align=0.0, track=-3.0):
            """Blit `text` one cached glyph at a time; returns its width.

            For the numbers that change every tick or two -- the timer's
            hundredths, the score, the live bonus. As whole-string Text, every
            new value was a new Text: a fresh layout each time, and enough of
            them to keep wiping the 128-entry text cache (and re-laying-out
            every OTHER label on the stage with it). Per-glyph, the whole fight
            is a few dozen cached glyphs and a number costs one dict lookup per
            digit. `align` is 0 left / 0.5 centre / 1 right, of x. `track`
            takes back most of the outline padding each glyph render carries
            on both sides, so the digits sit at normal spacing.
            """
            parts = []
            w = 0.0
            for ch in text:
                if ch == " ":
                    adv = size * 0.36
                    parts.append((None, adv))
                    w += adv
                    continue
                r, (gw, _gh) = tex(("gl", ch, size, color), self._glyph(ch, size, color),
                                   size * 2, size * 2)
                adv = gw + track
                parts.append((r, adv))
                w += adv
            w -= track
            cx = x - w * align
            for r, adv in parts:
                if r is not None:
                    dest.subpixel_blit(r, (cx, y))
                cx += adv
            return w

        def _misc(self, key, builder):
            # Shared factory for non-bullet displayables: icons, aura quads,
            # shader rings, cached Solid colors, etc. builder is called only on
            # a cache miss, so lambdas passed here should close over immutable
            # values, not mutable per-frame objects.
            #
            # Soft cap for the same reason _text has one: most keys here are a
            # fixed handful, but the bucketed shader quads (veil / spell circle
            # / focus sigil) key on colour AND a quantized size or alpha, and an
            # Endless run reads enough colours to keep minting new combinations.
            # Every key in here is reproducible from its lambda, so dropping the
            # lot costs one frame of rebuilds and nothing else.
            d = KTStage._misc_cache.get(key)
            if d is None:
                if len(KTStage._misc_cache) > 1200:
                    KTStage._misc_cache.clear()
                d = builder()
                KTStage._misc_cache[key] = d
            return d

        def _text(self, text, size, color, use_font=True, bold=False):
            # Text rendering is expensive enough to cache, but score and timer
            # values can create many unique strings. The soft cap prevents the
            # text cache from growing forever across repeated runs.
            key = (text, size, color, use_font, bold)
            t = KTStage._text_cache.get(key)
            if t is None:
                if len(KTStage._text_cache) > 128:
                    KTStage._text_cache.clear()
                t = Text(text, size=size, color=color, bold=bold,
                        font=(KT_FONT if use_font else None),
                        outlines=[(2, "#02040b", 0, 0)])
                KTStage._text_cache[key] = t
            return t

        def _text_fade(self, text, size, color, bold, ab, steps=8):
            """One cached Text wrapped in a BUCKETED alpha.

            A Text displayable has no alpha of its own, so a label that fades
            has to be a Transform around one -- and a Transform built per frame
            per label is exactly the allocation the rest of this renderer goes
            out of its way to avoid. Bucketing the alpha into `steps` costs a
            handful of _misc keys per string and is invisible at eight steps,
            which is the same trade the bullets, sparks and motes all make.

            The top bucket returns the bare Text so a fully-opaque label is
            never wrapped at all (and so the flight below can reuse the render
            it already made to MEASURE the line).
            """
            if ab >= steps - 1:
                return self._text(text, size, color, True, bold)
            ab = max(0, ab)
            return self._misc(("tfade", text, size, color, bold, ab, steps),
                (lambda: Transform(self._text(text, size, color, True, bold),
                                   alpha=ab / float(steps - 1))))

        def _card_lines(self, text):
            # Spell card names are split into "Sign Type" and quoted title so
            # both the declaration banner and the in-card HUD can size them
            # independently.
            quote_at = text.find('"')
            if quote_at > 0:
                return [text[:quote_at].strip(), text[quote_at:].strip()]
            return [text]

        def _size_for_line(self, text, base, minimum):
            # Small text fitter for long card names and banners. It is crude on
            # purpose: a fixed few sizes cache better than per-pixel font math.
            if len(text) > 34:
                return max(minimum, base - 6)
            if len(text) > 28:
                return max(minimum, base - 3)
            return base

        # ----- spell-card declaration ----------------------------------------
        # Four helpers and one draw. They are pure functions of the declare
        # tick wherever they possibly can be: the smear needs LAST tick's
        # portrait position and the flight needs a value that survives a phase
        # change, and both of those are things a stored field gets wrong the
        # first time a catch-up frame runs two sim ticks or the pause overlay
        # freezes one.

        def _cutin_half(self, pt):
            """Half-height of the declaration ribbon at declare tick `pt`.

            Ease-OUT on the way open (it flies apart and settles) and ease-IN
            on the way shut (it hesitates, then snaps closed). Never reaches
            zero: the last frame is a hairline, which is what the closing
            flash is painted on.
            """
            if pt < KT_DECL_OPEN:
                u = pt / float(KT_DECL_OPEN)
                return max(1.0, KT_DECL_BAND_HALF * (1.0 - (1.0 - u) ** 3))
            if pt < KT_DECL_CLOSE:
                return KT_DECL_BAND_HALF
            u = kt_clamp((pt - KT_DECL_CLOSE) /
                         float(KT_DECLARE_TICKS - 1 - KT_DECL_CLOSE), 0.0, 1.0)
            return max(1.0, KT_DECL_BAND_HALF * (1.0 - u * u))

        def _cutin_port_x(self, pt):
            """Centre x of the portrait at declare tick `pt`.

            She comes in from the LEFT lip, opposite the right-aligned type.
            A cubic ease-out arrival, then a slow push. This is the whole
            difference between an entrance and a slide show: the old pass
            moved her at a flat 10.5 px/tick from the first frame of the
            declaration to the last, and one constant speed cannot read as
            anything arriving anywhere.
            """
            if pt < KT_DECL_PORT_IN:
                u = kt_clamp(pt / float(KT_DECL_PORT_IN), 0.0, 1.0)
                return (KT_DECL_PORT_X0 +
                        (KT_DECL_PORT_X1 - KT_DECL_PORT_X0) * (1.0 - (1.0 - u) ** 3))
            u = kt_clamp((pt - KT_DECL_PORT_IN) /
                         float(KT_DECLARE_TICKS - KT_DECL_PORT_IN), 0.0, 1.0)
            return KT_DECL_PORT_X1 + (KT_DECL_PORT_X2 - KT_DECL_PORT_X1) * u

        def _card_flight(self, g):
            """0.0 = the card name is parked in the declaration banner;
            1.0 = it is settled in its HUD slot.

            This is the value that makes the handover seamless, and the only
            reason it lives in its own method is that it spans a PHASE
            BOUNDARY: it starts moving inside `declare` and finishes inside
            `spell`, so the name is one object crossing the flip rather than a
            big label that vanishes from mid-stage and a small one that
            appears in the corner on the very next frame.

            The declare half divides by (KT_DECLARE_TICKS - 1) because
            _run_phase flips the phase the moment phase_tick REACHES
            KT_DECLARE_TICKS: the renderer never sees that tick, so dividing
            by it would leave a visible step in the middle of the handover.
            """
            if g.phase == "declare":
                if g.phase_tick < KT_DECL_CLOSE:
                    return 0.0
                u = kt_clamp((g.phase_tick - KT_DECL_CLOSE) /
                             float(KT_DECLARE_TICKS - 1 - KT_DECL_CLOSE), 0.0, 1.0)
                return 0.62 * u * u                          # ease-in: it leaves
            if g.phase == "spell" and g.phase_tick < KT_CARD_FLIGHT:
                u = g.phase_tick / float(KT_CARD_FLIGHT)
                return 0.62 + 0.38 * (1.0 - (1.0 - u) ** 3)  # ease-out: it lands
            return 1.0

        def _card_flight_draw(self, g, bar, f, stage, tex):
            """The card name partway between the banner and the HUD slot.

            Both faces are drawn against the SAME right edge, the big one
            fading out and the small one fading in, so the change of size
            happens as a dissolve at the moment the eye is already tracking a
            moving object -- which is what sells one label shrinking rather
            than two labels swapping. Right-aligned at both ends (the ribbon's
            type column and the top-right HUD slot) is what lets the path be a
            plain lerp of that edge and still look concentric.

            Each line is MEASURED at its opaque size before anything is drawn
            faded, so the stack it lands in is pixel-identical to the static
            HUD draw and nothing jumps on the frame the flight ends.
            """
            lines = self._card_lines(bar["card"])
            a_big = kt_clamp(1.0 - f / 0.66, 0.0, 1.0)
            a_small = kt_clamp((f - 0.40) / 0.42, 0.0, 1.0)
            ab = int(a_big * 7.999)
            asm = int(a_small * 7.999)
            rx = KT_DECL_TEXT_R + (KT_HUD_R - KT_DECL_TEXT_R) * f
            big_y = KT_DECL_TEXT_Y
            small_y = KT_HUD_NAME_Y
            for i, line in enumerate(lines):
                bsize = self._size_for_line(line, 27, 21)
                ssize = self._size_for_line(line, 16 if i == 0 else 15, 12)
                scol = (KT_PAL[bar["color"]] if i == 0 and len(lines) > 1
                        else "#ffd7e8")
                y = big_y + (small_y - big_y) * f
                bmr, (bmw, bmh) = tex(("cardname", g.bar_index, i, bsize),
                    self._text(line, bsize, "#f5faff", True, True), KT_W - 60, 52)
                smr, (smw, smh) = tex(("cardname_sm", g.bar_index, i, ssize),
                    self._text(line, ssize, scol, True, True), KT_W - 130, 30)
                if a_big > 0.02:
                    if ab >= 7:
                        fr_ = bmr
                    else:
                        fr_, _fs = tex(("cardfly_b", i, bsize, ab),
                            self._text_fade(line, bsize, "#f5faff", True, ab),
                            KT_W - 60, 52)
                    stage.subpixel_blit(fr_, (rx - bmw, y))
                if a_small > 0.02:
                    if asm >= 7:
                        sr2 = smr
                    else:
                        sr2, _ss = tex(("cardfly_s", i, ssize, scol, asm),
                            self._text_fade(line, ssize, scol, True, asm),
                            KT_W - 130, 30)
                    stage.subpixel_blit(sr2, (rx - smw, y))
                big_y += bmh + 4
                small_y += smh + 2

        def _draw_cutin(self, g, bar, stage, tex, rect, fx_col):
            """The spell-card declaration, staged.

            Everything that belongs INSIDE the ribbon is blitted into `cut`, a
            sub-render whose height IS the animation: it flies open, holds and
            shuts, and the clipping flags crop the glass, the portrait and the
            type against its edges for nothing. Flags, not subsurface -- see
            the note at the bottom of render(); a subsurface here would walk
            and rebuild every child it contains, every frame.

            The shader quad inside is always the full KT_DECL_BAND_H tall and
            is simply clipped by the ribbon, because a mesh Transform's pixel
            size is both a cache key AND a render-to-texture: animating it
            would reallocate a texture on every frame of the open and the
            shut. Same rule as koto.circle's u_koto_scale -- animate a
            uniform, never a cached quad's dimensions.
            """
            pt = g.phase_tick
            col = KT_PAL[bar["color"]]
            half = self._cutin_half(pt)
            btop = KT_DECL_BAND_MID - half
            bh = max(2, int(half * 2.0))
            f = self._card_flight(g)

            # Letterbox pinch. The stage stops competing with the ribbon and
            # comes back up as it shuts; this is most of why the beat reads as
            # a cut rather than as an overlay parked on top of the fight.
            pinch = (kt_clamp(pt / 14.0, 0.0, 1.0) *
                     kt_clamp((KT_DECLARE_TICKS - 4 - pt) / 20.0, 0.0, 1.0))
            if pinch > 0.01:
                pc = "#000000%02x" % int(pinch * 82.0)
                stage.blit(rect(pc, KT_W, max(1, int(btop))), (0, 0))
                stage.blit(rect(pc, KT_W, max(1, int(KT_H - btop - bh))),
                           (0, int(btop + bh)))

            cut = renpy.Render(KT_W, bh)
            cut.xclipping = True
            cut.yclipping = True
            cblit = cut.subpixel_blit
            oy = -btop                  # stage-local y -> ribbon-local y

            # --- glass, speed lines and sheen: one quad ---------------------
            if KT_SHADER_OK:
                rush_u = kt_clamp(pt / 40.0, 0.0, 1.0)
                # The sheen crosses once on the open and once on the shut, and
                # is parked far off the quad in between -- cheaper than a
                # branch in the shader, and it keeps the uniform continuous.
                if 8 <= pt < 42:
                    sheen = -0.35 + (pt - 8) / 34.0 * 1.75
                elif pt >= KT_DECL_CLOSE:
                    sheen = 1.40 - (pt - KT_DECL_CLOSE) / 20.0 * 1.75
                else:
                    sheen = 9.0
                cut_d = Transform(
                    self._fx_solid(), xysize=(KT_W, KT_DECL_BAND_H),
                    shader="koto.cutin", mesh=True,
                    u_koto_col=fx_col,
                    u_koto_alpha=(kt_clamp(pt / 6.0, 0.0, 1.0) *
                                  kt_clamp((KT_DECLARE_TICKS - 2 - pt) / 14.0,
                                           0.0, 1.0)),
                    # Her anchor, in this quad's normalized space. She floats
                    # ABOVE the ribbon during a declaration, so the focus is a
                    # negative y and the fan enters over the top rail.
                    u_koto_focus=(g.bx / float(KT_W),
                                  (g.by - (KT_DECL_BAND_MID - KT_DECL_BAND_HALF))
                                  / float(KT_DECL_BAND_H)),
                    u_koto_aspect=KT_W / float(KT_DECL_BAND_H),
                    u_koto_rush=(2.05 * (1.0 - (1.0 - rush_u) ** 2)
                                 + 0.16 * math.sin(g.tick * 0.06)),
                    # The fan is loudest on the throw and has settled to a
                    # bed by the time the name has finished cascading in, so it
                    # never competes with the card it exists to introduce.
                    u_koto_rushamp=1.0 - 0.66 * kt_clamp((pt - 18) / 26.0, 0.0, 1.0),
                    u_koto_sheen=sheen)
                try:
                    cur_, _csz = tex(("cutin_q",), cut_d, KT_W, KT_DECL_BAND_H)
                    cut.blit(cur_, (0, int(KT_DECL_BAND_MID - KT_DECL_BAND_HALF + oy)))
                except Exception:
                    pass

            # --- portrait ---------------------------------------------------
            # Her silhouette arrives from the right lip and stops. The smear
            # is taken from the ANALYTIC difference between this tick's
            # position and last tick's, so it stores nothing: there is no
            # streak to leak into the next declaration, nothing to reset on a
            # phase change, and it freezes correctly under the pause overlay.
            cx = self._cutin_port_x(pt)
            dx = cx - self._cutin_port_x(max(0, pt - 1))
            py = KT_DECL_PORT_CY + math.sin(g.tick * 0.05) * 4.0 + oy
            # The portrait is the card-raised pose, and it keeps breathing on
            # the stage sprite's own loop rather than freezing as a still.
            prow = KT_BOSS_DECLARE[-1]
            pcol = (g.tick // KT_BOSS_PHASE_TICKS) % KT_BOSS_PHASES
            hkey = ("cutin_halo", bar["color"], pcol)
            hdisp = self._misc(hkey, (lambda c=bar["color"], pc=pcol: Transform(
                KT_BOSS_FRAMES[prow][pc], zoom=KT_DECL_PORT_ZOOM * 1.07,
                nearest=True, subpixel=True,
                matrixcolor=TintMatrix(KT_PAL[c]), alpha=0.17)))
            hr_, (hw_, hh_) = tex(hkey, hdisp, 700, 700)
            cblit(hr_, (cx - hw_ / 2.0, py - hh_ / 2.0))
            if abs(dx) > 2.2:
                # Three ghosts trailing the travel, and ONLY while there is
                # travel: on the settle they stop existing rather than fading
                # out, which is the difference between a fast entrance and a
                # permanently blurry one.
                for k in (3, 2, 1):
                    gkey = ("cutin_smear", k, pcol)
                    gdisp = self._misc(gkey, (lambda kk=k, pc=pcol: Transform(
                        KT_BOSS_FRAMES[prow][pc], zoom=KT_DECL_PORT_ZOOM,
                        nearest=True, subpixel=True, alpha=0.22 / kk)))
                    gr_, (gw_, gh_) = tex(gkey, gdisp, 680, 680)
                    cblit(gr_, (cx - dx * k * 1.6 - gw_ / 2.0, py - gh_ / 2.0))
            # NOT tinted, and that is the entire difference between a
            # portrait and a wash. A TintMatrix collapses the cell to one hue
            # scaled by luminance, and her art is pale hair over a dark dress:
            # tinted to the card colour at any alpha that stayed under the type
            # she became a pink smudge on a pink fan, which is what the old
            # 0.22 silhouette had always been. Her own colours read against the
            # dark glass, and the tinted halo behind her carries the card.
            pkey = ("cutin_port", pcol)
            pdisp = self._misc(pkey, lambda pc=pcol: Transform(
                KT_BOSS_FRAMES[prow][pc], zoom=KT_DECL_PORT_ZOOM,
                nearest=True, subpixel=True, alpha=0.62))
            pr_, (pw_, ph_) = tex(pkey, pdisp, 680, 680)
            cblit(pr_, (cx - pw_ / 2.0, py - ph_ / 2.0))

            # --- rails ------------------------------------------------------
            # Drawn at the RIBBON's own edges rather than at fixed stage
            # coordinates, so they ride the open and the shut instead of
            # appearing once it has landed. Two hairlines used to be the
            # entire frame; they are the trim now.
            ra = kt_clamp(pt / 3.0, 0.0, 1.0)
            glow_c = col + ("%02x" % int(34 * ra))
            rail_c = col + ("%02x" % int(215 * ra))
            inner_c = col + ("%02x" % int(68 * ra))
            cut.blit(rect(glow_c, KT_W, 10), (0, 0))
            cut.blit(rect(glow_c, KT_W, 10), (0, bh - 10))
            cut.blit(rect(rail_c, KT_W, 2), (0, 0))
            cut.blit(rect(rail_c, KT_W, 2), (0, bh - 2))
            cut.blit(rect(inner_c, KT_W, 1), (0, 7))
            cut.blit(rect(inner_c, KT_W, 1), (0, bh - 8))
            # A soft chip of light travelling each rail, in opposite
            # directions. One direction reads as a texture sliding past; two
            # read as a frame that is lit. A stretched flare rather than a
            # Solid, so both ends feather instead of ending in a hard corner.
            chkey = ("cutin_chip",)
            chd = self._misc(chkey, lambda: Transform(
                kt_art("kt_fx", "flare:13"), xzoom=3.4, yzoom=0.28, subpixel=True,
                alpha=0.95, additive=1.0))
            chr_, (chw, chh) = tex(chkey, chd, 240, 32)
            chip = (g.tick * 7.0) % (KT_W + chw * 2.0) - chw
            cblit(chr_, (chip, 1.0 - chh / 2.0))
            cblit(chr_, (KT_W - chw - chip, bh - 1.0 - chh / 2.0))

            # --- the slam ---------------------------------------------------
            # The seam the ribbon opened from, thinning out where it split.
            if pt < 12:
                sh = max(1, 9 - pt)
                cut.blit(rect("#f5faff" + ("%02x" % int(230 * (1.0 - pt / 12.0))),
                              KT_W, sh),
                         (0, int(KT_DECL_BAND_MID + oy - sh / 2.0)))
            # ...and the same seam closing on it. Once the ribbon is thinner
            # than the flash, the flash fills the whole thing, so the last
            # frames of a declaration are a bright line pinching out.
            if half < 10.0:
                cut.blit(rect(col + ("%02x" % int(225 * (1.0 - half / 10.0))),
                              KT_W, bh), (0, 0))

            # --- type -------------------------------------------------------
            # Mask cards declare as MASK CARD, soul cards as SOUL CARD -- the
            # one-frame tell that an Endless-exclusive is about to be read.
            if g.cur_is_soul:
                kick_label = "SOUL CARD"
            elif g.cur_is_mask:
                kick_label = "MASK CARD"
            else:
                kick_label = "SPELL CARD"
            # Cascade: kick label, then each name line, each on its own
            # ease-out slide. The old pass strobed the whole block on and off
            # for its first 24 ticks (`(pt // 3) % 4 != 0`), which is a
            # flicker, not an entrance.
            ke = (kt_clamp((pt - 6) / 12.0, 0.0, 1.0) *
                  kt_clamp((KT_DECLARE_TICKS - 6 - pt) / 14.0, 0.0, 1.0))
            if ke > 0.01:
                # The right edge slides in from further right (the type column
                # is right-aligned; see KT_DECL_TEXT_R).
                kx = KT_DECL_TEXT_R + 56.0 * (1.0 - ke) ** 2
                # FOUR alpha steps, not eight. The cascade labels are moving
                # fast enough that the banding is invisible, and each bucket
                # is a _misc key per (string, card colour): at eight, an
                # Endless run's 15 colours and 22 cards mint enough entries to
                # start tripping the 1200-key wipe mid-fight. The flight below
                # keeps eight -- that one is slow and the eye is on it.
                kab = int(ke * 3.999)
                if pt < 16:
                    # Chromatic split on arrival: two tinted ghosts either
                    # side, closing as it lands. Two cache keys, and it is the
                    # difference between the label appearing and it LANDING.
                    sp = (16 - pt) * 0.5
                    for _tint, _off in (("#ff2d55", -sp), ("#2df5ff", sp)):
                        gkey2 = ("cutin_kickghost", kick_label, _tint)
                        gd2 = self._misc(gkey2, (lambda t=_tint: Transform(
                            self._text(kick_label, 15, "#ffffff", True, True),
                            matrixcolor=TintMatrix(t), alpha=0.42)))
                        gr2, (gw2, _gh2) = tex(gkey2, gd2, 240, 30)
                        cblit(gr2, (kx - gw2 + _off, KT_DECL_KICK_Y + oy))
                kr_, (kw2, kh2) = tex(("cutin_kick", kick_label, col, kab),
                    self._text_fade(kick_label, 15, col, True, kab, 4), 240, 30)
                cblit(kr_, (kx - kw2, KT_DECL_KICK_Y + oy))

            card_lines = self._card_lines(bar["card"])
            line_y = KT_DECL_TEXT_Y
            widest = 0
            for i, line in enumerate(card_lines):
                size = self._size_for_line(line, 27, 21)
                nmr, (nw, nh) = tex(("cardname", g.bar_index, i, size),
                    self._text(line, size, "#f5faff", True, True), KT_W - 60, 52)
                # Once the flight has begun the name is no longer IN the
                # ribbon -- it is on its way to the corner, drawn on the stage
                # below so the closing ribbon cannot clip it.
                le = kt_clamp((pt - 12 - i * 6) / 14.0, 0.0, 1.0)
                if le > 0.0 and f <= 0.0:
                    lx = KT_DECL_TEXT_R + 70.0 * (1.0 - le) ** 3
                    lab = int(le * 3.999)
                    if lab >= 3:
                        lr_ = nmr
                    else:
                        lr_, _ls = tex(("cutin_line", i, size, lab),
                            self._text_fade(line, size, "#f5faff", True, lab, 4),
                            KT_W - 60, 52)
                    cblit(lr_, (lx - nw, line_y + oy))
                line_y += nh + 4
                widest = max(widest, nw)

            # Rule under the name: a line that ARRIVES at its length is a
            # beat; a line that is simply there is furniture.
            ru = (kt_clamp((pt - KT_DECL_RULE_AT) / float(KT_DECL_RULE_LEN),
                           0.0, 1.0) *
                  kt_clamp((KT_DECLARE_TICKS - 8 - pt) / 12.0, 0.0, 1.0))
            if ru > 0.01:
                # Capped, because the rule belongs to the TYPE COLUMN. Left
                # uncapped it tracked the widest line, and the longest card
                # names ("The Scene Everyone Remembers") ran it straight
                # through the portrait's forearm.
                # It draws out LEFTWARD from the type column's right edge.
                rw = max(1, int(min(widest + 26, 330) * (1.0 - (1.0 - ru) ** 3)))
                cut.blit(rect(col + "cc", rw, 2),
                         (int(KT_DECL_TEXT_R - rw), int(line_y + 8 + oy)))
                cut.blit(rect(col + "2e", rw, 7),
                         (int(KT_DECL_TEXT_R - rw), int(line_y + 10 + oy)))
            if ru > 0.40:
                # What the capture is worth, said out loud at the moment the
                # card is named -- the one number the declaration was never
                # telling you.
                vtxt = "BONUS  " + format(g.cur_value, ",")
                vab = int(kt_clamp((ru - 0.40) / 0.50, 0.0, 1.0) * 3.999)
                vr_, (vw_, _vh) = tex(("cutin_val", vtxt, vab),
                    self._text_fade(vtxt, 12, "#9aa8bd", False, vab, 4), 280, 24)
                cblit(vr_, (KT_DECL_TEXT_R - vw_, line_y + 22 + oy))

            stage.subpixel_blit(cut, (0.0, btop))

            # White kick over the whole stage, drawn last and short: it is the
            # CUT. The card-colour wash is _flash's job and is already running
            # underneath it on its own longer decay.
            if pt < 6:
                stage.blit(rect("#f5faff" + ("%02x" % int(155 * (1.0 - pt / 6.0))),
                                KT_W, KT_H), (0, 0))

            # The name, once it has left the ribbon. On the stage rather than
            # in the sub-render, precisely so the ribbon shutting cannot clip
            # it out of its own flight.
            if f > 0.0:
                self._card_flight_draw(g, bar, f, stage, tex)

        def _advance_boss_anim(self, game):
            """One simulation tick of Kotonoha's cosmetic pose state.

            Picks the ROW for this tick (the column is the clock -- see
            _boss_frame). Guarded by the caller on the sim tick, so a duplicate
            render() never double-steps it and the pause freezes it.
            """
            steps = max(1, game.tick - self._boss_motion_tick)
            dx = (game.bx - self._boss_last_x) / steps
            self._boss_last_x = game.bx
            self._boss_motion_tick = game.tick
            tick = game.tick

            # Ease toward the current signed travel speed. The ease is what
            # makes a lean ramp in and settle out; raw per-tick dx is noisy,
            # because the lerp in _move_boss wobbles it near every target.
            # Closed form, so a catch-up frame lands where n ticks would.
            target = kt_clamp(dx / KT_BOSS_LEAN_FULL, -1.0, 1.0)
            k = 1.0 - (1.0 - KT_BOSS_LEAN_EASE) ** steps
            self._boss_lean += (target - self._boss_lean) * k
            mag = abs(self._boss_lean)
            if self._boss_lean <= -KT_BOSS_FACE_LATCH:
                self._boss_face = -1
            elif self._boss_lean >= KT_BOSS_FACE_LATCH:
                self._boss_face = 1
            want = self._lean_want
            while want < 3 and mag >= KT_BOSS_LEAN_RISE[want]:
                want += 1
            while want > 0 and mag < KT_BOSS_LEAN_FALL[want - 1]:
                want -= 1
            self._lean_want = want

            # Cast pulse: see KT_BOSS_CAST_*. A pulse only STARTS from a
            # body that is travelling gently (at a hard lean the tilt is the
            # read, and the muzzle flare still sells the volley), and only once
            # the last pulse's rest is over.
            cast_lv = self._lvl["cast"]
            if game.muzzle != self._cast_muzzle:
                self._cast_muzzle = game.muzzle
                if tick < self._cast_end:
                    self._cast_end = min(tick + KT_BOSS_CAST_HOLD,
                                         self._cast_start + KT_BOSS_CAST_SPREAD_MAX)
                elif (cast_lv[0] == 0 and tick >= self._cast_rest_until
                      and want <= KT_BOSS_CAST_MAX_LEAN):
                    self._cast_start = tick
                    self._cast_end = tick + KT_BOSS_CAST_HOLD
            # Travel wins: if she sets off hard mid-pulse, the arms come down
            # and she leans into it, instead of sliding across in a cast.
            if want >= 2 and tick < self._cast_end:
                self._cast_end = tick

            hurt = game.phase == "victory" or (game.phase == "break"
                                               and game.phase_tick < KT_BOSS_HURT_TICKS)
            # The arms only rise once the body is within one depth of
            # upright; a pulse that starts while a lean is still walking down
            # waits the few ticks that takes, rather than popping two depths.
            cast_want = 3 if (tick < self._cast_end and not hurt
                              and (cast_lv[0] or self._lvl["lean"][0] <= 1)) else 0
            # Declaration: the card comes up across the declare and goes back
            # down on the far side of the flip.
            decl_want = 3 if (game.phase == "declare" and not hurt) else 0
            # Every upright pose straightens her: the cast, card and recoil rows
            # have no lean, so the lean is walked back to 0 underneath them and
            # walked out again afterwards -- through its in-betweens -- rather
            # than popping from a full tilt to upright and back.
            upright = hurt or cast_lv[0] or self._lvl["decl"][0]
            lean_want = 0 if upright else want

            # Nothing SHOWN changes faster than KT_BOSS_ROW_MIN ticks. Level
            # steps are already spaced, but two different actions can hand
            # over on consecutive ticks (the arms reach 0 and the lean steps
            # out the next tick), which flashed a one-tick idle between them.
            # The declaration's first step is exempt: it is cued on the beat.
            if tick - self._row_since >= KT_BOSS_ROW_MIN:
                was_cast = cast_lv[0]
                self._step_lvl("decl", decl_want, tick, KT_BOSS_DECL_UP, KT_BOSS_DECL_DOWN)
                self._step_lvl("cast", cast_want, tick, KT_BOSS_CAST_UP, KT_BOSS_CAST_DOWN)
                self._step_lvl("lean", lean_want, tick, KT_BOSS_LEAN_STEP, KT_BOSS_LEAN_STEP)
                if was_cast and not cast_lv[0]:
                    self._cast_rest_until = tick + KT_BOSS_CAST_REST
            elif decl_want and not self._lvl["decl"][0]:
                self._step_lvl("decl", decl_want, tick, KT_BOSS_DECL_UP, KT_BOSS_DECL_DOWN)

            # Row priority: recoil > card > cast > lean > hover.
            lean_lvl = self._lvl["lean"][0]
            cast_lvl = cast_lv[0]
            decl_lvl = self._lvl["decl"][0]
            if hurt:
                row = KT_BOSS_HURT
            elif decl_lvl:
                row = KT_BOSS_DECLARE[decl_lvl - 1]
            elif cast_lvl:
                row = KT_BOSS_CAST[cast_lvl - 1]
            elif lean_lvl and self._boss_face:
                row = (KT_BOSS_LEFT if self._boss_face < 0 else KT_BOSS_RIGHT)[lean_lvl - 1]
            else:
                row = KT_BOSS_IDLE
            if row != self._boss_row:
                self._boss_row = row
                self._row_since = tick

        def _step_lvl(self, name, want, tick, up, down):
            """Walk one pose level ONE depth toward `want`, at most once per
            `up` (rising) or `down` (falling) ticks. Stepping instead of
            jumping is the whole trick: every change of pose passes through
            the sheet's in-between rows on its way."""
            lv = self._lvl[name]
            if lv[0] == want:
                return
            if tick - lv[1] < (up if want > lv[0] else down):
                return
            lv[0] += 1 if want > lv[0] else -1
            lv[1] = tick

        def _fx_solid(self, color="#00000000"):
            """The child every shader quad is painted onto.

            Caching the SOLID rather than the Transform around it is what makes
            rebuilding those Transforms every frame cheap: gl2 turns a mesh
            Transform's child into a texture (load_all_textures ->
            render_to_texture), and a cached Solid hands back a cached texture
            instead of uploading a new one. The Transform itself is a handful of
            objects, which is the price of a level that can move every frame.
            """
            return self._misc(("fx_solid", color), lambda c=color: Solid(c))

        def _fx_targets(self, g):
            """Where every cosmetic level WANTS to be for the current phase.

            Pure function of simulation state -- no easing, no history. The
            envelope in _advance_fx_env is what actually walks toward these.
            """
            phase = g.phase
            if phase == "declare":
                ramp = kt_clamp(g.phase_tick / 30.0, 0.0, 1.0)
                c_px, c_a, c_spin = 220.0 + 110.0 * ramp, 0.40 + 0.42 * ramp, 1.7
                c_br = 0.020 + 0.022 * ramp
                # Slams in oversized, then settles onto the card size.
                sp_ = kt_clamp(g.phase_tick / 26.0, 0.0, 1.0)
                s_px, s_a = 330.0 - 120.0 * sp_, 0.85 * sp_
                v_a = 0.055 + 0.045 * kt_clamp(g.phase_tick / 40.0, 0.0, 1.0)
                dim, aura = 0x78, 1.0
            elif phase == "spell":
                c_px, c_a, c_spin, c_br = 322.0, 0.60, 1.0, 0.042
                s_px, s_a = 210.0, 0.34
                v_a, dim, aura = 0.10, 0x78, 1.0
            elif phase == "intro":
                ramp = kt_clamp((g.phase_tick - 60) / 80.0, 0.0, 1.0)
                c_px, c_a, c_spin, c_br = 258.0, 0.48 * ramp, 0.55, 0.026
                s_px, s_a = 210.0, 0.0
                v_a, dim, aura = 0.04, 0x55, ramp
            elif phase == "victory":
                fade = kt_clamp(1.0 - g.phase_tick / 90.0, 0.0, 1.0)
                c_px = 250.0 * (0.35 + 0.65 * fade)
                c_a, c_spin, c_br = 0.55 * fade, 2.4, 0.050
                s_px, s_a = 210.0, 0.0
                v_a, dim, aura = 0.04, 0x55, fade
            elif phase == "defeat":
                c_px, c_a, c_spin, c_br = 200.0, 0.0, 0.55, 0.022
                s_px, s_a = 210.0, 0.0
                v_a, dim, aura = 0.04, 0x55, 0.0
            else:  # nonspell / break
                c_px, c_a, c_spin, c_br = 228.0, 0.38, 0.55, 0.022
                s_px, s_a = 210.0, 0.0
                v_a, dim, aura = 0.055 if phase in ("nonspell", "break") else 0.04, 0x55, 1.0
            return (c_px, c_a, c_spin, c_br, s_px, s_a, v_a, dim, aura)

        def _advance_fx_env(self, g):
            """One simulation tick of the cosmetic FX envelope.

            Guarded and catch-up-aware exactly like _advance_boss_anim: a
            duplicate render() in the same tick must not double-step it, pause
            must freeze it, and a frame that ran several sim ticks has to move
            the envelope by all of them or the levels lag behind the fight.

            An ease applied n times in a row is not the ease applied once, so
            the closed form 1 - (1 - rate) ** n is what makes a catch-up frame
            land where sixty separate frames would have.
            """
            steps = g.tick - self._fx_tick
            if steps <= 0:
                return
            steps = min(steps, KT_MAX_CATCHUP)
            self._fx_tick = g.tick

            def ease(cur, target, rate):
                k = 1.0 - (1.0 - rate) ** steps
                return cur + (target - cur) * k

            (c_px, c_a, c_spin, c_br,
             s_px, s_a, v_a, dim, aura) = self._fx_targets(g)

            # Levels: attack fast, release slow. Sizes and spin ease at one rate
            # both ways -- a size that lagged on the way out would read as the
            # sigil being dragged rather than dimming.
            self._fx_circle_a = ease(self._fx_circle_a, c_a,
                KT_FX_ATTACK if c_a > self._fx_circle_a else KT_FX_RELEASE)
            self._fx_seal_a = ease(self._fx_seal_a, s_a,
                KT_FX_SEAL_ATTACK if s_a > self._fx_seal_a else KT_FX_SEAL_RELEASE)
            self._fx_veil_a = ease(self._fx_veil_a, v_a,
                KT_FX_ATTACK if v_a > self._fx_veil_a else KT_FX_RELEASE)
            self._fx_aura_a = ease(self._fx_aura_a, aura,
                KT_FX_ATTACK if aura > self._fx_aura_a else KT_FX_RELEASE)
            self._fx_circle_px = ease(self._fx_circle_px, c_px, KT_FX_SIZE_EASE)
            self._fx_circle_breath = ease(self._fx_circle_breath, c_br, KT_FX_SIZE_EASE)
            self._fx_circle_spin = ease(self._fx_circle_spin, c_spin, KT_FX_SIZE_EASE)
            self._fx_dim = ease(self._fx_dim, float(dim), KT_FX_DIM_EASE)

            # The seal's SIZE is taken straight, with no ease at all. It is not
            # a level -- it is the authored slam, 330px down to 210px across 26
            # ticks, and an envelope chasing a target that is itself already
            # falling never reaches the top of it: eased at 0.14 the seal peaked
            # near 260px and the "thrown down oversized" gesture just stopped
            # happening. Its size never hard-cuts anyway (every non-declare
            # phase targets the same 210), so there is nothing here to smooth.
            # The ALPHA envelope is what carries this layer's fades.
            self._fx_seal_px = s_px

            # Focus sigil: its own, much faster envelope. This one answers a key
            # the player is holding, so it has to feel instant while still not
            # being a hard on/off.
            f_t = 1.0 if g.focus else 0.0
            self._fx_focus_a = ease(self._fx_focus_a, f_t,
                KT_FX_FOCUS_ATTACK if f_t > self._fx_focus_a else KT_FX_FOCUS_RELEASE)
            # The options glide between their two stances at one rate.
            self._fx_opt = ease(self._fx_opt, f_t, 0.24)
            # The spell background comes up across the declaration (it is
            # fully in by the time the ribbon shuts) and holds for the card;
            # its STYLE is latched like the seal's drawing, re-read only while
            # it is dark, so a background never switches pattern mid-fade.
            if g.phase == "declare":
                b_t = kt_clamp(g.phase_tick / float(KT_DECL_CLOSE), 0.0, 1.0)
            elif g.phase == "spell":
                b_t = 1.0
            else:
                b_t = 0.0
            self._fx_sbg_a = ease(self._fx_sbg_a, b_t,
                KT_FX_ATTACK if b_t > self._fx_sbg_a else KT_FX_RELEASE * 0.6)
            if self._fx_sbg_a < 0.02:
                self._fx_sbg_style = KT_SPELL_BG[g.sp_pat % len(KT_SPELL_BG)]
            # The life ring is up while she has a bar to lose.
            r_t = 1.0 if g.phase in ("nonspell", "declare", "spell") else 0.0
            self._fx_ring_a = ease(self._fx_ring_a, r_t,
                KT_FX_ATTACK if r_t > self._fx_ring_a else KT_FX_RELEASE)

            # Card colour crossfades across the WHOLE stage (circle, veil,
            # aura), so a new bar bleeds into its palette instead of the arena
            # changing colour between two frames. The seal cannot join in -- it
            # is a different drawing per card, not a tint -- which is exactly
            # why its alpha envelope has to carry the swap instead.
            tgt = Color(KT_PAL[g.cur_color]).rgb
            for i in range(3):
                self._fx_col[i] = ease(self._fx_col[i], tgt[i], KT_FX_COL_EASE)

            # WHICH seal is latched, and only re-read while the ink is
            # effectively gone. Every card has its own drawing, so it cannot
            # crossfade -- and sp_pat moves to the next card the moment a bar
            # ends, which would swap the sigil to a different drawing halfway
            # through its own fade-out. There is a whole nonspell between one
            # card's fade and the next one's slam, so this always re-latches
            # in time.
            if self._fx_seal_a < 0.02:
                self._fx_seal_idx = g.sp_pat

        def _boss_frame(self, game):
            """(row, col) of the sheet cell to draw this tick.

            The row is the pose _advance_boss_anim picked. The column is the
            shared secondary-motion loop and nothing else: it runs off the sim
            clock in every pose, so a held pose keeps its hair and sleeves
            moving, and a change of pose never jumps the loop.
            """
            if game.tick != self._boss_motion_tick:
                self._advance_boss_anim(game)
            col = (game.tick // KT_BOSS_PHASE_TICKS) % KT_BOSS_PHASES
            return self._boss_row, col

        def _boss_tf(self, variant, row, col, **props):
            """Cached boss Transform (see _boss_cache)."""
            key = (variant, row, col)
            d = KTStage._boss_cache.get(key)
            if d is None:
                if len(KTStage._boss_cache) > 800:
                    KTStage._boss_cache.clear()
                d = Transform(KT_BOSS_FRAMES[row][col], nearest=True,
                              subpixel=True, **props)
                KTStage._boss_cache[key] = d
            return d

        # ----- render --------------------------------------------------------

        def render(self, width, height, st, at):
            g = self.game

            # F3 profiler (perf.rpy). One attribute read when it is off, which
            # is what leaving the instrumentation in shipping code costs.
            _perf = MSBF_PERF.on
            _t = msbf_perf_t0() if _perf else 0.0

            # LOW DETAIL (Settings > Graphics > Effects Detail; see
            # graphics_detail.rpy). Read once per frame. This stage is
            # CPU-bound -- every blit below is python -- so Low cuts BLITS of
            # pure decoration: the veil's rays, the ambient motes, her travel
            # afterimages, the soul's dash ghosts and the spawn rings go, and
            # sparks and bullet-cancel stars are thinned. Every bullet, laser,
            # telegraph, seal, ring and readout draws exactly as on Full.
            low = enter_m_low_detail()

            # Fixed-timestep simulation: st is wall time; clamp big jumps (a
            # dropped frame, the pause overlay) and never run more than
            # KT_MAX_CATCHUP ticks in one frame.
            #
            # Why this accumulator exists:
            #   render() can be called at uneven wall-clock intervals, but the
            #   game should still advance in exact 1/60s slices. acc stores
            #   leftover fractional time until enough has accumulated for
            #   another simulation tick. KT_MAX_CATCHUP prevents one long hitch
            #   from running dozens of gameplay ticks in a single render call.
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
                while self.acc >= KT_TICK and steps < KT_MAX_CATCHUP:
                    g.step()
                    self.acc -= KT_TICK
                    steps += 1
                if steps >= KT_MAX_CATCHUP:
                    self.acc = 0.0

            if _perf:
                msbf_perf_t1("sim", _t)
                MSBF_PERF.note("bullets", len(g.bullets))
                MSBF_PERF.note("sparks", len(g.sparks))
                _t = msbf_perf_t0()

            rv = renpy.Render(1280, 720)

            # Per-frame texture memo: each distinct cached displayable is
            # rendered AT MOST once per frame, then blitted many times.
            # This is the safe place to keep renpy.Render objects because the
            # dict dies when render() returns.
            frame_tex = {}

            def tex(key, disp, w=128, h=128):
                # Render displayable -> (Render, size) for this frame. Every
                # draw section below should go through tex() unless it needs a
                # one-off shader quad with uniforms that change every frame.
                entry = frame_tex.get(key)
                if entry is None:
                    r = renpy.render(disp, w, h, st, at)
                    rv.depends_on(r)
                    entry = (r, r.get_size())
                    frame_tex[key] = entry
                return entry

            def rect(color, w, h):
                # Solid rectangle cache used for masks, flashes, HP bars, and
                # overlays. Returning a Render directly keeps callsites compact;
                # unlike tex(), the size is already known from w/h.
                w = max(1, int(w))
                h = max(1, int(h))
                key = ("rect", color, w, h)
                entry = frame_tex.get(key)
                if entry is None:
                    solid = self._misc(("solid", color), lambda: Solid(color))
                    r = renpy.render(solid, w, h, st, at)
                    rv.depends_on(r)
                    entry = r
                    frame_tex[key] = entry
                return entry

            # --- SCREEN-SPACE CHROME (was the fight screen's own displayables) --
            # The backdrop, the four panel masks and the cabinet trim used to be
            # `add` statements in kototouhou_screen. They live here now for one
            # reason: the backdrop's slow breathing zoom was an ATL loop, and an
            # ATL interpolation asks for its next frame with a delay of ZERO --
            # so the fight screen was requesting frames at the panel's full
            # refresh rate for the entire run, straight past the draw-rate
            # governor at the bottom of this method. Everything that moves is in
            # here now, and the screen is inert; see the KT_BREATHE_* note up
            # top. Cost of the move: ~20 solid blits a frame, which is noise.
            #
            # Two 9-second eases back to back are a raised cosine, so this is the
            # same curve the ATL drew -- just clocked off g.tick (freezing under
            # pause with the rest of the fight) and quantized so the zoomed
            # backdrop is one cached texture per step instead of one per frame.
            bd_w = 0.5 * (1.0 - math.cos(g.tick * (2.0 * math.pi / KT_BREATHE_PERIOD)))
            bd_step = int(bd_w * (KT_BREATHE_STEPS - 0.001))
            bd_key = ("backdrop", g.endless, bd_step)
            bd_d = self._misc(bd_key, (lambda e=g.endless, k=bd_step: Transform(
                KT_DIR + ("endless.png" if e else "kotobackdrop.png"),
                zoom=1.0 + KT_BREATHE_AMOUNT * k / float(KT_BREATHE_STEPS - 1),
                subpixel=True)))
            bdr, (bdw, bdh) = tex(bd_key, bd_d, 1280, 720)
            rv.subpixel_blit(bdr, (640.0 - bdw / 2.0, 360.0 - bdh / 2.0))

            # Panel masks around the playfield.
            rv.blit(rect("#02040bd9", KT_SX, 720), (0, 0))
            rv.blit(rect("#02040bd9", 1280 - KT_SX - KT_W, 720), (KT_SX + KT_W, 0))
            rv.blit(rect("#02040bd9", KT_W, KT_SY), (KT_SX, 0))
            rv.blit(rect("#02040bd9", KT_W, 720 - KT_SY - KT_H), (KT_SX, KT_SY + KT_H))

            # Stage chrome: one pre-drawn overlay (kt_frame.png) -- a glowing
            # double border round the playfield, a rosette on each corner, the
            # margins written in the seals' invented script, and the score
            # panel's divider. Transparent inside the field, so it can never
            # sit on the fight. It replaced sixteen hand-placed trim rects.
            frr, (_frw, _frh) = tex("frame", self._art(
                "kt_frame", "frame", add=False), 1280, 720)
            rv.blit(frr, (0, 0))

            stage = renpy.Render(KT_W, KT_H)
            sblit = stage.subpixel_blit

            # Draw order is intentional:
            #   background dim -> boss/aura -> player shots -> sparks -> enemy
            #   bullets -> bomb/death/player/focus -> darkness -> HUD/overlays.
            # In particular, enemy bullets draw above player shots, and the
            # spell-5 darkness draws after the player so it darkens the whole
            # playfield through one shader pass.

            # Advance every cosmetic level ONE simulation tick before anything
            # reads one. Must happen here, above the first draw, because the
            # stage dim right below is already an envelope consumer.
            self._advance_fx_env(g)
            fx_col = tuple(self._fx_col)

            # Stage dim so danmaku pops against the shrine backdrop; deeper
            # during spell cards, Touhou-style -- and it CROSSFADES between the
            # two, because a full-screen dim snapping 0x55 -> 0x78 on the tick a
            # card is declared is the most visible hard cut on the stage.
            # Quantized to the alpha byte, which is as fine as a hex colour goes
            # and still finer than one step per tick, so rect()'s Solid cache
            # tops out at the ~36 values between the two levels.
            stage.blit(rect("#000000%02x" % int(self._fx_dim + 0.5), KT_W, KT_H), (0, 0))

            # --- koto.spellbg: the spell card's own backdrop -------------------
            # Right over the dim, under everything else: the room changes when
            # a card is read (see KT_SPELL_BG). Built fresh each frame like the
            # veil -- the quad never changes size, so the cached Solid carries
            # the texture and only the uniforms move.
            if KT_SHADER_OK and self._fx_sbg_a > 0.004:
                sbg_d = Transform(
                    self._fx_solid(), xysize=(KT_W, KT_H), shader="koto.spellbg",
                    mesh=True, u_koto_col=fx_col, u_koto_alpha=self._fx_sbg_a,
                    u_koto_style=float(self._fx_sbg_style),
                    u_koto_res=(float(KT_W), float(KT_H)))
                try:
                    sbr, _sbsz = tex(("spellbg",), sbg_d, KT_W, KT_H)
                    stage.blit(sbr, (0, 0))
                except Exception:
                    pass

            # --- koto.veil: the living backdrop -------------------------------
            # One GPU quad of slow rays + ripples in the card colour, right on
            # top of the dim so everything else still draws over it. Alpha is
            # phase-staged: barely-there in a nonspell, a touch louder under a
            # card, swelling through the declare.
            if KT_SHADER_OK and self._fx_veil_a > 0.002 and not low:
                # Alpha and colour both come off the envelope, so the veil
                # swells through a declare and bleeds into the next card's
                # palette instead of switching. u_time is a DRAW-time uniform
                # (gl2shader.pyx fills it from interface.frame_time), so the
                # ray/ripple motion is on the GPU either way.
                #
                # Built fresh rather than cached, like the spell circle and the
                # seal: the quad's PIXEL SIZE never changes, so the only cached
                # thing that matters -- the Solid's texture -- is still cached,
                # and what a cache key would buy here is a staircase in the one
                # value the eye is watching.
                veil_d = Transform(
                    self._fx_solid(), xysize=(KT_W, KT_H), shader="koto.veil",
                    mesh=True, u_koto_col=fx_col, u_koto_alpha=self._fx_veil_a)
                try:
                    vlr, _vsz = tex(("veil",), veil_d, KT_W, KT_H)
                    stage.blit(vlr, (0, 0))
                except Exception:
                    pass

            # --- ambient atmosphere motes (backmost gameplay layer) -----------
            # A soft, ever-present drift of light over the shrine so the arena
            # reads as a living place, not just bullets on a flat picture. Motes
            # twinkle (3 alpha buckets) and come in two sizes; the big ones use
            # the petal sprite. Cheap: fixed pool, few cached textures.
            # Frame memo first, exactly as the bullet loop does it: the whole
            # pool collapses onto a dozen textures, so the common case should
            # cost one dict get -- not a lambda allocation, a _misc lookup and a
            # tex() call per mote, every mote, every frame.
            # Small ones are bokeh (out-of-focus lights in the air); the few big
            # ones are petals, turning slowly as they rise. A petal's heading
            # is its POOL INDEX plus the tick, never its twinkle phase (which
            # moves every tick and would flick it between headings), turned in
            # 12-degree steps. Petals do not twinkle and keep one size, so a
            # petal key is (colour, heading) alone: the pool's four petal
            # colours x 30 headings is 120 textures at most, which keeps them
            # well clear of _misc's 1200-key wipe.
            for mi, m in (() if low else enumerate(g.ambient)):
                bg = m["big"]
                if bg:
                    ab = pb = ((g.tick // 12) + mi * 5) % 30
                    akey = ("amb_p", m["ci"], pb)
                else:
                    ab = int((0.5 + 0.5 * math.sin(m["ph"])) * 2.999)
                    akey = ("amb", m["ci"], ab, m["scb"])
                got = frame_tex.get(akey)
                if got is None:
                    if bg:
                        amb_d = self._art("kt_fx", "petal:%d" % m["ci"], zoom=0.9,
                                          alpha=0.28, rotate=ab * 12.0)
                    else:
                        amb_d = self._art("kt_fx", "mote:%d" % m["ci"],
                                          zoom=0.46 * (0.7 + 0.4 * m["scb"]),
                                          alpha=0.12 + 0.11 * ab)
                    got = tex(akey, amb_d, 48, 48)
                amr_, (amw_, amh_) = got
                sblit(amr_, (m["x"] - amw_ / 2.0, m["y"] - amh_ / 2.0))

            # --- Seer gaps (border portals) ------------------------------------
            # Each gap is the seam sprite -- a tall slit of light, hot along its
            # centre line -- drawn additively, stood perpendicular to the
            # emission direction (the art is vertical, so an emission straight
            # right is rotation 0), with a flare where the bullets pour out.
            # Alpha fades in over the first beats and back out over the last,
            # bucketed x3 so the texture cache stays tiny.
            for p in g.portals:
                page = g.tick - p["born"]
                if page < 0 or page >= p["ttl"]:
                    continue
                if page < 15:
                    ab3 = min(2, page // 5)
                elif p["ttl"] - page < 42:
                    ab3 = max(0, (p["ttl"] - page) // 14)
                else:
                    ab3 = 2
                bkt = int(round(math.degrees(p["ang"]) / 15.0)) % 24
                pkey3 = ("portal", p["ci"], bkt, ab3)
                prr, (prw, prh) = tex(pkey3, self._art(
                    "kt_fx", "portal:%d" % p["ci"], zoom=1.25,
                    alpha=0.34 + 0.30 * ab3, rotate=bkt * 15.0), 200, 200)
                sblit(prr, (p["x"] - prw / 2.0, p["y"] - prh / 2.0))
                ckey3 = ("portalf", p["ci"], ab3)
                crr, (crw, crh) = tex(ckey3, self._art(
                    "kt_fx", "flare:%d" % p["ci"], zoom=0.8,
                    alpha=0.20 + 0.16 * ab3), 64, 64)
                sblit(crr, (p["x"] - crw / 2.0, p["y"] - crh / 2.0))

            # Bar-7 card (sp_pat 6): the room goes red. Every OTHER spell card
            # instead gets a subtler card-colour edge glow so the stage feels
            # themed to whichever mask is being read. Two nested strips per edge
            # fake a soft falloff (kept low-alpha to protect bullet clarity).
            if g.phase == "spell" and g.sp_pat == 6:
                pulse = 0.5 + 0.5 * math.sin(g.tick * 0.05)
                stage.blit(rect("#ff203819" if pulse < 0.5 else "#ff203828", KT_W, KT_H), (0, 0))
            elif g.phase == "spell":
                gp = 0.5 + 0.5 * math.sin(g.tick * 0.045)
                base = KT_PAL[g.cur_color]
                for depth, peak in ((40, 9), (16, 18)):
                    ea = int(peak + peak * gp)
                    ec = base + ("%02x" % min(255, ea))
                    stage.blit(rect(ec, KT_W, depth), (0, 0))
                    stage.blit(rect(ec, KT_W, depth), (0, KT_H - depth))
                    stage.blit(rect(ec, depth, KT_H), (0, 0))
                    stage.blit(rect(ec, depth, KT_H), (KT_W - depth, 0))

            # --- boss (spell circle, aura, phantom, trail, sprite) ------------
            # Card presentation (accent colour + name) comes from g.cur_* so
            # endless's randomised waves render right; a normal fight fills these
            # straight from KT_BARS, so this is identical there. Wrapped as `bar`
            # so the draws below keep their KT_BARS-style field access.
            bar = {"color": g.cur_color, "card": g.cur_card}
            # Victory cinematic: she shakes harder as the detonations land,
            # flickering white, until the final boom at tick 96 takes her off
            # the stage entirely.
            vt = g.phase_tick if g.phase == "victory" else -1
            boss_on = g.phase not in ("defeat",) and g.by > -70.0 and vt < 96
            # The float: a slow tick-driven figure-8 (x at half the y frequency)
            # so she drifts on the air instead of bobbing on a string. Tick-based
            # so the pause overlay freezes her with the rest of the sim.
            tb = g.tick
            bob = math.sin(tb * 0.035) * 4.5
            bobx = math.sin(tb * 0.0175) * 3.5
            shake_x = 0.0
            if 0 <= vt < 96:
                amp = 2.0 + vt * 0.11
                shake_x = math.sin(g.tick * 1.9) * amp
                bob += math.cos(g.tick * 2.7) * amp * 0.5
            bx_draw = g.bx + bobx + shake_x
            by_draw = g.by + bob
            boss_row, boss_col = self._boss_frame(g)
            if boss_on:
                # Spell circle: her float anchor. Small and slow while a
                # nonspell runs, flaring open through the declare, wide and
                # bright under a spell card, collapsing during the victory
                # detonations. One shader quad per frame.
                if KT_SHADER_OK and self._fx_circle_a > 0.004:
                    # Size, alpha, breath depth, spin rate and colour ALL come
                    # off the envelope, so the circle grows and brightens into a
                    # declaration and settles out of it rather than teleporting
                    # between five authored constants.
                    #
                    # The quad is a fixed KT_FX_CIRCLE_QUAD square and the size
                    # rides u_koto_scale. That is the whole trick: the previous
                    # pass sized the QUAD, and quad size is a cache key, so the
                    # size could only ever land on 4px steps -- five discrete
                    # sizes cycling under a spell card. A uniform has no steps.
                    # Nothing about the picture changes: dividing r scales band
                    # widths with everything else, so this is what sizing the
                    # quad drew, minus the snapping.
                    q = KT_FX_CIRCLE_QUAD
                    circ_d = Transform(
                        self._fx_solid(), xysize=(q, q), shader="koto.circle",
                        mesh=True, u_koto_col=fx_col,
                        u_koto_alpha=self._fx_circle_a,
                        u_koto_spin=self._fx_circle_spin,
                        u_koto_breath=self._fx_circle_breath,
                        u_koto_scale=self._fx_circle_px / float(q))
                    try:
                        ccr, (ccw, cch) = tex(("circle",), circ_d, q, q)
                        sblit(ccr, (bx_draw - ccw / 2.0, by_draw - cch / 2.0))
                    except Exception:
                        pass
                # Summoning seal: this card's own magic circle (each one drawn
                # for its card by the art generator -- the knives of Nice Boat,
                # the clock of unread mail, Justice's six chambers), slammed
                # down UNDER her on the declare and held, turning, for the rest
                # of the card. The shader circle above is the moving light;
                # this is the ink it is drawn on.
                # Level and size are the envelope's (the slam ramp itself lives
                # in _fx_targets); only the spin is computed here.
                seal_a = self._fx_seal_a
                seal_px = self._fx_seal_px
                seal_rot = 0.0
                if g.phase == "declare":
                    sp_ = kt_clamp(g.phase_tick / 26.0, 0.0, 1.0)
                    # Slam-spin: 150 degrees of extra turn bled off on a cubic
                    # ease, so she reads as having THROWN it down rather than
                    # faded it in. The offset reaches exactly zero as the slam
                    # ends, which is what lets the steady spin below carry
                    # straight through the declare -> spell handover without a
                    # jump when phase_tick resets.
                    seal_rot = -150.0 * (1.0 - sp_) ** 3
                if seal_a > 0.004:
                    # Steady counter-rotation, keyed to g.tick (not phase_tick,
                    # not st) so it freezes with the rest of the sim under the
                    # pause overlay. It turns AGAINST the shader circle's dashed
                    # band above it: two rings going opposite ways read as one
                    # mechanism, where two going the same way read as one decal
                    # with a slipping texture.
                    seal_rot += tb * KT_SEAL_SPIN
                    # Breath, deliberately off-rate and out of phase with the
                    # shader's, so the ink and the light are never caught doing
                    # the same thing at the same moment.
                    seal_px *= 1.0 + 0.035 * math.sin(tb * 0.031 + 1.1)
                    seal_cell = "seal:%d" % self._fx_seal_idx
                    # NOT cached, and that is the point. This used to quantize
                    # zoom to 1/8ths and alpha to 8 steps, which put the entire
                    # breathing pulse inside TWO zoom buckets: it snapped
                    # between two sizes forever instead of moving. Bucketing
                    # rotation finely enough to look smooth would mint hundreds
                    # of entries per card and trip _misc_cache's 1200-key wipe,
                    # which is a far worse hitch than this costs. One Transform
                    # allocation a frame, for one sprite -- and mark_sweep()
                    # reaps its render at the end of the frame either way, so
                    # caching the displayable was only ever saving that alloc.
                    # Drawn as light: the seal is glowing line-work, and added
                    # over the dimmed stage it reads as lit ink rather than as
                    # a decal stuck on top of the fight.
                    seal_d = Transform(
                        kt_art("kt_seals", seal_cell), zoom=seal_px / KT_SEAL_PX,
                        rotate=seal_rot, subpixel=True, alpha=seal_a,
                        additive=1.0)
                    try:
                        # rotate_pad is left on (default) so the corners are
                        # never sheared off; it grows the render to the child's
                        # diagonal, so the offer has to clear 330 * sqrt(2) for
                        # the hexagram's slam frame.
                        sr_, (sw_, sh_) = tex(("seal",), seal_d, 560, 560)
                        sblit(sr_, (bx_draw - sw_ / 2.0, by_draw - sh_ / 2.0))
                    except Exception:
                        pass
                if MSBF_FX_SHADERS and self._fx_aura_a > 0.004:
                    # Aura: the soft card-colour bloom she floats in. This used
                    # to quantize its sine into FOUR intensity buckets, which is
                    # a four-step staircase in the one thing on screen whose
                    # whole job is to be a smooth glow. It is continuous now.
                    # The 190px quad never resizes (so no texture is
                    # reallocated) -- the halo appears to breathe because
                    # u_softness moves the falloff exponent instead: a lower
                    # exponent spreads the same core wider.
                    apulse = 0.5 + 0.5 * math.sin(g.tick * 0.040)
                    aswell = 0.5 + 0.5 * math.sin(g.tick * 0.023 + 2.3)
                    aura = Transform(
                        self._fx_solid(), xysize=(190, 190), shader="msbf.glow",
                        mesh=True,
                        u_color=fx_col,
                        u_intensity=(0.42 + 0.39 * apulse) * self._fx_aura_a,
                        u_softness=2.25 - 0.55 * aswell)
                    try:
                        ar, (aw, ah) = tex(("aura",), aura, 190, 190)
                        sblit(ar, (bx_draw - aw / 2.0, by_draw - ah / 2.0))
                    except Exception:
                        pass
                if g.mirror_on:
                    if g.cur_special == "you":
                        # Mask of You: the phantom is YOUR soul, point-reflected
                        # through the stage centre (so it hangs upside down),
                        # bleached -- the reader has no colour of their own.
                        phantom = self._misc("you_phantom", lambda: Transform(
                            kt_art("kt_player", "soul_hot"), xzoom=-KT_SOUL_ZOOM,
                            yzoom=-KT_SOUL_ZOOM, alpha=0.5, subpixel=True))
                        pr, (pw, ph_) = tex("you_phantom", phantom, 64, 64)
                        sblit(pr, (KT_W - g.px - pw / 2.0, KT_H - g.py - ph_ / 2.0))
                    else:
                        phantom = self._boss_tf(
                            "phantom", boss_row, boss_col, xzoom=-KT_BOSS_ZOOM,
                            yzoom=KT_BOSS_ZOOM, alpha=0.5)
                        pr, (pw, ph_) = tex(("boss_phantom", boss_row, boss_col),
                                            phantom, 220, 220)
                        sblit(pr, (KT_W - g.bx - pw / 2.0, by_draw - ph_ / 2.0))
                # Travel afterimages: when a dart/sweep move actually carries
                # her, two fading ghosts trail the motion so the reposition
                # reads as flight, not a teleport-ish slide.
                if g.tick - self._trail_tick >= 3 and not g.paused:
                    # Sample only every 3 ticks so the trail is short and cheap.
                    self._trail_tick = g.tick
                    self.trail.append((bx_draw, by_draw))
                    if len(self.trail) > 3:
                        del self.trail[0]
                if self.trail and not low:
                    t0x, t0y = self.trail[0]
                    # Do not draw ghosts while she is merely bobbing in place;
                    # require actual travel distance.
                    if abs(bx_draw - t0x) + abs(by_draw - t0y) > 11.0:
                        ghost = self._boss_tf("ghost", boss_row, boss_col,
                                              zoom=KT_BOSS_ZOOM, alpha=0.16)
                        gr_, (gw_, gh_) = tex(("boss_ghost", boss_row, boss_col),
                                              ghost, 220, 220)
                        for gx, gy in self.trail[:-1]:
                            sblit(gr_, (gx - gw_ / 2.0, gy - gh_ / 2.0))
                # The sheet's lean rows supply the bank. Keeping the sprite
                # axis-aligned (and at an integer zoom) protects its pixel
                # clusters; rotating pixel art just re-samples it into mush.
                #
                # HIT FEEDBACK IS A GLINT, NOT A WHITEOUT. She used to blow out
                # to a white silhouette for 3 ticks on every hit, and with a
                # volley landing every 5 ticks that is most of the fight spent
                # as a white shape -- the old-game read this mode is leaving.
                # A hit now lays her own sprite back over her ADDITIVELY at low
                # alpha: she brightens without losing her colours. The hard
                # flicker is kept for the victory detonations, where it is the
                # point.
                vflash = vt >= 0 and (g.tick // 3) % 2 == 0
                if vflash:
                    boss_d = self._boss_tf("flash", boss_row, boss_col,
                                           zoom=KT_BOSS_ZOOM,
                                           matrixcolor=BrightnessMatrix(0.55))
                else:
                    boss_d = self._boss_tf("plain", boss_row, boss_col,
                                           zoom=KT_BOSS_ZOOM)
                br, (bw, bh) = tex(("boss", boss_row, boss_col, vflash), boss_d, 220, 220)
                sblit(br, (bx_draw - bw / 2.0, by_draw - bh / 2.0))
                # LIFE RING. The chip ghost is advanced here (it used to live
                # with the flat top bar) -- per render, which is per tick
                # because the draw rate is the tick rate (see the governor at
                # the bottom of render()). It snaps UP instantly on a new bar.
                hp_frac = kt_clamp(g.boss_hp / g.boss_hp_max, 0.0, 1.0)
                if hp_frac > self._hp_ghost:
                    self._hp_ghost = hp_frac
                else:
                    self._hp_ghost += (hp_frac - self._hp_ghost) * 0.06
                if KT_SHADER_OK and self._fx_ring_a > 0.004:
                    lq_ = KT_LIFE_RING_QUAD
                    ring_l = Transform(
                        self._fx_solid(), xysize=(lq_, lq_), shader="koto.lifering",
                        mesh=True, u_koto_col=fx_col, u_koto_fill=hp_frac,
                        u_koto_ghost=self._hp_ghost,
                        u_koto_split=0.5 if g.phase == "nonspell" else -1.0,
                        u_koto_alpha=self._fx_ring_a)
                    try:
                        lrr, (lrw, lrh) = tex(("lifering",), ring_l, lq_, lq_)
                        sblit(lrr, (bx_draw - lrw / 2.0, by_draw + 4.0 - lrh / 2.0))
                    except Exception:
                        pass
                if g.boss_flash > 0 and not vflash:
                    # 0.16: her art is pale already, and she is under fire
                    # for most of a card -- at 0.30 she read as washed out.
                    hit_d = self._boss_tf("hit", boss_row, boss_col,
                                          zoom=KT_BOSS_ZOOM, additive=1.0, alpha=0.16)
                    hr4, (hw4, hh4) = tex(("boss_hit", boss_row, boss_col), hit_d, 220, 220)
                    sblit(hr4, (bx_draw - hw4 / 2.0, by_draw - hh4 / 2.0))

                # Muzzle bloom: a bright flare at Kotonoha for ~7 ticks after
                # each fire cue (set in _se), so every volley reads as HER
                # casting. A card-colour bloom under a white heart, both
                # additive and fading; keyed on a strength bucket so the cache
                # stays tiny.
                mz = g.tick - g.muzzle
                if 0 <= mz < 7:
                    mf = int((1.0 - mz / 7.0) * 3.999)      # 0..3 fade bucket
                    sb = 1 if g.muzzle_str >= 0.9 else 0
                    mscale = 0.8 + 0.4 * sb
                    mhr, (mhw, mhh) = tex(("muzzle_h", g.cur_color, mf, sb), self._art(
                        "kt_fx", "flare:%d" % g.cur_color, zoom=(1.2 + 0.45 * mf) * mscale,
                        alpha=0.30 + 0.16 * mf), 160, 160)
                    sblit(mhr, (bx_draw - mhw / 2.0, by_draw - mhh / 2.0))
                    mcr, (mcw, mch) = tex(("muzzle_c", mf, sb), self._art(
                        "kt_fx", "flare:13", zoom=(0.45 + 0.22 * mf) * mscale,
                        alpha=0.36 + 0.18 * mf), 80, 80)
                    sblit(mcr, (bx_draw - mcw / 2.0, by_draw - mch / 2.0))

            # --- player shots (under enemy bullets) ---------------------------
            # Needles of light, drawn additively so a stream of them reads as a
            # beam of the reader's own colour rather than a column of pellets.
            # The unfocused spread leans with its heading (three headings, so
            # three textures); the focused pair is a longer, whiter needle.
            for s in g.shots:
                lean = 0 if s["vx"] == 0.0 else (1 if s["vx"] > 0.0 else -1)
                foc = s.get("f", False)
                skey2 = ("pshot", foc, lean)
                got = frame_tex.get(skey2)
                if got is None:
                    got = tex(skey2, self._art(
                        "kt_player", "shot_focus" if foc else "shot",
                        alpha=0.9, rotate=(lean * 7.45) if lean else None), 64, 64)
                sr, (sw, sh) = got
                sblit(sr, (s["x"] - sw / 2.0, s["y"] - sh / 2.0))

            # --- sparkles ------------------------------------------------------
            # Up to KT_MAX_SPARKS of these on a bomb frame, across at most
            # 15 colours x 3 fade steps of texture -- so, like the bullets and
            # the motes, the frame memo is checked before anything is built.
            # Additive motes of light with a faint four-point glint.
            # Low thins by a STABLE key (a hash of the dict's identity), never
            # by list position: sparks die out of the middle of the list, so an
            # index stride would hand the "drawn" half to different sparks
            # every frame and the field would flicker. (Hashed, because raw
            # ids are allocator-aligned and their low bits barely move.)
            for s in ([s_ for s_ in g.sparks if not ((id(s_) * 2654435761) >> 21) & 1] if low else g.sparks):
                frac = s["age"] / float(s["ttl"])
                # ab is a 3-step fade bucket. Like every other visual bucket in
                # this renderer, fewer alpha states means more texture reuse.
                ab = 2 - min(2, int(frac * 3.0))
                skey = ("spark", s["ci"], ab)
                got = frame_tex.get(skey)
                if got is None:
                    got = tex(skey, self._art("kt_fx", "spark:%d" % s["ci"],
                                              alpha=0.40 + 0.28 * ab), 32, 32)
                spr, (spw, sph) = got
                sblit(spr, (s["x"] - spw / 2.0, s["y"] - sph / 2.0))

            # --- bullet cancels -------------------------------------------------
            # A cleared bullet leaves a small star of its own colour that lifts,
            # hangs, and is then drawn into the soul (KTGame._update_cancels;
            # purely cosmetic -- the clear was already scored). The modern read
            # of a bomb or a bar break: the field does not just vanish, it
            # POURS into you. Two twinkle frames x three fade steps per colour.
            for c in ([c_ for c_ in g.cancels if ((id(c_) * 2654435761) >> 21) % 3 == 0] if low else g.cancels):
                ca = c["age"]
                ab = 2 if ca < KT_CANCEL_TTL - 30 else (1 if ca < KT_CANCEL_TTL - 12 else 0)
                tw = ((ca // 3) + c["ph"]) % 2
                ckey4 = ("cancel", c["ci"], ab, tw)
                got = frame_tex.get(ckey4)
                if got is None:
                    got = tex(ckey4, self._art("kt_fx", "cancel:%d" % c["ci"],
                                               zoom=0.9 if tw else 0.72,
                                               alpha=0.35 + 0.27 * ab), 32, 32)
                cnr, (cnw, cnh) = got
                sblit(cnr, (c["x"] - cnw / 2.0, c["y"] - cnh / 2.0))

            # --- lasers (UNDER the bullets, so a bullet on a beam stays read) -
            # Each beam is this mode's own beam body (kt_lasers.png: a white-hot
            # core in a coloured body in a soft glow, 256 long), stretched to
            # length, rotated into place and drawn as LIGHT. Four frames of
            # striations flow along it while it burns.
            #
            # BUILT FRESH EVERY FRAME, NOT CACHED. A beam's width swells through
            # its telegraph, throbs while it burns and collapses as it fades,
            # and with the flow frames on top a cached beam minted hundreds of
            # keys per broadside -- enough to trip _misc's wipe mid-card. There
            # are rarely more than a couple on the stage and the texture is the
            # shared beam atlas either way, so a fresh Transform per beam per frame
            # is the cheap option, and it lets width and fade move continuously
            # instead of in whole-pixel steps. The ANGLE stays bucketed: it is
            # what the art is rotated by, and 6 degrees is invisible on a beam.
            lframe = (g.tick // 3) % 4
            for li, L in enumerate(g.lasers):
                stage_l, prog = g._laser_phase(L, g.tick)
                if stage_l is None:
                    continue
                half = g._laser_width(L, g.tick)
                if half <= 0.05:
                    continue
                lbucket = int(round(math.degrees(L["ang"]) / KT_ROT_DEG)) % KT_ROT_BUCKETS
                # The telegraph is a hairline in the laser's OWN colour (the
                # modern read: you learn which line becomes which beam), pale
                # and still -- no flow -- so it can be planned around and never
                # be mistaken for the live beam.
                lcol = L["ci"]
                if stage_l == "warn":
                    lalpha = 0.30 + 0.22 * prog
                    lf = 0
                else:
                    lalpha = 1.0 if stage_l == "live" else (1.0 - prog)
                    lf = lframe
                ab_l = int(lalpha * 5.999)
                lkey = ("laser", li)
                # yzoom: the body is the middle 16px of the 32px art, so
                # 2*half/16 makes the drawn body exactly 2*half wide (the
                # collider's KT_LASER_HIT_FRAC is a fraction of that).
                laser_d = Transform(
                    kt_art("kt_lasers", "laser:%d:%d" % (lcol, lf)),
                    xzoom=L["len"] / 256.0, yzoom=half / 8.0, subpixel=True,
                    rotate=lbucket * KT_ROT_DEG, alpha=lalpha, additive=1.0)
                # The art is drawn about its own centre, so the blit anchors on
                # the MIDPOINT of the segment, not its origin.
                mx = L["x"] + math.cos(L["ang"]) * L["len"] * 0.5
                my = L["y"] + math.sin(L["ang"]) * L["len"] * 0.5
                try:
                    # A rotated displayable is PADDED to a square as wide as the
                    # beam is long, so this box is big (a full-width beam is
                    # ~600x600) and is blitted from a negative origin. That is
                    # fine -- the stage clips it -- but it does mean the blit
                    # position must be the box's CORNER, i.e. the midpoint minus
                    # half the RETURNED size, never the beam's own origin.
                    quad = int(L["len"]) + 64
                    lr_, (lw_, lh_) = tex(lkey, laser_d, quad, quad)
                    sblit(lr_, (mx - lw_ / 2.0, my - lh_ / 2.0))
                except Exception:
                    pass
                # The source: a flare where the beam leaves, sized by how fat
                # the beam is burning (a telegraph gets a pin of light).
                fz_ = round(min(1.6, 0.35 + half / 12.0), 1)
                lsk = ("lsrc", lcol, ab_l, fz_)
                lsr, (lsw, lsh) = tex(lsk, self._art(
                    "kt_fx", "flare:%d" % lcol, zoom=fz_, alpha=(ab_l + 0.5) / 6.0), 128, 128)
                sblit(lsr, (L["x"] - lsw / 2.0, L["y"] - lsh / 2.0))

            # --- enemy bullets: THE hot loop ----------------------------------
            bullets = g.bullets
            # The spawn ring is an extra blit per NEWBORN bullet; once the field
            # is dense enough that frame time matters more, it is skipped. (The
            # old second "white core" blit on every orb is gone outright: the
            # art carries its own white-hot core now.)
            draw_rings = len(bullets) <= 320 and not low
            twirl = KT_TWIRL
            spawn_body = KTStage.SPAWN_BODY
            # Patience tell, resolved ONCE per frame: while the soul is still,
            # every calm bullet drops to a ghost texture -- the field itself
            # answers your stillness. Move and they snap solid again.
            calm_ghost = 1 if g.still_ticks > 0 else 0
            for b in bullets:
                kind = b["kind"]
                # Both cache keys are computed by the SIMULATION and cached on
                # the bullet: sq is the scale in quarter steps (fixed for life),
                # and rb is the rotation bucket, which _advance_bullets already
                # had the heading in hand to compute. Rotation buckets trade a
                # little angular precision for a huge cache win -- 60 buckets is
                # 6 degrees per texture -- and doing the arithmetic once per
                # tick instead of once per draw keeps this loop to dict reads.
                sq = b["sq"]
                bucket = b["rb"]
                age = b["age"]
                x = b["x"]
                y = b["y"]
                ci = b["ci"]
                # Twirling kinds turn on their own clock (KT_TWIRL): the bucket
                # comes from the bullet's age, offset by its ring phase so the
                # stars in one ring are not all at the same angle. Age stops
                # under the Seer's time stop, so a stopped star stops turning.
                tw_ = twirl.get(kind)
                if tw_ is not None:
                    bucket = ((age + int(b["ph"] * 5.0)) // tw_[1]) % tw_[0]
                elif kind == "butterfly" and (age // 6) % 2:
                    # The other wing-beat. Same heading bucket, different art.
                    kind = "butterfly_b"
                # MATERIALIZE (see the SPAWN MATERIALIZE block up top): for its
                # first KT_SPAWN_TICKS a bullet is still arriving -- translucent
                # and a little under size -- while a ring of its own colour
                # closes down onto it from well outside, the modern Touhou spawn
                # read. The ring is the telegraph: for those few ticks you can
                # see where a wall is about to be before it is one. Everything
                # here is a bucketed cache key (ring: colour x 8 steps x 3 body
                # sizes), so the whole effect is a handful of textures.
                if age < KT_SPAWN_TICKS:
                    grow = (age + 1) / float(KT_SPAWN_TICKS)
                    sq = max(1, int(round(sq * (0.72 + 0.28 * grow))))
                    ab = min(KT_SPAWN_STEPS - 1, int(grow * KT_SPAWN_STEPS))
                    if draw_rings:
                        body = spawn_body.get(kind, 18.0) * b["sq"] * 0.25
                        bcl = 0 if body < 21.0 else (1 if body < 34.0 else 2)
                        rkey = ("sring", ci, age, bcl)
                        rgot = frame_tex.get(rkey)
                        if rgot is None:
                            # Faint on purpose: a bloom spawns 30 bullets on one
                            # point, and 30 rings added on top of each other at
                            # any real alpha is a white blob over her. Faint
                            # rings stack into a soft burst instead.
                            dia = (20.0, 28.0, 50.0)[bcl] * (2.3 - 1.3 * grow)
                            rgot = tex(rkey, self._art(
                                "kt_fx", "spawnring:%d" % ci, zoom=round(dia / 40.0, 2),
                                alpha=round(0.08 + 0.30 * (1.0 - grow), 2)), 192, 192)
                        rr_, (rw_, rh_) = rgot
                        sblit(rr_, (x - rw_ / 2.0, y - rh_ / 2.0))
                else:
                    ab = KT_SPAWN_STEPS
                gh = 1 if (calm_ghost and b["calm"]) else 0
                # Frame memo FIRST. tex() takes the displayable as an argument,
                # so writing tex(key, self._bullet_tf(...)) builds the transform
                # lookup on every single bullet -- a bound-method call, a second
                # tuple and a second dict get -- even when this frame has
                # already rendered that texture. Rotation is bucketed to six
                # degrees and scale to quarter steps precisely so that a volley
                # collapses onto a handful of textures, so the hit path is the
                # common path and it should cost one dict get.
                key = (kind, ci, bucket, sq, gh, ab)
                got = frame_tex.get(key)
                if got is None:
                    got = tex(key, self._bullet_tf(kind, ci, bucket, sq, gh, ab))
                r, (w, h) = got
                sblit(r, (x - w / 2.0, y - h / 2.0))

            # --- the stopped clock (Seer mask) ----------------------------------
            # While enemy time is frozen the whole field sits under cold glass:
            # a pale blue wash OVER the bullets, warming to white as the world
            # is about to resume (the player's cue to be somewhere else).
            if g.tick < g.stop_until:
                stage.blit(rect("#9ab8ff30", KT_W, KT_H), (0, 0))
                rem = g.stop_until - g.tick
                if rem < 12:
                    stage.blit(rect("#f5faff" + ("%02x" % (58 - rem * 4)), KT_W, KT_H), (0, 0))

            # --- bomb: the full Touhou send-off ---------------------------------
            # Detonation flash, THREE staggered shockwave rings (a tight bright
            # leader, the main sweep, a fat trailing echo), plus the wavefront
            # sparks the sim spawns; the whole stage also shakes (applied at
            # the final mount, below).
            if g.bomb_tick is not None:
                bt = g.tick - g.bomb_tick
                if bt < 10:
                    fa = int((1.0 - bt / 10.0) * 120)
                    stage.blit(rect("#ffd7e8" + ("%02x" % fa), KT_W, KT_H), (0, 0))
                # Bomb WASH: this mode's own blast disc (kt_bombwash.png), blown
                # out from the ship underneath the shader rings. The rings are
                # the edge of the blast; this is its body -- without it the
                # bomb reads as three expanding outlines around empty stage.
                # It is one cached texture per (size, alpha) bucket, and it
                # lives for only the first half of the wave so it never hides
                # the bullets it is busy clearing.
                if bt < KT_BOMB_WAVE_TICKS * 0.6:
                    bwp = kt_clamp(bt / (KT_BOMB_WAVE_TICKS * 0.6), 0.0, 1.0)
                    bw_px = 180.0 + 900.0 * bwp
                    bw_a = (1.0 - bwp) * 0.5
                    # Continuous, not bucketed. The old EIGHT alpha steps meant
                    # the brightest thing the player ever triggers dimmed out in
                    # eight visible drops across 36 ticks.
                    # The blast body is its own art (a pink bloom with an
                    # inked burst of rays and a rim), drawn as light.
                    wash_d = Transform(
                        kt_art("kt_bombwash", "bombwash"), zoom=bw_px / 256.0,
                        subpixel=True, alpha=bw_a, additive=1.0)
                    try:
                        bwq = int(bw_px) + 32
                        bwr, (bww, bwh) = tex(("bombwash",), wash_d, bwq, bwq)
                        sblit(bwr, (g.px - bww / 2.0, g.py - bwh / 2.0))
                    except Exception:
                        pass
                if MSBF_FX_SHADERS:
                    # Tuple fields: cache-name, frame delay, shader-quad size,
                    # RGB color, ring thickness, brightness. Same shader, three
                    # different delayed rings.
                    for rkey_name, delay, quad, col, thick, inten in (
                            ("bombring_lead", 0, 1360, (1.0, 0.92, 0.96), 0.05, 1.5),
                            ("bombring", 4, 1560, (1.0, 0.62, 0.78), 0.10, 1.15),
                            ("bombring_echo", 10, 1560, (1.0, 0.44, 0.62), 0.18, 0.8)):
                        if bt < delay:
                            continue
                        prog = kt_clamp((bt - delay) / float(KT_BOMB_WAVE_TICKS), 0.0, 1.0)
                        # u_progress is CONTINUOUS. It used to be cached in 16
                        # buckets, which meant a shockwave crossing 1560px in 60
                        # ticks did it in sixteen jumps of nearly a hundred
                        # pixels each -- the single most visible stutter in the
                        # fight, on the single fastest-moving thing in it. The
                        # quad size is fixed per ring, so the cached Solid still
                        # carries the texture and only the Transform is rebuilt.
                        ring_d = Transform(
                            self._fx_solid(), xysize=(quad, quad),
                            shader="msbf.ring", mesh=True,
                            u_progress=prog, u_color=col,
                            u_thickness=thick, u_intensity=inten)
                        try:
                            wr, (ww, wh) = tex((rkey_name,), ring_d, quad, quad)
                            sblit(wr, (g.px - ww / 2.0, g.py - wh / 2.0))
                        except Exception:
                            pass

            # --- victory shock rings (each staged detonation + the final boom) --
            if g.phase == "victory" and MSBF_FX_SHADERS:
                # Each tuple is one explosion: start tick, shader-quad size,
                # and RGB color. The final 1200px ring is the white-out boom.
                for boom, quad, col in ((14, 360, (1.0, 0.56, 0.72)),
                        (34, 360, (0.72, 0.86, 1.0)),
                        (52, 420, (1.0, 0.56, 0.72)),
                        (68, 420, (1.0, 0.9, 0.6)),
                        (82, 480, (1.0, 0.56, 0.72)),
                        (96, 1200, (1.0, 0.92, 0.96))):
                    aget = g.phase_tick - boom
                    if 0 <= aget < 46:
                        # Continuous progress, like the bomb rings. aget is
                        # local age since this specific explosion started.
                        ring_v = Transform(
                            self._fx_solid(), xysize=(quad, quad),
                            shader="msbf.ring", mesh=True,
                            u_progress=aget / 46.0, u_color=col,
                            u_thickness=0.14, u_intensity=1.3)
                        try:
                            vr_, (vw_, vh_) = tex(("winring", boom), ring_v, quad, quad)
                            sblit(vr_, (g.bx - vw_ / 2.0, g.by + bob - vh_ / 2.0))
                        except Exception:
                            pass

            # --- event shockwaves (declare / capture / bar break) -------------
            # Each queued ring expands over 46 ticks from where it was fired.
            # Same 16-bucket msbf.ring cache as the bomb/victory booms.
            if MSBF_FX_SHADERS and g.ring_fx:
                for _ri, rf in enumerate(g.ring_fx):
                    raged = g.tick - rf["born"]
                    if raged < 0 or raged >= 46:
                        continue
                    rq = rf["quad"]
                    ring_e = Transform(
                        self._fx_solid(), xysize=(rq, rq),
                        shader="msbf.ring", mesh=True,
                        u_progress=raged / 46.0, u_color=rf["col"],
                        u_thickness=0.12, u_intensity=1.2)
                    try:
                        er_, (ew_, eh_) = tex(("evtring", _ri), ring_e, rq, rq)
                        sblit(er_, (rf["x"] - ew_ / 2.0, rf["y"] - eh_ / 2.0))
                    except Exception:
                        pass

            # --- player death FX: red stage sting, crimson pichun ring, flare --
            for dfx in g.death_fx:
                aged = g.tick - dfx["born"]
                if aged >= 46:
                    continue
                if aged < 8:
                    stage.blit(rect("#ff334822", KT_W, KT_H), (0, 0))
                if MSBF_FX_SHADERS:
                    # Red pichun ring expands smoothly over its 46 ticks.
                    ring_dx = Transform(
                        self._fx_solid(), xysize=(520, 520),
                        shader="msbf.ring", mesh=True,
                        u_progress=aged / 46.0, u_color=(1.0, 0.35, 0.45),
                        u_thickness=0.16, u_intensity=1.35)
                    try:
                        dr_, (dw_, dh_) = tex(("deathring", dfx["born"]), ring_dx, 520, 520)
                        sblit(dr_, (dfx["x"] - dw_ / 2.0, dfx["y"] - dh_ / 2.0))
                    except Exception:
                        pass
                if aged < 12:
                    # A white flare at the death point, shrinking in six steps.
                    sqv = max(2, 8 - (aged // 2))
                    fr3, (fw3, fh3) = tex(("dflare", sqv), self._art(
                        "kt_fx", "flare:13", zoom=0.3 * sqv, alpha=0.9), 192, 192)
                    sblit(fr3, (dfx["x"] - fw3 / 2.0, dfx["y"] - fh3 / 2.0))

            # --- player --------------------------------------------------------
            alive = g.phase not in ("defeat",) and g.result is None
            if alive:
                inv = g.tick < g.invuln_until
                blink_off = inv and (g.tick // 3) % 2 == 1
                # Dash afterimages: sample the ship every 2 ticks while it moves
                # unfocused, then draw faint ghosts behind it so fast weaving
                # streaks. Cleared on focus (precise play leaves no smear) and
                # reset on a big jump so a respawn doesn't draw a screen-long
                # smear from the death spot.
                if not g.focus and not g.paused and g.tick - self._ptrail_tick >= 2:
                    self._ptrail_tick = g.tick
                    if self.ptrail:
                        lx, ly = self.ptrail[-1]
                        if abs(g.px - lx) + abs(g.py - ly) > 60.0:
                            self.ptrail = []
                    self.ptrail.append((g.px, g.py))
                    if len(self.ptrail) > 3:
                        del self.ptrail[0]
                if g.focus:
                    self.ptrail = []
                if self.ptrail and not g.focus and not low:
                    p0x, p0y = self.ptrail[0]
                    if abs(g.px - p0x) + abs(g.py - p0y) > 9.0:
                        pgr, (pgw, pgh) = tex("player_ghost", self._art(
                            "kt_player", "soul", zoom=KT_SOUL_ZOOM, alpha=0.26), 64, 64)
                        for gx, gy in self.ptrail[:-1]:
                            sblit(pgr, (gx - pgw / 2.0, gy - pgh / 2.0))
                if not blink_off:
                    # Options: two bookmark crystals that ride with the soul --
                    # spread wide and a little behind while you move freely,
                    # tucked in close ahead when you focus (the modern shot-type
                    # read of "focused"). The spread is eased per SIM tick in
                    # _advance_fx_env, so they glide between the two stances.
                    of = self._fx_opt
                    orr, (ow, oh) = tex("option", self._art(
                        "kt_player", "option", add=False), 32, 32)
                    for side in (-1.0, 1.0):
                        obob = math.sin(g.tick * 0.11 + side * 1.3) * 1.6
                        ox = g.px + side * (25.0 - 14.0 * of)
                        oy = g.py + 7.0 - 24.0 * of + obob
                        sblit(orr, (ox - ow / 2.0, oy - oh / 2.0))
                    # During the deathbomb window the soul burns white-hot --
                    # the "you just got clipped, X NOW" telegraph.
                    plkey = "soul_hot" if g.dying_tick is not None else "soul"
                    plr, (plw, plh) = tex(("player", plkey), self._art(
                        "kt_player", plkey, zoom=KT_SOUL_ZOOM, add=False), 64, 64)
                    sblit(plr, (g.px - plw / 2.0, g.py - plh / 2.0))
                if self._fx_focus_a > 0.004:
                    # Focus sigil: a small, fast copy of the boss spell circle
                    # spinning under the ship (the classic hitbox sigil), with
                    # the blob ring kept as the no-shader fallback. It fades in
                    # and out on its own fast envelope rather than blinking on
                    # with the key -- and it also SCALES up as it arrives, which
                    # is the affordance: the sigil opening is what tells you the
                    # smaller hitbox is live.
                    fa = self._fx_focus_a
                    drew_sigil = False
                    if KT_SHADER_OK:
                        try:
                            # Fixed 58px quad; size rides u_koto_scale and the
                            # pulse rides u_koto_breath, both on the GPU. Sizing
                            # this from a python sine only ever bought SEVEN
                            # whole-pixel sizes at this scale, and it flicked
                            # between them twice a second.
                            fs = 58
                            fsig = Transform(
                                self._fx_solid(), xysize=(fs, fs),
                                shader="koto.circle", mesh=True,
                                u_koto_col=Color("#ff3b73").rgb,
                                u_koto_alpha=0.85 * fa, u_koto_spin=3.2,
                                u_koto_breath=0.055,
                                u_koto_scale=0.55 + 0.45 * fa)
                            fsr, (fsw, fsh) = tex(("sigil",), fsig, fs, fs)
                            sblit(fsr, (g.px - fsw / 2.0, g.py - fsh / 2.0))
                            drew_sigil = True
                        except Exception:
                            pass
                    if not drew_sigil:
                        fring = Transform(
                            kt_art("kt_fx", "spawnring:0"), zoom=0.8, subpixel=True,
                            alpha=0.6 * fa, additive=1.0)
                        fr, (fw, fh) = tex(("focus_ring",), fring, 64, 64)
                        sblit(fr, (g.px - fw / 2.0, g.py - fh / 2.0))
                    # The true hitbox: a white point in a crimson ring, drawn
                    # opaque (it is the one thing on the stage that must never
                    # be lost in the light around it).
                    hr_, (hw, hh) = tex("hitbox", self._art(
                        "kt_player", "hitbox", add=False), 24, 24)
                    sblit(hr_, (g.px - hw / 2.0, g.py - hh / 2.0))
                # Graze pulse: a cyan ripple pops off the ship for 8 ticks after
                # every graze -- close calls FEEL paid. Eight cached transforms
                # total (one per age step), keyed on the tick delta.
                gpa = g.tick - g.graze_tick
                if 0 <= gpa < 8:
                    gpr, (gpw, gph) = tex(("grzp", gpa), self._art(
                        "kt_fx", "spawnring:6", zoom=round(0.42 + gpa * 0.13, 2),
                        alpha=round(0.62 - gpa * 0.07, 2)), 96, 96)
                    sblit(gpr, (g.px - gpw / 2.0, g.py - gph / 2.0))

            # --- spell-5 darkness (GPU spotlight) ------------------------------
            if g.dark > 0.02 and KT_SHADER_OK:
                try:
                    dark_d = Transform(Solid("#000000"), xysize=(KT_W, KT_H),
                                        shader="koto.spotlight", mesh=True,
                                        u_koto_p=(g.px, g.py),
                                        u_koto_b=(bx_draw, by_draw),
                                        u_koto_dark=g.dark,
                                        u_koto_res=(float(KT_W), float(KT_H)))
                    dr = renpy.render(dark_d, KT_W, KT_H, st, at)
                    rv.depends_on(dr)
                    stage.blit(dr, (0, 0))
                except Exception:
                    pass

            # --- corner brackets: card-colour cabinet framing, breathing -------
            # Four L-brackets pinned to the stage corners, pulsing on a 4-step
            # alpha bucket so the rect cache stays bounded (palette x 4).
            cbq = int((0.5 + 0.5 * math.sin(g.tick * 0.03)) * 3.999)
            cbc = KT_PAL[g.cur_color] + ("%02x" % (40 + 15 * cbq))
            for cxx, cyy, ddx, ddy in ((3, 3, 1, 1), (KT_W - 3, 3, -1, 1),
                    (3, KT_H - 3, 1, -1), (KT_W - 3, KT_H - 3, -1, -1)):
                stage.blit(rect(cbc, 24, 3), (cxx if ddx > 0 else cxx - 24,
                                                cyy if ddy > 0 else cyy - 3))
                stage.blit(rect(cbc, 3, 24), (cxx if ddx > 0 else cxx - 3,
                                                cyy if ddy > 0 else cyy - 24))

            # --- in-stage HUD ---------------------------------------------------
            # The modern Touhou layout. Her life is the RING around her (drawn
            # with the boss, above); up here are her name and the stars for the
            # bars she has left (top-left), the timer with its hundredths (top
            # centre) and, under a spell card, the card's name, bonus and
            # history (top-right, where the declaration's flight lands).
            if g.phase in ("nonspell", "declare", "spell"):
                if not KT_SHADER_OK:
                    # No shaders, no ring: fall back to a thin bar so the
                    # fight is still readable.
                    bw_ = KT_W - 20
                    stage.blit(rect("#0a1220dd", bw_, 4), (10, 2))
                    fill_w = int(bw_ * kt_clamp(g.boss_hp / g.boss_hp_max, 0.0, 1.0))
                    if fill_w > 0:
                        stage.blit(rect(KT_PAL[bar["color"]], fill_w, 4), (10, 2))
                nmr_, (_nmw, _nmh) = tex(("t", "hud_name"), self._text(
                    "KOTONOHA  KATSURA", 12, "#ffd7e8", True, True), 260, 22)
                stage.blit(nmr_, (12, 6))
                if g.endless:
                    # No fixed bar count in endless -- show the wave instead.
                    wvr, (wvw, wvh) = tex(("wave_hud", g.endless_wave),
                                        self._text("WAVE %d" % (g.endless_wave + 1), 13, "#ffd7e8", True, True), 170, 24)
                    sblit(wvr, (12, 24))
                elif g.debug_wave is not None:
                    # Wave viewer: name the forced pairing instead of stars.
                    dv = "VIEWING  NS %d / SP %d" % (g.debug_wave[0] + 1, g.debug_wave[1] + 1)
                    dvr, (dvw, dvh) = tex(("t", "dbwave", dv),
                                        self._text(dv, 13, "#ffb84a", True, True), 260, 24)
                    sblit(dvr, (12, 24))
                else:
                    # One star per spell card still to come after this one.
                    stars = len(KT_BARS) - g.bar_index - 1
                    if stars > 0:
                        sir, (siw, sih) = tex("hud_star", self._art(
                            "kt_player", "icon_star", zoom=0.85, add=False), 32, 32)
                        for i in range(stars):
                            sblit(sir, (14 + i * 16 - siw / 2.0 + 6, 32.0 - sih / 2.0))
                # The timer: whole seconds large, hundredths small, both drawn
                # from cached glyphs (a new string every tick would otherwise be
                # a new Text every tick).
                tl_ = max(0, g.time_left)
                secs = tl_ // 60
                cs = (tl_ % 60) * 100 // 60
                tcol = "#ff5c6a" if secs < 10 else "#f5faff"
                self._draw_glyphs(stage, tex, "%02d" % secs, 314.0, 2.0, 24, tcol, align=1.0)
                self._draw_glyphs(stage, tex, ".%02d" % cs, 313.0, 12.0, 14, tcol, align=0.0)

            # Spell card name: staged inside the declaration ribbon, then FLOWN
            # into its HUD slot across the phase flip. See _draw_cutin.
            if g.phase == "declare":
                self._draw_cutin(g, bar, stage, tex, rect, fx_col)
            elif g.phase == "spell":
                card_lines = self._card_lines(bar["card"])
                # The far half of the flight. Until it lands, the HUD name is
                # still in the air and _card_flight_draw owns it -- drawing the
                # parked copy here as well would put two of it on the stage.
                flight = self._card_flight(g)
                if flight < 1.0:
                    self._card_flight_draw(g, bar, flight, stage, tex)
                else:
                    line_y = KT_HUD_NAME_Y
                    for i, line in enumerate(card_lines):
                        size = self._size_for_line(line, 16 if i == 0 else 15, 12)
                        color = KT_PAL[bar["color"]] if i == 0 and len(card_lines) > 1 else "#ffd7e8"
                        nr, (nw, nh) = tex(("cardname_sm", g.bar_index, i, size),
                                            self._text(line, size, color, True, True), KT_W - 130, 28)
                        stage.blit(nr, (int(KT_HUD_R - nw), int(line_y)))
                        line_y += nh + 2
                    # The plate's rule: a hairline in the card's accent drawn
                    # leftward from a diamond at the right edge.
                    rlr, (rlw, rlh) = tex("hud_rule", self._misc("hud_rule", lambda: Transform(
                        kt_art("kt_player", "rule"), xzoom=-1.0, alpha=0.9)), 260, 16)
                    stage.blit(rlr, (int(KT_HUD_R + 6 - rlw), int(line_y - 3)))
                    # Live capture bonus (classic Touhou): what the card is
                    # worth RIGHT NOW, draining with the clock, and the card's
                    # history. Greyed the moment the bonus is forfeit.
                    hc, ha = g.cur_hist
                    htxt = "HISTORY %02d/%02d" % (hc, ha)
                    if g.spell_ok:
                        bfrac = kt_clamp(g.time_left / float(max(1, g.cur_sp_time)), 0.0, 1.0)
                        bval = int(g.cur_value * (0.30 + 0.70 * bfrac))
                        bval -= bval % 10
                        btxt = "BONUS " + format(bval, ",") + "   " + htxt
                        bcol = "#ffd7e8"
                    else:
                        btxt = "BONUS FAILED   " + htxt
                        bcol = "#9aa8bd"
                    self._draw_glyphs(stage, tex, btxt, KT_HUD_R, line_y + 6.0, 11, bcol, align=1.0)

            # ENEMY tag on the bottom lip, riding her x (the modern marker: a
            # small labelled plate in the card's colour, not a bare bar).
            if boss_on and g.phase in ("nonspell", "spell", "declare"):
                ex_ = int(kt_clamp(g.bx, 26.0, KT_W - 26.0))
                stage.blit(rect(KT_PAL[g.cur_color] + "d0", 48, 13), (ex_ - 24, KT_H - 14))
                etr, (etw, eth) = tex(("t", "enemy_tag"), self._text(
                    "ENEMY", 10, "#f5faff", True, True), 80, 20)
                stage.blit(etr, (int(ex_ - etw / 2.0), int(KT_H - 14 + (13 - eth) / 2.0)))

            # Banners (EXTEND! / SPELL CARD CAPTURED! / +1 BOMB...), rising+fading.
            for bn in g.banners:
                age = g.tick - bn["born"]
                if age > bn["ttl"]:
                    continue
                frac = age / float(bn["ttl"])
                ab = 3 - min(3, int(frac * 4.0))
                bsize = self._size_for_line(bn["text"], bn["size"], 22)
                # ab is a 3-step fade bucket. It used to sit in the tex() key
                # WITHOUT reaching the displayable, so every banner rose at a
                # flat alpha and then vanished on its last tick; all four
                # buckets were the same picture under four different keys.
                bnr, (bnw, bnh) = tex(("banner", bn["text"], bn["ci"], bsize, ab),
                                        self._text_fade(bn["text"], bsize, KT_PAL[bn["ci"]], True, ab, 4), KT_W - 36, 72)
                stage.blit(bnr, (int(KT_W / 2 - bnw / 2), int(bn["y"] - frac * 20.0)))

            # Intro nameplate / end cards.
            if g.phase == "intro":
                pt = g.phase_tick
                if pt > 20:
                    n1, (w1, h1) = tex(("t", "koto1"), self._text("KOTONOHA  KATSURA", 34, "#ff8fc8", True, True), 520, 62)
                    stage.blit(n1, (int(KT_W / 2 - w1 / 2), 250))
                if pt > 50:
                    if g.endless and g.practice:
                        sub = "Endless Practice  --  No Last Page, No Last Life"
                    elif g.endless:
                        sub = "Endless Reading  --  No Last Page"
                    else:
                        sub = "The Last Word Etched"
                    n2, (w2, h2) = tex(("t", "koto2", sub), self._text(sub, 17, "#f5faff", True), 520, 34)
                    stage.blit(n2, (int(KT_W / 2 - w2 / 2), 296))
            elif g.phase == "victory":
                # Results card fades in staged, then the final boom's white-out
                # (drawn last) washes over it and the text bleeds through.
                vt2 = g.phase_tick
                if vt2 >= 118:
                    stage.blit(rect("#00000066", KT_W, KT_H), (0, 0))
                if vt2 >= 132:
                    v1, (w1, h1) = tex(("t", "clear"), self._text("SCENE  CLEARED", 40, "#ffe65c", True, True), 520, 70)
                    stage.blit(v1, (int(KT_W / 2 - w1 / 2), 236))
                if vt2 >= 162:
                    sline = "FINAL SCORE   " + format(g.score, ",")
                    v2, (w2, h2) = tex(("winscore", sline), self._text(sline, 20, "#f5faff", True), 460, 36)
                    stage.blit(v2, (int(KT_W / 2 - w2 / 2), 306))
                if vt2 >= 186:
                    cline = "SPELL CARDS CAPTURED   %d / %d" % (g.captures, len(KT_BARS))
                    v3, (w3, h3) = tex(("wincaps", cline), self._text(cline, 15, "#9aa8bd", True), 420, 30)
                    stage.blit(v3, (int(KT_W / 2 - w3 / 2), 342))
                    if g.practice or g.debug:
                        rec_tag = "DEBUG READING  --  NO RECORD" if g.debug else "PRACTICE READING  --  NO RECORD"
                        rec_col = "#ffb84a" if g.debug else "#8affb0"
                        v4, (w4, h4) = tex(("t", "winprac", rec_tag), self._text(rec_tag, 13, rec_col, True), 400, 28)
                        stage.blit(v4, (int(KT_W / 2 - w4 / 2), 372))
                if 96 <= vt2 < 152:
                    # The final boom's white overlay fades out after tick 96,
                    # letting the result text appear through the wash.
                    wa = 1.0 - (vt2 - 96) / 56.0
                    ab2 = int(wa * 15.99)
                    if ab2 > 0:
                        stage.blit(rect("#f5faff" + ("%02x" % (ab2 * 14)), KT_W, KT_H), (0, 0))
            elif g.phase == "defeat":
                stage.blit(rect("#00000088", KT_W, KT_H), (0, 0))
                d1, (w1, h1) = tex(("t", "over"), self._text("GAME  OVER", 40, "#ff5c6a", True, True), 440, 70)
                stage.blit(d1, (int(KT_W / 2 - w1 / 2), 270))

            # General event flash (declare / capture / break): a colour wash
            # over the whole stage that decays from its peak. Drawn above the
            # HUD but below the pause overlay for a clean punch.
            if g.screen_flash is not None:
                sf = g.screen_flash
                sfa = g.tick - sf["born"]
                if sfa < sf["ttl"]:
                    fa = int(sf["peak"] * (1.0 - sfa / float(sf["ttl"])))
                    if fa > 0:
                        stage.blit(rect(sf["col"] + ("%02x" % min(255, fa)), KT_W, KT_H), (0, 0))

            # The pause panel used to be drawn HERE, as hand-blitted text in a
            # hand-measured box. It is a screen (kt_pause_panel) now, because a
            # CDD cannot hold a draggable widget and the panel carries the audio
            # mixer: you can move the volume without leaving the run. The dim
            # below is all that is left, and it still covers the PLAYFIELD only
            # so the score/lives HUD stays readable while you are stopped.
            if g.paused:
                stage.blit(rect("#000000aa", KT_W, KT_H), (0, 0))

            # Clip the stage (bullets live 70px past the lip) and mount it.
            # A live bomb rocks the whole playfield: a decaying two-axis shake
            # on the mount position (Touhou screen-quake). The few px of
            # overlap with the chrome during the kick reads as impact.
            #
            # THE CLIP IS A FLAG, NOT A SUBSURFACE. `stage.subsurface(...)` looks
            # free and is not: Render.subsurface walks EVERY child, computes two
            # sublines for it, and builds a fresh cropped Render around it (which
            # recurses one more level into the blitted texture's own Render). At
            # 400 bullets that is ~1600 Render objects a frame -- each one a
            # python object with two lists and a set, each one appended to
            # renpy.display.render.live_renders and then walked and killed again
            # by the next frame's mark_sweep. It was the single most expensive
            # thing this method did, and it was pure bookkeeping: not one pixel
            # came out different.
            #
            # Setting the clipping flags asks gl2 for exactly the same rectangle
            # (gl2draw.draw_one turns xclipping/yclipping into a clip polygon and
            # crops each quad's mesh against it on the GPU-facing side) with zero
            # allocation on ours. Bullets, lasers, bomb rings and the declare
            # cut-in all still stop dead at the cabinet edge.
            stage.xclipping = True
            stage.yclipping = True
            mx_, my_ = KT_SX, KT_SY
            if g.bomb_tick is not None:
                bt2 = g.tick - g.bomb_tick
                if bt2 < 54:
                    amp = 6.0 * (1.0 - bt2 / 54.0)
                    mx_ += math.sin(bt2 * 1.9) * amp
                    my_ += math.cos(bt2 * 2.6) * amp * 0.6
            rv.blit(stage, (mx_, my_))

            # --- side HUD (screen space, right panel) ---------------------------
            hx = KT_SX + KT_W + 42
            # Panel spine: a card-colour rail beside the frame's pink divider,
            # so the score panel always carries the current card's accent.
            rv.blit(rect(KT_PAL[g.cur_color] + "3c", 3, 604), (hx - 26, 58))
            # Endless keeps its own hi-score; the fixed run keeps the other.
            hi_best = (persistent.kotomode_endless_hiscore if g.endless else persistent.kotomode_hiscore) or 0
            hi = max(g.score, hi_best)
            rows = [
                ("HI SCORE", format(hi, ",")),
                ("SCORE", format(g.score, ",")),
            ]
            y = 66
            # A divider rule under each heading, and the values drawn from
            # cached glyphs (the score changes every few ticks all fight).
            prl, (prw, prh) = tex("panel_rule", self._art(
                "kt_player", "rule", add=False, alpha=0.75), 260, 16)
            for label, val in rows:
                lr, (lw, lh) = tex(("t", "lbl" + label), self._text(label, 15, "#ff8fc8", True, True), 180, 28)
                rv.blit(lr, (hx, y))
                rv.blit(prl, (hx - 4, y + 15))
                self._draw_glyphs(rv, tex, val, hx + 24, y + 25, 24, "#f5faff")
                y += 66
            # Lives (hearts) + bombs (daggers).
            lr, (lw, lh) = tex(("t", "lives"), self._text("PLAYER", 15, "#ff8fc8", True, True), 180, 28)
            rv.blit(lr, (hx, y))
            rv.blit(prl, (hx - 4, y + 15))
            hr2, (hw2, hh2) = tex("life_icon", self._art(
                "kt_player", "soul", zoom=0.62, add=False), 48, 48)
            if g.practice or g.debug:
                rv.blit(hr2, (hx + 24, y + 26))
                inf_tag = "x INF  (DEBUG)" if g.debug else "x INF  (PRACTICE)"
                inf_col = "#ffb84a" if g.debug else "#8affb0"
                ir, (iw, ih) = tex(("t", "inf", inf_tag), self._text(inf_tag, 15, inf_col, True, True), 260, 32)
                rv.blit(ir, (hx + 24 + hw2 + 10, y + 28))
            else:
                for i in range(g.lives):
                    rv.blit(hr2, (hx + 24 + i * (hw2 + 8), y + 26))
            y += 66
            br2, (bw2, bh2) = tex(("t", "bombs"), self._text("BOMB", 15, "#ff8fc8", True, True), 180, 28)
            rv.blit(br2, (hx, y))
            rv.blit(prl, (hx - 4, y + 15))
            bir, (biw, bih) = tex("bomb_icon", self._art(
                "kt_player", "icon_bomb", zoom=0.95, add=False), 48, 48)
            for i in range(g.bombs):
                rv.blit(bir, (hx + 24 + i * (biw + 10), y + 24))
            y += 70
            if g.endless and g.practice:
                # Endless Practice sets no record, so the slot that shows the
                # record in real Endless counts falls instead: the only thing a
                # run with unlimited lives can be measured by.
                stat_rows = (("GRAZE", str(g.graze)),
                            ("CARDS", str(g.captures)),
                            ("WAVE", str(g.endless_wave + 1)),
                            ("FALLS", str(g.deaths)))
            elif g.endless:
                stat_rows = (("GRAZE", str(g.graze)),
                            ("CARDS", str(g.captures)),
                            ("WAVE", str(g.endless_wave + 1)),
                            ("BEST W", str(max((persistent.kotomode_endless_wave or 0) + 1,
                                                g.endless_wave + 1))))
            else:
                stat_rows = (("GRAZE", str(g.graze)),
                            ("CARDS", "%d / %d" % (g.captures, len(KT_BARS))),
                            ("BAR", "%d / %d" % (min(g.bar_index + 1, len(KT_BARS)), len(KT_BARS))))
            for label, val in stat_rows:
                lr3, (lw3, lh3) = tex(("t", "lbl2" + label), self._text(label, 13, "#ff8fc8", True, True), 120, 24)
                rv.blit(lr3, (hx, y))
                self._draw_glyphs(rv, tex, val, hx + 110, y - 2, 18, "#f5faff")
                y += 36
            # Mode chip: which reading this is, wearing its own colour, with a
            # small pip of the same colour as a bullet-point.
            if g.endless or g.practice or g.debug or g.debug_wave is not None:
                if g.debug_wave is not None:
                    tag, tcol2 = "WAVE VIEWER", "#ffb84a"
                elif g.debug:
                    tag, tcol2 = "DEBUG READING", "#ffb84a"
                elif g.practice and g.endless:
                    tag, tcol2 = "ENDLESS PRACTICE", "#5cd7ff"
                elif g.practice:
                    tag, tcol2 = "PRACTICE READING", "#8affb0"
                else:
                    tag, tcol2 = "ENDLESS READING", "#ff8fc8"
                y += 10
                rv.blit(rect(tcol2 + "2e", 4, 20), (hx, y + 2))
                chp, (chw, chh) = tex(("t", "chip", tag),
                                    self._text(tag, 12, tcol2, True, True), 260, 24)
                rv.blit(chp, (hx + 12, y))

            # Keep the CDD alive. Matsu'Py will call render() again immediately,
            # at which point the fixed-step accumulator decides whether enough
            # wall time has passed to run another simulation tick.
            #
            # ...but only while there is a fight to advance. Paused or finished,
            # every one of those frames redrew an unchanging picture -- and this
            # is the most expensive stage in the project, so it was also the
            # worst place to do it. kototouhou_screen binds K_ESCAPE and
            # mouseup_3 to game.toggle_pause and branches on `game.paused`, so
            # the interaction restarts on unpause and the stage rebuilds; the
            # sim cannot get stuck behind this. Matches the guard in
            # tsubaki_soul.rpy and the Archivist Invasions stages.
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
                renpy.redraw(self, max(0.0, KT_TICK - self.acc))
            return rv

# --- SCREEN --------------------------------------------------------------------
# The fight screen is deliberately STATIC: backdrop, panel chrome, one KTStage.
# All motion lives inside the displayable, so nothing here rebuilds per frame.
# A slow 0.25s poll hands the result back (Function() actions end the
# interaction when they return non-None).
#
# Do not add timer-driven animation here. Timers restart interactions; this
# screen's job is to hold stable chrome and route only pause/quit/result events.

# DEV ONLY -- the wave viewer's picker. One grid, every opener and every card
# visible and clickable at once (the old renpy.display_menu pages ran off the
# bottom of the screen once the roster grew past a menu-full). Click one
# opener + one card, confirm. Returns (ns_index, sp_index), or None on back.
screen kt_wave_picker():
    modal True
    add Solid("#02040b")

    default wvp_ns = 0
    default wvp_sp = 0

    # Chrome: title + hairline, echoing the fight's cabinet trim.
    add Solid("#ff8fc866") xpos 40 ypos 78 xsize 1200 ysize 2
    text "THE WAVE VIEWER" font KT_FONT size 30 color "#ff8fc8" xpos 40 ypos 24 bold True
    text "pick the page: one opener, one card. she reads it once, then hands the book back." font KT_FONT size 12 color "#9aa8bd" xpos 42 ypos 60

    # --- opener column (nonspells) --------------------------------------------
    vbox:
        xpos 40
        ypos 100
        spacing 4
        text "OPENER  --  NONSPELL" font KT_FONT size 14 color "#ff8fc8" bold True
        null height 4
        for idx, tag, part in kt_wvp_ns_entries():
            button:
                xsize 330
                padding (8, 4, 8, 4)
                background ("#1a2c4a" if wvp_ns == idx else "#0a1220")
                hover_background "#14203a"
                action SetScreenVariable("wvp_ns", idx)
                hbox:
                    spacing 8
                    text tag font KT_FONT size 11 color "#ff8fc8" min_width 28 yalign 0.5 bold True
                    text part font KT_FONT size 12 yalign 0.5 color ("#f5faff" if wvp_ns == idx else "#9aa8bd")

    # --- card columns: her eight / the masks / the souls ----------------------
    hbox:
        xpos 410
        ypos 100
        spacing 18
        for header, entries in kt_wvp_sp_groups():
            vbox:
                spacing 4
                text header font KT_FONT size 14 color "#ff8fc8" bold True
                null height 4
                for idx, ci, title in entries:
                    button:
                        xsize 262
                        padding (8, 4, 8, 4)
                        background ("#1a2c4a" if wvp_sp == idx else "#0a1220")
                        hover_background "#14203a"
                        action SetScreenVariable("wvp_sp", idx)
                        hbox:
                            spacing 8
                            add Solid(KT_PAL[ci]) xsize 5 ysize 16 yalign 0.5
                            text title font KT_FONT size 11 yalign 0.5 color ("#f5faff" if wvp_sp == idx else "#9aa8bd")

    # --- footer: full names of the current pick + confirm/back ----------------
    add Solid("#ff8fc833") xpos 40 ypos 636 xsize 1200 ysize 1
    vbox:
        xpos 40
        ypos 650
        spacing 4
        text ("NS   " + KT_NS_LABELS[wvp_ns]) font KT_FONT size 12 color "#ffd7e8"
        text ("SP   " + kt_wvp_sp_full(wvp_sp)) font KT_FONT size 12 color "#ffd7e8"
    hbox:
        xpos 1240
        ypos 656
        xanchor 1.0
        spacing 14
        button:
            padding (18, 8, 18, 8)
            background "#2a1220"
            hover_background "#3d1c30"
            action Return(None)
            text "BACK" font KT_FONT size 14 color "#9aa8bd" bold True
        button:
            padding (18, 8, 18, 8)
            background "#ff8fc8"
            hover_background "#ffb1d8"
            action Return((wvp_ns, wvp_sp))
            text "READ THIS PAGE" font KT_FONT size 14 color "#02040b" bold True

    key "K_ESCAPE" action Return(None)

screen koto_keyboard_notice():
    style_prefix "hw"
    modal True
    use enter_m_input_lock()
    add Solid("#000000")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 720
        padding (0, 0, 0, 0)
        background "#d4d0c8"

        vbox:
            spacing 0

            frame:
                xsize 720
                ysize 26
                padding (8, 4, 8, 4)
                background "#0a246a"
                text "Keyboard Notice":
                    color "#ffffff"
                    bold True
                    size 12
                    yalign 0.5

            frame:
                xsize 720
                padding (24, 22, 24, 18)
                background "#ffffff"
                vbox:
                    spacing 14
                    text "This mode can only be played with a keyboard.":
                        color "#000000"
                        bold True
                        size 15
                        xsize 672

            frame:
                xsize 720
                padding (0, 8, 18, 16)
                background "#d4d0c8"
                hbox:
                    xalign 1.0
                    spacing 10
                    button:
                        background "#0a246a"
                        hover_background "#245edb"
                        padding (18, 6, 18, 6)
                        hover_sound gui.hover_sound
                        activate_sound gui.activate_sound
                        action Return("continue")
                        text "Continue":
                            color "#ffffff"
                            bold True
                            size 13

# --- THE PAUSE PANEL -----------------------------------------------------------
# Screen language, not CDD blits, for one reason: the AUDIO block. A mixer
# slider is a draggable widget, and a Creator-Defined Displayable can draw one
# but can never be one -- so the whole panel moved out here when the volume did.
#
# It carries the SAME `Preference("...volume")` bars the Settings screen and the
# Matsuda fight's pause menu use, so this is the game's one persistent mix being
# nudged mid-run, not a per-fight copy of it. Kotonoha's stage music rides the
# `music` mixer and every stage cue rides `sfx`, so both bars are live here.
#
# The dim behind it is still drawn inside KTStage, over the PLAYFIELD ONLY, so
# the score/lives/bombs HUD on the right stays readable while you are stopped.
screen kt_pause_panel(game):

    frame:
        style "kt_pause_frame"
        xpos (KT_SX + KT_W // 2)
        xanchor 0.5
        ypos (KT_SY + KT_H // 2)
        yanchor 0.5

        vbox:
            spacing 12
            xsize 396

            text "PAUSED" style "kt_pause_title" xalign 0.5

            add Solid("#ff8fc855") xysize (396, 2)

            hbox:
                spacing 10
                add Solid("#ff8fc8") xysize (4, 18) yalign 0.5
                text "AUDIO" style "kt_pause_section" yalign 0.5

            vbox:
                spacing 5

                if config.has_music:
                    text "MUSIC" style "kt_pause_small"
                    bar value Preference("music volume") style "kt_pause_slider"
                    null height 8

                if config.has_sound:
                    text "SOUND" style "kt_pause_small"
                    bar value Preference("sound volume") style "kt_pause_slider"
                    null height 8

                if config.has_voice:
                    text "VOICE" style "kt_pause_small"
                    bar value Preference("voice volume") style "kt_pause_slider"
                    null height 8

                if config.has_music or config.has_sound or config.has_voice:
                    textbutton _("MUTE ALL"):
                        style "kt_pause_button"
                        action Preference("all mute", "toggle")

            add Solid("#ff8fc82f") xysize (396, 2)

            hbox:
                xalign 0.5
                spacing 24

                textbutton _("RESUME"):
                    style "kt_pause_button"
                    action Function(game.toggle_pause)

                # Endless Practice has no game over, so leaving is the only
                # way a run ends -- it is not giving up on anything.
                textbutton (_("END RUN") if (game.endless and game.practice) else _("GIVE UP")):
                    style "kt_pause_quit_button"
                    action Function(game.give_up)

            text ("ESC  RESUME        Q  END RUN" if (game.endless and game.practice) else "ESC  RESUME        Q  GIVE UP"):
                style "kt_pause_hint"
                xalign 0.5


screen kototouhou_screen(game):
    modal True
    use enter_m_input_lock()

    # THE game. Backdrop, panel masks and cabinet trim are drawn by KTStage
    # itself now -- see the chrome block at the top of its render(). They moved
    # in so that this screen holds NOTHING that animates: the backdrop's
    # breathing zoom was an ATL loop, and ATL asks for its next frame with a
    # zero delay, which meant the fight redrew at the panel's refresh rate no
    # matter what KTStage's own draw-rate governor asked for.
    add KTStage(game)

    # Right-panel footer.
    text "KOTONOHA  KATSURA" style "msbf_shmup_card_kicker":
        xpos (KT_SX + KT_W + 42)
        ypos 26
    text "Z SHOOT   X BOMB   ARROWS MOVE   SHIFT FOCUS   ESC PAUSE" style "msbf_shmup_controls_small":
        xpos (KT_SX + KT_W + 42)
        ypos 690

    if game.paused:
        use kt_pause_panel(game)

    key "K_ESCAPE" action Function(game.toggle_pause)
    key "mouseup_3" action Function(game.toggle_pause)
    if game.paused:
        key "K_q" action Function(game.give_up)

    # _update_screens=False: a None poll must NOT restart the interaction (that
    # would rebuild KTStage 4x/sec and bleed the sim's time accumulator).
    timer 0.25 repeat True action Function(kt_poll_result, game, _update_screens=False)

# --- STORY WRAPPER ---------------------------------------------------------------
# (Audio define + state defaults live at the top of the file.)

# Entry point -- jumped from cs_matsuda_02's roster menu (Matsuda is on screen,
# bg ether, enterm playing).
label kototouhou:
    $ kt_continue_bar = 0
    $ kt_continues = 0
    $ kt_practice = False
    $ kt_debug = False
    $ kt_endless = False
    $ kt_debug_wave = False

    if persistent.kotomode_cleared:
        ma "Back for Kotonoha again? Guess the survivor's high is a hell of a drug."
        ma "You know where the stage is. Try not to redecorate it with your face this time."
    else:
        ma "Rules are on the tin: Z to shoot, X to bomb, arrows to move, Shift to focus if you enjoy seeing exactly how small your hitbox is."
        ma "Rack up points and breaking her bars pays you back in extends and spell stock. That's the economy. Don't be stingy with bombs, dying is worse."
        ma "Oh, and house rule: a game over means the WHOLE recital starts over. No checkpoints, no save states. She was extremely insistent about that part."
        ma "If that scares you, she does offer a...let's call it a 'guided reading'. You'll see the option. No judgment here. {size=-10}(Some judgment.){/size}"
        ma "...Right then. She's been waiting. She's VERY patient, which is...kind of the problem."

    show matsuda at thide
    hide matsuda
    stop music fadeout 1.0
    scene black with dissolve_scene_full
    pause 0.8

    scene koto_backdrop with dissolve_scene_full
    play music dream
    show kotonoha neut at t11 zorder 2

    if persistent.kotomode_cleared:
        ko "Ah. Welcome back."
        ko "Would you like another reading?"
    else:
        ko "Oh... you came."
        ko "She said somebody might. I didn't believe her. People don't usually pick me."
        ko "I made this place myself. The moon, the lanterns, the water... Every bullet, too."
        ko "There are eight of them. Eight people I've been. The polite one, the diligent one, the one nobody looked at twice..."
        ko "I kept every single one. That's my talent, you know. Keeping going... It's a blessing. {size=-8}...And a curse.{/size}"
        ko "I'd like you to read them all. ...You can't skim. You have to dodge every word."
        ko "So....."

    menu:
        "I'm ready. Let's dance.":
            ko "\"Dance.\" That's a nice way to put it."
            ko "Then...please don't die in the first stanza. It'd be embarrassing for both of us."
        "Eight bars seems excessive.":
            ko "Does it? I cut it down from twenty."
            ko "Seeing the fruits of your labor is mostly editing."
        "Actually, never mind.":
            ko "...Oh."
            ko "That's fine. Everyone says that. Go on, then."
            show kotonoha neut at thide
            hide kotonoha
            scene black with dissolve_scene_full
            stop music fadeout 1.0
            play music theme_matsuda_a
            scene bg matsudavr with dissolve_scene_full
            show matsuda neut at t11 zorder 2
            ma "Smart. You're a total pansy, but at least you're alive. Who else?"
            jump msbf_roster_choice

label kototouhou_mode_select:
    # The wave viewer routes BACK here after its one bar (and its picker can
    # be backed out of), so the forced-wave flag must not leak into whichever
    # mode gets chosen next -- the other menu branches never touch it.
    $ kt_debug_wave = False
    ko "And one last thing: how would you like to read it?"

    menu:
        "For real. (5 lives -- a game over restarts the whole fight)":
            $ kt_practice = False
            $ kt_debug = False
            $ kt_endless = False
            ko "...Good. It only means something if it can end."
            ko "I'll try to make it beautiful."
        "Endless reading. (5 lives, random forever -- survive as long as you can)":
            $ kt_practice = False
            $ kt_debug = False
            $ kt_endless = True
            ko "There's no last page to this one, so I'm sure this would attract more hardcore players."
            ko "Not to mention some quote-unquote 'cut content' that truthfully would have been too on the nose."
            ko "...Well, have at you, then."
        "Practice mode. (unlimited lives, but it doesn't count)":
            $ kt_practice = True
            $ kt_debug = False
            $ kt_endless = False
            ko "Oh. The...annotated edition. With the training wheels."
            ko "That's completely fine. Everyone starts somewhere."
            ma "{i}(from somewhere offstage){/i} NOOOOOOB!"
            ko "...She means it with love. Probably. No high score for you, though."
        "Endless practice. (unlimited lives, random forever -- no records)":
            $ kt_practice = True
            $ kt_debug = False
            $ kt_endless = True
            ko "Every page, shuffled, with no last one. And you can't run out of lives."
            ko "So it isn't a reading, exactly. It's more like standing out in the rain on purpose."
            ma "{i}(from the booth){/i} THIS one's for the adrenaline junkies! No stakes, all spectacle! Go feel like a legend!"
            ko "Nothing gets written down. ...I'll still be watching, though."
        "Debug reading. (DEV ONLY: every shot one-shots a bar)" if config.developer:
            $ kt_practice = False
            $ kt_debug = True
            $ kt_endless = False
            ko "...You brought a red pen to a poetry reading."
            ko "Fine. Skim it. Cross out whole stanzas if you must. The margins will remember."
            ma "{i}(from the booth){/i} Oi, that's MY console! Fine, FINE! Just don't leak the ending!"
        "Debug wave viewer. (DEV ONLY: read any one wave, your pick)" if config.developer:
            $ kt_practice = True
            $ kt_debug = False
            $ kt_endless = False
            $ kt_debug_wave = True
            ko "A private reading of one page? That's rather particular."
            ko "...I respect it. Pick the page."
            # Use a native screen call so automatic window management owns the
            # dialogue-to-picker handoff. Normalize defensive non-tuple returns.
            call screen kt_wave_picker
            $ _kt_pick = _return if isinstance(_return, tuple) and len(_return) == 2 else None
            if _kt_pick is None:
                ko "...Changed your mind mid-shelf? That's fine. Pick a different reading."
                jump kototouhou_mode_select
            $ kt_dbwave_ns = _kt_pick[0]
            $ kt_dbwave_sp = _kt_pick[1]
            ko "Noted. One page, cover to cover. Then you bring the book back."

    show kotonoha neut at thide
    hide kotonoha
    scene black with dissolve_scene_full
    stop music fadeout 1.2

    # This is a normal keyboard notice screen before the CDD takes over.
    # The actual fight does not use the dialogue window or quick menu.
    call screen koto_keyboard_notice

label kototouhou_fight:
    # Rollback through a live real-time minigame is nonsense: it would restore
    # script state without necessarily restoring the external-feeling key/input
    # timing the player just performed.
    $ renpy.block_rollback()

    # Construct the simulation immediately before the screen call. The game
    # object is not saved for later; _finish() snapshots the result into
    # kt_last_* before the interaction ends.
    $ kt_game = KTGame(start_bar=kt_continue_bar, continues_used=kt_continues, practice=kt_practice, debug=kt_debug, endless=kt_endless, debug_wave=((kt_dbwave_ns, kt_dbwave_sp) if kt_debug_wave else None))

    # Hide VN affordances during the arcade segment. The pause overlay is drawn
    # by KTStage, and the usual game menu is disabled so Save/Load cannot open
    # over a mutable 60Hz battle state.
    $ _kt_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ _kt_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None
    scene black
    # Endless Mode rides its own survival loop; the fixed run keeps the boss theme.
    if kt_endless:
        play music kt_endless_theme
    else:
        play music kt_boss_theme
    call screen kototouhou_screen(kt_game)
    $ _kt_result = _return

    # Restore script/UI state before branching back into VN dialogue.
    $ kt_game = None
    $ quick_menu = _kt_prev_quick_menu
    $ _game_menu_screen = _kt_prev_game_menu
    stop music fadeout 2.0
    scene black with dissolve_scene_full

    # EVERYTHING THIS RUN EARNED, AWARDED ABOVE THE ARCADE/STORY SPLIT, so both
    # paths award identically and the result labels below only render.
    #
    # PRACTICE never grants (unlimited lives), but DEBUG runs DO -- that's the
    # sanctioned way to test this without an hour of legit play, and the debug
    # option only exists in developer builds. A real clear also gets an explicit
    # event grant here; kotomode_cleared remains the recovery path for old saves.
    # Debug keeps the RECORDS pencil-only ("debugger's ink doesn't keep":
    # _finish leaves kotomode_cleared/hiscore untouched), while the explicit
    # event hook still lets the developer validate the trophy.
    if _kt_result == "victory" and not (kt_last_practice or kt_last_endless):
        $ ach_grant("koto_clear")
    # Reconcile any older completed objective here, not at the next Archive open.
    $ ach_sync()

    # ARCADE: skip all VN result dialogue -> shared arcade results card. Inert in
    # the in-story path (arcade_active is only ever set by game/addons/Arcade).
    if arcade_active:
        jump arcade_koto_result

    if _kt_result == "victory":
        jump kototouhou_victory
    elif _kt_result == "wave_done":
        jump kototouhou_wave_done
    elif _kt_result == "quit":
        jump kototouhou_quit
    jump kototouhou_defeat

# Wave viewer only (DEV): the forced bar was read once, front half and back.
# Restore the shrine and hand the dev straight back to the mode selector --
# no records, no victory lap, just the next pick.
label kototouhou_wave_done:
    scene koto_backdrop with dissolve_scene_full
    play music dream
    show kotonoha neut at t11 zorder 2
    ko "...And that's that page, cover to cover."
    ko "Well? Another one? Or shall we read it properly this time?"
    jump kototouhou_mode_select

label kototouhou_defeat:
    # The displayable is gone now; use the snapshot fields KTGame._finish()
    # copied into the store.
    $ kt_score_str = format(kt_last_score, ",")
    $ kt_defeat_bar = kt_last_bar_index + 1
    # _finish already folded this run into the persistent records. There are no
    # live endless trophies today, but this keeps old-save reconciliation local
    # to the mode result rather than deferring it to the Archive.
    $ ach_sync()

    if kt_last_endless:
        # Endless has no bars to reference -- it's waves survived + best. Both
        # kt_last_endless_wave and the persistent record are 0-based wave
        # indexes; display them +1. _finish already folded THIS run into the
        # record, so this run set a new best iff it equals the stored record.
        $ kt_waves = kt_last_endless_wave + 1
        $ kt_best_waves = persistent.kotomode_endless_wave + 1
        $ kt_endless_hi = format(persistent.kotomode_endless_hiscore, ",")
        $ kt_new_best = (kt_last_endless_wave >= persistent.kotomode_endless_wave)
        ko "...Oh. You're down. Here I was, almost forgetting you could even stop."
        ko "[kt_waves] waves and [kt_score_str] points. Not bad at all."
        if kt_new_best and kt_waves > 1:
            ko "Oh, and look at that. You set a new record. Go you."
        else:
            ko "Your best is still [kt_best_waves] waves, [kt_endless_hi] points. ...I've been counting. I count everything."

        menu:
            "Drop me in again, boss.":
                $ kt_continue_bar = 0
                $ kt_continues = 0
                ko "Yes. Keep reading. There's always another wave..."
                scene black with dissolve_scene_full
                jump kototouhou_fight
            "Leave.":
                ko "...I understand. Endless is a lot to ask of anyone."
                ko "The stage will keep, but so will I."
                scene black with dissolve_scene_full
                return

    ko "...Oh no. Ooooh, no no no. Get up. Please?"
    ko "You made it to bar [kt_defeat_bar] of 8, and you scored [kt_score_str]. That's...that's really good. It really is."

    menu:
        "Restart from the very top.":
            $ kt_continue_bar = 0
            $ kt_continues = 0
            ko "From the first line? You really do want to read it properly..."
            scene black with dissolve_scene_full
            jump kototouhou_fight
        "Leave.":
            ko "...I understand. It was a lot. It's always a lot."
            ko "The stage will keep, but so will I."
            scene black with dissolve_scene_full
            return

label kototouhou_quit:
    if kt_last_endless and kt_last_practice:
        # Endless Practice cannot end any other way, so this is its results
        # screen, not a scolding. kt_last_endless_wave is the 0-based wave in
        # progress when the run ended.
        $ kt_waves = kt_last_endless_wave + 1
        $ kt_score_str = format(kt_last_score, ",")
        ko "...And you close the book. That's allowed, in this one."
        ko "You reached wave [kt_waves], with [kt_score_str] points."
        if kt_last_deaths == 0:
            ko "And you never fell once. That's the kind of thing I'd write down, if this one kept records."
        elif kt_last_deaths == 1:
            ko "You fell once, and you got up once. That's the whole trick, really."
        else:
            ko "You fell [kt_last_deaths] times and got up [kt_last_deaths] times. I counted."

        menu:
            "Deal me back in.":
                $ kt_continue_bar = 0
                $ kt_continues = 0
                ko "Of course. It's still raining."
                scene black with dissolve_scene_full
                jump kototouhou_fight
            "Leave.":
                ko "Then go and dry off. The pages will keep."
                scene black with dissolve_scene_full
                return

    ko "You stopped mid-sentence."
    ko "...That's ruder than dying, you know."

    menu:
        "Sorry. Deal me back in.":
            $ kt_continue_bar = 0
            $ kt_continues = 0
            ko "Forgiven. Completely. Instantly. ...Don't do it again."
            scene black with dissolve_scene_full
            jump kototouhou_fight
        "I need to go.":
            ko "Then go. I'll reread the opening by myself."
            scene black with dissolve_scene_full
            return

label kototouhou_victory:
    pause 1.0
    scene koto_backdrop with dissolve_scene_full
    show kotonoha neut at t11 zorder 2
    # Same result snapshot as defeat/quit. Practice/debug status is checked
    # below so Kotonoha can acknowledge no-record clears without altering the
    # simulation result path.
    $ kt_score_str = format(kt_last_score, ",")
    $ kt_caps = kt_last_captures

    ko "...You read all of it."
    ko "All eight. Every pellet, every blade, every version hidden in the margins."
    if kt_caps >= 8:
        ko "And you captured every single spell card. All eight seals, unbroken. Nobody was ever supposed to do that."
        ko "...I don't know whether to frame you or fear you."
    elif kt_caps >= 4:
        ko "You even captured [kt_caps] of my spell cards. You were really listening, weren't you?"
    elif kt_caps >= 1:
        ko "You captured [kt_caps] of the cards, too. The rest...we can call those first drafts."
    else:
        ko "You bombed every card, though. Skimmed the whole thing like an airport paperback."
        ko "...Effective."
    if kt_last_debug:
        ko "Final score, [kt_score_str]. Written in pencil. Debugger's ink doesn't keep."
    elif kt_last_practice:
        ko "Final score, [kt_score_str]. It doesn't go in the record, but...you still read it. That matters to me."
    else:
        ko "Final score, [kt_score_str]. I'll write it on the moon so I don't forget."
    ko "Thank you for the dance. Truly. Come read to me again sometime..."
    ko "...or I'll come read to you."

    show kotonoha neut at thide
    hide kotonoha
    scene black with dissolve_scene_full
    pause 1.0
    play music theme_matsuda_a
    scene bg matsudavr with dissolve_scene_full
    show matsuda neut at t11 zorder 2

    ma "...You're alive. You're actually alive. {i}HOW{/i} are you alive?!"
    ma "I watched the whole thing from the booth! Bar six I started drafting your eulogy--it rhymed and everything!"
    if kt_caps >= 8:
        ma "A perfect all-capture run, too... I'm not saying it's the most impressive thing this stupid engine has ever rendered, but the engine is."
    ma "...Oh, who am I kidding? This was piss easy compared to modern shmup standards"
    ma "Anyway. That's the Kotonoha act. Tell literally everyone, my ticket sales depend on it."
    ma "Now scram before she writes a ninth bar about you specifically. GIDDOUT!"

    stop music fadeout 2.0
    scene black with dissolve_scene_full
    pause 1.5
    return


# =============================================================================
# PAUSE PANEL STYLES
# =============================================================================
# Her palette, not the Archive's: #ff8fc8 pink trim on #02040b, SF Automaton for
# the plate text. Font paths are spelled out rather than read from KT_FONT --
# style statements and the init python block that defines KT_FONT share init
# priority 0, and the project already writes them out this way (see
# msbf_shmup_card_name in fx.rpy).

style kt_pause_frame:
    background Solid("#02040bee")
    padding (22, 18)

style kt_pause_title:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 36
    color "#f5faff"
    bold True
    kerning 2.0
    outlines [(2, "#02040b", 0, 0), (1, "#ff8fc888", 1, 1)]

style kt_pause_section:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 17
    color "#ffd7e8"
    bold True
    kerning 2.0
    outlines [(2, "#02040b", 0, 0)]

style kt_pause_small:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 13
    color "#9aa8bd"
    bold True
    kerning 3.0
    outlines [(1, "#02040b", 0, 0)]

style kt_pause_hint:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 12
    color "#6f7c90"
    bold True
    kerning 2.0
    outlines [(1, "#02040b", 0, 0)]

# is slider_slider so the drag feel and the log scale match Settings and the
# Matsuda pause menu exactly; only the width and the trim colour differ.
style kt_pause_slider is slider_slider:
    xsize 396
    ysize 12
    base_bar Solid("#152134")
    thumb Solid("#ff8fc8")
    hover_thumb Solid("#ffd7e8")

style kt_pause_button:
    xsize 168
    ysize 34
    background Solid("#0d1524dd")
    hover_background Solid("#3a1a2ef2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (10, 6)

style kt_pause_button_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 15
    color "#9aa8bd"
    hover_color "#ffd7e8"
    bold True
    kerning 2.0
    xalign 0.5
    yalign 0.5
    outlines [(1, "#02040b", 0, 0)]

style kt_pause_quit_button is kt_pause_button:
    hover_background Solid("#4a1020f2")

style kt_pause_quit_button_text is kt_pause_button_text:
    hover_color "#ff6b8f"
