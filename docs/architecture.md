# Architecture

## Current topology

- Raspberry Pi handles microphone capture, LED status, and text-to-speech playback.
- Ubuntu VM handles speech-to-text over HTTP and Ollama text generation.
- Ollama is reachable on `http://192.168.1.24:11434`.
- The transcription service is reachable on `http://192.168.1.24:8765`.

## Request flow

1. Pi records audio into `input.wav`.
2. Pi uploads the WAV file to the VM transcription endpoint.
3. VM transcribes speech with `faster-whisper` and returns JSON with `text`.
4. Pi runs local intent routing.
5. If no local intent matches, Pi sends text to Ollama on the VM.
6. Pi speaks the reply with `espeak | aplay`.

## Package layout

- `src/assistant/app.py`: main loop and stage timing
- `src/assistant/config.py`: shared constants and endpoint settings
- `src/assistant/audio.py`: `arecord` capture
- `src/assistant/stt.py`: Pi client for VM-hosted transcription
- `src/assistant/server.py`: VM transcription HTTP service
- `src/assistant/llm.py`: Ollama HTTP client
- `src/assistant/intents.py`: local commands and safe fallbacks
- `src/assistant/tts.py`: `espeak` output pipeline
- `src/assistant/leds.py`: WS2812 LED ring control
- `src/assistant/timing.py`: simple per-stage timing context manager

## Dependency split

- Base dependencies: `requests`
- Pi extra: `.[pi]`
  - `rpi-ws281x`
  - `adafruit-circuitpython-neopixel`
  - `adafruit-blinka`
- VM/server extra: `.[server]`
  - `faster-whisper`

## Notes

- The Pi no longer needs local `faster-whisper`.
- The VM transcription server currently uses Python's built-in `http.server` instead of Flask/FastAPI to keep the first working version small.
- Ollama and transcription are separate services today. They could be merged behind one VM endpoint later.
