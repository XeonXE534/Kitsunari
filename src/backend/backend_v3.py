from pathlib import Path
from typing import Dict, List, Optional, Union, Generator
from anipy_api.provider.providers.allanime_provider import AllAnimeProvider
from anipy_api.anime import Anime
from anipy_api.provider import LanguageTypeEnum, ProviderStream
from anipy_api.player import get_player

# Backend v3

class AnimeBackend:
    BATCH_SIZE = 10

    def __init__(self):
        self.provider = AllAnimeProvider()
        self._cache: Dict[Union[int, str], Anime] = {}
        self._episodes_cache: Dict[Union[int, str], List[Union[int, float]]] = {}
        self._batch_cache: Dict[str, List[List[Anime]]] = {}
        self._generators: Dict[str, Generator[Anime, None, None]] = {}
        self.current_page: Dict[str, int] = {}
        self._exhausted_queries: set[str] = set()

    def _search_generator(self, query: str) -> Generator[Anime, None, None]:
        try:
            results = self.provider.get_search(query)
            if not results:
                return

            for idx, r in enumerate(results):
                try:
                    key = getattr(r, "id", idx)

                    if key in self._cache:
                        anime = self._cache[key]

                    else:
                        anime = Anime.from_search_result(self.provider, r)
                        self._cache[key] = anime

                    yield anime

                except Exception:
                    continue

        except Exception:
            return

    def start_search(self, query: str) -> None:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty or whitespace :/")

        query = query.strip()

        if query not in self._generators:
            self._generators[query] = self._search_generator(query)

        if query not in self._batch_cache:
            self._batch_cache[query] = []

    def get_next_page(self, query: str) -> List[Anime]:
        if not query or not query.strip():
            return []

        query = query.strip()
        self.start_search(query)
        batch = []

        try:
            gen = self._generators[query]
            for _ in range(self.BATCH_SIZE):
                try:
                    batch.append(next(gen))

                except StopIteration:
                    break

        except Exception as e:
            print(f"Error fetching next page for query '{query}': {e} :/")

        if batch:
            self._batch_cache[query].append(batch)

        else:
            self._exhausted_queries.add(query)
        return batch

    def get_page(self, query: str, page_idx: int) -> List[Anime]:
        if not query or page_idx < 0:
            return []

        query = query.strip()
        batches = self._batch_cache.get(query, [])
        return batches[page_idx] if page_idx < len(batches) else []

    def get_anime_by_query(self, query: str, next_page: bool = False) -> List[Anime]:
        if not query or not query.strip():
            return []

        query = query.strip()
        self.start_search(query)

        if query in self._exhausted_queries:
            return []

        if next_page:
            self.current_page[query] = self.current_page.get(query, -1) + 1

        else:
            self.current_page[query] = 0

        page_idx = self.current_page[query]
        batches = self._batch_cache.get(query, [])

        while page_idx >= len(batches):
            batch = self.get_next_page(query)
            if not batch:
                break
            batches = self._batch_cache[query]

        return self.get_page(query, page_idx)

    def is_last_page(self, query: str) -> bool:
        if query in self._exhausted_queries:
            return True
        batches = self._batch_cache.get(query, [])
        return bool(batches) and len(batches[-1]) < self.BATCH_SIZE

    def get_episodes(self, anime: Anime) -> List[Union[int, float]]:
        if not anime:
            return []

        anime_id = getattr(anime, "id", id(anime))

        if anime_id in self._episodes_cache:
            return self._episodes_cache[anime_id]

        try:
            episodes = anime.get_episodes(lang=LanguageTypeEnum.SUB) or []
            self._episodes_cache[anime_id] = episodes
            return episodes

        except Exception as e:
            print(f"Error fetching episodes for anime {anime_id}: {e} :/")
            self._episodes_cache[anime_id] = []
            return []

    def get_episode_stream(self, anime: Anime, episode: Union[int, float], quality=720) -> Optional[ProviderStream]:
        if not anime:
            return None

        try:
            return anime.get_video(episode=episode, lang=LanguageTypeEnum.SUB, preferred_quality=quality)

        except Exception as e:
            print(f"Error getting stream for episode {episode}: {e}")
            return None

    def play_episode(self, anime: Anime, episode: Union[int, float], quality: Union[str, int] = 720) -> bool:
        if not anime:
            print("Error: No anime provided")
            return False

        def on_play(anime_obj: Anime, stream: ProviderStream) -> None:
            print(f"Now playing: {getattr(anime_obj, 'name', 'Unknown')} - Episode {episode}")

        try:
            if isinstance(quality, str):
                try:
                    quality = int(quality)

                except ValueError:
                    print(f"Warning: Invalid quality '{quality}', using 720p")
                    quality = 720

            stream = self.get_episode_stream(anime, episode, quality)
            if not stream:
                print(f"Error: No stream available for episode {episode}")
                return False

            mpv_player = get_player(Path("mpv"), extra_args=["--fs"], play_callback=on_play)
            mpv_player.play_title(anime, stream)
            mpv_player.wait()
            return True

        except FileNotFoundError:
            print("Error: mpv player not found. Please ensure mpv is installed and in PATH.")
            return False

        except Exception as e:
            print(f"Error during playback: {e}")
            return False

    def clear_cache(self, query: Optional[str] = None) -> None:
        if query:
            query = query.strip()
            self._batch_cache.pop(query, None)
            self._generators.pop(query, None)
            self._exhausted_queries.discard(query)
        else:
            self._cache.clear()
            self._episodes_cache.clear()
            self._batch_cache.clear()
            self._generators.clear()
            self._exhausted_queries.clear()

    def get_cached_anime_count(self) -> int:
        return len(self._cache)

    def get_cached_queries(self) -> List[str]:
        return list(self._batch_cache.keys())