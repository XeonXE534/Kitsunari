# PROJECT KITSUNARI | キツナーリ v1.1.0-beta

**Modern Terminal UI for anime streaming.**  
A beautiful, interactive TUI application for browsing and watching anime, powered by anipy-cli and Textual.  
GUI version planned for future release.

---

## Features

- **Rich Terminal Interface** - Beautiful, interactive TUI with mouse support
- **Powered by anipy-cli** - Reliable anime sources and streaming backend  
- **Modern UX** - Browse anime with panels, tabs, and real-time updates
- **Keyboard & Mouse** - Navigate with arrow keys or click to interact
- **Episode Management** - Queue episodes, track progress, and seamless playback
- **Clean Architecture** - Modular design ready for GUI expansion

---

## Installation

```bash
git clone git@github.com:XeonXE534/Kitsunari.git
cd Kitsunari
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Launch the TUI application:
```bash
python -m src.kitsunari_tui.app
```

### Controls (THESE MAY CHANGE!!!!!)
- `Ctrl+Q` - Exit application
- `Tab` - Navigate between panels
- `Enter` - Select item
- `b` - Go back
- Mouse clicks work throughout the interface

## Requirements

- **Python 3.8+**
- **anipy-cli** - Handles anime sources and streaming
- **textual** - Powers the terminal user interface
- **Media player** - mpv recommended for best experience

## Project Structure

```
kitsunari/
├── src/
│   ├── kitsunari_tui/
│   │   ├── app.py              # Main Textual application
│   │   ├── main.py             # Entry point
│   │   ├── backend/            # anipy-cli integration
│   │   ├── widgets/            # Custom TUI components  
│   │   ├── screens/            # Different app views
│   │   └── player.py           # Media player integration
│   └── kitsunari_gui/          # Future GUI version
├── tests/                      # Unit tests
├── NOTES.md                    # Development reference
└── requirements.txt            # Dependencies
```

## Screenshots

*Coming soon - TUI interface screenshots*

## Roadmap

- [x] ~~CLI-based anime streaming~~ → **TUI Implementation**
- [ ] Enhanced episode browsing and search
- [ ] User preferences and watch history  
- [ ] Multiple anime source support
- [ ] GUI version with Qt/PySide
- [ ] Cross-platform distribution

## Why Kitsunari?

While excellent CLI tools like ani-cli and anipy-cli exist, Kitsunari focuses on the **user experience**. It provides a modern, intuitive interface that makes anime discovery and watching more enjoyable, while leveraging proven backends for reliability.

## Contributing

Contributions welcome! This project uses:
- **Backend**: anipy-cli for anime sources
- **Frontend**: Textual for the TUI
- **Future**: PySide6 for GUI

Feel free to fork and submit pull requests.

## License

This project is licensed under GPL 3.0 - see the LICENSE file for details.

*Built with ❤️ for the anime community*
