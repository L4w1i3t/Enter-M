# =============================================================================
# ag_sweep.rpy  --  CONTAINMENT SWEEP   (Arcade Original #4)
# =============================================================================
# Minesweeper, dressed as the job nobody in the lab wants: walking a floor after
# an incident with a detector that only tells you HOW MANY unlabelled flasks are
# next to where you are standing, never which ones.
#
# WHY THIS IS ON THE SHELF
#   The other three originals are reaction games. This one is the opposite kind
#   of pressure -- no reflex at all, only inference, with a clock running. It is
#   also the only cabinet played entirely with the mouse, which is why the
#   framework's right-click-to-pause binding is switched off for it (AGGame.MOUSE).
#
# THE RULES, AND THE TWO THAT ARE NOT STANDARD
#   Standard: numbers count adjacent incidents, an empty cell floods open its
#   whole region, flags mark what you have deduced, and a revealed number with
#   exactly its count in flags around it can be CHORDED to open the rest.
#   Not standard, and both are anti-frustration rather than difficulty:
#     * The first sweep is always safe -- incidents are placed AFTER it, with
#       the clicked cell and its whole neighbourhood excluded. So the opening
#       move can never be a coin flip, and it always opens a real region.
#     * Chording is on left-click as well as middle-click. Middle-click is the
#       traditional binding and almost nobody knows it exists.
#
# SCORING
#   Five points a cell keeps a lost run from being worth nothing, and the win
#   bonus is a par-time race: clear the floor under par and the remaining
#   seconds are worth ten each. Best CLEAR TIME per board is recorded separately
#   from the score (ag_set_best with lower_is_better) -- for this genre the time
#   is the real record and the score is the arcade's way of ranking it.
# =============================================================================

