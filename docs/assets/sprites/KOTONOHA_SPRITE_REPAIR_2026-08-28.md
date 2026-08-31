# Kotonoha Sprite/Expression Repair

Date: 2026-08-28

## Outcome

Rebuilt and installed Kotonoha's 40 non-neutral casual/work face layers without
the duplicate neutral eyebrow. Her 20 expression designs, identity, outfit
bases, face registration, transparency contract, and three fixed poses remain
unchanged. Both `face_neut_*` files remain intentionally blank compatibility
layers.

## Root cause

The selected magenta-backed expression masters each contained one coherent
brow pair. In the flattened canonical art, part of the viewer-right neutral
brow is connected to the diagonal bang. The builder's canonical hair/detail
guard classified that connected ink as hair and restored it after compositing
the authored alternate face, producing the visible second brow. Ren'Py itself
was correctly composing one outfit base with one conditioned face layer.

## Repair

- Added a narrow, reviewed two-brow ownership boundary to the deterministic
  builder and registered it from casual to work space.
- Required zero intersection between canonical detail preservation and that
  ownership boundary.
- Rebuilt and atomically installed the exact 42-face/three-pose generated
  manifest; only the 40 alternate faces changed.
- Upgraded build provenance to schema version 2.
- Extended the validator to hash-check the builder, 23 masters, 45 staged
  generated files, and 45 installed files, and to require zero canonical brow
  restoration across all 40 alternate builds.

The image-editing model was used in edit mode on the `afraid` master with the
operative instruction to remove any duplicate/ghost eyebrow while preserving
Kotonoha's identity, hair, eyes, expression, framing, and style. The clean
master-versus-composite comparison showed that the master was already correct,
so none of those diagnostic variants were promoted. The final production bank
comes from the existing selected masters plus the corrected deterministic
ownership logic.

## Verification evidence

- `python tools/build_kotonoha_sprites.py --install`: 42 face layers and three
  poses built and installed.
- `python tools/validate_kotonoha_sprites.py`: pass; two byte-exact bases,
  exact 47-file runtime manifest, 23 master hashes, 45 staged/installed hashes,
  and 40/40 alternate brow guards at zero preserved canonical pixels.
- `python tools/build_kotonoha_render_probe.py --run`: 135 GL2 screenshots
  rendered and verified; 47 copied inputs and nine review sheets verified.
- Installed MatsuPy `compile`: pass.
- Installed MatsuPy `lint`: pass.

## Review artifacts

- `tmp/kotonoha_brow_diagnosis/root_cause_afraid.png`
- `tmp/kotonoha_brow_diagnosis/before_install_review.png`
- `tmp/kotonoha_brow_diagnosis/after_install_review.png`
- `tmp/kotonoha_sprite_build/review/heads_light.png`
- `tmp/kotonoha_render_probe/review_expressions_head_light.png`
- `tmp/kotonoha_render_probe/review_expressions_head_checker.png`

The authoritative detailed production record remains
`docs/assets/sprites/KOTONOHA_SPRITE_PROMPTS.md`.
