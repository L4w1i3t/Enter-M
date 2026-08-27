# =============================================================================
# def_characters.rpy  --  ENTER M cast: sprites, Characters, display names
# =============================================================================
#
# WHAT THIS FILE IS
#   Every ENTER M character the story can speak as, plus their project-local
#   sprites. Vanilla DDLC's own cast lives in game/definitions.rpy; nothing here
#   overrides it.
#
# THE TWO KINDS OF ENTRY
#   Named cast use DynamicCharacter so the player-facing name can change at
#   runtime (the ID-card screen renames MC; a story beat could rename anyone
#   else). Their name lives in a `default <x>_name` variable.
#   Incidental cast (teachers, Coach, club regulars, NPCs) use a plain Character
#   because their names are fixed.
#
# HOUSE STYLE FOR A NEW CHARACTER
#   image <tag> neut = Transform("assets/characters/<folder>/neutral.png",
#                                fit="contain", xysize=(640, 960))
#   define <short> = DynamicCharacter('<short>_name', image='<tag>', **SAY_STYLE)
#   default <short>_name = "Display Name"
#   SAY_STYLE is the shared quote-marks + click-to-continue kwargs below, so a
#   change to the say style is a one-line change instead of a 20-line sweep.
#
# RELATED FILES
#   def_audio.rpy   -- music / SFX aliases and the extra audio channels
#   def_images.rpy  -- backgrounds and CGs
# =============================================================================

