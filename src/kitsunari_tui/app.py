from textual.app import App
from .screens.search import SearchScreen

class Kitsunari(App):
    CSS_PATH = 'Style.css'

    def on_mount(self):
        self.push_screen(SearchScreen())

if __name__ == "__main__":
    Kitsunari().run()
