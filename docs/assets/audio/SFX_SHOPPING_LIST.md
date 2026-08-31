# ENTER M SFX Shopping List

Scope scanned: `game/story/season1/*.rpy`, including `0515.rpy` through `0531.rpy`, `s1disc.rpy`, and `exam_guard.rpy`.

Tags:
- `Explicit` means the story file already contains a `# SFX SUGGESTION` or direct sound/impact cue.
- `Inferred` means the cue is suggested by scene action, location, or recurring atmosphere.
- `P1` = high reuse or strongly scene-defining. `P2` = useful polish. `P3` = optional accent.

Existing reusable definitions to audit before sourcing new audio:
- `moddooropen` / `moddoorclose` - `game/assets/audio/sfx/dooropen.ogg`, `doorclose.ogg`
- `ac` - `game/assets/audio/sfx/ac.ogg`
- `modwriting` - `game/assets/audio/sfx/writing.ogg`
- `interjection` - `game/assets/audio/sfx/interject.wav`
- Phone SFX now wired: `phone_text_in` = `messagereceive.ogg`, `phone_text_out` = `messagesend.ogg`, `phone_notification` = the same restrained `messagereceive.ogg` cue, and `phone_ringtone` = `ringtone.ogg` (assets in `game/assets/audio/sfx/phone/`). Still `None`: `phone_open` (no "raise phone" cue yet).

Tone target: restrained, close, tactile, and slightly dry. The story gets a lot of pressure from small physical details, so most sounds should feel like real room noise rather than comedy punctuation. Save louder/stylized cues for diegetic media, arcade games, exam breaks, and dream/meta material.

## Buy Or Make First

- [ ] `P1` Phone vibration pack - short fabric-muted buzz, desk/table rattle, nightstand rattle, pocket buzz, repeated-message sequence, incoming-call vibration, timer buzz. `[Explicit/Inferred]` Sources: `0516:25`, `0518:17`, `0519:9`, `0519:406`, `0520:210`, `0521:563`, `0524:414`, `0524:565`, `0525:48`, `0525:1018`, `0526:371`, `0528:277`, `0529:93`, `0531:72`.
- [ ] `P1` Phone UI pack - open/raise phone, thread reveal tick, a distinct contact-unlock cue, phone call answer/end. `[Inferred]` Partially filled: text sent/received (`messagesend.ogg`/`messagereceive.ogg`), random-conversation availability (currently reusing `messagereceive.ogg`), and the incoming-call ringtone (`ringtone.ogg`) are wired; `phone_open` (open/raise phone) is still a `None` placeholder in `game/addons/Phone System/phone_model_construct.rpy`.
- [ ] `P1` School bell set - clean warning bell, final bell, distant/muffled rooftop bell, stark exam bell with no crowd tail, underwater/dream bell. `[Explicit]` Sources: `0517:110`, `0519:203`, `0521:313`, `0522:29`, `0522:140`, `0523:295`, `0524:492`, `0526:22`, `0528:256`, `0530:215`, `0531:127`.
- [ ] `P1` School hallway bed - layered students, shoe squeaks, bag swings, corridor tile footsteps, room-release chatter after bells. `[Explicit/Inferred]` Sources: `0517:110`, `0519:228`, `0528:256`, `0529:121`, `0531:127`.
- [ ] `P1` Classroom/exam room bed - pencils, paper shifts, occasional cough, clock tick, chairs, silence-forward room tone. `[Explicit/Inferred]` Sources: `0516:129`, `0519:156`, `0526:14`, `0526:79`, `0526:121`, `0526:465`, `0527:22`, `0527:162`, `0528:22`.
- [ ] `P1` Paper/writing/desk pack - dry pen tap, pencil tap, pencil clatter, pencil slap, page flips, paper stack alignment, exam packet slap, flashcard flip, sticky note peel, folder slide. `[Explicit/Inferred]` Sources: `0515:38`, `0520:100`, `0520:152`, `0520:161`, `0524:547`, `0525:117`, `0525:130`, `0525:247`, `0526:79`, `0526:465`, `0527:393`, `0528:22`, `0530:344`, `0530:397`.
- [ ] `P1` Door variants - home front door, bedroom door soft close, classroom/club sliding door, rooftop metal latch/hinge, cafe/store door chime, empty-house latch with room echo. `[Explicit/Inferred]` Existing `moddooropen`/`moddoorclose` may cover only a generic door. Sources: direct `play sound moddooropen/moddoorclose` throughout, plus `0523:115`, `0525:411`, `0530:503`.
- [ ] `P1` Kitchen/home bed - refrigerator hum, kettle boil and click, toaster pop, frying oil, pot boil, pan sizzle, cabinet doors, microwave start, sink/plate/bowl/glass/chopsticks, quiet house pipe tick, floorboards. `[Explicit/Inferred]` Sources: `0515:239`, `0516:25`, `0520:82`, `0521:444`, `0523:58`, `0525:22`, `0526:300`, `0528:335`, `0530:522`.
- [ ] `P1` Track/running pack - rubber track footfalls, easy jogging cadence, measured breathing, coach whistle, water bottle handling, shoe/track bag movement. `[Explicit/Inferred]` Sources: `0521:353`, `0525:1011`, `0527:342`, `0529:177`, `0531:168`, `0531:196`.
- [ ] `P1` Arcade pack - room ambience loop, racing cabinet countdown/engine/tire scrape/collision, light-gun fire, dance cabinet beat/crowd bleed, prize-machine jingles, claw motor/clack/plush drop, air hockey hit. `[Explicit/Inferred]` Sources: `0531:364`, `0531:393`, `0531:433`, `0531:452`, `0531:510`, `0531:554`, `0531:566`.
- [ ] `P1` Library/cafe quiet public beds - library hush, cart squeak, stamp thump, cafe doorbell, cafe crowd murmur, cup/saucer, ice in glass, register/payment. `[Explicit/Inferred]` Sources: `0525:95`, `0525:149`, `0525:247`, `0525:411`, `0525:541`, `0525:658`, `0531:583`, `0531:705`.

