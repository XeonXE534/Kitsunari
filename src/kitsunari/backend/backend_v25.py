import time
import subprocess
from threading import Thread
from typing import Optional, List
from anipy_api.anime import Anime
from logs.logger import get_logger
from .utils_v3 import WatchHistory
from anipy_cli.config import Config
from anipy_api.provider import ProviderStream, LanguageTypeEnum
from anipy_api.provider.providers.allanime_provider import AllAnimeProvider

# Animebackend v2.5

class AnimeBackend:
    def __init__(self):
        self.logger = get_logger("AnimeBackend")
        self.provider = AllAnimeProvider()
        self.cache = {}
        self.episodes_cache = {}
        self.watch_history = WatchHistory()

        self.global_quality: int = 720
        self.current_anime: Optional[Anime] = None
        self.current_episode: Optional[int] = None
        self.current_duration: Optional[int] = None

        self.mpv_process: Optional[subprocess.Popen] = None
        self._stderr_thread: Optional[Thread] = None

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

    def _choose_stream(self, streams: List[ProviderStream], quality: int) -> ProviderStream:
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

    def _stderr_logger(self, stderr_pipe):
        """Read stderr lines from mpv and log them in realtime. Courtesy of ChatGPT lol"""
        try:
            for raw in iter(stderr_pipe.readline, b""):
                if not raw:
                    break

                try:
                    line = raw.decode(errors="ignore").strip()

                except Exception:
                    line = str(raw)
                self.logger.info(f"MPV STDERR: {line}")

        except Exception as e:
            self.logger.debug(f"MPV stderr reader stopped: {e}")

    def play_episode(self, anime: Anime, episode, quality=None, start_time=0):
        """
        Play an episode using subprocess mpv while tracking progress via a simple timer.
        """
        if quality != self.global_quality:
            quality = self.global_quality

        self.logger.info(f"Playing {anime} EP{episode} at {quality}p :3")
        self._kill_existing_mpv()

        try:
            stream = self.get_episode_stream(anime, episode, quality)
            if not stream:
                self.logger.warning("No stream found :/")
                return

            anime_id = getattr(anime, "identifier", str(id(anime)))
            anime_name = getattr(anime, "name", "Unknown")
            self.current_anime = anime
            self.current_episode = episode

            cfg = Config()
            player_bin = str(cfg.player_path) if cfg.player_path else "mpv"
            referrer = stream.referrer or self.get_referrer_for_url(stream.url)
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

            extra_args = cfg.mpv_commandline_options if isinstance(cfg.mpv_commandline_options, list) else []

            mpv_cmd = [
                player_bin,
                f"--start={start_time}",
                "--force-window=immediate",
                "--input-default-bindings=yes",
                "--keep-open=no",
                "--osc=yes",
                "--fs",
                "--no-resume-playback",
                f"--referrer={referrer}" if referrer else "",
                f"--user-agent={user_agent}",
            ] + extra_args + [stream.url]

            mpv_cmd = [c for c in mpv_cmd if c]
            self.logger.info(f"Starting MPV: {' '.join(mpv_cmd)} >.<")

            self.mpv_process = subprocess.Popen(mpv_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

            if self.mpv_process.stderr:
                self._stderr_thread = Thread(target=self._stderr_logger, args=(self.mpv_process.stderr,), daemon=True)
                self._stderr_thread.start()

            progress_thread = Thread(
                target=self._track_progress_timer,
                args=(anime_id, anime_name, episode),
                daemon=True,
            )
            progress_thread.start()

            return_code = self.mpv_process.wait()
            self.logger.info(f"MPV exited with code: {return_code} :|")

            elapsed = int(time.time() - getattr(self, "_progress_start_time", time.time()))
            try:
                self.watch_history.update_progress(anime_id, anime_name, episode, elapsed, elapsed + 60)

            except Exception as e:
                self.logger.debug(f"Failed final progress save: {e} :/")

        except Exception as e:
            self.logger.exception(f"Error playing episode: {e}")

        finally:
            self._kill_existing_mpv()

    def _track_progress_timer(self, anime_id, anime_name, episode):
        """
        Track elapsed time since MPV started and update watch history every 10s.
        This is a simple fallback for subprocess mode (no JSON IPC).
        """
        try:
            start_time = time.time()
            self._progress_start_time = start_time

            last_saved = 0
            while hasattr(self, "mpv_process") and self.mpv_process and self.mpv_process.poll() is None:
                time.sleep(1)
                elapsed = int(time.time() - start_time)

                if elapsed % 10 == 0 and elapsed != last_saved:
                    last_saved = elapsed
                    try:
                        self.watch_history.update_progress(anime_id, anime_name, episode, elapsed, elapsed + 60)

                    except Exception as e:
                        self.logger.debug(f"Progress update failed: {e}")

        except Exception as e:
            self.logger.debug(f"Progress tracking stopped: {e}")

    def _kill_existing_mpv(self):
        """
        Kill any existing MPV process.
        """
        if hasattr(self, "mpv_process") and self.mpv_process:
            try:
                self.logger.debug("Terminating existing MPV process :3")
                self.mpv_process.terminate()
                self.mpv_process.wait(timeout=5)

            except subprocess.TimeoutExpired:
                self.logger.warning("MPV didn't terminate gracefully, forcing... >:3")

                try:
                    self.mpv_process.kill()
                    self.mpv_process.wait()

                except Exception as e:
                    self.logger.error(f"Error forcing MPV kill: {e} :/")

            except Exception as e:
                self.logger.error(f"Error killing MPV: {e} :/")

            finally:
                self.mpv_process = None

        try:
            subprocess.run(["pkill", "-f", "mpv.*--force-window"], timeout=5, capture_output=True)

        except Exception:
            pass

    def resume_anime(self, anime_id, quality=None):
        """
        Resume watching an anime from watch history.
        """
        if quality != self.global_quality:
            quality = self.global_quality

        entry = self.watch_history.get_entry(anime_id)
        if not entry:
            self.logger.warning("No history found for " + anime_id + ":/")
            return False

        anime = self.get_anime_by_id(anime_id)
        if not anime:
            results = self.get_anime_by_query(entry["anime_name"])
            if results:
                anime = results[0]

            else:
                self.logger.error("Could not find anime to resume :(")
                return False

        self.play_episode(anime, entry["episode"], quality, entry["timestamp"])
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
