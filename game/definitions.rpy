#### Definitions.RPY has been modified to coincide with definitions that are used by DDLC and not necessary for development of a modifcation.
#### You can change any of these as much as you like without ruining the development process.
#### It will only break certain actions inside of DDLC while you are changing scripts and debugging.

init python:
    config.keymap['game_menu'].remove('mouseup_3')
    config.keymap['hide_windows'].append('mouseup_3')
    config.keymap['self_voicing'] = []
    config.keymap['clipboard_voicing'] = []
    config.keymap['toggle_skip'] = []
    renpy.music.register_channel("music_poem", mixer="music", tight=True)
    def get_pos(channel='music'):
        pos = renpy.music.get_pos(channel=channel)
        if pos: return pos
        return 0
    def delete_all_saves():
        for savegame in renpy.list_saved_games(fast=True):
            renpy.unlink_save(savegame)
    def pause(time=None):
        global _windows_hidden
        if not time:
            _windows_hidden = True
            renpy.ui.saybehavior(afm=" ")
            renpy.ui.interact(mouse='pause', type='pause', roll_forward=None)
            _windows_hidden = False
            return
        if time <= 0: return
        _windows_hidden = True
        renpy.pause(time)
        _windows_hidden = False

#Definitions for Audio BGM and noises.
define -50 audio.t1 = "<loop 22.073>assets/audio/bgm/1.ogg"
define -50 audio.t2 = "<loop 4.499>assets/audio/bgm/2.ogg"
define -50 audio.t3 = "<loop 4.618>assets/audio/bgm/3.ogg"
define -50 audio.t4 = "<loop 19.451>assets/audio/bgm/4.ogg"
define -50 audio.t5 = "<loop 4.444>assets/audio/bgm/5.ogg"
define -50 audio.t6 = "<loop 10.893>assets/audio/bgm/6.ogg"
define -50 audio.t7 = "<loop 2.291>assets/audio/bgm/7.ogg"
define -50 audio.t8 = "<loop 9.938>assets/audio/bgm/8.ogg"
define -50 audio.t9 = "<loop 3.172>assets/audio/bgm/9.ogg"
define -50 audio.t9g = "<loop 1.532>assets/audio/bgm/9g.ogg"
define -50 audio.t10 = "<loop 5.861>assets/audio/bgm/10.ogg"
define -50 audio.td = "<loop 36.782>assets/audio/bgm/d.ogg"
define -50 audio.m1 = "<loop 0>assets/audio/bgm/m1.ogg"
define -50 audio.ghostmenu = "<loop 0>assets/audio/bgm/ghostmenu.ogg"
define -50 audio.g1 = "<loop 0>assets/audio/bgm/g1.ogg"
define -50 audio.g2 = "<loop 0>assets/audio/bgm/g2.ogg"
define -50 audio.hb = "<loop 0>assets/audio/bgm/heartbeat.ogg"
define -50 audio.closet_open = "assets/audio/sfx/closet-open.ogg"
define -50 audio.closet_close = "assets/audio/sfx/closet-close.ogg"
define -50 audio.page_turn = "assets/audio/sfx/pageflip.ogg"
define -50 audio.fall = "assets/audio/sfx/fall.ogg"

#Definitions for flashing still images, scene transition images.
image black = "#000000"
image dark = "#000000e4"
image darkred = "#110000c8"
image white = "#ffffff"
#Definition for Splash.rpy PNG.
image splash = "assets/images/bg/splash.png"
#Definition for End Card at the very end of the game, before the main menu is shown again.
image end:
    truecenter
    "assets/gui/end.png"
#Definitions for each Background in the game.
image bg residential_day = "assets/images/bg/residential.png"
image bg class_day = "assets/images/bg/class.png"
image bg corridor = "assets/images/bg/corridor.png"
image bg club_day = "assets/images/bg/club.png"
image bg club_day2:
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "bg club_day"
    choice:
        "assets/images/bg/club-skill.png"
image bg closet = "assets/images/bg/closet.png"
image bg bedroom = "assets/images/bg/bedroom.png"
image bg sayori_bedroom = "assets/images/bg/sayori_bedroom.png"
image bg house = "assets/images/bg/house.png"
image bg kitchen = "assets/images/bg/kitchen.png"
image bg notebook = "assets/images/bg/notebook.png"
image bg notebook-glitch = "assets/images/bg/notebook-glitch.png"
image bg glitch = LiveTile("assets/images/bg/glitch.jpg")

#Definitions for certain Glitch effects using PNGs in the /game/ assets.
image glitch_color:
    ytile 3
    zoom 2.5
    parallel:
        "assets/images/bg/glitch-red.png"
        0.1
        "assets/images/bg/glitch-green.png"
        0.1
        "assets/images/bg/glitch-blue.png"
        0.1
        repeat
    parallel:
        yoffset 720
        linear 0.5 yoffset 0
        repeat
    parallel:
        choice:
            xoffset 0
        choice:
            xoffset 10
        choice:
            xoffset 20
        choice:
            xoffset 35
        choice:
            xoffset -10
        choice:
            xoffset -20
        choice:
            xoffset -30
        0.01
        repeat
    parallel:
        alpha 0.6
        linear 0.15 alpha 0.1
        0.2
        alpha 0.6
        linear 0.15 alpha 0.1
        0.2
        alpha 0.7
        linear 0.45 alpha 0

image glitch_color2:
    ytile 3
    zoom 2.5
    parallel:
        "assets/images/bg/glitch-red.png"
        0.1
        "assets/images/bg/glitch-green.png"
        0.1
        "assets/images/bg/glitch-blue.png"
        0.1
        repeat
    parallel:
        yoffset 720
        linear 0.5 yoffset 0
        repeat
    parallel:
        choice:
            xoffset 0
        choice:
            xoffset 10
        choice:
            xoffset 20
        choice:
            xoffset 35
        choice:
            xoffset -10
        choice:
            xoffset -20
        choice:
            xoffset -30
        0.01
        repeat
    parallel:
        alpha 0.7
        linear 0.45 alpha 0

