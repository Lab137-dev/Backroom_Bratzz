from backroom_bratzz.save_data import SaveData


def test_save_round_trip(tmp_path):
    path = tmp_path / "save.json"
    data = SaveData(high_score=450, highest_level=2, ninja_unlocked=True, games_played=3)
    data.save(path)
    assert SaveData.load(path) == data


def test_bad_save_falls_back_to_defaults(tmp_path):
    path = tmp_path / "save.json"
    path.write_text("not-json", encoding="utf-8")
    assert SaveData.load(path) == SaveData()


def test_record_keeps_best_values():
    data = SaveData(high_score=900, highest_level=3)
    data.record(400, 1, True)
    assert data.high_score == 900
    assert data.highest_level == 3
    assert data.ninja_unlocked is True
    assert data.games_played == 1
