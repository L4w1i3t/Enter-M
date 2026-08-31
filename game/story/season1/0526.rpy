label a0526:
    # --- Day 12: 2025-05-26 --
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    play music quiz
    # Three days of exams. Day 1: morning Civics, afternoon Language Arts.
    #
    # CONTRACT ORDER IS LOAD-BEARING. The proctor states the in-world rule and
    # nier states the out-of-world half BEFORE exam_guard_begin_exam_period()
    # arms anything. A rule the player is only shown at the moment of
    # punishment is not a rule; everything the guard does downstream depends on
    # this block running first.
    "First day of exams."
    "The classroom has gone into that special exam silence where every cough feels like a misdemeanor."
    "Civics is first."
    show civics_teacher neut at t11
    civics_teacher "Phones away. Bags at the front."
    civics_teacher "Two things before the bell."
    civics_teacher "One: an answer is final once it is marked. If you change your mind, cross it out and live with the crossing out."
    civics_teacher "Two: a paper that leaves this room and comes back different is not a corrected paper. It is a different paper, and I will treat it as one."
    "{i}Dramatic for a Monday.{/i}"
    civics_teacher "You may begin when the bell rings."
    "The paper lands on my desk facedown."
    $ hide_calendar()
    scene black with dissolve_scene_full
    call nier_enter from _call_nier_enter_0526_1
    nier "That second rule was not only for him."
    nier "From now until Wednesday evening, this story keeps its own record of which answer you marked first."
    nier "Saving is fine. Quitting is fine. Resuming from where you stopped is fine."
    nier "Going back to an answer you have already marked is not, and it will be noticed."
    nier "If something goes genuinely wrong, the whole exam period can be restarted from before the first paper. That door stays open."
    nier "Three days. Choose accordingly."
    call nier_exit from _call_nier_exit_0526_1
    pause 1.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    with dissolve_scene_full
    $ exam_guard_begin_exam_period()
    $ exam_guard_checkpoint_or_jump("civics", "exam_start", "a0526_civics_save_scum")
    # SFX SUGGESTION: A stark exam bell with no crowd noise following it.
    "The bell rings."
    "I turn the paper over."
    $ exam_guard_checkpoint_or_jump("civics", "q1_open", "a0526_civics_save_scum")
    "{i}Question 1. When a court strikes down a law because it conflicts with the constitution, which principle is being applied?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Federalism.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Federalism. Courts and legislatures, two levels of something disagreeing."
            "I circle it."
        "Judicial review.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Judicial review. A court checks a law against the higher rulebook and finds the conflict."
            "{i}Careful confidence.{/i}"
        "Popular sovereignty.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Popular sovereignty. The phrase looks noble on the page, and noble usually scores well."
            "I circle it."
    $ exam_guard_checkpoint_or_jump("civics", "q1_answered", "a0526_civics_save_scum")
    "The next few questions stay polite and use familiar language."
    "Rights, institutions, participation. All the comforting nouns that become less comforting the moment people enter the room."
    $ exam_guard_checkpoint_or_jump("civics", "q2_open", "a0526_civics_save_scum")
    "{i}Question 2. Which situation is the clearest example of federalism?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "A national legislature passes one law for the whole country.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "One law, one country. That is the most national-sounding option on the page."
            "I mark it and move on."
        "Local and national governments both exercise powers in their own spheres.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Layered authority, divided responsibility, and enough overlap to keep lawyers busy."
            "{i}Mom would appreciate that last part more than the exam grader.{/i}"
        "A court explains the meaning of a disputed statute.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "A court and a statute in the same sentence. Close enough to feel civic."
            "I mark it and move on."
    $ exam_guard_checkpoint_or_jump("civics", "q2_answered", "a0526_civics_save_scum")
    # SFX SUGGESTION: A wooden pencil clattering once against the hard classroom floor.
    "A pencil drops somewhere behind me."
    "Nobody reacts. The class has achieved true exam discipline."
    $ exam_guard_checkpoint_or_jump("civics", "q3_open", "a0526_civics_save_scum")
    "{i}Question 3. Before the government can deprive a person of liberty or property, it must follow fair procedures. Which constitutional concept does this describe?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "Separation of powers.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Branches keeping one another from getting too comfortable. This question is about limits, and that is the limits one."
            "I mark it."
        "Majority rule.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Somebody decided to deprive somebody. Somebody usually decides by counting."
            "I mark it."
        "Due process.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Due process. Rules for how authority is allowed to touch a life before it starts rearranging one."
            "{i}The sentence is cleaner than my handwriting, at least.{/i}"
    $ exam_guard_checkpoint_or_jump("civics", "q3_answered", "a0526_civics_save_scum")
    "The last page asks for a short response about legitimacy and public trust."
    "I write about authority needing reasons people can recognize, not just consequences people fear."
    "I leave the sentence alone after that."
