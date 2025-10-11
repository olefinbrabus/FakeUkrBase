from datetime import datetime

from config import fake


def generate_full_name():
    return f"{fake.first_name()} {fake.last_name()}"


def generate_birthdate():
    end_time = datetime.strptime("2005-12-31", "%Y-%m-%d")
    rand_data = fake.date(end_datetime=end_time)
    return datetime.strptime(rand_data, "%Y-%m-%d")


def generate_address():
    return fake.address()
