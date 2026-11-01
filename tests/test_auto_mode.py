"""Auto-mode tests: default detection, kind label, other-only view.

The scan mode defaults to "auto": the model first decides which kind
the photo is (notice, machine, form, sign, or other) and the result
shows a small "Detected:" label. Photos with nothing to do with
daily life show only a short polite message. Unknown modes still
fall back to notice, and both AI prompts carry the safety rules.

Run from the project root:
    python -m unittest tests.test_auto_mode -v
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

NEW_KEYS = (
    "explain.modeAuto",
    "explain.moreOptions",
    "explain.detected",
    "explain.kindNotice",
    "explain.kindMachine",
    "explain.kindForm",
    "explain.kindSign",
    "explain.otherKind",
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


class AutoModeBackendTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def _posted_prompt(self, mode):
        seen = {}

        def fake_urlopen(req, timeout=120):
            seen["payload"] = json.loads(req.data.decode("utf-8"))
            return _api_reply("{}")

        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=fake_urlopen):
            data = {"photo": _image_file(), "language": "en",
                    "mode": mode}
            res = self.client.post("/explain", data=data,
                                   content_type="multipart/form-data")
        self.assertEqual(res.status_code, 200, mode)
        return seen["payload"]["messages"][0]["content"][0]["text"]

    def test_auto_mode_accepted(self):
        prompt = self._posted_prompt("auto")
        self.assertIn("First decide which kind", prompt)
        # The model gets every kind's rules, so it can follow the
        # detected kind exactly.
        for marker in ("numbered walkthrough",
                       "what to write, in which box",
                       "station board"):
            self.assertIn(marker, prompt)

    def test_kind_key_requested(self):
        prompt = self._posted_prompt("auto")
        self.assertIn('"kind"', prompt)
        self.assertIn('one of "notice", "machine", "form", "sign", '
                      'or "other"', prompt)

    def test_other_kind_explained(self):
        prompt = self._posted_prompt("auto")
        self.assertIn('use kind "other"', prompt)
        self.assertIn("selfie", prompt)

    def test_unknown_mode_still_falls_back(self):
        prompt = self._posted_prompt("rocket")
        self.assertNotIn("First decide which kind", prompt)
        self.assertNotIn("numbered walkthrough", prompt)
        self.assertNotIn("paper form", prompt)
        self.assertNotIn("station board", prompt)
        self.assertIn('"markers"', prompt)

    def test_explicit_modes_unchanged(self):
        prompt = self._posted_prompt("machine")
        self.assertIn("numbered walkthrough", prompt)
        self.assertNotIn("First decide which kind", prompt)

    def test_safety_rules_in_explain_prompt(self):
        prompt = self._posted_prompt("auto")
        for marker in ("card number", "PIN", "password",
                       "cover the keypad",
                       "do not give medical or legal advice",
                       "pharmacist"):
            self.assertIn(marker, prompt)


class AskHowToPromptTest(unittest.TestCase):
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
            return _api_reply("answer")

        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=fake_urlopen):
            res = self.client.post("/ask", json={
                "question": "How do I withdraw money?",
                "language": "en",
            })
        self.assertEqual(res.status_code, 200)
        return seen["payload"]["messages"][0]["content"][0]["text"]

    def test_howto_guide_in_ask_prompt(self):
        prompt = self._posted_prompt()
        for marker in ("step-by-step",
                       "button labels",
                       "reading in",
                       "brackets",
                       "common mistakes",
                       "not visible in the photo"):
            self.assertIn(marker, prompt)

    def test_safety_rules_in_ask_prompt(self):
        prompt = self._posted_prompt()
        for marker in ("card number", "cover the keypad",
                       "do not give medical or legal advice",
                       "pharmacist"):
            self.assertIn(marker, prompt)


class AutoModeFrontendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_auto_is_default(self):
        self.assertIn('<option value="auto" selected', self.page)
        self.assertIn('"explain.modeAuto"', self.page)

    def test_mode_select_in_more_options(self):
        self.assertIn("<details", self.page)
        self.assertIn('"explain.moreOptions"', self.page)
        self.assertIn('id="mode"', self.page)

    def test_old_modes_kept(self):
        for value in ("notice", "machine", "form", "sign"):
            self.assertIn('value="%s"' % value, self.page)
        for key in ("explain.modeLabel", "explain.modeNotice",
                    "explain.modeMachine", "explain.modeForm",
                    "explain.modeSign"):
            self.assertIn('"%s"' % key, self.page)

    def test_kind_label(self):
        for marker in ('id="kind-label"', "function kindLabel(kind)",
                       "function updateKindLabel()",
                       '"explain.detected"', '"explain.kindNotice"',
                       '"explain.kindMachine"', '"explain.kindForm"',
                       '"explain.kindSign"'):
            self.assertIn(marker, self.page)
        self.assertIn('/"kind"\\s*:\\s*"', self.page)

    def test_other_only_view(self):
        for marker in ('id="other-message"', '"explain.otherKind"',
                       'lastKind === "other" ? "none" : "block"',
                       'lastKind !== "other"'):
            self.assertIn(marker, self.page)

    def test_kind_dark_theme(self):
        css = _read("style.css")
        for selector in ('html[data-theme="dark"] .kind-label',
                         'html[data-theme="dark"] .other-message',
                         'html[data-theme="dark"] .more-options summary'):
            self.assertIn(selector, css)


class AutoModeTranslationTest(unittest.TestCase):
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
