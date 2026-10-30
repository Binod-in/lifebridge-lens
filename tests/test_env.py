"""Environment loading tests: tiny .env loader in server.py.

Run from the project root:
    python -m unittest tests.test_env -v
"""
import os
import tempfile
import unittest

import server


class DotenvLoaderTest(unittest.TestCase):
    def test_loads_values_and_never_overrides(self):
        fd, path = tempfile.mkstemp(suffix=".env")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write("# comment\n\nLB_TEST_A=hello\n"
                        "LB_TEST_B=\"quoted value\"\nLB_TEST_C='single'\n")
            os.environ["LB_TEST_B"] = "already-set"
            try:
                server._load_dotenv(path)
                self.assertEqual(os.environ.get("LB_TEST_A"), "hello")
                self.assertEqual(os.environ.get("LB_TEST_B"), "already-set")
                self.assertEqual(os.environ.get("LB_TEST_C"), "single")
            finally:
                os.environ.pop("LB_TEST_A", None)
                os.environ.pop("LB_TEST_B", None)
                os.environ.pop("LB_TEST_C", None)
        finally:
            os.remove(path)

    def test_missing_file_is_silent(self):
        missing = os.path.join(tempfile.gettempdir(), "lb-no-such-file.env")
        if os.path.exists(missing):
            os.remove(missing)
        server._load_dotenv(missing)


if __name__ == "__main__":
    unittest.main()
