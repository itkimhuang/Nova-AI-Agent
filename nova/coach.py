from __future__ import annotations

import re
from typing import Any

from nova.memory import remember_progress, touch_memory
from nova.models import CoachResponse


def coach(user_message: str, memory: dict[str, Any]) -> CoachResponse:
    message = user_message.strip()
    lowered = message.lower()
    progress_update: str | None = None
    previous_goal = _current_goal(memory)

    minutes = _extract_minutes(lowered)
    if minutes is not None:
        memory["available_time_today_minutes"] = minutes
        touch_memory(memory)
        progress_update = f"I saved that you have about {minutes} minutes today."

    goal = _extract_goal(message, lowered)
    if goal:
        if previous_goal and previous_goal.lower() == goal.lower():
            progress_update = f"I already have this as your current goal: {goal}"
        else:
            memory["current_goal"] = goal
            touch_memory(memory)
            progress_update = f"I saved your current goal: {goal}"

    if _mentions_progress(lowered):
        remember_progress(memory, message)
        progress_update = "I saved this as a recent progress note."

    if _is_greeting(lowered):
        main_task = _greeting_task(memory)
        optional_task = "You can also tell me how much time you have."
        tip = "A clear goal and time limit help me keep the plan small."
    elif _asks_practice(lowered):
        main_task = _practice_task(memory, lowered)
        optional_task = "Write down one thing that was confusing during the lab."
        tip = "Hands-on practice is good; keep the lab small enough to finish today."
    elif _asks_project_plan(lowered):
        memory["project_focus"] = memory.get("project_focus") or "Plan side project process"
        main_task = "Write a three-step project path: smallest prototype, first test, next improvement."
        optional_task = "Pick the one step you can finish this week."
        tip = "Keep the plan boring and concrete; a tiny working loop beats a big perfect map."
    elif _feels_low_motivation(lowered):
        main_task = _small_task_for(memory)
        optional_task = "Stop after the first 10 minutes if you still feel stuck."
        tip = "Use a five-minute timer and only promise to start, not to finish everything."
    elif minutes is not None:
        main_task = _time_boxed_task(memory, minutes)
        optional_task = "Write one sentence about what you learned when the timer ends."
        tip = "Protect the time box; one focused block is enough for today."
    elif goal:
        main_task = _first_goal_task(goal)
        optional_task = "Write down one question you want Nova to help with next."
        tip = "Start with the smallest visible action so momentum has somewhere to land."
    elif _asks_next(lowered):
        main_task = _next_task(memory)
        optional_task = "If you finish early, write a one-line progress note."
        tip = "Do the next useful step, not the most impressive one."
    else:
        main_task = _next_task(memory)
        optional_task = "Share your available time today so I can size the next task better."
        tip = "Keep today's plan to one clear action."

    main_task = _avoid_repeated_task(main_task, memory)
    memory["last_suggested_task"] = main_task
    touch_memory(memory)

    return CoachResponse(
        main_task=main_task,
        optional_task=optional_task,
        tip=tip,
        progress=progress_update,
        encouragement=_encouragement(lowered),
    )


def _extract_minutes(lowered: str) -> int | None:
    match = re.search(r"\b(\d{1,3})\s*(minutes?|mins?|min)\b", lowered)
    if match:
        return int(match.group(1))
    if "half an hour" in lowered:
        return 30
    return None


