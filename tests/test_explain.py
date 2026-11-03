"""Lens /explain tests: the model is asked for JSON with fixed keys.

Run from the project root:
    python -m unittest tests.test_explain -v
"""
import contextlib
import io
import json
import os
import unittest
from unittest import mock

import server

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JSON_KEYS = ("what", "why", "importance", "next_steps", "deadline",
             "amount", "staff_phrase", "staff_phrase_meaning",
             "check", "deadline_date")


def _image_file(name="notice.jpg", size=1024):
    body = b"\xff\xd8\xff" + b"x" * max(0, size - 3)  # real JPEG magic bytes
    return (io.BytesIO(body), name, "image/jpeg")


def _api_reply(text, finish_reason="stop", usage=None):
    envelope = {"choices": [{"message": {"content": text},
                             "finish_reason": finish_reason}]}
    if usage is not None:
        envelope["usage"] = usage
    body = json.dumps(envelope).encode("utf-8")
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

    def test_prompt_converts_era_years(self):
        prompt = self._posted_prompt("en")
        self.assertIn("Reiwa 8 (2026)", prompt)

    def test_prompt_keeps_single_language(self):
        prompt = self._posted_prompt("ne")
        self.assertIn("only in Nepali", prompt)
        self.assertIn("Do not mix English words", prompt)

    def test_prompt_amount_rule(self):
        prompt = self._posted_prompt("en")
        self.assertIn("exactly as written", prompt)
        self.assertIn("12,340 yen", prompt)
        self.assertIn("Never guess an amount", prompt)

    def test_prompt_staff_phrase_rule(self):
        prompt = self._posted_prompt("en")
        self.assertIn("polite Japanese sentence", prompt)
        self.assertIn("office counter", prompt)
        self.assertIn("staff_phrase_meaning", prompt)

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

    def test_explain_payload_timeout_and_brevity_rule(self):
        seen = {}

        def fake_urlopen(req, timeout=None):
            seen["payload"] = json.loads(req.data.decode("utf-8"))
            seen["timeout"] = timeout
            return _api_reply("{}")

        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=fake_urlopen):
            res = self._post_photo()
        self.assertEqual(res.status_code, 200)
        self.assertNotIn("max_tokens", seen["payload"])
        self.assertEqual(seen["payload"]["reasoning_effort"], "low")
        self.assertEqual(seen["timeout"], 40)
        prompt = seen["payload"]["messages"][0]["content"][0]["text"]
        self.assertIn("at most 2 sentences", prompt)

    def test_reasoning_effort_honours_env_override(self):
        seen = {}

        def fake_urlopen(req, timeout=None):
            seen["payload"] = json.loads(req.data.decode("utf-8"))
            return _api_reply("{}")

        with mock.patch.object(server, "REASONING_EXPLAIN", "medium"), \
                mock.patch.object(server.urllib.request, "urlopen",
                                  side_effect=fake_urlopen):
            res = self._post_photo()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(seen["payload"]["reasoning_effort"], "medium")
        prompt = seen["payload"]["messages"][0]["content"][0]["text"]
        self.assertIn("at most 2 sentences", prompt)


