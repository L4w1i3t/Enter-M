# Music Room Addon
# Provides a music player for listening to the mod's soundtrack

init python:
    class MusicTrack:
        def __init__(self, title, artist, file_path):
            self.title = title
            self.artist = artist
            self.file_path = file_path
            self.is_unlocked = True

    music_library = []

    def init_music_library():
        global music_library
        music_library = [
            MusicTrack(
                "The Way Home",
                "San-Z Studio",
                "mod_assets/bgm/roster_place.ogg"
            ),
            # Add more tracks here as they become available
            MusicTrack(
                "13 AM",
                "Toby Fox",
                "mod_assets/bgm/13am.ogg"
            ),
            MusicTrack(
                "12 AM",
                "Toby Fox",
                "mod_assets/bgm/12am.ogg"
            ),
            MusicTrack(
                "Can You Feel",
                "Torchkas",
                "mod_assets/bgm/map003.ogg"
            ),
            MusicTrack(
                "Hymn of the Righteous",
                "Intelligent Systems",
                "mod_assets/bgm/hotr.ogg"
            ),
            MusicTrack(
                "Proud Flight",
                "Intelligent Systems",
                "mod_assets/bgm/flight.ogg"
            ),
            MusicTrack(
                "The Devoted",
                "Intelligent Systems",
                "mod_assets/bgm/devoted.ogg"
            ),
            MusicTrack(
                "Grandma",
                "Square Enix",
                "mod_assets/bgm/grandma.mp3"
            ),
            MusicTrack(
                "The Incomplete Stone",
                "Square Enix",
                "mod_assets/bgm/stone.mp3"
            ),
            MusicTrack(
                "City of Commerce",
                "Square Enix",
                "mod_assets/bgm/seafront.mp3"
            ),
            MusicTrack(
                "Fleeting Words - Family",
                "Square Enix",
                "mod_assets/bgm/family.mp3"
            ),
            MusicTrack(
                "Snow in Summer",
                "Square Enix",
                "mod_assets/bgm/sis.mp3"
            ),
            MusicTrack(
                "Song of the Ancients - Devola",
                "Square Enix",
                "mod_assets/bgm/devola.mp3"
            ),
            MusicTrack(
                "Song of the Ancients - Popola",
                "Square Enix",
                "mod_assets/bgm/popola.mp3"
            ),
            MusicTrack(
                "Song of the Ancients - Hollow Dreams",
                "Square Enix",
                "mod_assets/bgm/hollow.mp3"
            ),
            MusicTrack(
                "This Dream",
                "Square Enix",
                "mod_assets/bgm/dream.mp3"
            ),
            MusicTrack(
                "Beautiful Days (16-bit)",
                "Spike Chunsoft",
                "mod_assets/bgm/beautiful.mp3"
            ),
            MusicTrack(
                "All Star Apologies (16-bit)",
                "Spike Chunsoft",
                "mod_assets/bgm/apology.mp3"
            ),
            MusicTrack(
                "Dump",
                "Toby Fox",
                "mod_assets/bgm/dump.ogg"
            ),
            MusicTrack(
                "Temple of Drifting Sands",
                "Square Enix",
                "mod_assets/bgm/sands.mp3"
            ),
            MusicTrack(
                "Wretched Automatons",
                "Square Enix",
                "mod_assets/bgm/automatons.mp3"
            ),
            MusicTrack(
                "Blu Bird",
                "Square Enix",
                "mod_assets/bgm/blubird.mp3"
            ),
            MusicTrack(
                "60% Daily Fantasy",
                "San-Z Studio",
                "mod_assets/bgm/dailyfantasy.ogg"
            ),
            MusicTrack(
                "60% Fantasy Passion",
                "San-Z Studio",
                "mod_assets/bgm/fantasypassion.ogg"
            ),
            MusicTrack(
                "60% Daily Leisure",
                "San-Z Studio",
                "mod_assets/bgm/dailyleisure.ogg"
            ),
            MusicTrack(
                "60% Daily",
                "San-Z Studio",
                "mod_assets/bgm/daily.ogg"
            ),
            MusicTrack(
                "60% Fantasy Serenity",
                "San-Z Studio",
                "mod_assets/bgm/fantasyserenity.ogg"
            ),
            MusicTrack(
                "Scheduled Programming",
                "L4w1i3t",
                "mod_assets/bgm/holdmusic.ogg"
            ),
            MusicTrack(
                "Black Knife (Remix)",
                "Anthony Lo Re, Toby Fox",
                "mod_assets/bgm/epicbattlephase1.ogg"
            ),
            MusicTrack(
                "Guardian (Remix)",
                "Anthony Lo Re, Toby Fox",
                "mod_assets/bgm/epicbattlephase2.ogg"
            ),
        ]

    current_track = None
    is_playing = False
    music_current_cg = None

    def pick_random_cg():
        """Return the path of a random unlocked CG, or None if none exist yet."""
        import random
        try:
            unlocked = [
                cg.image_path
                for act in cg_gallery_catalog
                for ch in act.chapters
                for cg in ch.cgs
                if cg.unlocked
            ]
        except Exception:
            unlocked = []
        return random.choice(unlocked) if unlocked else None

    def format_time(seconds):
        if seconds is None or seconds < 0:
            return "0:00"
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return "{}:{:02d}".format(minutes, secs)

    def play_track(track):
        """Play a specific track from the library."""
        global current_track, is_playing, music_current_cg
        current_track = track
        is_playing = True
        music_current_cg = pick_random_cg()
        renpy.music.play("<loop 0>" + track.file_path, channel="music")
        renpy.restart_interaction()

    def play_next_track():
        global current_track, is_playing
        if not music_library:
            return
        if current_track is None:
            idx = 0
        else:
            try:
                idx = (music_library.index(current_track) + 1) % len(music_library)
            except ValueError:
                idx = 0
        current_track = music_library[idx]
        is_playing = True
        music_current_cg = pick_random_cg()
        renpy.music.play("<loop 0>" + current_track.file_path, channel="music")
        renpy.restart_interaction()

    def play_previous_track():
        global current_track, is_playing
        if not music_library:
            return
        if current_track is None:
            idx = 0
        else:
            try:
                idx = (music_library.index(current_track) - 1) % len(music_library)
            except ValueError:
                idx = 0
        current_track = music_library[idx]
        is_playing = True
        music_current_cg = pick_random_cg()
        renpy.music.play("<loop 0>" + current_track.file_path, channel="music")
        renpy.restart_interaction()

    def toggle_playback():
        """Toggle play/pause. Resumes current track or starts first track."""
        global current_track, is_playing
        if is_playing:
            is_playing = False
            renpy.music.stop(channel="music")
        else:
            if current_track is None and music_library:
                current_track = music_library[0]
            if current_track:
                is_playing = True
                renpy.music.play("<loop 0>" + current_track.file_path, channel="music")
        renpy.restart_interaction()

    def leave_music_room():
        """Clean exit: stop playback, restore archive BGM, hide screen."""
        global current_track, is_playing
        is_playing = False
        current_track = None
        renpy.music.play("<loop 0>mod_assets/bgm/roster_place.ogg", channel="music")
        renpy.hide_screen("music_room")

    def music_time_current(st, at):
        """DynamicDisplayable callback for current position."""
        pos = renpy.music.get_pos(channel="music")
        if pos is None:
            pos = 0.0
        return Text(format_time(pos), style="music_time"), 0.1

    def music_time_total(st, at):
        """DynamicDisplayable callback for total duration."""
        duration = renpy.music.get_duration(channel="music")
        if duration is None or duration <= 0:
            duration = 0.0
        return Text(format_time(duration), style="music_time"), 1.0

