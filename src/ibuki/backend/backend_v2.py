import time
from threading import Thread
from typing import Optional, List
from anipy_api.anime import Anime
from ..logs.logger import get_logger
from .utils_v3 import WatchHistory
from anipy_api.provider import ProviderStream, LanguageTypeEnum
from anipy_api.provider.providers.allanime_provider import AllAnimeProvider
from .mpv_player import MPVPlayer


class AnimeBackend:
    def __init__(self):
        self.logger = get_logger("AnimeBackend--TEST")
        self.provider = AllAnimeProvider()
        self.player = MPVPlayer()
        self.watch_history = WatchHistory()
        self.cache = {}
        self.episodes_cache = {}

        self.global_quality: int = 720
        self.current_anime: Optional[Anime] = None
        self.current_episode: Optional[int] = None
        self.current_duration: Optional[int] = None

        self.logger.debug("AnimeBackend ready.")

    @staticmethod
    def get_referrer_for_url(url: str) -> str:
        if "fast4speed" in url:
            return "https://allanime.day"
        elif "sunshinerays" in url:
            return "https://allanime.to"
        else:
            return "https://allanime.day"

    def _choose_stream(self, streams: List[ProviderStream], quality: int) -> Optional[ProviderStream]:
        streams_sorted = sorted(streams, key=lambda s: getattr(s, "resolution", 0), reverse=True)
        for s in streams_sorted:
            if getattr(s, "resolution", 0) == quality:
                return s
        lower = [s for s in streams_sorted if getattr(s, "resolution", 0) < quality]
        if lower:
            return lower[0]
        return streams_sorted[0] if streams_sorted else None

    def get_anime_by_query(self, query):
        self.logger.info(f"Searching for: {query}")
        try:
            results = self.provider.get_search(query)
        except Exception as e:
            self.logger.exception(f"Error during search: {e}")
            return []

        anime_list = []
        for i, r in enumerate(results):
            key = getattr(r, "id", i)
            anime = self.cache.get(key) or Anime.from_search_result(self.provider, r)
            self.cache[key] = anime
            anime_list.append(anime)
        return anime_list

    def get_anime_by_id(self, anime_id):
        return self.cache.get(anime_id)

    def get_episode_stream(self, anime, episode, quality) -> Optional[ProviderStream]:
        try:
            streams = anime.get_video(episode=episode, lang=LanguageTypeEnum.SUB, preferred_quality=quality)
            if not streams:
                return None
            if isinstance(streams, list):
                return self._choose_stream(streams, quality)
            return streams
        except Exception as e:
            self.logger.exception(f"Error fetching stream: {e}")
            return None

    def get_episodes(self, anime):
        anime_id = getattr(anime, "id", id(anime))
        if anime_id in self.episodes_cache:
            return self.episodes_cache[anime_id]
        try:
            episodes = anime.get_episodes(lang=LanguageTypeEnum.SUB)
        except Exception as e:
            self.logger.exception(f"Error fetching episodes: {e}")
            return []
        self.episodes_cache[anime_id] = episodes
        return episodes

    def play_episode(self, anime: Anime, episode: int, stream: ProviderStream, start_time: int = 0):
        url = stream.url
        anime_id = getattr(anime, "identifier", str(id(anime)))
        anime_name = getattr(anime, "name", "Unknown")
        self.current_anime = anime
        self.current_episode = episode

        def on_mpv_exit():
            self.logger.info(f"MPV closed, saving history for {anime_name} EP{episode}")
            try:
                elapsed = self.player.get_elapsed_time() if hasattr(self.player, "get_elapsed_time") else 0
                self.watch_history.update_progress(anime_id, anime_name, episode, elapsed, elapsed + 60)
            except Exception as e:
                self.logger.debug(f"Failed to save final progress: {e}")

        self.player.on_exit = on_mpv_exit
        self.player.launch(url, start_time=start_time)
        self.player.start_progress_tracker(
            lambda elapsed: self.watch_history.update_progress(anime_id, anime_name, episode, elapsed, elapsed + 60)
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
        return [
            {
                "anime_id": anime_id,
                "anime_name": h["anime_name"],
                "episode": h["episode"],
                "progress_percent": h["progress_percent"],
                "timestamp": h["timestamp"],
                "last_watched": h["last_watched"],
            }
            for anime_id, h in cont
        ]

    def _on_play_start(self, anime):
        self.logger.info(f"Playback started: {anime}")
