# =============================================================================
# ag_brick.rpy  --  PEER REVIEW   (Arcade Original #2)
# =============================================================================
# A paddle-and-ball wall breaker where the wall is a PAPER. Matsuda submitted
# something; you are the reviewer, and your only tools are a clipboard, a rubber
# stamp and a very fast ball. Each section of the manuscript is a level; each
# brick is a claim.
#
# WHAT IS KEPT, AND WHAT IS THIS CABINET'S OWN
#   The skeleton is the genre's -- a ball, a paddle that aims it by where it
#   lands, a wall to clear, three lives -- and that part is untouched. What sits
#   on the skeleton is Peer Review's own:
#
#   THE ARGUMENT  claims are joined into arguments. A SOURCE props up every
#                 SUPPORTED claim tethered to it: while it stands they cannot be
#                 hurt (the ball glances off them), and the moment it falls they
#                 COLLAPSE together in a cascade. A section is read before it is
#                 played -- find the load-bearing claim -- and the best shot on
#                 the page is often the awkward one.
#   THE STAMP     tap Z just before the ball meets the clipboard and it leaves
#                 STAMPED: faster, and its next claim takes two hits instead of
#                 one. A stamp that meets nothing locks the next one out for
#                 half a second, so mashing is worse than not stamping at all.
#                 It is the game's one active skill, and it is a timing read.
#   MARGIN NOTES  power-ups are sticky notes that FLUTTER down, swaying side to
#                 side, so a catch is a read of where the note will be rather
#                 than a race to where it is. Four help. ERRATUM is a trap, and
#                 its colour is the only tell:
#                   RED PEN         the ball cuts straight THROUGH claims for a
#                                   few seconds instead of bouncing off them
#                   STRIKETHROUGH   the next claim the ball hits takes its whole
#                                   line down with it
#                   EXTRA BALL      another ball, mirrored off each in play
#                   SAFETY NET      a one-time floor under the clipboard that
#                                   sends the next falling ball back up
#                   ERRATUM         narrower clipboard, faster ball
#
# THE CLAIMS
#   PLAIN       one hit.
#   HEDGED      two hits.
#   ENTRENCHED  three hits. The author is attached to this one.
#   SOURCE      one hit; props up every SUPPORTED claim tethered to it.
#   SUPPORTED   untouchable while its source stands; collapses when it falls.
#               Each is tethered to its NEAREST source, so the tethers on the
#               page are the whole rule.
#   CITED       one hit, but it COMES BACK about twelve seconds later, once. A
#               ghost outline warns where, so a returning claim is a planned
#               problem rather than an ambush.
#   REDACTED    indestructible: the walls of a level, and what make later
#               sections about ANGLES rather than power.
#
# PHYSICS NOTES  (the parts that are easy to get wrong)
#   * The ball moves in SUB-STEPS of at most ~3px, so it never tunnels through a
#     26px claim at a shallow angle or clips the corner of the clipboard.
#   * Only the FIRST solid claim found in a sub-step is resolved; resolving two
#     at once double-reflects the ball somewhere unrelated to what was seen.
#   * The reflection axis comes from comparing penetration depths, which is what
#     makes hitting the SIDE of a claim bounce sideways rather than down.
#   * Every bounce is reshaped so the heading is never nearly flat (a ball that
#     pings wall to wall for half a minute) or exactly vertical (a ball locked
#     into a column it has punched clean through).
#   * A RED PEN ball does not reflect off what it cuts, so it damages a claim
#     once on ENTRY and not again until it has left it.
# =============================================================================

