# utils_v3 Documentation
> This document provides an overview of the `utils_v3` module.

`utils_v3` is a utility module for handling HTML cleanup and JSON-based watch history.

---

## Functions

### `clean_html(raw: str | None) -> str`

Remove HTML tags and unescape HTML entities.\
**Returns:**
Cleaned text or `"Not available :("` if input is empty.

```python
text = clean_html("<p>Hello &amp; Welcome!</p>")
# -> "Hello & Welcome!"
```

---

## Classes

### `WatchHistory(file_path=Path("./progress.json"))`

Handles anime watch history tracking and persistence.

**Stores:**

* `anime_name`
* `episode`
* `timestamp`
* `total_duration`
* `last_watched`
* `progress_percent`

**All data stored as JSON** in `progress.json`.

---

#### `load() -> dict`

Reads and returns the JSON data from disk.
Returns `{}` if missing or invalid.

#### `save() -> None`

Writes current history to file with indentation.

#### `update_progress(anime_id, anime_name, episode, timestamp, total_duration)`

Updates or creates a progress entry.
Automatically calculates `progress_percent`.

---

#### `get_continue_watching(limit: int = 10) -> list[tuple]`

Returns a sorted list of partially watched entries (5s < progress < 95%).\
Sorted by `last_watched` descending.

---

#### `get_entry(anime_id: str) -> dict | None`

Returns a single watch entry or `None`.

---

#### `remove_entry(anime_id: str)`

Removes a history entry from file and logs the action.

---

## Example

```python
from backend.utils_v3 import WatchHistory

history = WatchHistory()

# Save progress
history.update_progress("frieren", "Sousou no Frieren", 3, 720, 1440)

# Continue watching list
continue_list = history.get_continue_watching()
```