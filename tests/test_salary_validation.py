import copy
import logging
import pytest
from mimesis import Person

from core import SalaryPayment, AbstractEmployee
from validations import validate_salaries


logger = logging.getLogger(__name__)


def test_valid_salary_from_dict(valid_salary: dict):
    try:
        salary = SalaryPayment(**valid_salary)
        assert True
    except Exception as e:
        pytest.fail(e)


def test_invalid_salary_from_dict(
    invalid_salary_for_pydantic: dict, valid_salary: dict
):

    for k, v in invalid_salary_for_pydantic.items():
        copied_salary = copy.deepcopy(valid_salary)
        logger.log(logging.INFO, copied_salary.items())
        copied_salary[k] = v
        try:
            salary = SalaryPayment(**copied_salary)
            assert False
        except ValueError as e:
            logger.log(logging.INFO, e)


def test_valid_salary_in_validator(valid_salary: dict, valid_employee_dict: dict):
    salary = SalaryPayment(**valid_salary)
    validate_salaries(
        [
            [salary] * 12,
        ],
        [AbstractEmployee(**valid_employee_dict)],
    )


def test_invalid_salary_in_validator(
    invalid_salary_for_validator: dict, valid_salary: dict, valid_employee_dict: dict
):
    for k, v in invalid_salary_for_validator.items():
        copied_salary = copy.deepcopy(valid_salary)
        copied_salary[k] = v
        logger.log(logging.INFO, v)
        try:
            salary = SalaryPayment(**copied_salary)
            validate_salaries(
                [
                    [salary] * 12,
                ],
                [AbstractEmployee(**valid_employee_dict)],
            )
            assert False
        except ValueError as e:
            logger.log(logging.INFO, e)
