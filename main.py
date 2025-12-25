import os
from typing import Any

import click
import pandas as pd

from config import SESSION_PERSON_FILE_DIR, SESSION_SALARY_FILE_DIR, cli_set_seed
from core import AbstractPerson, AbstractEmployee
from dataframes.dataframe_person import PersonDataFrameManager
from display.display import display_df
from mappers.salary_mappers import salaries_to_dataframe
from services.db.save import save_frames_to_db
from services.etl.postgres_to_clickhouse import run_etl
from services.generator import generate_persons
from services.statistics.analytics_methods import run_statistics
from validations import validate_persons


@click.group()
def cli():
    pass


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
def cli_read_persons_to_parquet(read):
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
    click.secho("Display Completed", fg="green")


@click.command("save")
def cli_save_file():
    from services.db.session import Base, engine

    Base.metadata.create_all(bind=engine)

    person_df = pd.read_parquet(SESSION_PERSON_FILE_DIR)
    salary_df = pd.read_parquet(SESSION_SALARY_FILE_DIR)

    save_frames_to_db(person_df, salary_df)
    click.secho("Data saved to Postgres database.", fg="green")


@click.command("olap")
@click.option("--full", "-f", is_flag=True, help="Clear previous data")
def cli_olap(full: bool) -> None:
    run_etl(full_reload=full)
    click.secho("OLAP Load Completed", fg="green")


@click.command("statistics")
@click.option(
    "--method",
    "-m",
    type=click.Choice(
        [
            "descriptive",
            "correlation",
            "regression",
            "timeseries",
            "clustering",
            "anomaly",
            "all",
        ],
        case_sensitive=False,
    ),
    default="all",
    show_default=True,
    help="Which type of statistics to show",
)
@click.option(
    "--no-plots",
    is_flag=True,
    default=False,
    help="Show only analytics log",
)
def cli_statistics(method: str, no_plots: bool) -> None:
    results, report_text = run_statistics(
        method=method.lower(),
        show_plots_flag=not no_plots,
    )

    click.secho("Analytics log:", fg="green")
    click.echo(report_text)


cli.add_command(cli_generate_person)
cli.add_command(cli_read_persons_to_parquet)
cli.add_command(cli_display_person)
cli.add_command(cli_save_file)
cli.add_command(cli_olap)
cli.add_command(cli_statistics)

if __name__ == "__main__":
    cli()
