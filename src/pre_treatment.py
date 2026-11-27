from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CITIES_FILE = ROOT / "data" / "cities_51largest.csv"
REGIONS_FILE = ROOT / "data" / "administrative_regions.csv"


def load(path):
    return pd.read_csv(path, index_col=0)


def capital_of_each_region(regions, cities):
    """Index (dans cities) de la capitale de chaque région, par coordonnées les plus proches."""
    capitals = cities[cities["admin_centre"]]
    d = (regions["latitude"].values[:, None] - capitals["latitude"].values[None, :]) ** 2 + (
        regions["longitude"].values[:, None] - capitals["longitude"].values[None, :]
    ) ** 2
    idx = capitals.index.values[d.argmin(axis=1)]
    if len(set(idx)) != len(idx):
        raise ValueError("Deux régions correspondent à la même capitale.")
    return pd.Series(idx, index=regions.index)


def provinces(path_cities=CITIES_FILE, path_regions=REGIONS_FILE):
    """
    DataFrame indexé par région avec :
        latitude, longitude : coordonnées de la capitale
        capital_city        : index de la capitale dans le CSV des villes
        population_est      : population totale de la province
    """
    regions = load(path_regions)
    cities = load(path_cities)

    df = regions[["latitude", "longitude", "population_est"]].copy()
    df["capital_city"] = capital_of_each_region(regions, cities)
    df.index.name = "region"
    return df[["latitude", "longitude", "capital_city", "population_est"]]


if __name__ == "__main__":
    df = provinces()
    print(df.to_string())
    print(f"\nPopulation totale : {df['population_est'].sum()}")
