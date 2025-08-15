# AnimeBackend Documentation
> This document provides an overview for `AnimeBackend v3` 

`AnimeBackend` is a **synchronous backend** for searching anime, fetching episodes, and playing streams via `anipy_api`. It supports **pagination** and caches results to reduce repeated API calls. Fully compatible with **Textual frontends**.

---

## Table of Contents

* [Initialization](#initialization)
* [Searching & Paging](#searching--paging)
* [Episodes & Playback](#episodes--playback)
  * [get\_episodes](#get_episodes)
  * [get\_episode\_stream](#get_episode_stream)
  * [play\_episode](#play_episode)
* [Caching](#caching)
* [Notes](#notes)

---

## Initialization

```python
from backend.backend import AnimeBackend

backend = AnimeBackend()
```

* **Description:**
  Creates a new `AnimeBackend` instance using `AllAnimeProvider`. Caches are empty on initialization.
---

## Searching & Paging

### `get_anime_by_query(query: str, next_page: bool = False) -> list[Anime]`

* **Description:**
  Searches for anime by name and returns a **page of results**.
  Paging is controlled by `next_page`:
  * `False` → returns the first page of results.
  * `True` → returns the next page of cached search results (or fetches the next batch).
* **Parameters:**
  * `query` – The anime title string.
  * `next_page` – Whether to fetch the next page (default: `False`).
* **Returns:**
  * List of `Anime` objects for the requested page.
  * Empty list if no results are found or all pages are exhausted.
* **Notes:**
  * Uses a **generator** internally to lazily fetch search results.
  * Skips entries missing critical fields (`id`, `url`).
  * Safe to call from a synchronous frontend like Textual.

```python
# First page
first_page = backend.get_anime_by_query("Blue Archive")

# Next page
second_page = backend.get_anime_by_query("Blue Archive", next_page=True)
```

---

## Episodes & Playback

### `get_episodes(anime: Anime) -> list[int | float]`

* **Description:**
  Returns the episode list for a given anime (subbed). Episodes are cached after the first fetch.
* **Parameters:**
  * `anime` – An `Anime` instance.
* **Returns:**
  * List of episode numbers (int or float).
  * Empty list if episodes cannot be fetched.

```python
episodes = backend.get_episodes(anime)
```

---

### `get_episode_stream(anime: Anime, episode: int, quality: int) -> ProviderStream | None`

* **Description:**
  Fetches a playable stream for a specific episode.
* **Parameters:**
  * `anime` – The `Anime` instance.
  * `episode` – Episode number.
  * `quality` – Preferred quality (e.g., 720, 1080).
* **Returns:**
  * `ProviderStream` object if available, else `None`.

```python
stream = backend.get_episode_stream(anime, 1, 720)
```

---

### `play_episode(anime: Anime, episode: int, quality: int | str = 720) -> bool`

* **Description:**
  Plays the selected episode using **mpv** in fullscreen.
* **Parameters:**
  * `anime` – The `Anime` instance.
  * `episode` – Episode number.
  * `quality` – Preferred quality (int or string, e.g., `"720"`).
* **Returns:**
  * `True` if playback started successfully, else `False`.
* **Behavior:**
  * Fetches the stream using `get_episode_stream`.
  * Synchronously waits until playback finishes.

```python
backend.play_episode(anime, 1, 720)
```

---

## Caching

* **Anime objects:** Stored in `_cache` keyed by `anime.id`.
* **Episodes:** Stored in `_episodes_cache`.
* **Search results:** Stored in `_batch_cache` by query, split into pages of `BATCH_SIZE`.
* **Generators:** Stored in `_generators` to lazily fetch remaining results.
* **Methods:**

```python
backend.clear_cache()  # Clear all caches
backend.clear_cache("Blue Archive")  # Clear specific query
backend.get_cached_anime_count()  # Total cached anime
backend.get_cached_queries()  # List of queries with cached pages
```

---

## Notes

* Fully synchronous—no async required.
* Pagination prevents going past the last page.
* Safe against missing or malformed provider data.
* Designed for Textual frontends: search, next/previous page, episodes, and playback.
* Caching reduces API calls but keeps it simple and fast-ish.
* Blocks navigation past the first or last page to avoid spammed “Anime not found! :/” entries.