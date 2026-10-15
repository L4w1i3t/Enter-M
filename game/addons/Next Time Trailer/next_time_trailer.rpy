# Chapter 0.5's closing "Next time" trailer: one minute of overheard lines and
# moving pictures, cut to scamall. 0531.rpy calls enter_m_prologue_trailer once,
# after the month turns. enter_m_prologue_trailer_skip (Esc, Space, Enter, the
# SKIP button) cuts it short. Both exits hand back a black frame with
# quick_menu restored, the music stopped and no trailer screen left showing.
#
# THE CLOCK. Every cut waits on scamall's own playback position
# (enter_m_tr_at), so a slow decode costs one late frame, never a drift. Muted
# audio falls back to the wall clock. A save loaded mid-trailer restarts the
# cue at zero; the two clocks then disagree and each shot holds its nominal
# length instead of stalling.
#
# THE CUE (scamall.ogg, 75 BPM: 0.8 s beats, 3.2 s bars; onsets measured Oct 14
# 2026 from the file): bars 0-6 a quiet pad; bar 7 a riser whose crash lands
# at 25.50 s; bars 8-14 the full band in two-bar phrases, each with a breath on
# the fourth beat of its first bar; bar 15 the brightest hits (48.8 and 50.0 s),
# then silence from 50.40 s; the drop, a lighter groove, is bar 16 at 51.20 s.
#
# THE CUT LIST (seconds of music; edit a mark here and in the label together)
#    0.0  THEATER    the dark house, the blank screen; up from black
#    3.2  WATCHER    MC lit by the screen; the room slides back (a dolly zoom)
#    6.4  CUP        a paper cup on a bench, pulled into focus      line 1
#    9.6  STREET     headlights; Matsuda backs into frame; the focus
#                    racks past her to Tsubaki                       line 2
#   14.4  BUS        Monika by the window, the road running behind
#   19.2  TRACK      the lane, gathering speed; MC goes by at its edge
#   22.4  RISER      whip-ins on the beat, then the half-beat: Matsuda,
#                    the arcade, the library, Sam, the kitchen, Monika
#   25.5  TABLE      the crash on six lunches; Tsubaki comes in        line 3
#   32.0  SIX        all six on the roof, tracked past in two depths
#   38.4  HOME       MC sharp, Asahina soft at the edge, then the turn line 4
#   41.6  MONTAGE    the race, the beach, the umbrellas, the club room
#   44.8  CLUB       Monika listening; the push lands as the line ends line 5
#   48.0  DOOR       a climb, rushing up to the doorway                line 6
#   50.4  BREAK      the silence: past the door, the traveler, his back to
#                    us in the static, looking round; line 6 holds
#   51.2  DROP       pull back to the whole key art; the title
#   54.4  NEXT       "Next time: Chapter 1, Room for Six"
#   56.8  OUT        fade and music fadeout; control returns at about 59.4 s
#
# THE WORDS. Six lines, every one already said or written in Chapter 0.5 and
# heard on every route, so the trailer makes no new promises:
#   1 "They spelled my name wrong."            Matsuda, 0531
#   2 "You can just say friend."               Tsubaki, 0517
#   3 "You can sit if you want."               MC, 0521
#   4 "Hey, I listen sometimes."               Asahina, 0515
#   5 "I'm giving the place time to exist."    MC, 0530
#   6 Does the traveler go inside?             Monika's green ink, 0530
# Spoken lines are quoted and nobody is named. Each plays over the scene it
# came from, usually on the face it was said to; a rack focus or a landing
# push hands it to its speaker only where the shot wants that.
#
# RULES THIS FILE KEEPS
#   * Withhold the shape: no chapter cards, no months, no season graded to a
#     mood. Every shot wears the same hollow grade, and the year's order is
#     scrambled.
#   * Every shot sits on an ink plate, so nothing transparent ever shows (the
#     developer build tiles a checkerboard behind transparency).
#   * Nothing here depends on the OP folder, which does not ship. The key art
#     is a copy in this folder.
#   * Chapter CGs appear only as partial crops, so the gallery's seen-means-
#     unlocked rule stays honest. A full-frame chapter CG needs cg_unlock().
#   * Effects are whole-frame or ride a whole layer (grades, pushes, blur,
#     light bands crossing the frame, the signal layer). Nothing is pinned to a
#     spot inside a background.
#   * The prose guide's locked vocabulary for this trailer ("mystique, not
#     angelic"; "ethereal, not cosmic"; broadcast decay, a signal that can
#     barely hold) lives in the frame and the signal layer: grain throughout,
#     bands and a hum bar riding the riser and the band (the music, never the
#     story), gone in the silence, a light grain under the title. Type always
#     sits above the decay.
#   * Photosensitive Mode takes the light and keeps the picture: flashes become
#     a low, slow swell, screen flicker holds still, light bands dim and slow,
#     and the riser's fast cuts become short dissolves.
#   * No spoilers: no silhouettes; the six appear together once, on everyday
#     faces, Tsubaki among them; Sam on his pleasant baseline, always whole in
#     frame; neither Kotonoha nor Himeko on screen; nothing from the
#     dependency route.
#   * Pixel positions in ATL are ints. A float position is a fraction of the
#     screen, so 1840.0 sends a picture 1840 screens away.


# -----------------------------------------------------------------------------
# 1. CONSTANTS AND STATE
# -----------------------------------------------------------------------------

define enter_m_tr_bpm = 75.0
define enter_m_tr_beat = 60.0 / enter_m_tr_bpm        # 0.80 s
define enter_m_tr_bar = enter_m_tr_beat * 4.0         # 3.20 s

# Measured onsets (see the header). The crash leads bar 8 by a tenth.
define enter_m_tr_hit = 25.5
define enter_m_tr_break = enter_m_tr_bar * 15.75      # 50.40 s
define enter_m_tr_drop = enter_m_tr_bar * 16.0        # 51.20 s

define ENTER_M_TR_DIR = "addons/Next Time Trailer/"
define ENTER_M_TR_INK = "#04070a"
define ENTER_M_TR_TEAL = "#79e6d2"

# The one grade every shot wears, so no season reads warmer than another.
define ENTER_M_TR_HOLLOW = TintMatrix("#d8e3e6") * SaturationMatrix(0.78)
# A room behind a face, held back so the face carries the frame.
define ENTER_M_TR_DIM = TintMatrix("#8f9aa1") * SaturationMatrix(0.55)
# The table again, far back, under the Next card.
define ENTER_M_TR_DEEP = TintMatrix("#5a6469") * SaturationMatrix(0.35)

