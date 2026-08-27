# =============================================================================
# ag_core.rpy  --  ARCADE ORIGINALS: the shared cabinet
# =============================================================================
# The Arcade hub (game/addons/Arcade/arcade.rpy) launches the five STORY game
# modes -- fights that exist in the script and are merely replayable from a
# menu. This folder is the other half of the shelf: small ORIGINAL games that
# have no story attachment at all, exist only in the Arcade, and are always
# available (no clear predicate, no content warning). In fiction they are the
# cabinets Matsuda built in the lab because she was bored; mechanically they are
# pick-up-and-play score attacks.
#
# WHAT THIS FILE IS
#   The cabinet every original plugs into. One fixed-timestep displayable, one
#   gameplay screen, one pause overlay, one controls card, one launch label, one
#   record store. A new game is then ONE file that:
#       1. subclasses AGGame        (step() + draw(), nothing else is required)
#       2. calls ag_register(...)   (title, accent, blurb, controls, music, art)
#       3. adds one tile to arcade_items in arcade.rpy
#   Everything else -- pausing, quitting, results, high scores, the shelf cover,
#   the retry loop -- is inherited.
#
# THE SHAPE OF A GAME
#   AGGame owns state and rules; it does no drawing and knows nothing about
#   Matsu'Py displayables. AGStage owns the clock and the canvas; it knows nothing
#   about any particular game. They meet at exactly two calls per frame:
#       game.step()          advance 1/60s of simulation (called 0..N times)
#       game.draw(canvas)    paint the current state (called exactly once)
#   That split is what makes the games frame-rate independent: a machine drawing
#   at 30fps runs step() twice per frame and plays identically to one at 240.
#
# WHY POLLED INPUT, NOT KEY EVENTS
#   Same reasoning as Kotonoha mode: "which way is held THIS tick" is a state
#   question. Every read goes through MSBFKeyLatch (battle_logic.rpy) so a key
#   release swallowed by an alt-tab cannot leave the player gliding forever --
#   see the SHARED KEY LATCH block there. AGGame.held()/tapped() wrap it, and
#   AGStage.event() feeds it the real events. Mouse games (Peer Review, the
#   sweep) instead take raw events through AGGame.on_event().
#
# RECORDS
#   persistent.ag_records is one dict, id -> best value, written through
#   ag_set_best(). It is REASSIGNED rather than mutated in place so the
#   persistent file is unambiguously marked dirty (see the note on that
#   function), and unknown keys simply appear -- adding a game needs no
#   migration and old saves stay valid.
#
# COST
#   Everything here draws through the canvas' two caches: displayables are built
#   once and kept (AGCanvas._disp), and each distinct one is rendered at most
#   once per frame and then blitted many times (the per-frame memo). A game
#   drawing 600 cells a frame therefore costs 600 blits of a handful of
#   textures, which is what keeps these at full rate alongside the shader field.
# =============================================================================

# --- RECORDS -----------------------------------------------------------------
# id -> best value. Scores are "higher is better"; the sweep's clear times are
# stored through the same helper with lower_is_better=True.
default persistent.ag_records = {}

# Snapshot of the last finished run, read by the results card AFTER the game
# object has been dropped (same contract as Kotonoha's kt_last_*: the labels
# below never touch fields on a live game).
default ag_last_title = "ARCADE"
default ag_last_outcome = "-"
default ag_last_rows = []
default ag_last_accent = "#ffb454"

# Which cabinet the retry loop is running, and its variant (the sweep's board
# size). Set by ag_play before it jumps into the loop.
default ag_cur_kind = "snake"
default ag_cur_variant = None


