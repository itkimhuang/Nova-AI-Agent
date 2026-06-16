from __future__ import annotations

import json

from nova.memory import DEFAULT_MEMORY_PATH, load_memory, save_memory


def test_default_memory_path_uses_project_data_directory():
    assert DEFAULT_MEMORY_PATH.is_absolute()
    assert DEFAULT_MEMORY_PATH.parts[-2:] == ("data", "nova_memory.json")


def test_load_memory_creates_default_file(tmp_path):
    path = tmp_path / "memory.json"

    memory = load_memory(path)

    assert path.exists()
    assert memory["current_goal"] is None
    assert memory["recent_progress"] == []


def test_load_memory_fills_missing_fields(tmp_path):
    path = tmp_path / "memory.json"
    path.write_text(json.dumps({"current_goal": "learn AI agents"}), encoding="utf-8")

    memory = load_memory(path)

    assert memory["current_goal"] == "learn AI agents"
    assert memory["available_time_today_minutes"] is None
    assert memory["recent_progress"] == []


def test_save_memory_persists_updates(tmp_path):
    path = tmp_path / "memory.json"
    memory = load_memory(path)
    memory["current_goal"] = "learn AI agents"

    save_memory(memory, path)
    loaded = load_memory(path)

    assert loaded["current_goal"] == "learn AI agents"
