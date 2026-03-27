import json
import os
import tempfile
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from time import perf_counter

from faster_whisper import WhisperModel

from . import config


class TranscriptionHandler(BaseHTTPRequestHandler):
    model = None

    def do_GET(self):
        if self.path != "/health":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return

        self._send_json(HTTPStatus.OK, {"status": "ok"})

    def do_POST(self):
        if self.path != "/transcribe":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "empty request body"})
            return

        audio_bytes = self.rfile.read(content_length)
        if not audio_bytes:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "empty audio payload"})
            return

        started = perf_counter()
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_path = temp_file.name

            segments, _ = self.model.transcribe(
                temp_path,
                beam_size=1,
                vad_filter=True,
            )
            text = " ".join(seg.text.strip() for seg in segments).strip()
            duration = perf_counter() - started

            self._send_json(
                HTTPStatus.OK,
                {
                    "text": text,
                    "duration_seconds": round(duration, 3),
                },
            )
        except Exception as exc:
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": str(exc)},
            )
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)

    def log_message(self, format, *args):
        print(
            f"{self.address_string()} - "
            f"{self.log_date_time_string()} - {format % args}"
        )

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run():
    print("Loading Whisper model...")
    TranscriptionHandler.model = WhisperModel(
        config.WHISPER_MODEL,
        compute_type=config.COMPUTE_TYPE,
    )

    server = ThreadingHTTPServer(
        (config.TRANSCRIBE_SERVER_HOST, config.TRANSCRIBE_SERVER_PORT),
        TranscriptionHandler,
    )

    print(
        "Transcription server listening on "
        f"http://{config.TRANSCRIBE_SERVER_HOST}:{config.TRANSCRIBE_SERVER_PORT}"
    )
    server.serve_forever()


if __name__ == "__main__":
    run()
