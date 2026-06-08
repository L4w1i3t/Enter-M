# Roster View Addon
# Provides a character roster viewer with character profiles and information

init python:
    import store

    class CharacterProfile:
        def __init__(self, name, full_name, sprite_image, age, height, weight, chest, likes, dislikes, description, fit_mode="contain", manual_exception=None, grayed_out=False):
            self.name = name
            self.full_name = full_name
            self.sprite_image = sprite_image
            self.age = age
            self.height = height      # Height in inches (or string like "Secret")
            self.weight = weight      # Weight in pounds (or string like "Secret")
            self.chest = chest        # Chest in inches (or string like "Secret")
            self.likes = likes
            self.dislikes = dislikes
            self.description = description
            self.fit_mode = fit_mode  # "contain" or "cover" for sprite fitting
            self.manual_exception = manual_exception  # Replaces chest with build descriptor (e.g. for minors)
            self.grayed_out = grayed_out

        @property
        def is_dead(self):
            return "Dead" if self.grayed_out else "Alive"

        def get_height_display(self):
            if isinstance(self.height, str):
                return self.height
            cm = round(self.height * 2.54, 1)
            return "{}\" ({} cm)".format(self.height, cm)

        def get_weight_display(self):
            if isinstance(self.weight, str):
                return self.weight
            kg = round(self.weight * 0.453592, 1)
            return "{} lb ({} kg)".format(self.weight, kg)

        def get_chest_display(self):
            if isinstance(self.chest, str):
                return self.chest
            cm = round(self.chest * 2.54, 1)
            return "{}\" ({} cm)".format(self.chest, cm)
    
    # Initialize character roster
    character_roster = []

    def init_roster():
        global character_roster
        character_roster = [
            CharacterProfile(
                "Matsuda",
                "Matsuda Akai",
                "matsuda neut",
                18,
                69,
                158,
                36,
                "Mystery novels, sports cars, data fragments (???)",
                "Laziness, idiots, mundane tasks",
                "A theatrical transfer student who treats everyday life like she's permanently on stage. Loud, charismatic, and impossible to ignore, Matsuda has a habit of pulling people into her orbit before they realize what's happening. Whether her confidence is genuine or carefully constructed is another question entirely.",
                "contain",
                None,
                False,  # grayed_out
            ),
            CharacterProfile(
                "Player",
                "The Player",
                "mc neut",
                "Variable",
                70,
                150,
                36,
                "???, ???, ???",
                "???, ???, ???",
                "An academically gifted senior student-athlete who prefers structure, routine, and keeping people at arm's length. While others see him as calm and composed, the reality is more complicated: his tendency to hyperfocus, overthink, and emotionally shut down often leaves him feeling disconnected from the people around him. Still, for reasons even he doesn't fully understand, he remains deeply tied to the literature club.",
                "contain",
                None,
                False,
            ),
            CharacterProfile(
                "Tsubaki",
                "Tsubaki Kareda",
                "tsubaki neut",
                17,
                64,
                128,
                0,
                "Hygiene, note-taking, validation",
                "Egos, drama, loud noises",
                "Matsuda's closest friend and frequent damage control specialist. While considerably more reserved than the people around her, Tsubaki has an easygoing warmth that makes her easy to trust. She's the kind of person who keeps things from falling apart quietly, without expecting anyone to notice.",
                "contain",
                "Slim",  # manual_exception
            ),
            CharacterProfile(
                "Asahina",
                "Asahina *********",
                "asahina neut",
                16,
                64,
                139,
                0,
                "Video games, volleyball, her boyfriend",
                "Nagging, early nights, overbearing people",
                "A socially bold underclassman determined to be taken seriously by the people around her. Asahina often presents herself as more mature and experienced than she actually is, bouncing between genuine insight and complete recklessness with alarming speed. Her blunt honesty tends to catch people off guard—especially her older brother.",
                "contain",
                "Athletic",  # manual_exception
            ),
            CharacterProfile(
                "Sam",
                "Masayami Inugami",
                "sam neut",
                18,
                71,
                165,
                38,
                "Indie music, basketball, power naps",
                "Cliffhangers, sour food, micromanagement",
                "Charismatic, perceptive, and difficult to pin down, Sam effortlessly drifts between friend groups without ever seeming out of place. His relaxed attitude and easy smile make him popular with just about everyone he meets, though very few people can confidently say they truly know him.",
                "contain",
                None,
            ),
            CharacterProfile(
                "Mom",
                "Himeko *********",
                "mom neut",
                42,
                66,
                142,
                34,
                "Her children, deck building, initiative",
                "Secrets, unforced errors, messes",
                "A civil lawyer with a calm demeanor and a dangerously accurate read on people. Himeko rarely raises her voice, but her ability to dissect situations—and the people involved in them—makes lying to her feel almost impossible. Beneath her firm exterior is someone trying her best to hold her family together, even when they make that difficult.",
                "contain",
                None,
            ),
            CharacterProfile(
                "Monika",
                "Monika",
                "monika 1a",
                18,
                65,
                125,
                34,
                "Reading, piano, debate",
                "Procrastination, negativity, bugs",
                "A high-achieving senior known for her leadership, composure, and involvement in just about everything the school has to offer. Monika shares an unusually close bond with the protagonist, often acting as both a source of support and the person most capable of seeing through him. Her behavior toward him occasionally borders on flirtatious, whether intentionally or not.",
                "cover",
                None,
                False,
            ),
            CharacterProfile(
                "Kotonoha",
                "Kotonoha",
                "kotonoha neut",
                18,
                65,
                "Secret",
                "Secret",
                "Unknown",
                "Unknown",
                "A student whose existence feels more like a persistent urban legend than a real classmate. Whether she's working behind a cash register, serving customers at a restaurant, or quietly passing through the halls at school, Kotonoha always seems slightly out of place in ways people struggle to explain. Most students know of her, but very few actually know her.",
                "contain",
                None,
            ),
        ]

    def get_character_by_name(name):
        for char in character_roster:
            if char.name.lower() == name.lower():
                return char
        return None

    character_thought_catalog = [
        {
            "id": "monika",
            "name": "Monika",
            "subtitle": "Literature Club president",
            "sprite_image": "monika 1a",
            "fit_mode": "cover",
            "thought": "Monika runs on polish and pressure. She's easy to trust, which is exactly why I keep noticing when she is tired.",
        },
        {
            "id": "mom",
            "name": "Mom",
            "subtitle": "Family",
            "sprite_image": "mom neut",
            "fit_mode": "contain",
            "thought": "She is already thinking three moves ahead about my future, and I do not know whether that helps or corners me.",
        },
        {
            "id": "asahina",
            "name": "Asahina",
            "subtitle": "Younger sister",
            "sprite_image": "asahina neut",
            "fit_mode": "contain",
            "thought": "Asa can turn a favor into a duel, but the poster matters to her more than she wants anyone to notice.",
        },
        {
            "id": "sam",
            "name": "Sam",
            "subtitle": "Asahina's boyfriend",
            "sprite_image": "sam neut",
            "fit_mode": "contain",
            "thought": "Quiet, polite, and harder to read than he looks. Asa relaxes around him in a way she usually refuses to admit.",
        },
        {
            "id": "kotonoha",
            "name": "Kotonoha",
            "subtitle": "Store clerk",
            "sprite_image": "kotonoha neut",
            "fit_mode": "contain",
            "thought": "She makes ordinary transactions feel like they were rehearsed. Useful, distant, and almost impossible to place.",
        },
        {
            "id": "matsuda",
            "name": "Matsuda Akai",
            "subtitle": "Sidewalk collision survivor",
            "sprite_image": "matsuda neut",
            "fit_mode": "contain",
            "thought": "She entered the evening like a curtain went up, demanded my number, and somehow left me curious instead of annoyed.",
        },
        {
            "id": "tsubaki",
            "name": "Tsubaki Kareda",
            "subtitle": "Matsuda's best friend",
            "sprite_image": "tsubaki neut",
            "fit_mode": "contain",
            "thought": "Tsubaki spent most of our first meeting apologizing for someone else. That says more than she probably meant it to.",
        },
    ]

    character_thought_index = dict((entry["id"], entry) for entry in character_thought_catalog)

    def thought_state_list(name):
        value = getattr(store, name, None)
        if value is None:
            value = []
            setattr(store, name, value)
        return value

    def thought_state_dict(name):
        value = getattr(store, name, None)
        if value is None:
            value = {}
            setattr(store, name, value)
        return value

    def mark_character_met(character_id, thought=None):
        met_ids = thought_state_list("met_character_ids")
        if character_id not in met_ids:
            met_ids.append(character_id)

        if thought:
            thought_state_dict("character_thoughts")[character_id] = thought

    def update_character_thought(character_id, thought):
        mark_character_met(character_id)
        thought_state_dict("character_thoughts")[character_id] = thought

    def get_met_character_thought_entries():
        met_ids = thought_state_list("met_character_ids")
        thought_overrides = thought_state_dict("character_thoughts")
        entries = []

        for character_id in met_ids:
            if character_id not in character_thought_index:
                continue

            entry = dict(character_thought_index[character_id])
            entry["thought"] = thought_overrides.get(character_id, entry["thought"])
            entries.append(entry)

        return entries

