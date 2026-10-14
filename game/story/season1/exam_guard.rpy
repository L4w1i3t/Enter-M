default exam_guard_key = None
default exam_guard_subject = None
default exam_guard_period_armed = False
default exam_guard_save_scum_subjects = []
default exam_guard_run = None

# The fields below hold ONE run's ledger (persistent.exam_guard_run names it);
# every other run's waits in exam_guard_runs. See exam_guard_switch_run.
default persistent.exam_guard_run = None
default persistent.exam_guard_runs = {}
default persistent.exam_guard_key = None
default persistent.exam_guard_subject = None
default persistent.exam_save_scum_subjects = []
default persistent.did_save_scum_civics = False
default persistent.did_save_scum_la = False
default persistent.did_save_scum_biology = False
default persistent.did_save_scum_chemistry = False
default persistent.did_save_scum_algebra = False
default persistent.did_save_scum_english = False
default persistent.exam_guard_restart_required = False

init python:
    import datetime as exam_guard_datetime
    import uuid as exam_guard_uuid

    EXAM_GUARD_START_DATE = exam_guard_datetime.date(2025, 5, 26)
    EXAM_GUARD_END_DATE = exam_guard_datetime.date(2025, 5, 28)
    EXAM_GUARD_COMPLETE_KEY = "exam_period:complete"

    EXAM_GUARD_SUBJECT_BASE = {
        "civics": 0,
        "la": 3,
        "biology": 6,
        "chemistry": 9,
        "algebra": 12,
        "english": 15,
    }

    EXAM_GUARD_CHECKPOINT_COMMITMENTS = {
        "day_ready": 0,
        "exam_start": 0,
        "q1_open": 0,
        "q1_answered": 1,
        "q2_open": 1,
        "q2_answered": 2,
        "q3_open": 2,
        "q3_answered": 3,
        "caught": 3,
    }

    EXAM_GUARD_CAUGHT_LABELS = {
        "civics": "a0526_civics_save_scum",
        "la": "a0526_la_save_scum",
        "biology": "a0527_biology_save_scum",
        "chemistry": "a0527_chemistry_save_scum",
        "algebra": "a0528_algebra_save_scum",
        "english": "a0528_english_save_scum",
    }

    EXAM_GUARD_FLAG_NAMES = {
        "civics": "did_save_scum_civics",
        "la": "did_save_scum_la",
        "biology": "did_save_scum_biology",
        "chemistry": "did_save_scum_chemistry",
        "algebra": "did_save_scum_algebra",
        "english": "did_save_scum_english",
    }

    EXAM_GUARD_SUBJECT_NAMES = {
        "civics": "civics",
        "la": "language arts",
        "biology": "biology",
        "chemistry": "chemistry",
        "algebra": "algebra",
        "english": "foreign language",
    }

    # One run's ledger: each persistent field with its empty value.
    EXAM_GUARD_LEDGER = {
        "exam_guard_key": None,
        "exam_guard_subject": None,
        "exam_save_scum_subjects": [],
        "exam_guard_restart_required": False,
    }
    for _exam_guard_flag in EXAM_GUARD_FLAG_NAMES.values():
        EXAM_GUARD_LEDGER[_exam_guard_flag] = False

    def exam_guard_switch_run(run):
        """Make the persistent ledger fields describe `run`. True if they changed.

        Every playthrough shares one persistent file, and the story reads the
        ledger straight from it. Without this, a catch (or a bad ending) in one
        run reads as a catch in every other run loaded after it.
        """
        held = persistent.exam_guard_run
        if run == held:
            return False

        # shortcut: one small archived ledger per exam attempt, never pruned;
        # prune the oldest if persistent size ever matters.
        runs = dict(persistent.exam_guard_runs or {})
        if held:
            filed = {}
            for name, empty in EXAM_GUARD_LEDGER.items():
                value = getattr(persistent, name)
                filed[name] = list(value or []) if isinstance(empty, list) else value
            runs[held] = filed

        record = runs.get(run, None) or {}
        for name, empty in EXAM_GUARD_LEDGER.items():
            value = record.get(name, empty)
            setattr(persistent, name, list(value or []) if isinstance(empty, list) else value)

        persistent.exam_guard_runs = runs
        persistent.exam_guard_run = run
        return True

    def exam_guard_clear_state():
        global exam_guard_key
        global exam_guard_subject
        global exam_guard_period_armed
        global exam_guard_save_scum_subjects
        exam_guard_key = None
        exam_guard_subject = None
        persistent.exam_guard_key = None
        persistent.exam_guard_subject = None
        exam_guard_period_armed = False
        exam_guard_save_scum_subjects = []
        persistent.exam_save_scum_subjects = []
        for flag_name in EXAM_GUARD_FLAG_NAMES.values():
            setattr(persistent, flag_name, False)

    def exam_guard_reset_for_new_game():
        # File the previous run's ledger away rather than erasing it: its
        # saves may still be loaded, and must meet their own record.
        exam_guard_switch_run(None)
        exam_guard_clear_state()
        persistent.exam_guard_restart_required = False
        renpy.save_persistent()

    def exam_guard_begin_exam_period():
        global exam_guard_period_armed
        global exam_guard_run
        exam_guard_run = exam_guard_uuid.uuid4().hex
        exam_guard_switch_run(exam_guard_run)
        exam_guard_clear_state()
        exam_guard_period_armed = True
        renpy.save_persistent()

    def exam_guard_finish_exam_period():
        global exam_guard_key
        global exam_guard_subject
        global exam_guard_period_armed
        exam_guard_period_armed = True
        exam_guard_key = EXAM_GUARD_COMPLETE_KEY
        exam_guard_subject = "exam"
        persistent.exam_guard_key = EXAM_GUARD_COMPLETE_KEY
        persistent.exam_guard_subject = "exam"
        renpy.save_persistent()
        renpy.block_rollback()

    def exam_guard_scum_count():
        return len(getattr(persistent, "exam_save_scum_subjects", None) or [])

    def exam_guard_subject_scummed(subject):
        flag_name = EXAM_GUARD_FLAG_NAMES.get(subject, None)
        if flag_name:
            return bool(getattr(persistent, flag_name, False))
        return subject in (getattr(persistent, "exam_save_scum_subjects", None) or [])

    def exam_guard_day_scummed(subject_1=None, subject_2=None):
        return any(exam_guard_subject_scummed(subject) for subject in (subject_1, subject_2) if subject)

    def exam_guard_scummed_subjects(subject_1=None, subject_2=None):
        return [subject for subject in (subject_1, subject_2) if subject and exam_guard_subject_scummed(subject)]

    def exam_guard_scummed_subjects_outside(subjects):
        excluded = set(subjects or [])
        return [
            subject
            for subject in (getattr(persistent, "exam_save_scum_subjects", None) or [])
            if subject and subject not in excluded
        ]

    def exam_guard_subjects_text(subjects):
        names = [EXAM_GUARD_SUBJECT_NAMES.get(subject, subject) for subject in subjects]
        if not names:
            return "the exam"
        if len(names) == 1:
            return names[0]
        return "{} and {}".format(", ".join(names[:-1]), names[-1])

    def exam_guard_should_bad_end():
        return exam_guard_scum_count() >= 2

    def exam_guard_requires_exam_restart():
        return bool(getattr(persistent, "exam_guard_restart_required", False))

    def exam_guard_rejects_restart_load():
        return exam_guard_requires_exam_restart() and bool(globals().get("exam_guard_key", None))

    def exam_guard_accept_restart_load():
        if exam_guard_requires_exam_restart():
            persistent.exam_guard_restart_required = False
            renpy.save_persistent()

    def exam_guard_release_for_exam_restart():
        exam_guard_clear_state()
        persistent.exam_guard_restart_required = True
        renpy.save_persistent()
        renpy.block_rollback()

    def exam_guard_current_date():
        calendar_obj = globals().get("calendar", None)
        return getattr(calendar_obj, "current_date", None)

    def exam_guard_is_exam_date():
        current_date = exam_guard_current_date()
        if current_date is None:
            return False
        return EXAM_GUARD_START_DATE <= current_date <= EXAM_GUARD_END_DATE

    def exam_guard_prepare_after_load():
        global exam_guard_save_scum_subjects
        # Runs first on every load: the restart lock and the mismatch check
        # after it must read the loaded run's ledger, not the last one played.
        # An armed save with no run predates per-run ledgers and keeps the
        # shared one, as it always did.
        run = globals().get("exam_guard_run", None)
        switched = False
        if run or not globals().get("exam_guard_period_armed", False):
            switched = exam_guard_switch_run(run)

        # Progress must survive the night between papers, and the completed
        # marker must survive after May 28. Otherwise an older exam save can
        # arrive with no persistent point to disagree with and silently reset
        # only part of the three-day period.
        # The offense record also has a save-local mirror, so a save still
        # carries its run's consequence if that run's ledger is ever lost.
        saved_subjects = list(globals().get("exam_guard_save_scum_subjects", None) or [])
        persistent_subjects = list(getattr(persistent, "exam_save_scum_subjects", None) or [])
        merged_subjects = list(persistent_subjects)
        for subject in saved_subjects:
            if subject not in merged_subjects:
                merged_subjects.append(subject)

        exam_guard_save_scum_subjects = list(merged_subjects)
        # The May 29-31 scripts cache this branch marker for readability. A
        # loaded post-exam save restores cached store variables too, so refresh
        # them after merging the save-local and persistent offense records.
        globals()["_exam_one_catch"] = len(merged_subjects) == 1
        globals()["_exam_repair_subject_text"] = exam_guard_subjects_text(merged_subjects)

        persistent_dirty = switched or merged_subjects != persistent_subjects
        if merged_subjects != persistent_subjects:
            persistent.exam_save_scum_subjects = merged_subjects

        for subject in merged_subjects:
            flag_name = EXAM_GUARD_FLAG_NAMES.get(subject, None)
            if flag_name and not bool(getattr(persistent, flag_name, False)):
                setattr(persistent, flag_name, True)
                persistent_dirty = True

        if persistent_dirty:
            renpy.save_persistent()

    def exam_guard_commitment_rank(key):
        if key == EXAM_GUARD_COMPLETE_KEY:
            return 18
        if not key or ":" not in key:
            return 0

        subject, checkpoint = key.split(":", 1)
        base = EXAM_GUARD_SUBJECT_BASE.get(subject, 0)
        committed = EXAM_GUARD_CHECKPOINT_COMMITMENTS.get(checkpoint, 0)
        return base + committed

    def exam_guard_has_mismatch():
        persistent_key = getattr(persistent, "exam_guard_key", None)
        save_key = globals().get("exam_guard_key", None)
        if not exam_guard_is_exam_date():
            return False

        save_armed = bool(globals().get("exam_guard_period_armed", False))
        if not persistent_key:
            # A missing ledger (persistent deleted, or a save copied from
            # another machine) must not turn into an erase button for a save
            # from inside the exam period. A pre-paper save is unarmed and
            # remains the legitimate whole-period restart door.
            return bool(save_armed and save_key)
        if not save_key:
            return save_armed

        # Merely viewing the next question or crossing an overnight story beat
        # is harmless. Only moving to a save with fewer committed answers is
        # the prohibited revision described to the player.
        return exam_guard_commitment_rank(save_key) < exam_guard_commitment_rank(persistent_key)

    def exam_guard_subject_for_catch():
        return (
            globals().get("exam_guard_subject", None)
            or getattr(persistent, "exam_guard_subject", None)
            or "exam"
        )

    def exam_guard_caught_label(subject=None):
        subject = subject or exam_guard_subject_for_catch()
        return EXAM_GUARD_CAUGHT_LABELS.get(subject, "exam_save_scum_caught_generic")

    def exam_guard_set_checkpoint(subject, checkpoint):
        global exam_guard_key
        global exam_guard_subject
        if exam_guard_has_mismatch():
            return True

        key = "{}:{}".format(subject, checkpoint)
        # The store half always moves, because that is what a save carries and
        # what the next load is compared against. The persistent half only has
        # to reach disk before the player can rewind past a committed answer.
        #
        # renpy.save_persistent() is not cheap here: find_changes deep-copies
        # _seen_ever (58k entries by late season 1) on every call, then the
        # developer DebugPickler pickles the 1.4MB persistent a second time
        # before the real dump, then zlib and a write to every save location.
        # Measured floor ~100ms. Paying that at all ten checkpoints of a paper
        # is the hitch on advancing text and on answering a question.
        #
        # Only a rank INCREASE can change a later verdict. exam_start and
        # q1_open both rank 0, q2_open ranks equal to q1_answered, and a new
        # subject's opening rank equals the previous subject's last answer, so
        # a same-rank move cannot make exam_guard_has_mismatch() decide
        # differently. That leaves the three _answered transitions per paper.
        # It also collapses the old double write, where answering flushed once
        # from the choice action and again from the checkpoint after the menu.
        #
        # Ren'Py flushes persistent itself on renpy.save() and on quit or full
        # restart, which covers every ordinary route out of a live session to a
        # rewind; the in-memory persistent stays current either way.
        # An empty key on disk is not merely rank 0: has_mismatch reads it
        # through a different branch, the one that refuses to let a New Game
        # act as an erase button for an armed mid-exam save. So the first
        # checkpoint of a period always flushes, and only same-rank moves on
        # top of an existing key are skipped.
        old_key = getattr(persistent, "exam_guard_key", None)
        exam_guard_key = key
        exam_guard_subject = subject
        persistent.exam_guard_key = key
        persistent.exam_guard_subject = subject
        if (not old_key) or (exam_guard_commitment_rank(key)
                            > exam_guard_commitment_rank(old_key)):
            renpy.save_persistent()
        renpy.block_rollback()
        return False

    def exam_guard_checkpoint_or_jump(subject, checkpoint, caught_label):
        if exam_guard_set_checkpoint(subject, checkpoint):
            renpy.jump(caught_label)

    def exam_guard_answer_checkpoint_from_key():
        key = globals().get("exam_guard_key", None)
        if not key or ":" not in key:
            return None

        subject, checkpoint = key.split(":", 1)
        if not checkpoint.endswith("_open"):
            return None

        return subject, "{}_answered".format(checkpoint[:-5])

    def exam_guard_record_choice_attempt():
        answer_checkpoint = exam_guard_answer_checkpoint_from_key()
        if not answer_checkpoint:
            return

        subject, checkpoint = answer_checkpoint
        if exam_guard_set_checkpoint(subject, checkpoint):
            renpy.jump(exam_guard_caught_label(subject))

    def exam_guard_choice_action(action):
        if action is None:
            return action

        if exam_guard_answer_checkpoint_from_key():
            if isinstance(action, list):
                return [exam_guard_record_choice_attempt] + action

            return [exam_guard_record_choice_attempt, action]

        return action

    def exam_guard_mark_scummed(subject=None):
        global exam_guard_key
        global exam_guard_subject
        global exam_guard_save_scum_subjects
        subject = subject or exam_guard_subject_for_catch()
        subjects = list(getattr(persistent, "exam_save_scum_subjects", None) or [])
        if subject not in subjects:
            subjects.append(subject)
        persistent.exam_save_scum_subjects = subjects
        exam_guard_save_scum_subjects = list(subjects)

        flag_name = EXAM_GUARD_FLAG_NAMES.get(subject, None)
        if flag_name:
            setattr(persistent, flag_name, True)

        key = "{}:caught".format(subject)
        exam_guard_key = key
        exam_guard_subject = subject
        persistent.exam_guard_key = key
        persistent.exam_guard_subject = subject

        renpy.save_persistent()
        renpy.block_rollback()

