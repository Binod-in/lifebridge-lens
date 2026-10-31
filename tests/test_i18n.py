"""i18n coverage tests: key parity, HTML key usage, chatbot keys.

Run from the project root:
    python -m unittest tests.test_i18n -v
"""
import glob
import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("en", "ne", "vi", "my")


def _read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


def _lang_key_list(src, lang):
    match = re.search(
        r"\n        " + lang + r": \{(.*?)(?:\n        (?:en|ne|vi|my): \{|\n    \};)",
        src,
        re.S,
    )
    if not match:
        raise AssertionError("language block not found: " + lang)
    return re.findall(r'^            "([^"]+)":', match.group(1), re.M)


class KeyParityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        src = _read("i18n.js")
        cls.lists = {lang: _lang_key_list(src, lang) for lang in LANGS}
        cls.keys = {lang: set(items) for lang, items in cls.lists.items()}

    def test_no_duplicate_keys(self):
        for lang in LANGS:
            items = self.lists[lang]
            dupes = sorted({k for k in items if items.count(k) > 1})
            self.assertEqual(dupes, [], lang + " has duplicate keys")

    def test_all_languages_match_english(self):
        for lang in ("ne", "vi", "my"):
            missing = sorted(self.keys["en"] - self.keys[lang])
            extra = sorted(self.keys[lang] - self.keys["en"])
            self.assertEqual(missing, [], lang + " missing keys")
            self.assertEqual(extra, [], lang + " unknown keys")

    def test_lens_keys_present(self):
        for lang in LANGS:
            for key in ("lens.title", "lens.tagline", "lens.scan",
                        "lens.dates", "lens.money",
                        "explain.saveDate", "explain.dateSaved",
                        "explain.dateExists", "explain.viewDates",
                        "explain.viewDatesPage", "explain.checkDate",
                        "explain.confirmSave", "explain.saveDateLabel",
                        "explain.badDate", "explain.privacyHint",
                        "explain.hAmount", "explain.sample.amount",
                        "explain.tooSlow",
                        "index.hero", "index.exampleLabel",
                        "index.exampleAfter", "index.step1",
                        "index.step2", "index.step3",
                        "explain.daysLeft", "explain.dayLeft",
                        "explain.deadlinePassed", "explain.load1",
                        "explain.load2", "explain.load3",
                        "explain.notShown",
                        "explain.addToCal",
                        "explain.sample.staff",
                        "explain.sample.staffMeaning",
                        "chat.title", "chat.placeholder", "chat.send",
                        "chat.offline", "chat.online", "chat.open",
                        "chat.close",
                        "net.banner", "net.offline",
                        "dates.title", "dates.lead", "dates.dateLabel",
                        "journey.nav.dates",
                        "app.noDates", "app.remove", "app.removeDate",
                        "doc.menu", "doc.mobileNav",
                        "nav.home", "nav.explainShort",
                        "tracker.saveFailed"):
                self.assertIn(key, self.keys[lang], lang)


class HtmlKeyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.en_keys = set(_lang_key_list(_read("i18n.js"), "en"))

    def test_html_keys_exist(self):
        pattern = re.compile(r'data-i18n(?:-html|-placeholder|-aria-label|-alt)?="([^"]+)"')
        unknown = {}
        for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
            with open(path, encoding="utf-8") as f:
                for key in pattern.findall(f.read()):
                    if key not in self.en_keys:
                        unknown.setdefault(os.path.basename(path), []).append(key)
        self.assertEqual(unknown, {})


class ChatbotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src = _read("chatbot.js")
        marker = "var LB_CHAT_KB = "
        start = cls.src.index(marker) + len(marker)
        depth = 0
        in_string = False
        escape = False
        end = None
        for i in range(start, len(cls.src)):
            ch = cls.src[i]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
            elif ch == '"':
                in_string = True
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        cls.kb = json.loads(cls.src[start:end])
        cls.en_keys = set(_lang_key_list(_read("i18n.js"), "en"))

    def test_intents_complete(self):
        self.assertGreaterEqual(len(self.kb), 10)
        ids = [intent["id"] for intent in self.kb]
        self.assertIn("fallback", ids)
        self.assertEqual(len(ids), len(set(ids)), "duplicate intent ids")
        for intent in self.kb:
            for lang in LANGS:
                answer = intent["answers"].get(lang, "")
                self.assertTrue(answer.strip(), intent["id"] + " missing " + lang)
            # No guide pages exist here, so no intent may link to one.
            self.assertEqual(intent.get("links"), [], intent.get("id"))

    def test_chat_keys_exist(self):
        for key in sorted(set(re.findall(r'"((?:chat|net)\.[a-zA-Z]+)"', self.src))):
            self.assertIn(key, self.en_keys, "chatbot.js uses " + key)


class ServiceWorkerTest(unittest.TestCase):
    def test_precache_lists_only_existing_files(self):
        src = _read("sw.js")
        match = re.search(r"const CORE = \[(.*?)\];", src, re.S)
        self.assertTrue(match, "CORE list not found")
        entries = re.findall(r'"([^"]+)"', match.group(1))
        self.assertEqual(set(entries), {
            "/", "offline.html", "index.html", "explain.html",
            "tracker.html", "dates.html", "style.css", "i18n.js",
            "chatbot.js", "site.webmanifest", "icons/document.svg",
            "icons/icon-192.png", "icons/icon-512.png",
        })
        for entry in entries:
            if entry == "/":
                continue
            self.assertTrue(os.path.isfile(os.path.join(ROOT, entry)), entry)



class TaglineTest(unittest.TestCase):
    def test_tagline_in_all_languages(self):
        src = _read("i18n.js")
        self.assertEqual(src.count('"footer.tagline"'), 4)
        for text in ("Understand Japanese notices in your own language.",
                     "जापानी सूचनाहरू आफ्नै भाषामा बुझ्नुहोस्।",
                     "Hiểu các thông báo tiếng Nhật bằng ngôn ngữ của bạn.",
                     "ဂျပန်အသိပေးစာများကို သင့်ဘာသာစကားဖြင့် နားလည်ပါ။"):
            self.assertIn('"footer.tagline": "%s"' % text, src)
        self.assertNotIn("Your everyday guide to living in Japan.", src)


if __name__ == "__main__":
    unittest.main()
