from .mpv_player import MPVPlayer
from typing import Optional, List
from anipy_api.anime import Anime
from ..logs.logger import get_logger
from .utils_v3 import WatchHistory
from anipy_api.provider import ProviderStream, LanguageTypeEnum
from anipy_api.provider.providers.allanime_provider import AllAnimeProvider

# Animebackend v3

class AnimeBackend:
    def __init__(self):
        self.logger = get_logger("AnimeBackend")
        self.provider = AllAnimeProvider()
        self.cache = {}
        self.episodes_cache = {}
        self.watch_history = WatchHistory()
        self.player = MPVPlayer()

        self.global_quality: int = 720
        self.current_anime: Optional[Anime] = None
        self.current_episode: Optional[int] = None
        self.current_duration: Optional[int] = None

        self.logger.debug("AnimeBackend ready.")

    @staticmethod
    def get_referrer_for_url(url: str) -> str:
        """
        Get appropriate referrer for a given URL.
        """
        if "fast4speed" in url:
            return "https://allanime.day"

        elif "sunshinerays" in url:
            return "https://allanime.to"

        else:
            return "https://allanime.day"

    def _choose_stream(self, streams: List[ProviderStream], quality: int) -> Optional[ProviderStream]:
        """
        Choose best matching stream:
        - Exact resolution match first
        - Otherwise nearest lower resolution
        - Otherwise highest available
        """
        def sort_by_resolution(stream: ProviderStream):
            return getattr(stream, "resolution", 0)

        streams_sorted = sorted(streams, key=sort_by_resolution, reverse=True)

        for s in streams_sorted:
            if getattr(s, "resolution", 0) == quality:
                return s

        lower = []
        for s in streams_sorted:
            if getattr(s, "resolution", 0) < quality:
                lower.append(s)

        if lower:
            return lower[0]

        if not streams_sorted:
            self.logger.error("No streams available :/")
            return None

        return streams_sorted[0]

    def get_anime_by_query(self, query):
        """
        Search for anime by query string.
        Returns a list of Anime objects.
        Caches results to avoid redundant searches.
        """
        self.logger.info("Searching for: " + query + ":]")
        try:
            results = self.provider.get_search(query)

        except Exception as e:
            self.logger.exception("Error during search: " + str(e) + ":/")
            return []

        if not results:
            self.logger.warning("No results found :(")
            return []

        anime_list = []
        for i, r in enumerate(results):
            key = getattr(r, "id", i)
            if key in self.cache:
                anime = self.cache[key]

            else:
                anime = Anime.from_search_result(self.provider, r)
                self.cache[key] = anime
            anime_list.append(anime)

        return anime_list

    def get_anime_by_id(self, anime_id):
        """
        Retrieve an Anime object by its ID from the cache.
        """
        return self.cache.get(anime_id)

    def get_episode_stream(self, anime, episode, quality) -> Optional[ProviderStream]:
        """
        Return a single ProviderStream (best matching quality) or None.
        Accepts provider returning either a single ProviderStream or a list.
        """
        try:
            streams = anime.get_video(episode=episode, lang=LanguageTypeEnum.SUB, preferred_quality=quality)
            if not streams:
                return None

            if isinstance(streams, list):
                return self._choose_stream(streams, quality)

            else:
                return streams

        except Exception as e:
            self.logger.exception("Error fetching stream: " + str(e) + ":/")
        return None

    def get_episodes(self, anime):
        """
        Get list of episodes for an anime, with caching.
        """
        anime_id = getattr(anime, "id", id(anime))

        if anime_id in self.episodes_cache:
            return self.episodes_cache[anime_id]

        try:
            episodes = anime.get_episodes(lang=LanguageTypeEnum.SUB)
        except Exception as e:
            self.logger.exception("Error fetching episodes: " + str(e))
            return []

        self.episodes_cache[anime_id] = episodes
        return episodes

    def play_episode(self, anime: Anime, episode: int, stream: ProviderStream, start_time: int = 0):
        url = stream.url
        referrer = getattr(stream, 'referrer', self.get_referrer_for_url(url))
        extra_args = [f"--referrer={referrer}"]
        anime_id = getattr(anime, "identifier", str(id(anime)))
        anime_name = getattr(anime, "name", "Unknown")
        self.current_anime = anime
        self.current_episode = episode

        def on_mpv_exit():
            self.logger.info(f"MPV closed, saving history for {anime_name} EP{episode}")
            try:
                elapsed = self.player.get_elapsed_time()
                duration = self.player.current_duration or (elapsed + 300)
                self.watch_history.update_progress(anime_id, anime_name, episode, elapsed, duration)

            except Exception as e:
                self.logger.debug(f"Failed to save final progress: {e}")

        self.player.on_exit = on_mpv_exit
        self.player.launch(url, start_time=start_time, extra_args=extra_args)
        self.player.start_progress_tracker(
            lambda elapsed, duration: self.watch_history.update_progress(
                anime_id, anime_name, episode, elapsed, duration
            )
        )

    def resume_anime(self, anime_id, quality=None):
        quality = quality or self.global_quality
        entry = self.watch_history.get_entry(anime_id)
        if not entry:
            self.logger.warning(f"No history found for {anime_id}")
            return False

        anime = self.get_anime_by_id(anime_id) or (self.get_anime_by_query(entry["anime_name"]) or [None])[0]
        if not anime:
            self.logger.error("Could not find anime to resume")
            return False

        stream = self.get_episode_stream(anime, entry["episode"], quality)
        if not stream:
            self.logger.warning("No stream found for resume")
            return False

        self.play_episode(anime, entry["episode"], stream, entry["timestamp"])
        return True

    def get_continue_watching_list(self, limit=10):
        cont = self.watch_history.get_continue_watching(limit)
        result = []

        for anime_id, h in cont:
            result.append(
                {
                    "anime_id": anime_id,
                    "anime_name": h["anime_name"],
                    "episode": h["episode"],
                    "progress_percent": h["progress_percent"],
                    "timestamp": h["timestamp"],
                    "last_watched": h["last_watched"],
                }
            )
        return result

    def _on_play_start(self, anime):
        self.logger.info(f"Playback started: {anime}")