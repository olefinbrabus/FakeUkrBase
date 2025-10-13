from datetime import datetime

from config import fake, base_random
from mimesis import Person, Gender



def generate_sex():
    return Gender.FEMALE if base_random.random() < 0.5 else Gender.MALE

def generate_full_name(gender: Gender):
    if gender == Gender.MALE:
        return {
            "first_name": fake.first_name_male(),
            "last_name": fake.last_name_male(),
            "middle_name": fake.middle_name_male(),
        }
    return {
        "first_name": fake.first_name_female(),
        "last_name": fake.last_name_female(),
        "middle_name": fake.middle_name_female(),
    }


def generate_birthdate():
    end_time = datetime.strptime("2005-12-31", "%Y-%m-%d")
    rand_data = fake.date(end_datetime=end_time)
    return datetime.strptime(rand_data, "%Y-%m-%d")


def generate_address():
    return fake.address()
