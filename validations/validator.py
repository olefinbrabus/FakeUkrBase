from pandas import DataFrame
from progress.bar import ShadyBar
from pydantic import ValidationError

from core import AbstractPerson, AbstractEmployee
from validations.abstract_person_validations.abstract_person_validator import (
    validate_abstract_person,
)
from validations.dataset_validations.person_dataset_validator import (
    validate_person_categories,
)
from validations.employee_validations.employee_validator import validate_employee


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
        if isinstance(person, AbstractEmployee) and not validate_employee(person):
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