label a0526_after_civics:
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_civics:
        nier "Civics continues without me."
        nier "That is the first thing that really gets through. Not the zero, not the teacher's voice, not the way the room looked away too quickly."
        nier "The exam keeps moving, and I sit with my pencil down while everyone else still has a future measured in answer bubbles."
        nier "By the bell, my paper is already somewhere on the teacher's desk, separate from the others in a way that feels administrative before it feels dramatic."
    else:
        nier "Civics ends with a stack of papers carried to the front in a silence nobody wants to disturb."
        # SFX SUGGESTION: Several chairs scraping back as the exam-room silence breaks into low chatter.
        nier "The room exhales in fragments. Chairs scrape, bags reclaim their owners, and several people begin the sacred post-exam ritual of asking questions whose answers can only cause harm."
        nier "I do not participate."
    call nier_clear from _call_nier_clear_0526_1
    pause 2.0
    scene bg corridor
    $ show_calendar()
    $ atmos("afternoon")
    stop music fadeout 1.0
    with wipeleft_scene
    if persistent.did_save_scum_civics:
        play music hopeless
    else:
        play music daily
    if persistent.did_save_scum_civics:
        "Lunch is not lunch."
        "It is forty minutes of pretending my bag has not turned into a sealed envelope marked {i}disciplinary matter{/i}."
        "The hallway still does hallway things around me."
        "People compare answers, complain about due process, ask whether the short response needed examples."
        "I hear due process and almost laugh, but the sound gets stuck somewhere under my ribs."
        "{i}Mom is going to hear about this.{/i}"
        "{i}Not vague hear about this. Not 'I got a bad score' hear about this.{/i}"
        "{i}Lawyer Mom, counselor Mom, cross-examination-over-breakfast Mom is going to hear that her honor student got pulled from an exam for cheating.{/i}"
        "The university page from Friday night surfaces without being asked."
        "Admissions. Merit scholarship. Optional portfolio statement that was not actually optional."
        "Every clean heading on that site suddenly has room for one dirty little asterisk."
        "{i}Does academic misconduct go on the internal record? Does the counselor see it? Does Monika hear before I can make my face normal?{/i}"
        "My lunch sits untouched in my lap until the packaging warms under my hands."
    else:
        "Lunch is not lunch so much as a scheduled decompression chamber."
        "The hallway outside the classroom has become a market for panic."
        "One classmate insists the due process question was a trick. Another claims every question is a trick if you are sufficiently unprepared."
        "{i}That philosophy belongs on a poster in the nurse's office.{/i}"
        "I eat near the windows and reread nothing."
        "Just food, water, and the faint ache in my fingers from writing too hard."
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_civics:
        nier "The afternoon bell arrives before I find a single sentence that would make any of this sound survivable."
        nier "Everyone returns to class carrying exam fatigue."
        nier "I return carrying something with teeth."
    else:
        nier "The afternoon bell cuts in and lunch never gets around to being useful."
        nier "Everyone returns to class let down, having genuinely believed forty minutes would restore a full human soul."
    call nier_clear from _call_nier_clear_0526_2
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("afternoon")
    stop music fadeout 1.0
    with wipeleft_scene
    play music quiz
    "Language arts waits for us in a fresh stack."
    $ exam_guard_checkpoint_or_jump("la", "exam_start", "a0526_la_save_scum")
    "The top page has a passage printed in neat columns, which means the exam is going to pretend to be literature before it becomes a knife."
    show japanese_teacher neut at t11
    japanese_teacher "Definitions are not enough. Explain what the technique makes the reader do."
    "Her gaze moves across the room."
    japanese_teacher "Begin."
    show japanese_teacher at thide
    hide japanese_teacher
    $ exam_guard_checkpoint_or_jump("la", "q1_open", "a0526_la_save_scum")
    "{i}Question 1. A narrator describes concrete actions while repeatedly omitting the actor responsible for them. What is the most likely effect?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "It proves the narrator is objective.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "No actor named, no opinion offered. Objective is what that looks like from a distance."
            "I mark it."
        "It forces the reader to participate in assigning agency.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "The action stays visible. Responsibility gets slippery."
            "{i}Device, pressure, meaning. Keep the chain intact.{/i}"
        "It removes all emotional tension from the passage.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Nothing in the sentence is doing anything to anybody. That reads as flat."
            "I mark it."
    $ exam_guard_checkpoint_or_jump("la", "q1_answered", "a0526_la_save_scum")
    "The passage itself is about a room after an argument."
    "Door open. Light off. A cup on the table."
    "Teachers truly love cups when they want guilt to look domestic."
    $ exam_guard_checkpoint_or_jump("la", "q2_open", "a0526_la_save_scum")
    "{i}Question 2. Which answer best describes an unreliable narrator?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "A narrator who uses first-person pronouns.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Every unreliable narrator I can name says I a lot. That has to count for something."
            "I mark it."
        "A narrator who tells the story in chronological order.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Order is the only structural word in the options, and this feels like a structure question."
            "I mark it."
        "A narrator whose account conflicts with evidence in the story.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "Not just someone who lies. Someone whose version cannot be trusted without checking the room around them."
            "{i}A little pointed, considering the room.{/i}"
    $ exam_guard_checkpoint_or_jump("la", "q2_answered", "a0526_la_save_scum")
    "My wrist starts complaining around the short-response section."
    "I rotate the pencil once and keep going."
    $ exam_guard_checkpoint_or_jump("la", "q3_open", "a0526_la_save_scum")
    "{i}Question 3. Which use of a recurring image best supports a theme?{/i}"
    $ atmos_pressure()
    with dissolve
    menu:
        "A locked door appears whenever characters avoid making a choice.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(True)
            with dissolve
            "A locked door that keeps appearing when people dodge decisions."
            "{i}A recurring image doing actual work.{/i}"
        "A blue curtain appears once because the room needed curtains.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "Curtains are the most famous symbol in the history of being made to read things."
            "I mark it."
        "A character names the theme directly in the final paragraph.":
            $ atmos_pressure_clear()
            $ s1_exam_mark(False)
            with dissolve
            "If the theme is stated outright, the theme is definitely supported. That feels almost too obvious to be wrong."
            "I mark it."
    $ exam_guard_checkpoint_or_jump("la", "q3_answered", "a0526_la_save_scum")
    "The final written response asks how the passage's restrained diction changes the reader's sympathy for the narrator."
    "My first draft of the answer is unusable, so I translate it into something a grader can accept."
