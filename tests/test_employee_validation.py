import copy

import logging
import pytest
from mimesis import Gender

from core import AbstractEmployee
from validations.validator import validate_persons

logger = logging.getLogger(__name__)


def test_valid_employee_from_dict(valid_employee_dict: dict):
    person: AbstractEmployee
    try:
        person = AbstractEmployee(**valid_employee_dict)
        assert True
    except Exception as e:
        pytest.fail(e)


def test_invalid_employee_from_dict(
    invalid_employee_dict_for_pydantic: dict, valid_employee_dict: dict
):
    person: AbstractEmployee

    for k, v in invalid_employee_dict_for_pydantic.items():
        copied_person = copy.deepcopy(valid_employee_dict)
        copied_person[k] = v
        try:
            person = AbstractEmployee(**copied_person)
            assert False
        except Exception as e:
            logger.log(logging.INFO, e)


def test_valid_employee_in_validator(valid_employee_dict: dict):
    person: AbstractEmployee
    person = AbstractEmployee(**valid_employee_dict)
    validate_persons(
        [
            person,
        ],
        AbstractEmployee,
    )


def test_invalid_employee_in_validator(
    invalid_employee_dict_for_validator: dict, valid_employee_dict: dict
):
    person: AbstractEmployee
    for k, v in invalid_employee_dict_for_validator.items():
        try:
            logger.log(logging.INFO, v)
            if v == Gender.MALE or k == "id":
                continue
            print(f"{k}: {v}")

            copied_person = copy.deepcopy(valid_employee_dict)
            copied_person[k] = v
            person = AbstractEmployee(**copied_person)
            validate_persons([person,], AbstractEmployee,)
            assert False
        except Exception as e:
            logger.log(logging.INFO, e)
