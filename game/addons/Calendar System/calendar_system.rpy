# Calendar System - Persona-style date tracking and display.

define audio.calendar_tick = "mod_assets/sfx/tick.ogg"

init python:
    import calendar as py_calendar
    import datetime

    class CalendarSystem:
        """Manages in-game date tracking and display."""

        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_names_short = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        def __init__(self):
            self.current_date = datetime.date(2025, 4, 7)
            self.display_enabled = True
            self.show_year = False

        def advance_day(self, days=1):
            self.current_date += datetime.timedelta(days=days)

        def set_date(self, year, month, day):
            self.current_date = datetime.date(year, month, day)

        def get_day_of_week(self):
            return self.current_date.weekday()

        def get_day_name(self, short=False):
            names = self.day_names_short if short else self.day_names
            return names[self.get_day_of_week()]

        def get_month_name(self):
            return self.month_names[self.current_date.month - 1]

        def get_day(self):
            return self.current_date.day

        def get_month(self):
            return self.current_date.month

        def get_year(self):
            return self.current_date.year

        def get_formatted_date(self, format_type="full"):
            if format_type == "full":
                year_str = ", {}".format(self.get_year()) if self.show_year else ""
                return "{}, {} {}{}".format(self.get_day_name(), self.get_month_name(), self.get_day(), year_str)
            if format_type == "short":
                return "{} {}/{}".format(self.get_day_name(short=True), self.get_month(), self.get_day())
            if format_type == "numeric":
                return self.current_date.strftime("%m/%d/%Y")
            if format_type == "persona":
                return "{}/{} ({})".format(self.get_month(), self.get_day(), self.get_day_name(short=True))
            return str(self.current_date)

        def get_snapshot(self, date_value=None):
            if date_value is None:
                date_value = self.current_date

            weekday = date_value.weekday()
            return {
                "date": date_value,
                "day": date_value.day,
                "day_padded": "{:02d}".format(date_value.day),
                "month": date_value.month,
                "month_name": self.month_names[date_value.month - 1],
                "month_short": self.month_names[date_value.month - 1][:3].upper(),
                "year": date_value.year,
                "year_text": str(date_value.year),
                "dow": self.day_names[weekday],
                "dow_short": self.day_names_short[weekday],
                "is_weekend": weekday in (5, 6),
                "date_display": "{} {}".format(self.month_names[date_value.month - 1], date_value.day),
                "date_display_with_year": "{} {}, {}".format(self.month_names[date_value.month - 1], date_value.day, date_value.year),
                "persona": "{}/{} ({})".format(date_value.month, date_value.day, self.day_names_short[weekday]),
            }

        def is_weekend(self):
            return self.get_day_of_week() in (5, 6)

        def toggle_display(self):
            self.display_enabled = not self.display_enabled

        def show(self):
            self.display_enabled = True

        def hide(self):
            self.display_enabled = False

    class CalendarView:
        def __init__(self):
            self.viewing_year = None
            self.viewing_month = None

        def reset_to_current(self):
            self.viewing_year = calendar.get_year()
            self.viewing_month = calendar.get_month()

        def next_month(self):
            if self.viewing_month == 12:
                self.viewing_month = 1
                self.viewing_year += 1
            else:
                self.viewing_month += 1

        def prev_month(self):
            if self.viewing_month == 1:
                self.viewing_month = 12
                self.viewing_year -= 1
            else:
                self.viewing_month -= 1

    calendar_view = CalendarView()

    def get_calendar_grid(year, month):
        return py_calendar.monthcalendar(year, month)

    def show_calendar():
        calendar.show()
        renpy.show_screen("calendar_overlay")

    def hide_calendar():
        renpy.hide_screen("calendar_overlay")

default calendar = CalendarSystem()


# Script-level helpers.
label calendar_advance(days=1, animate=True):
    if animate:
        call calendar_day_transition(days) from _call_calendar_day_transition
    else:
        $ calendar.advance_day(days)
    return

label calendar_day_transition(days=1):
    $ _calendar_old_date = calendar.current_date
    $ _calendar_new_date = calendar.current_date + datetime.timedelta(days=days)
    $ _calendar_old_snapshot = calendar.get_snapshot(_calendar_old_date)
    $ _calendar_new_snapshot = calendar.get_snapshot(_calendar_new_date)
    $ calendar.current_date = _calendar_new_date
    call screen calendar_day_change(_calendar_old_snapshot, _calendar_new_snapshot)
    return

label calendar_set_date(year, month, day):
    $ calendar.set_date(year, month, day)
    return

label calendar_show:
    $ calendar.show()
    return

label calendar_hide:
    $ calendar.hide()
    return

