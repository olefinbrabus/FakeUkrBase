import datetime

from core.models import SalaryPayment
import logging

logger = logging.getLogger(__name__)


def validate_salary(salary: SalaryPayment):
    if salary.month > datetime.date.today().replace(year=datetime.date.today().year + 2):
        logger.log(
            logging.ERROR, f"salary date {salary.month} is greater than current range per year"
        )
        return False

    if salary.pay_date > datetime.date.today().replace(year=datetime.date.today().year + 2):
        logger.log(
            logging.ERROR, f"salary pay date {salary.pay_date} is greater than current range per year"
        )
        return False

    if salary.gross_amount < 0:
        logger.log(logging.ERROR, f"salary gross {salary.month} is less than zero")
        return False

    if salary.bonus_amount < 0:
        logger.log(
            logging.ERROR, f"salary bonus {salary.bonus_amount} is less than zero"
        )
        return False

    if salary.penalty_amount < 0:
        logger.log(
            logging.ERROR,
            f"salary penalty amount {salary.penalty_amount} is less than zero",
        )
        return False

    if salary.is_delayed != bool(salary.delay_days):
        logger.log(
            logging.ERROR,
            f"salary is delayed: {salary.is_delayed}, but delayed days is {salary.delay_days}",
        )
        return False

    return True
