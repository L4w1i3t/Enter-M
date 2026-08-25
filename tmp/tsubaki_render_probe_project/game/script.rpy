transform tsubaki_sprite_size:
    fit "contain"
    xysize (640, 960)

layeredimage tsubaki:
    at tsubaki_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "images/tsubaki/neutral.png"
        attribute uniform:
            "images/tsubaki/neut_uniform.png"

    group face:
        attribute neut default if_all "casual":
            "images/tsubaki/face_neut_casual.png"
        attribute neut if_all "uniform":
            "images/tsubaki/face_neut_uniform.png"
        attribute happy if_all "casual":
            "images/tsubaki/face_happy_casual.png"
        attribute happy if_all "uniform":
            "images/tsubaki/face_happy_uniform.png"
        attribute smug if_all "casual":
            "images/tsubaki/face_smug_casual.png"
        attribute smug if_all "uniform":
            "images/tsubaki/face_smug_uniform.png"
        attribute teasing if_all "casual":
            "images/tsubaki/face_teasing_casual.png"
        attribute teasing if_all "uniform":
            "images/tsubaki/face_teasing_uniform.png"
        attribute thinking if_all "casual":
            "images/tsubaki/face_thinking_casual.png"
        attribute thinking if_all "uniform":
            "images/tsubaki/face_thinking_uniform.png"
        attribute curious if_all "casual":
            "images/tsubaki/face_curious_casual.png"
        attribute curious if_all "uniform":
            "images/tsubaki/face_curious_uniform.png"
        attribute unamused if_all "casual":
            "images/tsubaki/face_unamused_casual.png"
        attribute unamused if_all "uniform":
            "images/tsubaki/face_unamused_uniform.png"
        attribute annoyed if_all "casual":
            "images/tsubaki/face_annoyed_casual.png"
        attribute annoyed if_all "uniform":
            "images/tsubaki/face_annoyed_uniform.png"
        attribute frustrated if_all "casual":
            "images/tsubaki/face_frustrated_casual.png"
        attribute frustrated if_all "uniform":
            "images/tsubaki/face_frustrated_uniform.png"
        attribute angry if_all "casual":
            "images/tsubaki/face_angry_casual.png"
        attribute angry if_all "uniform":
            "images/tsubaki/face_angry_uniform.png"
        attribute sad if_all "casual":
            "images/tsubaki/face_sad_casual.png"
        attribute sad if_all "uniform":
            "images/tsubaki/face_sad_uniform.png"
        attribute crying if_all "casual":
            "images/tsubaki/face_crying_casual.png"
        attribute crying if_all "uniform":
            "images/tsubaki/face_crying_uniform.png"
        attribute embarrassed if_all "casual":
            "images/tsubaki/face_embarrassed_casual.png"
        attribute embarrassed if_all "uniform":
            "images/tsubaki/face_embarrassed_uniform.png"
        attribute nervous if_all "casual":
            "images/tsubaki/face_nervous_casual.png"
        attribute nervous if_all "uniform":
            "images/tsubaki/face_nervous_uniform.png"
        attribute worried if_all "casual":
            "images/tsubaki/face_worried_casual.png"
        attribute worried if_all "uniform":
            "images/tsubaki/face_worried_uniform.png"
        attribute shocked if_all "casual":
            "images/tsubaki/face_shocked_casual.png"
        attribute shocked if_all "uniform":
            "images/tsubaki/face_shocked_uniform.png"
        attribute afraid if_all "casual":
            "images/tsubaki/face_afraid_casual.png"
        attribute afraid if_all "uniform":
            "images/tsubaki/face_afraid_uniform.png"
        attribute panicked if_all "casual":
            "images/tsubaki/face_panicked_casual.png"
        attribute panicked if_all "uniform":
            "images/tsubaki/face_panicked_uniform.png"
        attribute determined if_all "casual":
            "images/tsubaki/face_determined_casual.png"
        attribute determined if_all "uniform":
            "images/tsubaki/face_determined_uniform.png"
        attribute empty if_all "casual":
            "images/tsubaki/face_empty_casual.png"
        attribute empty if_all "uniform":
            "images/tsubaki/face_empty_uniform.png"
        attribute disgusted if_all "casual":
            "images/tsubaki/face_disgusted_casual.png"
        attribute disgusted if_all "uniform":
            "images/tsubaki/face_disgusted_uniform.png"


image probe_background = Solid("#ece9e2")

transform probe_center:
    xalign 0.5
    yalign 1.0


label start:
    python:
        import os
        _tsubaki_probe_dir = os.environ["TSUBAKI_PROBE_DIR"].replace("\\", "/")

    scene probe_background

    show tsubaki casual neut at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/01_casual_neut.png")

    show tsubaki casual happy at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/02_casual_happy.png")

    show tsubaki casual smug at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/03_casual_smug.png")

    show tsubaki casual teasing at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/04_casual_teasing.png")

    show tsubaki casual thinking at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/05_casual_thinking.png")

    show tsubaki casual curious at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/06_casual_curious.png")

    show tsubaki casual unamused at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/07_casual_unamused.png")

    show tsubaki casual annoyed at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/08_casual_annoyed.png")

    show tsubaki casual frustrated at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/09_casual_frustrated.png")

    show tsubaki casual angry at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/10_casual_angry.png")

    show tsubaki casual sad at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/11_casual_sad.png")

    show tsubaki casual crying at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/12_casual_crying.png")

    show tsubaki casual embarrassed at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/13_casual_embarrassed.png")

    show tsubaki casual nervous at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/14_casual_nervous.png")

    show tsubaki casual worried at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/15_casual_worried.png")

    show tsubaki casual shocked at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/16_casual_shocked.png")

    show tsubaki casual afraid at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/17_casual_afraid.png")

    show tsubaki casual panicked at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/18_casual_panicked.png")

    show tsubaki casual determined at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/19_casual_determined.png")

    show tsubaki casual empty at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/20_casual_empty.png")

    show tsubaki casual disgusted at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/21_casual_disgusted.png")

    show tsubaki uniform neut at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/22_uniform_neut.png")

    show tsubaki uniform happy at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/23_uniform_happy.png")

    show tsubaki uniform smug at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/24_uniform_smug.png")

    show tsubaki uniform teasing at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/25_uniform_teasing.png")

    show tsubaki uniform thinking at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/26_uniform_thinking.png")

    show tsubaki uniform curious at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/27_uniform_curious.png")

    show tsubaki uniform unamused at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/28_uniform_unamused.png")

    show tsubaki uniform annoyed at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/29_uniform_annoyed.png")

    show tsubaki uniform frustrated at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/30_uniform_frustrated.png")

    show tsubaki uniform angry at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/31_uniform_angry.png")

    show tsubaki uniform sad at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/32_uniform_sad.png")

    show tsubaki uniform crying at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/33_uniform_crying.png")

    show tsubaki uniform embarrassed at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/34_uniform_embarrassed.png")

    show tsubaki uniform nervous at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/35_uniform_nervous.png")

    show tsubaki uniform worried at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/36_uniform_worried.png")

    show tsubaki uniform shocked at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/37_uniform_shocked.png")

    show tsubaki uniform afraid at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/38_uniform_afraid.png")

    show tsubaki uniform panicked at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/39_uniform_panicked.png")

    show tsubaki uniform determined at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/40_uniform_determined.png")

    show tsubaki uniform empty at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/41_uniform_empty.png")

    show tsubaki uniform disgusted at probe_center
    $ renpy.pause(0.25, hard=True)
    $ renpy.screenshot(_tsubaki_probe_dir + "/42_uniform_disgusted.png")

    $ renpy.quit()
    return