# The chapter art, reached by name so a crop reads as what it is.
image enter_m_tr_cg1 = "assets/cg/chapter_select/chapter_1_room_for_six.png"
image enter_m_tr_cg2 = "assets/cg/chapter_select/chapter_2_summer_uncontained.png"
image enter_m_tr_cg3 = "assets/cg/chapter_select/chapter_3_between_bells.png"
image enter_m_tr_cg5 = "assets/cg/chapter_select/chapter_5_somewhere_warm.png"
image enter_m_tr_keyart = "addons/Next Time Trailer/titledropalt.png"

# quick_menu as the caller left it; the last mark the clock reached.
default enter_m_tr_prev_quick_menu = True
default enter_m_tr_mark = 0.0


# -----------------------------------------------------------------------------
# 2. CLOCK, CLEANUP, WARM-UP
# -----------------------------------------------------------------------------

init python:
    import time as _enter_m_tr_time
    import threading as _enter_m_tr_threading

    # Every screen either exit must take down.
    ENTER_M_TR_SCREENS = (
        "enter_m_tr_frame",
        "enter_m_tr_signal",
        "enter_m_tr_line",
        "enter_m_tr_note",
        "enter_m_tr_flash",
        "enter_m_tr_title",
        "enter_m_tr_next",
        "enter_m_prologue_trailer_skip",
    )

    def enter_m_tr_cleanup():
        # Immediately: a skip during the title must not leave its hide
        # animation playing over whatever the caller shows next.
        for name in ENTER_M_TR_SCREENS:
            try:
                renpy.hide_screen(name, immediately=True)
            except Exception:
                pass

    # Session-only on purpose: a loaded save must not trust an old start time.
    _ENTER_M_TR_CLOCK = {"t0": None}

    def enter_m_tr_clock_start():
        _ENTER_M_TR_CLOCK["t0"] = _enter_m_tr_time.time()
        store.enter_m_tr_mark = 0.0

    def _enter_m_tr_now():
        """Seconds of scamall heard so far, or None if no clock can be trusted."""
        t0 = _ENTER_M_TR_CLOCK["t0"]
        if t0 is None:
            return None
        wall = _enter_m_tr_time.time() - t0
        pos = renpy.music.get_pos("music")
        if pos is None:
            # Muted, or no audio device: the wall clock is the cue's clock.
            return wall
        if abs(pos - wall) < 0.5:
            return pos
        return None

    def enter_m_tr_t(bar, beat=0.0):
        """A mark on the cue's grid: `bar` bars plus `beat` beats, in seconds."""
        return bar * enter_m_tr_bar + beat * enter_m_tr_beat

    def enter_m_tr_at(mark):
        """Hold the current shot until `mark` seconds into the cue."""
        last = store.enter_m_tr_mark
        store.enter_m_tr_mark = mark
        now = _enter_m_tr_now()
        delay = (mark - last) if now is None else (mark - now)
        if delay > 0.0:
            renpy.pause(delay, hard=True)

    def enter_m_tr_cut():
        """The riser's cut: hard, or a short dissolve in Photosensitive Mode."""
        return Dissolve(0.22) if enter_m_photosensitive() else None

    # Shots animate every frame, so Ren'Py's own predictor never gets an idle
    # frame during the trailer. Decode its art up front on a daemon thread
    # instead (the same pattern as msbf_px_warm_fight_art).
    _ENTER_M_TR_WARM = {"busy": False}

    def _enter_m_tr_images(d, seen, out, depth=0):
        if d is None or depth > 16 or id(d) in seen:
            return
        seen.add(id(d))
        if isinstance(d, renpy.display.im.ImageBase):
            out.append(d)
            return
        try:
            children = d.visit() or ()
        except Exception:
            children = ()
        for child in children:
            _enter_m_tr_images(child, seen, out, depth + 1)

    def _enter_m_tr_warm_worker(images):
        try:
            for im in images:
                try:
                    renpy.display.im.cache.get(im, predict=True, texture=True)
                except Exception:
                    pass
        finally:
            _ENTER_M_TR_WARM["busy"] = False

    def enter_m_tr_warm(names):
        if _ENTER_M_TR_WARM["busy"]:
            return
        seen = set()
        images = []
        for name in names:
            try:
                _enter_m_tr_images(renpy.displayable(name), seen, images)
            except Exception:
                pass
        if not images:
            return
        _ENTER_M_TR_WARM["busy"] = True
        _enter_m_tr_threading.Thread(
            target=_enter_m_tr_warm_worker, args=(images,), daemon=True).start()

    # In order of first use, so the early shots are ready first.
    ENTER_M_TR_WARM_LIST = (
        "bg theater_inside", "mc neut", "enter_m_tr_cg5", "bg residential_night",
        "tsubaki casual unamused", "matsuda casual pose_chuuni",
        "bg bus_interior", "monika forward uniform dist cm oe nobl rdown ldown",
        "bg track_evening", "bg corridor", "matsuda uniform pose_laughing",
        "bg arcade", "tsubaki uniform determined", "asahina uniform happy",
        "bg library", "bg living_room_night", "sam casual happy",
        "bg kitchen_night", "bg club_day", "monika forward uniform happ",
        "enter_m_tr_cg1", "tsubaki uniform nervous", "tsubaki uniform happy",
        "bg rooftop", "sam uniform happy", "mc happy", "asahina uniform teasing",
        "asahina casual smug", "matsuda uniform smug", "enter_m_tr_cg2",
        "enter_m_tr_cg3", "monika forward uniform curi om oe nobl rdown ldown",
        "monika forward uniform happ cm ce nobl rdown ldown", "bg rooftop_door",
        "enter_m_tr_keyart",
    )


# -----------------------------------------------------------------------------
# 3. THE CAST, FRAMED
# -----------------------------------------------------------------------------
# Close-ups are built from each layered image's own layer stack, scaled from
# the master art and flattened at the final size. The registered images
# flatten at 640x960 first, so zooming one upscales that texture: measured on
# the same face at x1.6, the stack route is a quarter sharper, same color.

