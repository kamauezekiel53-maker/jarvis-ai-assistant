"""Command-line interaction loop."""

import argparse
import sys

from jarvis_ai.config import ConfigurationError, Settings
from jarvis_ai.providers.openai_compatible import (
    OpenAICompatibleProvider,
    ProviderError,
)
from jarvis_ai.runtime import Message


def run_chat() -> int:
    try:
        provider = OpenAICompatibleProvider(Settings.from_env())
    except ConfigurationError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    history: list[Message] = []
    print("Jarvis CLI. Type /exit to quit.")
    while True:
        try:
            prompt = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if prompt.lower() in {"/exit", "/quit"}:
            return 0
        if not prompt:
            continue

        history.append(Message("user", prompt))
        try:
            response = provider.complete(history)
        except ProviderError as exc:
            history.pop()
            print(f"Model error: {exc}", file=sys.stderr)
            continue
        history.append(Message("assistant", response))
        print(f"Jarvis> {response}")


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="jarvis",
        description="Start a text conversation with a configured model endpoint.",
    )
    parser.parse_args()
    return run_chat()


if __name__ == "__main__":
    raise SystemExit(main())
