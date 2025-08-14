from textual.app import App
from .screens.home import KitsunariHome
import importlib.resources as pkg_resources
from . import css

class KitsunariTUI(App):
    CSS_PATH = str(pkg_resources.files(css).joinpath("home_styles.css"))

    def on_mount(self):
        self.push_screen(KitsunariHome())

def run():
    KitsunariTUI().run()

if __name__ == "__main__":
    run()
