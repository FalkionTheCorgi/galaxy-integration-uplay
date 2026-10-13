from unittest.mock import AsyncMock

import pytest
from galaxy.api.errors import AccessDenied

from backend import BackendClient


@pytest.mark.asyncio
async def test_club_titles_forbidden_does_not_refresh_authentication():
    client = BackendClient.__new__(BackendClient)
    client._do_request = AsyncMock(side_effect=AccessDenied())
    client._do_request_safe = AsyncMock(side_effect=AssertionError("should not refresh auth"))

    with pytest.raises(AccessDenied):
        await client.get_club_titles()

    client._do_request.assert_awaited_once()
    client._do_request_safe.assert_not_awaited()
