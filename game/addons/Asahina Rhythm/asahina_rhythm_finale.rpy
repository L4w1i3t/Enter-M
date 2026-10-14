# Asarhythm's endings and the wipes between its screens.
#
# ARWipe is the one wipe every Asarhythm screen uses. Slanted bands sweep in
# from the left until the screen is covered, the screen hands over, and the
# next screen sweeps the same bands off to the right. A covering wipe returns
# its value from event() once it has closed, so a screen always leaves on a
# covered frame, never on a timer that a stalled draw could outrun.
#
# ARFinale is how a song ends on the stage: the fail sequence (a hit stop, a
# burst from the player, the lanes collapsing, then the wipe) and the shorter
# clear outro. The stage calls into it from asahina_rhythm.rpy. Nothing here
# uses a matrixcolor, for the reason given at the top of asahina_rhythm_fx.rpy.
#
# The results screens and their backdrop effects are at the bottom.

define -50 audio.asarhythm_fail = "assets/audio/sfx/touhou/se_pldead00.wav"  # the fail burst

init -1 python:
    AR_SFX_CHANNEL = "asahina_rhythm_sfx"
    if not renpy.music.channel_defined(AR_SFX_CHANNEL):
        renpy.music.register_channel(AR_SFX_CHANNEL, mixer="sfx", loop=False, stop_on_mute=False)

    # ---- wipes ---------------------------------------------------------------
    AR_WIPE_TIME = .46          # One sweep, covering or clearing.
    AR_WIPE_HOLD = .10          # A covered screen waits this long before it hands over.
    AR_WIPE_TITLE_HOLD = .34    # The stage holds the song's title card this long.
    AR_WIPE_SLANT = 250.0       # How far a band's top runs ahead of its foot, in px.
    AR_WIPE_STAGGER = (0.0, .075, .15)  # The two slivers lead the plate by these fractions of a sweep.
    # (leading sliver, second sliver, plate). An uncover must use its cover's palette.
    AR_WIPE_PALETTES = {
        "enter": ("#f06ba8", "#5fd8e8", "#160f24"),
        "clear": ("#ffcf5a", "#f06ba8", "#1a0f2e"),
        "fail": ("#fa698b", "#6b3a8f", "#0c0716"),
    }
    AR_INPUT_EVENTS = frozenset(getattr(ar_pg, name) for name in (
        "KEYDOWN", "KEYUP", "MOUSEBUTTONDOWN", "MOUSEBUTTONUP", "MOUSEWHEEL", "TEXTINPUT",
        "JOYBUTTONDOWN", "JOYBUTTONUP", "CONTROLLERBUTTONDOWN", "CONTROLLERBUTTONUP") if hasattr(ar_pg, name))

    def ar_ease_in_out(t):
        t = max(0.0, min(1.0, t))
        return 4 * t * t * t if t < .5 else 1 - (-2 * t + 2) ** 3 / 2

    def ar_slant_fill(target, solid, left, right, y, height, slant, st, at):
        """Fill ``solid`` between two parallel slanted edges, from row ``y`` down ``height`` px.

        ``left`` and ``right`` are the edges at the band's mid-height; each edge's
        top runs ``slant`` px ahead of its foot. One sheared Render, no texture.
        """
        width = right - left
        if width < .5 or height < .5:
            return
        k = slant / float(height)
        wrap = renpy.Render(width, height)
        # Child (x, y) lands at (x - k*y, y): the top of the band leans right.
        wrap.reverse = renpy.display.matrix.Matrix2D(1.0, -k, 0.0, 1.0)
        wrap.forward = renpy.display.matrix.Matrix2D(1.0, k, 0.0, 1.0)
        wrap.blit(renpy.render(solid, width, height, st, at), (0, 0))
        target.subpixel_blit(wrap, (left + slant * .5, y))

    class ARWipe(renpy.Displayable):
        """A slanted-band wipe. An ``uncover`` wipe starts on its first frame; a ``cover`` waits for arm().

        A cover returns arm()'s value from event() once it has closed and held.
        Both swallow the player's input while they run (unless ``block`` is
        False), and an uncover keeps swallowing it for ``grace`` seconds after
        it clears: keys mashed to skip an ending must not press the next
        screen's buttons.
        """
        def __init__(self, mode="cover", palette="enter", title=None, subtitle=None, hold=0.0,
                     grace=0.0, block=True, **kwargs):
            super(ARWipe, self).__init__(**kwargs)
            self.mode = mode
            self.palette = palette
            self.title, self.subtitle = title, subtitle
            self.hold = hold
            self.grace = grace
            self.block = block
            self.armed = mode == "uncover"
            self.value = None
            self.elapsed = 0.0
            self.last = None
            self.texts = {}
            self.solids = {}

        def arm(self, value, palette=None, title=None, subtitle=None):
            """Start covering. The screen returns ``value`` once the cover has closed."""
            if self.mode != "cover" or self.armed:
                return
            self.armed = True
            self.value = value
            self.palette = palette or self.palette
            self.title, self.subtitle = title, subtitle
            self.elapsed, self.last = 0.0, None
            renpy.redraw(self, 0)

        def length(self):
            if self.mode == "cover":
                return AR_WIPE_TIME + max(AR_WIPE_HOLD, self.hold)
            return self.hold + AR_WIPE_TIME

        @property
        def closed(self):
            return self.mode == "cover" and self.armed and self.elapsed >= self.length()

        @property
        def busy(self):
            """True while the wipe is moving or holding (a cover stays busy once it has closed)."""
            if not self.armed:
                return False
            return self.mode == "cover" or self.elapsed < self.length()

        def visit(self):
            # texts holds (string, Text) pairs, keyed by role.
            return [shown for text, shown in self.texts.values()] + list(self.solids.values())

        def _solid(self, color):
            if color not in self.solids:
                self.solids[color] = Solid(color)
            return self.solids[color]

        def _text(self, key, text, **properties):
            if key not in self.texts or self.texts[key][0] != text:
                self.texts[key] = (text, Text(text, substitute=False, **properties))
            return self.texts[key][1]

        def render(self, width, height, st, at):
            rv = renpy.Render(1280, 720)
            if not self.armed:
                return rv
            wall = ar_time.perf_counter()
            if self.last is not None:
                # A stalled frame (a first decode, a GL compile) delays the wipe instead of skipping it.
                self.elapsed += min(max(0.0, wall - self.last), 1 / 30.0)
            self.last = wall
            if self.mode == "cover":
                self._draw(rv, min(1.0, self.elapsed / AR_WIPE_TIME), st, at)
                if self.closed:
                    # Hand over on the next event; event() returns the value.
                    renpy.timeout(0)
                renpy.redraw(self, 0)
            else:
                p = min(1.0, max(0.0, self.elapsed - self.hold) / AR_WIPE_TIME)
                if p < 1.0:
                    self._draw(rv, p, st, at)
                if self.elapsed < self.length() + self.grace:
                    renpy.redraw(self, 0)
            return rv

        def event(self, ev, x, y, st):
            if not self.armed:
                return None
            if self.closed:
                return self.value
            if self.block and ev.type in AR_INPUT_EVENTS:
                if self.mode == "cover" or self.elapsed < self.length() + self.grace:
                    raise renpy.IgnoreEvent()
            return None

        def _draw(self, rv, p, st, at):
            lead, second, plate = AR_WIPE_PALETTES.get(self.palette, AR_WIPE_PALETTES["enter"])
            s = AR_WIPE_SLANT
            span = 1.0 + AR_WIPE_STAGGER[-1]
            # An edge at `near` clears every row; at `far` it covers every row.
            near, far = -s * .5 - 6, 1280 + s * .5 + 6
            cover = self.mode == "cover"
            stagger = AR_WIPE_STAGGER if cover else tuple(reversed(AR_WIPE_STAGGER))
            edge = near
            # Drawn lead first, plate last: while covering, the slivers show
            # ahead of the plate; while clearing, they trail behind it.
            for color, delay in zip((lead, second, plate), stagger):
                edge = near + (far - near) * ar_ease_in_out(p * span - delay)
                if cover:
                    ar_slant_fill(rv, self._solid(color), -s - 60, edge, 0, 720, s, st, at)
                else:
                    ar_slant_fill(rv, self._solid(color), edge, 1280 + s + 60, 0, 720, s, st, at)
            if near < edge < far:
                # A hairline of light along the plate's moving edge.
                if cover:
                    ar_slant_fill(rv, self._solid("#ffffff5c"), edge - 3, edge, 0, 720, s, st, at)
                else:
                    ar_slant_fill(rv, self._solid("#ffffff5c"), edge, edge + 3, 0, 720, s, st, at)
            if self.title:
                self._draw_title(rv, p, lead, st, at)

        def _draw_title(self, rv, p, accent, st, at):
            # The song's title card rides the plate: it slides in as the cover
            # closes and slides on out as the uncover opens.
            if self.mode == "cover":
                a = ar_ease_out((p - .55) / .35)
                shift = -44 * (1 - a)
            else:
                lift = min(1.0, p / .38) ** 2
                a, shift = 1 - lift, 44 * lift
            if a <= .003:
                return
            outline = ((6, "#0b0714", 0, 3),)
            title = self._text("title", ar_fit_text(self.title, 1040, AR_FONT, 60, outline),
                               font=AR_FONT, size=60, color="#ffffff", outlines=list(outline))
            ar_blit(rv, title, 640 + shift, 330, st, at, alpha=a)
            bar = 170 * a
            ar_slant_fill(rv, self._solid(accent), 640 + shift - bar * .5, 640 + shift + bar * .5, 374, 6, 6, st, at)
            if self.subtitle:
                sub = self._text("subtitle", self.subtitle, font=AR_UI_FONT, size=17, color=AR_GOLD, kerning=1.5,
                                 outlines=[(2, "#0b0714", 0, 1)])
                ar_blit(rv, sub, 640 + shift * .6, 402, st, at, alpha=a)

    # ---- the stage's ending ----------------------------------------------------
    AR_FAIL_FREEZE = .12        # The hit stop: only the flash, the shake and the burst move.
    AR_FAIL_LENGTH = 2.3        # The fail sequence runs this long before its wipe starts.
    AR_FAIL_SKIP = .70          # After this long, a key starts the wipe at once.
    AR_CLEAR_LENGTH = 1.6
    AR_CLEAR_SKIP = .40
    AR_FAIL_SHARDS = 18
    # Where the burst leaves the player (world px), and the shot the camera pushes into.
    AR_FAIL_CHEST = (AR_SPOT_X["player"], AR_FEET_Y - 236)
    AR_FAIL_SHOT = (AR_SPOT_X["player"] - 10, 610, 1.30)
    AR_CLEAR_SHOT = (836, 566, .96)

    class ARFinale(object):
        """How a song ends on the stage: ``failed``, ``clear``, ``retry`` or ``quit``.

        Failed and clear play a sequence, then arm the stage's exit wipe; retry
        and quit arm it at once. ``age`` runs on wall time with stalled frames
        clamped, like ARWipe's clock, so a slow frame never skips a beat of it.

        The fail sequence, in order: the song cuts and the burst sound plays; a
        white flash and a hit stop with the frame shaking; a burst of rings and
        sparks from the player; the room goes dark except for one light on the
        player, who is knocked back and slumps while the camera pushes in; the
        outlines drop one at a time and the notes on the highway spill off it;
        the player's icon falls off the bar; Asahina celebrates.
        """
        PALETTES = {"failed": "fail", "clear": "clear"}

        @staticmethod
        def preload(stage):
            """Load everything an ending draws, so none of it is created mid-song."""
            for name, tint in (("glow", "white"), ("glow", "pink"), ("glow", "gold"), ("ring", "white"),
                               ("ring", "pink"), ("shard", "white"), ("shard", "pink"), ("beam", "white"),
                               ("pool", "white")):
                stage.fx.texture(name, tint)
            for tint in AR_CONFETTI_TINTS:
                stage.fx.texture("confetti", tint)
            # All 32 original singer drawings, including win/lose, are already
            # cached and predicted by ARStage.

        def __init__(self, stage, kind):
            self.stage = stage
            self.kind = kind
            self.age = 0.0
            self.last = None
            self.wipe_at = {"failed": AR_FAIL_LENGTH, "clear": AR_CLEAR_LENGTH}.get(kind, 0.0)
            self.skip_after = {"failed": AR_FAIL_SKIP, "clear": AR_CLEAR_SKIP}.get(kind, 0.0)
            self.view0 = stage.view
            self.rigs = {}
            # The note heads on screen when the lanes collapse, taken on the first collapsing frame.
            self.spill = None
            if kind == "failed":
                renpy.music.play(audio.asarhythm_fail, channel=AR_SFX_CHANNEL, loop=False, relative_volume=.9)
            elif kind == "clear":
                stage.fx.flashes.append(stage.now)
                stage._volley()

        # ---- helpers -----------------------------------------------------------

        def _tex(self, name, tint=None):
            return self.stage.fx.texture(name, tint)

        def _rig(self, key, child):
            rig = self.rigs.get(key)
            if rig is None:
                rig = self.rigs[key] = Transform(child, rotate_pad=True)
            return rig

        def _turn(self, target, rig, x, y, degrees, alpha=1.0, additive=False, zoom=1.0):
            """Blit a rig turned about its centre, centred on (x, y)."""
            ar_blit_turned(target, rig, (2, 2), (1, 1), (x, y), degrees, self.stage.st, self.stage.at,
                           alpha, additive, 1.0, zoom)

        # ---- clock -------------------------------------------------------------

        def step(self, wall):
            dt = 0.0 if self.last is None else min(max(0.0, wall - self.last), 1 / 30.0)
            self.age += dt
            self.last = wall
            stage = self.stage
            if self.kind == "clear":
                # The room keeps dancing after the last note. A failed room stays frozen.
                stage.now = stage.end_time + self.age
            elif self.kind == "failed" and self.age >= AR_FAIL_FREEZE:
                # Song time has stopped, which would leave the last rating hanging
                # in the air. Running its own clock lets it finish falling.
                for pop in stage.popups:
                    pop["born"] -= dt
            wipe = stage.exit_wipe
            if wipe is not None and not wipe.armed and self.age >= self.wipe_at:
                title = subtitle = None
                if self.kind == "retry":
                    title, subtitle = stage.chart["title"], "   •   ".join(stage.tags) or None
                wipe.arm(stage.result, self.PALETTES.get(self.kind, "enter"), title, subtitle)

        def skip(self):
            """A key during the sequence starts the wipe now, once the sequence has had its moment."""
            if self.skip_after <= self.age < self.wipe_at:
                self.wipe_at = self.age

        def collapsing(self):
            return self.kind == "failed" and self.age >= AR_FAIL_FREEZE

        def shake(self):
            """Screen px the frame is knocked by right now."""
            if self.kind != "failed" or self.age > .7:
                return 0.0, 0.0
            amp = 15.0 * ar_math.exp(-self.age / .17)
            return amp * ar_math.sin(self.age * 81.0), amp * .6 * ar_math.cos(self.age * 63.0)

        def chrome_alpha(self):
            """What is left of the bar, the time bar and the callouts."""
            if self.kind == "failed":
                return 1 - ar_ease_out((self.age - .55) / .6)
            if self.kind == "clear":
                return 1 - ar_ease_out(self.age / .45)
            return 1.0

        def lanes_alpha(self):
            if self.kind == "clear":
                return 1 - ar_ease_out((self.age - .30) / .45)
            return 1.0

        # ---- world ---------------------------------------------------------------

        def camera(self):
            """The world view during the ending, or None to leave the stage's camera where it is."""
            if self.kind == "failed":
                t, target = ar_ease_out((self.age - AR_FAIL_FREEZE) / .95), AR_FAIL_SHOT
            elif self.kind == "clear":
                t, target = ar_ease_in_out(self.age / 1.3), AR_CLEAR_SHOT
            else:
                return None
            x0, y0, z0 = self.view0
            z = z0 + (target[2] - z0) * t
            dx, dy = self.shake()
            x = x0 + (target[0] - x0) * t + dx / z
            y = y0 + (target[1] - y0) * t + dy / z
            half_w, half_h = 640.0 / z, 360.0 / z
            return (min(max(x, half_w), AR_WORLD[0] - half_w), min(max(y, half_h), AR_WORLD[1] - half_h), z)

        def pose(self, side):
            """Ending expression, or None during the frozen stage hit stop.

            The full-frame displayable owns each gesture's timing and stable
            placement. Endings do not add separate instant position/scale kicks.
            """
            age = self.age
            if self.kind == "failed":
                t = age - AR_FAIL_FREEZE
                if side == "player":
                    if t < 0:
                        return None
                    return "miss" if t < .30 else "lose"
                t -= .28
                if t < 0:
                    return None
                return "hey" if t < .9 else "win"
            if self.kind == "clear":
                if side == "player":
                    return "hey" if age < 1.0 else "win"
                return "miss" if age < .32 else "lose"
            return None

        def draw_world_veil(self, layer):
            """Failed: the room goes dark behind the player, with one light left on them. Drawn before the player."""
            if self.kind != "failed":
                return
            level = ar_ease_out((self.age - AR_FAIL_FREEZE) / .55)
            if level <= .003:
                return
            stage = self.stage
            veil = renpy.Render(*AR_WORLD)
            veil.blit(renpy.render(stage._solid("#10061a"), AR_WORLD[0], AR_WORLD[1], stage.st, stage.at), (0, 0))
            layer.blit(ar_fade(veil, .66 * level), (0, 0))
            x = AR_SPOT_X["player"] + 30
            stage._place(layer, self._tex("beam", "white"), x, -40, scale=1.25, sy=(AR_FEET_Y + 40) / 900.0,
                         alpha=.22 * level, yanchor=0.0, additive=True)
            stage._place(layer, self._tex("pool", "white"), x, AR_FEET_Y + 4, scale=1.2, alpha=.45 * level, additive=True)

        def draw_world_burst(self, layer):
            """Failed: rings and sparks leave the player's chest. Drawn over the singers."""
            if self.kind != "failed":
                return
            stage, age = self.stage, self.age
            cx, cy = AR_FAIL_CHEST
            if age < .5:
                fade = 1 - age / .5
                stage._place(layer, self._tex("glow", "pink"), cx, cy, scale=3.2, alpha=.85 * fade, additive=True)
                stage._place(layer, self._tex("glow", "white"), cx, cy, scale=.3 + 1.7 * fade, alpha=fade, additive=True)
            for delay, tint, reach, life in ((0.0, "white", 2.4, .40), (.06, "pink", 3.4, .60), (.15, "pink", 4.8, .85)):
                t = (age - delay) / life
                if 0 <= t < 1:
                    stage._place(layer, self._tex("ring", tint), cx, cy, scale=.2 + reach * ar_ease_out(t),
                                 alpha=(1 - t) ** 1.6, additive=True)
            for i in range(AR_FAIL_SHARDS):
                life = .5 + .4 * ar_unit(77, i, 1)
                if age >= life:
                    continue
                angle = 2 * ar_math.pi * (i + .6 * ar_unit(77, i, 2)) / AR_FAIL_SHARDS
                # Fast out of the chest, dragged to a stop, and a little gravity.
                reach = (1000.0 + 1100.0 * ar_unit(77, i, 3)) * .16 * (1 - ar_math.exp(-age / .16))
                x = cx + ar_math.cos(angle) * reach
                y = cy + ar_math.sin(angle) * reach + 300.0 * age * age
                tint = "white" if i % 3 else "pink"
                self._turn(layer, self._rig(("shard", i), self._tex("shard", tint)), x, y, ar_math.degrees(angle),
                           alpha=1 - age / life, additive=True, zoom=1.1 + .9 * ar_unit(77, i, 4))

        def draw_screen(self, r):
            """Failed: the white flash, over everything the stage draws."""
            if self.kind != "failed" or self.age > .6:
                return
            stage = self.stage
            plate = renpy.Render(1280, 720)
            plate.blit(renpy.render(stage._solid("#fff1f6"), 1280, 720, stage.st, stage.at), (0, 0))
            r.blit(ar_fade(plate, .75 * ar_math.exp(-self.age / .075), additive=True), (0, 0))

        # ---- HUD -----------------------------------------------------------------

        def draw_hud(self, hud, ry):
            if self.collapsing():
                self._draw_collapse(hud, ry)
            elif self.kind == "clear":
                self._draw_clear(hud, ry)

        def _draw_collapse(self, hud, ry):
            stage = self.stage
            t0 = self.age - AR_FAIL_FREEZE
            # The outlines drop one at a time, the player's first.
            for side in (1, 0):
                playable = side == 1 or stage.game.duet
                for lane in range(4):
                    order = lane if side == 1 else 4 + lane
                    x = ar_lane_x(side, lane)
                    base = 1.0 if playable else .85
                    receptor = stage.images[("receptor", lane)]
                    t = t0 - .045 * order
                    if t <= 0:
                        stage._place(hud, receptor, x, ry, 1.0, base)
                        continue
                    y = ry - (200.0 + 160.0 * ar_unit(91, order, 1)) * t + 1300.0 * t * t
                    alpha = base * max(0.0, min(1.0, 1 - (t - .45) / .35))
                    if y < 860 and alpha > .003:
                        self._turn(hud, self._rig(("receptor", order), receptor), x + (ar_unit(91, order) - .5) * 260.0 * t,
                                   y, (ar_unit(91, order, 2) - .5) * 560.0 * t, alpha)
            # The notes on the highway spill off it.
            if self.spill is None:
                self.spill = list(stage.heads[-40:])
            for i, (x, y, lane, alpha) in enumerate(self.spill):
                note = stage.images[("note", lane)]
                t = t0 - .06 * ar_unit(53, i)
                if t <= 0:
                    stage._place(hud, note, x, y, 1.0, alpha)
                    continue
                gy = y - (120.0 + 280.0 * ar_unit(53, i, 2)) * t + 1500.0 * t * t
                fade = alpha * max(0.0, min(1.0, 1 - (t - .40) / .30))
                if gy < 860 and fade > .003:
                    self._turn(hud, self._rig(("note", i), note), x + (ar_unit(53, i, 1) - .5) * 340.0 * t, gy,
                               (ar_unit(53, i, 3) - .5) * 720.0 * t, fade)
            # The player's icon comes off the right end of the empty bar.
            if t0 < .9:
                cy = 72 if stage.downscroll else 650
                y = cy - 8 - 560.0 * t0 + 1700.0 * t0 * t0
                if y < 860:
                    self._turn(hud, self._rig(("icon",), stage.images[("icon", "asahiko", "losing")]),
                               978 + 150.0 * t0, y, 380.0 * t0, max(0.0, min(1.0, 1 - (t0 - .5) / .3)), zoom=.72)

        def _draw_clear(self, hud, ry):
            stage, age = self.stage, self.age
            # Every playable outline lights once, left to right, as the lanes fade.
            order = 0
            for side in ((0, 1) if stage.game.duet else (1,)):
                for lane in range(4):
                    t = age - .04 * order
                    order += 1
                    if 0 <= t < .5:
                        stage._place(hud, stage.images[("confirm", lane)], ar_lane_x(side, lane), ry,
                                     1 + .22 * ar_math.exp(-t / .08), 1 - t / .5)
            # The banner shoots across and the words punch in over it.
            e = ar_ease_out((age - .12) / .40)
            if e <= 0:
                return
            cy, h, slant = 318.0, 112.0, 40.0
            reach = -120.0 + 1560.0 * e
            st, at = stage.st, stage.at
            ar_slant_fill(hud, stage._solid("#160f24b0"), -300, reach - 10, cy - h * .5 + 14, h, slant, st, at)
            ar_slant_fill(hud, stage._solid(AR_GOLD), -300, reach + 30, cy - h * .5 - 7, h + 14, slant, st, at)
            ar_slant_fill(hud, stage._solid(AR_PINK), -300, reach, cy - h * .5, h, slant, st, at)
            shown = max(0.0, min(1.0, (age - .20) / .10))
            if shown > 0:
                word = stage._text("STAGE CLEAR!", 80, "#ffffff", AR_FONT, ((10, AR_INK, 0, 5), (5, "#ff8cc4", 0, 0)))
                stage._place(hud, word, 640, cy, 1 + .35 * ar_math.exp(-max(0.0, age - .20) / .09), shown)

    # ---- song select and results -------------------------------------------------

    def ar_leave_for_song(wipe, index, chart, duo=None):
        """Song select's way in: cover the page with the song's title card, then return ``index``."""
        if wipe.armed:
            return
        if duo is not None:
            duo.react("ready")
        persistent.asahina_rhythm_last_song = chart["id"]
        tags = ar_mod_names(ar_active_mods(), practice=bool(persistent.asahina_rhythm_practice),
                            autoplay=bool(persistent.asahina_rhythm_autoplay))
        wipe.arm(index, "enter", chart["title"], "   •   ".join(tags) or None)

    class ARRibbon(renpy.Displayable):
        """The results header's slanted band. It shoots in from the left edge once, after ``delay``, and stays."""
        def __init__(self, color, sliver, width=700, height=104, delay=0.0, **kwargs):
            super(ARRibbon, self).__init__(**kwargs)
            self.color, self.sliver, self.shadow = Solid(color), Solid(sliver), Solid("#0b071499")
            self.width, self.height, self.delay = width, height, delay

        def visit(self):
            return [self.color, self.sliver, self.shadow]

        def render(self, width, height, st, at):
            w, h = self.width, self.height
            rv = renpy.Render(w + 80, h + 24)
            e = ar_ease_out((st - self.delay) / .42)
            if e < 1:
                renpy.redraw(self, 0)
            if e <= 0:
                return rv
            slant = h * AR_WIPE_SLANT / 720.0
            reach = -slant + (w + slant) * e
            ar_slant_fill(rv, self.shadow, -200, reach - 8, 14, h, slant, st, at)
            ar_slant_fill(rv, self.sliver, -200, reach + 26, 0, h + 10, slant, st, at)
            ar_slant_fill(rv, self.color, -200, reach, 4, h, slant, st, at)
            return rv

    class ARResultsFX(renpy.Displayable):
        """The results backdrop's motion. A clear gets two warm beams swaying over the winner and
        falling confetti; a failure gets one cold light on the winner and slow falling ash."""
        def __init__(self, won, **kwargs):
            super(ARResultsFX, self).__init__(**kwargs)
            self.won = won
            self.images = {}
            if won:
                self.beams = (("gold", 120.0, -9.0, 0.0), ("pink", 390.0, 9.0, 2.3))
                for tint in AR_CONFETTI_TINTS:
                    self.images[("confetti", tint)] = Image(AR_FX + "confetti_%s.png" % tint)
            else:
                self.beams = (("white", 250.0, 0.0, 0.0),)
                self.images[("glow", "white")] = Image(AR_FX + "glow_white.png")
                self.images[("pool", "pink")] = Image(AR_FX + "pool_pink.png")
            for tint, x, rest, phase in self.beams:
                self.images[("beam", tint)] = Image(AR_FX + "beam_%s.png" % tint)
            self.rigs = [Transform(self.images[("beam", tint)], rotate_pad=True) for tint, x, rest, phase in self.beams]

        def visit(self):
            return list(self.images.values())

        def render(self, width, height, st, at):
            rv = renpy.Render(1280, 720)
            fade = min(1.0, st / .8)
            for rig, (tint, x, rest, phase) in zip(self.rigs, self.beams):
                degrees = rest + (7.0 if self.won else 2.5) * ar_math.sin(st * (.55 if self.won else .25) + phase)
                ar_blit_turned(rv, rig, (220, 900), (110, 0), (x, -70), degrees, st, at,
                               (.26 if self.won else .16) * fade, True, 1.0, 1.0)
            if self.won:
                for j in range(48):
                    fall = 55.0 + 75.0 * ar_unit(211, j, 1)
                    y = (st * fall + 800.0 * ar_unit(211, j, 2)) % 800.0 - 40.0
                    x = 1280.0 * ar_unit(211, j, 3) + 34.0 * ar_math.sin(1.1 * st + 6.283 * ar_unit(211, j, 4))
                    tint = AR_CONFETTI_TINTS[int(ar_unit(211, j, 5) * len(AR_CONFETTI_TINTS))]
                    spin = 4.0 + 6.0 * ar_unit(211, j, 6)
                    # Tumbling paper, as in ARStageFX._piece.
                    ar_blit(rv, self.images[("confetti", tint)], x, y, st, at,
                            scale=.55 + .45 * abs(ar_math.sin(spin * .6 * st + j)),
                            sy=.18 + .82 * abs(ar_math.cos(spin * st + j)), alpha=.9 * fade)
            else:
                ar_blit(rv, self.images[("pool", "pink")], 250, 708, st, at, scale=1.5, alpha=.30 * fade, additive=True)
                for j in range(34):
                    fall = 14.0 + 22.0 * ar_unit(223, j, 1)
                    y = (st * fall + 780.0 * ar_unit(223, j, 2)) % 780.0 - 30.0
                    x = 1280.0 * ar_unit(223, j, 3) + 22.0 * ar_math.sin(.5 * st + 6.283 * ar_unit(223, j, 4))
                    twinkle = .5 + .5 * ar_math.sin(st * (.7 + ar_unit(223, j, 5)) + j)
                    ar_blit(rv, self.images[("glow", "white")], x, y, st, at, scale=.03 + .05 * ar_unit(223, j, 6),
                            alpha=(.10 + .16 * twinkle) * fade, additive=True)
            renpy.redraw(self, 0)
            return rv

