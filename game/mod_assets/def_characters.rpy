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
#   image <tag> neut = Transform("mod_assets/char_sprites/<folder>/neutral.png",
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
# Authoring tokens mirror docs/TODO.txt; Neutral stays `neut` for compatibility,
# and Empty/Dead-eyed is the `empty` attribute.
layeredimage matsuda:
    at matsuda_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "mod_assets/char_sprites/matsuda/neutral.png"
        attribute uniform:
            "mod_assets/char_sprites/matsuda/neut_uniform.png"

    group face:
        attribute neut default if_all "casual":
            "mod_assets/char_sprites/matsuda/face_neut_casual.png"
        attribute neut if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_neut_uniform.png"
        attribute happy if_all "casual":
            "mod_assets/char_sprites/matsuda/face_happy_casual.png"
        attribute happy if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_happy_uniform.png"
        attribute smug if_all "casual":
            "mod_assets/char_sprites/matsuda/face_smug_casual.png"
        attribute smug if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_smug_uniform.png"
        attribute teasing if_all "casual":
            "mod_assets/char_sprites/matsuda/face_teasing_casual.png"
        attribute teasing if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_teasing_uniform.png"
        attribute thinking if_all "casual":
            "mod_assets/char_sprites/matsuda/face_thinking_casual.png"
        attribute thinking if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_thinking_uniform.png"
        attribute curious if_all "casual":
            "mod_assets/char_sprites/matsuda/face_curious_casual.png"
        attribute curious if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_curious_uniform.png"
        attribute unamused if_all "casual":
            "mod_assets/char_sprites/matsuda/face_unamused_casual.png"
        attribute unamused if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_unamused_uniform.png"
        attribute annoyed if_all "casual":
            "mod_assets/char_sprites/matsuda/face_annoyed_casual.png"
        attribute annoyed if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_annoyed_uniform.png"
        attribute frustrated if_all "casual":
            "mod_assets/char_sprites/matsuda/face_frustrated_casual.png"
        attribute frustrated if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_frustrated_uniform.png"
        attribute angry if_all "casual":
            "mod_assets/char_sprites/matsuda/face_angry_casual.png"
        attribute angry if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_angry_uniform.png"
        attribute sad if_all "casual":
            "mod_assets/char_sprites/matsuda/face_sad_casual.png"
        attribute sad if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_sad_uniform.png"
        attribute crying if_all "casual":
            "mod_assets/char_sprites/matsuda/face_crying_casual.png"
        attribute crying if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_crying_uniform.png"
        attribute embarrassed if_all "casual":
            "mod_assets/char_sprites/matsuda/face_embarrassed_casual.png"
        attribute embarrassed if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_embarrassed_uniform.png"
        attribute nervous if_all "casual":
            "mod_assets/char_sprites/matsuda/face_nervous_casual.png"
        attribute nervous if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_nervous_uniform.png"
        attribute worried if_all "casual":
            "mod_assets/char_sprites/matsuda/face_worried_casual.png"
        attribute worried if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_worried_uniform.png"
        attribute shocked if_all "casual":
            "mod_assets/char_sprites/matsuda/face_shocked_casual.png"
        attribute shocked if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_shocked_uniform.png"
        attribute afraid if_all "casual":
            "mod_assets/char_sprites/matsuda/face_afraid_casual.png"
        attribute afraid if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_afraid_uniform.png"
        attribute panicked if_all "casual":
            "mod_assets/char_sprites/matsuda/face_panicked_casual.png"
        attribute panicked if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_panicked_uniform.png"
        attribute determined if_all "casual":
            "mod_assets/char_sprites/matsuda/face_determined_casual.png"
        attribute determined if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_determined_uniform.png"
        attribute empty if_all "casual":
            "mod_assets/char_sprites/matsuda/face_empty_casual.png"
        attribute empty if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_empty_uniform.png"
        attribute disgusted if_all "casual":
            "mod_assets/char_sprites/matsuda/face_disgusted_casual.png"
        attribute disgusted if_all "uniform":
            "mod_assets/char_sprites/matsuda/face_disgusted_uniform.png"

