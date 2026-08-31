##### GUI/Visual Settings #####

# Set init offset to -2 so these definitions happen before other init blocks
init offset = -2

init python:
    # Initialize the GUI with the game's resolution
    gui.init(1280, 720)

# Sound effects for UI interactions
define gui.hover_sound = audio.uihover          # Sound when hovering over buttons
define gui.activate_sound = audio.uiselect      # Sound when selecting buttons

# Color scheme for the interface
define gui.accent_color = '#56d7ff'                   # Primary accent color
define gui.idle_color = '#b8c7cf'                     # Color for inactive elements
define gui.idle_small_color = '#75838d'               # Color for small inactive elements
define gui.hover_color = '#ff315b'                    # Color when hovering over elements
define gui.selected_color = '#f4fbff'                 # Color for selected elements
define gui.insensitive_color = '#6d78847f'            # Color for disabled elements
define gui.muted_color = '#16303d'                    # Color for background elements
define gui.hover_muted_color = '#245366'              # Hover color for background elements
define gui.text_color = '#eef7f4'                     # Default text color
define gui.interface_text_color = '#eaf8ff'           # Color for interface text

# Fonts used throughout the game
# -----------------------------------------------------------------------------
# GLYPH COVERAGE -- READ THIS BEFORE TYPING A NON-ASCII CHARACTER INTO A `text`
#
# These three fonts are display faces, not text faces. Measured from their cmap
# tables (2026-08-05): Myanmar has 197 codepoints, SF Automaton 224, NovaSquare
# 418. Matsu'Py does NOT fall back to another font -- a missing glyph is drawn as
# an empty rectangle, on screen, in the shipped game.
#
#   SAFE EVERYWHERE  ASCII, and the prose punctuation the writing actually uses:
#                    em dash (which config.replace_text generates from every
#                    "--" in dialogue -- see options.rpy), curly quotes, bullet.
#   INTERFACE ONLY   the advance/choice arrow is U+2023 TRIANGULAR BULLET and it
#                    only draws in gui.interface_font. Every U+25Bx arrow
#                    (25B6 25B8 25BA 25B7) is a box in ALL THREE fonts, as is
#                    the ellipsis U+2026 outside the interface font.
#   NOT IN ANY OF    geometric shapes, stars, hearts, technical symbols. If a
#   THEM             screen needs those it must name a font that has them --
#                    "DejaVuSans.ttf" (~5900 codepoints, and what Hina's World
#                    already uses via hw_font). Even DejaVu lacks U+23FB.
#
# When in doubt draw the icon out of rects the way the phone's hang-up handset
# is drawn (addons/Phone System/call.rpy), or fall back to ASCII.
# -----------------------------------------------------------------------------
define gui.default_font = "assets/fonts/Myanmar.otf"     # Default dialogue font
define gui.name_font = "assets/fonts/SF Automaton Extended.ttf" # Font for character names
define gui.interface_font = "assets/fonts/NovaSquare-Regular.ttf"   # Font for UI elements

# Text sizes for different parts of the interface
define gui.text_size = 25                             # Size of dialogue text
define gui.say_text_size = 23                         # Size of textbox dialogue text
define gui.name_text_size = 23                        # Size of character names
define gui.interface_text_size = 21                   # Size of interface text
define gui.label_text_size = 30                       # Size of section labels
define gui.notify_text_size = 16                      # Size of notification text
define gui.title_text_size = 42                       # Size of title text

# Background images for menus
define gui.main_menu_background = "enter_m_main_menu_bg"  # Interactive title-screen background
define gui.game_menu_background = "enter_m_game_menu_bg"  # Interactive pause/submenu background

# Show game title in main menu
define gui.show_name = False

# Text box settings
define gui.textbox_height = 182                       # Height of dialogue box
define gui.textbox_yalign = 0.99                      # Vertical position of dialogue box

# Name box position and size
define gui.name_xpos = 350                            # Horizontal position of name box
define gui.name_ypos = -3                             # Vertical position of name box
define gui.name_xalign = 0.5                          # Horizontal alignment of name text
define gui.namebox_width = 168                        # Width of name box
define gui.namebox_height = 39                        # Height of name box
define gui.namebox_borders = Borders(5, 5, 5, 2)      # Border size around name box
define gui.namebox_tile = False                       # Whether to tile the namebox background

# Dialogue text position and size
define gui.text_xpos = 260                            # Horizontal position of dialogue text
define gui.text_ypos = 53                             # Vertical position of dialogue text
define gui.text_width = 760                           # Width of dialogue text area
define gui.text_xalign = 0.0                          # Horizontal alignment of dialogue text

