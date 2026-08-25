# =============================================================================
# ag_brick.rpy  --  PEER REVIEW   (Arcade Original #2)
# =============================================================================
# A brick breaker where the wall is a PAPER. Matsuda submitted something; you
# are the reviewer, and the only review tool you have is a clipboard and a very
# fast ball. Each section of the manuscript is a level; each brick is a claim.
#
# THE FOUR CLAIM TYPES (and why the wall is not just HP)
#   PLAIN       one hit. The bulk of any section.
#   SUPPORTED   two hits -- it has a citation propping it up, so it cracks
#               before it breaks.
#   ENTRENCHED  three hits. The author is attached to this one.
#   CITED       one hit, but it COMES BACK about twelve seconds later, once. A
#               claim that gets re-asserted in the rebuttal. A ghost outline
#               shows where and warns you it is coming, so a returning brick is
#               a planned problem rather than an ambush.
#   REDACTED    indestructible. It cannot be argued with because you are not
#               allowed to see it. These are the walls of the level, and they
#               are what make later sections about ANGLES rather than power.
#
# POWER-UPS  (they drop from broken claims, and one of them is a trap)
#   WIDE / MULTI / LASER / SLOW are the good four. ERRATUM is the fifth: it
#   looks the same until you catch it, then it narrows the clipboard and speeds
#   the ball up. It exists so that hoovering up every falling capsule is a
#   decision instead of a reflex -- and its colour is the tell, if you know it.
#
# PHYSICS NOTES  (the parts that are easy to get wrong)
#   * The ball moves in SUB-STEPS of at most ~3px. A ball travelling 8px/tick
#     that moved in one jump could pass clean through a 26px brick row at a
#     shallow angle, or clip the corner of the paddle. Sub-stepping costs a few
#     more collision tests per tick and removes tunnelling entirely.
#   * Only the FIRST brick found in a sub-step is resolved. Resolving two at
#     once double-reflects the ball and sends it somewhere unrelated to what the
#     player saw.
#   * The reflection axis comes from comparing penetration depths, not from the
#     ball's velocity sign -- that is what makes hitting the SIDE of a brick
#     bounce sideways rather than down.
#   * After every brick hit the velocity is re-normalised so |vy| never drops
#     below AGB_MIN_VY of the speed. Without it, a ball can end up travelling
#     almost horizontally and ping between the two walls for half a minute with
#     nothing the player can do.
# =============================================================================

