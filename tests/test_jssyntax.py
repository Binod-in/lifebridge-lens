"""JavaScript syntax tests: every page and script file must parse.

Needs node (plain `node` or the Playwright-bundled one). Skips
honestly when no node is available.

Run from the project root:
    python -m unittest tests.test_jssyntax -v
"""
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


if __name__ == "__main__":
    unittest.main()
