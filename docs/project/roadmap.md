# ENTER M -- A DDLC(?) Mod

> **Version:** 0.1.0 | **Engine:** Matsu'Py | **Resolution:** 1280x720
> **Build Name:** ENTER-M | **Save Directory:** ENTERM

---

## Table of Contents

1. [General Story Timeline](#general-story-timeline)
2. [Characters](#characters)
3. [Deaths / Casualties](#deaths--casualties)
4. [Act Outlines](#act-outlines)
5. [Implemented Scenes & Labels](#implemented-scenes--labels)
6. [Locations](#locations)
7. [Music & Audio](#music--audio)
8. [Game Systems & Addons](#game-systems--addons)

---

## General Story Timeline

The story follows the Japanese school calendar and spans one full school year, beginning May 15 and ending March 7 of the following year. Calendar dates are tracked in-engine via the Calendar System addon (default start: April 7, 2025; story start set to **May 15, 2025**).

### ENTER M -- Generation 1

#### Act 1

| Chapter | Date Range | Label(s) | Status |
|---------|-----------|----------|--------|
| Chapter 0.5 | May 15 -- May 31 | `disclaimer`, `s1pro` | **Started** |
| Chapter 1 | June 1 -- July 15 | -- | Not started |
| Chapter 2 | July 16 -- September 1 | -- | Not started |
| Chapter 3 | September 2 -- October 15 | -- | Not started |
| Chapter 4 | October 16 -- December 31 | -- | Not started |
| Chapter 5 | January 1 -- March 7 | -- | Not started |

> **Key scripted date:** Monika disbands the literature club on **February 24, 2026** (label `dev_monika_disbands_club`).

#### Act 2 (Dual Perspective)

| Chapter | Perspective | Label(s) | Status |
|---------|------------|----------|--------|
| Chapter 6 | MC | `s2ch1` (empty) | Not started |
| Chapter 6 | Matsuda | -- | Not started |
| Chapter 7 | MC | -- | Not started |
| Chapter 7 | Matsuda | -- | Not started |
| Chapter 8 | MC | -- | Not started |
| Chapter 8 | Matsuda | -- | Not started |

#### Intermission: *Temperamental*

| Chapter | Label(s) | Status |
|---------|----------|--------|
| Chapter 8x | -- | **Started** (outline only) |
| Chapter 8xx | -- | Not started |
| Chapter 8xxx | -- | Not started |
| Intermission Endgame | -- | Not started |

#### Act 3

| Chapter | Label(s) | Status |
|---------|----------|--------|
| Chapter 9 | `s3ch1` (empty) | Not started |
| Chapter 10 | -- | Not started |
| Chapter 11 | -- | Not started |
| Chapter 12 | -- | Not started |
| Chapter 13 | -- | Not started |
| Endgame | -- | Not started |

#### Gaiden Chapters (Side Content)

| Title | Type | Status |
|-------|------|--------|
| *Vigilante* | RPG (SMT / Persona / Devil Survivor hybrid) | Not started |
| *Asahina* | VN side story (between Acts 2 and 3) | Not started |

---

## Characters

### Introduced in Act 1

---

#### Matsuda Akai

> **Script variable:** `ma` | **Image tag:** `matsuda neut` | **Thematic instrument:** Synth

| Stat | Value |
|------|-------|
| Age | 18 |
| Height | 5'9" (69" / 175.3 cm) |
| Weight | 158 lb |
| Chest | 36" |
| Likes | Mystery novels, sports cars, data fragments (???) |
| Dislikes | Laziness, idiots, mundane tasks |

**Appearance:** Silky red hair in a high ponytail with a right-side braid. Naturally white porcelain skin. Red eyeliner accentuating turquoise/aqua eyes. Left earring is a literal pair of hanging dice (car-mirror style). White fashionable gloves. Diamond-shaped diamond pendant on a silver chain. Well-defined figure.

**Personality & Role:** Known to most as just Matsuda. A foreign transfer student from North America who arrived in Japan with misplaced confidence, fueled by a brief stint as a side character on a children's TV show. This fleeting brush with fame left her with an inflated sense of self-importance. Her persona blends charisma and delusion; she insists on being an idol despite having no real following. Her behavior oscillates between endearing and irritating as she perpetually seeks the spotlight. Beneath her various facades--whether playing the stoic loner or the outgoing socialite--lies deep-seated insecurity and imposter syndrome. She struggles with her past, unable to appreciate her present achievements, and clings to her constructed identity. Despite her sometimes boisterous exterior, she harbors a genuinely kind heart and unwavering loyalty to those she trusts, making her a uniquely contradictory character whose true depth is revealed only to the most persistent friends (which, in this case, is nobody).

**Meta-awareness:** Unbeknownst to MC and others, Matsuda possesses meta-awareness similar to Monika. However, instead of wanting to disrupt or destroy the world, Matsuda seeks to isolate herself from the DDLC-verse and pursue her own creations and endeavors. Despite not being as academically successful, she is more intellectually gifted than her peers, including Monika. She wants to escape her predetermined role but knows she must adhere to her character's script.

**Story presence:** Central focus and actual protagonist of the story. Prevalent throughout all 3 acts.

---

#### MC

> **Script variable:** `mc` (DynamicCharacter, uses `player` name)

| Stat | Value |
|------|-------|
| Age | 18 (graduating senior) |

**Personality & Role:** The narrator. An above-average yet humble student who struggles to balance school, personal life, and other concerns. Joined the literature club at the start of year 11; has been a member for a year and is close friends with Monika, who serves as a crutch for pretty much anything. Despite his intelligence, MC has his share of external and internal struggles that can make him unstable and unreliable at times.

**Story presence:** Narrator throughout the entirety of the main story (Acts 1, 2, 3, and the Intermission).

---

#### Asahina

> **Script variable:** `ah` | **Image tag:** `asahina neut` | **Thematic instrument:** Flute

| Stat | Value |
|------|-------|
| Full Name | Asahina ********* |
| Age | 16 |
| Height | 5'4" (64" / 162.6 cm) |
| Weight | 139 lb |
| Build | Athletic |
| Likes | Video games, volleyball, her boyfriend |
| Dislikes | Nagging, early nights, overbearing people |

**Personality & Role:** MC's younger sister. A freshman in high school (Japanese standards; equivalent to 10th grade in America). Can come off as snobbish and wanting independence, yet gets offended when called childish or immature. She and MC bicker as siblings do, but never out of hatred. At the end of the day, she truly values her brother and friends, even if she doesn't come off that way.

**Story presence:** Major supporting character in Acts 1 and 2. Cameos only (phone calls/texts) in Act 3. Stars in her own Gaiden side story.

---

#### Masayami Inugami (Sam)

> **Script variable:** `sa` | **Image tag:** `sam neut`

| Stat | Value |
|------|-------|
| Age | 18 |
| Height | 5'11" (71" / 180.3 cm) |
| Weight | 165 lb |
| Chest | 38" |
| Likes | Indie music, basketball, power naps |
| Dislikes | Cliffhangers, sour food, micromanagement |

**Personality & Role:** Asahina's boyfriend, who prefers to be called "Sam" informally. Comes off as a ladies' man, which makes Asahina competitive for his attention, though he assures her she's the only one. Can be conniving, but hides this from MC and Asahina.

**Story presence:** Minor character in Act 1, cameo in Act 2. Despite his small role, he serves as a catalyst for a massive conflict regarding Asahina (directly) and Matsuda (indirectly).

---

#### Kotonoha

> **Script variable:** `ko` | **Image tag:** `kotonoha neut` | **Thematic instrument:** Music box

| Stat | Value |
|------|-------|
| Age | 18 |
| Height | 5'5" (65" / 165.1 cm) |
| Weight | Secret |
| Chest | Secret |
| Likes | Unknown |
| Dislikes | Unknown |

**Personality & Role:** A strange individual who effortlessly balances multiple part-time jobs while still in high school. Her presence is felt more at the convenience store, as a waitress, or in other workplaces than in the classroom. Her background is a complete mystery. Never seen socializing or engaging in typical teenage activities, which spawns rumors. Interactions are polite but distant, maintaining a professional demeanor at all times. A living myth to her school--someone people know exists but treat like a Boogeyman. Takes the "Nurse Joy" archetype, except she doesn't have sisters with the same name.

**Story presence:** Recurring in Act 1, appears only a couple of times in Act 2, but plays major roles in the Intermission and Act 3.

---

#### Monika

> **Script variable:** `m` (DynamicCharacter, `m_name`) | **Image tag:** `monika` | **Thematic instrument:** Piano

| Stat | Value |
|------|-------|
| Age | 18 |
| Height | 5'5" (65" / 165.1 cm) |
| Weight | 125 lb |
| Chest | 34" |
| Likes | Reading, piano, debate |
| Dislikes | Procrastination, negativity, bugs |

**Personality & Role:** MC's classmate and president of the literature club. Pretty close friends with MC at the start--her behavior could be mistaken as flirting (it is). Gradually falls into obscurity throughout the story.

**Story presence:** Major character in Act 1, very minor in Act 2, disappears entirely in the Intermission and Act 3.

---

#### Tsubaki Kareda

> **Script variable:** `ts` | **Image tags:** `tsubaki neut`, `tsubaki post_neut`

| Stat | Value |
|------|-------|
| Age | 17 |
| Height | 5'4" (64" / 162.6 cm) |
| Weight | 128 lb |
| Build | Slim |
| Likes | Hygiene, note-taking, validation |
| Dislikes | Egos, drama, loud noises |

**Personality & Role:** Matsuda's best friend from a different class. Perceives herself as painfully average and has an even worse case of insecurity than Matsuda, despite having a couple of secret admirers. Unlike her friends, she wears her insecurity on her sleeve instead of masking it with personas, often resorting to self-deprecation. Keeps her friend circle extremely small, avoiding anyone surrounded by egos or drama. Has an unrequited crush on Sam but keeps it hidden to avoid ruining his relationship with Asahina.

**Story presence:** Subject of conflict in Act 1 (undergoes visible deterioration due to Sam's influence). Seen once and mentioned once in Act 2. Serves as a catalyst for MC rekindling his friendship with Matsuda.

> **Note:** Has a secondary sprite tag (`tsubaki post_neut`) for her deteriorated appearance near the end of Act 1.

---

#### Mom (Himeko)

> **Script variable:** `mom` | **Image tag:** `mom neut`

| Stat | Value |
|------|-------|
| Full Name | Himeko ********* |
| Age | 42 |
| Height | 5'6" (66" / 167.6 cm) |
| Weight | 142 lb |
| Chest | 34" |
| Likes | Her children, deck building, initiative |
| Dislikes | Secrets, unforced errors, messes |

**Personality & Role:** Mother of MC and Asahina. Strict but caring. Featured in the Asahina confrontation scene where she scolds Asahina for her relationship with Sam.

---

#### Generic NPCs

> **Script variables:** `npc1` ("NPC 1"), `npc2` ("NPC 2")

Used for background characters (e.g., jock students gossiping about Tsubaki).

---

### Introduced in Act 2

*TBD -- no characters defined yet.*

---

### Introduced in Act 3

*TBD -- no characters defined yet.*

---

## Deaths / Casualties

| Character | Timing | Details |
|-----------|--------|---------|
| Monika | Act 3 | Implied death. Cause and time of death revealed during *Temperamental*. |
| Tsubaki | Act 2 | Fate unknown. Revealed during the *Asahina* side story. |
| Sam | Act 2 | Fate unknown. Revealed during the *Asahina* side story. |
| Sayori | Act 1 | Never present to begin with. Existence unknown. |
| Yuri | Act 1 | Never present to begin with. Existence unknown. |
| Natsuki | Act 1 | Never present to begin with. Existence unknown. |

> **Roster system note:** The `CharacterProfile` class has a `grayed_out` flag and `is_dead` property. When `grayed_out = True`, the roster reports "Dead" status for that character.

---

## Act Outlines

### Act 1 -- *Started*

**Beginning:**
The school year starts smoothly. MC is doing fine academically, he's joined a club and made friends, and life is typical for a high school senior. He meets Matsuda, and the two become fast friends--almost too fast, as if they became automatic best friends.

**Conflict and Rising Action:**
Minor conflicts are typical high school drama, but the central focus is MC's escalating relationship with Matsuda. She wants his company for what feels like every waking second. Her behavior isn't intentionally malicious; it's driven by a deeper, unseen motivation. MC is almost never home, participates in things he'd normally decline, and his sister begins showing both mockery and genuine concern.

MC must deal with:

- Escalating demands from Matsuda
- Social isolation from other friends and family
- Emotional passive-aggression and manipulation
- Overdependence

Consequences:

- Becomes less rational
- Grades slip as entrance exams approach
- Encounters bullying from students who are jealous or see him as a "lapdog"

Matsuda is not made out to be a villain or anti-heroine, but it should be clear that something is not right with her way of thinking. Her meta-awareness drives her actions as part of a greater plan--she wants to escape her predetermined role while adhering to her character's script, and she often comes across as a clown alongside many other intolerable things (a persona she was designed to embody).

*[Climax TBD: needs a realistic breaking point for MC]*

**Ending:**
Near the end of the school year, MC and Matsuda have a falling out. MC calls out Matsuda for putting him in a toxic friendship: she's been trying to make him more like her, which drives MC to feel stressed and overwhelmed. He feels isolated from his sister and parents because he's been going out of his way to make time for Matsuda and adopting her traits and interests. MC snaps and cuts off their friendship--at least until their paths cross again a few years later.

**Subplots:**

- **Asahina and Sam** -- Asahina's relationship with Sam and its consequences (confrontation scene with Mom at home).
- **Tsubaki's deterioration** -- Her life goes down a dark path due to Sam's influence. Visible decline shown through the `tsubaki post_neut` sprite.

---

### Act 2 -- *Not Started*

**Structure:** The first half is split between two perspectives and narrators: MC and Matsuda. Perspectives swap back and forth, with the flipping growing more rapid as they approach convergence (like waves from a neutron star merger). The player can choose which perspective to start with, but at a certain point the story locks into a set direction. After convergence, MC becomes the default narrator.

**Perspective (MC):**

- Conflict/Action: *TBD*

**Perspective (Matsuda):**

- Conflict/Action: *TBD*

**Convergence:** *TBD*

**Common Conflict and Action:** *TBD*

**Climax:** *TBD*

**Ending:** *TBD*

**Subplots:** *TBD*

---

### Intermission: *Temperamental* -- *Started* (outline only)

> Unlocked after completing the main Enter M story.

A detective thriller involving a cold case. MC is now a licensed public investigator, and Kotonoha is an assistant at the same firm. Matsuda makes a couple of cameo mentions but otherwise takes a backseat. The intermission spans three main chapters and an endgame, each functioning as self-contained acts--the pacing exists in a "pocket dimension" separate from the rest of the game.

---

### Act 3 -- *Not Started*

*No outline yet.*

---

### Gaiden: *Vigilante* -- *Not Started*

An RPG side campaign inspired by mainline SMT, Persona, and Devil Survivor:

| Influence | Elements Borrowed |
|-----------|-------------------|
| SMT | Demon list, press-turn battle system, frame-based moon cycle |
| Persona | PT outfits, unique summoning methods per character, affinity-gated demons |
| Devil Survivor | Lockdown/time-sensitive premise, world building, small playable cast |

---

### Gaiden: *Asahina* -- *Not Started*

A VN side story centered around MC's sister and her life. Takes place between Acts 2 and 3. Intended to be more hopeful than the main plot. Provides finality for Sam, Tsubaki, and other minor characters. Ties up loose ends with the supporting cast.

---

## Implemented Scenes & Labels

All currently defined labels across the project, including dev/test scenes:

| Label | File | Act / Context | Summary |
|-------|------|---------------|---------|
| `start` | script.rpy | Entry point | Initializes variables, routes based on `persistent.playthrough`. Currently calls `dev_scene_manager`. |
| `splashscreen` | splash.rpy | Boot | Splash messages, mod logo, first-run logic, character file restoration. |
| `after_load` | splash.rpy | Load hook | Anti-cheat, save state validation. |
| `disclaimer` | s1ch1.rpy | Pre-game | Content warning, story timeline breakdown, Japanese school schedule explanation. |
| `s1ch1` | s1ch1.rpy | Act 1, Chapter 0.5 | Sets calendar to May 15, 2025. Monika finds MC's ID card in the corridor. Roster system demo. |
| `dev_scene_manager` | dev_scene_manager.rpy | Dev tool | Scene selection menu with toggle controls for persistent archive unlocks. |
| `dev_asahina_grill` | dev_scene_manager.rpy | Act 1 | Mom scolds Asahina (16) for sleeping with Sam. MC forced to listen. Grounding + doctor appointment. |
| `dev_act3_implicit_scene` | dev_scene_manager.rpy | Act 3 | MC visits Matsuda's house. She hasn't been eating. VR lab date suggestion. Implied sexual encounter. |
| `dev_tsubaki_completely_ruined` | dev_scene_manager.rpy | Late Act 1 | Tsubaki appears completely disheveled. MC and Matsuda witness it. Jock NPCs gossip. Leads into `sam_encounter_99`. |
| `sam_encounter_99` | dev_scene_manager.rpy | Late Act 1 | Sam asks MC to spy on Asahina. MC refuses, boards bus. Suspicious text from Asahina vs. Sam walking back to school. |
| `mc_breaking_point` | dev_scene_manager.rpy | Late Act 1 | MC confides in Monika about Matsuda's behavior and Sam's effect on Tsubaki/Asahina. Monika advises him. |
| `dev_mom_cancer_reveal` | dev_scene_manager.rpy | Act 1, Chapter 4 | Calendar: Nov 20, 2025. Mom tells MC she was diagnosed with a rare cancer subtype in early November. Prognosis unclear; Asahina does not know yet. |
| `dev_monika_disbands_club` | dev_scene_manager.rpy | End of Act 1 | Calendar: Feb 24, 2026. Monika tells MC she's disbanding the club. Everyone graduating, no replacements. |
| `cs_matsuda_01` | cs_matsuda_01.rpy | Character Story | "Dead Fantasy" -- tabletop RPG session with Matsuda, Gary, Gregor, Leif, Tsubaki discussing battle tactics. |

---

## Locations

All background images defined in the project:

### Vanilla DDLC Backgrounds

| ID | Description |
|----|-------------|
| `bg residential_day` | Residential street (daytime) |
| `bg class_day` | Classroom (daytime) |
| `bg corridor` | School corridor |
| `bg club_day` | Literature club room (daytime) |
| `bg club_day2` | Literature club room, alternate (1/100 easter egg) |
| `bg closet` | Closet |
| `bg bedroom` | MC's bedroom |
| `bg sayori_bedroom` | Sayori's bedroom |
| `bg house` | House exterior |
| `bg kitchen` | Kitchen |
| `bg notebook` | Notebook |
| `bg notebook-glitch` | Glitched notebook |
| `bg glitch` | Glitch background |

### Mod-Original Backgrounds

| ID | Description |
|----|-------------|
| `bg living_room` | Living room (MC's house) |
| `bg bus_interior` | Bus interior |
| `bg archive` | Archive screen background |
| `bg battlefield01` | Battlefield (Vigilante / Character Stories) |
| `bg castle01` | Castle (Vigilante / Character Stories) |

---

## Music & Audio

### Mod-Original BGM

| Variable | File | Used In |
|----------|------|---------|
| `roster_place` | assets/audio/bgm/roster_place.ogg | Archive menu, general scenes |
| `hopeless` | assets/audio/bgm/hopeless.ogg | Tsubaki's deterioration, Sam encounter |
| `twelveam` | assets/audio/bgm/twelveam.ogg | Monika disbands club scene |
| `canyoufeel` | assets/audio/bgm/canyoufeel.ogg | Main menu |
| `hotr` | assets/audio/bgm/hotr.ogg | "Dead Fantasy" character story |
| `flight` | assets/audio/bgm/flight.ogg | -- |
| `devoted` | assets/audio/bgm/devoted.ogg | -- |

### Mod-Original SFX

| Variable | File |
|----------|------|
| `moddooropen` | assets/audio/sfx/dooropen.ogg |
| `moddoorclose` | assets/audio/sfx/doorclose.ogg |

### Vanilla DDLC BGM (retained)

| Variable | File | Description |
|----------|------|-------------|
| `t1` -- `t10y` | assets/audio/bgm/*.ogg | Original DDLC tracks (Ohayou Sayori, Okay Everyone, etc.) |
| `td` | assets/audio/bgm/d.ogg | Sayo-nara |
| `m1` | assets/audio/bgm/m1.ogg | Just Monika |
| `mend` | assets/audio/bgm/monika-end.ogg | Your Reality |
| `ghostmenu` | assets/audio/bgm/ghostmenu.ogg | Ghost menu theme |
| `g1`, `g2` | assets/audio/bgm/g1.ogg, g2.ogg | Glitch tracks |
| `hb` | assets/audio/bgm/heartbeat.ogg | Heartbeat |

### Vanilla DDLC SFX (retained)

`closet_open`, `closet_close`, `page_turn`, `fall`

---

## Game Systems & Addons

### Calendar System

- **File:** game/addons/Calendar System/calendar_system.rpy
- **Classes:** `CalendarSystem`, `CalendarView`
- **Default start:** April 7, 2025
- **Features:** Day advancement, date formatting (full/short/numeric/persona styles), weekend detection, full calendar pause menu with month navigation
- **Screens:** `calendar_overlay` (top-right default), `calendar_overlay_minimal`, `calendar_overlay_bottom`
- **Theme:** Dark (#1a1a1a) with red accent (#cc0000), gold today (#ffdd55), weekend red (#ff8888), weekday blue (#88ccff)

### Roster / Character Profiles

- **File:** game/addons/Roster View/roster_view.rpy
- **Class:** `CharacterProfile`
- **Fields:** name, full_name, sprite_image, age, height, weight, chest, likes, dislikes, description, fit_mode, manual_exception, grayed_out
- **Screens:** `roster_view_screen` (3x3 grid), `character_detail_screen` (full profile)
- **Functions:** `init_roster()`, `get_character_by_name(name)`

### CG Gallery

- **File:** game/addons/CG View/cg_gallery.rpy
- **Classes:** `CGEntry`, `CGChapter`, `CGAct`
- **Features:** Persistent unlock per CG, fullscreen viewer with navigation, organized by Act > Chapter
- **Current catalog:** Placeholder entries using vanilla DDLC CGs

### Character Stories

- **File:** game/addons/Character Stories/char_stories.rpy
- **Classes:** `CharacterStoryEntry`, `CharacterStoryCatalog`
- **Available:** Matsuda -- "Dead Fantasy" (`cs_matsuda_01`)
- **Coming Soon:** Tsubaki, Asahina, Sam, Mom, Monika, Kotonoha, ???

### Archive Hub

- **File:** game/archive.rpy
- **Items:** Roster, CG Gallery, Music Room, Side Stories, Lost Records, Achievements
- **Panel flags:** `archive_unlocked_roster`, `archive_unlocked_cgs`, `archive_unlocked_music`, `archive_unlocked_poems`, `archive_unlocked_character_stories`, `archive_unlocked_lost_records`, `archive_unlocked_achievements`. All ship True except the Music Room, which is the reward for clearing the campaign (currently the end of Chapter 0.5).
- **Per-item gating:** the shell is open; the contents fill in. Roster slots unlock on `mark_character_met`, outfits when a character is seen wearing one, CGs on `cg_unlock` at each show site, tracks when heard on any music channel. Side-story titles stay sealed until their `cs_*_unlocked` flag is set.

### Visual Effects

- **File:** game/effects.rpy
- **Effects:** Screen inversion, screen tearing/glitch, rectangular static noise, particle bursts, blood particles (drips/bursts/squirts), animated masks, BSOD, vein overlay

### Transforms & Transitions

- **File:** game/transforms.rpy
- **Character positions:** Standard DDLC 4-position grid with show/replace/instant/focus/sink/hop variants
- **Transitions:** dissolve (0.25s), dissolve_cg (0.75s), dissolve_scene (1.0s), eye blink (close/open), wipe left
- **Ambient:** Noise loops, vignette (static/fade/flicker), layer flicker, rewind effect, heartbeat pulse

# Notes to put here because I'm too lazy to format them into this writeup
- Each chapter in act 1 will have a narrative feel where each chapter will have its own self-contained story and subplot, but there is an underlying continuity and narrative underneath that is brewing but doesn't really become apparent until chapter 3. The first half of the act will set the stage and then things will start connecting and coming together in the latter half while still having self-contained stories, EXCEPT for the last chapter in the act where it focuses entirely on the continuous narrative.
- Act 1 is a dark comedy that introduces itself as a slice-of-life story. The TRUE nature of the story begins to unravel at the end of chapter 3. It isn't a dark comedy for the sake of being dark; it should tackle some very real subject material that most teenagers and young adults could probably relate to.
- Throughout the calendar year of Act 1, there will be days that have MAJOR story beats, but others will be simply "Daily Life" segments that either give some miscellaneous interactions between characters or set up the stage for future major story points.

Ideas for episodic chapter subplots:
- Chapter 0.5: Introducing the main cast of the act, friendship dynamics, relationship dynamics, etc. Fun bout about MC's time in the literature club
- Ch1: School days, classes, clubs, literature, and a rival subplot between Matsuda and Monika
- Ch2: Summertime fun between MC and Matsuda that turns into...something, idk i'm still brainstorming
- Ch3: Love triangle drama between Tsubaki, Sam, and Asahina. There should now be noticeable decline in MC's performance, health, etc, but it gets brushed off narratively (like MC doesn't want the reader to pay attention to that fact). Some sort of massive tonal shift should happen at the end of the chapter that makes it clear that something is very wrong with the story, but it shouldn't be so blatant that it completely overshadows the narrative. It should be more of a "wait, what?" moment that leaves the reader with a sense of unease and confusion, but they can still continue on with the story without being too distracted by it.
- Ch4: i have no idea, but it should end with the reveal of Tsubaki's complete and utter deterioration that started back in chapter 2 or 3 (a la metamorphosis/emergence/177071/that really fucked up comic). The ending should be where the underlying narrative is at its loudest and most apparent--so much so that it basically TRIES to hog the spotlight as if it were aware as some sort of force of nature.
- Ch5: Tying together the rest of the loose ends in the continous/underlying narrative. At the end, MC is finally given an excuse to distance himself and cut ties with Matsuda (currently not known what this excuse is. Maybe a giant verbal altercation or some such?) Pretty much the whole chapter until the ending should feel quiet, more monochrome, and subdued compared to everything else. Think of how the season of winter can often be associated with slow, quiet, and bleak atmospheres. The chapter should feel like that, and the ending should be the "spring" where things start to look up for MC but still with a bittersweet tone.

Ideas for major story beats:
- MC's mom reveals that she was diagnosed with cancer in early November and it's a rare strand, meaning there's an unknown fatality rate. Happens sometime in chapter 4.
- Tsubaki should be completely removed from the narrative come the final chapter, as her fate should be left ambiguous--she's stopped coming to school, nobody hears a response from her via text or call, it's like she disappeared off the face of the earth. Not even the story acknowledges her anymore.

Rambling notes:
- over the course of the story as well, there should be very subtle hints that things about matsuda herself are a bit weird. for example: - oddly immodest around MC (exhibit A, she is awfully calm about MC seeing her in a swimsuit during summertime, especially since matsuda knows what she has as far as her body goes) - complete clown in class but somehow still has extremely high grades (enough to rival monika's) - sometimes lukewarm reactions to things that happen in the world, when extreme emotions and tension would be high kind of like, instead of being self-aware and having an ego death, she KNOWS she's a character and she's more than willing to play the part as best as she can, but she still has gaps in her acting
- the reason i chose MC having an excuse instead of some profound realization is because most teenagers who are in toxic relationships often stay in them because they justify it in their head to some degree. when something happens that puts the relationship in jeopardy, that's when someone goes "this is my chance to unbuckle and escape"

- MC's classes during the day (in the given order) so I don't forget:
    1. Phys Ed
    2. Civics (Senior Social Studies)
    3. Japanese L.A.
    4. Biology

    4.5. Lunch break
    
    5. Chemistry
    6. College Algebra
    7. English (Foreign Language)

Character Story Notes:
- These stories are meant for me to explore different ways of storytelling. No two characters should share the same format

- Sam's story 1:
    - Based on a crappy/weird bootleg video game that someone would either find at a yard sale or download from Aptoide
- Monika's story 1: Do better and more cohesive work with the sprites (add in MPT?)
    - Straightforward, DDLC mod format, Little Timmy's first DDLC mod.
- Kotonoha's story 1: Just change the music to something that isn't copyrighted and reduce redundant repetition
    - Based on the formatting seen in the Nier Replicant Forest of Myth text adventures
- Asahina's story 1: Not written yet
    - Make the story based on the Lacey Games horror series (2000s flash site with flash games)
- Mom's story 1: Not written yet
- Tsubaki's story 1: Not written yet
    - Split screen text adventures where the reader has to manage their focus on the same story but told through two different mindsets
- Matsuda's story 1: Not written yet
    - An actualization of a D&D campaign that's happening between her and MC

(THIS WHOLE DOC IS SEVERELY OUT OF DATE AND NEEDS UPDATED, BUT STILL SERVES USEFUL FOR CONTEXT)
