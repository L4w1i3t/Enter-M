# The writer's workspace at 1280x720: header, document bar, script, beat detail,
# stage, insert palette and status bar. Geometry comes from the SW_* constants in
# controller.rpy; dialogs live in dialogs.rpy.
screen story_writer(session):
    modal True
    zorder 210
    style_prefix "sw"

    # Lowest priority: the game's own shortcuts are off while writing, so a key
    # pressed with no field focused cannot hide the screen, reload the game,
    # take a screenshot or open another tool. Right-click no longer closes.
    key ["rollback", "rollforward", "screenshot", "toggle_fullscreen", "game_menu", "hide_windows",
        "launch_editor", "reload_game", "inspector", "full_inspector", "developer", "help",
        "choose_renderer", "progress_screen", "bubble_editor", "accessibility", "self_voicing",
        "clipboard_voicing", "debug_voicing", "extra_voicing", "skip", "toggle_skip", "fast_skip",
        "console", "director", "performance", "image_load_log", "profile_once", "memory_profile"] action NullAction()

    # Writer shortcuts. A focused field sees keys first and passes these through.
    key "K_ESCAPE" action Function(session.escape)
    key "ctrl_K_s" action Function(session.save_shortcut)
    key "K_F5" action Function(session.play)
    key "ctrl_K_RETURN" action Function(session.next_textbox)
    key "ctrl_K_KP_ENTER" action Function(session.next_textbox)
    key "ctrl_K_UP" action Function(session.step_selection, -1)
    key "ctrl_K_DOWN" action Function(session.step_selection, 1)
    key "alt_K_UP" action Function(session.edit_operation, "up")
    key "alt_K_DOWN" action Function(session.edit_operation, "down")
    key "ctrl_K_z" action Function(session.edit_operation, "undo")
    key "ctrl_K_y" action Function(session.edit_operation, "redo")
    key "ctrl_K_o" action Function(session.open_modal, "files")
    key "K_F11" action Preference("display", "toggle")
    # Idle commit, autosave and disk check. It only rebuilds the screen when
    # one of them changed something (a rebuild used to happen every tick).
    timer 1.0 repeat True action Function(session.tick, _update_screens=False)

    $ sw_block = session.block
    $ sw_left_w = SW_FULL_W if session.focus_mode else SW_LEFT_W
    $ sw_inner_w = sw_left_w - 2 * SW_DETAIL_PAD

    add Solid("#161c22")

    # Header: file actions | history | saving | reading and view | close.
    add Solid("#10151a") xysize (1280, 56)
    add Solid("#29343b") ypos 56 xysize (1280, 1)
    add Solid(SW_ACCENT) xpos 20 ypos 16 xysize (4, 24)
    text "STORY WRITER" xpos 34 ypos 17 size 18 font SW_FONT_BOLD color SW_INK
    hbox:
        xpos 214 ypos 11 spacing 6
        textbutton "Open" action Function(session.open_modal, "files")
        textbutton "New" action Function(session.open_modal, "new")
        textbutton "Outline" action Function(session.open_modal, "outline")
        null width 10
        textbutton "Undo" action Function(session.edit_operation, "undo")
        textbutton "Redo" action Function(session.edit_operation, "redo")
        null width 10
        textbutton "Save Draft" action Function(session.save_draft_action)
        textbutton "Save to Story" action Function(session.save_source) style "sw_primary"
        null width 10
        textbutton "Read Scene" action Function(session.play)
        textbutton ("Split View" if session.focus_mode else "Focus") action Function(session.toggle_focus) selected session.focus_mode
    textbutton "Close" xpos 1260 xanchor 1.0 ypos 11 action Function(session.exit)

    # Document bar: file and state on the left, where the selection sits on the right.
    hbox:
        xpos 20 ypos 63 spacing 10
        text sw_fit(session.filename, 420, 15) size 15 color SW_INK yalign 0.5
        frame:
            yalign 0.5 padding (8, 2)
            background Solid("#4a3b25" if session.dirty else "#23372f")
            text ("Unsaved" if session.dirty else "Saved") size 12 color (SW_WARN if session.dirty else SW_ACCENT)
        if session.disk_changed:
            textbutton "Changed on disk: Reload" style "sw_small_warn" yalign 0.5 action Function(session.reload_from_disk)
    if sw_block is not None:
        $ sw_where = session.breadcrumb(sw_block)
        if sw_where:
            text sw_fit(sw_where, 390, 13) xpos 650 ypos 67 size 13 color "#8a9899"
        text ("line %d  ·  beat %d of %d" % (sw_block.line, max(1, session.row_index() + 1), len(session.rows()))) xpos 1260 xanchor 1.0 ypos 67 size 13 color SW_MUTED

    # Script: every beat in source order. Only the rows near the viewport exist.
    add Solid("#11171d") xpos SW_LEFT_X ypos 96 xysize (sw_left_w, 288)
    text "SCRIPT" xpos (SW_LEFT_X + 12) ypos 104 size 12 font SW_FONT_BOLD color SW_MUTED
    hbox:
        xpos (SW_LEFT_X + sw_left_w - 8) xanchor 1.0 ypos 99 spacing 4
        if session.focus_mode:
            textbutton "Insert…" style "sw_small" action Function(session.open_modal, "insert") sensitive session.insert_allowed()
        textbutton "Duplicate" style "sw_small" action Function(session.edit_operation, "duplicate") sensitive sw_block.editable
        textbutton "Up" style "sw_small" action Function(session.edit_operation, "up") sensitive sw_block.editable
        textbutton "Down" style "sw_small" action Function(session.edit_operation, "down") sensitive sw_block.editable
        textbutton "Delete" style "sw_small_danger" action Function(session.edit_operation, "delete") sensitive sw_block.editable
    viewport:
        xpos SW_LEFT_X ypos SW_LIST_Y xysize (sw_left_w, SW_LIST_H)
        yadjustment session.list_adjustment
        mousewheel True
        scrollbars "vertical"
        fixed:
            xysize ((sw_left_w - 12), session.list_height())
            for sw_index, sw_row in session.window_rows():
                $ sw_tag, sw_tag_color, sw_summary, sw_summary_color, sw_depth = session.row_parts(sw_row)
                $ sw_is_selected = sw_row.uid == session.selected
                $ sw_indent = 14 * min(sw_depth, 4)
                $ sw_row_font = SW_FONT_BOLD if sw_row.kind == "label" else SW_FONT
                button:
                    xpos 0 ypos (sw_index * SW_ROW_PITCH) xysize ((sw_left_w - 12), SW_ROW_H)
                    padding (0, 0)
                    background Solid("#2a3f42" if sw_is_selected else ("#1a2229" if sw_row.editable else "#141a20"))
                    hover_background Solid("#33484b" if sw_is_selected else "#232e35")
                    action Function(session.select, sw_row.uid)
                    fixed:
                        if sw_is_selected:
                            add Solid(SW_ACCENT) xysize (3, SW_ROW_H)
                        text str(sw_row.line) xpos 46 xanchor 1.0 yalign 0.5 size 12 color "#6d7b7e"
                        text sw_fit(sw_tag, 88, 13) xpos 58 yalign 0.5 size 13 color sw_tag_color
                        text sw_fit(sw_summary, (sw_left_w - 12 - 166 - sw_indent), 15, sw_row_font) xpos (156 + sw_indent) yalign 0.5 size 15 font sw_row_font color sw_summary_color

    # Beat detail: the selected beat's own editor.
    add Solid("#1b232a") xpos SW_LEFT_X ypos SW_DETAIL_Y xysize (sw_left_w, SW_DETAIL_H)
    fixed:
        xpos (SW_LEFT_X + SW_DETAIL_PAD) ypos (SW_DETAIL_Y + 10) xysize (sw_inner_w, (SW_DETAIL_H - 20))
        if sw_block.kind == "say":
            use sw_detail_say(session, sw_inner_w)
        elif sw_block.kind in ("scene", "show", "hide", "with", "pause"):
            use sw_detail_stage(session, sw_inner_w)
        elif sw_block.kind == "music":
            use sw_detail_music(session, sw_inner_w)
        else:
            use sw_detail_other(session, sw_inner_w)

    if not session.focus_mode:
        # Stage: the composition as of the selected beat.
        add Solid("#11171d") xpos SW_RIGHT_X ypos 96 xysize (SW_RIGHT_W, 360)
        text "STAGE" xpos (SW_RIGHT_X + 12) ypos 104 size 12 font SW_FONT_BOLD color SW_MUTED
        text ("as of line %d" % sw_block.line) xpos (SW_RIGHT_X + 66) ypos 105 size 12 color "#6f7c7f"
        hbox:
            xpos (SW_RIGHT_X + SW_RIGHT_W - 8) xanchor 1.0 ypos 99 spacing 4
            textbutton "Replay" style "sw_small" action Function(session.replay_stage)
            textbutton "Source" style "sw_small" action Function(session.open_modal, "source")
        fixed:
            xpos SW_RIGHT_X ypos 128 xysize (SW_RIGHT_W, SW_STAGE_H)
            add Solid("#0b1016")
            if session.stage is not None:
                add session.stage
            if session.stage_warning:
                frame:
                    yalign 1.0 xfill True padding (10, 6)
                    background Solid("#0d131ae8")
                    text sw_caption(session.stage_warning) size 12 color SW_WARN xmaximum (SW_RIGHT_W - 20)

        # Insert palette: everything that can follow the selected beat.
        $ sw_can_insert = session.insert_allowed()
        add Solid("#1b232a") xpos SW_RIGHT_X ypos 466 xysize (SW_RIGHT_W, 218)
        text (("INSERT AFTER LINE %d" % sw_block.line) if sw_can_insert else "INSERT") xpos (SW_RIGHT_X + 12) ypos 475 size 12 font SW_FONT_BOLD color SW_MUTED
        if not sw_can_insert:
            text "Select an editable beat or a scene label first." xpos (SW_RIGHT_X + 76) ypos 476 size 12 color SW_WARN
        use sw_palette(session, (SW_RIGHT_X + 12), 498, sw_can_insert)

    # Status bar.
    add Solid("#10151a") ypos 692 xysize (1280, 28)
    add Solid("#29343b") ypos 692 xysize (1280, 1)
    if session.error:
        frame:
            xpos 20 ypos 697 padding (6, 1)
            background Solid("#5a2f2c")
            text "PROBLEM" size 11 font SW_FONT_BOLD color "#ffd9d4"
    text sw_fit(session.status, (850 if session.error else 930), 13) xpos (96 if session.error else 20) ypos 698 size 13 color (SW_ERROR if session.error else SW_MUTED)
    text "Ctrl+Up/Down beats  ·  Ctrl+S save  ·  F5 read" xpos 1260 xanchor 1.0 ypos 699 size 12 color "#6f7c7f"

    if session.modal:
        use sw_modal(session)

