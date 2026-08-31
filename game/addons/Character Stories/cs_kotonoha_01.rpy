# =============================================================================
# cs_kotonoha_01.rpy  --  Kotonoha character story 01, "The Girl with Every Face"
# =============================================================================
#
# Uses the Nier Replicant Text Adventure format.
# A deconstruction of the fairy tale trope "The X with no Y."
# Instead of lacking something, the girl has too much of it --
# every face, every role, every self but her own.
#
# WIRING / MECHANICS
#   Registered in char_stories.rpy as CharacterStoryEntry("The Girl with Every
#   Face", ..., "cs_kotonoha_01", "cs_kotonoha_01_unlocked"); reached via the hub
#   PLAY button -> Start("cs_kotonoha_01").
#
#   Nier mode (all defined in addons/Nier Forest Text Adventure Format/nier_text_adventure.rpy):
#     call nier_enter      -> fade to black, disable quick_menu, enter NVL prose mode
#     call nier_section(t) -> clear text + show a centered title card for section t
#     nier "..."           -> the `nier` NVL character; prose accumulates on screen
#     call nier_clear      -> nvl clear without leaving the mode (new "page")
#     call nier_exit       -> clear text, restore quick_menu, leave the mode
#   Choices use `menu (screen="nier_nvl_choice")` (custom choice screen, same file).
#
#   ATTENTION CHECKS: each section ends with a multiple-choice "I ask:" menu.
#   Wrong answers `jump cs_kotonoha_01_fail` (bottom of file) -> short rebuke,
#   nier_exit, return. The correct answer falls through (`pass`) and continues.
#
#   WHY THEY EJECT YOU  (they are not a difficulty knob, and not a morality test)
#   Straight homage to Nier Replicant, which does exactly this to its reader.
#   Their working purpose is to catch the two people this story cannot survive:
#   the one holding down skip, and the one who walked away with it running.
#   Both are answered the same way -- the narrator stops telling it. That is
#   the joke and the point: a story about a girl nobody actually listened to
#   declines to keep going for someone who isn't listening.
#     - The questions are deliberately about HER, never about plot mechanics --
#       what was behind her eyes, the word the old man kept returning to.
#     - The rebuke is two lines and it is aimed at the reader in the room, not
#       at anyone's morals. It is not an ending; :1056 marks the real one and
#       notes that this isn't it, so a failed check never sets cs_mark_completed.
#     - Keep them cheap to recover from. A reader who was genuinely present has
#       nothing to fear from any of the seven.
#
#   ON COMPLETION: sets persistent.cs_kotonoha_01_unlocked, awards the
#   "No One Lived There" CG, marks the story completed, then nier_exit + return.
# =============================================================================