default met_character_ids = []
default character_thoughts = {}

# Initialize roster on game start
init 5 python:
    init_roster()

# Entrance animation for roster cards (no hover -- handled by style)
transform roster_card_anim(delay=0.0):
    alpha 0.0
    yoffset 25
    subpixel True
    pause delay
    easein_back 0.4 alpha 1.0 yoffset 0

# Frame entrance animation
transform roster_frame_enter:
    on show:
        alpha 0.0
        yoffset -60
        easein_back 0.5 alpha 1.0 yoffset 0
    on hide:
        alpha 1.0
        easeout_quad 0.3 alpha 0.0 yoffset -40

# Detail screen entrance
transform detail_frame_enter:
    on show:
        alpha 0.0
        zoom 0.85
        yoffset 80
        easein_back 0.45 alpha 1.0 zoom 1.0 yoffset 0
    on hide:
        alpha 1.0
        zoom 1.0
        easeout_quad 0.25 alpha 0.0 zoom 0.92

# Slide-in from left/right for detail content
transform detail_slide_left(delay=0.0):
    alpha 0.0
    xoffset -25
    pause delay
    easein_quad 0.4 alpha 1.0 xoffset 0

transform detail_slide_right(delay=0.0):
    alpha 0.0
    xoffset 25
    pause delay
    easein_quad 0.4 alpha 1.0 xoffset 0

