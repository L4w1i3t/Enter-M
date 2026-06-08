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
    # CRITIQUE: This is legally functional, but the first spoken voice of the story is stiff and repetitive. If Nier framing is part of the atmosphere, make even the warning feel intentional; if it is just compliance text, consider keeping it out of the main narrative voice.
    nier "This story is a work of fiction. Any resemblance to actual persons, living or dead, is purely coincidental."
    nier "The events and characters depicted herein are entirely fictional and are not intended to represent any real individuals or occurrences."
    nier "Understand that this story may contain themes and situations that are sensitive in nature."
    nier "Reader discretion is advised."
    nier "By proceeding, you acknowledge that you have read and understood this disclaimer."
    menu (screen="nier_nvl_choice"):
        "Proceed":
            pass
        "Do not proceed":
            call nier_clear from _call_nier_clear_s1disc_1
            nier "...Then I cannot allow you to partake in this story."
            $ renpy.quit()
    call nier_clear from _call_nier_clear_s1disc_2
    nier "Understood. Thank you for your cooperation."
    # CRITIQUE: This transition from legal warning into timeline exposition is clean but emotionally neutral. If the Nier voice is meant to be part of the story's atmosphere, give the line one eerie or thematic turn before "Make the most of your time here."
    nier "This story takes place within one school year, spanning from May to March of the following year." # May 15 to March 7
    # Prologue (May 15 to May 31)
    # Chapter 1 (June 1 to July 15)
    # Chapter 2 (July 16 to September 1)
    # Chapter 3 (September 2 to October 15)
    # Chapter 4 (October 16 to December 31)
    # Chapter 5 (January 1 to March 7)
    # Japanese school schedule
    nier "Make the most of your time here."
    call nier_exit from _call_nier_exit_s1disc_1
    window hide
    pause 2.0
    jump a0515
