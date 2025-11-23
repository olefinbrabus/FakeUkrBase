from pandas import DataFrame
from rich_dataframe import prettify

from core import AbstractPerson
from dataframes.shape_shift_dataframe import change_shape_person


def display_df(
    dataframe: DataFrame,
    person_cls: type[AbstractPerson] = AbstractPerson,
    columns_to_hide: dict = None,
) -> None:
    # if columns_to_hide:
    dataframe = change_shape_person(dataframe, person_cls, columns_to_hide or {})
    # print(tabulate(dataframe, headers=dataframe.keys()))
    prettify(dataframe, row_limit=50, col_limit=15)
