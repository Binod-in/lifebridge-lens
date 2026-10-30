"""PWA manifest tests: valid JSON, icons exist on disk.

Run from the project root:
    python -m unittest tests.test_manifest -v
"""
import json
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


class ManifestTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(_read("site.webmanifest"))

    def test_manifest_has_name_and_icons(self):
        self.assertTrue(self.manifest.get("name"))
        self.assertTrue(self.manifest.get("icons"))

    def test_icons_exist_on_disk(self):
        for icon in self.manifest["icons"]:
            src = icon.get("src", "")
            self.assertTrue(src, "icon without src")
            self.assertTrue(icon.get("sizes"), src)
            self.assertTrue(icon.get("type"), src)
            self.assertTrue(os.path.isfile(os.path.join(ROOT, src)), src)

    def test_manifest_icons_are_precached(self):
        sw = _read("sw.js")
        for icon in self.manifest["icons"]:
            self.assertIn('"%s"' % icon["src"], sw)


if __name__ == "__main__":
    unittest.main()
