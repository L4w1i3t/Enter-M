# All Addons and Side Content: What Actually Earns Its Place

## Scope

I am treating “all” literally enough to be useful. I reviewed every top-level entry under **game/addons**, the Archive that houses most of them, every currently playable Character Story, every boss and Arcade mode, every optional phone conversation, the Lost Records catalog and its hidden rewrite, and everything in **game/story/out_of_context**. I also looked at the first-run and end-of-demo material because it determines how the optional material is framed.

I am not reviewing every image, sound, shader, or helper file as if it were separate content. Those belong to the feature that uses them. I am also not counting the exam-guard branch as side content; it is conditional main-story material.

The project uses “addon” for several completely different things, so I use these verdicts:

- **Core infrastructure** means it is part of how the main novel tells its story. It should not have to justify itself as a bonus.
- **Genuine supplement** means it adds a useful angle without replacing, resolving, or pre-empting the main story.
- **Standalone bonus** means it may be good, but it is effectively another game or anthology piece bundled with ENTER M.
- **Meaningful experiment** means the gimmick is doing expressive work, even if the result is excessive or unfair.
- **Premature scaffolding** means the shell is public before there is enough content to justify it.
- **Dev-only prototype** means it is a tool, draft, or experiment rather than player-facing content.
- **Pointless gimmick** is a label I reserve for something that adds friction, clutter, or empty promise without enough payoff.

That distinction matters. “Not supplemental” does not mean “bad,” and “technically impressive” does not automatically mean “good for this project.”

## The short version

The best actual supplements are the optional phone conversations, the evolving **Current Reads** in the People menu, **Dead Fantasy**, **Heads/Tails**, and much of **Hina’s World**. They add texture or a new angle while remaining recognizably about these characters.

The strongest side works overall are not always the best supplements. **Hina’s World**, **Purgatorium**, the Kotonoha prose pieces, and the character boss fights are closer to companion games, alternate-universe essays, or headline events. Several are excellent. Several also explain a character more decisively than the main story currently does, which makes the “independent continuity” disclaimer feel less like a boundary and more like permission to publish the character bible early.

The Arcade originals are genuine games. They are not pointless, but they are not character content either. They make ENTER M partly a minigame anthology. The Anime OP is a title sequence and the next-time trailer is a promotional coda. The Developer Date Jump is a QA tool. Autofocus, the phone framework, poem display, font sizing, and the NieR-like prose mode are presentation infrastructure. Calling all of these “side content” hides the real scope problem.

My blunt overall opinion is that ENTER M currently feels like three projects sharing one executable:

1. A slow, observant character novel.
2. An alternate-fiction archive about those characters.
3. A Ren’Py technical showcase and Arcade platform.

All three contain good work. The first one has the clearest identity. The danger is not that the extras are amateurish; it is that the extras are so ambitious, numerous, and tonally loud that they can make the actual novel feel like the quiet lobby outside its own bonus features.

## The Archive shell

**Verdict: Useful hub, but premature platform signaling.**

The Archive is a coherent home for the Roster, CG Gallery, Music Room, Character Stories, Lost Records, and Achievements. The terminal-like presentation makes the collection feel intentional instead of like a list of disconnected developer menus. It also solves a real discovery problem: without a hub, the amount of optional material would be impossible to navigate.

The drawback is what it communicates. A six-module Archive available from the beginning tells the player that ENTER M is already a content platform. At present, several of those modules contain empty acts, empty folders, unavailable records, or material dominated by one source. The shell therefore advertises breadth more successfully than the current build delivers depth.

I would keep the Archive, but hide empty categories and let modules appear when they have something worth opening. A locked door can create anticipation; a room full of labeled empty display cases mostly creates an unfinished-product feeling.

The Archive source also contains a hidden **poem_archive** “Coming Soon” stub and a dormant poem-unlock flag. Because no player-facing card reaches it, this is invisible premature scaffolding rather than an additional feature. It should stay out of the runtime file until there is a real poem archive to open.

## System and presentation addons

### Achievements

**Verdict: Polished completion metagame; not supplemental, and currently overbearing.**

The achievement system is well organized, persistent, and unusually serious about auditing whether its goals are reachable. Its twenty-nine awards give collectors a reason to revisit stories and modes. As infrastructure, it is excellent.

Its reward design quietly makes a much larger claim: that reading the novel, finding optional narrative material, clearing a superboss, earning a huge bullet-hell score, completing no-miss challenges, and mastering unrelated Arcade genres are equivalent parts of “completing” ENTER M. That may be the intended product, but it is not a neutral bonus layer. A prose-first player cannot earn the top completion status without becoming good at games they did not arrive to play.

Some hidden achievements also encourage the player to seek hostile or ethically ugly branches. That can be interesting once. Across several systems, however, it contributes to the sense that the game lays traps, records curiosity, and then morally judges the person who explored what it offered.

I would split narrative discovery from challenge mastery. Give the novel and anthology their own completion track, then make Arcade feats a separate cabinet scorecard. The current system is not pointless; it is simply enforcing the project’s scope confusion.

### Autofocus

**Verdict: Justified core infrastructure.**

Automatically emphasizing the current speaker gives multi-character scenes an immediate visual grammar. The Darken, Opaque, and None preferences make the effect adaptable, and the implementation accounts for manual sprite placement and reloads rather than assuming ideal scenes.

My only substantive complaint is accessibility. “None” removes dimming but does not fully disable the speaker pop, and the underlying autofocus toggle is not exposed in Settings. Someone sensitive to repeated sprite motion should be able to turn the whole system off.

This is the kind of addon that earns its complexity because the player experiences the result rather than the machinery.

### Automatic dialogue font sizing

**Verdict: Useful invisible safety net.**

The feature measures long lines, caches the result, and shrinks dialogue that would otherwise overflow. That is sensible defensive UI work, not side content and not a gimmick.

