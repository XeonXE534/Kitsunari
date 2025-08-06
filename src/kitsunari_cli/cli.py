# Imports
import os
import sys
import time
import platform
import argparse
import traceback
import subprocess
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

console = Console()
DEV_MODE = False # DISABLE THIS IN PROD PLEASE FOR THE LOVE OF :3 !

# Clear console
def clear():
    if not DEV_MODE:
        os.system('clear' if os.name != 'nt' else 'cls')

# Debug logger
def log(message):
    if DEV_MODE:
        console.print(f'[dim][DEV][/dim] {message}')

# Dependency check
def check_depends():
    deps = ['fzf']
    missing = []

    for dep in deps:
        try:
            subprocess.run([dep, '--version'], capture_output=True, check=True)
            log(f' Dependency "{dep}" installed! :3')

        except subprocess.CalledProcessError:
            log(f' Dependency "{dep}" not installed! :/')
            missing.append(dep)

    if missing:
        console.print(f' Missing deps: {','.join(missing)} :/', style='bold red')
        console.print(' Install fzf from: https://github.com/junegunn/fzf!', style='yellow')
        sys.exit(1)

    if DEV_MODE:
        console.print(' Running in dev mode! :3', style='yellow')
        log(f"Platform: {platform.system()} {platform.release()}")
        log(f"Python version: {platform.python_version()}")
        log(f"Terminal: {os.getenv('TERM', 'unknown')}")
        log(f"Current working dir: {os.getcwd()}")
        log(f"Script args: {sys.argv}")

# Banner
def banner():
    banner_txt = Text('Kitsunāri | キツナーリ: CLI', style='dark_orange')
    subtitle = Text('Version: 0.1.5', style='deep_pink2')
    group = Group(banner_txt, subtitle)
    console.print(Panel.fit(group, border_style='red1'))

# Dev banner
def dev_banner():
    banner_txt = Text('Kitsunāri | キツナーリ: CLI', style='red1')
    subtitle = Text('Version: 0.1.5-dev', style='red1')
    group = Group(banner_txt, subtitle)
    console.print(Panel.fit(group, border_style='red1'))

# Fuzzy search
def fzf_select(items, prompt='Select one :3'):
    if not items:
        console.print('Error! :/', style='red1')
        return None

    is_tuple = isinstance(items[0], tuple)
    display_list = [x[0] if is_tuple else x for x in items] # Refer /docs/fzf.md, SEC-1.0
    fzf_input = '\n'.join(display_list)
    cmd = ["fzf", "--reverse", "--cycle", "--height", "40%", "--border", "--prompt", prompt]

    log(f"fzf input list: {display_list}")
    log(f"fzf command: {cmd}")

    try:
        start = time.time()
        result = subprocess.run(cmd, input=fzf_input, text=True, capture_output=True)
        duration = time.time() - start

        picked = result.stdout.strip()
        log(f"fzf returned: '{picked}' in {duration:.2f}s")

        if not picked:
            console.print('No selection made :/', style='red1')
            return None

        if is_tuple:
            return next(val for name, val in items if name == picked) # Refer /docs/fzf.md, SEC-1.1
        return picked

    except KeyboardInterrupt:
        console.print('Bye! :3', style='pink1')
        return None

    except Exception as e:
        console.print('Unexpected error occurred! :/ ', style='red1')

        if DEV_MODE:
            traceback.print_exc()
        return None

# Dummy functions! FOR TESTING PURPOSES ONLY! REPLACE!!!!!
def dummy_search(query):
    return [
        (f"{query} Season 1", "s1"),
        (f"{query} Season 2", "s2"),
        (f"{query} Movie", "movie"),
        ("Demon Slayer", "ds"),
        ("Attack on Titan", "aot")
    ]

def dummy_episodes(anime_id):
    return [(f"Episode {i + 1}", str(i + 1)) for i in range(12)]

def dummy_qualities():
    return [
        ("1080p (Best)", "1080p"),
        ("720p (Good)", "720p"),
        ("480p (Fast)", "480p")
    ]

