from pandas import DataFrame

from core import AbstractPerson, AbstractEmployee


def change_shape_person(
    dataframe: DataFrame,
    person_cls: type[AbstractPerson],
    columns_to_hide: dict[str, bool],
):
    dataframe = dataframe.copy(deep=True)
    dataframe = change_shape_abstract_person(dataframe, **columns_to_hide)
    if "job_name" in dataframe.keys():
        dataframe = change_shape_abstract_employee(dataframe, **columns_to_hide)

    return dataframe


def change_shape_abstract_person(
    dataframe: DataFrame,
    id: bool = True,
    names: bool = False,
    english_names: bool = True,
    address: bool = True,
    cards: bool = True,
    birthdate: bool = True,
    sex: bool = False,
    phone_number: bool = True,
):
    dict_to_exclude_fields = {
        "id": id,
        "first_name": names,
        "middle_name": names,
        "second_name": names,
        "first_name_eng_lang": english_names,
        "middle_name_eng_lang": english_names,
        "second_name_eng_lang": english_names,
        "address": address,
        "credit_card": cards,
        "birthdate": birthdate,
        "sex": sex,
        "phone_number": phone_number,
    }

    return dataframe.drop(
        columns=[k for k, v in dict_to_exclude_fields.items() if v], axis=1
    )


def change_shape_abstract_employee(
    dataframe: DataFrame,
    working_email_address: bool = True,
    working_phone_number: bool = True,
):
    dict_to_exclude_fields = {
        "working_email_address": working_email_address,
        "working_phone_number": working_phone_number,
    }

    return dataframe.drop(
        columns=[k for k, v in dict_to_exclude_fields.items() if v], axis=1
    )
