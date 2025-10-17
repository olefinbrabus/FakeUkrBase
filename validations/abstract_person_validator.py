import re
from datetime import date, datetime


def is_valid_ukrainian_word(*words) -> bool:
    for word in words:
        if not bool(re.match(r"^[а-яА-ЯЇїІіЄєҐґʼ\s]+$", word)):
            return False
    return True


def is_valid_birthdate(birth_date: date) -> bool:
    return (
        date(year=1900, month=1, day=1)
        <= birth_date
        <= date(
            year=datetime.now().year - 18,
            month=datetime.now().month,
            day=datetime.now().day - 1,
        )
    )
