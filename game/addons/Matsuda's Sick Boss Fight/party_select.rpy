# =============================================================================
# party_select.rpy  --  ONTOLOGICAL SEER :: FORMATION
# =============================================================================
#
# WHAT THIS IS
#   The seven-character party picker for both Seer fights (Normal + Id Mode).
#   Third build. Sep 30 2026 replaced the revolver cylinder (kept in
#   ENTER-M-backups/20260930-seer-facelift-before); Oct 1 2026 rebuilt this
#   screen around how it is USED -- the pre-pass copy is in
#   ENTER-M-backups/20261001-formation-before.
#
# THE LAYOUT (1280x720). Every region owns its rectangle; nothing is drawn
# where something else has to be read.
#
#   +----------------+-----------------------------------------------------+
#   | VS. FORMATION  |  ROSTER -- seven cards, one row                     |
#   |                +-----------------------+-----------------------------+
#   |  THE OFFICIAL  |  DOSSIER              |  REAR       FRONT >>>       |
#   |  DESIGN        |  name, role, stats,   |  THE FORMATION DECK         |
#   |  (one shared   |  affinities, skills   |  the battle sprites, in     |
#   |  scale, heads  |  [ ADD TO PARTY  Z ]  |  their rows, idling         |
#   |  on one line)  +-----------------------+-----------------------------+
#   |                |  PARTY -- four plates, turn order left to right     |
#   | BATTLE ART     |  context help                       [   BEGIN    ]  |
#   +----------------+-----------------------------------------------------+
#
# THREE ROWS, ONE CURSOR
#   Everything you can act on sits in one of three horizontal rows -- ROSTER,
#   PARTY, BEGIN -- so the keys mean the same thing everywhere:
#     LEFT / RIGHT   along the row (hold to scroll the roster)
#     UP / DOWN      change row: BEGIN is at most two presses from anywhere
#     Z / ENTER      roster: add or remove   party: swap row   BEGIN: begin
#     X / SHIFT      remove the browsed fighter, or that party member
#     SPACE          begin, from anywhere, once the party is ready
#     TAB            battle art: pixel / illustrated
#   Picking the fourth fighter moves the cursor onto BEGIN, so Z on four
#   cards and Z once more is a whole formation. (The old screen walked
#   UP/DOWN through every member, so reaching BEGIN took a press per party
#   member plus one.)
#
#   The MOUSE drives the SAME cursor: hovering a card, a plate, a sprite or
#   BEGIN moves it there -- which is also how you inspect a fighter -- click
#   acts and right-click removes. One cursor means one highlight; the pointer
#   and the keys can never each light a different card. The help strip
#   follows whichever you touched last.
#
#   Every handler reads and writes the LIVE screen scope (renpy.get_screen),
#   never a SetScreenVariable built at the last redraw: under key repeat the
#   screen re-executes slower than keys arrive, and a value captured at the
#   last redraw makes the cursor stall then jump (see msbf_kb_step, ui.rpy).
#
# THE OFFICIAL DESIGN IS DRAWN AT ONE SCALE FOR EVERYBODY
#   The seven archetypes were painted at one scale -- eye line to chin
#   measures 57-65 source px on every one of them -- but their canvases are
#   not one shape: Monika's is landscape (1375x1144, mid-leap). Fitting each
#   canvas into the panel drew her at 78% of everyone else and stood her on
#   the floor. Now every source is drawn at MSBF_FM_HERO_K with its head
#   centre on MSBF_FM_HERO_HEAD_Y: faces are one size, the eyes never jump as
#   you browse, and she floats because she is in the air. Her battle sprite
#   had the same fault from the other direction (its PARTY span) and was
#   rebuilt the same day.
#
# STATE (unchanged, so nothing downstream moves)
#   picks / rows, msbf_select_member / msbf_remove_member / msbf_toggle_row /
#   msbf_can_begin / msbf_party_config, and the same Return value.
# =============================================================================

init -10 python:

    def _msbf_fm_register_shaders():
        # ---- THE FORMATION PLATE --------------------------------------------
        # msbf.plate's parallelogram plus what a thing you PRESS needs: an
        # inner glow for the cursor, a sheen band it sweeps across on arrival,
        # a fine diagonal hatch (the Seer's paper), a dashed outline for an
        # empty slot, and a top/bottom fade so a plate can lie on the floor as
        # a lane. Every uniform is set by every caller -- an unset one is a
        # crash, not a default.
        renpy.register_shader("msbf.formation_plate", variables="""
            uniform vec2 u_model_size;
            uniform float u_fp_slant;
            uniform vec4 u_fp_top;
            uniform vec4 u_fp_bottom;
            uniform vec4 u_fp_edge;
            uniform vec4 u_fp_accent;
            uniform float u_fp_glow;
            uniform float u_fp_sheen;
            uniform float u_fp_hatch;
            uniform float u_fp_dash;
            uniform float u_fp_vfade;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 sz = u_model_size;
            vec2 p = v_tex_coord * sz;
            float yt = p.y / max(1.0, sz.y);
            float sl = u_fp_slant;
            float xl = max(sl, 0.0) * (1.0 - yt) + max(-sl, 0.0) * yt;
            float xr = sz.x - (max(-sl, 0.0) * (1.0 - yt) + max(sl, 0.0) * yt);
            float inside = smoothstep(xl - 0.5, xl + 0.5, p.x) * (1.0 - smoothstep(xr - 0.5, xr + 0.5, p.x));
            vec4 col = mix(u_fp_top, u_fp_bottom, yt);

            float hl = abs(fract((p.x + p.y) / 7.0) - 0.5) * 7.0;
            col.rgb += vec3(1.0 - smoothstep(0.35, 1.1, hl)) * u_fp_hatch * 0.05;

            float dl = p.x - xl;
            float dr = xr - p.x;
            float dside = min(dl, dr);
            float dcap = min(p.y, sz.y - p.y);
            float de = max(0.0, min(dside, dcap));

            float g = exp(-de / 5.0) * u_fp_glow;
            col.rgb = mix(col.rgb, u_fp_edge.rgb, clamp(g * 0.55, 0.0, 1.0));
            col.a = max(col.a, g * 0.45 * u_fp_edge.a);

            float edge = 1.0 - smoothstep(0.6, 1.4, de);
            float along = mix(p.x, p.y, step(dside, dcap));
            float dash = step(0.45, fract(along / 9.0));
            edge *= mix(1.0, dash, u_fp_dash);
            col.rgb = mix(col.rgb, u_fp_edge.rgb, edge * u_fp_edge.a);
            col.a = max(col.a, edge * u_fp_edge.a);

            float rail = step(1.5, dl) * (1.0 - smoothstep(4.0, 5.0, dl));
            col.rgb = mix(col.rgb, u_fp_accent.rgb, rail * u_fp_accent.a);
            col.a = max(col.a, rail * u_fp_accent.a);

            float s = (p.x + (sz.y - p.y) * 0.8) / max(1.0, sz.x + sz.y * 0.8);
            float band = 1.0 - smoothstep(0.0, 0.07, abs(s - u_fp_sheen));
            col.rgb += vec3(band * 0.30);
            col.a = max(col.a, band * 0.26);

            float fade = 1.0;
            if (u_fp_vfade > 0.0) {
                fade = smoothstep(0.0, u_fp_vfade, yt) * smoothstep(0.0, u_fp_vfade, 1.0 - yt);
            }
            float a = clamp(col.a, 0.0, 1.0) * inside * fade;
            gl_FragColor = vec4(min(col.rgb, vec3(1.0)) * a, a);
        """)

        # ---- THE FLOOR RING ---------------------------------------------------
        # Etrian Odyssey's position marker: an ellipse ring (and a fainter inner
        # one) lying on the deck under a party member, with an optional
        # expanding pulse for the member under the cursor. Line widths are
        # measured in SCREEN px through the ellipse's own gradient, so a ring
        # squashed to the floor angle keeps a one-and-a-half pixel line all the
        # way round instead of going fat at the ends.
        renpy.register_shader("msbf.formation_ring", variables="""
            uniform vec2 u_model_size;
            uniform vec4 u_fr_color;
            uniform float u_fr_fill;
            uniform float u_fr_pulse;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 q = v_tex_coord * 2.0 - 1.0;
            float r = max(length(q), 0.0001);
            vec2 gq = vec2(q.x * 2.0 / max(1.0, u_model_size.x), q.y * 2.0 / max(1.0, u_model_size.y)) / r;
            float g = max(length(gq), 0.0001);
            float ring = 1.0 - smoothstep(0.5, 1.6, abs(r - 0.88) / g);
            float inner = (1.0 - smoothstep(0.4, 1.3, abs(r - 0.62) / g)) * 0.45;
            float wr = 0.50 + 0.50 * u_fr_pulse;
            float wave = (1.0 - smoothstep(0.5, 3.0, abs(r - wr) / g)) * (1.0 - u_fr_pulse);
            float fill = (1.0 - smoothstep(0.15, 0.95, r)) * u_fr_fill;
            float a = clamp(ring + inner + wave * 0.8 + fill * 0.55, 0.0, 1.0) * u_fr_color.a * (1.0 - step(1.0, r));
            gl_FragColor = vec4(u_fr_color.rgb * a, a);
        """)

    try:
        _msbf_fm_register_shaders()
    except Exception as _msbf_fm_e:
        if config.developer:
            renpy.log("MSBF FORMATION: shader registration failed: %r" % (_msbf_fm_e,))


