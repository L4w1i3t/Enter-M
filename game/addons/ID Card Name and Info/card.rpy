# Student ID entry: call screen id_card_info_entry to collect a name/birthday.
# Valid issuance stores player, persistent.playername and the birthday/date parts.
# commit_id_card_info() uses the same validation without opening the screen.
# Names use letters/spaces/hyphens/apostrophes, within the configured length limits;
# normalized lookup rejects reserved names and look-alike variants. Birthdays must
# form a real month/day. Screen-local fields own focus and restore the quick menu.

default id_card_name_input = ""
default id_card_birth_month = ""
default id_card_birth_day = ""
default id_card_active_field = "name"
default id_card_prev_quick_menu = True
default persistent.player_birthday = ""
default persistent.player_birth_month = ""
default persistent.player_birth_day = ""

init python:
    import datetime
    import unicodedata

    # Characters the name input accepts (also enforced by the input's `allow`).
    ID_CARD_NAME_ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -'"

    # Leetspeak/look-alike folding used by the lookup key so e.g. "M0nika" still
    # maps to the blocked "monika". (digit/symbol -> letter it imitates)

    ID_CARD_NAME_LOOKALIKE_CHARS = {
        "0": "o",
        "1": "i",
        "3": "e",
        "4": "a",
        "5": "s",
        "7": "t",
        "@": "a",
        "$": "s",
    }

    # Lazy/placeholder names that get a "be more creative" nudge.
    unoriginal_names = {
        "mc",
        "player",
        "maincharacter",
        "main character",
        "protagonist",
        "protag",
        "emcee"
    }

    # Reserved/blocked names -> the bespoke refusal line shown if entered. Covers
    # cast members, in-joke creator/template references, and profanity/slurs.
    # (Matched via the normalized lookup key, so variants are caught too.)
    illegal_names = {
        "monika": "Sorry, but I'm already Monika~",
        "sayori": "Sorry, eheh...",
        "natsuki": "N-No, baka!",
        "yuri": "...Not appropriate.",
        "matsuda": "Sorry, love, that's mine~",
        "tsubaki": "Um...yeah, no.",
        "masayami": "Absolutely [[bleep] not.",
        "sam": "Absolutely [[bleep] not.",
        "asahina": "Get your own name, bro!",
        "asa": "Get your own name, bro!",
        "kotonoha": "Wanna break immersion?",
        "koto": "Wanna break immersion?",
        "braethan": "This one's personal.",
        "weiss": "Make a better template, first.",
        "ganstakingofsa": "The Windows 11 of templates.",
        "bronya": "She's not even that good!",
        "bronyarand": "She's not even that good!",
        "azaraeldelcarmen": "The Windows 11 of templates.",
        "azarael": "Everything personal.",
        "aahilj": "Pfffft no, not that one.",
        "savage": "Probably best not to.",
        "savagesentral": "Probably best not to.",
        "tuneeternal": "Buy a vinyl and then we'll talk.",
        "qilin": "No.",
        "jqilin": "No.",
        "jayqilin": "No.",
        "qilingaming": "No.",
        "jqilingaming": "No.",
        "jayqilingaming": "No.",
        "afrozero": "Stay vigilant, pick another one.",
        "kryo": "This one's personal.",
        "kryogenic": "This one's personal.",
        "retronika": "Everything personal.",
        "davidlocklin": "Everything personal.",
        "daes": "Nope, not that one.",
        "dokidokidaes": "You're not slick.",
        "atazoth": "Ha, no.",
        "sans": "already taken, kid",
        "papyrus": "I'M NOT EVEN IN THIS GAME",
        "papyru": "I'M NOT EVEN IN THIS GAME",
        "undyne": "Funny, but no.",
        "alphys": "U-Uh, n-no thanks!",
        "mettaton": "Sorry, darling~",
        "toriel": "I'm sorry, my child...",
        "asgore": "I, uh...don't think so.",

        # Profanity
        "shit": "That's not appropriate.",
        "damn": "That's not appropriate.",
        "fuck": "That's not appropriate.",
        "bitch": "That's not appropriate.",
        "asshole": "That's not appropriate.",
        "bastard": "That's not appropriate.",
        "dick": "That's not appropriate.",
        "pussy": "That's not appropriate.",
        "ass": "That's not appropriate.",
        "cock": "That's not appropriate.",
        "cunt": "That's not appropriate.",
        "nigger": "That's not appropriate.",
        "nigga": "That's not appropriate.",
        "faggot": "That's not appropriate.",
        "fag": "That's not appropriate.",
        "slut": "That's not appropriate.",
        "whore": "That's not appropriate.",
        "dickhead": "That's not appropriate.",
        "piss": "That's not appropriate.",
        "retard": "That's not appropriate.",
        "epstein": "That's not appropriate.",
        "hitler": "That's not appropriate.",
        "stalin": "That's not appropriate.",
        "osama": "That's not appropriate.",
        "biden": "That's not appropriate.",
        "trump": "That's not appropriate.",
        "putin": "That's not appropriate.",
    }

    # Collapse runs of whitespace and trim -> the "display" cleaning.
    def id_card_clean_name(name):
        return " ".join((name or "").strip().split())

    # The anti-bypass normalizer. Steps: NFKC + casefold, strip combining accents
    # (NFKD), fold look-alikes (leetspeak), and keep only alphanumerics. The
    # result is what the unoriginal/illegal sets are keyed on, so spacing, case,
    # punctuation, accents, and basic leet variants all collapse to one key.
    def id_card_name_lookup_key(name):
        folded_name = unicodedata.normalize("NFKC", id_card_clean_name(name)).casefold()
        folded_name = unicodedata.normalize("NFKD", folded_name)
        chars = []

        for char in folded_name:
            if unicodedata.combining(char):
                continue

            char = ID_CARD_NAME_LOOKALIKE_CHARS.get(char, char)

            if char.isalnum():
                chars.append(char)

        return "".join(chars)

    unoriginal_name_keys = set(id_card_name_lookup_key(name) for name in unoriginal_names)
    illegal_name_keys = dict(
        (id_card_name_lookup_key(name), message)
        for name, message in illegal_names.items()
    )

    def id_card_name_uses_allowed_chars(name):
        return all(char in ID_CARD_NAME_ALLOWED_CHARS for char in name)

    # Special-case ID photo for a couple of blocked template names; otherwise the
    # default MC photo. (Gotcha: if a special-case asset is missing, Matsu'Py errors
    # on the missing image when that name is entered.)
    def id_card_photo_for_name(name):
        compact_name = id_card_name_lookup_key(name)

        if compact_name in ("azaraeldelcarmen", "azarael", "weiss", "ganstakingofsa"):
            return "assets/gui/azarael.png"

        return "assets/gui/mc_id_photo.png"

    def id_card_prepare():
        existing_name = "Asahiko" # "canon" name, but exists as a means to say "this is TECHNICALLY the canon name, but you can name them whatever you want"
        if not existing_name and player not in ("", "?"):
            existing_name = player

        store.id_card_name_input = existing_name
        store.id_card_birth_month = str(persistent.player_birth_month or "")
        store.id_card_birth_day = str(persistent.player_birth_day or "")
        store.id_card_active_field = "name"

    # The validator. Returns (ok, error_message, data) -- data (name + parsed
    # birthday fields + "MM/DD" display) only on success. The screen calls this
    # every redraw to drive the error/ready text and the ISSUE button's sensitivity.
    def validate_id_card_info(name, month, day):
        clean_name = id_card_clean_name(name)
        name_key = id_card_name_lookup_key(clean_name)

        if not clean_name:
            return False, "Enter a name.", None

        if not name_key:
            return False, "Enter a name with letters.", None

        if name_key in unoriginal_name_keys:
            return False, "Can't you be more creative?", None

        if name_key in illegal_name_keys:
            return False, illegal_name_keys[name_key], None

        if not id_card_name_uses_allowed_chars(clean_name):
            return False, "Use letters, spaces, hyphens, and apostrophes only.", None

        if len(clean_name) < 3:
            return False, "Name is too short.", None

        if len(clean_name) > 24:
            return False, "Name must be 24 characters or fewer.", None

        try:
            month_i = int(month)
            day_i = int(day)
        except Exception:
            return False, "Enter a numeric birthday.", None

        try:
            datetime.date(2000, month_i, day_i)
        except ValueError:
            return False, "Enter a valid birthday.", None

        return True, "", {
            "name": clean_name,
            "birth_month": month_i,
            "birth_day": day_i,
            "birthday_display": "{:02d}/{:02d}".format(month_i, day_i),
        }

    def id_card_zero_pad_birth_field(field):
        if field == "month":
            attr = "id_card_birth_month"
        elif field == "day":
            attr = "id_card_birth_day"
        else:
            return

        value = (getattr(store, attr) or "").strip()
        if len(value) == 1 and value.isdigit():
            setattr(store, attr, "{:02d}".format(int(value)))

    def id_card_zero_pad_birthday():
        id_card_zero_pad_birth_field("month")
        id_card_zero_pad_birth_field("day")

    def id_card_select_field(field):
        id_card_zero_pad_birth_field(store.id_card_active_field)
        store.id_card_active_field = field

    def id_card_blur_field():
        id_card_zero_pad_birth_field(store.id_card_active_field)
        store.id_card_active_field = ""

    # zero-pad helpers keep single-digit month/day fields as "0N" when focus leaves.
    # commit_*_from_fields is what the ISSUE button calls (pads, then commits).
    def commit_id_card_info_from_fields():
        id_card_zero_pad_birthday()
        commit_id_card_info(store.id_card_name_input, store.id_card_birth_month, store.id_card_birth_day)

    # PUBLIC: validate then persist. On failure it just notifies and returns
    # (does NOT save). On success: sets player + the persistent.* fields and saves.
    def commit_id_card_info(name, month, day):
        ok, message, data = validate_id_card_info(name, month, day)

        if not ok:
            renpy.notify(message)
            return

        store.player = data["name"]
        persistent.playername = data["name"]
        persistent.player_birthday = data["birthday_display"]
        persistent.player_birth_month = "{:02d}".format(data["birth_month"])
        persistent.player_birth_day = "{:02d}".format(data["birth_day"])
        renpy.save_persistent()