# These four full-body reactions use five files because laughing supports both
# outfits. Each pose has a fixed face, outfit, and silhouette.
# Keeping them outside the layered image prevents its default torso and face
# from appearing behind poses that move Matsuda's arms and hair.
image matsuda uniform pose_facepalm = Transform("mod_assets/char_sprites/matsuda/pose_facepalm_uniform.png", fit="contain", xysize=(640, 960))
image matsuda uniform pose_chuuni = Transform("mod_assets/char_sprites/matsuda/pose_chuuni_uniform.png", fit="contain", xysize=(640, 960))
image matsuda uniform pose_shrug = Transform("mod_assets/char_sprites/matsuda/pose_shrug_uniform.png", fit="contain", xysize=(640, 960))
image matsuda casual pose_laughing = Transform("mod_assets/char_sprites/matsuda/pose_laughing_casual.png", fit="contain", xysize=(640, 960))
image matsuda uniform pose_laughing = Transform("mod_assets/char_sprites/matsuda/pose_laughing_uniform.png", fit="contain", xysize=(640, 960))

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
            "mod_assets/char_sprites/tsubaki/neutral.png"
        attribute uniform:
            "mod_assets/char_sprites/tsubaki/neut_uniform.png"

    group face:
        attribute neut default if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_neut_casual.png"
        attribute neut if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_neut_uniform.png"
        attribute happy if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_happy_casual.png"
        attribute happy if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_happy_uniform.png"
        attribute smug if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_smug_casual.png"
        attribute smug if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_smug_uniform.png"
        attribute teasing if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_teasing_casual.png"
        attribute teasing if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_teasing_uniform.png"
        attribute thinking if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_thinking_casual.png"
        attribute thinking if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_thinking_uniform.png"
        attribute curious if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_curious_casual.png"
        attribute curious if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_curious_uniform.png"
        attribute unamused if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_unamused_casual.png"
        attribute unamused if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_unamused_uniform.png"
        attribute annoyed if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_annoyed_casual.png"
        attribute annoyed if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_annoyed_uniform.png"
        attribute frustrated if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_frustrated_casual.png"
        attribute frustrated if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_frustrated_uniform.png"
        attribute angry if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_angry_casual.png"
        attribute angry if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_angry_uniform.png"
        attribute sad if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_sad_casual.png"
        attribute sad if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_sad_uniform.png"
        attribute crying if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_crying_casual.png"
        attribute crying if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_crying_uniform.png"
        attribute embarrassed if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_embarrassed_casual.png"
        attribute embarrassed if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_embarrassed_uniform.png"
        attribute nervous if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_nervous_casual.png"
        attribute nervous if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_nervous_uniform.png"
        attribute worried if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_worried_casual.png"
        attribute worried if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_worried_uniform.png"
        attribute shocked if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_shocked_casual.png"
        attribute shocked if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_shocked_uniform.png"
        attribute afraid if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_afraid_casual.png"
        attribute afraid if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_afraid_uniform.png"
        attribute panicked if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_panicked_casual.png"
        attribute panicked if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_panicked_uniform.png"
        attribute determined if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_determined_casual.png"
        attribute determined if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_determined_uniform.png"
        attribute empty if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_empty_casual.png"
        attribute empty if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_empty_uniform.png"
        attribute disgusted if_all "casual":
            "mod_assets/char_sprites/tsubaki/face_disgusted_casual.png"
        attribute disgusted if_all "uniform":
            "mod_assets/char_sprites/tsubaki/face_disgusted_uniform.png"

image tsubaki post_neut = Transform("mod_assets/char_sprites/tsubaki/post_neut.png", fit="contain", xysize=(640, 960)) # her "metamorphosis" transformation
image tsubaki post_revelation = Transform("mod_assets/char_sprites/tsubaki/post_rev.png", fit="contain", xysize=(640, 960)) # same as above, but with a psychotic expression, like she had a revelation

transform asahina_sprite_size:
    fit "contain"
    xysize (640, 960)


