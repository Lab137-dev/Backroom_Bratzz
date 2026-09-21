from __future__ import annotations

import argparse
import os

from .game import Game
from .save_data import SaveData, user_data_dir
from .settings import GameSettings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Backroom Bratzz: Boss Shift")
    parser.add_argument("--headless", action="store_true", help="Use SDL dummy drivers for diagnostics")
    args = parser.parse_args(argv)
    if args.headless:
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
        os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    data_dir = user_data_dir()
    settings_path = data_dir / "settings.json"
    save_path = data_dir / "save.json"
    settings = GameSettings.load(settings_path)
    game = Game(settings, SaveData.load(save_path), save_path)
    try:
        return game.run()
    finally:
        settings.save(settings_path)


if __name__ == "__main__":
    raise SystemExit(main())

