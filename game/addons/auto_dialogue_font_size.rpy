# =============================================================================
# auto_dialogue_font_size.rpy  --  auto-shrink long ADV dialogue to fit
# =============================================================================
#
# WHAT IT DOES
#   Keeps ADV dialogue at the normal gui.say_text_size, but if a given line would
#   render taller than a "line budget" (say_text_fit_max_lines lines), it steps
#   the size down toward say_text_fit_min_size until it fits. Stops long lines
#   from overflowing the textbox without shrinking everything globally.
#
# HOW IT'S WIRED IN
#   The say screen calls it per line:
#     game/screens.rpy ~line 141:  text what id "what" size enter_m_auto_say_text_size(what)
#   So enter_m_auto_say_text_size(text) -> the pixel font size to use for `text`.
#
# TUNABLES (gui.* defines below)
#   say_text_fit_max_lines    : how many lines = the budget (default 3).
#   say_text_fit_min_size     : smallest size it will shrink to (18).
#   say_text_fit_height_fudge : slack px added to the budget (2).
#   say_text_fit_cache_limit  : LRU cache cap for measured results (256).
#
# WHY THE CACHES
#   Measuring text by actually rendering it (renpy.render) is costly, and the say
#   screen re-evaluates every interaction, so results are memoized: one LRU cache
#   keyed by (text, sizes, width, font, align) and one for the per-size budget.
# =============================================================================

# Tunables (see header).
define gui.say_text_fit_max_lines = 3
define gui.say_text_fit_min_size = 18
define gui.say_text_fit_height_fudge = 2
define gui.say_text_fit_cache_limit = 256

init -1 python:
    from collections import OrderedDict

    # LRU cache of final sizes (text->size); plain cache of per-size line budgets.
    _enter_m_say_text_fit_cache = OrderedDict()
    _enter_m_say_text_line_budget_cache = {}

    def _enter_m_hashable_text_key(text):
        if isinstance(text, str):
            return text

        return repr(text)

    # Render `text` at a given size/width off-screen and return its pixel height.
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

    # The height of `max_lines` lines of "Ag" at this size/width = the budget a
    # real line must fit under. Cached per (size,width,max_lines,font,align).
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

    # PUBLIC: return the font size to render `text` at. Tries base_size first and
    # steps down to min_size until the rendered height fits the line budget (+fudge).
    # Memoized; returns base_size on any measurement error or when shrinking is off.
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
