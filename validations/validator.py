import datetime
from decimal import Decimal

from mimesis import Gender
from pandas import DataFrame
from phonenumbers.phonenumber import PhoneNumber
from progress.bar import ShadyBar

from core import AbstractPerson, CreditCard
from core.countries_data.enums import TypeCreditCard, ExtendedPaymentCardBrand
from mappers import dict_to_person, persons_to_dataframe
from validations import is_valid_ukrainian_word
from validations.abstract_person_validator import is_valid_birthdate
from validations.card_validator import is_valid_luna
from validations.person_dataset_validator import validate_person_categories


def validate_abstract_person(
    person_obj: AbstractPerson | dict[str, str],
    person_cls: type[AbstractPerson] = AbstractPerson,
) -> bool:
    if isinstance(person_obj, dict):
        person_obj = dict_to_person(person_obj, person_cls)

    if not is_valid_luna(person_obj.credit_card.number):
        return False

    if not is_valid_birthdate(person_obj.birthdate):
        return False

    if not is_valid_ukrainian_word(
        person_obj.first_name, person_obj.second_name, person_obj.middle_name
    ):
        return False

    return True


def validate_persons(
    person_obj: list[AbstractPerson] | dict[str, str],
    person_cls: type[AbstractPerson] = AbstractPerson,
):
    persons_len = len(person_obj)
    bar = ShadyBar(message=f"Validate {person_cls.__name__}'s...", max=persons_len)
    for person in person_obj:
        if not validate_abstract_person(person, person_cls):
            print(f"{person} is not a valid")
            raise Exception
        bar.next()
    bar.finish()


def validate_person_dataset(
    dataset: DataFrame,
    person_cls: type[AbstractPerson] = AbstractPerson
):
    duplicate_list_by_categories = validate_person_categories(
        dataset.copy(deep=True),
        person_cls,
    )

    print(duplicate_list_by_categories)

    if duplicate_list_by_categories:
        for category in duplicate_list_by_categories:
            print(category)
            # ids_repeatable_items = [id in ]
            print('')


# if __name__ == "main":
persons =  [AbstractPerson(
    **{
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
        )})
] * 10

fr = persons_to_dataframe(persons)
print(fr)

validate_person_dataset(fr)