init python:

    # Where each face sits in its REGISTERED image (pixels, 960 tall): the
    # point between the irises, and how large the face is drawn against the
    # reference cast. Monika's DDLC plate draws hers 1.25x larger (pupil
    # distance about 88px against 69 for MC). Measured on renders Oct 14 2026.
    ENTER_M_TR_FACE = {
        "mc": (320.0, 168.0, 1.0),
        "matsuda": (294.0, 221.0, 1.0),
        "tsubaki": (317.0, 238.0, 1.0),
        "asahina": (299.0, 198.0, 1.0),
        "sam": (301.0, 177.0, 1.0),
        "monika": (477.0, 284.0, 1.25),
    }

    # Pose images are their own canvases, so their eyes sit elsewhere.
    # Measured on renders Oct 14 2026.
    ENTER_M_TR_POSE_FACE = {
        "matsuda casual pose_chuuni": (287.0, 220.0, 1.0),
        "matsuda uniform pose_laughing": (363.0, 213.0, 1.0),
    }

    # The box each registered image is fitted into (Monika's is square).
    ENTER_M_TR_BOX = {"monika": (960, 960)}

    _ENTER_M_TR_CAST = {}

    def _enter_m_tr_stack(d, depth=0):
        """The first Fixed under a layered image: the layer stack itself."""
        if d is None or depth > 8:
            return None
        if isinstance(d, renpy.display.layout.MultiBox):
            return d
        try:
            children = d.visit() or ()
        except Exception:
            return None
        for child in children:
            found = _enter_m_tr_stack(child, depth + 1)
            if found is not None:
                return found
        return None

    def enter_m_tr_cast(name, zoom):
        """`name` (with attributes) at `zoom` of its registered size, crisp."""
        key = (name, zoom)
        rv = _ENTER_M_TR_CAST.get(key)
        if rv is None:
            bw, bh = ENTER_M_TR_BOX.get(name.split()[0], (640, 960))
            rv = Transform(name, zoom=zoom)
            try:
                stack = _enter_m_tr_stack(renpy.displayable(name))
                if stack is not None:
                    rv = Flatten(Transform(stack, fit="contain",
                        xysize=(int(bw * zoom + 0.5), int(bh * zoom + 0.5))))
            except Exception:
                pass
            _ENTER_M_TR_CAST[key] = rv
        return rv

    def enter_m_tr_face(name, zoom, x, y):
        """A figure whose eyes land at (x, y) of whatever holds it. The body
        hangs below, past the letterbox, so the sprite's lower edge never shows."""
        ex, ey, scale = ENTER_M_TR_POSE_FACE.get(name) or \
            ENTER_M_TR_FACE.get(name.split()[0], (320.0, 200.0, 1.0))
        z = zoom / scale
        return Transform(enter_m_tr_cast(name, z), xanchor=0, yanchor=0,
            xpos=int(x - ex * z), ypos=int(y - ey * z))


# -----------------------------------------------------------------------------
# 4. THE SHOTS
# -----------------------------------------------------------------------------
# Each shot is one picture: a plate, the people in it and its light, every
# layer with its own motion, built when the shot is cut to. The label shows it
# on an ink plate and puts the camera (grade, push, whip) on the whole.