init -2 python:

    MSBF_FM_TAG = "msbf_party_select"

    # --- LAYOUT (screen px) ----------------------------------------------------
    MSBF_FM_CARD = (448, 22, 110, 84, 9)      # roster: x0, y, w, h, gap
    MSBF_FM_PLATE = (448, 586, 200, 54, 8)    # party:  x0, y, w, h, gap
    MSBF_FM_BEGIN = (1022, 650, 250, 56)      # x, y, w, h
    MSBF_FM_PANEL = (440, 114, 332, 442)      # the dossier
    # Where the formation may stand. Each formation is CENTRED in this box,
    # not placed at a fixed offset: a four-deep column is 436 px tall and a
    # one-front-three-rear spread is 494 px wide, and no single offset fits
    # both inside the deck without one of them running under the dossier or
    # the party strip. Re-centring slides (msbf_fm_slide), so a row swap reads
    # as the formation re-forming.
    MSBF_FM_DECK_BOX = (778, 140, 1272, 582)
    MSBF_FM_LANE_W = 146

    MSBF_FM_FRONT = "#ffcf66"     # the front row's colour, everywhere
    MSBF_FM_REAR = "#86a9cc"      # the rear row's
    MSBF_FM_CYAN = "#55ddff"      # the cursor's
    MSBF_FM_INK_TOP = (0.03, 0.05, 0.09, 0.90)
    MSBF_FM_INK_BOTTOM = (0.01, 0.02, 0.04, 0.94)
    MSBF_FM_IDLE_EDGE = (0.50, 0.62, 0.78, 0.30)
    MSBF_FM_CLEAR = (0.0, 0.0, 0.0, 0.0)

    # Keycap arrows are the pixel cursor turned (no font here has an arrow
    # glyph -- see the glyph-coverage note in memory): rotate is clockwise.
    MSBF_FM_KEY_ARROWS = {"lr": (90, 270), "ud": (180, 0), "u": (180,), "d": (0,)}

    # --- THE OFFICIAL DESIGN ---------------------------------------------------
    MSBF_FM_HERO_K = 0.42           # screen px per source px, for everybody
    MSBF_FM_HERO_HEAD_Y = 140       # every head centre lands on this line
    MSBF_FM_HERO_CX = 224           # the panel's centre line
    MSBF_FM_HERO_LEFT = -30         # how far a wide figure may run off the left
    # Opaque bounding box of each archetype (alpha > 24), source px. Wide art
    # centres on its BOX, not its canvas, so Seeker's sword and Monika's spell
    # circle do not push the figure off the panel.
    MSBF_FM_ART_BOX = {
        "seeker": (28, 27, 1031, 1454), "monika": (46, 8, 1348, 1126),
        "kotonoha": (56, 128, 984, 1426), "asahina": (4, 5, 1016, 1530),
        "sam": (47, 4, 1017, 1520), "tsubaki": (51, 142, 979, 1370),
        "himeko": (37, 30, 996, 1516),
    }

    def msbf_fm_hero_place(member_id):
        """-> (left, top, width, height) of the archetype on screen."""
        W, H = MSBF_ARCH_SIZES.get(member_id, (1024, 1536))
        hx, hy, _scale = MSBF_ROSTER_HEADS.get(member_id, (0.5, 0.15, 3.0))
        x0, y0, x1, y1 = MSBF_FM_ART_BOX.get(member_id, (0, 0, W, H))
        k = MSBF_FM_HERO_K
        cx = max(MSBF_FM_HERO_CX, MSBF_FM_HERO_LEFT + (x1 - x0) * k * 0.5)
        left = cx - (x0 + x1) * 0.5 * k
        top = MSBF_FM_HERO_HEAD_Y - hy * H * k
        return (int(round(left)), int(round(top)), int(round(W * k)), int(round(H * k)))

    def msbf_fm_face(member_id, w, h, span=220, drop=0.10):
        """A head shot at ONE source scale for everybody: `span` source px
        tall, framed a touch below the measured head centre. (The sources
        share a scale; their canvases do not -- a cover-fit crop of Monika's
        landscape canvas is a different zoom from everyone else's.)"""
        img = MSBF_SIL_SPRITE.get(member_id)
        if not img:
            return Null(int(w), int(h))
        W, H = MSBF_ARCH_SIZES.get(member_id, (1024, 1536))
        hx, hy, _scale = MSBF_ROSTER_HEADS.get(member_id, (0.5, 0.15, 3.0))
        sh = float(span)
        sw = sh * float(w) / float(h)
        x0 = min(max(0.0, hx * W - sw * 0.5), W - sw)
        y0 = min(max(0.0, hy * H + sh * drop - sh * 0.5), H - sh)
        return Transform(img, crop=(int(x0), int(y0), int(sw), int(sh)), xysize=(int(w), int(h)))

    def _msbf_fm_plate_static(slant, top, bottom, edge, accent, hatch, dash, glow):
        return Transform(Solid("#00000000"), mesh=True, shader="msbf.formation_plate",
            u_fp_slant=float(slant), u_fp_top=top, u_fp_bottom=bottom,
            u_fp_edge=edge, u_fp_accent=accent, u_fp_glow=float(glow),
            u_fp_sheen=-1.0, u_fp_hatch=float(hatch), u_fp_dash=float(dash), u_fp_vfade=0.0)

    def msbf_fm_plate_static(slant=8.0, top=MSBF_FM_INK_TOP, bottom=MSBF_FM_INK_BOTTOM,
            edge=MSBF_FM_IDLE_EDGE, accent=MSBF_FM_CLEAR, hatch=0.0, dash=0.0, glow=0.0):
        """A formation plate that never animates -- for frame and button
        backgrounds, which are drawn at whatever size the frame is. One object
        per look, so the button or frame it backs can be reused (msbf_memo)."""
        return msbf_memo(_msbf_fm_plate_static, float(slant), _pl_rgba(top), _pl_rgba(bottom),
            _pl_rgba(edge), _pl_rgba(accent), float(hatch), float(dash), float(glow))

    def msbf_fm_window(child, w, h, slant):
        """`child` seen through a slanted window the shape of the plates."""
        mask = msbf_fm_plate_static(slant, (1.0, 1.0, 1.0, 1.0), (1.0, 1.0, 1.0, 1.0), MSBF_FM_CLEAR)
        return AlphaMask(child, Transform(mask, xysize=(int(w), int(h))))

    def msbf_fm_headshot(member_id, w, h, slant, span):
        """A fighter's head shot in a slanted window (use through msbf_memo)."""
        return msbf_fm_window(msbf_fm_face(member_id, w, h, span), w, h, slant)

    def msbf_fm_arrow(angle):
        """The pixel cursor turned into a keycap arrow (use through msbf_memo)."""
        return Transform(MSBF_HUD_UI + "cursor_down.png", rotate=angle, rotate_pad=False, nearest=True)

    # --- BUILT ONCE, REUSED ------------------------------------------------------
    # Every argument change on an ATL transform rebuilds it, and a rebuild here
    # costs several full property scans (see msbf_t, seer_battle.rpy). These
    # pieces change WHEN the cursor moves but do not need to animate between
    # states, so each state is a ready-made displayable instead: a revisit
    # hands back the same object and nothing is rebuilt. Each is wrapped in a
    # Fixed carrying its own position, so the screen adds it with no
    # properties (properties would wrap it in a Transform that is rebuilt
    # whenever the object changes).

    # Card portrait looks: (saturation, brightness) by card state.
    MSBF_FM_PORTRAIT_LOOK = {
        "hot": (1.0, 0.04), "browsed": (0.95, 0.0), "in": (0.90, 0.0),
        "lock": (0.0, -0.30), "idle": (0.35, -0.12),
    }

    def msbf_fm_card_portrait(member_id, look):
        """A roster card's head shot in one state (use through msbf_memo)."""
        sat, bri = MSBF_FM_PORTRAIT_LOOK.get(look, (1.0, 0.0))
        shot = Transform(msbf_memo(msbf_fm_headshot, member_id, 94, 50, 4.8, 220),
            matrixcolor=SaturationMatrix(sat) * BrightnessMatrix(bri))
        return Fixed(shot, xpos=9, ypos=5, xysize=(94, 50))

    def msbf_fm_card_state(hot, browsed, in_party, locked):
        if hot:
            return "hot"
        if browsed:
            return "browsed"
        if in_party:
            return "in"
        return "lock" if locked else "idle"

    def msbf_fm_hero(member_id, role):
        """The official design, placed and sized (use through msbf_memo).
        `role` keeps the art and its afterimage two separate objects."""
        img = MSBF_SIL_SPRITE.get(member_id)
        if not img:
            return Null()
        x, y, w, h = msbf_fm_hero_place(member_id)
        return Fixed(Transform(img, xysize=(w, h)), xpos=x, ypos=y, xysize=(w, h))

    def msbf_fm_bar(value, max_value, fill_color, w=138, h=5):
        """A dossier stat bar: msbf.bar's look, drawn static (use through
        msbf_memo) -- the fight's msbf_energy_bar is an ATL transform."""
        frac = max(0.0, min(1.0, float(value) / float(max_value))) if max_value else 0.0
        lo, hi, track = msbf_bar_palette_from_fill(fill_color, "#152333")
        bar = Transform(Solid(fill_color), xysize=(w, h), mesh=True, shader="msbf.bar",
            u_fill=frac, u_col_lo=lo, u_col_hi=hi, u_track=track, u_glow=(1.05 if frac > 0.0 else 0.0), u_pulse=0.0)
        return Fixed(bar, ypos=17, xysize=(w, h))

    def msbf_fm_row_color(row):
        return MSBF_FM_FRONT if row == "front" else MSBF_FM_REAR

    def msbf_fm_card_look(hot, browsed, in_party, locked, accent):
        """Roster card plate -> (edge, glow, rail, hatch). The portrait's look
        for the same states is MSBF_FM_PORTRAIT_LOOK."""
        if hot:
            return (_pl_rgba(accent, 0.95), 0.75, _pl_rgba(accent, 1.0), 0.4)
        if browsed:
            return (_pl_rgba(accent, 0.65), 0.0, _pl_rgba(accent, 0.90), 0.4)
        if in_party:
            return (_pl_rgba(MSBF_FM_FRONT, 0.55), 0.0, _pl_rgba(accent, 0.85), 0.4)
        if locked:
            return ((0.40, 0.46, 0.56, 0.18), 0.0, _pl_rgba(accent, 0.20), 1.0)
        return (MSBF_FM_IDLE_EDGE, 0.0, _pl_rgba(accent, 0.40), 0.4)

    def msbf_fm_begin_look(ready, hot):
        """BEGIN -> (top, bottom, edge, accent rail)."""
        if ready:
            return ((0.09, 0.36, 0.56, 0.96), (0.03, 0.12, 0.24, 0.96),
                    (0.62, 0.95, 1.0, 0.95), _pl_rgba(MSBF_FM_FRONT, 1.0))
        return ((0.03, 0.05, 0.09, 0.82), (0.01, 0.02, 0.05, 0.88),
                _pl_rgba(MSBF_FM_CYAN, 0.70) if hot else (0.45, 0.55, 0.70, 0.30),
                (0.40, 0.48, 0.60, 0.35))

    def msbf_fm_need_text(picks, rows):
        n = len(picks)
        if n == 0:
            return "PICK FOUR FIGHTERS"
        if n < 4:
            return "PICK %d MORE" % (4 - n)
        if msbf_front_count(picks, rows) < 1:
            return "ONE MUST STAND FRONT"
        return ""

    def msbf_fm_skills(member_id):
        entry = MSBF_ROSTER_BY_ID.get(member_id, {})
        out = []
        for sid in entry.get("skills", []):
            sk = MSBF_SKILLS.get(sid)
            if sk is not None:
                out.append((sk.name, sk.element, sk.cost))
        return out

    def msbf_fm_hints(zone, mouse, in_party, full, ready, n):
        """The help strip: what each key -- or the mouse -- does RIGHT NOW."""
        if mouse:
            if zone == "party":
                return [("CLICK", "SWAP ROW"), ("RIGHT-CLICK", "REMOVE")]
            if zone == "begin":
                return [("CLICK", "BEGIN" if ready else "NOT READY YET")]
            return [("CLICK", "REMOVE" if in_party else ("PARTY FULL" if full else "ADD TO PARTY")),
                    ("RIGHT-CLICK", "REMOVE"), ("HOVER", "INSPECT")]
        if zone == "party":
            return [("lr", "MEMBER"), ("Z", "SWAP ROW"), ("X", "REMOVE"), ("ud", "ROSTER / BEGIN")]
        if zone == "begin":
            return [("Z", "BEGIN" if ready else "NOT READY YET"), ("u", "PARTY" if n else "ROSTER"), ("lr", "ROSTER")]
        rv = [("lr", "BROWSE"), ("Z", "REMOVE" if in_party else ("PARTY FULL" if full else "ADD"))]
        if n:
            rv.append(("d", "PARTY"))
        rv.append(("SPACE", "BEGIN") if ready else ("ESC", "MENU"))
        return rv

    # --- THE DECK ----------------------------------------------------------------
    # Formation px are the battle's own (msbf_px_formation); the deck draws
    # them shifted by msbf_fm_deck_offset.
    def _msbf_fm_reach(member_id, foot):
        """The box a member's sprite covers when standing on `foot`."""
        meta = msbf_px_party_meta(member_id)
        fx, fy = foot
        if not meta:
            return (fx - 60, fy - 200, fx + 60, fy + 8)
        sc = meta["scale"]
        mfx, mfy = meta["foot"]
        bx0, by0, bx1, by1 = meta["bbox"]
        return (fx - (mfx - bx0) * sc, fy - (mfy - by0) * sc, fx + (bx1 - mfx) * sc, fy + 8)

    def msbf_fm_ghost_rows():
        return ["front", "front", "rear", "rear"]

    def msbf_fm_deck_offset(picks, rows):
        """The (dx, dy) that centres THIS formation in the deck box, snapped
        to the 2 px art grid so the pixel sprites stay crisp. Both lanes
        count even when one is empty: centring on the members alone pushed
        an empty REAR lane under the dossier and an empty FRONT label off
        the right edge."""
        if picks:
            rl = [rows.get(m, "front") for m in picks]
            form = msbf_px_formation(rl)
            boxes = [_msbf_fm_reach(m, f) for m, f in zip(picks, form)]
        else:
            rl = msbf_fm_ghost_rows()
            form = msbf_px_formation(rl)
            boxes = [(fx - 60, fy - 40, fx + 60, fy + 20) for fx, fy in form]
        boxes += [(x, y, x + w, y + h) for x, y, w, h, _s, _r, _lit in msbf_fm_lanes(rl, form)]
        L = min(b[0] for b in boxes)
        T = min(b[1] for b in boxes)
        R = max(b[2] for b in boxes)
        B = max(b[3] for b in boxes)
        x0, y0, x1, y1 = MSBF_FM_DECK_BOX
        dx = (x0 + x1) * 0.5 - (L + R) * 0.5
        dy = (y0 + y1) * 0.5 - (T + B) * 0.5
        return (int(round(dx / 2.0)) * 2, int(round(dy / 2.0)) * 2)

    def msbf_fm_lanes(rl, form):
        """The two floor lanes under the columns, leaning with the deck:
        [(x, y, w, h, slant, row, occupied)] in formation px."""
        out = []
        for row, base, ydrop in (("rear", MSBF_PX_COL_REAR, 22), ("front", MSBF_PX_COL_FRONT, 0)):
            ys = [f[1] for f, r in zip(form, rl) if r == row]
            if ys:
                y0, y1 = min(ys) - 44, max(ys) + 30
            else:
                y0, y1 = MSBF_PX_COL_MID + ydrop - 70, MSBF_PX_COL_MID + ydrop + 50
            xt = base + (y0 - MSBF_PX_COL_MID) * MSBF_PX_COL_LEAN
            xb = base + (y1 - MSBF_PX_COL_MID) * MSBF_PX_COL_LEAN
            slant = xt - xb
            out.append((int(xb - MSBF_FM_LANE_W * 0.5), int(y0), int(MSBF_FM_LANE_W + slant),
                        int(y1 - y0), float(slant), row, bool(ys)))
        return out

    def msbf_fm_point(member_id, foot, key="chest"):
        meta = msbf_px_party_meta(member_id)
        fx, fy = foot
        if not meta:
            return (int(fx), int(fy - 90))
        sc = meta["scale"]
        mfx, mfy = meta["foot"]
        x, y = meta.get(key, meta["chest"])
        return (int(fx + (x - mfx) * sc), int(fy + (y - mfy) * sc))

    def msbf_fm_member_box(member_id, foot):
        """Click target for a sprite on the deck: head to feet, torso wide."""
        hx, hy = msbf_fm_point(member_id, foot, "head")
        fx, fy = foot
        return (int(fx - 42), int(hy - 18), 84, int(fy - hy + 26))

    def msbf_fm_depth_order(form):
        """Back to front -- the nearer member is added last, so it is on top
        for clicks exactly as it is on top in the picture."""
        return sorted(range(len(form)), key=lambda k: form[k][1])

    # --- INPUT -------------------------------------------------------------------
    # Screen actions only; a screen BODY must never call these (prediction runs
    # every branch of a screen, and would mutate the cursor while predicting).
    def _msbf_fm_scope():
        sd = renpy.get_screen(MSBF_FM_TAG)
        return sd.scope if sd is not None else None

    def _msbf_fm_sfx(name):
        path = MSBF_UI_SFX.get(name) or MSBF_SFX.get(name)
        if path:
            msbf_play_pooled_sfx(path)

    def _msbf_fm_index(member_id):
        try:
            return MSBF_ALL_MEMBER_IDS.index(member_id)
        except ValueError:
            return 0

    def _msbf_fm_live(sc):
        return list(sc.get("picks") or []), dict(sc.get("rows") or {})

    def _msbf_fm_commit(sc, picks, rows):
        sc["picks"] = picks
        sc["rows"] = rows
        if picks:
            sc["pidx"] = max(0, min(int(sc.get("pidx", 0) or 0), len(picks) - 1))
        else:
            sc["pidx"] = 0
            if sc.get("zone") == "party":
                sc["zone"] = "roster"

    def _msbf_fm_deny(sc, what):
        sc["deny"] = int(sc.get("deny", 0) or 0) + 1
        sc["deny_what"] = what
        _msbf_fm_sfx("denied")

    def _msbf_fm_toggle(sc, member_id):
        picks, rows = _msbf_fm_live(sc)
        if member_id in picks:
            picks, rows = msbf_remove_member(picks, rows, member_id)
            _msbf_fm_sfx("denied")
        elif len(picks) >= 4:
            _msbf_fm_deny(sc, "full")
            return
        else:
            picks, rows = msbf_select_member(picks, rows, member_id)
            _msbf_fm_sfx("accept")
            if msbf_can_begin(picks, rows):
                # The party is ready: the next confirm starts the fight.
                sc["zone"] = "begin"
        _msbf_fm_commit(sc, picks, rows)

    def _msbf_fm_swap(sc, member_id):
        picks, rows = _msbf_fm_live(sc)
        _msbf_fm_commit(sc, picks, msbf_toggle_row(picks, rows, member_id))
        _msbf_fm_sfx("accept")

    def _msbf_fm_unpick(sc, member_id):
        picks, rows = _msbf_fm_live(sc)
        if member_id not in picks:
            return
        picks, rows = msbf_remove_member(picks, rows, member_id)
        _msbf_fm_commit(sc, picks, rows)
        if sc.get("zone") == "party" and picks:
            sc["sel"] = _msbf_fm_index(picks[sc["pidx"]])
        _msbf_fm_sfx("denied")

    def msbf_fm_move(dx, dy):
        sc = _msbf_fm_scope()
        if sc is None or sc.get("launch"):
            return
        sc["mouse"] = False
        picks, rows = _msbf_fm_live(sc)
        n = len(MSBF_ROSTER)
        zone = sc.get("zone", "roster")
        if zone == "party" and not picks:
            zone = "roster"
        before = (zone, sc.get("sel", 0), sc.get("pidx", 0))
        if dy:
            order = ["roster"] + (["party"] if picks else []) + ["begin"]
            j = order.index(zone) if zone in order else 0
            zone = order[max(0, min(len(order) - 1, j + (1 if dy > 0 else -1)))]
            if zone == "party":
                # Land on the fighter being inspected if they are in the party.
                sel_id = MSBF_ROSTER[int(sc.get("sel", 0) or 0) % n]["id"]
                p = picks.index(sel_id) if sel_id in picks else max(0, min(int(sc.get("pidx", 0) or 0), len(picks) - 1))
                sc["pidx"] = p
                sc["sel"] = _msbf_fm_index(picks[p])
        elif dx:
            if zone == "party":
                p = (int(sc.get("pidx", 0) or 0) + dx) % len(picks)
                sc["pidx"] = p
                sc["sel"] = _msbf_fm_index(picks[p])
            else:
                # Sideways off BEGIN goes back to browsing: the fourth pick
                # lands the cursor on BEGIN, and RIGHT should still mean "next".
                zone = "roster"
                sc["sel"] = (int(sc.get("sel", 0) or 0) + dx) % n
        sc["zone"] = zone
        if (zone, sc.get("sel", 0), sc.get("pidx", 0)) != before:
            _msbf_fm_sfx("hover")
        renpy.restart_interaction()

    def msbf_fm_begin():
        sc = _msbf_fm_scope()
        if sc is None or sc.get("launch"):
            return None
        picks, rows = _msbf_fm_live(sc)
        if not msbf_can_begin(picks, rows):
            _msbf_fm_deny(sc, "begin")
            renpy.restart_interaction()
            return None
        # The screen's own timer returns the party once the launch flash has
        # run (see the end of msbf_party_select).
        sc["zone"] = "begin"
        sc["launch"] = True
        _msbf_fm_sfx("turn_ready")
        renpy.restart_interaction()
        return None

    def msbf_fm_confirm():
        sc = _msbf_fm_scope()
        if sc is None or sc.get("launch"):
            return None
        sc["mouse"] = False
        picks, rows = _msbf_fm_live(sc)
        zone = sc.get("zone", "roster")
        if zone == "begin":
            return msbf_fm_begin()
        if zone == "party" and picks:
            _msbf_fm_swap(sc, picks[max(0, min(int(sc.get("pidx", 0) or 0), len(picks) - 1))])
        else:
            _msbf_fm_toggle(sc, MSBF_ROSTER[int(sc.get("sel", 0) or 0) % len(MSBF_ROSTER)]["id"])
        renpy.restart_interaction()
        return None

    def msbf_fm_back():
        sc = _msbf_fm_scope()
        if sc is None or sc.get("launch"):
            return
        sc["mouse"] = False
        picks, rows = _msbf_fm_live(sc)
        zone = sc.get("zone", "roster")
        if zone == "party" and picks:
            _msbf_fm_unpick(sc, picks[max(0, min(int(sc.get("pidx", 0) or 0), len(picks) - 1))])
        elif zone == "begin":
            sc["zone"] = "party" if picks else "roster"
            _msbf_fm_sfx("hover")
        else:
            _msbf_fm_unpick(sc, MSBF_ROSTER[int(sc.get("sel", 0) or 0) % len(MSBF_ROSTER)]["id"])
        renpy.restart_interaction()

    def msbf_fm_hover(zone, i=0):
        """The pointer moved onto something: the cursor follows it."""
        sc = _msbf_fm_scope()
        if sc is None or sc.get("launch"):
            return None
        picks, rows = _msbf_fm_live(sc)
        changed = not sc.get("mouse")
        sc["mouse"] = True
        if zone == "roster":
            changed = changed or sc.get("zone") != "roster" or sc.get("sel") != i
            sc["zone"] = "roster"
            sc["sel"] = i
        elif zone == "party" and 0 <= i < len(picks):
            changed = changed or sc.get("zone") != "party" or sc.get("pidx") != i
            sc["zone"] = "party"
            sc["pidx"] = i
            sc["sel"] = _msbf_fm_index(picks[i])
        elif zone == "begin":
            changed = changed or sc.get("zone") != "begin"
            sc["zone"] = "begin"
        if changed:
            renpy.restart_interaction()
        return None

    def msbf_fm_click_card(i):
        sc = _msbf_fm_scope()
        if sc is None or sc.get("launch"):
            return
        sc["zone"] = "roster"
        sc["sel"] = i
        _msbf_fm_toggle(sc, MSBF_ROSTER[i]["id"])
        renpy.restart_interaction()

    def msbf_fm_unpick_card(i):
        sc = _msbf_fm_scope()
        if sc is None or sc.get("launch"):
            return
        sc["zone"] = "roster"
        sc["sel"] = i
        _msbf_fm_unpick(sc, MSBF_ROSTER[i]["id"])
        renpy.restart_interaction()

    def msbf_fm_click_member(i):
        sc = _msbf_fm_scope()
        if sc is None or sc.get("launch"):
            return
        picks, rows = _msbf_fm_live(sc)
        if 0 <= i < len(picks):
            sc["zone"] = "party"
            sc["pidx"] = i
            sc["sel"] = _msbf_fm_index(picks[i])
            _msbf_fm_swap(sc, picks[i])
        renpy.restart_interaction()

    def msbf_fm_unpick_member(i):
        sc = _msbf_fm_scope()
        if sc is None or sc.get("launch"):
            return
        picks, rows = _msbf_fm_live(sc)
        if 0 <= i < len(picks):
            sc["zone"] = "party"
            sc["pidx"] = i
            _msbf_fm_unpick(sc, picks[i])
        renpy.restart_interaction()

    def msbf_fm_set_art(style):
        if style not in MSBF_SEER_ART_STYLES:
            return
        persistent.msbf_seer_art = style
        _msbf_fm_sfx("hover")
        renpy.restart_interaction()

    def msbf_fm_toggle_art():
        sc = _msbf_fm_scope()
        if sc is not None and sc.get("launch"):
            return
        msbf_fm_set_art("pixel" if msbf_seer_art_hq() else "hq")