init python:
    import math
    import random

    AGS2_ACCENT = "#e0c05e"

    # variant id -> (label, cols, rows, incidents, cell px, par seconds)
    # Densities are the genre's own: ~12% for the small board, ~16% for the
    # middle one, ~21% for the big one (the same ratio as an expert board, which
    # is the point at which pure logic stops always being enough).
    AGS2_BOARDS = {
        "spill":    ("SPILL", 9, 9, 10, 44, 60),
        "breach":   ("BREACH", 16, 16, 40, 32, 200),
        "outbreak": ("OUTBREAK", 24, 16, 80, 32, 420),
    }
    AGS2_ORDER = ["spill", "breach", "outbreak"]
    # Vertical budget: header band ends ~110, legend sits at 696, and the two
    # lines under the board need ~50. Every board centres inside this box.
    AGS2_MAX_H = 512            # tallest board; smaller ones centre inside it
    AGS2_TOP = 118

    # Reading colours. The classic ramp (cool for low counts, hot for high),
    # pulled onto this project's palette so the board sits in the same world as
    # the rest of the cabinet.
    AGS2_NUM = {
        1: "#6f9bff", 2: "#4fbf7a", 3: "#ff7a8a", 4: "#b57ae0",
        5: "#e0a04f", 6: "#5ec8e0", 7: "#f7f0e6", 8: "#a99fc4",
    }


    class AGSweep(AGGame):
        """Containment Sweep: minesweeper with a first-move guarantee."""

        KIND = "sweep"
        TITLE = "CONTAINMENT SWEEP"
        ACCENT = AGS2_ACCENT
        MOUSE = True
        CONTROLS = [
            ("LEFT CLICK", "sweep a tile"),
            ("RIGHT CLICK", "label a suspected incident"),
            ("LEFT CLICK on a reading", "chord -- open the rest around it"),
            ("ARROWS + Z / X", "the same, without a mouse"),
            ("ESC", "pause  //  Q while paused gives up"),
        ]

        def __init__(self, variant=None):
            super(AGSweep, self).__init__(variant)

            key = variant if variant in AGS2_BOARDS else "breach"
            self.board = key
            label, cols, rows, mines, cell, par = AGS2_BOARDS[key]
            self.label = label
            self.cols = cols
            # nrows, not rows: AGGame.rows() is the results-card method, and an
            # attribute of the same name shadows it -- which silently costs the
            # card every stat line but one.
            self.nrows = rows
            self.mines = mines
            self.cell = cell
            self.par = par

            self.w = cols * cell
            self.h = rows * cell
            self.bx = (AG_W - self.w) // 2
            self.by = AGS2_TOP + max(0, (AGS2_MAX_H - self.h) // 2)

            # Board planes. Flat lists indexed y * cols + x: one allocation, and
            # the neighbour walk below is the only place indices are computed.
            n = cols * rows
            self.mine = [False] * n
            self.adj = [0] * n
            self.shown = [False] * n
            self.flag = [False] * n

            self.placed = False         # incidents are laid on the first sweep
            self.revealed = 0
            self.flags = 0
            self.clicks = 0
            self.chords = 0
            self.elapsed = 0            # ticks
            self.cursor = [cols // 2, rows // 2]
            self.hover = None
            self.boom = None            # index of the incident that got you
            self.ending = 0
            self.won = False
            self.note = None

        # ---- grid helpers ---------------------------------------------------

        def _idx(self, x, y):
            return y * self.cols + x

        def _neighbours(self, x, y):
            for dy in (-1, 0, 1):
                ny = y + dy
                if ny < 0 or ny >= self.nrows:
                    continue
                for dx in (-1, 0, 1):
                    nx = x + dx
                    if (dx == 0 and dy == 0) or nx < 0 or nx >= self.cols:
                        continue
                    yield nx, ny

        def _place(self, safe_x, safe_y):
            """Lay the incidents, keeping the opening move and everything
            touching it clear. If the board is so dense that the exclusion zone
            would not leave room, only the clicked cell itself is protected --
            the guarantee is 'your first click is safe', not 'your first click
            opens a cavern'."""
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

            for y in range(self.nrows):
                for x in range(self.cols):
                    if self.mine[self._idx(x, y)]:
                        continue
                    self.adj[self._idx(x, y)] = sum(
                        1 for nx, ny in self._neighbours(x, y)
                        if self.mine[self._idx(nx, ny)])
            self.placed = True

        # ---- actions --------------------------------------------------------

        def _reveal(self, x, y):
            """Open one cell, flooding through the empty region it belongs to.

            The flood is an explicit stack rather than recursion: a 24x16 board
            with a lucky opening can cascade through nearly 400 cells, which is
            deep enough to matter and there is no reason to put it on Python's
            call stack.
            """
            if self.ending:
                return
            start = self._idx(x, y)
            if self.flag[start] or self.shown[start]:
                return
            # Incidents are laid on the first cell actually swept, around it --
            # so this is also the moment the clock starts.
            if not self.placed:
                self._place(x, y)

            if self.mine[start]:
                self.boom = start
                self._lose()
                return

            stack = [(x, y)]
            opened = 0
            while stack:
                cx, cy = stack.pop()
                i = self._idx(cx, cy)
                if self.shown[i] or self.flag[i]:
                    continue
                self.shown[i] = True
                opened += 1
                if self.adj[i] == 0:
                    for nx, ny in self._neighbours(cx, cy):
                        if not self.shown[self._idx(nx, ny)]:
                            stack.append((nx, ny))

            self.revealed += opened
            self.score += 5 * opened
            ag_se("reveal", 0.5 if opened < 4 else 0.75)
            self._check_win()

        def _toggle_flag(self, x, y):
            i = self._idx(x, y)
            if self.shown[i] or self.ending:
                return
            self.flag[i] = not self.flag[i]
            self.flags += 1 if self.flag[i] else -1
            ag_se("flag", 0.6)

        def _chord(self, x, y):
            """Open every unflagged neighbour of a satisfied reading. Wrong
            flags make this lethal, which is the whole bargain."""
            i = self._idx(x, y)
            if not self.shown[i] or self.adj[i] == 0:
                return
            around = list(self._neighbours(x, y))
            flagged = sum(1 for nx, ny in around if self.flag[self._idx(nx, ny)])
            if flagged != self.adj[i]:
                ag_se("deny", 0.4)
                return
            self.chords += 1
            for nx, ny in around:
                j = self._idx(nx, ny)
                if not self.flag[j] and not self.shown[j]:
                    self._reveal(nx, ny)
                    if self.ending:
                        return

        def _check_win(self):
            if self.revealed >= self.cols * self.nrows - self.mines:
                self.won = True
                self.ending = 1
                seconds = self.elapsed // 60
                bonus = 500 + max(0, self.par - seconds) * 10
                self.score += bonus
                ag_se("clear")

        def _lose(self):
            self.ending = 1
            self.won = False
            ag_se("boom")
            ag_se("over", 0.7)

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
                # Left-clicking an open reading chords; left-clicking anything
                # else sweeps it.
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
            return (self.bx + x * self.cell, self.by + y * self.cell)

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
                        # Swept floor: a recessed seat with its reading.
                        c.rect("#0d0a1e", px + 1, py + 1, cell - 2, cell - 2)
                        c.rect("#ffffff08", px + 1, py + 1, cell - 2, 1)
                        n = self.adj[i]
                        if n:
                            # UI face, not the display face: the display font's
                            # 1 is a bare bar, which on a board of readings is
                            # exactly the digit you cannot afford to misread.
                            c.text(str(n), px + cell / 2.0, py + cell / 2.0,
                                    size=int(cell * 0.56),
                                    color=AGS2_NUM.get(n, AG_INK),
                                    font=AG_FONT_UI, bold=True,
                                    anchor=(0.5, 0.5))
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

        def _draw_label(self, c, px, py, wrong):
            cell = self.cell
            col = "#e0455e" if wrong else AGS2_ACCENT
            # A specimen label: pin, tag, and a strike through it if it was
            # placed on a cell that turned out to be clean.
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
            # moves when the board size does. (They used to be pinned to the
            # board's own edges, and on the small floor they collided.)
            left = self.mines - self.flags
            c.header("CONTAINMENT SWEEP",
                    "MATSUCOM  //  FLOOR: %s" % self.label, AGS2_ACCENT)
            c.stat_row([
                ("SCORE", ag_num(self.score), AG_DIM),
                ("TIME", ag_time(self.elapsed / 60.0), AG_DIM),
                ("UNLABELLED", str(left),
                    ("#e0455e" if left < 0 else AG_INK)),
            ])

            # One quiet centred line under the board for the two numbers that
            # only matter between runs.
            best = ag_best("sweep_time_" + self.board)
            y = self.by + self.h + 20
            note = "PAR  %s" % ag_time(self.par)
            if best:
                note = "BEST CLEAR  %s        %s" % (ag_time(best), note)
            c.text(note, AG_W / 2, y, size=13, color=AG_FAINT,
                    anchor=(0.5, 0.0))

            if not self.placed:
                pulse = 0.5 + 0.5 * math.sin(self.tick * 0.1)
                c.text("the first sweep is always safe", AG_W / 2, y + 24,
                        size=16, color=AGS2_ACCENT, anchor=(0.5, 0.0),
                        alpha=pulse)

            c.legend("LEFT SWEEP   //   RIGHT LABEL   //   ESC PAUSE")

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
                c.text("CONTAINMENT FAILURE", AG_W / 2, AG_H / 2 - 18,
                        size=48, color="#e0455e", font=AG_FONT, bold=True,
                        anchor=(0.5, 0.5), alpha=a)
                c.text("you stood on one", AG_W / 2, AG_H / 2 + 30, size=18,
                        color=AG_DIM, anchor=(0.5, 0.5), alpha=a)

        # ---- results --------------------------------------------------------

        def record(self):
            self.new_record = ag_set_best("sweep_score", self.score)
            if self.won:
                ag_set_best("sweep_time_" + self.board, self.elapsed // 60,
                            lower_is_better=True)

        def outcome(self, kind):
            if kind == "quit":
                return "ABANDONED"
            return "FLOOR CLEAR" if self.won else "CONTAINMENT FAILURE"

        def card_accent(self, kind):
            if kind == "quit":
                return "#8f86a8"
            return "#4fbf7a" if self.won else "#e0455e"

        def rows(self, kind):
            seconds = self.elapsed // 60
            best = ag_best("sweep_time_" + self.board)
            out = [
                ("FLOOR", self.label),
                ("TIME", ag_time(seconds)),
                ("SCORE", ag_num(self.score)),
                ("SWEPT", "%d / %d" % (self.revealed,
                                        self.cols * self.nrows - self.mines)),
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
        """Box art: a corner of a floor mid-sweep -- readings, one label, and
        one tile that was a bad idea."""
        parts = ag_cover_base(AGS2_ACCENT)
        readings = {
            (0, 0): "1", (1, 0): "1", (2, 0): "", (3, 0): "2",
            (0, 1): "1", (1, 1): "2", (2, 1): "3", (3, 1): "!",
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
                parts.append(Transform(
                    Text(ch, font=AG_FONT, size=30, bold=True,
                        color=AGS2_NUM.get(int(ch), "#f7f0e6")),
                    pos=(x + 20, y + 6)))
        parts += ag_cover_title("INCIDENT FLOOR", "CONTAINMENT SWEEP",
                                AGS2_ACCENT)
        return Fixed(*parts, xysize=(AG_COVER_SIZE, AG_COVER_SIZE))


    ag_register(
        "sweep", AGSweep,
        title="Containment Sweep",
        accent=AGS2_ACCENT,
        blurb="Read the floor, label the incidents, don't stand on one. Three "
                "floor sizes, a first sweep that is always safe, and a par time "
                "to beat.",
        controls=AGSweep.CONTROLS,
        music=audio.holdmusic,
        cover=ag_sweep_cover,
        variants=[(vid, AGS2_BOARDS[vid][0],
                    "%d x %d  //  %d incidents  //  par %s"
                    % (AGS2_BOARDS[vid][1], AGS2_BOARDS[vid][2],
                        AGS2_BOARDS[vid][3], ag_time(AGS2_BOARDS[vid][5])))
                for vid in AGS2_ORDER],
    )
