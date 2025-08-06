# FZF Usage Documentation
### This is a guide for myself on how to use fzf in my scripts cuz ill definitely forget what I wrote.

## SEC-1.0
This list comprehension creates a list of display items for fzf.

- If `items` contains tuples (e.g., `("Naruto", "ninja")`), it takes only the first value (e.g., `"Naruto"`).
- If `items` is a list of strings, it just keeps them as-is.

### Basically:
```display_list = [x[0] if is_tuple else x for x in items]```

### Means:
for each item:
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

## SEC-1.1
This loop is used to find the corresponding value (like a URL, ID, or path) for the item selected via fzf.

- Items is a list of tuples: e.g. ("Naruto", "https://anime.com/naruto").
- Picked is the user’s selected item (e.g. "Naruto").
- The loop checks each tuple's first element (name) to see if it matches picked.
- If a match is found, the second value (val) is returned.

### Basically:
```return next(val for name, val in items if name == picked)```

### Means:
- Loop through each (name, val) in the list.
- If name == picked, return the corresponding val (the thing you actually want to use).

### Expanded:
```python
for name, val in items:
    if name == picked:
        return val
```

