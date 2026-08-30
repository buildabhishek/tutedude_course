"""
groq_chatbot.py

The actual chatbot logic lives here instead of inline in main.py, so both the
notebook (for testing) and the FastAPI app can import the same function
instead of two copies of the same code drifting apart.
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


GROQ_MODEL = "openai/gpt-oss-120b"


_client = None


def get_client() -> Groq:
    """Lazily create the Groq client so importing this file doesn't blow up
    just because GROQ_API_KEY isn't set yet - it only fails when something
    actually tries to use it."""
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to a .env file or export it "
                "before running this."
            )
        _client = Groq(api_key=api_key)
    return _client


def groq_chat(prompt: str, system: str = "You are a helpful assistant.") -> str:
    """Send one prompt to Groq and return just the text back. Kept as a
    single function since that's basically all Task 2 asked for - system +
    user message in, a plain string answer out."""
    client = get_client()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(groq_chat("Explain what Groq is in two lines."))
