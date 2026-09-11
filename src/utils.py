import hashlib
import re
from pathlib import Path


def file_hash(path: Path) -> str:
    """Return an MD5 hash for the file contents."""

    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def extract_json(text: str) -> str:
    """Extract a JSON object or array from model output."""

    text = text.strip()

    text = re.sub(
        r"^```[a-z]*\n?",
        "",
        text,
    )

    text = re.sub(
        r"\n?```$",
        "",
        text,
    )

    text = text.strip()

    for pattern in (
        r"(\{[\s\S]*\})",
        r"(\[[\s\S]*\])",
    ):
        match = re.search(pattern, text)

        if match:
            return match.group(1)

    return text
