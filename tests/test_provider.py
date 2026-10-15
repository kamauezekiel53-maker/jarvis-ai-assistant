import json
import unittest
from unittest.mock import patch
from urllib.error import URLError

from jarvis_ai.config import Settings
from jarvis_ai.providers.openai_compatible import (
    OpenAICompatibleProvider,
    ProviderError,
)
from jarvis_ai.runtime import Message


class FakeResponse:
    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self):
        return self.body


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.provider = OpenAICompatibleProvider(
            Settings("http://localhost:1234/v1", "test-model", "secret")
        )

    @patch("jarvis_ai.providers.openai_compatible.urlopen")
    def test_sends_chat_request_and_returns_assistant_content(self, open_url):
        open_url.return_value = FakeResponse(
            json.dumps(
                {"choices": [{"message": {"content": " Hello there. "}}]}
            ).encode()
        )
        result = self.provider.complete([Message("user", "Hi")])
        self.assertEqual(result, "Hello there.")
        request = open_url.call_args.args[0]
        self.assertEqual(
            request.full_url, "http://localhost:1234/v1/chat/completions"
        )
        self.assertEqual(request.get_header("Authorization"), "Bearer secret")
        body = json.loads(request.data.decode())
        self.assertEqual(body["model"], "test-model")
        self.assertEqual(body["messages"], [{"role": "user", "content": "Hi"}])

    @patch("jarvis_ai.providers.openai_compatible.urlopen")
    def test_reports_network_failure(self, open_url):
        open_url.side_effect = URLError("connection refused")
        with self.assertRaisesRegex(ProviderError, "Could not reach model endpoint"):
            self.provider.complete([Message("user", "Hi")])

    @patch("jarvis_ai.providers.openai_compatible.urlopen")
    def test_rejects_invalid_response_shape(self, open_url):
        open_url.return_value = FakeResponse(b'{"choices":[]}')
        with self.assertRaisesRegex(ProviderError, "missing choices"):
            self.provider.complete([Message("user", "Hi")])

    @patch("jarvis_ai.providers.openai_compatible.urlopen")
    def test_reports_invalid_json(self, open_url):
        open_url.return_value = FakeResponse(b"not-json")
        with self.assertRaisesRegex(ProviderError, "invalid JSON"):
            self.provider.complete([Message("user", "Hi")])


if __name__ == "__main__":
    unittest.main()
