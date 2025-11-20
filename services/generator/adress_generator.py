import click
import pandas as pd

from config import UKRAINE_DATA, base_random

TYPE_MAP = {
        "село": "village",
        "с.": "village",
        "смт": "urban_settlement",
        "селище міського типу": "urban_settlement",
        "селище": "urban_settlement",
        "місто": "city",
        "м.": "city",
        "Київ": "capital",
}

def create_address():
    places_dataframe: pd.DataFrame

    try:
        places_dataframe = pd.read_excel(UKRAINE_DATA, sheet_name="Populated Places")
    except FileNotFoundError:
        click.echo("you have to install the ukr-populated-places.xlsx")
        raise

    # places_dataframe["populated_areas_category"] = places_dataframe["TYPE_UK"].apply(normalize_populated_areas_by_type)
    populate_area = places_dataframe.sample(n=1, random_state=base_random.randint(1,1000)).to_dict(orient="records")[0]
    return {
        "eng_name": populate_area["ADM4_EN"],
        "ukr_name": populate_area["ADM4_UK"],
        "category": normalize_populated_areas_by_type(str(populate_area["TYPE_UK"])),
    }

def normalize_populated_areas_by_type(raw_string: str):
    return TYPE_MAP.get(raw_string.strip().lower(), "unknown")





if __name__ == '__main__':
    print(create_address())
