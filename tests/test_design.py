"""Design-system tests: fonts, colors, shapes, text rules, components.

Run from the project root:
    python -m unittest tests.test_design -v
"""
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ("index.html", "explain.html", "dates.html", "tracker.html",
         "offline.html")


def _read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


class FontTest(unittest.TestCase):
    def test_every_page_loads_noto_fonts(self):
        for page in PAGES:
            text = _read(page)
            self.assertIn("fonts.googleapis.com", text, page)
            for family in ("Noto+Sans:", "Noto+Sans+Devanagari",
                           "Noto+Sans+JP", "Noto+Sans+Myanmar"):
                self.assertIn(family, text, page)

    def test_base_type(self):
        css = _read("style.css")
        self.assertIn('"Noto Sans", "Noto Sans Devanagari", '
                      '"Noto Sans JP", "Noto Sans Myanmar", system-ui', css)
        self.assertRegex(css, r"html\s*\{\s*font-size: 17px;")
        self.assertRegex(css, r"body\s*\{[^}]*?line-height: 1.7;")


class ShapeColorTest(unittest.TestCase):
    def test_no_gradients(self):
        for name in ("style.css", "explain.html", "tracker.html",
                     "dates.html"):
            self.assertNotIn("gradient", _read(name), name)

    def test_buttons_use_8px_radius(self):
        css = _read("style.css")
        self.assertRegex(css, r"\.btn\s*\{[^}]*?border-radius: 8px;")
        self.assertRegex(css, r"\.chip\s*\{[^}]*?border-radius: 8px;")
        self.assertRegex(css, r"\.chat-fab\s*\{[^}]*?border-radius: 8px;")
        page = _read("explain.html")
        self.assertRegex(page, r"\.chip\s*\{[^}]*?border-radius: 8px;")
        self.assertNotIn("999px", css)
        self.assertNotIn("999px", page)

    def test_deadline_colors(self):
        css = _read("style.css")
        self.assertRegex(css,
                         r"\.due\s*\{[^}]*?background: #fef3c7;[^}]*?color: #b45309;")
        self.assertRegex(css,
                         r"\.due-soon\s*\{[^}]*?background: #fee2e2;[^}]*?color: #b91c1c;")
        self.assertRegex(css,
                         r"\.summary-bar\s*\{[^}]*?background: #fef3c7;")
        self.assertRegex(css,
                         r"\.summary-bar\.soon\s*\{[^}]*?background: #fee2e2;")

    def test_dark_theme_covers_new_elements(self):
        css = _read("style.css")
        for selector in ('html[data-theme="dark"] .hero-text',
                         'html[data-theme="dark"] .example-before',
                         'html[data-theme="dark"] .steps li',
                         'html[data-theme="dark"] .summary-bar',
                         'html[data-theme="dark"] .summary-big',
                         'html[data-theme="dark"] .check-list',
                         'html[data-theme="dark"] .scan-steps',
                         'html[data-theme="dark"] .due',
                         'html[data-theme="dark"] .due-soon'):
            self.assertIn(selector, css)


class TextRulesTest(unittest.TestCase):
    def test_no_em_or_en_dashes_in_ui(self):
        for name in PAGES + ("i18n.js", "chatbot.js"):
            text = _read(name)
            self.assertNotIn("\u2014", text, name)
            self.assertNotIn("\u2013", text, name)

    def test_no_emoji_in_ui_or_readme(self):
        pat = re.compile("[\u2600-\u27bf\u2b00-\u2bff"
                         "\U0001f000-\U0001faff\ufe0f]")
        for name in PAGES + ("i18n.js", "chatbot.js", "README.md"):
            self.assertEqual(pat.findall(_read(name)), [], name)


class IndexPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("index.html")

    def test_hero_and_example(self):
        self.assertIn('"index.hero"', self.page)
        self.assertIn("Got a Japanese letter", self.page)
        self.assertIn('"index.exampleLabel"', self.page)
        self.assertIn("\u56fd\u6c11\u5065\u5eb7\u4fdd\u967a\u6599", self.page)
        self.assertIn("12,340\u5186", self.page)
        self.assertIn('"index.exampleAfter"', self.page)

    def test_three_steps_with_icons(self):
        self.assertIn('<ol class="steps">', self.page)
        for key in ("index.step1", "index.step2", "index.step3"):
            self.assertIn('"%s"' % key, self.page)
        start = self.page.index('<ol class="steps">')
        end = self.page.index("</ol>", start)
        self.assertEqual(self.page.count("<svg", start, end), 3)

    def test_main_buttons_kept(self):
        start = self.page.index('<div class="lens-actions">')
        end = self.page.index("</div>", start)
        block = self.page[start:end]
        for href in ("explain.html", "dates.html", "tracker.html"):
            self.assertIn(href, block)


class ExplainDesignTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_summary_bar(self):
        self.assertIn('id="summary-bar"', self.page)
        self.assertIn('id="summary-deadline"', self.page)
        self.assertIn('id="summary-amount"', self.page)
        self.assertIn('id="summary-days"', self.page)
        self.assertIn("function updateSummary()", self.page)
        self.assertIn("function daysUntil(dateStr)", self.page)
        for key in ("explain.daysLeft", "explain.dayLeft",
                    "explain.deadlinePassed"):
            self.assertIn('"%s"' % key, self.page)
        self.assertIn('add("soon")', self.page)
        self.assertIn('add("passed")', self.page)
        self.assertIn('.replace("{n}", String(n))', self.page)

    def test_next_steps_checklist(self):
        self.assertIn('<ol id="result-next" class="check-list">', self.page)
        self.assertIn("function fillCard(id, text)", self.page)
        self.assertIn('createElement("li")', self.page)

    def test_check_card_highlight(self):
        self.assertIn("check-card", self.page)
        self.assertIn("border-left: 4px solid #b45309;", _read("style.css"))

    def test_card_title_icons(self):
        # What, why, importance, next steps, check. Deadline and amount
        # live only in the summary box, without their own cards.
        found = re.findall(r'<h3><svg class="card-icon"', self.page)
        self.assertEqual(len(found), 5)

    def test_loading_steps(self):
        self.assertIn('id="scan-steps"', self.page)
        for key in ("explain.load1", "explain.load2", "explain.load3"):
            self.assertIn('"%s"' % key, self.page)
        self.assertIn("startScanSteps();", self.page)
        self.assertIn("stopScanSteps();", self.page)
        css = _read("style.css")
        self.assertIn(".scan-steps li.on", css)
        self.assertIn("prefers-reduced-motion", css)


class DatesDesignTest(unittest.TestCase):
    def test_urgency_chips(self):
        page = _read("dates.html")
        self.assertIn("function dueClass(dateStr)", page)
        self.assertIn('"due due-soon"', page)
        self.assertIn('"due due-passed"', page)


class TapTargetTest(unittest.TestCase):
    def test_interactive_elements_are_48px(self):
        css = _read("style.css")
        for selector in (r"\.btn", r"\.chip", r"\.main-nav a",
                         r"\.footer-links a", r"\.bottom-nav a",
                         r"\.menu-btn", r"\.lang-select", r"\.chat-close",
                         r"\.saved-back"):
            self.assertRegex(css, selector + r"\s*\{[^}]*?min-height: 48px;",
                             selector)
        page = _read("explain.html")
        self.assertRegex(page, r"\.chip\s*\{[^}]*?min-height: 48px;")


if __name__ == "__main__":
    unittest.main()
