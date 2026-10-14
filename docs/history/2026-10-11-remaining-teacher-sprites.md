# Remaining teacher sprites — October 11, 2026

Created and installed neutral photographic sprites for the science, Japanese,
and English teachers. The requested stock-photo appearance matches the existing
math teacher, civics teacher, and track coach.

## Installed art

All three are 1024 × 1536 RGBA PNGs under
`game/assets/characters/npc/`:

| File | New visual design | Registered pupil mean |
| --- | --- | --- |
| `science_teacher.png` | Brown ponytail, glasses, sage blouse, white lab coat; folded arms | 130.3 |
| `japanese_teacher.png` | Dark bob, burgundy cardigan, ivory blouse; attendance folder | 154.7 |
| `english_teacher.png` | Dark curls, tan blazer, blue blouse; relaxed hands | 158.4 |

[Three-sprite preview](../assets/teachers/2026-10-11/review/teachers-preview.jpg).

The live script establishes all three as women: science in
`game/story/season1/0529.rpy:188`, Japanese/language arts in
`0526.rpy:378`, and English in `0528.rpy:605` and `617`.
Their specific faces, ages, ethnicities, and clothing are new art decisions,
not previously established biographical facts. The language arts attendance
folder is consistent with the May 26 scene. Generic teacher and principal
voices have no sprite requirement in the current definitions.

## Integration

- `game/asset_definitions/def_characters.rpy`: replaced the three placeholder
  paths while retaining the existing tags, `neut` attribute, and 640 × 960
  `fit="contain"` transform. Existing story shows now resolve to the new art.
- `game/story_cast_framing.rpy`: replaced the placeholder pupil means with
  measurements from the new images. Source coordinates were multiplied by
  0.625; visual measurement precision is about one source pixel.
- Existing 1.00 camera correction and 64-inch incidental role estimates remain.
  Those heights are framing assumptions, not newly asserted canon.
- Math, civics, and coach image hashes match their pre-task values.
  Story dialogue and scene staging were not edited.

The integration follows the current official
[Ren'Py image statement documentation](https://www.renpy.org/doc/html/displaying_images.html#image-statement),
checked October 11, 2026. The project convention supplies explicit paths to the
existing image definitions.

## Generation and evidence

Used the built-in `image_gen` tool, one call per teacher, with the three
existing photographic adults as style/framing references and
`transparent_background=true`.

The complete, exact prompt set is in
[prompts.json](../assets/teachers/2026-10-11/prompts.json).
Production PNGs are byte-identical copies of the generated outputs, with no
resizing, recoloring, matting, or alpha edits.

The generated files contain genuine transparency. Their interior alpha is
predominantly 253/255; it was preserved. Some RGB values underneath transparent
pixels form a glow when a viewer ignores alpha. Proper compositing confirms
that glow is absent from the visible sprite; no painted backdrop was shipped.

File metadata, source hashes, reference preservation, and definition checks:
[validation.json](../assets/teachers/2026-10-11/validation.json).

Rebuild diagnostic composites and metadata without editing the art:

```powershell
python docs/assets/teachers/2026-10-11/build_review.py
```

Light, dark, and magenta diagnostic backgrounds are in
[review](../assets/teachers/2026-10-11/review).
Primary and independent visual reviews covered photographic style, distinct
faces, anatomy, hands, clothing, and cutout edges. No material defects were
identified. User artistic approval is not recorded.

Task-local source snapshots for comparison are in
[before](../assets/teachers/2026-10-11/before); they preserve the pre-task
working files, including changes that predated this task.

## Runtime validation

Focused MatsuPy 8.6 checks and screenshots are recorded in
[qa](../assets/teachers/2026-10-11/qa).

- Compile passed. Lint passed with only the existing
  `config.check_conflicting_properties` advisory. Reachability reported zero
  unreachable items across 159 production source files.
- Five 1280 × 720 GL2 captures passed: each new teacher alone, plus
  science/civics/Japanese and science/civics/English groups. Both group captures
  were directly reviewed: compatible face/shoulder scale, aligned eye lines,
  clean classroom composites, and no head or prop clipping.
- The probe asserted the exact registered `neut` images and active production
  story framing for every shown teacher.
- Used `MATSU_FRESH_RUN=1` and fresh private save directories; runtime assertions
  verified private save/sync/token paths. Shared save/persistent/token hashes
  and mtimes remained unchanged, with zero blocked writes.
- The final runtime exited 0 in 13.62 seconds. Earlier QA-only attempts hit the
  known software-renderer startup issue and two harness API mistakes; those
  attempts and their isolation evidence are retained separately. The final
  probe uses the external safe-mode startup workaround and GL2.

This is direct-entry visual/integration QA with dummy audio. Full-route pacing,
audio, packaged builds, and old-save compatibility were not tested.

