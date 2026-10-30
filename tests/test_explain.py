"""Lens /explain tests: the model is asked for JSON with fixed keys.

Run from the project root:
    python -m unittest tests.test_explain -v
"""
import io
import json
import os
import unittest
from unittest import mock

import server

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JSON_KEYS = ("what", "why", "importance", "next_steps", "deadline", "check",
             "deadline_date")


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


class ExplainPromptTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def _posted_prompt(self, language):
        """POST a photo and return the text prompt sent to the model."""
        seen = {}

        def fake_urlopen(req, timeout=120):
            seen["payload"] = json.loads(req.data.decode("utf-8"))
            return _api_reply("{}")

        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=fake_urlopen):
            data = {"photo": _image_file(), "language": language}
            res = self.client.post("/explain", data=data,
                                   content_type="multipart/form-data")
        self.assertEqual(res.status_code, 200)
        return seen["payload"]["messages"][0]["content"][0]["text"]

    def test_prompt_requests_json_keys(self):
        prompt = self._posted_prompt("en")
        self.assertIn("JSON", prompt)
        for key in JSON_KEYS:
            self.assertIn('"%s"' % key, prompt)

    def test_prompt_uses_user_language(self):
        prompt = self._posted_prompt("ne")
        self.assertIn("Nepali", prompt)

    def test_prompt_keeps_no_guessing_rule(self):
        prompt = self._posted_prompt("en")
        self.assertIn("Never invent amounts, dates, or names.", prompt)

    def test_prompt_reminds_to_confirm_with_office(self):
        prompt = self._posted_prompt("en")
        self.assertIn("confirm the details with the issuing office", prompt)

    def _raw_reply(self, body):
        """Fake urlopen context manager returning raw bytes."""
        resp = mock.MagicMock()
        resp.read.return_value = body
        ctx = mock.MagicMock()
        ctx.__enter__.return_value = resp
        ctx.__exit__.return_value = False
        return ctx

    def _post_photo(self):
        data = {"photo": _image_file(), "language": "en"}
        return self.client.post("/explain", data=data,
                               content_type="multipart/form-data")

    def test_explain_rejects_malformed_provider_reply(self):
        ctx = self._raw_reply(b"this is not json")
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=lambda req, timeout=120: ctx):
            res = self._post_photo()
        self.assertEqual(res.status_code, 502)

    def test_explain_rejects_reply_without_choices(self):
        ctx = self._raw_reply(b'{"oops": true}')
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=lambda req, timeout=120: ctx):
            res = self._post_photo()
        self.assertEqual(res.status_code, 502)
        self.assertIn("error", res.get_json())

    def test_explain_timeout_is_502(self):
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=TimeoutError("slow")):
            res = self._post_photo()
        self.assertEqual(res.status_code, 502)

    def test_explain_returns_model_text_unchanged(self):
        reply = json.dumps({key: "line %s" % key for key in JSON_KEYS})
        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=lambda req, timeout=120: _api_reply(reply)):
            data = {"photo": _image_file(), "language": "en"}
            res = self.client.post("/explain", data=data,
                                   content_type="multipart/form-data")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {"text": reply})


