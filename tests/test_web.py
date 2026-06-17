from __future__ import annotations

import json
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any

from nova.memory import load_memory
from nova.web import create_handler, handle_message, memory_payload


def test_memory_payload_reads_current_memory(tmp_path):
    path = tmp_path / "memory.json"
    memory = load_memory(path)
    memory["current_goal"] = "learn CCNA"
    path.write_text(json.dumps(memory), encoding="utf-8")

    payload = memory_payload(path)

    assert payload["memory"]["current_goal"] == "learn CCNA"


def test_handle_message_routes_through_coach_and_saves_memory(tmp_path):
    path = tmp_path / "memory.json"

    payload = handle_message("I want to learn CCNA", path)
    saved = load_memory(path)

    assert payload["response"]["main_task"]
    assert payload["memory"]["current_goal"] == "learn CCNA"
    assert saved["current_goal"] == "learn CCNA"


def test_web_api_message_updates_memory(tmp_path):
    path = tmp_path / "memory.json"
    server = ThreadingHTTPServer(("127.0.0.1", 0), create_handler(path))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        body = _request(
            server.server_port,
            "POST",
            "/api/message",
            {"message": "I only have 30 minutes today."},
        )
    finally:
        server.shutdown()
        server.server_close()

    assert body["memory"]["available_time_today_minutes"] == 30
    assert body["response"]["tip"]


def test_web_api_memory_endpoint(tmp_path):
    path = tmp_path / "memory.json"
    handle_message("I want to learn CCNA", path)
    server = ThreadingHTTPServer(("127.0.0.1", 0), create_handler(path))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        body = _request(server.server_port, "GET", "/api/memory")
    finally:
        server.shutdown()
        server.server_close()

    assert body["memory"]["current_goal"] == "learn CCNA"


def test_web_server_serves_browser_ui(tmp_path):
    path = tmp_path / "memory.json"
    server = ThreadingHTTPServer(("127.0.0.1", 0), create_handler(path))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        conn = HTTPConnection("127.0.0.1", server.server_port, timeout=5)
        conn.request("GET", "/")
        response = conn.getresponse()
        body = response.read().decode("utf-8")
        conn.close()
    finally:
        server.shutdown()
        server.server_close()

    assert response.status == 200
    assert "Nova Study Coach" in body
    assert "message" in body


def _request(
    port: int,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    conn = HTTPConnection("127.0.0.1", port, timeout=5)
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    conn.request(method, path, body=body, headers=headers)
    response = conn.getresponse()
    raw = response.read()
    conn.close()
    assert response.status < 400
    return json.loads(raw.decode("utf-8"))
