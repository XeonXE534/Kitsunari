from .search import SearchScreen
from textual.screen import Screen
from textual.app import ComposeResult
from textual.containers import Vertical
from ..backend.backend_v2 import AnimeBackend
from .continue_watching import ContinueWatchingScreen
from textual.widgets import Static, Footer, Header, Button

class KitsunariHome(Screen):
    CSS_PATH = "../css/home_styles.css"
    banner = """
██╗  ██╗██╗████████╗███████╗██╗   ██╗███╗   ██╗ █████╗ ██████╗ ██╗
██║ ██╔╝██║╚══██╔══╝██╔════╝██║   ██║████╗  ██║██╔══██╗██╔══██╗██║
█████╔╝ ██║   ██║   ███████╗██║   ██║██╔██╗ ██║███████║██████╔╝██║
██╔═██╗ ██║   ██║   ╚════██║██║   ██║██║╚██╗██║██╔══██║██╔══██╗██║
██║  ██╗██║   ██║   ███████║╚██████╔╝██║ ╚████║██║  ██║██║  ██║██║
╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
"""

    BINDINGS = [
        ("escape", "quit_app", "Quit"),
        ("s", "search", "Search Anime"),
        ("c", "continue", "Continue Watching"),
        #("t", "settings", "Settings"),
    ]

    def __init__(self, backend: AnimeBackend, **kwargs):
        super().__init__(**kwargs)
        self.backend = backend

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Static(self.banner, classes="title")
        yield Static("Modern TUI Anime Streaming", classes="subtitle")
        yield Vertical(
            Button("Search Anime", id="search"),
            Button("Continue Watching", id="continue"),
            #Button("Settings", id="settings"),
            Button("Quit", id="quit"),
            classes="menu"
        )
        yield Static("v1.5.1", classes="footer-note")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "search":
            self.app.push_screen(SearchScreen())

        elif button_id == "continue":
            self.app.push_screen(ContinueWatchingScreen(self.backend))

        #elif button_id == "settings":
            # TODO: Implement Settings screen
        #    pass

        elif button_id == "quit":
            self.app.exit()

    def action_quit_app(self) -> None:
        self.app.exit()

    def action_search(self) -> None:
        self.app.push_screen(SearchScreen())

    def action_continue(self) -> None:
        self.app.push_screen(ContinueWatchingScreen(self.backend))

    #def action_settings(self) -> None:
        # TODO: Implement Settings screen
    #    pass
