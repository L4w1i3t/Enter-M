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
#   MOM IS NOT A JOKE ABOUT TECHNOLOGY. She is a civil lawyer, she is good at her
#   job, and both her kids are gaming-and-computer people, so she is perfectly
#   literate with a phone. When the picture drops out it is the hotel's fault and
#   she says so. Her humour is dry understatement, never fumbling.
#
# AUDIO
#   fantasyserenity throughout, the calm night cue. Nothing is scored to the
#   call itself; it starts before the phone rings and is still going after.

label ooc_0612_reception:

    scene black
    stop music
    pause 2.0
    scene bg bedroom
    $ atmos("home_night")
    with dissolve_scene_full
    play music fantasyserenity
    $ show_calendar()

    "Thursday night, and the house is doing its empty-house impression."
    "Asahina is at a friend's until tomorrow. Mom is four hours away in a hotel with a conference room attached, doing whatever it is people do the night before a deposition."
    "I have a chemistry packet, a desk lamp, and the specific kind of focus you only get when nobody is home to interrupt it."
    # SFX SUGGESTION: A phone buzzing against a desk, twice, then continuing.
    "So obviously the phone goes off."

    call phone_call("Mom", status="Incoming Video Call", can_decline=False) from _call_phone_call_ooc0612_1

    python:
        ooc0612_lines = [
            phone_call_line("them", "Can you see me? You're a slideshow on this end."),
            phone_call_line("me", "You're about four frames a second."),
            phone_call_line("them", "That'll be the hotel. It advertises high-speed internet in the lobby, in vinyl lettering."),
            phone_call_note("The picture stalls, catches up all at once, and settles."),
            phone_call_line("them", "There. It comes good if I sit still and don't insult it."),
            phone_call_line("me", "Perfect. Hi."),
            phone_call_line("them", "Hi!"),
            phone_call_line("them", "Look at you. You look like you've been indoors."),
            phone_call_line("me", "I have been indoors. That's where the homework is."),
            phone_call_line("them", "Mm. Have you eaten?"),
            phone_call_line("me", "Yes."),
            phone_call_line("them", "Have you eaten something that was cooked?"),
            phone_call_line("me", "...Define cooked."),
            phone_call_line("them", "I'm going to take that as a no and be very brave about it."),
            phone_call_line("me", "How's the hotel?"),
            phone_call_line("them", "Beige. Aggressively beige. There's a painting of a boat."),
            phone_call_line("me", "What kind of boat?"),
            phone_call_line("them", "The kind that isn't going anywhere."),
            phone_call_line("me", "Relatable."),
            phone_call_line("them", "Don't be smart, it's late."),
            phone_call_line("them", "It IS late, actually. Why are you up?"),
            phone_call_line("me", "You called me."),
            phone_call_line("them", "That's not an answer, that's a technicality."),
            phone_call_line("me", "It's the good kind, though. You'd be proud."),
            phone_call_line("them", "I am unbearably proud. Go to bed."),
            phone_call_line("me", "In a minute."),
            phone_call_line("them", "Is the front door locked?"),
            phone_call_line("me", "Yes."),
            phone_call_line("them", "Did you check, or is that a yes for my benefit?"),
            phone_call_line("me", "...I'm checking it after this."),
            phone_call_line("them", "Thank you."),
            phone_call_note("She shifts, and the room behind her goes briefly sideways."),
            phone_call_line("them", "I'll be back tomorrow evening. There's money on the counter if you two want to order something."),
            phone_call_line("me", "Asa's at a friend's until tomorrow."),
            phone_call_line("them", "Then there's money on the counter and you don't have to share it."),
            phone_call_line("me", "Now THAT'S a deposition."),
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

    "The screen goes back to being a screen."
    "I sit there for a second with the phone face up on the chemistry packet, in a house that is exactly as empty as it was ten minutes ago."
    "Then I go downstairs and check the front door, which was locked, the way I said it was."
    "I check it anyway. She'll ask tomorrow."

    $ hide_calendar()
    scene black with dissolve_scene_full
    pause 2.0
    return