init -1 python:
    # Shared say-window styling for the whole ENTER M cast. Vanilla DDLC draws
    # dialogue without quote marks; ENTER M quotes spoken lines and shows the
    # click-to-continue caret in a fixed corner.
    SAY_STYLE = dict(what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")


# -----------------------------------------------------------------------------
# Named cast -- renameable at runtime
# -----------------------------------------------------------------------------

# Every cast sprite is normalised to the same 640x960 canvas. That makes them all
# one SIZE rather than one SCALE -- see docs/cutting-room/sprite-height-scaling.md
# for the measured version of that problem and the shelved fix.

transform matsuda_sprite_size:
    fit "contain"
    xysize (640, 960)


# Matsuda's outfit-native neutral sprites are the fixed bases for her expression
# bank. Each face patch is registered independently to the corresponding
# 1023x1537 outfit canvas, so changing expressions cannot move or crop her body.
# Flatten after sizing so fades and Autofocus alpha apply once to the composed
# sprite instead of once per overlapping layer.
# Authoring tokens mirror docs/project/TODO.txt; Neutral stays `neut` for compatibility,
# and Empty/Dead-eyed is the `empty` attribute.
layeredimage matsuda:
    at matsuda_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "assets/characters/matsuda/neutral.png"
        attribute uniform:
            "assets/characters/matsuda/neut_uniform.png"

    group face:
        attribute neut default if_all "casual":
            "assets/characters/matsuda/face_neut_casual.png"
        attribute neut if_all "uniform":
            "assets/characters/matsuda/face_neut_uniform.png"
        attribute happy if_all "casual":
            "assets/characters/matsuda/face_happy_casual.png"
        attribute happy if_all "uniform":
            "assets/characters/matsuda/face_happy_uniform.png"
        attribute smug if_all "casual":
            "assets/characters/matsuda/face_smug_casual.png"
        attribute smug if_all "uniform":
            "assets/characters/matsuda/face_smug_uniform.png"
        attribute teasing if_all "casual":
            "assets/characters/matsuda/face_teasing_casual.png"
        attribute teasing if_all "uniform":
            "assets/characters/matsuda/face_teasing_uniform.png"
        attribute thinking if_all "casual":
            "assets/characters/matsuda/face_thinking_casual.png"
        attribute thinking if_all "uniform":
            "assets/characters/matsuda/face_thinking_uniform.png"
        attribute curious if_all "casual":
            "assets/characters/matsuda/face_curious_casual.png"
        attribute curious if_all "uniform":
            "assets/characters/matsuda/face_curious_uniform.png"
        attribute unamused if_all "casual":
            "assets/characters/matsuda/face_unamused_casual.png"
        attribute unamused if_all "uniform":
            "assets/characters/matsuda/face_unamused_uniform.png"
        attribute annoyed if_all "casual":
            "assets/characters/matsuda/face_annoyed_casual.png"
        attribute annoyed if_all "uniform":
            "assets/characters/matsuda/face_annoyed_uniform.png"
        attribute frustrated if_all "casual":
            "assets/characters/matsuda/face_frustrated_casual.png"
        attribute frustrated if_all "uniform":
            "assets/characters/matsuda/face_frustrated_uniform.png"
        attribute angry if_all "casual":
            "assets/characters/matsuda/face_angry_casual.png"
        attribute angry if_all "uniform":
            "assets/characters/matsuda/face_angry_uniform.png"
        attribute sad if_all "casual":
            "assets/characters/matsuda/face_sad_casual.png"
        attribute sad if_all "uniform":
            "assets/characters/matsuda/face_sad_uniform.png"
        attribute crying if_all "casual":
            "assets/characters/matsuda/face_crying_casual.png"
        attribute crying if_all "uniform":
            "assets/characters/matsuda/face_crying_uniform.png"
        attribute embarrassed if_all "casual":
            "assets/characters/matsuda/face_embarrassed_casual.png"
        attribute embarrassed if_all "uniform":
            "assets/characters/matsuda/face_embarrassed_uniform.png"
        attribute nervous if_all "casual":
            "assets/characters/matsuda/face_nervous_casual.png"
        attribute nervous if_all "uniform":
            "assets/characters/matsuda/face_nervous_uniform.png"
        attribute worried if_all "casual":
            "assets/characters/matsuda/face_worried_casual.png"
        attribute worried if_all "uniform":
            "assets/characters/matsuda/face_worried_uniform.png"
        attribute shocked if_all "casual":
            "assets/characters/matsuda/face_shocked_casual.png"
        attribute shocked if_all "uniform":
            "assets/characters/matsuda/face_shocked_uniform.png"
        attribute afraid if_all "casual":
            "assets/characters/matsuda/face_afraid_casual.png"
        attribute afraid if_all "uniform":
            "assets/characters/matsuda/face_afraid_uniform.png"
        attribute panicked if_all "casual":
            "assets/characters/matsuda/face_panicked_casual.png"
        attribute panicked if_all "uniform":
            "assets/characters/matsuda/face_panicked_uniform.png"
        attribute determined if_all "casual":
            "assets/characters/matsuda/face_determined_casual.png"
        attribute determined if_all "uniform":
            "assets/characters/matsuda/face_determined_uniform.png"
        attribute empty if_all "casual":
            "assets/characters/matsuda/face_empty_casual.png"
        attribute empty if_all "uniform":
            "assets/characters/matsuda/face_empty_uniform.png"
        attribute disgusted if_all "casual":
            "assets/characters/matsuda/face_disgusted_casual.png"
        attribute disgusted if_all "uniform":
            "assets/characters/matsuda/face_disgusted_uniform.png"

# These four full-body reactions use five files because laughing supports both
# outfits. Each pose has a fixed face, outfit, and silhouette.
# Keeping them outside the layered image prevents its default torso and face
# from appearing behind poses that move Matsuda's arms and hair.
image matsuda uniform pose_facepalm = Transform("assets/characters/matsuda/pose_facepalm_uniform.png", fit="contain", xysize=(640, 960))
image matsuda uniform pose_chuuni = Transform("assets/characters/matsuda/pose_chuuni_uniform.png", fit="contain", xysize=(640, 960))
image matsuda uniform pose_shrug = Transform("assets/characters/matsuda/pose_shrug_uniform.png", fit="contain", xysize=(640, 960))
image matsuda casual pose_laughing = Transform("assets/characters/matsuda/pose_laughing_casual.png", fit="contain", xysize=(640, 960))
image matsuda uniform pose_laughing = Transform("assets/characters/matsuda/pose_laughing_uniform.png", fit="contain", xysize=(640, 960))

transform tsubaki_sprite_size:
    fit "contain"
    xysize (640, 960)


# Tsubaki's outfit-native neutral sprites are the fixed bases for her expression
# bank. Each alternate face is registered independently to the corresponding
# 1023x1537 outfit canvas, so changing expressions cannot move or crop her body.
layeredimage tsubaki:
    at tsubaki_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "assets/characters/tsubaki/neutral.png"
        attribute uniform:
            "assets/characters/tsubaki/neut_uniform.png"

    group face:
        attribute neut default if_all "casual":
            "assets/characters/tsubaki/face_neut_casual.png"
        attribute neut if_all "uniform":
            "assets/characters/tsubaki/face_neut_uniform.png"
        attribute happy if_all "casual":
            "assets/characters/tsubaki/face_happy_casual.png"
        attribute happy if_all "uniform":
            "assets/characters/tsubaki/face_happy_uniform.png"
        attribute smug if_all "casual":
            "assets/characters/tsubaki/face_smug_casual.png"
        attribute smug if_all "uniform":
            "assets/characters/tsubaki/face_smug_uniform.png"
        attribute teasing if_all "casual":
            "assets/characters/tsubaki/face_teasing_casual.png"
        attribute teasing if_all "uniform":
            "assets/characters/tsubaki/face_teasing_uniform.png"
        attribute thinking if_all "casual":
            "assets/characters/tsubaki/face_thinking_casual.png"
        attribute thinking if_all "uniform":
            "assets/characters/tsubaki/face_thinking_uniform.png"
        attribute curious if_all "casual":
            "assets/characters/tsubaki/face_curious_casual.png"
        attribute curious if_all "uniform":
            "assets/characters/tsubaki/face_curious_uniform.png"
        attribute unamused if_all "casual":
            "assets/characters/tsubaki/face_unamused_casual.png"
        attribute unamused if_all "uniform":
            "assets/characters/tsubaki/face_unamused_uniform.png"
        attribute annoyed if_all "casual":
            "assets/characters/tsubaki/face_annoyed_casual.png"
        attribute annoyed if_all "uniform":
            "assets/characters/tsubaki/face_annoyed_uniform.png"
        attribute frustrated if_all "casual":
            "assets/characters/tsubaki/face_frustrated_casual.png"
        attribute frustrated if_all "uniform":
            "assets/characters/tsubaki/face_frustrated_uniform.png"
        attribute angry if_all "casual":
            "assets/characters/tsubaki/face_angry_casual.png"
        attribute angry if_all "uniform":
            "assets/characters/tsubaki/face_angry_uniform.png"
        attribute sad if_all "casual":
            "assets/characters/tsubaki/face_sad_casual.png"
        attribute sad if_all "uniform":
            "assets/characters/tsubaki/face_sad_uniform.png"
        attribute crying if_all "casual":
            "assets/characters/tsubaki/face_crying_casual.png"
        attribute crying if_all "uniform":
            "assets/characters/tsubaki/face_crying_uniform.png"
        attribute embarrassed if_all "casual":
            "assets/characters/tsubaki/face_embarrassed_casual.png"
        attribute embarrassed if_all "uniform":
            "assets/characters/tsubaki/face_embarrassed_uniform.png"
        attribute nervous if_all "casual":
            "assets/characters/tsubaki/face_nervous_casual.png"
        attribute nervous if_all "uniform":
            "assets/characters/tsubaki/face_nervous_uniform.png"
        attribute worried if_all "casual":
            "assets/characters/tsubaki/face_worried_casual.png"
        attribute worried if_all "uniform":
            "assets/characters/tsubaki/face_worried_uniform.png"
        attribute shocked if_all "casual":
            "assets/characters/tsubaki/face_shocked_casual.png"
        attribute shocked if_all "uniform":
            "assets/characters/tsubaki/face_shocked_uniform.png"
        attribute afraid if_all "casual":
            "assets/characters/tsubaki/face_afraid_casual.png"
        attribute afraid if_all "uniform":
            "assets/characters/tsubaki/face_afraid_uniform.png"
        attribute panicked if_all "casual":
            "assets/characters/tsubaki/face_panicked_casual.png"
        attribute panicked if_all "uniform":
            "assets/characters/tsubaki/face_panicked_uniform.png"
        attribute determined if_all "casual":
            "assets/characters/tsubaki/face_determined_casual.png"
        attribute determined if_all "uniform":
            "assets/characters/tsubaki/face_determined_uniform.png"
        attribute empty if_all "casual":
            "assets/characters/tsubaki/face_empty_casual.png"
        attribute empty if_all "uniform":
            "assets/characters/tsubaki/face_empty_uniform.png"
        attribute disgusted if_all "casual":
            "assets/characters/tsubaki/face_disgusted_casual.png"
        attribute disgusted if_all "uniform":
            "assets/characters/tsubaki/face_disgusted_uniform.png"

image tsubaki post_neut = Transform("assets/characters/tsubaki/post_neut.png", fit="contain", xysize=(640, 960)) # her "metamorphosis" transformation
image tsubaki post_revelation = Transform("assets/characters/tsubaki/post_rev.png", fit="contain", xysize=(640, 960)) # same as above, but with a psychotic expression, like she had a revelation

transform asahina_sprite_size:
    fit "contain"
    xysize (640, 960)


# Asahina's intact neutral sprites are the fixed outfit bases. Neutral is a
# transparent compatibility layer; every alternate is one registered,
# feathered head replacement shared by the matching neutral head geometry.
# This mirrors Himeko's simple base + face-plate setup without featureless-body
# intermediates, while preserving the original 1023x1537 stage registration.
layeredimage asahina:
    at asahina_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "assets/characters/asahina/neutral.png"
        attribute uniform:
            "assets/characters/asahina/neut_uniform.png"

    group face:
        attribute neut default:
            "assets/characters/asahina/face_neut.png"
        attribute happy:
            "assets/characters/asahina/face_happy.png"
        attribute smug:
            "assets/characters/asahina/face_smug.png"
        attribute teasing:
            "assets/characters/asahina/face_teasing.png"
        attribute thinking:
            "assets/characters/asahina/face_thinking.png"
        attribute curious:
            "assets/characters/asahina/face_curious.png"
        attribute unamused:
            "assets/characters/asahina/face_unamused.png"
        attribute annoyed:
            "assets/characters/asahina/face_annoyed.png"
        attribute frustrated:
            "assets/characters/asahina/face_frustrated.png"
        attribute angry:
            "assets/characters/asahina/face_angry.png"
        attribute sad:
            "assets/characters/asahina/face_sad.png"
        attribute crying:
            "assets/characters/asahina/face_crying.png"
        attribute embarrassed:
            "assets/characters/asahina/face_embarrassed.png"
        attribute nervous:
            "assets/characters/asahina/face_nervous.png"
        attribute worried:
            "assets/characters/asahina/face_worried.png"
        attribute shocked:
            "assets/characters/asahina/face_shocked.png"
        attribute afraid:
            "assets/characters/asahina/face_afraid.png"
        attribute panicked:
            "assets/characters/asahina/face_panicked.png"
        attribute determined:
            "assets/characters/asahina/face_determined.png"
        attribute empty:
            "assets/characters/asahina/face_empty.png"
        attribute disgusted:
            "assets/characters/asahina/face_disgusted.png"

# Full-body reactions stay outside the layered image because their arms, hair,
# and head angles change. `terror` remains as a public compatibility alias for
# the newly generated phone-panic pose used by the 10/30 story beat.
image asahina uniform pose_hairflip = Transform("assets/characters/asahina/pose_hairflip_uniform.png", fit="contain", xysize=(640, 960))
image asahina uniform pose_pointing = Transform("assets/characters/asahina/pose_pointing_uniform.png", fit="contain", xysize=(640, 960))
image asahina uniform pose_eyeroll = Transform("assets/characters/asahina/pose_eyeroll_uniform.png", fit="contain", xysize=(640, 960))
image asahina uniform pose_phone_panic = Transform("assets/characters/asahina/pose_phone_panic_uniform.png", fit="contain", xysize=(640, 960))
image asahina uniform terror = Transform("assets/characters/asahina/pose_phone_panic_uniform.png", fit="contain", xysize=(640, 960)) # unique sprite on 10/30 where she receives a bone-chilling text from mom to come home IMMEDIATELY after school and that she has some explaining to do

transform sam_sprite_size:
    fit "contain"
    xysize (640, 960)


# Sam's intact neutral sprites are the fixed outfit bases. Neutral is a
# transparent compatibility layer; every alternate is one registered,
# feathered face replacement shared by both identically registered outfits.
# Empty/Dead-eyed uses the `empty` attribute like the rest of the cast.
layeredimage sam:
    at sam_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "assets/characters/masayami/neutral.png"
        attribute uniform:
            "assets/characters/masayami/neut_uniform.png"

    group face:
        attribute neut default:
            "assets/characters/masayami/face_neut.png"
        attribute happy:
            "assets/characters/masayami/face_happy.png"
        attribute smug:
            "assets/characters/masayami/face_smug.png"
        attribute teasing:
            "assets/characters/masayami/face_teasing.png"
        attribute thinking:
            "assets/characters/masayami/face_thinking.png"
        attribute curious:
            "assets/characters/masayami/face_curious.png"
        attribute unamused:
            "assets/characters/masayami/face_unamused.png"
        attribute annoyed:
            "assets/characters/masayami/face_annoyed.png"
        attribute frustrated:
            "assets/characters/masayami/face_frustrated.png"
        attribute angry:
            "assets/characters/masayami/face_angry.png"
        attribute sad:
            "assets/characters/masayami/face_sad.png"
        attribute crying:
            "assets/characters/masayami/face_crying.png"
        attribute embarrassed:
            "assets/characters/masayami/face_embarrassed.png"
        attribute nervous:
            "assets/characters/masayami/face_nervous.png"
        attribute worried:
            "assets/characters/masayami/face_worried.png"
        attribute shocked:
            "assets/characters/masayami/face_shocked.png"
        attribute afraid:
            "assets/characters/masayami/face_afraid.png"
        attribute panicked:
            "assets/characters/masayami/face_panicked.png"
        attribute determined:
            "assets/characters/masayami/face_determined.png"
        attribute empty:
            "assets/characters/masayami/face_empty.png"
        attribute disgusted:
            "assets/characters/masayami/face_disgusted.png"

# These full-body reactions have fixed outfits and silhouettes, so they stay
# outside the layered image instead of inheriting its default torso and face.
image sam casual pose_open_hand = Transform("assets/characters/masayami/pose_open_hand_casual.png", fit="contain", xysize=(640, 960))
image sam uniform pose_crossed = Transform("assets/characters/masayami/pose_crossed_uniform.png", fit="contain", xysize=(640, 960))
image sam uniform pose_thinking = Transform("assets/characters/masayami/pose_thinking_uniform.png", fit="contain", xysize=(640, 960))
image sam casual pose_phone = Transform("assets/characters/masayami/pose_phone_casual.png", fit="contain", xysize=(640, 960))

transform kotonoha_sprite_size:
    fit "contain"
    xysize (640, 960)


# Kotonoha's restrained expression bank uses one registered, fixed feathered
# face plate per outfit. The original casual/work sprites remain byte-exact
# bases, while each conditioned layer changes only her brows, eyes, mouth, and
# expression-specific tears/blush. This preserves her silhouette and subdued
# demeanor without introducing checker, matte, collar, or registration residue.
layeredimage kotonoha:
    at kotonoha_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "assets/characters/kotonoha/neutral.png"
        attribute work:
            "assets/characters/kotonoha/work.png"

    group face:
        attribute neut default if_all "casual":
            "assets/characters/kotonoha/face_neut_casual.png"
        attribute neut if_all "work":
            "assets/characters/kotonoha/face_neut_work.png"
        attribute happy if_all "casual":
            "assets/characters/kotonoha/face_happy_casual.png"
        attribute happy if_all "work":
            "assets/characters/kotonoha/face_happy_work.png"
        attribute smug if_all "casual":
            "assets/characters/kotonoha/face_smug_casual.png"
        attribute smug if_all "work":
            "assets/characters/kotonoha/face_smug_work.png"
        attribute teasing if_all "casual":
            "assets/characters/kotonoha/face_teasing_casual.png"
        attribute teasing if_all "work":
            "assets/characters/kotonoha/face_teasing_work.png"
        attribute thinking if_all "casual":
            "assets/characters/kotonoha/face_thinking_casual.png"
        attribute thinking if_all "work":
            "assets/characters/kotonoha/face_thinking_work.png"
        attribute curious if_all "casual":
            "assets/characters/kotonoha/face_curious_casual.png"
        attribute curious if_all "work":
            "assets/characters/kotonoha/face_curious_work.png"
        attribute unamused if_all "casual":
            "assets/characters/kotonoha/face_unamused_casual.png"
        attribute unamused if_all "work":
            "assets/characters/kotonoha/face_unamused_work.png"
        attribute annoyed if_all "casual":
            "assets/characters/kotonoha/face_annoyed_casual.png"
        attribute annoyed if_all "work":
            "assets/characters/kotonoha/face_annoyed_work.png"
        attribute frustrated if_all "casual":
            "assets/characters/kotonoha/face_frustrated_casual.png"
        attribute frustrated if_all "work":
            "assets/characters/kotonoha/face_frustrated_work.png"
        attribute angry if_all "casual":
            "assets/characters/kotonoha/face_angry_casual.png"
        attribute angry if_all "work":
            "assets/characters/kotonoha/face_angry_work.png"
        attribute sad if_all "casual":
            "assets/characters/kotonoha/face_sad_casual.png"
        attribute sad if_all "work":
            "assets/characters/kotonoha/face_sad_work.png"
        attribute crying if_all "casual":
            "assets/characters/kotonoha/face_crying_casual.png"
        attribute crying if_all "work":
            "assets/characters/kotonoha/face_crying_work.png"
        attribute embarrassed if_all "casual":
            "assets/characters/kotonoha/face_embarrassed_casual.png"
        attribute embarrassed if_all "work":
            "assets/characters/kotonoha/face_embarrassed_work.png"
        attribute nervous if_all "casual":
            "assets/characters/kotonoha/face_nervous_casual.png"
        attribute nervous if_all "work":
            "assets/characters/kotonoha/face_nervous_work.png"
        attribute worried if_all "casual":
            "assets/characters/kotonoha/face_worried_casual.png"
        attribute worried if_all "work":
            "assets/characters/kotonoha/face_worried_work.png"
        attribute shocked if_all "casual":
            "assets/characters/kotonoha/face_shocked_casual.png"
        attribute shocked if_all "work":
            "assets/characters/kotonoha/face_shocked_work.png"
        attribute afraid if_all "casual":
            "assets/characters/kotonoha/face_afraid_casual.png"
        attribute afraid if_all "work":
            "assets/characters/kotonoha/face_afraid_work.png"
        attribute panicked if_all "casual":
            "assets/characters/kotonoha/face_panicked_casual.png"
        attribute panicked if_all "work":
            "assets/characters/kotonoha/face_panicked_work.png"
        attribute determined if_all "casual":
            "assets/characters/kotonoha/face_determined_casual.png"
        attribute determined if_all "work":
            "assets/characters/kotonoha/face_determined_work.png"
        attribute empty if_all "casual":
            "assets/characters/kotonoha/face_empty_casual.png"
        attribute empty if_all "work":
            "assets/characters/kotonoha/face_empty_work.png"
        attribute disgusted if_all "casual":
            "assets/characters/kotonoha/face_disgusted_casual.png"
        attribute disgusted if_all "work":
            "assets/characters/kotonoha/face_disgusted_work.png"

# These fixed mid-thigh poses change arm/hand silhouettes, so they stay outside
# the layered image instead of inheriting its default torso and face plate.
image kotonoha work pose_exact_fold = Transform("assets/characters/kotonoha/pose_exact_fold_work.png", fit="contain", xysize=(640, 960))
image kotonoha casual pose_watching = Transform("assets/characters/kotonoha/pose_watching_casual.png", fit="contain", xysize=(640, 960))
image kotonoha casual pose_open_hands = Transform("assets/characters/kotonoha/pose_open_hands_casual.png", fit="contain", xysize=(640, 960))

transform mom_sprite_size:
    fit "contain"
    xysize (640, 960)


# Himeko's two forward-facing outfits share one registered expression bank. The
# original 1023x1537 sprites stay intact as the bases; each alternate face is a
# feathered patch aligned to Casual Neutral before it is exported on that same
# full canvas. This keeps the head, glasses, silhouette, and stage placement
# fixed and prevents the generator's transparency checker from entering Ren'Py.
layeredimage mom:
    at mom_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "assets/characters/himeko/neut_face_base.png"
        attribute uniform:
            "assets/characters/himeko/neut_uniform_face_base.png"

    group face:
        attribute neut default:
            "assets/characters/himeko/face_neut.png"
        attribute happy:
            "assets/characters/himeko/face_happy.png"
        attribute smug:
            "assets/characters/himeko/face_smug.png"
        attribute teasing:
            "assets/characters/himeko/face_teasing.png"
        attribute thinking:
            "assets/characters/himeko/face_thinking.png"
        attribute curious:
            "assets/characters/himeko/face_curious.png"
        attribute unamused:
            "assets/characters/himeko/face_unamused.png"
        attribute annoyed:
            "assets/characters/himeko/face_annoyed.png"
        attribute frustrated:
            "assets/characters/himeko/face_frustrated.png"
        attribute angry:
            "assets/characters/himeko/face_angry.png"
        attribute sad:
            "assets/characters/himeko/face_sad.png"
        attribute crying:
            "assets/characters/himeko/face_crying.png"
        attribute embarrassed:
            "assets/characters/himeko/face_embarrassed.png"
        attribute nervous:
            "assets/characters/himeko/face_nervous.png"
        attribute worried:
            "assets/characters/himeko/face_worried.png"
        attribute shocked:
            "assets/characters/himeko/face_shocked.png"
        attribute afraid:
            "assets/characters/himeko/face_afraid.png"
        attribute panicked:
            "assets/characters/himeko/face_panicked.png"
        attribute determined:
            "assets/characters/himeko/face_determined.png"
        attribute empty:
            "assets/characters/himeko/face_empty.png"
        attribute disgusted:
            "assets/characters/himeko/face_disgusted.png"

# These reactions change Himeko's head or full-body silhouette, so exact image
# names keep the layered image's default body and face from appearing beneath
# them. The legacy `mom wasted` name remains for its existing story/UI callers.
image mom wasted = Transform("assets/characters/himeko/wasted.png", fit="contain", xysize=(640, 960))
image mom casual pose_wasted = Transform("assets/characters/himeko/wasted.png", fit="contain", xysize=(640, 960))
image mom casual pose_furious = Transform("assets/characters/himeko/pose_furious_casual.png", fit="contain", xysize=(640, 960))
image mom uniform pose_objection = Transform("assets/characters/himeko/pose_objection_uniform.png", fit="contain", xysize=(640, 960))

transform mc_sprite_size:
    fit "contain"
    xysize (640, 960)


# Asahiko's front-facing casual neutral is the fixed base for his expression
# bank. Neutral is a transparent compatibility layer, so every existing
# `mc neut` caller draws the canonical base without changing its public image
# name, stage size, or framing.
layeredimage mc:
    at mc_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "assets/characters/mc/neutral.png"

    group face:
        attribute neut default:
            "assets/characters/mc/face_neut.png"
        attribute happy:
            "assets/characters/mc/face_happy.png"
        attribute smug:
            "assets/characters/mc/face_smug.png"
        attribute teasing:
            "assets/characters/mc/face_teasing.png"
        attribute thinking:
            "assets/characters/mc/face_thinking.png"
        attribute curious:
            "assets/characters/mc/face_curious.png"
        attribute unamused:
            "assets/characters/mc/face_unamused.png"
        attribute annoyed:
            "assets/characters/mc/face_annoyed.png"
        attribute frustrated:
            "assets/characters/mc/face_frustrated.png"
        attribute angry:
            "assets/characters/mc/face_angry.png"
        attribute sad:
            "assets/characters/mc/face_sad.png"
        attribute crying:
            "assets/characters/mc/face_crying.png"
        attribute embarrassed:
            "assets/characters/mc/face_embarrassed.png"
        attribute nervous:
            "assets/characters/mc/face_nervous.png"
        attribute worried:
            "assets/characters/mc/face_worried.png"
        attribute shocked:
            "assets/characters/mc/face_shocked.png"
        attribute afraid:
            "assets/characters/mc/face_afraid.png"
        attribute panicked:
            "assets/characters/mc/face_panicked.png"
        attribute determined:
            "assets/characters/mc/face_determined.png"
        attribute empty:
            "assets/characters/mc/face_empty.png"
        attribute disgusted:
            "assets/characters/mc/face_disgusted.png"

define ma = DynamicCharacter('ma_name', image='matsuda', **SAY_STYLE)
define ts = DynamicCharacter('ts_name', image='tsubaki', **SAY_STYLE)
define ah = DynamicCharacter('as_name', image='asahina', **SAY_STYLE)
define sa = DynamicCharacter('sa_name', image='sam', **SAY_STYLE)
define ko = DynamicCharacter('ko_name', image='kotonoha', **SAY_STYLE)
define mom = DynamicCharacter('mom_name', image='mom', **SAY_STYLE)

default ma_name = "Matsuda"
default ts_name = "Tsubaki"
default as_name = "Asahina"
default sa_name = "Sam"
default ko_name = "Kotonoha"
# "Mom" is her name to MC, not the common noun -- see the capitalisation rule
# used throughout season one.
default mom_name = "Mom"


# -----------------------------------------------------------------------------
# Incidental cast -- fixed names, several still on the placeholder sprite
# -----------------------------------------------------------------------------

image math_teacher neut = Transform("assets/characters/npc/math_teacher.png", fit="contain", xysize=(640, 960))
image civics_teacher neut = Transform("assets/characters/npc/civics_teacher.png", fit="contain", xysize=(640, 960))
image track_coach neut = Transform("assets/characters/npc/track_coach.png", fit="contain", xysize=(640, 960))

# PLACEHOLDER ART: these six still share the generic placeholder sprite.
image science_teacher neut = Transform("assets/characters/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image japanese_teacher neut = Transform("assets/characters/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image english_teacher neut = Transform("assets/characters/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image hikari neut = Transform("assets/characters/npc/hikari.png", fit="contain", xysize=(640, 960))
image homura neut = Transform("assets/characters/npc/homura.png", fit="contain", xysize=(640, 960))
# One scene, one asking, gone forever -- ooc_0604_out_of_ten. He is not written
# as a joke and he is not coming back; the sprite is placeholder because he does
# not warrant art, not because he does not warrant a name.
image daichi neut = Transform("assets/characters/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))

define math_teacher = Character("Teacher", image="math_teacher", **SAY_STYLE)
define civics_teacher = Character("Teacher", image="civics_teacher", **SAY_STYLE)
define science_teacher = Character("Teacher", image="science_teacher", **SAY_STYLE)
define japanese_teacher = Character("Teacher", image="japanese_teacher", **SAY_STYLE)
define english_teacher = Character("Teacher", image="english_teacher", **SAY_STYLE)
define track_coach = Character("Coach", image="track_coach", **SAY_STYLE)
define hikari = Character("Hikari", image="hikari", **SAY_STYLE)
define homura = Character("Homura", image="homura", **SAY_STYLE)
define dai = Character("Daichi", image="daichi", **SAY_STYLE)

# VOICE-ONLY incidentals -- no sprite, no roster entry, because the story never
# puts them on screen. They exist so a line that is plainly SOMEONE talking gets a
# namebox instead of being typed as an escaped-quote narrator line, where it reads
# as MC's inner voice.
#   principal -- the May 24 pep assembly, heard over the gym PA from the front of
#                the room. Role name, matching Teacher / Coach.
#   teacher   -- any unnamed teacher with a single crowd-control line. The five
#                teachers above are each tied to a subject AND a sprite, so none
#                of them fits a hallway or a gym doorway.
define principal = Character("Principal", **SAY_STYLE)
define teacher = Character("Teacher", **SAY_STYLE)

define npc1 = Character("NPC 1", **SAY_STYLE)
define npc2 = Character("NPC 2", **SAY_STYLE)


# -----------------------------------------------------------------------------
# Side-story cast sprites (no Character of their own; the owning story speaks
# for them). Fire Emblem bit players from Matsuda's "Dead Fantasy".
# -----------------------------------------------------------------------------

image gary = Transform("assets/characters/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image gregor = Transform("assets/characters/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image leif = Transform("assets/characters/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))

# Purgatorium (Sam's character story).
image purg_girl = Transform("assets/extra_sprites/purg_girl.png", fit="contain", xysize=(640, 960))
image purg_girl_day7 = Transform("assets/extra_sprites/purg_girl_day7.png", fit="contain", xysize=(640, 960))
image purg_girl_yukata = Transform("assets/extra_sprites/purg_girl_yukata.png", fit="contain", xysize=(640, 960))


# -----------------------------------------------------------------------------
# THE SPRITE-TAG ROSTER
# Every image tag above that is a CHARACTER standing in a scene (as opposed to a
# background, CG or UI image). The Autofocus addon registers a default rest
# transform for each of these at init 999, so a bare `show <tag>` still lands in
# a tracked slot; it used to keep its own hand-copied list, which silently went
# stale every time a sprite was added here (the four Dead Fantasy / Purgatorium
# sprites below were never in it).
#
# ADDING A SPRITE: add its tag here in the same edit that adds its `image` line.
# init 999 is when Autofocus reads this, so plain init order is fine.
# -----------------------------------------------------------------------------
init python:
    ENTER_M_SPRITE_TAGS = (
        # DDLC layeredimages (game/assets/mpt/)
        "monika", "sayori", "natsuki", "yuri",
        # Named cast
        "matsuda", "tsubaki", "asahina", "sam", "kotonoha", "mom", "mc",
        # NPCs
        "math_teacher", "civics_teacher", "science_teacher", "japanese_teacher",
        "english_teacher", "track_coach", "hikari", "homura", "daichi",
        # Side-story bit players
        "gary", "gregor", "leif",
        "purg_girl", "purg_girl_day7", "purg_girl_yukata",
    )
