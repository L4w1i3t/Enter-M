# =============================================================================
# mc_reveal_fx.rpy  --  THE PULL CINEMATIC
# =============================================================================
#
# WHAT THIS FILE IS
#   The spectacle between paying and seeing what you got. mc_gacha.rpy owns the
#   machine, the odds and the results wall; this file owns the twenty to thirty
#   frames in the middle that make a pull feel like an event instead of a
#   transaction.
#
# THE SHAPE OF A PULL  (this is the genre's structure, not an invention)
#   DROP     the capsule falls out of the chute and settles.
#   CHARGE   it winds up, ringed by light. The COLOUR of that light is the tell.
#   ESCALATE the tell can UPGRADE mid-charge -- steel to violet to gold. An SSR
#            climbs all three rungs, so the moment the light changes is the
#            moment the player already knows, and that anticipation is the
#            single most valuable beat a gacha reveal has. An R never climbs, so
#            the ladder means something.
#   BURST    god rays, a shockwave, a screen flash and a shake, keyed to tier.
#   WALL     mc_gacha.rpy's reveal, where the cards flip face-up one by one.
#
# RARITY GRADES THE WHOLE THING
#   An R pull is one short rung and a modest pop (about 1.2s). An SSR climbs
#   three rungs and detonates (about 3.0s). Nothing about the sequence is
#   uniform, because a reveal that costs the same time whatever it produced
#   trains the player to skip all of them.
#
# AND IT IS ALWAYS SKIPPABLE
#   Click, Enter or Escape at ANY point jumps straight to the finished wall with
#   every card already face-up. There is also a speed control on the machine
#   (FULL / FAST / OFF) written to persistent.mc_fx_speed -- this is a screen
#   somebody will see several hundred times, and a spectacle you cannot turn
#   down stops being one.
#
# SHADERS  (namespace: mcg.*)
#   mcg.orb   : the charge aura -- core glow plus rings converging inward.
#   mcg.burst : the blowout -- angular god rays, an expanding shockwave, a
#               central flash.
#   Both follow the house rules: registered at init -10, driven by an OPAQUE
#   Solid base at a known xysize so the mesh is not culled, every animated
#   uniform ATL-interpolated rather than keyed to u_time (a settled screen asks
#   for no frames, so a u_time effect freezes and snaps), and both output
#   PREMULTIPLIED alpha -- `min(col, vec3(a))` -- or the plate rectangle shows
#   up as a glowing box over everything behind it.
#   register_shader runs in `init python`, which does NOT re-run on hot reload:
#   editing the GLSL below needs a full restart, not a Shift+R.
# =============================================================================


