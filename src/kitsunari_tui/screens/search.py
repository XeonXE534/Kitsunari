from textual.screen import Screen
from textual.widgets import Input, ListView, ListItem, Static, Footer
from textual.app import ComposeResult
from ..backend.backend_v3 import AnimeBackend
from ..backend.utils import clean_html
from .anime_detail import AnimeDetailScreen
from .episode_view import EpisodeDetailScreen

class SearchScreen(Screen):
    BINDINGS = [
        ('escape', 'go_back', 'Go Back'),
        ('left', 'previous_page', 'Previous Page'),
        ('right', 'next_page', 'Next Page'),
        ('e', 'episodes', 'Episodes'),
        ('s', 'synopsis', 'Synopsis')
    ]
    CSS_PATH = '../css/search_styles.css'

    def __init__(self):
        super().__init__()
        self.backend = AnimeBackend()
        self.current_query: str = ""

    def compose(self) -> ComposeResult:
        yield Input(placeholder='Search for anime :3', id='search_input')
        yield ListView(id='search_results')
        yield Static('', id='synopsis_display')
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.input.value.strip()
        self.current_query = query
        self._display_search_results(query, reset_page=True)

    def _display_search_results(self, query: str, reset_page: bool = False):
        if not query:
            self._show_no_results()
            return

        anime_list = self.backend.get_anime_by_query(query, next_page=not reset_page)
        if not anime_list:
            self._show_no_results()
            return

        list_view = self.query_one('#search_results', ListView)
        list_view.clear()

        for idx, anime in enumerate(anime_list):
            if anime is None or not hasattr(anime, 'get_info'):
                continue

            info = anime.get_info()
            title = info.name
            synopsis = clean_html(info.synopsis)
            item_widget = Static(title)
            list_item = ListItem(item_widget)
            list_item.index = idx
            list_item.synopsis = synopsis
            list_item.anime = anime
            list_view.append(list_item)

    def _show_no_results(self):
        list_view = self.query_one('#search_results', ListView)
        list_view.clear()
        list_view.append(ListItem(Static('Anime not found! :/')))

    def action_synopsis(self):
        list_view = self.query_one('#search_results', ListView)
        idx = list_view.index

        if idx is None or idx < 0:
            print("[Error] No anime selected to show synopsis for.")
            return

        children = list(list_view.children)

        if idx >= len(children):
            print("[Error] Selected index out of range.")
            return

        item = children[idx]
        anime = getattr(item, 'anime', None)
        synopsis = getattr(item, 'synopsis', 'No synopsis available.')

        if anime:
            self.app.push_screen(AnimeDetailScreen(anime, synopsis))

        else:
            print('[Error] Selected item has no anime data attached.')

    def action_episodes(self):
        list_view = self.query_one('#search_results', ListView)
        idx = list_view.index

        if idx is None or idx < 0:
            print("[Error] No anime selected to show episodes for.")
            return
        children = list(list_view.children)

        if idx >= len(children):
            print("[Error] Selected index out of range.")
            return

        item = children[idx]
        anime = getattr(item, 'anime', None)
        if anime:
            self.app.push_screen(EpisodeDetailScreen(anime))

        else:
            print("[Error] Selected item has no anime data attached.")

    def action_next_page(self):
        if not self.current_query:
            return

        if self.backend.is_last_page(self.current_query):
            print("[Info] No more pages to show.")
            return

        self._display_search_results(self.current_query, reset_page=False)

    def action_previous_page(self):
        if not self.current_query:
            return

        current_page = self.backend.current_page.get(self.current_query, 0)
        if current_page <= 0:
            print("[Info] Already at first page.")
            return

        self.backend.current_page[self.current_query] = current_page - 2
        self._display_search_results(self.current_query, reset_page=False)

    def action_go_back(self):
        self.app.pop_screen()