# Asahina's registered expression bank is shared across both original outfits.
# Each outfit has a native featureless face base and an exact neutral layer;
# alternate layers contain only aligned eyes, brows, mouths, tears, and blush.
# This keeps the hair, nose, jaw, silhouette, color, and stage placement fixed.
layeredimage asahina:
    at asahina_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "mod_assets/char_sprites/asahina/neut_face_base.png"
        attribute uniform:
            "mod_assets/char_sprites/asahina/neut_uniform_face_base.png"

    group face:
        attribute neut default if_all "casual":
            "mod_assets/char_sprites/asahina/face_neut_casual.png"
        attribute neut if_all "uniform":
            "mod_assets/char_sprites/asahina/face_neut_uniform.png"
        attribute happy:
            "mod_assets/char_sprites/asahina/face_happy.png"
        attribute smug:
            "mod_assets/char_sprites/asahina/face_smug.png"
        attribute teasing:
            "mod_assets/char_sprites/asahina/face_teasing.png"
        attribute thinking:
            "mod_assets/char_sprites/asahina/face_thinking.png"
        attribute curious:
            "mod_assets/char_sprites/asahina/face_curious.png"
        attribute unamused:
            "mod_assets/char_sprites/asahina/face_unamused.png"
        attribute annoyed:
            "mod_assets/char_sprites/asahina/face_annoyed.png"
        attribute frustrated:
            "mod_assets/char_sprites/asahina/face_frustrated.png"
        attribute angry:
            "mod_assets/char_sprites/asahina/face_angry.png"
        attribute sad:
            "mod_assets/char_sprites/asahina/face_sad.png"
        attribute crying:
            "mod_assets/char_sprites/asahina/face_crying.png"
        attribute embarrassed:
            "mod_assets/char_sprites/asahina/face_embarrassed.png"
        attribute nervous:
            "mod_assets/char_sprites/asahina/face_nervous.png"
        attribute worried:
            "mod_assets/char_sprites/asahina/face_worried.png"
        attribute shocked:
            "mod_assets/char_sprites/asahina/face_shocked.png"
        attribute afraid:
            "mod_assets/char_sprites/asahina/face_afraid.png"
        attribute panicked:
            "mod_assets/char_sprites/asahina/face_panicked.png"
        attribute determined:
            "mod_assets/char_sprites/asahina/face_determined.png"
        attribute empty:
            "mod_assets/char_sprites/asahina/face_empty.png"
        attribute disgusted:
            "mod_assets/char_sprites/asahina/face_disgusted.png"

# Full-body reactions stay outside the layered image because their arms, hair,
# and head angles change. `terror` remains available for existing story calls;
# `pose_phone_panic` exposes the same art under the descriptive pose vocabulary.
image asahina uniform pose_hairflip = Transform("mod_assets/char_sprites/asahina/pose_hairflip_uniform.png", fit="contain", xysize=(640, 960))
image asahina uniform pose_pointing = Transform("mod_assets/char_sprites/asahina/pose_pointing_uniform.png", fit="contain", xysize=(640, 960))
image asahina uniform pose_eyeroll = Transform("mod_assets/char_sprites/asahina/pose_eyeroll_uniform.png", fit="contain", xysize=(640, 960))
image asahina uniform pose_phone_panic = Transform("mod_assets/char_sprites/asahina/terror.png", fit="contain", xysize=(640, 960))
image asahina uniform terror = Transform("mod_assets/char_sprites/asahina/terror.png", fit="contain", xysize=(640, 960)) # unique sprite on 10/30 where she receives a bone-chilling text from mom to come home IMMEDIATELY after school and that she has some explaining to do

transform sam_sprite_size:
    fit "contain"
    xysize (640, 960)


