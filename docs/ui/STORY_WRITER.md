# Story Writer

Checked September 25, 2026 against `game/addons/Story Writer/` and
`game/python-packages/story_writer_model.py` / `story_writer_text.py`.
The developer menu calls `story_writer_open` from `game/addons/Dev Hub/dev_hub.rpy`;
`game/dev.rpy` selects developer mode. Release exclusions live in `game/options.rpy`.

The writer shows source-order beats, their editing controls, a stage preview,
and an insert palette. It handles textboxes, backgrounds, sprites, music,
transitions, pauses, and Nier boundaries. Unsupported logic and branch context
must remain source-preserved. Preview is a controlled rendering path, not
permission to execute arbitrary authored Python.

Drafts and recovery data live in `dev/story_writer/`, outside loaded game
scripts. Source export checks the whole candidate and external file changes
before replacing the target. Keep backups/recovery data until an export has
been reviewed; do not copy a draft into `game/` just to preview it.

| Responsibility | File under `game/addons/Story Writer/` |
| --- | --- |
| Session, selection, staging and export controls | `controller.rpy` |
| Main layout and dialogs | `screens.rpy`, `dialogs.rpy` |
| Text input and canvas | `text_editor.rpy`, `canvas.rpy` |
| Controlled scene preview | `preview.rpy` |
| Candidate validation | `validation.rpy` |

Read the [isolation requirements](../engineering/QA.md) before running engine
probes.
The older design and implementation reports are summarized in
[presentation history](../history/presentation.md); their test totals and
intermediate layouts are not current guarantees.
