"""Security regression tests: static allowlist, upload checks, rate limits.

Run from the project root (Flask must be installed):
    python -m unittest tests.test_security -v
"""
import io
import json
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import server


def _api_reply(text):
    body = json.dumps({"choices": [{"message": {"content": text}}]}).encode("utf-8")
    resp = mock.MagicMock()
    resp.read.return_value = body
    ctx = mock.MagicMock()
    ctx.__enter__.return_value = resp
    ctx.__exit__.return_value = False
    return ctx


def _image_file(name="notice.jpg", size=1024):
    body = b"\xff\xd8\xff" + b"x" * max(0, size - 3)  # real JPEG magic bytes
    return (io.BytesIO(body), name, "image/jpeg")


class StaticAllowlistTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()

    def test_public_files_allowed(self):
        for path in ["/", "/index.html", "/style.css", "/explain.html"]:
            res = self.client.get(path)
            try:
                self.assertEqual(res.status_code, 200, path)
            finally:
                res.close()

    def test_backend_files_blocked(self):
        for path in ["/server.py", "/requirements.txt", "/.env.example",
                     "/tests/test_ask.py", "/.gitignore"]:
            res = self.client.get(path)
            self.assertEqual(res.status_code, 404, path)


class UploadValidationTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def test_non_image_rejected(self):
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=lambda req, timeout=120: _api_reply("ok")):
            data = {"photo": (io.BytesIO(b"not an image"), "note.txt", "text/plain"),
                    "language": "en"}
            res = self.client.post("/explain", data=data,
                                   content_type="multipart/form-data")
        self.assertEqual(res.status_code, 400)

    def test_oversize_rejected(self):
        old = server.MAX_UPLOAD_BYTES
        server.MAX_UPLOAD_BYTES = 100
        try:
            with mock.patch.object(server.urllib.request, "urlopen",
                                   side_effect=lambda req, timeout=120: _api_reply("ok")):
                data = {"photo": _image_file(size=200), "language": "en"}
                res = self.client.post("/explain", data=data,
                                       content_type="multipart/form-data")
        finally:
            server.MAX_UPLOAD_BYTES = old
        self.assertEqual(res.status_code, 413)

    def test_fake_image_rejected(self):
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=lambda req, timeout=120: _api_reply("ok")):
            data = {"photo": (io.BytesIO(b"this is not photo data at all"),
                              "fake.jpg", "image/jpeg"),
                    "language": "en"}
            res = self.client.post("/explain", data=data,
                                   content_type="multipart/form-data")
        self.assertEqual(res.status_code, 400)


class ImageKindTest(unittest.TestCase):
    def test_magic_bytes(self):
        self.assertEqual(server._image_kind(b"\xff\xd8\xff" + b"0" * 20), "image/jpeg")
        self.assertEqual(server._image_kind(b"\x89PNG\r\n\x1a\n" + b"0" * 20), "image/png")
        self.assertEqual(server._image_kind(b"RIFF1234WEBP" + b"0" * 20), "image/webp")
        self.assertEqual(server._image_kind(b"GIF89a" + b"0" * 20), "")
        self.assertEqual(server._image_kind(b"hello"), "")
        self.assertEqual(server._image_kind(b""), "")


class ExplainSuccessTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def test_explain_returns_text(self):
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=lambda req, timeout=120: _api_reply("What is this?\nA gas bill.")):
            data = {"photo": _image_file(), "language": "ne"}
            res = self.client.post("/explain", data=data,
                                   content_type="multipart/form-data")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {"text": "What is this?\nA gas bill."})

    def test_meta_error_is_sanitized(self):
        err = server.urllib.error.HTTPError(
            "https://api.meta.ai/v1/chat/completions", 401, "Unauthorized", {}, None)

        def fake_urlopen(req, timeout=120):
            raise err

        with mock.patch.object(server.urllib.request, "urlopen", side_effect=fake_urlopen):
            data = {"photo": _image_file(), "language": "en"}
            res = self.client.post("/explain", data=data,
                                   content_type="multipart/form-data")
        self.assertEqual(res.status_code, 502)
        self.assertNotIn("401", res.get_json()["error"])
        self.assertIn("try again", res.get_json()["error"])


class SecurityHeadersTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()

    def test_headers_present(self):
        res = self.client.get("/")
        try:
            self.assertIn("Content-Security-Policy", res.headers)
            self.assertIn("Strict-Transport-Security", res.headers)
            self.assertIn("Permissions-Policy", res.headers)
            self.assertEqual(res.headers["X-Content-Type-Options"], "nosniff")
            self.assertEqual(res.headers["X-Frame-Options"], "DENY")
            self.assertIn("camera=(self)", res.headers["Permissions-Policy"])
        finally:
            res.close()

    def test_cache_headers(self):
        res = self.client.get("/style.css")
        try:
            self.assertIn("max-age=86400", res.headers.get("Cache-Control", ""))
        finally:
            res.close()
        res = self.client.get("/")
        try:
            self.assertIn("no-cache", res.headers.get("Cache-Control", ""))
        finally:
            res.close()


class AccessControlTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        self._token = server.API_TOKEN
        server.API_KEY = "test-key"
        server.API_TOKEN = ""
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server.API_TOKEN = self._token
        server._reset_rate_limits()

    def test_cross_site_origin_rejected(self):
        res = self.client.post("/ask", json={"question": "Hi?", "language": "en"},
                               headers={"Origin": "https://evil.example"})
        self.assertEqual(res.status_code, 403)

    def test_same_origin_allowed(self):
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=lambda req, timeout=120: _api_reply("ok")):
            res = self.client.post("/ask", json={"question": "Hi?", "language": "en"},
                                   headers={"Origin": "http://localhost"})
        self.assertEqual(res.status_code, 200)

    def test_token_required_when_set(self):
        server.API_TOKEN = "s3cret"
        res = self.client.post("/ask", json={"question": "Hi?", "language": "en"})
        self.assertEqual(res.status_code, 401)
        res = self.client.post("/ask", json={"question": "Hi?", "language": "en"},
                               headers={"X-LB-Token": "wrong"})
        self.assertEqual(res.status_code, 401)
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=lambda req, timeout=120: _api_reply("ok")):
            res = self.client.post("/ask", json={"question": "Hi?", "language": "en"},
                                   headers={"X-LB-Token": "s3cret"})
        self.assertEqual(res.status_code, 200)

    def test_non_ascii_token_rejected_not_crash(self):
        server.API_TOKEN = "s3cret"
        res = self.client.post("/ask", json={"question": "Hi?", "language": "en"},
                               headers={"X-LB-Token": "sécret"})
        self.assertEqual(res.status_code, 401)

    def test_lb_config_serves_token(self):
        server.API_TOKEN = "s3cret"
        res = self.client.get("/lb-config.js")
        self.assertEqual(res.status_code, 200)
        self.assertIn("application/javascript",
                      res.headers.get("Content-Type", ""))
        self.assertIn("no-store", res.headers.get("Cache-Control", ""))
        self.assertEqual(res.get_data(as_text=True),
                         'window.LB_API_TOKEN = "s3cret";')

    def test_lb_config_empty_without_token(self):
        res = self.client.get("/lb-config.js")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(as_text=True), "")

    def test_lb_config_escapes_token(self):
        server.API_TOKEN = 'a"b\\c'
        res = self.client.get("/lb-config.js")
        self.assertEqual(res.get_data(as_text=True),
                         'window.LB_API_TOKEN = "a\\"b\\\\c";')


class ProxyRateLimitTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        self._ask_limit = server.ASK_LIMIT
        self._proxy = server.TRUST_PROXY
        server.API_KEY = "test-key"
        server.ASK_LIMIT = 1
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server.ASK_LIMIT = self._ask_limit
        server.TRUST_PROXY = self._proxy
        server._reset_rate_limits()

    def _ask(self, xff=None):
        headers = {"X-Forwarded-For": xff} if xff else {}
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=lambda req, timeout=120: _api_reply("ok")):
            return self.client.post("/ask", json={"question": "Hi?", "language": "en"},
                                    headers=headers)

    def test_forwarded_ip_used_when_trusted(self):
        server.TRUST_PROXY = True
        self.assertEqual(self._ask("1.2.3.4").status_code, 200)
        self.assertEqual(self._ask("1.2.3.4").status_code, 429)
        self.assertEqual(self._ask("5.6.7.8").status_code, 200)

    def test_forwarded_ip_ignored_when_untrusted(self):
        server.TRUST_PROXY = False
        self.assertEqual(self._ask("1.2.3.4").status_code, 200)
        self.assertEqual(self._ask("5.6.7.8").status_code, 429)

    def test_rate_buckets_are_capped(self):
        for i in range(5005):
            server._rate_limited(("ask", "10.0.0.%d" % i), 30)
        self.assertLess(len(server._rate_hits), 5005)

    def test_full_table_evicts_oldest_not_all(self):
        for i in range(server.RATE_BUCKET_CAP):
            server._rate_limited(("ask", "ip-%d" % i), 100)
        victim = ("ask", "ip-%d" % (server.RATE_BUCKET_CAP - 1))
        for _ in range(99):
            self.assertFalse(server._rate_limited(victim, 100))
        self.assertTrue(server._rate_limited(victim, 100))
        # A new visitor triggers eviction of the oldest bucket only.
        server._rate_limited(("ask", "newcomer"), 100)
        self.assertLessEqual(len(server._rate_hits), server.RATE_BUCKET_CAP)
        self.assertNotIn(("ask", "ip-0"), server._rate_hits)
        self.assertTrue(server._rate_limited(victim, 100))


class AskValidationTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def test_long_question_rejected(self):
        res = self.client.post("/ask", json={"question": "x" * 2001, "language": "en"})
        self.assertEqual(res.status_code, 400)

    def test_long_explanation_rejected(self):
        res = self.client.post("/ask", json={"question": "Hi?", "language": "en",
                                             "explanation": "y" * 8001})
        self.assertEqual(res.status_code, 400)

    def test_bad_image_rejected(self):
        for image in ["not-a-data-uri",
                      "data:image/gif;base64,/9j/2Q==",
                      "data:image/jpeg;base64,aGVsbG8="]:
            res = self.client.post("/ask", json={"question": "Hi?", "language": "en",
                                                 "image": image})
            self.assertEqual(res.status_code, 400, image)


class NotFoundTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()

    def test_api_path_returns_json_404(self):
        res = self.client.get("/explain/nope")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.get_json(), {"error": "Not found."})

    def test_page_path_returns_html_404(self):
        res = self.client.get("/missing-page.html")
        self.assertEqual(res.status_code, 404)
        self.assertIn(b"Page not found", res.data)

    def test_dot_segments_rejected(self):
        res = self.client.get("/a/../server.py")
        self.assertEqual(res.status_code, 404)


class RateLimitTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        self._explain = server.EXPLAIN_LIMIT
        self._ask = server.ASK_LIMIT
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server.EXPLAIN_LIMIT = self._explain
        server.ASK_LIMIT = self._ask
        server._reset_rate_limits()

    def test_explain_rate_limited(self):
        server.EXPLAIN_LIMIT = 2
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=lambda req, timeout=120: _api_reply("What is this?\nA bill.")):
            for _ in range(2):
                data = {"photo": _image_file(), "language": "en"}
                res = self.client.post("/explain", data=data,
                                       content_type="multipart/form-data")
                self.assertEqual(res.status_code, 200)
            data = {"photo": _image_file(), "language": "en"}
            res = self.client.post("/explain", data=data,
                                   content_type="multipart/form-data")
            self.assertEqual(res.status_code, 429)

    def test_ask_rate_limited(self):
        server.ASK_LIMIT = 2
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=lambda req, timeout=120: _api_reply("Pay at a store.")):
            for _ in range(2):
                res = self.client.post("/ask", json={"question": "Where?", "language": "en"})
                self.assertEqual(res.status_code, 200)
            res = self.client.post("/ask", json={"question": "Where?", "language": "en"})
            self.assertEqual(res.status_code, 429)

    def test_empty_bucket_key_removed(self):
        # A bucket whose hits all expired must not stay in memory.
        server._rate_hits["old-ip"] = [-1000000.0]
        server._rate_limited("old-ip", 0)
        self.assertNotIn("old-ip", server._rate_hits)


if __name__ == "__main__":
    unittest.main()
