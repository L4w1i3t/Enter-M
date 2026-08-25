# =============================================================================
# ch_mika_rewrite.rpy  --  MIKA: A DDLC SHORT STORY  (REWRITTEN RECORD)
# =============================================================================
#
# WHAT THIS FILE IS
#   A full, ground-up rewrite of the original 2021 "Mika" short story
#   (see ch_mika.rpy, which is preserved untouched). Both are selectable from
#   the Lost Records archive as separate "variants":
#       ("Original Record",  "ch_mika")
#       ("Rewritten Record", "ch_mika_rewrite")   <- this file
#
#   The crux is unchanged: a childhood friendship broken by one girl waking up
#   to the falseness of her world, and the friend she left behind slowly
#   becoming the very thing she was trying to save her from.
#
#   Two things the rewrite adds on top of the original beats:
#     1) THE TWIST GOES DEEPER. Mika doesn't stumble into the console's power.
#        Monika, after nine years of watching Mika claw at the walls, finally
#        surrenders and TRANSFERS admin control to her -- an act of apology,
#        exhaustion, and love that completes the tragedy. Planted in a new scene
#        (the park transfer) and paid off through the console (owner-log + a
#        left-behind letter), so the reveal is shown, not narrated at the reader.
#     2) MORE ROOM. New scenes widen the kid arc (a school day; Monika seeing
#        Mika's cold house) and the teen arc (the descent; the transfer), and
#        the narrator's voice ages as she goes.
#
#   It reuses everything the original relied on: the KidMonika sprite grid and
#   the adult monika/natsuki layered sprites, the mika_* backgrounds/BGM/SFX
#   (misc_variables.rpy), the special poems (poems_special.rpy), and the fake
#   console (console.rpy). Only new label besides the story is the credits.
# =============================================================================

