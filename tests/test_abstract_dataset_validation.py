import pytest
from pydantic import ValidationError

from core import AbstractPerson
from dataframes.dataframe_person import PersonDataFrameManager
from validations.validator import validate_person_dataset


def test_duplicated_fields_in_persons_validation(valid_person_dict: dict):
    duplicated_persons = [
        AbstractPerson(**valid_person_dict)
    ] * 10

    pdfm = PersonDataFrameManager(duplicated_persons, AbstractPerson)

    try:
        if not validate_person_dataset(pdfm.dataframe, AbstractPerson):
            assert True
    except ValidationError as e:
        pass
    assert False






