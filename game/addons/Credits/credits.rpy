# =============================================================================
# credits.rpy  --  CREDITS MENU (main-menu feature)
# =============================================================================
#
# WHAT THIS FILE PROVIDES
#   A two-pane credits browser: a left sidebar listing sections (Project,
#   Systems, Writing, Characters, Visuals, Music, Sound, Thanks), and a right
#   content pane showing the selected section's entries. Pure data + one screen.
#
# HOW IT IS REACHED
#   - Main menu / game menu "Credits" button -> ShowMenu("credits_menu")
#     (game/screens.rpy lines ~425 and ~527). `tag menu` => it slots into the
#     menu screen group like the other menu screens.
#
# DATA MODEL (credits_sections, built in init python below)
#   credits_sections = [ CreditSection(title, subtitle, accent, [CreditEntry...]) ]
#     CreditEntry(title, credit, details=None)
#       title   : the credited item / person (bold heading on the card)
#       credit  : the attribution line
#       details : optional list of extra lines (track lists, notes, caveats)
#     CreditSection.accent : the section's highlight color (sidebar pip + rule).
#   To add a credit: append a CreditEntry to the right section's list; to add a
#   whole category: append a CreditSection. Nothing else needs editing.
#
# THEME NOTE
#   This screen belongs to the domestic menu family: the same painted evening
#   room, selector assets, and warm editorial palette as the title screen. Its
#   folio chrome and scrollbar are local so Archive keeps its own identity.
# =============================================================================

# Credits Menu Addon
# Standalone screen so it can be opened cleanly from the main menu.

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
                CreditEntry("Doki Doki Literature Club OST", "Dan Salvato.", ["Base game music and original DDLC audio."]),
                CreditEntry("NieR Replicant ver. 1.22...", "Square Enix / Keiichi Okabe.", ["Grandma", "The Incomplete Stone", "City of Commerce", "Fleeting Words - Family", "Snow in Summer", "Song of the Ancients - Devola / Popola / Hollow Dreams", "This Dream", "Temple of Drifting Sands", "Wretched Automatons", "Blu Bird"]),
                CreditEntry("San-Z Studio", "Music Room tracks.", ["The Way Home", "60% Daily Fantasy", "60% Fantasy Passion", "60% Daily Leisure", "60% Daily", "60% Fantasy Serenity"]),
                CreditEntry("Toby Fox", "Deltarune and related placeholder tracks.", ["13 AM", "12 AM", "Dump"]),
                CreditEntry("Intelligent Systems / Nintendo", "Fire Emblem: Radiant Dawn music.", ["Hymn of the Righteous", "Proud Flight", "The Devoted"]),
                CreditEntry("Spike Chunsoft / Masafumi Takada", "Danganronpa series music.", ["Beautiful Days (16-bit)", "All Star Apologies (16-bit)"]),
                CreditEntry("Torchkas", "Can You Feel.", ["Main menu theme."]),
                CreditEntry("Menu and Mode Themes", "Attribution review pending.", ["Archive theme, Arcade hub theme, and the per-mode tracks.", "Confirm each source before public release."]),
                CreditEntry("Opening Theme", "Attribution review pending.", ["Working title: ENTER M Opening Theme. Final title and source credit pending confirmation."]),
                CreditEntry("Additional Dump-Folder Tracks", "Attribution review pending.", ["A Flower of Melancholy", "An Empty Bliss Beyond This World", "Clair de Lune", "Darkness Space", "December Quartet", "Hidden Sea Buried Deep", "Holiday Mood", "It's Fruitful and Ephemeral", "Neon Purple", "Night Run Away", "Oh How My World Breaks", "Piano Sinking in Water", "Rain Lovers", "Serious Mentality", "Sprouting Kogane", "Summer Fog", "Take a Walk With a Pug"]),
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

    add "enter_m_main_menu_bg" at room_menu_bg_arrive
    add Solid("#04090c73")

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

                            add "assets/gui/logo.png":
                                fit "contain"
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
                                        if idx == selected_section:
                                            background ROOM_MENU_SELECTOR_SELECTED
                                            hover_background ROOM_MENU_SELECTOR_SELECTED
                                        else:
                                            background ROOM_MENU_SELECTOR_IDLE
                                            hover_background ROOM_MENU_SELECTOR_HOVER

                                        action [
                                            SetScreenVariable("selected_section", idx),
                                            Function(credits_scroll_top, credits_content_yadj),
                                            Function(credits_nav_scroll_visible, credits_nav_yadj, idx),
                                        ]

                                        hbox:
                                            spacing 10
                                            yalign 0.5

                                            add Solid(item.accent):
                                                xsize 4
                                                ysize 34
                                                yalign 0.5

                                            vbox:
                                                spacing 1
                                                yalign 0.5
                                                xsize 244

                                                text item.title style "credits_nav_title"
                                                text item.subtitle style "credits_nav_subtitle"

                        textbutton _("Return"):
                            style "credits_return_button"
                            action Return()

                add Solid("#e8dbc536"):
                    xsize 2
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
                                xsize 650

                                text section.title style "credits_section_title"
                                text section.subtitle style "credits_section_subtitle"

                            null width 1 xfill True

                            frame:
                                yalign 0.5
                                xsize 122
                                ysize 34
                                padding (10, 5)
                                background ROOM_MENU_SELECTOR_IDLE

                                hbox:
                                    spacing 7
                                    xalign 0.5
                                    yalign 0.5

                                    add Solid(section.accent) xysize (6, 6) yalign 0.5
                                    text _("{:02d} of {:02d}").format(selected_section + 1, section_count):
                                        style "credits_counter"
                                        yalign 0.5

                        add Solid(section.accent):
                            xsize 780
                            ysize 3
                            at credits_rule_enter(selected_section)

                        viewport:
                            style_prefix "credits_room_sv"
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            pagekeys True
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

                                            add Solid(section.accent):
                                                xsize 780
                                                ysize 3

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

    # Paper/coral rules sit over the folio plate, replacing the old console
    # brackets with one quiet editorial edge.
    add Solid("#e8dbc536") xpos 46 ypos 46 xysize (1168, 1)
    add Solid(ROOM_MENU_CORAL) xpos 46 ypos 46 xysize (126, 3) at credits_rule_enter
    add Solid("#e8dbc528") xpos 46 ypos 673 xysize (1168, 1)