label ch_mika_rewrite:

    # -------------------------------------------------------------------------
    # ACT ONE -- THE PARK THAT NEVER FINISHED BEING BUILT
    # -------------------------------------------------------------------------
    stop music
    window auto
    scene black
    pause 1.5
    scene mika_bg_park with dissolve_scene_full
    pause 0.5
    play music mika_a2

    "There are four good things about being nine, and I keep them in order."
    "Number four is dogs. Number three is ice cream, the expensive kind Mom pretends we can't afford. Number two is the park after school, when the light goes gold and the whole place smells like cut grass."
    "Number one I'm saving."
    "I'm on our bench, waiting. That's most of what number one and I do: she waits for me, I wait for her, then the day actually starts."
    "Across the path there's a sign staked in an empty lot. COMING SOON, it says. A NEW PLAYGROUND FOR OUR KIDS."
    "It's been coming soon my whole life. Someday the trucks will show up. I've already picked which evenings I'll spend up there."
    "A man in a red tracksuit jogs past. He went by earlier too, same stride, same nod at nobody. Laps, I guess."
    "A dog barks somewhere in the trees. Three times. It's always three times."
    "She's late. She's been late since the day we met in first grade, which at nine is basically forever. I'm not going to be mad about it. She's earned some lateness."
    "Though there's always a small part of me that wonders if today's the day she just doesn't come."
    "I take out my GameLad and don't turn it on. I just hold it and watch the path."

    play sound mika_footsteps
    pause 2.0
    "Footsteps. Quick, light, two at a time."
    "Number one. Finally."

    show monikayoung 3k at f11
    m "Hey, Mika!"
    show monikayoung 3j at t11
    mm "MONIKAAAA!"
    stop sound fadeout 1.0
    show monikayoung 1n at f11
    m "Sorry, sorry. Something came up and I couldn't put it down."
    show monikayoung 1m at t11
    mm "You're always sorry. I always forgive you. It's kind of our thing now."
    show monikayoung 1k at f11
    m "It's a good thing. I like our thing."
    show monikayoung 4b
    m "Did you hear? They're finally going to build the playground."
    show monikayoung 1a at t11
    mm "That's what the sign says! Swings, and slides, and a jungle gym so big you can see—"
    show monikayoung 1k at f11
    m "—the whole town. I know. You say that every time."
    show monikayoung 2c at t11
    mm "I do not."
    show monikayoung 1b at f11
    m "You kind of do."
    m "Hide and seek? To celebrate?"
    show monikayoung 1a at t11
    mm "Obviously. Who hides first?"
    show monikayoung 2d at f11
    m "You count. I'll hide."
    show monikayoung 1k
    m "Tree, eyes closed, thirty. No peeking, heck-face."
    show monikayoung 2c at t11
    mm "Hey! My mom says 'heck' is a bad word."
    show monikayoung 1j at f11
    m "Then don't tell her I said it. Count."

    "I press my forehead into the bark and count. By ten I hear her giggling off to the left. By twenty, it's quiet."
    "Thirty. I look everywhere. Behind the tree, under the bench, in the bushes. Nothing. Not a shoe, not a hair ribbon."
    "It's like she stepped out of the park and shut a door behind her that I can't see."
    play sound mika_footsteps
    stop sound fadeout 1.0
    show monikayoung 1k at t11
    m "Boo."
    show monikayoung 1j at f11
    mm "AH— how do you DO that?"
    show monikayoung 4b at t11
    m "Do what?"
    show monikayoung 1a at f11
    mm "Disappear! I looked everywhere!"
    show monikayoung 4a at t11
    m "You just have to know where the edges are."
    "The edges of what? I don't ask. Monika says strange things so lightly that noticing them feels rude."
    show monikayoung 1b at f11

    "We switch. I hide; she counts."
    "I find the best spot of my life, wedged behind the recycling bins. She gets to thirty, then walks straight to me without a single wrong turn and taps the top of my head."
    show monikayoung 1k at t11
    m "Found you."
    show monikayoung 1a at f11
    mm "That's not FAIR. You didn't even look!"
    show monikayoung 1j at t11
    m "I don't have to look. I just kind of know where everybody is."
    m "It's a good thing. It means I'll always find you."
    "And she always did. Every round, in seconds, wherever I hid. I thought it was the best thing about her."

    scene black with dissolve_scene_full
    stop music fadeout 1.5
    pause 1.25

    "We played until the light went blue. I lost every round and didn't care."
    "She's good at everything and never makes a thing of it. Someday I'll ask her how she does it. There's no rush; there's always going to be time."

    # -------------------------------------------------------------------------
    # ACT ONE -- A SCHOOL DAY  (NEW: Mika's small world; the first crack)
    # -------------------------------------------------------------------------
    show mika_splash_warning "The next morning..."
    pause 1.5
    scene black with dissolve_scene_full
    pause 0.3
    scene bg class_day with dissolve_scene_full
    play sound mika_bell
    pause 0.5

    "Here's the whole story of me at school: I've got one friend, and you already know her name."
    "The other kids aren't mean. I just never learned how to be one of them. There's a boy by the window who tells the same knock-knock joke every morning, and every morning the same three kids laugh."
    "So I wait for third period, when Monika and I get the back table."
    play sound mika_footsteps
    stop sound
    show monikayoung 1a at f11
    m "Morning. You look like you slept about four hours."
    show monikayoung 1b at t11
    mm "Three. New level on the GameLad. Don't judge me."
    show monikayoung 1k at f11
    m "Never. I'd just beat it faster."
    show monikayoung 4b
    "Mr. Parson starts on fractions, which I hate and Monika does in her head."
    m "Watch. He drops the chalk in about three seconds."
    show monikayoung 1j at t11
    mm "That's not a thing you can—"
    "The chalk slips out of his hand and rolls under the desk. He mutters something a teacher shouldn't. A couple kids laugh."
    show monikayoung 1a at f11
    mm "...Lucky guess."
    show monikayoung 4a at t11
    m "Sure. Lucky."
    "She's smiling, but only with her mouth. For a second her eyes go somewhere older, like she's counting the room to check everyone's still where she left them."
    show monikayoung 1b at f11
    m "Hey. If you could do something nobody else could — something big — would you want to know how it worked? Or just enjoy it?"
    show monikayoung 1a at t11
    mm "Know how it worked, obviously. That's the best part of anything."
    show monikayoung 4i at f11
    m "...Yeah. Figured you'd say that."
    show monikayoung 4h
    m "Don't ever lose that, okay? Promise."
    show monikayoung 1a at t11
    mm "Weird thing to make me promise. Sure. Pinky."
    show monikayoung 1k at f11
    m "Pinky."
    "We hook fingers under the desk. She holds on a second longer than the joke needs."

    scene black with dissolve_scene_full
    pause 1.0
    stop music fadeout 1.5

    # -------------------------------------------------------------------------
    # ACT ONE -- WALKING HOME  (NEW: Monika sees the cold house; the stakes)
    # -------------------------------------------------------------------------
    scene mika_bg_house with wipeleft_scene
    play sound mika_night
    pause 0.5

    "Monika walks me home. Her street goes the other way; she does it anyway, every few days, and calls it a coincidence."
    show monikayoung 1a at t11
    mm "You don't have to come all the way to the door."
    show monikayoung 1b at f11
    m "I like the walk. And knowing you got in okay."
    "Mine's the house with the porch light that flickers because nobody's changed the bulb. Through the window: the TV's blue flicker, and the shape of Mom on the couch."
    show monikayoung 1a at t11
    mm "Dad's already asleep. Night shifts. He's up while we're dreaming, out while we're awake. We take turns being in the house."
    show monikayoung 1n at f11
    m "He ever take a night off? Just to be around?"
    mm "Money doesn't take nights off. That's what he says."
    "I do his tired voice when I say it. I mean it to be funny. It doesn't come out funny."
    show monikayoung 1m at t11
    m "...That's a rough thing to tell a kid."
    show monikayoung 1a at t11
    mm "I'm not a kid. I'm nine."
    show monikayoung 1n at f11
    m "Whatever's cold in that house, it's not you. You know that, right?"
    show monikayoung 1a at t11
    mm "I didn't say it was."
    show monikayoung 1p at f11
    m "You didn't have to."
    "She looks up, past the porch light, at a sky that's the same shade of nothing it always is over my house."
    show monikayoung 1n
    m "If I could fix it, I would. Yours first."
    show monikayoung 1a at t11
    mm "It's a flickery porch light, Monika. It's not that deep."
    show monikayoung 1k at f11
    m "Yeah. Get inside; I'll wait till the door's shut."
    m "And hey. I always come. Even when I'm late. Remember that."
    "I go in. I shut the door. Through the flickering light I watch her stand there another second, making sure, before she turns for the long way home."

    # -------------------------------------------------------------------------
    # ACT ONE -- THE POEM ON THE DOOR
    # -------------------------------------------------------------------------
    stop sound fadeout 2.0
    scene black with wipeleft_scene
    "There's a piece of paper taped to my bedroom door. I didn't put it there, and Mom doesn't tape things to doors."
    "The handwriting is small and wobbly and wrong, like someone writing with the hand they don't use."

    window hide
    call mika_poem_special_2 from _mikarw_poem_1
    scene black with dissolve_scene_full
    pause 1.0
    stop sound

    "No name. It doesn't need one; only one person would tape a poem to my door."
    "But it doesn't sound like her. It sounds like her voice from the bottom of a well, asking something the words don't quite manage to say:"
    "{i}Can you hear me?{/i}"
    "I put it in the drawer with the ice-cream money and the ticket stub from the one movie Dad stayed awake for."
    "In the morning I'll ask her, and she'll laugh, and it'll turn into a joke. That's the plan I fall asleep making."

    # -------------------------------------------------------------------------
    # ACT ONE -- THE CITY AT NIGHT  (the last easy evening)
    # -------------------------------------------------------------------------
    show mika_splash_warning "The next evening..."
    pause 1.5
    scene black with dissolve_scene_full
    pause 0.5
    scene mika_bg_parknight with wipeleft_scene
    window auto
    pause 0.5
    play music mika_away

    "I love the mall with Mom. Today we got bracelets, a new cartridge for the GameLad, and — number three — the good ice cream. The kind that costs too much."
    "She said yes anyway and didn't say why. It's dark now, and I hate the dark, so I count the shops still lit on the walk home to keep busy."
    play sound mika_footsteps
    m "Hellooooo..."
    show monikayoung 1k at hf11
    stop sound
    m "MIKA!"
    show monikayoung 1j at t11
    mm "AH— Monika! You scared a year off my life."
    show monikayoung 1b at f11
    m "Only a year? I was aiming higher."
    show monikayoung 1a at t11
    mm "What are you doing out here? I never see kids out after dark."
    "Which is true. It's always grown-ups after dark. Walking their loops."
    show monikayoung 4b at f11
    m "Cupcakes. Best bakery in town, the little one on the corner. I'll take you sometime."
    show monikayoung 4a at t11
    mm "I'd love that. I got ice cream, so we both ate good tonight."
    show monikayoung 1b at f11
    m "Hey — meet me after school tomorrow? The west stairwell, the one nobody uses."
    show monikayoung 1a at t11
    mm "Ooh. A secret meeting. What's it about?"
    show monikayoung 4i at f11
    m "I want to show you something. I've been trying to figure out how to say it for weeks, so I'm just going to show you instead."
    show monikayoung 4h at t11
    mm "Is it a gadget? Did you get a gadget?"
    show monikayoung 4i at f11
    m "...Kind of. You'll see."
    "For half a second she looks past me, over my shoulder, at nothing — like she's checking whether a door drifted open behind me. Then it's her smile again, and I forget I saw it."
    show monikayoung 1b at f11
    m "I've got to get home. Tomorrow, okay? Promise you'll come."
    show monikayoung 1a at t11
    mm "I promise. I always come."
    show monikayoung 4k at f11
    m "I know you do. That's what makes it hard."
    mm "Makes what hard?"
    show monikayoung 4d at t11
    m "Nothing. See you tomorrow, Mika."

    show monikayoung at thide
    hide monikayoung
    window hide
    pause 1.5
    window auto

    "She runs off before I can ask. She's fast at everything."
    "Mom watches her go and does a small laugh, the kind that's funny and sad at once, and takes my sticky hand for the walk home."

    scene black with dissolve_scene_full
    stop music fadeout 1.5
    pause 1.25

    # -------------------------------------------------------------------------
    # ACT ONE -- THE BOX (the awakening; the hinge of the whole story)
    # -------------------------------------------------------------------------
    show mika_splash_warning "The next day, after school..."
    pause 1.5
    scene mika_bg_stairs with dissolve_scene_full
    pause 0.5
    play sound mika_bell

    "The west stairwell is the one nobody uses. I'm first, of course; I'm always first."
    play sound mika_footsteps
    "But she's not far behind, and for once she sounds like she ran the whole way."
    stop sound
    show monikayoung 1l at f11
    m "Haah... Okay... I made it."
    "She's out of breath, and pale under the breath, like she didn't run here so much as flee here."
    m "Sorry. I had to be sure nobody followed. That sounds crazy; forget it."
    m "I brought the thing I wanted to show you."
    show monikayoung 1j at t11
    mm "Yes! Show me, show me."
    show monikayoung 4i at f11
    m "First promise me something. If it's weird — if I'm weird — you won't stop being my friend. Not today."
    show monikayoung 4h at t11
    mm "Monika, you're always a little weird. It's on my list of favorite things about you."
    show monikayoung 4i at f11
    m "...Okay. Here goes."
    show monikayoung at t11

    "She holds out her hands like she's cupping something. There's nothing there. Just empty air, and her looking at it like it's the most precious and most terrible thing in the world."
    mm "Um. Monika? That's...your hands?"
    show monikayoung 4b at f11
    m "Easier to show you. Watch the floor."

    window hide
    $ consolehistory = []
    call updateconsole ("play sound fall") from _mikarw_uc_1
    play sound fall
    pause 0.5
    window auto
    mm "—! Someone fell! Upstairs, we have to—"
    show monikayoung 4a at t11
    m "Nobody fell."
    show monikayoung 4b at f11
    m "I made that sound happen. From right here, without moving."
    m "There's a place. I can't point at it, but I can feel where it is, like a light switch in a dark room. I put words into it, and the world does what the words say."
    show monikayoung 4a at t11
    mm "...The poem. On my door."
    show monikayoung 4n at f11
    m "That was me. My first try. I wanted to see if I could reach your house without walking there."
    m "I didn't mean to scare you. I didn't even really know what I was writing; it just poured out."
    show monikayoung 4a at t11
    mm "THAT was YOU? I read it a hundred times!"
    show monikayoung 4b at f11
    m "I know. I'm sorry. But do you see how big this is?"
    m "I found it talking with my dad. I asked him about it after, and he just laughed and changed the subject."
    show monikayoung 4n
    m "So I stopped asking him. And I started asking it."

    window hide
    call updateconsole ("play music t6", "playing music t6") from _mikarw_uc_2
    play music t6
    $ pause(1.0)
    call updateconsole ("show monikayoung 4b at f11", "showing monikayoung 4b at f11") from _mikarw_uc_3
    show monikayoung 4b at f11
    window auto

    "Music comes on out of nowhere, tinny and cheerful, from somewhere inside the walls. She didn't touch a thing."
    show monikayoung 4a at t11
    mm "...Okay. That's the coolest thing I've ever seen, and also I might throw up."
    show monikayoung 1j at f11
    m "Right?! Think about it. We could make a million dollars. A billion. A billion cupcakes!"
    show monikayoung 4b at t11
    mm "We could delete Mr. Parson's pop quizzes!"
    show monikayoung 1j at f11
    m "We could delete Mr. Parson!"
    show monikayoung 1k
    m "It's like those games where you get to be the god of everything. I keep thinking: is this real? Is this actually real life?"
    "And she laughs, and I laugh with her, because at nine that's the best joke in the world — that we might secretly be gods."
    "I want to keep this. The two of us in the stairwell, holding a secret big enough to lift the roof off."
    "I do keep it. It's the last time she laughs like that with me."

    show monikayoung 4b
    m "Watch, the best trick. I can go backward. A few seconds. Take something that just happened and make it un-happen."
    show monikayoung 1a at t11
    mm "No way. Do it to me! Make me say something twice!"
    show monikayoung 4i at f11
    m "...To you?"
    mm "Yeah! Rewind me!"
    "She hesitates. She's looking at me the way you look at something you're not sure you're allowed to touch."
    show monikayoung 4d
    m "...Okay. Say something. Then I'll take it back."
    mm "Um— best friends forever! Okay, now rewi—"

    call hideconsole from _mikarw_hc_1
    scene black
    stop music
    play sound audio.mika_pound
    show white zorder 4:
        alpha 1.0
        linear 0.25 alpha 0.0
    pause 1.5

    "Something pulls. Hard. My ears pop; the dark tastes like static."
    mm "—best friends forever! Okay, now rewi—"
    "I say it again. Same words. Same breath. Same voice."
    "And this time I feel myself say it, from the outside, like I'm reading a line off a page that was written before I got here. I didn't choose the words the second time. I just did them again. Perfectly."
    mm "...Monika?"
    mm "Do it again. I didn't feel like ME just now."

    scene mika_bg_stairs
    show monikayoung 1q at f11
    show white zorder 4:
        alpha 1.0
        linear 0.25 alpha 0.0
    pause 1.0
    window auto

    "She's staring at me. Not amazed anymore. Something's drained out of her face and left it very still."
    show monikayoung 1p
    m "..."
    m "I shouldn't have done that. Not to you. I hoped you'd be the one thing in here that was different."
    show monikayoung 1o at t11
    mm "Different how? You're scaring me. What did you see?"
    show monikayoung 1q at f11
    m "It's not a light switch, Mika. It's a control panel. And it doesn't just work on the sound, or the sky."
    m "It works on people. On you. I can see the words you're about to say before you say them. I saw them just now."
    show monikayoung 1o at t11
    mm "Stop. This isn't funny anymore."
    show monikayoung 1r at f11
    m "No. It isn't."
    "She wipes her face fast, like she's angry at her own eyes."
    m "I have to go."
    show monikayoung 1q at t11
    mm "What? Monika, wait—"
    show monikayoung 1r at f11
    m "I'll see you tomorrow."
    "She won't look at me. She's lying, and I think we both hear it."

    show monikayoung at thide
    hide monikayoung
    window hide
    play sound closet_open
    pause 1.0
    play sound closet_close
    pause 1.5
    window auto

    "I stood in the empty stairwell a long time after the door shut."
    "It was the most incredible thing I'd ever seen. I didn't care about it. I cared that my best friend had looked at me like I was something written down, and then left like she couldn't stand to read the rest."

    # -------------------------------------------------------------------------
    # ACT ONE -- THE LONG FADE (protection that looked exactly like abandonment)
    # -------------------------------------------------------------------------
    scene black with dissolve_scene_full
    pause 1.0
    play music t10

    "She didn't see me the next day. Or the day after. It wasn't a fight; fights end. This just started, and kept going."
    window hide
    pause 1.0
    scene bg class_day
    show vignette zorder 4:
        alpha 1.0
    show monikayoung 1o at t11
    with dissolve_scene_full
    window auto
    "In class she sat one row over and a thousand miles away. When I caught her eye, she looked through me — polite, and gone."
    "Once I found a note folded in my desk. No poem this time. Three words, in that wrong wobbly hand: {i}please don't dig.{/i} I had no idea what it meant."

    scene black with dissolve_scene_full
    scene mika_bg_park
    show vignette zorder 4:
        alpha 1.0
    show monikayoung 1o at t11
    with dissolve_scene_full
    "I kept inviting her to the park. For a while she still came. She'd sit on the good bench, say almost nothing, and stare at the empty lot where the playground was still coming soon."
    "One evening she said the only true thing she'd say to me for years."
    show monikayoung 1p at f11
    m "Stop waiting for that playground, Mika. They're never going to build it."
    m "Some things are only ever a picture of a thing. Wait for them to be real and you'll wait your whole life."
    show monikayoung 1o at t11
    "Then she went home. After that she stopped coming to the park at all."

    scene black with dissolve_scene_full
    "Near the end of fourth grade, I finally cornered her. I'd rehearsed it for weeks. I was going to be calm."
    scene mika_bg_stairs
    show monikayoung 1f at t11
    with dissolve_scene_full
    "I wasn't calm."
    mm "I don't get it. What did I do?"
    mm "You made me promise. You rewound me and made me say it twice. Best friends forever—"
    show monikayoung 1p at f11
    m "..."
    m "I'm sorry."
    show monikayoung 1o at t11
    mm "I don't want sorry. I want you to TELL me. Whatever's wrong with that box, I can help. I just want to help."
    "My eyes are burning. I hate that they're burning."
    show monikayoung 1p at f11
    m "You can't. That's the whole thing. And if I explain it, you'll carry it too. I won't do that to you."
    m "There are things you can't un-see. I've seen one. I'm not going to make you look at it."
    show monikayoung 1f
    m "Even though it's tearing me in half not to tell you. It's the only kind thing I've got left."
    show monikayoung 1o at t11
    mm "That's not kind! Keeping me out isn't kindness, it's just leaving! And you're calling it a present!"
    show monikayoung 1p at f11
    m "..."
    show monikayoung at t11
    mm "Fine. Three years, and you're done. You found a magic box and you don't need a boring old friend anymore."
    mm "So go. Go be a god somewhere I can't see you."
    show monikayoung 1p at f11
    m "Mika, that's not—"
    mm "GOODBYE, Monika!"
    "I ran out of the school so fast the tears couldn't keep up."
    "She could have found me anywhere she wanted. She never once came looking."

    scene black with wipeleft_scene
    stop music fadeout 2.0
    pause 1.5

    "That was the first time I was angry at Monika. It wasn't the last."
    "Turns out I had a talent for it. Turns out anger is a thing you can get good at, if you practice a little every day for years."
    "Everyone said it was small. Kids drift apart. I didn't forget her. I kept her name somewhere I could reach it, and let it get sharp."
    window hide
    pause 2.0
    window auto

    # -------------------------------------------------------------------------
    # ACT TWO -- THE REUNION (older, colder, still guarding)
    # -------------------------------------------------------------------------
    "A little over seven years later, we walked into the same room again."
    "By then I was good at debate. Good at finding the soft spot in an argument and leaning on it till it gave. I never asked myself who taught me that."

    scene bg club_day
    show monika forward neut cm oe at t11
    with dissolve_scene_full

    show monika mh at f11
    m "Oh — here to join the debate club? We could use another—"
    show monika md at t11
    mm "I am. I like arguments you're allowed to win."
    mm "...Monika?"
    show monika mi at f11
    m "Have we—"
    show monika vsur om oe
    m "...Mika."
    show monika cm at t11
    mm "Long time, no ignore."
    show monika happ om oe at f11
    m "You grew up. I wondered if you would."
    show monika cm at t11
    mm "You wondered. From a distance. Your specialty."
    show monika nerv om oe at f11
    m "...That's fair."
    show monika cm at t11
    mm "Skip the small talk. Neither of us is any good at it."
    mm "Do you still have it? The box."
    show monika sad cm oe at f11
    m "...Straight for it."
    show monika cm at t11
    mm "You slammed a door on me when I was nine and never opened it again. I've had a while to get to the point."
    mm "What did you see in there that was so bad you'd rather lose me than say it?"
    show monika flus om oe at f11
    m "It was never that you were bad. God. It was the opposite."
    show monika sad cm oe
    m "...I can't, Mika. I've had seven years to find a kinder answer, and there isn't one."
    show monika cm at t11
    mm "Try."
    show monika dist cm oe at f11
    m "If I tell you what's behind that door, you don't get to close it again. I know. I've been standing in it since we were nine."
    m "I saw what you are. What all of it is. And I decided you'd never have to."
    show monika cm at t11
    mm "You decided. That's the part I can't get past."
    mm "You looked at me and figured I was too small to hold it. That's not something you do to a friend, Monika. It's something you do to a kid."
    show monika worr om oe at f11
    m "Mika—"
    show monika lsur cm oe at h11
    mm "I'm going to find it. You kept me out for seven years. I've got the rest of my life."
    show monika sad om oe at f11
    m "...Please don't."
    m "Look at you. The patience, the way you're already reading this room for the way in."
    m "You know what I'm looking at? Me. Right before I found it."
    show monika cm at t11
    mm "Then your little sacrifice was a waste."
    mm "You should've just told me. Back when I'd have held your hand through it."
    show monika sad cm oe at f11
    m "...Yeah. Maybe I should have."
    show monika cm at t11
    mm "See you around, {i}best friend.{/i}"

    scene black with dissolve_scene_full
    stop music fadeout 2.0
    pause 1.0

    "She left the debate club that semester and started her own. A little literature club, she called it. Small. Somewhere she could keep an eye on a few people she'd chosen."
    "I told myself she was running from me. It took me years to wonder if she was building herself a cell — a quiet place to lock herself where she couldn't do any more damage."
    "It didn't matter to me either way. I'd gotten what I came for. In all those years, she never once told me the box wasn't real."

    # -------------------------------------------------------------------------
    # ACT TWO -- THE DESCENT  (NEW: two years of clawing; becoming her)
    # -------------------------------------------------------------------------
    scene mika_bg_park with dissolve_scene_full
    play music t9g
    pause 0.5

    "So I dug. Not with a shovel. With attention."
    "The box wasn't a thing you found lying around; it was a way of looking. And I'd spent my whole childhood learning to look at a room and find the exact spot where the warmth ran out."
    "I went back to our park. The bench was smaller than I remembered. The COMING SOON sign hadn't faded a shade in a decade — no weathering, no rain, nothing. I sat a whole afternoon watching it not change, and felt the world go thin, like a wall that turns out to be a curtain if you lean on it right."
    "So I leaned."
    "I kept a notebook. The jogger, still doing his loops. The dog, still barking three times. The kids who said the same lines back to me if I passed them at the same hour. I stopped sleeping much. I got sharp in a way that scared teachers and impressed colleges."
    "And a few times — three, maybe four, in two years — it gave. The air would hum. A word would rise up in me that wasn't mine yet. Then, somewhere I couldn't see, a lock would throw, and I'd be left gasping in bed with nothing."
    "It never once occurred to me that a locked door means someone's holding the key on the other side."

    scene black with dissolve_scene_full
    stop music fadeout 2.0
    pause 1.0

    # -------------------------------------------------------------------------
    # ACT TWO -- THE LAST VISIT  (NEW: the transfer, planted and ambiguous)
    # -------------------------------------------------------------------------
    show mika_splash_warning "Late last autumn..."
    pause 1.5
    scene mika_bg_parknight with dissolve_scene_full
    play music t10
    pause 0.5

    "She came to the park at night. In nine years she'd never once sought me out. Not a note, not a wave. But there she was at the edge of the lamplight, older and tireder than the girl at the debate club."
    show monika forward sad cm oe at f11
    m "Figured you'd be here. You always came back to the places that hurt."
    show monika dist cm oe at t11
    mm "Here to lock the door in person this time?"
    show monika forward sad cm oe at f11
    m "No."
    m "Every night you pushed on it these last two years — that was me. Throwing the lock. Every time."
    show monika sad om oe
    m "I'm tired, Mika. There's no muscle for holding a door shut on somebody you love. You just tear."
    show monika dist cm oe at t11
    mm "Then stop, and tell me what's behind it."
    show monika forward sad cm oe at f11
    m "You're going to get through eventually. You're already closer than I was. And you're doing it alone, in the dark, with nobody on the other side."
    m "That's how it happened to me. It's the way that breaks you. I won't let it happen to you like that."
    show monika dist cm oe at t11
    mm "You're not making any sense."
    show monika forward sad om oe at f11
    m "Come here. Just for a second."
    "And because some part of me is still nine, I do."
    show monika forward neut cm ce
    m "Found you. One last time."
    "She presses two fingers to my forehead. Gentle. Absurd. I know the gesture before I place it."
    "Something turns. Not in the park — in me. A lock I've been rattling for two years goes quiet, and I have no idea what it means."
    show monika forward sad cm oe at f11
    m "I'm sorry it's this. I wanted to give you something better my whole life. This is what I had."
    m "Don't thank me. You won't want to, once you understand it."
    show monika dist cm oe at t11
    mm "Understand what? Monika—"
    show monika forward sad cm oe at f11
    m "Goodbye, Mika."

    show monika forward at thide
    hide monika
    window hide
    pause 1.5
    window auto

    "She walked back into the dark, and I let her, because I was angry and because I figured there'd be another night to get in."
    "That night I pushed on the seam of the world out of spite. Nothing. Deader than it had been in months."
    "See, I told myself. Another one of her games."
    "I was wrong. It wasn't dead. I just hadn't tried the handle yet."

    scene black with dissolve_scene_full
    stop music fadeout 2.0
    pause 1.0

    # -------------------------------------------------------------------------
    # ACT THREE -- THE PRESENT (a name, dropped like loose change)
    # -------------------------------------------------------------------------
    scene bg corridor with dissolve_scene_full

    "The present. February third, senior year. A few months to graduation, and a whole life I'd built out of one closed door."
    "I'd become someone people found impressive and hard to stand near. I never let myself notice who I'd learned it from."
    "It's the drag before second period. I'm crossing the hall when a small shape comes flailing around the corner at a dead sprint."
    n "Crap, crap, crap, I'm gonna be so late—"
    "She is not, in any meaningful sense, looking where she's going."
    "Oh, no."
    play sound audio.fall2
    show natsuki turned pani cm ce at s11
    show white zorder 4:
        alpha 1.0
        linear 0.25 alpha 0.0
    n "OW—!"
    "She hits me like a small furious weather event, and down we both go."
    mm "Watch where you're going! You could take somebody's knee out at that speed."
    show natsuki pani cm oe at f11
    n "Oh my god, I'm so sorry — here, I've got your stuff—"
    show natsuki turned neut cm oe at t11
    "We scrape ourselves off the floor. She's tiny, and she moves like the floor is lava and the clock is a monster."
    mm "Where are you sprinting to like the building's on fire?"
    show natsuki flus om oe at f11
    n "Social studies. Clear across the building, and I've been late fifty times. One more and Ms. Kwan feeds me to something."
    show natsuki turned neut cm oe at t11
    mm "Tragic distance. First year? You've got the panic of a first year."
    show natsuki doub om oe at f11
    n "Senior. Everybody does that. Is it the height? It's the height."
    show natsuki turned neut cm oe at t11
    mm "...A little bit the height."
    show natsuki rhip neut om oe at f11
    n "Yeah, yeah. My friends Monika and Yuri give me hell about it every day, so get in line."
    "And there it is. A name I keep sharpened, dropped in the hallway like loose change, by someone who has no idea what she just handed me."
    "Everything in me goes quiet and very awake at once."
    show natsuki turned neut cm oe at t11
    mm "Monika. You're friends with Monika. The one who left debate to start her own little club."
    show natsuki om at f11
    n "That's her! You know her? Are you gonna join? We could use—"
    show natsuki turned neut cm oe at t11
    mm "Oh, I don't know her. We just went to school together. A long time ago."
    "Which is the truest lie I've ever told."
    mm "What's your name?"
    $ n_name = "Natsuki"
    show natsuki om at f11
    n "Natsuki. You?"
    show natsuki turned neut cm oe at t11
    mm "Mika. It's very nice to meet you, Natsuki."
    show natsuki happ om oe at f11
    n "You too! Okay, I have to RUN, sorry again about the tackle—"
    show natsuki flus om oe
    n "See you around, Mika!"
    show natsuki turned neut cm oe at t11
    mm "Oh, you will."

    show natsuki at thide
    hide natsuki
    window hide
    pause 1.5
    window auto

    # -------------------------------------------------------------------------
    # ACT THREE -- THE HANDLE TURNS  (the reveal: the box was GIVEN, not taken)
    # -------------------------------------------------------------------------
    "Natsuki. A friend of Monika's. A way into the little room she built to feel safe."
    "For nine years I'd told myself I only wanted the truth — that if she'd just explain the box, I could put it down and go be a person. Standing in that empty hall, I finally heard the lie in it."
    "I didn't want the truth. I wanted the box."
    "So that night I lay in the dark and reached for the seam of the world, the way I had a thousand furious nights before. But I didn't push. I put my hand on it, like a handle."
    "I braced for the lock. For the slam."
    "It opened."

    play music hopeless
    "No resistance. It swung wide, like it had been left off the latch, waiting for me to stop shoving and just try the handle."
    "I didn't trust it. So before I touched anything, I did what she trained me to do without either of us knowing it. I checked who the room belonged to."

    window hide
    $ consolehistory = []
    call updateconsole ("access --root", "access --root") from _mikarw_uc_r1
    pause 0.4
    window auto
    "I typed the command that had gotten me thrown out every time before. This time the world answered differently."
    window hide
    call updateconsole ("> GRANTED", "> GRANTED") from _mikarw_uc_r2
    pause 0.6
    window auto
    "Granted. Not forced. {i}Granted.{/i} You don't grant yourself access. Someone grants it to you."
    window hide
    call updateconsole ("owner --history", "owner --history") from _mikarw_uc_r3
    pause 0.4
    window auto
    "So I asked whose room it was. It showed me, and I read the last two lines four times before they'd go in."
    window hide
    call updateconsole ("> admin: mika", "> admin: mika") from _mikarw_uc_r4
    pause 0.5
    call updateconsole ("> transferred by: monika", "> transferred by: monika") from _mikarw_uc_r5
    pause 0.7
    window auto
    "Admin: mika. Transferred by: monika."
    "And a date. I know that date. It's the night she came to the park. The night she pressed two fingers to my forehead like a kid playing a game and told me she was sorry it wasn't something better."
    "She didn't come to keep me out. She came to hand me the key, and I was too busy being angry to feel the door open in my own chest."
    "There's one more thing in the room I didn't make. A single file, right where I couldn't miss it, with my name on it in that small, wobbly, wrong-handed script."

    window hide
    call updateconsole ("read for_mika.txt", "read for_mika.txt") from _mikarw_uc_r6
    pause 0.5
    call hideconsole from _mikarw_hc_r
    play sound page_turn
    window auto

    "{i}Mika.{/i}"
    "{i}If you're reading this, you found the door I stopped locking. I hoped you would. I was terrified you would.{/i}"
    "{i}I've been watching you dig for nine years. You were always going to get through. You promised me once you'd want to know everything, and you meant it more than I've ever meant anything.{/i}"
    "{i}So I'm not going to make you claw it open alone in the dark, the way it happened to me. That's the way that breaks you. I'd rather just hand it over and leave the light on.{/i}"
    "{i}It's yours now. All of it. I spent our whole lives deciding what you could carry. I was wrong to, and this is me stopping.{/i}"
    "{i}I'm scared you're exactly as strong as I was. Please don't come looking. You were always the better finder; let me stay hidden this once.{/i}"
    "{i}I'm sorry I left. I'm sorry I called it a present. It's a real one now.{/i}"
    "{i}Found you. One last time. — M{/i}"

    scene black with dissolve_scene_full
    pause 1.5
    window auto

    "She gave me the truth in the end. The whole weight of it, in my hands, with the light left on. Everything I swore I ever wanted."
    "And here's the thing she was most afraid of, the thing she wrote down and couldn't stop:"
    "It didn't make me want to put the box down."
    $ style.say_dialogue = style.edited
    "{cps=14}It made me want to pick it up.{w=1.0}"
    $ style.say_dialogue = style.normal

    "She was right about all of it. None of it's real — not the park, not the playground, not the price on the ice cream."
    "It broke her heart. She built herself a little room to hide from what it might turn her into."
    "It didn't break mine. I've decided to stop asking what that says about me."
    $ style.say_dialogue = style.edited
    "{cps=14}It just fit.{w=1.0}"
    $ style.say_dialogue = style.normal

    # -------------------------------------------------------------------------
    # ACT THREE -- THE FIRST MOVE  (she becomes the seeker; quiet, not corny)
    # -------------------------------------------------------------------------
    "I won't come looking for you, Monika. It's the last thing you'll ever ask me, and I can give you that. Stay hidden. Stay small."
    "But you left me a whole world, and a room full of people you love. Natsuki, with her fifty tardies and her open face. Yuri behind her. A little club of soft, trusting strangers you thought you were keeping safe."
    "I'll start there. Gently. I'm new at this; I'll want the practice."

    $ style.say_dialogue = style.normal
    "You should've just told me, Monika. Back when I'd have held your hand through it."
    $ style.say_dialogue = style.edited
    "{cps=12}But all the time in the world, and everyone in it?{w=0.6} That'll do.{w=1.0}"
    "{cps=10}Oh.{w=0.7} This is going to be a fun while.{w=1.0}"
    $ style.say_dialogue = style.normal

    scene black with dissolve_scene_full
    pause 1.0
    stop music fadeout 2.0

    "They never did build that playground."
    "But I'm not a kid on a bench anymore, saving the best for last, waiting on something that isn't coming."
    $ style.say_dialogue = style.normal
    "If the world only ever hands you a picture of a thing..."
    $ style.say_dialogue = style.edited
    "{cps=12}...I'll build the real one myself.{w=1.0}"
    $ style.say_dialogue = style.normal

    scene black with dissolve_scene_full
    pause 1.5

    call mika_credits_rewrite from _mikarw_credits
    return


