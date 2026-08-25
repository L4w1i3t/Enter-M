# =============================================================================
# ag_intake.rpy  --  INTAKE   (Arcade Original #3)
# =============================================================================
# Falling blocks, played as a night shift. Samples arrive from the chute, you
# rack them in cold storage, and a full shelf gets processed and taken away.
# Matsuda does not stop sending samples because you are behind.
#
# THE TWIST: CONTAMINATION
#   Every so often the intake pushes a row up from the BOTTOM -- a batch that
#   arrived unsorted, with a single gap in it. It is telegraphed by a hazard
#   stripe two seconds ahead, so it is a problem to solve rather than a hand
#   slapping the board. It does three things at once that ordinary garbage in
#   this genre does: it raises the stack (pressure), it puts a hole somewhere
#   you did not choose (planning), and it arrives FASTER as the level climbs, so
#   the late game is about keeping a low, clean stack you can afford to lose the
#   bottom of. The stack you build for a long game is a different shape from the
#   one you would build without it, which is the whole reason the twist is here.
#
# WHAT IS STANDARD (deliberately -- muscle memory should transfer)
#   7-bag randomiser, SRS rotation states with the standard wall/floor kick
#   tables, hold (once per piece), ghost piece, DAS/ARR horizontal repeat, lock
#   delay with a reset cap, soft and hard drop, and the usual 100/300/500/800
#   line values scaled by level plus a combo bonus. Anyone who has played the
#   genre can sit down and play this immediately; the contamination is the only
#   thing they have to learn.
#
# THE HIDDEN ROWS
#   The grid is AGI_H rows tall and only the bottom AGI_VIS are drawn. The two
#   hidden rows at the top are the spawn box: a piece materialises there and
#   only enters the visible field as it falls. Topping out is defined as a piece
#   that cannot fit in that box -- the standard rule, and the reason a stack can
#   touch the ceiling without ending the run instantly.
# =============================================================================

