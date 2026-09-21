# Backroom Bratzz: Boss Shift

An upgraded, modular Python edition of the original **Backroom Bratzz Deluxe** browser game.

Choose Alex or Riley-L, fire rubber bands across an increasingly chaotic retail backroom, collect pizza power-ups, survive Rea-Rae's warnings, and defeat Jaxon to unlock Ninja. This edition expands the original joke into a structured Pygame project with multiple levels, persistent progress, original bundled assets, diagnostics, tests, Windows packaging, and automated builds.

> This is an independent fictional parody inspired by retail work. It is not affiliated with or endorsed by TJX, TJ Maxx, or any retailer.

## Quick start

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
python run_game.py
```

macOS or Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python run_game.py
```

Windows users can also double-click `launch_windows.bat`; it creates a local virtual environment and installs the runtime dependency on first launch.

## Controls

| Action | Control |
|---|---|
| Select Alex / Riley-L | `1` / `2` |
| Select unlocked Ninja | `3` |
| Move | `A` / `D` or left/right arrows |
| Shoot | Space or mouse click |
| Fullscreen | `F` |
| Music | `M` |
| Quit | Escape |

## Characters

- **Alex** fires rubber bands faster. Pizza Power increases that fire rate dramatically.
- **Riley-L** moves faster. Pizza Power changes the weapon into a three-way spread.
- **Ninja** is permanently unlocked after defeating Jaxon and uses ninja stars.

## Rules

- Managers take multiple hits and award score.
- Defeating Rea-Rae generates a warning. Three warnings ends the shift.
- Defeating Jaxon unlocks Ninja permanently.
- Collect three pizzas to activate a seven-second character special.
- Stars award bonus points.
- Meet each department's quota before its timer expires.

## Project structure

```text
backroom_bratzz/       Python package and game systems
assets/
  images/              Original PNG sprites and background
  sounds/              Original WAV sound effects
  music/               Original looping shift theme
  fonts/               Bundled DejaVu font and attribution
  levels/              Data-driven JSON level definitions
packaging/             PyInstaller configuration
tests/                 Unit and headless smoke tests
tools/                 Asset generator and diagnostics
.github/workflows/     Linux tests and Windows executable build
run_game.py            Development entry point
```

## Save data and settings

Progress and preferences are stored outside the repository:

- Windows: `%APPDATA%\LAB137\BackroomBratzz`
- Linux: `$XDG_DATA_HOME/LAB137/BackroomBratzz` or `~/.local/share/LAB137/BackroomBratzz`

The game saves high score, highest level, Ninja unlock state, games played, audio volume, fullscreen preference, high contrast, and screen shake settings. Invalid or missing save files safely fall back to defaults.

## Development

Install development tools:

```bash
pip install -r requirements-dev.txt
```

Regenerate the original art and audio:

```bash
python tools/generate_assets.py
```

Run checks:

```bash
ruff check .
pytest -q
python -m tools.diagnostics
```

## Build a Windows executable

```powershell
pyinstaller packaging/backroom_bratzz.spec --noconfirm
```

The packaged game will be written to `dist/BackroomBratzz/`. The GitHub Actions Windows workflow also creates a downloadable build artifact.

## Credits and licensing

Game design, code, original sprites, sound effects, and music: **Danny Morgan / LAB-137**.

See [assets/credits.md](assets/credits.md) for third-party asset attribution. Code and original LAB-137 assets are released under the [MIT License](LICENSE). The bundled DejaVu font retains its own license.

The original single-file browser edition remains available in this repository's `main` branch history.