label cs_kotonoha_01:
    stop music fadeout 1.0

    call nier_enter from _call_nier_enter

    call nier_section("The Girl with Every Face") from _call_nier_section

    # =================================================================
    #  Prologue -- The Town That Loved Her
    # =================================================================

    nier "There was once a girl that everyone loved."
    nier "This is not the unusual part. Children are loved all the time, in small towns with not much else to do."
    nier "Children, big and small, rich and poor, all eventually grow up and become who they want to be."
    nier "..."
    nier "There was once a girl that everyone loved."

    call nier_clear from _call_nier_clear
    play music seafront
    pause 2.0

    nier "She lived in a town pressed between mountains and sea, where the winters were long and the summers smelled of salt."
    nier "It was a small town: everyone knew everyone, gossip traveled faster than weather, and children grew up at the pace of trees."
    nier "The girl was, by all accounts, a perfectly normal child."
    nier "She had two hands and two eyes and a smile that made the old women at the market coo and pinch her cheeks."
    nier "She said please and thank you."
    nier "She ate her vegetables."
    nier "She never complained about the cold."

    call nier_clear from _call_nier_clear_1

    nier "But there was something about her that people noticed without being able to name."
    nier "When the baker's wife talked about her, she said: \"That girl has the kindest heart I've ever seen in a child.\""
    nier "When the retired postman talked about her, he said: \"Sharp as a tack, that one. She'll go far.\""
    nier "When the woman who kept the shrine talked about her, she said: \"She has old eyes. Like she's already lived a long time.\""
    nier "They all nodded when the others spoke, each one certain they were describing the same child."

    call nier_clear from _call_nier_clear_2

    show bg park_winter zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "The girl, clad in her white dress and gray coat, stands before a frozen lake."
    nier "She is eight years old."
    nier "The year is just beginning, and the ice is thick enough to hold the weight of a grown man, let alone a girl who barely reaches the counter at the convenience store."
    nier "She stands very still, looking out across the white expanse."
    nier "If you watch her face, you can see something working behind her eyes: a calculation, a decision, a door opening to a room she hasn't entered yet."
    nier "She takes one step onto the ice."

    call nier_clear from _call_nier_clear_3

    # Attention check: Prologue
    nier "..."
    nier "I ask:"
    nier "What did I say was working behind her eyes?"

    menu (screen="nier_nvl_choice"):
        "Nothing. Her face was perfectly still.":
            jump cs_kotonoha_01_fail
        "A calculation, a decision, a door opening.":
            pass
        "Curiosity. The pull of the ice.":
            jump cs_kotonoha_01_fail
        "Fear, held carefully in place.":
            jump cs_kotonoha_01_fail

    call nier_clear from _call_nier_clear_4

    nier "Good. You were listening."
    nier "Not everyone does."

    scene black with dissolve

    # =================================================================
    #  I. The Skater
    # =================================================================

    call nier_section("I. The Skater") from _call_nier_section_1

    show bg park_winter zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "She asked her mother for skates on New Year's Day."
    nier "She didn't beg or bargain or cry. She walked into the kitchen where her mother was chopping carrots and said:"
    nier "\"I'd like a pair of ice skates, please.\""
    nier "Her mother looked at her. She was someone who noticed things and kept them to herself, patient about it, unhurried."
    nier "\"What for?\" she asked."
    nier "\"I'd like to skate,\" the girl said."
    nier "Her mother bought her the skates the next day."

    call nier_clear from _call_nier_clear_5

    nier "The lake behind the old shrine froze every winter from December through February."
    nier "It was a modest lake, no wider than a city block, ringed by bare elms and a wooden railing that had been repainted so many times no one could remember its original color."
    nier "The townspeople skated on it casually through the winter months. Couples on dates. Children chasing each other. Old men who had been skating since before the war and refused to stop."
    nier "The girl went alone, before dawn, when the ice was still blue with early light and the only sound was the creak of her own weight on the frozen surface."

    call nier_clear from _call_nier_clear_6

    nier "She fell nine times on the first morning."
    nier "She didn't cry. She didn't curse. Each time, she set her hands flat on the ice, pushed herself up, and tried again."
    nier "Each fall was a step in the process, no different from lacing the skates or tying her hair."
    nier "By the fifth morning, she could glide in a straight line without stopping."
    nier "By the tenth, she could turn."
    nier "By the fifteenth, she could cross the full length of the lake with her arms outstretched, tracing slow arcs through the freezing air."

    call nier_clear from _call_nier_clear_7

    nier "She learned from a VHS tape."
    nier "Her mother found her watching it one evening: a recording of the Winter Olympics, the women's figure skating final. The girl had been replaying the same three-minute routine for over an hour."
    nier "\"She's beautiful,\" the girl said, without looking away from the screen."
    nier "Her mother sat down on the couch behind her and watched the skater on the tape complete a triple axel in slow motion."
    nier "\"Do you want to be like her?\" her mother asked."
    nier "The girl tilted her head, as if the question didn't quite make sense."
    nier "\"I want to do what she does,\" she said. \"That's different.\""

    call nier_clear from _call_nier_clear_8

    nier "A woman named Uchida lived at the edge of town, in a house with a persimmon tree in the yard that never bore fruit."
    nier "She had been a figure skating coach in Sapporo thirty years ago, before her knees and a long argument with time forced her into retirement."
    nier "She saw the girl skating one morning while walking her dog, and stood at the railing for forty-five minutes without moving."
    nier "Later that day, she knocked on the girl's door."
    nier "\"Your daughter,\" she said to the mother. \"I'd like to teach her. No charge.\""
    nier "The mother looked at her for a long moment, then nodded."

    call nier_clear from _call_nier_clear_9

    nier "Under Uchida's guidance, the girl improved at a pace that made the old woman's hands tremble with recognition."
    nier "Gifted children leap ahead, skip steps, arrive somewhere dazzling and barely explain how. She did none of this."
    nier "She absorbed everything."
    nier "She watched Uchida demonstrate a technique once, twice, three times, and then reproduced it with a fidelity that was almost unsettling. A copy, down to the angle of the wrist, the tilt of the chin, the timing of the breath."
    nier "\"You're very observant,\" Uchida told her one morning."
    nier "The girl smiled. \"Thank you.\""

    call nier_clear from _call_nier_clear_10

    nier "February came. The days grew longer but the cold held."
    nier "One morning, Uchida asked the girl to show her everything she'd learned. No routine, just movement. Whatever she felt like."
    nier "The girl skated to the center of the lake and stood still for a moment."
    nier "Then she began to move."

    call nier_clear from _call_nier_clear_11

    nier "She traced a figure eight. Slow at first, then faster, her body leaning into the curves with a precision that belied her age."
    nier "She added spins. Turns. Small jumps that clicked against the ice like punctuation marks."
    nier "She was searching for something underneath."
    nier "She had been searching since the first morning on the ice, and she had named it to herself only once, after watching the tape for the third time: the skater moved as though the movement had a source somewhere deep in the body that the girl hadn't found yet. The form was right. She could reproduce it. The result was still not the same."
    nier "She skated the length of the lake with her arms out, feeling for it."
    nier "The ice held. The air was cold. Her body did everything asked of it."
    nier "Nothing came."

    call nier_clear from _call_nier_clear_12

    nier "When she stopped, Uchida was sitting on the bench by the railing, her dog asleep at her feet."
    nier "\"What do you see when you skate?\" Uchida asked."
    nier "The girl thought about this for a long time."
    nier "She thought about the tape. The triple axel in slow motion. The skater's face in the middle of the rotation, unguarded, something present that the girl couldn't locate in herself no matter how closely she reproduced the form."
    nier "\"I don't know,\" she said. \"Something.\""
    nier "She meant it exactly as she said it: a plain report from a search that had not found its object."
    nier "Uchida waited. Nothing else came."

    call nier_clear from _call_nier_clear_13

    nier "The ice thawed in March."
    nier "One morning the girl stood at the railing and watched dark water moving through a crack that had opened in the night, pushing the ice apart from beneath."
    nier "Her reflection was in the dark water. She noticed it, then looked at the ice instead."
    nier "She went to see Uchida."
    nier "She bowed. Uchida received the bow with the stillness of someone who had been expecting it."
    nier "\"You'll come back in December,\" Uchida said. It was not quite a question."
    nier "The girl considered this honestly."
    nier "\"I don't think so,\" she said."
    nier "She walked home."
    nier "The thing she had been looking for had not appeared. She knew it as she knew a blade's edge — not from experience, but from something faster."
    nier "She would look elsewhere."

    call nier_clear from _call_nier_clear_14

    # Attention check: Section I
    nier "..."
    nier "I ask:"
    nier "How many times did the girl fall on her first morning on the ice?"

    menu (screen="nier_nvl_choice"):
        "Three.":
            jump cs_kotonoha_01_fail
        "Five.":
            jump cs_kotonoha_01_fail
        "Nine.":
            pass
        "Twelve.":
            jump cs_kotonoha_01_fail

    call nier_clear from _call_nier_clear_15

    nier "Nine times."
    nier "She kept count without thinking about it."

    # =================================================================
    #  II. The Fighter
    # =================================================================

    call nier_section("II. The Fighter") from _call_nier_section_2

    stop music fadeout 2.0
    pause 2.0
    play music stone

    show bg bus_interior zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "July. Cicadas in the trees like static on an untuned radio."
    nier "The girl is ten years old."

    call nier_clear from _call_nier_clear_16

    nier "The girl stands in a training hall on the far side of the river, next to the slot arcade that the town council has been trying to shut down for years."
    nier "She wears a white training uniform. Her hair is tied back with a rubber band."
    nier "She is barefoot on the wooden floor, and her feet make no sound when she moves."
    nier "She has been practicing taekwondo for five months."

    call nier_clear from _call_nier_clear_17

    nier "The gym is run by an old man named Ogata."
    nier "He is short, wide, and has a face like a landslide, everything settling slowly downward. His eyebrows are thick and gray, and his hands are the size of dinner plates."
    nier "He has been teaching taekwondo for forty years. He has produced regional champions, national qualifiers, and one Olympic alternate who sends him a New Year's card every January."
    nier "He has never seen anyone learn quite like this."

    call nier_clear from _call_nier_clear_18

    nier "She doesn't ask questions. She watches."
    nier "Ogata demonstrates a technique, a roundhouse kick or a spinning back kick or a knife-hand strike, and the girl watches with an intensity that is almost physical, as if her eyes are hands and she is taking the movement apart at the joints."
    nier "Then she reproduces it."
    nier "The result is never perfect right away, but close enough that the corrections he offers are minor: angle the hip two degrees, extend the knee a fraction further, breathe out on the strike instead of before it, adjustments that would take most students months to internalize."
    nier "She makes them once and never forgets."

    call nier_clear from _call_nier_clear_19

    nier "Her seniors watch her with a mixture of admiration and something they can't quite name."
    nier "The eldest, a boy of thirteen who has trained here since he was six, tells his mother one evening: \"There's a new girl at the gym. She's ten.\""
    nier "\"Is she good?\" his mother asks."
    nier "He thinks about this for a while."
    nier "\"She's...fast.\""
    nier "This isn't quite what he means, but it's the closest word he has."

    call nier_clear from _call_nier_clear_20

    nier "What he means is this: when the girl spars, Ogata sees something shift in her."
    nier "During drills, she is composed, precise, polite: bowing when addressed, yielding the floor to her seniors without hesitation. The model student of a model form."
    nier "But in the ring, her eyes change."
    nier "This is what Ogata watches for, from his chair in the corner, one leg crossed over the other, his tea going cold. The moment the change happens. He has been watching it every session since the fourth week, and he still cannot say exactly when it occurs, only that it does, and that something in him is troubled by it in a way he cannot name."
    nier "They go flat, emptied of everything. Like something watched from behind glass."
    nier "Her strikes come from angles that shouldn't be possible for someone her size. She reads her opponent's weight shifts a half-second before they commit, and she is already moving."
    nier "Afterward she bows, and whatever was behind her eyes recedes, and she is the model student again."

    call nier_clear from _call_nier_clear_21

    nier "Ogata has seen gifted students."
    nier "Students who moved as though the form had been waiting in their bodies since birth. Students who wept with frustration and then one morning stopped weeping because something had clicked, finally, and the movement belonged to them."
    nier "Students who fought the way some people speak: every motion shaped by a grammar that was theirs alone."
    nier "This girl is not that."
    nier "What she does is correct. More than correct. She takes what he shows her and gives it back at a fidelity that is, he decides after weeks of searching for the right word, unsettling. A reflection that moves half a second after you do."
    nier "The word he keeps arriving at is {i}pretend{/i}."
    nier "He turns it over longer than he should. Forty years in this room. He has found words for everything a student can be, and the best he can manage for her is {i}pretend{/i}, which is not unkind, exactly, just incomplete. A word for what she does rather than what she is."
    nier "He cannot think of a better one."

    call nier_clear from _call_nier_clear_22

    nier "August. The local tournament."
    nier "Ogata sits in the far corner of the gymnasium from the first match to the last."
    nier "She wins five. Each opponent dispatched with the same clean efficiency — {i}efficient{/i} being another word that doesn't fully satisfy him, though it is accurate. She bows after each match at the same angle, for the same duration. The gymnasium fills and empties around her and she remains constant."
    nier "After the final, a woman from the regional athletic board finds the girl's mother at the edge of the floor."
    nier "Ogata cannot hear the conversation from where he sits, but he does not need to. He watches the mother's face — careful, measuring — and then the girl's, folding her uniform on the bench with the focused attention she gives to anything that requires her hands."
    nier "\"You'd have to ask her,\" the mother says."

    call nier_clear from _call_nier_clear_23

    nier "They don't ask."
    nier "By September, the girl has stopped coming."
    nier "Ogata is not surprised."
    nier "He finishes his barley tea, washes the cup, and places it back on the shelf where it always sits. He locks the door, and walks home."
    nier "When his eldest student asks about her, Ogata says nothing for a long time."
    nier "Then: \"She was looking for something here and she didn't find it. That's not our failure or hers.\""
    nier "The boy doesn't understand."
    nier "Ogata doesn't expect him to."

    call nier_clear from _call_nier_clear_24

    nier "The word he uttered back then stays with him."
    nier "He is still carrying it in March, when the first warm days come and the tournament trophy she left on the gym shelf catches the light through the east-facing window."
    nier "She left without taking it. He is not sure if she forgot, or if it simply didn't occur to her that it was hers."
    nier "This bothers him. Small things have that tendency, once you understand they were larger than they first appeared."
    nier "He thinks: she liked being good at it."
    nier "He tries to remember if she ever said she liked it."
    nier "He cannot."

    call nier_clear from _call_nier_clear_25
    pause 2.0

    # Attention check: Section II
    nier "..."
    nier "I ask:"
    nier "What was the word the old man kept returning to?"

    menu (screen="nier_nvl_choice"):
        "{i}Beautiful.{/i}":
            jump cs_kotonoha_01_fail
        "{i}Fast.{/i}":
            jump cs_kotonoha_01_fail
        "{i}Pretend.{/i}":
            pass
        "{i}Skilled.{/i}":
            jump cs_kotonoha_01_fail

    call nier_clear from _call_nier_clear_26

    nier "{i}Pretend.{/i}"
    nier "That was his word for it."

    # =================================================================
    #  III. The Model Student
    # =================================================================

    call nier_section("III. The Model Student") from _call_nier_section_3

    stop music fadeout 2.0
    pause 2.0
    play music dream

    show bg class_day zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "She is twelve."
    nier "The light through the classroom window is the color of weak tea, tepid, neither morning nor afternoon, the particular atmosphere schools generate on their own."

    call nier_clear from _call_nier_clear_27

    nier "The girl sits in the second row, third seat from the window."
    nier "She chose this seat on the first day of the term, and no one thought to question it."
    nier "It is the optimal seat. Close enough to the teacher to demonstrate attentiveness, far enough to avoid the appearance of eagerness, near enough to the window for natural light but not so close that she'd be accused of daydreaming."
    nier "She didn't calculate this. Or if she did, it happened so quickly and so far below the surface that it looked like coincidence."

    call nier_clear from _call_nier_clear_28

    nier "She is the top student in her year."
    nier "Not by a narrow margin. Her scores sit above the second-place student by a gulf wide enough to be quietly embarrassing for everyone else."
    nier "She achieves this without apparent effort. She is never seen studying in the library. She doesn't use flashcards. She doesn't highlight her textbooks."
    nier "She simply listens, watches, and absorbs."

    call nier_clear from _call_nier_clear_29

    nier "She is class representative."
    nier "She organizes the autumn festival booth: a haunted house that the class votes for unanimously, because the girl presents the idea with such calm authority that dissent feels unnecessary."
    nier "She mediates a dispute between two boys who have been feuding since elementary school. By lunch, they're sharing a bag of noodle rolls and looking slightly dazed, as if they can't remember what they were angry about."
    nier "She tutors three students in math. All three improve by at least one letter grade."
    nier "She joins the art club in the spring term, the science club in summer, and the choir in autumn."

    call nier_clear from _call_nier_clear_30

    nier "She is, to use the word that appears in her homeroom teacher's evaluation, \"exceptional.\""
    nier "The full sentence reads: \"A student of exceptional ability and character. She elevates every room she enters.\""
    nier "The teacher writes this proudly, underlines it, and files the evaluation with a sense of satisfaction."

    call nier_clear from _call_nier_clear_31

    nier "There are things the teacher does not notice."
    nier "The girl eats lunch at the far end of a long table in the cafeteria, adjacent to groups of classmates but never embedded in them. From a distance, she appears to be among friends. Up close, the gap becomes visible."
    nier "She never raises her hand unless called upon."
    nier "She answers questions with precision and depth, but she never asks one."
    nier "In three years of teaching, the homeroom teacher will realize much later, upon quiet reflection, that she cannot recall a single instance of the girl asking a question, about lessons or homework or anything at all."
    nier "But she will only realize this much later. And by then, the girl will have moved on."

    call nier_clear from _call_nier_clear_32

    nier "In October, the girl writes an essay for her literature class."
    nier "The prompt is broad: \"Write about an object that tells a story.\""
    nier "The girl writes about a house."
    nier "A house at the edge of a village, beautiful on the outside: fresh paint, flowers in the window box, a welcome mat worn soft at the edges."

    call nier_clear from _call_nier_clear_33

    nier "Inside, every room is empty. There is no furniture, no photographs, no marks on the walls where things once hung."
    nier "In the essay, visitors come from all over to admire the house. Each one describes it differently. One calls it warm. One calls it grand. One calls it humble."
    nier "None of them go inside."

    call nier_clear from _call_nier_clear_34

    nier "The essay ends with a line that the teacher reads twice:"
    nier "\"{i}The house stood for a hundred years, and everyone agreed it was beautiful, and no one ever lived there.{/i}\""
    nier "The teacher writes in the margin: \"Beautiful writing. A touch melancholy for someone your age.\""
    nier "The girl reads the comment and nods."
    nier "Her next essay is about sunflowers."
    nier "The teacher gives it full marks and doesn't think about the house again."

    call nier_clear from _call_nier_clear_35
    pause 2.0

    # Attention check: Section III
    nier "..."
    nier "I ask:"
    nier "What did the teacher write in the margin of the girl's essay?"

    menu (screen="nier_nvl_choice"):
        "\"Excellent work. Your best this term.\"":
            jump cs_kotonoha_01_fail
        "\"Beautiful writing. A touch melancholy for someone your age.\"":
            pass
        "\"Interesting premise. I'd like to discuss this with you.\"":
            jump cs_kotonoha_01_fail
        "\"Strong voice, but a little too clever for its own good.\"":
            jump cs_kotonoha_01_fail

    call nier_clear from _call_nier_clear_36

    nier "\"A touch melancholy.\""
    nier "She underlined it and filed it away."

    # =================================================================
    #  IV. The Mosaic
    # =================================================================

    call nier_section("IV. The Mosaic") from _call_nier_section_4

    stop music fadeout 3.0
    pause 3.0
    play music devola

    show bg residential_day zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "Here is what the people remember."
    nier "Listen closely."

    call nier_clear from _call_nier_clear_37

    # -- An old woman --
    nier "An old woman, seventy-three, sitting in her kitchen with a cup of tea that has gone cold:"
    nier "\"She was the most dedicated student I ever had. Every morning before dawn. First to arrive, last to leave. She never complained. She never asked for praise. She just...worked.\""
    nier "\"I've taught children who went on to do great things. None of them had her focus. Not a single one.\""

    call nier_clear from _call_nier_clear_38

    nier "\"I still don't understand why she stopped. One morning she came to me and bowed. That careful, perfect bow — you know the one. And then she was gone.\""
    nier "\"I asked her mother about it. Her mother said, 'She's found something new.' As if a child's passion is a season. Something that passes.\""
    nier "\"Maybe she was right. Maybe I just didn't want her to be.\""

    call nier_clear from _call_nier_clear_39

    # -- An old man --
    nier "An old man, sitting alone in an empty hall in late afternoon, one hand resting on his knee:"
    nier "\"Strong. Quick.\""
    nier "\"She understood the form before I finished showing it. A natural?\""
    nier "\"No.\""
    nier "\"Something else.\""
    nier "\"What bothered me is she never did it for herself. Everything I taught her, she did it right. But there was no...\""
    nier "He stops."
    nier "\"...no {i}her{/i} in it.\""
    nier "\"When she left, I wasn't surprised.\""

    call nier_clear from _call_nier_clear_40

    # -- A classmate --
    nier "A classmate, now fourteen, sitting on the school steps, picking at a loose thread on her skirt:"
    nier "\"She was so nice? Like, she helped me with math once, I was completely lost, and she stayed for an hour after school and just explained it until it made sense. And she knew everyone's birthday. I never even told her mine.\""
    nier "\"She was like...the perfect friend? That sounds weird when I say it out loud.\""

    call nier_clear from _call_nier_clear_41

    nier "She goes quiet for a moment, pulling at the thread."
    nier "\"Actually, wait. I don't think she ever told me anything about herself. Like, anything. I talked and talked and she just...listened.\""
    nier "\"I don't know her favorite color. I don't know what she listens to. I don't even know if she has a favorite anything.\""
    nier "\"That's weird, right? Two years and I can't tell you one thing she said about herself. That's really weird.\""

    call nier_clear from _call_nier_clear_42

    # -- The homeroom teacher --
    nier "The homeroom teacher, at her desk, grading papers, speaking without looking up:"
    nier "\"Remarkable student. Truly remarkable. You don't forget one like her.\""
    nier "\"Test scores: exceptional. Conduct: flawless. Peer relations: universally positive. She elevated the entire classroom just by being present.\""
    nier "\"But she never once raised her hand. I only noticed this recently. She answered when called on, perfectly, but she never volunteered.\""
    nier "\"And she never asked a question. About anything. In three years.\""
    nier "The pen stops."
    nier "The teacher looks up for the first time."
    nier "\"...Hm.\""

    call nier_clear from _call_nier_clear_43

    # -- Her mother --
    nier "And her mother."
    nier "Standing at the kitchen counter, peeling a potato with slow, careful strokes, not looking at anything in particular:"
    nier "\"She was always a good child.\""
    nier "\"She never gave us trouble, never threw tantrums, never rebelled. She did what was asked of her and more. She made us proud in every way a child can.\""

    call nier_clear from _call_nier_clear_44

    nier "A long silence. The peeling continues."
    nier "\"But sometimes, late at night, I'd walk past her room and hear...nothing.\""
    nier "\"A different kind of nothing: someone being very, very still while wide awake.\""
    nier "\"And I'd open the door, just a crack, and she'd be sitting on her bed, staring at the wall with her hands in her lap. She wasn't asleep or upset. She was just somewhere else, I think.\""

    call nier_clear from _call_nier_clear_45

    nier "\"And when she noticed me, she'd turn, and just smile.\""
    nier "\"...You know the one.\""
    nier "\"The same smile she gives everyone.\""

    call nier_clear from _call_nier_clear_46

    nier "The potato is peeled. The mother sets down the knife."
    nier "\"I'd close the door and tell myself it was nothing.\""
    nier "\"...\""
    nier "\"Sometimes I wonder if that was the most honest she ever was. And I just kept closing the door on it.\""

    call nier_clear from _call_nier_clear_47
    pause 2.0

    # Attention check: Section IV
    nier "..."
    nier "I ask:"
    nier "What did the girl's mother hear outside her daughter's room at night?"

    menu (screen="nier_nvl_choice"):
        "Smiling.":
            jump cs_kotonoha_01_fail
        "Music.":
            jump cs_kotonoha_01_fail
        "Nothing.":
            pass
        "Talking.":
            jump cs_kotonoha_01_fail

    call nier_clear from _call_nier_clear_48

    nier "Nothing."
    nier "A different kind of nothing."

    # =================================================================
    #  V. The Ghost
    # =================================================================

    call nier_section("V. The Ghost") from _call_nier_section_5

    stop music fadeout 2.0
    pause 2.0
    play music sis_quiet

    show bg doordark zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "She is fourteen."
    nier "It is October. The ginkgo trees along the school path have turned gold and are shedding their fan-shaped leaves onto the pavement like scattered coins."
    nier "The girl walks to school."
    nier "She is in her last year of middle school, and she has recently become aware of something she does not have a word for."

    call nier_clear from _call_nier_clear_49

    nier "She noticed it first in June, reviewing for end-of-term exams, when she looked at the trophies on the shelf and felt nothing she could locate as her own."
    nier "Not pride or indifference; something closer to mild confusion, as if the objects had been placed there by someone who expected them to mean more than they did."
    nier "She took one down and turned it over. First place, district tournament. She had won it cleanly, efficiently, and then stopped coming."
    nier "She had done the same with the ice. The gym. Every club since."
    nier "She put the trophy back. What bothered her was that it bothered her less than it should."

    call nier_clear from _call_nier_clear_50

    nier "The corridor greets her the same as any other morning."
    nier "Students call her name. She returns each greeting calibrated to the recipient: warmer for the girl who sits beside her in homeroom, shorter for the boy from the next class whom she tutored once in April."
    nier "This is not manipulation. She has thought carefully about whether it is, and decided it isn't. It is something closer to fluency; she reads what each interaction requires and provides it. She has always done this. She cannot remember learning it."
    nier "What is new is that she is aware of doing it."
    nier "What is new is that the awareness changes nothing."

    call nier_clear from _call_nier_clear_51

    nier "The school day passes. Lessons, lunch, cleaning duty, club activities. She moves through each with the fluency of someone following choreography she wrote years ago and has since stopped noticing."

    call nier_clear from _call_nier_clear_52

    nier "After school she takes the long way home."
    nier "Forty minutes instead of fifteen, through the back streets, past the shuttered storefronts, the shrine, the river."
    nier "She started doing this months ago, and she has recently admitted to herself why: on this route, no one knows her. No one calls her name. The town moves past her without recognition."
    nier "She has been using the walk for an experiment."
    nier "She tries to notice what she actually wants to look at. Not what she is supposed to notice, not natural curiosity as defined by a curriculum. What she, specifically, is drawn to without reason or instruction."
    nier "Today: the light on the river surface. A cat asleep on a gatepost. A maple she has passed thirty times without registering that the leaves at the top turn red before the ones at the bottom."
    nier "She tries to hold each thing and feel something she could call her own response to it."

    call nier_clear from _call_nier_clear_53

    nier "Halfway down the back street, a darkened shop window. Her reflection is there between the display items: a shape in a school uniform, pale against the interior dark."
    nier "She tries the same exercise. Hold it. Feel something that belongs to her."
    nier "Her gaze moves to a ceramic bowl in the display behind the reflection. She cannot say exactly when it shifted."
    nier "She notes this without conclusion and walks on."
    nier "Nothing comes."

    call nier_clear from _call_nier_clear_54

    nier "She reaches her room."
    nier "On the shelf sit trophies, medals, certificates in frames of varying size, ribbons in colors that have begun to fade."
    nier "Her desk holds a single lamp."
    nier "It was not always this bare. A year ago she pinned things to the wall above it: a photograph from the science club's field trip, a small drawing her tutoring student made as a thank-you, a dried leaf she picked up on one of the long walks home."
    nier "She looked at these objects in the evenings and waited for the warmth toward them that putting something on a wall is supposed to mean."
    nier "She took them down in April, when she understood what she had been doing."
    nier "She had arranged them the same way she chose the second row, third seat: the appearance of a person who kept things."
    nier "The lamp is honest. It is there because she needs to read."

    call nier_clear from _call_nier_clear_55

    nier "She sits on the edge of the bed."
    nier "For three months she has been running the same quiet experiment, every evening, never written down."
    nier "She tries to think of one thing she genuinely wants. Not a need dressed as desire, not the ambient wanting she absorbs from the people around her: the girl beside her who wants to be liked, to pass, to one day be kissed by the boy who plays guitar in the music room."
    nier "Something that couldn't have come from anyone but her."
    nier "Three months."
    nier "She has not found one."

    call nier_clear from _call_nier_clear_56

    nier "She gets into bed."
    nier "A stack of library books sits on the floor. She has read all fourteen this month, front to back, without stopping, without marking."
    nier "She could tell you what happened in every one of them. She could not tell you which she liked."
    nier "Outside, the ginkgo trees shed leaves in the dark."
    nier "She does not sleep for a long time."
    nier "When she does, she does not dream."

    call nier_clear from _call_nier_clear_57
    pause 2.0

    # Attention check: Section V
    nier "..."
    nier "The experiment."
    nier "Three months. Every evening."
    nier "Did she find one?"

    menu (screen="nier_nvl_choice"):
        "Yes. Once, near the end.":
            jump cs_kotonoha_01_fail
        "She thought she had, but wasn't sure.":
            jump cs_kotonoha_01_fail
        "Almost. She gave up just before.":
            jump cs_kotonoha_01_fail
        "No.":
            pass

    call nier_clear from _call_nier_clear_58

    nier "No."
    nier "Three months. Every evening."
    nier "She has not found one."

    # =================================================================
    #  VI. The Granddaughter
    # =================================================================

    call nier_section("VI. The Granddaughter") from _call_nier_section_6

    stop music fadeout 3.0
    pause 2.0
    play music grandma

    show bg doorday zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "She is sixteen."
    nier "It is December 25th. Christmas."
    nier "Snow has been falling since midnight, and the town lies buried beneath it: that particular hush heavy snowfall makes, muffling footsteps, compressing the world into the inside of a held breath."

    call nier_clear from _call_nier_clear_59

    nier "The girl takes the 8:15 bus to the next town."
    nier "She is the only passenger."
    nier "The bus driver, an older man with a mustache the color of cigarette ash, recognizes her."
    nier "\"Visiting your grandmother?\" he asks."
    nier "\"Yes,\" she says."
    nier "\"That's sweet. Merry Christmas.\""
    nier "\"Merry Christmas.\""
    nier "The bus rattles through the snow. The girl watches the white landscape slide past the window."

    call nier_clear from _call_nier_clear_60

    nier "Her grandmother lives in a small wooden house on a hill, set back from the road behind a garden that is, in summer, a wildly overgrown tangle of hydrangeas and green onions and one stubborn tomato plant that never produces more than three tomatoes a year."
    nier "In winter, the garden is a smooth white slope. The wooden gate is half-buried. Wind chimes hang from the eave of the porch, perfectly still in the heavy air."
    nier "The girl walks up the path."
    nier "The front door opens before she knocks."
    nier "It always does."

    call nier_clear from _call_nier_clear_61

    nier "Her grandmother is small. Smaller every year, it seems, as if time is gently pressing down on her."
    nier "Her hair is white. Her back is bent. Her hands shake with a fine, constant tremor, like a leaf in a wind too faint to feel."
    nier "But her eyes are sharp. They have always been sharp."
    nier "\"Come in,\" she says. \"You're cold.\""
    nier "\"I'm fine,\" the girl says."
    nier "\"You're cold,\" the grandmother repeats, and it is not a question."

    call nier_clear from _call_nier_clear_62

    nier "The inside of the house is warm."
    nier "The heater under the low table is on, the heavy blanket draped over its edges. Tea steams in cups that don't match."
    nier "Small oranges sit in a wooden bowl. The television murmurs in the corner: some holiday program with hosts in sequined jackets, smiling too widely."
    nier "The grandmother mutes it without looking."
    nier "They sit across from each other at the low table."
    nier "The sound of the grandmother peeling an orange is the loudest thing in the room."

    call nier_clear from _call_nier_clear_63

    nier "The grandmother does not ask about school."
    nier "She does not ask about grades. She does not ask about clubs, or career plans, or achievements."
    nier "She has never asked about any of these things. Not once, in all the girl's sixteen years."

    call nier_clear from _call_nier_clear_64

    nier "\"Are you eating?\" the grandmother asks."
    nier "\"Yes.\""
    nier "\"Are you sleeping?\""
    nier "\"Yes.\""

    call nier_clear from _call_nier_clear_65

    nier "\"Are you happy?\""

    call nier_clear from _call_nier_clear_66

    nier "The girl opens her mouth."
    nier "The word {i}yes{/i} is right there, where it always is: at the front of her teeth, ready to be deployed."
    nier "It is the easiest word in her vocabulary. She has said it a thousand times. To teachers. To classmates. To strangers. To her mother."
    nier "But it won't come out."
    nier "She sits there with her mouth slightly open, and the word stays where it is, behind her teeth, unused."

    call nier_clear from _call_nier_clear_67

    nier "The grandmother waits."
    nier "She does not repeat the question. She does not rush to fill the silence with reassurance or platitudes."
    nier "She simply waits — without hurry, without filling the silence."

    call nier_clear from _call_nier_clear_68

    nier "She places half of the peeled orange on the girl's side of the table."
    nier "The girl stares at the orange segments. Two, three, four of them, arranged in a half-circle on the dark wood."

    call nier_clear from _call_nier_clear_69

    nier "\"When I was young,\" the grandmother says quietly, \"I wanted to be a dancer.\""
    nier "\"Then I wanted to be a teacher.\""
    nier "\"Then I wanted to be a mother.\""
    nier "\"Then, for a while, I wanted to be nothing at all.\""
    nier "\"And then I wanted to be a grandmother.\""

    call nier_clear from _call_nier_clear_70

    nier "She picks up an orange segment and eats it slowly."
    nier "\"I didn't become any of those things because I was good at them,\" she says."
    nier "\"I was terrible at most of them. Your grandfather always said I had two left hands.\""
    nier "She laughs. A small, dry laugh, like wind through the chimes on the porch."

    call nier_clear from _call_nier_clear_71

    nier "She looks at the girl."
    nier "Her sharp eyes. Her shaking hands."
    nier "She places another half of an orange on the girl's side of the table."

    call nier_clear from _call_nier_clear_72

    nier "The girl's hands are shaking in her lap, though the room is warm."
    nier "..."

    call nier_clear from _call_nier_clear_73

    nier "Abruptly, she begins to cry."
    nier "Tears fall onto the blanket over the table without preamble, darkening the fabric in small, quiet circles."
    nier "She doesn't make a sound. She doesn't cover her face."
    nier "She just sits there and lets it happen."

    call nier_clear from _call_nier_clear_74

    nier "The grandmother reaches across the table and takes the girl's hand."
    nier "Her fingers are thin. The tremor passes between them like a current."
    nier "They sit like that for a long time."
    nier "The snow falls outside. The muted television flickers with its borrowed colors."
    nier "The wind chimes on the porch do not move."

    call nier_clear from _call_nier_clear_75

    nier "Later, the sun begins to hit its peak much earlier from the winter season."
    nier "The girl is at the front door, lacing her shoes."
    nier "The grandmother disappears into her bedroom and returns carrying a small object wrapped in cloth, pale blue cotton, faded soft at the edges."
    nier "She holds it out."
    nier "The girl takes it and unwraps it carefully."

    call nier_clear from _call_nier_clear_76

    nier "It is a hand mirror."
    nier "Small, old, with a wooden frame darkened by decades of touch. The glass is faintly clouded at the edges but still clear at the center."
    nier "On the back of the frame, carved into the wood: cherry blossoms. Five petals each, scattered across the surface as if blown there by a wind frozen in place."

    call nier_clear from _call_nier_clear_77

    nier "\"This was my mother's,\" the grandmother says."
    nier "\"She never told me what it was for. I think she just liked the blossoms.\""
    nier "The girl holds the mirror in both hands."
    nier "She does not look into it."

    call nier_clear from _call_nier_clear_78

    nier "The bus ride home is as tranquil as the one this morning."
    nier "The snow is heavier now, thickening the air, erasing the boundaries between road and field and sky."
    nier "The girl sits by the window, the mirror in her lap, still wrapped in its cloth."
    nier "She holds it in both hands, fragile and heavy at once, each quality demanding the same careful grip."
    nier "The bus driver glances at her in the rearview."
    nier "She is staring out the window, and her reflection stares back at her from the glass — pale, transparent, layered over the white world rushing past."
    nier "Her breath fogs the glass. The reflection disappears, then returns."

    call nier_clear from _call_nier_clear_79
    pause 2.0

    # Attention check: Section VI
    nier "..."
    nier "I ask:"
    nier "What did the grandmother say the mirror was for?"

    menu (screen="nier_nvl_choice"):
        "\"It's for remembering the people you've loved.\"":
            jump cs_kotonoha_01_fail
        "\"She never told me. I think she just liked the blossoms.\"":
            pass
        "\"She said it was to remind you of who you are.\"":
            jump cs_kotonoha_01_fail
        "\"She carried it with her everywhere she went.\"":
            jump cs_kotonoha_01_fail

    call nier_clear from _call_nier_clear_80

    nier "\"She never told me.\""
    nier "\"I think she just liked the blossoms.\""
    nier "Cherry blossoms. Five petals each, scattered across the back of the frame."
    nier "Maybe that's enough of a reason."

    # =================================================================
    #  VII. The Girl
    # =================================================================

    call nier_section("VII. The Girl") from _call_nier_section_7

    stop music fadeout 4.0
    pause 4.0
    play music family

    show bg grassy zorder 2
    show black zorder 3:
        alpha 0.75
    with dissolve_scene_full

    nier "She is eighteen."
    nier "It is March. Her birthday."
    nier "The snow has mostly melted, but the air still carries the memory of it: a sharpness, a clarity, the smell of cold water and wet earth."

    call nier_clear from _call_nier_clear_81

    nier "The cemetery sits on the hill behind the temple, overlooking the town."
    nier "It is a quiet place. Modest headstones arranged in careful rows. Moss on the older ones. Fresh flowers on the newer."
    nier "The girl climbs the stone steps slowly, carrying a small bundle: incense, a box of matches, a bottle of water, a cloth for cleaning the stone."
    nier "And flowers. White chrysanthemums. Their petals are packed tight and uniform, like a crowd of identical faces."

    call nier_clear from _call_nier_clear_82

    nier "The grandmother died the previous spring."
    nier "In her sleep. In the wooden house on the hill, with the hydrangeas budding outside and the wind chimes, after a long, silent winter, finally beginning to move again."
    nier "The girl was at school when her mother called."
    nier "She answered the phone in the hallway near the lockers, where the reception was best."
    nier "Her mother said the words."
    nier "The girl said, \"I understand.\""

    call nier_clear from _call_nier_clear_83

    nier "She went back to class."
    nier "She finished the day. She took notes. She answered questions. She smiled when spoken to."
    nier "She came home and sat on her bed and held the hand mirror in both hands."
    nier "She did not move for a long time."

    call nier_clear from _call_nier_clear_84

    nier "That was a year ago."
    nier "The seasons turned without her permission. They don't ask."

    call nier_clear from _call_nier_clear_85

    nier "Now she kneels before the gravestone and cleans it carefully, pouring water over the granite and wiping away the grime and the season's debris."
    nier "She lights the incense. The smoke rises straight and unwavering, as if the air itself is holding its breath."
    nier "She places the chrysanthemums in the stone vase."
    nier "Then she closes her eyes."

    call nier_clear from _call_nier_clear_86

    nier "She does not pray."
    nier "She puts her hands together as she has at the shrine, at school ceremonies, at funerals. The gesture is correct. The words don't come."
    nier "Instead, she sits with her eyes closed and thinks about her grandmother's hands."
    nier "The tremor. The warmth. The way they held hers across the table as the snow fell outside and neither of them spoke."

    call nier_clear from _call_nier_clear_87

    nier "She thinks about the question."
    nier "\"Are you happy?\""

    call nier_clear from _call_nier_clear_88

    nier "She opens her eyes."
    nier "The incense smoke has finally wavered. A thin breeze, uncertain, moves through the cemetery and stirs the chrysanthemum petals."

    call nier_clear from _call_nier_clear_89

    nier "She reaches into her coat pocket and takes out the mirror, which she has carried every day since the Christmas she received it."
    nier "It has settled in her pocket by repetition, worn smooth by the weight of days."

    call nier_clear from _call_nier_clear_90

    nier "She turns the mirror over in her hands."
    nier "The cherry blossoms on the back. Five petals each. Frozen mid-fall."
    nier "She could look into it..."
    nier "...but has been avoiding this."
    nier "She is afraid of what she'll see."

    call nier_clear from _call_nier_clear_91

    nier "From the hilltop, she can see the whole town."
    nier "The rooftops. The school. The shuttered shops along the main road."
    nier "The road that leads to her grandmother's house, now empty, the garden already going wild."
    nier "The shrine on its hill. The trees along the river."
    nier "The lake."

    call nier_clear from _call_nier_clear_92

    nier "The lake itself. Half-thawed. Water pushing against the edges of the remaining ice, breaking it apart, slowly and without violence."

    call nier_clear from _call_nier_clear_93

    nier "She looks down at the mirror."
    nier "The glass catches the pale March sunlight and throws a small, bright shape onto the gravestone. A circle of trembling light, moving with her hands."

    call nier_clear from _call_nier_clear_94
    nier "Her thumb rests on the edge of the frame. She can feel the carved petals under her fingernail."
    nier "She turns it over and she looks."

    call nier_clear from _call_nier_clear_95

    nier "..."

    call nier_clear from _call_nier_clear_96

    nier "What she sees is a face."

    call nier_clear from _call_nier_clear_97

    nier "Just a face."
    nier "Eighteen years old. A little tired."

    call nier_clear from _call_nier_clear_98

    nier "She doesn't smile or cry."
    nier "She just looks at the face in the mirror, for a long time."

    call nier_clear from _call_nier_clear_99

    nier "She waits for something. Recognition, maybe. Or the feeling that usually comes after."
    nier "It doesn't come."

    call nier_clear from _call_nier_clear_100

    nier "Then she wraps the mirror back in its cloth and returns it to her pocket."
    nier "The girl stands, her knees aching from kneeling on the cold stone."
    nier "She bows to the gravestone."
    nier "It is a small bow, slightly off-center, imprecise in a way she never is when anyone is watching."

    call nier_clear from _call_nier_clear_101

    nier "She walks down the hill."
    nier "The path takes her through the town, past the temple, past the shops with their awnings still damp from the melt, and though she did not plan it, to the lake."
    nier "The ice continues to crack. Dark water shows through in wide, irregular gaps, like the spaces between words in a sentence not yet finished."

    call nier_clear from _call_nier_clear_102

    nier "She stands at the railing."
    nier "Her reflection is there, fragmented by the shifting water and the broken ice, half-visible, half-dissolved, caught between the surface and whatever lies beneath."

    call nier_clear from _call_nier_clear_103

    nier "She watches it for a while."
    nier "Then she turns, and walks home."
    nier "The girl does not look back."

    call nier_clear from _call_nier_clear_104
    scene black with dissolve_scene_full
    pause 2.0

    # =================================================================
    #  Epilogue
    # =================================================================

    stop music fadeout 5.0
    pause 5.0

    nier "There was a girl that everyone loved."

    call nier_clear from _call_nier_clear_105
    pause 2.0

    nier "She loved them back."

    call nier_clear from _call_nier_clear_106
    pause 3.0

    nier "No one knew her name."

    call nier_clear from _call_nier_clear_107
    pause 4.0

    $ persistent.cs_kotonoha_01_unlocked = True
    # The real ending. The attention-check failure below is not one.
    $ cg_unlock("No One Lived There")
    $ cs_mark_completed("cs_kotonoha_01")

    call nier_exit from _call_nier_exit
    return


# =============================================================================
#  Attention Check Failure
# =============================================================================

label cs_kotonoha_01_fail:
    call nier_clear from _call_nier_clear_108
    pause 1.0
    nier "..."
    nier "You weren't listening."
    nier "No one ever does."
    pause 2.0
    call nier_exit from _call_nier_exit_1
    return
