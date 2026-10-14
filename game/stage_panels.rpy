# Main-story background panels. A bg-tag shader divides the room into up to
# six views; sprites remain unclipped in front. Larger crowds group neighbors.
# Slot centers in ENTER_M_PANEL_SLOT_X must match transforms.rpy. Source views
# tile left-to-right; eased zoom engages from an unchanged background.
#
# An explicit bg at-list opts out. Master-layer transforms and atmosphere's
# camera remain independent; scene cuts reset panel geometry. Frame-time
# integration advances shared state once even when transitions draw two bgs.
# Season 1 source enables the scope latch; other presentation roots disable
# it; shared helpers leave it alone. stage_panels_suspend/resume override it.
# Settings owns persistent.enter_m_panels via stage_panels_set_enabled().
#
# Shader uniforms u_em_sp_p0..p5 hold (left, right, source center, screen center).
# Unused panels sit outside the screen. Selection uses slanted coordinates;
# source sampling uses unskewed coordinates so the room is not sheared.
# ENTER_M_PANEL_MAX cannot exceed six without extending the shader.
#
# THE CAST LIVES INSIDE THE PANELS (Sep 26 2026). The same cut geometry is
# published every paint as _stage_mask, and story_cast_framing.rpy masks each
# framed sprite to its own panel with enter_m.cast_mask, so a gutter cuts
# through the cast exactly where it cuts the room. Both shaders pick panels by
# SCREEN position (gl_Position, see _EM_SCREEN_VERTEX), not plate position:
# a layer shake moves the room and the cast inside a frame that holds still,
# and the two can never disagree about where a cut is. Per-panel u_em_sp_f*
# carry (listener dim, speaker accent, open glint); _EM_EDGE_LOOK is the one
# seam/shade/dim treatment both shaders apply, so a seam runs unbroken from
# the wall across a shoulder.

