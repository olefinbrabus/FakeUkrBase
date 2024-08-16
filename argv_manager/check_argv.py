from typing import Any

from .argv_parser import execute_symbols
from config import fake, base_random
from dataframes.dataframe_person import PersonDataFrameManager
from files_manager import read_file, save_file
from user import AbstractPerson, Employee
from exceptions import ConflictDataTakenException
from generate_data.persons_generator import generate_person_data


def check_argv(argv: list[str]):
    argv: list[str] = argv[1:]
    frame = None
    seed = None
    person: AbstractPerson.__class__ = AbstractPerson

    if "--person" in argv:
        person_number = execute_symbols(argv, "--person", 0, True)
        person = set_person(person_number)

    if "--generate" in argv and "--read" in argv:
        raise ConflictDataTakenException("--read", "--generate")

    if "--seed" in argv:
        seed = execute_symbols(argv, "--seed", 1, False)

    set_seed(seed)

    if "--generate" in argv or len(argv) == 0:
        persons_count = execute_symbols(argv, "--generate", 10)
        frame = frame_by_generate_word_in_argv(persons_count, person)

    if "--read" in argv:
        complete_path = execute_symbols(argv, "--read")
        frame = PersonDataFrameManager(read_file(complete_path),person)


    if "--display" in argv or len(argv) == 0:
        frame.display()

    if "--save" in argv:
        if frame is None:
            raise Exception("Frame has undefined")
        complete_path: str = execute_symbols(argv, "--save", "default", False)
        save_file(frame, complete_path)


def frame_by_generate_word_in_argv(persons_count: int, person_class) -> PersonDataFrameManager:
    persons = generate_person_data(person_class, persons_count)

    frame = PersonDataFrameManager(persons, person_class)
    return frame


def set_seed(seed: Any) -> None:
    fake.seed_instance(seed)
    base_random.seed(seed)


def set_person(person_number):
    persons = [AbstractPerson, Employee]
    if 0 < person_number > len(persons):
        raise ValueError("Person number out of range")
    return persons[person_number]