# -----------------------------------------------------------------------------
# TRANSFORMS
# -----------------------------------------------------------------------------

# One animated plate. Colours ease (so a card lighting up is a fade, not a
# pop) and the sheen runs once whenever `sheen` turns on -- any change of
# arguments restarts the block, which is also what makes a card that changes
# state while under the cursor flash once more.
transform msbf_fm_plate_t(slant=8.0, top=(0.0, 0.0, 0.0, 0.0), bottom=(0.0, 0.0, 0.0, 0.0), edge=(0.0, 0.0, 0.0, 0.0), accent=(0.0, 0.0, 0.0, 0.0), glow=0.0, hatch=0.0, dash=0.0, vfade=0.0, sheen=False):
    mesh True
    shader "msbf.formation_plate"
    u_fp_slant slant
    u_fp_hatch hatch
    u_fp_dash dash
    u_fp_vfade vfade
    u_fp_sheen -0.5
    parallel:
        ease 0.16 u_fp_top top u_fp_bottom bottom u_fp_edge edge u_fp_accent accent u_fp_glow glow
    parallel:
        pause 0.04
        linear (0.5 if sheen else 0.01) u_fp_sheen (1.5 if sheen else -0.5)

# BEGIN: breathes and glints on a loop once the party is ready.
transform msbf_fm_begin_t(ready=False, hot=False):
    mesh True
    shader "msbf.formation_plate"
    u_fp_slant 14.0
    u_fp_hatch (0.6 if ready else 0.3)
    u_fp_dash 0.0
    u_fp_vfade 0.0
    u_fp_sheen -0.5
    u_fp_glow 0.0
    parallel:
        ease 0.2 u_fp_top msbf_fm_begin_look(ready, hot)[0] u_fp_bottom msbf_fm_begin_look(ready, hot)[1] u_fp_edge msbf_fm_begin_look(ready, hot)[2] u_fp_accent msbf_fm_begin_look(ready, hot)[3]
    parallel:
        block:
            ease 0.9 u_fp_glow (0.95 if ready else (0.55 if hot else 0.0))
            ease 0.9 u_fp_glow (0.35 if ready else (0.55 if hot else 0.0))
            repeat
    parallel:
        block:
            pause 0.15
            linear (0.6 if ready else 0.01) u_fp_sheen (1.5 if ready else -0.5)
            pause (1.8 if ready else 9999.0)
            u_fp_sheen -0.5
            repeat