It can, however, make individual lines visibly jump in size, and it can shrink quite far. It should catch rare accidents, not make overlong dialogue acceptable. If players regularly notice it, the prose or text box needs revision.

### Calendar System

**Verdict: Essential date infrastructure attached to a mostly empty menu.**

The live date, phone timestamps, corner badge, and day-change transition are fundamental to a story told one school day at a time. They orient the reader and give the prologue a measured rhythm. That part fully earns its place.

The browsable month calendar currently has no events, plans, deadlines, annotations, or journal data. It is an elaborate way to restate the date already visible elsewhere. The lengthy “DATE SYNC” treatment is attractive but oversized for the information it conveys.

So this is two verdicts in one: the date system is core; the calendar menu is premature scaffolding. Either let it accumulate plans and meaningful history or remove the empty grid until it does.

### CG Gallery

**Verdict: Sensible future infrastructure; a glorified OP storyboard right now.**

The gallery has twenty-two cataloged images, but nineteen are stills from the Anime OP. Only three currently come from side stories. The Season and Intermission acts are largely empty, and the OP itself is already replayable.

That makes the gallery technically functional but conceptually thin. Unlocking nearly the entire collection by watching the mandatory opening is not meaningful discovery, and empty acts advertise an imagined finished game rather than serving the current one. Path-derived unlock keys may also become brittle as placeholder art is renamed.

Keep the viewer, but do not give it such a prominent Archive presence until the main story has actual scene CGs. Hide empty acts. The current gallery is not pointless in design; it is premature in presentation.

### Credits

**Verdict: Necessary project infrastructure, not side content.**

The credits are thorough, readable, and candid about sources. That is basic responsibility, and the custom presentation is consistent with the rest of the project.

The current text also admits unknown artists, unconfirmed sources, and attribution still under review. Honesty is good, but attribution is not the same thing as permission. With commercial-game music and other borrowed material in the build, this needs a real rights and replacement pass before public distribution, especially while the main menu contains a donation link.

The feature itself earns its place. Its unfinished contents are a release-readiness warning.

### Developer Date Jump

**Verdict: Excellent dev tool; absolutely not player content.**

The date jumper discovers story labels, launches future-scene drafts, unlocks side material, exposes invasions, and provides god-mode conveniences. A polished test harness can save enormous time, and this one appears genuinely useful rather than decorative.

It does not reconstruct all prior story state when jumping into a later day, so it is suitable for smoke tests and scene iteration, not full continuity validation. That is a limitation, not a condemnation.

The interface may be indulgently elaborate for a developer menu, but unlike the empty player-facing shells it performs real work. Keep it developer-only.

### ID Card, name entry, and birthday

**Verdict: Strong diegetic onboarding buried under counterproductive validation gimmicks.**

Using an ID card to name the protagonist is much more fitting than a generic text prompt. It belongs to the opening, grounds the school setting, and participates in one of the earliest small Monika/meta moments.

The validation layer is where it loses me. It only permits a narrow ASCII name format, rejects legitimate short or international names, and contains a huge blocklist covering cast names, profanity, public figures, creator jokes, and attempted bypasses. Most of that does not protect the story; it tells the player that the author is standing over the form trying to win a naming contest.

The birthday field is stored but currently used nowhere else. Asking for personalizing information and then never acknowledging it is fake personalization. The card also prefers the default Asahiko entry rather than naturally restoring the saved name.

Keep the card. Relax the policing to what is technically necessary, support real names beyond a narrow English pattern, and either use the birthday meaningfully or stop asking. The core idea is excellent; the “anti-cheese” fortress is one of the clearer pointless gimmicks.

### Music Room

**Verdict: Good replay utility, not narrative supplement.**

Tracks unlock when the player actually hears them, and the room supports search, shuffle, repeat, track progress, and navigation around locked entries. That is exactly what a jukebox should do. Its engineering is proportionate to a large soundtrack.

The larger issue is curatorial identity. The catalog combines many tracks from existing commercial games and artists with original or differently licensed material. A music room makes that borrowing more visible: instead of functioning as a temporary cue inside a scene, it becomes part of ENTER M’s displayed collection. Randomly pairing tracks with unlocked CGs also feels arbitrary rather than curated.

I would separate original score from borrowed/temp music, complete the rights review, and eventually let the project develop a more recognizable sound of its own. As a utility, the room is worthwhile.

### NieR Forest Text Adventure Format

**Verdict: Effective core presentation language with unnecessarily borrowed branding.**

The black-screen prose mode is used for disclaimers, section cards, endings, exam material, and the Kotonoha stories. It gives the project a restrained register distinct from normal ADV dialogue and is reusable enough to be real infrastructure.

The problems in the Kotonoha stories’ attention checks are story-design problems, not engine problems. The format itself works. My only objection is the name: the presentation is general enough that explicitly branding it after NieR makes ENTER M sound more derivative than the feature needs to be. Give the house style its own name.

### Phone System

**Verdict: The most justified large addon in the project.**

Phones are not decorative here. Texting is part of how the cast maintains relationships, the saved threads give those relationships memory, and calls, group chats, avatars, timestamps, and notifications all contribute to the contemporary setting. The framework is heavily engineered, down to deterministic typing mistakes and measured compose boxes, but the main story actually uses it.

Some of the shell remains ornamental: home-screen app icons do nothing, FaceTime mute/camera buttons are inert, and main-story incoming calls cannot really be declined. Those details create the appearance of a phone simulation without equivalent agency. Still, this is overengineering around a legitimate narrative organ rather than a feature searching for a reason to exist.

The ten optional conversations are the cleanest side-content model in the project:

