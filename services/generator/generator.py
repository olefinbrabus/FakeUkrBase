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
) -> AbstractEmployee:
    job = create_job(abstract_person.address, abstract_person.type_populated_area)
    length_of_work = generate_length_of_work(abstract_person.birthdate)
    contract_payment = calculate_contract_payment(
        populate_area_type=abstract_person.type_populated_area,
        qualification=job.qualification,
        job_name=job.name,
        employee_stage=length_of_work,
    )

    employee = AbstractEmployee(
        job=job,
        length_of_work=length_of_work,
        contract_payment=contract_payment,
        **abstract_person.__dict__,
    )

    return employee

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

    def make_person(self, id: int) -> AbstractEmployee:
        person = make_abstract_person(id=id)
        if issubclass(self.person_cls, AbstractEmployee):
            person = make_employee(person)
        return person


def generate_year_salaries_per_each_employee(employee_list: list[AbstractEmployee]) -> list[list[SalaryPayment]]:
    salaries_per_employee_list: list[list[SalaryPayment]] = []
    bar = ShadyBar(message=f"Create salaries's...", max=len(employee_list))
    for employee in employee_list:
        employee_salary = generate_salary_payments_for_year(employee)
        salaries_per_employee_list.append(employee_salary)
        bar.next()
    bar.finish()
    return salaries_per_employee_list


def generate_persons(count: int, person_cls: type[AbstractPerson] = AbstractPerson):
    persons_list = []

    generator_person_service = GeneratorPersonService(person_cls=person_cls)
    bar = ShadyBar(message=f"Create {person_cls.__name__}'s...", max=count)
    for i in range(1, count + 1):
        person = generator_person_service.make_person(i)
        persons_list.append(person)
        bar.next()
    bar.finish()
    return persons_list
