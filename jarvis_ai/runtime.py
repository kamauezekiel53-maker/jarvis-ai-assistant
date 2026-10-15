"""Small provider boundary for assistant runtimes and future model backends."""

from dataclasses import dataclass
from typing import Protocol, Sequence


@dataclass(frozen=True)
class Message:
    role: str
    content: str


class ModelProvider(Protocol):
    def complete(self, messages: Sequence[Message]) -> str:
        """Return one assistant response for the supplied conversation."""
