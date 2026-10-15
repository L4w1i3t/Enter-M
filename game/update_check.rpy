# Optional release notification. Network work begins only when the title screen
# is shown; no requests during init, screen prediction, loading, or gameplay.
init python:
    import enter_m_updates

    def enter_m_check_updates():
        # Ren'Py worker threads are unavailable in browser builds.
        if renpy.emscripten:
            return
        enter_m_updates.checker.start(
            config.version,
            renpy.invoke_in_thread,
            renpy.invoke_in_main_thread,
            renpy.restart_interaction,
        )
