from __future__ import annotations

from pathlib import Path

import pygame


class MusicController:
    def __init__(self, music_folder: Path, volume: float):
        self.folder = music_folder
        self.volume = volume
        self.enabled = pygame.mixer.get_init() is not None
        self.current = ""
        self.paused = False

    def play(self, track: str = "shift_theme") -> None:
        path = self.folder / f"{track}.wav"
        if self.enabled and path.exists() and track != self.current:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
            self.current = track
            self.paused = False

    def start(self) -> None:
        self.play("shift_theme")

    def toggle(self) -> bool:
        if not self.enabled:
            return False
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            return False
        pygame.mixer.music.unpause()
        self.paused = False
        return True
