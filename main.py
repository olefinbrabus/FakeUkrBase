import os
from typing import Any

import click
import pandas as pd

# from .argv_parser import execute_symbols
from config import fake, base_random, SESSION_PERSON_FILE_DIR, SESSION_SALARY_FILE_DIR

# from user import AbstractPerson, Employee
from core import AbstractPerson, AbstractEmployee
from core.persons_generatorOld import generate_person_data
from dataframes.dataframe_person import PersonDataFrameManager
from display.display import display_df
from exceptions import ConflictDataTakenException
from mappers.salary_mappers import salaries_to_dataframe
from services.db.save import save_frames_to_db
from services.etl.postgres_to_clickhouse import run_etl
from services.generator.generator import generate_persons
from validations.validator import validate_persons


# import ctypes
# from files_manager import read_file, save_file


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

    persons, salary_list = generate_persons(count, person_class)
    validate_persons(persons, person_class)

    person_dataframe_manager = PersonDataFrameManager(persons, person_class)

    person_dataframe_manager.dataframe.to_parquet(
        SESSION_PERSON_FILE_DIR,
        engine="fastparquet",
        compression="snappy",
        object_encoding="utf8",
    )

    if salary_list is not None:
        salary_frame = salaries_to_dataframe(
            all_persons_salaries_list=salary_list, employees=persons
        )

        salary_frame.to_parquet(
            SESSION_SALARY_FILE_DIR,
            engine="fastparquet",
            compression="snappy",
            object_encoding="utf8",
        )
        click.secho(f"Generated {len(persons)} people", fg="green")


@click.command("read")
@click.option("--read", type=str, help="Read array of persons")
def cli_read_persons(read):
    pass


@click.command("display")
@click.option("--count", "-c", default=10, type=int, help="Display of amount of people")
@click.option("--salary", "-s", is_flag=True, help="Display salary of persons")
def cli_display_person(count: int, salary) -> None:
    if count < 1:
        raise ValueError("Display must be greater than 0")
    if not os.path.exists(SESSION_PERSON_FILE_DIR):
        raise click.ClickException("No session found. Run 'generate' first.")
    person_df = pd.read_parquet(SESSION_PERSON_FILE_DIR)
    salary_df = pd.read_parquet(SESSION_SALARY_FILE_DIR)

    display_df(person_df, salary_df)


@click.command("save")
# @click.option(
#     # "--test",
#     # default=DEFAULT_SAVE_DIR,
#     # type=ClickPath(exists=False, path_type=Path),
#     # help="Save path",
# )
def cli_save_file():
    from services.db.session import Base, engine
    from services.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    person_df = pd.read_parquet(SESSION_PERSON_FILE_DIR)
    salary_df = pd.read_parquet(SESSION_SALARY_FILE_DIR)

    save_frames_to_db(person_df, salary_df)
    click.echo("Data saved to Postgres database.")


@click.command("olap")
@click.option("--full", "-f", is_flag=True, help="Clear previous data")
def cli_olap(full: bool) -> None:
    run_etl(full_reload=full)
    click.secho("OLAP Load Completed", fg="green")


# cli.add_command(cli_set_seed)
# cli.add_command(cli_set_person)
cli.add_command(cli_generate_person)
cli.add_command(cli_read_persons)
cli.add_command(cli_display_person)
cli.add_command(cli_save_file)
cli.add_command(cli_olap)

if __name__ == "__main__":
    cli()
