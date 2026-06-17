## ADDED Requirements

### Requirement: Local web coaching session
Nova SHALL provide a local browser-based typed interaction mode for v0.2.

#### Scenario: User opens the local web UI
GIVEN the local Nova web server is running
WHEN the user opens the local web address in a browser
THEN Nova SHALL show a usable coaching interface
AND the interface SHALL allow the user to type a message.

#### Scenario: User sends a message from the web UI
GIVEN the local Nova web UI is open
WHEN the user submits a typed coaching message
THEN Nova SHALL return a structured coaching response
AND the response SHALL include one main task
AND the response SHALL include no more than one optional task
AND the response SHALL include one practical tip
AND the response SHALL include a short encouraging message.

### Requirement: Web UI memory visibility
Nova SHALL show lightweight local memory in the web UI.

#### Scenario: User views remembered context
GIVEN Nova has local memory
WHEN the user opens or refreshes the local web UI
THEN Nova SHALL show the current goal when one exists
AND Nova SHALL show today's available time when one exists
AND Nova SHALL show recent progress when it exists
AND Nova SHALL show the last suggested task when it exists.

#### Scenario: User sends progress-relevant information from the web UI
GIVEN the local Nova web UI is open
WHEN the user provides a new goal, time constraint, or progress-relevant message
THEN Nova SHALL update local JSON memory when appropriate
AND the updated memory SHALL be visible in the web UI.

### Requirement: v0.2 interface boundaries
Nova SHALL keep v0.2 as a local personal tool.

#### Scenario: User runs v0.2
GIVEN the v0.2 implementation is complete
WHEN the user interacts with Nova through the web UI
THEN Nova SHALL NOT require a database
AND Nova SHALL NOT require user accounts
AND Nova SHALL NOT require cloud deployment
AND Nova SHALL NOT require voice input
AND the existing CLI SHALL remain available.
