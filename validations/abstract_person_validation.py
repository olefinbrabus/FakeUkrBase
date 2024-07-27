import re
from datetime import datetime


def full_name_validator(name: str) -> bool:
    return bool(re.match(r"^[а-яА-ЯЇїІіЄєҐґʼ\s]+$", name))


def birthdate_validator(birth_date: datetime) -> bool:
    return 1900 <= birth_date.year <= 2005


def phone_validator(phone_number: str) -> bool:
    return bool(re.match(r"\+380\s\([0-9]+\)\s[0-9]+-[0-9]+-[0-9]+", phone_number))
