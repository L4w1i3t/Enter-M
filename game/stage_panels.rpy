# =============================================================================
# ENTER-M :: STAGE PANELS  --  the split-screen story layout
# -----------------------------------------------------------------------------
# WHAT IT DOES
#   While the main story is running, the BACKGROUND is cut into one panel per
#   on-stage character, divided by slanted gutters, and each panel frames its
#   own slice of the room. Two people talking are two shots side by side; a
#   third arrives and the room splits again to make space. Nobody on stage and
#   the background is exactly what it has always been.
#
#   THE CAST AND THE CUTS ARE ONE PIECE OF GEOMETRY. An N-person stage divides
#   the screen into N equal panels, and game/transforms.rpy's slot i stands in
#   the middle of panel i -- x = (i - 0.5) / N * 1280 -- so a character is never
#   crowded against a gutter nor marooned at a screen edge, whichever way the
#   room is split. The slot table is mirrored below in ENTER_M_PANEL_SLOT_X;
#   move a slot in one and you must move it in the other. On top of that, a cut
#   is then held ENTER_M_PANEL_CLEARANCE away from the characters either side of
#   it, so neither the speaker's claim nor a hand-placed sprite can put a gutter
#   through somebody's face.
#
#   What the panels do NOT do is clip. Sprites keep their slots, their poses,
#   their entrances, Autofocus, and every transform the story has ever put on
#   them -- they stand IN FRONT of the panel structure and are free to break the
#   frame, which an outflung arm will. That is a deliberate choice, not a
#   shortcut: this project's sprites are 300-440px wide depending on the pose,
#   so no gutter position cleanly separates them and a hard per-panel clip would
#   always leave a sliver of somebody's arm on the wrong side of a cut.
#   Everything below therefore happens in ONE fragment shader hung on the `bg`
#   tag, underneath every sprite.
#
# WHY IT IS SAFE WITH THE REST OF THE ENGINE
#   * It is a per-tag transform on `bg`, installed through config.tag_transform,
#     which Matsu'Py only applies to a show that carries NO `at` clause. A scene
#     written as `scene bg cafeteria at fx_push(...)` therefore opts itself out
#     and behaves exactly as it did before. SceneLists.clear() wipes at_list on
#     every `scene`, so the transform is re-applied per cut, predictably.
#   * It never touches the master layer at_list (fx_shake_screen) or the master
#     CAMERA list (atmosphere's saturation). Both stacks stay free.
#   * Transitions compose: a `with dissolve_scene_full` blends two frames that
#     are each already panelled, and a `scene` snaps the geometry (see
#     _stage_panels_scene) so the layout never slides across a cut.
#   * A split that OPENS mid-scene is seamless by construction, not by timing.
#     Every framing quantity is derived from the current eased zoom, and at zoom
#     1.0 each panel's window onto the room comes out exactly equal to its own
#     screen span -- the identity mapping. So engagement 0 is the untouched
#     background however many panels exist, and the room appears to crack apart
#     from the frame already on screen. (It used to map every panel's centre to
#     the CENTRE of the plate regardless of engagement, so the instant a second
#     panel was born the background jumped sideways under the gutter, and only
#     the gutter itself faded in.)
#   * The atmosphere grade, its particles and the theater house-lights all draw
#     ABOVE this, so the gutters are graded with the room instead of sitting on
#     top of it.
#
# WHY THE EASING IS CLOCKED ON frame_time AND NOT ON `st`
#   During a scene transition the OLD bg and the NEW bg are both on screen, so
#   the driver runs TWICE per frame with two unrelated `st` values. Integrating
#   dt from `st` would double-step the animation and desynchronise the two
#   copies. renpy.display.interface.frame_time is stamped once per drawn frame
#   (renpy/display/core.py:4168), so the first copy to render advances the
#   shared state and the second one reads it -- identical geometry, correct
#   speed. This is also why the fx.rpy layer-at-list `st` restart problem
#   cannot bite here: `st` is never read.
#
# SCOPE  --  MAIN STORY ONLY
#   Panels are for season 1. The scope latch reads the filename of the running
#   statement: a season 1 file turns it ON, one of the other presentation roots
#   (side stories, lost records, out-of-context scenes, the game modes, the OP,
#   the trailer) turns it OFF, and anything else -- helpers, addons, screens --
#   leaves the latch alone so a `call` into a shared label cannot flicker it.
#   stage_panels_suspend() / stage_panels_resume() are the manual override.
#
# PUBLIC API
#   persistent.enter_m_panels          on/off, wired to Settings > Graphics.
#   stage_panels_set_enabled(bool)     the setter the option calls.
#   stage_panels_suspend() / _resume() force it off around bespoke sequences.
#   stage_panels_refresh()             recompute now (after a manual re-stage).
#
# NO TWO PANELS SHOW THE SAME PART OF THE ROOM
#   Each panel's window onto the plate is a slice of a left-to-right TILING, not
#   a free-floating crop -- see _stage_panel_frames. Panel order and room order
#   therefore agree, adjacent shots are separated by a little deliberately
#   skipped background, and the same chair cannot appear either side of a cut.
#   (The windows were previously all centred on the plate and merely nudged
#   toward their character, which at two panels put ~13% of the background
#   inside both of them -- visibly duplicated furniture across the gutter.)
#
# HOW MANY PEOPLE IT HANDLES
#   Six, and gracefully more: the shader carries six panels, transforms.rpy
#   defines stages of one through six, and past six the closest neighbours on
#   stage share a panel (_stage_panel_group) rather than the format switching
#   itself off in the middle of a crowd scene. Panel zoom rises with the count,
#   because a narrower panel is a tighter shot -- which is what a camera would
#   do, and is also what buys the room for six windows to be six different
#   places.
#
# TUNING lives in section 2. The look is: gutter width, slant, the rim light
# and the shading that falls into each gutter. The framing is: panel zoom per
# stage size, how much room is skipped between panels, how hard a window leans
# toward its own character, and the clearance a cut keeps from the cast.
# =============================================================================