screen sw_palette(session, x, y, enabled):
    vbox:
        xpos x ypos y spacing 8
        for sw_group, sw_entries in SW_PALETTE:
            hbox:
                spacing 6
                fixed:
                    xysize (64, 34)
                    text sw_group size 13 color SW_MUTED yalign 0.5
                for sw_kind, sw_label in sw_entries:
                    textbutton sw_label action Function(session.palette_insert, sw_kind) sensitive enabled

screen sw_form_row(label, height=40):
    hbox:
        spacing 8
        fixed:
            xysize (96, height)
            text label size 13 color SW_MUTED yalign 0.5
        transclude

screen sw_detail_header(title, color, line, extra=""):
    text title ypos 2 size 12 font SW_FONT_BOLD color color
    text (("line %d" % line) + extra) xpos 150 ypos 3 size 12 color SW_MUTED

screen sw_detail_say(session, width):
    $ sw_speaker = session.fields.get("speaker", "")
    $ sw_attributes = session.fields.get("attributes", "")
    use sw_detail_header("TEXTBOX", SW_ACCENT, session.block.line)
    if sw_attributes:
        text sw_fit("expression: " + sw_attributes, 300, 12) xpos width xanchor 1.0 ypos 3 size 12 color SW_MUTED
    hbox:
        ypos 22 spacing 6
        textbutton sw_fit("Speaker: " + session.speaker_label(sw_speaker), 200, 15) action Function(session.open_modal, "speakers") style "sw_primary"
        textbutton "Expression…" action Function(session.browse_assets, "cast", "attributes") sensitive bool(sw_speaker and sw_speaker != "nier")
        textbutton "Narration" action Function(session.change_field, "speaker", "") selected (not sw_speaker)
        textbutton "Nier" action Function(session.change_field, "speaker", "nier") selected (sw_speaker == "nier")
    hbox:
        xpos width xanchor 1.0 ypos 22 spacing 4
        textbutton "A−" action Function(session.resize_text, -2)
        textbutton "A+" action Function(session.resize_text, 2)
    add session.field("text", width, SW_PROSE_H, True) ypos 64
    hbox:
        ypos 240 spacing 6
        textbutton "Split at cursor" style "sw_small" action Function(session.split_text)
        textbutton "Join next" style "sw_small" action Function(session.join_text)
    text "Enter  new textbox   ·   Shift+Enter  line break" xpos width xanchor 1.0 ypos 244 size 12 color "#7c898b"

