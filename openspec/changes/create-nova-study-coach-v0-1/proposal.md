# Change: Create Nova Study Coach v0.1

## Summary
Create the first local version of Nova, a personal voice-oriented study and project coach. In v0.1, Nova will run as a simple local text-based assistant that helps plan study sessions, side-project progress, and daily next steps while keeping lightweight memory in a JSON file.

Nova is a learning-focused side project, not an enterprise agent platform. The first version should be small, understandable, and easy to run locally.

## Scope
- Provide a Python-based local agent backend.
- Accept typed user messages from a local command-line interface.
- Respond with a concise coaching format:
  - one main task for today
  - one optional task
  - one practical tip
  - one short encouraging message
  - memory or progress update when relevant
- Store simple memory in a local JSON file.
- Track current goal, available time, recent progress, and lightweight user state.
- Support study planning, side-project planning, goal breakdown, learning tips, and motivation.
- Design for future voice output without requiring it in v0.1.

## Non-Goals
- No web UI in v0.1.
- No database in v0.1.
- No voice input in v0.1.
- No multi-user support.
- No cloud deployment.
- No complex planner, calendar integration, reminders, or notification system.
- No autonomous background execution.
- No enterprise permissions, audit logs, analytics, or team features.
- No large plugin architecture or tool ecosystem in v0.1.

## Future Direction
These items are not part of the v0.1 implementation scope, but they describe a likely step-by-step path for later OpenSpec changes:

- v0.2 may add a local web UI that connects to the same Python coach backend and JSON memory.
- v0.3 may add optional voice output so Nova can speak responses.
- v0.4 may add voice input so spoken messages can become user input.
- Later versions may improve scheduling, reminders, richer memory, and project tracking after the basic coaching loop is stable.

Each future version should be proposed as its own OpenSpec change instead of being bundled into v0.1.

## Why
The project needs a small first milestone that teaches the fundamentals of building an AI agent:
- clear user input and assistant output loop
- simple memory
- practical behavior constraints
- spec-driven development
- room to add voice later

## Minimal First Milestone
Build a runnable local CLI prototype where the user can type:
- "I want to learn AI agents this week."
- "I only have 30 minutes today."
- "What should I do next?"
- "I feel lazy today."
- "Plan my project process."

Nova should answer calmly and practically with one main task, one optional task, one tip, encouragement, and any memory update. The memory should persist between runs in a local JSON file.

## Open Questions
- Which AI model provider should v0.1 use, or should the first prototype support a deterministic/mock response mode for learning and testing?
- Should voice output be omitted completely in v0.1, or included as an optional interface behind a simple setting?
- What exact fields should the first memory JSON file contain beyond current goal, progress, available time, and recent notes?
