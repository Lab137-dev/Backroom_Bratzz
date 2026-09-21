from __future__ import annotations

import math
import random

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, name: str):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midbottom=(480, 566))
        self.name = name
        self.speed = 390 if name == "Riley-L" else 345
        self.cooldown = 0.13 if name == "Alex" else 0.18
        self.last_shot = -10.0
        self.special_until = 0.0

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper) -> None:
        direction = keys[pygame.K_d] + keys[pygame.K_RIGHT] - keys[pygame.K_a] - keys[pygame.K_LEFT]
        self.rect.x += round(direction * self.speed * dt)
        self.rect.clamp_ip(pygame.Rect(24, 0, 912, 574))

    def can_shoot(self, now: float) -> bool:
        rate = self.cooldown * (0.42 if now < self.special_until else 1.0)
        return now - self.last_shot >= rate


class Projectile(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, pos: tuple[int, int], velocity: pygame.Vector2):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=pos)
        self.pos = pygame.Vector2(self.rect.center)
        self.velocity = velocity

    def update(self, dt: float) -> None:
        self.pos += self.velocity * dt
        self.rect.center = self.pos
        if self.rect.bottom < -20 or self.rect.top > 640 or not (-40 < self.rect.centerx < 1000):
            self.kill()


class Manager(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, kind: str, speed: float, y: int):
        super().__init__()
        self.image = image
        self.kind = kind
        self.hp = 3 if kind in {"rea_rae", "jaxon"} else 1
        self.max_hp = self.hp
        self.value = 120 if kind == "jaxon" else 80
        from_left = random.choice((True, False))
        self.rect = image.get_rect(midleft=(-image.get_width(), y)) if from_left else image.get_rect(midright=(960 + image.get_width(), y))
        self.pos = pygame.Vector2(self.rect.center)
        self.velocity = speed if from_left else -speed
        self.phase = random.random() * math.tau

    def update(self, dt: float) -> None:
        self.phase += dt * 3
        self.pos.x += self.velocity * dt
        self.pos.y += math.sin(self.phase) * 18 * dt
        self.rect.center = self.pos
        if self.rect.right < -80 or self.rect.left > 1040:
            self.kill()


class Pickup(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, kind: str, x: int):
        super().__init__()
        self.image = image
        self.kind = kind
        self.rect = image.get_rect(midtop=(x, -30))
        self.pos = pygame.Vector2(self.rect.center)

    def update(self, dt: float) -> None:
        self.pos.y += 155 * dt
        self.rect.center = self.pos
        if self.rect.top > 620:
            self.kill()