# -----------------------------------------------------------------------------
# 1. SHADER
# -----------------------------------------------------------------------------
# GLSL ES 1.00, matching atmosphere.rpy and theater_fx.rpy: no derivatives, no
# dynamic loops, every smoothstep with edge0 strictly below edge1, and every
# identifier prefixed because Matsu'Py 8.1.1 combines shader-part source into a
# single scope. fragment_300 so it wins against renpy.texture's fragment_200.
#
# Panel selection is SIX unrolled compares rather than a loop over an array:
# u_em_sp_p0..p5 are (left_edge, right_edge, source_center_x, screen_center_x),
# ordered left to right, and an unused panel parks its left edge at 3.0 where
# nothing can select it. The FIRST panel's left edge is -1.0 and the LAST
# panel's right edge is 2.0, which is what keeps a gutter from being drawn down
# the sides of the screen without needing a flag for it. Six is the ceiling on
# how many people the format will split the room between; ENTER_M_PANEL_MAX may
# be lowered but never raised past it without adding uniforms here.
#
# The cut is slanted, the CONTENT is not: panel selection and gutter distance
# use the skewed x, while the source lookup uses the true x. Slanting both
# would shear the room.
init -10 python:

    def _enter_m_stage_panels_register_shader():
        renpy.register_shader("enter_m.stage_panels", variables="""
            uniform sampler2D tex0;
            uniform vec2  u_model_size;
            uniform vec2  u_em_sp_screen;
            uniform vec4  u_em_sp_p0;
            uniform vec4  u_em_sp_p1;
            uniform vec4  u_em_sp_p2;
            uniform vec4  u_em_sp_p3;
            uniform vec4  u_em_sp_p4;
            uniform vec4  u_em_sp_p5;
            uniform float u_em_sp_zoom;
            uniform float u_em_sp_gap;
            uniform float u_em_sp_slant;
            uniform float u_em_sp_rim;
            uniform float u_em_sp_edge;
            uniform float u_em_sp_shade;
            uniform float u_em_sp_falloff;
            varying vec2  v_tex_coord;
        """, fragment_300="""
            // Child pixels -> screen fraction. Every background in the story is
            // 1280x720 at the origin, so this is the identity there; an odd-
            // sized plate degrades to the right scale instead of tearing.
            vec2 em_sp_size = max(u_model_size, vec2(1.0));
            vec2 em_sp_screen = max(u_em_sp_screen, vec2(1.0));
            vec2 em_sp_ratio = em_sp_size / em_sp_screen;
            vec2 em_sp_suv = v_tex_coord * em_sp_ratio;

            float em_sp_xs = em_sp_suv.x + (em_sp_suv.y - 0.5) * u_em_sp_slant;

            vec4 em_sp_pan = u_em_sp_p0;
            if (em_sp_xs >= u_em_sp_p1.x) { em_sp_pan = u_em_sp_p1; }
            if (em_sp_xs >= u_em_sp_p2.x) { em_sp_pan = u_em_sp_p2; }
            if (em_sp_xs >= u_em_sp_p3.x) { em_sp_pan = u_em_sp_p3; }
            if (em_sp_xs >= u_em_sp_p4.x) { em_sp_pan = u_em_sp_p4; }
            if (em_sp_xs >= u_em_sp_p5.x) { em_sp_pan = u_em_sp_p5; }

            // This panel's window onto the room: its own centre of the source
            // plate, scaled about that centre. Python has already clamped the
            // centre so the window cannot run off the edge of the plate.
            float em_sp_zoom = max(u_em_sp_zoom, 0.01);
            vec2 em_sp_src = vec2(
                em_sp_pan.z + (em_sp_suv.x - em_sp_pan.w) / em_sp_zoom,
                0.5 + (em_sp_suv.y - 0.5) / em_sp_zoom);
            vec2 em_sp_uv = clamp(
                em_sp_src / em_sp_ratio, vec2(0.0005), vec2(0.9995));

            vec4 em_sp_tex = texture2D(tex0, em_sp_uv);
            float em_sp_a = max(em_sp_tex.a, 0.0001);
            vec3 em_sp_col = em_sp_tex.rgb / em_sp_a;

            // Distance to the nearer edge of this panel, in the skewed x.
            float em_sp_d = min(em_sp_xs - em_sp_pan.x, em_sp_pan.y - em_sp_xs);
            float em_sp_aa = 0.0014;
            float em_sp_gap = max(u_em_sp_gap, 0.0);
            float em_sp_cut = 1.0 - smoothstep(
                max(em_sp_gap - em_sp_aa, 0.0),
                em_sp_gap + em_sp_aa,
                em_sp_d);

            // Shading that falls INTO the gutter gives the panels an edge to
            // sit on; the rim is the thin catch-light just inside the cut.
            float em_sp_shade = 1.0 - smoothstep(
                em_sp_gap,
                em_sp_gap + max(u_em_sp_falloff, 0.001),
                em_sp_d);
            float em_sp_rim = (1.0 - smoothstep(
                em_sp_gap,
                em_sp_gap + max(u_em_sp_rim, 0.0005),
                em_sp_d)) * (1.0 - em_sp_cut);

            em_sp_col *= 1.0 - em_sp_shade * clamp(u_em_sp_shade, 0.0, 1.0);
            em_sp_col += vec3(1.0) * em_sp_rim * max(u_em_sp_edge, 0.0);
            em_sp_col *= 1.0 - em_sp_cut;

            gl_FragColor = vec4(em_sp_col * em_sp_a, em_sp_a);
        """)

    try:
        _enter_m_stage_panels_register_shader()
        ENTER_M_STAGE_PANEL_SHADER = True
    except Exception as _enter_m_stage_panels_error:
        ENTER_M_STAGE_PANEL_SHADER = False
        renpy.log("ENTER-M PANELS: shader registration failed: %r" %
            _enter_m_stage_panels_error)