init python:

    def enter_m_tr_plate(name, zoom=1.0, ax=0.5, ay=0.5, sx=None, sy=None, blur=0.0, margin=0):
        """A picture filling the shot at `zoom`: its point (ax, ay) held at
        screen (sx, sy), or where it already is. The hold is clamped so the
        picture always covers the frame plus `margin` pixels a side."""
        sx = ax if sx is None else sx
        sy = ay if sy is None else sy
        mx = float(margin) / 1280.0
        my = float(margin) / 720.0
        sx = min(max(sx, 1.0 - (1.0 - ax) * zoom + mx), ax * zoom - mx)
        sy = min(max(sy, 1.0 - (1.0 - ay) * zoom + my), ay * zoom - my)
        kw = {"blur": blur} if blur else {}
        return Transform(name, zoom=zoom, xanchor=ax, yanchor=ay, xpos=sx, ypos=sy, **kw)

    def enter_m_tr_lit():
        """A screen's light on a face: a flicker, or a still light in
        Photosensitive Mode."""
        return enter_m_tr_still if enter_m_photosensitive() else enter_m_tr_flicker

    def enter_m_tr_gleam(w=280):
        """A soft vertical band of light, for headlights and glare."""
        band = Transform(ENTER_M_TR_DIR + "band.png", xysize=(720, w), rotate=90, rotate_pad=False)
        return AlphaMask(Solid("#ffffff", xysize=(w, 720)), band)

    def enter_m_tr_sweep_of(x0, x1, delay, t, peak):
        """A light band crossing the frame; dimmer and slower in
        Photosensitive Mode."""
        if enter_m_photosensitive():
            peak, t = peak * 0.35, t * 2.0
        return At(enter_m_tr_gleam(), enter_m_tr_sweep(x0, x1, delay, t, peak))

    def enter_m_tr_shot(*layers):
        return Fixed(*layers, xysize=(1280, 720))

    # A layer's own placement survives only under transforms that set none,
    # so inner layers take offsets, zoom-only, blur, alpha and color; the
    # pushes that frame a whole shot go on the shot, in the label.

    # 3.2 WATCHER: MC in the seats, the screen's light on him. The camera
    # pushes in on him (label) while the room behind slides back faster than
    # he grows: a dolly zoom, so the house goes slightly wrong.
    def enter_m_tr_s_watcher():
        room = At(enter_m_tr_plate("bg theater_inside", 1.6, 0.5, 0.42, blur=9.0),
            enter_m_tr_zoom(1.0, 0.8, 3.4), enter_m_tr_grade(ENTER_M_TR_DIM))
        him = At(enter_m_tr_face("mc neut", 1.75, 430, 300), enter_m_tr_lit()())
        return enter_m_tr_shot(room, him)

    # 6.4 CUP: the paper cup somebody left, pulled into focus.
    def enter_m_tr_s_cup():
        cup = At(enter_m_tr_plate("enter_m_tr_cg5", 2.35, 0.27, 0.70, 0.5, 0.5),
            enter_m_tr_focus(7.0, 0.0, 0.35, 0.7))
        return enter_m_tr_shot(cup)

    # 9.6 STREET: the vending machine, headlights going past, then Matsuda backs
    # into frame mid-performance. The focus racks past her to Tsubaki for the
    # line: it was Tsubaki's.
    def enter_m_tr_s_street():
        street = At(enter_m_tr_plate("bg residential_night", 1.18, 0.22, 0.56, margin=40),
            enter_m_tr_drift(-34, 0, 4.9))
        tsubaki = At(enter_m_tr_face("tsubaki casual unamused", 0.62, 300, 330),
            enter_m_tr_drift(-20, 0, 4.9), enter_m_tr_focus(3.5, 0.0, 2.35, 0.5))
        matsuda = At(enter_m_tr_face("matsuda casual pose_chuuni", 1.2, 950, 250),
            enter_m_tr_enter(560, 0.6, 0.8, -26, 3.6), enter_m_tr_focus(0.0, 4.0, 2.35, 0.5))
        lights = enter_m_tr_sweep_of(1500, -420, 0.2, 1.1, 0.22)
        return enter_m_tr_shot(street, tsubaki, matsuda, lights)

    # 14.4 BUS: Monika with nobody to be bright at; the road runs out behind
    # her and the trees' shadows cross her face.
    def enter_m_tr_s_bus():
        road = At(enter_m_tr_plate("bg bus_interior", 1.2, 0.525, 0.44, blur=4.5),
            enter_m_tr_zoom(1.0, 1.22, 4.9))
        her = At(enter_m_tr_face("monika forward uniform dist cm oe nobl rdown ldown", 1.3, 860, 270),
            enter_m_tr_bob(2.0, 1.1), enter_m_tr_lit()(0.1))
        return enter_m_tr_shot(road, her)

    # 19.2 TRACK: down the lane, faster and softer into the riser. MC at the
    # lane's edge is nearer than the track, so he goes by faster than it does.
    def enter_m_tr_s_track():
        lane = At(enter_m_tr_plate("bg track_evening", 1.45, 0.4, 0.62, margin=260),
            enter_m_tr_run(250, -250, 3.3))
        him = At(enter_m_tr_face("mc determined", 0.95, 900, 300),
            enter_m_tr_run(260, -560, 3.3))
        return enter_m_tr_shot(lane, him)

    # 22.4 RISER, one per beat and then per half-beat. The first keeps the
    # lane's direction: everything still travels right to left.
    def enter_m_tr_s_bard():
        hall = enter_m_tr_plate("bg corridor", 1.2, 0.5, 0.5, blur=2.0)
        her = At(enter_m_tr_face("matsuda uniform pose_laughing", 1.15, 640, 250),
            enter_m_tr_enter(640, 0.0, 0.3, -14, 0.6))
        return enter_m_tr_shot(hall, her)

    def enter_m_tr_s_arcade_gun():
        floor = enter_m_tr_plate("bg arcade", 1.4, 0.62, 0.5, blur=4.0)
        asahina = At(enter_m_tr_face("asahina uniform happy", 1.0, 920, 300), enter_m_tr_lit()(0.12))
        tsubaki = At(enter_m_tr_face("tsubaki uniform determined", 1.3, 400, 270), enter_m_tr_lit()(0.12))
        return enter_m_tr_shot(floor, asahina, tsubaki)

    def enter_m_tr_s_notes():
        return enter_m_tr_shot(enter_m_tr_plate("bg library", 1.6, 0.40, 0.60, 0.5, 0.5))

    def enter_m_tr_s_sam():
        room = enter_m_tr_plate("bg living_room_night", 1.2, 0.5, 0.5, blur=4.0)
        return enter_m_tr_shot(room, enter_m_tr_face("sam casual happy", 1.3, 760, 260))

    def enter_m_tr_s_kitchen():
        return enter_m_tr_shot(enter_m_tr_plate("bg kitchen_night", 1.35, 0.62, 0.55, 0.5, 0.5))

    def enter_m_tr_s_club_glimpse():
        room = enter_m_tr_plate("bg club_day", 1.2, 0.5, 0.5, blur=3.0)
        return enter_m_tr_shot(room, enter_m_tr_face("monika forward uniform happ", 1.25, 820, 260))

    # 25.5 TABLE: the crash on six lunches. Tsubaki comes in from the left,
    # stops short, hears the line, and her face turns before she sits.
    def enter_m_tr_s_table():
        lunches = enter_m_tr_plate("enter_m_tr_cg1", 1.45, 0.66, 0.66, 0.6, 0.5)
        unsure = At(enter_m_tr_face("tsubaki uniform nervous", 1.15, 330, 270), enter_m_tr_fade(1.0, 0.0, 4.1, 0.3))
        glad = At(enter_m_tr_face("tsubaki uniform happy", 1.15, 330, 270), enter_m_tr_fade(0.0, 1.0, 4.1, 0.3))
        her = At(Fixed(unsure, glad, xysize=(1280, 720)),
            enter_m_tr_enter(-720, 1.5, 0.8, 0, 0.1), enter_m_tr_sit(70, 4.9, 0.6))
        return enter_m_tr_shot(lunches, her)

    # 32.0 SIX: the six on the roof in two depths, the camera tracking past
    # them. The far row moves slower than the near one. Nobody is singled out,
    # and every face is an everyday one.
    def enter_m_tr_s_six():
        roof = At(enter_m_tr_plate("bg rooftop", 1.3, 0.5, 0.5, blur=1.5, margin=70),
            enter_m_tr_drift(-60, 0, 6.6))
        far = At(Fixed(
            enter_m_tr_face("sam uniform happy", 0.66, 380, 300),
            enter_m_tr_face("monika forward uniform happ", 0.66, 770, 292),
            enter_m_tr_face("mc happy", 0.66, 1170, 300),
            xysize=(1280, 720)), enter_m_tr_drift(-150, 0, 6.6), enter_m_tr_focus(1.2, 1.2, 0.0, 0.1))
        near = At(Fixed(
            enter_m_tr_face("asahina uniform teasing", 0.98, 250, 335),
            enter_m_tr_face("tsubaki uniform happy", 0.98, 620, 345),
            enter_m_tr_face("matsuda uniform pose_laughing", 0.98, 1010, 330),
            xysize=(1280, 720)), enter_m_tr_drift(-280, 0, 6.6))
        glare = enter_m_tr_sweep_of(-400, 1500, 2.4, 1.6, 0.16)
        return enter_m_tr_shot(roof, far, near, glare)

    # 38.4 HOME: MC sharp; his sister soft at the edge of frame. The focus goes
    # to her as her line ends.
    def enter_m_tr_s_home():
        room = enter_m_tr_plate("bg living_room_night", 1.15, 0.5, 0.5, blur=3.0)
        him = At(enter_m_tr_face("mc neut", 1.3, 800, 280), enter_m_tr_focus(0.0, 4.0, 2.0, 0.5))
        her = At(enter_m_tr_face("asahina casual smug", 2.2, 130, 300), enter_m_tr_focus(6.0, 0.0, 2.0, 0.5))
        return enter_m_tr_shot(room, him, her)

    # 41.6 MONTAGE, one per beat.
    def enter_m_tr_s_race():
        cabinets = enter_m_tr_plate("bg arcade", 1.35, 0.12, 0.47, 0.5, 0.5, blur=3.0)
        mc = At(enter_m_tr_face("mc happy", 1.2, 410, 290), enter_m_tr_lit()(0.12))
        matsuda = At(enter_m_tr_face("matsuda uniform smug", 1.2, 880, 280), enter_m_tr_lit()(0.12))
        return enter_m_tr_shot(cabinets, mc, matsuda)

    def enter_m_tr_s_beach():
        return enter_m_tr_shot(enter_m_tr_plate("enter_m_tr_cg2", 1.55, 0.42, 0.66, 0.5, 0.5))

    def enter_m_tr_s_umbrellas():
        return enter_m_tr_shot(enter_m_tr_plate("enter_m_tr_cg3", 1.45, 0.40, 0.55, 0.5, 0.5))

    def enter_m_tr_s_club_wide():
        return enter_m_tr_shot(enter_m_tr_plate("bg club_day", 1.05, 0.5, 0.5))

    # 44.8 CLUB: Monika asked what he's stuck on; she listens to the answer, and
    # her face turns on the breath after it.
    def enter_m_tr_s_club():
        room = enter_m_tr_plate("bg club_day", 1.2, 0.6, 0.45, blur=2.5)
        asking = At(enter_m_tr_face("monika forward uniform curi om oe nobl rdown ldown", 1.35, 430, 280),
            enter_m_tr_fade(1.0, 0.0, 2.4, 0.25))
        amused = At(enter_m_tr_face("monika forward uniform happ cm ce nobl rdown ldown", 1.35, 430, 280),
            enter_m_tr_fade(0.0, 1.0, 2.4, 0.25))
        return enter_m_tr_shot(room, asking, amused)