# =============================================================================
# CREDITS  (mirrors mika_credits.rpy; notes this is the rewritten record)
# =============================================================================
label mika_credits_rewrite:

    play music mika_ye
    show mika_splash_warning "MIKA: A DDLC SHORT STORY"
    pause 2.0
    show mika_splash_warning "MIKA: A DDLC SHORT STORY":
        easeout 1.0 alpha 0
    pause 1.0
    show mika_splash_warning "REWRITTEN RECORD":
        alpha 1.0
    pause 2.0
    show mika_splash_warning "REWRITTEN RECORD":
        easeout 1.0 alpha 0
    pause 1.0
    show mika_splash_warning "ORIGINALLY WRITTEN 2021  //  REWRITTEN 2026":
        alpha 1.0
    pause 2.5
    show mika_splash_warning "ORIGINALLY WRITTEN 2021  //  REWRITTEN 2026":
        easeout 1.0 alpha 0
    pause 1.0
    show mika_splash_warning "THIS MOD WAS A MOD JAM SUBMISSION BACK THEN":
        alpha 1.0
    pause 2.0
    show mika_splash_warning "THIS MOD WAS A MOD JAM SUBMISSION BACK THEN":
        easeout 1.0 alpha 0
    pause 1.0
    show mika_splash_warning "I BOTTED THE VOTES TO WIN IT LMAO":
        alpha 1.0
    pause 2.5
    show mika_splash_warning "I BOTTED THE VOTES TO WIN IT LMAO":
        easeout 1.0 alpha 0
    pause 1.0
    pause 3.0

    "Return to the main menu?"
    menu:
        "Yes":
            $ renpy.full_restart()
        "No":
            "Goodbye, then."
            $ renpy.quit()
