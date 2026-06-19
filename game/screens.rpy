init offset = -1

style default:
    font gui.default_font
    size gui.text_size
    color gui.text_color
    outlines [(1, "#02050acc", 0, 1)]
    line_overlap_split 1
    line_spacing 1

style default_monika is normal:
    slow_cps 30

style edited is default:
    font gui.interface_font
    outlines [(2, "#02050a", 0, 1)]
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

style normal is default:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

style input:
    color gui.accent_color

style hyperlink_text:
    color gui.accent_color
    hover_color gui.hover_color
    hover_underline True

style splash_text:
    size 28
    color "#f4fbff"
    font gui.default_font
    text_align 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style splash_warning_panel is empty:
    xalign 0.5
    yalign 0.5
    xsize 760
    yminimum 250
    padding (48, 36, 48, 40)
    background "#050811dd"

style splash_warning_heading is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 30
    color "#ff4968"
    xalign 0.5
    text_align 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#ffffff66", 1, 1)]

style poemgame_text:
    yalign 0.5
    font gui.interface_font
    size 30
    color "#101820"
    outlines []

    hover_xoffset -3
    hover_outlines [(2, "#56d7ff88", 0, 0)]

style gui_text:
    font gui.interface_font
    color gui.interface_text_color
    size gui.interface_text_size


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.button_text_properties("button")
    yalign 0.5


style label_text is gui_text:
    color gui.accent_color
    size gui.label_text_size

style prompt_text is gui_text:
    color gui.text_color
    size gui.interface_text_size

style vbar:
    xsize gui.bar_size
    top_bar Solid("#56d7ff")
    bottom_bar Solid("#102431")

style bar:
    ysize 10
    base_bar Solid("#132532")
    thumb Solid("#56d7ff")

style scrollbar:
    ysize 10
    base_bar Solid("#132532")
    thumb Solid("#56d7ff")
    unscrollable "hide"
    bar_invert True


style vscrollbar:
    xsize 10
    base_bar Solid("#132532")
    thumb Solid("#56d7ff")
    unscrollable "hide"
    bar_invert True

style slider:
    ysize 10
    base_bar Solid("#132532")
    thumb Solid("#ff315b")

style vslider:
    xsize gui.slider_size
    base_bar Solid("#132532")
    thumb Solid("#ff315b")

