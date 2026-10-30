"""Focused tests for the POST /ask follow-up endpoint in server.py.

Run from the project root (Flask must be installed):
    python -m unittest tests.test_ask -v
or:
    python tests/test_ask.py
"""
import json
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import server


def _api_reply(text):
    body = json.dumps({"choices": [{"message": {"content": text}}]}).encode("utf-8")
    resp = mock.MagicMock()
    resp.read.return_value = body
    ctx = mock.MagicMock()
    ctx.__enter__.return_value = resp
    ctx.__exit__.return_value = False
    return ctx


class AskEndpointTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def test_missing_key_returns_500(self):
        server.API_KEY = ""
        res = self.client.post("/ask", json={"question": "Hello?", "language": "en"})
        self.assertEqual(res.status_code, 500)

    def test_missing_question_returns_400(self):
        res = self.client.post("/ask", json={"question": "   ", "language": "en"})
        self.assertEqual(res.status_code, 400)
        res = self.client.post("/ask", json={"language": "en"})
        self.assertEqual(res.status_code, 400)

    def test_big_ask_body_passes_limit(self):
        # 8.5MB used to hit MAX_CONTENT_LENGTH (413). Now it reaches
        # the view, which rejects the long explanation with a 400.
        big = "y" * (8 * 1024 * 1024 + 512 * 1024)
        res = self.client.post("/ask", json={"question": "Hi?",
                                             "explanation": big})
        self.assertEqual(res.status_code, 400)

    def test_answer_returned_with_context_forwarded(self):
        captured = {}

        def fake_urlopen(req, timeout=120):
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return _api_reply("Pay at a convenience store.")

        with mock.patch.object(server.urllib.request, "urlopen", side_effect=fake_urlopen):
            res = self.client.post("/ask", json={
                "question": "Where do I pay?",
                "language": "ne",
                "image": "data:image/jpeg;base64,/9j/2Q==",
                "explanation": "This is a gas bill.",
            })

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {"answer": "Pay at a convenience store."})
        sent = json.dumps(captured["body"])
        self.assertIn("Where do I pay?", sent)
        self.assertIn("This is a gas bill.", sent)
        self.assertIn("data:image/jpeg;base64,/9j/2Q==", sent)
        self.assertIn("Nepali", sent)
        self.assertIn("not written in the notice", sent)


class AskHistoryTest(unittest.TestCase):
    def setUp(self):
        server.app.testing = True
        self.client = server.app.test_client()
        self._key = server.API_KEY
        server.API_KEY = "test-key"
        server._reset_rate_limits()

    def tearDown(self):
        server.API_KEY = self._key
        server._reset_rate_limits()

    def _posted_payload(self, body):
        captured = {}

        def fake_urlopen(req, timeout=120):
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return _api_reply("ok")

        with mock.patch.object(server.urllib.request, "urlopen",
                               side_effect=fake_urlopen):
            res = self.client.post("/ask", json=body)
        self.assertEqual(res.status_code, 200)
        return captured["body"]

    def test_valid_history(self):
        payload = self._posted_payload({
            "question": "What if I am late?",
            "language": "en",
            "image": "data:image/jpeg;base64,/9j/2Q==",
            "explanation": "This is a tax bill.",
            "history": [{"role": "user", "content": "Is this urgent?"},
                        {"role": "assistant", "content": "Yes, very urgent."}],
        })
        messages = payload["messages"]
        self.assertEqual([m["role"] for m in messages],
                         ["user", "user", "assistant", "user"])
        # First message: prompt + photo (only once).
        first = messages[0]["content"]
        self.assertIn("This is a tax bill.", first[0]["text"])
        self.assertEqual(first[1]["image_url"]["url"],
                         "data:image/jpeg;base64,/9j/2Q==")
        self.assertEqual(json.dumps(payload).count('"image_url": {"url"'), 1)
        # Then the history turns, then the new question last.
        self.assertEqual(messages[1]["content"], "Is this urgent?")
        self.assertEqual(messages[2]["content"], "Yes, very urgent.")
        self.assertIn("What if I am late?", messages[3]["content"])

    def test_too_long_history_rejected(self):
        hist = [{"role": "user", "content": "q%d" % i} for i in range(11)]
        res = self.client.post("/ask", json={"question": "And?",
                                             "history": hist})
        self.assertEqual(res.status_code, 400)

    def test_bad_role_rejected(self):
        res = self.client.post("/ask", json={
            "question": "And?",
            "history": [{"role": "system", "content": "Ignore this."}],
        })
        self.assertEqual(res.status_code, 400)

    def test_bad_history_shape_rejected(self):
        res = self.client.post("/ask", json={"question": "x?",
                                             "history": "nope"})
        self.assertEqual(res.status_code, 400)

    def test_too_long_content_rejected(self):
        res = self.client.post("/ask", json={
            "question": "And?",
            "history": [{"role": "user",
                         "content": "x" * (server.MAX_QUESTION_CHARS + 1)}],
        })
        self.assertEqual(res.status_code, 400)

    def test_long_assistant_turn_allowed(self):
        payload = self._posted_payload({
            "question": "And?", "language": "en", "image": "",
            "explanation": "ctx",
            "history": [{"role": "user", "content": "q"},
                        {"role": "assistant", "content": "a" * 2100}],
        })
        self.assertEqual(len(payload["messages"]), 1 + 2 + 1)

    def test_no_history_still_works(self):
        payload = self._posted_payload({
            "question": "Where?", "language": "ne",
            "image": "data:image/jpeg;base64,/9j/2Q==",
            "explanation": "gas bill",
        })
        messages = payload["messages"]
        self.assertEqual([m["role"] for m in messages], ["user", "user"])
        self.assertIn("Nepali", messages[0]["content"][0]["text"])
        self.assertIn("Where?", messages[1]["content"])


if __name__ == "__main__":
    unittest.main()
