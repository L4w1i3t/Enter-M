# =============================================================================
# ag_snake.rpy  --  OUROBOROS PROTOCOL   (Arcade Original #1)
# =============================================================================
# A grid crawler, with the change that turns a nostalgia piece into a game about
# Matsuda's actual working habits: THE FOOD ROTS. Two more rules sit on top of
# that one -- THE SEAL and THE SPRINT, both below -- and the three together are
# what make this cabinet its own game rather than a reskin of the genre.
#
# THE TWIST
#   Every culture on the floor carries a timer. Reach it in the first half of
#   that timer and it is FRESH: the chain multiplier climbs, and the incinerator
#   eats the oldest spoiled tile on the floor. Reach it late and you still eat,
#   but the chain resets to one. Miss it entirely and it SPOILS where it sits --
#   a permanent hazard tile that kills on contact and never leaves on its own.
#   So the board is a running record of how tidy you have been. Play fast and
#   the lab stays clean; dawdle and you bury yourself in your own neglect. There
#   is no way to clear hazards except by being quick, which means the pressure
#   comes from the scoring system rather than from an artificial timer.
#
# WHY THAT WORKS AS A SCORE ATTACK
#   Classic snake's difficulty is entirely emergent (your own tail) and its risk
#   is entirely self-inflicted. Adding decay gives the player a SECOND, opposed
#   pressure: the tail says "take the safe long route", the timer says "take the
#   dangerous short one". Every sample is that argument, and the chain
#   multiplier pays for taking the dangerous side of it.
#
# SPEED
#   The snake speeds up per sample eaten (AGS_PERIOD_STEP), floored at
#   AGS_MIN_PERIOD -- about 17 cells a second, which is where a 32px grid stops
#   being readable. Speed is expressed as a PERIOD IN TICKS rather than a
#   cells-per-second rate so movement lands exactly on the 60Hz simulation grid
#   and never stutters between two frame counts.
#
# THE SEAL  (close a ring of body around the spoilage)
#   Rot is only permanent for a player who will not go back for it. Close a
#   loop of the specimen's own body around spoiled tiles and they are SEALED:
#   every hazard inside the ring burns off at once, and the pay grows with the
#   SQUARE of how many went together, so one patient ring around a bad corner
#   beats four hurried ones. The board edge is never part of a seal -- only the
#   body is -- so a seal is always something the player drew.
#
#   It is the counterweight to the rot. The incinerator rewards SPEED; the seal
#   rewards LENGTH and nerve, because a ring big enough to matter has to be
#   steered around the very tiles that kill on contact.
#
#   DETECTION is a flood from the rim. Every non-body cell reachable from the
#   board's edge by 8-connected steps is OUTSIDE; a hazard the flood never
#   reaches is inside a ring. The body is a 4-connected path, and a closed
#   4-connected curve always splits the grid into separate 8-connected pieces,
#   so a diagonal near-miss LEAKS and only a real closure counts -- which is
#   exactly the line a player can see. The flood is ~480 cells and only runs on
#   a move that could have closed something: spoilage on the floor, and the
#   head now touching its own body somewhere past the neck.
#
# THE SPRINT  (hold Shift)
#   Three things happen at once, and they are meant to be felt as one decision.
#
#   FASTER      the movement period is SCALED (x AGS_SPRINT_SCALE), not
#               replaced, so the sprint stays proportionally useful late, when
#               the base speed has already climbed.
#   CLUMSIER    the turn queue drops from two deep to one, AND a turn taken at
#               speed locks steering for one cell (the queued direction is kept,
#               it just lands late). Together: a sprint can be steered but not
#               zig-zagged, so threading a gap at speed is a genuine risk. Both
#               are deterministic and both are drawn -- the head wears a bar
#               while it will not corner -- so a sprint death is always legible.
#   BURNS       holding it accumulates heat, and every AGS_BURN_COST of heat
#               boils off a tail segment. The rate RAMPS with how long the key
#               has been held (AGS_BURN_RAMP), so a tap costs nearly nothing and
#               a long run eats the specimen. Below AGS_SPRINT_MIN_LEN there is
#               nothing left to spend and the sprint simply will not engage.
#
#   The burn only means something because LENGTH IS INCOME: a sample's base
#   value is 10 + length/AGS_LEN_BONUS, so the body you boil off to reach a
#   culture in time is body that was paying you on every sample after it.
#   Without that, burning length would be pure upside -- a shorter snake is an
#   easier snake -- and the sprint would have no cost at all, only a benefit.
#   THAT is the trade: spend future income to protect the chain now, or stay
#   long, stay rich, and watch a culture rot because you could not reach it.
#
# STRUCTURE
#   AGSnake is rules only (see ag_core.rpy for the AGGame/AGStage contract).
#   Everything it draws goes through the canvas' caches, and the whole board is
#   at most ~500 blits of about a dozen distinct textures.
# =============================================================================

