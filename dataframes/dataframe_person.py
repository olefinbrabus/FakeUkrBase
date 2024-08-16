from typing import Any

import pandas as pd
from pandas import Timestamp
from tabulate import tabulate
from IPython.display import display

from user import AbstractPerson
from config import UKRAINIAN_OPERATORS


class PersonDataFrameManager:
    def __init__(self, dataframe: pd.DataFrame | list[AbstractPerson], person: AbstractPerson.__class__):
        self.person = person
        self.dataframe = dataframe

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value) -> None:
        if isinstance(value, pd.DataFrame):
            valid_persons = self.to_persons(value, self.person)
            self._dataframe = self.to_dataframe(valid_persons)
        elif isinstance(value, list):
            self._dataframe = self.to_dataframe(value)
        else:
            raise TypeError(f"{value} is not a dataframe or list of persons")

    def get_phone_operators_count(self) -> dict[str, int]:
        frame = self.dataframe["phone number"]
        phone_operators_count = {keys: 0 for keys in UKRAINIAN_OPERATORS.keys()}
        for number in frame:
            operator = AbstractPerson.phone_operator(number)
            phone_operators_count[operator] += 1
        return phone_operators_count

    def display(self) -> None:
        display(tabulate(self._dataframe, headers=self.dataframe.keys()))

    @staticmethod
    def to_dataframe(persons: list[AbstractPerson]) -> pd.DataFrame:
        columns = [x[1:].replace("_", " ") for x in persons[0].__dict__.keys()]
        df = pd.DataFrame(columns=columns)
        for i, person in enumerate(persons):
            df.loc[i] = list(person.__dict__.values())
        return df

    @staticmethod
    def to_persons(frame: pd.DataFrame, person_class) -> list[AbstractPerson]:
        list_persons: list[dict[str:Any]] = frame.to_dict(orient="records")

        valid_list_persons = []
        for person in list_persons:
            valid_person_dict: dict[str, Any] = {}

            for key, value in person.items():
                key = key.replace(" ", "_")

                if isinstance(value, Timestamp):
                    value = value.to_pydatetime()
                valid_person_dict[key] = value
            valid_list_persons.append(valid_person_dict)

        return [person_class(**person) for person in valid_list_persons]

    def __str__(self):
        return tabulate(self._dataframe, headers=self.dataframe.keys())

    def __len__(self):
        return len(self.dataframe)