init 5 python:
    init_music_library()

# Named transforms for music room
transform music_frame_enter:
    on show:
        alpha 0.0
        yoffset -40
        easein_back 0.4 alpha 1.0 yoffset 0
    on hide:
        alpha 1.0
        easeout_quad 0.25 alpha 0.0 yoffset -25

transform music_panel_left:
    alpha 0.0
    xoffset -25
    pause 0.15
    easein 0.35 alpha 1.0 xoffset 0

transform music_panel_right:
    alpha 0.0
    xoffset 25
    pause 0.15
    easein 0.35 alpha 1.0 xoffset 0

# Music Room Main Screen
screen music_room():
    modal True

    # Stop the archive BGM on open (the player will handle its own audio)
    on "show" action Function(renpy.music.stop, channel="music")

    use archive_backdrop

    key "game_menu" action Function(leave_music_room)
    key "K_ESCAPE" action Function(leave_music_room)

    frame:
        style "archive_shell_frame"
        at music_frame_enter

        vbox:
            spacing 14

            use archive_header("MUSIC ROOM", Function(leave_music_room))

            add Solid("#56d7ff66"):
                xsize 1150
                ysize 2
                xalign 0.5

            null height 2

            hbox:
                spacing 18
                xalign 0.5

                frame:
                    style "music_list_frame"
                    at music_panel_left

                    vbox:
                        spacing 5

                        frame:
                            background Solid("#07111dcc")
                            xfill True
                            padding (12, 7)

                            text "TRACK LIST" style "music_list_header"

                        null height 5

                        # Scrollable track list
                        viewport:
                            style_prefix "cs_sv"
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            pagekeys True
                            xsize 530
                            ysize 420

                            vbox:
                                spacing 6
                                xsize 510

                                for idx, track in enumerate(music_library):
                                    $ _is_active = (track == current_track)

                                    button:
                                        style "music_track_button"
                                        if _is_active:
                                            background Solid("#12314af2")
                                            hover_background Solid("#17415fee")
                                        action Function(play_track, track)
                                        at transform:
                                            on show:
                                                alpha 0.0
                                                xoffset 15
                                                pause idx * 0.05
                                                easein 0.25 alpha 1.0 xoffset 0

                                        hbox:
                                            spacing 12

                                            $ _tnum = idx + 1
                                            text "[_tnum]." style "music_track_number"

                                            vbox:
                                                spacing 2
                                                text track.title style "music_track_title"
                                                text track.artist style "music_track_artist"

                frame:
                    style "music_player_frame"
                    at music_panel_right

                    vbox:
                        spacing 10
                        xalign 0.5

                        frame:
                            background Solid("#07111dcc")
                            xfill True
                            padding (12, 7)

                            text "NOW PLAYING" style "music_player_header"

                        null height 5

                        # Visualization area — random CG thumbnail
                        frame:
                            xsize 340
                            ysize 150
                            xalign 0.5
                            background Solid("#07101add")
                            padding (0, 0, 0, 0)

                            if music_current_cg:
                                add music_current_cg:
                                    fit "cover"
                                    xsize 340
                                    ysize 150
                                    xalign 0.5
                                    yalign 0.5
                            else:
                                text "No Track Selected" style "music_no_track"

                        null height 5

                        # Track info (always rendered, placeholder when empty)
                        vbox:
                            spacing 5
                            xalign 0.5
                            xsize 340

                            if current_track:
                                text current_track.title style "music_now_playing_title"
                                text current_track.artist style "music_now_playing_artist"
                            else:
                                text "---" style "music_now_playing_title"
                                text " " style "music_now_playing_artist"

                            null height 4

                            # Progress bar
                            bar:
                                value AudioPositionValue(channel="music")
                                xsize 320
                                ysize 6
                                xalign 0.5
                                left_bar Solid("#56d7ff")
                                right_bar Solid("#102338")
                                thumb None
                                thumb_offset 0

                            # Time display
                            hbox:
                                xsize 320
                                xalign 0.5

                                add DynamicDisplayable(music_time_current)

                                text " " xalign 0.5

                                add DynamicDisplayable(music_time_total):
                                    xalign 1.0

                        null height 5

                        # Player controls (using text labels that all fonts support)
                        hbox:
                            spacing 15
                            xalign 0.5

                            textbutton "|<<":
                                style "music_control_button"
                                action Function(play_previous_track)

                            $ _play_label = "||" if is_playing else ">"
                            textbutton _play_label:
                                style "music_play_button"
                                action Function(toggle_playback)

                            textbutton ">>|":
                                style "music_control_button"
                                action Function(play_next_track)

