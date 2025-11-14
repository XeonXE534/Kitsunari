<p>
  <img src="images/halo.png" alt="logo" width="50" style="vertical-align:middle;">
  <strong style="font-size:1.5em;">v2.1.1</strong>
</p>


**Modern Terminal UI for anime streaming**
A sleek, interactive TUI application for browsing and watching anime, powered by a custom backend built on `anipy-api` and Textual.
GUI version planned for future release.

---

## Features

* **Rich Terminal Interface** – Interactive TUI with mouse support
* **Reliable Backend** – Fast-ish synchronous anime fetching using `anipy-api`
* **Modern UX** – Browse anime with panels, tabs, and real-time updates
* **Episode Management** – Queue episodes, track progress*, seamless playback
* **Fast Releases** – Quickly access the latest anime releases

---

## Installation
```bash
# Clone the repo
git clone https://github.com/XeonXE534/Project-Ibuki.git
cd Project-Ibuki

# Run the installer
bash ./install.sh
```

After installation, you can run Project-Ibuki anywhere using:
`ibuki`

## Requirements

* **Python 3.10+**
* **Anipy-api**
* **Textual**
* **MPV**

---

## Screenshots

![Home screen](images/home.png)
![Search screen](images/search.png)
![Anime Details screen](images/synopsis.png)
![Episodes screen](images/ep.png)

---

## Roadmap

* [x] ~~CLI-based anime streaming~~ → **TUI Implementation**
* [x] Enhanced episode browsing and search
* [x] Watch history
* [ ] User preferences
* [ ] GUI version with Qt/PySide
* [ ] Cross-platform distribution

---

## Notes

- Some minor bugs may exist (search, playback)  
- Continue Watching is broken as of v2.x.x
- Only Linux fully supported 
- MPV must be installed and available in your PATH for playback.
- This version uses `backend_v2.5` which is the stable backend.
- Check out the `test_branch` branch for the unstable beta backend (NOT RECOMMENDED FOR DAILY USE, UNSTABLE)
- Check out the `backend_v3` branch for a (hopefully) faster backend (NOT RECOMMENDED FOR DAILY USE, UNSTABLE AND UNDER DEVELOPMENT)

---

## Contributing

Contributions welcome!
Fork, tweak, and submit PRs, any improvements are welcome.

---

## License

GPL 3.0 – see LICENSE file for details

## Credits
- Backend: [Anipy](https://github.com/sdaqo/anipy-cli)
- UI: [Textual](https://github.com/textualize/textual/)


*Built with ❤️ for the anime community*
