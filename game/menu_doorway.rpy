# The illustrated doorway links title-menu destinations. The earlier CRT
# transitions remain available to isolated gameplay and for measured comparison.
# This move renders only the visible scene, never two live menu trees together.

init -4 python:
    class EnterMDoorwayTransition(EnterMFocusGate, renpy.display.transition.Transition):
        def __init__(self, delay=0.72, old_widget=None, new_widget=None, **properties):
            super(EnterMDoorwayTransition, self).__init__(delay, **properties)
            self.old_widget = old_widget
            self.new_widget = new_widget
            self.events = False
            self._incoming_prepared = False
            self._left = Transform("assets/gui/first_boot/opening_seal.svg", crop=(0, 0, 640, 720))
            self._right = Transform("assets/gui/first_boot/opening_seal.svg", crop=(640, 0, 640, 720))

        def visit(self):
            return [d for d in (self.old_widget, self.new_widget, self._left, self._right) if d is not None]

        def render(self, width, height, st, at):
            if self.new_widget is None:
                return renpy.display.render.Render(width, height)
            if st >= self.delay or renpy.game.less_updates:
                self.events = True
                self.gate_land()
                return renpy.display.render.render(self.new_widget, width, height, st, at)

            # Music already hands over at 0.34 seconds. Keep its decoder start
            # behind the closed artwork, then reveal picture and sound together.
            close = 0.24
            reveal = ENTER_M_MENU_REVEAL
            rv = renpy.display.render.Render(width, height)
            if st < close:
                coverage = 1.0 - (1.0 - max(st, 0.0) / close) ** 3
                if self.old_widget is not None:
                    rv.blit(renpy.display.render.render(self.old_widget, width, height, st, at), (0, 0), focus=False)
            elif st < reveal:
                coverage = 1.0
                # Prepare text and first-use textures once while fully covered.
                # No invisible menu is repeatedly redrawn throughout the hold.
                if not self._incoming_prepared:
                    renpy.display.render.render(self.new_widget, width, height, st, at)
                    self._incoming_prepared = True
            else:
                coverage = max(0.0, 1.0 - (st - reveal) / (self.delay - reveal)) ** 3
                rv.blit(renpy.display.render.render(self.new_widget, width, height, st, at), (0, 0), focus=False)

            # Native virtual dimensions are 1280x720. Both halves use the same
            # cached SVG raster; there is no shader compilation, texture readback,
            # screenshot capture, or Python image construction in this move.
            distance = int(round(640 * (1.0 - coverage)))
            rv.blit(renpy.display.render.render(self._left, 640, 720, st, at), (-distance, 0), focus=False)
            rv.blit(renpy.display.render.render(self._right, 640, 720, st, at), (640 + distance, 0), focus=False)
            self.gate_moved = True
            renpy.display.render.redraw(self, 0)
            return rv

    class EnterMTitleDoorwayEnter(renpy.object.Object):
        def __init__(self):
            self.gameplay = EnterMMenuEnter()

        def __call__(self, old_widget=None, new_widget=None):
            move = enter_m_menu_doorway if getattr(store, "main_menu", False) else self.gameplay
            return move(old_widget=old_widget, new_widget=new_widget)

define -3 enter_m_menu_doorway = renpy.curry(EnterMDoorwayTransition)(0.72)

init 10 python:
    config.enter_transition = EnterMTitleDoorwayEnter()
    config.intra_transition = enter_m_menu_doorway
    config.game_main_transition = enter_m_menu_doorway
    config.end_game_transition = enter_m_menu_doorway
    # Chapter Select is a called screen in the New Game flow, not ShowMenu.
    # Its story-start dissolve stays separate from this menu-to-menu move.
    cs_move_open = enter_m_menu_doorway
