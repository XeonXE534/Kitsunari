from textual.app import App
from .screens.home import KitsunariHome

class KitsunariTUI(App):
    def on_mount(self):
        self.push_screen(KitsunariHome())

if __name__ == "__main__":
    KitsunariTUI().run()
