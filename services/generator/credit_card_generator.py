from datetime import date, datetime
from decimal import Decimal

from pydantic_extra_types.payment import PaymentCardNumber

from config import fake, base_random
from core.countries_data.enums import ExtendedPaymentCardBrand, TypeCreditCard
from services.utils import transliterate_word
from core.models import CreditCard



def generate_credit_data(person_full_name: str) -> CreditCard:
    number = PaymentCardNumber(fake.credit_card_number())
    brand: ExtendedPaymentCardBrand = _generate_brand()
    cvv = base_random.randint(15,979)
    date_expired = date.today()
    person_full_name = transliterate_word(person_full_name)
    amount = Decimal(base_random.randint(1,1_000_000) + base_random.randint(1, 99)) / 100
    """for future currency have to been calculate by formula with social rating"""
    type_card = _generate_type()
    print(date_expired)



    # card_data = card_data.replace("\n", "\\")
    # first_index_slash_name = card_data.index("\\")
    # second_index_slash_name = card_data.index("\\", first_index_slash_name + 1)
    # eng_full_name = transliterate_word(person_full_name)
    # card_data = (
    #     card_data[: first_index_slash_name + 1]
    #     + eng_full_name
    #     + card_data[second_index_slash_name:]
    # )
    card = CreditCard(
        number=number,
        brand=brand,
        cvv=cvv,
        date_expired=date_expired,
        person_full_name=person_full_name,
        amount=amount,
        type=type_card
    )
    return card

def _generate_type() -> TypeCreditCard:
    return base_random.choice((TypeCreditCard.credit, TypeCreditCard.debit))

def _generate_brand() -> ExtendedPaymentCardBrand:
    brand = fake.credit_card_provider()
    if brand == "ПРОСТІР":
        brand = ExtendedPaymentCardBrand.prostir
    brand = ExtendedPaymentCardBrand(brand)
    return brand

def _generate_date_expire() -> date:
    date_string = fake.credit_card_expire(start="-3y", end="+4y")
    print(date_string)
    valid_date_string = date_string[:2] + "-20" + date_string[3:5]
    print(valid_date_string)



    date_expire: date = datetime.strptime( valid_date_string + "-01", "%m-%Y-%d")

    return date_expire

# print(generate_credit_data("Mykola Zhunichuk"))
print(_generate_date_expire())