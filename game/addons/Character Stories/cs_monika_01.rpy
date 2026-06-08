# Monika Character Story 01 -- "Lies and Poems"
# A vanilla DDLC scenario. An ordinary day at the Literature Club.
# Something is wrong but nobody can name it. MC does not exist in this
# story. Where his presence would normally be, the narrative simply
# skips forward -- a hard cut, like frames removed from film.

# =====================================================================
#  Poem Infrastructure
#  Provides the Poem class, display screen, text styles, and showpoem
#  label needed for vanilla-style poem presentation on paper.
#  These are normally defined in the base game's scripts.rpa but are
#  not present in the mod's game/ directory.
# =====================================================================

# Guard: only define Poem class if not already present elsewhere
init -1 python:
    if not hasattr(store, 'Poem'):
        class Poem:
            def __init__(self, author="", title="", text="", yuri_2=False, yuri_3=False):
                self.author = author
                self.title = title
                self.text = text
                self.yuri_2 = yuri_2
                self.yuri_3 = yuri_3

# Poem definitions for this story
init python:
    poem_cs_m01_monika = Poem(
        author="monika",
        title="Watermark",
        text="""\
The day my pen ran dry
I wrote with water instead.
The words dissolved before the ink could set
and I was left with paper
that remembered being touched
but not what was written.

I held it up to the light
hoping for an imprint --
some indent where the pressure of a word
had been enough to leave a mark.

There was nothing.

But the paper was warped
in just the right places,
as though something had been there once
and the page still bent toward the shape of it."""
    )

    poem_cs_m01_natsuki = Poem(
        author="natsuki",
        title="Too Many",
        text="""\
I baked enough for everyone
and counted them out on the tray.
Each one the same size and shape
(as close as I could get them).

But when I set the plate down
the numbers didn't add up.
I made too many.

One extra, sitting at the edge,
cooling off for someone
who must have canceled."""
    )

    poem_cs_m01_sayori = Poem(
        author="sayori",
        title="Half-Step",
        text="""\
The walk to school has a rhythm
my feet know by heart.
Left, right, left, right,
and then a half-step
where I slow down to match
a stride that isn't there.

I keep drifting to the edge of the sidewalk
like I'm making room for someone.
But when I look, it's just me and my shadow
and a stretch of warm concrete.

My shoes are wearing unevenly.
One sole thinner than the other.
I wonder how long I've been walking like this."""
    )

    poem_cs_m01_yuri = Poem(
        author="yuri",
        title="The Empty Cup",
        text="""\
In the room there is a set for tea.
Cups for each guest, arranged in a half circle,
handles turned outward, facing the one who will drink.

I prepared them from memory.
The water, the leaves, the temperature, the count.
Everything was correct.

And yet when I sat down to serve
I had poured one cup too many.

The tea grew cold.
I couldn't bring myself to pour it down the drain.
It would have felt like closing a door
that someone was still walking toward."""
    )

# Paper texture (packed in images.rpa)
image cs_m01_poem_paper_bg = "images/bg/poem.jpg"

transform cs_m01_poem_paper:
    truecenter
    zoom 1.01
    rotate -0.15

transform cs_m01_marker_flicker:
    alpha 0.0
    linear 0.12 alpha 0.18
    linear 0.08 alpha 0.06
    linear 0.18 alpha 0.14
    pause 0.8
    linear 0.4 alpha 0.10

transform cs_m01_bad_title_in:
    alpha 0.0
    yoffset -18
    easeout_quad 0.35 alpha 1.0 yoffset 0

# Deliberately crude sprite work for this route. These positions are local to
# "Lies and Poems" and mimic an early DDLC mod: inconsistent scale, sprites a
# little too low, awkward empty gaps, and speaker focus that often overlaps.
transform cs_m01_timmy_stand(x=640, z=0.80, xo=0, yo=0, y=1.085):
    subpixel False
    xcenter x
    xoffset xo
    yanchor 1.0
    ypos y
    yoffset yo
    zoom z
    alpha 1.0
    on show:
        alpha 0.0
        pause 0.02
        alpha 1.0
    on replace:
        alpha 1.0
        xcenter x
        xoffset xo
        ypos y
        yoffset yo
        zoom z

transform cs_m01_timmy_focus(x=640, z=0.88, xo=0, yo=0, y=1.09):
    subpixel False
    xcenter x
    xoffset xo
    yanchor 1.0
    ypos y
    yoffset yo
    zoom z
    alpha 1.0
    on show:
        alpha 0.0
        pause 0.02
        alpha 1.0
    on replace:
        alpha 1.0
        xcenter x
        xoffset xo
        ypos y
        yoffset yo
        zoom z

transform cs_m01_timmy_hop(x=640, z=0.80, xo=0, yo=0):
    cs_m01_timmy_stand(x, z, xo, yo)
    easeout_quad 0.05 yoffset yo - 34
    easein_quad 0.08 yoffset yo + 4
    easeout_quad 0.07 yoffset yo

transform cs_m01_timmy_dip(x=640, z=0.80, xo=0, yo=0):
    cs_m01_timmy_stand(x, z, xo, yo)
    easein_quad 0.06 yoffset yo + 44
    easeout_quad 0.08 yoffset yo

transform cs_m01_t11:
    cs_m01_timmy_stand(626, 0.91, 0, 18)
transform cs_m01_t21:
    cs_m01_timmy_stand(392, 0.86, -18, 26)
transform cs_m01_t22:
    cs_m01_timmy_stand(884, 0.79, 24, 8)
transform cs_m01_t31:
    cs_m01_timmy_stand(244, 0.74, -24, 38)
transform cs_m01_t32:
    cs_m01_timmy_stand(646, 0.90, 8, 14)
transform cs_m01_t33:
    cs_m01_timmy_stand(1040, 0.76, 34, 28)
transform cs_m01_t41:
    cs_m01_timmy_stand(160, 0.70, -24, 42)
transform cs_m01_t42:
    cs_m01_timmy_stand(438, 0.78, 16, 12)
transform cs_m01_t43:
    cs_m01_timmy_stand(782, 0.72, -12, 34)
transform cs_m01_t44:
    cs_m01_timmy_stand(1090, 0.84, 22, 16)

transform cs_m01_f11:
    cs_m01_timmy_focus(626, 0.99, 0, 2)
transform cs_m01_f21:
    cs_m01_timmy_focus(392, 0.96, -10, 8)
transform cs_m01_f22:
    cs_m01_timmy_focus(884, 0.93, 28, 2)
transform cs_m01_f31:
    cs_m01_timmy_focus(244, 0.88, -12, 20)
transform cs_m01_f32:
    cs_m01_timmy_focus(646, 1.00, 4, 0)
transform cs_m01_f33:
    cs_m01_timmy_focus(1040, 0.90, 34, 12)
transform cs_m01_f41:
    cs_m01_timmy_focus(160, 0.82, -18, 24)
transform cs_m01_f42:
    cs_m01_timmy_focus(438, 0.89, 16, 8)
transform cs_m01_f43:
    cs_m01_timmy_focus(782, 0.84, -4, 18)
transform cs_m01_f44:
    cs_m01_timmy_focus(1090, 0.94, 22, 4)

transform cs_m01_l11:
    cs_m01_timmy_stand(600, 0.91, -72, 18)
