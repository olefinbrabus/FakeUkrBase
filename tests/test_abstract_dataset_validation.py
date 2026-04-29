import pytest
import logging

from core import AbstractPerson
from dataframes.dataframe_person import PersonDataFrameManager
from validations.validator import validate_person_dataset

logger = logging.getLogger(__name__)


def test_duplicated_fields_in_persons_validation(valid_person_dict: dict):
    duplicated_persons = [AbstractPerson(**valid_person_dict)] * 10

    pdfm = PersonDataFrameManager(duplicated_persons, AbstractPerson)

    with pytest.raises(Exception) as e:
        validate_person_dataset(pdfm.dataframe, AbstractPerson)
    logger.log(logging.ERROR, e)
    assert True
