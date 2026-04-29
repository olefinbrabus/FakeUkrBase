from core import AbstractEmployee
from validations.job_validations.job_validator import validate_job

import logging

logger = logging.getLogger(__name__)


def validate_employee(employee: AbstractEmployee):
    if not validate_job(employee.job):
        logger.error("Employee Job not valid")
        return False

    if employee.length_of_work > 55:
        logger.error("Employee Length of Work is greater than 55 years")
        return False

    if employee.contract_payment <= 0:
        logger.error("Employee Contract Payment can't be less than 0")
        return False

    return True
