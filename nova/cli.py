from __future__ import annotations

from pathlib import Path

from nova.coach import coach
from nova.memory import DEFAULT_MEMORY_PATH, load_memory, save_memory


EXIT_COMMANDS = {"exit", "quit", "q"}


def run(memory_path: Path = DEFAULT_MEMORY_PATH) -> None:
    memory = load_memory(memory_path)
    print("Nova v0.1 - local study coach")
    print("Type a message, or 'exit' to leave.")

    while True:
        try:
            user_message = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nNova: See you next time.")
            break

        if not user_message:
            continue

        if user_message.lower() in EXIT_COMMANDS:
            print("Nova: See you next time.")
            break

        response = coach(user_message, memory)
        save_memory(memory, memory_path)
        print(f"\nNova:\n{response.to_text()}")


def main() -> None:
    run()


if __name__ == "__main__":
    main()