#Definitions for Sayori's sprite.
image sayori 1 = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/a.png")
image sayori 1a = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/a.png")
image sayori 1b = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/b.png")
image sayori 1c = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/c.png")
image sayori 1d = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/d.png")
image sayori 1e = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/e.png")
image sayori 1f = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/f.png")
image sayori 1g = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/g.png")
image sayori 1h = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/h.png")
image sayori 1i = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/i.png")
image sayori 1j = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/j.png")
image sayori 1k = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/k.png")
image sayori 1l = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/l.png")
image sayori 1m = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/m.png")
image sayori 1n = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/n.png")
image sayori 1o = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/o.png")
image sayori 1p = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/p.png")
image sayori 1q = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/q.png")
image sayori 1r = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/r.png")
image sayori 1s = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/s.png")
image sayori 1t = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/t.png")
image sayori 1u = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/u.png")
image sayori 1v = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/v.png")
image sayori 1w = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/w.png")
image sayori 1x = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/x.png")
image sayori 1y = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/y.png")

image sayori 2 = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/a.png")
image sayori 2a = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/a.png")
image sayori 2b = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/b.png")
image sayori 2c = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/c.png")
image sayori 2d = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/d.png")
image sayori 2e = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/e.png")
image sayori 2f = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/f.png")
image sayori 2g = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/g.png")
image sayori 2h = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/h.png")
image sayori 2i = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/i.png")
image sayori 2j = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/j.png")
image sayori 2k = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/k.png")
image sayori 2l = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/l.png")
image sayori 2m = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/m.png")
image sayori 2n = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/n.png")
image sayori 2o = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/o.png")
image sayori 2p = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/p.png")
image sayori 2q = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/q.png")
image sayori 2r = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/r.png")
image sayori 2s = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/s.png")
image sayori 2t = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/t.png")
image sayori 2u = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/u.png")
image sayori 2v = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/v.png")
image sayori 2w = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/w.png")
image sayori 2x = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/x.png")
image sayori 2y = im.Composite((960, 960), (0, 0), "assets/images/sayori/1l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/y.png")

image sayori 3 = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/a.png")
image sayori 3a = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/a.png")
image sayori 3b = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/b.png")
image sayori 3c = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/c.png")
image sayori 3d = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/d.png")
image sayori 3e = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/e.png")
image sayori 3f = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/f.png")
image sayori 3g = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/g.png")
image sayori 3h = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/h.png")
image sayori 3i = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/i.png")
image sayori 3j = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/j.png")
image sayori 3k = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/k.png")
image sayori 3l = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/l.png")
image sayori 3m = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/m.png")
image sayori 3n = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/n.png")
image sayori 3o = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/o.png")
image sayori 3p = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/p.png")
image sayori 3q = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/q.png")
image sayori 3r = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/r.png")
image sayori 3s = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/s.png")
image sayori 3t = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/t.png")
image sayori 3u = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/u.png")
image sayori 3v = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/v.png")
image sayori 3w = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/w.png")
image sayori 3x = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/x.png")
image sayori 3y = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/1r.png", (0, 0), "assets/images/sayori/y.png")

image sayori 4 = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/a.png")
image sayori 4a = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/a.png")
image sayori 4b = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/b.png")
image sayori 4c = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/c.png")
image sayori 4d = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/d.png")
image sayori 4e = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/e.png")
image sayori 4f = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/f.png")
image sayori 4g = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/g.png")
image sayori 4h = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/h.png")
image sayori 4i = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/i.png")
image sayori 4j = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/j.png")
image sayori 4k = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/k.png")
image sayori 4l = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/l.png")
image sayori 4m = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/m.png")
image sayori 4n = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/n.png")
image sayori 4o = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/o.png")
image sayori 4p = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/p.png")
image sayori 4q = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/q.png")
image sayori 4r = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/r.png")
image sayori 4s = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/s.png")
image sayori 4t = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/t.png")
image sayori 4u = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/u.png")
image sayori 4v = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/v.png")
image sayori 4w = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/w.png")
image sayori 4x = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/x.png")
image sayori 4y = im.Composite((960, 960), (0, 0), "assets/images/sayori/2l.png", (0, 0), "assets/images/sayori/2r.png", (0, 0), "assets/images/sayori/y.png")

image sayori 5 = im.Composite((960, 960), (0, 0), "assets/images/sayori/3a.png")
image sayori 5a = im.Composite((960, 960), (0, 0), "assets/images/sayori/3a.png")
image sayori 5b = im.Composite((960, 960), (0, 0), "assets/images/sayori/3b.png")
image sayori 5c = im.Composite((960, 960), (0, 0), "assets/images/sayori/3c.png")
image sayori 5d = im.Composite((960, 960), (0, 0), "assets/images/sayori/3d.png")

image sayori 1ba = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/a.png")
image sayori 1bb = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/b.png")
image sayori 1bc = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/c.png")
image sayori 1bd = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/d.png")
image sayori 1be = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/e.png")
image sayori 1bf = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/f.png")
image sayori 1bg = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/g.png")
image sayori 1bh = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/h.png")
image sayori 1bi = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/i.png")
image sayori 1bj = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/j.png")
image sayori 1bk = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/k.png")
image sayori 1bl = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/l.png")
image sayori 1bm = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/m.png")
image sayori 1bn = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/n.png")
image sayori 1bo = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/o.png")
image sayori 1bp = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/p.png")
image sayori 1bq = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/q.png")
image sayori 1br = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/r.png")
image sayori 1bs = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/s.png")
image sayori 1bt = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/t.png")
image sayori 1bu = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/u.png")
image sayori 1bv = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/v.png")
image sayori 1bw = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/w.png")
image sayori 1bx = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/x.png")
image sayori 1by = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/y.png")

image sayori 2ba = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/a.png")
image sayori 2bb = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/b.png")
image sayori 2bc = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/c.png")
image sayori 2bd = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/d.png")
image sayori 2be = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/e.png")
image sayori 2bf = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/f.png")
image sayori 2bg = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/g.png")
image sayori 2bh = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/h.png")
image sayori 2bi = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/i.png")
image sayori 2bj = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/j.png")
image sayori 2bk = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/k.png")
image sayori 2bl = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/l.png")
image sayori 2bm = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/m.png")
image sayori 2bn = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/n.png")
image sayori 2bo = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/o.png")
image sayori 2bp = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/p.png")
image sayori 2bq = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/q.png")
image sayori 2br = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/r.png")
image sayori 2bs = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/s.png")
image sayori 2bt = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/t.png")
image sayori 2bu = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/u.png")
image sayori 2bv = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/v.png")
image sayori 2bw = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/w.png")
image sayori 2bx = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/x.png")
image sayori 2by = im.Composite((960, 960), (0, 0), "assets/images/sayori/1bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/y.png")

