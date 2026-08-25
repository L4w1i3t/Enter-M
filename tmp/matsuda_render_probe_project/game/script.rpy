transform matsuda_sprite_size:
    fit "contain"
    xysize (640, 960)

layeredimage matsuda:
    at matsuda_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "images/matsuda/neutral.png"
        attribute uniform:
            "images/matsuda/neut_uniform.png"

    group face:
        attribute neut default if_all "casual":
            "images/matsuda/face_neut_casual.png"
        attribute neut if_all "uniform":
            "images/matsuda/face_neut_uniform.png"
        attribute happy if_all "casual":
            "images/matsuda/face_happy_casual.png"
        attribute happy if_all "uniform":
            "images/matsuda/face_happy_uniform.png"
        attribute smug if_all "casual":
            "images/matsuda/face_smug_casual.png"
        attribute smug if_all "uniform":
            "images/matsuda/face_smug_uniform.png"
        attribute teasing if_all "casual":
            "images/matsuda/face_teasing_casual.png"
        attribute teasing if_all "uniform":
            "images/matsuda/face_teasing_uniform.png"
        attribute thinking if_all "casual":
            "images/matsuda/face_thinking_casual.png"
        attribute thinking if_all "uniform":
            "images/matsuda/face_thinking_uniform.png"
        attribute curious if_all "casual":
            "images/matsuda/face_curious_casual.png"
        attribute curious if_all "uniform":
            "images/matsuda/face_curious_uniform.png"
        attribute unamused if_all "casual":
            "images/matsuda/face_unamused_casual.png"
        attribute unamused if_all "uniform":
            "images/matsuda/face_unamused_uniform.png"
        attribute annoyed if_all "casual":
            "images/matsuda/face_annoyed_casual.png"
        attribute annoyed if_all "uniform":
            "images/matsuda/face_annoyed_uniform.png"
        attribute frustrated if_all "casual":
            "images/matsuda/face_frustrated_casual.png"
        attribute frustrated if_all "uniform":
            "images/matsuda/face_frustrated_uniform.png"
        attribute angry if_all "casual":
            "images/matsuda/face_angry_casual.png"
        attribute angry if_all "uniform":
            "images/matsuda/face_angry_uniform.png"
        attribute sad if_all "casual":
            "images/matsuda/face_sad_casual.png"
        attribute sad if_all "uniform":
            "images/matsuda/face_sad_uniform.png"
        attribute crying if_all "casual":
            "images/matsuda/face_crying_casual.png"
        attribute crying if_all "uniform":
            "images/matsuda/face_crying_uniform.png"
        attribute embarrassed if_all "casual":
            "images/matsuda/face_embarrassed_casual.png"
        attribute embarrassed if_all "uniform":
            "images/matsuda/face_embarrassed_uniform.png"
        attribute nervous if_all "casual":
            "images/matsuda/face_nervous_casual.png"
        attribute nervous if_all "uniform":
            "images/matsuda/face_nervous_uniform.png"
        attribute worried if_all "casual":
            "images/matsuda/face_worried_casual.png"
        attribute worried if_all "uniform":
            "images/matsuda/face_worried_uniform.png"
        attribute shocked if_all "casual":
            "images/matsuda/face_shocked_casual.png"
        attribute shocked if_all "uniform":
            "images/matsuda/face_shocked_uniform.png"
        attribute afraid if_all "casual":
            "images/matsuda/face_afraid_casual.png"
        attribute afraid if_all "uniform":
            "images/matsuda/face_afraid_uniform.png"
        attribute panicked if_all "casual":
            "images/matsuda/face_panicked_casual.png"
        attribute panicked if_all "uniform":
            "images/matsuda/face_panicked_uniform.png"
        attribute determined if_all "casual":
            "images/matsuda/face_determined_casual.png"
        attribute determined if_all "uniform":
            "images/matsuda/face_determined_uniform.png"
        attribute empty if_all "casual":
            "images/matsuda/face_empty_casual.png"
        attribute empty if_all "uniform":
            "images/matsuda/face_empty_uniform.png"
        attribute disgusted if_all "casual":
            "images/matsuda/face_disgusted_casual.png"
        attribute disgusted if_all "uniform":
            "images/matsuda/face_disgusted_uniform.png"

image matsuda uniform pose_facepalm = Transform("images/matsuda/pose_facepalm_uniform.png", fit="contain", xysize=(640, 960))
image matsuda uniform pose_chuuni = Transform("images/matsuda/pose_chuuni_uniform.png", fit="contain", xysize=(640, 960))
image matsuda uniform pose_shrug = Transform("images/matsuda/pose_shrug_uniform.png", fit="contain", xysize=(640, 960))
image matsuda casual pose_laughing = Transform("images/matsuda/pose_laughing_casual.png", fit="contain", xysize=(640, 960))
image matsuda uniform pose_laughing = Transform("images/matsuda/pose_laughing_uniform.png", fit="contain", xysize=(640, 960))


image probe_background_light = Solid("#ece9e2")
image probe_background_dark = Solid("#202229")
image probe_background_checker = Tile("images/probe_checker.png")

transform probe_center:
    xalign 0.5
    yalign 1.0


label start:
    python:
        import os
        _matsuda_probe_dir = os.environ["MATSUDA_PROBE_DIR"].replace("\\", "/")

    scene probe_background_light

    show matsuda casual neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/light/expressions/01_casual_neut.png")

    show matsuda casual smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/light/expressions/03_casual_smug.png")

    show matsuda casual thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/light/expressions/05_casual_thinking.png")

    show matsuda uniform neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/light/expressions/22_uniform_neut.png")

    show matsuda uniform smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/light/expressions/24_uniform_smug.png")

    show matsuda uniform thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/light/expressions/26_uniform_thinking.png")

    scene probe_background_dark

    show matsuda casual neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/dark/expressions/01_casual_neut.png")

    show matsuda casual smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/dark/expressions/03_casual_smug.png")

    show matsuda casual thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/dark/expressions/05_casual_thinking.png")

    show matsuda uniform neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/dark/expressions/22_uniform_neut.png")

    show matsuda uniform smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/dark/expressions/24_uniform_smug.png")

    show matsuda uniform thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/dark/expressions/26_uniform_thinking.png")

    scene probe_background_checker

    show matsuda casual neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/checker/expressions/01_casual_neut.png")

    show matsuda casual smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/checker/expressions/03_casual_smug.png")

    show matsuda casual thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/checker/expressions/05_casual_thinking.png")

    show matsuda uniform neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/checker/expressions/22_uniform_neut.png")

    show matsuda uniform smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/checker/expressions/24_uniform_smug.png")

    show matsuda uniform thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_matsuda_probe_dir + "/checker/expressions/26_uniform_thinking.png")

    $ renpy.quit()
    return