# =============================================================================
# STYLES -- a quiet production folio over the domestic menu background.
# `is empty` bases keep every panel's geometry explicit and predictable.
# =============================================================================
style credits_shell is empty:
    xpos 46
    ypos 46
    xsize 1168
    ysize 628
    background Solid(ROOM_MENU_PANEL)
    padding (0, 0)

style credits_sidebar is empty:
    xsize 318
    ysize 628
    background Solid("#091419eb")
    padding (18, 18)

style credits_title_block is empty:
    xsize 168
    ysize 104
    background Solid("#172124d9")
    padding (12, 10)

style credits_screen_kicker is room_menu_kicker:
    size 8
    color ROOM_MENU_OCHRE
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
    xmaximum 244

style credits_nav_subtitle is room_menu_meta:
    size 9
    color ROOM_MENU_MUTED
    xmaximum 244

style credits_return_button is room_menu_button:
    xsize 282
    ysize 42
    padding (15, 8)

style credits_return_button_text is room_menu_button_text:
    size 18
    xalign 0.5
    text_align 0.5

style credits_content is empty:
    xsize 848
    ysize 628
    background Solid(ROOM_MENU_PANEL_SOFT)
    padding (24, 20)

style credits_section_title is room_menu_heading:
    size 34
    xmaximum 650

style credits_section_subtitle is room_menu_meta:
    size 13
    color ROOM_MENU_PAPER
    xmaximum 650

style credits_counter is room_menu_meta:
    size 11
    color ROOM_MENU_TEAL

style credits_entry_card is empty:
    xfill True
    yminimum 78
    background Solid("#162125e8")
    padding (0, 0)

style credits_entry_title is room_menu_heading:
    size 20
    xmaximum 720

style credits_entry_credit is room_menu_body:
    size 15
    color ROOM_MENU_PAPER
    xmaximum 720
    line_spacing 2

style credits_entry_detail is room_menu_meta:
    size 12
    color ROOM_MENU_MUTED
    xmaximum 720
    line_spacing 2

# Credits-local scrollbar chrome. Archive's style family is deliberately not
# inherited or modified, so the two menus can evolve independently.
style credits_room_sv_vscrollbar:
    xsize 7
    base_bar Frame(Solid("#26332f"), 0, 0, 0, 0)
    thumb Frame(Solid(ROOM_MENU_CORAL), 2, 2, 2, 2)
    unscrollable "hide"
