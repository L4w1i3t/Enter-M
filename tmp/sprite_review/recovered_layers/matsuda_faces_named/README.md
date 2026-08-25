# Recovered Matsuda face sources

This directory contains 18 byte-exact pre-v2 source PNGs recovered from
loose Git blobs. The complete 56-blob nearest-expression inventory is in
`all_56_similarity.tsv`; only rows marked `exact_source` were recovered as named PNGs.

These are reference/source layers, not recommended drop-in game assets. Their retained
RGB agrees exactly with the installed feature masks, but the old alpha covers a broad,
nearly opaque head rectangle. The installed v2 feature-only alpha is cleaner and avoids
the baked background/seam risk.

No exact loose-blob source was found for: crying, disgusted, shocked.
`disgusted` was replaced from a newly generated source during v2 processing; `crying`
and `shocked` appear to have come from task intermediates that were never stored as
loose Git objects.
