# Shared story choices: lower-third plates, lifted when a prompt owns the
# textbox, with caption-sized widths, previous-choice marks and number keys.
# CHOICE_* geometry matches the plate art in assets/gui/choice/; change both.
#
# Each plate is a top-level button so screen hide events reach its transform.
# Keep transform arguments constant during the menu's lifetime: the hide pass
# re-evaluates the screen. Selection travels through _enter_m_choice_fx;
# choice_lifted is a screen default so hiding say cannot move the exit stack.
# Nested button transforms receive hover/idle events.

define CHOICE_ROOT = "assets/gui/choice/"

# Geometry (matches the plate art).
define CHOICE_SLOPE = 0.36          # lean of every cut, px per px of height
define CHOICE_H = {1: 54, 2: 88}    # plate height by caption line count
define CHOICE_TAIL = 13             # speech-tail canvas under a spoken plate
define CHOICE_SRC_LEFT = 64         # three-slice borders of the plate sources
define CHOICE_SRC_RIGHT = 44

# Layout.
define CHOICE_TEXT_MAX = 680        # widest caption column; longer ones wrap
define CHOICE_TEXT_MIN = 200        # narrowest, so short menus are not slivers
define CHOICE_CHIP_X = 10           # mid-height left cut -> index chip
define CHOICE_TEXT_X = 58           # mid-height left cut -> caption
define CHOICE_RPAD = 36             # caption column -> mid-height right cut
define CHOICE_GAP = 12              # between plates (a speech tail is 13)
define CHOICE_BOTTOM = 690          # stack bottom with no textbox up
define CHOICE_BOTTOM_SAY = 516      # stack bottom above the namebox
define CHOICE_LEAN = 74.0 / 720.0   # ENTER_M_PANEL_SLANT over screen height
define CHOICE_STAGGER = 0.05        # cascade step, top plate first
define CHOICE_SCRIM_ALPHA = 0.85    # lower-third darkening (asset peaks at 50%)

define CHOICE_STREAK = Frame(CHOICE_ROOT + "streak.png", 20, 0, 20, 0)
define CHOICE_CHIP_IDLE = CHOICE_ROOT + "chip_idle.png"
define CHOICE_CHIP_HOVER = CHOICE_ROOT + "chip_hover.png"
define CHOICE_TICK = CHOICE_ROOT + "tick.png"


