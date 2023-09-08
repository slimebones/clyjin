import pytest

from clyjin.core.boot import Boot


@pytest.mark.asyncio
async def test_start():
    await Boot().start(["-h"])
    assert 0
