from datetime import datetime

from generate_data.generator import (
    generate_full_name,
    generate_birthdate,
    generate_email,
    generate_phone_number,
    generate_address,
)
from validations.abstract_person_validation import (
    full_name_validator,
    birthdate_validator,
    phone_validator,
    email_validator,
)
from config import UKRAINIAN_OPERATORS


class AbstractPerson:

    def __init__(
        self,
        id: int,
        full_name: str = None,
        birthdate: datetime = None,
        email: str = None,
        phone_number: str = None,
        address: str = None,
    ):
        self.id = id
        self.full_name = full_name
        self.birthdate: datetime = birthdate
        self.email = email
        self.phone_number = phone_number
        self.address = address

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def full_name(self):
        return self._full_name

    @property
    def first_name(self):
        return self._full_name.split(" ")[0]

    @property
    def second_name(self):
        return self._full_name.split(" ")[1]

    @full_name.setter
    def full_name(self, value: str):
        if value is None:
            self._full_name = generate_full_name()
        elif full_name_validator(value):
            value = value.replace("ʼ", "")
            self._full_name = value

        else:
            raise ValueError(f"'{value}' is not a valid full name")

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, value):
        if value is None:
            self._birthdate = generate_birthdate()
        elif type(value) is datetime and birthdate_validator(value):
            self._birthdate = value
        elif type(value) is str:
            try:
                self._birthdate = datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise f"'{value}' is not a valid birthdate, it should be YYYY-MM-DD"

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is None:
            value = generate_email(self)
        if email_validator(value):
            self._email = value
        else:
            raise ValueError(f"'{value}' is not a valid email")

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        if value is None:
            self._phone_number = generate_phone_number()
        elif type(value) is str and phone_validator(value):
            self._phone_number = value
        else:
            raise ValueError(f"'{value}' is not a valid phone number")

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if value is None:
            self._address = generate_address()
        elif type(value) is str:
            self._address = value
        else:
            raise ValueError(f"'{value}' is not a valid address")

    @staticmethod
    def phone_operator(number: str):
        operator_number = int(number[6:8])

        for operator_name, numbers in UKRAINIAN_OPERATORS.items():
            for number in numbers:
                if number == operator_number:
                    return operator_name
        return "Undefined"

    def __str__(self):
        birthdate = self.birthdate.strftime("%Y-%m-%d")
        return (
            f"Повне імʼя: {self.full_name}, День народження:{birthdate},"
            f" Пошта: {self.email}, Телефон: {self._phone_number}, Адресса: {self._address}"
        )
