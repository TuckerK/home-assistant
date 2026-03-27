# Status

## Working now

- Pi can reach Ollama on the VM at `192.168.1.24:11434`.
- Pi can reach the VM transcription server at `192.168.1.24:8765`.
- Time intent supports a small built-in timezone alias map including Shanghai.
- Live-data requests like weather are blocked with an explicit fallback instead of fake answers.
- Recording shutdown noise from `arecord` has been suppressed.

## Measured behavior

Before VM-hosted STT:

- `stt` on Pi was consistently about `4.3s` to `4.4s`
- `llm` varied from near-zero for local intents to several seconds for open-ended prompts
- `tts` scaled mostly with response length

Reason for moving STT:

- Pi-side Whisper was the largest fixed delay
- Pi should handle hardware and playback, not model inference

## Known gaps

- The new VM-hosted STT path still needs fresh Pi timing numbers after pull/update.
- The transcription server is running manually, not yet as a `systemd` service.
- The repo contains unrelated untracked Node artifacts:
  - `node_modules/`
  - `package.json`
  - `package-lock.json`
  - nested `home-assistant/`
- The LLM can still be slow on long/open-ended prompts. Limiting output tokens is the next easy latency improvement.
- The timezone alias map is intentionally small and not a general geocoder.

## Recommended next steps

1. Pull the latest changes on the Pi and measure the new `stt` time.
2. Turn the VM transcription server into a `systemd` service.
3. Clean the repo so only the Python project remains.
4. Add stricter Ollama generation limits for shorter responses.
5. Optionally collapse STT and LLM into one VM endpoint to simplify the Pi client.