# -----------------------------------------------------------------------------
# 2. TUNING
# -----------------------------------------------------------------------------
# The player-facing switch. New key, so `default` reaches every profile: the
# format ships ON and the option in Settings > Graphics turns it off for anyone
# who wants the plain single-frame presentation back.
default persistent.enter_m_panels = True

# SLOT TABLE. These are the screen x of each slot in game/transforms.rpy, and
# they are THE SAME NUMBERS the panels are cut on: an N-person stage divides the
# screen into N equal panels and slot i stands in the middle of panel i, so
#
#     x = (i - 0.5) / N * 1280
#
# The table is duplicated here rather than derived because an ATL block's call
# arguments are not readable from Python. IF YOU MOVE A SLOT IN transforms.rpy,
# MOVE IT HERE TOO; a stale entry does not crash, it just puts the gutter in the
# wrong place. Stages of five and six exist for the same reason the shader
# carries six panels -- see ENTER_M_PANEL_MAX.
define ENTER_M_PANEL_SLOT_X = {
    "61": 107, "62": 320, "63": 533, "64": 747, "65": 960, "66": 1173,
    "51": 128, "52": 384, "53": 640, "54": 896, "55": 1152,
    "41": 160, "42": 480, "43": 800, "44": 1120,
    "31": 213, "32": 640, "33": 1067,
    "21": 320, "22": 960,
    "11": 640,
}

# How many panels the room will be cut into. SIX IS THE HARD CEILING -- it is
# how many vec4s the shader carries. Past this the closest neighbours on stage
# SHARE a panel (see _stage_panel_group) rather than the format switching itself
# off, because a layout that collapses exactly when the room is at its busiest
# reads as a bug.
define ENTER_M_PANEL_MAX = 6
define ENTER_M_PANEL_MIN_W = 0.13     # narrowest a panel may be, as a fraction

# LOOK
define ENTER_M_PANEL_GAP = 16.0       # gutter width in px at full engagement
define ENTER_M_PANEL_SLANT = 74.0     # px the cut leans across the screen height
define ENTER_M_PANEL_SLANT_FIT = 340.0  # panels narrower than this lean less
define ENTER_M_PANEL_RIM = 2.6        # px of catch-light inside each cut
define ENTER_M_PANEL_EDGE = 0.30      # how bright that catch-light burns
define ENTER_M_PANEL_SHADE = 0.34     # how dark the plate goes into the gutter
define ENTER_M_PANEL_FALLOFF = 26.0   # px that shading reaches into the panel

# FRAMING. How far each panel pushes into the plate, by how many panels there
# are: a narrow panel is a tighter shot, which is both what a camera would do
# and what buys the room for the panels to look at DIFFERENT parts of the plate
# (see _stage_panel_frames -- the free space a zoom opens up is exactly the
# budget the windows are spread across). Stages of one to three keep the 1.10
# the format shipped with.
define ENTER_M_PANEL_ZOOM = {
    1: 1.10, 2: 1.16, 3: 1.22, 4: 1.28, 5: 1.32, 6: 1.36,
}

# Room deliberately SKIPPED between neighbouring panels, as a fraction of the
# plate: a slice of the background that no panel shows, so two adjacent shots
# read as two angles on a room instead of one photograph with a line drawn down
# it. Capped at a share of whatever free space the zoom actually opened up.
define ENTER_M_PANEL_SEPARATION = 0.055
define ENTER_M_PANEL_SEP_SHARE = 0.65

# How hard a panel's window leans toward its own character when the character is
# not standing in the middle of their panel (the speaker's claim, or a
# hand-placed sprite). 0 frames every panel dead centre.
define ENTER_M_PANEL_LEAN = 0.55

define ENTER_M_PANEL_EXPAND = 0.036   # extra width the speaker's panel claims

# CLEARANCE. A cut never comes closer than this -- as a fraction of the screen --
# to the character on either side of it, whatever the speaker's claim or a
# hand-placed sprite would otherwise do. 0.085 is 109px, comfortably outside the
# shoulders of this cast at the staging scales in transforms.rpy.
define ENTER_M_PANEL_CLEARANCE = 0.085

