"""Phase 1 tests: payment_methods and consequences fields.

The /explain prompt requests two new JSON fields, the frontend parses
them into result cards, the sample notice fills them, and all labels
exist in all four languages.

Run from the project root:
    python -m unittest tests.test_phase1 -v
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
NEW_KEYS = ("explain.hPayment", "explain.hConsequences",
            "explain.sample.payment", "explain.sample.consequences")


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


class Phase1PromptTest(unittest.TestCase):
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
        self.assertIn('"payment_methods"', prompt)
        self.assertIn('"consequences"', prompt)

    def test_prompt_forbids_invented_payment_details(self):
        prompt = self._posted_prompt()
        self.assertIn("Never invent a", prompt)
        self.assertIn("QR code, barcode, or payment number", prompt)

    def test_prompt_forbids_invented_fine_amounts(self):
        prompt = self._posted_prompt()
        self.assertIn("Never invent", prompt)
        self.assertIn("specific fine amount", prompt)


class Phase1FrontendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_new_cards_present(self):
        self.assertIn('id="result-payment"', self.page)
        self.assertIn('id="result-consequences"', self.page)
        self.assertIn('"explain.hPayment"', self.page)
        # Consequences has no own card: one line in the importance card.
        self.assertIn('class="consequence-line"', self.page)

    def test_parser_maps_new_keys(self):
        self.assertIn('payment_methods: "result-payment"', self.page)
        self.assertIn('consequences: "result-consequences"', self.page)

    def test_header_fallback_covers_new_cards(self):
        self.assertIn('["Payment methods", "result-payment"]', self.page)
        self.assertIn('["Consequences", "result-consequences"]', self.page)

    def test_sample_fills_new_cards(self):
        self.assertIn('"explain.sample.payment"', self.page)
        self.assertIn('"explain.sample.consequences"', self.page)

    def test_icon_card_count_unchanged(self):
        # The new cards use plain headings; deadline and amount cards
        # were removed, so the icon count is 5.
        found = re.findall(r'<h3><svg class="card-icon"', self.page)
        self.assertEqual(len(found), 5)


class Phase1TranslationTest(unittest.TestCase):
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
