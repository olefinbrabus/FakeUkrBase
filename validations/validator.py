from pandas import DataFrame
from progress.bar import ShadyBar
from pydantic import ValidationError

from core import AbstractPerson
from mappers import dict_to_person
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
        print(f"Invalid credit card number: {person_obj.credit_card.number}")
        return False

    if not is_valid_birthdate(person_obj.birthdate):
        print(f"Invalid birthdate: {person_obj.birthdate}")
        return False

    if not is_valid_ukrainian_word(
        person_obj.first_name, person_obj.second_name, person_obj.middle_name
    ):
        print("Invalid ukrainian name")
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
    dataset: DataFrame, person_cls: type[AbstractPerson] = AbstractPerson
):
    duplicate_list_by_categories = validate_person_categories(
        dataset.copy(deep=True),
        person_cls,
    )

    if duplicate_list_by_categories:
        for category in duplicate_list_by_categories:
            print(category)
            print(f"in {category["_specific_word"]}")

        raise ValidationError("")
