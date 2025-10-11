from datetime import date
from decimal import Decimal

from phonenumbers.phonenumber import PhoneNumber
from pydantic import BaseModel, EmailStr, Field, ConfigDict, with_config
from pydantic_extra_types.payment import PaymentCardNumber

from core.countries_data.enums import ExtendedPaymentCardBrand, TypeCreditCard


class ConfigModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class CreditCard(ConfigModel):
    person_full_name: str
    number: PaymentCardNumber
    type: TypeCreditCard
    date_expired: date
    brand: ExtendedPaymentCardBrand
    cvv: str = Field(pattern=r"/^[0-9]{3,4}/")
    currency: str = Field(default="USD")
    amount: Decimal = Field(default=Decimal("0.00"))


class AbstractPerson(ConfigModel):

    id: int
    first_name: str
    first_name_county_lang: str
    second_name: str
    second_name_county_lang: str
    third_name: str
    third_name_county_lang: str
    email_address: EmailStr
    address: str
    birthdate: date
    phone_number: PhoneNumber
    credit_card: CreditCard
    # future features for better analyse
    # salary: float = None
    # amount_of_violation: int = None

    def __str__(self):
        return f"""
        first_name: {self.first_name}\nsecond_name: {self.second_name}\nthird_name: {self.third_name}
        email: {self.email}\nphone_number: {self.phone_number}\naddress: {self.address}
        \nbirthdate: {self.birthdate}

"""


class AbstractEmployee(AbstractPerson):

    working_address: str
    working_email_address: EmailStr
    working_phone_number: PhoneNumber
    working_credit_card: CreditCard
