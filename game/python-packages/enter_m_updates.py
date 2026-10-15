"""Read-only GitHub release checks; process state stays out of Ren'Py saves."""

import json
import re
import urllib.request


REPOSITORY = "L4w1i3t/Enter-M"
RELEASES_URL = "https://github.com/" + REPOSITORY + "/releases"
API_URL = "https://api.github.com/repos/" + REPOSITORY + "/releases/latest"
REQUEST_TIMEOUT = 8
MAX_RESPONSE_BYTES = 512 * 1024

_VERSION = re.compile(
    r"[vV]?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)


def version_key(value):
    """A comparable SemVer key, or None for an unrecognized release tag."""
    if not isinstance(value, str) or len(value) > 64:
        return None
    match = _VERSION.fullmatch(value.strip())
    if match is None:
        return None
    core = tuple(int(part) for part in match.group(1, 2, 3))
    prerelease = match.group(4)
    if prerelease is None:
        return core, 1, ()
    identifiers = []
    for part in prerelease.split("."):
        if part.isdigit():
            if len(part) > 1 and part.startswith("0"):
                return None
            identifiers.append((0, int(part)))
        else:
            identifiers.append((1, part))
    return core, 0, tuple(identifiers)


def newer_release_version(release, current_version):
    """Only a valid, published stable version can light the indicator."""
    if not isinstance(release, dict):
        return None
    if release.get("draft") is not False or release.get("prerelease") is not False:
        return None
    current = version_key(current_version)
    tag = release.get("tag_name")
    latest = version_key(tag)
    if current is None or latest is None or latest[1] != 1 or latest <= current:
        return None
    return tag.strip().lstrip("vV")


def fetch_latest_release():
    """Fetch public metadata only, with TLS verification and bounded input."""
    # Ren'Py bundles certifi with Requests. Its embedded Python may not find
    # usable system roots through ssl's default paths (notably on Windows).
    import certifi
    import ssl

    request = urllib.request.Request(API_URL, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "ENTER-M-release-check",
        "X-GitHub-Api-Version": "2026-03-10",
    })
    context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT, context=context) as response:
        payload = response.read(MAX_RESPONSE_BYTES + 1)
    if len(payload) > MAX_RESPONSE_BYTES:
        raise ValueError("Release metadata exceeds the size limit")
    return json.loads(payload.decode("utf-8"))


class UpdateChecker:
    """Check once per process; dispatch the result back to the UI thread."""

    def __init__(self):
        self.state = "idle"
        self.available_version = None

    def start(self, current_version, launch, dispatch, refresh):
        # Called only from the UI thread. Menu revisits and interaction restarts
        # reuse the result, including failures, instead of repeatedly hitting GitHub.
        if self.state != "idle":
            return
        self.state = "checking"
        try:
            launch(self._worker, current_version, dispatch, refresh)
        except Exception:
            # An optional notification must never prevent entering the game.
            self.state = "unavailable"

    def _worker(self, current_version, dispatch, refresh):
        try:
            release = fetch_latest_release()
            version = newer_release_version(release, current_version)
            state = "available" if version else "no_update"
        except Exception:
            # Includes offline, timeout, rate limits, no public releases (404),
            # and malformed metadata. Retry on the next launch, without a popup.
            version, state = None, "unavailable"
        dispatch(self._finish, version, state, refresh)

    def _finish(self, version, state, refresh):
        self.available_version = version
        self.state = state
        refresh()


# Imported Python module state is neither rolled back nor restored by old saves.
checker = UpdateChecker()
