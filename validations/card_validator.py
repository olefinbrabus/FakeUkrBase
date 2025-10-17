from luhncheck import is_luhn


def is_valid_luna(card_number: str) -> bool:
    return is_luhn(card_number)