- **Asahina — leftovers:** tiny domestic continuity and believable sibling entitlement. Genuine supplement.
- **Asahina — spider:** almost pure sitcom garnish, but proportionate and human. Harmless flavor.
- **Asahina — wrong chat:** a setup with no meaningful resolution. A thin gag.
- **Mom — discoverable:** concise lawyer-mom humor that only she could deliver. Genuine supplement.
- **Monika — waypoint:** lets her be sincerely excited about a book without turning the moment into plot. Strong supplement.
- **Monika — asterisk:** a typo-correction joke stretched into a character beat. Near-gimmick, though it does humanize her perfectionism.
- **Matsuda — omen:** theatrics become an indirect offer to share a drink. Repeats her surface, but the bid for closeness gives it value.
- **Mom — big pot call:** generic domestic comedy, pleasant and appropriately small.
- **Monika — paragraph call:** the best of the set. Literature talk, a pause for traffic, and “get home safe” create intimacy without announcing it.
- **Matsuda — duck-hat video call:** mostly a demonstration that FaceTime works. In-character, cute, and still a system-led gimmick.

Even the weaker chats succeed by ending before they inflate into a thesis. I would add an optional replay/history index, but I would not make them louder or more consequential.

### Planner display

**Verdict: Worthwhile one-scene presentation gimmick, heavily overbuilt.**

The animated two-page planner makes one planning scene more legible and fits the protagonist’s relationship with schedules and control. It is not pointless.

It is also hundreds of lines of custom presentation for one appearance. Unless the planner becomes a recurring character tool or an interactive record of changing commitments, it remains a lavish prop. This is the benign kind of indulgence: visible, charming, and disproportionate.

### Poem display

**Verdict: Fully justified core infrastructure.**

The literature and poems are central to the character work, and the reusable presentation lets them breathe without pretending to be ordinary spoken dialogue. It is used repeatedly and stays out of its own way. No real complaint.

### Roster View and People

**Verdict: Half excellent supplement, half dated VN-database baggage.**

The **Current Reads** are one of the best optional features in the game. They let the protagonist revise his impressions after meaningful encounters, reinforce his voice, and provide a recap without interrupting scenes. I wish earlier reads were preserved as a small history instead of being overwritten; watching the judgment change would be more revealing than only seeing the latest result.

The full Roster is less convincing. Basic identity, relationships, likes, and dislikes can help in a large cast. Exact height, weight, chest/build, and game-like “secret” fields feel imported from an anime character sheet rather than discovered through humane writing. Weight data for young characters and chest measurements for adults add objectification without useful characterization. “Preferred Instrument” appears to function as an authorial motif, but the interface presents it as literal canon trivia.

Keep the evolving subjective reads. Strip the dossier down to information a player might genuinely want to remember, and distinguish symbolic design notes from facts the characters supposedly supplied.

### Sick Ass Anime OP

**Verdict: Impressive title-sequence showpiece; not supplemental, and badly placed as mandatory boot material.**

The roughly eighty-second opening is a serious piece of choreography, with beat-locked cuts, effects, fallbacks, and a large visual vocabulary. It communicates energy, ensemble scale, impending darkness, and Matsuda’s association with production and spectacle. As a demo edit or promotional music video, it has value.

As the thing shown on every launch, it is self-defeating. A new player sees future arguments, puppet imagery, a broken Asahina world, disappearance language, and imagery labeled around Sam’s villain role before learning who these people are. The OP promises a much louder and more catastrophic work than the current slow prologue. It also contains temporary-joke language—“this won’t be in the full release”—despite being wired into the actual startup, and its “barely DDLC” joke punctures its own polish.

Nineteen of its stills then dominate the CG Gallery, so the same showpiece occupies both the front door and most of the museum.

I would keep it replayable in the Archive, use it as an end-of-demo unlock, or rebuild it from current-chapter-safe material. Showing it on every boot is repeated friction. This is a meaningful gimmick and a real branding artifact, but it currently introduces spectacle before the story has earned attachment.

### Next Time, on ENTER M

**Verdict: Useful season trailer and structural coda, not side content.**

The degrading-broadcast trailer gives the quiet prologue a future-facing contract. Matsuda as a host, the TV language, the montage rhythm, and the promise of memory, illness, disappearance, complicity, and fracture all fit the larger design. It is more justified than the OP because it arrives after the reader knows the cast and because a demo needs to say what kind of continuation it is promising.

It still overplays its hand. Lines about everyone knowing, everyone looking away, and whether the player remembers how it ends pre-judge guilt and tragedy before the connecting story exists. Several fragments resemble generic cryptic accusations rather than precise hooks. It is also long immediately after an already extended chapter ending.

Keep it, but use fewer and sharper fragments. The trailer should create questions, not hand the audience the prosecution’s closing language.

### The extensionless “addons and custom features go here” marker

**Verdict: Pointless repository debris.**

It contains a tiny “why are you in here?” joke and has no game function. It is harmless, but it is the one item for which “pointless gimmick” is almost literally the complete review. Delete it or leave it outside the shipped project.

## Character Stories

### The Character Stories hub

**Verdict: Strong organizer with poor expectation-setting and visible empty promises.**

The hub clearly separates stories by subject, tracks unread/completed state, and explicitly says the stories are independent of the main continuity and may be what-ifs. That disclaimer is necessary.

It is not sufficient. All eight live stories unlock together after May 31, producing an enormous post-prologue content dump. The descriptions often conceal rather than explain the form: “You guys like RPGs?” does not tell someone that Ontological Seer is a large Press Turn boss suite, and “Inspired by Lacey Games” does not communicate that Hina’s World may take hours or contains grooming and body/food material. The hub should state approximate length, interaction type, difficulty, content concerns, and recommended order.

Player, Himeko, and Monika appear as empty folders or commented plans. Empty folders are not tantalizing when several other archives are also empty; they make the build feel like a roadmap. Hide them until a story exists.

