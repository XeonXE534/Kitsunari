from pathlib import Path
from anipy_api.provider.providers.allanime_provider import AllAnimeProvider
from anipy_api.anime import Anime
from anipy_api.provider import LanguageTypeEnum, ProviderStream
from anipy_api.player import get_player
from src.backend.db import init_db, save_episodes, load_episodes, save_anime

# Initialize DB once at startup
init_db()

class AnimeBackend:
    def __init__(self):
        self.provider = AllAnimeProvider()
        self._cache: dict = {}
        self._episodes_cache: dict = {}
        self._episodes_fetching: dict = {}

    # --------------------
    # Anime search
    # --------------------
    def get_anime_by_query(self, query: str) -> list[Anime]:
        try:
            results = self.provider.get_search(query)
            if not results:
                return []

            anime_list = []
            for idx, r in enumerate(results):
                key = getattr(r, "id", None) or idx

                if key in self._cache:
                    anime = self._cache[key]
                else:
                    anime = Anime.from_search_result(self.provider, r)
                    self._cache[key] = anime
                    # Cache metadata in DB
                    save_anime(key, anime.title, {"provider": "AllAnimeProvider"})

                anime_list.append(anime)

            return anime_list

        except Exception:
            return []

    # --------------------
    # Episodes
    # --------------------
    def get_episodes(self, anime: Anime) -> list[int | float]:
        anime_id = getattr(anime, "id", None) or id(anime)

        # Check in-memory first
        if anime_id in self._episodes_cache:
            return self._episodes_cache[anime_id]

        # Check persistent DB cache
        episodes = load_episodes(anime_id)
        if episodes:
            ep_numbers = [ep['number'] for ep in episodes]
            self._episodes_cache[anime_id] = ep_numbers
            return ep_numbers

        # Fetch from provider
        episodes_list = anime.get_episodes(lang=LanguageTypeEnum.SUB)

        # Cache episodes in DB if threshold is met
        episodes_for_db = [{"number": n} for n in episodes_list]
        save_episodes(anime_id, episodes_for_db)

        # Keep in-memory cache too
        self._episodes_cache[anime_id] = episodes_list

        return episodes_list

    # --------------------
    # Stream
    # --------------------
    def get_episode_stream(self, anime: Anime, episode: int, quality: int) -> ProviderStream | None:
        try:
            stream = anime.get_video(
                episode=episode,
                lang=LanguageTypeEnum.SUB,
                preferred_quality=quality
            )
            return stream
        except Exception:
            return None

    # --------------------
    # Play episodes
    # --------------------
    def play_episode(self, anime: Anime, episode: int, quality: int = 720):
        def on_play(anime: Anime, stream: ProviderStream) -> None:
            pass

        try:
            stream = self.get_episode_stream(anime, episode, quality)
            if not stream:
                return

            mpv_player = get_player(
                Path("mpv"),
                extra_args=["--fs"],
                play_callback=on_play
            )

            mpv_player.play_title(anime, stream)
            mpv_player.wait()

        except Exception:
            pass
