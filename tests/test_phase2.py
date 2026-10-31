"""Phase 2 tests: Photo Tutor modes and image markers.

Modes change the /explain prompt, follow-ups carry the mode, markers
are validated before display, and all new strings exist in all four
languages. Old requests without a mode keep working.

Run from the project root:
    python -m unittest tests.test_phase2 -v
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
NEW_KEYS = ("explain.modeLabel", "explain.modeNotice",
            "explain.modeMachine", "explain.modeForm",
            "explain.modeSign", "explain.markersTitle",
            "explain.markedPhotoAlt")


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


class Phase2PromptTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def _posted_prompt(self, **form):
        seen = {}

        def fake_urlopen(req, timeout=120):
            seen["payload"] = json.loads(req.data.decode("utf-8"))
            return _api_reply("{}")

        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=fake_urlopen):
            data = {"photo": _image_file(), "language": "en"}
            data.update(form)
            res = self.client.post("/explain", data=data,
                                   content_type="multipart/form-data")
        self.assertEqual(res.status_code, 200)
        return seen["payload"]["messages"][0]["content"][0]["text"]

    def test_prompt_requests_markers(self):
        prompt = self._posted_prompt()
        self.assertIn('"markers"', prompt)
        self.assertIn("at most 5 markers", prompt)
        self.assertIn("percentages from the top-left", prompt)

    def test_prompt_forbids_invented_objects(self):
        prompt = self._posted_prompt()
        self.assertIn("never invent", prompt)
        self.assertIn("buttons, labels, or objects", prompt)

    def test_machine_mode_changes_prompt(self):
        prompt = self._posted_prompt(mode="machine")
        self.assertIn("ticket machine, ATM", prompt)
        self.assertIn("numbered walkthrough", prompt)

    def test_form_mode_changes_prompt(self):
        prompt = self._posted_prompt(mode="form")
        self.assertIn("paper form", prompt)
        self.assertIn("what to write, in which box", prompt)

    def test_sign_mode_changes_prompt(self):
        prompt = self._posted_prompt(mode="sign")
        self.assertIn("station board", prompt)
        self.assertIn("what the reader should do", prompt)

    def test_unknown_mode_falls_back_to_notice(self):
        prompt = self._posted_prompt(mode="rocket")
        self.assertNotIn("numbered walkthrough", prompt)
        self.assertNotIn("paper form", prompt)
        self.assertNotIn("station board", prompt)
        self.assertIn('"markers"', prompt)

    def test_ask_carries_mode(self):
        seen = {}

        def fake_urlopen(req, timeout=120):
            seen["payload"] = json.loads(req.data.decode("utf-8"))
            return _api_reply("answer")

        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=fake_urlopen):
            res = self.client.post("/ask", json={
                "question": "Where is the button?",
                "language": "en",
                "mode": "machine",
            })
        self.assertEqual(res.status_code, 200)
        prompt = seen["payload"]["messages"][0]["content"][0]["text"]
        self.assertIn("photo shows a machine", prompt)


class Phase2FrontendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_mode_selector_present(self):
        self.assertIn('id="mode"', self.page)
        for value in ("notice", "machine", "form", "sign"):
            self.assertIn('value="%s"' % value, self.page)
        for key in ("explain.modeLabel", "explain.modeNotice",
                    "explain.modeMachine", "explain.modeForm",
                    "explain.modeSign"):
            self.assertIn('"%s"' % key, self.page)

    def test_mode_sent_to_backend(self):
        self.assertIn('data.append("mode",', self.page)
        self.assertIn("mode: document.getElementById", self.page)

    def test_marker_parser_validates(self):
        self.assertIn("function markersFromReply(text)", self.page)
        self.assertIn("!Array.isArray(data.markers)", self.page)
        self.assertIn("out.length >= 5", self.page)
        self.assertIn("x < 0 || x > 100 || y < 0 || y > 100", self.page)
        self.assertIn(".slice(0, 60)", self.page)

    def test_marker_overlay_present(self):
        self.assertIn('id="marked-photo-wrap"', self.page)
        self.assertIn('id="marker-layer"', self.page)
        self.assertIn('id="marker-list"', self.page)
        self.assertIn("function showMarkers(markers)", self.page)
        self.assertIn('"explain.markersTitle"', self.page)

    def test_markers_use_percent_positions(self):
        self.assertIn('m.x + "%"', self.page)
        self.assertIn('m.y + "%"', self.page)


class Phase2StyleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = _read("style.css")

    def test_marker_styles(self):
        self.assertIn(".marker-stage {", self.css)
        self.assertIn("position: relative;", self.css)
        self.assertIn(".marker-dot {", self.css)
        self.assertIn("transform: translate(-50%, -50%);", self.css)
        self.assertIn(".marker-list {", self.css)

    def test_marker_dark_theme(self):
        self.assertIn('html[data-theme="dark"] .marker-stage img', self.css)
        self.assertIn('html[data-theme="dark"] .marker-list', self.css)
        self.assertIn('html[data-theme="dark"] #mode', self.css)


class Phase2TranslationTest(unittest.TestCase):
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


class Phase2CompatTest(unittest.TestCase):
    def test_old_keys_still_requested(self):
        src = _read("server.py")
        for key in ("what", "why", "importance", "next_steps",
                    "deadline", "amount", "staff_phrase",
                    "staff_phrase_meaning", "payment_methods",
                    "consequences", "check", "deadline_date"):
            self.assertIn('"%s"' % key, src)

    def test_notice_flow_kept(self):
        page = _read("explain.html")
        for marker in ('id="followup-card"', 'id="save-date-btn"',
                       'id="save-date-cal"', "fillSampleCards()"):
            self.assertIn(marker, page)


if __name__ == "__main__":
    unittest.main()
