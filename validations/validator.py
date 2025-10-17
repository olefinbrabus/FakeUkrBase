from core import AbstractPerson
from validations import is_valid_ukrainian_word
from validations.abstract_person_validator import is_valid_birthdate
from validations.card_validator import is_valid_luna


def to_person_model(
    person_dict: dict[str, str], person_cls: type[AbstractPerson]
) -> AbstractPerson:
    if isinstance(person_dict, dict):
        try:
            return person_cls(**person_dict)
        except ValueError as e:
            print(e)
            raise e
    raise TypeError(f"this dict is not an {person_dict.__class__.__name__}")


def validate_abstract_person(
    person_obj: AbstractPerson | dict[str, str], person_cls: type[AbstractPerson]
) -> bool:
    if isinstance(person_obj, dict):
        person_obj = to_person_model(person_obj, person_cls)

    if not is_valid_luna(person_obj.credit_card.number):
        return False

    if not is_valid_birthdate(person_obj.birthdate):
        return False

    if not is_valid_ukrainian_word(person_obj.first_name, person_obj.last_name, person_obj.middle_name):
        return False

    return True
