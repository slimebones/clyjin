from loguru import logger
from .core import cli

@logger.catch
def call_cli():
    cli.main()


if __name__ == "__main__":
    call_cli()
