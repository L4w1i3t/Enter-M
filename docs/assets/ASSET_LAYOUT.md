# Asset layout

Checked September 25, 2026. Shared runtime assets live under `game/assets/`;
declarations live under `game/asset_definitions/`. Runtime paths are relative to
`game/`, for example `assets/characters/...`.

| Content | Directories under `game/assets/` |
| --- | --- |
| Scenes and illustrations | `backgrounds/`, `cg/` |
| Cast and imported sprite art | `characters/`, `mpt/`, `extra_sprites/` |
| Sound | `audio/bgm/`, `audio/sfx/` |
| Interface and type | `gui/`, `ui/`, `fonts/`, `emoji/` |
| Modes and effects | `greywake/`, `bullets/`, `transitions/` |
| Unsorted material requiring reference checks | `dump/` |

Addons can own assets beside their source under `game/addons/`. Imported Lost
Records content can retain its own layout. Root `icon.ico`/`icon.icns` are build
inputs. `game/options.rpy` controls automatic image lookup and build exclusions;
a folder's name alone does not decide whether it ships.

CG Gallery and Music Room retain some older paths as persistent identity keys.
Those keys are not live file references; changing them can relock progress.
Inspect their explicit compatibility fields before changing a path.

Do not infer unused status just because `rg` returns no literal hit: many
paths are constructed at runtime.

Authoring prompts, source atlases, manifests, and review images under `docs/`
remain provenance. Their historical dimensions and approval language describe
the corresponding production pass, not necessarily the installed asset.
Keep source/backup data intact during runtime pruning.
