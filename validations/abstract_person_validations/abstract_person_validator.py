import re
from datetime import date, datetime

from core import AbstractPerson
from mappers import dict_to_person
from validations.abstract_person_validations.card_validator import validate_card
import logging

logger = logging.getLogger(__name__)


def is_valid_ukrainian_name(*words) -> bool:
    for word in words:
        if not bool(re.match(r"^[-а-яА-ЯЇїІіЄєҐґʼ\s]+$", word)):
            return False
    return True


def is_valid_english_name(*words) -> bool:
    for word in words:
        if not bool(re.match(r"^[A-Za-z ,ʼ.'-]+$", word)):
            return False
    return True


def is_valid_birthdate(birth_date: date) -> bool:
    return (
        date(year=1900, month=1, day=1)
        <= birth_date
        <= date(
            year=datetime.now().year - 18,
            month=datetime.now().month,
            day=datetime.now().day - 1,
        )
    )


def validate_abstract_person(
    person_obj: AbstractPerson | dict[str, str],
    person_cls: type[AbstractPerson] = AbstractPerson,
) -> bool:
    if isinstance(person_obj, dict):
        person_obj = dict_to_person(person_obj, person_cls)

    if person_obj.id < 0:
        logger.error(f"Invalid id: {person_obj.id}")
        return False

    if not validate_card(
        person_obj.credit_card,
        person_obj.first_name_eng_lang,
        person_obj.second_name_eng_lang,
    ):
        logger.error(f"Invalid credit card number: {person_obj.credit_card.number}")
        return False

    if not is_valid_birthdate(person_obj.birthdate):
        logger.error(f"Invalid birthdate: {person_obj.birthdate}")
        return False

    if not is_valid_ukrainian_name(
        person_obj.first_name, person_obj.second_name, person_obj.middle_name
    ):
        logger.error("Invalid ukrainian name")
        return False

    if not is_valid_english_name(
        person_obj.first_name_eng_lang,
        person_obj.second_name_eng_lang,
        person_obj.middle_name_eng_lang,
    ):
        logger.error("Invalid english name")
        return False

    return True