# -----------------------------------------------------------------------------
# 5. STYLES
# -----------------------------------------------------------------------------

style enter_m_tr_text is default:
    outlines []

style enter_m_tr_bug is enter_m_tr_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 15
    kerning 4.0
    color "#79e6d2"

style enter_m_tr_kicker is enter_m_tr_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 19
    kerning 6.0
    color "#79e6d2"
    outlines [(1, "#04070a", 0, 1)]

style enter_m_tr_card_title is enter_m_tr_text:
    font "assets/fonts/SF Automaton Extended.ttf"
    size 70
    kerning 1.0
    color "#f6fbf9"
    outlines [(3, "#04070a", 0, 3)]

style enter_m_tr_span is enter_m_tr_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 17
    kerning 3.0
    color "#c3d2cd"
    outlines [(1, "#04070a", 0, 1)]

style enter_m_tr_say is enter_m_tr_text:
    font "assets/fonts/Myanmar.otf"
    size 31
    color "#f3f8f6"
    outlines [(2, "#04070ad8", 0, 1)]
    text_align 0.5

# Written, not spoken: the dialogue face in the italic the story uses for notes,
# in Monika's green ink.
style enter_m_tr_note is enter_m_tr_text:
    font "assets/fonts/Myanmar.otf"
    size 36
    italic True
    color "#9fd3a8"
    outlines [(2, "#04070ad0", 0, 1)]
    text_align 0.5

style enter_m_tr_wordmark is enter_m_tr_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 96
    kerning 2.0
    color "#ffffff"

style enter_m_tr_next_kicker is enter_m_tr_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 28
    kerning 10.0
    color "#79e6d2"

style enter_m_tr_skip_button is default:
    background Solid("#04070ab8")
    hover_background Solid("#79e6d24d")
    xpadding 16
    ypadding 7

style enter_m_tr_skip_button_text is enter_m_tr_text:
    font "assets/fonts/NovaSquare-Regular.ttf"
    size 15
    kerning 3.0
    color "#cfe9e3"
    hover_color "#ffffff"


# -----------------------------------------------------------------------------
# 6. TRANSFORMS
# -----------------------------------------------------------------------------
# Ren'Py's warper names run opposite to CSS: easein decelerates into place,
# easeout accelerates away. Pixel arguments are ints.

# Camera: hold one point of the picture still while the zoom moves through it.
# The point stays where it already is on screen, unless (sx, sy) moves it
# there instead (the traveler, held at center in the silence).
transform enter_m_tr_push(z0=1.0, z1=1.08, t=3.2, x=0.5, y=0.5, sx=None, sy=None):
    subpixel True
    xpos (x if sx is None else sx)
    ypos (y if sy is None else sy)
    xanchor x
    yanchor y
    zoom z0
    linear t zoom z1

# Camera: lands big and settles, then keeps creeping.
transform enter_m_tr_slam(z0=1.25, z1=1.0, t=0.5, x=0.5, y=0.5, creep=0.04, hold=3.0):
    subpixel True
    xpos x
    ypos y
    xanchor x
    yanchor y
    zoom z0
    easein t zoom z1
    linear hold zoom (z1 + creep)

# Camera: up the stairs at a run, the doorway rushing up to meet the climax.
# The cut to black comes before anything past the door is seen.
transform enter_m_tr_climb(t1=1.2, t2=1.25):
    subpixel True
    xpos 0.53
    ypos 0.42
    xanchor 0.53
    yanchor 0.42
    zoom 1.04
    linear t1 zoom 1.45
    easeout t2 zoom 2.3

# Camera: the drop. Off the traveler (the key art at x2.4 on his shoulders)
# and back to the whole picture, then a slow creep under the title. Zoom and
# position share one warper, so the frame stays covered the whole way.
transform enter_m_tr_reveal(z0=2.4, x=0.32, y=0.32, t=0.7):
    subpixel True
    xanchor x
    yanchor y
    xpos 0.5
    ypos 0.5
    zoom z0
    easein t xpos x ypos y zoom 1.0
    linear 2.6 zoom 1.03

# Camera: a whip arriving on the cut. The shot starts thrown sideways and
# smeared, and settles. `z` overscans so the throw never shows an edge.
transform enter_m_tr_whip(dx=180, t=0.26, z=1.3):
    subpixel True
    xanchor 0.5
    yanchor 0.5
    xpos 0.5
    ypos 0.5
    zoom z
    xoffset dx
    blur 9.0
    easein t xoffset 0 blur 0.0

# A layer growing or shrinking about its own anchor.
transform enter_m_tr_zoom(z0=1.0, z1=1.1, t=3.2):
    subpixel True
    zoom z0
    linear t zoom z1

# A layer sliding (dx, dy) pixels over t: parallax, or a slow track.
transform enter_m_tr_drift(dx=0, dy=0, t=3.2):
    subpixel True
    xoffset 0
    yoffset 0
    linear t xoffset dx yoffset dy

# Somebody arriving from dx pixels away: in, settle, then a little drift.
transform enter_m_tr_enter(dx=-300, delay=0.0, t=0.6, after=0, hold=3.0):
    subpixel True
    xoffset dx
    pause delay
    easein t xoffset 0
    linear hold xoffset after

# Somebody sitting down: drop dy pixels after `delay`.
transform enter_m_tr_sit(dy=60, delay=0.0, t=0.6):
    subpixel True
    yoffset 0
    pause delay
    easein t yoffset dy

