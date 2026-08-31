# =============================================================================
# Phone Model  --  SHARED PHONE CHASSIS for the in-story phone UI
# =============================================================================
#
# WHAT THIS FILE IS
#   The reusable "phone hardware": the body frame, glass screen, side keys,
#   status bar, app icons, the home screen, AND the rounded-surface toolkit that
#   gives the whole phone its modern look. The three phone "apps" each live in a
#   sibling file and BUILD ON the constants + sub-screens here:
#     - text.rpy     : contacts list + message threads (phone_text_*).
#     - call.rpy     : incoming-call + active-call transcript screens.
#     - facetime.rpy : video-call screen.
#
# ROUNDED-SURFACE TOOLKIT (the "flair")
#   Every panel that used to be a hard-cornered Solid is now a rounded, softly
#   shaded panel drawn by two tiny SDF shaders (asset-free, registered at init -10
#   exactly like the OP / boss-fight shaders):
#     - enter_m.phonepanel : a fixed-size rounded rect with an optional vertical
#       gradient + optional border. Used via the PhonePanel(w,h,...) factory.
#     - enter_m.roundmask  : rounds the corners of ANY already-rendered child
#       (used for auto-sized content like message bubbles). Applied via the
#       `phone_round(radius)` transform (`at phone_round(18)`).
#   Helpers: PhonePanel(), _phx_rgba()/_phx_shade() (hex<->float color math).
#   (Depth comes from the body's rim-light border + gradients, not drop shadows:
#   a blurred phone-sized panel still leaves a faint filled rectangle.)
#
# SHARED PIECES OTHER FILES REUSE
#   Constants (init -2): PHONE_MODEL_WIDTH/HEIGHT, PHONE_SCREEN_X/Y/WIDTH/HEIGHT,
#     PHONE_SAFE_LEFT/TOP -- every app sizes its screen to these so the device
#     looks identical across apps.
#   Helper: phone_contact_initials(name) -> 1-2 letter avatar initials.
#   THE CHASSIS: `use phone_device(screen_fill=..., status_clock=...): <content>`
#     draws the scrim + body + glass + notch + status bar + home bar ONCE and
#     transcludes each app's content into the screen area. Every app screen uses
#     it, so the device is pixel-identical everywhere and defined in one place.
#   Sub-screens: phone_side_keys, phone_status_bar(clock,dark), phone_app_icon.
#   Style: phone_model_body (the outer device shell). Transform: phone_model_enter.
#
# ENTRY POINTS (from the menus / story)
#   - Quick menu "Phone" button -> Show("phone_contacts_screen") (in text.rpy).
#   - label phone_home (bottom of this file) shows the app grid; the grid's icons
#     are currently decorative (no per-icon actions wired yet).
#
# AUDIO HOOKS
#   phone_text_in / phone_text_out : the received / sent message SFX, wired into
#     the animated message thread -- each bubble plays its sound as it reveals
#     (see phone_play_reveal_sound in text.rpy). phone_notification deliberately
#     reuses the received-message cue for the small in-game availability alert.
#     phone_ringtone loops on the dedicated "phone_ring" channel while an incoming
#     call rings (see phone_call in call.rpy). phone_open stays a None placeholder
#     (no "raise phone" SFX yet).
# =============================================================================

define -50 audio.phone_text_in = "assets/audio/sfx/phone/messagereceive.ogg"
define -50 audio.phone_text_out = "assets/audio/sfx/phone/messagesend.ogg"
define -50 audio.phone_notification = "assets/audio/sfx/phone/messagereceive.ogg"
define -50 audio.phone_open = None
define -50 audio.phone_ringtone = "assets/audio/sfx/phone/ringtone.ogg"


init python:
    # Dedicated channels keep a notification cue from cutting off a story SFX,
    # and keep the incoming-call ringtone isolated until answer/decline. Both use
    # the sfx mixer, so the player's SFX volume still governs them. try/except
    # keeps autoreload from erroring on a re-register.
    try:
        renpy.music.register_channel("phone_alert", mixer="sfx", loop=False)
    except Exception:
        pass

    try:
        renpy.music.register_channel("phone_ring", mixer="sfx", loop=True)
    except Exception:
        pass


