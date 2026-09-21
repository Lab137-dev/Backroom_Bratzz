from backroom_bratzz.settings import GameSettings


def test_settings_clamp_volume(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text('{"music_volume": 9, "sound_volume": -2}', encoding="utf-8")
    settings = GameSettings.load(path)
    assert settings.music_volume == 1.0
    assert settings.sound_volume == 0.0


def test_settings_round_trip(tmp_path):
    path = tmp_path / "settings.json"
    expected = GameSettings(fullscreen=True, music_volume=0.2)
    expected.save(path)
    assert GameSettings.load(path) == expected