# --- ANIMATION LIBRARY (the card's "alive" layer) ---------------------------
# Entrance: the card is dealt onto the desk (slide up + slight rotation with a
# small overshoot), then it floats gently forever. On hide it slips back down.
transform id_card_info_entry_enter:
    on show:
        subpixel True
        alpha 0.0
        zoom 1.05
        rotate -5
        yoffset 54
        easeout_quad 0.30 alpha 1.0 zoom 0.995 rotate 0.6 yoffset -6
        ease 0.16 zoom 1.0 rotate 0.0 yoffset 0
        block:
            ease 2.6 yoffset -5
            ease 2.6 yoffset 0
            repeat
    on hide:
        subpixel True
        easein_quad 0.24 alpha 0.0 yoffset 42 rotate 3 zoom 1.03

# Backdrop dim that fades in under the card so the scene behind recedes.
transform id_card_backdrop_dim:
    alpha 0.0
    linear 0.35 alpha 0.42

# Very faint colored light bands drifting diagonally behind the card.
transform id_card_bg_band(y=200, band_alpha=0.05, direction=1):
    subpixel True
    xysize (1600, 120)
    rotate (-8 * direction)
    xpos -160
    ypos y
    alpha 0.0
    linear 0.6 alpha band_alpha
    block:
        linear 9.0 xoffset (120 * direction)
        linear 9.0 xoffset 0
        repeat