# -----------------------------------------------------------------------------
# Rounded-surface shaders. Registered defensively at init -10 (before any screen
# is shown): a flaky GL driver shouldn't take the whole phone UI down with it.
# Both output PREMULTIPLIED alpha (rgb already * a), matching Matsu'Py's GL2
# pipeline and the project's other shaders.
# -----------------------------------------------------------------------------
init -10 python:
    def _enter_m_phone_register_shaders():

        # ---- phonepanel: procedural rounded rect (gradient + border) ---------
        # Ignores the child texture; draws a rounded rectangle filled with a
        # vertical gradient (u_top -> u_bottom) and an optional inner border ring
        # (u_bcolor / u_border px). The signed-distance field gives crisp,
        # anti-aliased corners at any size.
        renpy.register_shader("enter_m.phonepanel", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_model_size;
            uniform float u_radius;
            uniform vec4 u_top;
            uniform vec4 u_bottom;
            uniform float u_border;
            uniform vec4 u_bcolor;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float enterm_rr_sd(vec2 p, vec2 b, float r) {
                vec2 q = abs(p) - b + vec2(r);
                return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - r;
            }
        """, fragment_300="""
            vec2 size = max(u_model_size, vec2(1.0));
            vec2 uv = v_tex_coord;
            vec2 p = uv * size - size * 0.5;
            vec2 halfb = size * 0.5;
            float r = clamp(u_radius, 0.0, min(halfb.x, halfb.y));
            float d = enterm_rr_sd(p, halfb, r);
            float aa = 1.25;
            float fill = 1.0 - smoothstep(0.0, aa, d);
            vec4 col = mix(u_top, u_bottom, clamp(uv.y, 0.0, 1.0));
            float bw = max(u_border, 0.0);
            float band = (1.0 - smoothstep(bw - aa, bw + aa, abs(d))) * step(d, 0.0) * step(0.001, bw);
            float w = band * u_bcolor.a;
            vec3 rgb = mix(col.rgb, u_bcolor.rgb, w);
            float a = mix(col.a, u_bcolor.a, w) * fill;
            gl_FragColor = vec4(rgb * a, a);
        """)

        # ---- roundmask: round the corners of an existing child ---------------
        # Samples the child (tex0, already premultiplied) and multiplies its
        # alpha by a rounded-rect mask. Lets us round auto-sized content (message
        # bubbles) where we can't know the size up front.
        renpy.register_shader("enter_m.roundmask", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_model_size;
            uniform float u_radius;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float enterm_rr_sd(vec2 p, vec2 b, float r) {
                vec2 q = abs(p) - b + vec2(r);
                return min(max(q.x, q.y), 0.0) + length(max(q, 0.0)) - r;
            }
        """, fragment_300="""
            vec2 size = max(u_model_size, vec2(1.0));
            vec2 uv = v_tex_coord;
            vec2 p = uv * size - size * 0.5;
            vec2 halfb = size * 0.5;
            float r = clamp(u_radius, 0.0, min(halfb.x, halfb.y));
            float d = enterm_rr_sd(p, halfb, r);
            float aa = 1.25;
            float mask = 1.0 - smoothstep(0.0, aa, d);
            gl_FragColor = texture2D(tex0, uv) * mask;
        """)

    try:
        _enter_m_phone_register_shaders()
    except Exception as e:
        renpy.log("ENTER-M PHONE: shader registration failed: %r" % e)


