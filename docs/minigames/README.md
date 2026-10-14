# Asarhythm source and authoring

Checked September 25, 2026. The installed implementation is under
`game/addons/Asahina Rhythm/`.

| Responsibility | Source |
| --- | --- |
| Play session, settings, countdown and render integration | `asahina_rhythm.rpy` |
| Song selection | `asahina_rhythm_menu.rpy` |
| Presentation effects | `asahina_rhythm_fx.rpy` |
| Ending/continuation flow | `asahina_rhythm_finale.rpy` |
| Developer chart authoring | `chart_editor.rpy` |
| Engine-independent scoring/chart logic | `game/python-packages/asahina_rhythm_core.py` |
| Editor model | `game/python-packages/asahina_rhythm_editor.py` |
| Singer timing/registration | `game/python-packages/asahina_rhythm_motion.py` |

The original singers use whole-body drawings. `SingerFrames` keeps idle on a
two-beat cycle and restarts the singing gesture on each distinct note event,
including another note on the same arrow. A held sustain keeps the event.
Stance offsets register existing drawings; do not reinterpret earlier redraw
reports as approval to replace poses or character proportions.

Practice/autoplay/modifier handling and reward eligibility belong to the core
and play-session code. Photosensitive presentation reads the shared
accessibility setting; it does not establish medical safety. Chart-editor
source/model/export exclusions are explicit in `game/options.rpy`.

```text
python -m unittest discover -s tools -p "test_asahina_rhythm_*.py"
```

The original implementation/redraw/polish reports were consolidated in
[rhythm history](../history/rhythm.md). Treat historical build-source paths as
provenance and verify their presence before attempting a replay. Runtime visual
captures, scoring/model checks, human input, and audible sync are separate
verification scopes; see [QA](../engineering/QA.md).
