# anipy_client.py
import re
from anipy_api.provider.providers.allanime_provider import AllAnimeProvider
from anipy_api.anime import Anime
from anipy_api.provider import LanguageTypeEnum

def clean_html(raw: str) -> str:
    return re.sub(r'<.*?>', '', raw).strip()

def get_anime_by_query(query: str) -> Anime:
    provider = AllAnimeProvider()
    results = provider.get_search(query)

    if not results:
        raise ValueError(f"No anime found for query :/: {query}")

    anime = Anime.from_search_result(provider, results[0])
    return anime

def print_anime_info(anime: Anime) -> None:
    info = anime.get_info()
    print("Title:", info.name)
    print("Synopsis:", clean_html(info.synopsis or ""))

def print_episodes(anime: Anime) -> None:
    episodes = anime.get_episodes(lang=LanguageTypeEnum.SUB)

    if episodes == list(range(1, len(episodes) + 1)):
        print(f"Episodes: 1-{len(episodes)}")
    else:
        print(f"Episodes: {episodes}")

