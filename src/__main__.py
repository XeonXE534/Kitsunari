from textual.app import App
from .screens.home import KitsunariHome
from backend.backend_v2 import AnimeBackend

class KitsunariTUI(App):
    def on_mount(self):
        backend = AnimeBackend()
        self.push_screen(KitsunariHome(backend))

app = KitsunariTUI()

if __name__ == "__main__":
    app.run()
