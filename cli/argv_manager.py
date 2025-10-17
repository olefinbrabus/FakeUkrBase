from typing import Any

import click
from click import Path as ClickPath
from pathlib import Path

# from .argv_parser import execute_symbols
from config import fake, base_random, DEFAULT_SAVE_DIR, type_person
from dataframes.dataframe_person import PersonDataFrameManager
from files_manager import read_file, save_file

# from user import AbstractPerson, Employee
from core import AbstractPerson, AbstractEmployee
from exceptions import ConflictDataTakenException
from core.persons_generatorOld import generate_person_data

# @click.group()
# def the_most_important_commands():
#     pass


def check_argv(argv: list[str]):
    argv: list[str] = argv[1:]
    frame = None
    seed = None
    person: AbstractPerson.__class__ = AbstractPerson

    if "--person" in argv:
        pass
        # person_number = execute_symbols(argv, "--person", 0, True)
        # person = set_person(person_number)

    if "--generate" in argv and "--read" in argv:
        raise ConflictDataTakenException("--read", "--generate")

    if "--seed" in argv:
        pass
        # seed = execute_symbols(argv, "--seed", 1, False)

    set_seed(seed)

    if "--generate" in argv or len(argv) == 0:
        pass
        # persons_count = execute_symbols(argv, "--generate", 10)
        # frame = frame_by_generate_word_in_argv(persons_count, person)

    if "--read" in argv:
        pass
        # complete_path = execute_symbols(argv, "--read", None)
        # frame = PersonDataFrameManager(read_file(complete_path), person)

    if "--display" in argv or len(argv) == 0:
        frame.display()

    if "--save" in argv:
        if frame is None:
            raise Exception("Frame has undefined")
        # complete_path: str = execute_symbols(argv, "--save", "default", False)
        # save_file(frame, complete_path)


def frame_by_generate_word_in_argv(
    persons_count: int, person_class
) -> PersonDataFrameManager:
    persons = generate_person_data(person_class, persons_count)

    frame = PersonDataFrameManager(persons, person_class)
    return frame


@click.command()
@click.option("--seed", default=None, help="Change random seed")
def set_seed(seed: Any) -> None:
    fake.seed_instance(seed)
    base_random.seed(seed)


@click.command()
@click.option(
    "--person", default="abstractperson", help="Change person with different fields"
)
@click.pass_context
def set_person(ctx, person: str) -> None:
    persons_classes = [AbstractPerson, AbstractEmployee]
    persons_name_str: dict = {
        person.__name__.lower(): person for person in persons_classes
    }

    ctx.obj["person"] = persons_name_str[person]


@click.command()
@click.option("--generate", default=10, type=int, help="Generate of amount of people")
def generate_person(generate):
    pass


@click.command()
@click.option("read", type=str, help="Read array of persons")
def read_persons(read):
    pass


@click.command()
@click.option("--display", default=10, type=int, help="Display of amount of people")
def display_person(display):
    if display < 1:
        raise ValueError("Display must be greater than 0")


@click.command()
@click.option(
    "--save",
    default=DEFAULT_SAVE_DIR,
    type=ClickPath(exists=False, path_type=Path),
    help="Save path",
)
def save_file(save: Path):
    pass