## Reusable Ambience Beds

- [ ] `P1` Club room afternoon - quiet paper, pens, chair creaks, desk nicks, faint hallway bleed. `[Inferred]` Sources: `0515`, `0516`, `0520`, `0522`, `0524`, `0526`, `0528`, `0530`.
- [ ] `P1` Kitchen morning - kettle/toaster/fridge/counter movement, subdued family breakfast. `[Inferred]` Sources: `0516`, `0519`, `0520`, `0523`, `0525`, `0529`, `0530`, `0531`.
- [ ] `P1` Kitchen dinner - plates, utensils, rice bowl, pan/steam, fridge hum under pauses. `[Inferred]` Sources: `0515`, `0521`, `0524`, `0526`, `0528`, `0529`, `0530`.
- [ ] `P1` Bedroom night - desk room tone, phone charging buzz, screen glow hum, clock, outside car pass. `[Inferred]` Sources: `0517`, `0519`, `0520`, `0521`, `0524`, `0525`, `0530`, `0531`.
- [ ] `P2` Residential street day/night - distant traffic, bicycle wheel click, vending machine hum, open kitchen-window dishes, neighborhood voices. `[Explicit/Inferred]` Sources: `0517:249`, `0517:259`, `0525:1007`, `0529:263`, `0531:762`.
- [ ] `P2` City/station/transit - bus interior, bus engine, pneumatic hiss, doors, traffic under windows, storefronts, evening station district. `[Explicit/Inferred]` Sources: `0516:270`, `0519:97`, `0525:75`, `0531:752`.
- [ ] `P2` Rooftop lunch - open air, light wind, lunch packaging, metal rooftop door, distant bell through door. `[Explicit/Inferred]` Sources: `0521`, `0523:115`, `0523:295`, `0524:492`, `0530:215`.
- [ ] `P2` School gym assembly - large room murmur, PA feedback, microphone pop/cutoff, plastic floor/bleachers, gym handclap echo. `[Explicit/Inferred]` Sources: `0524:69`, `0524:74`, `0524:126`, `0524:176`.
- [ ] `P2` Theater outing - lobby crowd, ticket/concession room tone, theater seating, movie audio bleed, post-movie lobby. `[Explicit/Inferred]` Sources: `0518:104`, `0518:153`, `0518:225`, `0518:258`.
- [ ] `P2` Bookstore - paper bags, old magazines sliding, shelf browsing, register/twine wrap, door/sidewalk bleed. `[Inferred]` Sources: `0531:264`, `0531:299`, `0531:345`.

## One-Shot Foley And Impacts

- [ ] `P1` Soft weighted school bag thump. `[Explicit]` Sources: `0515:195`, `0525:111`, `exam_guard:521`.
- [ ] `P1` Soft cloth/body thump, non-combat. `[Explicit]` Sources: `0520:281`, `0529:456`.
- [ ] `P1` Blunt shoulder collision with clothing and phone fumble. `[Explicit]` Source: `0517:264`.
- [ ] `P2` Forehead/table thump plus pencil roll. `[Explicit]` Source: `0525:757`.
- [ ] `P2` Finger snap, close and dry. `[Explicit]` Source: `0517:35`.
- [ ] `P2` Two sharp gym handclaps with room echo. `[Explicit]` Source: `0524:176`.
- [ ] `P2` Single sharp Monika clap after timer. `[Explicit]` Source: `0530:375`.
- [ ] `P2` Paper bag crinkle and paper wrapper toss/bin hit. `[Explicit]` Sources: `0517:368`, `0529:149`.
- [ ] `P2` Gym bag drop plus refrigerator seal pull. `[Explicit]` Source: `0530:522`.
- [ ] `P2` Ice cubes in glass. `[Explicit]` Sources: `0525:541`, also useful at `0531:628`.
- [ ] `P2` Water glass placed outside door, very soft tap. `[Inferred]` Source: `0526:302`.
- [ ] `P2` Floorboard small complaint/creak. `[Inferred]` Sources: `0526:300`, `exam_guard:465`, `exam_guard:676`, `0525:1133`.
- [ ] `P2` Cabinet/TV game-box open, card box handling, cards dealt. `[Explicit/Inferred]` Sources: `0529:343`, `0529:369`.
- [ ] `P3` Fry hitting cheek / food toss accent. `[Inferred]` Source: `0515:161`.
- [ ] `P3` Ruler/tape/poster-board arts-and-crafts rustle. `[Inferred]` Sources: `0517:415`, `0517:444`.
- [ ] `P3` Water bottle cap twist / bottle set down / cap turned toward MC. `[Inferred]` Sources: `0527:401`, `0521:199`.

## Dream, Meta, And Unsettling Cues

- [ ] `P1` Old PA speaker click with faint electrical crackle. `[Explicit]` Source: `0522:19`.
- [ ] `P1` Underwater/muffled school bell with warped reverb. `[Explicit]` Source: `0522:29`.
- [ ] `P1` Abrupt phone video/music cutoff after frantic taps. `[Explicit]` Source: `0522:81`.
- [ ] `P2` Waiting-room number dispenser cough. `[Inferred]` Source: `0522:24`.
- [ ] `P2` Floating chalk underline/scrape and cup slide in dream classroom. `[Inferred]` Sources: `0522:47`, `0522:51`.
- [ ] `P2` Conveyor belt carrying school/home objects under cheerful waiting music. `[Inferred]` Source: `0522:58`.
- [ ] `P2` Cold exam/meta sting for generic caught state. `[Inferred]` Source: `exam_guard:237`.
- [ ] `P3` Nier/disclaimer/menu ambience - low text-screen pulse or faint paper/static texture if the disclaimer needs audio later. `[Inferred]` Source: `s1disc.rpy`.

