"""README tests: no merge markers, single project heading.

Run from the project root:
    python -m unittest tests.test_readme -v
"""
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


class ReadmeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = _read("README.md")

    def test_no_merge_conflict_markers(self):
        for marker in ("<<<<<<<", "=======", ">>>>>>>"):
            self.assertNotIn(marker, self.readme)

    def test_single_lens_heading(self):
        self.assertIn("# LifeBridge Lens", self.readme)
        self.assertNotIn("# lifebridge-lens", self.readme)


if __name__ == "__main__":
    unittest.main()
