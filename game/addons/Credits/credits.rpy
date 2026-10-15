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
            "Where it comes from",
            "#56d7ff",
            [
                CreditEntry(
                    "ENTER-M",
                    "Created, written, designed, and built by Lawliet.",
                    ["Story, systems, modes, interface, and art direction."],
                ),
                CreditEntry("Matsu'Py", "Visual novel engine by Lawliet, a fork of Ren'Py."),
                CreditEntry("Ren'Py", "Visual novel engine by Tom Rothamel and the Ren'Py contributors."),
                CreditEntry(
                    "Doki Doki Literature Club",
                    "Created and published by Team Salvato.",
                    ["ENTER-M is an unofficial fan work. It is not affiliated with or endorsed by Team Salvato."],
                ),
            ],
        ),
        CreditSection(
            "Systems",
            "Menus and gameplay tools",
            "#ff4968",
            [
                CreditEntry("Every System in This Build", "Designed and implemented by Lawliet.", ["If you clicked it, opened it, or collected it, it was built for ENTER-M."]),
                CreditEntry("Archive", "Roster, CG Gallery, Music Room, Side Stories, Lost Records, Achievements, Cards, and the Vault."),
                CreditEntry("Arcade", "The cabinet shelf, the mode launcher, and the MATSUCOM originals."),
                CreditEntry("Matsucoins and Cards", "Currency, rewards, and the card binder."),
                CreditEntry("Music Room", "Player, queue, shuffle, favorites, and a library that fills in as you listen."),
                CreditEntry("Phone", "Contacts, texts, calls, video calls, and idle conversations."),
                CreditEntry("Calendar", "Dates, the day-change dial, and the calendar menu."),
                CreditEntry("Records", "Saving, loading, copying, renaming, and erasing, all in one place."),
                CreditEntry("Presentation", "Speaker focus, stage panels, scene lighting, transitions, and the effects library."),
                CreditEntry("Text Adventure Format", "Inspired by the forest text adventure in NieR (Square Enix)."),
                CreditEntry("Next Time Trailer", "The preview at the end of the chapter."),
            ],
        ),
        CreditSection(
            "Modes",
            "Fights, set pieces, and Arcade originals",
            "#8a5cff",
            [
                CreditEntry("Ontological Seer and Id Mode", "Designed and implemented by Lawliet.", ["Inspired by Shin Megami Tensei and Etrian Odyssey (ATLUS) and Final Fantasy (Square Enix)."]),
                CreditEntry("Embodiment of Violet Ink", "Designed and implemented by Lawliet.", ["Inspired by the Touhou Project (ZUN).", "Endless Mode's soul patterns are inspired by Undertale and Deltarune (Toby Fox)."]),
                CreditEntry("The Unwritten Act", "Designed and implemented by Lawliet.", ["Inspired by Undertale and Deltarune (Toby Fox)."]),
                CreditEntry("A Fine Date", "Designed and implemented by Lawliet."),
                CreditEntry("Asarhythm", "Designed and implemented by Lawliet.", ["Inspired by Friday Night Funkin'."]),
                CreditEntry("MATSUCOM Originals", "Designed and implemented by Lawliet.", [
                    "Ouroboros Protocol, inspired by Snake.",
                    "Peer Review, inspired by brick-breaker games.",
                    "Intake, inspired by Tetris.",
                    "Containment Sweep, inspired by Minesweeper.",
                    "Board Meeting, inspired by chess. It is, admittedly, just chess.",
                    "Outlier, inspired by Peggle (PopCap Games).",
                ]),
                CreditEntry("Prize Machine", "Designed and implemented by Lawliet."),
            ],
        ),
        CreditSection(
            "Writing",
            "Story and concepts",
            "#d39a55",
            [
                CreditEntry("Main Story", "Story and concept by Lawliet."),
                CreditEntry("Side Stories", "Stories and concepts by Lawliet.", ["Hina's World is inspired by the Lacey Games horror series.", "Kotonoha's stories are inspired by the NieR Replicant text adventure format."]),
                CreditEntry("Lost Records", "Legacy stories by Lawliet.", ["The Answer", "SVHS TAP-05052022", "Mika: A DDLC Short Story", "Doki Doki Funni Club", "DDLC: Lost Media"]),
            ],
        ),
        CreditSection(
            "Characters",
            "The cast",
            "#b875ff",
            [
                CreditEntry("Monika", "Character by Team Salvato."),
                CreditEntry("Kotonoha", "Concept by Cyrke.", ["Written into ENTER-M by Lawliet."]),
                CreditEntry("Everyone Else", "Characters by Lawliet.", ["Matsuda, Tsubaki, Asahina, Sam, Mom, the player, and everyone you meet along the way."]),
            ],
        ),
        CreditSection(
            "Visuals",
            "Art, backgrounds, CGs, and UI",
            "#6df2a2",
            [
                CreditEntry("Doki Doki Literature Club Assets", "Team Salvato."),
                CreditEntry("Everything Else", "Lawliet.", ["Character art, CGs, interface, menus, and effects."]),
                CreditEntry("Backgrounds and Arcade Box Art", "Directed, polished, modified, and integrated by Lawliet.", ["Rough base imagery generated with a Stable Diffusion pipeline."]),
                CreditEntry("Additional Backgrounds", "Uncle Mugen, Elduator (Erika B. Hall), and Lornn.", ["Two fan-made DDLC door backgrounds by an artist we haven't identified. If they're yours, get in touch."]),
                CreditEntry("Cold Open", "Presenter logos belong to their respective owners."),
                CreditEntry("Fonts", "By their respective designers.", ["NovaSquare, SF Automaton Extended, Galldr, Myanmar, and the DDLC interface fonts."]),
            ],
        ),
        CreditSection(
            "Music",
            "Soundtrack and rhythm songs",
            "#75f7ff",
            [
                CreditEntry("Soundtrack", "Every track is credited in the Archive's Music Room.", ["Tracks appear there once you've heard them in the game."]),
                CreditEntry("Raise Up Your Bat", "From DELTARUNE, by Toby Fox."),
                CreditEntry("Zavodila (Remix)", "Original by Mike Geno, remix by Yori."),
                CreditEntry("Home", "From the FNF Doki Doki Takeover Bad Ending mod.", ["Full credits are with that mod's team."]),
                CreditEntry("Onslaught", "From the FNF Bob's Onslaught mod.", ["Full credits are with that mod's team."]),
            ],
        ),
        CreditSection(
            "Sound",
            "Effects and interface audio",
            "#f3d16b",
            [
                CreditEntry("Doki Doki Literature Club", "Sound effects by Team Salvato."),
                CreditEntry("Touhou Project", "Sound effects by ZUN."),
                CreditEntry("Ace Attorney", "Sound effects by Capcom."),
                CreditEntry("Everything Else", "Lawliet, with a few cues from Toby Fox and stock libraries."),
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
            "Community and friends",
            "#f4fbff",
            [
                CreditEntry("The Community", "Everyone who played, tested, reported a bug, or cheered this on."),
                CreditEntry("Friends", "For two years of patience, playtests, and pep talks."),
                CreditEntry("You", "For playing. See you next time."),
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
