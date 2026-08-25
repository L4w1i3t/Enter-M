# =============================================================================
# kototouhou.rpy -- "Kotonoha mode": the literal Touhou stage you reach from
#                    cs_matsuda_02's roster ("I want to fight somebody else.").
# =============================================================================
#
# WHAT THIS IS
#   A complete danmaku boss battle against Katsura Kotonoha, played straight as
#   a one-boss Touhou stage. Eight health bars; each bar opens on a NONSPELL
#   pattern and flips into a named SPELL CARD at half health -- pattern, card,
#   rinse, repeat, exactly like a Touhou boss. Z shoots, X bombs, arrows move,
#   Shift focuses (slow + shows the hitbox). Standard runs start with 5 lives
#   / 3 bombs; practice runs have unlimited lives and do not count for records.
#   ENDLESS MODE rolls random waves forever from the FULL pattern hat: the
#   eight fixed bars PLUS four Endless-only nonspells, eight Endless-only
#   MASK spell cards (the other cast members' styles, worn one wave at a
#   time), and six Endless-only SOUL cards (older readings from a different
#   cellar -- the mode's Undertale debt, paid openly). Every entry in the
#   hat is EQUALLY likely on every wave; the only constraint is no immediate
#   repeat of the same nonspell or spell card.
#   A third, config.developer-only "debug reading" makes every shot one-shot
#   the current pattern (unlimited lives, no records) so a dev can fast-clear
#   all 8 bars to check the fight's back half and ending.
#
# ARCHITECTURE (and why it hits 60fps where Id Mode ran at 30)
#   * KTGame (below) owns ALL simulation state: player, shots, enemy bullets,
#     sparkles, the bar/card state machine, scoring. Pure python dicts + lists.
#   * KTStage is ONE creator-defined displayable that draws the whole stage --
#     bullets, boss, player, HUD text, banners -- as cached-texture blits in a
#     single render() pass, then asks for an immediate redraw. The simulation
#     is stepped INSIDE render() on a fixed 1/60s accumulator, so gameplay is
#     framerate-locked at 60 ticks/sec without a screen timer and without
#     renpy.restart_interaction() churn (the thing that capped Id Mode's
#     Curtain Script at 30fps: its screen timer rebuilt the interaction every
#     0.033s). Here the screen tree is static; only the CDD repaints.
#   * Bullet sprites come from the shipped pixel art (bullet/pellet/dagger.png)
#     plus bulletsheet.png, a 256x256 atlas of six more shapes (star, sphere,
#     winged ring, knife, oval, spark) and four painted 64px "eye" orbs, plus
#     the SHARED atlas in mod_assets/def_bullets.rpy (arrow, ofuda, rice,
#     kunai, heart, sunburst, moon, the laser hairline, the summoning seals,
#     the bloom discs -- see EMB_ATLAS_RAW there). Cells are cropped once into
#     shared displayables, then colour-tinted via cached TintMatrix transforms
#     and rotation-bucketed like ui.rpy's MSBFShmupField, so per (kind, colour,
#     angle-bucket, scale) there is exactly ONE texture, reused by every blit.
#     See KT_SHEET, KT_SEAL_FOR_COLOR and KTStage.KINDS.
#   * LASERS are their own entity (self.lasers), not bullets: a segment with a
#     telegraph -> fire -> fade life and point-to-segment collision. See
#     _kt_laser and KT_LASER_*. Bar 3's spell card is the one that fires one.
#   * SFX ride battle_logic.rpy's pooled one-shot channels
#     (msbf_play_pooled_sfx) so rapid danmaku cues overlap instead of cutting
#     each other off.
#
# WIRING
#   cs_matsuda_02.rpy -> "I want to fight somebody else." -> "Kotonoha" ->
#   `jump kototouhou`. Ends with `return`, unwinding back to the archive.
#
# PERSISTENT
#   persistent.kotomode_cleared  : set on the first 8-bar clear.
#   persistent.kotomode_hiscore  : best score across runs.
#
# READ THIS FIRST IF YOU ARE LOST
#   This file is three systems stacked together:
#
#   1. KTGame is the simulation. It knows nothing about Matsu'Py display trees.
#      It only mutates numbers and small dicts once per 1/60s tick.
#
#   2. Pattern helpers are free functions that get attached to KTGame after
#      the class is declared. That is intentional: the state-machine code stays
#      readable, while the 34 bullet scripts (8 fixed bars' worth + the
#      Endless-only nonspells, Mask cards, and Soul cards) live in one
#      obvious block.
#
#   3. KTStage is the renderer. It is a Matsu'Py creator-defined displayable
#      whose render() method both advances KTGame and paints the frame.
#
#   The major data flow is:
#
#       label kototouhou_fight
#           -> creates KTGame
#           -> calls kototouhou_screen
#           -> screen owns one KTStage(game)
#           -> KTStage.render() accumulates wall time into fixed 60Hz ticks
#           -> KTGame.step() mutates bullets/shots/state
#           -> KTStage.render() draws the current state
#           -> kt_poll_result() returns victory/defeat/quit (or the wave
#              viewer's wave_done) to the label
#
#   Units:
#     * All gameplay coordinates are PLAYFIELD-LOCAL pixels: (0, 0) is the
#       top-left of the 620x680 stage, not the 1280x720 screen.
#     * KTStage mounts that stage at (KT_SX, KT_SY) after drawing.
#     * Speeds are pixels per simulation tick. At 60 ticks/sec, 2.0 means
#       roughly 120 px/sec.
#     * Timers are ticks unless a variable is explicitly named seconds.
#
#   Runtime entity dicts:
#     * bullet: x/y/vx/vy, kind, ci, scale, sway/ph, ax/ay, ttl/fz, home,
#       home_t, bnc, blk, rot, age, gz, hr.
#     * shot: x/y/vx/vy/dmg.
#     * spark: x/y/vx/vy/age/ttl/ci.
#     * banner: text/ci/size/born/ttl/slot/y.
#     * death_fx: x/y/born.
#
#   Phase machine:
#     intro -> nonspell -> declare -> spell -> break, repeated for each bar.
#     victory/defeat/quit are terminal outcomes. "declare" is the dramatic
#     spell-card cut-in between the top half and bottom half of each HP bar.
#
#   Performance rules:
#     * Do not put per-frame gameplay in the screen. The screen should remain
#       static so Matsu'Py can reuse it.
#     * Do not store renpy.Render objects on KTStage or KTGame. Render objects
#       are frame products; the renderer keeps only displayable factories across
#       frames and memoizes actual renders for the current frame only.
#     * If you add bullet art, add it through KTStage.KINDS and keep rotation /
#       tint cache keys small. Thousands of unique Transform keys will tank FPS.
#       A new kind needs THREE entries kept in step: KINDS (sprite + zoom),
#       KT_KIND_HR (hit radius) and, if it points where it flies, KT_SPIN.
#     * If you add a pattern, respect KT_MAX_BULLETS and prefer deterministic
#       formulas keyed from t/phase_tick over random calls.
# =============================================================================

# --- IMAGES / AUDIO / STATE DEFAULTS -----------------------------------------
image koto_backdrop = "addons/Matsuda's Sick Boss Fight/kotonohamode/kotobackdrop.png"
# Endless Mode reads somewhere else entirely: not her shrine, but the barrier
# the endless reading happens behind. Swapped in by kototouhou_screen.
image koto_backdrop_endless = "addons/Matsuda's Sick Boss Fight/kotonohamode/endless.png"

define -50 audio.kt_boss_theme = "<loop 0>mod_assets/bgm/kotobossmusic.ogg"
# Endless Mode gets its own loop -- a different, no-ending survival theme.
define -50 audio.kt_endless_theme = "<loop 0>mod_assets/bgm/kotoendlessmode.ogg"

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
transform kt_backdrop_breathe:
    subpixel True
    xalign 0.5
    yalign 0.5
    zoom 1.0
    block:
        ease 9.0 zoom 1.035
        ease 9.0 zoom 1.0
        repeat

