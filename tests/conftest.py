import datetime
from decimal import Decimal

import pandas as pd
import pytest
from mimesis import Gender
from phonenumbers import PhoneNumber
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import CreditCard, AbstractPerson
from core.enums import TypeCreditCard, ExtendedPaymentCardBrand, QualificationType
from core.models import Job, AbstractEmployee, SalaryPayment
from mappers import persons_to_dataframe
from mappers.salary_mappers import salaries_to_dataframe
from services.db.session import Base


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
        "address": "Вишгород",
        "address_eng_lang": "Vyshgorod",
        "type_populated_area": "City",
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
def invalid_person_dict_for_validator() -> dict:
    return {
        "id": -1,
        "sex": Gender.MALE,
        "first_name": "Сер1231237гій",
        "first_name_eng_lang": "Serh1123ij",
        "middle_name": "Свя1232тославович",
        "middle_name_eng_lang": "Svjatoslavovych",
        "second_name": "Пелех231235",
        "second_name_eng_lang": "Pelekhdsad1235",
        "email_address": "Pelekh.Serhij6666666663475435743785356478@gmail.com",
        "address": "площа Костанді, буд. 182, Вишгород, 85979",
        "address_eng_lang": "Vyshgorod",
        "type_populated_area": "City",
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

@pytest.fixture
def valid_employee_dict(valid_person_dict) -> dict:
    return valid_person_dict | {
        "job": Job(
            name="Програміст",
            qualification=QualificationType.junior,
            address="Вишгород"
        ),
        "length_of_work": 2,
        "contract_payment": Decimal("27000.00")


    }

@pytest.fixture
def valid_salary() -> dict:
    return {
        "person_id": 1,
        "job_name": "Програміст",
        "job_qualification": "Junior",
        "job_address": "Вишгород",
        "month": "2025-01-01",
        "gross_amount": Decimal("26766.00"),
        "bonus_amount": Decimal("500.00"),
        "penalty_amount": Decimal("0.00"),
        "is_delayed": False,
        "delay_days": 0,
        "pay_date": "2025-01-31",
    }


@pytest.fixture
def invalid_person_dict_for_pydantic() -> dict:
    return {
        "id": "adad",
        "sex": "no",
        "first_name": 22,
        "first_name_eng_lang": ("Serh1123ij", "4414"),
        "middle_name": {},
        "middle_name_eng_lang": [1, 2, 3],
        "second_name": True,
        "second_name_eng_lang": False,
        "email_address": 5 / 2,
        "address": 100_000_000,
        "address_eng_lang": 5**2,
        "type_populated_area": 43,
        "birthdate": 29328.13,
        "phone_number": 380945670584012312,
        "credit_card": True,
    }


@pytest.fixture()
def engine():
    eng = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)

@pytest.fixture()
def session_factory(engine):
    test_session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    def _factory():
        return test_session()
    yield _factory

@pytest.fixture()
def valid_abstract_person_frame(valid_person_dict):
    dataframe = persons_to_dataframe([AbstractPerson(**valid_person_dict),])
    yield dataframe

@pytest.fixture()
def valid_employee_frame(valid_employee_dict):
    dataframe = persons_to_dataframe([AbstractEmployee(**valid_employee_dict),])
    yield dataframe

@pytest.fixture
def valid_salary_frame(valid_employee_dict, valid_salary):
    payments = []
    for m in range(1, 13):
        month = f"2025-{m:02d}-01"
        pay_date = pd.Timestamp(month) + pd.offsets.MonthEnd(0)
        p = SalaryPayment(**(valid_salary | {"month": month, "pay_date": str(pay_date.date())}))
        payments.append(p)

    df = salaries_to_dataframe(
        [AbstractEmployee(**valid_employee_dict)],
        [payments],
    )
    return df