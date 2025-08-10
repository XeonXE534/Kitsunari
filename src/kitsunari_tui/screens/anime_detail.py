from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.app import ComposeResult
from anipy_api.anime import Anime

class AnimeDetailScreen(Screen):
    def __init__(self, anime: Anime, synopsis: str):
        super().__init__()
        self.anime = anime
        self.synopsis = synopsis

    def compose(self) -> ComposeResult:
        info = self.anime.get_info()
        yield Static(info.name, classes="detail-title")
        yield Static(self.synopsis, classes="detail-synopsis")
        yield Footer()

    def on_key(self, event):
        # Simple back key
        if event.key.lower() in ["b", "escape"]:
            self.app.pop_screen()
