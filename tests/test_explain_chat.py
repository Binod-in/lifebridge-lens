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
    "explain.hankoDays",
    "explain.hankoDay",
    "explain.hankoOverdue",
    "explain.slowDown",
    "explain.tryAgain",
    "explain.longLetter",
    "explain.stop",
    "explain.stopped",
    "explain.jumpLatest",
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
                         r"\.chat-sidebar\s*\{[^}]*?background: #2a2420;")

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
        # One composer: the chip holds thumbnail, name and remove only;
        # Send runs the scan.
        for marker in ('id="photo-chip"', 'id="preview"',
                       'id="photo-name"', 'id="photo-remove"',
                       "function clearPhotoChip()"):
            self.assertIn(marker, self.page)
        self.assertNotIn('id="explain-btn"', self.page)

    def test_ask_box(self):
        for marker in ('id="ask-form"', 'id="ask-input"',
                       'id="ask-btn"', 'id="ask-status"',
                       'id="attach-btn"', 'id="language"',
                       '"explain.ask"', '"chat.sendHint"'):
            self.assertIn(marker, self.page)
        self.assertIn('<textarea id="ask-input"', self.page)
        self.assertIn('e.key === "Enter" && !e.shiftKey', self.page)
        self.assertIn("Math.min(askInput.scrollHeight, 135)", self.page)

    def test_ask_always_enabled(self):
        self.assertIn("function updateAskState()", self.page)
        self.assertIn('"explain.askComposer"', self.page)
        self.assertIn('"explain.askNeedPhoto"', self.page)
        self.assertIn("askInput.disabled = false;", self.page)
        self.assertNotIn("askInput.disabled = !hasResult;", self.page)

    def test_unified_send(self):
        for marker in ("function sendComposer()",
                       "function runScan()",
                       "pendingQuestion = askInput.value.trim();",
                       "askQuestion(firstQ);",
                       '"explain.needPhotoFirst"',
                       "addYouPhotoRow(preview.src, pendingQuestion);"):
            self.assertIn(marker, self.page)

    def test_send_label(self):
        self.assertIn('"explain.ask": "Send"', _read("i18n.js"))
        self.assertIn('id="ask-btn"', self.page)
        self.assertIn('"explain.ask"', self.page)

    def test_hint_clears_on_photo_or_typing(self):
        chip_at = self.page.index("function showPhotoChip(input) {")
        self.assertIn('askStatus.textContent = "";',
                      self.page[chip_at:chip_at + 400])
        input_at = self.page.index('askInput.addEventListener("input"')
        block = self.page[input_at:input_at + 300]
        self.assertIn('askStatus.textContent = "";', block)
        self.assertIn("autoGrowAsk();", block)

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

    def test_composer_one_row(self):
        # Paperclip, textarea, square Send in one row; hint in the
        # small row under it; language select up in the chat header.
        main_at = self.page.index('class="composer-main"')
        attach_at = self.page.index('id="attach-btn"', main_at)
        input_at = self.page.index('id="ask-input"', main_at)
        send_at = self.page.index('id="ask-btn"', main_at)
        row_at = self.page.index('class="composer-row"', main_at)
        self.assertLess(attach_at, input_at)
        self.assertLess(input_at, send_at)
        self.assertLess(send_at, row_at)
        self.assertNotIn('id="language"', self.page[row_at:row_at + 1200])
        self.assertIn("chat-hint", self.page[row_at:row_at + 1200])
        head_at = self.page.index('class="chat-top"')
        self.assertIn('id="language"', self.page[head_at:head_at + 2500])
        self.assertIn('id="lang-slot-desktop"', self.page)
        self.assertIn("placeLanguageSelect();", self.page)
        self.assertRegex(self.page,
                         r"\.composer-main\s*\{[^}]*?display: flex;")
        self.assertRegex(self.page,
                         r"#ask-btn\s*\{[^}]*?width: 44px;")
        self.assertRegex(self.page,
                         r"#ask-btn\s*\{[^}]*?height: 44px;")


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
                         r"\.you-photo\s*\{[^}]*?border-radius: 4px;")

    def test_you_row_is_dark_box(self):
        self.assertRegex(
            self.page,
            r"#chat-thread \.lb-msg-user \.lb-msg-main\s*\{[^}]*?max-width: 260px;")
        self.assertRegex(
            self.page,
            r"#chat-thread \.lb-msg-user \.lb-msg-text\s*\{[^}]*?background: var\(--text\);")
        self.assertRegex(
            self.page,
            r"#chat-thread \.lb-msg-user \.lb-msg-text\s*\{[^}]*?color: var\(--card\);")

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

    def test_dark_chat_page_uses_tokens(self):
        self.assertIn('html[data-theme="dark"] {', self.css)
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
            self.assertNotIn(selector, self.css)


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
        self.assertIn("background: var(--card);", full[0])
        self.assertIn("border-bottom: 1px solid var(--line);", full[0])
        badges = re.findall(r"\.chat-main-head \.status-badge\s*\{[^}]*\}",
                              self.page)
        self.assertTrue(badges)
        self.assertIn("background: var(--soft);", badges[0])
        self.assertIn("border: 1px solid var(--line);", badges[0])
        self.assertIn("border-radius: 4px;", badges[0])

    def test_page_chrome(self):
        self.assertRegex(self.page,
                         r"\.site-header\s*\{\s*display: none;\s*\}")
        self.assertRegex(self.page,
                         r"\.chat-fab\s*\{\s*display: none;\s*\}")
        self.assertRegex(self.page,
                         r"\.bottom-nav\s*\{\s*display: none;\s*\}")
        bars = re.findall(r"\.chat-composer-bar\s*\{[^}]*\}", self.page)
        self.assertTrue(any("bottom: 0;" in b for b in bars))
        self.assertFalse(any("bottom: 72px;" in b for b in bars))
        self.assertIn("env(safe-area-inset-bottom", self.page)

    def test_dark_fixes_use_tokens(self):
        css = _read("style.css")
        for selector in ('html[data-theme="dark"] .chat-main-head',
                         'html[data-theme="dark"] .chat-main-head .status-badge',
                         'html[data-theme="dark"] .chat-composer:focus-within'):
            self.assertNotIn(selector, css)


class AppShellTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_no_footer_on_chat_page(self):
        self.assertNotIn("<footer", self.page)

    def test_footer_kept_elsewhere(self):
        for name in ("index.html", "dates.html", "tracker.html"):
            self.assertIn('<footer class="site-footer">', _read(name))

    def test_page_locked_thread_scrolls(self):
        self.assertIn("overflow: hidden;", self.page)
        self.assertIn("height: 100dvh;", self.page)
        mains = re.findall(r"\.chat-main\s*\{[^}]*\}", self.page)
        self.assertTrue(any("overflow-y: auto" in m for m in mains))
        self.assertTrue(any("min-height: 0" in m for m in mains))
        # Thread padding tracks the real composer height plus 16px
        # through a ResizeObserver, not a fixed guess.
        self.assertIn("new ResizeObserver(syncThreadPadding)"
                      ".observe(composerBar);", self.page)
        self.assertIn("offsetHeight + 16", self.page)
        self.assertNotIn("padding-bottom: 260px", self.page)
        self.assertNotIn("padding-bottom: 190px", self.page)

    def test_amount_muted_when_missing(self):
        self.assertIn("lastAmountMissing", self.page)
        self.assertIn('classList.toggle("summary-muted", lastAmountMissing)',
                      self.page)
        muted = re.findall(r"\.summary-big\.summary-muted\s*\{[^}]*\}",
                            self.page)
        self.assertTrue(muted)
        self.assertIn("font-size: 13px;", muted[0])
        self.assertIn("font-weight: 400;", muted[0])
        self.assertIn("color: var(--muted);", muted[0])
        self.assertNotIn('html[data-theme="dark"] .summary-big.summary-muted',
                         _read("style.css"))


class LoadingStateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_flat_loading_message(self):
        self.assertIn('id="loading-card"', self.page)
        self.assertNotIn('class="card load-card"', self.page)
        self.assertNotIn('id="loading-thumb"', self.page)
        self.assertNotIn('id="loading-name"', self.page)
        self.assertNotIn('id="loading-lang"', self.page)
        self.assertNotIn('"explain.loadingTitle"', self.page)
        for marker in ('id="scan-steps"', '"explain.load1"',
                       '"explain.loadPrivacy"'):
            self.assertIn(marker, self.page)

    def test_step_states(self):
        for marker in ('toggle("done", i < at)',
                       'toggle("current", i === at)',
                       "setInterval(advance, 4000)",
                       "function startScanSteps()",
                       "function stopScanSteps()"):
            self.assertIn(marker, self.page)
        self.assertNotIn('add("on")', self.page)
        css = _read("style.css")
        for marker in (".scan-steps li.current::before",
                       ".scan-steps li.done::before",
                       "@keyframes lb-spin"):
            self.assertIn(marker, css)

    def test_single_announcement(self):
        # One Send button: no Scan button, no spinner swap, no repeated
        # status line; the steps announce the load once.
        self.assertNotIn('"explain.explaining"', self.page)
        self.assertNotIn('"explain.reading"', self.page)
        self.assertNotIn('id="explain-btn"', self.page)
        self.assertNotIn('class="btn-spinner"', self.page)
        self.assertNotIn(".btn-spinner", self.page)
        self.assertIn("function sendComposer()", self.page)
        self.assertIn('id="ask-btn"', self.page)

    def test_spinner_css(self):
        css = _read("style.css")
        start = css.index("@media (prefers-reduced-motion: reduce)")
        block = css[start:]
        self.assertIn(".scan-steps li.current::before", block)
        self.assertNotIn(".btn-spinner", block)

    def test_slow_line(self):
        self.assertIn('id="load-slow"', self.page)
        self.assertIn('"explain.stillWorking"', self.page)
        self.assertIn("}, 20000);", self.page)
        self.assertIn("clearTimeout(slowTimer)", self.page)
        self.assertIn(".load-slow {", self.page)
        self.assertNotIn('html[data-theme="dark"] .load-slow',
                         _read("style.css"))

    def test_hanko_stamp_wired(self):
        self.assertIn('id="summary-hanko"', self.page)
        self.assertIn('id="summary-hanko-num"', self.page)
        self.assertIn('id="summary-hanko-sub"', self.page)
        self.assertIn('classList.add("overdue")', self.page)
        self.assertIn('classList.remove("overdue")', self.page)
        for key in ('"explain.hankoDays"', '"explain.hankoDay"',
                    '"explain.hankoOverdue"'):
            self.assertIn(key, self.page)

    def test_timeout_retry_row(self):
        # A scan timeout shows a LifeBridge message with a Try again
        # button that resends the same photo and typed text.
        for marker in ("function addRetryRow(key, fb, mode)",
                       "addRetryRow();",
                       "It is taking longer than usual.",
                       '"explain.slowDown"',
                       '"explain.tryAgain"',
                       "lastRetryText = pendingQuestion",
                       "pendingQuestion = lastRetryText;",
                       "lb-msg lb-msg-bot lb-retry",
                       "btn btn-prim lb-retry-btn",
                       'querySelectorAll(".lb-retry")',
                       ".lb-retry-btn {"):
            self.assertIn(marker, self.page)

    def test_long_letter_message_translated(self):
        for marker in ('json.code === "long_letter"',
                       '"explain.longLetter"',
                       "This letter is long. Try a photo of just the top"
                       " part, or try again."):
            self.assertIn(marker, self.page)


