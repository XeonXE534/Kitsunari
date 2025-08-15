```python
import asyncio
import os
from pygments.styles.dracula import *
import rich
from textual.app import App, ComposeResult
from textual.widgets import Input, Static, ListView, ListItem, Header, Footer, Button
from textual.message import Message
from backend.anipy_client import Anime, AllAnimeProvider, LanguageTypeEnum, clean_html

class AnimeSelected(Message):
    def __init__(self, anime: Anime):
        self.anime = anime
        super().__init__()

class KitsunariApp(App):
    CSS = """

    #results {
        height: 10;
        border: solid green;
    }
    #details {
        border: solid yellow;
        height: 6;
    }

    """
    BINDINGS = [
        ('l', 'quit', 'Toggle Dark Mode'),
    ]

    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        yield Input(placeholder="Search anime...", id="search")
        yield ListView(id="results")
        yield Static("", id="details")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.value.strip()
        if not query:
            return

        provider = AllAnimeProvider()

        # Run blocking search off main thread
        results = await asyncio.to_thread(provider.get_search, query)

        list_view = self.query_one("#results", ListView)
        await list_view.clear()

        self.anime_map = {}

        if not results:
            await list_view.append(ListItem(Static("No results found")))
            return

        for res in results:
            # Run blocking from_search_result off main thread too
            anime = await asyncio.to_thread(Anime.from_search_result, provider, res)
            info = anime.get_info()
            self.anime_map[info.name] = anime
            await list_view.append(ListItem(Static(info.name)))

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected_item = event.item
        if not selected_item.children:
            return

        title = selected_item.children[0].renderable
        anime = self.anime_map.get(title)
        if not anime:
            return

        # Run blocking get_episodes off main thread
        episodes = await asyncio.to_thread(anime.get_episodes, lang=LanguageTypeEnum.SUB)
        info = anime.get_info()
        details = (
            f"Title: {info.name}\n"
            f"Episodes: {len(episodes)}\n"
            f"Synopsis: {clean_html(info.synopsis or '')}"
        )
        self.query_one("#details", Static).update(details)

if __name__ == "__main__":
    KitsunariApp().run()
```

```python
from textual import on
from textual.app import App
from textual.widgets import Input, Static, ListView, ListItem, Header, Footer, Button
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.message import Message
from backend.anipy_client import Anime, AllAnimeProvider, LanguageTypeEnum, clean_html

class Box(Static):
    @on(Button.Pressed)
    def cheese(self):
        ...

    def compose(self):
        yield Button('button1',
                     variant='primary',
                     id='a1')

        yield Button('button2',
                     variant='error',
                     id='a2')

        yield Button('button3',
                     variant='success',
                     id='a3')

class KitsunariApp(App):
    BINDINGS = [
        
    ]

    CSS_PATH = 'search_styles.css'

    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        with ScrollableContainer(id='boxes'):
            for i in range(10):
                yield Box()


if __name__ == "__main__":
    KitsunariApp().run()
```

```Python    
    if episodes == list(range(1, len(episodes) + 1)):
        print(f"Episodes: 1-{len(episodes)}")
    else:
        print(f"Episodes: {episodes}")
```

```python
import argparse
import sys

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
```
```css
#synopsis_display {
    height: auto;
    max-height: 10fr;
    overflow: auto;

    color: white;
    background: #1e1e1e;
    padding: 1;
    border: solid white;
    border-title-align: left;
    border-title-color: cyan;

    text-style: italic;
}

#search_input {

}
```

```CSS
Box {
    layout: horizontal;
    background: $boost;
    margin: 1;
    padding: 1;
    height: 5;
}

#a1 {
    dock: left;
}

#a2 {
    dock: left;
    display: none;
}

#a3 {
    dock:right;
}
```