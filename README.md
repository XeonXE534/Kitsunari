# PROJECT KITSUNARI | キツナーリ v1.0.0-beta

## TL;DR
Beta, bleeding edge version of Kitsunari. Sometimes works, sometimes summons demons. Use at your own risk. Seriously.  

## !!! HIGHLY EXPERIMENTAL !!!
- May crash, explode, or summon satan, who tf knows bruh.
- EXTREMELY buggy.
- Check `main` for stable version.  

## Backend Chaos
- Split into **two files**:
  - `backend_v2` – old, works, stable.
  - `backend_v3` – new, shiny, batches results by 10 (changeable in code), *should* be faster.  
- Search system (`search.py`) is now hooked up to `backend_v3`.  

## How to use
1. Launch the app. Pray it doesn’t crash.  
2. Type your anime in the search bar.  
3. Navigate with arrow keys:
   - Left: previous page (if the universe allows)  
   - Right: next page (only if there’s more)  
   - `E`: see episodes  
   - `S`: see synopsis  
4. Click an episode to watch in MPV (needs MPV in your PATH).  

## Known Issues
- Results may overlap if you search too fast.  
- Going past the last page = “Anime not found! :/” spam.  
- May eat your snacks.  

## TL;DR
Beta. Works sometimes. Don’t cry if it breaks.