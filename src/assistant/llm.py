import requests

from . import config


def ask(text):
    prompt = (
        "You are a voice assistant for a Raspberry Pi device. "
        "Reply naturally, clearly, and briefly. "
        "Keep replies to one short sentence unless the user asks for more. "
        "Do not use markdown or bullet points.\n\n"
        f"User: {text}\nAssistant:"
    )
    try:
        response = requests.post(
            config.OLLAMA_URL,
            json={
                "model": config.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "keep_alive": "30m",
            },
            timeout=config.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip() or "I did not get a useful reply."
    except requests.RequestException as exc:
        print("Ollama error:", exc)
        return "I cannot reach the language model right now."
