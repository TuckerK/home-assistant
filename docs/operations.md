# Operations

## Pi setup

```bash
cd ~/Projects/home-assistant
~/assistant-env/bin/pip install -e ".[pi]"
sudo ~/assistant-env/bin/python -m assistant
```

## VM setup

Create the virtual environment once:

```bash
cd ~/projects/home-assistant
python3 -m venv .venv
.venv/bin/pip install -e ".[server]"
```

Run the transcription service:

```bash
cd ~/projects/home-assistant
.venv/bin/python -m assistant.server
```

Health check:

```bash
curl http://127.0.0.1:8765/health
```

Expected response:

```json
{"status": "ok"}
```

## Ollama service on VM

- Ollama is expected to listen on `0.0.0.0:11434`.
- The active fix was removing a bad `OLLAMA_MODELS=/home/tuck/ollama` override that prevented the `ollama` service user from starting.
- The current override should keep only:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Useful checks:

```bash
sudo systemctl show ollama --property=Environment --property=DropInPaths
ss -tulnp | grep 11434
curl http://127.0.0.1:11434/api/tags
curl http://192.168.1.24:11434/api/tags
```

## Git workflow

VM:

```bash
cd ~/projects/home-assistant
git status
git add <files>
git commit -m "<message>"
git push
```

Pi:

```bash
cd ~/Projects/home-assistant
git pull
```

## Testing checklist

Run on Pi and verify:

1. LED changes through idle, recording, thinking, and speaking states.
2. `record`, `stt`, `llm`, and `tts` timings print for each interaction.
3. `What time is it in Shanghai?` returns the Shanghai timezone, not the Pi local timezone.
4. Weather/news/current-data questions return the safe fallback instead of hallucinated facts.
5. Normal prompts still reach Ollama on the VM.
