from progress.bar import ShadyBar

from core import AbstractPerson, AbstractEmployee
from core.models import SalaryPayment
from services.generator.adress_generator import create_address
from services.generator.contract_salary_generator import calculate_contract_payment
from services.generator.credit_card_generator import generate_credit_data
from services.generator.email_generator import generate_email
from services.generator.employee_generator import generate_length_of_work
from services.generator.job_generator import create_job
from services.generator.person_generator import (
    generate_sex,
    generate_full_name,
    generate_birthdate,
)
from services.generator.phone_generator import generate_phone_number
from services.generator.salary_generator import generate_salary_payments_for_year
from services.utils import transliterate_word


def make_employee(
    abstract_person: AbstractPerson,
) -> tuple[AbstractEmployee, list[SalaryPayment]]:
    job = create_job(abstract_person.address, abstract_person.type_populated_area)
    length_of_work = generate_length_of_work(abstract_person.birthdate)
    contract_payment = calculate_contract_payment(
        populate_area_type=abstract_person.type_populated_area,
        qualification=job.qualification,
        job_name=job.name,
        employee_stage=length_of_work,
    )
    # print(contract_payment)

    employee = AbstractEmployee(
        job=job,
        length_of_work=length_of_work,
        contract_payment=contract_payment,
        **abstract_person.__dict__,
    )

    year_salary = generate_salary_payments_for_year(employee)

    return employee, year_salary


def make_abstract_person(id: int):
    sex = generate_sex()
    full_name: dict[str, str] = generate_full_name(gender=sex)

    birthdate = generate_birthdate()
    person_full_name = f"{full_name['first_name']} {full_name['last_name']}"

    email_address = generate_email(
        person_full_name=person_full_name, person_birthdate=birthdate
    )
    credit_card = generate_credit_data(person_full_name)
    phone_number = generate_phone_number()

    address_dict: dict = create_address()

    return AbstractPerson(
        id=id,
        sex=sex,
        first_name=full_name["first_name"],
        first_name_eng_lang=transliterate_word(full_name["first_name"]),
        middle_name=full_name["middle_name"],
        middle_name_eng_lang=transliterate_word(full_name["middle_name"]),
        second_name=full_name["last_name"],
        second_name_eng_lang=transliterate_word(full_name["last_name"]),
        email_address=email_address,
        credit_card=credit_card,
        birthdate=birthdate,
        address=address_dict["ukr_name"],
        address_eng_lang=address_dict["eng_name"],
        type_populated_area=address_dict["category"],
        phone_number=phone_number,
    )


class GeneratorPersonService:
    def __init__(self, person_cls: type[AbstractPerson] = AbstractPerson):
        self.person_cls = person_cls

    def make_person(self, id: int) -> tuple[AbstractEmployee, list[SalaryPayment]]:
        person = make_abstract_person(id=id)
        salary = None
        if self.person_cls == AbstractEmployee:
            person, salary = make_employee(person)
        return person, salary


def generate_persons(count: int, person_cls: type[AbstractPerson] = AbstractPerson):
    persons_list = []
    salary_payments_list = []

    generator_person_service = GeneratorPersonService(person_cls=person_cls)
    bar = ShadyBar(message=f"Create {person_cls.__name__}'s...", max=count)
    for i in range(1, count + 1):
        person, salary = generator_person_service.make_person(i)
        persons_list.append(person)
        if salary is not None:
            salary_payments_list.append(salary)
        bar.next()
    bar.finish()
    return persons_list, salary_payments_list


if __name__ == "__main__":
    print(generate_persons(count=5, person_cls=AbstractEmployee))
