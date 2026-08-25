##### DEVTOOLS #####
##### Disable these when building your mod
define config.developer = "auto"
define config.autoreload = "auto"

#### Define/Default Variables found in Definitions.RPY that have multiple uses across the template,
#### and were rather hidden deep in the files, so we moved it here for ease-of-access. ####
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
