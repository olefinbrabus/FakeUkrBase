from typing import Any

import pandas as pd
from pandas import Timestamp
from tabulate import tabulate

from core import AbstractPerson
from mappers import dataframe_to_persons, persons_to_dataframe


class PersonDataFrameManager:
    def __init__(
        self,
        dataframe: list[AbstractPerson],
        person: type[AbstractPerson],
    ):
        self.person = person
        self.dataframe = dataframe

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value) -> None:
        if isinstance(value, pd.DataFrame):
            valid_persons = dataframe_to_persons(value, self.person)
            self._dataframe = persons_to_dataframe(valid_persons)
        elif isinstance(value, list):
            self._dataframe = persons_to_dataframe(value)
        else:
            raise TypeError(f"{value} is not a dataframe or list of persons")

    def __str__(self):
        return tabulate(self._dataframe, headers=self.dataframe.keys())

    # def __len__(self):
    #     return len(self.dataframe)
