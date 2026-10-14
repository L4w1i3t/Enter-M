# Validation

Run from the project root. Choose checks relevant to the changed system;
successful static checks do not imply that every story route or asset has
played correctly.

## Lint

Lint is not read-only: it compiles scripts and saves persistent on exit. Give
it a private TEMP, save directory and fresh-run flag, which also lets it run
beside an open game. Write its output to a file; a piped stdout makes it exit
silently.

```powershell
$sdk = (Resolve-Path "..\..\RenPy 8\matsupy-sdk-860").Path
$t = "$env:LOCALAPPDATA\Temp\enterm-qa"
New-Item -ItemType Directory -Force "$t\saves" | Out-Null
$env:TEMP = $t; $env:TMP = $t; $env:MATSU_FRESH_RUN = "1"
Start-Process "$sdk\matsupy.exe" -ArgumentList "`"$PWD`"","--savedir","`"$t\saves`"","lint","`"$t\lint.txt`"" -NoNewWindow -Wait -RedirectStandardOutput "$t\out.txt"
Get-Content "$t\lint.txt"
```

Trust the result only if the report contains "dialogue blocks, containing".

## Orphaned compiled scripts

Ren'Py loads a `.rpyc` whose `.rpy` is gone. This must print nothing:

```powershell
Get-ChildItem game -Recurse -Filter *.rpyc | Where-Object { -not (Test-Path ($_.FullName -replace '\.rpyc$','.rpy')) }
```

## Exam guard

`dev/checks/exam_guard_runs.rpy` plays caught, clean and bad-ending runs side
by side and checks which ledger each load sees. With the lint environment above:

```powershell
$env:RENPY_SEARCHPATH = (Resolve-Path dev\checks).Path
$env:EG_PROBE_OUT = "$t\exam_guard.txt"
Start-Process "$sdk\matsupy.exe" -ArgumentList "`"$PWD`"","--savedir","`"$t\saves`"" -NoNewWindow -Wait
Get-Content "$t\exam_guard.txt"
```

Every line must start with `PASS`.

## Evidence

An exit code of zero is insufficient if logs contain a traceback or permission
error. Preserve failed-run evidence; do not turn an isolation failure into a
passing claim because the intended fixture completed.

GL2 captures use controlled fixtures and dummy audio. They establish only the
scenes and assertions actually exercised. Human navigation, focus/Alt-Tab,
audible synchronization, ordinary-speed reading, branch coverage, and packaged
runtime need their own checks. Historical evidence can be useful comparison
material but must be identified by date and source revision. See
[history](../history/README.md).
