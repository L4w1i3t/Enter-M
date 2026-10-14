# Shared paper/viewport poem presentation: call enter_m_showpoem(poem).
# Poem stores author, title and text; the guarded class declaration also supports
# an existing compatible store.Poem. Monika uses m1.TTF; other authors use Halogen.
# Playback hides dialogue, temporarily disables AFM, turns the page and waits for
# dismissal. persistent.first_poem controls the one-time dismissal hint.

init -2 python:
    if not hasattr(store, "Poem"):
        class Poem:
            def __init__(self, author="", title="", text="", yuri_2=False, yuri_3=False):
                self.author = author
                self.title = title
                self.text = text
                self.yuri_2 = yuri_2
                self.yuri_3 = yuri_3

image enter_m_poem_paper = "assets/backgrounds/poem.jpg"

transform enter_m_poem_paper_position:
    truecenter

style enter_m_poem_vbox:
    xalign 0.5

style enter_m_poem_viewport:
    xanchor 0
    xsize 720
    ysize 650
    xpos 280
    ypos 20

style enter_m_poem_vbar is vscrollbar:
    xpos 1000
    yalign 0.5
    ysize 680

style enter_m_poem_mc_text:
    font "assets/gui/font/Halogen.ttf"
    size 30
    color "#000"
    outlines []
    line_leading 4

style enter_m_poem_monika_text:
    font "assets/gui/font/m1.TTF"
    size 34
    color "#000"
    outlines []

style enter_m_poem_default_text:
    font "assets/gui/font/Halogen.ttf"
    size 30
    color "#000"
    outlines []
    line_leading 4

# The poem display: paper image + a scrollable viewport of the title/text, with
# the handwriting style chosen by currentpoem.author. Shown by enter_m_showpoem.
screen enter_m_poem(currentpoem, paper="enter_m_poem_paper"):
    style_prefix "enter_m_poem"

    vbox:
        add paper at enter_m_poem_paper_position

    viewport id "vp":
        child_size (710, None)
        mousewheel True
        draggable True
        has vbox

        null height 40

        if currentpoem.author == "monika":
            text "[currentpoem.title]\n\n[currentpoem.text]" style "enter_m_poem_monika_text"
        elif currentpoem.author == "mc":
            text "[currentpoem.title]\n\n[currentpoem.text]" style "enter_m_poem_mc_text"
        else:
            text "[currentpoem.title]\n\n[currentpoem.text]" style "enter_m_poem_default_text"

        null height 100

    vbar value YScrollValue(viewport="vp") style "enter_m_poem_vbar"


# PUBLIC: present a poem and block until the player clicks it away.
# Saves/disables auto-forward (afm) so a poem can't auto-advance and shows the
# one-time dismiss hint on the very first poem.
label enter_m_showpoem(poem=None):
    if poem == None:
        return

    play sound page_turn
    window hide(None)
    $ _enter_m_poem_prev_afm = renpy.game.preferences.afm_enable
    $ renpy.game.preferences.afm_enable = False

    show screen enter_m_poem(poem)

    if not persistent.first_poem:
        $ persistent.first_poem = True
        $ renpy.save_persistent()
        show expression "assets/gui/poem_dismiss.png" as poem_dismiss:
            xpos 1050
            ypos 590

    with Dissolve(1)
    $ pause()

    hide screen enter_m_poem
    hide poem_dismiss
    $ renpy.game.preferences.afm_enable = _enter_m_poem_prev_afm
    with Dissolve(.5)
    return
