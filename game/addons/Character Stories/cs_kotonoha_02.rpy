# =============================================================================
# cs_kotonoha_02.rpy  --  Kotonoha character story 02, "The Void Hunter"
# =============================================================================
#
# Uses the Nier Replicant Text Adventure format.
# A deconstruction of the hero's journey.
# The "void hunter" is not literal -- she hunts for meaning
# in a world that has stopped providing it.
# Disjointed identity: she has been every role but none of them are hers.
# Central thread: she is looking for a worthy end for her sword's story.
#
# WIRING / MECHANICS
#   Registered in char_stories.rpy as CharacterStoryEntry("The Void Hunter", ...,
#   "cs_kotonoha_02", "cs_kotonoha_02_unlocked"); reached via Start("cs_kotonoha_02").
#
#   Same Nier-mode toolkit as cs_kotonoha_01 (see that file's header):
#   nier_enter / nier_section / nier "..." / nier_clear / nier_exit, plus the
#   `menu (screen="nier_nvl_choice")` attention checks. Wrong answers
#   jump cs_kotonoha_02_fail (bottom of file) -> rebuke, nier_exit, return.
#   The checks are a Nier Replicant homage and an anti-skip / anti-AFK device,
#   not a difficulty setting -- see the long note in cs_kotonoha_01.rpy's
#   header for the full reasoning; it governs both files.
#
#   ON COMPLETION: sets persistent.cs_kotonoha_02_unlocked = True, then
#   nier_exit + return. (Note: the unique `from _call_nier_*` clause suffixes on
#   the call statements are Matsu'Py rollback-id tags; they keep save compatibility
#   across edits and must stay unique within the file.)
# =============================================================================