transform cs_m01_l21:
    cs_m01_timmy_stand(372, 0.86, -96, 26)
transform cs_m01_l22:
    cs_m01_timmy_stand(864, 0.79, -52, 8)
transform cs_m01_l31:
    cs_m01_timmy_stand(218, 0.76, -90, 40)
transform cs_m01_l32:
    cs_m01_timmy_stand(618, 0.88, -84, 16)
transform cs_m01_l33:
    cs_m01_timmy_stand(1010, 0.78, -66, 30)
transform cs_m01_l41:
    cs_m01_timmy_stand(150, 0.70, -80, 42)
transform cs_m01_l42:
    cs_m01_timmy_stand(420, 0.78, -80, 12)
transform cs_m01_l43:
    cs_m01_timmy_stand(760, 0.72, -78, 34)
transform cs_m01_l44:
    cs_m01_timmy_stand(1070, 0.84, -70, 16)

transform cs_m01_h11:
    cs_m01_timmy_hop(626, 0.91, 0, 18)
transform cs_m01_h21:
    cs_m01_timmy_hop(392, 0.86, -18, 26)
transform cs_m01_h22:
    cs_m01_timmy_hop(884, 0.79, 24, 8)
transform cs_m01_h31:
    cs_m01_timmy_hop(244, 0.74, -24, 38)
transform cs_m01_h32:
    cs_m01_timmy_hop(646, 0.90, 8, 14)
transform cs_m01_h33:
    cs_m01_timmy_hop(1040, 0.76, 34, 28)

transform cs_m01_d11:
    cs_m01_timmy_dip(626, 0.91, 0, 18)
transform cs_m01_d21:
    cs_m01_timmy_dip(392, 0.86, -18, 26)
transform cs_m01_d22:
    cs_m01_timmy_dip(884, 0.79, 24, 8)
transform cs_m01_d31:
    cs_m01_timmy_dip(244, 0.74, -24, 38)
transform cs_m01_d32:
    cs_m01_timmy_dip(646, 0.90, 8, 14)
transform cs_m01_d33:
    cs_m01_timmy_dip(1040, 0.76, 34, 28)

transform cs_m01_mod_4a:
    cs_m01_timmy_stand(148, 0.69, -18, 46)
transform cs_m01_mod_4b:
    cs_m01_timmy_stand(414, 0.80, 26, 18)
transform cs_m01_mod_4c:
    cs_m01_timmy_stand(880, 0.72, -10, 34)
transform cs_m01_mod_4d:
    cs_m01_timmy_stand(1116, 0.86, 42, 12)

screen cs_m01_bad_mod_title():
    zorder 120
    add Solid("#ffd4ef")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 420
        padding (28, 24, 28, 24)
        background Solid("#ffffffcc")
        at cs_m01_bad_title_in

        vbox:
            spacing 16
            xalign 0.5
            yalign 0.5

            text "Doki Doki Literature Club":
                xalign 0.5
                color "#ff6fb7"
                size 42
                bold True
                outlines [(3, "#ffffff", 0, 0), (5, "#7a2d74", 0, 0)]

            text "LIES AND POEMS":
                xalign 0.5
                color "#44b7ff"
                size 56
                bold True
                outlines [(4, "#ffffff", 0, 0), (7, "#ff70bc", 0, 0)]

            text "made by: bootyluvr3921":
                xalign 0.5
                color "#444444"
                size 18

screen cs_m01_missing_slot(x=640, y=92, w=176, h=430, label=""):
    zorder 1
    $ _slot_x = int(x - (w / 2))
    frame:
        xpos _slot_x
        ypos y
        xysize (w, h)
        padding (0, 0, 0, 0)
        background Solid("#ffffff20")
        at cs_m01_marker_flicker

        frame:
            xalign 0.5
            yalign 0.5
            xsize w - 16
            ysize h - 16
            padding (0, 0, 0, 0)
            background Solid("#00000012")

        if label:
            text label:
                xalign 0.5
                yalign 0.08
                color "#ffffffaa"
                size 16
                bold True
                outlines [(2, "#00000080", 0, 0)]

# Character handwriting styles (fonts packed in fonts.rpa)
style cs_m01_poem_vbox:
    xalign 0.5

style cs_m01_poem_viewport:
    xanchor 0
    xsize 650
    ysize 620
    xpos 315
    ypos 38

style cs_m01_poem_vbar is vscrollbar:
    xpos 980
    yalign 0.5
    ysize 640

style cs_m01_monika_text:
    font "gui/font/m1.ttf"
    size 34
    color "#000"
    outlines []

style cs_m01_sayori_text:
    font "gui/font/s1.ttf"
    size 34
    color "#000"
    outlines []

style cs_m01_natsuki_text:
    font "gui/font/n1.ttf"
    size 28
    color "#000"
    outlines []
    line_leading 1

style cs_m01_yuri_text:
    font "gui/font/y1.ttf"
    size 32
    color "#000"
    outlines []

# Poem display screen (replicates vanilla paper + viewport layout)
screen cs_m01_poem(currentpoem, paper="cs_m01_poem_paper_bg"):
    style_prefix "cs_m01_poem"
    add Solid("#f6d1e4")
    vbox:
        add paper at cs_m01_poem_paper
    frame:
        xpos 42
        ypos 30
        padding (10, 5, 10, 5)
        background Solid("#ffffff99")
        text "Poem Sharing Time!!!":
            color "#ff69b4"
            size 18
            bold True
            outlines [(2, "#ffffff", 0, 0), (3, "#7a2d74", 0, 0)]
    viewport id "vp":
        child_size (710, None)
        mousewheel True
        draggable True
        has vbox
        null height 40
        if currentpoem.author == "monika":
            text "[currentpoem.title]\n\n[currentpoem.text]" style "cs_m01_monika_text"
        elif currentpoem.author == "sayori":
            text "[currentpoem.title]\n\n[currentpoem.text]" style "cs_m01_sayori_text"
        elif currentpoem.author == "natsuki":
            text "[currentpoem.title]\n\n[currentpoem.text]" style "cs_m01_natsuki_text"
        elif currentpoem.author == "yuri":
            if currentpoem.yuri_2:
                text "[currentpoem.title]\n\n[currentpoem.text]" style "cs_m01_yuri_text"
            elif currentpoem.yuri_3:
                text "[currentpoem.title]\n\n[currentpoem.text]" style "cs_m01_yuri_text"
            else:
                text "[currentpoem.title]\n\n[currentpoem.text]" style "cs_m01_yuri_text"
        null height 100
    vbar value YScrollValue(viewport="vp") style "cs_m01_poem_vbar"

# Simplified showpoem label for this story.
# Shows the poem on paper with a page-turn sound, waits for click to
# dismiss, then returns to dialogue. Club BGM continues underneath.
label cs_m01_showpoem(poem=None):
    if poem == None:
        return
    play sound page_turn
    window hide
    $ _cs_m01_prev_afm_enable = renpy.game.preferences.afm_enable
    $ renpy.game.preferences.afm_enable = False
    show screen cs_m01_poem(poem)
    with Dissolve(1)
    $ pause()
    hide screen cs_m01_poem
    $ renpy.game.preferences.afm_enable = _cs_m01_prev_afm_enable
    with Dissolve(.5)
    window auto
    return