# Styles
style music_room_frame:
    xalign 0.5
    yalign 0.5
    xsize 950
    ysize 620
    background Solid("#050811e8")
    padding (25, 18)

style music_room_title:
    font "mod_assets/fonts/SF Automaton Extended.ttf"
    size 34
    color "#f4fbff"
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]


style music_list_frame:
    xsize 560
    ysize 520
    background Solid("#07101add")
    padding (10, 10)

style music_list_header:
    font gui.interface_font
    size 20
    color "#f4fbff"
    xalign 0.5
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style music_track_button:
    xsize 510
    ysize 52
    background Solid("#07111dcc")
    hover_background Solid("#12314aee")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (10, 8)

style music_track_number:
    font gui.interface_font
    color "#56d7ff"
    size 18
    bold True
    outlines [(1, "#02040b", 0, 0)]

style music_track_title:
    font gui.interface_font
    color "#dff8ff"
    size 17
    bold True
    outlines [(1, "#02040b", 0, 0)]

style music_track_artist:
    font gui.interface_font
    color "#9fc9d6"
    size 13
    outlines [(1, "#02040b", 0, 0)]

style music_player_frame:
    xsize 440
    ysize 520
    background Solid("#07101add")
    padding (10, 10)

style music_player_header:
    font gui.interface_font
    size 20
    color "#f4fbff"
    xalign 0.5
    bold True
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style music_visualizer:
    font gui.interface_font
    size 90
    color "#56d7ff"
    xalign 0.5
    yalign 0.5
    outlines [(2, "#02040b", 0, 0)]

style music_no_track:
    font gui.interface_font
    size 20
    color "#687787"
    xalign 0.5
    yalign 0.5
    outlines [(1, "#02040b", 0, 0)]

style music_now_playing_title:
    font gui.interface_font
    size 20
    color "#dff8ff"
    xalign 0.5
    text_align 0.5
    bold True
    outlines [(1, "#02040b", 0, 0)]

style music_now_playing_artist:
    font gui.interface_font
    size 16
    color "#9fc9d6"
    xalign 0.5
    text_align 0.5
    outlines [(1, "#02040b", 0, 0)]

style music_time:
    font gui.interface_font
    size 14
    color "#9fc9d6"
    outlines [(1, "#02040b", 0, 0)]

style music_control_button:
    xysize (55, 55)
    background Solid("#07111dcc")
    hover_background Solid("#12314af2")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound
    padding (8, 8)

style music_control_button_text:
    font gui.interface_font
    size 22
    color "#dff8ff"
    xalign 0.5
    yalign 0.5
    outlines [(2, "#02040b", 0, 0), (1, "#56d7ff88", 1, 1)]

style music_play_button is music_control_button:
    xysize (65, 55)

style music_play_button_text is music_control_button_text:
    size 24
