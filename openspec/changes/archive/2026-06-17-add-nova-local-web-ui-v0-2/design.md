## Context

Nova v0.1 is a local Python CLI that routes typed messages through `nova.coach`, updates memory with `nova.memory`, and stores local state in `data/nova_memory.json`. The next step is to make the same coaching loop easier to use by adding a local browser UI while keeping the existing CLI and memory behavior intact.

This change should stay beginner-friendly. It should not introduce accounts, cloud hosting, a database, voice input, or a large frontend framework unless the implementation proves it is clearly worth the extra complexity.

## Goals / Non-Goals

**Goals:**

- Add a local web UI for typed Nova conversations.
- Reuse the existing Python coach and JSON memory modules.
- Show current goal, available time, recent progress, and last suggested task in the UI.
- Keep the response style and one-main-task behavior from v0.1.
- Keep the CLI working.
- Keep the app runnable locally with simple commands.

**Non-Goals:**

- No voice input.
- No required voice output.
- No database.
- No authentication or multi-user accounts.
- No cloud deployment.
- No large autonomous agent framework.
- No replacement of the existing CLI.

## Decisions

### Use a Small Python Web Server

Use a lightweight Python web server so the browser UI can call the same backend code as the CLI.

Rationale:
- keeps the project Python-first
- avoids duplicating coach behavior in JavaScript
- gives a natural future path for voice output and richer UI controls

Alternative considered: static HTML only. This is simpler, but it cannot safely update local JSON memory without a local backend.

### Keep Coach Logic UI-Independent

The web route should call `coach(user_message, memory)` just like the CLI does. UI code should format and display results, not decide coaching behavior.

Rationale:
- keeps one source of truth for Nova behavior
- keeps tests focused
- makes future CLI/web behavior consistent

Alternative considered: separate web-specific coach behavior. This would drift quickly and make beginner maintenance harder.

### Use Local JSON Memory for v0.2

Continue using `data/nova_memory.json`.

Rationale:
- matches v0.1 constraints
- keeps memory inspectable by the user
- avoids database setup

Alternative considered: SQLite. This is useful later, but too much for v0.2.

### Build a Practical App Screen, Not a Landing Page

The first browser screen should be the usable Nova chat and memory view.

Rationale:
- Nova is a tool, not a marketing site
- the user should immediately interact with the coach
- visible memory helps the user understand what Nova remembers

## Risks / Trade-offs

- Browser UI may add frontend complexity -> keep HTML/CSS/JS small and focused.
- API and CLI could diverge -> route all coaching through shared `nova.coach`.
- Memory file writes could be inconsistent -> keep memory load/save in `nova.memory`.
- UI may imply Nova is smarter than the rule-based v0.1 backend -> keep copy and behavior practical, and avoid pretending there is a real AI model until one is added.

## Migration Plan

1. Add the local web server and UI files.
2. Keep existing CLI commands working.
3. Add tests for the web API.
4. Run the CLI and web UI manually.

Rollback is simple: remove the web server/UI files and dependency while keeping the v0.1 CLI modules.

## Open Questions

- Should v0.2 use Flask, FastAPI, or Python standard library HTTP serving?
- Should the local web UI expose a clear memory reset button in v0.2, or leave memory reset as manual file deletion?
- Should v0.2 include a small API endpoint for reading memory separately from sending messages?
