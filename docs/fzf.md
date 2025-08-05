This list comprehension creates a list of display items for fzf.

- If `items` contains tuples (e.g., `("Naruto", "ninja")`), it takes only the first value (e.g., `"Naruto"`).
- If `items` is a list of strings, it just keeps them as-is.

Basically:
[x[0] if is_tuple else x for x in items]
⬇️
Means:
for each item:
  - use x[0] if it's a tuple
  - otherwise just use x
