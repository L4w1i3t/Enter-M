# Story Writer dialogs: one overlay pattern for every chooser and confirmation.
# The dialog frame is modal, so a click inside it never falls through to the
# dismiss layer; only a click outside the frame (or Escape) closes it.
screen sw_modal(session):
    # These keys outrank the workspace's, and frame modality only blocks the
    # mouse, so writer shortcuts are explicitly held while a dialog is open.
    key ["ctrl_K_s", "K_F5", "ctrl_K_RETURN", "ctrl_K_KP_ENTER", "ctrl_K_UP", "ctrl_K_DOWN",
        "alt_K_UP", "alt_K_DOWN", "ctrl_K_z", "ctrl_K_y", "ctrl_K_o"] action NullAction()
    key "K_ESCAPE" action Function(session.close_modal)

    $ sw_compact = session.modal in ("confirm", "preview_setup", "new", "destination")
    $ sw_dialog_w, sw_dialog_h = (760, 440) if sw_compact else (1040, 610)
    $ sw_body_w, sw_body_h = sw_dialog_w - 48, sw_dialog_h - 36 - 48
    $ sw_asset_titles = {"attributes": "Choose an expression", "edit": "Replace the image", "insert": "Choose an image to insert"}
    $ sw_title = {"files": "Open a story file", "drafts": "Drafts", "outline": "Outline",
        "new": "New scene", "destination": "Save the new scene", "speakers": "Speaker",
        "music": "Music library", "insert": "Insert", "source": "Source",
        "preview_setup": "Where should the reading start?",
        "assets": sw_asset_titles.get(session.asset_target, "Images"),
        "confirm": (session.confirm or {}).get("title", "Confirm")}.get(session.modal, "Story Writer")

    add Solid("#05090ee0")
    button:
        xfill True yfill True
        background None hover_background None
        action Function(session.close_modal)
    frame:
        modal True
        xalign 0.5 yalign 0.5 xysize (sw_dialog_w, sw_dialog_h)
        padding (24, 18)
        background Solid("#1f2830")
        fixed:
            text sw_fit(sw_title, (sw_body_w - 110), 20, SW_FONT_BOLD) size 20 font SW_FONT_BOLD color SW_INK
            textbutton "Close" style "sw_small" xpos sw_body_w xanchor 1.0 action Function(session.close_modal)
            fixed:
                ypos 48 xysize (sw_body_w, sw_body_h)
                if session.modal == "files":
                    use sw_dialog_files(session, sw_body_w, sw_body_h)
                elif session.modal == "drafts":
                    use sw_dialog_drafts(session, sw_body_w, sw_body_h)
                elif session.modal == "outline":
                    use sw_dialog_outline(session, sw_body_w, sw_body_h)
                elif session.modal in ("new", "destination"):
                    use sw_dialog_new(session, sw_body_w, sw_body_h)
                elif session.modal == "insert":
                    text ("Insert after line %d." % session.block.line) size 14 color SW_MUTED
                    use sw_palette(session, 0, 34, session.insert_allowed())
                elif session.modal == "speakers":
                    use sw_dialog_speakers(session, sw_body_w, sw_body_h)
                elif session.modal == "music":
                    use sw_dialog_music(session, sw_body_w, sw_body_h)
                elif session.modal == "source":
                    use sw_dialog_source(session, sw_body_w, sw_body_h)
                elif session.modal == "preview_setup":
                    use sw_dialog_preview_setup(session, sw_body_w, sw_body_h)
                elif session.modal == "confirm":
                    use sw_dialog_confirm(session, sw_body_w, sw_body_h)
                elif session.modal == "assets":
                    use sw_dialog_assets(session, sw_body_w, sw_body_h)

screen sw_dialog_files(session, width, height):
    hbox:
        spacing 10
        add session.utility_field("search", 520)
        textbutton "Recover last draft" yalign 0.5 action Function(session.recover) sensitive _sw_os.path.isfile(session.draft_file)
        textbutton "All drafts" yalign 0.5 action Function(session.open_modal, "drafts")
    $ sw_files, sw_more = session.filtered("files")
    viewport:
        ypos 54 xysize (width, (height - 54))
        mousewheel True
        scrollbars "vertical"
        vbox:
            spacing 3
            if not sw_files:
                text "No story files match." size 15 color SW_MUTED
            $ sw_folder = None
            for sw_file in sw_files:
                $ sw_parent = sw_file.rsplit("/", 1)[0] if "/" in sw_file else "story"
                if sw_parent != sw_folder:
                    $ sw_folder = sw_parent
                    null height 6
                    text sw_caption(sw_parent) size 12 font SW_FONT_BOLD color SW_MUTED
                textbutton sw_caption(sw_file.rsplit("/", 1)[-1]) style "sw_list" xsize (width - 16) action Function(session.open_file, sw_file) selected (("story/" + sw_file) == session.filename)

