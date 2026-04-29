import pandas as pd
import datetime

import pytest

from config import set_seed, base_random, fake
from core import AbstractPerson, AbstractEmployee, SalaryPayment, Job
from mappers import persons_to_dataframe
from mappers.salary_mappers import salaries_to_dataframe

from services import generate_persons, generate_year_salaries_per_each_employee
from tests.utils_pytest import df_sha256


@pytest.fixture(scope="session")
def seed():
    set_seed("a")


def test_abstract_person_generation_same_seeding():
    set_seed("a")
    persons_a = generate_persons(count=100, person_cls=AbstractPerson)
    set_seed("a")
    persons_b = generate_persons(count=100, person_cls=AbstractPerson)

    set_seed("a")
    assert df_sha256(persons_to_dataframe(persons_a)) == df_sha256(
        persons_to_dataframe(persons_b)
    )


def test_employee_with_salary_generation_same_seeding():
    set_seed("a")
    persons_a = generate_persons(count=100, person_cls=AbstractEmployee)
    salary_a = generate_year_salaries_per_each_employee(persons_a)
    set_seed("a")
    persons_b = generate_persons(count=100, person_cls=AbstractEmployee)
    salary_b = generate_year_salaries_per_each_employee(persons_a)

    set_seed("a")
    assert df_sha256(persons_to_dataframe(persons_a)) == df_sha256(
        persons_to_dataframe(persons_b)
    )
    assert df_sha256(salaries_to_dataframe(persons_a, salary_a)) == df_sha256(
        salaries_to_dataframe(persons_b, salary_b)
    )


def test_invariants_salary_non_negative_and_links(seed: int) -> None:
    persons = generate_persons(100, AbstractEmployee)
    salaries = generate_year_salaries_per_each_employee(persons)

    persons_df = persons_to_dataframe(persons)
    salary_df = salaries_to_dataframe(persons, salaries)

    person_ids = set(persons_df["id"].astype(int).tolist())
    salary_person_ids = set(salary_df["person_id"].astype(int).tolist())

    assert salary_person_ids.issubset(person_ids)

    for col in ["gross_amount", "bonus_amount", "penalty_amount"]:
        values = pd.to_numeric(salary_df[col], errors="raise")
        assert (values >= 0).all()

    delay_days = pd.to_numeric(salary_df["delay_days"], errors="raise")
    is_delayed = salary_df["is_delayed"].astype(bool)

    assert (delay_days >= 0).all()
    assert (delay_days[~is_delayed] == 0).all()


def test_uniqueness_person_keys(seed: int) -> None:
    persons = generate_persons(100, AbstractEmployee)
    df = persons_to_dataframe(persons)

    assert not df["id"].duplicated().any()
    assert not df["email_address"].duplicated().any()
    assert not df["phone_number"].astype(str).duplicated().any()


def test_uniqueness_salary_employee_month(seed: int) -> None:
    persons = generate_persons(100, AbstractEmployee)
    salaries = generate_year_salaries_per_each_employee(persons)
    df = salaries_to_dataframe(persons, salaries)

    key_dupes = df.duplicated(subset=["person_id", "month"])
    assert not key_dupes.any()
