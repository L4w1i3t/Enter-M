# Search-scope change — September 22, 2026

The September 22 audit attributed excessive agent context to unscoped recursive
searches. Adding `.rgignore` exclusions for generated sprite-audit evidence,
archived material, and temporary QA files reduced its representative matching
file count from 2,732 to 225 (91.8%). These are that run's measurements, not a
fresh inventory of this checkout.

The continuing practice is to start `rg` in the smallest relevant source
directory and name generated evidence explicitly when needed. The live
`.rgignore` defines the current exclusions; ignored search output does not
establish that a file is unused or absent.