# A plate's sheen on mouse hover, for the buttons outside the cursor's three
# rows (the dossier's button). The button passes hover/idle down to it.
transform msbf_fm_hover_sheen(slant=10.0):
    mesh True
    shader "msbf.formation_plate"
    u_fp_slant slant
    u_fp_top (0.0, 0.0, 0.0, 0.0)
    u_fp_bottom (0.0, 0.0, 0.0, 0.0)
    u_fp_edge (0.0, 0.0, 0.0, 0.0)
    u_fp_accent (0.0, 0.0, 0.0, 0.0)
    u_fp_glow 0.0
    u_fp_hatch 0.0
    u_fp_dash 0.0
    u_fp_vfade 0.0
    u_fp_sheen -0.5
    on hover:
        u_fp_sheen -0.5
        linear 0.45 u_fp_sheen 1.5
    on idle, insensitive:
        u_fp_sheen -0.5

transform msbf_fm_ring_t(color=(1.0, 1.0, 1.0, 1.0), fill=0.0, pulse=False):
    mesh True
    shader "msbf.formation_ring"
    u_fr_pulse 1.0
    parallel:
        ease 0.18 u_fr_color color u_fr_fill fill
    parallel:
        block:
            u_fr_pulse 0.0
            linear (1.2 if pulse else 0.01) u_fr_pulse 1.0
            pause (0.3 if pulse else 9999.0)
            repeat

# The lift animates a fixed INSIDE each button, never the button: a moving
# hit box slides out from under a pointer resting near its edge and flickers
# (the choice-plate hover-drift bug).
transform msbf_fm_lift(on=False, dy=-6):
    ease 0.14 yoffset (dy if on else 0)

transform msbf_fm_slide(dx=0, dy=0):
    ease 0.26 xoffset dx yoffset dy

transform msbf_fm_tint(color="#ffffff", a=1.0):
    ease 0.35 matrixcolor TintMatrix(color) * SaturationMatrix(0.0) alpha a

