"""Redesign tests: translations, calendar files, deadlines, dark mode.

Covers the UI redesign: new i18n keys in all four languages, .ics
calendar downloads, deadline math, empty result cards, dark theme
for new elements, responsive layout markers, the em dash ban in
i18n.js, and a backend smoke test (no API key needed).

Run from the project root:
    python -m unittest tests.test_redesign -v
"""
import os
import re
import unittest

import server

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("en", "ne", "vi", "my")
PAGES = ("index.html", "explain.html", "dates.html", "tracker.html",
         "offline.html")

NEW_KEYS = (
    "nav.moneyShort",
    "index.step1d", "index.step2d", "index.step3d",
    "explain.eraLabel", "explain.loadingTitle", "explain.loadingLang",
    "dates.upcoming", "dates.past", "dates.completed",
    "dates.markDone", "dates.reopen",
    "dates.prevMonth", "dates.nextMonth",
    "dates.calendarTitle", "dates.today",
    "offline.title", "offline.lead", "offline.retry",
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


class TranslationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = _read("i18n.js")
        cls.blocks = {lang: _lang_block(cls.src, lang) for lang in LANGS}

    def test_new_keys_in_all_four_languages(self):
        for key in NEW_KEYS:
            for lang in LANGS:
                self.assertIn('"%s":' % key, self.blocks[lang],
                              "%s missing in %s" % (key, lang))

    def test_new_keys_have_no_empty_values(self):
        for lang in LANGS:
            for key in NEW_KEYS:
                match = re.search(r'"%s": "(.*?)"' % re.escape(key),
                                  self.blocks[lang])
                self.assertTrue(match, "%s missing in %s" % (key, lang))
                self.assertTrue(match.group(1).strip(),
                                "%s is empty in %s" % (key, lang))

    def test_hero_mentions_japanese_letter(self):
        for lang in LANGS:
            match = re.search(r'"index\.hero": "(.*?)"', self.blocks[lang])
            self.assertTrue(match, lang)
            self.assertTrue(match.group(1).strip(), lang)
        self.assertIn("Got a Japanese letter", self.blocks["en"])


class CalendarFileTest(unittest.TestCase):
    def test_ics_download_in_both_pages(self):
        for page in ("dates.html", "explain.html"):
            text = _read(page)
            self.assertIn("function downloadIcs(title, dateStr)", text, page)
            self.assertIn("function icsText(value)", text, page)
            self.assertIn("function icsStamp(when)", text, page)

    def test_ics_has_event_and_reminder(self):
        for page in ("dates.html", "explain.html"):
            text = _read(page)
            for marker in ("BEGIN:VCALENDAR", "BEGIN:VEVENT",
                           "DTSTART;VALUE=DATE:", "SUMMARY:",
                           "BEGIN:VALARM", "TRIGGER:-P3D",
                           "ACTION:DISPLAY", "END:VCALENDAR"):
                self.assertIn(marker, text, page)

    def test_ics_escapes_special_text(self):
        text = _read("dates.html")
        # Backslashes, semicolons, commas and newlines are escaped.
        self.assertIn('.replace(/\\\\/g, "\\\\\\\\")', text)
        self.assertIn('.replace(/;/g, "\\\\;")', text)
        self.assertIn('.replace(/,/g, "\\\\,")', text)
        self.assertIn('.replace(/\\r?\\n/g, "\\\\n")', text)


class DeadlineMathTest(unittest.TestCase):
    def test_days_until_counts_whole_days(self):
        for page in ("dates.html", "explain.html"):
            text = _read(page)
            self.assertIn("function daysUntil(dateStr)", text, page)
            # Milliseconds per day, rounded to whole days.
            self.assertIn("/ 86400000", text, page)

    def test_red_only_within_seven_days(self):
        text = _read("dates.html")
        self.assertIn("function dueClass(dateStr)", text)
        self.assertIn('"due due-soon"', text)
        self.assertIn('"due due-passed"', text)
        # The red threshold is exactly 7 days.
        self.assertRegex(text, r"if \(n <= 7\) return \"due due-soon\";")
        self.assertIn("function countdownClass(n)", text)
        self.assertIn('"deadline-count soon"', text)

    def test_era_date_covers_three_eras(self):
        text = _read("explain.html")
        self.assertIn("function toEraDate(dateStr)", text)
        # Era start dates: Reiwa, Heisei, Showa.
        self.assertIn('"2019-05-01"', text)
        self.assertIn('"1989-01-08"', text)
        self.assertIn('"1926-12-25"', text)
        for name in ("Reiwa", "Heisei", "Showa"):
            self.assertIn(name, text)
        self.assertIn("(year - 2018)", text)
        self.assertIn("(year - 1988)", text)
        self.assertIn("(year - 1925)", text)

    def test_era_shown_with_deadline(self):
        text = _read("explain.html")
        self.assertIn('id="summary-era"', text)
        self.assertNotIn('id="result-era"', text)
        self.assertIn('"explain.eraLabel"', text)


class EmptyCardTest(unittest.TestCase):
    def test_empty_cards_show_not_shown(self):
        text = _read("explain.html")
        self.assertIn("function fillCard(id, text)", text)
        self.assertIn('t("explain.notShown", "Not shown")', text)

    def test_empty_staff_card_shows_not_shown(self):
        text = _read("explain.html")
        self.assertIn("function fillStaff(phrase, meaning)", text)
        self.assertIn('id="result-staff"', text)
        self.assertIn('id="copy-staff-btn"', text)
        self.assertIn('"explain.copied"', text)

    def test_empty_deadline_groups_show_message(self):
        text = _read("dates.html")
        self.assertIn('t("app.noDates", "No dates added yet.")', text)
        for list_id in ("date-upcoming", "date-past", "date-done"):
            self.assertIn('id="%s"' % list_id, text)


class RedesignDarkThemeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = _read("style.css")

    def test_dark_covers_redesign_selectors(self):
        for selector in ('html[data-theme="dark"] .hero-text',
                         'html[data-theme="dark"] .scan-steps',
                         'html[data-theme="dark"] .check-card',
                         'html[data-theme="dark"] .cal',
                         'html[data-theme="dark"] .cal-day',
                         'html[data-theme="dark"] .deadline-title',
                         'html[data-theme="dark"] .deadline-count',
                         'html[data-theme="dark"] .deadline-amount',
                         'html[data-theme="dark"] .step-desc'):
            self.assertIn(selector, self.css)

    def test_dark_covers_tracker_extras(self):
        for selector in ('html[data-theme="dark"] .tag-income',
                         'html[data-theme="dark"] .tag-expense',
                         'html[data-theme="dark"] .tag-saving',
                         'html[data-theme="dark"] .progress',
                         'html[data-theme="dark"] .del-btn'):
            self.assertIn(selector, self.css)

    def test_no_purple_or_pills(self):
        for name in ("style.css", "tracker.html", "explain.html",
                     "dates.html", "index.html"):
            text = _read(name)
            for banned in ("#3730a3", "#e6e9fd", "999px"):
                self.assertNotIn(banned, text, name)


class ResponsiveTest(unittest.TestCase):
    def test_viewport_on_every_page(self):
        for page in PAGES:
            text = _read(page)
            self.assertIn('name="viewport"', text, page)
            self.assertIn("width=device-width", text, page)

    def test_mobile_first_breakpoints(self):
        css = _read("style.css")
        self.assertIn("@media (min-width: 720px)", css)
        page = _read("explain.html")
        self.assertIn("@media (min-width: 600px)", page)
        self.assertIn("@media (min-width: 700px)", page)

    def test_cards_use_fluid_widths(self):
        css = _read("style.css")
        self.assertIn("max-width: 960px;", css)
        page = _read("explain.html")
        self.assertIn("width: min(800px, calc(100% - 40px));", page)

    def test_buttons_stack_on_phones(self):
        css = _read("style.css")
        match = re.search(r"\.lens-actions \{(.*?)\}", css, re.S)
        self.assertTrue(match)
        self.assertIn("flex-direction: column;", match.group(1))

    def test_bottom_nav_stays_fixed(self):
        css = _read("style.css")
        match = re.search(r"\.bottom-nav \{(.*?)\}", css, re.S)
        self.assertTrue(match)
        self.assertIn("position: fixed;", match.group(1))
        self.assertIn("bottom: 0;", match.group(1))


class NoEmDashTest(unittest.TestCase):
    def test_no_em_or_en_dash_in_i18n(self):
        text = _read("i18n.js")
        self.assertNotIn("—", text)
        self.assertNotIn("–", text)


class BackendSmokeTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def test_home_serves_index(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("LifeBridge Lens", res.get_data(as_text=True))

    def test_explain_needs_photo(self):
        res = self.client.post("/explain", data={},
                               content_type="multipart/form-data")
        self.assertEqual(res.status_code, 400)

    def test_ask_needs_question(self):
        res = self.client.post("/ask", json={})
        self.assertEqual(res.status_code, 400)

    def test_unknown_page_is_404(self):
        res = self.client.get("/no-such-page.html")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
