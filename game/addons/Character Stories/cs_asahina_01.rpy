# =============================================================================
#  cs_asahina_01.rpy  --  "Hina's World"   (DIEGETIC / NO-VN SIDE STORY)
# =============================================================================
#
#  WHAT THIS IS
#    A self-contained, *exclusively diegetic* side story. There is not a single
#    say-statement, narrator line, or character() call anywhere below. Every beat
#    is an artifact ON a simulated 2000s computer:
#        - intro            -> a Windows XP desktop + a hinasworld.exe icon
#        - "the site loads" -> a Macromedia Flash preloader bar
#        - mini-games       -> actual clickable Flash-stage screens
#        - reveals/horror   -> Windows message boxes, a popup ad, a self-typing
#                              chat window, a Notepad .txt the player reads
#        - logging off      -> the Start menu (XP-style), which is THE way out and
#                              triggers the consequence-scaled culmination
#    The horror is the machine turning on you -- never a character explaining it.
#
#  THEME  ("show, don't tell")
#    The ultimate subject is: what happens to girls (any child) who try to grow up
#    too quickly? Hina is a literal kid whose cute Flash site keeps pushing her to
#    be older -- dress older, answer older, be rated as older -- until the child
#    underneath is gone. Teenage-girl struggles (peer pressure, cyberbullying, a
#    quiet body/food sub-thread, an unsettling adult stranger) are the texture; the
#    point is the lost childhood, implied through artifacts, never narrated.
#
#  THIS ALREADY HAPPENED  (read this before touching the axes or the ending)
#    This is not a what-if and the player is not steering it. It is CANON: it
#    happened to Asahina when she was nine, years before Chapter 0.5, and the
#    player is coming across the record of it. The machine is an artifact, not
#    a simulation with the player at the controls -- which is why the ending
#    cannot be avoided, argued with, or won. Nobody in this story is waiting on
#    the player to save them, because the part where someone could have is long
#    over by the time the desktop boots.
#
#  WHAT THE CHOICES ACTUALLY DO
#    hw_grow / hw_kept_child / hw_kind / hw_cruel / hw_guest do NOT decide what
#    happens to Hina. They decide how much of it the record gives up, and in
#    what voice -- which log files exist, how plainly the diary says it, how far
#    the desktop has rotted by the time you log off. See hw_ending_tone().
#    The player is choosing how closely to look at something finished, not
#    choosing its outcome. Write every branch so that it reads as reconstruction
#    rather than authorship, and never let a line imply the player caused it.
#
#  THE CABINET (seven games)
#    Core four (required for the mom-message ending): Outfitter, Chatting,
#    Quiz Corner, Rating Game. Extra three (texture + axes, never required):
#    Lunchbox Break (the food thread), Mr Toast & Mochi (the childhood anchor --
#    the ONE game that never sours), Makeover Mirror (the mirror guesses her
#    age and the UI rewards the number going up). Each drops its own log file.
#
#  THE GUEST (escalation design)
#    xX_guest_Xx follows real grooming shape, kept deniable at every step:
#    generic praise -> useful and liked (#glitter_help) -> small asks that
#    sound like nothing (timezone) -> platform move (msn) -> isolation +
#    secrecy + the photo ask. He retreats gracefully when rebuffed, praises
#    caution, mentions work/adult life in plain sight, and echoes the site's
#    own language ("old soul"). Two-tier gallery comments: friendly and
#    publicly defensible at stage 1-2, familiar/entitled at stage 3+. His
#    persistence NEVER gates on hw_guest -- only how far Hina walks toward him
#    does. The taskbar clock creeps toward midnight as pressure rises.
#
#  GUARDRAILS
#    Lacey-Games *shape* (cute lost-Flash nostalgia -> UI wrongness -> player
#    complicity -> buried personal horror) but none of its specifics. Social horror
#    only, no gore. The stranger undertone is implied, never explicit.
# =============================================================================

# -----------------------------------------------------------------------------
#  FONT FIX
#    The mod's dialogue font (assets/fonts/Myanmar.otf) has no glyphs for the
#    2000s decorations this story leans on (star, heart, bullet, guillemet,
#    arrows), so they rendered as tofu. DejaVuSans.ttf ships with Matsu'Py, covers
#    all of them, and conveniently reads like Tahoma/Verdana -- right at home on a
#    simulated Windows XP machine. Applied to these screens via `style_prefix "hw"`
#    so every text/button-text picks it up without touching frame/button behavior.
# -----------------------------------------------------------------------------
define hw_font = "DejaVuSans.ttf"

# NOTE: the mod's `style default` (screens.rpy) puts a dark navy outline on ALL
# text. Inheriting that here made every label look heavy/muddy ("too dark"), so
# the hw_ text styles explicitly clear `outlines` for crisp 2000s-UI text.
style hw_text is text:
    font hw_font
    outlines []
style hw_button is button
style hw_button_text is button_text:
    font hw_font
    outlines []
style hw_frame is frame
style hw_viewport is viewport
style hw_vbox is vbox
style hw_hbox is hbox
style hw_fixed is fixed
style hw_grid is grid
style hw_bar is bar
style hw_vscrollbar is vscrollbar

# Fit, not cover: the 3:2 wallpaper leaves awkward sidebars on 16:9.
image hw2_xp_wallpaper = Transform("assets/backgrounds/xp.png", fit="contain", xysize=(1280, 720), xalign=0.5, yalign=0.5)

screen hw2_desktop_backdrop():
    add Solid("#000000")
    add "hw2_xp_wallpaper"

# -----------------------------------------------------------------------------
#  STATE
# -----------------------------------------------------------------------------
# Browsing state (reset on entry)
default hinas_world_page = "home"
default hinas_world_corruption = 0
default hinas_world_seen_outfitter = False
default hinas_world_seen_chatting = False
default hinas_world_seen_quiz = False
default hinas_world_seen_rating = False
default hinas_world_seen_bento = False
default hinas_world_seen_petsalon = False
default hinas_world_seen_makeover = False

# Reading axes (reset on entry). Choices don't branch the ENDING -- it already
# happened, years ago, and the record only reports it -- but they're read back
# through the desktop files, so what changes is how much of it you end up
# holding. The horror is not that you pushed her there; it's that you can watch
# the whole shape of it from the outside and it still goes exactly where it
# went. hw_guest is the sharp edge: how much of the stranger the record shows
# you before it stops being deniable.
default hw_grow = 0          # how far the site's push to grow up gets followed
default hw_kept_child = 0    # how much of the kid the record keeps in frame
default hw_kind = 0          # gentleness / defending others under pressure
default hw_cruel = 0         # joining in on the bullying
default hw_guest = 0         # warmth toward the older stranger (the danger)
default hw_outfit = {}       # what the player dressed her in (for closet.txt)
default hw_rating_total = 0  # the score the player gave her (for scores.txt)
default hw_bento = {}        # what the player packed (for lunchbox.txt)
default hw_bento_light = 0   # how many "lighter/skip" picks went in the box
default hw_bento_fav = 0     # how many favorites went in the box
default hw_makeover_guess = 0  # the age the mirror guessed (for mirror.txt)
default hw_pet_result = ""   # "" / "kept" / "hid" -- the pet-game fork
default hw_chat_session = 0  # completed chatrooms; once exhausted, nobody is online
default hw_ambient_ticks = 0 # ordinary clicks/views; the player controls tempo
default hw_pressure_notice_stage = 0
default hw_last_pressure_reason = ""
# Gallery slots the player has opened. Looking is the trigger: the photos you
# actually open are the first to "go public / get noticed," so the player paces
# which parts of her life get exposed, and how fast.
default hw_photos_viewed = []

# UI / session
default hw_start_open = False
default hw_browser_opened_once = False
default hw_snoop_return_folder = "my_computer"
default hw_nav_history = []  # browser Back-button history (page ids)
default _hw_prev_quick_menu = True

