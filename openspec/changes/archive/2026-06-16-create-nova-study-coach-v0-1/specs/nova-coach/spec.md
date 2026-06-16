# nova-coach Specification

## ADDED Requirements

### Requirement: Local typed coaching session
Nova SHALL provide a local text-based interaction mode for v0.1.

#### Scenario: User sends a typed study goal
GIVEN Nova is running locally
WHEN the user enters "I want to learn AI agents this week."
THEN Nova SHALL respond with a concise coaching response
AND the response SHALL include one main task for today
AND the response SHALL include no more than one optional task
AND Nova SHALL remember the current goal when appropriate.

#### Scenario: User asks what to do next
GIVEN Nova has stored a current goal
WHEN the user asks "What should I do next?"
THEN Nova SHALL recommend one main next task related to the current goal
AND Nova SHOULD include one optional task only if it is helpful
AND Nova SHALL avoid listing many tasks at once.

### Requirement: Daily task focus
Nova SHALL prioritize a single main task for the current day.

#### Scenario: User has limited time
GIVEN Nova is running locally
WHEN the user says "I only have 30 minutes today."
THEN Nova SHALL tailor the main task to fit the stated time limit
AND Nova SHOULD update memory with the available time for today
AND Nova SHALL avoid recommending a workload that exceeds the stated constraint.

#### Scenario: User feels low motivation
GIVEN Nova is running locally
WHEN the user says "I feel lazy today."
THEN Nova SHALL suggest a small achievable main task
AND Nova SHALL provide a practical tip for starting
AND Nova SHALL include a short encouraging message
AND Nova SHALL NOT shame the user.

### Requirement: Response content
Nova SHALL respond in a calm, friendly, direct, and practical style.

#### Scenario: Nova responds to a coaching request
GIVEN the user sends a study or project planning message
WHEN Nova generates a response
THEN the response SHALL include one main task
AND the response SHALL include one practical tip
AND the response SHALL include a short encouraging message
AND the response SHOULD include one optional task
AND the response MAY include a memory or progress update.

#### Scenario: Nova avoids overwhelming the user
GIVEN the user asks for planning help
WHEN Nova generates a response
THEN Nova SHALL NOT provide a long list of tasks
AND Nova SHALL NOT assign multiple required tasks for the same day
AND Nova SHOULD keep the response brief.

### Requirement: Study planning support
Nova SHALL help the user plan study goals into small daily actions.

#### Scenario: User states a weekly learning goal
GIVEN the user has no current goal stored
WHEN the user states a weekly study goal
THEN Nova SHOULD store the goal as the current goal
AND Nova SHALL propose one practical task for today that starts the goal.

### Requirement: Side project planning support
Nova SHALL help the user plan side-project progress in small steps.

#### Scenario: User asks to plan project process
GIVEN Nova is running locally
WHEN the user says "Plan my project process."
THEN Nova SHALL suggest one concrete project-planning task for today
AND Nova SHOULD include one optional follow-up task
AND Nova SHALL keep the plan suitable for a beginner.

### Requirement: Local memory
Nova SHALL persist lightweight user memory locally for v0.1.

#### Scenario: Memory file does not exist
GIVEN Nova starts and no memory file exists
WHEN Nova needs memory
THEN Nova SHALL create or initialize memory with default values
AND Nova SHALL continue running without requiring manual setup.

#### Scenario: User provides progress-relevant information
GIVEN Nova is running locally
WHEN the user provides a new goal, time constraint, or progress update
THEN Nova SHALL update local memory when appropriate
AND the updated memory SHALL be available in later interactions.

### Requirement: v0.1 implementation boundaries
Nova SHALL remain a simple local v0.1 assistant.

#### Scenario: User runs v0.1
GIVEN the v0.1 implementation is complete
WHEN the user interacts with Nova
THEN Nova SHALL NOT require a database
AND Nova SHALL NOT require a web UI
AND Nova SHALL NOT require voice input
AND Nova MAY expose a future extension point for voice output.
