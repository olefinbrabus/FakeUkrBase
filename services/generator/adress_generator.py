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
    "київ": "capital",
}

CATEGORY_WEIGHTS = {
    "village": 0.40,
    "urban_settlement": 0.20,
    "city": 0.35,
    "capital": 0.05,
}


def normalize_populated_areas_by_type(raw_string: str) -> str:
    return TYPE_MAP.get(raw_string.strip().lower(), "unknown")


def read_ukrainian_populated_areas() -> pd.DataFrame:
    try:
        places_dataframe = pd.read_excel(UKRAINE_DATA, sheet_name="Populated Places")
    except FileNotFoundError:
        click.echo("you have to install the ukr-populated-places.xlsx")
        raise

    places_dataframe["category"] = (
        places_dataframe["TYPE_UK"].astype(str).apply(normalize_populated_areas_by_type)
    )

    places_dataframe = places_dataframe[places_dataframe["category"] != "unknown"]

    return places_dataframe


class PopulatedAreaFrameManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._frame: pd.DataFrame = read_ukrainian_populated_areas()
            self._frames_by_category: dict[str, pd.DataFrame] = {}
            for cat in self._frame["category"].unique():
                self._frames_by_category[cat] = self._frame[
                    self._frame["category"] == cat
                ].reset_index(drop=True)
            self._initialized = True

    @property
    def frame(self) -> pd.DataFrame:
        return self._frame

    @property
    def frames_by_category(self) -> dict[str, pd.DataFrame]:
        return self._frames_by_category


def _choose_category() -> str:
    categories = list(CATEGORY_WEIGHTS.keys())
    weights = [CATEGORY_WEIGHTS[c] for c in categories]
    return base_random.choices(categories, weights=weights, k=1)[0]


def create_address() -> dict:
    manager = PopulatedAreaFrameManager()
    frames_by_category = manager.frames_by_category

    category = _choose_category()

    df_cat = frames_by_category.get(category)
    if df_cat is None or df_cat.empty:
        df_cat = manager.frame

    row = df_cat.sample(
        n=1,
        random_state=base_random.randint(1, 10**9),
    ).iloc[0]

    return {
        "eng_name": row["ADM4_EN"],
        "ukr_name": row["ADM4_UK"],
        "category": row["category"],  # уже нормализованный тип
    }


if __name__ == "__main__":
    for _ in range(10):
        print(create_address())