## Day-By-Day Scene Cues

### 0515

- [ ] `P1` Club room pen tap in quiet room. `[Explicit]` `0515:38`
- [ ] `P1` Door open/close pair for club/house transitions. `[Explicit]` `0515:129`, `0515:136`, `0515:174`, `0515:180`
- [ ] `P2` House exterior with food bag/grease-paper handling and fry toss. `[Inferred]` `0515:145-161`
- [ ] `P1` Weighted bag thump in bedroom. `[Explicit]` `0515:195`
- [ ] `P1` Katsudon prep loop - sink water, breading, frying oil sizzle. `[Explicit/Inferred]` `0515:218`, `0515:231`, `0515:239`
- [ ] `P2` Dinner table - plates cleared, chopsticks pause, water/medication. `[Inferred]` `0515:275-325`
- [ ] `P1` Living-room night book pages plus handheld button taps. `[Explicit]` `0515:322`

### 0516

- [ ] `P1` Phone vibrating against wood plus distant toaster pop. `[Explicit]` `0516:25`
- [ ] `P2` Breakfast eggs, plate set-down, toast, glass of water. `[Inferred]` `0516:34-65`
- [ ] `P1` Math classroom pencils on paper. `[Inferred]` `0516:129`
- [ ] `P2` Club notebook/page handling and bag drop. `[Inferred]` `0516:165-205`
- [ ] `P1` Door close after club. `[Explicit]` `0516:225`
- [ ] `P2` Shopping street/vending machine/public sidewalk bed. `[Inferred]` `0516:230`
- [ ] `P1` Wet tires passing close with gutter splash. `[Explicit]` `0516:259`
- [ ] `P1` Bus engine groan plus pneumatic brake hiss. `[Explicit]` `0516:270`
- [ ] `P2` Home door and living-room guest entrance sequence. `[Explicit/Inferred]` `0516:289`, `0516:295`, `0516:341`, `0516:343`

### 0517

- [ ] `P2` Doorway morning chaos - shoe tying, bag search, wrapped toast. `[Inferred]` `0517:9-15`
- [ ] `P2` Finger snap. `[Explicit]` `0517:35`
- [ ] `P1` School door close. `[Explicit]` `0517:47`
- [ ] `P2` Civics classroom - small laugh killed by teacher stare, pencils resume. `[Inferred]` `0517:79-87`
- [ ] `P1` Final bell into hallway crowd/shoe squeaks/bag swings. `[Explicit]` `0517:110`
- [ ] `P2` Tech store checkout - crowd line, scanner, game case/security sticker, bag crinkle. `[Inferred]` `0517:143-164`
- [ ] `P1` Front door open for Asahina/poster scene. `[Explicit]` `0517:187`
- [ ] `P2` Arts-and-crafts bed - poster board, tape, ruler, glue. `[Inferred]` `0517:188`, `0517:415`, `0517:444`
- [ ] `P2` Residential night - bicycle wheel click, dishes through kitchen window, vending machine hum. `[Inferred]` `0517:249-259`
- [ ] `P1` Phone buzz before collision. `[Inferred]` `0517:260`
- [ ] `P1` Shoulder impact with phone/clothing fumble. `[Explicit]` `0517:264`
- [ ] `P2` Paper bag crinkle as Matsuda turns. `[Explicit]` `0517:368`
- [ ] `P1` Repeated Matsuda contact message buzzes. `[Inferred]` `0517:352`, `0517:380`, `0517:417`

### 0518

- [ ] `P1` Fabric-muted phone vibration. `[Explicit]` `0518:17`
- [ ] `P2` Living-room quiet texting with Asahina nearby. `[Inferred]` `0518:3-68`
- [ ] `P1` City morning delivery carts and storefront shutters. `[Explicit]` `0518:93`
- [ ] `P2` Theater exterior/lobby ambience and ticket/concession movement. `[Inferred]` `0518:104-219`
- [ ] `P1` Theater/lobby door open. `[Explicit]` `0518:156`
- [ ] `P1` Theater-loud thunderclap with sub-bass tail. `[Explicit]` `0518:258`
- [ ] `P2` Horror movie wet tunnel/creature sound, very close and overmixed. `[Inferred]` `0518:277-309`
- [ ] `P2` Post-movie lobby crowd shift. `[Inferred]` `0518:318-350`
- [ ] `P1` Home door open. `[Explicit]` `0518:406`
- [ ] `P1` Night text thread message cue. `[Inferred]` `0518:464`

### 0519

- [ ] `P1` Insistent phone alarm loop plus nightstand vibration. `[Explicit]` `0519:9-12`
- [ ] `P2` Breakfast - toast, folder into work bag, travel mug, microwave clock pressure. `[Inferred]` `0519:42-86`
- [ ] `P2` Morning bus/window ride and station arrival. `[Inferred]` `0519:97-101`
- [ ] `P2` Civics chalk underline, pens, pencil tap. `[Inferred]` `0519:112`, `0519:156`
- [ ] `P1` Lunch warning bell cutting off unfinished moment. `[Explicit]` `0519:203`
- [ ] `P2` Hallway ambush crowd and Matsuda's too-loud entrance. `[Inferred]` `0519:228-294`
- [ ] `P2` Dinner cutlery/fridge/home table under banter. `[Inferred]` `0519:306-383`
- [ ] `P2` Controller set-down/game menu/video playback. `[Inferred]` `0519:401-421`
- [ ] `P1` Perfectly timed phone notification buzz. `[Explicit]` `0519:406`

### 0520

