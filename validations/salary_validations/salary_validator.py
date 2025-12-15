import datetime

from core.models import SalaryPayment


def validate_salary(salary: SalaryPayment):
    if salary.month > datetime.date.today():
        print(f"salary date {salary.month} is greater than current date")
        return False

    if salary.gross_amount <= 0:
        print(f"salary gross {salary.month} is less than zero")
        return False

    if salary.bonus_amount <= 0:
        print(f"salary bonus {salary.month} is less than zero")
        return False

    if salary.penalty_amount <= 0:
        print(f"salary penalty amount {salary.month} is less than zero")
        return False

    if salary.is_delayed ^ salary.delay_days:
        print(
            f"salary is delayed: {salary.is_delayed}, but delayed days is {salary.delay_days}"
        )
        return False

    return True
