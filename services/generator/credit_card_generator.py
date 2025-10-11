from config import fake
from services.utils import transliterate_word


def generate_credit_data(person) -> str:
    card_data = fake.credit_card_full()
    card_data = card_data.replace("\n", "\\")
    first_index_slash_name = card_data.index("\\")
    second_index_slash_name = card_data.index("\\", first_index_slash_name + 1)
    eng_full_name = transliterate_word(person.full_name)
    card_data = (
        card_data[: first_index_slash_name + 1]
        + eng_full_name
        + card_data[second_index_slash_name:]
    )
    return card_data
