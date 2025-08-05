# PROJECT KITSUNARI | キツナーリ

**Terminal-based anime streaming tool for Linux.**  
A lightweight, efficient command-line interface for searching and playing anime.  
GUI version planned for future release.

---

## Features

- Fast, interactive anime search powered by fuzzy matching (`fzf`).
- Episode selection with multiple video quality options.
- Integration-ready for popular CLI media players like `mpv` and `vlc`.
- Clean, modular Python codebase built with maintainability in mind.

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

Run the CLI tool with:
```
   python -m src.kitsunari_cli.main
```
## Requirements

    Python 3.8 or higher

    fzf installed and available in your system PATH

    A CLI-compatible media player (e.g., mpv, vlc)

Project Structure
```
kitsunari/
├── src/
│   ├── kitsunari_cli/
│   │   ├── cli.py         # CLI interface and logic
│   │   ├── main.py        # Main entry point
│   │   ├── extractors/    # Site-specific extraction logic
│   │   ├── scrapers/      # Web scraping modules
│   │   └── utils/         # Helper utilities
├── tests/                 # Unit tests
├── requirements.txt       # Python dependencies
├── setup.py               # Package configuration
└── README.md              # Project overview
```

## Roadmap

- [ ] Add GUI version for desktop users.
- [ ] Implement caching for faster repeated queries.
- [ ] Add watch history and user preferences.
- [ ] Expand scraper support for additional anime streaming sources.

## Contributing

Contributions, issues, and feature requests are welcome.
Feel free to fork the repo and submit pull requests.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## Notes

This project was inspired by ani-cli. I did not and do not use any of their code. Any similarites are pure coincidence 
