transform kotonoha_sprite_size:
    fit "contain"
    xysize (640, 960)

layeredimage kotonoha:
    at kotonoha_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "images/kotonoha/neutral.png"
        attribute work:
            "images/kotonoha/work.png"

    group face:
        attribute neut default if_all "casual":
            "images/kotonoha/face_neut_casual.png"
        attribute neut if_all "work":
            "images/kotonoha/face_neut_work.png"
        attribute happy if_all "casual":
            "images/kotonoha/face_happy_casual.png"
        attribute happy if_all "work":
            "images/kotonoha/face_happy_work.png"
        attribute smug if_all "casual":
            "images/kotonoha/face_smug_casual.png"
        attribute smug if_all "work":
            "images/kotonoha/face_smug_work.png"
        attribute teasing if_all "casual":
            "images/kotonoha/face_teasing_casual.png"
        attribute teasing if_all "work":
            "images/kotonoha/face_teasing_work.png"
        attribute thinking if_all "casual":
            "images/kotonoha/face_thinking_casual.png"
        attribute thinking if_all "work":
            "images/kotonoha/face_thinking_work.png"
        attribute curious if_all "casual":
            "images/kotonoha/face_curious_casual.png"
        attribute curious if_all "work":
            "images/kotonoha/face_curious_work.png"
        attribute unamused if_all "casual":
            "images/kotonoha/face_unamused_casual.png"
        attribute unamused if_all "work":
            "images/kotonoha/face_unamused_work.png"
        attribute annoyed if_all "casual":
            "images/kotonoha/face_annoyed_casual.png"
        attribute annoyed if_all "work":
            "images/kotonoha/face_annoyed_work.png"
        attribute frustrated if_all "casual":
            "images/kotonoha/face_frustrated_casual.png"
        attribute frustrated if_all "work":
            "images/kotonoha/face_frustrated_work.png"
        attribute angry if_all "casual":
            "images/kotonoha/face_angry_casual.png"
        attribute angry if_all "work":
            "images/kotonoha/face_angry_work.png"
        attribute sad if_all "casual":
            "images/kotonoha/face_sad_casual.png"
        attribute sad if_all "work":
            "images/kotonoha/face_sad_work.png"
        attribute crying if_all "casual":
            "images/kotonoha/face_crying_casual.png"
        attribute crying if_all "work":
            "images/kotonoha/face_crying_work.png"
        attribute embarrassed if_all "casual":
            "images/kotonoha/face_embarrassed_casual.png"
        attribute embarrassed if_all "work":
            "images/kotonoha/face_embarrassed_work.png"
        attribute nervous if_all "casual":
            "images/kotonoha/face_nervous_casual.png"
        attribute nervous if_all "work":
            "images/kotonoha/face_nervous_work.png"
        attribute worried if_all "casual":
            "images/kotonoha/face_worried_casual.png"
        attribute worried if_all "work":
            "images/kotonoha/face_worried_work.png"
        attribute shocked if_all "casual":
            "images/kotonoha/face_shocked_casual.png"
        attribute shocked if_all "work":
            "images/kotonoha/face_shocked_work.png"
        attribute afraid if_all "casual":
            "images/kotonoha/face_afraid_casual.png"
        attribute afraid if_all "work":
            "images/kotonoha/face_afraid_work.png"
        attribute panicked if_all "casual":
            "images/kotonoha/face_panicked_casual.png"
        attribute panicked if_all "work":
            "images/kotonoha/face_panicked_work.png"
        attribute determined if_all "casual":
            "images/kotonoha/face_determined_casual.png"
        attribute determined if_all "work":
            "images/kotonoha/face_determined_work.png"
        attribute empty if_all "casual":
            "images/kotonoha/face_empty_casual.png"
        attribute empty if_all "work":
            "images/kotonoha/face_empty_work.png"
        attribute disgusted if_all "casual":
            "images/kotonoha/face_disgusted_casual.png"
        attribute disgusted if_all "work":
            "images/kotonoha/face_disgusted_work.png"

image kotonoha work pose_exact_fold = Transform("images/kotonoha/pose_exact_fold_work.png", fit="contain", xysize=(640, 960))
image kotonoha casual pose_watching = Transform("images/kotonoha/pose_watching_casual.png", fit="contain", xysize=(640, 960))
image kotonoha casual pose_open_hands = Transform("images/kotonoha/pose_open_hands_casual.png", fit="contain", xysize=(640, 960))


image probe_background_light = Solid("#ece9e2")
image probe_background_dark = Solid("#202229")
image probe_background_checker = Tile("images/probe_checker.png")

transform probe_center:
    xalign 0.5
    yalign 1.0


