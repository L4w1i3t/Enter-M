# =============================================================================
# ARCHIVIST INVASION 04 -- MYSTERY
# =============================================================================
#
# WHAT THIS IS
#   The fourth Archivist Invasion. Same two-act shape as the other three,
#   built out of a fourth set of materials.
#
#       Biography  wants to FINISH something.
#       Horror     wants to BE NEAR you.
#       Nonfiction wants to CHECK you against the record.
#       Mystery    wants to be WORKED OUT, and never SOLVED.
#
#   It is the only one of the four that is on your side, and that is what is
#   wrong with it. It hands you evidence. It rules things out for you, for
#   free, correctly, over and over, and every single thing it gives you is
#   TRUE. What it will not do -- what it cannot do, because the moment it does
#   it stops existing -- is let any of it add up.
#
#   THE THEME IS AN OXYMORON ON PURPOSE: elucidation and evidence WITHOUT
#   definitive truth. Everything in this fight illuminates. Nothing in this
#   fight concludes. Every number on screen goes the right way and none of
#   them arrive.
#
# THE FORM IT IS WEARING
#   Biography turned up wearing a specific person, because a life needs
#   someone to have lived it. Nonfiction turned up wearing nobody in
#   particular, because a fact needs nobody in particular to be true.
#
#   Mystery turns up wearing THE INVESTIGATOR. Not the culprit -- a mystery
#   does not need one of those, it needs someone who is ABOUT to explain, and
#   never anyone who does. So it is the coat and the hat and the posture of
#   the person who was going to tell you at the end of the chapter, layered up
#   out of torn paper, with holes punched where a face should be and empty
#   picture frames hanging off it. The frames are where the answer goes. There
#   is nothing in them and there was never going to be.
#
# THE ONE THING IT WILL NOT DO
#   Horror's readouts lie, and lie more the closer it gets. Nonfiction's are
#   always true because procedure demands it. Mystery's are always true for a
#   completely different reason: A LIE WOULD BE A FACT ABOUT THE CASE. If it
#   told you one wrong thing you could rule that thing out, and ruling things
#   out is how a case closes.
#
#   Which is why THERE ARE NO RED HERRINGS IN HERE, and why act two is as
#   frightening as it is. A herring is not a lie. A herring is a true fact
#   about SOMETHING ELSE. Mystery does not have to invent anything to bury
#   you: it only has to make sure there is always something else in the room.
#
#   ACT ONE -- THE FIELD. Turn-based, the house furniture, the same rolling
#   odometer. THE FIELD is how many readings of the case are still open. It
#   starts at seven. You bring it down with NARROW, it brings it down FOR you
#   with DISCLOSE, and everything that happens in the bout is a negotiation
#   over one integer.
#
#   ACCUSE is the attack, and it is worth more the narrower the field is --
#   the command panel prints the exact damage it would do RIGHT NOW, next to
#   the word, which is the whole tutorial for the act and is not a sentence.
#   And an accusation REOPENS the case: the field springs back up, because
#   everything a failed accusation ruled out is on the table again.
#
#   So the loop is NARROW, NARROW, CASH OUT, and the fight is about timing the
#   cash-out -- because DOUBT is climbing the entire time you are narrowing,
#   and it does not climb toward failure, it climbs toward CERTAINTY, which is
#   worse. At 100 the case is REOPENED and the whole position is gone.
#
#   THE FIELD CAN NEVER REACH ONE. NARROW is refused at two, forever, with no
#   explanation. That refusal is the single most important line in the file:
#   it is the Archivist's entire nature expressed as an unavailable menu
#   option, learned in one turn, for free, and never forgotten.
#
#   ACT TWO -- the CORRUPTIVE STATE: the dark. Every light goes out. There is
#   no boss on screen, there is no boss anywhere on screen for the whole act,
#   and that is the point. It is in here with you and you cannot see it.
#
#   THE JOINT, AND IT IS THE BEST ONE IN THE SET: the FIELD you carry through
#   the tear is how many bodies are standing in the dark. Not a metaphor, not
#   a difficulty multiplier -- act one's abstract counter becomes a literal
#   population. Every reading you never ruled out is a shape moving around a
#   room you cannot see, dropping evidence indistinguishable from its. And
#   because the field can never reach one, THERE IS ALWAYS SOMEBODY ELSE IN
#   THE ROOM. That is why act one's refusal matters and it is why act two is
#   the shape it is.
#
# THE FOUR POLES (this is why act two is what it is)
#       Biography   you must CLOSE distance.       A stage you circle.
#       Horror      you must OPEN distance.        A throat you flee down.
#       Nonfiction  distance is irrelevant.        A page you hold ground on.
#       Mystery     DISTANCE IS NOT THE AXIS.      A dark room you have to
#                                                  build out of evidence.
#   The axis is KNOWLEDGE. You are never running out of room, or space, or
#   ground -- the room is enormous and nothing in it is chasing you very hard.
#   You are running out of things you can still prove.
#
#   And so the camera. Biography has a proscenium, Horror has a vanishing
#   point, Nonfiction has no camera at all. Mystery has the same flat
#   orthographic overhead as Nonfiction and is its exact photographic
#   negative: Nonfiction's page is entirely visible and is being ERASED cell
#   by cell, Mystery's room is entirely invisible and is being DRAWN line by
#   line. The two fights are the same picture run in opposite directions.
#
# ACT TWO, THE ACTUAL LOOP
#   You are a LAMP. You are the only light in the encounter and it does not
#   reach far.
#
#   MARKS. Every body in the room leaves them, in bursts of MY_TRAIL_LEN. A
#   mark lying in the dark is invisible; your lamp passing over it collects it,
#   permanently. And here is the geometry, which is real and honest and IS the
#   fight:
#
#       A mark lies a little way off the body and records HOW FAR AWAY IT WAS.
#       So it says: IT WAS EXACTLY D FROM HERE, AT THIS TIME.
#       A body moves at most MY_TRACE_SPREAD px per tick.
#       Therefore it is NOW somewhere in the ANNULUS of radius D about that
#       mark, whose half-width is (now - then) * MY_TRACE_SPREAD.
#
#   One of those is a rumour -- a whole circle of room. Two cross in two
#   places. Three settle it. That statement is true when you collect it and
#   stays true forever; the annulus simply thickens every tick until it is
#   the whole room and says nothing. THAT IS THE THEME AS ARITHMETIC. The
#   evidence is never wrong. The evidence is never enough. You are not racing
#   a timer, you are racing the rate at which true things stop being useful.
#
#   RANGES, AND NOT POSITIONS, AND THIS IS THE LOAD-BEARING DECISION IN THE
#   WHOLE FILE. The first build recorded positions, which decay into discs --
#   and discs about one body never combine into anything tighter than the
#   newest of them, because the disc round an older mark is a strict superset
#   of the newer one's reachable set. An act built out of discs has no
#   deduction in it at all, and the harness said so in one line: the live set
#   averaged 1.0 marks about any one body. Rings took that to 1.9 and made
#   the act exist.
#
#   THE BELIEF FIELD is where the live annuli agree, evaluated per pixel in
#   inv.lamp and painted into the dark as light. Thin bright circles crossing
#   in the black; where enough of them meet it concentrates and goes gold. It
#   is the only warm colour in the act and it is what you are chasing. It is
#   also frequently WRONG and never lying: with four bodies in the room your
#   rings are about four different things, so the field knots in places where
#   nothing is standing and every ring that made that knot is correct.
#
#   AND A STATEMENT'S WEIGHT IS ITS PRECISION. Every claim in here is equally
#   TRUE and they are emphatically not equally INFORMATIVE, so the field
#   weights each one by how tight it still is. Counting them instead was the
#   second thing that had to be fixed and it was worth as much as the first:
#   unweighted, the brightest point on the board was routinely four exhausted
#   statements grazing each other, two thirds of the knots had nothing in
#   them, and there was no signal anywhere in the act.
#
#   ACCUSE (hold Z) is act one's verb, deliberately, because act one already
#   taught it and rule 1 forbids the sentence that would explain it. It roots
#   you for forty ticks and then resolves against whatever is actually within
#   MY_NAME_R of you:
#       THE SUBJECT     a hit. SOLVED climbs, every live constraint is voided
#                       (the case reopens -- same rule as act one), it breaks
#                       away across the room, and the act gets harder.
#       A BYSTANDER     RULED OUT. That body is gone from the room for good
#                       and a chalk X is left where it stood. A real, useful,
#                       permanent result that is not the win.
#       NOTHING         INCONCLUSIVE -- and a permanent exclusion ring goes
#                       down where you stood, which genuinely narrows the
#                       field for the rest of the act.
#   THERE IS NO WASTED ACCUSATION IN THIS FIGHT AND THERE IS NO FINAL ONE.
#   Every outcome produces true information and none of them end it.
#
#   SWEEP (X) is the bargain verb, and every one of these fights has one.
#   Flares the lamp to nearly three times its radius for eighteen ticks and
#   collects every trace inside it -- and then your eyes are gone: the lamp
#   drops to MY_LAMP_MIN and takes MY_SWEEP_BLIND ticks to recover. It is the
#   only way to gather fast enough to keep a tight field, and the recovery is
#   the most dangerous window in the act.
#
#   AND THE ROOM FILLS UP WITH TRUE THINGS. A collected trace does not
#   disappear when its disc grows useless -- it goes pale and STAYS, drawn on
#   the dark forever, along with every exclusion ring and every chalk X. By
#   the end of a run the black is full of a dense, precise, beautiful survey
#   lattice, every line of which is correct, none of which is any longer of
#   the slightest use. That picture is the whole encounter and it is the only
#   thing left on screen at the end of the winning ending.
#
# HOW YOU LOSE, AND THE FAIRNESS SPLIT THAT MAKES IT LEGAL
#   Health, and only health. Nothing else in act two can kill you (the
#   Nonfiction principle: no death spiral, only lost time). Damage comes from
#   ONE source -- the subject walking into you in the dark.
#
#   Which sounds monstrous, so: DEDUCTION IS FOR OFFENCE, AND THE DEFENCE IS
#   A SIGNAL YOU DO NOT HAVE TO DEDUCE. Proximity to the subject drives DREAD:
#   the heartbeat comes up, the lamp starts to fail, and the frame closes in,
#   all of it continuous and all of it starting well outside contact range.
#   Failing the puzzle NEVER kills you. It only means you never finish.
#   That is what makes rule 5 hold in a fight against something invisible.
#
#   THE MOST RELIABLE EVIDENCE IN THE ACT IS THE KIND YOU GET BY WALKING INTO
#   SOMETHING. Contact leaves an exact, permanent, zero-radius mark -- a body
#   was HERE, NOW -- which is worth more than any disc. A bystander only
#   startles and moves off. The subject takes MY_HIT_HP off you. So the
#   reckless line is real and it is priced: feel for the dread, and if there
#   is none there, walk into the dark and find out what it is.
#   Note the inversion that falls out of that, which is genuine strategy
#   rather than decoration: the MORE bodies are in the room, the SAFER a blind
#   contact is and the harder the deduction. Act one is choosing which of
#   those two problems you would rather have.
#
# THE RULES (from the invasion spec -- restated because they bind here too)
#   1. NO FLAVOR TEXT. Controls, numbers and state words. The complete list of
#      drawable strings in this fight is: MYSTERY / NARROW / ACCUSE / RECHECK
#      / RUN / FIELD / LEADS / DOUBT / HP / SOLVED / SWEEP / TRACES /
#      DISCLOSE / TESTIMONY / INTRODUCE / ALIBI / DENOUEMENT / SOLUTION /
#      REOPENED / REOPENING / PENDING / TWO REMAIN / NO LEADS / STILL OPEN /
#      NOT RULED OUT / INCONCLUSIVE / SEE FIELD / RULED OUT / CONTACT / GOD /
#      PAUSED, plus three control hints. Nothing in here is a sentence.
#   2. NOTHING MAY BE FUNNY. Checked hardest on RUN, which is the one joke the
#      form allows and which is played completely straight here: every refusal
#      is a true statement about the state of the case.
#   3. IT MOVES LIKE SOMETHING THAT HAS SEEN A DIAGRAM. Its own body shader,
#      inv.lacuna -- the fourth axis. See the note there.
#   4. IT ARRIVES AND LEAVES THROUGH A HOLE. It does not climb out of the
#      rupture and it is never seen arriving: the light in the room fails
#      three times, and each time it comes back there is more of it standing
#      there. The hole is what the light fails INTO.
#   5. EVERY PATTERN MUST BE BEATABLE HITLESS. See the fairness split above:
#      the single damage source is continuously telegraphed by a channel that
#      requires no deduction at all, from well outside its own range.
#
# BALANCE (MEASURED, not guessed -- change one number and re-run the harness)
#   Driven headless with scripted bots: an init 999 block gated on an env var,
#   a fake _poll_input, run through lint. Rebuild it before retuning anything.
#
#   ACT ONE (4 seeds a line). The case is 1000; the tear is at MY_SHIFT_CASE
#   dealt or turn MY_SHIFT_TURN_CAP, whichever comes first, and what it hands
#   over is THE FIELD.
#       narrow, cash out on PENDING   tore t9-t20, case 240-524, FIELD 3-8
#       narrow to two and only then   tore t20, case 170-312, FIELD 8-9
#       accuse every single turn      DEAD at the cap in 3 of 4, FIELD 10-12
#       recheck every single turn     survives everything untouched, case 0,
#                                     FIELD 10-12
#   Read the last column, because it is the only one act two ever sees. Note
#   the shape, which is Nonfiction's shape: act one is close to unloseable if
#   you never push, and it is the SECOND HALF that collects the bill.
#
#   THE FIELD ONLY WENT UP IN THE FIRST BUILD, and it is worth recording how
#   badly. NARROW took one off and the Archivist had three moves that put
#   them back, so a bot narrowing on every available turn went 7 -> 12 and
#   dealt LITERALLY ZERO damage in eighteen turns. A tug of war with one rope
#   on one side and three on the other is not a tug of war. MY_NARROW_FIELD
#   is why the act works.
#
#   ACT TWO (4 seeds a cell). SOLVED is 100 at MY_SOLVE_GAIN a landed
#   accusation, so the act is FOUR hits long. Health is MY_HP2_MAX against
#   MY_HIT_HP a contact, which is thirteen contacts.
#
#                       field 2            field 4            field 6
#     field + dread   3/4  62-140s      4/4  67-158s      4/4  84-205s
#                     hp 0-266          hp 178-266       hp 62-274
#     field only      4/4 119-174s      4/4  63-255s      4/4  89-160s
#                     hp 106-222        hp 186-280       hp 156-280
#
#   And the lines that do not play it:
#       gathers and never accuses       0/4   75-123s   dead
#       stands still                    0/4  203-338s   dead
#       backs off whenever it feels
#         anything                      1/4   69-500s
#   NO LINE THAT ENGAGES LOSES, which is the property to preserve (it is
#   Nonfiction's). The last three are the honest warnings in the table:
#   gathering without ever confirming is a way to lose, and so is treating
#   the dread channel as something to run from rather than something to ask.
#
#   THE DREAD CHANNEL IS WORTH A THIRD OF THE ACT: same wins, roughly half
#   the accusations (12-22 against 24-48), because the cheapest thing in the
#   fight is walking to a knot and finding out for free that nothing is
#   standing on it. It is a skill the act never mentions.
#
#   THE FIELD YOU CARRIED shows up in the CLOCK rather than in deaths, which
#   is the correct place for it. Getting that direction right took three
#   passes: a flat per-body evidence rate makes a WIDE field EASIER (more
#   bodies is simply more marks -- measured, field 6 beat field 2 outright),
#   and a flat TOTAL rate overcorrects and starves the two-body case until it
#   has nothing to work with. The crowd scale in _step_bodies sits between
#   them, and the rest of the cost is carried by MY_NAME_CD_MISS: more things
#   in the room means more of your accusations land on the wrong one, and the
#   bill arrives as TIME, which is the only currency this act may charge in.
#
#   THE HONESTY INVARIANT IS ASSERTED, NOT ASSUMED. Every tick of every run
#   above checked that each live constraint actually contains the body it is
#   about -- that the Archivist has not said one false thing. It caught two
#   real bugs and 0 violations survive across 24 runs: a startled body
#   outrunning its own evidence (168-372 false claims a run), and then
#   _void_body withdrawing only the COLLECTED marks and leaving the
#   uncollected ones lying in the dark to be picked up later (8-16 a run) --
#   a statement does not become unsound at the moment somebody reads it.
#   Rebuild that assertion before touching _drop_trace, _void_body,
#   _step_bodies, MY_BREAK_REACH or any speed constant.
#
#   THE THIRD BUG THE INVARIANT IMPLIES BUT DOES NOT CATCH, recorded because
#   it was nearly shipped: making a body's evidence sound again by DELETING
#   it also deletes the contact mark you just earned. _step_contact withdrew
#   the body's marks and then made the contact mark -- in that order -- so
#   the single best piece of evidence in the act was silently binned on every
#   contact and the trade the whole mechanic advertises was a lie. The mark
#   is made AFTER the withdrawal now and carries MY_BREAK_REACH of slack, so
#   it survives the break-away it causes and stays true across it.
#
#   THE NUMBER THAT ACTUALLY GOVERNS THE ACT is the relationship between
#   MY_TRACE_SPREAD, MY_TRACE_EVERY, MY_TRAIL_LEN and MY_LAMP_R, and it is
#   worth stating plainly because every future tuning pass will want to touch
#   the wrong one. An annulus thickens MY_TRACE_SPREAD px per tick, so a mark
#   is worth having for about (MY_TRACE_MAXR / MY_TRACE_SPREAD) = 250 ticks,
#   and you need three of them ABOUT THE SAME BODY inside that window to get
#   a knot worth walking to. MY_TRAIL_LEN is what makes three of them arrive
#   together; the lamp radius sets how much of the room you can gather from at
#   once, which is why SWEEP exists and why it costs your eyes.
#
#   NOT DONE, and it is the same gap Nonfiction has: inv.lamp and inv.lacuna
#   REGISTER cleanly (asserted headless) but have never been drawn on a GPU.
#   renpy.screenshot() comes back near-black for a shader-driven CDD, so the
#   check that is available is the render-time *_OK flags, not a PNG.
#
#   ESCALATION is one number, `heat()`, half clock and half record, exactly
#   like Nonfiction's churn(): it buys subject speed, trace scarcity, faster
#   reopenings and a shorter useful life on a disc. And past MY_SOLVE_HARD
#   every landed accusation ALSO puts another body in the room -- closing in
#   widens the field, which is act one's law arriving in act two's language
#   and is why the endgame is the hardest part of the act.
#
# ARCHITECTURE
#   Same as every invasion: MYGame owns the simulation, MYStage is one CDD
#   stepping it at a fixed 60Hz inside render(). Two shaders of its own --
#   inv.lamp (the room, BOTH acts, and the belief field is evaluated inside
#   it) and inv.lacuna (the body). The padded plate and the heart come from
#   invasions.rpy.
#
# READ THIS FIRST IF YOU ARE LOST
#   MYGame.step() dispatches on self.mode:
#     arrive   the rupture; the light fails three times
#     menu     act one commands
#     beat     the one-line readout; WAITS for a key, never auto-advances
#     enemy    its turn
#     shift    the tear -- the lights go out and the field walks in
#     dark     act two
#     leave_w  the room comes up empty / leave_l  your lamp goes out
#   Units: screen pixels (1280x720), speeds are px per 1/60s tick, timers are
#   ticks. Act two is continuous space inside MY_ARENA -- there is no grid in
#   this fight, which is the other half of not being Nonfiction.
# =============================================================================

