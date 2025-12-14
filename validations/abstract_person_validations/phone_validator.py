import re


def is_valid_phone_number(phone_number: str) -> bool:
    return bool(re.match(r"\+380\s\([0-9]+\)\s[0-9]+-[0-9]+-[0-9]+", phone_number))
