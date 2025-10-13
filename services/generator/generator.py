from pydantic import EmailStr

from core import AbstractPerson, AbstractEmployee

from .person_generator import generate_sex, generate_full_name, generate_birthdate, generate_address
from .email_generator import generate_email, generate_employee_email
from .credit_card_generator import generate_credit_data
from ..utils import transliterate_word


class GeneratorPersonService:
    def __init__(self, person: AbstractPerson = AbstractPerson):
        self.person = person

    def make_person(self, id: int):
        person = self.person
        person.id = id
        person.gender = generate_sex()
        full_name: dict[str, str] = generate_full_name(gender=person.gender)
        person.first_name = full_name['first_name']
        person.first_name_county_lang = transliterate_word(person.first_name)
        person.middle_name = full_name['middle_name']
        person.middle_name_county_lang = transliterate_word(person.middle_name)
        person.last_name = full_name['last_name']
        person.last_name_county_lang = transliterate_word(person.last_name)
        person.birthdate = generate_birthdate()
        person.email_address = generate_email(person_full_name=f"{person.first_name} {person.last_name}")

        return person

