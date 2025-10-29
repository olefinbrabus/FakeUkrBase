import os
from typing import Any

# import ctypes

import click
import pandas as pd
from click import Path as ClickPath
from pathlib import Path

# from .argv_parser import execute_symbols
from config import fake, base_random, DEFAULT_SAVE_DIR, SESSION_FILE_DIR
from dataframes.dataframe_person import PersonDataFrameManager

# from files_manager import read_file, save_file

# from user import AbstractPerson, Employee
from core import AbstractPerson, AbstractEmployee
from display.display import display_df
from exceptions import ConflictDataTakenException
from core.persons_generatorOld import generate_person_data
from services.generator.generator import generate_persons
from validations.validator import validate_persons


@click.group()
def cli():
    pass


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

    cli_set_seed(seed)

    if "--generate" in argv or len(argv) == 0:
        pass
        # persons_count = execute_symbols(argv, "--generate", 10)
        # frame = frame_by_generate_word_in_argv(persons_count, person)

    if "--read" in argv:
        pass
        # complete_path = execute_symbols(argv, "--read", None)
        # frame = PersonDataFrameManager(read_file(complete_path), person)

    if "--display" in argv or len(argv) == 0:
        pass
        # frame.display()

    if "--save" in argv:
        if frame is None:
            raise Exception("Frame has undefined")
        # complete_path: str = execute_symbols(argv, "--save", "default", False)
        # save_file(frame, complete_path)


def frame_by_generate_word_in_argv(
    persons_count: int, person_cls
) -> PersonDataFrameManager:
    persons = generate_person_data(person_cls, persons_count)

    frame = PersonDataFrameManager(persons, person_cls)
    return frame


def cli_set_seed(seed: Any) -> None:
    fake.seed_instance(seed)
    base_random.seed(seed)


def cli_set_person(person: str) -> type[AbstractPerson]:
    persons_classes = [AbstractPerson, AbstractEmployee]
    persons_name_str: dict = {
        person.__name__.lower(): person for person in persons_classes
    }

    return persons_name_str[person]


@click.command("generate")
@click.option(
    "--count", "-c", default=10, type=int, help="Generate of amount of people"
)
@click.option(
    "--person",
    "-p",
    default="abstractperson",
    help="Change person with different fields",
)
@click.option("--seed", "-s", default=None, help="Change random seed")
def cli_generate_person(count: int, person: str, seed: Any) -> None:

    person_class = cli_set_person(person)

    cli_set_seed(seed)

    persons: list[AbstractPerson] = generate_persons(count, person_class)
    validate_persons(persons, person_class)

    pdfm = PersonDataFrameManager(persons, person_class)

    pdfm.dataframe.to_parquet(
        SESSION_FILE_DIR,
        engine="fastparquet",
        compression="snappy",
        object_encoding="utf8"
    )
    click.secho(f"Generated {len(persons)} people", fg="green")



@click.command("read")
@click.option("--read", type=str, help="Read array of persons")
def cli_read_persons(read):
    pass


@click.command("display")
@click.option("--count", "-c", default=10, type=int, help="Display of amount of people")
def cli_display_person(count: int) -> None:
    if count < 1:
        raise ValueError("Display must be greater than 0")
    if not os.path.exists(SESSION_FILE_DIR):
        raise click.ClickException("No session found. Run 'generate' first.")
    df = pd.read_parquet(SESSION_FILE_DIR)


    display_df(df, )


@click.command()
@click.option(
    "--save",
    default=DEFAULT_SAVE_DIR,
    type=ClickPath(exists=False, path_type=Path),
    help="Save path",
)
def cli_save_file(save: Path):
    pass


# cli.add_command(cli_set_seed)
# cli.add_command(cli_set_person)
cli.add_command(cli_generate_person)
cli.add_command(cli_read_persons)
cli.add_command(cli_display_person)
cli.add_command(cli_save_file)

if __name__ == "__main__":
    cli()
