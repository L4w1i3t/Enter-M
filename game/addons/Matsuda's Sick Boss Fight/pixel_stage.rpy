# =============================================================================
# pixel_stage.rpy  --  ONTOLOGICAL SEER :: THE PIXEL STAGE
# =============================================================================
#
# WHAT THIS FILE IS
#   The world layer of both Seer fights (Normal and Id Mode) and of their
#   entrances. Everybody standing in the room is a PIXEL SPRITE now: the party
#   at 2x on the right in a Final Fantasy side-view formation, Matsuda at 3x on
#   the left, big enough that her later forms run off the frame.
#
#   The illustrated archetypes are still the party's official designs -- the
#   party select shows them -- and Matsuda's three illustrated forms are still
#   defined (msbf_matsuda_phase1..3) for the gacha cards and the archive. The
#   sprites here are DERIVED from that art; nothing in this file draws a
#   character by hand.
#
# HOW A SPRITE MOVES WITHOUT EVER LOOKING FILTERED
#   msbf.px samples its texture at ART-PIXEL CENTRES. Every warp (breathing,
#   lean, wings, writhing, squash) is evaluated per art pixel and then the
#   nearest texel is taken, so a bent sprite is still made of whole, crisp
#   pixels -- it moves like hand-animated pixel art, not like a scaled bitmap.
#   Whole-sprite motion (dashes, jumps, knockback) is snapped to the sprite's
#   own pixel grid for the same reason.
#
# WHO DECIDES WHAT ANIMATES
#   MSBFPixelStage only READS the battle (fx_event/fx_serial, float_events,
#   alive/guard/hp, current_actor) plus one presentation bus, MSBF_PX_BUS, that
#   screen ACTIONS write when the player commits a move. It owns its own
#   animation clocks and never writes game state -- so a save, a reload or a
#   screen prediction pass cannot be changed by anything in here.
# =============================================================================

