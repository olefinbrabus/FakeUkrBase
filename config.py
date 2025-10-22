import os
import random
import pathlib
import tempfile

from faker import Faker

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

SUPPORT_FORMATS = (".csv", ".xlsx", ".json", ".xml")

SESSION_FILE_DIR = os.path.join(tempfile.gettempdir(), "fakeukrbase_session.parquet")
