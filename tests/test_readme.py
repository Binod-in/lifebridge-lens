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

    def test_accuracy_and_speed_results(self):
        for marker in (
                "## Accuracy check",
                "| Water and sewer bill (Shiki City) | Real letter | Yes | Yes | Nov 16, 2026 / 2,304 yen |",
                '| Road repair notice | Real letter | N/A (information only) | N/A | Date and time correct, said "not a payment" |',
                "| National Health Insurance payment slip | Synthetic sample | Yes | Yes | Did not confuse the barcode expiry date with the deadline |",
                "| National Pension exemption rejected | Synthetic sample | N/A | N/A | Said the exemption was rejected, payment is still needed, and the 3-month appeal window |",
                "| Water bill auto-debit failed | Synthetic sample | Yes | Yes | Nov 25, 2026 / 3,520 yen |",
                "## Speed (real iPhone tests on home Wi-Fi)",
                "- Scan: about 11–27 s (most 11–21 s). Before tuning reasoning_effort: 28–37 s.",
                "- Follow-up answer: 6–8 s. Before: about 19 s.",
                "never a real letter"):
            self.assertIn(marker, self.readme)

    def test_links_screenshots_and_length(self):
        self.assertIn("Demo video: TODO", self.readme)
        self.assertIn("Live demo: TODO", self.readme)
        self.assertNotIn("coming soon", self.readme)
        for shot in ("lens-sample-390-light.png",
                     "lens-sample-390-dark.png",
                     "lens-sample-1280-light.png"):
            self.assertIn(shot, self.readme)
            path = os.path.join(ROOT, "deliverables", "screenshots", shot)
            self.assertTrue(os.path.isfile(path), shot)
        lines = self.readme.splitlines()
        self.assertGreaterEqual(len(lines), 120)
        self.assertLessEqual(len(lines), 160)


if __name__ == "__main__":
    unittest.main()
