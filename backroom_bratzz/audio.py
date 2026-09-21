from __future__ import annotations

from pathlib import Path

import pygame


class MusicController:
    def __init__(self, music_path: Path, volume: float):
        self.path = music_path
        self.volume = volume
        self.enabled = pygame.mixer.get_init() is not None

    def start(self) -> None:
        if self.enabled and self.path.exists():
            pygame.mixer.music.load(self.path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)

    def toggle(self) -> bool:
        if not self.enabled:
            return False
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            return False
        pygame.mixer.music.unpause()
        return True

