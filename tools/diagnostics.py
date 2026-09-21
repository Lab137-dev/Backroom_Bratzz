from __future__ import annotations

import json
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from backroom_bratzz.assets import AssetBank
from backroom_bratzz.levels import load_levels
from backroom_bratzz.settings import ASSETS, LEVELS


def main() -> int:
    errors: list[str] = []
    pygame.init()
    pygame.display.set_mode((16, 16))
    bank = AssetBank(ASSETS)
    try:
        bank.load()
    except Exception as exc:
        errors.append(f"Asset load failed: {exc}")

    required_images = {"alex", "riley_l", "ninja", "danny", "rea_rae", "jaxon", "jazzy", "riley_not_l", "rubber_band", "enemy_rubber_band", "ninja_star", "pizza", "star", "background", "logo"}
    missing = required_images.difference(bank.images)
    if missing:
        errors.append(f"Missing images: {', '.join(sorted(missing))}")
    if not bank.font_path.exists():
        errors.append("Bundled font is missing")
    for track in ("shift_theme.wav", "jazzy_rush.wav", "riley_slow.wav"):
        if not (ASSETS / "music" / track).exists():
            errors.append(f"Missing music track: {track}")
    try:
        levels = load_levels(LEVELS)
        if len(levels) < 3:
            errors.append("Expected at least three levels")
    except Exception as exc:
        errors.append(f"Level validation failed: {exc}")

    report = {"pygame": pygame.version.ver, "images": len(bank.images), "sounds": len(bank.sounds), "levels": len(list(LEVELS.glob('*.json'))), "errors": errors}
    print(json.dumps(report, indent=2))
    pygame.quit()
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