init -1 python:
    import math
    import random

    # --- clock ---------------------------------------------------------------
    # 60Hz fixed timestep. AG_MAX_CATCHUP caps how much simulation one long
    # hitch may run in a single frame: without it, a 2-second stall (a load, a
    # window drag) would fire 120 ticks at once and teleport everything.
    AG_TICK = 1.0 / 60.0
    AG_MAX_CATCHUP = 5

    AG_W = 1280
    AG_H = 720

    # --- type ----------------------------------------------------------------
    AG_FONT = "assets/fonts/SF Automaton Extended.ttf"   # display / headings
    AG_FONT_UI = "assets/fonts/NovaSquare-Regular.ttf"   # readouts / body
    AG_INK = "#f7f0e6"
    AG_DIM = "#a99fc4"
    AG_FAINT = "#6f668c"
    AG_BACK = "#0a0713"

    # --- SFX -----------------------------------------------------------------
    # Same arrangement as the boss fight's registry (battle_logic.rpy) and
    # Kotonoha's KT_SFX: a name -> (path, relative volume) table played onto a
    # small pool of channels. This is the sanctioned exception to the
    # "no raw paths, always an audio.* alias" rule (def_audio.rpy) -- the table
    # IS the definition system, and nothing here is played by a `play`
    # statement. Cues are shared across all four cabinets on purpose: one
    # vocabulary makes the originals sound like one machine.
    AG_SFX_DIR = "assets/audio/sfx/msbf/"
    AG_TH_DIR = "assets/audio/sfx/touhou/"
    AG_SFX = {
        "ui_move":  (AG_SFX_DIR + "uiblip.wav", 0.55),
        "ui_ok":    (AG_SFX_DIR + "ui_accept.wav", 0.7),
        "ui_no":    (AG_SFX_DIR + "ui_denied.wav", 0.6),
        "pause":    (AG_TH_DIR + "se_pause.wav", 0.8),
        "pickup":   (AG_TH_DIR + "se_item00.wav", 0.75),
        "bonus":    (AG_TH_DIR + "se_cardget.wav", 0.7),
        "chain":    (AG_TH_DIR + "se_kira00.wav", 0.6),
        "spoil":    (AG_SFX_DIR + "debuff.wav", 0.7),
        "burn":     (AG_SFX_DIR + "buff.wav", 0.6),
        "bounce":   (AG_TH_DIR + "se_tan01.wav", 0.6),
        "crack":    (AG_TH_DIR + "se_tan00.wav", 0.6),
        "smash":    (AG_TH_DIR + "se_enep00.wav", 0.6),
        "shoot":    (AG_TH_DIR + "se_plst00.wav", 0.5),
        "power":    (AG_TH_DIR + "se_powerup.wav", 0.7),
        "serve":    (AG_TH_DIR + "se_ch00.wav", 0.7),
        "rotate":   (AG_TH_DIR + "se_select00.wav", 0.5),
        "lock":     (AG_TH_DIR + "se_ok00.wav", 0.6),
        "line":     (AG_TH_DIR + "se_kira01.wav", 0.75),
        "quad":     (AG_TH_DIR + "se_cardget.wav", 0.85),
        "rise":     (AG_SFX_DIR + "resist.wav", 0.7),
        "reveal":   (AG_TH_DIR + "se_ch01.wav", 0.6),
        "flag":     (AG_TH_DIR + "se_tan02.wav", 0.6),
        "deny":     (AG_TH_DIR + "se_invalid.wav", 0.6),
        "boom":     (AG_SFX_DIR + "explode.ogg", 0.85),
        "die":      (AG_TH_DIR + "se_pldead00.wav", 0.8),
        "over":     (AG_SFX_DIR + "down.wav", 0.8),
        "clear":    (AG_SFX_DIR + "victory.wav", 0.8),
        "level":    (AG_SFX_DIR + "phase.wav", 0.75),
    }

    # Eight channels: enough that a line clear, a lock and three UI blips in the
    # same tick all ring out. Allocation goes through msbf_pick_pool_channel,
    # which takes an IDLE channel rather than blindly rotating onto a live cue.
    AG_SFX_POOL = ["ag_sfx_%d" % i for i in range(8)]
    for _ag_ch in AG_SFX_POOL:
        if not renpy.music.channel_defined(_ag_ch):
            renpy.music.register_channel(_ag_ch, mixer="sfx", loop=False)

    def ag_se(name, volume_scale=1.0):
        """Play one cabinet cue. Unknown names are silently ignored so a game
        can name a sound it has not been given yet without crashing a run."""
        entry = AG_SFX.get(name)
        if not entry:
            return
        try:
            channel = msbf_pick_pool_channel(AG_SFX_POOL, "cursor", ag_se)
            if channel is None:
                return
            renpy.sound.play(entry[0], channel=channel,
                            relative_volume=entry[1] * volume_scale)
        except Exception:
            pass
    ag_se.cursor = 0

    def ag_stop_sfx(fadeout=0.0):
        """Silence the pool on the way out so nothing rings over the results."""
        for channel in AG_SFX_POOL:
            try:
                renpy.music.stop(channel=channel, fadeout=fadeout)
            except Exception:
                pass

    # --- small math ----------------------------------------------------------
    def ag_clamp(v, lo, hi):
        return lo if v < lo else (hi if v > hi else v)

    def ag_mix(a, b, t):
        """Blend two "#rrggbb" strings. Used for gradients along a snake body,
        brick rows, cell heat -- anywhere a palette wants to be generated
        instead of typed out."""
        try:
            a = a.lstrip("#")
            b = b.lstrip("#")
            out = []
            for i in (0, 2, 4):
                ca = int(a[i:i + 2], 16)
                cb = int(b[i:i + 2], 16)
                out.append(int(round(ca + (cb - ca) * t)))
            return "#%02x%02x%02x" % tuple(max(0, min(255, v)) for v in out)
        except Exception:
            return "#" + a

    def ag_num(n):
        """Thousands-separated score string."""
        try:
            return format(int(n), ",")
        except Exception:
            return str(n)

    def ag_time(seconds):
        """M:SS readout for the sweep's clock and the results card."""
        try:
            s = int(seconds)
            return "%d:%02d" % (s // 60, s % 60)
        except Exception:
            return "-"

    # --- records -------------------------------------------------------------
    def ag_best(key, default=0):
        try:
            return (persistent.ag_records or {}).get(key, default)
        except Exception:
            return default

    def ag_set_best(key, value, lower_is_better=False):
        """Record `value` under `key` if it beats what is stored; return whether
        it did (games use that to flash a NEW RECORD banner).

        The dict is COPIED, written, and REASSIGNED rather than mutated in
        place. Matsu'Py pickles persistent wholesale so an in-place mutation
        would in fact be saved -- but assignment is the form that is
        unambiguously correct under every path (including a persistent merge
        between two saves), and it costs one dict copy per finished run.
        """
        try:
            records = dict(persistent.ag_records or {})
        except Exception:
            records = {}
        old = records.get(key)
        if old is None:
            better = True
        elif lower_is_better:
            better = value < old
        else:
            better = value > old
        if better:
            records[key] = value
            persistent.ag_records = records
        return better


# =============================================================================
# THE CANVAS
# A thin drawing surface handed to game.draw() once a frame. Two layers of
# caching sit under every call:
#   AGCanvas._disp  displayables, built once and kept between frames
#   self.memo       renpy.Render objects, reused within THIS frame only
# The second is why the memo is an instance field and the first a class field:
# Render objects are frame products and must never outlive the frame that made
# them (the same rule KTStage documents), while a Solid or a Text is immutable
# and worth keeping forever.
# =============================================================================
init -1 python:

    class AGCanvas(object):

        _disp = {}          # cache key -> displayable
        _DISP_CAP = 1400    # soft cap; cleared wholesale when exceeded

        def __init__(self, rv, st, at):
            self.rv = rv
            self.st = st
            self.at = at
            self.memo = {}

        @staticmethod
        def cached(key, builder):
            d = AGCanvas._disp.get(key)
            if d is None:
                if len(AGCanvas._disp) > AGCanvas._DISP_CAP:
                    AGCanvas._disp.clear()
                d = builder()
                AGCanvas._disp[key] = d
            return d

        def _tex(self, key, disp, w, h):
            entry = self.memo.get(key)
            if entry is None:
                r = renpy.render(disp, w, h, self.st, self.at)
                self.rv.depends_on(r)
                entry = (r, r.get_size())
                self.memo[key] = entry
            return entry

        # ---- primitives -----------------------------------------------------

        def rect(self, color, x, y, w, h, sub=False):
            """Filled rectangle. `sub` blits at subpixel precision, for things
            that move continuously (a ball, a paddle) rather than on a grid."""
            w = int(round(w))
            h = int(round(h))
            if w <= 0 or h <= 0:
                return
            key = ("r", color, w, h)
            d = AGCanvas.cached(("solid", color), lambda: Solid(color))
            r, _ = self._tex(key, d, w, h)
            if sub:
                self.rv.subpixel_blit(r, (x, y))
            else:
                self.rv.blit(r, (int(round(x)), int(round(y))))

        def frame(self, color, x, y, w, h, t=2):
            """Hollow rectangle, drawn as four solids."""
            self.rect(color, x, y, w, t)
            self.rect(color, x, y + h - t, w, t)
            self.rect(color, x, y + t, t, h - 2 * t)
            self.rect(color, x + w - t, y + t, t, h - 2 * t)

        def panel(self, x, y, w, h, top="#1e1742ee", bottom=None, radius=14.0,
                border=0.0, bcolor="#00000000"):
            """A rounded gradient plate -- the same enter_m.arcade_panel shader
            the hub's pages and buttons use, so HUD chrome in a game and chrome
            in the catalog are literally the same surface."""
            w = int(round(w))
            h = int(round(h))
            if w <= 0 or h <= 0:
                return
            key = ("p", w, h, top, bottom, radius, border, bcolor)
            d = AGCanvas.cached(key, lambda: ArcadePanel(
                w, h, top=top, bottom=bottom, radius=radius,
                border=border, border_color=bcolor))
            r, _ = self._tex(key, d, w, h)
            self.rv.blit(r, (int(round(x)), int(round(y))))

        def text(self, s, x, y, size=20, color=None, font=None, bold=False,
                anchor=(0.0, 0.0), alpha=1.0, outline="#00000099", kerning=0.0):
            """Draw a string and return its (w, h). `anchor` is fractional, so
            (0.5, 0.5) centres and (1.0, 0.0) right-aligns."""
            color = color or AG_INK
            font = font or AG_FONT_UI
            a = round(float(alpha), 2)
            key = ("t", s, size, color, font, bold, outline, a, kerning)

            def build():
                kw = dict(size=size, color=color, bold=bold, font=font)
                if kerning:
                    kw["kerning"] = kerning
                if outline:
                    kw["outlines"] = [(2, outline, 0, 0)]
                t = Text(s, **kw)
                if a < 0.999:
                    t = Transform(t, alpha=a)
                return t

            d = AGCanvas.cached(key, build)
            r, (tw, th) = self._tex(key, d, AG_W, AG_H)
            self.rv.blit(r, (int(round(x - tw * anchor[0])),
                            int(round(y - th * anchor[1]))))
            return (tw, th)

        def measure(self, key, builder, w=AG_W, h=AG_H):
            """The (w, h) a cached displayable WOULD occupy, without blitting it.

            Rendering is the only way to learn a Text's real extent, and a game
            that has to know one before it can place or hit-test it would
            otherwise be stuck estimating from character counts. The render goes
            through the same per-frame memo as disp(), so measuring a thing and
            then drawing it costs exactly one render, not two.
            """
            d = AGCanvas.cached(key, builder)
            _r, size = self._tex(key, d, w, h)
            return size

        def disp(self, key, builder, x, y, w=256, h=256, anchor=(0.0, 0.0),
                sub=False):
            """Blit an arbitrary cached displayable. `builder` must close over
            immutable values only -- it runs once, on the first miss."""
            d = AGCanvas.cached(key, builder)
            r, (dw, dh) = self._tex(key, d, w, h)
            px = x - dw * anchor[0]
            py = y - dh * anchor[1]
            if sub:
                self.rv.subpixel_blit(r, (px, py))
            else:
                self.rv.blit(r, (int(round(px)), int(round(py))))
            return (dw, dh)

        # ---- composites -----------------------------------------------------

        def cell(self, x, y, size, color, inset=3, radius=0):
            """One grid tile: a dark seat with a lighter face inset into it.
            Every grid game here (snake, the stack, the sweep) draws through
            this so they share a physical language."""
            self.rect("#00000055", x, y, size, size)
            if radius:
                self.panel(x + inset, y + inset, size - inset * 2,
                            size - inset * 2, top=color, radius=radius)
            else:
                self.rect(color, x + inset, y + inset,
                        size - inset * 2, size - inset * 2)

        def bar(self, x, y, w, h, frac, color, back="#ffffff14"):
            """Horizontal meter."""
            self.rect(back, x, y, w, h)
            f = ag_clamp(float(frac), 0.0, 1.0)
            if f > 0.0:
                self.rect(color, x, y, max(2, int(round(w * f))), h)

        def readout(self, label, value, x, y, size=30, color=None,
                    anchor=(0.0, 0.0), accent=None):
            """A HUD stat: small caps label over a big value. Returns the height
            used so callers can stack them without hard-coding offsets.

            The VALUE is set in the UI face, not the display face: the display
            font draws a 1 as a bare vertical bar, so "1,409" reads as "I,409"
            and a swept board's 1s read like its 3s. Titles keep the display
            face, where that styling is the whole point.
            """
            self.text(label, x, y, size=12, color=(accent or AG_FAINT),
                        font=AG_FONT_UI, bold=True, kerning=2.0, anchor=anchor)
            self.text(value, x, y + 16, size=size, color=(color or AG_INK),
                        font=AG_FONT_UI, bold=True, anchor=anchor)
            return 16 + size + 6

        # ---- the shared HUD grid --------------------------------------------
        # Every cabinet lays its chrome out on the SAME grid, for two reasons.
        # One: four games that read as one machine. Two, and the reason this
        # lives in the framework rather than being copied four times --
        # anchoring HUD text to a PLAYFIELD edge is a trap. The sweep's board
        # changes size with the difficulty, so a title pinned to its left edge
        # and readouts pinned to its right edge walked into each other on the
        # small board. Header left, stats right, legend centred at the foot, all
        # at fixed screen coordinates no playfield can push around.

        AG_HUD_TOP = 30
        AG_HUD_LEFT = 60
        AG_HUD_RIGHT = 1220
        AG_LEGEND_Y = 696

        def header(self, title, subtitle, accent):
            self.text(title, AGCanvas.AG_HUD_LEFT, AGCanvas.AG_HUD_TOP,
                        size=30, color=AG_INK, font=AG_FONT, bold=True)
            if subtitle:
                self.text(subtitle, AGCanvas.AG_HUD_LEFT,
                        AGCanvas.AG_HUD_TOP + 38, size=12, color=accent,
                        bold=True, kerning=3.0)

        def stat_row(self, items, y=None, right=None, size=28, gap=32):
            """A right-aligned row of (label, value[, colour]) readouts.

            Laid out from the right edge LEFTWARDS, measuring each column as it
            goes (canvas.text returns what it drew), so a five-figure score
            pushes the row further left instead of colliding with its
            neighbour. Returns the row's left edge.
            """
            x = AGCanvas.AG_HUD_RIGHT if right is None else right
            y = AGCanvas.AG_HUD_TOP if y is None else y
            for item in reversed(items):
                label = item[0]
                value = item[1]
                color = item[2] if len(item) > 2 else AG_INK
                vw, _vh = self.text(value, x, y + 16, size=size, color=color,
                        font=AG_FONT_UI, bold=True, anchor=(1.0, 0.0))
                lw, _lh = self.text(label, x, y, size=12, color=AG_FAINT,
                        bold=True, kerning=2.0, anchor=(1.0, 0.0))
                x -= max(vw, lw) + gap
            return x

        def legend(self, text, y=None):
            """The one-line control reminder each cabinet carries at the foot of
            the screen. Centred, so it never has to negotiate with anything
            anchored to a playfield."""
            self.text(text, AG_W / 2,
                        AGCanvas.AG_LEGEND_Y if y is None else y, size=12,
                        color=AG_FAINT, kerning=1.5, anchor=(0.5, 0.5))


# =============================================================================
# THE GAME BASE
# Rules and state only: no displayables, no Matsu'Py drawing, no knowledge of the
# screen. Subclasses override step()/draw() and, if they want more than a score
# on the results card, rows()/outcome().
# =============================================================================
init -1 python:

    class AGGame(object):

        # --- identity (overridden per cabinet) --------------------------------
        KIND = "game"
        TITLE = "GAME"
        ACCENT = "#ffb454"
        # MOUSE cabinets keep right-click for themselves (the sweep flags with
        # it), so the screen does not bind it to pause.
        MOUSE = False
        # Shown on the controls card and in the pause overlay.
        CONTROLS = []

        def __init__(self, variant=None):
            self.variant = variant
            self.tick = 0
            self.paused = False
            self.result = None
            self.score = 0
            self.new_record = False
            # Feeds MSBFKeyLatch the real key events (AGStage.event does the
            # handing over); see the SHARED KEY LATCH block in battle_logic.rpy.
            self.keys = MSBFKeyLatch()
            self._edges = {}

        # ---- contract -------------------------------------------------------

        def step(self):
            """Advance exactly 1/60s of simulation."""

        def draw(self, c):
            """Paint the current state onto the canvas."""

        def on_event(self, ev, x, y):
            """Raw Matsu'Py event (mouse games only). Never return a value."""

        # ---- input ----------------------------------------------------------

        def poll(self):
            """SDL keyboard state for this tick, or None when another window
            owns the keyboard (in which case everything reads as released, so a
            game cannot keep moving while the player is elsewhere)."""
            try:
                import pygame_sdl2 as pg
                keys = pg.key.get_pressed()
            except Exception:
                return None
            if not self.keys.focused():
                self.keys.clear()
                self._edges = {}
                return None
            return keys

        def held(self, keys, *codes):
            """True while any of `codes` is genuinely down."""
            if keys is None:
                return False
            return self.keys.pressed(keys, *codes)

        def tapped(self, keys, name, *codes):
            """Rising edge of `codes`, remembered under `name`.

            MUST be called exactly once per tick per name -- it stores the
            previous state as a side effect, so calling it twice in a tick eats
            the press and calling it zero times makes the next press look like a
            hold. Every caller here does it in one input block at the top of
            step().
            """
            down = self.held(keys, *codes)
            was = self._edges.get(name, False)
            self._edges[name] = down
            return down and not was

        # ---- lifecycle ------------------------------------------------------

        def toggle_pause(self):
            if self.result is not None:
                return
            self.paused = not self.paused
            ag_se("pause")
            # The screen's `if game.paused` bindings (Q to quit) only re-evaluate
            # when the interaction restarts.
            renpy.restart_interaction()

        def give_up(self):
            if self.result is None:
                self.paused = False
                self.finish("quit")
                renpy.restart_interaction()

        def finish(self, kind):
            """End the run. Records are written, the results card's data is
            snapshotted into store variables, and self.result is set -- which
            the screen's slow poll timer notices and turns into the return value
            of `call screen`."""
            if self.result is not None:
                return
            try:
                self.record()
            except Exception:
                pass
            store.ag_last_title = self.TITLE
            store.ag_last_outcome = self.outcome(kind)
            store.ag_last_accent = self.card_accent(kind)
            try:
                store.ag_last_rows = [(str(a), str(b)) for a, b in self.rows(kind)]
            except Exception:
                store.ag_last_rows = [("SCORE", ag_num(self.score))]

            # MATSUCOINS. This is the one place every cabinet run ends, so it is
            # the one place the payout has to be wired -- a new cabinet earns
            # coins on the day it is registered without touching this file, and
            # without its author having to know the currency exists.
            #
            # record() has already run above, so self.new_record is settled and
            # the record bonus is judged against the score that was actually
            # banked. Wrapped like everything else here: a currency fault must
            # cost the player their coins, never their results card.
            try:
                _ag_coins = mc_award_run(self.KIND, self.TITLE, self.score,
                                        kind, self.new_record)
                if _ag_coins:
                    store.ag_last_rows.append(
                        ("MATSUCOINS EARNED", "+%s" % mc_num(_ag_coins)))
            except Exception:
                pass

            self.result = kind

        # ---- results (override for anything richer than a score) ------------

        def record(self):
            """Write high scores. Set self.new_record so draw() can say so."""
            if self.score:
                self.new_record = ag_set_best(self.KIND + "_score", self.score)

        def outcome(self, kind):
            return "ABANDONED" if kind == "quit" else "RUN COMPLETE"

        def card_accent(self, kind):
            return "#8f86a8" if kind == "quit" else self.ACCENT

        def rows(self, kind):
            return [("SCORE", ag_num(self.score)),
                    ("BEST", ag_num(max(self.score, ag_best(self.KIND + "_score"))))]


# =============================================================================
# THE STAGE  (creator-defined displayable)
# Owns the clock, the canvas and the pause overlay. One instance per run.
# =============================================================================
init -1 python:

    class AGStage(renpy.Displayable):

        def __init__(self, game, **kwargs):
            super(AGStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0

        def event(self, ev, x, y, st):
            # The latch is fed first and unconditionally: it is what unsticks a
            # key whose release was swallowed. Then the game gets the raw event
            # (mouse cabinets read it; keyboard ones ignore it).
            g = self.game
            g.keys.handle_event(ev)
            if g.result is None and not g.paused:
                try:
                    g.on_event(ev, x, y)
                except Exception:
                    pass
            # Always None: returning a value here would end the interaction and
            # steal the screen's own key bindings.
            return None

        def render(self, width, height, st, at):
            g = self.game

            # Fixed timestep. st is wall time; the accumulator holds the
            # leftover fraction so the sim advances in exact 1/60s slices no
            # matter how unevenly render() is called.
            if self.last_st is None:
                self.last_st = st
            dt = st - self.last_st
            self.last_st = st
            if dt < 0.0:
                dt = 0.0
            elif dt > 0.25:
                dt = 0.25

            if g.paused or g.result is not None:
                self.acc = 0.0
            else:
                self.acc += dt
                steps = 0
                while self.acc >= AG_TICK and steps < AG_MAX_CATCHUP:
                    g.tick += 1
                    g.step()
                    self.acc -= AG_TICK
                    steps += 1
                if steps >= AG_MAX_CATCHUP:
                    # Ran out of catch-up budget: drop the backlog rather than
                    # spiral (each frame would otherwise owe more than the last).
                    self.acc = 0.0

            rv = renpy.Render(AG_W, AG_H)
            c = AGCanvas(rv, st, at)

            try:
                g.draw(c)
            except Exception:
                # A drawing bug should not strand the player in a dead frame
                # with no way out; the pause overlay and Escape still work.
                c.text("DISPLAY FAULT -- ESC TO PAUSE, Q TO QUIT",
                        AG_W / 2, AG_H / 2, size=22, color="#e0455e",
                        anchor=(0.5, 0.5))
                raise

            if g.paused:
                self._pause_overlay(c, g)

            # A realtime game wants every frame it can get -- WHILE IT IS
            # RUNNING. A paused or finished cabinet is a still picture, and
            # asking for frames at 0 held the whole stack (this render, the
            # ArcadePanel shader behind it, every cached texture blit) at the
            # monitor's full rate for as long as the player left the pause card
            # up. On a 240Hz panel that is a static overlay costing 240 full
            # redraws a second.
            #
            # Dropping the request is safe because the screen -- not this
            # displayable -- owns the way out: ag_screen binds K_ESCAPE and
            # mouseup_3 to game.toggle_pause and branches on `game.paused`, so
            # unpausing restarts the interaction and rebuilds the stage. This
            # is the same guard the four Archivist Invasions stages and
            # tsubaki_soul.rpy already use; this cabinet was the outlier.
            if g.result is None and not g.paused:
                renpy.redraw(self, 0)
            return rv

        def _pause_overlay(self, c, g):
            c.rect("#0a0713cc", 0, 0, AG_W, AG_H)
            rows = list(g.CONTROLS)
            h = 236 + 30 * len(rows)
            y0 = (AG_H - h) / 2
            c.panel(390, y0, 500, h, top="#241b46f4", bottom="#120c24f8",
                    radius=20, border=1.5, bcolor=(g.ACCENT + "66"))
            c.text("PAUSED", 640, y0 + 46, size=44, color=AG_INK,
                    font=AG_FONT, bold=True, anchor=(0.5, 0.5))
            c.text(g.TITLE, 640, y0 + 80, size=13, color=g.ACCENT,
                    bold=True, kerning=3.0, anchor=(0.5, 0.5))
            c.rect(g.ACCENT + "55", 470, y0 + 104, 340, 1)

            y = y0 + 128
            for keyname, what in rows:
                c.text(keyname, 610, y, size=15, color=AG_INK, bold=True,
                        anchor=(1.0, 0.0))
                c.text(what, 634, y, size=15, color=AG_DIM, anchor=(0.0, 0.0))
                y += 30

            y += 14
            c.rect("#ffffff18", 470, y, 340, 1)
            c.text("ESC  RESUME", 604, y + 20, size=15, color=AG_DIM,
                    anchor=(1.0, 0.0))
            c.text("Q  GIVE UP", 676, y + 20, size=15, color="#e0455e",
                    anchor=(0.0, 0.0))


    # Screen-poll helper: a non-None return ends the interaction with that value
    # (Function() action semantics), which is how a game hands its outcome back
    # to the script without restarting the interaction 4x/second.
    def ag_poll_result(game):
        return game.result


# =============================================================================
# THE REGISTRY
# One entry per cabinet, filled by each game file's ag_register() call. The hub
# tile table does NOT read this (it is built in arcade.rpy, which loads first);
# tiles name their cabinet by string and everything else is resolved at runtime.
# =============================================================================
init -1 python:

    AG_GAMES = {}
    _ag_cover_cache = {}

    def ag_register(kind, factory, title, accent, blurb, controls, music,
                    cover=None, variants=None, variant_prompt=None):
        """Declare a cabinet.

        kind      : stable id; also the persistent record prefix.
        factory   : callable(variant) -> AGGame.
        title     : catalog title, also the results-card heading.
        accent    : per-cabinet colour, used by the field, chrome and cover.
        blurb     : one line on the controls card.
        controls  : [(keys, what)] for the controls card and pause overlay.
        music     : an audio.* alias (never a raw path -- def_audio.rpy).
        cover     : callable() -> displayable, the procedurally drawn box art.
        variants  : optional [(id, name, note)] for cabinets that ask first.
        variant_prompt : the line under the title on that card. The default
                    ("Pick a board.") is the sweep's; a cabinet whose variants
                    are opponents rather than boards says so instead.
        """
        AG_GAMES[kind] = {
            "factory": factory, "title": title, "accent": accent,
            "blurb": blurb, "controls": controls, "music": music,
            "cover": cover, "variants": variants,
            "variant_prompt": variant_prompt,
        }

    def ag_spec(kind):
        return AG_GAMES.get(kind, {})

    def ag_make_game(kind, variant=None):
        spec = AG_GAMES.get(kind)
        if not spec:
            return None
        return spec["factory"](variant)

    def ag_music_for(kind):
        return AG_GAMES.get(kind, {}).get("music")

    def ag_cover(kind):
        """The shelf cover for a cabinet, built once and kept.

        Called from arcade_art_for() on every hub screen rebuild -- which is
        every frame a card is hovered -- so it must not rebuild displayables.
        """
        d = _ag_cover_cache.get(kind)
        if d is None:
            spec = AG_GAMES.get(kind) or {}
            builder = spec.get("cover")
            if builder is None:
                return None
            d = builder()
            _ag_cover_cache[kind] = d
        return d

    # --- cover helpers -------------------------------------------------------
    # Every original's box art is drawn here rather than painted, out of the
    # same parts as its playfield, so the shelf reads as one product line. A
    # real PNG dropped at addons/Arcade/art/<slug>.png still wins over these
    # (see arcade_art_for) -- these are the default cover, not a lock.
    AG_COVER_SIZE = 320

    def ag_cover_base(accent, dark="#0b0818"):
        """The shared cover ground: deep plate, accent glow, corner ticks."""
        s = AG_COVER_SIZE
        return [
            Solid(dark, xysize=(s, s)),
            Transform(Solid(ag_mix(dark, accent, 0.22), xysize=(s, 150)),
                        pos=(0, 170)),
            Transform(Solid(accent + "26", xysize=(s, 3)), pos=(0, 168)),
        ]

    def ag_cover_title(text_top, text_main, accent):
        """The wordless-card rule is the STORY modes' (their covers are painted
        art). The originals are generated, so they carry their own small
        nameplate -- it is the only thing that keeps four procedural cards from
        reading as four swatches."""
        return [
            Transform(Text(text_top, font=AG_FONT_UI, size=13, bold=True,
                            color=accent, kerning=3.0), pos=(22, 232)),
            Transform(Text(text_main, font=AG_FONT, size=30, bold=True,
                            color="#f7f0e6", outlines=[(2, "#00000099", 0, 0)],
                            xmaximum=280), pos=(20, 252)),
        ]


# =============================================================================
# SCREENS
# =============================================================================

# --- THE GAMEPLAY SCREEN -----------------------------------------------------
# One screen for every original. It owns nothing but the field, the stage and
# three key bindings; all HUD, all overlays and all feedback are drawn by the
# game itself inside AGStage.
#
# BINDINGS, and why they are exactly these:
#   K_ESCAPE      pause. Bound directly rather than through "game_menu" because
#                 Escape is a MEMBER of the game_menu keysym set -- binding both
#                 would fire two handlers for one press and toggle pause twice.
#                 The save/load menu itself is already disabled for the run
#                 (_game_menu_screen = None, set by the launch label).
#   mouseup_3     pause as well, but ONLY on keyboard cabinets. The sweep flags
#                 incidents with right-click and must keep it.
#   K_q           quit, live only while paused, so a mistyped key mid-run can
#                 never throw away a good score.
screen ag_screen(game):
    modal True
    zorder 10
    use enter_m_input_lock()

    # The same gradient field the hub draws behind its shelf, tinted to this
    # cabinet. Static: one shader quad, no per-frame cost.
    add ArcadeField(game.ACCENT)
    add AGStage(game)

    key "K_ESCAPE" action Function(game.toggle_pause)
    if not game.MOUSE:
        key "mouseup_3" action Function(game.toggle_pause)
    if game.paused:
        key "K_q" action Function(game.give_up)

    # _update_screens=False: a None poll must NOT restart the interaction, which
    # would rebuild the stage 4x/sec and bleed the simulation's accumulator.
    timer 0.25 repeat True action Function(ag_poll_result, game, _update_screens=False)


# --- CONTROLS CARD -----------------------------------------------------------
# Shown once before a run (not on retry). Doubles as the "are you sure" -- Escape
# here goes back to the shelf without starting anything.
screen ag_controls_card(kind):
    modal True
    zorder 20
    use enter_m_input_lock()

    python:
        _ag_spec = ag_spec(kind)
        _ag_accent = _ag_spec.get("accent", "#ffb454")
        _ag_rows = _ag_spec.get("controls", [])
        _ag_best = ag_best(kind + "_score", 0)
        _ag_card_h = 320 + 34 * len(_ag_rows)

    add ArcadeField(_ag_accent)
    add Solid("#0a071388")

    fixed:
        xysize (640, _ag_card_h)
        align (0.5, 0.5)
        at arcade_pop

        add ArcadePanel(640, _ag_card_h, top="#241b46f2", bottom="#120c24f7",
                        radius=20, border=1.5, border_color=(_ag_accent + "66"))

        vbox:
            xalign 0.5
            ypos 34
            spacing 6
            text "MATSUCOM ORIGINAL" style "arcade_kicker" xalign 0.5
            text _ag_spec.get("title", "GAME") style "arcade_panel_title" xalign 0.5
            text _ag_spec.get("blurb", ""):
                style "arcade_panel_sub"
                xalign 0.5
                xsize 540
                text_align 0.5

        vbox:
            xpos 96
            ypos 176
            spacing 12
            for _k, _what in _ag_rows:
                fixed:
                    xsize 448
                    ysize 22
                    text _k:
                        style "arcade_chip_dim"
                        size 15
                        color _ag_accent
                        xpos 0
                        yalign 0.5
                    text _what:
                        style "arcade_row_label"
                        size 15
                        xanchor 1.0
                        xpos 448
                        yalign 0.5

        vbox:
            xalign 0.5
            yalign 1.0
            yoffset -28
            spacing 12
            if _ag_best:
                text ("CABINET BEST   %s" % ag_num(_ag_best)):
                    style "arcade_meta"
                    xalign 0.5
            hbox:
                xalign 0.5
                spacing 16
                button:
                    style "arcade_play_button"
                    xsize 200
                    ysize 56
                    action Return("start")
                    background ArcadePanel(200, 56, top=_arcade_mix(_ag_accent, "#140f28", 0.34), bottom=_arcade_mix(_ag_accent, "#140f28", 0.62), radius=11, border=1.5, border_color=(_ag_accent + "cc"))
                    hover_background ArcadePanel(200, 56, top=_arcade_mix(_ag_accent, "#ffffff", 0.18), bottom=_arcade_mix(_ag_accent, "#140f28", 0.30), radius=11, border=2.5, border_color=_arcade_mix(_ag_accent, "#ffffff", 0.45))
                    text "START":
                        style "arcade_play_text"
                        size 22
                        align (0.5, 0.5)
                button:
                    style "arcade_play_button"
                    xsize 150
                    ysize 56
                    action Return("back")
                    background ArcadePanel(150, 56, top="#2a2148", bottom="#1c1636", radius=11, border=1.0, border_color="#ffffff22")
                    hover_background ArcadePanel(150, 56, top="#43336a", bottom="#2a1f4a", radius=11, border=2.0, border_color="#ffffff55")
                    text "BACK":
                        style "arcade_play_text"
                        size 18
                        color "#c9c0dc"
                        align (0.5, 0.5)

    key "K_RETURN" action Return("start")
    key "K_KP_ENTER" action Return("start")
    key "K_z" action Return("start")
    key "K_ESCAPE" action Return("back")


# --- VARIANT CARD ------------------------------------------------------------
# Generic version of the hub's Kotonoha picker, driven by a cabinet's
# spec["variants"] = [(id, name, note)]. Returns the chosen id, or None on
# Escape. Only cabinets that declare variants ever see it.
screen ag_variant_card(kind):
    modal True
    zorder 20
    use enter_m_input_lock()

    python:
        _ag_spec = ag_spec(kind)
        _ag_accent = _ag_spec.get("accent", "#ffb454")
        _ag_vars = _ag_spec.get("variants") or []
        _ag_prompt = _ag_spec.get("variant_prompt") or _("Pick a board.")
        _ag_card_h = 210 + 78 * len(_ag_vars)

    add ArcadeField(_ag_accent)
    add Solid("#0a071388")

    fixed:
        xysize (640, _ag_card_h)
        align (0.5, 0.5)
        at arcade_pop

        add ArcadePanel(640, _ag_card_h, top="#241b46f2", bottom="#120c24f7",
                        radius=20, border=1.5, border_color=(_ag_accent + "66"))

        vbox:
            xalign 0.5
            ypos 32
            spacing 6
            text _ag_spec.get("title", "GAME") style "arcade_panel_title" xalign 0.5
            text _ag_prompt style "arcade_panel_sub" xalign 0.5

        vbox:
            xalign 0.5
            ypos 128
            spacing 12
            for _vid, _vname, _vnote in _ag_vars:
                button:
                    style "arcade_variant_button"
                    xsize 520
                    background ArcadePanel(520, 64, top="#2a2148", bottom="#1c1636", radius=12, border=1.0, border_color=(_ag_accent + "44"))
                    hover_background ArcadePanel(520, 64, top="#43336a", bottom="#2a1f4a", radius=12, border=2.0, border_color=(_ag_accent + "cc"))
                    action Return(_vid)
                    vbox:
                        spacing 2
                        yalign 0.5
                        text _vname style "arcade_variant_head"
                        text _vnote style "arcade_variant_sub"

    key "K_ESCAPE" action Return(None)


# =============================================================================
# LAUNCH
# ag_play is entered ONLY through renpy.call_in_new_context (the tile action),
# which is why it can take parameters and still `return` its way out of the
# context at the end -- there is no call frame above it to fall back into.
# Parameters are namespaced ag_* because label parameters assign into the GLOBAL
# store; a bare `kind` or `variant` would clobber whatever else owns that name.
# =============================================================================
label ag_play(ag_kind="snake", ag_variant=None):
    $ arcade_active = True
    $ ag_cur_kind = ag_kind
    $ ag_cur_variant = ag_variant
    call arcade_launch_prep from _call_arcade_launch_prep_ag

    # Cabinets that ask a question first (board size, difficulty).
    if ag_spec(ag_cur_kind).get("variants") and ag_cur_variant is None:
        call screen ag_variant_card(ag_cur_kind)
        $ ag_cur_variant = _return
        if ag_cur_variant is None:
            jump arcade_return

    call screen ag_controls_card(ag_cur_kind)
    if _return != "start":
        jump arcade_return
    jump ag_play_loop

# The retry loop. Retry re-enters HERE, so it skips the controls card and keeps
# the chosen variant -- one keypress from a finished run back into a fresh one.
label ag_play_loop:
    window hide
    # Rollback through a live realtime game is nonsense: it would restore script
    # state without restoring the input timing the player just performed.
    $ renpy.block_rollback()

    $ ag_game = ag_make_game(ag_cur_kind, ag_cur_variant)

    # Hide the VN affordances for the duration. The pause overlay is drawn by
    # AGStage, and the game menu is disabled so Save/Load cannot open over a
    # mutable 60Hz state.
    $ _ag_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ _ag_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None

    scene black
    $ renpy.music.play(ag_music_for(ag_cur_kind), loop=True, fadein=0)
    call screen ag_screen(ag_game)

    $ ag_game = None
    $ quick_menu = _ag_prev_quick_menu
    $ _game_menu_screen = _ag_prev_game_menu
    $ ag_stop_sfx(0.2)
    stop music fadeout 1.0

    # Everything the card shows was snapshotted by AGGame.finish() before the
    # object was dropped; nothing below reads the game.
    call screen arcade_result(ag_last_title, ag_last_outcome, ag_last_rows, ag_last_accent)
    if _return == "retry":
        jump ag_play_loop
    jump arcade_return
