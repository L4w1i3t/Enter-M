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

    ID_CARD_NAME_ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -'"

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

    unoriginal_names = {
        "mc",
        "player",
        "maincharacter",
        "main character",
        "protagonist",
        "protag",
        "emcee"
    }

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
        "bronya": "Everything personal.",
        "bronyarand": "Everything personal.",
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

    def id_card_clean_name(name):
        return " ".join((name or "").strip().split())

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

    def id_card_photo_for_name(name):
        compact_name = id_card_name_lookup_key(name)

        if compact_name in ("azaraeldelcarmen", "azarael", "weiss", "ganstakingofsa"):
            return "mod_assets/gui/azarael.png"

        return "mod_assets/gui/mc_id_photo.png"

    def id_card_prepare():
        existing_name = persistent.playername or ""
        if not existing_name and player not in ("", "?"):
            existing_name = player

        store.id_card_name_input = existing_name
        store.id_card_birth_month = str(persistent.player_birth_month or "")
        store.id_card_birth_day = str(persistent.player_birth_day or "")
        store.id_card_active_field = "name"

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

    def commit_id_card_info_from_fields():
        id_card_zero_pad_birthday()
        commit_id_card_info(store.id_card_name_input, store.id_card_birth_month, store.id_card_birth_day)

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


transform id_card_info_entry_enter:
    on show:
        alpha 0.0
        yoffset -12
        easein_quad 0.25 alpha 1.0 yoffset 0
    on hide:
        alpha 1.0
        easeout_quad 0.25 alpha 0.0 yoffset -12


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

    #add Solid("#03050af2")

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
            add "mod_assets/gui/id_frame.png":
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
            else:
                text "READY FOR ISSUE" style "id_card_ready":
                    xpos 248
                    ypos 332

            textbutton "ISSUE CARD":
                style "id_card_submit_button"
                xpos 600
                ypos 365
                sensitive _id_ok
                action _id_submit_action

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

style id_card_photo_text:
    font gui.interface_font
    size 16
    color "#5f6368"
    bold True
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
