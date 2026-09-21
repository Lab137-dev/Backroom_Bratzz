"""Generate the original LAB-137 placeholder art and audio shipped with the game."""
from __future__ import annotations

import math
import random
import shutil
import struct
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def font(size: int) -> ImageFont.FreeTypeFont:
    source = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    return ImageFont.truetype(source, size)


def save_character(name: str, shirt: str, hair: str, style: str = "short") -> None:
    image = Image.new("RGBA", (72, 88), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    if style in {"long_straight", "long_wavy", "long_blond"}:
        d.rounded_rectangle((15, 8, 57, 72), 17, fill=hair, outline="#eef5ff", width=2)
        if style == "long_wavy":
            for y in range(34, 72, 10):
                d.arc((10, y - 8, 27, y + 9), 270, 90, fill="#6c5149", width=3)
                d.arc((45, y - 8, 62, y + 9), 90, 270, fill="#6c5149", width=3)
    d.rounded_rectangle((16, 38, 56, 82), 10, fill=shirt, outline="#eef5ff", width=3)
    d.ellipse((20, 8, 52, 43), fill="#d69a73", outline="#eef5ff", width=3)
    if style != "bald":
        d.pieslice((18, 2, 55, 36), 180, 360, fill=hair)
    if style in {"short_grey_glasses", "curly_glasses"}:
        if style == "curly_glasses":
            for x, y in [(20, 8), (28, 5), (37, 4), (46, 7), (52, 14), (18, 17)]:
                d.ellipse((x - 7, y - 5, x + 7, y + 9), fill=hair)
        else:
            d.rectangle((20, 8, 52, 17), fill="#b9bdc6")
        d.rectangle((23, 20, 34, 29), outline="#303746", width=2)
        d.rectangle((38, 20, 49, 29), outline="#303746", width=2)
        d.line((34, 24, 38, 24), fill="#303746", width=2)
    d.ellipse((29, 22, 33, 26), fill="#132038")
    d.ellipse((41, 22, 45, 26), fill="#132038")
    d.arc((31, 24, 44, 35), 15, 165, fill="#8a3e42", width=2)
    if style == "bald":
        d.arc((28, 27, 46, 46), 5, 175, fill="#90949c", width=3)
        d.polygon([(31, 35), (43, 35), (40, 45), (34, 45)], fill="#8e9299")
        d.arc((22, 5, 51, 38), 190, 350, fill="#efbf99", width=2)
    if style == "ninja":
        d.rectangle((18, 15, 54, 31), fill="#171928")
        d.rectangle((26, 21, 47, 27), fill="#d69a73")
    image.save(ASSETS / "images" / f"{name}.png")


def icon(name: str, painter) -> None:
    image = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    painter(ImageDraw.Draw(image))
    image.save(ASSETS / "images" / f"{name}.png")


def tone(path: Path, notes: list[tuple[float, float]], volume: float = 0.3) -> None:
    rate = 44100
    frames: list[bytes] = []
    for frequency, duration in notes:
        count = int(rate * duration)
        for i in range(count):
            fade = min(1.0, i / 180, (count - i) / 250)
            sample = int(32767 * volume * fade * math.sin(2 * math.pi * frequency * i / rate))
            frames.append(struct.pack("<h", sample))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(b"".join(frames))


def music(path: Path, bpm: int = 118, pitch: float = 1.0, energy: float = 1.0) -> None:
    """Create a compact disco loop: four-on-the-floor kick, offbeat hats, bass, and stabs."""
    rate, bars = 44100, 6
    beat = 60 / bpm
    duration = bars * 4 * beat
    rng = random.Random(137)
    bass_notes = [55.0, 55.0, 65.41, 73.42, 55.0, 82.41, 73.42, 65.41]
    chord_notes = [(220.0, 277.18, 329.63), (261.63, 329.63, 392.0)]
    frames: list[bytes] = []
    for i in range(int(rate * duration)):
        t = i / rate
        beat_pos = t % beat
        half_pos = t % (beat / 2)
        beat_index = int(t / beat)
        eighth_index = int(t / (beat / 2))
        kick = math.sin(2 * math.pi * (62 - 24 * min(beat_pos / 0.12, 1)) * t) * math.exp(-beat_pos * 20)
        hat = (rng.random() * 2 - 1) * math.exp(-half_pos * 65) if eighth_index % 2 else 0
        bass_freq = bass_notes[eighth_index % len(bass_notes)] * pitch
        bass_phase = 2 * math.pi * bass_freq * t
        bass = (math.sin(bass_phase) + 0.28 * math.sin(2 * bass_phase)) * 0.42
        stab_age = (t - beat / 2) % beat
        stab = 0.0
        if stab_age < 0.13:
            chord = tuple(note * pitch for note in chord_notes[(beat_index // 4) % 2])
            stab = sum(math.sin(2 * math.pi * note * t) for note in chord) / 3 * math.exp(-stab_age * 18)
        sample = 0.48 * kick + 0.12 * hat * energy + 0.27 * bass + 0.18 * stab * energy
        frames.append(struct.pack("<h", int(max(-1, min(1, sample)) * 32767 * 0.72)))
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(b"".join(frames))


def draw_star(d: ImageDraw.ImageDraw) -> None:
    points = []
    for index in range(10):
        angle = math.radians(-90 + index * 36)
        radius = 17 if index % 2 == 0 else 7
        points.append((20 + math.cos(angle) * radius, 20 + math.sin(angle) * radius))
    d.polygon(points, fill="#ffd94a", outline="#fff5a3")


def main() -> None:
    for folder in ("images", "icons", "sounds", "music", "fonts", "levels"):
        (ASSETS / folder).mkdir(parents=True, exist_ok=True)

    bg = Image.new("RGB", (960, 600), "#091125")
    d = ImageDraw.Draw(bg)
    for y in range(0, 600, 48):
        d.rectangle((0, y, 960, y + 46), fill="#101c36" if y % 96 else "#132341")
    for x in range(30, 960, 155):
        d.rectangle((x, 105, x + 112, 470), fill="#263554", outline="#6581aa", width=4)
        for shelf in range(145, 455, 62):
            d.rectangle((x + 5, shelf, x + 107, shelf + 8), fill="#7e8da8")
            d.rectangle((x + 12, shelf - 29, x + 48, shelf), fill="#ad7046")
            d.rectangle((x + 55, shelf - 23, x + 99, shelf), fill="#8c5c3f")
    d.rectangle((0, 530, 960, 600), fill="#172039")
    bg.save(ASSETS / "images" / "background.png")

    logo = Image.new("RGBA", (620, 115), (0, 0, 0, 0))
    ld = ImageDraw.Draw(logo)
    ld.rounded_rectangle((4, 4, 616, 111), 24, fill="#121d39", outline="#4b9cff", width=5)
    ld.text((310, 56), "BACKROOM BRATZZ", anchor="mm", font=font(44), fill="#f4f7ff", stroke_width=2, stroke_fill="#326ec4")
    logo.save(ASSETS / "images" / "logo.png")

    app_icon = Image.new("RGBA", (256, 256), "#091125")
    icon_draw = ImageDraw.Draw(app_icon)
    icon_draw.rounded_rectangle((10, 10, 246, 246), 48, fill="#14234a", outline="#4b9cff", width=12)
    icon_draw.polygon([(128, 26), (154, 95), (228, 98), (170, 143), (188, 218), (128, 176), (68, 218), (86, 143), (28, 98), (102, 95)], fill="#ffc53e")
    icon_draw.text((128, 128), "BB", anchor="mm", font=font(72), fill="#091125")
    app_icon.save(ASSETS / "icons" / "backroom_bratzz.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    app_icon.save(ASSETS / "icons" / "backroom_bratzz.png")

    save_character("alex", "#f28a63", "#19151a", "long_straight")
    save_character("riley_l", "#ad70f6", "#211820", "long_wavy")
    save_character("ninja", "#303447", "#12131b", "ninja")
    save_character("danny", "#56657c", "#90949c", "bald")
    save_character("rea_rae", "#d34b62", "#b9bdc6", "short_grey_glasses")
    save_character("jaxon", "#87ceeb", "#9a6842", "short")
    save_character("jazzy", "#d97745", "#70452f", "curly_glasses")
    save_character("riley_not_l", "#63b6a4", "#f0c96a", "long_blond")

    icon("rubber_band", lambda d: d.ellipse((5, 14, 35, 26), outline="#64d9ff", width=5))
    icon("enemy_rubber_band", lambda d: d.ellipse((5, 14, 35, 26), outline="#ff596f", width=5))
    icon("ninja_star", lambda d: d.polygon([(20, 2), (25, 14), (38, 20), (25, 25), (20, 38), (15, 25), (2, 20), (15, 14)], fill="#dfe8f7", outline="#65748e"))
    icon("pizza", lambda d: (d.polygon([(5, 34), (35, 34), (20, 4)], fill="#ffd55f", outline="#bc7134"), d.ellipse((17, 20, 23, 26), fill="#df4553")))
    icon("star", draw_star)

    tone(ASSETS / "sounds" / "shoot.wav", [(850, 0.055)], 0.2)
    tone(ASSETS / "sounds" / "hit.wav", [(220, 0.08), (130, 0.06)], 0.28)
    tone(ASSETS / "sounds" / "collect.wav", [(620, 0.07), (880, 0.09)], 0.24)
    tone(ASSETS / "sounds" / "powerup.wav", [(440, 0.08), (660, 0.08), (990, 0.16)], 0.25)
    tone(ASSETS / "sounds" / "warning.wav", [(150, 0.18), (120, 0.18)], 0.3)
    music(ASSETS / "music" / "shift_theme.wav", bpm=118, pitch=1.0, energy=1.0)
    music(ASSETS / "music" / "jazzy_rush.wav", bpm=154, pitch=1.25, energy=1.4)
    music(ASSETS / "music" / "riley_slow.wav", bpm=82, pitch=0.72, energy=0.55)

    system_font = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    if system_font.exists():
        shutil.copy2(system_font, ASSETS / "fonts" / system_font.name)
    print(f"Generated game assets in {ASSETS}")


if __name__ == "__main__":
    main()