# -----------------------------------------------------------------------------
#  DATA + HELPERS
# -----------------------------------------------------------------------------
init python:

    def hw_apply(weights):
        # Apply a dict of axis deltas, e.g. {"grow": 1} or {"kind": 2}.
        for k, v in (weights or {}).items():
            if k == "grow":
                store.hw_grow += v
            elif k == "child":
                store.hw_kept_child += v
            elif k == "kind":
                store.hw_kind += v
            elif k == "cruel":
                store.hw_cruel += v
            elif k == "guest":
                store.hw_guest += v

    # --- Ambient escalation --------------------------------------------------
    # The ending is fixed -- it happened -- but how quickly the record gives up
    # ordinary internet exposure does move: public profile fields, cached forms, copied
    # links, visitor counters, and guestbook activity.
    def hw_add_pressure(reason="look", amount=1):
        store.hw_ambient_ticks = min(99, store.hw_ambient_ticks + amount)
        store.hw_last_pressure_reason = reason

    def hw_seen_game_count():
        return sum([
            1 if store.hinas_world_seen_outfitter else 0,
            1 if store.hinas_world_seen_chatting else 0,
            1 if store.hinas_world_seen_quiz else 0,
            1 if store.hinas_world_seen_rating else 0,
            1 if store.hinas_world_seen_bento else 0,
            1 if store.hinas_world_seen_petsalon else 0,
            1 if store.hinas_world_seen_makeover else 0,
        ])

    def hw_core_games_done():
        # The four site-core games are the ones the story files lean on. The
        # three extra cabinet games (lunchbox / pet salon / makeover) add texture
        # and feed the axes, but missing one shouldn't cost anyone the ending.
        return (
            store.hinas_world_seen_outfitter
            and store.hinas_world_seen_chatting
            and store.hinas_world_seen_quiz
            and store.hinas_world_seen_rating
        )

    def hw_all_beats_hit():
        # "Every necessary beat in the computer environment": the four core games
        # AND every chat room played to the end. Completing the rooms means the
        # beat where Asahiko tells Mom has happened -- the real world is waiting.
        return hw_core_games_done() and store.hw_chat_session >= len(HW2_CHAT_SCRIPTS)

    # GRACE: the site is just a cute, normal kids' page until the player has
    # actually ENGAGED with it. Idle clicking/looking is capped so browsing alone
    # can never make things weird -- only doing the games, the chat rooms, and
    # warming to the guest push past the threshold. Everything "weird" (gallery
    # turning, page-text souring, the surveillance files, guestbook/system lines)
    # is measured RELATIVE to HW_GRACE, so nothing starts until you cross it, then
    # it creeps in gradually instead of slamming on. (Raised from 9 when the game
    # cabinet grew to seven games -- the sweet phase should survive ~3 plays.)
    HW_GRACE = 10

    def hw_engagement():
        # Distinct things the player has actually done: each game once, plus every
        # chat room after the first. (seen_game_count already counts chatting once,
        # so chat rooms beyond #1 are the +1s.) Browsing/looking is NOT engagement.
        return hw_seen_game_count() + max(0, store.hw_chat_session - 1)

    def hw_pressure_score():
        return (
            min(store.hw_ambient_ticks, 6)            # browsing alone caps out here
            + (hw_engagement() * 3)
            + (store.hw_guest * 2)
            + max(0, store.hw_grow - store.hw_kept_child)
        )

    def hw_pressure_over():
        # how far PAST the grace threshold we are (negative = still in grace)
        return hw_pressure_score() - HW_GRACE

    def hw_escalation_stage():
        over = hw_pressure_over()
        if over < 1:
            return 0
        if over >= 12:
            return 4
        if over >= 8:
            return 3
        if over >= 4:
            return 2
        return 1

    def hw_site_corruption():
        # Purely from escalation now, so it's gradual and grace-gated (0 until the
        # player crosses the threshold). hinas_world_corruption is left as legacy.
        return min(3, hw_escalation_stage())

    def hw_visitor_number():
        return "001,{:03d}".format(337 + hw_pressure_score())

    def hw_browser_address(page):
        base = HINAS_WORLD_ADDRESSES.get(page, HINAS_WORLD_ADDRESSES["home"])
        stage = hw_escalation_stage()
        if stage >= 4:
            return base + "?view=profile"
        if stage >= 3:
            return base + "?ref=guestbook"
        if stage >= 2:
            return base + "?public=1"
        return base

    def hw_status_text():
        stage = hw_escalation_stage()
        if stage >= 4:
            return "Done - cached page"
        if stage >= 3:
            return "Done - guestbook updated"
        if stage >= 2:
            return "Done - cookies enabled"
        if stage >= 1:
            return "Done - profile updated"
        return "Done"

    def hw_clock_text():
        # The taskbar clock creeps toward midnight as engagement piles up -- the
        # session simply gets later the deeper you go. Never announced; it's just
        # there for whoever glances at the corner. (School night. She's ten.)
        total = (20 * 60 + 3) + min(hw_pressure_score(), 45) * 6
        hh = (total // 60) % 24
        mm = total % 60
        h12 = hh % 12
        if h12 == 0:
            h12 = 12
        return "{}:{:02d} {}".format(h12, mm, "PM" if hh >= 12 else "AM")

    # --- Browser navigation (Back button is real now) ------------------------
    def hw_nav_to(page):
        if store.hinas_world_page != page:
            store.hw_nav_history.append(store.hinas_world_page)
            store.hw_nav_history = store.hw_nav_history[-12:]
            store.hinas_world_page = page

    def hw_nav_back():
        if store.hw_nav_history:
            store.hinas_world_page = store.hw_nav_history.pop()

    # --- Outfitter -----------------------------------------------------------
    # A genuinely cute dress-up game on its face. Each option is tagged "child"
    # (kid stuff), "grow" (older), or None. Nothing is forbidden -- the player just
    # decides, item by item, how much older to make a little girl look. The voice
    # stays innocent; the unease is in what you choose, not in what it says.
    HW2_OUTFITTER_SLOTS = [
        ("Top",   [("Cartoon Tee", "child"), ("Hoodie", None), ("Crop Top", "grow"), ("Going-Out Top", "grow")]),
        ("Shoes", [("Light-Ups", "child"), ("Sneakers", None), ("Sandals", None), ("Heels", "grow")]),
        ("Extra", [("Backpack", "child"), ("Her Bunny", "child"), ("Phone", "grow"), ("Lip Gloss", "grow")]),
    ]

    def hw_outfit_commit(sel):
        for v in sel.values():
            if not v:
                continue
            if v[1] == "grow":
                store.hw_grow += 1
            elif v[1] == "child":
                store.hw_kept_child += 1
        store.hw_outfit = dict((k, (v[0] if v else None)) for k, v in sel.items())

    def hw2_outfit_caption(sel):
        # Stays a chipper dress-up voice. At most one quietly-off note.
        picks = [v for v in sel.values() if v]
        if not picks:
            return u"Pick out something for Hina to wear today! ☆"
        grow = sum(1 for v in picks if v[1] == "grow")
        child = sum(1 for v in picks if v[1] == "child")
        if grow and child:
            return u"Mix and match! Whatever you think suits her best ♥"
        if grow >= 2:
            return u"So stylish! She'll fit right in with the big kids ♥"
        if child >= 2:
            return u"Cute!! The bunny goes everywhere with her ♥"
        return u"Looking good! Try a few more and see what fits ♥"

    # --- Lunchbox Break -----------------------------------------------------------
    # The food sub-thread, playable. A cheerful lunch-packing game where every
    # slot quietly offers a "lighter" way out. The game's voice never says diet,
    # never says skip -- it just praises whatever you pack, including packing
    # almost nothing. The weight lands later, in lunchbox.txt.
    HW2_BENTO_SLOTS = [
        ("Main",  [("Rolled omelette + rice", "child"), ("Rice ball", None), ("Half a sandwich", "grow"), ("Just rice", "grow")]),
        ("Side",  [("Octopus wieners", "child"), ("Cucumber sticks", None), ("Salad only", "grow"), ("No side", "grow")]),
        ("Sweet", [("Peach jelly", "child"), ("Apple slices", None), ("Sugar-free gum", "grow"), ("No sweets", "grow")]),
        ("Drink", [("Strawberry milk", "child"), ("Barley tea", None), ("Just water", "grow"), ("Zero cola", "grow")]),
    ]

    def hw_bento_commit(sel):
        light = 0
        fav = 0
        for v in sel.values():
            if not v:
                continue
            if v[1] == "grow":
                store.hw_grow += 1
                light += 1
            elif v[1] == "child":
                store.hw_kept_child += 1
                fav += 1
        store.hw_bento = dict((k, (v[0] if v else None)) for k, v in sel.items())
        store.hw_bento_light = light
        store.hw_bento_fav = fav

    def hw2_bento_caption(sel):
        picks = [v for v in sel.values() if v]
        if not picks:
            return u"Pack a super yummy lunch for Hina! ☆"
        light = sum(1 for v in picks if v[1] == "grow")
        fav = sum(1 for v in picks if v[1] == "child")
        if light >= 2:
            return u"So light! Very grown-up of her ♥"
        if fav >= 2:
            return u"All her favorites!! She'll finish every bite ♥"
        return u"A little of everything! She'll like that ♥"

    # --- Pet Salon (Mr Toast & Mochi) -------------------------------------------
    # The one game on the whole site with nothing wrong in it. No guest, no
    # scores, no aging-up -- just brushing a plush bunny and a cat. The knife is
    # the fork: partway through, Emily signs on and can SEE what she's playing.
    # Keeping the window open is the bravest thing on the site.
    HW2_PET_LINES = [
        u"brush brush brush~",
        u"mochi says: prrrrp.",
        u"mr toast approves. (he always approves.)",
        u"mochi is now 20% fluffier.",
        u"mr toast did a flop. incredible.",
        u"mochi caught the ribbon!! champion of the world.",
        u"they're both watching you. happily.",
    ]

    def hw_pet_commit(result):
        store.hw_pet_result = result
        if result == "kept":
            store.hw_kept_child += 2
        else:
            store.hw_grow += 1

    # --- Makeover Mirror --------------------------------------------------------
    # Lacey-makeover shape with the thesis in the reward loop: the mirror guesses
    # her age, and the interface celebrates harder the higher the number goes.
    # Staying little gets a small "aw, cute!" and no stars. Nothing forbids it --
    # the site just makes it feel like losing.
    HW2_MAKEOVER_ROWS = [
        ("Hair",  [("Pigtails", "child"), ("Ponytail", None), ("Straightened", "grow"), ("Like the magazine", "grow")]),
        ("Face",  [("Nothing!", "child"), ("Lip balm", None), ("Lip gloss", "grow"), ("Mascara", "grow")]),
        ("Nails", [("Sticker stars", "child"), ("Clear coat", None), ("Pink polish", "grow"), ("Deep red", "grow")]),
    ]

    def hw_makeover_commit(sel):
        grow = 0
        for v in sel.values():
            if not v:
                continue
            if v[1] == "grow":
                store.hw_grow += 1
                grow += 1
            elif v[1] == "child":
                store.hw_kept_child += 1
        store.hw_makeover_guess = [9, 10, 12, 14][min(grow, 3)]

    # --- Chatting ------------------------------------------------------------
    #   bot line    : (handle, kind, text)   kind in friend/troll/creep/system
    #   player turn : ("you", "you", [(label, weights), ...])
    # Click-driven (see screen hw2_chatting). The tells are kept light: it reads as
    # a normal kids' chat with two edges -- a new kid getting piled on, and an older
    # "guest" who is just a little too friendly. Two of the player turns are real
    # forks: whether to join the bullying, and how far to let Hina go with the guest.
    HW2_CHAT_SCRIPTS = [
        # ---- Week 1, Monday night -- the ordinary version of her world --------
        {
            "room": "~*HINA'S FRIENDS*~",
            "when": "Mon  ||  9:41 PM",
            "users": "StarCute  Emily_x0x  DreamyDoll  PixelHeart  xX_guest_Xx",
            "lines": [
                ("system", "system", u"*** Connected to KidsTown Chat through HinaWeb Chat 2.1 ***"),
                ("system", "system", u"topic: sleepovers, glitter cursors, guestbooks"),
                ("StarCute", "friend", u"HINA!! ur on :D ok important: sleepover saturday, still on??"),
                ("PixelHeart", "friend", u"im bringing the good nail polish this time i promise"),
                ("StarCute", "friend", u"and we are NOT watching the scary one again. u didnt sleep"),
                ("you", "you", [
                    (u"yes!! i'll ask mom but yes", {"child": 1}, [
                        ("StarCute", "friend", u"yayy ask nicely, she likes u best"),
                    ]),
                    (u"maybe, depends on practice", {"grow": 1}, [
                        ("Emily_x0x", "friend", u"u always say that lately"),
                    ]),
                    (u"i'll see", {}, [
                        ("DreamyDoll", "troll", u"thrilling"),
                    ]),
                ]),
                ("StarCute", "friend", u"oh oh did u get the new outfitter stuff? show ur profile pic"),
                ("you", "you", [
                    (u"yeah i kept mr toast in it hehe", {"child": 1}, [
                        ("StarCute", "friend", u"the bunny!! classic. perfect"),
                        ("Emily_x0x", "friend", u"the bunny AGAIN. nobody our age does that hina"),
                    ]),
                    (u"i picked the going-out top :)", {"grow": 1}, [
                        ("Emily_x0x", "friend", u"FINALLY. screenshot it, looks older"),
                        ("StarCute", "friend", u"ok that is kinda cute tho"),
                    ]),
                    (u"havent decided", {}, [
                        ("DreamyDoll", "troll", u"decisive"),
                    ]),
                ]),
                ("Emily_x0x", "friend", u"profile pics matter btw. ppl save everything off here"),
                ("PixelHeart", "friend", u"emily ur stressing her out lol"),
                ("you", "you", [
                    (u"i want it to still feel like me", {"child": 1}, [
                        ("PixelHeart", "friend", u"exactly. let her have one thing"),
                    ]),
                    (u"ok i'll make it look older", {"grow": 1}, [
                        ("Emily_x0x", "friend", u"see? easy. u look 14 like that"),
                    ]),
                    (u"whatever gets the most views", {"grow": 1}, [
                        ("Emily_x0x", "friend", u"now ur getting it"),
                    ]),
                ]),
                ("system", "system", u"kero_kero_99 has entered the room."),
                ("kero_kero_99", "friend", u"wrong room!! sorry!! kero"),
                ("system", "system", u"kero_kero_99 has left the room."),
                ("StarCute", "friend", u"the webring is leaking again"),
                ("system", "system", u"xX_guest_Xx signed your guestbook."),
                ("xX_guest_Xx", "creep", u"cute page :)"),
                ("StarCute", "friend", u"lol who's that. some random off the webring"),
                ("DreamyDoll", "troll", u"hina has FANS now"),
                ("system", "system", u"new_kid has entered the room."),
                ("new_kid", "friend", u"hi. first time here. hina are u on this one"),
                ("new_kid", "friend", u"mom says the downstairs phone line is needed in 20 min"),
                ("DreamyDoll", "troll", u"did ur brother follow ur favorites bar in here LMAO"),
                ("Emily_x0x", "friend", u"wait is that asahiko"),
                ("new_kid", "friend", u"no. im new_kid. stop"),
                ("you", "you", [
                    (u"leave him alone, he didn't do anything", {"kind": 2, "child": 1}, [
                        ("new_kid", "friend", u"thanks. i wont tell mom u were still on"),
                        ("DreamyDoll", "troll", u"hina the bodyguard lol"),
                    ]),
                    (u"......", {}, [
                        ("new_kid", "friend", u"nvm. wrong room"),
                    ]),
                    (u"lol yeah go back to cartoons new_kid", {"cruel": 2, "grow": 1}, [
                        ("DreamyDoll", "troll", u"SHE SAID IT"),
                        ("new_kid", "friend", u"wow. ok."),
                        ("new_kid", "friend", u"sorry. bye"),
                    ]),
                ]),
                ("system", "system", u"new_kid has left the room."),
                ("StarCute", "friend", u"anyway!! saturday. sleepover. pajamas. dont be weird about it"),
                ("you", "you", [
                    (u"i'll be there. pajamas and everything :)", {"child": 1}, [
                        ("StarCute", "friend", u"THATS my hina <3 nite"),
                    ]),
                    (u"if i have time", {"grow": 1}, [
                        ("StarCute", "friend", u"...ok. nite hina"),
                    ]),
                ]),
                ("system", "system", u"StarCute has logged off."),
                ("system", "system", u"Emily_x0x has logged off."),
                ("system", "system", u"DreamyDoll has logged off."),
                ("system", "system", u"Room idle. Phone line released."),
            ],
        },
        # ---- Tuesday after school -- a private window with her best friend -----
        {
            "room": "Private: StarCute",
            "when": "Tue  ||  4:32 PM",
            "users": "StarCute  Hina",
            "lines": [
                ("system", "system", u"*** Private message from StarCute ***"),
                ("StarCute", "friend", u"hihi. this is just us, emily cant see private windows"),
                ("StarCute", "friend", u"are u ok? u seemed kinda off in the room last night"),
                ("you", "you", [
                    (u"yeah! just tired from practice", {"grow": 1}, [
                        ("StarCute", "friend", u"u say tired a lot lately"),
                    ]),
                    (u"i dunno. emily makes me feel babyish", {"child": 1, "kind": 1}, [
                        ("StarCute", "friend", u"emily makes EVERYONE feel babyish. ignore her"),
                    ]),
                    (u"i'm fine. why does everyone keep asking", {"grow": 1}, [
                        ("StarCute", "friend", u"ok ok sorry. i just worry about u"),
                    ]),
                ]),
                ("StarCute", "friend", u"can i say something. dont get mad"),
                ("StarCute", "friend", u"u changed ur about page. it doesnt sound like u anymore"),
                ("StarCute", "friend", u"it used to be mr toast and cartoons. now its all older stuff"),
                ("you", "you", [
                    (u"i just want people to take me serious", {"grow": 1}, [
                        ("StarCute", "friend", u"i take u serious. i've known u since 2nd grade"),
                    ]),
                    (u"i still like cartoons. dont tell emily", {"child": 1}, [
                        ("StarCute", "friend", u"ur secret is safe. the saturday ones are the best ones anyway"),
                    ]),
                    (u"people change, star", {"grow": 1}, [
                        ("StarCute", "friend", u"not this fast. ur kind of scaring me"),
                    ]),
                ]),
                ("StarCute", "friend", u"oh also. some guest signed my guestbook. and pixel's too"),
                ("StarCute", "friend", u"same guy, xX_guest. kinda creepy he hits every page"),
                ("you", "you", [
                    (u"yeah he signed mine. probably nothing", {"child": 1}, [
                        ("StarCute", "friend", u"probably. just dont add him or anything ok"),
                    ]),
                    (u"he actually seems nice tho", {"guest": 1, "grow": 1}, [
                        ("StarCute", "friend", u"hina. u dont know him. be careful pls"),
                    ]),
                    (u"i'll block him if he gets weird", {"child": 1, "kind": 1}, [
                        ("StarCute", "friend", u"good. ok gotta go set the table. love u nerd"),
                    ]),
                ]),
                ("system", "system", u"StarCute has gone offline."),
                ("system", "system", u"*** conversation saved to chat history ***"),
            ],
        },
        # ---- Wednesday, after practice -- the team, the food, the watching -----
        {
            "room": "track-team (school webring)",
            "when": "Wed  ||  6:10 PM",
            "users": "Emily_x0x  StarCute  Coach_Bot  xX_guest_Xx",
            "lines": [
                ("system", "system", u"*** track-team room - school webring ***"),
                ("system", "system", u"Coach_Bot: meet photos are up. great running today, team."),
                ("Emily_x0x", "friend", u"coach put the meet pics on ur gallery. ur famous lol"),
                ("StarCute", "friend", u"ribbon girl!! u looked so fast out there"),
                ("you", "you", [
                    (u"thanks!! i was so tired after", {"child": 1}, [
                        ("StarCute", "friend", u"u always run urself into the ground"),
                    ]),
                    (u"i should've done better", {"grow": 1}, [
                        ("Emily_x0x", "friend", u"u say that every meet. eat something maybe"),
                    ]),
                    (u"did i look ok in them", {}, [
                        ("Emily_x0x", "friend", u"stop refreshing the gallery omg ur fine"),
                    ]),
                ]),
                ("Emily_x0x", "friend", u"btw u skipped the team dinner pic. ppl noticed u werent eating"),
                ("StarCute", "friend", u"emily oh my god leave it"),
                ("you", "you", [
                    (u"i had strawberry milk after", {"child": 1}, [
                        ("StarCute", "friend", u"milk counts. ur fine hina"),
                    ]),
                    (u"wasn't hungry", {"grow": 1}, [
                        ("Emily_x0x", "friend", u"u and 'not hungry'. sure"),
                    ]),
                    (u"can everyone stay out of my food", {"cruel": 1}, [
                        ("Emily_x0x", "friend", u"FINE. forget i said anything"),
                    ]),
                ]),
                ("xX_guest_Xx", "creep", u"saw the meet photos. u look really disciplined. thats rare"),
                ("StarCute", "friend", u"who let the guest into the SCHOOL room"),
                ("you", "you", [
                    (u"nobody. ignore him", {"child": 1, "kind": 1}, [
                        ("xX_guest_Xx", "creep", u"just being nice. ppl work hard and nobody says anything. thats all"),
                    ]),
                    (u"haha thanks :)", {"grow": 1, "guest": 1}, [
                        ("xX_guest_Xx", "creep", u"most kids cant take a compliment. ur different"),
                    ]),
                    (u"how do u even see these", {}, [
                        ("xX_guest_Xx", "creep", u"theyre public :) anyone can. keep them up, theyre good"),
                    ]),
                ]),
                ("system", "system", u"Coach_Bot: reminder - set team photos to friends-only."),
                ("StarCute", "friend", u"^ do that. ok gtg, dinner. text me ok?"),
                ("system", "system", u"Emily_x0x has logged off."),
                ("system", "system", u"StarCute has logged off."),
            ],
        },
        # ---- Thursday, homework hour -- the stranger makes himself useful ------
        # The trust-building beat. He solves a real problem, publicly, and asks
        # for nothing... except one tiny thing that sounds like nothing. This is
        # the room that makes "he's actually nice" a reasonable thing for a kid
        # to think -- which is exactly why it has to exist.
        {
            "room": "#glitter_help (site-help webring)",
            "when": "Thu  ||  5:05 PM",
            "users": "PixelHeart  StarCute  webmistress_yui  xX_guest_Xx  HelpBot",
            "lines": [
                ("system", "system", u"*** #glitter_help - ask ur site questions here ***"),
                ("system", "system", u"HelpBot: please do not paste ur whole page into the chat."),
                ("PixelHeart", "friend", u"hina u had a question right? the marquee thing"),
                ("you", "you", [
                    (u"my welcome text scrolls away and never comes back :(", {}, [
                        ("PixelHeart", "friend", u"mine did that too!! i never fixed it, i just deleted it"),
                    ]),
                    (u"also my sparkle cursor stopped sparkling", {"child": 1}, [
                        ("StarCute", "friend", u"a tragedy. an actual tragedy"),
                    ]),
                    (u"how do i make my page look less babyish", {"grow": 1}, [
                        ("PixelHeart", "friend", u"ur page is fine?? whos saying that"),
                    ]),
                ]),
                ("xX_guest_Xx", "creep", u"the marquee needs the loop thing set. one sec"),
                ("xX_guest_Xx", "creep", u'<marquee loop="-1"> ... like that. -1 means forever'),
                ("PixelHeart", "friend", u"wait that actually worked. ok thanks guest guy"),
                ("webmistress_yui", "friend", u"can someone look at MY guestbook next. its doing the blink thing"),
                ("StarCute", "friend", u"...ok that was helpful. i still think its weird ur in every room"),
                ("xX_guest_Xx", "creep", u"i do this stuff at work all day. its nothing"),
                ("you", "you", [
                    (u"thank u!! my site is fixed!!", {}, [
                        ("xX_guest_Xx", "creep", u"np :) it was a good page already. now it loops too"),
                    ]),
                    (u"u know a lot. how long have u made sites?", {"guest": 1}, [
                        ("xX_guest_Xx", "creep", u"longer than uve been alive probably lol. it goes fast"),
                    ]),
                    (u"why do u hang around kids' site rooms", {"kind": 1}, [
                        ("xX_guest_Xx", "creep", u"everyone starts somewhere. someone helped me once too"),
                    ]),
                ]),
                ("xX_guest_Xx", "creep", u"whats ur timezone btw? so i know when this room is actually awake"),
                ("StarCute", "friend", u"u dont have to answer stuff like that hina"),
                ("you", "you", [
                    (u"star's right. it doesnt matter", {"child": 1, "kind": 1}, [
                        ("xX_guest_Xx", "creep", u"fair enough. smart to be careful online :)"),
                    ]),
                    (u"we're always on after dinner", {"guest": 1}, [
                        ("xX_guest_Xx", "creep", u"after dinner. got it :)"),
                    ]),
                    (u"why?", {}, [
                        ("xX_guest_Xx", "creep", u"no reason. forget i asked. anyway the loop fix should hold"),
                    ]),
                ]),
                ("system", "system", u"PixelHeart has logged off."),
                ("system", "system", u"HelpBot: room going quiet. logs are saved."),
            ],
        },
        {
            "room": "#hinasworld_afterdark",
            "when": "Fri  ||  10:58 PM",
            "users": "StarCute  PixelHeart  xLordVoidx  xX_guest_Xx  Guest_44",
            "lines": [
                ("system", "system", u"*** Joined #hinasworld_afterdark (AIM relay) ***"),
                ("system", "system", u"*** it's been a few days since your last visit ***"),
                ("PixelHeart", "friend", u"hina ur guestbook colors blink now?? did u do that"),
                ("StarCute", "friend", u"and theres a popup. visitor 1337 wins a private album??"),
                ("you", "you", [
                    (u"i didn't make any of that", {"child": 1}, [
                        ("PixelHeart", "friend", u"then change ur password. seriously"),
                    ]),
                    (u"it looks kind of cool tho", {"grow": 1}, [
                        ("StarCute", "friend", u"it looks like an older-kid site. weird for urs"),
                    ]),
                    (u"don't click the popup", {"kind": 1}, [
                        ("PixelHeart", "friend", u"too late but it only opened one window i think"),
                    ]),
                ]),
                ("Guest_44", "creep", u"site owners get special attention. thats normal"),
                ("xLordVoidx", "troll", u"this room is still going? pink overload lol"),
                ("StarCute", "friend", u"nobody invited u void"),
                ("xX_guest_Xx", "creep", u"hina works hard on this page. ppl should appreciate it"),
                ("StarCute", "friend", u"u know her name a LOT for a guest"),
                ("xX_guest_Xx", "creep", u"its on the page. relax"),
                ("system", "system", u"new_kid has entered the room."),
                ("new_kid", "friend", u"the printer made 12 copies of ur homepage. mom saw"),
                ("new_kid", "friend", u"also stop saving stuff to the desktop, my homework folder moved"),
                ("you", "you", [
                    (u"tell mom i'll clean it up", {"child": 1, "kind": 1}, [
                        ("new_kid", "friend", u"ok. i'll put my folder back. dont stay up too late"),
                    ]),
                    (u"asahiko stop embarrassing me online", {"grow": 1}, [
                        ("new_kid", "friend", u"you said my name :/"),
                        ("Guest_44", "troll", u"asahiko lol"),
                    ]),
                    (u"not my problem", {"cruel": 1}, [
                        ("new_kid", "friend", u"fine. i just wanted a turn after"),
                    ]),
                ]),
                ("system", "system", u"new_kid has left the room."),
                ("xX_guest_Xx", "creep", u"siblings never get the website thing. ur brother means well tho"),
                ("xX_guest_Xx", "creep", u"btw ur gallery loads slow bc the pics are huge. i could resize them for u. 5 minute job"),
                ("you", "you", [
                    (u"i'm ok, thanks", {"child": 1, "kind": 1}, [
                        ("xX_guest_Xx", "creep", u"no problem. offer stands. ur smart to be careful :)"),
                        ("system", "system", u"xX_guest_Xx is idle."),
                    ]),
                    (u"maybe sometime", {"guest": 1}, [
                        ("xX_guest_Xx", "creep", u"cool. u have msn? easier to send files there than paste them here"),
                        ("xX_guest_Xx", "creep", u"ur easy to talk to, u know that?"),
                    ]),
                    (u"how do u know all this stuff", {}, [
                        ("xX_guest_Xx", "creep", u"work stuff. u pick things up. anyway the offer's free"),
                    ]),
                ]),
                ("system", "system", u"StarCute has logged off."),
                ("system", "system", u"PixelHeart has logged off."),
                ("system", "system", u"#hinasworld_afterdark has no active moderators."),
            ],
        },
        # ---- Sunday morning -- her brother, on the family computer, worried ----
        {
            "room": "Private: asahiko",
            "when": "Sun  ||  8:15 AM",
            "users": "asahiko  Hina",
            "lines": [
                ("system", "system", u"*** asahiko started a private chat ***"),
                ("asahiko", "friend", u"i know its early. ur still asleep probably"),
                ("asahiko", "friend", u"i was getting my turn on the computer and i saw something"),
                ("asahiko", "friend", u"that guest guy is in ur guestbook AND ur chat history. a lot"),
                ("asahiko", "friend", u"he knows ur school from the track pics. i checked. its public"),
                ("you", "you", [
                    (u"asahiko did you go through my stuff?!", {"grow": 1}, [
                        ("asahiko", "friend", u"its the FAMILY computer hina. it was just open"),
                    ]),
                    (u"...what else did you see", {"child": 1}, [
                        ("asahiko", "friend", u"enough. ur about page. the older photos. him"),
                    ]),
                    (u"its none of your business", {"cruel": 1}, [
                        ("asahiko", "friend", u"ok but it kind of is. i live here too"),
                    ]),
                ]),
                ("asahiko", "friend", u"i'm not trying to be the annoying brother right now"),
                ("asahiko", "friend", u"my friend at school, his cousin had a guy like this once"),
                ("asahiko", "friend", u"do u want me to NOT tell mom? i'll stay quiet if u fix it"),
                ("you", "you", [
                    (u"please dont tell mom. i'll handle it", {"guest": 1, "grow": 1}, [
                        ("asahiko", "friend", u"...thats the part that scares me. why dont u want her to know"),
                    ]),
                    (u"ok. tell mom. i think i need help", {"child": 2, "kind": 1}, [
                        ("asahiko", "friend", u"ok. i will. ur not in trouble with me, just so u know"),
                    ]),
                    (u"there's nothing to fix. drop it", {"grow": 1}, [
                        ("asahiko", "friend", u"hina ur not even awake and ur already lying. i can tell"),
                    ]),
                ]),
                ("asahiko", "friend", u"i left u the whole peach jelly btw. not half. the whole one"),
                ("asahiko", "friend", u"get up soon, mom's making egg rice"),
                ("system", "system", u"asahiko is away: breakfast."),
            ],
        },
        # ---- The next week -- the people who love her try to pull her back ----
        {
            "room": "#help_my_page",
            "when": "next Thu  ||  7:20 PM",
            "users": "PixelHeart  new_kid2  StarCute",
            "lines": [
                ("system", "system", u"*** site-help room ***"),
                ("PixelHeart", "friend", u"hina ok we need to talk about the guest thing for real"),
                ("PixelHeart", "friend", u"he's in ur guestbook on basically every photo now"),
                ("PixelHeart", "friend", u"my cousin had a guy EXACTLY like this. it got bad. block him"),
                ("StarCute", "friend", u"i'm here too. we're not ganging up on u. we're worried"),
                ("you", "you", [
                    (u"ok. you're right. i'm blocking him", {"child": 2, "kind": 1}, [
                        ("PixelHeart", "friend", u"THANK U. and tell ur mom too. for real"),
                        ("StarCute", "friend", u"proud of u ok?"),
                    ]),
                    (u"he's honestly nicer than emily is", {"guest": 1, "grow": 1}, [
                        ("PixelHeart", "friend", u"hina thats what they DO. they're nice first"),
                        ("StarCute", "friend", u"please listen to her"),
                    ]),
                    (u"it's my page. i'll handle it myself", {"grow": 1}, [
                        ("PixelHeart", "friend", u"ok but handle it. not later. tonight"),
                    ]),
                ]),
                ("system", "system", u"new_kid2 has entered the room."),
                ("new_kid2", "friend", u"its me. asahiko. i made a new name so u'd actually answer"),
                ("StarCute", "friend", u"u literally have the same username just with a 2 at the end lol"),
                ("new_kid2", "friend", u"i told mom a guest keeps typing ur name. she got real quiet"),
                ("you", "you", [
                    (u"asahiko you PROMISED", {"guest": 1, "grow": 1}, [
                        ("new_kid2", "friend", u"i promised IF u fixed it. u didnt. so."),
                    ]),
                    (u"...good. thanks for telling her", {"child": 2, "kind": 1}, [
                        ("new_kid2", "friend", u"ok. i'm not just the annoying one then"),
                    ]),
                    (u"it's nothing. it's fine", {}, [
                        ("new_kid2", "friend", u"you always say that. its not"),
                    ]),
                ]),
                ("StarCute", "friend", u"we love u. dont disappear into that page ok"),
                ("system", "system", u"PixelHeart has logged off."),
                ("system", "system", u"StarCute has logged off."),
                ("system", "system", u"new_kid2 has logged off."),
            ],
        },
        # ---- Friday, very late, two weeks deep -- alone with him --------------
        {
            "room": "MSN: Hina's World Live Chat",
            "when": "Fri  ||  11:34 PM",
            "users": "xX_guest_Xx  PixelHeart  Away:StarCute",
            "lines": [
                ("system", "system", u"*** Reconnected. Last message may have been sent twice. ***"),
                ("PixelHeart", "friend", u"hina? its almost midnight. ur profile is public-public now"),
                ("PixelHeart", "friend", u"like the whole web. not just friends. please fix it"),
                ("xX_guest_Xx", "creep", u"public pages are how people find each other. its fine"),
                ("xX_guest_Xx", "creep", u"i found u because ur special. not random. u know that by now"),
                ("you", "you", [
                    (u"i'm making it private right now", {"child": 2, "kind": 1}, [
                        ("PixelHeart", "friend", u"good. i'll help u tomorrow. go to bed"),
                        ("xX_guest_Xx", "creep", u"thats a little dramatic dont u think"),
                    ]),
                    (u"maybe public is okay", {"guest": 1, "grow": 1}, [
                        ("xX_guest_Xx", "creep", u"exactly. u get it. they dont"),
                    ]),
                    (u"i just want people to like it", {"grow": 1}, [
                        ("PixelHeart", "friend", u"people can like it without knowing where u live, hina"),
                    ]),
                ]),
                ("system", "system", u"PixelHeart has logged off."),
                ("system", "system", u"StarCute is away: asleep."),
                ("xX_guest_Xx", "creep", u"finally. just us. easier to talk when theyre not hovering"),
                ("xX_guest_Xx", "creep", u"i know im older. thats exactly why im honest with u. nobody else on here is"),
                ("xX_guest_Xx", "creep", u"send me the outfit pic before u change the privacy? just for me"),
                ("you", "you", [
                    (u"no. i'm blocking you. goodbye", {"child": 2, "kind": 1}, [
                        ("system", "system", u"xX_guest_Xx has been blocked."),
                        ("system", "system", u"You are the only one left in the room."),
                    ]),
                    (u"i don't think i should", {"child": 1}, [
                        ("xX_guest_Xx", "creep", u"then dont call it sending. call it trusting me"),
                    ]),
                    (u"ok. just one. dont tell anyone", {"guest": 2, "grow": 1}, [
                        ("xX_guest_Xx", "creep", u"good girl. see? ur older than they all think"),
                    ]),
                ]),
                ("system", "system", u"Connection lost."),
            ],
        },
    ]

    def hw2_chat_script(session=None):
        if session is None:
            session = store.hw_chat_session
        if 0 <= session < len(HW2_CHAT_SCRIPTS):
            return HW2_CHAT_SCRIPTS[session]["lines"]
        return []

    def hw2_chat_room(session=None):
        if session is None:
            session = store.hw_chat_session
        if 0 <= session < len(HW2_CHAT_SCRIPTS):
            return HW2_CHAT_SCRIPTS[session]["room"]
        return "~*HINA'S FRIENDS*~"

    def hw2_chat_users(session=None):
        if session is None:
            session = store.hw_chat_session
        if 0 <= session < len(HW2_CHAT_SCRIPTS):
            return HW2_CHAT_SCRIPTS[session]["users"]
        return ""

    def hw2_chat_when(session=None):
        # the date/time stamp on a room -- the whole thing spans days into weeks
        if session is None:
            session = store.hw_chat_session
        if 0 <= session < len(HW2_CHAT_SCRIPTS):
            return HW2_CHAT_SCRIPTS[session].get("when", "")
        return ""

    def hw2_chat_choice_parts(opt):
        label = opt[0]
        weights = opt[1] if len(opt) > 1 else {}
        branch = opt[2] if len(opt) > 2 else []
        return label, weights, branch

    def hw_chat_exhausted():
        return store.hw_chat_session >= len(HW2_CHAT_SCRIPTS)

    def hw_chat_card_blurb():
        left = max(0, len(HW2_CHAT_SCRIPTS) - store.hw_chat_session)
        if left <= 0:
            return u"Nobody else is online."
        if left == len(HW2_CHAT_SCRIPTS):
            return u"Chat with cute friends from all over the web."
        if left == 1:
            return u"One room is still awake."
        return u"{} rooms are still awake.".format(left)

    def hw2_chat_lines(session, step, choices, branches):
        script = hw2_chat_script(session)
        out = []
        n = len(script)
        for i in range(min(step, n)):
            who, kind, payload = script[i]
            if who == "you":
                out.append(("HINA", "you", choices.get(i, u"...")))
                out.extend(branches.get(i, []))
            else:
                out.append((who, kind, payload))
        if step < n:
            who, kind, payload = script[step]
            if who != "you":
                out.append((who, kind, payload))
        # Full history -- the transcript screen scrolls now, so nothing is lost.
        return out

    # --- Quiz ----------------------------------------------------------------
    #   (question, [(answer, tag), ...])     tag: grow / child / None / "guest"
    # A normal magazine-style quiz. It never says "grow up"; the answers just lean
    # older, and the player picks how far. Question 3 quietly feeds the guest thread.
    HW2_QUIZ = [
        (u"What's your perfect Saturday?",
            [(u"cartoons in pjs!", "child"), (u"the park", None), (u"the mall with friends", "grow"), (u"an older kid's party", "grow")]),
        (u"Pick a look:",
            [(u"matching pjs", "child"), (u"jeans + tee", None), (u"something cute", "grow"), (u"something they'll notice", "grow")]),
        (u"Someone older says you're mature. You feel...",
            [(u"weird. i'd tell someone", "child"), (u"nothing really", None), (u"kind of flattered", "guest"), (u"finally seen :)", "guest")]),
        (u"After school you usually...",
            [(u"snack + play", "child"), (u"homework", None), (u"talk online for hours", "grow"), (u"skip dinner to stay on", "grow")]),
        (u"Be honest -- you wish you were...",
            [(u"the same! i like being me", "child"), (u"a little taller", None), (u"older", "grow"), (u"older. way older.", "grow")]),
    ]

    def hw_quiz_commit(ans):
        for tag in ans.values():
            if tag == "grow":
                store.hw_grow += 1
            elif tag == "child":
                store.hw_kept_child += 1
            elif tag == "guest":
                store.hw_grow += 1
                store.hw_guest += 1

    # --- Rating --------------------------------------------------------------
    # Cute on its face: "rate Hina's new look out of 5." No clinical reveal -- the
    # discomfort is just realising you're scoring a little girl, and that she reads
    # the number and tries to match it. The weight is carried by scores.txt later.
    HW2_RATING_ROWS = [u"Outfit", u"Hair", u"Smile", u"Cool factor", u"Overall"]

    def hw_rating_commit(scores):
        total = sum(scores.values())   # 5 rows x 1..5  ->  5..25
        store.hw_rating_total = total
        if total >= 18:
            store.hw_grow += 2
        elif total >= 12:
            store.hw_grow += 1

    # --- Ending --------------------------------------------------------------
    # Rebalanced around NET push (grow - child) when the cabinet grew to seven
    # games: absolute grow totals inflate with more content, but the question was
    # always "how much older did you make her than you let her stay".
    def hw_ending_tone():
        cruel = store.hw_cruel
        grow = store.hw_grow
        kind = store.hw_kind
        child = store.hw_kept_child
        net = grow - child
        if cruel >= 2 or net >= 6:
            return "harsh"
        if net >= 2:
            return "pushed"
        if kind >= 2 or child >= max(grow, 1):
            return "tender"
        return "hollow"

    # --- Desktop files -------------------------------------------------------
    # The record the player can read mid-session WITHOUT logging off. Each file
    # is generated from current state, so it reflects exactly how much of the
    # nine-year-old's year has been surfaced so far. The ending is the same
    # melancholy regardless; these are how you find out what it already cost
    # her. Built with "\n".join (clean indentation for the lexer).

    def hw_files_present():
        # filenames currently sitting on the desktop, given progress + choices
        out = ["diary.txt"]
        if store.hinas_world_seen_outfitter:
            out.append("closet.txt")
        if store.hinas_world_seen_chatting:
            out.append("chat.txt")
        if store.hinas_world_seen_quiz:
            out.append("quiz.txt")
        if store.hinas_world_seen_rating:
            out.append("scores.txt")
        if store.hinas_world_seen_bento:
            out.append("lunchbox.txt")
        if store.hinas_world_seen_petsalon:
            out.append("mochi_and_toast.txt")
        if store.hinas_world_seen_makeover:
            out.append("mirror.txt")
        if store.hw_guest >= 2:   # the sharp edge: only once the record shows it
            out.append("(1) new message.txt")
        stage = hw_escalation_stage()
        if stage >= 1:
            out.append("visitor_log.txt")
        if stage >= 2:
            out.append("profile_cache.txt")
        if stage >= 3:
            out.append("autocomplete.txt")
        if stage >= 4:
            out.append("recent_status.txt")
        return out

    def hw_desktop_icons():
        icons = [
            ("browser", "hinasworld.exe", "app", "H", False),
            ("snoop:my_computer", "My Computer", "pc", "PC", False),
            ("snoop:internet_history", "Internet Explorer", "app", "e", False),
            ("snoop:msn", "MSN Messenger", "msn", "msn", False),
            ("snoop:family_photos", "Family Photos", "folder", "img", False),
            ("snoop:mom_recipes", "Mom Recipes", "folder", "doc", False),
            ("snoop:asahiko_stuff", "Asahiko Stuff", "folder", "asa", False),
            ("snoop:recycle_bin", "Recycle Bin", "bin", "bin", False),
        ]
        for fname in hw_files_present():
            is_msg = fname.startswith("(1)")
            icons.append((
                "file:" + fname,
                fname,
                "doc",
                "@" if is_msg else "txt",
                is_msg,
            ))
        return icons

    HW2_SNOOP_FOLDERS = {
        "my_computer": {
            "title": "My Computer",
            "address": "C:\\",
            "note": "Shared family computer. Everyone saves things in the wrong place.",
            "entries": [
                ("folder", "my_documents", "Shared Documents", "doc", "homework, lists, and things nobody renamed"),
                ("folder", "family_photos", "Family Photos", "img", "camera imports and old albums"),
                ("folder", "mom_recipes", "Mom Recipes", "doc", "recipes, notes, grocery lists"),
                ("folder", "asahiko_stuff", "Asahiko Stuff", "asa", "games, homework, do-not-read files"),
                ("folder", "internet_history", "Internet Explorer", "e", "favorites and history"),
                ("folder", "recycle_bin", "Recycle Bin", "bin", "deleted items"),
            ],
        },
        "my_documents": {
            "title": "Shared Documents",
            "address": "C:\\Documents and Settings\\All Users\\Documents",
            "note": "Shared files from every user account.",
            "entries": [
                ("doc", "family_schedule", "family_schedule.txt", "txt", "computer turns, dinner, practice"),
                ("doc", "printer_note", "printer_note.txt", "txt", "left beside the printer"),
                ("doc", "mom_email_draft", "email_draft.txt", "txt", "unsent"),
                ("doc", "hina_school_list", "hina_school_list.txt", "txt", "things to remember"),
                ("doc", "field_trip_form", "field_trip_form.txt", "txt", "maybe already turned in"),
                ("doc", "dentist_reminder", "dentist_reminder.txt", "txt", "old appointment card"),
                ("doc", "summer_chore_chart", "summer_chore_chart_OLD.txt", "txt", "still being argued over"),
                ("doc", "dad_call_times", "dad_call_times.txt", "txt", "written twice"),
                ("doc", "quiet_house_rules", "quiet_house_rules.txt", "txt", "kid logic"),
                ("doc", "two_house_map", "two_house_map.txt", "txt", "not a real map"),
                ("doc", "computer_rules", "COMPUTER_RULES.txt", "txt", "ignored by both children"),
                ("doc", "phone_log", "phone_line_log.txt", "txt", "who got yelled at"),
                ("doc", "snack_treaty", "snack_treaty.txt", "txt", "unsigned but enforced"),
                ("folder", "hina_site", "HinaSite", "H", "website files and half-finished pages"),
                ("folder", "family_photos", "Family Photos", "img", "camera imports and old albums"),
                ("folder", "asahiko_stuff", "Asahiko Stuff", "asa", "he keeps moving it back"),
            ],
        },
        "family_photos": {
            "title": "Family Photos",
            "address": "C:\\Documents and Settings\\All Users\\Documents\\My Pictures",
            "note": "Shared pictures. Web copies found in HinaSite/gallery.",
            "entries": [
                ("image", "Pancake Morning", "pancake_morning.jpg", "img", "breakfast table"),
                ("image", "Strawberry Milk", "strawberry_milk.jpg", "img", "after practice"),
                ("image", "Lunch Box", "lunch_box.jpg", "img", "lunch before school"),
                ("image", "Curry Night", "curry_night.jpg", "img", "kitchen light"),
                ("image", "Festival Noodles", "festival_noodles.jpg", "img", "summer stall"),
                ("image", "Pudding Cup", "pudding_cup.jpg", "img", "fridge prize"),
                ("image", "Dad's Chair", "dads_chair.jpg", "img", "living room"),
                ("image", "Train Platform", "train_platform.jpg", "img", "weekend morning"),
                ("image", "Two Cakes", "two_cakes.jpg", "img", "birthday table"),
                ("doc", "camera_import", "camera_import_log.txt", "txt", "last import"),
                ("doc", "album_note", "album_note.txt", "txt", "mom's reminder"),
            ],
        },
        "hina_site": {
            "title": "HinaSite",
            "address": "C:\\Documents and Settings\\All Users\\Documents\\HinaSite",
            "note": "Local copy of hinasworld.net. Last publish: unknown.",
            "entries": [
                ("doc", "site_readme", "README_FIRST.txt", "txt", "how to upload"),
                ("doc", "index_html", "index_home.html", "txt", "homepage source"),
                ("doc", "guestbook_export", "guestbook_export.txt", "txt", "copied comments"),
                ("doc", "gallery_manifest", "gallery_manifest.txt", "txt", "public/private flags"),
                ("doc", "layout_todo", "layout_todo.txt", "txt", "glitter cursor crisis"),
                ("doc", "password_hint", "password_hint.txt", "txt", "terrible idea"),
                ("doc", "old_updates", "updates_OLD.html", "txt", "not linked anymore"),
                ("doc", "color_tests", "colors_maybe.txt", "txt", "too many pinks"),
                ("doc", "counter_backup", "visitor_counter_BACKUP.txt", "txt", "numbers nobody trusts"),
                ("doc", "princess_house", "princess_house_story.txt", "txt", "Hina draft"),
                ("doc", "calm_page", "calm_page.html", "txt", "hidden page test"),
                ("doc", "dad_link_note", "dad_link_note.txt", "txt", "do not publish"),
            ],
        },
        "mom_recipes": {
            "title": "Mom Recipes",
            "address": "C:\\Documents and Settings\\Mom\\My Documents\\Recipes",
            "note": "Typed quickly, printed often, stained by the keyboard.",
            "entries": [
                ("doc", "star_pancakes", "star_pancakes.txt", "txt", "Asahina's favorite shape"),
                ("doc", "after_practice_snack", "after_practice_snack.txt", "txt", "for track days"),
                ("doc", "curry_leftovers", "curry_leftovers.txt", "txt", "make extra potatoes"),
                ("doc", "grocery_list", "grocery_list.txt", "txt", "fridge magnets copied here"),
                ("doc", "lunch_rotation", "lunch_rotation.txt", "txt", "school mornings"),
                ("doc", "emergency_dinner", "emergency_dinner.txt", "txt", "when practice runs late"),
                ("doc", "noodles_if_sick", "noodles_if_sick.txt", "txt", "ginger if tolerated"),
                ("doc", "nikujaga_notes", "nikujaga_notes.txt", "txt", "weeknight batch"),
                ("doc", "freezer_inventory", "freezer_inventory_OLD.txt", "txt", "probably inaccurate"),
                ("doc", "pancake_test", "pancake_test.txt", "txt", "never tested twice"),
            ],
        },
        "asahiko_stuff": {
            "title": "Asahiko Stuff",
            "address": "C:\\Documents and Settings\\Asahiko\\Desktop\\Asahiko Stuff",
            "note": "Folder label: DO NOT SNOOP. Last opened by: Hina.",
            "entries": [
                ("doc", "asahiko_homework", "homework_about_family.txt", "txt", "not finished"),
                ("doc", "do_not_read", "DO_NOT_READ_HINA.txt", "txt", "obviously read"),
                ("doc", "cat_names", "cat_names.txt", "txt", "mochi alternatives"),
                ("doc", "game_cheats", "platformer_cheats.txt", "txt", "typed from a magazine"),
                ("doc", "asahiko_chat_warning", "weird_chat_people.txt", "txt", "not a lecture"),
                ("doc", "turn_manifesto", "computer_turn_manifesto.txt", "txt", "very serious"),
                ("doc", "snack_debt", "snack_debt.txt", "txt", "itemized damages"),
                ("doc", "trade_offer", "trade_offer.txt", "txt", "rejected proposal"),
                ("doc", "old_save_files", "save_files_do_not_delete.txt", "txt", "maybe broken"),
                ("doc", "secret_questions", "secret_questions.txt", "txt", "bad security audit"),
                ("doc", "dad_question_list", "questions_for_dad.txt", "txt", "crossed out"),
                ("doc", "stair_rules", "stair_rules.txt", "txt", "when voices are loud"),
            ],
        },
        "internet_history": {
            "title": "Internet Explorer",
            "address": "C:\\Documents and Settings\\All Users\\Documents\\Browser Logs",
            "note": "Exported browser logs. AutoComplete enabled.",
            "entries": [
                ("doc", "browser_history", "history.txt", "txt", "last seven days"),
                ("doc", "browser_history_asahiko", "history_asahiko.txt", "txt", "also last seven days"),
                ("doc", "favorites", "favorites.txt", "txt", "saved links"),
                ("doc", "search_terms", "search_terms.tmp", "txt", "autocomplete"),
                ("doc", "download_log", "download_log.txt", "txt", "mostly cursors"),
                ("doc", "cookies", "cookies.txt", "txt", "tiny crumbs"),
                ("doc", "print_queue", "print_queue_old.txt", "txt", "stuck jobs"),
                ("doc", "toolbar_note", "toolbar_note.txt", "txt", "where did that button come from"),
                ("doc", "map_searches", "map_searches.txt", "txt", "directions"),
                ("doc", "saved_mail_headers", "mail_headers.txt", "txt", "subjects only"),
                ("folder", "msn", "MSN Messenger", "msn", "contacts and saved status"),
            ],
        },
        "msn": {
            "title": "MSN Messenger",
            "address": "C:\\Program Files\\MSN Messenger",
            "note": "Remember my password is checked.",
            "entries": [
                ("doc", "msn_contacts", "contacts.cache", "txt", "screen names"),
                ("doc", "away_messages", "away_messages.txt", "txt", "saved status lines"),
                ("doc", "blocked_users", "blocked_users.txt", "txt", "mostly empty"),
                ("doc", "nudge_log", "nudge_log.txt", "txt", "too many nudges"),
                ("doc", "display_names", "display_names.txt", "txt", "terrible ideas"),
            ],
        },
        "recycle_bin": {
            "title": "Recycle Bin",
            "address": "Recycle Bin",
            "note": "Deleted does not mean gone.",
            "entries": [
                ("doc", "deleted_guestbook", "deleted_guestbook_comment.tmp", "txt", "recovered fragment"),
                ("doc", "old_profile", "old_profile_about.txt", "txt", "older version"),
                ("doc", "bad_shortcut", "private_album.lnk", "txt", "broken shortcut"),
                ("doc", "deleted_rules", "COMPUTER_RULES_old.txt", "txt", "somehow worse"),
                ("doc", "deleted_recipe", "omurice_final_FINAL.txt", "txt", "not final"),
                ("doc", "deleted_grocery", "grocery_list_lastweek.txt", "txt", "already shopped"),
                ("doc", "desktop_cleanup", "desktop_cleanup_wizard.log", "txt", "recommendations ignored"),
                ("doc", "old_lunch_note", "lunch_note_unsent.txt", "txt", "not packed"),
                ("doc", "deleted_family_note", "for_dad_unsent.txt", "txt", "not sent"),
                ("doc", "deleted_story", "normal_house_story_OLD.txt", "txt", "too obvious"),
            ],
        },
    }

    def hw_snoop_folder(folder_id):
        return HW2_SNOOP_FOLDERS.get(folder_id, HW2_SNOOP_FOLDERS["my_computer"])

    def hw_snoop_parent(folder_id):
        parents = {
            "my_computer": None,
            "my_documents": "my_computer",
            "family_photos": "my_documents",
            "hina_site": "my_documents",
            "mom_recipes": "my_computer",
            "asahiko_stuff": "my_computer",
            "internet_history": "my_computer",
            "msn": "internet_history",
            "recycle_bin": "my_computer",
        }
        return parents.get(folder_id, "my_computer")

    def hw_snoop_doc_title(doc_id):
        titles = {
            "family_schedule": "family_schedule.txt",
            "printer_note": "printer_note.txt",
            "mom_email_draft": "email_draft.txt",
            "hina_school_list": "hina_school_list.txt",
            "field_trip_form": "field_trip_form.txt",
            "dentist_reminder": "dentist_reminder.txt",
            "summer_chore_chart": "summer_chore_chart_OLD.txt",
            "dad_call_times": "dad_call_times.txt",
            "quiet_house_rules": "quiet_house_rules.txt",
            "two_house_map": "two_house_map.txt",
            "computer_rules": "COMPUTER_RULES.txt",
            "phone_log": "phone_line_log.txt",
            "snack_treaty": "snack_treaty.txt",
            "camera_import": "camera_import_log.txt",
            "album_note": "album_note.txt",
            "site_readme": "README_FIRST.txt",
            "index_html": "index_home.html",
            "guestbook_export": "guestbook_export.txt",
            "gallery_manifest": "gallery_manifest.txt",
            "layout_todo": "layout_todo.txt",
            "password_hint": "password_hint.txt",
            "old_updates": "updates_OLD.html",
            "color_tests": "colors_maybe.txt",
            "counter_backup": "visitor_counter_BACKUP.txt",
            "princess_house": "princess_house_story.txt",
            "calm_page": "calm_page.html",
            "dad_link_note": "dad_link_note.txt",
            "star_pancakes": "star_pancakes.txt",
            "after_practice_snack": "after_practice_snack.txt",
            "curry_leftovers": "curry_leftovers.txt",
            "grocery_list": "grocery_list.txt",
            "lunch_rotation": "lunch_rotation.txt",
            "emergency_dinner": "emergency_dinner.txt",
            "noodles_if_sick": "noodles_if_sick.txt",
            "nikujaga_notes": "nikujaga_notes.txt",
            "freezer_inventory": "freezer_inventory_OLD.txt",
            "pancake_test": "pancake_test.txt",
            "asahiko_homework": "homework_about_family.txt",
            "do_not_read": "DO_NOT_READ_HINA.txt",
            "cat_names": "cat_names.txt",
            "game_cheats": "platformer_cheats.txt",
            "asahiko_chat_warning": "weird_chat_people.txt",
            "turn_manifesto": "computer_turn_manifesto.txt",
            "snack_debt": "snack_debt.txt",
            "trade_offer": "trade_offer.txt",
            "old_save_files": "save_files_do_not_delete.txt",
            "secret_questions": "secret_questions.txt",
            "dad_question_list": "questions_for_dad.txt",
            "stair_rules": "stair_rules.txt",
            "browser_history": "history.txt",
            "browser_history_asahiko": "history_asahiko.txt",
            "favorites": "favorites.txt",
            "search_terms": "search_terms.tmp",
            "download_log": "download_log.txt",
            "cookies": "cookies.txt",
            "print_queue": "print_queue_old.txt",
            "toolbar_note": "toolbar_note.txt",
            "map_searches": "map_searches.txt",
            "saved_mail_headers": "mail_headers.txt",
            "msn_contacts": "contacts.cache",
            "away_messages": "away_messages.txt",
            "blocked_users": "blocked_users.txt",
            "nudge_log": "nudge_log.txt",
            "display_names": "display_names.txt",
            "deleted_guestbook": "deleted_guestbook_comment.tmp",
            "old_profile": "old_profile_about.txt",
            "bad_shortcut": "private_album.lnk",
            "deleted_rules": "COMPUTER_RULES_old.txt",
            "deleted_recipe": "omurice_final_FINAL.txt",
            "deleted_grocery": "grocery_list_lastweek.txt",
            "desktop_cleanup": "desktop_cleanup_wizard.log",
            "old_lunch_note": "lunch_note_unsent.txt",
            "deleted_family_note": "for_dad_unsent.txt",
            "deleted_story": "normal_house_story_OLD.txt",
            "help_support": "Help and Support.txt",
        }
        return titles.get(doc_id, doc_id + ".txt")

    def hw_snoop_doc_body(doc_id):
        if doc_id == "family_schedule":
            L = [
                "family_schedule.txt",
                "------------------------------",
                "",
                "MON  Asahina practice / Asahiko math worksheet",
                "TUE  mom late shift / leftovers",
                "WED  computer turns:",
                "       6:00 - Asahiko homework",
                "       6:30 - Asahina website",
                "       7:15 - mom email",
                "FRI  Dad calls after dinner if he remembers",
                "SAT  ask before making plans. ask MOM first.",
                "",
                "DO NOT stay on after the phone rings.",
            ]
        elif doc_id == "printer_note":
            L = [
                "printer_note.txt",
                "------------------------------",
                "",
                "Asahina,",
                "",
                "Please stop printing the pink web page.",
                "The ink is not free.",
                "",
                "Asahiko,",
                "",
                "Please stop printing cheat codes.",
                "Also not free.",
            ]
        elif doc_id == "mom_email_draft":
            L = [
                "email_draft.txt",
                "------------------------------",
                "",
                "To: mrs_kawase@school.ne.jp",
                "Subject: Asahina",
                "",
                "Sorry to bother you. Has Asahina seemed different",
                "after practice? She says she's fine, but she is",
                "spending a lot more time on the computer lately.",
                "",
                "I may be worrying over nothing.",
                "",
                "[unsent]",
            ]
        elif doc_id == "hina_school_list":
            L = [
                "hina_school_list.txt",
                "------------------------------",
                "",
                "- track uniform",
                "- math workbook",
                "- lunch box",
                "- give Asahiko back his eraser",
                "- do not let Emily see old backpack keychain",
                "- smile normal in profile picture",
            ]
        elif doc_id == "field_trip_form":
            L = [
                "field_trip_form.txt",
                "------------------------------",
                "",
                "FIELD TRIP - AQUARIUM / CLASS 5B",
                "",
                "Bring:",
                "- top up the tram card",
                "- raincoat if forecast changes",
                "- lunch that does not leak in backpack",
                "",
                "Mom note: Did I sign this already?",
                "Asahina note: yes probably",
                "Asahiko note: 'probably' is not a signature",
            ]
        elif doc_id == "dentist_reminder":
            L = [
                "dentist_reminder.txt",
                "------------------------------",
                "",
                "Asahina cleaning - rescheduled from April",
                "Asahiko sealant check - ask about back molar",
                "",
                "card was under keyboard.",
                "date may be old.",
                "",
                "Do not use this file as proof you brushed.",
            ]
        elif doc_id == "summer_chore_chart":
            L = [
                "summer_chore_chart_OLD.txt",
                "------------------------------",
                "",
                "MON  take cans out",
                "TUE  water porch plants",
                "WED  fold towels",
                "THU  feed Mochi before arguing about computer",
                "FRI  clear plates without being asked twice",
                "",
                "OLD does not mean nobody has to do it.",
                "It means Mom got tired of printing new charts.",
            ]
        elif doc_id == "dad_call_times":
            L = [
                "dad_call_times.txt",
                "------------------------------",
                "",
                "Dad call times",
                "",
                "FRI  after dinner",
                "SUN  before bath if he is not driving",
                "",
                "Mom version:",
                "Do not wait by the phone. If he calls, he calls.",
                "",
                "Hina version:",
                "wait by phone but pretend not to",
                "",
                "Asahiko version:",
                "do not let Hina answer if Mom and Dad are doing the quiet voice.",
            ]
        elif doc_id == "quiet_house_rules":
            L = [
                "quiet_house_rules.txt",
                "------------------------------",
                "",
                "RULES FOR WHEN GROWN-UPS TALK IN THE KITCHEN",
                "",
                "1. TV volume 12 or lower.",
                "2. Do not ask if Dad is staying for dinner.",
                "3. If Mom says 'not now,' it means actually not now.",
                "4. If Dad says 'ask your mother,' ask later.",
                "5. If nobody is yelling, do not make them remember yelling.",
                "",
                "Hina added: make website louder in headphones.",
                "Asahiko added: headphones do not fix doors.",
            ]
        elif doc_id == "two_house_map":
            L = [
                "two_house_map.txt",
                "------------------------------",
                "",
                "NOT A REAL MAP",
                "",
                "home home:",
                "  mom room / our room / computer / mochi / rice cooker",
                "",
                "dad maybe home:",
                "  train / stairs / blue vending machine / shoes by door",
                "",
                "rules:",
                "- if you forget toothbrush, Dad has a spare",
                "- if you forget homework, Mom says this is why we pack bags",
                "- if you forget which house has what, Asahiko remembers",
                "",
                "Hina note: can a map have one middle?",
            ]
        elif doc_id == "computer_rules":
            L = [
                "COMPUTER_RULES.txt",
                "------------------------------",
                "",
                "1. Homework comes before games.",
                "2. Homework does not include changing your cursor.",
                "3. Homework does not include printing cheat codes.",
                "4. Ask before using the phone line.",
                "5. Nobody may yell DIAL-UP IS SCREAMING at dinner.",
                "6. Asahina gets practice nights.",
                "7. Asahiko gets math nights.",
                "8. Mom gets the computer when she says she gets it.",
                "",
                "Rule 8 is not up for debate.",
            ]
        elif doc_id == "phone_log":
            L = [
                "phone_line_log.txt",
                "------------------------------",
                "",
                "times someone picked up the phone during internet:",
                "",
                "6:12  Asahiko - said he forgot. believable.",
                "6:41  Asahina - said website upload was important.",
                "7:03  Mom - does not count. Mom pays for phone.",
                "7:44  Asahiko - claimed he was checking if dinner existed.",
                "8:01  Asahina - yelled from computer room.",
                "8:38  Dad - called during upload. Mom took it in kitchen.",
                "8:39  Asahiko - turned TV up by two.",
                "",
                "current punishment: both children apologize to the modem.",
            ]
        elif doc_id == "snack_treaty":
            L = [
                "snack_treaty.txt",
                "------------------------------",
                "",
                "SNACK TREATY  (draft 4)",
                "",
                "Article 1: last korokke belongs to whoever called it first.",
                "Article 2: calling it while asleep does not count.",
                "Article 3: Hina may not say 'for my website' to claim pudding.",
                "Article 4: Asahiko may not lick rice crackers to create ownership.",
                "Article 5: Mom can overrule all treaties by cutting fruit evenly.",
                "",
                "signed: asahiko",
                "signed: HINA but under protest",
                "signed: Mom (not legally binding)",
            ]
        elif doc_id == "camera_import":
            L = [
                "camera_import_log.txt",
                "------------------------------",
                "",
                "imported from: FAMILY-CAMERA",
                "destination: Shared Pictures",
                "",
                "pancake_morning.jpg",
                "strawberry_milk.jpg",
                "lunch_box.jpg",
                "curry_night.jpg",
                "festival_noodles.jpg",
                "pudding_cup.jpg",
                "dads_chair.jpg",
                "train_platform.jpg",
                "two_cakes.jpg",
                "",
                "copies also found in:",
                "C:\\HinaSite\\gallery\\",
            ]
        elif doc_id == "album_note":
            L = [
                "album_note.txt",
                "------------------------------",
                "",
                "Ask before putting family pictures online.",
                "Especially pictures with Asahiko in them.",
                "",
                "This means you, Asahina.",
            ]
        elif doc_id == "site_readme":
            L = [
                "README_FIRST.txt",
                "------------------------------",
                "",
                "how to update hinasworld:",
                "",
                "1. edit the html file",
                "2. do NOT delete the old one until new one works",
                "3. upload with cuteftp",
                "4. if it asks about public permissions press no",
                "5. if it asks twice ask Mom",
                "",
                "note from Asahiko: stop naming every file FINAL",
            ]
        elif doc_id == "index_html":
            L = [
                "index_home.html",
                "------------------------------",
                "",
                "<title>~*~ Hina's World ~*~</title>",
                "<body bgcolor=pink>",
                "<marquee>welcome to my page!!</marquee>",
                "<!-- add guestbook here -->",
                "<!-- add new photos but not the ones Mom said no about -->",
                "<!-- remember to make private album PRIVATE this time -->",
                "</body>",
            ]
        elif doc_id == "guestbook_export":
            L = [
                "guestbook_export.txt",
                "------------------------------",
                "",
                "StarCute: FIRST!!",
                "kero_kero_99: found u thru the webring!! kero kero",
                "PixelHeart: your page makes my computer fan go loud",
                "GlitterGardener: enjoy the star cursor!!",
                "Emily_x0x: too many sparkles but fine",
                "xLordVoidx: pink overload. cool marquee tho",
                "new_kid: hina mom says dinner",
                "Hina: STOP USING MY GUESTBOOK FOR DINNER",
                "BlossomMama: lovely page hina. -pixel's mom",
                "FREE_CURSORS_NOW: [removed by HinaWeb spam filter]",
                "",
            ]
            if store.hw_chat_session >= 1:
                L += ["xX_guest_Xx: cute page :)"]
            if hw_escalation_stage() >= 3:
                # he tracks her presence whether or not she ever answered him
                L += ["xX_guest_Xx: u werent on yesterday. hope practice went ok"]
            if store.hw_guest >= 2:
                L += ["xX_guest_Xx: dont let them boss u around. some ppl just get u."]
        elif doc_id == "gallery_manifest":
            L = [
                "gallery_manifest.txt",
                "------------------------------",
                "",
                "track_meet.jpg        public",
                "sleepover.jpg         friends",
                "birthday.jpg          friends",
                "pancake_morning.jpg   public",
                "lunch_box.jpg         public",
                "asahiko_firstday.jpg  DO NOT UPLOAD",
                "",
                "last batch upload: defaulted new photos to public",
            ]
        elif doc_id == "layout_todo":
            L = [
                "layout_todo.txt",
                "------------------------------",
                "",
                "- glitter cursor",
                "- music that does not restart every page",
                "- guestbook colors",
                "- secret page? maybe",
                "- ask PixelHeart how to make comments scroll",
                "- ask Asahiko why he keeps adding DINNER to guestbook",
                "- delete ugly old profile photo",
                "- keep bunny somewhere nobody laughs",
            ]
        elif doc_id == "password_hint":
            L = [
                "password_hint.txt",
                "------------------------------",
                "",
                "password hint:",
                "",
                "favorite after-practice snack + favorite number",
                "",
                "Asahiko says this is not a hint if everyone knows",
                "she always picks the same thing from the station kiosk.",
            ]
        elif doc_id == "old_updates":
            L = [
                "updates_OLD.html",
                "------------------------------",
                "",
                "<b>site updates!!</b>",
                "",
                "9/03 - added guestbook",
                "9/05 - added my favorite songs page",
                "9/08 - fixed broken blink tag",
                "9/09 - took down school map because Mom said ABSOLUTELY NOT",
                "9/10 - maybe add quiz?",
                "",
                "<!-- no link to this page anymore. probably. -->",
            ]
        elif doc_id == "color_tests":
            L = [
                "colors_maybe.txt",
                "------------------------------",
                "",
                "homepage pink:      #ffcce8",
                "button pink:        #ff66cc",
                "guestbook purple:   too purple",
                "secret page black:  too scary",
                "text yellow:        StarCute says unreadable",
                "",
                "Asahiko added green and called it 'less painful'.",
                "Do not use his opinion.",
            ]
        elif doc_id == "counter_backup":
            L = [
                "visitor_counter_BACKUP.txt",
                "------------------------------",
                "",
                "old counter code:",
                "",
                "<script src='free_counter.js'></script>",
                "start number: 001337",
                "show leading zeroes: yes",
                "reset when embarrassed: maybe",
                "",
                "note: the counter goes up when Hina refreshes it.",
                "note from Asahiko: then it is lying.",
            ]
        elif doc_id == "princess_house":
            L = [
                "princess_house_story.txt",
                "------------------------------",
                "",
                "Once there was a princess with TWO castles.",
                "One castle had her cat and computer and mom's good soup.",
                "One castle had a couch that folded out and a loud street.",
                "",
                "The princess did not pick because princesses are not judges.",
                "The king and queen had to stop making her hold the crown.",
                "",
                "Then the castles moved next door to each other and everyone",
                "could eat dinner without checking the clock.",
                "",
                "THE END maybe",
            ]
        elif doc_id == "calm_page":
            L = [
                "calm_page.html",
                "------------------------------",
                "",
                "<title>quiet room</title>",
                "<body bgcolor=white>",
                "things that are quiet:",
                "<br>snow",
                "<br>mochi sleeping",
                "<br>the computer before the modem starts",
                "<br>mom after dad leaves",
                "<br>asahiko when he knows i heard",
                "</body>",
                "",
                "<!-- not linked from homepage -->",
            ]
        elif doc_id == "dad_link_note":
            L = [
                "dad_link_note.txt",
                "------------------------------",
                "",
                "Dad asked for the website address again.",
                "",
                "Do NOT send:",
                "- guestbook",
                "- gallery with the house number",
                "- private album even if it is private",
                "",
                "Maybe send home.html after fixing music.",
                "",
                "Mom said: ask me first.",
                "Dad said: I can see my own kid's website.",
                "Asahiko said: can both of you not do this by the computer.",
            ]
        elif doc_id == "star_pancakes":
            L = [
                "star_pancakes.txt",
                "------------------------------",
                "",
                "Use small pan.",
                "Pour batter in five points first.",
                "Asahina likes the crispy corners.",
                "Serve with kiwi if we have it.",
                "Asahiko says stars taste the same. Ignore him.",
            ]
        elif doc_id == "after_practice_snack":
            L = [
                "after_practice_snack.txt",
                "------------------------------",
                "",
                "cold barley tea",
                "tuna-mayo rice ball if practice runs late",
                "banana if she says she is only a little hungry",
                "custard pudding for Fridays",
                "",
                "Do not comment on how much she eats.",
                "She notices.",
            ]
        elif doc_id == "curry_leftovers":
            L = [
                "curry_leftovers.txt",
                "------------------------------",
                "",
                "Make extra carrots.",
                "Keep one container mild.",
                "Asahina says she doesn't want seconds when people ask.",
                "She gets them later if nobody makes a big deal.",
            ]
        elif doc_id == "grocery_list":
            L = [
                "grocery_list.txt",
                "------------------------------",
                "",
                "milk",
                "strawberry syrup",
                "curry blocks",
                "noodles",
                "cabbage",
                "frozen gyoza",
                "yogurt cups",
                "apples",
                "rice crackers",
                "printer ink (again)",
            ]
        elif doc_id == "lunch_rotation":
            L = [
                "lunch_rotation.txt",
                "------------------------------",
                "",
                "MON  tuna rice ball / cucumber sticks / apple slices",
                "TUE  noodle salad if Asahiko did not spill the sauce",
                "WED  egg sandwich / yogurt cup / tea money",
                "THU  omelette / green beans / tiny fork for Asahina",
                "FRI  noodle roll only if actual lunch was eaten",
                "",
                "Note: Asahina will trade cucumber sticks for almost anything.",
                "Do not pack only cucumber sticks to test this.",
            ]
        elif doc_id == "emergency_dinner":
            L = [
                "emergency_dinner.txt",
                "------------------------------",
                "",
                "IF PRACTICE RUNS LATE:",
                "",
                "1. rice is in cooker",
                "2. soup is in the small pot",
                "3. Asahiko will say he is starving even if he ate",
                "4. Asahina will say she is not hungry if someone asks",
                "5. heat gyoza or leftover nikujaga anyway",
                "",
                "Nobody has died from reheated vegetables.",
            ]
        elif doc_id == "noodles_if_sick":
            L = [
                "noodles_if_sick.txt",
                "------------------------------",
                "",
                "soft noodles",
                "egg if stomach is okay",
                "ginger only if she asks",
                "little scallions, not a whole garden",
                "",
                "Asahiko gets the same if he stops saying he is also sick.",
            ]
        elif doc_id == "nikujaga_notes":
            L = [
                "nikujaga_notes.txt",
                "------------------------------",
                "",
                "thin beef",
                "potatoes",
                "carrots",
                "onion",
                "snap peas if cheap",
                "",
                "Make enough for lunch boxes.",
                "Hide one serving before Asahiko calls it a midnight emergency.",
            ]
        elif doc_id == "freezer_inventory":
            L = [
                "freezer_inventory_OLD.txt",
                "------------------------------",
                "",
                "2 bags frozen gyoza? maybe 1",
                "1 tray korokke",
                "ice pops - lemon only, nobody wants grape",
                "mystery container from last month",
                "frozen peas for rice",
                "",
                "If this list is wrong, blame whoever took the last ice pop.",
            ]
        elif doc_id == "pancake_test":
            L = [
                "pancake_test.txt",
                "------------------------------",
                "",
                "Trial 1:",
                "too much cabbage according to Asahiko",
                "not enough cabbage according to Mom",
                "Asahina said it was fine, ate around the squid",
                "",
                "Trial 2:",
                "never happened because someone used the flour for glue paste",
            ]
        elif doc_id == "asahiko_homework":
            L = [
                "homework_about_family.txt",
                "------------------------------",
                "",
                "My family uses one computer.",
                "My sister Hina makes websites and says not to look",
                "but she looks in my folder all the time.",
                "Mom says sharing means waiting.",
                "",
                "I am still waiting.",
            ]
        elif doc_id == "do_not_read":
            L = [
                "DO_NOT_READ_HINA.txt",
                "------------------------------",
                "",
                "HINA STOP",
                "",
                "if you are reading this then you owe me the good",
                "computer chair AND two korokke from the corner shop.",
                "",
                "also someone named guest keeps showing up in history.",
                "thats weird.",
            ]
        elif doc_id == "cat_names":
            L = [
                "cat_names.txt",
                "------------------------------",
                "",
                "mochi",
                "momo",
                "toast jr",
                "sir paws",
                "",
                "hina says mochi already picked his name.",
            ]
        elif doc_id == "game_cheats":
            L = [
                "platformer_cheats.txt",
                "------------------------------",
                "",
                "UP UP DOWN DOWN LEFT RIGHT",
                "hold jump on level 3",
                "do not let Hina delete this again",
            ]
        elif doc_id == "asahiko_chat_warning":
            L = [
                "weird_chat_people.txt",
                "------------------------------",
                "",
                "things Hina says are NOT my business:",
                "",
                "- her website",
                "- her guestbook",
                "- the purple chat room",
                "- why guest people know her name",
                "",
                "things that are my business:",
                "",
                "- the computer is also mine",
                "- weird guest people are weird",
                "- if Mom asks I warned her first",
            ]
        elif doc_id == "turn_manifesto":
            L = [
                "computer_turn_manifesto.txt",
                "------------------------------",
                "",
                "A FORMAL COMPLAINT",
                "",
                "Hina says 'one more minute' but her minutes are fake.",
                "One Hina minute = 12 normal minutes.",
                "One website upload = whole evening.",
                "One 'I am almost done' = phone line hostage situation.",
                "",
                "Requested solution:",
                "install second computer in my room.",
                "",
                "backup solution:",
                "install lock on Hina.",
            ]
        elif doc_id == "snack_debt":
            L = [
                "snack_debt.txt",
                "------------------------------",
                "",
                "HINA SNACK DEBT LEDGER",
                "",
                "korokke bites:          2",
                "noodle roll half:    disputed",
                "pudding spoonfuls:      4",
                "rice cracker sleeves:   1",
                "ice pop trades:         illegal",
                "cat bribery bonito:     suspicious",
                "",
                "total owed: infinite",
                "",
                "paid if she lets me use the computer first tomorrow.",
            ]
        elif doc_id == "trade_offer":
            L = [
                "trade_offer.txt",
                "------------------------------",
                "",
                "PROPOSAL:",
                "",
                "Asahiko receives: computer from 7:00 to 7:30",
                "Hina receives: my extra grape gummies and silence",
                "",
                "Counteroffer from Hina:",
                "Asahiko receives: one rice cracker",
                "Hina receives: computer until website is done",
                "",
                "status: negotiations collapsed",
            ]
        elif doc_id == "old_save_files":
            L = [
                "save_files_do_not_delete.txt",
                "------------------------------",
                "",
                "Platformer World 3 - save is on memory card OR desktop.",
                "If desktop file is fake, do not delete anyway.",
                "",
                "Files that matter:",
                "hero_final.sav",
                "hero_final2.sav",
                "REAL_hero_final.sav",
                "",
                "Hina says none of these are real.",
                "She is not invited to decide.",
            ]
        elif doc_id == "secret_questions":
            L = [
                "secret_questions.txt",
                "------------------------------",
                "",
                "Hina's password hints are bad.",
                "",
                "bad question: favorite food",
                "bad answer: anyone at school can guess station snacks",
                "",
                "better question: name of first stuffed animal",
                "problem: she put Mr Toast on the homepage",
                "",
                "conclusion: everybody in this house is bad at secrets.",
            ]
        elif doc_id == "dad_question_list":
            L = [
                "questions_for_dad.txt",
                "------------------------------",
                "",
                "questions for Dad",
                "",
                "1. are you coming Saturday",
                "2. do we bring school bags or just overnight bags",
                "3. does Hina have to bring Mr Toast or is that babyish",
                "4. why did you tell Mom one thing and me another",
                "5. can you not say 'be the man of the house' because no",
                "",
                "questions not to ask in front of Hina:",
                "",
                "all of them apparently",
            ]
        elif doc_id == "stair_rules":
            L = [
                "stair_rules.txt",
                "------------------------------",
                "",
                "STAIR RULES",
                "",
                "If Mom and Dad are talking by the sink:",
                "- do not stand on stair 4 because it creaks",
                "- stair 5 is safe if you hold the rail",
                "- Hina is bad at whispering so do not bring her",
                "- if she comes anyway, say you were getting water",
                "",
                "If Dad leaves fast:",
                "- do not run to the window",
                "- Hina will run to the window",
                "- pretend you did not see",
            ]
        elif doc_id == "browser_history":
            L = [
                "history.txt",
                "------------------------------",
                "",
                "account: Hina",
                "",
                "www.hinasworld.net/home.html",
                "www.kidstown-chat.ne.jp/rooms/friends",
                "www.glittercursor-garden.ne.jp/pink/star3",
                "www.trackmeet-results.local/asahina",
                "search: how to make glitter cursor",
                "search: delete guestbook comment",
                "search: why does msn say remember password",
                "search: old soul meaning",
                "search: can someone tell if you block them",
                "search: cute lunch ideas without tomatoes",
                "search: can you have two homes",
                "search: how loud is too loud for parents arguing",
            ]
            if store.hw_chat_session >= 1:
                L += ["www.hinasworld.net/private_album.html", "search: can guests see public profile", "search: how to hide msn contact from mom"]
        elif doc_id == "browser_history_asahiko":
            L = [
                "history_asahiko.txt",
                "------------------------------",
                "",
                "account: Asahiko",
                "",
                "www.cheatplanet.ne.jp/platformer-world",
                "www.catnames.example/mochi",
                "search: how to make sister get off computer",
                "search: does unplugging modem break internet forever",
                "search: how to fix printer says magenta",
                "search: what is magenta",
                "search: is guest in chatroom a virus",
                "search: can mom see history",
                "search: can sisters steal pudding legally",
                "search: dad apartment train stop",
                "search: what does temporary mean",
                "",
                "deleted: no",
                "subtle: also no",
            ]
        elif doc_id == "favorites":
            L = [
                "favorites.txt",
                "------------------------------",
                "",
                "Hina's World",
                "KidsTown Chat",
                "Glitter Cursor Garden",
                "Track Meet Results",
                "Mom's Mail",
                "Recipe Box",
                "CuteFTP Trial Version",
                "Asahiko Cheats (do not click)",
            ]
        elif doc_id == "search_terms":
            L = [
                "search_terms.tmp",
                "------------------------------",
                "",
                "how to make profile private",
                "is old soul a compliment",
                "how to know if someone blocked you msn",
                "how to clear internet history windows xp",
                "track girls eat after practice",
                "why does brother read everything",
                "good comeback for baby drink",
                "what does public profile mean",
            ]
        elif doc_id == "download_log":
            L = [
                "download_log.txt",
                "------------------------------",
                "",
                "glitter_cursor_star.exe        complete",
                "pink_scrollbar_pack.zip        complete",
                "cuteftp_trial_setup.exe        complete",
                "platformer_map_world3.bmp      Asahiko",
                "sparkle_button_FREE.gif        complete",
                "private_album_viewer.exe       failed",
                "",
                "warning: one file was blocked by Internet Explorer.",
            ]
        elif doc_id == "cookies":
            L = [
                "cookies.txt",
                "------------------------------",
                "",
                "hinasworld.net        user=Hina",
                "kidstown-chat.ne.jp   room=friends",
                "glittercursor         color=pink",
                "cheatplanet           user=asahiko_rules",
                "recipebox             user=mom",
                "",
                "Asahiko note: cookies are not real cookies.",
                "Hina note: i know that.",
            ]
        elif doc_id == "print_queue":
            L = [
                "print_queue_old.txt",
                "------------------------------",
                "",
                "Paused jobs:",
                "",
                "001  glitter_cursor_steps.html       Hina",
                "002  map_world3_secret_exit.bmp      Asahiko",
                "003  lunch_rotation.txt              Mom",
                "004  private_album_viewer_coupon     unknown",
                "",
                "Status: printer out of magenta.",
                "Mom note: nothing in this house requires magenta today.",
            ]
        elif doc_id == "toolbar_note":
            L = [
                "toolbar_note.txt",
                "------------------------------",
                "",
                "Internet Explorer has a new toolbar.",
                "",
                "Hina says it came with the sparkle buttons.",
                "Asahiko says it watches you.",
                "Mom says both of you stop clicking YES.",
                "",
                "Buttons visible:",
                "Search!!!",
                "Smileys",
                "Win A Prize",
                "Coupon Lunch Club",
            ]
        elif doc_id == "map_searches":
            L = [
                "map_searches.txt",
                "------------------------------",
                "",
                "recent map lookups:",
                "",
                "home -> Dad work",
                "home -> station blue vending machine",
                "station -> Dad new building",
                "Dad new building -> aquarium",
                "home -> ward office Saturday desk",
                "",
                "last one typed by: Mom",
                "deleted from address bar: yes",
                "deleted from file: no",
            ]
        elif doc_id == "saved_mail_headers":
            L = [
                "mail_headers.txt",
                "------------------------------",
                "",
                "Saved mail subjects only:",
                "",
                "Re: Saturday timing",
                "Re: Please do not promise them things first",
                "School forms - father signature line",
                "Utility bill / name change question",
                "Asahina website photos",
                "This is not a conversation for the kids",
                "",
                "body text not available offline.",
            ]
        elif doc_id == "msn_contacts":
            L = [
                "contacts.cache",
                "------------------------------",
                "",
                "StarCute        online",
                "PixelHeart      away",
                "Emily_x0x       busy",
                "new_kid         offline",
            ]
            if store.hw_guest >= 1:
                L += ["xX_guest_Xx     online"]
            elif hw_escalation_stage() >= 2:
                L += ["", "1 contact request waiting: xX_guest_Xx", "(not answered)"]
        elif doc_id == "away_messages":
            L = [
                "away_messages.txt",
                "------------------------------",
                "",
                "dinner brb",
                "practice!!!",
                "dont call the phone line",
                "if mom asks i am doing homework",
                "sleeping early :)",
            ]
        elif doc_id == "blocked_users":
            L = [
                "blocked_users.txt",
                "------------------------------",
                "",
            ]
            if store.hw_guest <= 0:
                L += ["xX_guest_Xx"]
            else:
                L += ["(empty)"]
        elif doc_id == "nudge_log":
            L = [
                "nudge_log.txt",
                "------------------------------",
                "",
                "last 24 hours:",
                "",
                "StarCute nudged Hina 3 times",
                "Emily_x0x nudged Hina 1 time",
                "PixelHeart nudged Hina 8 times (apologized)",
                "kero_kero_99 nudged Hina 1 time (wrong window, apologized in frog)",
                "new_kid nudged Hina 14 times from downstairs",
                "",
                "system note: excessive nudging may annoy contacts.",
                "Hina note: TELL ASAHIKO THAT",
            ]
            if store.hw_chat_session >= 1:
                L += ["xX_guest_Xx nudged Hina 1 time"]
        elif doc_id == "display_names":
            L = [
                "display_names.txt",
                "------------------------------",
                "",
                "Hina -> Hina ☆ online",
                "Hina -> Hina!! brb dinner",
                "Hina -> hinasworld.net updated!!",
                "Hina -> not a baby",
                "Hina -> doing homework (real)",
                "",
                "Asahiko -> NEW_KID",
                "Asahiko -> new_kid_not_brother",
                "Asahiko -> HINA GIVE COMPUTER",
                "",
                "Mom -> Mom",
                "Mom -> I can read these names",
            ]
        elif doc_id == "deleted_guestbook":
            L = [
                "deleted_guestbook_comment.tmp",
                "------------------------------",
                "",
                "recovered text:",
                "",
                "cute page. don't listen when they call you little.",
                "some people see the real you.",
            ]
            if store.hw_chat_session < 1:
                L += ["", "date: unknown"]
            else:
                L += ["", "user: xX_guest_Xx"]
        elif doc_id == "old_profile":
            L = [
                "old_profile_about.txt",
                "------------------------------",
                "",
                "Hina loves cartoons, running, drawing, sleepovers,",
                "mr toast, strawberry milk, and when Asahiko stops",
                "breathing on her keyboard.",
                "",
                "profile status: friends only",
            ]
        elif doc_id == "bad_shortcut":
            L = [
                "private_album.lnk",
                "------------------------------",
                "",
                "Shortcut target missing.",
                "",
                "C:\\HinaSite\\gallery\\private\\",
                "",
                "Windows cannot verify who created this shortcut.",
            ]
        elif doc_id == "deleted_rules":
            L = [
                "COMPUTER_RULES_old.txt",
                "------------------------------",
                "",
                "OLD RULES - DO NOT USE",
                "",
                "1. Be nice.",
                "2. Take turns.",
                "3. Do not download anything with dancing letters.",
                "4. Do not type with jam fingers.",
                "5. Do not rename Mom's files to MOM BORING.",
                "6. Do not rename Asahiko's files to ASAHIKO BORING.",
                "7. Do not rename Asahina's files to HINA WORLD DOMINATION.",
                "",
                "These rules failed immediately.",
            ]
        elif doc_id == "deleted_recipe":
            L = [
                "omurice_final_FINAL.txt",
                "------------------------------",
                "",
                "FINAL OMURICE NOTES",
                "",
                "Ketchup face should be a heart, not a cat.",
                "Asahiko says the cat was recognizable.",
                "Mom says nobody who writes HINA WORLD DOMINATION",
                "in ketchup gets to call this dinner subtle.",
                "",
                "not final. pan too hot.",
            ]
        elif doc_id == "deleted_grocery":
            L = [
                "grocery_list_lastweek.txt",
                "------------------------------",
                "",
                "already bought / probably:",
                "",
                "cabbage",
                "bean sprouts",
                "mackerel tins",
                "peaches in syrup",
                "yakinoodles",
                "mini jellies for lunch boxes",
                "",
                "Do not buy more bean sprouts unless we want to become bean sprouts.",
            ]
        elif doc_id == "desktop_cleanup":
            L = [
                "desktop_cleanup_wizard.log",
                "------------------------------",
                "",
                "Windows found unused desktop shortcuts:",
                "",
                "HinaSite Backup - 89 days",
                "CuteFTP Trial - 14 days",
                "Private Album - unknown",
                "Asahiko DO NOT OPEN - opened yesterday",
                "",
                "Recommendation: move unused files.",
                "User response: canceled.",
            ]
        elif doc_id == "old_lunch_note":
            L = [
                "lunch_note_unsent.txt",
                "------------------------------",
                "",
                "Asahina,",
                "",
                "I packed extra edamame because practice is long today.",
                "You do not have to finish it if the cafeteria is too loud.",
                "Just eat something, okay?",
                "",
                "Love, Mom",
                "",
                "[not printed]",
            ]
        elif doc_id == "deleted_family_note":
            L = [
                "for_dad_unsent.txt",
                "------------------------------",
                "",
                "Dad,",
                "",
                "i made a page with quiet music so you and mom can",
                "use it when you talk and then maybe not get mad.",
                "",
                "it has stars because mom likes when things are neat",
                "and you like space shows.",
                "",
                "asahiko said this is not how grownups work but he",
                "also said my cursor was bad and then used it.",
                "",
                "please come to track day if mom says ok.",
                "",
                "[not sent]",
            ]
        elif doc_id == "deleted_story":
            L = [
                "normal_house_story_OLD.txt",
                "------------------------------",
                "",
                "Once there was a normal house.",
                "It had one dinner table and four chairs.",
                "Nobody counted chairs because all of them were used.",
                "",
                "The brother was annoying but brave.",
                "The sister was cute but not a baby.",
                "The mom slept more.",
                "The dad did not check his watch by the door.",
                "",
                "Then the house stayed normal forever.",
                "",
                "Asahiko note: this is too obvious.",
                "Hina note: nobody asked you.",
            ]
        elif doc_id == "help_support":
            L = [
                "Help and Support.txt",
                "------------------------------",
                "",
                "Windows Help could not connect to the Help Center.",
                "",
                "Try again later.",
            ]
        else:
            L = [doc_id + ".txt", "------------------------------", "", "(empty)"]
        return u"\n".join(L)

    def hw_diary():
        L = ["diary.txt", "------------------------------", "", ""]
        L += [
            u"sept 2 - i made a WEBSITE today!!! it has my name and",
            u"         my games and a picture of my bunny mr toast.",
            u"         im going to be SO popular :D",
            u"", u"",
        ]
        if store.hinas_world_seen_outfitter:
            if store.hw_grow > store.hw_kept_child:
                L += [
                    u"??? - emily helped me pick newer clothes. she says",
                    u"      the kid stuff makes ppl not take u serious.",
                    u"      i looked older in the mirror. i didnt smile",
                    u"", u"",
                ]
            else:
                L += [
                    u"??? - i kept my favorites on, bunny and all. i know",
                    u"      its babyish but it feels like ME",
                    u"", u"",
                ]
        if store.hinas_world_seen_chatting:
            if store.hw_guest >= 2:
                L += [
                    u"??? - i gave the nice older boy my msn. hes the only",
                    u"      one who doesnt call me a baby. he said dont",
                    u"      tell mom. ok. its just ours",
                    u"", u"",
                ]
            elif store.hw_cruel >= 2:
                L += [
                    u"??? - everyone laughed at the new kid so i laughed too.",
                    u"      he typed my name first. i think it was asahiko.",
                    u"      i didnt stop. it worked. i feel sick",
                    u"", u"",
                ]
            elif store.hw_kind >= 2:
                L += [
                    u"??? - everyone piled on the new kid so i told them to",
                    u"      quit it. emilys mad now. (i think it was asahiko",
                    u"      trying to find me in there.) worth it",
                    u"", u"",
                ]
            else:
                L += [
                    u"??? - the chat is loud and everyone wants me to be",
                    u"      diffrent. i just sat there",
                    u"", u"",
                ]
        if store.hinas_world_seen_rating:
            if store.hw_rating_total >= 18:
                L += [
                    u"??? - i got a high score today!! i HAVE to keep it",
                    u"      up now. cant slip. cant let them down",
                    u"", u"",
                ]
            else:
                L += [
                    u"??? - my score went down. i'll try harder. i'll be",
                    u"      better tomorow",
                    u"", u"",
                ]
        if store.hinas_world_seen_bento:
            if store.hw_bento_light >= 2:
                L += [
                    u"??? - i packed the light lunch. emily says track",
                    u"      girls dont do seconds. my stomach was so loud",
                    u"      in math i pretended it was my chair",
                    u"", u"",
                ]
            else:
                L += [
                    u"??? - the lunch game let me pack ALL my favorites.",
                    u"      mom packed almost the same thing for real.",
                    u"      shes magic like that",
                    u"", u"",
                ]
        if store.hinas_world_seen_petsalon:
            if store.hw_pet_result == "hid":
                L += [
                    u"??? - emily almost saw the pet game so i closed it",
                    u"      super fast. its just a game. i dont know why",
                    u"      my heart was going so loud",
                    u"", u"",
                ]
            else:
                L += [
                    u"??? - mochi sat on the keyboard and got a high",
                    u"      score in the pet game. best day. im not",
                    u"      telling emily about any of it",
                    u"", u"",
                ]
        if store.hinas_world_seen_makeover:
            if store.hw_makeover_guess >= 12:
                L += [
                    u"??? - the mirror game said i look {}!! i wrote it".format(store.hw_makeover_guess),
                    u"      on my hand so i can do the same settings",
                    u"      tomorow. {}. imagine".format(store.hw_makeover_guess),
                    u"", u"",
                ]
            else:
                L += [
                    u"??? - the mirror said {}. star said GOOD. she".format(max(9, store.hw_makeover_guess)),
                    u"      likes me the regular way",
                    u"", u"",
                ]
        # closing -- always sad; flavour from how hard you pushed
        tone = hw_ending_tone()
        L += [u""]
        if tone in ("harsh", "pushed"):
            L += [
                u"i dont play the games anymore. theres no time to be",
                u"little. theres too much to keep up with now.",
            ]
        elif tone == "tender":
            L += [
                u"i think i'm still aloud to be little a bit longer.",
                u"i hope so. i'm not ready to be done yet.",
            ]
        else:
            L += [
                u"i talk to the screen even when nobodys there.",
                u"its better than how quiet my room gets.",
            ]
        # the quiet gut-punch -- her real age, never stated, only shown
        L += [
            u"",
            u"i lost a tooth today. the toothfairy still comes for me.",
            u"i didnt tell anyone online. theyd laugh.",
            u"",
            u"                              - hina",
        ]
        return u"\n".join(L)

    def hw_closet():
        o = store.hw_outfit or {}
        items = [v for v in o.values() if v]
        L = ["closet.txt", "------------------------------", "", u"today hina is wearing:", u""]
        if items:
            for v in items:
                L.append(u"  - " + v)
        else:
            L.append(u"  - (nothing picked)")
        L += [u""]
        if store.hw_grow > store.hw_kept_child:
            L += [u"saved to her public profile. she looks older in it.", u"63 people viewed this look."]
        else:
            L += [u"saved to her public profile. it's very her.", u"3 people viewed this look."]
        return u"\n".join(L)

    def hw_chat_file():
        completed = min(store.hw_chat_session, len(HW2_CHAT_SCRIPTS))
        L = ["chat.txt", "------------------------------", "", u"saved rooms - HinaWeb Chat 2.1", u""]
        L += [u"rooms saved: {} / {}".format(completed, len(HW2_CHAT_SCRIPTS)), u""]
        if completed >= 1:
            L += [
                u"> new_kid knew about the downstairs computer and the phone line.",
                u"  everybody laughed before he could pretend he was a stranger.",
                u"",
            ]
        if store.hw_cruel >= 2:
            L += [u"> you and DreamyDoll piled on new_kid till he left.", u"  he typed Hina's name first, then deleted most of it.", u""]
        elif store.hw_kind >= 2:
            L += [u"> you stuck up for new_kid. emily's annoyed with you.", u"  new_kid logged off anyway, but not mad.", u""]
        if store.hw_guest >= 2:
            L += [u"> xX_guest_Xx is on her contacts now.", u"  he asked her not to mention him.", u""]
        elif store.hw_guest == 1:
            L += [u"> xX_guest_Xx keeps messaging. she hasn't said no.", u""]
        else:
            L += [u"> xX_guest_Xx left on read. good.", u""]
        if completed >= len(HW2_CHAT_SCRIPTS):
            L += [u"nobody else is online now."]
        else:
            L += [u"the room empties out by the end. it always does."]
        return u"\n".join(L)

    def hw_quiz_file():
        grown = store.hw_grow
        L = ["quiz.txt", "------------------------------", "", u"QUIZ RESULT", u""]
        if grown >= 4:
            L += [u"You got:  OLD SOUL  ♥", u"Mature, cool, ahead of the curve. Everyone says so."]
        elif grown >= 2:
            L += [u"You got:  COOL FOR YOUR AGE  ♥", u"Growing up fast! Keep it up~"]
        else:
            L += [u"You got:  SWEET & SILLY  ♥", u"You're just a kid, and that's okay!"]
        L += [u"", u"result posted to your public profile."]
        if store.hw_guest >= 1:
            L += [u"1 new profile viewer:  xX_guest_Xx"]
        return u"\n".join(L)

    def hw_scores_file():
        t = store.hw_rating_total   # 5..25
        avg = t / 5.0
        L = ["scores.txt", "------------------------------", "", u"today's rating:  {:.1f} / 5".format(avg), u""]
        if t >= 18:
            L += [u"hina saw the score.", u'she wrote back: "i\'ll keep it up!! ♥"']
        elif t >= 10:
            L += [u"hina saw the score.", u'she wrote back: "i\'ll do better tomorow"']
        else:
            L += [u"hina saw the score.", u'she wrote back: "ok. i understand."', u"she didn't log on the next day."]
        return u"\n".join(L)

    def hw_bento_file():
        b = store.hw_bento or {}
        items = [v for v in b.values() if v]
        L = ["lunchbox.txt", "------------------------------", "", u"packed today:", u""]
        if items:
            for v in items:
                L.append(u"  - " + v)
        else:
            L.append(u"  - (nothing packed)")
        L += [u""]
        if store.hw_bento_fav > store.hw_bento_light:
            L += [
                u"the box came back empty.",
                u"she traded the boring part for a rice cracker. obviously.",
            ]
        elif store.hw_bento_light >= 2:
            L += [
                u"the box came back almost full.",
                u'"wasn\'t hungry." second time this week.',
            ]
        else:
            L += [u"the box came back half full. practice ran long."]
        if hw_escalation_stage() >= 2:
            L += [
                u"",
                u"the team page posted lunch photos again.",
                u"she checked the comments before she ate.",
            ]
        return u"\n".join(L)

    def hw_pet_file():
        L = ["mochi_and_toast.txt", "------------------------------", ""]
        if store.hw_pet_result == "hid":
            L += [
                u"last played: today. two minutes.",
                u"the window closed in a hurry.",
                u"",
                u"mochi waited by the chair anyway.",
                u"mr toast doesn't mind waiting. it's what he's for.",
            ]
        else:
            L += [
                u"care level: ***** (max)",
                u"",
                u"she plays this one with the sound turned down",
                u"so nobody hears the music.",
                u"",
                u"mochi doesn't care how old she acts.",
                u"neither does the bunny.",
            ]
        return u"\n".join(L)

    def hw_mirror_file():
        g = store.hw_makeover_guess
        L = ["mirror.txt", "------------------------------", "", u"the mirror said {}.".format(g), u""]
        if g >= 12:
            L += [
                u"she wrote the number on her hand.",
                u"it washed off in the bath. she wrote it again.",
            ]
        elif g >= 10:
            L += [u"she asked it twice more to be sure."]
        elif store.hw_kept_child > store.hw_grow:
            L += [u"she made a face at it and went back to playing."]
        else:
            L += [u"she wiped the result and started over."]
        L += [u"", u"result posted to your public profile."]
        if store.hw_guest >= 1 and hw_escalation_stage() >= 1:
            L += [
                u"",
                u'1 comment:  "the mirror gets it right sometimes :)"',
                u"            - xX_guest_Xx",
            ]
        return u"\n".join(L)

    def hw_message_file():
        # The sharp edge. Only exists if the player let hw_guest reach 2. No
        # explicit content -- just the grooming red flags (flattery, secrecy,
        # isolation, "more grown up," a request) that the topic is ABOUT.
        L = [
            u"(1) new message  -  xX_guest_Xx",
            u"------------------------------",
            u"",
            u"hey :) glad u added me.",
            u"",
            u"ur different from the other kids on there.",
            u"more grown up. i feel like i can actually talk to u.",
            u"",
            u"dont tell emily we talk, ok? or ur mom.",
            u"they wouldnt get it. its just our thing :)",
            u"",
            u"send me the outfit from the dress-up game?",
            u"the cute one. just between us ♥",
            u"",
            u"      [ Reply ]        [ Block ]",
        ]
        return u"\n".join(L)

    def hw_visitor_log():
        L = [
            u"visitor_log.txt",
            u"------------------------------",
            u"",
            u"HinaWeb SiteStats 2.0",
            u"",
            u"visits this session: {}".format(hw_pressure_score()),
            u"current visitor no.: {}".format(hw_visitor_number()),
            u"last updated from: FAMILY-COMPUTER",
            u"",
            u"recent pages:",
            u"  /home.html",
            u"  /games.html",
        ]
        if store.hinas_world_seen_chatting:
            L.append(u"  /chat/room_saved.html")
        if store.hinas_world_seen_quiz or store.hinas_world_seen_rating:
            L.append(u"  /profile/result_public.html")
        if hw_escalation_stage() >= 2:
            L += [u"", u"referrer: guestbook_export"]
        return u"\n".join(L)

    def hw_profile_cache():
        L = [
            u"profile_cache.txt",
            u"------------------------------",
            u"",
            u"public profile fields cached:",
            u"",
            u"  name: Hina",
            u"  computer: shared family pc",
            u"  favorite pages: gallery, games, guestbook",
            u"  profile age: guessed older",
            u"",
            u"privacy: public",
            u"profile link: visible from guestbooks",
            u"search listing: not submitted",
        ]
        if store.hw_guest >= 1:
            L += [u"", u"1 viewer saved this profile to favorites."]
        return u"\n".join(L)

    def hw_autocomplete_file():
        L = [
            u"autocomplete.txt",
            u"------------------------------",
            u"",
            u"Internet Explorer AutoComplete",
            u"",
            u"saved form entries:",
            u"  name: Hina",
            u"  screen name: hinasworld",
            u"  favorite snack: station korokke / peach jelly",
            u"  profile mood: older than they think",
            u"",
            u"remember passwords: no",
            u"clear saved forms: no",
        ]
        if store.hw_chat_session >= 1:
            L += [u"", u"recent contact typed: xX_guest_Xx"]
        return u"\n".join(L)

    def hw_recent_status_file():
        L = [
            u"recent_status.txt",
            u"------------------------------",
            u"",
            u"MSN Messenger cached status",
            u"",
            u"Hina - Online at 9:47 PM",
            u"away message: working on my site!!",
            u"",
            u"recent profile viewers:",
            u"  StarCute",
            u"  Emily_x0x",
        ]
        if store.hw_chat_session >= 1:
            L.append(u"  xX_guest_Xx")
        return u"\n".join(L)

    def hw_file_body(name):
        if name == "diary.txt":
            return hw_diary()
        if name == "closet.txt":
            return hw_closet()
        if name == "chat.txt":
            return hw_chat_file()
        if name == "quiz.txt":
            return hw_quiz_file()
        if name == "scores.txt":
            return hw_scores_file()
        if name == "lunchbox.txt":
            return hw_bento_file()
        if name == "mochi_and_toast.txt":
            return hw_pet_file()
        if name == "mirror.txt":
            return hw_mirror_file()
        if name.startswith("(1)"):
            return hw_message_file()
        if name == "visitor_log.txt":
            return hw_visitor_log()
        if name == "profile_cache.txt":
            return hw_profile_cache()
        if name == "autocomplete.txt":
            return hw_autocomplete_file()
        if name == "recent_status.txt":
            return hw_recent_status_file()
        return name

    # Each photo has its child's caption (normal) and a grounded "exposure" line
    # (wrong). The wrong line is NEVER the photo changing by itself -- it is the
    # realisation that a real picture of a real kid is now public, saved, or being
    # picked over by a stranger. That is the actual horror; no haunting required.
    HW2_GALLERY_PHOTOS = [
        ("Track Meet", "field day!! i got a ribbon", "field day. a guest saved this one to keep."),
        ("Sleepover", "best friends forever!!", "this one's public now. not just friends."),
        ("Birthday", "my party with too much cake", "strangers can count the candles."),
        ("First Day", "first day!! asahiko cried more than me", "mom said don't post asahiko. it's public anyway."),
        ("Computer Desk", "taking turns on the family computer", "you can read the address on the mail. so can they."),
        ("Backyard", "asahiko stole the hose!!", "his whole face is in this one. it's up."),
        ("Pancake Morning", "dad made pancakes shaped like stars", "a guest left a comment about what i eat."),
        ("Strawberry Milk", "favorite drink after practice!!", "someone i don't know added this to favorites."),
        ("Lunch Box", "mom put little tomatoes in a heart", "a stranger knows what's in my lunch now."),
        ("Donut Day", "sprinkles make everything better", "the newest comments aren't from friends."),
        ("Curry Night", "second bowl because it was soooo good", "someone online keeps count of what i eat."),
        ("Festival Noodles", "summer festival dinner!! sauce everywhere", "a guest knows which festival stall we went to."),
        ("Pudding Cup", "saved the caramel part for last", "the newest comment knows what was in the fridge."),
        ("Korokke Run", "corner shop korokke after practice", "someone online asks which route we walk home."),
        ("Dad's Chair", "dad's chair is the best for games", "the chair is empty in every newer picture."),
        ("Train Platform", "weekend train with asahiko!!", "the station name tells people which way dad went."),
        ("Two Cakes", "two birthdays means two cakes!!", "two cakes also means two rooms, two tables, two stories."),
    ]

    # The passerby cast, so the site reads like a real webring neighborhood and
    # not a five-person stage play: friendly randoms (kero_kero_99, otter_pop,
    # webmistress_yui, GlitterGardener), hecklers (xLordVoidx, PoisonBerry13),
    # a spam bot (FREE_CURSORS_NOW), and ONE transparent benign adult
    # (BlossomMama, Pixel's mom, always signs who she is) -- the deliberate
    # contrast that makes the guest's anonymity read as a choice.
    HW2_GALLERY_COMMENTS = {
        "Track Meet": [
            ("StarCute", "speedy hina!! ribbon girl", "friend"),
            ("kero_kero_99", "i was at that meet!! my sister ran the relay. kero", "friend"),
            ("DreamyDoll", "field day pics are soooo tryhard", "troll"),
        ],
        "Sleepover": [
            ("PixelHeart", "i miss this one. my bangs were tragic lol", "friend"),
            ("Emily_x0x", "delete the pajama pic before school finds it", "friend"),
            ("DreamyDoll", "lmaooooo baby blankets is crazy", "troll"),
            ("xLordVoidx", "girl sites are all sleepovers and glitter. yawn", "troll"),
        ],
        "Birthday": [
            ("StarCute", "cake cake cake!!", "friend"),
            ("BlossomMama", "happy birthday hina! -pixel's mom", "friend"),
            ("Guest_17", "why do kid parties always look sticky", "troll"),
        ],
        "First Day": [
            ("new_kid", "i did NOT cry more than you", "friend"),
            ("Emily_x0x", "awww little asahiko backpack", "friend"),
        ],
        "Computer Desk": [
            ("new_kid", "mom said my turn after your website", "friend"),
            ("webmistress_yui", "we have the same keyboard!! mine sticks too", "friend"),
            ("Guest_44", "public computer public page. makes sense.", "troll"),
        ],
        "Backyard": [
            ("StarCute", "hose fight champion", "friend"),
            ("otter_pop", "hose fight hose fight hose fight", "friend"),
            ("DreamyDoll", "why is your brother always lurking", "troll"),
        ],
        "Pancake Morning": [
            ("StarCute", "star pancakes rule", "friend"),
            ("otter_pop", "STAR SHAPED?? my dad only does circles", "friend"),
            ("PixelHeart", "save me the tiny burned one next time", "friend"),
        ],
        "Strawberry Milk": [
            ("Emily_x0x", "thats such a little kid drink lol", "troll"),
            ("PoisonBerry13", "baby drink babyyy drink", "troll"),
            ("StarCute", "no it's good. don't listen", "friend"),
        ],
        "Lunch Box": [
            ("PixelHeart", "your mom makes cute lunches", "friend"),
            ("Guest_17", "heart tomatoes? embarrassing", "troll"),
        ],
        "Donut Day": [
            ("StarCute", "sprinkles fix math tests", "friend"),
            ("DreamyDoll", "two donuts. someone's feeling brave", "troll"),
            ("FREE_CURSORS_NOW", "CLICK HERE for 1000 free cursors!! (link removed by HinaWeb)", "troll"),
        ],
        "Curry Night": [
            ("new_kid", "you said i could have the last potato", "friend"),
            ("Guest_44", "track girls eat seconds?", "troll"),
        ],
        "Festival Noodles": [
            ("StarCute", "festival sauce on your sleeve forever", "friend"),
            ("kero_kero_99", "i went sunday!! did u do the goldfish scoop", "friend"),
            ("Guest_17", "that stall is near the station, right?", "troll"),
        ],
        "Pudding Cup": [
            ("new_kid", "you ate my caramel part. criminal.", "friend"),
            ("PixelHeart", "custard pudding is the best one, no contest", "friend"),
        ],
        "Korokke Run": [
            ("new_kid", "corner shop lady gave me the bigger one", "friend"),
            ("PixelHeart", "hot korokke after practice is unbeatable", "friend"),
        ],
        "Dad's Chair": [
            ("new_kid", "that chair is not yours just because you spin in it", "friend"),
            ("StarCute", "why is it by the window now?", "friend"),
            ("webmistress_yui", "comfy chairs make the best game chairs", "friend"),
        ],
        "Train Platform": [
            ("new_kid", "you promised not to post the station sign", "friend"),
            ("Emily_x0x", "weekend dad trip?", "friend"),
            ("xLordVoidx", "trains. riveting content as usual", "troll"),
        ],
        "Two Cakes": [
            ("StarCute", "two cakes is powerful actually", "friend"),
            ("BlossomMama", "two parties! lucky girl. -pixel's mom", "friend"),
            ("new_kid", "one had better frosting and i stand by that", "friend"),
        ],
    }

    # Two tiers, same man, same photos -- only the distance changes, and that gap
    # IS the escalation. Early (stage 1-2): publicly defensible, the kind of
    # comment nobody could report; a couple of them fish for details, but framed
    # as small talk. Late (stage 3+): familiar, entitled, quietly watching --
    # never announcing itself, never explicit. He should read as a nice guy for
    # as long as possible; the player connects the dots before the kids do.
    HW2_GALLERY_CREEP_EARLY = {
        "Track Meet": "congrats on the ribbon :) hard work shows.",
        "Sleepover": "looks fun. good friends matter.",
        "Birthday": "happy late birthday :)",
        "First Day": "cute pic. time flies huh.",
        "Computer Desk": "nice setup. i had those same speakers once.",
        "Backyard": "summer pics are the best pics.",
        "Pancake Morning": "star pancakes, nice. talented dad.",
        "Strawberry Milk": "dont let anyone tease u about what u like.",
        "Lunch Box": "ur mom puts real effort in. lucky kid.",
        "Donut Day": "everyone deserves a donut day :)",
        "Curry Night": "curry night is the best night.",
        "Festival Noodles": "festivals are great. which one is this?",
        "Pudding Cup": "saving the caramel for last is the correct way.",
        "Korokke Run": "after-practice snack. u earned it.",
        "Dad's Chair": "comfy chair. best seat in the house?",
        "Train Platform": "day trips are fun :)",
        "Two Cakes": "two cakes!! lucky :)",
    }

    HW2_GALLERY_CREEP_COMMENTS = {
        "Track Meet": "u look proud here. keep this one up.",
        "Sleepover": "didnt see this one before. i check every day :)",
        "Birthday": "cute age. older than they treat u though.",
        "First Day": "u were easy to spot even back then.",
        "Computer Desk": "family computers never stay private. careful.",
        "Backyard": "u smile even when nobody else is. i notice stuff like that.",
        "Pancake Morning": "star pancakes. knew u had good taste.",
        "Strawberry Milk": "still ur favorite? u told me that once.",
        "Lunch Box": "your mom watches close, huh?",
        "Donut Day": "sweet things suit u.",
        "Curry Night": "second bowl means u know what u want.",
        "Festival Noodles": "i think ive been to that one. small world :)",
        "Pudding Cup": "u save the best part. patient.",
        "Korokke Run": "same shop every time? loyal :)",
        "Dad's Chair": "empty chairs still say a lot.",
        "Train Platform": "i know that station. ive changed lines there.",
        "Two Cakes": "lucky. two birthdays for one girl.",
    }

    def hw_note_photo_view(slot):
        # Looking is the trigger. The photos you actually open are the first to
        # "turn" -- i.e., the first a stranger notices too. The player decides the
        # order and the tempo; the direction (more exposure) never reverses.
        if slot not in store.hw_photos_viewed:
            store.hw_photos_viewed = store.hw_photos_viewed + [slot]

    def hw_photo_turn_order():
        # viewed photos first (in the order you opened them), then the rest
        viewed = [s for s in store.hw_photos_viewed]
        rest = [name for (name, _n, _w) in HW2_GALLERY_PHOTOS if name not in viewed]
        return viewed + rest

    def hw_photos_turned_count():
        # Nothing turns during the grace period. Past the threshold it creeps in
        # ~one photo per couple of clicks (measured from grace, so it starts at 0
        # and ramps -- no slam). Monotonic; never goes back.
        over = hw_pressure_over()
        if over < 1:
            return 0
        return max(0, min(len(HW2_GALLERY_PHOTOS), over // 2))

    def hw_photo_turned(slot):
        order = hw_photo_turn_order()
        if slot not in order:
            return False
        return order.index(slot) < hw_photos_turned_count()

    def hw_gallery_caption(slot, corruption=0):
        for name, normal, wrong in HW2_GALLERY_PHOTOS:
            if name == slot:
                return wrong if hw_photo_turned(slot) else normal
        return u"photo"

    def hw_photo_status(slot):
        # the grounded "what happened to this photo" line under the viewer
        if not hw_photo_turned(slot):
            return u"saved to: friends only"
        seen_by = 1 + (store.hw_guest if store.hw_guest > 0 else 0) + max(0, hw_escalation_stage() - 1)
        if store.hw_chat_session >= 1 and store.hw_guest >= 1:
            return u"public  ||  1 guest has this saved  ||  seen by {}".format(seen_by)
        return u"public  ||  seen by {}".format(seen_by)

    def hw_gallery_comments(slot):
        out = list(HW2_GALLERY_COMMENTS.get(slot, []))
        if hw_escalation_stage() >= 2:
            out.append(("system", "linked from guestbook", "system"))
        if hw_escalation_stage() >= 1 and store.hw_chat_session >= 1 and slot in HW2_GALLERY_CREEP_COMMENTS:
            _tier = HW2_GALLERY_CREEP_COMMENTS if hw_escalation_stage() >= 3 else HW2_GALLERY_CREEP_EARLY
            out.append(("xX_guest_Xx", _tier.get(slot, HW2_GALLERY_CREEP_COMMENTS[slot]), "creep"))
        if hw_escalation_stage() >= 4:
            out.append(("system", "comments are visible to all visitors", "system"))
        if not out:
            out.append(("system", "comments closed", "system"))
        return out

    def hw_game_blurb(game_id, blurb):
        if game_id == "chatting":
            return hw_chat_card_blurb()
        if hw_escalation_stage() >= 3:
            # NOTE: "petsalon" is deliberately absent -- the pet game is the one
            # corner of the site that never sours. The wrongness there is only
            # that she stops opening it.
            altered = {
                "outfitter": "Dress Hina for the new profile picture.",
                "quiz": "Find out what your answers say about you.",
                "rating": "Score today's Hina before the guestbook does.",
                "bento": "Pack Hina's lunch. Light ones score better.",
                "makeover": "Find out how old you really look.",
            }
            return altered.get(game_id, blurb)
        if hw_escalation_stage() >= 1 and game_id == "rating":
            return "Score today's Hina out of five. Results may be posted."
        return blurb

# -----------------------------------------------------------------------------
#  TRANSFORMS
# -----------------------------------------------------------------------------
transform hw2_blink:
    block:
        alpha 1.0
        pause 0.45
        alpha 0.25
        pause 0.45
        repeat

screen hw2_icon(kind="doc", glyph="txt", size=46, blink=False):
    style_prefix "hw"
    fixed:
        xysize (size, size)
        xalign 0.5
        if kind == "folder":
            frame:
                xpos 2
                ypos 7
                xysize (int(size * 0.52), int(size * 0.18))
                padding (0, 0, 0, 0)
                background "#f2c84b"
            frame:
                xpos 0
                ypos int(size * 0.24)
                xysize (size, int(size * 0.62))
                padding (0, 0, 0, 0)
                background "#f0d060"
        elif kind == "image":
            frame:
                xysize (size, size)
                padding (0, 0, 0, 0)
                background "#ffffff"
            frame:
                xpos 4
                ypos 4
                xysize (size - 8, size - 8)
                padding (0, 0, 0, 0)
                background "#b9dcff"
            frame:
                xpos int(size * 0.12)
                ypos int(size * 0.62)
                xysize (int(size * 0.76), int(size * 0.18))
                padding (0, 0, 0, 0)
                background "#5ca65c"
            frame:
                xpos int(size * 0.62)
                ypos int(size * 0.18)
                xysize (int(size * 0.14), int(size * 0.14))
                padding (0, 0, 0, 0)
                background "#fff060"
        elif kind == "app":
            frame:
                xysize (size, size)
                padding (0, 0, 0, 0)
                background "#c20060"
            text glyph:
                color "#ffff99"
                bold True
                size int(size * 0.58)
                xalign 0.5
                yalign 0.5
        elif kind == "pc":
            frame:
                xpos 3
                ypos 4
                xysize (size - 6, int(size * 0.62))
                padding (0, 0, 0, 0)
                background "#d4d0c8"
            frame:
                xpos 7
                ypos 8
                xysize (size - 14, int(size * 0.42))
                padding (0, 0, 0, 0)
                background "#244a9a"
            frame:
                xpos int(size * 0.34)
                ypos int(size * 0.70)
                xysize (int(size * 0.32), int(size * 0.12))
                padding (0, 0, 0, 0)
                background "#b0aca4"
            frame:
                xpos int(size * 0.22)
                ypos int(size * 0.82)
                xysize (int(size * 0.56), int(size * 0.10))
                padding (0, 0, 0, 0)
                background "#d4d0c8"
        elif kind == "msn":
            frame:
                xpos int(size * 0.16)
                ypos int(size * 0.10)
                xysize (int(size * 0.30), int(size * 0.30))
                padding (0, 0, 0, 0)
                background "#58a6ff"
            frame:
                xpos int(size * 0.43)
                ypos int(size * 0.18)
                xysize (int(size * 0.28), int(size * 0.28))
                padding (0, 0, 0, 0)
                background "#69c56b"
            frame:
                xpos int(size * 0.08)
                ypos int(size * 0.44)
                xysize (int(size * 0.76), int(size * 0.32))
                padding (0, 0, 0, 0)
                background "#7fb8ff"
        elif kind == "bin":
            frame:
                xpos int(size * 0.18)
                ypos int(size * 0.24)
                xysize (int(size * 0.64), int(size * 0.60))
                padding (0, 0, 0, 0)
                background "#b8d6e6"
            frame:
                xpos int(size * 0.14)
                ypos int(size * 0.14)
                xysize (int(size * 0.72), int(size * 0.10))
                padding (0, 0, 0, 0)
                background "#d7edf7"
            text "bin":
                color "#335566"
                bold True
                size int(size * 0.22)
                xalign 0.5
                yalign 0.56
        else:
            frame:
                xysize (int(size * 0.82), size)
                xpos int(size * 0.09)
                padding (0, 0, 0, 0)
                background ("#f0e85a" if blink else "#ffffff")
                if blink:
                    at hw2_blink
                frame:
                    xysize (int(size * 0.82), int(size * 0.16))
                    ypos 0
                    padding (0, 0, 0, 0)
                    background ("#c9a800" if blink else "#3a6ea5")
                text glyph:
                    color ("#7a5c00" if blink else "#3a6ea5")
                    bold True
                    size int(size * 0.22)
                    xalign 0.5
                    yalign 0.52

# =============================================================================
#  CHROME:  taskbar + Start menu + generic window + message box
# =============================================================================

# --- XP taskbar (Start button opens the Start menu) ---------------------------
# The clock is LIVE now: it creeps from 8:03 PM toward past-midnight as pressure
# piles up (hw_clock_text). Nobody comments on it; it's just later every time
# you look. `task` shows the active window as a pressed XP task button.
screen hw2_taskbar(clock=None, task=""):
    style_prefix "hw"
    $ _hw_clk = clock or hw_clock_text()
    frame:
        xalign 0.5
        yalign 1.0
        xysize (1280, 30)
        padding (0, 0, 0, 0)
        background "#245edb"
        fixed:
            button:
                xpos 0
                yalign 0.5
                background ("#4aa525" if hw_start_open else "#3c8b1e")
                hover_background "#4aa525"
                padding (14, 4, 20, 4)
                action SetVariable("hw_start_open", not hw_start_open)
                text "start":
                    color "#ffffff"
                    bold True
                    italic True
                    size 15
                    yalign 0.5
            if task:
                frame:
                    xpos 86
                    yalign 0.5
                    ysize 24
                    background "#1e54c8"
                    padding (8, 3, 12, 3)
                    hbox:
                        spacing 6
                        yalign 0.5
                        frame:
                            xysize (13, 13)
                            padding (0, 0, 0, 0)
                            background "#5a8ae8"
                            yalign 0.5
                        text task:
                            color "#ffffff"
                            size 11
                            yalign 0.5
            # system tray: MSN + speaker blips, then the (creeping) clock
            frame:
                xalign 1.0
                yalign 0.5
                ysize 30
                background "#1349b0"
                padding (10, 5, 12, 5)
                hbox:
                    spacing 7
                    yalign 0.5
                    frame:
                        xysize (11, 11)
                        padding (0, 0, 0, 0)
                        background "#69c56b"
                        yalign 0.5
                    frame:
                        xysize (11, 11)
                        padding (0, 0, 0, 0)
                        background "#b8d6e6"
                        yalign 0.5
                    text _hw_clk:
                        color "#ffffff"
                        size 12
                        yalign 0.5
    if hw_start_open:
        use hw2_startmenu()

# --- Start menu (the way to log off) -----------------------------------------
screen hw2_startmenu():
    style_prefix "hw"
    # full-screen catcher: a click anywhere outside closes the menu
    button:
        xfill True
        yfill True
        background None
        action SetVariable("hw_start_open", False)
    frame:
        xpos 0
        yalign 1.0
        yoffset -30
        xsize 256
        padding (0, 0, 0, 0)
        background "#0a246a"
        vbox:
            spacing 0
            # header strip
            frame:
                xsize 256
                ysize 48
                padding (0, 0, 0, 0)
                background "#1657c8"
                hbox:
                    xpos 12
                    yalign 0.5
                    spacing 10
                    frame:
                        xysize (32, 32)
                        background "#c20060"
                        yalign 0.5
                        text "H":
                            color "#ffff99"
                            bold True
                            size 20
                            xalign 0.5
                            yalign 0.5
                    text "Hina":
                        color "#ffffff"
                        bold True
                        size 18
                        yalign 0.5
            # program list / recent places on the family computer
            frame:
                xsize 256
                padding (0, 6, 0, 6)
                background "#ffffff"
                vbox:
                    spacing 0
                    for _kind, _ic, _lbl, _sub, _act in [
                            ("folder", "doc", "My Documents", "shared folder", "snoop:my_documents"),
                            ("folder", "img", "My Pictures", "family photos", "snoop:family_photos"),
                            ("msn", "msn", "MSN Messenger", "remembered", "snoop:msn"),
                            ("app", "e", "Internet", "history", "snoop:internet_history"),
                            ("bin", "bin", "Recycle Bin", "3 items", "snoop:recycle_bin"),
                            ("doc", "?", "Help and Support", "no answer", "snoopfile:help_support"),
                        ]:
                        button:
                            xsize 256
                            background None
                            hover_background "#d8e6ff"
                            padding (12, 6, 12, 6)
                            action [SetVariable("hw_start_open", False), Return(_act)]
                            hbox:
                                spacing 10
                                yalign 0.5
                                use hw2_icon(_kind, _ic, 24, False)
                                vbox:
                                    spacing 0
                                    text _lbl:
                                        color "#202020"
                                        size 14
                                    text _sub:
                                        color "#9a9a9a"
                                        size 10
            # log-off bar
            frame:
                xsize 256
                padding (8, 8, 8, 10)
                background "#d6e4f5"
                vbox:
                    spacing 4
                    button:
                        xsize 240
                        background None
                        hover_background "#bcd4f0"
                        padding (10, 7, 10, 7)
                        hover_sound gui.hover_sound
                        activate_sound gui.activate_sound
                        action [SetVariable("hw_start_open", False), Return("logoff")]
                        hbox:
                            spacing 10
                            yalign 0.5
                            frame:
                                xysize (24, 24)
                                background "#e0a000"
                                yalign 0.5
                                text u"↺":
                                    color "#ffffff"
                                    bold True
                                    size 15
                                    xalign 0.5
                                    yalign 0.5
                            text "Log Off Hina...":
                                color "#0a246a"
                                bold True
                                size 14
                                yalign 0.5
                    button:
                        xsize 240
                        background None
                        hover_background "#bcd4f0"
                        padding (10, 7, 10, 7)
                        hover_sound gui.hover_sound
                        activate_sound gui.activate_sound
                        action [SetVariable("hw_start_open", False), Return("logoff")]
                        hbox:
                            spacing 10
                            yalign 0.5
                            frame:
                                xysize (24, 24)
                                background "#c00000"
                                yalign 0.5
                                text u"⊙":
                                    color "#ffffff"
                                    bold True
                                    size 14
                                    xalign 0.5
                                    yalign 0.5
                            text "Turn Off Computer":
                                color "#0a246a"
                                bold True
                                size 14
                                yalign 0.5

# --- Generic Windows 9x/XP program window with a transcluded client area -----
screen hw2_window(title="", icon="e", titlebg="#0a246a", clientbg="#c0c0c0", w=920, h=636, close_value=None):
    style_prefix "hw"
    # drop shadow
    frame:
        xalign 0.5
        yalign 0.46
        xoffset 4
        yoffset 5
        xysize (w, h)
        padding (0, 0, 0, 0)
        background "#202020"
    # window body
    frame:
        xalign 0.5
        yalign 0.46
        xysize (w, h)
        padding (0, 0, 0, 0)
        background "#d4d0c8"
        vbox:
            spacing 0
            # title bar
            frame:
                xsize w
                ysize 26
                padding (0, 0, 0, 0)
                background titlebg
                fixed:
                    hbox:
                        xpos 4
                        yalign 0.5
                        spacing 4
                        frame:
                            xysize (18, 18)
                            background "#1e4fd4"
                            padding (0, 0, 0, 0)
                            yalign 0.5
                            text icon:
                                color "#ffffff"
                                bold True
                                size 13
                                xalign 0.5
                                yalign 0.5
                        text title:
                            color "#ffffff"
                            bold True
                            size 11
                            yalign 0.5
                    hbox:
                        xalign 1.0
                        xoffset -3
                        yalign 0.5
                        spacing 2
                        # minimize / maximize -- decorative, same as the IE
                        # window (nobody minimizes anything on this machine)
                        frame:
                            xysize (17, 15)
                            padding (0, 0, 0, 0)
                            background "#c0c0c0"
                            yalign 0.5
                            text "_":
                                color "#000000"
                                size 12
                                bold True
                                xalign 0.5
                                yalign 0.5
                        frame:
                            xysize (17, 15)
                            padding (0, 0, 0, 0)
                            background "#c0c0c0"
                            yalign 0.5
                            frame:
                                xysize (9, 8)
                                padding (0, 0, 0, 0)
                                background "#000000"
                                xalign 0.5
                                yalign 0.5
                                frame:
                                    xysize (7, 6)
                                    padding (0, 0, 0, 0)
                                    background "#c0c0c0"
                                    xalign 0.5
                                    yalign 1.0
                        if close_value is not None:
                            button:
                                yalign 0.5
                                xysize (17, 15)
                                padding (0, 0, 0, 0)
                                background "#c00000"
                                hover_background "#ff3b3b"
                                hover_sound gui.hover_sound
                                action Return(close_value)
                                text "X":
                                    color "#ffffff"
                                    bold True
                                    size 10
                                    xalign 0.5
                                    yalign 0.5
                        else:
                            frame:
                                yalign 0.5
                                xysize (17, 15)
                                padding (0, 0, 0, 0)
                                background "#c00000"
                                text "X":
                                    color "#ffffff"
                                    bold True
                                    size 10
                                    xalign 0.5
                                    yalign 0.5
            # client area (story content goes here)
            frame:
                xysize (w, h - 26)
                padding (0, 0, 0, 0)
                background clientbg
                transclude

# --- Windows message box -----------------------------------------------------
#   icon: "i" info / "!" warning / "x" error.  buttons: [(label, returnvalue), ...]
screen hw2_msgbox(title="Hina's World", message="", icon="i", buttons=[("OK", "ok")]):
    style_prefix "hw"
    modal True
    zorder 60
    key "K_RETURN" action Return(buttons[0][1])
    # ESC / title-bar X dismiss like Windows: same as the first (safe) button.
    key "K_ESCAPE" action Return(buttons[0][1])
    add Solid("#00000055")
    frame:
        xalign 0.5
        yalign 0.45
        xsize 400
        padding (0, 0, 0, 0)
        background "#d4d0c8"
        vbox:
            spacing 0
            frame:
                xsize 400
                ysize 24
                padding (0, 0, 0, 0)
                background "#0a246a"
                fixed:
                    text title:
                        color "#ffffff"
                        bold True
                        size 11
                        xpos 6
                        yalign 0.5
                    button:
                        xalign 1.0
                        xoffset -4
                        yalign 0.5
                        xysize (17, 15)
                        padding (0, 0, 0, 0)
                        background "#c00000"
                        hover_background "#ff3b3b"
                        hover_sound gui.hover_sound
                        action Return(buttons[0][1])
                        text "X":
                            color "#ffffff"
                            bold True
                            size 10
                            xalign 0.5
                            yalign 0.5
            frame:
                xsize 400
                padding (16, 16, 16, 12)
                background "#d4d0c8"
                hbox:
                    spacing 14
                    $ _ic_bg = "#c00000" if icon == "x" else ("#d4a800" if icon == "!" else "#1e6fd4")
                    $ _ic_ch = "X" if icon == "x" else ("!" if icon == "!" else "i")
                    frame:
                        xysize (32, 32)
                        background _ic_bg
                        yalign 0.0
                        text _ic_ch:
                            color "#ffffff"
                            bold True
                            size 20
                            xalign 0.5
                            yalign 0.5
                    text message:
                        color "#000000"
                        size 12
                        xsize 322
            frame:
                xsize 400
                padding (0, 4, 10, 10)
                background "#d4d0c8"
                hbox:
                    xalign 1.0
                    spacing 8
                    for _blabel, _bval in buttons:
                        button:
                            background "#ece9d8"
                            hover_background "#c2d8f0"
                            padding (16, 4, 16, 4)
                            hover_sound gui.hover_sound
                            activate_sound gui.activate_sound
                            action Return(_bval)
                            text _blabel:
                                color "#000000"
                                size 12
                                xalign 0.5

# =============================================================================
#  BOOT FRAME:  desktop -> double-click -> Flash preloader
# =============================================================================

screen hw2_desktop():
    style_prefix "hw"
    modal True
    key "K_ESCAPE" action SetVariable("hw_start_open", not hw_start_open)
    key "game_menu" action SetVariable("hw_start_open", not hw_start_open)
    # The desktop wallpaper stays exactly the same all the way through -- no mood
    # darkening, no badges popping up. Escalation is felt through the files that
    # appear and the site itself, discovered by the player, not announced here.
    use hw2_desktop_backdrop()

    # Desktop icons: family-computer shortcuts plus text-log files for choices.
    # Reading the logs does NOT log you off -- that's the Start menu.
    fixed:
        for _idx, (_act, _label, _kind, _glyph, _blink) in enumerate(hw_desktop_icons()):
            $ _col = _idx // 6
            $ _row = _idx % 6
            $ _x = 24 + (_col * 116)
            $ _y = 22 + (_row * 104)
            button:
                xpos _x
                ypos _y
                xysize (106, 92)
                padding (5, 5, 5, 5)
                background None
                hover_background "#3169c688"
                hover_sound gui.hover_sound
                activate_sound gui.activate_sound
                action (Return(_act) if _act else NullAction())
                vbox:
                    xsize 96
                    spacing 4
                    use hw2_icon(_kind, _glyph, 46, _blink)
                    text _label:
                        color "#ffffff"
                        size 10
                        xsize 96
                        ysize 32
                        xalign 0.5
                        text_align 0.5
                        # XP desktop labels carry a drop shadow so they read on
                        # any wallpaper (hw_text clears outlines; re-add here)
                        outlines [(1, "#000000c0", 1, 1)]
    use hw2_taskbar()

screen hw2_snoop_folder(folder_id="my_computer"):
    style_prefix "hw"
    modal True
    key "K_ESCAPE" action SetVariable("hw_start_open", not hw_start_open)
    key "game_menu" action SetVariable("hw_start_open", not hw_start_open)
    use hw2_desktop_backdrop()
    default current_folder = folder_id
    default back_stack = []
    default forward_stack = []
    $ _folder = hw_snoop_folder(current_folder)
    $ _parent = hw_snoop_parent(current_folder)

    use hw2_window(title=_folder["title"] + " - Windows Explorer", icon="PC", titlebg="#0a246a", clientbg="#ffffff", w=760, h=560, close_value="close"):
        vbox:
            spacing 0
            frame:
                xsize 760
                ysize 36
                background "#d4d0c8"
                padding (8, 4, 8, 4)
                hbox:
                    spacing 5
                    for _label, _enabled, _actions in [
                            ("< Back", bool(back_stack), [
                                Function(hw_add_pressure, "folder_back", 1),
                                SetScreenVariable("forward_stack", forward_stack + [current_folder]),
                                SetScreenVariable("current_folder", back_stack[-1] if back_stack else current_folder),
                                SetScreenVariable("back_stack", back_stack[:-1]),
                            ]),
                            ("Fwd >", bool(forward_stack), [
                                Function(hw_add_pressure, "folder_forward", 1),
                                SetScreenVariable("back_stack", back_stack + [current_folder]),
                                SetScreenVariable("current_folder", forward_stack[-1] if forward_stack else current_folder),
                                SetScreenVariable("forward_stack", forward_stack[:-1]),
                            ]),
                            ("Up", bool(_parent), [
                                Function(hw_add_pressure, "folder_up", 1),
                                SetScreenVariable("back_stack", back_stack + [current_folder]),
                                SetScreenVariable("current_folder", _parent if _parent else current_folder),
                                SetScreenVariable("forward_stack", []),
                            ]),
                        ]:
                        button:
                            background ("#e4e2dc" if _enabled else "#c8c8c8")
                            hover_background "#c2d8f0"
                            padding (7, 3, 7, 3)
                            sensitive _enabled
                            action _actions
                            text _label:
                                color ("#000000" if _enabled else "#777777")
                                size 10
                    frame:
                        xysize (1, 22)
                        padding (0, 0, 0, 0)
                        background "#808080"
                        yalign 0.5
                    text "Address:":
                        color "#000000"
                        size 10
                        yalign 0.5
                    frame:
                        xsize 430
                        ysize 20
                        background "#ffffff"
                        padding (4, 2, 4, 2)
                        text _folder["address"]:
                            color "#000000"
                            size 10
                            yalign 0.5

            hbox:
                spacing 0
                frame:
                    xysize (190, 498)
                    background "#eef3ff"
                    padding (12, 10, 12, 10)
                    vbox:
                        spacing 9
                        text "File and Folder Tasks":
                            color "#244a9a"
                            bold True
                            size 12
                        text "Open a folder":
                            color "#3366aa"
                            size 11
                        text "Read a file":
                            color "#3366aa"
                            size 11
                        text "Pretend you weren't looking":
                            color "#3366aa"
                            size 11
                        null height 8
                        text "Details":
                            color "#244a9a"
                            bold True
                            size 12
                        text "{} object(s)".format(len(_folder["entries"])):
                            color "#404040"
                            size 10
                        text _folder["note"]:
                            color "#404040"
                            size 10
                            xsize 160

                frame:
                    xysize (570, 498)
                    background "#ffffff"
                    padding (10, 10, 10, 10)
                    vpgrid:
                        cols 2
                        spacing 8
                        xysize (550, 478)
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        for _kind, _target, _label, _glyph, _desc in _folder["entries"]:
                            $ _ret = ("snoop:" + _target) if _kind == "folder" else (("img_" + _target) if _kind == "image" else ("snoopfile:" + _target))
                            $ _icon_kind = "folder" if _kind == "folder" else ("image" if _kind == "image" else ("msn" if _glyph == "msn" else ("bin" if _glyph == "bin" else ("app" if _glyph == "e" else "doc"))))
                            $ _nav_action = [Function(hw_add_pressure, "folder", 1), SetScreenVariable("back_stack", back_stack + [current_folder]), SetScreenVariable("current_folder", _target), SetScreenVariable("forward_stack", [])] if _kind == "folder" else [Function(hw_add_pressure, "open_file", 1), SetVariable("hw_snoop_return_folder", current_folder), Return(_ret)]
                            button:
                                xysize (260, 72)
                                background "#ffffff"
                                hover_background "#d8e6ff"
                                padding (8, 6, 8, 6)
                                hover_sound gui.hover_sound
                                activate_sound gui.activate_sound
                                action _nav_action
                                hbox:
                                    spacing 8
                                    use hw2_icon(_icon_kind, _glyph, 36, False)
                                    vbox:
                                        spacing 2
                                        yalign 0.5
                                        text _label:
                                            color "#202020"
                                            bold True
                                            size 11
                                            xsize 198
                                        text _desc:
                                            color "#666666"
                                            size 9
                                            xsize 198

    use hw2_taskbar(task=_folder["title"])

screen hw2_preloader():
    style_prefix "hw"
    modal True
    use hw2_desktop_backdrop()
    default pct = 0
    timer 0.03 repeat True action SetScreenVariable("pct", min(pct + 2, 100))
    timer 2.4 action Return("done")
    # A real IE window with the Flash stage loading inside it -- not a bare
    # floating rectangle. The X works (closing IE mid-load goes back to the
    # desktop and the preloader will play again next time).
    use hw2_window(title="Hina's World - Internet Explorer", icon="e", titlebg="#0a246a", clientbg="#1a1a1a", w=920, h=636, close_value="close"):
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 18
            text u"~*~ Hina's World ~*~":
                color "#ff66cc"
                bold True
                size 40
                xalign 0.5
            frame:
                xysize (384, 22)
                xalign 0.5
                background "#000000"
                padding (2, 2, 2, 2)
                $ _bw = max(1, int(380 * pct / 100))
                add Solid("#ff33aa"):
                    xysize (_bw, 18)
                    xalign 0.0
                    yalign 0.5
            $ _ptxt = "Loading... {}%".format(pct)
            text _ptxt:
                color "#ffffff"
                size 14
                xalign 0.5
            text "Macromedia Flash Player 6":
                color "#9a9a9a"
                size 11
                xalign 0.5
    use hw2_taskbar(task="Hina's World - Internet Explorer")

# =============================================================================
#  MINI-GAME 1:  Hina's Outfitter  (the game keeps nudging her older)
# =============================================================================
screen hw2_outfitter():
    style_prefix "hw"
    modal True
    key "K_ESCAPE" action SetVariable("hw_start_open", not hw_start_open)
    key "game_menu" action SetVariable("hw_start_open", not hw_start_open)
    use hw2_desktop_backdrop()
    default sel = {"Top": None, "Shoes": None, "Extra": None}
    default clicks = 0

    use hw2_window(title="Hina's Outfitter - Hina's World", icon="H", titlebg="#c20060", clientbg="#ffe6f4", w=920, h=636, close_value="cancel"):
        hbox:
            spacing 0
            # --- paper-doll preview (placeholder; no art assets) ---
            frame:
                xysize (360, 610)
                background "#ffd6ec"
                padding (16, 16, 16, 16)
                vbox:
                    xalign 0.5
                    spacing 12
                    text "~ Hina ~":
                        color "#c20060"
                        bold True
                        size 22
                        xalign 0.5
                    frame:
                        xysize (220, 360)
                        xalign 0.5
                        background "#ffb5df"
                        vbox:
                            xalign 0.5
                            yalign 0.5
                            spacing 10
                            $ _top  = sel["Top"][0]   if sel["Top"]   else "(pick a top)"
                            $ _shoe = sel["Shoes"][0] if sel["Shoes"] else "(pick shoes)"
                            $ _hold = sel["Extra"][0] if sel["Extra"] else "(nothing)"
                            text _top:
                                color "#7a1147"
                                bold True
                                size 16
                                xalign 0.5
                            text _shoe:
                                color "#7a1147"
                                size 14
                                xalign 0.5
                            text _hold:
                                color "#9a3a6e"
                                size 13
                                xalign 0.5

            # --- controls ---
            frame:
                xysize (560, 610)
                background "#ffe6f4"
                padding (22, 16, 22, 16)
                vbox:
                    spacing 14
                    text "Dress up Hina!":
                        color "#aa0066"
                        bold True
                        size 20

                    for _slot, _opts in HW2_OUTFITTER_SLOTS:
                        vbox:
                            spacing 4
                            text _slot:
                                color "#aa0066"
                                bold True
                                size 13
                            hbox:
                                spacing 6
                                for _label, _tag in _opts:
                                    $ _on = (sel[_slot] == (_label, _tag))
                                    button:
                                        background ("#ff66cc" if _on else "#ffffff")
                                        hover_background "#ffb3e0"
                                        padding (9, 4, 9, 4)
                                        hover_sound gui.hover_sound
                                        action [SetDict(sel, _slot, (_label, _tag)), SetScreenVariable("clicks", clicks + 1)]
                                        text _label:
                                            color ("#ffffff" if _on else "#aa3377")
                                            size 11

                    null height 6

                    $ _cap = hw2_outfit_caption(sel)
                    text _cap:
                        color "#a32f6e"
                        size 14
                        xsize 500

                    button:
                        background "#c20060"
                        hover_background "#ff3399"
                        padding (24, 8, 24, 8)
                        activate_sound gui.activate_sound
                        action [Function(hw_outfit_commit, sel), Return("done")]
                        text "- Done -":
                            color "#ffffff"
                            bold True
                            size 14
    use hw2_taskbar(task="Hina's Outfitter")

# =============================================================================
#  MINI-GAME 2:  Hina's Chatting  (friends, trolls, a stranger; messages stay)
# =============================================================================
screen hw2_chatting(session=0):
    style_prefix "hw"
    modal True
    key "K_ESCAPE" action SetVariable("hw_start_open", not hw_start_open)
    key "game_menu" action SetVariable("hw_start_open", not hw_start_open)
    use hw2_desktop_backdrop()
    default step = 0
    default choices = {}
    default branches = {}
    default chat_yadj = ui.adjustment()

    $ _script = hw2_chat_script(session)
    $ _n_chat = len(_script)
    $ _empty = (_n_chat == 0)
    $ _is_you = ((not _empty) and step < _n_chat and _script[step][0] == "you")
    $ _at_end = (step >= _n_chat)
    # Every advance slams the transcript adjustment past its range; the viewport
    # clamps it to the true bottom on the next layout. (yinitial/id tricks do
    # NOT reliably re-snap an existing viewport -- this does.)
    $ _hw_adv = [SetScreenVariable("step", step + 1), SetField(chat_yadj, "value", 999999)]
    # Progression is CLICK-driven (not timer-driven): screen timers can fail to
    # re-arm across re-renders, which softlocked the room. Clicking the transcript
    # (or the bar below) advances bot/system lines; player turns wait for a reply.

    use hw2_window(title="Hina's Chatting - hinasworld.net", icon="H", titlebg="#7700cc", clientbg="#f3d9ee", w=920, h=636, close_value="cancel"):
        vbox:
            spacing 0
            # room header  (room name + the date it happened -- days into weeks)
            frame:
                xsize 920
                ysize 40
                background "#aa55e0"
                fixed:
                    $ _room_title = "Room: " + hw2_chat_room(session)
                    $ _room_when = hw2_chat_when(session)
                    $ _room_users = ("Users: " + hw2_chat_users(session)) if (not _empty) else "Users: (none)"
                    vbox:
                        xpos 10
                        yalign 0.5
                        spacing 1
                        text _room_title:
                            color "#ffffff"
                            bold True
                            size 12
                        if _room_when:
                            text _room_when:
                                color "#ecccf8"
                                size 9
                    text _room_users:
                        color "#f7ddff"
                        size 10
                        xalign 1.0
                        xoffset -10
                        yalign 0.5
            # transcript -- newest eight lines. The whole log is a click target on
            # bot turns so the chat can never softlock.
            button:
                xysize (920, 460)
                background "#fff4fb"
                hover_background "#fdeaf6"
                padding (16, 12, 16, 12)
                action (None if (_empty or _is_you or _at_end) else _hw_adv)
                if _empty:
                    vbox:
                        spacing 10
                        yalign 0.5
                        xalign 0.5
                        text u"*** Dialing HinaWeb Chat 2.1 ***":
                            color "#9a7fb0"
                            italic True
                            size 12
                            xalign 0.5
                        text u"Connected to ~*HINA'S FRIENDS*~":
                            color "#9a7fb0"
                            italic True
                            size 12
                            xalign 0.5
                        text u"Nobody else is online.":
                            color "#7700cc"
                            bold True
                            size 18
                            xalign 0.5
                else:
                    # Scrollable full transcript. The viewport id changes with
                    # `step`, so each new line re-snaps the view to the bottom
                    # (yinitial 1.0) while still letting the player wheel back
                    # up to reread anything from earlier in the room.
                    viewport:
                        yadjustment chat_yadj
                        xysize (888, 436)
                        mousewheel True
                        yinitial 1.0
                        vbox:
                            spacing 6
                            yalign 1.0
                            for _who, _kind, _txt in hw2_chat_lines(session, step, choices, branches):
                                if _kind == "system":
                                    text _txt:
                                        color "#9a7fb0"
                                        italic True
                                        size 11
                                        xalign 0.5
                                elif _kind == "you":
                                    hbox:
                                        xalign 1.0
                                        frame:
                                            background "#ff66cc"
                                            padding (10, 5, 10, 5)
                                            xmaximum 540
                                            vbox:
                                                spacing 1
                                                text _who:
                                                    color "#ffe6f4"
                                                    bold True
                                                    size 9
                                                text _txt:
                                                    color "#ffffff"
                                                    size 13
                                else:
                                    # friend / troll / creep -- coloured by who it is
                                    $ _nm_col = {"friend": "#cc3399", "troll": "#b00000", "creep": "#7a5c00"}.get(_kind, "#cc3399")
                                    $ _bub = {"friend": "#ffffff", "troll": "#fff0f0", "creep": "#fff7e0"}.get(_kind, "#ffffff")
                                    $ _tx_col = {"friend": "#8a2a63", "troll": "#7a2a2a", "creep": "#5a4500"}.get(_kind, "#8a2a63")
                                    $ _tag = " (guest)" if _kind == "creep" else ""
                                    hbox:
                                        xalign 0.0
                                        frame:
                                            background _bub
                                            padding (10, 5, 10, 5)
                                            xmaximum 540
                                            vbox:
                                                spacing 1
                                                text (_who + _tag):
                                                    color _nm_col
                                                    bold True
                                                    size 9
                                                text _txt:
                                                    color _tx_col
                                                    size 13
            # reply / continue bar
            frame:
                xysize (920, 110)
                background "#ead3e6"
                padding (16, 8, 16, 8)
                if _empty:
                    button:
                        xalign 0.5
                        yalign 0.5
                        background "#7700cc"
                        hover_background "#9933dd"
                        padding (24, 8, 24, 8)
                        hover_sound gui.hover_sound
                        activate_sound gui.activate_sound
                        action Return("empty")
                        text "Close window":
                            color "#ffffff"
                            bold True
                            size 14
                elif _is_you:
                    vbox:
                        spacing 5
                        text "Reply as Hina:":
                            color "#7700cc"
                            bold True
                            size 11
                        hbox:
                            spacing 8
                            for _choice in _script[step][2]:
                                $ _opt, _w, _branch = hw2_chat_choice_parts(_choice)
                                button:
                                    background "#ffffff"
                                    hover_background "#ffd0ee"
                                    padding (10, 6, 10, 6)
                                    xmaximum 290
                                    hover_sound gui.hover_sound
                                    action ([SetDict(choices, step, _opt), SetDict(branches, step, _branch), Function(hw_apply, _w)] + _hw_adv)
                                    text _opt:
                                        color "#aa3377"
                                        size 12
                elif _at_end:
                    button:
                        xalign 0.5
                        yalign 0.5
                        background "#7700cc"
                        hover_background "#9933dd"
                        padding (24, 8, 24, 8)
                        hover_sound gui.hover_sound
                        activate_sound gui.activate_sound
                        action Return("done")
                        text "Close window":
                            color "#ffffff"
                            bold True
                            size 14
                else:
                    button:
                        xfill True
                        yfill True
                        background None
                        action _hw_adv
                        text u"▼  click to continue":
                            color "#8a5fa0"
                            size 14
                            xalign 0.5
                            yalign 0.5
    use hw2_taskbar(task="Hina's Chatting")

# =============================================================================
#  MINI-GAME 3:  Hina's Quiz Corner  (it stops asking and starts deciding)
# =============================================================================
screen hw2_quiz():
    style_prefix "hw"
    modal True
    key "K_ESCAPE" action SetVariable("hw_start_open", not hw_start_open)
    key "game_menu" action SetVariable("hw_start_open", not hw_start_open)
    use hw2_desktop_backdrop()
    default qi = 0
    default answers = {}

    $ _n_q = len(HW2_QUIZ)
    use hw2_window(title="Hina's Quiz Corner - Hina's World", icon="H", titlebg="#0066aa", clientbg="#dff0ff", w=920, h=636, close_value="cancel"):
        vbox:
            xalign 0.5
            yalign 0.5
            xsize 780
            spacing 22
            if qi < _n_q:
                $ _qn = qi + 1
                $ _hdr = "Question {} of {}".format(_qn, _n_q)
                $ _q, _opts = HW2_QUIZ[qi]
                text _hdr:
                    color "#0066aa"
                    bold True
                    size 14
                    xalign 0.5
                text _q:
                    color "#004a7a"
                    bold True
                    size 24
                    xalign 0.5
                    text_align 0.5
                vbox:
                    xalign 0.5
                    spacing 10
                    for _opt, _tag in _opts:
                        button:
                            xsize 460
                            background "#ffffff"
                            hover_background "#bfe4ff"
                            padding (16, 9, 16, 9)
                            hover_sound gui.hover_sound
                            activate_sound gui.activate_sound
                            action [SetDict(answers, qi, _tag), SetScreenVariable("qi", qi + 1)]
                            text _opt:
                                color "#0066aa"
                                size 15
                                xalign 0.5
            else:
                # an innocent-looking magazine result; the weight lands later in
                # quiz.txt on the desktop, not here
                $ _grown = sum(1 for t in answers.values() if t in ("grow", "guest"))
                $ _res = (u"OLD SOUL" if _grown >= 4 else (u"COOL FOR YOUR AGE" if _grown >= 2 else u"SWEET & SILLY"))
                text "your result!":
                    color "#004a7a"
                    bold True
                    size 18
                    xalign 0.5
                frame:
                    xsize 560
                    xalign 0.5
                    background "#ffffff"
                    padding (22, 20, 22, 20)
                    vbox:
                        spacing 10
                        text (u"You're:  " + _res + u"  ♥"):
                            color "#0066aa"
                            bold True
                            size 22
                            xalign 0.5
                        text (u"Mature, cool, ahead of the curve!" if _grown >= 2 else u"You're just a kid, and that's okay!"):
                            color "#004a7a"
                            size 13
                            xalign 0.5
                        text u"result posted to your public profile.":
                            color "#7a93a3"
                            italic True
                            size 11
                            xalign 0.5
                button:
                    xalign 0.5
                    background "#0066aa"
                    hover_background "#0088cc"
                    padding (24, 8, 24, 8)
                    activate_sound gui.activate_sound
                    action [Function(hw_quiz_commit, answers), Return("done")]
                    text "Continue":
                        color "#ffffff"
                        bold True
                        size 14
    use hw2_taskbar(task="Hina's Quiz Corner")

# =============================================================================
#  MINI-GAME 4:  Hina's Rating Game  (you are made to grade her)
# =============================================================================
screen hw2_rating():
    style_prefix "hw"
    modal True
    key "K_ESCAPE" action SetVariable("hw_start_open", not hw_start_open)
    key "game_menu" action SetVariable("hw_start_open", not hw_start_open)
    use hw2_desktop_backdrop()
    default scores = {}
    default submitted = False

    $ _n_rows = len(HW2_RATING_ROWS)
    use hw2_window(title="Hina's Rating Game - Hina's World", icon="H", titlebg="#bb5500", clientbg="#fff0e0", w=920, h=636, close_value=("done" if submitted else "cancel")):
        vbox:
            xalign 0.5
            yalign 0.5
            xsize 740
            spacing 16
            if not submitted:
                text u"Rate Hina's new look! ☆":
                    color "#bb5500"
                    bold True
                    size 22
                    xalign 0.5
            else:
                text u"Thanks for rating Hina! ♥":
                    color "#bb5500"
                    bold True
                    size 22
                    xalign 0.5

            for _idx, _label in enumerate(HW2_RATING_ROWS):
                hbox:
                    spacing 14
                    yalign 0.5
                    text _label:
                        color "#995500"
                        bold True
                        size 16
                        xsize 320
                        yalign 0.5
                    for _n in range(1, 6):
                        $ _ssel = (scores.get(_idx) == _n)
                        button:
                            xysize (40, 36)
                            background ("#bb5500" if _ssel else "#ffffff")
                            hover_background "#ffcc99"
                            sensitive (not submitted)
                            hover_sound gui.hover_sound
                            action SetDict(scores, _idx, _n)
                            text str(_n):
                                color ("#ffffff" if _ssel else "#995500")
                                bold True
                                size 16
                                xalign 0.5
                                yalign 0.5

            if not submitted:
                $ _ready = (len(scores) == _n_rows)
                button:
                    xalign 0.5
                    background ("#bb5500" if _ready else "#d8c0a8")
                    hover_background "#ff8800"
                    padding (24, 8, 24, 8)
                    sensitive _ready
                    activate_sound gui.activate_sound
                    action [Function(hw_rating_commit, scores), SetScreenVariable("submitted", True)]
                    text "Submit":
                        color "#ffffff"
                        bold True
                        size 15
            else:
                text u"Hina can see how you scored her.":
                    color "#995500"
                    size 13
                    xalign 0.5
                    text_align 0.5
                button:
                    xalign 0.5
                    background "#bb5500"
                    hover_background "#ff8800"
                    padding (24, 8, 24, 8)
                    activate_sound gui.activate_sound
                    action Return("done")
                    text "Continue":
                        color "#ffffff"
                        bold True
                        size 14
    use hw2_taskbar(task="Hina's Rating Game")

# =============================================================================
#  MINI-GAME 5:  Hina's Lunchbox Break  (the food thread, playable)
# =============================================================================
screen hw2_bento():
    style_prefix "hw"
    modal True
    key "K_ESCAPE" action SetVariable("hw_start_open", not hw_start_open)
    key "game_menu" action SetVariable("hw_start_open", not hw_start_open)
    use hw2_desktop_backdrop()
    default bsel = {"Main": None, "Side": None, "Sweet": None, "Drink": None}

    use hw2_window(title="Hina's Lunchbox Break - Hina's World", icon="H", titlebg="#2e8b2e", clientbg="#eaffe0", w=920, h=636, close_value="cancel"):
        hbox:
            spacing 0
            # --- lunchbox preview (placeholder; no art assets) ---
            frame:
                xysize (360, 610)
                background "#d8f5c8"
                padding (16, 16, 16, 16)
                vbox:
                    xalign 0.5
                    spacing 12
                    text "~ Today's Lunch ~":
                        color "#2e7a1e"
                        bold True
                        size 22
                        xalign 0.5
                    frame:
                        xysize (240, 320)
                        xalign 0.5
                        background "#bfe8a8"
                        vbox:
                            xalign 0.5
                            yalign 0.5
                            spacing 16
                            for _bslot in ["Main", "Side", "Sweet", "Drink"]:
                                $ _bpick = bsel[_bslot][0] if bsel[_bslot] else "(empty)"
                                text _bpick:
                                    color ("#2e5a1e" if bsel[_bslot] else "#7a9a6a")
                                    bold (bsel[_bslot] is not None)
                                    size 15
                                    xalign 0.5
                    text "school + practice day":
                        color "#5a8a4a"
                        size 11
                        xalign 0.5

            # --- controls ---
            frame:
                xysize (560, 610)
                background "#eaffe0"
                padding (22, 16, 22, 16)
                vbox:
                    spacing 14
                    text "Pack Hina's lunch!":
                        color "#2e7a1e"
                        bold True
                        size 20

                    for _slot, _opts in HW2_BENTO_SLOTS:
                        vbox:
                            spacing 4
                            text _slot:
                                color "#2e7a1e"
                                bold True
                                size 13
                            hbox:
                                spacing 6
                                for _label, _tag in _opts:
                                    $ _on = (bsel[_slot] == (_label, _tag))
                                    button:
                                        background ("#4aa544" if _on else "#ffffff")
                                        hover_background "#c8eab0"
                                        padding (9, 4, 9, 4)
                                        hover_sound gui.hover_sound
                                        action SetDict(bsel, _slot, (_label, _tag))
                                        text _label:
                                            color ("#ffffff" if _on else "#3a7a2e")
                                            size 11

                    null height 6

                    $ _bcap = hw2_bento_caption(bsel)
                    text _bcap:
                        color "#3a7a2e"
                        size 14
                        xsize 500

                    button:
                        background "#2e8b2e"
                        hover_background "#4aa544"
                        padding (24, 8, 24, 8)
                        activate_sound gui.activate_sound
                        action [Function(hw_bento_commit, bsel), Return("done")]
                        text "- Pack it! -":
                            color "#ffffff"
                            bold True
                            size 14
    use hw2_taskbar(task="Hina's Lunchbox Break")

# =============================================================================
#  MINI-GAME 6:  Mr Toast & Mochi  (the one game with nothing wrong in it)
# =============================================================================
screen hw2_petsalon():
    style_prefix "hw"
    modal True
    key "K_ESCAPE" action SetVariable("hw_start_open", not hw_start_open)
    key "game_menu" action SetVariable("hw_start_open", not hw_start_open)
    use hw2_desktop_backdrop()
    default care_toast = 0
    default care_mochi = 0
    default decision = None

    $ _care = care_toast + care_mochi
    $ _fork = (_care >= 6 and decision is None)
    $ _pline = (HW2_PET_LINES[(_care - 1) % len(HW2_PET_LINES)] if _care > 0 else u"mr toast and mochi are waiting!")

    use hw2_window(title="Mr Toast & Mochi - Hina's World", icon="H", titlebg="#a07a00", clientbg="#fff6d8", w=920, h=636, close_value="cancel"):
        fixed:
            vbox:
                xalign 0.5
                ypos 18
                spacing 14
                text u"Give them the royal treatment! ☆":
                    color "#8a6a00"
                    bold True
                    size 22
                    xalign 0.5

                hbox:
                    xalign 0.5
                    spacing 24
                    for _pet, _count, _var, _pbg in [("MR TOAST", care_toast, "care_toast", "#ffe9b0"), ("MOCHI", care_mochi, "care_mochi", "#f5ddb8")]:
                        frame:
                            xysize (390, 380)
                            background "#fffbe8"
                            padding (14, 12, 14, 12)
                            vbox:
                                spacing 10
                                xalign 0.5
                                text _pet:
                                    color "#8a6a00"
                                    bold True
                                    size 16
                                    xalign 0.5
                                frame:
                                    xysize (340, 190)
                                    xalign 0.5
                                    background _pbg
                                    text ("the bunny" if _pet == "MR TOAST" else "the cat"):
                                        color "#9a7a30"
                                        bold True
                                        size 15
                                        xalign 0.5
                                        yalign 0.5
                                # fluff meter
                                frame:
                                    xysize (340, 16)
                                    xalign 0.5
                                    background "#e8d8a8"
                                    padding (2, 2, 2, 2)
                                    add Solid("#e0a838"):
                                        xysize (max(1, int(336 * min(_count, 5) / 5.0)), 12)
                                        xalign 0.0
                                        yalign 0.5
                                hbox:
                                    xalign 0.5
                                    spacing 8
                                    for _act in ["Brush", "Snack", "Play"]:
                                        button:
                                            background "#ffffff"
                                            hover_background "#ffe9b0"
                                            padding (14, 5, 14, 5)
                                            sensitive (not _fork)
                                            hover_sound gui.hover_sound
                                            activate_sound gui.activate_sound
                                            action SetScreenVariable(_var, _count + 1)
                                            text _act:
                                                color "#8a6a00"
                                                bold True
                                                size 12

                text _pline:
                    color "#9a7a30"
                    size 14
                    xalign 0.5

                if decision == "kept":
                    text u"mochi purrs at max volume. mr toast approves.":
                        color "#8a6a00"
                        bold True
                        size 13
                        xalign 0.5
                    button:
                        xalign 0.5
                        background "#a07a00"
                        hover_background "#c89a20"
                        padding (24, 8, 24, 8)
                        activate_sound gui.activate_sound
                        action [Function(hw_pet_commit, "kept"), Return("done")]
                        text "- Done -":
                            color "#ffffff"
                            bold True
                            size 14
                elif not _fork:
                    text u"(brush them a while. there's no score in this one.)":
                        color "#bfa060"
                        italic True
                        size 11
                        xalign 0.5

            # --- the fork: someone can see what she's playing -------------------
            if _fork:
                button:
                    xfill True
                    yfill True
                    background "#00000033"
                    action NullAction()
                frame:
                    xalign 0.5
                    yalign 0.42
                    xsize 380
                    padding (0, 0, 0, 0)
                    background "#d4d0c8"
                    vbox:
                        spacing 0
                        frame:
                            xsize 380
                            ysize 24
                            padding (6, 4, 6, 4)
                            background "#0a246a"
                            text "HinaWeb Messenger":
                                color "#ffffff"
                                size 11
                                yalign 0.5
                        frame:
                            xsize 380
                            padding (16, 14, 16, 12)
                            background "#ffffff"
                            vbox:
                                spacing 8
                                text u"Emily_x0x just signed on.":
                                    color "#000000"
                                    bold True
                                    size 13
                                text u"she can see what game you're playing.":
                                    color "#404040"
                                    size 12
                        frame:
                            xsize 380
                            padding (10, 8, 10, 10)
                            background "#d4d0c8"
                            hbox:
                                xalign 0.5
                                spacing 12
                                button:
                                    background "#ece9d8"
                                    hover_background "#ffe9b0"
                                    padding (14, 5, 14, 5)
                                    hover_sound gui.hover_sound
                                    activate_sound gui.activate_sound
                                    action SetScreenVariable("decision", "kept")
                                    text u"keep playing ♥":
                                        color "#000000"
                                        size 12
                                button:
                                    background "#ece9d8"
                                    hover_background "#c2d8f0"
                                    padding (14, 5, 14, 5)
                                    hover_sound gui.hover_sound
                                    activate_sound gui.activate_sound
                                    action [Function(hw_pet_commit, "hid"), Return("done")]
                                    text u"close it, quick":
                                        color "#000000"
                                        size 12
    use hw2_taskbar(task="Mr Toast & Mochi")

# =============================================================================
#  MINI-GAME 7:  Hina's Makeover Mirror  (the mirror guesses her age; the UI
#  celebrates harder the higher the number goes. Staying little gets no stars.)
# =============================================================================
screen hw2_makeover():
    style_prefix "hw"
    modal True
    key "K_ESCAPE" action SetVariable("hw_start_open", not hw_start_open)
    key "game_menu" action SetVariable("hw_start_open", not hw_start_open)
    use hw2_desktop_backdrop()
    default msel = {"Hair": None, "Face": None, "Nails": None}
    default revealed = False

    use hw2_window(title="Hina's Makeover Mirror - Hina's World", icon="H", titlebg="#0e7a70", clientbg="#e0f7f4", w=920, h=636, close_value=("done" if revealed else "cancel")):
        vbox:
            xalign 0.5
            yalign 0.5
            xsize 760
            spacing 20
            if not revealed:
                text u"~ The Magic Mirror ~":
                    color "#0e6a60"
                    bold True
                    size 24
                    xalign 0.5
                text u"give Hina a new look, then ask the mirror what it sees!":
                    color "#2e8a80"
                    size 13
                    xalign 0.5

                for _slot, _opts in HW2_MAKEOVER_ROWS:
                    vbox:
                        spacing 4
                        xalign 0.5
                        text _slot:
                            color "#0e6a60"
                            bold True
                            size 13
                            xalign 0.5
                        hbox:
                            xalign 0.5
                            spacing 6
                            for _label, _tag in _opts:
                                $ _on = (msel[_slot] == (_label, _tag))
                                button:
                                    background ("#18a898" if _on else "#ffffff")
                                    hover_background "#b8e8e0"
                                    padding (11, 5, 11, 5)
                                    hover_sound gui.hover_sound
                                    action SetDict(msel, _slot, (_label, _tag))
                                    text _label:
                                        color ("#ffffff" if _on else "#0e7a70")
                                        size 12

                $ _mready = all(msel.values())
                button:
                    xalign 0.5
                    background ("#0e7a70" if _mready else "#a8c8c0")
                    hover_background "#18a898"
                    padding (24, 8, 24, 8)
                    sensitive _mready
                    activate_sound gui.activate_sound
                    action [Function(hw_makeover_commit, msel), SetScreenVariable("revealed", True)]
                    text "Look in the mirror!":
                        color "#ffffff"
                        bold True
                        size 14
            else:
                $ _mguess = hw_makeover_guess
                text u"the mirror says...":
                    color "#0e6a60"
                    bold True
                    size 18
                    xalign 0.5
                frame:
                    xsize 460
                    xalign 0.5
                    background "#ffffff"
                    padding (22, 24, 22, 24)
                    vbox:
                        spacing 12
                        text u"you look {}!".format(_mguess):
                            color "#0e7a70"
                            bold True
                            size 34
                            xalign 0.5
                        if _mguess >= 12:
                            text u"☆ ☆ ☆  WOW!  ☆ ☆ ☆":
                                color "#c8a000"
                                bold True
                                size 20
                                xalign 0.5
                                at hw2_blink
                            text u"so grown up!! everyone's going to notice~":
                                color "#2e8a80"
                                size 13
                                xalign 0.5
                        elif _mguess >= 10:
                            text u"☆  cute AND cool!  ☆":
                                color "#c8a000"
                                bold True
                                size 15
                                xalign 0.5
                        else:
                            text u"aw. cute!":
                                color "#8aa8a0"
                                size 12
                                xalign 0.5
                        text u"result posted to your public profile.":
                            color "#7a9a93"
                            italic True
                            size 11
                            xalign 0.5
                button:
                    xalign 0.5
                    background "#0e7a70"
                    hover_background "#18a898"
                    padding (24, 8, 24, 8)
                    activate_sound gui.activate_sound
                    action Return("done")
                    text "Continue":
                        color "#ffffff"
                        bold True
                        size 14
    use hw2_taskbar(task="Makeover Mirror")

# =============================================================================
#  GALLERY VIEWER  (clickable "photos" -- childhood being overwritten)
# =============================================================================
screen hw2_imageview(slot="Track Meet", corruption=0):
    style_prefix "hw"
    modal True
    zorder 40
    add Solid("#00000066")
    use hw2_window(title=slot + " - Image Viewer", icon="H", titlebg="#0a246a", clientbg="#202020", w=700, h=610):
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 10
            $ _turned = hw_photo_turned(slot)
            frame:
                xysize (620, 250)
                xalign 0.5
                background ("#ffb5df" if not _turned else "#5a3a52")
                $ _cap2 = hw_gallery_caption(slot)
                text _cap2:
                    color ("#7a1147" if not _turned else "#e2b7d2")
                    bold True
                    size 18
                    xalign 0.5
                    yalign 0.5
                    text_align 0.5
            text slot:
                color "#dddddd"
                size 13
                xalign 0.5
            text hw_photo_status(slot):
                color ("#9a9a9a" if not _turned else "#c98aae")
                size 11
                xalign 0.5
            frame:
                xysize (620, 200)
                xalign 0.5
                background "#f4edf3"
                padding (10, 8, 10, 8)
                vbox:
                    spacing 6
                    text "Comments":
                        color "#5a3550"
                        bold True
                        size 12
                    viewport:
                        xysize (600, 158)
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        vbox:
                            spacing 5
                            for _who, _txt, _kind in hw_gallery_comments(slot):
                                $ _name_col = {"friend": "#a020c0", "troll": "#b00000", "creep": "#7a5c00", "system": "#777777"}.get(_kind, "#a020c0")
                                $ _bg = {"friend": "#ffffff", "troll": "#fff0f0", "creep": "#fff7e0", "system": "#eeeeee"}.get(_kind, "#ffffff")
                                frame:
                                    xsize 580
                                    background _bg
                                    padding (8, 5, 8, 5)
                                    hbox:
                                        spacing 8
                                        text _who + ":":
                                            color _name_col
                                            bold True
                                            size 10
                                            xsize 92
                                        text _txt:
                                            color "#4a3344"
                                            size 11
                                            xsize 456
            button:
                xalign 0.5
                background "#3a3a3a"
                hover_background "#555555"
                padding (24, 8, 24, 8)
                activate_sound gui.activate_sound
                action Return("close")
                text "Close":
                    color "#ffffff"
                    size 13

# =============================================================================
#  ENDING ARTIFACTS:  Notepad
# =============================================================================
# Notepad rides the shared hw2_window chrome now (one title-bar implementation
# to rule them all -- the old hand-rolled copy had a dead, hover-less X).
screen hw2_notepad(title="Notepad", body=""):
    style_prefix "hw"
    modal True
    zorder 50
    key "K_ESCAPE" action Return("close")
    use hw2_desktop_backdrop()
    use hw2_window(title=title, icon="N", titlebg="#0a246a", clientbg="#d4d0c8", w=640, h=470, close_value="close"):
        vbox:
            spacing 0
            frame:
                xsize 640
                ysize 18
                background "#d4d0c8"
                padding (6, 2, 0, 0)
                hbox:
                    spacing 14
                    for _m in ["File", "Edit", "Format", "View", "Help"]:
                        text _m:
                            color "#000000"
                            size 11
            frame:
                xysize (640, 426)
                background "#ffffff"
                padding (10, 8, 10, 8)
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    xfill True
                    yfill True
                    text body:
                        color "#000000"
                        size 14
                        substitute False
    use hw2_taskbar(task=title)

# --- Windows 9x "safe to turn off" shutdown screen (one word is wrong) --------
# --- The cliffhanger: the real world arrives. Only if every beat was hit, an
#     IRC message from Mom catches her on the way out -- the offline consequence
#     of the whole online thing. Click-driven; no choice; she has to go down.
screen hw2_mom_message():
    style_prefix "hw"
    modal True
    add Solid("#000000")
    default step = 0
    $ _mom_lines = [
        u"Asahina.",
        u"Come to the living room. Right now.",
        u"Your brother showed me those chat rooms and the messages.",
        u"That man. How long has he been writing to you?",
        u"Don't you dare delete anything before we look at the site or so help me God.",
        u"We are dealing with all of it. Tonight.",
        u"NOW, Asahina! Off the damn computer and down here!",
    ]
    $ _mom_shown = min(step, len(_mom_lines))
    $ _mom_done = step >= len(_mom_lines)
    # drop shadow
    frame:
        xalign 0.5
        yalign 0.5
        xoffset 4
        yoffset 5
        xysize (540, 360)
        background "#202020"
        padding (0, 0, 0, 0)
    frame:
        xalign 0.5
        yalign 0.5
        xysize (540, 360)
        background "#d4d0c8"
        padding (0, 0, 0, 0)
        vbox:
            spacing 0
            # title bar -- urgent red
            frame:
                xsize 540
                ysize 26
                background "#a00000"
                fixed:
                    text u"MOM  -  Instant Message":
                        color "#ffffff"
                        bold True
                        size 12
                        xpos 8
                        yalign 0.5
                    text u"_  □  X":
                        color "#ffdede"
                        size 11
                        xalign 1.0
                        xoffset -8
                        yalign 0.5
            # message area
            button:
                xysize (540, 286)
                background "#ffffff"
                hover_background "#fff6f6"
                padding (16, 14, 16, 14)
                action (None if _mom_done else SetScreenVariable("step", step + 1))
                vbox:
                    spacing 7
                    yalign 1.0
                    for _i in range(_mom_shown):
                        text (u"MOM:  " + _mom_lines[_i]):
                            color "#9a0000"
                            bold True
                            size 14
                            xsize 500
                    if not _mom_done:
                        text u"MOM is typing...":
                            color "#b08a8a"
                            italic True
                            size 11
            # status / action bar
            frame:
                xsize 540
                ysize 48
                background "#d4d0c8"
                padding (10, 8, 10, 8)
                if _mom_done:
                    button:
                        xalign 0.5
                        yalign 0.5
                        background "#ece9d8"
                        hover_background "#f0c0c0"
                        padding (22, 6, 22, 6)
                        hover_sound gui.hover_sound
                        activate_sound gui.activate_sound
                        action Return()
                        text u"...i'm coming downstairs.":
                            color "#000000"
                            size 13
                else:
                    text u"▼  (read)":
                        color "#8a6a6a"
                        size 12
                        xalign 0.5
                        yalign 0.5

screen hw2_shutdown(tone="hollow"):
    style_prefix "hw"
    add Solid("#000000")
    key "K_RETURN" action Return()
    timer 6.0 action Return()
    # click anywhere to finish
    button:
        xfill True
        yfill True
        background None
        action Return()
    $ _line2 = {
        "harsh": u"She'll be exactly how you left her.",
        "pushed": u"She doesn't play anymore.",
        "tender": u"She kept the bunny.",
    }.get(tone, u"The room is empty now.")
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 22
        text u"It's now safe to turn her off.":
            color "#e8a200"
            size 28
            xalign 0.5
            text_align 0.5
        text _line2:
            color "#7a6a3a"
            size 16
            xalign 0.5
            text_align 0.5

screen hw2_content_notice():
    style_prefix "hw"
    modal True
    add Solid("#000000")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 720
        padding (0, 0, 0, 0)
        background "#d4d0c8"
        vbox:
            spacing 0
            frame:
                xsize 720
                ysize 26
                padding (8, 4, 8, 4)
                background "#0a246a"
                text "Content Notice":
                    color "#ffffff"
                    bold True
                    size 12
                    yalign 0.5
            frame:
                xsize 720
                padding (24, 22, 24, 18)
                background "#ffffff"
                vbox:
                    spacing 14
                    text "Hina's World deals with unsafe online attention toward a child, peer pressure, bullying, and coercive secrecy.":
                        color "#000000"
                        size 15
                        xsize 672
                    text "This material is not in any way a fantasy, romanticization, or invitation to read it that way.":
                        color "#000000"
                        bold True
                        size 15
                        xsize 672
                    text "You can skip this side story now with no consequence. Future stories will not require finishing it; opening this story is enough.":
                        color "#000000"
                        size 15
                        xsize 672
            frame:
                xsize 720
                padding (0, 8, 18, 16)
                background "#d4d0c8"
                hbox:
                    xalign 1.0
                    spacing 10
                    button:
                        background "#ece9d8"
                        hover_background "#c2d8f0"
                        padding (18, 6, 18, 6)
                        hover_sound gui.hover_sound
                        activate_sound gui.activate_sound
                        action Return("skip")
                        text "Skip":
                            color "#000000"
                            size 13
                    button:
                        background "#0a246a"
                        hover_background "#245edb"
                        padding (18, 6, 18, 6)
                        hover_sound gui.hover_sound
                        activate_sound gui.activate_sound
                        action Return("continue")
                        text "Continue":
                            color "#ffffff"
                            bold True
                            size 13

# =============================================================================
#  LABELS  (zero say-statements -- all story is delivered through the screens)
# =============================================================================

label hw2_maybe_ambient_notice:
    # Intentionally a no-op. The site used to interrupt with pop-ups ("your profile
    # is public", "you have a new guestbook comment") -- but the player should
    # discover all of that on their own: new icons quietly appearing on the desktop,
    # the visitor counter climbing, a guestbook comment that's just...there. The
    # call sites are left in place so escalation can be re-hooked here if needed.
    return

label cs_asahina_01:
    hide screen archive
    hide screen character_stories
    stop music fadeout 1.0
    scene black
    $ _hw_prev_quick_menu = quick_menu
    $ quick_menu = False
    # Opening this story counts for future Asahina unlocks; completion is optional.
    $ persistent.cs_asahina_01_unlocked = True
    call screen hw2_content_notice
    if _return == "skip":
        $ quick_menu = _hw_prev_quick_menu
        return
    $ hw_start_open = False
    $ hw_browser_opened_once = False
    $ hinas_world_page = "home"
    $ hinas_world_corruption = 0
    $ hinas_world_seen_outfitter = False
    $ hinas_world_seen_chatting = False
    $ hinas_world_seen_quiz = False
    $ hinas_world_seen_rating = False
    $ hinas_world_seen_bento = False
    $ hinas_world_seen_petsalon = False
    $ hinas_world_seen_makeover = False
    $ hw_grow = 0
    $ hw_kept_child = 0
    $ hw_kind = 0
    $ hw_cruel = 0
    $ hw_guest = 0
    $ hw_outfit = {}
    $ hw_rating_total = 0
    $ hw_bento = {}
    $ hw_bento_light = 0
    $ hw_bento_fav = 0
    $ hw_makeover_guess = 0
    $ hw_pet_result = ""
    $ hw_nav_history = []
    $ hw_chat_session = 0
    $ hw_ambient_ticks = 0
    $ hw_pressure_notice_stage = 0
    $ hw_last_pressure_reason = ""
    $ hw_photos_viewed = []
    pause 0.6
    jump cs_asahina_desktop

# --- The desktop is the hub. You open windows, close them, and read the log
#     files here. Logging off is ONLY via the Start menu (Turn Off Computer).
label cs_asahina_desktop:
    call screen hw2_desktop
    $ _act = _return
    if _act == "logoff":
        jump cs_asahina_log_off
    if _act == "browser":
        $ hw_add_pressure("open_browser", 1)
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice
        jump cs_asahina_browser_open
    if _act and _act.startswith("snoop:"):
        $ hw_add_pressure("open_folder", 1)
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_1
        jump cs_asahina_snoop
    if _act and _act.startswith("snoopfile:"):
        $ hw_add_pressure("open_file", 1)
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_2
        jump cs_asahina_snoop_file
    if _act and _act.startswith("file:"):
        $ _fname = _act[5:]
        $ hw_add_pressure("desktop_file", 1)
        call screen hw2_notepad(title=_fname + " - Notepad", body=hw_file_body(_fname))
        if _return == "logoff":
            jump cs_asahina_log_off
        if _return and _return.startswith("snoop:"):
            $ _act = _return
            jump cs_asahina_snoop
        if _return and _return.startswith("snoopfile:"):
            $ _act = _return
            jump cs_asahina_snoop_file
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_3
        jump cs_asahina_desktop
    jump cs_asahina_desktop

label cs_asahina_snoop:
    $ _folder = _act[6:]

label cs_asahina_snoop_loop:
    call screen hw2_snoop_folder(_folder)
    $ _sret = _return
    if _sret == "logoff":
        jump cs_asahina_log_off
    if _sret == "close":
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_4
        jump cs_asahina_desktop
    if _sret and _sret.startswith("snoop:"):
        $ _folder = _sret[6:]
        jump cs_asahina_snoop_loop
    if _sret and _sret.startswith("snoopfile:"):
        $ _doc = _sret[10:]
        call screen hw2_notepad(title=hw_snoop_doc_title(_doc) + " - Notepad", body=hw_snoop_doc_body(_doc))
        if _return == "logoff":
            jump cs_asahina_log_off
        if _return and _return.startswith("snoop:"):
            $ _folder = _return[6:]
            jump cs_asahina_snoop_loop
        if _return and _return.startswith("snoopfile:"):
            $ _doc = _return[10:]
            jump cs_asahina_snoop_file_open
        $ _folder = hw_snoop_return_folder
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_5
        jump cs_asahina_snoop_loop
    if _sret and _sret.startswith("img_"):
        $ _slot = _sret[4:]
        $ hw_add_pressure("open_photo", 1)
        $ hw_note_photo_view(_slot)
        call screen hw2_imageview(_slot, hw_site_corruption())
        if _return == "logoff":
            jump cs_asahina_log_off
        $ _folder = hw_snoop_return_folder
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_6
        jump cs_asahina_snoop_loop
    jump cs_asahina_desktop

label cs_asahina_snoop_file:
    $ _doc = _act[10:]
    $ hw_add_pressure("open_file", 1)

label cs_asahina_snoop_file_open:
    call screen hw2_notepad(title=hw_snoop_doc_title(_doc) + " - Notepad", body=hw_snoop_doc_body(_doc))
    if _return == "logoff":
        jump cs_asahina_log_off
    if _return and _return.startswith("snoop:"):
        $ _act = _return
        jump cs_asahina_snoop
    if _return and _return.startswith("snoopfile:"):
        $ _doc = _return[10:]
        jump cs_asahina_snoop_file_open
    call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_7
    jump cs_asahina_desktop

label cs_asahina_browser_open:
    # the Flash preloader plays the first time the site is opened this session
    if not hw_browser_opened_once:
        call screen hw2_preloader
        if _return == "close":
            # closed IE mid-load: back to the desktop, load never finished
            jump cs_asahina_desktop
        $ hw_browser_opened_once = True
        $ hw_add_pressure("preloader", 1)
        if _return == "logoff":
            jump cs_asahina_log_off
        if _return and _return.startswith("snoop:"):
            $ _act = _return
            jump cs_asahina_snoop
        if _return and _return.startswith("snoopfile:"):
            $ _act = _return
            jump cs_asahina_snoop_file
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_8
    jump cs_asahina_browser

label cs_asahina_browser:
    call screen cs_asahina_window98(hinas_world_page, hw_site_corruption(), hinas_world_seen_outfitter, hinas_world_seen_chatting, hinas_world_seen_quiz, hinas_world_seen_rating)
    $ _hw = _return

    if _hw == "logoff":
        jump cs_asahina_log_off
    if _hw and _hw.startswith("snoop:"):
        $ hw_add_pressure("open_folder", 1)
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_9
        $ _act = _hw
        jump cs_asahina_snoop
    if _hw and _hw.startswith("snoopfile:"):
        $ hw_add_pressure("open_file", 1)
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_10
        $ _act = _hw
        jump cs_asahina_snoop_file
    if _hw == "close":
        # the X just closes the tab -- back to the desktop, where the logs are
        jump cs_asahina_desktop

    if _hw == "nav_home":
        $ hw_add_pressure("nav_home", 1)
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_11
        $ hw_nav_to("home")
        jump cs_asahina_browser
    if _hw == "nav_games":
        $ hw_add_pressure("nav_games", 1)
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_12
        $ hw_nav_to("games")
        jump cs_asahina_browser
    if _hw == "nav_gallery":
        $ hw_add_pressure("nav_gallery", 1)
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_13
        $ hw_nav_to("gallery")
        jump cs_asahina_browser
    if _hw == "nav_guestbook":
        $ hw_add_pressure("nav_guestbook", 1)
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_14
        $ hw_nav_to("guestbook")
        jump cs_asahina_browser
    if _hw == "nav_about":
        $ hw_add_pressure("nav_about", 1)
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_15
        $ hw_nav_to("about")
        jump cs_asahina_browser
    if _hw == "nav_back":
        $ hw_nav_back()
        jump cs_asahina_browser
    if _hw == "refresh":
        # the counter goes up when Hina refreshes it. (it is lying.)
        $ hw_add_pressure("refresh", 1)
        jump cs_asahina_browser

    if _hw and _hw.startswith("img_"):
        $ _slot = _hw[4:]
        $ hw_add_pressure("open_photo", 1)
        $ hw_note_photo_view(_slot)
        call screen hw2_imageview(_slot, hw_site_corruption())
        if _return == "logoff":
            jump cs_asahina_log_off
        if _return and _return.startswith("snoop:"):
            $ _act = _return
            jump cs_asahina_snoop
        if _return and _return.startswith("snoopfile:"):
            $ _act = _return
            jump cs_asahina_snoop_file
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_16
        jump cs_asahina_browser

    if _hw == "game_outfitter":
        jump cs_asahina_outfitter
    if _hw == "game_chatting":
        jump cs_asahina_chatting
    if _hw == "game_quiz":
        jump cs_asahina_quiz
    if _hw == "game_rating":
        jump cs_asahina_rating
    if _hw == "game_bento":
        jump cs_asahina_bento
    if _hw == "game_petsalon":
        jump cs_asahina_petsalon
    if _hw == "game_makeover":
        jump cs_asahina_makeover

    jump cs_asahina_browser

# Each game just records its consequences and drops a log file on the desktop --
# no narrator pop-up announcing the horror. The player finds it by reading.
label cs_asahina_outfitter:
    call screen hw2_outfitter
    if _return == "logoff":
        jump cs_asahina_log_off
    if _return and _return.startswith("snoop:"):
        $ _act = _return
        jump cs_asahina_snoop
    if _return and _return.startswith("snoopfile:"):
        $ _act = _return
        jump cs_asahina_snoop_file
    if _return == "cancel":
        # X'd out mid-game: nothing committed, nothing counted
        $ hinas_world_page = "games"
        jump cs_asahina_browser
    $ hinas_world_seen_outfitter = True
    $ hinas_world_corruption = max(hinas_world_corruption, 1)
    $ hw_add_pressure("finish_outfitter", 2)
    call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_17
    $ hinas_world_page = "games"
    jump cs_asahina_browser

label cs_asahina_chatting:
    $ _hw_chat_before = hw_chat_session
    call screen hw2_chatting(_hw_chat_before)
    if _return == "logoff":
        jump cs_asahina_log_off
    if _return and _return.startswith("snoop:"):
        $ _act = _return
        jump cs_asahina_snoop
    if _return and _return.startswith("snoopfile:"):
        $ _act = _return
        jump cs_asahina_snoop_file
    if _return == "cancel":
        # left the room early: the messages were still said, but the room
        # doesn't count as finished and nothing was chosen past that point
        $ hinas_world_page = "games"
        jump cs_asahina_browser
    if _hw_chat_before < len(HW2_CHAT_SCRIPTS):
        $ hinas_world_seen_chatting = True
        $ hw_chat_session = min(hw_chat_session + 1, len(HW2_CHAT_SCRIPTS))
        $ hinas_world_corruption = max(hinas_world_corruption, 2)
        $ hw_add_pressure("finish_chat", 2)
        call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_18
    $ hinas_world_page = "games"
    jump cs_asahina_browser

label cs_asahina_quiz:
    call screen hw2_quiz
    if _return == "logoff":
        jump cs_asahina_log_off
    if _return and _return.startswith("snoop:"):
        $ _act = _return
        jump cs_asahina_snoop
    if _return and _return.startswith("snoopfile:"):
        $ _act = _return
        jump cs_asahina_snoop_file
    if _return == "cancel":
        $ hinas_world_page = "games"
        jump cs_asahina_browser
    $ hinas_world_seen_quiz = True
    $ hinas_world_corruption = max(hinas_world_corruption, 2)
    $ hw_add_pressure("finish_quiz", 2)
    call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_19
    $ hinas_world_page = "games"
    jump cs_asahina_browser

label cs_asahina_rating:
    call screen hw2_rating
    if _return == "logoff":
        jump cs_asahina_log_off
    if _return and _return.startswith("snoop:"):
        $ _act = _return
        jump cs_asahina_snoop
    if _return and _return.startswith("snoopfile:"):
        $ _act = _return
        jump cs_asahina_snoop_file
    if _return == "cancel":
        $ hinas_world_page = "games"
        jump cs_asahina_browser
    $ hinas_world_seen_rating = True
    $ hinas_world_corruption = max(hinas_world_corruption, 3)
    $ hw_add_pressure("finish_rating", 2)
    call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_20
    $ hinas_world_page = "games"
    jump cs_asahina_browser

label cs_asahina_bento:
    call screen hw2_bento
    if _return == "logoff":
        jump cs_asahina_log_off
    if _return and _return.startswith("snoop:"):
        $ _act = _return
        jump cs_asahina_snoop
    if _return and _return.startswith("snoopfile:"):
        $ _act = _return
        jump cs_asahina_snoop_file
    if _return == "cancel":
        $ hinas_world_page = "games"
        jump cs_asahina_browser
    $ hinas_world_seen_bento = True
    $ hw_add_pressure("finish_bento", 2)
    call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_21
    $ hinas_world_page = "games"
    jump cs_asahina_browser

label cs_asahina_petsalon:
    call screen hw2_petsalon
    if _return == "logoff":
        jump cs_asahina_log_off
    if _return and _return.startswith("snoop:"):
        $ _act = _return
        jump cs_asahina_snoop
    if _return and _return.startswith("snoopfile:"):
        $ _act = _return
        jump cs_asahina_snoop_file
    if _return == "cancel":
        $ hinas_world_page = "games"
        jump cs_asahina_browser
    $ hinas_world_seen_petsalon = True
    $ hw_add_pressure("finish_petsalon", 2)
    call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_22
    $ hinas_world_page = "games"
    jump cs_asahina_browser

label cs_asahina_makeover:
    call screen hw2_makeover
    if _return == "logoff":
        jump cs_asahina_log_off
    if _return and _return.startswith("snoop:"):
        $ _act = _return
        jump cs_asahina_snoop
    if _return and _return.startswith("snoopfile:"):
        $ _act = _return
        jump cs_asahina_snoop_file
    if _return == "cancel":
        $ hinas_world_page = "games"
        jump cs_asahina_browser
    $ hinas_world_seen_makeover = True
    $ hw_add_pressure("finish_makeover", 2)
    call hw2_maybe_ambient_notice from _call_hw2_maybe_ambient_notice_23
    $ hinas_world_page = "games"
    jump cs_asahina_browser

# =============================================================================
#  THE CULMINATION  (logging off is the inevitable end; your choices were the
#  log files you could read all along. Restraint over spectacle.)
# =============================================================================
label cs_asahina_log_off:
    $ hw_start_open = False
    $ _hw_tone = hw_ending_tone()

    call screen hw2_msgbox(title="Turn Off Computer", message="Are you sure you want to turn off the computer?", icon="!", buttons=[("Cancel", "cancel"), ("Turn Off", "ok")])
    if _return == "cancel":
        jump cs_asahina_desktop

    # The cliffhanger: if she did the whole thing, the real world catches her on
    # the way out -- Mom's IRC message lands before the machine ever powers down.
    if hw_all_beats_hit():
        call screen hw2_mom_message

    # Straight to shutdown. The diary is on the desktop the whole time for anyone
    # who wants to read it -- we don't force it open and confuse the log-off.
    scene black
    call screen hw2_shutdown(_hw_tone)

label cs_asahina_log_off_end:
    hide screen hw2_startmenu
    scene black with dissolve_scene_full
    pause 0.8
    $ persistent.cs_asahina_01_unlocked = True
    $ hw_start_open = False
    $ cg_unlock("Hina's World")
    $ cs_mark_completed("cs_asahina_01")
    $ quick_menu = _hw_prev_quick_menu
    return


# =============================================================================
#  BROWSER CHROME + SITE DATA  (fully diegetic; contrast fixed; Unicode font)
# =============================================================================

init python:
    HINAS_WORLD_NAV = [
        ("Home", "home"),
        ("Games", "games"),
        ("Gallery", "gallery"),
        ("Guestbook", "guestbook"),
        ("About", "about"),
    ]

    HINAS_WORLD_ADDRESSES = {
        "home": "http://www.hinasworld.net/home.html",
        "games": "http://www.hinasworld.net/games.html",
        "gallery": "http://www.hinasworld.net/gallery.html",
        "guestbook": "http://www.hinasworld.net/guestbook.html",
        "about": "http://www.hinasworld.net/about.html",
    }

    HINAS_WORLD_GAMES = [
        ("outfitter", "#e0559a", "#c20060", "Hina's\nOutfitter", "Dress Hina for school, practice, and growing up."),
        ("chatting", "#aa55e0", "#7700cc", "Hina's\nChatting", "Chat with cute friends from all over the web."),
        ("quiz", "#55aadd", "#0066aa", "Hina's\nQuiz Corner", "Find out how grown-up you really are."),
        ("rating", "#e08844", "#bb5500", "Hina's\nRating Game", "Score today's Hina out of five."),
        ("bento", "#7bc26a", "#2e8b2e", "Hina's\nLunchbox Break", "Pack a yummy lunch for school and practice days!"),
        ("petsalon", "#e8c33f", "#a07a00", "Mr Toast\n& Mochi", "Give the bunny and the cat the royal treatment!"),
        ("makeover", "#55c2b8", "#0e7a70", "Hina's\nMakeover Mirror", "Try new looks in Hina's magic mirror!"),
    ]

# =============================================================================
#  SCREEN: cs_asahina_window98 -- Internet Explorer 6 window with the Flash site
#  Resolution target: 1280x720
# =============================================================================
screen cs_asahina_window98(page="home", corruption=0, seen_outfitter=False, seen_chatting=False, seen_quiz=False, seen_rating=False):
    style_prefix "hw"
    modal True
    # ESC / menu key now open the Start menu (the Start menu is the way to log off)
    key "game_menu" action SetVariable("hw_start_open", not hw_start_open)
    key "K_ESCAPE" action SetVariable("hw_start_open", not hw_start_open)

    $ _hw_stage = hw_escalation_stage()
    $ _hw_address = hw_browser_address(page)

    use hw2_desktop_backdrop()

    # --- Drop shadow ---  (yalign 0.46 matches the mini-game windows, leaving
    #   room for the taskbar below)
    frame:
        xalign 0.5
        yalign 0.46
        xoffset 4
        yoffset 5
        xsize 920
        ysize 636
        padding (0, 0, 0, 0)
        background "#202020"

    # --- Main browser window ---
    frame:
        xalign 0.5
        yalign 0.46
        xsize 920
        ysize 636
        padding (0, 0, 0, 0)
        background "#d4d0c8"

        vbox:
            spacing 0
            xsize 920

            # =========================================================
            #  TITLE BAR  (26px)
            # =========================================================
            frame:
                xsize 920
                ysize 26
                padding (0, 0, 0, 0)
                background "#0a246a"

                frame:
                    xsize 920
                    ysize 2
                    xpos 0
                    ypos 0
                    padding (0, 0, 0, 0)
                    background "#3169c6"

                hbox:
                    xpos 4
                    ypos 15
                    yalign 0.5
                    spacing 4

                    frame:
                        xysize (18, 18)
                        background "#1e4fd4"
                        padding (0, 0, 0, 0)
                        yalign 0.5
                        text "e":
                            color "#ffffff"
                            bold True
                            size 13
                            xalign 0.5
                            yalign 0.5

                    text "Hina's World - Internet Explorer":
                        color "#ffffff"
                        bold True
                        size 11
                        yalign 0.5

                hbox:
                    xalign 1.0
                    xoffset -3
                    yalign 0.5
                    spacing 2

                    # Minimize
                    frame:
                        xysize (17, 15)
                        padding (0, 0, 0, 0)
                        background "#c0c0c0"
                        yalign 0.5
                        text "_":
                            color "#000000"
                            size 12
                            bold True
                            xalign 0.5
                            yalign 0.5

                    # Maximize -- drawn as nested frames (box glyph not guaranteed)
                    frame:
                        xysize (17, 15)
                        padding (0, 0, 0, 0)
                        background "#c0c0c0"
                        yalign 0.5
                        frame:
                            xysize (9, 8)
                            padding (0, 0, 0, 0)
                            background "#000000"
                            xalign 0.5
                            yalign 0.5
                            frame:
                                xysize (7, 6)
                                padding (0, 0, 0, 0)
                                background "#c0c0c0"
                                xalign 0.5
                                yalign 1.0

                    # Close (red) -- closes the TAB, back to the desktop (does
                    # not log off; the logs are still there to read)
                    button:
                        xysize (17, 15)
                        padding (0, 0, 0, 0)
                        background "#c00000"
                        hover_background "#ff3b3b"
                        yalign 0.5
                        action Return("close")
                        text "X":
                            color "#ffffff"
                            bold True
                            size 10
                            xalign 0.5
                            yalign 0.5

            # =========================================================
            #  MENU BAR  (20px)   -- fixed: dark text, now legible
            # =========================================================
            frame:
                xsize 920
                ysize 20
                padding (6, 3, 0, 0)
                background "#d4d0c8"

                hbox:
                    yalign 0.5
                    spacing 14
                    for item in ["File", "Edit", "View", "Favorites", "Tools", "Help"]:
                        text item:
                            color "#000000"
                            size 11

            frame:
                xsize 920
                ysize 1
                padding (0, 0, 0, 0)
                background "#808080"

            # =========================================================
            #  TOOLBAR  (30px)   -- fixed: dark text on the buttons/fields
            # =========================================================
            frame:
                xsize 920
                ysize 30
                padding (4, 3, 4, 3)
                background "#d4d0c8"

                hbox:
                    yalign 0.5
                    spacing 3

                    # Back / Refresh / Home actually work now (Refresh bumps the
                    # visitor counter, exactly like counter_backup.txt claims).
                    # Fwd and Stop stay decorative, greyed like a real IE6.
                    for _btn, _bact in [
                            ("< Back", ("nav_back" if hw_nav_history else None)),
                            ("Fwd >", None),
                            ("Stop", None),
                            ("Refresh", "refresh"),
                            ("Home", "nav_home"),
                        ]:
                        if _bact:
                            button:
                                background "#e4e2dc"
                                hover_background "#c2d8f0"
                                padding (6, 2, 6, 2)
                                yalign 0.5
                                hover_sound gui.hover_sound
                                action Return(_bact)
                                text _btn:
                                    color "#000000"
                                    size 10
                        else:
                            frame:
                                background "#e4e2dc"
                                padding (6, 2, 6, 2)
                                yalign 0.5
                                text _btn:
                                    color "#8a8a8a"
                                    size 10

                    frame:
                        xysize (2, 20)
                        padding (0, 0, 0, 0)
                        background "#808080"
                        yalign 0.5

                    text "Address:":
                        color "#000000"
                        size 10
                        yalign 0.5

                    frame:
                        xsize 486
                        ysize 20
                        padding (4, 2, 4, 2)
                        background "#ffffff"
                        yalign 0.5
                        text _hw_address:
                            color "#000000"
                            size 10
                            yalign 0.5

                    frame:
                        background "#e4e2dc"
                        padding (8, 2, 8, 2)
                        yalign 0.5
                        text "Go":
                            color "#000000"
                            size 10

            frame:
                xsize 920
                ysize 1
                padding (0, 0, 0, 0)
                background "#808080"

            # =========================================================
            #  FLASH SITE CONTENT AREA  (538px)
            # =========================================================
            frame:
                xsize 920
                ysize 538
                padding (0, 0, 0, 0)
                background ("#ffcce8" if _hw_stage < 3 else "#f5d7e8")

                vbox:
                    spacing 0
                    xsize 920

                    # --- Site header bar ---
                    frame:
                        xsize 920
                        ysize 68
                        padding (0, 0, 0, 0)
                        background "#c20060"

                        frame:
                            xsize 920
                            ysize 3
                            xpos 0
                            ypos 0
                            padding (0, 0, 0, 0)
                            background "#ff3399"

                        text u"~*~ Hina's World ~*~":
                            color "#ffff99"
                            bold True
                            size 26
                            xalign 0.5
                            ypos 7

                        text (u"dress up  -  chatting  -  quizzes  -  makeover  -  and more!" if _hw_stage < 2 else u"dress up  -  chatting  -  quizzes  -  profile  -  public"):
                            color "#ffd6ee"
                            size 11
                            xalign 0.5
                            ypos 47

                    # --- Site navigation bar (always visible; high contrast) ---
                    frame:
                        xsize 920
                        ysize 28
                        padding (0, 3, 0, 3)
                        background "#8800aa"

                        hbox:
                            xalign 0.5
                            yalign 0.5
                            spacing 4
                            for nav, nav_page in HINAS_WORLD_NAV:
                                $ _hw_nav_bg = "#ff33dd" if page == nav_page else "#dd00cc"
                                button:
                                    background _hw_nav_bg
                                    hover_background "#ff66dd"
                                    padding (14, 2, 14, 2)
                                    yalign 0.5
                                    hover_sound gui.hover_sound
                                    action Return("nav_" + nav_page)
                                    text nav:
                                        color "#ffffff"
                                        bold True
                                        size 11

                    # --- Main content (left sidebar + body) ---
                    hbox:
                        spacing 0
                        xsize 920

                        # === Left Sidebar (196px) ===
                        frame:
                            xsize 196
                            ysize 442
                            padding (8, 8, 8, 8)
                            background "#ffaad4"

                            vbox:
                                spacing 8
                                xsize 180

                                frame:
                                    xsize 180
                                    padding (7, 6, 7, 6)
                                    background "#ffffff"
                                    vbox:
                                        spacing 4
                                        text "* News *":
                                            color "#d6006e"
                                            bold True
                                            size 12
                                        text (u"> New game added!\n  Hina's Chatting\n  is finally here!" if _hw_stage < 2 else u"> Guestbook busy!\n  Friends are linking\n  Hina's page."):
                                            color "#b3306e"
                                            size 11
                                        text (u"> Outfitter updated\n  with grown-up looks!" if _hw_stage < 3 else u"> Profile stamps on!\n  New visitors show\n  up fast."):
                                            color "#b3306e"
                                            size 11

                                frame:
                                    xsize 180
                                    padding (7, 6, 7, 6)
                                    background "#ffffff"
                                    vbox:
                                        spacing 4
                                        text "* Friends *":
                                            color "#d6006e"
                                            bold True
                                            size 12
                                        for lnk in ["StarCute", "Emily_x0x", "DreamyDoll", "PixelHeart"]:
                                            text u"» " + lnk:
                                                color "#a020c0"
                                                size 11
                                        if corruption >= 2:
                                            text u"» xX_guest_Xx":
                                                color "#7a5c00"
                                                bold True
                                                size 11

                                text u"-~*~-~*~-~*~-~*~-":
                                    color "#ff3399"
                                    size 12
                                    xalign 0.5

                                frame:
                                    xsize 180
                                    padding (7, 6, 7, 6)
                                    background "#330033"
                                    vbox:
                                        spacing 2
                                        text "Visitor No.":
                                            color "#ff99dd"
                                            size 10
                                            xalign 0.5
                                        text hw_visitor_number():
                                            color "#00ff88"
                                            bold True
                                            size 14
                                            xalign 0.5

                        frame:
                            xsize 1
                            ysize 442
                            padding (0, 0, 0, 0)
                            background "#dd88bb"

                        # === Main Content Area (723px) ===
                        frame:
                            xsize 723
                            ysize 442
                            padding (12, 10, 12, 10)
                            background "#ffe6f4"
                            use hinas_world_page_content(page, corruption, seen_outfitter, seen_chatting, seen_quiz, seen_rating)

            # =========================================================
            #  STATUS BAR  (20px)   -- fixed: dark text, now legible
            # =========================================================
            frame:
                xsize 920
                ysize 1
                padding (0, 0, 0, 0)
                background "#808080"

            frame:
                xsize 920
                ysize 19
                padding (4, 2, 4, 2)
                background "#d4d0c8"
                text hw_status_text():
                    color "#000000"
                    size 10
                    xpos 0
                    yalign 0.5
                text "Internet":
                    color "#000000"
                    size 10
                    xalign 1.0
                    xoffset -4
                    yalign 0.5

    # XP taskbar + Start menu (the Start menu is how you log off)
    use hw2_taskbar(task="Hina's World - Internet Explorer")


screen hinas_world_page_content(page, corruption, seen_outfitter, seen_chatting, seen_quiz, seen_rating):
    style_prefix "hw"
    # Read straight from the store so the three newer cabinet games get PLAYED
    # badges too (the four legacy params are kept for call-site compatibility).
    $ _hw_seen = {
        "outfitter": hinas_world_seen_outfitter,
        "chatting": hinas_world_seen_chatting,
        "quiz": hinas_world_seen_quiz,
        "rating": hinas_world_seen_rating,
        "bento": hinas_world_seen_bento,
        "petsalon": hinas_world_seen_petsalon,
        "makeover": hinas_world_seen_makeover,
    }
    $ _hw_stage = hw_escalation_stage()

    vbox:
        spacing 10
        xsize 699

        if page == "home":
            frame:
                xsize 699
                padding (10, 8, 10, 8)
                background "#ffffff"
                vbox:
                    spacing 4
                    text "* Welcome to Hina's World! *":
                        color "#d6006e"
                        bold True
                        size 15
                    text ("The #1 spot for fun Flash games and so much more! Updated weekly~" if corruption < 2 and _hw_stage < 1 else ("The #1 spot for fun Flash games and so much more! Guestbook updated daily~" if _hw_stage < 3 else "The #1 spot for fun Flash games and so much more! People keep finding it.")):
                        color "#b3306e"
                        size 11

            text ("- Featured Games -" if corruption < 2 and _hw_stage < 2 else "- Most Visited -"):
                color "#8800aa"
                bold True
                size 13
                xalign 0.5

            hbox:
                spacing 10
                xsize 699
                for game_id, bg_light, bg_dark, title, blurb in HINAS_WORLD_GAMES[:4]:
                    use hinas_world_game_card(game_id, bg_light, bg_dark, title, blurb, _hw_seen.get(game_id, False))

            button:
                xalign 0.5
                background "#dd00cc"
                hover_background "#ff66dd"
                padding (14, 3, 14, 3)
                hover_sound gui.hover_sound
                action Return("nav_games")
                text u"+ {} more games in the Game Cabinet! →".format(max(0, len(HINAS_WORLD_GAMES) - 4)):
                    color "#ffffff"
                    bold True
                    size 11

            text u"~*~  ~*~  ~*~  ~*~  ~*~  ~*~  ~*~  ~*~  ~*~  ~*~  ~*~":
                color "#ff3399"
                size 11
                xalign 0.5

            hbox:
                spacing 10
                frame:
                    xsize 344
                    padding (9, 7, 9, 7)
                    background "#ffffff"
                    vbox:
                        spacing 3
                        text "* Webring *":
                            color "#d6006e"
                            bold True
                            size 12
                        text "KidsTown Sites -> Glitter Girls -> Hina's World -> Random":
                            color "#8a4575"
                            size 10
                            xsize 320
                        text ("status: linked by 4 friends" if corruption < 2 and _hw_stage < 2 else ("status: linked from Emily's page" if _hw_stage < 4 else "status: linked by someone new")):
                            color "#8a4575"
                            size 10
                frame:
                    xsize 344
                    padding (9, 7, 9, 7)
                    background "#ffffff"
                    vbox:
                        spacing 3
                        text "* Site Stats *":
                            color "#d6006e"
                            bold True
                            size 12
                        text "last updated from: FAMILY-COMPUTER":
                            color "#8a4575"
                            size 10
                        text ("chat rooms left: {}".format(max(0, len(HW2_CHAT_SCRIPTS) - hw_chat_session))):
                            color "#8a4575"
                            size 10
                        if _hw_stage >= 2:
                            text "profile views today: {}".format(hw_pressure_score()):
                                color "#7a0050"
                                size 10

        elif page == "games":
            frame:
                xsize 699
                padding (10, 8, 10, 8)
                background "#ffffff"
                vbox:
                    spacing 4
                    text "* Game Cabinet *":
                        color "#d6006e"
                        bold True
                        size 15
                    text ("Pick any game! They're all super fun!" if corruption < 2 and _hw_stage < 2 else "Pick any game. They remember what you picked last time."):
                        color "#b3306e"
                        size 11

            # Seven cards now -- a scrolling cabinet instead of a fixed 2x2.
            vpgrid:
                cols 2
                spacing 10
                allow_underfull True
                xysize (699, 352)
                scrollbars "vertical"
                mousewheel True
                draggable True
                for game_id, bg_light, bg_dark, title, blurb in HINAS_WORLD_GAMES:
                    use hinas_world_game_card(game_id, bg_light, bg_dark, title, blurb, _hw_seen.get(game_id, False), wide=True)

        elif page == "gallery":
            frame:
                xsize 699
                padding (10, 8, 10, 8)
                background "#ffffff"
                vbox:
                    spacing 4
                    text "* Gallery *":
                        color "#d6006e"
                        bold True
                        size 15
                    text ("Click a picture to see it bigger~" if hw_photos_turned_count() < 1 else "Click a picture. The ones you open don't stay friends-only for long."):
                        color "#b3306e"
                        size 11

            frame:
                xysize (699, 304)
                padding (0, 0, 0, 0)
                background "#fff7fb"
                vpgrid:
                    cols 3
                    spacing 8
                    xysize (699, 304)
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    for _slot, _normal, _wrong in HW2_GALLERY_PHOTOS:
                        $ _pturned = hw_photo_turned(_slot)
                        button:
                            xysize (218, 126)
                            padding (6, 6, 6, 6)
                            background "#ffffff"
                            hover_background "#ffd0ee"
                            hover_sound gui.hover_sound
                            activate_sound gui.activate_sound
                            action Return("img_" + _slot)
                            vbox:
                                spacing 4
                                frame:
                                    xysize (204, 70)
                                    xalign 0.5
                                    background ("#ffb5df" if not _pturned else "#6a4a60")
                                    text ("VIEW" if not _pturned else "PUBLIC"):
                                        color "#ffffff"
                                        bold True
                                        size 13
                                        xalign 0.5
                                        yalign 0.5
                                text _slot:
                                    color ("#a020c0" if not _pturned else "#7a0050")
                                    bold True
                                    size 10
                                    xsize 204
                                    xalign 0.5
                                    text_align 0.5
                                $ _n_comments = len(hw_gallery_comments(_slot))
                                text ("{} comments".format(_n_comments) if not _pturned else "{} comments  ||  public".format(_n_comments)):
                                    color "#8a4575"
                                    size 9
                                    xalign 0.5

            $ _turned_total = hw_photos_turned_count()
            if _turned_total >= 1:
                text ("{} of these are public now. you can't make them friends-only again.".format(_turned_total) if _turned_total < len(HW2_GALLERY_PHOTOS) else u"all of them are public now. that doesn't undo."):
                    color "#7a0050"
                    size 11
                    xalign 0.5

        elif page == "guestbook":
            frame:
                xsize 699
                padding (10, 8, 10, 8)
                background "#ffffff"
                vbox:
                    spacing 4
                    text "* Guestbook *":
                        color "#d6006e"
                        bold True
                        size 15
                    text ("Leave Hina a nice message! No spam please~" if corruption < 2 and _hw_stage < 2 else "Leave Hina a message. The oldest ones keep moving down."):
                        color "#b3306e"
                        size 11

            # Scrollable, like a real guestbook -- and populated by more than
            # just her four friends: webring passersby, a heckler, spam the
            # filter half-caught, and one adult who signs exactly who she is.
            viewport:
                xysize (699, 250)
                scrollbars "vertical"
                mousewheel True
                draggable True
                vbox:
                    spacing 7
                    for _who, _msg, _col in [
                            ("StarCute", "cute page!! add more glitter cursors", "#a020c0"),
                            ("kero_kero_99", "found u thru the webring!! kero kero", "#a020c0"),
                            ("PixelHeart", "your gallery loads slow but i like the track meet pic", "#a020c0"),
                            ("GlitterGardener", "thanks for linking glitter cursor garden! star order shipped hehe", "#a020c0"),
                            ("new_kid", "hina the printer is stuck again. mom says dinner soon", "#336699"),
                            ("xLordVoidx", "pink overload. cool marquee tho", "#b00000"),
                            ("Emily_x0x", "u should delete the baby pictures before ppl see", "#a020c0"),
                            ("FREE_CURSORS_NOW", "CONGRATULATIONS VISITOR!! you have won a (removed by spam filter)", "#b00000"),
                            ("BlossomMama", "lovely page hina! tell your mom i said hello. -pixel's mom", "#2e7a4e"),
                            ("webmistress_yui", "sign mine back?? yui-planet on the webring!!", "#a020c0"),
                        ]:
                        frame:
                            xsize 680
                            padding (8, 5, 8, 5)
                            background "#fff7fb"
                            hbox:
                                spacing 8
                                text _who + ":":
                                    color _col
                                    bold True
                                    size 11
                                    xsize 128
                                text _msg:
                                    color "#8a4575"
                                    size 11
                                    xsize 520

                    # He keeps showing up whether or not she ever answered him
                    # -- persistence is his, not hers. Deniable on its face;
                    # the tell is that he knows her schedule.
                    if _hw_stage >= 3 and hw_chat_session >= 1:
                        frame:
                            xsize 680
                            padding (8, 5, 8, 5)
                            background "#fff7e0"
                            hbox:
                                spacing 8
                                text "xX_guest_Xx:":
                                    color "#7a5c00"
                                    bold True
                                    size 11
                                    xsize 128
                                text "u werent on yesterday. hope practice went ok :)":
                                    color "#6a4a00"
                                    size 11
                                    xsize 520

                    if hw_guest >= 2:
                        frame:
                            xsize 680
                            padding (8, 5, 8, 5)
                            background "#fff0cc"
                            hbox:
                                spacing 8
                                text "xX_guest_Xx:":
                                    color "#7a5c00"
                                    bold True
                                    size 11
                                    xsize 128
                                text "don't answer here. use the other name i gave u":
                                    color "#6a4a00"
                                    size 11
                                    xsize 520

                    if _hw_stage >= 3:
                        frame:
                            xsize 680
                            padding (8, 5, 8, 5)
                            background "#eeeeee"
                            hbox:
                                spacing 8
                                text "system:":
                                    color "#777777"
                                    bold True
                                    size 11
                                    xsize 128
                                text "comment moderation disabled while profile is public":
                                    color "#5a5a5a"
                                    size 11
                                    xsize 520

            if corruption >= 3 or _hw_stage >= 4:
                text u"admin note: one hidden comment is waiting for approval.":
                    color "#7a0050"
                    italic True
                    size 11
                    xalign 0.5

        else:
            frame:
                xsize 699
                padding (10, 8, 10, 8)
                background "#ffffff"
                vbox:
                    spacing 4
                    text "* About Hina *":
                        color "#d6006e"
                        bold True
                        size 15
                    text "Hina loves friends, running, drawing, sleepovers, and making every day fun!":
                        color "#b3306e"
                        size 11

            frame:
                xsize 699
                padding (10, 8, 10, 8)
                background "#fff7fb"
                vbox:
                    spacing 5
                    text u"Favorite show: cartoons (the saturday ones!)":
                        color "#8a4575"
                        size 11
                    text u"Best friend: my cat, mochi ♥":
                        color "#8a4575"
                        size 11
                    text u"Always carries: her bunny, mr toast":
                        color "#8a4575"
                        size 11
                    text u"Shares computer with: asahiko (when he asks nicely)":
                        color "#8a4575"
                        size 11
                    text u"Can't wait for: summer break!!":
                        color "#8a4575"
                        size 11
                    if corruption >= 1:
                        text u"Recently into: older music, staying up late":
                            color "#8a4575"
                            size 11
                    if corruption >= 2 or _hw_stage >= 2:
                        text u"Profile is set to: Public":
                            color "#7a0050"
                            size 11
                    if _hw_stage >= 3:
                        text u"Profile stamp: newest guestbook comment shown first":
                            color "#7a0050"
                            size 11
                    if (corruption >= 2 or _hw_stage >= 2) and hw_guest >= 1:
                        text u"Comments (1):  “such a mature girl :)”  - xX_guest_Xx":
                            color "#7a0050"
                            size 11
                    if corruption >= 3 or _hw_stage >= 4:
                        text u"Last updated: after practice":
                            color "#7a0050"
                            bold True
                            size 11


screen hinas_world_game_card(game_id, bg_light, bg_dark, title, blurb, seen=False, wide=False):
    style_prefix "hw"
    $ _hw_card_size = (334, 92) if wide else (162, 132)
    $ _hw_thumb_size = (96, 70) if wide else (154, 90)
    $ _hw_play_label = "EMPTY" if (game_id == "chatting" and hw_chat_exhausted()) else ("PLAYED" if seen else "- PLAY -")
    $ _hw_blurb = hw_game_blurb(game_id, blurb)

    button:
        xysize _hw_card_size
        padding (4, 4, 4, 4)
        background bg_dark
        hover_background "#ff66cc"
        hover_sound gui.hover_sound
        activate_sound gui.activate_sound
        action Return("game_" + game_id)

        if wide:
            hbox:
                spacing 8
                yalign 0.5
                frame:
                    xysize _hw_thumb_size
                    padding (0, 0, 0, 0)
                    background bg_light
                    text _hw_play_label:
                        color "#ffffff"
                        bold True
                        size 12
                        xalign 0.5
                        yalign 0.5
                vbox:
                    spacing 4
                    xsize 218
                    text title.replace("\n", " "):
                        color "#ffffff"
                        bold True
                        size 11
                    text _hw_blurb:
                        color "#ffe8f4"
                        size 9
        else:
            vbox:
                spacing 4
                xsize 154
                frame:
                    xysize _hw_thumb_size
                    padding (0, 0, 0, 0)
                    background bg_light
                    text _hw_play_label:
                        color "#ffffff"
                        bold True
                        size 15
                        xalign 0.5
                        yalign 0.5
                text title:
                    color "#ffffff"
                    bold True
                    size 10
                    xalign 0.5
                    text_align 0.5
                text _hw_blurb:
                    color "#ffe8f4"
                    size 9
                    xalign 0.5
                    text_align 0.5
                    xsize 146