style frame:
    padding gui.frame_borders.padding
    background Frame("mod_assets/gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        text what id "what" size enter_m_auto_say_text_size(what)

        if who is not None:

            window:
                style "namebox"
                text who id "who"



    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

    use quick_menu

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue
style namebox is default
style namebox_label is say_label

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("mod_assets/gui/textbox.png", xalign=0.5, yalign=1.0)

style window_monika is window:
    background Image("mod_assets/gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("mod_assets/gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    color gui.accent_color
    font gui.name_font
    size gui.name_text_size
    xalign gui.name_xalign
    yalign 0.5
    outlines [(3, "#123a5a", 0, 0), (1, "#02050a", 1, 1)]

style say_dialogue:
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    size gui.say_text_size

    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

image ctc:
    xalign 0.81 yalign 0.98 xoffset -5 alpha 0.0 subpixel True
    "gui/ctc.png"
    block:
        easeout 0.75 alpha 1.0 xoffset 0
        easein 0.75 alpha 0.5 xoffset -5
        repeat

style ctc_text is gui_text:
    color "#ff315b"
    size 20
    outlines [(1, "#02050a", 0, 1)]

image input_caret:
    Solid("#ff315b")
    size (2,25) subpixel True
    block:
        linear 0.35 alpha 0
        linear 0.35 alpha 1
        repeat

screen input(prompt):
    style_prefix "input"

    window:

        has vbox:
            xpos gui.text_xpos
            xanchor 0.5
            ypos gui.text_ypos

        text prompt style "input_prompt"
        input id "input"

style input_prompt is default

style input_prompt:
    xmaximum gui.text_width
    xalign gui.text_xalign
    text_align gui.text_xalign

style input:
    caret "input_caret"
    xmaximum gui.text_width
    xalign 0.5
    text_align 0.5

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action exam_guard_choice_action(i.action) at choice_button_hover

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 280
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    xsize gui.choice_button_width
    padding (26, 13, 26, 13)
    background "#071019e8"
    hover_background "#2a1020f2"
    selected_background "#183447f2"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")
    outlines [(1, "#02050a", 0, 1)]

transform choice_button_hover:
    subpixel True
    on hover:
        easeout 0.12 xoffset 10
    on idle:
        easeout 0.16 xoffset 0

init python:
    def RigMouse():
        currentpos = renpy.get_mouse_pos()
        targetpos = [640, 345]
        if currentpos[1] < targetpos[1]:
            renpy.display.draw.set_mouse_pos((currentpos[0] * 9 + targetpos[0]) / 10.0, (currentpos[1] * 9 + targetpos[1]) / 10.0)

screen rigged_choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action exam_guard_choice_action(i.action) at choice_button_hover

    timer 1.0/30.0 repeat True action Function(RigMouse)

define config.narrator_menu = True

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 280
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    xsize gui.choice_button_width
    padding (26, 13, 26, 13)
    background "#071019e8"
    hover_background "#2a1020f2"
    selected_background "#183447f2"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")
    outlines [(1, "#02050a", 0, 1)]

screen quick_menu():

    zorder 100

    if quick_menu:

        vbox:
            style_prefix "quick"

            xpos 12
            yalign 1.0
            yoffset -12
            spacing 4

            textbutton _("History") action ShowMenu('history')
            textbutton _("Skip") action Skip()
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            # textbutton _("Save") action ShowMenu('save')
            # textbutton _("Load") action ShowMenu('load')
            textbutton _("Phone") action Show("phone_contacts_screen")
            textbutton _("People") action Show("character_thoughts_screen")
            textbutton _("Settings") action ShowMenu('preferences')

default quick_menu = True

style quick_button:
    properties gui.button_properties("quick_button")
    xsize 88
    ysize 26
    background Solid("#05090fcc")
    hover_background Solid("#2a1020f2")
    padding (8, 2, 8, 3)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style quick_button_text:
    properties gui.button_text_properties("quick_button")
    font gui.interface_font
    size 12
    color "#d6e6ee"
    hover_color "#ff315b"
    text_align 0.5
    xalign 0.5
    yalign 0.5
    outlines [(1, "#02050a", 0, 1)]

init python:
    def FinishEnterName():
        if not player: return
        persistent.playername = player
        renpy.save_persistent()
        renpy.hide_screen("name_input")
        renpy.jump_out_of_context("start")

screen navigation(menu_context=None, embedded=False):

    $ nav_main = main_menu if menu_context is None else menu_context
    $ _msbf_save_load_locked = (not nav_main and msbf_save_load_locked())

    vbox:

        style_prefix "navigation"
        xfill True

        if not embedded:
            if nav_main:
                xpos gui.navigation_xpos
                yalign 0.8
            else:
                xalign 0.5
                yalign 0.0

        spacing gui.navigation_spacing

        if not persistent.autoload or not nav_main:

            if nav_main:

                # if persistent.playthrough == 1:
                #     textbutton _("ŔŗñĮ¼»ŧþŀÂŻŕěōì«") action If(persistent.playername, true=Start(), false=Show(screen="name_input", message="Please enter your name", ok_action=Function(FinishEnterName)))
                # else:
                textbutton _("New Game") action Start()

            else:

                textbutton _("History") action [ShowMenu("history"), SensitiveIf(renpy.get_screen("history") == None)]
                # Custom Calendar button
                textbutton _("Calendar") action ShowMenu("calendar_menu") sensitive renpy.get_screen("calendar_menu") == None

                textbutton _("Save Game") action ShowMenu("save") sensitive (not _msbf_save_load_locked and renpy.get_screen("save") == None)

            textbutton _("Load Game") action ShowMenu("load") sensitive (not _msbf_save_load_locked and renpy.get_screen("load") == None)

            if nav_main:

                textbutton _("Archive") action ShowMenu("archive")
                textbutton _("Credits") action ShowMenu("credits_menu")

            # if _in_replay:

            #     textbutton _("End Replay") action EndReplay(confirm=True)

            elif not nav_main:
                if persistent.playthrough != 3:
                    textbutton _("Main Menu") action MainMenu()
                else:
                    textbutton _("Main Menu") action NullAction()

            textbutton _("Settings") action [ShowMenu("preferences"), SensitiveIf(renpy.get_screen("preferences") == None)]

            if renpy.variant("pc"):

                #textbutton _("Help") action [Help("README.html"), Show(screen="dialog", message="The help file has been opened in your browser.", ok_action=Hide("dialog"))]
                textbutton _("Quit") action Quit(confirm=not nav_main)

        else:
            timer 1.75 action Start("autoload")

style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    xsize 238
    ysize 42
    padding (14, 5, 14, 5)
    background "#071019dd"
    hover_background "#2a1020f2"
    selected_background "#183447f2"
    insensitive_background "#03070baa"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 19
    color "#eaf8ff"
    hover_color "#ff315b"
    selected_color "#8bd7ff"
    insensitive_color "#7b8795"
    outlines [(2, "#02050a", 0, 1)]
    hover_outlines [(2, "#02050a", 0, 1), (1, "#ff315b99", 0, 0)]
    insensitive_outlines [(1, "#02050a", 0, 1)]
    hover_xoffset 8

screen main_menu():

    style_prefix "main_menu" tag menu

    add "menu_bg"
    add Solid("#02050ac8")
    add Solid("#06101bdc") xysize (402, 720)
    add Solid("#56d7ff4f") xysize (2, 616) xpos 402 ypos 52
    add Solid("#ff315b55") xysize (2, 172) xpos 410 ypos 62 at menu_panel_enter(0.18, 0, -18)
    add Solid("#56d7ff24") xysize (1280, 2) at menu_scanline_slow

    if not persistent.autoload:

        fixed:
            xsize 1280
            ysize 720

            frame:
                style "main_menu_command_frame"
                at menu_panel_enter(0.04, -64, 0)

                vbox:
                    xfill True
                    spacing 10

                    text "ENTER-M":
                        style "main_menu_panel_title"

                    text "v[config.version]":
                        style "main_menu_status"

                    null height 18

                    textbutton _("New Game"):
                        style "main_menu_command_button"
                        action Start()
                        default_focus True
                        at menu_button_enter(0.12)

                    textbutton _("Load Game"):
                        style "main_menu_command_button"
                        action [ShowMenu("load"), SensitiveIf(renpy.get_screen("load") == None)]
                        at menu_button_enter(0.17)

                    textbutton _("Archive"):
                        style "main_menu_command_button"
                        action ShowMenu("archive")
                        at menu_button_enter(0.22)

                    textbutton _("Credits"):
                        style "main_menu_command_button"
                        action ShowMenu("credits_menu")
                        at menu_button_enter(0.27)

                    textbutton _("Donate"):
                        style "main_menu_command_button"
                        action OpenURL("https://ko-fi.com/l4w1i3t")
                        at menu_button_enter(0.32)

                    textbutton _("Settings"):
                        style "main_menu_command_button"
                        action [ShowMenu("preferences"), SensitiveIf(renpy.get_screen("preferences") == None)]
                        at menu_button_enter(0.37)

                    textbutton _("Quit"):
                        style "main_menu_command_button"
                        action Quit(confirm=False)
                        at menu_button_enter(0.42)

            add "mod_assets/gui/logo.png" at menu_logo_reveal

    else:

        timer 1.75 action Start("autoload")

    if gui.show_name:

        vbox:
            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"

    key "K_ESCAPE" action Quit(confirm=False)

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text:
    color "#9bb0b8"
    size 16
    outlines [(1, "#02050a", 0, 1)]

style main_menu_frame:
    xsize 310
    yfill True

    background "menu_nav"

style main_menu_vbox:
    xalign 1.0
    xoffset -20
    xmaximum 800
    yalign 1.0
    yoffset -20

# Dark semi-transparent panel behind each pentagon menu button.
style pentagon_panel is empty:
    xoffset 2000
    background None
    padding (22, 10, 22, 12)

style main_menu_command_frame is empty:
    xpos 42
    ypos 50
    xsize 330
    ysize 620
    padding (30, 32, 30, 28)

style main_menu_panel_title is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 31
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]

style main_menu_status is gui_text:
    font gui.interface_font
    size 14
    color "#9fc9d6"
    outlines [(1, "#02050a", 0, 1)]

style main_menu_command_button is navigation_button:
    xsize 270
    ysize 44
    padding (18, 6, 18, 7)
    background "#071019dd"
    hover_background "#2a1020f2"
    insensitive_background "#03070baa"

style main_menu_command_button_text is navigation_button_text:
    size 21

style main_menu_signal_frame is empty:
    xpos 822
    ypos 498
    xsize 324
    ysize 114
    padding (22, 18, 22, 18)
    background "#05090fcc"

style main_menu_signal_text is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 19
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1)]

