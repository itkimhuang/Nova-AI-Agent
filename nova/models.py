from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CoachResponse:
    main_task: str
    optional_task: str | None
    tip: str
    encouragement: str
    progress: str | None = None

    def to_text(self) -> str:
        lines = [f"Main task: {self.main_task}"]
        if self.optional_task:
            lines.append(f"Optional: {self.optional_task}")
        lines.append(f"Tip: {self.tip}")
        if self.progress:
            lines.append(f"Progress: {self.progress}")
        lines.append(f"Encouragement: {self.encouragement}")
        return "\n".join(lines)
