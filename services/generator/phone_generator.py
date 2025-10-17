import re

from phonenumbers.phonenumber import PhoneNumber

from config import fake, UKRAINIAN_OPERATORS, base_random
from validations.abstract_person_validation import phone_validator


def generate_phone_number():
    phone_number: str = fake.phone_number()
    while not phone_validator(phone_number):
        phone_number = fake.phone_number()
    phone_number = phone_number[:6] + _get_random_operator() + phone_number[8:]
    phone_number = re.sub("[^0-9]", "", phone_number)
    return PhoneNumber(int(phone_number))


def _get_random_operator():
    chosen_operator = base_random.choice(list(UKRAINIAN_OPERATORS.values()))
    return str(base_random.choice(chosen_operator))
