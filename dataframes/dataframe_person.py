import pandas as pd
from tabulate import tabulate
from IPython.display import display

from user.abstract_person import AbstractPerson
from config import UKRAINIAN_OPERATORS


class PersonDataFrame:
    def __init__(self, dataframe: pd.DataFrame | list[AbstractPerson]):
        self.dataframe = dataframe

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value) -> None:
        if isinstance(value, pd.DataFrame):
            self._dataframe = value
        elif isinstance(value, list):
            self._dataframe = self.create_dataframe(value)
        else:
            raise TypeError(f"{value} is not a dataframe or list of persons")

    @staticmethod
    def create_dataframe(persons: list[AbstractPerson]) -> pd.DataFrame:
        columns = [x[1:].replace("_", " ") for x in persons[0].__dict__.keys()]
        df = pd.DataFrame(columns=columns)
        for i, person in enumerate(persons):
            df.loc[i] = list(person.__dict__.values())
        return df

    def get_phone_operators_count(self) -> dict[str, int]:
        frame = self.dataframe["phone number"]
        phone_operators_count = {keys: 0 for keys in UKRAINIAN_OPERATORS.keys()}
        for number in frame:
            operator = AbstractPerson.phone_operator(number)
            phone_operators_count[operator] += 1
        return phone_operators_count

    def display(self) -> None:
        display(tabulate(self._dataframe, headers=self.dataframe.keys()))

    def __str__(self):
        return tabulate(self._dataframe, headers=self.dataframe.keys())

    def __len__(self):
        return len(self.dataframe)