### Dead Fantasy

**Verdict: Genuine ensemble supplement; indulgent first half.**

The fantasy war initially appears to be a straight alternate story, then reveals itself as Matsuda running a tabletop campaign for the group. The table is where it becomes valuable. Matsuda refuses to fudge open dice because an engineered ending would belong to her rather than everyone. Tsubaki asks repeatedly whether her cleric survived and is talked over. Monika counts every ignored request and finally breaks the table’s momentum to make people hear her. Asahina drops third-person roleplay when grief becomes personal. Sam insists that cost and effort should mean something.

That is excellent supplemental characterization because it shows the ensemble making something together. It also complicates Matsuda’s control: she wants the grand ending, but she respects shared authorship enough to accept a draw.

The long fantasy section before the table reveal is much more generic. Campaign logistics and melodrama take up space that the interpersonal aftermath uses better, and the story lands its ending more than once. The easy group intimacy also previews an equilibrium the main story has not reached.

Keep it, trim the war, and file it honestly as an ensemble story rather than pretending Matsuda is its only subject.

### Ontological Seer

**Verdict: Bonus-game hub misfiled as a Character Story.**

Matsuda’s performance, pattern obsession, ego, clean-loser streak, and desire to turn interaction into spectacle all make the boss concept character-congruent. There is a real idea here: to know Matsuda is to engage a system she has staged and then demonstrate that one has learned its rules.

The wrapper itself offers little new characterization. The actual content is a party-building RPG fight, its superboss escalation, and the alternate Monika, Kotonoha, and Tsubaki modes it unlocks. Its scale, controls, difficulty, and genre requirements are hidden behind a deliberately vague catalog description.

This belongs under Arcade or Challenges, with an assisted/story-view option for readers. It is worthwhile, but calling it a story confuses technical spectacle with narrative substance.

### Heads

**Verdict: Excellent genuine thematic supplement, if read as allegory.**

The quiet mender removes cracks and flaws from her loud friend with a needle of noticing, cataloging each repaired piece until care becomes possession. It is a sharp gothic x-ray of how Tsubaki’s attention, service, and desire to be indispensable could curdle into control.

The story does not need to be literal biography to matter. In fact, it is stronger as a possible emotional shape than as a secret factual explanation. The risk is filing something this specific under Tsubaki and then relying on a continuity disclaimer to stop readers from treating it as prophecy.

### Tails

**Verdict: Essential companion to Heads, not redundant.**

The reverse perspective reveals that the loud friend rigged the coin, knowingly returned, wanted to be found without having to confess need, and experienced the archive of flaws as proof that someone had counted her. That changes the moral shape from simple predation to mutually reinforcing codependence.

Together, Heads and Tails are the strongest pure prose in the side catalog. Their fake coin choices changing nothing are thematically defensible, although they join a larger project habit of offering agency mainly to comment on its absence. The aphoristic prose occasionally reaches for a quotable line in every paragraph.

Require Heads before Tails, present them explicitly as paired, and trim lightly. These earn their place.

### Hina’s World

**Verdict: Outstanding companion game; too foundational and too large to be a mere supplement.**

The simulated old Windows/Flash environment is the most convincing case in the project for form doing narrative work. Dress-up tools, lunch games, pets, makeover screens, chats, guestbook entries, files, diaries, and photos let the player encounter a child’s self-construction as an environment rather than as an explanatory monologue. The grooming escalation is especially effective because the stranger begins with useful, publicly defensible attention, moves toward private contact, isolates, and only gradually asks for an image. Asahiko’s intervention and Mom’s response connect the family’s present vigilance to something concrete.

It deepens Asahina’s performed maturity, body and food anxieties, appetite for validation, childish tastes, divorce-era instability, and dependence on her brother. It is also thousands of lines, seven mini-apps, multiple value axes, extensive filesystem exploration, and potentially hours of play. The central danger can disappear beneath completionist clicking, and logging off early can still count as completion without making the missing closure obvious.

The specificity creates a canon problem. A disclaimer says “independent,” but this story supplies such a comprehensive causal file that most readers will use it as the explanation of Asahina. It risks turning a complicated present person into the output of a childhood dossier. The grow/kept-child choices also sometimes make ordinary aesthetic preferences stand in for maturity or regression when the real issue should be pressure and compulsion.

I would either release it as a clearly labeled companion title or divide it into resumable sections with explicit progress, length, and content guidance. It is one of the best things here. It is also evidence that the side project can eclipse the main one.

### Purgatorium

**Verdict: Powerful standalone horror essay; unfair as interaction and harmful as early supplement.**

The fake mobile romance game turns Sam’s way of seeing people into Affection, Trust, Desire, and Dependency meters. Deleted contacts, skipped self-description, invasive permissions, fake crashes, repeated doors, and the warm phone in darkness all support the same accusation: he learns enough to lower walls, not enough to know a person, and leaves the silence arranged so that she cannot move on.

The form is strong. The prosecution is rigged. The script forces screenshots, skipped backstory, stat fixation, compliance, and continued play, then accuses “you” of making those choices. There is no genuine route in which the player reads carefully, resists, exits, or refuses the predatory logic. The piece creates the evidence and then blames its captive witness. Its climax also arrives in too many waves: confrontation, crash, mirror space, device invasion, fragment assault, stat reveal, quiet bedroom, and ransom image all restate the thesis.

More importantly, it settles Sam. The main story is carefully constructing ambiguity around charismatic care, monitoring, shame, and control. Purgatorium declares a broad history of serial manipulation and ghosting. Once read, every gentle main-story action becomes evidence for a verdict already delivered.

This is not pointless. It may be the catalog’s most effective horror piece. It should appear after the relevant main revelation, be labeled as an alternate indictment, or be rewritten to give resistance real meaning. Right now it competes with the novel instead of supplementing it.