# The results header, one letter at a time. A clear's letters bounce onto the
# line and then ride a slow wave. A failure's fall like dead weight, and two
# colour ghosts behind them slip out of register now and then. Letters move
# only by offset and alpha, so the hbox never reflows while they animate, and
# spacing -12 takes back the 6 px outline each letter carries on both sides.
screen ar_results_header(word, won, delay=0.0):
    fixed:
        xpos 40 ypos 42
        xysize (600, 96)
        if not won:
            hbox:
                spacing -12
                at ar_ghost(-9, delay + .90)
                for letter in word:
                    text letter style "ar_header_ghost" color "#5fd8e8" substitute False
            hbox:
                spacing -12
                at ar_ghost(9, delay + .95)
                for letter in word:
                    text letter style "ar_header_ghost" color "#fa698b" substitute False
        hbox:
            spacing -12
            for i, letter in enumerate(word):
                if won:
                    text letter style "ar_header" substitute False at ar_letter_bounce(delay + i * .045)
                else:
                    text letter style "ar_header" substitute False at ar_letter_drop(delay + i * .04)

transform ar_letter_bounce(delay=0.0):
    alpha 0.0 yoffset -64
    pause delay
    parallel:
        linear .12 alpha 1.0
    parallel:
        easein_back .36 yoffset 0
        pause .6
        block:
            ease .5 yoffset -6
            ease .5 yoffset 0
            repeat

transform ar_letter_drop(delay=0.0):
    alpha 0.0 yoffset -96
    pause delay
    parallel:
        linear .08 alpha 1.0
    parallel:
        easeout .22 yoffset 6
        easein .12 yoffset 0

transform ar_ghost(dx=4, delay=1.0):
    alpha 0.0 xoffset 0 yoffset 0
    pause delay
    alpha .85 xoffset dx
    block:
        pause 1.7
        xoffset (dx * 2) yoffset 2
        pause .05
        xoffset (-dx) yoffset -1
        pause .05
        xoffset (dx * 1.5) yoffset 0
        pause .04
        xoffset dx
        pause .6
        repeat

style ar_header:
    font AR_FONT
    size 64
    color "#ffffff"
    outlines [(6, "#160f24", 0, 3)]
# A transparent outline keeps each ghost letter exactly the size of the letter it haunts.
style ar_header_ghost is ar_header:
    outlines [(6, "#00000000", 0, 3)]
style ar_reached:
    font AR_FONT
    size 44
    color "#ffffff"
    outlines [(5, "#160f24", 0, 2)]
