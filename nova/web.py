from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from nova.coach import coach
from nova.memory import DEFAULT_MEMORY_PATH, load_memory, save_memory


STATIC_DIR = Path(__file__).resolve().parent / "web_static"


def memory_payload(memory_path: Path = DEFAULT_MEMORY_PATH) -> dict[str, Any]:
    return {"memory": load_memory(memory_path)}


def handle_message(message: str, memory_path: Path = DEFAULT_MEMORY_PATH) -> dict[str, Any]:
    memory = load_memory(memory_path)
    response = coach(message, memory)
    save_memory(memory, memory_path)
    return {
        "response": asdict(response),
        "response_text": response.to_text(),
        "memory": memory,
    }


def create_handler(memory_path: Path = DEFAULT_MEMORY_PATH) -> type[BaseHTTPRequestHandler]:
    class NovaWebHandler(BaseHTTPRequestHandler):
        server_version = "NovaWeb/0.2"

        def do_GET(self) -> None:
            route = urlparse(self.path).path
            if route == "/api/memory":
                self._send_json(memory_payload(memory_path))
                return

            static_path = self._static_path(route)
            if static_path is None:
                self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
                return

            self._send_file(static_path)

        def do_POST(self) -> None:
            route = urlparse(self.path).path
            if route != "/api/message":
                self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
                return

            payload = self._read_json()
            message = str(payload.get("message", "")).strip()
            if not message:
                self._send_json(
                    {"error": "Message is required."},
                    HTTPStatus.BAD_REQUEST,
                )
                return

            self._send_json(handle_message(message, memory_path))

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length <= 0:
                return {}
            raw = self.rfile.read(length)
            try:
                payload = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                return {}
            return payload if isinstance(payload, dict) else {}

        def _send_json(
            self,
            payload: dict[str, Any],
            status: HTTPStatus = HTTPStatus.OK,
        ) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_file(self, path: Path) -> None:
            content_types = {
                ".html": "text/html; charset=utf-8",
                ".css": "text/css; charset=utf-8",
                ".js": "application/javascript; charset=utf-8",
            }
            body = path.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header(
                "Content-Type",
                content_types.get(path.suffix, "application/octet-stream"),
            )
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _static_path(self, route: str) -> Path | None:
            if route in {"", "/"}:
                candidate = STATIC_DIR / "index.html"
            else:
                candidate = STATIC_DIR / route.lstrip("/")

            try:
                resolved = candidate.resolve()
                resolved.relative_to(STATIC_DIR)
            except ValueError:
                return None

            return resolved if resolved.is_file() else None

    return NovaWebHandler


def run(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), create_handler())
    url = f"http://{host}:{port}"
    print(f"Nova web UI running at {url}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nNova web UI stopped.")
    finally:
        server.server_close()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run Nova's local web UI.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args(argv)
    run(args.host, args.port)


if __name__ == "__main__":
    main()