### The Girl with Every Face

**Verdict: Meaningful alternate biography weakened by repetition and a punitive gimmick.**

Kotonoha masters roles so completely that other people mistake flawless service for identity. The grandmother is the first person to ask whether she is happy and then actually wait. The imperfect bow after the funeral is a small, effective original gesture. The core is poignant and makes her many jobs feel less like a running gag.

It also provides nearly all of Kotonoha’s interiority while the main story still uses her mainly as a recurring cameo. That makes the piece closer to a dramatized character bible than an optional angle. Its movement-by-movement symmetry reconfirms the same discovery after the emotional center has already landed.

The seven exact-recall checks are actively bad. Missing an arbitrary detail causes “You weren’t listening. No one ever does” and ejects the reader without completion. Remembering a coat color is not the same as caring, and punishing someone near the end of a long literary story does not deepen the theme. It converts Kotonoha’s hunger to be read into the author policing attention.

Remove the quizzes or turn them into reflective questions with no ejection. The prose story itself is worth keeping.

### The Void Hunter

**Verdict: Worthwhile parable, but duplicative and less specifically Kotonoha.**

The postwar swordswoman carries purpose as a weapon, searches for one final act that would justify fifteen years of damage, and eventually puts the sword down without pretending the urge has vanished. The abandoned objects, stew, ordinary child, and open shaking hands create a credible argument for living without first solving one’s grand meaning.

The weakness is comparative. It again uses titled movements, accumulated examples, a reflective journey, symbolic objects, and eventual release. After The Girl with Every Face, the structure feels like a house template. It could describe many traumatized veterans rather than uniquely illuminating Kotonoha.

It repeats the same seven hostile memory checks, which should be removed for the same reason. The current source does establish “The Recess” before asking about it; an older version’s continuity bug is no longer present.

Keep it if the prose is differentiated and tightened. Otherwise, the two Kotonoha epics start making her feel like a theme repository rather than a person.

### Empty and shared Character Story files

**Verdict: Maintenance scaffolding, not content.**

The Player “Coming Soon” and Himeko “Continuance” files are comment-only placeholders. Monika’s “Lies and Poems” is referenced by stale defaults/catalog planning, but its source is absent. The shared Tsubaki gothic file is a prose engine, not a third Tsubaki story.

None of these should count toward the advertised story catalog. Move plans to development notes and keep empty folders out of the player UI.

## Matsuda’s Sick Boss Fight family

This suite is roughly a separate game embedded in the novel. Its systems, effects, pause handling, party design, and genre shifts show real craft. The correct criticism is not “these are fake games.” They are real games. The question is whether ENTER M benefits from owning all of them.

### Ontological Seer — normal

**Verdict: Character-congruent RPG spectacle; meaningful bonus, thin supplement.**

Choosing four from the cast, managing rows, affinities, buffs, scans, press turns, and Matsuda’s changing patterns gives the fight genuine party-building depth. Her second phase reads aggression and stalling, which fits a character obsessed with controlling and interpreting the room.

Spectacle still outweighs insight. Matsuda already performs, escalates, protects open rules, and wants to be learned. The fight mostly says those things at enormous mechanical volume. The intentionally tiny first-phase HP makes its elaborate opening mechanically fake, and selecting “I want to leave” on the repeat roster can quit the whole application—an actively hostile joke. Victory unlocks a Seer CG that is not actually displayed during the encounter.

Keep it as a clearly labeled Arcade challenge, fix the exit behavior, and add an assisted route. It should not be the price of reaching other character material.

### Ontological Seer: Id

**Verdict: Maximalist superboss, not supplemental.**

The larger boss, full cast, bullet-hell interludes, typing, timed questions, and genre shifts are Matsuda’s escalation instinct turned into a mode. For players who want a Ren’Py superboss, it has real value.

For everyone else, it is an unrelated mastery test attached to a character archive. Some quiz answers state the intended interpretation so directly that gameplay becomes a delivery device for authorial answers. This belongs unapologetically in a Challenge cabinet and nowhere near narrative completion requirements.

### A Fine Date

**Verdict: Smart alternate mechanical essay with severe UX and continuity problems.**

Only Monika has “health.” Cold refusal damages her composure; warmth and hesitation restore it. The player must keep saying no until a perfect date can no longer make love irrefutable. The ending’s best thought is that staying present and telling the truth can be kinder than comforting compliance.

In practice, the mode belongs more to original/meta DDLC Monika than to the current main-story character. It asks for many repeated refusals, shrinks reading windows to roughly a second and a half, and culminates in a response layout whose correct answer is effectively reduced to mashing the top option. Worse, it disables the normal game menu without exposing a reliable pause/escape route, so a player can appear trapped until winning or closing the program.

Clearly label it noncanon, move it to Arcade, add timing/accessibility controls and a real exit, and cut the repetitions. Meaningful gimmick; not fair supplement.

### Embodiment of Violet Ink

**Verdict: Excellent character/game metaphor that becomes a full Touhou fangame.**

Kotonoha’s masks, unread messages, work, invisibility, memorable scenes, and inability to locate a self become eight spell cards. “Reading” the bullets is a genuinely elegant way to make attention physical. Practice and Endless modes show that this is not a fake set piece but a proper score-driven bullet hell.

Eight health bars, no ordinary difficulty setting, and no narrative checkpoint make the character value inaccessible to many prose readers. Endless mode adds cast masks and explicit Undertale-soul cards, increasing reference density without adding much Kotonoha insight. Touhou, School Days, Undertale, and ENTER M all compete inside one character’s metaphor.

Normal mode is a meaningful alternate-form study. Endless is fanservice/challenge expansion. Add an assisted no-record story view and stop using “training wheels” or “NOOB” language around accessibility.

### The Unwritten Act