style main_menu_signal_subtext is gui_text:
    font gui.interface_font
    size 14
    color "#ff315b"
    outlines [(1, "#02050a", 0, 1)]

style main_menu_text:
    xalign 1.0

    layout "subtitle"
    text_align 1.0
    color gui.accent_color

style main_menu_title:
    size gui.title_text_size

screen game_menu_m():
    $ persistent.menu_bg_m = True
    add "game_menu_bg"
    add Solid("#02050add")
    timer 0.3 action Hide("game_menu_m")

screen game_menu(title, scroll=None):

    if main_menu:

        add gui.main_menu_background

    else:

        key "mouseup_3" action Return()
        add gui.game_menu_background

    add Solid("#02050acc")
    add Solid("#56d7ff1c") xysize (1280, 2) at menu_scanline_slow

    style_prefix "game_menu"

    frame:
        style "game_menu_outer_frame"
        at menu_panel_enter(0.0, -28, 0)

        hbox:
            spacing 16

            frame:
                style "game_menu_navigation_frame"

                vbox:
                    xfill True
                    spacing 14

                    text "ENTER-M":
                        style "game_menu_nav_title"

                    use navigation(main_menu, embedded=True)

                    null height 10

                    textbutton _("Return"):
                        style "return_button"
                        action Return()

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
            
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        yinitial 1.0
                        side_yfill True
                        has vbox
                        transclude

                elif scroll == "vpgrid":

                    vpgrid:

                        cols 1
                        yinitial 1.0
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        side_yfill True
                        transclude

                else:

                    transclude

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")