init python:
    import builtins as _enter_m_choice_builtins
    import re as _enter_m_choice_re

    class _EnterMChoiceFX(object):
        """Which plate the player took, read by the exit animation."""

        def __init__(self):
            self.picked = -1

    _enter_m_choice_fx = _EnterMChoiceFX()

    def enter_m_choice_pick(idx):
        _enter_m_choice_fx.picked = idx

    def enter_m_choice_reset():
        _enter_m_choice_fx.picked = -1

    def enter_m_choice_exit(idx):
        """
        ATL `function` for a plate's `on hide`. Decides once, on its first
        call, whether this plate was the one taken -- a menu shown straight
        after this one resets the pick while this exit is still playing.
        """

        memo = {}

        def run(trans, st, at):
            if "picked" not in memo:
                memo["picked"] = (_enter_m_choice_fx.picked == idx)

            if memo["picked"]:
                if st < 0.06:
                    k = st / 0.06
                    trans.matrixcolor = BrightnessMatrix(0.6 * k)
                    trans.xzoom = 1.0 + 0.06 * k
                    trans.yzoom = 1.0 + 0.10 * k
                else:
                    k = min((st - 0.06) / 0.26, 1.0)
                    e = k * k
                    trans.matrixcolor = BrightnessMatrix(0.6 * (1.0 - k))
                    trans.xzoom = 1.06 + 0.05 * k
                    trans.yzoom = max(1.10 - 1.08 * e, 0.02)
                    trans.xoffset = 44.0 * e
                    trans.alpha = 1.0 - e
                return 0 if st < 0.32 else None

            k = min(st / 0.14, 1.0)
            trans.yzoom = max(1.0 - k * k, 0.02)
            trans.alpha = 1.0 - k
            return 0 if st < 0.14 else None

        return run

    def enter_m_choice_actions(item, idx):
        """
        (button action, key action) for one menu entry. Both record the pick
        first, then run the exam guard's wrapping of the real choice.
        """

        action = exam_guard_choice_action(getattr(item, "action", None))
        if action is None:
            return None, None

        if not isinstance(action, list):
            action = [action]

        pick = Function(enter_m_choice_pick, idx)
        sound = Function(renpy.play, gui.activate_sound)
        return [pick] + action, [pick, sound] + action

    # Layout is cached per menu. A plain dict, not the store's revertable
    # one: this is derived data and has no business in rollback or saves.
    _enter_m_choice_cache = _enter_m_choice_builtins.dict()

    _ENTER_M_CHOICE_SPOKEN = _enter_m_choice_re.compile(
        r'\s*(?:\{[^}]*\}\s*)*["“]')

    class EnterMChoiceRow(object):
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    class EnterMChoiceLayout(object):
        def __init__(self, rows, scrim_h):
            self.rows = rows
            self.scrim_h = scrim_h

    def _enter_m_choice_text_size(caption, width):
        return Text(caption, style="choice_plate_caption").size(width=width)

    def enter_m_choice_layout(items, lifted):
        # MenuEntry is a tuple (caption, action, chosen); menu prediction
        # passes plain tuples of the same shape.
        captions = tuple(i[0] for i in items)
        chosen = tuple(bool(i[2]) if len(i) > 2 else False for i in items)
        key = (captions, chosen, bool(lifted), _preferences.language)

        rv = _enter_m_choice_cache.get(key)
        if rv is not None:
            return rv

        one_line = _enter_m_choice_text_size("Ag", 4000)[1]
        natural = [_enter_m_choice_text_size(c, 4000)[0] for c in captions]
        tw = int(min(CHOICE_TEXT_MAX, max([CHOICE_TEXT_MIN] + natural))) + 1
        span = CHOICE_TEXT_X + tw + CHOICE_RPAD

        lines = []
        for c in captions:
            h = _enter_m_choice_text_size(c, tw)[1]
            lines.append(2 if h > one_line * 1.5 else 1)

        heights = [CHOICE_H[n] for n in lines]
        total = sum(heights) + CHOICE_GAP * max(len(heights) - 1, 0)
        bottom = CHOICE_BOTTOM_SAY if lifted else CHOICE_BOTTOM

        centres = []
        y = bottom - total
        for h in heights:
            centres.append(y + h / 2.0)
            y += h + CHOICE_GAP

        # Rows drift right as they rise, along the gutter angle; the whole
        # stack stays centred on the screen.
        shifts = [(centres[-1] - cy) * CHOICE_LEAN for cy in centres] if centres else []
        drift = (max(shifts) + min(shifts)) / 2.0 if shifts else 0.0
        col = config.screen_width / 2.0 - span / 2.0

        rows = []
        for idx, c in enumerate(captions):
            n = lines[idx]
            h = heights[idx]
            lean = CHOICE_SLOPE * h
            mid = lean / 2.0
            spoken = bool(_ENTER_M_CHOICE_SPOKEN.match(c))
            suffix = "_{}{}.png".format(n, "_say" if spoken else "")
            glint = CHOICE_ROOT + "glint_{}.png".format(n)
            glint_w = renpy.image_size(glint)[0]
            w = int(round(span + lean))
            x = int(round(col + shifts[idx] - drift - mid))

            rows.append(EnterMChoiceRow(
                idx=idx,
                caption=c,
                chosen=chosen[idx],
                number=str(idx + 1) if idx < 9 else "",
                delay=CHOICE_STAGGER * idx,
                x=x,
                cy=int(round(centres[idx])),
                w=w,
                h=h,
                ch=h + (CHOICE_TAIL if spoken else 0),
                mx=int(round(x + mid)),
                span=span,
                tw=tw,
                chip_cx=int(round(mid + CHOICE_CHIP_X + 18)),
                text_x=int(round(mid + CHOICE_TEXT_X)),
                tick_x=int(round(mid + CHOICE_TEXT_X + tw + 8)),
                idle=Frame(CHOICE_ROOT + "idle" + suffix, CHOICE_SRC_LEFT, 0, CHOICE_SRC_RIGHT, 0),
                wash=Frame(CHOICE_ROOT + "wash" + suffix, CHOICE_SRC_LEFT, 0, CHOICE_SRC_RIGHT, 0),
                flash=Frame(CHOICE_ROOT + "flash" + suffix, CHOICE_SRC_LEFT, 0, CHOICE_SRC_RIGHT, 0),
                glint=glint,
                glint_x0=int(round(lean)),
                glint_x1=max(w - glint_w - int(round(lean)), 0),
                ))

        # The scrim darkens the band the stack sits in. With a textbox up it
        # would darken the prompt too, so a lifted menu goes without.
        scrim_h = 0 if lifted else max(260, int(config.screen_height - (bottom - total) + 90))

        rv = EnterMChoiceLayout(rows, scrim_h)
        if len(_enter_m_choice_cache) > 64:
            _enter_m_choice_cache.clear()
        _enter_m_choice_cache[key] = rv
        return rv