label exam_save_scum_caught_generic:
    $ exam_guard_mark_scummed()
    scene black
    stop music fadeout 1.0
    pause 2.0
    "The exam remembers the answer you marked."
    "This save cannot take you back far enough to make that first choice disappear."
    $ renpy.utter_restart()

label exam_guard_home_repeat_confrontation(day_name, subject_1=None, subject_2=None):
    $ _exam_guard_home_subjects = exam_guard_scummed_subjects(subject_1, subject_2)
    if not _exam_guard_home_subjects:
        return
    $ _exam_guard_prior_subjects = exam_guard_scummed_subjects_outside(_exam_guard_home_subjects)
    $ _exam_guard_home_subject_text = exam_guard_subjects_text(_exam_guard_home_subjects)
    $ _exam_guard_prior_subject_text = exam_guard_subjects_text(_exam_guard_prior_subjects)
    $ _exam_guard_cross_day = bool(_exam_guard_prior_subjects)
    $ _exam_guard_repeat_multiple = len(_exam_guard_home_subjects) > 1
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 0.5
    pause 2.0
    scene bg living_room_night
    show vignette zorder 99:
        alpha 0.75
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music safety
    play sound moddooropen
    "Mom isn't standing this time. She's at the coffee table with another incident notice open beside my phone."
    play sound moddoorclose
    show mom uniform sad at t11
    if _exam_guard_cross_day:
        mom "It was [_exam_guard_home_subject_text]."
        mom "Again."
    else:
        mom "A second call."
        mom "The same day."
    "My bag slides off my shoulder on its own, and the buckle hits the floor. Above us, somebody moves, then stops."
    show mom uniform determined
    mom "Tell me what you {i}thought{/i} would happen."
    mc "I... don't know."
    mom "Yes, you do."
    "The minute hand above the television crawls forward while I try to get enough air past the back of my tongue to speak."
    mc "...I thought I'd fix one answer. Just the one, and then I'd stop."
    if _exam_guard_repeat_multiple:
        mom "You did not stop after the first."
    mom "That's what you {i}wanted{/i}. I asked what you thought would happen."
    "She waits me out."
    mc "I thought... if it worked, nobody would know."
    show mom uniform sad
    "Her eyes stay on me. Nothing else in her face moves."
    mom "You had already been caught once. What did you think was going to change?"
    mc "I {i}meant{/i} it last time."
    mom "I {i}believed{/i} you."
    "I find a loose thread at my cuff and wind it tight around one finger."
    mom "You stood right there and told me 'okay.' Was that just so I'd let you go upstairs?"
    mc "No! I meant it. I don't know how to--I did mean it."
    show mom uniform worried
    mom "I don't know."
    "I wind the thread until it bites into my fingertip. Same three words she gave me the first night, and tonight I don't dare ask when she'll know."
    mc "...Mom."
    show mom uniform frustrated
    mom "Please don't ask me to comfort you right now."
    "My shoulders fold in anyway, and some stupid, automatic part of me keeps waiting for her to cross the room."
    mom "Please."
    "She presses the heel of her hand into one eye and holds it there."
    show mom uniform sad
    mom "Because I want to."
    mom "After we talked, I got as far as the bottom of those stairs, going over every word I'd said and wondering whether I'd been too hard on you."
    mom "And then the school called me again."
    mom "I love you, [player]."
    mom "Of course I love you. That isn't the part I'm unsure of."
    "She holds out one hand."
    "My hands go to my blazer pockets, then my pants, looking for a phone that's already sitting beside her."
    "Mom remembers with me. Her hand drops back into her lap."
    mom "Right."
    "I have never wanted my phone back less."
    show mom uniform determined
    mom "I have to speak to your teachers and the counselor again. When they ask for your account, you give them the one you just gave me."
    if day_name == "May 28":
        mom "The exams are over. What you did in them is not."
    else:
        mom "You will sit every paper that remains, and you will answer each question once, even when you know you chose wrong."
    mc "...Okay."
    mom "Go upstairs."
    "I bend for my bag."
    mom "[player]."
    "My fingers freeze on the buckle."
    mom "Leave it."
    "I leave the bag where it fell."
    $ hide_calendar()
    scene black with wipeleft_scene
    "Asahina's door eases shut while I'm still on the stairs. When I look back from the landing, Mom is right where I left her."
    return