style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    xpos 44
    ypos 42
    xsize 1192
    ysize 636
    padding (0, 0, 0, 0)
    background None

style game_menu_navigation_frame:
    xsize 272
    ysize 636
    padding (24, 28, 20, 24)
    background "#05090fee"

style game_menu_content_frame:
    xsize 904
    ysize 636
    padding (34, 84, 34, 32)
    background "#071019e8"

style game_menu_viewport:
    xsize 828

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 10

style game_menu_label:
    xpos 348
    ypos 62
    xsize 830
    ysize 58

style game_menu_label_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 36
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]
    yalign 0.5

style return_button:
    xsize 246
    ysize 42

style game_menu_nav_title is gui_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 24
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]

screen about():

    tag menu

    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            if gui.about:

                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")

define gui.about = ""

style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size

screen save():

    tag menu
    if msbf_save_load_locked() and not main_menu:
        use locked_file_menu(_("Save"), _("Saving is unavailable during Matsuda's boss fight."))
    else:
        use file_slots(_("Save"))


screen load():
    
    tag menu
    if msbf_save_load_locked() and not main_menu:
        use locked_file_menu(_("Load"), _("Loading is unavailable during Matsuda's boss fight."))
    else:
        use file_slots(_("Load"))

screen locked_file_menu(title, message):
    use game_menu(title):
        frame:
            xalign 0.5
            yalign 0.5
            xsize 650
            ysize 150
            background Solid("#050811e8")
            padding (24, 22)

            vbox:
                spacing 12
                text message style "locked_file_menu_text":
                    xalign 0.5
                    text_align 0.5
                text _("Finish or leave the battle before using save files.") style "locked_file_menu_hint":
                    xalign 0.5
                    text_align 0.5

init python:
    def FileActionMod(name, page=None, **kwargs):
        if msbf_save_load_locked():
            return NullAction()
        if persistent.playthrough == 1 and not persistent.deleted_saves and renpy.current_screen().screen_name[0] == "load" and FileLoadable(name):
            return Show(screen="dialog", message="This save belongs to an unavailable route state.",
                ok_action=Show(screen="dialog", message="Starting a clean session from the current story entry.", ok_action=Function(renpy.full_restart, label="start")))
        elif persistent.playthrough == 3 and renpy.current_screen().screen_name[0] == "save":
            return Show(screen="dialog", message="Saving is locked during this route state.", ok_action=Hide("dialog"))
        else:
            return FileAction(name)


screen file_slots(title):

    default page_name_value = FilePageNameInputValue()

    use game_menu(title):

        fixed:

            order_reverse True

            button:
                style "page_label"


                xalign 0.5


                input:
                    style "page_label_text"
                    value page_name_value


            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileActionMod(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)


            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing








                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)




style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text
style locked_file_menu_text is gui_text
style locked_file_menu_hint is gui_text

style page_label:
    xpadding 50
    ypadding 3

