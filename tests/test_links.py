"""Link tests: every page links only to files that exist in this repo.

Run from the project root:
    python -m unittest tests.test_links -v
"""
import glob
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Served by Flask, so no file exists on disk.
VIRTUAL = {"lb-config.js"}


def _read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


class PageLinkTest(unittest.TestCase):
    def test_internal_links_resolve(self):
        for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
            with open(path, encoding="utf-8") as f:
                html = f.read()
            urls = re.findall(r'(?:href|src)="([^"]+)"', html)
            self.assertTrue(urls, os.path.basename(path))
            for url in urls:
                if url.startswith(("http://", "https://", "data:",
                                   "mailto:")):
                    continue
                if url.startswith("#"):
                    continue
                clean = url.split("#")[0].split("?")[0]
                if not clean or clean in VIRTUAL:
                    continue
                where = "%s -> %s" % (os.path.basename(path), clean)
                self.assertTrue(os.path.isfile(os.path.join(ROOT, clean)),
                                where)

    def test_footer_explore_links_dates(self):
        for path in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
            with open(path, encoding="utf-8") as f:
                html = f.read()
            navs = re.findall(r'<nav[^>]*class="footer-links"[^>]*>(.*?)</nav>',
                              html, re.S)
            if navs:
                self.assertIn("dates.html", navs[0],
                              os.path.basename(path))

    def test_explain_dates_button(self):
        html = _read("explain.html")
        self.assertEqual(html.count("explain.viewDatesPage"), 1)
        self.assertIn('id="view-dates-btn"', html)
        scan_at = html.index('id="explain-btn"')
        link_at = html.index("explain.viewDatesPage")
        form_end = html.index("</form>", scan_at)
        self.assertLess(scan_at, link_at)
        self.assertLess(link_at, form_end)

    def test_chatbot_has_no_page_links(self):
        src = _read("chatbot.js")
        arrays = re.findall(r'"links": \[(.*?)\]', src)
        self.assertTrue(arrays)
        for found in arrays:
            self.assertEqual(found.strip(), "")


if __name__ == "__main__":
    unittest.main()
