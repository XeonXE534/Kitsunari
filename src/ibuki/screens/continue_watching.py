from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Vertical
from ..backend.backend_v2 import AnimeBackend
from textual.widgets import Static, Footer, Header, Button

class ContinueWatchingScreen(Screen):
    CSS_PATH = "../css/home_styles.css"
    BINDINGS = [("escape", "quit_app", "Quit")]

    def __init__(self, backend: AnimeBackend, **kwargs):
        super().__init__(**kwargs)
        self.backend = backend

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Static("Continue Watching", classes="title")

        cont_list = self.backend.get_continue_watching_list(limit=10)
        if not cont_list:
            yield Static("No anime to continue watching.", classes="subtitle")

        else:
            buttons = []
            for entry in cont_list:
                percent = entry["progress_percent"]
                btn_text = f"{entry['anime_name']} EP{entry['episode']} ({percent}%)"
                buttons.append(Button(btn_text, id=entry["anime_id"]))
            yield Vertical(*buttons, classes="menu")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        anime_id = event.button.id
        self.backend.resume_anime(anime_id)
        self.app.pop_screen()

    def action_quit_app(self) -> None:
        self.app.pop_screen()