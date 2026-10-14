# Per-save story date (calendar), corner overlay, day transition and month grid.
# CalendarSystem owns the date and formatted snapshots consumed by phone/screens;
# CalendarView browses months independently of the current story date.
# Use calendar.set_date(), calendar_advance(days=, animate=), show_calendar() and
# hide_calendar(). ShowMenu("calendar_menu") opens the calendar from navigation.
# The day-change screen snapshots old/new dates and animates the enter_m.cal_dial
# shader and rolling date cells. Read get_snapshot() for shared display fields.

init python:
    import calendar as py_calendar
    import datetime

    # The date model. Holds the current date + display flags, and knows how to
    # format itself every way the UI needs. Instantiated once as `calendar` below.
    class CalendarSystem:
        """Manages in-game date tracking and display."""

        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_names_short = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        def __init__(self):
            self.current_date = datetime.date(2025, 4, 7)  # default start date
            self.display_enabled = True   # is the overlay allowed to render?
            self.show_year = False        # include the year in "full" format?

        # Mutators: move the date forward/back, or jump to an absolute date.
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

        # One-string formatters. Examples (for Thu, May 15 2025):
        #   "full"    -> "Thursday, May 15" (+ ", 2025" if show_year)
        #   "short"   -> "THU 5/15"
        #   "numeric" -> "05/15/2025"
        #   "persona" -> "5/15 (THU)"
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

        # Return a dict of EVERY pre-formatted field a screen (or the Phone
        # System) might want for a given date (defaults to the current date).
        # The day-change panel passes explicit old/new dates to snapshot both.
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

    # Browsing state for the month-grid menu ONLY (which month is on screen).
    # Separate from CalendarSystem so paging around the menu never moves the
    # actual in-game date. Singleton instance `calendar_view` below.
    #
    # NoRollback because this is pure UI state: rolling the story back should
    # not move the month the player happens to be looking at, and none of it
    # belongs in a save. (It is not what caused the Sep 2026 "arrows skip a
    # month" bug -- that was screen prediction; see the note on calendar_menu.)
    class CalendarView(renpy.python.NoRollback):
        def __init__(self):
            self.viewing_year = None
            self.viewing_month = None

        # Browsing is clamped to the story's own window (see
        # CALENDAR_STORY_FIRST / _LAST): the player can walk every month the
        # story reaches and no further.

        def _bounds(self):
            fy, fm, _ = CALENDAR_STORY_FIRST
            ly, lm, _ = CALENDAR_STORY_LAST
            return (fy * 12 + fm - 1, ly * 12 + lm - 1)

        def current_month(self):
            """
            (year, month) the grid is showing. Falls back to the story's own
            month and WRITES NOTHING: the menu screen has to stay side-effect
            free (see the note on calendar_menu).
            """
            if self.viewing_year is None:
                return (calendar.get_year(), calendar.get_month())
            return (self.viewing_year, self.viewing_month)

        def _index(self):
            year, month = self.current_month()
            return year * 12 + month - 1

        def _go(self, index):
            low, high = self._bounds()
            index = max(low, min(high, index))
            self.viewing_year, month = divmod(index, 12)
            self.viewing_month = month + 1

        def can_prev(self):
            return self._index() > self._bounds()[0]

        def can_next(self):
            return self._index() < self._bounds()[1]

        def reset_to_current(self):
            self.viewing_year = calendar.get_year()
            self.viewing_month = calendar.get_month()
            self._go(self._index())

        def next_month(self):
            self._go(self._index() + 1)

        def prev_month(self):
            self._go(self._index() - 1)

    calendar_view = CalendarView()

    # 2D list of week rows for the menu grid (0 = day not in this month).
    def get_calendar_grid(year, month):
        return py_calendar.monthcalendar(year, month)

    # show/hide the corner overlay. show_calendar both enables the flag AND
    # shows the screen; hide just hides the screen (the date itself is untouched).
    def show_calendar():
        calendar.show()
        renpy.show_screen("calendar_overlay")

    def hide_calendar():
        renpy.hide_screen("calendar_overlay")

    def calendar_story_window():
        """The story's own span, as dates: (first playable, last playable)."""
        return (datetime.date(*CALENDAR_STORY_FIRST),
                datetime.date(*CALENDAR_STORY_LAST))

    def calendar_cell_state(year, month, day):
        """'outside', 'past', 'today' or 'future' for one menu grid cell."""
        cell = datetime.date(year, month, day)
        first, last = calendar_story_window()

        if cell < first or cell > last:
            return "outside"
        if cell < calendar.current_date:
            return "past"
        if cell == calendar.current_date:
            return "today"
        return "future"

    def calendar_cell_color(state, weekend):
        if state == "outside":
            return "#4f5c5a"
        if state == "past":
            return "#71807e"
        return ROOM_MENU_CORAL if weekend else ROOM_MENU_PAPER

    def calendar_month_fraction(date_value):
        """
        Where a date sits in its own month, as a fraction of a full turn:
        0.0 on the 1st, one day short of 1.0 on the last. Dividing by the
        month's length rather than by (length - 1) is what keeps the last day
        of the month from pointing at exactly the same place as the first.

        Drives the corner badge's dial pointer.
        """
        # py_calendar, not `calendar`: the latter is the game's own object.
        days = py_calendar.monthrange(date_value.year, date_value.month)[1]
        return (date_value.day - 1) / float(max(days, 1))

