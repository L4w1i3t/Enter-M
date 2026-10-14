# Codebase maintenance — September 25, 2026

The current source was the authority for this cleanup. The starting checkout
already had extensive changes; snapshots preserve that working copy rather than
assuming Git HEAD describes it. No story dialogue, routes, chart notes, audio,
or installed custom character artwork was rewritten.

Documentation prose was reduced by about 80%, consolidating 91 obsolete reports.
Current implementation guides begin at [the documentation index](../README.md);
this directory holds patch notes and superseded design context. Author goals,
voice/continuity instructions, distinct future-story ideas, vendor material,
artwork, prompts, masters and manifests remain. File timestamps helped order
records; source resolved conflicts. Historical evidence is not current approval.

The source pass changed 78 existing source/test files and removed approximately
5,100 net lines from those files, mainly stale commentary and unused inherited
declarations. New audit/check tools were added separately. Opaque local names in
save-bank and rhythm helpers now describe their purpose. Public/save-facing
identifiers and necessary rendering/serialization constraints were preserved.

Concrete fixes:

- Story Writer detects a source file disappearing and invalidates its file-state
  cache when switching/recovering documents with matching metadata. Draft
  snapshots reuse the existing helper.
- Dialogue-size caching includes height slack, preventing reuse of a size fitted
  against different available space.
- A failed save deletion preserves its custom label. The FPS meter uses
  monotonic elapsed time. Rhythm effect ordering uses a cached lookup.
- Asset-path auditing distinguishes constructed prefixes from filenames and
  exempts only the eight verified legacy unlock IDs, rather than every missing
  path in a gallery/music source file.
- Distribution exclusions now cover the actual `DDLC copy for reference/`
  directory, all `dev/` maintenance/backups, and `tmp/` QA output. Classification
  was checked with the installed SDK's matcher. Searches also exclude the
  reference copy and maintenance artifacts unless explicitly requested.

The vanilla comparison removed **265 assets / 42,257,967 bytes (40.3 MiB)**,
795 unused image declarations, the unused console and MPT refresh-helper
scripts (including compiled counterparts), and unused effect classes/helpers.
All 531 image/audio/font entries in the reference RPAs matched the extracted
reference files. The supplied reference copy was not changed.

**33 byte-identical vanilla assets remain because they are used.** Retention
includes numeric Monika poses, shared effects/audio/fonts and the generic GUI
button textures resolved through `config.search_prefixes`. Modified backgrounds,
GUI assets, Monika layered art and active load handling remain. Legacy gallery
and music path strings remain as persistent identities. The four numeric Monika
forms use `Flatten(Composite(...))` so opacity applies to the finished composite.

Validation completed:

| Check | Result |
| --- | --- |
| Python model suite | 200 cases: 199 passed, one generated-chart case skipped |
| Additional maintenance regressions | 10 passed |
| Asset paths | 1,140 concrete references; zero errors; eight known unlock-ID warnings; eight dynamic expressions require separate review |
| Story/exam, developer, phone, currency contracts | Passed |
| MatsuPy 8.6 compile and lint | Passed; zero missing assets/obsolete manipulators and zero unreachable items across 153 sources |
| Story GL2 fixtures | 89 captures with production staging/callback checks |
| Menu/retained-asset GL2 fixtures | Seven menus, implicit button idle/hover, and 24 pixel-exact Monika comparisons at three opacities on two backgrounds |
| Particle refactor | 252 before/after callback cases equivalent |
| Rollback/reference checks | Removed/retained SHA-256 checks and complete RPA extraction coverage passed |

The pre-existing lint warning about `story_cast_framing.rpy` init priority 1000
and recommendation to enable conflicting-property checks remain. Home's 229-second
chart endpoint is intentional and supported by the editor/runtime; its quieter
audio tail continues to 237.671875 seconds. The obsolete exact-duration test was
replaced with endpoint/bounds tests without changing authored chart or audio data.

Every engine probe used a private savedir, `MATSU_FRESH_RUN=1`, a pre-import
shared-write guard and before/after shared-state hashes. Runtime asserted private
active save locations. Shared state remained unchanged. GL2 evidence uses
synthetic fixtures and dummy audio; full routes, normal-speed/human input,
acoustic behavior, older/external save loading and packaged/protected builds were
not verified. This pass is not proof that every remaining algorithm is optimal.

Review and rollback artifacts are in `dev/maintenance/2026-09-25/`:
`source-before.zip`, `source-changes.patch`, `source-changes.json`,
`docs-before.zip`, `docs-changes.json`, `docs-link-check.json`,
`vanilla-assets-before.zip`, `vanilla-prune-manifest.json`,
`static-validation.json`, `story-presentation-qa/`, and `runtime-smoke-final/`.
The asset ZIP contains 267 originals, including the two GUI textures restored
after tracing implicit lookup; the manifest records the final 265 removals.
Final engine logs are under
`tmp/story_writer_20260913/qa/runs/maintenance_documented_{compile,lint}_20260925/`.

Recheck commands: `python tools/check_maintenance.py`,
`python tools/audit_asset_paths.py`,
`python dev/maintenance/2026-09-25/verify_vanilla_prune.py`, and
`python dev/maintenance/2026-09-25/docs_check.py`.
The static vanilla tool deliberately reports provenance and mentions, not an
automatic deletion verdict; dynamic references still need review.

Technical references checked against the installed SDK and current official
[distribution](https://www.renpy.org/doc/html/build.html),
[Python](https://www.renpy.org/doc/html/python.html), and
[command-line](https://www.renpy.org/doc/html/cli.html) documentation.