# Geometry constants + the rounded-surface toolkit. init -2 so they exist before
# any screen OR style statement (init 0) that references them.
init -2 python:
    PHONE_MODEL_WIDTH = 394
    PHONE_MODEL_HEIGHT = 668
    PHONE_SCREEN_X = 13
    PHONE_SCREEN_Y = 18
    PHONE_SCREEN_WIDTH = 368
    PHONE_SCREEN_HEIGHT = 632
    PHONE_SAFE_LEFT = 28
    PHONE_SAFE_TOP = 26

    # --- Color math -----------------------------------------------------------
    # _phx_rgba: hex string ("#rgb"/"#rgba"/"#rrggbb"/"#rrggbbaa") OR an rgba/rgb
    # float tuple -> a normalized (r, g, b, a) tuple suitable as a vec4 uniform.
    # _phx_shade: multiply rgb by a factor (keeps alpha) for cheap light/dark
    # variants used to fake gradients.
    # The project-wide parser (game/fx.rpy, init -5). Kept under the local name
    # the rest of this file already uses.
    _phx_rgba = enter_m_rgba

    def _phx_shade(value, factor):
        r, g, b, a = _phx_rgba(value)
        f = max(0.0, factor)
        return (min(1.0, r * f), min(1.0, g * f), min(1.0, b * f), a)

    # --- Rounded panel factory ------------------------------------------------
    # A fixed-size displayable: a rounded rect filled with a vertical gradient
    # (color -> bottom, or flat if bottom is None) and an optional border. The
    # Transform's own xysize defines the mesh area, so u_model_size == (w, h).
    def PhonePanel(width, height, color="#0b1220", bottom=None, radius=22.0, border=0.0, border_color="#00000000"):
        top_rgba = _phx_rgba(color)
        bot_rgba = _phx_rgba(bottom) if bottom is not None else top_rgba
        return Transform(
            Solid("#000000"),
            xysize=(int(round(width)), int(round(height))),
            mesh=True,
            shader="enter_m.phonepanel",
            u_radius=float(radius),
            u_top=top_rgba,
            u_bottom=bot_rgba,
            u_border=float(border),
            u_bcolor=_phx_rgba(border_color),
        )

    # Avatar initials: first letter of the first one or two name words, uppercased.
    # "matsuda_akai" -> "MA", "Monika" -> "M", "" -> "?".
    def phone_contact_initials(name):
        parts = [p for p in name.replace("_", " ").split() if p]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[1][0]).upper()

    # Notification counts are normally one or two digits, but developer tools
    # can expose a much larger catalog. Size badges from the actual text instead
    # of clipping the count or turning it into an inaccurate "99+" shorthand.
    def phone_badge_width(count, min_width=18, digit_width=7, padding=10):
        return max(int(min_width), len(str(max(0, int(count)))) * int(digit_width) + int(padding))


