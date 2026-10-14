# Credits menu: credits_sections groups CreditEntry attribution records into
# CreditSection categories. ShowMenu("credits_menu") opens the shared menu screen.
# Section accents drive the sidebar and folio rules; details supply extra credit
# lines. Keep attribution data with its entry when changing the presentation.

init python:
    # One credited item: a title, an attribution line, and optional detail lines.
    class CreditEntry:
        def __init__(self, title, credit, details=None):
            self.title = title
            self.credit = credit
            self.details = details or []

    # A group of CreditEntry cards under a heading, with an accent color.
    class CreditSection:
        def __init__(self, title, subtitle, accent, entries):
            self.title = title
            self.subtitle = subtitle
            self.accent = accent
            self.entries = entries

    def credits_scroll_top(adjustment):
        """Return the independent content pane to its first credit card."""
        adjustment.change(0)
        return None

    def credits_nav_scroll_visible(adjustment, index):
        """Keep a keyboard-selected 54px section row inside its viewport."""
        row_top = index * 62
        row_bottom = row_top + 54
        view_top = adjustment.value
        if row_top < view_top:
            adjustment.change(row_top)
        elif row_bottom > view_top + 352:
            adjustment.change(row_bottom - 352)
        return None

    # The full credits dataset. Order here = order in the sidebar/content pane.
    credits_sections = [
        CreditSection(
            "Project",
            "Core production",
            "#56d7ff",
            [
                CreditEntry(
                    "ENTER-M",
                    "Created, written, designed, and implemented by L4w1i3t.",
                    ["Version 0.1.0", "Original mod content, direction, UI, systems, and integration."],
                ),
                CreditEntry(
                    "Matsu'Py Visual Novel Engine",
                    "Engine forked from Ren'Py, by the Ren'Py project.",
                    ["Project currently built on Matsu'Py, a fork of Ren'Py 8.1.1."],
                ),
                CreditEntry(
                    "Doki Doki Literature Club",
                    "Created and published by Team Salvato.",
                    ["Base game, original characters, original assets, and original code foundation."],
                ),
            ],
        ),
        CreditSection(
            "Systems",
            "Menus and gameplay tools",
            "#ff4968",
            [
                CreditEntry("Archive Hub", "Custom archive menu and unlock flow by L4w1i3t.", ["Roster, CG Gallery, Music Room, Side Stories, Lost Records, and Achievements access.", "Shared archive chrome, readouts, portrait crops, and scanline styling."]),
                CreditEntry("Roster View", "Addon code, profile data, thoughts list, and archive presentation by L4w1i3t."),
                CreditEntry("CG Gallery", "Gallery catalog, fullscreen viewer, and archive integration by L4w1i3t."),
                CreditEntry("Music Room", "Music browser, playback controls, play modes, shuffle engine, and CG visualization by L4w1i3t."),
                CreditEntry("Side Stories", "Story catalog, unlock logic, and story archive UI by L4w1i3t."),
                CreditEntry("Lost Records", "Record catalog and archive menu by L4w1i3t."),
                CreditEntry("Achievements", "Tiered completion checklist, unlock engine, and toast system by L4w1i3t.", ["Derived and explicit trophies for the currently playable story and modes."]),
                CreditEntry("Arcade Hub", "Cabinet front-end, jewel-case shelf, and mode launcher by L4w1i3t.", ["Lets a beaten mode be replayed on its own, outside the story."]),
                CreditEntry("Phone System", "Contacts, text messaging, calls, video-call UI, and idle conversations by L4w1i3t."),
                CreditEntry("Calendar System", "Calendar state, date display, day-change sequence, and calendar menu by L4w1i3t."),
                CreditEntry("ID Card", "Name and birthdate entry flow by L4w1i3t."),
                CreditEntry("NieR-Style Text Adventure", "Text adventure presentation system by L4w1i3t.", ["Inspired by NieR's forest text-adventure format."]),
                CreditEntry("Speaker Focus", "Automatic sprite spotlighting and listener dimming by L4w1i3t.", ["Player-configurable in Settings."]),
                CreditEntry("Interface Choreography", "Menu transitions, pause-menu console chrome, and scene transitions by L4w1i3t."),
                CreditEntry("Scene Atmosphere and FX", "Lighting grade, camera work, shaders, and effects library by L4w1i3t."),
                CreditEntry("Anime OP Replay", "Opening sequence direction, timing, image choreography, and archive replay hook by L4w1i3t."),
                CreditEntry("Next Time Trailer", "Episode-preview sequence by L4w1i3t."),
            ],
        ),
        CreditSection(
            "Modes",
            "Fights, set pieces, and Arcade originals",
            "#8a5cff",
            [
                CreditEntry("Ontological Seer", "Press-turn boss battle designed and implemented by L4w1i3t.", ["Turn economy inspired by the Shin Megami Tensei / Persona press-turn system."]),
                CreditEntry("Ontological Seer: Id", "Superboss rematch designed and implemented by L4w1i3t.", ["Genre-shift phases: bullet hell, typing, and quiz microgames."]),
                CreditEntry("A Fine Date", "Anti-dating-sim QTE mode designed and implemented by L4w1i3t.", ["The only way to win is to keep saying no."]),
                CreditEntry("Embodiment of Violet Ink", "Danmaku boss stage designed and implemented by L4w1i3t.", ["Bullet-pattern grammar inspired by the Touhou Project series.", "Kotonoha character by Cyrke."]),
                CreditEntry("The Unwritten Act", "SOUL box duel designed and implemented by L4w1i3t.", ["Box-fight format inspired by Undertale and Deltarune."]),
                CreditEntry("MATSUCOM Originals", "Arcade cabinet framework and original minigames by L4w1i3t.", ["Ouroboros Protocol - grid survival", "Peer Review - brick breaker", "Intake - falling blocks", "Containment Sweep - deduction", "Board Meeting - chess", "Each is a story-free take on a classic arcade genre."]),
            ],
        ),
        CreditSection(
            "Writing",
            "Story content",
            "#d39a55",
            [
                CreditEntry("Main Story", "Written by L4w1i3t."),
                CreditEntry("Matsuda Story - Dead Fantasy", "Written by L4w1i3t."),
                CreditEntry("Matsuda Story - Ontological Seer", "Written by L4w1i3t."),
                CreditEntry("Tsubaki Story - Heads", "Written by L4w1i3t.", ["One gothic story told twice; this is the mender's manuscript."]),
                CreditEntry("Tsubaki Story - Tails", "Written by L4w1i3t.", ["The same events as told by the one who was mended."]),
                CreditEntry("Asahina Story - Hina's World", "Written by L4w1i3t.", ["Inspired by the Lacey Games horror series."]),
                CreditEntry("Sam Story - Purgatorium", "Written by L4w1i3t."),
                CreditEntry("Kotonoha Story - The Girl with Every Face", "Written by L4w1i3t."),
                CreditEntry("Kotonoha Story - The Void Hunter", "Written by L4w1i3t."),
                CreditEntry("Lost Records", "Legacy-story archive concept by L4w1i3t.", ["The Answer", "SVHS TAP-05052022", "Mika: A DDLC Short Story, in original and rewritten tellings"]),
            ],
        ),
        CreditSection(
            "Characters",
            "Design and sprites",
            "#b875ff",
            [
                CreditEntry("Matsuda", "Character by L4w1i3t and Matsuda Akai.", ["Current sprite asset is a placeholder."]),
                CreditEntry("Tsubaki", "Character and concept by L4w1i3t.", ["Current sprite assets are placeholders."]),
                CreditEntry("Asahina", "Character and concept by L4w1i3t.", ["Current sprite asset is a placeholder."]),
                CreditEntry("Sam / Masayami", "Character and concept by L4w1i3t.", ["Current sprite asset is a placeholder."]),
                CreditEntry("Himeko / Mom", "Character and concept by L4w1i3t.", ["Current sprite asset is a placeholder."]),
                CreditEntry("Player / MC", "Character and concept by L4w1i3t.", ["Current sprite asset is a placeholder."]),
                CreditEntry("Purgatorium Girl", "Character and scenario concept by L4w1i3t.", ["Additional sprite variants for story use."]),
                CreditEntry("Kotonoha", "Character, sprites, and concept by Cyrke.", ["Custom implementation and story usage by L4w1i3t."]),
                CreditEntry("Original DDLC Cast", "Characters and sprites by Team Salvato.", ["Monika, Sayori, Natsuki, Yuri, and original base game assets."]),
            ],
        ),
        CreditSection(
            "Visuals",
            "Art, backgrounds, CGs, and UI",
            "#6df2a2",
            [
                CreditEntry("Vanilla DDLC Assets", "Team Salvato.", ["Original backgrounds, sprites, CGs, UI assets, and effects."]),
                CreditEntry("Cold Open", "Presenter-logo and content-warning sequence by L4w1i3t.", ["Presenter marks belong to their respective owners; the presentation around them is original."]),
                CreditEntry("Opening CG Sequence", "Image sequence and presentation by L4w1i3t.", ["Current OP images are custom placeholder assets in addons/Sick Ass Anime OP."]),
                CreditEntry("Arcade Box Art", "Creative direction, title treatment, editing, and integration by L4w1i3t; base imagery generated with OpenAI's built-in image-generation tool.", ["Classic-edition covers use a restrained 16-bit print treatment; The Unwritten Act preserves its existing illustration in an optimized display copy."]),
                CreditEntry("Custom CGs", "Custom placeholder CG assets prepared by L4w1i3t.", ["campaign, ransom, hell, hell2, lies, everyface, and voidhunter."]),
                CreditEntry("Custom Backgrounds", "Creative direction, selection, editing, and integration by L4w1i3t; base imagery generated with OpenAI's built-in image-generation tool.", ["House, residential, city, movie-theater, and library location families, including lighting and weather variants."]),
                CreditEntry("Uncle Mugen", "Background assets.", ["park_winter, bus_interior, grassy, and river."]),
                CreditEntry("Fanmade DDLC Background Assets", "Artist currently unknown.", ["doordark and doorday."]),
                CreditEntry("L4w1i3t", "Custom background and UI integration.", ["corridor_bootleg, menu styling, archive and binder styling, screen layouts, and asset integration."]),
                CreditEntry("Elduator / Erika B. Hall", "town_day background asset."),
                CreditEntry("Lornn", "fields background asset."),
                CreditEntry("Additional Background Placeholders", "Attribution review pending.", ["Remaining custom backgrounds and dump-folder visual placeholders should be verified before release."]),
                CreditEntry("Fonts", "SF Automaton Extended, NovaSquare, Galldr, and Myanmar font assets.", ["Packaged in assets/fonts. Confirm license text before public distribution."]),
            ],
        ),
        CreditSection(
            "Music",
            "Tracks and music room library",
            "#75f7ff",
            [
                CreditEntry("TEMP", ["TEMP"]),
            ],
        ),
        CreditSection(
            "Sound",
            "Effects and interface audio",
            "#f3d16b",
            [
                CreditEntry("Base DDLC Sound Effects", "Team Salvato.", ["closet, page, fall, heartbeat, and vanilla interface sounds."]),
                CreditEntry("Custom SFX", "Provided by L4w1i3t, Toby Fox, or stock libraries.", ["dooropen, doorclose, ac, hellbassboost, hover, select, snap, tick, vinyl, rain, clock, beep, and related UI sounds."]),
                CreditEntry("Matsuda Boss Fight UI SFX", "Generated in-project as synthetic interface and combat cues.", ["assets/audio/sfx/msbf/*.wav"]),
                CreditEntry("Phone Audio", "Prepared for custom phone UI.", ["Current phone sound definitions are placeholders until final SFX are assigned."]),
            ],
        ),
        CreditSection(
            "Backers",
            "Funding support",
            "#f4fbff",
            [
                CreditEntry("JQilinGaming", "Playtesting, publicity, content creation, writing assistance."),
                CreditEntry("TuneEternal", "Publicity, playtesting, writing assistance."),
                CreditEntry("Iris Candy", "Publicity, playtesting, writing assistance."),
                CreditEntry("HoldThisL", "Funding support, writing assistance, playtesting."),
                CreditEntry("RJTCougar", "Publicity, playtesting, writing assistance."),
            ],
        ),
        CreditSection(
            "Thanks",
            "Community and support",
            "#f4fbff",
            [
                CreditEntry("The DDLC Modding Community", "Tools, references, discussion, and support."),
                CreditEntry("Players and Testers", "Everyone who played, reported issues, or supported development."),
                CreditEntry("Attribution Notes", "Credits reflect the known project state in source files.", ["Any placeholder asset marked attribution review pending should be replaced, confirmed, or removed before public release."]),
            ],
        ),
    ]

