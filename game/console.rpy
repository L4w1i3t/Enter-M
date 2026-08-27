# Define the appearance of the console background
image console_bg:
    "#333"                      # Dark gray background
    topleft                     # Positioned at the top-left corner
    alpha 0.75 size (480,180)   # 75% opacity, 480x180 pixel size

# Style definition for console text
style console_text:
    font "assets/gui/font/F25_Bank_Printer.ttf"   # Typewriter-style font
    color "#fff"                         # White text
    size 18                                # Font size
    outlines []                            # No text outlines

# Style for animated text that appears as typing
style console_text_console is console_text:
    slow_cps 30                            # Character-per-second typing speed

# Initialize the console history as an empty list
default consolehistory = []

# Create the main text area where commands are displayed
image console_text = ParameterizedText(style="console_text_console", anchor=(0,0), xpos=30, ypos=10)

# Create the history text area that shows previous commands
image console_history = ParameterizedText(style="console_text", anchor=(0,0), xpos=30, ypos=50)

# Create the command prompt caret ">"
image console_caret = Text(">", style="console_text", anchor=(0,0), xpos=5, ypos=10)

# Main function to update the console with new text
label updateconsole(text="", history=""):
    show console_bg zorder 100             # Show console background (high zorder to be on top)
    show console_caret zorder 100          # Show the command prompt
    show console_text "_" as ctext zorder 100  # Show initial cursor
    show console_text "[text]" as ctext zorder 100  # Show the command text
    $ pause(len(text) / 30.0 + 0.5)        # Pause proportional to text length to simulate typing
    hide ctext                             # Hide the text
    show console_text "_" as ctext zorder 100  # Show just the cursor again
    call updateconsolehistory (history) from _call_updateconsolehistory    # Update the history with new text
    $ pause(0.5)                           # Brief pause before continuing
    return

# Function to update the command history section
label updateconsolehistory(text=""):
    if text:
        python:
            consolehistory.insert(0, text)  # Add new history item at the beginning
            if len(consolehistory) > 5:     # Limit history to 5 items
                del consolehistory[5:]
            # Convert history list to a displayed string with line breaks
            consolehistorydisplay = '\n'.join(map(str, consolehistory))
        # Show the history text
        show console_history "[consolehistorydisplay]" as chistory zorder 100
    return

# Function to hide all console elements
label hideconsole:
    hide console_bg      # Hide background
    hide console_caret   # Hide prompt
    hide ctext           # Hide current text
    hide chistory        # Hide history