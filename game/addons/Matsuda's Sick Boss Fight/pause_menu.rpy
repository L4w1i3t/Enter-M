# =============================================================================
# MATSUDA BOSS-FIGHT PAUSE MENU
# =============================================================================
# The Matsuda fight (msbf_battle_screen, Normal + Id Mode) used to bind Escape to
# ShowMenu("preferences") -- which opens the full preferences screen WITH the game
# navigation sidebar (Main Menu / Save / Load) over a live, mutable battle state.
# "Main Menu" from there dumps you to the title WITHOUT the fight's teardown
# running (music/state never reset), and Save/Load can clobber a mid-fight state.
#
# This is a self-contained pause menu bound in place of that: bare essentials only
# -- Resume, live audio settings, and a SAFE "Quit Fight" that actually runs the
# teardown. It carries no Main Menu / Save / Load, so none of those hazards exist.
#
# HOW IT RESUMES / QUITS
#   The key binding in ui.rpy uses Show("msbf_pause_menu") -- a plain modal
#   OVERLAY on the running battle interaction, NOT the game-menu context. So:
#     Resume / Escape -> Hide("msbf_pause_menu"): the battle was never left.
#     Quit Fight      -> Return("quit"): ends the battle `call screen` normally;
#                        cs_matsuda_02_battle sees "quit" and jumps msbf_forfeit.
#   Nothing here enters the game menu, calls MainMenu(), or unwinds a context --
#   which is what previously dumped a call_in_new_context fight to the main menu.
# =============================================================================

screen msbf_pause_menu():
    modal True

    # Screen-local confirm state for the Quit Fight two-step.
    default mp_confirm = False

    # Read the fight mode for the subtitle without assuming the var is defaulted.
    $ mp_id = getattr(store, "_msbf_id_mode", False)

    # Dim the frozen battle underneath + a drifting scanline (never a full scene,
    # so the fight stays visible behind the panel).
    add Solid("#02050ade")
    add Solid("#56d7ff1c") xysize (1280, 2) at menu_scanline_slow

    frame:
        style "archive_frame"
        xsize 760
        ysize 540
        at archive_frame_enter()

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 14

            # --- Title bar (title-only; no Return button -- Resume is below). ---
            hbox:
                xfill True
                ysize 64
                frame:
                    style "archive_header_title_frame"
                    hbox:
                        spacing 13
                        yalign 0.5
                        add Solid("#56d7ff") xysize (11, 11) yalign 0.5 at console_blink
                        text "COMBAT PAUSED" style "archive_title"
                add Solid("#56d7ff") xysize (3, 46) yalign 0.5 xoffset 16 at enter_m_pip_pulse

            text ("ONTOLOGICAL SEER // ID MODE" if mp_id else "ONTOLOGICAL SEER // NORMAL"):
                style "archive_meta_text"
                xoffset 4

            add Solid("#56d7ff66") xysize (700, 2)

            null height 2

            # --- Audio panel (live -- adjusts the running fight's mix). ---
            frame:
                style "archive_panel"
                xsize 700
                vbox:
                    spacing 8

                    hbox:
                        spacing 10
                        add Solid("#56d7ff") xysize (4, 20) yalign 0.5
                        text "AUDIO" style "archive_panel_label"

                    if config.has_music:
                        text "Music" style "archive_panel_small"
                        bar value Preference("music volume") style "pref_wide_slider"

                    if config.has_sound:
                        text "Sound" style "archive_panel_small"
                        bar value Preference("sound volume") style "pref_wide_slider"

                    if config.has_voice:
                        text "Voice" style "archive_panel_small"
                        bar value Preference("voice volume") style "pref_wide_slider"

                    if config.has_music or config.has_sound or config.has_voice:
                        null height 2
                        textbutton _("Mute All"):
                            style "archive_return_button"
                            xsize 180
                            action Preference("all mute", "toggle")

            null height 6

            # --- Action row: Resume / Quit Fight. ---
            hbox:
                xalign 0.5
                spacing 28
                textbutton _("Resume"):
                    style "arcade_result_button"
                    action Hide("msbf_pause_menu")
                textbutton _("Quit Fight"):
                    style "msbf_pause_quit_button"
                    action SetScreenVariable("mp_confirm", True)

    use console_brackets(260, 90, 760, 540, "#56d7ff7a", 24, 2)

    # Escape / right-click resume the fight -- but only when the quit confirm is
    # not up (the confirm block below binds Escape to Cancel instead).
    if not mp_confirm:
        key "K_ESCAPE" action Hide("msbf_pause_menu")
        key "game_menu" action Hide("msbf_pause_menu")

    # --- Quit confirmation overlay -----------------------------------------------
    # Shown on top of the pause panel; forfeits by ending the battle `call screen`
    # with Return("quit"), which the fight dispatch routes to msbf_forfeit.
    if mp_confirm:
        add Solid("#02050aee")
        # Full-screen catcher: eats clicks that would otherwise fall through the
        # dim onto the Resume/Quit buttons underneath (Solids don't block input).
        button:
            xysize (1280, 720)
            action NullAction()
        frame:
            style "archive_frame"
            xsize 620
            ysize 240
            at archive_frame_enter()
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 18
                text "Abandon this fight?":
                    style "archive_item_text"
                    xalign 0.5
                text "Your progress in this fight will be lost.":
                    style "archive_panel_small"
                    xalign 0.5
                null height 4
                hbox:
                    xalign 0.5
                    spacing 28
                    textbutton _("Quit"):
                        style "msbf_pause_quit_button"
                        action [Hide("msbf_pause_menu"), Return("quit")]
                    textbutton _("Cancel"):
                        style "arcade_result_button"
                        action SetScreenVariable("mp_confirm", False)
        use console_brackets(330, 240, 620, 240, "#ff315b7a", 20, 2)
        key "K_ESCAPE" action SetScreenVariable("mp_confirm", False)
        key "game_menu" action SetScreenVariable("mp_confirm", False)


# --- SAFE FORFEIT ------------------------------------------------------------
# Reached from cs_matsuda_02_battle when the pause menu's Quit returns "quit".
# The battle `call screen` already returned (auto-hiding the fight screen) and the
# dispatch already ran teardown; the calls below are idempotent belt-and-braces.
# Then return -- unwinding to the story hub, or (arcade) through arcade_return to
# the Arcade hub with its music restored.
label msbf_forfeit:
    $ msbf_clear_battle_watch()
    $ msbf_stop_battle_music(1.5)
    $ quick_menu = _msbf_prev_quick_menu
    scene black with dissolve_scene_full
    if arcade_active:
        jump arcade_return
    return


# =============================================================================
# STYLES
# =============================================================================
# Red-accent danger button for Quit, otherwise mirroring the arcade result button.
style msbf_pause_quit_button is arcade_result_button:
    hover_background Solid("#3a0f1af2")
    xsize 180

style msbf_pause_quit_button_text is arcade_result_button_text:
    hover_color "#ff8fa6"
