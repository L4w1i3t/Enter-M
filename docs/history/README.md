# Version history and patch notes

This partition records changes and superseded design context. Consult the
[current source map](../engineering/CURRENT_CODE.md) for implemented behavior.

- [July–September story revisions](story-revisions.md)
- [August–September presentation and authoring](presentation.md)
- [September rhythm-mode revisions](rhythm.md)
- [Asset revision history](asset-revisions.md)
- [Audio research and cue changes](audio.md)
- [Earlier character and long-range story design](early-story-design.md)
- [September 22 search-scope improvement](2026-09-22-token-efficiency.md)
- [September 25 textbox preference](2026-09-25-textbox-default-opacity.md)
- [September 25 codebase maintenance](2026-09-25-codebase-maintenance.md)
- [September 26 story cast presentation](2026-09-26-cast-presentation.md)
- [September 30 Kotonoha boss sprite rebuild and Endless Practice](2026-09-30-kotonoha-boss-facelift.md)
- [October 1 Ontological Seer formation rebuild and Monika's scale](2026-10-01-seer-formation-rebuild.md)
- [October 2 Archivist Invasions makeover and Mystery's witness lineup](2026-10-02-invasions-makeover.md)
- [October 9 stress test, spec emulation and Effects Detail](2026-10-09-stress-test-and-low-detail.md)

The September 25 documentation consolidation replaced repeated task narratives,
stale line-by-line audits, old QA counts, and redundant inventories with these
summaries and source-linked current guides. Historical test results have not
been rerun simply by moving them into this partition.

The reversible baseline is outside the active documentation tree:
`dev/maintenance/2026-09-25/docs-before.zip`. Its matching `docs-before.json`
records every original Markdown/text path, byte count, SHA-256, and modification
time in UTC. `docs-changes.json` records the consolidation. The ZIP preserves
pre-existing working-copy content, including uncommitted edits; it is not a
replacement for repository history. It contains neither game assets nor saves.
`docs-review-pages-before.zip` and its matching JSON separately preserve the
three existing HTML review pages before two obsolete navigation links were
repaired; their artwork and review controls were not changed.

For a new patch note, record the concrete change, affected source, checks that
actually ran, and remaining coverage. Update the corresponding current guide
when behavior changes. Keep obsolete implementation recipes in history only.
