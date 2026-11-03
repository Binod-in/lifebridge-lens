"""Slim first-scan tests: fewer keys, short values, timing logs.

The first scan asks only for the core keys; payment details,
consequences, markers, and practice variations moved to follow-up
chips. The frontend hides those cards when the keys are missing,
and the server logs how long each Meta API call takes.

Run from the project root:
    python -m unittest tests.test_slim_scan -v
"""
import contextlib
import io
import json
import os
import re
import unittest
from unittest import mock

import server

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("en", "ne", "vi", "my")

NEW_KEYS = (
    "explain.needPhotoFirst",
    "explain.qHowPay",
    "explain.qIfNotPay",
    "explain.qMorePhrases",
)

KEPT_KEYS = (
    "what", "kind", "why", "importance", "next_steps", "deadline",
    "deadline_date", "amount", "staff_phrase", "staff_phrase_meaning",
    "staff_reading", "check",
)

REMOVED_KEYS = (
    "staff_variations", "payment_methods", "consequences", "markers",
    "payment_codes", "payment_steps",
)


def _read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


def _lang_block(src, lang):
    match = re.search(
        r"\n        " + lang + r": \{(.*?)(?:\n        (?:en|ne|vi|my): \{|\n    \};)",
        src,
        re.S,
    )
    if not match:
        raise AssertionError("language block not found: " + lang)
    return match.group(1)


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


class SlimPromptTest(unittest.TestCase):
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

    def test_slim_key_set(self):
        prompt = self._posted_prompt()
        for key in KEPT_KEYS:
            self.assertIn('"%s"' % key, prompt)
        for key in REMOVED_KEYS:
            self.assertNotIn('"%s"' % key, prompt)

    def test_shortness_rule(self):
        prompt = self._posted_prompt()
        self.assertIn("at most 2 sentences", prompt)
        self.assertIn("next_steps at most", prompt)
        self.assertIn("4 short steps", prompt)
        self.assertIn("Do not use markdown", prompt)


class ApiTimingTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def _logged_output(self, post):
        buf = io.StringIO()

        def fake_urlopen(req, timeout=120):
            return _api_reply("{}")

        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=fake_urlopen):
            with contextlib.redirect_stdout(buf):
                res = post()
        self.assertEqual(res.status_code, 200)
        return buf.getvalue()

    def test_explain_logs_duration(self):
        out = self._logged_output(lambda: self.client.post(
            "/explain",
            data={"photo": _image_file(), "language": "en"},
            content_type="multipart/form-data"))
        self.assertRegex(out, r"explain took \d+\.\ds")

    def test_ask_logs_duration(self):
        out = self._logged_output(lambda: self.client.post(
            "/ask", json={"question": "Is this urgent?",
                          "language": "en"}))
        self.assertRegex(out, r"ask took \d+\.\ds")


class HideMissingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_optional_cards_hide_when_missing(self):
        for marker in ("function updateOptionalCards(sections)",
                       '"result-payment", "result-codes", "result-paysteps"',
                       'closest("article")',
                       '"result-consequences"',
                       "updateOptionalCards(sections);"):
            self.assertIn(marker, self.page)

    def test_sample_shows_all_cards(self):
        self.assertIn('updateOptionalCards({ "result-payment": "x"',
                      self.page)

    def test_followup_chips_for_removed_info(self):
        for marker in ('"explain.qHowPay"', '"explain.qIfNotPay"'):
            self.assertIn(marker, self.page)

    def test_only_four_followup_chips(self):
        start = self.page.index('class="chip-row"')
        end = self.page.index("</div>", start)
        block = self.page[start:end]
        self.assertEqual(block.count('class="chip"'), 4)
        for marker in ('"explain.qStepByStep"', '"explain.qHowPay"',
                       '"explain.qIfNotPay"', '"explain.qWhere"'):
            self.assertIn(marker, block)
        for marker in ('"explain.qDeadline"', '"explain.qDocs"',
                       '"explain.qUrgent"', '"explain.qMorePhrases"'):
            self.assertNotIn(marker, block)


class SlimTranslationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        src = _read("i18n.js")
        cls.blocks = {lang: _lang_block(src, lang) for lang in LANGS}

    def test_new_keys_in_all_four_languages(self):
        for key in NEW_KEYS:
            for lang in LANGS:
                match = re.search(r'"%s": "(.*?)"' % re.escape(key),
                                  self.blocks[lang])
                self.assertTrue(match, "%s missing in %s" % (key, lang))
                self.assertTrue(match.group(1).strip(),
                                "%s is empty in %s" % (key, lang))

    def test_new_keys_have_no_em_or_en_dash(self):
        for lang in LANGS:
            for key in NEW_KEYS:
                match = re.search(r'"%s": "(.*?)"' % re.escape(key),
                                  self.blocks[lang])
                value = match.group(1)
                self.assertNotIn("\u2014", value, "%s %s" % (key, lang))
                self.assertNotIn("\u2013", value, "%s %s" % (key, lang))


if __name__ == "__main__":
    unittest.main()