**Verdict: Ambitious noncanon nightmare and probably the strongest system/story fusion; still not supplemental.**

Tsubaki hangs on five strings in an Undertale/Deltarune battle grammar. Zero attack, healing needles, ordinary-kindness ACTs, violence, patience, cutting strings, and late betrayal all express her need to be chosen and the danger of turning control into rest. Matsuda insisting she did not write the fight is a good rupture. The small remembered details keep the dependency theme personal.

It also performs what feels like a future emotional climax before the main story has earned it. Violence, a very long pacifist route, and betrayal all converge on the same fall and reset, with different condemnation layered over the result. Offering FIGHT and then moralizing the player for using it is easy; making nonviolence genuinely alter the relationship is harder. Here, enormous effort mainly changes the wording of failure.

Keep it as a clearly alternate nightmare unlocked after relevant main-story development. Shorten it, provide difficulty controls, and let route behavior leave more meaningful residue. It is a meaningful experiment, not casual character context.

### Shared fight infrastructure and debris

**Verdict: Real support code plus cleanup needs.**

The custom pause/forfeit handling is justified because normal Save, Load, and Main Menu behavior can corrupt live combat state. Several concept images and old assets are unreferenced, and the Seer CG is unlocked without being shown. Those are packaging/cleanup issues, not content.

## Arcade

### Arcade hub

**Verdict: Polished replay room fused to a separate minigame anthology.**

The hub exposes five story-derived modes and five original cabinets, with records, warnings, fixed-timestep infrastructure, and careful teardown. It says “NO STORY ATTACHED,” but story-derived modes can be launched before their prerequisites after only a spoiler warning. That slogan is therefore false in both directions: half the room absolutely contains story material, while the original half is genuinely detached.

The replay room is useful. The original cabinets are scope expansion. I would keep the former inside ENTER M and seriously consider packaging the latter as a separate free Arcade/portfolio companion. At minimum, separate narrative completion from cabinet completion.

The inert **Coming Soon** cartridge is pure placeholder. Remove it until there is something to announce.

### Ouroboros Protocol

**Verdict: Strong standalone arcade remix.**

Snake pickups decay into permanent hazards; purging, multipliers, fresh samples, and sprinting at the cost of one’s own length create actual score strategy. It is probably the most mechanically distinctive of the original cabinets.

The lab fiction is a skin, not worldbuilding. That is fine. This is a good small game and not a supplement.

### Peer Review

**Verdict: Clever writing-themed gimmick with enough mechanics to earn itself.**

The Breakout manuscript has supported, entrenched, cited, redacted, respawning, and revised material, plus errata and powerups. It is witty, readable as a joke about revision, and more connected to ENTER M’s concerns than the other original cabinets.

It still does not teach us anything about the story or cast. Keep it as a polished toy, not as evidence of narrative scope.

### Intake

**Verdict: Very complete falling-block game; clearest “because I could” indulgence.**

Seven-bag generation, rotation rules, hold, ghost pieces, movement timing, lock delay, and contaminated rows make it a legitimate modern falling-block implementation.

That completeness is also the critique. It is the least narratively distinctive cabinet and duplicates an entire established game genre inside a VN. Good execution cannot answer the opportunity-cost question. If any original belongs in a separate Arcade package, this is the obvious example.

### Containment Sweep

**Verdict: Clean Minesweeper bonus, almost entirely decorative to ENTER M.**

Safe first click, chording, multiple board sizes, keyboard/mouse support, and best times make it a competent version of the game. The containment terminology provides a cohesive skin.

It is pleasant filler. Calling it more would be dishonest. Not pointless if people enjoy it; completely non-supplemental.

### Board Meeting

**Verdict: Astonishing overbuild and the clearest scope warning in the repository.**

This is a real chess engine with castling, en passant, promotion, draw logic, search, transposition tables, quiescence, pruning, and four opponent personalities, including an adaptive session model. As software craft, it is remarkable.

As an addon to this novel, it is almost absurd. “Grandmaster” overstates what is really a strong-club engine, and the adaptive model—arguably the part most connected to the project’s watched/meta theme—disappears after the session. Search is frame-sliced to avoid freezing, though it can still consume a large portion of a frame.

Chess fans may get more replay from this than from any side story. That does not make it supplemental. It makes ENTER M a launcher containing a chess product. This is the feature I would point to when asking whether the project is pursuing its strongest work or demonstrating that every idea can be implemented.

## Archivist Invasions

**Verdict: Impressive unwired prototype, not current content.**

The master switch is off, nothing in the live story calls the system, and the source labels it “DRAWING BOARD.” Seven genre invasions are planned—Biography, Horror, Nonfiction, Mystery, Comedy, Tragedy, and Fiction—but only Biography exists. The other six are design notes, not addons.

Biography is itself a substantial prototype. A silent entity “wearing Matsuda” begins in an EarthBound-like menu battle, then tears away the interface into real-time dagger and glaive combat. The state words, rolling health, shader work, and interface rupture create atmosphere. The intended biography/filing idea and the distinction between the Archivist and Matsuda are mostly legible only from comments, however. A player would primarily experience a difficult Matsuda-shaped attack appearing without explanation.

The planned repeat-run model—rare random interruptions, unbeaten pools, all seven needed for a larger unlock—could make rereading feel haunted. It could also make it a rare-event action grind. Every invasion adds another mechanical vocabulary to a project already mixing RPG combat, bullet hell, Undertale, chess, mobile horror, desktop exploration, and prose quizzes.

Keep the whole system dev-only until the main narrative earns its ontology, failure/resume behavior is accessible, and more than one genre exists. It is neither pointless nor supplemental yet. It is R&D.

The six unbuilt ideas may be promising—Horror as a dwindling resource, Nonfiction reporting truths, Mystery withholding visibility, Comedy requiring participation, Tragedy announcing an unavoidable end, and Fiction rewriting rules—but they are notes, not content and should never be counted in feature totals.

