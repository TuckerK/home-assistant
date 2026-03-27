# Home Assistant Device

Voice assistant package for a Raspberry Pi client using local audio I/O, VM-hosted speech-to-text, Ollama over HTTP, and WS2812 LED state feedback.

## Documentation

- `docs/architecture.md`: current system design and module map
- `docs/operations.md`: install, run, and test commands for Pi and VM
- `docs/status.md`: current behavior, measurements, and known gaps
- `docs/next-steps.md`: next session handoff and ordered follow-up work

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
