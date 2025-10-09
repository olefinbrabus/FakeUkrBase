from datetime import date

from phonenumbers.phonenumber import PhoneNumber
from pydantic import BaseModel, EmailStr


class AbstractPerson(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    id: int
    first_name: str
    second_name: str
    third_name: str
    email: EmailStr
    phone_number: PhoneNumber
    address: str
    birthdate: date

    def __str__(self):
        return f"""
        first_name: {self.first_name}\nsecond_name: {self.second_name}\nthird_name: {self.third_name}
        email: {self.email}\nphone_number: {self.phone_number}\naddress: {self.address}
        \nbirthdate: {self.birthdate}
        
"""
