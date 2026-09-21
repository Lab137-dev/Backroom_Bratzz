from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

TITLE = "Backroom Bratzz: Boss Shift"
WIDTH, HEIGHT = 960, 600
FPS = 60

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
LEVELS = ASSETS / "levels"

COLORS = {
    "ink": (242, 246, 255),
    "muted": (163, 174, 204),
    "navy": (10, 16, 32),
    "panel": (20, 29, 54),
    "blue": (73, 156, 255),
    "gold": (255, 197, 62),
    "green": (86, 219, 132),
    "red": (246, 82, 102),
}


@dataclass(slots=True)
class GameSettings:
    fullscreen: bool = False
    music_volume: float = 0.45
    sound_volume: float = 0.75
    high_contrast: bool = False
    screen_shake: bool = True

    def normalized(self) -> "GameSettings":
        self.music_volume = max(0.0, min(1.0, float(self.music_volume)))
        self.sound_volume = max(0.0, min(1.0, float(self.sound_volume)))
        return self

    @classmethod
    def load(cls, path: Path) -> "GameSettings":
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            allowed = cls.__dataclass_fields__.keys()
            return cls(**{key: raw[key] for key in allowed if key in raw}).normalized()
        except (OSError, ValueError, TypeError):
            return cls()

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")

