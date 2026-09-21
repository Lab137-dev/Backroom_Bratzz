from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Level:
    name: str
    duration: float
    target_score: int
    spawn_interval: float
    manager_speed: float
    box_rate: float
    palette: str


def load_level(path: Path) -> Level:
    raw = json.loads(path.read_text(encoding="utf-8"))
    required = {"name", "duration", "target_score", "spawn_interval", "manager_speed", "box_rate", "palette"}
    missing = required.difference(raw)
    if missing:
        raise ValueError(f"Level {path.name} is missing: {', '.join(sorted(missing))}")
    return Level(**{key: raw[key] for key in required})


def load_levels(folder: Path) -> list[Level]:
    levels = [load_level(path) for path in sorted(folder.glob("*.json"))]
    if not levels:
        raise FileNotFoundError(f"No levels found in {folder}")
    return levels

