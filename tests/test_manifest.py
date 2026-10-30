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



class IconFilesTest(unittest.TestCase):
    def test_pwa_png_icons_present(self):
        manifest = json.loads(_read("site.webmanifest"))
        by_src = {icon["src"]: icon for icon in manifest["icons"]}
        for src, size in (("icons/icon-192.png", "192x192"),
                          ("icons/icon-512.png", "512x512")):
            self.assertIn(src, by_src)
            self.assertEqual(by_src[src]["sizes"], size)
            self.assertEqual(by_src[src]["type"], "image/png")

    def test_every_icon_file_is_used(self):
        refs = _read("site.webmanifest") + _read("sw.js")
        names = sorted(os.listdir(os.path.join(ROOT, "icons")))
        self.assertTrue(names)
        for name in names:
            self.assertIn("icons/" + name, refs, name)


if __name__ == "__main__":
    unittest.main()
