"""Phase 6 tests: chatbot knowledge expansion and sources.

Seven new intents cover transport, payments, emergencies, and jobs.
Verified answers name a source, the rest are labelled general
guidance, and new keywords never steal old pinned queries.

Run from the project root:
    python -m unittest tests.test_phase6 -v
"""
import json
import os
import re
import unicodedata
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("en", "ne", "vi", "my")
NEW_IDS = ("train-tickets", "commuter-pass", "conbini-pay", "atm-use",
           "lost-passport", "job-resume", "job-interview")
VERIFIED_IDS = ("train-tickets", "commuter-pass", "lost-passport")
PUNCT = ".,!?;:()[]\"「」、。！？・"


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


def load_kb():
    src = _read("chatbot.js")
    start = src.index("var LB_CHAT_KB = ") + len("var LB_CHAT_KB = ")
    end = src.index("var LB_CHAT_SUGGEST", start)
    raw = src[start:end].strip()
    if raw.endswith(";"):
        raw = raw[:-1]
    return json.loads(raw)


def normalize(text):
    value = unicodedata.normalize("NFKC", str(text or ""))
    chars = []
    for ch in value.lower():
        if ch in PUNCT:
            chars.append(" ")
        else:
            chars.append(ch)
    return " " + re.sub(r"\s+", " ", "".join(chars)).strip() + " "


def find_best(kb, text):
    text = normalize(text)
    best = None
    best_score = 0
    for intent in kb:
        if not intent or intent.get("id") == "fallback":
            continue
        score = 0
        groups = intent.get("keys", {})
        for lang, words in groups.items():
            whole_words = lang in ("en", "vi")
            for word in words or []:
                word = normalize(word).strip()
                if not word:
                    continue
                if whole_words:
                    if " " + word + " " in text:
                        score += 1
                elif word in text:
                    score += 1
        if score > best_score:
            best_score = score
            best = intent
    if best is None:
        for intent in kb:
            if intent and intent.get("id") == "fallback":
                return intent
    return best


class Phase6IntentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = load_kb()
        cls.by_id = {intent["id"]: intent for intent in cls.kb}

    def _intent_id(self, text):
        return find_best(self.kb, text)["id"]

    def test_new_intents_present(self):
        for intent_id in NEW_IDS:
            self.assertIn(intent_id, self.by_id)

    def test_verified_intents_name_a_source(self):
        for intent_id in VERIFIED_IDS:
            intent = self.by_id[intent_id]
            self.assertIs(intent.get("verified"), True, intent_id)
            self.assertTrue((intent.get("source") or "").strip(), intent_id)

    def test_general_intents_are_not_verified(self):
        for intent_id in set(NEW_IDS) - set(VERIFIED_IDS):
            intent = self.by_id[intent_id]
            self.assertIsNot(intent.get("verified"), True, intent_id)

    def test_new_queries_resolve(self):
        cases = {
            "how do I buy a train ticket": "train-tickets",
            "train ticket": "train-tickets",
            "commuter pass": "commuter-pass",
            "pay bill at conbini": "conbini-pay",
            "withdraw cash atm": "atm-use",
            "lost passport": "lost-passport",
            "rirekisho": "job-resume",
            "resume": "job-resume",
            "job interview": "job-interview",
            "interview": "job-interview",
        }
        for text, intent_id in cases.items():
            self.assertEqual(self._intent_id(text), intent_id, text)

    def test_old_queries_not_stolen(self):
        cases = {
            "I lost my phone": "lost-phone",
            "I lost my residence card": "lost-residence",
            "how to pay tax": "tax",
            "my account was hacked": "fallback",
            "I lost my train pass": "lost-general",
            "banking app": "bank",
            "apartment rent": "housing",
            "earthquake": "earthquake",
        }
        for text, intent_id in cases.items():
            self.assertEqual(self._intent_id(text), intent_id, text)


class Phase6RendererTest(unittest.TestCase):
    def test_source_line_rendered(self):
        src = _read("chatbot.js")
        self.assertIn("function addSource(intent)", src)
        self.assertIn("chat-source", src)
        self.assertIn('"chat.source"', src)
        self.assertIn('"chat.general"', src)
        self.assertIn("addSource(intent)", src)

    def test_source_styles(self):
        css = _read("style.css")
        self.assertIn(".chat-source {", css)
        self.assertIn('html[data-theme="dark"] .chat-source', css)


class Phase6TranslationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        src = _read("i18n.js")
        cls.blocks = {lang: _lang_block(src, lang) for lang in LANGS}

    def test_new_keys_in_all_four_languages(self):
        for key in ("chat.source", "chat.general"):
            for lang in LANGS:
                match = re.search(r'"%s": "(.*?)"' % re.escape(key),
                                  self.blocks[lang])
                self.assertTrue(match, "%s missing in %s" % (key, lang))
                self.assertTrue(match.group(1).strip(),
                                "%s is empty in %s" % (key, lang))


if __name__ == "__main__":
    unittest.main()