# Button appearance settings
define gui.button_width = None                        # Default button width (None = auto)
define gui.button_height = 40                         # Default button height
define gui.button_borders = Borders(12, 5, 12, 5)     # Border size around buttons
define gui.button_tile = False                        # Whether to tile button backgrounds
define gui.button_text_font = gui.interface_font      # Button text font
define gui.button_text_size = gui.interface_text_size # Button text size
define gui.button_text_idle_color = gui.idle_color    # Button text color when inactive
define gui.button_text_hover_color = gui.hover_color  # Button text color when hovered
define gui.button_text_selected_color = gui.selected_color  # Button text color when selected
define gui.button_text_insensitive_color = gui.insensitive_color  # Button text color when disabled
define gui.button_text_xalign = 0.5                   # Button text horizontal alignment

# Radio and check buttons
define gui.radio_button_borders = Borders(28, 4, 4, 4)  # Radio button borders
define gui.check_button_borders = Borders(28, 4, 4, 4)  # Checkbox borders

# Confirm button text alignment
define gui.confirm_button_text_xalign = 0.5           # Center confirm button text

# Page navigation buttons
define gui.page_button_borders = Borders(10, 4, 10, 4)  # Page button borders

# Quick menu buttons (bottom of screen during gameplay)
define gui.quick_button_text_size = 14                # Quick button text size
define gui.quick_button_text_idle_color = "#d6e6ee"   # Quick button inactive color
define gui.quick_button_text_hover_color = "#ff315b"  # Quick button hover color
define gui.quick_button_text_selected_color = gui.accent_color  # Quick button selected color
define gui.quick_button_text_insensitive_color = "#66727b"  # Quick button disabled color

# Choice buttons (dialogue choices)
define gui.choice_button_width = 720                  # Choice button width
define gui.choice_button_height = None                # Choice button height
define gui.choice_button_tile = False                 # Whether to tile choice backgrounds
define gui.choice_button_borders = Borders(24, 12, 24, 12)  # Choice button borders
define gui.choice_button_text_font = gui.default_font  # Choice text font
define gui.choice_button_text_size = gui.text_size     # Choice text size
define gui.choice_button_text_xalign = 0.5             # Choice text alignment
define gui.choice_button_text_idle_color = "#eef7f4"   # Choice text color when inactive
define gui.choice_button_text_hover_color = "#ff315b"  # Choice text color when hovered

# Save/load slot buttons
# NOTE: dead since the RECORD BANK replaced the save/load grid -- these dressed
# `screen file_slots`, which no longer exists. The bank draws its own rows and
# sizes them from the EMB_* constants in game/data_bank.rpy. Left in place
# because they are stock Ren'Py GUI names and something in the SDK's own
# common screens may still read one.
define gui.slot_button_width = 270                     # Save slot width
define gui.slot_button_height = 206                    # Save slot height
define gui.slot_button_borders = Borders(12, 12, 12, 12)  # Save slot borders
define gui.slot_button_text_size = 14                  # Save slot text size
define gui.slot_button_text_xalign = 0.5               # Save slot text alignment
define gui.slot_button_text_idle_color = gui.idle_small_color  # Save slot inactive color
define gui.slot_button_text_hover_color = gui.hover_color      # Save slot hover color

# Save thumbnails
# Sized to draw 1:1 on the record bank's monitor glass (EMB_SHOT_W/H), so a
# save written from here needs no rescaling to be previewed. Saves written
# before this change carry a 256x144 thumbnail and are scaled up to fit.
define config.thumbnail_width = 416                    # Save thumbnail width
define config.thumbnail_height = 234                   # Save thumbnail height

# Save/load screen grid layout
# Also dead with `screen file_slots`. The bank is one flat scrolling list of
# EMB_SLOTS records; gui.file_slot_cols * gui.file_slot_rows only survives as
# the page size Ren'Py names slots by, which the bank hardcodes as EMB_PER_PAGE
# so that changing these can never rename an existing save file.
define gui.file_slot_cols = 3                          # Number of save slots per row
define gui.file_slot_rows = 2                          # Number of rows of save slots

# Positioning
define gui.navigation_xpos = 64                        # Position of navigation buttons
define gui.skip_ypos = 18                              # Position of skip indicator
define gui.notify_ypos = 26                            # Position of notifications

# Spacing
define gui.choice_spacing = 22                         # Spacing between choice buttons
define gui.navigation_spacing = 8                      # Spacing between navigation buttons
define gui.pref_spacing = 10                           # Spacing in preferences screens
define gui.pref_button_spacing = 0                     # Spacing between preference buttons
define gui.page_spacing = 0                            # Spacing between page buttons
define gui.slot_spacing = 16                           # Spacing between save slots