# --- SHADERS (spell 5 darkness + the boss spell circle) ----------------------
# koto.spotlight: a GPU spotlight -- the stage goes dark except for a soft
# window around the player and a dimmer one around Kotonoha.
# koto.circle: a procedural Touhou "spell circle" -- concentric rings, a dashed
# band rotating one way, soft spokes sweeping the other. Drawn behind the boss
# (her float anchor) and, small and fast, under the player while focused.
# Registered defensively like fx.rpy; on failure the fight plays without them.
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

        # u_time is Matsu'Py's built-in frame clock, so the circle spins on the
        # GPU with no per-frame python. Premultiplied output.
        # GLSL note: the circle shader is just polar-coordinate math:
        #   r   = distance from center of the quad
        #   ang = angle around that center
        # Then it layers thin rings, dashed arcs, spokes, and a center glow.
        renpy.register_shader("koto.circle", variables="""
            uniform vec3 u_koto_col;
            uniform float u_koto_alpha;
            uniform float u_koto_spin;
            uniform float u_time;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 d = v_tex_coord - vec2(0.5);
            float r = length(d) * 2.0;
            float ang = atan(d.y, d.x);
            float t = u_time * u_koto_spin;
            float a = 0.0;
            // Two razor-thin concentric rings.
            a += smoothstep(0.035, 0.0, abs(r - 0.93)) * 0.9;
            a += smoothstep(0.025, 0.0, abs(r - 0.60)) * 0.65;
            // Dashed band: fract() repeats around the circle, step() turns
            // every other segment on/off, and subtracting t rotates it.
            float dash = step(0.5, fract((ang - t) * 3.8197));
            a += smoothstep(0.09, 0.0, abs(r - 0.775)) * dash * 0.55;
            // Soft spokes: high exponent makes narrow bright rays; the radial
            // masks stop them from filling the center or leaking past the ring.
            float spoke = pow(abs(cos((ang + t * 0.6) * 3.0)), 24.0);
            a += spoke * smoothstep(0.93, 0.30, r) * step(0.34, r) * 0.4;
            // Faint center fill so the sigil reads as one object, not just
            // disconnected lines.
            a += (1.0 - smoothstep(0.0, 0.55, r)) * 0.10;
            a *= u_koto_alpha;
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

    # KT_DIR is now only this mode's OWN art: the ship, the boss sprite, the
    # backdrops, the bomb icon. Every bullet sprite -- including the four
    # shipped pixel ones and the old bulletsheet.png -- lives in the shared
    # mod_assets/bullets/ folder and is reached through EMB_DIR (defined in
    # mod_assets/def_bullets.rpy at init -20), so that all bullet art in the
    # project sits in exactly one place.
    KT_DIR = "addons/Matsuda's Sick Boss Fight/kotonohamode/"
    KT_SE_DIR = "mod_assets/sfx/touhou/"

    # Kotonoha's boss sheet is a strict 4x4 atlas of 128px cells:
    #   row 0 idle/hover, row 1 bank left, row 2 bank right, row 3 cast.
    # Frames are cropped once here and selected from the simulation tick in
    # KTStage. That keeps animation deterministic, freezes it under pause, and
    # avoids rebuilding the screen interaction at animation speed.
    KT_BOSS_SHEET = KT_DIR + "kotoboss_sheet.png"
    KT_BOSS_CELL = 128
    KT_BOSS_ZOOM = 1.35
    KT_BOSS_IDLE = 0
    KT_BOSS_LEFT = 1
    KT_BOSS_RIGHT = 2
    KT_BOSS_CAST = 3
    KT_BOSS_IDLE_LOOP = (0, 1, 2, 3, 2, 1)
    KT_BOSS_CAST_LOOP = (0, 1, 2, 3, 2, 1)

    def kt_boss_cell(row, col):
        return Crop((col * KT_BOSS_CELL, row * KT_BOSS_CELL,
                     KT_BOSS_CELL, KT_BOSS_CELL), KT_BOSS_SHEET)

    KT_BOSS_FRAMES = tuple(
        tuple(kt_boss_cell(row, col) for col in range(4))
        for row in range(4)
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

    # Bullets.
    KT_MAX_BULLETS = 480
    KT_MAX_SHOTS = 64
    KT_MAX_SPARKS = 170
    KT_ROT_BUCKETS = 60
    KT_ROT_DEG = 360.0 / KT_ROT_BUCKETS

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

    # --- THE BULLET SHEET -----------------------------------------------------
    # bulletsheet.png is 256x256: an 8x8 grid of 32px cells holding SIX shapes
    # down the rows -- star / sphere / ring / knife / oval / spark -- each
    # painted in eight colourways across the columns, plus four 64px "eye" orbs
    # filling the bottom two rows.
    #
    # Those eight colourways are NOT how bullets get their colour here. Every
    # bullet carries a KT_PAL index and the renderer tints it, exactly as it
    # already does for the shipped pixel art, so a shape stays one cache family
    # across all fifteen palette entries instead of eight fixed ones. The
    # shapes are therefore cut from COLUMN 7, the brightest fully-desaturated
    # colourway (measured saturation < 0.05, value 0.73-0.99), which takes a
    # TintMatrix cleanly. One Crop displayable per shape, built once here and
    # shared by every cached bullet Transform below.
    KT_SHEET = EMB_DIR + "bulletsheet.png"
    KT_SHEET_WHITE = 7          # the tintable column

    def kt_sheet_cell(row, col=KT_SHEET_WHITE, size=32):
        # Live Crop, not a copy: the sheet is one texture and every cell is a
        # subsurface of it.
        return Crop((col * size, row * size, size, size), KT_SHEET)

    # The four 64px orbs are painted art rather than silhouettes -- white shell,
    # saturated corona, black pupil -- so tinting one would just crush the
    # corona it was drawn with. They ship as four fixed colourways instead, and
    # a bullet's palette index picks the nearest through KT_EYE_COL.
    KT_EYE_CELLS = [kt_sheet_cell(3, c, 64) for c in range(4)]   # red violet green yellow
    KT_EYE_COL = [
        0,  # 0  red      -> red
        0,  # 1  pink     -> red
        1,  # 2  magenta  -> violet
        1,  # 3  purple   -> violet
        1,  # 4  violet   -> violet
        1,  # 5  blue     -> violet
        2,  # 6  cyan     -> green
        2,  # 7  teal     -> green
        2,  # 8  green    -> green
        2,  # 9  lime     -> green
        3,  # 10 yellow   -> yellow
        3,  # 11 amber    -> yellow
        3,  # 12 orange   -> yellow
        0,  # 13 white    -> red     (the white shell already carries the white)
        1,  # 14 grey     -> violet
    ]

    # Which painted summoning seal a card wears, by its KT_PAL accent. Same
    # deal as KT_EYE_COL: the seals are painted art from the shared atlas
    # (def_bullets.rpy) and carry their own colour, so a card's accent picks
    # the NEAREST sigil rather than tinting one. Indexed by KT_PAL index, so a
    # given card always slams down the same seal.
    KT_SEAL_FOR_COLOR = [
        "seal_hex",     # 0  red     -- the red hexagram, and it is the red card
        "seal_hex",     # 1  pink
        "seal_spike",   # 2  magenta -- the white/black spiked ring
        "seal_blue",    # 3  purple
        "seal_blue",    # 4  violet
        "seal_blue",    # 5  blue
        "seal_blue",    # 6  cyan
        "seal_green",   # 7  teal
        "seal_green",   # 8  green
        "seal_green",   # 9  lime
        "seal_yellow",  # 10 yellow
        "seal_yellow",  # 11 amber
        "seal_orange",  # 12 orange
        "seal_spike",   # 13 white
        "seal_spike",   # 14 grey
    ]

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

    def kt_debug_wave_pick():
        # DEV ONLY -- interactive picker for the debug wave viewer. The old
        # version stacked renpy.display_menu pages, which overflowed the VN
        # menu once the roster outgrew the screen (items ran off the bottom
        # and could not be clicked). It is now one purpose-built grid screen:
        # every opener and every card visible at once, click one of each,
        # confirm. Returns (ns_index, sp_index) into the combined roster, or
        # None if the dev backs out.
        #
        # BACK/ESC return None and READ THIS PAGE returns a 2-tuple -- those are
        # the only picker returns. But a stray dismiss from a lingering say
        # window can end the interaction with True, so normalize anything that
        # isn't a 2-tuple to None; the caller's None check then can't blow up on
        # a bool subscript.
        rv = renpy.call_screen("kt_wave_picker")
        if isinstance(rv, tuple) and len(rv) == 2:
            return rv
        return None

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

    # SFX table (ZUN-standard cue names, shipped in mod_assets/sfx/touhou/). Volumes are
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
                if gone % 3 == 1 and len(self.sparks) < KT_MAX_SPARKS:
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
                if len(self.shots) < KT_MAX_SHOTS:
                    if self.focus:
                        for ox in (-7.0, 7.0):
                            self.shots.append({"x": self.px + ox, "y": self.py - 12.0,
                                                "vx": 0.0, "vy": -KT_SHOT_SPEED, "dmg": dmg * 1.3})
                    else:
                        for ang in (-0.13, 0.0, 0.13):
                            self.shots.append({"x": self.px, "y": self.py - 12.0,
                                                "vx": math.sin(ang) * KT_SHOT_SPEED,
                                                "vy": -math.cos(ang) * KT_SHOT_SPEED, "dmg": dmg})
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
                if self.phase_tick == 40:
                    self._se("charge2", 0, 0.9)
                if self.phase_tick >= 85:
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
                        b["rot"] = math.degrees(math.atan2(b["vy"], b["vx"])) + 90.0
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
            # no hiscore, no clear flag from either. Endless keeps its OWN
            # records (best score + furthest wave) and never sets the clear flag.
            try:
                if self.endless:
                    if self.score > (persistent.kotomode_endless_hiscore or 0):
                        persistent.kotomode_endless_hiscore = self.score
                    if self.endless_wave > (persistent.kotomode_endless_wave or 0):
                        persistent.kotomode_endless_wave = self.endless_wave
                elif not (self.practice or self.debug):
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
#   and bar 7 are knives, bar 4 is rice rain, the Seer pours winged rings,
#   Justice fires eyes). The shared atlas widened this vocabulary a lot; that
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
    KT_KIND_HR = {
        # the shipped pixel art
        "orb": 6.0, "pellet": 4.5, "dagger": 4.5, "big": 15.0,
        # bulletsheet.png (see KT_SHEET above)
        "star": 6.5,        # 27px point-to-point
        "sphere": 6.0,      # 22px glowing disc -- the soft twin of orb
        "ring": 5.0,        # 15px ring inside a wide, faint winged aura
        "knife": 5.0,       # 12x30 blade, a shade heavier than dagger
        "oval": 4.5,        # 11x22 petal/droplet/casing, leans with its heading
        "spark": 5.0,       # 16px core under long thin rays
        "eye": 15.0,        # 48px painted orb -- big's replacement where it lands
        # the shared atlas (mod_assets/def_bullets.rpy). Same house rule: the
        # radius is ~55-65% of the drawn body, so what you see is bigger than
        # what kills you.
        "arrow": 5.5,       # 21px chevron -- reads as a direction, not a dot
        "hoop": 5.5,        # 20px hollow ring, lighter than `ring` (no wings)
        "rice": 4.0,        # 12x21 grain of rice, the small filler shot
        "kunai": 5.0,       # 16x20 pinned dart with a bead at its throat
        "grain": 4.8,       # 17x19 husk, blunter than rice
        # 18x21 talisman card, stays UPRIGHT (see KT_SPIN). Deliberately a
        # shade under its drawn body: it inherited bar 2's ring role and the
        # finale quotes it 26 at a time, so a true 6.0 would have retuned a
        # card nobody asked me to retune.
        "ofuda": 5.5,
        "slug": 4.5,        # 12x22 capsule round
        "seed": 4.5,        # 12x22 dark pip inside a bright rim
        "ministar": 5.5,    # 20x19 star -- the small sibling of `star`
        "gloss": 6.0,       # 21px lacquered ball with a hard specular
        "heart": 7.0,       # 24px heart
        "sunburst": 6.5,    # 26px eight-point burst
        "moon": 11.0,       # 34px white core in a wide corona -- big and slow
        "frost": 6.5,       # 27px ice crystal
    }

    # Kinds whose sprite points along its heading. Everything else stays in
    # rotation bucket 0, which is what keeps a round bullet at one texture per
    # (colour, scale) instead of sixty. Keep this set small for that reason --
    # `ofuda` is deliberately NOT in it (a talisman hangs upright), and neither
    # are any of the radially symmetric shapes.
    KT_SPIN = frozenset((
        "pellet", "dagger", "knife", "oval",
        "arrow", "rice", "kunai", "grain", "slug", "seed",
    ))

    # --- SPAWN MATERIALIZE -----------------------------------------------------
    # Bullets used to arrive at full size and full opacity on their very first
    # drawn tick, which reads as them popping into existence -- worst on the
    # knives, whose long blade appears all at once and out of nowhere. Now every
    # bullet BLOOMS instead: over KT_SPAWN_TICKS it fades up through a few alpha
    # steps while scaling out from a pinpoint, under a brief white flare at the
    # emission point. Touhou's own bullets do exactly this, and it doubles as an
    # honest telegraph -- for those few ticks you can see where a wall is about
    # to be before it is one.
    #
    # It stays cheap because it is expressed entirely in the SAME bucketed keys
    # the renderer already caches on: the fade is KT_SPAWN_STEPS discrete alpha
    # values (not a continuous one), and the growth reuses the existing quantized
    # scale key. So a 40-bullet ring materializing still draws out of a handful of
    # textures. Both the flare and the growth also ride the frozen (fz) window
    # unchanged, since a bullet's age advances while it is held.
    KT_SPAWN_TICKS = 8            # length of the materialize, in ticks
    KT_SPAWN_STEPS = 3            # discrete alpha steps (index KT_SPAWN_STEPS = opaque)
    KT_SPAWN_ALPHA = (0.16, 0.42, 0.72)
    KT_SPAWN_FLARE_TICKS = 5      # white bloom at the emission point

    def _kt_add(self, x, y, vx, vy, kind="orb", ci=13, scale=1.0, sway=0.0,
                ph=0.0, ax=0.0, ay=0.0, ttl=None, fz=0, home=0, home_t=50, bnc=0,
                blk=0, calm=0):
        # Core bullet constructor. Field meanings:
        #   x/y      current stage-local position
        #   vx/vy    velocity applied every tick
        #   kind     sprite/hit-radius family: orb, big, pellet, dagger
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
        #   rot      renderer heading in degrees
        #   gz       whether this bullet has already paid graze once
        #   hr       cached hit radius, pre-scaled for collision speed
        # Returns the live bullet dict (or None at the cap) so patterns that
        # need to revisit a bullet later -- the Hunter's flare shells, the
        # Kindness servings -- can keep a handle instead of scanning the list.
        if len(self.bullets) >= KT_MAX_BULLETS:
            return None
        rot = 0.0
        if kind in KT_SPIN:
            rot = math.degrees(math.atan2(vy, vx)) + 90.0
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
            "rot": rot, "age": 0, "gz": False,
            "hr": KT_KIND_HR[kind] * scale,
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
    # A laser is drawn from the `lens` art in the shared atlas (a 248x8 hairline
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
        # slip with a face printed on it. It is the one shape on the sheet that
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
        # SPRITES: the broadside is KNIVES, the biggest blade in the sheet, and
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
        # warning) -- the schedule always finds you. Same oval rain as her
        # nonspell, harder; the strikes are knives, because they are not rain.
        wind = math.sin(t * 0.016) * 1.5
        if t % 3 == 0:
            # Pseudo-random x via modular arithmetic: deterministic coverage of
            # the width without calling random every three ticks.
            ci = 8 if (t // 3) % 2 == 0 else 9
            self._add((t * 97) % KT_W, -12.0, wind, 2.9, "oval", ci)
            self._se("fire", 26, 0.45)
        cyc = t % 170
        if cyc == 0:
            # Snapshot the player's x at warning time. The strike uses this
            # saved column 30 ticks later, so the player gets a fair tell.
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
        # never which bullet, only which side of the mirror threw it.
        mx = KT_W - self.bx
        if t % 80 == 0:
            # Mirrored boss x: not a separate entity, just the reflected firing
            # origin. The renderer draws the phantom while mirror_on is true.
            down = math.pi * 0.5
            self._fan(self.bx, self.by, 12, down, 0.20, 2.15, "ring", 6)
            self._fan(mx, self.by, 12, down, 0.20, 2.15, "ring", 2)
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
        # petal -- and the whole flowers that follow are spheres, heads intact.
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
                        math.cos(a) * 0.5, math.sin(a) * 0.5 + 1.1, "sphere", 0, 1.3)
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
        if cyc == 0:
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
        # WINGED RINGS (the sheet's butterfly), the lattice is knives, and what
        # comes through the gaps at the end are EYES.
        cyc = t % 460
        gaps = self.scratch.get("gaps")
        if cyc == 0:
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
                    "ring", 0 if gi % 2 == 0 else 6, 1.0, sway=0.7, ph=cyc * 0.3)
            self._add(gx, gy, math.cos(ga - wob) * 1.6, math.sin(ga - wob) * 1.6,
                    "ring", (11, 2, 8, 4)[(cyc // 9) % 4], 1.0, sway=0.5, ph=cyc * 0.2)
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
        if cyc == 0:
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
        # daggers -- handwriting, not blades -- while the blots are round and
        # the nib is the one real knife on the page.
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
            self._add((k * 149) % KT_W, -12.0, 0.0, 1.7 + 0.5 * (k % 3), "sphere",
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
    KT_FONT = "mod_assets/fonts/SF Automaton Extended.ttf"

    class KTStage(renpy.Displayable):

        # Class-level displayable caches (persist across frames + interactions).
        # These cache Transform/Text/Solid displayables, NOT renpy.Render
        # objects. Matsu'Py Render objects are frame products and should not be
        # retained on a creator-defined displayable. The frame_tex memo inside
        # render() handles per-frame Render reuse safely.
        _tf_cache = {}
        _text_cache = {}
        _misc_cache = {}

        # (sprite source, base zoom, rotates-to-heading?, pixel art?)
        # Adding a bullet family starts here. Keep the set small and prefer
        # palette tinting over many separate files; the cache key is
        # (kind, color-index, rotation-bucket, scale-quarter).
        #
        # `sprite source` is an image path, OR a LIST of pre-coloured
        # displayables -- art that carries its own colour and so is indexed by
        # KT_EYE_COL[ci] instead of tinted.
        # `pixel art` picks the scaling filter: the four shipped sprites are
        # 16px pixel art and want nearest; the bulletsheet shapes are
        # anti-aliased at 32/64px and want smooth.
        #
        # Zooms are chosen so each shape's drawn body lands near its siblings:
        # orb reads 22px across, so star reads 26 point-to-point, sphere 22,
        # knife 12x30 against dagger's 13x27, oval 11x22 against pellet's
        # 14x22, and eye 48 against big's 48.
        # The atlas shapes below come from mod_assets/def_bullets.rpy, which
        # hands back the NEUTRAL (desaturated) cell of each family -- exactly
        # the same deal as KT_SHEET_WHITE above, so they tint through the same
        # KT_PAL index and stay one cache family apiece. They are anti-aliased
        # art, so `pixel art` is False for all of them.
        KINDS = {
            "orb":    (EMB_DIR + "bullet.png", 1.35, False, True),
            "big":    (EMB_DIR + "bullet.png", 3.0,  False, True),
            "pellet": (EMB_DIR + "pellet.png", 1.4,  True,  True),
            "dagger": (EMB_DIR + "dagger.png", 1.8,  True,  True),
            "star":   (kt_sheet_cell(0), 0.90, False, False),
            "sphere": (kt_sheet_cell(1), 0.85, False, False),
            "ring":   (kt_sheet_cell(2), 1.00, False, False),
            "knife":  (kt_sheet_cell(3), 1.00, True,  False),
            "oval":   (kt_sheet_cell(4), 0.85, True,  False),
            "spark":  (kt_sheet_cell(5), 0.90, False, False),
            "eye":    (KT_EYE_CELLS,     0.78, False, False),
            # shared atlas -- zooms chosen so each body lands near its siblings
            "arrow":    (emb_cell("arrow"),    1.30, True,  False),
            "hoop":     (emb_cell("hoop"),     1.25, False, False),
            "rice":     (emb_cell("rice"),     1.30, True,  False),
            "kunai":    (emb_cell("kunai"),    1.25, True,  False),
            "grain":    (emb_cell("grain"),    1.20, True,  False),
            "ofuda":    (emb_cell("ofuda"),    1.30, False, False),
            "slug":     (emb_cell("slug"),     1.35, True,  False),
            "seed":     (emb_cell("seed"),     1.35, True,  False),
            "ministar": (emb_cell("ministar"), 1.25, False, False),
            "gloss":    (emb_cell("gloss"),    1.30, False, False),
            "heart":    (emb_cell("heart"),    0.80, False, False),
            "sunburst": (emb_cell("sunburst"), 0.82, False, False),
            "moon":     (emb_cell("moon"),     0.55, False, False),
            "frost":    (emb_cell("frost"),    0.85, False, False),
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
            # Actual tick-to-tick boss travel, sampled only when the simulation
            # tick changes. Duplicate render calls must not erase the direction
            # and pause must freeze it with the rest of the fight.
            self._boss_motion_tick = game.tick
            self._boss_last_x = game.bx
            self._boss_dx = 0.0
            # Player dash afterimages (renderer-side): sampled while the ship
            # moves unfocused, drawn as faint ghosts behind it.
            self.ptrail = []
            self._ptrail_tick = -99
            # HP-bar chip ghost (renderer-side, cosmetic): a pale segment that
            # lags behind the real fill so burst damage reads as a bite.
            self._hp_ghost = 1.0

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
                src, base_zoom, rotates, pixel = KTStage.KINDS[kind]
                kw = dict(zoom=base_zoom * (sq / 4.0), subpixel=True)
                if isinstance(src, list):
                    # Pre-coloured art: pick the shipped colourway nearest this
                    # palette index. Tinting it would only crush the corona it
                    # was painted with.
                    src = src[KT_EYE_COL[ci]]
                else:
                    kw["matrixcolor"] = TintMatrix(KT_PAL[ci])
                if pixel:
                    kw["nearest"] = True
                if ghost:
                    kw["alpha"] = 0.34
                elif ab < KT_SPAWN_STEPS:
                    kw["alpha"] = KT_SPAWN_ALPHA[ab]
                if rotates:
                    kw["rotate"] = bucket * KT_ROT_DEG
                tf = Transform(src, **kw)
                KTStage._tf_cache[key] = tf
            return tf

        def _misc(self, key, builder):
            # Shared factory for non-bullet displayables: icons, aura quads,
            # shader rings, cached Solid colors, etc. builder is called only on
            # a cache miss, so lambdas passed here should close over immutable
            # values, not mutable per-frame objects.
            d = KTStage._misc_cache.get(key)
            if d is None:
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

        def _boss_frame(self, game):
            """Choose one cached sheet cell from simulation state and time."""
            if game.tick != self._boss_motion_tick:
                self._boss_dx = game.bx - self._boss_last_x
                self._boss_last_x = game.bx
                self._boss_motion_tick = game.tick

            if game.phase == "declare":
                frame = KT_BOSS_CAST_LOOP[(game.phase_tick // 6) % len(KT_BOSS_CAST_LOOP)]
                return KT_BOSS_CAST, frame
            if game.phase == "victory":
                return KT_BOSS_CAST, 2
            if game.phase == "break":
                return KT_BOSS_CAST, 3

            cast_age = game.tick - game.muzzle
            if 0 <= cast_age < 12:
                frame = KT_BOSS_CAST_LOOP[min(len(KT_BOSS_CAST_LOOP) - 1, cast_age // 2)]
                return KT_BOSS_CAST, frame

            move_frame = (game.tick // 5) % 4
            if self._boss_dx < -0.35:
                return KT_BOSS_LEFT, move_frame
            if self._boss_dx > 0.35:
                return KT_BOSS_RIGHT, move_frame

            frame = KT_BOSS_IDLE_LOOP[(game.tick // 8) % len(KT_BOSS_IDLE_LOOP)]
            return KT_BOSS_IDLE, frame

        # ----- render --------------------------------------------------------

        def render(self, width, height, st, at):
            g = self.game

            # F3 profiler (perf.rpy). One attribute read when it is off, which
            # is what leaving the instrumentation in shipping code costs.
            _perf = MSBF_PERF.on
            _t = msbf_perf_t0() if _perf else 0.0

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

            stage = renpy.Render(KT_W, KT_H)
            sblit = stage.subpixel_blit

            # Draw order is intentional:
            #   background dim -> boss/aura -> player shots -> sparks -> enemy
            #   bullets -> bomb/death/player/focus -> darkness -> HUD/overlays.
            # In particular, enemy bullets draw above player shots, and the
            # spell-5 darkness draws after the player so it darkens the whole
            # playfield through one shader pass.

            # Stage dim so danmaku pops against the shrine backdrop; deeper
            # during spell cards, Touhou-style.
            in_spell = g.phase in ("declare", "spell")
            stage.blit(rect("#00000055" if not in_spell else "#00000078", KT_W, KT_H), (0, 0))

            # --- koto.veil: the living backdrop -------------------------------
            # One GPU quad of slow rays + ripples in the card colour, right on
            # top of the dim so everything else still draws over it. Alpha is
            # phase-staged: barely-there in a nonspell, a touch louder under a
            # card, swelling through the declare.
            if KT_SHADER_OK:
                if g.phase == "declare":
                    va = 0.055 + 0.045 * kt_clamp(g.phase_tick / 40.0, 0.0, 1.0)
                elif g.phase == "spell":
                    va = 0.10
                elif g.phase in ("nonspell", "break"):
                    va = 0.055
                else:
                    va = 0.04
                try:
                    veil = Transform(Solid("#00000000"), xysize=(KT_W, KT_H),
                                    shader="koto.veil",
                                    u_koto_col=Color(KT_PAL[g.cur_color]).rgb,
                                    u_koto_alpha=va)
                    vlr = renpy.render(veil, KT_W, KT_H, st, at)
                    rv.depends_on(vlr)
                    stage.blit(vlr, (0, 0))
                except Exception:
                    pass

            # --- ambient atmosphere motes (backmost gameplay layer) -----------
            # A soft, ever-present drift of light over the shrine so the arena
            # reads as a living place, not just bullets on a flat picture. Motes
            # twinkle (3 alpha buckets) and come in two sizes; the big ones use
            # the petal sprite. Cheap: fixed pool, few cached textures.
            for m in g.ambient:
                tw = 0.5 + 0.5 * math.sin(m["ph"])
                ab = int(tw * 2.999)
                big = m["big"]
                scb = m["scb"]
                akey = ("amb", m["ci"], ab, scb, big)
                amb_d = self._misc(akey, (lambda ci=m["ci"], a=ab, s=scb, bg=big: Transform(
                    (EMB_DIR + ("pellet.png" if bg else "bullet.png")),
                    zoom=((0.95 if bg else 0.42) * (0.7 + 0.4 * s)),
                    subpixel=True, matrixcolor=TintMatrix(KT_PAL[ci]),
                    alpha=0.09 + 0.10 * a)))
                amr_, (amw_, amh_) = tex(akey, amb_d, 32, 32)
                sblit(amr_, (m["x"] - amw_ / 2.0, m["y"] - amh_ / 2.0))

            # --- Seer gaps (border portals) ------------------------------------
            # Each gap is two stretched glow quads: a card-colour outer seam and
            # a white inner slit, both rotated perpendicular to the emission
            # direction. Alpha fades in over the first beats and back out over
            # the last, bucketed x3 so the texture cache stays tiny.
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
                bkt = int(round((math.degrees(p["ang"]) + 90.0) / 15.0)) % 24
                pkey3 = ("portal", p["ci"], bkt, ab3)
                port_d = self._misc(pkey3, (lambda c=p["ci"], bk=bkt, a3=ab3: Transform(
                    EMB_DIR + "bullet.png", xzoom=6.5, yzoom=1.5, subpixel=True,
                    rotate=bk * 15.0, matrixcolor=TintMatrix(KT_PAL[c]),
                    alpha=0.14 + 0.13 * a3)))
                prr, (prw, prh) = tex(pkey3, port_d, 160, 160)
                sblit(prr, (p["x"] - prw / 2.0, p["y"] - prh / 2.0))
                ckey3 = ("portalc", bkt, ab3)
                core3 = self._misc(ckey3, (lambda bk=bkt, a3=ab3: Transform(
                    EMB_DIR + "bullet.png", xzoom=4.4, yzoom=0.5, subpixel=True,
                    rotate=bk * 15.0, matrixcolor=TintMatrix("#f5faff"),
                    alpha=0.18 + 0.14 * a3)))
                crr, (crw, crh) = tex(ckey3, core3, 160, 160)
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
            boss_src = KT_BOSS_FRAMES[boss_row][boss_col]
            boss_frame_key = (boss_row, boss_col)
            if boss_on:
                # Spell circle: her float anchor. Small and slow while a
                # nonspell runs, flaring open through the declare, wide and
                # bright under a spell card, collapsing during the victory
                # detonations. One shader quad per frame.
                if KT_SHADER_OK:
                    if g.phase == "declare":
                        # Declare ramp: circle grows and brightens during the
                        # spell-card callout, then settles into the spell size.
                        ramp = kt_clamp(g.phase_tick / 30.0, 0.0, 1.0)
                        csize, calpha, cspin = 220.0 + 110.0 * ramp, 0.40 + 0.42 * ramp, 1.7
                    elif g.phase == "spell":
                        csize, calpha, cspin = 322.0, 0.60, 1.0
                    elif g.phase == "intro":
                        ramp = kt_clamp((g.phase_tick - 60) / 80.0, 0.0, 1.0)
                        csize, calpha, cspin = 258.0, 0.48 * ramp, 0.55
                    elif vt >= 0:
                        fade = kt_clamp(1.0 - vt / 90.0, 0.0, 1.0)
                        csize, calpha, cspin = 250.0 * (0.35 + 0.65 * fade), 0.55 * fade, 2.4
                    else:  # nonspell / break
                        csize, calpha, cspin = 228.0, 0.38, 0.55
                    # Tiny breathing pulse so the circle does not look like a
                    # static decal even when the shader pattern is slow.
                    csize *= 1.0 + 0.03 * math.sin(tb * 0.05)
                    if calpha > 0.01:
                        try:
                            # ci_ is size-as-int, not a color index. The shader
                            # quad must be a square bitmap surface of csize px.
                            ci_ = int(csize)
                            circ = Transform(Solid("#00000000"), xysize=(ci_, ci_),
                                            shader="koto.circle",
                                            u_koto_col=Color(KT_PAL[bar["color"]]).rgb,
                                            u_koto_alpha=calpha, u_koto_spin=cspin)
                            ccr = renpy.render(circ, ci_, ci_, st, at)
                            rv.depends_on(ccr)
                            ccw, cch = ccr.get_size()
                            sblit(ccr, (bx_draw - ccw / 2.0, by_draw - cch / 2.0))
                        except Exception:
                            pass
                # Summoning seal: a painted magic circle from the shared atlas,
                # slammed down UNDER her on the declare and held, faint, for the
                # rest of the card. The shader circle above is the moving light;
                # this is the ink it is drawn on. Which seal she wears is picked
                # from the card colour so the same card always shows the same
                # sigil. Painted art, so it is NOT tinted -- see def_bullets.rpy.
                seal_a = 0.0
                seal_px = 0.0
                if g.phase == "declare":
                    sp_ = kt_clamp(g.phase_tick / 26.0, 0.0, 1.0)
                    # Slams in oversized, then settles onto the card size.
                    seal_px = 330.0 - 120.0 * sp_
                    seal_a = 0.85 * sp_
                elif g.phase == "spell":
                    seal_px = 210.0 * (1.0 + 0.03 * math.sin(tb * 0.03))
                    seal_a = 0.34
                if seal_a > 0.01:
                    seal_name = KT_SEAL_FOR_COLOR[bar["color"] % len(KT_SEAL_FOR_COLOR)]
                    # The seals are not all the same native size (seal_hex is
                    # 127x139, the rest 62x62), so zoom targets a DRAWN width --
                    # otherwise the hexagram would slam in at twice the size of
                    # every other card's sigil.
                    seal_nw = emb_size(seal_name)[0]
                    zq = int(seal_px / float(seal_nw) * 8.0)
                    aq = int(seal_a * 7.999)
                    skey_ = ("seal", seal_name, zq, aq)
                    seal_d = self._misc(skey_, (lambda n=seal_name, z=zq, a=aq: Transform(
                        emb_cell(n), zoom=z / 8.0, subpixel=True,
                        alpha=(a + 0.5) / 8.0)))
                    try:
                        sr_, (sw_, sh_) = tex(skey_, seal_d, 460, 460)
                        sblit(sr_, (bx_draw - sw_ / 2.0, by_draw - sh_ / 2.0))
                    except Exception:
                        pass
                if MSBF_FX_SHADERS:
                    # Four aura intensity buckets. This deliberately quantizes
                    # the sine pulse so the cached aura displayables are reused
                    # instead of creating one Transform for every tiny alpha.
                    ib = int((0.5 + 0.5 * math.sin(g.tick * 0.04)) * 3.999)
                    aura_key = ("aura", bar["color"], ib)
                    col = Color(KT_PAL[bar["color"]]).rgb
                    aura = self._misc(aura_key, (lambda c=col, k=ib: Transform(
                        Solid("#00000000"), xysize=(190, 190), shader="msbf.glow",
                        u_color=c, u_intensity=0.42 + 0.13 * k, u_softness=2.0)))
                    try:
                        ar, (aw, ah) = tex(aura_key, aura, 190, 190)
                        sblit(ar, (bx_draw - aw / 2.0, by_draw - ah / 2.0))
                    except Exception:
                        pass
                if g.mirror_on:
                    if g.cur_special == "you":
                        # Mask of You: the phantom is YOUR ship, point-reflected
                        # through the stage centre, tracking your every move.
                        phantom = self._misc("you_phantom", lambda: Transform(
                            KT_DIR + "player.png", xzoom=-3.0, yzoom=-3.0,
                            alpha=0.55,
                            nearest=True, subpixel=True,
                            matrixcolor=TintMatrix("#c8d2dd")))
                        pr, (pw, ph_) = tex("you_phantom", phantom, 64, 64)
                        sblit(pr, (KT_W - g.px - pw / 2.0, KT_H - g.py - ph_ / 2.0))
                    else:
                        phantom_key = ("boss_phantom",) + boss_frame_key
                        phantom = self._misc(phantom_key, lambda: Transform(
                            boss_src, xzoom=-KT_BOSS_ZOOM, yzoom=KT_BOSS_ZOOM,
                            alpha=0.5, nearest=True, subpixel=True))
                        pr, (pw, ph_) = tex(phantom_key, phantom, 220, 220)
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
                if self.trail:
                    t0x, t0y = self.trail[0]
                    # Do not draw ghosts while she is merely bobbing in place;
                    # require actual travel distance.
                    if abs(bx_draw - t0x) + abs(by_draw - t0y) > 11.0:
                        ghost_key = ("boss_ghost",) + boss_frame_key
                        ghost = self._misc(ghost_key, lambda: Transform(
                            boss_src, zoom=KT_BOSS_ZOOM, nearest=True,
                            subpixel=True, alpha=0.16))
                        gr_, (gw_, gh_) = tex(ghost_key, ghost, 220, 220)
                        for gx, gy in self.trail[:-1]:
                            sblit(gr_, (gx - gw_ / 2.0, gy - gh_ / 2.0))
                # Directional sheet poses now supply the bank. Keeping the
                # sprite axis-aligned protects its pixel clusters and bounds
                # this cache at 16 frames x two flash states.
                flash_on = g.boss_flash > 0 or (vt >= 0 and (g.tick // 3) % 2 == 0)
                bkey = ("boss", boss_row, boss_col, flash_on)
                if flash_on:
                    boss_d = self._misc(bkey, lambda: Transform(
                        boss_src, zoom=KT_BOSS_ZOOM, nearest=True,
                        subpixel=True, matrixcolor=BrightnessMatrix(0.55)))
                else:
                    boss_d = self._misc(bkey, lambda: Transform(
                        boss_src, zoom=KT_BOSS_ZOOM, nearest=True, subpixel=True))
                br, (bw, bh) = tex(bkey, boss_d, 220, 220)
                sblit(br, (bx_draw - bw / 2.0, by_draw - bh / 2.0))

                # Muzzle bloom: a bright flare at Kotonoha for ~7 ticks after
                # each fire cue (set in _se), so every volley reads as HER
                # casting. A card-colour halo under a white core, both fading;
                # keyed on a strength bucket so the cache stays tiny.
                mz = g.tick - g.muzzle
                if 0 <= mz < 7:
                    mf = int((1.0 - mz / 7.0) * 3.999)      # 0..3 fade bucket
                    sb = 1 if g.muzzle_str >= 0.9 else 0
                    halo = self._misc(("muzzle_h", g.cur_color, mf, sb),
                        (lambda c=g.cur_color, f=mf, s=sb: Transform(
                            EMB_DIR + "bullet.png",
                            zoom=(1.9 + 0.7 * f) * (0.8 + 0.4 * s), subpixel=True,
                            matrixcolor=TintMatrix(KT_PAL[c]), alpha=0.13 + 0.10 * f)))
                    mhr, (mhw, mhh) = tex(("muzzle_h", g.cur_color, mf, sb), halo, 96, 96)
                    sblit(mhr, (bx_draw - mhw / 2.0, by_draw - mhh / 2.0))
                    core = self._misc(("muzzle_c", mf, sb),
                        (lambda f=mf, s=sb: Transform(
                            EMB_DIR + "bullet.png",
                            zoom=(0.9 + 0.55 * f) * (0.8 + 0.4 * s), subpixel=True,
                            matrixcolor=TintMatrix("#ffffff"), alpha=0.22 + 0.16 * f)))
                    mcr, (mcw, mch) = tex(("muzzle_c", mf, sb), core, 64, 64)
                    sblit(mcr, (bx_draw - mcw / 2.0, by_draw - mch / 2.0))

            # --- player shots (under enemy bullets) ---------------------------
            if g.shots:
                shot_d = self._misc("shot", lambda: Transform(
                    EMB_DIR + "pellet_player.png", zoom=1.25, nearest=True, subpixel=True,
                    matrixcolor=TintMatrix("#ffd7e8"), alpha=0.8))
                sr, (sw, sh) = tex("shot", shot_d, 48, 48)
                for s in g.shots:
                    sblit(sr, (s["x"] - sw / 2.0, s["y"] - sh / 2.0))

            # --- sparkles ------------------------------------------------------
            for s in g.sparks:
                frac = s["age"] / float(s["ttl"])
                # ab is a 3-step fade bucket. Like every other visual bucket in
                # this renderer, fewer alpha states means more texture reuse.
                ab = 2 - min(2, int(frac * 3.0))
                skey = ("spark", s["ci"], ab)
                spark_d = self._misc(skey, (lambda ci=s["ci"], a=ab: Transform(
                    EMB_DIR + "bullet.png", zoom=0.55, subpixel=True,
                    matrixcolor=TintMatrix(KT_PAL[ci]), alpha=0.3 + 0.3 * a)))
                spr, (spw, sph) = tex(skey, spark_d, 32, 32)
                sblit(spr, (s["x"] - spw / 2.0, s["y"] - sph / 2.0))

            # --- lasers (UNDER the bullets, so a bullet on a beam stays read) -
            # Each beam is the `lens` hairline from the shared atlas, stretched
            # to length and rotated into place. Everything the cache keys on is
            # an int: the angle is bucketed like the bullets', the length is in
            # 16px steps and the width in half-pixels, so a sweeping laser
            # re-uses one texture per (bucket, colour, stage) instead of minting
            # a new one every tick.
            for L in g.lasers:
                stage_l, prog = g._laser_phase(L, g.tick)
                if stage_l is None:
                    continue
                half = g._laser_width(L, g.tick)
                if half <= 0.05:
                    continue
                lbucket = int(round(math.degrees(L["ang"]) / KT_ROT_DEG)) % KT_ROT_BUCKETS
                lq = max(1, int(L["len"] / 16.0))
                wq = max(1, int(half * 2.0))
                if stage_l == "warn":
                    # The telegraph is deliberately pale and slightly
                    # transparent: visible enough to plan around, never bright
                    # enough to be mistaken for the live beam.
                    lalpha = 0.30 + 0.22 * prog
                    lcol = 13
                else:
                    lalpha = 1.0 if stage_l == "live" else (1.0 - prog)
                    lcol = L["ci"]
                ab_l = int(lalpha * 5.999)
                lkey = ("laser", lbucket, lq, wq, lcol, ab_l)
                lz = lq * 16.0 / 248.0
                laser_d = self._misc(lkey, (lambda bk=lbucket, z=lz, w=wq, c=lcol, a=ab_l: Transform(
                    emb_cell("lens"), xzoom=z, yzoom=w / 4.0, subpixel=True,
                    rotate=bk * KT_ROT_DEG, matrixcolor=TintMatrix(KT_PAL[c]),
                    alpha=(a + 0.5) / 6.0)))
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

            # --- enemy bullets: THE hot loop ----------------------------------
            bullets = g.bullets
            # White cores look good on orb bullets but double the blit count.
            # Disable them once density is high enough that FPS matters more
            # than the small highlight.
            draw_cores = len(bullets) <= 320
            # Patience tell, resolved ONCE per frame: while the soul is still,
            # every calm bullet drops to a ghost texture -- the field itself
            # answers your stillness. Move and they snap solid again.
            calm_ghost = 1 if g.still_ticks > 0 else 0
            for b in bullets:
                kind = b["kind"]
                # Scale is quantized to quarter steps for cache keys:
                # scale 1.0 -> sq 4, scale 1.25 -> sq 5, etc.
                sq = int(round(b["scale"] * 4.0))
                if kind in KT_SPIN:
                    # Rotation buckets trade a little angular precision for a
                    # huge cache win. 60 buckets = 6 degrees per texture.
                    bucket = int(round(b["rot"] / KT_ROT_DEG)) % KT_ROT_BUCKETS
                else:
                    bucket = 0
                age = b["age"]
                x = b["x"]
                y = b["y"]
                # MATERIALIZE (see the SPAWN MATERIALIZE block up top): for its
                # first KT_SPAWN_TICKS a bullet is still arriving -- white-hot,
                # translucent, and smaller than its true size -- so it grows into
                # the field instead of appearing in it. Everything here is a
                # bucketed cache key, so the whole effect is free of new textures
                # beyond a couple of steps per kind.
                if age < KT_SPAWN_TICKS:
                    grow = (age + 1) / float(KT_SPAWN_TICKS)
                    ci = 13 if age < 4 else b["ci"]
                    sq = max(1, int(round(sq * (0.40 + 0.60 * grow))))
                    ab = min(KT_SPAWN_STEPS - 1, int(grow * KT_SPAWN_STEPS))
                    # The emission flare: one bright, wide, very faint orb that
                    # swells and dies over the first few ticks, so a volley reads
                    # as having been CAST at a point rather than teleported in.
                    # Suppressed at the same density draw_cores is, so a packed
                    # screen never pays for it.
                    if draw_cores and age < KT_SPAWN_FLARE_TICKS:
                        fstep = KT_SPAWN_FLARE_TICKS - age
                        fkey = ("spawnflare", fstep)
                        flare_d = self._misc(fkey, (lambda s=fstep: Transform(
                            EMB_DIR + "bullet.png", zoom=1.35 * (0.9 + 0.45 * s),
                            subpixel=True, matrixcolor=TintMatrix("#ffffff"),
                            alpha=0.06 + 0.05 * s)))
                        flr, (flw, flh) = tex(fkey, flare_d, 96, 96)
                        sblit(flr, (x - flw / 2.0, y - flh / 2.0))
                else:
                    ci = b["ci"]
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
                if draw_cores and not gh and ci != 13 and (kind == "orb" or kind == "big"):
                    ckey = (kind, 13, 0, max(1, sq // 2), 0, ab)
                    cgot = frame_tex.get(ckey)
                    if cgot is None:
                        cgot = tex(ckey, self._bullet_tf(kind, 13, 0, max(1, sq // 2), 0, ab))
                    cr, (cw, ch) = cgot
                    sblit(cr, (x - cw / 2.0, y - ch / 2.0))

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
                # Bomb WASH: a painted radial disc from the shared atlas, blown
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
                    bzq = int(bw_px / 24.0)
                    baq = int(bw_a * 7.999)
                    bwkey = ("bombwash", bzq, baq)
                    wash_d = self._misc(bwkey, (lambda z=bzq, a=baq: Transform(
                        emb_cell("bloom_soft"), zoom=z * 24.0 / 245.0, subpixel=True,
                        matrixcolor=TintMatrix("#ffd7e8"), alpha=(a + 0.5) / 8.0)))
                    try:
                        bwq = int(bw_px) + 32
                        bwr, (bww, bwh) = tex(bwkey, wash_d, bwq, bwq)
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
                        # msbf.ring is cached in 16 progress buckets. The
                        # shader receives bucket midpoint ((p + .5) / 16) so
                        # each cached displayable looks centered in its slice.
                        pb = int(prog * 15.999)
                        wkey = (rkey_name, pb)
                        ring_d = self._misc(wkey, (lambda q=quad, p=pb, c=col, th=thick, i2=inten: Transform(
                            Solid("#00000000"), xysize=(q, q), shader="msbf.ring",
                            u_progress=(p + 0.5) / 16.0, u_color=c,
                            u_thickness=th, u_intensity=i2)))
                        try:
                            wr, (ww, wh) = tex(wkey, ring_d, quad, quad)
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
                        # Same 16-bucket ring cache as the bomb. aget is local
                        # age since this specific explosion started.
                        pb2 = int(aget / 46.0 * 15.999)
                        vkey = ("winring", quad, pb2, col)
                        ring_v = self._misc(vkey, (lambda q=quad, p=pb2, c=col: Transform(
                            Solid("#00000000"), xysize=(q, q), shader="msbf.ring",
                            u_progress=(p + 0.5) / 16.0, u_color=c,
                            u_thickness=0.14, u_intensity=1.3)))
                        try:
                            vr_, (vw_, vh_) = tex(vkey, ring_v, quad, quad)
                            sblit(vr_, (g.bx - vw_ / 2.0, g.by + bob - vh_ / 2.0))
                        except Exception:
                            pass

            # --- event shockwaves (declare / capture / bar break) -------------
            # Each queued ring expands over 46 ticks from where it was fired.
            # Same 16-bucket msbf.ring cache as the bomb/victory booms.
            if MSBF_FX_SHADERS and g.ring_fx:
                for rf in g.ring_fx:
                    raged = g.tick - rf["born"]
                    if raged < 0 or raged >= 46:
                        continue
                    rp = int(raged / 46.0 * 15.999)
                    rq = rf["quad"]
                    ekey = ("evtring", rq, rp, rf["col"])
                    ring_e = self._misc(ekey, (lambda q=rq, p=rp, c=rf["col"]: Transform(
                        Solid("#00000000"), xysize=(q, q), shader="msbf.ring",
                        u_progress=(p + 0.5) / 16.0, u_color=c,
                        u_thickness=0.12, u_intensity=1.2)))
                    try:
                        er_, (ew_, eh_) = tex(ekey, ring_e, rq, rq)
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
                    # Red pichun ring expands for 46 ticks, again quantized to
                    # 16 buckets so repeated deaths reuse shader displayables.
                    p3 = int(aged / 46.0 * 15.999)
                    dkey = ("deathring", p3)
                    ring_dx = self._misc(dkey, (lambda p=p3: Transform(
                        Solid("#00000000"), xysize=(520, 520), shader="msbf.ring",
                        u_progress=(p + 0.5) / 16.0, u_color=(1.0, 0.35, 0.45),
                        u_thickness=0.16, u_intensity=1.35)))
                    try:
                        dr_, (dw_, dh_) = tex(dkey, ring_dx, 520, 520)
                        sblit(dr_, (dfx["x"] - dw_ / 2.0, dfx["y"] - dh_ / 2.0))
                    except Exception:
                        pass
                if aged < 12:
                    # Tiny white flare at the death point, shrinking by using
                    # smaller cached orb scales instead of a custom animation.
                    sqv = max(2, 8 - (aged // 2))
                    fkey = ("orb", 13, 0, sqv)
                    fr3, (fw3, fh3) = tex(fkey, self._bullet_tf("orb", 13, 0, sqv))
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
                if self.ptrail and not g.focus:
                    p0x, p0y = self.ptrail[0]
                    if abs(g.px - p0x) + abs(g.py - p0y) > 9.0:
                        pghost = self._misc("player_ghost", lambda: Transform(
                            KT_DIR + "player.png", zoom=3.0, nearest=True,
                            subpixel=True, alpha=0.20))
                        pgr, (pgw, pgh) = tex("player_ghost", pghost, 64, 64)
                        for gx, gy in self.ptrail[:-1]:
                            sblit(pgr, (gx - pgw / 2.0, gy - pgh / 2.0))
                if not blink_off:
                    # During the deathbomb window the ship burns white-hot --
                    # the "you just got clipped, X NOW" telegraph.
                    if g.dying_tick is not None:
                        pl = self._misc("player_hit", lambda: Transform(
                            KT_DIR + "player.png", zoom=3.0, nearest=True, subpixel=True,
                            matrixcolor=BrightnessMatrix(0.85)))
                        plkey = "player_hit"
                    else:
                        pl = self._misc("player", lambda: Transform(
                            KT_DIR + "player.png", zoom=3.0, nearest=True, subpixel=True))
                        plkey = "player"
                    plr, (plw, plh) = tex(plkey, pl, 64, 64)
                    sblit(plr, (g.px - plw / 2.0, g.py - plh / 2.0))
                if g.focus:
                    # Focus sigil: a small, fast copy of the boss spell circle
                    # spinning under the ship (the classic hitbox sigil), with
                    # the blob ring kept as the no-shader fallback.
                    drew_sigil = False
                    if KT_SHADER_OK:
                        try:
                            fs = int(58.0 + 3.0 * math.sin(tb * 0.15))
                            fsig = Transform(Solid("#00000000"), xysize=(fs, fs),
                                            shader="koto.circle",
                                            u_koto_col=Color("#ff3b73").rgb,
                                            u_koto_alpha=0.85, u_koto_spin=3.2)
                            fsr = renpy.render(fsig, fs, fs, st, at)
                            rv.depends_on(fsr)
                            fsw, fsh = fsr.get_size()
                            sblit(fsr, (g.px - fsw / 2.0, g.py - fsh / 2.0))
                            drew_sigil = True
                        except Exception:
                            pass
                    if not drew_sigil:
                        fring = self._misc("focus_ring", lambda: Transform(
                            EMB_DIR + "bullet.png", zoom=1.7, subpixel=True,
                            matrixcolor=TintMatrix("#ff3b73"), alpha=0.5))
                        fr, (fw, fh) = tex("focus_ring", fring, 48, 48)
                        sblit(fr, (g.px - fw / 2.0, g.py - fh / 2.0))
                    hb = self._misc("hitbox", lambda: Transform(
                        EMB_DIR + "bullet.png", zoom=0.5, subpixel=True))
                    hr_, (hw, hh) = tex("hitbox", hb, 24, 24)
                    sblit(hr_, (g.px - hw / 2.0, g.py - hh / 2.0))
                # Graze pulse: a cyan ripple pops off the ship for 8 ticks after
                # every graze -- close calls FEEL paid. Eight cached transforms
                # total (one per age step), keyed on the tick delta.
                gpa = g.tick - g.graze_tick
                if 0 <= gpa < 8:
                    gkey = ("grzp", gpa)
                    gp_d = self._misc(gkey, (lambda a4=gpa: Transform(
                        EMB_DIR + "bullet.png", zoom=0.9 + a4 * 0.24, subpixel=True,
                        matrixcolor=TintMatrix("#5cd7ff"), alpha=0.44 - a4 * 0.05)))
                    gpr, (gpw, gph) = tex(gkey, gp_d, 72, 72)
                    sblit(gpr, (g.px - gpw / 2.0, g.py - gph / 2.0))

            # --- spell-5 darkness (GPU spotlight) ------------------------------
            if g.dark > 0.02 and KT_SHADER_OK:
                try:
                    dark_d = Transform(Solid("#000000"), xysize=(KT_W, KT_H),
                                        shader="koto.spotlight",
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
            # Boss HP bar + remaining-bar pips + spell timer.
            if g.phase in ("nonspell", "declare", "spell"):
                bw_ = KT_W - 20
                stage.blit(rect("#0a1220dd", bw_, 10), (10, 8))
                frac = kt_clamp(g.boss_hp / g.boss_hp_max, 0.0, 1.0)
                # Chip ghost: a pale segment lags behind the true fill (snaps
                # UP instantly on a new bar), so burst damage reads as a bite
                # being taken out of her instead of the bar just being shorter.
                if frac > self._hp_ghost:
                    self._hp_ghost = frac
                else:
                    self._hp_ghost += (frac - self._hp_ghost) * 0.06
                # The spell half of the bar renders dimmer so the 50% flip is
                # readable at a glance.
                fill_w = int(bw_ * frac)
                ghost_w = int(bw_ * self._hp_ghost)
                if ghost_w > fill_w:
                    stage.blit(rect("#f5faff3c", ghost_w - fill_w, 10), (10 + fill_w, 8))
                if fill_w > 0:
                    stage.blit(rect(KT_PAL[bar["color"]], fill_w, 10), (10, 8))
                    stage.blit(rect("#f5faff", 2, 10), (10 + fill_w - 1, 8))
                half_x = 10 + bw_ // 2
                stage.blit(rect("#02040b", 2, 14), (half_x, 6))
                if g.endless:
                    # No fixed bar count in endless -- show the wave instead.
                    wvr, (wvw, wvh) = tex(("wave_hud", g.endless_wave),
                                        self._text("WAVE %d" % (g.endless_wave + 1), 15, "#ffd7e8", True, True), 170, 26)
                    sblit(wvr, (16, 26))
                elif g.debug_wave is not None:
                    # Wave viewer: name the forced pairing instead of bar pips.
                    dv = "VIEWING  NS %d / SP %d" % (g.debug_wave[0] + 1, g.debug_wave[1] + 1)
                    dvr, (dvw, dvh) = tex(("t", "dbwave", dv),
                                        self._text(dv, 15, "#ffb84a", True, True), 260, 26)
                    sblit(dvr, (16, 26))
                else:
                    pips = len(KT_BARS) - g.bar_index - 1
                    for i in range(pips):
                        pkey = ("orb", 1, 0, 3)
                        pr2, (pw2, ph2) = tex(pkey, self._bullet_tf("orb", 1, 0, 3))
                        sblit(pr2, (16 + i * 16 - pw2 / 2.0 + 6, 30.0 - ph2 / 2.0))
                secs = max(0, g.time_left // 60)
                tcol = "#ff5c6a" if secs <= 10 else "#f5faff"
                tr, (tw, th) = tex(("timer", secs, tcol),
                                    self._text("%02d" % secs, 22, tcol), 72, 34)
                stage.blit(tr, (KT_W - tw - 12, 24))
                # Live capture-bonus ticker (classic Touhou): what the card is
                # worth RIGHT NOW, draining with the clock, greyed the moment
                # the bonus is forfeit. Quantized to 5000s so the text cache
                # sees a few strings per second, not sixty.
                if g.phase == "spell":
                    if g.spell_ok:
                        bfrac = kt_clamp(g.time_left / float(max(1, g.cur_sp_time)), 0.0, 1.0)
                        bval = int(g.cur_value * (0.30 + 0.70 * bfrac))
                        bval -= bval % 5000
                        btxt = "BONUS " + format(bval, ",")
                        bcol = "#ffd7e8"
                    else:
                        btxt = "BONUS ----"
                        bcol = "#9aa8bd"
                    bkr, (bkw, bkh) = tex(("sbonus", btxt),
                                        self._text(btxt, 12, bcol, True), 240, 24)
                    stage.blit(bkr, (KT_W - bkw - 12, 54))

            # Spell card name: big + centred while declaring, parked top-left
            # while the card runs.
            if g.phase == "declare":
                pt = g.phase_tick
                # Portrait cut-in: her card-colour silhouette sweeps across the
                # stage behind the declaration (one cached texture -- only the
                # blit position moves), riding between two thin framing rails.
                cin_key = ("cutin", bar["color"])
                cin = self._misc(cin_key, (lambda c=bar["color"]: Transform(
                    KT_BOSS_FRAMES[KT_BOSS_CAST][2], zoom=3.6, nearest=True,
                    subpixel=True, matrixcolor=TintMatrix(KT_PAL[c]), alpha=0.22)))
                cir, (ciw, cih) = tex(cin_key, cin, 640, 720)
                sblit(cir, (KT_W + 150.0 - pt * 10.5 - ciw / 2.0, 235.0 - cih / 2.0))
                stage.blit(rect(KT_PAL[bar["color"]] + "26", KT_W, 2), (0, 168))
                stage.blit(rect(KT_PAL[bar["color"]] + "26", KT_W, 2), (0, 300))
                # Mask cards declare as MASK CARD, soul cards as SOUL CARD --
                # the one-frame tell that an Endless-exclusive is about to be
                # read at you.
                if g.cur_is_soul:
                    kick_label = "SOUL CARD"
                elif g.cur_is_mask:
                    kick_label = "MASK CARD"
                else:
                    kick_label = "SPELL CARD"
                kick, (kw2, kh2) = tex(("t", "kick", kick_label), self._text(kick_label, 15, KT_PAL[bar["color"]], True, True), 200, 28)
                a = kt_clamp(pt / 18.0, 0.0, 1.0)
                card_lines = self._card_lines(bar["card"])
                yy = 210.0 - (1.0 - a) * 26.0
                if (pt // 3) % 4 != 0 or pt > 24:
                    stage.blit(kick, (int(KT_W / 2 - kw2 / 2), int(yy - 32)))
                    line_y = int(yy)
                    for i, line in enumerate(card_lines):
                        size = self._size_for_line(line, 27, 21)
                        nr, (nw, nh) = tex(("cardname", g.bar_index, i, size),
                                            self._text(line, size, "#f5faff", True, True), KT_W - 44, 46)
                        stage.blit(nr, (int(KT_W / 2 - nw / 2), line_y))
                        line_y += nh + 4
                flash = kt_clamp((8 - pt) / 8.0, 0.0, 1.0)
                if flash > 0.0:
                    stage.blit(rect("#f5faff" + ("%02x" % int(flash * 110)), KT_W, KT_H), (0, 0))
            elif g.phase == "spell":
                card_lines = self._card_lines(bar["card"])
                line_y = 44
                for i, line in enumerate(card_lines):
                    size = self._size_for_line(line, 16 if i == 0 else 15, 12)
                    color = KT_PAL[bar["color"]] if i == 0 and len(card_lines) > 1 else "#ffd7e8"
                    nr, (nw, nh) = tex(("cardname_sm", g.bar_index, i, size),
                                        self._text(line, size, color, True, True), KT_W - 130, 28)
                    stage.blit(nr, (14, line_y))
                    line_y += nh + 2
                if not g.spell_ok:
                    fr2, (fw2, fh2) = tex(("t", "nobonus"), self._text("BONUS FAILED", 11, "#9aa8bd", True), 140, 24)
                    stage.blit(fr2, (14, line_y + 2))

            # Enemy position marker on the bottom lip (Touhou's "Enemy" carat).
            if boss_on and g.phase in ("nonspell", "spell", "declare"):
                stage.blit(rect("#ff8fc8", 26, 5), (int(g.bx) - 13, KT_H - 7))

            # Banners (EXTEND! / SPELL CARD CAPTURED! / +1 BOMB...), rising+fading.
            for bn in g.banners:
                age = g.tick - bn["born"]
                if age > bn["ttl"]:
                    continue
                frac = age / float(bn["ttl"])
                ab = 3 - min(3, int(frac * 4.0))
                bsize = self._size_for_line(bn["text"], bn["size"], 22)
                bnr, (bnw, bnh) = tex(("banner", bn["text"], bn["ci"], bsize, ab),
                                        self._text(bn["text"], bsize, KT_PAL[bn["ci"]], True, True), KT_W - 36, 72)
                stage.blit(bnr, (int(KT_W / 2 - bnw / 2), int(bn["y"] - frac * 20.0)))

            # Intro nameplate / end cards.
            if g.phase == "intro":
                pt = g.phase_tick
                if pt > 20:
                    n1, (w1, h1) = tex(("t", "koto1"), self._text("KATSURA  KOTONOHA", 34, "#ff8fc8", True, True), 520, 62)
                    stage.blit(n1, (int(KT_W / 2 - w1 / 2), 250))
                if pt > 50:
                    sub = "Endless Reading  --  No Last Page" if g.endless else "The Last Word Etched"
                    n2, (w2, h2) = tex(("t", "koto2", g.endless), self._text(sub, 17, "#f5faff", True), 480, 34)
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

            if g.paused:
                stage.blit(rect("#000000aa", KT_W, KT_H), (0, 0))
                box_w = 410
                box_h = 138
                box_x = int(KT_W / 2 - box_w / 2)
                box_y = 252
                stage.blit(rect("#02040bd2", box_w, box_h), (box_x, box_y))
                stage.blit(rect("#ff8fc855", box_w, 2), (box_x, box_y))
                stage.blit(rect("#ff8fc82f", box_w, 2), (box_x, box_y + box_h - 2))
                p1, (w1, h1) = tex(("t", "pause1"), self._text("PAUSED", 36, "#f5faff", True, True), 320, 62)
                stage.blit(p1, (int(KT_W / 2 - w1 / 2), box_y + 24))
                cmds = [("ESC:", "RESUME"), ("Q:", "GIVE UP")]
                parts = []
                total_w = -46
                for keycap, action in cmds:
                    # Measure/render each text fragment first, then center the
                    # combined row manually. This avoids relying on a screen
                    # language hbox inside the CDD.
                    kr, (kw, kh) = tex(("pause_key", keycap), self._text(keycap, 14, "#ff8fc8", True, True), 72, 26)
                    ar, (aw, ah) = tex(("pause_action", action), self._text(action, 14, "#9aa8bd", True, True), 124, 26)
                    parts.append((kr, kw, kh, ar, aw, ah))
                    total_w += kw + 8 + aw + 46
                x = int(KT_W / 2 - total_w / 2)
                y2 = box_y + 88
                for kr, kw, kh, ar, aw, ah in parts:
                    stage.blit(kr, (x, y2))
                    stage.blit(ar, (x + kw + 8, y2))
                    x += kw + 8 + aw + 46

            # Clip the stage (bullets live 70px past the lip) and mount it.
            # A live bomb rocks the whole playfield: a decaying two-axis shake
            # on the mount position (Touhou screen-quake). The few px of
            # overlap with the chrome during the kick reads as impact.
            mx_, my_ = KT_SX, KT_SY
            if g.bomb_tick is not None:
                bt2 = g.tick - g.bomb_tick
                if bt2 < 54:
                    amp = 6.0 * (1.0 - bt2 / 54.0)
                    mx_ += math.sin(bt2 * 1.9) * amp
                    my_ += math.cos(bt2 * 2.6) * amp * 0.6
            rv.blit(stage.subsurface((0, 0, KT_W, KT_H)), (mx_, my_))

            # --- side HUD (screen space, right panel) ---------------------------
            hx = KT_SX + KT_W + 42
            # Panel spine: a card-colour rail with a soft pink echo, so the
            # score panel always carries the current card's accent.
            rv.blit(rect(KT_PAL[g.cur_color] + "3c", 3, 604), (hx - 24, 58))
            rv.blit(rect("#ff8fc81e", 1, 604), (hx - 18, 58))
            # Endless keeps its own hi-score; the fixed run keeps the other.
            hi_best = (persistent.kotomode_endless_hiscore if g.endless else persistent.kotomode_hiscore) or 0
            hi = max(g.score, hi_best)
            rows = [
                ("HI SCORE", format(hi, ",")),
                ("SCORE", format(g.score, ",")),
            ]
            y = 66
            for label, val in rows:
                lr, (lw, lh) = tex(("t", "lbl" + label), self._text(label, 15, "#ff8fc8", True, True), 180, 28)
                rv.blit(lr, (hx, y))
                vr, (vw, vh) = tex(("hudval", label, val), self._text(val, 24, "#f5faff", True), 280, 42)
                rv.blit(vr, (hx + 24, y + 22))
                y += 66
            # Lives (hearts) + bombs (daggers).
            lr, (lw, lh) = tex(("t", "lives"), self._text("PLAYER", 15, "#ff8fc8", True, True), 180, 28)
            rv.blit(lr, (hx, y))
            heart = self._misc("life_icon", lambda: Transform(
                KT_DIR + "player.png", zoom=2.2, nearest=True))
            hr2, (hw2, hh2) = tex("life_icon", heart, 48, 48)
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
            bomb_i = self._misc("bomb_icon", lambda: Transform(
                KT_DIR + "bomb.png", zoom=2.4, nearest=True))
            bir, (biw, bih) = tex("bomb_icon", bomb_i, 48, 48)
            for i in range(g.bombs):
                rv.blit(bir, (hx + 24 + i * (biw + 10), y + 24))
            y += 70
            if g.endless:
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
                vr3, (vw3, vh3) = tex(("hudval2", label, val), self._text(val, 18, "#f5faff", True), 120, 30)
                rv.blit(vr3, (hx + 110, y - 2))
                y += 36
            # Mode chip: which reading this is, wearing its own colour, with a
            # small pip of the same colour as a bullet-point.
            if g.endless or g.practice or g.debug or g.debug_wave is not None:
                if g.debug_wave is not None:
                    tag, tcol2 = "WAVE VIEWER", "#ffb84a"
                elif g.debug:
                    tag, tcol2 = "DEBUG READING", "#ffb84a"
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

screen kototouhou_screen(game):
    modal True
    use enter_m_input_lock()

    # Endless Mode is not played at her shrine -- it gets its own arena.
    add ("koto_backdrop_endless" if game.endless else "koto_backdrop") at kt_backdrop_breathe

    # Panel masks around the playfield.
    add Solid("#02040bd9") xpos 0 ypos 0 xsize KT_SX ysize 720
    add Solid("#02040bd9") xpos (KT_SX + KT_W) ypos 0 xsize (1280 - KT_SX - KT_W) ysize 720
    add Solid("#02040bd9") xpos KT_SX ypos 0 xsize KT_W ysize KT_SY
    add Solid("#02040bd9") xpos KT_SX ypos (KT_SY + KT_H) xsize KT_W ysize (720 - KT_SY - KT_H)

    # Stage chrome: main frame, then a quieter outer hairline and white corner
    # ticks so the cabinet reads as bespoke trim rather than four bare strips.
    # All static Solids -- nothing here rebuilds or animates.
    add Solid("#ff8fc866") xpos (KT_SX - 2) ypos (KT_SY - 2) xsize (KT_W + 4) ysize 2
    add Solid("#ff8fc866") xpos (KT_SX - 2) ypos (KT_SY + KT_H) xsize (KT_W + 4) ysize 2
    add Solid("#ff8fc866") xpos (KT_SX - 2) ypos KT_SY xsize 2 ysize KT_H
    add Solid("#ff8fc866") xpos (KT_SX + KT_W) ypos KT_SY xsize 2 ysize KT_H
    add Solid("#ff8fc822") xpos (KT_SX - 7) ypos (KT_SY - 7) xsize (KT_W + 14) ysize 1
    add Solid("#ff8fc822") xpos (KT_SX - 7) ypos (KT_SY + KT_H + 6) xsize (KT_W + 14) ysize 1
    add Solid("#ff8fc822") xpos (KT_SX - 7) ypos (KT_SY - 7) xsize 1 ysize (KT_H + 14)
    add Solid("#ff8fc822") xpos (KT_SX + KT_W + 6) ypos (KT_SY - 7) xsize 1 ysize (KT_H + 14)
    add Solid("#f5faff66") xpos (KT_SX - 7) ypos (KT_SY - 7) xsize 14 ysize 2
    add Solid("#f5faff66") xpos (KT_SX - 7) ypos (KT_SY - 7) xsize 2 ysize 14
    add Solid("#f5faff66") xpos (KT_SX + KT_W - 7) ypos (KT_SY - 7) xsize 14 ysize 2
    add Solid("#f5faff66") xpos (KT_SX + KT_W + 5) ypos (KT_SY - 7) xsize 2 ysize 14
    add Solid("#f5faff66") xpos (KT_SX - 7) ypos (KT_SY + KT_H + 5) xsize 14 ysize 2
    add Solid("#f5faff66") xpos (KT_SX - 7) ypos (KT_SY + KT_H - 7) xsize 2 ysize 14
    add Solid("#f5faff66") xpos (KT_SX + KT_W - 7) ypos (KT_SY + KT_H + 5) xsize 14 ysize 2
    add Solid("#f5faff66") xpos (KT_SX + KT_W + 5) ypos (KT_SY + KT_H - 7) xsize 2 ysize 14

    # THE game.
    add KTStage(game)

    # Right-panel footer.
    text "KATSURA  KOTONOHA" style "msbf_shmup_card_kicker":
        xpos (KT_SX + KT_W + 42)
        ypos 26
    text "Z SHOOT   X BOMB   ARROWS MOVE   SHIFT FOCUS   ESC PAUSE" style "msbf_shmup_controls_small":
        xpos (KT_SX + KT_W + 42)
        ypos 690

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
    window auto

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
            play music enterm
            scene bg ether with dissolve_scene_full
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
            # Drop the say window before the modal picker. A lingering window-auto
            # box flashes the default (missing) textbox as a checkerboard over the
            # viewer, and its stray dismiss can end the picker interaction with
            # True. Every other call screen in this file pairs with window hide.
            window hide
            $ _kt_pick = kt_debug_wave_pick()
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
    window hide

    # This is a normal keyboard notice screen before the CDD takes over.
    # The actual fight does not use the dialogue window or quick menu.
    call screen koto_keyboard_notice

label kototouhou_fight:
    window hide
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
    # sanctioned way to test these without an hour of legit play, and the debug
    # option only exists in developer builds. Debug keeps the RECORDS
    # pencil-only ("debugger's ink doesn't keep": _finish leaves
    # kotomode_cleared/hiscore untouched), so the Eight Bars clear is granted
    # directly here on debug instead of derived from the flag.
    if _kt_result == "victory" and not (kt_last_practice or kt_last_endless):
        if kt_last_debug:
            $ ach_grant("koto_clear")
        if kt_last_deaths == 0:
            $ ach_grant("koto_nomiss")
        if kt_last_captures >= 8:
            $ ach_grant("koto_allcaps")
    # And sync the derived ones this run just satisfied (Eight Bars from
    # kotomode_cleared, set moments ago in _finish on a real run) so they toast
    # here, not at the next Archive open.
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
    window auto
    scene koto_backdrop with dissolve_scene_full
    play music dream
    show kotonoha neut at t11 zorder 2
    ko "...And that's that page, cover to cover."
    ko "Well? Another one? Or shall we read it properly this time?"
    jump kototouhou_mode_select

label kototouhou_defeat:
    window auto
    # The displayable is gone now; use the snapshot fields KTGame._finish()
    # copied into the store.
    $ kt_score_str = format(kt_last_score, ",")
    $ kt_defeat_bar = kt_last_bar_index + 1
    # _finish already folded this run into the persistent records, so sync now:
    # the endless-mode achievements (Pro Gamer / No Curtain Call) are earned in
    # runs that END here, and shouldn't wait for the next Archive open to toast.
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
                window hide
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
            window hide
            jump kototouhou_fight
        "Leave.":
            ko "...I understand. It was a lot. It's always a lot."
            ko "The stage will keep, but so will I."
            scene black with dissolve_scene_full
            return

label kototouhou_quit:
    window auto
    ko "You stopped mid-sentence."
    ko "...That's ruder than dying, you know."

    menu:
        "Sorry. Deal me back in.":
            $ kt_continue_bar = 0
            $ kt_continues = 0
            ko "Forgiven. Completely. Instantly. ...Don't do it again."
            scene black with dissolve_scene_full
            window hide
            jump kototouhou_fight
        "I need to go.":
            ko "Then go. I'll reread the opening by myself."
            scene black with dissolve_scene_full
            return

label kototouhou_victory:
    window auto
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
    play music enterm
    scene bg ether with dissolve_scene_full
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
