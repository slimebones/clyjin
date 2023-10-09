import asyncio

from clyjin.core.boot import Boot
from clyjin.log import Log


@Log.catch
def main() -> None:
    asyncio.run(Boot().start())


if __name__ == "__main__":
    main()
