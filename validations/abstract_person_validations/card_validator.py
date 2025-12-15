from luhncheck import is_luhn

from core import CreditCard


def validate_card(
    credit_card: CreditCard, first_name_eng_lang: str, second_name_eng_lang: str
) -> bool:
    return is_valid_luna(credit_card.number) and is_name_person_valid_in_card(
        card_name=credit_card.person_full_name,
        first_name_eng_lang=first_name_eng_lang,
        second_name_eng_lang=second_name_eng_lang,
    )


def is_valid_luna(card_number: str) -> bool:
    return is_luhn(card_number)


def is_name_person_valid_in_card(
    card_name: str, first_name_eng_lang: str, second_name_eng_lang: str
) -> bool:
    return f"{first_name_eng_lang} {second_name_eng_lang}" == card_name
