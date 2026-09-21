from __future__ import annotations

from pathlib import Path

import pygame


class AssetBank:
    def __init__(self, root: Path):
        self.root = root
        self.images: dict[str, pygame.Surface] = {}
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self.font_path = root / "fonts" / "DejaVuSans-Bold.ttf"

    def load(self) -> None:
        image_dir = self.root / "images"
        for path in image_dir.glob("*.png"):
            self.images[path.stem] = pygame.image.load(path).convert_alpha()
        if pygame.mixer.get_init():
            for path in (self.root / "sounds").glob("*.wav"):
                self.sounds[path.stem] = pygame.mixer.Sound(path)

    def image(self, name: str) -> pygame.Surface:
        return self.images[name]

    def font(self, size: int) -> pygame.font.Font:
        return pygame.font.Font(self.font_path, size)

    def play(self, name: str, volume: float = 1.0) -> None:
        sound = self.sounds.get(name)
        if sound:
            sound.set_volume(volume)
            sound.play()

