import copy
import logging

import pytest
from mimesis import Gender

from core import AbstractPerson
from validations.validator import validate_persons

logger = logging.getLogger(__name__)


def test_valid_from_dict(valid_person_dict: dict):
    person: AbstractPerson
    try:
        person = AbstractPerson(**valid_person_dict)
        assert True
    except Exception as e:
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
        except Exception as e:
            logger.log(logging.INFO, e)


def test_valid_in_validator(valid_person_dict: dict):
    person: AbstractPerson
    person = AbstractPerson(**valid_person_dict)
    validate_persons(
        [
            person,
        ]
    )


def test_invalid_in_validator(
    invalid_person_dict_for_validator: dict, valid_person_dict: dict
):
    person: AbstractPerson
    for k, v in invalid_person_dict_for_validator.items():
        logger.log(logging.INFO, v)
        if v == Gender.MALE or k == "id":
            continue
        logger.log(logging.INFO, f"{k}: {v}")
        print(f"{k}: {v}")

        copied_person = copy.deepcopy(valid_person_dict)
        copied_person[k] = v
        person = AbstractPerson(**copied_person)
        if validate_persons(
            [
                person,
            ]
        ):
            assert False