image sayori 3ba = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/a.png")
image sayori 3bb = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/b.png")
image sayori 3bc = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/c.png")
image sayori 3bd = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/d.png")
image sayori 3be = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/e.png")
image sayori 3bf = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/f.png")
image sayori 3bg = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/g.png")
image sayori 3bh = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/h.png")
image sayori 3bi = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/i.png")
image sayori 3bj = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/j.png")
image sayori 3bk = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/k.png")
image sayori 3bl = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/l.png")
image sayori 3bm = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/m.png")
image sayori 3bn = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/n.png")
image sayori 3bo = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/o.png")
image sayori 3bp = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/p.png")
image sayori 3bq = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/q.png")
image sayori 3br = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/r.png")
image sayori 3bs = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/s.png")
image sayori 3bt = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/t.png")
image sayori 3bu = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/u.png")
image sayori 3bv = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/v.png")
image sayori 3bw = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/w.png")
image sayori 3bx = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/x.png")
image sayori 3by = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/1br.png", (0, 0), "assets/images/sayori/y.png")

image sayori 4ba = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/a.png")
image sayori 4bb = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/b.png")
image sayori 4bc = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/c.png")
image sayori 4bd = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/d.png")
image sayori 4be = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/e.png")
image sayori 4bf = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/f.png")
image sayori 4bg = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/g.png")
image sayori 4bh = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/h.png")
image sayori 4bi = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/i.png")
image sayori 4bj = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/j.png")
image sayori 4bk = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/k.png")
image sayori 4bl = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/l.png")
image sayori 4bm = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/m.png")
image sayori 4bn = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/n.png")
image sayori 4bo = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/o.png")
image sayori 4bp = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/p.png")
image sayori 4bq = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/q.png")
image sayori 4br = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/r.png")
image sayori 4bs = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/s.png")
image sayori 4bt = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/t.png")
image sayori 4bu = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/u.png")
image sayori 4bv = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/v.png")
image sayori 4bw = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/w.png")
image sayori 4bx = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/x.png")
image sayori 4by = im.Composite((960, 960), (0, 0), "assets/images/sayori/2bl.png", (0, 0), "assets/images/sayori/2br.png", (0, 0), "assets/images/sayori/y.png")

image sayori glitch:
    "assets/images/sayori/glitch1.png"
    pause 0.01666
    "assets/images/sayori/glitch2.png"
    pause 0.01666
    repeat

#Definitions for Natsuki's sprite.
image natsuki 11 = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/1t.png")
image natsuki 1a = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/a.png")
image natsuki 1b = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/b.png")
image natsuki 1c = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/c.png")
image natsuki 1d = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/d.png")
image natsuki 1e = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/e.png")
image natsuki 1f = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/f.png")
image natsuki 1g = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/g.png")
image natsuki 1h = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/h.png")
image natsuki 1i = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/i.png")
image natsuki 1j = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/j.png")
image natsuki 1k = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/k.png")
image natsuki 1l = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/l.png")
image natsuki 1m = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/m.png")
image natsuki 1n = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/n.png")
image natsuki 1o = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/o.png")
image natsuki 1p = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/p.png")
image natsuki 1q = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/q.png")
image natsuki 1r = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/r.png")
image natsuki 1s = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/s.png")
image natsuki 1t = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/t.png")
image natsuki 1u = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/u.png")
image natsuki 1v = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/v.png")
image natsuki 1w = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/w.png")
image natsuki 1x = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/x.png")
image natsuki 1y = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/y.png")
image natsuki 1z = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/z.png")

image natsuki 21 = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/1t.png")
image natsuki 2a = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/a.png")
image natsuki 2b = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/b.png")
image natsuki 2c = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/c.png")
image natsuki 2d = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/d.png")
image natsuki 2e = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/e.png")
image natsuki 2f = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/f.png")
image natsuki 2g = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/g.png")
image natsuki 2h = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/h.png")
image natsuki 2i = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/i.png")
image natsuki 2j = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/j.png")
image natsuki 2k = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/k.png")
image natsuki 2l = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/l.png")
image natsuki 2m = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/m.png")
image natsuki 2n = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/n.png")
image natsuki 2o = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/o.png")
image natsuki 2p = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/p.png")
image natsuki 2q = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/q.png")
image natsuki 2r = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/r.png")
image natsuki 2s = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/s.png")
image natsuki 2t = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/t.png")
image natsuki 2u = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/u.png")
image natsuki 2v = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/v.png")
image natsuki 2w = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/w.png")
image natsuki 2x = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/x.png")
image natsuki 2y = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/y.png")
image natsuki 2z = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/z.png")

image natsuki 31 = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/1t.png")
image natsuki 3a = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/a.png")
image natsuki 3b = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/b.png")
image natsuki 3c = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/c.png")
image natsuki 3d = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/d.png")
image natsuki 3e = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/e.png")
image natsuki 3f = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/f.png")
image natsuki 3g = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/g.png")
image natsuki 3h = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/h.png")
image natsuki 3i = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/i.png")
image natsuki 3j = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/j.png")
image natsuki 3k = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/k.png")
image natsuki 3l = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/l.png")
image natsuki 3m = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/m.png")
image natsuki 3n = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/n.png")
image natsuki 3o = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/o.png")
image natsuki 3p = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/p.png")
image natsuki 3q = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/q.png")
image natsuki 3r = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/r.png")
image natsuki 3s = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/s.png")
image natsuki 3t = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/t.png")
image natsuki 3u = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/u.png")
image natsuki 3v = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/v.png")
image natsuki 3w = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/w.png")
image natsuki 3x = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/x.png")
image natsuki 3y = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/y.png")
image natsuki 3z = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/z.png")

image natsuki 41 = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/1t.png")
image natsuki 4a = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/a.png")
image natsuki 4b = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/b.png")
image natsuki 4c = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/c.png")
image natsuki 4d = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/d.png")
image natsuki 4e = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/e.png")
image natsuki 4f = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/f.png")
image natsuki 4g = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/g.png")
image natsuki 4h = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/h.png")
image natsuki 4i = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/i.png")
image natsuki 4j = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/j.png")
image natsuki 4k = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/k.png")
image natsuki 4l = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/l.png")
image natsuki 4m = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/m.png")
image natsuki 4n = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/n.png")
image natsuki 4o = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/o.png")
image natsuki 4p = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/p.png")
image natsuki 4q = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/q.png")
image natsuki 4r = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/r.png")
image natsuki 4s = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/s.png")
image natsuki 4t = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/t.png")
image natsuki 4u = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/u.png")
image natsuki 4v = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/v.png")
image natsuki 4w = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/w.png")
image natsuki 4x = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/x.png")
image natsuki 4y = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/y.png")
image natsuki 4z = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/z.png")

