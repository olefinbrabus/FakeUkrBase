import pytest

from config import set_seed, base_random, fake
from core import (
AbstractPerson,
AbstractEmployee,
SalaryPayment,
Job
)
from mappers import persons_to_dataframe

from services import generate_persons
from tests.utils_pytest import df_sha256


@pytest.fixture(scope="session")
def seed():
    set_seed("a")


def test_abstract_person_generation_seeding():
    set_seed("a")
    persons_a = generate_persons(count=10000, person_cls=AbstractPerson)
    set_seed("a")
    persons_b = generate_persons(count=10000, person_cls=AbstractPerson)

    set_seed("a")
    assert df_sha256(persons_to_dataframe(persons_a)) == df_sha256(persons_to_dataframe(persons_b))



