# Auto Dialogue Font Size
#
# Keeps ADV dialogue at gui.say_text_size unless Ren'Py's own text layout says it
# would exceed the configured line budget.

define gui.say_text_fit_max_lines = 3
define gui.say_text_fit_min_size = 18
define gui.say_text_fit_height_fudge = 2
define gui.say_text_fit_cache_limit = 256

init -1 python:
    from collections import OrderedDict

    _enter_m_say_text_fit_cache = OrderedDict()
    _enter_m_say_text_line_budget_cache = {}

    def _enter_m_hashable_text_key(text):
        if isinstance(text, str):
            return text

        return repr(text)

    def _enter_m_say_text_render_height(text, size, width):
        displayable = Text(
            text,
            style="say_dialogue",
            size=size,
            xsize=width,
            slow=False,
            substitute=False,
        )
        return renpy.render(displayable, width, 4096, 0, 0).get_size()[1]

    def _enter_m_say_text_line_budget_height(size, width, max_lines):
        key = (
            size,
            width,
            max_lines,
            getattr(gui, "default_font", None),
            getattr(gui, "text_xalign", None),
        )

        cached = _enter_m_say_text_line_budget_cache.get(key)
        if cached is not None:
            return cached

        marker = "\n".join(["Ag"] * max_lines)
        height = _enter_m_say_text_render_height(marker, size, width)
        _enter_m_say_text_line_budget_cache[key] = height
        return height

    def enter_m_auto_say_text_size(text):
        base_size = int(gui.say_text_size)
        min_size = min(base_size, int(getattr(gui, "say_text_fit_min_size", base_size)))
        max_lines = max(1, int(getattr(gui, "say_text_fit_max_lines", 3)))
        width = int(gui.text_width)

        if not text or base_size <= min_size:
            return base_size

        try:
            measured_text = renpy.substitute(text)
        except Exception:
            measured_text = text

        key = (
            _enter_m_hashable_text_key(measured_text),
            base_size,
            min_size,
            max_lines,
            width,
            getattr(gui, "default_font", None),
            getattr(gui, "text_xalign", None),
        )

        cached = _enter_m_say_text_fit_cache.get(key)
        if cached is not None:
            _enter_m_say_text_fit_cache.move_to_end(key)
            return cached

        try:
            result = min_size

            for candidate_size in range(base_size, min_size - 1, -1):
                text_height = _enter_m_say_text_render_height(measured_text, candidate_size, width)
                line_budget = _enter_m_say_text_line_budget_height(candidate_size, width, max_lines)

                if text_height <= line_budget + int(gui.say_text_fit_height_fudge):
                    result = candidate_size
                    break

        except Exception:
            result = base_size

        _enter_m_say_text_fit_cache[key] = result

        cache_limit = max(1, int(gui.say_text_fit_cache_limit))

        while len(_enter_m_say_text_fit_cache) > cache_limit:
            _enter_m_say_text_fit_cache.popitem(last=False)

        return result
