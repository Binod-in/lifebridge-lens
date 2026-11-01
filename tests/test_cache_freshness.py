"""Cache freshness tests: new versions must reach browsers.

Two cooperating fixes stop old JS/CSS from sticking around: the
service worker install bypasses the HTTP cache when precaching, and
the server sends versioned text assets (.js, .css, .webmanifest)
with "no-cache" so browsers revalidate. Only images keep a long
max-age.

Run from the project root:
    python -m unittest tests.test_cache_freshness -v
"""
import os
import unittest

import server

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REVALIDATED = ("/index.html", "/style.css", "/i18n.js",
               "/chatbot.js", "/site.webmanifest")
LONG_LIVED = ("/icons/document.svg", "/icons/icon-192.png",
              "/icons/icon-512.png")


def _read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


class SwInstallReloadTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sw = _read("sw.js")

    def test_install_bypasses_http_cache(self):
        # cache: "reload" forces a network fetch so a stale HTTP
        # cache entry can never fill the precache.
        self.assertIn(
            "cache.addAll(CORE.map(function (url) { "
            'return new Request(url, { cache: "reload" }); }))',
            self.sw)

    def test_install_does_not_precache_stale_entries(self):
        self.assertNotIn("cache.addAll(CORE)", self.sw)


class ServerCacheHeadersTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()

    def test_text_assets_revalidate(self):
        for path in REVALIDATED:
            res = self.client.get(path)
            try:
                self.assertEqual(res.status_code, 200, path)
                control = res.headers.get("Cache-Control", "")
                self.assertIn("no-cache", control, path)
                self.assertNotIn("max-age", control, path)
            finally:
                res.close()

    def test_images_keep_long_max_age(self):
        for path in LONG_LIVED:
            res = self.client.get(path)
            try:
                self.assertEqual(res.status_code, 200, path)
                self.assertIn("max-age=86400",
                              res.headers.get("Cache-Control", ""), path)
            finally:
                res.close()


if __name__ == "__main__":
    unittest.main()
