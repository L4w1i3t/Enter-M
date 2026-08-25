init python:
    import weakref as _fx_weakref

    # Surface cache lives on the renpy module itself, which is never
    # serialized by the save/rollback system.  This keeps raw pygame
    # Surfaces completely out of any dict that Matsu'Py might pickle.
    #
    # IT IS KEYED BY THE DISPLAYABLE, NOT BY id(). The original keyed on
    # id(self) against a plain dict, which is wrong twice over:
    #
    #   * NOTHING EVER REMOVED AN ENTRY. Each Invert/Tear holds a full
    #     screenshot at *drawable* resolution -- 1920x1080x4 is 8MB, and a
    #     fullscreen 4K panel is 33MB -- so every glitch beat leaked one of
    #     those for the rest of the session. A scene that tears a dozen times
    #     was carrying a hundred megabytes of dead pygame Surfaces.
    #   * id() IS REUSED. CPython hands a freed object's address to the next
    #     allocation of the same size, so a new Tear could be born already
    #     "cached" -- holding the *previous* effect's screenshot, which is a
    #     stale frame of a scene the player has already left.
    #
    # A WeakKeyDictionary fixes both: the entry dies with the displayable that
    # owns it, and identity is the object rather than a recycled integer.
    # Displayable defines only __ne__ (renpy/display/core.py), so it keeps the
    # default identity hash and is both hashable and weak-referenceable.
    if not hasattr(renpy, '_effect_srf_cache'):
        renpy._effect_srf_cache = _fx_weakref.WeakKeyDictionary()

    # Tear's per-piece slices, kept here for the same reason and on the same
    # terms as the screenshots above: they are Surface VIEWS, so holding one on
    # the displayable would put a Surface back inside a picklable object and
    # undo the invariant this cache exists to maintain.
    if not hasattr(renpy, '_effect_slice_cache'):
        renpy._effect_slice_cache = _fx_weakref.WeakKeyDictionary()

    def screenshot_srf():
        srf = renpy.display.draw.screenshot(None)
        return srf

    def invert():
        srf = screenshot_srf()
        inv = renpy.Render(srf.get_width(), srf.get_height()).canvas().get_surface()
        inv.fill((255,255,255,255))
        inv.blit(srf, (0,0), None, 2)
        return inv

    class Invert(renpy.Displayable):
        def __init__(self, delay=0.0, screenshot_delay=0.0):
            super(Invert, self).__init__()
            width, height = renpy.get_physical_size()
            # `//`, not `/`. Under Python 3 this was true division, so both
            # dimensions reached renpy.Render() as floats.
            self.width = int(width)
            self.height = int(width) * 9 // 16
            renpy._effect_srf_cache[self] = invert()
            self.delay = delay

        def render(self, width, height, st, at):
            srf = renpy._effect_srf_cache.get(self)
            if srf is None:
                srf = invert()
                renpy._effect_srf_cache[self] = srf
            render = renpy.Render(self.width, self.height)
            if st >= self.delay:
                render.blit(srf, (0, 0))
            return render

    def hide_windows_enabled(enabled=True):
        global _windows_hidden
        _windows_hidden = not enabled

screen invert(length, delay=0.0):
    add Invert(delay) size (1280, 720)
    timer delay action PauseAudio("music")
    timer delay action Play("sound", audio.glitch1)
    timer length + delay action Hide("invert")
    on "show" action Function(hide_windows_enabled, enabled=False)
    on "hide" action PauseAudio("music", False)
    on "hide" action Stop("sound")
    on "hide" action Function(hide_windows_enabled, enabled=True)

