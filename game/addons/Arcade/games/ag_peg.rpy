# =============================================================================
# ag_peg.rpy  --  OUTLIER   (Arcade Original #6)
# =============================================================================
# A peg shooter over a dataset that needs cleaning. The board is a scatter plot;
# twenty-two of its points are OUTLIERS, and the study only comes out
# significant once every one of them is gone. You have fifteen samples and a
# launcher. Matsuda calls this "data cleaning". Everybody else in the lab calls
# it what it is.
#
# WHAT IS KEPT, AND WHAT IS THIS CABINET'S OWN
#   The skeleton is the pachinko one, older than video games: aim, fire, and a
#   ball falls under gravity through a field of pins. Every peg it touches
#   LIGHTS, and lit pegs are removed once the ball has left the board. The
#   target pegs must all go before the samples run out, and a catcher on the
#   floor hands a sample back. That skeleton is kept exactly; what hangs on it
#   is Outlier's own:
#
#   THE PLOT        pegs are scatter-plot markers, and their SHAPE is their role:
#                   a data point is a hollow ring, an outlier a crimson disc
#                   crossed out, a grant a gold disc with a plus.
#   CORRELATIONS    up to three outliers per attempt are TETHERED to a data point
#                   elsewhere on the board. Light either end and both light. The
#                   easy end of a tether is often the best way to the hard one,
#                   so a board is read, not just aimed at.
#   CONFIDENCE      the multiplier is a confidence meter that climbs one step for
#                   every five outliers hit (x2 .. x5), a straight ramp.
#   THE TRAYS       two small trays slide along the floor as a mirrored pair,
#                   meeting in the middle and parting at the walls. A sample
#                   that lands in either comes back.
#   EXTRA BALLS     a ball also comes back for four outliers in one shot, and
#                   again at seven and ten: the reward is the goal itself.
#   STYLE           LONG RANGE (an outlier hit far from the previous hit), WALL
#                   BOUNCE (an outlier straight off a wall), the 20- and 40-PEG
#                   SHOT, and CLEAN CATCH (into a tray having lit nothing).
#   SIGNIFICANCE    the last outlier freezes the board for a beat, punches the
#                   camera in and stamps the result; the ball plays out; then
#                   every unused ball fires at once in the BONUS ROUND, a fan
#                   across the whole board. Saved balls are worth exactly what
#                   they hit. (The code calls it the robustness check.)
#   THE NOTES       a hit rings a marimba note chosen by the HEIGHT of the peg,
#                   so a falling shot plays its own path downward.
#
# THE FIVE POWERS (one per board; the code calls them grants)
#   FORECAST     (forecast)  the aim guide follows the next two shots through
#                            their bounces and rings every peg they will light.
#   SPLIT        (replicate) a second ball splits off the power peg.
#   SPILLOVER    (spill)     a contagion: pegs near the power peg light, then
#                            pegs near those, up to three rings out.
#   RE-FIRE      (resubmit)  once this shot's lit pegs have popped, the SAME
#                            shot is fired again, free, through the new board.
#   EXCLUSION    (phack)     the two remaining outliers farthest from the
#                            launcher are quietly dropped. They no longer need
#                            clearing -- but the confidence meter counts only
#                            outliers actually hit, so the board tops out lower.
#
# DETERMINISM IS LOAD-BEARING
#   FORECAST draws a shot before it is taken, which only works because
#   the board is a pure function of (peg state, world time): the trays and the
#   orbiting pegs are positioned from AGPWorld.t, nothing in flight is random,
#   and the anti-balance kick picks its side from state rather than random().
#   Keep it that way or the forecast starts lying.
#
# PHYSICS NOTES
#   * The ball moves in sub-steps of at most AGP_SUB px, so nothing tunnels.
#   * One contact is resolved per sub-step, the first one found.
#   * A CONTACT is not a HIT. A ball rolling along a brick is in contact every
#     sub-step; a hit is a contact with a different body, or with the same one
#     after a gap. Only hits light pegs, ring notes and count toward the
#     stuck-ball rule.
# =============================================================================

