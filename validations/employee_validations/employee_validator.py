from core import AbstractEmployee
from validations.job_validations.job_validator import validate_job


def validate_employee(employee: AbstractEmployee):
    if not validate_job(employee.job):
        print('Employee Job not valid')
        return False

    if employee.length_of_work > 55:
        print('Employee Length of Work is greater than 55 years')
        return False

    if employee.contract_payment<=0:
        print('Employee Contract Payment cant\'t be less than 0')
        return False

    return True