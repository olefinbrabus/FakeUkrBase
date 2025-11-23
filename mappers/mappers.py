from typing import Any

from mimesis import Gender
from pandas import Timestamp, DataFrame

from core import AbstractPerson, AbstractEmployee


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
    # columns = [x.replace("_", " ") for x in persons[0].__dict__.keys()]
    # columns = [x for x in persons[0].__dict__.keys()]
    # df = DataFrame(columns=columns)
    # if type(persons[0]) is AbstractEmployee:
    #     df = df.assign(job_name=[], job_qualification=[], job_address=[])

    rows: list = []


    for i, person in enumerate(persons):
        person_dict = person.model_dump()
        person_dict["credit_card"] = person.credit_card.number
        person_dict["phone_number"] = int(person.phone_number.country_code)
        person_dict["sex"] = "Чоловік" if person.sex == Gender.MALE else "Жінка"
        person_dict["birthdate"] = person.birthdate.strftime("%Y-%m-%d")

        if type(person) is AbstractEmployee:
            person_dict["contract_payment"] = float(person.contract_payment)

            job = person_dict.pop("job")
            person_dict["job_name"] = job["name"]
            person_dict["job_qualification"] = job["qualification"]
            person_dict["job_address"] = job["address"]
        # df.loc[i] = list(person_dict.values())

        rows.append(person_dict)

    return DataFrame(rows)

# def abstract_persons_to_hashable(persons: list[AbstractPerson]) -> dict:


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
): ...