# Down the lane: the plate runs from x0 to x1, gathering speed and softness.
transform enter_m_tr_run(x0=250, x1=-250, t=3.2):
    subpixel True
    xoffset x0
    blur 0.0
    easeout t xoffset x1 blur 3.0

# A focus pull: hold blur b0, then rack to b1.
transform enter_m_tr_focus(b0=0.0, b1=5.0, delay=1.0, t=0.5):
    blur b0
    pause delay
    ease t blur b1

# One face fading over another, for a turn of expression.
transform enter_m_tr_fade(a0=1.0, a1=0.0, delay=1.0, t=0.25):
    alpha a0
    pause delay
    linear t alpha a1

# A small sway: a bus, a step.
transform enter_m_tr_bob(amp=2.0, period=1.2):
    subpixel True
    block:
        ease (period / 2.0) yoffset amp
        ease (period / 2.0) yoffset 0
        repeat

# A screen's light on a face. It only ever dims, never flashes.
transform enter_m_tr_flicker(depth=0.08):
    matrixcolor BrightnessMatrix(0.0)
    block:
        linear 0.2 matrixcolor BrightnessMatrix(-depth)
        linear 0.3 matrixcolor BrightnessMatrix(0.0)
        linear 0.12 matrixcolor BrightnessMatrix(-depth * 0.5)
        linear 0.42 matrixcolor BrightnessMatrix(0.0)
        linear 0.17 matrixcolor BrightnessMatrix(-depth * 0.8)
        linear 0.33 matrixcolor BrightnessMatrix(0.0)
        repeat

transform enter_m_tr_still(depth=0.0):
    matrixcolor BrightnessMatrix(-depth * 0.4)

# A band of light crossing the frame from x0 to x1 (pixels).
transform enter_m_tr_sweep(x0=1500, x1=-400, delay=0.0, t=1.0, peak=0.2):
    blend "add"
    xanchor 0.5
    xpos x0
    alpha 0.0
    pause delay
    alpha peak
    linear t xpos x1
    alpha 0.0

# Up out of black.
transform enter_m_tr_fade_in(t=1.4):
    alpha 0.0
    linear t alpha 1.0

transform enter_m_tr_grade(m):
    matrixcolor m

transform enter_m_tr_blur(b=10.0):
    blur b

transform enter_m_tr_flash_t(delay=0.0, rise=0.05, fall=0.6, peak=0.8):
    alpha 0.0
    pause delay
    linear rise alpha peak
    easein fall alpha 0.0

# Typography lives on its own clock: in, hold, out, all inside `life`.
transform enter_m_tr_life(delay=0.0, life=2.0):
    alpha 0.0
    yoffset 10
    pause delay
    easein 0.3 alpha 1.0 yoffset 0
    pause max(0.0, life - 0.6)
    easeout 0.3 alpha 0.0 yoffset -6

# The written line arrives and stays; the drop takes it down with a cut.
transform enter_m_tr_arrive(delay=0.0):
    alpha 0.0
    yoffset 8
    pause delay
    easein 0.45 alpha 1.0 yoffset 0

# A thin dropout band slipping sideways now and then: the signal losing lock.
transform enter_m_tr_tear(y=200, slip=40.0, period=2.0, delay=0.0):
    ypos y
    alpha 0.0
    pause delay
    block:
        linear 0.04 alpha 0.55 xoffset slip
        linear 0.10 xoffset 0
        linear 0.06 alpha 0.0
        pause period
        repeat

# A soft dark hum bar rolling down the frame, slowly, the way a weak signal does.
transform enter_m_tr_roll(period=3.2):
    block:
        ypos -160
        linear period ypos 720
        repeat

# The letterbox leaves when the title lands; the chrome fades with it.
transform enter_m_tr_bar_top:
    on hide:
        easeout 0.45 yoffset -60

transform enter_m_tr_bar_bottom:
    on hide:
        easeout 0.45 yoffset 60

transform enter_m_tr_chrome:
    on show:
        alpha 0.0
        linear 0.8 alpha 1.0
    on hide:
        linear 0.3 alpha 0.0

# The wordmark slams in on the drop.
transform enter_m_tr_title_in:
    on show:
        subpixel True
        alpha 0.0
        zoom 1.22
        easein 0.42 alpha 1.0 zoom 1.0
    on hide:
        linear 0.35 alpha 0.0

# The "M" splits red and cyan like the logo's, then kicks wider on the next two
# hits (52.4 and 53.2 s: 1.2 and 2.0 s after the title appears).
transform enter_m_tr_chroma(side=1):
    subpixel True
    blend "add"
    alpha 0.0
    xoffset (side * 36)
    easein 0.45 alpha 0.95 xoffset (side * 5)
    pause 0.69
    easeout 0.06 xoffset (side * 16)
    easein 0.3 xoffset (side * 5)
    pause 0.44
    easeout 0.06 xoffset (side * 16)
    easein 0.3 xoffset (side * 5)

transform enter_m_tr_fade_screen:
    on show:
        alpha 0.0
        linear 0.4 alpha 1.0
    on hide:
        linear 0.5 alpha 0.0


# -----------------------------------------------------------------------------
# 7. SCREENS
# -----------------------------------------------------------------------------

# The frame for everything before the title: letterbox and the preview bug.
screen enter_m_tr_frame():
    zorder 80

    add Solid(ENTER_M_TR_INK) xysize (1280, 60) at enter_m_tr_bar_top
    add Solid(ENTER_M_TR_INK) xysize (1280, 60) ypos 660 at enter_m_tr_bar_bottom

    hbox:
        at enter_m_tr_chrome
        xpos 34
        ypos 23
        spacing 10
        add Solid(ENTER_M_TR_TEAL) xysize (8, 8) yalign 0.5
        text _("NEXT TIME") style "enter_m_tr_bug" yalign 0.5

# A spoken line, subtitled. Nobody is named.
screen enter_m_tr_line(what, delay=0.0, life=2.0):
    zorder 90

    fixed:
        at enter_m_tr_life(delay, life)
        add ENTER_M_TR_DIR + "shade_v.png" xysize (1280, 250) ypos 410
        text ('"' + what + '"') style "enter_m_tr_say" xalign 0.5 yanchor 1.0 ypos 640 xmaximum 1040

    timer (delay + life + 0.05) action Hide("enter_m_tr_line")

# A written line. It stays until the label takes it down, so it can outlast
# the picture under it and hold through the silence.
screen enter_m_tr_note(what, delay=0.0):
    zorder 90

    fixed:
        at enter_m_tr_arrive(delay)
        add ENTER_M_TR_DIR + "shade_v.png" xysize (1280, 250) ypos 410
        text what style "enter_m_tr_note" xalign 0.5 yanchor 0.5 ypos 560 xmaximum 1040

