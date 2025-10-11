from config import base_random
from string import ascii_letters

from config import fake

from services.utils import transliterate_word


def generate_email(
    person, exclude_education_email: bool = False, company_word: str = None
) -> str:
    letters_university = None
    if not exclude_education_email or not company_word:
        letters_university = _get_random_university()

    if company_word is None:
        domains: tuple = (
            "gmail.com",
            "ukr.net",
            "icloud.com",
            f"{letters_university}.edu.ua",
        )
        coefficients: tuple
        if exclude_education_email:
            domains = domains[:-1]
            coefficients = (0.6, 0.2, 0.2)
        else:
            coefficients = (0.6, 0.2, 0.1, 0.1)

        chosen_domain = base_random.choices(domains, weights=coefficients)[0]
    else:
        chosen_domain = company_word.lower() + ".com"

    name_to_email = _get_email_name(person)

    return f"{name_to_email}@{chosen_domain}"


def _get_random_university() -> str:
    return "".join(base_random.choices(ascii_letters, k=3)).lower() + "u"


def random_replaced_names_in_email() -> bool:
    return fake.boolean(65)


def _get_email_name(person) -> str:
    email_name: str = transliterate_word(person.full_name.lower())
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


def generate_employee_email(person) -> str:
    english_word_company = transliterate_word(fake.word())
    return generate_email(person, company_word=english_word_company)
