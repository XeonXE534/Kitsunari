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

def write_progress(title: str, episode: int) -> None:
    data = {}
    if PROGRESS_FILE.exists():
        try:
            data = json.loads(PROGRESS_FILE.read_text())

        except Exception:
            data = {}

    data[title] = {
        "episode": episode
    }

    PROGRESS_FILE.write_text(json.dumps(data, indent=2))

def read_progress() -> dict:
    if not PROGRESS_FILE.exists():
        return {}
    try:
        return json.loads(PROGRESS_FILE.read_text())

    except Exception:
        return {}