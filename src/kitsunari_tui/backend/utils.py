import re
import html

def clean_html(raw: str) -> str:
    text = re.sub(r'<.*?>', '', raw).strip()
    return html.unescape(text)