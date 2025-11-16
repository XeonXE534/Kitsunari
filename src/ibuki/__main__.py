from textual.app import App
from .screens.home import IbukiHome
from .backend.backend_v3 import AnimeBackend

class Ibuki(App):
    def on_mount(self):
        backend = AnimeBackend()
        self.push_screen(IbukiHome(backend))

app = Ibuki()

def run():
    app.run()

if __name__ == "__main__":
    run()