init -10 python:
    def _mc_fx_register_shaders():

        # ---- orb: the charge aura ------------------------------------------
        # A core that brightens with u_charge, plus three rings sweeping inward
        # as it rises. The rings are keyed to u_charge and NOT to time, so they
        # are a readout of how wound-up the pull is rather than idle decoration.
        renpy.register_shader("mcg.orb", variables="""
            uniform vec2 u_model_size;
            uniform vec4 u_color;
            uniform float u_charge;
            uniform float u_rings;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 uv = v_tex_coord * u_model_size;
            vec2 c = u_model_size * 0.5;
            float r = length(uv - c) / (min(u_model_size.x, u_model_size.y) * 0.5);

            float core = exp(-r * r * 7.0) * (0.20 + 0.62 * u_charge);

            float rings = 0.0;
            for (int i = 0; i < 3; i++) {
                float t = fract(u_charge * 1.7 + float(i) * 0.3333);
                float rr = 0.90 - t * 0.84;
                rings += smoothstep(0.055, 0.0, abs(r - rr)) * (1.0 - t);
            }

            float a = clamp(core + rings * u_rings * 0.9, 0.0, 1.0);
            a *= smoothstep(0.99, 0.82, r);

            vec3 col = u_color.rgb * (0.60 + 0.70 * a);
            gl_FragColor = vec4(min(col * a, vec3(a)), a);
        """)

        # ---- burst: the blowout --------------------------------------------
        # Three layers on one pass: an angular comb sharpened into god rays, a
        # shockwave ring travelling outward and thinning as it goes, and a
        # central flash the caller drives separately so the white peak can be
        # timed against the shake rather than against the ring.
        renpy.register_shader("mcg.burst", variables="""
            uniform vec2 u_model_size;
            uniform vec4 u_color;
            uniform float u_progress;
            uniform float u_rays;
            uniform float u_flash;
            varying vec2 v_tex_coord;
        """, fragment_300="""
            vec2 uv = v_tex_coord * u_model_size;
            vec2 c = u_model_size * 0.5;
            vec2 d = uv - c;
            float r = length(d) / (u_model_size.y * 0.5);
            float ang = atan(d.y, d.x);
            float p = clamp(u_progress, 0.0, 1.0);

            // Two combs at different frequencies, not one. A single comb
            // draws evenly spaced spokes and reads as a wheel; laying a few
            // FAT rays over many thin ones is what makes it read as light.
            float comb_fine = sin(ang * 18.0 + p * 2.4);
            float comb_wide = sin(ang * 7.0 - p * 1.3);
            float rays = pow(max(comb_fine, 0.0), 6.0) * 0.72
                    + pow(max(comb_wide, 0.0), 10.0) * 0.60;
            rays *= smoothstep(0.02, 0.30, r) * smoothstep(2.0, 0.40, r);
            rays *= u_rays * (1.0 - p * 0.85);

            float rr = p * 2.1;
            float ring = smoothstep(0.15 * (1.0 - p) + 0.015, 0.0, abs(r - rr));
            ring *= (1.0 - p) * 1.25;

            float flash = exp(-r * r * 2.6) * u_flash;

            float a = clamp(rays * 0.80 + ring + flash, 0.0, 1.0);
            vec3 col = mix(u_color.rgb, vec3(1.0), clamp(0.40 * flash + 0.30 * ring, 0.0, 1.0));
            gl_FragColor = vec4(min(col * a, vec3(a)), a);
        """)

    try:
        _mc_fx_register_shaders()
        MC_FX_SHADERS = True
    except Exception as _mc_fx_e:
        MC_FX_SHADERS = False
        if config.developer:
            renpy.log("MC FX: shader registration failed: %r" % (_mc_fx_e,))


# =============================================================================
# THE LADDER, THE CLOCK, AND THE SPEED CONTROL
# =============================================================================

# FULL is the authored pacing. FAST keeps every beat and plays it at a bit under
# half length, which is what somebody grinding a hundred pulls actually wants.
# OFF skips the cinematic entirely AND lands the wall instantly.
default persistent.mc_fx_speed = "full"

