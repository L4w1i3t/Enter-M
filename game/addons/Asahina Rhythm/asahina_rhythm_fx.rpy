# Chart-cued stage effects for Asarhythm: the concert lighting, lasers, haze,
# crowd and fanfare that the Chart Studio's FX lane places -- and the dread set
# that does the opposite of all of it.
#
# THERE ARE TWO PALETTES IN HERE AND THEY ARE BUILT ON OPPOSITE PRINCIPLES.
# The concert set ADDS light and KEEPS TIME: beams sweep on the beat, the
# fanfare burns gold, confetti answers a clear. The dread set TAKES light away
# and REFUSES to keep time. Dread's aperture breathes on a seven-second cycle
# that belongs to no tempo; Arrhythmia thumps at a flat 46 BPM whatever the
# song is doing, so it slides through the music and never once resolves onto a
# downbeat; Gutter fails on three incommensurable rates at once. That is the
# whole trick. A rhythm game teaches you to predict the next moment within a
# few bars, and horror here is simply the refusal to be predicted -- which is
# also why none of it is a jump scare. The loudest thing in the dread set is a
# silhouette at 46% alpha for five frames.
#
# The same principle is what makes Photosensitive Mode cheap to honour. Nearly
# nothing here works by changing the brightness of the frame quickly, so the
# switch can take the few things that do and leave the rest of the horror
# standing. See accessibility.rpy for the policy; the per-effect decisions are
# written at the call sites below, each one next to the drawing it changes.
#
# HOW THE COLOUR EFFECTS WORK WITHOUT A SHADER. Red Wash, Invert, Negative,
# Infrared and Deep Fried all want to transform pixels that are already in the
# frame, which normally means a shader or a matrixcolor -- and the rule at the
# top of this file is that neither may be compiled mid-song, because a first-use
# GL program compile can outrun the stalled-frame auto-pause.
#
# They use GL BLEND FUNCTIONS instead. `config.gl_blend_func` is an extensible
# dictionary, and a blend function is fixed-function GPU state: it selects
# how a source fragment combines with what is already in the framebuffer.
# NOTHING IS COMPILED. Setting one on a Render costs a state change and no
# more, so it is safe at any point in a song.
#
# What that buys, with a plate of flat colour at alpha `a` (Ren'Py premultiplies,
# which is what makes every one of these land as a clean lerp on `a`):
#
#   multiply    result = dst * (1 - a*(1 - C))      a tint that keeps detail
#   ar_screen   result = src*(1 - dst) + dst        a lift that keeps highlights
#   ar_invert   result = lerp(dst, 1 - dst, a)      a true negative
#
# Stacked, multiply-then-screen is a contrast curve, which is all Deep Fried is.
# Multiply by pure green leaves only the green channel, which is a monochrome
# camera, which is all Infrared is. Measured in a probe before any of it was
# written; see the write-up.
#
# ONE THING BLEND FUNCTIONS CANNOT DO IS LOSE RESOLUTION, and Bitcrush has to.
# Render.zoom only multiplies matrices -- zooming down and back up resamples
# nothing -- and setting `mesh` on a Render does nothing either. What works is a
# pair of Transforms on a DISPLAYABLE with `mesh=True`, which forces the child
# to a texture at the transform's size. That is why Bitcrush wraps the stage's
# children one at a time instead of crushing the finished world layer: the world
# is a Render by then, and a Render cannot be resampled. It is also why the HUD
# comes out sharp, which is the right answer anyway -- the lanes have to stay
# readable or the effect is not a filter, it is a difficulty setting.
#
# Chart effects are closed-form functions of song time and carry no per-frame
# state. A pause, a seek or an editor preview that starts mid-song therefore
# shows exactly what a straight play-through would. The only stateful pieces
# are gameplay reactions (a fanfare relit, a streak topped), which the stage
# stamps with the song time they happened at.
#
# Textures have every tint baked in.
# Nothing here uses a matrixcolor: a GL program first compiled mid-song can stall
# a frame long enough to trip the stage's auto-pause. Nothing is pinned to a spot
# in the backdrop either. Lamps hang above the frame, emitters sit past its
# edges, and the only fixed marks are the singers' own spots from AR_SPOT_X.