transform detail_slide_up(delay=0.0):
    alpha 0.0
    yoffset 15
    pause delay
    easein_quad 0.4 alpha 1.0 yoffset 0

# Roster View Main Screen
screen roster_view_screen():
    modal True
    key "K_ESCAPE" action Hide("roster_view_screen")

    use archive_backdrop

    frame:
        style "archive_shell_frame"
        at roster_frame_enter

        vbox:
            spacing 10

            use archive_header("CHARACTER ROSTER", Hide("roster_view_screen"))

            add Solid("#56d7ff66"):
                xsize 1150
                ysize 2
                xalign 0.5

            null height 2

            viewport:
                style_prefix "archive_sv"
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                xsize 1150
                ysize 560

                vbox:
                    spacing 20
                    xalign 0.5

                    grid 3 3:
                        spacing 25
                        xalign 0.5

                        for idx, char in enumerate(character_roster):
                            $ d = idx * 0.06

                            button:
                                style "roster_card_button"
                                action Show("character_detail_screen", character=char)
                                at roster_card_anim(d)

                                vbox:
                                    spacing 0

                                    # Character sprite area
                                    frame:
                                        xsize 300
                                        ysize 350
                                        background Solid("#07101add")
                                        padding (0, 0)

                                        if char.grayed_out:
                                            add char.sprite_image:
                                                fit char.fit_mode
                                                xalign 0.5
                                                yalign 1.0
                                                matrixcolor BrightnessMatrix(0.0) * SaturationMatrix(0.0)
                                        else:
                                            add char.sprite_image:
                                                fit char.fit_mode
                                                xalign 0.5
                                                yalign 1.0

                                    # Name plate
                                    frame:
                                        background Solid("#07111dcc")
                                        xsize 300
                                        padding (10, 6)

                                        text char.name style "roster_card_name"

                        # Pad remaining cells to fill the 3x3 grid
                        for _pad in range(9 - len(character_roster)):
                            null xysize (300, 400)

                    null height 20

