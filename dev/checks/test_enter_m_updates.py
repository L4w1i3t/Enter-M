"""Offline regression checks: python -B dev/checks/test_enter_m_updates.py."""

import importlib.util
import io
import json
from pathlib import Path
import ssl
import unittest
from unittest import mock
from urllib.error import HTTPError, URLError

import certifi


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "game" / "python-packages" / "enter_m_updates.py"
)
SPEC = importlib.util.spec_from_file_location("enter_m_updates_under_test", MODULE_PATH)
updates = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(updates)


def release(tag="v1.2.4", **fields):
    result = {"tag_name": tag, "draft": False, "prerelease": False}
    result.update(fields)
    return result


class VersionTests(unittest.TestCase):
    def test_current_older_and_newer_versions(self):
        for tag, expected in (
            ("1.2.2", None),
            ("1.2.3", None),
            ("1.2.4", "1.2.4"),
            ("1.10.0", "1.10.0"),
            ("2.0.0", "2.0.0"),
        ):
            with self.subTest(tag=tag):
                self.assertEqual(
                    updates.newer_release_version(release(tag), "1.2.3"), expected
                )

    def test_v_prefix_and_build_metadata(self):
        self.assertEqual(
            updates.newer_release_version(release(" V1.2.4+desktop "), "v1.2.3"),
            "1.2.4+desktop",
        )
        self.assertIsNone(
            updates.newer_release_version(release("v1.2.3+new"), "1.2.3+old")
        )

    def test_semver_prerelease_precedence(self):
        versions = [
            "1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta",
            "1.0.0-beta", "1.0.0-beta.2", "1.0.0-beta.11",
            "1.0.0-rc.1", "1.0.0",
        ]
        for older, newer in zip(versions, versions[1:]):
            with self.subTest(older=older, newer=newer):
                self.assertLess(updates.version_key(older), updates.version_key(newer))
        self.assertEqual(
            updates.newer_release_version(release("v1.0.0"), "1.0.0-rc.1"),
            "1.0.0",
        )

    def test_only_published_stable_releases_are_offered(self):
        for metadata in (
            release(draft=True), release(prerelease=True),
            release("2.0.0-beta.1"), release(draft=None),
            release(prerelease=0), {"tag_name": "2.0.0"},
        ):
            with self.subTest(metadata=metadata):
                self.assertIsNone(updates.newer_release_version(metadata, "1.0.0"))

    def test_unrecognized_versions_do_not_offer_an_update(self):
        for invalid in (
            None, 123, "", "latest", "1.2", "01.2.3", "1.2.3.4",
            "1.2.3-beta.01", "1.2.3-", "1.2.3+", "x" * 65,
        ):
            with self.subTest(invalid=invalid):
                self.assertIsNone(updates.version_key(invalid))
                self.assertIsNone(updates.newer_release_version(release(invalid), "1.0.0"))
                self.assertIsNone(updates.newer_release_version(release(), invalid))

    def test_non_object_metadata_cannot_offer_an_update(self):
        for invalid in (None, [], "v9.0.0", 1):
            with self.subTest(invalid=invalid):
                self.assertIsNone(updates.newer_release_version(invalid, "1.0.0"))