# The broadcast itself: grain from the first frame, then dropout bands and a
# hum bar while the music runs hot (`level` 0-1, set per section by the label).
# The whole frame decays together; nothing in a picture or a face is singled
# out. Photosensitive Mode keeps a still grain and the slow hum bar, and drops
# the flickering bands.
screen enter_m_tr_signal(level=0.35):
    zorder 78

    python:
        _tr_safe = enter_m_photosensitive()

    if _tr_safe:
        add "assets/backgrounds/noise1.jpg" xysize (1280, 720) alpha (0.05 * level)
    else:
        add "noise" alpha (0.06 * level)

    if level >= 0.5:
        add ENTER_M_TR_DIR + "band.png" xysize (1280, 160) alpha ((0.2 if _tr_safe else 0.38) * level) at enter_m_tr_roll(3.2)
        if not _tr_safe:
            add Solid("#0b1512") xysize (1280, 5) at enter_m_tr_tear(176, 46 * level, 1.7, 0.2)
            add Solid("#1a2a25") xysize (1280, 2) at enter_m_tr_tear(452, -34 * level, 2.3, 0.9)
            add Solid("#0e1a17") xysize (1280, 7) at enter_m_tr_tear(574, 28 * level, 2.9, 1.5)

# A swell of light over the whole picture (under the letterbox, which stays
# black). Photosensitive Mode keeps a low, slow one.
screen enter_m_tr_flash(color="#eef5f7", peak=0.7, rise=0.05, fall=0.6, delay=0.0):
    zorder 79

    python:
        _tr_safe = enter_m_photosensitive()
        _tr_peak = min(peak, 0.22) if _tr_safe else peak
        _tr_rise = max(rise, 0.45) if _tr_safe else rise
        _tr_fall = max(fall, 0.9) if _tr_safe else fall

    add Solid(color) at enter_m_tr_flash_t(delay, _tr_rise, _tr_fall, _tr_peak)

    timer (delay + _tr_rise + _tr_fall + 0.1) action Hide("enter_m_tr_flash")

# The title: the logo's wordmark, set live so it stays sharp at any size.
screen enter_m_tr_title():
    zorder 90

    add ENTER_M_TR_DIR + "vignette.png" xysize (1280, 720) at enter_m_tr_fade_screen
    add ENTER_M_TR_DIR + "band.png" xysize (1280, 250) yalign 0.5 at enter_m_tr_fade_screen

    hbox:
        at enter_m_tr_title_in
        xalign 0.5
        yalign 0.5
        text ">" style "enter_m_tr_wordmark" color "#8b9096"
        text " ENTER_" style "enter_m_tr_wordmark"
        fixed:
            fit_first True
            text "M" style "enter_m_tr_wordmark"
            text "M" style "enter_m_tr_wordmark" color "#ff2d55" at enter_m_tr_chroma(-1)
            text "M" style "enter_m_tr_wordmark" color "#28e6ff" at enter_m_tr_chroma(1)
        text "." style "enter_m_tr_wordmark"

# The sign-off.
screen enter_m_tr_next():
    zorder 90

    vbox:
        at enter_m_tr_fade_screen
        xalign 0.5
        yalign 0.47
        spacing 8
        text _("NEXT TIME") style "enter_m_tr_next_kicker" xalign 0.5
        add Solid(ENTER_M_TR_TEAL) xysize (44, 2) xalign 0.5
        null height 14
        text _("CHAPTER 1") style "enter_m_tr_kicker" xalign 0.5
        text _("ROOM FOR SIX") style "enter_m_tr_card_title" xalign 0.5
        text _("JUNE 1 – JULY 15") style "enter_m_tr_span" xalign 0.5

# The skip affordance, live for the whole trailer.
screen enter_m_prologue_trailer_skip():
    zorder 100

    key "K_ESCAPE" action Jump("enter_m_prologue_trailer_skip")
    key "K_SPACE" action Jump("enter_m_prologue_trailer_skip")
    key "K_RETURN" action Jump("enter_m_prologue_trailer_skip")
    key "K_KP_ENTER" action Jump("enter_m_prologue_trailer_skip")

    textbutton _("SKIP"):
        style "enter_m_tr_skip_button"
        xanchor 1.0
        xpos 1246
        ypos 13
        action Jump("enter_m_prologue_trailer_skip")


# -----------------------------------------------------------------------------
# 8. THE TRAILER
# -----------------------------------------------------------------------------
# Each shot cuts to its picture on an ink plate, then holds to the next mark
# on the cue. Text screens time themselves (delay + life), so a shot never
# waits on its type. A replaced screen keeps the old instance's hide timer,
# which would take a new line down on arrival, so each line hides the last
# before it shows.