# MOTION. Two exponential time constants: the room OPENING (and closing) is the
# slower of the two, because it is a reveal, while boundaries sliding and the
# speaker's claim are corrections and want to be crisp.
define ENTER_M_PANEL_EASE = 0.115
define ENTER_M_PANEL_OPEN = 0.20

# SCOPE. Prefixes are matched against the filename of the running statement.
# ON wins over OFF; anything in neither list leaves the latch where it is, so a
# `call` into a shared helper label cannot strobe the layout.
define ENTER_M_PANEL_SCOPE_ON = (
    "game/story/season1/",
)
define ENTER_M_PANEL_SCOPE_OFF = (
    "game/story/out_of_context/",
    "game/lost_records/",
    "game/addons/Character Stories/",
    "game/addons/Matsuda's Sick Boss Fight/",
    "game/addons/Arcade/",
    "game/addons/Archivist Invasions/",
    "game/addons/Next Time Trailer/",
    "game/addons/Sick Ass Anime OP/",
)


# -----------------------------------------------------------------------------
# 3. GEOMETRY
# -----------------------------------------------------------------------------
# _stage_panels is the live layout, ordered left to right. One entry per panel:
#
#   tag    the character it belongs to
#   x/cx   target and current centre, as a fraction of screen width
#   w/cw   target and current width share; a panel is BORN at cw 0.0 and DIES
#          by easing its target to 0.0, which is what makes the room open and
#          close instead of popping.
#
# Widths are normalised at paint time rather than here, so a panel opening
# automatically squeezes its neighbours by exactly the space it takes.
#
# None of this is saved. It is derived entirely from the scene lists plus the
# persistent switch, and a load or a `scene` snaps it -- which is also why an
# init-python dict is the right home for it (see the init-state-not-saved rule:
# a mutated init dict is never written to a save, and here that is a feature).
init python:
    import math as _enter_m_sp_math

    _SP_LAYER = "master"

    _stage_panels = []

    _stage_state = {
        "amt": 0.0,          # engagement 0..1: gutters, zoom and parallax ride it
        "amt_target": 0.0,
        "speaker": None,
        "scope": False,      # is the running statement inside the main story
        "suspend": 0,        # manual override depth
        "frame": None,       # last frame_time the ease advanced on
        "snap": False,       # next advance lands instantly (cut, load, restage)
        "signature": None,   # last target set handed to the driver
    }

    def _stage_panels_active():
        return (ENTER_M_STAGE_PANEL_SHADER
            and persistent.enter_m_panels
            and _stage_state["scope"]
            and _stage_state["suspend"] <= 0)

    # --- where a sprite is standing -----------------------------------------
    # The slot table is the primary answer because it is exact, stable, and
    # unaffected by an entrance still animating -- a divider that chased a
    # sliding sprite would swim. Autofocus already owns the reverse mapping
    # from a live at_list back to a slot (including the durable ATL-location
    # path that survives a reload and a load), so it is borrowed rather than
    # reimplemented, defensively in case that addon is ever removed.
    def _stage_panel_measure(tag):
        """Fallback: the sprite's real placement, for a manual `at`."""
        try:
            lists = renpy.game.context().scene_lists
            shown = lists.get_displayable_by_tag(_SP_LAYER, tag)

            if shown is None:
                return None

            place = shown.get_placement()
        except Exception:
            return None

        xpos = place[0]
        xoffset = place[4]

        if xpos is None:
            return None

        try:
            x = float(xpos)
        except (TypeError, ValueError):
            return None

        # A bare float is a fraction of the screen; `absolute` (and an int) is
        # already in pixels. Every slot transform uses xcenter, i.e. absolute.
        if isinstance(xpos, float) and not isinstance(xpos, absolute):
            if 0.0 <= x <= 1.0:
                x *= float(config.screen_width)

        try:
            x += float(xoffset or 0)
        except (TypeError, ValueError):
            pass

        return x

    def _stage_panel_x(tag):
        reverse = getattr(store, "_autofocus_slot_from_at_list", None)

        if reverse is not None:
            try:
                at_list = renpy.get_at_list(tag, layer=_SP_LAYER)
            except Exception:
                at_list = None

            if at_list:
                match = reverse(list(at_list))

                if match is not None:
                    slot_x = ENTER_M_PANEL_SLOT_X.get(match[0])

                    if slot_x is not None:
                        return float(slot_x)

        return _stage_panel_measure(tag)

    def _stage_panels_scan():
        """[(x fraction, tag)] for every cast sprite on stage, left to right."""
        roster = getattr(store, "ENTER_M_SPRITE_TAGS", ())

        if not roster:
            return []

        width = float(config.screen_width)
        stage = []

        for tag in renpy.get_showing_tags(layer=_SP_LAYER):
            if tag not in roster:
                continue

            x = _stage_panel_x(tag)

            if x is None:
                continue

            stage.append((max(0.0, min(1.0, x / width)), tag))

        stage.sort()

        return stage

    # --- how many panels the room will take ----------------------------------
    # Six is the shader's ceiling; ENTER_M_PANEL_MAX may sit below it.
    _SP_SHADER_PANELS = 6

    def _stage_panel_limit():
        return max(1, min(int(ENTER_M_PANEL_MAX), _SP_SHADER_PANELS))

    # More people on stage than there are panels to give them. Dropping the
    # format here is the wrong answer -- the layout would collapse exactly when
    # the room is at its busiest, which reads as a bug rather than a choice --
    # so the closest pair of neighbours SHARES a panel instead, repeatedly,
    # until the stage fits. The merged panel sits at the group's mean x and
    # keeps the leftmost member's tag as its identity, so a crowd that holds
    # still produces the same grouping on every pass.
    def _stage_panel_group(stage):
        limit = _stage_panel_limit()

        if len(stage) <= limit:
            return stage

        groups = [[x, tag, 1] for x, tag in stage]

        while len(groups) > limit:
            best = 0
            gap = None

            for index in range(len(groups) - 1):
                span = groups[index + 1][0] - groups[index][0]

                if gap is None or span < gap:
                    gap = span
                    best = index

            left = groups[best]
            right = groups.pop(best + 1)
            total = left[2] + right[2]
            left[0] = (left[0] * left[2] + right[0] * right[2]) / total
            left[2] = total

        return [(x, tag) for x, tag, _count in groups]

    # --- target widths -------------------------------------------------------
    # A boundary sits at the midpoint between two neighbours, which -- because
    # the slot table stands everyone in the middle of their own panel already
    # (game/transforms.rpy) -- is the cut the staging was designed around. The
    # speaker then claims a fixed slice of extra width, fixed rather than
    # proportional so the emphasis stays legible in a six-way split instead of
    # shrinking with the panel; and then every cut is pulled back out of the
    # personal space of the characters on either side of it.
    def _stage_panel_normalise(widths):
        total = sum(widths)

        if total <= 1e-6:
            return [1.0 / max(len(widths), 1)] * len(widths)

        return [w / total for w in widths]

    def _stage_panel_widths(stage, speaker):
        xs = [x for x, _ in stage]
        count = len(xs)

        if count == 1:
            return [1.0]

        edges = [0.0]
        edges += [(xs[i] + xs[i + 1]) * 0.5 for i in range(count - 1)]
        edges += [1.0]

        # The claim is taken from whichever neighbours the speaker has -- half
        # from each in the middle of a row, all of it from the one inner edge at
        # either end of it.
        if speaker is not None and ENTER_M_PANEL_EXPAND > 0.0:
            for index, (_, tag) in enumerate(stage):
                if tag != speaker:
                    continue

                sides = (1 if index > 0 else 0) + (1 if index < count - 1 else 0)

                if sides:
                    claim = ENTER_M_PANEL_EXPAND / sides

                    if index > 0:
                        edges[index] -= claim

                    if index < count - 1:
                        edges[index + 1] += claim

                break

        # CLEARANCE. Slot x is panel centre, so on a scripted stage nothing here
        # binds; it catches the speaker's claim and hand-placed sprites, and
        # when it catches one it is the difference between a gutter behind a
        # shoulder and a gutter through a face. The bounds cannot cross each
        # other (xs is sorted and every window is [x + c, x' - c]), so the edge
        # list stays monotonic and the widths stay positive.
        for index in range(1, count):
            low = xs[index - 1] + ENTER_M_PANEL_CLEARANCE
            high = xs[index] - ENTER_M_PANEL_CLEARANCE

            if low > high:
                low = high = (xs[index - 1] + xs[index]) * 0.5

            edges[index] = min(max(edges[index], low), high)

        widths = [max(0.0, edges[i + 1] - edges[i]) for i in range(count)]
        widths = _stage_panel_normalise(widths)

        # Pull anything below the floor back up, paying for it out of whatever
        # room the wider panels have to spare. Three passes is plenty for four
        # panels and cannot loop forever on a degenerate layout.
        floor = ENTER_M_PANEL_MIN_W

        if count * floor < 1.0:
            for _ in range(3):
                deficit = sum(max(0.0, floor - w) for w in widths)

                if deficit <= 1e-6:
                    break

                spare = sum(max(0.0, w - floor) for w in widths)

                if spare <= 1e-6:
                    break

                scale = max(0.0, 1.0 - deficit / spare)
                widths = [
                    floor + (w - floor) * scale if w > floor else floor
                    for w in widths]

        return _stage_panel_normalise(widths)

    def _stage_panels_retarget():
        """Re-derive every panel's target from who is on stage right now."""
        stage = _stage_panels_scan() if _stage_panels_active() else []

        if stage:
            stage = _stage_panel_group(stage)

        if not stage:
            # Nobody on stage: every panel dies and the plate returns to being a
            # plain background, at which point the shader takes itself off.
            _stage_state["amt_target"] = 0.0

            for panel in _stage_panels:
                panel["alive"] = False
                panel["w"] = 0.0

            _stage_panels_wake()

            return

        _stage_state["amt_target"] = 1.0

        speaker = _stage_state["speaker"]
        widths = _stage_panel_widths(stage, speaker)

        # Dying panels are candidates too, so a character who is re-shown
        # before their panel has finished closing REVIVES it -- otherwise the
        # tag ends up owning two panels at once and the room never adds up.
        # Where a tag somehow has both, the wider one is the real panel.
        existing = {}

        for panel in _stage_panels:
            current = existing.get(panel["tag"])

            if current is None or panel["cw"] > current["cw"]:
                existing[panel["tag"]] = panel

        keep = set()

        for index, (x, tag) in enumerate(stage):
            panel = existing.get(tag)

            if panel is None:
                panel = {"tag": tag, "x": x, "cx": x, "w": 0.0, "cw": 0.0,
                        "alive": True}
                _stage_panels.append(panel)

            panel["x"] = x
            panel["w"] = widths[index]
            panel["alive"] = True
            # Identity, not equality: two panels with the same contents are
            # equal as dicts, and `panel in keep` would then keep the wrong one.
            keep.add(id(panel))

        for panel in _stage_panels:
            if id(panel) not in keep:
                panel["alive"] = False
                panel["w"] = 0.0

        # Left to right, dying panels included, so a panel collapses in place.
        _stage_panels.sort(key=lambda p: p["x"] if p["alive"] else p["cx"])

        # The shader carries six panels. A cast swap can briefly stack live
        # panels on top of dying ones, so the faintest ghosts are dropped
        # rather than silently falling off the end of the uniform list.
        while len(_stage_panels) > _SP_SHADER_PANELS:
            ghosts = [p for p in _stage_panels if not p["alive"]]

            if not ghosts:
                del _stage_panels[_SP_SHADER_PANELS:]
                break

            _stage_panels.remove(min(ghosts, key=lambda p: p["cw"]))

    # THE WAKE-UP. A settled driver returns None, and Matsu'Py then caches the
    # background's render and stops calling the driver at all -- which is
    # exactly what we want while a layout is holding still, and exactly what
    # strands it the moment a target moves. Measured: without this, a character
    # arriving mid-scene was added to the layout and the plate never redrew, so
    # the panel stayed at width zero forever. renpy.redraw() invalidates that
    # cached render and the driver takes over again from the next frame.
    def _stage_panels_signature():
        return (
            round(_stage_state["amt_target"], 4),
            tuple((p["tag"], p["alive"], round(p["w"], 4), round(p["x"], 4))
                for p in _stage_panels))

    def _stage_panels_wake():
        signature = _stage_panels_signature()

        if signature == _stage_state["signature"]:
            return

        _stage_state["signature"] = signature

        try:
            lists = renpy.game.context().scene_lists
            shown = lists.get_displayable_by_tag(_SP_LAYER, "bg")
        except Exception:
            return

        if shown is not None:
            renpy.redraw(shown, 0)

    # --- the ease ------------------------------------------------------------
    # Advances AT MOST once per drawn frame. See the header for why the clock is
    # frame_time and not the transform's st.
    def _stage_panels_advance():
        now = getattr(renpy.display.interface, "frame_time", None)
        last = _stage_state["frame"]
        _stage_state["frame"] = now

        if _stage_state["snap"]:
            blend = 1.0
            opening = 1.0
        elif now is None or last is None or now <= last:
            return
        else:
            # Clamped to a single frame's worth. The driver sleeps whenever a
            # layout is settled, so `last` can be a whole line of dialogue old;
            # integrating that gap in one go would spend most of the ease on
            # the first frame and land as a snap.
            delta = min(now - last, 1.0 / 30.0)
            blend = 1.0 - _enter_m_sp_math.exp(
                -delta / max(ENTER_M_PANEL_EASE, 0.001))
            opening = 1.0 - _enter_m_sp_math.exp(
                -delta / max(ENTER_M_PANEL_OPEN, 0.001))

        if blend <= 0.0:
            return

        _stage_state["snap"] = False
        _stage_state["amt"] += (
            _stage_state["amt_target"] - _stage_state["amt"]) * opening

        for panel in _stage_panels:
            panel["cw"] += (panel["w"] - panel["cw"]) * blend
            panel["cx"] += (panel["x"] - panel["cx"]) * blend

        for panel in list(_stage_panels):
            if not panel["alive"] and panel["cw"] <= 0.0015:
                _stage_panels.remove(panel)

    def _stage_panels_settled():
        if abs(_stage_state["amt_target"] - _stage_state["amt"]) > 0.0015:
            return False

        for panel in _stage_panels:
            if abs(panel["w"] - panel["cw"]) > 0.0015:
                return False

            if abs(panel["x"] - panel["cx"]) > 0.0015:
                return False

        return True


