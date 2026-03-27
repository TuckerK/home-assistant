from datetime import datetime
import subprocess
from zoneinfo import ZoneInfo

from . import llm

TIMEZONE_ALIASES = {
    "shanghai": "Asia/Shanghai",
    "tokyo": "Asia/Tokyo",
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "new york": "America/New_York",
    "los angeles": "America/Los_Angeles",
    "san francisco": "America/Los_Angeles",
    "chicago": "America/Chicago",
}

LIVE_INFO_KEYWORDS = (
    "weather",
    "forecast",
    "temperature",
    "rain",
    "snow",
    "news",
    "traffic",
    "stock",
    "stocks",
    "bitcoin",
    "price",
)


def _time_response(text):
    lower = " ".join(text.lower().split())

    for place, zone in TIMEZONE_ALIASES.items():
        if place in lower:
            local_time = datetime.now(ZoneInfo(zone)).strftime("%I:%M %p")
            return f"It is {local_time} in {place.title()}."

    return subprocess.check_output(["date", "+%I:%M %p"]).decode().strip()


def handle(text):
    if not text:
        return "I did not catch that."

    lower = " ".join(text.lower().split())

    if "time" in lower:
        return _time_response(text)
    if "hello" in lower:
        return "Hello Tucker. I am online."
    if "shutdown" in lower or "shut down" in lower:
        return "Shutdown command recognized, but not executed."
    if any(keyword in lower for keyword in LIVE_INFO_KEYWORDS):
        return "I do not have live data access for that yet."

    return llm.ask(text)
