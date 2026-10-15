"""Environment-based runtime configuration."""

from dataclasses import dataclass
import os


class ConfigurationError(ValueError):
    """Raised when required model configuration is absent or invalid."""


@dataclass(frozen=True)
class Settings:
    base_url: str
    model: str
    api_key: str | None = None
    timeout_seconds: float = 60.0

    @classmethod
    def from_env(cls) -> "Settings":
        base_url = os.environ.get("JARVIS_BASE_URL", "").strip().rstrip("/")
        model = os.environ.get("JARVIS_MODEL", "").strip()
        if not base_url:
            raise ConfigurationError(
                "JARVIS_BASE_URL is not set. Configure an OpenAI-compatible "
                "endpoint, such as http://localhost:11434/v1."
            )
        if not model:
            raise ConfigurationError(
                "JARVIS_MODEL is not set. Set it to the model name served by "
                "your configured endpoint."
            )
        if not base_url.startswith(("http://", "https://")):
            raise ConfigurationError("JARVIS_BASE_URL must use http:// or https://.")
        api_key = (os.environ.get("JARVIS_API_KEY") or "").strip() or None
        return cls(
            base_url=base_url,
            model=model,
            api_key=api_key,
        )
