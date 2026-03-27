# Next Steps

## Session handoff

As of 2026-03-27:

- Ollama is reachable from the Pi at `http://192.168.1.24:11434`.
- The VM transcription server is running at `http://192.168.1.24:8765`.
- The Pi is using VM-hosted STT successfully.
- Measured Pi timings after the STT move:
  - `stt`: about `1.84s` to `1.95s`
  - `llm`: about `3.77s` for an open-ended joke prompt
  - `tts`: about `3.90s` for the longer joke response

## Immediate next work

1. Tighten Ollama responses for speed.
   - Update `src/assistant/llm.py`
   - Add generation options such as lower temperature and a shorter output cap
   - Aim for shorter default replies so both `llm` and `tts` times fall

2. Turn the VM transcription server into a `systemd` service.
   - Create a service unit for `.venv/bin/python -m assistant.server`
   - Ensure it starts on boot
   - Verify with `systemctl status`, `ss -tulnp | grep 8765`, and `/health`

3. Clean the repository.
   - Remove or isolate unrelated files:
     - `node_modules/`
     - `package.json`
     - `package-lock.json`
     - nested `home-assistant/`
     - generated `src/home_assistant_device.egg-info/`
   - Expand `.gitignore` accordingly

## Recommended order

1. LLM response tuning
2. VM transcription service via `systemd`
3. Repo cleanup

## Notes for next session

- The biggest fixed latency problem was solved by moving STT to the VM.
- The next latency gains are likely from shorter LLM answers, not more STT tuning.
- Live data questions currently return a safe fallback instead of hallucinated answers.
- Timezone support is a small alias map, not a full place resolver.