- [ ] `P1` Morning group text receive cue. `[Inferred]` `0520:7-20`
- [ ] `P1` Kettle switch snap-off with fading boil. `[Explicit]` `0520:82`
- [ ] `P2` Science classroom chalk taps and group reaction murmur. `[Inferred]` `0520:100-115`
- [ ] `P1` Club paper, pencil scratches, page turns, chair creak. `[Inferred]` `0520:140-161`
- [ ] `P1` Repeated notification buzz sequence from Matsuda. `[Explicit]` `0520:210-229`
- [ ] `P2` Notebook close, downstairs laugh, room transition into TV/game space. `[Inferred]` `0520:231-245`
- [ ] `P1` Soft cloth-muted ribcage thump. `[Explicit]` `0520:281`
- [ ] `P1` Party-game round-start jingle and TV/controller layer. `[Explicit/Inferred]` `0520:294-303`
- [ ] `P2` Cartoon explosives from TV game. `[Inferred]` `0520:303`
- [ ] `P2` Takeout/dishes/kitchen carry. `[Inferred]` `0520:357-359`
- [ ] `P1` Door close for Sam exit. `[Explicit]` `0520:386`
- [ ] `P2` Late front door opening through floorboards. `[Explicit/Inferred]` `0520:421`

### 0521

- [ ] `P1` Classroom paper-rustle wave. `[Explicit]` `0521:32`
- [ ] `P2` Rooftop door/air and lunch bag handling. `[Explicit/Inferred]` `0521:96-133`
- [ ] `P1` Distant warning bell muffled by rooftop door. `[Explicit]` `0521:313`
- [ ] `P1` Track warmup, strides, rubber footfalls, coach field voice. `[Inferred]` `0521:329-425`
- [ ] `P1` Boiling water with low pan sizzle. `[Explicit]` `0521:444`
- [ ] `P1` Mom text buzz on counter. `[Inferred]` `0521:461`
- [ ] `P2` Plates/cabinet/table setting, covered plate for Mom, kitchen quieter without her. `[Inferred]` `0521:476-494`
- [ ] `P2` Kitchen cleanup and plate into fridge. `[Inferred]` `0521:551-553`
- [ ] `P1` Incoming-call vibration rattling on desk. `[Explicit]` `0521:563`
- [ ] `P2` Pen click heard through call. `[Inferred]` `0521:614`
- [ ] `P2` Late cabinet doors and microwave downstairs. `[Inferred]` `0521:666`

### 0522

- [ ] `P1` Old PA speaker click with electrical crackle. `[Explicit]` `0522:19`
- [ ] `P2` Number dispenser cough, chairs turning without movement. `[Inferred]` `0522:22-24`
- [ ] `P1` Underwater school bell. `[Explicit]` `0522:29`
- [ ] `P2` Floating chalk underline, cup slide, dream classroom shimmer. `[Inferred]` `0522:47-58`
- [ ] `P1` Frantic touchscreen taps into abrupt audio cutoff. `[Explicit]` `0522:81`
- [ ] `P2` Empty kitchen - bowl in sink, chair pushed back, fridge rice ball grab. `[Inferred]` `0522:100-111`
- [ ] `P2` Rushed morning - toothbrush, bag checks, jog to station, bus. `[Inferred]` `0522:116-118`
- [ ] `P1` Full-volume final bell interrupting conversation. `[Explicit]` `0522:140`
- [ ] `P1` Club door open/close, careful gentle close. `[Explicit]` `0522:176`, `0522:211`
- [ ] `P2` Club argument texture - paper gripped, closet area, soda bottles, paper stack. `[Inferred]` `0522:179-285`

### 0523

- [ ] `P1` Kettle click-off with boil fade. `[Explicit]` `0523:58`
- [ ] `P2` Hallway/stairwell current to rooftop. `[Inferred]` `0523:89-103`
- [ ] `P1` Rooftop metal door latch/hinge plus light wind. `[Explicit]` `0523:115`
- [ ] `P2` Rooftop wind tugging napkin/notebook/paper. `[Inferred]` `0523:140`, `0523:189`, `0523:226`
- [ ] `P1` Second rooftop door open and door close. `[Explicit]` `0523:207`, `0523:269`
- [ ] `P2` Rice cracker wrapper/hand-off. `[Inferred]` `0523:254`
- [ ] `P1` Thin school warning bell from below. `[Explicit]` `0523:295`
- [ ] `P1` Track practice - easy laps, breath, water, stretching. `[Inferred]` `0523:313-395`
- [ ] `P2` Evening home - shower, covered plate, clean laundry, laptop open/fan, pen tap. `[Inferred]` `0523:403-627`
- [ ] `P1` Uneven air conditioner rattle with trash bin scrape outside. `[Explicit]` `0523:654`
- [ ] `P2` Four alarms being set. `[Inferred]` `0523:688`

### 0524

- [ ] `P1` Gym PA microphone pop/feedback and cutoff. `[Explicit/Inferred]` `0524:74`, `0524:126`
- [ ] `P1` Gym crowd swelling back in after assembly. `[Explicit]` `0524:126`
- [ ] `P1` Two sharp teacher handclaps with gym echo. `[Explicit]` `0524:176`
- [ ] `P2` Algebra review pencil scratch and calculator anxiety in class. `[Inferred]` `0524:229-304`
- [ ] `P1` Rooftop door opens/closes and wind. `[Explicit/Inferred]` `0524:339`, `0524:399`, `0524:426`, `0524:508`
- [ ] `P1` Phone vibration muffled under lunch bag. `[Explicit]` `0524:414`
- [ ] `P1` Distant warning bell breaking rooftop quiet. `[Explicit]` `0524:492`
- [ ] `P1` Club writing quiet - paper, eraser wrinkling page, desk creak, steady pen. `[Inferred]` `0524:547-550`
- [ ] `P1` Short neutral phone timer buzz. `[Explicit]` `0524:565`
- [ ] `P2` Dinner kitchen hum, serving spoon, plates drying, phones charging, pen scratch. `[Inferred]` `0524:694-786`
- [ ] `P1` Bedroom phone buzz for library confirmation. `[Inferred]` `0524:800`