init -10 python:

    # Clip space -> screen fraction, top-left origin. Runs after renpy.geometry
    # (vertex_100) has applied u_transform, so it already includes every slot
    # transform, the focus push and any master-layer shake.
    #
    # RENDER-TO-TEXTURE FLIPS Y (measured Sep 26 2026). Drawing into a texture
    # -- every dissolve renders both scenes that way -- inverts the projection's
    # y, and the documented `-gl_Position.y * .5 + .5` then puts the top of the
    # screen at the bottom: mid-dissolve the gutters leaned the wrong way and
    # their signal marks sat at the foot of the frame. Model y (down the image)
    # maps to clip -y on screen and to clip +y into a texture, so the sign of
    # u_transform[1][1] says which, for anything drawn upright.
    _EM_SCREEN_VERTEX = """
            {v} = vec2(0.5 + 0.5 * gl_Position.x / gl_Position.w,
                       0.5 - 0.5 * sign(-u_transform[1][1]) * gl_Position.y / gl_Position.w);
    """

    # THE EDGE LOOK, shared by the room and the cast. Inputs: {d} distance to
    # this panel's nearer cut (skewed screen fraction), {y} screen y, {fx}
    # (listener dim, speaker accent, open glint), {acc} the speaker's voice
    # colour, {col} straight colour. The seam is the ENTER M coachwork line from
    # the dialogue box: a bright inner hairline plus a faint second rule, cyan,
    # burning hottest at the top of the frame and cooling toward the text. The
    # live speaker's panel runs it in their own colour (ENTER_M_PANEL_VOICE),
    # with a soft {glow} of it thrown into the shot. Listener panels desaturate
    # and fall back as one camera.
    _EM_EDGE_LOOK = """
            float {p}aa = 0.0014;
            float {p}cut = 1.0 - smoothstep(max({gap} - {p}aa, 0.0), {gap} + {p}aa, {d});
            float {p}sh = 1.0 - smoothstep({gap}, {gap} + max({falloff}, 0.001), {d});
            float {p}sm = (1.0 - smoothstep({gap}, {gap} + max({rim}, 0.0005), {d})) * (1.0 - {p}cut);
            float {p}s2 = smoothstep({gap} + 3.4 * {rim}, {gap} + 4.2 * {rim}, {d})
                - smoothstep({gap} + 4.6 * {rim}, {gap} + 5.4 * {rim}, {d});
            float {p}prof = mix(1.0, 0.28, smoothstep(0.04, 0.82, {y}));
            vec3 {p}sc = mix(vec3(0.51, 0.84, 0.86), {acc}, {fx}.y);
            float {p}gain = {edge} * {p}prof * (1.0 + 1.1 * {fx}.y + 2.6 * {fx}.z) * {fade};
            float {p}lum = dot({col}, vec3(0.299, 0.587, 0.114));
            {col} = mix({col}, vec3({p}lum) * vec3(0.90, 0.97, 1.06), 0.38 * {fx}.x);
            {col} *= 1.0 - 0.40 * {fx}.x;
            {col} *= 1.0 - {p}sh * {shade} * {fade};
            {col} += {p}sc * ({p}sm + 0.32 * {p}s2) * {p}gain;
            float {p}gl = exp(-max({d} - {gap}, 0.0) / 0.011) * (1.0 - {p}cut);
            {col} += {acc} * {p}gl * {glow} * {fx}.y * {p}prof * {fade};
    """

    def _em_edge_look(prefix, **names):
        names["p"] = prefix
        return _EM_EDGE_LOOK.format(**names)

    def _enter_m_stage_panels_register_shader():
        renpy.register_shader("enter_m.stage_panels", variables="""
            uniform sampler2D tex0;
            uniform mat4  u_transform;
            uniform vec2  u_model_size;
            uniform vec2  u_em_sp_screen;
            uniform vec4  u_em_sp_p0;
            uniform vec4  u_em_sp_p1;
            uniform vec4  u_em_sp_p2;
            uniform vec4  u_em_sp_p3;
            uniform vec4  u_em_sp_p4;
            uniform vec4  u_em_sp_p5;
            uniform vec3  u_em_sp_f0;
            uniform vec3  u_em_sp_f1;
            uniform vec3  u_em_sp_f2;
            uniform vec3  u_em_sp_f3;
            uniform vec3  u_em_sp_f4;
            uniform vec3  u_em_sp_f5;
            uniform vec3  u_em_sp_c0;
            uniform vec3  u_em_sp_c1;
            uniform vec3  u_em_sp_c2;
            uniform vec3  u_em_sp_c3;
            uniform vec3  u_em_sp_c4;
            uniform vec3  u_em_sp_c5;
            uniform float u_em_sp_zoom;
            uniform float u_em_sp_gap;
            uniform float u_em_sp_slant;
            uniform float u_em_sp_rim;
            uniform float u_em_sp_edge;
            uniform float u_em_sp_shade;
            uniform float u_em_sp_falloff;
            uniform float u_em_sp_tick;
            uniform float u_em_sp_push;
            uniform float u_em_sp_glow;
            varying vec2  v_tex_coord;
            varying vec2  v_em_sp_scr;
        """, vertex_300=_EM_SCREEN_VERTEX.format(v="v_em_sp_scr"), fragment_300="""
            // Child pixels -> plate fraction, for SAMPLING. Every background in
            // the story is 1280x720 at the origin, so this is the identity
            // there; an odd-sized plate degrades to the right scale.
            vec2 em_sp_size = max(u_model_size, vec2(1.0));
            vec2 em_sp_screen = max(u_em_sp_screen, vec2(1.0));
            vec2 em_sp_ratio = em_sp_size / em_sp_screen;
            vec2 em_sp_suv = v_tex_coord * em_sp_ratio;

            // Panel SELECTION is in screen space; see the header.
            vec2 em_sp_scr = v_em_sp_scr;
            float em_sp_xs = em_sp_scr.x + (em_sp_scr.y - 0.5) * u_em_sp_slant;

            vec4 em_sp_pan = u_em_sp_p0;
            vec3 em_sp_fx = u_em_sp_f0;
            vec3 em_sp_acc = u_em_sp_c0;
            if (em_sp_xs >= u_em_sp_p1.x) { em_sp_pan = u_em_sp_p1; em_sp_fx = u_em_sp_f1; em_sp_acc = u_em_sp_c1; }
            if (em_sp_xs >= u_em_sp_p2.x) { em_sp_pan = u_em_sp_p2; em_sp_fx = u_em_sp_f2; em_sp_acc = u_em_sp_c2; }
            if (em_sp_xs >= u_em_sp_p3.x) { em_sp_pan = u_em_sp_p3; em_sp_fx = u_em_sp_f3; em_sp_acc = u_em_sp_c3; }
            if (em_sp_xs >= u_em_sp_p4.x) { em_sp_pan = u_em_sp_p4; em_sp_fx = u_em_sp_f4; em_sp_acc = u_em_sp_c4; }
            if (em_sp_xs >= u_em_sp_p5.x) { em_sp_pan = u_em_sp_p5; em_sp_fx = u_em_sp_f5; em_sp_acc = u_em_sp_c5; }

            // This panel's window onto the room: its own centre of the source
            // plate, scaled about that centre. Python has already clamped the
            // centre so the window cannot run off the edge of the plate.
            float em_sp_zoom = max(u_em_sp_zoom, 0.01);

            // The live panel's camera pushes in a little, about the cast's eye
            // height, so the speaker's room tightens while the rest hold.
            float em_sp_k = 1.0 + u_em_sp_push * em_sp_fx.y;
            vec2 em_sp_pivot = vec2(em_sp_pan.w, 0.40);
            vec2 em_sp_q = em_sp_pivot + (em_sp_suv - em_sp_pivot) / em_sp_k;
            vec2 em_sp_src = vec2(
                em_sp_pan.z + (em_sp_q.x - em_sp_pan.w) / em_sp_zoom,
                0.5 + (em_sp_q.y - 0.5) / em_sp_zoom);
            vec2 em_sp_uv = clamp(
                em_sp_src / em_sp_ratio, vec2(0.0005), vec2(0.9995));

            vec4 em_sp_tex = texture2D(tex0, em_sp_uv);
            float em_sp_a = max(em_sp_tex.a, 0.0001);
            vec3 em_sp_col = em_sp_tex.rgb / em_sp_a;

            // Distance to the nearer edge of this panel, in the skewed x.
            float em_sp_d = min(em_sp_xs - em_sp_pan.x, em_sp_pan.y - em_sp_xs);
            float em_sp_gap = max(u_em_sp_gap, 0.0);
            """ + _em_edge_look("em_sp_e_", d="em_sp_d", y="em_sp_scr.y", fx="em_sp_fx",
            acc="em_sp_acc", col="em_sp_col", gap="em_sp_gap", rim="u_em_sp_rim",
            edge="u_em_sp_edge", shade="clamp(u_em_sp_shade, 0.0, 1.0)",
            falloff="u_em_sp_falloff", glow="u_em_sp_glow", fade="1.0") + """
            // The gutter is graphite, carrying the dialogue box's signal
            // marks near the top of every cut -- a cyan bar and a short
            // crimson one, down the centre third of the gutter.
            float em_sp_mid = 1.0 - smoothstep(em_sp_gap * 0.34, em_sp_gap * 0.52, em_sp_d);
            float em_sp_t1 = smoothstep(0.052, 0.056, em_sp_scr.y) * (1.0 - smoothstep(0.112, 0.116, em_sp_scr.y));
            float em_sp_t2 = smoothstep(0.126, 0.130, em_sp_scr.y) * (1.0 - smoothstep(0.146, 0.150, em_sp_scr.y));
            vec3 em_sp_gutter = vec3(0.025, 0.038, 0.047);
            vec3 em_sp_mark = mix(vec3(0.44, 0.77, 0.82), em_sp_acc, em_sp_fx.y);
            em_sp_gutter = mix(em_sp_gutter, em_sp_mark, em_sp_mid * em_sp_t1 * u_em_sp_tick);
            em_sp_gutter = mix(em_sp_gutter, vec3(0.85, 0.47, 0.48), em_sp_mid * em_sp_t2 * u_em_sp_tick);
            em_sp_col = mix(em_sp_col, em_sp_gutter, em_sp_e_cut);

            gl_FragColor = vec4(em_sp_col * em_sp_a, em_sp_a);
        """)

        # THE CAST MASK. Applied by story_cast_framing.rpy to a framed story
        # sprite's Render (no mesh: the part rides the sprite's own texture
        # draw, so this costs no render-to-texture). u_em_cm_edge is (left
        # cut, right cut, slant, half gutter); u_em_cm_fx is (dim, accent,
        # glint, slack). Slack pushes the cuts outward -- the speaker breaking
        # the frame, or the whole layout disengaging -- and fades the edge
        # treatment with it, so an open frame carries no seam across a face.
        renpy.register_shader("enter_m.cast_mask", variables="""
            uniform mat4  u_transform;
            uniform vec4  u_em_cm_edge;
            uniform vec4  u_em_cm_look;
            uniform vec4  u_em_cm_fx;
            uniform vec3  u_em_cm_acc;
            uniform float u_em_cm_glow;
            varying vec2  v_em_cm_scr;
        """, vertex_300=_EM_SCREEN_VERTEX.format(v="v_em_cm_scr"), fragment_300="""
            float em_cm_xs = v_em_cm_scr.x + (v_em_cm_scr.y - 0.5) * u_em_cm_edge.z;
            float em_cm_d = min(em_cm_xs - u_em_cm_edge.x, u_em_cm_edge.y - em_cm_xs);
            float em_cm_gap = max(u_em_cm_edge.w, 0.0);
            float em_cm_slack = max(u_em_cm_fx.w, 0.0);
            float em_cm_keep = smoothstep(max(em_cm_gap - 0.0014, 0.0),
                em_cm_gap + 0.0014, em_cm_d + em_cm_slack);
            float em_cm_fade = 1.0 - smoothstep(0.0, 0.006, em_cm_slack);
            float em_cm_a = max(gl_FragColor.a, 0.0001);
            vec3 em_cm_col = gl_FragColor.rgb / em_cm_a;
            vec3 em_cm_fx3 = u_em_cm_fx.xyz;
            """ + _em_edge_look("em_cm_e_", d="em_cm_d", y="v_em_cm_scr.y", fx="em_cm_fx3",
            acc="u_em_cm_acc", col="em_cm_col", gap="em_cm_gap", rim="u_em_cm_look.x",
            edge="u_em_cm_look.y", shade="u_em_cm_look.z",
            falloff="u_em_cm_look.w", glow="u_em_cm_glow",
            fade="em_cm_fade") + """
            gl_FragColor = vec4(em_cm_col * em_cm_a, em_cm_a) * em_cm_keep;
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
define ENTER_M_PANEL_GAP = 12.0       # gutter width in px at full engagement
define ENTER_M_PANEL_SLANT = 74.0     # px the cut leans across the screen height
define ENTER_M_PANEL_SLANT_FIT = 340.0  # panels narrower than this lean less
define ENTER_M_PANEL_RIM = 1.5        # px of the seam's bright inner hairline
define ENTER_M_PANEL_EDGE = 0.50      # how bright the seam burns at the top
define ENTER_M_PANEL_SHADE = 0.26     # how dark the plate goes into the gutter
define ENTER_M_PANEL_FALLOFF = 22.0   # px that shading reaches into the panel
define ENTER_M_PANEL_TICK = 1.0       # the cyan/crimson signal marks in each gutter
define ENTER_M_PANEL_GLOW = 0.30      # voice-coloured light the live seam throws in
define ENTER_M_PANEL_PUSH = 0.03      # how far the live panel's camera pushes in

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
# hand-placed sprite). 0 frames every panel dead centre. This is the SMALL-OFFSET
# gain; _stage_panel_frames caps it so the lean can never run out of room before
# the character reaches their panel's edge (see the note there).
define ENTER_M_PANEL_LEAN = 0.55

define ENTER_M_PANEL_EXPAND = 0.036   # extra width the speaker's panel claims

# THE LIVE CAMERA. While someone on stage is speaking, every other panel -- room
# AND sprite, one grade for both -- falls back, and the speaker's own seams run
# crimson. DIM scales the fall-back; it only applies while Speaker Focus is on
# "Darken" (the panel then does Autofocus's darkening for framed story sprites,
# see story_cast_framing.rpy), so "Fade" and "Off" keep their exact behaviour.
# BREAKOUT is how far, in px, the speaker's figure may cross their own cuts:
# the comic-panel pop-out. FOCUS is the time constant all three ease on.
define ENTER_M_PANEL_DIM = 1.0
define ENTER_M_PANEL_BREAKOUT = 30.0
define ENTER_M_PANEL_FOCUS = 0.085

# A cut glints as its panel opens or closes, and every cut glints as the whole
# layout cracks open from a plain background.
define ENTER_M_PANEL_GLINT = 1.0

# VOICE COLOURS. The live speaker's seams burn in their own colour, taken from
# their art, so a character is recognisable by the edge of their shot before
# the name box is read. Anyone unlisted speaks in the interface crimson.
define ENTER_M_PANEL_VOICE = {
    "matsuda": "#ff4b55",
    "monika": "#4fe08e",
    "kotonoha": "#b69cff",
    "sam": "#ffc849",
    "asahina": "#5fb2ff",
    "tsubaki": "#f3b25e",
    "mom": "#ff907a",
    "mc": "#a8bdd2",
}
define ENTER_M_PANEL_VOICE_DEFAULT = "#ff315b"

# THE EXIT SLIDE. How far past the frame the last cut is carried as the panel
# beyond it finishes collapsing, as a fraction of the screen. A cut that merely
# converges ON the edge still shows its gutter and its 26px of shading INSIDE
# the frame, and then loses them all at once when the panel is finally dropped;
# this is the extra distance that takes the whole gutter -- half the gap, the
# falloff, and the slant's own excursion (about 71px together) -- off-screen
# before that happens.
define ENTER_M_PANEL_EXIT = 0.12

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

# A character MOVING between slots (t11 -> t31) is not a correction, it is the
# sprite gliding, and the room should pan with it rather than get there first.
# So a panel whose character changes position follows tcommon's own curve --
# `easein_cubic .30` in game/transforms.rpy, fast start and decelerating --
# instead of the exponential above. Keep this equal to that duration.
define ENTER_M_PANEL_GLIDE = 0.30

# SCOPE. Prefixes are matched against the filename of the running statement.
# Loose scripts report `game/...`; archived scripts report the path INSIDE the
# archive (without `game/`), and protected bundles lowercase that path. Section
# 5 canonicalises all three forms before matching. ON wins over OFF; anything in
# neither list leaves the latch where it is, so a `call` into a shared helper
# label cannot strobe the layout.
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

    # The cut geometry as of the last paint, for the cast mask. `panels` maps
    # every cast tag on stage (group members included) to
    # (left cut, right cut, (dim, accent, glint), slack, width).
    _stage_mask = {"on": False, "t": None, "panels": {},
        "edge": (0.0, 0.0), "look": (0.0, 0.0, 0.0, 0.0)}

    # Called whenever the layout gets a new target, after the bg is woken:
    # anything else drawn from this geometry (the cast mask) must redraw too.
    _stage_panels_wake_hooks = []

    def _stage_mask_for(tag):
        if not _stage_mask["on"]:
            return None

        return _stage_mask["panels"].get(tag)

    def _stage_panel_voice(tag):
        """A speaker's seam colour as a straight 0..1 RGB triple."""
        return tuple(Color(ENTER_M_PANEL_VOICE.get(
            tag, ENTER_M_PANEL_VOICE_DEFAULT)).rgb)

    def _stage_panel_dim_strength():
        if not getattr(store, "autofocus_enabled", False):
            return 0.0

        if persistent.autofocus_dim_mode != "darken":
            return 0.0

        return float(ENTER_M_PANEL_DIM)

    _stage_state = {
        "amt": 0.0,          # engagement 0..1: gutters, zoom and parallax ride it
        "amt_target": 0.0,
        "speaker": None,
        "scope": False,      # is the running statement inside the main story
        "suspend": 0,        # manual override depth
        "frame": None,       # last frame_time the ease advanced on
        "snap": False,       # next advance lands instantly (cut, load, restage)
        "signature": None,   # last target set handed to the driver
        # HOW FAR THE PLATE IS PUSHED INTO, AND HOW HARD THE CUTS LEAN. Both are
        # properties of the SETTLED layout (see _stage_panels_retarget), eased
        # like everything else rather than read off the live panel list -- a
        # panel that is opening or collapsing is momentarily the narrowest thing
        # on screen and the whole layout used to follow it there. See the note
        # on the ease below.
        "zoomv": 1.0,        # eased ENTER_M_PANEL_ZOOM for the live stage
        "zoom_target": 1.0,
        "narrowv": 1.0,      # eased narrowest TARGET panel, as a screen fraction
        "narrow_target": 1.0,
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
        return [(x, tag) for x, tag, _members in _stage_panel_group_members(stage)]

    # The same grouping, remembering who is in each panel: the speaker may be a
    # merged panel's second member, and the cast mask needs every member.
    def _stage_panel_group_members(stage):
        limit = _stage_panel_limit()

        if len(stage) <= limit:
            return [(x, tag, [tag]) for x, tag in stage]

        groups = [[x, tag, 1, [tag]] for x, tag in stage]

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
            left[3].extend(right[3])

        return [(x, tag, members) for x, tag, _count, members in groups]

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

    def _stage_panel_retire(panel):
        """Mark a panel dead, remembering the width it is leaving FROM.

        `ref` is frozen here and nowhere else, so _stage_panel_exit can report
        progress through the exit as a clean 0..1 no matter how wide the panel
        happened to be when its character was hidden. A panel that is already
        dead keeps the ref it was retired with -- retargeting again while it
        collapses must not restart its exit.
        """
        if panel["alive"]:
            panel["ref"] = max(panel["cw"], 1e-4)
            panel["alive"] = False

        panel["w"] = 0.0
        # A leaving panel stops being the speaker's; a dimmed listener who
        # leaves stays dim on the way out rather than flashing back up.
        panel["acc_t"] = 0.0
        panel["out_t"] = 0.0

    def _stage_panel_exit(panel):
        """0 the moment a panel is retired, 1 once it has finished collapsing.

        Live panels never slide: an established panel that is merely resizing
        (everyone widens when someone leaves) must not be read as leaving, and a
        newborn does not need it -- one frame of the ease already carries its
        cut 86px in from the edge, while a dying panel's exponential tail parks
        its cut ON the edge for the better part of half a second.
        """
        if panel["alive"]:
            return 0.0

        ref = max(panel.get("ref", 0.0), 1e-4)

        return min(1.0, max(0.0, 1.0 - panel["cw"] / ref))

    def _stage_panels_retarget():
        """Re-derive every panel's target from who is on stage right now."""
        stage = _stage_panels_scan() if _stage_panels_active() else []
        grouped = _stage_panel_group_members(stage) if stage else []
        stage = [(x, tag) for x, tag, _members in grouped]

        if not stage:
            # Nobody on stage: every panel dies and the plate returns to being a
            # plain background, at which point the shader takes itself off.
            _stage_state["amt_target"] = 0.0

            for panel in _stage_panels:
                _stage_panel_retire(panel)

            _stage_panels_wake()

            return

        _stage_state["amt_target"] = 1.0

        speaker = _stage_state["speaker"]
        widths = _stage_panel_widths(stage, speaker)

        # Which panel is live. A speaker who shares a merged panel lights the
        # whole panel; a speaker with no panel (off stage) lights nobody's.
        speaker_index = None

        # Speaker Focus switched off means no speaker emphasis at all: no
        # listener dim, no live seam, no pop-out, no push-in.
        emphasis = bool(getattr(store, "autofocus_enabled", True))

        for index, (_x, _tag, members) in enumerate(grouped):
            if emphasis and speaker is not None and speaker in members:
                speaker_index = index
                break

        dim = _stage_panel_dim_strength() if speaker_index is not None else 0.0
        breakout = float(ENTER_M_PANEL_BREAKOUT) if len(stage) > 1 else 0.0

        # The framing targets belong to the stage that is ARRIVING, so they are
        # read from the live cast and its settled widths -- never from the panel
        # list, which also carries whatever is still collapsing.
        _stage_state["zoom_target"] = _stage_panel_zoom(len(stage))
        _stage_state["narrow_target"] = min(widths) if widths else 1.0

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
                        "alive": True, "ref": 0.0}
                _stage_panels.append(panel)
            elif abs(panel["x"] - x) > 1e-6:
                # The character moved. Glide from wherever the panel is NOW
                # (which may be partway through an earlier glide) on the
                # sprite's own curve; the clock starts on the next drawn frame
                # -- see _stage_panels_advance for why not here.
                panel["x0"] = panel["cx"]
                panel["t0"] = None
                panel["glide"] = True

            panel["x"] = x
            panel["w"] = widths[index]
            panel["alive"] = True
            panel["members"] = tuple(grouped[index][2])
            speaking = index == speaker_index
            panel["dim_t"] = 0.0 if speaking else dim

            # The colour is only ever SET: a panel whose speaker falls silent
            # keeps it while its accent fades, so it cools rather than flicks.
            if speaking:
                panel["voice"] = _stage_panel_voice(speaker)
            panel["acc_t"] = 1.0 if speaking and len(stage) > 1 else 0.0
            panel["out_t"] = breakout if speaking else 0.0
            # Identity, not equality: two panels with the same contents are
            # equal as dicts, and `panel in keep` would then keep the wrong one.
            keep.add(id(panel))

        for panel in _stage_panels:
            if id(panel) not in keep:
                _stage_panel_retire(panel)

        # Left to right by where each panel IS, dying panels included, so a
        # panel collapses in place. Current position, not target: two
        # characters swapping sides used to trade panels on the first frame --
        # the whole room jumped 62px -- whereas ordered by position they keep
        # their panels until the glide actually carries them past each other,
        # and the order is kept up to date per frame in _stage_panels_advance.
        _stage_panels.sort(key=lambda p: p["cx"])

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
            tuple((p["tag"], p["alive"], round(p["w"], 4), round(p["x"], 4),
                round(p.get("dim_t", 0.0), 3), round(p.get("acc_t", 0.0), 3),
                round(p.get("out_t", 0.0), 2))
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

        for hook in _stage_panels_wake_hooks:
            try:
                hook()
            except Exception:
                pass

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
            focus = 1.0
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
            focus = 1.0 - _enter_m_sp_math.exp(
                -delta / max(ENTER_M_PANEL_FOCUS, 0.001))

        if blend <= 0.0:
            return

        snapping = _stage_state["snap"]
        _stage_state["snap"] = False
        _stage_state["amt"] += (
            _stage_state["amt_target"] - _stage_state["amt"]) * opening

        _stage_state["zoomv"] += (
            _stage_state["zoom_target"] - _stage_state["zoomv"]) * blend
        _stage_state["narrowv"] += (
            _stage_state["narrow_target"] - _stage_state["narrowv"]) * blend

        for panel in _stage_panels:
            panel["cw"] += (panel["w"] - panel["cw"]) * blend

            for key in ("dim", "acc", "out"):
                value = panel.get(key, 0.0)
                panel[key] = value + (panel.get(key + "_t", 0.0) - value) * focus

            if not panel.get("glide"):
                panel["cx"] += (panel["x"] - panel["cx"]) * blend
                continue

            if snapping or now is None:
                panel["cx"] = panel["x"]
                panel["glide"] = False
                continue

            # THE GLIDE CLOCK STARTS HERE, NOT IN _stage_panels_retarget. That
            # runs at interaction start, when the last drawn frame can be a
            # whole line of dialogue old (Low-Resource Mode presents every
            # 200ms), and a start time that stale would put the first frame
            # most of the way through the move -- the snap all over again. So
            # the move is dated one frame back from the first frame that draws
            # it, the same single-frame clamp the ease above uses.
            if panel.get("t0") is None:
                step = min(now - last, 1.0 / 30.0) if last is not None else 1.0 / 60.0
                panel["t0"] = now - step

            progress = (now - panel["t0"]) / max(ENTER_M_PANEL_GLIDE, 0.001)

            if progress >= 1.0:
                panel["cx"] = panel["x"]
                panel["glide"] = False
            else:
                # easein_cubic, Matsu'Py's naming: fast out of the gate,
                # settling into place -- the same curve the sprite is on.
                eased = 1.0 - (1.0 - progress) ** 3
                panel["cx"] = panel["x0"] + (panel["x"] - panel["x0"]) * eased

        for panel in list(_stage_panels):
            if not panel["alive"] and panel["cw"] <= 0.0015:
                _stage_panels.remove(panel)

        # Keep the row in the order the panels actually stand in. A swap
        # crosses over mid-glide, on a frame where both characters are at the
        # same x -- so the handover is continuous rather than a jump.
        _stage_panels.sort(key=lambda p: p["cx"])

    def _stage_panels_settled():
        if abs(_stage_state["amt_target"] - _stage_state["amt"]) > 0.0015:
            return False

        if abs(_stage_state["zoom_target"] - _stage_state["zoomv"]) > 0.0004:
            return False

        if abs(_stage_state["narrow_target"] - _stage_state["narrowv"]) > 0.0015:
            return False

        for panel in _stage_panels:
            if abs(panel["w"] - panel["cw"]) > 0.0015:
                return False

            if abs(panel["x"] - panel["cx"]) > 0.0015:
                return False

            if abs(panel.get("dim_t", 0.0) - panel.get("dim", 0.0)) > 0.002:
                return False

            if abs(panel.get("acc_t", 0.0) - panel.get("acc", 0.0)) > 0.002:
                return False

            if abs(panel.get("out_t", 0.0) - panel.get("out", 0.0)) > 0.05:
                return False

            # The cubic's tail spends its last ~50ms inside the tolerance
            # above; a driver that fell asleep there would finish the glide
            # with a jump on whatever frame woke it.
            if panel.get("glide"):
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
    def _stage_panel_frames(spans, zoom, amt, presence=None):
        count = len(spans)
        sizes = [max(right - left, 1e-5) / max(zoom, 0.01)
            for left, right, _x in spans]
        free = max(0.0, 1.0 - sum(sizes))

        # Room deliberately SKIPPED between neighbouring panels: a slice of the
        # plate no panel shows, so two adjacent shots read as two angles on a
        # room rather than one photograph with a line drawn down it. It can only
        # ever spend a share of the free space the zoom actually opened up.
        #
        # ONE GAP PER BOUNDARY, NOT ONE SEPARATION FOR THE WHOLE ROW. `count`
        # is a step function -- a panel that is collapsing is still one of them
        # right up until it is dropped -- so a single shared separation, charged
        # `count - 1` times against the margin, redistributed itself across
        # every surviving gap on the one frame a ghost left the list. Measured
        # 47px of plate lurching sideways, three quarters of a second after the
        # character had walked off: the pop at the end of an exit.
        #
        # THE TOTAL is one separation per REAL boundary, and the number of real
        # boundaries is `sum(presence) - 1` -- a count that slides from 4 to 3
        # as a panel goes instead of stepping. At rest that is exactly the old
        # `separation * (count - 1)`.
        #
        # THE SHAPE comes from prefix/suffix presence, NOT from the two panels
        # either side. A dying panel does not always sit at the end of the row:
        # a survivor's slot slides ACROSS the ghosts on its way to a new centre,
        # so a layout is routinely [live, ghost, ghost, live, ghost], where the
        # first three slots are all really the ONE boundary between the two
        # survivors and only the last hangs off the end with nothing beyond it.
        # min() of the two neighbours reads every one of those as unreal and
        # collapsed the whole budget to nothing (measured 54px). Asking instead
        # whether anything substantial survives on EACH SIDE of a slot gets it
        # right: interior slots stay real and share the budget -- they are
        # stacked at one point once the ghosts reach zero width, so their sum is
        # the single gap that replaces them -- while an end slot goes to zero.
        if presence is None:
            presence = [1.0] * count

        prefix = []
        suffix = [0.0] * count
        run = 0.0

        for index in range(count):
            run = max(run, presence[index])
            prefix.append(run)

        run = 0.0

        for index in range(count - 1, -1, -1):
            run = max(run, presence[index])
            suffix[index] = run

        # Each slot is worth the average presence of the two panels it parts,
        # gated by whether anything substantial survives on each side of it.
        # The average is what makes a RUN of slots add up correctly: two ghosts
        # of presence p between the same pair of survivors give slots of
        # (1+p)/2, p and (p+1)/2, which sum to 1 + 2p -- three boundaries when
        # they are real panels, ONE once they have collapsed onto a single
        # point. The min() gate is what zeroes a slot with nothing but ghosts
        # beyond it, which is a gap spent off the end of the row. Taking one or
        # the other alone leaves a step of a third of a gap (24px measured) on
        # the frame the ghosts are dropped; at rest both are 1 and every slot is
        # worth exactly one separation, as before.
        weights = [
            (presence[i] + presence[i + 1]) * 0.5
                * min(prefix[i], suffix[i + 1])
            for i in range(count - 1)]
        spread = sum(weights)
        budget = min(
            ENTER_M_PANEL_SEPARATION * amt * max(0.0, sum(presence) - 1.0),
            free * ENTER_M_PANEL_SEP_SHARE)

        if spread > 1e-6:
            gaps = [budget * (weight / spread) for weight in weights]
        else:
            gaps = [0.0] * max(count - 1, 0)

        margin = max(0.0, (free - budget) * 0.5)

        centres = []
        cursor = margin

        for index, size in enumerate(sizes):
            left, right, char_x = spans[index]
            # The lean: a character who is NOT in the middle of their own panel
            # (the speaker's claim widened it, or the sprite was hand-placed)
            # drags their window the same way, so the panel keeps looking at the
            # part of the room they are standing in.
            #
            # SCALED BY PRESENCE, or a panel that is no longer there hijacks the
            # ones that are. A dying panel keeps its character's old position
            # while its span collapses to a sliver somewhere else entirely --
            # a slot at 0.70 with a span centred on 0.50 leans by 0.11 of the
            # whole plate -- and the clamp passes below then push that straight
            # into its neighbours. Measured on a 5 -> 2 exit: the surviving
            # right-hand panel was looking 54px off, and snapped back the frame
            # the ghosts were dropped. A panel with no width has nothing to
            # look at, so it gets no say in where anything points.
            #
            # CAPPED SO IT CANNOT RUN OUT OF ROOM MID-MOVE. The whole row can
            # only shift by `margin` before the clamp passes below pin it to
            # the plate edge, and with one person on stage (zoom 1.10) that is
            # 4.5% of the plate. At the raw 0.55 gain a character used all of
            # it after crossing a tenth of the way from t11 to t31 -- two
            # frames into a 0.3s glide -- so the room lurched 64px and then sat
            # pinned while the sprite was still travelling: the "background
            # snaps instead of panning" bug. The gain is therefore limited to
            # margin / reach, where reach is half the panel: a character only
            # spends the full margin when standing at their panel's very edge,
            # and the pan stays proportional to where they are all the way
            # there. Multi-panel stages, whose offsets are small (the
            # speaker's claim), mostly keep the raw gain.
            reach = max((right - left) * 0.5, 1e-4)
            gain = min(ENTER_M_PANEL_LEAN, margin / reach)
            lean = ((char_x - (left + right) * 0.5)
                * gain * amt * presence[index])
            centres.append(cursor + size * 0.5 + lean)
            cursor += size

            if index < count - 1:
                cursor += gaps[index]

        # Put anything the lean pushed into a neighbour, or off the plate, back
        # where it fits. Forward pass first, then backward: the backward pass
        # walks right to left reading the neighbour it has already settled, so
        # it cannot undo the forward pass's work. A solution always exists --
        # sum(sizes) is 1/zoom, sum(gaps) is capped at a share of the free space
        # the zoom opened, so sum(sizes) + sum(gaps) < 1.0 by construction.
        low = sizes[0] * 0.5

        for index in range(count):
            if index:
                low = (centres[index - 1]
                    + (sizes[index - 1] + sizes[index]) * 0.5 + gaps[index - 1])

            centres[index] = max(centres[index], low)

        high = 1.0 - sizes[-1] * 0.5

        for index in range(count - 1, -1, -1):
            if index < count - 1:
                high = (centres[index + 1]
                    - (sizes[index] + sizes[index + 1]) * 0.5 - gaps[index])

            centres[index] = min(centres[index], high)

        return centres

    def _stage_panels_paint(trans):
        panels = _stage_panels
        amt = _stage_state["amt"]
        live = any(p["alive"] for p in panels)

        if amt <= 0.0015 and not live:
            del panels[:]
            _stage_mask["on"] = False
            _stage_mask["panels"] = {}
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

        exits = []

        for panel in panels:
            share = (max(panel["cw"], 0.0) / total) if total > 1e-4 else even
            spans.append((cursor, cursor + share, panel["cx"]))
            exits.append(_stage_panel_exit(panel))
            cursor += share

        if not spans:
            spans.append((0.0, 1.0, 0.5))
            exits.append(0.0)

        # Belt and braces: _stage_panels_retarget already trims the list, and
        # the uniform block has nowhere to put a seventh panel -- a silently
        # dropped one would leave the right-hand edge of the screen ungoverned.
        del spans[_SP_SHADER_PANELS:]
        del exits[_SP_SHADER_PANELS:]

        # Floating point drift would otherwise leave a hairline of the last
        # panel's gutter down the right-hand edge of the screen.
        first = spans[0]
        last = spans[-1]
        spans[0] = (0.0, first[1], first[2])
        spans[-1] = (last[0], 1.0, last[2])

        count = len(spans)

        # HOW MUCH OF A PANEL IS ACTUALLY THERE, 0..1. A settled layout never
        # produces one narrower than ENTER_M_PANEL_MIN_W (_stage_panel_widths
        # floors it), so anything under that is necessarily mid-transition and
        # is counted in proportionally. Resizing panels stay at 1 throughout --
        # only the one that is arriving or leaving fades -- which is what makes
        # this safe to hang the framing budget on.
        presence = [
            min(1.0, (right - left) / max(ENTER_M_PANEL_MIN_W, 1e-4))
            for left, right, _x in spans]

        # ZOOM RIDES THE EASE, NOT THE PANEL COUNT. `spans` still carries every
        # panel that is collapsing, so len(spans) is a step function that only
        # falls when the last ghost is finally dropped -- three quarters of a
        # second after the character actually left, and a whole ZOOM step in a
        # single frame. That was the pop on an exit. zoomv is the same table
        # read against the LIVE stage and eased, so the plate pushes in and out
        # as one continuous move that starts when the cast changes.
        # Still multiplied by amt, so zoom is exactly 1.0 -- the identity, and
        # the reason a split is seamless -- whenever the layout is retracted.
        zoom = 1.0 + (_stage_state["zoomv"] - 1.0) * amt
        centres = _stage_panel_frames(spans, zoom, amt, presence)

        # THE EXIT SLIDE. A cut whose whole remaining row is on its way out has
        # nothing left to divide, so it leaves the frame rather than converging
        # on the edge and parking there. Without this the last gutter ends up
        # against the screen edge with its shading still inside the picture and
        # then vanishes in one frame -- the border that "doesn't go completely
        # out before it pops".
        #
        # out_r[i] is how far gone EVERY panel to the right of boundary i is
        # (product, so one panel that is staying puts a hard stop on it), out_l
        # the mirror. A ghost between two live panels therefore never slides:
        # its two cuts converge and merge into the one boundary that replaces
        # them, which is already seamless. Both products are empty at the outer
        # ends, i.e. 1, which is the -1.0 / 2.0 overhang the format already had.
        edges = [spans[0][0]] + [right for _l, right, _x in spans]
        out_r = [1.0] * (count + 1)
        out_l = [1.0] * (count + 1)

        for index in range(count - 1, -1, -1):
            out_r[index] = out_r[index + 1] * exits[index]

        for index in range(1, count + 1):
            out_l[index] = out_l[index - 1] * exits[index - 1]

        # Monotonic by construction: out_r only ever falls left to right and
        # out_l only ever falls right to left, so no boundary can overtake its
        # neighbour and the shader's cascading panel pick stays well ordered.
        edges = [
            edge + ENTER_M_PANEL_EXIT * (out_r[index] - out_l[index])
            for index, edge in enumerate(edges)]

        values = []

        for index, (left, right, _char_x) in enumerate(spans):
            values.append((
                -1.0 if index == 0 else edges[index],
                2.0 if index == count - 1 else edges[index + 1],
                centres[index],
                (left + right) * 0.5))

        while len(values) < _SP_SHADER_PANELS:
            values.append((3.0, 3.0, 0.5, 0.5))

        # A cut that leans 74px across the screen is a lean of a fifth of a panel
        # at two people and most of a panel at six, so past a certain narrowness
        # the slant comes off proportionally -- otherwise the busiest layouts are
        # the ones whose gutters eat the most of each shot.
        #
        # MEASURED AGAINST THE SETTLED LAYOUT, NOT THE LIVE SPANS. There is one
        # slant uniform for the whole screen, so taking it from the narrowest
        # span meant a single panel opening or collapsing -- momentarily a
        # hairline, and never wider than the layout it is heading for -- dragged
        # EVERY cut on screen upright with it. Measured on a 3 -> 2 exit: all
        # gutters rotated from 74px to 0.4px (vertical) over ~0.6s and then
        # snapped back to 74px in one frame when the ghost was dropped.
        narrowest = max(_stage_state["narrowv"], 0.0) * width
        slant = ENTER_M_PANEL_SLANT * min(
            1.0, narrowest / max(ENTER_M_PANEL_SLANT_FIT, 1.0))

        # Per-panel look: (listener dim, speaker accent, glint). Everything is
        # scaled by engagement, so a retracted layout is the untouched plate.
        # The glint peaks halfway through a panel opening or closing, and
        # halfway through the whole layout cracking open.
        crack = 4.0 * amt * (1.0 - amt)
        fx = []

        for index in range(count):
            # `spans` gets a placeholder when the last ghost has been dropped
            # but engagement is still easing out; it has no panel behind it.
            panel = panels[index] if index < len(panels) else {}
            p = presence[index]
            glint = ENTER_M_PANEL_GLINT * max(4.0 * p * (1.0 - p), crack)
            fx.append((panel.get("dim", 0.0) * amt,
                panel.get("acc", 0.0) * amt, glint))

        while len(fx) < _SP_SHADER_PANELS:
            fx.append((0.0, 0.0, 0.0))

        default_voice = _stage_panel_voice(None)
        voices = [
            (panels[index].get("voice") if index < len(panels) else None)
                or default_voice
            for index in range(count)]

        while len(voices) < _SP_SHADER_PANELS:
            voices.append(default_voice)

        # Publish the cuts for the cast mask, in the shader's own units. Slack
        # opens every mask as the layout disengages, so a sprite is never
        # clipped by a cut the room is not showing.
        slack = (1.0 - amt) * 0.6
        mask = {}

        for index in range(min(count, len(panels))):
            panel = panels[index]
            left, right = values[index][0], values[index][1]
            entry = (left, right, fx[index],
                slack + panel.get("out", 0.0) * amt / width, right - left,
                voices[index], count)

            for member in panel.get("members") or (panel["tag"],):
                prior = mask.get(member)

                if prior is None or entry[4] > prior[4]:
                    mask[member] = entry

        _stage_mask["panels"] = mask
        _stage_mask["edge"] = ((slant / width) * amt,
            (ENTER_M_PANEL_GAP * 0.5 / width) * amt)
        _stage_mask["look"] = (ENTER_M_PANEL_RIM / width,
            ENTER_M_PANEL_EDGE * amt, ENTER_M_PANEL_SHADE * amt,
            ENTER_M_PANEL_FALLOFF / width)
        _stage_mask["t"] = getattr(renpy.display.interface, "frame_time", None)
        _stage_mask["on"] = True

        trans.mesh = True
        trans.shader = "enter_m.stage_panels"
        trans.u_em_sp_screen = (width, height)
        trans.u_em_sp_p0 = values[0]
        trans.u_em_sp_p1 = values[1]
        trans.u_em_sp_p2 = values[2]
        trans.u_em_sp_p3 = values[3]
        trans.u_em_sp_p4 = values[4]
        trans.u_em_sp_p5 = values[5]
        trans.u_em_sp_f0 = fx[0]
        trans.u_em_sp_f1 = fx[1]
        trans.u_em_sp_f2 = fx[2]
        trans.u_em_sp_f3 = fx[3]
        trans.u_em_sp_f4 = fx[4]
        trans.u_em_sp_f5 = fx[5]
        trans.u_em_sp_tick = ENTER_M_PANEL_TICK * amt
        trans.u_em_sp_push = ENTER_M_PANEL_PUSH
        trans.u_em_sp_glow = ENTER_M_PANEL_GLOW
        trans.u_em_sp_c0 = voices[0]
        trans.u_em_sp_c1 = voices[1]
        trans.u_em_sp_c2 = voices[2]
        trans.u_em_sp_c3 = voices[3]
        trans.u_em_sp_c4 = voices[4]
        trans.u_em_sp_c5 = voices[5]
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

    def _stage_panels_scope_classify(filename):
        """True for story, False for isolated content, None for a helper."""
        if not filename:
            return None

        # In development, AST filenames are `game/story/...`. The archive
        # builder strips that first component, so the same statement becomes
        # `story/...` in a release. An absolute filename can also reach this
        # helper through tooling. Reduce every form to one case-insensitive
        # `game/...` logical path before applying the public scope tables.
        logical = filename.replace("\\", "/")
        game_marker = logical.lower().rfind("/game/")

        if game_marker >= 0:
            logical = logical[game_marker + 1:]
        else:
            logical = logical.lstrip("/")
            if not logical.lower().startswith("game/"):
                logical = "game/" + logical

        logical = logical.lower()

        for prefix in ENTER_M_PANEL_SCOPE_ON:
            if logical.startswith(prefix.replace("\\", "/").lower()):
                return True

        for prefix in ENTER_M_PANEL_SCOPE_OFF:
            if logical.startswith(prefix.replace("\\", "/").lower()):
                return False

        return None

    def _stage_panels_scope_update():
        try:
            filename = renpy.get_filename_line()[0]
        except Exception:
            return

        scope = _stage_panels_scope_classify(filename)

        if scope is not None:
            _stage_state["scope"] = scope

        # Anything else -- a helper label, an addon, a screen -- says nothing
        # about scope, so the latch holds.

    def enter_m_main_story_active():
        """True in the main-story presentation scope, independent of panels."""
        # Refresh at the call site as well as at interaction start. This keeps
        # screen actions and programmatic phone checks correct even before the
        # first interaction in a freshly started standalone story.
        _stage_panels_scope_update()
        return bool(_stage_state["scope"])

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
        _stage_mask["on"] = False
        _stage_mask["panels"] = {}
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
