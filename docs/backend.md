# AnimeBackend Documentation
> This document provides an overview for `AnimeBackend v2` 

`AnimeBackend` is a synchronous backend for fetching anime data, episodes, and playable streams using the `anipy_api`. It’s designed to be simple-ish, fast-ish, and fully compatible with a Textual-based frontend.

---

## Table of Contents

* [Initialization](#initialization)
* [Methods](#methods)
  * [get\_anime\_by\_query](#get_anime_by_query)
  * [get\_episodes](#get_episodes)
  * [get\_episode\_stream](#get_episode_stream)
  * [play\_episode](#play_episode)
* [Caching & Behavior](#caching--behavior)

---

## Initialization

```python
from backend.backend import AnimeBackend

backend = AnimeBackend()
```

* **Description:**
Creates a new backend instance with `AllAnimeProvider` as the default (and only) provider.

---

## Methods

### `get_anime_by_query(query: str) -> list[Anime]`

* **Description:**
  Search for anime by name.
* **Parameters:**
  * `query` – The search string (anime title).
* **Returns:**
  * List of `Anime` objects if results are found.
  * Empty list if no results or an error occurs.
* **Notes:**
  * Skips search results missing critical fields (`id`, `url`).
  * Fully synchronous; safe to call from a Textual frontend.

```python
results = backend.get_anime_by_query("Blue Archive")
```

---

### `get_episodes(anime: Anime) -> list[int | float]`

* **Description:**
  Retrieves the episode list for the given anime (English subbed). This call is **synchronous** and will block until all episodes are fetched from the provider. Subsequent calls return the cached episodes.
* **Parameters:**
  * `anime` – An instance of `Anime`.
* **Returns:**
  * List of episode numbers (int or float) for the anime.
  * Will raise an exception if fetching fails (currently caught silently in your code).

```python
episodes = backend.get_episodes(anime)
```

---

### `get_episode_stream(anime: Anime, episode: int, quality: int) -> ProviderStream | None`

* **Description:**
  Fetch a playable stream for a specific episode.
* **Parameters:**
  * `anime` – An `Anime` instance.
  * `episode` – Episode number.
  * `quality` – Preferred quality (e.g., 720).
* **Returns:**
  * `ProviderStream` object if available.
  * `None` if the stream could not be fetched.

```python
stream = backend.get_episode_stream(anime, 1, 720)
```

---

### `play_episode(anime: Anime, episode: int, quality: str | int = 720) -> None`

* **Description:**
  Plays the selected episode using MPV.
* **Parameters:**
  * `anime` – The `Anime` instance.
  * `episode` – Episode number.
  * `quality` – Preferred quality (`int` or `"worst"`/`"best"`).
* **Behavior:**
  * Uses `get_episode_stream` to fetch the video.
  * Initializes an MPV player and plays in fullscreen.
  * Runs synchronously; the function waits until playback finishes.
```python
backend.play_episode(anime, 1, 720)
```

---

## Caching & Behavior

* **Episode caching:** Fetched episodes are stored in `_episodes_cache`.
* **Fetch behavior:** `get_episodes` is synchronous and will block until all episodes are fetched from the provider. Subsequent calls return cached episodes.
* Fully synchronous backend.

---

## Notes

* No logging in this version
* Resolution is dictated by the provider. Most streams are 1080 or higher.
* Only supports `AllAnimeProvider` currently.
* Designed to gracefully handle missing or malformed data from the provider.
* Simple caching reduces repeated API calls but still hits the provider if uncached.
* Stable, fast-ish, and minimal—won’t crash for massive anime series.
* Honestly, it’s a bit of a Frankenstein backend, but it works 👍