# Home Assistant Device

Voice assistant package for a Raspberry Pi client using local audio I/O, VM-hosted speech-to-text, Ollama over HTTP, and WS2812 LED state feedback.

## Pi setup

```bash
pip install -e ".[pi]"
python -m assistant
```

## VM transcription server

```bash
pip install -e ".[server]"
python -m assistant.server
```
