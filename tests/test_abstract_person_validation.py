import copy

import pytest
from mimesis import Gender
from pydantic import ValidationError

from core import AbstractPerson
from validations.validator import validate_abstract_person


def test_valid_from_dict(valid_person_dict: dict):
    person: AbstractPerson
    try:
        person = AbstractPerson(**valid_person_dict)
        assert True
    except ValidationError as e:
        pytest.fail(e)


def test_invalid_from_dict(
    invalid_person_dict_for_pydantic: dict, valid_person_dict: dict
):
    person: AbstractPerson

    for k, v in invalid_person_dict_for_pydantic.items():
        copied_person = copy.deepcopy(valid_person_dict)
        copied_person[k] = v
        try:
            person = AbstractPerson(**copied_person)
            assert False
        except ValidationError as e:
            print(e)


def test_valid_in_validator(valid_person_dict: dict):
    person: AbstractPerson
    try:
        person = AbstractPerson(**valid_person_dict)
        assert validate_abstract_person(person) == True
    except ValidationError as e:
        pytest.fail(e)


def test_invalid_in_validator(
    invalid_person_dict_for_validator: dict, valid_person_dict: dict
):
    person: AbstractPerson
    for k, v in invalid_person_dict_for_validator.items():
        print(v)
        if v == Gender.MALE:
            continue

        copied_person = copy.deepcopy(valid_person_dict)
        copied_person[k] = v
        person = AbstractPerson(**copied_person)
        if validate_abstract_person(person):
            assert False
