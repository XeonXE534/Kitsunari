from textual.screen import Screen
from textual.app import ComposeResult
from ..backend.backend_v3 import AnimeBackend
from textual.widgets import ListView, ListItem, Static, Footer

class EpisodeDetailScreen(Screen):
    BINDINGS = [
        ("escape", "go_back", "Go Back"),
        ("p", "play_selected", "Play Episode"),
    ]
    CSS_PATH = '../css/episode_styles.css'

    def __init__(self, anime):
        super().__init__()
        self.anime = anime
        self.backend = AnimeBackend()
        self.episodes = []

    def compose(self) -> ComposeResult:
        yield Static(self.anime.name, id="title")
        yield ListView(id="episode_list")
        yield Footer()

    def on_mount(self):
        episode_list = self.query_one("#episode_list", ListView)
        self.episodes = self.backend.get_episodes(self.anime)

        if not self.episodes:
            episode_list.append(ListItem(Static("No episodes found.")))
            return

        for idx, ep_num in enumerate(self.episodes):
            label = f"Ep {ep_num}"
            item = ListItem(Static(label))
            item.index = idx
            episode_list.append(item)

    def action_go_back(self):
        self.app.pop_screen()

    def action_play_selected(self) -> None:
        episode_list = self.query_one("#episode_list", ListView)
        selected_index = episode_list.index

        if selected_index is None or selected_index < 0:
            return

        selected = list(episode_list.children)[selected_index]
        ep_index = getattr(selected, "index", None)
        if ep_index is None:
            return

        episode_number = self.episodes[ep_index]
        self.backend.play_episode(self.anime, episode_number)
