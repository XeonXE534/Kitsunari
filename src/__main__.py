from textual.app import App
from .screens.home import KitsunariHome

class KitsunariTUI(App):
    def on_mount(self):
        self.push_screen(KitsunariHome())

app = KitsunariTUI()

if __name__ == "__main__":
    app.run()