screen sw_dialog_drafts(session, width, height):
    text "Every file you have edited keeps its latest unsaved version here. Recovering never overwrites story source." size 13 color SW_MUTED xmaximum width
    viewport:
        ypos 30 xysize (width, (height - 30))
        mousewheel True
        scrollbars "vertical"
        vbox:
            spacing 3
            if not session.draft_catalog:
                text "Drafts appear here once you have written something." size 15 color SW_MUTED
            for sw_draft_path, sw_draft_name in session.draft_catalog:
                textbutton sw_fit(sw_draft_name, (width - 60), 15) style "sw_list" xsize (width - 16) action Function(session.recover, sw_draft_path)

screen sw_dialog_outline(session, width, height):
    $ sw_here = session.outline_here()
    text "Labels, scene changes, branches and Nier sections. Select one to jump there." size 13 color SW_MUTED
    viewport:
        ypos 28 xysize (width, (height - 28))
        mousewheel True
        scrollbars "vertical"
        vbox:
            spacing 3
            for sw_entry in session.outline_blocks():
                $ sw_tag, sw_color, sw_summary, sw_unused, sw_depth = session.row_parts(sw_entry)
                $ sw_indent = 18 * min(sw_depth, 5)
                button:
                    style "sw_list"
                    xsize (width - 16)
                    selected (sw_entry.uid == sw_here)
                    action [Function(session.close_modal), Function(session.select, sw_entry.uid)]
                    fixed:
                        ysize 22
                        text str(sw_entry.line) xpos 42 xanchor 1.0 yalign 0.5 size 13 color "#6d7b7e"
                        text sw_fit(sw_tag, 70, 13) xpos 54 yalign 0.5 size 13 color sw_color
                        text sw_fit(sw_summary, (width - 180 - sw_indent), 15) xpos (136 + sw_indent) yalign 0.5 size 15 color SW_INK
                        if sw_entry.uid == sw_here:
                            text "you are here" xpos (width - 44) xanchor 1.0 yalign 0.5 size 12 color SW_ACCENT

screen sw_dialog_new(session, width, height):
    $ sw_problem = session.new_problem()
    $ sw_folder_now = session.new_path.replace("\\", "/").rsplit("/", 1)[0] if "/" in session.new_path else ""
    text "Folder" size 13 color SW_MUTED
    hbox:
        ypos 20 spacing 6
        for sw_folder in session.story_folders():
            textbutton sw_caption(sw_folder) style "sw_segment" selected (sw_folder == sw_folder_now) action Function(session.set_new_folder, sw_folder)
    text "File inside game/story" ypos 66 size 13 color SW_MUTED
    add session.utility_field("new_path", width) ypos 86
    if session.modal == "new":
        text "Scene label" ypos 140 size 13 color SW_MUTED
        add session.utility_field("new_label", 360) ypos 160
        text "Follows the file name until you type your own." xpos 376 ypos 172 size 12 color "#7c898b"
    text (sw_caption(sw_problem) if sw_problem else "Ready.") ypos 220 size 14 color (SW_ERROR if sw_problem else SW_ACCENT) xmaximum width
    hbox:
        ypos 256 spacing 8
        textbutton ("Create scene" if session.modal == "new" else "Save source") style "sw_primary" action Function(session.create_new if session.modal == "new" else session.choose_destination) sensitive (not sw_problem)
        textbutton "Cancel" action Function(session.close_modal)
    text "The writer makes ordinary .rpy source. Connecting the scene to a route happens in the story code." ypos 318 size 13 color SW_MUTED xmaximum width

screen sw_dialog_speakers(session, width, height):
    $ sw_current = session.fields.get("speaker", "")
    $ sw_cell = (width - 28) // 3
    vpgrid:
        cols 3
        spacing 6
        xysize (width, height)
        mousewheel True
        scrollbars "vertical"
        allow_underfull True
        textbutton "Narration" style "sw_list" xsize sw_cell action Function(session.pick_speaker, "") selected (not sw_current)
        textbutton "Nier prose" style "sw_list" xsize sw_cell action Function(session.pick_speaker, "nier") selected (sw_current == "nier")
        for sw_alias, sw_name in session.speakers:
            if sw_alias and sw_alias != "nier":
                textbutton sw_fit(sw_name + "  ·  " + sw_alias, (sw_cell - 26), 15) style "sw_list" xsize sw_cell action Function(session.pick_speaker, sw_alias) selected (sw_current == sw_alias)