label calendar_toggle:
    $ calendar.toggle_display()
    return


# Overlay transforms.
transform calendar_overlay_enter:
    on show:
        alpha 0.0
        yoffset -12
        easein_quad 0.25 alpha 1.0 yoffset 0
    on hide:
        alpha 1.0
        easeout_quad 0.15 alpha 0.0 yoffset -8

transform calendar_change_panel:
    alpha 0.0
    yoffset 24
    easeout_quad 0.25 alpha 1.0 yoffset 0

transform calendar_rotary_old:
    alpha 1.0
    yoffset 0
    yzoom 1.0
    pause 0.92
    easein_quad 0.28 alpha 0.55 yoffset -48 yzoom 0.72
    easeout_quad 0.38 alpha 0.0 yoffset -118 yzoom 0.42

transform calendar_rotary_new:
    alpha 0.0
    yoffset 118
    yzoom 0.42
    pause 0.92
    easeout_quad 0.38 alpha 0.65 yoffset 48 yzoom 0.74
    easeout_quad 0.32 alpha 1.0 yoffset 0 yzoom 1.0

transform cal_content_fade(delay=0.0):
    alpha 0.0
    yoffset 10
    pause delay
    easein_quad 0.25 alpha 1.0 yoffset 0


screen calendar_overlay():
    zorder 100

    if calendar.display_enabled:
        $ _cal = calendar.get_snapshot()
        $ _cal_dow_color = "#e06b6b" if _cal["is_weekend"] else "#72b8d4"

        frame:
            xalign 0.985
            yalign 0.025
            xysize (158, 70)
            background Solid("#090b10dd")
            padding (10, 7, 10, 7)
            at calendar_overlay_enter

            fixed:
                text _cal["month_short"] style "cal_overlay_month":
                    xpos 0
                    ypos 2

                text _cal["day_padded"] style "cal_overlay_day":
                    xpos 0
                    ypos 22

                add Solid("#ffffff22"):
                    xpos 58
                    ypos 10
                    xsize 1
                    ysize 44

                text _cal["dow_short"] style "cal_overlay_dow":
                    xpos 74
                    ypos 23
                    color _cal_dow_color


screen calendar_overlay_minimal():
    zorder 100

    if calendar.display_enabled:
        $ _cal_date_text = calendar.get_formatted_date("persona")

        frame:
            xalign 0.985
            yalign 0.025
            xysize (148, 42)
            background Solid("#090b10dd")
            padding (0, 0)
            at calendar_overlay_enter

            text _cal_date_text style "cal_overlay_minimal":
                xalign 0.5
                yalign 0.5


screen calendar_overlay_bottom():
    zorder 100

    if calendar.display_enabled:
        $ _cal = calendar.get_snapshot()
        $ _cal_dow_color = "#e06b6b" if _cal["is_weekend"] else "#72b8d4"

        frame:
            xalign 0.5
            yalign 0.965
            xysize (520, 46)
            background Solid("#090b10dd")
            padding (20, 0)
            at calendar_overlay_enter

            hbox:
                spacing 14
                yalign 0.5

                text _cal["dow"] style "cal_bottom_dow":
                    color _cal_dow_color

                add Solid("#ffffff33"):
                    xsize 1
                    ysize 24
                    yalign 0.5

                text _cal["date_display"] style "cal_bottom_date"


