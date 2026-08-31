# =============================================================================
# ARCHIVIST INVASION 03 -- NONFICTION
# =============================================================================
#
# WHAT THIS IS
#   The third Archivist Invasion. Same two-act shape as Biography and Horror,
#   built out of a third set of materials.
#
#       Biography wants to FINISH something.
#       Horror wants to BE NEAR you.
#       Nonfiction wants to CHECK you against the record.
#
#   It is not trying to kill anybody. It is establishing whether what is in
#   front of it can be corroborated, and whatever cannot be corroborated does
#   not get to have happened. It does not attack. IT RETRACTS.
#
# THE FORM IT IS WEARING
#   Biography turned up wearing a specific person, because a life needs
#   someone to have lived it. Nonfiction turns up wearing NOBODY IN
#   PARTICULAR -- a figure with no distinguishing features -- because a fact
#   does not need anybody in particular to be true. The blankness is the
#   correct answer, not a placeholder for one.
#
#   (Practically: nonfiction.png is a stand-in until the real portrait lands.
#   Nothing in this file cares what is in the image -- inv.strike prints
#   whatever it is given as a monochrome halftone plate, so a flat silhouette
#   reads as an illustration in a reference book rather than as missing art.
#   When the portrait arrives, update NF_SPRITE_W/H and NF_FIG_DX/DY and
#   nothing else.)
#
# THE ONE THING IT WILL NOT DO
#   Horror's readouts LIE to you, more often the closer it gets. Nonfiction's
#   readouts are always true. It tells you the name of the move it is about to
#   make and the exact number attached to it, every single turn, and it never
#   withholds anything. That is not mercy. It is procedure.
#
#   ACT ONE -- the sourcing bout. Turn-based, the house furniture, the same
#   rolling odometer. The twist is that DAMAGE IS NOT DAMAGE UNTIL IT IS
#   SOURCED. STATE puts a claim on the board as UNSOURCED; CITE moves the
#   whole unsourced pile onto its permanent LEDGER. Everything sitting
#   unsourced can be taken back, and it will be: carrying a pile makes its
#   QUERY hurt more, and a STRIKE erases the lot.
#
#   ACT TWO -- the CORRUPTIVE STATE: the page. Every light in the room comes
#   up, the room turns WHITE, and the fight is held on a plain ruled plane
#   that is being struck out cell by cell while you stand on it. There is
#   nothing to attack. The only win is to get yourself ON RECORD -- and that
#   is done by STANDING STILL on something it has already corroborated, which
#   is the last thing a shrinking floor lets you do.
#
#   THE ESCROW COMES WITH YOU (Aug 14 2026). The first build of this act
#   dropped act one's one good idea at the door and became "walk to the box,
#   stand in the box, dodge the walls" -- a fine picture and a thin loop,
#   because nothing you did was ever at risk and so nothing you did was ever
#   a decision. Now standing on the entry fills PENDING, pending is capped,
#   pending is what a retraction takes and what a redaction takes, and it
#   becomes VERIFIED only when you walk it into THE MARGIN. Column zero of
#   the grid is the margin: nothing may ever be struck out of it (a redaction
#   covers text; the margin is not text), the entry is never placed in it,
#   and standing anywhere in it files what you are carrying. The row you file
#   on will not take another citation until the ink is dry, so the walk is a
#   different walk each time.
#
#   FILL, CARRY, FILE -- and each third of that is exposed to something
#   different: filling to the volleys landing around you, carrying to the
#   page having closed behind you while you stood there, filing to which
#   rows are still open. VERIFIED cannot be taken by anything, which is act
#   one's rule ("only the ledger is real") honoured rather than restated, and
#   which is also why there is no death spiral in here -- only lost time.
#
#   ONE VERB: hold Z to ATTEST. It roots you, and while it lasts you fill at
#   double rate, a retraction cannot take what you are carrying, and a
#   redaction cannot cover the cell you are standing in. All three are things
#   you CHOOSE; nothing in the act obliges you to spend it, which is the fix
#   for the version of this act that did (see BALANCE).
#
#   AND THE PAGE GETS WORKED OVER. The escalation is one number, `churn()`,
#   and it buys: a press cycle that stretches from six seconds to twelve (and
#   past NF_PRESS_PARTIAL_AT stops lifting everything, so the sheet is never
#   quite blank again); a SECOND HALFTONE SCREEN at a fighting angle, which
#   is where moire comes from and is the correct way for a printed thing to
#   become hard to look at; a second set of rules between the first; grubbier
#   stock; and printer's correction marks accumulating in the open cells.
#   None of that has a hitbox, none of it flows, and none of it invents a
#   frame of anything -- which are the three things this Archivist may not do.
#
#   THE PLATE IS NOT ON THE BEAT, and that was tried and cut (user, Aug 14
#   2026). The watermark re-registers on its own schedule and on the passes
#   that bring a volley in, so it falls near the pulse sometimes and does not
#   the rest of the time. That reads as coincidence rather than choreography,
#   which is the better version of the effect and the only one in character:
#   a press that keeps time is a press with an opinion about the music, and
#   nothing in this fight has an opinion. Do not re-lock it.
#
# THE THREE POLES (this is why act two is what it is)
#       Biography   you must CLOSE distance.        A stage you circle.
#       Horror      you must OPEN distance.         A throat you flee down.
#       Nonfiction  distance is irrelevant.         A page you HOLD GROUND on.
#   And so the camera: Biography has a proscenium, Horror has a vanishing
#   point, and Nonfiction has NO PERSPECTIVE AT ALL. Flat, orthographic,
#   overhead. It does not invent a camera any more than it invents anything
#   else.
#
# THE JOINT BETWEEN THE ACTS (the thing that makes act one matter)
#   THE LEDGER CARRIES. HP and sources are handed back in full at the tear --
#   what survives is exactly the part of your account you managed to SOURCE,
#   and it becomes your opening VERIFIED. Everything still unsourced at that
#   moment is struck out on screen as the panels come off, which is the lesson
#   act one was teaching, administered once, at full volume.
#
# THE RULES (from the invasion spec -- restated because they bind here too)
#   1. NO FLAVOR TEXT. Controls, numbers and state words only. The complete
#      list of drawable strings in this fight is: NONFICTION / STATE / CITE /
#      AMEND / RUN / QUERY / FOOTNOTE / MARK / STRIKE / CORRECTION / ERRATUM /
#      MARKED / UNSOURCED / UNRECORDED / NO SOURCES / SCRUTINY / HP / SRC /
#      VERIFIED / CREDIT / GOD / PAUSED, plus the act-two readout keys and
#      three control hints. Nothing in here is a sentence.
#   2. NOTHING MAY BE FUNNY. Checked hardest on the white page: a bright
#      screen is one bad decision away from cheerful. It is lit like a
#      photocopier, it has no shadows to hide in, and the only colour anywhere
#      in the second half is you.
#   3. IT MOVES LIKE SOMETHING THAT HAS SEEN A DIAGRAM. Its own body shader,
#      inv.strike -- see the note there. Nothing about it flows.
#   4. IT ARRIVES AND LEAVES THROUGH A HOLE. It does not climb out of the
#      rupture: it is PRINTED into the room, in three hard registration passes
#      with more of it present each time.
#   5. EVERY PATTERN MUST BE BEATABLE HITLESS -- and here that is not a
#      spacing rule, it is a REACHABILITY rule. See FAIRNESS below.
#
# FAIRNESS (a contract, not decoration)
#   The page is a maze that closes. A maze can be unfair in a way a bullet
#   pattern cannot: it can seal you in. So every redaction is validated by
#   flood fill BEFORE it is committed, on the actual 8x5 grid:
#
#     0. THE MARGIN IS NEVER STRUCK, unconditionally, and it can never be
#        WALLED OFF either -- five marks down column one would put the filing
#        strip on the far side of the page from you, which is not a hard
#        fight, it is a stalled one. Every check below also requires the
#        anchor's open component to touch the margin.
#     1. THE ANCHOR IS NEVER STRUCK, nor are its four neighbours. There is
#        always somewhere to stand.
#     2. A LINE IS REFUSED if committing it would leave the anchor
#        unreachable from open ground, or would shrink the open component
#        below NF_MIN_ROOM cells. Refused silently -- a quiet volley beats an
#        impossible one.
#     3. YOU ARE NEVER SEALED INSIDE INK. If a strike lands on the cell you
#        are standing in, it hits you and EJECTS you to the nearest open cell
#        in the anchor's component. Redaction pushes you out of the text; it
#        does not bury you in it.
#     4. A LAST-RESORT RE-CHECK after inking (you may have moved during the
#        telegraph) lifts the most recent line if the anchor ended up cut off.
#     5. THE ANCHOR IS PLACED INSIDE YOUR OWN COMPONENT, and ink is lifted off
#        that component's edge until there is room to fight in it. This one
#        was not in the first draft and the harness found what it cost: a
#        relocation could drop the anchor in a pocket you were walled out of,
#        which is not a hard fight, it is an unwinnable one with no death, no
#        message and no way to tell. 8861 violations across eight runs.
#        Anything that moves the anchor goes through _place_anchor.
#
# BALANCE (MEASURED, not guessed -- change one number and re-run the harness)
#   These figures come from driving NFGame headless with scripted bots. The
#   method is the one from the other fights: an init 999 block gated on an env
#   var, a fake _poll_input, run via lint. Rebuild it before retuning anything;
#   it caught two things nothing else would have, both recorded below.
#
#   ACT ONE. Its standing is 1000 and the tear is at 480 sourced, or turn 18,
#   whichever comes first. STATE puts ~70 on the board and costs 9 scrutiny;
#   CITE banks the pile for 10 of your 40 sources and takes 20 scrutiny back
#   off. So the loop is STATE STATE CITE and AMEND is what pays for it -- the
#   heal, the guard, the source refill and the big scrutiny drop in one, at
#   the price of a third of everything you have not sourced yet. Measured:
#       STATE / CITE / AMEND as needed   18 turns, 512 sourced, full health
#                                        -> hands over 45, the ceiling
#       STATE every single turn          DEAD on turn 12, 145 unsourced,
#                                        nothing on the ledger at all
#       AMEND every single turn          survives everything, sources nothing
#                                        -> hands over 8, the floor
#   Greed is punished twice over: QUERY scales with the unsourced pile, and
#   scrutiny at 100 fires an ERRATUM that wipes the pile AND takes 90 back off
#   the ledger. Note the shape of that spread -- act one is close to
#   unloseable if you never push, and it is the SECOND HALF that collects.
#
#   ACT TWO, RE-MEASURED AFTER THE ESCROW (Aug 14 2026). VERIFIED is 100.
#   Standing still on the entry fills PENDING at 0.100/tick (0.200 attesting)
#   to a cap of 34, and pending only becomes verified in the margin. Six
#   seeded runs a line, and THE LINE THAT MATTERS IS THE FIRST ONE -- the
#   naive read of the new loop, from a player who fills to the cap every time
#   and never reacts to a telegraph:
#       naive: fills to the cap        57-167s, 38-258 of 280  -- wins 6/6
#       files early on a telegraph     39- 95s, 170-280        -- wins 6/6
#       ...and attests as well         29- 63s, 192-258        -- wins 4/4
#       hesitates a third of the time 131-207s,  60-148        -- wins 4/4
#   No line of that table loses, which is the property the old one had and
#   the property to preserve. The two middle lines are the whole point of the
#   rebuild: BOTH of them are things a player discovers rather than is told,
#   and each roughly halves the run without ever being required.
#
#   THE FAIRNESS CHECK IS IN THE HARNESS, not just in the code. Every tick of
#   every run above asserted that from where the player is standing, BOTH the
#   entry and the margin are reachable through open cells. 0 violations over
#   20 runs. Rebuild that assertion before touching _plan_volley,
#   _commit_volley, _place_anchor, or the partial press.
#
#   THE FIRST BUILD OF THIS ACT WAS UNWINNABLE AND THE HARNESS SAID IT WAS
#   FINE. Worth keeping, because the failure is instructive. Strikes took out
#   whole ROWS AND COLUMNS, so four of them inside a press cycle left the page
#   almost solid black; a full-height rule swept across as well, unanswerable
#   except by attesting; and attesting was funded below what that rule
#   demanded, with the shortfall only repayable through a near miss nothing on
#   screen teaches. Arithmetic: the sweep alone killed you in ~72s and filling
#   the bar needed ~66s of standing still, before travel or dodging.
#   The bot won 8 runs out of 8 -- because it pathed perfectly and hugged ink,
#   so it always had credit. A bot that plays a fight optimally proves it is
#   POSSIBLE. It cannot prove it is playable, and it will hide any difficulty
#   that only exists for someone who does not already know the answer.
#
#   What that cost: rows and columns became short contiguous marks, the sweep
#   was cut outright, and the two legibility holes the bot could not feel --
#   nothing pointing at the anchor, nothing distinguishing standing still from
#   standing on it -- became the leader line and the closed ring.
#
#   CREDIT is a skill curve, not a toll: regen alone funds one attest per ~390
#   ticks and threading a volley (ink landing in the cell next to you) buys
#   another. Play close and you can attest often; park in the emptiest corner
#   of the page and you attest rarely. Neither line loses the fight.
#
# ARCHITECTURE
#   Same as every invasion: NFGame owns the simulation, NFStage is one CDD
#   stepping it at a fixed 60Hz inside render(). Two shaders of its own --
#   inv.plain (the room, BOTH acts: unlike the other two, Nonfiction does not
#   change rooms at the tear, it EMPTIES the one it is in) and inv.strike (the
#   body). The padded plate and the heart come from invasions.rpy.
#
# READ THIS FIRST IF YOU ARE LOST
#   NFGame.step() dispatches on self.mode:
#     arrive   the rupture; it is printed into the room in passes
#     menu     act one commands
#     beat     the one-line readout; WAITS for a key, never auto-advances
#     enemy    its turn
#     shift    the tear -- the unsourced pile is struck out, the page whitens
#     page     act two
#     leave_w  it files itself as unverifiable / leave_l  you are retracted
#   Units: screen pixels (1280x720), speeds are px per 1/60s tick, timers are
#   ticks. The act-two grid is NF_COLS x NF_ROWS cells addressed (col, row).
# =============================================================================

