# One fixed Matsuda head with two masked, continuously positioned irises.
# The stage supplies song time; pausing or restarting therefore also pauses or
# restarts the gaze. All parts are in the existing 256x224 head coordinates.

init -2 python:
    def ar_matsuda_gaze_offset(seconds):
        """Look toward Asahina, the player, then the camera, with eased saccades."""
        t = max(0.0, float(seconds)) % 13.4

        def between(start, end, a, b):
            u = (t - start) / (end - start)
            # Quintic interpolation has zero velocity and acceleration at both
            # ends, including the final move back into the next cycle.
            u = u * u * u * (u * (u * 6.0 - 15.0) + 10.0)
            return a + (b - a) * u

        if t < 3.5:
            return -5.2
        if t < 3.92:
            return between(3.5, 3.92, -5.2, 5.2)
        if t < 8.0:
            return 5.2
        if t < 8.32:
            return between(8.0, 8.32, 5.2, 0.0)
        if t < 13.0:
            return 0.0
        return between(13.0, 13.4, 0.0, -5.2)


    class _ARMatsudaEyeLayer(renpy.Displayable):
        """The only moving artwork; its parent clips it to the authored sclera."""
        def __init__(self, **properties):
            super(_ARMatsudaEyeLayer, self).__init__(**properties)
            self.now = 0.0
            self.iris = Image("addons/Asahina Rhythm/art/matsuda/rig/gaze_iris.png")

        def render(self, width, height, st, at):
            rv = renpy.Render(256, 224)
            iris = renpy.render(self.iris, width, height, st, at)
            iw, ih = iris.get_size()
            gaze = ar_matsuda_gaze_offset(self.now)
            # The vertical offset follows the tilted eye line. Both irises
            # travel together in head space and retain one consistent shape.
            for cx, cy in ((105.5, 117.8), (151.5, 103.5)):
                rv.subpixel_blit(iris, (cx + gaze - iw * .5,
                                       cy - .29 * gaze - ih * .5))
            renpy.redraw(self, 0)
            return rv

        def visit(self):
            return [self.iris]


    class ARMatsudaGaze(renpy.Displayable):
        """Drop-in 256x224 head; the existing head Composite owns the earring."""
        def __init__(self, **properties):
            super(ARMatsudaGaze, self).__init__(**properties)
            root = "addons/Asahina Rhythm/art/matsuda/rig/"
            self.pupils = _ARMatsudaEyeLayer()
            self.head = Composite(
                (256, 224),
                (0, 0), Image(root + "gaze_head.png"),
                (0, 0), AlphaMask(self.pupils, Image(root + "gaze_sclera_mask.png")),
            )

        @property
        def now(self):
            return self.pupils.now

        @now.setter
        def now(self, value):
            self.pupils.now = float(value)

        def render(self, width, height, st, at):
            rv = renpy.render(self.head, width, height, st, at)
            renpy.redraw(self, 0)
            return rv

        def visit(self):
            return [self.head]
