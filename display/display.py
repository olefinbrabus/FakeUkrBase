from pandas import DataFrame
from tabulate import tabulate


def display_df(dataframe: DataFrame) -> None:
    print(tabulate(dataframe, headers=dataframe.keys()))
