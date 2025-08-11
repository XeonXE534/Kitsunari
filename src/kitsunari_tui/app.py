# src/kitsunari_tui/app.py
import argparse
import sys
from textual.app import App
from .screens.search import SearchScreen
from .backend.backend import AnimeBackend

backend = AnimeBackend()

class KitsunariTUI(App):
    def on_mount(self):
        self.push_screen(SearchScreen())

def dev_mode(query: str):
    logger = backend.logger if hasattr(backend, "logger") else None
    if logger:
        logger.info(f"[DEV MODE] Searching for: {query}")

    results = backend.get_anime_by_query(query)
    if isinstance(results, str):
        print(results)
        sys.exit(1)

    anime = results[0]
    episodes = backend.get_episodes(anime)
    if not episodes:
        print("No episodes found.")
        sys.exit(1)

    first_ep = episodes[0]
    print(f"[DEV MODE] Playing: {anime.name} Episode {first_ep}")
    backend.play_episode(anime, first_ep, quality="worst")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", action="store_true", help="Run in dev mode without TUI")
    parser.add_argument("-q", "--query", default="Blue Archive", help="Anime to search in dev mode")
    args = parser.parse_args()

    if args.dev:
        dev_mode(args.query)
    else:
        app = KitsunariTUI()
        app.run()

if __name__ == "__main__":
    main()
