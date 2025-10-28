from pandas import DataFrame
from tabulate import tabulate

from core import AbstractPerson


def display_df(
        dataframe: DataFrame,
        person_cls: type[AbstractPerson] = AbstractPerson,


) -> None:

    print(tabulate(dataframe, headers=dataframe.keys()))
