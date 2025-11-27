from pandas import DataFrame
from rich_dataframe import prettify

from core import AbstractPerson
from dataframes.shape_shift_dataframe import change_shape_person


def display_df(
    person_dataframe: DataFrame,
    salary_dataframe: DataFrame,
    person_cls: type[AbstractPerson] = AbstractPerson,
    columns_to_hide: dict = None,
) -> None:
    # if columns_to_hide:
    person_dataframe = change_shape_person(
        person_dataframe, person_cls, columns_to_hide or {}
    )
    # print(tabulate(dataframe, headers=dataframe.keys()))
    prettify(person_dataframe, row_limit=50, col_limit=15)
    prettify(salary_dataframe, row_limit=50, col_limit=15)
