from transliterate import translit


def transliterate_word(ukrainian_word: str) -> str:
    return translit(ukrainian_word, "uk", reversed=True)
