from typing import Any


def execute_symbols(
    argv: list[str], key: str, default: Any, to_int: bool = True
) -> Any:
    if key in argv:
        index = argv.index(key)

        if index + 1 < len(argv):
            symbols = argv[index + 1]
            to_int = argv[index + 1].isdigit() and to_int

            if to_int:
                if symbols.isdigit():
                    return int(symbols)
                raise ValueError("Value must be an integer")
            return symbols

    if default is None:
        raise ValueError("Path not found")
    return default
