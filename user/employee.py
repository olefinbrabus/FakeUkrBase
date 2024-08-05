from datetime import datetime

from generate_data.generator import generate_credit_data, generate_employee_email
from .abstract_person import AbstractPerson
from validations.abstract_person_validation import email_validator


class Employee(AbstractPerson):
    def __init__(
            self,
            id: int,
            full_name: str = None,
            birthdate: datetime = None,
            email: str = None,
            phone_number: str = None,
            address: str = None,
            credit_data: str = None,
            work_email: str = None,

    ):
        super().__init__(id, full_name, birthdate, email, phone_number, address)
        self.credit_data = credit_data
        self.work_email = work_email

    @property
    def credit_data(self):
        return self._credit_data

    @credit_data.setter
    def credit_data(self, value):
        if value is None:
            self._credit_data = generate_credit_data(self)
        if value:
            self._credit_data = value

    @property
    def work_email(self):
        return self._work_email

    @work_email.setter
    def work_email(self, value):
        if value is None:
            self._work_email = generate_employee_email(self)
        if email_validator(value):
            self._work_email = value






