# Textbox default opacity - 2026-09-25

Set `persistent.textbox_opacity` to default to `0.75` in `game/screens.rpy`.
Restore Defaults and the invalid-value fallback now use the same value.
Existing saved user preferences remain intact. The slider's established
0.2-to-1.0 alpha mapping and cached background transforms are unchanged;
the default setting therefore maps to a background transform alpha of 0.8.

Validation: inspected all production references to `textbox_opacity` and
confirmed initialization, reset, and fallback agree. No runtime replay was
needed for this settings-only change. QA fixtures that explicitly select
maximum/minimum opacity continue to exercise those extremes.
