## 1. Spec Review

- [x] 1.1 Review `proposal.md`, `design.md`, and `specs/nova-coach/spec.md`.
- [x] 1.2 Confirm v0.2 scope is a local web UI that reuses the existing Python coach and JSON memory.
- [x] 1.3 Confirm the existing CLI remains in scope and must keep working.
- [x] 1.4 Run `openspec validate add-nova-local-web-ui-v0-2 --strict` before implementation.

## 2. Web Server Setup

- [x] 2.1 Choose a lightweight Python web server approach.
- [x] 2.2 Add required dependency and run instructions.
- [x] 2.3 Add a local web entry point that can be run from the command line.
- [x] 2.4 Serve the browser UI from the local Python app.

## 3. Web API

- [x] 3.1 Add an endpoint for reading current Nova memory.
- [x] 3.2 Add an endpoint for sending a typed message to Nova.
- [x] 3.3 Route web messages through the existing `nova.coach` logic.
- [x] 3.4 Save memory updates through the existing `nova.memory` logic.
- [x] 3.5 Return structured response and memory data to the browser.

## 4. Browser UI

- [x] 4.1 Build a usable first screen with chat input and response history.
- [x] 4.2 Show current goal, available time, recent progress, and last suggested task.
- [x] 4.3 Display Nova responses with main task, optional task, tip, progress, and encouragement.
- [x] 4.4 Keep the layout practical, calm, and suitable for repeated study use.
- [x] 4.5 Handle empty input, loading state, and request errors.

## 5. Existing CLI Compatibility

- [x] 5.1 Confirm `python -m nova.cli` still works.
- [x] 5.2 Confirm CLI and web UI use the same project-level memory file.
- [x] 5.3 Confirm no web-specific coaching rules duplicate the core coach logic.

## 6. Tests

- [x] 6.1 Add tests for reading memory through the web API.
- [x] 6.2 Add tests for sending a message through the web API.
- [x] 6.3 Add tests that web requests update local memory.
- [x] 6.4 Keep existing v0.1 coach and memory tests passing.

## 7. Validation

- [x] 7.1 Run the full test suite.
- [x] 7.2 Run OpenSpec validation for the change.
- [x] 7.3 Manually start the local web server.
- [x] 7.4 Open the local web UI in a browser and send a message.
- [x] 7.5 Confirm memory is visible in the UI and updates after a message.
- [x] 7.6 Confirm there is no database, user account, cloud deployment, or voice input implementation.

## 8. User Acceptance Check

- [x] 8.1 User can start the local web UI from the command line.
- [x] 8.2 User can open Nova in a browser.
- [x] 8.3 User can send typed messages and receive useful Nova responses.
- [x] 8.4 User can see current goal, available time, recent progress, and last suggested task.
- [x] 8.5 User confirms the web UI feels calm, friendly, practical, and not too verbose.
- [x] 8.6 User confirms the CLI still works.
- [x] 8.7 User confirms v0.2 remains local and does not add database, accounts, cloud deployment, or voice input.
