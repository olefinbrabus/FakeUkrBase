import re
from datetime import datetime


def full_name_validator(name: str) -> bool:
    return bool(re.match(r"^[а-яА-ЯЇїІіЄєҐґʼ\s]+$", name))


def birthdate_validator(birth_date: datetime) -> bool:
    return 1900 <= birth_date.year <= 2005


def email_validator(email: str) -> bool:
    email_regex = (
        r"^(?:[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+)@"
        r"(?:(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}|"
        r"\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\])$"
    )
    try:
        return bool(re.match(email_regex, email))
    except TypeError:
        return False


def phone_validator(phone_number: str) -> bool:
    return bool(re.match(r"\+380\s\([0-9]+\)\s[0-9]+-[0-9]+-[0-9]+", phone_number))
