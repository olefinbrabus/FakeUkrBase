from datetime import date
from decimal import Decimal

from mimesis import Gender
from phonenumbers.phonenumber import PhoneNumber
from pydantic import BaseModel, EmailStr, Field, ConfigDict, PositiveInt
from pydantic_extra_types.payment import PaymentCardNumber


from core.enums import ExtendedPaymentCardBrand, TypeCreditCard, QualificationType


class ConfigModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class CreditCard(ConfigModel):
    person_full_name: str
    number: PaymentCardNumber
    type: TypeCreditCard
    date_expired: date
    brand: ExtendedPaymentCardBrand
    cvv: str = Field(pattern=r"^\d{3,4}$")
    currency: str = Field(default="USD")
    amount: Decimal = Field(default=Decimal("0.00"))


class Job(ConfigModel):
    name: str
    qualification: QualificationType
    address: str | None


class SalaryPayment(ConfigModel):
    month: date
    gross_amount: Decimal
    net_amount: Decimal | None = None
    bonus_amount: Decimal = Field(default=Decimal("0.00"))
    penalty_amount: Decimal = Field(default=Decimal("0.00"))
    is_delayed: bool = False
    delay_days: int = 0

    pay_date: date | None = None


class AbstractPerson(ConfigModel):

    id: PositiveInt
    sex: Gender
    first_name: str
    first_name_eng_lang: str
    middle_name: str
    middle_name_eng_lang: str
    second_name: str
    second_name_eng_lang: str
    email_address: EmailStr
    address: str
    address_eng_lang: str
    type_populated_area: str
    birthdate: date
    phone_number: PhoneNumber
    credit_card: CreditCard
    # future features for better analyze
    # amount_of_violation: int = None


class AbstractEmployee(AbstractPerson):

    job: Job
    length_of_work: PositiveInt
    working_email_address: EmailStr | None = None
    working_phone_number: PhoneNumber | None = None
    contract_payment: Decimal = Field(default=Decimal("0.00"))
