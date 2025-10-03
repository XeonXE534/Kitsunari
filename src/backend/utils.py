import html
import re

def clean_html(raw: str | None) -> str:
    if not raw:
        return "No synopsis available."
    text = re.sub(r'<.*?>', '', raw).strip()
    return html.unescape(text)
