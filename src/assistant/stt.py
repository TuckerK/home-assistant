import requests

from . import config


class SpeechToText:
    def __init__(self, url=None):
        self.url = url or config.TRANSCRIBE_URL

    def transcribe(self, filename):
        with open(filename, "rb") as audio_file:
            response = requests.post(
                self.url,
                data=audio_file,
                headers={"Content-Type": "audio/wav"},
                timeout=config.TRANSCRIBE_TIMEOUT,
            )

        response.raise_for_status()
        data = response.json()
        return data.get("text", "").strip()