screen choice(items):

    default choice_lifted = (renpy.get_screen("say") is not None)

    $ choice_layout = enter_m_choice_layout(items, choice_lifted)

    on "show" action Function(enter_m_choice_reset)

    if choice_layout.scrim_h:
        add Transform(CHOICE_ROOT + "scrim.png", xysize=(config.screen_width, choice_layout.scrim_h)):
            ypos config.screen_height
            yanchor 1.0
            at choice_scrim_show

    for r in choice_layout.rows:
        $ choice_button_action, choice_key_action = enter_m_choice_actions(items[r.idx], r.idx)

        add CHOICE_STREAK:
            xpos r.mx
            ypos r.cy
            yanchor 0.5
            xysize (r.span, 14)
            at choice_streak(r.delay)

        # The button itself NEVER moves while the menu is up: its only
        # transform is the exit, which is idle until `hide`. Entrance and
        # hover animate the plate INSIDE it. A button that kicks or swells
        # under a still cursor drags its own hit box out from under it, drops
        # to idle, slides back, re-hovers -- and a plate caught in that loop
        # mid-entrance settles wherever the last ease left it.
        button:
            style "choice_plate_button"
            xpos r.x
            ypos r.cy
            yanchor 0.5
            xysize (r.w, r.h)
            action choice_button_action
            at choice_plate_exit(r.idx)

            fixed:
                xysize (r.w, r.h)
                ypos r.h // 2
                yanchor 0.5
                at choice_plate_enter(r.delay), choice_plate_hover

                add r.idle xysize (r.w, r.ch)
                add r.wash xysize (r.w, r.ch) at choice_wash
                add r.glint at choice_glint(r.glint_x0, r.glint_x1)
                add r.flash xysize (r.w, r.ch) at choice_flash(r.delay)

                fixed:
                    xysize (36, 26)
                    xpos r.chip_cx
                    ypos r.h // 2
                    xanchor 0.5
                    yanchor 0.5
                    at choice_chip_pop(r.delay)

                    add CHOICE_CHIP_IDLE
                    add CHOICE_CHIP_HOVER at choice_hover_fade
                    if r.number:
                        text r.number style "choice_plate_index"

                text r.caption:
                    style ("choice_plate_caption_chosen" if r.chosen else "choice_plate_caption")
                    xpos r.text_x
                    ypos r.h // 2
                    yanchor 0.5
                    xmaximum r.tw
                    at choice_text_in(r.delay)

                if r.chosen:
                    add CHOICE_TICK:
                        xpos r.tick_x
                        ypos r.h // 2
                        yanchor 0.5
                        at choice_text_in(r.delay)

        if choice_key_action is not None and r.number:
            key ("K_" + r.number) action choice_key_action
            key ("K_KP" + r.number) action choice_key_action


