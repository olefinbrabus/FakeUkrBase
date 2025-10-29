from pandas import DataFrame

from core import AbstractPerson, AbstractEmployee


def change_shape_person(
        dataframe: DataFrame,
        person_cls: type[AbstractPerson],
        columns_to_hide: dict[str, bool]

):
    dataframe = dataframe.copy(deep=True)

    if person_cls == type[AbstractPerson]:
        dataframe = change_shape_abstract_person(dataframe, **columns_to_hide)

    if person_cls == type[AbstractEmployee]:
        pass

    return dataframe




def change_shape_abstract_person(
        dataframe: DataFrame,
        id: bool = False,
        names: bool = False,
        english_names: bool = False,
        address: bool = False,
        cards: bool = False,
        birthdate: bool = False,
        sex: bool = False,
        phone_number: bool = False,
):
    dict_to_exclude_fields = {
        "id": id,
        "names": names,
        "english_names": english_names,
        "address": address,
        "cards": cards,
        "birthdate": birthdate,
        "sex": sex,
        "phone_number": phone_number,
    }

    return dataframe.drop(columns=[
        k for k, v in dict_to_exclude_fields.items() if v
    ], axis=1)

