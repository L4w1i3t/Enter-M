# Story cast presentation — September 26, 2026

Replaces the September 25 story-cast framing. The goal: stop the main story
reading as a DDLC standee row. The panels were only cutting the background,
so the cast stood in a row in front of wallpaper. Now each character lives
inside their own panel shot.

## What changed

**The cast is inside the panels.** `game/stage_panels.rpy` publishes its cut
geometry every paint (`_stage_mask`). `game/story_cast_framing.rpy` masks each
framed story sprite to its own panel with a new shader part,
`enter_m.cast_mask`. The part rides the sprite's own texture draw, so there is
no render-to-texture. A gutter now cuts through the cast exactly where it cuts
the room.

**Live camera.** While someone on stage speaks:

- Every other panel (room and figure together) desaturates and falls back.
  This only happens with Speaker Focus on Darken. The panel does the darkening
  there, so Autofocus's matrixcolor is withheld for masked sprites. Fade and
  Off keep their exact behaviour.
- The speaker's seams burn in their voice colour and throw a soft glow into
  the shot (`ENTER_M_PANEL_VOICE`): Matsuda red, Monika emerald, Kotonoha
  lavender, Sam gold, Asahina blue, Tsubaki honey, Mom coral, MC steel. Anyone
  unlisted uses the interface crimson.
- The speaker's figure may cross their own cuts by 30px, a comic-panel
  pop-out (`ENTER_M_PANEL_BREAKOUT`).
- The speaker's room pushes in 3% about eye height (`ENTER_M_PANEL_PUSH`).

Switching Speaker Focus off removes all speaker emphasis.

**Panel chrome.** Every cut now carries the dialogue box's language:

- A bright inner hairline plus a faint second rule. It burns hottest at the top
  and cools toward the text.
- The cyan and crimson signal marks near the top of each gutter.
- A glint along a cut while its panel opens or closes, and along every cut as
  the layout cracks open.

**Equalizer.** Every figure is framed from three rules. There is one entry per
character in `ENTER_M_CAST_BODY`, measured on the registered neutral image:

1. **Camera.** A per-art correction to one house camera distance.
   - Tsubaki and Asahina ×0.94: both are drawn about 6% closer, and their faces
     and shoulders both measure larger than their peers'.
   - Monika's DDLC plate ×0.94.
   - Mom ×0.97.
   - The reference group is Sam, MC, Matsuda and Kotonoha.
2. **Stature.** A mild whole-figure scale of (height / 66") ** 0.5. When height
   was shown by placement alone, the two shortest girls read as standing
   *closer* rather than as smaller people.
3. **Height.** The eye line rises 14px per inch of Roster height (at slot zoom
   0.80) around y=262 for 66". The Roster heights are Sam 71, MC 70,
   Matsuda 69, Mom 66, Monika 65, Kotonoha 65, Tsubaki 64 and Asahina 64.

Codex's eyeballed scale/crop tables are gone. Face length alone was tried as the
scale rule and rejected: it is a style feature, not a distance (Sam's tilted
head measures 20% "bigger").

**Crowds frame closer.** A masked crowd cannot pile up, so four-, five- and
six-person stages are framed at 0.78, 0.76 and 0.74 instead of 0.74, 0.68 and
0.63. The change rides panel engagement. Seven and eight still share panels and
keep standing back.

## Engine findings

- **Render-to-texture flips clip-space y.** Every dissolve draws both scenes
  into textures, and the documented `-gl_Position.y * .5 + .5` then puts the top
  of the screen at the bottom. Mid-dissolve the gutters leaned the wrong way.
  Both shaders take the orientation from the sign of `u_transform[1][1]`.
- **Panels are picked in screen space now, not plate space.** A master-layer
  shake moves the room and the cast inside a frame that holds still, and mask
  and gutter can never disagree.
- **A dissolve re-renders the outgoing scene with the incoming geometry.** A
  frame is therefore masked only while it belongs to the master layer's current
  entries, re-derived at each interaction start. Hiding (`hide$tag`) entries
  count, and `scene` empties the set. Rollback and load re-derive it for free.

## Unchanged

Registered images, and therefore the Archive, roster, dossiers, phone and
every screen `add`. Side stories and other out-of-scope content. Manual
placements and inline ATL. The slot vocabulary. Save compatibility: class names
are kept, and pickled frames re-derive their framing on first render.

## Checks run

All on the installed 8.6 SDK, GL2, isolated saves (`MATSU_FRESH_RUN`, private
savedir, audit-hook write guard). No shared saves or persistent changed in any
run.

- Lint clean. The old init-1000 warning on the framing file is gone. Only the
  standing `check_conflicting_properties` advisory remains.
- The September 25 suite (`tools/probes/story_presentation_capture.rpy`) passes
  all 89 captures and every assertion, including:
  - one frame per sprite across expression changes;
  - slot restage, Autofocus toggle, and suspend/resume;
  - manual placements left unframed;
  - animated hide;
  - legacy-save heal once, and at-list pickle round trip;
  - engine save readable, and menu over the frozen stage;
  - 1–8-person crowd entry and exit;
  - Archive portrait fixture.
- `tools/run_cast_presentation_qa.py` (probe
  `tools/probes/cast_presentation_capture.rpy`, output in
  `%LOCALAPPDATA%\Temp\enter_m_cast_qa\`) restages the four screenshot scenes (May 15–18) plus
  solo, 3-, 4- and 6-person height lineups. It also samples an entrance,
  a mid-ease speaker switch, a mid-dissolve scene change, a mid-shake, a
  t11→t31 glide and an exit.
- Redraw budget: 0 frame renders and 0 driver calls in 2s idle after settling
  and again after a speaker switch. Frames only redraw while the cuts move.

Not verified: full-route play, human input at normal speed, packaged builds,
older save files from real play, and atmosphere presets in combination.