init python:
    import math
    import random

    # --- arena geometry ------------------------------------------------------
    # The page sits under the header band and leaves room at the foot for the
    # power-up rail (AGB_BOT + 18) and the control legend at 696.
    AGB_X = 190
    AGB_Y = 104
    AGB_W = 900
    # Height is a PACING number, not a framing one. Measured with a realistic
    # keyboard paddle: on a 546-tall page the ball spent most of every rally in
    # the empty gap between the claims and the clipboard -- ~73 brick contacts
    # in five minutes, i.e. a rally every four and a half seconds. Shortening
    # the transit and quickening the ball roughly doubles the contact rate
    # without making anything harder to read.
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
    AGB_PAD_WIDE = 168
    AGB_PAD_NARROW = 76
    # The clipboard is a touch faster than the fastest legal ball, so a
    # perfect read is always physically reachable on keys -- but only just,
    # and only if you start moving early.
    AGB_PAD_SPEED = 10.0

    AGB_R = 7.0                 # ball radius
    AGB_SPD = 5.4               # base speed, px/tick
    AGB_SPD_STEP = 0.28         # added per section cleared
    AGB_SPD_MAX = 9.2
    # 0.42, not 0.30: the paddle already returns the ball at 0.49 or steeper,
    # so this only governs what a brick bounce may leave behind -- and at 0.30 a
    # rally could drift to seventeen degrees off horizontal and spend two
    # hundred ticks crossing the page without threatening anything.
    AGB_MIN_VY = 0.42           # floor on |vy| as a fraction of speed
    AGB_MIN_VX = 0.15           # floor on |vx| -- see AGBrick._shape
    AGB_LIVES = 3
    AGB_DROP_CHANCE = 0.15
    AGB_ACCENT = "#ff8f5e"

    # --- claim types ---------------------------------------------------------
    # char -> (hp, score, base colour, label)
    AGB_TYPES = {
        "1": (1, 50, "#6f7ad6", "PLAIN"),
        "2": (2, 110, "#4fb0c9", "SUPPORTED"),
        "3": (3, 190, "#c98fe0", "ENTRENCHED"),
        "C": (1, 90, "#e0c05e", "CITED"),
        "R": (0, 0, "#4a4560", "REDACTED"),
    }

    # --- the manuscript ------------------------------------------------------
    # Each section is (name, rows). Rows are 12 characters wide, top row first.
    # After the last section the paper goes back to the top as a REVISION with
    # a faster ball -- the reviewer's nightmare, and a clean endless ramp.
    AGB_SECTIONS = [
        ("ABSTRACT", [
            "111111111111",
            "111111111111",
            "122222222221",
        ]),
        ("METHODS", [
            "..CC....CC..",
            ".2222222222.",
            "111111111111",
            "1..1111111.1",
        ]),
        ("RESULTS", [
            "R1111111111R",
            "122222222221",
            "12C33333C221",
            "122222222221",
            "R1111111111R",
        ]),
        ("DISCUSSION", [
            "333333333333",
            "2CC22RR22CC2",
            "222222222222",
            "111111111111",
            "1.1.1.1.1.1.",
        ]),
    ]

    # --- power-ups -----------------------------------------------------------
    # id -> (label, colour, weight). ERRATUM is deliberately the same size and
    # shape as the rest: the colour is the only warning.
    AGB_POWERS = [
        ("wide", "WIDE", "#4fbf7a", 22),
        ("multi", "MULTI", "#5ec8e0", 20),
        ("laser", "LASER", "#ffd45e", 18),
        ("slow", "SLOW", "#9d8fe0", 16),
        ("erratum", "ERRATUM", "#e0455e", 14),
    ]
    AGB_POWER_TOTAL = sum(p[3] for p in AGB_POWERS)


    class AGBrick(AGGame):
        """Peer Review: brick breaker over a manuscript that argues back."""

        KIND = "brick"
        TITLE = "PEER REVIEW"
        ACCENT = AGB_ACCENT
        # KEYBOARD ONLY, deliberately. An earlier draft let the mouse drive the
        # clipboard, and it was not a control option so much as an easier game:
        # a pointer places the paddle instantly and exactly, which removes the
        # travel time that every interesting decision here is made of (do I go
        # for the falling power-up or stay under the ball?). Keys make position
        # cost something.
        MOUSE = False
        CONTROLS = [
            ("LEFT / RIGHT  or  A / D", "move the clipboard"),
            ("Z  or  SPACE", "serve, and fire the rebuttal laser"),
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
            self.balls = []
            self.drops = []
            self.shots = []
            self.fx = []
            self.note = None

            self.pad_x = AGB_X + AGB_W / 2.0
            self.pad_w = AGB_PAD_W
            self.serving = True
            self.serve_wait = 0

            # Timed states: ticks remaining, 0 = off.
            self.t_wide = 0
            self.t_narrow = 0
            self.t_laser = 0
            self.t_slow = 0
            self.laser_cd = 0

            self.speed = AGB_SPD
            self.bricks_broken = 0
            self.powers_taken = 0
            self.sections_done = 0
            self.clearing = 0           # level-clear flourish timer
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
            rows = AGB_SECTIONS[self.section][1][:AGB_ROWS]
            for r, line in enumerate(rows):
                for col, ch in enumerate(line[:AGB_COLS]):
                    if ch == ".":
                        continue
                    spec = AGB_TYPES.get(ch)
                    if spec is None:
                        continue
                    hp = spec[0]
                    # The paper gets tougher every time it comes back: one extra
                    # hit on everything that can be hit at all.
                    if hp and self.revision:
                        hp += min(2, self.revision)
                    self.bricks[(col, r)] = {
                        "type": ch, "hp": hp, "max": max(1, hp),
                        "returns": (1 if ch == "C" else 0), "hit": 0,
                    }
            self.speed = min(AGB_SPD_MAX,
                            AGB_SPD + AGB_SPD_STEP * self.sections_done)
            self._say(self._section_name(), AGB_ACCENT, 130)

        def _reset_ball(self):
            self.balls = [{
                "x": self.pad_x, "y": AGB_PAD_Y - AGB_R - 1,
                "vx": 0.0, "vy": 0.0, "dead": False,
            }]
            self.drops = []
            self.shots = []
            self.serving = True
            self.serve_wait = 0

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
            return self.speed * (0.78 if self.t_slow else 1.0)

        def _say(self, text, color=None, ticks=90):
            self.note = [text, ticks, color or AGB_ACCENT]

        # ---- geometry -------------------------------------------------------

        def _brick_rect(self, col, row):
            return (AGB_GX + col * (AGB_BW + AGB_GAP),
                    AGB_GY + row * (AGB_BH + AGB_GAP))

        def _destructible_left(self):
            return sum(1 for b in self.bricks.values() if b["type"] != "R")

        # ---- input ----------------------------------------------------------

        def _press_fire(self):
            if self.serving:
                self._serve()
            elif self.t_laser and self.laser_cd <= 0:
                self._fire()

        def _fire(self):
            self.laser_cd = 14
            for side in (-1, 1):
                self.shots.append({
                    "x": self.pad_x + side * (self.pad_w / 2.0 - 6),
                    "y": AGB_PAD_Y - 4,
                })
            ag_se("shoot")

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
            self._step_shots()
            self._step_drops()

            for b in list(self.balls):
                self._move_ball(b)
            self.balls = [b for b in self.balls if not b["dead"]]

            if not self.balls:
                self._lose_ball()
            elif not self._destructible_left():
                self._clear_section()

        def _step_timers(self):
            for name in ("t_wide", "t_narrow", "t_laser", "t_slow"):
                v = getattr(self, name)
                if v > 0:
                    setattr(self, name, v - 1)
            if self.laser_cd > 0:
                self.laser_cd -= 1
            # WIDE and ERRATUM's narrowing are opposites; whichever was caught
            # last is the one in force, which is why they are separate timers
            # rather than one width value.
            if self.t_narrow:
                target = AGB_PAD_NARROW
            elif self.t_wide:
                target = AGB_PAD_WIDE
            else:
                target = AGB_PAD_W
            if self.pad_w < target:
                self.pad_w = min(target, self.pad_w + 3)
            elif self.pad_w > target:
                self.pad_w = max(target, self.pad_w - 3)

        def _step_fx(self):
            if self.note is not None:
                self.note[1] -= 1
                if self.note[1] <= 0:
                    self.note = None
            # Hit flashes are counted down HERE, not in draw(): the renderer
            # runs once per frame but the simulation runs at a fixed 60Hz, so a
            # flash decremented while drawing would last twice as long on a
            # 30fps machine as on a 60fps one.
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
                # Never materialise a brick on top of a ball -- that reads as
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
                }
                ag_se("rise", 0.7)
            self.pending = still

        def _step_shots(self):
            if not self.shots:
                return
            alive = []
            for s in self.shots:
                s["y"] -= 11.0
                if s["y"] < AGB_Y:
                    continue
                hit = self._brick_at(s["x"], s["y"])
                if hit is not None:
                    self._damage(hit, 1, s["x"], s["y"])
                    continue
                alive.append(s)
            self.shots = alive

        def _step_drops(self):
            if not self.drops:
                return
            half = self.pad_w / 2.0
            alive = []
            for d in self.drops:
                d["y"] += 2.4
                if d["y"] > AGB_BOT:
                    continue
                if (d["y"] + 10 >= AGB_PAD_Y
                        and d["y"] <= AGB_PAD_Y + AGB_PAD_H
                        and abs(d["x"] - self.pad_x) <= half + 14):
                    self._take_power(d)
                    continue
                alive.append(d)
            self.drops = alive

        def _take_power(self, d):
            kind = d["kind"]
            self.powers_taken += 1
            self.score += 150
            if kind == "wide":
                self.t_wide = 900
                self.t_narrow = 0
                self._say("WIDER MARGINS", "#4fbf7a")
            elif kind == "multi":
                self._multiball()
                self._say("SECOND OPINION", "#5ec8e0")
            elif kind == "laser":
                self.t_laser = 900
                self._say("REBUTTAL ARMED  --  Z TO FIRE", "#ffd45e")
            elif kind == "slow":
                self.t_slow = 600
                self._say("CAREFUL READING", "#9d8fe0")
            else:
                # ERRATUM: the trap. Narrower clipboard AND a faster ball.
                self.t_narrow = 600
                self.t_wide = 0
                self.speed = min(AGB_SPD_MAX, self.speed + 0.5)
                for b in self.balls:
                    self._rescale(b)
                self._say("ERRATUM ISSUED", "#e0455e")
                ag_se("ui_no")
                return
            ag_se("power")

        def _multiball(self):
            if not self.balls:
                return
            extra = []
            for b in self.balls[:3]:
                spd = math.hypot(b["vx"], b["vy"]) or self._speed()
                base = math.atan2(b["vy"], b["vx"])
                for delta in (-0.42, 0.42):
                    extra.append({
                        "x": b["x"], "y": b["y"],
                        "vx": math.cos(base + delta) * spd,
                        "vy": math.sin(base + delta) * spd,
                        "dead": False,
                    })
            self.balls.extend(extra[:6])

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
            elif b["y"] - AGB_R > AGB_BOT:
                b["dead"] = True

        def _brick_at(self, x, y):
            """Grid lookup for a point (used by the laser)."""
            col = int((x - AGB_GX) // (AGB_BW + AGB_GAP))
            row = int((y - AGB_GY) // (AGB_BH + AGB_GAP))
            if (col, row) not in self.bricks:
                return None
            bx, by = self._brick_rect(col, row)
            if bx <= x <= bx + AGB_BW and by <= y <= by + AGB_BH:
                return (col, row)
            return None

        def _bricks_hit(self, b):
            col0 = int((b["x"] - AGB_R - AGB_GX) // (AGB_BW + AGB_GAP))
            col1 = int((b["x"] + AGB_R - AGB_GX) // (AGB_BW + AGB_GAP))
            row0 = int((b["y"] - AGB_R - AGB_GY) // (AGB_BH + AGB_GAP))
            row1 = int((b["y"] + AGB_R - AGB_GY) // (AGB_BH + AGB_GAP))

            for row in range(row0, row1 + 1):
                for col in range(col0, col1 + 1):
                    key = (col, row)
                    if key not in self.bricks:
                        continue
                    bx, by = self._brick_rect(col, row)
                    nx = ag_clamp(b["x"], bx, bx + AGB_BW)
                    ny = ag_clamp(b["y"], by, by + AGB_BH)
                    dx = b["x"] - nx
                    dy = b["y"] - ny
                    if dx * dx + dy * dy > AGB_R * AGB_R:
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
                    self._damage(key, 1, b["x"], b["y"])
                    # One brick per sub-step: see the header note.
                    return

        def _shape(self, b):
            """Keep the heading out of both degenerate corners.

            TOO HORIZONTAL is the one every brick breaker guards against: a ball
            that ends up travelling almost flat pings between the side walls for
            half a minute with nothing the player can do about it.

            TOO VERTICAL is the one this game had to learn about. Once a column
            of claims has been punched clean through, a ball with vx of exactly
            zero falls into that channel and bounces paddle-ceiling-paddle
            forever -- and it is REACHABLE, because a paddle centred under the
            ball returns it at exactly ninety degrees, and the clipboard stops
            dead the moment the key is released. Measured in the harness: a
            perfectly tracking paddle broke three bricks in five minutes and
            then span its wheels. So the paddle bounce and every brick bounce
            both run through here, and a ball that comes out perfectly vertical
            is given the smallest sideways component that still reads as
            straight up.
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
            # skill of the game lives in this one line.
            off = ag_clamp((b["x"] - self.pad_x) / half, -1.0, 1.0)
            ang = -math.pi / 2.0 + off * 1.06
            spd = min(AGB_SPD_MAX, math.hypot(b["vx"], b["vy"]) + 0.02)
            b["vx"] = math.cos(ang) * spd
            b["vy"] = math.sin(ang) * spd
            b["y"] = AGB_PAD_Y - AGB_R - 0.5
            self._shape(b)
            ag_se("bounce")

        # ---- bricks ----------------------------------------------------------

        def _damage(self, key, amount, x, y):
            brick = self.bricks.get(key)
            if brick is None:
                return
            if brick["type"] == "R":
                brick["hit"] = 8
                ag_se("crack", 0.5)
                return

            brick["hp"] -= amount
            brick["hit"] = 8
            spec = AGB_TYPES[brick["type"]]

            if brick["hp"] > 0:
                self.score += 10
                ag_se("crack")
                self._spark(x, y, spec[2], 4)
                return

            del self.bricks[key]
            self.bricks_broken += 1
            self.score += spec[1]
            self._spark(x, y, spec[2], 12)
            ag_se("smash")

            if brick["returns"]:
                # A cited claim comes back once, twelve seconds later.
                self.pending.append((key[0], key[1], brick["type"],
                                    self.tick + 720))

            if random.random() < AGB_DROP_CHANCE:
                self._drop(key)

        def _drop(self, key):
            roll = random.randrange(AGB_POWER_TOTAL)
            acc = 0
            pick = AGB_POWERS[0]
            for p in AGB_POWERS:
                acc += p[3]
                if roll < acc:
                    pick = p
                    break
            bx, by = self._brick_rect(*key)
            self.drops.append({
                "x": bx + AGB_BW / 2.0, "y": by + AGB_BH / 2.0,
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
            self.t_laser = 0
            self.t_narrow = 0
            ag_se("die")
            if self.lives <= 0:
                self.over = 1
                ag_se("over")
            else:
                self.dying = 1
                self._say("%d REVIEW%s LEFT"
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
            self._draw_shots(c)
            self._draw_paddle(c)
            self._draw_balls(c)
            self._draw_fx(c)
            self._draw_hud(c)

            if self.clearing:
                self._draw_banner(c, "SECTION ACCEPTED", "#4fbf7a", self.clearing)
            elif self.over:
                self._draw_banner(c, "MANUSCRIPT REJECTS YOU", "#e0455e", self.over)

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
                    # Damage reads as the face going pale and losing its lip.
                    wear = 1.0 - (brick["hp"] / float(brick["max"]))
                    face = ag_mix(spec[2], "#f2ecff", 0.30 * wear)
                    c.panel(bx, by, AGB_BW, AGB_BH,
                            top=ag_mix(face, "#ffffff", 0.18),
                            bottom=ag_mix(face, "#0b0720", 0.30),
                            radius=4)
                    c.rect(ag_mix(spec[2], "#ffffff", 0.5) + "66",
                            bx + 3, by + AGB_BH - 4, AGB_BW - 6, 2)
                    for i in range(brick["max"] - brick["hp"]):
                        c.rect("#0b072077", bx + 8 + i * 9, by + 6, 2, AGB_BH - 12)

                if brick["hit"] > 0:
                    c.rect("#ffffff%02x" % int(brick["hit"] * 22),
                            bx, by, AGB_BW, AGB_BH)

            # Ghost outlines: a cited claim about to be re-asserted.
            for col, row, _ch, due in self.pending:
                left = due - self.tick
                if left > 180:
                    continue
                bx, by = self._brick_rect(col, row)
                pulse = 0.4 + 0.6 * (1.0 - left / 180.0)
                c.frame("#e0c05e%02x" % int(90 * pulse), bx, by,
                        AGB_BW, AGB_BH, 1)

        def _draw_paddle(self, c):
            half = self.pad_w / 2.0
            col = "#e0455e" if self.t_narrow else (
                "#4fbf7a" if self.t_wide else "#d8d2e8")
            c.panel(self.pad_x - half, AGB_PAD_Y, self.pad_w, AGB_PAD_H,
                    top=ag_mix(col, "#ffffff", 0.35),
                    bottom=ag_mix(col, "#221a3a", 0.45), radius=6)
            if self.t_laser:
                for side in (-1, 1):
                    c.rect("#ffd45e", self.pad_x + side * (half - 6) - 2,
                            AGB_PAD_Y - 6, 4, 6)

        def _draw_balls(self, c):
            for b in self.balls:
                c.rect("#ffffff22", b["x"] - AGB_R - 2, b["y"] - AGB_R - 2,
                        AGB_R * 2 + 4, AGB_R * 2 + 4, sub=True)
                c.rect("#fdfbff", b["x"] - AGB_R, b["y"] - AGB_R,
                        AGB_R * 2, AGB_R * 2, sub=True)
            if self.serving and self.balls:
                b = self.balls[0]
                pulse = 0.5 + 0.5 * math.sin(self.tick * 0.15)
                c.text("Z / SPACE TO SERVE", b["x"], b["y"] - 34, size=14,
                        color=AGB_ACCENT, anchor=(0.5, 0.5), alpha=pulse)

        def _draw_shots(self, c):
            for s in self.shots:
                c.rect("#ffd45e", s["x"] - 2, s["y"] - 12, 4, 14, sub=True)

        def _draw_drops(self, c):
            for d in self.drops:
                c.panel(d["x"] - 26, d["y"] - 9, 52, 18,
                        top=ag_mix(d["col"], "#ffffff", 0.25),
                        bottom=ag_mix(d["col"], "#0b0720", 0.35), radius=5)
                c.text(d["label"], d["x"], d["y"], size=11, color="#0b0720",
                        bold=True, anchor=(0.5, 0.5), outline=None)

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
                ("REVIEWS", str(self.lives),
                    ("#e0455e" if self.lives <= 1 else AG_INK)),
                ("BEST", ag_num(max(self.score, ag_best("brick_score"))),
                    AG_DIM),
                ("SCORE", ag_num(self.score), AG_INK),
            ])

            # Live power-up timers, centred under the page: only the ones
            # actually running are drawn, so the rail is empty most of the time.
            live = [(label, left, span, col)
                    for label, left, span, col in (
                        ("WIDE", self.t_wide, 900, "#4fbf7a"),
                        ("LASER", self.t_laser, 900, "#ffd45e"),
                        ("SLOW", self.t_slow, 600, "#9d8fe0"),
                        ("ERRATUM", self.t_narrow, 600, "#e0455e"))
                    if left]
            if live:
                pitch = 116
                x = AG_W / 2 - (len(live) * pitch - 20) / 2
                y = AGB_BOT + 10
                for label, left, span, col in live:
                    c.text(label, x, y, size=12, color=col, bold=True,
                            kerning=1.5)
                    c.bar(x, y + 16, 96, 4, left / float(span), col)
                    x += pitch

            # Callouts flash inside the page, above the paddle.
            if self.note is not None:
                text, left, col = self.note
                c.text(text, AG_W / 2, AGB_PAD_Y - 48, size=20, color=col,
                        bold=True, kerning=2.0, anchor=(0.5, 0.5),
                        alpha=ag_clamp(left / 40.0, 0.0, 1.0))

            c.legend("ARROWS MOVE   //   Z SERVE + FIRE   //   "
                    "ESC PAUSE")

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
            return "ABANDONED" if kind == "quit" else "REVIEW ENDED"

        def card_accent(self, kind):
            if kind == "quit":
                return "#8f86a8"
            return "#4fbf7a" if self.sections_done >= 4 else "#e0455e"

        def rows(self, kind):
            return [
                ("SCORE", ag_num(self.score)),
                ("BEST", ag_num(max(self.score, ag_best("brick_score")))),
                ("SECTIONS CLEARED", str(self.sections_done)),
                ("CLAIMS DEMOLISHED", str(self.bricks_broken)),
                ("POWER-UPS TAKEN", str(self.powers_taken)),
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
        """Box art: a page of claims with one column already argued away."""
        parts = ag_cover_base(AGB_ACCENT)
        rows = ["1111", "12R1", "1C21", "1111"]
        for r, line in enumerate(rows):
            for col, ch in enumerate(line):
                spec = AGB_TYPES.get(ch)
                if spec is None:
                    continue
                parts.append(Transform(
                    Solid(spec[2], xysize=(56, 26)),
                    pos=(34 + col * 64, 40 + r * 34)))
        parts.append(Transform(Solid("#fdfbff", xysize=(14, 14)), pos=(196, 186)))
        parts.append(Transform(Solid("#d8d2e8", xysize=(76, 10)), pos=(150, 208)))
        parts += ag_cover_title("MANUSCRIPT", "PEER REVIEW", AGB_ACCENT)
        return Fixed(*parts, xysize=(AG_COVER_SIZE, AG_COVER_SIZE))


    ag_register(
        "brick", AGBrick,
        title="Peer Review",
        accent=AGB_ACCENT,
        blurb="Demolish a manuscript one claim at a time, on keys. Some claims "
                "are cited and come back, some are redacted and can't be argued "
                "with, and one of the five power-ups is a trap.",
        controls=AGBrick.CONTROLS,
        music=audio.tetris,
        cover=ag_brick_cover,
    )
