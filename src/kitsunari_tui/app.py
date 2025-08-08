from textual.app import App, ComposeResult
from textual.widgets import Input, Static, ListView, ListItem, Header, Footer, Button
from textual.message import Message
from backend.anipy_client import Anime, AllAnimeProvider, LanguageTypeEnum, clean_html

class Box(Static):
    def compose(self) -> ComposeResult:
        yield Button('button1', variant='primary')
        yield Button('button2', variant='error')

class KitsunariApp(App):

    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        yield Box()

if __name__ == "__main__":
    KitsunariApp().run()
