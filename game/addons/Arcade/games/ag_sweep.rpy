# =============================================================================
# ag_sweep.rpy  --  CONTAINMENT SWEEP   (Arcade Original #4)
# =============================================================================
# Deduction on a grid, dressed as the job nobody in the lab wants: walking a
# floor after an incident with a detector that only tells you HOW MANY
# unlabelled incidents are near where you are standing, never which ones.
#
# WHY THIS IS ON THE SHELF
#   The other originals are reaction games. This one is the opposite kind of
#   pressure -- no reflex at all, only inference, with a clock running. It is
#   also played with the mouse, which is why the framework's right-click-to-
#   pause binding is switched off for it (AGGame.MOUSE).
#
# THE RULES THE GENRE SHARES
#   A reading counts the incidents around its tile, a tile reading zero floods
#   open its whole region, labels mark what you have deduced, and a satisfied
#   reading can be CHORDED to open the rest around it (left-click as well as
#   middle-click). The first sweep is always safe: incidents are laid AFTER it,
#   with the clicked tile and its neighbourhood excluded.
#
# THE RULES THAT ARE THIS CABINET'S OWN
#   WIDE READINGS   about one clean tile in ten carries a wide-field sensor. Its
#                   reading counts the 5 x 5 around it -- two tiles out, not
#                   one -- and it is drawn with corner marks so it can never be
#                   mistaken for an ordinary reading. A wide zero floods like
#                   any zero; a wide chord opens its whole 5 x 5. It changes the
#                   deduction rather than the difficulty: a wide 3 beside an
#                   ordinary 1 says things neither says alone.
#   HAZMAT SUITS    each floor issues suits (1 / 2 / 3 by size). Stepping on an
#                   incident while wearing one TEARS it instead of ending the
#                   run: the incident is contained where it stands (it counts as
#                   labelled from then on, so the readings around it still add
#                   up), and the clock takes a penalty. The run ends on the
#                   incident you find with no suit left. Suits you walk out with
#                   are paid on a clear, so a forced guess is a real trade rather
#                   than a coin flip for the whole board.
#   THE FLOORS      10 x 10, 18 x 14 and 26 x 16, at their own densities.
#
# SCORING
#   Five points a tile keeps a lost run from being worth nothing. A clear pays
#   500, plus ten a second under par (penalties included), plus every suit left.
#   Best CLEAR TIME per floor is recorded separately from the score -- for this
#   genre the time is the real record, and the score is the arcade ranking it.
# =============================================================================

