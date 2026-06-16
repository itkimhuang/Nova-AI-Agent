from __future__ import annotations

from nova.coach import coach
from nova.memory import default_memory


def test_goal_message_updates_memory_and_returns_coaching_response():
    memory = default_memory()

    response = coach("I want to learn AI agents this week.", memory)

    assert memory["current_goal"] == "learn AI agents this week"
    assert response.main_task
    assert response.optional_task
    assert response.tip
    assert response.encouragement
    assert "Main task:" in response.to_text()


def test_goal_message_accepts_missing_to_before_learn():
    memory = default_memory()

    response = coach("I want learn CCNA", memory)

    assert memory["current_goal"] == "learn CCNA"
    assert "CCNA" in response.main_task
    assert response.progress == "I saved your current goal: learn CCNA"


def test_repeated_goal_acknowledges_existing_memory():
    memory = default_memory()
    memory["current_goal"] = "learn CCNA"

    response = coach("I want learn CCNA", memory)

    assert memory["current_goal"] == "learn CCNA"
    assert response.progress == "I already have this as your current goal: learn CCNA"


def test_repeated_task_rotates_to_alternate_action():
    memory = default_memory()
    memory["current_goal"] = "learn CCNA"

    first = coach("I want learn CCNA", memory)
    second = coach("I want learn CCNA", memory)

    assert first.main_task != second.main_task
    assert "flashcards" in second.main_task


def test_greeting_does_not_reuse_old_goal_as_task():
    memory = default_memory()
    memory["current_goal"] = "learn AI agents this week"
    memory["available_time_today_minutes"] = 30

    response = coach("Hello", memory)

    assert "continue working on learn AI agents this week" in response.main_task
    assert "AI-agent" not in response.main_task


def test_longer_greeting_is_handled_as_greeting():
    memory = default_memory()
    memory["current_goal"] = "learn CCNA"

    response = coach("hi see u again", memory)

    assert "continue working on learn CCNA" in response.main_task
    assert "Good to see you again" in response.encouragement


def test_ccna_packet_tracer_practice_request():
    memory = default_memory()
    memory["current_goal"] = "learn CCNA"

    response = coach("pratice with Cisco package tracer", memory)

    assert "Cisco Packet Tracer" in response.main_task
    assert "tiny LAN" in response.main_task


def test_limited_time_updates_memory_and_sizes_task():
    memory = default_memory()
    memory["current_goal"] = "learn AI agents this week"

    response = coach("I only have 30 minutes today.", memory)

    assert memory["available_time_today_minutes"] == 30
    assert "30" in response.main_task
    assert response.progress


def test_what_next_reuses_current_goal():
    memory = default_memory()
    memory["current_goal"] = "learn AI agents this week"

    response = coach("What should I do next?", memory)

    assert "agent" in response.main_task.lower()
    assert response.optional_task is not None


def test_lazy_message_is_small_and_encouraging():
    memory = default_memory()
    memory["current_goal"] = "learn AI agents this week"

    response = coach("I feel lazy today.", memory)

    assert "10 minutes" in response.main_task
    assert "Small still counts" in response.encouragement


def test_project_process_stays_beginner_friendly():
    memory = default_memory()

    response = coach("Plan my project process.", memory)

    assert "three-step" in response.main_task
    assert response.optional_task
    assert "tiny working loop" in response.tip