# -----------------------------------------------------------------------------
# COLOR EMOJI  --  drop-in image emoji (works on Matsu'Py 8.1.1, which can't render
# color-emoji FONTS). Put Twemoji/OpenMoji-style PNGs in game/assets/emoji/
# named by codepoint (Twemoji convention): 👍 -> "1f44d.png", 👍🏽 -> "1f44d-1f3fd.png",
# ❤️ -> "2764.png" (the FE0F variation selector is dropped). Then just type the
# literal emoji in a message body -- phone_emojify() swaps it for the image.
# The system is dormant until the folder has PNGs (missing emoji stay as text,
# and the thumbs-up reaction falls back to its hand-drawn icon).
# -----------------------------------------------------------------------------
init python:
    PHONE_EMOJI_DIR = "assets/emoji"
    PHONE_EMOJI_PX = 24          # inline size inside a message bubble
    _phone_emoji_codes = set()   # codepoint-keys we have a PNG (and image) for

    def _phone_scan_emoji():
        # Register every PNG in the emoji folder as a sized image named
        # "emoji_<code>" so {image=emoji_<code>} can reference it. Re-runs on
        # hot-reload, so newly added PNGs light up without a restart.
        try:
            files = renpy.list_files()
        except Exception:
            files = []
        prefix = PHONE_EMOJI_DIR + "/"
        for fn in files:
            if fn.startswith(prefix) and fn.lower().endswith(".png"):
                code = fn[len(prefix):-4].lower()
                if code and code not in _phone_emoji_codes:
                    try:
                        renpy.image("emoji_" + code, Transform(fn, size=(PHONE_EMOJI_PX, PHONE_EMOJI_PX)))
                        _phone_emoji_codes.add(code)
                    except Exception:
                        pass

    def _phone_is_emoji_base(ch):
        o = ord(ch)
        return (
            0x1F300 <= o <= 0x1FAFF or   # main + supplemental symbols/pictographs
            0x1F000 <= o <= 0x1F0FF or   # mahjong / dominoes / playing cards
            0x1F1E6 <= o <= 0x1F1FF or   # regional indicators (flags)
            0x2600 <= o <= 0x27BF or     # misc symbols + dingbats
            0x2300 <= o <= 0x23FF or     # technical (⌚ ⏰ ▶ ...)
            0x2B00 <= o <= 0x2BFF or     # misc symbols & arrows (★ ⬆ ...)
            0x2190 <= o <= 0x21FF or     # arrows
            o in (0x203C, 0x2049, 0x2122, 0x2139)
        )

    def _phone_is_skin(ch):
        return 0x1F3FB <= ord(ch) <= 0x1F3FF

    def _phone_is_regional(ch):
        return 0x1F1E6 <= ord(ch) <= 0x1F1FF

    # Joiner/combining codepoints that glue an emoji cluster together.
    _PH_VS16 = chr(0xFE0F)     # variation selector-16 (emoji presentation)
    _PH_KEYCAP = chr(0x20E3)   # combining enclosing keycap
    _PH_ZWJ = chr(0x200D)      # zero-width joiner

    # Walk a string, grouping emoji "clusters" (base + skin tone / VS16 / keycap /
    # ZWJ-joined sequences / flag pairs). Calls on_emoji(cluster) per cluster and
    # on_text(char) for every non-emoji character.
    def _phone_emoji_walk(text, on_emoji, on_text):
        i, n = 0, len(text)
        while i < n:
            c = text[i]
            if _phone_is_emoji_base(c):
                j = i + 1
                if _phone_is_regional(c) and j < n and _phone_is_regional(text[j]):
                    j += 1
                while j < n:
                    cj = text[j]
                    if cj == _PH_VS16 or cj == _PH_KEYCAP or _phone_is_skin(cj):
                        j += 1
                    elif cj == _PH_ZWJ and j + 1 < n and _phone_is_emoji_base(text[j + 1]):
                        j += 2
                    else:
                        break
                on_emoji(text[i:j])
                i = j
            else:
                on_text(c)
                i += 1

    def _phone_emoji_code(cluster):
        # Twemoji filename key: hex codepoints joined by '-', dropping FE0F.
        return "-".join("{:x}".format(ord(c)) for c in cluster if c != _PH_VS16)

    # Both rewriters walk their input character by character, and both are
    # called from a SCREEN BODY -- once per visible bubble, on every rebuild.
    # A thread animating its reveal restarts the screen 10x/sec, so the same
    # handful of strings would otherwise be re-walked hundreds of times to
    # produce a byte-identical result. The emoji table is fixed after
    # _phone_scan_emoji() at init, so the mapping can never go stale; the cap
    # just keeps a long playthrough's worth of dialogue from accumulating.
    _PHONE_EMOJI_CACHE_MAX = 512
    _phone_emojify_cache = {}
    _phone_strip_cache = {}

    def _phone_cache_put(cache, key, value):
        if len(cache) >= _PHONE_EMOJI_CACHE_MAX:
            cache.clear()
        cache[key] = value
        return value

    def phone_emojify(body):
        # Replace each emoji that has a registered image with {image=emoji_...}.
        # Emoji with no PNG yet are left as literal text.
        if not body:
            return body
        cached = _phone_emojify_cache.get(body)
        if cached is not None:
            return cached
        parts = []
        def emo(cluster):
            code = _phone_emoji_code(cluster)
            if code in _phone_emoji_codes:
                parts.append("{image=emoji_%s}" % code)
            else:
                parts.append(cluster)
        _phone_emoji_walk(body, emo, parts.append)
        return _phone_cache_put(_phone_emojify_cache, body, "".join(parts))

    def phone_strip_emoji(body):
        # Drop emoji entirely -- used for the contacts-list preview line, where a
        # 24px inline image would not fit the small row text.
        if not body:
            return body
        cached = _phone_strip_cache.get(body)
        if cached is not None:
            return cached
        parts = []
        _phone_emoji_walk(body, lambda cluster: None, parts.append)
        return _phone_cache_put(_phone_strip_cache, body, "".join(parts))

    def phone_emoji_loadable(code):
        return renpy.loadable("%s/%s.png" % (PHONE_EMOJI_DIR, code))

    _phone_scan_emoji()


transform phone_model_enter:
    on show:
        alpha 0.0
        yoffset 34
        zoom 0.985
        easeout_quad 0.22 alpha 1.0 yoffset 0 zoom 1.0
    on hide:
        alpha 1.0
        yoffset 0
        easein_quad 0.14 alpha 0.0 yoffset 18

# Rounds the corners of whatever displayable it is applied to (`at phone_round(18)`).
# Renders the child to a texture (mesh) then masks it with a rounded-rect SDF.
transform phone_round(radius=20.0):
    mesh True
    shader "enter_m.roundmask"
    u_radius radius


