"""Editor text operations independent of Ren'Py rendering or story execution."""

import time
from collections import namedtuple


VisualLine = namedtuple("VisualLine", "start end text hard_break")


def normalize_text(value):
    return str(value).replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")


class TextBuffer:
    """Selection and bounded, grouped undo; offsets index the original Unicode text."""

    def __init__(self, text=""):
        self.text = normalize_text(text)
        self.anchor = self.caret = len(self.text)
        self.undo_stack = []
        self.redo_stack = []
        self._group = None
        self._time = 0.0
        self._after = None

    @property
    def selection(self):
        return min(self.anchor, self.caret), max(self.anchor, self.caret)

    def snapshot(self):
        return self.text, self.anchor, self.caret

    def break_group(self):
        self._group = self._after = None

    def set_text(self, text):
        self.text = normalize_text(text)
        self.anchor = self.caret = len(self.text)
        self.undo_stack[:] = []
        self.redo_stack[:] = []
        self.break_group()

    def move(self, position, extend=False):
        self.caret = max(0, min(len(self.text), int(position)))
        if not extend:
            self.anchor = self.caret
        self.break_group()

    def replace(self, value, kind="edit", now=None):
        value = normalize_text(value)
        start, end = self.selection
        replacement = self.text[:start] + value + self.text[end:]
        if replacement == self.text:
            return False
        now = time.monotonic() if now is None else now
        before = self.snapshot()
        grouped = (kind in ("type", "backspace", "delete")
                   and self._group == kind and self._after == before
                   and 0 <= now - self._time < 0.8)
        if not grouped:
            self.undo_stack.append(before)
            del self.undo_stack[:-256]
        self.text = replacement
        self.anchor = self.caret = start + len(value)
        self.redo_stack[:] = []
        self._group = kind
        self._time = now
        self._after = self.snapshot()
        return True

    def erase(self, backwards=True, word=False, now=None):
        start, end = self.selection
        if start != end:
            return self.replace("", now=now)
        position = self.word(-1 if backwards else 1) if word else self.caret + (-1 if backwards else 1)
        position = max(0, min(len(self.text), position))
        if position == self.caret:
            return False
        # Preserve the pre-delete cursor snapshot when grouping repeated deletion.
        before = self.snapshot()
        self.anchor = position
        group_after = self._after
        if group_after == before:
            self._after = self.snapshot()
        result = self.replace("", "backspace" if backwards else "delete", now=now)
        if result and self.undo_stack and self.undo_stack[-1] == (before[0], position, before[2]):
            self.undo_stack[-1] = before
        return result

    def word(self, direction):
        position = self.caret
        value = self.text
        if direction < 0:
            while position and value[position - 1].isspace():
                position -= 1
            if position:
                word = value[position - 1].isalnum() or value[position - 1] == "_"
                while position and not value[position - 1].isspace() and ((value[position - 1].isalnum() or value[position - 1] == "_") == word):
                    position -= 1
        else:
            if position < len(value) and not value[position].isspace():
                word = value[position].isalnum() or value[position] == "_"
                while position < len(value) and not value[position].isspace() and ((value[position].isalnum() or value[position] == "_") == word):
                    position += 1
            while position < len(value) and value[position].isspace():
                position += 1
        return position

    def undo(self):
        if not self.undo_stack:
            return False
        self.redo_stack.append(self.snapshot())
        self.text, self.anchor, self.caret = self.undo_stack.pop()
        self.break_group()
        return True

    def redo(self):
        if not self.redo_stack:
            return False
        self.undo_stack.append(self.snapshot())
        self.text, self.anchor, self.caret = self.redo_stack.pop()
        self.break_group()
        return True


def wrap_text(text, width, measure):
    """Greedy wrapping retaining every source character and explicit newline."""
    width = max(1, width)
    lines = []
    start = 0
    paragraphs = text.split("\n")
    for paragraph_index, paragraph in enumerate(paragraphs):
        hard = paragraph_index < len(paragraphs) - 1
        if not paragraph:
            lines.append(VisualLine(start, start, "", hard))
        offset = 0
        while offset < len(paragraph):
            remaining_length = len(paragraph) - offset
            high = 1
            # Probe only the current visual row; a long pasted paragraph should
            # never render its entire remaining suffix once per wrapped row.
            while high < remaining_length and measure(paragraph[offset:offset + high]) <= width:
                high = min(remaining_length, high * 2)
            if measure(paragraph[offset:offset + high]) <= width:
                take = high
            else:
                # Binary search actual measured prefixes; no fixed glyph-width assumption.
                low = 1
                while low < high:
                    middle = (low + high + 1) // 2
                    if measure(paragraph[offset:offset + middle]) <= width:
                        low = middle
                    else:
                        high = middle - 1
                take = low
                # Prefer a whitespace boundary, retaining it on the previous row.
                boundary = max(paragraph.rfind(" ", offset, offset + take), paragraph.rfind("\t", offset, offset + take))
                if boundary >= offset:
                    take = boundary - offset + 1
            end = offset + max(1, take)
            lines.append(VisualLine(start + offset, start + end, paragraph[offset:end], hard and end == len(paragraph)))
            offset = end
        start += len(paragraph) + 1
    return lines


def line_for_position(lines, position, prefer_previous=False):
    for index, line in enumerate(lines):
        if position < line.end or (position == line.end and (line.hard_break or prefer_previous or index == len(lines) - 1)):
            return index
    return len(lines) - 1


def hit_offset(widths, x):
    """Nearest measured insertion boundary, also valid for zero-width glyphs."""
    return min(range(len(widths)), key=lambda index: abs(widths[index] - x))


def nearest_boundary(width_at, length, x):
    """Nearest insertion offset for monotonic prefix widths in O(log n) probes.

    ``width_at(offset)`` measures ``text[:offset]``. Equal widths (zero-width
    marks) resolve to the later offset, so a caret stays after its mark.
    """
    if length <= 0 or x <= 0:
        return 0
    if x >= width_at(length):
        return length
    low, high = 0, length
    while high - low > 1:
        middle = (low + high) // 2
        if width_at(middle) <= x:
            low = middle
        else:
            high = middle
    return low if x - width_at(low) <= width_at(high) - x else high
