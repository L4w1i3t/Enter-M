# Developer Story Writer: a paragraph editor with native-font measured hit testing.
# The pure buffer deliberately knows nothing about Ren'Py statements or game state.
init -20 python:
    import time as _sw_text_time
    import renpy.pygame as _sw_text_pygame
    from collections import OrderedDict as _SWTextOrderedDict
    from story_writer_text import TextBuffer as _SWTextBuffer
    from story_writer_text import wrap_text as _sw_wrap_text
    from story_writer_text import line_for_position as _sw_line_for_position
    from story_writer_text import nearest_boundary as _sw_nearest_boundary
    from story_writer_text import normalize_text as _sw_normalize_text

    class SWTextEditor(renpy.Displayable):
        """Cached screen `add` component. Enter submits; Shift+Enter adds a newline."""
        _active_editor = None

        def __init__(self, text="", changed=None, submit=None, width=560, height=190,
                     font_size=24, multiline=True, placeholder="", **properties):
            super(SWTextEditor, self).__init__(**properties)
            self.buffer = _SWTextBuffer(text)
            self.changed = changed
            self.submit = submit
            self.width = int(width)
            self.height = int(height)
            self.font_size = int(font_size)
            self.multiline = bool(multiline)
            self.placeholder = placeholder
            self.focused = False
            self.dragging = False
            self.scroll = 0.0
            # A 40px metadata field needs room for the native 18px font's full
            # line box; prose keeps the more spacious paragraph inset.
            self._padding = 12 if self.multiline else 6
            self._layout_key = None
            self._lines = []
            self._measure_cache = _SWTextOrderedDict()
            self._display_cache = _SWTextOrderedDict()
            self._render_width = self.width
            self._render_height = self.height
            self._line_height = int(self.font_size * 1.45)
            self._preferred_x = None
            self._line_affinity = False
            self._reveal = True
            self._blink_reset = _sw_text_time.monotonic()
            self._composition = ""
            self._composition_start = 0
            self._composition_length = 0
            self._last_click_time = 0.0
            self._last_click_pos = None

        @property
        def text(self):
            return self.buffer.text

        @property
        def caret_position(self):
            return self.buffer.caret

        @property
        def selection(self):
            return self.buffer.selection

        def set_text(self, text, notify=False):
            text = _sw_normalize_text(text)
            self.buffer.set_text(text)
            self._composition = ""
            self.scroll = 0.0
            self._line_affinity = False
            self._touch(notify)

        def set_font_size(self, size):
            size = max(14, min(48, int(size)))
            if size != self.font_size:
                self.font_size = size
                self._measure_cache.clear()
                self._display_cache.clear()
                self._layout_key = None
                self._touch(False)

        def set_focus(self, focused):
            focused = bool(focused)
            if focused:
                active = SWTextEditor._active_editor
                if active is not None and active is not self:
                    active.set_focus(False)
                SWTextEditor._active_editor = self
            elif SWTextEditor._active_editor is self:
                SWTextEditor._active_editor = None
            self.focused = focused
            if not focused:
                self.dragging = False
                self._composition = ""
                self.buffer.break_group()
            self._touch(False)

        def _touch(self, notify=False, preserve_x=False):
            self._blink_reset = _sw_text_time.monotonic()
            self._reveal = True
            if not preserve_x:
                self._preferred_x = None
            renpy.redraw(self, 0)
            if notify and self.changed is not None:
                self.changed(self.text)

        def undo(self):
            if self.buffer.undo():
                self._touch(True)

        def redo(self):
            if self.buffer.redo():
                self._touch(True)

        def _text_displayable(self, text, color="#eaded0"):
            key = (text, color, self.font_size)
            cached = self._display_cache.get(key)
            if cached is not None:
                self._display_cache.move_to_end(key)
                return cached
            # Braces are literal source; interpolation is always disabled here.
            displayable = renpy.text.text.Text(
                text.replace("{", "{{").replace("\t", "    "),
                substitute=False, slow=False, font="DejaVuSans.ttf",
                size=self.font_size, color=color, outlines=[],
                layout="nobreak", line_spacing=0, xminimum=0,
                text_align=0.0, first_indent=0, rest_indent=0)
            self._display_cache[key] = displayable
            if len(self._display_cache) > 512:
                self._display_cache.popitem(last=False)
            return displayable

        def _measure(self, text):
            if not text:
                return 0.0
            cached = self._measure_cache.get(text)
            if cached is not None:
                self._measure_cache.move_to_end(text)
                return cached
            # Layout-only sizing reports the same advance as a full render
            # (measured identical on DejaVu Sans) at about a quarter of the cost.
            value = float(self._text_displayable(text).size(32768, 2048)[0])
            self._measure_cache[text] = value
            if len(self._measure_cache) > 4096:
                self._measure_cache.popitem(last=False)
            return value

        def _layout(self):
            available = max(1, self._render_width - self._padding * 2 - 5)
            key = (self.text, available, self.font_size)
            if key != self._layout_key:
                self._lines = _sw_wrap_text(self.text, available, self._measure)
                self._layout_key = key
                sample_height = self._text_displayable("Ag").size(32768, 2048)[1]
                self._line_height = max(int(self.font_size * 1.4), sample_height + 5)

        def _x_at(self, index, offset):
            # Only the offsets a caret, selection or click needs are measured;
            # every prefix of a long line used to be rendered on first touch.
            text = self._lines[index].text
            return self._measure(text[:max(0, min(len(text), offset))])

        def _caret_line(self):
            return _sw_line_for_position(self._lines, self.buffer.caret, self._line_affinity)

        def _max_scroll(self):
            return max(0, len(self._lines) * self._line_height - (self._render_height - 2 * self._padding))

        def _reveal_caret(self):
            index = self._caret_line()
            y = index * self._line_height
            available = self._render_height - self._padding * 2
            if y < self.scroll:
                self.scroll = y
            elif y + self._line_height > self.scroll + available:
                self.scroll = y + self._line_height - available
            self.scroll = max(0, min(self._max_scroll(), self.scroll))
            self._reveal = False

        def _hit(self, x, y):
            self._layout()
            index = int((y - self._padding + self.scroll) // self._line_height)
            index = max(0, min(len(self._lines) - 1, index))
            line = self._lines[index]
            offset = _sw_nearest_boundary(lambda value: self._x_at(index, value), len(line.text), x - self._padding)
            self._line_affinity = offset == len(line.text)
            return line.start + offset

        def _move_vertical(self, direction, extend):
            self._layout()
            index = self._caret_line()
            line = self._lines[index]
            if self._preferred_x is None:
                self._preferred_x = self._x_at(index, self.buffer.caret - line.start)
            destination = max(0, min(len(self._lines) - 1, index + direction))
            next_line = self._lines[destination]
            offset = _sw_nearest_boundary(lambda value: self._x_at(destination, value), len(next_line.text), self._preferred_x)
            self._line_affinity = offset == len(next_line.text)
            self.buffer.move(next_line.start + offset, extend)
            self._touch(False, preserve_x=True)

        def _copy(self):
            start, end = self.buffer.selection
            if start != end:
                _sw_text_pygame.scrap.put(_sw_text_pygame.scrap.SCRAP_TEXT, self.text[start:end].encode("utf-8"))

        def _paste(self):
            value = _sw_text_pygame.scrap.get(_sw_text_pygame.scrap.SCRAP_TEXT)
            if value is None:
                return
            if isinstance(value, bytes):
                value = value.decode("utf-8", "replace")
            value = _sw_normalize_text(value)
            if not self.multiline:
                value = value.replace("\n", " ")
            if self.buffer.replace(value, "paste"):
                self._touch(True)

        def render(self, width, height, st, at):
            self._render_width = max(30, min(self.width, int(width)))
            self._render_height = max(30, min(self.height, int(height)))
            self._layout()
            if self._reveal:
                self._reveal_caret()
            result = renpy.Render(self._render_width, self._render_height)
            canvas = result.canvas()
            canvas.rect("#211f20", (0, 0, self._render_width, self._render_height))
            canvas.rect("#b99b78" if self.focused else "#514643", (0, 0, self._render_width, self._render_height), 1)
            inner_width = self._render_width - self._padding * 2
            inner_height = self._render_height - self._padding * 2
            inner = renpy.Render(inner_width, inner_height)
            inner_canvas = inner.canvas()
            start, end = self.buffer.selection
            first = max(0, int(self.scroll // self._line_height))
            last = min(len(self._lines), first + int(inner_height // self._line_height) + 2)
            for index in range(first, last):
                line = self._lines[index]
                y = index * self._line_height - self.scroll
                selected_start = max(start, line.start)
                selected_end = min(end, line.end)
                newline_selected = line.hard_break and start <= line.end < end
                if selected_start < selected_end or newline_selected:
                    x1 = self._x_at(index, selected_start - line.start)
                    x2 = self._x_at(index, selected_end - line.start)
                    if newline_selected:
                        x2 += max(8, self.font_size * 0.35)
                    inner_canvas.rect("#625046" if self.focused else "#443b36", (int(x1), int(y), max(2, int(x2 - x1)), self._line_height))
                if line.text:
                    child = renpy.render(self._text_displayable(line.text), 32768, self._line_height, st, at)
                    inner.blit(child, (0, int(y)))
            if not self.text and not self._composition and self.placeholder:
                child = renpy.render(self._text_displayable(self.placeholder, "#877971"), 32768, inner_height, st, at)
                inner.blit(child, (0, 0))
            if self.focused:
                caret_line = self._caret_line()
                line = self._lines[caret_line]
                caret_x = self._x_at(caret_line, self.buffer.caret - line.start)
                caret_y = caret_line * self._line_height - self.scroll
                elapsed = _sw_text_time.monotonic() - self._blink_reset
                if int(elapsed / 0.55) % 2 == 0:
                    inner_canvas.rect("#f4d7ae", (int(caret_x), int(caret_y), 2, self._line_height - 3))
                if self._composition:
                    child = renpy.render(self._text_displayable(self._composition, "#f4d7ae"), 32768, self._line_height, st, at)
                    inner_canvas.rect("#39302a", (int(caret_x), int(caret_y), child.get_size()[0] + 4, self._line_height))
                    inner.blit(child, (int(caret_x), int(caret_y)))
                    inner_canvas.line("#f4d7ae", (int(caret_x), int(caret_y + self._line_height - 2)), (int(caret_x + child.get_size()[0]), int(caret_y + self._line_height - 2)), 1)
                renpy.redraw(self, max(0.02, 0.55 - elapsed % 0.55))
                # Same engine contract as stock Input: starts SDL text input / IME.
                result.text_input = True
            inner = inner.subsurface((0, 0, inner_width, inner_height))
            result.blit(inner, (self._padding, self._padding))
            if self._max_scroll() > 0:
                thumb_height = max(16, inner_height * inner_height / float(len(self._lines) * self._line_height))
                thumb_y = self._padding + (inner_height - thumb_height) * self.scroll / self._max_scroll()
                canvas.rect("#8c7461", (self._render_width - 6, int(thumb_y), 3, int(thumb_height)))
            return result

        def event(self, ev, x, y, st):
            pg = _sw_text_pygame
            inside = 0 <= x < self._render_width and 0 <= y < self._render_height
            if ev.type == pg.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    if not inside:
                        if self.focused:
                            self.set_focus(False)
                        return None
                    self.set_focus(True)
                    position = self._hit(x, y)
                    shift = bool(pg.key.get_mods() & pg.KMOD_SHIFT)
                    now = _sw_text_time.monotonic()
                    if self._last_click_pos == position and now - self._last_click_time < 0.4:
                        self.buffer.move(position)
                        start = self.buffer.word(-1)
                        end = self.buffer.word(1)
                        self.buffer.move(start)
                        self.buffer.move(end, True)
                    else:
                        self.buffer.move(position, shift)
                    self._last_click_time = now
                    self._last_click_pos = position
                    self.dragging = True
                    self._touch(False)
                    raise renpy.IgnoreEvent()
                if inside and ev.button in (4, 5):
                    self.scroll = max(0, min(self._max_scroll(), self.scroll + (-1 if ev.button == 4 else 1) * self._line_height * 3))
                    self._reveal = False
                    renpy.redraw(self, 0)
                    raise renpy.IgnoreEvent()
            if ev.type == pg.MOUSEBUTTONUP and ev.button == 1 and self.dragging:
                self.dragging = False
                raise renpy.IgnoreEvent()
            if ev.type == pg.MOUSEMOTION and self.dragging:
                if y < self._padding:
                    self.scroll = max(0, self.scroll - self._line_height)
                elif y > self._render_height - self._padding:
                    self.scroll = min(self._max_scroll(), self.scroll + self._line_height)
                self.buffer.move(self._hit(x, y), True)
                self._touch(False)
                raise renpy.IgnoreEvent()
            if ev.type == getattr(pg, "MOUSEWHEEL", -10) and inside:
                self.scroll = max(0, min(self._max_scroll(), self.scroll - ev.y * self._line_height * 3))
                self._reveal = False
                renpy.redraw(self, 0)
                raise renpy.IgnoreEvent()
            if not self.focused:
                return None
            if ev.type == pg.TEXTEDITING:
                self._composition = ev.text
                self._composition_start = getattr(ev, "start", 0)
                self._composition_length = getattr(ev, "length", 0)
                self._touch(False)
                raise renpy.IgnoreEvent()
            if ev.type == pg.TEXTINPUT:
                self._composition = ""
                if self.buffer.replace(ev.text, "type"):
                    self._touch(True)
                raise renpy.IgnoreEvent()
            if ev.type == pg.KEYUP:
                raise renpy.IgnoreEvent()
            if ev.type != pg.KEYDOWN:
                return None
            mod = getattr(ev, "mod", pg.key.get_mods())
            control = bool(mod & (pg.KMOD_CTRL | pg.KMOD_META)) and not bool(mod & pg.KMOD_ALT)
            shift = bool(mod & pg.KMOD_SHIFT)
            key = ev.key
            alt = bool(mod & pg.KMOD_ALT) and not bool(mod & (pg.KMOD_CTRL | pg.KMOD_META))
            if (key == pg.K_F5 or (control and key in (pg.K_s, pg.K_RETURN, pg.K_KP_ENTER, pg.K_UP, pg.K_DOWN))
                    or (alt and key in (pg.K_UP, pg.K_DOWN))):
                # Writer actions owned by the containing screen: save, read,
                # next textbox, and moving between or reordering beats.
                self.buffer.break_group()
                return None
            if key == pg.K_ESCAPE:
                if self._composition:
                    self._composition = ""
                    self._touch(False)
                else:
                    self.set_focus(False)
                raise renpy.IgnoreEvent()
            if self._composition:
                # SDL/IME owns its pre-edit navigation and confirmation.
                raise renpy.IgnoreEvent()
            if control and key == pg.K_a:
                self.buffer.move(0)
                self.buffer.move(len(self.text), True)
                self._touch(False)
            elif control and key in (pg.K_c, pg.K_x):
                self._copy()
                if key == pg.K_x and self.buffer.selection[0] != self.buffer.selection[1]:
                    self.buffer.replace("", "cut")
                    self._touch(True)
            elif control and key == pg.K_v:
                self._paste()
            elif control and key == pg.K_z:
                self.redo() if shift else self.undo()
            elif control and key == pg.K_y:
                self.redo()
            elif key in (pg.K_RETURN, pg.K_KP_ENTER):
                if shift and self.multiline:
                    if self.buffer.replace("\n", "newline"):
                        self._touch(True)
                elif self.submit is not None:
                    self.buffer.break_group()
                    self.submit()
            elif key in (pg.K_BACKSPACE, pg.K_DELETE):
                if self.buffer.erase(key == pg.K_BACKSPACE, control):
                    self._touch(True)
            elif key in (pg.K_LEFT, pg.K_RIGHT):
                backwards = key == pg.K_LEFT
                start, end = self.buffer.selection
                if not shift and start != end:
                    position = start if backwards else end
                else:
                    position = self.buffer.word(-1 if backwards else 1) if control else self.buffer.caret + (-1 if backwards else 1)
                self._line_affinity = backwards
                self.buffer.move(position, shift)
                self._touch(False)
            elif key in (pg.K_UP, pg.K_DOWN, pg.K_PAGEUP, pg.K_PAGEDOWN):
                direction = -1 if key in (pg.K_UP, pg.K_PAGEUP) else 1
                if key in (pg.K_PAGEUP, pg.K_PAGEDOWN):
                    direction *= max(1, int((self._render_height - self._padding * 2) // self._line_height) - 1)
                self._move_vertical(direction, shift)
            elif key in (pg.K_HOME, pg.K_END):
                self._layout()
                line = self._lines[self._caret_line()]
                end = key == pg.K_END
                position = (len(self.text) if end else 0) if control else (line.end if end else line.start)
                self._line_affinity = end
                self.buffer.move(position, shift)
                self._touch(False)
            # Text is committed by SDL TEXTINPUT, never a duplicate KEYDOWN.unicode.
            # Consume every focused key so game skip/rollback/hide shortcuts cannot leak.
            raise renpy.IgnoreEvent()

        def per_interact(self):
            renpy.redraw(self, 0)

        def visit(self):
            return []
