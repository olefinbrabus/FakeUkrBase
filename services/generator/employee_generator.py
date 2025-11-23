from datetime import date

from config import base_random


def generate_length_of_work(birth_date: date) -> int:
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    max_possible_length_of_work = max(0, age - 18)
    allowed_max = min(max_possible_length_of_work, 10)

    if allowed_max <= 0:
        return 1

    return base_random.randint(1, allowed_max)