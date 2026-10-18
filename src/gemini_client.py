import os
import json
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

def extract_info(text: str) -> dict:
    prompt = f"""
    Extract the name, age, and city from the text below.
    Return ONLY a valid JSON object with keys: "name", "age", "city".
    If a field is missing, use null.
    
    Text: {text}
    """
    
    interaction = _client.interactions.create(
        model=MODEL,
        input=prompt,
        response_format={"type": "json_object"} # Force JSON output!
    )
    
    try:
        return json.loads(interaction.output_text)
    except json.JSONDecodeError:
        raise ValueError("AI did not return valid JSON")

def get_embeddings(texts: list[str]) -> list[list[float]]:
    response = _client.models.embed_content(
        model="gemini-embedding-2",
        contents=texts,
    )
    return [e.values for e in response.embeddings]