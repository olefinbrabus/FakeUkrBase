import re
from datetime import datetime
from config import base_random
from string import ascii_letters

from config import fake, UKRAINIAN_OPERATORS
from transliterate import translit


def generate_full_name():
    return f"{fake.first_name()} {fake.last_name()}"


def generate_birthdate():
    end_time = datetime.strptime("2005-12-31", "%Y-%m-%d")
    rand_data = fake.date(end_datetime=end_time)
    return datetime.strptime(rand_data, "%Y-%m-%d")


def generate_email(person) -> str:
    letters_university = _get_random_university()
    domains: tuple = (
        "gmail.com",
        "ukr.net",
        "icloud.com",
        f"{letters_university}.edu.ua",
    )
    coefficients: tuple = (0.6, 0.2, 0.1, 0.1)

    chosen_domain = base_random.choices(domains, weights=coefficients)[0]

    name_to_email = _get_email_name(person)

    return f"{name_to_email}@{chosen_domain}"


def _get_random_university() -> str:
    return "".join(base_random.choices(ascii_letters, k=3)).lower() + "u"


def _get_email_name(person) -> str:
    email_name: str = translit(person.full_name.lower(), "uk", reversed=True)
    email_name = email_name.replace("'", "")
    email_name = email_name.replace("ʼ", "")

    interval = base_random.choice(("", "_", ".", "-"))

    if random_replaced_names_in_email():
        temp = email_name.split(" ")
        temp[0], temp[1] = temp[1], temp[0]
        email_name = " ".join(temp)

    email_name = email_name.replace(" ", interval)

    chance_to_postfix_number = base_random.randint(1, 100) > 80

    if chance_to_postfix_number:
        if fake.boolean():
            year = str(person.birthdate.year)[2:]
            email_name += year

        else:
            email_name += str(base_random.randint(0, 99))

    return email_name


def random_replaced_names_in_email() -> bool:
    return fake.boolean(65)


def generate_phone_number():
    phone_number: str = fake.phone_number()
    while not re.match(r"\+380\s\([0-9]+\)\s[0-9]+-[0-9]+-[0-9]+", phone_number):
        phone_number = fake.phone_number()
    phone_number = phone_number[:6] + _get_random_operator() + phone_number[8:]
    return phone_number


def _get_random_operator():
    chosen_operator = base_random.choice(list(UKRAINIAN_OPERATORS.values()))
    return str(base_random.choice(chosen_operator))


def generate_address():
    return fake.address()
