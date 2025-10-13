from concurrent.futures import ProcessPoolExecutor, wait
from multiprocessing import cpu_count

from user import AbstractPersonOld


def async_generate_person_data(
    person_class, persons_count: int
) -> list[AbstractPersonOld]:
    person_list = []

    with ProcessPoolExecutor(max_workers=cpu_count() - 1) as executor:
        for i in range(persons_count):
            person_list.append(executor.submit(person_class, i))

    wait(person_list)

    person_list = [future.result() for future in person_list]
    return person_list


def generate_person_data(person_class, persons_count: int) -> list[AbstractPersonOld]:
    return [person_class(i + 1) for i in range(persons_count)]