class FetchTests(unittest.TestCase):
    def response(self, payload):
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = payload
        return response

    def test_public_metadata_request_is_bounded_and_has_no_credentials(self):
        metadata = release()
        response = self.response(json.dumps(metadata).encode("utf-8"))
        with mock.patch.object(ssl, "create_default_context", wraps=ssl.create_default_context) as tls:
            with mock.patch.object(updates.urllib.request, "urlopen", return_value=response) as get:
                self.assertEqual(updates.fetch_latest_release(), metadata)
        tls.assert_called_once_with(cafile=certifi.where())
        context = get.call_args.kwargs["context"]
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)
        request = get.call_args.args[0]
        self.assertEqual(request.full_url, updates.API_URL)
        self.assertEqual(request.get_method(), "GET")
        self.assertIsNone(request.data)
        headers = {name.lower(): value for name, value in request.header_items()}
        self.assertNotIn("authorization", headers)
        self.assertIn("user-agent", headers)
        self.assertEqual(headers["accept"], "application/vnd.github+json")
        self.assertGreater(get.call_args.kwargs["timeout"], 0)
        self.assertLessEqual(get.call_args.kwargs["timeout"], 10)
        response.read.assert_called_once_with(updates.MAX_RESPONSE_BYTES + 1)

    def test_malformed_or_oversized_payload_is_rejected(self):
        for payload in (b"not json", b"\xff", b"x" * (updates.MAX_RESPONSE_BYTES + 1)):
            with self.subTest(size=len(payload), prefix=payload[:12]):
                response = self.response(payload)
                with mock.patch.object(updates.urllib.request, "urlopen", return_value=response):
                    with self.assertRaises((ValueError, UnicodeError)):
                        updates.fetch_latest_release()


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.checker = updates.UpdateChecker()
        self.jobs = []
        self.ui_calls = []
        self.refresh = mock.Mock()

    def launch(self, callback, *args):
        self.jobs.append((callback, args))

    def dispatch(self, callback, *args):
        self.ui_calls.append((callback, args))

    def start(self):
        self.checker.start("1.2.3", self.launch, self.dispatch, self.refresh)

    def run_next(self, queue):
        callback, args = queue.pop(0)
        callback(*args)

    def test_one_request_and_no_ui_result_until_dispatch(self):
        with mock.patch.object(updates, "fetch_latest_release", return_value=release()) as fetch:
            self.start()
            self.start()
            self.assertEqual(len(self.jobs), 1)
            self.assertEqual(self.checker.state, "checking")
            fetch.assert_not_called()
            self.run_next(self.jobs)
            self.start()
            self.assertEqual(self.jobs, [])
            self.assertEqual(self.checker.state, "checking")
            self.assertIsNone(self.checker.available_version)
            self.refresh.assert_not_called()
            self.assertEqual(len(self.ui_calls), 1)
            self.run_next(self.ui_calls)
            self.assertEqual(self.checker.state, "available")
            self.assertEqual(self.checker.available_version, "1.2.4")
            self.refresh.assert_called_once_with()
            self.start()
            self.assertEqual(self.jobs, [])
            fetch.assert_called_once_with()

    def test_no_indicator_for_equal_older_or_ineligible_release(self):
        for metadata in (release("1.2.3"), release("1.2.2"), release(prerelease=True), []):
            with self.subTest(metadata=metadata):
                self.setUp()
                with mock.patch.object(updates, "fetch_latest_release", return_value=metadata):
                    self.start()
                    self.run_next(self.jobs)
                    self.run_next(self.ui_calls)
                self.assertEqual(self.checker.state, "no_update")
                self.assertIsNone(self.checker.available_version)

    def test_http_and_connection_failures_are_quiet_and_not_retried(self):
        errors = [
            HTTPError(updates.API_URL, code, "test failure", {}, io.BytesIO())
            for code in (404, 403, 429, 500)
        ] + [URLError("offline"), TimeoutError("timeout"), ValueError("bad metadata")]
        for error in errors:
            if isinstance(error, HTTPError):
                self.addCleanup(error.close)
            with self.subTest(error=str(error)):
                self.setUp()
                with mock.patch.object(updates.urllib.request, "urlopen", side_effect=error) as get:
                    self.start()
                    self.run_next(self.jobs)
                    self.assertEqual(self.checker.state, "checking")
                    self.assertIsNone(self.checker.available_version)
                    self.refresh.assert_not_called()
                    self.run_next(self.ui_calls)
                    self.assertEqual(self.checker.state, "unavailable")
                    self.assertIsNone(self.checker.available_version)
                    self.refresh.assert_called_once_with()
                    self.start()
                    self.assertEqual(self.jobs, [])
                    get.assert_called_once()

    def test_worker_launch_failure_does_not_interrupt_game_or_retry(self):
        launch = mock.Mock(side_effect=RuntimeError("thread unavailable"))
        for _ in range(2):
            self.checker.start("1.2.3", launch, self.dispatch, self.refresh)
        self.assertEqual(self.checker.state, "unavailable")
        self.assertIsNone(self.checker.available_version)
        self.assertEqual(self.ui_calls, [])
        self.refresh.assert_not_called()
        launch.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
