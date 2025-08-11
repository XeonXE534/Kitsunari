# backend.py
from anipy_api.provider.providers.allanime_provider import AllAnimeProvider
from anipy_api.anime import Anime
from anipy_api.provider import LanguageTypeEnum, ProviderStream
from logs.logger import get_logger
from anipy_api.player import get_player
from pathlib import Path

logger = get_logger("anime_backend")

class AnimeBackend:
    def __init__(self):
        self.provider = AllAnimeProvider()

    def get_anime_by_query(self, query: str) -> str | list[Anime]:
        try:
            results = self.provider.get_search(query)

            if not results:
                logger.warning(f"No results for query: {query}")
                return "No anime found for query :/"

            anime_list = []
            for i in results:
                anime = Anime.from_search_result(self.provider, i)
                anime_list.append(anime)

            logger.debug(f"Found {len(anime_list)} results for query: {query}")
            return anime_list

        except Exception as e:
            logger.error(f"Error in get_anime_by_query('{query}'): {e}", exc_info=True)
            return "An error occurred while searching."

    def get_episodes(self, anime: Anime) -> list[int | float]:
        try:
            return anime.get_episodes(lang=LanguageTypeEnum.SUB)
        except Exception as e:
            logger.error(f"Error in get_episodes: {e}", exc_info=True)
            return []

    def get_episode_stream(self, anime: Anime, episode: int, quality: int) -> ProviderStream | None:
        try:
            stream = anime.get_video(
                episode=episode,
                lang=LanguageTypeEnum.SUB,
                preferred_quality=quality
            )
            return stream
        except Exception as e:
            logger.error(f"Error in get_episode_stream(ep={episode}, quality={quality}): {e}", exc_info=True)
            return None

    def play_episode(self, anime: Anime, episode: int, quality: str | int = 720):
        def on_play(anime: Anime, stream: ProviderStream) -> None:
            logger.info(f"Now playing episode {stream.episode} from {anime.name}!")

        try:
            stream = self.get_episode_stream(anime, episode, quality)
            if not stream:
                logger.error(f"No stream found for episode {episode}")
                return

            mpv_player = get_player(
                Path("mpv"),
                extra_args=["--fs"],
                play_callback=on_play
            )

            mpv_player.play_title(anime, stream)
            mpv_player.wait()

        except Exception as e:
            logger.error(f"Error in play_episode: {e}", exc_info=True)