style page_label_text:
    color "#f2fbff"
    outlines [(1, "#02050a", 0, 1)]
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")
    background "#071019cc"
    hover_background "#2a1020f2"
    selected_background "#183447f2"

style page_button_text:
    properties gui.button_text_properties("page_button")
    color "#b8c7cf"
    hover_color "#ff315b"
    selected_color "#8bd7ff"
    outlines [(1, "#02050a", 0, 1)]

style slot_button:
    properties gui.button_properties("slot_button")
    background "#071019dd"
    hover_background "#2a1020f2"
    selected_background "#183447f2"
    insensitive_background "#03070baa"

style slot_button_text:
    properties gui.button_text_properties("slot_button")
    color "#b8c7cf"
    hover_color "#ff315b"
    selected_color "#8bd7ff"
    outlines [(1, "#02050a", 0, 1)]

style locked_file_menu_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 24
    color "#eaf8ff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]

style locked_file_menu_hint:
    font gui.interface_font
    size 18
    color "#9bb0b8"
    outlines [(1, "#02050a", 0, 1)]









init python:
    def enter_m_restore_default_preferences():
        _preferences.fullscreen = False
        _preferences.desktop_rollback_side = "disable"
        _preferences.mobile_rollback_side = "disable"
        _preferences.skip_unseen = False
        _preferences.skip_after_choices = False
        _preferences.afm_enable = False
        _preferences.afm_after_click = False
        _preferences.text_cps = 50
        _preferences.afm_time = 15

        for mixer in ("main", "music", "sfx", "voice"):
            _preferences.set_volume(mixer, 1.0)
            _preferences.set_mute(mixer, False)

        renpy.restart_interaction()

    def enter_m_max_volume():
        for mixer in ("main", "music", "sfx", "voice"):
            _preferences.set_volume(mixer, 1.0)
            _preferences.set_mute(mixer, False)

        renpy.restart_interaction()


transform pref_panel_enter(delay=0.0):
    alpha 0.0
    yoffset 14
    pause delay
    easeout 0.18 alpha 1.0 yoffset 0

transform pref_button_hover:
    subpixel True
    on show:
        xoffset 0
    on hover:
        easeout 0.10 xoffset 6
    on idle:
        easeout 0.14 xoffset 0


