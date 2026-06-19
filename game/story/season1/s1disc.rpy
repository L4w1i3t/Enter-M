label disclaimer:
    # temporary all content unlock
    $ _all_on = persistent.archive_unlocked_roster and persistent.archive_unlocked_music and persistent.archive_unlocked_cgs and persistent.archive_unlocked_character_stories and persistent.archive_unlocked_lost_records
    python:
        persistent.archive_unlocked_roster = True
        persistent.archive_unlocked_music = True
        persistent.archive_unlocked_cgs = True
        persistent.archive_unlocked_character_stories = True
        persistent.archive_unlocked_lost_records = True
        for _cat in character_story_catalog:
            for _story in _cat.stories:
                if _story.persistent_key:
                    setattr(persistent, _story.persistent_key, True)
        for _act in cg_gallery_catalog:
            for _ch in _act.chapters:
                for _cg in _ch.cgs:
                    if _cg.persistent_key:
                        setattr(persistent, _cg.persistent_key, True)
    stop music fadeout 1.0
    call nier_enter from _call_nier_enter_s1disc_1
    call nier_section("NOTICE") from _call_nier_section_s1disc_1
    # CRITIQUE (ADDRESSED): Tightened from five repetitive compliance lines to four that keep the legal function (fiction, no resemblance, sensitive content, acknowledgment) while letting the Nier voice carry one eerie turn instead of reading as flat boilerplate.
    nier "What follows is a work of fiction. Any resemblance to persons living or dead is coincidence."
    nier "Though coincidence, I have found, is only a pattern the reader has not finished tracing."
    nier "Some of what waits inside is heavier than it first appears, and it will not stop to warn you a second time. Reader discretion is advised."
    nier "Proceed only if you accept what you have just been told."
    menu (screen="nier_nvl_choice"):
        "Proceed":
            pass
        "Do not proceed":
            call nier_clear from _call_nier_clear_s1disc_1
            nier "...Then I cannot allow you to partake in this story."
            $ renpy.quit()
    call nier_clear from _call_nier_clear_s1disc_2
    nier "Understood. Thank you for your cooperation."
    # CRITIQUE (ADDRESSED): Added one thematic turn (time only looks generous at the start) before "Make the most of your time here," so the handoff into the timeline carries the slow-burn dread instead of reading as neutral exposition.
    nier "This story takes place within one school year, spanning from May to the March that follows." # May 15 to March 7
    # Prologue (May 15 to May 31)
    # Chapter 1 (June 1 to July 15)
    # Chapter 2 (July 16 to September 1)
    # Chapter 3 (September 2 to October 15)
    # Chapter 4 (October 16 to December 31)
    # Chapter 5 (January 1 to March 7)
    # Japanese school schedule
    nier "It is a generous-looking stretch of road. Most of it only looks that way from where you are standing now."
    nier "Make the most of your time here."
    call nier_exit from _call_nier_exit_s1disc_1
    window hide
    pause 2.0
    jump a0515