# Sam's two original outfits use outfit-native featureless bases and registered
# expression layers. Neutral reconstructs each source sprite exactly; alternate
# layers contain only the brows, eyes, mouth, tears, and controlled blush, so
# the hair, face outline, and full-body placement remain fixed. Empty/Dead-eyed
# uses the `empty` attribute, matching the rest of the cast's expression bank.
layeredimage sam:
    at sam_sprite_size, Flatten

    group outfit:
        attribute casual default:
            "mod_assets/char_sprites/masayami/neut_face_base.png"
        attribute uniform:
            "mod_assets/char_sprites/masayami/neut_uniform_face_base.png"

    group face:
        attribute neut default if_all "casual":
            "mod_assets/char_sprites/masayami/face_neut_casual.png"
        attribute neut if_all "uniform":
            "mod_assets/char_sprites/masayami/face_neut_uniform.png"
        attribute happy if_all "casual":
            "mod_assets/char_sprites/masayami/face_happy_casual.png"
        attribute happy if_all "uniform":
            "mod_assets/char_sprites/masayami/face_happy_uniform.png"
        attribute smug if_all "casual":
            "mod_assets/char_sprites/masayami/face_smug_casual.png"
        attribute smug if_all "uniform":
            "mod_assets/char_sprites/masayami/face_smug_uniform.png"
        attribute teasing if_all "casual":
            "mod_assets/char_sprites/masayami/face_teasing_casual.png"
        attribute teasing if_all "uniform":
            "mod_assets/char_sprites/masayami/face_teasing_uniform.png"
        attribute thinking if_all "casual":
            "mod_assets/char_sprites/masayami/face_thinking_casual.png"
        attribute thinking if_all "uniform":
            "mod_assets/char_sprites/masayami/face_thinking_uniform.png"
        attribute curious if_all "casual":
            "mod_assets/char_sprites/masayami/face_curious_casual.png"
        attribute curious if_all "uniform":
            "mod_assets/char_sprites/masayami/face_curious_uniform.png"
        attribute unamused if_all "casual":
            "mod_assets/char_sprites/masayami/face_unamused_casual.png"
        attribute unamused if_all "uniform":
            "mod_assets/char_sprites/masayami/face_unamused_uniform.png"
        attribute annoyed if_all "casual":
            "mod_assets/char_sprites/masayami/face_annoyed_casual.png"
        attribute annoyed if_all "uniform":
            "mod_assets/char_sprites/masayami/face_annoyed_uniform.png"
        attribute frustrated if_all "casual":
            "mod_assets/char_sprites/masayami/face_frustrated_casual.png"
        attribute frustrated if_all "uniform":
            "mod_assets/char_sprites/masayami/face_frustrated_uniform.png"
        attribute angry if_all "casual":
            "mod_assets/char_sprites/masayami/face_angry_casual.png"
        attribute angry if_all "uniform":
            "mod_assets/char_sprites/masayami/face_angry_uniform.png"
        attribute sad if_all "casual":
            "mod_assets/char_sprites/masayami/face_sad_casual.png"
        attribute sad if_all "uniform":
            "mod_assets/char_sprites/masayami/face_sad_uniform.png"
        attribute crying if_all "casual":
            "mod_assets/char_sprites/masayami/face_crying_casual.png"
        attribute crying if_all "uniform":
            "mod_assets/char_sprites/masayami/face_crying_uniform.png"
        attribute embarrassed if_all "casual":
            "mod_assets/char_sprites/masayami/face_embarrassed_casual.png"
        attribute embarrassed if_all "uniform":
            "mod_assets/char_sprites/masayami/face_embarrassed_uniform.png"
        attribute nervous if_all "casual":
            "mod_assets/char_sprites/masayami/face_nervous_casual.png"
        attribute nervous if_all "uniform":
            "mod_assets/char_sprites/masayami/face_nervous_uniform.png"
        attribute worried if_all "casual":
            "mod_assets/char_sprites/masayami/face_worried_casual.png"
        attribute worried if_all "uniform":
            "mod_assets/char_sprites/masayami/face_worried_uniform.png"
        attribute shocked if_all "casual":
            "mod_assets/char_sprites/masayami/face_shocked_casual.png"
        attribute shocked if_all "uniform":
            "mod_assets/char_sprites/masayami/face_shocked_uniform.png"
        attribute afraid if_all "casual":
            "mod_assets/char_sprites/masayami/face_afraid_casual.png"
        attribute afraid if_all "uniform":
            "mod_assets/char_sprites/masayami/face_afraid_uniform.png"
        attribute panicked if_all "casual":
            "mod_assets/char_sprites/masayami/face_panicked_casual.png"
        attribute panicked if_all "uniform":
            "mod_assets/char_sprites/masayami/face_panicked_uniform.png"
        attribute determined if_all "casual":
            "mod_assets/char_sprites/masayami/face_determined_casual.png"
        attribute determined if_all "uniform":
            "mod_assets/char_sprites/masayami/face_determined_uniform.png"
        attribute empty if_all "casual":
            "mod_assets/char_sprites/masayami/face_empty_casual.png"
        attribute empty if_all "uniform":
            "mod_assets/char_sprites/masayami/face_empty_uniform.png"
        attribute disgusted if_all "casual":
            "mod_assets/char_sprites/masayami/face_disgusted_casual.png"
        attribute disgusted if_all "uniform":
            "mod_assets/char_sprites/masayami/face_disgusted_uniform.png"

