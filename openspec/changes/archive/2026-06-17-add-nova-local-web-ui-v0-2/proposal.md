## Why

Nova v0.1 works from the command line, but a personal coach is easier to use when the current goal, memory, and conversation are visible in one place. A local web UI is the next small step toward making Nova feel like a daily study companion without adding voice, accounts, deployment, or a database.

## What Changes

- Add a local browser-based UI for typed conversations with Nova.
- Keep the existing Python coach logic and local JSON memory as the source of truth.
- Add a small local web server/API that the browser UI can call.
- Show the current goal, today's available time, recent progress, and last suggested task in the UI.
- Allow the user to send typed messages and see Nova's structured response.
- Keep the CLI available and working.
- Do not add voice input, cloud deployment, user accounts, or a database.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `nova-coach`: Add local web interaction behavior while preserving the existing CLI and local memory behavior.

## Impact

- Adds a small local web server layer around the existing coach.
- Adds browser UI files for the local chat experience.
- Reuses `nova.coach` and `nova.memory` instead of duplicating coaching logic.
- May add lightweight Python web dependencies.
- Keeps memory in `data/nova_memory.json`.