init python:
    class TearPiece:
        def __init__(self, startY, endY, offtimeMult, ontimeMult, offsetMin, offsetMax):
            self.startY = startY
            self.endY = endY
            self.offTime = (random.random() * 0.2 + 0.2) * offtimeMult
            self.onTime = (random.random() * 0.2 + 0.2) * ontimeMult
            self.offset = 0
            self.offsetMin = offsetMin
            self.offsetMax = offsetMax

        def update(self, st):
            st = st % (self.offTime + self.onTime)
            if st > self.offTime and self.offset == 0:
                self.offset = random.randint(self.offsetMin, self.offsetMax)
            elif st <= self.offTime and self.offset != 0:
                self.offset = 0

    class Tear(renpy.Displayable):
        def __init__(self, number, offtimeMult, ontimeMult, offsetMin, offsetMax, srf=None):
            super(Tear, self).__init__()
            width, height = renpy.get_physical_size()
            # Integer floor division throughout. Under Python 3 `/` is true
            # division, so height came out a float and then
            # random.randint(10, self.height - 10) raised
            # "non-integer arg 1 for randrange()" -- this effect could not run
            # at all on Matsu'Py 8 until now.
            if float(width) / float(height) > 16.0 / 9.0:
                self.width = int(height) * 16 // 9
                self.height = int(height)
            else:
                self.width = int(width)
                self.height = int(width) * 9 // 16
            self.number = number
            renpy._effect_srf_cache[self] = srf if srf else screenshot_srf()
            # Slice geometry is fixed for the life of the effect, so the
            # subsurfaces are cut once and memoized instead of being re-cut per
            # piece per frame. Only `offset` moves, and that is a blit
            # coordinate.
            renpy._effect_slice_cache.pop(self, None)
            self.pieces = []
            tearpoints = [0, self.height]
            for i in range(number):
                tearpoints.append(random.randint(10, self.height - 10))
            tearpoints.sort()
            for i in range(number+1):
                self.pieces.append(TearPiece(tearpoints[i], tearpoints[i+1], offtimeMult, ontimeMult, offsetMin, offsetMax))

        def _slices_for(self, srf):
            """One subsurface per piece off `srf`, cut once and memoized."""
            entry = renpy._effect_slice_cache.get(self)
            if entry is not None and entry[0] is srf:
                return entry[1]

            slices = []
            for piece in self.pieces:
                top = max(0, piece.startY - 1)
                rows = max(0, min(piece.endY, self.height) - piece.startY)
                slices.append(
                    srf.subsurface((0, top, self.width, rows)) if rows > 0 else None)

            renpy._effect_slice_cache[self] = (srf, slices)
            return slices

        def render(self, width, height, st, at):
            srf = renpy._effect_srf_cache.get(self)
            if srf is None:
                srf = screenshot_srf()
                renpy._effect_srf_cache[self] = srf
                renpy._effect_slice_cache.pop(self, None)
            render = renpy.Render(self.width, self.height)
            render.blit(srf, (0,0))
            slices = self._slices_for(srf)
            for piece, subsrf in zip(self.pieces, slices):
                piece.update(st)
                if subsrf is not None:
                    render.blit(subsrf, (piece.offset, piece.startY))
            renpy.redraw(self, 0)
            return render

# Screen parameter 'srf' removed -- no callers pass it and keeping a
# Surface reference in the screen scope would poison the rollback log.
screen tear(number=10, offtimeMult=1, ontimeMult=1, offsetMin=0, offsetMax=50):
    zorder 150
    add Tear(number, offtimeMult, ontimeMult, offsetMin, offsetMax) size (1280,720)
    on "show" action Function(hide_windows_enabled, enabled=False)
    on "hide" action Function(hide_windows_enabled, enabled=True)