screen sw_detail_stage(session, width):
    $ block = session.block
    $ kind = block.kind
    $ sw_form_w = width - 14
    $ sw_field_w = sw_form_w - 104
    use sw_detail_header({"scene": "BACKGROUND", "show": "SPRITE", "hide": "HIDE IMAGE", "with": "TRANSITION", "pause": "PAUSE"}[kind],
        SW_KIND_COLORS[SW_KIND_WORDS[kind]], block.line)
    hbox:
        xpos width xanchor 1.0 ypos 0 spacing 4
        textbutton "Apply" style "sw_small" action Function(session.apply)
        if kind in ("scene", "show"):
            textbutton ("Browse sprites…" if kind == "show" else "Browse backgrounds…") style "sw_small" action Function(session.browse_assets, ("cast" if kind == "show" else "backgrounds"), "edit")
    viewport:
        ypos 26 xysize (width, 242)
        mousewheel True
        scrollbars "vertical"
        vbox:
            spacing 6
            if kind in ("scene", "show", "hide"):
                use sw_form_row("Image" if kind != "hide" else "Image tag"):
                    add session.field("image", sw_field_w)
            if kind == "hide":
                $ sw_tags = [entry["tag"] for entry in session.stage_images(before=True)]
                use sw_form_row("On stage", 34):
                    if not sw_tags:
                        text "nobody at this point" size 13 color SW_MUTED yalign 0.5
                    for sw_tag in sw_tags[:6]:
                        textbutton sw_tag style "sw_segment" yalign 0.5 action Function(session.change_field, "image", sw_tag) selected (session.fields.get("image") == sw_tag)
            if kind == "show":
                $ sw_motion = session.motion_state()
                use sw_form_row("Motion", 34):
                    for sw_value, sw_label in (("t", "Move"), ("i", "Snap"), ("h", "Hop"), ("l", "Slide in")):
                        textbutton sw_label style "sw_segment" yalign 0.5 action Function(session.set_motion, motion=sw_value) selected (sw_motion is not None and sw_motion[0] == sw_value)
                    null width 6
                    textbutton "Focused" style "sw_segment" yalign 0.5 action Function(session.set_motion, focused=not (sw_motion and sw_motion[3])) selected bool(sw_motion and sw_motion[3]) sensitive (sw_motion is None or sw_motion[0] in ("t", "h", "l"))
                    null width 6
                    textbutton "Leave" style "sw_segment" yalign 0.5 action Function(session.change_field, "at", "thide") selected (session.fields.get("at") == "thide")
                use sw_form_row("Slot", 34):
                    text "cast" size 12 color SW_MUTED yalign 0.5
                    for sw_count in range(1, 7):
                        textbutton str(sw_count) style "sw_segment" xminimum 28 yalign 0.5 action Function(session.set_motion, count=sw_count) selected (sw_motion is not None and sw_motion[1] == sw_count)
                    null width 10
                    text "position" size 12 color SW_MUTED yalign 0.5
                    for sw_slot in range(1, (sw_motion[1] if sw_motion else 1) + 1):
                        textbutton str(sw_slot) style "sw_segment" xminimum 28 yalign 0.5 action Function(session.set_motion, slot=sw_slot) selected (sw_motion is not None and sw_motion[2] == sw_slot)
            if kind in ("scene", "show"):
                use sw_form_row("Placement"):
                    add session.field("at", 190)
                    fixed:
                        xysize (72, 40)
                        text "transition" size 12 color SW_MUTED yalign 0.5 xalign 1.0
                    add session.field("transition", (sw_field_w - 190 - 72 - 16))
            if kind in ("hide", "with"):
                use sw_form_row("Transition"):
                    add session.field("transition", sw_field_w)
            if kind in ("scene", "show", "hide", "with"):
                use sw_form_row("", 30):
                    for sw_transition in ("dissolve", "dissolve_scene_full", "wipeleft_scene", "fade", "None"):
                        $ sw_value = "None" if (sw_transition == "None" and kind == "with") else ("" if sw_transition == "None" else sw_transition)
                        textbutton sw_transition style "sw_segment" yalign 0.5 action Function(session.change_field, "transition", sw_value) selected (session.fields.get("transition", "") == sw_value)
            if kind == "pause":
                use sw_form_row("Seconds"):
                    add session.field("duration", 110)
                    for sw_seconds in ("0.25", "0.5", "1.0", "2.0"):
                        textbutton sw_seconds style "sw_segment" yalign 0.5 action Function(session.change_field, "duration", sw_seconds) selected (session.fields.get("duration") == sw_seconds)
                    textbutton "Wait for click" style "sw_segment" yalign 0.5 action Function(session.change_field, "duration", "") selected (not session.fields.get("duration"))
            if kind in ("scene", "show"):
                textbutton ("Hide advanced" if session.advanced else "Advanced: inline motion, layer, stack order, alias") style "sw_link" action [SetField(session, "advanced", not session.advanced)]
                if session.advanced:
                    use sw_form_row("Inline motion", 88):
                        add session.field("atl", sw_field_w, 84, True)
                    use sw_form_row("Layer"):
                        add session.field("layer", 120)
                        fixed:
                            xysize (84, 40)
                            text "stack order" size 12 color SW_MUTED yalign 0.5 xalign 1.0
                        add session.field("zorder", 70)
                        fixed:
                            xysize (40, 40)
                            text "alias" size 12 color SW_MUTED yalign 0.5 xalign 1.0
                        add session.field("tag", (sw_field_w - 120 - 84 - 70 - 40 - 32))

