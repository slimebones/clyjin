from .core import cli


if __name__ == "__main__":
    # Catch all unhandled exceptions
    try:
        cli.main()
    except Exception as err:
        print("[clyjin.runtime] {}".format(err))