init -3 python:

    MC_FX_SPEEDS = (
        ("full", "FULL",  1.00),
        ("fast", "FAST",  0.45),
        ("off",  "OFF",   0.00),
    )

    # Which rungs of the tier ladder a pull climbs. The batch's BEST card
    # decides, so a ten-pull carrying one SSR gets the full climb even though
    # nine of its cards are commons -- which is correct: the climb is a promise
    # about the batch, and the wall pays it off card by card.
    MC_FX_LADDER = {
        "r":   ("r",),
        "sr":  ("r", "sr"),
        "ssr": ("r", "sr", "ssr"),
    }

    # Seconds each rung is held, by rung INDEX. A later rung is held longer:
    # the whole point of an upgrade is that it gets to be looked at.
    MC_FX_RUNG_HOLD = (0.62, 0.66, 0.92)
    MC_FX_BURST_HOLD = {"r": 0.46, "sr": 0.62, "ssr": 0.86}

    def mc_fx_speed():
        """The stored speed key, defended against a stale persistent value."""
        key = getattr(persistent, "mc_fx_speed", "full")
        return key if key in dict((k, s) for k, _l, s in MC_FX_SPEEDS) else "full"

    def mc_fx_scale():
        """Seconds multiplier. 0.0 means the cinematic does not play at all."""
        for key, _label, scale in MC_FX_SPEEDS:
            if key == mc_fx_speed():
                return scale
        return 1.0

    def mc_fx_speed_label():
        for key, label, _scale in MC_FX_SPEEDS:
            if key == mc_fx_speed():
                return label
        return "FULL"

    def mc_fx_cycle_speed():
        """Button action on the machine: FULL -> FAST -> OFF -> FULL."""
        keys = [k for k, _l, _s in MC_FX_SPEEDS]
        try:
            index = keys.index(mc_fx_speed())
        except ValueError:
            index = 0
        persistent.mc_fx_speed = keys[(index + 1) % len(keys)]
        try:
            renpy.save_persistent()
        except Exception:
            pass
        mc_se("coin", 0.5)
        renpy.restart_interaction()
        return None

    def mc_fx_rungs(best):
        return MC_FX_LADDER.get(best, MC_FX_LADDER["r"])

    def mc_fx_hold(index):
        """How long rung `index` is held, already speed-scaled.

        Floored at 0.05 rather than allowed to reach zero: a Ren'Py timer with
        a delay of 0 or less raises, and a rung that has been scaled into
        nothing should still tick over rather than take the screen down."""
        base = MC_FX_RUNG_HOLD[min(index, len(MC_FX_RUNG_HOLD) - 1)]
        return max(0.05, base * mc_fx_scale())

    def mc_fx_burst_hold(best):
        return max(0.05, MC_FX_BURST_HOLD.get(best, 0.46) * mc_fx_scale())

    def mc_fx_should_play():
        """False when the player has turned the cinematic off."""
        return mc_fx_scale() > 0.0

    # ---- cues ---------------------------------------------------------------
    def mc_fx_rung_sound(index, total):
        """The rung-change sting. Climbing onto the LAST rung of a ladder that
        actually climbed is the upgrade moment, so it gets the bigger cue."""
        if index <= 0:
            return None
        if index >= total - 1 and total > 1:
            mc_se("fx_upgrade")
        else:
            mc_se("fx_charge")
        return None

    def mc_fx_burst_sound(best):
        """Two layers on purpose: a shared impact under a tier-specific sting,
        so every burst has weight and only the tier changes character."""
        mc_se("fx_impact", 0.9 if best == "ssr" else 0.6)
        mc_se(best if best in MC_SFX else "r")
        return None

    def mc_fx_advance_sound(next_phase, total, best):
        """One cue dispatcher for the phase timer, so the screen does not have
        to know that arriving past the last rung means the burst."""
        if next_phase >= total:
            return mc_fx_burst_sound(best)
        return mc_fx_rung_sound(next_phase, total)


