"""JavaScript syntax tests: every page and script file must parse.

Needs node (plain `node` or the Playwright-bundled one). Skips
honestly when no node is available.

Run from the project root:
    python -m unittest tests.test_jssyntax -v
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ("index.html", "explain.html", "dates.html", "tracker.html",
         "offline.html")
SCRIPTS = ("i18n.js", "chatbot.js", "sw.js")


def _find_node():
    found = shutil.which("node")
    if found:
        return found
    try:
        import playwright
    except ImportError:
        return None
    folder = os.path.join(os.path.dirname(playwright.__file__), "driver")
    for name in ("node.exe", "node"):
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            return path
    return None


NODE = _find_node()


def _inline_scripts(page):
    with open(os.path.join(ROOT, page), encoding="utf-8") as f:
        text = f.read()
    return re.findall(r"<script(?![^>]*src=)[^>]*>(.*?)</script>", text, re.S)


@unittest.skipUnless(NODE, "node not available")
class JsSyntaxTest(unittest.TestCase):
    def _check(self, code, label):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as f:
            f.write(code)
            path = f.name
        try:
            proc = subprocess.run([NODE, "--check", path],
                                  capture_output=True, text=True, timeout=60)
        finally:
            os.unlink(path)
        self.assertEqual(proc.returncode, 0, label + ":\n" + proc.stderr)

    def test_inline_scripts_parse(self):
        for page in PAGES:
            blocks = _inline_scripts(page)
            self.assertTrue(blocks, page)
            for i, code in enumerate(blocks):
                self._check(code, "%s block %d" % (page, i))

    def test_script_files_parse(self):
        for name in SCRIPTS:
            with open(os.path.join(ROOT, name), encoding="utf-8") as f:
                self._check(f.read(), name)


def _split_steps_source():
    """Extract STEP consts and helpers plus splitSteps (one block)."""
    with open(os.path.join(ROOT, "explain.html"), encoding="utf-8") as f:
        text = f.read()
    start = text.index("const STEP_NUM =")
    fn_at = text.index("function splitSteps(text)", start)
    i = text.index("{", fn_at)
    depth = 0
    in_str = None
    while True:
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 1
            elif ch == in_str:
                in_str = None
        elif ch in ("'", '"'):
            in_str = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    return text[start:i + 1]


class StepsSplitWiredTest(unittest.TestCase):
    def test_fill_card_uses_split_steps(self):
        with open(os.path.join(ROOT, "explain.html"), encoding="utf-8") as f:
            text = f.read()
        self.assertIn("const STEP_MARK =", text)
        self.assertIn("function splitSteps(text)", text)
        self.assertIn("for (const step of splitSteps(text))", text)


@unittest.skipUnless(NODE, "node not available")
class StepsSplitBehaviorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cases = [
            # Real Nepali answer: one line, Devanagari numbers.
            "१. 令和8年... बाटो बन्द हुन्छ। २. सो दिन अर्को बाटो "
            "प्रयोग गर्नुहोस्। ३. पानी परेमा मिति सर्न सक्छ।",
            "1. Read the letter. 2. Pay at the bank.",
            "१. पहिलो। २) दोस्रो। ३.) तेस्रो",
            "၁. first။ ၂. second",
            "①first②second③third",
            "１． first。 ２． second",
            "令和8年X",
            "Costs 3.5 percent",
            "No markers here",
            "1. a\n2. b",
            "Reiwa 8 (2026) नोभेम्बर २५ भित्र तिर्नुहोस्।",
            "令和8年（2026）11月",
            "21. foo",
            "(A. 2. x)",
            "(①)",
        ]
        code = (_split_steps_source()
                + "\nconst CASES = " + json.dumps(cases) + ";"
                + "\nconsole.log(JSON.stringify(CASES.map(splitSteps)));")
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                         encoding="utf-8") as f:
            f.write(code)
            path = f.name
        try:
            proc = subprocess.run([NODE, path], capture_output=True,
                                  text=True, encoding="utf-8", timeout=60,
                                  errors="strict")
        finally:
            os.unlink(path)
        assert proc.returncode == 0, proc.stderr
        cls.got = json.loads(proc.stdout)

    def test_nepali_answer_is_three_steps(self):
        steps = self.got[0]
        self.assertEqual(len(steps), 3)
        self.assertTrue(steps[0].startswith("令和8年"), steps)
        self.assertIn("अर्को बाटो", steps[1])
        self.assertIn("पानी परेमा", steps[2])

    def test_each_numeral_system_splits(self):
        self.assertEqual(len(self.got[1]), 2)
        self.assertEqual(len(self.got[2]), 3)
        self.assertEqual(len(self.got[3]), 2)
        self.assertEqual(len(self.got[4]), 3)
        self.assertEqual(len(self.got[5]), 2)
        self.assertEqual(self.got[4], ["first", "second", "third"])

    def test_years_decimals_and_plain_text_do_not_split(self):
        self.assertEqual(self.got[6], ["令和8年X"])
        self.assertEqual(self.got[7], ["Costs 3.5 percent"])
        self.assertEqual(self.got[8], ["No markers here"])
        self.assertEqual(self.got[9], ["a", "b"])

    def test_years_brackets_and_big_numbers_do_not_split(self):
        self.assertEqual(self.got[10],
                         ["Reiwa 8 (2026) नोभेम्बर २५ भित्र तिर्नुहोस्।"])
        self.assertEqual(self.got[11], ["令和8年（2026）11月"])
        self.assertEqual(self.got[12], ["21. foo"])
        self.assertEqual(self.got[13], ["(A. 2. x)"])
        self.assertEqual(self.got[14], ["(①)"])


if __name__ == "__main__":
    unittest.main()
