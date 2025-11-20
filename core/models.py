from datetime import date
from decimal import Decimal

from mimesis import Gender
from phonenumbers.phonenumber import PhoneNumber
from pydantic import BaseModel, EmailStr, Field, ConfigDict
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
    average_payment: Decimal = Field(default=Decimal("0.00"))


class AbstractPerson(ConfigModel):

    id: int
    sex: Gender
    first_name: str
    first_name_eng_lang: str
    middle_name: str
    middle_name_eng_lang: str
    second_name: str
    second_name_eng_lang: str
    email_address: EmailStr
    address: str
    birthdate: date
    phone_number: PhoneNumber
    credit_card: CreditCard
    # future features for better analyse
    # salary: float = None
    # amount_of_violation: int = None


class AbstractEmployee(AbstractPerson):

    job_type: str
    working_address: str
    working_email_address: EmailStr
    working_phone_number: PhoneNumber | None = None
