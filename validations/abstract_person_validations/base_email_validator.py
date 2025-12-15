import re


def is_valid_email(email: str) -> bool:
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
