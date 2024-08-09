from concurrent.futures import ProcessPoolExecutor, wait
from multiprocessing import cpu_count

from user import AbstractPerson


def generate_data(person_class, persons_count: int, data: list[dict] = None) -> list[AbstractPerson]:
    person_list = []

    with ProcessPoolExecutor(max_workers=cpu_count() - 1) as executor:
        for i in range(persons_count):
            if data is not None:
                person_list.append(executor.submit(person_class, i, **data[i]))
            else:
                person_list.append(executor.submit(person_class, i))

    wait(person_list)

    person_list = [future.result() for future in person_list]
    return person_list