label enter_m_prologue_trailer:
    $ enter_m_tr_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ enter_m_tr_warm(ENTER_M_TR_WARM_LIST)

    # 0.0 THEATER -- the dark house and its blank screen, up from black. The
    # projector's light stirs before anyone is seen.
    scene expression Solid(ENTER_M_TR_INK)
    show bg theater_inside as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_push(1.0, 1.08, 3.4, 0.48, 0.30), enter_m_tr_fade_in(1.2)
    show screen enter_m_tr_frame
    show screen enter_m_tr_signal(0.35)
    show screen enter_m_prologue_trailer_skip
    play music scamall noloop
    $ enter_m_tr_clock_start()
    $ enter_m_tr_at(enter_m_tr_t(1))

    # 3.2 WATCHER -- the reverse: MC in the seats, the screen's light on him.
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_watcher() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_push(1.0, 1.07, 3.4, 430.0 / 1280.0, 300.0 / 720.0)
    $ enter_m_tr_at(enter_m_tr_t(2))

    # 6.4 CUP -- a paper cup somebody left, coming into focus.
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_cup() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_push(1.0, 1.06, 3.4, 0.5, 0.5)
    show screen enter_m_tr_line(_("They spelled my name wrong."), delay=1.0, life=2.0)
    $ enter_m_tr_at(enter_m_tr_t(3))

    # 9.6 STREET -- headlights, then Matsuda backs into frame mid-performance,
    # and the focus finds Tsubaki for her line.
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_street() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW)
    hide screen enter_m_tr_line
    show screen enter_m_tr_line(_("You can just say friend."), delay=2.4, life=2.2)
    $ enter_m_tr_at(enter_m_tr_t(4, 2))

    # 14.4 BUS -- Monika by the window, the road running out behind her; the
    # push lands on her eyes.
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_bus() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_push(1.0, 1.12, 4.9, 860.0 / 1280.0, 270.0 / 720.0)
    $ enter_m_tr_at(enter_m_tr_t(6))

    # 19.2 TRACK -- down the lane, gathering speed into the riser.
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_track() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW)
    $ enter_m_tr_at(enter_m_tr_t(7))

    # 22.4 RISER -- whip-ins on the beat, then the half-beat; the signal slips.
    show screen enter_m_tr_signal(0.8)
    $ renpy.transition(enter_m_tr_cut(), layer="master")
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_bard() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_whip(200)
    $ enter_m_tr_at(enter_m_tr_t(7, 1))
    $ renpy.transition(enter_m_tr_cut(), layer="master")
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_arcade_gun() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_whip(200)
    $ enter_m_tr_at(enter_m_tr_t(7, 2))
    $ renpy.transition(enter_m_tr_cut(), layer="master")
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_notes() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_whip(-200)
    $ enter_m_tr_at(enter_m_tr_t(7, 2.5))
    $ renpy.transition(enter_m_tr_cut(), layer="master")
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_sam() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_whip(200)
    $ enter_m_tr_at(enter_m_tr_t(7, 3))
    $ renpy.transition(enter_m_tr_cut(), layer="master")
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_kitchen() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_whip(-200)
    $ enter_m_tr_at(enter_m_tr_t(7, 3.5))
    $ renpy.transition(enter_m_tr_cut(), layer="master")
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_club_glimpse() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_whip(200)
    $ enter_m_tr_at(enter_m_tr_hit)

    # 25.5 TABLE -- the crash lands on six lunches, set out and waiting, and
    # Tsubaki comes in from the left.
    show screen enter_m_tr_flash("#eef5f7", 0.7, rise=0.03, fall=0.7)
    show screen enter_m_tr_signal(0.6)
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_table() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_slam(1.12, 1.0, 0.55, 0.6, 0.5, 0.05, 5.9)
    hide screen enter_m_tr_line
    show screen enter_m_tr_line(_("You can sit if you want."), delay=2.7, life=2.6)
    $ enter_m_tr_at(enter_m_tr_t(10))

    # 32.0 SIX -- all of them, once, the camera tracking past in two depths.
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_six() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW)
    $ enter_m_tr_at(enter_m_tr_t(12))

    # 38.4 HOME -- MC sharp, his sister soft at the edge; the focus goes to
    # her as her line ends.
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_home() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW)
    hide screen enter_m_tr_line
    show screen enter_m_tr_line(_("Hey, I listen sometimes."), delay=0.4, life=2.2)
    $ enter_m_tr_at(enter_m_tr_t(13))

    # 41.6 MONTAGE -- one per beat: the race, the beach, the umbrellas, and
    # the club room, wide.
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_race() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_push(1.0, 1.06, 0.9, 0.5, 0.45)
    $ enter_m_tr_at(enter_m_tr_t(13, 1))
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_beach() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_whip(-160, 0.24, 1.2)
    $ enter_m_tr_at(enter_m_tr_t(13, 2))
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_umbrellas() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_push(1.0, 1.05, 0.9, 0.5, 0.5)
    $ enter_m_tr_at(enter_m_tr_t(13, 3))
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_club_wide() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_push(1.0, 1.04, 0.9, 0.35, 0.45)
    $ enter_m_tr_at(enter_m_tr_t(14))

    # 44.8 CLUB -- Monika listens; the push lands on her as the line ends.
    scene expression Solid(ENTER_M_TR_INK)
    show expression enter_m_tr_s_club() as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_push(1.0, 1.16, 3.3, 430.0 / 1280.0, 280.0 / 720.0)
    show screen enter_m_tr_signal(0.5)
    hide screen enter_m_tr_line
    show screen enter_m_tr_line(_("I'm giving the place time to exist."), delay=0.4, life=2.4)
    $ enter_m_tr_at(enter_m_tr_t(15))

    # 48.0 DOOR -- up the stairs at a run, the doorway rushing up on the
    # brightest hits; the question comes in on the second of them.
    scene expression Solid(ENTER_M_TR_INK)
    show bg rooftop_door as tr_shot at enter_m_tr_grade(ENTER_M_TR_HOLLOW), enter_m_tr_climb
    show screen enter_m_tr_note(_("Does the traveler go inside?"), delay=0.8)
    $ enter_m_tr_at(enter_m_tr_break)

    # 50.4 BREAK -- the music stops and so does the signal. Through the door:
    # the traveler, his back to us in the static, looking over his shoulder.
    # The question stays, and nothing moves.
    scene expression Solid(ENTER_M_TR_INK)
    show enter_m_tr_keyart as tr_shot at enter_m_tr_push(2.4, 2.42, 0.9, 0.32, 0.32, 0.5, 0.5)
    hide screen enter_m_tr_signal
    $ enter_m_tr_at(enter_m_tr_drop)

    # 51.2 DROP -- the camera pulls back off him to the whole picture, and the
    # title lands on it. The letterbox opens with it.
    hide screen enter_m_tr_note
    show screen enter_m_tr_flash("#eef5f7", 0.5, rise=0.02, fall=0.5)
    scene enter_m_tr_keyart at enter_m_tr_reveal
    hide screen enter_m_tr_frame
    show screen enter_m_tr_signal(0.3)
    show screen enter_m_tr_title
    $ enter_m_tr_at(enter_m_tr_t(17))

    # 54.4 NEXT -- where the story picks up: the same table, far back.
    hide screen enter_m_tr_title
    hide screen enter_m_tr_signal
    scene enter_m_tr_cg1 at enter_m_tr_grade(ENTER_M_TR_DEEP), enter_m_tr_blur(14.0), enter_m_tr_push(1.25, 1.3, 3.6, 0.5, 0.6)
    show screen enter_m_tr_next
    $ enter_m_tr_at(enter_m_tr_t(17, 3))

    # 56.8 OUT -- the cue fades under the last frame; control returns after it.
    stop music fadeout 2.4
    hide screen enter_m_tr_next
    scene black
    with Dissolve(1.2)
    $ renpy.pause(1.4, hard=True)
    # The fade is long done in play; Ctrl-skip passes the pauses, so make sure.
    stop music
    $ enter_m_tr_cleanup()
    $ quick_menu = enter_m_tr_prev_quick_menu
    return

# SKIP: stop the music, take everything down, hand back the same clean state.
label enter_m_prologue_trailer_skip:
    $ quick_menu = False
    stop music fadeout 0.25
    $ enter_m_tr_cleanup()
    scene black with Dissolve(0.25)
    $ renpy.pause(0.25, hard=True)
    stop music
    $ quick_menu = enter_m_tr_prev_quick_menu
    return
