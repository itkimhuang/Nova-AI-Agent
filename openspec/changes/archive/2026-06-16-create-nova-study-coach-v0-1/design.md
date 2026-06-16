# Design: Nova Study Coach v0.1

## Goals
Nova v0.1 should be simple enough for a beginner to understand while still behaving like a useful personal coach. The implementation should favor explicit code, small modules, and a narrow set of behaviors over generalized agent infrastructure.

## Suggested Project Structure
```text
nova/
  __init__.py
  cli.py
  coach.py
  memory.py
  models.py
  prompts.py
data/
  nova_memory.json
tests/
  test_coach.py
  test_memory.py
README.md
pyproject.toml
```

## Runtime Shape
```text
User types message
        |
        v
CLI reads input
        |
        v
Memory loads JSON
        |
        v
Coach interprets message and prepares response
        |
        v
Memory updates when relevant
        |
        v
CLI prints calm, concise response
```

## Core Components

### CLI
The CLI is the first user interface. It should:
- start a local interactive session
- accept typed messages
- pass messages to the coach
- print Nova's response
- allow a simple exit command

### Coach
The coach is responsible for user-facing behavior. It should:
- keep responses short and practical
- choose one main task and at most one optional task
- include one practical tip
- include one encouraging sentence
- identify when memory should be updated
- avoid overwhelming the user with too many tasks

### Memory
Memory should be stored in a local JSON file. A minimal shape could be:
```json
{
  "current_goal": null,
  "available_time_today_minutes": null,
  "recent_progress": [],
  "project_focus": null,
  "last_suggested_task": null,
  "updated_at": null
}
```

The memory layer should:
- create the file if missing
- tolerate missing fields by applying defaults
- save updates after relevant messages
- remain human-readable

### Model Integration
v0.1 may use an LLM provider or a deterministic local response path. The design should keep model access behind a small boundary so learning and testing remain easy.

Recommended beginner-friendly path:
- implement the coach behavior around a clear response schema
- support deterministic tests for memory and formatting
- add real LLM calls only after the local loop is stable

### Voice Output
Voice output is future-facing for v0.1. The design may include a placeholder interface such as `speak(text)`, but actual text-to-speech implementation is optional. Voice input is out of scope.

## Future Interface Roadmap
Nova's interface can grow in layers without rewriting the coaching core:

```text
v0.1 CLI
  typed input -> coach backend -> JSON memory -> text response

v0.2 Local Web UI
  browser chat -> same coach backend -> JSON memory -> visual response

v0.3 Voice Output
  text response -> optional text-to-speech

v0.4 Voice Input
  speech-to-text -> same coach backend -> text and/or voice response
```

The v0.1 design should keep the coach backend independent from the CLI so later interfaces can call the same behavior. This is a design direction only; web UI and voice input remain out of scope for v0.1.

## Response Format
Nova should produce a predictable structure:
```text
Main task: ...
Optional: ...
Tip: ...
Progress: ...
Encouragement: ...
```

If there is no meaningful memory update, the progress line may be omitted or say that no memory changed. The wording should stay natural and not feel like a form.

## Key Design Decisions
- Use Python for the backend.
- Use a local JSON file for v0.1 memory.
- Use a CLI instead of a web UI.
- Keep behavior narrow and coaching-oriented.
- Prefer a small, testable response pipeline over a broad autonomous agent framework.
- Treat voice output as an extension point, not a required v0.1 feature.

## Risks
- The assistant may over-plan and give too many tasks.
- Memory updates may become messy if the JSON shape is not constrained.
- LLM responses may drift from the desired calm, concise coaching style.
- Adding voice too early could distract from the core coaching loop.

## Mitigations
- Define observable response requirements in the spec.
- Use a simple response schema.
- Add tests for memory defaults and update behavior.
- Keep v0.1 CLI-only.
- Defer voice input entirely.
