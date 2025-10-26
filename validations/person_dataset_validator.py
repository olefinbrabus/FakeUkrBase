from pandas import DataFrame

from core import AbstractPerson, AbstractEmployee


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
    elif isinstance(person_cls, type(AbstractEmployee)):
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
    print(column)
    print(dataset)
    item_list = dataset[column].values.tolist()
    print(item_list)

    duplicates: dict = {"_specific_word": column}
    for i, item in enumerate(item_list):
        if item_list.count(item) > 1:
            if item not in duplicates:
                duplicates[item] = [i]
            else:
                duplicates[item].append(i)

    return duplicates


if __name__ == "__main__":
    df = DataFrame({"numbers": [1, 1, 15], "greeb": ["asass", "sadasd", "asass"]})

    print(validate_duplicate_items_in_dataset_by_column(df, "numbers"))
    print(validate_duplicate_items_in_dataset_by_column(df, "greeb"))
