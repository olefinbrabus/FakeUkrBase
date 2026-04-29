import logging

from core import SalaryPayment, AbstractEmployee

logger = logging.getLogger(__name__)


def validate_salary_person_relation(
    salaries: list[SalaryPayment], persons: AbstractEmployee
) -> None:
    for i, salary in enumerate(salaries):
        if not salary.person_id == persons.id:
            logger.error(
                f"this salary with person_id {salary.person_id} "
                f"doesn't have relation with this employee id {persons.id}"
            )
            raise ValueError