class ExplainPageScriptTest(unittest.TestCase):
    """explain.html must keep the browser-side Lens fixes."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(ROOT, "explain.html"), encoding="utf-8") as f:
            cls.page = f.read()

    def test_array_values_become_numbered_lines(self):
        self.assertIn('". " + cleanText(value[i])', self.page)

    def test_json_retry_uses_first_and_last_brace(self):
        self.assertIn('fenced.indexOf("{")', self.page)
        self.assertIn('fenced.lastIndexOf("}")', self.page)

    def test_shrink_fills_white_background(self):
        self.assertIn('fillStyle = "#ffffff"', self.page)
        self.assertIn("fillRect(0, 0, canvas.width, canvas.height)", self.page)

    def test_ai_fetches_use_timeout(self):
        self.assertIn("AI_TIMEOUT_MS = 45000", self.page)
        self.assertIn("new AbortController()", self.page)
        self.assertIn('fetchWithTimeout("/explain"', self.page)
        self.assertIn('fetchWithTimeout("/ask"', self.page)
        self.assertIn("AbortError", self.page)
        self.assertIn('"explain.tooSlow"', self.page)

    def test_api_replies_checked_before_json(self):
        self.assertIn("application/json", self.page)
        self.assertIn("lbServerError", self.page)
        self.assertIn('"explain.serverError"', self.page)
        # One call site: the fetch helper reads the body before its timer stops.
        self.assertEqual(self.page.count("await readApiJson(res)"), 1)
        # Exactly one res.json() call site, inside the guarded helper.
        self.assertEqual(self.page.count("res.json()"), 1)

    def test_timeout_covers_body_read(self):
        start = self.page.index("async function fetchWithTimeout")
        parse_at = self.page.index("await readApiJson(res)")
        end = self.page.index("async function readApiJson")
        self.assertLess(start, parse_at)
        self.assertLess(parse_at, end)

    def test_scan_epoch_guard(self):
        self.assertIn("let scanEpoch = 0;", self.page)
        self.assertIn("scanEpoch++;", self.page)
        self.assertIn("const myEpoch = scanEpoch;", self.page)
        self.assertIn("if (myEpoch !== scanEpoch) return;", self.page)
        guard_at = self.page.index("if (myEpoch !== scanEpoch) return;")
        self.assertLess(guard_at, self.page.index('addMsg("chat-a", answer);'))
        self.assertLess(guard_at, self.page.index("chatHistory.push"))

    def test_photo_always_reencoded(self):
        self.assertIn("Math.min(1, 1600 / longest)", self.page)
        self.assertNotIn("longest <= 1600", self.page)

    def test_same_photo_sent_to_explain_and_ask(self):
        self.assertIn("await shrinkPhoto(photoInput.files[0])", self.page)
        self.assertIn('"data:" + lastPhotoMime + ";base64," + lastPhotoB64',
                       self.page)

    def test_followup_keeps_history(self):
        self.assertIn("let chatHistory = [];", self.page)
        self.assertIn('chatHistory.push({role: "user", content: question});',
                      self.page)
        self.assertIn('chatHistory.push({role: "assistant", '
                      'content: answer.slice(0, 8000)});',
                      self.page)
        self.assertIn("history: chatHistory.slice(-10)", self.page)

    def test_new_explanation_clears_history(self):
        # Declaration + clear on real scan + clear on sample fill.
        self.assertEqual(self.page.count("chatHistory = [];"), 3)

    def test_lb_config_script_loaded(self):
        self.assertIn('<script src="lb-config.js"></script>', self.page)

    def test_save_deadline_button(self):
        self.assertIn('id="save-date-btn"', self.page)
        self.assertIn('"explain.saveDate"', self.page)
        self.assertIn("lb_dates", self.page)
        self.assertIn("dates.html", self.page)
        self.assertIn("/^\\d{4}-\\d{2}-\\d{2}$/", self.page)

    def test_save_deadline_validates_date(self):
        self.assertIn("function isRealDate(text)", self.page)
        self.assertIn("isRealDate(lastDeadlineDate)", self.page)
        self.assertIn('t("tracker.saveFailed"', self.page)

    def test_sample_tag_is_styled_pill(self):
        self.assertRegex(self.page,
                         r'#sample-tag\s*\{[^}]*?background: #BE123C;')
        self.assertRegex(self.page,
                         r'#sample-tag\s*\{[^}]*?border-radius: 999px;')

    def test_save_date_message_rerenders_on_lang_change(self):
        self.assertIn("function renderSaveDateMsg()", self.page)
        self.assertIn("if (saveDateState) renderSaveDateMsg();", self.page)

    def test_sample_button_fills_cards(self):
        self.assertIn("Try a sample notice", self.page)
        self.assertIn("fillSampleCards()", self.page)
        self.assertIn("2027-02-01", self.page)
        self.assertIn('id="sample-tag"', self.page)
        self.assertIn('"explain.sampleTag"', self.page)
        self.assertIn('"explain.sample.what"', self.page)
        self.assertIn("if (sampleShowing) fillSampleCards();", self.page)
        self.assertNotIn("requestSubmit", self.page)

    def test_sample_deadline_locked(self):
        # 4th resident-tax installment: Jan 31, 2027 is a Sunday, so Feb 1.
        self.assertIn('lastDeadlineDate = "2027-02-01";', self.page)
        with open(os.path.join(ROOT, "i18n.js"), encoding="utf-8") as f:
            i18n = f.read()
        for text in ("February 1, 2027 (4th installment)",
                     "फेब्रुअरी 1, 2027 (चौथो किस्ता)",
                     "Ngày 1 tháng 2 năm 2027 (đợt 4)",
                     "၂၀၂၇ ဖေဖော်ဝါရီ ၁ (စတုတ္ထအရစ်ကျ)"):
            self.assertIn(text, i18n)

    def test_save_date_asks_to_confirm(self):
        self.assertIn('id="save-date-confirm"', self.page)
        self.assertIn('id="save-date-input"', self.page)
        self.assertIn('type="date"', self.page)
        self.assertIn('"explain.checkDate"', self.page)
        self.assertIn('"explain.confirmSave"', self.page)
        self.assertIn("saveDateInput.value = lastDeadlineDate", self.page)
        self.assertIn("isRealDate(picked)", self.page)

    def test_privacy_hint_shown(self):
        self.assertIn('"explain.privacyHint"', self.page)
        self.assertIn("residence card number", self.page)

    def test_scan_state_updates_atomically(self):
        # The new photo must wait in locals until the reply succeeds, so a
        # failed scan keeps the previous photo + explanation pair untouched.
        self.assertIn("const newPhotoB64 = await blobToB64(smallPhoto);",
                      self.page)
        self.assertIn("const newPhotoMime = smallPhoto.type", self.page)
        self.assertIn("lastPhotoB64 = newPhotoB64;", self.page)
        self.assertIn("lastPhotoMime = newPhotoMime;", self.page)
        self.assertNotIn("lastPhotoB64 = await", self.page)
        self.assertNotIn("lastPhotoMime = smallPhoto", self.page)
        self.assertLess(self.page.index("parseExplainReply(json.text"),
                        self.page.index("lastPhotoB64 = newPhotoB64;"))

    def test_scan_disables_followup_ui(self):
        # The question box, Ask button and chips are all disabled while a
        # scan is in flight (askQuestion already disables the latter two,
        # so each appears twice) and re-enabled when it finishes.
        self.assertIn("askInput.disabled = true;", self.page)
        self.assertIn("askInput.disabled = false;", self.page)
        self.assertEqual(self.page.count("askBtn.disabled = true;"), 2)
        self.assertEqual(self.page.count("askBtn.disabled = false;"), 2)
        self.assertEqual(self.page.count("c.disabled = true;"), 2)
        self.assertEqual(self.page.count("c.disabled = false;"), 2)


if __name__ == "__main__":
    unittest.main()