screen sw_dialog_music(session, width, height):
    $ sw_tracks, sw_more = session.filtered("music")
    $ sw_purpose = {"insert_play": "Choosing a track plays it after line %d." % session.block.line,
        "insert_queue": "Choosing a track queues it after line %d." % session.block.line,
        "edit": "Choosing a track changes this cue."}.get(session.music_target, "Listen to tracks here. Choosing one sets the default for new cues.")
    hbox:
        spacing 10
        add session.utility_field("search", 520)
        textbutton "Stop listening" yalign 0.5 action Function(session.stop_audition) sensitive session.auditioning
    text sw_caption(sw_purpose) ypos 50 size 13 color SW_MUTED
    viewport:
        ypos 76 xysize (width, (height - 76))
        mousewheel True
        scrollbars "vertical"
        vbox:
            spacing 3
            if not sw_tracks:
                text "No tracks match." size 15 color SW_MUTED
            for sw_alias, sw_path in sw_tracks:
                hbox:
                    spacing 6
                    button:
                        style "sw_list"
                        xsize (width - 16 - 96 - 6)
                        action Function(session.pick_music, sw_alias)
                        fixed:
                            ysize 22
                            text sw_fit(sw_alias, 250, 15) yalign 0.5 size 15 color SW_INK
                            text sw_fit(sw_path, (width - 16 - 96 - 6 - 300), 12) xpos 270 yalign 0.5 size 12 color SW_MUTED
                    textbutton "Listen" xsize 96 action Function(session.audition, sw_alias)
            if sw_more:
                text ("%d more. Refine the search." % sw_more) size 13 color SW_MUTED

screen sw_dialog_source(session, width, height):
    hbox:
        spacing 12
        textbutton "Export .rpy copy" style "sw_primary" action Function(session.export_source)
        text "Source around the selected beat. Copies go to dev/story_writer/exports and are never loaded by the game." size 13 color SW_MUTED yalign 0.5 xmaximum (width - 200)
    frame:
        ypos 54 xysize (width, (height - 54))
        background Solid("#11171d")
        padding (8, 8)
        viewport:
            mousewheel True
            scrollbars "vertical"
            vbox:
                for sw_number, sw_line, sw_is_here in session.source_context():
                    fixed:
                        xysize ((width - 40), 20)
                        if sw_is_here:
                            add Solid("#2a3f42")
                        text str(sw_number) xpos 44 xanchor 1.0 size 13 color (SW_ACCENT if sw_is_here else "#5f6d6b")
                        text sw_caption(sw_line) xpos 56 size 14 layout "nobreak" color ("#f4eee4" if sw_is_here else "#b8c2bd")

screen sw_dialog_preview_setup(session, width, height):
    $ sw_warning = session.plan.get("warning", "") if isinstance(session.plan, dict) else ""
    text sw_caption(sw_warning or "This beat follows logic that the writer does not run.") size 16 color SW_WARN xmaximum width
    text "Start a visual rehearsal at this beat on an empty stage. Existing Python and branch conditions stay unexecuted." ypos 90 size 15 color SW_INK xmaximum width
    hbox:
        ypos 190 spacing 8
        textbutton "Start here on an empty stage" style "sw_primary" action Function(session.play, True)
        textbutton "Cancel" action Function(session.close_modal)

screen sw_dialog_confirm(session, width, height):
    $ sw_confirm = session.confirm or {}
    text sw_caption(sw_confirm.get("message", "")) size 15 color SW_INK xmaximum width
    hbox:
        ypos (height - 44) spacing 8
        textbutton sw_caption(sw_confirm.get("label", "Continue")) style "sw_primary" action Function(session.confirm_accept)
        textbutton "Keep editing" action Function(session.close_modal)