## Lost Records

### Lost Records hub

**Verdict: Creator archaeology, not ENTER M supplementation; mostly placeholder in its current state.**

The museum concept is valid. Preserving older projects can show where themes, voices, and techniques came from. It should be explicitly framed as author history outside ENTER M continuity.

Only one of five catalog cards is playable. **The Answer**, **SVHS TAP-05052022**, **Doki Doki Funni Club**, and **DDLC: Lost Media** are logos, dates, genres, and “NOT RESTORED” notices. Those are index cards, not side stories. Four unavailable records around one restored piece make the museum feel unfinished rather than expansive.

Hide unrestored entries or put them in a small archival index rather than presenting each as a destination.

The Lost Records directory also contains a zero-byte “lost records stories go here” marker. It has no runtime or archival value and can simply be removed.

### Mika: A DDLC Short Story — Original Record

**Verdict: Interesting 2021 artifact, not a current-quality supplement.**

Child Mika watches Monika discover the console and conclude that their reality is false. Monika abandons her “to protect her.” Years later they meet in debate club, and Mika’s fixation begins turning threatening as she plans an indirect route to an answer.

The premise contains recognizable ancestors of ENTER M’s control, protection, abandonment, and metafiction. The prose is far below the current project’s standard: tense problems, repeated exposition, abrupt transitions, inconsistent child voice, and missing connective development in Mika’s later escalation. Listing it simply as “Slice-of-Life” is misleading, and finishing it sends the player to restart/quit rather than cleanly back to the Archive.

Keep it only as a preserved artifact labeled something like “Original August 2021 version, substantially unedited.” Its roughness is the point of a museum; pretending it is ordinary bonus fiction helps nobody.

### Mika — hidden 2026 rewrite

**Verdict: Substantial unreleased retelling, but not really a Lost Record.**

The rewrite gives the Mika/Monika relationship a fuller tragic arc: Monika eventually transfers administrative control through love, guilt, and exhaustion; Mika becomes the seeker and turns toward the Literature Club. It is much stronger than the original and complicates Monika rather than using her only as an inciting wound.

It is still long and motif-saturated. Doors, keys, edges, finding, and polished aphorisms recur heavily, and very young children sometimes speak like finished literary adults. Its meta lore could also muddy ENTER M’s own ontology.

Most importantly, a ground-up 2026 rewrite is new work, not a recovered 2021 record. If restored, present it as a clearly separate modern reinterpretation alongside the artifact, not as if both have the same archival status.

## Out-of-context material

This folder is reachable through the Developer Date Jump, not through the player’s normal path. Its completed pieces are future main-story drafts. Its incomplete pieces are notes. Calling any of them shipped “side content” would misrepresent their job.

### June 4 — Out of Ten

**Verdict: Strong future main-scene draft, not supplement.**

Daichi asks Matsuda out, tells her she belongs on TV, and receives a highly public dissection of the transactional expectation behind the request. In private, Matsuda explains that a quiet no often invites another attempt later. The protagonist refuses to become a jealousy-triangle lead, and the imported orange soda finally receives a rating of seven.

The public takedown is memorable and the actor wound gives the TV comment real weight. It also humiliates a basically decent boy at greater length than necessary, a discomfort the scene only partly acknowledges. This belongs in continuity with the consequences around it, not as a floating optional vignette.

### June 12 — Reception

**Verdict: A system demonstration with enough warmth to earn a smaller life.**

Mom calls from a deposition hotel over bad Wi-Fi, asks whether the protagonist ate and locked the door, and says goodnight twice. It is ordinary, specific, and charming.

The source openly exists to prove the FaceTime system. That is a warning sign: content should not be invented only because a feature lacks a use. This one survives because the interaction feels true. If retained, it would work better as an optional phone vignette than as a load-bearing dated scene.

### October 26 — Passed Out

**Verdict: Effective future plot scene with rough tonal breadth.**

Mom’s rare drunken collapse begins as broad boat/rice/fish comedy and turns when the protagonist notices a thrown medical pamphlet, smooths it, and deliberately does not read it. Asahina declines to record Mom even though she jokes about it. The scene reveals family care through avoidance and preserves the protagonist’s agency in not knowing.

The rug pull works. Some comedy and phrasing are rougher and more caricatured than the current main-story voice. This is a major illness seed and clearly belongs in the future plot, not an extras menu.

### October 30 — Uh Oh

**Verdict: Excellent future ensemble draft, extremely spoilery and somewhat overlong.**

Six friends play a knockoff UNO game until an unseen text from Mom terrifies Asahina. She fixes her face and returns; Sam quietly rights her chair and offers care; Matsuda initially misses the room, then changes; Tsubaki lets the wrong final card stand after recognizing distress. Small reactions make the group dynamic credible.

The long CRISIS! rules and briefcase riff establish normality, but they run past the point needed for contrast. The scene gives away major Sam/Mom/Asahina stakes without connective tissue. It should eventually become main story, where those consequences can breathe.

### Deleted OOC tombstones

**Verdict: Not content.**

The January 1 “This Year Too,” October 30 “Nothing to Add,” and December 24 “Closing Exercises” files contain only comments saying they were deleted or will be rewritten. Remove them from runtime source or move the notes to a planning document.

### December 24 — Unasked

**Verdict: Unwritten route design, not content; conceptually risky.**

The comment-only plan imagines a hidden dependency ending in which the player “saves” Tsubaki from Sam and becomes an even worse controlling replacement. It includes planner dependence, awareness that Matsuda bends the narrative, directives, and abort routes.