# -----------------------------------------------------------------------------
# 4. THE DRIVER
# -----------------------------------------------------------------------------
# A function transform, hung on the `bg` tag. It writes the uniforms for the
# current geometry and hands the frame back; when the layout is fully retracted
# it takes the mesh and the shader off again, so a scene with nobody in it pays
# nothing at all -- no render-to-texture, no extra pass.
#
# The callable is a module-level class instance rather than a closure for the
# same reason Autofocus's grade is: the transform ends up attached to a shown
# image, and Matsu'Py pickles the whole image stack on every save. A local
# closure cannot be pickled and takes the save down with it.
init python:

    def _stage_panel_zoom(count):
        """How far into the plate a stage of `count` panels pushes."""
        table = ENTER_M_PANEL_ZOOM

        if not table:
            return 1.0

        return table.get(max(1, min(count, max(table))), 1.0)

    # THE FRAMING. One source window per panel -- which part of the room that
    # panel is a photograph of.
    #
    # THE WINDOWS ARE DISJOINT. The plate is tiled left to right in panel order,
    # so no two panels can be looking at the same corner of the room. They used
    # to be free to overlap: every window was centred on the middle of the plate
    # and merely nudged toward its character, which at two panels put ~13% of the
    # background inside BOTH of them -- the same chair, the same pot plant,
    # visibly duplicated either side of the cut.
    #
    # It is also what makes the split seamless. Everything below is derived from
    # the CURRENT eased zoom, and at zoom 1.0 there is no free space to spend,
    # no separation and no lean -- so the windows come out exactly equal to the
    # panels' own screen spans, which is the identity mapping. Engagement 0
    # therefore draws the untouched background no matter how many panels exist,
    # and a room that splits appears to CRACK APART from the frame the player
    # was already looking at instead of cutting to a rearranged one.
    def _stage_panel_frames(spans, zoom, amt):
        count = len(spans)
        sizes = [max(right - left, 1e-5) / max(zoom, 0.01)
            for left, right, _x in spans]
        free = max(0.0, 1.0 - sum(sizes))

        # Room deliberately SKIPPED between neighbouring panels: a slice of the
        # plate no panel shows, so two adjacent shots read as two angles on a
        # room rather than one photograph with a line drawn down it. It can only
        # ever spend a share of the free space the zoom actually opened up.
        if count > 1:
            separation = min(
                ENTER_M_PANEL_SEPARATION * amt,
                free * ENTER_M_PANEL_SEP_SHARE / (count - 1))
        else:
            separation = 0.0

        margin = max(0.0, (free - separation * (count - 1)) * 0.5)

        centres = []
        cursor = margin

        for index, size in enumerate(sizes):
            left, right, char_x = spans[index]
            # The lean: a character who is NOT in the middle of their own panel
            # (the speaker's claim widened it, or the sprite was hand-placed)
            # drags their window the same way, so the panel keeps looking at the
            # part of the room they are standing in.
            lean = (char_x - (left + right) * 0.5) * ENTER_M_PANEL_LEAN * amt
            centres.append(cursor + size * 0.5 + lean)
            cursor += size + separation

        # Put anything the lean pushed into a neighbour, or off the plate, back
        # where it fits. Forward pass first, then backward: the backward pass
        # walks right to left reading the neighbour it has already settled, so
        # it cannot undo the forward pass's work. A solution always exists --
        # sum(sizes) + separation * (count - 1) <= 1.0 by construction.
        low = sizes[0] * 0.5

        for index in range(count):
            if index:
                low = (centres[index - 1]
                    + (sizes[index - 1] + sizes[index]) * 0.5 + separation)

            centres[index] = max(centres[index], low)

        high = 1.0 - sizes[-1] * 0.5

        for index in range(count - 1, -1, -1):
            if index < count - 1:
                high = (centres[index + 1]
                    - (sizes[index] + sizes[index + 1]) * 0.5 - separation)

            centres[index] = min(centres[index], high)

        return centres

    def _stage_panels_paint(trans):
        panels = _stage_panels
        amt = _stage_state["amt"]
        live = any(p["alive"] for p in panels)

        if amt <= 0.0015 and not live:
            del panels[:]
            trans.mesh = False
            trans.shader = None
            return None

        width = float(config.screen_width)
        height = float(config.screen_height)

        # Screen spans, left to right. Widths are normalised here rather than in
        # the ease, so a panel opening squeezes its neighbours by exactly the
        # room it takes. When EVERY panel is newborn their shares are all still
        # ~0 and the division says nothing, so the room starts out divided
        # evenly -- and engagement is ~0 on that same frame, so the plate is
        # untouched either way and there is nothing to see yet.
        total = sum(max(p["cw"], 0.0) for p in panels)
        even = 1.0 / max(len(panels), 1)
        spans = []
        cursor = 0.0

        for panel in panels:
            share = (max(panel["cw"], 0.0) / total) if total > 1e-4 else even
            spans.append((cursor, cursor + share, panel["cx"]))
            cursor += share

        if not spans:
            spans.append((0.0, 1.0, 0.5))

        # Belt and braces: _stage_panels_retarget already trims the list, and
        # the uniform block has nowhere to put a seventh panel -- a silently
        # dropped one would leave the right-hand edge of the screen ungoverned.
        del spans[_SP_SHADER_PANELS:]

        # Floating point drift would otherwise leave a hairline of the last
        # panel's gutter down the right-hand edge of the screen.
        first = spans[0]
        last = spans[-1]
        spans[0] = (0.0, first[1], first[2])
        spans[-1] = (last[0], 1.0, last[2])

        count = len(spans)
        zoom = 1.0 + (_stage_panel_zoom(count) - 1.0) * amt
        centres = _stage_panel_frames(spans, zoom, amt)
        values = []

        for index, (left, right, _char_x) in enumerate(spans):
            values.append((
                -1.0 if index == 0 else left,
                2.0 if index == count - 1 else right,
                centres[index],
                (left + right) * 0.5))

        while len(values) < _SP_SHADER_PANELS:
            values.append((3.0, 3.0, 0.5, 0.5))

        # A cut that leans 74px across the screen is a lean of a fifth of a panel
        # at two people and most of a panel at six, so past a certain narrowness
        # the slant comes off proportionally -- otherwise the busiest layouts are
        # the ones whose gutters eat the most of each shot.
        narrowest = min(right - left for left, right, _x in spans) * width
        slant = ENTER_M_PANEL_SLANT * min(
            1.0, narrowest / max(ENTER_M_PANEL_SLANT_FIT, 1.0))

        trans.mesh = True
        trans.shader = "enter_m.stage_panels"
        trans.u_em_sp_screen = (width, height)
        trans.u_em_sp_p0 = values[0]
        trans.u_em_sp_p1 = values[1]
        trans.u_em_sp_p2 = values[2]
        trans.u_em_sp_p3 = values[3]
        trans.u_em_sp_p4 = values[4]
        trans.u_em_sp_p5 = values[5]
        trans.u_em_sp_zoom = zoom
        trans.u_em_sp_gap = (ENTER_M_PANEL_GAP * 0.5 / width) * amt
        trans.u_em_sp_slant = (slant / width) * amt
        trans.u_em_sp_rim = ENTER_M_PANEL_RIM / width
        trans.u_em_sp_edge = ENTER_M_PANEL_EDGE * amt
        trans.u_em_sp_shade = ENTER_M_PANEL_SHADE * amt
        trans.u_em_sp_falloff = ENTER_M_PANEL_FALLOFF / width

        return None if _stage_panels_settled() else 0

    def _stage_panels_drive(trans, st, at):
        if not ENTER_M_STAGE_PANEL_SHADER:
            return None

        _stage_panels_advance()

        return _stage_panels_paint(trans)

    class _StagePanelDriver(object):
        """Picklable stand-in for the driver; resolved by name at call time."""

        def __call__(self, trans, st, at):
            return _stage_panels_drive(trans, st, at)

    def _stage_panels_transform():
        return Transform(function=_StagePanelDriver())


