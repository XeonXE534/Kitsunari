import subprocess
from pathlib import Path
import json
from datetime import datetime
from anipy_api.provider.providers.allanime_provider import AllAnimeProvider
from anipy_api.anime import Anime
from anipy_api.provider import LanguageTypeEnum
from anipy_api.player.players import MpvControllable
from logs.logger import get_logger
from threading import Thread
import time

PROGRESS_FILE = Path("./progress.json").expanduser()

# Animebackend v2.5

class WatchHistory:
    def __init__(self, file_path=PROGRESS_FILE):
        self.file_path = file_path
        self.logger = get_logger("WatchHistory")
        self.history = self.load()

    def load(self):
        if self.file_path.exists():
            try:
                return json.loads(self.file_path.read_text())

            except Exception as e:
                self.logger.error("Failed to load watch history: " + str(e))
                return {}

        return {}

    def save(self):
        try:
            self.file_path.write_text(json.dumps(self.history, indent=2))

        except Exception as e:
            self.logger.error("Failed to save watch history: " + str(e))

    def update_progress(self, anime_id, anime_name, episode, timestamp, total_duration):
        percent = 0
        if total_duration > 0:
            percent = round((timestamp / total_duration) * 100, 1)

        self.history[anime_id] = {
            "anime_name": anime_name,
            "episode": episode,
            "timestamp": timestamp,
            "total_duration": total_duration,
            "last_watched": datetime.now().isoformat(),
            "progress_percent": percent
        }
        self.save()
        self.logger.debug(f"Updated {anime_name} EP{episode}: {timestamp}s")

    def get_continue_watching(self, limit=10):
        active = {}

        for k, v in self.history.items():
            if 5 < v["timestamp"] < v["total_duration"] * 0.95:
                active[k] = v

        sorted_items = sorted(active.items(), key=lambda x: x[1]["last_watched"], reverse=True)
        return sorted_items[:limit]

    def get_entry(self, anime_id):
        return self.history.get(anime_id)

    def remove_entry(self, anime_id):
        if anime_id in self.history:
            del self.history[anime_id]
            self.save()
            self.logger.info(f"Removed {anime_id} from watch history")

class AnimeBackend:
    def __init__(self):
        self.logger = get_logger("AnimeBackend")
        self.provider = AllAnimeProvider()
        self.cache = {}
        self.episodes_cache = {}
        self.watch_history = WatchHistory()

        self.current_anime = None
        self.current_episode = None
        self.current_duration = None


        self.current_player: MpvControllable | None = None

        self.logger.debug("AnimeBackend ready.")

    def get_anime_by_query(self, query):
        self.logger.info("Searching for: " + query)
        try:
            results = self.provider.get_search(query)
        except Exception as e:
            self.logger.exception("Error during search: " + str(e))
            return []

        if not results:
            self.logger.warning("No results found.")
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
        return self.cache.get(anime_id)

    def get_episode_stream(self, anime, episode, quality):
        try:
            stream = anime.get_video(episode=episode, lang=LanguageTypeEnum.SUB, preferred_quality=quality)
            return stream

        except Exception as e:
            self.logger.exception("Error fetching stream: " + str(e))
        return None

    def get_episodes(self, anime):
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

    def play_episode(self, anime, episode, quality=720, start_time=0):
        self.logger.info(f"Playing {anime} EP{episode} at {quality}p")
        self._kill_existing_mpv()

        try:
            stream = self.get_episode_stream(anime, episode, quality)
            if not stream:
                self.logger.warning("No stream found")
                return

            anime_id = getattr(anime, "identifier", str(id(anime)))
            anime_name = getattr(anime, "name", "Unknown")

            mpv_cmd = [
                'mpv',
                f'--start={start_time}',
                '--force-window=immediate',
                '--input-default-bindings=yes',
                '--keep-open=no',
                '--osc=yes',
                '--title=MPV - Anime Player',
                '--no-resume-playback',
                stream.url
            ]
            self.logger.info(f"Starting MPV: {' '.join(mpv_cmd)}")

            self.mpv_process = subprocess.Popen(
                mpv_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            progress_thread = Thread(
                target=self._track_progress,
                args=(anime_id, anime_name, episode),
                daemon=True
            )
            progress_thread.start()

            return_code = self.mpv_process.wait()
            self.logger.info(f"MPV exited with code: {return_code}")

            self.mpv_process = None

        except Exception as e:
            self.logger.exception(f"Error playing episode: {e}")
        finally:
            self._kill_existing_mpv()

    def _track_progress(self, anime_id, anime_name, episode):
        try:
            start_time = time.time()
            while (hasattr(self, 'mpv_process') and
                   self.mpv_process and
                   self.mpv_process.poll() is None):
                time.sleep(10)
                elapsed = time.time() - start_time
                self.logger.debug(f"Playing {anime_name} EP{episode} for {elapsed:.0f}s")

            if hasattr(self, 'mpv_process') and self.mpv_process:
                return_code = self.mpv_process.poll()
                if return_code == 0:
                    elapsed = time.time() - start_time
                    self.watch_history.update_progress(
                        anime_id, anime_name, episode, int(elapsed), int(elapsed + 60)
                    )

        except Exception as e:
            self.logger.debug(f"Progress tracking stopped: {e}")

    def _kill_existing_mpv(self):
        if hasattr(self, 'mpv_process') and self.mpv_process:
            try:
                self.mpv_process.terminate()
                self.mpv_process.wait(timeout=5)

            except subprocess.TimeoutExpired:
                self.logger.warning("MPV didn't terminate gracefully, forcing...")
                self.mpv_process.kill()
                self.mpv_process.wait()

            except Exception as e:
                self.logger.error(f"Error killing MPV: {e}")

            finally:
                self.mpv_process = None

        try:
            subprocess.run(
                    ['pkill', '-f', 'mpv.*--force-window'],
                           timeout=5, capture_output=True
                           )
        except:
            pass

    def resume_anime(self, anime_id, quality=720):
        entry = self.watch_history.get_entry(anime_id)
        if not entry:
            self.logger.warning("No history found for " + anime_id)
            return False

        anime = self.get_anime_by_id(anime_id)
        if not anime:
            results = self.get_anime_by_query(entry['anime_name'])
            if results:
                anime = results[0]
            else:
                self.logger.error("Could not find anime to resume")
                return False

        self.play_episode(anime, entry['episode'], quality, entry['timestamp'])
        return True

    def get_continue_watching_list(self, limit=10):
        cont = self.watch_history.get_continue_watching(limit)
        result = []

        for anime_id, h in cont:
            result.append({
                "anime_id": anime_id,
                "anime_name": h["anime_name"],
                "episode": h["episode"],
                "progress_percent": h["progress_percent"],
                "timestamp": h["timestamp"],
                "last_watched": h["last_watched"]
            })
        return result

    def _on_play_start(self, anime, stream):
        self.logger.info(f"Playback started: {anime}")
