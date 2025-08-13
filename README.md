# PROJECT KITSUNARI | キツナーリ v1.0.0

**Modern Terminal UI for anime streaming**
A sleek, interactive TUI application for browsing and watching anime, powered by a custom backend built on `anipy-api` and Textual.
GUI version planned for future release.

---

## Features

* **Rich Terminal Interface** – Interactive TUI with mouse support
* **Reliable Backend** – Fast-ish threaded anime fetching using `anipy-api`
* **Modern UX** – Browse anime with panels, tabs, and real-time updates
* **Keyboard & Mouse Navigation** – Arrow keys, Enter, Tab, and clickable items
* **Episode Management** – Queue episodes, track progress, seamless playback
* **Clean Architecture** – Modular design ready for GUI expansion

---

## Installation

```bash
git clone git@github.com:XeonXE534/Kitsunari.git
cd Kitsunari
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

Launch the TUI application:

```bash
python -m src.kitsunari_tui.main
```

## Requirements

* **Python 3.8+**
* **anipy-api** – Fast, reliable anime sources
* **textual** – Powers the terminal user interface
* **Media player** – mpv recommended

---

## Project Structure

```
kitsunari/
├── src/
│   ├── kitsunari_tui/
│   │   ├── app.py              # Main Textual application
│   │   ├── main.py             # Entry point
│   │   ├── backend/            # Anime backend (fast-ish threaded fetch)
│   │   ├── widgets/            # Custom TUI components  
│   │   ├── screens/            # Different app views
│   │   └── player.py           # Media player integration
│   └── kitsunari_gui/          # Future GUI version
├── tests/                      # Unit tests
├── NOTES.md                    # Development notes
└── requirements.txt            # Dependencies
```

---

## Screenshots

*Coming soon – TUI interface screenshots*

---

## Roadmap

* [x] CLI-based anime streaming → **TUI Implementation**
* [ ] Enhanced episode browsing and search
* [ ] User preferences and watch history
* [ ] Multiple anime source support
* [ ] GUI version with Qt/PySide
* [ ] Cross-platform distribution

---

## Why Kitsunari?

While CLI tools like ani-cli and anipy-cli are great, Kitsunari focuses on **user experience**.
It provides a modern, intuitive interface for discovering and watching anime while keeping the backend reliable and fast-ish.

---

## Contributing

Contributions welcome!

* **Backend:** Custom threaded `anipy-api` integration
* **Frontend:** Textual for TUI
* **Future GUI:** PySide6

Fork, tweak, and submit PRs—any improvements are welcome.

---

## License

GPL 3.0 – see LICENSE file for details

*Built with ❤️ for the anime community*