init python:
    import math
    class ParticleBurst(object):
        def __init__(self, theDisplayable, explodeTime=0, numParticles=20, particleTime = 0.500, particleXSpeed = 3, particleYSpeed = 5):
            self.sm = SpriteManager(update=self.update)

            self.stars = [ ]
            self.displayable = theDisplayable
            self.explodeTime = explodeTime
            self.numParticles = numParticles
            self.particleTime = particleTime
            self.particleXSpeed = particleXSpeed
            self.particleYSpeed = particleYSpeed
            self.gravity = 240
            self.timePassed = 0

            for i in range(self.numParticles):
                self.add(self.displayable, 1)

        def add(self, d, speed):
            s = self.sm.create(d)
            speed = random.random()
            angle = random.random() * 3.14159 * 2
            xSpeed = speed * math.cos(angle) * self.particleXSpeed
            ySpeed = speed * math.sin(angle) * self.particleYSpeed - 1
            s.x = xSpeed * 24
            s.y = ySpeed * 24
            pTime = self.particleTime
            self.stars.append((s, ySpeed, xSpeed, pTime))

        def update(self, st):
            # REBUILT, NOT POPPED. The original walked self.stars with a
            # separate counter and popped from the same list mid-iteration:
            # every removal shifted the tail down one while the counter kept
            # advancing, so the particle after a dead one was skipped -- it was
            # never updated and never destroyed again on that pass. The burst
            # therefore left a residue of frozen sprites behind, and
            # `self.stars.pop(sindex)` was removing whatever had slid into that
            # slot rather than the star just destroyed.
            #
            # A burst is small and short-lived, so rebuilding the survivor list
            # is cheaper than the index bookkeeping and cannot go wrong.
            alive = []
            for s, ySpeed, xSpeed, particleTime in self.stars:
                if st < particleTime:
                    s.x = xSpeed * 120 * (st + .20)
                    s.y = (ySpeed * 120 * (st + .20) + (self.gravity * st * st))
                    alive.append((s, ySpeed, xSpeed, particleTime))
                else:
                    s.destroy()
            self.stars = alive
            # Nothing left to move: stop asking SpriteManager for frames.
            return 0 if alive else None

    class Blood(object):
        def __init__(self, theDisplayable, density=120.0, particleTime=1.0, dripChance=0.05, dripSpeedX=0.0, dripSpeedY=120.0, dripTime=180.0, burstSize=100, burstSpeedX=200.0, burstSpeedY=400.0, numSquirts=4, squirtPower=400, squirtTime=0.25):
            self.sm = SpriteManager(update=self.update)
            self.drops = []
            self.squirts = []
            self.displayable = theDisplayable
            self.density = density
            self.particleTime = particleTime
            self.dripChance = dripChance
            self.dripSpeedX = dripSpeedX
            self.dripSpeedY = dripSpeedY
            self.gravity = 800.0
            self.dripTime = dripTime
            self.burstSize = burstSize
            self.burstSpeedX = burstSpeedX
            self.burstSpeedY = burstSpeedY
            self.lastUpdate = 0
            self.delta = 0.0

            for i in range(burstSize): self.add_burst(theDisplayable, 0)
            for i in range(numSquirts): self.add_squirt(squirtPower, squirtTime)

        def add_squirt(self, squirtPower, squirtTime):
            angle = random.random() * 6.283
            xSpeed = squirtPower * math.cos(angle)
            ySpeed = squirtPower * math.sin(angle)
            self.squirts.append([xSpeed, ySpeed, squirtTime])

        def add_burst(self, d, startTime):
            s = self.sm.create(d)
            xSpeed = (random.random() - 0.5) * self.burstSpeedX + 20
            ySpeed = (random.random() - 0.75) * self.burstSpeedY + 20
            pTime = self.particleTime
            self.drops.append([s, xSpeed, ySpeed, pTime, startTime])

        def add_drip(self, d, startTime):
            s = self.sm.create(d)
            xSpeed = (random.random() - 0.5) * self.dripSpeedX + 20
            ySpeed = random.random() * self.dripSpeedY + 20
            pTime = self.particleTime
            self.drops.append([s, xSpeed, ySpeed, pTime, startTime])

        def update(self, st):
            delta = st - self.lastUpdate
            self.delta += st - self.lastUpdate
            self.lastUpdate = st

            # Same pop-while-iterating fault as ParticleBurst, and far more
            # damaging here because this field is a FOUNTAIN, not a one-shot:
            # `density` drops are spawned every second for `dripTime` seconds
            # (120/s for 180s by default). Skipping every other expiry on each
            # pass meant the survivor list grew faster than it drained, so the
            # sprite count -- and the per-frame cost of walking it -- climbed
            # for as long as the effect was on screen. Both lists are now
            # rebuilt from their survivors.
            self.squirts = [q for q in self.squirts if st <= q[2]]

            if st < self.dripTime:
                while self.delta * self.density >= 1.0:
                    self.delta -= (1.0 / self.density)
                    if random.random() >= 1 - self.dripChance: self.add_drip(self.displayable, st)
                    for xSpeed, ySpeed, squirtTime in self.squirts:
                        s = self.sm.create(self.displayable)
                        s.x += (random.random() - 0.5) * 5
                        s.y += (random.random() - 0.5) * 5
                        self.drops.append([s, xSpeed + (random.random() - 0.5) * 20, ySpeed + (random.random() - 0.5) * 20, self.particleTime, st])

            alive = []
            for drop in self.drops:
                s, xSpeed, ySpeed, particleTime, startTime = drop
                if (st - startTime) < particleTime:
                    s.x += xSpeed * delta
                    s.y += ySpeed * delta
                    drop[2] += self.gravity * delta
                    alive.append(drop)
                else:
                    s.destroy()
            self.drops = alive

            # Spent AND past the spawning window: stop requesting frames.
            return 0 if (alive or st < self.dripTime) else None

