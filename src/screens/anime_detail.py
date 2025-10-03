from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.app import ComposeResult
from anipy_api.anime import Anime

class AnimeDetailScreen(Screen):
    BINDINGS = [
        ('escape', 'go_back', 'Go Back')
    ]
    CSS_PATH = '../css/details_styles.css'

    def __init__(self, anime: Anime, synopsis: str):
        super().__init__()
        self.anime = anime
        self.synopsis = synopsis

    def compose(self) -> ComposeResult:
        info = self.anime.get_info()
        yield Static(info.name, classes='detail-title')
        yield Static(self.synopsis, classes='detail-synopsis')
        yield Footer()

    def action_go_back(self):
        self.app.pop_screen()