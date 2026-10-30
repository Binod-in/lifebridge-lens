"""Chatbot intent tests: reported inputs must resolve to the right intent.

The matcher below mirrors findBest() in chatbot.js: whole-word matching
for en/vi keywords, substring matching for ne/my/ja. This keeps the KB
honest without running JavaScript.

Run from the project root:
    python -m unittest tests.test_chatbot -v
"""
import json
import os
import re
import unicodedata
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PUNCT = ".,!?;:()[]\"「」、。！？・"


def normalize(text):
    value = unicodedata.normalize("NFKC", str(text or ""))
    chars = []
    for ch in value.lower():
        if ch in PUNCT:
            chars.append(" ")
        else:
            chars.append(ch)
    return " " + re.sub(r"\s+", " ", "".join(chars)).strip() + " "


def load_kb():
    with open(os.path.join(ROOT, "chatbot.js"), encoding="utf-8") as f:
        src = f.read()
    start = src.index("var LB_CHAT_KB = ") + len("var LB_CHAT_KB = ")
    end = src.index("var LB_CHAT_SUGGEST", start)
    raw = src[start:end].strip()
    if raw.endswith(";"):
        raw = raw[:-1]
    return json.loads(raw)


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


class ChatbotIntentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = load_kb()

    def _intent_id(self, text):
        return find_best(self.kb, text)["id"]

    def test_lost_phone(self):
        self.assertEqual(self._intent_id("I lost my phone"), "lost-phone")

    def test_lost_residence_card(self):
        self.assertEqual(self._intent_id("I lost my residence card"),
                         "lost-residence")

    def test_garbage_day(self):
        self.assertEqual(self._intent_id("garbage day"), "garbage")

    def test_pay_tax(self):
        self.assertEqual(self._intent_id("how to pay tax"), "tax")

    def test_visa_renewal(self):
        self.assertEqual(self._intent_id("visa renewal"), "visa")

    def test_lost_phone_nepali(self):
        self.assertEqual(self._intent_id("मेरो फोन हरायो"), "lost-phone")

    def test_hacked_account_is_not_bank(self):
        self.assertEqual(self._intent_id("my account was hacked"), "fallback")

    def test_lost_train_pass_is_not_lost_residence(self):
        self.assertEqual(self._intent_id("I lost my train pass"),
                         "lost-general")

    def test_renew_residence_card(self):
        self.assertEqual(self._intent_id("I want to renew my residence card"),
                         "visa")

    def test_banking_app(self):
        self.assertEqual(self._intent_id("banking app"), "bank")

    def test_salary_luong_is_bank(self):
        self.assertEqual(self._intent_id("luong"), "bank")

    def test_get_residence_card_is_not_lost(self):
        self.assertNotEqual(self._intent_id("Where do I get a residence card"),
                            "lost-residence")

    def test_neutral_residence_card_nepali_is_address(self):
        self.assertEqual(self._intent_id("निवास कार्ड भनेको के हो?"),
                         "address")

    def test_neutral_residence_card_vietnamese_is_address(self):
        self.assertEqual(self._intent_id("thẻ cư trú là gì?"),
                         "address")

    def test_neutral_residence_card_burmese_is_address(self):
        self.assertEqual(self._intent_id("နေထိုင်ခွင့်ကတ် ဆိုတာ ဘာလဲ?"),
                         "address")

    def test_lost_residence_card_nepali(self):
        self.assertEqual(self._intent_id("मेरो निवास कार्ड हरायो"),
                         "lost-residence")

    def test_lost_residence_card_vietnamese(self):
        self.assertEqual(self._intent_id("tôi bị mất thẻ cư trú"),
                         "lost-residence")

    def test_lost_residence_card_burmese(self):
        self.assertEqual(self._intent_id("ကျွန်တော့် နေထိုင်ခွင့်ကတ် ပျောက်သွားတယ်"),
                         "lost-residence")

    def test_visa_answer_mentions_renewal_fee(self):
        visa = next(i for i in self.kb if i.get("id") == "visa")
        for lang in ("en", "ne", "vi", "my"):
            answer = visa["answers"][lang]
            self.assertIn("ISA", answer, lang)
            self.assertIn("33", answer, lang)

    def test_apartment_rent_is_housing(self):
        self.assertEqual(self._intent_id("apartment rent"), "housing")

    def test_earthquake_is_earthquake(self):
        self.assertEqual(self._intent_id("earthquake"), "earthquake")



class AnswerWordingTest(unittest.TestCase):
    """Greeting and fallback describe offline answers, not saved guides."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(ROOT, "chatbot.js"), encoding="utf-8") as f:
            cls.src = f.read()
        cls.kb = {intent["id"]: intent for intent in load_kb()}

    def test_no_saved_guides_wording(self):
        for old in ("from the saved guides",
                    "सेभ गरिएका गाइडबाट",
                    "hướng dẫn đã lưu",
                    "သိမ်းထားသော လမ်းညွှန်များမှ",
                    "Details are in the Emergency guide.",
                    "विवरण Emergency गाइडमा छ।",
                    "Chi tiết trong hướng dẫn Emergency.",
                    "အသေးစိတ်ကို Emergency လမ်းညွှန်တွင် ကြည့်ပါ။"):
            self.assertNotIn(old, self.src)

    def test_offline_answers_in_all_languages(self):
        new = {"en": "I answer common questions, even offline",
               "ne": "सामान्य प्रश्नहरूको जवाफ दिन्छु, अफलाइन पनि",
               "vi": "Tôi trả lời các câu hỏi thường gặp, kể cả khi ngoại tuyến",
               "my": "အမေးများသော မေးခွန်းများကို ဖြေပေးပါတယ်၊ အော့ဖ်လိုင်းလည်း ရပါတယ်"}
        for intent_id in ("greeting", "fallback"):
            answers = self.kb[intent_id]["answers"]
            for lang, text in new.items():
                self.assertIn(text, answers[lang], intent_id + " " + lang)


if __name__ == "__main__":
    unittest.main()
