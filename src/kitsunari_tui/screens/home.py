from textual.screen import Screen
from textual.widgets import Static, Footer, Header, Button
from textual.containers import Vertical
from textual.app import ComposeResult
from .search import SearchScreen

class KitsunariHome(Screen):
    CSS_PATH = "../css/home_styles.css"

    BINDINGS = [
        ("q", "quit_app", "Quit"),
        ("s", "search", "Search Anime"),
        ("c", "continue", "Continue Watching"),
        ("t", "settings", "Settings"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Static("Kitsunari | キツナーリ", classes="title")
        yield Static("Modern TUI Anime Streaming", classes="subtitle")
        yield Vertical(
            Button("Search Anime", id="search"),
            Button("Continue Watching", id="continue"),
            Button("Settings", id="settings"),
            Button("Quit", id="quit"),
            classes="menu"
        )
        yield Static("v1.0.0 — Powered by anipy-api + Textual", classes="footer-note")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "search":
            self.app.push_screen(SearchScreen())
        elif button_id == "continue":
            # TODO: Implement Continue Watching screen
            pass
        elif button_id == "settings":
            # TODO: Implement Settings screen
            pass
        elif button_id == "quit":
            self.app.exit()

    def action_quit_app(self) -> None:
        self.app.exit()

    def action_search(self) -> None:
        self.app.push_screen(SearchScreen())

    def action_continue(self) -> None:
        # TODO: Implement Continue Watching screen
        pass

    def action_settings(self) -> None:
        # TODO: Implement Settings screen
        pass
