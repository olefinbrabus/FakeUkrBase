from luhncheck import is_luhn

from services.utils import transliterate_word


def is_valid_luna(card_number: str) -> bool:
    return is_luhn(card_number)


def is_name_person_valid_in_card(
    first_name: str, last_name: str, card_name: str
) -> bool:
    return (
        f"{transliterate_word(first_name)} {transliterate_word(last_name)}" == card_name
    )