screen sw_detail_music(session, width):
    $ sw_operation = session.fields.get("operation", "play")
    use sw_detail_header("MUSIC CUE", SW_KIND_COLORS["music"], session.block.line)
    textbutton "Apply" style "sw_small" xpos width xanchor 1.0 ypos 0 action Function(session.apply)
    vbox:
        ypos 26 spacing 4
        use sw_form_row("Action", 34):
            for sw_value in ("play", "queue", "stop"):
                textbutton sw_value.title() style "sw_segment" yalign 0.5 selected (sw_operation == sw_value) action Function(session.change_field, "operation", sw_value)
            null width 14
            text "channel" size 12 color SW_MUTED yalign 0.5
            for sw_channel in ("music", "sound", "voice"):
                textbutton sw_channel style "sw_segment" yalign 0.5 selected (session.fields.get("channel") == sw_channel) action Function(session.change_field, "channel", sw_channel)
        if sw_operation != "stop":
            use sw_form_row("Track"):
                textbutton sw_fit(session.fields.get("track", "") or "Choose a track…", 240, 15) style "sw_primary" yalign 0.5 action Function(session.open_modal, "music")
                textbutton "Listen" yalign 0.5 action Function(session.audition)
                textbutton "Stop listening" yalign 0.5 action Function(session.stop_audition) sensitive session.auditioning
        use sw_form_row("Timing"):
            if sw_operation != "stop":
                text "fade in" size 12 color SW_MUTED yalign 0.5
                add session.field("fadein", 70)
            if sw_operation in ("play", "stop"):
                text "fade out" size 12 color SW_MUTED yalign 0.5
                add session.field("fadeout", 70)
            if sw_operation != "stop":
                text "volume 0–1" size 12 color SW_MUTED yalign 0.5
                add session.field("volume", 70)
        if sw_operation != "stop":
            use sw_form_row("Loop", 34):
                for sw_value, sw_label in (("default", "Channel default"), ("loop", "Loop"), ("noloop", "Play once")):
                    textbutton sw_label style "sw_segment" yalign 0.5 selected (session.fields.get("loop", "default") == sw_value) action Function(session.change_field, "loop", sw_value)
        use sw_form_row("Writes", 30):
            text sw_fit(session.block.raw.strip(), (width - 110), 13) size 13 color "#9fb0a8" yalign 0.5

