VOICE_OUTPUT_NOTE = (
    "Nova v0.1 is text-only. Future versions may pass the response text to "
    "a text-to-speech adapter."
)


def speak(text: str) -> None:
    """Placeholder extension point for future text-to-speech support."""
    _ = text
