from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path


def user_data_dir() -> Path:
    base = os.getenv("APPDATA") if os.name == "nt" else os.getenv("XDG_DATA_HOME")
    if not base:
        base = str(Path.home() / ".local" / "share")
    return Path(base) / "LAB137" / "BackroomBratzz"


@dataclass(slots=True)
class SaveData:
    high_score: int = 0
    highest_level: int = 1
    ninja_unlocked: bool = False
    games_played: int = 0

    @classmethod
    def load(cls, path: Path) -> "SaveData":
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            allowed = cls.__dataclass_fields__.keys()
            return cls(**{key: raw[key] for key in allowed if key in raw})
        except (OSError, ValueError, TypeError):
            return cls()

    def record(self, score: int, level: int, ninja_unlocked: bool) -> None:
        self.high_score = max(self.high_score, int(score))
        self.highest_level = max(self.highest_level, int(level))
        self.ninja_unlocked = self.ninja_unlocked or ninja_unlocked
        self.games_played += 1

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
        temp.replace(path)

