# Core input behavior, reused DDLC assets, and shared story state.
# ENTER M's cast, audio catalog, and backgrounds extend these definitions in
# asset_definitions/. Only legacy Monika poses used by the phone and OP remain.

init python:
    config.keymap['game_menu'].remove('mouseup_3')
    config.keymap['hide_windows'].append('mouseup_3')
    config.keymap['self_voicing'] = []
    config.keymap['clipboard_voicing'] = []
    config.keymap['toggle_skip'] = []

    def delete_all_saves():
        for savegame in renpy.list_saved_games(fast=True):
            renpy.unlink_save(savegame)

    def pause(time=None):
        """Pause the story while suppressing the dialogue window."""
        global _windows_hidden
        if not time:
            _windows_hidden = True
            renpy.ui.saybehavior(afm=" ")
            renpy.ui.interact(mouse='pause', type='pause', roll_forward=None)
            _windows_hidden = False
            return
        if time <= 0:
            return
        _windows_hidden = True
        renpy.pause(time)
        _windows_hidden = False

# Reused cues: Purgatorium ambience and the shared poem presentation.
define -50 audio.ghostmenu = "<loop 0>assets/audio/bgm/ghostmenu.ogg"
define -50 audio.hb = "<loop 0>assets/audio/bgm/heartbeat.ogg"
define -50 audio.page_turn = "assets/audio/sfx/pageflip.ogg"

image black = "#000000"
image darkred = "#110000c8"
image white = "#ffffff"

image bg residential_day = "assets/backgrounds/residential.png"
image bg class_day = "assets/backgrounds/class.png"
image bg corridor = "assets/backgrounds/corridor.png"
image bg club_day = "assets/backgrounds/club.png"
image bg closet = "assets/backgrounds/closet.png"
image bg bedroom = "assets/backgrounds/bedroom.png"
image bg house = "assets/backgrounds/house.png"
image bg kitchen = "assets/backgrounds/kitchen.png"
image bg glitch = LiveTile("assets/backgrounds/glitch.jpg")

# Numeric poses used by phone portraits and the opening's illustrated cards.
# Flatten applies parent fades once to the composed sprite, including overlaps.
image monika 1a = Flatten(Composite((960, 960), (0, 0), "assets/characters/monika/1l.png", (0, 0), "assets/characters/monika/1r.png", (0, 0), "assets/characters/monika/a.png"))
image monika 1p = Flatten(Composite((960, 960), (0, 0), "assets/characters/monika/1l.png", (0, 0), "assets/characters/monika/1r.png", (0, 0), "assets/characters/monika/p.png"))
image monika 2c = Flatten(Composite((960, 960), (0, 0), "assets/characters/monika/1l.png", (0, 0), "assets/characters/monika/2r.png", (0, 0), "assets/characters/monika/c.png"))
image monika 2g = Flatten(Composite((960, 960), (0, 0), "assets/characters/monika/1l.png", (0, 0), "assets/characters/monika/2r.png", (0, 0), "assets/characters/monika/g.png"))

# Monika's main-story poses are defined by mpt/monika_layeredimage.rpy.
define narrator = Character(ctc="ctc", ctc_position="fixed")
define mc = DynamicCharacter('player', image='mc', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define m = DynamicCharacter('m_name', image='monika', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")

# Retained by the modified load handler, poem hint, and save metadata.
default persistent.anticheat = 0
default persistent.first_poem = None
default anticheat = 0
define config.mouse = None
default chapter = 0
default m_name = "Monika"