# Character Detail Screen
screen character_detail_screen(character):
    modal True
    zorder 100
    key "K_ESCAPE" action Hide("character_detail_screen")

    add Solid("#000000") at transform:
        alpha 0.0
        linear 0.25 alpha 0.85

    # Pre-compute display strings outside the screen tree
    $ _height_str = character.get_height_display()
    $ _weight_str = character.get_weight_display()
    $ _chest_str = character.get_chest_display()
    $ _status_str = character.is_dead
    $ _build_label = "Build" if character.manual_exception else "Chest"
    $ _build_value = character.manual_exception if character.manual_exception else _chest_str
    $ _detail_stats = [("Full Name", character.full_name), ("Age", character.age), ("Height", _height_str), ("Weight", _weight_str), (_build_label, _build_value), ("Status", _status_str)]
    $ _detail_traits = [("Likes", character.likes), ("Dislikes", character.dislikes)]

    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 600
        background Solid("#050811e8")
        padding (25, 20)
        at detail_frame_enter

        vbox:
            spacing 14

            use archive_header(character.full_name, Hide("character_detail_screen"), "Close")

            add Solid("#56d7ff66"):
                xsize 850
                ysize 2
                xalign 0.5

            # Content area
            viewport:
                style_prefix "archive_sv"
                scrollbars "vertical"
                mousewheel True
                draggable True
                xsize 850
                ysize 480

                vbox:
                    spacing 16
                    xsize 830

                    # Top section: sprite + stats side by side
                    hbox:
                        spacing 18

                        # Character sprite
                        frame:
                            style "character_detail_portrait_frame"
                            padding (0, 0)
                            at detail_slide_left(0.1)

                            if character.grayed_out:
                                add character.sprite_image:
                                    fit character.fit_mode
                                    xalign 0.5
                                    yalign 1.0
                                    matrixcolor BrightnessMatrix(0.0) * SaturationMatrix(0.0)
                            else:
                                add character.sprite_image:
                                    fit character.fit_mode
                                    xalign 0.5
                                    yalign 1.0

                        # Character stats
                        frame:
                            style "character_detail_stats_panel"
                            at detail_slide_right(0.15)

                            vbox:
                                spacing 10

                                hbox:
                                    spacing 10
                                    yalign 0.5

                                    add Solid("#56d7ff"):
                                        xsize 4
                                        ysize 22
                                        yalign 0.5

                                    text "Profile" style "character_detail_section"

                                add Solid("#56d7ff24"):
                                    xsize 472
                                    ysize 1

                                vbox:
                                    spacing 7

                                    for _label, _value in _detail_stats:
                                        hbox:
                                            spacing 16
                                            xsize 472
                                            yalign 0.5

                                            text _label style "character_detail_stat_label"
                                            text "[_value]" style "character_detail_stat_value"

                                add Solid("#56d7ff16"):
                                    xsize 472
                                    ysize 1

                                vbox:
                                    spacing 7

                                    for _label, _value in _detail_traits:
                                        hbox:
                                            spacing 16
                                            xsize 472
                                            yalign 0.5

                                            text _label style "character_detail_stat_label"
                                            text "[_value]" style "character_detail_stat_value"

                    # Description section
                    frame:
                        style "character_detail_desc_panel"
                        at detail_slide_up(0.3)

                        vbox:
                            spacing 10

                            hbox:
                                spacing 10
                                yalign 0.5

                                add Solid("#56d7ff"):
                                    xsize 4
                                    ysize 22
                                    yalign 0.5

                                text "Description" style "character_detail_section"

                            add Solid("#56d7ff24"):
                                xsize 798
                                ysize 1

                            text character.description style "character_detail_desc"