### 0525

- [ ] `P1` Sparse house morning - pipe tick, refrigerator hum, car pass. `[Explicit]` `0525:22`
- [ ] `P1` Morning text buzz. `[Inferred]` `0525:48`
- [ ] `P2` Plate rinse, door lock, bus interior. `[Inferred]` `0525:67-76`
- [ ] `P1` Child shoes knocking against bus seat, then stopping. `[Explicit]` `0525:75`
- [ ] `P1` Library second floor hush - paper, carpet, quiet people, table/chairs. `[Inferred]` `0525:95-120`
- [ ] `P2` Book cart passing and librarian stamp thumps. `[Inferred]` `0525:149`, `0525:247`
- [ ] `P2` Flashcards, folders, sticky notes, water bottle, clock. `[Inferred]` `0525:117-334`
- [ ] `P1` Cafe doorbell chime. `[Explicit]` `0525:411`
- [ ] `P2` Cafe lunch - menus, water, lunch plates, register, payment, playlist. `[Inferred]` `0525:453-659`
- [ ] `P1` Ice cubes clicking in glass. `[Explicit]` `0525:541`
- [ ] `P1` Forehead table thump and pencil roll. `[Explicit]` `0525:757`
- [ ] `P2` Kitchen table paper panic, wrapper, chair pull, clock tick. `[Inferred]` `0525:749-905`
- [ ] `P1` Easy running footfalls and measured breathing. `[Explicit]` `0525:1011`
- [ ] `P1` Pocket phone buzz and incoming call during jog. `[Inferred]` `0525:1018-1023`
- [ ] `P2` Grocery-store pocket call bed - produce handling, checkout/card reader, register. `[Inferred]` `0525:1029-1053`
- [ ] `P1` Night text buzz and paper/folder cleanup. `[Inferred]` `0525:1092-1120`

### 0526

- [ ] `P1` Stark exam bell with no crowd tail. `[Explicit]` `0526:22`
- [ ] `P1` Exam paper landing/turn-over and pencil movement. `[Inferred]` `0526:20-26`
- [ ] `P1` Pencil clatter against hard classroom floor. `[Explicit]` `0526:79`
- [ ] `P1` Chairs scraping and low chatter after exam silence breaks. `[Explicit]` `0526:121`
- [ ] `P2` Lunch/intermission hallway comparison chatter. `[Inferred]` `0526:136-165`
- [ ] `P2` Bedroom consequence branch - one closed door, floorboard creak, glass set outside door. `[Inferred]` `0526:294-308`
- [ ] `P1` Club room door open. `[Explicit]` `0526:353`
- [ ] `P1` Quiet club-room timer buzz. `[Explicit]` `0526:371`
- [ ] `P2` Dinner - rice, miso, vegetables, glass placement, steam, tofu. `[Inferred]` `0526:383-405`
- [ ] `P1` Caught-cheating pencil slap in exam silence. `[Explicit]` `0526:465`
- [ ] `P2` Caught-cheating room stop - pencils halt, faces turn, clock resumes. `[Inferred]` `0526:444-471`

### 0527

- [ ] `P1` Thick biology exam packet paper slap. `[Explicit]` `0527:22`
- [ ] `P2` Water bottle refill/snack/lunch exam intermission. `[Inferred]` `0527:132-143`
- [ ] `P1` Calculator power buttons clicking awake. `[Explicit]` `0527:162`
- [ ] `P2` Living-room consequence branch - water glass set near MC, page waits. `[Inferred]` `0527:271-309`
- [ ] `P1` Rubber track shoe strikes settling into jogging rhythm. `[Explicit]` `0527:342`
- [ ] `P2` Breathing count, coach wave-down, water bottles, stretching. `[Inferred]` `0527:346-371`
- [ ] `P1` Kitchen table page flip and pen tap. `[Explicit]` `0527:393`
- [ ] `P2` Cut fruit, water bottle cap turned toward MC, floorboard-muted studying. `[Inferred]` `0527:381-422`
- [ ] `P2` Science teacher hand on paper/calculator off in caught-cheating branches. `[Inferred]` `0527:487-503`

### 0528

- [ ] `P1` Heavy algebra packet landing flat on desk. `[Explicit]` `0528:22`
- [ ] `P2` English listening exam recorded voice and audio stop. `[Inferred]` `0528:166`, `0528:577`
- [ ] `P1` Final bell into chair drag and held-breath release. `[Explicit]` `0528:256`
- [ ] `P1` Close phone buzz through released hallway noise. `[Explicit]` `0528:277`
- [ ] `P2` Living-room consequence branch - cabinet close in kitchen, bag by coffee table. `[Inferred]` `0528:315-345`
- [ ] `P1` Club door open. `[Explicit]` `0528:378`
- [ ] `P2` Quiet no-studying club room - cracked windows, traffic, hallway laugh, folder facedown. `[Inferred]` `0528:380-425`
- [ ] `P2` Kitchen morale ice cream - freezer, bowls, spoons, uneven serving ritual. `[Inferred]` `0528:450-513`
- [ ] `P2` Caught-cheating branches - teacher hand on paper, red pen, recorded voice stopped. `[Inferred]` `0528:536-584`

### 0529