label a0526_after_la:
    $ hide_calendar()
    scene black with wipeleft_scene
    if persistent.did_save_scum_civics or persistent.did_save_scum_la:
        nier "The second session ends, but the day does not."
        nier "That is the cruel part. School is very good at continuing after it has already ruined a person."
        if persistent.did_save_scum_civics and persistent.did_save_scum_la:
            nier "Two zeros. Two separate teachers. One day."
            nier "The number is so stupidly small that it starts looking unreal, like a typo in my life."
        else:
            nier "One zero sits at the edge of the day and makes every ordinary sound feel like it knows."
        nier "By the time I leave the classroom, I am already rehearsing explanations and rejecting all of them because each one sounds like a defendant trying to become a victim."
        nier "Mom told me Friday that consequences exist whether I feel ready or not."
        nier "I hate that my first instinct is to wonder whether she has case-law for being disappointed in your own kid."
    else:
        nier "The second session ends with less noise than the first."
        nier "By afternoon, everyone has learned that comparing answers only makes the day worse."
        nier "I leave the classroom with two subjects behind me and four more waiting patiently in line."
    call nier_clear from _call_nier_clear_0526_3
    if exam_guard_day_scummed("civics", "la"):
        call exam_guard_home_confrontation("May 26", "civics", "la") from _call_exam_guard_home_confrontation_0526
    if exam_guard_should_bad_end():
        jump exam_guard_bad_ending
    if persistent.exam_save_scum_subjects:
        pause 2.0
        scene bg bedroom_night
        $ show_calendar()
        $ atmos("home_night")
        stop music fadeout 1.0
        with wipeleft_scene
        play music hopeless
        "My room is still my room, but it does not feel like it belongs to me in the usual way."
        "No phone. No laptop upstairs. No casual little escape routes glowing from the desk."
        "Just the biology packet for tomorrow and the sound of the house continuing with one door closed."
        "I sit on the edge of the bed and do not open the packet right away."
        "The words from downstairs keep arriving late."
        "{i}Choice. Trust. Record.{/i}"
        "They do not become easier because I understand them."
        "A floorboard creaks in the hall."
        "For one second I think Mom has changed her mind and come upstairs to keep talking."
        "Instead, something small taps against the outside of my door."
        "A glass of water sits there when I open it."
        "No note."
        "No speech."
        "Just water, placed carefully enough not to spill."
        "{i}Asa.{/i}"
        "I stand in the doorway with the glass in my hand and listen to her door close softly across the hall."
        "The house gives me nothing else."
        "That is probably fair."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Monday ends with biology still waiting and no clean way to make tomorrow simple."
        nier "The only useful thing left is to take the next paper honestly."
        nier "Useful is not the same as enough."
        call nier_clear from _call_nier_clear_0526_4_scum
    else:
        pause 2.0
        scene bg corridor
        $ show_calendar()
        $ atmos("afternoon")
        stop music fadeout 1.0
        with wipeleft_scene
        play music fantasyserenity
        "The hallway after the first exam day has a strange, temporary looseness to it."
        "Nobody is free, not really."
        "There are still four exams ahead, and every backpack in sight looks heavier than it should."
        "But two papers are behind us now, and the building seems to know that counts for something."
        show monika forward uniform dist cm oe nobl rdown ldown at t11
        "Monika finds me near the stairwell with her folder hugged against her chest."
        m forward uniform curi om oe nobl rdown ldown "No answer autopsy?"
        mc "Absolutely not."
        m forward uniform happ cm ce nobl rdown ldown "Good."
        mc "That was a test, wasn't it?"
        m forward uniform happ om oe nobl rdown lpoint "A small one."
        mc "Cruel timing."
        "She smiles. The tiredness keeps it gentle."
        m forward uniform happ om oe nobl rdown ldown "Club room for a few minutes?"
        mc "I thought we were preserving brain function."
        m "We are."
        m forward uniform happ om oe nobl rhip lpoint "No exam talk for fifteen minutes."
        mc "That actually sounds useful."
        "We move with the thinning crowd."
        "A few people pass us still arguing about the language arts passage."
        "Monika and I both pretend we cannot hear them. It is a mercy, and we are the ones receiving it."
        $ hide_calendar()
        scene black with wipeleft_scene
        pause 2.0
        scene bg club_day
        $ show_calendar()
        $ atmos("afternoon")
        with wipeleft_scene
        play sound moddooropen
        show monika forward uniform dist cm oe nobl rdown ldown at t11
        "The rule is on the board exactly as promised."
        "{i}NO POSTMORTEMS FOR FIFTEEN MINUTES.{/i}"
        "Under it, Monika has written the start and end time in smaller letters."
        "The room is not empty, but the few people inside have accepted the rule with obvious relief, like they were all waiting for somebody else to say it."
        m forward uniform curi om oe nobl rhip ldown "No questions, no comparing, no trying to remember whether a word was in paragraph two or paragraph three."
        mc "What happens if someone breaks the rule?"
        m forward uniform happ cm oe nobl rhip ldown "They close their notebook and drink water."
        mc "Strict."
        m forward uniform happ cm ce nobl rdown ldown "Practical."
        "She sets her own water bottle on the nearest desk so the rule applies to her too."
        "For a few minutes, the club room manages exactly what the board asks."
        "Someone opens a manga and does not pretend it is review material."
        "Someone else puts their head down on folded arms."
        "She sits across from me, not quite smiling, not quite collapsing."
        "I almost mention the short response once."
        "Her eyes flick to the board, and I let the thought go."
        # SFX SUGGESTION: A restrained phone-timer buzz in the otherwise quiet club room.
        "By the time the timer on Monika's phone buzzes, none of us looks magically restored."
        "But the day has a small clean pocket in it."
        "That is enough."
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "The club room disperses before it can turn into another study session."
        nier "Monika waves from the hallway with the same tired softness she had at the library yesterday."
        nier "I leave with nothing solved, which is not the same as leaving empty-handed."
        call nier_clear from _call_nier_clear_0526_4
        pause 2.0
        scene bg dining_table_night
        $ show_calendar()
        $ atmos("home_night")
        stop music fadeout 1.0
        with wipeleft_scene
        play music dailyleisure
        "Dinner is ordinary in a way that feels deliberately constructed."
        "Mom makes rice, soup, and a pan of vegetables cut smaller than necessary because chopping gives her hands something practical to do."
        "Asahina appears halfway through setting the table, sees me place a glass on the wrong side of the plate, and silently fixes it."
        show mom determined at t21
        show asahina teasing at t22
        mom "No post-exam autopsies at the table."
        ah "What if the autopsy is funny?"
        show mom unamused
        mom "Especially then."
        mc "Strict household."
        show mom smug
        mom "Functional household."
        show asahina neut
        "Asahina sits and nudges the serving spoon toward me with her knuckles."
        ah "Did you live?"
        mc "Mostly."
        ah "Same."
        "That is all she offers. It is more than it sounds like."
        "Mom watches the exchange and decides not to press. She passes the soup instead."
        "For a while, dinner is only plates, steam, and the small negotiations of who gets the last piece of fried tofu."
        "Asahina wins because she grabs it while pretending not to."
        mc "Due process was not followed."
        show mom teasing
        mom "File an appeal after dishes."
        show asahina smug
        ah "The system works."
        "The joke works, gently, and goes nowhere else."
        "Nobody asks for scores that do not exist yet."
        "Nobody asks whether tomorrow will be worse."
        "Answering would not help."
        $ update_character_thought("monika", "Monika gave the room fifteen minutes of no exam talk, and that did more than another review sheet could have.")
        $ hide_calendar()
        scene black with wipeleft_scene
        nier "Monday night narrows down to sensible things."
        nier "Light review. Bag packed. Water bottle refilled because Coach, Mom, and apparently basic survival have reached consensus."
        nier "The first day of midterms is behind me. Tomorrow is science."
        call nier_clear from _call_nier_clear_0526_5
    $ exam_guard_clear_active_checkpoint()
    stop music fadeout 2.0
    pause 2.0
    call calendar_advance(days=1) from _call_calendar_advance_0526_1
    jump a0527

