"""Explain chat-page tests: sidebar, thread, composer, turns.

The Lens page is a messaging-style chat: a desktop sidebar, a
scrolling conversation thread with a welcome state, LifeBridge turns
that keep old results as frozen snapshots, and a fixed composer.
All scan logic (requests, parsing, modes, saving, calendar, staff
card, sample, storage keys) is unchanged and covered by the earlier
suites; these tests cover the new layout and its wiring.

Run from the project root:
    python -m unittest tests.test_explain_chat -v
"""
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("en", "ne", "vi", "my")

NEW_KEYS = (
    "explain.chatEyebrow",
    "explain.chatTitle",
    "explain.chatWelcomeTitle",
    "explain.chatWelcomeSub",
    "explain.cardGalleryTitle",
    "explain.cardSampleSub",
    "explain.cardPhotoSub",
    "explain.cardGallerySub",
    "explain.askComposer",
    "explain.askNeedPhoto",
    "explain.youExplain",
    "explain.qStepByStep",
    "explain.qStepByStepAsk",
    "sidebar.newScan",
    "sidebar.helper",
    "sidebar.savedDeadlines",
    "sidebar.offline",
    "sidebar.noSaved",
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


class ChatLayoutTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_sidebar(self):
        for marker in ('class="chat-sidebar"', '"sidebar.newScan"',
                       '"sidebar.helper"', '"sidebar.savedDeadlines"',
                       'id="side-dates"', 'id="helper-btn"',
                       "window.LBChat", ".open()"):
            self.assertIn(marker, self.page)
        self.assertRegex(self.page,
                         r"\.chat-sidebar\s*\{[^}]*?width: 270px;")
        self.assertRegex(self.page,
                         r"\.chat-sidebar\s*\{[^}]*?background: #13203f;")

    def test_sidebar_saved_list_reads_storage(self):
        self.assertIn("function renderSideDates()", self.page)
        self.assertIn('localStorage.getItem("lb_dates")', self.page)
        self.assertIn(".slice(0, 3)", self.page)
        self.assertIn('"sidebar.noSaved"', self.page)

    def test_desktop_hides_chrome(self):
        self.assertIn("@media (min-width: 1024px)", self.page)
        start = self.page.index("@media (min-width: 1024px)")
        block = self.page[start:start + 1200]
        self.assertIn(".site-header", block)
        self.assertIn(".bottom-nav", block)
        self.assertIn("display: none;", block)

    def test_main_head(self):
        for marker in ('class="chat-main-head"',
                       '"explain.chatEyebrow"', '"explain.chatTitle"'):
            self.assertIn(marker, self.page)
        self.assertRegex(self.page,
                         r"\.chat-title\s*\{[^}]*?font-size: 26px;")

    def test_mobile_head(self):
        for marker in ('class="chat-top"', 'class="chat-back"',
                       "LifeBridge Lens"):
            self.assertIn(marker, self.page)

    def test_status_badges(self):
        self.assertEqual(self.page.count('class="status-badge"'), 2)
        self.assertIn("function updateNetBadges()", self.page)
        self.assertIn('"sidebar.offline"', self.page)
        self.assertIn('badge.classList.toggle("off", offline)', self.page)

    def test_thread_width(self):
        self.assertRegex(self.page,
                         r"\.chat-main\s*\{[^}]*?max-width: 820px;")


class WelcomeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_welcome_block(self):
        for marker in ('id="welcome"', '"chat.welcomeKicker"',
                       '"explain.chatWelcomeTitle"',
                       '"explain.chatWelcomeSub"',
                       '"explain.privacyHint"',
                       "residence card number",
                       "hideWelcome()"):
            self.assertIn(marker, self.page)
        self.assertRegex(self.page,
                         r"\.welcome-icon\s*\{[^}]*?width: 72px;")
        self.assertRegex(self.page,
                         r"\.welcome-title\s*\{[^}]*?font-size: 22px;")

    def test_suggestion_cards(self):
        for marker in ('id="sample-btn"', 'id="snap-btn"',
                       'id="gallery-btn"', "Try a sample notice",
                       '"explain.sampleBtn"', '"index.step1"',
                       '"explain.cardGalleryTitle"',
                       '"explain.cardSampleSub"',
                       '"explain.cardPhotoSub"',
                       '"explain.cardGallerySub"'):
            self.assertIn(marker, self.page)
        self.assertRegex(self.page,
                         r"\.suggest-card\s*\{[^}]*?min-height: 64px;")


class ComposerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_photo_inputs(self):
        self.assertIn('id="photo"', self.page)
        self.assertIn('capture="environment"', self.page)
        self.assertIn('id="photo-gallery"', self.page)
        self.assertIn("new DataTransfer()", self.page)

    def test_photo_chip(self):
        for marker in ('id="photo-chip"', 'id="preview"',
                       'id="photo-name"', 'id="photo-remove"',
                       'id="explain-btn"', '"explain.submit"',
                       "function clearPhotoChip()"):
            self.assertIn(marker, self.page)
        self.assertRegex(self.page,
                         r"\.photo-chip #explain-btn\s*\{[^}]*?min-height: 44px;")

    def test_ask_box(self):
        for marker in ('id="ask-form"', 'id="ask-input"',
                       'id="ask-btn"', 'id="ask-status"',
                       'id="attach-btn"', 'id="language"',
                       '"explain.ask"', '"chat.sendHint"'):
            self.assertIn(marker, self.page)
        self.assertIn('<textarea id="ask-input"', self.page)
        self.assertIn('e.key === "Enter" && !e.shiftKey', self.page)
        self.assertIn("Math.min(askInput.scrollHeight, 135)", self.page)

    def test_ask_gating(self):
        self.assertIn("function updateAskState()", self.page)
        self.assertIn('"explain.askComposer"', self.page)
        self.assertIn('"explain.askNeedPhoto"', self.page)
        self.assertIn("askInput.disabled = !hasResult;", self.page)

    def test_mode_stays_auto(self):
        self.assertIn('<option value="auto" selected', self.page)
        self.assertIn('id="mode"', self.page)

    def test_ai_note(self):
        self.assertIn('"index.note"', self.page)

    def test_composer_tap_targets(self):
        self.assertRegex(self.page,
                         r"\.icon-btn\s*\{[^}]*?min-height: 44px;")
        self.assertRegex(self.page,
                         r"#ask-btn\s*\{[^}]*?min-height: 44px;")


class TurnsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_you_photo_row(self):
        for marker in ("function addYouPhotoRow(",
                       '"explain.youExplain"',
                       "lb-msg lb-msg-user"):
            self.assertIn(marker, self.page)
        self.assertRegex(self.page,
                         r"\.you-photo\s*\{[^}]*?max-width: 220px;")
        self.assertRegex(self.page,
                         r"\.you-photo\s*\{[^}]*?border-radius: 8px;")

    def test_turns_hold_live_sections(self):
        self.assertIn("function newTurn()", self.page)
        self.assertIn('"lb-turn"', self.page)
        self.assertIn('"lb-turn-body"', self.page)
        self.assertIn('getElementById("loading-card")', self.page)
        self.assertIn('getElementById("result-card")', self.page)

    def test_old_results_freeze(self):
        self.assertIn("function freezeResult()", self.page)
        self.assertIn("cloneNode(true)", self.page)
        self.assertIn("removeAttribute(\"id\")", self.page)
        self.assertIn("hasResult = true;", self.page)

    def test_thread_keeps_old_rows(self):
        self.assertNotIn('thread.innerHTML = "";', self.page)

    def test_step_chip(self):
        self.assertIn('id="step-chip"', self.page)
        self.assertIn('"explain.qStepByStep"', self.page)
        self.assertIn('"explain.qStepByStepAsk"', self.page)
        self.assertIn('chip.id === "step-chip"', self.page)


class LogicKeptTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_requests_and_parsing_kept(self):
        for marker in ('fetchWithTimeout("/explain"',
                       'fetchWithTimeout("/ask"',
                       "function parseExplainReply(",
                       'history: chatHistory.slice(-10)',
                       'addMsg("chat-q", question);',
                       'addMsg("chat-a", answer);',
                       "function showThinking()",
                       "function updateKindLabel()"):
            self.assertIn(marker, self.page)

    def test_result_ids_kept(self):
        for marker in ('id="result-card"', 'id="summary-bar"',
                       'id="summary-deadline"', 'id="summary-amount"',
                       'id="save-date-btn"', 'id="save-date-cal"',
                       'id="result-staff"', 'id="followup-card"',
                       'id="loading-card"', 'id="chat-thread"'):
            self.assertIn(marker, self.page)

    def test_storage_keys_kept(self):
        self.assertIn('"lb_dates"', self.page)
        self.assertIn('"lb_lang"', _read("i18n.js"))


class OldFormGoneTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_step_cards_gone(self):
        self.assertNotIn('class="lens-top"', self.page)
        self.assertNotIn('<label class="upload-area">', self.page)
        self.assertNotIn('<div class="form-actions">', self.page)
        self.assertNotIn('"explain.step1"', self.page)
        self.assertNotIn('"explain.step2"', self.page)

    def test_dates_link_moved_to_sidebar(self):
        self.assertNotIn('id="view-dates-btn"', self.page)
        self.assertNotIn("explain.viewDatesPage", self.page)


class ChatTranslationTest(unittest.TestCase):
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


class ChatDarkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = _read("style.css")

    def test_dark_covers_chat_page(self):
        for selector in ('html[data-theme="dark"] .chat-top',
                         'html[data-theme="dark"] .status-badge',
                         'html[data-theme="dark"] .chat-title',
                         'html[data-theme="dark"] .welcome-icon',
                         'html[data-theme="dark"] .suggest-card',
                         'html[data-theme="dark"] .chat-composer-bar',
                         'html[data-theme="dark"] .chat-composer',
                         'html[data-theme="dark"] #ask-input',
                         'html[data-theme="dark"] .photo-chip',
                         'html[data-theme="dark"] .icon-btn',
                         'html[data-theme="dark"] .composer-note',
                         'html[data-theme="dark"] .you-photo'):
            self.assertIn(selector, self.css)


class LayoutFixesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_sidebar_visible_on_desktop(self):
        blocks = re.findall(r"\.chat-sidebar\s*\{[^}]*\}", self.page)
        full = [b for b in blocks if "width: 270px" in b]
        self.assertTrue(full)
        for block in full:
            self.assertNotIn("display: none", block)
        start = self.page.index("@media (min-width: 1024px)")
        media = self.page[start:start + 1200]
        self.assertIn(".chat-sidebar", media)
        self.assertIn("display: flex;", media)

    def test_status_lines_above_box(self):
        bar = self.page.index('class="chat-composer-bar"')
        box = self.page.index('class="chat-composer">', bar)
        status = self.page.index('id="status"', bar)
        ask_status = self.page.index('id="ask-status"', bar)
        self.assertLess(bar, status)
        self.assertLess(status, box)
        self.assertLess(ask_status, box)
        self.assertIn("min-height: 0;", self.page)
        self.assertIn("#status:empty,", self.page)
        self.assertIn("#ask-status:empty {", self.page)

    def test_hidden_inputs_take_no_space(self):
        self.assertIn("clip-path: inset(50%);", self.page)
        self.assertIn("#explain-form {", self.page)

    def test_mode_select_hidden_but_present(self):
        self.assertIn('<details class="more-options" hidden>', self.page)
        self.assertIn('id="mode"', self.page)
        self.assertIn('<option value="auto" selected', self.page)

    def test_compact_composer(self):
        boxes = re.findall(r"\.chat-composer\s*\{[^}]*\}", self.page)
        self.assertTrue(any("padding: 12px 14px;" in b for b in boxes))
        inputs = re.findall(r"#ask-input\s*\{[^}]*\}", self.page)
        self.assertTrue(any("border: none;" in b for b in inputs))
        self.assertIn(".chat-composer:focus-within {", self.page)

    def test_result_has_no_outer_card(self):
        self.assertNotIn('class="card" id="result-card"', self.page)
        self.assertIn('id="result-card"', self.page)
        self.assertIn("#result-card > h2 {", self.page)

    def test_desktop_header_bar(self):
        heads = re.findall(r"\.chat-main-head\s*\{[^}]*\}", self.page)
        full = [b for b in heads if "padding: 28px 40px 18px;" in b]
        self.assertTrue(full)
        self.assertIn("background: #ffffff;", full[0])
        self.assertIn("border-bottom: 1px solid #e3e8f0;", full[0])
        badges = re.findall(r"\.chat-main-head \.status-badge\s*\{[^}]*\}",
                              self.page)
        self.assertTrue(badges)
        self.assertIn("background: #edf8f1;", badges[0])
        self.assertIn("border: 1px solid #cfe6d8;", badges[0])
        self.assertIn("border-radius: 8px;", badges[0])

    def test_page_chrome(self):
        self.assertRegex(self.page,
                         r"\.site-header\s*\{\s*display: none;\s*\}")
        self.assertRegex(self.page,
                         r"\.chat-fab\s*\{\s*display: none;\s*\}")
        bars = re.findall(r"\.chat-composer-bar\s*\{[^}]*\}", self.page)
        self.assertTrue(any("bottom: 72px;" in b for b in bars))

    def test_dark_covers_fixes(self):
        css = _read("style.css")
        for selector in ('html[data-theme="dark"] .chat-main-head',
                         'html[data-theme="dark"] .chat-main-head .status-badge',
                         'html[data-theme="dark"] .chat-composer:focus-within'):
            self.assertIn(selector, css)


if __name__ == "__main__":
    unittest.main()
