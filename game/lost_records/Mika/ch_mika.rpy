# =============================================================================
# ch_mika.rpy  --  "MIKA: A DDLC SHORT STORY" (ORIGINAL RECORD)
#
# WHAT THIS FILE IS
#   The lost record as it was originally written in 2021, preserved unedited.
#   It is the "Original Record" entry in the Lost Records archive
#   (Lost Records View/lost_records.rpy -> ("Original Record", "ch_mika")).
#
#   ch_mika_rewrite.rpy holds the ground-up 2026 retelling of the same story.
#   The two are meant to be readable side by side, so DO NOT "fix" this file to
#   match the rewrite -- its rougher prose is the point of keeping both.
#
# WHAT IT DEPENDS ON
#   misc_variables.rpy    the mm character, monikayoung/mika sprites, mika_* BGM,
#                         SFX and backgrounds
#   mod_assets/MPT/*.rpy  the Monika Pose Toolkit layered images
#   mod_assets/poems_special.rpy  the one surviving special poem
#   mika_credits.rpy      the end-card, called at the end of the record
#
# ENDING
#   Falls through to mika_credits, which offers a full restart or a quit --
#   this record deliberately does not return to the archive.
# =============================================================================
label ch_mika:

    stop music
    window auto
    scene black
    pause 1.5
    scene mika_bg_park with dissolve_scene_full
    pause 0.5
    play music mika_a2

    "{i}*sigh*{/i} I love the park."
    "It's a great place to come to after school and just relax."
    "Whether it's playing with friends or looking around, there's lots of fun!"
    "I heard that the people here are going to build a new playground for us kids. I wonder what it will be like!"
    "I bet I will spend so many evenings on it with friends after we finish our phonics or math homework."
    "Speaking of friends, I was supposed to meet my friend here, but she's late for some reason..."
    "I just hope she didn't be a jerkwad and bail on me. She's been my friend ever since we started first grade, and that was three whole years ago."
    "That's, like, basically forever!"
    "She couldn't just hurt me like that, would she?"
    "I sit on the bench and watch people go by as I waited for her."
    "Some people brought their dogs here for walks... I love dogs!"
    "Anyway, since my friend is taking her time, I guess I can play on my GameLad..."
    play sound mika_footsteps
    pause 2.0
    "Hm? I see a girl walking towards me."
    "Oh... Never-mind the GameLad, my friend is finally here!"
    show monikayoung 3k at f11
    m "Hey, Mika!"
    show monikayoung 3j at t11
    mm "EEEEEEEE, MONIKA!!"
    stop sound fadeout 1.0
    show monikayoung 1n at f11
    m "Sorry that I'm late, I was doing something important."
    m "I was the one who wanted to play with you here, so I'm even more sorry."
    show monikayoung 1m at t11
    mm "It's okay, I forgive you."
    show monikayoung 1k at f11
    m "Yay!"
    show monikayoung 4b
    m "Anyways, did you hear about the playground being made?"
    show monikayoung 1a at t11
    mm "Yeah! Are you excited about it? There's gonna be swings, and slides, and jungle gyms, and monkey bars, and-"
    show monikayoung 1k at f11
    m "AAAAAAHHH, I CAN'T WAIT!"
    show monikayoung 1j at t11
    mm "AAAAAAHHHHHHH, SO EXCITING!"
    show monikayoung 1b at f11
    m "So, to celebrate, wanna play hide and seek?"
    show monikayoung 1a at t11
    mm "Heck yeah! Who's hiding first?"
    show monikayoung 2d at f11
    m "Hey, watch your mouth. My mom says that \"heck\" is a bad word..."
    show monikayoung 2c at t11
    mm "It is? Well, I guess I won't use it, then."
    mm "So, is it okay if I hide first?"
    show monikayoung 1k at f11
    m "Heck yeah! I'll lean against this tree and count to thirty!"
    show monikayoung 1j at t11
    mm "Hehe, you won't find me!"
    "I start to look for a good hiding spot..."
    mm "Wait a minute... You said-"
    show monikayoung 3k

    scene black with dissolve_scene_full
    stop music fadeout 1.5
    pause 1.25

    "I had a really fun afternoon with Monika. I was amazed by how fast she found me every time."
    "I gave up every time she hid. How does she do it?"
    "I'll have to ask her sometime. I'm really jealous of how she is so good at so many things."
    window hide
    play sound closet_open
    pause 1.0
    play sound closet_close
    pause 1.0
    scene mika_bg_house with wipeleft_scene
    window auto
    play sound mika_night
    "Nights at home are the worst..."
    "My mom is sitting on the couch watching TV as usual, and I can hear my dad snoring upstairs."
    "He's asleep at 21:00 just because he works night shifts. He can't make any time for his family..."
    "Well, anyway, I guess I'm gonna go up to my room and do something up there. Might watch YouToob videos or read a book..."
    "I dunno. Things just suck without Monika around."
    stop sound fadeout 2.0
    scene black with wipeleft_scene
    "As soon as I got to my room's door, there was a piece of paper taped onto it."
    "The writing on here is very funky..."

    window hide
    call mika_poem_special_2 from _call_mika_poem_special_2
    scene black with dissolve_scene_full
    pause 1.0
    stop sound
    show mika_splash_warning "The next evening..."
    pause 1.5
    scene black with dissolve_scene_full
    pause 0.5
    scene mika_bg_parknight with wipeleft_scene
    window auto
    pause 0.5
    play music mika_away

    "I love shopping at the mall with my mom! Today we picked up a couple bracelets, a new game for my GameLad, and my favorite thing in the whole wide world: ice cream!"
    "There's this one place that makes the best ice cream, but my mom always tells me it costs a lot..."
    "I thought parents had unlimited money?"
    "Anyway, It's about time we made our way home. It's already dark, and I hate the dark."
    play sound mika_footsteps
    "So many stores and places are still open..."
    m "Hellooooo...."
    show monikayoung 1k at hf11
    stop sound
    m "MIKA!"
    show monikayoung 1j at t11
    mm "AH!"
    mm "Monika! You scared me!"
    show monikayoung 1b at f11
    m "Sorry, sorry! It just seemed like the perfect chance."
    show monikayoung 1a at t11
    mm "What are you up to, anyway? I never see other kids in public."
    show monikayoung 4b at f11
    m "Just got some cupcakes. I have to show you the shop sometime. It's the best bakery in town."
    show monikayoung 4a at t11
    mm "Wow! I would love to go one day! I actually got some ice cream earlier, so we both ate good, huh?"
    show monikayoung 1b at f11
    m "I bet!"
    m "Say, I want to show you something tomorrow. It's such a cool gadget!"
    show monikayoung 1a at t11
    mm "I wanna see it, then! I'm sure it's really cool if my best friend has it!"
    "I wish I had cool stuff..."
    show monikayoung 1k at f11
    m "Hehe, I think you have cool stuff too, Mika!"
    "Hold on, how did she know what I was thinking?"
    m "Anyway, I wish I could stay longer, but I don't wanna keep my parents waiting."
    show monikayoung 1j at t11
    mm "Awww, okay..."
    mm "Well, I'll see you at school tomorrow, then!"
    show monikayoung 4k at f11
    m "Laters!"

    show monikayoung at thide
    hide monikayoung
    window hide
    pause 1.5
    window auto

    "Wow, she is a fast runner. I bet all the boys love her."
    "My mom just chuckles for some reason. I guess she's happy I have friends?"
    mm "Okay, mom, let's go home!"
    "My mom nods, still with a smile on her face."

    scene black with dissolve_scene_full
    stop music fadeout 1.5
    pause 1.25
    show mika_splash_warning "The next day after school..."
    pause 1.5

    scene mika_bg_stairs with dissolve_scene_full
    pause 0.5
    play sound mika_bell

    "So Monika wanted to meet me in the stairwell after class, and I'm the first one to show up...again."
    "I don't know if she has a habit of being late or what, but it gets annoying after so much."
    play sound mika_footsteps
    "At least she isn't running too late. I hear footsteps coming towards me."
    stop sound
    show monikayoung 1l at f11
    m "Haaaah..."
    "She seems out of breath."
    m "S-Sorry for being late. I had...had to talk with Mr. Parson for a second."
    m "I also brought the thing I wanted to show you."
    show monikayoung 1j at t11
    mm "Yes!!! Show me, show me!"
    show monikayoung 4i at f11
    m "Just to warn you, though... If you think it's weird, I don't blame you."
    show monikayoung 4h at t11
    mm "I promise I won't."
    show monikayoung 4i at f11
    m "Okay, here it goes..."
    show monikayoung at t11

    "...Huh? You mean it's not a {i}thing{/i}?"
    window hide
    $ consolehistory = []
    call updateconsole ("play sound fall") from _call_updateconsole_15
    play sound fall
    pause 0.5
    window auto
    mm "Oh no! I think I just heard someone fall!"
    mm "We need to check and see if they're-"
    show monikayoung 4b at f11
    m "Actually, I made that sound happen!"
    show monikayoung 4a at t11
    mm "...Huh?"
    show monikayoung 4b at f11
    m "See, I can put something in this little box here, and it makes something happen!"
    m "I actually sent you a spooky paper not too long ago, just to test it out."
    show monikayoung 4a at t11
    mm "THAT WAS YOU?!"
    mm "It scared me!"
    show monikayoung 4b at f11
    m "Eheheh..."
    m "I have no idea how it does that, but I got it the other day when I was talking with my dad."
    show monikayoung 4n
    m "I asked him about it, but he just laughed it off... I have no idea why."
    show monikayoung 4m at t11
    mm "Oh my gosh, Monika..."
    mm "Think about all the cool things we can do with that!"
    show monikayoung 4a
    mm "You could, like, make a million, no, a BILLION dollars with it!"
    mm "Or better yet, A BILLION CUPCAKES!!!"
    mm "Or....you could just erase all the annoying teachers!"

    window hide
    call updateconsole ("play music t6", "playing music t6") from _call_updateconsole_16
    play music t6
    $ pause(1.0)
    call updateconsole ("show monikayoung 4b at f11", "showing monikayoung 4b at f11") from _call_updateconsole_17
    show monikayoung 4b at f11
    window auto

    m "I know, right?! Some of these things, I don't even know what they mean, but they must be good!"
    m "It's like one of those games where you become a god and stuff!"
    m "When I got this power, I first thought, \"Is this real life?\" and was amazed!"
    show monikayoung 4d
    call hideconsole from _call_hideconsole_2
    scene black
    stop music
    play sound audio.mika_pound
    show white zorder 4:
        alpha 1.0
        linear 0.25 alpha 0.0
    pause 2.5
    m "..."

    mm "Monika?"
    m "Is this...real life...?"
    mm "Are you okay, Monika?!"
    m "Is this...real...life...?"
    mm "I mean, of course it is! Why would you think-"
    m "Is it..."

    window hide
    pause 2.0
    scene mika_bg_stairs
    show monikayoung 1q at f11
    show white zorder 4:
        alpha 1.0
        linear 0.25 alpha 0.0
    pause 2.0
    window auto
    m "..."
    show monikayoung at t11
    mm "..."
    show monikayoung 1r at f11
    m "Sorry, Mika, but I gotta go."
    m "I'll see you tomorrow."
    show monikayoung 1q at t11
    mm "Monika, wait-"

    show monikayoung at thide
    hide monikayoung
    window hide
    play sound closet_open
    pause 1.0
    play sound closet_close
    pause 1.5

    window auto
    "What was her deal there? That was not like Monika at all..."
    "That box thingy was cool, but now I'm worried about my friend..."

    scene black with dissolve_scene_full
    pause 1.0
    play music t10

    "After that day, Monika changed drastically."
    "So much so that she began to stop talking to me or hanging out with me."
    "I do not understand why she ceased her friendship with me, as I see no clear connection between the box and myself."
    window hide
    pause 1.0
    scene bg class_day
    show vignette zorder 4:
        alpha 1.0
    show monikayoung 1o at t11
    with dissolve_scene_full
    window auto
    "Starting the day after, she began to outright ignore me."
    scene black with dissolve_scene_full
    scene mika_bg_park
    show vignette zorder 4:
        alpha 1.0
    show monikayoung 1o at t11
    with dissolve_scene_full
    "Even when I invited her to the park, she barely spoke a word to me, nor was she active much if at all."
    scene black with dissolve_scene_full
    "Near the end of fourth grade, I finally laid it all onto her."
    scene mika_bg_stairs
    show monikayoung 1f at t11
    with dissolve_scene_full
    mm "I just don't get it... Why do you keep ignoring me?!"
    mm "I thought we were best friends, Monika!"
    show monikayoung 1p at f11
    m "..."
    m "I'm sorry."
    show monikayoung 1o at t11
    mm "Just tell me what's wrong! Please, I-I just want to help!!"
    "My eyes begin to tear up."
    show monikayoung 1p at f11
    m "...I doubt you'd understand, Mika."
    m "Just...I don't know, I can't explain it."
    m "Even though my heart is being ripped in two..."
    show monikayoung 1o at t11
    mm "But why, though?! You can tell me anything!"
    show monikayoung at f11
    m "..."
    show monikayoung at t11
    mm "I..."
    mm "I see how it is."
    mm "You're just done being friends with me, after three entire years."
    mm "IS THAT IT?!?!"
    show monikayoung 1p at f11
    m "I-"
    show monikayoung 1o at t11
    mm "Know what...? I don't care anymore."
    mm "If you don't wanna be friends anymore... If you don't trust me...then..."
    mm "THEN GOODBYE!!!"
    "I storm out of the school building, not being able to see because of my tears."

    scene black with wipeleft_scene
    pause 1.5

    "That was the first time I got upset at Monika."
    "That was the first time I hated Monika."
    "That was the first time I doubted Monika."
    "Even now, my blood boils just thinking about her."
    "Call it petty or trivial, but she was the best friend I ever had. Nobody else came close to the bond I shared with her."
    window hide
    pause 2.0
    window auto

    "A little over seven years later, we crossed paths again when we both joined the debate club."


    scene bg club_day
    show monika forward neut cm oe at t11
    with dissolve_scene_full


    show monika mh at f11
    m "Oh, are you here to join the debate club as well?"

    show monika md at t11
    mm "Yes. I've always had an interest in-"
    mm "Wait..."
    mm "Monika?"
    show monika mi at f11
    m "Yes, that is me. Do you know m-"
    show monika vsur om oe
    m "Hold on..."
    m "Mika?!"
    show monika cm at t11
    mm "It is you, then!"
    mm "Long time no see! How has it been?"
    show monika happ om oe at f11
    m "Pretty well, I would say. Still, though, things have also been sort of...bleh."
    show monika cm at t11
    mm "Well, that's great, I assume."
    mm "Say, do you still have that thing you showed me when we were kids?"
    show monika nerv om oe at f11
    m "Well, um...yeah? It's complicated, but, uh..."
    show monika cm at t11
    mm "I'll just get straight to the point:"
    mm "Are your demons still haunting you, whatever they are?"
    show monika flus om oe at f11
    m "Um..."
    m "Geez, why did you have to remind me...?"
    m "Is this really how reunions are supposed to go? I thought I finally moved past that..."
    show monika cm at t11
    mm "Come on, Monika, it's just a simple question."
    mm "I thought that we could rekindle our bond. To me, that starts with burying hatchets."
    show monika at f11
    m "..."
    show monika om
    m "I'm sorry, but I cannot tell you. It is for your sake, believe me."
    show monika cm at t11
    mm "I see..."
    mm "Guess it translates to \"I still don't want to be your friend, Mika.\""
    mm "It seems like we still haven't moved on from it, several years later."
    mm "A disappointment, really."
    show monika curi om oe at f11
    m "N-No, you have the wrong idea, that's not it at a-{nw}"
    show monika lsur cm oe at h11
    mm "Shut up."
    mm "I swear, Monika, that I will get a straight answer from you, even if it takes me all school year."
    mm "I would hate to get a bit forceful, but sometimes you gotta do what you gotta do."
    show monika om at f11
    m "And {i}I{/i} swear, Mika, that, again, I am only trying to protec-{nw}"
    show monika cm at h11
    mm "Stop talking."
    mm "I'm done arguing for today. Ironic that we're in the debate club room."
    show monika neut mi oe at f11
    m "Mika, please, you're being irrational. Just calm down and-"
    show monika cm at t11
    mm "Yeah, yeah, whatever."
    mm "See you, {i}best friend{/i}."

    scene black with dissolve_scene_full
    stop music fadeout 2.0
    pause 1.0
    scene bg corridor with dissolve_scene_full

    "And now we jump to the present."
    "February 3rd of my senior year. Not too long until graduation."
    "Right now, it's right before second period, and today feels like such a drag."
    "I casually walk across the hallway before I see a lone girl running and flailing her arms like a lunatic."
    n "Crap, crap, crap, I'm gonna be late to class...!"
    "She's, uh, not looking ahead of her."
    "Hold on..."
    "OH SH-{nw}"
    play sound audio.fall2
    show natsuki turned pani cm ce at s11
    show white zorder 4:
        alpha 1.0
        linear 0.25 alpha 0.0
    n "OW!"
    "The girl slams into me and knocks the two of us over."
    mm "Hey, what the hell?! Watch where you're going next time!"
    show natsuki pani cm oe at f11
    n "Oh my god, I am so sorry...!"
    n "Here, I'll help you pick up your things!"
    show natsuki at t11
    "The girl and I get on our feet and gather our belongings."
    mm "Say, what class are you even headed to?"
    show natsuki flus om oe at f11
    n "Social studies. The room is across the entire building, and I don't wanna be late for the fiftieth time."
    show natsuki cm at t11
    mm "Oh dear, that is quite the distance. From the looks of it, are you a first year?"
    show natsuki doub om oe at f11
    n "Senior, actually. Are you just assuming that because I look like a kid?"
    show natsuki cm at t11
    mm "W-Well, umm..."
    mm "Yeah."
    show natsuki rhip neut om oe at f11
    n "Eh, I don't blame you. My friends Monika and Yuri give me a hard time because of it."
    "Wait... What did you just say?"
    show natsuki cm at t11
    mm "Oh, you're friends with Monika? The one who quit the debate club to start her own?"
    show natsuki om at f11
    n "Yep, that's the one. What about it?"
    show natsuki cm at t11
    mm "Oh...I see. How quaint..."
    "This girl seems pretty unaware of the circumstances..."
    mm "What's your name, by the by?"
    $ n_name = "Natsuki"
    show natsuki om at f11
    n "Natsuki. What's yours?"
    show natsuki cm at t11
    mm "I'm Mika. Pleased to meet you, Natsuki."
    show natsuki happ om oe at f11
    n "Likewise, Mika!"
    show natsuki flus om oe
    n "At any rate, I should probably hurry to class, and so should you."
    show natsuki happ om oe
    n "So I'll see you around!"
    show natsuki cm at t11
    mm "See you!"
    show natsuki at thide
    hide natsuki
    window hide
    pause 1.5
    window auto
    "Natsuki, huh?"
    "So you're a friend of Monika's..."
    $ style.say_dialogue = style.normal
    "If I can't get the answer directly from Monika, I know what I must do, even if I dislike what I am thinking of doing..."
    $ style.say_dialogue = style.edited
    "{cps=10}Oh,{w=1.0} this is going to be a fun while."
    $ style.say_dialogue = style.normal

    scene black with dissolve_scene_full

    call mika_credits from _call_mika_credits
    return
