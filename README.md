# PROJECT KITSUNARI | キツナーリ v1.0.1

**Modern Terminal UI for anime streaming**
A sleek, interactive TUI application for browsing and watching anime, powered by a custom backend built on `anipy-api` and Textual.
GUI version planned for future release.

---

## Features

* **Rich Terminal Interface** – Interactive TUI with mouse support
* **Reliable Backend** – Fast-ish synchronous anime fetching using `anipy-api`
* **Modern UX** – Browse anime with panels, tabs, and real-time updates
* **Keyboard & Mouse Navigation** – Arrow keys, Enter, Tab, and clickable items
* **Episode Management** – Queue episodes, track progress, seamless playback
* **Clean Architecture** – Modular design ready for GUI expansion

---

## OS support
**Linux (recommended)** – fully tested  
**macOS** – might work, not fully tested  
**Windows** – probably won’t work, use Linux for best experience

---

## Installation

```bash
# clone the repo
git clone https://github.com/XeonXE534/Kitsunari.git
cd Kitsunari

# optional but recommended: create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS

# install Kitsunari
pip install .
```

---

## Usage

Just run:

```bash
kitsunari
```

## Requirements

* **Python 3.10+**
* **Anipy-api** – Fast, reliable anime sources
* **Textual** – Powers the terminal user interface
* **Media player** – MPV must be installed and available in your PATH for playback.

---

## Project Structure

```
kitsunari/
├── docs/                     # Documentation
├── LICENSE                   # License file
├── logs/                     # Logging utilities
├── pyproject.toml            # Build and project config
├── README.md                 # Readme
├── src/
│   └──── kitsunari_tui/
│       ├── backend/          # Synchronous anime backend
│       ├── css/              # Stylesheets for Textual screens
│       ├── main.py           # Entry point
│       └── screens/          # Individual TUI screens/views
└── tests/                    # Unit tests

```

---

## Screenshots

*Coming soon – TUI interface screenshots*

---

## Roadmap

* [x] ~~CLI-based anime streaming~~ → **TUI Implementation**
* [ ] Enhanced episode browsing and search
* [ ] User preferences and watch history
* [ ] Multiple anime source support
* [ ] GUI version with Qt/PySide
* [ ] Cross-platform distribution

---

## Why Kitsunari?

While CLI tools like Ani-cli and Anipy-cli are great, Kitsunari focuses on **user experience**.
It provides a modern, intuitive interface for discovering and watching anime while keeping the backend reliable and fast-ish.

---

## Notes

- UI styling is rough – expect wonky layouts, broken CSS and all of that 
- Some minor bugs may exist (search, playback)  
- Only Linux fully supported 
- MPV must be installed and available in your PATH for playback.
- This version uses `backend_v2` which is the older but *FAR* more stable backend.
- Check out the `backend_v3` branch for the latest backend code (NOT RECOMMENDED FOR DAILY USE, UNSTABLE)

---

## Contributing

Contributions welcome!
Fork, tweak, and submit PRs, any improvements are welcome.

---

## License

GPL 3.0 – see LICENSE file for details

*Built with ❤️ for the anime community*

## Credits
Anipy [https://github.com/sdaqo/anipy-cli]
Textual [https://github.com/textualize/textual/]