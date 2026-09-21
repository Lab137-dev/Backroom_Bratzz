import json

import pytest

from backroom_bratzz.levels import load_level, load_levels


def test_repository_levels_load():
    from backroom_bratzz.settings import LEVELS

    levels = load_levels(LEVELS)
    assert len(levels) == 3
    assert levels[0].target_score > 0


def test_level_validation_reports_missing_fields(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"name": "Incomplete"}), encoding="utf-8")
    with pytest.raises(ValueError, match="missing"):
        load_level(path)

