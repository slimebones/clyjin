import typing

class UnconvertableStringException(Exception):
    def __init__(self, string: str, *args: object) -> None:
        message = "Unconvertable string {}".format(string)
        super().__init__(message, *args)

def convert_string_to_bool(string: str) -> bool:
    """Convert given string to bool according to logical rules.
    
    Possible values of input string:
        - "true"
        - "false"
        - "0"
        - "1"

    Args:
        string:
            String to be converted

    Return:
        Converted boolean

    Raise:
        UnconvertableStringException
    """
    if string in ["true", "1"]:
        return True
    elif string in ["false", "0"]:
        return False
    else:
        raise UnconvertableStringException(string)