- [ ] `P1` Corridor lunch phone buzzes. `[Inferred]` `0529:93`, `0529:105`, `0529:161`
- [ ] `P1` Fast purposeful footsteps on corridor tile. `[Explicit]` `0529:121`
- [ ] `P2` Melon bread wrapper handling. `[Inferred]` `0529:130-149`
- [ ] `P1` Paper-wrapper swish into hollow bin impact. `[Explicit]` `0529:149`
- [ ] `P1` Track reassessment - easy run, coach whistle, hydrate/walk it out. `[Inferred]` `0529:177-254`
- [ ] `P2` Neighborhood evening - dog/kid, distant dinner clatter through window. `[Inferred]` `0529:263`
- [ ] `P1` Home door open. `[Explicit]` `0529:279`
- [ ] `P2` Dinner - stove, work email, soy sauce, phone on table, spoon slowdown. `[Inferred]` `0529:281-334`
- [ ] `P1` Clean card shuffle and three hands dealt. `[Explicit]` `0529:369`
- [ ] `P1` Work-phone ringtone, full volume, repeating. `[Explicit]` `0529:412`
- [ ] `P2` Card game handling - cards placed, discard pile handshake, box sorting. `[Inferred]` `0529:343-476`
- [ ] `P1` Soft full-body thump into rug. `[Explicit]` `0529:456`
- [ ] `P1` Bedroom phone message cue from Matsuda. `[Inferred]` `0529:489`

### 0530

- [ ] `P2` Morning kitchen with chair/table/bag and Asahina phone. `[Inferred]` `0530:69-120`
- [ ] `P1` Rooftop metal door open/close and wind over index cards. `[Explicit/Inferred]` `0530:155`, `0530:179`, `0530:227`
- [ ] `P1` Distant warning bell through rooftop door. `[Explicit]` `0530:215`
- [ ] `P2` Corridor cardboard box strain, notebooks sliding/catching, papers in pocket. `[Inferred]` `0530:242-316`
- [ ] `P1` Club room active texture - stapler argument, closet opening, dust, page turns, chair shifts, pens. `[Inferred]` `0530:328-397`
- [ ] `P1` Short timer tone plus single clap. `[Explicit]` `0530:375`
- [ ] `P2` Corridor Matsuda/Tsubaki after club, index-card clip. `[Inferred]` `0530:431-492`
- [ ] `P1` Empty-house front latch with slight room echo. `[Explicit]` `0530:503`
- [ ] `P1` Home door open for Asahina. `[Explicit]` `0530:513`
- [ ] `P1` Gym bag thump and refrigerator seal. `[Explicit]` `0530:522`
- [ ] `P2` Empty-chair dinner - refrigerator hum, phone light, plates. `[Inferred]` `0530:543-567`
- [ ] `P2` Late Mom home - folders, plate/glass to kitchen, upstairs laugh. `[Inferred]` `0530:577-675`
- [ ] `P1` Group chat message cues and private Monika message. `[Inferred]` `0530:687-717`
- [ ] `P2` Desk lamp off/alarm set/arcade card into wallet. `[Inferred]` `0530:705-722`

### 0531

- [ ] `P1` Kitchen table phone vibration. `[Explicit]` `0531:72`
- [ ] `P2` Morning kitchen - toast, mugs, bag checks, track shoes, water bottle. `[Inferred]` `0531:17-98`
- [ ] `P1` Final bell into chair scrape. `[Explicit]` `0531:127`
- [ ] `P2` Corridor doorway/goodbye to Monika. `[Inferred]` `0531:135-183`
- [ ] `P1` Coach whistle from courtyard. `[Explicit]` `0531:168`
- [ ] `P1` Track drills - footfalls, whistle cutoff, cone walk-back, heat from rubber. `[Explicit/Inferred]` `0531:196-254`
- [ ] `P1` Bookstore ambience - shelves, old magazines, paper bags, rack turn, register/twine wrap. `[Inferred]` `0531:264-347`
- [ ] `P1` Arcade ambience loop. `[Explicit]` `0531:364`
- [ ] `P1` Racing cabinet - card tap, countdown, engines, results screen, tire scrape/collision. `[Explicit/Inferred]` `0531:387-433`
- [ ] `P2` Light-gun game - plastic gunfire, cable catch, helicopter crash. `[Inferred]` `0531:452-466`
- [ ] `P1` Arcade phone buzz during score tally. `[Inferred]` `0531:466`
- [ ] `P2` Dance cabinet and Asahina win moment. `[Inferred]` `0531:510`, `0531:835`
- [ ] `P1` Claw-machine motor, metal clack, plush/cabinet thump. `[Explicit]` `0531:554`
- [ ] `P2` Locker rental/checking, arcade cards, photo booth, air hockey, overhead lights dim. `[Inferred]` `0531:375`, `0531:566`
- [ ] `P2` Station cafe - tableware notice from heavy bag, food arrival, plates, ice, trains beyond window. `[Inferred]` `0531:588-628`
- [ ] `P2` Cafe cup on saucer, sugar packet adjustment. `[Inferred]` `0531:705`
- [ ] `P2` Station/train departure - doors, platform ambience, bundle handling. `[Inferred]` `0531:752-754`
- [ ] `P2` City evening walk - storefront lights, traffic signal, track bag strap catch. `[Inferred]` `0531:762-801`
- [ ] `P2` Home arrival/living room - Mom opens door, mug, kitchen water, laptop/legal pad. `[Inferred]` `0531:801-872`
- [ ] `P1` Bedroom group chat and private Matsuda buzzes. `[Inferred]` `0531:913-939`

### Exam Guard Branches

- [ ] `P1` Front door open/close under confrontation stillness. `[Explicit]` `exam_guard:260`, `exam_guard:271`, `exam_guard:508`, `exam_guard:515`, `exam_guard:646`, `exam_guard:672`
- [ ] `P1` Bag hits floor too loud in living room. `[Inferred]` `exam_guard:521`
- [ ] `P2` Mom phone tightened in hand / phone facedown on coffee table. `[Inferred]` `exam_guard:335`, `exam_guard:511`
- [ ] `P2` Upstairs floorboard tiny sound, then stillness. `[Inferred]` `exam_guard:465`, `exam_guard:676`
- [ ] `P2` Asahina fast kitchen/water/upstairs movement. `[Inferred]` `exam_guard:645-676`
- [ ] `P2` Bad-ending title-screen return sting or low system pulse. `[Inferred]` `exam_guard:730-766`