init python:
    import math
    import random

    # --- playfield -----------------------------------------------------------
    # Screen coordinates. The field sits between the sample tube on the left
    # rail and the confidence meter on the right, under the shared HUD header
    # and above the legend at 696.
    AGP_X0 = 262
    AGP_Y0 = 96
    AGP_FW = 756
    AGP_FH = 578
    AGP_X1 = AGP_X0 + AGP_FW
    AGP_Y1 = AGP_Y0 + AGP_FH

    AGP_PIVOT_X = 640.0
    AGP_PIVOT_Y = 108.0
    AGP_MUZZLE = 40.0
    AGP_AIM_MIN = math.radians(3.0)
    AGP_AIM_MAX = math.radians(177.0)

    AGP_ACCENT = "#46c7e8"
    AGP_SPR = "addons/Arcade/sprites/peg/"

    # Marker inks: data, outlier, grant -- plus the tether and meter colours.
    AGP_COL_INK = ("#c7d2ea", "#ff8a9e", "#ffd97a")
    AGP_OUT_FILL = "#f03e60"
    AGP_GRANT_INK = "#ffd97a"
    AGP_LINK_INK = "#5ee6ff"

    # --- bodies --------------------------------------------------------------
    AGP_BR = 8.0            # ball radius
    AGP_PR = 10.0           # peg radius
    AGP_KHL = 17.0          # brick: half-length of its core segment
    AGP_KR = 7.0            # brick: capsule radius around that segment

    # --- physics, per 1/60s tick ---------------------------------------------
    AGP_G = 0.15
    AGP_V0 = 10.0
    AGP_VMAX = 15.0
    AGP_E = 0.72            # restitution off pegs and bricks
    AGP_WALL_E = 0.82
    AGP_TANG = 0.985        # tangential speed kept through a bounce
    AGP_SUB = 4.0           # max travel per sub-step
    AGP_CELL = 40           # broad-phase grid

    # --- the trays -----------------------------------------------------------
    # Two catchers on one rail, mirrored about the centre line: they meet in the
    # middle and part at the walls. Both are positioned from world time alone.
    AGP_TRAY_Y = AGP_Y1 - 24.0
    AGP_TRAY_HW = 40.0          # centre to rim post (the sprite is built to it)
    AGP_TRAY_RIM = 6.0          # rim post radius
    AGP_TRAY_SPEED = 1.6
    AGP_TRAY_OUT = AGP_X0 + 56.0            # left tray's outermost centre
    AGP_TRAY_IN = AGP_PIVOT_X - 56.0        # left tray's innermost centre

    # --- rules ---------------------------------------------------------------
    AGP_BALLS = 15
    AGP_OUTLIERS = 22
    AGP_GRANT_PEGS = 2
    AGP_BASE = (10, 100, 50)            # data, outlier, grant
    # CONFIDENCE: (outliers hit, multiplier) for a board of AGP_OUTLIERS -- a
    # straight ramp, a step every five.
    AGP_MULT_STEPS = ((20, 5), (15, 4), (10, 3), (5, 2))
    AGP_FREE_OUTLIERS = (4, 7, 10)      # outliers in ONE shot that return a sample
    AGP_LINKS = 3                       # correlations dealt per attempt
    AGP_LINK_MIN_DIST = 170.0
    AGP_LINK_BONUS = 2500
    AGP_CLEAN_SWEEP = 50000
    AGP_FREEZE = 26                     # ticks the board holds on significance
    AGP_PUNCH = 1.28                    # the camera punch-in on that hit
    AGP_FAN_EDGE = 14.0                 # degrees clear of the rail, robustness fan

    # Style shots. Awarded flat, outside the multiplier.
    AGP_LONG_DIST = 380.0
    AGP_LONG_SHOT = 15000               # LONG RANGE
    AGP_WALL_SHOT = 4000                # WALL BOUNCE
    AGP_COMBO_SHOTS = ((40, 30000, "40-PEG SHOT"), (20, 8000, "20-PEG SHOT"))
    AGP_NULL_SHOT = 15000               # CLEAN CATCH

    # Stuck-ball rule: a lit body hit this many times is cleared early; a ball
    # crawling for AGP_STALL ticks clears what it last touched; a ball that
    # has not gained depth in AGP_NO_PROGRESS ticks clears every lit body near
    # it. AGP_SHOT_CAP is the backstop nothing should ever reach.
    AGP_STUCK_HITS = 7
    AGP_STALL_SPEED = 0.9
    AGP_STALL = 150
    AGP_NO_PROGRESS = 420
    AGP_SHOT_CAP = 3600

    # --- grants --------------------------------------------------------------
    # id -> (name, what it does, a plain-words tag for the rail).
    AGP_GRANTS = {
        "forecast": ("FORECAST",
                     "the aim guide follows the next two shots through their "
                     "bounces and rings every peg they will light",
                     "LONG AIM GUIDE"),
        "replicate": ("SPLIT",
                      "a second ball splits off the power peg", "SECOND BALL"),
        "spill": ("SPILLOVER",
                  "pegs near the power peg light, then pegs near those",
                  "CHAIN REACTION"),
        "resubmit": ("RE-FIRE",
                     "once its pegs have popped, the shot is fired again, free",
                     "SHOT REPEATS FREE"),
        "phack": ("EXCLUSION",
                  "the two outliers farthest from the launcher are dropped",
                  "DROPS 2 OUTLIERS"),
    }
    AGP_GUIDE_SHOTS = 2
    AGP_SPILL_R = 72.0
    AGP_SPILL_HOPS = 3
    AGP_SPILL_MAX = 16
    AGP_PHACK = 2

    # --- SFX -----------------------------------------------------------------
    # Registered into the shared cabinet table, so they play through ag_se and
    # its idle-channel pool like every other cue on the shelf. The hit notes
    # are a marimba on a minor pentatonic scale; a hit rings the note for the
    # HEIGHT of the peg it struck (AGPeg._note_for), not for how many pegs the
    # shot has lit.
    AGP_SFX_DIR = "assets/audio/sfx/peg/"
    AGP_NOTES = 18
    for _agp_i in range(AGP_NOTES):
        AG_SFX["peg_note_%02d" % _agp_i] = (
            AGP_SFX_DIR + "note_%02d.wav" % _agp_i, 0.5)
    AG_SFX.update({
        "peg_pop": (AGP_SFX_DIR + "pop.wav", 0.35),
        "peg_launch": (AGP_SFX_DIR + "launch.wav", 0.7),
        "peg_tray": (AGP_SFX_DIR + "tray.wav", 0.7),
        "peg_power": (AGP_SFX_DIR + "power.wav", 0.7),
        "peg_gong": (AGP_SFX_DIR + "gong.wav", 0.7),
        "peg_whoosh": (AGP_SFX_DIR + "whoosh.wav", 0.7),
        "peg_significant": (AGP_SFX_DIR + "significant.wav", 0.8),
    })

    # --- board building ------------------------------------------------------
    # Boards are authored in FIELD-LOCAL coordinates (0..756 x 0..578, launcher
    # at the top centre) as a list of bodies:
    #     ("p", x, y)                        a peg
    #     ("b", x, y, degrees)               a brick, rotated about its centre
    #     ("o", cx, cy, r, phase, omega)     a peg orbiting (cx, cy)
    # Keep the launcher's throat clear (nothing within ~70px of (378, 12)) and
    # keep bodies above ~530 so the trays have a lane.

    def _agp_arc(out, cx, cy, r, a0, a1, n, kind="p"):
        for i in range(n):
            a = math.radians(a0 + (a1 - a0) * (i / float(max(1, n - 1))))
            x = cx + r * math.cos(a)
            y = cy + r * math.sin(a)
            if kind == "p":
                out.append(("p", x, y))
            else:
                out.append(("b", x, y, math.degrees(a) + 90.0))

    def _agp_line(out, x0, y0, x1, y1, n, kind="p"):
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        for i in range(n):
            t = i / float(max(1, n - 1))
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t
            if kind == "p":
                out.append(("p", x, y))
            else:
                out.append(("b", x, y, ang))

    def _agp_mirror(out, items):
        """Append items, then their reflection across the centre line."""
        out.extend(items)
        for it in items:
            if it[0] == "p":
                out.append(("p", AGP_FW - it[1], it[2]))
            elif it[0] == "b":
                out.append(("b", AGP_FW - it[1], it[2], 180.0 - it[3]))

    def _agp_orbit(out, cx, cy, r, n, omega, phase=0.0):
        for i in range(n):
            out.append(("o", cx, cy, r, phase + i * 2.0 * math.pi / n, omega))

    def agp_board_pilot():
        e = []
        _agp_arc(e, 378, 60, 150, 20, 160, 11)
        _agp_arc(e, 378, 60, 235, 15, 165, 12, "b")
        _agp_arc(e, 378, 60, 320, 12, 168, 23)
        _agp_line(e, 76, 450, 680, 450, 16)
        _agp_line(e, 130, 512, 626, 512, 12)
        side = []
        _agp_line(side, 36, 180, 36, 380, 6)
        _agp_line(side, 60, 40, 120, 90, 3)
        _agp_mirror(e, side)
        return e

    def agp_board_quincunx():
        e = []
        for row in range(8):
            count = 6 + row
            y = 136 + row * 46
            x0 = 378 - (count - 1) * 28
            for k in range(count):
                e.append(("p", x0 + k * 56, y))
        top = []
        _agp_line(top, 50, 64, 190, 104, 3, "b")
        _agp_line(top, 40, 150, 40, 330, 4)
        _agp_mirror(e, top)
        # The bins of a Galton board, standing under the lattice.
        for k in range(7):
            e.append(("b", 42 + k * 112, 514, 90.0))
        return e

    def _agp_gauss_y(x, base=500.0, height=300.0, sd=115.0):
        z = (x - 378.0) / sd
        return base - height * math.exp(-0.5 * z * z)

    def agp_board_bell():
        e = []
        for i in range(25):
            x = 34 + i * (688 / 24.0)
            e.append(("p", x, _agp_gauss_y(x)))
        for i in range(9):
            x = 150 + i * (456 / 8.0)
            slope = (_agp_gauss_y(x + 1) - _agp_gauss_y(x - 1)) / 2.0
            e.append(("b", x, _agp_gauss_y(x) + 52,
                      math.degrees(math.atan(slope))))
        side = []
        # Error bars above the curve, histogram columns under it.
        for x in (138, 258):
            top = _agp_gauss_y(x) - 70
            for k in range(3):
                side.append(("p", x, top - k * 26))
        for x in (258, 318):
            y = _agp_gauss_y(x) + 110
            while y <= 510:
                side.append(("p", x, y))
                y += 32
        _agp_mirror(e, side)
        y = _agp_gauss_y(378) + 110
        while y <= 510:
            e.append(("p", 378, y))
            y += 32
        _agp_arc(e, 378, 560, 470, 228, 312, 15)
        for cx in (80, 676):
            for k in range(6):
                a = k * math.pi / 3.0
                e.append(("p", cx + 30 * math.cos(a), 330 + 30 * math.sin(a)))
        return e

    def agp_board_resubmit():
        e = []
        _agp_orbit(e, 210, 250, 78, 10, 0.011)
        _agp_orbit(e, 546, 250, 78, 10, -0.011)
        _agp_orbit(e, 210, 250, 36, 5, -0.02)
        _agp_orbit(e, 546, 250, 36, 5, 0.02)
        e.append(("p", 210, 250))
        e.append(("p", 546, 250))
        _agp_arc(e, 378, -160, 330, 55, 125, 11)
        for i in range(13):
            x = 40 + i * 56
            up = (i % 2 == 0)
            e.append(("b", x, 430 + (-14 if up else 14), -30.0 if up else 30.0))
        _agp_line(e, 100, 505, 656, 505, 10)
        _agp_line(e, 378, 200, 378, 350, 4)
        sides = []
        _agp_line(sides, 30, 120, 30, 330, 6)
        _agp_arc(sides, 210, 250, 124, 35, 145, 7)
        _agp_mirror(e, sides)
        return e

    def agp_board_forking():
        e = []
        _agp_arc(e, 378, 40, 115, 25, 155, 11)
        fork = []
        _agp_line(fork, 340, 200, 210, 270, 3, "b")
        _agp_line(fork, 300, 172, 170, 242, 4)
        _agp_line(fork, 352, 248, 270, 292, 3)
        _agp_line(fork, 180, 314, 132, 370, 2, "b")
        _agp_line(fork, 240, 314, 288, 370, 2, "b")
        for x in (110, 310):
            fork.append(("p", x - 22, 434))
            fork.append(("p", x + 22, 434))
            fork.append(("p", x, 464))
            fork.append(("p", x, 404))
        _agp_line(fork, 30, 180, 30, 400, 6)
        _agp_line(fork, 150, 96, 80, 150, 3)
        _agp_mirror(e, fork)
        for y in (262, 302, 342, 382):
            e.append(("p", 378, y))
        for y in (282, 322, 362):
            e.append(("p", 338, y))
            e.append(("p", 418, y))
        _agp_arc(e, 378, 760, 270, 240, 300, 8)
        return e

    # (id, name, grant, builder, variant note). The note is the variant card's
    # one line, so it stays inside ~62 characters.
    AGP_BOARDS = [
        ("b1", "PILOT STUDY", "forecast", agp_board_pilot,
            "gentle arcs // power: FORECAST (long aim guide)"),
        ("b2", "GALTON BOARD", "replicate", agp_board_quincunx,
            "a lattice of pins // power: SPLIT (second ball)"),
        ("b3", "BELL CURVE", "spill", agp_board_bell,
            "the normal curve // power: SPILLOVER (chain reaction)"),
        ("b4", "ORBITS", "resubmit", agp_board_resubmit,
            "moving rings // power: RE-FIRE (shot repeats free)"),
        ("b5", "FORKING PATHS", "phack", agp_board_forking,
            "branches // power: EXCLUSION (drops two outliers)"),
    ]