init python:
    import math
    import random

    # --- arena geometry ------------------------------------------------------
    # The page sits under the header band and leaves room at the foot for the
    # effect rail (AGB_BOT + 10) and the control legend at 696.
    AGB_X = 190
    AGB_Y = 104
    AGB_W = 900
    # Height is a PACING number, not a framing one: measured with a realistic
    # keyboard paddle, a taller page left the ball crossing empty space for most
    # of every rally.
    AGB_H = 512
    AGB_BOT = AGB_Y + AGB_H

    AGB_COLS = 12
    AGB_ROWS = 8
    AGB_BW = 70
    AGB_BH = 26
    AGB_GAP = 4
    AGB_GX = AGB_X + (AGB_W - (AGB_COLS * (AGB_BW + AGB_GAP) - AGB_GAP)) // 2
    AGB_GY = AGB_Y + 52

    AGB_PAD_Y = AGB_Y + AGB_H - 34
    AGB_PAD_H = 14
    AGB_PAD_W = 116
    AGB_PAD_NARROW = 76
    # The clipboard is a touch faster than the fastest legal ball, so a perfect
    # read is always reachable on keys -- but only just.
    AGB_PAD_SPEED = 10.0
    AGB_NET_Y = AGB_BOT - 10    # where an EXTENSION catches a falling ball

    AGB_R = 7.0                 # ball radius
    AGB_SPD = 5.4               # base speed, px/tick
    AGB_SPD_STEP = 0.28         # added per section cleared
    AGB_SPD_MAX = 9.2
    AGB_MIN_VY = 0.42           # floor on |vy| as a fraction of speed
    AGB_MIN_VX = 0.15           # floor on |vx| -- see AGBrick._shape
    AGB_LIVES = 3
    AGB_DROP_CHANCE = 0.15
    AGB_ACCENT = "#ff8f5e"

    # --- the stamp -----------------------------------------------------------
    AGB_STAMP_WINDOW = 10       # ticks a press stays live waiting for contact
    AGB_STAMP_COOLDOWN = 30     # ticks a stamp that met nothing locks out
    AGB_STAMP_BOOST = 1.22      # speed multiplier on a stamped return
    AGB_STAMP_DAMAGE = 2        # hits a stamped ball deals to its next claim
    AGB_STAMP_INK = "#ff5a5a"

    # --- the argument --------------------------------------------------------
    AGB_COLLAPSE_STAGGER = 5    # ticks between claims in a collapse
    AGB_COLLAPSE_BONUS = 30     # x position in the cascade
    AGB_TETHER = "#ffd45e"

    # --- margin notes --------------------------------------------------------
    AGB_PEN_TICKS = 420         # seven seconds of RED PEN
    AGB_ERRATUM_TICKS = 600
    AGB_STRIKE_MAX = 2          # STRIKETHROUGH charges that can be banked
    AGB_NOTE_FALL = 2.2         # px per tick
    AGB_NOTE_SWAY = 34.0        # px either side of its line
    AGB_NOTE_RATE = 0.06        # radians per tick
    AGB_NOTE_W = 84             # wide enough for the longest label, readably

    # --- claim types ---------------------------------------------------------
    # char -> (hp, score, base colour, label)
    AGB_TYPES = {
        "1": (1, 50, "#6f7ad6", "PLAIN"),
        "2": (2, 110, "#4fb0c9", "HEDGED"),
        "3": (3, 190, "#c98fe0", "ENTRENCHED"),
        "S": (1, 140, "#ffd45e", "SOURCE"),
        "s": (1, 80, "#7fc9a0", "SUPPORTED"),
        "C": (1, 90, "#d98ab0", "CITED"),
        "R": (0, 0, "#4a4560", "REDACTED"),
    }

    # --- the manuscript ------------------------------------------------------
    # Each section is (name, rows). Rows are 12 characters wide, top row first.
    # After the last section the paper goes back to the top as a REVISION with a
    # faster ball and tougher claims -- the reviewer's nightmare, and a clean
    # endless ramp.
    AGB_SECTIONS = [
        ("ABSTRACT", [
            "111111111111",
            "1ssss11ssss1",
            "11S111111S11",
        ]),
        ("METHODS", [
            "..CC....CC..",
            ".2222222222.",
            "ss11S11S11ss",
            "1..1111111.1",
        ]),
        ("RESULTS", [
            "R1111111111R",
            "1ssss22ssss1",
            "12C3S33S3C21",
            "122222222221",
            "R1111111111R",
        ]),
        ("DISCUSSION", [
            "333333333333",
            "2CCsRRRRsCC2",
            "2ss2S22S2ss2",
            "111111111111",
            "1.1.1.1.1.1.",
        ]),
    ]

    # --- margin notes --------------------------------------------------------
    # id -> (label, colour, weight). ERRATUM is the same size and shape as the
    # rest: its colour is the only warning.
    AGB_NOTES = [
        ("pen", "RED PEN", "#ff7b7b", 20),
        ("strike", "STRIKE", "#ffd45e", 18),
        ("second", "EXTRA BALL", "#5ec8e0", 20),
        ("extend", "SAFETY NET", "#6fdc8c", 18),
        ("erratum", "ERRATUM", "#b98cff", 14),
    ]
    AGB_NOTE_TOTAL = sum(n[3] for n in AGB_NOTES)


    class AGBrick(AGGame):
        """Peer Review: a manuscript whose claims hold each other up."""

        KIND = "brick"
        TITLE = "PEER REVIEW"
        ACCENT = AGB_ACCENT
        # KEYBOARD ONLY, deliberately. A mouse clipboard is not a control option
        # so much as an easier game: a pointer places the paddle instantly and
        # exactly, which removes the travel time every interesting decision here
        # is made of -- and it would make the stamp's timing trivial as well.
        MOUSE = False
        CONTROLS = [
            ("LEFT / RIGHT  or  A / D", "move the paddle"),
            ("Z  or  SPACE", "serve"),
            ("Z  as the ball lands", "stamp it -- faster, hits twice"),
            ("ESC", "pause"),
            ("Q  (while paused)", "give up"),
        ]

        def __init__(self, variant=None):
            super(AGBrick, self).__init__(variant)

            self.section = 0            # index into AGB_SECTIONS
            self.revision = 0           # how many times the paper has looped
            self.lives = AGB_LIVES
            self.bricks = {}            # (col, row) -> dict
            self.pending = []           # cited claims waiting to come back
            self.collapsing = []        # [key, due tick, place, cascade size]
            self.balls = []
            self.drops = []
            self.fx = []
            self.note = None

            self.pad_x = AGB_X + AGB_W / 2.0
            self.pad_w = AGB_PAD_W
            self.serving = True
            self.serve_wait = 0

            # Timed states: ticks remaining, 0 = off.
            self.t_pen = 0
            self.t_narrow = 0
            self.strikes = 0
            self.net = False
            self.strike_fx = None       # [row, ticks]

            self.stamp_live = 0
            self.stamp_cd = 0
            self.stamp_flash = 0

            self.speed = AGB_SPD
            self.bricks_broken = 0
            self.notes_taken = 0
            self.sections_done = 0
            self.collapsed = 0
            self.best_collapse = 0
            self.stamps = 0
            self.clearing = 0           # section-clear flourish timer
            self.dying = 0              # lost-ball flourish timer
            self.over = 0               # game-over flourish timer

            self._load_section()
            self._reset_ball()

        # ---- setup ----------------------------------------------------------

        def _section_name(self):
            name = AGB_SECTIONS[self.section][0]
            if self.revision:
                return "%s  //  REVISION %d" % (name, self.revision + 1)
            return name

        def _load_section(self):
            self.bricks = {}
            self.pending = []
            self.collapsing = []
            rows = AGB_SECTIONS[self.section][1][:AGB_ROWS]
            sources = []
            for r, line in enumerate(rows):
                for col, ch in enumerate(line[:AGB_COLS]):
                    spec = AGB_TYPES.get(ch)
                    if spec is None:
                        continue
                    hp = spec[0]
                    # The paper gets tougher every time it comes back -- except
                    # the argument claims, whose whole point is to go in one hit.
                    if hp and self.revision and ch not in ("S", "s"):
                        hp += min(2, self.revision)
                    self.bricks[(col, r)] = {
                        "type": ch, "hp": hp, "max": max(1, hp),
                        "returns": (1 if ch == "C" else 0), "hit": 0,
                        "src": None,
                    }
                    if ch == "S":
                        sources.append((col, r))

            # Tether every supported claim to its nearest source: Manhattan
            # distance on the grid, ties to the upper, then the left one, so
            # the rule is exactly what the drawn tethers show.
            for key, brick in self.bricks.items():
                if brick["type"] != "s" or not sources:
                    continue
                brick["src"] = min(sources, key=lambda s, k=key: (
                    abs(s[0] - k[0]) + abs(s[1] - k[1]), s[1], s[0]))

            self.speed = min(AGB_SPD_MAX,
                             AGB_SPD + AGB_SPD_STEP * self.sections_done)
            self._say(self._section_name(), AGB_ACCENT, 130)

        def _reset_ball(self):
            self.balls = [self._ball(self.pad_x, AGB_PAD_Y - AGB_R - 1, 0.0, 0.0)]
            self.drops = []
            self.serving = True
            self.serve_wait = 0
            self.stamp_live = 0

        @staticmethod
        def _ball(x, y, vx, vy):
            return {"x": x, "y": y, "vx": vx, "vy": vy, "dead": False,
                    "stamp": 0, "cut": ()}

        def _serve(self):
            if not self.serving or not self.balls:
                return
            self.serving = False
            b = self.balls[0]
            ang = -math.pi / 2.0 + random.uniform(-0.34, 0.34)
            spd = self._speed()
            b["vx"] = math.cos(ang) * spd
            b["vy"] = math.sin(ang) * spd
            ag_se("serve")

        def _speed(self):
            return self.speed

        def _say(self, text, color=None, ticks=90):
            self.note = [text, ticks, color or AGB_ACCENT]

        # ---- geometry -------------------------------------------------------

        def _brick_rect(self, col, row):
            return (AGB_GX + col * (AGB_BW + AGB_GAP),
                    AGB_GY + row * (AGB_BH + AGB_GAP))

        def _brick_centre(self, key):
            bx, by = self._brick_rect(*key)
            return bx + AGB_BW / 2.0, by + AGB_BH / 2.0

        def _destructible_left(self):
            return sum(1 for b in self.bricks.values() if b["type"] != "R")

        def _shielded(self, brick):
            return brick["type"] == "s" and brick["src"] in self.bricks

        def _solid(self, brick):
            """What a RED PEN ball still bounces off."""
            return brick["type"] == "R" or self._shielded(brick)

        # ---- input ----------------------------------------------------------

        def _press_fire(self):
            if self.serving:
                self._serve()
            elif self.stamp_cd <= 0 and self.stamp_live <= 0:
                self.stamp_live = AGB_STAMP_WINDOW

        def _read_input(self, keys):
            if keys is None:
                return
            if self.tapped(keys, "fire", AGB_K_FIRE1, AGB_K_FIRE2, AGB_K_FIRE3):
                self._press_fire()

            move = 0.0
            if self.held(keys, AGB_K_LEFT1, AGB_K_LEFT2):
                move -= 1.0
            if self.held(keys, AGB_K_RIGHT1, AGB_K_RIGHT2):
                move += 1.0
            if move:
                self.pad_x += move * AGB_PAD_SPEED

            half = self.pad_w / 2.0
            self.pad_x = ag_clamp(self.pad_x, AGB_X + half, AGB_X + AGB_W - half)

        # ---- simulation -----------------------------------------------------

        def step(self):
            if self.result is not None:
                return

            keys = self.poll()
            self._read_input(keys)
            self._step_timers()
            self._step_fx()

            if self.over:
                self.over += 1
                if self.over > 120:
                    self.finish("over")
                return

            if self.clearing:
                self.clearing += 1
                if self.clearing > 110:
                    self._next_section()
                return

            if self.dying:
                self.dying += 1
                if self.dying > 70:
                    self.dying = 0
                    self._reset_ball()
                return

            if self.serving:
                # A stalled serve launches itself, so a player who has put the
                # controller down never sits on a dead screen.
                b = self.balls[0]
                b["x"] = self.pad_x
                b["y"] = AGB_PAD_Y - AGB_R - 1
                self.serve_wait += 1
                if self.serve_wait > 240:
                    self._serve()
                return

            self._step_pending()
            self._step_collapse()
            self._step_drops()

            for b in list(self.balls):
                self._move_ball(b)
            self.balls = [b for b in self.balls if not b["dead"]]

            if not self.balls:
                self._lose_ball()
            elif not self._destructible_left():
                self._clear_section()

        def _step_timers(self):
            if self.t_pen > 0:
                self.t_pen -= 1
            if self.t_narrow > 0:
                self.t_narrow -= 1
            if self.stamp_cd > 0:
                self.stamp_cd -= 1
            if self.stamp_flash > 0:
                self.stamp_flash -= 1
            if self.stamp_live > 0:
                self.stamp_live -= 1
                if self.stamp_live == 0:
                    # Met nothing: the lockout is what makes mashing a loss.
                    self.stamp_cd = AGB_STAMP_COOLDOWN
            target = AGB_PAD_NARROW if self.t_narrow else AGB_PAD_W
            if self.pad_w < target:
                self.pad_w = min(target, self.pad_w + 3)
            elif self.pad_w > target:
                self.pad_w = max(target, self.pad_w - 3)

        def _step_fx(self):
            if self.note is not None:
                self.note[1] -= 1
                if self.note[1] <= 0:
                    self.note = None
            if self.strike_fx is not None:
                self.strike_fx[1] -= 1
                if self.strike_fx[1] <= 0:
                    self.strike_fx = None
            # Hit flashes are counted down HERE, not in draw(): the renderer
            # runs once per frame but the simulation runs at a fixed 60Hz.
            for brick in self.bricks.values():
                if brick["hit"] > 0:
                    brick["hit"] -= 1
            if not self.fx:
                return
            alive = []
            for p in self.fx:
                p["life"] += 1
                if p["life"] >= p["ttl"]:
                    continue
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["vy"] += 0.16
                alive.append(p)
            self.fx = alive

        def _step_pending(self):
            if not self.pending:
                return
            still = []
            for item in self.pending:
                col, row, ch, due = item
                if self.tick < due:
                    still.append(item)
                    continue
                bx, by = self._brick_rect(col, row)
                # Never materialise a claim on top of a ball -- that reads as
                # the ball being eaten. Wait a beat and try again.
                blocked = any(
                    bx - AGB_R < b["x"] < bx + AGB_BW + AGB_R
                    and by - AGB_R < b["y"] < by + AGB_BH + AGB_R
                    for b in self.balls)
                if blocked:
                    still.append((col, row, ch, self.tick + 30))
                    continue
                self.bricks[(col, row)] = {
                    "type": ch, "hp": 1, "max": 1, "returns": 0, "hit": 8,
                    "src": None,
                }
                ag_se("rise", 0.7)
            self.pending = still

        def _step_collapse(self):
            if not self.collapsing:
                return
            still = []
            for item in self.collapsing:
                key, due, place, size = item
                if self.tick < due:
                    still.append(item)
                    continue
                brick = self.bricks.get(key)
                if brick is None:
                    continue
                x, y = self._brick_centre(key)
                self._destroy(key, brick, x, y, drops=False)
                self.score += AGB_COLLAPSE_BONUS * place
                self.collapsed += 1
                if place == size:
                    self.best_collapse = max(self.best_collapse, size)
                    self._say("COLLAPSE  x%d" % size, AGB_TETHER, 80)
            self.collapsing = still

        def _step_drops(self):
            if not self.drops:
                return
            half = self.pad_w / 2.0
            alive = []
            for d in self.drops:
                d["y"] += AGB_NOTE_FALL
                d["x"] = ag_clamp(
                    d["x0"] + math.sin(d["phase"] + self.tick * AGB_NOTE_RATE)
                    * AGB_NOTE_SWAY, AGB_X + AGB_NOTE_W / 2.0,
                    AGB_X + AGB_W - AGB_NOTE_W / 2.0)
                if d["y"] > AGB_BOT:
                    continue
                if (d["y"] + 14 >= AGB_PAD_Y
                        and d["y"] <= AGB_PAD_Y + AGB_PAD_H
                        and abs(d["x"] - self.pad_x) <= half + 24):
                    self._take_note(d)
                    continue
                alive.append(d)
            self.drops = alive

        def _take_note(self, d):
            kind = d["kind"]
            self.notes_taken += 1
            self.score += 150
            if kind == "pen":
                self.t_pen = AGB_PEN_TICKS
                self._say("RED PEN  --  THE BALL CUTS THROUGH", "#ff7b7b")
            elif kind == "strike":
                self.strikes = min(AGB_STRIKE_MAX, self.strikes + 1)
                self._say("STRIKE READY  --  NEXT HIT CLEARS A ROW", AGB_TETHER)
            elif kind == "second":
                self._second_opinion()
                self._say("EXTRA BALL", "#5ec8e0")
            elif kind == "extend":
                self.net = True
                self._say("SAFETY NET", "#6fdc8c")
            else:
                # ERRATUM: the trap. Narrower clipboard AND a faster ball.
                self.t_narrow = AGB_ERRATUM_TICKS
                self.speed = min(AGB_SPD_MAX, self.speed + 0.5)
                for b in self.balls:
                    self._rescale(b)
                self._say("ERRATUM  --  SMALLER PADDLE", "#b98cff")
                ag_se("ui_no")
                return
            ag_se("power")

        def _second_opinion(self):
            """One more ball per ball in play (at most four in all), leaving on
            the mirror of that ball's heading."""
            extra = []
            for b in self.balls:
                if len(self.balls) + len(extra) >= 4:
                    break
                nb = self._ball(b["x"], b["y"], -b["vx"], b["vy"])
                if abs(nb["vx"]) < 0.5:
                    nb["vx"] = 2.0 if b["vx"] <= 0 else -2.0
                self._shape(nb)
                extra.append(nb)
            self.balls.extend(extra)

        def _rescale(self, b):
            """Re-point an existing ball at the current speed, keeping heading."""
            spd = math.hypot(b["vx"], b["vy"])
            if spd <= 0.001:
                return
            target = self._speed()
            b["vx"] = b["vx"] / spd * target
            b["vy"] = b["vy"] / spd * target

        # ---- ball ------------------------------------------------------------

        def _move_ball(self, b):
            speed = math.hypot(b["vx"], b["vy"])
            steps = max(1, int(speed / 3.0) + 1)
            for _i in range(steps):
                b["x"] += b["vx"] / steps
                b["y"] += b["vy"] / steps
                self._walls(b)
                if b["dead"]:
                    return
                self._bricks_hit(b)
                self._paddle(b)

        def _walls(self, b):
            if b["x"] - AGB_R < AGB_X:
                b["x"] = AGB_X + AGB_R
                b["vx"] = abs(b["vx"])
                ag_se("bounce", 0.5)
            elif b["x"] + AGB_R > AGB_X + AGB_W:
                b["x"] = AGB_X + AGB_W - AGB_R
                b["vx"] = -abs(b["vx"])
                ag_se("bounce", 0.5)
            if b["y"] - AGB_R < AGB_Y:
                b["y"] = AGB_Y + AGB_R
                b["vy"] = abs(b["vy"])
                ag_se("bounce", 0.5)
            elif (self.net and b["vy"] > 0 and b["y"] + AGB_R >= AGB_NET_Y
                    and b["y"] - AGB_R < AGB_NET_Y):
                # EXTENSION: one save, then it is gone.
                self.net = False
                b["y"] = AGB_NET_Y - AGB_R
                b["vy"] = -abs(b["vy"])
                self._shape(b)
                self._spark(b["x"], AGB_NET_Y, "#6fdc8c", 14)
                self._say("SAFETY NET USED", "#6fdc8c", 60)
                ag_se("bounce")
            elif b["y"] - AGB_R > AGB_BOT:
                b["dead"] = True

        def _bricks_hit(self, b):
            col0 = int((b["x"] - AGB_R - AGB_GX) // (AGB_BW + AGB_GAP))
            col1 = int((b["x"] + AGB_R - AGB_GX) // (AGB_BW + AGB_GAP))
            row0 = int((b["y"] - AGB_R - AGB_GY) // (AGB_BH + AGB_GAP))
            row1 = int((b["y"] + AGB_R - AGB_GY) // (AGB_BH + AGB_GAP))
            pen = self.t_pen > 0
            cutting = []

            for row in range(row0, row1 + 1):
                for col in range(col0, col1 + 1):
                    key = (col, row)
                    brick = self.bricks.get(key)
                    if brick is None:
                        continue
                    bx, by = self._brick_rect(col, row)
                    nx = ag_clamp(b["x"], bx, bx + AGB_BW)
                    ny = ag_clamp(b["y"], by, by + AGB_BH)
                    dx = b["x"] - nx
                    dy = b["y"] - ny
                    if dx * dx + dy * dy > AGB_R * AGB_R:
                        continue

                    if pen and not self._solid(brick):
                        # RED PEN: cut through, once per entry.
                        cutting.append(key)
                        if key not in b["cut"]:
                            self._hit_claim(b, key)
                        continue

                    # Reflect along whichever axis is LESS deeply penetrated:
                    # that is the face the ball actually came through.
                    cx = bx + AGB_BW / 2.0
                    cy = by + AGB_BH / 2.0
                    ox = (AGB_BW / 2.0 + AGB_R) - abs(b["x"] - cx)
                    oy = (AGB_BH / 2.0 + AGB_R) - abs(b["y"] - cy)
                    if ox < oy:
                        b["vx"] = -b["vx"]
                        b["x"] += ox if b["x"] > cx else -ox
                    else:
                        b["vy"] = -b["vy"]
                        b["y"] += oy if b["y"] > cy else -oy
                    self._shape(b)
                    self._hit_claim(b, key)
                    b["cut"] = tuple(cutting)
                    # One solid claim per sub-step: see the header note.
                    return
            b["cut"] = tuple(cutting)

        def _shape(self, b):
            """Keep the heading out of both degenerate corners.

            TOO HORIZONTAL: a ball travelling almost flat pings between the side
            walls for half a minute with nothing the player can do about it.

            TOO VERTICAL: once a column of claims has been punched clean through,
            a ball with vx of exactly zero falls into that channel and bounces
            clipboard-ceiling-clipboard forever -- and it is REACHABLE, because a
            clipboard centred under the ball returns it at exactly ninety
            degrees. So every bounce runs through here, and a ball that comes out
            perfectly vertical gets the smallest sideways component that still
            reads as straight up.
            """
            spd = math.hypot(b["vx"], b["vy"])
            if spd <= 0.001:
                return
            min_vy = spd * AGB_MIN_VY
            min_vx = spd * AGB_MIN_VX
            if abs(b["vy"]) < min_vy:
                b["vy"] = math.copysign(min_vy, b["vy"] or -1.0)
                b["vx"] = math.copysign(
                    math.sqrt(max(0.0, spd * spd - min_vy * min_vy)),
                    b["vx"] or 1.0)
            elif abs(b["vx"]) < min_vx:
                side = b["vx"] or random.choice((-1.0, 1.0))
                b["vx"] = math.copysign(min_vx, side)
                b["vy"] = math.copysign(
                    math.sqrt(max(0.0, spd * spd - min_vx * min_vx)),
                    b["vy"] or -1.0)

        def _paddle(self, b):
            if b["vy"] <= 0:
                return
            if b["y"] + AGB_R < AGB_PAD_Y or b["y"] - AGB_R > AGB_PAD_Y + AGB_PAD_H:
                return
            half = self.pad_w / 2.0
            if abs(b["x"] - self.pad_x) > half + AGB_R:
                return

            # Where on the clipboard it landed decides the angle -- the whole
            # skill of the genre lives in this one line.
            off = ag_clamp((b["x"] - self.pad_x) / half, -1.0, 1.0)
            ang = -math.pi / 2.0 + off * 1.06
            spd = min(AGB_SPD_MAX, math.hypot(b["vx"], b["vy"]) + 0.02)

            if self.stamp_live > 0:
                # THE STAMP: pressed in the window before contact.
                self.stamp_live = 0
                self.stamps += 1
                self.stamp_flash = 18
                self.score += 25
                b["stamp"] = 1
                spd = min(AGB_SPD_MAX + 1.6, spd * AGB_STAMP_BOOST)
                self._spark(b["x"], AGB_PAD_Y, AGB_STAMP_INK, 10)
                ag_se("chain", 0.8)
            else:
                ag_se("bounce")

            b["vx"] = math.cos(ang) * spd
            b["vy"] = math.sin(ang) * spd
            b["y"] = AGB_PAD_Y - AGB_R - 0.5
            self._shape(b)

        # ---- claims ----------------------------------------------------------

        def _hit_claim(self, b, key):
            """The ball has struck a claim: spend a stamp or a strikethrough if
            one is waiting, then do the damage."""
            brick = self.bricks.get(key)
            if brick is None:
                return
            amount = 1
            if b["stamp"]:
                b["stamp"] = 0
                amount = AGB_STAMP_DAMAGE
                self._rescale(b)
            if self.strikes > 0 and not self._solid(brick):
                self.strikes -= 1
                self._strike_row(key[1])
                return
            x, y = self._brick_centre(key)
            self._damage(key, amount, x, y)

        def _damage(self, key, amount, x, y):
            brick = self.bricks.get(key)
            if brick is None:
                return
            if brick["type"] == "R":
                brick["hit"] = 8
                ag_se("crack", 0.5)
                return
            if self._shielded(brick):
                # Glances off -- and the source it hangs from flashes, which is
                # how the rule teaches itself.
                brick["hit"] = 8
                self.bricks[brick["src"]]["hit"] = 14
                ag_se("crack", 0.4)
                return

            brick["hp"] -= amount
            brick["hit"] = 8
            if brick["hp"] > 0:
                self.score += 10
                ag_se("crack")
                self._spark(x, y, AGB_TYPES[brick["type"]][2], 4)
                return
            self._destroy(key, brick, x, y, drops=True)

        def _destroy(self, key, brick, x, y, drops):
            del self.bricks[key]
            self.bricks_broken += 1
            spec = AGB_TYPES[brick["type"]]
            self.score += spec[1]
            self._spark(x, y, spec[2], 12)
            ag_se("smash")

            if brick["returns"]:
                # A cited claim comes back once, twelve seconds later.
                self.pending.append((key[0], key[1], brick["type"],
                                     self.tick + 720))
            if brick["type"] == "S":
                self._topple(key)
            if drops and random.random() < AGB_DROP_CHANCE:
                self._drop(key)

        def _topple(self, src):
            """A source is gone: every claim tethered to it collapses, nearest
            first, a few ticks apart."""
            deps = [k for k, b in self.bricks.items()
                    if b["type"] == "s" and b["src"] == src]
            deps.sort(key=lambda k: (abs(k[0] - src[0]) + abs(k[1] - src[1]),
                                     k[1], k[0]))
            for n, k in enumerate(deps):
                self.collapsing.append(
                    [k, self.tick + (n + 1) * AGB_COLLAPSE_STAGGER, n + 1,
                     len(deps)])

        def _strike_row(self, row):
            """STRIKETHROUGH: every claim in the line that can be argued with
            goes at once. Redacted and still-supported claims stand."""
            self.strike_fx = [row, 24]
            gone = 0
            for key in sorted(k for k in self.bricks if k[1] == row):
                brick = self.bricks.get(key)
                if brick is None or self._solid(brick):
                    continue
                x, y = self._brick_centre(key)
                self._destroy(key, brick, x, y, drops=False)
                gone += 1
            self._say("ROW CLEARED  x%d" % gone, AGB_TETHER, 70)
            ag_se("boom", 0.6)

        def _drop(self, key):
            roll = random.randrange(AGB_NOTE_TOTAL)
            acc = 0
            pick = AGB_NOTES[0]
            for n in AGB_NOTES:
                acc += n[3]
                if roll < acc:
                    pick = n
                    break
            x, y = self._brick_centre(key)
            self.drops.append({
                "x0": x, "x": x, "y": y,
                "phase": random.uniform(0.0, math.pi * 2.0),
                "kind": pick[0], "label": pick[1], "col": pick[2],
            })

        def _spark(self, x, y, color, n):
            for _i in range(n):
                ang = random.uniform(0.0, math.pi * 2.0)
                spd = random.uniform(0.6, 2.4)
                self.fx.append({
                    "x": x, "y": y,
                    "vx": math.cos(ang) * spd, "vy": math.sin(ang) * spd - 0.8,
                    "life": 0, "ttl": random.randint(14, 28), "col": color,
                })

        # ---- run flow --------------------------------------------------------

        def _lose_ball(self):
            self.lives -= 1
            self.t_pen = 0
            self.t_narrow = 0
            ag_se("die")
            if self.lives <= 0:
                self.over = 1
                ag_se("over")
            else:
                self.dying = 1
                self._say("%d BALL%s LEFT"
                          % (self.lives, "" if self.lives == 1 else "S"),
                          "#e0455e", 80)

        def _clear_section(self):
            self.clearing = 1
            self.sections_done += 1
            self.score += 500 + 100 * self.lives
            ag_se("clear")

        def _next_section(self):
            self.clearing = 0
            self.section += 1
            if self.section >= len(AGB_SECTIONS):
                self.section = 0
                self.revision += 1
            self._load_section()
            self._reset_ball()

        # ---- drawing ---------------------------------------------------------

        def draw(self, c):
            self._draw_arena(c)
            self._draw_bricks(c)
            self._draw_drops(c)
            self._draw_paddle(c)
            self._draw_balls(c)
            self._draw_fx(c)
            self._draw_hud(c)

            if self.clearing:
                self._draw_banner(c, "SECTION CLEAR", "#4fbf7a", self.clearing)
            elif self.over:
                self._draw_banner(c, "GAME OVER", "#e0455e", self.over)

        def _draw_arena(self, c):
            c.panel(AGB_X - 12, AGB_Y - 12, AGB_W + 24, AGB_H + 24,
                    top="#161038ea", bottom="#0b0720f2", radius=16,
                    border=1.5, bcolor=(AGB_ACCENT + "55"))
            c.rect("#00000044", AGB_X, AGB_Y, AGB_W, AGB_H)
            # Margin rules, like a page.
            c.rect("#ffffff0c", AGB_X + 36, AGB_Y, 1, AGB_H)
            c.rect("#ffffff0c", AGB_X + AGB_W - 36, AGB_Y, 1, AGB_H)
            # The floor the ball must not cross.
            c.rect("#e0455e33", AGB_X, AGB_BOT - 2, AGB_W, 2)
            if self.net:
                for x in range(int(AGB_X) + 8, int(AGB_X + AGB_W) - 8, 30):
                    c.rect("#6fdc8cbb", x, AGB_NET_Y - 1, 18, 3)

        def _draw_bricks(self, c):
            for (col, row), brick in self.bricks.items():
                bx, by = self._brick_rect(col, row)
                ch = brick["type"]
                spec = AGB_TYPES[ch]

                if ch == "R":
                    c.panel(bx, by, AGB_BW, AGB_BH, top="#22203a",
                            bottom="#15142a", radius=4, border=1.0,
                            bcolor="#ffffff18")
                    c.rect("#05040c", bx + 8, by + 8, AGB_BW - 16, AGB_BH - 16)
                else:
                    shielded = self._shielded(brick)
                    # Damage reads as the face going pale; a supported claim
                    # still under its source is drawn a shade darker, locked.
                    wear = 1.0 - (brick["hp"] / float(brick["max"]))
                    face = ag_mix(spec[2], "#f2ecff", 0.30 * wear)
                    if shielded:
                        face = ag_mix(face, "#0b0720", 0.30)
                    c.panel(bx, by, AGB_BW, AGB_BH,
                            top=ag_mix(face, "#ffffff", 0.18),
                            bottom=ag_mix(face, "#0b0720", 0.30),
                            radius=4)
                    c.rect(ag_mix(spec[2], "#ffffff", 0.5) + "66",
                            bx + 3, by + AGB_BH - 4, AGB_BW - 6, 2)
                    for i in range(brick["max"] - brick["hp"]):
                        c.rect("#0b072077", bx + 8 + i * 9, by + 6, 2, AGB_BH - 12)
                    if ch == "S":
                        # The seal a source wears.
                        c.panel(bx + AGB_BW / 2.0 - 7, by + AGB_BH / 2.0 - 7,
                                14, 14, top="#fff3c4", bottom="#c99a2a",
                                radius=7)
                    elif shielded:
                        for ox in (4, AGB_BW - 10):
                            c.rect(AGB_TETHER + "cc", bx + ox, by + 4, 6, 2)
                            c.rect(AGB_TETHER + "cc", bx + ox + (0 if ox == 4 else 4),
                                   by + 4, 2, 6)

                if brick["hit"] > 0:
                    c.rect("#ffffff%02x" % int(min(14, brick["hit"]) * 16),
                            bx, by, AGB_BW, AGB_BH)

            # Tethers, OVER the claims: through a wall of adjacent claims a
            # tether drawn underneath would only show in the 4px gaps.
            for key, brick in self.bricks.items():
                if self._shielded(brick):
                    self._draw_tether(c, key, brick["src"])

            # Ghost outlines: a cited claim about to be re-asserted.
            for col, row, _ch, due in self.pending:
                left = due - self.tick
                if left > 180:
                    continue
                bx, by = self._brick_rect(col, row)
                pulse = 0.4 + 0.6 * (1.0 - left / 180.0)
                c.frame("#d98ab0%02x" % int(110 * pulse), bx, by,
                        AGB_BW, AGB_BH, 1)

            if self.strike_fx is not None:
                row, left = self.strike_fx
                _bx, by = self._brick_rect(0, row)
                c.rect("%s%02x" % (AGB_STAMP_INK, int(ag_clamp(left * 12, 0, 230))),
                       AGB_X + 20, by + AGB_BH / 2.0 - 2, AGB_W - 40, 4)

        def _draw_tether(self, c, a, b):
            ax, ay = self._brick_centre(a)
            bx, by = self._brick_centre(b)
            dist = math.hypot(bx - ax, by - ay)
            n = max(2, int(dist // 11))
            for k in range(1, n):
                t = k / float(n)
                c.rect(AGB_TETHER + "80", ax + (bx - ax) * t - 1.5,
                       ay + (by - ay) * t - 1.5, 3, 3)

        def _draw_paddle(self, c):
            half = self.pad_w / 2.0
            col = "#b98cff" if self.t_narrow else "#d8d2e8"
            if self.stamp_live > 0:
                col = AGB_STAMP_INK
            c.panel(self.pad_x - half, AGB_PAD_Y, self.pad_w, AGB_PAD_H,
                    top=ag_mix(col, "#ffffff", 0.35),
                    bottom=ag_mix(col, "#221a3a", 0.45), radius=6)
            if self.stamp_cd > 0:
                c.rect("#e0455e99", self.pad_x - half + 6, AGB_PAD_Y + AGB_PAD_H + 3,
                       (self.pad_w - 12) * self.stamp_cd / float(AGB_STAMP_COOLDOWN),
                       2)
            if self.stamp_flash > 0:
                a = ag_clamp(self.stamp_flash / 18.0, 0.0, 1.0)
                c.text("STAMPED", self.pad_x, AGB_PAD_Y - 18, size=13,
                       color=AGB_STAMP_INK, bold=True, kerning=2.0,
                       anchor=(0.5, 0.5), alpha=a)

        def _draw_balls(self, c):
            pen = self.t_pen > 0
            for b in self.balls:
                if b["stamp"]:
                    c.rect(AGB_STAMP_INK + "66", b["x"] - AGB_R - 5,
                           b["y"] - AGB_R - 5, AGB_R * 2 + 10, AGB_R * 2 + 10,
                           sub=True)
                c.rect("#ffffff22", b["x"] - AGB_R - 2, b["y"] - AGB_R - 2,
                        AGB_R * 2 + 4, AGB_R * 2 + 4, sub=True)
                c.rect("#ffb0b0" if pen else "#fdfbff", b["x"] - AGB_R,
                       b["y"] - AGB_R, AGB_R * 2, AGB_R * 2, sub=True)
            if self.serving and self.balls:
                b = self.balls[0]
                pulse = 0.5 + 0.5 * math.sin(self.tick * 0.15)
                c.text("Z / SPACE TO SERVE", b["x"], b["y"] - 34, size=14,
                        color=AGB_ACCENT, anchor=(0.5, 0.5), alpha=pulse)

        def _draw_drops(self, c):
            for d in self.drops:
                # A sticky note with a folded corner, wide enough for the
                # longest label.
                x = d["x"] - AGB_NOTE_W / 2.0
                y = d["y"] - 14
                c.rect("#00000044", x + 3, y + 4, AGB_NOTE_W, 28)
                c.rect(d["col"], x, y, AGB_NOTE_W, 28)
                c.rect(ag_mix(d["col"], "#ffffff", 0.35), x, y, AGB_NOTE_W, 5)
                c.rect(ag_mix(d["col"], "#0b0720", 0.35), x + AGB_NOTE_W - 8,
                       y + 20, 8, 8)
                c.text(d["label"], d["x"], d["y"] + 2, size=10,
                       color="#0b0720", bold=True, anchor=(0.5, 0.5),
                       outline=None)

        def _draw_fx(self, c):
            for p in self.fx:
                t = p["life"] / float(p["ttl"])
                size = max(2, int(6 * (1.0 - t)))
                c.rect("%s%02x" % (p["col"], int(220 * (1.0 - t))),
                        p["x"] - size / 2.0, p["y"] - size / 2.0,
                        size, size, sub=True)

        def _draw_hud(self, c):
            c.header("PEER REVIEW", self._section_name(), AGB_ACCENT)
            c.stat_row([
                ("CLAIMS", str(self._destructible_left()), AG_DIM),
                ("BALLS", str(self.lives),
                    ("#e0455e" if self.lives <= 1 else AG_INK)),
                ("BEST", ag_num(max(self.score, ag_best("brick_score"))),
                    AG_DIM),
                ("SCORE", ag_num(self.score), AG_INK),
            ])

            # Live effects, centred under the page: only what is actually in
            # force is drawn, so the rail is empty most of the time.
            live = []
            if self.t_pen:
                live.append(("RED PEN", self.t_pen / float(AGB_PEN_TICKS),
                             "#ff7b7b"))
            if self.strikes:
                live.append(("STRIKE x%d" % self.strikes, None, AGB_TETHER))
            if self.net:
                live.append(("SAFETY NET", None, "#6fdc8c"))
            if self.t_narrow:
                live.append(("ERRATUM", self.t_narrow / float(AGB_ERRATUM_TICKS),
                             "#b98cff"))
            if live:
                pitch = 120
                x = AG_W / 2 - (len(live) * pitch - 24) / 2
                y = AGB_BOT + 10
                for label, frac, col in live:
                    c.text(label, x, y, size=12, color=col, bold=True,
                            kerning=1.5)
                    if frac is not None:
                        c.bar(x, y + 16, 96, 4, frac, col)
                    else:
                        c.rect(col, x, y + 16, 96, 4)
                    x += pitch

            # Callouts flash inside the page, above the clipboard.
            if self.note is not None:
                text, left, col = self.note
                c.text(text, AG_W / 2, AGB_PAD_Y - 52, size=20, color=col,
                        bold=True, kerning=2.0, anchor=(0.5, 0.5),
                        alpha=ag_clamp(left / 40.0, 0.0, 1.0))

            c.legend("ARROWS MOVE   //   Z SERVE   //   TAP Z AS THE BALL LANDS "
                     "TO STAMP   //   ESC PAUSE")

        def _draw_banner(self, c, text, color, timer):
            a = ag_clamp(timer / 20.0, 0.0, 1.0)
            c.rect("#0a0713%02x" % int(150 * a), 0, 0, AG_W, AG_H)
            c.text(text, AG_W / 2, AG_H / 2, size=46, color=color,
                    font=AG_FONT, bold=True, anchor=(0.5, 0.5), alpha=a)

        # ---- results ---------------------------------------------------------

        def record(self):
            self.new_record = ag_set_best("brick_score", self.score)
            ag_set_best("brick_sections", self.sections_done)

        def outcome(self, kind):
            return "ABANDONED" if kind == "quit" else "GAME OVER"

        def card_accent(self, kind):
            if kind == "quit":
                return "#8f86a8"
            return "#4fbf7a" if self.sections_done >= 4 else "#e0455e"

        def rows(self, kind):
            return [
                ("SCORE", ag_num(self.score)),
                ("BEST", ag_num(max(self.score, ag_best("brick_score")))),
                ("SECTIONS CLEARED", str(self.sections_done)),
                ("CLAIMS BROKEN", str(self.bricks_broken)),
                ("COLLAPSED  (BIGGEST)", "%d  (%d)" % (self.collapsed,
                                                       self.best_collapse)),
                ("STAMPS LANDED", str(self.stamps)),
            ]


    # Keycodes, resolved once. Kept as module constants so the hot input path is
    # attribute-free.
    try:
        import pygame_sdl2 as _agb_pg
        AGB_K_LEFT1, AGB_K_LEFT2 = _agb_pg.K_LEFT, _agb_pg.K_a
        AGB_K_RIGHT1, AGB_K_RIGHT2 = _agb_pg.K_RIGHT, _agb_pg.K_d
        AGB_K_FIRE1, AGB_K_FIRE2, AGB_K_FIRE3 = (
            _agb_pg.K_z, _agb_pg.K_SPACE, _agb_pg.K_RETURN)
    except Exception:
        AGB_K_LEFT1 = AGB_K_LEFT2 = AGB_K_RIGHT1 = AGB_K_RIGHT2 = -1
        AGB_K_FIRE1 = AGB_K_FIRE2 = AGB_K_FIRE3 = -1


    def ag_brick_cover():
        """Box art: a page of claims hanging off one gold source, a stamped
        ball on its way up to it."""
        parts = ag_cover_base(AGB_ACCENT)
        rows = ["1s1s", "1S21", "1C21", "11.1"]
        for r, line in enumerate(rows):
            for col, ch in enumerate(line):
                spec = AGB_TYPES.get(ch)
                if spec is None:
                    continue
                parts.append(Transform(
                    Solid(spec[2], xysize=(56, 26)),
                    pos=(34 + col * 64, 40 + r * 34)))
        for x, y in ((98, 78), (110, 72), (130, 66), (150, 60)):
            parts.append(Transform(Solid(AGB_TETHER, xysize=(4, 4)), pos=(x, y)))
        parts.append(Transform(Solid("#fff3c4", xysize=(14, 14)), pos=(83, 80)))
        parts.append(Transform(Solid(AGB_STAMP_INK + "88", xysize=(24, 24)),
                               pos=(191, 181)))
        parts.append(Transform(Solid("#fdfbff", xysize=(14, 14)), pos=(196, 186)))
        parts.append(Transform(Solid("#d8d2e8", xysize=(76, 10)), pos=(150, 208)))
        parts += ag_cover_title("BRICK BREAKER", "PEER REVIEW", AGB_ACCENT)
        return Fixed(*parts, xysize=(AG_COVER_SIZE, AG_COVER_SIZE))


    ag_register(
        "brick", AGBrick,
        title="Peer Review",
        accent=AGB_ACCENT,
        blurb="A brick breaker on a page of claims, played on keys. Break a "
                "gold source and the claims tethered to it collapse, tap Z as "
                "the ball lands to stamp it for a harder hit, and watch the "
                "falling notes -- one of them is a trap.",
        controls=AGBrick.CONTROLS,
        music=audio.tetris,
        cover=ag_brick_cover,
    )
