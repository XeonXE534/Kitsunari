from textual.screen import Screen
from textual.widgets import Input, ListView, ListItem, Static, Footer
from textual.app import ComposeResult
from ..backend.backend import AnimeBackend as backend
from ..backend.utils import clean_html
from .anime_detail import AnimeDetailScreen

class SearchScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for anime :3", id="search_input")
        yield ListView(id="search_results")
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.input.value.strip()
        list_view = self.query_one("#search_results", ListView)
        list_view.clear()

        if not query:
            list_view.append(ListItem(Static("Anime not found! :/")))
            return

        anime_list = backend().get_anime_by_query(query)
        if not anime_list:
            list_view.append(ListItem(Static("Anime not found! :/")))
            return

        for idx, anime in enumerate(anime_list):
            if anime is not None and hasattr(anime, "get_info"):
                info = anime.get_info()
            else:
                list_view.append(ListItem(Static("Anime not found! :/")))
                return

            title = info.name
            synopsis = clean_html(info.synopsis)
            item_widget = Static(title)

            list_item = ListItem(item_widget)
            list_item.index = idx
            list_item.synopsis = synopsis
            list_item.anime = anime
            list_view.append(list_item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        selected = event.item
        anime = getattr(selected, "anime", None)
        synopsis = getattr(selected, "synopsis", "No synopsis available.")

        try:
            synopsis_display = self.query_one("#synopsis_display", Static)
            synopsis_display.update(synopsis)
        except LookupError:
            print("[Warning] #synopsis_display widget not found.")

        if anime:
            self.app.push_screen(AnimeDetailScreen(anime, synopsis))
        else:
            print("[Error] Selected item has no anime data attached.")