# --- SHADERS -----------------------------------------------------------------
init -9 python:
    MY_LAMP_OK = False
    MY_LACUNA_OK = False

    def _my_register_lamp():
        # THE ROOM, BOTH ACTS -- and the belief field is evaluated in here.
        #
        # NAMED inv.lamp AND NOT inv.dark, WHICH IS NOT A STYLE CHOICE.
        # Horror already owns "inv.dark" (inv_horror.rpy). Registering a
        # second shader under an existing name does not warn and does not
        # fail -- the later registration silently REPLACES the earlier one,
        # and since these files load in alphabetical order this one won every
        # time. The symptom appeared in a completely different fight: Horror
        # crashed on its own room draw with "Shader inv.dark has not been
        # given uniform u_my_dark", because it was passing its uniforms to
        # Mystery's shader. Check the list in invasions.rpy before adding a
        # shader to any invasion.
        #
        # Every invasion's room says what its Archivist does to a space.
        # Biography's BOILS. Horror's RUSHES at you. Nonfiction's is PRINTED
        # and re-set and never still and never moving. Mystery's room is the
        # only one of the four that is mostly NOT THERE.
        #
        # Act one (u_my_open 0) is a room seen badly: the substrate is cold,
        # underlit and resolved only inside a soft pool of focus that drifts
        # across it, so you are always looking at part of something. There is
        # no domain warp and no flow -- it breathes on a very long period and
        # otherwise holds, because a room that churns is a room that is
        # inventing itself, and this one is merely difficult to see.
        #
        # Act two (u_my_open 1) puts every light out. What is left is:
        #   * black, and grain, and nothing else by default
        #   * THE LAMP -- one radial pool around u_my_lamp, the only light in
        #     the encounter, which reveals the substrate where it falls
        #   * THE BELIEF FIELD -- up to six live constraints handed in as
        #     u_my_c0..c5 = (x, y, radius, weight). Each one is the honest
        #     statement "a body was at (x,y) and cannot have got further than
        #     radius since", so the intersection of the live set is where a
        #     body must be. Summed, normalised by u_my_nlive and raised to a
        #     power, so a lone disc is a cold smear and six agreeing discs are
        #     a small hot knot. It is the only warm thing in the act.
        #   * the rims of those discs, drawn thin, because the boundary of a
        #     true statement is worth being able to see.
        #
        # u_my_dread is the fairness channel and it is deliberately loud in
        # here: proximity to the subject makes the lamp FAIL (a real flicker,
        # not a tint) and pulls the frame in. That, plus the heartbeat, is the
        # entire defence in a fight against something invisible -- see the
        # fairness split in the header. It must never be subtle.
        renpy.register_shader("inv.lamp", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_my_res;
            uniform float u_my_time;
            uniform float u_my_open;
            uniform float u_my_dark;
            uniform float u_my_flash;
            uniform float u_my_dread;
            uniform float u_my_reopen;
            uniform float u_my_heat;
            uniform float u_my_nlive;
            uniform float u_my_maxr;
            uniform vec4 u_my_hole;
            uniform vec4 u_my_lamp;
            uniform vec4 u_my_c0;
            uniform vec4 u_my_c1;
            uniform vec4 u_my_c2;
            uniform vec4 u_my_c3;
            uniform vec4 u_my_c4;
            uniform vec4 u_my_c5;
            uniform vec4 u_my_c6;
            uniform vec4 u_my_c7;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float my_hash(vec2 p) {
                return fract(sin(dot(p, vec2(23.71, 141.29))) * 31771.913);
            }
            vec2 my_mirror(vec2 p) {
                return abs(fract(p * 0.5) * 2.0 - 1.0);
            }
            // A STATEMENT'S WEIGHT IS ITS PRECISION, and this one line is
            // what stops the belief field being a liar's mirror. Every claim
            // in here is equally TRUE; they are emphatically not equally
            // INFORMATIVE, and counting them was the mistake. A ring with a
            // 250px tolerance and a ring with a 20px tolerance are worth the
            // same to a tally, so the brightest point on the page was
            // routinely a place where four exhausted statements happened to
            // graze each other -- measured, roughly two thirds of the knots
            // a bot walked to had nothing in them at all, and the fight had
            // no signal in it anywhere.
            //
            // Weighted by precision the field goes quiet as evidence ages,
            // which is the correct behaviour and the whole theme in one
            // function: a true thing you learned a while ago still glows,
            // faintly, and is outvoted by anything you have just found out.
            float my_weight(float tol, float maxr) {
                return clamp(1.0 - tol / max(maxr, 1.0), 0.10, 1.0);
            }
            // ONE CONSTRAINT, packed as (x, y, D, tol).
            //
            //   D > 0   A RANGE. "It was exactly D from here at time t", and
            //           it cannot have got further than tol since, so it is
            //           somewhere in the ANNULUS of radius D and half-width
            //           tol. Alone this is a big useless ring. Two of them
            //           cross in two places. Three settle it.
            //   D = 0   A CONTACT. The annulus collapses to a disc of radius
            //           tol -- an exact position, and the only kind of
            //           evidence in the act that is worth anything on its
            //           own. You get it by walking into something.
            //
            // tol <= 0 is an unused slot. Returns (belief, rim).
            vec2 my_claim(vec4 ci, vec2 p, float maxr) {
                float tol = ci.w;
                if (tol <= 0.001) {
                    return vec2(0.0);
                }
                float band = abs(distance(p, ci.xy) - max(ci.z, 0.0));
                float inside = 1.0 - smoothstep(tol * 0.70, tol, band);
                float rim = 1.0 - smoothstep(0.0, 2.4, abs(band - tol));
                float w = my_weight(tol, maxr);
                return vec2(inside * w, rim * w);
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            vec2 res = max(u_my_res, vec2(1.0));
            vec2 px = uv * res;
            float t = u_my_time;
            float open = clamp(u_my_open, 0.0, 1.0);
            float dread = clamp(u_my_dread, 0.0, 1.0);
            float heat = clamp(u_my_heat, 0.0, 1.0);
            float reop = clamp(u_my_reopen, 0.0, 1.0);
            float aspect = res.x / max(res.y, 1.0);

            vec2 c = uv - 0.5;

            // The rupture. Same instrument as every arrival -- but this one is
            // a hole the LIGHT falls into rather than a hole a body climbs out
            // of, so it drags the substrate in and gives nothing back.
            vec2 hp = (u_my_hole.xy / res) - 0.5;
            float hr = max(u_my_hole.z, 1.0) / res.x;
            float hs = clamp(u_my_hole.w, 0.0, 1.0);
            vec2 hv = c - hp;
            float hd = length(hv);
            float hinf = (1.0 - smoothstep(0.0, hr, hd)) * hs;
            if (hinf > 0.001) {
                float ha = hinf * hinf * 3.1;
                float ccs = cos(ha);
                float csn = sin(ha);
                hv = vec2(hv.x * ccs - hv.y * csn, hv.x * csn + hv.y * ccs);
                c = hp + hv * (1.0 - 0.66 * hinf);
            }

            // --- THE SUBSTRATE ---------------------------------------------
            // Quantised, cold, and low key. It breathes on a period long
            // enough that you cannot catch it doing it.
            vec2 sp = c + vec2(sin(t * 0.13), cos(t * 0.11)) * 0.010;
            float cells = mix(560.0, 300.0, open);
            vec2 q = floor((sp + 0.5) * cells) / cells;
            float lum = dot(texture2D(tex0, my_mirror(q)).rgb,
                            vec3(0.299, 0.587, 0.114));
            vec3 substrate = mix(vec3(0.048, 0.062, 0.086),
                                vec3(0.40, 0.48, 0.58), lum);

            // --- ACT ONE: A ROOM YOU CAN ONLY PARTLY SEE -------------------
            // A pool of focus drifts over the substrate. Inside it the room
            // resolves; outside it falls back to almost nothing. Nothing here
            // is hidden from you on purpose -- it is simply not lit, which is
            // a different and more patient kind of withholding.
            vec2 fpc = vec2(0.5 + 0.21 * sin(t * 0.19),
                            0.5 + 0.15 * cos(t * 0.23));
            float fd = distance(vec2(uv.x * aspect, uv.y),
                                vec2(fpc.x * aspect, fpc.y));
            float focus = 1.0 - smoothstep(0.15, 0.50, fd);
            vec3 room1 = substrate * (0.16 + 0.92 * focus);
            // A second, older pool, much fainter and moving the other way, so
            // the light in act one never reads as one lamp being carried.
            float fd2 = distance(vec2(uv.x * aspect, uv.y),
                                vec2((0.5 - 0.26 * cos(t * 0.11)) * aspect,
                                    0.5 + 0.20 * sin(t * 0.14)));
            room1 += substrate * (1.0 - smoothstep(0.10, 0.44, fd2)) * 0.22;

            // --- ACT TWO: THE DARK ------------------------------------------
            vec3 room2 = vec3(0.013, 0.016, 0.024);

            // THE LAMP. One pool, and it fails when something is close.
            vec2 lp = u_my_lamp.xy;
            float lr = max(u_my_lamp.z, 8.0);
            float ls = clamp(u_my_lamp.w, 0.0, 1.0);
            float ld = distance(px, lp);
            float lamp = (1.0 - smoothstep(lr * 0.30, lr, ld)) * ls;
            float flick = 0.55 + 0.45 * sin(t * 41.0 + sin(t * 9.7) * 3.4);
            lamp *= mix(1.0, mix(1.0, flick, 0.72), dread);
            // Where the lamp falls, the room is briefly a room again.
            room2 += substrate * lamp * 0.86;
            room2 += vec3(0.30, 0.38, 0.47) * lamp * 0.16;

            // THE BELIEF FIELD.
            vec2 b = vec2(0.0);
            b += my_claim(u_my_c0, px, u_my_maxr);
            b += my_claim(u_my_c1, px, u_my_maxr);
            b += my_claim(u_my_c2, px, u_my_maxr);
            b += my_claim(u_my_c3, px, u_my_maxr);
            b += my_claim(u_my_c4, px, u_my_maxr);
            b += my_claim(u_my_c5, px, u_my_maxr);
            b += my_claim(u_my_c6, px, u_my_maxr);
            b += my_claim(u_my_c7, px, u_my_maxr);
            // u_my_nlive is the SUM OF THE WEIGHTS, not the count, so
            // "everything agrees here" still normalises to 1.
            float nl = max(u_my_nlive, 0.35);
            float agree = clamp(b.x / nl, 0.0, 1.0);
            float belief = pow(agree, 2.7) + 0.62 * smoothstep(0.84, 1.0, agree);
            vec3 cold = vec3(0.30, 0.45, 0.62);
            vec3 gold = vec3(0.94, 0.74, 0.35);
            room2 += mix(cold, gold, smoothstep(0.34, 0.94, agree))
                    * belief * 0.62;
            // ...and the boundaries of the statements themselves.
            room2 += vec3(0.44, 0.54, 0.66) * clamp(b.y, 0.0, 1.2) * 0.20;

            vec3 col = mix(room1, room2, open);

            // --- REOPENING --------------------------------------------------
            // Not an attack and not drawn like one. The edges of the room go
            // red and come inward, because what is about to happen is that
            // everything outside what you are standing on stops being ruled
            // out.
            if (reop > 0.002) {
                float vgr = length(c);
                col = mix(col, vec3(0.26, 0.035, 0.070),
                        reop * smoothstep(0.62 - 0.42 * reop, 0.78, vgr) * 0.92);
            }

            // --- THE HOLE ---------------------------------------------------
            if (hs > 0.001) {
                float core = 1.0 - smoothstep(hr * 0.12, hr * 0.56, hd);
                col *= mix(1.0, 0.010, core * hs);
                float lip = 1.0 - smoothstep(0.0, hr * 0.09,
                                            abs(hd - hr * 0.56));
                col = mix(col, vec3(0.72, 0.78, 0.86), lip * hs * 0.85);
            }

            // Tooth, and it is grain rather than paper: this room has no
            // surface, it has a resolution.
            float tooth = my_hash(floor(px * 0.5) + floor(t * 24.0) * 0.013);
            col *= 1.0 - (0.055 + 0.045 * open + 0.050 * heat) * tooth;

            // The frame closes with dread and it closes hard. This is the
            // defence channel; it is not allowed to be tasteful.
            float vg = length(c);
            float vin = vg * vg * mix(0.86, 0.62 + 2.30 * dread, open);
            col *= max(0.0, 1.0 - vin);

            col = mix(col, vec3(0.86, 0.90, 0.96), clamp(u_my_flash, 0.0, 1.0));
            col *= 1.0 - clamp(u_my_dark, 0.0, 1.0);
            gl_FragColor = vec4(col, 1.0);
        """)

    def _my_register_lacuna():
        # MYSTERY'S OWN BODY -- the fourth axis. Every Archivist gets its own
        # way of being wrong or they all read as the same puppet in hats.
        #
        #   Biography  MISREGISTRATION. Fourteen hard bands sliding out of
        #              sync, chromatic fringing, high frequency. Digital.
        #   Horror     UNDULATION. Low frequency, liquid, no colour split, a
        #              swell from inside, a silhouette that frays into smoke.
        #   Nonfiction REPRODUCTION. It does not deform at all -- it is
        #              printed, posterized, screened, and its bands JUMP to a
        #              new offset and hold rather than travelling.
        #   Mystery    STRATIFICATION AND APERTURE, and it is the fourth thing
        #              rather than a blend of the other three.
        #
        # STRATIFICATION: it is not one body, it is a stack of layers sorted by
        # depth, and they slide against each other continuously and slowly on
        # unrelated clocks. Nothing about it ever jitters and nothing about it
        # ever settles. You never see the whole of it in one arrangement, so
        # there is no arrangement of it to remember.
        #
        # APERTURE: holes open and drift across it -- and what is inside a hole
        # is NOT the room behind it. It is more of the same coat, sampled from
        # somewhere else entirely. You cannot see through this thing. There is
        # only ever more of it. (The source art has the holes in it already;
        # this makes them behave.)
        #
        # THE LIT SLIVER: only a band of it is ever lit, and the band travels.
        # In an encounter whose second half is a dark room, a figure that is
        # fully and evenly lit is a figure from a different fight. u_lac_lit
        # widens the band to the whole body, which happens exactly once, at
        # the end of the winning ending, and is the only time it is all there.
        #
        # And it does not erode in cells, drain bottom-up, or get struck out.
        # IT LEAVES BY BECOMING ALL HOLES: u_lac_diss grows the apertures until
        # there is nothing between them.
        renpy.register_shader("inv.lacuna", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_lac_res;
            uniform float u_lac_t;
            uniform float u_lac_shear;
            uniform float u_lac_ap;
            uniform float u_lac_band;
            uniform float u_lac_lit;
            uniform vec2 u_lac_stretch;
            uniform float u_lac_pivot;
            uniform float u_lac_hurt;
            uniform float u_lac_diss;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float lac_hash(vec2 p) {
                return fract(sin(dot(p, vec2(27.19, 93.41))) * 21643.317);
            }
        """, fragment_300="""
            // The plate's OWN coordinate, kept before anything warps it. The
            // mesh is clipped at this rectangle, so the feather at the bottom
            // of this shader has to be measured in it and not in the warped
            // space the rest of the effect works in.
            vec2 plate_uv = v_tex_coord;

            vec2 uv = v_tex_coord;
            vec2 piv = vec2(0.5, clamp(u_lac_pivot, 0.0, 1.0));
            vec2 stv = max(u_lac_stretch, vec2(0.08));
            uv = (uv - piv) / stv + piv;

            float t = u_lac_t;
            float shear = clamp(u_lac_shear, 0.0, 3.0);
            float ap = clamp(u_lac_ap, 0.0, 1.0);
            float diss = clamp(u_lac_diss, 0.0, 1.0);
            vec2 res = max(u_lac_res, vec2(1.0));

            // STRATA. Probe once to find out how deep this pixel is, then
            // sample again through that stratum's own drift. Seven layers,
            // seven unrelated clocks, and the deeper a layer is the further it
            // has wandered from the one in front of it.
            vec4 probe = texture2D(tex0, uv);
            float plum = dot(probe.rgb, vec3(0.299, 0.587, 0.114));
            float layer = floor(clamp(plum, 0.0, 0.999) * 7.0);
            float lph = lac_hash(vec2(layer, 4.1)) * 6.2831853;
            float lrt = 0.55 + lac_hash(vec2(layer, 8.3)) * 0.9;
            vec2 drift = vec2(cos(t * 0.21 * lrt + lph),
                            sin(t * 0.17 * lrt + lph * 1.7))
                        * (0.003 + 0.026 * shear)
                        * (0.30 + 0.70 * (layer / 6.0));
            vec2 suv = uv + drift;

            vec4 src = texture2D(tex0, suv);
            float a = src.a;
            vec3 col = src.rgb;

            // The deeper strata have less colour in them. Nothing under the
            // coat was ever painted.
            float g = dot(col, vec3(0.299, 0.587, 0.114));
            col = mix(vec3(g), col, 0.28 + 0.60 * (layer / 6.0));

            // APERTURES.
            vec2 P = uv * res;
            float hole = 0.0;
            float lipv = 0.0;
            for (int i = 0; i < 5; i++) {
                float fi = float(i);
                float ph = lac_hash(vec2(fi, 13.0)) * 6.2831853;
                vec2 hc = vec2(0.50 + 0.26 * sin(t * (0.09 + 0.06
                                * lac_hash(vec2(fi, 17.0))) + ph),
                            0.14 + 0.70 * lac_hash(vec2(fi, 23.0))
                                + 0.07 * cos(t * 0.13 + ph));
                // Clamped, because at the old 0.62 * diss a departing
                // aperture was wider than the plate and its lip came off the
                // silhouette as a hard rectangle.
                float R = min((0.030 + 0.044 * lac_hash(vec2(fi, 29.0)))
                        * (0.30 + 1.25 * ap) + 0.34 * diss, 0.44) * res.x;
                float d = distance(P, hc * res);
                hole = max(hole, 1.0 - smoothstep(R * 0.84, R, d));
                lipv = max(lipv, 1.0 - smoothstep(0.0, max(R * 0.11, 1.0),
                                                abs(d - R * 0.88)));
            }

            // What is in a hole is more of the coat, not the room.
            vec4 inner = texture2D(tex0, fract(suv + vec2(0.17, -0.11)));
            float ig = dot(inner.rgb, vec3(0.299, 0.587, 0.114));
            col = mix(col, vec3(ig) * 0.34, hole * 0.90);
            col = mix(col, vec3(0.78, 0.82, 0.88), lipv * (0.22 + 0.40 * ap));

            // THE LIT SLIVER, raking across it.
            float axis = uv.y * 0.84 + uv.x * 0.46;
            float w = mix(0.085, 1.90, clamp(u_lac_lit, 0.0, 1.0));
            float lit = 1.0 - smoothstep(0.0, w, abs(axis - u_lac_band));
            col *= mix(0.085, 1.0, clamp(lit + 0.06, 0.0, 1.0));

            col = mix(col, vec3(1.0), clamp(u_lac_hurt, 0.0, 1.0) * 0.85);

            // It leaves by becoming all holes.
            float gone = smoothstep(0.74, 1.0, diss);
            a *= (1.0 - hole * mix(0.50, 1.0, diss)) * (1.0 - gone);
            // 0.85 rather than 0.55: with RGB now clamped to alpha, a
            // lip is only as bright as it is opaque, so an alpha this
            // low was quietly dimming the rim it exists to draw.
            a = max(a, lipv * probe.a * (1.0 - gone) * 0.85);

            // FEATHER THE PLATE. A mesh shader is clipped dead at the
            // rectangle it is drawn on, so anything still opaque when it
            // reaches the boundary is cut off in a straight line -- and a
            // straight line across a figure made of torn paper reads as a
            // container, which is exactly what it is and exactly what the
            // player must never see. The aperture lips are the worst
            // offenders because they are bright rings that get large during
            // an arrival or a departure.
            //
            // This makes the cut impossible rather than unlikely: whatever
            // the strata, the apertures or the stretch do, alpha is already
            // zero before the edge, so the plate can never draw its own
            // outline. It is the guarantee, not the padding -- the padding
            // just decides how much room the effect gets first.
            vec2 pe = min(plate_uv, vec2(1.0) - plate_uv);
            a *= smoothstep(0.0, 0.055, min(pe.x, pe.y));

            // PREMULTIPLIED ALPHA, AND THIS IS THE ONE THAT ACTUALLY DREW THE
            // BOX. Ren'Py's model renderer blends premultiplied: the result is
            // src + dst * (1 - a). So a pixel whose RGB is brighter than its
            // own alpha ADDS light to whatever is behind it, and a pixel at
            // alpha ZERO with bright RGB adds light while claiming to be
            // invisible.
            //
            // Everything in this shader that pushes colour around does it
            // without reference to alpha -- the aperture lips mix toward a
            // near-white, the hurt flash mixes toward white, and the hole
            // samples the coat from somewhere the coat is opaque and paints it
            // where this pixel is transparent. All three write bright RGB
            // across the plate's transparent margin, which is why the plate's
            // own RECTANGLE was visible on screen as a glowing box with hard
            // vertical and horizontal edges.
            //
            // Feathering alpha does not fix it and did not: the feather scales
            // `a` and leaves `col` exactly as bright as it was. Clamping RGB to
            // alpha is the fix, and it is the invariant every one of these body
            // shaders has to hold at its last line -- inv.flesh gets it for
            // free because it only ever scales the whole vec4 at once.
            gl_FragColor = vec4(min(col, vec3(a)), a);
        """)

    try:
        _my_register_lamp()
        MY_LAMP_OK = True
    except Exception as _my_lp_e:
        MY_LAMP_OK = False
        try:
            renpy.log("INV FX: lamp shader failed: %r" % _my_lp_e)
        except Exception:
            pass

    try:
        _my_register_lacuna()
        MY_LACUNA_OK = True
    except Exception as _my_lc_e:
        MY_LACUNA_OK = False
        try:
            renpy.log("INV FX: lacuna shader failed: %r" % _my_lc_e)
        except Exception:
            pass


# --- CONSTANTS AND TUNING ----------------------------------------------------
init python:
    MY_SOUP_IMG = INV_DIR + "hyperspace.png"
    MY_SPRITE = INV_DIR + "mystery.png"

    MY_SPRITE_W, MY_SPRITE_H = 1024, 1536
    # The figure very nearly fills its own canvas (alpha bbox 59,5 - 981,1527),
    # so the correction is small -- but it is applied the same way as the other
    # fights, because the formula is what future art has to be measured with.
    # FORMULA: MY_FIG_D* = (canvas centre) - (bbox centre), per axis.
    MY_FIG_DX, MY_FIG_DY = -8.0, 2.0

    # 0.26 at cy 330 puts the figure between y 130 and y 530: clear below
    # the chrome band (which ends at 80) and clear above the panels (548).
    # At 0.30/296 it ran from 66 to 527 and the case bar, the doubt rule and
    # the FIELD readout were all drawn over the top of it.
    MY_ZOOM_ACT1 = 0.26
    # A plate is a TEXTURE and textures cap at 4096px here. 1536 * 0.90 * 1.30
    # padding is ~1797px, comfortably inside; anything above this zoom is
    # applied to the finished mesh instead of rasterised into the plate.
    MY_PLATE_MAX_ZOOM = 0.90

    # =========================================================================
    # ACT ONE -- THE FIELD
    # =========================================================================
    MY_HP_MAX = 280
    MY_LEADS_MAX = 40
    MY_CASE_MAX = 1000
    # 420 and 20, not 520 and 18. THE TEAR SHOULD LAND ON THE CASE, NOT ON
    # THE CLOCK, and that is a joint requirement rather than a pacing one:
    # the field that carries is the field at the instant of the tear, an
    # ACCUSE only reopens by MY_ACCUSE_REOPEN, and so a bout finished by
    # accusing hands over (the field you accused at + 2). A bout finished by
    # the turn cap hands over whatever the field happened to be, which is
    # usually near the ceiling -- measured, at 520/18 three runs in four
    # ended on the cap and every one of them handed over the maximum
    # population regardless of how well the bout had gone.
    MY_SHIFT_CASE = 420
    MY_SHIFT_TURN_CAP = 20

    # THE FIELD. How many readings of the case are still open, and the only
    # number in act one that matters. Everything else in the bout is a way of
    # pushing it in one direction or the other.
    #
    # MY_FIELD_MIN IS TWO AND IT IS NEVER ONE. NARROW is refused there,
    # forever, with no explanation offered -- which is the Archivist's whole
    # nature delivered as an unavailable menu option and learned for free in
    # one turn. Do not "fix" this. It is also load-bearing for act two, where
    # the field becomes a population: a floor of two means there is always
    # exactly one other thing in the dark with it, at minimum, no matter how
    # well the bout went.
    MY_FIELD_START = 7
    MY_FIELD_MIN = 2
    MY_FIELD_MAX = 12

    # NARROW TAKES TWO OFF, NOT ONE, AND THIS IS THE NUMBER THE WHOLE ACT
    # TURNS ON. The first build had it at one, and the field only ever went
    # UP: the player has a single lever moving it down and the Archivist has
    # three moving it up (INTRODUCE, SOLUTION, REOPENED), so measured over
    # four seeds a bot that narrowed on every available turn went 7 -> 12 and
    # dealt LITERALLY ZERO damage in eighteen turns. A tug of war with one
    # rope on one side and three on the other is not a tug of war.
    MY_NARROW_COST = 5             # leads
    MY_NARROW_FIELD = 2
    MY_NARROW_DOUBT = 7

    # ACCUSE. Worth more the narrower the field is, and the command panel
    # prints the live figure next to the word -- that readout is the entire
    # tutorial for the act and it is a number, not a sentence.
    #   field 12 -> 22      field 7 -> 82      field 4 -> 118    field 2 -> 142
    MY_ACCUSE_BASE = 22
    MY_ACCUSE_PER = 12
    # ...and it reopens the case, because everything a failed accusation ruled
    # out is on the table again. This is the whole rhythm of act one: build a
    # position, spend it, watch it come back.
    MY_ACCUSE_REOPEN = 2
    MY_ACCUSE_DOUBT = 8

    # RECHECK is the honest move and honesty costs. Health, leads and quiet,
    # in exchange for going back over ground you had already covered -- which
    # opens a line of inquiry you had closed.
    MY_RECHECK_HEAL = 68
    MY_RECHECK_LEADS = 14
    MY_RECHECK_DOUBT = 30
    MY_RECHECK_FIELD = 1
    MY_GUARD_MULT = 0.45

    # DOUBT does not climb toward failure. It climbs toward CERTAINTY, which
    # is the thing this Archivist cannot permit, so it is what fires the
    # capstone.
    MY_DOUBT_MAX = 100
    MY_DOUBT_START = 10
    MY_DOUBT_STEP_LO, MY_DOUBT_STEP_HI = 3, 6
    MY_DOUBT_FLOOR = 30

    MY_TEST_BASE = 14
    MY_TEST_PER = 3.2              # being close is what hurts
    MY_INTRO_DMG = 16
    # IT IS AS GOOD AT NARROWING THE CASE AS YOU ARE, and it does it for
    # nothing, unprompted, on more of its turns than any other move. The
    # price is entirely in the other column: a disclosure is the single
    # biggest contributor to DOUBT in the fight, which is to say EVERY
    # KINDNESS IT DOES YOU MOVES YOU CLOSER TO THE CASE BEING REOPENED. That
    # relationship is the character of this Archivist expressed as two
    # numbers, and it is the reason DISCLOSE is not simply a gift.
    MY_DISCLOSE_FIELD = 2
    MY_DISCLOSE_DOUBT = 12
    MY_ALIBI_BACK = 24
    # DENOUEMENT: announced a full turn ahead, always. It is the decision the
    # act is built around -- cash your position in now, or keep narrowing and
    # eat it.
    MY_DN_DMG_BASE = 24
    MY_DN_DMG_PER = 4.5
    MY_DN_FIELD = 3
    MY_REOPEN_DMG = 54
    MY_REOPEN_FIELD = 4
    MY_REOPEN_CASE = 90

    # RUN never works. It is the one joke the form allows and it is played
    # completely straight: every refusal is a true statement about the state of
    # the case, and it is a different true statement each time.
    MY_RUN_WORDS = ("STILL OPEN", "NOT RULED OUT", "INCONCLUSIVE",
                    "SEE FIELD", "PENDING")

    MY_CMDS = (("narrow", "NARROW"), ("accuse", "ACCUSE"),
            ("recheck", "RECHECK"), ("run", "RUN"))

    def my_accuse_damage(field):
        """What ACCUSE is worth at this field. Printed live in the menu."""
        field = int(inv_clamp(field, MY_FIELD_MIN, MY_FIELD_MAX))
        return int(MY_ACCUSE_BASE + MY_ACCUSE_PER * (MY_FIELD_MAX - field))

    # =========================================================================
    # ACT TWO -- THE DARK
    # =========================================================================
    # Flat, orthographic, overhead -- the same camera Nonfiction has, and the
    # exact photographic negative of its page. Continuous space, no grid: the
    # grid is the other half of being Nonfiction and this fight is not it.
    MY_AR_X, MY_AR_Y = 118, 96
    MY_AR_W, MY_AR_H = 1044, 528

    MY_SPEED = 3.9                 # px per tick
    MY_PLAYER_R = 13.0

    MY_HP2_MAX = 280
    MY_HIT_HP = 22                 # thirteen contacts
    MY_IFRAMES = 72

    # THE LAMP. The only light in the encounter, and it does not reach far.
    MY_LAMP_R = 132.0
    MY_LAMP_MIN = 54.0             # what SWEEP leaves you with
    # The recovery rate is DERIVED from the blind window rather than picked,
    # so the two can never disagree: change MY_SWEEP_BLIND and the lamp comes
    # back over exactly that many ticks. (Horror's HOR_STRUCT_PHASE lesson.)

    # SWEEP is the bargain verb, and every one of these fights has one.
    # Biography's is standing inside the blade's reach, Horror's is looking
    # back at the thing chasing you, Nonfiction's is rooting yourself on a
    # page that is closing. Mystery's is SEEING MORE AT THE PRICE OF YOUR
    # EYES: it is the only way to gather fast enough to keep a field tight,
    # and the recovery is the most dangerous window in the act.
    MY_SWEEP_R = 336.0
    MY_SWEEP_TICKS = 18
    MY_SWEEP_BLIND = 108
    MY_SWEEP_CD = 200

    # THE POPULATION -- act one's field, standing in the dark.
    MY_BODIES_MIN, MY_BODIES_MAX = 2, 6
    MY_BODY_HARDCAP = 7            # what closing in is allowed to add up to
    MY_REPLACE_DELAY = 96          # a ruled-out body is replaced, not removed

    # SPEEDS. Every one of these is below MY_TRACE_SPREAD and that is a
    # CORRECTNESS constraint, not a balance one: a trace's disc grows at
    # MY_TRACE_SPREAD, and if any body could outrun its own disc then the
    # statement the disc makes would be FALSE. This Archivist does not get to
    # say a false thing. If a speed here is ever raised, raise the spread with
    # it, and read the note in the header about what that costs.
    MY_SUB_SPEED = 0.85            # the subject, at the start of the act
    MY_SUB_SPEED_HOT = 1.15        # ...and by the end
    MY_BYS_SPEED_LO, MY_BYS_SPEED_HI = 0.55, 1.00
    MY_TRACE_SPREAD = 1.20
    MY_BREAK_SPEED = 13.0          # the break-away after a landed accusation
    # HOW FAR A BREAK-AWAY CARRIES, and it is a bound rather than a taste.
    # A contact mark is made at the exact moment of contact and the thing then
    # breaks away faster than MY_TRACE_SPREAD, so the mark would be making a
    # claim it cannot support -- unless the claim is widened by the whole
    # distance the break can cover. Geometric series, worst case of the two
    # contact breaks: the subject leaves at MY_BREAK_SPEED * 0.62 under 0.905
    # friction for 34 ticks, which sums to 82px; the bystander's startle sums
    # to 51. So 88 is the smallest honest slack, and a contact remains by a
    # wide margin the tightest statement in the act.
    MY_BREAK_REACH = 88.0

    MY_TOUCH_R = 26.0

    # TRACES.
    #   dropped     every MY_TRACE_EVERY ticks by every body, wherever it is
    #   glimmering  for MY_TRACE_GLIMMER ticks it is faintly visible from
    #               ANYWHERE in the room -- a cold spark in the black. That is
    #               what makes the dark readable and what drives every metre
    #               you walk: a spark is something that moved out there just
    #               now, and you have a window to go and get it.
    #   dark        after that it can only be found by putting light on it,
    #               which is what SWEEP is for
    #   collected   permanently. It becomes a live constraint AND a survey
    #               mark that never leaves the room again.
    MY_TRACE_EVERY_LO, MY_TRACE_EVERY_HI = 96, 150
    # MARKS COME IN BURSTS, NOT ONE AT A TIME, and the reason is the same
    # arithmetic that made ranges necessary in the first place. Three rings
    # settle a position; three rings about THE SAME BODY are what you need,
    # and marks arriving one at a time from a room full of bodies never give
    # you three of anything. A burst puts three of them into the room inside
    # half a second, so a cluster of sparks appearing in the dark is one
    # thing's worth of evidence and going to fetch it is one decision.
    #
    # They are still scattered -- each is measured from its own offset -- so
    # the three rings cross at real angles rather than sitting concentric,
    # which would be three statements with one statement's worth of content.
    MY_TRAIL_LEN = 3
    MY_TRAIL_GAP = 26
    # A RANGE is measured from a point this far off the body, so that rings
    # cross each other at useful angles. Too small and every ring is a dot
    # sitting on top of the answer; too large and they all meet nearly
    # parallel, which is the same as having one of them.
    MY_RANGE_LO, MY_RANGE_HI = 95.0, 355.0
    MY_TRACE_GLIMMER = 100
    MY_TRACE_LIFE = 900            # uncollected housekeeping only
    # A disc bigger than this says nothing, so the constraint drops out of the
    # live set. Useful life = MY_TRACE_MAXR / MY_TRACE_SPREAD = 240 ticks.
    # THAT NUMBER IS THE FIGHT. Three overlapping discs inside a four second
    # window is a knot worth walking to; two is a smear; one is a rumour.
    MY_TRACE_MAXR = 300.0
    MY_TRACE_MAXR_HOT = 235.0      # the case goes colder as it goes on
    MY_LIVE_MAX = 8                # shader slots, and the freshest eight win

    # ACCUSE, act two. Act one's word, deliberately -- rule 1 forbids the
    # sentence that would explain a new one, and the player has spent a whole
    # act learning what this one means.
    MY_NAME_TICKS = 40
    # TWO COOLDOWNS, AND THE DIFFERENCE BETWEEN THEM IS WHAT A WIDE FIELD
    # ACTUALLY COSTS YOU. A landed accusation lets you carry straight on; a
    # wrong one takes twice as long to come back from. Nothing else in the act
    # scales with the population as cleanly: more things in the room means
    # more of your accusations land on the wrong one, and the bill arrives as
    # time rather than as damage, which is the only currency this act is
    # allowed to charge in (health has exactly one source and it is not this).
    MY_NAME_CD = 46
    MY_NAME_CD_MISS = 72
    MY_NAME_R = 92.0
    MY_NAME_DRIFT = 1.05           # you may creep this much per tick, no more

    MY_SOLVE_MAX = 100.0
    # 25, not 17: FOUR landed accusations, not six. Measured, six ran the act
    # to 90-256s against a family band of 40-90 (Biography 26-48, Nonfiction
    # 29-167, Horror 63-90) -- and the extra two were not extra fight, they
    # were the same loop twice more. Density x duration is what should match
    # across the set, not duration.
    MY_SOLVE_GAIN = 25.0
    # GETTING IT RIGHT IS WHAT KEEPS YOU IN THE ROOM. Biography's rule --
    # aggression is the heal -- in this fight's own terms, and it is what
    # makes the act self-balancing rather than a fixed budget of contacts:
    # health is the only loss condition and the only source of it is a
    # subject you failed to locate, so the player who is locating it is
    # exactly the player who should not be bleeding. Without it every long
    # run was a death rather than a long run.
    MY_SOLVE_HEAL = 30
    # Past this, every landed accusation ALSO puts another body in the room.
    # Closing in widens the field -- act one's law arriving in act two's
    # language, and the reason the endgame is the hardest part of the act.
    MY_SOLVE_HARD = 0.62

    # REOPENING. Act one's capstone, carried through the tear in a new
    # costume: every live constraint is voided. Telegraphed from the edges of
    # the room inward, and the decision it forces is exactly the act-one one --
    # spend the position you have or lose it.
    MY_REOPEN_EVERY = 900
    MY_REOPEN_EVERY_HOT = 660
    MY_REOPEN_WARN = 150

    # DREAD is the fairness channel: the ONLY damage source in the act is the
    # subject reaching you, and this is what tells you it is coming. It starts
    # at eight times contact range, it drives the heartbeat, the lamp's
    # flicker and the frame closing in, and it requires no deduction at all.
    # Rule 5 holds in a fight against something invisible because of this
    # number. It is not allowed to be subtle.
    #
    # AND IT IS THE SECOND HALF OF AIMING, WHICH IS THE POINT. A knot in the
    # belief field tells you SOMETHING is there; whether you can feel it
    # tells you WHICH something. Standing on a bright knot in complete calm
    # is how you learn you have been triangulating a bystander -- and it
    # costs nothing to learn, where accusing costs MY_NAME_CD_MISS. Measured,
    # a bot that reads the field and ignores this spends four fifths of the
    # act accusing empty floor.
    #
    # It is deliberately ANALOGUE and deliberately never a number: a flicker,
    # a heartbeat and a closing frame can tell you "not here" without ever
    # telling you "there", so it can veto a knot without replacing the work
    # that found one. Do not ever print it.
    MY_DREAD_NEAR = 240.0
    MY_DREAD_FULL = 46.0

    # How many of the collected ranges still carry their circle. Beyond this
    # the oldest keep their mark and lose their ring -- see _render_dark.
    MY_LATTICE_RINGS = 130

    MY_HEART_ZOOM = 2.6
    # The same figure the user pulled twice on the other two: it has to look
    # wrong without becoming the busiest object on screen -- and in here it is
    # also the only thing you can reliably find, so it may not be hard to see.
    MY_HEART_WARP = 1.15

    # --- palette: black, chalk, and exactly one warm thing -------------------
    MY_BLACK = "#04050a"
    MY_PALE = "#dce4ee"
    MY_DIM = "#7d8794"
    MY_FAINT = "#4a525e"
    MY_CHALK = "#9aa6b4"           # the survey lattice: everything you proved
    MY_GOLD = "#e6b855"            # the belief field, and nothing else
    MY_RED = "#c22a3c"             # contact, and the case reopening
    MY_WARN = "#c8913a"
    MY_WIN = "#060810e8"
    MY_LAMPC = "#bcd2e4"

    def my_arena_clamp(x, y, r=0.0):
        return (inv_clamp(x, MY_AR_X + r, MY_AR_X + MY_AR_W - r),
                inv_clamp(y, MY_AR_Y + r, MY_AR_Y + MY_AR_H - r))

    def my_arena_center():
        return (MY_AR_X + MY_AR_W * 0.5, MY_AR_Y + MY_AR_H * 0.5)


# --- SIMULATION --------------------------------------------------------------
init python:
    class MYGame(object):
        """All of Mystery's live state, stepped at a fixed 60Hz by MYStage.
        Owns zero rendering."""

        def __init__(self, retry=False, deaths=0, debug=False, start_open=False):
            self.result = None
            self.paused = False
            self.debug = bool(debug)
            self.retry = bool(retry)
            self.deaths = int(deaths)
            self.god = inv_godmode_on()

            self.tick = 0
            self.clock = 0.0
            self.rng = inv_random.Random()
            # Decoration draws from its OWN stream. Respawning grain out of the
            # gameplay RNG costs a whole round of results and reads as a
            # balance swing that is not there (the lesson is Biography's).
            self.rng_fx = inv_random.Random(0x4D595354)

            # --- the party member ------------------------------------------
            self.hp = MY_HP_MAX
            self.hp_shown = float(MY_HP_MAX)
            self.leads = MY_LEADS_MAX
            self.leads_shown = float(MY_LEADS_MAX)
            self.roll_cue = 0

            # --- the case ---------------------------------------------------
            # case  what you have taken off its account of itself.
            # field how many readings are still open. THE number in act one.
            self.case = 0
            self.case_shown = 0.0
            self.field = MY_FIELD_START
            self.field_shown = float(MY_FIELD_START)
            self.doubt = float(MY_DOUBT_START)

            # --- act one ------------------------------------------------------
            self.mode = "arrive"
            self.mtick = 0
            self.turn = 0
            self.cursor = 0
            self.guard = False
            self.dn_pending = False        # DENOUEMENT announced, not landed
            self.last_cmd = None
            self.last_enemy = None
            self.run_i = 0

            self.beat_label = ""
            self.beat_value = ""
            self.beat_after = "menu"

            # --- presentation --------------------------------------------------
            self.flash = 0.0
            self.dark = 1.0
            self.shake = 0.0
            self.open = 0.0                # 0 = the room, 1 = the dark
            # 1.0, not 0.0: the panels start OFF the bottom of the screen
            # and slide up once the bout actually begins (see _step_ambient).
            # They used to exist from frame one and simply go undrawn during
            # the arrival, which meant they appeared whole on a single frame,
            # at the same instant the body took its place -- one pop reading as
            # two things going wrong at once.
            self.panel_slide = 1.0
            self.hit_flash = 0.0
            self.floats = []
            self.hole = [640.0, 330.0, 240.0, 0.0]
            self.emerge = 1.0
            self.body_ap = 0.35            # aperture size on the body
            self.body_diss = 1.0           # it leaves by becoming all holes
            self.body_lit = 0.0            # how much of it is lit at once
            self.body_band = 0.30          # where the lit sliver is
            self.beat = 0.0
            self.beat_pulse = 0.0
            self.field_carried = MY_FIELD_START

            # --- act two --------------------------------------------------------
            self.px, self.py = my_arena_center()
            self.trail = []
            self.lamp_r = MY_LAMP_R
            self.lamp_s = 0.0              # lamp strength, ramps at the tear
            self.sweep_t = 0
            self.sweep_cd = 0
            self.solve = 0.0
            self.solve_shown = 0.0
            self.iframes = 0
            self.dist = 0.0                # ticks survived, for the ramp

            self.bodies = []
            self.body_seq = 0
            self.replace_q = []            # ticks until a bystander walks in
            self.traces = []
            self.live = []                 # the freshest MY_LIVE_MAX
            self.exclusions = []           # where you looked and found nothing
            self.ruleouts = []             # where you ruled somebody out

            self.naming = False
            self.name_t = 0
            self.name_cd = 0
            self.name_flash = 0.0
            self.reopen_t = MY_REOPEN_EVERY
            self.reopen_warn = 0.0
            self.dread_v = 0.0
            self.collect_flash = 0.0

            self.hud_fade = 1.0
            self.end_close = 0.0           # the loss: the lamp going out
            self.lattice_off = 0.0         # the loss: the survey going with it
            self.end_show = 0.0            # the win: it is finally all lit

            self.keys = MSBFKeyLatch()
            self._prev = {"left": False, "right": False, "up": False,
                        "down": False, "z": False, "x": False}

            if start_open:
                # Dev entry skips the bout, so hand over a middling field --
                # a bout that never happened cannot have ruled anything out.
                self.field = 4
                self.case = 300
                self._begin_dark(dev=True)

        # ----- helpers ---------------------------------------------------------

        def play(self, name, volume_scale=1.0):
            inv_play(name, volume_scale)

        def toggle_pause(self):
            if self.result is None:
                self.paused = not self.paused
                self.play("cancel" if self.paused else "confirm", 0.6)

        def give_up(self):
            if self.result is None:
                self.result = "quit"

        def toggle_god(self):
            if not config.developer:
                return
            inv_toggle_godmode()
            self.god = inv_godmode_on()
            self.play("scan", 0.7)
            renpy.notify("GODMODE " + ("ON" if self.god else "OFF"))

        def standing(self):
            """What is left of its account of itself."""
            return max(0, MY_CASE_MAX - self.case)

        def standing_frac(self):
            return inv_clamp(self.standing() / float(MY_CASE_MAX), 0.0, 1.0)

        def doubt_frac(self):
            return inv_clamp(self.doubt / float(MY_DOUBT_MAX), 0.0, 1.0)

        def solve_frac(self):
            return inv_clamp(self.solve / MY_SOLVE_MAX, 0.0, 1.0)

        def progress(self):
            """0 at the tear, 1 by the time act two should be over."""
            return inv_clamp(self.dist / 5400.0, 0.0, 1.0)

        def heat(self):
            """HOW COLD THE CASE HAS GOT, 0 to 1.

            One number, continuously, exactly like Nonfiction's churn() and
            for the same reason: the act should tighten the way a case goes
            cold rather than by switching a layer on at a threshold. Half of
            it is how long you have been in the dark and half is how far onto
            the answer you have got, so a slow run and a fast one arrive at
            the same pressure.
            """
            return inv_clamp(0.5 * self.progress() + 0.5 * self.solve_frac(),
                            0.0, 1.0)

        def subject(self):
            for b in self.bodies:
                if b["subject"]:
                    return b
            return None

        def dread(self):
            return self.dread_v

        def live_weight(self):
            """The weight the shader normalises the belief field by: the sum
            of the live set's PRECISIONS rather than its size. Kept here so
            the renderer and the shader cannot disagree about it."""
            maxr = self.trace_maxr()
            total = 0.0
            for tol, tr in self.live:
                total += inv_clamp(1.0 - tol / max(maxr, 1.0), 0.10, 1.0)
            return max(total, 0.35)

        def trace_maxr(self):
            return inv_lerp(MY_TRACE_MAXR, MY_TRACE_MAXR_HOT, self.heat())

        def _beat(self, label, value="", after="enemy"):
            self.beat_label = label
            self.beat_value = value
            self.beat_after = after
            self.mode = "beat"
            self.mtick = 0

        def float_text(self, x, y, text, color, big=False):
            self.floats.append({"x": x, "y": y, "vy": -1.6, "life": 52,
                                "text": text, "color": color, "big": big})

        def hurt(self, amount, x=None, y=None):
            amount = int(max(0, amount))
            if amount <= 0:
                return
            if not self.god:
                self.hp = int(max(0, self.hp - amount))
            self.shake = min(1.0, self.shake + 0.6)
            self.hit_flash = 1.0
            self.play("hurt")
            if x is not None:
                col = MY_DIM if self.god else MY_RED
                self.float_text(x, y, "-%d" % amount, col, True)

        def _deal(self, amount):
            """Take something off its account of itself."""
            amount = int(max(0, amount))
            self.case = int(min(MY_CASE_MAX, self.case + amount))
            return amount

        def _set_field(self, value):
            self.field = int(inv_clamp(value, MY_FIELD_MIN, MY_FIELD_MAX))

        # ----- input -----------------------------------------------------------

        def _poll_input(self):
            pg = inv_pg
            if pg is None:
                return None
            try:
                keys = pg.key.get_pressed()
            except Exception:
                return None

            blank = {"left": False, "right": False, "up": False,
                    "down": False, "z": False, "x": False}
            if not self.keys.focused():
                self.keys.stuck = set()
                self._prev.update(blank)
                edges = dict((k, False) for k in blank)
                edges["held"] = blank
                return edges

            cur = {
                "left": self.keys.pressed(keys, pg.K_LEFT, pg.K_a),
                "right": self.keys.pressed(keys, pg.K_RIGHT, pg.K_d),
                "up": self.keys.pressed(keys, pg.K_UP, pg.K_w),
                "down": self.keys.pressed(keys, pg.K_DOWN, pg.K_s),
                "z": self.keys.pressed(keys, pg.K_z, pg.K_RETURN, pg.K_KP_ENTER),
                "x": self.keys.pressed(keys, pg.K_x, pg.K_LSHIFT, pg.K_RSHIFT),
            }
            edges = {}
            for k in ("z", "x", "left", "right", "up", "down"):
                edges[k] = cur[k] and not self._prev[k]
                self._prev[k] = cur[k]
            edges["held"] = cur
            return edges

        # ----- dispatcher --------------------------------------------------------

        def step(self):
            edges = self._poll_input() or {
                "z": False, "x": False, "left": False, "right": False,
                "up": False, "down": False,
                "held": {"left": False, "right": False, "up": False,
                        "down": False, "z": False, "x": False},
            }
            self._step_ambient()
            if self.result is not None:
                return

            mode = self.mode
            if mode == "arrive":
                self._step_arrive()
            elif mode == "menu":
                self._step_menu(edges)
            elif mode == "beat":
                self._step_beat(edges)
            elif mode == "enemy":
                self._step_enemy()
            elif mode == "shift":
                self._step_shift()
            elif mode == "dark":
                self._step_dark(edges)
            elif mode in ("leave_w", "leave_l"):
                self._step_leave()

        def _step_ambient(self):
            self.tick += 1
            self.clock += INV_TICK

            self.beat += 1.0 / INV_BEAT_TICKS
            if self.beat >= 1.0:
                self.beat -= 1.0
                self.beat_pulse = 1.0
            self.beat_pulse *= 0.88

            self.flash *= 0.86
            self.shake *= 0.88

            # THE PANELS SEAT THEMSELVES once the bout begins. Guarded to the
            # act-one modes on purpose: the shift drives this same value the
            # other way (0 -> 1) to throw the panels off the screen, and a
            # decay running underneath that would fight it.
            if self.mode in ("menu", "beat", "enemy") and self.panel_slide > 0.0:
                self.panel_slide = max(0.0, self.panel_slide - 0.042)

            self.hit_flash *= 0.88
            self.name_flash *= 0.90
            self.collect_flash *= 0.90

            # The lit sliver never stops travelling across it. Nothing on this
            # body is ever held still and nothing on it ever jumps.
            self.body_band = 0.30 + 0.62 * (0.5 + 0.5 * math.sin(
                self.clock * 0.37))

            for attr, real in (("hp_shown", self.hp), ("leads_shown", self.leads)):
                shown = getattr(self, attr)
                gap = abs(shown - real)
                if gap > 0.01:
                    rate = inv_clamp(gap * 0.02, 0.25, 1.7)
                    setattr(self, attr, inv_approach(shown, float(real), rate))
                    if attr == "hp_shown":
                        self.roll_cue += 1
                        if self.roll_cue % 7 == 0:
                            self.play("roll", 0.5)
                else:
                    setattr(self, attr, float(real))

            gap = abs(self.case_shown - self.case)
            if gap > 0.01:
                self.case_shown = inv_approach(self.case_shown, float(self.case),
                                            inv_clamp(gap * 0.10, 0.6, 9.0))
            else:
                self.case_shown = float(self.case)

            # THE FIELD ROLLS TOO, and slowly. It is the number this whole
            # fight is about, so it is never allowed to simply change value
            # between one frame and the next -- you have to watch it move.
            gap = abs(self.field_shown - self.field)
            if gap > 0.005:
                self.field_shown = inv_approach(self.field_shown,
                                                float(self.field),
                                                inv_clamp(gap * 0.10, 0.012, 0.09))
            else:
                self.field_shown = float(self.field)

            gap = abs(self.solve_shown - self.solve)
            if gap > 0.005:
                self.solve_shown = inv_approach(self.solve_shown, self.solve,
                                                inv_clamp(gap * 0.12, 0.05, 1.4))
            else:
                self.solve_shown = self.solve

            for f in self.floats:
                f["y"] += f["vy"]
                f["vy"] += 0.055
                f["life"] -= 1
            self.floats = [f for f in self.floats if f["life"] > 0]

            if self.hp_shown <= 0.0 and self.mode not in ("leave_w", "leave_l",
                                                        "arrive"):
                self._begin_leave(False)

        # =====================================================================
        # ARRIVAL -- the light fails, three times
        # =====================================================================
        # It is never seen arriving. Nothing walks out of the rupture and
        # nothing is assembled in front of you: the room simply loses its light
        # for a moment, and when the light comes back there is more of it
        # standing there than there was. Rule 4 is honoured by what the hole
        # TAKES rather than by what it gives.

        def _step_arrive(self):
            self.mtick += 1
            t = self.mtick
            self.dark = inv_clamp(1.0 - t / 30.0, 0.0, 1.0)

            if t == 6:
                self.play("tear", 0.75)
            if t < 70:
                self.hole[3] = inv_smooth(t / 70.0)
                self.hole[2] = inv_lerp(30.0, 240.0, inv_smooth(t / 70.0))
                self.body_diss = 1.0
                self.body_lit = 0.0
                self.emerge = 1.0
            elif t < 250:
                self.hole[3] = 1.0
                # THREE FAILURES OF THE LIGHT. Each one is a hard drop to
                # black and a slower recovery, and each recovery brings back
                # more of it than the last.
                if t in (76, 136, 196):
                    self.play("phase", 0.5)
                    self.dark = 1.0
                    self.shake = 0.30
                step_i = 0 if t < 136 else (1 if t < 196 else 2)
                since = t - (76, 136, 196)[step_i]
                if since >= 0:
                    self.dark = max(self.dark,
                                    inv_clamp(1.0 - since / 34.0, 0.0, 1.0))
                self.body_diss = (0.74, 0.42, 0.12)[step_i]
                self.body_ap = (0.85, 0.62, 0.42)[step_i]
                self.body_lit = (0.06, 0.14, 0.24)[step_i]
                self.emerge = 1.0 - inv_clamp((t - 76) / 170.0, 0.0, 1.0)
            elif t < 300:
                u = (t - 250) / 50.0
                self.body_diss = inv_lerp(0.12, 0.0, inv_smooth(u))
                self.body_ap = inv_lerp(0.42, 0.34, inv_smooth(u))
                self.hole[3] = 1.0 - inv_smooth(u)
                self.hole[2] = inv_lerp(240.0, 24.0, inv_smooth(u))
            elif t == 300:
                self.hole[3] = 0.0
                self.body_diss = 0.0
                inv_music_survey()
            elif t >= 336:
                self._begin_player_turn()

        # =====================================================================
        # ACT ONE -- THE FIELD
        # =====================================================================

        def _begin_player_turn(self):
            self.mode = "menu"
            self.mtick = 0
            self.turn += 1
            self.cursor = 0
            self.guard = False

        def _step_menu(self, edges):
            self.mtick += 1
            n = len(MY_CMDS)
            if edges["up"]:
                self.cursor = (self.cursor - 1) % n
                self.play("cursor")
            elif edges["down"]:
                self.cursor = (self.cursor + 1) % n
                self.play("cursor")
            if edges["z"]:
                self.play("confirm")
                self._resolve_player(MY_CMDS[self.cursor][0])

        def _step_beat(self, edges):
            # WAITS. Never advances on its own.
            self.mtick += 1
            if self.mtick > 12 and (edges["z"] or edges["x"]):
                self.play("confirm", 0.7)
                after = self.beat_after
                self.beat_label = ""
                self.beat_value = ""
                if after == "enemy":
                    self.mode = "enemy"
                    self.mtick = 0
                elif after == "shift":
                    self.mode = "shift"
                    self.mtick = 0
                else:
                    self._begin_player_turn()

        def _resolve_player(self, cmd):
            self.last_cmd = cmd
            label, value = cmd.upper(), ""

            if cmd == "narrow":
                # THE REFUSAL. Two is the floor and it is the floor forever,
                # and the game does not say why. One turn spent finding this
                # out is the cheapest and most complete piece of
                # characterisation in the encounter -- do not add a line of
                # text explaining it and do not lift the floor.
                if self.field <= MY_FIELD_MIN:
                    self.play("cancel")
                    self._beat("NARROW", "TWO REMAIN", "menu")
                    return
                if self.leads < MY_NARROW_COST:
                    self.play("cancel")
                    self._beat("NARROW", "NO LEADS", "menu")
                    return
                self.leads -= MY_NARROW_COST
                self._set_field(self.field - MY_NARROW_FIELD)
                self.doubt = min(float(MY_DOUBT_MAX),
                                self.doubt + MY_NARROW_DOUBT)
                self.play("scan", 0.7)
                self.flash = 0.22
                value = "FIELD  %d" % self.field

            elif cmd == "accuse":
                dealt = self._deal(my_accuse_damage(self.field))
                self.doubt = min(float(MY_DOUBT_MAX),
                                self.doubt + MY_ACCUSE_DOUBT)
                self.play("bash")
                self.shake = 0.34
                self.flash = 0.30
                value = "-%d" % dealt
                # ...and the case reopens, because everything that accusation
                # ruled out is on the table again.
                before = self.field
                self._set_field(self.field + MY_ACCUSE_REOPEN)
                if self.field != before:
                    value += "   FIELD  %d" % self.field

            elif cmd == "recheck":
                self.hp = int(min(MY_HP_MAX, self.hp + MY_RECHECK_HEAL))
                self.leads = int(min(MY_LEADS_MAX,
                                    self.leads + MY_RECHECK_LEADS))
                self.doubt = max(0.0, self.doubt - MY_RECHECK_DOUBT)
                self.guard = True
                before = self.field
                self._set_field(self.field + MY_RECHECK_FIELD)
                self.play("heal")
                value = "+%d" % MY_RECHECK_HEAL
                if self.field != before:
                    value += "   FIELD  %d" % self.field

            elif cmd == "run":
                # It never works, and the reason is different every time --
                # and every reason is a true statement about the case.
                self.play("miss")
                value = MY_RUN_WORDS[self.run_i % len(MY_RUN_WORDS)]
                self.run_i += 1

            after = "enemy"
            if self.case >= MY_SHIFT_CASE:
                after = "shift"
            self._beat(label, value, after)

        def _pick_enemy_move(self):
            if self.dn_pending:
                return "solution"
            # DISCLOSE is its commonest move and that is the character: the
            # thing you are fighting spends most of its turns HELPING you, for
            # free, correctly.
            pool = ["disclose", "disclose", "testimony", "introduce"]
            if self.field <= 4:
                # The narrower you are, the more it wants to announce an
                # ending -- which is the decision the act is built around.
                pool += ["denouement", "denouement", "testimony"]
            elif self.turn >= 4:
                pool.append("denouement")
            if self.field <= MY_FIELD_MIN:
                pool = [m for m in pool if m != "disclose"] or ["testimony"]
            if self.case > 180:
                pool.append("alibi")
            if self.last_enemy in pool and len(set(pool)) > 1:
                pool = [m for m in pool if m != self.last_enemy] or pool
            return self.rng.choice(pool)

        def _step_enemy(self):
            self.mtick += 1
            if self.mtick < 26:
                return

            self.doubt = min(float(MY_DOUBT_MAX),
                            self.doubt + self.rng.randint(MY_DOUBT_STEP_LO,
                                                        MY_DOUBT_STEP_HI))

            # THE CAPSTONE. Doubt full: certainty is the one thing it cannot
            # allow, so the case is REOPENED and the whole position goes.
            if self.doubt >= MY_DOUBT_MAX:
                self.doubt = float(MY_DOUBT_FLOOR)
                self.dn_pending = False
                self.last_enemy = "reopened"
                back = min(self.case, MY_REOPEN_CASE)
                self.case -= back
                before = self.field
                self._set_field(self.field + MY_REOPEN_FIELD)
                self.play("break", 0.95)
                self.flash = 0.78
                self.shake = 1.0
                dmg = MY_REOPEN_DMG
                if self.guard:
                    dmg = int(dmg * MY_GUARD_MULT)
                self.hurt(dmg, 640, 470)
                self.guard = False
                value = "FIELD  %d" % self.field
                if back:
                    value += "   +%d" % back
                self._beat("REOPENED", value, self._after_enemy())
                return

            move = self._pick_enemy_move()
            self.last_enemy = move
            label = move.upper()
            value = ""
            dmg = 0

            if move == "disclose":
                # It rules one out for you. Free, correct, and it costs you
                # nothing but the certainty it buys.
                before = self.field
                self._set_field(self.field - MY_DISCLOSE_FIELD)
                self.doubt = min(float(MY_DOUBT_MAX),
                                self.doubt + MY_DISCLOSE_DOUBT)
                self.play("note", 0.85)
                self.flash = 0.18
                value = "FIELD  %d" % self.field
                if self.field == before:
                    value = "TWO REMAIN"

            elif move == "testimony":
                # The narrower you are, the more it costs to hold it there.
                dmg = int(MY_TEST_BASE
                        + MY_TEST_PER * (MY_FIELD_MAX - self.field))

            elif move == "introduce":
                before = self.field
                self._set_field(self.field + (2 if self.turn >= 10 else 1))
                dmg = MY_INTRO_DMG
                self.play("refuse", 0.7)
                if self.field != before:
                    value = "FIELD  %d   " % self.field

            elif move == "alibi":
                back = min(self.case, MY_ALIBI_BACK)
                self.case -= back
                self.play("refuse", 0.65)
                value = "+%d" % back

            elif move == "denouement":
                # Announced a full turn in advance, because it always is.
                self.dn_pending = True
                self.play("note", 0.95)
                self.flash = 0.22
                value = "PENDING"

            elif move == "solution":
                # ...and it is not one. It costs most when you are closest to
                # having your own, and it puts the field back.
                self.dn_pending = False
                label = "SOLUTION"
                dmg = int(MY_DN_DMG_BASE
                        + MY_DN_DMG_PER * (MY_FIELD_MAX - self.field))
                before = self.field
                self._set_field(self.field + MY_DN_FIELD)
                self.play("cut_big", 0.9)
                self.flash = 0.55
                self.shake = 0.8
                if self.field != before:
                    value = "FIELD  %d   " % self.field

            if dmg > 0:
                if self.guard:
                    dmg = int(dmg * MY_GUARD_MULT)
                self.play("enemy", 0.8)
                self.hurt(dmg, 640, 470)
                value += "-%d" % dmg

            self.guard = False
            self._beat(label, value, self._after_enemy())

        def _after_enemy(self):
            if self.case >= MY_SHIFT_CASE or self.turn >= MY_SHIFT_TURN_CAP:
                return "shift"
            return "menu"

        # =====================================================================
        # THE TEAR -- the lights go out and the field walks in
        # =====================================================================

        def _step_shift(self):
            self.mtick += 1
            t = self.mtick

            if t == 1:
                inv_music_stop(0.3)
                self.play("tear")
                # WHAT CARRIES. Not health, not leads -- the FIELD. Everything
                # you failed to rule out is about to be a thing in the room.
                self.field_carried = int(inv_clamp(self.field, MY_BODIES_MIN,
                                                MY_BODIES_MAX))
            if t == 24:
                self.float_text(640, 300, "FIELD  %d" % self.field_carried,
                                MY_PALE, True)
                self.play("scan", 0.9)
            if 60 <= t < 150:
                self.panel_slide = inv_smooth((t - 60) / 90.0)
                self.shake = max(self.shake, 0.26)
            if 60 <= t < 170:
                # Every light in the room going out, one at a time.
                self.dark = inv_clamp((t - 60) / 110.0, 0.0, 1.0)
                self.body_lit = max(0.0, 0.24 - 0.24 * ((t - 60) / 110.0))
            if t == 170:
                self.play("slam")
                self.play("phase", 0.9)
                self.shake = 1.0
                inv_music_corruptive()
                inv_heart_start(0.0)
                # Whole again for the second half: act one's currency was the
                # FIELD, and that is what carries.
                self.hp = MY_HP2_MAX
                self.leads = MY_LEADS_MAX
            if 170 <= t < 250:
                self.open = inv_clamp((t - 170) / 80.0, 0.0, 1.0)
                # The room is not lit again. Only the lamp comes up.
                self.dark = inv_clamp(1.0 - (t - 170) / 80.0, 0.0, 1.0)
                self.lamp_s = inv_smooth((t - 170) / 80.0)
            if t == 250:
                self.open = 1.0
                self.dark = 0.0
                self.lamp_s = 1.0
                self._begin_dark()

        # =====================================================================
        # ACT TWO -- THE DARK
        # =====================================================================

        def _begin_dark(self, dev=False):
            self.mode = "dark"
            self.mtick = 0
            self.open = 1.0
            self.dark = 0.0
            self.lamp_s = 1.0
            self.lamp_r = MY_LAMP_R
            self.hp = MY_HP2_MAX
            self.hp_shown = float(MY_HP2_MAX)
            self.px, self.py = my_arena_center()
            self.panel_slide = 1.0
            self.hole[3] = 0.0

            if dev:
                self.field_carried = int(inv_clamp(self.field, MY_BODIES_MIN,
                                                MY_BODIES_MAX))
                inv_music_corruptive()
                inv_heart_start(0.0)

            # THE JOINT. Act one's counter, made of bodies.
            self.bodies = []
            self.body_seq = 0
            self._add_body(subject=True)
            for _n in range(max(0, self.field_carried - 1)):
                self._add_body(subject=False)

            self.reopen_t = MY_REOPEN_EVERY
            self.reopen_warn = 0.0

        def _add_body(self, subject=False, at=None):
            self.body_seq += 1
            cx, cy = my_arena_center()
            if at is None:
                # It walks in from the edge -- there is nowhere else for it to
                # have come from, and you never see it happen.
                side = self.rng.randrange(4)
                if side == 0:
                    x, y = MY_AR_X + 12, self.rng.uniform(MY_AR_Y, MY_AR_Y + MY_AR_H)
                elif side == 1:
                    x, y = MY_AR_X + MY_AR_W - 12, self.rng.uniform(MY_AR_Y, MY_AR_Y + MY_AR_H)
                elif side == 2:
                    x, y = self.rng.uniform(MY_AR_X, MY_AR_X + MY_AR_W), MY_AR_Y + 12
                else:
                    x, y = self.rng.uniform(MY_AR_X, MY_AR_X + MY_AR_W), MY_AR_Y + MY_AR_H - 12
            else:
                x, y = at
            spd = (MY_SUB_SPEED if subject
                else self.rng.uniform(MY_BYS_SPEED_LO, MY_BYS_SPEED_HI))
            self.bodies.append({
                "id": self.body_seq,
                "subject": bool(subject),
                "x": float(x), "y": float(y),
                "vx": 0.0, "vy": 0.0,
                "ph": self.rng.uniform(0.0, 6.283),
                "rate": self.rng.uniform(0.0035, 0.0068),
                "seed": self.rng.uniform(0.0, 6.283),
                "speed": spd,
                "trace_t": self.rng.randint(20, MY_TRACE_EVERY_HI),
                "trail": MY_TRAIL_LEN,
                "break": 0, "bvx": 0.0, "bvy": 0.0,
                "touch_cd": 0,
                "born": self.tick,
            })

        # ----- the population ---------------------------------------------------

        def _step_bodies(self):
            cx, cy = my_arena_center()
            heat = self.heat()
            # THE ROOM PRODUCES A FIXED AMOUNT OF EVIDENCE, HOWEVER MANY
            # THINGS ARE IN IT. This one line is what makes act one's counter
            # something you FEEL rather than merely count, and it took two
            # measured passes to get right.
            #
            # Left alone, a wider field is a BIGGER PILE OF TRACES and the
            # joint runs backwards: measured, six bodies came out easier than
            # two (hp 112-184 against 40-88) because more of them meant more
            # evidence, more live constraints, and a subject that was near
            # you a smaller fraction of the time. A sub-linear scale halved
            # the effect and did not reverse it.
            #
            # So the interval scales LINEARLY with the population and the
            # total rate is flat. Six bodies leave exactly as much evidence
            # between them as two do -- each one leaves a third as much of
            # it, so every individual thing in the room is three times harder
            # to pin, which is precisely what "you failed to rule these out"
            # ought to cost.
            # EVIDENCE THINS AS THE FIELD WIDENS -- mildly, and the
            # mildness is the tuning. A flat per-body rate makes a wide field
            # EASIER, because more bodies simply means more marks in the room
            # (measured: field 6 won 3/4 where field 2 won 0/4). A flat TOTAL
            # rate overcorrects and starves the two-body case, which then has
            # nothing to work with at all. At 0.70 + 0.30n/2 the room still
            # produces more marks the fuller it is, just not proportionally,
            # so a wide field is noisier per body without either case going
            # hungry.
            crowd = 0.70 + 0.30 * (len(self.bodies) / float(MY_BODIES_MIN))
            lo = int(MY_TRACE_EVERY_LO * (1.0 + 0.40 * heat) * crowd)
            hi = int(MY_TRACE_EVERY_HI * (1.0 + 0.40 * heat) * crowd)

            for b in self.bodies:
                if b["touch_cd"] > 0:
                    b["touch_cd"] -= 1

                if b["break"] > 0:
                    # THE BREAK-AWAY. One impulse under friction, never a pan.
                    # It drops no traces while it is doing this, which is not
                    # a convenience: a trace dropped at this speed would make
                    # a FALSE statement, because its disc grows at
                    # MY_TRACE_SPREAD and it is currently moving faster than
                    # that. This Archivist does not get to say a false thing.
                    b["break"] -= 1
                    b["x"] += b["bvx"]
                    b["y"] += b["bvy"]
                    b["bvx"] *= 0.905
                    b["bvy"] *= 0.905
                    b["x"], b["y"] = my_arena_clamp(b["x"], b["y"], 10.0)
                    continue

                # The wander target rides a lissajous, so even an approach
                # never traces a line (the motion rule, and it matters more
                # here than anywhere: a body moving in a straight line in the
                # dark would be solvable off two traces and a ruler).
                ph = b["ph"] + self.tick * b["rate"]
                tx = cx + math.sin(ph) * MY_AR_W * 0.36 \
                    + math.sin(ph * 0.53 + b["seed"]) * 118.0
                ty = cy + math.cos(ph * 0.81 + b["seed"]) * MY_AR_H * 0.34 \
                    + math.sin(ph * 1.29) * 46.0

                if b["subject"]:
                    # It drifts toward you. It does not charge and it never
                    # will -- it is slower than you are and it is not in a
                    # hurry, which is the entire reason the fight is about
                    # knowing rather than about running.
                    b["speed"] = inv_lerp(MY_SUB_SPEED, MY_SUB_SPEED_HOT, heat)
                    # 0.45, not 0.66. It has to be DRAWN toward you or there
                    # is no tell separating it from a bystander -- the knot
                    # that keeps coming back is the read the whole act turns
                    # on -- but at two thirds it was effectively homing, and
                    # a slow homing thing in a dark room is not a menace, it
                    # is a metronome: contacts arrived on a schedule nothing
                    # the player did could change.
                    tx = inv_lerp(tx, self.px, 0.45)
                    ty = inv_lerp(ty, self.py, 0.45)

                dx, dy = tx - b["x"], ty - b["y"]
                d = math.hypot(dx, dy) or 1.0
                spd = b["speed"]
                b["vx"] += (dx / d) * spd * 0.085
                b["vy"] += (dy / d) * spd * 0.085
                b["vx"] *= 0.94
                b["vy"] *= 0.94
                # HARD SPEED CLAMP. Correctness, not feel -- see the note in
                # the constants block. Nothing may outrun its own disc.
                sp = math.hypot(b["vx"], b["vy"])
                if sp > spd:
                    k = spd / sp
                    b["vx"] *= k
                    b["vy"] *= k
                b["x"] += b["vx"]
                b["y"] += b["vy"]
                b["x"], b["y"] = my_arena_clamp(b["x"], b["y"], 10.0)

                b["trace_t"] -= 1
                if b["trace_t"] <= 0:
                    self._drop_trace(b["x"], b["y"], b["id"])
                    b["trail"] -= 1
                    if b["trail"] > 0:
                        b["trace_t"] = MY_TRAIL_GAP
                    else:
                        b["trail"] = MY_TRAIL_LEN
                        b["trace_t"] = self.rng.randint(lo, hi)

            # A ruled-out body is REPLACED, not removed. There is always
            # somebody else in the room -- that is act one's floor of two,
            # honoured for the whole of act two.
            if self.replace_q:
                self.replace_q = [n - 1 for n in self.replace_q]
                ready = [n for n in self.replace_q if n <= 0]
                self.replace_q = [n for n in self.replace_q if n > 0]
                for _r in ready:
                    if len(self.bodies) < MY_BODY_HARDCAP:
                        self._add_body(subject=False)

        def _drop_trace(self, x, y, body_id, exact=False, collected=False,
                        slack=0.0):
            """Leave one MARK. The statement it makes is true when it is made
            and it stays true forever.

            A RANGE (the ordinary kind): the mark lies at a point some way off
            the body and records HOW FAR AWAY the body was. So it says "it was
            exactly D from here at time t", which as the clock runs means "it
            is somewhere within tol of the circle of radius D about here". One
            of those is a rumour. Two cross in two places. Three settle it.

            THAT IS WHY MARKS ARE RANGES AND NOT POSITIONS, and it is the one
            piece of geometry the whole act rests on. The first build recorded
            positions, which decay into discs -- and discs about the same body
            never combine into anything tighter than the newest one of them,
            because a disc drawn round an older mark is a strict superset of
            the newer one's reachable set. An act built out of discs has no
            deduction in it whatsoever. The harness said so in one line: the
            live set averaged 1.0 marks about any one body, and the belief
            field was a union of unrelated smears.

            A CONTACT (exact=True): D is zero, the annulus collapses to a disc,
            and it is the only evidence in the act worth anything on its own.
            You get it by walking into something in the dark.
            """
            if exact:
                mx, my_, dist = float(x), float(y), 0.0
            else:
                ang = self.rng.uniform(0.0, 6.283185)
                d = self.rng.uniform(MY_RANGE_LO, MY_RANGE_HI)
                mx, my_ = my_arena_clamp(x + math.cos(ang) * d,
                                        y + math.sin(ang) * d, 18.0)
                # The clamp moved the mark, so the range is MEASURED again
                # rather than assumed. A statement this Archivist makes is
                # checked before it is made.
                dist = math.hypot(x - mx, y - my_)
            self.traces.append({
                "x": mx, "y": my_,
                "d": dist,
                "slack": float(slack),
                "t0": self.tick,
                "body": int(body_id),
                "got": bool(collected),
                "got_at": self.tick if collected else 0,
                "void": False,
                "exact": bool(exact),
            })

        # ----- the evidence -----------------------------------------------------

        def _collect(self, radius):
            """Light falling on a trace enters it into the record, forever.
            No key press: a retrieval that needs a button turns the best part
            of the loop into paperwork."""
            got = 0
            for tr in self.traces:
                if tr["got"] or tr["void"]:
                    continue
                if math.hypot(tr["x"] - self.px, tr["y"] - self.py) <= radius:
                    tr["got"] = True
                    tr["got_at"] = self.tick
                    got += 1
            if got:
                self.play("graze", 0.55 + 0.10 * got)
                self.collect_flash = 1.0
            return got

        def _rebuild_live(self):
            """The freshest MY_LIVE_MAX constraints that still say something.

            A constraint is 'that body was D from this mark, and cannot have
            got further than MY_TRACE_SPREAD per tick away from that range
            since'. It is true when collected and it stays true forever -- the
            annulus simply thickens every tick until it is the whole room and
            says nothing, which is a different thing entirely and is the whole
            point of the encounter.
            """
            maxr = self.trace_maxr()
            out = []
            for tr in self.traces:
                if not tr["got"] or tr["void"]:
                    continue
                tol = (tr.get("slack", 0.0)
                    + MY_TRACE_SPREAD * max(0, self.tick - tr["t0"]))
                if tol > maxr:
                    continue
                out.append((max(tol, 6.0), tr))
            out.sort(key=lambda e: e[0])
            self.live = out[:MY_LIVE_MAX]

        def _void_live(self):
            """The case reopens. Everything you had established stops bearing
            on the question -- the survey marks stay on the room forever,
            because they are still TRUE. They are simply no longer evidence."""
            for tr in self.traces:
                if tr["got"]:
                    tr["void"] = True
            self.live = []

        def _void_body(self, body_id):
            """WITHDRAW EVERY STATEMENT ABOUT ONE BODY.

            Called the instant anything enters a break-away, and it is a
            CORRECTNESS routine rather than a balance one. A disc grows at
            MY_TRACE_SPREAD; a body in a break-away moves faster than that;
            so from the frame it breaks, every disc it left behind is making
            a claim that is no longer sound. This Archivist does not get to
            say a false thing, so it takes the statement back rather than
            letting it stand.

            IT WITHDRAWS THE UNCOLLECTED ONES TOO, and that is the whole
            second half of the bug. The first version only voided traces the
            player had already picked up, which looks right and is not: an
            uncollected trace is a statement lying in the dark waiting to be
            read, and a statement does not become unsound at the moment
            somebody reads it. Measured, that left 8-16 false claims a run --
            a trace dropped, the body startled 48px clear of it, and the
            player walked over the trace a minute later and collected a disc
            that had never contained it.
            """
            for tr in self.traces:
                if tr["body"] == body_id:
                    tr["void"] = True

        # ----- act two's turn ----------------------------------------------------

        def _step_dark(self, edges):
            self.mtick += 1
            self.dist += 1.0
            held = edges["held"]

            if self.iframes > 0:
                self.iframes -= 1
            if self.name_cd > 0:
                self.name_cd -= 1
            if self.sweep_cd > 0:
                self.sweep_cd -= 1

            # --- THE LAMP -------------------------------------------------
            if edges["x"] and self.sweep_t <= 0 and self.sweep_cd <= 0:
                self.sweep_t = MY_SWEEP_TICKS
                self.sweep_cd = MY_SWEEP_CD
                self.play("scan", 0.85)
                self.flash = 0.12

            if self.sweep_t > 0:
                self.sweep_t -= 1
                self.lamp_r = MY_SWEEP_R
                self._collect(MY_SWEEP_R)
                if self.sweep_t <= 0:
                    # ...and then your eyes are gone.
                    self.lamp_r = MY_LAMP_MIN
                    self.play("cancel", 0.4)
            else:
                # DERIVED, not picked: the lamp comes back over exactly
                # MY_SWEEP_BLIND ticks, so changing the blind window changes
                # the recovery and the two can never disagree.
                self.lamp_r = min(MY_LAMP_R, self.lamp_r
                                + (MY_LAMP_R - MY_LAMP_MIN) / float(MY_SWEEP_BLIND))
                self._collect(self.lamp_r)

            # --- ACCUSE ---------------------------------------------------
            if edges["z"] and not self.naming and self.name_cd <= 0:
                self.naming = True
                self.name_t = 0
                self.play("wind", 0.5)
            if self.naming:
                if not held["z"]:
                    self.naming = False
                    self.name_t = 0
                    self.name_cd = 14
                else:
                    self.name_t += 1
                    if self.name_t >= MY_NAME_TICKS:
                        self.naming = False
                        self.name_t = 0
                        self.name_cd = MY_NAME_CD
                        self._resolve_accuse()

            # --- moving ----------------------------------------------------
            mx = (1 if held["right"] else 0) - (1 if held["left"] else 0)
            my = (1 if held["down"] else 0) - (1 if held["up"] else 0)
            if mx or my:
                # Naming roots you. It does not freeze you -- a fight that
                # takes the controls away is a fight that is doing something
                # to you rather than with you -- but you creep.
                spd = MY_NAME_DRIFT if self.naming else MY_SPEED
                n = math.hypot(mx, my) or 1.0
                self.px += (mx / n) * spd
                self.py += (my / n) * spd
                self.px, self.py = my_arena_clamp(self.px, self.py,
                                                MY_PLAYER_R)
                self.trail.append((self.px, self.py))
                if len(self.trail) > 26:
                    self.trail.pop(0)

            # --- the population, and what it leaves --------------------------
            self._step_bodies()
            self._rebuild_live()
            self._step_contact()
            self._step_dread()
            self._step_reopen()

            # Housekeeping only: an uncollected trace nobody ever found stops
            # existing eventually. A COLLECTED one never does.
            if self.tick % 60 == 0:
                cutoff = self.tick - MY_TRACE_LIFE
                self.traces = [tr for tr in self.traces
                            if tr["got"] or tr["t0"] > cutoff]

            if self.solve >= MY_SOLVE_MAX:
                self._begin_leave(True)

        def _step_contact(self):
            """WALKING INTO SOMETHING IN THE DARK is the most reliable
            evidence in the act and the most expensive way to get it.

            A contact leaves a mark with no RANGE on it at all -- a body was
            HERE -- widened only by MY_BREAK_REACH, which is far tighter than
            any ring and is the one statement in the act worth something on
            its own. A bystander only startles and goes. The subject takes
            MY_HIT_HP and then leaves too.
            """
            for b in self.bodies:
                if b["touch_cd"] > 0 or b["break"] > 0:
                    continue
                d = math.hypot(b["x"] - self.px, b["y"] - self.py)
                if d > MY_TOUCH_R + MY_PLAYER_R:
                    continue
                b["touch_cd"] = 44
                dx, dy = b["x"] - self.px, b["y"] - self.py
                n = math.hypot(dx, dy) or 1.0
                # ORDER MATTERS HERE AND IT IS NOT COSMETIC. Both branches
                # below break the body away and withdraw everything it had
                # left, so the contact mark has to be made AFTER that or
                # _void_body deletes the very evidence the contact was for --
                # which is what it did, silently, and which made the whole
                # trade this method documents a lie. It is stamped with
                # MY_BREAK_REACH of slack so it stays a sound statement
                # across the break-away it is about to cause.
                touched_x, touched_y = b["x"], b["y"]
                if b["subject"]:
                    if self.iframes <= 0:
                        self.iframes = MY_IFRAMES
                        self.hurt(MY_HIT_HP, self.px, self.py - 40)
                        self.play("struck", 0.7)
                        self.px -= (dx / n) * 26.0
                        self.py -= (dy / n) * 26.0
                        self.px, self.py = my_arena_clamp(self.px, self.py,
                                                        MY_PLAYER_R)
                        self.float_text(self.px, self.py - 66, "CONTACT",
                                        MY_RED)
                        # AND THEN IT LEAVES. It is not attacking you, it is
                        # passing through you, and having been touched it
                        # breaks away exactly as it does off a landed
                        # accusation. Two reasons, and the second is the one
                        # that matters:
                        #   * the fiction. It has no interest in killing the
                        #     party member and never did.
                        #   * measured. Without this a player who stops
                        #     moving is farmed -- it simply sits on them
                        #     through the i-frames and takes the bar down in
                        #     lumps, which turned every long run into a death
                        #     rather than a long run (the loop bot went 3/4
                        #     to 1/4 the moment runs got longer). A contact
                        #     is now a TRADE: the worst damage in the act,
                        #     for the single best piece of evidence in it,
                        #     and then room to use it.
                        ang = math.atan2(dy, dx)
                        b["break"] = 34
                        b["bvx"] = math.cos(ang) * MY_BREAK_SPEED * 0.62
                        b["bvy"] = math.sin(ang) * MY_BREAK_SPEED * 0.62
                        self._void_body(b["id"])
                        self._drop_trace(touched_x, touched_y, b["id"],
                                        exact=True, collected=True,
                                        slack=MY_BREAK_REACH)
                else:
                    # It startles and goes. Nothing is taken from you and you
                    # have just learned something exact.
                    b["break"] = 22
                    b["bvx"] = (dx / n) * 5.4
                    b["bvy"] = (dy / n) * 5.4
                    self._void_body(b["id"])
                    self._drop_trace(touched_x, touched_y, b["id"],
                                    exact=True, collected=True,
                                    slack=MY_BREAK_REACH)
                    self.play("graze", 0.8)
                    self.float_text(b["x"], b["y"] - 30, "CONTACT", MY_CHALK)

        def _step_dread(self):
            sub = self.subject()
            target = 0.0
            if sub is not None and sub["break"] <= 0:
                d = math.hypot(sub["x"] - self.px, sub["y"] - self.py)
                target = inv_clamp(
                    (MY_DREAD_NEAR - d) / (MY_DREAD_NEAR - MY_DREAD_FULL),
                    0.0, 1.0)
            # 0.05, so a full swing takes 20 ticks rather than 29. It has
            # to LAG -- an instantaneous readout would be a distance meter
            # with a number filed off, and the whole reason this channel can
            # coexist with the belief field is that it is slow and analogue --
            # but it also has to be able to answer the question the player
            # actually asks it, which is "is it here, now", asked while
            # standing on a knot they have just walked to.
            self.dread_v = inv_approach(self.dread_v, target, 0.05)
            inv_heart_level(0.14 + 0.62 * self.dread_v)

        def _step_reopen(self):
            every = int(inv_lerp(MY_REOPEN_EVERY, MY_REOPEN_EVERY_HOT,
                                self.heat()))
            self.reopen_t -= 1
            if self.reopen_t <= MY_REOPEN_WARN:
                self.reopen_warn = inv_clamp(
                    1.0 - self.reopen_t / float(MY_REOPEN_WARN), 0.0, 1.0)
                if self.reopen_t == MY_REOPEN_WARN:
                    self.play("wind2", 0.7)
            else:
                self.reopen_warn = 0.0
            if self.reopen_t <= 0:
                self.reopen_t = every
                self.reopen_warn = 0.0
                live = len(self.live)
                self._void_live()
                self.play("break", 0.7)
                self.flash = 0.34
                self.shake = 0.55
                if live:
                    self.float_text(self.px, self.py - 80, "REOPENING",
                                    MY_RED, True)

        def _resolve_accuse(self):
            """Act one's verb, and it resolves against what is actually there.

            THERE IS NO WASTED ACCUSATION AND THERE IS NO FINAL ONE. Every
            outcome produces a true, permanent thing, and none of them close
            the case.
            """
            best, bd = None, 1e9
            for b in self.bodies:
                d = math.hypot(b["x"] - self.px, b["y"] - self.py)
                if d < bd:
                    bd, best = d, b

            if best is not None and bd <= MY_NAME_R:
                if best["subject"]:
                    self.solve = min(MY_SOLVE_MAX, self.solve + MY_SOLVE_GAIN)
                    if self.hp < MY_HP2_MAX:
                        healed = min(MY_SOLVE_HEAL, MY_HP2_MAX - self.hp)
                        self.hp += healed
                        self.float_text(self.px + 54, self.py - 48,
                                        "+%d" % healed, MY_PALE)
                    self.play("crit", 0.95)
                    self.flash = 0.60
                    self.shake = 0.85
                    self.name_flash = 1.0
                    self.float_text(self.px, self.py - 72,
                                    "+%d" % int(MY_SOLVE_GAIN), MY_GOLD, True)
                    # It breaks away. One impulse, under friction.
                    ang = self.rng.uniform(0.0, 6.283)
                    best["break"] = 46
                    best["bvx"] = math.cos(ang) * MY_BREAK_SPEED
                    best["bvy"] = math.sin(ang) * MY_BREAK_SPEED
                    self._void_body(best["id"])
                    # And the case reopens -- the same rule act one taught,
                    # and the reason a landed hit does not simplify the room.
                    self._void_live()
                    # PAST MY_SOLVE_HARD, CLOSING IN WIDENS THE FIELD.
                    if (self.solve_frac() >= MY_SOLVE_HARD
                            and len(self.bodies) + len(self.replace_q)
                            < MY_BODY_HARDCAP):
                        self.replace_q.append(90)
                    self.name_cd = MY_NAME_CD
                else:
                    # RULED OUT. Permanent, useful, and not the win.
                    self.name_cd = MY_NAME_CD_MISS
                    self.bodies = [b for b in self.bodies
                                if b["id"] != best["id"]]
                    self.ruleouts.append({"x": best["x"], "y": best["y"],
                                        "t": self.tick})
                    # What it left behind stops bearing on the question, which
                    # is what ruling somebody out is FOR.
                    for tr in self.traces:
                        if tr["body"] == best["id"]:
                            tr["void"] = True
                    self.replace_q.append(MY_REPLACE_DELAY)
                    self.play("refuse", 0.85)
                    self.flash = 0.24
                    self.float_text(self.px, self.py - 72, "RULED OUT",
                                    MY_CHALK, True)
            else:
                # INCONCLUSIVE -- and a permanent exclusion goes down where you
                # stood. A wrong answer in this fight is still evidence.
                self.name_cd = MY_NAME_CD_MISS
                self.exclusions.append({"x": self.px, "y": self.py,
                                        "r": MY_NAME_R, "t": self.tick})
                self.play("miss", 0.7)
                self.float_text(self.px, self.py - 72, "INCONCLUSIVE",
                                MY_DIM)

        # =====================================================================
        # DEPARTURE
        # =====================================================================

        def _begin_leave(self, won):
            self.mode = "leave_w" if won else "leave_l"
            self.mtick = 0
            self.naming = False
            self.name_t = 0
            self.shake = 0.0
            self.reopen_warn = 0.0
            self.hud_fade = 1.0
            self.end_close = 0.0
            self.lattice_off = 0.0
            self.end_show = 0.0
            self.dread_v = 0.0
            inv_music_stop(3.0 if won else 1.8)
            # No sting either way. A victory chime would be the funniest thing
            # in the encounter.

        def _step_leave(self):
            """Neither ending is a spectacle and neither one settles anything.

            WON -- the belief field collapses to a point, and for the first
            and only time in the encounter the thing is fully lit and standing
            exactly where the evidence said it was. Then it opens: the
            apertures grow until there is nothing between them, and the hole
            takes what is left. And then the lamp goes out, and what is left
            on screen for a long moment is the SURVEY LATTICE -- every true
            thing you established, hanging in an empty room, none of it
            meeting anything.

            LOST -- you are not killed. THE LAMP GOES OUT. It dims, the radius
            closes, and the last thing inside it is a body standing near you.
            Then the lattice goes too, one mark at a time, in the order you
            found them, until the room is black -- and then nothing happens
            for a long time.
            """
            self.mtick += 1
            t = self.mtick
            won = (self.mode == "leave_w")

            if won:
                # 0-70     everything stops and the field collapses on it
                # 70-170   it is lit, all of it, once
                # 170-260  it opens, and the hole takes the rest
                # 260-400  the lattice alone, in an empty room
                if t == 1:
                    self.play("phase", 0.7)
                    inv_heart_stop(1.4)
                if t < 70:
                    u = t / 70.0
                    self.hud_fade = max(0.0, 1.0 - u)
                    self.lamp_r = inv_lerp(self.lamp_r, 210.0, 0.04)
                    sub = self.subject()
                    if sub is not None:
                        # It comes to rest exactly where the last of the
                        # evidence said it would be.
                        self.px = inv_lerp(self.px, sub["x"], 0.03)
                        self.py = inv_lerp(self.py, sub["y"], 0.03)
                elif t < 170:
                    u = inv_smooth((t - 70) / 100.0)
                    self.end_show = u
                    self.body_lit = u
                    self.body_ap = inv_lerp(0.34, 0.20, u)
                    self.body_diss = 0.0
                    if t == 74:
                        self.play("scan", 0.9)
                        self.flash = 0.30
                elif t < 260:
                    u = inv_smooth((t - 170) / 90.0)
                    self.end_show = 1.0
                    self.body_diss = u
                    self.body_ap = inv_lerp(0.20, 0.90, u)
                    self.hole[0], self.hole[1] = 640.0, 320.0
                    self.hole[3] = 1.0 - abs(u - 0.5) * 2.0
                    self.hole[2] = inv_lerp(40.0, 230.0, u)
                    if t == 172:
                        self.play("break", 0.55)
                else:
                    self.hole[3] = 0.0
                    self.end_show = 0.0
                    # THE LATTICE ALONE. Held a beat and a half longer than is
                    # comfortable, which is the house rule for these endings.
                    self.lamp_s = max(0.0, self.lamp_s - 0.020)
                    if t > 340:
                        self.dark = inv_clamp(self.dark + 0.013, 0.0, 1.0)
                if t > 430:
                    self.result = "victory"

            else:
                # 0-40     everything stops
                # 40-260   the lamp closes, and the last thing in it is near
                # 260-400  the lattice goes out, in the order you found it
                # 400+     black, held far longer than is comfortable
                if t == 1:
                    self.play("cut", 0.6)
                if 40 <= t < 260:
                    u = (t - 40) / 220.0
                    self.end_close = u
                    self.lamp_r = inv_lerp(MY_LAMP_R, 14.0, inv_smooth(u))
                    self.hud_fade = max(0.0, 1.0 - u * 1.5)
                    # The subject closes the last of the distance at walking
                    # pace, and then simply stands there.
                    sub = self.subject()
                    if sub is not None and u < 0.72:
                        dx, dy = self.px - sub["x"], self.py - sub["y"]
                        n = math.hypot(dx, dy) or 1.0
                        if n > 46.0:
                            sub["x"] += (dx / n) * 0.9
                            sub["y"] += (dy / n) * 0.9
                    if t == 250:
                        inv_heart_stop(0.5)
                if t == 260:
                    self.play("slam", 0.45)
                if t >= 260:
                    self.end_close = 1.0
                    self.lamp_s = max(0.0, self.lamp_s - 0.035)
                    # ...and everything you established goes out with it, one
                    # mark at a time, in the order you found them.
                    self.lattice_off = inv_clamp((t - 260) / 140.0, 0.0, 1.0)
                if t >= 400:
                    self.dark = inv_clamp(self.dark + 0.011, 0.0, 1.0)
                if t > 500:
                    self.result = "defeat"


# --- THE STAGE ---------------------------------------------------------------
init python:
    class MYStage(renpy.Displayable):
        """One CDD. Steps MYGame at a fixed 60Hz inside render() and paints the
        whole encounter from cached-texture blits and one canvas."""

        _tf_cache = {}
        _misc_cache = {}
        _text_cache = {}

        PANEL_CMD = (40, 548, 470, 148)
        PANEL_HUD = (770, 548, 470, 148)

        # Canvas colours. The room has three: what you proved, what you are
        # working out, and the one thing that can hurt you.
        C_CHALK = (154, 166, 180)
        C_GOLD = (230, 184, 85)
        C_RED = (194, 42, 60)
        C_PALE = (220, 228, 238)
        C_DIM = (125, 135, 148)
        C_LAMP = (188, 210, 228)

        def __init__(self, game, **kwargs):
            super(MYStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0

        def _misc(self, key, builder):
            d = MYStage._misc_cache.get(key)
            if d is None:
                if len(MYStage._misc_cache) > 600:
                    MYStage._misc_cache.clear()
                d = builder()
                MYStage._misc_cache[key] = d
            return d

        def _text(self, text, size, color, font=INV_FONT, bold=False,
                outline=None):
            key = (text, size, color, font, bold, outline)
            t = MYStage._text_cache.get(key)
            if t is None:
                if len(MYStage._text_cache) > 240:
                    MYStage._text_cache.clear()
                outl = [(2, outline, 0, 0)] if outline else []
                t = Text(text, size=size, color=color, bold=bold, font=font,
                        outlines=outl, substitute=False)
                MYStage._text_cache[key] = t
            return t

        def _body_plain(self, zoom, alpha=1.0):
            ab = int(inv_clamp(alpha, 0.0, 1.0) * 6)
            key = ("plain", round(zoom, 3), ab)
            tf = MYStage._tf_cache.get(key)
            if tf is None:
                kw = dict(zoom=zoom, subpixel=True)
                if ab < 6:
                    kw["alpha"] = ab / 6.0
                tf = Transform(MY_SPRITE, **kw)
                MYStage._tf_cache[key] = tf
            return tf

        def event(self, ev, x, y, st):
            self.game.keys.handle_event(ev)
            return None

        # ----- render ------------------------------------------------------------

        def render(self, width, height, st, at):
            g = self.game

            if self.last_st is None:
                self.last_st = st
            dt = st - self.last_st
            self.last_st = st
            dt = 0.0 if dt < 0.0 else (0.25 if dt > 0.25 else dt)

            if g.paused:
                self.acc = 0.0
            else:
                self.acc += dt
                steps = 0
                while self.acc >= INV_TICK and steps < INV_MAX_CATCHUP:
                    g.step()
                    self.acc -= INV_TICK
                    steps += 1
                if steps >= INV_MAX_CATCHUP:
                    self.acc = 0.0

            rv = renpy.Render(1280, 720)
            frame_tex = {}

            def tex(key, disp, w=1280, h=720):
                entry = frame_tex.get(key)
                if entry is None:
                    r = renpy.render(disp, w, h, st, at)
                    rv.depends_on(r)
                    entry = (r, r.get_size())
                    frame_tex[key] = entry
                return entry

            def rect(color, w, h):
                w = max(1, int(w))
                h = max(1, int(h))
                key = ("rect", color, w, h)
                entry = frame_tex.get(key)
                if entry is None:
                    solid = self._misc(("solid", color), lambda c=color: Solid(c))
                    r = renpy.render(solid, w, h, st, at)
                    rv.depends_on(r)
                    entry = r
                    frame_tex[key] = entry
                return entry

            def qa(a):
                return "%02x" % (int(inv_clamp(a, 0.0, 1.0) * 7.0) * 34 + 6)

            def blit_text(disp_text, size, color, x, y, font=INV_FONT,
                        bold=False, anchor=(0.0, 0.0), w=1200, h=200, key=None,
                        outline=None):
                t = self._text(disp_text, size, color, font=font, bold=bold,
                            outline=outline)
                r, (tw, th) = tex(key or ("t", disp_text, size, color, font,
                                        bold, w, outline), t, w, h)
                rv.blit(r, (int(x - tw * anchor[0]), int(y - th * anchor[1])))
                return (tw, th)

            # The survey layer. Matsu'Py fixes a layer's z-order the moment it is
            # first blitted into rv, and everything drawn on the dark -- the
            # lattice, the sparks, the rings -- belongs UNDER the body and
            # under the heart. So the canvas claims its slot before either of
            # those is drawn, and the room's own light (which is the shader,
            # already blitted) stays under all of it.
            canvas_layer = [None]

            def canvas():
                if canvas_layer[0] is None:
                    layer = renpy.Render(1280, 720)
                    canvas_layer[0] = layer.canvas()
                    rv.blit(layer, (0, 0))
                return canvas_layer[0]

            sblit = rv.subpixel_blit

            shake_x = shake_y = 0
            if g.shake > 0.01:
                amp = 12.0 * g.shake
                shake_x = int(math.sin(g.tick * 1.9) * amp)
                shake_y = int(math.cos(g.tick * 2.7) * amp * 0.6)

            in_dark = (g.open > 0.5)

            # --- 1. the room ------------------------------------------------
            self._render_plain(g, rv, rect, st, at)

            # --- 2. the encounter -------------------------------------------
            if in_dark:
                self._render_dark(g, rv, tex, rect, qa, blit_text, canvas,
                                sblit, shake_x, shake_y, st, at)
            else:
                self._render_room(g, rv, tex, rect, qa, blit_text, sblit,
                                shake_x, shake_y, st, at)

            # --- 3. numbers ---------------------------------------------------
            for f in g.floats:
                a = inv_clamp(f["life"] / 26.0, 0.0, 1.0)
                blit_text(f["text"], 28 if f["big"] else 20,
                        f["color"] + qa(a), int(f["x"]) + shake_x,
                        int(f["y"]) + shake_y, bold=f["big"],
                        anchor=(0.5, 0.5), w=380, h=60, outline=MY_BLACK)

            if g.paused:
                rv.blit(rect("#04050ad2", 1280, 720), (0, 0))
                blit_text("PAUSED", 40, MY_PALE, 640, 316, bold=True,
                        anchor=(0.5, 0.5), w=600, h=70)
                blit_text("ESC  RESUME        Q  QUIT", 16, MY_DIM,
                        640, 372, anchor=(0.5, 0.5), w=800, h=44)

            # THE DRAW RATE IS THE TICK RATE. Every pixel above is a pure
            # function of the simulation state: nothing in this method reads
            # self.acc and nothing interpolates between ticks, so between two
            # 1/60s ticks this stage paints a byte-identical picture. Asking
            # for the next frame IMMEDIATELY meant a 165Hz or 240Hz panel ran
            # the entire draw -- every python-side blit, every full-screen
            # shader pass, and the mark-and-sweep over every Render they make
            # -- two to four times per tick and threw the extra frames away.
            #
            # Handing redraw() the time remaining until the next tick lets the
            # engine's scheduler wake us exactly when there is something new to
            # draw. It wakes at the first vblank at or after the delay, so a
            # 60Hz display is unaffected and only a high-refresh one stops
            # paying. Input is unchanged: the key latch is polled inside
            # step(), on the tick. Same governor as kototouhou.rpy.
            if g.result is None and not g.paused:
                renpy.redraw(self, max(0.0, INV_TICK - self.acc))
            return rv

        # ----- the room --------------------------------------------------------

        def _claims(self, g):
            """The live constraint set, packed for the shader as
            (x, y, D, tol). A tol of 0 is an unused slot."""
            out = []
            if g.open > 0.5:
                for tol, tr in g.live:
                    out.append((float(tr["x"]), float(tr["y"]),
                                float(tr.get("d", 0.0)), float(tol)))
            while len(out) < MY_LIVE_MAX:
                out.append((0.0, 0.0, 0.0, 0.0))
            return out

        def _render_plain(self, g, rv, rect, st, at):
            global MY_LAMP_OK
            if MY_LAMP_OK:
                try:
                    cl = self._claims(g)
                    quad = Transform(
                        MY_SOUP_IMG, xysize=(1280, 720), mesh=True,
                        shader="inv.lamp",
                        u_my_res=(1280.0, 720.0),
                        u_my_time=g.clock,
                        u_my_open=g.open,
                        u_my_dark=g.dark,
                        u_my_flash=g.flash,
                        u_my_dread=g.dread(),
                        u_my_reopen=g.reopen_warn,
                        u_my_heat=g.heat(),
                        u_my_nlive=float(g.live_weight()),
                        u_my_maxr=float(g.trace_maxr()),
                        u_my_hole=(float(g.hole[0]), float(g.hole[1]),
                                float(g.hole[2]), float(g.hole[3])),
                        u_my_lamp=(float(g.px), float(g.py),
                                float(g.lamp_r), float(g.lamp_s)),
                        u_my_c0=cl[0], u_my_c1=cl[1], u_my_c2=cl[2],
                        u_my_c3=cl[3], u_my_c4=cl[4], u_my_c5=cl[5],
                        u_my_c6=cl[6], u_my_c7=cl[7])
                    qr = renpy.render(quad, 1280, 720, st, at)
                    rv.depends_on(qr)
                    rv.blit(qr, (0, 0))
                    return
                except Exception as e:
                    MY_LAMP_OK = False
                    try:
                        renpy.log("INV FX: lamp render failed: %r" % e)
                    except Exception:
                        pass
            rv.blit(rect(MY_BLACK, 1280, 720), (0, 0))

        # ----- the body --------------------------------------------------------

        def _draw_body(self, g, rv, tex, sblit, cx, cy, zoom, sx, sy, st, at,
                    shear=1.0, ap=0.35, lit=0.2, band=0.4, diss=0.0,
                    stretch=(1.0, 1.0), hurt=0.0, alpha=1.0):
            # The apertures overshoot the silhouette, and the strata slide past
            # it, so the plate needs a wide margin or both get clipped at the
            # edge of the sprite.
            plate_zoom = min(zoom, MY_PLATE_MAX_ZOOM)
            extra = zoom / plate_zoom
            # A WIDE MARGIN, because this body does not stay inside its
            # own silhouette: the strata slide sideways and the apertures
            # overshoot it. 1.9 x 1.5 at MY_PLATE_MAX_ZOOM is 1751 x 2073,
            # comfortably inside the 4096 texture cap.
            plate, W, H = inv_body_plate(MY_SPRITE, MY_SPRITE_W, MY_SPRITE_H,
                                        plate_zoom, pad_x=1.90, pad_y=1.50)
            # The figure is off-centre in its own canvas; put the FIGURE where
            # the caller asked, not the canvas.
            cx = cx + MY_FIG_DX * zoom
            cy = cy + MY_FIG_DY * zoom

            if MY_LACUNA_OK:
                try:
                    body = Transform(
                        plate, mesh=True, shader="inv.lacuna",
                        u_lac_res=(float(W), float(H)),
                        u_lac_t=g.clock,
                        u_lac_shear=float(shear),
                        u_lac_ap=float(ap),
                        u_lac_band=float(band),
                        u_lac_lit=float(lit),
                        u_lac_stretch=(float(stretch[0]), float(stretch[1])),
                        u_lac_pivot=0.90,
                        u_lac_hurt=float(hurt),
                        u_lac_diss=float(diss))
                    if extra > 1.01:
                        body = Transform(body, zoom=extra, subpixel=True)
                    if alpha < 0.99:
                        body = Transform(body, alpha=alpha)
                    r = renpy.render(body, int(W * extra) + 8,
                                    int(H * extra) + 8, st, at)
                    rv.depends_on(r)
                    w, h = r.get_size()
                    sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))
                    return
                except Exception:
                    pass

            r, (w, h) = tex(("plainbody", round(zoom, 3), alpha),
                            self._body_plain(zoom, alpha=alpha), 900, 1400)
            sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))

        def _draw_heart(self, g, rv, tex, sblit, cx, cy, sx, sy, st, at,
                    alpha=1.0):
            """You. The same SOUL heart as every other corruptive state -- and
            in here it is the only object in the room you can always find,
            which is why its warp is held where it is."""
            plate, W, H = inv_body_plate(INV_HEART, INV_HEART_W, INV_HEART_H,
                                        MY_HEART_ZOOM, pad_x=2.2, pad_y=2.2,
                                        nearest=True)
            squeeze = 1.0 - 0.20 * g.beat_pulse
            if INV_FLESH_OK:
                try:
                    d = inv_flesh(plate, W, H, g.clock * 2.6,
                                warp=MY_HEART_WARP, split=0.9,
                                stretch=(1.0 / max(0.5, squeeze), squeeze),
                                pivot=0.5, hurt=0.0, diss=0.05)
                    if alpha < 0.99:
                        d = Transform(d, alpha=alpha)
                    r = renpy.render(d, W, H, st, at)
                    rv.depends_on(r)
                    w, h = r.get_size()
                    sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))
                    return
                except Exception:
                    pass
            heart = self._misc(("heartplain",),
                            lambda: Transform(INV_HEART, zoom=MY_HEART_ZOOM,
                                            nearest=True, subpixel=True))
            r, (w, h) = tex(("heartplain",), heart, 160, 160)
            sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))

        # ----- ACT ONE ---------------------------------------------------------

        def _render_room(self, g, rv, tex, rect, qa, blit_text, sblit,
                        sx, sy, st, at):
            arriving = (g.mode == "arrive")
            doubt = g.doubt_frac()

            # It stands where it is and the strata do the moving. There is no
            # bob and no breath: everything about this figure that is in motion
            # is INSIDE it.
            cy = 330 + math.sin(g.clock * 0.31) * 4.0

            self._draw_body(g, rv, tex, sblit, 640, cy, MY_ZOOM_ACT1, sx, sy,
                            st, at,
                            shear=0.70 + 0.85 * doubt + 1.3 * g.hit_flash,
                            ap=g.body_ap + 0.22 * doubt,
                            lit=g.body_lit if arriving else (0.16 + 0.10 * doubt),
                            band=g.body_band,
                            diss=g.body_diss,
                            hurt=0.30 * g.hit_flash)

            if arriving:
                return

            # --- the only chrome act one gets --------------------------------
            blit_text("MYSTERY", 15, MY_PALE, 380, 24, bold=True, w=320,
                    h=30, outline=MY_BLACK)

            # ITS ACCOUNT OF ITSELF, and it is a plain bar: unlike Nonfiction
            # there is no escrow here and nothing you take off it comes back
            # except by its own hand.
            bar_w = 460
            rv.blit(rect("#04050ab4", bar_w + 4, 12), (380 - 2, 48))
            rv.blit(rect("#141820", bar_w, 8), (380, 50))
            left = int(bar_w * inv_clamp(
                (MY_CASE_MAX - g.case_shown) / float(MY_CASE_MAX), 0.0, 1.0))
            if left > 0:
                rv.blit(rect(MY_PALE, left, 8), (380, 50))

            # DOUBT. A second, thinner rule under the first -- and it is not a
            # danger meter, it is a CERTAINTY meter, which is why it is the
            # thing that fires the capstone.
            rv.blit(rect("#141820", bar_w, 4), (380, 64))
            dv = int(bar_w * doubt)
            if dv > 0:
                rv.blit(rect(MY_WARN if doubt < 0.85 else MY_RED, dv, 4),
                        (380, 64))
            blit_text("DOUBT", 11, MY_DIM, 380, 72, w=200, h=22,
                    outline=MY_BLACK)

            # THE FIELD. The number the whole act is about, so it is drawn
            # big, it rolls rather than changing, and it LIVES IN THE RIGHT
            # MARGIN -- clear of the figure's
            # footprint (x 507-773 at this zoom). It is the number the act is
            # about, so it gets its own space and is never drawn over the
            # thing it is about.
            fshown = g.field_shown
            blit_text("FIELD", 12, MY_DIM, 1240, 22, bold=True, w=160, h=24,
                    anchor=(1.0, 0.0), outline=MY_BLACK)
            fcol = MY_GOLD if g.field <= 3 else MY_PALE
            blit_text("%d" % int(round(fshown)), 44, fcol, 1240, 36,
                    bold=True, anchor=(1.0, 0.0), w=210, h=78,
                    outline=MY_BLACK)
            # The pips under it are the same integer said a second way, so the
            # relationship between "the field" and "what ACCUSE is worth" can
            # be read without arithmetic.
            for i in range(MY_FIELD_MAX):
                on = (i < g.field)
                col = (fcol if on else MY_FAINT)
                rv.blit(rect(col + qa(1.0 if on else 0.45), 5, 5),
                        (1084 + i * 13, 100))

            slide = int(g.panel_slide * 210)
            if g.panel_slide < 1.0:
                self._panel(rv, rect, MYStage.PANEL_CMD, sx, sy + slide)
                self._panel(rv, rect, MYStage.PANEL_HUD, sx, sy + slide)
                self._panel_contents(g, rv, tex, rect, qa, blit_text, sx,
                                    sy + slide)

        def _panel(self, rv, rect, box, sx, sy):
            x, y, w, h = box
            x += sx
            y += sy
            rv.blit(rect(MY_CHALK, w + 6, h + 6), (x - 3, y - 3))
            rv.blit(rect(MY_BLACK, w + 2, h + 2), (x - 1, y - 1))
            rv.blit(rect(MY_WIN, w, h), (x, y))
            # Corner ticks rather than rules: this is a case file, not a page.
            for cxo, cyo in ((10, 10), (w - 34, 10), (10, h - 12),
                            (w - 34, h - 12)):
                rv.blit(rect(MY_CHALK + "40", 24, 1), (x + cxo, y + cyo))

        def _panel_contents(self, g, rv, tex, rect, qa, blit_text, sx, sy):
            cx, cy, cw, ch = MYStage.PANEL_CMD
            cx += sx
            cy += sy

            if g.mode == "menu":
                for i, row in enumerate(MY_CMDS):
                    live = (i == g.cursor)
                    ry = cy + 16 + i * 30
                    if live:
                        rv.blit(rect(MY_PALE + qa(0.12), cw - 28, 26),
                                (cx + 14, ry - 3))
                        rv.blit(rect(MY_PALE, 9, 9), (cx + 22, ry + 6))
                    dead = (row[0] == "narrow"
                            and (g.field <= MY_FIELD_MIN
                                or g.leads < MY_NARROW_COST))
                    col = (MY_FAINT if dead
                        else (MY_PALE if live else MY_DIM))
                    blit_text(row[1], 20, col, cx + 42, ry, bold=live,
                            w=260, h=30)
                    # THE ONE READOUT THAT TEACHES THE ACT. ACCUSE prints what
                    # it is worth RIGHT NOW, so the player watches that number
                    # climb every time they narrow and works out the rule for
                    # themselves. It is a number, not a sentence, and it is
                    # the reason rule 1 costs this fight nothing.
                    if row[0] == "accuse":
                        blit_text("%d" % my_accuse_damage(g.field), 17,
                                MY_GOLD if g.field <= 4 else col,
                                cx + cw - 22, ry + 2, anchor=(1.0, 0.0),
                                bold=True, w=120, h=26)
                    elif row[0] == "narrow":
                        blit_text("%d" % MY_NARROW_COST, 14, col,
                                cx + cw - 22, ry + 4, anchor=(1.0, 0.0),
                                w=120, h=26)
                blit_text("Z  OK      ESC  PAUSE", 12, MY_FAINT,
                        cx + cw - 16, cy + ch - 22, anchor=(1.0, 0.0),
                        w=420, h=24)

            elif g.mode == "beat":
                blit_text(g.beat_label, 22, MY_PALE, cx + 20, cy + 30,
                        bold=True, w=cw - 40, h=40)
                if g.beat_value:
                    blit_text(g.beat_value, 24, MY_WARN, cx + 20, cy + 64,
                            bold=True, w=cw - 40, h=44)
                if g.mtick > 12 and (g.tick // 20) % 2 == 0:
                    rv.blit(rect(MY_PALE, 14, 4), (cx + cw - 36, cy + ch - 26))

            hx, hy, hw, hh = MYStage.PANEL_HUD
            hx += sx
            hy += sy
            blit_text(inv_player_name(), 19, MY_PALE, hx + 20, hy + 12,
                    bold=True, w=hw - 40, h=32)
            self._odometer(g, rv, rect, qa, blit_text, "HP", g.hp_shown,
                        g.hp, hx + 20, hy + 44, MY_PALE)
            self._odometer(g, rv, rect, qa, blit_text, "LEADS", g.leads_shown,
                        g.leads, hx + 20, hy + 96, MY_DIM, small=True)

            if g.dn_pending:
                blit_text("DENOUEMENT", 13, MY_RED, hx + hw - 20, hy + 16,
                        anchor=(1.0, 0.0), w=260, h=26)
                blit_text("PENDING", 13, MY_WARN, hx + hw - 20, hy + 38,
                        anchor=(1.0, 0.0), w=260, h=26)
            if g.god:
                blit_text("GOD", 12, MY_WARN + "aa", hx + hw - 20,
                        hy + hh - 24, anchor=(1.0, 0.0), w=120, h=24)

        def _odometer(self, g, rv, rect, qa, blit_text, label, shown, real,
                    x, y, color, small=False):
            """An EarthBound counter: fixed-width cells, and the digits that
            are moving are drawn mid-roll rather than swapped."""
            size = 22 if small else 30
            cell_w = 22 if small else 28
            cell_h = 32 if small else 42
            blit_text(label, 14, color, x, y + (6 if small else 12), bold=True,
                    w=90, h=28)

            value = int(math.ceil(shown - 0.0001)) if shown > 0 else 0
            rolling = abs(shown - real) > 0.05
            digits = "%03d" % inv_clamp(value, 0, 999)
            frac = shown - math.floor(shown)
            base_x = x + (58 if small else 50)

            for i, ch in enumerate(digits):
                dx = base_x + i * cell_w
                rv.blit(rect("#08090ee0", cell_w - 4, cell_h), (dx, y))
                if rolling:
                    off = int(frac * cell_h * (1 if real < shown else -1))
                    nxt = str((int(ch) + (1 if real > shown else -1)) % 10)
                    blit_text(nxt, size, color + qa(0.45),
                            dx + (cell_w - 4) // 2,
                            y + off - (cell_h if real < shown else -cell_h) + 2,
                            anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)
                    blit_text(ch, size, color, dx + (cell_w - 4) // 2,
                            y + off + 2, anchor=(0.5, 0.0), w=cell_w,
                            h=cell_h, bold=True)
                else:
                    blit_text(ch, size, color, dx + (cell_w - 4) // 2, y + 2,
                            anchor=(0.5, 0.0), w=cell_w, h=cell_h, bold=True)

        # ----- ACT TWO: THE DARK ------------------------------------------------

        def _render_dark(self, g, rv, tex, rect, qa, blit_text, canvas,
                        sblit, sx, sy, st, at):
            cv = canvas()
            fade = g.hud_fade
            latt = 1.0 - g.lattice_off

            def ca(base, a):
                a = inv_clamp(a, 0.0, 1.0)
                if a <= 0.01:
                    return None
                return (base[0], base[1], base[2], int(a * 255))

            # --- the walls ---------------------------------------------------
            # You can feel a wall without having established it, so the
            # boundary is drawn -- barely, and dashed, and brighter the nearer
            # you are standing to it. It is the only thing in the room you get
            # for free.
            near_edge = 1.0 - inv_clamp(
                min(g.px - MY_AR_X, MY_AR_X + MY_AR_W - g.px,
                    g.py - MY_AR_Y, MY_AR_Y + MY_AR_H - g.py) / 180.0, 0.0, 1.0)
            wall_a = (0.10 + 0.34 * near_edge) * g.lamp_s
            wc = ca(MYStage.C_CHALK, wall_a)
            if wc is not None:
                for k in range(0, MY_AR_W, 26):
                    w = min(13, MY_AR_W - k)
                    cv.line(wc, (MY_AR_X + k + sx, MY_AR_Y + sy),
                            (MY_AR_X + k + w + sx, MY_AR_Y + sy), 1)
                    cv.line(wc, (MY_AR_X + k + sx, MY_AR_Y + MY_AR_H + sy),
                            (MY_AR_X + k + w + sx, MY_AR_Y + MY_AR_H + sy), 1)
                for k in range(0, MY_AR_H, 26):
                    h = min(13, MY_AR_H - k)
                    cv.line(wc, (MY_AR_X + sx, MY_AR_Y + k + sy),
                            (MY_AR_X + sx, MY_AR_Y + k + h + sy), 1)
                    cv.line(wc, (MY_AR_X + MY_AR_W + sx, MY_AR_Y + k + sy),
                            (MY_AR_X + MY_AR_W + sx, MY_AR_Y + k + h + sy), 1)

            # --- THE SURVEY LATTICE -------------------------------------------
            # Every true thing you have established, drawn permanently on the
            # dark: a mark where each trace was collected, a traverse joining
            # them in the order you found them, a ring where you looked and
            # found nothing, and a cross where you ruled somebody out. None of
            # it ever leaves the room. Most of it stopped being useful a long
            # time ago and every single line of it is still correct.
            got = [tr for tr in g.traces if tr["got"]]
            keep = int(len(got) * latt)
            got = got[:keep] if latt < 1.0 else got
            # A long run collects a lot of true things. Past MY_LATTICE_RINGS
            # the OLDEST of them keep their mark and lose their circle -- the
            # room stays legible, the lattice keeps growing, and the ones that
            # still have a ring on them are the ones near enough to now to be
            # worth looking at. Nothing is ever deleted.
            ring_from = max(0, len(got) - MY_LATTICE_RINGS)
            prev = None
            for gi, tr in enumerate(got):
                x, y = int(tr["x"]) + sx, int(tr["y"]) + sy
                live_now = (not tr["void"]
                            and tr.get("slack", 0.0)
                            + MY_TRACE_SPREAD * max(0, g.tick - tr["t0"])
                            <= g.trace_maxr())
                a = (0.55 if live_now else 0.16) * g.lamp_s
                col = ca(MYStage.C_PALE if live_now else MYStage.C_CHALK, a)
                if col is not None:
                    if tr["exact"]:
                        # A contact. The one statement in the act with no
                        # range on it at all, and it is drawn like it.
                        cv.line(col, (x - 7, y), (x + 7, y), 1)
                        cv.line(col, (x, y - 7), (x, y + 7), 1)
                        cv.circle(col, (x, y), 5, 1)
                    elif gi >= ring_from:
                        # THE RING IS THE STATEMENT. This is what fills the
                        # room up: every range you ever took, drawn where you
                        # took it, at the distance it recorded. By the end of
                        # a run the dark is a lattice of them, every circle
                        # correct, almost none of them any use.
                        cv.circle(col, (x, y), max(3, int(tr.get("d", 0.0))), 1)
                        cv.circle(col, (x, y), 3, 0)
                    else:
                        cv.circle(col, (x, y), 3, 0)
                tcol = ca(MYStage.C_CHALK, 0.11 * g.lamp_s)
                if prev is not None and tcol is not None:
                    cv.line(tcol, prev, (x, y), 1)
                prev = (x, y)

            for ex in g.exclusions[:max(0, int(len(g.exclusions) * latt))]:
                col = ca(MYStage.C_CHALK, 0.22 * g.lamp_s)
                if col is not None:
                    cv.circle(col, (int(ex["x"]) + sx, int(ex["y"]) + sy),
                            int(ex["r"]), 1)
            for ro in g.ruleouts[:max(0, int(len(g.ruleouts) * latt))]:
                col = ca(MYStage.C_CHALK, 0.44 * g.lamp_s)
                if col is not None:
                    x, y = int(ro["x"]) + sx, int(ro["y"]) + sy
                    cv.line(col, (x - 15, y - 15), (x + 15, y + 15), 2)
                    cv.line(col, (x - 15, y + 15), (x + 15, y - 15), 2)
                    cv.circle(col, (x, y), 22, 1)

            # --- THE SPARKS ---------------------------------------------------
            # A fresh trace is faintly visible from anywhere in the room, and
            # that is what makes the dark readable: a spark is something that
            # moved out there just now, and there is a window on going to get
            # it. After MY_TRACE_GLIMMER ticks it goes dark and only light
            # will find it again.
            if g.mode == "dark":
                for tr in g.traces:
                    if tr["got"] or tr["void"]:
                        continue
                    age = g.tick - tr["t0"]
                    if age > MY_TRACE_GLIMMER:
                        continue
                    u = age / float(MY_TRACE_GLIMMER)
                    a = (1.0 - u) * (1.0 - u) * 0.85
                    x, y = int(tr["x"]) + sx, int(tr["y"]) + sy
                    col = ca(MYStage.C_LAMP, a)
                    if col is not None:
                        cv.circle(col, (x, y), 2, 0)
                    if age < 26:
                        ring = ca(MYStage.C_LAMP, (1.0 - age / 26.0) * 0.45)
                        if ring is not None:
                            cv.circle(ring, (x, y), int(4 + age * 0.8), 1)

            # --- THE ACCUSATION ------------------------------------------------
            px, py = int(g.px) + sx, int(g.py) + sy
            if g.naming:
                # The reach of the accusation, so "is it in range" is never a
                # guess -- and a ring that CLOSES as the hold fills, which is
                # the whole tutorial for the verb.
                col = ca(MYStage.C_PALE, 0.30)
                if col is not None:
                    cv.circle(col, (px, py), int(MY_NAME_R), 1)
                frac = inv_clamp(g.name_t / float(MY_NAME_TICKS), 0.0, 1.0)
                pts = []
                steps = max(3, int(46 * frac))
                for i in range(steps + 1):
                    ang = -1.5708 + 6.28318 * frac * (i / float(steps))
                    pts.append((int(px + math.cos(ang) * (MY_NAME_R - 9)),
                                int(py + math.sin(ang) * (MY_NAME_R - 9))))
                if len(pts) > 1:
                    gc = ca(MYStage.C_GOLD, 0.55 + 0.45 * frac)
                    if gc is not None:
                        cv.lines(gc, False, pts, 3)
            elif g.name_flash > 0.02:
                col = ca(MYStage.C_GOLD, g.name_flash * 0.8)
                if col is not None:
                    cv.circle(col, (px, py),
                            int(MY_NAME_R + (1.0 - g.name_flash) * 120), 2)

            # --- you -----------------------------------------------------------
            if g.iframes <= 0 or (g.tick // 4) % 2 == 0:
                self._draw_heart(g, rv, tex, sblit, g.px, g.py, sx, sy, st, at,
                                alpha=1.0 if g.mode == "dark" else 0.85)

            # --- the winning reveal ---------------------------------------------
            # The only time in the act that a body is drawn at all, and the
            # only time this figure is ever fully lit.
            if g.mode == "leave_w" and g.end_show > 0.01:
                sub = g.subject()
                if sub is not None:
                    self._draw_body(g, rv, tex, sblit, sub["x"], sub["y"] - 150,
                                    0.20, sx, sy, st, at,
                                    shear=0.35, ap=g.body_ap,
                                    lit=g.body_lit, band=g.body_band,
                                    diss=g.body_diss,
                                    alpha=inv_clamp(g.end_show * 1.4, 0.0, 1.0))

            if fade > 0.01:
                self._render_dark_hud(g, rv, rect, qa, blit_text, sx, sy, fade)

        def _render_dark_hud(self, g, rv, rect, qa, blit_text, sx, sy, fade):
            # SOLVED -- and the pips are what make a bar of 100 legible as
            # "six landed accusations" without a word of explanation.
            bar_w = 300
            blit_text("SOLVED", 12, MY_DIM + qa(fade), 40, 26, bold=True,
                    w=160, h=24, outline=MY_BLACK)
            rv.blit(rect("#04050a" + qa(0.70 * fade), bar_w + 4, 14), (38, 44))
            rv.blit(rect("#141820" + qa(fade), bar_w, 10), (40, 45))
            fw = int(bar_w * inv_clamp(g.solve_shown / MY_SOLVE_MAX, 0.0, 1.0))
            if fw > 0:
                rv.blit(rect(MY_GOLD + qa(fade), fw, 10), (40, 45))
            pips = int(math.ceil(MY_SOLVE_MAX / MY_SOLVE_GAIN))
            for i in range(1, pips):
                px_ = 40 + int(bar_w * (i * MY_SOLVE_GAIN / MY_SOLVE_MAX))
                rv.blit(rect(MY_BLACK + qa(0.8 * fade), 2, 10), (px_, 45))

            # FIELD -- act one's word, and the player already knows exactly
            # what it means. That reuse is the whole of rule 1's affordance
            # budget for this act.
            blit_text("FIELD", 12, MY_DIM + qa(fade), 40, 66, bold=True,
                    w=120, h=24, outline=MY_BLACK)
            blit_text("%d" % len(g.bodies), 20,
                    (MY_RED if len(g.bodies) > MY_BODIES_MAX else MY_PALE)
                    + qa(fade), 96, 60, bold=True, w=90, h=30,
                    outline=MY_BLACK)

            # HP, bottom left, small -- health is the only loss condition and
            # it is not what the act is about, so it does not get the big
            # counter.
            blit_text("HP", 12, MY_DIM + qa(fade), 40, 654, bold=True,
                    w=60, h=24, outline=MY_BLACK)
            blit_text("%03d" % int(max(0, math.ceil(g.hp_shown - 0.0001))), 24,
                    (MY_RED if g.hp < 90 else MY_PALE) + qa(fade), 70, 646,
                    bold=True, w=120, h=36, outline=MY_BLACK)

            # TRACES -- how many statements are still worth anything, which is
            # the number the belief field is made of.
            blit_text("TRACES", 12, MY_DIM + qa(fade), 1240, 636, bold=True,
                    anchor=(1.0, 0.0), w=140, h=24, outline=MY_BLACK)
            blit_text("%d" % len(g.live), 22,
                    (MY_GOLD if len(g.live) >= 4 else MY_PALE) + qa(fade),
                    1240, 652, bold=True, anchor=(1.0, 0.0), w=90, h=32,
                    outline=MY_BLACK)

            # SWEEP -- a bar that fills back, so the bargain is one you can see
            # coming rather than one you gamble on.
            ready = (g.sweep_cd <= 0 and g.sweep_t <= 0)
            blit_text("SWEEP", 11,
                    (MY_LAMPC if ready else MY_FAINT) + qa(fade),
                    1130, 616, bold=True, anchor=(1.0, 0.0), w=120, h=22,
                    outline=MY_BLACK)
            rv.blit(rect("#141820" + qa(fade), 120, 4), (1120, 634))
            cdw = int(120 * (1.0 - inv_clamp(g.sweep_cd / float(MY_SWEEP_CD),
                                            0.0, 1.0)))
            if cdw > 0:
                rv.blit(rect((MY_LAMPC if ready else MY_DIM) + qa(fade),
                            cdw, 4), (1120, 634))

            if g.reopen_warn > 0.01:
                a = fade * (0.45 + 0.55 * (0.5 + 0.5 * math.sin(g.tick * 0.32)))
                blit_text("REOPENING", 22, MY_RED + qa(a), 640, 40, bold=True,
                        anchor=(0.5, 0.0), w=420, h=36, outline=MY_BLACK)

            blit_text("Z  ACCUSE      X  SWEEP", 12, MY_FAINT + qa(fade),
                    640, 690, anchor=(0.5, 0.0), w=520, h=24,
                    outline=MY_BLACK)

            if g.god:
                blit_text("GOD", 12, MY_WARN + qa(0.7 * fade), 1240, 26,
                        anchor=(1.0, 0.0), w=120, h=24, outline=MY_BLACK)


# --- THE SCREEN --------------------------------------------------------------
screen inv_mystery_screen(game):
    modal True
    use enter_m_input_lock()

    add Solid("#04050a")
    add MYStage(game)

    key "K_ESCAPE" action Function(game.toggle_pause)
    key "mouseup_3" action Function(game.toggle_pause)
    if game.paused:
        key "K_q" action Function(game.give_up)

    if config.developer:
        key "K_g" action Function(game.toggle_god)

    timer 0.25 repeat True action Function(inv_poll_result, game, _update_screens=False)


# --- WRAPPER -----------------------------------------------------------------
default my_game = None
default my_deaths = 0
default my_retry = False

label archivist_invasion_mystery:
    $ my_deaths = 0
    $ my_retry = False

label inv_mystery_fight:
    $ renpy.block_rollback()

    $ my_game = MYGame(retry=my_retry, deaths=my_deaths,
                    debug=config.developer, start_open=inv_dev_start_open)

    $ _my_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ _my_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None
    scene black

    call screen inv_mystery_screen(my_game)
    $ _my_result = _return

    $ my_game = None
    $ quick_menu = _my_prev_quick_menu
    $ _game_menu_screen = _my_prev_game_menu
    $ inv_music_stop(1.0)
    $ inv_heart_stop(0.6)
    $ inv_stop_sfx(0.2)
    scene black

    if _my_result == "victory":
        $ inv_record_result("mystery", True)
        jump inv_mystery_victory
    elif _my_result == "quit":
        jump inv_mystery_quit

    $ inv_record_result("mystery", False)
    jump inv_mystery_defeat

label inv_mystery_victory:
    if inv_dev_test:
        $ renpy.notify("MYSTERY: named. Still open.")
        return
    # STORY PLACEMENT: DRAWING BOARD.
    return

label inv_mystery_defeat:
    $ my_deaths += 1
    $ my_retry = True

    menu:
        "AGAIN":
            scene black
            jump inv_mystery_fight

        "STOP":
            if inv_dev_test:
                $ renpy.notify("MYSTERY: unsolved. Recorded.")
            return

label inv_mystery_quit:
    $ my_retry = True
    if inv_dev_test:
        $ renpy.notify("MYSTERY: withdrawn.")
    return
