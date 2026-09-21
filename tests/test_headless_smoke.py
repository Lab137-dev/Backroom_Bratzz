import os
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

from backroom_bratzz.game import Game
from backroom_bratzz.save_data import SaveData
from backroom_bratzz.settings import GameSettings


def test_game_initializes_and_starts(tmp_path):
    game = Game(GameSettings(), SaveData(), tmp_path / "save.json")
    assert game.scene == "manager_intro"
    game.start_game("Alex")
    assert game.scene == "playing"
    assert game.player_group.sprite.name == "Alex"
    game.running = False


def test_special_managers_do_not_overlap(tmp_path):
    game = Game(GameSettings(), SaveData(), tmp_path / "save.json")
    game.start_game("Alex")
    with patch("backroom_bratzz.game.random.random", return_value=0.01):
        game.spawn_manager()
        game.spawn_manager()
    kinds = [manager.kind for manager in game.managers]
    assert kinds.count("jazzy") == 1
    assert "riley_not_l" not in kinds
    game.running = False
