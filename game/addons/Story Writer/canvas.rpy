# A broken asset must not take the writing session or its unsaved prose down.
init 5 python:
    def sw_composition_show(child, transforms=()):
        """Give a newly built miniature stage image its real initial ATL event.

        At constructs private transform instances with this new child. Sending
        the event to these instances leaves the named transform definitions
        untouched, matching the initialization performed by SceneLists.add.
        """
        if transforms:
            child = At(child, *transforms)
        child._unique()
        child.set_transform_event("show")
        return child

    class SWPreviewSurface(renpy.Displayable):
        def __init__(self, child, width, height, **properties):
            super(SWPreviewSurface, self).__init__(**properties)
            self.child = child
            self.width, self.height = int(width), int(height)
            self.last_error = ""

        def render(self, width, height, st, at):
            result = renpy.Render(self.width, self.height)
            try:
                rendered = renpy.render(self.child, self.width, self.height, st, at)
                result.place(self.child, width=self.width, height=self.height, render=rendered)
                self.last_error = ""
            except renpy.game.CONTROL_EXCEPTIONS:
                raise
            except Exception as exc:
                self.last_error = str(exc)
                explanation = Text(sw_caption("Preview unavailable\n" + sw_short(self.last_error, 210)),
                    size=16, color="#e8be88", font="DejaVuSans.ttf")
                rendered = renpy.render(explanation, self.width - 32, self.height - 32, st, at)
                result.blit(rendered, (16, 16))
            return result.subsurface((0, 0, self.width, self.height))

        def visit(self):
            return [self.child]