# -----------------------------------------------------------------------------
# 5. LIFECYCLE AND PUBLIC API
# -----------------------------------------------------------------------------
init python:

    def _stage_panels_scope_update():
        try:
            filename = renpy.get_filename_line()[0]
        except Exception:
            return

        if not filename:
            return

        filename = filename.replace("\\", "/")

        for prefix in ENTER_M_PANEL_SCOPE_ON:
            if filename.startswith(prefix):
                _stage_state["scope"] = True
                return

        for prefix in ENTER_M_PANEL_SCOPE_OFF:
            if filename.startswith(prefix):
                _stage_state["scope"] = False
                return

        # Anything else -- a helper label, an addon, a screen -- says nothing
        # about scope, so the latch holds.

    def stage_panels_refresh():
        """Recompute the layout from the current stage. Cheap; idempotent."""
        _stage_panels_scope_update()
        _stage_panels_retarget()
        _stage_panels_wake()

    def stage_panels_set_enabled(enabled):
        """Settings hook. Takes effect on the scene already on screen."""
        persistent.enter_m_panels = bool(enabled)
        stage_panels_refresh()
        renpy.restart_interaction()

    def stage_panels_suspend():
        """Force the format off (nestable) -- for a bespoke sequence."""
        _stage_state["suspend"] += 1
        stage_panels_refresh()

    def stage_panels_resume():
        _stage_state["suspend"] = max(0, _stage_state["suspend"] - 1)
        stage_panels_refresh()

    # The speaker drives the panel emphasis, so it is read from the same
    # "begin" event Autofocus uses. "end" is deliberately ignored for the same
    # reason it is there: holding until the next line is flicker-free.
    def _stage_panels_speaker(event, interact=True, **kwargs):
        if event != "begin":
            return

        tag = renpy.get_say_image_tag()

        if tag is not None and not renpy.showing(tag, layer=_SP_LAYER):
            tag = None

        _stage_state["speaker"] = tag
        stage_panels_refresh()

    def _stage_panels_interact():
        stage_panels_refresh()

    # A `scene` is a cut. Sliding the layout across one reads as a mistake, so
    # the geometry lands instantly and the new shot is simply already framed.
    def _stage_panels_scene(layer):
        if layer != _SP_LAYER:
            return

        _stage_state["speaker"] = None
        _stage_state["snap"] = True
        _stage_state["signature"] = None

    # A load drops a whole new image stack on us and the eased state describes
    # the session we just left. Clear it, re-prove the scope from the statement
    # that resumes, and land the first frame instantly.
    def _stage_panels_after_load():
        del _stage_panels[:]
        _stage_state["amt"] = 0.0
        _stage_state["amt_target"] = 0.0
        _stage_state["speaker"] = None
        _stage_state["scope"] = False
        _stage_state["frame"] = None
        _stage_state["snap"] = True
        _stage_state["signature"] = None

    config.all_character_callbacks.append(_stage_panels_speaker)
    config.start_interact_callbacks.append(_stage_panels_interact)
    config.scene_callbacks.append(_stage_panels_scene)
    config.after_load_callbacks.append(_stage_panels_after_load)


# init 999 (with Autofocus's own tag defaults): claim the `bg` tag. Only a show
# that carries no `at` clause picks this up, so `scene bg x at fx_push(...)`
# keeps opting itself out, and SceneLists.clear() drops it on every `scene` --
# which means the transform is rebuilt per cut and never goes stale.
init 999 python:
    if ENTER_M_STAGE_PANEL_SHADER:
        config.tag_transform.setdefault("bg", _stage_panels_transform())
