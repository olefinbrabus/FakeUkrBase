import logging
from pandas import DataFrame

from core import AbstractPerson, AbstractEmployee

logger = logging.getLogger(__name__)


def validate_person_categories(
    dataset: DataFrame, person_cls: type[AbstractPerson] = AbstractPerson
):
    copied_dataset = dataset.copy(deep=True)
    attributes_to_check_is_have_duplicate: list[str] = []
    duplicate_list_by_categories: list[dict] = []

    if isinstance(person_cls, type(AbstractPerson)):
        attributes_to_check_is_have_duplicate = [
            "email_address",
            "phone_number",
            "id",
            "credit_card",
        ]
    if isinstance(person_cls, type(AbstractEmployee)):
        attributes_to_check_is_have_duplicate += [
            "working_email address",
            "work_phone_number",
            "working_credit_card",
        ]
    else:
        raise TypeError("person_cls must be an instance of AbstractPerson")

    for attribute in attributes_to_check_is_have_duplicate:
        index_duplicate_items = validate_duplicate_items_in_dataset_by_column(
            copied_dataset, attribute
        )
        if len(index_duplicate_items) > 1:
            duplicate_list_by_categories.append(index_duplicate_items)

    return duplicate_list_by_categories


def validate_duplicate_items_in_dataset_by_column(dataset: DataFrame, column: str):
    df = dataset.copy()
    df[column] = df[column].astype(str)

    duplicates = df.groupby(column).filter(lambda x: len(x) > 1).groupby(column).indices

    return {
        "_specific_word": column,
        "duplicates": {k: v for k, v in duplicates.items()},
    }
