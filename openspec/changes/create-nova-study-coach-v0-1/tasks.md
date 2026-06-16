# Tasks: Create Nova Study Coach v0.1

## 1. Spec Review
- [x] 1.1 Review `proposal.md`, `design.md`, and `specs/nova-coach/spec.md`.
- [x] 1.2 Confirm v0.1 scope is CLI-only with Python backend and local JSON memory.
- [x] 1.3 Confirm future web UI, voice output, and voice input are documented only as later-version direction.
- [x] 1.4 Run `openspec validate create-nova-study-coach-v0-1 --strict` before implementation.

## 2. Project Setup
- [x] 2.1 Create the minimal Python project structure.
- [x] 2.2 Add a README with local run instructions.
- [x] 2.3 Add basic dependency and script configuration.

## 3. Memory
- [x] 3.1 Define the v0.1 JSON memory shape.
- [x] 3.2 Implement loading memory from a local JSON file.
- [x] 3.3 Implement default memory creation when the file does not exist.
- [x] 3.4 Implement saving memory updates.
- [x] 3.5 Add tests for missing file, missing fields, and persisted updates.

## 4. Coaching Behavior
- [x] 4.1 Implement the core coach function that accepts a user message and memory.
- [x] 4.2 Detect goal-setting messages and update current goal.
- [x] 4.3 Detect available-time messages and update available time for today.
- [x] 4.4 Generate one main task, one optional task, one practical tip, and one encouraging message.
- [x] 4.5 Keep responses concise and avoid suggesting too many tasks.
- [x] 4.6 Keep the coach logic independent from the CLI so future web and voice interfaces can reuse it.
- [x] 4.7 Add tests for the target v0.1 example messages.

## 5. CLI
- [x] 5.1 Implement a local interactive command-line loop.
- [x] 5.2 Load memory at startup and save it after relevant turns.
- [x] 5.3 Add a simple exit command.
- [x] 5.4 Print Nova responses in a readable format.

## 6. Optional Voice Output Design Hook
- [x] 6.1 Add a placeholder text-to-speech boundary or documented extension point.
- [x] 6.2 Keep actual voice output optional for v0.1.
- [x] 6.3 Do not implement voice input in v0.1.

## 7. Validation
- [x] 7.1 Run the test suite.
- [x] 7.2 Manually try the target v0.1 messages in the CLI.
- [x] 7.3 Confirm memory persists across CLI restarts.
- [x] 7.4 Confirm there is no database, web UI, or voice input implementation in v0.1.
- [x] 7.5 Confirm future web UI, voice output, and voice input are documented only as future OpenSpec changes.

## 8. Acceptance Check
- [x] 8.1 Nova can run locally from the command line.
- [x] 8.2 Nova accepts typed messages and exits cleanly.
- [x] 8.3 Nova answers the five target v0.1 messages with one main task, no more than one optional task, one practical tip, and one short encouraging message.
- [x] 8.4 Nova updates local JSON memory when the user provides a goal, time constraint, or progress-relevant information.
- [x] 8.5 Nova reuses stored memory in later interactions.
- [x] 8.6 Nova keeps responses calm, friendly, direct, practical, and not too verbose.
- [x] 8.7 Nova does not require a database, web UI, cloud deployment, or voice input.
- [x] 8.8 `openspec validate create-nova-study-coach-v0-1 --strict` passes after implementation.

## Minimal First Milestone
- [x] Create a runnable CLI where Nova can answer the five target message types and persist a current goal/progress JSON file.
