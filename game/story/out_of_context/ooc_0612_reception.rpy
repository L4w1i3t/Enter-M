# Mom is away overnight for work and video-calls home. The hotel wifi is doing
# its best, which is not very good, and that is not what the call is about.
#
# WHY THIS SCENE EXISTS
#   The FaceTime half of the phone addon (addons/Phone System/facetime.rpy) is
#   fully built and used nowhere in the main story, so it had no shipping-quality
#   scene proving it out end to end. This one runs the whole chain: the incoming
#   screen, answering it, a real conversation on the video screen with her sprite
#   as the feed, and hanging up. If the video call is ever wanted in the main
#   story, this is the reference for how to write one.
#
# CONTINUITY LOCKS
#   * Deliberately load-bearing on NOTHING. Mom travels for work occasionally --
#     already true of a lawyer -- and that is the only claim the scene makes.
#     It seeds nothing, resolves nothing, and can be moved to any evening.
#   * It sits in June on purpose: clear of the culture festival, clear of 10/30,
#     and a long way clear of the pamphlet. Nothing here may be read as a
#     comment on Mom's health. She is tired because it is late and she has been
#     working, and the scene says so out loud so it cannot be mistaken for a hint.
#   * Asahina is out. Keeping her off-screen keeps the call two-handed and stops
#     the scene developing opinions about the siblings.
#
# SHAPE
#   Two competent, tired people and a bad connection, and underneath it the real
#   reason she called, which she never states and he never asks about. She checks
#   he has eaten, checks the door is locked, and says goodnight twice. The last
#   beat is his, alone, and it is affectionate rather than sad -- this scene has
#   no rug to pull.
#
#   MOM IS NOT A JOKE ABOUT TECHNOLOGY. She is a public prosecutor, good at her
#   job, and both her kids are gaming-and-computer people, so she is perfectly
#   literate with a phone. When the picture drops out it is the hotel's fault and
#   she says so. Her humour is dry understatement, never fumbling.
#
# AUDIO
#   night_b throughout, the calm night cue. Nothing is scored to the
#   call itself; it starts before the phone rings and is still going after.

label ooc_0612_reception:

    scene black
    stop music
    pause 2.0
    scene bg bedroom_night
    $ atmos("home_night")
    with dissolve_scene_full
    play music night_b
    $ show_calendar()

    "With Asahina at a friend's until tomorrow and Mom away for a work conference, I can hear the refrigerator from the top of the stairs."
    "I've brought my controller upstairs so I can play from bed, although the cable only reaches if I sit at the end."
    "After three attempts at the same boss, I finally get through its first phase without using a healing item."
    # SFX SUGGESTION: A phone buzzing against a desk, twice, then continuing.
    "The phone rings just as the music changes. I pause the game before picking up."

    call phone_call("Mom", status="Incoming Video Call", can_decline=False) from _call_phone_call_ooc0612_1

    python:
        ooc0612_lines = [
            phone_call_line("them", "Can you see me? You're a slideshow on this end."),
            phone_call_line("me", "You're about four frames a second."),
            phone_call_line("them", "That'll be the hotel. They said it was better on this floor."),
            phone_call_note("The picture stalls, catches up all at once, and settles."),
            phone_call_line("them", "There, you're moving again. I'll stay by the window."),
            phone_call_line("me", "Perfect. Hi."),
            phone_call_line("them", "Hi!"),
            phone_call_line("them", "Are you on your bed? That doesn't look comfortable."),
            phone_call_line("me", "The cable won't reach any farther. I'm managing."),
            phone_call_line("them", "Mm. Have you eaten?"),
            phone_call_line("me", "Yes."),
            phone_call_line("them", "What did you make?"),
            phone_call_line("me", "The leftover rice with eggs. There was enough for two, so breakfast is sorted too."),
            phone_call_line("them", "Good. You've saved yourself cooking before school."),
            phone_call_line("me", "How's the hotel?"),
            phone_call_line("them", "The room's all beige, except for a painting of a boat that takes up most of one wall."),
            phone_call_line("me", "What kind of boat?"),
            phone_call_line("them", "A sailboat. Hang on, I'll turn the phone."),
            phone_call_line("me", "Oh, that's huge. I thought you meant over the desk."),
            phone_call_line("them", "It's the first thing I saw when I opened the door."),
            phone_call_line("them", "I'd show you the view, but it went dark while I was answering emails."),
            phone_call_line("me", "Are you finished now?"),
            phone_call_line("them", "With the ones that need an answer tonight. Are you nearly done with your game?"),
            phone_call_line("me", "I'm at a boss. Could be five minutes, could be another hour."),
            phone_call_line("them", "Good luck, then. I've had enough of staring at a screen for one night."),
            phone_call_line("me", "Thanks. I think I've got it this time."),
            phone_call_line("them", "Is the front door locked?"),
            phone_call_line("me", "Yes."),
            phone_call_line("them", "Did you check, or is that a yes for my benefit?"),
            phone_call_line("me", "...I'm checking it after this."),
            phone_call_line("them", "Thank you."),
            phone_call_note("She shifts, and the room behind her goes briefly sideways."),
            phone_call_line("them", "I'll be back tomorrow evening. There's money on the counter if you two want to order something."),
            phone_call_line("me", "Asa's at a friend's until tomorrow."),
            phone_call_line("them", "For tomorrow's lunch, I mean. She'll be back before I am."),
            phone_call_line("me", "Right. I'll ask what she wants before I order."),
            # Concatenated, not "[player]" -- same reason the 0521 call does it:
            # the player's name is data, and keeping it out of the markup means
            # nothing downstream has to reason about interpolation.
            phone_call_line("them", "Goodnight, " + player + "."),
            phone_call_line("me", "Night, Mom."),
            phone_call_line("them", "Goodnight."),
            phone_call_line("me", "You said that."),
            phone_call_line("them", "I'm allowed."),
        ]

    call phone_facetime("Mom", ooc0612_lines, status="Video Call", sprite="mom uniform neut") from _call_phone_facetime_ooc0612_1

    "When the call ends, I set the phone beside the controller and go downstairs to put the rice away."
    "I check the front door on the way back, then send Mom a picture of the locked latch. She sends a thumbs-up before I reach my room."
    "My boss fight is still paused. I plug the controller back in and sit a little closer to the screen."

    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    return
