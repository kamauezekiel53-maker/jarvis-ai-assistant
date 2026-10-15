# Jarvis AI Assistant

Jarvis is a Windows-first, cross-platform assistant foundation. Phase 1 provides
a real text CLI backed by any OpenAI-compatible chat-completions endpoint,
including a local endpoint such as Ollama. It has no built-in model, shell
runner, repository access, or hidden tool execution. This is a foundation, not
a claim that the planned features below are already available.

## Requirements

- Python 3.10 or newer
- An OpenAI-compatible server and a model served by that endpoint

No runtime package dependencies are required. Credentials are read only from
environment variables; do not put API keys in source files or commit them.

## Windows setup

In PowerShell, from the repository directory:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
$env:JARVIS_BASE_URL = "http://localhost:11434/v1"
$env:JARVIS_MODEL = "your-model-name"
jarvis
```

Alternatively, run `python -m jarvis_ai` instead of installing the `jarvis`
command. Set `JARVIS_API_KEY` only if your endpoint requires it. For example,
cloud endpoints may require a provider-issued key; configure their compatible
base URL and model name as well. Keys and endpoint errors are not written to
configuration files by Jarvis.

Type a message to chat. Enter `/exit` or `/quit` to end the session. The CLI
keeps conversation history in memory for that process only. If endpoint or
model configuration is missing, Jarvis reports the required variable and exits
without making a network request. Connection, HTTP, and malformed response
errors are reported explicitly.

## Development and tests

```powershell
python -m unittest discover -s tests -v
```

## Roadmap

Features below are planned unless explicitly listed under Phase 1. No
prompt/safeguard bypass behavior is planned; cybersecurity-adjacent features
will be limited to authorized, legitimate uses.

- **Phase 1 — Runtime foundation (implemented):** Windows-usable CLI; minimal
  provider boundary; OpenAI-compatible chat endpoint; environment-based
  configuration and focused tests.
- **Phase 2 — Coding-agent loop and repository context (planned):** bounded
  repository indexing/context, task execution loop, and verification.
- **Phase 3 — Secure execution (planned):** explicit per-action approvals,
  sandboxing, worktrees, checkpoints, and a verifier. No arbitrary shell or
  OS-changing actions without explicit controls.
- **Phase 4 — Model routing and memory (planned):** local/cloud model routing,
  persistent memory, and semantic retrieval.
- **Phase 5 — Extensions and agents (planned):** skills, connectors, plugins,
  MCP, managed agents, specialized agents, and routines.
- **Phase 6 — Multimodal and interface (planned):** voice, screen and other
  multimodal input; web dashboard and 3D agent view.
- **Phase 7 — Safe research tools (planned):** opt-in OSINT workflows scoped
  to authorized, legitimate sources and use.
