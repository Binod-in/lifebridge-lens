"""Phase 5 tests: Communication Tutor practice output.

The /explain prompt requests a hiragana reading and practice
sentences, the staff card shows them with a read-aloud button, and
all labels exist in all four languages.

Run from the project root:
    python -m unittest tests.test_phase5 -v
"""
import io
import json
import os
import re
import unittest
from unittest import mock

import server

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("en", "ne", "vi", "my")
NEW_KEYS = ("explain.listen", "explain.noVoice", "explain.variations",
            "explain.sample.reading", "explain.sample.variations")


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


class Phase5PromptTest(unittest.TestCase):
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

    def test_prompt_requests_new_keys(self):
        prompt = self._posted_prompt()
        self.assertIn('"staff_reading"', prompt)
        self.assertIn('"staff_variations"', prompt)

    def test_prompt_reading_is_hiragana_only(self):
        prompt = self._posted_prompt()
        self.assertIn("hiragana", prompt)
        self.assertIn("only", prompt)

    def test_prompt_variations_have_meanings(self):
        prompt = self._posted_prompt()
        self.assertIn("3 short practice sentences", prompt)
        self.assertIn("in brackets", prompt)


class Phase5FrontendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_practice_ui_present(self):
        self.assertIn('id="result-staff-reading"', self.page)
        self.assertIn('id="listen-staff-btn"', self.page)
        self.assertIn('id="staff-practice"', self.page)
        self.assertIn('id="result-variations"', self.page)
        for key in ("explain.listen", "explain.noVoice",
                    "explain.variations", "explain.sample.reading",
                    "explain.sample.variations"):
            self.assertIn('"%s"' % key, self.page)

    def test_practice_parser_present(self):
        self.assertIn("function practiceFromReply(text)", self.page)
        self.assertIn("function fillStaffPractice(reading, variations)", self.page)
        self.assertIn("data.staff_reading", self.page)
        self.assertIn("data.staff_variations", self.page)

    def test_read_aloud_uses_japanese_voice(self):
        self.assertIn("speechSynthesis", self.page)
        self.assertIn('said.lang = "ja-JP"', self.page)
        self.assertIn("SpeechSynthesisUtterance(phrase)", self.page)


class Phase5TranslationTest(unittest.TestCase):
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


class Phase5CompatTest(unittest.TestCase):
    def test_staff_helpers_unchanged(self):
        page = _read("explain.html")
        self.assertIn("function staffFromReply(text)", page)
        self.assertIn("function fillStaff(phrase, meaning)", page)
        self.assertIn('id="copy-staff-btn"', page)

    def test_staff_styles_kept(self):
        css = _read("style.css")
        self.assertIn(".staff-vars {", css)
        self.assertIn('html[data-theme="dark"] .staff-vars', css)


if __name__ == "__main__":
    unittest.main()
