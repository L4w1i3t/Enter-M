# Tsubaki broad oval face-plate rebuild - 2026-08-30

## Outcome

Tsubaki's casual and uniform expression banks were rebuilt with the same
structural model used by Himeko and Asahina: one intact neutral whole-body base
plus one broad, full-color oval face plate. The installed 40 alternate plates
now own the bangs, brows, eyes, nose, and mouth together. No neutral-base brow
can show through inside the solid face core.

This rebuild supersedes the schema-v4 semantic-detail repair and schema-v5
adaptive ghost-arc repair. Both approved neutral bases and the public 42-file
face-layer API remain unchanged.

## Diagnosis and reference comparison

Himeko and Asahina do not slice brows, eyes, and mouths into separate runtime
parts. Their alternate expressions use a stable feathered oval containing the
whole local head/face raster, including the bangs that cross the forehead.

The previous Tsubaki pipeline instead multiplied its nominal ellipse by a
connected skin component, then tried to repair the resulting holes with a
neutral-feature guard, sparse semantic ownership, and expression-relative
negative masks. That architecture left only about 36,000 visible alpha pixels
per alternate and made eyebrow/bang intersections depend on several masks.

The replacement plates contain about 60,800 visible pixels each:

| Outfit | Alpha bbox | Visible | Opaque | Feathered |
|---|---:|---:|---:|---:|
| Casual | `(355,277)-(663,515)` | 60,781 | 43,866 | 16,915 |
| Uniform | `(355,271)-(663,509)` | 60,769 | 43,856 | 16,913 |

Every casual alternate shares the casual alpha byte-for-byte; every uniform
alternate shares the uniform alpha byte-for-byte. The outfits remain separate
because the canonical eye registrations differ by roughly six vertical
pixels.

## Build architecture

`tools/build_tsubaki_faceplates.py` performs the canonical build:

1. Detect the source and outfit-native amber iris centers.
2. Register each authored expression master directly to the corresponding
   approved base.
3. Match local skin color without altering authored dark features, tears, or
   blush.
4. Remove only detached pale upper-lid residue in a bounded lash-relative band
   using the outfit-matched featureless donor. This happens before slicing and
   does not shape the exported alpha; legitimate near-lash folds remain.
5. Slice the complete registered raster through one geometric oval, multiply
   it only by the approved base alpha, and apply a geometric lower fade.
6. Export transparent compatibility layers for both `neut` states and full
   plates for the 20 alternates in each outfit.

The oval has radius `(155,135)`, a solid-radius fraction of `0.84`, a center 31
pixels below the detected eye midpoint, and a lower fade from center+85 through
center+105. The canonical bases are never rewritten.

The old `process_tsubaki_face_patches.py` and `install_tsubaki_sprites.py`
entry points were replaced with compatibility wrappers. The processor now
builds the oval bank; the installer accepts only an already-validated oval
build. This prevents an old command from silently restoring schema-v5 assets.

## Validation and visual acceptance

Static validation proved:

- exactly 42 expected installed face files;
- both neutral compatibility layers fully transparent;
- pixel-identical alternate alpha per outfit;
- 100 percent opaque ownership of the pinned neutral-brow footprint;
- exact replay from the registered source masters and donor inputs;
- zero RGB beneath zero alpha;
- zero checker contamination in both the solid core and feather;
- zero alpha outside the approved base silhouette;
- 40 distinct alternate head composites; and
- byte identity between production and the reviewed staging build.

The live API scan found 277 explicit `show tsubaki` statements, 14 `ts`
say-image expression calls, and live use of all 21 expression tokens.

The isolated Ren'Py GL2 probe rendered all 42 outfit/expression combinations at
1280x960. All screenshots decode, have the expected dimensions, and are
pixel-distinct. Native-scale review of `uniform unamused`, `worried`, and
`disgusted` shows one dark brow per eye. The remaining lighter lines sit
immediately above the lashes and read as intentional eyelid folds. Review of
both full banks found no oval edge, skin ring, hair halo, jaw/neck seam,
registration jump, over-cleaned lash, lost tear, or lost blush.

MatsuPy's blocking Python entry point compiled the live project successfully;
the content reachability audit reported zero unreachable items across 122
source files. Lint contained no Tsubaki references and no error/exception
entries. Its existing missing-asset warnings concern unrelated Monika and stock
Natsuki MPT assets.

## Reproduction

```powershell
python -B tools/build_tsubaki_faceplates.py build
python -B tools/build_tsubaki_faceplates.py review
python -B tools/build_tsubaki_faceplates.py validate
python -B tools/install_tsubaki_sprites.py
python -B tools/build_tsubaki_render_probe.py
python -B tools/validate_tsubaki_sprites.py `
  --render-root tmp/tsubaki_render_probe

& '..\..\RenPy 8\matsupy-sdk\lib\py3-windows-x86_64\python.exe' `
  '..\..\RenPy 8\matsupy-sdk\matsupy.py' `
  '<ENTER M project>' compile

& '..\..\RenPy 8\matsupy-sdk\lib\py3-windows-x86_64\python.exe' `
  '..\..\RenPy 8\matsupy-sdk\matsupy.py' `
  '<ENTER M project>' lint '<lint output>'
```

The accepted review sheet is
`tmp/tsubaki_oval_faceplates/review/tsubaki_uniform_focus_before_after_native_4x.png`.
The installed pre-change bank is preserved at
`tmp/tsubaki_oval_faceplates/pre_install_backup/`.

## References

- Ren'Py layered images: <https://www.renpy.org/doc/html/layeredimage.html>
- Pillow drawing primitives used for deterministic masks:
  <https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html>
