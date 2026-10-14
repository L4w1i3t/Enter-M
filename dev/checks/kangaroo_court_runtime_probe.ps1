param([switch]$Run, [switch]$DeskLayers)
$ErrorActionPreference = 'Stop'
$probe = Join-Path $PSScriptRoot 'kangaroo_court_runtime_probe.py'
$probeArgs = @($probe)
if ($Run) { $probeArgs += '--run' }
if ($DeskLayers) { $probeArgs += '--desk-layers' }
& python @probeArgs
if ($LASTEXITCODE -ne 0) { throw "Courtroom runtime probe failed with exit $LASTEXITCODE." }
