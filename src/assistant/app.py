import time

from . import config
from .audio import record_audio
from .intents import handle
from .leds import LedRing
from .stt import SpeechToText
from .timing import timed
from .tts import speak


def run():
    leds = LedRing()
    stt = SpeechToText()

    try:
        while True:
            leds.set(config.IDLE, "idle")
            cmd = input("Press Enter to talk, or type q to quit: ").strip().lower()

            if cmd == "q":
                break

            try:
                leds.set(config.RECORDING, "recording")
                print("Recording... Press Enter again to STOP")
                with timed("record"):
                    audio_file = record_audio()

                leds.set(config.THINKING, "thinking")
                print("Transcribing...")
                with timed("stt"):
                    text = stt.transcribe(audio_file)
                print("You said:", text if text else "(nothing detected)")

                with timed("llm"):
                    response = handle(text)
                print("Assistant:", response)

                leds.set(config.SPEAKING, "speaking")
                with timed("tts"):
                    speak(response)
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                print("Error:", exc)
                leds.set(config.ERROR, "error")
                speak("Something went wrong.")
                time.sleep(1)
    finally:
        leds.set(config.OFF, "off")
