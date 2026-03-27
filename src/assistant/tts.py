import re
import subprocess

from . import config


def _clean(text):
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    return " ".join(text.split()).strip()


def speak(text):
    text = _clean(text)
    if not text:
        return

    espeak = subprocess.Popen(
        ["espeak", text, "--stdout"],
        stdout=subprocess.PIPE,
    )
    try:
        subprocess.run(
            ["aplay", "-D", config.SPEAKER_DEVICE],
            stdin=espeak.stdout,
            check=True,
        )
    finally:
        if espeak.stdout:
            espeak.stdout.close()
        espeak.wait()