label a0526_civics_save_scum:
    $ exam_guard_mark_scummed("civics")
    $ calendar.set_date(2025, 5, 26)
    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    stop music fadeout 0.5
    with dissolve_scene_full
    play music safety
    show civics_teacher neut at t11
    civics_teacher "[player]."
    "Every pencil in the room seems to stop at once."
    "The teacher stands beside my desk with my answer sheet held low enough that no one else can read it."
    "That almost makes it worse."
    civics_teacher "Put your pencil down."
    mc "...Did I do something?"
    "My voice comes out too thin."
    "Not casual. Not even close."
    civics_teacher "Do not make this worse by asking me to pretend you do not understand procedure."
    "Her voice stays quiet, clipped and absolutely not for the rest of the class."
    civics_teacher "You are one of the students I expect to understand the difference between a bad answer and a dishonest one."
    civics_teacher "That expectation is why this is disappointing instead of merely annoying."
    "A few heads turn before people remember that staring at academic disasters is still staring."
    "Heat crawls up my neck."
    "For a second, I cannot find the classroom wall. Just faces, desks, the calendar overlay, and the fact that this is happening under my actual name."
    mc "...I'm sorry."
    "{i}Mom. Counselor. Honor status. Monika looking at me like she has to decide whether to ask what happened.{/i}"
    "{i}The thoughts pile up so fast they stop being thoughts and become weather.{/i}"
    civics_teacher "Apology noted."
    civics_teacher "It does not repair the trust you just asked this room to keep extending to you."
    "Her hand tightens on the answer sheet, briefly."
    civics_teacher "Zero for civics. Pencil down, eyes forward, no further discussion until the session ends."
    # SFX SUGGESTION: A sudden pencil slap against the desktop, loud in the exam silence.
    "My pencil hits the desk harder than I mean it to."
    mc "...Yes, ma'am."
    "{i}There it is.{/i}"
    "{i}Not a lecture. Not yelling. Just the sound of a door closing because I gave it a reason to.{/i}"
    "The room keeps going, and that's the part I cannot get past."
    "Pencils move. Someone two rows up turns a page. The clock ticks into the next minute like nothing in this one just ended."
    "I'm sitting in the exact seat I was in thirty seconds ago, back when I was still the person this didn't happen to."
    "There is no walking that back. No menu, no rewind, no last-second correction accepted. The version of me with a clean record is just...gone, and I am the one who deleted him."
    "{i}And behind it all, Friday night's college page quietly starts removing me from the photos.{/i}"
    "{i}One asterisk. That is all it takes. One word on a form, and every clean heading on that site grows a footnote with my name in it.{/i}"
    show civics_teacher at thide
    hide civics_teacher
    play music hopeless fadeout 1.0
    jump a0526_after_civics