There is a potentially strong critique of rescue fantasies here. The current notes also repeat the project’s most concerning habit: secretly track behavior, offer participation, reveal that the player was building abuse, then prosecute the player from a position of total authorial control. Describing the replacement as “worse than Sam” and planning extreme hatred or “psychotic” presentation could sensationalize dependency rather than understand it.

Before implementation, it needs fair warning through character response, meaningful opportunities to change, and careful distinction between care, dependence, coercion, and mental illness. Keep it in design notes until then.

## Adjacent first-run and story paratext

### First-run terms/disclaimer

**Verdict: Necessary development disclosure, badly voiced.**

Saying that the build is early, placeholders exist, and AI-assisted art may appear is useful. Immediately arguing with imagined critics—“talentless hack,” brick-wall rhetoric, and dismissing imagination concerns—spends player goodwill before the story starts. A disclaimer should disclose facts and boundaries, not win a fight with someone who has not spoken.

The mature-topic note is too vague to function as a useful content warning.

### Cold DDLC-style warning

**Verdict: Theatrical horror branding, not informed consent.**

“Not suitable for the faint of heart or the sensitive” is inherited genre language, but it stigmatizes the audience and tells them nothing actionable. Keep a short tone warning if desired; add specific, spoiler-conscious content and accessibility information elsewhere.

### Pre-Day-1 prose disclaimer

**Verdict: Effective diegetic prologue, not a real choice or warning.**

The fiction/coincidence language, school-year frame, and “generous-looking stretch of road” establish mood well. Proceed versus do not proceed is theatrical because refusal simply quits. That is fine as ritual, but it should not be mistaken for meaningful agency or adequate warning.

## Final triage

### Keep and foreground

- The Phone framework and its small optional conversations.
- Current Reads in People, ideally with a history.
- Poem display, Autofocus, font overflow protection, and the core date system.
- Dead Fantasy.
- Heads and Tails as an explicitly paired allegory.
- Hina’s World, but as a clearly scoped companion experience with progress and content guidance.
- The Archive once it hides empty rooms.
- The next-time trailer in a tighter form.

### Keep, but relabel as a different product category

- Ontological Seer and all character fights: **Arcade / Alternate Challenges**, not ordinary Character Stories.
- Purgatorium: **alternate horror indictment**, ideally post-reveal.
- The Kotonoha prose stories: **alternate biographies/parables**, without attention-test ejection.
- The five Arcade originals: **standalone bonus anthology**, with separate completion.
- The Anime OP: **replayable promotional edit**, not mandatory every-boot exposition.
- Lost Records: **creator archive outside continuity**.

### Hide until there is real content

- Empty Character Story folders.
- Empty CG acts.
- Four unrestored Lost Records destinations.
- The Arcade Coming Soon slot.
- Archivist Invasions and its six design-note encounters.
- Comment-only OOC and Character Story stubs.

### Remove or redesign

- The massive name blacklist and narrow name validation.
- Unused birthday collection.
- Kotonoha’s exact-recall ejection quizzes.
- Whole-application quit jokes inside a repeatable boss menu.
- Any challenge achievement required for narrative completion.
- Inert phone controls presented as functional.
- The extensionless joke marker.

## Coverage checklist

For clarity, the top-level addon inventory covered here is:

| Top-level entry | Where it is reviewed |
|---|---|
| Achievements | System and presentation addons |
| Arcade | Arcade |
| Archivist Invasions | Archivist Invasions |
| Autofocus | System and presentation addons |
| Calendar System | System and presentation addons |
| CG View | System and presentation addons |
| Character Stories | Character Stories |
| Credits | System and presentation addons |
| Developer Date Jump | System and presentation addons |
| ID Card Name and Info | System and presentation addons |
| Lost Records View | Lost Records |
| Matsuda’s Sick Boss Fight | Boss Fight family |
| Music Room | System and presentation addons |
| Next Time Trailer | System and presentation addons |
| Nier Forest Text Adventure Format | System and presentation addons |
| Phone System | System and presentation addons |
| Roster View | System and presentation addons |
| Sick Ass Anime OP | System and presentation addons |
| auto_dialogue_font_size.rpy | System and presentation addons |
| planner_display.rpy | System and presentation addons |
| poem_display.rpy | System and presentation addons |
| addons and custom features go here | System and presentation addons |

The related Archive shell, all ten optional phone conversations, all eight playable Character Stories, five story-derived Arcade modes, five original Arcade games, the playable Archivist prototype, five Lost Records cards, the hidden Mika rewrite, all eight out-of-context files, and the adjacent first-run material are also covered above.

## Bottom line

Very little here is pointless in the sense of showing no craft, thought, or entertainment value. The sharper criticism is that too much of it wants to be the main event.

The project is at its best when an extra leaves the character slightly more alive than it found them: a page number treated as a waypoint, Mom saying goodnight twice, Matsuda using an omen to offer a drink, Tsubaki’s parable changing when the coin turns over. Those pieces trust small evidence.

It is at its weakest when a system demands that the reader master a foreign genre, remember arbitrary facts, submit to a forced action, or enter an empty archive so the project can prove how much machinery exists. The repeated habit of manufacturing a trap and then judging the player for stepping into it is especially worth breaking. One such confrontation can be powerful. Across Purgatorium, Tsubaki’s routes, attention quizzes, secret achievements, fake choices, and planned dependency content, it begins to feel less like moral insight and more like the author reserving the right to be right.

My recommendation is not to delete the ambitious work. It is to impose a product hierarchy:

1. Let the main novel establish the characters and earn its revelations.
2. Let true supplements stay small, optional, and additive.
3. Label alternate essays as alternate essays.
4. Put mastery challenges in a clearly separate Arcade track.
5. Hide prototypes and empty promises until they are real.

If that hierarchy is enforced, the addons become evidence of range. Without it, they risk making ENTER M feel like an excellent character story continually interrupted by the need to demonstrate that it can also be everything else.