# =====================================================================
#  THE STORY
# =====================================================================

label cs_monika_01:
    hide screen archive
    hide screen character_stories
    stop music fadeout 1.0

    scene black
    window hide(None)
    pause 2.0
    show screen cs_m01_bad_mod_title
    with Dissolve(0.6)
    pause 2.2
    hide screen cs_m01_bad_mod_title
    with Dissolve(0.35)
    pause 0.5

    # =================================================================
    #  I. End of the School Day
    # =================================================================

    scene bg class_day
    with dissolve_scene_full
    play music t2

    # Static pop -- a recording clicking into place.
    play sound "mod_assets/sfx/vinyl.wav"
    show noise zorder 10:
        alpha 0.10
        linear 0.5 alpha 0.0
    pause 0.5
    hide noise

    window auto
    "The final bell rings."
    "Chairs scrape against linoleum. Bags are zipped. Conversations bloom and scatter like startled birds."
    "Another school day, ordinary in every way that matters, dissolves into the noise of the hallway."

    # =================================================================
    #  II. The Corridor
    # =================================================================

    scene bg corridor
    with wipeleft_scene

    "The corridor leading to the clubroom is quieter than the main halls."
    "Late afternoon light catches dust motes drifting between the windows."

    # A latch clicking -- distant, muffled. No doors in this hallway.
    play sound closet_close

    show sayori 4r zorder 2 at cs_m01_l11
    s "Club time, club time, club ti~me!"
    "Sayori bounces down the hall, bag swinging at her side like a pendulum."

    show natsuki 2c zorder 2 at cs_m01_t22
    show sayori zorder 2 at cs_m01_t21
    n "Every day. You do this every single day."
    show sayori zorder 3 at cs_m01_f21
    s 1a "And I'll do it every day until it sticks! Traditions don't build themselves, Natsuki."
    show natsuki zorder 3 at cs_m01_f22
    n 4c "It's been three weeks."
    show sayori zorder 3 at cs_m01_f21
    s 4r "Three weeks of {i}tradition{/i}~!"
    show natsuki zorder 3 at cs_m01_f22
    n 2q "...I can't argue with that logic because there IS no logic."
    show sayori zorder 2 at cs_m01_t21
    show natsuki zorder 2 at cs_m01_t22

    "They walk together, Sayori's pace brisk but slightly uneven, like she keeps adjusting for something."
    "Every few steps, she drifts to the left side of the hallway."

    show sayori 1c zorder 2 at cs_m01_t21
    "She glances to her right."
    show noise zorder 10:
        alpha 0.05
        linear 1.0 alpha 0.0
    "At the empty space beside her."
    "Her mouth opens, like she's about to say something to someone."
    hide noise

    show sayori 4r zorder 2 at cs_m01_t21
    s "So anyway, did you finish the reading Monika assigned last--"

    "She was looking at Natsuki."
    "Natsuki is on her {i}left{/i}."

    show sayori 1c zorder 2 at cs_m01_t21
    s "..."
    show natsuki zorder 3 at cs_m01_f22
    n "...Did I finish what?"
    show sayori zorder 3 at cs_m01_f21
    s 1a "Ahaha, never mind! I forgot what I was saying!"
    show natsuki zorder 3 at cs_m01_f22
    n 2c "You literally {i}just{/i} started saying it."
    show sayori zorder 3 at cs_m01_f21
    s 4n "My brain is a free spirit, Natsuki. It goes where it wants."
    show natsuki zorder 3 at cs_m01_f22
    n "That is not the flex you think it is."

    show natsuki zorder 1 at thide
    show sayori zorder 1 at thide
    hide natsuki
    hide sayori

    # =================================================================
    #  III. The Clubroom
    # =================================================================

    scene bg club_day
    with wipeleft_scene
    play music t3
    play sound moddooropen

    "The clubroom door swings open."
    "Inside, the desks are already arranged in their usual cluster: the same formation they've been in for weeks now, nudged into place by habit more than planning."
    "There are pencil marks on the whiteboard from three meetings ago, a half-empty tin of tea leaves by the window, and a manga volume bookmarking someone's spot on the shelf."
    "This is a room that's been lived in."

    show monika 1a zorder 2 at cs_m01_t21
    show yuri 1a zorder 2 at cs_m01_t22
    m "Hey, you two! Right on time."

    show yuri zorder 3 at cs_m01_f22
    y "I put the kettle on a few minutes ago. The oolong should be ready shortly."

    show monika zorder 2 at cs_m01_t21
    show yuri zorder 2 at cs_m01_t22

    show natsuki 1a zorder 2 at cs_m01_l31
    n "Oolong again?"
    show yuri zorder 3 at cs_m01_f22
    y 1s "It's a different blend than last week. This one has a lighter body with a slightly floral finish."
    show natsuki zorder 3 at cs_m01_f31
    n 2c "You know I have no idea what any of that means, right?"
    show yuri zorder 3 at cs_m01_f22
    y 2l "It means it tastes good."
    show natsuki zorder 3 at cs_m01_f31
    n 1q "...Fine. Pour me some."
    show natsuki zorder 2 at cs_m01_t31
    show yuri zorder 2 at cs_m01_t22

    show sayori 4r zorder 2 at cs_m01_l33
    s "Ooh, tea! Are there cookies too?"
    show natsuki zorder 3 at cs_m01_f31
    n 5c "I didn't say anything about cookies."
    show sayori at cs_m01_d33
    s 1g "But... but last week you said you might..."
    show natsuki zorder 3 at cs_m01_f31
    n "..."
    n 1q "..."
    "Natsuki reaches into her bag and produces a small plastic container."
    show sayori at cs_m01_h33
    s 4r "I KNEW IT!"
    show natsuki zorder 3 at cs_m01_f31
    n 4e "Shut up! I had extra batter! That's {i}all{/i}!"
    show natsuki zorder 2 at cs_m01_t31
    show sayori zorder 2 at cs_m01_t33
    show monika zorder 3 at cs_m01_f21
    m 2k "You always have 'extra batter,' Natsuki~"
    show natsuki zorder 3 at cs_m01_f31
    n 4q "Don't start."
    show monika zorder 2 at cs_m01_t21

    "The cookies are round and golden, dusted with sugar."
    "Natsuki sets the container on a desk with the careful precision of someone who has done this exact thing many times."

    "Yuri pours tea into mismatched cups, one for each member."
    "Sayori takes a cookie before the lid is fully off."
    "Monika pulls a chair to the front of the room, teacup in hand."

    show screen cs_m01_missing_slot(640, 82, 170, 440, "MC?")
    show natsuki zorder 2 at cs_m01_mod_4a
    show monika zorder 2 at cs_m01_mod_4b
    show yuri zorder 2 at cs_m01_mod_4c
    show sayori zorder 2 at cs_m01_mod_4d

    "For a moment, the clubroom is exactly what it should be."
    "Warm. Familiar."

    # The music hitches -- a groove in the record catching.
    play sound "mod_assets/sfx/vinyl.wav"
    $ renpy.music.set_volume(0.3, delay=0.1, channel="music")
    $ pause(0.5)
    $ renpy.music.set_volume(1.0, delay=0.7, channel="music")

    # =============================================================
    #  CUT 1 -- The arrival that doesn't happen.
    #  MC would walk in here. Sayori would wave. Monika would
    #  greet him. Natsuki would complain. It's the moment the
    #  room goes from "almost full" to "full."
    #  Instead:
    # =============================================================

    hide screen cs_m01_missing_slot
    show monika 1a zorder 3 at cs_m01_f21
    m "Alright, now that we're all--"

    # The scene stutters. A splice in the film.
    window hide(None)
    $ pause(0.3)
    show screen tear(8, 0.4, 0.4, 0, 15)
    $ pause(0.15)
    hide screen tear
    window show(None)

    # Residual grain -- the splice didn't clean up all the way.
    show noise zorder 10:
        alpha 0.04
        linear 8.0 alpha 0.0
    show monika 1d zorder 2 at cs_m01_t21
    show sayori 1c zorder 2 at cs_m01_t22
    hide natsuki
    hide yuri
    m "...all here."
    m "..."

    "Monika pauses, her gaze drifting across the room like she's counting heads."

    show monika 2b zorder 2 at cs_m01_t21
    m "...Anyway! Let's get into today's activity."

    show sayori zorder 3 at cs_m01_f22
    s 1g "Huh? Sorry, I think I blinked and missed something."
    show monika zorder 3 at cs_m01_f21
    m 1a "You probably just need your tea, Sayori."
    show sayori zorder 2 at cs_m01_t22
    show monika zorder 2 at cs_m01_t21

    show sayori 1c zorder 2 at cs_m01_t22
    s "...Yeah. Probably."

    show sayori zorder 1 at thide
    show monika zorder 1 at thide
    hide sayori
    hide monika

    # =================================================================
    #  IV. The Activity -- Monika's Writing Exercise
    # =================================================================

    show monika 2b zorder 2 at cs_m01_t11
    m "So, I've been thinking about our usual routine."
    m 2a "We always write poems at home and share them the next day. And that works great."
    m "But I thought we'd try something different today."
    m 1j "I want us to write our poems {i}here{/i}. Right now. In the clubroom, together."
    show monika zorder 1 at thide
    hide monika

    show natsuki 2c zorder 2 at cs_m01_t21
    show yuri 2a zorder 2 at cs_m01_t22
    n "So... homework, but supervised."
    show yuri zorder 3 at cs_m01_f22
    y "The term is 'workshop.' Writing in a shared space can create a productive kind of ambient energy."
    y "It's a well-established practice in creative circles."
    show natsuki zorder 3 at cs_m01_f21
    n 4c "That's just a fancy way of saying 'peer pressure.'"
    show yuri zorder 3 at cs_m01_f22
    y 2l "...Peer encouragement."
    show natsuki zorder 3 at cs_m01_f21
    n 2c "Uh-huh."
    show natsuki zorder 2 at cs_m01_t21
    show yuri zorder 2 at cs_m01_t22

    show monika 1a zorder 2 at cs_m01_t11
    m "There's something different about writing when the people who'll read it are sitting right next to you."
    m "It changes what you're willing to put on the page."
    show monika zorder 1 at thide
    hide monika

    show sayori 4r zorder 2 at cs_m01_t11
    s "Ooh, ooh! Is it like a race? Can we make it a race?"
    show sayori zorder 1 at thide
    hide sayori

    show monika 2b zorder 2 at cs_m01_t11
    m "It's not a race, Sayori."
    show monika zorder 1 at thide
    hide monika

    show sayori 4n zorder 2 at cs_m01_t11
    s "Fine... but I'm still gonna try to finish first."
    show sayori zorder 1 at thide
    hide sayori

    show natsuki 1q zorder 2 at cs_m01_t11
    n "Alright, I'll bite. How long do we have?"
    show natsuki zorder 1 at thide
    hide natsuki

    show monika 1a zorder 2 at cs_m01_t11
    m "Fifteen minutes. Then we share."
    m "I'm passing out paper now. And no peeking!"
    show monika zorder 1 at thide
    hide monika

    show sayori 4r zorder 2 at cs_m01_t11
    s "No promises~"
    show sayori zorder 1 at thide
    hide sayori

    # =================================================================
    #  V. The Writing Session
    # =================================================================

    "Monika distributes sheets of blank paper."
    "One to Sayori. One to Natsuki. One to Yuri. One for herself."
    "She holds the remaining stack for a moment, looks at it, then sets it aside."

    show screen cs_m01_missing_slot(640, 104, 150, 390)
    show monika 1a zorder 2 at cs_m01_mod_4a
    show sayori 1a zorder 2 at cs_m01_mod_4b
    show natsuki 1c zorder 2 at cs_m01_mod_4c
    show yuri 1a zorder 2 at cs_m01_mod_4d

    "The club settles in."
    "Sayori taps her pen against her chin, staring at the ceiling like the answer might be hidden in the acoustic tiles."
    "After a long moment, she brightens visibly, hunches forward, and starts writing in quick, excited strokes."

    "Natsuki's brow furrows. She writes a line, reads it back, frowns, and crosses it out."
    "Writes another. Crosses that out too."
    "She turns the paper over and starts fresh on the back, pen moving with sudden confidence."

    "Yuri sits perfectly still for nearly two full minutes, eyes closed, breathing measured."
    "When she opens them, she begins writing in careful, even lines. The kind of handwriting that looks more like calligraphy than note-taking."

    "Monika's pen moves steadily, without pause or hesitation."
    "Every few lines she re-reads what she's written, tucks a strand of hair behind her ear, and continues."

    hide screen cs_m01_missing_slot
    show monika zorder 1 at thide
    show sayori zorder 1 at thide
    show natsuki zorder 1 at thide
    show yuri zorder 1 at thide
    hide monika
    hide sayori
    hide natsuki
    hide yuri

    "The room goes quiet."
    "Not uncomfortable quiet. The kind that happens when everyone in a room is doing the same thing and none of them need to talk about it."
    "Just the scratch of pens. The tick of the wall clock. The muffled shouts of a sports club practicing outside."

    # Film grain creeping in. The tape is wearing.
    show noise zorder 10:
        alpha 0.0
        linear 25.0 alpha 0.06

    "..."

    "Time passes differently in a room like this."
    "Seconds stretch. Minutes compress."

    # Audio bleed -- a door closing, somewhere else entirely.
    play sound moddoorclose

    "..."

    # =========================================================
    #  CUT 2 -- MC would be sitting here, struggling to write.
    #  He'd stare at his paper. Scratch something out.
    #  Sayori would lean over and try to peek.
    #  He'd cover his poem with his arm.
    #  A normal, warm, silly moment between two friends.
    #  Instead, Sayori leans to her right --
    # =========================================================

    # A brief stutter in the playback.
    play sound "mod_assets/sfx/vinyl.wav"

    show sayori 1a zorder 2 at cs_m01_t11

    "Sayori leans sideways in her chair, craning her neck to the right."
    "She has the grin of someone about to commit a small crime."

    show sayori 5b zorder 2 at cs_m01_t11
    s "Psst. Hey, let me see what you've--"

    "She stops mid-lean. The desk next to her is empty."

    show sayori 1c zorder 2 at cs_m01_t11
    s "..."

    "Her grin doesn't fade immediately."
    "It hangs there for a second, confused, like it hasn't caught up to the rest of her face."

    "Then it drops."

    show sayori at cs_m01_d11
    s "..."

    "She straightens up, eyes darting between the empty desk and her own paper before settling on the empty desk again."

    show sayori 1a zorder 2 at cs_m01_t11
    s "Ahaha... I think I need more sleep."

    show sayori zorder 1 at thide
    hide sayori

    "Nobody noticed."
    show noise zorder 10:
        alpha 0.04
        linear 15.0 alpha 0.08
    "The writing continues."

    "..."

    "Natsuki has filled half her paper. She's rereading it with narrow eyes, like a jeweler inspecting a stone for flaws."
    "Yuri has written less, but each line is deliberate. She pauses between sentences to look out the window."
    "Sayori is drawing a small sun in the margin of her poem."
    "Monika finishes first. She sets her pen down and watches the others with a soft, patient smile."

    "..."

    "The clock ticks its way through fifteen minutes."

    # =================================================================
    #  VI. The Break
    # =================================================================

    show monika 2b zorder 2 at cs_m01_t11
    m "Alright, pens down! Let's take a short break before we share."
    show monika zorder 1 at thide
    hide monika

    "Chairs push back. People stretch."
    "Natsuki stands up first and heads straight for the supply closet."

    show natsuki 1a zorder 2 at cs_m01_t11
    n "I need a palate cleanser."
    play sound closet_open
    "She slides the closet door open and reaches for the shelf where she keeps her manga."
    "And stops."

    show natsuki 4c zorder 2 at cs_m01_t11
    stop music
    n "...Who moved my stuff?"

    show yuri 2a zorder 2 at cs_m01_t22
    show natsuki zorder 2 at cs_m01_t21
    y "Oh. I reorganized the shelf earlier this week."
    y "I needed room for a few reference books I brought from home."
    show natsuki zorder 3 at cs_m01_f21
    # play poem panic
    play music t7
    n 4e "You {i}moved my manga{/i} without asking?"
    show yuri zorder 3 at cs_m01_f22
    y 2t "I simply consolidated your collection to the lower shelf. Everything is still there and in order."
    show natsuki zorder 3 at cs_m01_f21
    n 4c "The {i}lower{/i} shelf! That's practically the floor, Yuri! Do you know how dusty it gets down there?"
    show yuri zorder 3 at cs_m01_f22
    y 3n "I didn't think it would be a problem. I was careful with them."
    show natsuki zorder 3 at cs_m01_f21
    n "You didn't {i}ask{/i}! That shelf was mine!"
    show yuri zorder 3 at cs_m01_f22
    y 2h "It wasn't formally assigned--"
    show natsuki zorder 3 at cs_m01_f21
    n 4e "It was {i}understood{/i}!"

    # This is the moment where MC would normally step in.
    # He'd say something slightly dumb. "Hey, why don't we just
    # split the shelf?" Both girls would redirect their frustration
    # at him instead, which would paradoxically defuse the tension.

    show natsuki 4c zorder 2 at cs_m01_t21
    show yuri 3o zorder 2 at cs_m01_t22

    "The argument hangs in the air."
    "Both of them glance, almost simultaneously, toward the center of the room."
    "Waiting for something."

    "..."
    stop music
    "No one steps in."
    "..."

    # =========================================================
    #  CUT 3 -- The intervention that doesn't come.
    # =========================================================

    window hide(None)
    show screen tear(5, 0.6, 0.3, 0, 10)
    play sound "sfx/glitch1.ogg"
    $ pause(0.2)
    hide screen tear
    stop sound
    window show(None)

    # The scene resumes slightly later. Something was excised.
    play sound "mod_assets/sfx/vinyl.wav"
    show noise zorder 10:
        alpha 0.06
        linear 6.0 alpha 0.03
    show natsuki 2q zorder 2 at cs_m01_t21
    show yuri 2v zorder 2 at cs_m01_t22
    n "...Fine. I'll take the second shelf. But you owe me."
    show yuri zorder 3 at cs_m01_f22
    y "...That's fair. I apologize, Natsuki."
    show natsuki zorder 3 at cs_m01_f21
    n 1q "..."
    n "Whatever. Just ask next time."
    show natsuki zorder 2 at cs_m01_t21
    show yuri zorder 2 at cs_m01_t22

    show monika 1d zorder 2 at cs_m01_t32
    m "..."
    m "Was there just--"
    m "..."
    play music t3
    m 1a "Glad you two got it sorted!"
    show monika zorder 1 at thide
    show natsuki zorder 1 at thide
    show yuri zorder 1 at thide
    hide monika
    hide natsuki
    hide yuri

    "Monika smiles, though her eyes linger on the gap between Natsuki and Yuri: the exact spot where someone would have been standing, if anyone had been there to step in."
    "After a moment, she looks away."

    "..."

    # A brief hitch -- the scene loading the next segment.
    window hide(None)
    $ pause(0.15)
    window show(None)

    # A quieter moment. Yuri is by the window with her tea.

    show yuri 1a zorder 2 at cs_m01_t21
    show monika 2a zorder 2 at cs_m01_t22
    y "I've been rereading {i}The Portrait of Markov{/i} this week."
    show monika zorder 3 at cs_m01_f22
    m "Again? You must really love that book."
    show yuri zorder 3 at cs_m01_f21
    y 2s "It reveals new things each time."
    y "The layers of identity and perception... I keep finding passages I missed before."
    y 1a "Or perhaps passages I wasn't ready for until now."
    show monika zorder 3 at cs_m01_f22
    m 1a "That's the mark of really good writing, isn't it?"
    show monika zorder 2 at cs_m01_t22
    show yuri zorder 2 at cs_m01_t21

    show yuri zorder 3 at cs_m01_f21
    y 1a "Actually, I've been meaning to lend it to..."
    y 1c "..."
    show yuri at cs_m01_d21
    y "...to..."
    show monika zorder 3 at cs_m01_f22
    m 1d "To...?"
    show yuri zorder 3 at cs_m01_f21
    show noise zorder 10:
        alpha 0.08
        linear 2.0 alpha 0.03
    y 3v "I... I lost the thought."
    y "That keeps happening. I have something perfectly clear in my mind, and then it just... dissolves."
    show monika zorder 3 at cs_m01_f22
    m 1l "Ahaha, it'll come back to you. Maybe it's the tea."
    show monika zorder 2 at cs_m01_t22
    show yuri zorder 2 at cs_m01_t21

    show yuri 2u zorder 2 at cs_m01_t21
    y "..."
    "Yuri stares at the book in her hands, turning it over slowly. She was going to lend it to someone. She was {i}certain{/i} of it."
    "The thought had been right there, warm and familiar and close, and then it simply wasn't."

    show yuri zorder 1 at thide
    show monika zorder 1 at thide
    hide yuri
    hide monika

    "On the other side of the room, Sayori is showing Natsuki something she doodled in the margins of her poem."
    "Natsuki pretends not to be charmed."
    "She fails."

    # =================================================================
    #  VII. Poem Sharing -- Monika
    # =================================================================

    show monika 2b zorder 2 at cs_m01_t11
    m "Okay! Break's over. Time to share what we wrote."
    m 2a "I'll go first to take the pressure off."
    show monika zorder 1 at thide
    hide monika

    stop music fadeout 1.5
    "Monika stands at the front of the room, paper in hand."
    "She holds it at her side with the easy posture of someone who has given a hundred presentations."

    show monika 2a zorder 2 at cs_m01_t11
    "She clears her throat."
    play music dream
    m "This one's called {i}Watermark{/i}."

    # The poem appears on paper (vanilla-style presentation).
    call cs_m01_showpoem(poem_cs_m01_monika) from _cs_m01_sp_1

    # Reactions
    show monika 1l zorder 2 at cs_m01_t11
    m "...That's it."
    m 1n "I'm honestly not sure where it came from. The words just sort of arrived."
    show monika zorder 1 at thide
    hide monika

    "..."

    show yuri 2s zorder 2 at cs_m01_t21
    show natsuki 1q zorder 2 at cs_m01_t22
    y "The extended metaphor of water and ink is very elegant, Monika."
    y 1a "And the final image: paper that bends toward the shape of something no longer there..."
    y 2s "That's genuinely moving."

    show natsuki zorder 3 at cs_m01_f22
    n "...Yeah. It's good."
    n 2a "I mean, obviously. It's Monika."
    show natsuki zorder 2 at cs_m01_t22
    show yuri zorder 2 at cs_m01_t21

    show yuri zorder 1 at thide
    show natsuki zorder 1 at thide
    hide yuri
    hide natsuki

    show sayori 2r zorder 2 at cs_m01_t11
    s "..."
    s 1a "I really liked it."
    s "It made me feel kind of... I don't know. Like when you walk into a room and you can tell someone just left."
    s "But you can't figure out who it was."
    show sayori zorder 1 at thide
    hide sayori

    show monika 2a zorder 2 at cs_m01_t11
    m "...Thank you, everyone."
    show monika zorder 1 at thide
    hide monika

    # =================================================================
    #  VIII. Poem Sharing -- Natsuki
    # =================================================================

    show natsuki 2q zorder 2 at cs_m01_t11
    n "Fine, I'll go next. Get it over with."
    n "And before anyone says anything -- it's short on purpose."
    show natsuki zorder 1 at thide
    hide natsuki

    show sayori 1a zorder 2 at cs_m01_t11
    s "Nobody was going to--"
    show sayori zorder 1 at thide
    hide sayori

    show natsuki 1e zorder 2 at cs_m01_t11
    n "I'm preempting."
    show natsuki zorder 1 at thide
    hide natsuki

    "Natsuki holds her paper at arm's length, like she's daring it to embarrass her."

    show natsuki 1c zorder 2 at cs_m01_t11
    n "It's called {i}Too Many{/i}."

    call cs_m01_showpoem(poem_cs_m01_natsuki) from _cs_m01_sp_2

    # Reactions
    show natsuki 2q zorder 2 at cs_m01_t11
    n "...That's it. Don't read into it."
    show natsuki zorder 1 at thide
    hide natsuki

    show monika 2a zorder 2 at cs_m01_t21
    show yuri 2s zorder 2 at cs_m01_t22
    m "Natsuki, that's lovely."
    show yuri zorder 3 at cs_m01_f22
    y "There's a real precision to it. The domesticity of baking as a vehicle for something more tender..."
    show natsuki 4q zorder 2 at cs_m01_t32
    n "It's not a {i}vehicle{/i}! I wrote about cookies! That's literally it!"
    show yuri zorder 2 at cs_m01_t22
    show monika zorder 3 at cs_m01_f21
    m 2k "Ahaha~"
    show monika zorder 2 at cs_m01_t21

    show natsuki 2q zorder 2 at cs_m01_t32
    n "..."
    n "...Okay, maybe it's a {i}little{/i} about more than cookies."
    n 1q "But only a little."
    show monika zorder 1 at thide
    show yuri zorder 1 at thide
    show natsuki zorder 1 at thide
    hide monika
    hide yuri
    hide natsuki

    show sayori 1a zorder 2 at cs_m01_t11
    s "I liked the part about counting them out. Like she really wanted to get it right for everybody."
    s 1c "...even the person who didn't show up."
    show sayori zorder 1 at thide
    hide sayori

    # A tone that shouldn't be here -- a stray signal.
    play sound "mod_assets/sfx/beep.ogg"
    $ pause(0.3)
    stop sound fadeout 0.2

    # =================================================================
    #  IX. CUT 4 -- The biggest cut. MC's poem.
    #  Monika would call on the next person. The girls would react.
    #  Sayori encouraging, Natsuki critical, Yuri analytical.
    #  It's the heart of the sharing circle.
    #  But MC doesn't exist. There is no poem to read.
    #  So it just --
    # =================================================================

    show monika 2a zorder 2 at cs_m01_t11
    m "Great work, Natsuki."
    m "Next up is--"

    # Hard splice. The scene jumps.
    window hide(None)
    $ pause(0.1)
    show screen tear(15, 0.1, 0.15, 0, 40)
    play sound "sfx/s_kill_glitch1.ogg"
    $ pause(0.25)
    stop sound
    hide screen tear
    # Brief flash of noise
    show noise zorder 10:
        alpha 0.3
    $ pause(0.15)
    hide noise
    window show(None)

    # Resume. The conversation has jumped forward mid-sentence.
    # Everyone is repositioned, as if time skipped.

    # The grain doesn't fully clear this time. Something's accumulating.
    show noise zorder 10:
        alpha 0.06
        linear 20.0 alpha 0.10
    show vignette zorder 5:
        alpha 0.0
        linear 30.0 alpha 0.25

    show natsuki 2g zorder 2 at cs_m01_t21
    show sayori 1c zorder 2 at cs_m01_t22
    n "...thought that was pretty-- wait."
    show sayori zorder 3 at cs_m01_f22
    s "Huh?"
    show natsuki zorder 3 at cs_m01_f21
    n 2c "What was I just saying?"
    show sayori zorder 3 at cs_m01_f22
    s 1g "I... don't know. I thought you were talking about somebody's poem?"
    show natsuki zorder 3 at cs_m01_f21
    n 4c "Whose?"
    show sayori zorder 3 at cs_m01_f22
    s "..."

    show sayori at cs_m01_d22
    s 1c "I don't remember."
    show natsuki zorder 2 at cs_m01_t21
    show sayori zorder 2 at cs_m01_t22

    show screen cs_m01_missing_slot(640, 116, 158, 380, "poem?")
    show yuri 2u zorder 2 at cs_m01_t32
    y "..."
    "Yuri is staring at the approximate center of the space between desks -- the spot where a person would be standing if they were presenting a poem."
    "Nobody is standing there."
    hide screen cs_m01_missing_slot
    show yuri zorder 1 at thide
    hide yuri

    show monika 1d zorder 2 at cs_m01_t32
    m "..."
    m 1a "...Right! Sayori, you're up!"

    show monika zorder 1 at thide
    show natsuki zorder 1 at thide
    show sayori zorder 1 at thide
    hide monika
    hide natsuki
    hide sayori

    # =================================================================
    #  X. Poem Sharing -- Sayori
    # =================================================================

    show sayori 1q zorder 2 at cs_m01_t11
    s "Okay! Mine is... kinda short."
    s "And maybe a little weird."
    s 1a "But it came from somewhere real, I think!"
    show sayori zorder 1 at thide
    hide sayori

    show monika 1a zorder 2 at cs_m01_t11
    m "That's all that matters."
    show monika zorder 1 at thide
    hide monika

    "Sayori holds up her paper."
    "It's wrinkled, with pen marks where things were crossed out and rewritten. There's a small doodle of a sun in the corner."

    show sayori 1a zorder 2 at cs_m01_t11
    s "It's called {i}Half-Step{/i}."

    call cs_m01_showpoem(poem_cs_m01_sayori) from _cs_m01_sp_3

    # Reactions
    show sayori 4r zorder 2 at cs_m01_t11
    s "...That's it! Ehehe~"
    s 1c "I started writing about walking and it just went somewhere kind of... heavy."
    s "I dunno where it came from."
    show sayori zorder 1 at thide
    hide sayori

    "..."

    show natsuki 1g zorder 2 at cs_m01_t21
    show yuri 2v zorder 2 at cs_m01_t22
    n "..."
    y "..."
    show natsuki zorder 1 at thide
    show yuri zorder 1 at thide
    hide natsuki
    hide yuri

    show monika 2r zorder 2 at cs_m01_t11
    m "..."
    "Monika is quiet for a long moment."
    show monika 2a zorder 2 at cs_m01_t11
    m "That's really beautiful, Sayori."
    m "The detail about the shoes wearing unevenly... that's the kind of thing a reader feels in their body."
    show monika zorder 1 at thide
    hide monika

    show yuri 1a zorder 2 at cs_m01_t11
    y "The repetition of 'left, right' creates a rhythm that the half-step disrupts."
    y 2s "It's a small detail, but it makes the reader physically uncomfortable. In, um... in a good way."
    show yuri zorder 1 at thide
    hide yuri

    show natsuki 2q zorder 2 at cs_m01_t11
    n "...It's good, Sayori."
    n 1q "I don't really know what to say about it. But it made me feel something. So."
    show natsuki zorder 1 at thide
    hide natsuki

    show sayori 4r zorder 2 at cs_m01_t11
    s "Aww~ Thanks, guys."
    show sayori zorder 1 at thide
    hide sayori

    # =================================================================
    #  XI. Poem Sharing -- Yuri
    # =================================================================

    show yuri 2a zorder 2 at cs_m01_t11
    y "I suppose that leaves me."
    show yuri zorder 1 at thide
    hide yuri

    "Yuri stands, holding her poem with both hands."
    "Her fingers press the edges of the paper so tightly the corners bend inward."

    show yuri 2s zorder 2 at cs_m01_t11
    y "{i}The Empty Cup{/i}."

    call cs_m01_showpoem(poem_cs_m01_yuri) from _cs_m01_sp_4

    # Reactions
    show yuri 4b zorder 2 at cs_m01_t11
    y "...I realize the tea metaphor might be overly specific. I--"
    show yuri zorder 1 at thide
    hide yuri

    show monika 1a zorder 2 at cs_m01_t11
    m "It's perfect, Yuri. Don't second-guess it."
    show monika zorder 1 at thide
    hide monika

    show natsuki 1q zorder 2 at cs_m01_t11
    n "..."
    "Natsuki is quiet -- not her usual dismissive quiet, but something else entirely."
    n 2c "The last two lines."
    n "About closing a door that someone's still walking toward."
    n "..."
    n 1q "That part's really good."
    show natsuki zorder 1 at thide
    hide natsuki

    show yuri 2m zorder 2 at cs_m01_t11
    y "...Thank you, Natsuki. That means a great deal."
    show yuri zorder 1 at thide
    hide yuri

    # =================================================================
    #  XII. Convergence
    # =================================================================

    stop music fadeout 1.5
    "A silence settles over the room -- not uncomfortable, but heavy in a way none of them can explain."

    show natsuki 1g zorder 2 at cs_m01_t11
    n "..."
    n 2c "Okay, is it just me?"
    show natsuki zorder 1 at thide
    hide natsuki

    show monika 1d zorder 2 at cs_m01_t11
    m "Is what just you?"
    show monika zorder 1 at thide
    hide monika

    play music grandma
    show natsuki 4c zorder 2 at cs_m01_t11
    n "Did we all just write the same poem?"
    n "Look at what we've got."
    n "Mine is about having one extra cookie. Sayori's is about leaving room on the sidewalk."
    n "Yuri's is about pouring a cup nobody drinks."
    n "And yours, Monika. Paper that bends toward the shape of something that's gone."
    n 2c "They're all about the same thing."
    n "Something extra. Something left over."
    n "Meant for someone who just... isn't."
    show natsuki zorder 1 at thide
    hide natsuki

    show sayori 1c zorder 2 at cs_m01_t11
    s "..."
    s "Huh."
    s "I didn't even notice."
    show sayori zorder 1 at thide
    hide sayori

    show yuri 2v zorder 2 at cs_m01_t21
    show monika 2r zorder 2 at cs_m01_t22
    y "It is unusual. Four people writing independently shouldn't converge this cleanly on the same emotional register."
    y "Not like this, at least."
    show yuri zorder 2 at cs_m01_t21

    show monika zorder 3 at cs_m01_f22
    m "..."
    m 2a "I think it just means we're really in sync as a club."
    m 1j "That's the whole point of writing together, right?"
    show monika zorder 2 at cs_m01_t22

    show yuri zorder 1 at thide
    show monika zorder 1 at thide
    hide yuri
    hide monika

    "Monika smiles. It's convincing...almost."

    stop music fadeout 1.5
    "..."

    "Nobody asks the obvious question."
    # The music warps -- the tape is degrading.
    play music t3g3 fadein 0.5
    "Nobody asks who the extra cookie was for."
    "Nobody asks who Sayori was making room for."
    "Nobody asks who the tea was poured for."

    show layer master:
        subpixel True
        truecenter
        linear 15 zoom 1.03

    "The question doesn't occur to them. It can't at all."

    # A brief stall. The game digesting something.
    window hide(None)
    $ pause(0.8)
    window show(None)

    # =================================================================
    #  XIII. Winding Down
    # =================================================================

    # Reset. The tape finds its groove again.
    show layer master
    play music t3 fadein 2.0
    show noise zorder 10:
        alpha 0.05

    "The remaining time passes the way comfortable afternoons do:"
    "slowly, with laughter, and quicker than anyone expects."

    show natsuki 5c zorder 2 at cs_m01_t21
    show sayori 4r zorder 2 at cs_m01_t22
    n "Sayori, you are getting cookie crumbs on the poem."
    s "It adds character!"
    show natsuki zorder 3 at cs_m01_f21
    n 4e "It adds grease stains!"
    show sayori at cs_m01_h22
    s 1r "Ahaha, oops..."
    show natsuki zorder 2 at cs_m01_t21
    show sayori zorder 2 at cs_m01_t22

    show natsuki zorder 1 at thide
    show sayori zorder 1 at thide
    hide natsuki
    hide sayori

    show yuri 1a zorder 2 at cs_m01_t21
    show monika 2a zorder 2 at cs_m01_t22
    y "I have to say, writing here was more comfortable than I expected."
    y 2s "The shared silence... it was grounding. I didn't feel self-conscious at all."
    show monika zorder 3 at cs_m01_f22
    m "I'm really glad to hear that! Maybe we should make this a regular thing."
    show yuri zorder 3 at cs_m01_f21
    y 1a "I wouldn't object to it."
    show monika zorder 2 at cs_m01_t22
    show yuri zorder 2 at cs_m01_t21

    show natsuki 1q zorder 2 at cs_m01_l31
    n "...I guess it wasn't the worst idea you've ever had."
    show monika zorder 3 at cs_m01_f22
    m 2k "High praise from Natsuki~"
    show natsuki zorder 3 at cs_m01_f31
    n 4q "Don't push it."
    show monika zorder 2 at cs_m01_t22
    show natsuki zorder 2 at cs_m01_t31
    show yuri zorder 2 at cs_m01_t21

    show monika zorder 1 at thide
    show yuri zorder 1 at thide
    show natsuki zorder 1 at thide
    hide monika
    hide yuri
    hide natsuki

    "The afternoon light shifts from gold to amber, long shadows stretching across the desks."

    show monika 2b zorder 2 at cs_m01_t11
    m "Alright, I think that's a good place to stop for today."
    m 2a "Great work, everyone. Really."
    m "I think these poems were some of the most honest things we've shared."
    show monika zorder 1 at thide
    hide monika

    show natsuki 2a zorder 2 at cs_m01_t31
    show yuri 1a zorder 2 at cs_m01_t32
    show sayori 4r zorder 2 at cs_m01_t33
    n "See you guys tomorrow."
    y "Have a good evening."
    s "Bye-bye~!"
    show natsuki zorder 1 at thide
    show yuri zorder 1 at thide
    show sayori zorder 1 at thide
    hide natsuki
    hide yuri
    hide sayori

    # =================================================================
    #  XIV. CUT 5 -- The Walk Home
    #  Sayori would wait at the clubroom door. She and MC
    #  would walk home together. She'd tease him.
    #  He'd pretend to be annoyed. It would be warm and ordinary.
    # =================================================================

    play sound moddoorclose
    scene bg corridor
    with wipeleft_scene
    play music t2

    # Another splice in the tape.
    play sound "mod_assets/sfx/vinyl.wav"
    show noise zorder 10:
        alpha 0.04

    "The hallway is nearly empty."
    "Most of the after-school clubs have let out. The building has the hushed, settling quality of a place that's done being used for the day."

    "Sayori steps out of the clubroom and turns left."

    show sayori 1a zorder 2 at cs_m01_t11
    "She takes a few steps, then stops and turns around."

    show sayori 1c zorder 2 at cs_m01_t11
    s "..."

    "She's waiting for someone, rocking on her heels as the seconds stretch -- three, five, ten."

    "Her hand drifts out to her right."
    "Loosely. Like she's about to nudge someone with her elbow."
    "Like she's done it a thousand times."

    "Her fingers close on air."
    "Her mouth opens."

    show sayori 1q zorder 2 at cs_m01_t11
    s "Ready to--"

    # The word snags.
    window hide(None)
    $ pause(0.1)
    show screen tear(3, 0.8, 0.2, 0, 6)
    $ pause(0.1)
    hide screen tear
    window show(None)

    show sayori 1c zorder 2 at cs_m01_t11
    s "..."
    s "..."

    "She closes her mouth and looks down the hallway. It's empty."

    show sayori at cs_m01_d11
    s "..."

    show sayori 1a zorder 2 at cs_m01_t11
    s "Hm."

    show sayori zorder 1 at thide
    hide sayori

    scene bg residential_day
    with wipeleft_scene

    "Sayori walks home alone, her shadow stretching long and thin on the pavement in the low sun."
    "She walks at her usual pace, but stays on the left side of the sidewalk, as though the right side is being saved for someone."

    "Her shoes tap against the concrete in the familiar rhythm -- left, right, left, right -- and then a half-step, the same hitch in her stride, every time."

    "..."
    "..."

    # =================================================================
    #  XV. Epilogue -- The Clubroom, After Everyone Has Left
    # =================================================================

    stop music fadeout 2.0
    scene black
    with dissolve_scene_full
    pause 2.0

    scene bg club_day
    with dissolve_scene_half

    "The clubroom is empty."
    "The last of the daylight comes through the windows at a low angle, painting long rectangles of orange across the floor."

    show monika 1a zorder 2 at cs_m01_t11

    "Monika is still here, collecting the poems and stacking them neatly -- the same way she does every day."

    show monika 1d zorder 2 at cs_m01_t11
    "She pauses, her attention caught by the stack of blank paper she'd set aside for the exercise."
    "She counts: five sheets passed out at the start of the session, four poems collected."

    m "..."

    "She counts the remaining blanks -- there are none. Five sheets out, four poems back. That leaves one unaccounted for, but the stack has no blanks."

    show monika 2r zorder 2 at cs_m01_t11
    m "..."

    "She fans the poems out on the desk."
    "Hers. Natsuki's. Sayori's. Yuri's."
    "Four poems. Four sheets. Four members."

    m "..."

    "She must have only passed out four."

    show monika 1a zorder 2 at cs_m01_t11
    "She gathers everything up."

    show monika zorder 1 at thide
    hide monika

    "On her way to the door, she passes the desk by the window -- the one nobody sat at today -- and stops."

    # Slow ambient dread.
    show layer master:
        subpixel True
        truecenter
        linear 30 zoom 1.04

    "The desk is bare, completely clean, but there's something on the surface."
    "A faint impression in the wood."
    "Small, thoughtless circles, pressed into the grain."
    "The kind a person makes with a pen when they're thinking about what to write."

    show monika 1d zorder 2 at cs_m01_t11
    m "..."
    m "When did..."
    m "..."

    show monika 1a zorder 2 at cs_m01_t11
    m "Hm."

    "She reaches out and runs her thumb across the indentations."
    "They're real. Someone sat here and pressed a pen into this desk, thoughtlessly, recently."

    # A low pulse -- not quite a heartbeat, but close.
    play music hb fadein 3.0

    show monika 2r zorder 2 at cs_m01_t11
    m "..."

    "Monika stands there for a long time."
    "The light from the window moves slowly across the floor."

    show monika 1r zorder 2 at cs_m01_t11

    "Then she picks up her bag, pushes the chair in, and turns off the light."

    show monika zorder 1 at thide
    hide monika
    show layer master

    scene black
    with dissolve

    "..."

    play sound moddoorclose
    "The door clicks shut."

    "..."
    "..."

    pause 2.0

    # Final image: the dark clubroom.
    # The chair at the window desk is pulled back out.
    # No one touched it.

    scene bg club_day
    show vignette zorder 5
    show noise zorder 4:
        alpha 0.08
    show screen cs_m01_missing_slot(640, 122, 170, 360, "chair")
    with dissolve

    "..."

    pause 3.0

    window hide(None)
    $ pause(0.5)
    show screen tear(4, 1.0, 0.2, 0, 8)
    $ pause(0.4)
    hide screen tear
    $ pause(1.5)

    hide screen cs_m01_missing_slot
    stop music fadeout 2.0
    scene black
    hide vignette
    hide noise
    with dissolve

    pause 3.0

    $ persistent.cs_monika_01_unlocked = True

    return