label a0526_la_save_scum:
    $ exam_guard_mark_scummed("la")
    $ calendar.set_date(2025, 5, 26)
    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    scene bg class_day
    $ show_calendar()
    $ atmos("pressure")
    stop music fadeout 0.5
    with dissolve_scene_full
    play music safety
    show japanese_teacher neut at t11
    japanese_teacher "[player]."
    "Her voice is quiet enough that the whole room has to become quieter around it."
    japanese_teacher "Close the exam, please."
    "Please should soften it."
    "It does not."
    mc "...Why?"
    japanese_teacher "Because the answer in front of me has acquired a revision without time, process, or permission."
    "She does not look at the class."
    "She looks only at me, like the room is an annotation she refuses to let distract her from the sentence."
    if persistent.did_save_scum_civics:
        japanese_teacher "After this morning, I was hoping you would understand the shape of the problem."
        "My stomach drops so hard it feels physical."
        mc "I do."
        japanese_teacher "Then I need you to stop behaving as if understanding it privately changes the public fact."
    japanese_teacher "Last week, you gave a very good answer about agency."
    japanese_teacher "So I am not going to insult either of us by pretending the actor disappeared."
    mc "I..."
    "Nothing useful follows the word."
    "My hand is still near the pencil."
    "I pull it back like the object itself can testify."
    japanese_teacher "You know how evasion reads when someone has already left evidence on the page."
    japanese_teacher "That is what makes this so frustrating."
    "Frustrating comes out controlled, but not clean."
    japanese_teacher "Zero for language arts. We will discuss the rest after the session."
    mc "Is this going to the office?"
    "I ask before I can dress it up."
    "Her expression changes by exactly nothing."
    japanese_teacher "Yes."
    "A single word with nothing attached to it. It lands heavier than a whole paragraph would have."
    "{i}I spent an entire unit learning how a sentence can bury the person who acted, and I just proved I never understood any of it, because there's no grammar left anywhere that takes my name back off this one.{/i}"
    "{i}It goes to the office, and then it goes home, and there is no version of walking through my own front door tonight where I get to narrate my way out of it.{/i}"
    show japanese_teacher at thide
    hide japanese_teacher
    play music hopeless fadeout 1.0
    jump a0526_after_la