# =============================================================================
# DISPLAYABLE FACTORIES
# Every one of these hands the shader an OPAQUE Solid at a known xysize: that
# is what defines u_model_size and what stops the mesh being culled before the
# fragment stage ever runs.
# =============================================================================
init -3 python:

    def McPlate(w, h):
        """
        An opaque base of exactly (w, h) for a shader ATL to run over.

        The shader and its uniforms live in the ATL transform, not here, because
        every uniform these effects use is ANIMATED -- and an animated uniform
        has to be interpolated by ATL (which requests a frame while it runs)
        rather than read off u_time (which does not, so it freezes on a settled
        screen and then snaps). Same split as the card's mc_card_fx_holo.
        """
        return Transform(Solid("#000000"), xysize=(int(w), int(h)))

    def McCardBack(w, h, radius=10.0):
        """
        The face-down card.

        Deliberately tier-NEUTRAL: the back is what the player stares at while
        they still do not know, so it must not leak the answer. The tier is
        spent entirely on the flip and the face.
        """
        w, h = int(w), int(h)
        return Fixed(
            ArcadePanel(w, h, top="#2a2150", bottom="#140e2a",
                        radius=radius, border=1.5, border_color="#ffb45455"),
            Transform(
                ArcadePanel(int(w * 0.74), int(h * 0.80), top="#00000000",
                            bottom="#00000000", radius=radius * 0.8,
                            border=1.0, border_color="#ffb45433"),
                align=(0.5, 0.5),
            ),
            Transform(MatsucoinIcon(int(h * 0.30)), align=(0.5, 0.5), alpha=0.55),
            xysize=(w, h),
        )

    def McGachaCapsule(size):
        """
        The capsule, as a plastic object rather than a coloured disc.

        A true two-hemisphere capsule needs clipping Ren'Py will not give a
        rounded rect, so this sells it the way the shape actually reads: a
        vertical gradient body (lit from above), a SEAM across the middle, and
        one specular highlight. Tier-NEUTRAL, like the card back -- the LIGHT is
        the tell, the plastic is just plastic.
        """
        s = int(size)
        seam_h = max(3, int(s * 0.045))
        hi_w, hi_h = int(s * 0.34), int(s * 0.22)

        return Fixed(
            ArcadePanel(s, s, top="#9c92dc", bottom="#2a2250", radius=s / 2.0,
                        border=1.5, border_color="#d8d0ff55"),
            # Short of the full width on purpose: the shell's edge is
            # antialiased and carries a border, so a seam drawn to the true
            # diameter reads as overhanging the silhouette rather than lying
            # on it.
            Transform(
                ArcadePanel(int(s * 0.92), seam_h, top="#171036dd",
                            bottom="#0d0824dd", radius=seam_h / 2.0),
                align=(0.5, 0.5),
            ),
            Transform(
                ArcadePanel(hi_w, hi_h, top="#ffffff", bottom="#ffffff00",
                            radius=hi_h / 2.0),
                align=(0.30, 0.22),
                alpha=0.40,
            ),
            xysize=(s, s),
        )

    def McCapsuleCore(size, color):
        """The light building up INSIDE the capsule.

        Its own displayable rather than part of McGachaCapsule, because it is
        the one part of the capsule that IS tier-coloured -- and so the one part
        that has to be rebuilt on every rung while the shell around it keeps its
        drop animation running.
        """
        s = int(size)
        return ArcadePanel(s, s, top=color, bottom=color, radius=s / 2.0)

    # Where the charge motes start from. Precomputed because a screen has no
    # convenient place to do trigonometry and this never changes.
    #
    # The list is emitted in a SCATTERED order, not walking the circle: the
    # screen staggers each mote's launch by its index, so consecutive angles
    # would fire one after another round the rim and leave the whole first half
    # of the charge lit down one side only. A stride co-prime with the count
    # visits every angle exactly once while putting each launch nowhere near
    # the last. The radius alternates for the same reason -- a perfect ring of
    # start points reads as a mechanism rather than as loose energy.
    def mc_fx_mote_offsets(count=10, radius=250, stride=3, jitter=22):
        import math as _mc_fx_math
        step = (2.0 * _mc_fx_math.pi) / float(count)
        out = []
        for i in range(count):
            angle = step * ((i * stride) % count)
            r = radius + (jitter if i % 2 else -jitter)
            out.append((int(round(_mc_fx_math.cos(angle) * r)),
                        int(round(_mc_fx_math.sin(angle) * r))))
        return tuple(out)

    MC_FX_MOTES = mc_fx_mote_offsets(10, 250)


# =============================================================================
# ANIMATION
# Two rules run through all of it. Every animated uniform is ATL-interpolated,
# never keyed to u_time. And any transform meant to KEEP RUNNING across a phase
# change takes constant arguments -- a screen rebuild with different `at` args
# builds a different transform and restarts the ATL from the top, which is
# right for the per-rung wind-up and very wrong for the capsule that is
# supposed to still be sitting there.
# =============================================================================

# No-op, so an `at` conditional always has something to fall back to.
transform mc_fx_still:
    alpha 1.0

# The charge aura. Rebuilt on every rung ON PURPOSE: each rung is a fresh
# wind-up, and u_charge climbing 0 -> 1 is what drives the rings inward.
transform mc_fx_orb(col, dur, rings=1.0):
    subpixel True
    mesh True
    shader "mcg.orb"
    u_color col
    u_rings rings
    u_charge 0.0
    linear dur u_charge 1.0

