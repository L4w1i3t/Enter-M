<#
.SYNOPSIS
Retired legacy processor for Asahina's generated sprite masters.

.DESCRIPTION
The old implementation copied generated faces at fixed coordinates and rebuilt
pose alpha from an opaque checkerboard extraction. That workflow produced the
misregistered expressions, broad face seams, and hard pale pose fringes this
project's canonical assets have since replaced.

Do not re-enable it without preserving the current per-expression registration,
feature-only masks, shared casual/uniform silhouette, and decontaminated soft
alpha edges in game/mod_assets/char_sprites/asahina.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourceDirectory,

    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory
)

$ErrorActionPreference = "Stop"

throw "process_asahina_sprites.ps1 is retired because its fixed-coordinate extraction would regress the canonical repaired sprites."
