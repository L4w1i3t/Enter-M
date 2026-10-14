# Presentation source

Checked September 25, 2026.

- `game/screens.rpy` owns shared screens, textbox opacity, quick menu, and
  settings. The opacity preference defaults/resets to 0.75; its background
  mapping uses `0.2 + 0.8 * preference`.
- `game/main_menu_room.rpy`, `game/main_menu_fx.rpy`,
  `game/illustrated_menu_theme.rpy`, and `game/room_menu_theme.rpy` provide the
  illustrated menu family. `game/menu_doorway.rpy` supplies the shared doorway.
- `game/first_boot_notice.rpy` handles the first-boot presentation;
  `game/story/season1/s1disc.rpy` handles the story threshold. These are separate
  from ordinary MC narration and Nier interstitials.
- `game/transforms.rpy` and `game/story_crowd_slots.rpy` define cast slots.
  `game/story_cast_framing.rpy` frames each shown story sprite under its outer
  slot. It sets one house camera (`ENTER_M_CAST_ZOOM`), a mild stature scale,
  and eye lines from heights (`ENTER_M_CAST_BODY`: the Roster's for the named
  cast, read off the art for incidentals), and masks the sprite into its story
  panel. It never redefines the source images used by the Archive, phone or
  roster. `game/stage_panels.rpy` owns the panels: the cut geometry, the live
  speaker (dim, voice colours, pop-out, push-in) and the shared edge look for
  room and cast. See the
  [September 26 note](../history/2026-09-26-cast-presentation.md) and the
  [October 11 note](../history/2026-10-11-cast-framing-pass.md).
- `game/arcade_context.rpy` launches cabinets in a child gameplay context and
  restores context-local flags on exit. Queue the doorway within that context.
- Calendar and Phone System source live in their addon directories. Their
  temporary menu state and main-story/save scope are behavior, not merely art.
- [Story Writer](STORY_WRITER.md) is developer authoring UI with source-safe
  drafts, validation, and previews.

For a visual change, inspect the actual relevant scene and combinations of
sprites/expressions. Compile/static checks do not establish readable layout or
approve the art. See [QA](../engineering/QA.md) and the
[historical presentation summary](../history/presentation.md).
