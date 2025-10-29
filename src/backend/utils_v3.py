import html
import re
import json
from pathlib import Path

PROGRESS_FILE = Path("kitsunari_progress.json").expanduser()

#utils v3
def clean_html(raw: str | None) -> str:
    if not raw:
        return "No synopsis available :("

    text = re.sub(r'<.*?>', '', raw).strip()
    return html.unescape(text)

