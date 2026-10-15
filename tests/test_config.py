import unittest
from unittest.mock import patch

from jarvis_ai.config import ConfigurationError, Settings


class SettingsTests(unittest.TestCase):
    def test_requires_endpoint_and_model(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaisesRegex(ConfigurationError, "JARVIS_BASE_URL"):
                Settings.from_env()

    def test_requires_model(self):
        with patch.dict(
            "os.environ", {"JARVIS_BASE_URL": "http://localhost:11434/v1"}, clear=True
        ):
            with self.assertRaisesRegex(ConfigurationError, "JARVIS_MODEL"):
                Settings.from_env()

    def test_reads_configuration_and_optional_key(self):
        values = {
            "JARVIS_BASE_URL": "http://localhost:11434/v1/",
            "JARVIS_MODEL": "qwen2.5",
            "JARVIS_API_KEY": "local-secret",
        }
        with patch.dict("os.environ", values, clear=True):
            settings = Settings.from_env()
        self.assertEqual(settings.base_url, "http://localhost:11434/v1")
        self.assertEqual(settings.model, "qwen2.5")
        self.assertEqual(settings.api_key, "local-secret")

    def test_rejects_unsupported_endpoint_scheme(self):
        values = {"JARVIS_BASE_URL": "file:///tmp", "JARVIS_MODEL": "test"}
        with patch.dict("os.environ", values, clear=True):
            with self.assertRaisesRegex(ConfigurationError, "http:// or https://"):
                Settings.from_env()


if __name__ == "__main__":
    unittest.main()