class MetaRetryTest(unittest.TestCase):
    """Timeouts and 5xx are retried once; 4xx is not."""

    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def _post_photo(self):
        data = {"photo": _image_file(), "language": "en"}
        return self.client.post("/explain", data=data,
                               content_type="multipart/form-data")

    def _http_error(self, code):
        return server.urllib.error.HTTPError(
            "https://meta.test/chat", code, "err", {}, io.BytesIO(b"nope"))

    def test_timeout_retried_once(self):
        reply = json.dumps({key: "line" for key in JSON_KEYS})
        buf = io.StringIO()
        with mock.patch.object(server.urllib.request, "urlopen") as m, \
                contextlib.redirect_stdout(buf):
            m.side_effect = [TimeoutError("slow"), _api_reply(reply)]
            res = self._post_photo()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(m.call_count, 2)
        self.assertIn("explain retry", buf.getvalue())
        self.assertIn("explain took", buf.getvalue())

    def test_http_400_not_retried(self):
        buf = io.StringIO()
        with mock.patch.object(server.urllib.request, "urlopen") as m, \
                contextlib.redirect_stdout(buf):
            m.side_effect = self._http_error(400)
            res = self._post_photo()
        self.assertEqual(res.status_code, 502)
        self.assertEqual(m.call_count, 1)
        self.assertNotIn("retry", buf.getvalue())
        self.assertIn("explain took", buf.getvalue())

    def _reasoning_error(self):
        return server.urllib.error.HTTPError(
            "https://meta.test/chat", 400, "err", {},
            io.BytesIO(b"unknown field: reasoning_effort"))

    def test_400_mentioning_reasoning_retried_without_it(self):
        payloads = []

        def fake_urlopen(req, timeout=None):
            payloads.append(json.loads(req.data.decode("utf-8")))
            if len(payloads) == 1:
                raise self._reasoning_error()
            return _api_reply("{}")

        buf = io.StringIO()
        with mock.patch.object(server.urllib.request, "urlopen") as m, \
                contextlib.redirect_stdout(buf):
            m.side_effect = fake_urlopen
            res = self._post_photo()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(m.call_count, 2)
        self.assertEqual(len(payloads), 2)
        self.assertEqual(payloads[0]["reasoning_effort"], "low")
        self.assertNotIn("reasoning_effort", payloads[1])
        self.assertIn("reasoning_effort not supported", buf.getvalue())
        self.assertIn("explain took", buf.getvalue())

    def test_reasoning_strip_happens_only_once(self):
        def always_reasoning_error(req, timeout=None):
            raise self._reasoning_error()

        buf = io.StringIO()
        with mock.patch.object(server.urllib.request, "urlopen") as m, \
                contextlib.redirect_stdout(buf):
            m.side_effect = always_reasoning_error
            res = self._post_photo()
        self.assertEqual(res.status_code, 502)
        self.assertEqual(m.call_count, 2)
        self.assertEqual(
            buf.getvalue().count("reasoning_effort not supported"), 1)

    def test_http_500_retried_once(self):
        reply = json.dumps({key: "line" for key in JSON_KEYS})
        buf = io.StringIO()
        with mock.patch.object(server.urllib.request, "urlopen") as m, \
                contextlib.redirect_stdout(buf):
            m.side_effect = [self._http_error(500), _api_reply(reply)]
            res = self._post_photo()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(m.call_count, 2)
        self.assertIn("explain retry", buf.getvalue())

    def test_budget_constants_leave_headroom(self):
        self.assertEqual(server.META_TIMEOUT, 40)
        self.assertEqual(server.META_BUDGET, 85)
        self.assertEqual(server.META_RETRY_MIN_LEFT, 30)
        self.assertLess(server.META_BUDGET, 90)

    def test_worst_case_stays_under_browser_timeout(self):
        now = [0.0]
        seen = []

        def fake_urlopen(req, timeout=None):
            seen.append(timeout)
            now[0] += timeout  # each attempt burns its full timeout
            raise TimeoutError("slow")

        with mock.patch.object(server.time, "monotonic",
                               side_effect=lambda: now[0]), \
                mock.patch.object(server.urllib.request, "urlopen",
                                  side_effect=fake_urlopen):
            res = self._post_photo()
        self.assertEqual(res.status_code, 502)
        self.assertEqual(seen, [40, 40])
        self.assertLess(now[0], 90)

    def test_no_retry_when_budget_nearly_spent(self):
        now = [0.0]
        burns = [60, 40]

        def fake_urlopen(req, timeout=None):
            now[0] += burns.pop(0)
            raise TimeoutError("slow")

        with mock.patch.object(server.time, "monotonic",
                               side_effect=lambda: now[0]), \
                mock.patch.object(server.urllib.request, "urlopen",
                                  side_effect=fake_urlopen):
            res = self._post_photo()
        self.assertEqual(res.status_code, 502)
        self.assertEqual(len(burns), 1)