label cs_kotonoha_02:

    stop music fadeout 1.0

    call nier_enter from _call_nier_enter_1

    call nier_section("The Void Hunter") from _call_nier_section_8

    # =================================================================
    #  Prologue -- The Road Without End
    # =================================================================

    nier "There is a road that runs through the center of the continent."
    nier "It was built for armies, back when there were armies worth building roads for -- supply lines and cavalry and siege engines dragged on wooden wheels through mud that never fully dried."
    nier "The armies have been gone for thirty years now, and the mud has hardened into something permanent, and the road just continues, the way a scar continues long after the wound has closed."

    call nier_clear from _call_nier_clear_109
    play music sands
    pause 2.0

    nier "A woman walks it."
    nier "She has no name, or hasn't used one in long enough that the distinction stopped mattering. A coin passed through enough hands eventually loses the face stamped on it."
    nier "She carries a sword on her back, longer than her arm, wrapped in stained cloth. The hilt protrudes above her left shoulder."
    nier "Her boots are cracked at the soles. Her coat, once black, has faded to the color of a bruise in its final days -- that sickly, indeterminate yellow-gray that comes just before the skin forgets it was ever hurt."

    call nier_clear from _call_nier_clear_110

    show bg grassy zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "The road ahead does not curve and does not fork. It goes flat and straight until the heat haze swallows it and the horizon closes like a door."
    nier "Behind her, the same road runs backward into the same haze. She does not look at it."

    call nier_clear from _call_nier_clear_111

    nier "The world she walks through is one that has finished its story."
    nier "The great wars ended a generation ago. The demon kings -- three of them, in succession -- were slain by heroes whose names are carved into monuments that no one visits anymore."
    nier "The cursed lands were purified, the stolen princesses returned, the ancient seals restored. Every prophecy fulfilled, every quest completed, every magic blade pulled from whatever it was stuck in."
    nier "And afterward, the world did what it does when the danger passes."

    call nier_clear from _call_nier_clear_112

    nier "The blacksmiths who forged legendary weapons make horseshoes now. The war mages teach arithmetic at village schools. The great fortresses have been converted into granaries and government offices, their battlements hung with laundry."
    nier "The heroes grew old, or died, or disappeared into a quiet that no one bothered to write songs about."

    call nier_clear from _call_nier_clear_113

    nier "The woman has been walking for a long time."
    nier "She has been asked, at crossroads and inns and in the doorways of places she passed through and did not stay, where she is going."
    nier "She has never had a useful answer."
    nier "Each morning, before the road, she checks the wrapping on the sword. The knots, the cloth, the way the weight sits against her back. The hilt her hand has not touched in months."
    nier "She does this with the care you give to something you are not finished with yet."

    call nier_clear from _call_nier_clear_114
    pause 2.0

    # Attention check: Prologue
    nier "..."
    nier "I ask:"
    nier "What color has her coat faded to?"

    menu (screen="nier_nvl_choice"):
        "The gray of a winter sky before snow.":
            jump cs_kotonoha_02_fail
        "The color of a bruise in its final days.":
            pass
        "Old blood, dried past recognition.":
            jump cs_kotonoha_02_fail
        "The yellow of a candle burning down.":
            jump cs_kotonoha_02_fail

    call nier_clear from _call_nier_clear_115

    nier "That sickly yellow-gray."
    nier "You noticed."

    scene black with dissolve

    # =================================================================
    #  I. The Last Village
    # =================================================================

    call nier_section("I. The Last Village") from _call_nier_section_9

    stop music fadeout 2.0
    pause 2.0
    play music popola

    show bg town_day zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "The village has a name, painted on a wooden sign at the crossroads, but the paint has run and faded until the letters are guesswork."
    nier "It exists between other places -- a stop you make on your way to wherever you're actually going, a comma in a longer sentence."

    call nier_clear from _call_nier_clear_116

    nier "Thirty houses, a well, and a tavern with a thatched roof that sags on one side. A market square that's really just a patch of packed dirt where three women sell turnips from woven baskets and an old man sharpens knives on a whetstone he's been using since before the wars."
    nier "Children run through the streets with the particular loudness of people who have never once considered that they might not exist tomorrow."

    call nier_clear from _call_nier_clear_117

    nier "The woman enters the village without announcement."
    nier "She sits at the tavern and orders water. The barkeep, a wide woman with hands like bread loaves, sets a cup down and looks at the shape on her back."
    nier "\"Soldier?\" she asks."
    nier "\"No.\""
    nier "\"Mercenary.\""
    nier "\"No.\""
    nier "The barkeep waits. The woman drinks her water."
    nier "\"Just passing through,\" she says."

    call nier_clear from _call_nier_clear_118

    nier "She doesn't pass through."
    nier "She stays three days, sleeping in the stable loft because the inn has no rooms, or because she prefers it -- difficult to tell with her."
    nier "On the second day she fixes the tavern's back door, which has been hanging at an angle since the last storm, working the hinge back into alignment before anyone thought to ask her."
    nier "On the third day, the village elder comes to see her."

    call nier_clear from _call_nier_clear_119

    nier "He has the look of a man who stopped changing a long time ago -- settled, worn smooth, everything about him decided."
    nier "He sits across from her at the tavern table and folds his hands and tells her about the thing to the east."
    nier "He calls it The {i}Recess{/i}."
    nier "\"Three days past the old garrison,\" he says. \"Into the hills where the war mages used to train. There's a place where things aren't right. Crops won't grow near it. Animals go around it. Even the wind seems to lose interest.\""

    call nier_clear from _call_nier_clear_120

    nier "\"People hear about it,\" he says. \"Word spreads. Soldiers, drifters, folks who came back from the wars and couldn't settle. They come through here asking directions, asking if it's real.\""
    nier "\"Sometimes we send our own. We sent three this past year. They all came back, but they came back quieter. Changed. Like they'd left some portion of themselves out there and couldn't say which.\""

    call nier_clear from _call_nier_clear_121

    nier "He looks at the shape on her back."
    nier "\"We can't pay much. But if you could go and see what it actually is--\""
    nier "\"I'll go,\" she says."
    nier "He blinks. He opens his mouth to mention provisions, or terms, but she is already standing."

    call nier_clear from _call_nier_clear_122

    nier "He watches her collect her things from the stable loft. On the counter below, the barkeep already has a full waterskin waiting."
    nier "\"Why?\" he says, from the bottom of the ladder."
    nier "She pauses at the door. The light from outside falls across her in a bright, shapeless column, and for a moment she is only a silhouette."
    nier "\"Because you asked,\" she says."

    call nier_clear from _call_nier_clear_123
    pause 2.0

    # Attention check: Section I
    nier "..."
    nier "I ask:"
    nier "What did the village elder call the thing in the hills?"

    menu (screen="nier_nvl_choice"):
        "The void.":
            jump cs_kotonoha_02_fail
        "The wound.":
            jump cs_kotonoha_02_fail
        "The Recess.":
            pass
        "The absence.":
            jump cs_kotonoha_02_fail

    call nier_clear from _call_nier_clear_124

    nier "The Recess."
    nier "He was careful with the word. People usually are, when they're naming something they don't understand."

    # =================================================================
    #  II. The Blade That Remembers
    # =================================================================

    call nier_section("II. The Blade That Remembers") from _call_nier_section_10

    stop music fadeout 2.0
    pause 2.0
    play music automatons

    show bg fortress zorder 2
    show black zorder 3:
        alpha 0.55
    with dissolve_scene_full

    nier "She unwraps the sword on the first night out, sitting by a fire she built from dead grass and the bones of a fence that used to mark someone's property line."
    nier "The cloth falls away in stiff strips, and the blade catches the firelight and throws it back in a long, unbroken line."

    call nier_clear from _call_nier_clear_125

    nier "It is a beautiful weapon, though not in any decorative sense. No gilt, no jewels, no inscriptions."
    nier "Every curve and taper has been shaped by use -- hammered, honed, ground down, built back up. The steel carries a grain like wood, folds upon folds upon folds, each one a hammer strike from a forge she hasn't visited in fifteen years."
    nier "The edge is so fine it seems to vanish where steel meets air."

    call nier_clear from _call_nier_clear_126

    nier "She holds the blade flat across her knees."
    nier "She has carried it for longer than she carried anything else in her life."
    nier "She has no good answer for why she still does."

    call nier_clear from _call_nier_clear_127

    nier "She was twenty-four when they put a sword in her hands for the first time."
    nier "The recruitment officer had a long face and tired eyes and a clipboard with more names on it than the page could comfortably hold. He measured her with his gaze the same way a carpenter measures lumber."
    nier "\"Can you fight?\" he asked."
    nier "\"I don't know,\" she said."
    nier "\"Close enough. We'll teach you.\""

    call nier_clear from _call_nier_clear_128

    nier "They taught her in six weeks, though it should have been six months. The third demon king's army was pressing south, and the kingdom needed bodies faster than it needed skill."
    nier "She learned to cut and block and parry, to keep her weight centered and her grip loose until the moment before contact. She learned that hesitation was a luxury no one in the infantry could afford."
    nier "She learned quickly, and she would later understand that this was not the same thing as learning well."

    call nier_clear from _call_nier_clear_129

    nier "Her first battle was in a valley between two rivers, where the farmland had been cleared and flattened into something the generals could use."
    nier "The songs always get the noise wrong. They remember the clash of swords, the war cries, the thunder of cavalry. They forget the rest -- the sucking sound of boots in mud that never dried, the animal screaming of horses caught in the advance, the wet, dense percussion of a human body hitting the ground at the full weight of everything it ever was."
    nier "She remembers all of it. Every sound from that day is filed away in perfect sequence, whether she wants it there or not."

    call nier_clear from _call_nier_clear_130

    nier "The line broke forty minutes in."
    nier "It frayed strand by strand, tension snapping in stages, until the formation dissolved into loose clusters of men swinging at whatever was closest."
    nier "She was in the third rank when the second rank collapsed forward. A man in front of her took a spear through the collarbone and fell sideways, clutching at her leg as he went down, and she stepped over him because there was no space to go around."

    call nier_clear from _call_nier_clear_131

    nier "Her first kill came from the left."
    nier "A young man, younger than her maybe, with a shield held too high and his footing planted wrong. She registered both errors in the same instant -- automatic, faster than thought, some process running underneath her that she hadn't been aware of until it surfaced."
    nier "She brought her sword across his exposed side, felt the resistance of cloth and then the different resistance underneath, and followed through to the end of the arc because a half-finished swing was how you got killed."

    call nier_clear from _call_nier_clear_132

    nier "He looked at her."
    nier "He was holding his side with both hands and his mouth was open and nothing was coming out, and she could see in his eyes the moment when he understood what had happened, and then the moment, immediately after, when understanding stopped mattering."
    nier "He fell, and the space where he'd been filled up with other bodies and other noise, and she kept moving because there was nothing else to do."

    call nier_clear from _call_nier_clear_133

    nier "The battle lasted six hours. She killed eleven men, though she didn't count them at the time. The number came later, in the debriefing tent, when an officer with clean boots asked each surviving soldier to estimate their kills and she realized she could recall every one of them in sequence, like beads on a string."
    nier "This was not a talent she had asked for."
    nier "She would come to rely on it completely."

    call nier_clear from _call_nier_clear_134

    nier "Over the next three years and nine battles she became something the other soldiers didn't have a word for."
    nier "She simply became very good at a thing that did not require her to feel anything about it, and the other soldiers gave her space in the corridors and didn't look at her too long."

    call nier_clear from _call_nier_clear_135

    nier "The last battle was the siege of the third demon king's fortress."
    nier "Eleven days. Walls of black stone that seemed to absorb the light, so that the fortress looked less like a building and more like a hole cut into the landscape."
    nier "She was part of the breach team: twelve soldiers and a war mage named Orsin who laughed before every engagement as though he'd heard a joke no one else was privy to, and a battering ram fashioned from the mast of a captured ship."
    nier "Tan was a former farmhand, built and disposed like someone who'd spent his life swinging heavy things at stubborn objects. He bound a gash across his forearm with a strip of dead man's sleeve and did not slow down."
    nier "They made the breach at dawn on the twelfth day."

    call nier_clear from _call_nier_clear_136

    nier "The inside of the fortress was a maze of narrow corridors lit by torches in rusted iron brackets, every surface the same featureless black stone, the echoes playing tricks with distance and direction."
    nier "They fought through them one by one. Close-quarters, grinding -- only the front two could engage at a time, which meant the woman and Tan carved at the front while the rest waited and took their turns when someone fell back."
    nier "In the second corridor, crossbow bolts came through slots cut into the walls. The team lost three soldiers before Orsin burned the mechanisms out with a pulse of fire that left the stone glowing dull red and the air tasting of copper. The floor became difficult to stand on."

    call nier_clear from _call_nier_clear_137

    nier "Orsin fell in the third corridor."
    nier "A crossbow bolt through the base of the throat, fired from a dark alcove she hadn't cleared. He dropped mid-laugh -- the sound just stopped, cut from the middle like a note torn out of a song, and the silence that replaced it was louder than anything else in the corridor."
    nier "She did not stop. There was no time and no point, and she had learned by then that grief was something you carried forward."

    call nier_clear from _call_nier_clear_138

    nier "By the time she pushed through the doors of the throne room, she was the last of the twelve still standing. Tan was two corridors back, slumped against a wall with his hands in his lap, breathing in a way that meant he would not be breathing much longer."
    nier "She had not said goodbye. There was nothing to say that the silence between them hadn't already covered."

    call nier_clear from _call_nier_clear_139

    nier "The demon king was already dead."
    nier "Poisoned by his own court. His body sat slumped on the throne with its chin on its chest and its hands folded, like a man who had fallen asleep in the middle of a thought he couldn't finish."
    nier "She stood in the doorway with her sword in her hand and blood drying on her coat, her chest rising and falling with the mechanical regularity of a body that does not know it is allowed to stop."
    nier "The room held nothing she could swing at, nothing she could cut through, and she stood there for a long time in that emptiness, in that silence."

    call nier_clear from _call_nier_clear_140

    nier "This was supposed to be the ending. This was where the sword was supposed to find its final purpose -- a demon king's throat, a last clean stroke, the closing line of a story that would justify everything the blade had done."
    nier "Instead: a corpse that someone else had already made. A room full of still air and torchlight and nothing."
    nier "The sword's story should have ended there. She couldn't let it end there."

    call nier_clear from _call_nier_clear_141

    nier "She turned and walked out through the rubble and the cheering and the morning light."
    nier "She did not stop walking."
    nier "That was twelve years ago."

    call nier_clear from _call_nier_clear_142
    pause 2.0

    # Attention check: Section II
    nier "..."
    nier "I ask:"
    nier "When she reached the throne room, what did she find?"

    menu (screen="nier_nvl_choice"):
        "The demon king, waiting for her.":
            jump cs_kotonoha_02_fail
        "An empty throne.":
            jump cs_kotonoha_02_fail
        "The demon king, already dead.":
            pass
        "A locked door she could not open.":
            jump cs_kotonoha_02_fail

    call nier_clear from _call_nier_clear_143

    nier "Already dead. Poisoned by his own court before she ever reached him."
    nier "She'd fought through three corridors and lost eleven people and the ending had already been decided without her."

    # =================================================================
    #  III. The Old Man on the Hill
    # =================================================================

    call nier_section("III. The Old Man on the Hill") from _call_nier_section_11

    stop music fadeout 2.0
    pause 2.0
    play music devola

    show bg fields zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "The hills east of the village rise in slow, patient increments, and the trees thin as she climbs -- mostly birch, their white trunks standing bare in the gray air."
    nier "By midday she reaches a plateau, and on the plateau there is a cottage, and in front of the cottage there is an old man sitting on a stump, peeling an apple with a knife so small it looks borrowed from a child's kitchen set."

    call nier_clear from _call_nier_clear_144

    nier "He looks up when she approaches."
    nier "He is spectacularly old, his face furrowed and hard at the center, the texture of a walnut that spent too many seasons in the sun. His eyes are the color of water in winter -- pale and difficult to look away from."
    nier "He wears a robe that was once white and has since absorbed the color of everything that happened in it: wood smoke, grass stains, decades of not caring about laundry."
    nier "\"Ah,\" he says. \"A sword.\""
    nier "\"A person carrying one.\""
    nier "\"If you say so.\""

    call nier_clear from _call_nier_clear_145

    nier "He claims to be a former war mage, Third Division, Northern Front, under General Hakuya."
    nier "\"Got turned into a frog once,\" he says cheerfully, slicing the apple into paper-thin segments. \"Twice, actually. The second time was on purpose, heheh.\""
    nier "She sits across from him on a rock. She had not planned to stop, but the old man has a voice that fills a space without crowding it -- warm, unhurried, oddly difficult to walk away from."

    call nier_clear from _call_nier_clear_146

    nier "\"You're heading for the recess,\" he says, and it is not a question."
    nier "\"The village asked.\""
    nier "\"And you went.\""
    nier "\"Yes.\""
    nier "He considers this while an apple slice disappears into his mouth."

    call nier_clear from _call_nier_clear_147

    nier "\"You're not the first to come this direction, you know. Not even the first this season.\""
    nier "\"The elder mentioned others.\""
    nier "\"I don't mean the village's people. I mean everyone else. The ones who hear about it on the road, at taverns, in barracks. Former soldiers, mostly. People who came home from the wars and found that home didn't fit anymore, or that they didn't fit inside it.\""

    call nier_clear from _call_nier_clear_148

    nier "He slices another segment, holds it up to the light, examines it as though it contains something worth reading."
    nier "\"They pass through here every few months. Always heading east. Always with this look -- you'd know it if you saw it. Not despair, exactly. More like they're waiting for something to happen and they've run out of places to wait.\""
    nier "\"Word spreads?\""
    nier "\"Word always spreads. Someone tells someone in a tavern. Someone writes it in a letter. Someone scratches it into the wall of a waystation. {i}Three days east past the garrison, into the hills. There's a place there. Go and see.{/i}\""

    call nier_clear from _call_nier_clear_149

    nier "\"I went there once myself,\" he says. \"Twenty years ago, give or take. Memory goes soft at the edges after a while.\""
    nier "\"What did you find?\""
    nier "\"That's the wrong question. The right one is what I brought with me.\""

    call nier_clear from _call_nier_clear_150

    nier "He offers her an apple slice on the flat of his knife. She takes it and eats it, and it is the sweetest thing she has tasted in months -- though she couldn't tell you whether the apple is exceptional or her mouth has simply forgotten the scale."

    call nier_clear from _call_nier_clear_151

    nier "\"The Recess isn't something you can fight,\" he says. \"You know that already, or you wouldn't have agreed so quickly.\""
    nier "\"I know.\""
    nier "\"People go in thinking they'll fix it. The village sends them, and they go, and they come back with less of themselves than they left with.\""
    nier "\"They told me.\""

    call nier_clear from _call_nier_clear_152

    nier "He finishes the apple and sets the knife on his knee."
    nier "\"The ones who come back the worst are the ones who go in thinking they've already lost everything there is to lose.\""
    nier "She looks at him. He looks back with those winter-water eyes, and neither of them says anything for a while, and the wind moves through the birch trees below but does not reach the plateau."

    call nier_clear from _call_nier_clear_153

    nier "\"That sword,\" he says. \"You've been carrying it for a long time.\""
    nier "\"Yes.\""
    nier "\"Are you looking for somewhere to use it, or somewhere to leave it?\""
    nier "She doesn't answer. He nods, as though the silence told him what he needed."

    call nier_clear from _call_nier_clear_154

    nier "He goes into the cottage and comes back with a folded piece of stained cloth covered in faded ink lines -- a map, or something that was once trying to be one."
    nier "She unfolds it, and the lines loop and contradict, and the distances seem to change depending on which direction she reads them."
    nier "\"This won't help me,\" she says."
    nier "\"Probably not,\" he agrees. \"But it was all I had to give, and you looked like someone who could use the gesture.\""

    call nier_clear from _call_nier_clear_155
    pause 2.0

    # Attention check: Section III
    nier "..."
    nier "I ask:"
    nier "What did the old man say about the people who fare worst in the recess?"

    menu (screen="nier_nvl_choice"):
        "They go in afraid.":
            jump cs_kotonoha_02_fail
        "They go in angry.":
            jump cs_kotonoha_02_fail
        "They go in thinking they've lost everything.":
            pass
        "They go in without a weapon.":
            jump cs_kotonoha_02_fail

    call nier_clear from _call_nier_clear_156

    nier "They go in thinking they've already lost everything there is to lose."
    nier "He looked at her when he said it, and she did not look away, and neither of them named what that meant."

    # =================================================================
    #  IV. The Crossing
    # =================================================================

    call nier_section("IV. The Crossing") from _call_nier_section_12

    stop music fadeout 2.0
    pause 2.0
    play music hotr

    show bg grassy zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "The old garrison sits where the elder said it would -- a ruin of stone walls and collapsed watchtowers, all overtaken by ivy, sitting in a field of tall grass."
    nier "She passes through it without stopping."

    call nier_clear from _call_nier_clear_157

    nier "Beyond the garrison, the hills flatten into a wide plain. The grass is golden-brown and waist-high and moves under the wind in long, slow waves, and there is no path through it."
    nier "She walks straight, navigating by the sun and the shape of the hills ahead."

    call nier_clear from _call_nier_clear_158

    nier "On the second day, the bandits find her."
    nier "There are six of them, and they rise out of the grass in a loose semicircle with the practiced ease of people who have done this many times before."
    nier "Their weapons are an assortment: two with short swords, one with a hand axe, one with a spear whose head has been chipped and resharpened until it barely qualifies, one with a nail-studded club, and one -- the leader, a tall man with a jaw like a shovel -- carrying a polearm that has been modified so many times it no longer resembles whatever weapon it started as."

    call nier_clear from _call_nier_clear_159

    nier "\"The sword,\" the leader says. \"And whatever else you're carrying. We don't want this to be difficult.\""
    nier "She looks at him, and then at each of the others in turn. Fifteen years of reading stances: weight, grip, breathing. She already knows how this ends."

    call nier_clear from _call_nier_clear_160
    stop music fadeout 1.0

    nier "She draws the sword."
    nier "It comes free of the wrappings with a sound that is not quite a ring and not quite a rasp -- something between the two, something that hangs in the air like a breath held and released."
    nier "No one moves for a full second."
    nier "The leader's eyes drop to the blade, and she can see the exact moment he understands what he is looking at -- not the length or the edge, but the quality of the steel, the quiet authority of a weapon forged for a war."
    nier "His jaw tightens."

    call nier_clear from _call_nier_clear_161
    play music blubird

    nier "The spearman moves first, off the wrong foot. She steps past the thrust, catches the shaft, and uses his momentum against him. He drops."
    nier "The two with short swords come together but not at the same time, which turns a dangerous combination into two separate problems. She handles them in sequence: a parried swing, a heel to a solar plexus, the flat of her blade against an open wrist."
    nier "The club man charges and swings overhead. She is already inside the arc."
    nier "The axeman watches all of this and turns and walks into the grass without looking back."

    call nier_clear from _call_nier_clear_162

    nier "The leader is the only one still standing."
    nier "He comes at her with genuine reach and a trained guard, and she gives him a few exchanges to measure the gap between his swings. When she finds it, she steps inside, catches the haft against her blade, and cuts it clean."
    nier "He looks at the broken stick in his hands."
    nier "\"Go,\" she says."
    nier "He goes."

    call nier_clear from _call_nier_clear_163
    stop music fadeout 1.0

    nier "She cleans the blade on her coat, wraps it, and steps over the men on the ground."
    nier "None of them were it. The sword is no closer to its ending than it was this morning."

    call nier_clear from _call_nier_clear_164

    nier "Later that day, as the sun slides toward the hills and the grass turns from gold to copper, she finds their camp."
    nier "She knows it is theirs because of the polearm heads -- three of them, leaning against a rock beside a blackened firepit. The same improvised craftsmanship. The same bent-nail fixings."

    call nier_clear from _call_nier_clear_165
    play music family

    nier "There is a woman sitting beside the dead fire."
    nier "She sits very still, hands in her lap. Her dress has been patched so many times the patches outnumber the original cloth. Her collarbones are sharp above the neckline."
    nier "Beside her, on a blanket spread over the bare ground, a boy sleeps. He is small -- four years old, maybe five. His face is flushed red and his breathing has the labored, wet quality of a chest cold that has gone untreated for too long."

    call nier_clear from _call_nier_clear_166

    nier "The woman looks up and sees the sword and does the same arithmetic the bandits did an hour ago, arriving at different answers."
    nier "\"You fought them,\" she says."
    nier "\"They'll live.\""
    nier "The woman's mouth tightens. She touches the boy's forehead with the back of her hand, an automatic motion, the gesture so practiced it belongs to the hand more than to her."

    call nier_clear from _call_nier_clear_167

    nier "\"The boy's sick,\" the woman says. Not a plea. A fact. Something about the weather."
    nier "The swordswoman looks at the boy."
    nier "She thinks about the six men she efficiently laid out in the grass an hour ago. About how little it cost her. About how that ease, that old practiced ease, has no application here at all."
    nier "His chest rises and settles with a faint, wet rattle."

    call nier_clear from _call_nier_clear_168

    nier "She reaches to her belt and unhooks the waterskin, crouches, and sets it beside the woman within arm's reach of the boy."
    nier "\"There's a village three days west,\" she says. \"The barkeep there will have a poultice, or know someone who does.\""
    nier "The woman stares at her."
    nier "\"That's all?\""
    nier "The swordswoman stands. The grass shifts around her knees."
    nier "\"That's all I have,\" she says."
    nier "She means it as a fact, but it lands as an admission."

    call nier_clear from _call_nier_clear_169

    nier "She walks east."
    nier "Behind her the boy coughs in his sleep, and the sound follows her across the plain for a long time -- long past the distance where she should be able to hear it, carried by something that has nothing to do with the wind."

    call nier_clear from _call_nier_clear_170
    pause 2.0

    # Attention check: Section IV
    nier "..."
    nier "I ask:"
    nier "At the bandits' camp, what did the swordswoman leave beside the boy?"

    menu (screen="nier_nvl_choice"):
        "A blanket.":
            jump cs_kotonoha_02_fail
        "Her sword.":
            jump cs_kotonoha_02_fail
        "A waterskin.":
            pass
        "Nothing.":
            jump cs_kotonoha_02_fail

    call nier_clear from _call_nier_clear_171

    nier "A waterskin. And a direction."

    # =================================================================
    #  V. The Heart of the Recess
    # =================================================================

    call nier_section("V. The Heart of the Recess") from _call_nier_section_13

    stop music fadeout 3.0
    pause 3.0
    play music sis_quiet

    scene black
    with dissolve_scene_full

    nier "She reaches it on the third day, and there is no border."
    nier "No wall, no threshold, no line in the earth she can point to. The grass simply thins, and the soil turns a darker shade, and the wind -- which has been her constant companion since she left the village -- stops."

    call nier_clear from _call_nier_clear_172

    nier "Not dies down. Stops. The air becomes motionless in a way that feels deliberate, as though it has withdrawn from this place and does not intend to come back."

    call nier_clear from _call_nier_clear_173

    show bg hollow zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "She stands at the edge of a circular clearing, perhaps two hundred paces across. The grass here has gone gray -- ash-gray, the color of something that has passed so far beyond burning that it no longer remembers heat."
    nier "At the center of the clearing there is an absence she can feel in her teeth."

    call nier_clear from _call_nier_clear_174

    nier "She is not the first person to come here."
    nier "The evidence is everywhere, once she starts looking. A ring of stones around an old firepit, the ashes long since scattered by rain. A pair of boots, cracked and empty, set neatly side by side at the clearing's edge as though someone meant to come back for them. A soldier's pack, moth-eaten, its straps cut and its contents removed. Scratches on a flat rock near the center: tally marks, names, a date from nine years ago."

    call nier_clear from _call_nier_clear_175

    nier "A wooden sword -- a child's training weapon, barely two feet long, jammed into the earth point-first. Someone carved a word into the hilt, but the grain has swollen with rain and sun until the letters are unreadable. It has been here for years."
    nier "Nearby, a medallion hangs from a stick driven into the ground: tarnished bronze, stamped with an insignia she recognizes. Third Division. The old man's unit, from the war."

    call nier_clear from _call_nier_clear_176

    nier "People have been coming here. Not a flood, but a steady trickle, year after year, drawn by the same word-of-mouth that moves through taverns and waystations and the long, quiet hours between midnight and dawn when former soldiers sit with drinks they don't remember ordering and say things they don't remember deciding to say."
    nier "{i}Three days east past the garrison. Into the hills. There's a place there. Go and see.{/i}"

    call nier_clear from _call_nier_clear_177

    nier "Each of them left something behind. Not all of them meant to."

    call nier_clear from _call_nier_clear_178

    nier "She walks toward the center, and each step takes more effort than the last -- not because the ground resists her or her legs are tired, but because something deep and old in her brain is pulling her backward, flooding her with the wordless conviction that the next step is the one she cannot undo."
    nier "She takes it anyway."

    call nier_clear from _call_nier_clear_179

    nier "She reaches the center and stands there."
    nier "The sword is on her back. She has not drawn it."
    nier "She turns, slowly, a full circle. Grass, sky, hills in the distance like faded brushstrokes. The boots. The pack. The wooden sword. The medallion. The tally marks on the stone."
    nier "No monster. No sealed evil. No final challenge."
    nier "Just a clearing full of the things other people couldn't carry anymore."

    call nier_clear from _call_nier_clear_180

    nier "She waits for an hour, and then another."
    nier "The light shifts from white to amber to the deep, heavy gold of early evening."

    call nier_clear from _call_nier_clear_181

    nier "She unslings the sword and holds it in front of her with both hands on the grip and the point aimed at the sky. The blade catches the last of the light and holds it."
    nier "She has been carrying this weapon for fifteen years, looking for the thing that would earn the right to be its final act. A demon king. A curse to break. A seal to close. Something large enough and terrible enough to justify a last clean stroke."
    nier "This clearing is not that thing."
    nier "Nothing will ever be that thing."

    call nier_clear from _call_nier_clear_182

    nier "She lowers the blade, sits down cross-legged in the gray grass with it across her knees."
    nier "And she stops, completely, with no intention left to resume."
    nier "She breathes, and the recess breathes with her, and the silence is the first honest silence she has sat inside in twelve years."

    call nier_clear from _call_nier_clear_183

    nier "What happens is not dramatic."
    nier "The quiet certainty that the next fight would be the meaningful one, that the next road would lead somewhere worth going, that the next village would offer a purpose worthy of this blade -- all of it loosens over the course of hours, as the gold light thins to gray and the first stars appear above the hills."
    nier "She watches them come out, one by one, and she thinks about the wooden sword planted in the earth behind her, and the word someone carved into its hilt that the weather erased."

    call nier_clear from _call_nier_clear_184

    nier "She thinks about Tan, slumped against the black stone wall. Orsin, mid-laugh. The boy in the valley with his shield too high."
    nier "She thinks about the boy in the grass, coughing."
    nier "She thinks about how long she has been walking, and how the sword on her knees has been the only answer she's had to every question the world has asked her, and how the world has stopped asking."

    call nier_clear from _call_nier_clear_185

    nier "The stars are all out now. The clearing is dark and still and holds her the way the earth holds a stone that has been lying in the same place for so long it has left an impression."
    nier "She sits there through the whole night, awake, with the blade across her knees and the objects left behind by strangers arranged around her in a rough, accidental circle."
    nier "She does not sleep."
    nier "She does not need to."
    nier "For the first time in twelve years, she is not going anywhere."

    call nier_clear from _call_nier_clear_186
    pause 2.0

    # Attention check: Section V
    nier "..."
    nier "I ask:"
    nier "Among the objects left behind by other visitors, there was a wooden sword."
    nier "What had someone carved into its hilt?"

    menu (screen="nier_nvl_choice"):
        "A name.":
            jump cs_kotonoha_02_fail
        "A prayer.":
            jump cs_kotonoha_02_fail
        "A word, but the weather had erased it.":
            pass
        "Nothing. The hilt was bare.":
            jump cs_kotonoha_02_fail

    call nier_clear from _call_nier_clear_187

    nier "A word. Swollen away by rain and sun."
    nier "Whatever it said, whoever carved it felt strongly enough to press a blade into wood."
    nier "And then they left it there, and walked away, and the weather took it."

    # =================================================================
    #  VI. The Road Back
    # =================================================================

    call nier_section("VI. The Road Back") from _call_nier_section_14

    stop music fadeout 3.0
    pause 2.0
    play music dream

    show bg town_day zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "She returns to the village on the sixth day."
    nier "The road is the same, and the sky is the same, and she had expected that at least one of them would have the decency to look different."

    call nier_clear from _call_nier_clear_188

    nier "She passes through the market square. The children are playing. The women are selling turnips. The old man is running his blade across the whetstone with a rhythm he has probably kept since before she was born."
    nier "Nobody stops. Nobody looks up."

    call nier_clear from _call_nier_clear_189

    nier "Halfway across the square, a man nearly collides with her."
    nier "He is younger than her -- mid-twenties, maybe. He has the build of someone who once had muscle and has since been whittled down by weeks of poor eating and hard walking. His clothes are patched. His eyes are the kind of tired that has nothing to do with sleep."
    nier "On his back, wrapped in cloth, is a sword."

    call nier_clear from _call_nier_clear_190

    nier "They both stop in their tracks."
    nier "He looks at the shape on her back, and she looks at the shape on his, and something passes between them that does not require introduction."
    nier "\"You're heading east,\" she says."
    nier "He nods."
    nier "\"Past the garrison. Into the hills.\""
    nier "\"Someone told me about it,\" he says. \"In a tavern, two towns back. He said there's a place--\""
    nier "\"There is.\""

    call nier_clear from _call_nier_clear_191

    nier "He waits for her to say more. She considers him -- the worn boots, the careful way he holds himself, the sword on his back that he carries with the same unconscious tension she recognizes from her own shoulders."
    nier "\"What did he tell you you'd find there?\" she asks."
    nier "\"An answer,\" he says."
    nier "\"To what?\""
    nier "He hesitates. His hand drifts toward the strap of his sword and then falls."
    nier "\"I fought in the border skirmish at Ohren. Two years ago. It lasted three days. They called it a skirmish because nobody wanted to call it a war.\""

    call nier_clear from _call_nier_clear_192

    nier "\"When I came back, everything was the same. The house, the town, my wife, the shop. All the same. And I couldn't--\""
    nier "He stops."
    nier "\"I couldn't put the sword down. I tried, I really did. I hung it over the hearth. I put it in the shed behind the house. I gave it to a blacksmith to melt. And yet...\""
    nier "\"Every time I went back for it within a week. My wife said I needed to see a healer. I said the sword was the only thing that still made sense.\""

    call nier_clear from _call_nier_clear_193

    nier "\"She left,\" he says. \"And, honestly, I don't fault her.\""
    nier "He looks at the swordswoman for a long moment."
    nier "\"The man in the tavern said people go to the recess and come back lighter. That they leave something behind. I want to leave...this behind.\""
    nier "He touches the strap on his shoulder."

    call nier_clear from _call_nier_clear_194

    nier "The swordswoman is quiet for a while."
    nier "The children behind her are screaming with laughter. A dog is barking. Turnips are being weighed on a rusted scale."
    nier "\"You won't find an answer there,\" she says."
    nier "His face changes."
    nier "\"Then what will I find?\""
    nier "She thinks about the clearing. The gray grass. The boots left by the edge. The wooden sword. The tally marks. The medallion. The night she spent awake with the stars coming out one by one over a place where the wind refused to go."

    call nier_clear from _call_nier_clear_195

    nier "\"A clearing,\" she says. \"Dead grass, old trinkets, that sort.\""
    nier "\"That's it?\""
    nier "\"...That's it.\""

    call nier_clear from _call_nier_clear_196

    nier "He stares at her, waiting for the rest of the sentence, the reassurance, the wisdom, the part where the older soldier tells the younger one that it gets easier."
    nier "She says nothing, because it doesn't, and she has never been someone who lies about things like that."

    call nier_clear from _call_nier_clear_197

    nier "\"Go anyway,\" she says, finally."
    nier "\"Why?\""
    nier "\"Because you came all this way.\""

    call nier_clear from _call_nier_clear_198

    nier "He looks at her for another long moment, and then he nods, and he adjusts the strap on his shoulder, and he turns east, and the crowd absorbs him, and he is gone."
    nier "She watches the space where he was."
    nier "She does not know his name. He does not know hers. Two people with swords they can't put down, meeting in a market square and then separating, their paths crossing for less than three minutes in a village that exists between other places."

    call nier_clear from _call_nier_clear_199

    nier "She finds the elder in the tavern, eating stew."
    nier "\"You're back,\" he says."
    nier "\"I'm back.\""
    nier "\"What did you find?\""

    call nier_clear from _call_nier_clear_200

    nier "She sits down across from him. The chair makes the same sound on the floor."
    nier "\"A clearing,\" she says. \"Dead grass, no wind, old campfires and things people left behind. It's not dangerous...just rather empty.\""
    nier "\"And?\""
    nier "\"And people keep going there for one reason or another.\""

    call nier_clear from _call_nier_clear_201

    nier "The elder sets down his spoon and looks at her for a long time."
    nier "\"The three we sent... They came back different.\""
    nier "\"They came back with less. That's a different thing than different.\""
    nier "He doesn't fully understand this, and she can see him choosing not to press it."

    call nier_clear from _call_nier_clear_202

    nier "\"You don't seem changed,\" he says, carefully."
    nier "\"No,\" she says. \"I don't seem changed.\""
    nier "He stirs the stew. \"...Will you stay for supper? The barkeep does a lamb stew on Tuesdays.\""
    nier "A beat, and then..."
    nier "\"...I'll stay.\""

    call nier_clear from _call_nier_clear_203

    nier "The stew is warm. The bread is fresh. The tavern fills slowly: farmers, tradespeople, a pair of teenagers holding hands under the table with the conviction that nobody can see them."
    nier "She sits in the corner and eats, and no one speaks to her, and no one avoids her."
    nier "She went somewhere and she came back and the world continued at exactly the pace it had been going."
    nier "She is not surprised."
    nier "She is not disappointed, either, and this is new."

    call nier_clear from _call_nier_clear_204
    pause 2.0

    # Attention check: Section VI
    nier "..."
    nier "I ask:"
    nier "In the market square, she met a young man heading east."
    nier "What did he say the sword was to him?"

    menu (screen="nier_nvl_choice"):
        "A weapon.":
            jump cs_kotonoha_02_fail
        "A burden.":
            jump cs_kotonoha_02_fail
        "The only thing that still made sense.":
            pass
        "A gift from his father.":
            jump cs_kotonoha_02_fail

    call nier_clear from _call_nier_clear_205

    nier "The only thing that still made sense."
    nier "She understood that better than she could have explained."

    # =================================================================
    #  VII. The River
    # =================================================================

    call nier_section("VII. The River") from _call_nier_section_15

    stop music fadeout 4.0
    pause 4.0
    play music hollow

    show bg river zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "She leaves the village at dawn the very next morning."
    nier "No one sees her go. The stable loft is empty when the barkeep's boy arrives to feed the horses, and the only evidence she was ever here is a door that hangs straight on its hinge and a cup, washed, placed upside down on the counter."

    call nier_clear from _call_nier_clear_206

    nier "She does not take the road she came in on."
    nier "She walks east instead, through a thin wood of pines, following a sound she has been hearing since she arrived but only now has stopped ignoring."

    call nier_clear from _call_nier_clear_207

    nier "The river is barely a river -- more a wide stream, shallow enough to wade across, running over stones the color of old bronze. The water catches the early light and breaks it into moving shapes that shift and overlap and refuse to settle."

    call nier_clear from _call_nier_clear_208

    nier "There is a flat rock at the water's edge, broad enough to sit on, smoothed by decades of current. Someone has been here before her -- there are the faint remains of a fire between two stones, and a mark scratched into the rock's surface. An arrow, pointing east. Below it, worn almost invisible: the word {i}further{/i}."
    nier "Someone sat here and couldn't decide whether to go on or to stop, and they left a message for the next person, and the next person was her."

    call nier_clear from _call_nier_clear_209

    nier "She stands at the bank with the sword on her back."
    nier "She has carried it for fifteen years. Three years of war and twelve years of looking for what the war should have ended with. It was forged for a purpose, and she has been unable to let it rest without a purpose, because to put it down without a final act would mean that all the years and all the blood and all the corridors and all the men she killed led to nothing."
    nier "Every road she walked, she was looking for the thing that would earn the right to be its last stroke."
    nier "The Recess had no such thing."
    nier "The road had no such thing."
    nier "She is beginning to understand that nothing will."

    call nier_clear from _call_nier_clear_210

    nier "She reaches back and unhooks the strap and slides the sword off her shoulder."
    nier "It is heavier than it has been in years, though the steel hasn't changed. What's changed is that she can feel the weight again. In the recess she stopped pretending it was light."

    call nier_clear from _call_nier_clear_211

    nier "She holds it in front of her."
    nier "The wrappings are loose. A strip of cloth hangs from the hilt."
    nier "She thinks about the wooden sword planted in the gray earth of the clearing, and the word carved into it that the weather had taken. She thinks about the young man in the market square, heading east with the same weight on his back and the same look behind his eyes."
    nier "She thinks about Tan, who never made it out of the third corridor. Orsin, who died between one laugh and the next. The boy in the valley, who looked at her and understood and then stopped understanding."

    call nier_clear from _call_nier_clear_212

    nier "She thinks about the forge where this blade was made. She has not been there in fifteen years, but she can picture the smith -- an old woman with burn-scarred hands who worked in silence and tested every blade by holding it up to the light and looking along the edge the way a musician listens to a tuning fork."
    nier "The old woman made this sword for the war. She didn't make it for what came after. She didn't make it to be carried down empty roads by a woman who couldn't find a reason to set it down."

    call nier_clear from _call_nier_clear_213

    nier "The swordswoman kneels at the water's edge."
    nier "She places the blade across the flat rock, beside the scratched arrow and the word {i}further{/i}."
    nier "There is no ceremony. She doesn't plunge it into the earth or cast it into the current or raise it to the sky for one last salute."
    nier "She puts it down."

    call nier_clear from _call_nier_clear_214

    nier "Her hands stay on the grip for a long time."
    nier "This is the hardest part. Not the decision, but the follow-through. The moment where her fingers have to open and the weight has to leave her palms and she has to sit there with nothing in her hands for the first time in fifteen years."

    call nier_clear from _call_nier_clear_215

    nier "She lets go."

    call nier_clear from _call_nier_clear_216

    nier "The sword lies on the rock. The morning light moves across the steel, slow and uneven, broken by the shifting water into patterns that do not repeat."
    nier "Her hands are in her lap. They are shaking, a fine tremor she hasn't felt since the first battle, when her body didn't yet know how to absorb the aftermath."

    call nier_clear from _call_nier_clear_217

    nier "She sits there."
    nier "The stream runs past. A bird calls from somewhere in the pines -- the first sound she has heard in this wood that wasn't her own footsteps."
    nier "She looks at the water. Her reflection is there, broken by the current into shifting pieces, a face she has not studied in a long time."

    call nier_clear from _call_nier_clear_218

    nier "She could name everything she has been. Recruit, soldier, killer, survivor, wanderer."
    nier "The list would describe a shape without telling you who lived inside it."

    call nier_clear from _call_nier_clear_219

    nier "Between one ripple and the next, there is a moment where the water stills -- briefly, improbably -- and the face in the stream holds together."
    nier "She doesn't recognize it."
    nier "Not a stranger's face. Not a memory. Something that has not been finished yet, and might never be, and she sits with that, and the stream resumes, and the face breaks apart again."

    call nier_clear from _call_nier_clear_220

    nier "Behind her, the sword lies on the rock. She can feel the absence of it on her back -- a lightness that is not relief, not yet. Just unfamiliar."
    nier "Ahead of her, the stream runs east, through the trees, into the hills, toward a hollow where other people have left the things they couldn't carry."

    call nier_clear from _call_nier_clear_221

    nier "She stays for a long time."
    nier "The sun climbs. The light changes. The shadows of the pines rotate slowly across the grass."
    nier "Somewhere far to the west, a boy coughs and a woman holds a waterskin. Somewhere to the east, a young man with a sword walks toward a clearing he won't understand until he sits in it."
    nier "Somewhere on a plateau, an old man peels an apple and watches the birch trees and waits for the next person heading east."

    call nier_clear from _call_nier_clear_222

    nier "She thinks about picking the sword back up."
    nier "The thought arrives and she lets it sit there, the same way she let the silence sit in the recess -- without fighting it, without giving in to it."
    nier "She just sits with it."

    call nier_clear from _call_nier_clear_223

    nier "The stream runs past."
    nier "The bird calls again."
    nier "She opens her hands, palms up, on her knees. They are still shaking."
    nier "She does not close them."

    call nier_clear from _call_nier_clear_224
    scene black with dissolve_scene_full
    pause 3.0

    stop music fadeout 5.0
    pause 5.0

    $ persistent.cs_kotonoha_02_unlocked = True
    # The real ending. The attention-check failure below is not one.
    $ cs_mark_completed("cs_kotonoha_02")

    call nier_exit from _call_nier_exit_2
    return


# =============================================================================
#  Attention Check Failure
# =============================================================================

label cs_kotonoha_02_fail:
    call nier_clear from _call_nier_clear_225
    pause 1.0
    nier "..."
    nier "You weren't listening."
    nier "No one ever does."
    pause 2.0
    call nier_exit from _call_nier_exit_3
    return
