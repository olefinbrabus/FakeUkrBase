import pytest
from pydantic import ValidationError

from core import AbstractPerson
from validations.validator import validate_abstract_person


def test_valid_from_dict(valid_person_dict: dict):
    person: AbstractPerson
    try:
        person = AbstractPerson(**valid_person_dict)
        assert True
    except ValidationError as e:
        pytest.fail(e.message)


def test_invalid_from_dict(invalid_person_dict: dict):
    person: AbstractPerson
    try:
        person = AbstractPerson(**invalid_person_dict)
        assert True
    except ValidationError as e:
        pytest.fail(e.message)


def test_valid_in_validator(valid_person_dict: dict):
    person: AbstractPerson
    try:
        person = AbstractPerson(**valid_person_dict)
        assert validate_abstract_person(person) == True
    except ValidationError as e:
        pytest.fail(e.message)


def test_invalid_in_validator(invalid_person_dict: dict):
    person: AbstractPerson
    try:
        person = AbstractPerson(**invalid_person_dict)
        assert validate_abstract_person(person) == False
    except ValidationError as e:
        pytest.fail(e.message)
