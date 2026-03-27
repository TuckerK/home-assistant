from faster_whisper import WhisperModel

from . import config


class SpeechToText:
    def __init__(self):
        self.model = WhisperModel(
            config.WHISPER_MODEL,
            compute_type=config.COMPUTE_TYPE,
        )

    def transcribe(self, filename):
        segments, _ = self.model.transcribe(
            filename,
            beam_size=1,
            vad_filter=True,
        )
        return " ".join(seg.text.strip() for seg in segments).strip()
