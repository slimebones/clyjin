import asyncio
from pathlib import Path

from clyjin.core.boot import Boot
from clyjin.utils.log import Log


@Log.catch
def main() -> None:
    asyncio.run(Boot(
        rootdir=Path.cwd(),
    ).start())


if __name__ == "__main__":
    main()
