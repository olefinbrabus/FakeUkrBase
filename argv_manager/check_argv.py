from typing import Any

from config import fake, base_random
from dataframes.dataframe_person import PersonDataFrame
from files_manager.save_manager import save_file
from user.abstract_person import AbstractPerson


def check_argv(argv: list[str]):
    argv: list[str] = argv[1:]
    frame = None
    seed = None

    if "--seed" in argv:
        seed = execute_symbols(argv, "seed", 1, False)

    set_seed(seed)

    if "--generate" in argv or len(argv) == 0:
        frame = frame_by_generate_word_in_argv(argv)

    if "--show" in argv or len(argv) == 0:
        frame.display()

    if "--save" in argv:
        complete_path: str = execute_symbols(argv, "--save", "default", False)
        save_file(frame, complete_path)


def execute_symbols(
    argv: list[str], key: str, default: Any = 10, to_int: bool = True
) -> Any:
    if key in argv:
        index = argv.index(key)

        if index + 1 < len(argv):
            symbols = argv[index + 1]
            to_int = argv[index + 1].isdigit() and to_int

            return int(symbols) if to_int else symbols
    return default


def frame_by_generate_word_in_argv(argv: list[str]) -> PersonDataFrame:
    persons_count = execute_symbols(argv, "generate", 10)
    persons = [AbstractPerson(i + 1) for i in range(persons_count)]

    frame = PersonDataFrame(persons)
    return frame


def set_seed(seed: Any) -> None:
    fake.seed_instance(seed)
    base_random.seed(seed)