image natsuki 12 = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/2t.png")
image natsuki 12a = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/2ta.png")
image natsuki 12b = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/2tb.png")
image natsuki 12c = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/2tc.png")
image natsuki 12d = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/2td.png")
image natsuki 12e = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/2te.png")
image natsuki 12f = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/2tf.png")
image natsuki 12g = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/2tg.png")
image natsuki 12h = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/2th.png")
image natsuki 12i = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/2ti.png")

image natsuki 42 = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/2t.png")
image natsuki 42a = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/2ta.png")
image natsuki 42b = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/2tb.png")
image natsuki 42c = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/2tc.png")
image natsuki 42d = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/2td.png")
image natsuki 42e = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/2te.png")
image natsuki 42f = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/2tf.png")
image natsuki 42g = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/2tg.png")
image natsuki 42h = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/2th.png")
image natsuki 42i = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/2ti.png")

image natsuki 51 = im.Composite((960, 960), (18, 22), "assets/images/natsuki/1t.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5a = im.Composite((960, 960), (18, 22), "assets/images/natsuki/a.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5b = im.Composite((960, 960), (18, 22), "assets/images/natsuki/b.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5c = im.Composite((960, 960), (18, 22), "assets/images/natsuki/c.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5d = im.Composite((960, 960), (18, 22), "assets/images/natsuki/d.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5e = im.Composite((960, 960), (18, 22), "assets/images/natsuki/e.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5f = im.Composite((960, 960), (18, 22), "assets/images/natsuki/f.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5g = im.Composite((960, 960), (18, 22), "assets/images/natsuki/g.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5h = im.Composite((960, 960), (18, 22), "assets/images/natsuki/h.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5i = im.Composite((960, 960), (18, 22), "assets/images/natsuki/i.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5j = im.Composite((960, 960), (18, 22), "assets/images/natsuki/j.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5k = im.Composite((960, 960), (18, 22), "assets/images/natsuki/k.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5l = im.Composite((960, 960), (18, 22), "assets/images/natsuki/l.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5m = im.Composite((960, 960), (18, 22), "assets/images/natsuki/m.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5n = im.Composite((960, 960), (18, 22), "assets/images/natsuki/n.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5o = im.Composite((960, 960), (18, 22), "assets/images/natsuki/o.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5p = im.Composite((960, 960), (18, 22), "assets/images/natsuki/p.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5q = im.Composite((960, 960), (18, 22), "assets/images/natsuki/q.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5r = im.Composite((960, 960), (18, 22), "assets/images/natsuki/r.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5s = im.Composite((960, 960), (18, 22), "assets/images/natsuki/s.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5t = im.Composite((960, 960), (18, 22), "assets/images/natsuki/t.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5u = im.Composite((960, 960), (18, 22), "assets/images/natsuki/u.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5v = im.Composite((960, 960), (18, 22), "assets/images/natsuki/v.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5w = im.Composite((960, 960), (18, 22), "assets/images/natsuki/w.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5x = im.Composite((960, 960), (18, 22), "assets/images/natsuki/x.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5y = im.Composite((960, 960), (18, 22), "assets/images/natsuki/y.png", (0, 0), "assets/images/natsuki/3.png")
image natsuki 5z = im.Composite((960, 960), (18, 22), "assets/images/natsuki/z.png", (0, 0), "assets/images/natsuki/3.png")

image natsuki 1ba = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/a.png")
image natsuki 1bb = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/b.png")
image natsuki 1bc = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/c.png")
image natsuki 1bd = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/d.png")
image natsuki 1be = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/e.png")
image natsuki 1bf = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/f.png")
image natsuki 1bg = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/g.png")
image natsuki 1bh = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/h.png")
image natsuki 1bi = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/i.png")
image natsuki 1bj = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/j.png")
image natsuki 1bk = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/k.png")
image natsuki 1bl = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/l.png")
image natsuki 1bm = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/m.png")
image natsuki 1bn = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/n.png")
image natsuki 1bo = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/o.png")
image natsuki 1bp = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/p.png")
image natsuki 1bq = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/q.png")
image natsuki 1br = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/r.png")
image natsuki 1bs = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/s.png")
image natsuki 1bt = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/t.png")
image natsuki 1bu = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/u.png")
image natsuki 1bv = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/v.png")
image natsuki 1bw = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/w.png")
image natsuki 1bx = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/x.png")
image natsuki 1by = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/y.png")
image natsuki 1bz = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/z.png")

image natsuki 2ba = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/a.png")
image natsuki 2bb = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/b.png")
image natsuki 2bc = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/c.png")
image natsuki 2bd = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/d.png")
image natsuki 2be = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/e.png")
image natsuki 2bf = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/f.png")
image natsuki 2bg = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/g.png")
image natsuki 2bh = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/h.png")
image natsuki 2bi = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/i.png")
image natsuki 2bj = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/j.png")
image natsuki 2bk = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/k.png")
image natsuki 2bl = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/l.png")
image natsuki 2bm = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/m.png")
image natsuki 2bn = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/n.png")
image natsuki 2bo = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/o.png")
image natsuki 2bp = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/p.png")
image natsuki 2bq = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/q.png")
image natsuki 2br = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/r.png")
image natsuki 2bs = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/s.png")
image natsuki 2bt = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/t.png")
image natsuki 2bu = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/u.png")
image natsuki 2bv = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/v.png")
image natsuki 2bw = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/w.png")
image natsuki 2bx = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/x.png")
image natsuki 2by = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/y.png")
image natsuki 2bz = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/z.png")

image natsuki 3ba = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/a.png")
image natsuki 3bb = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/b.png")
image natsuki 3bc = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/c.png")
image natsuki 3bd = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/d.png")
image natsuki 3be = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/e.png")
image natsuki 3bf = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/f.png")
image natsuki 3bg = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/g.png")
image natsuki 3bh = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/h.png")
image natsuki 3bi = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/i.png")
image natsuki 3bj = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/j.png")
image natsuki 3bk = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/k.png")
image natsuki 3bl = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/l.png")
image natsuki 3bm = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/m.png")
image natsuki 3bn = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/n.png")
image natsuki 3bo = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/o.png")
image natsuki 3bp = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/p.png")
image natsuki 3bq = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/q.png")
image natsuki 3br = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/r.png")
image natsuki 3bs = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/s.png")
image natsuki 3bt = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/t.png")
image natsuki 3bu = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/u.png")
image natsuki 3bv = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/v.png")
image natsuki 3bw = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/w.png")
image natsuki 3bx = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/x.png")
image natsuki 3by = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/y.png")
image natsuki 3bz = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/z.png")

image natsuki 4ba = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/a.png")
image natsuki 4bb = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/b.png")
image natsuki 4bc = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/c.png")
image natsuki 4bd = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/d.png")
image natsuki 4be = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/e.png")
image natsuki 4bf = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/f.png")
image natsuki 4bg = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/g.png")
image natsuki 4bh = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/h.png")
image natsuki 4bi = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/i.png")
image natsuki 4bj = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/j.png")
image natsuki 4bk = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/k.png")
image natsuki 4bl = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/l.png")
image natsuki 4bm = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/m.png")
image natsuki 4bn = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/n.png")
image natsuki 4bo = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/o.png")
image natsuki 4bp = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/p.png")
image natsuki 4bq = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/q.png")
image natsuki 4br = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/r.png")
image natsuki 4bs = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/s.png")
image natsuki 4bt = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/t.png")
image natsuki 4bu = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/u.png")
image natsuki 4bv = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/v.png")
image natsuki 4bw = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/w.png")
image natsuki 4bx = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/x.png")
image natsuki 4by = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/y.png")
image natsuki 4bz = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/z.png")

image natsuki 12ba = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/2bta.png")
image natsuki 12bb = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/2btb.png")
image natsuki 12bc = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/2btc.png")
image natsuki 12bd = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/2btd.png")
image natsuki 12be = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/2bte.png")
image natsuki 12bf = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/2btf.png")
image natsuki 12bg = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/2btg.png")
image natsuki 12bh = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/2bth.png")
image natsuki 12bi = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1bl.png", (0, 0), "assets/images/natsuki/1br.png", (0, 0), "assets/images/natsuki/2bti.png")

image natsuki 42ba = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/2bta.png")
image natsuki 42bb = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/2btb.png")
image natsuki 42bc = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/2btc.png")
image natsuki 42bd = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/2btd.png")
image natsuki 42be = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/2bte.png")
image natsuki 42bf = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/2btf.png")
image natsuki 42bg = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/2btg.png")
image natsuki 42bh = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/2bth.png")
image natsuki 42bi = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2bl.png", (0, 0), "assets/images/natsuki/2br.png", (0, 0), "assets/images/natsuki/2bti.png")

image natsuki 5ba = im.Composite((960, 960), (18, 22), "assets/images/natsuki/a.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bb = im.Composite((960, 960), (18, 22), "assets/images/natsuki/b.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bc = im.Composite((960, 960), (18, 22), "assets/images/natsuki/c.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bd = im.Composite((960, 960), (18, 22), "assets/images/natsuki/d.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5be = im.Composite((960, 960), (18, 22), "assets/images/natsuki/e.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bf = im.Composite((960, 960), (18, 22), "assets/images/natsuki/f.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bg = im.Composite((960, 960), (18, 22), "assets/images/natsuki/g.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bh = im.Composite((960, 960), (18, 22), "assets/images/natsuki/h.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bi = im.Composite((960, 960), (18, 22), "assets/images/natsuki/i.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bj = im.Composite((960, 960), (18, 22), "assets/images/natsuki/j.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bk = im.Composite((960, 960), (18, 22), "assets/images/natsuki/k.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bl = im.Composite((960, 960), (18, 22), "assets/images/natsuki/l.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bm = im.Composite((960, 960), (18, 22), "assets/images/natsuki/m.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bn = im.Composite((960, 960), (18, 22), "assets/images/natsuki/n.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bo = im.Composite((960, 960), (18, 22), "assets/images/natsuki/o.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bp = im.Composite((960, 960), (18, 22), "assets/images/natsuki/p.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bq = im.Composite((960, 960), (18, 22), "assets/images/natsuki/q.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5br = im.Composite((960, 960), (18, 22), "assets/images/natsuki/r.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bs = im.Composite((960, 960), (18, 22), "assets/images/natsuki/s.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bt = im.Composite((960, 960), (18, 22), "assets/images/natsuki/t.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bu = im.Composite((960, 960), (18, 22), "assets/images/natsuki/u.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bv = im.Composite((960, 960), (18, 22), "assets/images/natsuki/v.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bw = im.Composite((960, 960), (18, 22), "assets/images/natsuki/w.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bx = im.Composite((960, 960), (18, 22), "assets/images/natsuki/x.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5by = im.Composite((960, 960), (18, 22), "assets/images/natsuki/y.png", (0, 0), "assets/images/natsuki/3b.png")
image natsuki 5bz = im.Composite((960, 960), (18, 22), "assets/images/natsuki/z.png", (0, 0), "assets/images/natsuki/3b.png")

image natsuki 1 = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/1t.png")
image natsuki 2 = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/1t.png")
image natsuki 3 = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/1t.png")
image natsuki 4 = im.Composite((960, 960), (0, 0), "assets/images/natsuki/2l.png", (0, 0), "assets/images/natsuki/2r.png", (0, 0), "assets/images/natsuki/1t.png")
image natsuki 5 = im.Composite((960, 960), (18, 22), "assets/images/natsuki/1t.png", (0, 0), "assets/images/natsuki/3.png")

image natsuki ghost_base:
    "assets/images/natsuki/ghost1.png"

image natsuki ghost1:
    "natsuki 11"
    "natsuki ghost_base" with Dissolve(20.0, alpha=True)

image natsuki ghost2 = Image("assets/images/natsuki/ghost2.png")
image natsuki ghost3 = Image("assets/images/natsuki/ghost3.png")

image natsuki ghost4:
    "natsuki ghost3"
    parallel:
        easeout 0.25 zoom 4.5 yoffset 1200
    parallel:
        ease 0.025 xoffset -20
        ease 0.025 xoffset 20
        repeat
    0.25
    "black"

image natsuki glitch1:
    "assets/images/natsuki/glitch1.png"
    zoom 1.25
    block:
        yoffset 300 xoffset 100 ytile 2
        linear 0.15 yoffset 200
        repeat
    time 0.75
    yoffset 0 zoom 1 xoffset 0 ytile 1
    "natsuki 4e"

image natsuki scream = im.Composite((960, 960), (0, 0), "assets/images/natsuki/1l.png", (0, 0), "assets/images/natsuki/1r.png", (0, 0), "assets/images/natsuki/scream.png")
image natsuki vomit = "assets/images/natsuki/vomit.png"

#Definitions for Yuri's sprite.
image yuri 1 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/a.png")
image yuri 2 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/a.png")
image yuri 3 = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/a.png")
image yuri 4 = im.Composite((960, 960), (0, 0), "assets/images/yuri/3.png", (0, 0), "assets/images/yuri/a2.png")

image yuri 1a = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/a.png")
image yuri 1b = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/b.png")
image yuri 1c = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/c.png")
image yuri 1d = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/d.png")
image yuri 1e = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/e.png")
image yuri 1f = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/f.png")
image yuri 1g = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/g.png")
image yuri 1h = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/h.png")
image yuri 1i = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/i.png")
image yuri 1j = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/j.png")
image yuri 1k = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/k.png")
image yuri 1l = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/l.png")
image yuri 1m = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/m.png")
image yuri 1n = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/n.png")
image yuri 1o = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/o.png")
image yuri 1p = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/p.png")
image yuri 1q = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/q.png")
image yuri 1r = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/r.png")
image yuri 1s = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/s.png")
image yuri 1t = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/t.png")
image yuri 1u = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/u.png")
image yuri 1v = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/v.png")
image yuri 1w = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/w.png")

image yuri 1y1 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/y1.png")
image yuri 1y2 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/y2.png")
image yuri 1y3 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/y3.png")
image yuri 1y4 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/y4.png")
image yuri 1y5 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/y5.png")
image yuri 1y6 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/y6.png")
image yuri 1y7 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/y7.png")

image yuri 2a = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/a.png")
image yuri 2b = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/b.png")
image yuri 2c = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/c.png")
image yuri 2d = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/d.png")
image yuri 2e = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/e.png")
image yuri 2f = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/f.png")
image yuri 2g = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/g.png")
image yuri 2h = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/h.png")
image yuri 2i = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/i.png")
image yuri 2j = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/j.png")
image yuri 2k = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/k.png")
image yuri 2l = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/l.png")
image yuri 2m = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/m.png")
image yuri 2n = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/n.png")
image yuri 2o = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/o.png")
image yuri 2p = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/p.png")
image yuri 2q = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/q.png")
image yuri 2r = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/r.png")
image yuri 2s = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/s.png")
image yuri 2t = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/t.png")
image yuri 2u = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/u.png")
image yuri 2v = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/v.png")
image yuri 2w = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/w.png")

image yuri 2y1 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y1.png")
image yuri 2y2 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y2.png")
image yuri 2y3 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y3.png")
image yuri 2y4 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y4.png")
image yuri 2y5 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y5.png")
image yuri 2y6 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y6.png")
image yuri 2y7 = im.Composite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y7.png")

image yuri 3a = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/a.png")
image yuri 3b = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/b.png")
image yuri 3c = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/c.png")
image yuri 3d = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/d.png")
image yuri 3e = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/e.png")
image yuri 3f = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/f.png")
image yuri 3g = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/g.png")
image yuri 3h = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/h.png")
image yuri 3i = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/i.png")
image yuri 3j = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/j.png")
image yuri 3k = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/k.png")
image yuri 3l = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/l.png")
image yuri 3m = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/m.png")
image yuri 3n = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/n.png")
image yuri 3o = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/o.png")
image yuri 3p = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/p.png")
image yuri 3q = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/q.png")
image yuri 3r = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/r.png")
image yuri 3s = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/s.png")
image yuri 3t = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/t.png")
image yuri 3u = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/u.png")
image yuri 3v = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/v.png")
image yuri 3w = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/w.png")

image yuri 3y1 = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y1.png")
image yuri 3y2 = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y2.png")
image yuri 3y3 = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y3.png")
image yuri 3y4 = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y4.png")
image yuri 3y5 = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y5.png")
image yuri 3y6 = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y6.png")
image yuri 3y7 = im.Composite((960, 960), (0, 0), "assets/images/yuri/2l.png", (0, 0), "assets/images/yuri/2r.png", (0, 0), "assets/images/yuri/y7.png")

image yuri 4a = im.Composite((960, 960), (0, 0), "assets/images/yuri/3.png", (0, 0), "assets/images/yuri/a2.png")
image yuri 4b = im.Composite((960, 960), (0, 0), "assets/images/yuri/3.png", (0, 0), "assets/images/yuri/b2.png")
image yuri 4c = im.Composite((960, 960), (0, 0), "assets/images/yuri/3.png", (0, 0), "assets/images/yuri/c2.png")
image yuri 4d = im.Composite((960, 960), (0, 0), "assets/images/yuri/3.png", (0, 0), "assets/images/yuri/d2.png")
image yuri 4e = im.Composite((960, 960), (0, 0), "assets/images/yuri/3.png", (0, 0), "assets/images/yuri/e2.png")

image yuri 1ba = im.Composite((960, 960), (0, 0), "assets/images/yuri/a.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bb = im.Composite((960, 960), (0, 0), "assets/images/yuri/b.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bc = im.Composite((960, 960), (0, 0), "assets/images/yuri/c.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bd = im.Composite((960, 960), (0, 0), "assets/images/yuri/d.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1be = im.Composite((960, 960), (0, 0), "assets/images/yuri/e.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bf = im.Composite((960, 960), (0, 0), "assets/images/yuri/f.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bg = im.Composite((960, 960), (0, 0), "assets/images/yuri/g.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bh = im.Composite((960, 960), (0, 0), "assets/images/yuri/h.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bi = im.Composite((960, 960), (0, 0), "assets/images/yuri/i.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bj = im.Composite((960, 960), (0, 0), "assets/images/yuri/j.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bk = im.Composite((960, 960), (0, 0), "assets/images/yuri/k.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bl = im.Composite((960, 960), (0, 0), "assets/images/yuri/l.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bm = im.Composite((960, 960), (0, 0), "assets/images/yuri/m.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bn = im.Composite((960, 960), (0, 0), "assets/images/yuri/n.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bo = im.Composite((960, 960), (0, 0), "assets/images/yuri/o.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bp = im.Composite((960, 960), (0, 0), "assets/images/yuri/p.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bq = im.Composite((960, 960), (0, 0), "assets/images/yuri/q.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1br = im.Composite((960, 960), (0, 0), "assets/images/yuri/r.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bs = im.Composite((960, 960), (0, 0), "assets/images/yuri/s.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bt = im.Composite((960, 960), (0, 0), "assets/images/yuri/t.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bu = im.Composite((960, 960), (0, 0), "assets/images/yuri/u.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bv = im.Composite((960, 960), (0, 0), "assets/images/yuri/v.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")
image yuri 1bw = im.Composite((960, 960), (0, 0), "assets/images/yuri/w.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/1br.png")

image yuri 2ba = im.Composite((960, 960), (0, 0), "assets/images/yuri/a.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bb = im.Composite((960, 960), (0, 0), "assets/images/yuri/b.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bc = im.Composite((960, 960), (0, 0), "assets/images/yuri/c.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bd = im.Composite((960, 960), (0, 0), "assets/images/yuri/d.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2be = im.Composite((960, 960), (0, 0), "assets/images/yuri/e.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bf = im.Composite((960, 960), (0, 0), "assets/images/yuri/f.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bg = im.Composite((960, 960), (0, 0), "assets/images/yuri/g.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bh = im.Composite((960, 960), (0, 0), "assets/images/yuri/h.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bi = im.Composite((960, 960), (0, 0), "assets/images/yuri/i.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bj = im.Composite((960, 960), (0, 0), "assets/images/yuri/j.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bk = im.Composite((960, 960), (0, 0), "assets/images/yuri/k.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bl = im.Composite((960, 960), (0, 0), "assets/images/yuri/l.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bm = im.Composite((960, 960), (0, 0), "assets/images/yuri/m.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bn = im.Composite((960, 960), (0, 0), "assets/images/yuri/n.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bo = im.Composite((960, 960), (0, 0), "assets/images/yuri/o.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bp = im.Composite((960, 960), (0, 0), "assets/images/yuri/p.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bq = im.Composite((960, 960), (0, 0), "assets/images/yuri/q.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2br = im.Composite((960, 960), (0, 0), "assets/images/yuri/r.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bs = im.Composite((960, 960), (0, 0), "assets/images/yuri/s.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bt = im.Composite((960, 960), (0, 0), "assets/images/yuri/t.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bu = im.Composite((960, 960), (0, 0), "assets/images/yuri/u.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bv = im.Composite((960, 960), (0, 0), "assets/images/yuri/v.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 2bw = im.Composite((960, 960), (0, 0), "assets/images/yuri/w.png", (0, 0), "assets/images/yuri/1bl.png", (0, 0), "assets/images/yuri/2br.png")

image yuri 3ba = im.Composite((960, 960), (0, 0), "assets/images/yuri/a.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bb = im.Composite((960, 960), (0, 0), "assets/images/yuri/b.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bc = im.Composite((960, 960), (0, 0), "assets/images/yuri/c.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bd = im.Composite((960, 960), (0, 0), "assets/images/yuri/d.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3be = im.Composite((960, 960), (0, 0), "assets/images/yuri/e.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bf = im.Composite((960, 960), (0, 0), "assets/images/yuri/f.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bg = im.Composite((960, 960), (0, 0), "assets/images/yuri/g.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bh = im.Composite((960, 960), (0, 0), "assets/images/yuri/h.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bi = im.Composite((960, 960), (0, 0), "assets/images/yuri/i.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bj = im.Composite((960, 960), (0, 0), "assets/images/yuri/j.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bk = im.Composite((960, 960), (0, 0), "assets/images/yuri/k.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bl = im.Composite((960, 960), (0, 0), "assets/images/yuri/l.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bm = im.Composite((960, 960), (0, 0), "assets/images/yuri/m.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bn = im.Composite((960, 960), (0, 0), "assets/images/yuri/n.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bo = im.Composite((960, 960), (0, 0), "assets/images/yuri/o.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bp = im.Composite((960, 960), (0, 0), "assets/images/yuri/p.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bq = im.Composite((960, 960), (0, 0), "assets/images/yuri/q.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3br = im.Composite((960, 960), (0, 0), "assets/images/yuri/r.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bs = im.Composite((960, 960), (0, 0), "assets/images/yuri/s.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bt = im.Composite((960, 960), (0, 0), "assets/images/yuri/t.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bu = im.Composite((960, 960), (0, 0), "assets/images/yuri/u.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bv = im.Composite((960, 960), (0, 0), "assets/images/yuri/v.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")
image yuri 3bw = im.Composite((960, 960), (0, 0), "assets/images/yuri/w.png", (0, 0), "assets/images/yuri/2bl.png", (0, 0), "assets/images/yuri/2br.png")

image yuri 4ba = im.Composite((960, 960), (0, 0), "assets/images/yuri/a2.png", (0, 0), "assets/images/yuri/3b.png")
image yuri 4bb = im.Composite((960, 960), (0, 0), "assets/images/yuri/b2.png", (0, 0), "assets/images/yuri/3b.png")
image yuri 4bc = im.Composite((960, 960), (0, 0), "assets/images/yuri/c2.png", (0, 0), "assets/images/yuri/3b.png")
image yuri 4bd = im.Composite((960, 960), (0, 0), "assets/images/yuri/d2.png", (0, 0), "assets/images/yuri/3b.png")
image yuri 4be = im.Composite((960, 960), (0, 0), "assets/images/yuri/e2.png", (0, 0), "assets/images/yuri/3b.png")

image yuri stab_1 = "assets/images/yuri/stab/1.png"
image yuri stab_2 = "assets/images/yuri/stab/2.png"
image yuri stab_3 = "assets/images/yuri/stab/3.png"
image yuri stab_4 = "assets/images/yuri/stab/4.png"
image yuri stab_5 = "assets/images/yuri/stab/5.png"
image yuri stab_6 = LiveComposite((960,960), (0, 0), "assets/images/yuri/stab/6-mask.png", (0, 0), "yuri stab_6_eyes", (0, 0), "assets/images/yuri/stab/6.png")

image yuri stab_6_eyes:
    "assets/images/yuri/stab/6-eyes.png"
    subpixel True
    parallel:
        choice:
            xoffset 0.5
        choice:
            xoffset 0
        choice:
            xoffset -0.5
        0.2
        repeat
    parallel:
        choice:
            yoffset 0.5
        choice:
            yoffset 0
        choice:
            yoffset -0.5
        0.2
        repeat
    parallel:
        2.05
        easeout 1.0 yoffset -15
        linear 10 yoffset -15

image yuri oneeye = LiveComposite((960, 960), (0, 0), "assets/images/yuri/1l.png", (0, 0), "assets/images/yuri/1r.png", (0, 0), "assets/images/yuri/oneeye.png", (0, 0), "yuri oneeye2")

image yuri oneeye2:
    "assets/images/yuri/oneeye2.png"
    subpixel True
    pause 5.0
    linear 60 xoffset -50 yoffset 20

image yuri glitch:
    "assets/images/yuri/glitch1.png"
    pause 0.1
    "assets/images/yuri/glitch2.png"
    pause 0.1
    "assets/images/yuri/glitch3.png"
    pause 0.1
    "assets/images/yuri/glitch4.png"
    pause 0.1
    "assets/images/yuri/glitch5.png"
    pause 0.1
    repeat

image yuri glitch2:
    "assets/images/yuri/0a.png"
    pause 0.1
    "assets/images/yuri/0b.png"
    pause 0.5
    "assets/images/yuri/0a.png"
    pause 0.3
    "assets/images/yuri/0b.png"
    pause 0.3
    "yuri 1"

image yuri eyes = LiveComposite((1280, 720), (0, 0), "assets/images/yuri/eyes1.png", (0, 0), "yuripupils")

image yuri eyes_base = "assets/images/yuri/eyes1.png"

image yuripupils:
    "assets/images/yuri/eyes2.png"
    yuripupils_move

image yuri cuts = "assets/images/yuri/cuts.png"

image yuri dragon:
    "yuri 3"
    0.25
    parallel:
        "assets/images/yuri/dragon1.png"
        0.01
        "assets/images/yuri/dragon2.png"
        0.01
        repeat
    parallel:
        0.01
        choice:
            xoffset -1
            xoffset -2
            xoffset -5
            xoffset -6
            xoffset -9
            xoffset -10
        0.01
        xoffset 0
        repeat
    time 0.55
    xoffset 0
    "yuri 3"

#### Definitions for Monika's sprite.
image monika 1 = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/a.png")
image monika 2 = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/a.png")
image monika 3 = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/a.png")
image monika 4 = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/a.png")
image monika 5 = im.Composite((960, 960), (0, 0), "assets/images/monika/3a.png")

image monika 1a = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/a.png")
image monika 1b = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/b.png")
image monika 1c = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/c.png")
image monika 1d = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/d.png")
image monika 1e = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/e.png")
image monika 1f = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/f.png")
image monika 1g = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/g.png")
image monika 1h = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/h.png")
image monika 1i = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/i.png")
image monika 1j = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/j.png")
image monika 1k = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/k.png")
image monika 1l = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/l.png")
image monika 1m = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/m.png")
image monika 1n = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/n.png")
image monika 1o = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/o.png")
image monika 1p = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/p.png")
image monika 1q = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/q.png")
image monika 1r = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/r.png")

image monika 2a = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/a.png")
image monika 2b = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/b.png")
image monika 2c = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/c.png")
image monika 2d = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/d.png")
image monika 2e = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/e.png")
image monika 2f = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/f.png")
image monika 2g = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/g.png")
image monika 2h = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/h.png")
image monika 2i = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/i.png")
image monika 2j = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/j.png")
image monika 2k = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/k.png")
image monika 2l = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/l.png")
image monika 2m = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/m.png")
image monika 2n = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/n.png")
image monika 2o = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/o.png")
image monika 2p = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/p.png")
image monika 2q = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/q.png")
image monika 2r = im.Composite((960, 960), (0, 0), "assets/images/monika/1l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/r.png")

image monika 3a = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/a.png")
image monika 3b = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/b.png")
image monika 3c = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/c.png")
image monika 3d = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/d.png")
image monika 3e = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/e.png")
image monika 3f = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/f.png")
image monika 3g = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/g.png")
image monika 3h = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/h.png")
image monika 3i = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/i.png")
image monika 3j = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/j.png")
image monika 3k = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/k.png")
image monika 3l = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/l.png")
image monika 3m = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/m.png")
image monika 3n = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/n.png")
image monika 3o = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/o.png")
image monika 3p = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/p.png")
image monika 3q = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/q.png")
image monika 3r = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/1r.png", (0, 0), "assets/images/monika/r.png")

image monika 4a = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/a.png")
image monika 4b = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/b.png")
image monika 4c = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/c.png")
image monika 4d = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/d.png")
image monika 4e = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/e.png")
image monika 4f = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/f.png")
image monika 4g = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/g.png")
image monika 4h = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/h.png")
image monika 4i = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/i.png")
image monika 4j = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/j.png")
image monika 4k = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/k.png")
image monika 4l = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/l.png")
image monika 4m = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/m.png")
image monika 4n = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/n.png")
image monika 4o = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/o.png")
image monika 4p = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/p.png")
image monika 4q = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/q.png")
image monika 4r = im.Composite((960, 960), (0, 0), "assets/images/monika/2l.png", (0, 0), "assets/images/monika/2r.png", (0, 0), "assets/images/monika/r.png")

image monika 5a = im.Composite((960, 960), (0, 0), "assets/images/monika/3a.png")
image monika 5b = im.Composite((960, 960), (0, 0), "assets/images/monika/3b.png")

image monika g1:
    "assets/images/monika/g1.png"
    xoffset 35 yoffset 55
    parallel:
        zoom 1.00
        linear 0.10 zoom 1.03
        repeat
    parallel:
        xoffset 35
        0.20
        xoffset 0
        0.05
        xoffset -10
        0.05
        xoffset 0
        0.05
        xoffset -80
        0.05
        repeat
    time 1.25
    xoffset 0 yoffset 0 zoom 1.00
    "monika 3"

image monika g2:
    block:
        choice:
            "assets/images/monika/g2.png"
        choice:
            "assets/images/monika/g3.png"
        choice:
            "assets/images/monika/g4.png"
    block:
        choice:
            pause 0.05
        choice:
            pause 0.1
        choice:
            pause 0.15
        choice:
            pause 0.2
    repeat

#### Definitions of Character and Narrations (the current speaker in the name textbox)
define narrator = Character(ctc="ctc", ctc_position="fixed")
define mc = DynamicCharacter('player', image='mc', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define s = DynamicCharacter('s_name', image='sayori', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define m = DynamicCharacter('m_name', image='monika', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define n = DynamicCharacter('n_name', image='natsuki', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define y = DynamicCharacter('y_name', image='yuri', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")
define ny = Character('Nat & Yuri', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")

#### Defaults, Defines, and Persistents pertaining to the checks found inside of DDLC. ####
default persistent.anticheat = 0
default persistent.first_poem = None
default anticheat = 0
define config.mouse = None
default chapter = 0
default s_name = "Sayori"
default m_name = "Monika"
default n_name = "Natsuki"
default y_name = "Yuri"