# The live calendar object (per-save). Everything above is the blueprint; THIS
# is the instance the whole game reads/writes.
default calendar = CalendarSystem()

# The story's span. The menu browses these months and no others, and days
# outside the span are drawn as unreachable. Season 1 opens on 2025-05-15
# (story/season1/0515.rpy); the Developer Date Jump calls the same span "the
# May 2025-March 2026 story year".
define CALENDAR_STORY_FIRST = (2025, 5, 15)
define CALENDAR_STORY_LAST = (2026, 3, 7)

define cal_dial_face_size = 350
define cal_dial_glow_pad = 90
define cal_dial_render_size = cal_dial_face_size + cal_dial_glow_pad
define cal_dial_render_offset = cal_dial_glow_pad // 2
define cal_dial_fill = float(cal_dial_face_size) / float(cal_dial_render_size)


# -----------------------------------------------------------------------------
# ROTARY DIAL SHADER (day-change panel). gl2 / GLSL ES 3.00. One shader draws
# the whole chrono-instrument: a round hub face (the date reads on it), read-line
# side ticks, a rotating dashed hairline, a thick month-progress arc that fills
# 12-o'clock -> current day, 60 minor / 12 hour / 4 cardinal ticks, a beveled
# double outer bezel with a directional metal sheen, and a tapered pointer riding
# the rim. Solid parts are over-composited into (col,a); glows (rim bloom, arc
# comet head, pointer tip, radar sweep) are added as premultiplied emissive light
# so they read bright. Driven by u_sweep (0..1 = fraction through the month,
# animated old->new), u_glow (breathing), u_time (rotations). Ignores tex0.
#
# CRITICAL: the transform sets `mesh True` AND is applied to an OPAQUE
# Solid("#000000") base -- a shader only engages via the mesh/model path, and a
# transparent base is culled before it can run (matches PhonePanel). Also: the
# shader is registered in `init python`, which does NOT re-run on hot-reload --
# edits here need a FULL game restart to take effect.
# -----------------------------------------------------------------------------
init python:
    def _enter_m_calendar_register_shaders():

        renpy.register_shader("enter_m.cal_dial", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_model_size;
            uniform float u_sweep;
            uniform float u_glow;
            uniform float u_time;
            uniform float u_dial_fill;
            uniform vec4 u_accent;
            uniform vec4 u_track;
            uniform vec4 u_disc;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float enterm_ring(float r, float lo, float hi) {
                return step(lo, r) * step(r, hi);
            }
        """, fragment_300="""
            vec2 size = max(u_model_size, vec2(1.0));
            float dial_fill = clamp(u_dial_fill, 0.25, 1.0);
            float R = min(size.x, size.y) * 0.5 * dial_fill;
            vec2 p = (v_tex_coord - vec2(0.5)) * size;
            float rr = length(p);
            float r = rr / R;                          // 0 center .. 1 edge
            float ang = atan(p.x, -p.y);               // 0 at top, clockwise +
            float frac = ang / 6.28318530718;
            frac = frac - floor(frac);                 // 0..1 clockwise from top
            float sweep = u_sweep - floor(u_sweep);    // 0..1
            float pw = 1.6 / R;                         // ~1.6px in r-units (AA)
            float xf = p.x / R;
            float yf = p.y / R;

            vec3 acc = u_accent.rgb;
            vec3 trk = u_track.rgb;

            // directional bevel light (bright toward top-left) for a metal sheen
            vec2 nd = rr > 0.001 ? p / rr : vec2(0.0, -1.0);
            float light = 0.55 + 0.45 * clamp((-nd.y - nd.x) * 0.7071, -1.0, 1.0);

            // ================= SOLID PARTS (over-composited) ================
            vec3 col = vec3(0.0);
            float a = 0.0;

            // hub face -- the round dial the date reads on
            float hub = 1.0 - smoothstep(0.63 - pw * 2.0, 0.63 + pw * 2.0, r);
            float vign = 1.0 - 0.45 * smoothstep(0.0, 0.63, r);
            float gloss = 0.14 * clamp(-nd.y, 0.0, 1.0);
            vec3 hcol = u_disc.rgb * vign + acc * gloss * hub;
            float hla = hub * u_disc.a;
            col = mix(col, hcol, hla); a = a + hla * (1.0 - a);

            // read-line side ticks flanking the date slot (no full box)
            float rl = (1.0 - smoothstep(0.0, 0.013, abs(abs(yf) - 0.30))) * step(0.30, abs(xf)) * step(abs(xf), 0.47);
            float rla = rl * 0.55;
            col = mix(col, acc, rla); a = a + rla * (1.0 - a);

            // slow rotating dashed hairline (instrument life)
            float dband = enterm_ring(r, 0.655, 0.672);
            float dla = dband * step(0.5, fract(frac * 60.0 + u_time * 0.03)) * 0.30;
            col = mix(col, trk, dla); a = a + dla * (1.0 - a);

            // month-progress arc: dim track + lit fill (0 -> sweep)
            float aband = enterm_ring(r, 0.70, 0.775);
            float behind = sweep - frac;
            float inArc = smoothstep(0.0, 0.004, behind);
            float atk = aband * (1.0 - inArc) * 0.20;
            col = mix(col, trk, atk); a = a + atk * (1.0 - a);
            float alt = aband * inArc * 0.85;
            col = mix(col, acc, alt); a = a + alt * (1.0 - a);

            // tick ring: 60 minor / 12 hour / 4 cardinal
            float tdm = min(fract(frac * 60.0), 1.0 - fract(frac * 60.0));
            float mla = (1.0 - smoothstep(0.05, 0.10, tdm)) * enterm_ring(r, 0.855, 0.945) * 0.5;
            col = mix(col, trk, mla); a = a + mla * (1.0 - a);
            float tdh = min(fract(frac * 12.0), 1.0 - fract(frac * 12.0));
            float hla2 = (1.0 - smoothstep(0.04, 0.08, tdh)) * enterm_ring(r, 0.82, 0.965) * (0.6 + 0.4 * light);
            col = mix(col, acc, hla2); a = a + hla2 * (1.0 - a);
            float tdc = min(fract(frac * 4.0), 1.0 - fract(frac * 4.0));
            float cla = (1.0 - smoothstep(0.025, 0.055, tdc)) * enterm_ring(r, 0.80, 0.975);
            col = mix(col, acc, cla); a = a + cla * (1.0 - a);

            // outer bezel: beveled double ring
            float b1 = (1.0 - smoothstep(0.0, 0.006, abs(r - 0.965))) * (0.5 + 0.5 * light);
            col = mix(col, acc, b1); a = a + b1 * (1.0 - a);
            float b2 = (1.0 - smoothstep(0.0, 0.005, abs(r - 0.996))) * (0.4 + 0.6 * light) * 0.85;
            col = mix(col, acc * 0.85, b2); a = a + b2 * (1.0 - a);

            // pointer body: tapered marker riding the rim at angle = sweep
            float ad = abs(frac - sweep);
            ad = min(ad, 1.0 - ad);
            float prad = enterm_ring(r, 0.64, 0.83);
            float taper = mix(0.026, 0.006, smoothstep(0.64, 0.83, r));
            float pla = (1.0 - smoothstep(taper, taper + pw, ad)) * prad;
            col = mix(col, acc, pla); a = a + pla * (1.0 - a);

            // ================= EMISSIVE GLOWS (additive light) =============
            vec3 outc = col * a;                 // premultiplied base
            float outa = a;

            // rim bloom halo
            float halo_fade = 1.0 - smoothstep(1.02, 1.22, r);
            float halo = exp(-abs(r - 0.90) * 5.5) * 0.24 * halo_fade;
            outc += acc * halo; outa = max(outa, halo);
            // comet head at the arc's leading edge
            float head = aband * exp(-max(behind, 0.0) * 70.0) * (0.7 + 0.5 * u_glow);
            outc += (acc + vec3(0.35)) * head; outa = max(outa, clamp(head, 0.0, 1.0));
            // glowing pointer tip
            float ptx = (r - 0.82) / 0.05;
            float ptip = exp(-ptx * ptx) * (1.0 - smoothstep(0.02, 0.07, ad)) * (0.7 + 0.5 * u_glow);
            outc += (acc + vec3(0.35)) * ptip; outa = max(outa, clamp(ptip, 0.0, 1.0));
            // faint continuous radar sweep
            float sang = frac - fract(u_time * 0.05);
            sang = sang - floor(sang);
            float radar = (1.0 - smoothstep(0.0, 0.14, sang)) * enterm_ring(r, 0.63, 0.80) * 0.12;
            outc += acc * radar; outa = max(outa, radar);

            gl_FragColor = vec4(outc, clamp(outa, 0.0, 1.0));
        """)

    try:
        _enter_m_calendar_register_shaders()
    except Exception as e:
        renpy.log("ENTER-M CALENDAR: shader registration failed: %r" % e)


# -----------------------------------------------------------------------------
# SCRIPT-LEVEL LABEL HELPERS
# Thin `call`-able wrappers so story scripts can advance/set/show the date as
# statements. calendar_advance is the one to prefer for day breaks: animate=True
# routes through calendar_day_transition (the rotary-flip panel) which also
# performs the actual date change; animate=False just bumps the date silently.
# -----------------------------------------------------------------------------
# Script-level helpers.
label calendar_advance(days=1, animate=True):
    if animate:
        call calendar_day_transition(days) from _call_calendar_day_transition
    else:
        $ calendar.advance_day(days)
    return

# Snapshot the old + new dates, commit the change, then show the animated panel.
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


# Overlay transforms. (calendar_rotary_old/new drive the day-change "flip":
# the old date slides up and fades while the new date rises into its place.)
# Overlay transforms.
# The badge dial's pointer. Rotation is about the image's own centre, and the
# 64px canvas is placed centred on the dial, so the nib tracks the rim.
transform cal_overlay_hand(angle=0.0):
    rotate angle


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
    zoom 0.94
    easeout_quad 0.30 alpha 1.0 zoom 1.0

# The date cell rolling up off the hub (old) / rising onto it (new). yzoom crush
# at the extremes fakes the foreshortening of a rotating cylinder; alpha fades
# each cell out before the viewport's edge so the roll reads clean on the face.
transform calendar_rotary_old:
    yoffset 0
    yzoom 1.0
    alpha 1.0
    pause 1
    parallel:
        easein_cubic 0.64 yoffset -150 yzoom 0.34
    parallel:
        linear 0.34 alpha 1.0
        linear 0.30 alpha 0.0

transform calendar_rotary_new:
    yoffset 150
    yzoom 0.34
    alpha 0.0
    pause 1
    parallel:
        easeout_cubic 0.64 yoffset 0 yzoom 1.0
    parallel:
        linear 0.34 alpha 0.55
        linear 0.30 alpha 1.0

# The rotary gauge. Holds at the old day, then sweeps the needle/arc to the new
# day with a small overshoot before settling; u_glow then breathes forever to
# keep the needle alive (and the shader redrawing) while the panel is up.
transform cal_dial(f0, f1):
    mesh True
    shader "enter_m.cal_dial"
    u_accent (0.40, 0.88, 1.0, 1.0)
    u_track (0.34, 0.52, 0.62, 1.0)
    u_disc (0.055, 0.095, 0.140, 0.92)
    u_glow 1.0
    u_dial_fill cal_dial_fill
    xysize (cal_dial_render_size, cal_dial_render_size)
    u_sweep f0
    pause 1
    easein_cubic 0.80 u_sweep (f1 + 0.03)
    easeout_quad 0.22 u_sweep f1
    block:
        easeout_quad 1.10 u_glow 0.55
        easein_quad 1.10 u_glow 1.0
        repeat

transform cal_pip_blink:
    alpha 1.0
    easeout_quad 0.90 alpha 0.25
    easein_quad 0.90 alpha 1.0
    repeat

transform cal_content_fade(delay=0.0):
    alpha 0.0
    yoffset 10
    pause delay
    easein_quad 0.25 alpha 1.0 yoffset 0


# Corner date badge (shown via show_calendar()). Gates on
# calendar.display_enabled and tints weekends red.
screen calendar_overlay():
    zorder 100

    if calendar.display_enabled:
        $ _cal = calendar.get_snapshot()
        $ _cal_weekend = _cal["is_weekend"]
        $ _cal_dow_color = "#e06b6b" if _cal_weekend else "#72b8d4"
        $ _cal_page = "assets/gui/hud/cal_page_weekend.png" if _cal_weekend else "assets/gui/hud/cal_page.png"
        $ _cal_hand = "assets/gui/hud/cal_hand_weekend.png" if _cal_weekend else "assets/gui/hud/cal_hand.png"
        $ _cal_angle = 360.0 * calendar_month_fraction(_cal["date"])

        # A calendar page, not a button: square, with a punched month strip
        # and one clipped corner. The day number sits in a clock dial whose
        # pointer rides the rim at the day's place in the month -- the same
        # sweep the day-change panel's big dial uses. Weekends swap the whole
        # page (strip, ring and pointer) for the coral variant.
        fixed:
            xalign 0.985
            yalign 0.025
            xysize (176, 78)
            at calendar_overlay_enter

            add _cal_page

            text _cal["month_short"] style "cal_overlay_month":
                xpos 12
                ypos 4

            # Centre-anchored: a rotated render grows to the rotated
            # bounding box, so a top-left anchor would walk the pointer
            # off the dial as the angle changes.
            add _cal_hand:
                xpos 50
                ypos 49
                xanchor 0.5
                yanchor 0.5
                at cal_overlay_hand(_cal_angle)

            text _cal["day_padded"] style "cal_overlay_day":
                xpos 50
                xanchor 0.5
                ypos 49
                yanchor 0.5

            text _cal["dow_short"] style "cal_overlay_dow":
                xpos 132
                xanchor 0.5
                ypos 49
                yanchor 0.5
                color _cal_dow_color


# The animated "DATE SYNC" panel (shown by calendar_day_transition). Receives
# old/new snapshot dicts. The GLSL chrono-dial (cal_dial) sweeps its pointer +
# month-progress arc from the old day's angle to the new day's while the date
# (calendar_rotary_old/new) rolls old->new on the dial's round hub face; a tick
# fires on engage and on landing; auto-dismisses ~4s (or on dismiss). u_sweep
# fractions are derived here from each date's day-of-month.
screen calendar_day_change(old_date, new_date):
    modal True
    zorder 250

    add Solid("#000000cc")

    python:
        import calendar as _pycal
        _o = old_date["date"]
        _n = new_date["date"]
        _odim = _pycal.monthrange(_o.year, _o.month)[1]
        _ndim = _pycal.monthrange(_n.year, _n.month)[1]
        _f0 = (_o.day - 1) / float(max(_odim - 1, 1))
        _f1 = (_n.day - 1) / float(max(_ndim - 1, 1))
        if _f1 <= _f0:
            _f1 += 1.0                       # wound forward across a month/year seam
        _delta = (_n - _o).days
        _delta_label = "+{} DAY".format(_delta) if _delta == 1 else "+{} DAYS".format(_delta)
        _old_dow_color = "#e06b6b" if old_date["is_weekend"] else "#56d7ff"
        _new_dow_color = "#e06b6b" if new_date["is_weekend"] else "#56d7ff"

    frame:
        xalign 0.5
        yalign 0.5
        xysize (660, 500)
        background Solid("#00000000")
        padding (0, 0)
        at calendar_change_panel

        fixed:
            xysize (660, 500)

            # ---- corner brackets -------------------------------------------
            add Solid("#3f8ba1") xpos 12 ypos 12 xsize 22 ysize 2
            add Solid("#3f8ba1") xpos 12 ypos 12 xsize 2 ysize 22
            add Solid("#3f8ba1") xpos 626 ypos 12 xsize 22 ysize 2
            add Solid("#3f8ba1") xpos 646 ypos 12 xsize 2 ysize 22
            add Solid("#3f8ba1") xpos 12 ypos 486 xsize 22 ysize 2
            add Solid("#3f8ba1") xpos 12 ypos 466 xsize 2 ysize 22
            add Solid("#3f8ba1") xpos 626 ypos 486 xsize 22 ysize 2
            add Solid("#3f8ba1") xpos 646 ypos 466 xsize 2 ysize 22

            # ---- header ----------------------------------------------------
            add Solid("#56d7ff") xpos 22 ypos 19 xsize 4 ysize 20
            text "SYSTEM // DATE SYNC" style "cal_change_label":
                xpos 36
                ypos 21

            hbox:
                xpos 628
                xanchor 1.0
                ypos 23
                spacing 9
                text "0x4D" style "cal_change_tag":
                    yalign 0.5
                add Solid("#56d7ff") xsize 8 ysize 8 yalign 0.5 at cal_pip_blink

            add Solid("#ffffff14") xpos 26 ypos 52 xsize 608 ysize 1

            # ---- rotary gauge + date drum ----------------------------------
            # The dial (cal_dial) draws its own round hub the date reads on, so
            # no rectangular backing is needed. Bases are OPAQUE Solids: a fully
            # transparent Solid is culled before its shader can run.
            # The render box is larger than the 350px face so the glow can fade
            # out naturally instead of being cut off by a square edge.
            fixed:
                xysize (cal_dial_render_size, cal_dial_render_size)
                xpos 330
                xanchor 0.5
                ypos (56 - cal_dial_render_offset)

                add Solid("#000000") at cal_dial(_f0, _f1)

                fixed:
                    xysize (190, 140)
                    xalign 0.5
                    yalign 0.5

                    viewport:
                        xysize (190, 140)
                        draggable False
                        mousewheel False

                        fixed:
                            xysize (190, 140)

                            fixed:
                                xysize (190, 140)
                                at calendar_rotary_old

                                text old_date["month_short"] style "cal_change_month":
                                    xalign 0.5
                                    ypos 4
                                text old_date["day_padded"] style "cal_change_day":
                                    xalign 0.5
                                    ypos 34
                                text old_date["dow_short"] style "cal_change_dow":
                                    xalign 0.5
                                    ypos 104
                                    color _old_dow_color

                            fixed:
                                xysize (190, 140)
                                at calendar_rotary_new

                                text new_date["month_short"] style "cal_change_month":
                                    xalign 0.5
                                    ypos 4
                                text new_date["day_padded"] style "cal_change_day":
                                    xalign 0.5
                                    ypos 34
                                text new_date["dow_short"] style "cal_change_dow":
                                    xalign 0.5
                                    ypos 104
                                    color _new_dow_color

            # ---- old -> new readout ----------------------------------------
            hbox:
                xalign 0.5
                ypos 424
                spacing 16
                text old_date["persona"] style "cal_change_small_date":
                    yalign 0.5
                text ">" style "cal_change_small_arrow":
                    yalign 0.5
                text new_date["persona"] style "cal_change_small_date_new":
                    yalign 0.5

            frame:
                xalign 0.5
                ypos 458
                background Solid("#000000")
                padding (14, 5)
                text _delta_label style "cal_change_delta"

    timer 1 action Play("sound", audio.tick)
    timer 5 action Return()
    key "dismiss" action Return()

# Full month-grid menu (ShowMenu("calendar_menu"), wired in the game menu nav).
# Uses calendar_view for which month is displayed (resets to the real current
# month on show); highlights today, dims past days, tints weekends. Browsing
# months here never changes the actual in-game date.
screen calendar_menu():
    tag menu

    on "show" action Function(calendar_view.reset_to_current)
    on "replace" action Function(calendar_view.reset_to_current)

    use game_menu(_("Calendar"), current_screen="calendar_menu"):
        $ _cm_formatted = "{}, {} {}".format(calendar.get_day_name(), calendar.get_month_name(), calendar.get_day())
        $ _cm_year = calendar.get_year()
        $ _cm_month = calendar.get_month()
        $ _cm_dow = calendar.get_day_of_week()

        # NOTHING IN THIS SCREEN MAY CHANGE STATE. Ren'Py predicts screens on
        # idle frames, and prediction runs EVERY branch of an `if` whatever
        # the condition says. This screen used to carry
        #   if calendar_view.viewing_year is None:
        #       $ calendar_view.reset_to_current()
        # and prediction duly ran that reset over and over, so the browsed
        # month snapped back to today between clicks: the arrows could never
        # move past the month beside today, and stepping back from it landed
        # two months away. Measured Sep 20 2026 (the screen reported
        # predicting=True while the value it "saw as None" was 2025-5).
        # current_month() reads and falls back; it never writes.
        $ _cm_vy, _cm_vm = calendar_view.current_month()
        $ _cm_month_name = calendar.month_names[_cm_vm - 1]
        $ _cm_grid = get_calendar_grid(_cm_vy, _cm_vm)
        $ _cm_is_current_month = (_cm_vy == _cm_year and _cm_vm == _cm_month)

        fixed:
            xysize (836, 520)
            xalign 0.5
            yalign 0.5
            at cal_content_fade(0.0)

            vbox:
                xalign 0.5
                yalign 0.5
                spacing 16

                frame:
                    xysize (690, 58)
                    background ROOM_MENU_SELECTOR_SELECTED
                    padding (18, 0)

                    hbox:
                        yalign 0.5
                        spacing 14

                        text "TODAY" style "cal_menu_banner_label"
                        add Solid("#e8dbc54d"):
                            xsize 1
                            ysize 28
                            yalign 0.5
                        text _cm_formatted style "cal_menu_today"

                hbox:
                    spacing 14
                    xalign 0.5
                    yalign 0.5

                    textbutton "<":
                        style "cal_nav_button"
                        action Function(calendar_view.prev_month)
                        sensitive calendar_view.can_prev()

                    frame:
                        xysize (360, 48)
                        background ROOM_MENU_SELECTOR_IDLE
                        padding (0, 0)

                        text _cm_month_name style "cal_menu_month_label":
                            xalign 0.5
                            yalign 0.5

                    textbutton "Today":
                        style "cal_nav_today_button"
                        action Function(calendar_view.reset_to_current)
                        sensitive not _cm_is_current_month

                    textbutton ">":
                        style "cal_nav_button"
                        action Function(calendar_view.next_month)
                        sensitive calendar_view.can_next()

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
                                background (ROOM_MENU_SELECTOR_SELECTED if _hdr_active else ROOM_MENU_SELECTOR_IDLE)
                                padding (0, 0)

                                text _dow style "cal_day_header":
                                    xalign 0.5
                                    yalign 0.5
                                    if _hdr_active:
                                        color ROOM_MENU_INK
                                    elif _hdr_wkend:
                                        color ROOM_MENU_CORAL

                    # A month grid is 4, 5 or 6 weeks tall, and this block is
                    # centred, so letting it size itself moved the whole
                    # panel -- arrows included -- by half a row whenever the
                    # month changed. The arrow then slid out from under the
                    # pointer and the next click landed on nothing, which is
                    # what made months appear to skip. Always reserve six.
                    fixed:
                        xysize (544, 298)

                        vbox:
                            spacing 2

                            for _week in _cm_grid:
                                hbox:
                                    spacing 2

                                    for _wi, _wd in enumerate(_week):
                                        if _wd == 0:
                                            frame:
                                                style "cal_cell_empty"

                                        else:
                                            $ _state = calendar_cell_state(_cm_vy, _cm_vm, _wd)
                                            $ _is_wkend = _wi >= 5

                                            if _state == "today":
                                                frame:
                                                    style "cal_cell_today"
                                                    text "[_wd]" style "cal_cell_today_text"

                                            else:
                                                frame:
                                                    style ("cal_cell_outside" if _state == "outside" else "cal_cell")
                                                    text "[_wd]" style "cal_cell_text":
                                                        color calendar_cell_color(_state, _is_wkend)


# =============================================================================
# STYLES  -- story overlays retain their authored palette. The month-grid menu
# below joins the quiet room family with teal, coral, ochre, and paper tones.
# =============================================================================
# Dark ink: the month sits ON the accent strip, not on the dark page.
style cal_overlay_month:
    font gui.interface_font
    size 13
    color "#05121b"
    kerning 2.2
    outlines []

# Sized to sit inside the dial ring.
#
# The yoffsets are optical centring, and they are MEASURED, not guessed: a
# text's box is its full line box (ascent + descent) grown by the outline,
# but digits and caps only ink the upper part of it, so centring the box
# leaves the glyphs riding 5px high on the dial and the divider. Re-measure
# these two if the font, the size or the outline changes.
style cal_overlay_day:
    font gui.name_font
    size 26
    color "#ffffff"
    outlines [(2, "#000000", 0, 0)]
    yoffset 5

style cal_overlay_dow:
    font gui.name_font
    size 20
    color "#72b8d4"
    outlines [(1, "#000000", 0, 0)]
    yoffset 5

style cal_change_label:
    font gui.interface_font
    size 15
    color "#7fb4c9"
    kerning 2.0
    bold True
    outlines []

style cal_change_tag:
    font gui.interface_font
    size 13
    color "#83aebe"
    kerning 1.0
    outlines []

style cal_change_month:
    font gui.interface_font
    size 22
    color "#c4edf8"
    kerning 4.0
    outlines [(1, "#02060a", 0, 0)]

style cal_change_day:
    font gui.name_font
    size 56
    color "#f7fdff"
    outlines [(3, "#02060a", 0, 0), (1, "#56d7ff66", 0, 0)]

style cal_change_dow:
    font gui.name_font
    size 24
    color "#56d7ff"
    kerning 2.0
    outlines [(2, "#02060a", 0, 0)]

style cal_change_small_date:
    font gui.interface_font
    size 17
    color "#91adba"
    kerning 1.0
    outlines []

style cal_change_small_date_new:
    font gui.interface_font
    size 18
    color "#cfe9f3"
    kerning 1.0
    outlines [(1, "#02060a", 0, 0)]

style cal_change_small_arrow:
    font gui.name_font
    size 20
    color "#56d7ff"
    outlines []

style cal_change_delta:
    font gui.interface_font
    size 14
    color "#56d7ff"
    kerning 2.0
    bold True
    outlines []

style cal_menu_banner_label:
    font gui.interface_font
    size 14
    color ROOM_MENU_OCHRE
    kerning 1.2
    outlines [(1, "#05090d99", 0, 1)]
    yalign 0.5

style cal_menu_today:
    font gui.default_font
    size 20
    color ROOM_MENU_INK
    outlines [(1, "#05090db8", 0, 1)]
    yalign 0.5

style cal_menu_month_label:
    font gui.default_font
    size 24
    color ROOM_MENU_INK
    outlines [(2, "#05090db8", 0, 1)]

style cal_nav_button:
    xysize (48, 48)
    background ROOM_MENU_SELECTOR_IDLE
    hover_background ROOM_MENU_SELECTOR_HOVER
    # At either end of the story's months the arrow is dead, and has to look
    # it -- otherwise the calendar just stops responding.
    insensitive_background Solid("#0b1418c4")
    padding (0, 0)
    yalign 0.5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style cal_nav_button_text:
    font gui.default_font
    size 22
    color ROOM_MENU_PAPER
    hover_color "#fff8ea"
    insensitive_color "#4f5c5a"
    xalign 0.5
    yalign 0.5
    outlines [(1, "#05090db8", 0, 1)]

style cal_nav_today_button:
    xysize (94, 48)
    background ROOM_MENU_SELECTOR_IDLE
    hover_background ROOM_MENU_SELECTOR_HOVER
    insensitive_background ROOM_MENU_SELECTOR_SELECTED
    padding (0, 0)
    yalign 0.5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style cal_nav_today_button_text:
    font gui.interface_font
    size 15
    color ROOM_MENU_PAPER
    hover_color "#fff8ea"
    insensitive_color ROOM_MENU_INK
    xalign 0.5
    yalign 0.5
    outlines [(1, "#05090db8", 0, 1)]

style cal_day_header:
    font gui.interface_font
    size 13
    color ROOM_MENU_MUTED
    text_align 0.5
    outlines [(1, "#05090d99", 0, 1)]

style cal_cell:
    xysize (76, 48)
    background ROOM_MENU_SELECTOR_IDLE
    padding (0, 0)

style cal_cell_empty:
    xysize (76, 48)
    background Solid("#0711168f")
    padding (0, 0)

# A real day the story never reaches: before it opens, or after it ends.
style cal_cell_outside:
    xysize (76, 48)
    background Solid("#0b1418c4")
    padding (0, 0)

style cal_cell_text:
    font gui.interface_font
    size 20
    color ROOM_MENU_PAPER
    xalign 0.5
    yalign 0.5
    text_align 0.5
    outlines [(1, "#05090d99", 0, 1)]

style cal_cell_today:
    xysize (76, 48)
    background ROOM_MENU_SELECTOR_SELECTED
    padding (0, 0)

style cal_cell_today_text:
    font gui.default_font
    size 21
    color ROOM_MENU_INK
    xalign 0.5
    yalign 0.5
    text_align 0.5
    outlines [(2, "#05090db8", 0, 1)]