init python:
    import math
    import random

    AGS2_ACCENT = "#e0c05e"
    AGS2_WIDE_INK = "#6fd0ff"

    # variant id -> (label, cols, rows, incidents, cell px, par seconds, suits)
    # Densities run ~13% / ~17% / ~21%; the last is where logic alone stops
    # always being enough, which is exactly where the suits start to matter.
    # OUTBREAK was 92 at first: a subset-logic solver then won 28/40 but needed
    # two suits a run and cleared only 2/40 without one. At 86 it stays the
    # hard floor without making the suits mandatory.
    AGS2_BOARDS = {
        "spill":    ("SPILL", 10, 10, 13, 44, 75, 1),
        "breach":   ("BREACH", 18, 14, 42, 34, 240, 2),
        "outbreak": ("OUTBREAK", 26, 16, 86, 32, 520, 3),
    }
    AGS2_ORDER = ["spill", "breach", "outbreak"]
    # Vertical budget: header band ends ~110, legend sits at 696, and the two
    # lines under the board need ~50. Every board centres inside this box.
    AGS2_MAX_H = 512
    AGS2_TOP = 118

    AGS2_WIDE_SHARE = 0.10      # share of clean tiles that carry a wide sensor
    AGS2_WIDE_R = 2             # a wide sensor reads this far out (5 x 5)
    AGS2_SUIT_PENALTY = 20      # seconds added to the clock per torn suit
    AGS2_SUIT_BONUS = 300       # paid per suit still whole on a clear

    # A heat ramp, cool to hot, so a reading's colour says how dangerous its
    # neighbourhood is at a glance. Wide readings can run past eight; those
    # all draw white.
    AGS2_NUM = {
        1: "#7fe7c4", 2: "#b8e86a", 3: "#f0d45a", 4: "#f5a04a",
        5: "#f06a4a", 6: "#e8487a", 7: "#c65cff", 8: "#f7f0e6",
    }

    def ags2_num_color(n):
        return AGS2_NUM.get(n, "#ffffff")


    class AGSweep(AGGame):
        """Containment Sweep: grid deduction with wide readings and suits."""

        KIND = "sweep"
        TITLE = "CONTAINMENT SWEEP"
        ACCENT = AGS2_ACCENT
        MOUSE = True
        CONTROLS = [
            ("LEFT CLICK", "reveal a tile"),
            ("RIGHT CLICK", "mark a suspected incident"),
            ("LEFT CLICK on a number", "open the rest around it"),
            ("CORNER-MARKED NUMBER", "counts two tiles out, not one"),
            ("ARROWS + Z / X", "the same, without a mouse"),
            ("ESC", "pause  //  Q while paused gives up"),
        ]

        def __init__(self, variant=None):
            super(AGSweep, self).__init__(variant)

            key = variant if variant in AGS2_BOARDS else "breach"
            self.board = key
            label, cols, rows, mines, cell, par, suits = AGS2_BOARDS[key]
            self.label = label
            self.cols = cols
            # nrows, not rows: AGGame.rows() is the results-card method, and an
            # attribute of the same name shadows it -- which silently costs the
            # card every stat line but one.
            self.nrows = rows
            self.mines = mines
            self.cell = cell
            self.par = par
            self.suits_issued = suits
            self.suits = suits

            self.w = cols * cell
            self.h = rows * cell
            self.bx = (AG_W - self.w) // 2
            self.by = AGS2_TOP + max(0, (AGS2_MAX_H - self.h) // 2)

            # Board planes. Flat lists indexed y * cols + x.
            n = cols * rows
            self.mine = [False] * n
            self.wide = [False] * n
            self.read = [0] * n         # what the tile's sensor reports
            self.shown = [False] * n
            self.flag = [False] * n
            self.torn = [False] * n     # an incident contained by a suit

            self.placed = False         # incidents are laid on the first sweep
            self.revealed = 0
            self.flags = 0
            self.breaches = 0
            self.penalty = 0            # seconds
            self.clicks = 0
            self.chords = 0
            self.elapsed = 0            # ticks
            self.cursor = [cols // 2, rows // 2]
            self.hover = None
            self.boom = None            # the incident that ended the run
            self.ending = 0
            self.won = False
            self.note = None
            self.shake = 0

        # ---- grid helpers ---------------------------------------------------

        def _idx(self, x, y):
            return y * self.cols + x

        def _around(self, x, y, r):
            """Every tile within Chebyshev distance r of (x, y), itself
            excluded, clipped to the floor."""
            for ny in range(max(0, y - r), min(self.nrows, y + r + 1)):
                for nx in range(max(0, x - r), min(self.cols, x + r + 1)):
                    if nx != x or ny != y:
                        yield nx, ny

        def _neighbours(self, x, y):
            return self._around(x, y, 1)

        def _reach(self, i):
            """How far this tile's sensor reads: 1, or 2 for a wide one."""
            return AGS2_WIDE_R if self.wide[i] else 1

        def _place(self, safe_x, safe_y):
            """Lay the incidents, keeping the opening move and everything
            touching it clear, then hand out wide sensors -- never inside that
            opening, so the first sweep always floods a real region. If the
            board were too dense for the exclusion zone, only the clicked tile
            itself would be protected."""
            forbidden = set([(safe_x, safe_y)])
            for nx, ny in self._neighbours(safe_x, safe_y):
                forbidden.add((nx, ny))
            cells = [(x, y)
                     for y in range(self.nrows)
                     for x in range(self.cols)]
            pool = [c for c in cells if c not in forbidden]
            if len(pool) < self.mines:
                pool = [c for c in cells if c != (safe_x, safe_y)]

            for x, y in random.sample(pool, self.mines):
                self.mine[self._idx(x, y)] = True

            clean = [c for c in cells
                     if c not in forbidden and not self.mine[self._idx(*c)]]
            wide = int(round(AGS2_WIDE_SHARE * len(clean)))
            for x, y in random.sample(clean, min(wide, len(clean))):
                self.wide[self._idx(x, y)] = True

            for y in range(self.nrows):
                for x in range(self.cols):
                    i = self._idx(x, y)
                    if self.mine[i]:
                        continue
                    self.read[i] = sum(
                        1 for nx, ny in self._around(x, y, self._reach(i))
                        if self.mine[self._idx(nx, ny)])
            self.placed = True

        # ---- actions --------------------------------------------------------

        def _reveal(self, x, y):
            """Open one tile, flooding through the zero region it belongs to.
            Returns "boom", "torn" or None so a chord knows to stop.

            The flood is an explicit stack rather than recursion: a big floor
            with a lucky opening can cascade through hundreds of tiles. A zero
            -- ordinary or wide -- means nothing is in its 3 x 3, so its eight
            neighbours are always safe to open."""
            if self.ending:
                return None
            start = self._idx(x, y)
            if self.flag[start] or self.shown[start] or self.torn[start]:
                return None
            if not self.placed:
                self._place(x, y)

            if self.mine[start]:
                if self.suits > 0:
                    self._tear(start)
                    return "torn"
                self.boom = start
                self._lose()
                return "boom"

            stack = [(x, y)]
            opened = 0
            while stack:
                cx, cy = stack.pop()
                i = self._idx(cx, cy)
                if self.shown[i] or self.flag[i]:
                    continue
                self.shown[i] = True
                opened += 1
                if self.read[i] == 0:
                    for nx, ny in self._neighbours(cx, cy):
                        if not self.shown[self._idx(nx, ny)]:
                            stack.append((nx, ny))

            self.revealed += opened
            self.score += 5 * opened
            ag_se("reveal", 0.5 if opened < 4 else 0.75)
            self._check_win()
            return None

        def _tear(self, i):
            """A suit takes the hit: the incident is contained where it stands
            and counts as labelled from now on, and the clock pays for it."""
            self.suits -= 1
            self.breaches += 1
            self.torn[i] = True
            self.penalty += AGS2_SUIT_PENALTY
            self.elapsed += AGS2_SUIT_PENALTY * 60
            self.shake = 18
            ag_se("boom", 0.55)
            ag_se("spoil", 0.8)
            if self.suits:
                self._say("SUIT USED  --  %d LEFT  //  +%ds"
                          % (self.suits, AGS2_SUIT_PENALTY), "#f5a04a")
            else:
                self._say("LAST SUIT USED  //  +%ds" % AGS2_SUIT_PENALTY,
                          "#e0455e")

        def _toggle_flag(self, x, y):
            i = self._idx(x, y)
            if self.shown[i] or self.torn[i] or self.ending:
                return
            self.flag[i] = not self.flag[i]
            self.flags += 1 if self.flag[i] else -1
            ag_se("flag", 0.6)

        def _chord(self, x, y):
            """Open every unlabelled tile a satisfied reading covers -- its 3 x 3,
            or its 5 x 5 for a wide sensor. Wrong labels make this lethal, which
            is the whole bargain; a torn suit stops the chord where it lands."""
            i = self._idx(x, y)
            if not self.shown[i] or self.read[i] == 0:
                return
            around = list(self._around(x, y, self._reach(i)))
            known = sum(1 for nx, ny in around
                        if self.flag[self._idx(nx, ny)]
                        or self.torn[self._idx(nx, ny)])
            if known != self.read[i]:
                ag_se("deny", 0.4)
                return
            self.chords += 1
            for nx, ny in around:
                j = self._idx(nx, ny)
                if not self.flag[j] and not self.shown[j] and not self.torn[j]:
                    if self._reveal(nx, ny) or self.ending:
                        return

        def _check_win(self):
            if self.revealed >= self.cols * self.nrows - self.mines:
                self.won = True
                self.ending = 1
                seconds = self.elapsed // 60
                self.score += (500 + max(0, self.par - seconds) * 10
                               + self.suits * AGS2_SUIT_BONUS)
                ag_se("clear")

        def _lose(self):
            self.ending = 1
            self.won = False
            self.shake = 24
            ag_se("boom")
            ag_se("over", 0.7)

        def _say(self, text, color=None, ticks=110):
            self.note = [text, ticks, color or AGS2_ACCENT]

        # ---- input ----------------------------------------------------------

        def _cell_at(self, px, py):
            if not (self.bx <= px < self.bx + self.w
                    and self.by <= py < self.by + self.h):
                return None
            return (int((px - self.bx) // self.cell),
                    int((py - self.by) // self.cell))

        def on_event(self, ev, x, y):
            try:
                import pygame_sdl2 as pg
            except Exception:
                return
            if ev.type == pg.MOUSEMOTION:
                self.hover = self._cell_at(x, y)
                return
            if ev.type != pg.MOUSEBUTTONDOWN or self.ending:
                return
            spot = self._cell_at(x, y)
            if spot is None:
                return
            cx, cy = spot
            self.cursor = [cx, cy]
            button = getattr(ev, "button", 1)
            if button == 3:
                self._toggle_flag(cx, cy)
            elif button == 2:
                self._chord(cx, cy)
            elif button == 1:
                self.clicks += 1
                # Left-clicking an open reading chords; anything else sweeps.
                if self.shown[self._idx(cx, cy)]:
                    self._chord(cx, cy)
                else:
                    self._reveal(cx, cy)

        def _read_keys(self, keys):
            if keys is None:
                return
            moved = False
            if self.tapped(keys, "left", AGS2_K_LEFT1, AGS2_K_LEFT2):
                self.cursor[0] = max(0, self.cursor[0] - 1)
                moved = True
            if self.tapped(keys, "right", AGS2_K_RIGHT1, AGS2_K_RIGHT2):
                self.cursor[0] = min(self.cols - 1, self.cursor[0] + 1)
                moved = True
            if self.tapped(keys, "up", AGS2_K_UP1, AGS2_K_UP2):
                self.cursor[1] = max(0, self.cursor[1] - 1)
                moved = True
            if self.tapped(keys, "down", AGS2_K_DOWN1, AGS2_K_DOWN2):
                self.cursor[1] = min(self.nrows - 1, self.cursor[1] + 1)
                moved = True
            if moved:
                self.hover = None
                ag_se("ui_move", 0.3)

            cx, cy = self.cursor
            if self.tapped(keys, "ok", AGS2_K_OK1, AGS2_K_OK2):
                self.clicks += 1
                if self.shown[self._idx(cx, cy)]:
                    self._chord(cx, cy)
                else:
                    self._reveal(cx, cy)
            if self.tapped(keys, "flag", AGS2_K_FLAG1, AGS2_K_FLAG2):
                self._toggle_flag(cx, cy)

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

            if self.ending:
                self.ending += 1
                if self.ending > 150:
                    self.finish("clear" if self.won else "over")
                return

            self._read_keys(keys)

            # The clock starts on the first sweep, not on the first frame, so
            # reading the board before you commit costs nothing.
            if self.placed:
                self.elapsed += 1

        # ---- drawing --------------------------------------------------------

        def _cell_xy(self, x, y):
            ox = int(math.sin(self.tick * 1.9) * min(5, self.shake)) if self.shake else 0
            return (self.bx + x * self.cell + ox, self.by + y * self.cell)

        def draw(self, c):
            self._draw_floor(c)
            self._draw_cells(c)
            self._draw_marker(c)
            self._draw_hud(c)
            if self.ending:
                self._draw_end(c)

        def _draw_floor(self, c):
            c.panel(self.bx - 14, self.by - 14, self.w + 28, self.h + 28,
                    top="#161038ea", bottom="#0b0720f2", radius=16,
                    border=1.5, bcolor=(AGS2_ACCENT + "55"))

        def _draw_cells(self, c):
            cell = self.cell
            reveal_all = bool(self.ending)
            for y in range(self.nrows):
                for x in range(self.cols):
                    i = self._idx(x, y)
                    px, py = self._cell_xy(x, y)

                    if self.shown[i]:
                        c.rect("#0d0a1e", px + 1, py + 1, cell - 2, cell - 2)
                        c.rect("#ffffff08", px + 1, py + 1, cell - 2, 1)
                        if self.wide[i]:
                            self._draw_wide_marks(c, px, py)
                        n = self.read[i]
                        if n:
                            # UI face, not the display face: the display font's
                            # 1 is a bare bar, which on a board of readings is
                            # exactly the digit you cannot afford to misread.
                            c.text(str(n), px + cell / 2.0, py + cell / 2.0,
                                    size=int(cell * (0.56 if n < 10 else 0.44)),
                                    color=ags2_num_color(n),
                                    font=AG_FONT_UI, bold=True,
                                    anchor=(0.5, 0.5))
                        continue

                    if self.torn[i]:
                        self._draw_contained(c, px, py)
                        continue

                    if reveal_all and self.mine[i] and not self.flag[i]:
                        self._draw_incident(c, px, py, i == self.boom)
                        continue

                    # Unswept: a raised tile.
                    c.panel(px + 1, py + 1, cell - 2, cell - 2,
                            top="#2b2350", bottom="#1b1638", radius=5,
                            border=1.0, bcolor="#ffffff12")
                    if self.flag[i]:
                        wrong = reveal_all and not self.mine[i]
                        self._draw_label(c, px, py, wrong)

        def _draw_wide_marks(self, c, px, py):
            """Corner marks on a wide sensor: four L-shaped ticks just inside
            the tile, in a cool ink no reading ever uses."""
            s = self.cell
            k = max(6, int(s * 0.24))
            ink = AGS2_WIDE_INK + "cc"
            for ox, oy, sx, sy in ((3, 3, 1, 1), (s - 3, 3, -1, 1),
                                   (3, s - 3, 1, -1), (s - 3, s - 3, -1, -1)):
                x0 = px + ox
                y0 = py + oy
                c.rect(ink, x0 if sx > 0 else x0 - k, y0 if sy > 0 else y0 - 2,
                       k, 2)
                c.rect(ink, x0 if sx > 0 else x0 - 2, y0 if sy > 0 else y0 - k,
                       2, k)

        def _draw_incident(self, c, px, py, hot):
            cell = self.cell
            col = "#ff5c6e" if hot else "#a03bd6"
            c.rect(ag_mix(col, "#0b0720", 0.55), px + 1, py + 1,
                    cell - 2, cell - 2)
            r = int(cell * 0.30)
            c.panel(px + cell / 2.0 - r, py + cell / 2.0 - r, r * 2, r * 2,
                    top=col, radius=r)
            c.rect("#ffffffaa", px + cell / 2.0 - 1, py + 5, 2, cell - 10)
            c.rect("#ffffffaa", px + 5, py + cell / 2.0 - 1, cell - 10, 2)

        def _draw_contained(self, c, px, py):
            """An incident a suit took: amber, boxed in, clearly dealt with."""
            cell = self.cell
            c.rect("#2a1608", px + 1, py + 1, cell - 2, cell - 2)
            r = int(cell * 0.22)
            c.panel(px + cell / 2.0 - r, py + cell / 2.0 - r, r * 2, r * 2,
                    top="#f5a04a", radius=r)
            c.frame(AGS2_ACCENT + "cc", px + 4, py + 4, cell - 8, cell - 8, 2)

        def _draw_label(self, c, px, py, wrong):
            cell = self.cell
            col = "#e0455e" if wrong else AGS2_ACCENT
            # A specimen label: pin, tag, and a strike through it if it was
            # placed on a tile that turned out to be clean.
            c.rect("#d8d2e8", px + cell * 0.42, py + cell * 0.24, 2,
                    cell * 0.52)
            c.rect(col, px + cell * 0.44, py + cell * 0.24, cell * 0.30,
                    cell * 0.22)
            if wrong:
                c.rect("#ffffffcc", px + 6, py + cell / 2.0 - 1, cell - 12, 2)

        def _draw_marker(self, c):
            spot = self.hover if self.hover is not None else tuple(self.cursor)
            if spot is None:
                return
            x, y = spot
            if not (0 <= x < self.cols and 0 <= y < self.nrows):
                return
            px, py = self._cell_xy(x, y)
            pulse = 0.55 + 0.45 * math.sin(self.tick * 0.16)
            c.frame("%s%02x" % (AGS2_ACCENT, int(200 * pulse)),
                    px, py, self.cell, self.cell, 2)

        def _draw_hud(self, c):
            # Header left, readouts right, both on the shared grid -- so neither
            # moves when the board size does.
            left = self.mines - self.flags - self.breaches
            c.header("CONTAINMENT SWEEP",
                    "%s  //  %d x %d" % (self.label, self.cols, self.nrows), AGS2_ACCENT)
            c.stat_row([
                ("SCORE", ag_num(self.score), AG_DIM),
                ("TIME", ag_time(self.elapsed / 60.0),
                    ("#f5a04a" if self.penalty else AG_DIM)),
                ("SUITS", "%d / %d" % (self.suits, self.suits_issued),
                    ("#e0455e" if self.suits == 0 else AG_INK)),
                ("REMAINING", str(left),
                    ("#e0455e" if left < 0 else AG_INK)),
            ])

            # One quiet centred line under the board for the numbers that only
            # matter between runs.
            best = ag_best("sweep_clear_" + self.board)
            y = self.by + self.h + 20
            note = "PAR  %s" % ag_time(self.par)
            if best:
                note = "BEST CLEAR  %s        %s" % (ag_time(best), note)
            c.text(note, AG_W / 2, y, size=13, color=AG_FAINT,
                    anchor=(0.5, 0.0))

            if not self.placed:
                pulse = 0.5 + 0.5 * math.sin(self.tick * 0.1)
                c.text("the first click is always safe", AG_W / 2, y + 24,
                        size=16, color=AGS2_ACCENT, anchor=(0.5, 0.0),
                        alpha=pulse)

            # Callouts flash inside the floor, near its top edge, on a dark
            # plate: without one they sit on top of the readings they cover.
            if self.note is not None:
                text, ticks, col = self.note
                a = ag_clamp(ticks / 40.0, 0.0, 1.0)
                c.rect("#0a0713%02x" % int(215 * a), self.bx, self.by + 8,
                       self.w, 36)
                c.text(text, AG_W / 2, self.by + 26, size=18, color=col,
                       bold=True, kerning=2.0, anchor=(0.5, 0.5), alpha=a)

            c.legend("LEFT REVEAL   //   RIGHT MARK   //   CORNER-MARKED "
                     "NUMBERS COUNT TWO TILES OUT   //   ESC PAUSE")

        def _draw_end(self, c):
            a = ag_clamp(self.ending / 26.0, 0.0, 1.0)
            if self.won:
                c.rect("#04120c%02x" % int(140 * a), 0, 0, AG_W, AG_H)
                c.text("FLOOR CLEAR", AG_W / 2, AG_H / 2 - 18, size=50,
                        color="#4fbf7a", font=AG_FONT, bold=True,
                        anchor=(0.5, 0.5), alpha=a)
                c.text("%s  --  %s" % (self.label, ag_time(self.elapsed / 60.0)),
                        AG_W / 2, AG_H / 2 + 30, size=18, color=AG_DIM,
                        anchor=(0.5, 0.5), alpha=a)
            else:
                c.rect("#12040c%02x" % int(150 * a), 0, 0, AG_W, AG_H)
                c.text("GAME OVER", AG_W / 2, AG_H / 2 - 18,
                        size=48, color="#e0455e", font=AG_FONT, bold=True,
                        anchor=(0.5, 0.5), alpha=a)
                c.text("no suits left",
                       AG_W / 2, AG_H / 2 + 30, size=18,
                        color=AG_DIM, anchor=(0.5, 0.5), alpha=a)

        # ---- results --------------------------------------------------------

        def record(self):
            self.new_record = ag_set_best("sweep_score", self.score)
            if self.won:
                ag_set_best("sweep_clear_" + self.board, self.elapsed // 60,
                            lower_is_better=True)

        def outcome(self, kind):
            if kind == "quit":
                return "ABANDONED"
            return "FLOOR CLEAR" if self.won else "GAME OVER"

        def card_accent(self, kind):
            if kind == "quit":
                return "#8f86a8"
            return "#4fbf7a" if self.won else "#e0455e"

        def rows(self, kind):
            seconds = self.elapsed // 60
            best = ag_best("sweep_clear_" + self.board)
            time_txt = ag_time(seconds)
            if self.penalty:
                time_txt += "  (+%ds)" % self.penalty
            out = [
                ("FLOOR", self.label),
                ("TIME", time_txt),
                ("SCORE", ag_num(self.score)),
                ("REVEALED", "%d / %d" % (self.revealed,
                                        self.cols * self.nrows - self.mines)),
                ("SUITS USED", "%d / %d" % (self.breaches, self.suits_issued)),
            ]
            if best:
                out.append(("BEST CLEAR", ag_time(best)))
            return out


    try:
        import pygame_sdl2 as _ags2_pg
        AGS2_K_LEFT1, AGS2_K_LEFT2 = _ags2_pg.K_LEFT, _ags2_pg.K_a
        AGS2_K_RIGHT1, AGS2_K_RIGHT2 = _ags2_pg.K_RIGHT, _ags2_pg.K_d
        AGS2_K_UP1, AGS2_K_UP2 = _ags2_pg.K_UP, _ags2_pg.K_w
        AGS2_K_DOWN1, AGS2_K_DOWN2 = _ags2_pg.K_DOWN, _ags2_pg.K_s
        AGS2_K_OK1, AGS2_K_OK2 = _ags2_pg.K_z, _ags2_pg.K_RETURN
        AGS2_K_FLAG1, AGS2_K_FLAG2 = _ags2_pg.K_x, _ags2_pg.K_f
    except Exception:
        AGS2_K_LEFT1 = AGS2_K_LEFT2 = AGS2_K_RIGHT1 = AGS2_K_RIGHT2 = -1
        AGS2_K_UP1 = AGS2_K_UP2 = AGS2_K_DOWN1 = AGS2_K_DOWN2 = -1
        AGS2_K_OK1 = AGS2_K_OK2 = AGS2_K_FLAG1 = AGS2_K_FLAG2 = -1


    def ag_sweep_cover():
        """Box art: a corner of a floor mid-sweep -- readings, a wide sensor,
        one label, and one tile that was a bad idea."""
        parts = ag_cover_base(AGS2_ACCENT)
        readings = {
            (0, 0): "1", (1, 0): "1", (2, 0): "", (3, 0): "2",
            (0, 1): "1", (1, 1): "W", (2, 1): "3", (3, 1): "!",
            (0, 2): "", (1, 2): "F", (2, 2): "2", (3, 2): "1",
            (0, 3): "", (1, 3): "1", (2, 3): "1", (3, 3): "1",
        }
        for (cx, cy), ch in readings.items():
            x = 40 + cx * 60
            y = 26 + cy * 50
            if ch == "":
                parts.append(Transform(Solid("#2b2350", xysize=(54, 44)),
                                        pos=(x, y)))
                continue
            parts.append(Transform(Solid("#0d0a1e", xysize=(54, 44)),
                                    pos=(x, y)))
            if ch == "F":
                parts.append(Transform(Solid(AGS2_ACCENT, xysize=(18, 14)),
                                        pos=(x + 20, y + 12)))
            elif ch == "!":
                parts.append(Transform(Solid("#ff5c6e", xysize=(24, 24)),
                                        pos=(x + 15, y + 10)))
            else:
                value = "5" if ch == "W" else ch
                if ch == "W":
                    for ox, oy, w, h in ((3, 3, 12, 2), (3, 3, 2, 12),
                                         (39, 3, 12, 2), (49, 3, 2, 12),
                                         (3, 39, 12, 2), (3, 29, 2, 12),
                                         (39, 39, 12, 2), (49, 29, 2, 12)):
                        parts.append(Transform(
                            Solid(AGS2_WIDE_INK, xysize=(w, h)),
                            pos=(x + ox, y + oy)))
                parts.append(Transform(
                    Text(value, font=AG_FONT_UI, size=28, bold=True,
                        color=ags2_num_color(int(value))),
                    pos=(x + 20, y + 6)))
        parts += ag_cover_title("DEDUCTION", "CONTAINMENT SWEEP",
                                AGS2_ACCENT)
        return Fixed(*parts, xysize=(AG_COVER_SIZE, AG_COVER_SIZE))


    ag_register(
        "sweep", AGSweep,
        title="Containment Sweep",
        accent=AGS2_ACCENT,
        blurb="Find every incident without stepping on one. Corner-marked "
                "numbers count two tiles out, and a hazmat suit survives one "
                "bad step.",
        controls=AGSweep.CONTROLS,
        music=audio.holdmusic,
        cover=ag_sweep_cover,
        variants=[(vid, AGS2_BOARDS[vid][0],
                    "%d x %d  //  %d incidents  //  %d suit%s  //  par %s"
                    % (AGS2_BOARDS[vid][1], AGS2_BOARDS[vid][2],
                        AGS2_BOARDS[vid][3], AGS2_BOARDS[vid][6],
                        "" if AGS2_BOARDS[vid][6] == 1 else "s",
                        ag_time(AGS2_BOARDS[vid][5])))
                for vid in AGS2_ORDER],
    )