# The blowout. u_progress drives the rays and the shockwave; u_flash is its own
# fast spike so the white peak can be timed against the shake rather than
# against the ring. Separate parallel blocks, and they touch DISJOINT
# properties -- two parallel blocks animating the same property fight.
transform mc_fx_burst(col, dur):
    subpixel True
    mesh True
    shader "mcg.burst"
    u_color col
    u_rays 1.0
    u_progress 0.0
    u_flash 0.0
    parallel:
        linear dur u_progress 1.0
    parallel:
        linear (dur * 0.16) u_flash 1.0
        easeout (dur * 0.84) u_flash 0.0

# The capsule falling out of the chute, bouncing once, then breathing. Its
# argument is the pull's speed scale and nothing else, so it survives every
# rung change and keeps running instead of re-dropping.
transform mc_fx_capsule(dur):
    subpixel True
    alpha 0.0
    yoffset -280
    zoom 0.80
    parallel:
        easeout (dur * 0.45) alpha 1.0
    parallel:
        easein_quad (dur * 0.70) yoffset 22
        easeout_quad (dur * 0.16) yoffset -13
        easein_quad (dur * 0.14) yoffset 0
    parallel:
        easeout (dur * 0.70) zoom 1.0
        block:
            ease 0.55 zoom 1.05
            ease 0.55 zoom 1.0
            repeat

# ... and going up with the burst.
transform mc_fx_capsule_pop(dur):
    subpixel True
    zoom 1.0
    alpha 1.0
    parallel:
        easein_quad (dur * 0.32) zoom 1.60
    parallel:
        linear (dur * 0.32) alpha 0.0

# Impact shake. Hand-stepped rather than random so it reads the same every time
# and can be tuned by eye.
transform mc_fx_shake(mag=12.0, dur=0.5):
    subpixel True
    xoffset 0
    yoffset 0
    linear (dur * 0.06) xoffset mag yoffset (-mag * 0.6)
    linear (dur * 0.07) xoffset (-mag * 0.8) yoffset (mag * 0.5)
    linear (dur * 0.07) xoffset (mag * 0.55) yoffset (mag * 0.35)
    linear (dur * 0.08) xoffset (-mag * 0.32) yoffset (-mag * 0.22)
    linear (dur * 0.10) xoffset 0 yoffset 0

# The light inside the capsule, coming up with the charge. Rebuilt every rung
# along with its colour, which is exactly right -- each rung relights it.
transform mc_fx_core(dur):
    subpixel True
    alpha 0.0
    zoom 0.45
    parallel:
        easeout (dur * 0.85) alpha 0.80
    parallel:
        easeout dur zoom 1.0

# One mote of charge falling into the capsule. Ten of these on a stagger is what
# turns "a glowing ball" into "something is gathering here".
transform mc_fx_mote(dx, dy, delay, dur):
    subpixel True
    alpha 0.0
    xoffset dx
    yoffset dy
    zoom 1.0
    pause delay
    parallel:
        easeout (dur * 0.22) alpha 0.85
        linear (dur * 0.78) alpha 0.0
    parallel:
        easein_quad dur xoffset 0 yoffset 0
    parallel:
        linear dur zoom 0.30

# The tier wordmark arriving at the top of the burst.
transform mc_fx_banner_in:
    subpixel True
    alpha 0.0
    zoom 2.30
    easeout_quad 0.17 alpha 1.0 zoom 1.0
    block:
        ease 0.9 zoom 1.025
        ease 0.9 zoom 1.0
        repeat

# --- the card flip ----------------------------------------------------------
# A 2D flip: the back squashes to an edge, the face grows back out of it. Both
# halves are always in the tree and their ATL decides which is visible, so
# there is no swap to mistime.
#
# xzoom bottoms out at 0.02 rather than 0.0 (a zero-width render is degenerate),
# and both carry align 0.5 -- a Transform's default anchor is the top-left, so
# without it the card would squash toward its own left edge instead of its
# spine.
transform mc_fx_flip_back(delay=0.0, dur=0.26):
    subpixel True
    xalign 0.5
    yalign 0.5
    alpha 1.0
    xzoom 1.0
    pause delay
    easein_quad (dur * 0.5) xzoom 0.02
    alpha 0.0

