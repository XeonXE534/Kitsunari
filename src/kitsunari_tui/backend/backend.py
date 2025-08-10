# backend.py
import re
import html
from anipy_api.provider.providers.allanime_provider import AllAnimeProvider
from anipy_api.anime import Anime
from anipy_api.provider import LanguageTypeEnum
from anipy_api.player import get_player

# Cleans HTML
def clean_html(raw: str) -> str:
    text = re.sub(r'<.*?>', '', raw).strip()
    return html.unescape(text)

# Grabs anime
def get_anime_by_query(query: str) -> list[Anime]:
    provider = AllAnimeProvider()
    results = provider.get_search(query)

    if not results:
        raise ValueError(f"No anime found for query :/ :{query}")

    anime_list = []
    for i in results:
        anime = Anime.from_search_result(provider, i)
        anime_list.append(anime)

    return  anime_list

def get_episodes(anime: Anime) -> list[int | float]:
    return anime.get_episodes(lang=LanguageTypeEnum.SUB)

# Get a single stream URL for a specific episode at preferred quality.
def get_episode_stream(anime: Anime, episode: int, quality: int = 720):
    stream = anime.get_video(
        episode=episode,
        lang=LanguageTypeEnum.SUB,
        preferred_quality=quality
    )
    return stream

# Get all available stream URLs for a specific episode.
def get_episode_streams(anime: Anime, episode: int):
    streams = anime.get_videos(
        episode=episode,
        lang=LanguageTypeEnum.SUB
    )
    return streams
