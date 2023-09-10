import pytest

from clyjin.core.boot import Boot


@pytest.mark.asyncio
async def test_start():
    try:
        await Boot().start(["-h"])
    except SystemExit:
        pass
    else:
        raise AssertionError