label start:
    python:
        import os
        _kotonoha_probe_dir = os.environ["KOTONOHA_PROBE_DIR"].replace("\\", "/")

    scene probe_background_light

    show kotonoha casual neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/01_casual_neut.png")

    show kotonoha casual happy at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/02_casual_happy.png")

    show kotonoha casual smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/03_casual_smug.png")

    show kotonoha casual teasing at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/04_casual_teasing.png")

    show kotonoha casual thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/05_casual_thinking.png")

    show kotonoha casual curious at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/06_casual_curious.png")

    show kotonoha casual unamused at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/07_casual_unamused.png")

    show kotonoha casual annoyed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/08_casual_annoyed.png")

    show kotonoha casual frustrated at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/09_casual_frustrated.png")

    show kotonoha casual angry at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/10_casual_angry.png")

    show kotonoha casual sad at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/11_casual_sad.png")

    show kotonoha casual crying at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/12_casual_crying.png")

    show kotonoha casual embarrassed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/13_casual_embarrassed.png")

    show kotonoha casual nervous at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/14_casual_nervous.png")

    show kotonoha casual worried at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/15_casual_worried.png")

    show kotonoha casual shocked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/16_casual_shocked.png")

    show kotonoha casual afraid at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/17_casual_afraid.png")

    show kotonoha casual panicked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/18_casual_panicked.png")

    show kotonoha casual determined at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/19_casual_determined.png")

    show kotonoha casual empty at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/20_casual_empty.png")

    show kotonoha casual disgusted at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/21_casual_disgusted.png")

    show kotonoha work neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/22_work_neut.png")

    show kotonoha work happy at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/23_work_happy.png")

    show kotonoha work smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/24_work_smug.png")

    show kotonoha work teasing at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/25_work_teasing.png")

    show kotonoha work thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/26_work_thinking.png")

    show kotonoha work curious at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/27_work_curious.png")

    show kotonoha work unamused at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/28_work_unamused.png")

    show kotonoha work annoyed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/29_work_annoyed.png")

    show kotonoha work frustrated at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/30_work_frustrated.png")

    show kotonoha work angry at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/31_work_angry.png")

    show kotonoha work sad at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/32_work_sad.png")

    show kotonoha work crying at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/33_work_crying.png")

    show kotonoha work embarrassed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/34_work_embarrassed.png")

    show kotonoha work nervous at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/35_work_nervous.png")

    show kotonoha work worried at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/36_work_worried.png")

    show kotonoha work shocked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/37_work_shocked.png")

    show kotonoha work afraid at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/38_work_afraid.png")

    show kotonoha work panicked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/39_work_panicked.png")

    show kotonoha work determined at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/40_work_determined.png")

    show kotonoha work empty at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/41_work_empty.png")

    show kotonoha work disgusted at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/expressions/42_work_disgusted.png")

    show kotonoha work pose_exact_fold at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/poses/01_work_pose_exact_fold.png")

    show kotonoha casual pose_watching at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/poses/02_casual_pose_watching.png")

    show kotonoha casual pose_open_hands at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/light/poses/03_casual_pose_open_hands.png")

    scene probe_background_dark

    show kotonoha casual neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/01_casual_neut.png")

    show kotonoha casual happy at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/02_casual_happy.png")

    show kotonoha casual smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/03_casual_smug.png")

    show kotonoha casual teasing at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/04_casual_teasing.png")

    show kotonoha casual thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/05_casual_thinking.png")

    show kotonoha casual curious at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/06_casual_curious.png")

    show kotonoha casual unamused at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/07_casual_unamused.png")

    show kotonoha casual annoyed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/08_casual_annoyed.png")

    show kotonoha casual frustrated at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/09_casual_frustrated.png")

    show kotonoha casual angry at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/10_casual_angry.png")

    show kotonoha casual sad at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/11_casual_sad.png")

    show kotonoha casual crying at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/12_casual_crying.png")

    show kotonoha casual embarrassed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/13_casual_embarrassed.png")

    show kotonoha casual nervous at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/14_casual_nervous.png")

    show kotonoha casual worried at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/15_casual_worried.png")

    show kotonoha casual shocked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/16_casual_shocked.png")

    show kotonoha casual afraid at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/17_casual_afraid.png")

    show kotonoha casual panicked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/18_casual_panicked.png")

    show kotonoha casual determined at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/19_casual_determined.png")

    show kotonoha casual empty at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/20_casual_empty.png")

    show kotonoha casual disgusted at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/21_casual_disgusted.png")

    show kotonoha work neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/22_work_neut.png")

    show kotonoha work happy at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/23_work_happy.png")

    show kotonoha work smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/24_work_smug.png")

    show kotonoha work teasing at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/25_work_teasing.png")

    show kotonoha work thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/26_work_thinking.png")

    show kotonoha work curious at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/27_work_curious.png")

    show kotonoha work unamused at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/28_work_unamused.png")

    show kotonoha work annoyed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/29_work_annoyed.png")

    show kotonoha work frustrated at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/30_work_frustrated.png")

    show kotonoha work angry at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/31_work_angry.png")

    show kotonoha work sad at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/32_work_sad.png")

    show kotonoha work crying at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/33_work_crying.png")

    show kotonoha work embarrassed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/34_work_embarrassed.png")

    show kotonoha work nervous at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/35_work_nervous.png")

    show kotonoha work worried at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/36_work_worried.png")

    show kotonoha work shocked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/37_work_shocked.png")

    show kotonoha work afraid at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/38_work_afraid.png")

    show kotonoha work panicked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/39_work_panicked.png")

    show kotonoha work determined at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/40_work_determined.png")

    show kotonoha work empty at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/41_work_empty.png")

    show kotonoha work disgusted at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/expressions/42_work_disgusted.png")

    show kotonoha work pose_exact_fold at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/poses/01_work_pose_exact_fold.png")

    show kotonoha casual pose_watching at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/poses/02_casual_pose_watching.png")

    show kotonoha casual pose_open_hands at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/dark/poses/03_casual_pose_open_hands.png")

    scene probe_background_checker

    show kotonoha casual neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/01_casual_neut.png")

    show kotonoha casual happy at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/02_casual_happy.png")

    show kotonoha casual smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/03_casual_smug.png")

    show kotonoha casual teasing at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/04_casual_teasing.png")

    show kotonoha casual thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/05_casual_thinking.png")

    show kotonoha casual curious at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/06_casual_curious.png")

    show kotonoha casual unamused at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/07_casual_unamused.png")

    show kotonoha casual annoyed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/08_casual_annoyed.png")

    show kotonoha casual frustrated at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/09_casual_frustrated.png")

    show kotonoha casual angry at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/10_casual_angry.png")

    show kotonoha casual sad at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/11_casual_sad.png")

    show kotonoha casual crying at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/12_casual_crying.png")

    show kotonoha casual embarrassed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/13_casual_embarrassed.png")

    show kotonoha casual nervous at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/14_casual_nervous.png")

    show kotonoha casual worried at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/15_casual_worried.png")

    show kotonoha casual shocked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/16_casual_shocked.png")

    show kotonoha casual afraid at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/17_casual_afraid.png")

    show kotonoha casual panicked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/18_casual_panicked.png")

    show kotonoha casual determined at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/19_casual_determined.png")

    show kotonoha casual empty at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/20_casual_empty.png")

    show kotonoha casual disgusted at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/21_casual_disgusted.png")

    show kotonoha work neut at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/22_work_neut.png")

    show kotonoha work happy at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/23_work_happy.png")

    show kotonoha work smug at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/24_work_smug.png")

    show kotonoha work teasing at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/25_work_teasing.png")

    show kotonoha work thinking at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/26_work_thinking.png")

    show kotonoha work curious at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/27_work_curious.png")

    show kotonoha work unamused at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/28_work_unamused.png")

    show kotonoha work annoyed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/29_work_annoyed.png")

    show kotonoha work frustrated at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/30_work_frustrated.png")

    show kotonoha work angry at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/31_work_angry.png")

    show kotonoha work sad at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/32_work_sad.png")

    show kotonoha work crying at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/33_work_crying.png")

    show kotonoha work embarrassed at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/34_work_embarrassed.png")

    show kotonoha work nervous at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/35_work_nervous.png")

    show kotonoha work worried at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/36_work_worried.png")

    show kotonoha work shocked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/37_work_shocked.png")

    show kotonoha work afraid at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/38_work_afraid.png")

    show kotonoha work panicked at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/39_work_panicked.png")

    show kotonoha work determined at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/40_work_determined.png")

    show kotonoha work empty at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/41_work_empty.png")

    show kotonoha work disgusted at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/expressions/42_work_disgusted.png")

    show kotonoha work pose_exact_fold at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/poses/01_work_pose_exact_fold.png")

    show kotonoha casual pose_watching at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/poses/02_casual_pose_watching.png")

    show kotonoha casual pose_open_hands at probe_center
    $ renpy.pause(0.10, hard=True)
    $ renpy.screenshot(_kotonoha_probe_dir + "/checker/poses/03_casual_pose_open_hands.png")

    $ renpy.quit()
    return