## Local Candidate Assets To Audition

These may or may not be final-quality, but they are worth auditioning before sourcing new files:

- `game/assets/audio/sfx/writing.ogg` - writing/pencil bed.
- `game/assets/audio/sfx/ac.ogg` - air conditioner bed for `0523:654`.
- `game/assets/audio/sfx/tick.ogg` - clocks/timers if it fits the tone.
- `game/assets/audio/sfx/sfx-thunder.wav` - theater thunder candidate if it has enough tail.
- `game/assets/audio/sfx/sfx-wind.wav` - rooftop/city wind candidate.
- `game/assets/audio/sfx/sfx-hollowboom.wav` - dream/meta impact candidate.
- `game/assets/archive/unused_audio/mod_assets/sfx/sfx-footsteps.wav` - hallway/track starting point.
- `game/assets/archive/unused_audio/mod_assets/sfx/sfx-bell.wav` - school bell starting point.
- `game/assets/archive/unused_audio/mod_assets/sfx/sfx-phone1.wav` through `sfx-phone5.wav` and `sfx-phonebeep.wav` - phone pack starting points.
- `game/assets/archive/unused_audio/mod_assets/sfx/sfx-pageturn.wav`, `sfx-tap*.wav`, `sfx-sketching.wav`, `sfx-scrawl.wav` - paper/writing pack starting points.
- `game/assets/archive/unused_audio/mod_assets/sfx/sfx-crowdnoise.wav`, `sfx-crowdcheer.wav`, `sfx-gallery*.wav` - gym/hall/cafe crowd candidates.
- `game/assets/archive/unused_audio/mod_assets/sfx/sfx-engine.wav`, `sfx-tirescreech.wav` - bus/racing cabinet candidates.
- `game/assets/archive/unused_audio/mod_assets/sfx/sfx-computer*.wav`, `sfx-static*.wav` - phone/UI/dream/meta candidates.

## Out-Of-Context Scenes

Written to shipping quality ahead of their chapter (`game/story/out_of_context/`), so their `# SFX SUGGESTION` lines are real requests rather than prototype noise.

### 0101 - "This Year Too" (Chapter 5, New Year's Day)

This day is the Chapter 5 audio reference and it is deliberately music-poor, which puts almost the entire first half on room tone. Everything here is `P1` for that reason.

- [ ] `P1` **New Year's variety broadcast, two versions.** The single most load-bearing missing cue in the file: sections I to IV have no music and are scored entirely by a television nobody is watching. Needs (a) a through-the-floor mix - audience laugh roughly every forty seconds, a band stab, applause, no word legible - and (b) the same broadcast in-room at living-room volume with a compere audible but not intelligible. Must loop for several minutes without a recognisable seam. `[Explicit]` `ooc_0101:294`, `ooc_0101:323`
- [ ] `P1` Dead-shopping-street winter bed - wind down a street of closed shutters, one loose sign, a vending machine compressor close enough to dominate, no traffic and no voices. Currently standing in on `sfx-wind.wav`. `[Explicit]` `ooc_0101:564`
- [ ] `P2` Single crow, close, three calls with no answer, then nothing. `[Explicit]` `ooc_0101:726`
- [ ] `P2` Konbini exterior/interior on a holiday - door chime, one fluorescent tube with a dead flicker, register beep, no queue.
- [ ] `P2` Bus shelter - wind under a roof, a timetable sheet loose at one corner, a single bus arriving and pulling out of an empty street.
- [ ] `P3` Osechi/New Year table foley - lacquer box lid lifted and set down, soup bowl, mochi, an envelope handed over.
- [ ] `P3` Bundle of New Year cards - rubber band off, postcards shuffled and squared on a table.

Note that Matsuda's ringtone in this scene is `assets/audio/bgm/enterm.ogg` played on `sfxtrack2` on purpose - it is diegetic, coming out of a coat pocket, and does not need a bespoke asset.

## Later Scope

`game/story/dev_scene_manager.rpy` contains future/prototype story scenes with additional useful cues: empty-house refrigerator/clock/light buzz, bus door hiss and phone buzz, water fountain/corridor gossip footsteps, classroom door slide, and heavier confrontation room tone. I did not fold those into the main route checklist above because they are dev/test prototypes rather than the current implemented `season1` route.

## Cut-And-Dry Shopping List

### Core Phone And UI

- Phone text received buzz, soft.
- Phone text received buzz, hard surface rattle.
- Phone text received buzz, fabric/pocket muffled.
- Phone repeated-message buzz sequence.
- Phone alarm loop.
- Phone incoming-call vibration loop.
- Phone timer buzz.
- Phone open/raise sound.
- Phone text sent sound.
- Phone text received UI blip.
- Phone thread reveal/tap sound.
- Phone contact unlock/new contact sound.
- Phone call answer sound.
- Phone call end sound.

### School

- School warning bell.
- School final bell.
- School bell heard from far away.
- School bell muffled behind a rooftop door.
- Stark exam bell with no crowd tail.
- Underwater/dream school bell.
- Hallway crowd loop.
- Hallway shoe squeaks.
- Hallway bag/cloth movement.
- Fast footsteps on corridor tile.
- Classroom quiet room tone.
- Exam-room silence bed.
- Exam-room cough/shift accents.
- Chairs scraping after bell.
- Low post-exam chatter.
- Chalk writing.
- Chalk tap.
- Classroom wall clock tick.
- Calculator power-on clicks.
- PA speaker click/crackle.
- Gym microphone feedback.
- Gym microphone cutoff pop.
- Gym crowd swell.
- Gym handclaps with echo.

### Paper, Writing, And School Objects

