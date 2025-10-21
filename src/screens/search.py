from textual.screen import Screen
from textual.widgets import Input, ListView, ListItem, Static, Footer
from textual.app import ComposeResult
from ..backend.backend_v2 import AnimeBackend as backend
from ..backend.utils import clean_html
from .anime_detail import AnimeDetailScreen
from .episode_view import EpisodeDetailScreen

class SearchScreen(Screen):
    BINDINGS = [
        ('escape', 'go_back', 'Go Back'),
        ('e', 'episodes', 'Episodes'),
        ('s', 'synopsis', 'Synopsis')
    ]
    CSS_PATH = '../css/search_styles.css'

    def compose(self) -> ComposeResult:
        yield Input(placeholder='Search for anime :3', id='search_input')
        yield ListView(id='search_results')
        yield Static('', id='synopsis_display')
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        query = event.input.value.strip()
        list_view = self.query_one('#search_results', ListView)
        list_view.clear()

        if not query:
            list_view.append(ListItem(Static('Anime not found! :/')))
            return

        anime_list = backend().get_anime_by_query(query)
        if not anime_list:
            list_view.append(ListItem(Static('Anime not found! :/')))
            return

        for idx, anime in enumerate(anime_list):
            if anime is not None and hasattr(anime, 'get_info'):
                info = anime.get_info()
            else:
                list_view.append(ListItem(Static('Anime not found! :/')))
                return

            title = info.name
            synopsis = clean_html(info.synopsis)
            item_widget = Static(title)

            list_item = ListItem(item_widget)
            list_item.index = idx
            list_item.synopsis = synopsis
            list_item.anime = anime
            list_view.append(list_item)

    def action_synopsis(self):
        list_view = self.query_one('#search_results', ListView)
        selected_index = list_view.index
        if selected_index is None or selected_index < 0:
            print('[Error] No anime selected.')
            return

        children = list(list_view.children)
        if selected_index >= len(children):
            print('[Error] Selected index out of range.')
            return

        selected = children[selected_index]
        anime = getattr(selected, 'anime', None)
        synopsis = getattr(selected, 'synopsis', 'No synopsis available.')

        if anime:
            self.app.push_screen(AnimeDetailScreen(anime, synopsis))
        else:
            print('[Error] Selected item has no anime data attached.')

    def action_go_back(self):
        self.app.pop_screen()

    def action_episodes(self):
        list_view = self.query_one('#search_results', ListView)
        selected_index = list_view.index

        if selected_index is None or selected_index < 0:
            print("[Error] No anime selected to show episodes for.")
            return

        children = list(list_view.children)
        if selected_index >= len(children):
            print("[Error] Selected index out of range.")
            return

        selected_item = children[selected_index]
        anime = getattr(selected_item, 'anime', None)
        if anime is None:
            print("[Error] Selected item has no anime data attached.")
            return

        self.app.push_screen(EpisodeDetailScreen(anime))