init -1 python:
    from asahina_rhythm_core import (BURST_EFFECTS as AR_BURSTS, FANFARE_RELIGHT as AR_FANFARE_RELIGHT,
                                     REACTIVE_EFFECTS as AR_REACTIVE, IMPACT_GAIN as AR_IMPACT_GAIN,
                                     effect_tracks as ar_effect_tracks, impact_tracks as ar_impact_tracks,
                                     chord_sizes as ar_chord_sizes)

    # Blend modes beyond Ren'Py's own normal/add/multiply/min/max. Registered
    # once at init, namespaced so nothing else in the game can collide with
    # them, and guarded: a driver or a future SDK that does not expose the
    # constants loses these five effects and keeps the other thirty-two.
    AR_BLEND_OK = True
    try:
        from renpy.uguu import (GL_FUNC_ADD as _AR_ADD, GL_ONE as _AR_ONE,
                                GL_ONE_MINUS_SRC_ALPHA as _AR_INV_SA,
                                GL_ONE_MINUS_DST_COLOR as _AR_INV_DST)
        # lerp(dst, 1 - dst, src_alpha), for a white source.
        config.gl_blend_func["ar_invert"] = (_AR_ADD, _AR_INV_DST, _AR_INV_SA,
                                             _AR_ADD, _AR_ONE, _AR_INV_SA)
        # src*(1 - dst) + dst: screen, which lifts without clipping highlights.
        config.gl_blend_func["ar_screen"] = (_AR_ADD, _AR_INV_DST, _AR_ONE,
                                             _AR_ADD, _AR_ONE, _AR_INV_SA)
    except Exception:
        AR_BLEND_OK = False

    AR_FX = AR_ART + "fx/"
    # Reactive effects answer a singer's notes, so they wear that singer's colour.
    AR_SIDE_TINT = {"opponent": "pink", "player": "cyan"}
    AR_SIDE_LIGHT = {"opponent": "#ff86c4", "player": "#7fe6f4"}
    # A lone note's knock, in screen pixels; IMPACT_GAIN scales it by chord size.
    AR_QUAKE_PX = 15.0
    # How far a lunge shoves the camera toward whoever just sang, in world pixels.
    AR_LUNGE_PX = 46.0
    # How far a recoil shoves the camera AWAY from whoever sang, in world pixels,
    # and how far out it pulls the zoom. Put Lunge on one singer and Recoil on
    # the other and the frame is dragged in two directions at once.
    AR_RECOIL_PX = 40.0
    # Arrhythmia's tempo, in beats per minute, held flat no matter the song's.
    # A resting heart is around 60; this one is slow, and slow is worse.
    AR_HEART_BPM = 46.0
    # Watchers: how many pairs of eyes the dark holds, and the band of world
    # height they open in -- above the singers' heads, below the lamp line.
    AR_WATCH_COUNT = 11
    AR_WATCH_Y = (250.0, 470.0)
    # Tear: how long the picture stays off its hold, how many bands it breaks
    # into, and the widest slip in screen pixels.
    AR_TEAR_TIME, AR_TEAR_BANDS, AR_TEAR_PX = .45, 9, 58.0
    # Glimpse: how long someone is standing there. Five frames at 60Hz -- long
    # enough to register as a person, short enough that you cannot check.
    AR_GLIMPSE_HOLD = .085
    # Fracture: how long a crack stays, and how many are drawn at once. A dense
    # chart lands more than this inside one lifetime; the oldest simply stop.
    AR_CRACK_TIME, AR_CRACK_MAX = 2.2, 14
    # Blood: how far down the frame a full cue reaches, and the pool at the foot.
    AR_BLOOD_REACH, AR_BLOOD_POOL = 660.0, 120.0
    # Convulse: the widest shake in world pixels, and how hard a singer leans.
    AR_CONVULSE_PX, AR_CONVULSE_TILT = 13.0, 3.4
    # Invert: how long one glitch frame holds. Three frames at 60Hz.
    AR_INVERT_HOLD = .05
    # Bitcrush: the resample factors the crush steps through. Quantised, because
    # each distinct factor is a cached pair of Transforms and a per-frame
    # offscreen pass; a continuous factor would build one per frame forever.
    AR_CRUSH_STEPS = (4.0, 7.0, 12.0, 20.0)
    AR_STICK_TINTS = ("pink", "cyan", "gold", "green", "violet")
    AR_CONFETTI_TINTS = ("pink", "cyan", "gold", "green", "violet", "white")
    AR_LASER_TINTS = ("pink", "cyan", "green", "gold")
    AR_GLOW_FOR = {"pink": "pink", "cyan": "cyan", "gold": "gold", "green": "white", "violet": "pink"}
    # Lamp rigs across the top of the world: (fraction of world width, resting
    # angle, sweep phase, tint). A positive angle swings the beam's foot left.
    AR_SPOT_RIGS = ((.13, -18.0, 0.0, "pink"), (.37, -7.0, 1.7, "cyan"),
                    (.63, 7.0, 3.1, "gold"), (.87, 18.0, 4.6, "cyan"))
    # The textures each effect needs, so a chart loads only what it uses.
    AR_FX_TEXTURES = {
        "spotlights": [("beam", t) for t in ("pink", "cyan", "gold")] + [("pool", t) for t in ("pink", "cyan", "gold")],
        "blackout": [("beam", "white"), ("pool", "white")],
        "fanfare": ([("beam", "gold"), ("pool", "gold"), ("glow", "gold"), ("frame", "gold"), ("ring", "gold"),
                     ("burst", "gold")] + [("confetti", t) for t in AR_CONFETTI_TINTS]),
        "lasers": [("laser", t) for t in AR_LASER_TINTS] + [("glow", "white")],
        "haze": [("haze", None)],
        "crowd": ([("crowd", None)] + [("stick", t) for t in AR_STICK_TINTS] +
                  [("glow", t) for t in ("pink", "cyan", "gold", "white")]),
        "confetti": [("confetti", t) for t in AR_CONFETTI_TINTS],
        "sparks": [("glow", "gold"), ("glow", "white")],
        "shockwave": [("ring", "pink"), ("ring", "cyan")],
        # The dread set. Several need nothing: they are camera moves, a black
        # plate, or a second pass over art the stage already holds.
        "dread": [("shroud", None)],
        "watchers": [("socket", None), ("eye", "white"), ("eye", "pink"),
                     ("glow", "white"), ("glow", "pink")],
        "static": [("static", None), ("rollbar", None)],
        "hollow": [],
        "footlights": [("beam", "ash"), ("pool", "ash"), ("glow", "ash")],
        "rot": [("rot", None)],
        "arrhythmia": [],
        "doubles": [],
        "gutter": [],
        "recoil": [],
        "fracture": [("crack", "pink"), ("crack", "cyan")],
        "cut": [],
        "tear": [],
        "glimpse": [("figure", None)],
        # The body set.
        "veins": [("veins", None)],
        "blood": [("blood", None)],
        "convulse": [],
        "redwash": [],
        # The signal set. Four of the five are pure blend work and need no art.
        "invert": [],
        "negative": [],
        "infrared": [("scanlines", None), ("static", None)],
        "fried": [("static", None)],
        "bitcrush": [],
    }

    def ar_unit(seed, index, salt=0):
        """A stable pseudo-random number in [0, 1) for one particle, so particles need no stored state."""
        n = (seed * 73856093 ^ index * 19349663 ^ salt * 83492791) & 0xffffffff
        n = ((n ^ (n >> 13)) * 1274126177) & 0xffffffff
        return ((n ^ (n >> 16)) & 0xffffff) / float(0x1000000)

    def ar_beat_envelope(beat, beat_len, fall, every=1.0):
        """1 on each ``every``-beat boundary, falling away over ``fall`` seconds."""
        return ar_math.exp(-((beat % every) * beat_len) / fall)

    def ar_ease_out_back(t):
        t = max(0.0, min(1.0, t)) - 1
        return 1 + 2.70158 * t ** 3 + 1.70158 * t ** 2

    def ar_blit(target, child, x, y, st, at, scale=1.0, sy=None, alpha=1.0, xanchor=.5, yanchor=.5, additive=False):
        """ARStage._place for displayables other than the stage: anchor at (x, y), scaled and faded about it."""
        if alpha <= .003:
            return
        rendered = renpy.render(child, 1280, 720, st, at)
        width, height = rendered.get_size()
        sx, sy = scale, scale if sy is None else sy
        if sx == 1 and sy == 1 and alpha >= 1 and not additive:
            target.subpixel_blit(rendered, (x - width * xanchor, y - height * yanchor))
            return
        wrap = renpy.Render(width, height)
        if sx != 1 or sy != 1:
            wrap.zoom(sx, sy)
        wrap.blit(rendered, (0, 0))
        if alpha < 1 or additive:
            ar_fade(wrap, min(1.0, alpha), additive)
        target.subpixel_blit(wrap, (x - width * sx * xanchor, y - height * sy * yanchor))

    def ar_blit_turned(target, rig, size, pivot, point, degrees, st, at, alpha=1.0, additive=True, yzoom=1.0, zoom=1.0):
        """Blit a cached rig turned ``degrees`` clockwise about ``pivot`` (in the unturned child), pivot at ``point``.

        ``rig`` is a Transform with rotate_pad. Its rotation and zoom are set here
        and never in its constructor, whose values the update-state pass would
        otherwise restore on every render.
        """
        if alpha <= .003:
            return
        rig.rotate = degrees
        rig.yzoom = yzoom
        rig.zoom = zoom
        rig.update()
        rendered = renpy.render(rig, 1280, 720, st, at)
        width, height = rendered.get_size()
        theta = ar_math.radians(degrees)
        c, s = ar_math.cos(theta), ar_math.sin(theta)
        dx = (pivot[0] - size[0] * .5) * zoom
        dy = (pivot[1] - size[1] * .5) * zoom * yzoom
        mapped_x = width * .5 + c * dx - s * dy
        mapped_y = height * .5 + s * dx + c * dy
        if alpha < 1 or additive:
            wrap = renpy.Render(width, height)
            wrap.blit(rendered, (0, 0))
            rendered = ar_fade(wrap, min(1.0, alpha), additive)
        target.subpixel_blit(rendered, (point[0] - mapped_x, point[1] - mapped_y))

    class ARStageFX(object):
        def __init__(self, stage):
            self.stage = stage
            self.tracks = ar_effect_tracks(stage.chart)
            self.fanfare = self.tracks["fanfare"]
            self.used = set(kind for kind, track in self.tracks.items()
                            if (track.times if kind in AR_BURSTS else track.cues))
            # Reactive effects: the spans saying whose notes drive them, and how
            # many notes share each moment. Like the fanfare's flashes these are
            # gameplay reactions, so they are stamped with the song time they
            # happened at rather than being a closed-form function of it.
            self.impacts = ar_impact_tracks(stage.chart)
            self.chords = ar_chord_sizes(stage.chart)
            self.reactive = set(kind for kind in AR_REACTIVE if self.impacts[kind].cues)
            # Photosensitive Mode, re-read once a frame by ARStage.render rather
            # than per call: the switch can be flipped from the pause menu mid
            # song, and half the methods below ask about it more than once.
            self.safe = enter_m_photosensitive()
            # (song time, the note's side, gain, the kinds that answered it).
            self.landings = []
            self.rigs = {}
            # Bitcrush's resampling transforms, keyed (which child, what factor).
            self.crushes = {}
            # Gameplay-driven moments in song seconds: flash times, and (seed, time) confetti volleys.
            self.flashes = []
            self.volleys = []
            for kind in self.used:
                for name, tint in AR_FX_TEXTURES.get(kind, ()):
                    self.texture(name, tint)

        # ---- helpers ------------------------------------------------------------

        def texture(self, name, tint=None):
            key = ("fx", name, tint)
            if key not in self.stage.images:
                path = AR_FX + (name if tint is None else "%s_%s" % (name, tint)) + ".png"
                self.stage._image(key, path, zoom=.5 if name == "stick" else 1.0)
            return self.stage.images[key]

        def _rig(self, name, tint, *slot):
            key = (name, tint) + slot
            rig = self.rigs.get(key)
            if rig is None:
                rig = self.rigs[key] = Transform(self.texture(name, tint), rotate_pad=True)
            return rig

        def _turned(self, target, rig, size, pivot, point, degrees, alpha=1.0, additive=True, yzoom=1.0, zoom=1.0):
            ar_blit_turned(target, rig, size, pivot, point, degrees, self.stage.st, self.stage.at,
                           alpha, additive, yzoom, zoom)

        def _plate(self, target, color, alpha, additive=False, height=720, top=0, blend=None):
            """A flat colour over the whole frame (or one band of it) at ``alpha``.

            With ``blend`` it carries one of the modes registered at the top of
            this file, which is how every colour effect here transforms what is
            already in the frame without a shader. `alpha` stays the strength
            dial in every mode: Ren'Py premultiplies, so each of these blend
            functions works out to a clean lerp between the untouched frame and
            the full effect.
            """
            if alpha <= .003:
                return
            if blend is not None and not AR_BLEND_OK:
                return
            stage = self.stage
            plate = renpy.Render(1280, height)
            plate.blit(renpy.render(stage._solid(color), 1280, height, stage.st, stage.at), (0, 0))
            ar_fade(plate, min(1.0, alpha), additive)
            if blend is not None:
                plate.add_property("blend_func", config.gl_blend_func[blend])
            target.blit(plate, (0, top))

        def screen_x(self, world_x):
            """Where a world x lands in the frame under the camera as it stands this frame."""
            x, unused, z = self.stage.view
            return 640.0 + (world_x - x) * z

        def beat(self):
            stage = self.stage
            return (stage.now - stage.chart["offset"]) / stage.beat_len

        # ---- reactive: effects a singer sets off by singing ------------------------

        def impact(self, side, when, size):
            """Stamp a note landing on ``side`` at song time ``when``, ``size`` notes at once.

            Which effects answer is settled here, once, rather than every frame:
            a span that was not running at ``when`` never reacts to it, even if
            one starts before the knock has finished fading.
            """
            if not self.reactive:
                return
            kinds = frozenset(kind for kind in self.reactive if self.impacts[kind].drives(when, side))
            if not kinds:
                return
            self.landings.append((when, side, AR_IMPACT_GAIN[max(1, min(4, size))], kinds))
            # Deep enough to cover Fracture's whole lifetime on a dense chart;
            # what it draws is capped separately, by AR_CRACK_MAX.
            del self.landings[:-64]

        def chord_at(self, side, when):
            """How many of that side's notes land at ``when``; 1 for anything unlisted."""
            return self.chords.get(side, {}).get(round(when, 3), 1)

        def _live(self, kind, lifetime):
            """(age, gain, side) for each recent landing this effect answered."""
            return [row[1:] for row in self._live_keyed(kind, lifetime)]

        def _live_keyed(self, kind, lifetime):
            """(song time, age, gain, side) for each recent landing this effect answered.

            The song time is the landing's identity: Fracture needs a stable
            seed per note so one crack keeps its own angle for as long as it is
            on screen, and the time it landed at is the only thing it has.
            """
            if kind not in self.reactive:
                return ()
            now = self.stage.now
            return [(when, now - when, gain, side) for when, side, gain, kinds in self.landings
                    if kind in kinds and 0 <= now - when < lifetime]

        def quake(self):
            """Screen pixels the frame is knocked by, and the push-in that goes with it.

            Knocks add, so a chord hits harder than a lone note and a run of them
            never settles back to still. The push-in is what buys room for the
            shake: the camera clamp would otherwise eat it at the edges of the
            stage, or let the frame slide off them.
            """
            ox = oy = level = 0.0
            for age, gain, side in self._live("quake", .45):
                fall = ar_math.exp(-age / .13)
                amp = AR_QUAKE_PX * gain * fall
                ox += amp * ar_math.sin(age * 74.0)
                oy += amp * .62 * ar_math.cos(age * 58.0)
                level = max(level, gain * fall)
            limit = AR_QUAKE_PX * 2.4
            if self.safe:
                # Motion, not light: a knock is not a seizure risk, but a player
                # who turns the switch on is often turning it on for nausea too.
                ox, oy, level = ox * .55, oy * .55, level * .55
            return max(-limit, min(limit, ox)), max(-limit, min(limit, oy)), level

        def lunge(self):
            """(world px along the singers' line, signed zoom). Lunge shoves in, Recoil pulls out.

            Both reactive camera moves come out of here so the stage keeps one
            call. They are deliberately opposite in every axis: Lunge drives
            toward whoever sang and pushes the zoom in, Recoil flinches away
            and pulls it out. Put one on each singer and the frame is being
            dragged in two directions by two people who are not co-operating.
            """
            dx = push = pull = 0.0
            for age, gain, side in self._live("lunge", .5):
                fall = ar_math.exp(-age / .155)
                dx += (1 if side == "player" else -1) * AR_LUNGE_PX * gain * fall
                push = max(push, gain * fall)
            for age, gain, side in self._live("recoil", .55):
                # Slower to leave than a lunge, and slower to come back: a
                # flinch is not a hit, and it should read as reluctance.
                fall = ar_math.exp(-age / .21)
                dx += (-1 if side == "player" else 1) * AR_RECOIL_PX * gain * fall
                pull = max(pull, gain * fall)
            if self.safe:
                dx, push, pull = dx * .7, push * .7, pull * .7
            limit = (AR_LUNGE_PX + AR_RECOIL_PX) * 1.6
            return max(-limit, min(limit, dx)), push - pull * .55

        def strobe(self):
            """(alpha, colour) the last note left over the whole frame, in its singer's colour."""
            if self.safe:
                # A note-rate full-frame flare is the exact thing the switch is
                # for. There is no softened version of this worth shipping:
                # slow it down and it stops being a strobe and starts being a
                # wash that fights every other effect in the chart.
                return 0.0, None
            best, tint = 0.0, None
            for age, gain, side in self._live("strobe", .42):
                level = .42 * gain * ar_math.exp(-age / .105)
                if level > best:
                    best, tint = level, AR_SIDE_LIGHT[side]
            return best, tint

        def draw_shockwaves(self, layer):
            """A ring out of the singer's own spot, wider and brighter for a bigger chord."""
            stage = self.stage
            for age, gain, side in self._live("shockwave", .62):
                t = age / .62
                scale = .25 + 3.1 * gain * ar_ease_out(t)
                stage._place(layer, self.texture("ring", AR_SIDE_TINT[side]),
                             AR_SPOT_X[side], AR_FEET_Y - 210, scale=scale, sy=scale * .62,
                             alpha=(1 - t) ** 1.7 * .85, additive=True)

        def level(self, kind, rise=.35, fall=.5):
            if kind not in self.used:
                return 0.0
            return self.tracks[kind].level(self.stage.now, rise, fall)

        def fanfare_glow(self):
            """How hard the fanfare burns right now: dim while it is out, fading after it ends."""
            level = self.level("fanfare", .25, .8)
            if level <= 0:
                return 0.0
            inside, lit, multiplier, streak = self.stage.game.fanfare_state(self.stage.now)
            return level * (1.0 if lit or not inside else .3)

        def punch(self):
            """Extra camera punch: every beat under pulse, every other beat through a lit fanfare, and the heart."""
            stage = self.stage
            if not stage.started:
                return 0.0
            beat = self.beat()
            pulse = self.level("pulse", .2, .4) * ar_beat_envelope(beat, stage.beat_len, .16)
            fanfare = self.fanfare_glow() * ar_beat_envelope(beat, stage.beat_len, .2, 2.0) * .6
            if self.safe:
                pulse, fanfare = pulse * .6, fanfare * .6
            return max(pulse, fanfare, self.heart() * .9)

        def heart(self):
            """0..1: Arrhythmia's double thump, on a clock that is not the song's.

            Song time, not wall time, so it freezes with a pause and a seek
            lands on the same phase a straight play-through would. Everything
            else about it is wrong on purpose: 46 BPM against whatever the
            chart is running at, so the two drift through each other for the
            whole cue and never once agree. A camera that pulses ON the beat is
            a light show. A camera that pulses NEAR it is a room with something
            alive in it.
            """
            level = self.level("arrhythmia", 1.0, 1.4)
            if level <= .003:
                return 0.0
            period = 60.0 / AR_HEART_BPM
            t = max(0.0, self.stage.now) % period
            lub = ar_math.exp(-t / .085)
            dub = ar_math.exp(-(t - .30) / .075) * .72 if t >= .30 else 0.0
            if self.safe:
                level *= .6
            return level * max(lub, dub)

        # ---- world: behind the backstage rig and the singers -----------------------

        def draw_world_back(self, layer):
            stage = self.stage
            beat = self.beat()
            foot = self.level("footlights", .9, 1.3)
            # Footlights do not layer over the overhead rig: they REPLACE it.
            # The rig going out is half of what the effect is, and a chart that
            # runs both at once should watch the lamps die, not fight for the
            # frame with a second set of cones.
            spots, fan = self.level("spotlights") * (1 - foot), self.fanfare_glow() * (1 - foot)
            if spots > .003 or fan > .003:
                self._spotlights(layer, beat, spots, fan)
            lasers = self.level("lasers", .15, .3)
            if lasers > .003:
                self._lasers(layer, beat, lasers)
            if fan > .003:
                # A warm wash across the whole floor.
                stage._place(layer, self.texture("glow", "gold"), AR_WORLD[0] * .5, AR_FEET_Y + 30,
                             scale=6.8, sy=1.2, alpha=.30 * fan, additive=True)
            watch = self.level("watchers", 2.2, 2.8)
            if watch > .003:
                self._watchers(layer, watch)

        def _footlights(self, layer, level):
            # Drawn in FRONT of the singers, not behind them. An uplight that
            # cannot reach the people standing in it is not an uplight, and the
            # sprites are fixed artwork that will never relight themselves: the
            # only way to put a face in the wrong light is to put the light on
            # top of it. The veil goes first for the same reason -- what makes
            # a floor lamp read is not the lamp, it is that everything ABOVE
            # the lamp has gone out.
            """The rig inverted: cold light off the floor, thrown up into the dark.

            Everything that makes the overhead rig feel like a show is taken
            out here. The lamps do not sweep -- they drift a couple of degrees
            over thirteen seconds, which is a light nobody is operating. They
            are ash rather than pink or gold. And they throw UP, which is the
            one direction stage lighting never comes from and the direction a
            face is lit from when someone is holding a torch under it.
            """
            stage = self.stage
            now = max(0.0, stage.now)
            veil = renpy.Render(*AR_WORLD)
            veil.blit(renpy.render(stage._solid("#070512"), AR_WORLD[0], AR_WORLD[1], stage.st, stage.at), (0, 0))
            layer.blit(ar_fade(veil, .52 * level), (0, 0))
            for i, (fraction, rest, phase, unused) in enumerate(AR_SPOT_RIGS):
                x = AR_WORLD[0] * fraction
                # 180 degrees turns the cone over: its narrow end is the lamp,
                # now sitting on the floor with the wide end open to the ceiling.
                # It barely moves -- two degrees over thirteen seconds. A lamp
                # that sweeps has somebody operating it, and the point of this
                # rig is that nobody is.
                degrees = 180.0 - rest * .35 + 2.2 * ar_math.sin(2 * ar_math.pi * now / 13.0 + phase)
                self._turned(layer, self._rig("beam", "ash", i), (220, 900), (110, 0),
                             (x, AR_FEET_Y + 10), degrees, .74 * level, yzoom=.74)
                stage._place(layer, self.texture("pool", "ash"), x, AR_FEET_Y + 8,
                             scale=.95, alpha=.62 * level, additive=True)
                stage._place(layer, self.texture("glow", "ash"), x, AR_FEET_Y + 4, scale=.52,
                             alpha=.85 * level, additive=True)
            for side in ("opponent", "player"):
                # Light collecting at their feet and climbing them: the only
                # part of the effect the fixed sprite art can actually show.
                stage._place(layer, self.texture("glow", "ash"), AR_SPOT_X[side], AR_FEET_Y - 46,
                             scale=2.5, sy=1.15, alpha=.42 * level, additive=True)

        def _watchers(self, layer, level):
            """Eyes open in the dark past the stage. They do not approach and they do not leave.

            Each eye is a closed-form function of song time and its own index,
            so a seek lands mid-blink exactly where a play-through would. They
            arrive one at a time as the cue deepens rather than all at once:
            the second eye is the one that lands, because the first could have
            been a lamp.
            """
            stage = self.stage
            now = max(0.0, stage.now)
            for i in range(AR_WATCH_COUNT):
                # Each eye waits its turn: index 0 opens almost at once, the
                # last only if the cue runs long enough to reach full level.
                fade = min(1.0, max(0.0, (level - ar_unit(31, i) * .62) / .38))
                if fade <= .01:
                    continue
                x = 70.0 + ar_unit(31, i, 1) * (AR_WORLD[0] - 140.0)
                y = AR_WATCH_Y[0] + ar_unit(31, i, 2) * (AR_WATCH_Y[1] - AR_WATCH_Y[0])
                phase = ar_unit(31, i, 3) * 11.0
                # Its own blink, on its own period, none of them the song's.
                gap = 3.1 + 4.3 * ar_unit(31, i, 4)
                closed = ar_math.exp(-(((now + phase) % gap) / .085) ** 2)
                open_amount = 1.0 - closed
                if open_amount <= .02:
                    continue
                scale = .40 + .34 * ar_unit(31, i, 5)
                # A drift of a few pixels over half a minute: not enough to
                # catch it moving, enough that it is never quite where it was.
                x += 7.0 * ar_math.sin(2 * ar_math.pi * now / 31.0 + phase)
                tint = "pink" if i % 3 == 1 else "white"
                # The socket goes down first, straight and near-black. Without
                # it a pale eye is one more bright shape on a backdrop made of
                # bright shapes; with it the eye reads at any stage brightness,
                # and what opens is a HOLE with an eye in it rather than an eye
                # painted on the wall.
                stage._place(layer, self.texture("socket"), x, y, scale=scale * 1.25,
                             sy=scale * 1.25 * (.55 + .45 * open_amount), alpha=.88 * fade)
                stage._place(layer, self.texture("glow", tint), x, y, scale=scale * .95,
                             alpha=.16 * fade * open_amount, additive=True)
                stage._place(layer, self.texture("eye", tint), x, y, scale=scale,
                             sy=scale * open_amount, alpha=.92 * fade)

        def _spotlights(self, layer, beat, spots, fan):
            stage = self.stage
            top = -40.0
            reach = AR_FEET_Y - top
            # The backdrop already paints lamp beams, so these run bright enough to read over them.
            # The per-beat lift is a rhythmic change of frame brightness, so
            # the switch holds it at its mean rather than losing the lamps.
            accent = .50 if self.safe else .46 + .16 * ar_beat_envelope(beat, stage.beat_len, .2)
            for i, (fraction, rest, phase, tint) in enumerate(AR_SPOT_RIGS):
                x = AR_WORLD[0] * fraction
                # A fanfare swaps every lamp to gold and doubles the sweep speed.
                for colour, strength, period in ((tint, spots * (1 - fan), 8.0), ("gold", fan, 4.0)):
                    if strength <= .003:
                        continue
                    degrees = rest + 16.0 * ar_math.sin(2 * ar_math.pi * beat / period + phase)
                    theta = ar_math.radians(degrees)
                    # Stretch the cone so its foot always lands on the floor line.
                    stretch = reach / (900.0 * max(.35, ar_math.cos(theta)))
                    self._turned(layer, self._rig("beam", colour, i), (220, 900), (110, 0), (x, top),
                                 degrees, accent * strength, yzoom=stretch)
                    stage._place(layer, self.texture("pool", colour), x - ar_math.tan(theta) * reach, AR_FEET_Y + 6,
                                 alpha=.34 * strength, additive=True)

        def _lasers(self, layer, beat, level):
            stage = self.stage
            tint = AR_LASER_TINTS[int(ar_math.floor(beat / 4.0)) % len(AR_LASER_TINTS)]
            # Steady, and dimmer: a laser fan is high-contrast stripes sweeping
            # the frame, which is a provocation in its own right even when the
            # beams are not pulsing. Dropping the contrast keeps the shot.
            flicker = .85 if self.safe else .70 + .30 * ar_beat_envelope(beat, stage.beat_len, .12)
            if self.safe:
                level *= .6
            spread = .55 + .45 * ar_math.sin(ar_math.pi * beat)
            sweep = 14.0 * ar_math.sin(2 * ar_math.pi * beat / 8.0)
            y = AR_WORLD[1] - 36.0
            for side, (x, direction) in enumerate(((-30.0, 1), (AR_WORLD[0] + 30.0, -1))):
                for k in range(5):
                    elevation = 38.0 + (k - 2) * 9.0 * spread + sweep * direction
                    # 0 degrees points right, so an upward beam turns negative on the
                    # left emitter and mirrors past 180 on the right one.
                    degrees = -elevation if direction > 0 else 180.0 + elevation
                    self._turned(layer, self._rig("laser", tint, side, k), (1600, 22), (0, 11), (x, y),
                                 degrees, .55 * level * flicker)
                stage._place(layer, self.texture("glow", "white"), x + 36 * direction, y, scale=.55,
                             alpha=.6 * level * flicker, additive=True)

        # ---- world: after the backstage rig, before the singers -----------------------

        def draw_world_mid(self, layer):
            level = self.level("blackout", .5, .8)
            if level <= .003:
                return
            stage = self.stage
            veil = renpy.Render(*AR_WORLD)
            veil.blit(renpy.render(stage._solid("#05030c"), AR_WORLD[0], AR_WORLD[1], stage.st, stage.at), (0, 0))
            layer.blit(ar_fade(veil, .66 * level), (0, 0))
            for side in ("opponent", "player"):
                x = AR_SPOT_X[side]
                stage._place(layer, self.texture("beam", "white"), x, -40, scale=1.15, sy=(AR_FEET_Y + 40) / 900.0,
                             alpha=.24 * level, yanchor=0.0, additive=True)
                stage._place(layer, self.texture("pool", "white"), x, AR_FEET_Y + 4, scale=1.1,
                             alpha=.45 * level, additive=True)

        # ---- world: in front of the singers ----------------------------------------------

        def draw_world_front(self, layer):
            if self.reactive:
                self.draw_shockwaves(layer)
            foot = self.level("footlights", .9, 1.3)
            if foot > .003:
                self._footlights(layer, foot)
            level = self.level("haze", .8, 1.2)
            if level <= .003:
                return
            stage = self.stage
            now = max(0.0, stage.now)
            texture = self.texture("haze")
            for speed, alpha, additive, lift in ((22.0, .40, False, 0), (-13.0, .20, True, 40)):
                x = -((now * speed) % 1024.0)
                y = AR_WORLD[1] - 240 - lift
                while x < AR_WORLD[0]:
                    stage._place(layer, texture, x, y, alpha=alpha * level, xanchor=0.0, yanchor=0.0, additive=additive)
                    x += 1024.0

        def doubles(self, side):
            """((dx, dy, alpha), ...) for copies of a singer to stand behind themselves.

            Drawn by ARStage._draw_character, which is the only place in the
            frame where the singer's pose clock is already set for THIS frame,
            so the copies are the same drawing rather than a stale one.

            They breathe apart and back together on a nine-second cycle that no
            chart can land on, and at the bottom of that cycle they are almost
            exactly behind her and almost invisible. What the effect is really
            for is the moment they separate: for a second and a half there are
            three of her, and then there are not, and nothing in the song
            marked either event.
            """
            level = self.level("doubles", 1.1, 1.5)
            if level <= .003:
                return ()
            now = max(0.0, self.stage.now)
            rows = []
            for k in (0, 1):
                swing = ar_math.sin(2 * ar_math.pi * now / (9.4 + 3.1 * k) + k * 2.3)
                reach = abs(swing)
                rows.append(((1 if k else -1) * (12.0 + 64.0 * reach) * level,
                             -5.0 * level * (1.0 - reach),
                             .30 * level * (.5 + .5 * reach)))
            return rows

        def tremor(self, side):
            """(dx, dy, degrees) for a singer who is shaking where she stands.

            Read by ARStage._draw_character, like doubles(). Three sine terms
            at rates that share no common period, so the shake never settles
            into a rhythm the player can read as musical -- the moment it looks
            like dancing the effect has failed. The lean is slower than the
            shake and on its own clock again, so the body drifts off true while
            the shaking rides on top of it.
            """
            level = self.level("convulse", .45, .7)
            if level <= .003:
                return (0.0, 0.0, 0.0)
            now = max(0.0, self.stage.now)
            # Each singer gets her own phase, or they shake in unison, which
            # reads as a camera fault instead of as two people.
            phase = 0.0 if side == "opponent" else 2.7
            if self.safe:
                # High-frequency sprite jitter is one of the things a player
                # turns the switch on to be rid of, even though it is motion
                # rather than light. Slowed as well as shrunk: a slow sway is
                # a different, survivable effect, not a quiet version of this.
                level *= .4
                fast, mid = 7.0, 4.3
            else:
                fast, mid = 41.0, 23.7
            shake = (ar_math.sin(now * fast + phase) * .6
                     + ar_math.sin(now * mid + phase * 1.9) * .4)
            across = ar_math.sin(now * (fast * .73) + phase * 2.4)
            lean = ar_math.sin(now * 3.1 + phase)
            return (AR_CONVULSE_PX * level * shake,
                    AR_CONVULSE_PX * .45 * level * across,
                    AR_CONVULSE_TILT * level * lean)

        def crush_factor(self):
            """The resample factor Bitcrush is asking for, or 0 when it is not running.

            Quantised to AR_CRUSH_STEPS rather than continuous: every distinct
            factor is a cached pair of Transforms plus an offscreen pass per
            crushed child per frame, so a factor that moved smoothly would build
            a new pair every frame and never reuse one. Stepping also looks
            right -- a picture losing resolution drops through modes, it does
            not slide between them.
            """
            level = self.level("bitcrush", .3, .45)
            if level <= .02:
                return 0.0
            index = min(len(AR_CRUSH_STEPS) - 1, int(level * len(AR_CRUSH_STEPS)))
            return AR_CRUSH_STEPS[index]

        def crush(self, child, size, key):
            """``child`` resampled down and back up, or ``child`` itself when Bitcrush is idle.

            `mesh=True` is the whole trick: it forces the child to be rendered
            to a texture at the transform's size, which is the one way in this
            engine to actually LOSE resolution. Render.zoom will not do it (it
            multiplies matrices and resamples nothing) and neither will setting
            mesh on a Render. The outer transform restores the native size, so
            everything that measures this child afterwards -- every anchor in
            _place -- still gets the numbers it expects.
            """
            factor = self.crush_factor()
            if factor <= 0:
                return child
            cache = (key, factor)
            built = self.crushes.get(cache)
            if built is None:
                small = (max(1, int(size[0] / factor)), max(1, int(size[1] / factor)))
                built = self.crushes[cache] = Transform(
                    Transform(child, xysize=small, nearest=True, mesh=True),
                    xysize=size, nearest=True, mesh=True)
            return built

        def gutter(self):
            """0..1 of darkness over the frame from a stage rig that is failing.

            Three beaters at rates that share no common period, multiplied: the
            lamp is mostly low, recovers where all three happen to agree, and
            never repeats the same recovery twice inside a song. The fastest
            thing this produces is around 2.2Hz, under the photosensitive band
            -- but it is still a large repeated change of frame brightness, so
            the switch holds it at a flat dim. The stage stays dark; it just
            stops being a lamp that is dying and becomes one that is out.
            """
            level = self.level("gutter", .5, .9)
            if level <= .003:
                return 0.0
            if self.safe:
                return .40 * level
            now = max(0.0, self.stage.now)
            a = .5 + .5 * ar_math.sin(2 * ar_math.pi * now / 1.37)
            b = .5 + .5 * ar_math.sin(2 * ar_math.pi * now / .91 + 1.1)
            c = .5 + .5 * ar_math.sin(2 * ar_math.pi * now / 2.53 + 2.7)
            return level * (.62 - .48 * (a * b * c) ** .55)

        def blit_world(self, r, wrap, x, y):
            """Put the world layer into the frame. A Tear puts it in in slipped bands.

            This is the one effect that has to happen at the seam between the
            world and the frame, because what it does is break the world into
            strips and move them relative to each other. It is refused outright
            under Photosensitive Mode: a high-contrast displacement of the
            whole picture is on the short list of things the switch exists for,
            and there is no gentle version of losing the horizontal hold.
            """
            found = None
            if "tear" in self.used and not self.safe:
                for index, age in self.tracks["tear"].recent(self.stage.now, AR_TEAR_TIME):
                    found = (index, age)
            if found is None:
                r.subpixel_blit(wrap, (x, y))
                return
            index, age = found
            decay = (1.0 - age / AR_TEAR_TIME) ** 1.5
            # Quantised, so the slip JUDDERS in steps rather than sliding: a
            # picture off its hold jumps between positions, it does not pan.
            step = int(age * 26.0)
            for i in range(AR_TEAR_BANDS):
                top = int(720.0 * i / AR_TEAR_BANDS)
                bottom = int(720.0 * (i + 1) / AR_TEAR_BANDS)
                slip = (ar_unit(7700 + index * 53, i, step) * 2.0 - 1.0) * AR_TEAR_PX * decay
                band = renpy.Render(1280, bottom - top)
                band.xclipping = True
                band.yclipping = True
                band.subpixel_blit(wrap, (x + slip, y - top))
                r.blit(band, (0, top))

        def _veins(self, r, level):
            """A network branching in under the picture from the four corners, pulsing.

            Placed exactly as Rot is -- corner-anchored, a quarter turn each
            time, pinned to the FRAME and never to a spot in the backdrop art.
            What makes it read as alive rather than as decoration is that it
            pulses on the HEART's clock (46 BPM, AR_HEART_BPM) whether or not
            Arrhythmia is charted: run the two together and they agree without
            the charter doing anything, and run Veins alone and there is still
            something with a pulse behind the stage.
            """
            now = max(0.0, self.stage.now)
            period = 60.0 / AR_HEART_BPM
            t = now % period
            beat = ar_math.exp(-t / .13) + .6 * (ar_math.exp(-(t - .30) / .09) if t >= .30 else 0.0)
            # A wide swell, not a nudge. These are thin dark lines over busy
            # stage art: what makes them read is not their alpha at rest, it is
            # that they visibly throb, and a static screenshot is the one place
            # that never shows.
            swell = .68 + .58 * min(1.0, beat)
            for i, point in enumerate(((0, 0), (1280, 0), (1280, 720), (0, 720))):
                reach = min(1.0, max(0.0, (level - i * .11) / .67))
                if reach <= .01:
                    continue
                zoom = (.60 + 1.45 * reach) * (1.0 + .012 * beat)
                self._turned(r, self._rig("veins", None, i), (512, 512), (0, 0), point, 90.0 * i,
                             min(1.0, reach * 1.25) * .95 * swell, additive=False, zoom=zoom)

        def _blood(self, r, level):
            """It runs down from the top of the frame, and what gets there gathers.

            The runs are one tileable strip laid end to end and scaled DOWN the
            frame as the cue deepens, so the leading edge travels instead of the
            whole picture fading up. Each tile is offset by its own amount, so
            the seam between two copies never reads as a repeat.
            """
            stage = self.stage
            now = max(0.0, stage.now)
            reach = AR_BLOOD_REACH * ar_ease_out(min(1.0, level * 1.15))
            texture = self.texture("blood")
            for i in range(3):
                # Each strip starts a little further up, so the runs arrive ragged.
                lag = ar_unit(5150, i, 2) * .30
                travel = max(0.0, min(1.0, (level - lag) / max(.05, 1.0 - lag)))
                if travel <= .01:
                    continue
                stage._place(r, texture, i * 512.0 - 8.0, -14.0, sy=reach * travel / 640.0,
                             alpha=.92, xanchor=0.0, yanchor=0.0)
            # What has run down gathers at the foot of the frame, and creeps up.
            pool = max(0.0, (level - .45) / .55)
            if pool > .01:
                height = int(AR_BLOOD_POOL * ar_ease_out(pool))
                if height >= 2:
                    self._plate(r, "#3d040c", .88, height=height, top=720 - height)

        # ---- screen: the crowd sits under the vignette ---------------------------------

        def draw_crowd(self, r):
            level = self.level("crowd", .6, .8)
            hollow = self.level("hollow", 1.2, 1.6)
            if level <= .003:
                return
            stage = self.stage
            beat = self.beat()
            # Foreground parallax: the crowd slides faster than the stage as the camera pans.
            parallax = -(stage.view[0] - AR_WORLD[0] * .5) * 1.35
            # Hollow sinks the band as well as putting it out, so the room in
            # front of the stage empties downward as much as it goes dark.
            rise = (1 - level) * 70 + 30 * hollow
            band = self.texture("crowd")
            offset = parallax % 1280.0
            for x in (offset - 1280.0, offset):
                stage._place(r, band, x, 734 + rise, xanchor=0.0, yanchor=1.0)
            # They stop answering the beat before they stop being there. By the
            # time the sticks start going out the crowd has already been still
            # for a bar or two, which is the part that reads as wrong.
            hop = ar_beat_envelope(beat, stage.beat_len, .18) * max(0.0, 1.0 - hollow * 1.6)
            for i in range(24):
                u = ar_unit(7, i)
                # Each stick has its own place in the queue and goes out over a
                # short window of its own, so the room darkens raggedly rather
                # than dimming like something on a fader.
                alive = min(1.0, max(0.0, (ar_unit(7, i, 4) * .88 + .12 - hollow) / .12))
                x = ((i * 57.3 + u * 30 + parallax * 1.05) % 1400.0) - 60
                y = 650 + 10 * ar_unit(7, i, 1) + rise - 12 * hop * (1.0 if i % 3 else .4)
                degrees = 20.0 * ar_math.sin(ar_math.pi * beat + u * 6.283) * max(.12, alive)
                tint = AR_STICK_TINTS[i % len(AR_STICK_TINTS)]
                stage._place(r, self.texture("glow", AR_GLOW_FOR[tint]), x, y - 20, scale=.28,
                             alpha=.45 * level * alive, additive=True)
                self._turned(r, self._rig("stick", tint, i), (14, 48), (7, 40), (x, y), degrees,
                             .95 * level * (.22 + .78 * alive))
            if hollow > .003:
                # The front of the house goes with them.
                self._plate(r, "#05030c", .42 * hollow * level, height=170, top=550)

        # ---- screen: over the vignette, under the HUD ------------------------------------

        def draw_screen(self, r):
            stage = self.stage
            now = stage.now
            # The dread set goes in UNDER the concert set, in the order the
            # picture is being taken apart: Rot eats the corners, Dread closes
            # what is left, Gutter dims the whole of it, the heart pushes on
            # it. Everything below that is still the show, happening inside.
            rot = self.level("rot", 2.0, 2.6)
            if rot > .003:
                self._rot(r, rot)
            veins = self.level("veins", 2.4, 3.0)
            if veins > .003:
                self._veins(r, veins)
            dread = self.level("dread", 1.6, 2.2)
            if dread > .003:
                self._dread(r, dread)
            blood = self.level("blood", 3.2, 4.0)
            if blood > .003:
                self._blood(r, blood)
            self._plate(r, "#04030a", self.gutter() * .78)
            heart = self.heart()
            if heart > .003:
                # The squeeze that goes with the thump. Small, and under 1Hz --
                # felt rather than seen, which is the whole point of putting a
                # pulse on a clock the player cannot predict.
                self._plate(r, "#0a0410", heart * (.05 if self.safe else .11))
            glow = self.fanfare_glow()
            if glow > .003:
                pulse = ar_beat_envelope(self.beat(), stage.beat_len, .22)
                stage._place(r, self.texture("frame", "gold"), 640, 360, alpha=(.28 + .30 * pulse) * glow, additive=True)
            if "fanfare" in self.used:
                self._fanfare_rain(r, now)
            if "confetti" in self.used:
                for index, age in self.tracks["confetti"].recent(now, 4.6):
                    self._volley(r, 1000 + index * 131, age)
            for seed, born in self.volleys:
                if 0 <= now - born < 4.6:
                    self._volley(r, seed, now - born)
            if "sparks" in self.used:
                for index, age in self.tracks["sparks"].recent(now, 1.6):
                    self._sparks(r, 5000 + index * 97, age)
            if "fracture" in self.reactive:
                self._fracture(r)
            static = self.level("static", .35, .5)
            if static > .003:
                self._static(r, static)
            # A white frame is the textbook provocation, so under the switch it
            # becomes a SWELL: same cue, same moment, a fifth of the amplitude
            # over three times the time, which the eye reads as the room
            # brightening rather than as a flash.
            flash = 0.0
            if "flash" in self.used:
                for index, age in self.tracks["flash"].recent(now, 1.2):
                    flash = max(flash, .15 * ar_math.exp(-age / .42) if self.safe
                                else .55 * ar_math.exp(-age / .16))
            for born in self.flashes:
                age = now - born
                if 0 <= age < 1.2:
                    flash = max(flash, .09 * ar_math.exp(-age / .38) if self.safe
                                else .32 * ar_math.exp(-age / .14))
            self._plate(r, "#ffffff", flash, additive=True)
            level, tint = self.strobe()
            if level > .003:
                self._plate(r, tint, level, additive=True)
            if "glimpse" in self.used:
                self._glimpse(r, now)
            if "cut" in self.used:
                # Last of the dread set, and over everything in it: a cut puts
                # the show out, not one layer of it. The HUD is drawn after this
                # and survives, which is deliberate -- the lanes stay readable
                # and the player is still expected to keep playing through it.
                for index, age in self.tracks["cut"].recent(now, 1.2):
                    if self.safe:
                        # No step. A slow dip to a bit over half, and back.
                        dark = .58 * ar_math.exp(-((age - .30) / .27) ** 2)
                    else:
                        dark = 1.0 if age < .075 else max(0.0, 1.0 - (age - .075) / .20)
                    self._plate(r, "#000000", dark)
            self._signal(r, now)

        # ---- the signal: what the picture itself is doing ------------------------------

        def _signal(self, r, now):
            """Colour and contrast over the finished stage, under the HUD.

            Order is a processing chain, not a pile: grade first (Infrared, Deep
            Fried, Red Wash), then invert what came out of it. Inverting first
            and grading afterwards would tint the negative instead of negating
            the tint, which looks like a mistake rather than a decision.
            """
            infra = self.level("infrared", .5, .7)
            if infra > .003:
                self._infrared(r, infra)
            fried = self.level("fried", .4, .6)
            if fried > .003:
                self._fried(r, fried)
            red = self.level("redwash", .55, .85)
            if red > .003:
                # A pulse on a red wash is deep-red flicker, which is its own
                # named provocation -- the switch holds it at its mean and
                # keeps the wash, which is the part that was worth having.
                if self.safe:
                    swell = 1.0
                else:
                    period = 60.0 / AR_HEART_BPM
                    t = now % period
                    swell = .84 + .30 * ar_math.exp(-t / .16)
                self._plate(r, "#ff1c12", min(1.0, .82 * red * swell), blend="multiply")
            self._negative(r, now)

        def _infrared(self, r, level):
            """A night camera: one channel, blown out, grainy, behind a grille.

            Multiplying by pure green zeroes the red and blue channels, which
            IS a monochrome conversion -- and it costs one blend-mode plate.
            Screen on top pushes the bright end towards white so the picture
            blooms the way a gained-up sensor does.
            """
            stage = self.stage
            now = max(0.0, stage.now)
            self._plate(r, "#00ff00", level, blend="multiply")
            self._plate(r, "#1f5e28", .82 * level, blend="ar_screen")
            grain = self.texture("static")
            if self.safe:
                ox = oy = 0.0
            else:
                step = int(now * 20.0)
                ox = -ar_unit(4242, step) * 512.0
                oy = -ar_unit(4242, step, 1) * 512.0
            for i in range(3):
                for j in range(2):
                    stage._place(r, grain, ox + i * 512.0, oy + j * 512.0,
                                 alpha=.30 * level, xanchor=0.0, yanchor=0.0, additive=True)
            # The grille. It rolls, unless holding a moving high-contrast stripe
            # pattern still is the whole reason someone turned the switch on.
            y = 0.0 if self.safe else -((now * 26.0) % 4.0)
            stage._place(r, self.texture("scanlines"), 0.0, y, alpha=.75 * level,
                         xanchor=0.0, yanchor=0.0)

        def _fried(self, r, level):
            """Contrast and colour pushed past what the picture can hold.

            Multiply crushes the dark end, screen blows the bright end, and a
            saturated multiply on top puts the cast on. That stack IS a contrast
            curve; there is no more to deep frying than doing it too hard.
            """
            stage = self.stage
            self._plate(r, "#6e6e6e", .95 * level, blend="multiply")
            self._plate(r, "#a85c00", .92 * level, blend="ar_screen")
            self._plate(r, "#ff7a00", .48 * level, blend="multiply")
            now = max(0.0, stage.now)
            grain = self.texture("static")
            if self.safe:
                ox = oy = 0.0
                alpha = .26 * level
            else:
                step = int(now * 17.0)
                ox = -ar_unit(6161, step) * 512.0
                oy = -ar_unit(6161, step, 1) * 512.0
                alpha = .42 * level
            for i in range(3):
                for j in range(2):
                    stage._place(r, grain, ox + i * 512.0, oy + j * 512.0,
                                 alpha=alpha, xanchor=0.0, yanchor=0.0, additive=True)

        def _negative(self, r, now):
            """Invert, as a one-frame glitch and as a state the picture holds in.

            A PARTIAL invert is a flat grey wash -- lerp(dst, 1-dst, .5) is .5
            at every pixel, whatever the picture was. That is measured, not
            assumed, and it decides both of these: the burst snaps to full and
            holds, and the span ramps through the grey fast enough that nobody
            reads it as a fade to nothing.

            Under Photosensitive Mode the burst is removed outright -- a
            full-frame luminance flip in one frame is exactly what the switch is
            for, and there is no softer version of it that is still the effect.
            The SPAN survives, because what is dangerous is the transition and
            not the state: it ramps over three quarters of a second at each end
            and then simply holds inverted, which is a still picture.
            """
            level = 0.0
            if "negative" in self.used:
                ramp = .75 if self.safe else .14
                level = self.level("negative", ramp, ramp)
            if "invert" in self.used and not self.safe:
                for index, age in self.tracks["invert"].recent(now, AR_INVERT_HOLD):
                    level = 1.0
            if level > .003:
                self._plate(r, "#ffffff", min(1.0, level), blend="ar_invert")

        def _dread(self, r, level):
            """The dark closing in, on a seven-second breath that belongs to no tempo.

            One texture, blitted over itself. Alpha compounds as 1-(1-a)^n, so
            a second and third pass darken the SHOULDER of the gradient far
            faster than its middle: the aperture narrows while the centre of
            the frame stays as bright as it was. Scaling a vignette would have
            done this too, at the cost of a texture big enough to still cover
            1280x720 after it had been scaled down.
            """
            now = max(0.0, self.stage.now)
            breath = .5 + .5 * ar_math.sin(2 * ar_math.pi * now / 7.3)
            strength = level * (.60 + .40 * breath)
            shroud = self.texture("shroud")
            for cut, gain in ((0.0, 1.15), (.42, .92), (.74, .80)):
                alpha = (strength - cut) / max(.001, 1.0 - cut) * gain
                if alpha <= .01:
                    break
                self.stage._place(r, shroud, 640, 360, alpha=min(1.0, alpha))

        def _rot(self, r, level):
            """Something creeping in at the four corners of the FRAME, not of the stage.

            Straight, not additive, and near-black: it takes the picture away
            instead of putting light on it, which is what separates it from
            every concert effect in the file. Corner-anchored and rotated a
            quarter turn each time, so it is pinned to the frame and not to any
            spot in the backdrop art.
            """
            now = max(0.0, self.stage.now)
            for i, point in enumerate(((0, 0), (1280, 0), (1280, 720), (0, 720))):
                # Each corner is behind the last, so they arrive one at a time.
                reach = min(1.0, max(0.0, (level - i * .13) / .61))
                if reach <= .01:
                    continue
                zoom = (.55 + 1.35 * reach) * (1.0 + .02 * ar_math.sin(now * .41 + i * 1.7))
                self._turned(r, self._rig("rot", None, i), (512, 512), (0, 0), point, 90.0 * i,
                             min(1.0, reach * 1.35) * .84, additive=False, zoom=zoom)

        def _static(self, r, level):
            """Signal grain, and the seam that walks down a picture losing its hold.

            The grain tiles at 1:1 and is never scaled, so every speck is one
            texel and the field does not shimmer from resampling. Its offset is
            quantised to a 14Hz step rather than moving every frame: real noise
            resettles, it does not slide, and a closed-form step also means a
            seek lands on the same field a play-through would.
            """
            stage = self.stage
            now = max(0.0, stage.now)
            grain = self.texture("static")
            if self.safe:
                # Held still, and quieter. A stationary grain field is texture;
                # a grain field resettling 14 times a second is flicker.
                ox = oy = 0.0
                alpha = .20 * level
            else:
                step = int(now * 14.0)
                ox = -ar_unit(9001, step) * 512.0
                oy = -ar_unit(9001, step, 1) * 512.0
                alpha = .34 * level
            for i in range(3):
                for j in range(2):
                    stage._place(r, grain, ox + i * 512.0, oy + j * 512.0,
                                 alpha=alpha, xanchor=0.0, yanchor=0.0, additive=True)
            if not self.safe:
                # A wide high-contrast band sweeping the frame is its own
                # provocation, so this half of the effect does not survive the
                # switch even though the grain does.
                y = ((now * 62.0) % 1060.0) - 180.0
                stage._place(r, self.texture("rollbar"), 0.0, y, alpha=.30 * level,
                             xanchor=0.0, yanchor=0.0, additive=True)

        def _fracture(self, r):
            """Cracks spreading from whoever sang, in their colour, that stay after the note.

            Each crack keeps the angle it was born with for as long as it is on
            screen, so the break looks struck rather than animated. They are
            pinned to the singer's position in the frame THIS frame, derived
            from AR_SPOT_X and the live camera -- never from a spot in the art.
            """
            live = self._live_keyed("fracture", AR_CRACK_TIME)
            for when, age, gain, side in live[-AR_CRACK_MAX:]:
                seed = int(when * 1000.0)
                t = age / AR_CRACK_TIME
                # Under the switch the crack FADES UP instead of appearing:
                # same drawing, no step change in brightness anywhere.
                rise = min(1.0, age / .22) if self.safe else 1.0
                alpha = (1.0 - t) ** 1.6 * gain * rise * (.65 if self.safe else .80)
                if alpha <= .004:
                    continue
                zoom = (.50 + 1.05 * gain) * (.74 + .26 * ar_ease_out(min(1.0, age / .16)))
                x = self.screen_x(AR_SPOT_X[side]) + (ar_unit(seed, 1, 8) * 2.0 - 1.0) * 46.0
                y = 300.0 + (ar_unit(seed, 2, 8) * 2.0 - 1.0) * 120.0
                self._turned(r, self._rig("crack", AR_SIDE_TINT[side], seed % 8), (512, 512),
                             (256, 256), (x, y), ar_unit(seed, 3, 8) * 360.0, alpha, zoom=zoom)

        def _glimpse(self, r, now):
            """Someone is standing there.

            The restraint IS the effect. Five frames, under half alpha, at a
            size and a spot that change every time, with no stinger on the
            sound track and nothing in the chart marking it. It is not meant to
            make the player jump; it is meant to make them unsure, thirty
            seconds later, whether it happened at all.

            Under Photosensitive Mode it is not removed -- it is SLOWED. It
            fades up over half a second and back down over three quarters, at a
            lower alpha. Nobody is ambushed, and there is still someone there.
            """
            hold = 1.4 if self.safe else AR_GLIMPSE_HOLD
            for index, age in self.tracks["glimpse"].recent(now, hold):
                seed = 4400 + index * 179
                alpha = .34 * ar_math.exp(-((age - .55) / .42) ** 2) if self.safe else .52
                if alpha <= .01:
                    continue
                # The frame sinks with the figure. A near-black silhouette over
                # a lit stage at half alpha simply does not read -- the shape
                # needs the room to go quiet around it, which is also what the
                # moment feels like when it works.
                self._plate(r, "#05030c", alpha * .55)
                self.stage._place(r, self.texture("figure"),
                                  1280.0 * (.20 + .60 * ar_unit(seed, 0, 1)),
                                  706.0 - 24.0 * ar_unit(seed, 0, 3),
                                  scale=.78 + .30 * ar_unit(seed, 0, 2),
                                  alpha=min(1.0, alpha * 1.5), yanchor=1.0)

        def _piece(self, r, seed, x, y, age, alpha):
            if alpha <= .003 or not (-30 < x < 1310 and -30 < y < 750):
                return
            tint = AR_CONFETTI_TINTS[int(ar_unit(seed, 0, 3) * len(AR_CONFETTI_TINTS))]
            spin = 5.0 + 7.0 * ar_unit(seed, 0, 4)
            phase = ar_unit(seed, 0, 5) * 6.283
            # Tumbling paper: one axis flips edge-on and back while the other breathes.
            sy = .18 + .82 * abs(ar_math.cos(spin * age + phase))
            sx = .55 + .45 * abs(ar_math.sin(spin * .6 * age + phase))
            self.stage._place(r, self.texture("confetti", tint), x, y, scale=sx, sy=sy, alpha=alpha)

        def _fanfare_rain(self, r, now):
            rate, life = 6.0, 11.0
            for start, end in self.fanfare.cues:
                if now < start or now > end + life:
                    continue
                first = max(0, int(ar_math.floor((now - life - start) * rate)))
                last = int(ar_math.floor((min(now, end) - start) * rate))
                seed_base = int(start * 1000)
                for k in range(first, last + 1):
                    age = now - (start + k / rate)
                    if age < 0:
                        continue
                    seed = seed_base * 7 + k
                    fall = 70.0 + 60.0 * ar_unit(seed, k, 1)
                    y = -20.0 + fall * age
                    if y > 745:
                        continue
                    x = 1280.0 * ar_unit(seed, k, 2) + 40.0 * ar_math.sin(1.3 * age + 6.283 * ar_unit(seed, k, 6))
                    self._piece(r, seed, x, y, age, min(1.0, age / .3, (745.0 - y) / 80.0))

        def _volley(self, r, seed, age):
            """Two confetti cannons firing up and in from the bottom corners."""
            tau = .42
            drag = tau * (1 - ar_math.exp(-age / tau))
            fade = min(1.0, (4.6 - age) / .8)
            for j in range(70):
                left = j % 2 == 0
                vx = (260.0 + 700.0 * ar_unit(seed, j, 1)) * (1 if left else -1)
                vy = -(900.0 + 650.0 * ar_unit(seed, j, 2))
                fall = 70.0 + 60.0 * ar_unit(seed, j, 6)
                x = (-10.0 if left else 1290.0) + vx * drag + 26.0 * ar_math.sin(1.7 * age + j)
                y = 740.0 + vy * drag + fall * (age - drag)
                self._piece(r, seed * 3 + j, x, y, age, fade)

        def _sparks(self, r, seed, age):
            """Two spark fountains at the bottom edges of the frame."""
            stage = self.stage
            for j in range(56):
                life = .9 + .6 * ar_unit(seed, j, 1)
                if age >= life:
                    continue
                left = j % 2 == 0
                angle = ar_math.radians(8 + 22 * ar_unit(seed, j, 2)) * (1 if left else -1)
                speed = 620.0 + 520.0 * ar_unit(seed, j, 3)
                x = (70.0 if left else 1210.0) + ar_math.sin(angle) * speed * age
                y = 730.0 - ar_math.cos(angle) * speed * age + 700.0 * age * age
                fade = 1 - age / life
                stage._place(r, self.texture("glow", "gold"), x, y, scale=.10 + .06 * fade, alpha=.9 * fade, additive=True)
                stage._place(r, self.texture("glow", "white"), x, y, scale=.035, alpha=fade, additive=True)
            if age < .35:
                for x in (70.0, 1210.0):
                    stage._place(r, self.texture("glow", "gold"), x, 720, scale=1.0, alpha=.7 * (1 - age / .35), additive=True)

        # ---- HUD ------------------------------------------------------------------------

        def draw_strum_glow(self, hud, ry):
            glow = self.fanfare_glow()
            if glow <= .003:
                return
            stage = self.stage
            pulse = ar_beat_envelope(self.beat(), stage.beat_len, .18)
            for side in ((0, 1) if stage.game.duet else (1,)):
                for lane in range(4):
                    stage._place(hud, self.texture("ring", "gold"), ar_lane_x(side, lane), ry, scale=.46 + .04 * pulse,
                                 alpha=(.35 + .30 * pulse) * glow, additive=True)

        def draw_banner(self, hud):
            level = self.level("fanfare", .2, .5)
            if level <= .003:
                return
            stage = self.stage
            inside, lit, multiplier, streak = stage.game.fanfare_state(stage.now)
            cy = 158 if stage.downscroll else 592
            pulse = ar_beat_envelope(self.beat(), stage.beat_len, .14)
            if lit or not inside:
                word = ("FANFARE ×%d" % multiplier) if inside else "FANFARE"
                stage._place(hud, self.texture("burst", "gold"), 640, cy, scale=.24 + .03 * pulse,
                             alpha=.45 * level, additive=True)
                stage._place(hud, stage._text(word, 28, AR_GOLD, AR_FONT, ((6, AR_INK, 0, 3), (3, "#ffffff", 0, 0))),
                             640, cy, scale=1 + .08 * pulse, alpha=level)
            else:
                stage._place(hud, stage._text("FANFARE OUT", 22, "#b9a8d6", AR_FONT, ((5, AR_INK, 0, 2),)),
                             640, cy - 9, alpha=level)
                stage._place(hud, stage._text("%d / %d TO RELIGHT" % (streak, AR_FANFARE_RELIGHT), 14, "#ffffff",
                                              AR_UI_FONT, ((3, AR_INK, 0, 1),)), 640, cy + 15, alpha=level)
