# ENTER M cast sprites, speakers, and display names.
# DynamicCharacter names use the matching default <alias>_name variable.
# Monika, MC, and narrator keep their shared definitions in definitions.rpy.

init -1 python:
    # Spoken dialogue uses quote marks and a fixed click-to-continue caret.
    SAY_STYLE = dict(what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")


# -----------------------------------------------------------------------------
# Named cast -- renameable at runtime
# -----------------------------------------------------------------------------

# Outfit and pose transforms below preserve each character's registered scale.

transform matsuda_sprite_size:
    fit "contain"
    ysize 960


# Matsuda's repainted outfit bases share head scale and position. Each complete
# expression plate is registered to its outfit's face; changing expression
# cannot move the body. Pose canvases may widen, but source height stays 1537.
# Height-only sizing preserves anatomical scale when a gesture needs more room.
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

# Matsuda's four reactions each support both outfits. Standalone images keep
# moving arms and hair separate from the neutral body's expression layers.
# All assets use the same anatomical scale; width never controls their zoom.
image matsuda casual pose_facepalm = Transform("assets/characters/matsuda/pose_facepalm_casual.png", fit="contain", ysize=960)
image matsuda casual pose_chuuni = Transform("assets/characters/matsuda/pose_chuuni_casual.png", fit="contain", ysize=960)
image matsuda casual pose_shrug = Transform("assets/characters/matsuda/pose_shrug_casual.png", fit="contain", ysize=960)
image matsuda casual pose_laughing = Transform("assets/characters/matsuda/pose_laughing_casual.png", fit="contain", ysize=960)
image matsuda uniform pose_facepalm = Transform("assets/characters/matsuda/pose_facepalm_uniform.png", fit="contain", ysize=960)
image matsuda uniform pose_chuuni = Transform("assets/characters/matsuda/pose_chuuni_uniform.png", fit="contain", ysize=960)
image matsuda uniform pose_shrug = Transform("assets/characters/matsuda/pose_shrug_uniform.png", fit="contain", ysize=960)
image matsuda uniform pose_laughing = Transform("assets/characters/matsuda/pose_laughing_uniform.png", fit="contain", ysize=960)

transform tsubaki_sprite_size:
    fit "contain"
    xysize (640, 960)


# Tsubaki's outfit-native neutral sprites are fixed bases for her expression
# bank. Like Himeko and Asahina, each alternate is one broad, independently
# registered face plate that owns the bangs, brows, eyes, and mouth together.
# Changing expressions therefore cannot expose a second neutral-base eyebrow
# or move/crop her body.
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
# Register the skirt-waist anchor while retaining deliberate head pitch and
# torso compression. Vertex offsets preserve every source pixel and the shared
# nominal frame used by stage slots and the Sprite Viewer; no PNG is cropped.
image asahina uniform pose_hairflip = Transform("assets/characters/asahina/pose_hairflip_uniform.png", fit="contain", xysize=(640, 960), matrixtransform=OffsetMatrix(0, 18 * 960.0 / 1537.0, 0))
image asahina uniform pose_pointing = Transform("assets/characters/asahina/pose_pointing_uniform.png", fit="contain", xysize=(640, 960), matrixtransform=OffsetMatrix(0, 32 * 960.0 / 1537.0, 0))
image asahina uniform pose_eyeroll = Transform("assets/characters/asahina/pose_eyeroll_uniform.png", fit="contain", xysize=(640, 960), matrixtransform=OffsetMatrix(0, 25 * 960.0 / 1537.0, 0))
image asahina uniform pose_phone_panic = Transform("assets/characters/asahina/pose_phone_panic_uniform.png", fit="contain", xysize=(640, 960), matrixtransform=OffsetMatrix(0, 42 * 960.0 / 1537.0, 0))
image asahina uniform terror = Transform("assets/characters/asahina/pose_phone_panic_uniform.png", fit="contain", xysize=(640, 960), matrixtransform=OffsetMatrix(0, 42 * 960.0 / 1537.0, 0)) # unique sprite on 10/30 where she receives a bone-chilling text from mom to come home IMMEDIATELY after school and that she has some explaining to do

transform sam_sprite_size:
    fit "contain"
    xysize (640, 960)


# Each Sam expression is registered to its own intact outfit base.
# The show sam [outfit] [expression] API is unchanged.
layeredimage sam:
    at sam_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "assets/characters/masayami/neutral.png"
        attribute uniform:
            "assets/characters/masayami/neut_uniform.png"

    group face:
        attribute neut default if_all "casual":
            "assets/characters/masayami/face_neut_casual.png"
        attribute neut if_all "uniform":
            "assets/characters/masayami/face_neut_uniform.png"
        attribute happy if_all "casual":
            "assets/characters/masayami/face_happy_casual.png"
        attribute happy if_all "uniform":
            "assets/characters/masayami/face_happy_uniform.png"
        attribute smug if_all "casual":
            "assets/characters/masayami/face_smug_casual.png"
        attribute smug if_all "uniform":
            "assets/characters/masayami/face_smug_uniform.png"
        attribute teasing if_all "casual":
            "assets/characters/masayami/face_teasing_casual.png"
        attribute teasing if_all "uniform":
            "assets/characters/masayami/face_teasing_uniform.png"
        attribute thinking if_all "casual":
            "assets/characters/masayami/face_thinking_casual.png"
        attribute thinking if_all "uniform":
            "assets/characters/masayami/face_thinking_uniform.png"
        attribute curious if_all "casual":
            "assets/characters/masayami/face_curious_casual.png"
        attribute curious if_all "uniform":
            "assets/characters/masayami/face_curious_uniform.png"
        attribute unamused if_all "casual":
            "assets/characters/masayami/face_unamused_casual.png"
        attribute unamused if_all "uniform":
            "assets/characters/masayami/face_unamused_uniform.png"
        attribute annoyed if_all "casual":
            "assets/characters/masayami/face_annoyed_casual.png"
        attribute annoyed if_all "uniform":
            "assets/characters/masayami/face_annoyed_uniform.png"
        attribute frustrated if_all "casual":
            "assets/characters/masayami/face_frustrated_casual.png"
        attribute frustrated if_all "uniform":
            "assets/characters/masayami/face_frustrated_uniform.png"
        attribute angry if_all "casual":
            "assets/characters/masayami/face_angry_casual.png"
        attribute angry if_all "uniform":
            "assets/characters/masayami/face_angry_uniform.png"
        attribute sad if_all "casual":
            "assets/characters/masayami/face_sad_casual.png"
        attribute sad if_all "uniform":
            "assets/characters/masayami/face_sad_uniform.png"
        attribute crying if_all "casual":
            "assets/characters/masayami/face_crying_casual.png"
        attribute crying if_all "uniform":
            "assets/characters/masayami/face_crying_uniform.png"
        attribute embarrassed if_all "casual":
            "assets/characters/masayami/face_embarrassed_casual.png"
        attribute embarrassed if_all "uniform":
            "assets/characters/masayami/face_embarrassed_uniform.png"
        attribute nervous if_all "casual":
            "assets/characters/masayami/face_nervous_casual.png"
        attribute nervous if_all "uniform":
            "assets/characters/masayami/face_nervous_uniform.png"
        attribute worried if_all "casual":
            "assets/characters/masayami/face_worried_casual.png"
        attribute worried if_all "uniform":
            "assets/characters/masayami/face_worried_uniform.png"
        attribute shocked if_all "casual":
            "assets/characters/masayami/face_shocked_casual.png"
        attribute shocked if_all "uniform":
            "assets/characters/masayami/face_shocked_uniform.png"
        attribute afraid if_all "casual":
            "assets/characters/masayami/face_afraid_casual.png"
        attribute afraid if_all "uniform":
            "assets/characters/masayami/face_afraid_uniform.png"
        attribute panicked if_all "casual":
            "assets/characters/masayami/face_panicked_casual.png"
        attribute panicked if_all "uniform":
            "assets/characters/masayami/face_panicked_uniform.png"
        attribute determined if_all "casual":
            "assets/characters/masayami/face_determined_casual.png"
        attribute determined if_all "uniform":
            "assets/characters/masayami/face_determined_uniform.png"
        attribute empty if_all "casual":
            "assets/characters/masayami/face_empty_casual.png"
        attribute empty if_all "uniform":
            "assets/characters/masayami/face_empty_uniform.png"
        attribute disgusted if_all "casual":
            "assets/characters/masayami/face_disgusted_casual.png"
        attribute disgusted if_all "uniform":
            "assets/characters/masayami/face_disgusted_uniform.png"

# These full-body reactions have fixed outfits and silhouettes, so they stay
# outside the layered image instead of inheriting its default torso and face.
image sam casual pose_open_hand = Transform("assets/characters/masayami/pose_open_hand_casual.png", fit="contain", xysize=(640, 960))
image sam uniform pose_crossed = Transform("assets/characters/masayami/pose_crossed_uniform.png", fit="contain", xysize=(640, 960))
# These two masters were underscaled by the historical crown-to-canvas-bottom
# registration. Scale the retained art about the reviewed crown/body anchor;
# the nominal stage frame and full source canvas remain unchanged.
image sam uniform pose_thinking = Transform("assets/characters/masayami/pose_thinking_uniform.png", fit="contain", xysize=(640, 960), matrixanchor=(380.0 / 1023.0, 31.0 / 1537.0), matrixtransform=ScaleMatrix(1.12, 1.12, 1.0))
image sam casual pose_phone = Transform("assets/characters/masayami/pose_phone_casual.png", fit="contain", xysize=(640, 960), matrixanchor=(380.0 / 1023.0, 31.0 / 1537.0), matrixtransform=ScaleMatrix(1.18, 1.18, 1.0))

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


# Himeko uses an expression bank registered to each outfit's own neutral head.
# Hair, ears, jaw and neck retain the original base; acting features, blush and
# liquid accents remain expression-owned. The builder replays the reviewed
# registration/color repair after extracting the original generated masters.
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
        attribute happy if_all "casual":
            "assets/characters/himeko/face_happy.png"
        attribute happy if_all "uniform":
            "assets/characters/himeko/face_happy_uniform.png"
        attribute smug if_all "casual":
            "assets/characters/himeko/face_smug.png"
        attribute smug if_all "uniform":
            "assets/characters/himeko/face_smug_uniform.png"
        attribute teasing if_all "casual":
            "assets/characters/himeko/face_teasing.png"
        attribute teasing if_all "uniform":
            "assets/characters/himeko/face_teasing_uniform.png"
        attribute thinking if_all "casual":
            "assets/characters/himeko/face_thinking.png"
        attribute thinking if_all "uniform":
            "assets/characters/himeko/face_thinking_uniform.png"
        attribute curious if_all "casual":
            "assets/characters/himeko/face_curious.png"
        attribute curious if_all "uniform":
            "assets/characters/himeko/face_curious_uniform.png"
        attribute unamused if_all "casual":
            "assets/characters/himeko/face_unamused.png"
        attribute unamused if_all "uniform":
            "assets/characters/himeko/face_unamused_uniform.png"
        attribute annoyed if_all "casual":
            "assets/characters/himeko/face_annoyed.png"
        attribute annoyed if_all "uniform":
            "assets/characters/himeko/face_annoyed_uniform.png"
        attribute frustrated if_all "casual":
            "assets/characters/himeko/face_frustrated.png"
        attribute frustrated if_all "uniform":
            "assets/characters/himeko/face_frustrated_uniform.png"
        attribute angry if_all "casual":
            "assets/characters/himeko/face_angry.png"
        attribute angry if_all "uniform":
            "assets/characters/himeko/face_angry_uniform.png"
        attribute sad if_all "casual":
            "assets/characters/himeko/face_sad.png"
        attribute sad if_all "uniform":
            "assets/characters/himeko/face_sad_uniform.png"
        attribute crying if_all "casual":
            "assets/characters/himeko/face_crying.png"
        attribute crying if_all "uniform":
            "assets/characters/himeko/face_crying_uniform.png"
        attribute embarrassed if_all "casual":
            "assets/characters/himeko/face_embarrassed.png"
        attribute embarrassed if_all "uniform":
            "assets/characters/himeko/face_embarrassed_uniform.png"
        attribute nervous if_all "casual":
            "assets/characters/himeko/face_nervous.png"
        attribute nervous if_all "uniform":
            "assets/characters/himeko/face_nervous_uniform.png"
        attribute worried if_all "casual":
            "assets/characters/himeko/face_worried.png"
        attribute worried if_all "uniform":
            "assets/characters/himeko/face_worried_uniform.png"
        attribute shocked if_all "casual":
            "assets/characters/himeko/face_shocked.png"
        attribute shocked if_all "uniform":
            "assets/characters/himeko/face_shocked_uniform.png"
        attribute afraid if_all "casual":
            "assets/characters/himeko/face_afraid.png"
        attribute afraid if_all "uniform":
            "assets/characters/himeko/face_afraid_uniform.png"
        attribute panicked if_all "casual":
            "assets/characters/himeko/face_panicked.png"
        attribute panicked if_all "uniform":
            "assets/characters/himeko/face_panicked_uniform.png"
        attribute determined if_all "casual":
            "assets/characters/himeko/face_determined.png"
        attribute determined if_all "uniform":
            "assets/characters/himeko/face_determined_uniform.png"
        attribute empty if_all "casual":
            "assets/characters/himeko/face_empty.png"
        attribute empty if_all "uniform":
            "assets/characters/himeko/face_empty_uniform.png"
        attribute disgusted if_all "casual":
            "assets/characters/himeko/face_disgusted.png"
        attribute disgusted if_all "uniform":
            "assets/characters/himeko/face_disgusted_uniform.png"

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
# Incidental cast -- fixed names
# -----------------------------------------------------------------------------

image math_teacher neut = Transform("assets/characters/npc/math_teacher.png", fit="contain", xysize=(640, 960))
image civics_teacher neut = Transform("assets/characters/npc/civics_teacher.png", fit="contain", xysize=(640, 960))
image track_coach neut = Transform("assets/characters/npc/track_coach.png", fit="contain", xysize=(640, 960))

image science_teacher neut = Transform("assets/characters/npc/science_teacher.png", fit="contain", xysize=(640, 960))
image japanese_teacher neut = Transform("assets/characters/npc/japanese_teacher.png", fit="contain", xysize=(640, 960))
image english_teacher neut = Transform("assets/characters/npc/english_teacher.png", fit="contain", xysize=(640, 960))
image hikari neut = Transform("assets/characters/npc/hikari.png", fit="contain", xysize=(640, 960))
image homura neut = Transform("assets/characters/npc/homura.png", fit="contain", xysize=(640, 960))
# Compact expression sets for the club members; original neutral art stays intact.
image hikari angry = Transform("assets/characters/npc/hikari/angry.png", fit="contain", xysize=(640, 960))
image hikari unamused = Transform("assets/characters/npc/hikari/unamused.png", fit="contain", xysize=(640, 960))
image hikari curious = Transform("assets/characters/npc/hikari/curious.png", fit="contain", xysize=(640, 960))
image hikari sad = Transform("assets/characters/npc/hikari/sad.png", fit="contain", xysize=(640, 960))
image hikari determined = Transform("assets/characters/npc/hikari/determined.png", fit="contain", xysize=(640, 960))
image homura frustrated = Transform("assets/characters/npc/homura/frustrated.png", fit="contain", xysize=(640, 960))
image homura nervous = Transform("assets/characters/npc/homura/nervous.png", fit="contain", xysize=(640, 960))
image homura embarrassed = Transform("assets/characters/npc/homura/embarrassed.png", fit="contain", xysize=(640, 960))
image homura thinking = Transform("assets/characters/npc/homura/thinking.png", fit="contain", xysize=(640, 960))
image homura teasing = Transform("assets/characters/npc/homura/teasing.png", fit="contain", xysize=(640, 960))
image charlie neut = Transform("assets/characters/npc/charlie.png", fit="contain", xysize=(630, 945))
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
define charlie = Character("Charlie", image="charlie", **SAY_STYLE)
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
# for them). Original fantasy cast from Matsuda's "Dead Fantasy". Each tag has
# one purpose-built battlefield portrait; expression attributes should only be
# added when a visually distinct portrait actually exists.
# -----------------------------------------------------------------------------

transform dead_fantasy_sprite_size:
    # The source paintings are full-body, while ENTER M's regular sprites are
    # framed around the thighs. Enlarge and lower the complete canvas instead
    # of cropping it: two-person slots retain every cape, weapon and strand of
    # hair, while the dialogue window supplies the natural lower-frame cutoff.
    fit "contain"
    xysize (640, 960)
    zoom 1.25
    yoffset 300

image df_akai = At("assets/extra_sprites/dead_fantasy/akai.png", dead_fantasy_sprite_size)
image df_rival = At("assets/extra_sprites/dead_fantasy/rival.png", dead_fantasy_sprite_size)
image df_sam = At("assets/extra_sprites/dead_fantasy/sam_clean.png", dead_fantasy_sprite_size)
image df_tsubaki = At("assets/extra_sprites/dead_fantasy/tsubaki.png", dead_fantasy_sprite_size)
image gary = At("assets/extra_sprites/dead_fantasy/gary.png", dead_fantasy_sprite_size)
image gregor = At("assets/extra_sprites/dead_fantasy/gregor.png", dead_fantasy_sprite_size)
image leif = At("assets/extra_sprites/dead_fantasy/leif.png", dead_fantasy_sprite_size)

# Purgatorium (Sam's character story).
image purg_girl = Transform("assets/extra_sprites/purg_girl.png", fit="contain", xysize=(640, 960))
image purg_girl_day7 = Transform("assets/extra_sprites/purg_girl_day7.png", fit="contain", xysize=(640, 960))
image purg_girl_yukata = Transform("assets/extra_sprites/purg_girl_yukata.png", fit="contain", xysize=(640, 960))


# Character tags used by Autofocus at init 999 for default stage placement.
# Add a tag here when introducing a character image family.
init python:
    ENTER_M_SPRITE_TAGS = (
        # Monika uses the Mood Posing Tool layeredimage.
        "monika",
        # Named cast
        "matsuda", "tsubaki", "asahina", "sam", "kotonoha", "mom", "mc",
        # NPCs
        "math_teacher", "civics_teacher", "science_teacher", "japanese_teacher",
        "english_teacher", "track_coach", "hikari", "homura", "charlie", "daichi",
        # Side-story bit players
        "df_akai", "df_rival", "df_sam", "df_tsubaki",
        "gary", "gregor", "leif",
        "purg_girl", "purg_girl_day7", "purg_girl_yukata",
    )
