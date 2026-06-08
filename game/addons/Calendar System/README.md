# Calendar System Addon

A Persona-style calendar system for Ren'Py visual novels that tracks and displays the in-game date.

## Features

- **Date Tracking**: Track in-game dates with day, month, and year internally
- **Multiple Display Styles**: Choose from Persona-style, minimal, or bottom overlay
- **Day of Week**: Automatically calculates and displays day names
- **Weekend Detection**: Different colors for weekends vs weekdays
- **Easy Integration**: Simple functions to advance time and change dates
- **Customizable**: Easily modify appearance and behavior

## Quick Start

### 1. Basic Usage

The calendar is automatically initialized and displayed when the game starts.

```renpy
# Advance by one day
$ calendar.advance_day()

# Advance by multiple days
$ calendar.advance_day(7)

# Set a specific date
$ calendar.set_date(2025, 6, 15)  # June 15, 2025
```

### 2. Display Control

```renpy
# Hide the calendar
$ calendar.hide()

# Show the calendar
$ calendar.show()

# Toggle visibility
$ calendar.toggle_display()
```

### 3. Get Date Information

```renpy
# Get formatted date string
$ date_text = calendar.get_formatted_date("full")
# Returns: "Monday, April 7"

$ date_text = calendar.get_formatted_date("persona")
# Returns: "4/7 (MON)"

# Check if weekend
$ is_weekend = calendar.is_weekend()

# Get individual components
$ day = calendar.get_day()
$ month = calendar.get_month()
$ year = calendar.get_year()
$ day_name = calendar.get_day_name()
```

## Display Styles

### Default (Persona-style, top-right)
```renpy
show screen calendar_overlay
```

### Minimal (compact, top-right)
```renpy
show screen calendar_overlay_minimal
```

### Bottom (full width, bottom center)
```renpy
show screen calendar_overlay_bottom
```

## Customization

### Change Starting Date

Edit in `calendar_system.rpy`:
```python
self.current_date = datetime.date(2025, 4, 7)  # Change to your desired start date
```

### Include Year In Full Date Strings

```renpy
$ calendar.show_year = True
```

Screen overlays and the Calendar menu remain yearless; the year is still stored for continuous calendar math.

### Change Colors

Edit the screen definitions in `calendar_system.rpy` to change colors:
- `#ffffff` - White (main text)
- `#ffdd55` - Yellow (day number)
- `#88ccff` - Light blue (weekdays)
- `#ff8888` - Light red (weekends)

## Integration Examples

### Scene transitions with date advancement

```renpy
label morning_routine:
    scene bg bedroom
    show screen calendar_overlay
    "Another day begins..."
    
    # ... scene content ...
    
    jump afternoon
    
label afternoon:
    $ calendar.advance_day()
    scene bg school
    "The next day at school..."
```

### Conditional events based on day

```renpy
if calendar.get_day_of_week() == 0:  # Monday
    "It's Monday, time for club meeting!"
elif calendar.is_weekend():
    "Finally, the weekend!"
```

### Time skip

```renpy
menu:
    "Skip to next week?":
        "Yes":
            $ calendar.advance_day(7)
            "A week has passed..."
        "No":
            "Continuing current day..."
```

## Developer Menu Integration

Add to your dev_scene_manager or similar:

```renpy
label dev_calendar_test:
    menu:
        "Test Calendar System":
            
            "Advance 1 Day":
                $ calendar.advance_day()
                "[calendar.get_formatted_date('full')]"
            
            "Advance 1 Week":
                $ calendar.advance_day(7)
                "[calendar.get_formatted_date('full')]"
            
            "Set to Random Date":
                $ calendar.set_date(2025, 8, 15)
                "[calendar.get_formatted_date('full')]"
            
            "Toggle Display":
                $ calendar.toggle_display()
            
            "Return":
                return
    
    jump dev_calendar_test
```

## Notes

- The calendar persists across saves
- Dates are stored as Python datetime objects for accuracy
- Leap years are automatically handled
- Weekend detection works for any date
