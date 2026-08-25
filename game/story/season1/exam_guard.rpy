default exam_guard_key = None
default exam_guard_subject = None

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
# How many home confrontations the player has actually sat through. The repeat
# scene dispatches on THIS, not on the bad-end threshold: two catches on the
# same day used to cross the threshold before the first confrontation ran, so a
# player's opening scene could be the one full of "last time" callbacks to a
# conversation that never happened.
default persistent.exam_guard_confrontations = 0

init python:
    import datetime as exam_guard_datetime

    EXAM_GUARD_START_DATE = exam_guard_datetime.date(2025, 5, 26)
    EXAM_GUARD_END_DATE = exam_guard_datetime.date(2025, 5, 28)

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
        "english": "English",
    }

    def exam_guard_clear_state():
        global exam_guard_key
        global exam_guard_subject
        exam_guard_clear_active_checkpoint(save=False)
        persistent.exam_save_scum_subjects = []
        for flag_name in EXAM_GUARD_FLAG_NAMES.values():
            setattr(persistent, flag_name, False)
        # The confrontation counter is part of the same timeline as the scum
        # record and dies with it. It lives HERE and not in one of the callers
        # so every teardown path zeroes it: New Game, the start of the exam
        # period, and the bad-ending release. Leave it out of one of them and a
        # fresh run's FIRST catch opens on the repeat scene, which is nothing
        # but callbacks to a conversation that never happened.
        persistent.exam_guard_confrontations = 0

    def exam_guard_clear_active_checkpoint(save=True):
        global exam_guard_key
        global exam_guard_subject
        exam_guard_key = None
        exam_guard_subject = None
        persistent.exam_guard_key = None
        persistent.exam_guard_subject = None
        if save:
            renpy.save_persistent()

    def exam_guard_reset_for_new_game():
        exam_guard_clear_state()
        persistent.exam_guard_restart_required = False
        renpy.save_persistent()

    def exam_guard_begin_exam_period():
        exam_guard_clear_state()
        persistent.exam_guard_restart_required = False
        renpy.save_persistent()

    def exam_guard_seen_confrontation():
        return int(getattr(persistent, "exam_guard_confrontations", 0) or 0) > 0

    def exam_guard_note_confrontation():
        persistent.exam_guard_confrontations = int(
            getattr(persistent, "exam_guard_confrontations", 0) or 0
        ) + 1
        renpy.save_persistent()

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
        if not exam_guard_is_exam_date():
            exam_guard_clear_active_checkpoint()

    def exam_guard_has_mismatch():
        persistent_key = getattr(persistent, "exam_guard_key", None)
        save_key = globals().get("exam_guard_key", None)
        if not persistent_key or not save_key:
            return False
        if not exam_guard_is_exam_date():
            return False
        return save_key != persistent_key

    def exam_guard_subject_for_catch():
        return (
            getattr(persistent, "exam_guard_subject", None)
            or globals().get("exam_guard_subject", None)
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
        exam_guard_key = key
        exam_guard_subject = subject
        persistent.exam_guard_key = key
        persistent.exam_guard_subject = subject
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
        subject = subject or exam_guard_subject_for_catch()
        subjects = list(getattr(persistent, "exam_save_scum_subjects", None) or [])
        if subject not in subjects:
            subjects.append(subject)
        persistent.exam_save_scum_subjects = subjects

        flag_name = EXAM_GUARD_FLAG_NAMES.get(subject, None)
        if flag_name:
            setattr(persistent, flag_name, True)

        key = "{}:caught".format(subject)
        exam_guard_key = key
        exam_guard_subject = subject
        persistent.exam_guard_key = key
        persistent.exam_guard_subject = subject

        # Lock in the save-scum achievements NOW, while the scum is still counted.
        # This state (exam_save_scum_subjects) is wiped by exam_guard_reset_for_new_game()
        # on the next New Game, so waiting for the Archive to sync would lose it.
        # ach_lock writes into the permanent persistent.ach_earned set; running it
        # before save_persistent() below means it is saved in the same pass.
        _ach_lock = globals().get("ach_lock", None)
        if _ach_lock:
            _ach_lock("caught_once", "scum_two")

        renpy.save_persistent()
        renpy.block_rollback()

label exam_save_scum_caught_generic:
    $ exam_guard_mark_scummed()
    stop music
    scene black
    "The exam remembers."
    "This save file cannot return you to an answer you already tried."
    $ renpy.utter_restart()

label exam_guard_home_repeat_confrontation(day_name, subject_1=None, subject_2=None):
    $ _exam_guard_home_subjects = exam_guard_scummed_subjects(subject_1, subject_2)
    if not _exam_guard_home_subjects:
        return
    $ exam_guard_note_confrontation()
    $ _exam_guard_prior_subjects = exam_guard_scummed_subjects_outside(_exam_guard_home_subjects)
    $ _exam_guard_home_subject_text = exam_guard_subjects_text(_exam_guard_home_subjects)
    $ _exam_guard_prior_subject_text = exam_guard_subjects_text(_exam_guard_prior_subjects)
    $ _exam_guard_all_subject_text = exam_guard_subjects_text(getattr(persistent, "exam_save_scum_subjects", None) or [])
    $ _exam_guard_cross_day = bool(_exam_guard_prior_subjects)
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg living_room
    show vignette zorder 99:
        alpha 0.75
    $ show_calendar()
    $ atmos("home")
    stop music fadeout 0.5
    with dissolve_scene_full
    play music safety
    play sound moddooropen
    "The front door opens like it is trying not to make a sound."
    "It fails."
    "Mom is already in the living room."
    "Standing."
    "Phone in one hand."
    "Not facedown this time."
    "Not waiting to testify."
    "Already on the record."
    "None of the cold, court-ready calm from last time is here. No armor she put on at the door to get through this professionally."
    "Whatever she decided to be on the drive home didn't survive the walk from the car."
    play sound moddoorclose
    show mom uniform angry at t11
    mom "Bag down."
    mc "...Mom."
    mom "No."
    "One word."
    "No volume behind it."
    "No room inside it."
    mom "Put. Your shit. {i}DOWN.{/i}"
    "I lay my bag on the floor."
    "Carefully."
    "Like gentleness can retroactively become character."
    if _exam_guard_cross_day:
        mom "After [_exam_guard_prior_subject_text], I told myself the next call from school could not possibly be the same sentence."
        mom "I told myself my son understood what he had done."
        mom "Then today happened."
        $ _exam_guard_home_subject_sentence = _exam_guard_home_subject_text[:1].upper() + _exam_guard_home_subject_text[1:]
        mom "[_exam_guard_home_subject_sentence], of ALL things."
        $ _exam_guard_home_subject_sentence = _exam_guard_home_subject_text[:1].lower() + _exam_guard_home_subject_text[1:]
        "The subject name sits between us with no academic meaning left in it."
    else:
        mom "Two calls."
        mom "Same day."
        mom "Two separate times. Two separate chances for you to stop making the worst possible choice."
    mc "I--"
    mom "{i}Don't.{/i}"
    "Last time she kept her voice in a box. Tonight the box is open, and she's not putting anything back in it."
    show mom uniform determined
    mom "The first time, I could still call it a catastrophic decision."
    mom "A dishonest one."
    mom "An arrogant one."
    mom "A decision made by a scared kid who thought panic gave him permission to become smaller than himself."
    if _exam_guard_cross_day:
        mom "But this was after consequence."
        mom "After the school knew."
        mom "After I knew."
        mom "After you looked me in the face and said you understood."
    else:
        mom "But this was after the first teacher stopped you."
        mom "After the room changed around you."
        mom "After you had already seen exactly where that door led."
    show mom uniform angry
    mom "So I need you to hear the word I wouldn't let myself use last time."
    mom "This isn't panic anymore."
    "She's louder now. She doesn't try to pull it back."
    show mom uniform pose_objection
    mom "This is a {i}pattern.{/i}"
    mc "...I know I messed up."
    show mom uniform angry
    mom "No."
    mom "You do not get to call this messed up."
    mom "A mess is something scattered."
    mom "This has a line through it."
    mom "This is [_exam_guard_all_subject_text]."
    mom "This is you being given the boundary once, then walking through it again to see if the world was serious."
    mc "I wasn't trying to--"
    mom "You were trying to change an answer."
    mom "Again."
    mom "Everything after that is decoration."
    "My throat closes around the rest of the sentence."
    "It deserved worse than that."
    "It deserved to be refused before it reached the air."
    mom "Do you understand what happens when trust breaks twice?"
    mc "...It gets worse."
    mom "No."
    mom "It changes category."
    mom "The first break makes people careful."
    mom "The second makes them reevaluate whether they were wrong about you."
    show mom uniform worried
    "Her fingers tighten around the phone."
    "Not dramatically."
    "Just enough for me to see that anger is not the only thing she is holding back."
    mom "I have spent years telling people who you are."
    mom "Brilliant."
    mom "Tired, sometimes."
    mom "Too clever for your own good, often."
    mom "But decent."
    mom "Trying."
    mom "Worth trusting with the future he keeps pretending not to want."
    mom "And now I have to ask myself whether I was describing you, or a version of you I was proud to believe in."
    mc "Mom..."
    show mom uniform sad
    "Her face changes."
    "At first, I think she's getting angrier."
    "Then her mouth tightens in the wrong direction."
    "Not rage."
    "Not strategy."
    "Pain."
    mom "No."
    "The word barely comes out."
    mom "Do not say it like that."
    mom "Do not say Mom like it is a door you can still open just by sounding small enough."
    "Her breath catches."
    "She looks away from me for the first time since I came in."
    "That's worse than being stared down."
    "The argument loses its shape and becomes something I cannot defend against."
    show mom uniform frustrated
    mom "I am angrier than I have words I am willing to use in this house."
    mom "I do not trust myself to hold a full glass right now."
    "Her hand shakes around the phone."
    "This time she notices."
    "This time she cannot turn it into posture."
    show mom uniform afraid
    mom "And I am scared."
    mom "Do you understand that?"
    mom "I...am scared in a way I do not have a professional voice for."
    show mom uniform crying
    "She presses two fingers under one eye like she can physically hold the tear in place."
    "It doesn't work."
    mom "Because I know what to do with a school."
    mom "I can ask for policy. I can make calls. I can make sure nobody turns my son into one ugly word on a form."
    mom "I can do that."
    mom "I know how to do that."
    mom "I have done harder things than that for people I loved less."
    "Her voice breaks on loved."
    "The sound is so small it makes the whole room smaller with it."
    mom "But you..."
    "She stops."
    "Swallows."
    "Starts again, worse."
    mom "I cannot do that part for you."
    mom "I cannot cross-examine you into being honest."
    mom "I cannot argue you into...into caring about the rule when nobody is standing over your shoulder."
    mom "And I hate that I have to say that."
    mom "I hate that sentence being in my mouth."
    mom "I cannot protect you from the part where you chose this twice."
    mc "...I'm sorry."
    mom "Please do not make me comfort you right now."
    "That stops me harder than yelling."
    mom "Please."
    "The second one isn't anger."
    "It's almost pleading."
    "That's the part that makes my stomach turn."
    mom "Because I want to."
    mom "I hate that I want to."
    mom "No."
    mom "No, I do not hate it. I am your mother. Of course I want to."
    mom "You look like you are about to break, and I want to fix it."
    mom "I want to put my arms around you and tell you there is still a way through."
    mom "There probably is."
    mom "There usually is."
    mom "But I cannot..."
    "Her mouth closes."
    "For a second, she looks almost lost."
    mom "I cannot be the place you run to."
    mom "Not yet."
    mom "Not before you understand--"
    mom "No. Not understand."
    mom "You understand plenty."
    mom "Before you admit what you did without trying to turn yourself into the wounded part of it."
    show mom uniform determined
    "She wipes her face once, fast and angry."
    "Like the tears are another problem she intends to solve by force."
    mom "That is what this cost."
    "She says it like she hates the word."
    mom "Listen to me. Cost. Like I can total it."
    mom "It is not my good mood."
    mom "It is not one evening."
    mom "It is not even the calls from school."
    mom "It is this."
    show mom uniform sad
    mom "I love you."
    mom "I love you so much it is making me stupid right now."
    mom "And I do not know if I can trust you."
    mom "Those two things are in the same room now, and I do not know what to do with them."
    "The words land crooked."
    "They hurt more because they do not sound prepared."
    mom "That's what you did tonight. Not to me. Not {i}only{/i} to me."
    show mom uniform angry
    mom "And don't you {i}dare{/i} make this smaller by turning it into my feelings."
    mom "Stop looking for the version where the worst thing you did was hurt me. You made every adult who vouched for you go back through the file and wonder what {i}else{/i} they missed."
    "Everything tilts quietly."
    "Not enough to fall."
    "Just enough to understand that falling would be easier."
    mc "...What happens now?"
    mom "Now?"
    "She laughs once."
    "It isn't a laugh."
    "It's what her voice does because the body has no professional tool for this."
    "She drags one breath in."
    "Then another."
    "By the second one, Mom is trying to build the lawyer voice back out of the pieces."
    mom "Now..."
    "The first attempt falls apart."
    show mom uniform neut
    mom "Now I stop treating this like a bad night."
    show mom uniform determined
    mom "Your phone stays with me."
    mom "Your laptop stays downstairs."
    mom "Your teachers, counselor, and I are going to have a conversation you do not control."
    if day_name == "May 28":
        mom "And since the exams are over, you do not get the dignity of proving something tomorrow by simply taking the next paper honestly."
        mom "You start with repair."
        mom "Actual repair."
        mom "Not charm. Not grades. Not one more clean performance."
    else:
        mom "If there is another exam, you will take it with the knowledge that nobody in that building owes you the benefit of the doubt anymore."
        mom "You will sit there and earn back what you can, one honest answer at a time, knowing it may not be enough."
    mc "Yes, ma'am."
    mom "Do not."
    "The phrase dies in my mouth."
    mom "Do not give me obedience because you think it sounds like remorse."
    mom "Remorse is what you do when I am not in the room."
    mom "And right now, [player], I do not know who you are when I am not in the room."
    "That's the line."
    "Not the loudest one."
    "Not the cruelest."
    "The one that changes the room from home into evidence."
    "Somewhere upstairs, a floorboard makes the smallest sound and then goes still."
    "Asahina heard enough."
    "Of course she did."
    mom "Go upstairs."
    mc "...Okay."
    mom "No games."
    mom "No messages."
    mom "No speech about pressure."
    mom "You are going to sit with the fact that this was not one mistake the story could absorb."
    mom "This was you choosing the same lie after it already had consequences."
    "My hand finds the bag strap before I remember the bag is not coming with me."
    "Mom notices."
    "She says nothing."
    "That's worse."
    $ hide_calendar()
    scene black with wipeleft_scene
    "The stairs do not feel longer this time."
    "They feel final."
    "There's a difference between being punished inside a story and breaking the terms that let it keep going."
    "{i}I can feel that difference now.{/i}"
    return

label exam_guard_home_confrontation(day_name, subject_1=None, subject_2=None):
    $ _exam_guard_home_subjects = exam_guard_scummed_subjects(subject_1, subject_2)
    if not _exam_guard_home_subjects:
        return
    # Dispatch on whether Himeko has already had this conversation with him, not
    # on the bad-end count. Two catches in one day now play the FIRST scene (in
    # its two-subject variant), and the repeat scene only runs when there really
    # was a previous time for it to refer back to.
    if exam_guard_seen_confrontation():
        call exam_guard_home_repeat_confrontation(day_name, subject_1, subject_2) from _call_exam_guard_home_repeat_confrontation
        return
    $ exam_guard_note_confrontation()
    $ _exam_guard_home_subject_text = exam_guard_subjects_text(_exam_guard_home_subjects)
    $ _exam_guard_home_multiple = len(_exam_guard_home_subjects) > 1
    $ hide_calendar()
    scene black with wipeleft_scene
    pause 2.0
    scene bg living_room
    show vignette zorder 99:
        alpha 0.75
    $ show_calendar()
    $ atmos("home")
    stop music fadeout 0.5
    with dissolve_scene_full
    play music safety
    play sound moddooropen
    "I get the front door halfway open before the house tells me I'm late to my own sentencing."
    "Mom is standing in the living room. Her work bag is still by her feet. Her jacket is still on. Her phone is facedown on the coffee table like it already testified."
    play sound moddoorclose
    show mom uniform neut at t11
    "She doesn't even say hello and I can't even get in a word before--"
    mom "Set your bag down."
    mc "Mom..."
    show mom uniform determined
    mom "Down. We're not doing this in the doorway."
    "My fingers forget how straps work, and the bag hits the floor too loud."
    show mom uniform unamused
    mom "I got a nice little phone call from your school this afternoon."
    if _exam_guard_home_multiple:
        mom "Two of them, actually. I want you to sit with the fact that there were two."
    else:
        mom "About [_exam_guard_home_subject_text]."
    "My stomach goes through the floor and keeps going."
    mc "Listen, I can explain."
    show mom uniform determined
    mom "No. You don't get to open with explain."
    mom "Explain is what people reach for when the facts are bad and they want better lighting on them."
    mom "You can answer, and answer only."
    show mom uniform neut
    mom "Did you cheat on [_exam_guard_home_subject_text]?"
    mom "Yes or no."
    "The word {i}cheat{/i} doesn't sound like a word in her mouth. It sounds like a line item with my name typed above it."
    mc "..."
    mom "[player]. I won't ask a third time."
    mc "...Yes."
    mom "Thank you."
    "It's the most frightening thank-you I have ever heard."
    mom "You didn't make me pull it out of you. Hold onto that. It's the only thing you're keeping tonight."
    show mom uniform angry
    "Her hand moves toward the coffee table, sharp and useless, like she just needs somewhere to set the anger down. Halfway there she stops and folds it back against her side."
    "I watch her decide to stay calm. I watch what it costs. It crosses her face like weather and then it's gone, pressed flat."
    show mom uniform neut
    mom "I'm going to keep my voice down."
    mom "Not for your sake. Because if I start, I won't be fair--and you don't get to make me unfair on top of everything else you did today."
    mc "I panicked..."
    show mom uniform frustrated
    "She closes her eyes for exactly one second, then gradually opens them."
    "My skin grows colder at the audible deep breath that she takes in the process."
    mom "Don't hand me panic like it's a receipt."
    mc "I thought if I could just--"
    show mom uniform determined
    mom "Stop. Think about the end of that sentence before you say it to me."
    mc "...fix one answer."
    mom "Fix it..."
    show mom uniform thinking
    "She turns the word over like she's holding it up to the light to find the crack."
    mom "Fix it how, hm? By breaking the {i}one{/i} rule every other kid in that room managed to follow? By deciding the school day was your rough draft and everyone else was just living inside it?"
    mc "I'm not trying to make it smaller."
    show mom uniform neut
    mom "You are. That's the entire job of the word 'panicked.'"
    "She says it without heat. That's what makes it land."
    mom "It's the sentence that asks me to hear 'scared' and stop hearing 'chose.' I'm not doing that for you."
    "My mouth closes. It's embarrassing how fast it closes."
    if _exam_guard_home_multiple:
        mom "{i}Two exams{/i}, [player]."
        mom "Two."
        mom "Two separate adults had to stop their rooms because my son--my {i}honor student{/i}--decided rules were for people with less to lose."
    else:
        mom "{i}One exam{/i} was enough."
        mom "One adult had to stop a room because my son--my {i}honor student{/i}--decided rules were for people with less to lose."
    show mom uniform determined
    mom "Do you understand what that {i}does{/i}?"
    mom "Do you have any idea what kind of sentence you just attached to your own name?"
    mc "...It was a zero."
    mom "A zero?"
    show mom uniform angry
    "Her voice jumps on the word, then clamps back down so hard I can hear the effort."
    mom "{i}A zero?{/i}"
    mom "You think I am standing here in my work shoes, still in my nice clothes, because of a {i}zero{/i}?!"
    mc "No, I--I just meant--"
    show mom uniform unamused
    mom "I know what you meant."
    mom "You meant: maybe if I call it a grade, it stops being a character issue."
    mom "It does NOT."
    mc "That's not--"
    mom "It {i}is{/i}."
    mom "And no, you did not think. That is the problem."
    show mom uniform determined
    mom "This is not only a grade."
    mom "This is a {i}record{/i}."
    mom "This is a counselor conversation."
    mom "This is a teacher who now has to decide whether your recommendation comes with an asterisk."
    mom "This is the phrase {i}academic dishonesty{/i} attached to your name in a school system that was perfectly happy to call you exceptional last week."
    "Friday night comes back in pieces."
    "The laptop on the coffee table."
    "The program page."
    "Merit scholarship with a question mark beside it."
    "Mom writing dates down so the future would look less impossible."
    show mom uniform sad
    mom "On Friday night, I sat in this room and helped you look at admissions requirements."
    mom "Friday night, [player]."
    mom "I wrote {i}merit scholarship?{/i} with a question mark because I believed the question was logistics."
    show mom uniform pose_objection
    "She points at the coffee table, though the notebook is not there."
    mom "Now I have to ask whether academic misconduct follows you into recommendations."
    mom "Now I have to ask whether the counselor has to say, well, yes, he is brilliant, when he is not trying to cheat his way around pressure."
    mc "Mom, please, I wasn't trying to--"
    show mom uniform angry
    mom "{i}No.{/i}"
    mom "Do not {i}please{/i} me right now."
    mom "Do not give me the front half of 'I wasn't trying to' and expect me to fill in innocence on the back end."
    mom "You were not trying to what?"
    mom "Get caught?"
    mom "Hurt me?"
    mom "Damage your own future?"
    mom "Fine! Wonderful. {i}Congratulations{/i} on having bad intent management and even worse judgment."
    mom "Do NOT soften your voice and try to make me the cruel one for saying the hard thing out loud."
    show mom uniform frustrated
    "Her eyes are bright in a way that makes the anger worse."
    mom "I have spent my entire career watching people make bad decisions and then try to narrate them into something softer."
    mom "I am very good at hearing the shape of an excuse before it finishes standing up."
    mom "So do not--"
    "She stops herself."
    "She breathes in. It does not calm her down. It just files the edge off the word she was reaching for and leaves the meaning standing there, bare."
    show mom uniform angry
    mom "Do not insult me in my own fucking home by trying to dress this up as pressure."
    mc "I know I screwed up, but--"
    show mom uniform determined
    mom "You did {i}not{/i} screw up."
    mom "And you do {i}not{/i} get a but."
    "The sentence cuts clean through the room."
    mom "You. {i}Chose.{/i}"
    mom "A screwup is a forgotten homework sheet."
    mom "A screwup is sleeping through an alarm."
    mom "A screwup is writing the wrong formula because your brain saw one symbol and grabbed the wrong file."
    mom "This?"
    mom "This was a {i}choice{/i}."
    "My throat tightens."
    "I hate that I want her to stop."
    "I hate more that I do not have a right to ask."
    mc "...I know, I just--"
    mom "No."
    mom "No {i}just{/i}."
    mom "No corner to tuck the ugly part into."
    mom "No little word that makes the sentence easier to carry."
    mc "I...I know, mo--"
    show mom uniform neut
    mom "Do you?"
    "Not even a question. A door she isn't opening."
    mom "Because if you knew--{i}really{/i} knew--you'd be angrier at yourself than you are scared of me."
    mom "And what I'm looking at right now is fear. Calculation. A kid running the numbers on how bad this is about to get."
    show mom uniform disgusted
    mom "That's the part I can't stand. Not even the cheating. That you're sitting there still solving for the exit."
    "That one finds the soft part under the ribs."
    mc "I do understand, Mom..."
    "It comes out too fast. Too wet. Not crying, exactly. Close enough that pretending otherwise would be one more lie."
    show mom uniform neut
    mom "Then let it cost you something."
    mom "Hold onto it until it teaches you more than how to hide better next time. Otherwise that's all shame is good for, and I didn't raise you to get good at hiding."
    "The front door opens behind me."
    play sound moddooropen
    show mom uniform neut at t21
    show asahina uniform happy at t22
    with dissolve
    ah "I'm home--"
    show asahina uniform shocked
    "She stops with one foot still outside the room."
    "Her eyes move from Mom's face, to me, to my bag on the floor, to the phone sitting facedown like evidence."
    ah "...Oh."
    "This time, she doesn't make a joke fast enough to save herself."
    show asahina uniform nervous
    ah "I'm just gonna...ahah..."
    show mom uniform determined
    mom "Asahina."
    ah "Nah, I get the assignment."
    "She raises both hands, palms out, already backing toward the hall."
    show asahina uniform afraid
    ah "Kitchen, water, upstairs, out of your way."
    mom "Yep. Now go."
    ah "Yes, ma'am."
    mc "Asa--"
    show mom uniform angry
    mom "LEAVE your sister out of it."
    "Louder than her previous volume. It doesn't need to be, and yet it is."
    show asahina uniform sad
    "My sister, half paralyzed, looks at me for one second."
    "Not pity."
    "Not even shock anymore."
    "Her eyes tell a very quick, very clear message."
    "{i}'I cannot help you with this one.'{/i}"
    show asahina at thide
    hide asahina
    play sound moddoorclose
    show mom uniform unamused at t11
    with dissolve
    "The house swallows the sound of her escape."
    "Mom waits until the upstairs floorboard gives its smallest complaint."
    mom "Your sister has more sense walking into a room by accident than you showed walking into an exam on purpose."
    mc "...Yeah."
    mom "Here is what happens now."
    show mom uniform determined
    "She holds out one hand."
    mom "Phone. Now."
    "I pull it from my pocket and hand it over without reservation."
    "She sets it beside her own on the coffee table."
    mom "Laptop downstairs unless you are studying where I can see the screen."
    if day_name == "May 28":
        mom "School. Office meetings if they call them. Track if your coach requires it. Home."
    else:
        mom "School. Exams. Track if your coach requires it. Home."
    mom "No optional hangouts."
    mom "No club detours."
    mom "No pretending your room is a bunker where consequences politely wait outside."
    mc "For how long?"
    "The question is stupid."
    "I know it before her eyes answer."
    mom "Until I speak to the school, understand the formal consequences, and decide what I can trust you to handle."
    mom "And right now? That list is {i}short{/i}."
    mc "...Okay."
    mom "And tomorrow, you are going to walk into that building and behave like someone who still has a character to rebuild."
    if day_name == "May 28":
        mom "If there is no exam left, then you start with the office, the counselor, and every adult who now has reason to ask whether they misread you."
    else:
        mom "If there is another exam, you will take it honestly."
        mom "Even if your stomach is trying to climb out through your throat."
        mom "ESPECIALLY then."
    mc "Yes, ma'am."
    mom "Do not say that like a magic phrase."
    mc "I'm not."
    mom "Then make it {i}true{/i}."
    "She steps back, and only with the distance do I see it: she's been shaking the whole time. Small. Held. Controlled all the way down."
    "She kept it there through every word of that. On purpose. For both of us. I don't get to know what it cost her."
    show mom uniform neut
    mom "Now go upstairs."
    mom "I've said the part that's fair. If I keep going, I'll stop being fair, and you don't get to take that from me too."
    "That lands harder than any amount of yelling could have."
    mc "...Okay."
    $ hide_calendar()
    scene black with wipeleft_scene
    "The stairs feel longer than usual."
    "Behind me, the living room stays bright, clean, and occupied by a mother trying very hard not to turn anger into something less useful."
    "Upstairs, Asahina's door is closed."
    "There's no music from her room, nor can I hear laughter and sweet nothings from what's probably a phone call."
    "No sign that she wants to be dragged into the blast radius."
    "{i}Fair.{/i}"
    "{i}The radius is mine.{/i}"
    return

label exam_guard_bad_ending:
    $ renpy.block_rollback()
    stop music fadeout 1.0
    $ hide_calendar()
    $ atmos_clear()
    scene black with dissolve_scene_full
    call nier_enter from _call_nier_enter_exam_guard_bad_ending
    call nier_section("NOTICE") from _call_nier_section_exam_guard_bad_ending
    nier "You were asked to answer."
    nier "You chose instead to revise the terms of the world."
    nier "One dishonest exam can be contained as damage."
    nier "Two stops being an accident and starts being a shape you chose."
    call nier_clear from _call_nier_clear_exam_guard_bad_ending2
    nier "Through your dishonesty, you have derailed this story beyond repair."
    nier "The route cannot continue from here."
    nier "Start a new game, or load a save from before the first exam sheet was turned over on May 26."
    nier "I am disappointed."
    nier "Disappointed in the small, cold way that comes from watching someone capable choose less than themselves."
    call nier_clear from _call_nier_clear_exam_guard_bad_ending
    nier "Returning you to the title screen."
    call nier_exit from _call_nier_exit_exam_guard_bad_ending
    $ exam_guard_release_for_exam_restart()
    $ renpy.full_restart()

label exam_guard_bad_ending_locked_load:
    $ renpy.block_rollback()
    stop music fadeout 1.0
    $ hide_calendar()
    $ atmos_clear()
    scene black with dissolve_scene_full
    call nier_enter from _call_nier_enter_exam_guard_locked_load
    call nier_section("NOTICE") from _call_nier_section_exam_guard_locked_load
    nier "That is not the beginning of the exam period."
    nier "The story is still broken from that point."
    nier "Load a save from before the first exam sheet was turned over on May 26, or start a new game."
    nier "You were given the boundary because the boundary matters."
    call nier_clear from _call_nier_clear_exam_guard_locked_load
    nier "Returning you to the title screen."
    call nier_exit from _call_nier_exit_exam_guard_locked_load
    $ exam_guard_release_for_exam_restart()
    $ renpy.full_restart()