# Frames (borders around UI elements)
define gui.frame_borders = Borders(18, 18, 18, 18)     # Standard frame borders
define gui.confirm_frame_borders = Borders(34, 28, 34, 28)  # Confirm dialog borders
define gui.skip_frame_borders = Borders(18, 7, 18, 7)  # Skip indicator borders
define gui.notify_frame_borders = Borders(18, 7, 18, 7)  # Notification borders
define gui.frame_tile = False                          # Whether to tile frame backgrounds

# Bars, scrollbars, and sliders
define gui.bar_size = 28                               # Size of bars (like health)
define gui.scrollbar_size = 12                         # Size of scrollbars
define gui.slider_size = 30                            # Size of sliders
define gui.bar_tile = False                            # Whether to tile bar images
define gui.scrollbar_tile = False                      # Whether to tile scrollbar images
define gui.slider_tile = False                         # Whether to tile slider images
define gui.bar_borders = Borders(4, 4, 4, 4)           # Bar borders
define gui.scrollbar_borders = Borders(4, 4, 4, 4)     # Scrollbar borders
define gui.slider_borders = Borders(4, 4, 4, 4)        # Slider borders
define gui.vbar_borders = Borders(4, 4, 4, 4)          # Vertical bar borders
define gui.vscrollbar_borders = Borders(4, 4, 4, 4)    # Vertical scrollbar borders
define gui.vslider_borders = Borders(4, 4, 4, 4)       # Vertical slider borders
define gui.unscrollable = "hide"                       # What to do when scrolling not needed

# History screen settings
define config.history_length = 50                      # Number of dialogue lines to keep
define gui.history_height = None                       # Height of history entries
define gui.history_name_xpos = 150                     # Name horizontal position in history
define gui.history_name_ypos = 0                       # Name vertical position in history
define gui.history_name_width = 150                    # Name width in history
define gui.history_name_xalign = 1.0                   # Name horizontal alignment in history
define gui.history_text_xpos = 170                     # Text horizontal position in history
define gui.history_text_ypos = 5                       # Text vertical position in history
define gui.history_text_width = 740                    # Text width in history
define gui.history_text_xalign = 0.0                   # Text horizontal alignment in history

# NVL mode settings (full-screen text mode)
define gui.nvl_borders = Borders(0, 10, 0, 20)         # NVL screen borders
define gui.nvl_height = 115                            # Height of NVL entries
define gui.nvl_spacing = 10                            # Spacing between NVL entries
define gui.nvl_name_xpos = 430                         # NVL name horizontal position
define gui.nvl_name_ypos = 0                           # NVL name vertical position
define gui.nvl_name_width = 150                        # NVL name width
define gui.nvl_name_xalign = 1.0                       # NVL name horizontal alignment
define gui.nvl_text_xpos = 450                         # NVL text horizontal position
define gui.nvl_text_ypos = 8                           # NVL text vertical position
define gui.nvl_text_width = 590                        # NVL text width
define gui.nvl_text_xalign = 0.0                       # NVL text horizontal alignment
define gui.nvl_thought_xpos = 240                      # NVL thought horizontal position
define gui.nvl_thought_ypos = 0                        # NVL thought vertical position
define gui.nvl_thought_width = 780                     # NVL thought width
define gui.nvl_thought_xalign = 0.0                    # NVL thought horizontal alignment
define gui.nvl_button_xpos = 450                       # NVL button horizontal position
define gui.nvl_button_xalign = 0.0                     # NVL button horizontal alignment

# Mobile/small screen adaptations
init python:

    # Touch-based devices get wider button borders for easier tapping
    if renpy.variant("touch"):
        gui.quick_button_borders = Borders(60, 14, 60, 0)

    # Small screens get larger text and adjusted UI elements
    if renpy.variant("small"):

        gui.text_size = 30
        gui.say_text_size = 28
        gui.name_text_size = 36
        gui.notify_text_size = 25
        gui.interface_text_size = 36
        gui.button_text_size = 34
        gui.label_text_size = 36

        gui.textbox_height = 240
        gui.name_xpos = 80
        gui.text_xpos = 90
        gui.text_width = 1100

        gui.choice_button_width = 1240

        gui.navigation_spacing = 20
        gui.pref_button_spacing = 10

        gui.history_height = 190
        gui.history_text_width = 690

        gui.file_slot_cols = 2
        gui.file_slot_rows = 2

        gui.nvl_height = 170
        gui.nvl_name_width = 305
        gui.nvl_name_xpos = 325
        gui.nvl_text_width = 915
        gui.nvl_text_xpos = 345
        gui.nvl_text_ypos = 5
        gui.nvl_thought_width = 1240
        gui.nvl_thought_xpos = 20
        gui.nvl_button_width = 1240
        gui.nvl_button_xpos = 20

        gui.quick_button_text_size = 20