screen sw_dialog_assets(session, width, height):
    $ cast = session.asset_mode == "cast"
    $ sw_result = session.asset_result()
    $ sw_action = {"insert": "Insert after line %d" % session.block.line, "edit": "Use this image",
        "attributes": "Use this expression"}.get(session.asset_target, "Use selection")
    $ sw_writes = (" ".join(session.minimal_attributes(sw_result)) or "no change") if (session.asset_target == "attributes" and sw_result) else sw_result
    hbox:
        spacing 6
        for sw_mode, sw_mode_title in (("backgrounds", "Backgrounds"), ("cast", "Characters"), ("all", "All images")):
            textbutton sw_mode_title style "sw_segment" selected (session.asset_mode == sw_mode) action Function(session.set_asset_mode, sw_mode) sensitive (session.asset_target != "attributes" or sw_mode == "cast")
    text sw_fit("Writes: " + (sw_writes or "nothing selected"), 360, 13) xpos (width - 230) xanchor 1.0 ypos 6 size 13 color SW_MUTED
    textbutton sw_action style "sw_primary" xpos width xanchor 1.0 action Function(session.use_asset) sensitive bool(sw_result)

    add session.utility_field("search", 300) ypos 46
    viewport:
        ypos 96 xysize (300, (height - 96))
        mousewheel True
        scrollbars "vertical"
        vbox:
            spacing 2
            if cast:
                $ sw_items, sw_more = session.filtered("cast")
                for sw_tag in sw_items:
                    textbutton sw_caption(sw_tag) style "sw_list" xsize 284 action Function(dev_sprite_select_tag, sw_tag) selected (_dev_sprite.tag == sw_tag)
            else:
                $ sw_items, sw_more = session.filtered("images")
                for sw_name in sw_items:
                    textbutton sw_fit(sw_name, 250, 14) style "sw_list" xsize 284 action Function(session.pick_asset, sw_name) selected (session.asset_name == sw_name)
            if sw_more:
                text ("%d more. Refine the search." % sw_more) size 13 color SW_MUTED

    $ sw_preview_w = 340 if cast else (width - 316)
    fixed:
        xpos 316 ypos 46 xysize (sw_preview_w, (height - 46))
        add Solid("#11171d")
        if cast and _dev_sprite.tag:
            add SWPreviewSurface(dev_sprite_displayable(sw_preview_w, (height - 56)), sw_preview_w, (height - 56)) xalign 0.5 yalign 1.0
        elif (not cast) and session.asset_name:
            add SWPreviewSurface(Transform(ImageReference(session.asset_name), fit="contain", xysize=(sw_preview_w, (height - 46))), sw_preview_w, (height - 46)) xalign 0.5 yalign 0.5

    if cast and _dev_sprite.tag:
        $ sw_rig = dev_sprite_current_rig()
        $ sw_look = dev_sprite_look(_dev_sprite.tag)
        viewport:
            xpos 672 ypos 46 xysize ((width - 672), (height - 46))
            mousewheel True
            scrollbars "vertical"
            vbox:
                spacing 6
                if len(sw_look.get("rigs", [])) > 1:
                    text "Pose" size 12 color SW_MUTED
                    hbox:
                        spacing 4
                        for sw_index, sw_rig_entry in enumerate(sw_look["rigs"]):
                            textbutton sw_caption(" ".join(sw_rig_entry[0]) or "default") style "sw_segment" action Function(dev_sprite_select_rig, sw_index) selected (_dev_sprite.rig == sw_index and _dev_sprite.variant is None)
                if sw_rig:
                    for sw_group, sw_values in sw_rig["groups"]:
                        text sw_caption(sw_group) size 12 color SW_MUTED
                        vpgrid:
                            cols 2
                            spacing 3
                            allow_underfull True
                            for sw_attribute in sw_values:
                                textbutton sw_fit(sw_attribute, 120, 12) style "sw_chip" xsize 146 action Function(dev_sprite_set, sw_group, sw_attribute) selected (_dev_sprite.groups.get(sw_group) == sw_attribute and _dev_sprite.variant is None)
                            if sw_group not in sw_rig["defaults"]:
                                textbutton "none" style "sw_chip" xsize 146 action Function(dev_sprite_clear, sw_group) selected (sw_group not in _dev_sprite.groups)
                    if sw_rig.get("free"):
                        text "Optional" size 12 color SW_MUTED
                        vpgrid:
                            cols 2
                            spacing 3
                            allow_underfull True
                            for sw_attribute in sw_rig["free"]:
                                textbutton sw_fit(sw_attribute, 120, 12) style "sw_chip" xsize 146 action Function(dev_sprite_toggle_free, sw_attribute) selected (sw_attribute in _dev_sprite.free)
                if sw_look.get("variants"):
                    text "Full-body variants" size 12 color SW_MUTED
                    for sw_variant in sw_look["variants"]:
                        textbutton sw_fit(" ".join(sw_variant), 260, 12) style "sw_chip" xsize 296 action Function(dev_sprite_set_variant, sw_variant) selected (_dev_sprite.variant == tuple(sw_variant))
                $ sw_bad = dev_sprite_unsatisfied()
                if sw_bad:
                    text sw_caption("Draws nothing in this combination: " + ", ".join(str(item) for item in sw_bad)) size 12 color SW_WARN xmaximum 290

style sw_list is sw_button:
    background Solid("#26313a")
    hover_background Solid("#34454d")
    selected_background Solid("#2f4d49")
    selected_hover_background Solid("#3d615b")
    padding (12, 6)

style sw_list_text is sw_button_text:
    xalign 0.0

style sw_chip is sw_button:
    background Solid("#26313a")
    hover_background Solid("#34454d")
    selected_background Solid("#3f6a5f")
    selected_hover_background Solid("#548a7b")
    padding (6, 4)

style sw_chip_text is sw_button_text:
    size 12