class MobileChatTest(unittest.TestCase):
    """iPhone chat layout: compact composer, stop mode, auto-scroll."""

    @classmethod
    def setUpClass(cls):
        cls.page = _read("explain.html")

    def test_stop_mode(self):
        for marker in ("function setSendMode(mode)",
                       'setSendMode("stop")',
                       'setSendMode("send")',
                       "STOP_SVG",
                       '<rect x="7" y="7"',
                       'setAttribute("aria-label"',
                       "function stopRequest()",
                       "stopRequested = true",
                       "activeAbort.abort()",
                       "if (requestRunning)",
                       '"explain.stop"',
                       '"explain.stopped"',
                       "Stopped.",
                       "lastRetryAsk",
                       'mode === "ask"',
                       "askQuestion(lastRetryAsk)"):
            self.assertIn(marker, self.page)

    def test_jump_to_latest(self):
        for marker in ('id="jump-latest"',
                       ".jump-latest {",
                       '"explain.jumpLatest"',
                       "Jump to latest",
                       "function scrollThreadToBottom()",
                       "function threadScrolledUp()",
                       "stickToBottom",
                       "> 150",
                       "prefers-reduced-motion",
                       'behavior: reducedMotion() ? "auto" : "smooth"'):
            self.assertIn(marker, self.page)
        self.assertRegex(self.page,
                         r"\.jump-latest\s*\{[^}]*?min-height: 44px;")
        self.assertRegex(self.page,
                         r"\.jump-latest\s*\{[^}]*?position: absolute;")

    def test_keyboard_and_padding_wiring(self):
        for marker in ("window.visualViewport",
                       "innerHeight - vv.height - vv.offsetTop",
                       'addEventListener("resize", placeComposer)',
                       "syncThreadPadding()",
                       "main.style.paddingBottom"):
            self.assertIn(marker, self.page)

    def test_compact_mobile_composer(self):
        self.assertIn("@media (max-width: 759px)", self.page)
        start = self.page.index("@media (max-width: 759px)")
        block = self.page[start:start + 600]
        for marker in (".composer-row", ".composer-note", ".result-note"):
            self.assertIn(marker, block)
        self.assertIn("display: none;", block)
        self.assertIn("display: block;", block)
        self.assertRegex(self.page,
                         r"#ask-input\s*\{[^}]*?font-size: 16px;")
        self.assertIn("max-height: 52px;", self.page)
        self.assertEqual(self.page.count('data-i18n="index.note"'), 2)
        self.assertRegex(
            self.page,
            r"\.chat-composer-bar\s*\{[^}]*?background: var\(--page\);")

    def test_placeholders_are_short(self):
        block = _lang_block(_read("i18n.js"), "en")
        self.assertIn('"explain.askComposer": "Ask about the letter…"',
                      block)
        self.assertIn('"explain.askNeedPhoto": "Add a photo, then Send"',
                      block)

    def test_chip_cleared_on_send(self):
        self.assertIn("function hidePhotoChip()", self.page)
        self.assertIn("hidePhotoChip();", self.page)
        self.assertIn("showPhotoChip(photoInput);", self.page)

    def test_failed_scan_keeps_live_cards(self):
        # The live cards move into each turn: removing an empty turn
        # must rescue them first, or later scans find nothing to fill.
        rescue_at = self.page.index("thread.appendChild(result);")
        remove_at = self.page.index("emptyTurn.remove();")
        self.assertLess(rescue_at, remove_at)
        self.assertIn("thread.appendChild(loading);", self.page)

    def test_still_working_translated(self):
        src = _read("i18n.js")
        for lang in LANGS:
            block = _lang_block(src, lang)
            match = re.search(r'"explain\.stillWorking": "(.*?)"', block)
            self.assertTrue(match, lang)
            value = match.group(1)
            self.assertTrue(value.strip(), lang)
            self.assertNotIn("—", value, lang)
            self.assertNotIn("–", value, lang)


if __name__ == "__main__":
    unittest.main()
