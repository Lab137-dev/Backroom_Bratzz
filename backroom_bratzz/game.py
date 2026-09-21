from __future__ import annotations

import random
import time
from pathlib import Path

import pygame

from .assets import AssetBank
from .audio import MusicController
from .entities import Manager, Pickup, Player, Projectile
from .levels import Level, load_levels
from .save_data import SaveData
from .settings import ASSETS, COLORS, FPS, HEIGHT, LEVELS, TITLE, WIDTH, GameSettings


class Game:
    def __init__(self, settings: GameSettings, save: SaveData, save_path: Path):
        pygame.init()
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except pygame.error:
            pass
        flags = pygame.FULLSCREEN if settings.fullscreen else 0
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.settings = settings
        self.save = save
        self.save_path = save_path
        self.assets = AssetBank(ASSETS)
        self.assets.load()
        self.levels: list[Level] = load_levels(LEVELS)
        self.music = MusicController(ASSETS / "music", settings.music_volume)
        self.music.start()
        self.font_small = self.assets.font(18)
        self.font_tiny = self.assets.font(14)
        self.font_medium = self.assets.font(27)
        self.font_big = self.assets.font(52)
        self.running = True
        self.scene = "manager_intro"
        self.special_mode = "normal"
        self.character = "Alex"
        self.score = 0
        self.level_index = 0
        self.level_elapsed = 0.0
        self.spawn_clock = 0.0
        self.warning_count = 0
        self.pizzas = 0
        self.combo = 0
        self.ninja_unlocked = save.ninja_unlocked
        self.message = ""
        self.message_until = 0.0
        self.shake = 0.0
        self.player_group = pygame.sprite.GroupSingle()
        self.projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.managers = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()

    @property
    def level(self) -> Level:
        return self.levels[self.level_index]

    def start_game(self, character: str) -> None:
        self.character = character
        sprite = "alex" if character == "Alex" else "riley_l"
        if character == "Ninja":
            sprite = "ninja"
        self.player_group.empty()
        self.player_group.add(Player(self.assets.image(sprite), character))
        self.projectiles.empty()
        self.enemy_projectiles.empty()
        self.managers.empty()
        self.pickups.empty()
        self.score = 0
        self.level_index = 0
        self.level_elapsed = 0.0
        self.spawn_clock = 0.0
        self.warning_count = 0
        self.pizzas = 0
        self.combo = 0
        self.special_mode = "normal"
        self.music.play("shift_theme")
        self.scene = "playing"
        self.flash("SHIFT START — survive the managers!", 2.0)

    def finish_run(self, reason: str) -> None:
        self.scene = "game_over"
        self.special_mode = "normal"
        self.music.play("shift_theme")
        self.message = reason
        self.save.record(self.score, self.level_index + 1, self.ninja_unlocked)
        self.save.save(self.save_path)

    def flash(self, text: str, duration: float = 1.2) -> None:
        self.message = text
        self.message_until = time.monotonic() + duration

    def run(self) -> int:
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self.handle_events()
            if self.scene == "playing":
                self.update(dt)
            self.draw()
        pygame.quit()
        return 0

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_m:
                    self.music.toggle()
                elif event.key == pygame.K_f:
                    self.settings.fullscreen = not self.settings.fullscreen
                    flags = pygame.FULLSCREEN if self.settings.fullscreen else 0
                    self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
                elif self.scene == "manager_intro" and event.key in {pygame.K_RETURN, pygame.K_SPACE}:
                    self.scene = "title"
                elif self.scene in {"title", "game_over"}:
                    if event.key == pygame.K_1:
                        self.start_game("Alex")
                    elif event.key == pygame.K_2:
                        self.start_game("Riley-L")
                    elif event.key == pygame.K_3 and self.ninja_unlocked:
                        self.start_game("Ninja")
                elif self.scene == "playing" and event.key == pygame.K_SPACE:
                    self.shoot()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.scene == "manager_intro":
                    self.scene = "title"
                elif self.scene == "playing":
                    self.shoot()

    def shoot(self) -> None:
        player = self.player_group.sprite
        if not player:
            return
        now = time.monotonic()
        if not player.can_shoot(now):
            return
        player.last_shot = now
        image = self.assets.image("ninja_star" if player.name == "Ninja" else "rubber_band")
        velocities = [pygame.Vector2(0, -650)]
        if now < player.special_until and player.name == "Riley-L":
            velocities = [pygame.Vector2(-170, -620), pygame.Vector2(0, -670), pygame.Vector2(170, -620)]
        for velocity in velocities:
            self.projectiles.add(Projectile(image, player.rect.midtop, velocity))
        self.assets.play("shoot", self.settings.sound_volume)

    def spawn_manager(self) -> None:
        roll = random.random()
        special_present = any(m.kind in {"jazzy", "riley_not_l"} for m in self.managers)
        if not special_present and roll < 0.04:
            kind = "jazzy"
        elif not special_present and roll < 0.08:
            kind = "riley_not_l"
        else:
            normal_roll = random.random()
            kind = "danny" if normal_roll < 0.58 else "rea_rae" if normal_roll < 0.82 else "jaxon"
        image = self.assets.image(kind)
        speed = self.level.manager_speed * (1.35 if kind == "jaxon" else 0.9 if kind in {"jazzy", "riley_not_l"} else 1.0)
        self.managers.add(Manager(image, kind, speed, random.randint(105, 390)))

    def active_special(self) -> str:
        if any(manager.kind == "jazzy" for manager in self.managers):
            return "jazzy"
        if any(manager.kind == "riley_not_l" for manager in self.managers):
            return "riley_not_l"
        return "normal"

    def update_special_mode(self) -> str:
        mode = self.active_special()
        if mode != self.special_mode:
            self.special_mode = mode
            track = "jazzy_rush" if mode == "jazzy" else "riley_slow" if mode == "riley_not_l" else "shift_theme"
            self.music.play(track)
            if mode == "jazzy":
                self.flash("JAZZY PANIC!  EVERYBODY MOVE!", 1.8)
            elif mode == "riley_not_l":
                self.flash("RILEY-NOT-L: SLOOOOW SHIFT", 1.8)
        return mode

    def update(self, dt: float) -> None:
        self.level_elapsed += dt
        self.spawn_clock += dt
        mode = self.update_special_mode()
        if mode == "jazzy":
            player_dt, manager_dt, pickup_dt, shot_dt = dt * 1.25, dt * 1.75, dt * 1.5, dt * 1.15
        elif mode == "riley_not_l":
            player_dt = manager_dt = pickup_dt = shot_dt = dt * 0.55
        else:
            player_dt = manager_dt = pickup_dt = shot_dt = dt
        keys = pygame.key.get_pressed()
        self.player_group.update(player_dt, keys)
        self.projectiles.update(shot_dt)
        self.enemy_projectiles.update(shot_dt)
        self.managers.update(manager_dt)
        self.pickups.update(pickup_dt)

        if keys[pygame.K_SPACE]:
            self.shoot()
        if self.spawn_clock >= self.level.spawn_interval:
            self.spawn_clock = 0.0
            self.spawn_manager()
            if random.random() < self.level.box_rate:
                kind = "pizza" if random.random() < 0.58 else "star"
                self.pickups.add(Pickup(self.assets.image(kind), kind, random.randint(60, 900)))

        player = self.player_group.sprite
        if player:
            for manager in self.managers:
                if manager.kind == "danny" and manager.shot_clock <= 0:
                    direction = pygame.Vector2(player.rect.center) - pygame.Vector2(manager.rect.center)
                    if direction.length_squared():
                        direction.scale_to_length(300)
                    self.enemy_projectiles.add(
                        Projectile(self.assets.image("enemy_rubber_band"), manager.rect.center, direction)
                    )
                    manager.reset_shot()
                    self.assets.play("shoot", self.settings.sound_volume * 0.65)

        for manager in pygame.sprite.groupcollide(self.managers, self.projectiles, False, True):
            manager.hp -= 1
            self.score += 10 * max(1, self.combo)
            self.combo = min(8, self.combo + 1)
            self.assets.play("hit", self.settings.sound_volume)
            self.shake = 5.0
            if manager.hp <= 0:
                self.score += manager.value
                if manager.kind == "rea_rae":
                    self.warning_count += 1
                    self.flash(f"Rea-Rae warning {self.warning_count}/3!", 1.4)
                    self.assets.play("warning", self.settings.sound_volume)
                elif manager.kind == "jaxon" and not self.ninja_unlocked:
                    self.ninja_unlocked = True
                    self.flash("NINJA UNLOCKED!", 2.2)
                    self.assets.play("powerup", self.settings.sound_volume)
                manager.kill()

        if player:
            if pygame.sprite.spritecollide(player, self.enemy_projectiles, True):
                self.score = max(0, self.score - 100)
                self.combo = 0
                self.flash("DANNY SHOT BACK!  -100", 1.2)
                self.assets.play("warning", self.settings.sound_volume)
                self.shake = 7.0
            for pickup in pygame.sprite.spritecollide(player, self.pickups, True):
                if pickup.kind == "pizza":
                    self.pizzas += 1
                    if self.pizzas >= 3:
                        self.pizzas = 0
                        player.special_until = time.monotonic() + 7.0
                        self.flash("PIZZA POWER!", 1.5)
                        self.assets.play("powerup", self.settings.sound_volume)
                else:
                    self.score += 100
                    self.flash("STAR BONUS +100", 0.9)
                    self.assets.play("collect", self.settings.sound_volume)

        if self.warning_count >= 3:
            self.finish_run("FIRED — three manager warnings")
        elif self.level_elapsed >= self.level.duration:
            if self.score >= self.level.target_score:
                if self.level_index + 1 < len(self.levels):
                    self.level_index += 1
                    self.level_elapsed = 0.0
                    self.spawn_clock = 0.0
                    self.flash(f"LEVEL {self.level_index + 1}: {self.level.name}", 2.0)
                else:
                    self.finish_run("SHIFT COMPLETE — corporate survived you")
            else:
                self.finish_run(f"QUOTA MISSED — needed {self.level.target_score}")

        self.shake = max(0.0, self.shake - 18 * dt)

    def text(self, value: str, font: pygame.font.Font, color: tuple[int, int, int], pos: tuple[int, int], center: bool = False) -> None:
        surface = font.render(value, True, color)
        rect = surface.get_rect(center=pos) if center else surface.get_rect(topleft=pos)
        self.screen.blit(surface, rect)

    def draw(self) -> None:
        self.screen.blit(self.assets.image("background"), (0, 0))
        if self.scene == "manager_intro":
            self.draw_manager_intro()
        elif self.scene == "title":
            self.draw_title()
        elif self.scene == "playing":
            self.draw_playing()
        else:
            self.draw_game_over()
        pygame.display.flip()

    def draw_manager_intro(self) -> None:
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((3, 7, 18, 190))
        self.screen.blit(shade, (0, 0))
        self.text("MANAGER BRIEFING", self.font_big, COLORS["gold"], (480, 58), True)
        cards = [
            ("rea_rae", "REA-REA", "Defeat = warning", "Three warnings: FIRED"),
            ("jaxon", "JAXON", "Defeat to unlock", "the secret Ninja"),
            ("jazzy", "JAZZY", "Rare panic event", "Fast music + speed-up"),
            ("riley_not_l", "RILEY-NOT-L", "Rare slow event", "Slow music + slow-mo"),
        ]
        for index, (sprite, name, line1, line2) in enumerate(cards):
            x = 20 + index * 235
            pygame.draw.rect(self.screen, COLORS["panel"], (x, 115, 215, 350), border_radius=18)
            pygame.draw.rect(self.screen, COLORS["blue"], (x, 115, 215, 350), width=2, border_radius=18)
            image = pygame.transform.scale(self.assets.image(sprite), (108, 132))
            self.screen.blit(image, image.get_rect(center=(x + 108, 205)))
            self.text(name, self.font_medium, COLORS["ink"], (x + 108, 300), True)
            self.text(line1, self.font_tiny, COLORS["gold"], (x + 108, 350), True)
            self.text(line2, self.font_tiny, COLORS["muted"], (x + 108, 382), True)
        self.text("Jazzy and Riley-Not-L never appear together", self.font_small, COLORS["muted"], (480, 505), True)
        self.text("Press ENTER, SPACE, or click to continue", self.font_medium, COLORS["green"], (480, 552), True)

    def draw_title(self) -> None:
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((3, 7, 18, 128))
        self.screen.blit(shade, (0, 0))
        self.screen.blit(self.assets.image("logo"), self.assets.image("logo").get_rect(center=(480, 118)))
        self.text("BOSS SHIFT", self.font_big, COLORS["gold"], (480, 212), True)
        self.text("1  Alex — fastest rubber bands", self.font_medium, COLORS["ink"], (480, 300), True)
        self.text("2  Riley-L — faster movement + spread special", self.font_medium, COLORS["ink"], (480, 342), True)
        ninja = "3  Ninja — unlocked" if self.ninja_unlocked else "Ninja — defeat Jaxon to unlock"
        self.text(ninja, self.font_medium, COLORS["green"] if self.ninja_unlocked else COLORS["muted"], (480, 384), True)
        self.text("Move: A/D or arrows   Shoot: Space/click   F: fullscreen   M: music   Esc: quit", self.font_small, COLORS["muted"], (480, 476), True)
        self.text(f"High score: {self.save.high_score}", self.font_medium, COLORS["gold"], (480, 530), True)

    def draw_playing(self) -> None:
        offset = (random.randint(-int(self.shake), int(self.shake)), 0) if self.shake else (0, 0)
        layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for group in (self.pickups, self.managers, self.projectiles, self.enemy_projectiles, self.player_group):
            group.draw(layer)
        self.screen.blit(layer, offset)
        remaining = max(0, int(self.level.duration - self.level_elapsed))
        pygame.draw.rect(self.screen, (*COLORS["panel"], 235), (12, 10, 936, 58), border_radius=14)
        self.text(f"Score {self.score}", self.font_medium, COLORS["ink"], (28, 24))
        self.text(f"{self.level.name}  {remaining}s", self.font_medium, COLORS["blue"], (360, 24))
        self.text(f"Warnings {self.warning_count}/3   Pizza {self.pizzas}/3", self.font_small, COLORS["gold"], (680, 29))
        if self.special_mode == "jazzy":
            self.text("JAZZY PANIC x1.75", self.font_small, COLORS["red"], (480, 78), True)
        elif self.special_mode == "riley_not_l":
            self.text("RILEY-NOT-L SLOW-MO x0.55", self.font_small, COLORS["blue"], (480, 78), True)
        if time.monotonic() < self.message_until:
            self.text(self.message, self.font_medium, COLORS["gold"], (480, 92), True)

    def draw_game_over(self) -> None:
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((4, 7, 16, 205))
        self.screen.blit(shade, (0, 0))
        self.text(self.message, self.font_big, COLORS["red"], (480, 205), True)
        self.text(f"Score: {self.score}   Level: {self.level_index + 1}", self.font_medium, COLORS["ink"], (480, 290), True)
        self.text("Press 1 or 2 to work another shift", self.font_medium, COLORS["gold"], (480, 380), True)
        if self.ninja_unlocked:
            self.text("Press 3 for Ninja", self.font_medium, COLORS["green"], (480, 422), True)
