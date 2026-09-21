"""Generate the original LAB-137 placeholder art and audio shipped with the game."""
from __future__ import annotations

import math
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


def save_character(name: str, shirt: str, hair: str, accessory: str = "") -> None:
    image = Image.new("RGBA", (72, 88), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)
    d.rounded_rectangle((16, 38, 56, 82), 10, fill=shirt, outline="#eef5ff", width=3)
    d.ellipse((20, 8, 52, 43), fill="#d69a73", outline="#eef5ff", width=3)
    d.pieslice((18, 2, 55, 36), 180, 360, fill=hair)
    d.ellipse((29, 22, 33, 26), fill="#132038")
    d.ellipse((41, 22, 45, 26), fill="#132038")
    d.arc((31, 24, 44, 35), 15, 165, fill="#8a3e42", width=2)
    if accessory == "ninja":
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


def music(path: Path) -> None:
    melody = [110, 146.83, 164.81, 146.83, 123.47, 164.81, 196, 164.81] * 4
    tone(path, [(note, 0.24) for note in melody], 0.12)


def main() -> None:
    for folder in ("images", "sounds", "music", "fonts", "levels"):
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

    save_character("alex", "#f28a63", "#43251f")
    save_character("riley_l", "#ad70f6", "#e2c082")
    save_character("ninja", "#303447", "#12131b", "ninja")
    save_character("rea_rae", "#d34b62", "#251b1c")
    save_character("jaxon", "#4c96d6", "#64402c")
    save_character("supervisor", "#6d788e", "#353535")

    icon("rubber_band", lambda d: d.ellipse((5, 14, 35, 26), outline="#64d9ff", width=5))
    icon("ninja_star", lambda d: d.polygon([(20, 2), (25, 14), (38, 20), (25, 25), (20, 38), (15, 25), (2, 20), (15, 14)], fill="#dfe8f7", outline="#65748e"))
    icon("pizza", lambda d: (d.polygon([(5, 34), (35, 34), (20, 4)], fill="#ffd55f", outline="#bc7134"), d.ellipse((17, 20, 23, 26), fill="#df4553")))
    icon("star", lambda d: d.regular_polygon((20, 20, 17), 5, rotation=-18, fill="#ffd94a", outline="#fff5a3"))

    tone(ASSETS / "sounds" / "shoot.wav", [(850, 0.055)], 0.2)
    tone(ASSETS / "sounds" / "hit.wav", [(220, 0.08), (130, 0.06)], 0.28)
    tone(ASSETS / "sounds" / "collect.wav", [(620, 0.07), (880, 0.09)], 0.24)
    tone(ASSETS / "sounds" / "powerup.wav", [(440, 0.08), (660, 0.08), (990, 0.16)], 0.25)
    tone(ASSETS / "sounds" / "warning.wav", [(150, 0.18), (120, 0.18)], 0.3)
    music(ASSETS / "music" / "shift_theme.wav")

    system_font = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    if system_font.exists():
        shutil.copy2(system_font, ASSETS / "fonts" / system_font.name)
    print(f"Generated game assets in {ASSETS}")


if __name__ == "__main__":
    main()

