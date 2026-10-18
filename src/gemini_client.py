import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.8-flash"


def summarize(text: str) -> str:
    interaction = _client.interactions.create(
        model=MODEL,
        input=f"Summarize in one sentence:\n\n{text}",
    )
    return interaction.output_text


def usage_info(text: str) -> dict:
    interaction = _client.interactions.create(
        model=MODEL,
        input=text,
    )
    return {
        "text": interaction.output_text,
        "prompt_tokens": interaction.usage.total_input_tokens,
        "output_tokens": interaction.usage.total_output_tokens,
    }