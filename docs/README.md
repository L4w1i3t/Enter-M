# ENTER M Documentation

Project documentation lives here so the game and addon source trees contain
only runtime content. Matsu'Py excludes this directory from release builds.

MPT documentation remains with MPT as requested. License, attribution, vendor,
and runtime readmes stay beside the files they govern; location-sensitive
`.claude/` and `.agents/` metadata also remains in place.

## Filing guide

| Directory | Put documents here when they cover... |
|---|---|
| `project/` | project-wide plans, roadmaps, and active work trackers |
| `story/` | narrative criticism, editorial work, and story reference material |
| `assets/` | asset authoring records, sourcing lists, and runtime asset guides |
| `addons/` | addon setup, usage, and content-pipeline instructions |
| `archive/` | retained source material needed to reproduce an existing asset |
| `cutting-room/` | retired or superseded work kept for historical reference |

Use the subdivisions already present instead of adding new documents to this
directory's root. Broad narrative reports that span review and audit categories
may live directly in `story/` (for example, `story/pacing-analysis-season1.md`).

## Project

- [Roadmap](project/roadmap.md)
- [TODO](project/TODO.txt)

## Story

Broad analysis:

- [Season 1 pacing analysis](story/pacing-analysis-season1.md)

Reviews and opinions:

- [Blind-player review](story/reviews/BLIND_PLAYER_REVIEW.md)
- [Character opinions](story/reviews/CHARACTER_OPINIONS.md)
- [Addons and side-content opinions](story/reviews/ADDONS_AND_SIDE_CONTENT_OPINIONS.md)

Audits:

- [Bingo exposure](story/audits/BINGO_EXPOSURE_AUDIT.md)
- [Forced conundrums and punished choices](story/audits/FORCED_CONUNDRUM_AUDIT.md)
- [Narration naming](story/audits/NARRATION_NAMING_AUDIT.md)
- [Negated-definition prose tic](story/audits/NEGATED_DEFINITION_TIC_AUDIT.md)
- [Main-story repetition overview](story/audits/repetition/MAIN_STORY_REPETITION_AUDIT.md)
- [Repetition details: May 15-19](story/audits/repetition/MAIN_STORY_REPETITION_DETAILS_0515_0519.md)
- [Repetition details: May 20-24](story/audits/repetition/MAIN_STORY_REPETITION_DETAILS_0520_0524.md)
- [Repetition details: May 25-28 and exam guard](story/audits/repetition/MAIN_STORY_REPETITION_DETAILS_0525_0528_EXAM.md)

Revision records:

- [Review fix checklist](story/revision/REVIEW_FIX_CHECKLIST.md)
- [Revision annotation index](story/revision/REVISION_ANNOTATION_INDEX.md)
- [Annotation application log](story/revision/ANNOTATION_APPLY_LOG.md)

Reference material:

- [Jay's bingo sheet](story/reference/BEATING_JAYS_BINGO_SHEET.txt)

## Assets

- [Shared asset layout](assets/ASSET_LAYOUT.md)
- [SFX shopping list](assets/audio/SFX_SHOPPING_LIST.md)
- [Asahiko (MC) sprite authoring record](assets/sprites/ASAHIKO_SPRITE_PROMPTS.md)
- [Asahina sprite authoring record](assets/sprites/ASAHINA_SPRITE_PROMPTS.md)
- [Kotonoha sprite authoring record](assets/sprites/KOTONOHA_SPRITE_PROMPTS.md)
- [Matsuda sprite authoring record](assets/sprites/MATSUDA_SPRITE_PROMPTS.md)
- [Tsubaki sprite authoring record](assets/sprites/TSUBAKI_SPRITE_PROMPTS.md)
- [Phone emoji guide](assets/emoji/README.txt)

## Addons

- [Addon cheat sheet](addons/ADDON_CHEATSHEET.md)
- [Calendar System](addons/Calendar%20System/README.md)
- [Arcade box art](addons/Arcade/art/README.txt)

## Archive and cutting room

- [Kotonoha boss-sheet source](archive/kototouhou/README.md)
- [Retired sprite-height scaling](cutting-room/sprite-height-scaling.md)