# Holographic security chip: hue cycles forever (clipped inside the card).
transform id_card_holo:
    alpha 0.85
    block:
        matrixcolor HueMatrix(0.0)
        linear 5.0 matrixcolor HueMatrix(360.0)
        repeat

# One-shot glint: a single soft light band that crosses once. Real cards glint
# when they MOVE, so this fires exactly as the card lands from its entrance
# (and once over the photo), then stays quiet -- no looping conveyor-belt sheen.
# `soften` is a GPU blur that turns the bar into a light gradient.
transform id_card_sheen_once(delay=0.0, width=240, sheen_alpha=0.10, travel=1150, soften=36, height=900, speed=0.7):
    subpixel True
    xysize (width, height)
    rotate 24
    ypos (-height // 4)
    blur soften
    xpos (-width - 340)
    alpha 0.0
    pause delay
    linear 0.08 alpha sheen_alpha
    linear speed xpos travel
    linear 0.08 alpha 0.0

# Ambient highlight: a broad, very faint glow that breathes in sync with the
# card's idle float -- like room light shifting on a laminated surface.
transform id_card_sheen_ambient:
    subpixel True
    xysize (340, 900)
    rotate 24
    ypos -225
    xpos 420
    blur 64
    alpha 0.0
    linear 1.0 alpha 0.05
    block:
        ease 2.6 xoffset 36 alpha 0.075
        ease 2.6 xoffset 0 alpha 0.045
        repeat

# Underline that draws in under the focused field, then pulses.
transform id_card_focus_pulse:
    xanchor 0.0
    xzoom 0.0
    easeout_quad 0.20 xzoom 1.0
    block:
        linear 0.7 alpha 0.45
        linear 0.7 alpha 1.0
        repeat

# READY FOR ISSUE breathes; errors slide in once and hold.
transform id_card_ready_pulse:
    alpha 0.0
    easeout_quad 0.25 alpha 1.0
    block:
        linear 0.8 alpha 0.55
        linear 0.8 alpha 1.0
        repeat

transform id_card_error_in:
    alpha 0.0
    xoffset -8
    easeout_quad 0.18 alpha 1.0 xoffset 0

# Soft red halo behind ISSUE CARD while the card is valid.
transform id_card_issue_glow:
    alpha 0.0
    easeout_quad 0.30 alpha 0.55
    block:
        linear 0.75 alpha 0.30
        linear 0.75 alpha 0.60
        repeat

# Photo fades in ("develops") -- also replays when a special name swaps it.
transform id_card_photo_in:
    alpha 0.0
    linear 0.25 alpha 1.0


# =============================================================================
# THE ID CARD SCREEN
# Draws the card art + fields. Tabbing/Enter cycles name -> month -> day -> ISSUE.
# Clicking outside the fields blurs them (id_card_blur_field). On show it hides
# the quick menu and prepopulates via id_card_prepare(); on hide it restores the
# quick menu. The validator result (_id_ok/_id_error) gates the ISSUE button and
# the READY/error text. ISSUE -> commit_id_card_info_from_fields + Return(True).
# =============================================================================
screen id_card_info_entry():
    modal True
    zorder 220

    on "show" action [SetVariable("id_card_prev_quick_menu", quick_menu), SetVariable("quick_menu", False), Function(id_card_prepare)]
    on "hide" action SetVariable("quick_menu", id_card_prev_quick_menu)

    $ _id_ok, _id_error, _id_data = validate_id_card_info(
        id_card_name_input,
        id_card_birth_month,
        id_card_birth_day,
    )
    $ _id_name_value = VariableInputValue("id_card_name_input", default=(id_card_active_field == "name"))
    $ _id_month_value = VariableInputValue("id_card_birth_month", default=(id_card_active_field == "month"))
    $ _id_day_value = VariableInputValue("id_card_birth_day", default=(id_card_active_field == "day"))
    $ _id_submit_action = [Function(commit_id_card_info_from_fields), Return(True)]

    # Animated backdrop: dim the scene, drift two faint light bands behind the card.
    add Solid("#03050a") at id_card_backdrop_dim
    add Solid("#75c8ff") at id_card_bg_band(170, 0.05, 1)
    add Solid("#cc2233") at id_card_bg_band(520, 0.04, -1)

    button:
        xfill True
        yfill True
        background None
        hover_background None
        action Function(id_card_blur_field)

    frame:
        xalign 0.5
        yalign 0.5
        xysize (780, 420)
        background None
        padding (0, 0)
        at id_card_info_entry_enter

        fixed:
            # Soft drop shadow under the card (rides the float since it's inside the frame).
            add Solid("#000000"):
                xysize (780, 420)
                xoffset 12
                yoffset 16
                alpha 0.45
                blur 26

            add "assets/gui/id_frame.png":
                xpos 0
                ypos 0
                xsize 780
                ysize 420

            add Solid("#111722"):
                xpos 0
                ypos 0
                xsize 780
                ysize 74

            text "ITSUKI ACADEMY" style "id_card_school":
                xpos 34
                ypos 18

            text "STUDENT IDENTIFICATION" style "id_card_header":
                xpos 34
                ypos 44

            # Holographic security chip, hue-cycling forever.
            add Solid("#7fe0ff"):
                xysize (44, 44)
                xpos 706
                ypos 15
                at id_card_holo
            add Solid("#ffffff22"):
                xysize (44, 44)
                xpos 706
                ypos 15

            add Solid("#cc2233"):
                xpos 0
                ypos 74
                xsize 780
                ysize 8

            frame:
                xpos 36
                ypos 112
                xysize (178, 210)
                background Solid("#858585")
                padding (0, 0)

                fixed:

                    add id_card_photo_for_name(id_card_name_input):
                        xpos 26
                        ypos 26
                        xsize 126
                        ysize 126
                        at id_card_photo_in

                    # Laminate glare: one pass over the photo after the card lands.
                    viewport:
                        xpos 26
                        ypos 26
                        xysize (126, 126)
                        fixed:
                            xysize (126, 126)
                            add Solid("#ffffff") at id_card_sheen_once(0.95, 90, 0.20, 300, 16, 320, 0.5)

                    add Solid("#ffffff"):
                        xpos 28
                        ypos 174
                        xsize 122
                        ysize 10

            text "ID NUMBER" style "id_card_field_label":
                xpos 36
                ypos 334

            text "6769420" style "id_card_readonly_value":
                xpos 36
                ypos 354

            vbox:
                xpos 248
                ypos 110
                xsize 470
                spacing 18

                vbox:
                    spacing 6
                    text "NAME" style "id_card_field_label"
                    fixed:
                        xysize (470, 44)
                        button:
                            style "id_card_input_button"
                            selected id_card_active_field == "name"
                            action [Function(id_card_select_field, "name"), _id_name_value.Enable()]
                        input:
                            value _id_name_value
                            length 24
                            allow ID_CARD_NAME_ALLOWED_CHARS
                            style "id_card_input_text"
                            copypaste True
                            xpos 12
                            xanchor 0.0
                            ypos 0.5
                            yanchor 0.5
                            xsize 446
                        if id_card_active_field == "name":
                            add Solid("#cc2233"):
                                xysize (470, 3)
                                ypos 41
                                at id_card_focus_pulse

                vbox:
                    spacing 6
                    text "DATE OF BIRTH" style "id_card_field_label"
                    hbox:
                        spacing 10

                        fixed:
                            xysize (70, 44)
                            button:
                                style "id_card_short_input_button"
                                selected id_card_active_field == "month"
                                action [Function(id_card_select_field, "month"), _id_month_value.Enable()]
                            input:
                                value _id_month_value
                                length 2
                                allow "0123456789"
                                style "id_card_input_text"
                                xpos 10
                                xanchor 0.0
                                ypos 0.5
                                yanchor 0.5
                                xsize 50
                            if id_card_active_field == "month":
                                add Solid("#cc2233"):
                                    xysize (70, 3)
                                    ypos 41
                                    at id_card_focus_pulse

                        text "/" style "id_card_slash"

                        fixed:
                            xysize (70, 44)
                            button:
                                style "id_card_short_input_button"
                                selected id_card_active_field == "day"
                                action [Function(id_card_select_field, "day"), _id_day_value.Enable()]
                            input:
                                value _id_day_value
                                length 2
                                allow "0123456789"
                                style "id_card_input_text"
                                xpos 10
                                xanchor 0.0
                                ypos 0.5
                                yanchor 0.5
                                xsize 50
                            if id_card_active_field == "day":
                                add Solid("#cc2233"):
                                    xysize (70, 3)
                                    ypos 41
                                    at id_card_focus_pulse

                hbox:
                    spacing 18

                    vbox:
                        spacing 5
                        # fix this, it should be issued in early april
                        text "ISSUED" style "id_card_field_label"
                        text "04/04/2025" style "id_card_readonly_value"

                    vbox:
                        spacing 5
                        text "HOMEROOM" style "id_card_field_label"
                        text "3-B" style "id_card_readonly_value"

                    vbox:
                        spacing 5
                        text "STATUS" style "id_card_field_label"
                        text "ACTIVE" style "id_card_readonly_value"

            if _id_error:
                text _id_error style "id_card_error":
                    xpos 248
                    ypos 332
                    at id_card_error_in
            else:
                text "READY FOR ISSUE" style "id_card_ready":
                    xpos 248
                    ypos 332
                    at id_card_ready_pulse

            if _id_ok:
                add Solid("#cc2233"):
                    xysize (176, 54)
                    xpos 594
                    ypos 359
                    blur 16
                    at id_card_issue_glow

            textbutton "ISSUE CARD":
                style "id_card_submit_button"
                xpos 600
                ypos 365
                sensitive _id_ok
                action _id_submit_action

            # Card gloss (viewport clips it to the card): one soft glint as the
            # card lands, then only the ambient breathing highlight remains.
            viewport:
                xysize (780, 420)
                fixed:
                    xysize (780, 420)
                    add Solid("#ffffff") at id_card_sheen_ambient
                    add Solid("#ffffff") at id_card_sheen_once(0.55, 320, 0.10, 1150, 52)
                    add Solid("#ffffff") at id_card_sheen_once(0.62, 120, 0.14, 1150, 24)

    # Enter advances focus name -> month -> day; on the last field it submits if
    # valid, otherwise pads the birthday and notifies the current error.
    key ["K_RETURN", "K_KP_ENTER"] action If(
        id_card_active_field == "name",
        true=[Function(id_card_select_field, "month"), _id_month_value.Enable()],
        false=If(
            id_card_active_field == "month",
            true=[Function(id_card_select_field, "day"), _id_day_value.Enable()],
            false=If(
                _id_ok,
                true=_id_submit_action,
                false=[Function(id_card_zero_pad_birthday), Notify(_id_error)],
            ),
        ),
    )


# --- STYLES (the ID card's printed look: white fields on a navy/red card) ---
style id_card_school:
    font gui.name_font
    size 24
    color "#ffffff"
    outlines []

style id_card_header:
    font gui.interface_font
    size 16
    color "#a8adb7"
    outlines []

style id_card_field_label:
    font gui.interface_font
    size 14
    color "#5f6368"
    bold True
    outlines []

style id_card_input_button:
    xysize (470, 44)
    background Solid("#ffffff")
    hover_background Solid("#d9f1ff")
    selected_background Solid("#ffe1e7")
    selected_hover_background Solid("#ffd3dc")
    hover_foreground Solid("#72b8d433")
    selected_foreground Solid("#cc223333")
    padding (12, 5, 12, 5)
    keyboard_focus False
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style id_card_short_input_button:
    xysize (70, 44)
    background Solid("#ffffff")
    hover_background Solid("#d9f1ff")
    selected_background Solid("#ffe1e7")
    selected_hover_background Solid("#ffd3dc")
    hover_foreground Solid("#72b8d433")
    selected_foreground Solid("#cc223333")
    padding (10, 5, 10, 5)
    keyboard_focus False
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style id_card_input_text:
    font gui.interface_font
    size 24
    color "#111722"
    outlines []
    caret "input_caret"
    xalign 0.0
    xanchor 0.0
    text_align 0.0

style id_card_slash:
    font gui.interface_font
    size 30
    color "#5f6368"
    outlines []
    yalign 0.5

style id_card_readonly_value:
    font gui.name_font
    size 20
    color "#111722"
    outlines []

style id_card_error:
    font gui.interface_font
    size 16
    color "#cc2233"
    bold True
    outlines []

style id_card_ready:
    font gui.interface_font
    size 16
    color "#1d7a3f"
    bold True
    outlines []

style id_card_submit_button:
    xysize (164, 42)
    background Solid("#111722")
    hover_background Solid("#cc2233")
    insensitive_background Solid("#8f96a3")
    padding (0, 0)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style id_card_submit_button_text:
    font gui.name_font
    size 18
    color "#ffffff"
    insensitive_color "#d9dde3"
    xalign 0.5
    yalign 0.5
    outlines [(1, "#000000", 0, 0)]