screen preferences():
    tag menu

    use game_menu(_("Settings")):

        fixed:
            xysize (828, 500)
            xalign 0.5
            yalign 0.5

            hbox:
                spacing 14
                xfill True
                yfill True

                vbox:
                    style "pref_column"

                    frame:
                        style "pref_panel"
                        at pref_panel_enter(0.00)

                        vbox:
                            spacing 10

                            hbox:
                                style "pref_section_header"
                                add Solid("#56d7ff") xysize (4, 22) yalign 0.5
                                text _("Display") style "pref_section_title"

                            if renpy.variant("pc"):
                                hbox:
                                    style "pref_button_row"
                                    textbutton _("Window") style "radio_button" action Preference("display", "window") at pref_button_hover
                                    textbutton _("Fullscreen") style "radio_button" action Preference("display", "fullscreen") at pref_button_hover

                            if config.developer:
                                text _("Rollback Edge") style "pref_row_label"
                                hbox:
                                    style "pref_button_row"
                                    textbutton _("Off") style "pref_small_button" action Preference("rollback side", "disable") at pref_button_hover
                                    textbutton _("Left") style "pref_small_button" action Preference("rollback side", "left") at pref_button_hover
                                    textbutton _("Right") style "pref_small_button" action Preference("rollback side", "right") at pref_button_hover

                    frame:
                        style "pref_panel"
                        at pref_panel_enter(0.04)

                        vbox:
                            spacing 10

                            hbox:
                                style "pref_section_header"
                                add Solid("#ff315b") xysize (4, 22) yalign 0.5
                                text _("Reading") style "pref_section_title"

                            hbox:
                                style "pref_button_row"
                                textbutton _("Unseen Text") style "check_button" action Preference("skip", "toggle") at pref_button_hover
                                textbutton _("After Choices") style "check_button" action Preference("after choices", "toggle") at pref_button_hover

                            hbox:
                                style "pref_button_row"
                                textbutton _("Auto Mode") style "check_button" action Preference("auto-forward", "toggle") at pref_button_hover
                                textbutton _("After Click") style "check_button" action Preference("auto-forward after click", "toggle") at pref_button_hover

                            text _("Text Speed") style "pref_row_label"
                            bar value FieldValue(_preferences, "text_cps", range=180, max_is_zero=False, style="slider", offset=20) style "pref_wide_slider"

                            text _("Auto-Forward Delay") style "pref_row_label"
                            bar value Preference("auto-forward time") style "pref_wide_slider"

                vbox:
                    style "pref_column"

                    frame:
                        style "pref_panel"
                        at pref_panel_enter(0.08)

                        vbox:
                            spacing 10

                            hbox:
                                style "pref_section_header"
                                add Solid("#56d7ff") xysize (4, 22) yalign 0.5
                                text _("Audio") style "pref_section_title"

                            if config.has_music:
                                text _("Music Volume") style "pref_row_label"
                                bar value Preference("music volume") style "pref_wide_slider"

                            if config.has_sound:
                                text _("Sound Volume") style "pref_row_label"
                                hbox:
                                    style "pref_audio_row"
                                    bar value Preference("sound volume") style ("pref_audio_slider" if config.sample_sound else "pref_wide_slider")

                                    if config.sample_sound:
                                        textbutton _("Test") style "pref_test_button" action Play("sound", config.sample_sound) at pref_button_hover

                            if config.has_voice:
                                text _("Voice Volume") style "pref_row_label"
                                hbox:
                                    style "pref_audio_row"
                                    bar value Preference("voice volume") style ("pref_audio_slider" if config.sample_voice else "pref_wide_slider")

                                    if config.sample_voice:
                                        textbutton _("Test") style "pref_test_button" action Play("voice", config.sample_voice) at pref_button_hover

                            if config.has_music or config.has_sound or config.has_voice:
                                hbox:
                                    style "pref_button_row"
                                    textbutton _("Mute All") style "mute_all_button" action Preference("all mute", "toggle") at pref_button_hover
                                    textbutton _("Max Volume") style "pref_action_button" action Function(enter_m_max_volume) at pref_button_hover

                    frame:
                        style "pref_panel"
                        at pref_panel_enter(0.12)

                        vbox:
                            spacing 10

                            hbox:
                                style "pref_section_header"
                                add Solid("#ff315b") xysize (4, 22) yalign 0.5
                                text _("Quick") style "pref_section_title"

                            hbox:
                                style "pref_button_row"
                                textbutton _("Reset") style "pref_action_button" action Function(enter_m_restore_default_preferences) at pref_button_hover

                    frame:
                        style "pref_panel"
                        at pref_panel_enter(0.16)

                        vbox:
                            spacing 10

                            hbox:
                                style "pref_section_header"
                                add Solid("#56d7ff") xysize (4, 22) yalign 0.5
                                text _("Assist") style "pref_section_title"

                            hbox:
                                style "pref_button_row"
                                textbutton _("Cursor Assist") style "check_button" action Preference("automatic move", "toggle") at pref_button_hover
                                textbutton _("Audio Focus") style "check_button" action Preference("emphasize audio", "toggle") at pref_button_hover

    text "v[config.version]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"

style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text
style pref_column is vbox
style pref_panel is empty
style pref_section_header is hbox
style pref_section_title is gui_text
style pref_row_label is gui_text
style pref_button_row is hbox
style pref_audio_row is hbox
style pref_small_button is radio_button
style pref_small_button_text is radio_button_text
style pref_action_button is radio_button
style pref_action_button_text is radio_button_text
style pref_test_button is slider_button
style pref_test_button_text is slider_button_text
style pref_wide_slider is slider_slider
style pref_audio_slider is slider_slider

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 2

style pref_label_text:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 24
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]
    yalign 1.0

style pref_vbox:
    xsize 246

style pref_column:
    xsize 407
    spacing 14

style pref_panel:
    xsize 407
    padding (16, 14, 16, 16)
    background "#071019df"

style pref_section_header:
    spacing 9
    bottom_margin 2

