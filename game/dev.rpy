##### DEVTOOLS #####
##### Disable these when building your mod
define config.developer = True
define config.autoreload = True
default persistent.demo = False
default persistent.steam = ("steamapps" in config.basedir.lower())

#### Define/Default Variables found in Definitions.RPY that have multiple uses across the template,
#### and were rather hidden deep in the files, so we moved it here for ease-of-access. ####
define _dismiss_pause = config.developer
default persistent.playername = ""
default player = persistent.playername
default persistent.playthrough = 0
default persistent.clear = [False, False, False, False, False, False, False, False, False, False]
default persistent.clearall = None
default persistent.first_load = None
default allow_skipping = True

# Checks for Singleton.py (Permits only one instance of a Ren'Py game to run at a time.)
python early:
    import singleton
    me = singleton.SingleInstance()