transform msbf_fm_spin(period=60.0, turn=360.0):
    rotate 0.0
    linear period rotate turn
    repeat

# Tokens are READ so a new fighter always replays the entrance.
transform msbf_fm_hero_in(token=0):
    alpha 0.0
    xoffset (-46 if token % 2 else -40)
    easeout 0.30 alpha 1.0 xoffset 0

# The afterimage: a flat silhouette in their colour that overshoots and fades
# while the real art settles -- the fighting-game "snap in".
transform msbf_fm_ghost(token=0, color="#ffffff"):
    matrixcolor ColorizeMatrix(color, color)
    alpha (0.55 if token % 2 else 0.5)
    xoffset 0
    easeout 0.45 alpha 0.0 xoffset 52

transform msbf_fm_text_in(token=0, delay=0.0):
    alpha 0.0
    xoffset (14 if token % 2 else 12)
    pause delay
    easeout 0.22 alpha 1.0 xoffset 0

transform msbf_fm_watermark_in(token=0):
    rotate -90.0
    rotate_pad False
    alpha 0.0
    yoffset (80 if token % 2 else 72)
    easeout 0.55 alpha 0.5 yoffset 0

transform msbf_fm_pop:
    zoom 1.7
    alpha 0.0
    easeout 0.2 zoom 1.0 alpha 1.0

transform msbf_fm_flip(token=""):
    yzoom 0.0
    easeout 0.16 yzoom 1.0

transform msbf_fm_breathe(lo=0.45, hi=1.0, period=0.9):
    alpha lo
    block:
        ease period alpha hi
        ease period alpha lo
        repeat

transform msbf_fm_chevron(delay=0.0):
    alpha 0.15
    pause delay
    block:
        ease 0.35 alpha 0.95
        ease 0.55 alpha 0.15
        pause 0.3
        repeat

# A refusal. Token 0 never shakes, so nothing shakes on the first frame.
transform msbf_fm_shake(token=0):
    xoffset 0
    linear (0.04 if token else 0.0) xoffset (7 if token else 0)
    linear (0.06 if token else 0.0) xoffset (-6 if token else 0)
    linear (0.06 if token else 0.0) xoffset (4 if token else 0)
    linear (0.05 if token else 0.0) xoffset (-2 if token else 0)
    linear (0.04 if token else 0.0) xoffset 0

transform msbf_fm_launch_streak:
    xzoom 0.0
    alpha 0.95
    easeout 0.16 xzoom 1.0

transform msbf_fm_launch_word:
    alpha 0.0
    zoom 1.4
    easeout 0.16 alpha 1.0 zoom 1.0

transform msbf_fm_launch_flash:
    alpha 0.0
    pause 0.14
    easein 0.26 alpha 1.0


