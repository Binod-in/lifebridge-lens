"""Prompt text tests: exact era rule, no doubled quotes.

Guards the /explain prompt wording: the era rule must read exactly as
specified, and broken string joins must never produce "" in the text
sent to the model.

Run from the project root:
    python -m unittest tests.test_prompt_text -v
"""
import io
import json
import unittest
from unittest import mock

import server


def _image_file(name="notice.jpg", size=1024):
    body = b"\xff\xd8\xff" + b"x" * max(0, size - 3)  # real JPEG magic bytes
    return (io.BytesIO(body), name, "image/jpeg")


def _api_reply(text):
    body = json.dumps({"choices": [{"message": {"content": text}}]}).encode("utf-8")
    resp = mock.MagicMock()
    resp.read.return_value = body
    ctx = mock.MagicMock()
    ctx.__enter__.return_value = resp
    ctx.__exit__.return_value = False
    return ctx


class PromptTextTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def _posted_prompt(self):
        seen = {}

        def fake_urlopen(req, timeout=120):
            seen["payload"] = json.loads(req.data.decode("utf-8"))
            return _api_reply("{}")

        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=fake_urlopen):
            data = {"photo": _image_file(), "language": "en"}
            res = self.client.post("/explain", data=data,
                                   content_type="multipart/form-data")
        self.assertEqual(res.status_code, 200)
        return seen["payload"]["messages"][0]["content"][0]["text"]

    def test_era_rule_reads_exactly(self):
        prompt = self._posted_prompt()
        self.assertIn(
            "- Convert Japanese era years to Western years in brackets, "
            "for example \u4ee4\u548c8\u5e74 becomes "
            "\"Reiwa 8 (2026)\".",
            prompt)

    def test_prompt_has_no_doubled_quotes(self):
        prompt = self._posted_prompt()
        self.assertNotIn('""', prompt)


if __name__ == "__main__":
    unittest.main()
