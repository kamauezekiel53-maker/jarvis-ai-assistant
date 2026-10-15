"""Provider for OpenAI-compatible chat-completions endpoints."""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from typing import Sequence

from jarvis_ai.config import Settings
from jarvis_ai.runtime import Message


class ProviderError(RuntimeError):
    """Raised when a model endpoint cannot return a valid completion."""


class OpenAICompatibleProvider:
    def __init__(self, settings: Settings):
        self._settings = settings

    def complete(self, messages: Sequence[Message]) -> str:
        payload = json.dumps(
            {
                "model": self._settings.model,
                "messages": [
                    {"role": message.role, "content": message.content}
                    for message in messages
                ],
            }
        ).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self._settings.api_key:
            headers["Authorization"] = f"Bearer {self._settings.api_key}"
        request = Request(
            f"{self._settings.base_url}/chat/completions",
            data=payload,
            headers=headers,
            method="POST",
        )
        try:
            with urlopen(request, timeout=self._settings.timeout_seconds) as response:
                result = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace").strip()
            suffix = f": {detail}" if detail else ""
            raise ProviderError(
                f"Model endpoint returned HTTP {exc.code}{suffix}"
            ) from exc
        except URLError as exc:
            raise ProviderError(f"Could not reach model endpoint: {exc.reason}") from exc
        except (TimeoutError, OSError) as exc:
            raise ProviderError(f"Model request failed: {exc}") from exc
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ProviderError("Model endpoint returned invalid JSON.") from exc

        try:
            content = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(
                "Model endpoint response is missing choices[0].message.content."
            ) from exc
        if not isinstance(content, str) or not content.strip():
            raise ProviderError("Model endpoint returned an empty assistant response.")
        return content.strip()
