# Developer mode follows the engine's source-build detection. This file also
# owns runtime defaults and singleton startup; keep it in release builds.
define config.developer = "auto"
define config.autoreload = "auto"

# Shared player, load-hint and skipping state.
define _dismiss_pause = config.developer
default persistent.playername = ""
default player = persistent.playername
default persistent.playthrough = 0
default persistent.first_load = None
default allow_skipping = True

# Checks for Singleton.py (Permits only one instance of a Matsu'Py game to run at a time.)
python early:
    import singleton
    me = singleton.SingleInstance()