# A print palette is applied by the view; historical attribution data remains
# untouched, including its independent section definitions and ordering.
define CREDITS_PRINT_ACCENTS = ("#9c7442", "#367069", "#765974", "#926737", "#7b5b71", "#4e7664", "#3c7579", "#947a3d", "#80694d", "#80694d", "#80694d")
define CREDITS_PRINT_TAB = Frame("assets/gui/menu/illustrated/credits/section_tab.svg", 12, 10, 12, 10)
define CREDITS_PRINT_TAB_SELECTED = Frame("assets/gui/menu/illustrated/credits/section_tab_selected.svg", 12, 10, 12, 10)

# Entrance animations (cosmetic): panels slide/fade in; cards stagger in.
transform credits_panel_enter(delay=0.0, xoff=0, yoff=18):
    alpha 0.0
    xoffset xoff
    yoffset yoff
    subpixel True
    pause delay
    easeout_quad 0.32 alpha 1.0 xoffset 0 yoffset 0

transform credits_card_enter(delay=0.0):
    alpha 0.0
    yoffset 8
    subpixel True
    pause delay
    easeout_quad 0.18 alpha 1.0 yoffset 0


# A local, one-shot folio rule. Passing the selected section as the key creates
# a fresh transform when the reader changes sections, without borrowing any of
# Archive's transforms or introducing an ambient redraw loop.
transform credits_rule_enter(key=0):
    subpixel True
    xanchor 0.0
    xzoom 0.0
    easeout_cubic 0.36 xzoom 1.0