transform mc_fx_flip_face(delay=0.0, dur=0.26):
    subpixel True
    xalign 0.5
    yalign 0.5
    alpha 0.0
    xzoom 0.02
    pause (delay + dur * 0.5)
    alpha 1.0
    easeout_quad (dur * 0.5) xzoom 1.0

# The rarity pop behind a card as it turns over.
transform mc_fx_card_pop(delay=0.0, dur=0.50):
    subpixel True
    alpha 0.0
    zoom 0.55
    pause delay
    parallel:
        easeout (dur * 0.26) alpha 0.9
        linear (dur * 0.74) alpha 0.0
    parallel:
        easeout dur zoom 1.40

# A card that turned out to be worth something gets a little kick as it lands.
transform mc_fx_card_kick(delay=0.0):
    subpixel True
    pause delay
    yoffset 0
    linear 0.05 yoffset -9
    easeout_quad 0.16 yoffset 0


# =============================================================================
# THE CINEMATIC
# =============================================================================
# PHASES
#   phase 0 .. n-1 : the rungs of the tier ladder, one wind-up each
#   phase n        : the burst, which then hands off to mc_reveal
#
# WHY THE TIMERS SIT INSIDE A `for`
#   A screen `timer` whose delay CHANGES between updates does not restart: the
#   new Timer is handed the old one as `replaces` and inherits its state, so it
#   keeps counting to the ORIGINAL delay and every rung after the first would
#   run at the first rung's length. Putting each phase's timer at its own loop
#   index gives it its own identity, so advancing a phase really does build a
#   fresh timer. (Verified against renpy/display/behavior.py.)
# =============================================================================
screen mc_pull_cinematic():

    modal True
    zorder 72

    default phase = 0

    python:
        _mcc_best = _mc_pull_rt.best
        _mcc_rungs = mc_fx_rungs(_mcc_best)
        _mcc_n = len(_mcc_rungs)
        _mcc_bursting = (phase >= _mcc_n)

        _mcc_key = _mcc_rungs[min(phase, _mcc_n - 1)]
        _mcc_tier = MC_RARITY[_mcc_key]
        _mcc_glow = _mcc_tier["glow"]
        _mcc_col = _mcc_tier["color"]

        _mcc_scale = mc_fx_scale()
        _mcc_burst_len = mc_fx_burst_hold(_mcc_best)

        # Every way out lands on the same place: the finished wall, every card
        # already face-up. A skip should never cost the player the result.
        _mcc_skip = [Hide("mc_pull_cinematic"), Show("mc_reveal", instant=True)]

    on "show" action Function(mc_se, "fx_drop", 0.8)

    dismiss action _mcc_skip
    key "K_ESCAPE" action _mcc_skip
    key "game_menu" action _mcc_skip
    key "K_RETURN" action _mcc_skip
    key "K_KP_ENTER" action _mcc_skip

    for _mcc_i in range(_mcc_n + 1):
        if phase == _mcc_i:
            if _mcc_i < _mcc_n:
                timer mc_fx_hold(_mcc_i) action [
                    SetScreenVariable("phase", _mcc_i + 1),
                    Function(mc_fx_advance_sound, _mcc_i + 1, _mcc_n, _mcc_best),
                ]
            else:
                timer _mcc_burst_len action [
                    Hide("mc_pull_cinematic"),
                    Show("mc_reveal"),
                ]

    # --- the field ------------------------------------------------------------
    add Solid("#04030bf4")
    add ArcadePanel(1280, 720, top=(_mcc_col + "22"), bottom="#00000000", radius=0)

    # --- everything that takes the hit ---------------------------------------
    fixed:
        xysize (1280, 720)
        at (mc_fx_shake(18.0 if _mcc_best == "ssr" else 11.0, _mcc_burst_len)
            if _mcc_bursting else mc_fx_still)

        # THE CAPSULE, and the light inside it.
        #
        # The shell is tier-NEUTRAL and its transform takes only the speed
        # scale, so it survives every rung rebuild and keeps sitting there
        # bouncing. Its CHILDREN are free to change with the tier -- swapping a
        # child does not touch the parent's own ATL state, which is the whole
        # reason the light is a separate displayable from the plastic.
        fixed:
            xysize (170, 170)
            align (0.5, 0.5)
            at (mc_fx_capsule_pop(_mcc_burst_len) if _mcc_bursting
                else mc_fx_capsule(max(0.05, 0.48 * _mcc_scale)))

            add McGachaCapsule(150) align (0.5, 0.5)

            if not _mcc_bursting:
                add McCapsuleCore(86, _mcc_glow):
                    align (0.5, 0.5)
                    at mc_fx_core(mc_fx_hold(phase))

        # The aura sits OVER the capsule, not under it: light spilling out
        # around a shell, rather than a shell punched out of a glow. It is
        # rebuilt every rung, and that rebuild IS the wind-up.
        if not _mcc_bursting:
            add McPlate(660, 660):
                align (0.5, 0.5)
                at mc_fx_orb(enter_m_rgba(_mcc_glow), mc_fx_hold(phase))

            # Charge falling in from around the edge of the frame.
            for _mcc_k, (_mcc_dx, _mcc_dy) in enumerate(MC_FX_MOTES):
                add McCapsuleCore(14, _mcc_glow):
                    align (0.5, 0.5)
                    at mc_fx_mote(_mcc_dx, _mcc_dy,
                                _mcc_k * 0.045 * _mcc_scale,
                                max(0.08, mc_fx_hold(phase) * 0.85))

        if _mcc_bursting:
            add McPlate(1280, 720):
                align (0.5, 0.5)
                at mc_fx_burst(enter_m_rgba(_mcc_glow), _mcc_burst_len)

            # The wordmark only exists for something worth naming. An R burst
            # is a pop of light and then the wall -- calling it out by name
            # would make the ladder meaningless.
            if _mcc_best != "r":
                vbox:
                    align (0.5, 0.82)
                    spacing 4
                    at mc_fx_banner_in

                    text (("SSR" if _mcc_best == "ssr" else "SR")):
                        style "mc_fx_banner"
                        color _mcc_glow
                        xalign 0.5
                    text _mcc_tier["full"]:
                        style "mc_fx_banner_sub"
                        color _mcc_col
                        xalign 0.5

    if not _mcc_bursting:
        text "CLICK TO SKIP":
            style "mc_fx_hint"
            xalign 0.5
            ypos 668


