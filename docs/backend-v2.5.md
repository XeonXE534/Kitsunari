# AnimeBackend v2.5 Documentation
> This document provides an overview for `AnimeBackend v2.5`

`AnimeBackend` is a synchronous, fast-ish Python middleman/controller(confusing name, ik) for handling anime search, streaming, and playback via `anipy_api` and MPV.
It manages caching, watch history, and stream quality selection. It is made for TUI frontends.

---

## Initialization

```python
from backend.backend import AnimeBackend

backend = AnimeBackend()
```

Creates a new backend instance using:

* `AllAnimeProvider` (via `anipy_api`)
* Built-in caching (`cache` & `episodes_cache`)
* `WatchHistory` persistence
* MPV subprocess-based playback

---

## Core Attributes
| Attribute        | Type               | Description                                           |
|------------------|--------------------|-------------------------------------------------------|
| `provider`       | `AllAnimeProvider` | The anime provider used for all search and streaming. |
| `cache`          | `dict`             | Stores previously searched anime for faster lookups.  |
| `episodes_cache` | `dict`             | Caches episodes for each anime.                       |
| `global_quality` | `int`              | Default playback quality (e.g. 720).                  |
| `watch_history`  | `WatchHistory`     | Object managing JSON-based progress tracking.         |
| `mpv_process`    | `subprocess.Popen` | Active MPV process, if running.                       |
| `_stderr_thread` | `Thread`           | Background thread logging MPV output.                 |
---

## Public Methods

### `get_anime_by_query(query: str) -> list[Anime]`

Search for anime by name.

**Parameters:**

* `query` — Search string (e.g. `"Blue Archive"`)

**Returns:**

* `list[Anime]` — List of `Anime` objects from provider.
* Empty list if no results or error.

**Notes:**

* Caches results to `self.cache`.
* Safe to call synchronously from a CLI or Textual frontend.

```python
results = backend.get_anime_by_query("Frieren")
```

---

### `get_anime_by_id(anime_id: str) -> Anime | None`

Retrieve a cached `Anime` object by ID.\
**Returns:** Cached `Anime` instance or `None`.

---

### `get_episodes(anime: Anime) -> list`

Get all episodes (subbed) for a given anime.

**Behavior:**

* Caches results per anime ID.
* Returns empty list on error.

```python
episodes = backend.get_episodes(anime)
```

---

### `get_episode_stream(anime: Anime, episode: int, quality: int) -> ProviderStream | None`

Get a playable stream for a specific episode.

**Parameters:**

* `anime` – `Anime` instance
* `episode` – Episode number
* `quality` – Preferred resolution (e.g. `720`)

**Returns:**

* `ProviderStream` – if a valid stream is found.
* `None` – if provider returns no streams.

**Selection logic:**

1. Match exact quality
2. Fallback to next-lower resolution
3. Otherwise, pick the highest available stream

---

### `play_episode(anime: Anime, episode: int, quality: int = 720, start_time: int = 0)`

Plays an episode using MPV via `subprocess.Popen`.

**Behavior:**

* Auto-kills any existing MPV instance.
* Logs MPV stderr in real-time.
* Tracks playback progress every 10 seconds.
* Saves progress to `WatchHistory`.

**Parameters:**

* `anime` – `Anime` instance
* `episode` – Episode number
* `quality` – Desired resolution (default: 720)
* `start_time` – Resume point in seconds (default: 0)

```python
backend.play_episode(anime, 5, 1080)
```

---

### `resume_anime(anime_id: str, quality: int = 720) -> bool`

Resume a previously watched anime using saved progress.\
**Returns:**

* `True` if resumed successfully
* `False` if no valid history or anime found

```python
backend.resume_anime("blue-archive-the-animation")
```

---

### `get_continue_watching_list(limit: int = 10) -> list[dict]`

Returns a structured list of up to `limit` entries from watch history.\
**Each entry contains:**

```python
{
  "anime_id": str,
  "anime_name": str,
  "episode": int,
  "progress_percent": float,
  "timestamp": int,
  "last_watched": str
}
```

Used for “Continue Watching” UI panels.

---

## Internal Methods

| Method                                                 | Description                                                  |
|--------------------------------------------------------|--------------------------------------------------------------|
| `_choose_stream(streams, quality)`                     | Internal selector for best quality stream.                   |
| `_stderr_logger(stderr_pipe)`                          | Reads and logs MPV’s stderr output live.                     |
| `_track_progress_timer(anime_id, anime_name, episode)` | Periodically updates progress while MPV runs.                |
| `_kill_existing_mpv()`                                 | Terminates any lingering MPV process.                        |
| `get_referrer_for_url(url)`                            | Returns appropriate referrer header for anime provider URLs. |
| `_on_play_start(anime)`                                | Simple log hook for playback start (placeholder).            |

---

## Behavior & Notes

* Fully synchronous
* Threaded progress tracking for smooth MPV subprocess use.
* Automatically resumes progress on next playback.
* Graceful process cleanup - kills MPV if user restarts playback.
* Works fine with Textual.
* Only supports `AllAnimeProvider` as of v2.5.
* Logs everything (info/debug) via `logs.logger`.