screen credits_menu():
    tag menu

    # selected_section: which sidebar entry is active (screen-local state).
    default selected_section = 0
    default credits_content_yadj = ui.adjustment()
    default credits_nav_yadj = ui.adjustment()

    # Resolve the currently-selected section + total count for the header/counter.
    $ section = credits_sections[selected_section]
    $ section_count = len(credits_sections)
    $ credits_ink = CREDITS_PRINT_ACCENTS[selected_section % len(CREDITS_PRINT_ACCENTS)]

    add illustrated_menu_backdrop("credits")

    key "game_menu" action Return()
    key "K_ESCAPE" action Return()

    if selected_section > 0:
        key "K_LEFT" action [
            SetScreenVariable("selected_section", selected_section - 1),
            Function(credits_scroll_top, credits_content_yadj),
            Function(credits_nav_scroll_visible, credits_nav_yadj, selected_section - 1),
        ]
    if selected_section < section_count - 1:
        key "K_RIGHT" action [
            SetScreenVariable("selected_section", selected_section + 1),
            Function(credits_scroll_top, credits_content_yadj),
            Function(credits_nav_scroll_visible, credits_nav_yadj, selected_section + 1),
        ]

    fixed:
        xysize (1280, 720)

        frame:
            style "credits_shell"

            hbox:
                spacing 0

                # --- LEFT: corner mark + folio navigation + Return -----------
                frame:
                    style "credits_sidebar"
                    at credits_panel_enter(0.02, -24, 0)

                    vbox:
                        spacing 10

                        hbox:
                            spacing 10
                            xsize 282
                            ysize 104

                            add illustrated_menu_motif("credits", 96, 106):
                                xsize 104
                                ysize 104

                            frame:
                                style "credits_title_block"

                                vbox:
                                    spacing 3
                                    yalign 0.5

                                    text _("PRODUCTION FOLIO") style "credits_screen_kicker"
                                    text _("Credits") style "credits_screen_title"
                                    text _("[section_count] sections") style "credits_screen_meta"

                        viewport:
                            style_prefix "credits_room_sv"
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            yadjustment credits_nav_yadj
                            xsize 282
                            ysize 352

                            vbox:
                                spacing 8
                                xfill True

                                for idx, item index item.title in enumerate(credits_sections):
                                    button:
                                        style "credits_nav_button"
                                        xfill True
                                        ysize 54
                                        id ("credits_section_%d" % idx)
                                        if idx == selected_section:
                                            background CREDITS_PRINT_TAB_SELECTED
                                            hover_background CREDITS_PRINT_TAB_SELECTED
                                        else:
                                            background CREDITS_PRINT_TAB
                                            hover_background CREDITS_PRINT_TAB_SELECTED

                                        action [
                                            SetScreenVariable("selected_section", idx),
                                            Function(credits_scroll_top, credits_content_yadj),
                                            Function(credits_nav_scroll_visible, credits_nav_yadj, idx),
                                        ]

                                        hbox:
                                            spacing 10
                                            yalign 0.5

                                            add Solid(IM_GOLD if idx == selected_section else IM_MUTED):
                                                xsize 4
                                                ysize 34
                                                yalign 0.5

                                            vbox:
                                                spacing 1
                                                yalign 0.5
                                                xsize 232

                                                text item.title style "credits_nav_title"
                                                text item.subtitle style "credits_nav_subtitle"

                        textbutton _("Return"):
                            style "credits_return_button"
                            id "credits_return"
                            action Return()

                add "assets/gui/menu/illustrated/credits/binding.svg":
                    xsize 20
                    ysize 628

                # --- RIGHT: selected section's title + scrollable entry cards -
                frame:
                    style "credits_content"
                    at credits_panel_enter(0.06, 24, 0)

                    vbox:
                        spacing 16

                        hbox:
                            xfill True
                            ysize 72

                            vbox:
                                spacing 3
                                yalign 0.5
                                xsize 620

                                text section.title style "credits_section_title"
                                text section.subtitle style "credits_section_subtitle"

                            null width 1 xfill True

                            frame:
                                yalign 0.5
                                xsize 122
                                ysize 34
                                padding (10, 5)
                                background CREDITS_PRINT_TAB

                                hbox:
                                    spacing 7
                                    xalign 0.5
                                    yalign 0.5

                                    add Solid(IM_GOLD) xysize (6, 6) yalign 0.5
                                    text _("{:02d} of {:02d}").format(selected_section + 1, section_count):
                                        style "credits_counter"
                                        yalign 0.5

                        add Solid(credits_ink):
                            xsize 780
                            ysize 3
                            at credits_rule_enter(selected_section)

                        viewport:
                            style_prefix "credits_room_sv"
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            pagekeys True
                            id "credits_content_viewport"
                            yadjustment credits_content_yadj
                            xsize 800
                            ysize 470

                            vbox:
                                spacing 12
                                xsize 780

                                for entry_idx, entry index (section.title + "::" + entry.title) in enumerate(section.entries):
                                    $ card_delay = min(entry_idx, 7) * 0.025

                                    frame:
                                        style "credits_entry_card"
                                        at credits_card_enter(card_delay)

                                        vbox:
                                            spacing 0
                                            xfill True

                                            add Solid(credits_ink + "58"):
                                                xsize 740
                                                ysize 1

                                            frame:
                                                background None
                                                xfill True
                                                padding (18, 12, 14, 14)

                                                vbox:
                                                    spacing 6
                                                    xfill True

                                                    text entry.title style "credits_entry_title"
                                                    text entry.credit style "credits_entry_credit"

                                                    if entry.details:
                                                        vbox:
                                                            spacing 4

                                                            for line_idx, line index (section.title + "::" + entry.title + "::" + str(line_idx)) in enumerate(entry.details):
                                                                text line style "credits_entry_detail"

    # A printed gold rule closes the programme cover and its reading page.
    add Solid("#e8dbc536") xpos 46 ypos 46 xysize (1168, 1)
    add Solid(IM_GOLD) xpos 46 ypos 46 xysize (126, 3) at credits_rule_enter
    add Solid("#e8dbc528") xpos 46 ypos 673 xysize (1168, 1)

