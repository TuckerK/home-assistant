import subprocess

from . import llm


def handle(text):
    if not text:
        return "I did not catch that."

    lower = " ".join(text.lower().split())

    if "time" in lower:
        return subprocess.check_output(["date", "+%I:%M %p"]).decode().strip()
    if "hello" in lower:
        return "Hello Tucker. I am online."
    if "shutdown" in lower or "shut down" in lower:
        return "Shutdown command recognized, but not executed."

    return llm.ask(text)