screen sw_detail_other(session, width):
    $ block = session.block
    $ sw_tag, sw_tag_color, sw_summary, sw_summary_color, sw_depth = session.row_parts(block)
    $ sw_title = {"label": "SCENE LABEL", "branch": "BRANCH", "note": "NOTE", "logic": "PRESERVED SOURCE", "nier": "NIER PROSE"}.get(sw_tag, sw_tag.upper())
    $ sw_explain = {
        "label": "The first beat of this scene goes directly after its label. Insert it from the palette.",
        "branch": "Choices and conditions stay exactly as written. Select a beat inside the branch to edit it.",
        "note": "A source comment, kept as written.",
        "logic": "Kept byte for byte. It cannot be edited here, and Read Scene stops before it.",
        "nier": {"nier_enter": "Starts Nier prose: the screen clears and the following textboxes accumulate on one page.",
            "nier_clear": "Clears the Nier page. The next textbox starts a fresh page.",
            "nier_exit": "Returns from Nier prose to the normal textbox."}.get(block.kind, ""),
        }.get(sw_tag, "")
    use sw_detail_header(sw_title, sw_tag_color, block.line)
    text sw_caption(sw_explain) ypos 24 size 14 color SW_MUTED xmaximum width
    frame:
        ypos 70 xysize (width, 196)
        background Solid("#11171d")
        padding (10, 8)
        viewport:
            mousewheel True
            scrollbars "vertical"
            text sw_caption(block.raw.rstrip("\r\n").replace("\t", "    ")) size 14 color "#c5d0ca"