# =============================================================================
# STYLES -- a production programme with a clear paper reading surface.
# `is empty` bases keep every panel's geometry explicit and predictable.
# =============================================================================
style credits_shell is empty:
    xpos 46
    ypos 46
    xsize 1168
    ysize 628
    background IM_PAPER_PANEL
    padding (0, 0)

style credits_sidebar is empty:
    xsize 318
    ysize 628
    background IM_DARK_PANEL
    padding (18, 18)

style credits_title_block is empty:
    xsize 168
    ysize 104
    background None
    padding (12, 10)

style credits_screen_kicker is room_menu_kicker:
    size 8
    color IM_GOLD
    xmaximum 144

style credits_screen_title is room_menu_heading:
    size 25
    xmaximum 144

style credits_screen_meta is room_menu_meta:
    size 9
    color ROOM_MENU_MUTED
    xmaximum 144

style credits_nav_button is room_menu_button:
    ysize 54
    padding (12, 7)

style credits_nav_title is room_menu_body:
    size 17
    color ROOM_MENU_INK
    xmaximum 232

style credits_nav_subtitle is room_menu_meta:
    size 9
    color ROOM_MENU_MUTED
    xmaximum 232

style credits_return_button is room_menu_button:
    background IM_RETURN_IDLE
    hover_background IM_RETURN_HOVER
    xsize 282
    ysize 42
    padding (15, 8)

