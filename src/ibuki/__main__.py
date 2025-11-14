from textual.app import App
from .screens.home import IbukiHome
from .backend.stream import AnimeBackend

class Ibuki(App):
    def on_mount(self):
        backend = AnimeBackend()
        self.push_screen(IbukiHome(backend))

def run():
    app = Ibuki()
    app.run()

if __name__ == "__main__":
    run()