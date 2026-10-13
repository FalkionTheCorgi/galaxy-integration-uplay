import pytest
import os
from local_file_parser import LocalParser


@pytest.fixture
def good_yaml():
    with open(os.path.join('tests', 'resources', 'good.yaml'), 'rb') as r:
        return r.read()


def test_parse_games_safely_loads_yaml(monkeypatch):
    parser = LocalParser()
    configuration_data = b"root:\n  start_game: {}\n"
    game_record = {
        "offset": 0,
        "size": len(configuration_data),
        "install_id": "123",
        "launch_id": "456",
    }
    monkeypatch.setattr(parser, "_parse_configuration", lambda: {"game": game_record})
    monkeypatch.setattr(
        parser,
        "_parse_game",
        lambda game_yaml, install_id, launch_id: (game_yaml, install_id, launch_id),
    )

    assert list(parser.parse_games(configuration_data)) == [
        ({"root": {"start_game": {}}}, "123", "456")
    ]


# TODO mock registry
# def test_yaml_decent_parse(good_yaml):
#     count = 0
#     p = LocalParser(good_yaml)
#     p.parse_configuration()
#     for game in p.parse_games():
#         count += 1
#     assert count == 36
