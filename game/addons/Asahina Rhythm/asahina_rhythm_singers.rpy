# The original complete drawings own each singer's silhouette and acting.
# Presentation supplies frame timing; no articulated replacement artwork.

init -2 python:
    from asahina_rhythm_motion import (SingerFrames as ARSingerFramesClock,
                                      STANCE_OFFSETS as AR_SINGER_STANCE)

    class ARSingerFrames(renpy.Displayable):
        """The complete original 32-frame bank, predicted once per singer."""

        def __init__(self, name, **kwargs):
            super(ARSingerFrames, self).__init__(**kwargs)
            self.name = name
            self.motion = ARSingerFramesClock(name)
            self.images = {}
            root = "addons/Asahina Rhythm/art/"
            for pose, count in self.motion.COUNTS.items():
                for frame in range(count):
                    # Miss tint is pre-baked to avoid a shader compile mid-song.
                    path = (root + "ui/%s_miss_%d.png" % (name, frame) if pose == "miss"
                            else root + "%s/%s_%d.png" % (name, pose, frame))
                    self.images[(pose, frame)] = Image(path)
            self.now, self.beat = 0.0, 0.0

        def visit(self):
            return list(self.images.values())

        def set_pose(self, pose, now, event=None, held=False, duration=None):
            self.motion.set_pose(pose, now, event, held, duration)
            self.now = float(now)
            renpy.redraw(self, 0)

        def set_clock(self, now, beat, beat_len=None):
            self.now, self.beat = float(now), float(beat)
            if beat_len is not None:
                self.motion.beat_len = max(.05, float(beat_len))
            renpy.redraw(self, 0)

        def render(self, width, height, st, at):
            frame, sy = self.motion.sample(self.now, self.beat)
            child = self.images[(self.motion.pose, frame)]
            source = renpy.render(child, 384, 448, st, at)
            result = renpy.Render(384, 448)
            # Continuous beat compression keeps the authored floor at y=430.
            # Stance landmarks are fixed data, without alpha-weighted shoe means.
            breath = renpy.Render(384, 448)
            breath.zoom(1.0, sy)
            breath.blit(source, (0, 0))
            dx = AR_SINGER_STANCE[self.name][self.motion.pose][frame]
            result.subpixel_blit(breath, (dx, 430.0 * (1.0 - sy)))
            return result

    class ARSingerMenuPose(renpy.Displayable):
        """Results use the same full drawings and slower two-frame holds."""

        def __init__(self, name, pose, period, **kwargs):
            super(ARSingerMenuPose, self).__init__(**kwargs)
            self.singer = ARSingerFrames(name)
            self.pose = pose
            self.period = max(1.2, float(period))

        def visit(self):
            return [self.singer]

        def render(self, width, height, st, at):
            self.singer.set_pose(self.pose, st)
            self.singer.motion.loop_period = self.period
            self.singer.set_clock(st, st * 2.0 / self.period, self.period / 2.0)
            result = renpy.render(self.singer, width, height, st, at)
            renpy.redraw(self, 0)
            return result

    def ar_frame_menu_pose(name, pose, period):
        return ARSingerMenuPose(name, pose, period)