init python:
    import math
    import random

    # --- board ---------------------------------------------------------------
    AGI_W = 10                  # columns
    AGI_H = 22                  # rows including the hidden spawn box
    AGI_VIS = 20                # rows actually drawn
    AGI_CELL = 28
    AGI_BX = (AG_W - AGI_W * AGI_CELL) // 2
    # Under the header band (which ends near 80) and clear of the control
    # legend at 696: 100 + 20 rows * 28 = 660.
    AGI_BY = 100
    AGI_ACCENT = "#5ec8e0"

    # --- feel ----------------------------------------------------------------
    AGI_DAS = 14                # ticks held before a direction auto-repeats
    AGI_ARR = 3                 # ticks between auto-repeats
    AGI_SOFT = 2                # ticks per cell while soft dropping
    AGI_LOCK = 30               # lock delay
    AGI_LOCK_RESETS = 15        # how many times movement may refresh it
    AGI_CLEAR_TIME = 22         # line-clear flash before the rows are removed
    AGI_LINES_PER_LEVEL = 10
    AGI_GARBAGE_WARN = 120      # 2s of hazard stripe before a row rises

    # --- pieces --------------------------------------------------------------
    # Cells are (x, y) inside the piece's box, y DOWN, in the four SRS rotation
    # states (spawn, right, two, left). Written out in full rather than rotated
    # at runtime: the tables are the specification, and a rotation function that
    # is subtly wrong is much harder to see than a wrong coordinate.
    AGI_SHAPES = {
        "I": [
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(2, 0), (2, 1), (2, 2), (2, 3)],
            [(0, 2), (1, 2), (2, 2), (3, 2)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
        ],
        "J": [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (0, 2), (1, 2)],
        ],
        "L": [
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
        ],
        "O": [
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
        ],
        "S": [
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(1, 0), (1, 1), (2, 1), (2, 2)],
            [(1, 1), (2, 1), (0, 2), (1, 2)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
        ],
        "T": [
            [(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
        ],
        "Z": [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(2, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (1, 2), (2, 2)],
            [(1, 0), (0, 1), (1, 1), (0, 2)],
        ],
    }

    AGI_COLORS = {
        "I": "#5ec8e0", "J": "#5a6fd6", "L": "#e08a4f", "O": "#e0c05e",
        "S": "#4fbf7a", "T": "#b57ae0", "Z": "#e0455e", "#": "#6a6284",
    }

    # Standard SRS kick tables, keyed (from_state, to_state). Offsets are in SRS
    # convention (y UP); the rotation code negates y for this board's downward
    # axis. The first entry of every list is the no-kick attempt.
    AGI_KICKS_JLSTZ = {
        (0, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
        (1, 0): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
        (1, 2): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
        (2, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
        (2, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
        (3, 2): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
        (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
        (0, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    }
    AGI_KICKS_I = {
        (0, 1): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
        (1, 0): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
        (1, 2): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
        (2, 1): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
        (2, 3): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
        (3, 2): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
        (3, 0): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
        (0, 3): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    }

    AGI_LINE_SCORE = {1: 100, 2: 300, 3: 500, 4: 800}
    AGI_LINE_NAME = {1: "PROCESSED", 2: "DOUBLE BATCH", 3: "TRIPLE BATCH",
                    4: "FULL INTAKE"}


    class AGIntake(AGGame):
        """Intake: a stacker where the backlog pushes back."""

        KIND = "intake"
        TITLE = "INTAKE"
        ACCENT = AGI_ACCENT
        MOUSE = False
        CONTROLS = [
            ("LEFT / RIGHT", "shift the sample"),
            ("UP  or  X", "rotate clockwise"),
            ("Z", "rotate counter-clockwise"),
            ("DOWN", "soft drop"),
            ("SPACE", "hard drop"),
            ("C  or  SHIFT", "hold"),
            ("ESC", "pause  //  Q while paused gives up"),
        ]

        def __init__(self, variant=None):
            super(AGIntake, self).__init__(variant)

            self.grid = [[None] * AGI_W for _row in range(AGI_H)]
            self.bag = []
            self.queue = [self._next_kind() for _i in range(3)]
            self.piece = None
            self.hold = None
            self.hold_used = False

            self.level = 1
            self.lines = 0
            self.combo = -1
            self.b2b = False
            self.pieces_placed = 0

            self.grav_acc = 0
            self.lock_timer = 0
            self.lock_resets = 0
            self.das_dir = 0
            self.das_timer = 0
            self.soft_timer = 0

            self.clear_rows = []
            self.clear_timer = 0
            self.garbage_at = self._garbage_interval()
            self.garbage_warn = 0
            self.garbage_taken = 0
            self.note = None
            self.shake = 0
            self.over = 0

            self._spawn()

        # ---- randomiser -----------------------------------------------------

        def _next_kind(self):
            """7-bag: every seven pieces contains each shape exactly once, which
            is what stops the long droughts a pure random source produces."""
            if not self.bag:
                self.bag = list("IJLOSTZ")
                random.shuffle(self.bag)
            return self.bag.pop()

        def _garbage_interval(self):
            # Pieces between contamination rows. Tightens with the level and
            # bottoms out at 12 -- roughly one row every 45 seconds at speed.
            return max(12, 26 - self.level)

        # ---- board ----------------------------------------------------------

        def _cells(self, kind, rot, px, py):
            return [(px + cx, py + cy) for cx, cy in AGI_SHAPES[kind][rot]]

        def _fits(self, kind, rot, px, py):
            for x, y in self._cells(kind, rot, px, py):
                if x < 0 or x >= AGI_W or y >= AGI_H:
                    return False
                if y >= 0 and self.grid[y][x] is not None:
                    return False
            return True

        def _spawn(self):
            kind = self.queue.pop(0)
            self.queue.append(self._next_kind())
            self._spawn_kind(kind)

        def _spawn_kind(self, kind):
            self.piece = {"kind": kind, "rot": 0, "x": 3, "y": 0}
            self.grav_acc = 0
            self.lock_timer = 0
            self.lock_resets = 0
            self.hold_used = False
            if not self._fits(kind, 0, 3, 0):
                self._top_out()

        def _top_out(self):
            self.piece = None
            self.over = 1
            self.shake = 26
            ag_se("over")

        def _ghost_y(self):
            p = self.piece
            y = p["y"]
            while self._fits(p["kind"], p["rot"], p["x"], y + 1):
                y += 1
            return y

        # ---- input ----------------------------------------------------------

        def _read_input(self, keys):
            if keys is None:
                self.das_dir = 0
                return

            # Horizontal: DAS/ARR. Tapping moves once; holding waits AGI_DAS
            # then repeats every AGI_ARR, which is the standard feel and the
            # reason a long slide across the board is one held key.
            left = self.held(keys, AGI_K_LEFT)
            right = self.held(keys, AGI_K_RIGHT)
            direction = (-1 if left else 0) + (1 if right else 0)
            if direction == 0:
                self.das_dir = 0
                self.das_timer = 0
            elif direction != self.das_dir:
                self.das_dir = direction
                self.das_timer = 0
                self._shift(direction)
            else:
                self.das_timer += 1
                if self.das_timer >= AGI_DAS:
                    if (self.das_timer - AGI_DAS) % AGI_ARR == 0:
                        self._shift(direction)

            if self.tapped(keys, "cw", AGI_K_CW1, AGI_K_CW2):
                self._rotate(1)
            if self.tapped(keys, "ccw", AGI_K_CCW):
                self._rotate(-1)
            if self.tapped(keys, "hard", AGI_K_HARD):
                self._hard_drop()
            if self.tapped(keys, "hold", AGI_K_HOLD1, AGI_K_HOLD2, AGI_K_HOLD3):
                self._do_hold()

            if self.held(keys, AGI_K_DOWN):
                self.soft_timer += 1
                if self.soft_timer >= AGI_SOFT:
                    self.soft_timer = 0
                    if self._drop_one():
                        self.score += 1
            else:
                self.soft_timer = AGI_SOFT      # first press drops immediately

        def _shift(self, dx):
            p = self.piece
            if p is None:
                return
            if self._fits(p["kind"], p["rot"], p["x"] + dx, p["y"]):
                p["x"] += dx
                self._touch()
                ag_se("ui_move", 0.35)

        def _rotate(self, dr):
            p = self.piece
            if p is None:
                return
            frm = p["rot"]
            to = (frm + dr) % 4
            table = AGI_KICKS_I if p["kind"] == "I" else AGI_KICKS_JLSTZ
            for kx, ky in table.get((frm, to), [(0, 0)]):
                # SRS kick offsets are written with y pointing UP.
                nx = p["x"] + kx
                ny = p["y"] - ky
                if self._fits(p["kind"], to, nx, ny):
                    p["rot"] = to
                    p["x"] = nx
                    p["y"] = ny
                    self._touch()
                    ag_se("rotate")
                    return
            ag_se("deny", 0.4)

        def _touch(self):
            """A successful move refreshes the lock delay -- but only so many
            times, or a piece could be spun on top of the stack forever."""
            if self.lock_timer and self.lock_resets < AGI_LOCK_RESETS:
                self.lock_timer = 0
                self.lock_resets += 1

        def _do_hold(self):
            if self.piece is None or self.hold_used:
                if self.hold_used:
                    ag_se("deny", 0.4)
                return
            kind = self.piece["kind"]
            swap = self.hold
            self.hold = kind
            if swap is None:
                self._spawn()
            else:
                self._spawn_kind(swap)
            self.hold_used = True
            ag_se("ui_ok", 0.5)

        def _drop_one(self):
            p = self.piece
            if p is None:
                return False
            if self._fits(p["kind"], p["rot"], p["x"], p["y"] + 1):
                p["y"] += 1
                self.lock_timer = 0
                return True
            return False

        def _hard_drop(self):
            p = self.piece
            if p is None:
                return
            target = self._ghost_y()
            self.score += 2 * (target - p["y"])
            p["y"] = target
            self.shake = 5
            self._lock()

        # ---- simulation -----------------------------------------------------

        def step(self):
            if self.result is not None:
                return

            keys = self.poll()

            if self.note is not None:
                self.note[1] -= 1
                if self.note[1] <= 0:
                    self.note = None
            if self.shake > 0:
                self.shake -= 1

            if self.over:
                self.over += 1
                if self.over > 130:
                    self.finish("over")
                return

            # Line-clear pause: the board is frozen while the rows flash.
            if self.clear_timer:
                self.clear_timer -= 1
                if self.clear_timer == 0:
                    self._collapse()
                return

            self._read_input(keys)
            if self.piece is None:
                return

            # Gravity. _drop_one clears the lock timer whenever it actually
            # moves, so a piece sliding along the floor keeps its full delay.
            self.grav_acc += 1
            if self.grav_acc >= self._gravity():
                self.grav_acc = 0
                self._drop_one()

            # Resting on the stack: count down to lock.
            if not self._fits(self.piece["kind"], self.piece["rot"],
                                self.piece["x"], self.piece["y"] + 1):
                self.lock_timer += 1
                if self.lock_timer >= AGI_LOCK:
                    self._lock()
            else:
                self.lock_timer = 0

            # Contamination warning / arrival.
            if self.garbage_warn:
                self.garbage_warn -= 1
                if self.garbage_warn == 0:
                    self._push_garbage()

        def _gravity(self):
            """Ticks per cell of natural fall. Geometric per level, floored at
            two ticks -- past that the piece is faster than a human reaction and
            the game is decided by the queue rather than the player."""
            return max(2, int(round(48.0 * (0.79 ** (self.level - 1)))))

        def _lock(self):
            p = self.piece
            if p is None:
                return
            for x, y in self._cells(p["kind"], p["rot"], p["x"], p["y"]):
                if 0 <= y < AGI_H and 0 <= x < AGI_W:
                    self.grid[y][x] = p["kind"]
            self.piece = None
            self.pieces_placed += 1
            ag_se("lock")

            full = [y for y in range(AGI_H) if all(self.grid[y])]
            if full:
                self.clear_rows = full
                self.clear_timer = AGI_CLEAR_TIME
                ag_se("quad" if len(full) >= 4 else "line")
                return

            self.combo = -1
            self._after_piece()

        def _collapse(self):
            n = len(self.clear_rows)
            for y in sorted(self.clear_rows):
                del self.grid[y]
                self.grid.insert(0, [None] * AGI_W)
            self.clear_rows = []
            self.lines += n

            self.combo += 1
            gain = AGI_LINE_SCORE.get(n, 0) * self.level
            if n == 4 and self.b2b:
                # Back-to-back full intakes are worth half again -- the standard
                # reward for holding out for the big clear.
                gain = int(gain * 1.5)
            if self.combo > 0:
                gain += 50 * self.combo * self.level
            self.score += gain
            self.b2b = (n == 4)

            label = AGI_LINE_NAME.get(n, "PROCESSED")
            if self.combo > 0:
                label += "   x%d CHAIN" % (self.combo + 1)
            self._say(label, AGI_ACCENT)

            level = 1 + self.lines // AGI_LINES_PER_LEVEL
            if level > self.level:
                self.level = level
                self._say("SHIFT %d" % self.level, "#ffd45e")
                ag_se("level")

            self._after_piece()

        def _after_piece(self):
            """Between pieces: schedule contamination, then bring the next one
            in. Sequencing matters -- the warning has to be able to start before
            the player commits the next piece."""
            if (self.pieces_placed >= self.garbage_at
                    and not self.garbage_warn):
                self.garbage_warn = AGI_GARBAGE_WARN
                self.garbage_at = self.pieces_placed + self._garbage_interval()
                ag_se("rise", 0.6)
                self._say("INTAKE INBOUND", "#e0455e", 110)
            self._spawn()

        def _push_garbage(self):
            hole = random.randrange(AGI_W)
            row = ["#"] * AGI_W
            row[hole] = None
            # Everything shifts up one; anything already in the top hidden row
            # has nowhere to go, which is a top-out.
            top = self.grid.pop(0)
            self.grid.append(row)
            if any(cell is not None for cell in top):
                self._top_out()
                return
            self.garbage_taken += 1
            self.shake = 12
            ag_se("boom", 0.5)
            # The live piece may now be inside the stack; lift it if it can go.
            p = self.piece
            if p is not None and not self._fits(p["kind"], p["rot"], p["x"], p["y"]):
                if self._fits(p["kind"], p["rot"], p["x"], p["y"] - 1):
                    p["y"] -= 1
                else:
                    self._top_out()

        def _say(self, text, color=None, ticks=90):
            self.note = [text, ticks, color or AGI_ACCENT]

        # ---- drawing --------------------------------------------------------

        def _cell_xy(self, x, y):
            # Row AGI_H - AGI_VIS is the first visible one.
            return (AGI_BX + x * AGI_CELL,
                    AGI_BY + (y - (AGI_H - AGI_VIS)) * AGI_CELL)

        def draw(self, c):
            shake = 0
            if self.shake:
                shake = int(math.sin(self.tick * 1.7) * min(6, self.shake))

            self._draw_well(c, shake)
            self._draw_stack(c, shake)
            self._draw_piece(c, shake)
            self._draw_side(c)
            self._draw_hud(c)

            if self.over:
                a = ag_clamp(self.over / 24.0, 0.0, 1.0)
                c.rect("#12040c%02x" % int(160 * a), 0, 0, AG_W, AG_H)
                c.text("STORAGE FULL", AG_W / 2, AG_H / 2 - 16, size=50,
                        color="#e0455e", font=AG_FONT, bold=True,
                        anchor=(0.5, 0.5), alpha=a)
                c.text("the samples kept coming", AG_W / 2, AG_H / 2 + 30,
                        size=16, color=AG_DIM, anchor=(0.5, 0.5), alpha=a)

        def _draw_well(self, c, shake):
            x = AGI_BX + shake
            w = AGI_W * AGI_CELL
            h = AGI_VIS * AGI_CELL
            c.panel(x - 12, AGI_BY - 12, w + 24, h + 24, top="#161038ea",
                    bottom="#0b0720f2", radius=14, border=1.5,
                    bcolor=(AGI_ACCENT + "55"))
            c.rect("#00000055", x, AGI_BY, w, h)
            for col in range(1, AGI_W):
                c.rect("#ffffff0a", x + col * AGI_CELL, AGI_BY, 1, h)
            for row in range(1, AGI_VIS):
                c.rect("#ffffff0a", x, AGI_BY + row * AGI_CELL, w, 1)

            # Contamination warning: a hazard stripe under the well.
            if self.garbage_warn:
                pulse = 0.4 + 0.6 * abs(math.sin(self.tick * 0.2))
                c.rect("#e0455e%02x" % int(150 * pulse), x, AGI_BY + h + 2,
                        w, 5)

        def _draw_stack(self, c, shake):
            flash = bool(self.clear_timer and (self.clear_timer // 3) % 2)
            for y in range(AGI_H - AGI_VIS, AGI_H):
                row_clearing = y in self.clear_rows
                for x in range(AGI_W):
                    kind = self.grid[y][x]
                    if kind is None:
                        continue
                    cx, cy = self._cell_xy(x, y)
                    col = AGI_COLORS.get(kind, "#8f86a8")
                    if row_clearing:
                        col = "#ffffff" if flash else ag_mix(col, "#ffffff", 0.6)
                    self._block(c, cx + shake, cy, col)

        def _draw_piece(self, c, shake):
            p = self.piece
            if p is None:
                return
            col = AGI_COLORS[p["kind"]]

            # Ghost first, so the real piece draws over it.
            gy = self._ghost_y()
            if gy != p["y"]:
                for x, y in self._cells(p["kind"], p["rot"], p["x"], gy):
                    if y < AGI_H - AGI_VIS:
                        continue
                    cx, cy = self._cell_xy(x, y)
                    c.frame(col + "55", cx + shake + 2, cy + 2,
                            AGI_CELL - 4, AGI_CELL - 4, 2)

            # A piece about to lock brightens, so "it is going to set NOW" is
            # visible rather than something you learn by losing.
            settle = ag_clamp(self.lock_timer / float(AGI_LOCK), 0.0, 1.0)
            face = ag_mix(col, "#ffffff", 0.45 * settle)
            for x, y in self._cells(p["kind"], p["rot"], p["x"], p["y"]):
                if y < AGI_H - AGI_VIS:
                    continue
                cx, cy = self._cell_xy(x, y)
                self._block(c, cx + shake, cy, face)

        def _block(self, c, x, y, col):
            c.rect(ag_mix(col, "#0b0720", 0.45), x, y, AGI_CELL, AGI_CELL)
            c.rect(col, x + 2, y + 2, AGI_CELL - 4, AGI_CELL - 4)
            c.rect(ag_mix(col, "#ffffff", 0.45), x + 2, y + 2, AGI_CELL - 4, 3)

        def _draw_side(self, c):
            # HOLD, left of the well.
            hx = AGI_BX - 168
            c.panel(hx, AGI_BY, 140, 120, top="#1b1440e0", bottom="#0f0a26ee",
                    radius=12, border=1.0, bcolor="#ffffff18")
            c.text("HOLD", hx + 14, AGI_BY + 12, size=12, color=AG_FAINT,
                    bold=True, kerning=2.0)
            if self.hold:
                self._draw_mini(c, self.hold, hx + 70, AGI_BY + 74,
                                dim=self.hold_used)

            # NEXT, right of the well.
            nx = AGI_BX + AGI_W * AGI_CELL + 28
            c.panel(nx, AGI_BY, 140, 300, top="#1b1440e0", bottom="#0f0a26ee",
                    radius=12, border=1.0, bcolor="#ffffff18")
            c.text("NEXT", nx + 14, AGI_BY + 12, size=12, color=AG_FAINT,
                    bold=True, kerning=2.0)
            for i, kind in enumerate(self.queue[:3]):
                self._draw_mini(c, kind, nx + 70, AGI_BY + 74 + i * 84,
                                scale=(1.0 if i == 0 else 0.78))

        def _draw_mini(self, c, kind, cx, cy, scale=1.0, dim=False):
            """Draw a piece centred on (cx, cy) at a smaller cell size."""
            size = int(AGI_CELL * 0.62 * scale)
            cells = AGI_SHAPES[kind][0]
            xs = [p[0] for p in cells]
            ys = [p[1] for p in cells]
            w = (max(xs) - min(xs) + 1) * size
            h = (max(ys) - min(ys) + 1) * size
            ox = cx - w / 2.0 - min(xs) * size
            oy = cy - h / 2.0 - min(ys) * size
            col = AGI_COLORS[kind]
            if dim:
                col = ag_mix(col, "#3a3350", 0.62)
            for px, py in cells:
                x = ox + px * size
                y = oy + py * size
                c.rect(ag_mix(col, "#0b0720", 0.45), x, y, size, size)
                c.rect(col, x + 2, y + 2, size - 4, size - 4)

        def _draw_hud(self, c):
            c.header("INTAKE", "MATSUCOM  //  COLD STORAGE", AGI_ACCENT)
            c.stat_row([
                ("SHELVES", str(self.lines), AG_DIM),
                ("SHIFT", str(self.level), AG_INK),
                ("BEST", ag_num(max(self.score, ag_best("intake_score"))),
                    AG_DIM),
                ("SCORE", ag_num(self.score), AG_INK),
            ])

            # Contamination status sits under the HOLD plate -- beside the
            # board it is about to change, not stranded in a column of its own
            # halfway across the screen.
            hx = AGI_BX - 168
            y = AGI_BY + 140
            nxt = max(0, self.garbage_at - self.pieces_placed)
            warn = bool(self.garbage_warn)
            c.text("CONTAMINATION", hx, y, size=12,
                    color=("#e0455e" if warn else AG_FAINT), bold=True,
                    kerning=2.0)
            c.text("%d absorbed" % self.garbage_taken, hx, y + 20, size=14,
                    color=AG_DIM)
            c.text(("inbound now" if warn else "next batch in %d" % nxt),
                    hx, y + 40, size=14,
                    color=("#e0455e" if warn else AG_FAINT))

            # Line-clear callouts land INSIDE the well, over the rows that just
            # went. At the foot of the screen they were competing with the
            # control legend for the same twenty pixels.
            if self.note is not None:
                text, left, col = self.note
                c.text(text, AGI_BX + AGI_W * AGI_CELL / 2, AGI_BY + 40,
                        size=20, color=col, bold=True, kerning=2.0,
                        anchor=(0.5, 0.5),
                        alpha=ag_clamp(left / 40.0, 0.0, 1.0))

            c.legend("ARROWS MOVE  //  X / Z ROTATE  //  SPACE DROP  //  "
                    "C HOLD  //  ESC PAUSE")

        # ---- results --------------------------------------------------------

        def record(self):
            self.new_record = ag_set_best("intake_score", self.score)
            ag_set_best("intake_lines", self.lines)

        def outcome(self, kind):
            return "ABANDONED" if kind == "quit" else "STORAGE FULL"

        def card_accent(self, kind):
            return "#8f86a8" if kind == "quit" else "#e0455e"

        def rows(self, kind):
            return [
                ("SCORE", ag_num(self.score)),
                ("BEST", ag_num(max(self.score, ag_best("intake_score")))),
                ("SHELVES PROCESSED", str(self.lines)),
                ("SHIFT REACHED", str(self.level)),
                ("CONTAMINATION ABSORBED", str(self.garbage_taken)),
            ]


    try:
        import pygame_sdl2 as _agi_pg
        AGI_K_LEFT = _agi_pg.K_LEFT
        AGI_K_RIGHT = _agi_pg.K_RIGHT
        AGI_K_DOWN = _agi_pg.K_DOWN
        AGI_K_CW1, AGI_K_CW2 = _agi_pg.K_UP, _agi_pg.K_x
        AGI_K_CCW = _agi_pg.K_z
        AGI_K_HARD = _agi_pg.K_SPACE
        AGI_K_HOLD1, AGI_K_HOLD2, AGI_K_HOLD3 = (
            _agi_pg.K_c, _agi_pg.K_LSHIFT, _agi_pg.K_RSHIFT)
    except Exception:
        AGI_K_LEFT = AGI_K_RIGHT = AGI_K_DOWN = -1
        AGI_K_CW1 = AGI_K_CW2 = AGI_K_CCW = AGI_K_HARD = -1
        AGI_K_HOLD1 = AGI_K_HOLD2 = AGI_K_HOLD3 = -1


    def ag_intake_cover():
        """Box art: a shelf mid-stack, one row about to be processed."""
        parts = ag_cover_base(AGI_ACCENT)
        stack = [
            (0, 3, "J"), (1, 3, "J"), (2, 3, "T"), (3, 3, "T"), (4, 3, "L"),
            (0, 4, "S"), (1, 4, "S"), (2, 4, "O"), (3, 4, "O"), (4, 4, "L"),
            (2, 1, "I"), (2, 2, "I"),
        ]
        for cx, cy, kind in stack:
            col = AGI_COLORS[kind]
            x = 48 + cx * 46
            y = 34 + cy * 40
            parts.append(Transform(Solid(ag_mix(col, "#0b0720", 0.45),
                                        xysize=(42, 36)), pos=(x, y)))
            parts.append(Transform(Solid(col, xysize=(36, 30)),
                                    pos=(x + 3, y + 3)))
        parts += ag_cover_title("COLD STORAGE", "INTAKE", AGI_ACCENT)
        return Fixed(*parts, xysize=(AG_COVER_SIZE, AG_COVER_SIZE))


    ag_register(
        "intake", AGIntake,
        title="Intake",
        accent=AGI_ACCENT,
        blurb="Rack the samples, fill a shelf, get it processed. Standard "
                "controls, standard rotation, except the backlog pushes a "
                "contaminated row up from the bottom on its own schedule.",
        controls=AGIntake.CONTROLS,
        music=audio.tetris,
        cover=ag_intake_cover,
    )