screen calendar_day_change(old_date, new_date):
    modal True
    zorder 250

    add Solid("#000000cc")

    frame:
        xalign 0.5
        yalign 0.5
        xysize (620, 290)
        background Solid("#090b10f2")
        padding (32, 26, 32, 26)
        at calendar_change_panel

        fixed:
            add Solid("#ffffff20"):
                xpos 0
                ypos 58
                xsize 556
                ysize 1

            text "DATE CHANGE" style "cal_change_label":
                xalign 0.5
                ypos 0

            frame:
                xalign 0.5
                ypos 76
                xysize (390, 156)
                background Solid("#05070cf5")
                padding (0, 0)

                fixed:
                    viewport:
                        xpos 0
                        ypos 0
                        xysize (390, 156)
                        draggable False
                        mousewheel False

                        fixed:
                            xysize (390, 156)

                            fixed:
                                xysize (300, 124)
                                xalign 0.5
                                yalign 0.5
                                at calendar_rotary_old

                                text old_date["month_short"] style "cal_change_month":
                                    xalign 0.5
                                    ypos 0
                                text old_date["day_padded"] style "cal_change_day":
                                    xalign 0.5
                                    ypos 26
                                text old_date["dow_short"] style "cal_change_dow":
                                    xalign 0.5
                                    ypos 88

                            fixed:
                                xysize (300, 124)
                                xalign 0.5
                                yalign 0.5
                                at calendar_rotary_new

                                text new_date["month_short"] style "cal_change_month":
                                    xalign 0.5
                                    ypos 0
                                text new_date["day_padded"] style "cal_change_day":
                                    xalign 0.5
                                    ypos 26
                                text new_date["dow_short"] style "cal_change_dow":
                                    xalign 0.5
                                    ypos 88

                    add Solid("#ffffff10"):
                        xpos 0
                        ypos 0
                        xsize 390
                        ysize 1

                    add Solid("#00000055"):
                        xpos 0
                        ypos 0
                        xsize 390
                        ysize 38

                    add Solid("#00000055"):
                        xpos 0
                        ypos 118
                        xsize 390
                        ysize 38

                    add Solid("#ffffff24"):
                        xpos 20
                        ypos 77
                        xsize 350
                        ysize 1

                    add Solid("#ffffff16"):
                        xpos 18
                        ypos 34
                        xsize 354
                        ysize 1

                    add Solid("#ffffff16"):
                        xpos 18
                        ypos 121
                        xsize 354
                        ysize 1

            hbox:
                xalign 0.5
                ypos 246
                spacing 14

                text old_date["persona"] style "cal_change_small_date"
                text ">" style "cal_change_small_arrow"
                text new_date["persona"] style "cal_change_small_date"

    timer 0.9 action Play("sound", audio.calendar_tick)
    timer 3.35 action Return()
    key "dismiss" action Return()

screen calendar_menu():
    tag menu

    on "show" action Function(calendar_view.reset_to_current)

    use game_menu(_("Calendar")):
        $ _cm_formatted = "{}, {} {}".format(calendar.get_day_name(), calendar.get_month_name(), calendar.get_day())
        $ _cm_year = calendar.get_year()
        $ _cm_month = calendar.get_month()
        $ _cm_day = calendar.get_day()
        $ _cm_dow = calendar.get_day_of_week()

        if calendar_view.viewing_year is None:
            $ calendar_view.reset_to_current()

        $ _cm_vy = calendar_view.viewing_year
        $ _cm_vm = calendar_view.viewing_month
        $ _cm_month_name = calendar.month_names[_cm_vm - 1]
        $ _cm_grid = get_calendar_grid(_cm_vy, _cm_vm)
        $ _cm_is_current_month = (_cm_vy == _cm_year and _cm_vm == _cm_month)

        fixed:
            xysize (880, 520)
            xalign 0.5
            yalign 0.5
            at cal_content_fade(0.0)

            vbox:
                xalign 0.5
                yalign 0.5
                spacing 16

                frame:
                    xysize (690, 58)
                    background Solid("#090b10dd")
                    padding (18, 0)

                    hbox:
                        yalign 0.5
                        spacing 14

                        text "TODAY" style "cal_menu_banner_label"
                        add Solid("#ffffff33"):
                            xsize 1
                            ysize 28
                            yalign 0.5
                        text _cm_formatted style "cal_menu_today"

                hbox:
                    spacing 14
                    xalign 0.5
                    yalign 0.5

                    textbutton "<" style "cal_nav_button" action Function(calendar_view.prev_month)

                    frame:
                        xysize (360, 48)
                        background Solid("#161b22ee")
                        padding (0, 0)

                        text _cm_month_name style "cal_menu_month_label":
                            xalign 0.5
                            yalign 0.5

                    textbutton "Today":
                        style "cal_nav_today_button"
                        action Function(calendar_view.reset_to_current)
                        sensitive not _cm_is_current_month

                    textbutton ">" style "cal_nav_button" action Function(calendar_view.next_month)

                vbox:
                    spacing 2
                    xalign 0.5

                    hbox:
                        spacing 2

                        for _hi, _dow in enumerate(calendar.day_names_short):
                            $ _hdr_active = (_cm_is_current_month and _hi == _cm_dow)
                            $ _hdr_wkend = _hi >= 5

                            frame:
                                xysize (76, 32)
                                background Solid("#cc2233" if _hdr_active else "#090b10dd")
                                padding (0, 0)

                                text _dow style "cal_day_header":
                                    xalign 0.5
                                    yalign 0.5
                                    if _hdr_active:
                                        color "#ffffff"
                                    elif _hdr_wkend:
                                        color "#e06b6b"

                    for _week in _cm_grid:
                        hbox:
                            spacing 2

                            for _wi, _wd in enumerate(_week):
                                $ _is_today = (_wd == _cm_day and _cm_is_current_month and _wd != 0)
                                $ _is_wkend = _wi >= 5
                                $ _is_past = (_cm_is_current_month and _wd != 0 and _wd < _cm_day)

                                if _wd == 0:
                                    frame:
                                        style "cal_cell_empty"

                                elif _is_today:
                                    frame:
                                        style "cal_cell_today"
                                        text "[_wd]" style "cal_cell_today_text"

                                else:
                                    $ _cell_color = "#5f6368" if _is_past else ("#e06b6b" if _is_wkend else "#d6d9df")

                                    frame:
                                        style "cal_cell"
                                        text "[_wd]" style "cal_cell_text":
                                            color _cell_color


