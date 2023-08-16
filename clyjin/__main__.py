import asyncio
from pathlib import Path

from clyjin.core.boot import Boot
from clyjin.utils.log import Log


@Log.catch
async def main() -> None:
    await Boot(
        rootdir=Path.cwd(),
    ).start()


if __name__ == "__main__":
    asyncio.run(main())