# --- SHADERS -----------------------------------------------------------------
init -9 python:
    NF_PLAIN_OK = False
    NF_STRIKE_OK = False

    def _nf_register_plain():
        # THE ROOM, BOTH ACTS. The same hyperspace plate every invasion is
        # fought over -- printed. There is no domain warp anywhere in this
        # shader and that is deliberate: Biography's room boils and Horror's
        # room rushes, and nothing in Nonfiction's room is allowed to FLOW,
        # because flowing is a thing an image does when something is inventing
        # the next frame of it. This room is re-set instead: it samples on a
        # quantised grid, posterizes to a handful of levels, screens the result
        # into halftone dots, and jumps to a new registration in hard steps.
        # It is never still and it is never moving.
        #
        # u_nf_open is the whole corruptive shift in one number. At 0 the plate
        # is a photographic negative in a dark room. At 1 the room is a sheet
        # of paper: bone white, ruled, with the printing almost entirely gone
        # off it. Nonfiction does not drag you into a different room at the
        # tear -- it empties the one you are already in.
        renpy.register_shader("inv.plain", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_nf_res;
            uniform float u_nf_time;
            uniform float u_nf_open;
            uniform float u_nf_press;
            uniform float u_nf_reg;
            uniform float u_nf_scrut;
            uniform float u_nf_flash;
            uniform float u_nf_dark;
            uniform float u_nf_churn;
            uniform vec4 u_nf_hole;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float nf_hash(vec2 p) {
                return fract(sin(dot(p, vec2(41.13, 289.7))) * 27183.3141);
            }
            vec2 nf_mirror(vec2 p) {
                return abs(fract(p * 0.5) * 2.0 - 1.0);
            }
        """, fragment_300="""
            vec2 uv = v_tex_coord;
            float t = u_nf_time;
            float open = clamp(u_nf_open, 0.0, 1.0);
            float scrut = clamp(u_nf_scrut, 0.0, 1.0);
            float press = clamp(u_nf_press, 0.0, 1.0);
            // How hard the page is being worked. Zero at the tear; by the end
            // the sheet has been through the press enough times to show it.
            float churn = clamp(u_nf_churn, 0.0, 1.0) * open;

            vec2 c = uv - 0.5;

            // The rupture, same instrument as every arrival -- but a hole in a
            // page rather than in a fluid, so the lip is a hard rule.
            vec2 hp = (u_nf_hole.xy / max(u_nf_res, vec2(1.0))) - 0.5;
            float hr = max(u_nf_hole.z, 1.0) / max(u_nf_res.x, 1.0);
            float hs = clamp(u_nf_hole.w, 0.0, 1.0);
            vec2 hv = c - hp;
            float hd = length(hv);
            float hinf = (1.0 - smoothstep(0.0, hr, hd)) * hs;
            if (hinf > 0.001) {
                float ha = hinf * hinf * 4.2;
                float ccs = cos(ha);
                float csn = sin(ha);
                hv = vec2(hv.x * ccs - hv.y * csn, hv.x * csn + hv.y * ccs);
                c = hp + hv * (1.0 - 0.60 * hinf);
            }

            // REGISTRATION. Not a wave -- a STEP. The plate is re-set on the
            // page at a discrete offset and HOLDS there until the next pass.
            float sstep = floor(t * 0.75 + u_nf_reg);
            vec2 reg = vec2(nf_hash(vec2(sstep, 1.0)) - 0.5,
                            nf_hash(vec2(sstep, 7.0)) - 0.5)
                    * (0.006 + 0.055 * press + 0.014 * churn);
            vec2 sp = c + reg;

            // Quantised sampling: the substrate has a resolution, and you can
            // see it.
            float cells = mix(340.0, 148.0, open);
            sp = floor(sp * cells) / cells;
            float lum = dot(texture2D(tex0, nf_mirror(sp + 0.5)).rgb,
                            vec3(0.299, 0.587, 0.114));

            // POSTERIZE, then SCREEN. Ink is a dot or it is nothing.
            float levels = mix(6.0, 3.0, open);
            lum = floor(lum * levels) / levels;
            vec2 rot = vec2(uv.x * 0.7071 - uv.y * 0.7071,
                            uv.x * 0.7071 + uv.y * 0.7071);
            vec2 dc = fract(rot * mix(300.0, 205.0, open)) - 0.5;
            float dens = clamp(1.0 - lum, 0.0, 1.0);
            float rad = 0.53 * sqrt(dens);
            float ink = 1.0 - smoothstep(rad - 0.08, rad + 0.08, length(dc));

            // Almost all of the printing comes off the sheet at the tear.
            ink *= mix(1.0, 0.20, open);

            vec3 paper = mix(vec3(0.031, 0.033, 0.038),
                            vec3(0.906, 0.898, 0.876), open);
            vec3 inkc = mix(vec3(0.50 + 0.22 * scrut,
                                0.52 + 0.22 * scrut,
                                0.50 + 0.20 * scrut),
                            vec3(0.055, 0.052, 0.050), open);
            vec3 col = mix(paper, inkc, ink);

            // A SECOND SCREEN, AT A FIGHTING ANGLE. This is the whole
            // escalation and it is the correct one for this fight: a page
            // that has been run through the press again and again picks up
            // another halftone out of register with the first, and two
            // screens at slightly different angles is where MOIRE comes
            // from. So the sheet gets harder and harder to look at without
            // one new object being added to it, without anything flowing, and
            // without inventing a single frame of anything.
            // It carries its OWN density rather than the plate's: at open the
            // plate is nearly blank, so a second screen keyed to it would be
            // invisible exactly where it is wanted. Held to a third of full
            // weight -- the page has to become hard to look at, never hard to
            // read, and the redactions and the one red thing on it both have
            // to stay findable.
            if (churn > 0.002) {
                float ang2 = 0.7854 + 0.22 * churn;
                vec2 rot2 = vec2(uv.x * cos(ang2) - uv.y * sin(ang2),
                                uv.x * sin(ang2) + uv.y * cos(ang2));
                vec2 dc2 = fract(rot2 * mix(214.0, 176.0, churn)) - 0.5;
                float rad2 = 0.53 * sqrt(clamp(1.0 - lum * 0.74, 0.0, 1.0));
                float ink2 = 1.0 - smoothstep(rad2 - 0.10, rad2 + 0.10,
                                            length(dc2));
                col = mix(col, inkc, ink2 * churn * 0.34);
            }

            // RULED. Horizontal rules the whole way down, and one vertical
            // margin rule, because this is a page and it has always been a
            // page. The margin rule sits exactly on the edge of the margin
            // COLUMN in act two -- the shader draws the boundary the fight is
            // played against, rather than a decorative line near it.
            float ly = uv.y * u_nf_res.y;
            float rule = 1.0 - smoothstep(0.0, 0.055, fract(ly / 26.0));
            col = mix(col, inkc, rule * (0.09 + 0.26 * open + 0.16 * churn));
            // ...and a second set of rules between them once the page has
            // been worked, half-height and half-weight: ruled twice as close
            // and never quite lining up with the first set.
            float rule2 = 1.0 - smoothstep(0.0, 0.075, fract(ly / 13.0 + 0.5));
            col = mix(col, inkc, rule2 * 0.14 * churn);
            float mx = mix(0.113, 0.249, open);
            float marg = 1.0 - smoothstep(0.0, 1.6 / u_nf_res.x,
                                        abs(uv.x - mx));
            col = mix(col, inkc, marg * (0.10 + 0.34 * open));

            // Tooth. Paper has a surface; a negative has grain -- and paper
            // that has been through a press this many times has more of it.
            float tooth = nf_hash(floor(uv * u_nf_res * 0.5));
            col *= 1.0 - (0.030 + 0.028 * open + 0.055 * churn) * tooth;
            // And it is not white any more. Nothing dramatic: the stock goes
            // a shade grey and a shade warm, the way a sheet does.
            col = mix(col, col * vec3(0.90, 0.885, 0.855), churn * open);

            if (hs > 0.001) {
                float core = 1.0 - smoothstep(hr * 0.14, hr * 0.54, hd);
                col *= mix(1.0, 0.015, core * hs);
                float lip = 1.0 - smoothstep(0.0, hr * 0.10,
                                            abs(hd - hr * 0.54));
                col = mix(col, mix(vec3(0.86, 0.87, 0.84), vec3(0.02),
                                open), lip * hs);
            }

            // Act one is a room and rooms have corners. A page does not, so
            // the vignette leaves entirely at the tear.
            float r = length(c);
            float vig = 1.0 - r * r * (0.85 + 0.95 * scrut);
            col *= mix(max(vig, 0.0), 1.0, open);

            // THE PRESS COMING DOWN. A brief inversion, not a glow.
            col = mix(col, vec3(1.0) - col, press * 0.30);

            col = mix(col, vec3(0.97, 0.97, 0.95), clamp(u_nf_flash, 0.0, 1.0));
            col *= 1.0 - clamp(u_nf_dark, 0.0, 1.0);
            gl_FragColor = vec4(col, 1.0);
        """)

    def _nf_register_strike():
        # NONFICTION'S OWN BODY. Every Archivist gets its own way of being
        # wrong, or they all read as the same puppet in different hats.
        #
        #   Biography  MISREGISTRATION -- fourteen hard bands sliding out of
        #              sync, chromatic fringing, high frequency. Digital.
        #   Horror     UNDULATION -- low frequency, liquid, no colour split, a
        #              swell from inside and a silhouette that frays into
        #              smoke. You cannot find its edge.
        #   Nonfiction REPRODUCTION -- and it is the opposite of both, because
        #              it does not deform at all. It is PRINTED. Luminance
        #              only, posterized, screened into halftone dots, ruled
        #              across like typeset copy. Its bands do not travel
        #              between positions: they JUMP to a new offset and hold
        #              there, the way a plate is re-set rather than moved.
        #              It has no colour because it does not invent one.
        #
        # And it is REDACTED: u_st_bars grows solid black rules across it that
        # overshoot its own silhouette. That is its dissolve too -- it does
        # not erode in cells like Biography or drain bottom-up like Horror. It
        # is struck out.
        #
        # NOTE ON THE FLAT SOURCE: the tone ramp below is what lets a
        # featureless grey silhouette resolve into a plate with real tonal
        # structure instead of one uniform field of identical dots. Keep it
        # when the finished portrait arrives; it flatters that too.
        renpy.register_shader("inv.strike", variables="""
            uniform sampler2D tex0;
            uniform vec2 u_st_res;
            uniform float u_st_t;
            uniform float u_st_jump;
            uniform float u_st_reg;
            uniform vec2 u_st_stretch;
            uniform float u_st_pivot;
            uniform float u_st_ink;
            uniform float u_st_paper;
            uniform float u_st_bars;
            uniform float u_st_churn;
            varying vec2 v_tex_coord;
        """, fragment_functions="""
            float st_hash(vec2 p) {
                return fract(sin(dot(p, vec2(63.71, 11.29))) * 19317.7193);
            }
            // ONE SCREEN OF A PROCESS SEPARATION. `ang` is the screen angle,
            // `freq` its ruling, `tone` the density it is carrying. Returns
            // dot coverage 0..1. Real process printing runs each separation at
            // a DIFFERENT angle for exactly one reason -- so the rosettes
            // interlock instead of beating against each other -- and running
            // three of them is what makes this read as a printed plate rather
            // than as a filter with a dot pattern in it.
            float st_screen(vec2 uv, float ang, float freq, float tone,
                            float gain) {
                float ca = cos(ang);
                float sa = sin(ang);
                vec2 r = vec2(uv.x * ca - uv.y * sa, uv.x * sa + uv.y * ca);
                vec2 d = fract(r * freq) - 0.5;
                // DOT GAIN: ink spreads on absorbent stock, so a dot prints
                // bigger than it was screened, and it spreads MORE in the
                // midtones than at either end. This is the single detail that
                // separates "halftoned" from "printed".
                float cov = clamp(tone, 0.0, 1.0);
                cov += gain * cov * (1.0 - cov) * 1.6;
                float rad = 0.55 * sqrt(clamp(cov, 0.0, 1.0));
                return 1.0 - smoothstep(rad - 0.085, rad + 0.085, length(d));
            }
        """, fragment_300="""
            vec2 plate_uv = v_tex_coord;
            vec2 uv = v_tex_coord;
            vec2 piv = vec2(0.5, clamp(u_st_pivot, 0.0, 1.0));
            vec2 st = max(u_st_stretch, vec2(0.08));
            uv = (uv - piv) / st + piv;

            float t = u_st_t;
            float jump = clamp(u_st_jump, 0.0, 3.0);

            // RE-SET, NOT WARPED. Nine bands, each holding a fixed offset for
            // the whole of a registration step and then cutting to another.
            float sstep = floor(t * 3.0 + u_st_reg);
            float band = floor(uv.y * 9.0);
            uv.x += (st_hash(vec2(band, sstep)) - 0.5) * 0.032 * jump;
            uv += vec2(st_hash(vec2(sstep, 3.0)) - 0.5,
                    st_hash(vec2(sstep, 11.0)) - 0.5) * 0.009 * jump;

            vec4 src = texture2D(tex0, uv);
            float a = src.a;
            float churn = clamp(u_st_churn, 0.0, 1.0);

            // PRINTED, AND NOW ACTUALLY PRINTED. It used to be one 45-degree
            // screen over a posterized luminance, which is a halftone FILTER.
            // A plate is three separations, each screened at its own angle,
            // each carrying a different part of the tone range, and each very
            // slightly out of register with the others -- so this runs the
            // real process angles (15 / 75 / 45, the last one for the heavy
            // separation because that is where it goes) and lets the rosettes
            // interlock.
            //
            // NOTE THIS IS NOT BIOGRAPHY'S AXIS. Biography's plates fail to
            // line up and that is its whole character; these three line up
            // CORRECTLY and merely reveal that the thing was reproduced. The
            // difference is discipline, and it is the difference between the
            // two Archivists.
            float lum = dot(src.rgb, vec3(0.299, 0.587, 0.114));
            lum = clamp(lum * (0.58 + 0.66 * (1.0 - uv.y)), 0.0, 1.0);
            // Posterized, but on more levels than before and with the step
            // itself softened, so the tone ramp survives being screened.
            float levels = mix(5.0, 7.0, churn);
            lum = floor(lum * levels) / levels;
            float tone = clamp(1.0 - lum, 0.0, 1.0);

            // The three separations. Light / mid / heavy, each screened
            // separately, so a midtone is carried by two plates at once and a
            // shadow by all three -- which is where the density comes from.
            float gain = 0.18 + 0.34 * churn;
            float freq = mix(150.0, 196.0, churn);
            float s_lt = st_screen(uv, 0.2618, freq * 1.00,
                                clamp(tone * 1.35, 0.0, 1.0), gain);
            float s_md = st_screen(uv, 1.3090, freq * 0.88,
                                clamp(tone * 1.05 - 0.16, 0.0, 1.0), gain);
            float s_hv = st_screen(uv, 0.7854, freq * 0.74,
                                clamp(tone * 0.95 - 0.42, 0.0, 1.0), gain);
            float dotv = clamp(s_lt * 0.44 + s_md * 0.36 + s_hv * 0.42,
                            0.0, 1.0);

            vec3 stock = mix(vec3(0.74, 0.75, 0.72), vec3(0.94, 0.93, 0.91),
                            clamp(u_st_paper, 0.0, 1.0));
            vec3 inkc = mix(vec3(0.085, 0.085, 0.095), vec3(0.04, 0.04, 0.04),
                            clamp(u_st_paper, 0.0, 1.0));

            // PAPER FIBRE. Stock has a grain and it takes ink unevenly, so the
            // coverage is modulated by the sheet rather than being uniform.
            float fibre = st_hash(floor(plate_uv * u_st_res * 0.65));
            dotv *= 1.0 - (0.10 + 0.16 * churn) * fibre;

            vec3 printed = mix(stock, inkc, dotv);

            // SHOW-THROUGH. Something is printed on the other side of the
            // sheet and thin stock does not hide it: the body sampled from
            // behind, mirrored, very faint, and fainter still where this side
            // is already heavily inked.
            float back = dot(texture2D(tex0, vec2(1.0 - uv.x, uv.y)).rgb,
                            vec3(0.299, 0.587, 0.114));
            printed = mix(printed, printed * (0.90 - 0.14 * back),
                        (0.30 + 0.35 * churn) * (1.0 - dotv));

            float pr = clamp(u_st_ink, 0.0, 1.0);
            vec3 col = mix(src.rgb, printed, pr);

            // Typeset: rules run across it the same as they run across the
            // page it is printed on -- and a second, closer set once the sheet
            // has been through the press enough times to show it.
            float ly = uv.y * u_st_res.y;
            col = mix(col, inkc,
                    (1.0 - smoothstep(0.0, 0.07, fract(ly / 21.0))) * 0.20 * pr);
            col = mix(col, inkc,
                    (1.0 - smoothstep(0.0, 0.09, fract(ly / 10.5 + 0.5)))
                    * 0.13 * pr * churn);

            // REDACTED. Six rules, each growing from its own left edge and
            // overshooting the silhouette, because a redaction always covers
            // more than the thing it covers.
            float bars = clamp(u_st_bars, 0.0, 1.0);
            float bar = 0.0;
            float baredge = 0.0;
            for (int i = 0; i < 6; i++) {
                float fi = float(i);
                float on = smoothstep(fi / 7.0, fi / 7.0 + 0.20, bars);
                float by = 0.10 + 0.80 * st_hash(vec2(fi, 21.0));
                float bh = (0.017 + 0.030 * st_hash(vec2(fi, 33.0)))
                        * (0.7 + 2.9 * bars);
                float x0 = 0.08 + 0.14 * st_hash(vec2(fi, 45.0));
                float x1 = x0 + (0.90 - x0) * on;
                float band_y = step(abs(uv.y - by), bh * 0.5);
                float band_x = step(x0, uv.x) * step(uv.x, x1);
                bar = max(bar, band_y * band_x * step(0.001, on));
                float ey = step(abs(uv.y - by), bh * 0.5 + 0.010);
                float ex = step(x0 - 0.008, uv.x) * step(uv.x, x1 + 0.008);
                baredge = max(baredge, ey * ex * step(0.001, on));
            }

            col = mix(col, vec3(0.0), bar);
            // A bar is WET INK, not a black rectangle: it pools at its own
            // edge and darkens the stock just outside itself.
            col = mix(col, inkc * 0.55, clamp(baredge - bar, 0.0, 1.0) * 0.75);
            float gone = smoothstep(0.88, 1.0, bars);
            a = max(a, bar) * (1.0 - gone);

            // ---- THE PLATE CONTRACT (shared by every Archivist body) -------
            // Two things every one of these shaders has to do on its last
            // line, and none of them did until Aug 23 2026.
            //
            // 1. PREMULTIPLIED ALPHA. gl2 blends src + dst * (1 - a), so a
            //    pixel whose RGB is brighter than its own alpha ADDS light --
            //    and at alpha zero with bright RGB it adds light while
            //    claiming to be invisible. Every one of these shaders moves
            //    colour around without reference to alpha somewhere, so all of
            //    them were painting the transparent MARGIN of the padded plate
            //    and drawing the plate's own rectangle on screen as a faint
            //    glowing box. Clamping RGB to alpha is the fix.
            //
            // 2. THE EDGE. A mesh shader is clipped dead at its plate
            //    rectangle, so anything still opaque at the boundary is cut in
            //    a straight line. Padding buys room; it guarantees nothing.
            //    The feather is measured in the plate's OWN untransformed
            //    coordinate, so warps, swells and strays cannot escape it.
            // Nonfiction was the worst offender of the three: `printed`
            // is a bright paper STOCK, mixed in wherever u_st_ink is up and
            // entirely regardless of alpha, so the whole transparent margin
            // sat at roughly 0.74 grey with an alpha of zero -- a lit box the
            // size of the plate, on a dark room.
            vec2 pe = min(plate_uv, vec2(1.0) - plate_uv);
            a *= smoothstep(0.0, 0.050, min(pe.x, pe.y));

            gl_FragColor = vec4(min(col, vec3(a)), a);
        """)

    try:
        _nf_register_plain()
        NF_PLAIN_OK = True
    except Exception as _nf_pl_e:
        NF_PLAIN_OK = False
        try:
            renpy.log("INV FX: plain shader failed: %r" % _nf_pl_e)
        except Exception:
            pass

    try:
        _nf_register_strike()
        NF_STRIKE_OK = True
    except Exception as _nf_st_e:
        NF_STRIKE_OK = False
        try:
            renpy.log("INV FX: strike shader failed: %r" % _nf_st_e)
        except Exception:
            pass


# --- CONSTANTS AND TUNING ----------------------------------------------------
init python:
    NF_SOUP_IMG = INV_DIR + "hyperspace.png"
    NF_SPRITE = INV_DIR + "nonfiction.png"

    # PLACEHOLDER ART. nonfiction.png is a stand-in; these three lines are the
    # only thing that has to change when the finished portrait lands.
    NF_SPRITE_W, NF_SPRITE_H = 1024, 1536
    # The figure does not sit in the middle of its own canvas (alpha bbox is
    # 115,63 - 804,1536), so centring the plate would hang it off to one side.
    # FORMULA: NF_FIG_D* = (canvas centre) - (bbox centre), per axis.
    NF_FIG_DX, NF_FIG_DY = 52.5, -31.5

    NF_ZOOM_ACT1 = 0.28
    # A plate is a TEXTURE and textures cap at 4096px here. 1536 * 0.90 * 1.5
    # padding is ~2074px, comfortably inside; anything above this zoom is
    # applied to the finished mesh instead of rasterised into the plate.
    NF_PLATE_MAX_ZOOM = 0.90
    # Act two: it stops being a figure standing in the room and becomes the
    # WATERMARK ON THE PAGE -- large, faint, behind everything, and it never
    # walks anywhere. It only ever re-registers.
    NF_ZOOM_MARK = 0.62
    NF_MARK_ALPHA = 0.16

    # --- act one -------------------------------------------------------------
    NF_HP_MAX = 280
    NF_SRC_MAX = 40
    NF_STANDING_MAX = 1000
    NF_SHIFT_LEDGER = 480
    # 18, not 15. Measured: the STATE STATE CITE loop plus the AMEND turns
    # that pay for it lands on ~480 sourced around turn 16-18, so a cap of 15
    # was ending the bout on the clock instead of on the ledger and quietly
    # holding the hand-off below its own ceiling (measured 34 where 45 was
    # available).
    NF_SHIFT_TURN_CAP = 18

    # THE ESCROW. STATE puts a claim on the board UNSOURCED; only CITE moves
    # it onto the ledger, and only the ledger is real.
    NF_STATE_LO, NF_STATE_HI = 56, 84
    NF_STATE_SCRUT = 9
    NF_CITE_COST = 10
    NF_CITE_SCRUT = 20
    NF_AMEND_HEAL = 70
    NF_AMEND_SRC = 12
    NF_AMEND_SCRUT = 26
    NF_AMEND_PENDING = 0.34        # your own retraction, taken willingly
    NF_GUARD_MULT = 0.45           # AMEND is the guard as well as the heal

    NF_SCRUT_MAX = 100
    NF_SCRUT_START = 12
    NF_SCRUT_STEP_LO, NF_SCRUT_STEP_HI = 6, 10
    NF_SCRUT_FLOOR = 45            # where it falls back to after an erratum

    NF_QUERY_BASE = 18
    NF_QUERY_PER_PENDING = 0.22    # carrying a pile is what makes this hurt
    NF_FOOTNOTE_DMG = 14
    NF_FOOTNOTE_BLEED = 3
    NF_STRIKE_DMG = 24
    NF_CORROBORATE = 22
    NF_ERRATUM_LEDGER = 90         # it corrects something you already sourced
    NF_ERRATUM_DMG = 52

    # --- act two: the page ---------------------------------------------------
    # Flat, orthographic, overhead. No projection helpers in this file at all,
    # which is the point.
    NF_COLS, NF_ROWS = 8, 5
    NF_CELL_W, NF_CELL_H = 107, 92
    NF_PLANE_X, NF_PLANE_Y = 212, 176
    NF_PLANE_W = NF_COLS * NF_CELL_W          # 856
    NF_PLANE_H = NF_ROWS * NF_CELL_H          # 460

    NF_SPEED = 4.2                 # px per tick; one cell is ~26 ticks
    NF_PLAYER_R = 13.0

    # =========================================================================
    # THE ESCROW, CARRIED THROUGH THE TEAR
    # =========================================================================
    # The first build of act two dropped act one's one good idea at the door.
    # Act one is an escrow -- a claim is worth nothing until it is SOURCED --
    # and act two replaced that with a single bar that filled while you stood
    # somewhere. Which is a fine picture and a thin loop: go to the box, stand
    # in the box, dodge the walls. Nothing you did was ever at risk, so
    # nothing you did was ever a decision.
    #
    # SO THE ESCROW COMES WITH YOU. Standing on the entry fills PENDING, and
    # pending is not on the record. Pending is taken by a retraction, taken by
    # a redaction landing on you, and capped -- so you cannot fill the whole
    # bar in one sitting even if the page lets you. It becomes VERIFIED only
    # when you walk it into THE MARGIN, which is where a citation goes.
    #
    # The loop is now FILL, CARRY, FILE, and every part of it is exposed to a
    # different thing: filling is exposed to the volleys landing around you,
    # carrying is exposed to the page having closed behind you while you
    # stood there, and filing is exposed to which margin rows are still open.
    # And VERIFIED cannot be taken by anything, which is the act-one rule
    # ("only the ledger is real") honoured rather than restated -- it also
    # means there is no death spiral, only lost time.
    NF_VERIFY_MAX = 100.0
    # 0.100, up from 0.065, which was itself up from 0.048. The escrow adds a
    # walk to every fill, so the fill itself has to come in faster or the act
    # doubles in length -- measured, at 0.085 the naive bot ran 69-165s
    # against the old build's 48-69s, and half of that was time and half was
    # eating a retraction it could have avoided. At 0.100 a full pending is
    # 340 ticks, which fits INSIDE NF_RETRACT_EVERY: a player who starts a
    # fill on a clean clock can finish it, and only a player who starts one
    # late has a decision to make. That relationship is the tuning, not the
    # number.
    NF_FILL = 0.100                # standing still on the anchor
    NF_FILL_ATTEST = 0.200
    NF_VERIFY_FLOOR, NF_VERIFY_CEIL = 8.0, 45.0   # what act one can hand over
    # HOW MUCH YOU CAN CARRY AT ONCE. This is the whole pacing dial: raise it
    # and the act becomes two long sittings, lower it and it becomes a
    # shuttle. It is also the size of the thing a retraction can take, which
    # is the other reason it cannot be large.
    NF_PEND_MAX = 34.0

    # THE MARGIN. Column 0 of the grid, and it is not part of the maze: no
    # redaction may ever touch it (a redaction covers text, and the margin is
    # not text), the entry is never placed in it, and standing anywhere in it
    # files whatever you are carrying.
    #
    # ONE ROW AT A TIME, THOUGH. A citation is printed where it was filed and
    # the ink is wet, so that row will not take another for a while -- which
    # keeps the route from the entry to the margin from being the same walk
    # three times running.
    NF_MARGIN_COL = 0
    NF_MARGIN_REOPEN = 520
    NF_BANK_MIN = 3.0              # not worth the walk below this

    NF_HP2_MAX = 280
    # 22, down from 26. Health is now the ONLY loss condition in the act --
    # the record cannot be taken back any more, so a slow player no longer
    # bleeds out on the bar, they only lose time. Which means every death is
    # a death by redaction, and thirteen of them is a fairer number than ten
    # for a player who is still learning where the page closes.
    NF_HIT_HP = 22
    NF_HIT_PEND = 12.0             # being struck takes what is not filed yet
    # 54, up from 44. Aimed squarely at the population it exists for: it
    # changes nothing for a player who is not being hit, and it stops a player
    # who has just lost the thread from being hit twice on the way out.
    NF_IFRAMES = 54

    # CREDIT. What ATTEST costs.
    #
    # EVERY USE OF ATTEST IS OPT-IN. An earlier pass built a full-height sweep
    # that could only be answered by attesting, and then funded attesting at a
    # regen of 0.075 -- below what that sweep demanded, with the shortfall
    # only repayable through a near miss nothing on screen teaches. The result
    # was a hazard that always connected and a verb nobody could afford: the
    # act was arithmetically unwinnable for anyone not playing it perfectly.
    # The sweep is gone (see the note in _plan_volley) and the three things
    # ATTEST now does are all things you choose: fill at double rate, refuse a
    # retraction, and refuse ink on the cell you are standing in. Nothing in
    # the act REQUIRES it, so the regen only has to make it a live option.
    NF_CREDIT_MAX = 100.0
    NF_ATTEST_DRAIN = 1.35         # per held tick  (40 ticks = 54)
    NF_ATTEST_REGEN = 0.14         # per idle tick -- one attest per ~390
    NF_ATTEST_NEARMISS = 16.0      # threading a volley buys another
    NF_ATTEST_MIN = 18.0           # cannot start below this
    NF_ATTEST_MAX_TICKS = 40
    NF_ATTEST_CD = 55

    # THE PRESS. Redaction PERSISTS inside a cycle -- the floor genuinely
    # shrinks -- and then the page is re-printed and comes back whole. That
    # rhythm is the fight: pressure builds for seven seconds, snaps clean, and
    # builds again a little faster.
    #
    # AND THE CYCLE LENGTHENS. That is the difficulty ramp for the second
    # half, and it is a better one than "more marks faster" because it does
    # not touch the fairness contract at all -- NF_MIN_ROOM still caps how
    # much ink can exist, so a longer cycle means the page spends longer AT
    # that cap rather than exceeding it. It goes from a clean sheet every six
    # seconds to a clean sheet every twelve, and near the end the press stops
    # lifting everything: the oldest marks come off and the rest stay, so the
    # page is never quite blank again.
    NF_PRESS_CYCLE = 340
    NF_PRESS_CYCLE_LATE = 700
    NF_PRESS_PARTIAL_AT = 0.62     # progress past which a press only half lifts
    NF_PRESS_KEEP = 0.45           # ...and how much of it stays
    NF_VOLLEY_FAR = 96             # ticks between volleys at the start
    NF_VOLLEY_NEAR = 58            # ...and by the finish
    NF_VOLLEY_WARN = 46            # telegraph: ~2 cells of travel at NF_SPEED
    NF_VOLLEY_MARKS_FAR = 2
    NF_VOLLEY_MARKS_NEAR = 5
    # A REDACTION COVERS A PHRASE, NOT A LINE. Strikes used to take out whole
    # rows and columns, which is 20% and 12.5% of the page each, and with four
    # of them stacking inside a press cycle the board went almost entirely
    # black -- "the moving walls would always hit because they swiped past the
    # whole screen". They are contiguous runs of this many cells now, which is
    # both fairer and a much better picture of the thing they are.
    NF_SEG_LEN_H = (2, 4)
    NF_SEG_LEN_V = (2, 3)
    NF_INK_RATE = 0.14             # a strike sweeps in like a marker
    # Open cells the fairness check will not go below, of NF_COLS * NF_ROWS.
    # At 8 of 40 the guarantee was technically met and practically worthless:
    # a page that is 80% ink is one you are walled into whether or not a path
    # exists. 18 keeps the page navigable rather than merely connected.
    NF_MIN_ROOM = 18

    NF_ANCHOR_LIFE = (240, 340)
    NF_ANCHOR_MIN_DIST = 3         # cells; a new anchor is always a run away

    # THE WARNING HAS TO BE LONG ENOUGH TO RUN ON. At 60 ticks it was not:
    # the entry is placed at least NF_ANCHOR_MIN_DIST cells from wherever you
    # were, so the walk to the margin is 76-178 ticks, and a 60-tick telegraph
    # left exactly one answer to a retraction -- ATTEST -- which is rationed.
    # That is the toll this act was rebuilt once already to stop being (see
    # the note above NF_CREDIT_MAX; the sweep died of the same disease). At
    # 140 there are two ungated answers and they cost different things: hold
    # your ground and spend credit, or abandon the rest of the fill and go
    # and file what you have got. Measured: the naive bot -- fills to the cap,
    # never attests, never reacts to a telegraph -- went from 82-212s and one
    # loss in six to the figures in BALANCE.
    NF_RETRACT_EVERY = 560
    NF_RETRACT_WARN = 140
    # IT RETRACTS WHAT IS NOT SOURCED, which is the whole point of it and was
    # not what it used to do. It took a percentage of the RECORD -- chosen
    # over a flat sum because a flat drain is a treadmill (measured at a flat
    # 9, a hesitant bot took 318-536s and then died), but a percentage of the
    # record is still the wrong object: an Archivist that can take back a
    # thing you sourced contradicts the only rule act one taught. It takes
    # most of what you are CARRYING now. That cannot spiral either -- there is
    # nothing to take from a player who just filed -- and it is legible in a
    # way a percentage never was, because you can see the pile it took.
    NF_RETRACT_PEND = 0.50
    NF_RETRACT_MIN = 6.0

    NF_FACT_EVERY = 150            # ticks between readout rows appearing

    NF_HEART_ZOOM = 2.6
    # Same figure the user pulled twice on the other two: it has to look
    # wrong without becoming the busiest object on screen.
    NF_HEART_WARP = 1.15

    # --- palette: ink, paper, and exactly one colour -------------------------
    NF_INK = "#0d0d10"             # act two: ink on paper
    NF_PAPER = "#e8e6de"
    NF_PALE = "#dcded6"            # act one: light on the dark room
    NF_DIM = "#8d918a"
    NF_FAINT = "#5a5f59"
    NF_WIN = "#08080ae8"
    NF_RED = "#c2202f"             # the only colour anywhere in act two
    NF_WARN = "#c8a13c"
    NF_BLACK = "#050506"
    NF_RULE_COL = "#a9a89e"

    NF_CMDS = (("state", "STATE"), ("cite", "CITE"),
            ("amend", "AMEND"), ("run", "RUN"))

    def nf_cell_center(c, r):
        return (NF_PLANE_X + c * NF_CELL_W + NF_CELL_W * 0.5,
                NF_PLANE_Y + r * NF_CELL_H + NF_CELL_H * 0.5)

    def nf_cell_box(c, r):
        return (NF_PLANE_X + c * NF_CELL_W, NF_PLANE_Y + r * NF_CELL_H,
                NF_CELL_W, NF_CELL_H)

    # --- THE READOUT ---------------------------------------------------------
    # The corruptive state's signature: the numbers on screen stop being about
    # the person played and start being about the person playing.
    #
    # NOTHING HERE IS INVENTED. That is not a stylistic preference, it is the
    # only version of this idea that Nonfiction is allowed to do -- every row
    # is a figure the engine genuinely knows, read straight out of Matsu'Py's own
    # state, and a value that cannot be read honestly is OMITTED rather than
    # guessed at. No filesystem, no machine, no user: the game's own record.
    def nf_true_readouts(deaths=0):
        rows = []

        def add(key, value):
            if value:
                rows.append((key, value))

        try:
            rt = int(renpy.get_game_runtime())
            add("RUNTIME", "%d:%02d:%02d" % (rt // 3600, (rt // 60) % 60,
                                            rt % 60))
        except Exception:
            pass
        try:
            add("SEEN", "%d" % len(getattr(persistent, "_seen_ever", None) or {}))
        except Exception:
            pass
        try:
            add("SAVES", "%d" % len(renpy.list_saved_games(fast=True)))
        except Exception:
            pass
        try:
            add("RUNS", "%d" % int(getattr(persistent, "playthrough", 0) or 0))
        except Exception:
            pass
        try:
            losses = getattr(persistent, "inv_losses", None) or {}
            add("RETRACTED", "%d" % (int(losses.get("nonfiction", 0))
                                    + int(deaths)))
        except Exception:
            pass
        try:
            add("FENDED", "%d/%d" % (len(inv_fended()), len(INV_ARCHIVISTS)))
        except Exception:
            pass
        try:
            now = datetime.datetime.now()
            add("DATE", now.strftime("%Y-%m-%d"))
            add("LOCAL", now.strftime("%H:%M"))
        except Exception:
            pass
        try:
            info = renpy.get_renderer_info() or {}
            add("DRAWN", str(info.get("renderer", "")).upper())
        except Exception:
            pass

        return rows


# --- SIMULATION --------------------------------------------------------------
init python:
    class NFGame(object):
        """All of Nonfiction's live state, stepped at a fixed 60Hz by
        NFStage. Owns zero rendering."""

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

            # --- the party member ----------------------------------------------
            self.hp = NF_HP_MAX
            self.hp_shown = float(NF_HP_MAX)
            self.src = NF_SRC_MAX
            self.src_shown = float(NF_SRC_MAX)
            self.roll_cue = 0

            # --- the account ----------------------------------------------------
            # ledger  what you have SOURCED. Permanent. The only real number.
            # pending what you have merely STATED. It can all be taken back.
            self.ledger = 0
            self.pending = 0
            self.ledger_shown = 0.0
            self.pending_shown = 0.0
            self.scrutiny = float(NF_SCRUT_START)

            # --- act one ---------------------------------------------------------
            self.mode = "arrive"
            self.mtick = 0
            self.turn = 0
            self.cursor = 0
            self.guard = False
            self.bleed = 0
            self.marked = False
            self.last_cmd = None
            self.last_enemy = None

            self.beat_label = ""
            self.beat_value = ""
            self.beat_after = "menu"

            # --- presentation ------------------------------------------------------
            self.flash = 0.0
            self.dark = 1.0
            self.shake = 0.0
            self.freeze = 0
            self.open = 0.0            # 0 = the room, 1 = the page
            # 1.0, not 0.0: the panels start OFF the bottom of the screen
            # and slide up once the bout actually begins (see _step_ambient).
            # They used to exist from frame one and simply go undrawn during
            # the arrival, which meant they appeared whole on a single frame,
            # at the same instant the body took its place -- one pop reading as
            # two things going wrong at once.
            self.panel_slide = 1.0
            self.hit_flash = 0.0
            self.floats = []
            self.hole = [640.0, 330.0, 250.0, 0.0]
            self.emerge = 1.0
            self.press = 0.0           # the press coming down
            self.reg = 0.0             # registration seed; steps, never slides
            self.body_bars = 1.0       # how much of it is struck out
            self.body_ink = 0.0        # how much of it has been printed
            self.beat = 0.0
            self.beat_pulse = 0.0
            self.struck_out = 0        # the pile the tear takes back

            # --- act two ------------------------------------------------------------
            self.px = 640.0
            self.py = 400.0
            self.trail = []
            self.verify = 0.0
            self.verify_shown = 0.0
            self.pend2 = 0.0           # act two's escrow: filled, not filed
            self.pend2_shown = 0.0
            self.margin_cd = {}        # row -> ticks until it takes another
            self.credit = NF_CREDIT_MAX
            self.attest = 0            # ticks held so far
            self.attest_cd = 0
            self.attesting = False
            self.iframes = 0
            self.still = 0             # consecutive ticks without moving

            self.struck = {}           # (c, r) -> {"ink": 0..1, "dir": "h"/"v"}
            self.pending_lines = []    # telegraphed, not yet inked
            self.volley_t = 0
            self.volley_warn = 0
            self.press_t = NF_PRESS_CYCLE
            self.dist = 0.0            # ticks survived, for the difficulty ramp

            self.anchor = None         # (c, r)
            self.anchor_life = 0
            self.retract_t = 0
            self.retract_warn = 0

            self.facts = []
            self.facts_shown = 0
            self.fact_t = 0

            self.hud_fade = 1.0
            self.end_wipe = 0.0        # the loss: the page filling in
            self.end_bar = 0.0         # the loss: the bar drawn over you
            self.leave_bars = 0.0      # the win: the bars going across IT
            self.bank_flash = 0.0      # a citation just went into the margin

            self.keys = MSBFKeyLatch()
            self._prev = {"left": False, "right": False, "up": False,
                        "down": False, "z": False, "x": False}

            if start_open:
                # Dev entry skips the bout, so hand over a middling account --
                # a shift that never happened cannot have sourced anything.
                self.ledger = 300
                self._begin_page(dev=True)

        # ----- helpers -----------------------------------------------------------

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
            """What is left of its account of you."""
            return max(0, NF_STANDING_MAX - self.ledger - self.pending)

        def standing_frac(self):
            return inv_clamp(self.standing() / float(NF_STANDING_MAX), 0.0, 1.0)

        def scrut_frac(self):
            return inv_clamp(self.scrutiny / float(NF_SCRUT_MAX), 0.0, 1.0)

        def verify_frac(self):
            return inv_clamp(self.verify / NF_VERIFY_MAX, 0.0, 1.0)

        def progress(self):
            """0 at the tear, 1 by the time act two should be over."""
            return inv_clamp(self.dist / 5400.0, 0.0, 1.0)

        def churn(self):
            """HOW HARD THE PAGE IS BEING WORKED, 0 to 1.

            The single input to every escalating decoration in act two, and it
            is deliberately ONE number rather than a set of thresholds: the
            act should get busier the way a page gets busier, continuously and
            without a moment where a new layer switches on. Half of it is how
            long you have been on the page and half is how far onto the record
            you have got, so a slow run and a fast one both arrive at the same
            noise by the end.
            """
            return inv_clamp(0.5 * self.progress()
                            + 0.5 * (self.verify / NF_VERIFY_MAX), 0.0, 1.0)

        def pend_frac(self):
            return inv_clamp(self.pend2 / NF_PEND_MAX, 0.0, 1.0)

        def margin_open(self, r):
            """Is that row of the margin dry enough to take a citation."""
            return self.margin_cd.get(r, 0) <= 0

        def _reprint(self, strength=1.0):
            """A registration pass. Everything printed jumps at once."""
            self.press = max(self.press, inv_clamp(strength, 0.0, 1.0))
            self.reg += 1.0 + self.rng.random()

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
                col = NF_DIM if self.god else (NF_RED if self.open > 0.5
                                            else NF_WARN)
                self.float_text(x, y, "-%d" % amount, col, True)

        def bank(self):
            """Move the unsourced pile onto the ledger. The only thing in this
            fight that makes damage permanent."""
            moved = self.pending
            self.ledger = int(min(NF_STANDING_MAX, self.ledger + moved))
            self.pending = 0
            return moved

        # ----- input ---------------------------------------------------------------

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

        # ----- dispatcher ------------------------------------------------------------

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
            elif mode == "page":
                self._step_page(edges)
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
            self.press *= 0.83

            for attr, real in (("hp_shown", self.hp), ("src_shown", self.src)):
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

            # The account rolls too -- a retraction has to be watched arriving.
            for attr, real in (("ledger_shown", self.ledger),
                            ("pending_shown", self.pending)):
                shown = getattr(self, attr)
                gap = abs(shown - real)
                if gap > 0.01:
                    setattr(self, attr,
                            inv_approach(shown, float(real),
                                        inv_clamp(gap * 0.10, 0.6, 9.0)))
                else:
                    setattr(self, attr, float(real))

            gap = abs(self.verify_shown - self.verify)
            if gap > 0.005:
                self.verify_shown = inv_approach(self.verify_shown, self.verify,
                                                inv_clamp(gap * 0.12, 0.05, 1.4))
            else:
                self.verify_shown = self.verify

            # The escrow rolls too, and a bit faster -- a retraction taking it
            # has to be watched arriving, but a filing should feel like a
            # decision landing rather than a needle drifting.
            gap = abs(self.pend2_shown - self.pend2)
            if gap > 0.005:
                self.pend2_shown = inv_approach(self.pend2_shown, self.pend2,
                                                inv_clamp(gap * 0.18, 0.05, 2.2))
            else:
                self.pend2_shown = self.pend2
            self.bank_flash *= 0.90

            for f in self.floats:
                f["y"] += f["vy"]
                f["vy"] += 0.055
                f["life"] -= 1
            self.floats = [f for f in self.floats if f["life"] > 0]

            if self.hp_shown <= 0.0 and self.mode not in ("leave_w", "leave_l",
                                                        "arrive"):
                self._begin_leave(False)

        # =====================================================================
        # ARRIVAL -- it does not climb out, it is PRINTED
        # =====================================================================

        def _step_arrive(self):
            self.mtick += 1
            t = self.mtick
            self.dark = inv_clamp(1.0 - t / 30.0, 0.0, 1.0)

            if t == 6:
                self.play("tear", 0.75)
            if t < 70:
                self.hole[3] = inv_smooth(t / 70.0)
                self.hole[2] = inv_lerp(40.0, 250.0, inv_smooth(t / 70.0))
                self.body_bars = 1.0
                self.body_ink = 0.0
            elif t < 220:
                # THREE PASSES. Nothing moves between them; each one simply has
                # more of it on the page than the one before.
                self.hole[3] = 1.0
                self.emerge = 1.0 - inv_clamp((t - 70) / 150.0, 0.0, 1.0)
                if t in (74, 124, 174):
                    self._reprint(1.0)
                    self.play("phase", 0.55)
                    self.flash = 0.30
                    self.shake = 0.35
                step_i = 0 if t < 124 else (1 if t < 174 else 2)
                self.body_bars = (0.82, 0.52, 0.16)[step_i]
                self.body_ink = (0.35, 0.72, 1.0)[step_i]
            elif t < 275:
                u = (t - 220) / 55.0
                self.emerge = 0.0
                self.body_bars = inv_lerp(0.16, 0.0, inv_smooth(u))
                self.body_ink = 1.0
                self.hole[3] = 1.0 - inv_smooth(u)
                self.hole[2] = inv_lerp(250.0, 30.0, inv_smooth(u))
            elif t == 275:
                self.hole[3] = 0.0
                self.body_bars = 0.0
                inv_music_survey()
            elif t >= 310:
                self._begin_player_turn()

        # =====================================================================
        # ACT ONE -- THE SOURCING BOUT
        # =====================================================================

        def _begin_player_turn(self):
            self.mode = "menu"
            self.mtick = 0
            self.turn += 1
            self.cursor = 0
            self.guard = False

        def _step_menu(self, edges):
            self.mtick += 1
            n = len(NF_CMDS)
            if edges["up"]:
                self.cursor = (self.cursor - 1) % n
                self.play("cursor")
            elif edges["down"]:
                self.cursor = (self.cursor + 1) % n
                self.play("cursor")
            if edges["z"]:
                self.play("confirm")
                self._resolve_player(NF_CMDS[self.cursor][0])

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

            if cmd == "state":
                claim = self.rng.randint(NF_STATE_LO, NF_STATE_HI)
                room = max(0, NF_STANDING_MAX - self.ledger - self.pending)
                claim = min(claim, room)
                self.pending += claim
                self.scrutiny = min(float(NF_SCRUT_MAX),
                                    self.scrutiny + NF_STATE_SCRUT)
                self.play("bash")
                self.shake = 0.30
                self._reprint(0.45)
                value = "-" + str(claim) + " UNSOURCED"

            elif cmd == "cite":
                if self.src < NF_CITE_COST:
                    self.play("cancel")
                    self._beat("CITE", "NO SOURCES", "menu")
                    return
                if self.pending <= 0:
                    self.play("cancel")
                    self._beat("CITE", "UNSOURCED  0", "menu")
                    return
                self.src -= NF_CITE_COST
                moved = self.bank()
                self.scrutiny = max(0.0, self.scrutiny - NF_CITE_SCRUT)
                self.play("scan")
                self.flash = 0.45
                self._reprint(0.8)
                value = "-" + str(moved)

            elif cmd == "amend":
                # The honest move, and honesty costs. You take back a third of
                # everything you have not sourced yet, and in exchange you get
                # the turn off, the health, the sources and the quiet.
                given = int(self.pending * NF_AMEND_PENDING)
                self.pending = max(0, self.pending - given)
                self.hp = int(min(NF_HP_MAX, self.hp + NF_AMEND_HEAL))
                self.src = int(min(NF_SRC_MAX, self.src + NF_AMEND_SRC))
                self.scrutiny = max(0.0, self.scrutiny - NF_AMEND_SCRUT)
                self.guard = True
                self.play("heal")
                value = "+" + str(NF_AMEND_HEAL)
                if given:
                    value += "   +" + str(given) + " UNSOURCED"

            elif cmd == "run":
                # It never works, and it is never explained.
                self.play("miss")
                value = "UNRECORDED"

            after = "enemy"
            if self.ledger >= NF_SHIFT_LEDGER:
                after = "shift"
            self._beat(label, value, after)

        def _pick_enemy_move(self):
            if self.marked:
                return "strike"
            pool = ["query", "query", "footnote"]
            if self.pending >= 90:
                pool.append("mark")
                pool.append("mark")
            elif self.turn >= 3:
                pool.append("mark")
            if self.standing_frac() < 0.70:
                pool.append("corroborate")
            if self.last_enemy in pool and len(set(pool)) > 1:
                pool = [m for m in pool if m != self.last_enemy] or pool
            return self.rng.choice(pool)

        def _step_enemy(self):
            self.mtick += 1
            if self.mtick < 26:
                return

            self.scrutiny = min(float(NF_SCRUT_MAX),
                                self.scrutiny + self.rng.randint(
                                    NF_SCRUT_STEP_LO, NF_SCRUT_STEP_HI))

            # THE CAPSTONE. Scrutiny full: it does not merely erase what you
            # never sourced, it corrects something you did.
            if self.scrutiny >= NF_SCRUT_MAX:
                self.scrutiny = float(NF_SCRUT_FLOOR)
                lost = self.pending
                self.pending = 0
                back = min(self.ledger, NF_ERRATUM_LEDGER)
                self.ledger -= back
                self.marked = False
                self.last_enemy = "erratum"
                self.play("break", 0.95)
                self.flash = 0.75
                self.shake = 1.0
                self._reprint(1.0)
                dmg = NF_ERRATUM_DMG
                if self.guard:
                    dmg = int(dmg * NF_GUARD_MULT)
                self.hurt(dmg, 640, 470)
                self.guard = False
                value = "+" + str(back)
                if lost:
                    value += "   +" + str(lost) + " UNSOURCED"
                self._beat("ERRATUM", value, self._after_enemy())
                return

            move = self._pick_enemy_move()
            self.last_enemy = move
            label = move.upper()
            value = ""
            dmg = 0

            if move == "query":
                # Carrying a pile is what makes this hurt.
                dmg = int(NF_QUERY_BASE + NF_QUERY_PER_PENDING * self.pending)
            elif move == "footnote":
                dmg = NF_FOOTNOTE_DMG
                self.bleed = NF_FOOTNOTE_BLEED
            elif move == "mark":
                # It says so a full turn in advance, because it always does.
                self.marked = True
                self.play("note", 0.9)
                self._reprint(0.5)
                value = "MARKED"
            elif move == "strike":
                lost = self.pending
                self.pending = 0
                self.marked = False
                dmg = NF_STRIKE_DMG
                self.play("cut_big", 0.9)
                self.flash = 0.55
                self.shake = 0.8
                self._reprint(1.0)
                if lost:
                    value = "+" + str(lost) + " UNSOURCED   "
            elif move == "corroborate":
                back = min(self.ledger, NF_CORROBORATE)
                self.ledger -= back
                label = "CORRECTION"
                self.play("refuse", 0.7)
                value = "+" + str(back)

            if dmg > 0:
                if self.guard:
                    dmg = int(dmg * NF_GUARD_MULT)
                self.play("enemy", 0.8)
                self.hurt(dmg, 640, 470)
                value += "-" + str(dmg)

            if self.bleed > 0 and move != "footnote":
                self.bleed -= 1
                self.hurt(11, 640, 500)
                value += "   -11"

            self.guard = False
            self._beat(label, value, self._after_enemy())

        def _after_enemy(self):
            if self.ledger >= NF_SHIFT_LEDGER or self.turn >= NF_SHIFT_TURN_CAP:
                return "shift"
            return "menu"

        # =====================================================================
        # THE TEAR -- the unsourced pile is struck out and the room whitens
        # =====================================================================

        def _step_shift(self):
            self.mtick += 1
            t = self.mtick

            if t == 1:
                inv_music_stop(0.3)
                self.play("tear")
                # THE LESSON, ADMINISTERED ONCE. Everything still unsourced
                # goes, in front of you, before anything else happens.
                self.struck_out = self.pending
            if t == 30 and self.struck_out:
                self.pending = 0
                self.play("cut_big", 0.9)
                self.flash = 0.5
                self.shake = 0.9
                self._reprint(1.0)
                self.float_text(640, 300, "+" + str(self.struck_out)
                                + " UNSOURCED", NF_WARN, True)
            if 60 <= t < 150:
                self.panel_slide = inv_smooth((t - 60) / 90.0)
                self.shake = max(self.shake, 0.3)
            if t == 150:
                self.play("slam")
                self.play("phase", 0.9)
                self.flash = 1.0
                self.shake = 1.0
                self._reprint(1.0)
                inv_music_corruptive()
                # Whole again for the second half: act one's currency was the
                # LEDGER, and that is what carries.
                self.hp = NF_HP2_MAX
                self.src = NF_SRC_MAX
            if 150 <= t < 230:
                # Every light in the room coming up at once.
                self.open = inv_clamp((t - 150) / 80.0, 0.0, 1.0)
            if t == 230:
                self.open = 1.0
                self._begin_page()

        # =====================================================================
        # ACT TWO -- THE PAGE
        # =====================================================================

        def _begin_page(self, dev=False):
            self.mode = "page"
            self.mtick = 0
            self.open = 1.0
            self.dark = 0.0
            self.hp = NF_HP2_MAX
            self.hp_shown = float(NF_HP2_MAX)

            # THE JOINT: what you sourced is what you start with on record.
            # It arrives as VERIFIED, not as pending: it was sourced in act
            # one, and a sourced thing is already on the record.
            self.verify = inv_clamp(
                NF_VERIFY_CEIL * (self.ledger / float(NF_SHIFT_LEDGER)),
                NF_VERIFY_FLOOR, NF_VERIFY_CEIL)
            self.verify_shown = self.verify
            self.pend2 = 0.0
            self.pend2_shown = 0.0
            self.margin_cd = {}

            self.credit = NF_CREDIT_MAX
            self.attest = 0
            self.attest_cd = 0
            self.attesting = False
            self.iframes = 0
            self.still = 0
            self.dist = 0.0

            self.px, self.py = nf_cell_center(NF_COLS // 2, NF_ROWS // 2)
            self.bank_flash = 0.0
            self.trail = []
            self.struck = {}
            self.pending_lines = []
            self.volley_t = 120
            self.volley_warn = 0
            self.press_t = NF_PRESS_CYCLE
            self.retract_t = NF_RETRACT_EVERY
            self.retract_warn = 0

            self.facts = nf_true_readouts(self.deaths)
            self.facts_shown = 0
            self.fact_t = NF_FACT_EVERY

            self._place_anchor(first=True)
            self.play("break", 0.8)
            if dev:
                inv_music_corruptive()

        # ----- the grid ------------------------------------------------------------

        def cell_of(self, x, y):
            c = int((x - NF_PLANE_X) // NF_CELL_W)
            r = int((y - NF_PLANE_Y) // NF_CELL_H)
            return (int(inv_clamp(c, 0, NF_COLS - 1)),
                    int(inv_clamp(r, 0, NF_ROWS - 1)))

        def _protected(self):
            """Cells no redaction may ever touch.

            THE MARGIN, first and unconditionally: a redaction covers text,
            and the margin is not text. That is the fiction and it is also the
            fairness rule that makes the escrow safe to build on -- the place
            you file a citation can never be inked out from under you, and
            since the margin runs the full height of the page there is always
            a way to reach it from anywhere the flood fill allows.

            And then the anchor and its four neighbours, as before: there is
            always somewhere to stand."""
            out = set((NF_MARGIN_COL, r) for r in range(NF_ROWS))
            if self.anchor is None:
                return out
            c, r = self.anchor
            out.add((c, r))
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c + dc, r + dr)
                if 0 <= n[0] < NF_COLS and 0 <= n[1] < NF_ROWS:
                    out.add(n)
            return out

        def _component(self, start, blocked):
            """Flood fill of open cells reachable from `start`. This is the
            whole fairness contract: nothing is committed until this says the
            page is still a place you can move around in."""
            if start in blocked:
                return set()
            seen = set([start])
            stack = [start]
            while stack:
                c, r = stack.pop()
                for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (c + dc, r + dr)
                    if not (0 <= n[0] < NF_COLS and 0 <= n[1] < NF_ROWS):
                        continue
                    if n in seen or n in blocked:
                        continue
                    seen.add(n)
                    stack.append(n)
            return seen

        def _roll_mark(self):
            """One redaction: a contiguous run of cells, horizontal or
            vertical. Never a whole row, never a whole column, and never in
            the margin -- rolling one there would only be filtered out again
            and would quietly eat a try off the budget in _plan_volley."""
            first = NF_MARGIN_COL + 1
            if self.rng.random() < 0.62:
                n = self.rng.randint(*NF_SEG_LEN_H)
                c0 = self.rng.randint(first, max(first, NF_COLS - n))
                r = self.rng.randrange(NF_ROWS)
                return ("h", set((c0 + i, r) for i in range(n)))
            n = self.rng.randint(*NF_SEG_LEN_V)
            r0 = self.rng.randint(0, max(0, NF_ROWS - n))
            c = self.rng.randrange(first, NF_COLS)
            return ("v", set((c, r0 + i) for i in range(n)))

        def _margin_in(self, comp):
            """Does this open component actually touch the margin.

            The margin can never be inked, but it CAN be walled off -- five
            marks down column 1 and the filing strip is on the other side of
            the page from you, which is not a hard fight, it is a stalled one.
            Nothing commits ink without this returning True."""
            return any((NF_MARGIN_COL, r) in comp for r in range(NF_ROWS))

        def _place_anchor(self, first=False):
            """Somewhere corroborated, and never where you already are.

            THE HARD PART IS NOT PICKING A CELL, IT IS GUARANTEEING YOU CAN
            REACH IT. Dropping the anchor into a pocket the player happens to
            be walled out of makes the whole fight unwinnable in complete
            silence -- there is no death, no message, just a run that can
            never end. So it is chosen out of the player's OWN open component,
            and then ink is LIFTED off the edge of that component until there
            is enough page around it to fight in. Which is also the fiction:
            the sheet is re-set around a corroborated fact, and as much of the
            sheet as that takes."""
            blocked = set(self.struck.keys())
            pc = self.cell_of(self.px, self.py)
            reach = self._component(pc, blocked)
            if not reach:
                self.struck.pop(pc, None)
                reach = set([pc])

            # NEVER IN THE MARGIN. The margin is where a citation is filed,
            # not where a claim is made, and an entry sitting in it would
            # collapse the whole loop into standing in one cell again.
            reach = set(cell for cell in reach if cell[0] != NF_MARGIN_COL)
            if not reach:
                reach = set([pc]) if pc[0] != NF_MARGIN_COL else \
                    set([(NF_MARGIN_COL + 1, pc[1])])

            far = [cell for cell in reach
                if max(abs(cell[0] - pc[0]), abs(cell[1] - pc[1]))
                >= NF_ANCHOR_MIN_DIST]
            if first:
                pool = sorted(reach)
            else:
                pool = far or sorted(reach - set([pc])) or sorted(reach)
            self.anchor = self.rng.choice(sorted(pool))
            self.anchor_life = self.rng.randint(*NF_ANCHOR_LIFE)

            # The neighbourhood of a corroborated fact is never struck...
            for cell in self._protected():
                self.struck.pop(cell, None)

            # ...and neither is enough of the page around it to move in, NOR
            # the route out to the margin. Both conditions lift ink off the
            # edge of the component until they hold.
            guard = 0
            while guard < NF_COLS * NF_ROWS:
                guard += 1
                comp = self._component(self.anchor, set(self.struck.keys()))
                if len(comp) >= NF_MIN_ROOM and self._margin_in(comp):
                    break
                edge = [cell for cell in self.struck
                        if any((cell[0] + dc, cell[1] + dr) in comp
                            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
                if not edge:
                    break
                self.struck.pop(self.rng.choice(sorted(edge)), None)

            # A telegraph aimed at what is now protected ground is dropped.
            prot = self._protected()
            for line in self.pending_lines:
                line["cells"] = [x for x in line["cells"] if x not in prot]
            self.pending_lines = [l for l in self.pending_lines if l["cells"]]
            self.play("note", 0.55)

        # ----- redaction -----------------------------------------------------------

        def _plan_volley(self):
            """Choose the marks to strike, refusing any that would seal the
            page.

            THE ONLY HAZARD IN THIS ACT IS THE PAGE CLOSING. There was a
            full-height rule sweeping across as well, and it was cut: it
            spanned the whole frame, so it could not be walked around, which
            left exactly one answer to it, and that answer was rationed. A
            hazard with a single gated answer is not difficulty, it is a
            toll. Everything here is dodgeable on foot.

            Refusal is silent and deliberate: a quiet volley is a better
            failure than an impossible one."""
            prog = self.churn()
            want = int(round(inv_lerp(NF_VOLLEY_MARKS_FAR,
                                    NF_VOLLEY_MARKS_NEAR, prog)))
            prot = self._protected()
            blocked = set(self.struck.keys())
            pc = self.cell_of(self.px, self.py)

            accepted = []
            tries = 0
            while len(accepted) < want and tries < 24:
                tries += 1
                direction, cells = self._roll_mark()
                cells = cells - prot - blocked
                if not cells:
                    continue
                trial = blocked | cells
                anchor_comp = self._component(self.anchor, trial)
                if len(anchor_comp) < NF_MIN_ROOM:
                    continue
                if not self._margin_in(anchor_comp):
                    continue
                if pc in cells:
                    # It may land on you -- you get ejected -- but only if
                    # there is somewhere in the anchor's component to be
                    # ejected TO.
                    if not any((pc[0] + dc, pc[1] + dr) in anchor_comp
                            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        continue
                elif pc not in anchor_comp:
                    continue
                blocked = trial
                accepted.append({"dir": direction, "cells": sorted(cells)})

            if not accepted:
                return
            self.pending_lines = accepted
            self.volley_warn = NF_VOLLEY_WARN
            self.play("wind", 0.45)

        def _commit_volley(self):
            """Ink everything telegraphed, hit whoever is standing in it, and
            re-check the page one last time."""
            # ATTEST REFUSES INK ON THE CELL YOU ARE STANDING IN. You are on
            # record for as long as you can back it, and a redaction cannot
            # cover something that is on record.
            here_now = self.cell_of(self.px, self.py)
            spared = here_now if self.attesting else None
            if spared is not None:
                self.play("refuse", 0.6)

            order = []
            for line in self.pending_lines:
                direction = line["dir"]
                for cell in line["cells"]:
                    if cell in self._protected() or cell == spared:
                        continue
                    self.struck[cell] = {"ink": 0.0, "dir": direction}
                    order.append(cell)
            self.pending_lines = []
            if not order:
                return

            self.play("cut", 0.7)
            self._reprint(0.55)
            self.shake = max(self.shake, 0.25)

            # LAST-RESORT RE-CHECK. You had NF_VOLLEY_WARN ticks to move and
            # may have moved somewhere the plan did not expect, so the whole
            # contract is proved again against the real board rather than the
            # predicted one: the anchor's open component has to be big enough
            # to fight in, and you have to be in it (or standing in ink, which
            # ejects you into it). The newest lines lift until both hold.
            guard = 0
            while order and guard < 12:
                guard += 1
                blocked = set(self.struck.keys())
                comp = self._component(self.anchor, blocked)
                here = self.cell_of(self.px, self.py)
                if (len(comp) >= NF_MIN_ROOM and self._margin_in(comp)
                        and (here in comp or here in blocked)):
                    break
                self.struck.pop(order.pop(), None)

            here = self.cell_of(self.px, self.py)
            if here in self.struck:
                self._struck_by_ink()
                return

            # THE SKILL CURVE, and it is paid at the moment it is earned: ink
            # landing in a cell NEXT to you buys back the credit that
            # attesting costs. A player who threads a volley can afford to
            # stand still when it counts; one who retreats to the emptiest
            # corner of the page cannot.
            close = 0
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if (here[0] + dc, here[1] + dr) in self.struck:
                    close += 1
            if close:
                self.credit = min(NF_CREDIT_MAX,
                                self.credit + NF_ATTEST_NEARMISS
                                * min(close, 2))
                self.play("graze", 0.5)

        def _struck_by_ink(self):
            """A redaction landed on the cell you were standing in."""
            if self.iframes > 0:
                return
            self._eject()
            self._take_hit(NF_HIT_HP)

        def _eject(self):
            """Redaction pushes you out of the text. It does not bury you."""
            blocked = set(self.struck.keys())
            comp = self._component(self.anchor, blocked) if self.anchor else set()
            pc = self.cell_of(self.px, self.py)
            best = None
            best_d = None
            for c in range(NF_COLS):
                for r in range(NF_ROWS):
                    if (c, r) in blocked:
                        continue
                    d = abs(c - pc[0]) + abs(r - pc[1])
                    if (c, r) not in comp:
                        d += 100          # prefer the anchor's side of the page
                    if best_d is None or d < best_d:
                        best_d = d
                        best = (c, r)
            if best is not None:
                self.px, self.py = nf_cell_center(*best)
                self.trail = []

        def _take_hit(self, amount):
            self.hurt(amount, self.px, self.py - 34)
            # It does not only cost health -- but what it takes is the
            # unsourced pile, same as everything else in this fight.
            before = self.pend2
            self.pend2 = max(0.0, self.pend2 - NF_HIT_PEND)
            if self.pend2 < before:
                self.float_text(self.px, self.py - 62,
                                "-%d" % int(before - self.pend2), NF_INK)
            self.iframes = NF_IFRAMES
            self.freeze = 4
            self.play("struck", 0.75)

        # ----- the page's turn ------------------------------------------------------

        def _step_page(self, edges):
            self.mtick += 1
            self.dist += 1.0
            if self.freeze > 0:
                self.freeze -= 1
                return

            held = edges["held"]
            if self.iframes > 0:
                self.iframes -= 1

            # --- ATTEST ----------------------------------------------------------
            # The only verb. It roots you, it makes you unstrikeable, it fills
            # twice as fast, and it is the only answer to the rule and the only
            # refusal of a retraction. It costs CREDIT, and credit is bought by
            # dodging on your feet.
            if self.attest_cd > 0:
                self.attest_cd -= 1
            want = bool(held["z"]) and self.attest_cd <= 0
            if self.attesting:
                if (not want or self.credit <= 0.0
                        or self.attest >= NF_ATTEST_MAX_TICKS):
                    self.attesting = False
                    self.attest = 0
                    self.attest_cd = NF_ATTEST_CD
                else:
                    self.attest += 1
                    self.credit = max(0.0, self.credit - NF_ATTEST_DRAIN)
            elif want and self.credit >= NF_ATTEST_MIN:
                self.attesting = True
                self.attest = 0
                self.play("guard", 0.6)
            if not self.attesting:
                self.credit = min(NF_CREDIT_MAX, self.credit + NF_ATTEST_REGEN)

            # --- moving ---------------------------------------------------------
            dx = ((1.0 if held["right"] else 0.0)
                - (1.0 if held["left"] else 0.0))
            dy = ((1.0 if held["down"] else 0.0)
                - (1.0 if held["up"] else 0.0))
            if self.attesting:
                dx = dy = 0.0
            if dx and dy:
                dx *= 0.7071
                dy *= 0.7071

            moved = False
            if dx or dy:
                moved = self._move(dx * NF_SPEED, dy * NF_SPEED)
            self.still = 0 if moved else self.still + 1

            self.trail.insert(0, (self.px, self.py))
            if len(self.trail) > 9:
                self.trail.pop()

            # --- MAKING A CLAIM ----------------------------------------------------
            # Standing still on the entry fills PENDING, and pending is not on
            # the record. It stops dead at the cap: the page will not let you
            # sit in one cell and win, which is the thing the first build of
            # this act allowed and the reason it only had one decision in it.
            here_cell = self.cell_of(self.px, self.py)
            on_anchor = (self.anchor is not None and here_cell == self.anchor)
            filling = (on_anchor and (self.attesting or self.still > 4)
                    and self.pend2 < NF_PEND_MAX)
            if filling:
                rate = NF_FILL_ATTEST if self.attesting else NF_FILL
                self.pend2 = min(NF_PEND_MAX, self.pend2 + rate)
                if self.tick % 16 == 0:
                    self.play("tick", 0.30)

            # --- FILING IT ----------------------------------------------------------
            # A citation goes in the margin. Walk what you are carrying into
            # column zero and it stops being takeable -- and the row you filed
            # it on will not take another until the ink is dry, so the walk is
            # a different walk every time.
            if (here_cell[0] == NF_MARGIN_COL and self.pend2 >= NF_BANK_MIN
                    and self.margin_open(here_cell[1])):
                self._file(here_cell[1])

            if self.verify >= NF_VERIFY_MAX:
                self._begin_leave(True)
                return

            self._step_anchor()
            self._step_margin()
            self._step_press()
            self._step_facts()

        def _file(self, row):
            """The escrow closes. Whatever you were carrying becomes VERIFIED,
            and nothing in the encounter can take it back afterwards."""
            moved = self.pend2
            self.verify = min(NF_VERIFY_MAX, self.verify + moved)
            self.pend2 = 0.0
            self.margin_cd[row] = NF_MARGIN_REOPEN
            self.bank_flash = 1.0
            self.flash = max(self.flash, 0.22)
            self._reprint(0.5)
            self.play("confirm", 0.7)
            cx, cy = nf_cell_center(NF_MARGIN_COL, row)
            self.float_text(cx, cy - 30, "+%d" % int(moved), NF_INK, True)

        def _step_margin(self):
            for r in list(self.margin_cd.keys()):
                if self.margin_cd[r] > 0:
                    self.margin_cd[r] -= 1

        def _move(self, mx, my):
            """Ink is solid. Axis-separated so you slide along a redaction
            instead of sticking to it."""
            moved = False
            x0 = NF_PLANE_X + NF_PLAYER_R
            x1 = NF_PLANE_X + NF_PLANE_W - NF_PLAYER_R
            y0 = NF_PLANE_Y + NF_PLAYER_R
            y1 = NF_PLANE_Y + NF_PLANE_H - NF_PLAYER_R

            if mx:
                nx = inv_clamp(self.px + mx, x0, x1)
                if self.cell_of(nx, self.py) not in self.struck:
                    if nx != self.px:
                        moved = True
                    self.px = nx
            if my:
                ny = inv_clamp(self.py + my, y0, y1)
                if self.cell_of(self.px, ny) not in self.struck:
                    if ny != self.py:
                        moved = True
                    self.py = ny
            return moved

        def _step_anchor(self):
            self.anchor_life -= 1
            if self.anchor_life <= 0:
                self._place_anchor()

            # RETRACTION. It takes back the thing it granted -- unless you are
            # standing on it saying otherwise.
            if self.retract_warn > 0:
                self.retract_warn -= 1
                if self.retract_warn == 0:
                    if self.attesting:
                        self.play("refuse", 0.85)
                        self.flash = 0.30
                        self.float_text(self.px, self.py - 62, "REFUSED",
                                        NF_INK)
                    else:
                        # IT TAKES WHAT IS NOT SOURCED. Never the record --
                        # the record is the one thing in either act that is
                        # real, and an Archivist that can un-file a citation
                        # is contradicting the rule act one spent eighteen
                        # turns teaching. If you are carrying nothing it does
                        # nothing, and that is correct: it is not a punishment
                        # for existing, it is a reason to file.
                        before = self.pend2
                        take = max(NF_RETRACT_MIN,
                                self.pend2 * NF_RETRACT_PEND)
                        self.pend2 = max(0.0, self.pend2 - take)
                        self.play("cut_big", 0.75)
                        self.shake = max(self.shake, 0.5)
                        self._reprint(0.7)
                        if before > 0.0:
                            cx, cy = nf_cell_center(*self.anchor)
                            self.float_text(cx, cy - 30,
                                            "-%d" % int(before - self.pend2),
                                            NF_INK, True)
                        self._place_anchor()
                    self.retract_t = NF_RETRACT_EVERY + self.rng.randint(-90, 90)
            else:
                self.retract_t -= 1
                if self.retract_t <= 0:
                    self.retract_warn = NF_RETRACT_WARN
                    self.play("wind2", 0.7)

        def _step_press(self):
            """Ink is applied and it STAYS. The floor genuinely shrinks across
            a cycle, and then the page is re-printed and comes back whole."""
            for cell, data in self.struck.items():
                if data["ink"] < 1.0:
                    data["ink"] = min(1.0, data["ink"] + NF_INK_RATE)

            if self.volley_warn > 0:
                self.volley_warn -= 1
                if self.volley_warn == 0:
                    self._commit_volley()
                    prog = self.churn()
                    self.volley_t = int(inv_lerp(NF_VOLLEY_FAR, NF_VOLLEY_NEAR,
                                                prog)) + self.rng.randint(-8, 12)
                return

            self.volley_t -= 1
            if self.volley_t <= 0:
                self._plan_volley()
                if not self.pending_lines:
                    self.volley_t = 40

            self.press_t -= 1
            if self.press_t <= 0:
                # CHURN, NOT THE CLOCK. Driving the escalation off elapsed
                # time alone rebuilds the treadmill this act was fixed for
                # once already, just in a new costume: a player who is
                # struggling takes longer, and taking longer was making the
                # page permanently worse, which made them struggle. churn()
                # is half clock and half RECORD, so the page gets harder as
                # you get further onto it and a stuck player is left fighting
                # a page they can actually still fight.
                prog = self.churn()
                self.press_t = int(inv_lerp(NF_PRESS_CYCLE,
                                            NF_PRESS_CYCLE_LATE, prog))
                if self.struck:
                    # THE PRESS COMES DOWN. Everything struck lifts at once and
                    # the sheet is whole again for exactly as long as it takes
                    # to start filling in.
                    #
                    # LATE ON IT STOPS LIFTING EVERYTHING. The oldest marks
                    # come off and the newest stay, so the sheet is never
                    # quite blank again and the last third of the act is
                    # fought on a page that has been worked over. Ordering by
                    # ink is ordering by age -- a mark that has finished
                    # sweeping in has been there longest.
                    if prog >= NF_PRESS_PARTIAL_AT:
                        keep_n = int(len(self.struck) * NF_PRESS_KEEP)
                        newest = sorted(self.struck.items(),
                                        key=lambda kv: kv[1]["ink"])[:keep_n]
                        self.struck = dict(newest)
                        # The contract is re-proved against what is left, the
                        # same as anywhere else ink survives a decision.
                        guard = 0
                        while self.struck and guard < NF_COLS * NF_ROWS:
                            guard += 1
                            comp = self._component(self.anchor,
                                                set(self.struck.keys())) \
                                if self.anchor else set()
                            if (len(comp) >= NF_MIN_ROOM
                                    and self._margin_in(comp)):
                                break
                            self.struck.pop(
                                sorted(self.struck.keys())[0], None)
                    else:
                        self.struck = {}
                    self.play("slam", 0.6)
                    self.flash = 0.28
                self._reprint(1.0)

        def _step_facts(self):
            if self.facts_shown >= len(self.facts):
                return
            self.fact_t -= 1
            if self.fact_t <= 0:
                self.fact_t = NF_FACT_EVERY
                self.facts_shown += 1
                self.play("tick", 0.45)

        # =====================================================================
        # DEPARTURE
        # =====================================================================

        def _begin_leave(self, won):
            self.mode = "leave_w" if won else "leave_l"
            self.mtick = 0
            self.pending_lines = []
            self.retract_warn = 0
            self.shake = 0.0
            self.attesting = False
            self.hud_fade = 1.0
            self.end_wipe = 0.0
            self.end_bar = 0.0
            self.leave_bars = 0.0
            inv_music_stop(3.0 if won else 1.8)
            # No sting either way. A victory chime would be the funniest thing
            # in the encounter.

        def _step_leave(self):
            """Neither ending is a spectacle.

            WON -- you are on record, and a thing that is on record cannot be
            taken back. So it stops. Every redaction on the page LIFTS, the
            sheet comes back whole, and then the bars go across IT instead: it
            files itself as unverifiable, in the same three passes it arrived
            in, and the hole takes what is left.

            LOST -- you are not killed. You are RETRACTED. The page keeps
            being struck out, cell by cell, in order, at the same unhurried
            rate it has used all along, until there is nothing left of it but
            ink -- and the last thing struck out is you. Then the sheet is
            blank, and nothing happens for a long time.
            """
            self.mtick += 1
            t = self.mtick
            won = (self.mode == "leave_w")

            if won:
                # THE PRESS TURNS ON THE THING THAT HAS BEEN OPERATING IT.
                #
                # Nonfiction does not die and it is not beaten off -- it is
                # PROCESSED, by exactly the apparatus it spent the whole
                # encounter pointing at you. Every beat below is a thing this
                # fight has already done TO the player, done back, at full
                # volume:
                #
                #   0-56     THE SHEET COMES BACK WHOLE. Every redaction on
                #            the page lifts at once and the room goes blank.
                #   56-206   THREE IMPRESSIONS, and the press slamming is the
                #            loudest thing in the encounter. Less of it is
                #            present after each one.
                #   206-268  ERRATUM. The entire page is struck out around it,
                #            in reading order, at the same unhurried rate it
                #            used on you -- and then lifted, leaving only it.
                #   268-338  IT IS REDACTED. The bars close over it until it is
                #            one solid rectangle, and then the rectangle is
                #            lifted too, and there is nothing underneath.
                #   338+     A blank sheet. Held.
                if t < 56:
                    for cell in list(self.struck.keys()):
                        data = self.struck[cell]
                        data["ink"] = max(0.0, data["ink"] - 0.055)
                        if data["ink"] <= 0.0:
                            self.struck.pop(cell, None)
                    self.hud_fade = max(0.0, 1.0 - t / 56.0)
                    if t == 54:
                        self._reprint(0.5)

                elif t < 206:
                    # Three impressions. Each one is a real slam rather than a
                    # registration tick: the room inverts, the sheet jumps, and
                    # more of it is gone when the platen comes back up.
                    if t in (58, 108, 158):
                        self._reprint(1.0)
                        self.play("slam", 0.95)
                        self.play("phase", 0.75)
                        self.flash = 0.85
                        self.shake = 1.0
                    step_i = 0 if t < 108 else (1 if t < 158 else 2)
                    since = t - (58, 108, 158)[step_i]
                    # It is taken in a HARD STEP on the impression and then
                    # eaten a little further while the platen is down, so the
                    # bars are not a smooth ramp -- a press is not smooth.
                    base = (0.34, 0.66, 0.92)[step_i]
                    self.leave_bars = base + 0.05 * inv_clamp(since / 44.0,
                                                            0.0, 1.0)
                    if since < 8:
                        self.press = max(self.press, 1.0 - since / 8.0)

                elif t < 268:
                    # ERRATUM, and it is administered to the page rather than
                    # to you for the first and only time.
                    u = (t - 206) / 62.0
                    if t == 206:
                        self.play("break", 0.9)
                        self.flash = 0.4
                        self._reprint(1.0)
                    target = int(u * NF_COLS * NF_ROWS)
                    idx = 0
                    for r in range(NF_ROWS):
                        for c in range(NF_COLS):
                            if idx >= target:
                                break
                            if (c, r) not in self.struck:
                                self.struck[(c, r)] = {"ink": 0.0, "dir": "h"}
                                if idx % 5 == 0:
                                    self.play("text", 0.5)
                            idx += 1
                        if idx >= target:
                            break
                    for data in self.struck.values():
                        data["ink"] = min(1.0, data["ink"] + NF_INK_RATE * 1.5)
                    self.leave_bars = 0.97

                elif t < 338:
                    u = inv_smooth((t - 268) / 70.0)
                    if t == 268:
                        self.play("cut_big", 0.95)
                        self._reprint(1.0)
                        self.flash = 0.5
                        self.shake = 0.8
                    # The page is lifted back off around it...
                    for cell in list(self.struck.keys()):
                        data = self.struck[cell]
                        data["ink"] = max(0.0, data["ink"] - 0.030)
                        if data["ink"] <= 0.0:
                            self.struck.pop(cell, None)
                    # ...leaving one solid rectangle where it was standing, and
                    # then that is lifted too.
                    self.leave_bars = inv_lerp(0.97, 1.0, u)
                    self.hole[0] = 640.0
                    self.hole[1] = 330.0
                    self.hole[3] = 1.0 - abs(u - 0.5) * 2.0
                    self.hole[2] = inv_lerp(50.0, 250.0, u)
                    if t == 330:
                        self.play("slam", 0.45)
                        self._reprint(0.8)

                else:
                    self.hole[3] = 0.0
                    self.struck = {}
                    if t > 380:
                        self.dark = inv_clamp(self.dark + 0.016, 0.0, 1.0)
                if t > 450:
                    self.result = "victory"

            else:
                # 0-30    everything stops
                # 30-210  the page is struck out cell by cell, in reading order
                # 210-260 the bar goes across you
                # 260+    a blank sheet, held far longer than is comfortable
                if t == 1:
                    self.play("cut", 0.6)
                if 30 <= t < 210:
                    u = (t - 30) / 180.0
                    target = int(u * NF_COLS * NF_ROWS)
                    idx = 0
                    for r in range(NF_ROWS):
                        for c in range(NF_COLS):
                            if idx >= target:
                                break
                            if (c, r) not in self.struck:
                                self.struck[(c, r)] = {"ink": 0.0, "dir": "h"}
                                if idx % 4 == 0:
                                    self.play("tick", 0.35)
                            idx += 1
                        if idx >= target:
                            break
                    for data in self.struck.values():
                        data["ink"] = min(1.0, data["ink"] + NF_INK_RATE)
                    self.hud_fade = max(0.0, 1.0 - u * 1.4)
                if 210 <= t < 262:
                    self.end_bar = inv_smooth((t - 210) / 52.0)
                    if t == 212:
                        self.play("cut_big", 0.85)
                if t == 262:
                    self._reprint(1.0)
                    self.play("slam", 0.5)
                if t >= 262:
                    self.end_wipe = inv_clamp((t - 262) / 40.0, 0.0, 1.0)
                if t >= 400:
                    self.dark = inv_clamp(self.dark + 0.012, 0.0, 1.0)
                if t > 470:
                    self.result = "defeat"


# --- THE STAGE ---------------------------------------------------------------
init python:
    class NFStage(renpy.Displayable):
        """One CDD. Steps NFGame at a fixed 60Hz inside render() and paints the
        whole encounter from cached-texture blits."""

        _tf_cache = {}
        _misc_cache = {}
        _text_cache = {}

        PANEL_CMD = (40, 548, 470, 148)
        PANEL_HUD = (770, 548, 470, 148)

        def __init__(self, game, **kwargs):
            super(NFStage, self).__init__(**kwargs)
            self.game = game
            self.last_st = None
            self.acc = 0.0

        def _misc(self, key, builder):
            d = NFStage._misc_cache.get(key)
            if d is None:
                if len(NFStage._misc_cache) > 600:
                    NFStage._misc_cache.clear()
                d = builder()
                NFStage._misc_cache[key] = d
            return d

        def _text(self, text, size, color, font=INV_FONT, bold=False,
                outline=None):
            key = (text, size, color, font, bold, outline)
            t = NFStage._text_cache.get(key)
            if t is None:
                if len(NFStage._text_cache) > 240:
                    NFStage._text_cache.clear()
                outl = [(2, outline, 0, 0)] if outline else []
                t = Text(text, size=size, color=color, bold=bold, font=font,
                        outlines=outl, substitute=False)
                NFStage._text_cache[key] = t
            return t

        def _body_plain(self, zoom, alpha=1.0):
            ab = int(inv_clamp(alpha, 0.0, 1.0) * 6)
            key = ("plain", round(zoom, 3), ab)
            tf = NFStage._tf_cache.get(key)
            if tf is None:
                kw = dict(zoom=zoom, subpixel=True)
                if ab < 6:
                    kw["alpha"] = ab / 6.0
                tf = Transform(NF_SPRITE, **kw)
                NFStage._tf_cache[key] = tf
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

            sblit = rv.subpixel_blit

            shake_x = shake_y = 0
            if g.shake > 0.01:
                amp = 12.0 * g.shake
                shake_x = int(math.sin(g.tick * 1.9) * amp)
                shake_y = int(math.cos(g.tick * 2.7) * amp * 0.6)

            on_page = (g.open > 0.5)

            # --- 1. the room / the page -------------------------------------------
            self._render_plain(g, rv, rect, st, at)

            # --- 2. the encounter ---------------------------------------------------
            if on_page:
                self._render_page(g, rv, tex, rect, qa, blit_text, sblit,
                                shake_x, shake_y, st, at)
            else:
                self._render_room(g, rv, tex, rect, qa, blit_text, sblit,
                                shake_x, shake_y, st, at)

            # --- 3. numbers ---------------------------------------------------------
            for f in g.floats:
                a = inv_clamp(f["life"] / 26.0, 0.0, 1.0)
                blit_text(f["text"], 28 if f["big"] else 20,
                        f["color"] + qa(a), int(f["x"]) + shake_x,
                        int(f["y"]) + shake_y, bold=f["big"],
                        anchor=(0.5, 0.5), w=340, h=60)

            if g.paused:
                rv.blit(rect("#050506c8" if not on_page else "#e8e6dec8",
                            1280, 720), (0, 0))
                pcol = NF_PALE if not on_page else NF_INK
                blit_text("PAUSED", 40, pcol, 640, 316, bold=True,
                        anchor=(0.5, 0.5), w=600, h=70)
                blit_text("ESC  RESUME        Q  QUIT", 16,
                        NF_DIM if not on_page else NF_FAINT,
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

        def _render_plain(self, g, rv, rect, st, at):
            global NF_PLAIN_OK
            if NF_PLAIN_OK:
                try:
                    quad = Transform(
                        NF_SOUP_IMG, xysize=(1280, 720), mesh=True,
                        shader="inv.plain",
                        u_nf_res=(1280.0, 720.0),
                        u_nf_time=g.clock,
                        u_nf_open=g.open,
                        u_nf_press=g.press,
                        u_nf_reg=g.reg,
                        u_nf_scrut=g.scrut_frac(),
                        u_nf_flash=g.flash,
                        u_nf_dark=g.dark,
                        u_nf_churn=g.churn(),
                        u_nf_hole=(float(g.hole[0]), float(g.hole[1]),
                                float(g.hole[2]), float(g.hole[3])))
                    qr = renpy.render(quad, 1280, 720, st, at)
                    rv.depends_on(qr)
                    rv.blit(qr, (0, 0))
                    return
                except Exception as e:
                    NF_PLAIN_OK = False
                    try:
                        renpy.log("INV FX: plain render failed: %r" % e)
                    except Exception:
                        pass
            rv.blit(rect(NF_PAPER if g.open > 0.5 else NF_BLACK, 1280, 720),
                    (0, 0))

        # ----- the body --------------------------------------------------------

        def _draw_body(self, g, rv, tex, sblit, cx, cy, zoom, sx, sy, st, at,
                    bars=0.0, ink=1.0, jump=1.0, stretch=(1.0, 1.0),
                    alpha=1.0, paper=0.0):
            # A redaction overshoots the thing it covers, so the plate needs a
            # wide margin or the bars get clipped at the silhouette.
            plate_zoom = min(zoom, NF_PLATE_MAX_ZOOM)
            extra = zoom / plate_zoom
            plate, W, H = inv_body_plate(NF_SPRITE, NF_SPRITE_W, NF_SPRITE_H,
                                        plate_zoom, pad_x=1.55, pad_y=1.30)
            # The figure is off-centre in its own canvas; put the FIGURE where
            # the caller asked, not the canvas.
            cx = cx + NF_FIG_DX * zoom
            cy = cy + NF_FIG_DY * zoom

            if NF_STRIKE_OK:
                try:
                    body = Transform(
                        plate, mesh=True, shader="inv.strike",
                        u_st_res=(float(W), float(H)),
                        u_st_t=g.clock,
                        u_st_jump=float(jump),
                        u_st_reg=float(g.reg),
                        u_st_stretch=(float(stretch[0]), float(stretch[1])),
                        u_st_pivot=0.90,
                        u_st_ink=float(ink),
                        u_st_paper=float(paper),
                        u_st_churn=float(g.churn()),
                        u_st_bars=float(bars))
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
            """You. The same SOUL heart as the other modes, and in the second
            half the only thing anywhere on the page that has a colour."""
            plate, W, H = inv_body_plate(INV_HEART, INV_HEART_W, INV_HEART_H,
                                        NF_HEART_ZOOM, pad_x=2.2, pad_y=2.2,
                                        nearest=True)
            squeeze = 1.0 - 0.20 * g.beat_pulse
            if INV_FLESH_OK:
                try:
                    d = inv_flesh(plate, W, H, g.clock * 2.6,
                                warp=NF_HEART_WARP, split=0.9,
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
                            lambda: Transform(INV_HEART, zoom=NF_HEART_ZOOM,
                                            nearest=True, subpixel=True))
            r, (w, h) = tex(("heartplain",), heart, 160, 160)
            sblit(r, (cx - w * 0.5 + sx, cy - h * 0.5 + sy))

        # ----- ACT ONE ---------------------------------------------------------

        def _render_room(self, g, rv, tex, rect, qa, blit_text, sblit,
                        sx, sy, st, at):
            arriving = (g.mode == "arrive")
            scrut = g.scrut_frac()

            # It does not bob and it does not breathe. It stands where it is
            # printed, and every so often it is printed somewhere else.
            jitter = 4.0 * g.press
            cy = 300 + math.sin(g.reg * 2.1) * 3.0 + jitter

            if arriving:
                # NO cy OVERRIDE HERE, DELIBERATELY. Nonfiction does not climb
                # out of the rupture -- it is PRINTED into the room, in three
                # registration passes, and a printed thing appears where it is
                # going to be. Placing it at the hole and then snapping it to
                # its resting cy when the panels came up was the entrance
                # misalignment AND a contradiction of the one thing this
                # Archivist's arrival is supposed to say.
                bars = g.body_bars
                ink = g.body_ink
            else:
                bars = 0.10 * g.hit_flash
                ink = 1.0

            self._draw_body(g, rv, tex, sblit, 640, cy, NF_ZOOM_ACT1, sx, sy,
                            st, at, bars=bars, ink=ink,
                            jump=0.6 + 1.8 * g.press + 0.5 * scrut,
                            paper=0.0)

            if arriving:
                return

            # --- the only chrome act one gets ------------------------------------
            # These two sit directly on the room rather than inside a panel,
            # so they carry their own outline.
            blit_text("NONFICTION", 15, NF_PALE, 380, 24, bold=True, w=320,
                    h=30, outline=NF_BLACK)

            # ITS ACCOUNT. One bar, two materials: solid for what you have
            # SOURCED, hatched for what you have merely stated. The hatched
            # part is the part it can take back, and it looks like it.
            bar_w = 520
            rv.blit(rect("#050506b4", bar_w + 4, 12), (380 - 2, 48))
            rv.blit(rect("#1b1c1f", bar_w, 8), (380, 50))
            led = int(bar_w * inv_clamp(g.ledger_shown / float(NF_STANDING_MAX),
                                        0.0, 1.0))
            pend = int(bar_w * inv_clamp(g.pending_shown / float(NF_STANDING_MAX),
                                        0.0, 1.0))
            if led > 0:
                rv.blit(rect(NF_PALE, led, 8), (380, 50))
            if pend > 0:
                x = 380 + led
                for k in range(0, pend, 6):
                    rv.blit(rect(NF_PALE + qa(0.40), min(3, pend - k), 8),
                            (x + k, 50))

            # SCRUTINY. A second, thinner rule under the first.
            rv.blit(rect("#1b1c1f", bar_w, 4), (380, 64))
            sc = int(bar_w * scrut)
            if sc > 0:
                rv.blit(rect(NF_WARN if scrut < 0.85 else NF_RED, sc, 4),
                        (380, 64))
            blit_text("SCRUTINY", 11, NF_DIM, 380, 72, w=200, h=22,
                    outline=NF_BLACK)

            slide = int(g.panel_slide * 200)
            if g.panel_slide < 1.0:
                self._panel(rv, rect, NFStage.PANEL_CMD, sx, sy + slide)
                self._panel(rv, rect, NFStage.PANEL_HUD, sx, sy + slide)
                self._panel_contents(g, rv, tex, rect, qa, blit_text, sx,
                                    sy + slide)

        def _panel(self, rv, rect, box, sx, sy):
            x, y, w, h = box
            x += sx
            y += sy
            rv.blit(rect(NF_PALE, w + 6, h + 6), (x - 3, y - 3))
            rv.blit(rect(NF_BLACK, w + 2, h + 2), (x - 1, y - 1))
            rv.blit(rect(NF_WIN, w, h), (x, y))
            # A ruled page, not a game window.
            for k in range(1, 5):
                rv.blit(rect("#dcded61e", w - 24, 1), (x + 12, y + 12 + k * 30))

        def _panel_contents(self, g, rv, tex, rect, qa, blit_text, sx, sy):
            cx, cy, cw, ch = NFStage.PANEL_CMD
            cx += sx
            cy += sy

            if g.mode == "menu":
                for i, row in enumerate(NF_CMDS):
                    live = (i == g.cursor)
                    ry = cy + 16 + i * 30
                    if live:
                        rv.blit(rect(NF_PALE + qa(0.12), cw - 28, 26),
                                (cx + 14, ry - 3))
                        rv.blit(rect(NF_PALE, 9, 9), (cx + 22, ry + 6))
                    blit_text(row[1], 20, NF_PALE if live else NF_FAINT,
                            cx + 42, ry, bold=live, w=260, h=30)
                    if row[0] == "cite":
                        blit_text(str(NF_CITE_COST), 14,
                                NF_PALE if live else NF_FAINT,
                                cx + cw - 22, ry + 4, anchor=(1.0, 0.0),
                                w=120, h=26)
                blit_text("Z  OK      ESC  PAUSE", 12, NF_FAINT,
                        cx + cw - 16, cy + ch - 22, anchor=(1.0, 0.0),
                        w=420, h=24)

            elif g.mode == "beat":
                blit_text(g.beat_label, 22, NF_PALE, cx + 20, cy + 30,
                        bold=True, w=cw - 40, h=40)
                if g.beat_value:
                    blit_text(g.beat_value, 26, NF_WARN, cx + 20, cy + 64,
                            bold=True, w=cw - 40, h=44)
                if g.mtick > 12 and (g.tick // 20) % 2 == 0:
                    rv.blit(rect(NF_PALE, 14, 4), (cx + cw - 36, cy + ch - 26))

            hx, hy, hw, hh = NFStage.PANEL_HUD
            hx += sx
            hy += sy
            blit_text(inv_player_name(), 19, NF_PALE, hx + 20, hy + 12,
                    bold=True, w=hw - 40, h=32)
            self._odometer(g, rv, rect, qa, blit_text, "HP", g.hp_shown,
                        g.hp, hx + 20, hy + 44, NF_PALE)
            self._odometer(g, rv, rect, qa, blit_text, "SRC", g.src_shown,
                        g.src, hx + 20, hy + 96, NF_DIM, small=True)

            if g.pending > 0:
                blit_text("UNSOURCED  %d" % g.pending, 13,
                        NF_WARN if not g.marked else NF_RED,
                        hx + hw - 20, hy + 16, anchor=(1.0, 0.0), w=260, h=26)
            if g.marked:
                blit_text("MARKED", 13, NF_RED, hx + hw - 20, hy + 40,
                        anchor=(1.0, 0.0), w=200, h=26)
            if g.god:
                blit_text("GOD", 12, NF_WARN + "aa", hx + hw - 20,
                        hy + hh - 24, anchor=(1.0, 0.0), w=120, h=24)

        def _odometer(self, g, rv, rect, qa, blit_text, label, shown, real,
                    x, y, color, small=False, invert=False):
            """An EarthBound counter: fixed-width cells, and the digits that
            are moving are drawn mid-roll rather than swapped."""
            size = 22 if small else 30
            cell_w = 22 if small else 28
            cell_h = 32 if small else 42
            cell_col = "#dcded655" if invert else "#0a0a0ce0"
            blit_text(label, 14, color, x, y + (6 if small else 12), bold=True,
                    w=60, h=28)

            value = int(math.ceil(shown - 0.0001)) if shown > 0 else 0
            rolling = abs(shown - real) > 0.05
            digits = "%03d" % inv_clamp(value, 0, 999)
            frac = shown - math.floor(shown)
            base_x = x + 44

            for i, ch in enumerate(digits):
                dx = base_x + i * cell_w
                rv.blit(rect(cell_col, cell_w - 4, cell_h), (dx, y))
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

        # ----- ACT TWO: THE PAGE -----------------------------------------------

        def _render_page(self, g, rv, tex, rect, qa, blit_text, sblit,
                        sx, sy, st, at):
            leaving = g.mode in ("leave_w", "leave_l")

            # --- the watermark ------------------------------------------------
            # It is not standing anywhere. It is IN the paper -- large, faint,
            # behind the rules, and it never walks: it only re-registers, hard,
            # on the same passes that bring a volley in.
            #
            # AND IT IS NOT ON THE BEAT. A version of this ran off a monotonic
            # beat count so the plate re-set exactly on the music; it was cut
            # (user, Aug 14 2026). What it looks like NOW is a thing that
            # happens to fall near the pulse sometimes and does not the rest
            # of the time, which is the better version of the effect -- it
            # reads as coincidence rather than choreography, and a printing
            # press that keeps time is a press with an opinion about the
            # music. Nothing in this fight has an opinion.
            churn = g.churn()
            self._draw_body(g, rv, tex, sblit, 640, 380, NF_ZOOM_MARK, sx, sy,
                            st, at,
                            bars=(getattr(g, "leave_bars", 0.0)
                                if g.mode == "leave_w" else 0.0),
                            ink=1.0,
                            jump=0.5 + 2.2 * g.press,
                            alpha=NF_MARK_ALPHA * (1.0 + 1.6 * g.press),
                            paper=1.0)

            # --- the grid ------------------------------------------------------
            px0, py0 = NF_PLANE_X + sx, NF_PLANE_Y + sy
            rv.blit(rect(NF_RULE_COL + qa(0.55), NF_PLANE_W + 4, 2),
                    (px0 - 2, py0 - 2))
            rv.blit(rect(NF_RULE_COL + qa(0.55), NF_PLANE_W + 4, 2),
                    (px0 - 2, py0 + NF_PLANE_H))
            rv.blit(rect(NF_RULE_COL + qa(0.55), 2, NF_PLANE_H + 4),
                    (px0 - 2, py0 - 2))
            rv.blit(rect(NF_RULE_COL + qa(0.55), 2, NF_PLANE_H + 4),
                    (px0 + NF_PLANE_W, py0 - 2))
            for c in range(1, NF_COLS):
                rv.blit(rect(NF_RULE_COL + qa(0.28), 1, NF_PLANE_H),
                        (px0 + c * NF_CELL_W, py0))
            for r in range(1, NF_ROWS):
                rv.blit(rect(NF_RULE_COL + qa(0.28), NF_PLANE_W, 1),
                        (px0, py0 + r * NF_CELL_H))

            # --- THE MARGIN ------------------------------------------------------
            # Column zero, ruled off from the text with a double rule, because
            # it is not text. It is the only part of the page nothing can be
            # struck out of and the only place a citation may be filed.
            mgx = px0 + (NF_MARGIN_COL + 1) * NF_CELL_W
            rv.blit(rect(NF_RULE_COL + qa(0.70), 2, NF_PLANE_H), (mgx - 4, py0))
            rv.blit(rect(NF_RULE_COL + qa(0.70), 2, NF_PLANE_H), (mgx, py0))
            carrying = g.pend2 >= NF_BANK_MIN and not leaving

            # WHAT THE COLUMN IS FOR, in one word, and the word is act one's.
            # Rule 1 allows state words and refuses sentences, and this is the
            # cheapest legal nudge there is: the player spent eighteen turns
            # learning that a claim is worth nothing until it is CITED, so
            # heading the filing column with CITE says where to take the
            # unsourced pile without once saying take the unsourced pile
            # there. It sits quiet until you are actually carrying something.
            if not leaving:
                blit_text("CITE", 13,
                        NF_INK + qa(0.85 if carrying else 0.30),
                        NF_PLANE_X + NF_CELL_W // 2, 148, bold=carrying,
                        anchor=(0.5, 0.5), w=200, h=28)

            for r in range(NF_ROWS):
                bx, by, bw, bh = nf_cell_box(NF_MARGIN_COL, r)
                if carrying and g.margin_open(r):
                    # The destination reads as a PLACE while you have
                    # something to put in it, and as ruled-off paper the rest
                    # of the time.
                    rv.blit(rect(NF_INK + qa(0.07 + 0.05 * g.pend_frac()),
                                bw - 8, bh - 8),
                            (int(bx) + 4 + sx, int(by) + 4 + sy))
                if not g.margin_open(r):
                    # A CITATION, filed and still wet. Two short rules and a
                    # reference bar -- the shape of an entry, not an entry.
                    dry = 1.0 - g.margin_cd.get(r, 0) / float(NF_MARGIN_REOPEN)
                    a = 0.22 + 0.50 * dry
                    rv.blit(rect(NF_INK + qa(a), int(bw * 0.44), 3),
                            (int(bx) + 16 + sx, int(by + bh * 0.36) + sy))
                    rv.blit(rect(NF_INK + qa(a * 0.75), int(bw * 0.30), 3),
                            (int(bx) + 16 + sx, int(by + bh * 0.36) + 12 + sy))
                    rv.blit(rect(NF_INK + qa(a), 4, 22),
                            (int(bx) + 8 + sx, int(by + bh * 0.36) - 4 + sy))
                elif carrying:
                    # OPEN, AND YOU ARE CARRYING SOMETHING. A hollow slot,
                    # breathing. Rule 1 gets an affordance, never a caption.
                    puls = 0.5 + 0.5 * math.sin(g.tick * 0.11 + r * 0.9)
                    a = 0.16 + 0.30 * puls * g.pend_frac()
                    rv.blit(rect(NF_INK + qa(a), int(bw * 0.44), 2),
                            (int(bx) + 16 + sx, int(by + bh * 0.36) + sy))
                    rv.blit(rect(NF_INK + qa(a), int(bw * 0.44), 2),
                            (int(bx) + 16 + sx, int(by + bh * 0.36) + 14 + sy))

            # --- WHAT IS BEING DONE TO THE PAGE ------------------------------
            # Correction marks accumulating in the open cells: carets,
            # deletion loops, transposition hooks. They are printer's marks
            # rather than sentences, they have no mechanics whatever, and
            # there are more of them the harder the page is being worked --
            # which is the whole "it should get busier" answer, done in the
            # only vocabulary this fight has.
            if churn > 0.04 and not leaving:
                n_marks = int(2 + 20 * churn)
                for k in range(n_marks):
                    seed = ((k * 2654435761) % 1013) / 1013.0
                    c = int(seed * (NF_COLS - 1)) + 1
                    r = int((((k * 40503) % 977) / 977.0) * NF_ROWS)
                    if (c, r) in g.struck or (c, r) == g.anchor:
                        continue
                    bx, by, bw, bh = nf_cell_box(c, r)
                    ox = int(bx + 14 + seed * (bw - 40)) + sx
                    oy = int(by + 12 + ((k * 7919) % 100) / 100.0
                            * (bh - 34)) + sy
                    a = 0.10 + 0.26 * churn
                    kind = k % 3
                    if kind == 0:            # a caret
                        for i in range(6):
                            rv.blit(rect(NF_INK + qa(a), 2, 2),
                                    (ox + i * 2, oy + 10 - abs(i - 2) * 3))
                            rv.blit(rect(NF_INK + qa(a), 2, 2),
                                    (ox + 10 - i * 2,
                                    oy + 10 - abs(i - 2) * 3))
                    elif kind == 1:          # a deletion loop
                        for i in range(8):
                            ang = (i / 8.0) * 6.2831853
                            rv.blit(rect(NF_INK + qa(a), 2, 2),
                                    (ox + int(math.cos(ang) * 7),
                                    oy + int(math.sin(ang) * 5)))
                    else:                    # a transposition hook
                        rv.blit(rect(NF_INK + qa(a), 14, 2), (ox, oy))
                        rv.blit(rect(NF_INK + qa(a), 2, 8), (ox + 12, oy))
                        rv.blit(rect(NF_INK + qa(a), 10, 2), (ox + 2, oy + 8))

            # --- what has been struck out ---------------------------------------
            # A redaction sweeps in from one edge like a marker and OVERSHOOTS
            # its cell, because a redaction always covers more than the thing
            # it covers.
            for (c, r), data in g.struck.items():
                bx, by, bw, bh = nf_cell_box(c, r)
                ink = data["ink"]
                if data["dir"] == "v":
                    h = max(2, int(bh * ink))
                    rv.blit(rect("#000000", bw + 4, h + 3),
                            (int(bx) - 2 + sx, int(by) - 1 + sy))
                else:
                    w = max(2, int(bw * ink))
                    rv.blit(rect("#000000", w + 3, bh + 4),
                            (int(bx) - 1 + sx, int(by) - 2 + sy))

            # --- what is about to be ---------------------------------------------
            if g.pending_lines and g.volley_warn > 0:
                u = 1.0 - g.volley_warn / float(NF_VOLLEY_WARN)
                puls = 0.5 + 0.5 * math.sin(g.tick * 0.42)
                thick = 2 + int(6 * u)
                for line in g.pending_lines:
                    for (c, r) in line["cells"]:
                        bx, by, bw, bh = nf_cell_box(c, r)
                        col = NF_INK + qa(0.30 + 0.45 * u * puls)
                        if line["dir"] == "v":
                            rv.blit(rect(col, thick, bh),
                                    (int(bx + bw * 0.5 - thick * 0.5) + sx,
                                    int(by) + sy))
                        else:
                            rv.blit(rect(col, bw, thick),
                                    (int(bx) + sx,
                                    int(by + bh * 0.5 - thick * 0.5) + sy))

            # --- the anchor -------------------------------------------------------
            if g.anchor is not None and not leaving:
                bx, by, bw, bh = nf_cell_box(*g.anchor)
                expiring = g.anchor_life < 90 and (g.tick // 6) % 2 == 0
                acol = NF_INK + qa(0.20 if expiring else 0.55)
                # Corroborated ground is a shade off the rest of the sheet, so
                # it can be picked out from across the page at a glance.
                rv.blit(rect(NF_INK + qa(0.10), bw - 6, bh - 6),
                        (int(bx) + 3 + sx, int(by) + 3 + sy))
                for inset in (4, 9):
                    rv.blit(rect(acol, bw - inset * 2, 2),
                            (int(bx) + inset + sx, int(by) + inset + sy))
                    rv.blit(rect(acol, bw - inset * 2, 2),
                            (int(bx) + inset + sx,
                            int(by + bh) - inset - 2 + sy))
                    rv.blit(rect(acol, 2, bh - inset * 2),
                            (int(bx) + inset + sx, int(by) + inset + sy))
                    rv.blit(rect(acol, 2, bh - inset * 2),
                            (int(bx + bw) - inset - 2 + sx,
                            int(by) + inset + sy))
                if g.retract_warn > 0:
                    # It says so in advance, because it always does.
                    puls = 0.5 + 0.5 * math.sin(g.tick * 0.55)
                    rv.blit(rect(NF_INK + qa(0.25 + 0.50 * puls),
                                bw - 16, max(3, int(10 * puls))),
                            (int(bx) + 8 + sx, int(by + bh * 0.5) - 4 + sy))

            # --- WHERE TO GO --------------------------------------------------------
            # A dashed leader from you to whatever the next thing is. Rule 1
            # forbids a sentence telling the player what to do, and this is
            # the answer to that: not an instruction, a line on a page
            # pointing at the thing it refers to. Without it the whole act is
            # unreadable -- there is no other cue that the double-ruled square
            # is the objective rather than decoration.
            #
            # AND IT SWINGS TO THE MARGIN THE MOMENT YOU ARE CARRYING
            # ANYTHING WORTH FILING. That swing is the entire tutorial for the
            # escrow: the page stops pointing at the entry and starts pointing
            # at the nearest open row of column zero, and it does it while the
            # bar under VERIFIED is visibly holding something.
            target = None
            if not leaving:
                if carrying:
                    rows = [r for r in range(NF_ROWS) if g.margin_open(r)]
                    if rows and g.cell_of(g.px, g.py)[0] != NF_MARGIN_COL:
                        best_r = min(rows, key=lambda r: abs(
                            nf_cell_center(NF_MARGIN_COL, r)[1] - g.py))
                        target = nf_cell_center(NF_MARGIN_COL, best_r)
                elif (g.anchor is not None
                        and g.cell_of(g.px, g.py) != g.anchor):
                    target = nf_cell_center(*g.anchor)
            if target is not None:
                vx = target[0] - g.px
                vy = target[1] - g.py
                dist = math.hypot(vx, vy)
                if dist > 46.0:
                    ux = vx / dist
                    uy = vy / dist
                    step = 15.0
                    k = 34.0
                    while k < dist - 30.0:
                        a = 0.34 * (1.0 - k / max(dist, 1.0)) + 0.12
                        rv.blit(rect(NF_INK + qa(a), 5, 5),
                                (int(g.px + ux * k) + sx,
                                int(g.py + uy * k) + sy))
                        k += step

            # --- you ----------------------------------------------------------------
            if not (g.mode == "leave_l" and g.mtick > 262):
                for i, (tx, ty) in enumerate(g.trail):
                    if i == 0:
                        continue
                    a = 0.20 * (1.0 - i / float(len(g.trail)))
                    size = max(3, 10 - i)
                    rv.blit(rect(NF_RED + qa(a), size, size),
                            (int(tx) - size // 2 + sx, int(ty) - size // 2 + sy))

                blink = (g.iframes > 0 and (g.tick // 3) % 2 == 0)
                if not blink:
                    self._draw_heart(g, rv, tex, sblit, g.px, g.py, sx, sy,
                                    st, at)

                # WHAT YOU ARE CARRYING, drawn ON you rather than only in the
                # corner -- an arc closing round the heart as the escrow
                # fills, whole and pulsing once it will hold no more. The
                # player has to be able to answer "is this worth walking" from
                # the middle of the page without looking away from it.
                if not leaving and g.pend2 > 0.0:
                    pf = g.pend_frac()
                    full = pf >= 0.999
                    segs = 20
                    lit = int(round(segs * pf))
                    rr = 25.0
                    puls = 0.5 + 0.5 * math.sin(g.tick * 0.16)
                    a = 0.55 + (0.35 * puls if full else 0.0)
                    for k in range(lit):
                        ang = -1.5708 + (k / float(segs)) * 6.2831853
                        rv.blit(rect(NF_INK + qa(a), 4, 4),
                                (int(g.px + math.cos(ang) * rr) + sx,
                                int(g.py + math.sin(ang) * rr) + sy))

                # ON RECORD. THE RING ONLY CLOSES WHEN YOU STOP -- and that
                # sentence is the entire tutorial for this half of the fight,
                # delivered without writing it down. Standing still on
                # corroborated ground draws a whole ring; moving on it draws a
                # broken one. Nothing else on screen distinguishes the two
                # states, so the contrast has to be unmissable.
                if g.anchor is not None and not leaving:
                    if g.cell_of(g.px, g.py) == g.anchor:
                        filling = g.attesting or g.still > 4
                        segs = 24
                        rr = 36.0
                        size = 5 if filling else 3
                        for k in range(segs):
                            if not filling and k % 2:
                                continue          # a ring that is not closed
                            ang = -1.5708 + (k / float(segs)) * 6.2831853
                            rv.blit(rect(NF_INK + qa(0.90 if filling else 0.26),
                                        size, size),
                                    (int(g.px + math.cos(ang) * rr) + sx,
                                    int(g.py + math.sin(ang) * rr) + sy))
                        if g.attesting:
                            # Doubled, because attesting is doubled.
                            for k in range(segs):
                                ang = -1.5708 + ((k + 0.5) / segs) * 6.2831853
                                rv.blit(rect(NF_INK + qa(0.55), 3, 3),
                                        (int(g.px + math.cos(ang) * 46.0) + sx,
                                        int(g.py + math.sin(ang) * 46.0) + sy))

            # THE LAST THING STRUCK OUT IS YOU.
            if g.end_bar > 0.0:
                w = int(240 * g.end_bar)
                rv.blit(rect("#000000", w, 26),
                        (int(g.px) - 120 + sx, int(g.py) - 13 + sy))
            if g.end_wipe > 0.0:
                rv.blit(rect("#000000" + qa(g.end_wipe), 1280, 720), (0, 0))

            if g.hud_fade <= 0.02:
                return
            self._render_page_hud(g, rv, rect, qa, blit_text, sx, sy)

        def _render_page_hud(self, g, rv, rect, qa, blit_text, sx, sy):
            # --- VERIFIED, AND WHAT IS NOT VERIFIED YET --------------------------
            # ONE BAR, TWO WEIGHTS. The escrow is drawn as hatching sitting on
            # the end of the solid, so where it would reach if it were filed
            # is legible at a glance and it is unmistakably not the same
            # substance -- exactly the relationship act one drew between the
            # ledger and the pile. Two separate bars would have made them look
            # like two separate quantities.
            bw = NF_PLANE_W
            bx = NF_PLANE_X
            rv.blit(rect(NF_INK + qa(0.55), bw + 4, 20), (bx - 2, 96))
            rv.blit(rect(NF_PAPER, bw, 16), (bx, 98))
            fill = int(bw * inv_clamp(g.verify_shown / NF_VERIFY_MAX, 0.0, 1.0))
            if fill > 0:
                rv.blit(rect(NF_INK, fill, 16), (bx, 98))
            pend_w = int(bw * inv_clamp(g.pend2_shown / NF_VERIFY_MAX,
                                        0.0, 1.0))
            if pend_w > 0:
                x_p = bx + fill
                for k in range(0, min(pend_w, bw - fill), 6):
                    rv.blit(rect(NF_INK + qa(0.75), 3, 16), (x_p + k, 98))
                rv.blit(rect(NF_INK + qa(0.85), 2, 22),
                        (min(x_p + pend_w, bx + bw - 2), 95))
            if g.bank_flash > 0.02:
                rv.blit(rect(NF_INK + qa(0.55 * g.bank_flash), bw + 8, 26),
                        (bx - 4, 93))
            blit_text("VERIFIED", 13, NF_INK, bx, 74, bold=True, w=200, h=26)
            blit_text("%d" % int(g.verify), 15, NF_INK, bx + bw, 74,
                    bold=True, anchor=(1.0, 0.0), w=140, h=26)
            # AND THE HATCHING IS NAMED, in act one's word for it. The player
            # already knows what UNSOURCED means and already knows what it is
            # worth, which is nothing -- so labelling the hatched half of the
            # bar is the whole lesson delivered in one legal noun. It is
            # printed under the segment it describes and nowhere else.
            if g.pend2 >= 1.0:
                blit_text("UNSOURCED", 11,
                        NF_INK + qa(0.55 if g.pend_frac() < 0.999 else 0.95),
                        min(bx + fill + 6, bx + bw - 90), 118, w=200, h=22)
                blit_text("%d" % int(g.pend2), 13,
                        NF_INK + qa(0.62 if g.pend_frac() < 0.999 else 0.95),
                        bx + bw, 118, anchor=(1.0, 0.0), w=120, h=22)

            # --- HP and CREDIT ---------------------------------------------------
            self._odometer(g, rv, rect, qa, blit_text, "HP", g.hp_shown, g.hp,
                        44, 646, NF_INK, invert=True)
            cw = 220
            rv.blit(rect(NF_INK + qa(0.45), cw + 4, 12), (44 - 2, 622))
            rv.blit(rect(NF_PAPER, cw, 8), (44, 624))
            ccol = NF_INK if g.credit >= NF_ATTEST_MIN else NF_RED
            cf = int(cw * inv_clamp(g.credit / NF_CREDIT_MAX, 0.0, 1.0))
            if cf > 0:
                rv.blit(rect(ccol, cf, 8), (44, 624))
            rv.blit(rect(NF_INK + qa(0.55), 2, 14),
                    (44 + int(cw * (NF_ATTEST_MIN / NF_CREDIT_MAX)), 621))
            blit_text("CREDIT", 11, NF_FAINT, 44, 606, w=160, h=22)
            if g.attesting:
                blit_text("ATTEST", 13, NF_INK, 44 + cw + 12, 620, bold=True,
                        w=180, h=26)

            # --- THE READOUT -----------------------------------------------------
            # The margin stops reporting the person played.
            for i in range(min(g.facts_shown, len(g.facts))):
                key, value = g.facts[i]
                ry = 176 + i * 26
                a = 0.75
                if i == g.facts_shown - 1 and g.fact_t > NF_FACT_EVERY - 20:
                    a = 0.75 * ((NF_FACT_EVERY - g.fact_t) / 20.0)
                blit_text(key, 11, NF_FAINT + qa(a), 1092, ry, w=170, h=22)
                blit_text(value, 13, NF_INK + qa(a), 1256, ry - 2,
                        anchor=(1.0, 0.0), w=190, h=24)

            blit_text("MOVE  WASD      Z  ATTEST  (HOLD)", 12, NF_FAINT,
                    1256, 690, anchor=(1.0, 1.0), w=760, h=28)
            if g.god:
                blit_text("GOD", 12, NF_RED, 1256, 664, anchor=(1.0, 1.0),
                        w=120, h=24)


# --- THE SCREEN --------------------------------------------------------------
screen inv_nonfiction_screen(game):
    modal True
    use enter_m_input_lock()

    add Solid("#050506")
    add NFStage(game)

    key "K_ESCAPE" action Function(game.toggle_pause)
    key "mouseup_3" action Function(game.toggle_pause)
    if game.paused:
        key "K_q" action Function(game.give_up)

    if config.developer:
        key "K_g" action Function(game.toggle_god)

    timer 0.25 repeat True action Function(inv_poll_result, game, _update_screens=False)


# --- WRAPPER -----------------------------------------------------------------
default nf_game = None
default nf_deaths = 0
default nf_retry = False

label archivist_invasion_nonfiction:
    $ nf_deaths = 0
    $ nf_retry = False

label inv_nonfiction_fight:
    $ renpy.block_rollback()

    $ nf_game = NFGame(retry=nf_retry, deaths=nf_deaths,
                    debug=config.developer, start_open=inv_dev_start_open)

    $ _nf_prev_quick_menu = quick_menu
    $ quick_menu = False
    $ _nf_prev_game_menu = _game_menu_screen
    $ _game_menu_screen = None
    scene black

    call screen inv_nonfiction_screen(nf_game)
    $ _nf_result = _return

    $ nf_game = None
    $ quick_menu = _nf_prev_quick_menu
    $ _game_menu_screen = _nf_prev_game_menu
    $ inv_music_stop(1.0)
    $ inv_heart_stop(0.6)
    $ inv_stop_sfx(0.2)
    scene black

    if _nf_result == "victory":
        $ inv_record_result("nonfiction", True)
        jump inv_nonfiction_victory
    elif _nf_result == "quit":
        jump inv_nonfiction_quit

    $ inv_record_result("nonfiction", False)
    jump inv_nonfiction_defeat

label inv_nonfiction_victory:
    if inv_dev_test:
        $ renpy.notify("NONFICTION: on record.")
        return
    # STORY PLACEMENT: DRAWING BOARD.
    return

label inv_nonfiction_defeat:
    $ nf_deaths += 1
    $ nf_retry = True

    menu:
        "AGAIN":
            scene black
            jump inv_nonfiction_fight

        "STOP":
            if inv_dev_test:
                $ renpy.notify("NONFICTION: retracted. Recorded.")
            return

label inv_nonfiction_quit:
    $ nf_retry = True
    if inv_dev_test:
        $ renpy.notify("NONFICTION: withdrawn.")
    return
