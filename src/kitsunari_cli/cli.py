import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

# Pretty obi what this does
def check_dependencies():
    tools = ["fzf"]
    missing = []

    # Req's version check
    for tool in tools:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
        except:
            missing.append(tool)

    if missing:
        console.print(f" Missing: {', '.join(missing)}", style="red")
        console.print(" Run `pip install -r requirements.txt` from Kitsunari-cli parent folder", style="yellow")
        sys.exit(1)

# Banner
def show_banner():
    banner = Text(" Kitsunari CLI", style="bold magenta")
    subtitle = Text("Your anime streaming sidekick", style="italic cyan")
    console.print(Panel.fit(f"{banner}\n{subtitle}", border_style="bright_blue"))

# FZF (fuzzy finder) selection
def fzf_select(choices, prompt="Pick one:", multi=False):
    if not choices:
        return None

    is_tuple = isinstance(choices[0], tuple)
    display_list = [x[0] if is_tuple else x for x in choices]
    input_text = "\n".join(display_list)

    cmd = ["fzf", "--reverse", "--cycle", "--height", "40%", "--border", "--prompt", prompt]
    if multi:
        cmd.append("--multi")

    try:
        result = subprocess.run(cmd, input=input_text, text=True, capture_output=True)
        picked = result.stdout.strip()

        if not picked:
            return None

        if multi:
            picked = picked.split('\n')
        else:
            picked = [picked]

        if is_tuple:
            return [val for sel in picked for name, val in choices if sel == name] if multi else \
                   next(val for name, val in choices if name == picked[0])
        else:
            return picked if multi else picked[0]

    except KeyboardInterrupt:
        return None

def dummy_search(query):
    """Fake anime search results"""
    return [
        (f"{query} Season 1", "s1"),
        (f"{query} Season 2", "s2"),
        (f"{query} Movie", "movie"),
        ("Demon Slayer", "ds"),
        ("Attack on Titan", "aot")
    ]

def dummy_episodes(anime_id):
    """Returns 12 fake episodes"""
    return [(f"Episode {i+1}", str(i+1)) for i in range(12)]

def dummy_qualities():
    return [
        ("1080p (Best)", "1080p"),
        ("720p (Good)", "720p"),
        ("480p (Fast)", "480p")
    ]

def fake_play(anime, episode, quality):
    """Pretend to play an anime"""
    console.print("\n🎬 [bold green]Now Playing:[/bold green]")
    console.print(f"   📺 Anime: [cyan]{anime}")
    console.print(f"   🎬 Episode: [yellow]{episode}")
    console.print(f"   📶 Quality: [green]{quality}")
    console.print("\n🚧 This part still WIP. Streaming soon™", style="italic yellow")
    input("\n[Press Enter to continue]")

def interactive_mode():
    show_banner()
    console.print("\n🔍 Enter anime to search:")
    query = input("> ").strip()

    if not query:
        console.print("❌ You gotta type something!", style="red")
        return

    # Step 1: Search
    results = dummy_search(query)
    anime_id = fzf_select(results, "Select anime:")

    if not anime_id:
        console.print("❌ No anime picked", style="red")
        return

    anime_title = next(title for title, val in results if val == anime_id)

    # Step 2: Episode
    episodes = dummy_episodes(anime_id)
    ep = fzf_select(episodes, "Select episode:")
    if not ep:
        console.print("❌ No episode picked", style="red")
        return

    # Step 3: Quality
    quality = fzf_select(dummy_qualities(), "Select quality:")
    if not quality:
        console.print("❌ No quality picked", style="red")
        return

    # Step 4: Play
    fake_play(anime_title, ep, quality)

    # Step 5: Loop after play
    while True:
        action = fzf_select([
            ("▶️  Next", "next"),
            ("🔁 Replay", "replay"),
            ("⬅️  Prev", "prev"),
            ("📋 Pick another ep", "pick"),
            ("🎯 Change quality", "quality"),
            ("❌ Quit", "quit")
        ], f"Episode {ep} - What now?")

        if action == "quit" or not action:
            break
        elif action == "replay":
            fake_play(anime_title, ep, quality)
        elif action == "quality":
            new_q = fzf_select(dummy_qualities(), "Select quality:")
            if new_q:
                quality = new_q
                fake_play(anime_title, ep, quality)
        elif action == "pick":
            new_ep = fzf_select(episodes, "Pick another ep:")
            if new_ep:
                ep = new_ep
                fake_play(anime_title, ep, quality)
        elif action == "next":
            idx = next((i for i, (_, num) in enumerate(episodes) if num == ep), None)
            if idx is not None and idx + 1 < len(episodes):
                ep = episodes[idx + 1][1]
                fake_play(anime_title, ep, quality)
            else:
                console.print("❌ No next episode", style="red")
        elif action == "prev":
            idx = next((i for i, (_, num) in enumerate(episodes) if num == ep), None)
            if idx is not None and idx > 0:
                ep = episodes[idx - 1][1]
                fake_play(anime_title, ep, quality)
            else:
                console.print("❌ No previous episode", style="red")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="🦊 Kitsunari CLI - Stream anime from your terminal")
    parser.add_argument("query", nargs="*", help="Anime name to search for")
    parser.add_argument("-v", "--version", action="version", version="Kitsunari 0.1.0")
    args = parser.parse_args()

    try:
        console.print("🔧 Checking tools...", style="blue")
        check_dependencies()
        console.print("✅ All good!\n", style="green")

        if args.query:
            console.print(f"🔍 You searched: [cyan]{' '.join(args.query)}")
            console.print("⚠️  Direct search not ready yet. Launching interactive...", style="yellow")
            interactive_mode()
        else:
            interactive_mode()

    except KeyboardInterrupt:
        console.print("\n👋 Bye!", style="cyan")
        sys.exit(0)
    except Exception as e:
        console.print(f"💥 Error: {e}", style="bold red")
        sys.exit(1)