style pref_section_title:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 22
    color "#f2fbff"
    outlines [(2, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]
    yalign 0.5

style pref_row_label:
    font gui.interface_font
    size 17
    color "#d4e8f1"
    outlines [(1, "#02050a", 0, 1)]
    top_margin 2

style pref_button_row:
    spacing 10

style pref_audio_row:
    spacing 10
    yalign 0.5

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    xsize 176
    ysize 34
    padding (12, 4, 12, 5)
    background "#071019cc"
    hover_background "#2a1020f2"
    selected_background "#12314af2"
    selected_hover_background "#321223f2"
    insensitive_background "#03070baa"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style radio_button_text:
    properties gui.button_text_properties("radio_button")
    font gui.interface_font
    size 18
    color "#b8c7cf"
    hover_color "#ff315b"
    selected_color "#8bd7ff"
    selected_hover_color "#ff315b"
    outlines [(1, "#02050a", 0, 1)]
    hover_outlines [(1, "#02050a", 0, 1), (1, "#ff315b88", 0, 0)]
    selected_outlines [(1, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]
    selected_hover_outlines [(1, "#02050a", 0, 1), (1, "#ff315b99", 0, 0)]

style pref_small_button:
    xsize 116

style pref_action_button:
    xsize 176

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    xsize 176
    ysize 34
    padding (12, 4, 12, 5)
    background "#071019cc"
    hover_background "#2a1020f2"
    selected_background "#12314af2"
    selected_hover_background "#321223f2"
    insensitive_background "#03070baa"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style check_button_text:
    properties gui.button_text_properties("check_button")
    font gui.interface_font
    size 18
    color "#b8c7cf"
    hover_color "#ff315b"
    selected_color "#8bd7ff"
    selected_hover_color "#ff315b"
    outlines [(1, "#02050a", 0, 1)]
    hover_outlines [(1, "#02050a", 0, 1), (1, "#ff315b88", 0, 0)]
    selected_outlines [(1, "#02050a", 0, 1), (1, "#56d7ff88", 0, 0)]
    selected_hover_outlines [(1, "#02050a", 0, 1), (1, "#ff315b99", 0, 0)]

style slider_slider:
    xsize 330
    ysize 10

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 10

style slider_button_text:
    properties gui.button_text_properties("slider_button")
    color "#b8c7cf"
    hover_color "#ff315b"
    outlines [(1, "#02050a", 0, 1)]

style pref_wide_slider:
    xsize 360

style pref_audio_slider:
    xsize 286

style pref_test_button:
    xsize 64
    ysize 34
    left_margin 0
    padding (8, 4, 8, 5)
    background "#071019cc"
    hover_background "#2a1020f2"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style pref_test_button_text:
    size 16
    color "#b8c7cf"
    hover_color "#ff315b"
    outlines [(1, "#02050a", 0, 1)]

style slider_vbox:
    xsize 400










screen history():




    predict False tag menu

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport")):

        style_prefix "history"

        for h in _history_list:

            window:


                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"



                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                text h.what

        if not _history_list:
            label _("The dialogue history is empty.")


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5












































































































































































screen name_input(message, ok_action):


    modal True

    zorder 200

    style_prefix "confirm"

    add Solid("#02050ad9")
    key "K_RETURN" action [Play("sound", gui.activate_sound), ok_action]

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        input default "" value VariableInputValue("player") length 12 allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"






        hbox:
            xalign 0.5
            spacing 100

            textbutton _("OK") action ok_action

screen dialog(message, ok_action):


    modal True

    zorder 200

    style_prefix "confirm"

    add Solid("#02050ad9")

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("OK") action ok_action

image confirm_glitch = Null()

screen confirm(message, yes_action, no_action):


    modal True

    zorder 200

    style_prefix "confirm"

    add Solid("#02050ad9")

    frame:

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            style "confirm_prompt"
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Yes") action yes_action
            textbutton _("No") action no_action





style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame("mod_assets/gui/frame.png", gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    color "#101820"
    outlines []
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style confirm_button_text is navigation_button_text:
    properties gui.button_text_properties("confirm_button")








screen fake_skip_indicator():
    use skip_indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        has hbox:
            spacing 6

        text _("Skipping")

        text ">" at delayed_blink(0.0, 1.0) style "skip_triangle"
        text ">" at delayed_blink(0.2, 1.0) style "skip_triangle"
        text ">" at delayed_blink(0.4, 1.0) style "skip_triangle"



transform delayed_blink(delay, cycle):
    alpha .5

    pause delay
    block:

        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Solid("#05090fed")
    padding gui.skip_frame_borders.padding

style skip_text:
    color "#d6e6ee"
    size gui.notify_text_size

style skip_triangle:
    color "#ff315b"
    font gui.interface_font









screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Solid("#05090fed")
    padding gui.notify_frame_borders.padding

style notify_text:
    color "#d6e6ee"
    size gui.notify_text_size
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
