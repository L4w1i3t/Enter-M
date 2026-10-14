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

# Pre-fight callers pass prefight=True explicitly: do not infer it from a
# leftover battle object. Resume only hides this overlay; confirmed setup exit
# returns a distinct token that callers handle before constructing a battle.
screen msbf_pause_menu(prefight=False):
    modal True

    # Screen-local confirm state for the Quit Fight two-step.
    default mp_confirm = False

    # Read the fight mode for the subtitle without assuming the var is defaulted.
    $ mp_id = getattr(store, "_msbf_id_mode", False)

    # The live painted arena remains visible behind the modal material.
    add Solid("#02050ade")

    frame:
        style "msbf_pause_frame"
        xsize 760
        ysize 640
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
                    background None
                    padding (0, 0)
                    hbox:
                        spacing 13
                        yalign 0.5
                        add MSBF_SEER_ART + "sigil.png" xysize (38, 38) yalign 0.5
                        text ("SETUP PAUSED" if prefight else "COMBAT PAUSED") style "msbf_pause_title"

            text ("ONTOLOGICAL SEER // ID MODE" if mp_id else "ONTOLOGICAL SEER // NORMAL"):
                style "msbf_pause_meta"
                xoffset 4

            add (MSBF_SEER_ART + "divider.png") xysize (700, 2)

            null height 2

            # --- Audio panel (live -- adjusts the running fight's mix). ---
            frame:
                style "msbf_pause_panel"
                xsize 700
                vbox:
                    spacing 8

                    hbox:
                        spacing 10
                        add Solid("#d6bf87") xysize (3, 20) yalign 0.5
                        text "AUDIO" style "msbf_pause_label"

                    if config.has_music:
                        text "Music" style "msbf_pause_small"
                        bar value Preference("music volume") style "pref_wide_slider"

                    if config.has_sound:
                        text "Sound" style "msbf_pause_small"
                        bar value Preference("sound volume") style "pref_wide_slider"

                    if config.has_voice:
                        text "Voice" style "msbf_pause_small"
                        bar value Preference("voice volume") style "pref_wide_slider"

                    if config.has_music or config.has_sound or config.has_voice:
                        null height 2
                        textbutton _("Mute All"):
                            style "msbf_pause_mute"
                            xsize 180
                            action Preference("all mute", "toggle")

            # --- Battle art (live -- the stage reads it every frame). ---
            # Pixel sprites or the original illustrations; the choreography,
            # effects and glitches are the same either way.
            frame:
                style "msbf_pause_panel"
                xsize 700
                hbox:
                    spacing 14
                    hbox:
                        spacing 10
                        yalign 0.5
                        add Solid("#d6bf87") xysize (3, 20) yalign 0.5
                        text "BATTLE ART" style "msbf_pause_label"
                    null width 18
                    textbutton _("Pixel"):
                        id "msbf_pause_art_pixel"
                        style "msbf_pause_choice"
                        yalign 0.5
                        action SetField(persistent, "msbf_seer_art", "pixel")
                    textbutton _("Illustrated"):
                        id "msbf_pause_art_hq"
                        style "msbf_pause_choice"
                        yalign 0.5
                        action SetField(persistent, "msbf_seer_art", "hq")

            null height 6

            # --- Action row: Resume / Quit Fight. ---
            hbox:
                xalign 0.5
                spacing 28
                textbutton _("Resume"):
                    id "msbf_pause_resume"
                    style "msbf_pause_button"
                    action Hide("msbf_pause_menu")
                textbutton (_("Leave Setup") if prefight else _("Quit Fight")):
                    id "msbf_pause_leave"
                    style "msbf_pause_quit_button"
                    action SetScreenVariable("mp_confirm", True)

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
            style "msbf_pause_frame"
            xsize 620
            ysize 240
            at archive_frame_enter()
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 18
                text ("Leave fight setup?" if prefight else "Abandon this fight?"):
                    style "msbf_pause_label"
                    xalign 0.5
                text ("No fight will be started. Your party selection will be discarded." if prefight else "Your progress in this fight will be lost."):
                    style "msbf_pause_small"
                    xalign 0.5
                null height 4
                hbox:
                    xalign 0.5
                    spacing 28
                    textbutton (_("Leave") if prefight else _("Quit")):
                        id "msbf_pause_confirm_quit"
                        style "msbf_pause_quit_button"
                        action [Hide("msbf_pause_menu"), Return("cancel_setup" if prefight else "quit")]
                    textbutton _("Cancel"):
                        id "msbf_pause_confirm_cancel"
                        style "msbf_pause_button"
                        action SetScreenVariable("mp_confirm", False)
        use console_brackets(330, 240, 620, 240, "#ff315b7a", 20, 2)
        key "K_ESCAPE" action SetScreenVariable("mp_confirm", False)
        key "game_menu" action SetScreenVariable("mp_confirm", False)


# --- CANCEL SETUP -----------------------------------------------------------
# Both callers test this token immediately after the notice and the picker.
# No battle has been constructed and _msbf_prev_quick_menu is not initialized
# for this run yet, so this is deliberately separate from msbf_forfeit.
label msbf_cancel_setup:
    hide screen msbf_pause_menu
    hide screen msbf_keyboard_notice
    hide screen msbf_party_select
    $ msbf_clear_battle_watch()
    $ msbf_stop_battle_music(0.35)
    $ _msbf_party_ids = None
    scene black with dissolve_scene_full
    if arcade_active:
        jump arcade_return
    return


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
style msbf_pause_quit_button is msbf_pause_button:
    hover_background msbf_seer_frame(True, True)
    xsize 180

style msbf_pause_quit_button_text is msbf_pause_button_text:
    hover_color "#ff8fa6"

# Fight-local materials and type. Keep the established pause geometry and
# actions; these styles do not modify Archive or Arcade's shared presentation.
style msbf_pause_frame is empty:
    xalign 0.5
    yalign 0.5
    background msbf_seer_frame()
    padding (30, 22)

style msbf_pause_title is default:
    font "assets/gui/font/Aller_Rg.ttf"
    size 36
    color "#f4e8cf"
    bold True
    outlines []

style msbf_pause_meta is default:
    font "assets/gui/font/Aller_Rg.ttf"
    size 12
    color "#cbb68b"
    kerning 1.0
    outlines []

style msbf_pause_panel is empty:
    background msbf_seer_frame()
    padding (18, 18)

style msbf_pause_label is default:
    font "assets/gui/font/Aller_Rg.ttf"
    size 20
    color "#f4e8cf"
    bold True
    outlines []

style msbf_pause_small is default:
    font "assets/gui/font/Aller_Rg.ttf"
    size 14
    color "#bacbd6"
    outlines []

style msbf_pause_button is button:
    xsize 190
    ysize 54
    background msbf_seer_frame(command=True)
    hover_background msbf_seer_frame(True, True)
    padding (18, 10)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style msbf_pause_button_text is default:
    font "assets/gui/font/Aller_Rg.ttf"
    size 22
    color "#f4e8cf"
    hover_color "#ffffff"
    bold True

style msbf_pause_mute is msbf_pause_button:
    xsize 126
    ysize 42
    padding (15, 8)

style msbf_pause_mute_text is msbf_pause_button_text:
    size 20
    bold False

# The Battle Art pair: the chosen style stays lit.
style msbf_pause_choice is msbf_pause_mute:
    xsize 170
    selected_background msbf_seer_frame(True, True)

style msbf_pause_choice_text is msbf_pause_mute_text:
    xalign 0.5
    selected_color "#ffd98a"