def fake_play(anime, episode, quality):
    clear()
    console.print("\n🎬 [bold green]Now Playing:[/bold green]")
    console.print(f"   📺 Anime: [cyan]{anime}")
    console.print(f"   🎬 Episode: [yellow]{episode}")
    console.print(f"   📶 Quality: [green]{quality}")
    console.print("\n🚧 This part still WIP. Streaming soon™", style="italic yellow")
    input("\n[Press Enter to continue]")

# Main program loop
def player_loop():
    clear()
    check_depends()
    if DEV_MODE:
        dev_banner()
    else:
        banner()

    console.print('\n Enter anime to search! :3', style='black')
    query = input('> ').strip()
    clear()

    if not query:
        console.print('No input provided! :/', style='red1')
        return

    # Search for anime
    results = dummy_search(query)
    anime_id =fzf_select(results, 'Select anime :3')

    if not anime_id:
        console.print('No anime selected! :/', style='red1')
        return

    anime_title = next(name for name, val in results if val == anime_id) # Refer /docs/fzf.md, SEC-1.1

    # Select episode
    episodes = dummy_episodes(anime_id)
    ep = fzf_select(episodes, f'Select episode for {anime_title} :3')
    if not ep:
        console.print('No episode selected! :/', style='red1')
        return

    # Select quality
    quality = fzf_select(dummy_qualities(), 'Select quality :3')
    if not quality:
        console.print('No quality selected! :/', style='red1')
        return

    # Play
    fake_play(anime_title, ep, quality)

    while True:
        clear()
        options = fzf_select([
            ('    Next', 'next'),
            ('    Replay','replay'),
            ('    Prev', 'prev'),
            ('󰌍    Pick different ep', 'pick'),
            ('󰐵    Change quality', 'quality'),
            ('    Exit', 'exit')
        ], f'Now Playing {anime_title} {ep} :3')

        if options == 'exit' or not options:
            break

        elif options == 'replay':
            fake_play(anime_title, ep, quality)

        elif options == 'quality':
            new_q = fzf_select(dummy_qualities(), "Select quality:")

            if new_q:
                quality = new_q
                fake_play(anime_title, ep, quality)

        elif options == 'pick':
            new_ep = fzf_select(episodes, 'Pick another ep:')

            if new_ep:
                ep = new_ep
                fake_play(anime_title, ep, quality)

        elif options == 'next':            # Refer /docs/fzf.md, SEC-1.2
            idx = next((i for i, (_, num) in enumerate(episodes) if num == ep), None)

            if idx is not None and idx + 1 < len(episodes):
                ep = episodes[idx + 1][1]
                fake_play(anime_title, ep, quality)

            else:
                console.print('No next episode available! :/', style='red1')

        elif options == 'prev':             # Refer /docs/fzf.md, SEC-1.2
            idx = next((i for i, (_, num) in enumerate(episodes) if num == ep), None)

            if idx is not None and idx > 0:
                ep = episodes[idx - 1][1]
                fake_play(anime_title, ep, quality)

            else:
                console.print('No previous episode available! :/', style='red1')

def main():
    global DEV_MODE

    parser = argparse.ArgumentParser(description='Kitsunāri CLI - Stream anime from your terminal :3')
    parser.add_argument('query', nargs='*', help='Anime to search for')
    parser.add_argument('-v', '--version', action='version', version='Kitsunāri CLI 0.1.5')
    parser.add_argument('-d', '--dev', action='store_true', help='Enable dev mode')
    args = parser.parse_args()

    DEV_MODE = args.dev

    if DEV_MODE:
        log("Dev mode enabled! :3")

    try:
        if args.query:
            if DEV_MODE:
                log(f"Searching for: {' '.join(args.query)}")
                log(" Direct search not ready yet. Launching interactive...")
            else:
                console.print(f'Searching for: {" ".join(args.query)} :3', style='black')
                console.print(" Direct search not ready yet. Launching interactive...", style="yellow")
            player_loop()
        else:
            player_loop()

    except KeyboardInterrupt:
        console.print('Bye! :3', style='pink1')
        sys.exit(0)
    except Exception as e:
        console.print('Unexpected error occurred! :/ ', style='red1')
        if DEV_MODE:
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()