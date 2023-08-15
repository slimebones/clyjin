import asyncio
from clyjin.core.boot import Boot
from clyjin.utils.log import Log


@Log.catch(reraise=True)
async def main() -> None:
    await Boot().start()


if __name__ == "__main__":
    asyncio.run(main())
