"""Phase 4 tests: Money Tracker AI spending advice.

/spending-advice explains one month from totals only. The frontend
never reads entry notes or goal names when building the request, and
the backend never reads them either.

Run from the project root:
    python -m unittest tests.test_phase4 -v
"""
import json
import os
import re
import unittest
from unittest import mock

import server

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("en", "ne", "vi", "my")
NEW_KEYS = ("tracker.aiTitle", "tracker.aiLead", "tracker.aiButton",
            "tracker.aiWait", "tracker.aiEmpty", "tracker.aiError")


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


def _api_reply(text):
    body = json.dumps({"choices": [{"message": {"content": text}}]}).encode("utf-8")
    resp = mock.MagicMock()
    resp.read.return_value = body
    ctx = mock.MagicMock()
    ctx.__enter__.return_value = resp
    ctx.__exit__.return_value = False
    return ctx


class Phase4ApiTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def _post_advice(self, body):
        seen = {}

        def fake_urlopen(req, timeout=120):
            seen["payload"] = json.loads(req.data.decode("utf-8"))
            return _api_reply("You spent less than you earned.")

        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=fake_urlopen):
            res = self.client.post("/spending-advice", json=body)
        return res, seen.get("payload", {})

    def _valid_body(self):
        return {"language": "en", "month": "2026-11",
                "income": 200000, "expense": 150000, "saving": 20000,
                "goals": [{"target": 120000, "saved": 30000}]}

    def test_valid_totals_return_advice(self):
        res, _ = self._post_advice(self._valid_body())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(),
                         {"advice": "You spent less than you earned."})

    def test_prompt_uses_only_numbers(self):
        _, payload = self._post_advice(self._valid_body())
        prompt = payload["messages"][0]["content"]
        self.assertIn("Earned: 200000 yen", prompt)
        self.assertIn("Spent: 150000 yen", prompt)
        self.assertIn("target 120000 yen, saved 30000 yen (25%)", prompt)
        self.assertIn("Never invent transactions", prompt)

    def test_extra_notes_are_ignored(self):
        body = self._valid_body()
        body["notes"] = ["SECRET NOTE", "second secret"]
        body["goals"] = [{"target": 120000, "saved": 30000,
                          "name": "SECRET GOAL"}]
        res, payload = self._post_advice(body)
        self.assertEqual(res.status_code, 200)
        prompt = payload["messages"][0]["content"]
        self.assertNotIn("SECRET", prompt)

    def test_bad_month_rejected(self):
        body = self._valid_body()
        body["month"] = "November"
        res, _ = self._post_advice(body)
        self.assertEqual(res.status_code, 400)

    def test_negative_total_rejected(self):
        body = self._valid_body()
        body["expense"] = -5
        res, _ = self._post_advice(body)
        self.assertEqual(res.status_code, 400)

    def test_bad_goals_rejected(self):
        body = self._valid_body()
        body["goals"] = [{"target": 0, "saved": 10}]
        res, _ = self._post_advice(body)
        self.assertEqual(res.status_code, 400)


class Phase4FrontendTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("tracker.html")
        start = cls.page.index("// AI advice - start")
        end = cls.page.index("// AI advice - end")
        cls.block = cls.page[start:end]

    def test_advice_ui_present(self):
        self.assertIn('id="advice-btn"', self.page)
        self.assertIn('id="advice-status"', self.page)
        self.assertIn('id="advice-result"', self.page)
        for key in NEW_KEYS:
            self.assertIn('"%s"' % key, self.page)

    def test_payload_sends_totals_only(self):
        self.assertIn("function buildAdvicePayload()", self.block)
        for key in ("income:", "expense:", "saving:",
                    "target: g.target", "saved: saved"):
            self.assertIn(key, self.block)

    def test_payload_never_reads_notes_or_names(self):
        for banned in (".note", '"note"', "'note'", "note:",
                       ".name", '"name"', "goal.name"):
            self.assertNotIn(banned, self.block, banned)

    def test_advice_posts_to_endpoint(self):
        self.assertIn('fetch("/spending-advice"', self.block)
        self.assertIn("adviceHeaders()", self.block)
        self.assertIn('<script src="lb-config.js"></script>', self.page)


class Phase4TranslationTest(unittest.TestCase):
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


class Phase4CompatTest(unittest.TestCase):
    def test_tracker_storage_kept(self):
        page = _read("tracker.html")
        for marker in ("lb_money_entries", "lb_money_goals",
                       "cleanEntries(load(ENTRIES_KEY, []))",
                       "cleanGoals(load(GOALS_KEY, []))"):
            self.assertIn(marker, page)


if __name__ == "__main__":
    unittest.main()