# -----------------------------------------------------------------------------
# THE SCREEN
# -----------------------------------------------------------------------------
screen msbf_party_select():
    modal True
    use enter_m_input_lock()

    default picks = []
    default rows = {}
    default sel = 0
    # The one cursor: which row it is in, and where.
    default zone = "roster"
    default pidx = 0
    # Did the pointer move last? (The help strip speaks to whichever did.)
    default mouse = False
    default deny = 0
    default deny_what = ""
    default launch = False

    # Right-click on empty space opens the pause menu, as Escape does. It needs
    # its own binding: this project takes mouseup_3 OUT of game_menu
    # (definitions.rpy -- right-click hides the windows, as in DDLC), so the
    # old screen's right-click did nothing; every other mode binds it the same
    # way. Bound FIRST: a screen hands an event to its LAST children first, so
    # every card, plate and sprite below sees a right-click before this does
    # (they use it to remove). The cursor keys are bound LAST for the same
    # reason.
    if not launch:
        key "game_menu" action Show("msbf_pause_menu", prefight=True)
        key "mouseup_3" action Show("msbf_pause_menu", prefight=True)

    # --- state, read once ------------------------------------------------------
    $ _idm = bool(getattr(store, "_msbf_id_mode", False))
    $ _nr = len(MSBF_ROSTER)
    $ _sel = int(sel) % _nr
    $ _e = MSBF_ROSTER[_sel]
    $ _id = _e["id"]
    $ _acc = msbf_roster_accent(_sel)
    $ _np = len(picks)
    $ _zone = zone if (zone != "party" or _np) else "roster"
    $ _pi = max(0, min(int(pidx), _np - 1)) if _np else 0
    $ _ready = msbf_can_begin(picks, rows)
    $ _in = _id in picks
    $ _full = _np >= 4
    $ _hq = msbf_seer_art_hq()

    # =========================================================================
    # THE ROOM
    # =========================================================================
    use msbf_arena_static(2 if _idm else 1, 0.34)
    use msbf_hud_scrim(0, 0, 800, 720, 0.0, 0.7, 1.0, 0.62)
    use msbf_hud_scrim(0, 0, 1280, 160, 1.0, 1.4, 0.0, 0.50)
    use msbf_hud_scrim(0, 520, 1280, 200, 0.0, 1.2, 0.0, 0.66)

    # =========================================================================
    # THE OFFICIAL DESIGN (left)
    # =========================================================================
    # The light they stand in, the Seer's seal turning behind them in their
    # colour, and their class written down the edge of the frame.
    add msbf_memo(msbf_plate, 330, 720, -120, _pl_rgba(_acc, 0.16), _pl_rgba(_acc, 0.02), _pl_rgba(_acc, 0.0), _pl_rgba(_acc, 0.0)):
        xpos 60
        ypos 0
    use msbf_boss_aura(230, 300, 600, 600, msbf_hex_rgb(_acc), (1.0, 1.0, 1.0), 0.30)
    fixed:
        xysize (440, 440)
        xcenter 230
        ycenter 300
        at msbf_t(msbf_fm_spin, 90.0, 360.0)
        add (MSBF_SEER_ART + "seal.png") at msbf_t(msbf_fm_tint, _acc, 0.30):
            xysize (440, 440)
    fixed:
        xysize (520, 520)
        xcenter 230
        ycenter 300
        at msbf_t(msbf_fm_spin, 46.0, -360.0)
        add (MSBF_SEER_ART + "orbit_current.png") at msbf_t(msbf_fm_tint, _acc, 0.42):
            xysize (520, 520)
    text _e["role"].upper() style "msbf_fm_watermark" at msbf_t(msbf_fm_watermark_in, _sel):
        outlines [(2, _acc, 0, 0)]
        xcenter 46
        ycenter 372

    if MSBF_SIL_SPRITE.get(_id):
        add msbf_memo(msbf_fm_hero, _id, "ghost") at msbf_t(msbf_fm_ghost, _sel, _acc)
        add msbf_memo(msbf_fm_hero, _id, "art") at msbf_t(msbf_fm_hero_in, _sel)

    # Keep the title and the art switch legible over hair, hats and boots.
    # The top band is even across the panel: Sam's axe and Monika's hat rise
    # behind the right half of the title, not just the left.
    use msbf_hud_scrim(0, 0, 470, 150, 1.0, 1.2, 0.0, 0.80)
    use msbf_hud_scrim(0, 610, 470, 110, 0.0, 1.1, 1.0, 0.70)

    text "VS. THE ONTOLOGICAL SEER" style "msbf_hud_kicker" color "#9fb4c4" at msbf_t(msbf_hud_in, 0.0, -10, 0):
        xpos 30
        ypos 20
    if _idm:
        fixed:
            xpos 266
            ypos 15
            xysize (96, 24)
            at msbf_t(msbf_hud_in, 0.12, 0, -6)
            add msbf_fm_plate_static(6.0, (0.55, 0.05, 0.14, 0.94), (0.32, 0.02, 0.08, 0.94), (1.0, 0.42, 0.52, 0.85))
            text "ID MODE" style "msbf_fm_stamp":
                align (0.5, 0.5)
    text "FORMATION" style "msbf_fm_title" at msbf_t(msbf_hud_in, 0.04, -14, 0):
        xpos 26
        ypos 34
    text "PICK FOUR  ·  SET THEIR ROWS  ·  BEGIN" style "msbf_hud_small" color "#8fa3b8" at msbf_t(msbf_hud_in, 0.08, -10, 0):
        xpos 30
        ypos 88

    # =========================================================================
    # THE FORMATION DECK (right) -- the battle sprites, in their rows
    # =========================================================================
    $ _rowl = [rows.get(_m, "front") for _m in picks] if _np else msbf_fm_ghost_rows()
    $ _form = msbf_px_formation(_rowl)
    $ _ddx, _ddy = msbf_fm_deck_offset(picks, rows)

    # Row names ride with the formation sideways only, so they stay on one line.
    fixed:
        xysize (1280, 720)
        at msbf_t(msbf_fm_slide, _ddx, 0)
        text "REAR" style "msbf_hud_kicker" color MSBF_FM_REAR:
            xcenter MSBF_PX_COL_REAR + 8
            ypos 112
        text "FRONT" style "msbf_hud_kicker" color MSBF_FM_FRONT:
            xcenter MSBF_PX_COL_FRONT + 8
            ypos 112
        # She stands this way: the chevrons run toward her, off the right edge.
        for _ci in range(3):
            text "›" style "msbf_hud_kicker" color MSBF_FM_FRONT at msbf_t(msbf_fm_chevron, _ci * 0.18):
                xpos MSBF_PX_COL_FRONT + 40 + _ci * 10
                ypos 111

    fixed:
        xysize (1280, 720)
        at msbf_t(msbf_fm_slide, _ddx, _ddy)
        for _lane in msbf_fm_lanes(_rowl, _form):
            $ _lx, _ly, _lw, _lh, _ls, _lrow, _llit = _lane
            $ _lc = msbf_fm_row_color(_lrow)
            add msbf_blank(_lw, _lh) at msbf_t(msbf_fm_plate_t, _ls, _pl_rgba(_lc, 0.08 if _llit else 0.05), _pl_rgba(_lc, 0.05 if _llit else 0.03), _pl_rgba(_lc, 0.32 if _llit else 0.55), MSBF_FM_CLEAR, 0.0, 0.0, (0.0 if _llit else 1.0), 0.22, False):
                xpos _lx
                ypos _ly
            if not _llit and _np:
                # Nobody in this row: a dim mark where they would stand.
                # (int(): a float position is a FRACTION of the screen in
                # Ren'Py, and the slant is a float.)
                add msbf_blank(118, 32) at msbf_t(msbf_fm_ring_t, _pl_rgba(_lc, 0.32), 0.0, False):
                    xcenter int(_lx + (_lw - _ls) * 0.5 + _ls * 0.4)
                    ycenter int(_ly + _lh * 0.6)
        if _np:
            for _mi, _mid in enumerate(picks):
                $ _mfoot = _form[_mi]
                $ _mhot = (_zone == "party" and _mi == _pi)
                add msbf_blank(118, 32) at msbf_t(msbf_fm_ring_t, _pl_rgba(MSBF_FM_CYAN if _mhot else msbf_fm_row_color(_rowl[_mi]), 0.95 if _mhot else 0.55), (0.35 if _mhot else 0.0), _mhot):
                    xcenter _mfoot[0]
                    ycenter _mfoot[1] + 2
            add msbf_px_select_stage(picks, rows)
            for _mi in msbf_fm_depth_order(_form):
                $ _mbx, _mby, _mbw, _mbh = msbf_fm_member_box(picks[_mi], _form[_mi])
                button:
                    style "msbf_status_button"
                    keyboard_focus False
                    xpos _mbx
                    ypos _mby
                    xysize (_mbw, _mbh)
                    hovered Function(msbf_fm_hover, "party", _mi)
                    hover_sound MSBF_UI_SFX["hover"]
                    action Function(msbf_fm_click_member, _mi)
                    alternate Function(msbf_fm_unpick_member, _mi)
            if _zone == "party":
                $ _gx, _gy = msbf_fm_point(picks[_pi], _form[_pi], "chest")
                add (MSBF_HUD_UI + "cursor_hand.png") at msbf_hand_bob:
                    zoom 2
                    nearest True
                    xpos _gx - 72
                    ycenter _gy
        else:
            for _gfoot in _form:
                add msbf_blank(118, 32) at msbf_t(msbf_fm_ring_t, (0.60, 0.70, 0.85, 0.28), 0.0, False):
                    xcenter _gfoot[0]
                    ycenter _gfoot[1] + 2

    if not _np:
        text "CHOOSE FOUR FIGHTERS" style "msbf_fm_empty" at msbf_t(msbf_hud_in, 0.2, 0, 8):
            xcenter 1025
            ycenter 330
        text "THEY STAND HERE, IN THE ROW YOU GIVE THEM" style "msbf_hud_small" color "#6f7d92" at msbf_t(msbf_hud_in, 0.26, 0, 8):
            xcenter 1025
            ycenter 356

    # =========================================================================
    # THE DOSSIER (centre)
    # =========================================================================
    $ _px, _py, _pw, _ph = MSBF_FM_PANEL
    fixed:
        xpos _px
        ypos _py
        xysize (_pw, _ph)
        at msbf_t(msbf_hud_in, 0.10, 0, 10)
        add msbf_blank(_pw, _ph) at msbf_t(msbf_fm_plate_t, 12.0, (0.02, 0.04, 0.08, 0.84), (0.01, 0.02, 0.05, 0.90), _pl_rgba(_acc, 0.30), _pl_rgba(_acc, 0.95), 0.0, 0.6, 0.0, 0.0, False)
        fixed:
            xysize (_pw, _ph)
            at msbf_t(msbf_fm_text_in, _sel, 0.03)
            text _e["name"].upper() style "msbf_fm_name":
                xpos 26
                ypos 10
            text _e["role"].upper() style "msbf_fm_role" color _acc:
                xpos 28
                ypos 62
            add Solid(_acc + "38") xpos 28 ypos 81 xysize (286, 1)
            add Solid(_acc) xpos 28 ypos 80 xysize (44, 3)
            text _e["summary"] style "msbf_fm_summary":
                xpos 28
                ypos 88
                xmaximum 286

            grid 2 2:
                xpos 28
                ypos 134
                xspacing 10
                yspacing 8
                use msbf_fm_stat("HP", _e["max_hp"], 700, "#66e08a")
                use msbf_fm_stat("ATK", _e["offense"], 90, "#ffcf66")
                use msbf_fm_stat("MAG", _e["magic"], 80, "#82a6ff")
                use msbf_fm_stat("SPD", _e["agility"], 76, "#ff6b8e")

            hbox:
                xpos 28
                ypos 200
                spacing 6
                text "WEAK" style "msbf_hud_small" color "#ffcf66" min_width 58 yalign 0.5
                if _e["weaknesses"]:
                    for _el in _e["weaknesses"]:
                        use msbf_fm_chip(_el)
                else:
                    text "NONE" style "msbf_hud_el" color "#6b7a8e" yalign 0.5
            hbox:
                xpos 28
                ypos 226
                spacing 6
                text "RESIST" style "msbf_hud_small" color "#8fa3b8" min_width 58 yalign 0.5
                if _e["resists"]:
                    for _el in _e["resists"]:
                        use msbf_fm_chip(_el)
                else:
                    text "NONE" style "msbf_hud_el" color "#6b7a8e" yalign 0.5

            add Solid("#9fb4c42a") xpos 28 ypos 256 xysize (286, 1)
            $ _sk = msbf_fm_skills(_id)
            for _ki, _krow in enumerate(_sk):
                $ _kname, _kel, _kcost = _krow
                fixed:
                    xpos 28 + (_ki % 2) * 148
                    ypos 264 + (_ki // 2) * 22
                    xysize (140, 22)
                    add (MSBF_HUD_UI + "diamond.png"):
                        nearest True
                        yalign 0.5
                        matrixcolor TintMatrix(msbf_element_color(_kel))
                    text _kname style "msbf_fm_skill":
                        xpos 14
                        yalign 0.5
                    if _kcost:
                        text "[_kcost]" style "msbf_fm_cost":
                            xpos 138
                            xanchor 1.0
                            yalign 0.5

            if _in:
                $ _dpos = picks.index(_id) + 1
                $ _drow = "FRONT" if rows.get(_id, "front") == "front" else "REAR"
                text "IN THE PARTY  ·  #[_dpos]  ·  [_drow] ROW" style "msbf_fm_status" color "#7dffa0":
                    xpos 28
                    ypos 364
            elif _full:
                text "PARTY FULL" style "msbf_fm_status" color "#ff8a9a" at msbf_t(msbf_fm_shake, deny if deny_what == "full" else 0):
                    xpos 28
                    ypos 364
            else:
                text "AVAILABLE" style "msbf_fm_status" color "#9fb4c4":
                    xpos 28
                    ypos 364

        # The dossier's own button, for the mouse. (Z on the card does the
        # same thing, and the keys never need to reach this.)
        button:
            style "msbf_fm_cta"
            xpos 28
            ypos 386
            xysize (286, 40)
            keyboard_focus False
            sensitive (_in or not _full)
            hover_sound MSBF_UI_SFX["hover"]
            action Function(msbf_fm_click_card, _sel)
            background msbf_fm_plate_static(10.0, ((0.20, 0.05, 0.08, 0.80) if _in else (0.04, 0.10, 0.18, 0.86)), ((0.10, 0.02, 0.04, 0.86) if _in else (0.02, 0.05, 0.10, 0.90)), (_pl_rgba("#ff8a9a", 0.55) if _in else _pl_rgba(_acc, 0.60)), (_pl_rgba("#ff8a9a", 0.9) if _in else _pl_rgba(_acc, 0.9)), 0.4)
            hover_background msbf_fm_plate_static(10.0, ((0.32, 0.07, 0.12, 0.92) if _in else (0.08, 0.20, 0.34, 0.94)), ((0.16, 0.03, 0.06, 0.94) if _in else (0.03, 0.08, 0.16, 0.94)), (_pl_rgba("#ffb3be", 0.95) if _in else _pl_rgba(_acc, 1.0)), (_pl_rgba("#ff8a9a", 1.0) if _in else _pl_rgba(_acc, 1.0)), 0.4, 0.0, 0.8)
            insensitive_background msbf_fm_plate_static(10.0, (0.02, 0.03, 0.06, 0.60), (0.01, 0.02, 0.04, 0.66), (0.40, 0.46, 0.56, 0.20), MSBF_FM_CLEAR, 1.0)
            fixed:
                xysize (286, 40)
                add msbf_blank(286, 40) at msbf_t(msbf_fm_hover_sheen, 10.0)
                hbox:
                    xpos 20
                    yalign 0.5
                    spacing 12
                    text ("REMOVE FROM PARTY" if _in else ("REMOVE ONE FIRST" if _full else "ADD TO PARTY")) style "msbf_fm_cta_text" yalign 0.5
                    if _in or not _full:
                        use msbf_fm_keycap("Z")

    # =========================================================================
    # THE ROSTER (top) -- row one of the cursor
    # =========================================================================
    $ _cx0, _cy0, _cw, _ch, _cgap = MSBF_FM_CARD
    for _ri, _re in enumerate(MSBF_ROSTER):
        $ _rid = _re["id"]
        $ _rx = _cx0 + _ri * (_cw + _cgap)
        $ _rbrowse = (_ri == _sel)
        $ _rhot = _rbrowse and _zone == "roster"
        $ _rin = _rid in picks
        $ _rlock = _full and not _rin
        $ _racc = msbf_roster_accent(_ri)
        $ _redge, _rglow, _rrail, _rhatch = msbf_fm_card_look(_rhot, _rbrowse, _rin, _rlock, _racc)
        button:
            style "msbf_status_button"
            keyboard_focus False
            xpos _rx
            ypos _cy0
            xysize (_cw, _ch)
            hovered Function(msbf_fm_hover, "roster", _ri)
            hover_sound MSBF_UI_SFX["hover"]
            action Function(msbf_fm_click_card, _ri)
            alternate Function(msbf_fm_unpick_card, _ri)
            at msbf_t(msbf_hud_in, 0.05 + _ri * 0.035, 0, -12)
            fixed:
                xysize (_cw, _ch)
                at msbf_t(msbf_fm_lift, _rhot, -6)
                # The refusal shake is its own layer, so moving the cursor (which
                # rebuilds the lift) does not rebuild it too.
                fixed:
                    xysize (_cw, _ch)
                    at msbf_t(msbf_fm_shake, deny if (deny_what == "full" and _rhot) else 0)
                    add msbf_blank(_cw, _ch) at msbf_t(msbf_fm_plate_t, 8.0, MSBF_FM_INK_TOP, MSBF_FM_INK_BOTTOM, _redge, _rrail, _rglow, _rhatch, 0.0, 0.0, _rhot)
                    add msbf_memo(msbf_fm_card_portrait, _rid, msbf_fm_card_state(_rhot, _rbrowse, _rin, _rlock))
                    text _re["name"].upper() style "msbf_fm_cardname" color ("#ffffff" if (_rhot or _rin) else ("#dfe7f2" if _rbrowse else "#7f8da3")):
                        xcenter 55
                        ypos 57
                    text _re["role"].upper() style "msbf_fm_cardrole" color _racc:
                        xcenter 54
                        ypos 71
                    if _rin:
                        $ _rord = picks.index(_rid) + 1
                        fixed:
                            xysize (28, 28)
                            xpos 86
                            ypos -10
                            at msbf_fm_pop
                            add (MSBF_HUD_UI + "diamond.png"):
                                zoom 3
                                nearest True
                                align (0.5, 0.5)
                                matrixcolor TintMatrix(msbf_fm_row_color(rows.get(_rid, "front")))
                            text "[_rord]" style "msbf_fm_digit":
                                align (0.5, 0.5)
        if _rhot:
            add (MSBF_HUD_UI + "cursor_down.png") at msbf_cursor_bob:
                zoom 2
                nearest True
                xcenter _rx + _cw // 2 + 2
                ypos 3

    # =========================================================================
    # THE PARTY (bottom) -- row two. Turn order runs left to right.
    # =========================================================================
    text "PARTY" style "msbf_hud_kicker" color ("#ffffff" if _zone == "party" else "#9fb4c4"):
        xpos 450
        ypos 566
    text "[_np] / 4" style "msbf_fm_count":
        xpos 510
        ypos 561
    text "TURN ORDER  ›" style "msbf_hud_small" color "#6f7d92":
        xpos 572
        ypos 567

    $ _sx0, _sy0, _sw, _sh, _sgap = MSBF_FM_PLATE
    for _si in range(4):
        $ _sx = _sx0 + _si * (_sw + _sgap)
        $ _sn = _si + 1
        if _si < _np:
            $ _smid = picks[_si]
            $ _sent = MSBF_ROSTER_BY_ID[_smid]
            $ _srow = rows.get(_smid, "front")
            $ _src = msbf_fm_row_color(_srow)
            $ _shot = (_zone == "party" and _si == _pi)
            fixed:
                xpos _sx
                ypos _sy0
                xysize (_sw, _sh)
                at msbf_t(msbf_hud_in, 0.0, 0, 10)
                button:
                    style "msbf_status_button"
                    keyboard_focus False
                    xysize (_sw, _sh)
                    hovered Function(msbf_fm_hover, "party", _si)
                    hover_sound MSBF_UI_SFX["hover"]
                    action Function(msbf_fm_click_member, _si)
                    alternate Function(msbf_fm_unpick_member, _si)
                    fixed:
                        xysize (_sw, _sh)
                        at msbf_t(msbf_fm_lift, _shot, -5)
                        add msbf_blank(_sw, _sh) at msbf_t(msbf_fm_plate_t, 10.0, MSBF_FM_INK_TOP, MSBF_FM_INK_BOTTOM, (_pl_rgba(MSBF_FM_CYAN, 0.95) if _shot else MSBF_FM_IDLE_EDGE), _pl_rgba(_src, 0.95), (0.7 if _shot else 0.0), 0.4, 0.0, 0.0, _shot)
                        fixed:
                            xysize (28, 28)
                            xpos 13
                            yalign 0.5
                            add (MSBF_HUD_UI + "diamond.png"):
                                zoom 3
                                nearest True
                                align (0.5, 0.5)
                                matrixcolor TintMatrix(_src)
                            text "[_sn]" style "msbf_fm_digit":
                                align (0.5, 0.5)
                        add msbf_memo(msbf_fm_headshot, _smid, 46, 44, 4.0, 200):
                            xpos 46
                            yalign 0.5
                        text _sent["name"] style "msbf_fm_pname":
                            xpos 100
                            ypos 7
                        fixed:
                            xpos 100
                            ypos 31
                            xysize (60, 17)
                            at msbf_t(msbf_fm_flip, _srow)
                            add msbf_fm_plate_static(5.0, _pl_rgba(_src, 0.22), _pl_rgba(_src, 0.10), _pl_rgba(_src, 0.80))
                            text ("FRONT" if _srow == "front" else "REAR") style "msbf_fm_chip_text" color _src:
                                align (0.5, 0.5)
                # The remove badge, inside the plate of the member under the
                # cursor (it rides the same lift). It used to perch on the
                # corner and poked into the TURN ORDER line above.
                if _shot:
                    fixed:
                        xysize (_sw, _sh)
                        at msbf_t(msbf_fm_lift, True, -5)
                        button:
                            style "msbf_fm_x"
                            keyboard_focus False
                            xpos _sw - 34
                            ypos 27
                            xysize (22, 21)
                            hover_sound MSBF_UI_SFX["hover"]
                            action Function(msbf_fm_unpick_member, _si)
                            text "×" style "msbf_fm_x_text":
                                align (0.5, 0.45)
        else:
            $ _snext = (_si == _np)
            fixed:
                xpos _sx
                ypos _sy0
                xysize (_sw, _sh)
                at msbf_t(msbf_hud_in, 0.0, 0, 10)
                add msbf_blank(_sw, _sh) at msbf_t(msbf_fm_plate_t, 10.0, (0.02, 0.03, 0.06, 0.40), (0.01, 0.02, 0.04, 0.46), ((0.55, 0.92, 1.0, 0.55) if _snext else (0.45, 0.55, 0.68, 0.28)), MSBF_FM_CLEAR, 0.0, 0.0, 1.0, 0.0, False)
                fixed:
                    xysize (28, 28)
                    xpos 13
                    yalign 0.5
                    add (MSBF_HUD_UI + "diamond.png"):
                        zoom 3
                        nearest True
                        align (0.5, 0.5)
                        matrixcolor TintMatrix("#2a3546")
                    text "[_sn]" style "msbf_fm_digit" color "#7f8da3":
                        align (0.5, 0.5)
                if _snext:
                    text "NEXT PICK" style "msbf_fm_status" color "#9fe6ff" at msbf_t(msbf_fm_breathe, 0.45, 1.0, 0.8):
                        xpos 52
                        yalign 0.5
                else:
                    text "OPEN" style "msbf_fm_status" color "#4f5b6c":
                        xpos 52
                        yalign 0.5

    # =========================================================================
    # BEGIN -- row three -- and the help strip beside it
    # =========================================================================
    $ _bx, _by, _bw, _bh = MSBF_FM_BEGIN
    $ _bhot = (_zone == "begin")
    fixed:
        xpos _bx
        ypos _by
        xysize (_bw, _bh)
        at msbf_t(msbf_hud_in, 0.30, 12, 0), msbf_t(msbf_fm_shake, deny if deny_what == "begin" else 0)
        button:
            style "msbf_status_button"
            keyboard_focus False
            xysize (_bw, _bh)
            hovered Function(msbf_fm_hover, "begin")
            hover_sound MSBF_UI_SFX["hover"]
            action Function(msbf_fm_begin)
            fixed:
                xysize (_bw, _bh)
                at msbf_t(msbf_fm_lift, _bhot, -4)
                add msbf_blank(_bw, _bh) at msbf_t(msbf_fm_begin_t, _ready, _bhot)
                if _ready:
                    text "BEGIN" style "msbf_fm_begin_text":
                        xcenter 112
                        yalign 0.5
                    fixed:
                        xpos 184
                        yalign 0.5
                        xysize (52, 22)
                        use msbf_fm_keycap("SPACE")
                else:
                    hbox:
                        xcenter 128
                        ypos 11
                        spacing 6
                        for _bi in range(4):
                            add (MSBF_HUD_UI + "diamond.png"):
                                zoom 2
                                nearest True
                                matrixcolor TintMatrix(MSBF_FM_FRONT if _bi < _np else "#2a3546")
                    text msbf_fm_need_text(picks, rows) style "msbf_fm_need" color ("#ff8a9a" if (_np == 4) else "#8fa3b8"):
                        xcenter 128
                        ypos 30
    if _bhot:
        add (MSBF_HUD_UI + "cursor_hand.png") at msbf_hand_bob:
            zoom 2
            nearest True
            xpos _bx - 42
            ycenter _by + _bh // 2

    hbox:
        xpos 450
        ypos 664
        spacing 18
        at msbf_t(msbf_hud_in, 0.32, 0, 6)
        for _hk, _hl in msbf_fm_hints(_zone, mouse, _in, _full, _ready, _np):
            hbox:
                spacing 7
                yalign 0.5
                use msbf_fm_keycap(_hk)
                text _hl style "msbf_fm_hint" yalign 0.5

    # BATTLE ART -- the same choice as the fight's pause menu.
    hbox:
        xpos 26
        ypos 676
        spacing 6
        at msbf_t(msbf_hud_in, 0.34, 0, 6)
        text "BATTLE ART" style "msbf_hud_kicker" color "#9fb4c4" yalign 0.5
        null width 4
        textbutton "PIXEL":
            style "msbf_fm_seg"
            text_style "msbf_fm_seg_text"
            keyboard_focus False
            yalign 0.5
            selected (not _hq)
            hover_sound MSBF_UI_SFX["hover"]
            action Function(msbf_fm_set_art, "pixel")
        textbutton "ILLUSTRATED":
            style "msbf_fm_seg"
            text_style "msbf_fm_seg_text"
            keyboard_focus False
            yalign 0.5
            selected _hq
            hover_sound MSBF_UI_SFX["hover"]
            action Function(msbf_fm_set_art, "hq")
        null width 2
        use msbf_fm_keycap("TAB")

    # =========================================================================
    # THE LAUNCH, then the keys
    # =========================================================================
    if launch:
        # A slash of their colour, the word, then the white the entrance cuts
        # in from.
        add msbf_blank(1120, 104) at msbf_t(msbf_fm_plate_t, 48.0, _pl_rgba(_acc, 0.96), _pl_rgba(_acc, 0.78), (1.0, 1.0, 1.0, 0.9), (1.0, 1.0, 1.0, 0.95), 0.0, 0.0, 0.0, 0.0, True), msbf_fm_launch_streak:
            xcenter 640
            ycenter 360
        text "BEGIN" style "msbf_fm_launch_text" at msbf_fm_launch_word:
            xcenter 640
            ycenter 360
        add Solid("#ffffff") at msbf_fm_launch_flash
        timer 0.42 action Return(msbf_party_config(picks, rows))
    else:
        # Bound LAST so they beat a button under a resting pointer: Enter acts
        # on the cursor, never on whatever the mouse was left over.
        key "K_ESCAPE" action Show("msbf_pause_menu", prefight=True)
        key "focus_left" action NullAction()
        key "focus_right" action NullAction()
        key "focus_up" action NullAction()
        key "focus_down" action NullAction()
        key "anyrepeat_K_LEFT" action Function(msbf_fm_move, -1, 0)
        key "anyrepeat_K_a" action Function(msbf_fm_move, -1, 0)
        key "anyrepeat_K_RIGHT" action Function(msbf_fm_move, 1, 0)
        key "anyrepeat_K_d" action Function(msbf_fm_move, 1, 0)
        key "K_UP" action Function(msbf_fm_move, 0, -1)
        key "K_w" action Function(msbf_fm_move, 0, -1)
        key "K_DOWN" action Function(msbf_fm_move, 0, 1)
        key "K_s" action Function(msbf_fm_move, 0, 1)
        key "K_z" action Function(msbf_fm_confirm)
        key "K_RETURN" action Function(msbf_fm_confirm)
        key "K_KP_ENTER" action Function(msbf_fm_confirm)
        key "K_x" action Function(msbf_fm_back)
        key "K_LSHIFT" action Function(msbf_fm_back)
        key "K_BACKSPACE" action Function(msbf_fm_back)
        key "K_DELETE" action Function(msbf_fm_back)
        key "K_SPACE" action Function(msbf_fm_begin)
        key "K_TAB" action Function(msbf_fm_toggle_art)


# -----------------------------------------------------------------------------
# PIECES
# -----------------------------------------------------------------------------
screen msbf_fm_stat(label, value, max_value, fill_color):
    fixed:
        xysize (138, 24)
        text label style "msbf_hud_small":
            ypos 0
        text "[value]" style "msbf_hud_small" color "#ffffff":
            xpos 138
            xanchor 1.0
            ypos 0
        add msbf_memo(msbf_fm_bar, value, max_value, fill_color)

screen msbf_fm_chip(el):
    frame:
        background msbf_fm_plate_static(5.0, _pl_rgba(msbf_element_color(el), 0.22), _pl_rgba(msbf_element_color(el), 0.10), _pl_rgba(msbf_element_color(el), 0.75))
        padding (9, 2, 9, 3)
        yalign 0.5
        text el.upper() style "msbf_hud_el" color msbf_element_color(el)

# A key, drawn: a label, or the pixel cursor turned into arrows.
screen msbf_fm_keycap(k):
    frame:
        style "msbf_fm_keycap_frame"
        yalign 0.5
        if k in MSBF_FM_KEY_ARROWS:
            hbox:
                spacing 4
                yalign 0.5
                for _ka in MSBF_FM_KEY_ARROWS[k]:
                    add msbf_memo(msbf_fm_arrow, _ka):
                        yalign 0.5
        else:
            text k style "msbf_fm_keycap_text" yalign 0.5


# -----------------------------------------------------------------------------
# STYLES
# -----------------------------------------------------------------------------
style msbf_fm_title is default:
    font MSBF_HUD_FONT_NAME
    size 44
    color "#fbf6ec"
    kerning 4.0
    outlines [(3, "#02040acc", 0, 1)]

style msbf_fm_name is msbf_fm_title:
    size 42
    color "#ffffff"
    kerning 2.0

style msbf_fm_role is default:
    font MSBF_HUD_FONT_TECH
    size 13
    kerning 3.0
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_fm_summary is default:
    font MSBF_HUD_FONT_BODY
    size 15
    color "#cfd9e6"
    outlines [(1, "#02040acc", 0, 0)]

style msbf_fm_skill is default:
    font MSBF_HUD_FONT_BODY
    size 14
    color "#dfe7f2"
    outlines [(1, "#02040acc", 0, 0)]

style msbf_fm_cost is default:
    font MSBF_HUD_FONT_TECH
    size 11
    color "#a9c2ff"
    outlines [(1, "#02040acc", 0, 0)]

style msbf_fm_status is default:
    font MSBF_HUD_FONT_TECH
    size 12
    kerning 1.6
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_fm_cardname is default:
    font MSBF_HUD_FONT_TECH
    size 12
    kerning 1.4
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_fm_cardrole is default:
    font MSBF_HUD_FONT_TECH
    size 9
    kerning 1.0
    outlines [(1, "#02040ae6", 0, 0)]

style msbf_fm_digit is default:
    font MSBF_HUD_FONT_TECH
    size 13
    color "#0a0d12"

style msbf_fm_pname is default:
    font MSBF_HUD_FONT_BODY
    size 16
    bold True
    color "#ffffff"
    outlines [(2, "#02040acc", 0, 0)]

style msbf_fm_chip_text is default:
    font MSBF_HUD_FONT_TECH
    size 10
    kerning 1.6

style msbf_fm_count is default:
    font MSBF_HUD_FONT_TECH
    size 18
    color "#ffcf66"
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_fm_keycap_frame is default:
    background msbf_fm_plate_static(4.0, (0.10, 0.15, 0.22, 0.95), (0.05, 0.08, 0.13, 0.95), (0.62, 0.74, 0.88, 0.60))
    padding (7, 3, 7, 4)

style msbf_fm_keycap_text is default:
    font MSBF_HUD_FONT_TECH
    size 10
    color "#e8f1ff"
    kerning 1.0

style msbf_fm_hint is default:
    font MSBF_HUD_FONT_TECH
    size 11
    color "#9fb0c4"
    kerning 1.4
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_fm_begin_text is default:
    font MSBF_HUD_FONT_NAME
    size 30
    color "#ffffff"
    kerning 5.0
    outlines [(2, "#02040acc", 0, 1)]

style msbf_fm_need is default:
    font MSBF_HUD_FONT_TECH
    size 12
    kerning 1.8
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_fm_watermark is default:
    font MSBF_HUD_FONT_NAME
    size 76
    color "#05090fd0"
    kerning 5.0

style msbf_fm_empty is default:
    font MSBF_HUD_FONT_TECH
    size 18
    color "#8fa3b8"
    kerning 4.0
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_fm_stamp is default:
    font MSBF_HUD_FONT_TECH
    size 12
    color "#ffffff"
    kerning 2.4

style msbf_fm_launch_text is default:
    font MSBF_HUD_FONT_NAME
    size 64
    color "#ffffff"
    kerning 12.0
    outlines [(4, "#05090fd8", 0, 2)]

style msbf_fm_cta is button:
    padding (0, 0)

style msbf_fm_cta_text is default:
    font MSBF_HUD_FONT_TECH
    size 14
    color "#e8f1ff"
    hover_color "#ffffff"
    insensitive_color "#5b6678"
    kerning 2.4
    outlines [(2, "#02040ae6", 0, 0)]

style msbf_fm_x is button:
    padding (0, 0)
    background msbf_fm_plate_static(4.0, (0.20, 0.05, 0.08, 0.95), (0.12, 0.02, 0.05, 0.95), (1.0, 0.54, 0.60, 0.80))
    hover_background msbf_fm_plate_static(4.0, (0.50, 0.08, 0.14, 0.98), (0.30, 0.04, 0.08, 0.98), (1.0, 0.75, 0.80, 1.0), MSBF_FM_CLEAR, 0.0, 0.0, 0.8)

style msbf_fm_x_text is default:
    font MSBF_HUD_FONT_BODY
    size 18
    color "#ffd6dc"
    hover_color "#ffffff"

style msbf_fm_seg is button:
    padding (12, 5, 12, 6)
    background msbf_fm_plate_static(6.0, (0.03, 0.06, 0.11, 0.85), (0.01, 0.03, 0.06, 0.90), (0.45, 0.56, 0.70, 0.35))
    hover_background msbf_fm_plate_static(6.0, (0.06, 0.13, 0.22, 0.92), (0.02, 0.06, 0.12, 0.94), (0.62, 0.92, 1.0, 0.85), MSBF_FM_CLEAR, 0.0, 0.0, 0.6)
    selected_background msbf_fm_plate_static(6.0, (0.36, 0.80, 0.96, 0.96), (0.16, 0.50, 0.70, 0.96), (0.80, 0.97, 1.0, 0.95))
    selected_hover_background msbf_fm_plate_static(6.0, (0.48, 0.88, 1.0, 0.98), (0.22, 0.58, 0.80, 0.98), (1.0, 1.0, 1.0, 1.0), MSBF_FM_CLEAR, 0.0, 0.0, 0.6)

style msbf_fm_seg_text is default:
    font MSBF_HUD_FONT_TECH
    size 12
    color "#8fa3b8"
    hover_color "#ffffff"
    selected_color "#06101c"
    selected_hover_color "#06101c"
    kerning 2.0