init python:
    import math
    import random

    # --- board geometry ------------------------------------------------------
    # 30x16 cells of 32px = 960x512, centred with room for a HUD band above and
    # a control legend below.
    AGS_CELL = 32
    AGS_COLS = 30
    AGS_ROWS = 16
    AGS_W = AGS_CELL * AGS_COLS
    AGS_H = AGS_CELL * AGS_ROWS
    AGS_X = (AG_W - AGS_W) // 2
    AGS_Y = 148

    # --- tuning --------------------------------------------------------------
    AGS_ACCENT = "#57d6a8"          # culture-medium green
    AGS_START_PERIOD = 9.0          # ticks per cell at the start (~6.7 cells/s)
    AGS_MIN_PERIOD = 3.5            # the floor (~17 cells/s)
    AGS_PERIOD_STEP = 0.22          # shaved off per sample eaten
    AGS_TTL = 570                   # 9.5s before a culture spoils
    AGS_TTL_PRIORITY = 330          # 5.5s for the every-seventh gold sample
    AGS_FRESH = 0.5                 # grab inside this fraction of the timer = fresh
    AGS_CHAIN_MAX = 9
    AGS_GROW = 2                    # segments gained per sample
    AGS_READY = 96                  # hold before the first move (1.6s)
    AGS_DEATH = 108                 # death flourish before the results card
    AGS_HAZARD_CAP = 90             # hard ceiling; the floor is 480 cells

    # --- the sprint ----------------------------------------------------------
    # Hold Shift and the specimen runs hot: faster, clumsier, and boiling off
    # its own body to do it. See the SPRINT block in the file header.
    AGS_SPRINT_SCALE = 0.55         # movement period multiplier while sprinting
    AGS_SPRINT_FLOOR = 2.2          # absolute period floor (~27 cells/s)
    # The floor sits one below the starting length, so a player who presses
    # Shift in the first two seconds -- which every player does -- gets to feel
    # the sprint rather than a refusal message.
    AGS_SPRINT_MIN_LEN = 4          # below this it has nothing left to burn
    AGS_BURN_COST = 75.0            # heat needed to boil off one segment
    AGS_BURN_RAMP = 180.0           # ticks of held sprint that DOUBLE the rate
    AGS_COOL = 1.6                  # heat shed per tick once the key is up
    AGS_LEN_BONUS = 5               # +1 to a sample's base value per N segments

    # --- the seal ------------------------------------------------------------
    AGS_SEAL_VALUE = 25             # x (hazards sealed) squared
    AGS_SEAL_MIN_LEN = 8            # the smallest ring that has an inside
    AGS_SEAL_FX = 30                # ticks the sealed region glows

    def _ags_seal_tables():
        """Neighbour lists for the seal flood, built once: the 8-connected
        neighbours of every cell, and the rim cells the flood starts from."""
        neigh = []
        rim = []
        for i in range(AGS_COLS * AGS_ROWS):
            x = i % AGS_COLS
            y = i // AGS_COLS
            if x in (0, AGS_COLS - 1) or y in (0, AGS_ROWS - 1):
                rim.append(i)
            around = []
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx = x + dx
                    ny = y + dy
                    if ((dx or dy) and 0 <= nx < AGS_COLS
                            and 0 <= ny < AGS_ROWS):
                        around.append(ny * AGS_COLS + nx)
            neigh.append(tuple(around))
        return tuple(neigh), tuple(rim)

    AGS_NEIGH8, AGS_RIM = _ags_seal_tables()

    # Body gradient, quantized to 8 steps so a 120-segment snake still draws out
    # of 8 cached textures instead of 120.
    AGS_BODY_STEPS = 8
    AGS_HEAD_COL = "#9dffd8"
    AGS_TAIL_COL = "#1c6f57"


    class AGSnake(AGGame):
        """Ouroboros Protocol: a grid crawler with decaying food, body-ring
        seals and a sprint that spends length."""

        KIND = "snake"
        TITLE = "OUROBOROS PROTOCOL"
        ACCENT = AGS_ACCENT
        MOUSE = False
        CONTROLS = [
            ("ARROWS / WASD", "steer"),
            ("SHIFT  (hold)", "sprint -- faster, harder to turn, costs length"),
            ("CLOSE A LOOP", "clears any rot inside it"),
            ("ESC", "pause"),
            ("Q  (while paused)", "give up"),
        ]

        def __init__(self, variant=None):
            super(AGSnake, self).__init__(variant)

            # Seven long, mid-left, heading right: enough body that the
            # sprint is usable (and costly) from the first second.
            cy = AGS_ROWS // 2
            self.body = [[6 - i, cy] for i in range(7)]
            self.dir = (1, 0)
            self.turns = []             # queued direction changes (max 2)
            self.grow = 0

            self.move_period = AGS_START_PERIOD
            self.move_acc = 0.0
            self.ready = AGS_READY
            self.dying = 0

            self.sample = None
            self.hazards = []           # [[cx, cy, born_tick], ...]
            self.fx = []                # cosmetic sparks
            self.flash = 0              # screen-edge flash timer
            self.note = None            # (text, ticks_left, colour)

            # Sprint state. `heat` is the running cost of holding it: it climbs
            # while sprinting (faster the longer the key has been down), spends
            # itself a segment at a time, and bleeds away once you let go.
            self.sprinting = False
            self.sprint_ticks = 0
            self.sprint_total = 0
            self.heat = 0.0
            self.burned = 0
            self.turn_lock = 0          # cells to wait before another turn
            self.thin_warned = False

            self.chain = 1
            self.best_chain = 1
            self.eaten = 0
            self.spoiled = 0
            self.purged = 0

            # The seal: running totals, plus the region last sealed (cell
            # indices, ticks left) for its glow.
            self.sealed = 0
            self.best_seal = 0
            self.seals = 0
            self.seal_fx = None

            self._spawn_sample()

        # ---- helpers --------------------------------------------------------

        def _px(self, cx):
            return AGS_X + cx * AGS_CELL

        def _py(self, cy):
            return AGS_Y + cy * AGS_CELL

        def _occupied(self):
            cells = set((sx, sy) for sx, sy in self.body)
            for hx, hy, _born in self.hazards:
                cells.add((hx, hy))
            return cells

        def _spawn_sample(self):
            """Place the next culture on a free cell. Every seventh is a
            PRIORITY sample: triple value, but barely half the time to reach."""
            taken = self._occupied()
            free_count = AGS_COLS * AGS_ROWS - len(taken)
            if free_count <= 0:
                # The floor is genuinely full -- there is nowhere left to put a
                # sample, which is a win no one will ever see.
                self.finish("perfect")
                return

            # Rejection sampling is O(1) while the board is mostly empty (which
            # it is, for the whole of any realistic run); the scan is the exact
            # fallback for the pathological end state.
            spot = None
            for _attempt in range(60):
                cx = random.randrange(AGS_COLS)
                cy = random.randrange(AGS_ROWS)
                if (cx, cy) not in taken:
                    spot = (cx, cy)
                    break
            if spot is None:
                free = [(x, y)
                        for y in range(AGS_ROWS)
                        for x in range(AGS_COLS)
                        if (x, y) not in taken]
                if not free:
                    self.finish("perfect")
                    return
                spot = random.choice(free)

            priority = (self.eaten % 7) == 6
            self.sample = {
                "x": spot[0], "y": spot[1], "born": self.tick,
                "ttl": (AGS_TTL_PRIORITY if priority else AGS_TTL),
                "priority": priority,
            }

        def _spark(self, cx, cy, color, n=8, spread=1.6):
            for _i in range(n):
                ang = random.uniform(0.0, math.pi * 2.0)
                spd = random.uniform(0.35, 1.0) * spread
                self.fx.append({
                    "x": cx + 0.5, "y": cy + 0.5,
                    "vx": math.cos(ang) * spd * 0.08,
                    "vy": math.sin(ang) * spd * 0.08,
                    "life": 0, "ttl": random.randint(16, 30), "col": color,
                })

        def _say(self, text, color=None, ticks=70):
            self.note = [text, ticks, color or AGS_ACCENT]

        # ---- input ----------------------------------------------------------

        def _read_input(self, keys):
            """Edge-triggered steering, plus the held sprint key.

            The turn queue is the whole point of the steering: at seventeen
            cells a second a player entering a quick right-then-up around a
            corner would otherwise lose the second press, because both land
            inside the same movement step. Two is the right depth at normal
            speed -- one is not enough for a corner, three lets the player
            buffer a turn they can no longer see coming.

            SPRINTING TAKES THAT AWAY. The queue drops to one, so a corner has
            to be entered a press at a time; and see _advance for the other
            half, which is that a turn taken at speed locks out the next one
            for a cell. Neither is random -- both are the specimen being hard
            to steer when it is running, which is the whole trade.
            """
            if keys is None:
                self.sprinting = False
                return

            for name, codes, d in AGS_DIRS:
                if self.tapped(keys, name, *codes):
                    self._queue(d)

            want = self.held(keys, *AGS_SPRINT_KEYS)
            if want and len(self.body) <= AGS_SPRINT_MIN_LEN:
                # Nothing left to burn. Said once per press, not once a tick.
                if not self.thin_warned:
                    self.thin_warned = True
                    self._say("TOO SHORT TO SPRINT", "#ff9a4d", 50)
                    ag_se("ui_no", 0.5)
                want = False
            if not self.held(keys, *AGS_SPRINT_KEYS):
                self.thin_warned = False
            self.sprinting = bool(want) and not self.dying and self.ready <= 0

        def _queue(self, d):
            last = self.turns[-1] if self.turns else self.dir
            if d == last or (d[0] == -last[0] and d[1] == -last[1]):
                # Same direction is a no-op; a straight reversal would drive the
                # head into the neck, which reads as an input bug rather than a
                # mistake, so it is refused outright.
                return
            if len(self.turns) < (1 if self.sprinting else 2):
                self.turns.append(d)

        def _period(self):
            """Ticks per cell right now. Sprinting scales the current period
            rather than replacing it, so the sprint stays proportionally useful
            as the base speed climbs with every sample eaten."""
            if not self.sprinting:
                return self.move_period
            return max(AGS_SPRINT_FLOOR, self.move_period * AGS_SPRINT_SCALE)

        # ---- simulation -----------------------------------------------------

        def step(self):
            if self.result is not None:
                return

            keys = self.poll()
            self._read_input(keys)
            self._step_fx()

            if self.dying:
                self.dying += 1
                self.sprinting = False
                if self.dying > AGS_DEATH:
                    self.finish("over")
                return

            if self.ready > 0:
                self.ready -= 1
                return

            self._age_sample()
            self._step_sprint()

            self.move_acc += 1.0
            while self.move_acc >= self._period():
                self.move_acc -= self._period()
                self._advance()
                if self.dying or self.result is not None:
                    break

        def _step_sprint(self):
            """Charge (or shed) the sprint's heat, and boil off a segment each
            time it fills.

            The rate RAMPS: heat gains 1 per tick at the start of a sprint and
            2 per tick after AGS_BURN_RAMP ticks of holding it down, so a tap is
            nearly free and a long run eats the specimen alive. Letting go sheds
            heat quickly but does NOT give anything back -- burnt length is
            gone, which is what makes the decision to hold it one you have to
            keep making.
            """
            if self.sprinting:
                self.sprint_ticks += 1
                self.sprint_total += 1
                self.heat += 1.0 + self.sprint_ticks / AGS_BURN_RAMP
                while self.heat >= AGS_BURN_COST:
                    self.heat -= AGS_BURN_COST
                    if not self._burn_segment():
                        # Nothing left to give: the sprint cuts out on its own.
                        self.heat = 0.0
                        self.sprinting = False
                        self._say("TOO SHORT TO SPRINT", "#ff9a4d", 50)
                        break
            else:
                self.sprint_ticks = 0
                if self.heat > 0.0:
                    self.heat = max(0.0, self.heat - AGS_COOL)

        def _burn_segment(self):
            """Boil the tail segment off. False when the specimen is at its
            floor length and has nothing left to spend."""
            if len(self.body) <= AGS_SPRINT_MIN_LEN:
                return False
            tx, ty = self.body.pop()
            self.burned += 1
            self._spark(tx, ty, "#ff9a4d", n=5, spread=1.1)
            ag_se("burn", 0.45)
            return True

        def _step_fx(self):
            if self.flash > 0:
                self.flash -= 1
            if self.seal_fx is not None:
                self.seal_fx[1] -= 1
                if self.seal_fx[1] <= 0:
                    self.seal_fx = None
            if self.note is not None:
                self.note[1] -= 1
                if self.note[1] <= 0:
                    self.note = None
            if not self.fx:
                return
            alive = []
            for p in self.fx:
                p["life"] += 1
                if p["life"] >= p["ttl"]:
                    continue
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["vx"] *= 0.94
                p["vy"] *= 0.94
                alive.append(p)
            self.fx = alive

        def _age_sample(self):
            s = self.sample
            if s is None:
                self._spawn_sample()
                return
            if self.tick - s["born"] < s["ttl"]:
                return

            # Spoiled: it becomes a permanent hazard exactly where it sat.
            self.hazards.append([s["x"], s["y"], self.tick])
            if len(self.hazards) > AGS_HAZARD_CAP:
                self.hazards.pop(0)
            self.spoiled += 1
            self.chain = 1
            self._spark(s["x"], s["y"], "#c65cff", n=10)
            self._say("SPOILED", "#c65cff")
            ag_se("spoil")
            self.sample = None
            self._spawn_sample()

        def _advance(self):
            # HANDLING. A turn taken while sprinting locks steering for one
            # cell: the queued direction is NOT thrown away, it just lands a
            # cell later than asked. So a sprint can be steered, but it cannot
            # zig-zag -- consecutive turns need a cell of clearance between
            # them, and threading a gap at speed is a real risk rather than the
            # same input you would use walking. Deterministic, and visible in
            # the head's colour, so it is never a mystery death.
            if self.turn_lock > 0:
                self.turn_lock -= 1
            elif self.turns:
                self.dir = self.turns.pop(0)
                if self.sprinting:
                    self.turn_lock = 1

            hx = self.body[0][0] + self.dir[0]
            hy = self.body[0][1] + self.dir[1]

            if hx < 0 or hy < 0 or hx >= AGS_COLS or hy >= AGS_ROWS:
                self._die("HIT THE WALL")
                return

            # The tail cell is only a wall if the tail is NOT about to vacate it.
            # Growing means it stays put this step, so it counts.
            body_cells = set((sx, sy) for sx, sy in self.body)
            if self.grow <= 0 and len(self.body) > 1:
                body_cells.discard(tuple(self.body[-1]))
            if (hx, hy) in body_cells:
                self._die("HIT YOURSELF")
                return

            for haz in self.hazards:
                if haz[0] == hx and haz[1] == hy:
                    self._die("HIT THE ROT")
                    return

            self.body.insert(0, [hx, hy])
            if self.grow > 0:
                self.grow -= 1
            else:
                self.body.pop()

            s = self.sample
            if s is not None and s["x"] == hx and s["y"] == hy:
                self._eat(s)

            self._try_seal()

        def _eat(self, s):
            age = (self.tick - s["born"]) / float(max(1, s["ttl"]))
            fresh = age <= AGS_FRESH

            # LENGTH IS INCOME. A sample is worth more to a long specimen, which
            # is what puts a real price on the sprint: the body you boil off to
            # reach a culture in time is body that was paying you on every
            # sample after it. Without this, burning length would be pure
            # upside -- a shorter snake is an easier snake.
            base = 10 + len(self.body) // AGS_LEN_BONUS
            value = base * self.chain
            if s["priority"]:
                value *= 3

            self.grow += AGS_GROW + (1 if s["priority"] else 0)
            self.eaten += 1
            self.score += value

            purged = False
            if fresh:
                self.chain = min(AGS_CHAIN_MAX, self.chain + 1)
                self.best_chain = max(self.best_chain, self.chain)
                purged = self._incinerate()
            else:
                self.chain = 1

            self.move_period = max(
                AGS_MIN_PERIOD,
                AGS_START_PERIOD - AGS_PERIOD_STEP * self.eaten)

            self._spark(s["x"], s["y"],
                        "#ffd45e" if s["priority"] else AGS_HEAD_COL,
                        n=(14 if s["priority"] else 8))
            self.flash = 6
            # ONE callout, composed here rather than shouted by each system in
            # turn (the incinerator used to overwrite its own pickup message).
            # Showing the number is also how the length-is-income rule teaches
            # itself, without another readout on the HUD.
            if s["priority"]:
                ag_se("bonus")
                self._say("BONUS   +%d" % value, "#ffd45e", 55)
            elif purged:
                ag_se("burn")
                self._say("+%d   ROT CLEARED" % value, "#ff9a4d", 55)
            elif fresh and self.chain >= 4:
                ag_se("chain")
                self._say("+%d" % value, AGS_HEAD_COL, 45)
            else:
                ag_se("pickup")
                self._say("+%d" % value, AG_DIM, 40)

            self.sample = None
            self._spawn_sample()

        def _incinerate(self):
            """A fresh grab pays for one pass of the incinerator: the OLDEST
            hazard on the floor burns off. This is the only way the board is
            ever cleaned, and it is why chaining is worth the risk.

            Returns whether anything actually burned, so the caller can say so
            in the one pickup callout."""
            if not self.hazards:
                return False
            hx, hy, _born = self.hazards.pop(0)
            self.purged += 1
            self._spark(hx, hy, "#ff9a4d", n=12, spread=2.2)
            return True

        def _try_seal(self):
            """THE SEAL: burn off every hazard inside a closed ring of body.
            See the header for why the flood is 8-connected, and why it only
            runs once the head has touched its own body past the neck."""
            if not self.hazards or len(self.body) < AGS_SEAL_MIN_LEN:
                return
            hx, hy = self.body[0]
            for sx, sy in self.body[3:]:
                if abs(sx - hx) + abs(sy - hy) == 1:
                    break
            else:
                return

            cols = AGS_COLS
            size = cols * AGS_ROWS
            wall = bytearray(size)
            for sx, sy in self.body:
                wall[sy * cols + sx] = 1
            seen = bytearray(size)
            stack = []
            for i in AGS_RIM:
                if not wall[i]:
                    seen[i] = 1
                    stack.append(i)
            neigh = AGS_NEIGH8
            while stack:
                for j in neigh[stack.pop()]:
                    if not wall[j] and not seen[j]:
                        seen[j] = 1
                        stack.append(j)

            inside = [h for h in self.hazards if not seen[h[1] * cols + h[0]]]
            if not inside:
                return
            self.hazards = [h for h in self.hazards
                            if seen[h[1] * cols + h[0]]]

            n = len(inside)
            value = AGS_SEAL_VALUE * n * n
            self.score += value
            self.sealed += n
            self.purged += n
            self.seals += 1
            self.best_seal = max(self.best_seal, n)
            self.seal_fx = [[i for i in range(size)
                             if not wall[i] and not seen[i]], AGS_SEAL_FX]
            for zx, zy, _born in inside:
                self._spark(zx, zy, AGS_ACCENT, n=10, spread=2.0)
            self.flash = 12
            ag_se("bonus")
            ag_se("burn", 0.6)
            # Said after _eat's callout on purpose: a move that eats AND seals
            # reports the seal, which is the rarer and the bigger event.
            self._say("SEALED  x%d   +%d" % (n, value), AGS_HEAD_COL, 75)

        def _die(self, cause):
            if self.dying:
                return
            self.dying = 1
            self.death_cause = cause
            self.flash = 14
            head = self.body[0]
            self._spark(head[0], head[1], "#ff6b7f", n=20, spread=2.6)
            ag_se("die")
            ag_se("over", 0.8)

        # ---- drawing --------------------------------------------------------

        def draw(self, c):
            self._draw_board(c)
            self._draw_seal(c)
            self._draw_hazards(c)
            self._draw_sample(c)
            self._draw_body(c)
            self._draw_fx(c)
            self._draw_hud(c)

            if self.ready > 0:
                self._draw_ready(c)
            if self.dying:
                self._draw_death(c)

        def _draw_board(self, c):
            c.panel(AGS_X - 12, AGS_Y - 12, AGS_W + 24, AGS_H + 24,
                    top="#161038ea", bottom="#0b0720f2", radius=16,
                    border=1.5, bcolor=(AGS_ACCENT + "55"))
            c.rect("#00000055", AGS_X, AGS_Y, AGS_W, AGS_H)

            # Grid: one hairline per column/row. 46 blits of two textures.
            for cx in range(1, AGS_COLS):
                c.rect("#ffffff0b", self._px(cx), AGS_Y, 1, AGS_H)
            for cy in range(1, AGS_ROWS):
                c.rect("#ffffff0b", AGS_X, self._py(cy), AGS_W, 1)

            if self.flash > 0:
                a = int(ag_clamp(self.flash * 12, 0, 120))
                c.frame("%s%02x" % (AGS_ACCENT, a), AGS_X - 2, AGS_Y - 2,
                        AGS_W + 4, AGS_H + 4, 2)

        def _draw_seal(self, c):
            """The ring just closed: its whole inside washes bright and fades.
            Alpha is quantized to four steps, so fading a large region is still
            one cached texture per step."""
            if self.seal_fx is None:
                return
            cells, left = self.seal_fx
            step = int(ag_clamp(left / float(AGS_SEAL_FX), 0.0, 1.0) * 4 + 0.5)
            if step <= 0:
                return
            col = "%s%02x" % (AGS_ACCENT, 34 * step)
            for i in cells:
                c.rect(col, self._px(i % AGS_COLS) + 1,
                       self._py(i // AGS_COLS) + 1, AGS_CELL - 2, AGS_CELL - 2)

        def _draw_hazards(self, c):
            for hx, hy, born in self.hazards:
                age = self.tick - born
                # Fresh spoilage throbs for a second so the player sees where
                # the floor just got smaller.
                pulse = 0.5 + 0.5 * math.sin(age * 0.09)
                col = ag_mix("#3d1150", "#a03bd6", 0.35 + 0.35 * pulse)
                c.cell(self._px(hx), self._py(hy), AGS_CELL, col, inset=2)
                c.rect("#ffffff22", self._px(hx) + 12, self._py(hy) + 6, 8, 20)
                c.rect("#ffffff22", self._px(hx) + 6, self._py(hy) + 12, 20, 8)

        def _draw_sample(self, c):
            s = self.sample
            if s is None:
                return
            frac = ag_clamp((self.tick - s["born"]) / float(max(1, s["ttl"])),
                            0.0, 1.0)
            # Colour is the timer: mint while fresh, amber past the halfway
            # mark, red just before it spoils. The player never has to read a
            # number to know how long is left.
            if frac <= AGS_FRESH:
                col = ag_mix("#8affd0", "#ffe08a", frac / AGS_FRESH)
            else:
                col = ag_mix("#ffe08a", "#ff5c6e",
                            (frac - AGS_FRESH) / (1.0 - AGS_FRESH))
            if s["priority"]:
                col = ag_mix(col, "#ffd45e", 0.55)

            px = self._px(s["x"])
            py = self._py(s["y"])
            pulse = 0.5 + 0.5 * math.sin(self.tick * 0.14)
            grow = int(2 + 3 * pulse)

            c.rect(col + "33", px + 2, py + 2, AGS_CELL - 4, AGS_CELL - 4)
            inset = 8 - grow // 2
            c.cell(px, py, AGS_CELL, col, inset=inset, radius=6)

            # A shrinking pip under the sample: the last quarter of its life.
            if frac > 0.6:
                w = int((1.0 - frac) / 0.4 * (AGS_CELL - 8))
                c.rect("#ff5c6ecc", px + 4, py + AGS_CELL - 4, max(2, w), 2)

        def _draw_body(self, c):
            n = len(self.body)
            dying_flash = self.dying and (self.dying // 5) % 2 == 0
            # Running hot: the whole body is pulled toward ember, quantized to
            # the same 8 buckets so the sprint does not multiply the texture
            # cache. The tail end glows hardest -- that is the end being spent.
            hot = 0.0
            if self.sprinting:
                hot = 0.35 + 0.35 * (0.5 + 0.5 * math.sin(self.tick * 0.35))
            head_col = ag_mix(AGS_HEAD_COL, "#ffd45e", hot)
            tail_col = ag_mix(AGS_TAIL_COL, "#ff7a3d", hot)

            for i in range(n - 1, -1, -1):
                sx, sy = self.body[i]
                if dying_flash:
                    col = "#ffffff"
                else:
                    t = (i / float(max(1, n - 1)))
                    bucket = int(t * (AGS_BODY_STEPS - 1) + 0.5)
                    col = ag_mix(head_col, tail_col,
                                bucket / float(AGS_BODY_STEPS - 1))
                c.cell(self._px(sx), self._py(sy), AGS_CELL, col,
                        inset=(2 if i == 0 else 3), radius=(8 if i == 0 else 5))

            # Eyes, so the head reads as a front even when it fills the cell.
            hx, hy = self.body[0]
            ex = self._px(hx) + AGS_CELL // 2
            ey = self._py(hy) + AGS_CELL // 2
            dx, dy = self.dir
            fx = ex + dx * 7
            fy = ey + dy * 7
            ox, oy = (-dy * 6, dx * 6)
            for s in (1, -1):
                c.rect("#0b0720", fx + ox * s - 2, fy + oy * s - 2, 5, 5)

            # Steering lock: a bar across the head's nose while a turn is being
            # held off for a cell. The clumsiness is never a mystery -- you can
            # see the frame in which the specimen will not corner.
            if self.turn_lock > 0 and not self.dying:
                c.rect("#ff9a4dcc", ex + dx * 12 - (6 if dx else 9),
                        ey + dy * 12 - (9 if dx else 6),
                        (12 if dx else 18), (18 if dx else 12))

        def _draw_fx(self, c):
            for p in self.fx:
                t = p["life"] / float(p["ttl"])
                size = max(2, int(7 * (1.0 - t)))
                a = int(220 * (1.0 - t))
                c.rect("%s%02x" % (p["col"], a),
                        AGS_X + p["x"] * AGS_CELL - size / 2.0,
                        AGS_Y + p["y"] * AGS_CELL - size / 2.0,
                        size, size, sub=True)

        def _draw_hud(self, c):
            best = max(self.score, ag_best("snake_score"))

            chain_col = ag_mix(AGS_ACCENT, "#ffd45e",
                                (self.chain - 1) / float(AGS_CHAIN_MAX - 1))

            c.header("OUROBOROS PROTOCOL", "MATSUCOM",
                    AGS_ACCENT)
            # One row, right-aligned. ROT is what is on the board right now;
            # the rotted/cleared totals are on the results card.
            c.stat_row([
                ("ROT", str(len(self.hazards)),
                    ("#c65cff" if self.hazards else AG_FAINT)),
                # LENGTH carries what a sample is currently worth, because
                # length IS that number -- the sprint's cost is only legible if
                # you can see the income it is eating.
                ("LENGTH", "%d  (+%d)" % (len(self.body),
                    10 + len(self.body) // AGS_LEN_BONUS),
                    ("#ff9a4d" if self.sprinting else AG_DIM)),
                ("CHAIN", "x%d" % self.chain, chain_col),
                ("BEST", ag_num(best), AG_DIM),
                ("SCORE", ag_num(self.score), AG_INK),
            ])

            self._draw_heat(c)

            # Callouts (SPOILED / PURGED / PRIORITY) flash INSIDE the arena, at
            # the top edge, where the player is already looking -- not on a rail
            # underneath it that they would have to look away to read.
            if self.note is not None:
                text, left, col = self.note
                a = ag_clamp(left / 40.0, 0.0, 1.0)
                c.text(text, AG_W / 2, AGS_Y + 24, size=20, color=col,
                        bold=True, kerning=2.0, anchor=(0.5, 0.5), alpha=a)

            c.legend("ARROWS STEER   //   SHIFT SPRINT   //   LOOP AROUND ROT TO "
                    "CLEAR IT   //   ESC PAUSE   //   SPEED %d%%"
                    % int(round(AGS_START_PERIOD / self._period() * 100)))

        def _draw_heat(self, c):
            """The sprint gauge: how close the current run is to costing
            another segment. Drawn INSIDE the arena along its bottom edge, so
            it is in the same glance as the specimen, and only while it has
            something to say -- it fades out with the heat once the key is up.
            """
            if self.heat <= 0.0 and not self.sprinting:
                return
            frac = ag_clamp(self.heat / AGS_BURN_COST, 0.0, 1.0)
            w = 260
            x = AG_W / 2 - w / 2
            y = AGS_Y + AGS_H - 12
            col = ag_mix("#ffd45e", "#ff5c6e", frac)
            alpha = 1.0 if self.sprinting else ag_clamp(frac * 2.0, 0.0, 1.0)
            back = "#ffffff%02x" % int(20 * alpha)
            c.rect(back, x, y, w, 4)
            c.rect("%s%02x" % (col, int(230 * alpha)), x, y,
                    max(2, int(w * frac)), 4)
            if self.sprinting:
                c.text("SPRINT", x - 12, y - 5, size=11, color=col, bold=True,
                        kerning=2.0, anchor=(1.0, 0.0))
                c.text("-%d" % self.burned, x + w + 12, y - 5, size=11,
                        color="#ff9a4d", bold=True, kerning=1.0)

        def _draw_ready(self, c):
            pulse = 0.55 + 0.45 * math.sin(self.tick * 0.16)
            c.text("READY", AG_W / 2, AGS_Y + AGS_H / 2 - 16,
                    size=44, color=AG_INK, font=AG_FONT, bold=True,
                    anchor=(0.5, 0.5), alpha=pulse)
            c.text("eat samples before they rot", AG_W / 2,
                    AGS_Y + AGS_H / 2 + 26, size=16, color=AGS_ACCENT,
                    anchor=(0.5, 0.5), alpha=pulse)

        def _draw_death(self, c):
            a = ag_clamp(self.dying / 24.0, 0.0, 1.0)
            c.rect("#12040c%02x" % int(150 * a), 0, 0, AG_W, AG_H)
            c.text("GAME OVER", AG_W / 2, AG_H / 2 - 18, size=48,
                    color="#ff6b7f", font=AG_FONT, bold=True,
                    anchor=(0.5, 0.5), alpha=a)
            c.text(getattr(self, "death_cause", "-"), AG_W / 2, AG_H / 2 + 26,
                    size=16, color=AG_DIM, kerning=3.0, anchor=(0.5, 0.5),
                    alpha=a)

        # ---- results --------------------------------------------------------

        def record(self):
            self.new_record = ag_set_best("snake_score", self.score)
            ag_set_best("snake_length", len(self.body))
            ag_set_best("snake_seal", self.best_seal)

        def outcome(self, kind):
            if kind == "quit":
                return "ABANDONED"
            if kind == "perfect":
                return "BOARD FULL"
            return "GAME OVER"

        def card_accent(self, kind):
            if kind == "quit":
                return "#8f86a8"
            if kind == "perfect":
                return "#ffd45e"
            return "#e0455e"

        def rows(self, kind):
            return [
                ("SCORE", ag_num(self.score)),
                ("BEST", ag_num(max(self.score, ag_best("snake_score")))),
                ("SAMPLES EATEN", str(self.eaten)),
                ("LONGEST CHAIN", "x%d" % self.best_chain),
                ("ROTTED / CLEARED", "%d / %d" % (self.spoiled, self.purged)),
                ("SEALED  (BIGGEST LOOP)", "%d  (%d)"
                    % (self.sealed, self.best_seal)),
                ("LENGTH BURNED SPRINTING", "%d  (%s)"
                    % (self.burned, ag_time(self.sprint_total / 60.0))),
            ]


    # Steering table. Both arrow keys and WASD, edge-triggered under one name
    # per direction so holding W and Up together is still one press.
    try:
        import pygame_sdl2 as _ags_pg
        AGS_DIRS = [
            ("up", (_ags_pg.K_UP, _ags_pg.K_w), (0, -1)),
            ("down", (_ags_pg.K_DOWN, _ags_pg.K_s), (0, 1)),
            ("left", (_ags_pg.K_LEFT, _ags_pg.K_a), (-1, 0)),
            ("right", (_ags_pg.K_RIGHT, _ags_pg.K_d), (1, 0)),
        ]
        AGS_SPRINT_KEYS = (_ags_pg.K_LSHIFT, _ags_pg.K_RSHIFT)
    except Exception:
        AGS_DIRS = []
        AGS_SPRINT_KEYS = ()


    def ag_snake_cover():
        """Box art: a closed ring of body segments -- the snake that has caught
        its own tail -- around a single bright culture."""
        parts = ag_cover_base(AGS_ACCENT)
        ring = ([(x, 0) for x in range(5)] + [(4, y) for y in range(1, 5)]
                + [(x, 4) for x in range(3, -1, -1)]
                + [(0, y) for y in range(3, 0, -1)])
        for i, (cx, cy) in enumerate(ring):
            col = ag_mix(AGS_HEAD_COL, AGS_TAIL_COL, i / float(len(ring)))
            parts.append(Transform(Solid(col, xysize=(30, 30)),
                                    pos=(46 + cx * 40, 30 + cy * 40)))
        parts.append(Transform(Solid("#ffe08a", xysize=(22, 22)),
                                pos=(130, 114)))
        parts += ag_cover_title("GRID SURVIVAL", "OUROBOROS PROTOCOL",
                                AGS_ACCENT)
        return Fixed(*parts, xysize=(AG_COVER_SIZE, AG_COVER_SIZE))


    ag_register(
        "snake", AGSnake,
        title="Ouroboros Protocol",
        accent=AGS_ACCENT,
        blurb="Samples rot where they sit. Eat them fresh to keep your "
                "chain going, loop your body around rot to clear it, and hold "
                "Shift to sprint -- faster, harder to turn, and it costs "
                "length.",
        controls=AGSnake.CONTROLS,
        music=audio.tetris,
        cover=ag_snake_cover,
    )
