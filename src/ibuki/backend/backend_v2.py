from pathlib import Path
from anipy_api.anime import Anime
from anipy_api.player import get_player
from anipy_api.provider import LanguageTypeEnum, ProviderStream
from anipy_api.provider.providers.allanime_provider import AllAnimeProvider

# Animebackend v2

class AnimeBackend:
    def __init__(self):
        self.provider = AllAnimeProvider()
        self._cache: dict = {}
        self._episodes_cache: dict = {}
        self._episodes_fetching: dict = {}

    def get_anime_by_query(self, query: str) -> list[Anime]:
        """
        Search for anime by query string and return a list of Anime objects.
        """
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
                anime_list.append(anime)

            return anime_list

        except Exception:
            return []

    def get_episodes(self, anime: Anime) -> list[int | float]:
        """
        Retrieve the list of episodes for a given anime, using caching to avoid redundant fetches.
        """
        anime_id = getattr(anime, "id", None) or id(anime)

        if anime_id in self._episodes_cache:
            return self._episodes_cache[anime_id]

        episodes = anime.get_episodes(lang=LanguageTypeEnum.SUB)
        self._episodes_cache[anime_id] = episodes
        return episodes

    def get_episode_stream(self, anime: Anime, episode: int, quality: int) -> ProviderStream | None:
        """
        Get the streaming link for a specific episode of an anime at the desired quality.
        """
        try:
            stream = anime.get_video(
                episode=episode,
                lang=LanguageTypeEnum.SUB,
                preferred_quality=quality
            )
            return stream

        except Exception:
            return None

    def play_episode(self, anime: Anime, episode: int, quality: int = 720):
        """
        Play a specific episode of an anime using an external media player.
        """
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