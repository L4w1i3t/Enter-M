# Main-menu Arcade library and direct gameplay/result wrappers.
# Finished modes are immediately available; missing story-clear flags route
# through arcade_story_warning before launch. Persistent clear keys stay stable.
# Arcade contexts preserve the caller and return to the hub after results.
# arcade_active selects gameplay-only ending branches and is cleared on exit.
#
# Shipped covers use explicit optimized assets; discovery also supports title
# slugs under addons/Arcade/art and an engraved fallback. Cached lobby artwork
# shares the illustrated menu palette. Hover glints finish and idle poses stop
# requesting redraws; retain this when extending the library.

default persistent.arcade_id_cleared = False
default persistent.arcade_monika_cleared = False

# Global "we are inside an arcade run" flag. Rollback-managed default; the fight
# labels read it to pick the arcade branch. Reset to False on every exit.
default arcade_active = False

# Same clipped ticket silhouette and nine-slice geometry as IM_TAB_SELECTED.
define -2 ARCADE_PLAY_HOVER = Frame("assets/gui/menu/illustrated/arcade/play_hover.svg", 20, 16)


# =============================================================================
# SHADERS  (gl2 / GLSL ES 3.00)
# Registered defensively at init -10, before any screen or style can reference
# the factories below. All three output PREMULTIPLIED alpha, matching Matsu'Py's
# GL2 pipeline and the project's other shaders (phone panels, cal dial).
#
# CRITICAL (same rules as the phone/calendar shaders): a shader only engages via
# the mesh/model path, so every factory sets `mesh True` on a Transform whose own
# xysize (or whose pre-sized child) defines u_model_size, over an OPAQUE base --
# a transparent base is culled before the shader can run. Registration happens in
# `init python`, which does NOT re-run on hot-reload: edits to the GLSL below
# need a FULL game restart, not a Shift+R.
# =============================================================================
init -10 python:
    def _enter_m_arcade_register_shaders():

        # ---- field: the whole-hub background -------------------------------
        # Vertical indigo->black gradient, two soft blooms tinted to the SELECTED
        # cartridge's accent (one behind the featured art, one upper-right), a
        # third low glow seating the library rail, a darker "shelf" band under
        # it, fine CRT scanlines and a vignette. Opaque; ignores tex0.
        #
        # Deliberately STATIC (no u_time): it only changes when the selection
        # changes, so its render caches once and the hub costs nothing to hold on
        # screen. An ambient u_time drift here would have been imperceptible AND
        # unreliable -- see the u_sweep note on enter_m.arcade_cart for why
        # u_time animation can't be trusted to advance on this screen.
        renpy.register_shader("enter_m.arcade_field", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_model_size;
            uniform vec4 u_accent;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 size = max(u_model_size, vec2(1.0));
            vec2 uv = v_tex_coord;
            float aspect = size.x / max(size.y, 1.0);

            vec3 top = vec3(0.129, 0.094, 0.239);
            vec3 mid = vec3(0.078, 0.055, 0.157);
            vec3 bot = vec3(0.024, 0.016, 0.051);
            vec3 col = mix(top, mid, smoothstep(0.0, 0.55, uv.y));
            col = mix(col, bot, smoothstep(0.55, 1.0, uv.y));

            vec3 acc = u_accent.rgb;
            vec2 d1 = (uv - vec2(0.30, 0.42)) * vec2(aspect, 1.0);
            col += acc * exp(-dot(d1, d1) * 2.2) * 0.26;
            vec2 d2 = (uv - vec2(0.78, 0.24)) * vec2(aspect, 1.0);
            col += acc * exp(-dot(d2, d2) * 5.0) * 0.10;
            vec2 d3 = (uv - vec2(0.50, 0.82)) * vec2(aspect * 0.30, 1.0);
            col += acc * exp(-dot(d3, d3) * 12.0) * 0.07;

            col += vec3(0.020, 0.015, 0.032) * sin((uv.x * 0.8 + uv.y * 1.6) * 3.14159265);

            col *= 1.0 - smoothstep(0.66, 0.75, uv.y) * 0.28;
            col *= 1.0 - 0.05 * (0.5 + 0.5 * sin(uv.y * size.y * 3.14159265));

            vec2 vv = (uv - vec2(0.5)) * vec2(1.06, 1.0);
            col *= 1.0 - smoothstep(0.30, 0.88, length(vv)) * 0.45;

            gl_FragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
        """)

        # ---- panel: rounded gradient plate ---------------------------------
        # The hub's universal surface: rounded rect, u_top -> u_bottom gradient
        # (vertical, or horizontal when u_horiz is 1 -- used for the accent
        # rules), a whisper of top sheen + scanline, and an optional inner border
        # ring. Ignores tex0; the SDF keeps corners crisp at any size.
        renpy.register_shader("enter_m.arcade_panel", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_model_size;
            uniform float u_radius;
            uniform float u_horiz;
            uniform vec4 u_top;
            uniform vec4 u_bottom;
            uniform float u_border;
            uniform vec4 u_bcolor;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float enterm_arc_rr(vec2 p, vec2 b, float r) {
                vec2 q = abs(p) - b + vec2(r);
                return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - r;
            }
        """, fragment_300="""
            vec2 size = max(u_model_size, vec2(1.0));
            vec2 uv = v_tex_coord;
            vec2 p = uv * size - size * 0.5;
            vec2 halfb = size * 0.5;
            float rad = clamp(u_radius, 0.0, min(halfb.x, halfb.y));
            float d = enterm_arc_rr(p, halfb, rad);
            float aa = 1.25;
            float fill = 1.0 - smoothstep(0.0, aa, d);

            float t = mix(clamp(uv.y, 0.0, 1.0), clamp(uv.x, 0.0, 1.0), clamp(u_horiz, 0.0, 1.0));
            vec4 g = mix(u_top, u_bottom, smoothstep(0.0, 1.0, t));
            vec3 col = g.rgb;
            float a = g.a;

            col += vec3(1.0) * smoothstep(0.34, 0.0, uv.y) * 0.045;
            col *= 1.0 - 0.030 * (0.5 + 0.5 * sin(uv.y * size.y * 3.14159265));

            float bw = max(u_border, 0.0);
            float band = (1.0 - smoothstep(bw - aa, bw + aa, abs(d))) * step(d, 0.0) * step(0.001, bw);
            float w = band * u_bcolor.a;
            col = mix(col, u_bcolor.rgb, w);
            a = mix(a, max(a, u_bcolor.a), w) * fill;

            gl_FragColor = vec4(clamp(col, 0.0, 1.0) * a, a);
        """)

        # ---- cart: the cartridge face --------------------------------------
        # Takes the child (box art, or a flat accent Solid when a mode has none)
        # and makes a jewel case of it: rounded corners, top gloss, inner
        # vignette, scanline, accent edge ring (u_edge), a desaturating grey-out
        # for unavailable/coming-soon slots (u_dim), and the HOVER treatment --
        # overall brighten plus a specular band travelling across the face
        # (u_hover / u_sweep, both driven by arcade_cart_fx).
        # u_art 0 swaps the picture plane for a lit blank-case gradient built out
        # of the accent, so an art-less mode still looks like a real card.
        #
        # NOTE the glint position is u_sweep, an ATL-interpolated uniform, and
        # NOT the ambient u_time. Matsu'Py only advances u_time on frames it
        # actually draws, and it only draws when some displayable asks it to. The
        # menu scanline (menu_scanline_slow) naps for 2.2s every cycle, so a
        # u_time glint sat frozen through that window and then jumped -- measured
        # at 0-20fps in the dead window vs ~240fps outside it. An interpolating
        # ATL property requests a redraw every frame it runs, so the sweep now
        # paces itself and stays smooth no matter what else is on screen.
        renpy.register_shader("enter_m.arcade_cart", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_model_size;
            uniform float u_radius;
            uniform float u_art;
            uniform float u_dim;
            uniform float u_edge;
            uniform float u_hover;
            uniform float u_sweep;
            uniform vec4 u_accent;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float enterm_arc_cart_rr(vec2 p, vec2 b, float r) {
                vec2 q = abs(p) - b + vec2(r);
                return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - r;
            }
        """, fragment_300="""
            vec2 size = max(u_model_size, vec2(1.0));
            vec2 uv = v_tex_coord;
            vec2 p = uv * size - size * 0.5;
            vec2 halfb = size * 0.5;
            float rad = clamp(u_radius, 0.0, min(halfb.x, halfb.y));
            float d = enterm_arc_cart_rr(p, halfb, rad);
            float aa = 1.25;
            float mask = 1.0 - smoothstep(0.0, aa, d);

            vec4 src = texture2D(tex0, uv);
            float sa = max(src.a, 0.0001);
            vec3 col = src.rgb / sa;
            vec3 acc = u_accent.rgb;

            if (u_art < 0.5) {
                vec3 deep = acc * 0.18 + vec3(0.025, 0.018, 0.050);
                float rr = length((uv - vec2(0.5, 0.42)) * vec2(1.0, 1.06));
                col = mix(acc * 0.95, deep, smoothstep(0.06, 0.80, rr));
                col *= 1.0 + 0.05 * sin((uv.x + uv.y) * 23.0);
            }

            col += vec3(1.0) * smoothstep(0.40, 0.0, uv.y) * 0.10;
            float iv = smoothstep(0.52, 1.02, length((uv - vec2(0.5)) * 1.42));
            col *= 1.0 - iv * 0.38;
            col *= 1.0 - 0.045 * (0.5 + 0.5 * sin(uv.y * size.y * 3.14159265));

            float lum = dot(col, vec3(0.299, 0.587, 0.114));
            col = mix(col, vec3(lum) * 0.45, clamp(u_dim, 0.0, 1.0));

            float h = clamp(u_hover, 0.0, 1.0);
            col *= 1.0 + 0.16 * h;
            float bandc = uv.x * 0.55 + uv.y * 0.45;
            float st = (bandc - u_sweep) * 5.5;
            col += vec3(0.58, 0.55, 0.66) * exp(-st * st) * h * 0.35;

            float ew = 2.0 + 2.2 * h;
            float ring = (1.0 - smoothstep(ew - aa, ew + aa, abs(d))) * step(d, 0.0);
            vec3 edgec = mix(acc, vec3(1.0), 0.18 + 0.40 * h);
            col = mix(col, edgec, ring * clamp(u_edge, 0.0, 1.0) * (0.55 + 0.45 * h));

            float a = mask * min(sa, 1.0);
            gl_FragColor = vec4(clamp(col, 0.0, 1.0) * a, a);
        """)

    try:
        _enter_m_arcade_register_shaders()
    except Exception as e:
        renpy.log("ENTER-M ARCADE: shader registration failed: %r" % e)


# =============================================================================
# COLOR HELPERS + DISPLAYABLE FACTORIES
# init -2 so they exist before any screen OR style statement (init 0) uses them.
# =============================================================================
init -2 python:
    # --- color helpers -------------------------------------------------------

    def _arcade_mix(hexcol, target="#ffffff", t=0.26):
        # Linear blend of `hexcol` toward `target` (used for hover-brighten and
        # soft accent tints). Returns a "#rrggbb" string.
        try:
            h = hexcol.lstrip("#")
            g2 = target.lstrip("#")
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            tr, tg, tb = int(g2[0:2], 16), int(g2[2:4], 16), int(g2[4:6], 16)
            r = int(round(r + (tr - r) * t))
            g = int(round(g + (tg - g) * t))
            b = int(round(b + (tb - b) * t))
            return "#%02x%02x%02x" % (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        except Exception:
            return hexcol

    # "#rgb"/"#rgba"/"#rrggbb"/"#rrggbbaa" (or an rgb/rgba tuple) -> a
    # normalized (r, g, b, a) suitable as a vec4 uniform. The parser is the
    # project-wide one (game/fx.rpy, init -5); this is just the local name.
    _arcade_vec4 = enter_m_rgba

    # --- displayable factories ----------------------------------------------
    # Each wraps an OPAQUE base in a mesh Transform whose xysize sets
    # u_model_size (the PhonePanel pattern).
    @renpy.pure
    def ArcadeField(accent="#e0455e", width=1280, height=720):
        # The hub's whole-screen gradient field, tinted to the selected game.
        return Transform(
            Solid("#000000"),
            xysize=(int(width), int(height)),
            mesh=True,
            shader="enter_m.arcade_field",
            u_accent=_arcade_vec4(accent),
        )

    # MEMOIZED: the same arguments hand back the SAME plate. A Transform has no
    # value equality, so a screen that re-executes (a reveal timer ticking, a
    # hover restarting the interaction) could never reuse a freshly built one --
    # every update built a new shader Transform and paid a new render for it.
    # Arguments here come from UI code, so the set is small; the clear is a
    # backstop, not an eviction policy.
    _ARCADE_PANEL_CACHE = {}

    @renpy.pure
    def ArcadePanel(width, height, top="#1e1742ee", bottom=None, radius=16.0,
                    border=0.0, border_color="#00000000", horiz=False):
        # A rounded gradient plate: pages, badges, keycap plates, meters, the
        # PLAY button, the modal panels. `horiz` runs the gradient left->right
        # (the header/rail accent rules).
        key = (int(round(width)), int(round(height)), top, bottom, float(radius),
               float(border), border_color, bool(horiz))
        hit = _ARCADE_PANEL_CACHE.get(key)
        if hit is not None:
            return hit
        if len(_ARCADE_PANEL_CACHE) > 1024:
            _ARCADE_PANEL_CACHE.clear()
        top_rgba = _arcade_vec4(top)
        bot_rgba = _arcade_vec4(bottom) if bottom is not None else top_rgba
        hit = _ARCADE_PANEL_CACHE[key] = Transform(
            Solid("#000000"),
            xysize=(key[0], key[1]),
            mesh=True,
            shader="enter_m.arcade_panel",
            u_radius=float(radius),
            u_horiz=(1.0 if horiz else 0.0),
            u_top=top_rgba,
            u_bottom=bot_rgba,
            u_border=float(border),
            u_bcolor=_arcade_vec4(border_color),
        )
        return hit

    # The MATSUCOM console badge: a gold faceplate with slanted block letters,
    # after the Famicom's colours. Saved at 3x its 279x47 layout size and
    # declared OVERSAMPLED, so it stays sharp in big windows without a zoom.
    ARCADE_LOGO = Image("assets/gui/menu/illustrated/arcade/matsucom_logo.png", oversample=3)

    def ArcadeCartFace(size, color, art=None, case_trim=False):
        # A cartridge's picture plane, pre-sized square so the cart shader sees
        # u_model_size == (size, size). Box art if we have it, flat accent (which
        # the shader turns into a lit blank case) if we don't.
        s = int(round(size))
        if art:
            # fit="cover" SCALES but never CROPS. A 512x768 poster came out
            # 320x480, and the featured card -- which has no case trim to hold
            # it -- painted all of it, straight past the bottom of its frame.
            # (The shelf only looked right because its Composite happened to
            # clip.) Seat the covered art in an exact square and crop to it:
            # centred across, pinned to the TOP, since a poster's title lives
            # there.
            face = Transform(
                Fixed(Transform(art, xysize=(s, s), fit="cover",
                                xalign=0.5, yalign=0.0),
                      xysize=(s, s)),
                crop=(0, 0, s, s))
        else:
            face = Solid(color, xysize=(s, s))
        if case_trim:
            # Print fittings belong to the card, so selection/hover poses and
            # rounded clipping move the art and fittings as one surface.
            return Composite((s, s),
                (0, 0), face,
                (0, 0), Transform("assets/gui/menu/illustrated/arcade/cartridge_trim.svg", xysize=(s, s)))
        return face

    # --- box art resolution --------------------------------------------------
    # Convention: game/addons/Arcade/art/<slug>.png (see the file header). A tile
    # may also name an explicit path, which is tried first. Called per cartridge
    # on every screen rebuild, which is fine -- renpy.loadable keeps its own
    # cache, and deliberately NOT caching here means a cover dropped in while the
    # game is running shows up on the next reload instead of needing a restart.
    ARCADE_ART_DIR = "addons/Arcade/art"
    ARCADE_ART_EXTS = (".png", ".jpg", ".jpeg", ".webp")

    def _arcade_slug(title):
        s = "".join((ch if ch.isalnum() else "_") for ch in title.lower())
        while "__" in s:
            s = s.replace("__", "_")
        return s.strip("_")

    def arcade_art_for(title, explicit=None):
        # -> a loadable image path, a displayable, or None to fall back to the
        # plain color.
        #
        # "ag:<kind>" is not a path: it names a PROCEDURALLY DRAWN cover owned
        # by an Arcade Original (game/addons/Arcade/games). Those covers are
        # generated out of the same parts as their playfields, and are resolved
        # here at call time rather than in the tile table, because the table is
        # built before those files have registered anything. A real PNG at
        # art/<slug>.png still wins over a generated cover -- drop one in and
        # nothing needs editing.
        procedural = None
        if isinstance(explicit, str) and explicit.startswith("ag:"):
            procedural = explicit[3:]
            explicit = None

        cands = []
        if explicit:
            cands.append(explicit)
        slug = _arcade_slug(title)
        for ext in ARCADE_ART_EXTS:
            cands.append("%s/%s%s" % (ARCADE_ART_DIR, slug, ext))

        for c in cands:
            try:
                if renpy.loadable(c):
                    return c
            except Exception:
                pass

        if procedural:
            try:
                return ag_cover(procedural)
            except Exception:
                pass

        return None

    # --- shelf thumbnails ----------------------------------------------------
    # The shelf draws a card at 126px. The featured cover draws at 320px. Handing
    # the shelf the full-size cover meant decoding eight 512px images to show
    # them at a quarter of that, and MEASURED (Aug 31 2026, cache-instrumented)
    # that was 53ms of the hub's 130ms cold open -- its single largest cost.
    #
    # A 384px thumbnail beside the art covers a 126px card at 3x display scale,
    # so nothing is drawn below its own resolution at 4K, and the eight of them
    # decode in ~21ms instead of ~53ms.
    #
    # THE THUMBNAIL IS AN OPTIMISATION, NEVER A REQUIREMENT. A missing one falls
    # straight back to the full cover, so the "drop art/<slug>.png in and you are
    # done" convention in the file header still holds exactly as written -- a new
    # cover simply costs a few more milliseconds until someone generates a thumb.
    ARCADE_THUMB_DIR = "addons/Arcade/art/thumbs"

    def arcade_art_thumb(art):
        # Procedural covers (ag_cover) come back as displayables, not paths, and
        # are already drawn at whatever size they are asked for.
        if not isinstance(art, str):
            return art

        cand = "%s/%s.webp" % (
            ARCADE_THUMB_DIR, art.rsplit("/", 1)[-1].rsplit(".", 1)[0])
        try:
            if renpy.loadable(cand):
                return cand
        except Exception:
            pass

        return art


# --- TILE TABLE --------------------------------------------------------------
# Data-driven. Each entry:
#   (title, genre_tag, blurb, accent_color, art_path,
#    prerequisite_cleared_fn, launch_action)
# art_path is an EXPLICIT box-art override (None = use the art/<slug>.png
# convention, and fall back to the plain accent color if that's missing).
# prerequisite_cleared_fn is a ZERO-ARG callable used only to decide whether a
# content warning is needed (Tsubaki's check is a compound expression).
# launch_action fires for every finished game; None marks a "coming soon" slot.
# Future modes with no prerequisite use `lambda: True` and launch directly.
init python:
    arcade_items = [
        ("Ontological Seer", "PRESS-TURN BOSS",
            "Matsuda's four-on-one press-turn boss battle. Read her tempo, exploit the weakness, and grind down one absurd health bar.",
            "#e0455e", "addons/Arcade/art/ontological_seer_classic.webp",
            lambda: persistent.id_mode_unlocked,
            Function(arcade_launch, "arcade_play_msbf")),
        ("Ontological Seer: Id", "SUPERBOSS REMATCH",
            "The rematch with every safety off -- Matsuda throws every genre into a blender. Her no-warmup superboss form.",
            "#8a5cff", "addons/Arcade/art/ontological_seer_id_classic.webp",
            lambda: persistent.arcade_id_cleared,
            Function(arcade_launch, "arcade_play_msbf", id_mode=True)),
        ("A Fine Date", "ANTI-DATING SIM",
            "One evening, one exit. Every honest 'no' walks her a step closer to the open door.",
            "#4fbf7a", "addons/Arcade/art/a_fine_date_classic.webp",
            lambda: persistent.arcade_monika_cleared,
            Function(arcade_launch, "arcade_play_monika")),
        ("Embodiment of Violet Ink", "BULLET HELL",
            "Kotonoha's danmaku recital. Dodge every word. Normal, Endless, or Practice.",
            "#ff6fae", "addons/Arcade/art/embodiment_of_violet_ink_doujin.webp",
            lambda: persistent.kotomode_cleared,
            Show("arcade_koto_variant")),
        ("The Unwritten Act", "SOUL BOX FIGHT",
            "Tsubaki's SOUL box duel. Cut the strings -- violently or passively.",
            "#d9c68a", "addons/Arcade/art/the_unwritten_act_ui.webp",
            lambda: persistent.tsubamode_outcome is not None,
            Function(arcade_launch, "arcade_play_tsubaki")),
        ("Asarhythm", "FOUR-KEY RHYTHM BATTLE",
            "Asahina has the stage and a hunger for a revolution. "
            "Press to the beat and defeat her in a battle of song.",
            "#f36bc3", "addons/Arcade/art/asahina_rhythm.webp",
            lambda: persistent.asahina_rhythm_cleared,
            Function(arcade_launch, "arcade_play_asahina_rhythm")),

        # --- MATSUCOM ORIGINALS ----------------------------------------------
        # Cabinets with no story attachment: they exist only here, so their
        # prerequisite is `lambda: True` (always cleared -> no content notice)
        # and their covers use a shared 16-bit-era print direction. The
        # procedural "ag:<kind>" resolver remains available as a fallback for
        # future cabinets, but shipped covers are explicit optimized assets.
        # All four run on the shared cabinet in addons/Arcade/games/ag_core.rpy
        # and launch through one label with the cabinet named as a parameter.
        ("Ouroboros Protocol", "GRID SURVIVAL",
            "Samples rot where they sit. Eat them fresh, loop your body "
            "around the rot to clear it, and hold Shift to sprint if you "
            "can spare the length.",
            "#57d6a8", "addons/Arcade/art/ouroboros_protocol_classic.webp",
            lambda: True,
            Function(arcade_launch, "ag_play", ag_kind="snake")),
        ("Peer Review", "BRICK BREAKER",
            "A brick breaker on a page of claims. Knock out a gold source "
            "and everything tethered to it collapses, and stamp your returns "
            "for a harder hit.",
            "#ff8f5e", "addons/Arcade/art/peer_review_classic.webp",
            lambda: True,
            Function(arcade_launch, "ag_play", ag_kind="brick")),
        ("Intake", "FALLING BLOCKS",
            "Stack racks of three, four and five cells and clear full rows. "
            "Flip a rack instead of holding one, and keep the mold down.",
            "#5ec8e0", "addons/Arcade/art/intake_classic.webp",
            lambda: True,
            Function(arcade_launch, "ag_play", ag_kind="intake")),
        ("Containment Sweep", "DEDUCTION",
            "Find every incident without stepping on one. Some numbers count "
            "two tiles out, and a hazmat suit covers one mistake.",
            "#e0c05e", "addons/Arcade/art/containment_sweep_classic.webp",
            lambda: True,
            Function(arcade_launch, "ag_play", ag_kind="sweep")),
        ("Board Meeting", "CHESS",
            "Chess against four people who all want this over with. An "
            "intern who thinks out loud, a professional on a clock, a "
            "grandmaster on the same clock, and a model that reads you while "
            "you play and forgets you when you leave.",
            "#8fa8ff", "addons/Arcade/art/board_meeting_classic.webp",
            lambda: True,
            Function(arcade_launch, "ag_play", ag_kind="chess")),
        ("Outlier", "PEG SHOOTER",
            "Aim, fire, and let it fall. Clear all twenty-two outliers with "
            "fifteen balls, and save a few for the bonus round.",
            "#46c7e8", "ag:peg",
            lambda: True,
            Function(arcade_launch, "ag_play", ag_kind="peg")),

        # "Coming soon" slot (action None). When it is ready, give it a launch
        # action and use `lambda: True` if no story prerequisite applies.
        ("Coming Soon", "NEW GAMES",
            "More pick-up-and-play games are on the way!",
            "#5a5a6e", None,
            lambda: False, None),
    ]

    ARCADE_ORIGINAL_TITLES = frozenset((
        "Ouroboros Protocol",
        "Peer Review",
        "Intake",
        "Containment Sweep",
        "Board Meeting",
        "Outlier",
    ))

    def arcade_entry_is_original(entry):
        return entry[0] in ARCADE_ORIGINAL_TITLES

    def arcade_asahina_rhythm_award(result):
        """Pay one completed rhythm attempt through the boss-cabinet economy."""
        # Core results come from an imported .py module; Ren'Py's rollback dict
        # class does not recognize ordinary Python dictionaries as instances.
        if not isinstance(result, python_dict):
            return 0
        if result.get("_arcade_rewarded"):
            return result.get("coins", 0)
        result["_arcade_rewarded"] = True
        result["coins"] = 0
        if (result.get("outcome") not in ("clear", "failed")
                or result.get("practice") or result.get("autoplay")
                or not result.get("eligible", False)):
            return 0
        result["coins"] = mc_award_mode(
            "asahina_rhythm", "ASARHYTHM",
            result["outcome"] == "clear")
        return result["coins"]

    def arcade_prerequisite_is_cleared(prerequisite_cleared_fn):
        """Return whether a mode's prerequisite content has been experienced."""
        try:
            return bool(prerequisite_cleared_fn())
        except Exception:
            # Fail closed: an invalid predicate should show the warning rather
            # than silently exposing potentially spoiler-heavy content.
            return False

    def arcade_entry_action(title, prerequisite_cleared_fn, launch_action):
        """Build the action used by PLAY/Enter for one catalog entry."""
        if launch_action is None:
            return Show(
                "dialog",
                message="This slot is coming soon.",
                ok_action=Hide("dialog"),
            )
        if arcade_prerequisite_is_cleared(prerequisite_cleared_fn):
            return launch_action
        return Show(
            "arcade_story_warning",
            mode_title=title,
            proceed_action=launch_action,
        )


# =============================================================================
# SCREENS
# =============================================================================

# --- CARTRIDGE (box art card) ------------------------------------------------
# One square jewel case carrying NOTHING but its cover art (or, with no art, the
# plain accent color the shader lights into a blank case). Deliberately text-free
# -- the title / genre / blurb all live in the description panel beside it, so
# the shelf reads like a rack of real games. The WHOLE square is the click
# target; the shader handles corners, gloss, edge, grey-out and the hover sweep.
#
#   available      : True for every finished mode; False for an empty slot
#   edge_strength  : 0..1 accent-edge strength (selected carts get 1.0)
#   click_action   : what clicking the card does
#   pose_transform : the pose transform (arcade_thumb / arcade_feature_pop)
#
# HOVER PLUMBING -- the shape of this screen is load-bearing. Matsu'Py only hands
# hover/idle transform events to a button's DIRECT child (Button.focus ->
# self.child.set_transform_event), and containers like Fixed do NOT pass them
# further down -- only Transform does. So the face's shader transform has to be
# the button's one and only child, and the coming-soon badge has to be a SIBLING
# of the button rather than sitting inside it. (Badges are not focusable, so they
# do not steal the click.) Nest the face deeper and u_hover silently never fires.
screen arcade_cart(accent_color, available, card_size, artwork=None, edge_strength=0.35, click_action=None, pose_transform=None, cart_id=None, case_trim=False):
    python:
        _display_accent = accent_color if available else "#6d6860"
        _dim_strength = 0.0 if available else 0.86
        _corner_radius = max(6.0, round(card_size * 0.055))
        _display_artwork = artwork or "assets/gui/menu/illustrated/arcade/coming_soon.svg"
        _has_artwork = 1.0
        _accent_vector = _arcade_vec4(_display_accent)
        _badge_size = max(24, int(card_size * 0.20))
        _badge_inset = max(8, int(card_size * 0.045))
    fixed:
        xysize (card_size, card_size)
        align (0.5, 0.5)
        button:
            style "arcade_blank_button"
            id (cart_id or "arcade_cart")
            xysize (card_size, card_size)
            action click_action
            at pose_transform
            add ArcadeCartFace(card_size, _display_accent, _display_artwork, case_trim) at arcade_cart_fx(
                _corner_radius,
                _accent_vector,
                _has_artwork,
                _dim_strength,
                edge_strength,
            )
        if not available:
            fixed:
                xysize (_badge_size, _badge_size)
                pos (card_size - _badge_size - _badge_inset, card_size - _badge_size - _badge_inset)
                use arcade_coming_soon_badge(_badge_size)


# --- COMING-SOON BADGE -------------------------------------------------------
# A small lower-right ellipsis stamp marks the unavailable catalog slot without
# covering its engraved joystick artwork. Story prerequisites never affect
# cartridge availability.
screen arcade_coming_soon_badge(badge_size):
    python:
        _dot_size = max(3, int(round(badge_size * 0.11)))
        _dot_spacing = _dot_size + max(2, int(round(badge_size * 0.07)))
        _dot_y = (badge_size - _dot_size) // 2
        _ink_color = "#e7e0f4"
    fixed:
        xysize (badge_size, badge_size)
        align (0.5, 0.5)
        add ArcadePanel(
            badge_size,
            badge_size,
            top="#0b0818e0",
            bottom="#05030de0",
            radius=(badge_size / 2.0),
            border=1.5,
            border_color="#ffffff2e",
        )
        add Solid(_ink_color) xysize (_dot_size, _dot_size) pos (badge_size // 2 - _dot_spacing - _dot_size // 2, _dot_y)
        add Solid(_ink_color) xysize (_dot_size, _dot_size) pos (badge_size // 2 - _dot_size // 2, _dot_y)
        add Solid(_ink_color) xysize (_dot_size, _dot_size) pos (badge_size // 2 + _dot_spacing - _dot_size // 2, _dot_y)


# --- BACKDROP ----------------------------------------------------------------
# The painted console room remains visible behind engraved brass and coral
# cabinet fittings. Chrome is cached SVG/Frame artwork; the old full-screen
# scanline/gradient shader no longer runs over the room on every drawn frame.
screen arcade_backdrop(accent):
    add "assets/backgrounds/matsudavr.png"
    add "vignette":
        alpha 0.22
    add "assets/gui/menu/illustrated/arcade/surround.svg"


# --- KEYCAP CHIP -------------------------------------------------------------
# Auto-sizing little key plate used by the footer legend + the PLAY hint.
screen arcade_keycap_chip(klabel):
    frame:
        style "arcade_keycap"
        yalign 0.5
        text klabel style "arcade_keycap_text"


# --- STORY-CONTENT WARNING ---------------------------------------------------
# Shown only when a player launches a finished mode before its existing clear
# predicate has been satisfied. This is a Show() overlay rather than a called
# screen, so both choices explicitly hide it; Return() here would exit the hub.
screen arcade_story_warning(mode_title, proceed_action):
    modal True
    zorder 90
    use enter_m_input_lock()
    use arcade_backdrop("#ffb454")
    add Solid("#14212ade")

    frame:
        xalign 0.5
        yalign 0.5
        xysize (760, 360)
        padding (0, 0, 0, 0)
        background IM_DARK_PANEL

        vbox:
            xpos 34
            ypos 28
            xsize 692
            spacing 13

            hbox:
                spacing 12
                add Solid("#ffb454") xysize (5, 18) yalign 0.5
                text "CONTENT NOTICE" style "arcade_kicker" color IM_GOLD yalign 0.5

            text mode_title:
                style "arcade_feature_title"
                size 34
                color IM_PAPER

            add Solid("#e1bf8070") xysize (692, 1)

            text ("This mode appears later in the story. Playing it now may reveal events or undercut its intended introduction."):
                style "arcade_feature_blurb"
                size 18
                color IM_MUTED
                xsize 692

            text "Continue into the standalone mode anyway?":
                style "arcade_prompt_hint"
                size 16
                color IM_MUTED

            null height 6

            hbox:
                xalign 1.0
                spacing 12

                button:
                    xysize (190, 54)
                    id "arcade_warning_back"
                    padding (0, 0)
                    background IM_TAB_IDLE
                    hover_background IM_TAB_HOVER
                    hover_sound gui.hover_sound
                    activate_sound gui.activate_sound
                    action Hide("arcade_story_warning")
                    text "GO BACK" style "arcade_play_text" size 17 align (0.5, 0.5)

                button:
                    xysize (246, 54)
                    id "arcade_warning_play"
                    padding (0, 0)
                    background IM_TAB_IDLE
                    hover_background IM_TAB_HOVER
                    hover_sound gui.hover_sound
                    activate_sound gui.activate_sound
                    action [Hide("arcade_story_warning"), proceed_action]
                    text "PLAY ANYWAY" style "arcade_play_text" size 17 align (0.5, 0.5)

    key "K_ESCAPE" action Hide("arcade_story_warning")
    key "game_menu" action Hide("arcade_story_warning")


# --- THE HUB (catalog) -------------------------------------------------------
# `tag menu` -> shown via ShowMenu from the main menu; Escape pops back with the
# menu BGM. A "classic edition" library: a big featured cartridge + description
# page over a highlighted shelf of cards. `sel` is the selected index; the
# cartridge border and genre marker retain the selected game's accent within
# the shared paper-and-ink cabinet fittings.
#
# NAVIGATION: there are no arrows -- every shelf card is a full-square selection
# target. Launch from the large featured cover, PLAY, or Enter; this prevents a
# second click on the selected shelf item from unexpectedly starting a game.
#
# STABLE GEOMETRY: each shelf card sits in a fixed 156px slot and the featured
# card in a fixed 320px box, so the selection/hover zooms grow inside their own
# space instead of reflowing the row (and the description page keeps its
# fixed-height template).
screen arcade_hub():
    tag menu
    default sel = 0

    # HARD-RESET arcade_active on entry so a run that somehow left it set can
    # never taint the next in-story fight.
    #
    # The hub track is asked for in the SAME interaction that starts the move,
    # which is what lets the two land together: the main-menu track fades out
    # under the channel change, the picture holds on a dead channel, and the
    # Arcade theme cuts in at full volume as the hub rebuilds. See
    # menu_transitions.rpy section 6.
    # mc_refresh settles any Matsucoins owed for things earned elsewhere (an
    # achievement, a side story) so the header's wallet is correct the moment
    # the hub draws. It is a void wrapper on purpose -- an event action that
    # returns a value ends the interaction and bubbles it up like Return().
    on "show" action [SetVariable("arcade_active", False), EnterMMenuMusic(audio.arcade_theme), Function(mc_refresh)]
    on "replace" action [SetVariable("arcade_active", False), EnterMMenuMusic(audio.arcade_theme), Function(mc_refresh)]

    $ n = len(arcade_items)
    python:
        cur_title, cur_tag, cur_blurb, cur_color, cur_art_path, cur_prerequisite_fn, cur_action = arcade_items[sel]
        cur_art = arcade_art_for(cur_title, cur_art_path)
        cur_soon = (cur_action is None)
        cur_playable = not cur_soon
        cur_prerequisite_cleared = arcade_prerequisite_is_cleared(cur_prerequisite_fn)
        cur_enter = arcade_entry_action(cur_title, cur_prerequisite_fn, cur_action)
        # A MATSUCOM ORIGINAL has no story behind it, so "story cleared" is
        # meaningless for it -- it says so instead, and it is left out of the
        # story-clear census below.
        cur_is_original = arcade_entry_is_original(arcade_items[sel])
        ac_total = sum(1 for entry in arcade_items if entry[6] is not None)
        ac_story = sum(
            1 for entry in arcade_items
            if entry[6] is not None
            and not arcade_entry_is_original(entry)
        )
        ac_cleared = sum(
            1 for entry in arcade_items
            if entry[6] is not None
            and not arcade_entry_is_original(entry)
            and arcade_prerequisite_is_cleared(entry[5])
        )

    use arcade_backdrop(cur_color)

    # Faded handover rather than a hard cut -- see menu_transitions.rpy, sec. 6.
    key "game_menu" action [EnterMMenuMusic(audio.mainmenu), Return()]
    key "K_ESCAPE" action [EnterMMenuMusic(audio.mainmenu), Return()]
    key "K_LEFT" action SetScreenVariable("sel", (sel - 1) % n)
    key "K_RIGHT" action SetScreenVariable("sel", (sel + 1) % n)
    key "K_RETURN" action cur_enter
    key "K_KP_ENTER" action cur_enter
    key "K_p" action Show("mc_gacha")

    # Engraved coin/joystick mark and stamped edition ticket share the opening
    # programme's paper-and-ink treatment while keeping MATSUCOM's own identity.
    add "assets/gui/menu/illustrated/arcade/joystick.svg" xpos 43 ypos 28
    hbox:
        xpos 98 ypos 31
        spacing 18
        add ARCADE_LOGO
        fixed:
            xysize (188, 28)
            yalign 1.0
            yoffset -11
            add IM_TAB_IDLE xysize (188, 28)
            text "CLASSIC EDITION" style "arcade_logo_sub" align (0.5, 0.5)


    vbox:
        xpos 1218 ypos 32
        xanchor 1.0
        spacing 5
        text ("No. %02d / %02d" % (sel + 1, n)):
            style "arcade_pos"
            xalign 1.0
        text ("%d AVAILABLE // %d/%d STORY-CLEARED" % (ac_total, ac_cleared, ac_story)):
            style "arcade_meta"
            xalign 1.0
        # Story-clear meter. Availability is no longer progression-gated.
        fixed:
            xysize (210, 6)
            xalign 1.0
            add Solid("#c3ac7930") xysize (210, 6)
            if ac_cleared:
                add Solid(IM_GOLD) xysize (max(6, int(210.0 * ac_cleared / max(ac_story, 1))), 6)

    # Fine brass rule seats the header above the featured admission ticket.
    add Solid(IM_GOLD) xysize (1156, 1):
        xpos 62
        ypos 98

    # --- featured spread: box art + catalog copy on a soft "page" ---
    fixed:
        xysize (1152, 374)
        xalign 0.5
        ypos 104
        add "assets/gui/menu/illustrated/arcade/feature_mat.svg"

        hbox:
            xpos 32
            yalign 0.5
            spacing 46

            # The featured cartridge: the entire square launches the game.
            fixed:
                xysize (320, 320)
                yalign 0.5
                use arcade_cart(
                    cur_color,
                    cur_playable,
                    320,
                    artwork=cur_art,
                    edge_strength=1.0,
                    click_action=cur_enter,
                    pose_transform=arcade_feature_pop,
                    cart_id="arcade_feature_cover",
                )

            # FIXED-HEIGHT TEMPLATE: the title and blurb each live in a reserved
            # box (title bottom-anchored to sit on the chips, blurb top-anchored
            # under them), so a 1- vs 2-line title or a short vs long description
            # never shifts the chips / blurb / PLAY button. The whole block is a
            # constant height, so browsing keeps every element -- especially the
            # click target -- pinned in place.
            vbox:
                yalign 0.5
                xsize 700
                spacing 10

                hbox:
                    spacing 10
                    text "FEATURED CARTRIDGE" style "arcade_kicker" yalign 0.5
                    add Solid(cur_color + "70") xysize (180, 1) yalign 0.5

                fixed:
                    xysize (700, 92)
                    text cur_title:
                        style "arcade_feature_title"
                        yalign 1.0
                        # Outlines draw in list order, FIRST AT THE BACK (text.py's
                        # figure_outlines appends the letters themselves last):
                        # accent shadow, then the ink edge, then the text.
                        outlines [(3, _arcade_mix(cur_color, "#1d1418", 0.35), 3, 4), (3, "#1d1418", 0, 0)]

                # The two chips carry different content (one has an accent bar
                # beside its text, the other is text alone), so left to size
                # themselves they came out a pixel or two different and sat on
                # slightly different baselines. Both are pinned to one row height
                # and centred in it.
                hbox:
                    spacing 10
                    ysize 30
                    frame:
                        style "arcade_chip"
                        yalign 0.5
                        hbox:
                            spacing 8
                            add Solid(cur_color if cur_playable else IM_MUTED) xysize (4, 15) yalign 0.5
                            text cur_tag:
                                style "arcade_chip_accent"
                                color (_arcade_mix(cur_color, IM_PAPER, 0.30) if cur_playable else IM_MUTED)
                                yalign 0.5
                    frame:
                        style "arcade_chip"
                        yalign 0.5
                        text ("MATSUCOM ORIGINAL" if (cur_playable and cur_is_original) else ("STORY CLEARED" if (cur_playable and cur_prerequisite_cleared) else ("AVAILABLE // CONTENT NOTICE" if cur_playable else "COMING SOON"))):
                            style "arcade_chip_dim"
                            yalign 0.5

                fixed:
                    xysize (700, 78)
                    text cur_blurb:
                        style "arcade_feature_blurb"
                        yalign 0.0

                # --- the PLAY button (mouse), plus the keyboard hint ---
                # A textured admission ticket is cached once; the selected
                # cartridge keeps its accent in the title's genre marker.
                python:
                    _play_ink = IM_INK if cur_playable else IM_MUTED
                    _play_label = "PLAY" if cur_playable else "COMING SOON"

                hbox:
                    spacing 18
                    button:
                        style "arcade_play_button"
                        id "arcade_play"
                        action cur_enter
                        background (IM_TAB_SELECTED if cur_playable else IM_TAB_IDLE)
                        hover_background (ARCADE_PLAY_HOVER if cur_playable else IM_TAB_IDLE)
                        at arcade_play_bob
                        text _play_label:
                            style "arcade_play_text"
                            color _play_ink
                            # "COMING SOON" needs to come down a size to stay on
                            # one line inside the same plate as "PLAY".
                            size (25 if cur_playable else 18)
                            align (0.5, 0.5)

                    if cur_playable:
                        hbox:
                            yalign 0.5
                            spacing 8
                            use arcade_keycap_chip("ENTER")
                            text ("content notice first" if not cur_prerequisite_cleared else "or click the cover") style "arcade_prompt_hint" yalign 0.5
                    else:
                        text "New games incoming." style "arcade_prompt_unavailable" yalign 0.5

    # --- library shelf (every card is one big click target) ---
    hbox:
        xpos 64
        ypos 492
        spacing 12
        text "THE COLLECTION" style "arcade_rail_label" yalign 0.5
        add Solid("#e1bf8066") xysize (140, 1) yalign 0.5

    add "assets/gui/menu/illustrated/arcade/shelf.svg" xpos 64 ypos 508

    # WINDOWED SHELF: six 156px slots, left-aligned on the shelf art, leave its
    # right end for the prize machine to stand on (below). Past six catalog entries the
    # shelf shows a WINDOW centred on the selection instead of every card, and
    # the counts at either end say how much is off-shelf. The window is clamped
    # to the ends, so browsing to the first or last game parks the row rather
    # than scrolling past nothing.
    python:
        _shelf_span = 6
        if n <= _shelf_span:
            _shelf_start = 0
        else:
            _shelf_start = max(0, min(sel - _shelf_span // 2, n - _shelf_span))
        _shelf_end = min(n, _shelf_start + _shelf_span)
        _shelf_left = _shelf_start
        _shelf_right = n - _shelf_end

    if _shelf_left:
        text ("+%d" % _shelf_left):
            style "arcade_rail_label"
            size 15
            xpos 30
            ypos 578
    if _shelf_right:
        text ("+%d" % _shelf_right):
            style "arcade_rail_label"
            size 15
            xpos 1066
            ypos 578

    hbox:
        xpos 64
        ypos 508
        spacing 12
        for index, entry in enumerate(arcade_items[_shelf_start:_shelf_end], _shelf_start):
            $ entry_title, entry_tag, entry_blurb, entry_color, entry_art_path, entry_prerequisite_fn, entry_action = entry
            $ entry_available = (entry_action is not None)
            # Fixed slot: the zoom happens INSIDE it, so growing a card never
            # shoves the rest of the shelf sideways.
            fixed:
                xysize (156, 156)
                # Shelf clicks only change selection. Launching stays deliberate:
                # use the large featured cover, PLAY, or Enter.
                use arcade_cart(
                    entry_color,
                    entry_available,
                    126,
                    artwork=arcade_art_thumb(
                        arcade_art_for(entry_title, entry_art_path)),
                    edge_strength=(1.0 if index == sel else 0.30),
                    click_action=SetScreenVariable("sel", index),
                    pose_transform=arcade_thumb(index == sel),
                    cart_id=("arcade_cartridge_%d" % index),
                    case_trim=True,
                )

    # --- THE PRIZE MACHINE ----------------------------------------------------
    # The actual cabinet, standing on the floor at the end of the shelf, at a
    # size nobody walks past -- and with nothing blinking to say so. It used to
    # be a wallet chip in the header, which read as a readout, not a door. It is
    # the same sprite the prize screen opens on, and its brass plate carries the
    # wallet, which is where a player looks for what a run just paid.
    button:
        style "arcade_machine_button"
        id "arcade_prize_machine"
        # Explicit size: the house button style caps a button's height, and
        # under that cap the cabinet was clamped to a sliver of the corner.
        xysize (160, 266)
        xpos 1152
        ypos 698
        anchor (0.5, 1.0)
        action Show("mc_gacha")

        fixed:
            xysize (160, 266)

            add McMachine(236) xalign 0.5 at arcade_machine_idle

            fixed:
                xysize (150, 26)
                xalign 0.5
                ypos 240
                add IM_TAB_IDLE xysize (150, 26)
                hbox:
                    align (0.5, 0.5)
                    spacing 7
                    add MatsucoinIcon(15) yalign 0.5
                    text mc_num(mc_balance()) style "arcade_prize_amount" yalign 0.5

    # Pointer, keyboard, and controller users all have a visible way home.
    textbutton "Back":
        style "arcade_return_button"
        id "arcade_back"
        xpos 42
        ypos 673
        action [EnterMMenuMusic(audio.mainmenu), Return()]

    # --- footer controls ---
    hbox:
        xalign 0.55
        ypos 684
        spacing 9
        use arcade_keycap_chip("<")
        use arcade_keycap_chip(">")
        text "BROWSE" style "arcade_footer" yalign 0.5
        text "//" style "arcade_footer_sep" yalign 0.5
        use arcade_keycap_chip("ENTER")
        text "OR CLICK FEATURED COVER" style "arcade_footer" yalign 0.5
        text "//" style "arcade_footer_sep" yalign 0.5
        use arcade_keycap_chip("ESC")
        text "BACK" style "arcade_footer" yalign 0.5
        text "//" style "arcade_footer_sep" yalign 0.5
        use arcade_keycap_chip("P")
        text "PRIZES" style "arcade_footer" yalign 0.5


# The prize machine on the floor rises to meet the pointer, as a cartridge does,
# and catches a little light. No idle motion: it is a fixture, not an advert.
# No zoom either: it is pixel art at a whole-number scale (see McMachine).
transform arcade_machine_idle:
    subpixel True
    on idle:
        easein_quad 0.20 yoffset 0 zoom 1.0 matrixcolor BrightnessMatrix(0.0)
    on hover:
        easein_quad 0.22 yoffset -8 zoom 1.0 matrixcolor BrightnessMatrix(0.09)


# --- KOTONOHA VARIANT PICKER -------------------------------------------------
# Kotonoha is the only multi-variant mode. Shown as a modal overlay ON TOP of the
# hub (not a menu-replace), so each button must Hide() itself (in the OUTER menu
# context) BEFORE launching the fight in a new context -- otherwise the panel
# would still be up when the run returns.
screen arcade_koto_variant():
    modal True
    zorder 80

    add Solid("#14212ade")

    frame:
        style "arcade_panel"
        background IM_DARK_PANEL
        xalign 0.5
        yalign 0.5
        xsize 780
        ysize 556
        at arcade_pop

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 6

            null height 2
            text "EMBODIMENT OF VIOLET INK" style "arcade_panel_title" xalign 0.5
            text "How would you like to read it?" style "arcade_panel_sub" xalign 0.5
            null height 14

            button:
                style "arcade_variant_button"
                id "arcade_variant_normal"
                background IM_TAB_IDLE
                hover_background IM_TAB_HOVER
                action [Hide("arcade_koto_variant"), Function(arcade_launch, "arcade_play_koto")]
                vbox:
                    spacing 2
                    yalign 0.5
                    text "NORMAL" style "arcade_variant_head"
                    text "8 bars  //  5 lives  //  records count" style "arcade_variant_sub"
            button:
                style "arcade_variant_button"
                id "arcade_variant_endless"
                background IM_TAB_IDLE
                hover_background IM_TAB_HOVER
                action [Hide("arcade_koto_variant"), Function(arcade_launch, "arcade_play_koto", endless=True)]
                vbox:
                    spacing 2
                    yalign 0.5
                    text "ENDLESS" style "arcade_variant_head"
                    text "random forever  //  survival records" style "arcade_variant_sub"
            button:
                style "arcade_variant_button"
                id "arcade_variant_practice"
                background IM_TAB_IDLE
                hover_background IM_TAB_HOVER
                action [Hide("arcade_koto_variant"), Function(arcade_launch, "arcade_play_koto", practice=True)]
                vbox:
                    spacing 2
                    yalign 0.5
                    text "PRACTICE" style "arcade_variant_head"
                    text "unlimited lives  //  no records" style "arcade_variant_sub"
            button:
                style "arcade_variant_button"
                id "arcade_variant_endless_practice"
                background IM_TAB_IDLE
                hover_background IM_TAB_HOVER
                action [Hide("arcade_koto_variant"), Function(arcade_launch, "arcade_play_koto", practice=True, endless=True)]
                vbox:
                    spacing 2
                    yalign 0.5
                    text "ENDLESS PRACTICE" style "arcade_variant_head"
                    text "random forever  //  unlimited lives  //  no records" style "arcade_variant_sub"

            null height 12
            textbutton _("Back"):
                style "arcade_result_button"
                id "arcade_variant_back"
                background IM_RETURN_IDLE
                hover_background IM_RETURN_HOVER
                xalign 0.5
                action Hide("arcade_koto_variant")

    key "K_ESCAPE" action Hide("arcade_koto_variant")
    key "game_menu" action Hide("arcade_koto_variant")


# --- SHARED RESULTS CARD -----------------------------------------------------
# Called via `call screen arcade_result(...)`; returns "retry" or "leave". Drawn
# over the black the fight teardown leaves behind. `rrows` is a list of
# (label, value) string pairs shown in the stats panel.
screen arcade_result(rtitle, routcome, rrows, raccent="#ffb454"):
    modal True
    zorder 90

    use arcade_backdrop(raccent)
    add Solid("#111d26b8")

    frame:
        style "arcade_panel"
        background IM_DARK_PANEL
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 560
        at arcade_pop

        # Centred so a 2-row card and a 4-row card both sit balanced in the
        # fixed-size panel.
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 12

            null height 2
            text rtitle style "arcade_panel_title" xalign 0.5

            # Outcome badge in the mode's accent.
            frame:
                style "arcade_chip"
                xalign 0.5
                background Solid(raccent)
                text routcome style "arcade_outcome_text"

            add Solid(raccent + "70") xysize (760, 1) xalign 0.5
            null height 6

            # Stat rows: label pinned to the left edge, value pinned to the right,
            # both centred in a fixed-height row.
            #
            # This is a `fixed` with an xanchor'd value rather than an hbox with a
            # greedy `null width 1 xfill True`, because that idiom does not actually
            # right-align anything. Measured in an isolated harness: giving a box an
            # explicit `xsize` stops it packing its children to the left -- it
            # spreads them -- so the values drifted toward the middle by an amount
            # that depended on how long each string was, which is what made this
            # column look crooked ("0" and "ENDLESS" landing at different x). Setting
            # `text_align` on the value does nothing at all here. `fixed` +
            # `xanchor 1.0 xpos 760` lands every value on the same right edge to the
            # pixel, whatever its length.
            vbox:
                xalign 0.5
                xsize 760
                spacing 10
                for _rl, _rv in rrows:
                    fixed:
                        xsize 760
                        ysize 30

                        text _rl style "arcade_row_label" xpos 0 yalign 0.5
                        text _rv style "arcade_row_value" xanchor 1.0 xpos 760 yalign 0.5

            null height 18

            hbox:
                xalign 0.5
                spacing 28
                textbutton _("Retry"):
                    style "arcade_result_button"
                    background IM_TAB_IDLE
                    hover_background IM_TAB_HOVER
                    action Return("retry")
                textbutton _("Leave"):
                    style "arcade_result_button"
                    background IM_RETURN_IDLE
                    hover_background IM_RETURN_HOVER
                    action Return("leave")

    key "K_ESCAPE" action Return("leave")
    key "game_menu" action Return("leave")


# =============================================================================
# LAUNCH LABELS
# Each: flip arcade_active on, preset that mode's flags, drop the hub, and jump
# into the EXISTING preamble-free fight-invocation label. The guarded branch in
# that label routes results to arcade_<mode>_result below.
# =============================================================================

# --- Shared teardown ---------------------------------------------------------
# Every launcher drops the same hub chrome before handing off. Listing the
# hub-owned screens ONCE means adding a sub-screen (arcade_koto_variant was
# exactly this) can't be forgotten in three of the four launchers.
# `blackout` is False for Monika, whose mm_intro owns its own opening.
label arcade_launch_prep(blackout=True):
    hide screen arcade_hub
    hide screen arcade_koto_variant
    hide screen arcade_story_warning
    hide screen archive
    hide screen character_stories
    if blackout:
        stop music fadeout 0.5
        scene black
    return

# --- Matsuda main fight (Normal / Id share one setup path) -------------------
label arcade_play_msbf(id_mode=False):
    $ arcade_active = True
    $ _msbf_id_mode = id_mode
    $ msbf_clear_battle_watch()
    call arcade_launch_prep from _call_arcade_launch_prep
    # Controls notice + party select (both self-contained gameplay screens, not VN).
    call screen msbf_keyboard_notice
    if _return == "cancel_setup":
        jump msbf_cancel_setup
    call screen msbf_party_select
    if _return == "cancel_setup":
        jump msbf_cancel_setup
    $ _msbf_party_ids = _return
    # cs_matsuda_02_battle builds the fight, plays the entrance cinematic (the
    # arcade gets it now -- it is the mode's opening shot, not story), and
    # (guarded) jumps to arcade_msbf_result on finish.
    jump cs_matsuda_02_battle

# --- Kotonoha (four variants -> one launcher) --------------------------------
# practice + endless together is Endless Practice.
label arcade_play_koto(practice=False, endless=False):
    $ arcade_active = True
    $ kt_practice = practice
    $ kt_endless = endless
    $ kt_continue_bar = 0
    $ kt_continues = 0
    $ kt_debug = False
    $ kt_debug_wave = False
    call arcade_launch_prep from _call_arcade_launch_prep_1
    call screen koto_keyboard_notice
    jump kototouhou_fight

# --- Tsubaki -----------------------------------------------------------------
label arcade_play_tsubaki:
    $ arcade_active = True
    $ tsb_run_deaths = 0
    $ tsb_retry = False
    $ tsb_debug = False
    call arcade_launch_prep from _call_arcade_launch_prep_2
    call screen koto_keyboard_notice
    jump tsubamode_fight

# --- Asahina -----------------------------------------------------------------
# The mode owns its stage-styled result card and retry/setup loop. Every
# completed eligible attempt invokes arcade_asahina_rhythm_award there once.
label arcade_play_asahina_rhythm:
    $ arcade_active = True
    call arcade_launch_prep from _call_arcade_launch_prep_asahina_rhythm
    call asahina_rhythm_mode(arcade=True) from _call_arcade_asahina_rhythm_mode
    jump arcade_return

# --- Monika ------------------------------------------------------------------
# Monika's rounds ARE the dialogue-QTE mechanic, so "strip VN" means only the
# intro chatter + ending wrap. Replicate monikamode's quick_menu save (mm_intro
# itself does the rest of the setup and skips its intro lines while arcade_active).
label arcade_play_monika:
    $ arcade_active = True
    $ _mm_prev_quick_menu = quick_menu
    $ quick_menu = False
    call arcade_launch_prep(blackout=False) from _call_arcade_launch_prep_3
    jump mm_intro


# =============================================================================
# RESULT LABELS
# Reached only via the arcade_active guards. Each replicates the challenge-
# achievement grants its story victory label does (so arcade replays still earn
# them), renders the shared results card, then loops on Retry or exits on Leave.
# NB: Tsubaki records its ending + grants here WITHOUT the story's NieR true-reset.
# =============================================================================

label arcade_msbf_result:
    # Records and grants already happened in cs_matsuda_02_battle, above the
    # arcade split -- this label only renders.
    $ _ac_win = (_msbf_result == "victory")
    python:
        # Matsucoins are paid HERE rather than in the fight, so the story path
        # through cs_matsuda_02_battle stays byte-for-byte unchanged -- the same
        # discipline the arcade_active guards follow everywhere else in this file.
        _ac_coins = mc_award_mode(
            "msbf_id" if _msbf_id_mode else "msbf",
            "ONTOLOGICAL SEER: ID" if _msbf_id_mode else "ONTOLOGICAL SEER",
            _ac_win)
        _ac_rows = [
            ("MODE", "ID MODE" if _msbf_id_mode else "NORMAL"),
            ("RESULT", "CLEARED" if _ac_win else "WIPED"),
            ("PARTY MEMBERS DOWNED", str(_msbf_party_downs)),
        ]
        if _ac_coins:
            _ac_rows.append(("MATSUCOINS EARNED", "+%s" % mc_num(_ac_coins)))
    call screen arcade_result("ONTOLOGICAL SEER", ("VICTORY" if _ac_win else "DEFEAT"), _ac_rows, ("#4fbf7a" if _ac_win else "#e0455e"))
    if _return == "retry":
        jump cs_matsuda_02_battle
    jump arcade_return

label arcade_koto_result:
    # Records and grants already happened in kototouhou_fight, above the arcade
    # split -- this label only renders.
    python:
        _ac_win = (_kt_result == "victory")
        _ac_outcome = "VICTORY" if _ac_win else ("ABANDONED" if _kt_result == "quit" else "DEFEAT")
        _ac_rows = [("SCORE", format(kt_last_score, ","))]
        if kt_last_endless and kt_last_practice:
            # Endless Practice can only end by leaving, so leaving is not
            # abandoning it, and it has no record to compare against -- the
            # falls it took are the stat.
            _ac_outcome = "RUN ENDED"
            _ac_rows.append(("MODE", "ENDLESS PRACTICE"))
            _ac_rows.append(("WAVE REACHED", str(kt_last_endless_wave + 1)))
            _ac_rows.append(("FALLS", str(kt_last_deaths)))
        elif kt_last_endless:
            _ac_rows.append(("MODE", "ENDLESS"))
            _ac_rows.append(("WAVES SURVIVED", str(kt_last_endless_wave + 1)))
            _ac_rows.append(("BEST WAVES", str((persistent.kotomode_endless_wave or 0) + 1)))
        else:
            _ac_rows.append(("MODE", "PRACTICE" if kt_last_practice else "NORMAL"))
            _ac_rows.append(("REACHED BAR", "%d / 8" % (kt_last_bar_index + 1)))
            _ac_rows.append(("SPELLS CAPTURED", "%d / 8" % kt_last_captures))
        # PRACTICE (either kind) pays nothing: unlimited lives and no records,
        # so paying it would make it the cheapest possible coin farm and
        # quietly make the other variants pointless.
        _ac_coins = 0 if kt_last_practice else mc_award_mode(
            "koto", "EMBODIMENT OF VIOLET INK", _ac_win)
        if _ac_coins:
            _ac_rows.append(("MATSUCOINS EARNED", "+%s" % mc_num(_ac_coins)))
    call screen arcade_result("EMBODIMENT OF VIOLET INK", _ac_outcome, _ac_rows, ("#4fbf7a" if (_ac_win or _ac_outcome == "RUN ENDED") else "#e0455e"))
    if _return == "retry":
        $ kt_continue_bar = 0
        $ kt_continues = 0
        scene black
        jump kototouhou_fight
    jump arcade_return

label arcade_tsuba_result:
    # The ending was recorded and granted in tsubamode_fight, above the arcade
    # split. This label only renders -- notably WITHOUT the story's NieR
    # "TRUE RESET" flourish (see tsubamode_victory_v/p/b).
    python:
        _tsb_win = _tsb_result in ("victory_v", "victory_p", "victory_b")
        _tsb_ending = {
            "victory_v": "THE LOUD WAY",
            "victory_p": "EVERY STRING CUT",
            "victory_b": "THE CRUEL WAY",
        }.get(_tsb_result, "-")
        _ac_outcome = "SHE FELL" if _tsb_win else ("ABANDONED" if _tsb_result == "quit" else "YOU FELL")
        _ac_coins = mc_award_mode("tsuba", "THE UNWRITTEN ACT", _tsb_win)
        _ac_rows = [
            ("OUTCOME", _tsb_ending if _tsb_win else "NO ENDING REACHED"),
            ("DEATHS THIS RUN", str(tsb_run_deaths)),
        ]
        if _ac_coins:
            _ac_rows.append(("MATSUCOINS EARNED", "+%s" % mc_num(_ac_coins)))
    call screen arcade_result("THE UNWRITTEN ACT", _ac_outcome, _ac_rows, ("#4fbf7a" if _tsb_win else "#e0455e"))
    if _return == "retry":
        $ tsb_run_deaths = 0
        $ tsb_retry = False
        scene black
        jump tsubamode_fight
    jump arcade_return

label arcade_monika_result:
    # date_win + persistent.arcade_monika_cleared are already set in
    # mm_victory (the only win path). Monika has no defeat state -- this is a win card.
    python:
        _ac_coins = mc_award_mode("monika", "A FINE DATE", True)
        _ac_rows = [
            ("OUTCOME", "YOU KEPT YOUR HEAD"),
            ("TIMES SHE SURGED BACK", str(mm_slips)),
            ("RUN", "FLAWLESS" if mm_slips == 0 else "CLEARED"),
        ]
        if _ac_coins:
            _ac_rows.append(("MATSUCOINS EARNED", "+%s" % mc_num(_ac_coins)))
    call screen arcade_result("A FINE DATE", "REJECTED", _ac_rows, "#4fbf7a")
    if _return == "retry":
        $ arcade_active = True
        $ _mm_prev_quick_menu = quick_menu
        $ quick_menu = False
        jump mm_intro
    jump arcade_return


# --- SHARED EXIT -------------------------------------------------------------
# The single way out of any arcade run: clear the guard, restore hub music, and
# return -- which unwinds renpy.call_in_new_context back to the still-shown hub.
label arcade_return:
    $ arcade_active = False
    scene black
    # Through the shared handover, so a mode that never touched the music does
    # not get the hub track restarted from 0:00 underneath it on the way out.
    $ enter_m_menu_music(audio.arcade_theme)
    return


# =============================================================================
# TRANSFORMS + STYLES  ("classic edition" retro palette)
# Palette: deep indigo field (#15112a / #171129), warm off-white text (#f7f0e6),
# amber prompt accent (#ffb454 / #ffd98a), muted lilac body (#c9c0dc / #a99fc4),
# and a per-game accent color carried by each cartridge.
# =============================================================================
# --- cartridge face + hover --------------------------------------------------
# The mesh/shader transform every cartridge face wears. The bare statements are
# the implicit start block (they set the shader up and stick); the on-handlers
# animate u_hover (brighten + flared accent edge) and u_sweep (the glint's
# position across the face). Matsu'Py dispatches hover/idle to any transform living
# INSIDE a button, which is exactly where these sit.
#
# The ATL interpolation requests frames for one complete sweep when hover
# begins. It then rests beyond the card edge while the pointer remains parked.
# Idle restores the original brightness and sweep position; entering the card
# again starts a new sweep. No ambient clock or repeating hover redraw is used.
transform arcade_cart_fx(rad=14.0, acc=(1.0, 1.0, 1.0, 1.0), art=1.0, dim=0.0, edge=0.35):
    mesh True
    shader "enter_m.arcade_cart"
    u_radius rad
    u_accent acc
    u_art art
    u_dim dim
    u_edge edge
    u_hover 0.0
    u_sweep 2.0
    on hover:
        parallel:
            linear 0.18 u_hover 1.0
        parallel:
            u_sweep -0.40
            linear 1.05 u_sweep 1.40
    on idle:
        parallel:
            linear 0.28 u_hover 0.0
        parallel:
            linear 0.28 u_sweep 1.40

# Shelf card: sits centred in its fixed slot and grows in place. The implicit
# start block eases to the selected/unselected pose (so changing selection
# animates); hover lifts and brightens on top of whichever pose it is in.
transform arcade_thumb(is_sel):
    align (0.5, 0.5)
    ease 0.20 zoom (1.16 if is_sel else 0.92) alpha (1.0 if is_sel else 0.68) yoffset (-6 if is_sel else 2)
    on hover:
        easeout_quad 0.16 zoom (1.20 if is_sel else 1.04) alpha 1.0 yoffset (-12 if is_sel else -6)
    on idle:
        easein_quad 0.22 zoom (1.16 if is_sel else 0.92) alpha (1.0 if is_sel else 0.68) yoffset (-6 if is_sel else 2)

# Featured cover: re-pops each time the selection changes (the transform is
# rebuilt, so it starts from the faded pose again and `idle` eases it in), and
# leans toward the player on hover. BOTH handlers restate alpha/zoom/yoffset --
# an event that only mentions some of them would strand the rest mid-flight.
transform arcade_feature_pop:
    align (0.5, 0.5)
    alpha 0.0
    zoom 1.0
    yoffset 18
    on hover:
        easeout_quad 0.16 alpha 1.0 zoom 1.035 yoffset -5
    on idle:
        easein 0.26 alpha 1.0 zoom 1.0 yoffset 0

transform arcade_pop:
    on show:
        alpha 0.0
        zoom 0.94
        easein_back 0.30 alpha 1.0 zoom 1.0
    on hide:
        easeout_quad 0.18 alpha 0.0

# --- header / meta ---

style arcade_logo_sub is gui_text:
    font gui.interface_font
    size 14
    color IM_GOLD
    kerning 1.8
    outlines []

style arcade_machine_button:
    padding (0, 0)
    background None
    hover_background None
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style arcade_prize_amount:
    font gui.interface_font
    size 16
    color IM_GOLD
    bold True
    outlines [(1, "#0a0713", 0, 0)]

style arcade_pos is gui_text:
    font gui.interface_font
    size 24
    color IM_PAPER
    bold True

style arcade_meta is gui_text:
    font gui.interface_font
    size 12
    color IM_MUTED
    kerning 0.8

# --- featured panel ---
style arcade_feature_title:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 40
    color IM_PAPER
    # No faux bold: emboldening an already heavy extended face closed up its
    # counters, and cream on the mauve mat did the rest (user, Sep 11 2026:
    # "hard to read"). The ink outline lifts the letters off the mat; the
    # hub adds a drop shadow in the selected cartridge's own accent.
    bold False
    kerning 1.5
    xmaximum 700
    line_spacing -4
    outlines [(3, "#1d1418", 0, 0)]

style arcade_feature_blurb is gui_text:
    font gui.interface_font
    size 18
    color "#ded6c7"
    xmaximum 700
    line_spacing 4

style arcade_prompt_unavailable is gui_text:
    font gui.interface_font
    size 16
    color IM_MUTED

# --- chips ---
style arcade_chip:
    background IM_TAB_IDLE
    padding (12, 6)

style arcade_chip_accent:
    font gui.interface_font
    size 12
    bold True
    kerning 1.0

style arcade_chip_dim is gui_text:
    font gui.interface_font
    size 12
    color IM_MUTED
    bold True
    kerning 1.0

# --- footer ---
style arcade_footer is gui_text:
    font gui.interface_font
    size 13
    color IM_MUTED
    kerning 1.1

# --- panels (variant picker / result card) ---
# Cached nine-slice artwork preserves the engraved border at every panel size.
style arcade_panel:
    background IM_DARK_PANEL
    padding (34, 26)

style arcade_panel_title:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 34
    color IM_PAPER
    bold True
    outlines []

style arcade_panel_sub is gui_text:
    font gui.interface_font
    size 15
    color IM_MUTED

style arcade_outcome_text:
    font gui.interface_font
    size 20
    color "#0a0713"
    bold True
    kerning 1.0

style arcade_row_label is gui_text:
    font gui.interface_font
    size 16
    color IM_MUTED

style arcade_row_value is gui_text:
    font gui.interface_font
    size 20
    color IM_PAPER
    bold True

# --- buttons ---
style arcade_blank_button:
    background None
    padding (0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style arcade_variant_button:
    xsize 640
    ysize 64
    xalign 0.5
    background IM_TAB_IDLE
    hover_background IM_TAB_HOVER
    padding (22, 10)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style arcade_variant_head:
    font gui.interface_font
    size 20
    color IM_PAPER
    bold True
    kerning 1.0

style arcade_variant_sub is gui_text:
    font gui.interface_font
    size 13
    color IM_MUTED

style arcade_result_button:
    xsize 190
    ysize 54
    background IM_TAB_IDLE
    hover_background IM_TAB_HOVER
    padding (18, 10)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style arcade_result_button_text:
    font gui.interface_font
    size 22
    color IM_PAPER
    hover_color "#ffffff"
    bold True


# =============================================================================
# CATALOG CHROME  (kicker, PLAY button, keycaps, shelf label)
# The plates use the shared cached paper/ink Frames; styles carry type/geometry.
# =============================================================================
transform arcade_play_bob:
    alpha 0.0
    zoom 1.0
    yoffset 10
    on hover:
        easeout_quad 0.12 alpha 1.0 zoom 1.045 yoffset 0
    on idle:
        easein 0.24 alpha 1.0 zoom 1.0 yoffset 0

style arcade_kicker is gui_text:
    font gui.interface_font
    size 12
    color IM_GOLD
    bold True
    kerning 3.0

# --- PLAY ticket ------------------------------------------------------------
style arcade_play_button:
    xsize 236
    ysize 62
    padding (0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style arcade_play_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 25
    bold True
    kerning 2.0
    xalign 0.5
    yalign 0.5
    outlines []

# --- keycap chips (footer legend + the hint beside PLAY) ---
style arcade_keycap:
    background IM_TAB_IDLE
    padding (10, 4)

style arcade_keycap_text is gui_text:
    font gui.interface_font
    size 12
    color IM_PAPER
    bold True
    kerning 1.5

style arcade_prompt_hint is gui_text:
    font gui.interface_font
    size 15
    color IM_MUTED

# --- shelf label ---
style arcade_rail_label is gui_text:
    font gui.interface_font
    size 12
    color IM_GOLD
    bold True
    kerning 4.0

style arcade_footer_sep is gui_text:
    font gui.interface_font
    size 13
    color "#978363"

style arcade_return_button:
    xysize (120, 36)
    padding (10, 3)
    background IM_RETURN_IDLE
    hover_background IM_RETURN_HOVER
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style arcade_return_button_text:
    font gui.interface_font
    size 18
    color IM_PAPER
    hover_color "#ffffff"
    align (0.5, 0.5)
    outlines []
