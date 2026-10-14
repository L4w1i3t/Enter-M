# Screenshot inversion, tearing, and particle bursts shared by active scenes.
# Ren'Py callbacks use st (shown seconds) and at (animation seconds).

init python:
    import weakref as _fx_weakref

    # Surfaces stay outside save/rollback state and expire with their owner.
    if not hasattr(renpy, '_effect_srf_cache'):
        renpy._effect_srf_cache = _fx_weakref.WeakKeyDictionary()

    # Subsurface views must also stay outside pickled displayables.
    if not hasattr(renpy, '_effect_slice_cache'):
        renpy._effect_slice_cache = _fx_weakref.WeakKeyDictionary()

    def screenshot_srf():
        return renpy.display.draw.screenshot(None)

    def invert():
        screenshot = screenshot_srf()
        inverted = renpy.Render(screenshot.get_width(), screenshot.get_height()).canvas().get_surface()
        inverted.fill((255, 255, 255, 255))
        inverted.blit(screenshot, (0, 0), None, 2)
        return inverted

    class Invert(renpy.Displayable):
        def __init__(self, delay=0.0, screenshot_delay=0.0):
            # screenshot_delay is a retained legacy keyword; capture is immediate.
            super(Invert, self).__init__()
            width, height = renpy.get_physical_size()
            # Render dimensions must be integers under Python 3.
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
        """A horizontal slice with alternating off/on times and pixel offsets."""
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
        """Offset screenshot slices; timing multipliers scale each slice's cycle.

        srf optionally supplies the captured surface; offsetMin/Max are pixels.
        """
        def __init__(self, number, offtimeMult, ontimeMult, offsetMin, offsetMax, srf=None):
            super(Tear, self).__init__()
            width, height = renpy.get_physical_size()
            # Crop the captured surface to a 16:9 integer render area.
            if float(width) / float(height) > 16.0 / 9.0:
                self.width = int(height) * 16 // 9
                self.height = int(height)
            else:
                self.width = int(width)
                self.height = int(width) * 9 // 16
            self.number = number
            renpy._effect_srf_cache[self] = srf if srf else screenshot_srf()
            # Slice geometry is fixed; cache views once and move only offsets.
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
        """Emit numParticles sprites for particleTime seconds with gravity.

        particleXSpeed/particleYSpeed scale randomized initial velocities.
        Constructor names remain compatible with the OP and boss-fight callers.
        """
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
                self.add(self.displayable)

        def add(self, displayable):
            sprite = self.sm.create(displayable)
            speed = random.random()
            angle = random.random() * 3.14159 * 2
            horizontal_speed = speed * math.cos(angle) * self.particleXSpeed
            vertical_speed = speed * math.sin(angle) * self.particleYSpeed - 1
            sprite.x = horizontal_speed * 24
            sprite.y = vertical_speed * 24
            self.stars.append((sprite, vertical_speed, horizontal_speed, self.particleTime))

        def update(self, st):
            # Rebuild survivors so removing an expired sprite cannot skip one.
            alive = []
            for sprite, vertical_speed, horizontal_speed, lifetime in self.stars:
                if st < lifetime:
                    sprite.x = horizontal_speed * 120 * (st + .20)
                    sprite.y = vertical_speed * 120 * (st + .20) + self.gravity * st * st
                    alive.append((sprite, vertical_speed, horizontal_speed, lifetime))
                else:
                    sprite.destroy()
            self.stars = alive
            # Nothing left to move: stop asking SpriteManager for frames.
            return 0 if alive else None
