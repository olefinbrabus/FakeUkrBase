from pydantic import EmailStr
from email_validator import validate_email

from core import AbstractPerson, AbstractEmployee
from services.generator.person_generator import (
    generate_sex,
    generate_full_name,
    generate_birthdate,
    generate_address,
)
from services.generator.email_generator import generate_email, generate_employee_email
from services.generator.credit_card_generator import generate_credit_data
from services.generator.phone_generator import generate_phone_number
from services.utils import transliterate_word


class GeneratorPersonService:
    def __init__(self, person_cls: type[AbstractPerson] = AbstractPerson):
        self.person_cls = person_cls

    def make_person(self, id: int):
        sex = generate_sex()
        full_name: dict[str, str] = generate_full_name(gender=sex)

        birthdate = generate_birthdate()
        person_full_name = f"{full_name['first_name']} {full_name['last_name']}"

        email_address = generate_email(
            person_full_name=person_full_name, person_birthdate=birthdate
        )
        credit_card = generate_credit_data(person_full_name)
        phone_number = generate_phone_number()

        return self.person_cls(
            id=id,
            sex=sex,
            first_name=full_name["first_name"],
            first_name_eng_lang=transliterate_word(full_name["first_name"]),
            middle_name=full_name["middle_name"],
            middle_name_eng_lang=transliterate_word(full_name["middle_name"]),
            second_name=full_name["last_name"],
            second_name_eng_lang=transliterate_word(full_name["last_name"]),
            email_address=email_address,
            credit_card=credit_card,
            birthdate=birthdate,
            address=generate_address(),
            phone_number=phone_number,
        )


gen = GeneratorPersonService()
print(gen.make_person(0))
[print(gen.make_person(i)) for i in range(100)]