label exam_guard_home_confrontation(day_name, subject_1=None, subject_2=None):
    $ _exam_guard_home_subjects = exam_guard_scummed_subjects(subject_1, subject_2)
    if not _exam_guard_home_subjects:
        return
    $ _exam_guard_prior_home_subjects = exam_guard_scummed_subjects_outside(_exam_guard_home_subjects)
    # A prior subject, rather than a persistent scene counter, proves there was
    # an earlier confrontation. That keeps legal post-paper reloads from turning
    # one offense into the repeat scene merely because the player reread it.
    if _exam_guard_prior_home_subjects:
        call exam_guard_home_repeat_confrontation(day_name, subject_1, subject_2) from _call_exam_guard_home_repeat_confrontation
        return
    $ _exam_guard_home_subject_text = exam_guard_subjects_text(_exam_guard_home_subjects)
    $ _exam_guard_home_multiple = len(_exam_guard_home_subjects) > 1
    $ hide_calendar()
    scene black with wipeleft_scene
    stop music fadeout 0.5
    pause 2.0
    scene bg living_room_night
    show vignette zorder 99:
        alpha 0.75
    $ show_calendar()
    $ atmos("home")
    with dissolve_scene_full
    play music safety
    play sound moddooropen
    "I've got the front door halfway open when I see Mom standing in the living room, still buttoned into her work jacket like she came straight from court."
    "Her work bag sits at her feet, and her phone lies facedown on the coffee table."
    play sound moddoorclose
    show mom uniform worried at t11
    mom "Set your bag down."
    mc "Mom--"
    show mom uniform determined
    mom "Bag down first. Then look at me."
    "The strap snags around my wrist. I yank too hard, and the buckle smacks the floor just as my eyes start to sting."
    show mom uniform neut
    if _exam_guard_home_multiple:
        mom "Your school called me twice today."
    else:
        mom "Your school called me today about [_exam_guard_home_subject_text]."
    "I'm still clutching the strap when the refrigerator behind her cuts out, and the house goes dead quiet."
    mom "Did you cheat? Yes or no."
    "My mouth opens, but neither answer comes out."
    mom "[player]."
    mc "...Yes."
    "She looks down once. Not at the phone or my bag, just at the floor between us."
    mom "Tell me what you did."
    mc "They already told you."
    show mom uniform determined
    mom "I am asking {i}my son{/i}."
    "My pulse is pounding in my teeth, and {i}I don't remember{/i} very nearly makes it out of my mouth."
    mc "I wanted a better answer. So I went back to before I'd marked it and... picked again."
    "By the end of it I'm talking to my bag, even though she told me to look at her."
    if _exam_guard_home_multiple:
        mc "And then I did it again. On the other paper."
    show mom uniform frustrated
    "Mom shuts her eyes. They're wet when they open, but her jaw sets hard, and the voice that comes out next is low and perfectly level."
    show mom uniform determined
    mom "Did you think that was allowed?"
    mc "No."
    mom "Did somebody make you do it?"
    mc "No."
    mom "You knew it wasn't allowed, and nobody made you. So why?"
    mc "...I chose to do it."
    show mom uniform sad
    "Mom's shoulders drop. Mine climb toward my ears."
    mc "I panicked."
    mom "I {i}believe{/i} you."
    "It's not the answer I was bracing for."
    if _exam_guard_home_multiple:
        mom "But you did it twice. You had hours between those papers to stop."
    else:
        mom "You could have left the wrong answer there. You could have come home and told me the paper went badly."
    mc "The exams, college, all of it--"
    show mom uniform angry
    mom "Do not insult me in my own fucking home by trying to dress this up as pressure."
    "Mom flinches at her own volume, but she doesn't apologize, and she doesn't look away."
    mc "I'm not--I'm not saying it wasn't my fault."
    show mom uniform determined
    mom "Then tell me why you did it without asking me to agree that you had to."
    "My eyes slide off hers and land on the printout, right where we left it on the coffee table. Mom's handwriting runs down one side, and the last line reads {i}Merit scholarship? Ask counselor.{/i}"
    show mom uniform sad
    mom "On Friday, you and I sat in this room and made plans."
    if _exam_guard_home_multiple:
        mc "It was two answers."
    else:
        mc "It was one answer."
    "Mom's mouth goes thin."
    show mom uniform angry
    if _exam_guard_home_multiple:
        mom "It was two answers you were willing to be dishonest for."
    else:
        mom "It was one answer you were willing to be dishonest for."
    if _exam_guard_home_multiple:
        mom "The school can give you two zeros. They can sit you in an office and make you say what you did."
    else:
        mom "The school can give you a zero. They can sit you in an office and make you say what you did."
    show mom uniform neut
    mom "What happens in this house is mine to decide."
    "I stare at her phone. Somewhere under that dark glass, the school's number is sitting at the top of her recent calls."
    mom "Why didn't you tell me?"
    mc "I knew they would call."
    mom "I asked why you didn't tell me yourself."
    "I almost called her from the corridor. I got as far as opening our thread, then put the phone away."
    mc "...I was afraid to see your face."
    "Mom draws a long breath through her nose."
    mom "You still had to come home."
    "I study the buckle on the floor."
    play sound moddooropen
    show mom uniform sad at t21
    show asahina uniform happy at t22
    with dissolve
    ah "I'm home--"
    show asahina uniform shocked
    "Asahina pulls up short in the doorway and takes in my bag on the floor, then Mom's buttoned jacket, then me."
    ah "...Oh."
    show asahina uniform nervous
    ah "I can, um... I can go back outside."
    show mom uniform determined
    mom "No. You live here, and you haven't done anything wrong."
    mom "Go upstairs and get changed, please. I'll talk to you later."
    ah "Right. Okay."
    mc "Asa--"
    mom "Don't ask your sister to make this easier for you."
    show asahina uniform sad
    "Asahina looks back from the first stair, and I make sure all she gets is the top of my head."
    ah "...Night."
    show asahina at thide
    hide asahina
    play sound moddoorclose
    show mom uniform sad at t11
    with dissolve
    "Every stair complains on her way up, and neither of us says a word until her door shuts."
    mom "Here is what happens now."
    "Mom holds out her hand, and I'm already leaning toward her when I realize it isn't meant for my shoulder."
    mom "Phone."
    "I rock back onto my heels and dig the phone out with both hands. She looks away while I set it in her palm."
    show mom uniform determined
    mom "Your laptop stays downstairs, and if you're studying, you do it where I can see the screen."
    if day_name == "May 28":
        mom "Tomorrow is school, any office meeting they call, required track, and home."
    else:
        mom "Tomorrow is school, exams, required track, and home."
    mom "No optional hangouts or club detours, not until I've spoken to the school and decided what I can trust you to handle."
    mc "How long?"
    "It slips out on pure habit, and I want it back immediately."
    mom "I don't know."
    "I had a counteroffer ready for a week. A month, even. I've got nothing for {i}I don't know{/i}."
    if day_name == "May 28":
        mom "Tomorrow, you go to the office and tell the truth before anybody has to pull it out of you."
    else:
        mom "Tomorrow, you take the next paper honestly."
        mom "Even if you know you marked something wrong. Especially then."
    mc "...Okay."
    show mom uniform neut
    mom "Go upstairs. We'll talk again when I've had some time."
    mc "Goodnight."
    mom "...Goodnight."
    $ hide_calendar()
    scene black with wipeleft_scene
    "I take the third stair too fast, the one Mom is always warning me about. It creaks, and tonight the warning never comes."
    return