def _extract_goal(message: str, lowered: str) -> str | None:
    patterns = [
        r"\bi want(?: to)? (?P<goal>learn .+)",
        r"\bi want to (?P<goal>.+)",
        r"\bi need(?: to)? (?P<goal>learn .+)",
        r"\bi need to (?P<goal>.+)",
        r"\bmy goal is (?P<goal>.+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, message, flags=re.IGNORECASE)
        if match:
            return _clean_goal(match.group("goal"))
    if "learn ai agents" in lowered:
        return "learn AI agents this week"
    return None


def _clean_goal(goal: str) -> str:
    cleaned = goal.strip().rstrip(".!?")
    if cleaned.lower().startswith("learn "):
        return cleaned
    return cleaned[:1].lower() + cleaned[1:] if cleaned else cleaned


def _mentions_progress(lowered: str) -> bool:
    return any(
        phrase in lowered
        for phrase in ["i finished", "i completed", "i did ", "done with", "made progress"]
    )


def _is_greeting(lowered: str) -> bool:
    normalized = lowered.strip(" .!?\t")
    if normalized in {"hi", "hello", "hey", "yo"}:
        return True
    words = normalized.split()
    return len(words) <= 5 and words[:1] in [["hi"], ["hello"], ["hey"]]


def _asks_practice(lowered: str) -> bool:
    return any(
        phrase in lowered
        for phrase in [
            "practice",
            "pratice",
            "packet tracer",
            "package tracer",
            "cisco packet",
            "cisco package",
            "lab",
        ]
    )


def _asks_project_plan(lowered: str) -> bool:
    return "plan my project" in lowered or "project process" in lowered


def _feels_low_motivation(lowered: str) -> bool:
    return any(word in lowered for word in ["lazy", "tired", "stuck", "unmotivated"])


def _asks_next(lowered: str) -> bool:
    return "what should i do next" in lowered or "next?" in lowered


def _current_goal(memory: dict[str, Any]) -> str | None:
    goal = memory.get("current_goal")
    return goal if isinstance(goal, str) and goal.strip() else None


def _first_goal_task(goal: str) -> str:
    if "ai agent" in goal.lower():
        return "Spend 25 minutes learning what an agent loop is: input, memory, decision, response."
    if "ccna" in goal.lower():
        return "Spend 25 minutes reviewing one CCNA topic and write three key notes."
    return f"Spend 25 minutes making the first small note or outline for {goal}."


def _greeting_task(memory: dict[str, Any]) -> str:
    goal = _current_goal(memory)
    if goal:
        return f"Tell me if you want to continue working on {goal} today, or set a new goal."
    return "Tell me one goal you want to work on today."


def _practice_task(memory: dict[str, Any], lowered: str) -> str:
    goal = _current_goal(memory)
    if "ccna" in lowered or (goal and "ccna" in goal.lower()):
        return "Open Cisco Packet Tracer and build one tiny LAN with two PCs and one switch."
    if goal:
        return f"Spend 20 minutes doing one hands-on practice step for {goal}."
    return "Tell me the skill you want to practice, then I will make the lab smaller."


def _time_boxed_task(memory: dict[str, Any], minutes: int) -> str:
    goal = _current_goal(memory)
    if minutes <= 15:
        return "Do a tiny review: read one short section and write one takeaway."
    if goal and "ai agent" in goal.lower():
        return f"Use {minutes} minutes to study one AI-agent concept and write three bullet notes."
    if goal:
        return f"Use {minutes} minutes for one focused step toward {goal}."
    return f"Use {minutes} minutes to choose one goal and write the next concrete action."


def _small_task_for(memory: dict[str, Any]) -> str:
    goal = _current_goal(memory)
    if goal:
        return f"Open your materials for {goal} and work for just 10 minutes."
    return "Choose one small learning topic and spend 10 minutes getting started."


def _next_task(memory: dict[str, Any]) -> str:
    goal = _current_goal(memory)
    minutes = memory.get("available_time_today_minutes")
    if goal and isinstance(minutes, int):
        return _time_boxed_task(memory, minutes)
    if goal:
        return _first_goal_task(goal)
    return "Tell me one goal you want to work on, like 'I want to learn CCNA this week.'"


def _avoid_repeated_task(main_task: str, memory: dict[str, Any]) -> str:
    if memory.get("last_suggested_task") != main_task:
        return main_task

    goal = _current_goal(memory)
    minutes = memory.get("available_time_today_minutes")
    time_box = minutes if isinstance(minutes, int) else 15
    if goal and "ccna" in goal.lower():
        return f"Use {time_box} minutes to pick one CCNA exam objective and make two flashcards."
    if goal:
        return f"Use {time_box} minutes to make one concrete note for {goal}."
    return "Tell me your goal and today's available time so I can give a sharper next step."


def _encouragement(lowered: str) -> str:
    if _feels_low_motivation(lowered):
        return "Small still counts; make the start easy."
    if _is_greeting(lowered):
        return "Good to see you again; we can keep this simple."
    return "You are keeping this practical, and that is how progress starts."
