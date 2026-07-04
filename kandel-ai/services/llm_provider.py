"""
KANDEL AI - LLM Provider (Groq only)
Designed by Kandel Sanjaya

Single abstraction so the rest of the app never talks to the Groq SDK directly.
If the configured model has been deprecated/retired, we transparently retry
with the next model in GROQ_MODEL_FALLBACKS.
"""
from groq import Groq
from config.settings import settings

_client = None


def get_client():
    global _client
    if _client is None:
        if not settings.GROQ_API_KEY:
            raise RuntimeError(
                "GROQ_API_KEY is missing. Add it to your .env file before chatting."
            )
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client


def _candidate_models():
    models = [settings.GROQ_MODEL] + [
        m for m in settings.GROQ_MODEL_FALLBACKS if m != settings.GROQ_MODEL
    ]
    return models


def chat_completion(messages: list, temperature: float = 0.7, max_tokens: int = 1024):
    """Non-streaming completion, with automatic model fallback."""
    client = get_client()
    last_err = None
    for model in _candidate_models():
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content, model
        except Exception as e:  # deprecated model / rate limit / etc.
            last_err = e
            continue
    raise RuntimeError(f"All Groq models failed. Last error: {last_err}")


def stream_completion(messages: list, temperature: float = 0.7, max_tokens: int = 1024):
    """Generator yielding text chunks, with automatic model fallback."""
    client = get_client()
    last_err = None
    for model in _candidate_models():
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )

            def _gen():
                for chunk in stream:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta

            return _gen(), model
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"All Groq models failed. Last error: {last_err}")
