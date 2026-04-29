import os
import pathlib
import random
import tempfile
from typing import Any

from faker import Faker
import progress
# from mimesis import Person, Locale

base_random = random.Random()
fake = Faker("uk_UA")
# person = Person(locale=Locale("en"))


BASE_DIR = str(pathlib.Path(__file__).parent.absolute())
DEFAULT_SAVE_DIR = BASE_DIR + "/" + "files" + "/"


UKRAINIAN_OPERATORS: dict[str, tuple] = {
    "Kyivstar": (39, 67, 96, 97, 98),
    "Lifecell": (63, 73, 91, 92, 94),
    "Vodafone": (50, 66, 95, 99),
}

UKRAINE_DATA = (
    BASE_DIR
    + "/"
    + "core"
    + "/"
    + "countries_data"
    + "/"
    + "ukraine"
    + "/"
    + "ukr-populated-places.xlsx"
)

SUPPORT_FORMATS = (".csv", ".xlsx", ".json", ".xml")

SESSION_PERSON_FILE_DIR = os.path.join(
    tempfile.gettempdir(), "fakeukrbase_person_session.parquet"
)
SESSION_SALARY_FILE_DIR = os.path.join(
    tempfile.gettempdir(), "fakeukrbase_salary_session.parquet"
)


def set_seed(seed: Any) -> None:
    fake.seed_instance(seed)
    base_random.seed(seed)

#
# bar = progressbar.ProgressBar(widgets=[
#     ' [', progressbar.Timer(), '] ',
#     progressbar.Bar(),
#     ' (', progressbar.ETA(), ') ',
# ])