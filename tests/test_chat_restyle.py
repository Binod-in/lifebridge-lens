"""Chat restyle tests: shared message rows, welcome, composer, thinking.

Covers the chat-area restyle: new i18n keys in all four languages,
bubble-free message rows shared by the Ask LifeBridge panel and the
explain-page follow-up thread, the welcome state, the status badge,
the auto-growing composer, the thinking indicator, dark theme
coverage, and the design rules (no pills, no gradients, 48px taps).

Run from the project root:
    python -m unittest tests.test_chat_restyle -v
"""
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("en", "ne", "vi", "my")

NEW_KEYS = (
    "chat.welcomeKicker",
    "chat.welcomeTitle",
    "chat.welcomeSub",
    "chat.botName",
    "chat.userName",
    "chat.thinking",
    "chat.sendHint",
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


class ChatRestyleTranslationTest(unittest.TestCase):
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

    def test_english_welcome_wording(self):
        block = self.blocks["en"]
        self.assertIn('"chat.welcomeKicker": "NAMASTE"', block)
        self.assertIn('"chat.welcomeTitle": "What can I help you with today?"',
                      block)
        self.assertIn('"chat.thinking": "LifeBridge is thinking…"', block)
        self.assertIn('"chat.placeholder": "Ask a question…"', block)
        self.assertIn('"chat.offline": "Offline, saved answers only"', block)


class ChatPanelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.js = _read("chatbot.js")

    def test_shared_message_rows(self):
        for marker in ("lb-msg lb-msg-user", "lb-msg lb-msg-bot",
                       "lb-msg-avatar", "lb-msg-name", "lb-msg-text",
                       "lb-msg-time", '"chat.botName"', '"chat.userName"'):
            self.assertIn(marker, self.js)

    def test_bubble_classes_gone(self):
        for old in ("chat-msg-user", "chat-msg-bot", "chat-time",
                    "chat-chips", '"chat-form"', "showSuggestions",
                    "greeted"):
            self.assertNotIn(old, self.js)

    def test_status_badge_with_dot(self):
        self.assertIn("chat-status-dot", self.js)
        self.assertIn('"chat-status off"', self.js)
        self.assertIn('"chat.online"', self.js)
        self.assertIn('"chat.offline"', self.js)

    def test_close_button_uses_line_icon(self):
        self.assertIn("ICON_CLOSE", self.js)
        self.assertIn("M6 6l12 12M18 6L6 18", self.js)
        self.assertNotIn('textContent = "×"', self.js)

    def test_welcome_state(self):
        for marker in ("renderWelcome", "chat-welcome",
                       "chat-welcome-kicker", "chat-welcome-title",
                       "chat-welcome-sub", "chat-suggest-list",
                       "chat-suggest", '"chat.welcomeKicker"',
                       '"chat.welcomeTitle"', '"chat.welcomeSub"'):
            self.assertIn(marker, self.js)
        # Three suggestion buttons from the existing lists.
        self.assertIn("i < suggests.length && i < 3", self.js)
        self.assertIn("LB_CHAT_SUGGEST[chatLang()]", self.js)

    def test_composer(self):
        for marker in ("chat-composer", "chat-input", "chat-hint",
                       "chat-send", "createElement(\"textarea\")",
                       "autoGrow", "sendFromComposer", '"chat.sendHint"',
                       "shiftKey"):
            self.assertIn(marker, self.js)
        # Enter sends, Shift + Enter adds a new line.
        self.assertIn('event.key === "Enter" && !event.shiftKey', self.js)
        # The textarea grows from 1 to 5 lines (27px a line).
        self.assertIn("Math.min(input.scrollHeight, 135)", self.js)

    def test_line_icons_only(self):
        for marker in ("ICON_LENS", "ICON_PERSON", "ICON_ARROW_RIGHT",
                       "ICON_ARROW_UP", 'stroke="currentColor"',
                       'fill="none"'):
            self.assertIn(marker, self.js)

    def test_source_and_links_kept(self):
        self.assertIn("chat-source", self.js)
        self.assertIn('"chat.source"', self.js)
        self.assertIn('"chat.general"', self.js)
        self.assertIn("chat-links", self.js)


class ChatStyleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = _read("style.css")

    def test_message_row_styles(self):
        self.assertRegex(self.css,
                         r"\.lb-msg-avatar\s*\{[^}]*?width: 32px;")
        self.assertRegex(self.css,
                         r"\.lb-msg-avatar\s*\{[^}]*?border-radius: 8px;")
        self.assertRegex(
            self.css,
            r"\.lb-msg-bot \.lb-msg-avatar\s*\{[^}]*?background: #eaf1ff;")
        self.assertRegex(
            self.css,
            r"\.lb-msg-user \.lb-msg-avatar\s*\{[^}]*?background: #e7f0ea;")
        self.assertRegex(self.css,
                         r"\.lb-msg-text\s*\{[^}]*?font-size: 15px;")
        self.assertRegex(self.css,
                         r"\.lb-msg-text\s*\{[^}]*?line-height: 1\.8;")
        self.assertRegex(self.css,
                         r"\.lb-msg-text\s*\{[^}]*?white-space: pre-wrap;")

    def test_welcome_styles(self):
        self.assertRegex(self.css,
                         r"\.chat-welcome-icon\s*\{[^}]*?width: 64px;")
        self.assertRegex(self.css,
                         r"\.chat-welcome-icon\s*\{[^}]*?border-radius: 16px;")
        self.assertRegex(self.css,
                         r"\.chat-welcome-icon\s*\{[^}]*?background: #eaf1ff;")
        self.assertRegex(self.css,
                         r"\.chat-welcome-kicker\s*\{[^}]*?font-size: 12px;")
        self.assertRegex(
            self.css,
            r"\.chat-welcome-kicker\s*\{[^}]*?letter-spacing: 0\.08em;")
        self.assertRegex(self.css,
                         r"\.chat-welcome-title\s*\{[^}]*?font-size: 24px;")
        self.assertRegex(self.css,
                         r"\.chat-suggest\s*\{[^}]*?border-radius: 8px;")
        self.assertRegex(self.css,
                         r"\.chat-suggest\s*\{[^}]*?min-height: 48px;")

    def test_status_dot_styles(self):
        self.assertRegex(self.css,
                         r"\.chat-status-dot\s*\{[^}]*?width: 6px;")
        self.assertRegex(self.css,
                         r"\.chat-status-dot\s*\{[^}]*?height: 6px;")
        self.assertRegex(
            self.css,
            r"\.chat-status\.off \.chat-status-dot\s*\{[^}]*?background: #8a94a8;")

    def test_composer_styles(self):
        self.assertRegex(self.css,
                         r"\.chat-composer\s*\{[^}]*?border-radius: 14px;")
        self.assertRegex(
            self.css,
            r"\.chat-composer:focus-within\s*\{[^}]*?border-color: #1261ff;")
        self.assertIn("box-shadow: 0 0 0 3px #eaf1ff;", self.css)
        self.assertIn("@media (max-width: 399px)", self.css)

    def test_thinking_styles(self):
        self.assertIn(".lb-thinking {", self.css)
        self.assertIn(".lb-thinking-dots span {", self.css)
        self.assertIn("@keyframes lb-thinking-fade", self.css)
        self.assertIn("animation-delay: 0.2s;", self.css)
        self.assertIn("animation-delay: 0.4s;", self.css)

    def test_thinking_stops_without_motion(self):
        start = self.css.index("@media (prefers-reduced-motion: reduce)")
        block = self.css[start:]
        self.assertIn(".lb-thinking-dots span", block)
        self.assertIn("animation: none;", block)

    def test_no_pills_or_gradients(self):
        for name in ("style.css", "chatbot.js", "explain.html"):
            text = _read(name)
            self.assertNotIn("999px", text, name)
            self.assertNotIn("gradient", text, name)

    def test_dark_covers_chat_restyle(self):
        for selector in ('html[data-theme="dark"] .chat-head',
                         'html[data-theme="dark"] .chat-status',
                         'html[data-theme="dark"] .chat-close',
                         'html[data-theme="dark"] .lb-msg-text',
                         'html[data-theme="dark"] .lb-msg-bot .lb-msg-avatar',
                         'html[data-theme="dark"] .lb-msg-user .lb-msg-avatar',
                         'html[data-theme="dark"] .lb-msg-time',
                         'html[data-theme="dark"] .chat-welcome-icon',
                         'html[data-theme="dark"] .chat-welcome-title',
                         'html[data-theme="dark"] .chat-suggest',
                         'html[data-theme="dark"] .chat-composer',
                         'html[data-theme="dark"] .chat-input',
                         'html[data-theme="dark"] .lb-thinking'):
            self.assertIn(selector, self.css)


class FollowupRestyleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_followup_uses_shared_rows(self):
        for marker in ("lb-msg lb-msg-", "lb-msg-avatar", "lb-msg-name",
                       "lb-msg-text", "lb-msg-time", '"chat.botName"',
                       '"chat.userName"'):
            self.assertIn(marker, self.page)
        # The pinned call sites keep their shape.
        self.assertIn('addMsg("chat-q", question);', self.page)
        self.assertIn('addMsg("chat-a", answer);', self.page)

    def test_bubble_styles_gone(self):
        self.assertNotIn(".chat-q {", self.page)
        self.assertNotIn(".chat-a {", self.page)

    def test_thinking_indicator(self):
        for marker in ("showThinking()", "hideThinking()",
                       "function showThinking()", "function hideThinking()",
                       "lb-thinking", "lb-thinking-dots",
                       '"chat.thinking"'):
            self.assertIn(marker, self.page)
        ask_at = self.page.index("async function askQuestion(question)")
        shown = self.page.index("showThinking();", ask_at)
        hidden = self.page.index("hideThinking();", ask_at)
        guard = self.page.index("if (myEpoch !== scanEpoch) return;")
        self.assertLess(ask_at, shown)
        self.assertLess(shown, hidden)
        self.assertLess(hidden, guard)


if __name__ == "__main__":
    unittest.main()
