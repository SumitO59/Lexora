import json

from langchain_ollama import OllamaLLM

from .utils import extract_json


SUMMARY_PROMPT = """Summarize the following document in 3-5 sentences. Be concise and factual.

Text:
{text}

Summary:"""


ENTITIES_PROMPT = """Extract named entities from the text. Return ONLY a JSON object, no explanation.
Format: {{"people":["..."],"organizations":["..."],"locations":["..."],"dates":["..."]}}

Text:
{text}

JSON:"""


NUMBERS_PROMPT = """Extract important numbers, statistics, percentages, or monetary values from the text.
Return ONLY a JSON array, no explanation.
Format: [{{"value":"42%","context":"growth rate"}},{{"value":"$1.2M","context":"revenue"}}]
If none found, return: []

Text:
{text}

JSON array:"""


def analyze_document(
    llm: OllamaLLM,
    full_text: str,
) -> dict:
    """Run summary, entity extraction, and key-number extraction."""

    text = full_text[:1500].strip()

    try:
        summary = (
            llm.invoke(
                SUMMARY_PROMPT.format(text=text)
            ).strip()
            or "No summary generated."
        )
    except Exception as e:
        summary = f"(Summary failed: {e})"

    entities = {
        "people": [],
        "organizations": [],
        "locations": [],
        "dates": [],
    }

    try:
        raw = llm.invoke(
            ENTITIES_PROMPT.format(text=text)
        )

        clean = extract_json(raw)

        if clean:
            entities = json.loads(clean)

    except Exception:
        pass

    key_numbers = []

    try:
        raw = llm.invoke(
            NUMBERS_PROMPT.format(text=text)
        )

        clean = extract_json(raw)

        if clean:
            key_numbers = json.loads(clean)

    except Exception:
        pass

    return {
        "summary": summary,
        "entities": entities,
        "key_numbers": key_numbers,
    }