init -10 python:
    import json as _msbf_px_json

    def _msbf_register_px_shaders():

        # ---- THE ACTOR SHADER ---------------------------------------------
        # One draw per sprite, for BOTH battle-art styles. Everything is
        # computed in ART UNITS -- the pixel sprite's own pixels -- so a pose
        # means the same thing whichever texture is bound:
        #   pixel art   : u_px_unit 1, u_px_hq 0. The fragment is snapped to
        #                 an art-pixel cell and the texel centre is taken, so
        #                 a bent sprite is still whole, crisp pixels.
        #   illustrated : u_px_unit = texels per art pixel (pixel/hq/*), u_px_hq
        #                 1. Sampling is continuous and soft alpha is kept --
        #                 unless the genre is failing (u_px_block >= 2), which
        #                 pixelates the illustration itself.
        # Every uniform below is always supplied by the stage.
        renpy.register_shader("msbf.px", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_model_size;
            uniform float u_time;
            uniform vec2 u_px_foot;
            uniform vec2 u_px_head;
            uniform float u_px_breath;
            uniform float u_px_lean;
            uniform vec2 u_px_scale;
            uniform vec4 u_px_flow;
            uniform vec4 u_px_wing;
            uniform float u_px_writhe;
            uniform float u_px_flash;
            uniform vec4 u_px_tint;
            uniform float u_px_grey;
            uniform vec4 u_px_outline;
            uniform vec4 u_px_rim;
            uniform float u_px_block;
            uniform float u_px_poster;
            uniform float u_px_tear;
            uniform float u_px_dissolve;
            uniform float u_px_seed;
            uniform float u_px_unit;
            uniform float u_px_hq;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float px_hash(vec2 p, float seed) {
                return fract(sin(dot(p, vec2(12.9898, 78.233)) + seed * 7.13) * 43758.5453);
            }
            // s is in ART units. Pixel art reads the texel under the art
            // pixel; the illustration reads continuously.
            vec4 px_tap(sampler2D tex, vec2 s, vec2 size, float unit, float hq) {
                vec2 c = hq > 0.5 ? s * unit : floor(s) + 0.5;
                if (c.x < 0.0 || c.y < 0.0 || c.x > size.x || c.y > size.y) {
                    return vec4(0.0);
                }
                return texture2D(tex, c / size);
            }
        """, fragment_300="""
            vec2 size = u_model_size;
            float unit = max(0.001, u_px_unit);
            float hq = u_px_hq;
            float blk = max(1.0, floor(u_px_block + 0.5));
            vec2 tp = v_tex_coord * size;
            vec2 p;
            if (hq > 0.5 && blk < 1.5) {
                p = tp / unit;
            } else {
                float cell = blk * (hq > 0.5 ? unit : 1.0);
                p = (floor(tp / cell) + 0.5) * cell / unit;
            }

            // Genre rupture: whole rows slip sideways on a stepped clock.
            if (u_px_tear > 0.0) {
                float row = floor(p.y / 5.0);
                float tick = floor(u_time * 11.0);
                float h = px_hash(vec2(row, tick), u_px_seed);
                p.x += step(0.70, h) * (h - 0.85) * 6.0 * u_px_tear;
            }

            float span = max(1.0, u_px_foot.y - u_px_head.y);
            vec2 s = p;

            // Squash / stretch about the feet.
            s = u_px_foot + (s - u_px_foot) / max(u_px_scale, vec2(0.05));
            float hgt = clamp((u_px_foot.y - s.y) / span, 0.0, 1.4);

            // Breathing compresses the body toward the feet; lean shears it.
            s.y -= u_px_breath * hgt;
            s.x -= u_px_lean * hgt * hgt;

            // Secondary motion: the further a pixel is from the body's axis,
            // the more it flutters -- hair, capes, wing tips, tendrils.
            float ext = clamp(abs(s.x - u_px_head.x) / (span * 0.42), 0.0, 1.3);
            ext *= ext;
            s.x -= u_px_flow.x * ext * sin(s.y * u_px_flow.y + u_time * u_px_flow.z + u_px_flow.w);
            s.y -= u_px_flow.x * 0.45 * ext * cos(s.x * u_px_flow.y * 0.8 + u_time * u_px_flow.z * 0.9);

            // Wings: each side turns about its own root, more toward the tips.
            if (abs(u_px_wing.x) > 0.001) {
                float side = s.x < u_px_head.x ? -1.0 : 1.0;
                vec2 root = vec2(u_px_head.x + side * u_px_wing.y, u_px_head.y + u_px_wing.w);
                float w = smoothstep(u_px_wing.y, u_px_wing.y + u_px_wing.z, abs(s.x - u_px_head.x));
                float a = radians(u_px_wing.x) * w * side;
                vec2 v = s - root;
                float ca = cos(a);
                float sa = sin(a);
                s = root + vec2(ca * v.x - sa * v.y, sa * v.x + ca * v.y);
            }

            // Writhing: smooth noise displacement growing away from her core.
            if (u_px_writhe > 0.001) {
                float d = length((s - u_px_head) / span);
                float k = clamp(d - 0.22, 0.0, 1.6);
                vec2 n = vec2(sin(s.y * 0.13 + u_time * 2.3) + sin(s.x * 0.071 - u_time * 1.7 + s.y * 0.04),
                            cos(s.x * 0.09 + u_time * 1.9) + sin(s.y * 0.057 + u_time * 2.9));
                s += n * 0.5 * u_px_writhe * k;
            }

            vec4 col = px_tap(tex0, s, size, unit, hq);
            float a = col.a;
            vec3 rgb = a > 0.0001 ? col.rgb / a : vec3(0.0);
            if (a > 0.0001) {
                // Rim light on the edge that faces the key light; the sign of
                // rim.a is the side it comes from.
                if (abs(u_px_rim.a) > 0.0) {
                    float side = u_px_rim.a > 0.0 ? 1.0 : -1.0;
                    float edge = 1.0 - px_tap(tex0, s + vec2(side, 0.0), size, unit, hq).a;
                    float top = 1.0 - px_tap(tex0, s + vec2(0.0, -1.0), size, unit, hq).a;
                    rgb = mix(rgb, u_px_rim.rgb, clamp(max(edge, top * 0.6), 0.0, 1.0) * min(1.0, abs(u_px_rim.a)));
                }
                float lum = dot(rgb, vec3(0.30, 0.59, 0.11));
                rgb = mix(rgb, vec3(lum) * 0.55 + vec3(0.02, 0.02, 0.05), u_px_grey);
                rgb = mix(rgb, u_px_tint.rgb * (0.35 + lum * 1.25), u_px_tint.a);
                if (u_px_poster > 0.5) {
                    rgb = floor(rgb * u_px_poster + 0.5) / u_px_poster;
                }
                rgb = mix(rgb, vec3(1.0), u_px_flash);
            }
            vec4 outc = vec4(rgb * a, a);

            // Selection outline, one art unit thick, laid UNDER the figure.
            if (u_px_outline.a > 0.0 && a < 0.999) {
                float n4 = max(max(px_tap(tex0, s + vec2(1.0, 0.0), size, unit, hq).a,
                                    px_tap(tex0, s - vec2(1.0, 0.0), size, unit, hq).a),
                                max(px_tap(tex0, s + vec2(0.0, 1.0), size, unit, hq).a,
                                    px_tap(tex0, s - vec2(0.0, 1.0), size, unit, hq).a));
                float oa = u_px_outline.a * n4;
                outc = outc + vec4(u_px_outline.rgb * oa, oa) * (1.0 - outc.a);
            }

            if (u_px_dissolve > 0.0) {
                float hd = px_hash(floor(p / blk), u_px_seed);
                if (hd < u_px_dissolve) {
                    outc = vec4(0.0);
                }
            }
            gl_FragColor = outc;
        """)

        # ---- PIXEL FX ------------------------------------------------------
        # Spell and impact effects drawn on the same pixel grid as the sprites
        # they land on: computed per CELL (u_fx_cell screen px), then banded to
        # three colours with a little ordered noise -- a hand-pixelled effect's
        # palette, not a soft glow. The output alpha is held below the colour
        # so it lands partly additive and reads as light on a dark deck.
        renpy.register_shader("msbf.pxfx", variables="""
            uniform vec2 u_model_size;
            uniform float u_time;
            uniform float u_fx_kind;
            uniform float u_fx_p;
            uniform float u_fx_cell;
            uniform vec3 u_fx_c1;
            uniform vec3 u_fx_c2;
            uniform vec3 u_fx_c3;
            uniform float u_fx_seed;
            uniform float u_fx_angle;
            uniform float u_fx_solid;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float fx_h1(float n, float seed) { return fract(sin(n * 127.1 + seed * 17.3) * 43758.5453); }
            float fx_h2(vec2 p, float seed) { return fract(sin(dot(p, vec2(12.9898, 78.233)) + seed * 3.1) * 43758.5453); }
        """, fragment_300="""
            vec2 grid = max(vec2(1.0), floor(u_model_size / max(1.0, u_fx_cell)));
            vec2 cell = floor(v_tex_coord * grid);
            vec2 uv = (cell + 0.5) / grid;
            vec2 q = (uv - 0.5) * 2.0;
            q.x *= u_model_size.x / u_model_size.y;
            float ca = cos(u_fx_angle);
            float sa = sin(u_fx_angle);
            vec2 qr = vec2(ca * q.x + sa * q.y, -sa * q.x + ca * q.y);
            float r = length(q);
            float ang = atan(q.y, q.x);
            float p = clamp(u_fx_p, 0.0, 1.0);
            float e = 0.0;
            int k = int(u_fx_kind + 0.5);

            if (k == 0) {
                // BURST: a hot core and uneven spikes thrown outward.
                float sp = pow(abs(cos(ang * 4.0 + fx_h1(1.0, u_fx_seed) * 6.28)), 16.0) * 0.65
                            + pow(abs(cos(ang * 7.0 + fx_h1(2.0, u_fx_seed) * 6.28)), 28.0) * 0.55;
                float reach = mix(0.20, 1.0, sqrt(p));
                float core = 1.0 - smoothstep(0.0, 0.42 * (1.0 - p) + 0.02, r);
                float ray = sp * (1.0 - smoothstep(reach * 0.55, reach, r));
                e = max(core * 1.25, ray * (1.15 - p));
            } else if (k == 1) {
                // RING: one shock ring opening out and thinning.
                float rad = mix(0.06, 0.96, sqrt(p));
                float w = mix(0.16, 0.035, p);
                e = (1.0 - smoothstep(0.0, w, abs(r - rad))) * (1.15 - p);
            } else if (k == 2) {
                // SLASH: a crescent swept along qr.x, thick in the middle.
                float yb = qr.y + 0.55 * (1.0 - qr.x * qr.x);
                float th = 0.16 * (1.0 - abs(qr.x)) + 0.02;
                float band = 1.0 - smoothstep(0.0, th, abs(yb));
                float head = smoothstep(-1.0, 1.0, qr.x - (p * 3.0 - 1.6));
                float tail = 1.0 - smoothstep(-1.0, 1.0, qr.x - (p * 3.0 - 0.4));
                e = band * (1.0 - head) * (1.0 - tail * 0.0) * step(abs(qr.x), 1.0) * (1.3 - p) * smoothstep(-1.2, -0.2, p * 3.0 - 1.6 - qr.x + 1.0);
            } else if (k == 3) {
                // SPARKLE: a field of plus-shaped twinkles rising.
                vec2 g = floor((uv + vec2(0.0, p * 0.35)) * 7.0);
                float hh = fx_h2(g, u_fx_seed);
                vec2 f = fract((uv + vec2(0.0, p * 0.35)) * 7.0) - 0.5;
                float tw = step(0.62, hh) * (0.6 + 0.4 * sin(u_time * 9.0 + hh * 40.0));
                float plus = (1.0 - smoothstep(0.03, 0.10, abs(f.x)) * 1.0) * (1.0 - smoothstep(0.0, 0.38, abs(f.y)))
                            + (1.0 - smoothstep(0.03, 0.10, abs(f.y))) * (1.0 - smoothstep(0.0, 0.38, abs(f.x)));
                e = clamp(plus, 0.0, 1.0) * tw * (1.1 - p) * (1.0 - smoothstep(0.75, 1.15, r));
            } else if (k == 4) {
                // PILLAR: a beam that drops in, widens, and thins away.
                float wdt = mix(0.05, 0.42, smoothstep(0.0, 0.35, p)) * (1.0 - smoothstep(0.55, 1.0, p));
                float drop = smoothstep(0.0, 0.25, p);
                float body = (1.0 - smoothstep(wdt * 0.5, wdt, abs(q.x))) * step(uv.y, drop + 0.02);
                e = body * (1.1 + 0.25 * sin(uv.y * 30.0 - u_time * 22.0));
            } else if (k == 5) {
                // BOLT: a jagged line down the long axis, re-cut every few frames.
                // Wrapped: u_time is seconds since launch, and past ~an hour
                // sin() in fx_h1 loses its precision and the bolt goes straight.
                float tick = mod(floor(u_time * 18.0), 64.0);
                float yy = uv.y * 9.0;
                float seg = floor(yy);
                float x0 = (fx_h1(seg + tick * 3.1, u_fx_seed) - 0.5) * 0.6;
                float x1 = (fx_h1(seg + 1.0 + tick * 3.1, u_fx_seed) - 0.5) * 0.6;
                float xl = mix(x0, x1, fract(yy));
                float d = abs(q.x - xl);
                e = (1.0 - smoothstep(0.0, 0.07, d)) * 1.3 + (1.0 - smoothstep(0.0, 0.22, d)) * 0.5;
                e *= step(uv.y, smoothstep(0.0, 0.3, p) + 0.02) * (1.15 - p);
            } else if (k == 6) {
                // SHARDS: angular fragments flying out of the centre.
                float sect = floor((ang + 3.14159) / 6.28318 * 9.0);
                float rr = mix(0.1, 1.0, sqrt(p)) * (0.65 + 0.35 * fx_h1(sect, u_fx_seed));
                float fa = fract((ang + 3.14159) / 6.28318 * 9.0) - 0.5;
                float shard = (1.0 - smoothstep(0.0, 0.22 * (1.0 - abs(r - rr) * 5.0), abs(fa)))
                            * (1.0 - smoothstep(0.0, 0.16, abs(r - rr)));
                e = shard * (1.2 - p) + (1.0 - smoothstep(0.0, 0.25 * (1.0 - p), r)) * 0.9;
            } else if (k == 7) {
                // FLAME: a licking plume rising off the base.
                float yb = 1.0 - uv.y;
                float wv = sin(uv.y * 14.0 - u_time * 16.0 + fx_h1(3.0, u_fx_seed) * 6.0) * 0.12 * yb;
                float wdt = (0.55 - yb * 0.45) * (0.4 + 0.6 * smoothstep(0.0, 0.3, p));
                e = (1.0 - smoothstep(wdt * 0.4, wdt, abs(q.x + wv))) * smoothstep(-0.05, 0.25, uv.y)
                    * (1.0 - smoothstep(0.55, 1.0, p)) * (0.75 + 0.6 * uv.y);
            } else {
                // CIRCLE: a rune ring turning on the deck under a caster.
                float rad = 0.78;
                float ringA = 1.0 - smoothstep(0.0, 0.05, abs(r - rad));
                float ringB = 1.0 - smoothstep(0.0, 0.035, abs(r - rad * 0.70));
                float tick = (ang + u_time * 1.6) / 6.28318 * 18.0;
                float runes = step(0.55, fract(tick)) * (1.0 - smoothstep(0.0, 0.07, abs(r - rad * 0.85)));
                e = (ringA + ringB * 0.8 + runes * 0.7) * smoothstep(0.0, 0.2, p) * (1.0 - smoothstep(0.8, 1.0, p));
            }

            float v = e + (fx_h2(cell, u_fx_seed) - 0.5) * 0.16;
            vec3 col = vec3(0.0);
            float a = 0.0;
            if (v > 0.78) {
                col = u_fx_c1;
                a = 1.0;
            } else if (v > 0.48) {
                col = u_fx_c2;
                a = 0.92;
            } else if (v > 0.24) {
                col = u_fx_c3;
                a = 0.70;
            }
            gl_FragColor = vec4(col * a, a * u_fx_solid);
        """)

    try:
        _msbf_register_px_shaders()
        MSBF_PX_SHADERS = True
    except Exception as _msbf_px_e:
        MSBF_PX_SHADERS = False
        if config.developer:
            renpy.log("MSBF PX: shader registration failed: %r" % (_msbf_px_e,))


# The player's Battle Art choice -- "pixel" or "hq" (Illustrated). Persistent
# because it is a taste, not a save-file fact; toggled from the fight's pause
# menu and from the party select.
default persistent.msbf_seer_art = "pixel"

# -----------------------------------------------------------------------------
# 1. THE SPRITE DATA + WHERE EVERYONE STANDS
# -----------------------------------------------------------------------------
init -5 python:

    MSBF_PX_DIR = "addons/Matsuda's Sick Boss Fight/"

    # BATTLE ART: "pixel" (the pixel sprites) or "hq" (the original
    # illustrations, drawn through the SAME stage: every dash, flash, warp and
    # glitch is shared, because the illustrated twins in pixel/hq/ sit on the
    # pixel sprites' canvases at the same anchors). Read live each frame, so
    # flipping it mid-fight changes the art on the next frame.
    MSBF_SEER_ART_STYLES = ("pixel", "hq")

    def msbf_seer_art_hq():
        return getattr(persistent, "msbf_seer_art", "pixel") == "hq"

    def _msbf_px_load_meta():
        try:
            with renpy.open_file(MSBF_PX_DIR + "pixel/sprites.json", encoding="utf-8") as fh:
                return _msbf_px_json.load(fh)
        except Exception:
            return {"party": {}, "boss": {}}

    MSBF_PX_META = _msbf_px_load_meta()

    def msbf_px_party_meta(member_id):
        return MSBF_PX_META.get("party", {}).get(member_id)

    def msbf_px_boss_meta(phase):
        try:
            phase = min(3, max(1, int(phase)))
        except (TypeError, ValueError):
            phase = 1
        return MSBF_PX_META.get("boss", {}).get(str(phase))

    def msbf_px_image(meta):
        return MSBF_PX_DIR + meta["file"]

    # ONE displayable object per sprite file, for the life of the process.
    # _draw_sprite builds a fresh mesh Transform every frame (its uniforms
    # move every frame), and a mesh renders its child to a texture -- which
    # the engine reuses only while the child render is the SAME object it
    # saw last frame. Handed a path string, the Transform made a new Image
    # each time, so every figure's texture was re-rendered every frame:
    # five to eight render-to-texture passes a frame that drew nothing new.
    # Not saved: an init-time dict of displayables, filled lazily.
    MSBF_PX_DISPS = {}

    def msbf_px_disp(path):
        d = MSBF_PX_DISPS.get(path)
        if d is None:
            if len(MSBF_PX_DISPS) > 600:
                MSBF_PX_DISPS.clear()
            d = MSBF_PX_DISPS[path] = renpy.displayable(path)
        return d

    # Her illustrated forms -- the sources of the pixel sprites, still defined
    # as msbf_matsuda_phase1..3 for the gacha cards and the archive. Phase 3
    # flickers back into this art when the genre fails.
    MSBF_PX_ILLUSTRATION = {
        1: MSBF_PX_DIR + "phase1.png",
        2: MSBF_PX_DIR + "phase2.png",
        3: MSBF_PX_DIR + "idmode/idphase.png",
    }

    # --- MATSUDA'S MARK ON THE FLOOR -----------------------------------------
    # The party stands on the LEFT and faces right; she stands on the RIGHT.
    # Per form: where the centre of her bounding box sits on screen (x) and
    # where its bottom edge sits (y). Forms 2 and 3 are deliberately TALLER
    # than the frame: the crown and the halo run off the top. That crop is the
    # sense of scale -- the party is looking up at something the camera can
    # not fit.
    MSBF_PX_BOSS_PLACE = {
        1: (846, 772),
        2: (852, 716),
        3: (846, 730),
    }
    # How far above the deck she floats, for her shadow (screen px).
    MSBF_PX_BOSS_HOVER = {1: 34, 2: 48, 3: 30}

    def _msbf_px_snap(v, scale):
        return int(round(float(v) / scale) * scale)

    def msbf_px_boss_origin(phase):
        """Top-left of her sprite on screen, at rest."""
        meta = msbf_px_boss_meta(phase)
        if not meta:
            return (0, 0)
        sc = meta["scale"]
        bx0, by0, bx1, by1 = meta["bbox"]
        px, py = MSBF_PX_BOSS_PLACE.get(int(phase), MSBF_PX_BOSS_PLACE[1])
        ox = px - ((bx0 + bx1) * 0.5) * sc
        oy = py - (by1 + 1) * sc
        return (_msbf_px_snap(ox, sc), _msbf_px_snap(oy, sc))

    def msbf_px_boss_point(phase, key="core"):
        """A named point of her rest pose (core/head/foot) in screen px."""
        meta = msbf_px_boss_meta(phase)
        if not meta:
            return (452, 300)
        ox, oy = msbf_px_boss_origin(phase)
        sc = meta["scale"]
        x, y = meta.get(key, meta["core"])
        return (int(ox + (x + 0.5) * sc), int(oy + (y + 0.5) * sc))

    # --- THE PARTY'S FORMATION ----------------------------------------------
    # Final Fantasy's side view crossed with Etrian Odyssey's two ranks: the
    # party stands on the LEFT, facing her, in two columns -- the FRONT row
    # nearer to her, the REAR row a long step back. Within a column members
    # stand top to bottom in party order, zig-zagged so no two heads line up,
    # and the whole formation leans with the floor (nearer = lower = further
    # from her). The row the player chose is visible on the deck, not only in a
    # stat block.
    MSBF_PX_COL_FRONT = 430      # front column x at the formation's middle
    MSBF_PX_COL_REAR = 190       # rear column x
    MSBF_PX_COL_LEAN = -0.20     # screen px of x per px of y (nearer = further left)
    MSBF_PX_COL_MID = 462        # foot y the column is centred on
    MSBF_PX_ZIG = 26             # alternate members step this far in and out
    MSBF_PX_COLUMN_Y = {
        # members in one column: their foot y values, top to bottom
        1: (466,), 2: (392, 546), 3: (356, 456, 556),
        4: (336, 412, 488, 564), 5: (326, 388, 450, 512, 574),
        6: (320, 372, 424, 476, 528, 580), 7: (316, 360, 404, 448, 492, 536, 580),
    }
    MSBF_PX_ACTIVE_STEP = 18     # art px the acting member steps forward
    # Which way "forward" is on screen. The pose code below is written in
    # FORWARD units (negative = toward the enemy, for both sides) and flipped
    # onto the screen by these, so the layout can swap sides in one place.
    MSBF_PX_PARTY_FACE = 1       # the party faces +x (she is to the right)
    MSBF_PX_BOSS_FACE = -1       # she faces -x

    def _msbf_px_shadow_tf(w, h, strength):
        return Transform(Solid("#00000000"), xysize=(w, h), mesh=True, shader="msbf.shadow",
                         u_sh_strength=strength, u_sh_soft=1.4)

    def msbf_px_live_rows(n):
        """The live party's rows, if the live party is n long."""
        b = getattr(store, "msbf_battle_state", None)
        try:
            if b is not None and len(b.party) == n:
                return [getattr(m, "row", "front") for m in b.party]
        except Exception:
            pass
        return ["front" if k < 2 else "rear" for k in range(n)]

    # The layout is a pure function of the rows, and the stage asks for it
    # several times a frame (every slot lookup recomputed the whole column
    # set: ~0.4ms of every fight frame, measured). One answer per row tuple;
    # callers get a fresh list, so nothing can mutate the cached one.
    _MSBF_PX_FORMATIONS = {}

    def msbf_px_formation(rows):
        """rows (one per member, party order) -> [(foot x, foot y)]."""
        key = tuple(rows)
        hit = _MSBF_PX_FORMATIONS.get(key)
        if hit is None:
            if len(_MSBF_PX_FORMATIONS) > 256:
                _MSBF_PX_FORMATIONS.clear()
            hit = _MSBF_PX_FORMATIONS[key] = tuple(_msbf_px_formation_build(rows))
        return list(hit)

    def _msbf_px_formation_build(rows):
        n = len(rows)
        out = [None] * n
        cols = (("front", MSBF_PX_COL_FRONT, 0), ("rear", MSBF_PX_COL_REAR, 22))
        for name, base, ydrop in cols:
            members = [k for k in range(n) if (rows[k] == "front") == (name == "front")]
            ys = MSBF_PX_COLUMN_Y.get(len(members), MSBF_PX_COLUMN_Y[7])
            for j, k in enumerate(members):
                y = ys[min(j, len(ys) - 1)] + ydrop
                x = base + (y - MSBF_PX_COL_MID) * MSBF_PX_COL_LEAN
                if len(members) > 1:
                    # The more crowded the column, the wider the stagger, so a
                    # four-deep front row still reads as four people.
                    zig = MSBF_PX_ZIG + 22 * max(0, min(3, len(members) - 2))
                    x += zig if (j % 2) else -zig
                out[k] = (_msbf_px_snap(x, 2), _msbf_px_snap(y, 2))
        return out

    def msbf_px_slot(i, n, row="front", rows=None):
        """Foot point of party member i of n, at rest, in screen px."""
        try:
            n = max(1, min(7, int(n)))
        except (TypeError, ValueError):
            n = 4
        rows = list(rows) if rows is not None else msbf_px_live_rows(n)
        if len(rows) != n:
            rows = ["front" if k < 2 else "rear" for k in range(n)]
        if 0 <= i < n:
            rows[i] = row
        return msbf_px_formation(rows)[max(0, min(n - 1, i))]

    def msbf_px_member_point(member_id, i, n, row="front", key="chest", active=False, rows=None):
        """A named point (chest/head/foot) of a member at rest, in screen px."""
        meta = msbf_px_party_meta(member_id)
        fx, fy = msbf_px_slot(i, n, row, rows)
        if active:
            fx += MSBF_PX_ACTIVE_STEP * 2 * MSBF_PX_PARTY_FACE
        if not meta:
            return (fx, fy - 90)
        sc = meta["scale"]
        mx, my = meta["foot"]
        x, y = meta.get(key, meta["chest"])
        return (int(fx + (x - mx) * sc), int(fy + (y - my) * sc))

    # --- THE PRESENTATION BUS ------------------------------------------------
    # Written ONLY by screen actions (never by a screen body), read by the
    # stage. Lives in an init-time dict, so it is never saved and never rolled
    # back -- it is a cue, not state.
    MSBF_PX_BUS = {"commit": None, "serial": 0}

    def msbf_px_cue_commit(actor_index, skill_id, target_index=None):
        MSBF_PX_BUS["serial"] += 1
        MSBF_PX_BUS["commit"] = (MSBF_PX_BUS["serial"], actor_index, skill_id, target_index)

    # How long the stage holds a committed move before it resolves. Long
    # enough to READ the wind-up (a dash, a leap, a spell circle) and short
    # enough that a turn still feels quick. The screen's resolve timer reads
    # this, so the impact always lands on the frame the choreography strikes.
    def msbf_px_commit_time(member_id, skill):
        style = msbf_px_move_style(member_id, skill)
        return {"dash": 0.36, "jump": 0.46, "heavy": 0.44, "throw": 0.30,
                "cast": 0.40, "support": 0.32, "guard": 0.18}.get(style, 0.30)

    # The entrances' running orders, shared by the stage (the figures) and the
    # screens in cinematics.rpy (the light, the cards, the sound).
    MSBF_PX_INTRO = {"run": 0.30, "fall": 2.05, "land": 2.50, "sweep": 3.30,
                        "card": 3.62, "end": 6.40}
    MSBF_PX_ID_INTRO = {"party": 0.25, "boss": 0.80, "unfold": 1.05, "light": 2.05,
                        "card": 2.45, "end": 5.10}

    # The longest commit is ~0.46s; anything still committed well past that
    # lost its follow-through cue and is sent home.
    MSBF_PX_COMMIT_TIMEOUT = 1.2

    MSBF_PX_PHYS_KINDS = ("damage", "dev_cleave")
    MSBF_PX_PHYS_ELEMENTS = ("weapon", "slash", "pierce")

    # Each fighter swings in character. Asahina is a halberdier, so her
    # physical moves are a Dragoon's JUMP; Sam's are a heavy overhead chop;
    # Himeko throws cards and never leaves her mark.
    MSBF_PX_FIGHT_STYLE = {
        "seeker": "dash", "monika": "dash", "kotonoha": "dash",
        "asahina": "jump", "sam": "heavy", "tsubaki": "dash", "himeko": "throw",
    }

    def msbf_px_move_style(member_id, skill):
        if skill is None:
            return "cast"
        kind = getattr(skill, "kind", "damage")
        element = getattr(skill, "element", "slash")
        if kind == "guard":
            return "guard"
        if kind in MSBF_PX_PHYS_KINDS and (element in MSBF_PX_PHYS_ELEMENTS or getattr(skill, "id", "") in ("ruin_edge", "cleave")):
            return MSBF_PX_FIGHT_STYLE.get(member_id, "dash") if member_id else "dash"
        if getattr(skill, "target", "boss") in ("party", "ally", "self") or kind in ("heal", "heal_all", "revive", "focus", "haste", "white_wind", "blue_guard", "buff_attack_all", "buff_defense_all"):
            return "support"
        return "cast"

    # Element -> (pixel FX kind, core, mid, edge) for impacts on her.
    # Kinds: 0 burst, 1 ring, 2 slash, 3 sparkle, 4 pillar, 5 bolt, 6 shards,
    # 7 flame, 8 circle.
    MSBF_PX_ELEMENT_FX = {
        "weapon":    (2, (1.0, 1.0, 1.0), (0.80, 0.90, 1.0), (0.40, 0.55, 0.85)),
        "slash":     (2, (1.0, 1.0, 1.0), (0.85, 0.92, 1.0), (0.45, 0.55, 0.80)),
        "pierce":    (6, (1.0, 1.0, 1.0), (0.70, 0.78, 1.0), (0.35, 0.40, 0.85)),
        "fire":      (7, (1.0, 0.95, 0.70), (1.0, 0.55, 0.20), (0.75, 0.15, 0.10)),
        "ice":       (6, (0.95, 1.0, 1.0), (0.45, 0.85, 1.0), (0.20, 0.40, 0.85)),
        "lightning": (5, (1.0, 1.0, 0.85), (1.0, 0.85, 0.30), (0.70, 0.45, 0.95)),
        "wind":      (1, (0.90, 1.0, 0.92), (0.50, 0.90, 0.62), (0.20, 0.55, 0.45)),
        "psychic":   (1, (1.0, 0.85, 1.0), (0.80, 0.45, 1.0), (0.45, 0.20, 0.70)),
        "almighty":  (0, (1.0, 1.0, 1.0), (1.0, 0.45, 0.70), (0.55, 0.15, 0.45)),
        "healing":   (3, (0.92, 1.0, 0.90), (0.45, 0.95, 0.60), (0.20, 0.60, 0.45)),
        "support":   (3, (1.0, 1.0, 0.95), (0.70, 0.85, 1.0), (0.40, 0.50, 0.80)),
    }

    def msbf_px_element_fx(element):
        return MSBF_PX_ELEMENT_FX.get(element, MSBF_PX_ELEMENT_FX["slash"])


# -----------------------------------------------------------------------------
# 2. THE STAGE
# -----------------------------------------------------------------------------
init -4 python:
    import math as _pxm

    def _px_ease_out(t):
        t = min(1.0, max(0.0, t))
        return 1.0 - (1.0 - t) * (1.0 - t)

    def _px_ease_in(t):
        t = min(1.0, max(0.0, t))
        return t * t

    def _px_ease_io(t):
        t = min(1.0, max(0.0, t))
        return t * t * (3.0 - 2.0 * t)

    def _px_lerp(a, b, t):
        return a + (b - a) * t

    class _PXPose(python_object):
        """One frame's worth of numbers for one sprite. Defaults = at rest."""
        __slots__ = ("dx", "dy", "breath", "lean", "sx", "sy", "flow", "wing",
                        "writhe", "flash", "tint", "grey", "outline", "rim",
                        "block", "poster", "tear", "dissolve", "alpha", "rot",
                        "shadow", "pose", "anim", "anim_t0")

        def __init__(self):
            self.dx = 0.0
            self.dy = 0.0
            self.breath = 0.0
            self.lean = 0.0
            self.sx = 1.0
            self.sy = 1.0
            self.flow = (0.0, 0.2, 2.0, 0.0)
            self.wing = (0.0, 30.0, 40.0, 0.0)
            self.writhe = 0.0
            self.flash = 0.0
            self.tint = (1.0, 1.0, 1.0, 0.0)
            self.grey = 0.0
            self.outline = (1.0, 1.0, 1.0, 0.0)
            self.rim = (1.0, 1.0, 1.0, 0.0)
            self.block = 1.0
            self.poster = 0.0
            self.tear = 0.0
            self.dissolve = 0.0
            self.alpha = 1.0
            self.rot = 0
            self.shadow = 1.0
            self.pose = None
            self.anim = "idle"
            self.anim_t0 = 0.0

    class _PXFx(python_object):
        __slots__ = ("kind", "x", "y", "w", "h", "c1", "c2", "c3", "t0", "dur",
                        "cell", "angle", "seed", "solid", "delay")

        def __init__(self, kind, x, y, w, h, cols, t0, dur, cell=3, angle=0.0, seed=0.0, solid=0.62, delay=0.0):
            self.kind = kind
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            self.c1, self.c2, self.c3 = cols
            self.t0 = t0
            self.dur = dur
            self.cell = cell
            self.angle = angle
            self.seed = seed
            self.solid = solid
            self.delay = delay

    class _PXActorState(python_object):
        """Presentation-only memory for one party member."""
        __slots__ = ("anim_state", "anim_since",
                        "act", "act_t0", "act_style", "act_target", "hurt_t0",
                        "hurt_w", "hurt_crit", "was_alive", "down_t0", "rise_t0",
                        "seen_hit", "evade_t0", "support_t0")

        def __init__(self):
            self.anim_state = "idle"
            self.anim_since = 0.0
            self.act = None
            self.act_t0 = -99.0
            self.act_style = None
            self.act_target = None
            self.hurt_t0 = -99.0
            self.hurt_w = 1.0
            self.hurt_crit = False
            self.was_alive = True
            self.down_t0 = -99.0
            self.rise_t0 = -99.0
            self.seen_hit = -1
            self.evade_t0 = -99.0
            self.support_t0 = -99.0

    MSBF_PX_ENEMY_EVENTS = ("enemy", "enemy_hit", "enemy_aoe", "enemy_weak", "enemy_crit", "enemy_resist")
    MSBF_PX_ENEMY_SELF = ("enemy_buff", "enemy_guard", "enemy_heal")
    MSBF_PX_PLAYER_HITS = ("hit", "weak", "crit", "resist")

    # --- WARM THE FIGHT'S BIG ART, OFF THE MAIN THREAD -------------------------
    # Measured Oct 2 2026: without this the fight decoded its large art the
    # first time each piece was needed, ON the frame it was needed -- a 26-30
    # ms PNG/WebP decode inside a 55-70 ms frame: each archetype the first time
    # its owner's command window opened, arena_gold / arena_rupture on the very
    # frame a bar breaks, idphase.png in the middle of the Id reveal.
    #
    # The fix decodes everything the fight can show on a daemon thread, the way
    # Ren'Py's own preload thread does (cache.get(predict=True, texture=True):
    # the decode happens here, the GPU upload is queued for the main thread to
    # finish a texture at a time). It starts the first time a stage is built:
    # the FORMATION preview, then again at the battle intro as a backstop --
    # seconds of runway either way, and a cached image costs nothing.
    # (renpy.cache_pin is a no-op on 8.6, and image-predictor preloads queued
    # from a label are cleared by the next interaction's cache tick.)
    MSBF_PX_WARM_ART = ("seal.png", "orbit_current.png", "title_plate.png", "title_rule.png", "sigil.png",
        "wind_current.png", "debris_cyan.png", "debris_rupture.png", "mote.png",
        "turn_full.png", "turn_half.png", "turn_gain.png", "turn_spent.png")
    MSBF_PX_WARMING = {"busy": False}

    def msbf_px_warm_images():
        """Every large image a Seer fight can draw, as cache-able images."""
        paths = list(MSBF_SEER_PLATES.values()) + list(MSBF_PX_ILLUSTRATION.values())
        paths += [MSBF_SEER_ART + f for f in MSBF_PX_WARM_ART]
        for kind in ("party", "boss"):
            for meta in MSBF_PX_META.get(kind, {}).values():
                for m in [meta] + list((meta.get("poses") or {}).values()):
                    if m.get("file"):
                        paths.append(MSBF_PX_DIR + m["file"])
                    if (m.get("hq") or {}).get("file"):
                        paths.append(MSBF_PX_DIR + m["hq"]["file"])
        rv = []
        for p in paths:
            try:
                d = renpy.easy.displayable(p)
            except Exception:
                continue
            if isinstance(d, renpy.display.im.ImageBase):
                rv.append(d)
        for name in MSBF_SIL_SPRITE.values():
            d = renpy.get_registered_image(name)
            if isinstance(d, renpy.display.im.ImageBase):
                rv.append(d)
        return rv

    def _msbf_px_warm_worker(images):
        try:
            for im in images:
                try:
                    renpy.display.im.cache.get(im, predict=True, texture=True)
                except Exception:
                    pass
        finally:
            MSBF_PX_WARMING["busy"] = False

    def msbf_px_warm_fight_art():
        """Start decoding the fight's art in the background (idempotent)."""
        if MSBF_PX_WARMING["busy"]:
            return
        try:
            images = msbf_px_warm_images()
        except Exception:
            return
        import threading as _msbf_threading
        MSBF_PX_WARMING["busy"] = True
        _msbf_threading.Thread(target=_msbf_px_warm_worker, args=(images,), daemon=True).start()

    class MSBFPixelStage(renpy.Displayable):
        """Boss + party, as pixel sprites, reading (never writing) a battle.

        mode:
            "battle"  -- the live fight.
            "intro"   -- phase-1 entrance choreography (party runs in, she drops).
            "id_intro"-- Id Mode's entrance (she is simply, suddenly there).
            "reveal"  -- a phase reveal (the arriving form, driven by the stage's
                        own clock from the moment the reveal starts).
        """

        def __init__(self, battle=None, mode="battle", phase=1, party_ids=None, rows=None, **kwargs):
            super(MSBFPixelStage, self).__init__(**kwargs)
            # A stage is the first sign a fight is coming: start decoding its
            # art now, off the main thread (see msbf_px_warm_fight_art).
            msbf_px_warm_fight_art()
            self.battle = battle
            self.mode = mode
            self.fixed_phase = phase
            self.party_ids = list(party_ids or [])
            self.rows = dict(rows or {})
            self.actors = {}
            self.fx = []
            self.last_st = None
            self.seen_fx_serial = None
            self.seen_float_serial = None
            self.seen_commit = MSBF_PX_BUS["commit"][0] if MSBF_PX_BUS.get("commit") else 0
            self.boss_act = None
            self.boss_t0 = -99.0
            self.boss_w = 1.0
            self.boss_phase_seen = None
            self.boss_reveal_t0 = -99.0
            self.windup_t0 = -99.0
            self.last_fx_event = None
            self.event_t0 = -99.0
            self._rows = None
            self.break_phase = None
            self.break_t0 = -99.0

        # ---- helpers ------------------------------------------------------
        def _actor(self, mid):
            a = self.actors.get(mid)
            if a is None:
                a = _PXActorState()
                self.actors[mid] = a
            return a

        def _phase(self):
            if self.battle is not None:
                try:
                    return min(3, max(1, int(self.battle.phase)))
                except Exception:
                    return 1
            return self.fixed_phase

        def _party(self):
            """[(member_id, row, alive, hp_ratio, guard, member_or_None)]."""
            out = []
            if self.battle is not None:
                for m in self.battle.party:
                    out.append((m.id, getattr(m, "row", "front"), m.alive, m.hp_ratio, getattr(m, "guard", False), m))
            else:
                for mid in self.party_ids:
                    out.append((mid, self.rows.get(mid, "front"), True, 1.0, False, None))
            return out

        def spawn(self, kind, x, y, w, h, cols, t, dur, cell=3, angle=0.0, solid=0.62, delay=0.0):
            if len(self.fx) > 28:
                self.fx.pop(0)
            seed = (len(self.fx) * 7.31 + t * 13.7) % 97.0
            self.fx.append(_PXFx(kind, x, y, w, h, cols, t, dur, cell, angle, seed, solid, delay))

        # ---- event intake -------------------------------------------------
        def _poll(self, t):
            b = self.battle
            if b is None:
                return
            phase = self._phase()
            if self.boss_phase_seen is None:
                self.boss_phase_seen = phase
            elif phase != self.boss_phase_seen:
                # The bar broke. The battle has already become the next form,
                # so remember the one that is breaking and shatter IT.
                self.break_phase = self.boss_phase_seen
                self.break_t0 = t
                self.boss_phase_seen = phase
                self.boss_reveal_t0 = t
                self.fx = []
                # A bar break is a SCENE CHANGE: nothing in flight crosses it.
                # A killing blow raises "phase_blackout" instead of "hit", so
                # the striker never got the follow-through that walks them
                # home -- they stood frozen mid-dash at her feet for the whole
                # of the next phase. Everyone goes back to their mark here.
                for _a in self.actors.values():
                    _a.act = None
                    _a.hurt_t0 = -99.0
                    _a.evade_t0 = -99.0
                    _a.support_t0 = -99.0
                self.boss_act = None
                self.windup_t0 = -99.0
                ccx, ccy = msbf_px_boss_point(self.break_phase, "core")
                col = msbf_hex_rgb(msbf_phase_accent(self.break_phase)[0])
                self.spawn(6, ccx, ccy, 760, 760, ((1.0, 1.0, 1.0), col, tuple(c * 0.45 for c in col)), t, 0.75, 3, solid=0.85)

            party = list(b.party)
            n = len(party)

            # The player committed a move: start that member's wind-up.
            cue = MSBF_PX_BUS.get("commit")
            if cue and cue[0] != self.seen_commit:
                self.seen_commit = cue[0]
                _ser, ai, skill_id, ti = cue
                if ai is not None and 0 <= ai < n:
                    m = party[ai]
                    skill = MSBF_SKILLS.get(skill_id)
                    st = msbf_px_move_style(m.id, skill)
                    a = self._actor(m.id)
                    a.act = "commit"
                    a.act_t0 = t
                    a.act_style = st
                    a.act_target = ti
                    if st in ("cast", "support"):
                        fx, fy = msbf_px_member_point(m.id, ai, n, getattr(m, "row", "front"), "foot", True, self._rows)
                        el = getattr(skill, "element", "support")
                        _k, c1, c2, c3 = msbf_px_element_fx(el)
                        self.spawn(8, fx, fy - 4, 150, 46, (c1, c2, c3), t, 1.0, 2, solid=0.75)

            # A new combat cue.
            if b.fx_serial != self.seen_fx_serial:
                first = self.seen_fx_serial is None
                self.seen_fx_serial = b.fx_serial
                ev = b.fx_event
                if not first and ev:
                    self._on_event(ev, t, party, n)
            self.last_fx_event = b.fx_event

            # Who was just struck: the float feed's party anchors.
            if b.float_serial != self.seen_float_serial:
                first = self.seen_float_serial is None
                self.seen_float_serial = b.float_serial
                if not first:
                    self._on_floats(t, party, n)

            # KO / revive transitions.
            for i, m in enumerate(party):
                a = self._actor(m.id)
                if a.was_alive and not m.alive:
                    a.down_t0 = t
                elif (not a.was_alive) and m.alive:
                    a.rise_t0 = t
                    fx, fy = msbf_px_member_point(m.id, i, n, getattr(m, "row", "front"), "foot", False, self._rows)
                    self.spawn(4, fx, fy - 100, 90, 220, ((1.0, 1.0, 0.9), (0.5, 1.0, 0.65), (0.2, 0.6, 0.45)), t, 0.9, 2, solid=0.7)
                a.was_alive = m.alive

            # Enemy wind-up: she coils in the beat before each of her actions.
            if b.enemy_phase_active and not b.fx_event and not b.handover_active:
                if self.windup_t0 < 0 or self.boss_act not in (None, "windup"):
                    if t - self.boss_t0 > 0.6:
                        self.windup_t0 = t
                        self.boss_act = "windup"
                        self.boss_t0 = t
            elif self.boss_act == "windup":
                self.boss_act = None
                self.windup_t0 = -99.0

        def _on_event(self, ev, t, party, n):
            b = self.battle
            phase = self._phase()
            cx, cy = msbf_px_boss_point(phase, "core")
            w = msbf_impact_weight(ev)
            if ev in MSBF_PX_PLAYER_HITS or ev in ("miss",) and not b.enemy_phase_active:
                ai = getattr(b, "last_actor_index", None)
                el = getattr(b, "last_cast_element", None) or "slash"
                if ev != "miss":
                    self.boss_act = "hurt"
                    self.boss_t0 = t
                    self.boss_w = max(0.5, w)
                kind, c1, c2, c3 = msbf_px_element_fx(el)
                jitter = ((b.fx_serial * 37) % 60) - 30
                if ev != "miss":
                    big = 1.0 + 0.35 * (ev in ("weak", "crit"))
                    self.spawn(kind, cx + jitter, cy + 10, int(300 * big), int(300 * big), (c1, c2, c3), t, 0.55, 3,
                                angle=(-0.5 if (b.fx_serial % 2) else 0.45))
                    self.spawn(0, cx + jitter, cy + 10, int(220 * big), int(220 * big), (c1, c2, c3), t, 0.36, 3, solid=0.75)
                    if ev in ("weak", "crit"):
                        self.spawn(1, cx, cy, 520, 520, (c1, c2, c3), t + 0.04, 0.5, 3)
            elif ev in ("scan", "debuff"):
                self.boss_act = "hurt"
                self.boss_t0 = t
                self.boss_w = 0.35
                self.spawn(1, cx, cy, 420, 420, ((1.0, 1.0, 1.0), (0.6, 0.85, 1.0), (0.3, 0.45, 0.8)), t, 0.6, 3)
            elif ev in MSBF_PX_ENEMY_EVENTS or (ev == "miss" and b.enemy_phase_active):
                self.boss_act = "strike"
                self.boss_t0 = t
                self.boss_w = max(0.6, w)
            elif ev in MSBF_PX_ENEMY_SELF or ev == "shuffle":
                self.boss_act = "power"
                self.boss_t0 = t
                self.boss_w = 1.0
                col = msbf_hex_rgb(msbf_phase_accent(phase)[0])
                self.spawn(1, cx, cy, 640, 640, ((1.0, 1.0, 1.0), col, tuple(c * 0.5 for c in col)), t, 0.7, 3)
                if ev == "enemy_heal":
                    self.spawn(3, cx, cy, 420, 520, msbf_px_element_fx("healing")[1:], t, 0.9, 3)
            elif ev in ("heal", "revive", "buff", "guard", "pass", "focus", "haste"):
                pass
            elif ev == "phase":
                self.boss_reveal_t0 = t
            elif ev == "final_victory":
                self.boss_act = "collapse"
                self.boss_t0 = t
            elif ev == "final_defeat":
                self.boss_act = "loom"
                self.boss_t0 = t

            # The acting member's own follow-through after the resolve.
            if ev not in ("phase", "phase_blackout", "final_victory", "final_defeat") and not b.enemy_phase_active:
                ai = getattr(b, "last_actor_index", None)
                if ai is not None and 0 <= ai < n:
                    a = self._actor(party[ai].id)
                    if a.act == "commit":
                        a.act = "follow"
                        a.act_t0 = t

        def _enemy_magic(self):
            el = self._enemy_element()
            return el in ("fire", "ice", "lightning", "wind", "psychic", "almighty")

        def _enemy_element(self):
            b = self.battle
            bn = getattr(b, "action_banner", None) if b is not None else None
            if bn and bn[4] == "enemy":
                return bn[3]
            return None

        def _on_floats(self, t, party, n):
            b = self.battle
            enemy = b.enemy_phase_active or (b.fx_event in MSBF_PX_ENEMY_EVENTS)
            phase = self._phase()
            for fe in (b.float_events or []):
                anc = fe.get("anchor", "boss")
                kind = fe.get("kind", "dmg")
                if not isinstance(anc, int) or anc >= n:
                    continue
                m = party[anc]
                a = self._actor(m.id)
                px_, py_ = msbf_px_member_point(m.id, anc, n, getattr(m, "row", "front"), "chest", False, self._rows)
                if kind in ("enemy", "dmg", "crit", "weak") and enemy:
                    a.hurt_t0 = t
                    a.hurt_w = max(0.6, msbf_impact_weight(b.fx_event))
                    a.hurt_crit = b.fx_event in ("enemy_weak", "enemy_crit")
                    if self._enemy_magic():
                        ek, c1, c2, c3 = msbf_px_element_fx(self._enemy_element())
                        self.spawn(ek, px_, py_ - (60 if ek in (4, 5, 7) else 0), 200, 260 if ek in (4, 5, 7) else 200, (c1, c2, c3), t, 0.55, 2)
                    elif phase == 1:
                        col = ((1.0, 1.0, 1.0), (0.45, 0.95, 1.0), (0.15, 0.45, 0.80))
                        self.spawn(2, px_, py_, 220, 220, col, t, 0.40, 2, angle=-0.6)
                    elif phase == 2:
                        col = ((1.0, 1.0, 0.92), (1.0, 0.82, 0.40), (0.75, 0.45, 0.20))
                        self.spawn(4, px_, py_ - 80, 110, 300, col, t, 0.55, 2)
                    else:
                        col = ((1.0, 0.92, 0.95), (1.0, 0.25, 0.40), (0.45, 0.05, 0.18))
                        self.spawn(6, px_, py_, 200, 200, col, t, 0.45, 2)
                    self.spawn(0, px_, py_, 130, 130, ((1.0, 1.0, 1.0), (1.0, 0.45, 0.55), (0.6, 0.12, 0.25)), t, 0.28, 2, solid=0.8)
                elif kind == "miss":
                    a.evade_t0 = t
                elif kind == "heal":
                    a.support_t0 = t
                    self.spawn(3, px_, py_ - 30, 120, 220, msbf_px_element_fx("healing")[1:], t, 0.85, 2)

        # ---- poses --------------------------------------------------------
        def _party_pose(self, mid, i, n, row, alive, hp, guard, active, t, member_style):
            a = self._actor(mid)
            pz = _PXPose()
            seed = (hash(mid) % 100) * 0.0731
            # Idle: breath on a per-person clock so the line never pulses
            # in unison.
            pz.breath = 0.9 + 0.9 * _pxm.sin(t * 2.6 + seed * 10.0)
            pz.flow = (0.9, 0.16, 2.4, seed * 6.0)
            pz.rim = (0.62, 0.86, 1.0, 0.0)

            if not alive and t - a.down_t0 > 0.42:
                pz.rot = MSBF_PX_PARTY_FACE
                pz.grey = 0.75
                pz.breath = 0.0
                pz.flow = (0.0, 0.2, 2.0, 0.0)
                pz.shadow = 0.6
                return self._face(pz, MSBF_PX_PARTY_FACE)
            if not alive:
                k = (t - a.down_t0) / 0.42
                pz.sy = 1.0 - 0.35 * _px_ease_in(k)
                pz.lean = -10.0 * k
                pz.grey = 0.75 * k
                pz.flash = 0.6 * (1.0 - k)
                return self._face(pz, MSBF_PX_PARTY_FACE)

            if hp < 0.25 and not guard:
                # FF's "weak" kneel: crouched, leaning in, panting.
                pz.sy = 0.90
                pz.lean = -5.0
                pz.breath = 1.6 + 1.4 * _pxm.sin(t * 5.4 + seed)
            if guard:
                pz.sy = 0.93
                pz.sx = 1.03
                pz.lean = 3.0
                pz.tint = (0.55, 0.80, 1.0, 0.12 + 0.06 * _pxm.sin(t * 4.0))

            if active:
                k = _px_ease_out((t - (getattr(self, "_active_t0", {}).get(mid, t))) / 0.18)
                pz.dx = -MSBF_PX_ACTIVE_STEP * k
                pz.outline = (1.0, 1.0, 1.0, 0.55 + 0.35 * (0.5 + 0.5 * _pxm.sin(t * 6.0)))
                pz.rim = (0.70, 0.92, 1.0, 0.55 * MSBF_PX_PARTY_FACE)

            # Rise from KO.
            if t - a.rise_t0 < 0.5:
                k = (t - a.rise_t0) / 0.5
                pz.flash = max(pz.flash, 0.8 * (1.0 - k))
                pz.sy *= 0.75 + 0.25 * _px_ease_out(k)

            # Being struck: snap away from her, flash, settle.
            dt = t - a.hurt_t0
            if dt < 0.42:
                w = a.hurt_w
                if dt < 0.07:
                    k = dt / 0.07
                    pz.dx += 7.0 * w * k
                    pz.flash = max(pz.flash, 1.0 if int(dt * 30) % 2 == 0 else 0.0)
                else:
                    k = (dt - 0.07) / 0.35
                    pz.dx += 7.0 * w * (1.0 - _px_ease_io(k))
                    pz.flash = max(pz.flash, 0.5 * (1.0 - k) if int(dt * 30) % 2 == 0 else 0.0)
                pz.lean += 5.0 * w * (1.0 - min(1.0, dt / 0.3))
                if a.hurt_crit:
                    pz.tint = (1.0, 0.85, 0.40, 0.5 * (1.0 - min(1.0, dt / 0.42)))
            # Evaded: a quick hop back.
            dt = t - a.evade_t0
            if dt < 0.36:
                k = dt / 0.36
                pz.dx += 10.0 * _pxm.sin(k * _pxm.pi)
                pz.dy -= 6.0 * _pxm.sin(k * _pxm.pi)
            # Healed / buffed: a lift.
            dt = t - a.support_t0
            if dt < 0.6:
                k = dt / 0.6
                pz.tint = (0.55, 1.0, 0.65, 0.35 * (1.0 - k))
                pz.dy -= 2.0 * _pxm.sin(k * _pxm.pi)

            # The move itself. A committed move whose resolve never produced a
            # follow-through (a killing blow, the rupture threshold, the
            # finale) is walked home rather than left hanging at full reach.
            if a.act == "commit" and t - a.act_t0 > MSBF_PX_COMMIT_TIMEOUT:
                a.act = "follow"
                a.act_t0 = t
            if a.act in ("commit", "follow"):
                self._move_pose(pz, a, mid, i, n, row, t)
            return self._face(pz, MSBF_PX_PARTY_FACE)

        def _face(self, pz, face):
            # Forward units -> screen: forward is negative in the pose code.
            pz.dx *= -face
            pz.lean *= -face
            return pz

        def _move_pose(self, pz, a, mid, i, n, row, t):
            st = a.act_style or "cast"
            dt = t - a.act_t0
            fx, fy = msbf_px_slot(i, n, row, self._rows)
            # Where a melee lands: just in front of her, at the member's own
            # height band, in ART px relative to their slot (2x scale).
            bx, by = msbf_px_boss_point(self._phase(), "core")
            # A melee lands right in front of her: ~200px short of her core.
            reach = -max(0.0, (abs(bx - fx) - 200.0) / 2.0)
            if a.act == "commit":
                if st == "dash":
                    k = dt / 0.36
                    if k < 0.22:
                        pz.sy *= 1.0 - 0.08 * (k / 0.22)
                        pz.lean += 4.0 * (k / 0.22)
                    else:
                        kk = _px_ease_in((k - 0.22) / 0.78)
                        pz.dx = _px_lerp(pz.dx, reach, kk)
                        pz.dy -= 10.0 * _pxm.sin(min(1.0, kk) * _pxm.pi)
                        pz.lean -= 9.0 * kk
                        pz.sx *= 1.0 + 0.06 * kk
                elif st == "heavy":
                    k = dt / 0.44
                    if k < 0.35:
                        pz.sy *= 1.0 - 0.12 * (k / 0.35)
                        pz.lean += 7.0 * (k / 0.35)
                    else:
                        kk = _px_ease_in((k - 0.35) / 0.65)
                        pz.dx = _px_lerp(pz.dx, reach * 0.94, kk)
                        pz.dy -= 26.0 * _pxm.sin(min(1.0, kk) * _pxm.pi * 0.9)
                        pz.lean -= 12.0 * kk
                elif st == "jump":
                    # A Dragoon's jump: up out of frame, then down onto her.
                    k = dt / 0.46
                    if k < 0.18:
                        pz.sy *= 1.0 - 0.14 * (k / 0.18)
                    elif k < 0.55:
                        kk = _px_ease_in((k - 0.18) / 0.37)
                        pz.dy -= 260.0 * kk
                        pz.sy *= 1.0 + 0.12 * kk
                        pz.dx = _px_lerp(pz.dx, reach * 0.45, kk)
                    else:
                        kk = _px_ease_in((k - 0.55) / 0.45)
                        pz.dx = _px_lerp(reach * 0.45, reach, kk)
                        pz.dy -= 260.0 * (1.0 - kk)
                        pz.lean -= 6.0
                        pz.shadow = 0.25 + 0.75 * kk
                elif st == "throw":
                    k = dt / 0.30
                    pz.lean += 5.0 * _pxm.sin(min(1.0, k) * _pxm.pi)
                    pz.dx += -4.0 * _px_ease_out(k)
                elif st == "guard":
                    pz.sy *= 0.94
                    pz.lean += 3.0
                else:
                    # cast / support: rise on the toes, light gathering.
                    k = min(1.0, dt / 0.40)
                    pz.sy *= 1.0 + 0.05 * _px_ease_out(k)
                    pz.dy -= 3.0 * _px_ease_out(k)
                    pz.flash = max(pz.flash, 0.25 * k if int(t * 20) % 2 == 0 else 0.0)
            else:
                # Follow-through, then home.
                if st in ("dash", "heavy"):
                    lp = reach * (1.0 if st == "dash" else 0.94)
                    if dt < 0.22:
                        pz.dx = lp
                        pz.lean -= 12.0 * (1.0 - dt / 0.22)
                        pz.sy *= 0.94 + 0.06 * (dt / 0.22)
                    elif dt < 0.62:
                        kk = _px_ease_io((dt - 0.22) / 0.40)
                        pz.dx = _px_lerp(lp, pz.dx, kk)
                        pz.dy -= 12.0 * _pxm.sin(kk * _pxm.pi)
                    else:
                        a.act = None
                elif st == "jump":
                    lp = reach
                    if dt < 0.16:
                        pz.dx = lp
                        pz.sy *= 0.86 + 0.14 * (dt / 0.16)
                    elif dt < 0.66:
                        kk = _px_ease_io((dt - 0.16) / 0.50)
                        pz.dx = _px_lerp(lp, pz.dx, kk)
                        pz.dy -= 40.0 * _pxm.sin(kk * _pxm.pi)
                    else:
                        a.act = None
                elif st in ("cast", "support"):
                    if dt < 0.30:
                        pz.flash = max(pz.flash, 0.7 * (1.0 - dt / 0.30))
                        pz.sy *= 1.05 - 0.05 * (dt / 0.30)
                    else:
                        a.act = None
                else:
                    if dt > 0.3:
                        a.act = None

        def _boss_pose(self, phase, t):
            pz = _PXPose()
            b = self.battle
            # ---- the idles: one per form ----
            if phase == 1:
                # Nahobino: a fighter's weight, hair and cape in the wind.
                pz.breath = 1.2 + 1.2 * _pxm.sin(t * 1.9)
                pz.dy = -3.0 * _pxm.sin(t * 1.15)
                pz.lean = 1.5 * _pxm.sin(t * 0.83)
                pz.flow = (2.2, 0.085, 3.1, 0.0)
                pz.rim = (0.45, 0.90, 1.0, 0.30 * MSBF_PX_BOSS_FACE)
            elif phase == 2:
                # Tohu Imago: the wings beat in a long slow stroke with a
                # shallow second pulse inside it; the body barely moves.
                stroke = _pxm.sin(t * 1.25)
                pulse = 0.35 * _pxm.sin(t * 3.75 + 0.6)
                pz.wing = (7.5 * stroke + 2.0 * pulse, 26.0, 70.0, 6.0)
                pz.dy = -5.0 * _pxm.sin(t * 1.25 + 1.2)
                pz.breath = 0.8 + 0.8 * _pxm.sin(t * 1.25 + 0.3)
                pz.flow = (1.2, 0.06, 1.6, 0.0)
                pz.rim = (1.0, 0.90, 0.62, 0.26 * MSBF_PX_BOSS_FACE)
            else:
                # Imago Rupta: everything away from her core is writhing, and
                # the image keeps losing its genre for a frame or two.
                pz.writhe = 5.5 + 2.5 * _pxm.sin(t * 0.9)
                pz.flow = (1.6, 0.11, 4.2, 0.0)
                pz.breath = 1.0 + 1.0 * _pxm.sin(t * 2.7)
                pz.dy = -3.0 * _pxm.sin(t * 1.7)
                pz.rim = (1.0, 0.30, 0.42, 0.32 * MSBF_PX_BOSS_FACE)
                tick = int(t * 6.0)
                h = ((tick * 2654435761) % 1000) / 1000.0
                if h > 0.86:
                    pz.block = 2.0 if h < 0.93 else 4.0
                    pz.poster = 4.0 if h > 0.95 else 0.0
                if h > 0.80:
                    pz.tear = 1.0 + (h - 0.8) * 10.0
                # Rarely, the pixel art fails altogether and for a frame or
                # two she is back in the genre she came from: the illustrated
                # idphase.png, the art on her gacha card.
                if h > 0.975:
                    pz.pose = "illustration"

            # ---- reactions ----
            dt = t - self.boss_t0
            act = self.boss_act
            w = self.boss_w
            away = -1.0   # her "back" is screen-left
            if act == "hurt" and dt < 0.48:
                if dt < 0.06:
                    pz.flash = 1.0
                    pz.dx += away * 4.0 * w
                elif dt < 0.12:
                    pz.flash = 0.0
                    pz.dx += away * 6.0 * w
                else:
                    k = (dt - 0.12) / 0.36
                    pz.dx += away * 6.0 * w * (1.0 - _px_ease_io(k))
                    pz.flash = 0.45 if (int(dt * 30) % 2 == 0 and k < 0.4) else 0.0
                pz.dx += (2.0 * w if int(dt * 40) % 2 == 0 else -2.0 * w) * max(0.0, 1.0 - dt / 0.3)
                pz.lean += -3.0 * w * max(0.0, 1.0 - dt / 0.3)
            elif act == "windup":
                k = min(1.0, dt / 0.45)
                if phase == 1:
                    pz.sy *= 1.0 - 0.05 * _px_ease_out(k)
                    pz.lean += 5.0 * _px_ease_out(k)
                    pz.dx += away * 5.0 * _px_ease_out(k)
                elif phase == 2:
                    pz.wing = (pz.wing[0] - 10.0 * _px_ease_out(k), pz.wing[1], pz.wing[2], pz.wing[3])
                    pz.dy -= 6.0 * _px_ease_out(k)
                else:
                    pz.writhe += 4.0 * k
                    pz.tear = max(pz.tear, 0.6 * k)
                pz.tint = (1.0, 0.30, 0.40, 0.18 * k if int(t * 16) % 2 == 0 else 0.0)
            elif act == "strike" and dt < 0.7 and phase == 1 and self._enemy_magic():
                k = min(1.0, dt / 0.7)
                pz.dy -= 6.0 * _pxm.sin(min(1.0, dt / 0.25) * _pxm.pi * 0.5) * (1.0 - k)
                pz.flash = 0.55 * max(0.0, 1.0 - dt / 0.18)
                pz.sy *= 1.0 + 0.04 * (1.0 - k)
            elif act == "strike" and dt < 0.7:
                if phase == 1:
                    # The glaive sweep: she lunges at the party and back.
                    if dt < 0.10:
                        pz.dx += 26.0 * _px_ease_out(dt / 0.10)
                        pz.lean -= 8.0 * (dt / 0.10)
                    else:
                        k = (dt - 0.10) / 0.60
                        pz.dx += 26.0 * (1.0 - _px_ease_io(k))
                        pz.lean -= 8.0 * (1.0 - k)
                    pz.sx *= 1.0 + 0.04 * max(0.0, 1.0 - dt / 0.3)
                elif phase == 2:
                    k = min(1.0, dt / 0.7)
                    flare = _pxm.sin(min(1.0, dt / 0.18) * _pxm.pi * 0.5) * (1.0 - _px_ease_io(max(0.0, (dt - 0.18) / 0.52)))
                    pz.wing = (pz.wing[0] + 16.0 * flare, pz.wing[1], pz.wing[2], pz.wing[3])
                    pz.flash = 0.35 * flare
                    pz.dy -= 8.0 * flare
                else:
                    k = min(1.0, dt / 0.7)
                    pz.writhe += 10.0 * (1.0 - k)
                    pz.dx += 18.0 * _pxm.sin(min(1.0, dt / 0.25) * _pxm.pi)
                    pz.tear = max(pz.tear, 2.0 * (1.0 - k))
                    pz.block = 2.0 if dt < 0.12 else pz.block
            elif act == "power" and dt < 0.8:
                k = dt / 0.8
                pz.dy -= 8.0 * _pxm.sin(k * _pxm.pi)
                col = msbf_hex_rgb(msbf_phase_accent(phase)[0])
                pz.tint = (col[0], col[1], col[2], 0.35 * _pxm.sin(k * _pxm.pi))
                if phase == 2:
                    pz.wing = (pz.wing[0] + 9.0 * _pxm.sin(k * _pxm.pi), pz.wing[1], pz.wing[2], pz.wing[3])
            elif act == "collapse":
                # Matched to the hypernova: tremor building, implosion by ~0.8s,
                # gone at the detonation (0.84s).
                k = min(1.0, dt / 0.84)
                amp = 1.0 + 7.0 * k
                pz.dx += amp if int(dt * 50) % 2 == 0 else -amp
                pz.sx *= 1.0 - 0.45 * _px_ease_in(k)
                pz.sy *= 1.0 + 0.10 * k - 0.6 * _px_ease_in(max(0.0, (k - 0.7) / 0.3))
                pz.flash = min(1.0, k * 1.2)
                pz.dissolve = max(0.0, (k - 0.55) / 0.45)
                if dt > 0.86:
                    pz.alpha = 0.0
            elif act == "loom":
                k = min(1.0, dt / 1.6)
                pz.dx += 10.0 * _px_ease_io(k)
                pz.sx *= 1.0 + 0.10 * _px_ease_io(k)
                pz.sy *= 1.0 + 0.10 * _px_ease_io(k)
                pz.tint = (0.85, 0.12, 0.22, 0.35 * k)

            # ---- a phase reveal: the new form arrives ----
            rt = t - self.boss_reveal_t0
            if b is not None and getattr(b, "phase_transition_active", False) and b.fx_event == "phase":
                if phase == 2:
                    # Descent: from above the frame, slowly, wings closed then
                    # opening as she comes down into the light.
                    k = min(1.0, max(0.0, (rt - 0.55) / 2.6))
                    pz.dy -= 150.0 * (1.0 - _px_ease_out(k))
                    pz.alpha = min(1.0, max(0.0, (rt - 0.55) / 0.5))
                    pz.wing = (pz.wing[0] - 24.0 * (1.0 - _px_ease_io(k)), pz.wing[1], pz.wing[2], pz.wing[3])
                    pz.flash = 0.6 * (1.0 - k)
                else:
                    # Rupture: present in fragments, the genre failing first.
                    on = (rt > 0.45)
                    pz.alpha = 1.0 if on and int(rt * 14) % 3 != 0 or rt > 1.4 else 0.0
                    if rt < 1.6:
                        pz.block = 6.0 if rt < 0.8 else (3.0 if rt < 1.2 else 2.0)
                        pz.poster = 3.0 if rt < 1.0 else 0.0
                        pz.tear = 3.0
                        pz.writhe += 10.0
            # Written with forward = +x; her forward is toward the party.
            pz.dx *= -MSBF_PX_BOSS_FACE
            pz.lean *= -MSBF_PX_BOSS_FACE
            return pz

        # ---- drawing ------------------------------------------------------
        def _draw_sprite(self, rv, img, meta, ox, oy, pz, t, st, at, hq=None):
            """Draw one figure. `hq` is the sprite's illustrated twin
            (meta["hq"]) when Battle Art is Illustrated: same canvas, same
            anchors, `unit` texels per art pixel -- so the pose maths below is
            identical and only the texture, the filtering and the snap change.
            """
            sc = meta["scale"]
            if pz.alpha <= 0.0:
                return
            fx, fy = meta["foot"]
            hx, hy = meta["head"]
            if hq:
                tex = MSBF_PX_DIR + hq["file"]
                unit = float(hq.get("unit", 1.0))
                crisp = False
                snap = 1
            else:
                tex = img
                unit = 1.0
                crisp = True
                snap = sc
            tr = Transform(msbf_px_disp(tex), mesh=True, nearest=crisp, shader="msbf.px",
                u_px_foot=(float(fx) + 0.5, float(fy) + 0.5),
                u_px_head=(float(hx) + 0.5, float(hy) + 0.5),
                u_px_breath=float(pz.breath),
                u_px_lean=float(pz.lean),
                u_px_scale=(float(pz.sx), float(pz.sy)),
                u_px_flow=tuple(float(v) for v in pz.flow),
                u_px_wing=tuple(float(v) for v in pz.wing),
                u_px_writhe=float(pz.writhe),
                u_px_flash=float(min(1.0, max(0.0, pz.flash))),
                u_px_tint=tuple(float(v) for v in pz.tint),
                u_px_grey=float(pz.grey),
                u_px_outline=tuple(float(v) for v in pz.outline),
                u_px_rim=tuple(float(v) for v in pz.rim),
                u_px_block=float(pz.block),
                u_px_poster=float(pz.poster),
                u_px_tear=float(pz.tear),
                u_px_dissolve=float(pz.dissolve),
                u_px_seed=float((ox * 0.013 + oy * 0.007) % 9.0),
                u_px_unit=unit,
                u_px_hq=(1.0 if hq else 0.0),
                alpha=float(min(1.0, max(0.0, pz.alpha))))
            if pz.rot:
                # KO: flat on their back where they stood, head away from her.
                # A quarter turn of a pixel sprite is pixel-exact, so this is
                # the one rotation the stage ever does.
                face = pz.rot
                outer = Transform(tr, zoom=sc / unit, nearest=crisp, rotate=-90 * face, rotate_pad=False)
                r = renpy.render(outer, 4000, 4000, st, at)
                w, h = meta["size"]
                bx0, by0, bx1, by1 = meta["bbox"]
                foot_x = ox + (fx + 0.5) * sc
                foot_y = oy + (fy + 1) * sc
                if face > 0:
                    # counter-clockwise: (x, y) -> (y, w - x); the back is down
                    x = foot_x - fy * sc
                    y = foot_y - (w - bx0) * sc
                else:
                    # clockwise: (x, y) -> (h - y, x)
                    x = foot_x - (h - fy) * sc
                    y = foot_y - (bx1 + 1) * sc
                rv.blit(r, (_msbf_px_snap(x, snap), _msbf_px_snap(y, snap)))
            else:
                outer = Transform(tr, zoom=sc / unit, nearest=crisp)
                r = renpy.render(outer, 4000, 4000, st, at)
                rv.blit(r, (_msbf_px_snap(ox + pz.dx * sc, snap), _msbf_px_snap(oy + pz.dy * sc, snap)))

        def _frame(self, meta, pose):
            """(image, frame meta, art-px offset) for a pose of this sprite.

            Pose frames are other pieces of existing art of the same form,
            aligned to the base sprite by the bottom-centre of their boxes.
            """
            if pose:
                fm = meta.get("poses", {}).get(pose)
                if fm:
                    bx0, by0, bx1, by1 = meta["bbox"]
                    fx0, fy0, fx1, fy1 = fm["bbox"]
                    return (msbf_px_image(fm), fm, ((bx0 + bx1) - (fx0 + fx1)) * 0.5, float(by1 - fy1))
            return (msbf_px_image(meta), meta, 0.0, 0.0)

        # ---- HAND-ANIMATED FRAMES ------------------------------------------
        # When a character has imported frame strips (sprites.json, under
        # "anims"), the state's frames are drawn instead of the derived base
        # sprite, and the procedural BODY warps are switched off -- drawn
        # frames carry their own motion. Whole-sprite motion (dashes, jumps,
        # knockback), flashes, tints, outlines and FX all still apply, so a
        # state with no strip yet simply keeps today's derived animation.
        MSBF_PX_ANIM_FALLBACK = {
            "dash": "attack", "heavy": "attack", "jump": "attack", "throw": "attack",
            "support": "cast", "ready": "idle", "weak": "idle", "evade": "hurt",
            "windup": "idle", "strike": "attack", "power": "cast", "rise": "idle",
        }

        def _anim_frame(self, meta, state, dt):
            anims = meta.get("anims") if meta else None
            if not anims:
                return None
            spec = anims.get(state)
            if spec is None:
                spec = anims.get(self.MSBF_PX_ANIM_FALLBACK.get(state, ""), None)
            if spec is None and state != "idle":
                spec = anims.get("idle")
            if not spec or not spec.get("frames"):
                return None
            frames = spec["frames"]
            fps = float(spec.get("fps", 10.0))
            k = int(max(0.0, dt) * fps)
            if spec.get("loop", True):
                k %= len(frames)
            else:
                k = min(k, len(frames) - 1)
            fm = frames[k]
            bfx, bfy = meta["foot"]
            ffx, ffy = fm["foot"]
            return (msbf_px_image(fm), fm, float(bfx - ffx), float(bfy - ffy))

        def _track_anim(self, holder, state, t, since=None):
            """Start a state's clock when it changes (or at a known event time)."""
            if since is not None:
                holder.anim_state = state
                holder.anim_since = since
            elif holder.anim_state != state:
                holder.anim_state = state
                holder.anim_since = t
            return t - holder.anim_since

        def _party_anim(self, a, alive, hp, guard, active, t):
            """-> (state, seconds in it) for one party member."""
            if not alive:
                return "down", self._track_anim(a, "down", t, a.down_t0)
            if a.act in ("commit", "follow"):
                st_ = a.act_style or "cast"
                return st_, self._track_anim(a, st_, t, a.act_t0 if a.act == "commit" else None)
            if t - a.hurt_t0 < 0.45:
                return "hurt", self._track_anim(a, "hurt", t, a.hurt_t0)
            if t - a.evade_t0 < 0.40:
                return "evade", self._track_anim(a, "evade", t, a.evade_t0)
            if t - a.rise_t0 < 0.50:
                return "rise", self._track_anim(a, "rise", t, a.rise_t0)
            if guard:
                return "guard", self._track_anim(a, "guard", t)
            if hp < 0.25:
                return "weak", self._track_anim(a, "weak", t)
            if active:
                return "ready", self._track_anim(a, "ready", t)
            return "idle", self._track_anim(a, "idle", t)

        def _boss_anim(self, t):
            act = self.boss_act
            dt = t - self.boss_t0
            if act == "hurt" and dt < 0.48:
                state = "hurt"
            elif act == "windup":
                state = "windup"
            elif act == "strike" and dt < 0.7:
                state = "cast" if self._enemy_magic() else "attack"
            elif act == "power" and dt < 0.8:
                state = "power"
            else:
                return "idle", t
            return state, dt

        @staticmethod
        def _still(pz):
            pz.breath = 0.0
            pz.lean = 0.0
            pz.flow = (0.0, 0.2, 2.0, 0.0)
            pz.wing = (0.0, 30.0, 40.0, 0.0)
            pz.writhe = 0.0

        def _draw_shadow(self, rv, cx, cy, w, strength, st, at):
            if strength <= 0.02 or not MSBF_ARENA_SHADERS:
                return
            h = max(8, int(w * 0.24))
            # One shadow object per (size, strength): position is the blit's
            # business, so a figure standing still reuses last frame's render
            # instead of building and rendering a fresh shader transform --
            # five of those a frame cost ~0.5ms. Strength is rounded to a
            # thousandth, well under one 8-bit step of the shadow's alpha.
            d = msbf_memo(_msbf_px_shadow_tf, int(w), h, round(float(strength), 3))
            rv.blit(renpy.render(d, int(w), h, st, at), (int(cx - w / 2), int(cy - h / 2)))

        def _draw_fx(self, rv, t, st, at):
            keep = []
            for f in self.fx:
                age = t - f.t0 - f.delay
                if age > f.dur:
                    continue
                keep.append(f)
                if age < 0:
                    continue
                # Under the illustrations the same effects are drawn on a
                # one-pixel grid: still three-tone and banded (a cel look),
                # no longer chunky.
                cell = 1.0 if getattr(self, "_art_hq", False) else float(f.cell)
                d = Transform(Solid("#00000000"), xysize=(int(f.w), int(f.h)), mesh=True, shader="msbf.pxfx",
                                u_fx_kind=float(f.kind), u_fx_p=float(age / f.dur), u_fx_cell=cell,
                                u_fx_c1=f.c1, u_fx_c2=f.c2, u_fx_c3=f.c3, u_fx_seed=float(f.seed),
                                u_fx_angle=float(f.angle), u_fx_solid=float(f.solid))
                x = _msbf_px_snap(f.x - f.w / 2.0, cell)
                y = _msbf_px_snap(f.y - f.h / 2.0, cell)
                rv.blit(renpy.render(d, int(f.w), int(f.h), st, at), (x, y))
            self.fx = keep

        def render(self, width, height, st, at):
            rv = renpy.Render(1280, 720)
            if self.last_st is not None and st < self.last_st:
                # Re-shown: forget everything in flight.
                self.fx = []
                self.actors = {}
                self.seen_fx_serial = None
                self.seen_float_serial = None
                self.boss_act = None
            self.last_st = st
            t = st
            self._rows = [r for (_m, r, _a, _h, _g, _o) in self._party()]
            if not MSBF_PX_SHADERS:
                renpy.redraw(self, 0)
                return rv
            try:
                self._poll(t)
            except Exception:
                if config.developer:
                    raise
            phase = self._phase()
            b = self.battle
            art_hq = msbf_seer_art_hq()
            self._art_hq = art_hq

            # ---- the form that just broke, coming apart under the blowout ----
            if self.break_phase is not None and t - self.break_t0 < 0.72 and b is not None and b.fx_event == "phase_blackout":
                om = msbf_px_boss_meta(self.break_phase)
                if om:
                    k = (t - self.break_t0) / 0.72
                    opz = _PXPose()
                    opz.flash = 1.0 if k < 0.12 else 0.35
                    opz.block = 1.0 if k < 0.15 else (2.0 if k < 0.4 else 4.0)
                    opz.dissolve = min(1.0, max(0.0, (k - 0.12) / 0.80))
                    opz.tear = 3.0 * k
                    opz.sx = 1.0 + 0.10 * k
                    opz.sy = 1.0 - 0.08 * k
                    opz.dx = (4.0 if int(t * 40) % 2 else -4.0) * (1.0 - k)
                    oox, ooy = msbf_px_boss_origin(self.break_phase)
                    self._draw_sprite(rv, msbf_px_image(om), om, oox, ooy, opz, t, st, at, om.get("hq") if art_hq else None)

            # ---- Matsuda ----
            bmeta = msbf_px_boss_meta(phase)
            show_boss = True
            if b is not None:
                if getattr(b, "shmup_segment_active", False):
                    show_boss = False
                if getattr(b, "phase_transition_active", False) and b.fx_event != "phase":
                    show_boss = False
            if self.mode == "select":
                show_boss = False
            if bmeta and show_boss:
                bpz = self._boss_pose(phase, t)
                if self.mode == "intro":
                    self._intro_boss(bpz, t)
                elif self.mode == "id_intro":
                    self._id_intro_boss(bpz, t)
                ox, oy = msbf_px_boss_origin(phase)
                bfx, bfy = msbf_px_boss_point(phase, "foot")
                hov = MSBF_PX_BOSS_HOVER.get(phase, 30)
                sw = (bmeta["bbox"][2] - bmeta["bbox"][0]) * bmeta["scale"] * (0.45 if phase == 1 else 0.55)
                self._draw_shadow(rv, bfx + bpz.dx * 3, bfy + hov, sw, 0.55 * bpz.alpha, st, at)
                sc = bmeta["scale"]
                if bpz.pose == "illustration" and art_hq:
                    # Illustrated mode: the genre fails the OTHER way -- for a
                    # frame or two she drops into her pixel sprite.
                    bpz.pose = None
                    self._draw_sprite(rv, msbf_px_image(bmeta), bmeta, ox, oy, bpz, t, st, at)
                elif bpz.pose == "illustration":
                    bx0, by0, bx1, by1 = bmeta["bbox"]
                    bw, bh = int((bx1 - bx0 + 1) * sc), int((by1 - by0 + 1) * sc)
                    ill = Transform(MSBF_PX_ILLUSTRATION.get(phase, MSBF_PX_ILLUSTRATION[3]), fit="contain", xysize=(bw, bh),
                                    matrixcolor=TintMatrix("#ffd6de"))
                    rv.blit(renpy.render(ill, bw, bh, st, at), (int(ox + bx0 * sc + bpz.dx * sc), int(oy + by0 * sc)))
                else:
                    bstate, bdt = self._boss_anim(t)
                    # Hand-animated strips are pixel art; Illustrated mode keeps
                    # the illustration (and the stage's motion) instead.
                    hand = None if art_hq else self._anim_frame(bmeta, bstate, bdt)
                    if hand is not None:
                        fimg, fmeta, fdx, fdy = hand
                        self._still(bpz)
                    else:
                        fimg, fmeta, fdx, fdy = self._frame(bmeta, bpz.pose)
                    self._draw_sprite(rv, fimg, fmeta, ox + fdx * sc, oy + fdy * sc, bpz, t, st, at,
                                      fmeta.get("hq") if (art_hq and hand is None) else None)

            # ---- the party, back to front ----
            party = self._party()
            n = len(party)
            if not (b is not None and getattr(b, "shmup_segment_active", False)):
                actor = None
                if b is not None and self.mode == "battle":
                    try:
                        cur = b.current_actor
                        actor = cur.id if cur is not None else None
                    except Exception:
                        actor = None
                if not hasattr(self, "_active_t0"):
                    self._active_t0 = {}
                if actor is not None and actor not in self._active_t0:
                    self._active_t0 = {actor: t}
                elif actor is None:
                    self._active_t0 = {}
                order = sorted(range(n), key=lambda k: msbf_px_slot(k, n, party[k][1], self._rows)[1])
                for i in order:
                    mid, row, alive, hp, guard, m = party[i]
                    meta = msbf_px_party_meta(mid)
                    if not meta:
                        continue
                    pz = self._party_pose(mid, i, n, row, alive, hp, guard, mid == actor, t, None)
                    if self.mode == "intro":
                        self._intro_party(pz, i, n, t)
                    elif self.mode == "id_intro":
                        self._id_intro_party(pz, i, n, t)
                    fx, fy = msbf_px_slot(i, n, row, self._rows)
                    sc = meta["scale"]
                    mfx, mfy = meta["foot"]
                    ox = fx - mfx * sc
                    oy = fy - mfy * sc
                    sw = (meta["bbox"][2] - meta["bbox"][0]) * sc * 0.55
                    self._draw_shadow(rv, fx + pz.dx * sc, fy + 2, sw, 0.5 * pz.shadow, st, at)
                    hand = None
                    if meta.get("anims") and not art_hq:
                        astate, adt = self._party_anim(self._actor(mid), alive, hp, guard, mid == actor, t)
                        hand = self._anim_frame(meta, astate, adt)
                    if hand is not None:
                        fimg, fmeta, fdx, fdy = hand
                        self._still(pz)
                        if not alive and "down" in meta.get("anims", {}):
                            pz.rot = 0       # a drawn KO frame is already lying down
                    else:
                        fimg, fmeta, fdx, fdy = self._frame(meta, pz.pose)
                    self._draw_sprite(rv, fimg, fmeta, ox + fdx * sc, oy + fdy * sc, pz, t, st, at,
                                      fmeta.get("hq") if (art_hq and hand is None) else None)

            self._draw_fx(rv, t, st, at)
            renpy.redraw(self, 0)
            return rv

        # ---- THE ENTRANCES ---------------------------------------------------
        # Both entrances are choreographed HERE, on the stage's own clock, so
        # the figures in them are the same pixel sprites the fight uses. The
        # screens in cinematics.rpy add the light, the letterbox and the name
        # card on a matching timeline (MSBF_PX_INTRO / MSBF_PX_ID_INTRO).
        def _intro_party(self, pz, i, n, t):
            # Final Fantasy's battle entry: in from the left edge, and plant.
            start = MSBF_PX_INTRO["run"] + i * 0.11
            k = (t - start) / 0.62
            if k < 0:
                pz.alpha = 0.0
                return
            if k < 1.0:
                back = 300.0 * (1.0 - _px_ease_out(k))
                pz.dx -= back * MSBF_PX_PARTY_FACE
                pz.dy -= 4.0 * abs(_pxm.sin(k * _pxm.pi * 4.0))
                pz.lean += 7.0 * (1.0 - k) * MSBF_PX_PARTY_FACE
            elif k < 1.35:
                kk = (k - 1.0) / 0.35
                pz.sy *= 1.0 - 0.07 * _pxm.sin(kk * _pxm.pi)
            # The landing shoves them back a step.
            dt = t - MSBF_PX_INTRO["land"]
            if 0.0 <= dt < 0.5:
                kick = (1.0 - _px_ease_out(dt / 0.5)) * (10.0 - i * 0.8)
                pz.dx -= kick * MSBF_PX_PARTY_FACE
                pz.lean -= 4.0 * (1.0 - dt / 0.5) * MSBF_PX_PARTY_FACE
                pz.sy *= 1.0 - 0.06 * (1.0 - dt / 0.5)

        def _intro_boss(self, pz, t):
            T = MSBF_PX_INTRO
            if t < T["fall"]:
                pz.alpha = 0.0
                return
            face = MSBF_PX_BOSS_FACE
            if t < T["land"]:
                k = (t - T["fall"]) / (T["land"] - T["fall"])
                pz.dy -= 330.0 * (1.0 - _px_ease_in(k))
                pz.sy *= 1.30
                pz.sx *= 0.88
                pz.tint = (0.55, 0.95, 1.0, 0.55 * (1.0 - k))
                pz.flash = 0.25
                pz.shadow = k
                return
            if not getattr(self, "_intro_landed", False):
                self._intro_landed = True
                fx_, fy_ = msbf_px_boss_point(1, "foot")
                cx_, cy_ = msbf_px_boss_point(1, "core")
                hov = MSBF_PX_BOSS_HOVER.get(1, 30)
                self.spawn(1, fx_, fy_ + hov - 40, 1180, 360, ((1.0, 1.0, 1.0), (0.55, 0.95, 1.0), (0.15, 0.45, 0.85)), t, 0.7, 3, solid=0.8)
                self.spawn(6, fx_, fy_ + hov - 60, 520, 300, ((0.9, 1.0, 1.0), (0.40, 0.75, 0.95), (0.18, 0.30, 0.55)), t, 0.6, 3)
                self.spawn(0, cx_, cy_ + 60, 640, 640, ((1.0, 1.0, 1.0), (0.60, 0.95, 1.0), (0.20, 0.50, 0.85)), t, 0.4, 3, solid=0.85)
            dt = t - T["land"]
            if dt < 0.12:
                pz.sy *= 0.80
                pz.sx *= 1.12
                pz.flash = 1.0 if dt < 0.05 else 0.4
            elif dt < 0.62:
                k = (dt - 0.12) / 0.50
                over = _pxm.sin(k * _pxm.pi) * 0.05
                pz.sy *= 0.80 + 0.20 * _px_ease_out(k) + over
                pz.sx *= 1.12 - 0.12 * _px_ease_out(k)
            # The glaive sweep that cuts the frame. Forward units here are
            # SCREEN units already flipped by _boss_pose, so face is applied.
            st_ = t - T["sweep"]
            if 0.0 <= st_ < 0.55:
                k = st_ / 0.55
                swing = _pxm.sin(min(1.0, k * 1.6) * _pxm.pi * 0.5) * (1.0 - _px_ease_io(max(0.0, (k - 0.6) / 0.4)))
                pz.lean += 12.0 * swing * face
                pz.dx += 10.0 * swing * face
                if not getattr(self, "_intro_swept", False) and k > 0.22:
                    self._intro_swept = True
                    self.spawn(2, 560, 360, 1500, 520, ((1.0, 1.0, 1.0), (0.55, 0.95, 1.0), (0.20, 0.55, 0.90)), t, 0.42, 3, angle=0.0, solid=0.9)

        def _id_intro_party(self, pz, i, n, t):
            # Already standing there. They arrive the way the room does: in
            # torn, mis-decoded frames.
            T = MSBF_PX_ID_INTRO
            if t < T["party"]:
                pz.alpha = 0.0
                return
            k = t - T["party"]
            if k < 0.5:
                pz.alpha = 1.0 if int(t * 22 + i) % 3 else 0.0
                pz.block = 4.0 if k < 0.25 else 2.0
                pz.tear = 2.0
            dt = t - T["light"]
            if 0.0 <= dt < 0.6:
                pz.dx -= 6.0 * (1.0 - dt / 0.6) * MSBF_PX_PARTY_FACE
                pz.flash = max(pz.flash, 0.5 * (1.0 - dt / 0.6))

        def _id_intro_boss(self, pz, t):
            T = MSBF_PX_ID_INTRO
            if t < T["boss"]:
                pz.alpha = 0.0
                return
            k = t - T["boss"]
            if k < 0.45:
                pz.alpha = 1.0 if int(t * 18) % 3 else 0.0
                pz.block = 6.0 if k < 0.2 else 3.0
                pz.poster = 3.0
                pz.tear = 3.0
            # The wings were never folded -- they open anyway, tier by tier.
            u = (t - T["unfold"]) / 1.3
            if u < 0.0:
                pz.wing = (-30.0, pz.wing[1], pz.wing[2], pz.wing[3])
            elif u < 1.0:
                e = _px_ease_out(u)
                over = _pxm.sin(u * _pxm.pi) * 8.0
                pz.wing = (-30.0 + (30.0 + pz.wing[0]) * e + over, pz.wing[1], pz.wing[2], pz.wing[3])
            dt = t - T["light"]
            if 0.0 <= dt < 0.4:
                pz.flash = max(pz.flash, 0.8 * (1.0 - dt / 0.4))
                if not getattr(self, "_id_lit", False):
                    self._id_lit = True
                    hx_, hy_ = msbf_px_boss_point(2, "head")
                    self.spawn(1, hx_, hy_, 900, 900, ((1.0, 1.0, 0.92), (1.0, 0.82, 0.42), (0.70, 0.45, 0.20)), t, 0.9, 3, solid=0.8)
                    self.spawn(4, hx_, 360, 360, 720, ((1.0, 1.0, 0.95), (1.0, 0.86, 0.50), (0.75, 0.50, 0.25)), t, 1.1, 3, solid=0.55)

        def event(self, ev, x, y, st):
            return None

        def visit(self):
            return []

    # The party select's formation preview: the picked party, standing in the
    # rows they will fight in, as the sprites they will fight as. One stage per
    # distinct (picks, rows) so a redraw never restarts their idles.
    MSBF_PX_SELECT_STAGES = {}

    def msbf_px_select_stage(picks, rows):
        key = (tuple(picks), tuple(rows.get(m, "front") for m in picks))
        st = MSBF_PX_SELECT_STAGES.get(key)
        if st is None:
            if len(MSBF_PX_SELECT_STAGES) > 24:
                MSBF_PX_SELECT_STAGES.clear()
            st = MSBFPixelStage(None, "select", 1, list(picks), dict(rows))
            MSBF_PX_SELECT_STAGES[key] = st
        return st

    # ONE stage per battle, reused across every re-execution of the screen.
    # A new stage object per redraw would restart every animation clock each
    # time the fight's state changed. Not saved: init-time dict, mutated.
    MSBF_PX_STAGES = {}

    def msbf_px_stage(battle, mode="battle"):
        key = (id(battle), mode)
        st = MSBF_PX_STAGES.get(key)
        if st is None or st.battle is not battle:
            if len(MSBF_PX_STAGES) > 4:
                MSBF_PX_STAGES.clear()
            st = MSBFPixelStage(battle, mode)
            MSBF_PX_STAGES[key] = st
        return st