class FinishCutoffTest(unittest.TestCase):
    """finish_reason length: log it, keep valid JSON, friendly error if cut."""

    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def _post_photo(self):
        data = {"photo": _image_file(), "language": "en"}
        return self.client.post("/explain", data=data,
                               content_type="multipart/form-data")

    def test_length_finish_logs_but_keeps_valid_json(self):
        buf = io.StringIO()
        with mock.patch.object(server.urllib.request, "urlopen") as m, \
                contextlib.redirect_stdout(buf):
            m.side_effect = lambda req, timeout=None: _api_reply(
                '{"what": "ok"}', "length")
            res = self._post_photo()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {"text": '{"what": "ok"}'})
        self.assertIn("explain cut off", buf.getvalue())

    def test_fenced_answer_parses(self):
        buf = io.StringIO()
        with mock.patch.object(server.urllib.request, "urlopen") as m, \
                contextlib.redirect_stdout(buf):
            m.side_effect = lambda req, timeout=None: _api_reply(
                'Here is the letter:\n```json\n{"what": "ok"}\n```\nDone.',
                "length")
            res = self._post_photo()
        self.assertEqual(res.status_code, 200)
        self.assertIn("explain cut off", buf.getvalue())
        self.assertNotIn("explain retry", buf.getvalue())

    def test_length_retry_adds_short_answer_line(self):
        payloads = []

        def fake_urlopen(req, timeout=None):
            payloads.append(json.loads(req.data.decode("utf-8")))
            if len(payloads) == 1:
                return _api_reply('{"what": "ok"', "length")
            return _api_reply('{"what": "ok"}', "stop")

        with mock.patch.object(server.urllib.request, "urlopen") as m, \
                contextlib.redirect_stdout(io.StringIO()):
            m.side_effect = fake_urlopen
            res = self._post_photo()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(m.call_count, 2)
        self.assertEqual(len(payloads), 2)
        first = payloads[0]["messages"][0]["content"][0]["text"]
        second = payloads[1]["messages"][0]["content"][0]["text"]
        self.assertNotIn("too long", first)
        self.assertIn("Your last answer was too long. Use very short values,"
                      " at most 1 sentence each.", second)

    def test_double_failure_returns_long_letter_message(self):
        buf = io.StringIO()
        with mock.patch.object(server.urllib.request, "urlopen") as m, \
                contextlib.redirect_stdout(buf):
            m.side_effect = lambda req, timeout=None: _api_reply(
                '{"what": "ok"', "length")
            res = self._post_photo()
        self.assertEqual(res.status_code, 502)
        self.assertEqual(m.call_count, 2)
        self.assertEqual(res.get_json(), {
            "error": "This letter is long. Try a photo of just the top part,"
                     " or try again.",
            "code": "long_letter",
        })
        self.assertIn("explain cut off", buf.getvalue())
        self.assertIn("explain retry", buf.getvalue())

    def test_usage_logged_when_present(self):
        buf = io.StringIO()
        with mock.patch.object(server.urllib.request, "urlopen") as m, \
                contextlib.redirect_stdout(buf):
            m.side_effect = lambda req, timeout=None: _api_reply(
                '{"what": "ok"}', "stop",
                {"prompt_tokens": 10, "completion_tokens": 5})
            res = self._post_photo()
        self.assertEqual(res.status_code, 200)
        self.assertIn("explain usage {'prompt_tokens': 10", buf.getvalue())

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
        self.assertIn("AI_TIMEOUT_MS = 90000", self.page)
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
                         r'#sample-tag\s*\{[^}]*?border-radius: 4px;')

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

    def test_sample_staff_phrase(self):
        with open(os.path.join(ROOT, "i18n.js"), encoding="utf-8") as f:
            i18n = f.read()
        self.assertEqual(i18n.count("この保険料の支払いについて相談したいです。"), 4)
        for text in ("I want to ask about paying this insurance bill.",
                     "म यो बिमा शुल्क तिर्ने बारेमा सोध्न चाहन्छु।",
                     "Tôi muốn hỏi về việc nộp khoản bảo hiểm này.",
                     "ဒီအာမခံကြေးပေးချေရေးနဲ့ ပတ်သက်ပြီး မေးချင်ပါတယ်။",
                     "12,340 yen", "12,340 येन", "12.340 yên", "12,340 ယန်း"):
            self.assertIn(text, i18n)

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

    def test_amount_in_summary_box(self):
        # No separate amount card: the reply is parsed, stored, and shown
        # only in the amber summary box.
        self.assertNotIn('id="result-amount"', self.page)
        self.assertNotIn('id="result-deadline"', self.page)
        self.assertIn('id="summary-amount"', self.page)
        self.assertIn('"explain.hAmount"', self.page)
        self.assertIn('amount: "result-amount"', self.page)
        self.assertIn('"explain.sample.amount"', self.page)
        self.assertIn("lastAmountText", self.page)

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
        # The question box and chips are disabled while a scan is in
        # flight and re-enabled when it finishes. The Send button
        # stays enabled: it becomes a Stop button instead.
        self.assertIn("askInput.disabled = true;", self.page)
        self.assertIn("askInput.disabled = false;", self.page)
        self.assertNotIn("askBtn.disabled = true;", self.page)
        self.assertNotIn("askBtn.disabled = false;", self.page)
        self.assertEqual(self.page.count("c.disabled = true;"), 2)
        self.assertEqual(self.page.count("c.disabled = false;"), 2)
        self.assertIn('setSendMode("stop");', self.page)
        self.assertIn('setSendMode("send");', self.page)


class CalendarDownloadTest(unittest.TestCase):
    """Both pages build the same .ics file in JS."""

    def _page(self, name):
        with open(os.path.join(ROOT, name), encoding="utf-8") as f:
            return f.read()

    def test_ics_content(self):
        for name in ("explain.html", "dates.html"):
            page = self._page(name)
            for snippet in ("BEGIN:VCALENDAR", "VERSION:2.0",
                            "BEGIN:VEVENT", "END:VEVENT", "END:VCALENDAR",
                            "DTSTART;VALUE=DATE:", "TRIGGER:-P3D",
                            "BEGIN:VALARM", "END:VALARM", "ACTION:DISPLAY",
                            '"text/calendar"', ".ics",
                            "function downloadIcs(title, dateStr)"):
                self.assertIn(snippet, page, name)

    def test_add_to_calendar_buttons(self):
        explain = self._page("explain.html")
        self.assertIn('id="save-date-cal"', explain)
        self.assertIn('"explain.addToCal"', explain)
        self.assertIn("downloadIcs(lastSavedTitle, lastSavedDate)", explain)
        dates = self._page("dates.html")
        self.assertIn('"explain.addToCal"', dates)
        self.assertIn("downloadIcs(item.title, item.date)", dates)


if __name__ == "__main__":
    unittest.main()
