# Common materials for the illustrated menu family. Actual reading surfaces
# are cached SVG images; decoration adds no ongoing render callback or shader.
define -90 IM_INK = "#263238"
define -90 IM_PAPER = "#f0e6d2"
define -90 IM_MUTED = "#b9b5aa"
define -90 IM_PLUM = "#c5a0bd"
define -90 IM_GOLD = "#e1bf80"
define -90 IM_PAPER_PANEL = Frame("assets/gui/menu/illustrated/paper_panel.svg", 16, 16)
define -90 IM_DARK_PANEL = Frame("assets/gui/menu/illustrated/dark_panel.svg", 16, 16)
define -90 IM_TAB_IDLE = Frame("assets/gui/menu/illustrated/tab_idle.svg", 20, 16)
define -90 IM_TAB_HOVER = Frame("assets/gui/menu/illustrated/tab_hover.svg", 20, 16)
define -90 IM_TAB_SELECTED = Frame("assets/gui/menu/illustrated/tab_selected.svg", 20, 16)
define -90 IM_RETURN_IDLE = IM_TAB_IDLE
define -90 IM_RETURN_HOVER = IM_TAB_HOVER

screen illustrated_menu_backdrop(kind="archive"):
    add illustrated_menu_backdrop(kind)

screen illustrated_menu_motif(kind="archive", w=180, h=200):
    add illustrated_menu_motif(kind, w, h)

style im_notice_button is button:
    background IM_TAB_IDLE
    hover_background IM_TAB_HOVER
    xsize 180
    yminimum 48
    padding (18, 10)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style im_notice_button_text is default:
    font gui.interface_font
    size 20
    color IM_PAPER
    hover_color "#ffffff"
    outlines []
    align (0.5, 0.5)

init -90 python:
    # Displayable factories also support add-with-position at call sites. Screen
    # names live in Ren'Py's screen registry, separately from these store names.
    _im_backdrops = {kind: Image("assets/gui/menu/illustrated/backdrop_" + kind + ".svg") for kind in ("archive", "arcade", "chapter", "credits")}
    _im_motifs = {kind: Image("assets/gui/menu/illustrated/motif_" + kind + ".svg") for kind in ("archive", "arcade", "chapter", "credits")}

    def illustrated_menu_backdrop(kind="archive"):
        return _im_backdrops[kind]

    def illustrated_menu_motif(kind="archive", w=180, h=200):
        return Transform(_im_motifs[kind], xysize=(w, h), fit="contain")

    _im_title_prediction = (
        "assets/gui/first_boot/opening_seal.svg",
        "assets/gui/menu/illustrated/paper_panel.svg",
        "assets/gui/menu/illustrated/dark_panel.svg",
        "assets/gui/menu/illustrated/tab_idle.svg",
        "assets/gui/menu/illustrated/tab_hover.svg",
        "assets/gui/menu/illustrated/tab_selected.svg",
        "assets/gui/menu/illustrated/backdrop_credits.svg",
        "assets/gui/menu/illustrated/motif_credits.svg",
        "assets/gui/menu/illustrated/credits/binding.svg",
        "assets/gui/menu/illustrated/credits/section_tab.svg",
        "assets/gui/menu/illustrated/credits/section_tab_selected.svg",
        # Cold traces found these initial Arcade plates and covers loading on
        # the UI thread after the click. Prewarm just the visible collection.
        "assets/gui/menu/illustrated/arcade/surround.svg",
        "assets/gui/menu/illustrated/arcade/joystick.svg",
        "assets/gui/menu/illustrated/arcade/feature_mat.svg",
        "assets/gui/menu/illustrated/arcade/shelf.svg",
        "assets/gui/menu/illustrated/arcade/play_hover.svg",
        "assets/gui/menu/illustrated/arcade/cartridge_trim.svg",
        "addons/Arcade/art/ontological_seer_classic.webp",
        "addons/Arcade/art/thumbs/ontological_seer_classic.webp",
        "addons/Arcade/art/thumbs/ontological_seer_id_classic.webp",
        "addons/Arcade/art/thumbs/a_fine_date_classic.webp",
        "addons/Arcade/art/thumbs/embodiment_of_violet_ink_doujin.webp",
        "addons/Arcade/art/thumbs/the_unwritten_act_ui.webp",
        "addons/Arcade/art/thumbs/ouroboros_protocol_classic.webp",
        "addons/Arcade/art/thumbs/peer_review_classic.webp",
    )

    def illustrated_menu_predict():
        # Prewarm shared art while the title is visible. The SDK deduplicates
        # registrations; no session latch can outlive the store on full_restart.
        # Predict images only, without evaluating menu actions or unlock state.
        renpy.start_predict(*_im_title_prediction)

    def illustrated_menu_stop_predict():
        # Cached images remain available, but menu-only registrations must not
        # follow the player through every later gameplay interaction.
        renpy.stop_predict(*_im_title_prediction)