style cal_overlay_month:
    font gui.interface_font
    size 16
    color "#d6d9df"
    outlines []

style cal_overlay_day:
    font gui.name_font
    size 31
    color "#ffffff"
    outlines [(2, "#000000", 0, 0)]

style cal_overlay_dow:
    font gui.name_font
    size 20
    color "#72b8d4"
    outlines [(1, "#000000", 0, 0)]

style cal_overlay_year:
    font gui.interface_font
    size 16
    color "#a8adb7"
    outlines []

style cal_overlay_minimal:
    font gui.name_font
    size 19
    color "#ffffff"
    outlines [(1, "#000000", 0, 0)]

style cal_bottom_dow:
    font gui.name_font
    size 22
    color "#72b8d4"
    outlines [(1, "#000000", 0, 0)]
    yalign 0.5

style cal_bottom_date:
    font gui.interface_font
    size 20
    color "#ffffff"
    outlines [(1, "#000000", 0, 0)]
    yalign 0.5

style cal_change_label:
    font gui.interface_font
    size 20
    color "#a8adb7"
    bold True
    outlines []

style cal_change_month:
    font gui.interface_font
    size 22
    color "#a8adb7"
    outlines []

style cal_change_day:
    font gui.name_font
    size 58
    color "#ffffff"
    outlines [(3, "#000000", 0, 0)]

style cal_change_dow:
    font gui.name_font
    size 24
    color "#cc2233"
    outlines [(2, "#000000", 0, 0)]

style cal_change_arrow:
    font gui.name_font
    size 42
    color "#ffffff66"
    outlines []

style cal_change_small_date:
    font gui.interface_font
    size 18
    color "#a8adb7"
    outlines []

style cal_change_small_arrow:
    font gui.interface_font
    size 18
    color "#ffffff55"
    outlines []

style cal_menu_banner_label:
    font gui.name_font
    size 19
    color "#cc2233"
    outlines [(1, "#000000", 0, 0)]
    yalign 0.5

style cal_menu_today:
    font gui.interface_font
    size 21
    color "#ffffff"
    outlines [(1, "#000000", 0, 0)]
    yalign 0.5

style cal_menu_month_label:
    font gui.name_font
    size 28
    color "#ffffff"
    outlines [(2, "#000000", 0, 0)]

style cal_nav_button:
    xysize (48, 48)
    background Solid("#161b22ee")
    hover_background Solid("#cc2233")
    padding (0, 0)
    yalign 0.5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style cal_nav_button_text:
    font gui.name_font
    size 24
    color "#ffffff"
    bold True
    xalign 0.5
    yalign 0.5
    outlines [(1, "#000000", 0, 0)]

style cal_nav_today_button:
    xysize (94, 48)
    background Solid("#161b22ee")
    hover_background Solid("#cc2233")
    insensitive_background Solid("#090b10bb")
    padding (0, 0)
    yalign 0.5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style cal_nav_today_button_text:
    font gui.interface_font
    size 17
    color "#ffffff"
    insensitive_color "#5f6368"
    bold True
    xalign 0.5
    yalign 0.5
    outlines [(1, "#000000", 0, 0)]

style cal_day_header:
    font gui.interface_font
    size 15
    color "#8f96a3"
    bold True
    text_align 0.5
    outlines []

style cal_cell:
    xysize (76, 48)
    background Solid("#161b22dd")
    padding (0, 0)

style cal_cell_empty:
    xysize (76, 48)
    background Solid("#090b1099")
    padding (0, 0)

style cal_cell_text:
    font gui.interface_font
    size 22
    color "#d6d9df"
    xalign 0.5
    yalign 0.5
    text_align 0.5
    outlines [(1, "#000000", 0, 0)]

style cal_cell_today:
    xysize (76, 48)
    background Solid("#cc2233")
    padding (0, 0)

style cal_cell_today_text:
    font gui.name_font
    size 23
    color "#ffffff"
    bold True
    xalign 0.5
    yalign 0.5
    text_align 0.5
    outlines [(2, "#000000", 0, 0)]
