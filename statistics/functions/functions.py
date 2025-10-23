from pandas import DataFrame

from config import UKRAINIAN_OPERATORS
from core import AbstractPerson


def get_phone_operators_count(dataframe: DataFrame) -> dict[str, int]:
    frame = dataframe["phone number"]
    phone_operators_count = {keys: 0 for keys in UKRAINIAN_OPERATORS.keys()}
    for number in frame:
        operator = AbstractPerson.phone_operator(number)
        phone_operators_count[operator] += 1
    return phone_operators_count