# =============================================================================
# THE CHASSIS  --  phone_device
# One screen draws the entire device (scrim, body, glass, notch, status bar,
# home bar) and `transclude`s each app's content into the screen area. Every app
# screen wraps its content in `use phone_device(...): <content>`, so the hardware
# lives in exactly one place and looks identical across Messages/Calls/FaceTime.
#   screen_fill  : top color of the display (a slightly darker bottom is derived
#                  automatically for a subtle gradient).
#   status_clock : text shown at the top-left of the status bar (date or HH:MM).
#   device_xalign / device_yalign : where the handset sits on screen. The default
#                  is dead centre, which is what every app that owns the whole
#                  frame wants. The CALL screens push it left (device_xalign
#                  ~0.09) so the conversation can be read beside it -- see
#                  phone_active_call_screen in call.rpy.
#   scrim        : the wash over the scene behind the phone. The centred apps
#                  want it dark because nothing behind them matters; the calls
#                  lighten it, because the scene is still half the picture.
# =============================================================================
screen phone_device(screen_fill="#0b1220", status_clock=None, status_dark=False, show_status=True, show_home_bar=True, home_bar_color="#c7d2e480", device_xalign=0.5, device_yalign=0.5, scrim="#000000aa"):
    add Solid(scrim)

    # NOTE: the whole device (body + glass + notch + status + transcluded app
    # content) animates in/out as ONE unit via `at phone_model_enter` on this
    # frame. Keep the frame as the single animated root -- adding un-animated
    # siblings here (e.g. a drop-shadow) makes them pop in instantly and mask
    # the slide/fade, which reads as "the phone just pops in".
    frame:
        style "phone_model_body"
        at phone_model_enter
        xalign device_xalign
        yalign device_yalign

        fixed:
            xysize (PHONE_MODEL_WIDTH, PHONE_MODEL_HEIGHT)

            use phone_side_keys

            # Glass bezel: a near-black rounded inset that frames the display.
            add PhonePanel(PHONE_SCREEN_WIDTH, PHONE_SCREEN_HEIGHT, "#02040a", radius=34):
                xpos PHONE_SCREEN_X
                ypos PHONE_SCREEN_Y

            # The active display, with a subtle top->bottom gradient.
            add PhonePanel(346, 596, screen_fill, bottom=_phx_shade(screen_fill, 0.78), radius=30):
                xpos 24
                ypos 30

            # Dynamic-island style notch + camera lens.
            add PhonePanel(104, 22, "#000000", radius=11):
                xpos 145
                ypos 40
            add PhonePanel(9, 9, "#0a1626", bottom="#16304e", radius=5):
                xpos 227
                ypos 46

            if show_status:
                use phone_status_bar(status_clock if status_clock is not None else "21:12", status_dark)

            transclude

            if show_home_bar:
                add PhonePanel(108, 5, home_bar_color, radius=2):
                    xpos 143
                    ypos 636


# Decorative power/volume buttons drawn on the device edges (purely cosmetic).
screen phone_side_keys():
    add PhonePanel(5, 78, "#171f2d", radius=2):
        xpos 390
        ypos 128
    add PhonePanel(5, 48, "#171f2d", radius=2):
        xpos 390
        ypos 224
    add PhonePanel(5, 92, "#171f2d", radius=2):
        xpos -1
        ypos 176


# The top status bar: clock on the left, signal bars + battery on the right.
# `dark=True` flips the text/icon colors for use over light backgrounds.
# clock_text is whatever caller passes (often a date label or a HH:MM string).
screen phone_status_bar(clock_text="21:12", dark=False):
    $ _phone_status_style = "phone_status_dark_text" if dark else "phone_status_text"
    $ _phone_status_color = "#101722" if dark else "#f4f7fb"
    $ _phone_status_dim = "#10172255" if dark else "#f4f7fb55"

    fixed:
        xpos 31
        ypos 47
        xysize (332, 24)

        text clock_text style _phone_status_style:
            xpos 0
            yalign 0.5

        hbox:
            xalign 1.0
            yalign 0.5
            spacing 6

            text "LTE" style _phone_status_style

            hbox:
                spacing 2
                yalign 0.5
                add Solid(_phone_status_color):
                    xsize 3
                    ysize 5
                    yalign 1.0
                add Solid(_phone_status_color):
                    xsize 3
                    ysize 8
                    yalign 1.0
                add Solid(_phone_status_color):
                    xsize 3
                    ysize 11
                    yalign 1.0
                add Solid(_phone_status_dim):
                    xsize 3
                    ysize 14
                    yalign 1.0

            fixed:
                xysize (27, 14)
                yalign 0.5

                add PhonePanel(24, 12, "#00000000", radius=3, border=1.5, border_color=_phone_status_color):
                    ypos 1
                add PhonePanel(17, 7, _phone_status_color, radius=1.5):
                    xpos 2
                    ypos 3
                add PhonePanel(2, 5, _phone_status_color, radius=1):
                    xpos 24
                    ypos 4