style sw_text is gui_text:
    font "DejaVuSans.ttf"
    color "#eee7db"
    size 18
    outlines []

style sw_button is button:
    background Solid("#2e3a41")
    hover_background Solid("#44585a")
    selected_background Solid("#3d5f58")
    insensitive_background Solid("#1f272d")
    padding (11, 7)
    # `is button` inherits gui.button_height as a 40px minimum and maximum;
    # height here comes from padding so small and segment buttons stay small.
    xminimum 0
    yminimum 0
    xmaximum None
    ymaximum None

style sw_button_text is sw_text:
    size 15
    color "#e6dfd3"
    hover_color "#ffffff"
    selected_color "#d6fbe8"
    insensitive_color "#5f6d6b"
    xalign 0.5

style sw_primary is sw_button:
    background Solid("#3f6a5f")
    hover_background Solid("#548a7b")

style sw_primary_text is sw_button_text:
    color "#f2fff7"

style sw_small is sw_button:
    padding (8, 3)

style sw_small_text is sw_button_text:
    size 13

style sw_small_danger is sw_small:
    hover_background Solid("#7a3d38")

style sw_small_danger_text is sw_small_text

style sw_small_warn is sw_small:
    background Solid("#5a4726")
    hover_background Solid("#7a6232")

style sw_small_warn_text is sw_small_text:
    color "#ffe7c2"

# A plain `background` expands to every state and hides the inherited hover and
# selected backgrounds, so styles that set one restate the states they need.
style sw_segment is sw_button:
    background Solid("#253038")
    insensitive_background Solid("#1c242a")
    hover_background Solid("#3a4b52")
    selected_background Solid("#3f6a5f")
    selected_hover_background Solid("#548a7b")
    padding (8, 4)

style sw_segment_text is sw_button_text:
    size 13
    selected_color "#ffffff"

style sw_link is sw_button:
    background None
    hover_background Solid("#253038")
    padding (4, 3)

style sw_link_text is sw_button_text:
    size 13
    color "#9fc8bb"

style sw_vscrollbar is vscrollbar:
    xsize 8
    base_bar Solid("#151c22")
    # Bar uses the thumb's rendered height, so a minimum keeps it grabbable on a
    # 1,100-beat chapter where the proportional size would be two pixels.
    thumb Window(Null(), style="empty", background=Solid("#5d7a75"), yminimum=28, xfill=True, yfill=True)
    unscrollable "hide"

style sw_viewport is viewport
style sw_vpgrid is vpgrid
