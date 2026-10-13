import json
import re
from urllib.parse import parse_qs, quote, urlparse

from consts import AUTH_JS, AUTH_PARAMS, CLUB_APPID, CLUB_GENOME_ID
from plugin import _parse_auth_storage_jsons
import pytest


def test_auth_callback_uses_live_login_route():
    parameters = parse_qs(urlparse(AUTH_PARAMS["start_uri"]).query)
    callback = parameters["nextUrl"][0]
    matching_patterns = [pattern for pattern in AUTH_JS if re.fullmatch(pattern, callback)]

    assert parameters["appId"] == [CLUB_APPID]
    assert parameters["genomeId"] == [CLUB_GENOME_ID]
    assert callback == "https://connect.ubisoft.com/login?galaxyCallback=1"
    assert len(matching_patterns) == 1

    scripts = "\n".join(AUTH_JS[matching_patterns[0]])
    assert "PRODloginData" in scripts
    assert "PRODrememberMe" in scripts
    assert "PRODlastProfile" in scripts


@pytest.mark.parametrize("callback_prefix", [
    "https://connect.ubisoft.com/change_domain/",
    "https://connect.ubisoft.com/login?galaxyCallback=1,",
])
def test_auth_storage_parser_accepts_callback_routes(callback_prefix):
    storage_values = [
        {"userId": "user-1", "ticket": "ticket-1", "sessionId": "session-1"},
        {"rememberMeTicket": "remember-me-1"},
    ]
    encoded_values = quote(",".join(json.dumps(value) for value in storage_values))

    assert _parse_auth_storage_jsons(callback_prefix + encoded_values) == storage_values
