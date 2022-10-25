from loguru import logger
from .core import cli


def handle_err(err: Exception) -> None:
    # We are guaranteed that logger exceptions are handled at CLI, so here we
    # can use logger freely since we know that it is initialized (or program
    # could exit later)
    if (isinstance(err, Exception)):
        logger.bind(err=err).error("")
    else:
        print(
            "[#clyjin.runtime / ERROR] Passed to final handler error is not"
            " an Exception"
        )
    exit(1)

if __name__ == "__main__":
    # Catch all unhandled or passed errs
    try:
        out = cli.main()
    except Exception as err:
        handle_err(err)
