from textual.screen import Screen
from textual.app import ComposeResult
from ..backend.backend_v3 import AnimeBackend
from textual.widgets import ListView, ListItem, Static, Footer

class EpisodeDetailScreen(Screen):
    BINDINGS = [
        ("escape", "go_back", "Go Back"),
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

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle when user clicks or presses enter on an episode"""
        selected_item = event.item
        ep_index = getattr(selected_item, "index", None)

        if ep_index is None:
            return

        episode_number = self.episodes[ep_index]

        stream = self.backend.get_episode_stream(
            self.anime,
            episode_number,
            self.backend.global_quality
        )

        if not stream:
            self.app.notify("[Error] No stream available for this episode :(", severity="error", timeout=3)
            return

        anime_id = getattr(self.anime, "identifier", str(id(self.anime)))
        entry = self.backend.watch_history.get_entry(anime_id)

        start_time = 0
        if entry and entry["episode"] == episode_number:
            start_time = entry["timestamp"]

        self.backend.play_episode(self.anime, episode_number, stream, start_time)

    def action_go_back(self):
        self.app.pop_screen()