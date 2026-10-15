# GitHub release indicator — October 14, 2026

The title screen checks `Lawliet/Enter-M` for a newer published stable release.
When one exists, a teal **New build available - view release** button appears
above the sidebar footer and opens
[the releases page](https://github.com/L4w1i3t/Enter-M/releases).

## Behavior

- One background request per game process, starting when the main menu is shown.
  Returning to the menu reuses the result. No polling timer or startup wait.
- The installed version is `config.version` in `game/options.rpy`, currently
  `0.17.0`. The GitHub release **tag**, not its display title, is compared.
- Uses GitHub's public `/repos/L4w1i3t/Enter-M/releases/latest` endpoint with
  API version `2026-03-10`, a User-Agent, and the JSON Accept header.
- Stable SemVer tags such as `0.18.0` or `v0.18.0` are supported. Numeric ordering
  handles `0.9.0` versus `0.10.0`; equal and older releases do not show an alert.
  Build metadata does not change ordering. Drafts, prereleases, and unrecognized
  tag/version formats cannot trigger a notice.
- Offline, timeout, HTTP errors (including an empty repository's 404), and
  malformed metadata leave the indicator hidden. Relaunching retries the check.
- HTTPS certificate and hostname verification use Ren'Py's bundled `certifi`
  trust roots. The request has an eight-second
  socket timeout and a 512 KiB response limit. No credentials or player data are
  sent. No assets are downloaded, installed, or executed.
- Results live in an imported Python module, outside gameplay saves and rollback.
  The worker passes completion to Ren'Py's main thread before changing the UI.
- Browser exports skip the check because Ren'Py's worker-thread API is unavailable
  there. Desktop source runtime is the validation target for this change.

## Publishing the next build

1. Set `config.version` to the version of the build being packaged.
2. Publish a public GitHub release with the matching tag, for example `v0.18.0`,
   attach the build, and designate it as the latest stable release.
3. A build containing this checker at `0.17.0` will show the notice for that
   `v0.18.0` release; the `0.18.0` build will not notify about itself.

Tags alone, drafts, prereleases, and replacing an asset under the same version
do not produce a new-version notice. Publish a higher version for a new build.

## Files

- `game/python-packages/enter_m_updates.py`: bounded HTTP fetch, SemVer comparison,
  and process-local checker state.
- `game/update_check.rpy`: Ren'Py threading bridge.
- `game/main_menu_room.rpy`: menu show/replace hooks and the clickable notice.
- `game/options.rpy`: version guidance and explicit module inclusion in the mod
  archive, following the existing Python module packaging convention; excludes
  the generated developer graph from distributions.
- `dev/checks/test_enter_m_updates.py`: deterministic logic/network-failure tests.
- `dev/checks/update_check_runtime_probe.py`: isolated title-screen runtime probe.

## Validation

On October 14, the repository became publicly readable during implementation.
An unauthenticated `GET /releases?per_page=5` succeeded with an empty list;
`GET /releases/latest` returned 404 as expected with no published release.
No GitHub release or repository setting was changed by this task.

- `python -B dev/checks/test_enter_m_updates.py`: all 12 tests pass on host Python.
  Covers numeric/prerelease ordering, stable-channel filtering, malformed and
  oversized responses, HTTP/offline/timeout errors, single-request behavior,
  and the asynchronous completion boundary. No network is used by this suite.
- The SDK's stripped Python does not include `unittest`; its integration is
  exercised by the separate actual-engine runtime probe instead.
- The first real SDK network probe found that its default SSL context could not
  validate GitHub's issuer. Supplying the SDK's existing `certifi` bundle to
  `ssl.create_default_context` fixed this; certificate verification remains on.
- Independent focused code review found no actionable defects.
- `git diff --check` passes.
- The inherited `C:\Users\Admin\AGENTS.md` requires `graphify update .`; the
  generated code graph is a developer artifact and excluded from releases.

- `python -B dev/checks/update_check_runtime_probe.py --run --live`: final pass,
  [runtime report](evidence/update-check-2026-10-14/run_20261014_011437/runtime.json)
  and [run summary](evidence/update-check-2026-10-14/run_20261014_011437/summary.json).
  MatsuPy/Ren'Py 8.6 GL2, 1280x720, Atmosphere Off, dummy audio; copied production
  title UI and checker, with unrelated menu destinations/prediction stubbed.
  Four scenarios exercised newer, equal, offline, and the real public endpoint.
  The live SDK request reached GitHub and returned the expected no-release 404.
  Assertions verified worker/main-thread separation, one request after a menu
  revisit, indicator visibility, button geometry, and the browser action's URL.
- [Newer-release screenshot](evidence/update-check-2026-10-14/run_20261014_011437/newer.png)
  was inspected: the complete teal label fits between the description and footer.
  Equal/offline/no-release cases keep that band empty.
- The final probe exited 0 in 7.54 seconds. `MATSU_FRESH_RUN=1`, private savedir,
  active-path assertions, and a write guard were used. All 38 shared save/token
  files retained their hashes and mtimes; zero outside writes were attempted.
  Disposable fixture and private test-state folders were removed afterward.
- Earlier run folders retain failed fixture diagnostics and the reproduced TLS
  failure. They are not passing evidence; the final run above supersedes them.

No full-project lint, protected distribution build, browser launch/build,
full-story run, or old-save playthrough is claimed.

## References checked during implementation

- [GitHub release API](https://docs.github.com/en/rest/releases/releases#get-the-latest-release)
- [Ren'Py background and main-thread calls](https://www.renpy.org/doc/html/other.html#renpy.invoke_in_thread)
- [Ren'Py fetch behavior](https://www.renpy.org/doc/html/fetch.html): using fetch
  inside a screen action blocks display updates, hence the separate worker.
- [Python urllib.request](https://docs.python.org/3/library/urllib.request.html)
- [Certifi trust bundle](https://github.com/certifi/python-certifi)
- [Python default TLS context](https://docs.python.org/3/library/ssl.html#ssl.create_default_context)
- [Semantic Versioning 2.0.0](https://semver.org/)

The installed MatsuPy 8.6 SDK's thread implementations were checked alongside
the current upstream documentation.