init python:
    import math
    class AnimatedMask(renpy.Displayable):

        def __init__(self, child, mask, maskb, oc, op, moving=True, speed=1.0, frequency=1.0, amount=0.5, **properties):
            super(AnimatedMask, self).__init__(**properties)

            self.child = renpy.displayable(child)
            self.mask = renpy.displayable(mask)
            self.maskb = renpy.displayable(maskb)
            self.oc = oc
            self.op = op
            self.null = None
            self.size = None
            self.moving = moving
            self.speed = speed
            self.amount = amount
            self.frequency = frequency

        def render(self, width, height, st, at):

            cr = renpy.render(self.child, width, height, st, at)
            mr = renpy.render(self.mask, width, height, st, at)
            mb = renpy.Render(width, height)


            if self.moving:
                mb.place(self.mask, ((-st * 50) % (width * 2)) - (width * 2), 0)
                mb.place(self.maskb, -width / 2, 0)
            else:
                mb.place(self.mask, 0, 0)
                mb.place(self.maskb, 0, 0)



            cw, ch = cr.get_size()
            mw, mh = mr.get_size()

            w = min(cw, mw)
            h = min(ch, mh)
            size = (w, h)

            # The guard never armed: `self.size` was compared but never
            # assigned, so it stayed None and a fresh Null was allocated on
            # EVERY frame of a permanently-redrawing displayable. Recording the
            # size is the whole fix -- the Null is now built once per size
            # change, which for a full-screen mask means once.
            if self.size != size or self.null is None:
                self.null = Null(w, h)
                self.size = size

            nr = renpy.render(self.null, width, height, st, at)

            # `import sys` and a version test used to run here, per frame, to
            # decide whether renpy.Render still took `opaque`. imports.rpy
            # already imports sys at init, and this file only ever loads under
            # Matsu'Py 8 (Python 3), where the parameter is gone. Straight call.
            rv = renpy.Render(w, h)

            rv.operation = renpy.display.render.IMAGEDISSOLVE
            rv.operation_alpha = 1.0
            rv.operation_complete = self.oc + math.pow(math.sin(st * self.speed / 8), 64 * self.frequency) * self.amount
            rv.operation_parameter = self.op

            rv.blit(mb, (0, 0), focus=False, main=False)
            rv.blit(nr, (0, 0), focus=False, main=False)
            rv.blit(cr, (0, 0))

            renpy.redraw(self, 0)
            return rv

image blood_particle:
    subpixel True
    "gui/blood_drop.png"
    zoom 0.75
    alpha 0.75
    choice:
        linear 0.25 zoom 0
    choice:
        linear 0.35 zoom 0
    choice:
        linear 0.35 zoom 0
    choice:
        linear 0.55 zoom 0

image blood:
    size (1, 1)
    truecenter
    Blood("blood_particle").sm

image bsod_1:
    "images/bg/bsod.png"
    size (1280,720)
image bsod_2:
    "black"
    0.1
    yoffset 250
    0.1
    yoffset 500
    0.1
    yoffset 750

image bsod = LiveComposite((1280, 720), (0, 0), "bsod_1", (0, 0), "bsod_2")

image veins:
    AnimatedMask("images/bg/veinmask.png", "images/bg/veinmask.png", "images/bg/veinmaskb.png", 0.15, 16, moving=False, speed=10.0, frequency=0.25, amount=0.1)
    xanchor 0.05 zoom 1.10
    xpos -5
    subpixel True
    parallel:
        ease 2.0 xpos 5
        ease 1.0 xpos 0
        ease 1.0 xpos 5
        ease 2.0 xpos -5
        ease 1.0 xpos 0
        ease 1.0 xpos -5
        repeat
    parallel:
        choice:
            0.6
        choice:
            0.2
        choice:
            0.3
        choice:
            0.4
        choice:
            0.5
        pass
        choice:
            xoffset 0
        choice:
            xoffset 1
        choice:
            xoffset 2
        choice:
            xoffset -1
        choice:
            xoffset -2
        repeat