# =============================================================================
# THE WORLD
# Geometry and physics only. AGPWorld knows where every body is at world time
# t and how a ball moves through them; it keeps NO per-attempt state. Which
# bodies are alive, which are lit and how often each has been hit live in three
# plain lists passed into advance(), so the aim guide and the PREDICTIVE MODEL
# forecast can run the real physics on copies without the board ever noticing.
# =============================================================================
init python:

    AGP_EV_HIT = 0          # (kind, body, first, ball, dist_since_hit, wall)
    AGP_EV_UNSTICK = 1      # (kind, body, ball)
    AGP_EV_WALL = 2         # (kind, ball)
    AGP_EV_TRAY = 3         # (kind, ball)
    AGP_EV_EXIT = 5         # (kind, ball)
    AGP_EV_RIM = 6          # (kind, ball)

    class AGPBall(object):
        """One sample in flight. Plain attributes, so a predictor can clone
        it with a dict copy."""

        def __init__(self, x, y, vx, vy):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.alive = True
            self.last_i = -1        # body touched on the latest contact
            self.last_t = -99
            self.hx = x             # where the previous HIT happened
            self.hy = y
            self.has_hit = False
            self.wall = False       # side-wall bounce since the previous hit
            self.stall = 0
            self.prog = 0
            self.maxy = y
            self.hits = 0
            self.age = 0

        def clone(self):
            b = AGPBall(self.x, self.y, self.vx, self.vy)
            b.__dict__.update(self.__dict__)
            return b


    class AGPWorld(object):

        def __init__(self, items):
            self.n = 0
            self.kind = []          # 0 peg, 1 brick, 2 orbiting peg
            self.x = []
            self.y = []
            self.deg = []
            self.ax = []
            self.ay = []
            self.sx = []
            self.sy = []
            self.il2 = []
            self.orb = []
            self.movers = []
            self.grid = {}
            # The robustness check plays on a board with the trays taken away.
            self.finale = False
            for it in items:
                self._add(it)
            self._build_grid()

        # ---- construction ---------------------------------------------------

        def _add(self, it):
            i = self.n
            self.n += 1
            ax = ay = sx = sy = 0.0
            il2 = 0.0
            deg = 0.0
            orb = None
            if it[0] == "p":
                kind, x, y = 0, AGP_X0 + it[1], AGP_Y0 + it[2]
            elif it[0] == "b":
                kind, x, y = 1, AGP_X0 + it[1], AGP_Y0 + it[2]
                deg = it[3]
                a = math.radians(deg)
                ux = math.cos(a) * AGP_KHL
                uy = math.sin(a) * AGP_KHL
                ax, ay = x - ux, y - uy
                sx, sy = 2.0 * ux, 2.0 * uy
                il2 = 1.0 / max(1e-9, sx * sx + sy * sy)
            else:
                kind = 2
                orb = (AGP_X0 + it[1], AGP_Y0 + it[2], it[3], it[4], it[5])
                x = orb[0] + orb[2] * math.cos(orb[3])
                y = orb[1] + orb[2] * math.sin(orb[3])
                self.movers.append(i)
            self.kind.append(kind)
            self.x.append(x)
            self.y.append(y)
            self.deg.append(deg)
            self.ax.append(ax)
            self.ay.append(ay)
            self.sx.append(sx)
            self.sy.append(sy)
            self.il2.append(il2)
            self.orb.append(orb)

        @staticmethod
        def _key(cx, cy):
            return cx * 4096 + cy

        def _build_grid(self):
            """Static bodies only, each filed under every cell its REACH
            (own radius + ball radius) overlaps, so one lookup at the ball's
            centre finds everything it could be touching."""
            c = AGP_CELL
            for i in range(self.n):
                k = self.kind[i]
                if k == 2:
                    continue
                if k == 0:
                    reach = AGP_PR + AGP_BR
                    x0, x1 = self.x[i] - reach, self.x[i] + reach
                    y0, y1 = self.y[i] - reach, self.y[i] + reach
                else:
                    reach = AGP_KR + AGP_BR
                    ex = self.ax[i] + self.sx[i]
                    ey = self.ay[i] + self.sy[i]
                    x0 = min(self.ax[i], ex) - reach
                    x1 = max(self.ax[i], ex) + reach
                    y0 = min(self.ay[i], ey) - reach
                    y1 = max(self.ay[i], ey) + reach
                for cx in range(int(x0) // c, int(x1) // c + 1):
                    for cy in range(int(y0) // c, int(y1) // c + 1):
                        self.grid.setdefault(self._key(cx, cy), []).append(i)

        # ---- time-dependent positions ---------------------------------------

        def pos(self, i, t):
            o = self.orb[i]
            if o is None:
                return self.x[i], self.y[i]
            a = o[3] + o[4] * t
            return o[0] + o[2] * math.cos(a), o[1] + o[2] * math.sin(a)

        def tray_xs(self, t):
            """Centres of the two trays at world time t. The left one runs from
            the wall to the middle and back; the right one is its mirror about
            the centre line, so they meet and part together."""
            span = AGP_TRAY_IN - AGP_TRAY_OUT
            p = (t * AGP_TRAY_SPEED) % (2.0 * span)
            lx = AGP_TRAY_OUT + (p if p <= span else 2.0 * span - p)
            return lx, 2.0 * AGP_PIVOT_X - lx

        def tray_v(self, t):
            """The LEFT tray's velocity at world time t (the right one's is the
            negative of it)."""
            span = AGP_TRAY_IN - AGP_TRAY_OUT
            p = (t * AGP_TRAY_SPEED) % (2.0 * span)
            return AGP_TRAY_SPEED if p <= span else -AGP_TRAY_SPEED

        def advance(self, b, t, alive, lit, hits, ev):
            """Move ball `b` through one tick of world time `t`."""
            if not b.alive:
                return
            b.vy += AGP_G
            sp = math.hypot(b.vx, b.vy)
            if sp > AGP_VMAX:
                k = AGP_VMAX / sp
                b.vx *= k
                b.vy *= k
                sp = AGP_VMAX
            n = int(sp / AGP_SUB) + 1
            trays = None if self.finale else self.tray_xs(t)

            for _s in range(n):
                py = b.y
                b.x += b.vx / n
                b.y += b.vy / n
                if b.x < AGP_X0 + AGP_BR:
                    b.x = AGP_X0 + AGP_BR
                    b.vx = abs(b.vx) * AGP_WALL_E
                    b.wall = True
                    ev.append((AGP_EV_WALL, b))
                elif b.x > AGP_X1 - AGP_BR:
                    b.x = AGP_X1 - AGP_BR
                    b.vx = -abs(b.vx) * AGP_WALL_E
                    b.wall = True
                    ev.append((AGP_EV_WALL, b))
                if b.y < AGP_Y0 + AGP_BR:
                    b.y = AGP_Y0 + AGP_BR
                    b.vy = abs(b.vy) * AGP_WALL_E

                self._contact(b, t, alive, lit, hits, ev)

                if trays is not None and self._trays(b, t, trays, py, ev):
                    return

                if b.y - AGP_BR > AGP_Y1:
                    b.alive = False
                    ev.append((AGP_EV_EXIT, b))
                    return

            self._unstick(b, t, alive, lit, ev)

        def _contact(self, b, t, alive, lit, hits, ev):
            found = -1
            dx = dy = d2 = rr = 0.0
            pvx = pvy = 0.0
            cand = self.grid.get(self._key(int(b.x) // AGP_CELL,
                                           int(b.y) // AGP_CELL))
            if cand:
                kind = self.kind
                for i in cand:
                    if not alive[i]:
                        continue
                    if kind[i] == 0:
                        dx = b.x - self.x[i]
                        dy = b.y - self.y[i]
                        rr = AGP_PR + AGP_BR
                    else:
                        ax = self.ax[i]
                        ay = self.ay[i]
                        sx = self.sx[i]
                        sy = self.sy[i]
                        u = ((b.x - ax) * sx + (b.y - ay) * sy) * self.il2[i]
                        if u < 0.0:
                            u = 0.0
                        elif u > 1.0:
                            u = 1.0
                        dx = b.x - (ax + u * sx)
                        dy = b.y - (ay + u * sy)
                        rr = AGP_KR + AGP_BR
                    d2 = dx * dx + dy * dy
                    if d2 < rr * rr:
                        found = i
                        break

            if found < 0 and self.movers:
                rr = AGP_PR + AGP_BR
                for i in self.movers:
                    if not alive[i]:
                        continue
                    cx, cy, r, ph, om = self.orb[i]
                    a = ph + om * t
                    dx = b.x - (cx + r * math.cos(a))
                    dy = b.y - (cy + r * math.sin(a))
                    d2 = dx * dx + dy * dy
                    if d2 < rr * rr:
                        found = i
                        # The peg's own velocity goes into the bounce, so a
                        # ring sweeping into the ball bats it.
                        pvx = -r * om * math.sin(a)
                        pvy = r * om * math.cos(a)
                        break

            if found < 0:
                return
            i = found

            d = math.sqrt(d2)
            if d < 1e-6:
                nx, ny, d = 0.0, -1.0, 0.0
            else:
                nx = dx / d
                ny = dy / d
            push = rr - d
            b.x += nx * push
            b.y += ny * push

            rvx = b.vx - pvx
            rvy = b.vy - pvy
            vn = rvx * nx + rvy * ny
            if vn < 0.0:
                tx = rvx - vn * nx
                ty = rvy - vn * ny
                rvx = tx * AGP_TANG - AGP_E * vn * nx
                rvy = ty * AGP_TANG - AGP_E * vn * ny
                b.vx = rvx + pvx
                b.vy = rvy + pvy
                # A ball dropped dead-centre on a peg would balance on it.
                # Tip it -- and pick the side from STATE, never random(), or
                # the predictors would stop agreeing with the real shot.
                if ny < -0.94 and abs(b.vx) < 0.25:
                    b.vx += 0.3 if ((i + b.hits) & 1) else -0.3

            if b.last_i != i or t - b.last_t > 5:
                first = not lit[i]
                lit[i] = True
                hits[i] += 1
                b.hits += 1
                dist = math.hypot(b.x - b.hx, b.y - b.hy) if b.has_hit else 0.0
                ev.append((AGP_EV_HIT, i, first, b, dist, b.wall))
                b.hx = b.x
                b.hy = b.y
                b.has_hit = True
                b.wall = False
                if not first and hits[i] >= AGP_STUCK_HITS:
                    alive[i] = False
                    ev.append((AGP_EV_UNSTICK, i, b))
            b.last_i = i
            b.last_t = t

        def _trays(self, b, t, xs, py, ev):
            """Both trays: solid rim posts, a catch on the rim line, and a solid
            body underneath for anything that came in from the side."""
            if b.y < AGP_TRAY_Y - AGP_TRAY_RIM - AGP_BR:
                return False
            vl = self.tray_v(t)
            rr = AGP_TRAY_RIM + AGP_BR
            inner = AGP_TRAY_HW - AGP_TRAY_RIM
            for bx, vxb in ((xs[0], vl), (xs[1], -vl)):
                for side in (-AGP_TRAY_HW, AGP_TRAY_HW):
                    dx = b.x - (bx + side)
                    dy = b.y - AGP_TRAY_Y
                    d2 = dx * dx + dy * dy
                    if d2 < rr * rr:
                        d = math.sqrt(d2) or 1e-6
                        nx = dx / d
                        ny = dy / d
                        b.x += nx * (rr - d)
                        b.y += ny * (rr - d)
                        rvx = b.vx - vxb
                        vn = rvx * nx + b.vy * ny
                        if vn < 0.0:
                            rvx -= (1.0 + AGP_E) * vn * nx
                            b.vy -= (1.0 + AGP_E) * vn * ny
                            b.vx = rvx + vxb
                            ev.append((AGP_EV_RIM, b))

                # The catch is judged on the RIM LINE itself. It used to wait
                # until the ball was 4px below it -- and the solid-body shove
                # underneath fires the moment the centre passes the rim line,
                # so every ball dropping into the opening was thrown out
                # sideways before it could count. (The user's first playtest:
                # "the net repels the ball".)
                if (b.vy > 0.0 and py <= AGP_TRAY_Y < b.y
                        and abs(b.x - bx) < inner):
                    b.alive = False
                    ev.append((AGP_EV_TRAY, b))
                    return True

                # Below the rim a tray is a solid body: anything still in there
                # came in from the side, and is shoved back out of it.
                if b.y > AGP_TRAY_Y and abs(b.x - bx) < AGP_TRAY_HW + AGP_BR:
                    if b.x < bx:
                        b.x = bx - AGP_TRAY_HW - AGP_BR
                        b.vx = min(b.vx, vxb) - 0.5
                    else:
                        b.x = bx + AGP_TRAY_HW + AGP_BR
                        b.vx = max(b.vx, vxb) + 0.5
            return False

        def _unstick(self, b, t, alive, lit, ev):
            """The stuck-ball rule, once per tick."""
            b.age += 1
            if abs(b.vx) + abs(b.vy) < AGP_STALL_SPEED * 1.4:
                b.stall += 1
            else:
                b.stall = max(0, b.stall - 3)
            if b.stall > AGP_STALL:
                b.stall = 0
                i = b.last_i
                if i >= 0 and alive[i]:
                    alive[i] = False
                    ev.append((AGP_EV_UNSTICK, i, b))
            if b.y > b.maxy + 2.0:
                b.maxy = b.y
                b.prog = 0
            else:
                b.prog += 1
                if b.prog > AGP_NO_PROGRESS:
                    b.prog = 0
                    self.clear_near(b, t, alive, lit, ev, 72.0)

        def clear_near(self, b, t, alive, lit, ev, radius):
            r2 = radius * radius
            for i in range(self.n):
                if alive[i] and lit[i]:
                    x, y = self.pos(i, t)
                    if (x - b.x) ** 2 + (y - b.y) ** 2 < r2:
                        alive[i] = False
                        ev.append((AGP_EV_UNSTICK, i, b))

        # ---- prediction -----------------------------------------------------

        def touching(self, x, y, t, alive):
            cand = self.grid.get(self._key(int(x) // AGP_CELL,
                                           int(y) // AGP_CELL))
            if cand:
                for i in cand:
                    if not alive[i]:
                        continue
                    if self.kind[i] == 0:
                        dx = x - self.x[i]
                        dy = y - self.y[i]
                        rr = AGP_PR + AGP_BR
                    else:
                        u = (((x - self.ax[i]) * self.sx[i]
                              + (y - self.ay[i]) * self.sy[i]) * self.il2[i])
                        u = 0.0 if u < 0.0 else (1.0 if u > 1.0 else u)
                        dx = x - (self.ax[i] + u * self.sx[i])
                        dy = y - (self.ay[i] + u * self.sy[i])
                        rr = AGP_KR + AGP_BR
                    if dx * dx + dy * dy < rr * rr:
                        return True
            for i in self.movers:
                if alive[i]:
                    mx, my = self.pos(i, t)
                    if (x - mx) ** 2 + (y - my) ** 2 < (AGP_PR + AGP_BR) ** 2:
                        return True
            return False

        def guide_path(self, x, y, vx, vy, t, alive, ticks=80, every=3):
            """The ordinary aim guide: the arc up to the first thing the shot
            will touch, and no further."""
            pts = [(x, y)]
            for k in range(ticks):
                vy += AGP_G
                n = int(math.hypot(vx, vy) / AGP_SUB) + 1
                for _s in range(n):
                    x += vx / n
                    y += vy / n
                    if (x < AGP_X0 + AGP_BR or x > AGP_X1 - AGP_BR
                            or y > AGP_Y1 or self.touching(x, y, t + k, alive)):
                        pts.append((x, y))
                        return pts
                if k % every == every - 1:
                    pts.append((x, y))
            return pts

        def predict_path(self, ball, t, alive, lit, hits, ticks, every=3):
            """The PREDICTIVE MODEL forecast: the real physics, run on copies.
            Returns the path, and every body the shot would newly light, in
            the order it would light them."""
            b = ball.clone()
            al = list(alive)
            li = list(lit)
            hi = list(hits)
            ev = []
            pts = [(b.x, b.y)]
            marks = []
            for k in range(ticks):
                self.advance(b, t + k, al, li, hi, ev)
                for e in ev:
                    if e[0] == AGP_EV_HIT and e[2]:
                        marks.append(e[1])
                del ev[:]
                if k % every == every - 1 or not b.alive:
                    pts.append((b.x, b.y))
                if not b.alive:
                    break
            return pts, marks

# =============================================================================
# THE VIEW
# Everything OUTLIER draws, as a mixin AGPeg inherits. It reads game state and
# writes none, apart from the frame counter.
#
# THE ZOOM
#   The significance punch is done with Render.zoom, which zooms only a render's
#   CHILDREN and never its own size or blit coordinates. So the board is drawn
#   into a full-screen layer, that layer is blitted at (0, 0) into a zoomed
#   wrapper (everything inside scales about the origin), and the wrapper is
#   blitted into a field-sized render with the clipping FLAGS set -- flags, not
#   subsurface, for the reason kototouhou.rpy's render() documents. The offset
#   keeps the focus point where it already was on screen.
# =============================================================================
init python:

    AGP_CAN_ZOOM = hasattr(renpy.Render, "zoom")

    def _agp_hex_alpha(color, a):
        """#rrggbb + a quantised alpha, so fades cost a handful of cached
        Solids rather than one per frame."""
        q = int(ag_clamp(a, 0.0, 1.0) * 8.0 + 0.5) * 31
        return "%s%02x" % (color, min(255, q))

    class AGPegView(object):

        def draw(self, c):
            self.frame += 1
            c.panel(AGP_X0 - 10, AGP_Y0 - 10, AGP_FW + 20, AGP_FH + 20,
                    top="#0f1a34f0", bottom="#08101ef4", radius=16,
                    border=1.5, bcolor=(AGP_ACCENT + "55"))
            if self.zoom > 1.001 and AGP_CAN_ZOOM:
                self._draw_zoomed(c)
            else:
                self._draw_board(c)
            self._draw_left_rail(c)
            self._draw_right_rail(c)
            self._draw_hud(c)
            self._draw_callouts(c)
            if self.phase == "card":
                self._draw_card(c)
            if self.banner is not None:
                self._draw_banner(c)

        def _draw_zoomed(self, c):
            layer = renpy.Render(AG_W, AG_H)
            bc = AGCanvas(layer, c.st, c.at)
            bc.memo = c.memo
            self._draw_board(bc)
            z = self.zoom
            wrap = renpy.Render(AG_W, AG_H)
            wrap.zoom(z, z)
            wrap.blit(layer, (0, 0))
            clip = renpy.Render(AGP_FW, AGP_FH)
            clip.xclipping = True
            clip.yclipping = True
            ox = self.zoom_fx - self.zoom_fx * z
            oy = self.zoom_fy - self.zoom_fy * z
            clip.subpixel_blit(wrap, (ox - AGP_X0, oy - AGP_Y0))
            c.rv.blit(clip, (AGP_X0, AGP_Y0))

        # ---- the board ------------------------------------------------------

        def _draw_board(self, c):
            c.disp(("agp_img", "field"), lambda: Image(AGP_SPR + "field.png"),
                   AGP_X0, AGP_Y0, w=AGP_FW, h=AGP_FH)
            self._draw_links(c)
            self._draw_bodies(c)
            if self.phase == "aim":
                self._draw_guide(c)
            if not self.world.finale:
                for tx in self.world.tray_xs(self.t):
                    c.disp(("agp_img", "tray"),
                           lambda: Image(AGP_SPR + "tray.png"),
                           tx, AGP_TRAY_Y - AGP_TRAY_RIM, w=96, h=30,
                           anchor=(0.5, 0.0), sub=True)
            self._draw_launcher(c)
            for b in self.balls:
                self._draw_ball(c, b.x, b.y)
            self._draw_fx(c)
            self._draw_floats(c)

        def _draw_links(self, c):
            """CORRELATIONS: a dotted tether between each linked pair, faint
            while both ends wait and bright once either has lit."""
            w = self.world
            for o, d in self.links:
                if not (self.alive[o] and self.alive[d]):
                    continue
                ox, oy = w.pos(o, self.t)
                dx, dy = w.pos(d, self.t)
                col = AGP_LINK_INK + ("dd" if (self.lit[o] or self.lit[d]) else "58")
                n = max(2, int(math.hypot(dx - ox, dy - oy) // 13))
                for k in range(1, n):
                    t = k / float(n)
                    c.rect(col, ox + (dx - ox) * t - 1.5,
                           oy + (dy - oy) * t - 1.5, 3, 3, sub=True)

        def _draw_bodies(self, c):
            w = self.world
            t = self.t
            last = self.last_outlier if self.outliers_left() == 1 else -1
            for i in range(w.n):
                if not self.alive[i]:
                    continue
                lit = self.lit[i]
                name = AGP_COL_NAMES[self.color[i]]
                suffix = "_lit" if lit else ""
                kind = w.kind[i]
                x, y = w.pos(i, t)
                if i == last:
                    pulse = 0.5 + 0.5 * math.sin(self.tick * 0.18)
                    q = int(pulse * 3.0 + 0.5) / 3.0
                    big = (kind == 1)
                    c.disp(("agp_last", q, big),
                           lambda q=q, big=big: Transform(
                               AGP_SPR + "peg_outlier_lit.png",
                               zoom=(2.8 if big else 1.9),
                               alpha=0.25 + 0.55 * q),
                           x, y, w=128, h=128, anchor=(0.5, 0.5),
                           sub=(kind == 2))
                if kind == 1:
                    deg = int(round(w.deg[i])) % 360
                    c.disp(("agp_brick", name, lit, deg),
                           lambda f=("brick_%s%s.png" % (name, suffix)), d=deg:
                               Transform(AGP_SPR + f, rotate=d),
                           x, y, w=96, h=96, anchor=(0.5, 0.5))
                else:
                    c.disp(("agp_peg", name, lit),
                           lambda f=("peg_%s%s.png" % (name, suffix)):
                               Image(AGP_SPR + f),
                           x, y, w=64, h=64, anchor=(0.5, 0.5),
                           sub=(kind == 2))
                if i in self.excluded:
                    # A recoded outlier keeps a crimson strike, so the p-hack
                    # stays on the record.
                    c.rect(AGP_COL_INK[1] + "dd", x - 10, y - 1.5, 20, 3,
                           sub=True)

        def _draw_guide(self, c):
            pts = self.guide
            if len(pts) >= 2:
                smart = self.guide_shots > 0
                col = AGP_LINK_INK if smart else "#ffffff"
                n = float(len(pts))
                for k in range(1, len(pts)):
                    x, y = pts[k]
                    fade = 1.0 - (k / n) * (0.75 if smart else 0.35)
                    c.rect(_agp_hex_alpha(col, 0.9 * fade), x - 2, y - 2, 4, 4,
                           sub=True)
            # The forecast also rings every peg the shot is going to light.
            for i in self.guide_marks:
                if self.alive[i]:
                    x, y = self.world.pos(i, self.t)
                    c.frame(AGP_LINK_INK + "aa", x - 13, y - 13, 26, 26, 2)

        def _draw_launcher(self, c):
            c.disp(("agp_img", "base"), lambda: Image(AGP_SPR + "base.png"),
                   AGP_PIVOT_X, AGP_PIVOT_Y, w=120, h=80, anchor=(0.5, 0.125))
            deg = int(round(math.degrees(self.aim) - 90.0))
            c.disp(("agp_barrel", deg),
                   lambda d=deg: Transform(AGP_SPR + "barrel.png", rotate=d),
                   AGP_PIVOT_X, AGP_PIVOT_Y, w=128, h=128, anchor=(0.5, 0.5))
            if self.phase == "aim" and self.balls_left > 0:
                self._draw_ball(c, AGP_PIVOT_X + math.cos(self.aim) * AGP_MUZZLE,
                                AGP_PIVOT_Y + math.sin(self.aim) * AGP_MUZZLE)

        def _draw_ball(self, c, x, y):
            c.disp(("agp_img", "ball"), lambda: Image(AGP_SPR + "ball.png"),
                   x, y, w=40, h=40, anchor=(0.5, 0.5), sub=True)

        def _draw_fx(self, c):
            for p in self.fx:
                t = p[4] / float(p[5])
                size = 2 + int(3 * (1.0 - t))
                c.rect(_agp_hex_alpha(p[6], 1.0 - t), p[0] - size / 2.0,
                       p[1] - size / 2.0, size, size, sub=True)

        def _draw_floats(self, c):
            for text, x, y, color, size, life, ttl in self.floats:
                a = 1.0 if life < ttl * 0.6 else 1.0 - (life - ttl * 0.6) / (ttl * 0.4)
                c.text(text, x, y, size=size, color=color, bold=True,
                       anchor=(0.5, 0.5), alpha=int(a * 4 + 0.5) / 4.0)

        # ---- rails ----------------------------------------------------------

        def _draw_left_rail(self, c):
            c.readout("BALLS", str(self.balls_left), 60, 104, size=34)

            # The tube.
            tx, ty, tw, th = 196, 150, 36, 524
            c.panel(tx, ty, tw, th, top="#0e1a2af0", bottom="#08101cf4",
                    radius=14, border=1.2, bcolor=(AGP_ACCENT + "55"))
            loaded = 1 if (self.phase == "aim" and self.balls_left) else 0
            shown = min(20, max(0, self.balls_left - loaded))
            for k in range(shown):
                self._draw_ball(c, tx + tw / 2.0, ty + th - 16 - k * 24)

            # The grant.
            name, what, tag = AGP_GRANTS[self.grant]
            y = 190
            c.text("POWER", 60, y, size=12, color=AG_FAINT, bold=True,
                   kerning=2.0)
            c.text(name.replace(" ", "\n"), 60, y + 18, size=15,
                   color=AGP_GRANT_INK, bold=True)
            lines = 2 if " " in name else 1
            c.text(tag, 60, y + 22 + lines * 19, size=11, color=AG_DIM,
                   kerning=1.0)
            status = None
            if self.grant == "forecast" and self.guide_shots:
                status = "%d SHOT%s LEFT" % (self.guide_shots,
                                             "" if self.guide_shots == 1 else "S")
            elif self.grant == "resubmit" and self.resubmits:
                status = "RE-FIRE ARMED"
            elif self.grant == "phack" and self.excluded:
                status = "%d DROPPED" % len(self.excluded)
            if status:
                c.text(status, 60, y + 40 + lines * 19, size=12,
                       color="#ffe7a8", bold=True, kerning=1.5)

            # What the markers mean.
            y = 470
            for sprite, label, ink in (
                    ("peg_outlier.png", "OUTLIER", AGP_COL_INK[1]),
                    ("peg_data.png", "DATA", AGP_COL_INK[0]),
                    ("peg_grant.png", "POWER", AGP_COL_INK[2])):
                c.disp(("agp_key", sprite),
                       lambda s=sprite: Transform(AGP_SPR + s, zoom=0.75),
                       72, y, w=48, h=48, anchor=(0.5, 0.5))
                c.text(label, 90, y, size=12, color=ink, bold=True,
                       kerning=1.5, anchor=(0.0, 0.5))
                y += 28
            for k in range(4):
                c.rect(AGP_LINK_INK + "cc", 61 + k * 6, y - 1, 3, 3)
            c.text("LINKED", 90, y, size=12, color=AGP_LINK_INK, bold=True,
                   kerning=1.5, anchor=(0.0, 0.5))

        def _draw_right_rail(self, c):
            m = self.mult()
            c.readout("CONFIDENCE", "X%d" % m, 1046, 104, size=34,
                      color=(AGP_LINK_INK if m > 1 else AG_INK))

            mx, my, mw, mh = 1046, 190, 22, 450
            seg = mh / float(self.outlier_total)
            c.panel(mx - 5, my - 5, mw + 10, mh + 10, top="#0e1a2af0",
                    bottom="#08101cf4", radius=8, border=1.0,
                    bcolor="#ffffff22")
            cut = self.outlier_total - len(self.excluded)
            for k in range(self.outlier_total):
                y = my + mh - (k + 1) * seg
                if k < self.outlier_hit:
                    col = AGP_OUT_FILL
                elif k >= cut:
                    col = AGP_COL_INK[1] + "30"
                else:
                    col = "#ffffff10"
                c.rect(col, mx, y + 1, mw, max(1, seg - 2))
            scale = self.outlier_total / float(AGP_OUTLIERS)
            for need, mul in AGP_MULT_STEPS:
                k = int(math.ceil(need * scale))
                y = my + mh - k * seg
                hit = self.outlier_hit >= k
                c.rect(AGP_LINK_INK if hit else "#ffffff44", mx - 6, y, mw + 12, 1)
                c.text("X%d" % mul, mx + mw + 12, y, size=12,
                       color=(AGP_LINK_INK if hit else AG_FAINT), bold=True,
                       anchor=(0.0, 0.5))

            c.readout("OUTLIERS", str(self.outliers_left()), 1120, 480,
                      size=28, color=AGP_COL_INK[1])
            c.readout("THIS SHOT", ag_num(self.shot_score), 1120, 560,
                      size=20)
            nxt = None
            for need in AGP_FREE_OUTLIERS:
                if self.shot_outliers < need:
                    nxt = need
                    break
            if nxt is not None and not self.significant:
                c.text("+1 BALL AT %d OUTLIERS" % nxt, 1120, 606, size=11,
                       color=AG_FAINT, kerning=1.0)
                c.bar(1120, 624, 100, 4, self.shot_outliers / float(nxt),
                      AGP_LINK_INK)

        def _draw_hud(self, c):
            c.header("OUTLIER", "%s  //  %s" % (self.where(), self.board_name),
                     AGP_ACCENT)
            if self.full:
                best = max(self.total, ag_best("peg_score"))
            else:
                best = max(self.board_score, ag_best("peg_" + self.board_id))
            c.stat_row([
                ("BEST", ag_num(best), AG_DIM),
                ("SCORE", ag_num(self.total), AG_INK),
            ])
            c.legend("MOUSE AIM   //   CLICK OR Z FIRE   //   "
                     "ARROWS OR WHEEL FINE AIM   //   ESC PAUSE")

        def _draw_callouts(self, c):
            y = AGP_Y0 + 250
            for text, sub, color, life, ttl in self.callouts:
                fade_in = ag_clamp(life / 8.0, 0.0, 1.0)
                fade_out = ag_clamp((ttl - life) / 20.0, 0.0, 1.0)
                a = int(min(fade_in, fade_out) * 4 + 0.5) / 4.0
                if a <= 0.0:
                    continue
                c.text(text, AGP_PIVOT_X, y, size=28, color=color,
                       font=AG_FONT, bold=True, anchor=(0.5, 0.5), alpha=a)
                if sub:
                    c.text(sub, AGP_PIVOT_X, y + 26, size=13, color=AG_INK,
                           bold=True, kerning=2.0, anchor=(0.5, 0.5), alpha=a)
                y += 62

        def _draw_banner(self, c):
            text, color, life, ttl = self.banner[:4]
            sub = self.banner[4] if len(self.banner) > 4 else None
            a = min(ag_clamp(life / 14.0, 0.0, 1.0),
                    ag_clamp((ttl - life) / 30.0, 0.0, 1.0))
            qa = int(a * 4 + 0.5) / 4.0
            c.rect(_agp_hex_alpha("#0a0713", 0.62 * a), 0, AG_H / 2 - 60,
                   AG_W, 120)
            c.text(text, AG_W / 2, AG_H / 2 - (10 if sub else 0), size=52,
                   color=color, font=AG_FONT, bold=True, anchor=(0.5, 0.5),
                   alpha=qa)
            if sub:
                c.text(sub, AG_W / 2, AG_H / 2 + 34, size=15, color=AG_INK,
                       bold=True, kerning=2.5, anchor=(0.5, 0.5), alpha=qa)

        def _draw_card(self, c):
            rows = self.card_rows
            w = 540
            h = 190 + 32 * len(rows)
            x = AG_W / 2 - w / 2
            y = AG_H / 2 - h / 2
            c.rect("#0a0713aa", 0, 0, AG_W, AG_H)
            c.panel(x, y, w, h, top="#241b46f4", bottom="#120c24f8",
                    radius=20, border=1.5, bcolor="#4fbf7a88")
            c.text("BOARD CLEAR", AG_W / 2, y + 42, size=34,
                   color="#4fbf7a", font=AG_FONT, bold=True, anchor=(0.5, 0.5))
            c.text(self.board_name, AG_W / 2, y + 74, size=13,
                   color=AGP_ACCENT, bold=True, kerning=3.0, anchor=(0.5, 0.5))
            ry = y + 104
            for label, value in rows:
                c.text(label, x + 48, ry, size=15, color=AG_DIM)
                c.text(value, x + w - 48, ry, size=15, color=AG_INK, bold=True,
                       anchor=(1.0, 0.0))
                ry += 32
            c.rect("#ffffff22", x + 40, ry + 4, w - 80, 1)
            c.text("BOARD SCORE", x + 48, ry + 16, size=15, color="#ffcf6a",
                   bold=True)
            c.text(ag_num(self.board_score), x + w - 48, ry + 12, size=24,
                   color="#ffcf6a", bold=True, anchor=(1.0, 0.0))
            if self.board_record:
                c.text("NEW BOARD RECORD", AG_W / 2, y + h - 22, size=12,
                       color=AGP_LINK_INK, bold=True, kerning=2.0,
                       anchor=(0.5, 0.5))
            elif self.phase_t > 50:
                c.text("CLICK TO CONTINUE", AG_W / 2, y + h - 22, size=12,
                       color=AG_FAINT, bold=True, kerning=2.0,
                       anchor=(0.5, 0.5))


# =============================================================================
# THE GAME
# Rules, flow and scoring. A board is played in phases:
#   aim    the launcher follows the mouse; the world clock runs (trays, rings)
#   fly    balls in flight, including the ROBUSTNESS CHECK fan; the
#          significance freeze holds this phase still for a beat
#   pop    lit pegs leave, in the order they were hit
#   tally  the clean-dataset check
#   card   the board's results, then the next board or the end of the run
#   fail   out of samples with outliers still standing
# =============================================================================
init python:

    try:
        import pygame_sdl2 as _agp_pg
        AGP_K_LEFT1, AGP_K_LEFT2 = _agp_pg.K_LEFT, _agp_pg.K_a
        AGP_K_RIGHT1, AGP_K_RIGHT2 = _agp_pg.K_RIGHT, _agp_pg.K_d
        AGP_K_FIRE1, AGP_K_FIRE2, AGP_K_FIRE3 = (
            _agp_pg.K_z, _agp_pg.K_SPACE, _agp_pg.K_RETURN)
        AGP_K_SHIFT1, AGP_K_SHIFT2 = _agp_pg.K_LSHIFT, _agp_pg.K_RSHIFT
    except Exception:
        AGP_K_LEFT1 = AGP_K_LEFT2 = AGP_K_RIGHT1 = AGP_K_RIGHT2 = -1
        AGP_K_FIRE1 = AGP_K_FIRE2 = AGP_K_FIRE3 = -1
        AGP_K_SHIFT1 = AGP_K_SHIFT2 = -1

    AGP_COL_NAMES = ("data", "outlier", "grant")

    # Music around significance: the board track fades OUT on the last outlier
    # (user request, Sep 11 2026: it should stop gracefully there), stays silent
    # through the robustness check and the card, and fades back IN when the next
    # board of a full study begins.
    AGP_FINALE_MUSIC_FADE = 1.0
    AGP_MUSIC_FADEIN = 1.5


    class AGPeg(AGPegView, AGGame):
        """OUTLIER: a peg shooter over a dataset that needs cleaning."""

        KIND = "peg"
        TITLE = "OUTLIER"
        ACCENT = AGP_ACCENT
        # Left click fires and nothing else is taken, so right-click stays
        # bound to pause like the keyboard cabinets.
        MOUSE = False
        CONTROLS = [
            ("MOUSE", "aim the launcher"),
            ("LEFT CLICK  or  Z / SPACE", "fire"),
            ("LEFT / RIGHT  or  WHEEL", "fine aim  (SHIFT: finer)"),
            ("ESC  or  RIGHT CLICK", "pause"),
            ("Q  (while paused)", "give up"),
        ]

        def __init__(self, variant=None):
            super(AGPeg, self).__init__(variant)
            ids = [b[0] for b in AGP_BOARDS]
            if variant in ids:
                self.order = [ids.index(variant)]
                self.full = False
            else:
                self.order = list(range(len(AGP_BOARDS)))
                self.full = True
            self.stage = 0

            self.total = 0
            self.boards_cleared = 0
            self.outliers = 0
            self.style_count = 0
            self.free_balls = 0
            self.links_hit = 0
            self.cleared = False
            self.board_record = False

            self.aim = math.radians(90.0)
            self.want_fire = False
            # A fire key still held from the controls card must be released
            # before it counts: tapped() only sees rising edges.
            self._edges["fire"] = True
            self.frame = 0
            self._ev = []

            self.fx = []
            self.floats = []
            self.callouts = []
            self.banner = None
            self._last_wall_se = -99
            self._last_tock_se = -99
            self._load_board()

        # ---- setup ----------------------------------------------------------

        def _load_board(self):
            bid, name, grant, builder, _note = AGP_BOARDS[self.order[self.stage]]
            self.board_id = bid
            self.board_name = name
            self.grant = grant
            self.world = AGPWorld(builder())
            n = self.world.n
            self.alive = [True] * n
            self.lit = [False] * n
            self.hits = [0] * n

            # Roles are dealt fresh on every attempt, so a board is a shape
            # rather than a solution.
            deal = list(range(n))
            random.shuffle(deal)
            self.color = [0] * n
            self.outlier_total = min(AGP_OUTLIERS, n)
            for i in deal[:self.outlier_total]:
                self.color[i] = 1
            for i in deal[self.outlier_total:self.outlier_total + AGP_GRANT_PEGS]:
                self.color[i] = 2
            self.outlier_hit = 0
            self.last_outlier = -1
            self.excluded = set()
            self._deal_links()

            self.t = 0
            self.balls_left = AGP_BALLS
            self.board_score = 0
            self.balls = []
            self.hit_order = []
            self.pop_queue = []
            self.phase = "aim"
            self.phase_t = 0
            self.fire_lock = 24
            self.last_aim = self.aim

            self.guide = []
            self.guide_marks = []
            self.guide_shots = 0
            self.resubmits = 0

            self.significant = False
            self.robust_done = False
            self.robust_fired = 0
            self.freeze = 0
            self.zoom = 1.0
            self.zoom_fx = AGP_PIVOT_X
            self.zoom_fy = AGP_Y0 + AGP_FH / 2.0

            self.shot_score = 0
            self.shot_new = 0
            self.shot_outliers = 0
            self.shot_ticks = 0
            self.board_style = 0
            self.board_free = 0
            self.board_links = 0
            self.clean_paid = 0
            self.card_rows = []
            self.banner = None
            self._update_guide()
            self._say(name, "%s  //  POWER: %s" % (
                self.where(), AGP_GRANTS[grant][0]), AGP_ACCENT, 170)

        def where(self):
            """BOARD 2 / 5 in a full run; a lone board keeps its own number."""
            if self.full:
                return "BOARD %d / %d" % (self.stage + 1, len(self.order))
            return "BOARD %d" % (self.order[0] + 1)

        def _deal_links(self):
            """CORRELATIONS: tether up to AGP_LINKS outliers to data points at
            least AGP_LINK_MIN_DIST away. Distance is judged at world time zero;
            on the orbiting board a tether keeps moving with its pegs."""
            w = self.world
            outs = [i for i in range(w.n) if self.color[i] == 1]
            data = [i for i in range(w.n) if self.color[i] == 0]
            random.shuffle(outs)
            used = set()
            self.links = []
            for o in outs:
                if len(self.links) >= AGP_LINKS:
                    break
                ox, oy = w.pos(o, 0)
                far = [d for d in data if d not in used
                       and math.hypot(w.pos(d, 0)[0] - ox,
                                      w.pos(d, 0)[1] - oy) >= AGP_LINK_MIN_DIST]
                if far:
                    d = random.choice(far)
                    used.add(d)
                    self.links.append((o, d))
            self.link_of = {}
            for o, d in self.links:
                self.link_of[o] = d
                self.link_of[d] = o

        # ---- rules helpers --------------------------------------------------

        def _mult_for(self, hit):
            scale = self.outlier_total / float(AGP_OUTLIERS)
            for need, m in AGP_MULT_STEPS:
                if hit >= int(math.ceil(need * scale)):
                    return m
            return 1

        def mult(self):
            return self._mult_for(self.outlier_hit)

        def value(self, i):
            return AGP_BASE[self.color[i]]

        def outliers_left(self):
            return self.outlier_total - self.outlier_hit - len(self.excluded)

        def _launch_vector(self, a):
            ca = math.cos(a)
            sa = math.sin(a)
            return (AGP_PIVOT_X + ca * AGP_MUZZLE, AGP_PIVOT_Y + sa * AGP_MUZZLE,
                    ca * AGP_V0, sa * AGP_V0)

        def _make_ball(self, a):
            x, y, vx, vy = self._launch_vector(a)
            return AGPBall(x, y, vx, vy)

        def _note_for(self, y):
            """A hit rings the note for the peg's HEIGHT: the top of the board is
            the top of the scale, so a falling shot plays its own descent."""
            k = int((AGP_Y1 - y) / float(AGP_FH) * AGP_NOTES)
            return 0 if k < 0 else (AGP_NOTES - 1 if k >= AGP_NOTES else k)

        # ---- input ----------------------------------------------------------

        def _set_aim(self, a):
            self.aim = ag_clamp(a, AGP_AIM_MIN, AGP_AIM_MAX)

        def _aim_at(self, x, y):
            a = math.atan2(y - AGP_PIVOT_Y, x - AGP_PIVOT_X)
            if a < 0.0:
                a = AGP_AIM_MIN if x >= AGP_PIVOT_X else AGP_AIM_MAX
            self._set_aim(a)

        def on_event(self, ev, x, y):
            try:
                import pygame_sdl2 as pg
            except Exception:
                return
            if ev.type == pg.MOUSEMOTION:
                if self.phase == "aim":
                    self._aim_at(x, y)
            elif ev.type == pg.MOUSEBUTTONDOWN:
                button = getattr(ev, "button", 1)
                if button == 1:
                    if self.phase == "aim":
                        self._aim_at(x, y)
                    self.want_fire = True
                elif button == 4:
                    self._set_aim(self.aim + math.radians(0.25))
                elif button == 5:
                    self._set_aim(self.aim - math.radians(0.25))
            elif ev.type == getattr(pg, "MOUSEWHEEL", -12345):
                dy = getattr(ev, "y", 0)
                if dy:
                    self._set_aim(self.aim + math.radians(0.25) * dy)

        def _input(self, keys):
            if self.tapped(keys, "fire", AGP_K_FIRE1, AGP_K_FIRE2, AGP_K_FIRE3):
                self.want_fire = True
            if self.phase != "aim":
                return
            fine = self.held(keys, AGP_K_SHIFT1, AGP_K_SHIFT2)
            rate = math.radians(0.08 if fine else 0.45)
            if self.held(keys, AGP_K_LEFT1, AGP_K_LEFT2):
                self._set_aim(self.aim + rate)
            if self.held(keys, AGP_K_RIGHT1, AGP_K_RIGHT2):
                self._set_aim(self.aim - rate)

        # ---- the tick -------------------------------------------------------

        def step(self):
            if self.result is not None:
                return
            keys = self.poll()
            self._input(keys)
            if self.fire_lock > 0:
                self.fire_lock -= 1

            phase = self.phase
            if phase == "aim":
                self._step_aim()
            elif phase == "fly":
                self._step_fly()
            elif phase == "pop":
                self._step_pop()
            elif phase == "tally":
                self._step_tally()
            elif phase == "card":
                self._step_card()
            elif phase == "fail":
                self._step_fail()

            # A click only means "fire" on the tick it lands in a phase that
            # can use it; it is never banked for later.
            self.want_fire = False
            self.phase_t += 1
            self._step_camera()
            self._step_fx()

        def _set_phase(self, phase):
            self.phase = phase
            self.phase_t = 0

        def _step_aim(self):
            if self.want_fire and self.fire_lock <= 0:
                self._fire()
                return
            # Clock first, guide second: the guide on screen is then computed
            # for exactly the world time a shot fired next tick will start at.
            self.t += 1
            self._update_guide()

        def _update_guide(self):
            x, y, vx, vy = self._launch_vector(self.aim)
            if self.guide_shots > 0:
                self.guide, self.guide_marks = self.world.predict_path(
                    AGPBall(x, y, vx, vy), self.t, self.alive, self.lit,
                    self.hits, 150)
            else:
                self.guide = self.world.guide_path(x, y, vx, vy, self.t,
                                                   self.alive)
                self.guide_marks = []

        def _fire(self):
            self.balls_left -= 1
            if self.guide_shots > 0:
                self.guide_shots -= 1
            self.last_aim = self.aim
            self._launch(self.aim)

        def _launch(self, a):
            self.shot_score = 0
            self.shot_new = 0
            self.shot_outliers = 0
            self.shot_ticks = 0
            self.hit_order = []
            self.balls = [self._make_ball(a)]
            self._set_phase("fly")
            ag_se("peg_launch")
            x, y, _vx, _vy = self._launch_vector(a)
            self._spark(x, y, "#bfefff", 8, 1.6)

        # ---- flight ---------------------------------------------------------

        def _step_fly(self):
            self.shot_ticks += 1
            if self.freeze > 0:
                # SIGNIFICANCE: the board holds still for a beat.
                self.freeze -= 1
                return

            ev = self._ev
            for b in list(self.balls):
                self.world.advance(b, self.t, self.alive, self.lit, self.hits, ev)
            self.t += 1
            if ev:
                self._handle(ev)
                del ev[:]
            self.balls = [b for b in self.balls if b.alive]

            if self.shot_ticks > AGP_SHOT_CAP:
                for b in self.balls:
                    b.alive = False
                self.balls = []
            if not self.balls:
                self._end_flight()

        def _handle(self, events):
            for e in events:
                kind = e[0]
                if kind == AGP_EV_HIT:
                    if e[2]:
                        self._light(e[1], e[3], e[4], e[5])
                    elif self.tick - self._last_tock_se > 3:
                        self._last_tock_se = self.tick
                        ag_se("bounce", 0.35)
                elif kind == AGP_EV_UNSTICK:
                    self._pop(e[1], quiet=True)
                elif kind == AGP_EV_WALL:
                    if self.tick - self._last_wall_se > 6:
                        self._last_wall_se = self.tick
                        ag_se("bounce", 0.3)
                elif kind == AGP_EV_RIM:
                    ag_se("bounce", 0.5)
                elif kind == AGP_EV_TRAY:
                    self._tray_catch(e[1])

        def _add_points(self, v):
            self.shot_score += v
            self.board_score += v
            self.total += v
            self.score = self.total

        def _light(self, i, b, dist, wall, quiet=False):
            m = self.mult()
            val = self.value(i) * m
            c = self.color[i]
            self.hit_order.append(i)
            self.shot_new += 1
            self._add_points(val)
            x, y = self.world.pos(i, self.t)

            if not quiet:
                ag_se("peg_note_%02d" % self._note_for(y))
            ink = AGP_COL_INK[c]
            self._float("+" + ag_num(val), x, y - 18, ink, 16 if c else 12)
            self._spark(x, y, ink, 5, 1.4)

            if c == 1:
                self.outlier_hit += 1
                self.outliers += 1
                self.shot_outliers += 1
                if self.mult() != m:
                    self._say("CONFIDENCE X%d" % self.mult(), None,
                              AGP_LINK_INK, 90)
                    ag_se("level", 0.7)
                if dist >= AGP_LONG_DIST:
                    self._style("LONG RANGE", AGP_LONG_SHOT)
                elif wall:
                    self._style("WALL BOUNCE", AGP_WALL_SHOT)
                if not self.significant and self.shot_outliers in AGP_FREE_OUTLIERS:
                    self._free_ball("EXTRA BALL", "%d OUTLIERS IN ONE SHOT"
                                    % self.shot_outliers)
                self._check_last(i)
            elif c == 2:
                self._grant(i, b)

            # CORRELATIONS: the other end of a tether lights with this one.
            j = self.link_of.get(i)
            if j is not None and self.alive[j] and not self.lit[j]:
                self.lit[j] = True
                self.links_hit += 1
                self.board_links += 1
                self._add_points(AGP_LINK_BONUS)
                self._say("LINKED", "+%s" % ag_num(AGP_LINK_BONUS),
                          AGP_LINK_INK, 80)
                ag_se("chain", 0.8)
                self._light(j, b, 0.0, False, quiet=True)

            # Not during the robustness check: a fan of every unused sample
            # lights forty pegs "in one shot" almost by construction.
            if not self.robust_done:
                for need, pts, label in AGP_COMBO_SHOTS:
                    if self.shot_new == need:
                        self._style(label, pts)

        def _check_last(self, i):
            left = self.outliers_left()
            if left == 1:
                self._find_last()
            elif left <= 0 and not self.significant:
                self._significant(i)

        def _find_last(self):
            self.last_outlier = -1
            for j in range(self.world.n):
                if self.color[j] == 1 and self.alive[j] and not self.lit[j]:
                    self.last_outlier = j
                    return

        def _style(self, label, pts):
            self.style_count += 1
            self.board_style += 1
            self._add_points(pts)
            self._say(label, "+%s" % ag_num(pts), "#ffe08a", 110)
            ag_se("bonus", 0.8)

        def _free_ball(self, label, sub=None):
            self.balls_left += 1
            self.free_balls += 1
            self.board_free += 1
            self._say(label, sub, AGP_LINK_INK, 110)
            ag_se("peg_tray")

        def _grant(self, i, b):
            name = AGP_GRANTS[self.grant][0]
            x, y = self.world.pos(i, self.t)
            ag_se("peg_power")
            self._ring(x, y, AGP_GRANT_INK)
            g = self.grant
            if g == "forecast":
                self.guide_shots += AGP_GUIDE_SHOTS
                self._say(name, "LONG GUIDE FOR %d SHOTS" % self.guide_shots,
                          AGP_GRANT_INK, 130)
            elif g == "replicate":
                nb = b.clone()
                nb.vx = -b.vx if abs(b.vx) > 0.6 else (2.5 if b.vx <= 0 else -2.5)
                self.balls.append(nb)
                self._say(name, "A SECOND BALL", AGP_GRANT_INK, 110)
            elif g == "spill":
                self._spillover(i, b)
            elif g == "resubmit":
                self.resubmits += 1
                self._say(name, "THIS SHOT REPEATS", AGP_GRANT_INK,
                          120)
            elif g == "phack":
                self._p_hack(i)

        def _spillover(self, i, b):
            """SPILLOVER: a contagion outward from the grant peg. Every unlit peg
            within AGP_SPILL_R of a peg already caught lights, ring by ring, for
            AGP_SPILL_HOPS rings and at most AGP_SPILL_MAX pegs."""
            w = self.world
            frontier = [w.pos(i, self.t)]
            caught = 0
            r2 = AGP_SPILL_R * AGP_SPILL_R
            ag_se("boom", 0.6)
            for _hop in range(AGP_SPILL_HOPS):
                ring = []
                for fx, fy in frontier:
                    for j in range(w.n):
                        if caught >= AGP_SPILL_MAX:
                            break
                        if not self.alive[j] or self.lit[j]:
                            continue
                        jx, jy = w.pos(j, self.t)
                        if (jx - fx) ** 2 + (jy - fy) ** 2 < r2:
                            self.lit[j] = True
                            caught += 1
                            ring.append((jx, jy))
                            self._spark(jx, jy, AGP_GRANT_INK, 4, 1.2)
                            self._light(j, b, 0.0, False, quiet=True)
                frontier = ring
                if not frontier or caught >= AGP_SPILL_MAX:
                    break
            self._say(AGP_GRANTS["spill"][0], "%d PEGS LIT" % caught,
                      AGP_GRANT_INK, 110)

        def _p_hack(self, i):
            """P-HACKING: the outliers hardest to reach -- the remaining ones
            farthest from the launcher -- are quietly recoded as data. The
            confidence meter only counts real hits, so the study tops out lower."""
            w = self.world
            cands = [j for j in range(w.n)
                     if self.color[j] == 1 and self.alive[j] and not self.lit[j]]
            cands.sort(key=lambda j: -math.hypot(w.pos(j, self.t)[0] - AGP_PIVOT_X,
                                                 w.pos(j, self.t)[1] - AGP_PIVOT_Y))
            dropped = cands[:AGP_PHACK]
            for j in dropped:
                self.color[j] = 0
                self.excluded.add(j)
                x, y = w.pos(j, self.t)
                self._spark(x, y, AGP_COL_INK[1], 10, 1.8)
                self._float("DROPPED", x, y - 20, AGP_COL_INK[1], 12, ttl=70)
                # A recoded outlier's tether goes with it.
                k = self.link_of.pop(j, None)
                if k is not None:
                    self.link_of.pop(k, None)
            self.links = [(o, d) for o, d in self.links if o not in self.excluded]
            ag_se("peg_gong")
            self._say(AGP_GRANTS["phack"][0], "%d OUTLIERS DROPPED" % len(dropped),
                      AGP_COL_INK[1], 130)
            self._check_last(i)

        def _tray_catch(self, b):
            if self.shot_new == 0:
                self._style("CLEAN CATCH", AGP_NULL_SHOT)
            self._free_ball("EXTRA BALL", "TRAY CATCH")
            self._spark(b.x, AGP_TRAY_Y, AGP_LINK_INK, 14, 2.2)

        def _significant(self, i):
            """The last outlier: the board freezes for a beat and the result is
            stamped; then the ball plays out. The camera punches in on the peg
            and eases back out on its own."""
            self.significant = True
            self.freeze = AGP_FREEZE
            self.zoom_fx, self.zoom_fy = self.world.pos(i, self.t)
            self.zoom = AGP_PUNCH
            self.banner = ["SIGNIFICANT", AGP_LINK_INK, 0, 190,
                           "ALL OUTLIERS CLEARED"]
            # The banner carries the news; callouts underneath it would only
            # print over its letters.
            self.callouts = []
            ag_se("peg_significant")
            try:
                renpy.music.stop(channel="music", fadeout=AGP_FINALE_MUSIC_FADE)
            except Exception:
                pass
            for _n in range(3):
                self._firework(random.uniform(AGP_X0 + 80, AGP_X1 - 80),
                               random.uniform(AGP_Y0 + 60, AGP_Y0 + 300))

        def _end_flight(self):
            self.pop_queue = [i for i in self.hit_order if self.alive[i]]
            # Anything lit without passing through _light still has to leave.
            for i in range(self.world.n):
                if self.lit[i] and self.alive[i] and i not in self.pop_queue:
                    self.pop_queue.append(i)
            self._set_phase("pop")

        # ---- after the shot -------------------------------------------------

        def _step_pop(self):
            self.t += 1
            per_tick = 2 if len(self.pop_queue) > 24 else 1
            if self.phase_t % 3 == 0:
                for _k in range(per_tick):
                    if self.pop_queue:
                        self._pop(self.pop_queue.pop(0))
            if not self.pop_queue and self.phase_t > 10:
                self._after_shot()

        def _pop(self, i, quiet=False):
            if not self.alive[i] and not quiet:
                return
            self.alive[i] = False
            x, y = self.world.pos(i, self.t)
            self._spark(x, y, AGP_COL_INK[self.color[i]], 7, 2.0)
            ag_se("peg_pop", 0.6 if quiet else 1.0)

        def _after_shot(self):
            if self.significant:
                if not self.robust_done and self.balls_left > 0:
                    self._robustness()
                else:
                    self._set_phase("tally")
                return
            if self.shot_score > 0:
                self._float(ag_num(self.shot_score), AGP_PIVOT_X, AGP_Y0 + 150,
                            "#ffffff", 30, ttl=80)
            if self.resubmits > 0:
                # RESUBMISSION: the same shot, through the board as it is now.
                self.resubmits -= 1
                self._say("RE-FIRE", "SAME SHOT AGAIN",
                          AGP_GRANT_INK, 110)
                ag_se("peg_whoosh")
                self._launch(self.last_aim)
                return
            if self.balls_left <= 0:
                self._fail()
                return
            self._set_phase("aim")
            self._update_guide()

        def _robustness(self):
            """ROBUSTNESS CHECK: every unused sample fires at once, fanned evenly
            across the launcher's arc, through a board with no trays. Whatever
            they light is scored at the confidence the study reached."""
            n = self.balls_left
            self.robust_done = True
            self.robust_fired = n
            self.balls_left = 0
            self.world.finale = True
            self.shot_score = 0
            self.shot_new = 0
            self.shot_outliers = 0
            self.shot_ticks = 0
            self.hit_order = []
            lo = math.radians(AGP_FAN_EDGE)
            hi = math.radians(180.0 - AGP_FAN_EDGE)
            self.balls = [self._make_ball(lo + (hi - lo) * ((k + 0.5) / n))
                          for k in range(n)]
            self._set_phase("fly")
            self.banner = ["BONUS ROUND", AGP_GRANT_INK, 0, 120,
                           "EVERY SAVED BALL AT ONCE"]
            ag_se("peg_launch")
            ag_se("peg_whoosh", 0.8)

        def _step_tally(self):
            self.t += 1
            if self.phase_t == 30 and not any(self.alive):
                self.clean_paid = 1
                self._add_points(AGP_CLEAN_SWEEP)
                self._say("EVERY PEG CLEARED", "+%s"
                          % ag_num(AGP_CLEAN_SWEEP), "#ffe08a", 150)
                ag_se("bonus")
            if self.phase_t > (150 if self.clean_paid else 60):
                self._open_card()

        def _open_card(self):
            self.boards_cleared += 1
            self.board_record = ag_set_best("peg_" + self.board_id,
                                            self.board_score)
            n = self.world.n
            data = sum(1 for i in range(n)
                       if not self.alive[i] and self.color[i] == 0)
            data_total = sum(1 for i in range(n) if self.color[i] == 0)
            rows = [
                ("OUTLIERS CLEARED", "%d / %d" % (self.outlier_hit,
                                                 self.outlier_total)),
            ]
            if self.grant == "phack":
                rows.append(("OUTLIERS DROPPED", str(len(self.excluded))))
            rows += [
                ("DATA PEGS CLEARED", "%d / %d" % (data, data_total)),
                ("LINKS", str(self.board_links)),
                ("STYLE SHOTS", str(self.board_style)),
                ("EXTRA BALLS", str(self.board_free)),
                ("BONUS ROUND BALLS", str(self.robust_fired)),
            ]
            self.card_rows = rows
            self.banner = None
            self._set_phase("card")

        def _step_card(self):
            self.t += 1
            if (self.want_fire and self.phase_t > 50) or self.phase_t > 600:
                ag_se("ui_ok")
                if self.full and self.stage + 1 < len(self.order):
                    self.stage += 1
                    self._load_board()
                    self._music_back()
                else:
                    self.cleared = True
                    self.finish("clear")

        def _fail(self):
            self.banner = ["INCONCLUSIVE", "#e0455e", 0, 400]
            ag_se("over")
            self._set_phase("fail")

        def _step_fail(self):
            self.t += 1
            if self.phase_t > 160:
                self.finish("over")

        def _music_back(self):
            """Significance stopped the board music; the next board of a full
            study fades it back in. A lone board never needs this: its run ends
            at the card, and ag_play_loop starts the music for a retry."""
            try:
                music = ag_music_for(self.KIND)
                if music:
                    renpy.music.play(music, channel="music", loop=True,
                                     fadein=AGP_MUSIC_FADEIN, if_changed=True)
            except Exception:
                pass

        # ---- camera and feedback --------------------------------------------

        def _step_camera(self):
            # Only the significance punch zooms, and it eases back to rest --
            # slowly while the board is frozen, quickly once it moves again.
            if self.zoom > 1.0:
                self.zoom += (1.0 - self.zoom) * (0.025 if self.freeze else 0.09)
                if self.zoom - 1.0 < 0.002:
                    self.zoom = 1.0

        def _say(self, text, sub, color, ticks):
            self.callouts.append([text, sub, color, 0, ticks])
            if len(self.callouts) > 3:
                self.callouts.pop(0)

        def _float(self, text, x, y, color, size, ttl=46):
            self.floats.append([text, x, y, color, size, 0, ttl])
            if len(self.floats) > 40:
                self.floats.pop(0)

        def _spark(self, x, y, color, n, speed):
            for _i in range(n):
                a = random.uniform(0.0, 2.0 * math.pi)
                s = random.uniform(0.4, 1.0) * speed
                self.fx.append([x, y, math.cos(a) * s, math.sin(a) * s - 0.6,
                                0, random.randint(16, 30), color, 0.10])
            if len(self.fx) > 260:
                del self.fx[:len(self.fx) - 260]

        def _ring(self, x, y, color, radius=60.0):
            for k in range(28):
                a = k * 2.0 * math.pi / 28
                s = radius / 22.0
                self.fx.append([x, y, math.cos(a) * s, math.sin(a) * s,
                                0, 22, color, 0.0])

        def _firework(self, x, y):
            color = random.choice((AGP_LINK_INK, AGP_GRANT_INK, AGP_COL_INK[1],
                                   "#ffffff", "#b8f0ff"))
            for k in range(22):
                a = k * 2.0 * math.pi / 22 + random.uniform(-0.1, 0.1)
                s = random.uniform(2.2, 3.4)
                self.fx.append([x, y, math.cos(a) * s, math.sin(a) * s,
                                0, random.randint(34, 50), color, 0.06])

        def _step_fx(self):
            if self.banner is not None:
                self.banner[2] += 1
                if self.banner[2] >= self.banner[3]:
                    self.banner = None
            if self.callouts:
                for c in self.callouts:
                    c[3] += 1
                self.callouts = [c for c in self.callouts if c[3] < c[4]]
            if self.floats:
                for f in self.floats:
                    f[5] += 1
                    f[2] -= 0.6
                self.floats = [f for f in self.floats if f[5] < f[6]]
            if self.fx:
                alive = []
                for p in self.fx:
                    p[4] += 1
                    if p[4] >= p[5]:
                        continue
                    p[0] += p[2]
                    p[1] += p[3]
                    p[3] += p[7]
                    p[2] *= 0.97
                    alive.append(p)
                self.fx = alive

        # ---- results --------------------------------------------------------

        def record(self):
            if self.full:
                self.new_record = (ag_set_best("peg_score", self.total)
                                   if self.total else False)
                ag_set_best("peg_boards", self.boards_cleared)
            else:
                self.new_record = bool(self.cleared and self.board_record)

        def outcome(self, kind):
            if kind == "quit":
                return "ABANDONED"
            if kind == "clear":
                return "ALL BOARDS CLEAR" if self.full else "BOARD CLEAR"
            return "INCONCLUSIVE"

        def card_accent(self, kind):
            if kind == "quit":
                return "#8f86a8"
            return "#4fbf7a" if kind == "clear" else "#e0455e"

        def rows(self, kind):
            rows = [("SCORE", ag_num(self.total))]
            if self.full:
                rows.append(("BEST RUN", ag_num(max(self.total,
                                                     ag_best("peg_score")))))
                rows.append(("BOARDS CLEARED", "%d / %d" % (self.boards_cleared,
                                                           len(self.order))))
            else:
                best = ag_best("peg_" + self.board_id)
                if self.cleared:
                    best = max(best, self.board_score)
                rows.append(("BOARD", self.board_name))
                rows.append(("BOARD BEST", ag_num(best) if best else "-"))
            rows.append(("OUTLIERS CLEARED", str(self.outliers)))
            rows.append(("LINKS", str(self.links_hit)))
            rows.append(("EXTRA BALLS", str(self.free_balls)))
            return rows


# =============================================================================
# SHELF
# =============================================================================
init python:

    def ag_peg_cover():
        """Box art: an arc of plot points under the launcher -- one outlier lit,
        one tethered to a data point -- and a sample on its way."""
        parts = ag_cover_base(AGP_ACCENT)
        pts = []
        for k in range(9):
            a = math.radians(18 + k * 18)
            x = 160 + 118 * math.cos(a)
            y = 26 + 118 * math.sin(a)
            sprite = "peg_outlier.png" if k in (2, 6) else "peg_data.png"
            if k == 1:
                sprite = "peg_grant.png"
            elif k == 4:
                sprite = "peg_outlier_lit.png"
            pts.append((x, y))
            parts.append(Transform(AGP_SPR + sprite, pos=(int(x - 16), int(y - 16))))
        ax, ay = pts[6]
        bx, by = 96.0, 150.0
        for k in range(1, 9):
            t = k / 9.0
            parts.append(Transform(Solid(AGP_LINK_INK, xysize=(3, 3)),
                                   pos=(int(ax + (bx - ax) * t),
                                        int(ay + (by - ay) * t))))
        for x, y in ((96, 150), (224, 150)):
            parts.append(Transform(AGP_SPR + "peg_data.png", pos=(x - 16, y - 16)))
        parts.append(Transform(AGP_SPR + "base.png", pos=(118, -6)))
        parts.append(Transform(AGP_SPR + "ball.png", pos=(186, 92)))
        parts += ag_cover_title("PEG SHOOTER", "OUTLIER", AGP_ACCENT)
        return Fixed(*parts, xysize=(AG_COVER_SIZE, AG_COVER_SIZE))


    ag_register(
        "peg", AGPeg,
        title="Outlier",
        accent=AGP_ACCENT,
        blurb="Aim, fire, let it fall. Clear all twenty-two outliers with "
              "fifteen balls. Linked pegs light together, and saved balls fire "
              "in a bonus round.",
        controls=AGPeg.CONTROLS,
        music=audio.tetris,
        cover=ag_peg_cover,
        variants=([("run", "ALL FIVE BOARDS",
                    "in order // one score // no retries")]
                  + [(b[0], "%d   %s" % (k + 1, b[1]), b[4])
                     for k, b in enumerate(AGP_BOARDS)]),
        variant_prompt=_("Play all five boards, or pick one."),
    )
