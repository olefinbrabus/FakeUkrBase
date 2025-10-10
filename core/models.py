from datetime import date

from phonenumbers.phonenumber import PhoneNumber
from pydantic import BaseModel, EmailStr, Field, ConfigDict, with_config
from pydantic_extra_types.payment import PaymentCardNumber, PaymentCardBrand

@with_config(ConfigDict(arbitrary_types_allowed=True))
class ConfigModel(BaseModel):
    pass


class CreditCard(ConfigModel):
    credit_number: PaymentCardNumber
    type_credit_card: str
    date_expired: date
    card_brand: PaymentCardBrand
    cvv: str = Field(pattern=r'^\d{4}-\d{3}-\d{3}-\d{4}$')


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





print(AbstractPerson.__subclasses__())