label exam_guard_bad_ending:
    $ renpy.block_rollback()
    $ hide_calendar()
    $ atmos_clear()
    scene black with dissolve_scene_full
    stop music fadeout 1.0
    pause 2.0
    call nier_enter from _call_nier_enter_exam_guard_bad_ending
    call nier_section("NOTICE") from _call_nier_section_exam_guard_bad_ending
    nier "You revised final answers more than once, so this route cannot continue from here."
    nier "Start a new game, or load a save from before the first exam sheet was turned over on May 26."
    nier "The exam period has to begin again."
    call nier_clear from _call_nier_clear_exam_guard_bad_ending
    nier "Returning you to the title screen."
    call nier_exit from _call_nier_exit_exam_guard_bad_ending
    $ exam_guard_release_for_exam_restart()
    $ renpy.full_restart()

label exam_guard_bad_ending_locked_load:
    $ renpy.block_rollback()
    $ hide_calendar()
    $ atmos_clear()
    scene black with dissolve_scene_full
    stop music fadeout 1.0
    pause 2.0
    call nier_enter from _call_nier_enter_exam_guard_locked_load
    call nier_section("NOTICE") from _call_nier_section_exam_guard_locked_load
    nier "That save begins after the exam period was already broken, so the story cannot continue from there."
    nier "Load a save from before the first exam sheet was turned over on May 26, or start a new game."
    nier "Saves made after that point cannot restart the exam period."
    call nier_clear from _call_nier_clear_exam_guard_locked_load
    nier "Returning you to the title screen."
    call nier_exit from _call_nier_exit_exam_guard_locked_load
    $ exam_guard_release_for_exam_restart()
    $ renpy.full_restart()
