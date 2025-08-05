# Imports
import subprocess
import sys
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

console = Console()

# Dependency check
def check_depends():
    deps = ['fzf']
    missing = []

    for dep in deps:
        try:
            subprocess.run([dep, '--version'], capture_output=True, check=True)
        except:
            missing.append(dep)
    if missing:
        console.print(f' Missing deps: {','.join(missing)} :/', style='bold red')
        console.print(' Install fzf from: https://github.com/junegunn/fzf!', style='yellow')
        sys.exit(1)

# Banner
def banner():
    banner_txt = Text('Kitsunāri | キツナーリ: CLI', style='dark_orange')
    subtitle = Text('Version: 0.1.0', style='deep_pink2')
    group = Group(banner_txt, subtitle)
    console.print(Panel.fit(group, border_style='red1'))

# Fuzzy search
def fzf_select(items, prompt='Select one :3'):
    if not items:
        console.print('Error! :/', style='red1')
        return None

    is_tuple = isinstance(items[0], tuple)
    display_list = [x[0] if is_tuple else x for x in items] # Refer FZF part in docs for explanation

    fzf_input = '\n'.join(display_list)
    cmd = ["fzf", "--reverse", "--cycle", "--height", "40%", "--border", "--prompt", prompt]