# These full-body reactions have fixed outfits and silhouettes, so they stay
# outside the layered image instead of inheriting its default torso and face.
image sam casual pose_open_hand = Transform("mod_assets/char_sprites/masayami/pose_open_hand_casual.png", fit="contain", xysize=(640, 960))
image sam uniform pose_crossed = Transform("mod_assets/char_sprites/masayami/pose_crossed_uniform.png", fit="contain", xysize=(640, 960))
image sam uniform pose_thinking = Transform("mod_assets/char_sprites/masayami/pose_thinking_uniform.png", fit="contain", xysize=(640, 960))
image sam casual pose_phone = Transform("mod_assets/char_sprites/masayami/pose_phone_casual.png", fit="contain", xysize=(640, 960))

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
            "mod_assets/char_sprites/kotonoha/neutral.png"
        attribute work:
            "mod_assets/char_sprites/kotonoha/work.png"

    group face:
        attribute neut default if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_neut_casual.png"
        attribute neut if_all "work":
            "mod_assets/char_sprites/kotonoha/face_neut_work.png"
        attribute happy if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_happy_casual.png"
        attribute happy if_all "work":
            "mod_assets/char_sprites/kotonoha/face_happy_work.png"
        attribute smug if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_smug_casual.png"
        attribute smug if_all "work":
            "mod_assets/char_sprites/kotonoha/face_smug_work.png"
        attribute teasing if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_teasing_casual.png"
        attribute teasing if_all "work":
            "mod_assets/char_sprites/kotonoha/face_teasing_work.png"
        attribute thinking if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_thinking_casual.png"
        attribute thinking if_all "work":
            "mod_assets/char_sprites/kotonoha/face_thinking_work.png"
        attribute curious if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_curious_casual.png"
        attribute curious if_all "work":
            "mod_assets/char_sprites/kotonoha/face_curious_work.png"
        attribute unamused if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_unamused_casual.png"
        attribute unamused if_all "work":
            "mod_assets/char_sprites/kotonoha/face_unamused_work.png"
        attribute annoyed if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_annoyed_casual.png"
        attribute annoyed if_all "work":
            "mod_assets/char_sprites/kotonoha/face_annoyed_work.png"
        attribute frustrated if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_frustrated_casual.png"
        attribute frustrated if_all "work":
            "mod_assets/char_sprites/kotonoha/face_frustrated_work.png"
        attribute angry if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_angry_casual.png"
        attribute angry if_all "work":
            "mod_assets/char_sprites/kotonoha/face_angry_work.png"
        attribute sad if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_sad_casual.png"
        attribute sad if_all "work":
            "mod_assets/char_sprites/kotonoha/face_sad_work.png"
        attribute crying if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_crying_casual.png"
        attribute crying if_all "work":
            "mod_assets/char_sprites/kotonoha/face_crying_work.png"
        attribute embarrassed if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_embarrassed_casual.png"
        attribute embarrassed if_all "work":
            "mod_assets/char_sprites/kotonoha/face_embarrassed_work.png"
        attribute nervous if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_nervous_casual.png"
        attribute nervous if_all "work":
            "mod_assets/char_sprites/kotonoha/face_nervous_work.png"
        attribute worried if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_worried_casual.png"
        attribute worried if_all "work":
            "mod_assets/char_sprites/kotonoha/face_worried_work.png"
        attribute shocked if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_shocked_casual.png"
        attribute shocked if_all "work":
            "mod_assets/char_sprites/kotonoha/face_shocked_work.png"
        attribute afraid if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_afraid_casual.png"
        attribute afraid if_all "work":
            "mod_assets/char_sprites/kotonoha/face_afraid_work.png"
        attribute panicked if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_panicked_casual.png"
        attribute panicked if_all "work":
            "mod_assets/char_sprites/kotonoha/face_panicked_work.png"
        attribute determined if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_determined_casual.png"
        attribute determined if_all "work":
            "mod_assets/char_sprites/kotonoha/face_determined_work.png"
        attribute empty if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_empty_casual.png"
        attribute empty if_all "work":
            "mod_assets/char_sprites/kotonoha/face_empty_work.png"
        attribute disgusted if_all "casual":
            "mod_assets/char_sprites/kotonoha/face_disgusted_casual.png"
        attribute disgusted if_all "work":
            "mod_assets/char_sprites/kotonoha/face_disgusted_work.png"