screen character_thoughts_screen():
    modal True
    zorder 215
    key "K_ESCAPE" action Hide("character_thoughts_screen")

    $ _thought_entries = get_met_character_thought_entries()

    use archive_backdrop

    frame:
        style "archive_shell_frame"
        at roster_frame_enter

        vbox:
            spacing 10

            use archive_header("CURRENT READS", Hide("character_thoughts_screen"), "Close")

            add Solid("#56d7ff66"):
                xsize 1150
                ysize 2
                xalign 0.5

            null height 2

            viewport:
                style_prefix "archive_sv"
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                xsize 1150
                ysize 560

                vbox:
                    spacing 14
                    xfill True

                    if not _thought_entries:
                        frame:
                            style "thought_entry_frame"

                            text "No one notable yet." style "thought_body":
                                xalign 0.5
                                yalign 0.5
                    else:
                        for entry in _thought_entries:
                            frame:
                                style "thought_entry_frame"

                                hbox:
                                    spacing 18

                                    frame:
                                        style "thought_sprite_frame"

                                        add entry["sprite_image"]:
                                            fit entry["fit_mode"]
                                            xalign 0.5
                                            yalign 1.0

                                    vbox:
                                        spacing 8
                                        yalign 0.5
                                        xsize 900

                                        text entry["name"] style "thought_name"
                                        text entry["subtitle"] style "thought_subtitle"

                                        add Solid("#56d7ff44"):
                                            xsize 880
                                            ysize 1

                                        text entry["thought"] style "thought_body"

# Styles
style roster_title:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 36
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]


style roster_card_button:
    xysize (300, 400)
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (0, 0)

style roster_card_name:
    size 22
    color "#dff8ff"
    bold True
    xalign 0.5
    text_align 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style character_detail_title:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 38
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style character_detail_section:
    size 22
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style character_detail_portrait_frame:
    xsize 300
    ysize 360
    background Solid("#07101add")
    padding (0, 0)

style character_detail_stats_panel:
    xsize 512
    yminimum 360
    background Solid("#07111dcc")
    padding (16, 14, 16, 14)

style character_detail_info:
    size 19
    color "#dff8ff"
    outlines [(1, "#02040b", 0, 0)]

style character_detail_stat_label:
    size 14
    color "#8fb6c5"
    xsize 112
    xalign 0.0
    text_align 0.0
    outlines [(1, "#02040b", 0, 0)]

style character_detail_stat_value:
    size 18
    color "#dff8ff"
    xsize 344
    xalign 0.0
    text_align 0.0
    outlines [(1, "#02040b", 0, 0)]

style character_detail_desc_panel:
    xsize 830
    background Solid("#07111dcc")
    padding (16, 14, 16, 16)

style character_detail_desc:
    size 18
    color "#c9d8e1"
    text_align 0.0
    line_spacing 4
    xmaximum 798
    outlines [(1, "#02040b", 0, 0)]

style thought_entry_frame:
    xsize 1128
    yminimum 172
    background Solid("#07111dcc")
    padding (16, 14, 16, 14)

style thought_sprite_frame:
    xsize 118
    ysize 144
    background Solid("#07101add")
    padding (0, 0)

style thought_name:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 25
    color "#f4fbff"
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style thought_subtitle:
    font gui.interface_font
    size 14
    color "#8fb6c5"
    outlines [(1, "#02040b", 0, 0)]

style thought_body:
    font gui.default_font
    size 18
    color "#c9d8e1"
    line_spacing 1
    xmaximum 880
    outlines [(1, "#02040b", 0, 0)]

# Label to call roster view
label roster_view:
    call screen roster_view_screen
    return