# =============================================================================
# STYLES
# =============================================================================

style mc_fx_banner is gui_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 76
    color "#ffe6a8"
    outlines [(4, "#0b0818", 0, 2)]
    kerning 6

style mc_fx_banner_sub is gui_text:
    font gui.interface_font
    size 19
    color "#ffb454"
    bold True
    kerning 7
    outlines [(2, "#0b0818", 0, 1)]

style mc_fx_hint is gui_text:
    font gui.interface_font
    size 13
    color "#7d7595"
    kerning 3
    outlines [(1, "#0b0818", 0, 1)]

# The speed control on the machine's header. `is button` inherits
# gui.button_properties("button"), which pins BOTH yminimum and ymaximum to
# gui.button_height -- so a pill that sets its own xysize has to clear the
# inherited maxima or config.enforce_window_max_size clamps it back.
style mc_fx_pill is button:
    background ArcadePanel(152, 30, top="#2b2250", bottom="#171130",
                        radius=15, border=1.0, border_color="#ffb45466")
    hover_background ArcadePanel(152, 30, top="#4a3a6e", bottom="#241a44",
                                radius=15, border=1.5, border_color="#ffe6a8")
    xmaximum None
    ymaximum None
    padding (0, 0)

style mc_fx_pill_text is gui_text:
    font gui.interface_font
    size 11
    color "#c8bce8"
    hover_color "#ffe6a8"
    bold True
    kerning 1
