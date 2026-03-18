# CLAUDE.md — video-agency-ai

This file provides context and conventions for Claude when working in this repository.

## Project Overview

`video-agency-ai` is an AI-powered video production agency built on the Claude Agent SDK.
A user provides a brief, and a team of specialized agents collaborates to produce a complete video — from script to final cut.

## Repository Structure

| Directory  | Purpose |
|------------|---------|
| `agents/`  | Specialized AI agents (Script, Director, Review, etc.) |
| `brain/`   | Orchestration layer — task routing and agent coordination |
| `core/`    | Shared infrastructure: base classes, config, logging |
| `tools/`   | External tool wrappers (video render, TTS, image gen, etc.) |
| `memory/`  | Persistent and session-scoped memory for agents |
| `output/`  | Runtime-generated artifacts (not committed to git) |

## Conventions

- **Language**: Python 3.11+
- **AI SDK**: `anthropic` — use Claude claude-sonnet-4-6 (`claude-sonnet-4-6`) as the default model, Claude Opus 4.6 (`claude-opus-4-6`) for complex reasoning tasks
- **Agent pattern**: Each agent lives in its own file under `agents/`, inherits from `core/base_agent.py`
- **Tool pattern**: Each tool is a standalone function or class in `tools/`, stateless and composable
- **Memory**: Prefer structured memory files in `memory/`; vector store integration goes in `memory/vector/`
- **Secrets**: Never hardcode API keys — use `.env` (excluded from git)

## Running the Agency

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env  # then fill in your keys

# Run the agency with a brief
python -m brain.orchestrator --brief "Create a 60-second explainer about climate change"
```

## Key Design Principles

1. **Each agent has a single responsibility** — don't let agents bleed into each other's roles
2. **Brain decides, agents act** — routing logic lives in `brain/`, not in agents
3. **Tools are stateless** — all state lives in `memory/`
4. **Output is ephemeral** — regenerate rather than rely on cached output
