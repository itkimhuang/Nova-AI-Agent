from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MEMORY_PATH = PROJECT_ROOT / "data" / "nova_memory.json"

DEFAULT_MEMORY: dict[str, Any] = {
    "current_goal": None,
    "available_time_today_minutes": None,
    "recent_progress": [],
    "project_focus": None,
    "last_suggested_task": None,
    "updated_at": None,
}


def default_memory() -> dict[str, Any]:
    return deepcopy(DEFAULT_MEMORY)


def normalize_memory(memory: dict[str, Any] | None) -> dict[str, Any]:
    normalized = default_memory()
    if memory:
        normalized.update(memory)
    if not isinstance(normalized.get("recent_progress"), list):
        normalized["recent_progress"] = []
    return normalized


def load_memory(path: Path = DEFAULT_MEMORY_PATH) -> dict[str, Any]:
    if not path.exists():
        memory = default_memory()
        save_memory(memory, path)
        return memory

    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        loaded = {}

    memory = normalize_memory(loaded if isinstance(loaded, dict) else {})
    if memory != loaded:
        save_memory(memory, path)
    return memory


def save_memory(memory: dict[str, Any], path: Path = DEFAULT_MEMORY_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = normalize_memory(memory)
    path.write_text(
        json.dumps(normalized, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def touch_memory(memory: dict[str, Any]) -> None:
    memory["updated_at"] = datetime.now(timezone.utc).isoformat()


def remember_progress(memory: dict[str, Any], note: str, limit: int = 5) -> None:
    progress = list(memory.get("recent_progress") or [])
    progress.append(note)
    memory["recent_progress"] = progress[-limit:]
    touch_memory(memory)