style credits_return_button_text is room_menu_button_text:
    size 18
    xalign 0.5
    text_align 0.5

style credits_content is empty:
    xsize 830
    ysize 628
    background None
    padding (16, 20)

style credits_section_title is room_menu_heading:
    size 36
    color IM_INK
    outlines []
    xmaximum 620

style credits_section_subtitle is room_menu_meta:
    size 13
    color "#746756"
    outlines []
    xmaximum 620

style credits_counter is room_menu_meta:
    size 11
    color IM_PAPER

style credits_entry_card is empty:
    xfill True
    yminimum 78
    background None
    padding (0, 0)

style credits_entry_title is room_menu_heading:
    size 22
    color IM_INK
    outlines []
    xmaximum 720

style credits_entry_credit is room_menu_body:
    size 16
    color "#41484a"
    outlines []
    xmaximum 720
    line_spacing 2

style credits_entry_detail is room_menu_meta:
    size 12
    color "#6c675e"
    outlines []
    xmaximum 720
    line_spacing 2

# Credits-local scrollbar chrome. Archive's style family is deliberately not
# inherited or modified, so the two menus can evolve independently.
style credits_room_sv_vscrollbar:
    xsize 7
    base_bar Frame(Solid("#8e796436"), 0, 0, 0, 0)
    thumb Frame(Solid("#aa8652"), 2, 2, 2, 2)
    unscrollable "hide"
