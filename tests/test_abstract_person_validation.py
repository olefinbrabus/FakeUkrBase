import datetime
from decimal import Decimal

import pytest
from mimesis import Gender
from phonenumbers import PhoneNumber
from pydantic import ValidationError

from core import AbstractPerson, CreditCard
from core.countries_data.enums import TypeCreditCard, ExtendedPaymentCardBrand
from validations.validator import validate_abstract_person


@pytest.fixture
def valid_person_dict() -> dict:
    return {
        "id": 1,
        "sex": Gender.MALE,
        "first_name": "Сергій",
        "first_name_eng_lang": "Serhij",
        "middle_name": "Святославович",
        "middle_name_eng_lang": "Svjatoslavovych",
        "second_name": "Пелех",
        "second_name_eng_lang": "Pelekh",
        "email_address": "Pelekh.Serhij66@gmail.com",
        "address": "площа Костанді, буд. 182, Вишгород, 85979",
        "birthdate": datetime.date(1982, 12, 10),
        "phone_number": PhoneNumber(country_code=380945670584),
        "credit_card": CreditCard(
            **{
                "person_full_name": "Serhij Pelekh",
                "number": "9040124327573011",
                "type": TypeCreditCard.credit,
                "date_expired": datetime.date(2025, 10, 20),
                "brand": ExtendedPaymentCardBrand.prostir,
                "cvv": "283",
                "currency": "USD",
                "amount": Decimal("3231.25"),
            }
        ),
    }


@pytest.fixture
def invalid_person_dict() -> dict:
    return {
        "id": 1,
        "sex": Gender.FEMALE,
        "first_name": "Сер1231237гій",
        "first_name_eng_lang": "Serh1123ij",
        "middle_name": "Свя1232тославович",
        "middle_name_eng_lang": "Svjatoslavovych",
        "second_name": "Пелех231235",
        "second_name_eng_lang": "Pelekhdsad1235",
        "email_address": "Pelekh.Serhij6666666663475435743785356478@gmail.com",
        "address": "площа Костанді, буд. 182, Вишгород, 85979",
        "birthdate": datetime.date(1876, 12, 10),
        "phone_number": PhoneNumber(country_code=380945670584012312),
        "credit_card": CreditCard(
            **{
                "person_full_name": "Olexa Bulbash",
                "number": "9040124327573011",
                "type": TypeCreditCard.credit,
                "date_expired": datetime.date(1888, 10, 20),
                "brand": ExtendedPaymentCardBrand.prostir,
                "cvv": "283",
                "currency": "USD",
                "amount": Decimal("-1.25"),
            }
        ),
    }


def test_valid_from_dict(valid_person_dict: dict):
    person: AbstractPerson
    try:
        person = AbstractPerson(**valid_person_dict)
        assert True
    except ValidationError as e:
        pytest.fail(e.message)


def test_invalid_from_dict(invalid_person_dict: dict):
    person: AbstractPerson
    try:
        person = AbstractPerson(**invalid_person_dict)
        assert True
    except ValidationError as e:
        pytest.fail(e.message)


def test_valid_in_validator(valid_person_dict: dict):
    person: AbstractPerson
    try:
        person = AbstractPerson(**valid_person_dict)
        assert validate_abstract_person(person) == True
    except ValidationError as e:
        pytest.fail(e.message)


def test_invalid_in_validator(invalid_person_dict: dict):
    person: AbstractPerson
    try:
        person = AbstractPerson(**invalid_person_dict)
        assert validate_abstract_person(person) == False
    except ValidationError as e:
        pytest.fail(e.message)
