# Usage Documentation - PERSONAL

## SEC-1.0
This list comprehension creates a list of display items for fzf.

- If `items` contains tuples (e.g., `("Naruto", "ninja")`), it takes only the first value (e.g., `"Naruto"`).
- If `items` is a list of strings, it just keeps them as-is.

### Basically:
```python
display_list = [x[0] if is_tuple else x for x in items]
```

### Means:
- for each item:
  - use x[0] if it's a tuple
  - otherwise just use x

### Expanded:
```python 
    display_list = []
for i in items:
    if is_tuple:
        display_list.append(i[0])
    else:
        display_list.append(i)
```
---
## SEC-1.1
This loop is used to find the corresponding value (like a URL, ID, or path) for the item selected via fzf.

- Items is a list of tuples: e.g. ("Naruto", "https://anime.com/naruto").
- Picked is the user’s selected item (e.g. "Naruto").
- The loop checks each tuple's first element (name) to see if it matches picked.
- If a match is found, the second value (val) is returned.

### Basically:
```python
return next(val for name, val in items if name == picked)
```

### Means:
- Loop through each (name, val) in the list.
- If name == picked, return the corresponding val (the thing you actually want to use).

### Expanded:
```python
for name, val in items:
    if name == picked:
        return val
```
---
## SEC-1.2
This logic is used to play the next or previous episode from a list of episodes, depending on the action selected.

- episodes is a list of tuples like: ("Naruto - Episode 1", 1)
- ep is the current episode number
- action is either "next" or "prev"
- We find the index of the current episode in the list.
- Then depending on the action:
    - We move to the next or previous episode (if possible)
    - Otherwise, print a error message

### Basically:
```python
elif action == "next":
    idx = next((i for i, (_, num) in enumerate(episodes) if num == ep), None)
    if idx is not None and idx + 1 < len(episodes):
        ep = episodes[idx + 1][1]
        fake_play(anime_title, ep, quality)
    else:
        console.print("No next episode", style="red")
elif action == "prev":
    idx = next((i for i, (_, num) in enumerate(episodes) if num == ep), None)
    if idx is not None and idx > 0:
        ep = episodes[idx - 1][1]
        fake_play(anime_title, ep, quality)
    else:
        console.print("No previous episode", style="red")
```
### Means:
- Go through episodes, find the one with the current episode number (ep).
- If found:
    - "next" → play the next one in the list.
    - "prev" → play the one before it.
    - If it’s already the first or last episode, show an error.

### Expanded:
```python
if action == "next":
    idx = None
    for i, (title, num) in enumerate(episodes):
        if num == ep:
            idx = i
            break
    if idx is not None and idx + 1 < len(episodes):
        ep = episodes[idx + 1][1]
        fake_play(anime_title, ep, quality)
    else:
        console.print("No next episode", style="red")

elif action == "prev":
    idx = None
    for i, (title, num) in enumerate(episodes):
        if num == ep:
            idx = i
            break
    if idx is not None and idx > 0:
        ep = episodes[idx - 1][1]
        fake_play(anime_title, ep, quality)
    else:
        console.print("No previous episode", style="red")
```
