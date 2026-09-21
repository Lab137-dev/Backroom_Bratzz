import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from backroom_bratzz.game import Game
from backroom_bratzz.save_data import SaveData
from backroom_bratzz.settings import GameSettings


def test_game_initializes_and_starts(tmp_path):
    game = Game(GameSettings(), SaveData(), tmp_path / "save.json")
    game.start_game("Alex")
    assert game.scene == "playing"
    assert game.player_group.sprite.name == "Alex"
    game.running = False

