# Current source map

Checked September 25, 2026. Follow the code when this map and implementation
diverge; update this page in the same change that alters a public boundary.

| Responsibility | Source |
| --- | --- |
| New Game and shared session initialization | `game/script.rpy` |
| Available chapters and entry routing | `game/chapter_select.rpy` |
| Boot, first-run state and load handling | `game/splash.rpy`, `game/first_boot_notice.rpy` |
| Written campaign and exam behavior | `game/story/season1/`, `game/story/dependency_route.rpy` |
| Menus and preferences | `game/screens.rpy`, `game/archive.rpy`, `game/room_menu_theme.rpy` |
| Story scene presentation | `game/transforms.rpy`, `game/story_crowd_slots.rpy`, `game/story_cast_framing.rpy`, `game/stage_panels.rpy` |
| Atmosphere, shared effects and transitions | `game/atmosphere.rpy`, `game/fx.rpy`, `game/theater_fx.rpy`, `game/menu_doorway.rpy` |
| Shared art/audio declarations | `game/asset_definitions/` |
| Self-contained systems and modes | `game/addons/` |
| Effects Detail and Effects Resolution for the heavy modes | `game/graphics_detail.rpy`, `game/addons/Matsuda's Sick Boss Fight/perf.rpy` |
| Engine patch: transform state copy/compare fast path | `game/transform_fastpath.rpy` |
| Developer spec emulator (throttled performance testing) | `game/addons/Dev Hub/spec_emulator.rpy` |
| Engine-independent models | `game/python-packages/` |
| Developer authoring/recovery data | `dev/story_writer/` |
| Exam-guard regression probe | `dev/checks/exam_guard_runs.rpy` ([QA](QA.md)) |
| Packaging policy | `game/options.rpy` |

New Game initializes state and opens Chapter Select. Chapter availability is
based on entry-label existence. May 15–31 are implemented as 17 day files;
plans for later chapters are not evidence that those chapters can launch.
The dependency route retains its ledger and incomplete-manifest gate.

Arcade launch enters `arcade_run_context` before queuing the shared doorway.
The context owns temporary menu/gameplay flags and calls the requested label.
Do not queue a transition in the parent and assume it will survive entry.

Effects Detail (`enter_m_low_detail()`) is honored by Matsuda's fight and Id
Mode, Kotonoha, Tsubaki and the Archivist Invasions. Low may drop decoration
only: never a bullet, hazard, telegraph, hit flash, health readout or interface
element. A mode that adds a decorative layer decides at its own call site
whether Low drops it. A 60 Hz displayable reads the switch once per frame.
Thinning keys on a hash of each item's identity, never on its list index.
Effects Resolution (`persistent.msbf_gfx`) caps Biography's room through
`msbf_fx_scaled`. A capped pass adds a render of its own every frame, so route
a backdrop through it only after measuring that it gets cheaper (Matsuda's,
Tsubaki's and the other three rooms got slower). It never caps a pass that
also carries sprites or text.

`game/transform_fastpath.rpy` replaces two engine methods only while their
bytecode matches the Matsu'Py 8.6.0 build it was verified against. After an
SDK change, `TRANSFORM_FASTPATH_ACTIVE` reports whether it installed;
`TRANSFORM_FASTPATH_SHADOW = True` repeats the side-by-side check before you
re-fingerprint it.

Names used in Ren'Py source, labels, image attributes, screen actions, persistent
keys, and serialized state are compatibility boundaries. Rename local variables
for clarity only after checking those consumers. A string in a gallery/music
catalog can be a stable unlock key rather than a physical asset path.

Start searches in the owning directory. Inspect constructed paths, callbacks,
screen actions, registered images/audio, and archive-backed assets before
classifying an apparently unreferenced file as unused.

Use the [QA guide](QA.md) for bounded validation. Current behavior belongs here;
dated outcomes belong in [history](../history/README.md). Do not carry fixed
test counts or old screenshot approval forward as present evidence.
