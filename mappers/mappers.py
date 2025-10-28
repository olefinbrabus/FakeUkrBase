from typing import Any

from pandas import Timestamp, DataFrame

from core import AbstractPerson


def dict_to_person(
    person_dict: dict[str, str], person_cls: type[AbstractPerson]
) -> AbstractPerson:
    if isinstance(person_dict, dict):
        try:
            return person_cls(**person_dict)
        except ValueError as e:
            print(e)
            raise e
    raise TypeError(f"this dict is not an {person_dict.__class__.__name__}")


def persons_to_dataframe(persons: list[AbstractPerson]) -> DataFrame:
    # columns = [x[1:].replace("_", " ") for x in persons[0].__dict__.keys()]
    columns = [x.replace("_", " ") for x in persons[0].__dict__.keys()]
    columns = [x for x in persons[0].__dict__.keys()]
    df = DataFrame(columns=columns)
    for i, person in enumerate(persons):
        df.loc[i] = list(person.__dict__.values())
    return df


def dataframe_to_persons(frame: DataFrame, person_class) -> list[AbstractPerson]:
    list_persons: list[dict] = frame.to_dict(orient="records")

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

def persons_to_employees(
    persons: list[AbstractPerson],
    show_id: bool = True,
):
    ...
