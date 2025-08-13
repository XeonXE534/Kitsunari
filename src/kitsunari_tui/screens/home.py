from textual.screen import Screen
from .search import SearchScreen
from textual.widgets import Static, Footer, Button
from textual.app import ComposeResult

class KitsunariHome(Screen):
    BINDINGS = [
        ('q', 'exit', 'exit'),
        ('s', 'search', 'Search for anime'),
    ]
    CSS_PATH = '../css/home_styles.css'

    def compose(self) -> ComposeResult:
        yield Heading()
        yield Button('Search', variant='success', id='search_btn')
        yield Button('Exit', variant='error', id='exit_btn')
        yield Footer()

    def action_search(self):
        self.app.push_screen(SearchScreen())

    def action_exit(self):
        self.app.exit()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'search_btn':
            self.action_search()
        elif event.button.id == 'exit_btn':
            self.action_exit()

class Heading(Static):
    def compose(self):
        yield Static('Kitsunari TUI', classes='heading')
        yield Static('Place Holder Text :3', classes='subheading')