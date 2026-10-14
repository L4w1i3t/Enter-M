# =============================================================================
# KANGAROO COURT -- Himeko character story 01
# Foundation dated 2026-09-04. COMMENT-ONLY OUTLINE; NOT A PLAYABLE STORY.
# Companion: docs/assets/kangaroo_court/README.md
# =============================================================================
#
# Scope: establish the story, case, prosecution-side game design, art needs, and
# continuity boundaries for a later implementation. Every nonblank line remains
# a comment. No entry label, character definitions, gameplay, unlock, completion,
# achievement, gallery registration, or changes to main-story state belong here
# yet. The existing Himeko catalog placeholder stays unavailable.
#
# AUTHORIAL CONTRACT
# ------------------
# Himeko is in her late twenties; Asahiko is four. Follow Himeko's perspective
# through the case that ends her criminal-law career, then her leave, departure
# from her employer, time with her family, and gradual return as a civil lawyer.
# The court mechanics initially offer the satisfaction of testing an argument
# and making a careful case. Their limits become personal when a child testifies.
# A shooting interrupts the court immediately before the verdict. Himeko knows
# exactly what she witnessed; the audience is deliberately not given that
# account. The player cannot prevent the event, identify a shooter, establish a
# casualty list, or uncover a withheld answer through another route.
#
# The ending is her embrace of her own child at home. He remains four: he can
# notice crying, ask a literal question, and complain that a hug is too tight.
# He cannot understand the case, counsel her, or become responsible for recovery.
# Recovery takes time and support; civil practice is a chosen professional
# boundary, with lasting effects still present years later.
#
# CONTINUITY AND WORKING CAST
# --------------------------
# HIMEKO -- late twenties, existing identity and recognizable visual features;
# surname unspecified. A career public prosecutor in a district public
# prosecutors office, with a supervising prosecutor and established case team.
# Latest author correction supersedes the earlier private-firm premise: there
# is no private employer or special appointment for this hearing. The public
# office prosecutes for the state; the bereaved family is not her private client.
# This dramatized unnamed court borrows Japanese professional/procedural details
# without claiming to reproduce a Japanese homicide trial's precise tribunal
# composition or treating an Ace Attorney single-judge setup as legal fact.
# The judge in scene directions is the presiding speaker, not a promised sole
# decision-maker. Lock the visible tribunal composition at implementation time.
#
# Her voice is measured, complete, practical, and dryly lawyerly. Younger means
# less settled in her professional armor, not naive, incompetent, or teenage.
# She checks the next task when feeling threatens to interrupt the current one.
# Her legal skill and warmth are already hers, not gifts bestowed by trauma.
# The visual departure from current Mom must be noticeable: shoulder-length
# chestnut lob, no glasses, navy blazer, high ivory blouse, burgundy neck ribbon,
# and a prosecutor's badge (red sun, white chrysanthemum petals, gold leaves).
# Art direction revised 2026-10-12: crisp ink contours, decisive cel shadows,
# saturated courtroom staging and expressive Ace Attorney fangame performance.
# Preserve Himeko's adult proportions, identity and outfit; never age her down.
#
# OFFICE LEGAL ASSISTANT -- voice only; name and gender unassigned. This is the
# public-office support counterpart to the original paralegal premise. Himeko
# asks this colleague to cover reception, existing administrative work, incoming
# press requests, and
# routine case logistics while she is at court. Her boss ordered someone to
# remain at the office because the viral case may draw callers and visitors there.
# Any work needing a prosecutor's legal judgment goes to the duty prosecutor;
# the assistant covers administrative work and never inherits legal authority.
# Boss remains offscreen and unnamed; do not invent a whole office hierarchy.
#
# STAN DARD -- provisional pun on "standard." Generic middle-aged defense
# attorney: thinning hair, glasses, ordinary suit, well-used briefcase. The name
# can earn one early beat; his competence must survive the joke. He contests the
# state's proof and guards the accused's rights without becoming cruel or evil.
# He makes some valid objections that Himeko accepts. Once Haru takes the stand,
# retire comic music, gag animation, and name-pun banter.
#
# NAOTO MORI -- provisional. Bereaved family complainant, living brother of
# murdered Kenji and brother-in-law of murdered Aya; father of seven-year-old
# Haru. This is the living character the request calls "the plaintiff." In the
# criminal proceeding the state is the formal prosecuting party; Naoto is the
# family representative, not Himeko's private plaintiff/client.
# Naoto signed the complaint and is an adult witness to earlier events. His own
# testimony concerns the neighborhood dispute and what he personally observed,
# not an invented eyewitness account of the killings. He was not in the house.
# He wants a conviction and also wants his son to get through the day. Let those
# wants collide in small conduct rather than a speech assigning blame to Haru.
#
# HARU MORI -- seven, Naoto's son, visiting his aunt Aya and uncle Kenji when they
# were killed. A protected minor witness, first brought into the courtroom in
# the second half. He witnessed the killings; the story does not reproduce that
# graphic recollection. His live testimony is limited to the necessary disputed
# return, not a demand to retell everything he suffered. He remembers ordinary
# kindness from the accused: Kurose once
# repaired the loose wheel on his toy car and knew where Aya kept spare mugs.
# Those memories are real. His trust and the acts he saw cannot fit together.
# Keep his language concrete, limited, and sometimes mistaken about procedure.
# He can say he does not remember; a pause is never an admission of dishonesty.
#
# KENJI MORI / AYA MORI -- provisional. The two homicide victims, husband and
# wife, neighbors of the accused. They remain dead throughout. Their ordinary
# lives exist in a few case-file details, not merely the method of their deaths.
# No living "victim's son" is silently substituted for the established family:
# Haru is their nephew, and his own father Naoto remains alive before the event.
#
# MASATO KUROSE -- provisional. The accused, guilty of both murders. Formerly a
# familiar neighbor with ordinary kindnesses, grievances, and adult choices.
# Kenji reported irregularities in a neighborhood repair fund Kurose handled.
# Kurose blamed him for the ensuing exposure and consequences. The grievance is
# a working motive, not a justification or a claim that hardship causes murder.
# He killed Kenji, then deliberately returned and killed Aya after an interval.
# Aya had tried to call for help. The state proves those choices; Haru never has
# to explain a motive, determine guilt, or supply an account of either wound.
#
# ASAHIKO -- four-year-old MC, fixed historical identity. Use "Asahiko" or an
# age-appropriate generic child nameplate, never the current save's player name
# or the teenage mc Character/image. He is safely at home with an offscreen
# trusted adult. Do not invent a father's status, an exact sibling timeline, or
# a named carer. Himeko reaches the doorway before the child comes to greet her.
#
# JUDGE / CLERK / BAILIFF / INVESTIGATOR / WITNESS SUPPORT WORKER -- functional
# supporting roles. Keep them human and capable; the later violence does not
# retroactively require everyone to have been incompetent or corrupt.
#
# CASE SPINE AND EVIDENCE DESIGN (PROVISIONAL DETAILS, FIXED OUTCOME)
# ----------------------------------------------------------------
# The press has already reduced the case to an obvious monster and a sure win.
# The docket contains two deaths, two charges, and an evidentiary burden that
# remains the state's regardless of publicity. Himeko expects a demanding but
# manageable final hearing after prior case preparation and admitted testimony.
#
# Kurose admits being present and causing both deaths, but the defense disputes
# the state's account of deliberate murder: one continuous emergency, perceived
# self-defense, and a confused escape. This is a position Himeko must answer,
# not permission to label all defenses dishonest. No alternate innocent killer
# or hidden exonerating ending will later contradict the completed proof.
#
# Evidence is introduced before the player needs it. Files state observation,
# source, chain of custody, and limits; separate a fact from an inference.
# Motive and character alone never establish identity, intent, or both counts.
# No magic enhancement, surprise confession button, or weapon-label shortcut.
#
# E01 -- ADMITTED SCENE PLAN / DOOR INSPECTION.
#   Rear kitchen door, internal passage, front exit, and sightlines are fixed.
#   The kitchen door latches when shut; exterior return requires opening it.
#   The plan supports movement claims, not mental state. Do not manufacture an
#   impossible view through a wall to make any witness or puzzle work.
# E02 -- EXTERIOR CAMERA EXTRACT / VERIFIED CLOCK OFFSET.
#   Same interval shows a person leaving and later returning along the side
#   passage. The image alone cannot establish a face or what happened indoors.
#   A documented clock offset makes the relationship to E03 interpretable.
# E03 -- EMERGENCY CALL CONNECTION RECORD.
#   Aya's call connected between the two exterior movements. The defense may
#   inspect the full relevant record; the player gets a neutral transcript of
#   the relevant timing, not a collectible recording of a person's suffering.
# E04 -- RECOVERED INSTRUMENT / LAB AND COLLECTION RECORDS.
#   Corroborates Kurose's admitted involvement in both deaths. A legible custody
#   log answers a specific defense handling question. This does not by itself
#   prove intent or refute a claim of self-defense.
# E05 -- REPAIR-FUND COMPLAINT / AUTHENTICATED PRIOR MESSAGE.
#   Kenji's report and Kurose's response establish the dispute and its timing.
#   The exact message can be drafted later; it must not become a perfect spoken
#   confession. Naoto can authenticate only what he directly received or saw.
# E06 -- HARU'S INITIAL ACCOUNT / WITNESS-SUPPORT RECORD.
#   Preserved in ordinary case preparation and disclosed in advance, not hidden
#   from defense or sprung on the child in the lobby. Its scope is his direct
#   observation of Kurose returning from outside after the kitchen door shut.
#   Reveal this entry in the player's record UI only after the midpoint witness
#   reveal; the court's earlier disclosure and the player's access are distinct.
#   The initial interviewer was independent of Naoto's later conversations.
#   The record alone does not eliminate the need to test the disputed direct
#   observation; the judge permits only the necessary, limited live testimony.
# E07 -- ADULT EYEWITNESS / FRONT-DOOR SIGHTLINE / DELIVERY RECORD.
#   An independent adult courier saw the first confrontation from the open front
#   doorway while making a logged delivery. They saw Kurose initiate the attack
#   and continue as an unarmed Kenji retreated; they did not see Kenji attack him.
#   The observed sequence supports deliberate fatal violence against Kenji and
#   directly answers the first count's self-defense claim. Corroborating scene
#   and medical findings are summarized without wound images or gore.
#   E01 verifies the adult's unobstructed view; the delivery record independently
#   locates the witness there. The defense tests those limits and identification
#   in adult testimony. Do not make a forensic report pronounce anyone's motive.
#   The courier then withdrew from that doorway to seek help and could not see
#   the rear kitchen entrance. Their first-count evidence does not replace the
#   separately disputed second-count observation Haru supplies.
#
# Claim/evidence/reason pairings for the future rebuttal loop:
# FIRST COUNT. "Kenji attacked first; my client could not safely disengage."
#    Use E07's direct adult observation of initiation and retreat, its verified
#    E01 sightline, and corroborating findings from E04. This completes the
#    first-count answer during adult evidence. E05 supplies context, never a
#    substitute for proof of the act and intent. Haru carries none of this burden.
# A. "The two movements belong to one uninterrupted departure."
#    Compare E02's corrected times with E03, identifying the intervening call.
#    Concede the camera cannot identify a face. The reply narrows the dispute
#    to who returned; it does not pretend chronology alone proves a murderer.
# B. "Handling uncertainty makes this item unusable for the state's claim."
#    Read the specific transfer entry in E04; answer only the alleged gap.
#    If Stan objects to Himeko using it as proof of motive, accept the limit.
# C. "A hostile family supplied this whole account after the fact."
#    Separate Naoto's E05 knowledge from the independent preparation in E06.
#    Never treat bereavement as proof of truth or doubt as proof of bad faith.
# D. "Haru merely heard a door while Kurose was still inside."
#    The narrow testimony distinguishes hearing the latch from seeing Kurose
#    outside and then entering. Relate that direct observation to E01/E02/E03.
#    Do not coach a child to repeat an adult legal conclusion or exact clock time.
# E. "Even accepting the return, this was one continuing defensive emergency."
#    Tie the admitted exit, intervening call, deliberate return, and the complete
#    adult evidence to the separate choices and charges. The full case, not a
#    child's tears, defeats this final theory. Himeko addresses both victims.
#
# Before scripting, lock a one-page chronology with enough time for the exit,
# call, return, and both acts. Select actual times only after the scene plan and
# record comparisons have been checked. Preserve the narrow inference limits.
#
# FUTURE GAMEMODE: A PROSECUTOR'S CASE
# ----------------------------------
# Presentation: original courtroom portraits with the 2026-10-12 inked, cel-shaded
# courtroom art direction, opposed counsel benches, witness close-ups, evidence cards, assertive
# argument punctuations, and music-driven momentum evoke an Ace Attorney trial.
# Every portrait is a separate transparent PNG composited against a fixed court
# background. The counsel desk foreground covers the lower sprite as appropriate.
# Never bake a portrait or an expression change into a new courtroom background.
#
# Core loop: listen to a defense argument / cross-examination passage, inspect
# the already admitted record, select the claim at issue, choose an admissible
# exhibit or a procedural response, then explain the connection. Suggested
# actions: REVIEW RECORD, REBUT, CLARIFY SCOPE, ACCEPT THE LIMIT, REQUEST A BREAK.
# Himeko responds to defense moves; the player does not freely press each child
# testimony line as a conventional defense cross-examination minigame.
#
# Not every objection deserves a counterattack. Conceding a real limitation
# and rebuilding a narrower sound claim are successful professional actions.
# Supply readable transcripts and no reaction-time gate. Incorrect selections
# get useful local feedback and a nearby retry; they cannot acquit a guilty
# defendant, endanger a witness, change the shooting, or exhaust a child's trust.
# No guilt meter, child-distress score, combo reward, objection-spam strategy,
# or achievement for making Haru cry. No time limit on his speech or a break.
#
# First half teaches the pairings with adult testimony and procedure. Second
# half reduces fanfare and removes celebratory counters. The record remains
# legible and the player retains choices about Himeko's careful handling.
# At the closing submissions the authored case is complete. Finish all player
# actions before the judge begins the verdict preamble; the shooting is a fixed
# story event and never a punishment for a failed choice or an invisible timer.
#
# BEAT OUTLINE
# ------------
# 01. THE HIGHWAY / CAR-SPEAKER CALL.
#   Sleek car interior in morning light; established local road geography and
#   driving side must agree with the game's background family. Phone audio is
#   explicitly through Bluetooth/car speakers. Both hands remain available for
#   driving; no handheld call, text entry, or phone-menu interaction at speed.
#   The office assistant reads back the day's cover plan while indicator clicks
#   and road joints break the exchange. Himeko has already secured child care.
#   Boss's instruction is practical: keep the office's existing work moving and
#   route the press. She has asked a colleague to keep the office, not her house.
#   Viral headlines and expected turnout enter through a traffic/arrival detail
#   and a stack of press calls, not a biography delivered to someone who knows it.
#   Sample HIMEKO: "The chief wants someone at the office until this is over.
#   Put anything that needs a prosecutor through to whoever's on duty."
#   Sample HIMEKO: "And please stop promising callers I'll be free after lunch."
#   Her hands, connected-call display, dashboard, and road remain spatially
#   coherent. Finish or safely end the call before arrival logistics.
#
# 02. BLACK / THE FILE.
#   Nier bullet prose carries Himeko's own first-person diction. Summarize Kenji
#   and Aya, Kurose's charges, the widely known admissions, disputed justification,
#   her public-office role, and the crowd's expectation. Leave motive
#   emotionally incomplete so the living people can complicate the case later.
#   Sample NIER: "By breakfast, the papers had already finished the trial."
#   Sample NIER: "Kenji Mori and his wife, Aya. I had written their names often
#   enough that I no longer had to look at the cover sheet."
#   Do not announce a tragedy is coming or narrate future shooting facts.
#
# 03. LOBBY / PREPARATION.
#   Calm version of the lobby. Establish doors, benches, notice board, ceiling
#   lighting, security boundary, and the route to court that the panic variant
#   will preserve. Visitors and reporters can crowd a lawful public area without
#   supplying an explanation for the later weapon's entry.
#   Himeko checks tabs, confirms exhibit copies, drinks water, then finds she has
#   aligned one tab twice. The clerk confirms the expected timetable. She hopes
#   to be home for Asahiko's bedtime without telling the player this is a motif.
#   Naoto brings a folded child-sized cardigan but keeps it beside his own coat;
#   do not reveal Haru's witness role in the catalog or opening gag sequence.
#   A quiet exchange gives Naoto a life and a wish beyond revenge. Himeko promises
#   clear information about the schedule, never a conviction or his son's relief.
#   Stan introduces himself while looking for a working pen. One modest name
#   beat can establish the homage; the actual defense immediately earns respect.
#   Sample STAN: "Dard. Stan Dard. I believe you've got the amended exhibit list."
#   Sample HIMEKO: "I have three copies, which usually means someone needs four."
#
# 04. COURT CONVENES / THE SHAPE OF A MANAGEABLE DAY.
#   Wide geography shot: judge, prosecution and defense, witness position, gallery,
#   exits. Court positions stay consistent across all later coverage.
#   Charge summary names both deaths without graphic images. Judge states the
#   burden rests on the prosecution. Himeko's short opening sets two counts and
#   the evidence sequence; no victory pose over the bereaved family.
#   Stan's concrete continuous-emergency argument establishes the player's task.
#   Her composure, preparation, and a first fair rebuttal initially feel capable.
#
# 05. ADULT EVIDENCE / FIRST-HALF ARGUMENTS.
#   Investigator, courier, and Naoto supply their limited portions of the record.
#   Establish the adult first-count proof in E07 before using pairings A/B to
#   teach reading evidence and hearing what a claim actually says. Valid defense
#   objections cost Himeko an overbroad phrasing, not dignity.
#   Her next sentence gets narrower; the point still moves. Preserve ordinary
#   pauses for a missing page, water, the clerk, and waiting while Stan reads.
#   Naoto admits Kurose used to help around the neighborhood. Himeko does not
#   cross out the kindness because it inconveniences a simple villain picture.
#   The financial grievance explains the dispute's shape, not away the murders.
#
# 06. RECESS / THE CHILD BEHIND THE PREPARATION.
#   At the midpoint, proceedings must resolve the return through the rear door.
#   Haru's role is revealed to the player: Naoto's seven-year-old son saw it.
#   Himeko knew from preparation; she is not surprised by her own witness list.
#   The narrative has withheld that part of the day's burden until it arrives.
#   Defense has had appropriate disclosure and may contest reliability fairly.
#   The judge considers available records, alternatives, and the narrow remaining
#   factual dispute before allowing supported testimony. A familiar support
#   worker explains the room; Haru has already been prepared without rehearsal
#   of answers. His father stays nearby subject to the court's arrangement.
#   Sample HARU: "Do I have to be loud?"
#   Sample HIMEKO: "Just loud enough for the microphone. If you need to stop,
#   tell us, and we will stop."
#   He asks whether Kurose can hear him. Himeko answers truthfully and simply.
#   His swinging feet and the cardigan take up more space than case jargon.
#   E06 now enters the player's reviewable record, before pairing C contests its
#   provenance. Earlier disclosure to the defense remains established fact.
#
# 07. LIMITED TESTIMONY / THE SECOND-HALF TURN.
#   A lowered microphone and appropriate seat put Haru at the actual witness
#   position. Avoid a tiny head floating behind an adult witness podium.
#   One question at a time, no graphic exhibits, no demand to describe the acts.
#   The necessary fact: he heard the kitchen door shut, then later saw Kurose
#   outside it and coming back in. He cannot give clock times. Himeko accepts it.
#   Sample HARU: "The door went click. Then he was outside again."
#   Sample HARU: "I saw him come in. I was sitting by the cupboard."
#   When the defense distinguishes sound from sight, it is doing its job. Let
#   Stan rephrase a complicated question without turning him into a secret hero
#   or a sneering persecutor. Himeko objects only to a real problem in scope.
#   Haru's prior trust emerges in a plain association, not a written monologue.
#   Sample HARU: "He fixed the wheel. It kept coming off before."
#   Nobody needs to explain which adult act that memory fails to understand.
#   A pause or requested break is honored without pressure, penalty, or applause.
#   Use pairings C/D/E around the adult arguments about his words. Child answers
#   remain authored, never extracted through player coercion or repeated presses.
#   Himeko has one professional sentence ready and needs an extra breath to begin
#   it. She adjusts the water instead. Do not have her imagine Asahiko being killed.
#
# 08. CLOSINGS / EVERYTHING NECESSARY TO DECIDE.
#   Haru is no longer being questioned and sits with his father/support adult in
#   the court's designated family area before the interruption. This establishes
#   his presence without predicting what will happen to anyone.
#   Complete the two-count argument from converging physical and documentary
#   evidence, admission, and limited eyewitness observation. Himeko names both
#   victims and both choices. The defense has had an actual chance to answer.
#   No uncertainty remains for the story about Kurose's guilt. Nobody declares a
#   verdict yet. Neither a confession CG nor a punchline supplies the missing proof.
#   Close submissions, then acknowledge deliberation and reconvening for judgment.
#   This may be a later sitting; the trial need not resolve in one calendar day.
#   Re-establish who is present, including Haru with his father/support adult,
#   without suggesting any later outcome. Judge starts the judgment preamble.
#   A page moves; Himeko's pen waits. The verdict itself has not been spoken.
#
# 09. THE INTERRUPTION / KNOWLEDGE STOPS AT THE CAMERA.
#   Gunshots interrupt immediately before the verdict. Himeko ducks beneath her
#   prosecution desk. In the instant before taking cover she has seen enough to
#   understand firsthand who is acting and what is happening; she continues to
#   know what she personally witnesses. Her awareness is not erased by the cut.
#   Camera remains with Himeko's movement/desk underside, then cuts to black.
#   Gallery screams, overlapping adult and child voices, harsh shouting, shots,
#   impact and movement can continue briefly over black. These sounds suggest
#   the people already in the room without confirming a particular individual's
#   action, wound, survival, or death. Do not identify a shooter or gun location.
#   Audio captions remain non-attributed: [gunshots], [overlapping shouts],
#   [screaming]. Do not use named-character dialogue labels for these fragments.
#   No weapon silhouette, muzzle-flash origin, bullet path, dying declaration,
#   body, recognizable abandoned personal item, or decisive offscreen subtitle.
#   The audience learns only that Himeko lived through something intolerable.
#
# 10. LOBBY IN PANIC / AN INCOMPLETE PHYSICAL RETURN.
#   Fleeting views of the exact established lobby now in evacuation: doors open,
#   people spilling through, papers and a toppled barrier, a hand reaching for a
#   wall. Crowd figures remain anonymous, uninjured as far as the art establishes,
#   and free of identifying cast accessories. No firearm, blood, or body in art.
#   Himeko struggles to stay alert; the room loses focus and comes back. Her own
#   breathing is fast before she notices it belongs to her. A person asks her to
#   sit. Her attention catches on a grout line or her bag strap, then loses it.
#   Sample NARRATION: "Someone is breathing into my ear. I turn, and it follows."
#   The flashes represent attention failing, not a rapid white strobe. Later
#   implementation must offer reduced motion and captions with the same withheld
#   information. Do not turn breathing into a timing minigame or a medical lesson.
#   Cut to black again before the view can become a roll call of survivors.
#
# 11. BLACK / GETTING HOME.
#   Himeko's Nier voice reports concrete immediate actions and omissions: giving
#   her name to a responder, sitting where directed, finding the bag, asking to
#   go home. She can provide the required account privately without reproducing
#   it for the audience or asserting the investigation was already complete.
#   She is checked and an unnamed trusted adult drives her home after handoff;
#   she does not drive through ongoing dizziness/hyperventilation. "Rushed home"
#   concerns urgency, not reckless speed. Avoid an implausible flight past aid.
#   Her phone keeps ringing. She recognizes that it is hers and cannot answer.
#   Do not show news previews, caller identities that prove someone survived,
#   messages from specific court occupants, or a casualty summary on screen.
#   Sample NIER: "I gave them my name twice. Someone else took the keys."
#   Sample NIER: "The phone stopped, and I waited for it to start again."
#   The late-day arrival keeps the house/court/road lighting progression coherent.
#
# 12. HOME / THE DOORWAY.
#   Use the established home-entry geography, cleared of later-era teenage
#   possessions where necessary. A trusted carer opens the door and stays close
#   offscreen. Asahiko approaches from inside after Himeko reaches the threshold.
#   Establish four-year-old height and movement. He had something ordinary to
#   show her and is halfway through explaining it when he notices her face.
#   Sample ASAHIKO: "Mommy? Why are you crying?"
#   She tries to answer and cannot finish it. Her knees give way; she gathers him
#   tightly against her in the doorway and sobs. Bag slips down beside her feet.
#   Keep the CG/coverage child-sized, physically possible, close, and non-glamorous.
#   Sample ASAHIKO: "Mommy, you're squishing me."
#   She loosens her arms enough for him immediately; he remains held. The innocent
#   complaint must register as an actual child's discomfort, not a cure or a gag
#   that restores the old music. No tiny therapist speech or adult comprehension.
#   Sample HIMEKO: "I'm sorry, sweetheart. Just... stay here a minute."
#   Let the image and a quiet breath hold before moving into retrospective prose.
#
# 13. BLACK / LEAVE, THEN A DIFFERENT PRACTICE.
#   Extended leave. A practical message routed through her public office rather
#   than a spectacular resignation. She ultimately leaves public prosecution,
#   takes time with her family, and later returns to law through civil work. Do not imply
#   she instantly founded her own firm or that civil cases cannot be distressing.
#   A few separated ordinary moments carry the elapsed months: food cooling while
#   she sits with Asahiko, a phone eventually answered, a file she can open again.
#   Support and steadier days make work possible; none requires her child to heal
#   her. An interrupted task or a sound she still notices preserves the years-long
#   scar without diagnosing every present-day behavior or linking unrelated illness.
#   Sample NIER: "The leave was extended, and then I stopped asking for an end date."
#   Sample NIER: "When I took another case, it was a dispute over a house. I read
#   the first page at the kitchen table while my son colored beside me."
#   Do not reveal who died, who survived, who fired, how the firearm entered, the
#   legal outcome after the interruption, or an eventual "real verdict" in this
#   coda. No sequel hook promises that answer. End in the family/profession change.
#
# KNOWLEDGE BOUNDARY APPLIES TO THE WHOLE DELIVERABLE
# ------------------------------------------------
# Himeko's firsthand knowledge remains intact: she knows who acted and who was
# affected. No identity or outcome is specified for the player or assigned in
# production notes. The withheld account is a formal viewpoint choice.
# Avoid amnesia, hallucination, unreliable-witness twists, or
# an author note asserting a secret shooter/casualty solution. Do not invent that
# solution in source comments, branch data, asset names/metadata, galleries,
# subtitles, alt text, achievements, case files, completion logs, or later docs.
# The player knows the initial two victims and Kurose's established guilt. Those
# pre-shooting case facts are separate from the deliberately undisclosed event.
#
# ASSET AND IMPLEMENTATION HANDOFF
# --------------------------------
# The dated companion document and separate asset manifest own exact paths and
# delivered-versus-planned status. Fixed empty background PNGs are under
# assets/backgrounds/kangaroo_court/; separate 1280x720 RGBA portrait PNGs are
# under assets/characters/kangaroo_court/. Desk occlusion reuses a foreground
# crop from the relevant empty plate. Raw mattes/prompts: docs/assets/kangaroo_court/.
# Required family: calm/chaotic courtroom lobby;
# courtroom establishing view, opposite counsel angles, judge and witness views;
# desk fronts as compositing foregrounds; late-twenties Himeko courtroom poses;
# Stan Dard; Naoto Mori; Kurose; Haru with appropriately low witness seating;
# highway car interior; age-four doorstep embrace or child sprite/entry coverage.
# The existing adult mom images are identity references, not the younger delivery.
# Use the current home_entry_day/home_entry_night layout for the homecoming.
#
# Future runtime: clean store via archive_start_isolated_content("cs_mom_01").
# Keep every case/checkpoint/choice value save-local under a kc_ namespace. No
# main-story player-name interpolation, calendar changes, phone conversations,
# notification enumeration, receipt leaks, or persistent in-progress case state.
# Story unlock/completion can use the existing hub conventions only once playable.
#
# Nier integration: use the shared nier narrator with Himeko-authored first-person
# prose. Enter on black with nier_enter; clear accumulated text at deliberate
# page/scene boundaries; always call nier_exit before normal ADV or trial screens.
# Each authored textbox normally has at most two substantial sentences, keeps
# dialogue separate from narration, and earns its pause. Use original 1280x720
# staging and test real desk layering, child height, text wrapping, transitions,
# captions, reduced-motion mode, save/load, and isolated Archive launch later.
#
# LATER WORK, NOT DONE BY THIS FOUNDATION
# --------------------------------------
# Lock case timestamps/diagram and all new names; script the full dialogue;
# finish missing poses/supporting art/audio; implement the rebuttal screen and
# save/load behavior; author content notice without hidden-event spoilers; run
# interactive visual/pacing/accessibility QA; then register/unlock the story.
# No playable label or catalog availability should be inferred from this outline.
