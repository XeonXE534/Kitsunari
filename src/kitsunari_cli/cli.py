# Imports
import subprocess
import sys
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
import os
import time
import platform
import traceback

console = Console()
dev_mode = True # DISABLE THIS IN PROD!

# Debug logger
def log(message):
    if dev_mode:
        console.print(f'[black1][DEV][/black1] {message}', highlight=False)

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

    if dev_mode:
        console.print(' Running in dev mode! :3', style='yellow')
        log(f"Platform: {platform.system()} {platform.release()}")
        log(f"Python version: {platform.python_version()}")
        log(f"Terminal: {os.getenv('TERM', 'unknown')}")
        log(f"Current working dir: {os.getcwd()}")
        log(f"Script args: {sys.argv}")

# Banner
def banner():
    banner_txt = Text('Kitsunāri | キツナーリ: CLI', style='dark_orange')
    subtitle = Text('Version: 0.0.5', style='deep_pink2')
    group = Group(banner_txt, subtitle)
    console.print(Panel.fit(group, border_style='red1'))

# Dev banner
def dev_banner():
    banner_txt = Text('Kitsunāri | キツナーリ: CLI', style='red1')
    subtitle = Text('Version: 0.0.5-dev', style='red1')
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
        if dev_mode:
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
    console.print("\n🎬 [bold green]Now Playing:[/bold green]")
    console.print(f"   📺 Anime: [cyan]{anime}")
    console.print(f"   🎬 Episode: [yellow]{episode}")
    console.print(f"   📶 Quality: [green]{quality}")
    console.print("\n🚧 This part still WIP. Streaming soon™", style="italic yellow")
    input("\n[Press Enter to continue]")

# Main program loop
def player_loop():
    check_depends()

    if dev_mode:
        dev_banner()
    else:
        banner()

    console.print('\n Enter anime to search! :3', style='black')
    query = input('> ').strip()

    if not query:
        console.print('No input provided! :/', style='red1')
        return
