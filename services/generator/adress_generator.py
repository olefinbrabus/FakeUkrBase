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

class PopulatedAreaFrameManager:
    _instance = None
    _frame = None


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

    @property
    def frame(self):
        if self._frame is None:
            self._frame = read_ukrainian_populated_areas()
        return self._frame



def read_ukrainian_populated_areas():
    try:
        places_dataframe = pd.read_excel(UKRAINE_DATA, sheet_name="Populated Places")
    except FileNotFoundError:
        click.echo("you have to install the ukr-populated-places.xlsx")
        raise
    return places_dataframe





def create_address():
    frame_manager = PopulatedAreaFrameManager()
    places_dataframe: pd.DataFrame = frame_manager.frame
    # places_dataframe["populated_areas_category"] = places_dataframe["TYPE_UK"].apply(normalize_populated_areas_by_type)
    populate_area = places_dataframe.sample(
        n=1, random_state=base_random.randint(1, 1000)
    ).to_dict(orient="records")[0]
    return {
        "eng_name": populate_area["ADM4_EN"],
        "ukr_name": populate_area["ADM4_UK"],
        "category": normalize_populated_areas_by_type(str(populate_area["TYPE_UK"])),
    }


def normalize_populated_areas_by_type(raw_string: str):
    return TYPE_MAP.get(raw_string.strip().lower(), "unknown")


if __name__ == "__main__":
    for _ in range(10):
        print(create_address())
