"""Site bug-fix tests: tracker safety, theme script, dark theme, chat scroll.

Run from the project root:
    python -m unittest tests.test_sitebugs -v
"""
import glob
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("en", "ne", "vi", "my")


def _read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


class TrackerSafetyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("tracker.html")

    def test_save_uses_try_catch(self):
        self.assertIn("const save = (key, value) => {", self.page)
        self.assertIn("localStorage.setItem(key, JSON.stringify(value));", self.page)
        self.assertIn("return false;", self.page)

    def test_save_failure_shows_message(self):
        self.assertIn("tracker.saveFailed", self.page)

    def test_broken_entries_skipped_on_load(self):
        self.assertIn("function cleanEntries(list)", self.page)
        self.assertIn("cleanEntries(load(ENTRIES_KEY, []))", self.page)

    def test_broken_goals_skipped_on_load(self):
        self.assertIn("function cleanGoals(list)", self.page)
        self.assertIn("cleanGoals(load(GOALS_KEY, []))", self.page)

    def test_goal_name_uses_text_content(self):
        self.assertIn('row.querySelector(".entry-goal").textContent', self.page)
        self.assertNotIn('goal.name) : ""}</small>', self.page)

    def test_delete_goal_button_with_confirm(self):
        self.assertIn('t("tracker.deleteGoal", "Delete goal")', self.page)
        self.assertIn('confirm(t("tracker.deleteGoalConfirm"', self.page)


class TrackerKeysTest(unittest.TestCase):
    def test_new_keys_in_all_languages(self):
        src = _read("i18n.js")
        for key in ("tracker.deleteGoal", "tracker.deleteGoalConfirm",
                    "tracker.saveFailed"):
            self.assertEqual(src.count('"%s"' % key), 4, key)


class ThemeScriptTest(unittest.TestCase):
    def test_every_page_sets_theme_in_head(self):
        pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))
        self.assertEqual(len(pages), 5)
        missing = []
        for path in pages:
            with open(path, encoding="utf-8") as f:
                head = f.read().split("</head>")[0]
            if ('localStorage.getItem("lb_theme")' not in head
                    or 'setAttribute("data-theme", theme)' not in head):
                missing.append(os.path.basename(path))
        self.assertEqual(missing, [])


class HeaderProfileTest(unittest.TestCase):
    """No Demo Profile button is injected into the shared header."""

    @classmethod
    def setUpClass(cls):
        cls.src = _read("i18n.js")

    def test_no_profile_link_injected(self):
        self.assertNotIn("addProfileLink", self.src)

    def test_menu_and_bottom_nav_builders_kept(self):
        self.assertIn("addMenuButton", self.src)
        self.assertIn("addBottomNav", self.src)

    def test_bottom_nav_links_only_repo_pages(self):
        start = self.src.index("function addBottomNav")
        end = self.src.index("function themePreference")
        block = self.src[start:end]
        for href in ("index.html", "explain.html", "dates.html",
                     "tracker.html"):
            self.assertIn('"%s"' % href, block)
        self.assertNotIn("guide.html", block)
        self.assertNotIn("login.html", block)


class DarkThemeTest(unittest.TestCase):
    """Dark theme keeps tracker tiles and Lens surfaces readable."""

    @classmethod
    def setUpClass(cls):
        cls.css = _read("style.css")

    def test_dark_tracker_tile_text_is_light(self):
        self.assertRegex(
            self.css,
            r'html\[data-theme="dark"\] \.summary-box span \{\s*'
            r'color: #c3cede;')
        self.assertRegex(
            self.css,
            r'html\[data-theme="dark"\] \.summary-box strong \{\s*'
            r'color: #ffffff;')

    def test_dark_lens_surfaces_covered(self):
        for selector in ('html[data-theme="dark"] .bottom-nav',
                         'html[data-theme="dark"] .chat-panel',
                         'html[data-theme="dark"] .date-list li',
                         'html[data-theme="dark"] .footer-links a',
                         'html[data-theme="dark"] .page-lead',
                         'html[data-theme="dark"] .net-banner',
                         'html[data-theme="dark"] .main-nav a'):
            self.assertIn(selector, self.css)


class ChatScrollTest(unittest.TestCase):
    """Open chat locks page scroll; messages contain overscroll."""

    @classmethod
    def setUpClass(cls):
        cls.css = _read("style.css")
        cls.js = _read("chatbot.js")

    def test_message_area_contains_overscroll(self):
        self.assertRegex(self.css,
                         r'\.chat-msgs\s*\{[^}]*?overscroll-behavior: contain;')

    def test_open_chat_fixes_body(self):
        self.assertRegex(self.css,
                         r'html\.chat-open body \{\s*position: fixed;')

    def test_toggle_saves_and_restores_scroll(self):
        self.assertIn("document.body.style.top", self.js)
        self.assertIn("window.scrollTo", self.js)
        self.assertIn('classList.add("chat-open")', self.js)
        self.assertIn('classList.remove("chat-open")', self.js)


if __name__ == "__main__":
    unittest.main()
