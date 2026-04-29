from pandas import DataFrame
from progress.bar import ShadyBar
import logging

from core import AbstractPerson, AbstractEmployee, SalaryPayment
from validations.abstract_person_validations.abstract_person_validator import (
    validate_abstract_person,
)
from validations.dataset_validations.person_dataset_validator import (
    validate_person_categories,
)
from validations.employee_validations.employee_validator import validate_employee
from validations.salary_validations.salary_person_validator import (
    validate_salary_person_relation,
)
from validations.salary_validations.salary_validator import validate_salary

logger = logging.getLogger(__name__)


def validate_persons(
    person_obj: list[AbstractPerson] | dict[str, str],
    person_cls: type[AbstractPerson] = AbstractPerson,
) -> None:
    persons_len = len(person_obj)
    bar = ShadyBar(
        message=f"Validate {person_cls.__name__}'s...",
        max=persons_len,
        suffix='%(percent)d%% | elapsed: %(elapsed)ds | eta: %(eta)ds'
        )
    for person in person_obj:
        if not validate_abstract_person(person, person_cls):
            logger.error(f"{person} is not a valid")
            raise ValueError
        if isinstance(person, AbstractEmployee) and not validate_employee(person):
            logger.error(f"{person} is not a valid")
            raise ValueError
        bar.next()
    bar.finish()


def validate_salaries(
    salaries: list[list[SalaryPayment]], persons: list[AbstractEmployee]
) -> None:
    bar = ShadyBar(
        message=f"Validate salaries...",
        max=len(salaries),
        suffix='%(percent)d%% | elapsed: %(elapsed)ds | eta: %(eta)ds'
    )
    for salaries_per_year, employee in zip(salaries, persons):
        validate_salary_person_relation(salaries_per_year, employee)
        if len(salaries_per_year) != 12:
            logger.error(
                f"length of salaries_per_year is {len(salaries_per_year)},"
                f" {"less" if len(salaries_per_year) < 12 else "greater"} than month in year"
            )
            raise ValueError
        for salary in salaries_per_year:
            if not validate_salary(salary):
                logger.error(f"salary with fields\n{salary}\nis not a valid")
                raise ValueError
        bar.next()
    bar.finish()


def validate_person_dataset(
    dataset: DataFrame, person_cls: type[AbstractPerson] = AbstractPerson
) -> None:
    duplicate_list_by_categories = validate_person_categories(
        dataset.copy(deep=True),
        person_cls,
    )

    if duplicate_list_by_categories:
        for category in duplicate_list_by_categories:
            logger.log(logging.ERROR, category)
            logger.log(logging.ERROR, f"in {category["_specific_word"]}")

        raise Exception
