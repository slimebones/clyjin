from .core import cli


def handle_err(err: Exception) -> None:
    if (isinstance(err, Exception)):
        print(
            "[clyjin.#runtime / ERROR] {}: {}"
                .format(err.__class__.__name__, " ".join(err.args))
        )
    else:
        print(
            "[clyjin.#runtime / ERROR] Passed to final handler error is not"
            " an Exception"
        )
    exit(1)

if __name__ == "__main__":
    # Catch all unhandled or passed errs
    try:
        out = cli.main()
    except Exception as err:
        handle_err(err)