- Dry pen tap on desk.
- Light pen tap against page.
- Pencil writing loop.
- Pen writing loop.
- Pencil clatter on hard floor.
- Pencil slap on desk.
- Pencil rolling across table.
- Page turn.
- Paper rustle wave.
- Paper stack alignment.
- Exam packet light slap.
- Exam packet heavy slap.
- Flashcard flip.
- Sticky note peel/adjust.
- Folder slide.
- Notebook close.
- Manga/book open.
- Stapler jam/argument sound.
- Clipboard/notebook handling.
- Paper bag crinkle.
- Paper wrapper swish.
- Paper wrapper landing in bin.

### Doors And Building Foley

- Home front door open.
- Home front door close.
- Bedroom door soft close.
- Club/classroom sliding door open.
- Club/classroom sliding door close.
- Rooftop metal door latch.
- Rooftop metal door hinge.
- Empty-house front latch with room echo.
- Cafe doorbell chime.
- Store door chime.
- Locker close.
- Cabinet door open/close.
- Floorboard creak.
- Soft knock/tap outside bedroom door.

### Home And Kitchen

- Refrigerator hum loop.
- Refrigerator seal opening.
- Kettle boil loop.
- Kettle click-off.
- Toaster pop.
- Frying oil sizzle.
- Pot boiling.
- Pan sizzle.
- Microwave start.
- Sink water.
- Plate set down.
- Bowl set down.
- Glass set down.
- Chopsticks/utensils.
- Serving spoon.
- Freezer open.
- Ice cream scoop/bowl handling.
- Ice cubes in glass.
- Mug pickup/set-down.
- Tea pour or kettle pour.
- Dishes being washed.
- Quiet house ambience with pipe tick.
- Car passing outside house.

### Body, Clothing, And Impacts

- Weighted school bag thump.
- Track/gym bag thump.
- Bag strap shift.
- Cloth-muted body thump.
- Full-body thump onto rug.
- Shoulder collision impact.
- Phone-and-clothing fumble.
- Forehead thump onto table.
- Finger snap.
- Single sharp hand clap.
- Two sharp hand claps.
- Soft fist bump/knuckle tap.
- Chair creak.
- Chair pull.
- Clothing rustle.
- Lunch bag rustle.
- Wrapped toast/food wrapper handling.

### Outdoor, Transit, And City

- Residential street daytime loop.
- Residential street night loop.
- Bicycle wheel loose click.
- Vending machine hum.
- Distant kitchen/dishes through open window.
- City morning traffic loop.
- City day sidewalk loop.
- City evening storefront/traffic loop.
- Delivery cart wheels.
- Metal storefront shutters.
- Wet tires passing.
- Gutter splash.
- Bus engine groan.
- Bus pneumatic brake hiss.
- Bus doors open/close.
- Bus interior loop.
- Child shoes knocking plastic bus seat.
- Train/platform ambience.
- Train doors.
- Train passing beyond cafe/station window.

### Rooftop And Weather

- Rooftop light wind loop.
- Rooftop stronger gust.
- Paper/napkin flapping in wind.
- Outdoor courtyard/track ambience.
- Theater thunderclap with sub-bass tail.
- Rain-slick arcade racing ambience.

### Track And Sports

- Rubber track footfalls, easy jog.
- Rubber track footfalls, strides.
- Running breathing, steady.
- Running breathing, tired.
- Coach whistle, close.
- Coach whistle, distant.
- Water bottle cap twist.
- Water bottle set down.
- Track shoes on floor.
- Track bag knocking leg.
- Volleyball/gym practice distant bed.

### Theater

- Theater exterior crowd.
- Theater lobby crowd.
- Theater lobby concession/ticket bed.
- Theater seating rustle.
- Movie theater room tone.
- Loud horror movie thunder.
- Wet horror movie creature/tunnel sound.
- Movie audio tail/rumble.

### Library And Cafe

- Library hush loop.
- Library book cart squeak.
- Library stamp thump.
- Cafe ambience loop.
- Cafe playlist low bed.
- Cafe register/payment.
- Cafe water/menu handling.
- Cafe plate delivery.
- Cup on saucer.
- Sugar packet movement.
- Tableware reacting to heavy bag.
- Busy cafe crowd that can cover silence.

### Store, Bookstore, And Shopping

- Tech store crowd/checkout bed.
- Barcode scanner beep.
- Game case handling.
- Security sticker/case turn.
- Bookstore ambience loop.
- Old magazine page flips.
- Magazine stack shift.
- Rotating rack turn.
- Register counter handling.
- Twine wrapping magazines.
- Cash/coin change.
- Grocery store produce handling.
- Grocery checkout/card reader trouble.

### Games And Arcade

- TV party-game round-start jingle.
- TV/controller button taps.
- Cartoon game explosion.
- Console controller set-down.
- Board/card game shuffle.
- Cards dealt onto floor.
- Cards placed/discarded.
- Card box open/sort.
- Arcade room ambience loop.
- Arcade card tap.
- Arcade kiosk/load credit sound.
- Racing cabinet countdown.
- Racing cabinet engine.
- Racing cabinet tire scrape.
- Racing cabinet collision.
- Racing results screen blip.
- Light-gun cabinet ambience.
- Plastic light-gun shots.
- Light-gun cable catch.
- Helicopter crash/game over.
- Dance cabinet music/gameplay bed.
- Air hockey hit.
- Photo booth curtain/camera cue.
- Prize machine jingle.
- Claw machine motor.
- Claw machine metal clack.
- Plush landing/cabinet thump.
- Arcade locker close.

### Dream, Meta, And Unsettling

- Old PA speaker electrical crackle.
- Waiting-room number dispenser cough.
- Floating chalk scrape.
- Cup sliding on desk.
- Conveyor belt loop.
- Cheerful waiting music loop.
- Abrupt phone-video audio cutoff.
- Low static pulse.
- Cold exam/meta sting.
- Title-screen return sting.
- Subtle text-screen ambience for Nier/disclaimer scenes.