# -----------------------------------------------------------------------------
# SHARED AVATAR  --  a circular contact avatar used by the contacts list and the
# call / video-call screens. Shows the contact's profile photo (phone_contact_pfp)
# cropped to a circle when one exists, otherwise the initials chip. `size` is the
# circle diameter and `text_style` styles the initials fallback. Draw it inside a
# container sized (size, size) at the position you want (a `use` can't be placed).
# -----------------------------------------------------------------------------
screen phone_avatar(name, size=44, text_style="phone_contact_avatar_text"):
    $ _avatar_size = int(size)
    $ _avatar_radius = _avatar_size / 2.0
    $ _avatar_pfp = phone_contact_pfp(name)

    if _avatar_pfp:
        add Transform(_avatar_pfp, xysize=(_avatar_size, _avatar_size), fit="cover") at phone_round(_avatar_radius)
        add PhonePanel(_avatar_size, _avatar_size, "#00000000", radius=_avatar_radius, border=2.0, border_color="#ffffff33")
    else:
        add PhonePanel(_avatar_size, _avatar_size, "#3a8dff", bottom="#1f6fe0", radius=_avatar_radius)
        text phone_contact_initials(name) style text_style:
            xalign 0.5
            yalign 0.5


# A tiny smartphone silhouette shared by the quick-menu notification badge and
# its short-lived alert chip. Drawing it from the phone's existing panel toolkit
# keeps it crisp at the game's native resolution without adding another asset.
screen phone_notification_glyph(color="#ffffff"):
    fixed:
        xysize (18, 25)

        add PhonePanel(16, 24, "#00000000", radius=4, border=2.0, border_color=color):
            xpos 1
            ypos 0

        add PhonePanel(5, 2, color, radius=1):
            xpos 7
            ypos 3

        add PhonePanel(4, 2, color, radius=1):
            xpos 7
            ypos 19


# A home-screen app icon: a gradient "squircle" with a soft shadow under it,
# the short glyph centered, and the label beneath. Decorative (no action wired).
screen phone_app_icon(short_label, label, color):
    fixed:
        xysize (92, 104)

        fixed:
            xalign 0.5
            ypos 0
            xysize (58, 58)

            add PhonePanel(58, 58, _phx_shade(color, 1.16), bottom=_phx_shade(color, 0.78), radius=15, border=1.0, border_color=_phx_rgba(_phx_shade(color, 1.5), alpha=0.5)):
                xalign 0.5
                yalign 0.5

            text short_label style "phone_app_icon_text":
                xalign 0.5
                yalign 0.5

        text label style "phone_app_label":
            xalign 0.5
            ypos 68


screen phone_home_screen(title="Phone", subtitle=None):
    modal True
    zorder 220

    use phone_device(screen_fill="#0b1220", status_clock="21:12"):

        text title style "phone_home_title":
            xalign 0.5
            ypos 92

        if subtitle:
            text subtitle style "phone_home_subtitle":
                xalign 0.5
                ypos 130

        grid 2 2:
            xpos 78
            ypos 214
            spacing 28

            use phone_app_icon("MSG", "Messages", "#2f7dff")
            use phone_app_icon("CAL", "Calendar", "#ff3b30")
            use phone_app_icon("CON", "Contacts", "#34c759")
            use phone_app_icon("TEL", "Calls", "#30b85b")

    key "dismiss" action Return()


style phone_model_body is empty:
    xalign 0.5
    yalign 0.5
    xysize (394, 668)
    background PhonePanel(394, 668, "#0c111b", bottom="#04060c", radius=50, border=2.0, border_color="#1b2536")
    padding (0, 0)

style phone_status_text:
    font gui.interface_font
    size 13
    color "#f4f7fb"
    bold True
    outlines []

style phone_status_dark_text is phone_status_text:
    color "#101722"

style phone_home_title:
    font gui.name_font
    size 31
    color "#f8fafc"
    text_align 0.5
    outlines [(2, "#000000", 0, 0)]

style phone_home_subtitle:
    font gui.interface_font
    size 16
    color "#aab2c0"
    text_align 0.5
    outlines []

style phone_app_icon_text:
    font gui.name_font
    size 17
    color "#ffffff"
    bold True
    text_align 0.5
    outlines [(1, "#00000066", 0, 0)]

style phone_app_label:
    font gui.interface_font
    size 14
    color "#e6edf7"
    text_align 0.5
    outlines [(1, "#000000", 0, 0)]


# Story/script helper: open the home screen as a blocking call. Automatic window
# management owns the dialogue box while the screen is active.
label phone_home(title="Phone", subtitle=None):
    play sound phone_open
    call screen phone_home_screen(title, subtitle)
    return
