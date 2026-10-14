# Arcade games execute in a child gameplay context. A title menu's identity
# must not follow them: Return(None) would otherwise show the title on top of
# a still-running call screen instead of returning from a nested pause menu.

init -5 python:
    def arcade_launch(label_name, **launch_kwargs):
        # The transition must be queued after the child context is created:
        # entering a context clears the interface's in-flight transitions.
        # `arcade_run_context` does that before launch prep, while the inherited
        # screens layer keeps the cabinet/variant screen available as its old
        # frame.
        renpy.call_in_new_context(
            "arcade_run_context",
            label_name,
            launch_kwargs,
            _clear_layers=["top", "bottom"],
        )
        # Screen Function actions must not propagate a child's return value
        # into the parent hub interaction.
        return None

label arcade_run_context(run_label, run_kwargs):
    $ renpy.transition(enter_m_menu_doorway)
    python:
        # The SDK restores these store values when this context exits, even
        # when a cabinet's script returns through its own cleanup labels.
        renpy.context_dynamic("main_menu", "_menu", "_game_menu_screen",
            "quick_menu", "arcade_active")
        main_menu = False
        _menu = False
        _game_menu_screen = None
        quick_menu = False
        arcade_active = True
        # Context info is copied by the SDK, not shared with the parent.
        renpy.context()._menu = False
        renpy.context()._main_menu = False

    call expression run_label pass (**run_kwargs) from _call_arcade_context_game
    return
