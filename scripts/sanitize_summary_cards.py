"""Remove email addresses before publishing generated profile cards."""

from html import unescape
from pathlib import Path
import re
import xml.etree.ElementTree as ET


EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
TEXT = re.compile(r"<text\b[^>]*>.*?</text>", re.DOTALL)


def sanitize(svg):
    def remove_email(match):
        text = "".join(ET.fromstring(match.group()).itertext())
        return "" if EMAIL.search(unescape(text)) else match.group()

    cleaned = TEXT.sub(remove_email, svg)
    ET.fromstring(cleaned)
    if EMAIL.search(unescape(cleaned)):
        raise ValueError("Email address remains in generated SVG")
    return cleaned


if __name__ == "__main__":
    for path in Path("profile-summary-card-output").rglob("*.svg"):
        original = path.read_text()
        cleaned = sanitize(original)
        if cleaned != original:
            path.write_text(cleaned)
