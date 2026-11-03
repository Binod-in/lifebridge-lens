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
                           "Noto+Sans+JP", "Noto+Sans+Myanmar",
                           "Noto+Serif+JP", "Noto+Serif+Devanagari"):
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

    def test_buttons_use_4px_radius(self):
        css = _read("style.css")
        self.assertRegex(css, r"\.btn\s*\{[^}]*?border-radius: 4px;")
        self.assertRegex(css, r"\.chip\s*\{[^}]*?border-radius: 4px;")
        self.assertRegex(css, r"\.chat-fab\s*\{[^}]*?border-radius: 4px;")
        self.assertRegex(css, r"\.chat-composer\s*\{[^}]*?border-radius: 4px;")
        self.assertRegex(css,
                         r"\.detail-card\s*\{[^}]*?border-radius: 4px;")
        page = _read("explain.html")
        self.assertRegex(page, r"\.chip\s*\{[^}]*?border-radius: 4px;")
        self.assertRegex(page, r"\.card\s*\{[^}]*?border-radius: 4px;")
        self.assertNotIn("999px", css)
        self.assertNotIn("999px", page)

    def test_no_big_radii_left(self):
        for name in ("style.css", "explain.html", "tracker.html"):
            text = _read(name)
            for radius in ("border-radius: 8px", "border-radius: 12px",
                           "border-radius: 14px", "border-radius: 16px"):
                self.assertNotIn(radius, text, name)

    def test_no_shadows(self):
        for name in ("style.css", "explain.html", "tracker.html"):
            self.assertNotIn("box-shadow", _read(name), name)

    def test_deadline_colors(self):
        css = _read("style.css")
        self.assertRegex(css,
                         r"\.due\s*\{[^}]*?background: #fef3c7;[^}]*?color: #b45309;")
        self.assertRegex(css,
                         r"\.due-soon\s*\{[^}]*?background: #fee2e2;[^}]*?color: #b91c1c;")
        self.assertRegex(css,
                         r"\.summary-bar\s*\{[^}]*?background: var\(--card\);")
        self.assertRegex(css,
                         r"\.summary-bar\s*\{[^}]*?border: 1\.5px solid var\(--accent\);")
        self.assertRegex(css,
                         r"\.summary-bar\.soon\s*\{[^}]*?background: var\(--soft\);")
        self.assertRegex(css,
                         r"\.summary-bar\.soon \.summary-days\s*\{[^}]*?color: var\(--accent\);")

    def test_washi_tokens(self):
        css = _read("style.css")
        start = css.index(":root {")
        block = css[start:start + 700]
        for line in ("--page: #f4efe6;", "--card: #fffdf8;",
                     "--line: #e2d8c6;", "--text: #2a2420;",
                     "--muted: #7a6e62;", "--accent: #b8322a;",
                     "--accent-text: #ffffff;", "--soft: #f6e3df;",
                     "--ok: #1f9d55;"):
            self.assertIn(line, block)

    def test_dark_theme_is_var_based(self):
        css = _read("style.css")
        start = css.index('html[data-theme="dark"] {')
        block = css[start:start + 700]
        for line in ("--page: #1c1916;", "--card: #26221e;",
                     "--line: #3a332c;", "--text: #efe7da;",
                     "--muted: #a99c8c;", "--accent: #e0675c;",
                     "--accent-text: #1c1916;", "--soft: #3a2622;"):
            self.assertIn(line, block)
        # Only fixed urgency colors keep their own dark rules.
        for selector in ('html[data-theme="dark"] .due',
                         'html[data-theme="dark"] .due-soon',
                         'html[data-theme="dark"] .net-banner'):
            self.assertIn(selector, css)
        for selector in ('html[data-theme="dark"] .hero-text',
                         'html[data-theme="dark"] .summary-bar',
                         'html[data-theme="dark"] .summary-big',
                         'html[data-theme="dark"] .check-list',
                         'html[data-theme="dark"] .scan-steps',
                         'html[data-theme="dark"] .chat-composer'):
            self.assertNotIn(selector, css)

    def test_serif_for_headings_and_numbers(self):
        css = _read("style.css")
        self.assertRegex(css, r"h1, h2, h3 \{[^}]*?font-family: var\(--serif\);")
        self.assertRegex(css,
                         r"\.logo-name\s*\{[^}]*?font-family: var\(--serif\);")
        self.assertRegex(css,
                         r"\.summary-big\s*\{[^}]*?font-family: var\(--serif\);")
        self.assertRegex(css,
                         r"\.summary-big\s*\{[^}]*?font-size: 26px;")
        self.assertRegex(css,
                         r"\.deadline-amount\s*\{[^}]*?font-family: var\(--serif\);")
        self.assertRegex(css,
                         r"\.summary-label\s*\{[^}]*?text-transform: uppercase;")

    def test_check_list_numbers(self):
        css = _read("style.css")
        self.assertRegex(css,
                         r"\.check-list li::before\s*\{[^}]*?width: 24px;")
        self.assertRegex(
            css,
            r"\.check-list li::before\s*\{[^}]*?background: var\(--soft\);")
        self.assertRegex(
            css,
            r"\.check-list li::before\s*\{[^}]*?color: var\(--accent\);")
        self.assertRegex(css,
                         r"\.check-list li::before\s*\{[^}]*?border-radius: 4px;")

    def test_hanko_stamp(self):
        css = _read("style.css")
        self.assertRegex(css, r"\.hanko\s*\{[^}]*?width: 62px;")
        self.assertRegex(css, r"\.hanko\s*\{[^}]*?height: 62px;")
        self.assertRegex(css, r"\.hanko\s*\{[^}]*?border-radius: 50%;")
        self.assertRegex(
            css,
            r"\.hanko\s*\{[^}]*?border: 2\.5px solid var\(--accent\);")
        self.assertRegex(css, r"\.hanko\s*\{[^}]*?transform: rotate\(-8deg\);")
        self.assertRegex(css,
                         r"#summary-hanko-num\s*\{[^}]*?font-size: 20px;")

    def test_deadline_count_is_small_stamp(self):
        css = _read("style.css")
        self.assertRegex(
            css,
            r"\.deadline-count\s*\{[^}]*?border: 1\.5px solid var\(--muted\);")
        self.assertRegex(css, r"\.deadline-count\s*\{[^}]*?transform: rotate\(-2deg\);")
        self.assertRegex(
            css,
            r"\.deadline-count\.soon\s*\{[^}]*?color: var\(--accent\);")


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
        self.assertIn("function updateSummary()", self.page)
        self.assertIn("function daysUntil(dateStr)", self.page)
        self.assertIn('add("soon")', self.page)
        self.assertIn('add("passed")', self.page)

    def test_summary_bar_single_days_count(self):
        # Days left live only in the hanko stamp: no second text
        # line, no era label prefix. The big date comes from
        # deadline_date in the user's language.
        self.assertNotIn('id="summary-days"', self.page)
        self.assertNotIn('"explain.daysLeft"', self.page)
        self.assertNotIn('"explain.dayLeft"', self.page)
        self.assertNotIn('"explain.deadlinePassed"', self.page)
        self.assertNotIn('"explain.eraLabel"', self.page)
        self.assertNotIn('.replace("{n}", String(n))', self.page)
        self.assertIn("function toLocaleDate(dateStr)", self.page)
        self.assertIn("toLocaleDate(lastDeadlineDate) || lastDeadlineText",
                      self.page)
        self.assertIn("getElementById(\"summary-era\").textContent = "
                      "toEraDate(lastDeadlineDate);", self.page)

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
        self.assertIn(".scan-steps li.current", css)
        self.assertIn(".scan-steps li.done", css)
        self.assertIn("@keyframes lb-spin", css)
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
