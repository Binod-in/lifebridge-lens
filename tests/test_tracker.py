"""Static checks for tracker.html storage-failure rollback."""
import unittest
from pathlib import Path


TRACKER = Path(__file__).resolve().parent.parent / "tracker.html"


class TestTrackerRollback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = TRACKER.read_text(encoding="utf-8")

    def test_entry_delete_rolls_back(self):
        self.assertIn("const prevEntries = entries;", self.page)
        self.assertIn("entries = prevEntries;", self.page)

    def test_goal_delete_rolls_back(self):
        self.assertIn("const prevGoals = goals;", self.page)
        self.assertIn("goals = prevGoals;", self.page)


if __name__ == "__main__":
    unittest.main()
