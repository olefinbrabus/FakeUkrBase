from PIL.DdsImagePlugin import item1
from pandas import DataFrame

from core import AbstractPerson, AbstractEmployee


def validate_person_dataset(dataset: DataFrame, person_class: AbstractPerson = AbstractPerson):
    copied_dataset = dataset.copy(deep=True)
    attributes_to_check_is_repeat: list[str] = []

    if isinstance(person_class, AbstractPerson):
        attributes_to_check_is_repeat = [
            "email_address", "phone_number", "id", "credit_card"
        ]
    elif isinstance(person_class, AbstractEmployee):
        attributes_to_check_is_repeat += [
            "working_email_address", "work_phone_number", "working_credit_card"
        ]
    else:
        raise TypeError("person_class must be an instance of AbstractPerson")

    for attribute in attributes_to_check_is_repeat:
        index_duplicate_items = validate_repeatable_items_in_dataset_by_column(copied_dataset, attribute)







def validate_repeatable_items_in_dataset_by_column(dataset: DataFrame, column: str):
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





# df = DataFrame({
#     "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1, 1, 15],
# })
#
# print(validate_repeatable_items_in_dataset_by_column(df, "numbers"))