style choice_plate_button is empty:
    background None
    padding (0, 0, 0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

# Hover changes COLOUR only. Anything that changes the laid-out size (a wider
# outline, a different font) would wrap differently from the measurement the
# plate height was chosen by.
style choice_plate_caption is default:
    font gui.default_font
    size 24
    color "#eef6f8"
    hover_color "#ffffff"
    selected_color "#ffffff"
    insensitive_color "#7d8f97"
    outlines [(1, "#02050acc", 0, 1)]
    hover_outlines [(1, "#3a0716d0", 0, 1)]
    selected_outlines [(1, "#3a0716d0", 0, 1)]
    text_align 0.0

style choice_plate_caption_chosen is choice_plate_caption:
    color "#a9c3cd"

style choice_plate_index is default:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 14
    color "#56d7ff"
    hover_color "#ff315b"
    selected_color "#ff315b"
    outlines []
    xalign 0.5
    yalign 0.5
    xoffset 1


# -----------------------------------------------------------------------------
# Motion
# -----------------------------------------------------------------------------
#
# `exit` sits on the button, because the screen hands `hide` only to its
# top-level children. `enter` and `hover` sit on the plate inside the button,
# so neither can move the hit box (see the note in the screen).

transform choice_scrim_show:
    on start:
        alpha 0.0
        easeout 0.28 alpha CHOICE_SCRIM_ALPHA
    on hide:
        linear 0.24 alpha 0.0

# The cut: shoots across the plate's centre line, then blows out and fades as
# the plate opens out of it. `delay` is the plate's cascade slot.
transform choice_streak(delay=0.0):
    subpixel True
    alpha 0.0
    xzoom 0.02
    pause delay
    alpha 1.0
    easeout_quart 0.10 xzoom 1.0
    parallel:
        easeout_quad 0.24 yzoom 3.4
    parallel:
        linear 0.24 alpha 0.0

transform choice_plate_enter(delay=0.0):
    subpixel True
    alpha 0.0
    yzoom 0.02
    pause delay + 0.06
    parallel:
        linear 0.05 alpha 1.0
    parallel:
        easeout_quad 0.08 yzoom 1.18
        easein_quad 0.07 yzoom 0.94
        easeout_quad 0.09 yzoom 1.0

transform choice_plate_hover:
    subpixel True
    on idle:
        easeout_cubic 0.20 xoffset 0 zoom 1.0 alpha 1.0
    on hover:
        easeout_back 0.18 xoffset 14 zoom 1.03 alpha 1.0
    on insensitive:
        easeout 0.20 xoffset 0 zoom 1.0 alpha 0.55

transform choice_plate_exit(idx=0):
    on hide:
        function enter_m_choice_exit(idx)

# The wipe is a CROP, not an xzoom. Scaling the wash squashes the whole plate
# shape into the revealed sliver -- the slanted ends flatten toward vertical
# and the sliver spills out past the left cut and under the speech tail. A
# crop leaves every pixel where it belongs and just uncovers them.
transform choice_wash:
    xanchor 0.0
    crop_relative True
    alpha 0.0
    on hover, selected_idle, selected_hover:
        alpha 1.0
        crop (0.0, 0.0, 0.02, 1.0)
        easeout_quart 0.16 crop (0.0, 0.0, 1.0, 1.0)
    on idle:
        easeout_quad 0.14 alpha 0.0

# Starts just inside the left cut, so the band never hangs off the plate.
transform choice_glint(x0=0, x1=100):
    blend "add"
    alpha 0.0
    on hover:
        xpos x0
        alpha 0.0
        pause 0.05
        parallel:
            ease_quad 0.34 xpos x1
        parallel:
            linear 0.08 alpha 0.9
            pause 0.12
            linear 0.14 alpha 0.0
    on idle:
        linear 0.08 alpha 0.0

# The entrance flash, then a softer blink on every hover after it.
transform choice_flash(delay=0.0):
    blend "add"
    alpha 0.0
    pause delay + 0.06
    alpha 0.9
    easeout_quad 0.24 alpha 0.0
    on hover:
        alpha 0.42
        easeout_quad 0.26 alpha 0.0

transform choice_chip_pop(delay=0.0):
    subpixel True
    alpha 0.0
    zoom 1.9
    pause delay + 0.12
    parallel:
        linear 0.06 alpha 1.0
    parallel:
        easeout_back 0.22 zoom 1.0

transform choice_hover_fade:
    alpha 0.0
    on hover, selected_idle, selected_hover:
        easeout 0.10 alpha 1.0
    on idle:
        easeout 0.14 alpha 0.0

# From the right: sliding in from the left drags the caption across the chip.
transform choice_text_in(delay=0.0):
    subpixel True
    alpha 0.0
    xoffset 18
    pause delay + 0.12
    parallel:
        linear 0.10 alpha 1.0
    parallel:
        easeout_cubic 0.24 xoffset 0