# These fixed mid-thigh poses change arm/hand silhouettes, so they stay outside
# the layered image instead of inheriting its default torso and face plate.
image kotonoha work pose_exact_fold = Transform("mod_assets/char_sprites/kotonoha/pose_exact_fold_work.png", fit="contain", xysize=(640, 960))
image kotonoha casual pose_watching = Transform("mod_assets/char_sprites/kotonoha/pose_watching_casual.png", fit="contain", xysize=(640, 960))
image kotonoha casual pose_open_hands = Transform("mod_assets/char_sprites/kotonoha/pose_open_hands_casual.png", fit="contain", xysize=(640, 960))

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
            "mod_assets/char_sprites/himeko/neut_face_base.png"
        attribute uniform:
            "mod_assets/char_sprites/himeko/neut_uniform_face_base.png"

    group face:
        attribute neut default:
            "mod_assets/char_sprites/himeko/face_neut.png"
        attribute happy:
            "mod_assets/char_sprites/himeko/face_happy.png"
        attribute smug:
            "mod_assets/char_sprites/himeko/face_smug.png"
        attribute teasing:
            "mod_assets/char_sprites/himeko/face_teasing.png"
        attribute thinking:
            "mod_assets/char_sprites/himeko/face_thinking.png"
        attribute curious:
            "mod_assets/char_sprites/himeko/face_curious.png"
        attribute unamused:
            "mod_assets/char_sprites/himeko/face_unamused.png"
        attribute annoyed:
            "mod_assets/char_sprites/himeko/face_annoyed.png"
        attribute frustrated:
            "mod_assets/char_sprites/himeko/face_frustrated.png"
        attribute angry:
            "mod_assets/char_sprites/himeko/face_angry.png"
        attribute sad:
            "mod_assets/char_sprites/himeko/face_sad.png"
        attribute crying:
            "mod_assets/char_sprites/himeko/face_crying.png"
        attribute embarrassed:
            "mod_assets/char_sprites/himeko/face_embarrassed.png"
        attribute nervous:
            "mod_assets/char_sprites/himeko/face_nervous.png"
        attribute worried:
            "mod_assets/char_sprites/himeko/face_worried.png"
        attribute shocked:
            "mod_assets/char_sprites/himeko/face_shocked.png"
        attribute afraid:
            "mod_assets/char_sprites/himeko/face_afraid.png"
        attribute panicked:
            "mod_assets/char_sprites/himeko/face_panicked.png"
        attribute determined:
            "mod_assets/char_sprites/himeko/face_determined.png"
        attribute empty:
            "mod_assets/char_sprites/himeko/face_empty.png"
        attribute disgusted:
            "mod_assets/char_sprites/himeko/face_disgusted.png"

# These reactions change Himeko's head or full-body silhouette, so exact image
# names keep the layered image's default body and face from appearing beneath
# them. The legacy `mom wasted` name remains for its existing story/UI callers.
image mom wasted = Transform("mod_assets/char_sprites/himeko/wasted.png", fit="contain", xysize=(640, 960))
image mom casual pose_wasted = Transform("mod_assets/char_sprites/himeko/wasted.png", fit="contain", xysize=(640, 960))
image mom casual pose_furious = Transform("mod_assets/char_sprites/himeko/pose_furious_casual.png", fit="contain", xysize=(640, 960))
image mom uniform pose_objection = Transform("mod_assets/char_sprites/himeko/pose_objection_uniform.png", fit="contain", xysize=(640, 960))

image mc neut = Transform("mod_assets/char_sprites/mc/neutral.png", fit="contain", xysize=(640, 960))

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

image math_teacher neut = Transform("mod_assets/char_sprites/npc/math_teacher.png", fit="contain", xysize=(640, 960))
image civics_teacher neut = Transform("mod_assets/char_sprites/npc/civics_teacher.png", fit="contain", xysize=(640, 960))
image track_coach neut = Transform("mod_assets/char_sprites/npc/track_coach.png", fit="contain", xysize=(640, 960))

# PLACEHOLDER ART: these six still share the generic placeholder sprite.
image science_teacher neut = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image japanese_teacher neut = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image english_teacher neut = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image hikari neut = Transform("mod_assets/char_sprites/npc/hikari.png", fit="contain", xysize=(640, 960))
image homura neut = Transform("mod_assets/char_sprites/npc/homura.png", fit="contain", xysize=(640, 960))
# One scene, one asking, gone forever -- ooc_0604_out_of_ten. He is not written
# as a joke and he is not coming back; the sprite is placeholder because he does
# not warrant art, not because he does not warrant a name.
image daichi neut = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))

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

image gary = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image gregor = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))
image leif = Transform("mod_assets/char_sprites/placeholder/placeholder_sprite.png", fit="contain", xysize=(640, 960))

# Purgatorium (Sam's character story).
image purg_girl = Transform("mod_assets/extra_sprites/purg_girl.png", fit="contain", xysize=(640, 960))
image purg_girl_day7 = Transform("mod_assets/extra_sprites/purg_girl_day7.png", fit="contain", xysize=(640, 960))
image purg_girl_yukata = Transform("mod_assets/extra_sprites/purg_girl_yukata.png", fit="contain", xysize=(640, 960))


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
        # DDLC layeredimages (game/mod_assets/MPT/)
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
