#Meme code que main.py pour generer le graph (A clean)
import os
import numpy as np
import pandas as pd
from pathlib import Path
import random

# Paths to CSV files
CITIES_FILE = "data/cities_51largest.csv"
GOVTS_FILE = "data/administrative_regions.csv"

def load(fname):
    path = os.path.join(os.getcwd(), fname)
    with open(path, "r") as f:
        df = pd.read_csv(f)
    return df


def gen_edges(df, degree):
    longitudes = df["longitude"]
    latitudes = df["latitude"]
    n = len(latitudes)

    all_edges = []

    for city1 in range(n):
        x1, y1 = longitudes[city1], latitudes[city1]

        distances = []
        edges = []

        for city2 in range(n):
            if city1 == city2:
                continue

            x2, y2 = longitudes[city2], latitudes[city2]
            dist = (x1 - x2) ** 2 + (y1 - y2) ** 2

            distances.append(dist)
            edges.append((city2, city1))  # ordering matters

        idx = np.argsort(distances)

        for i in range(degree):
            all_edges.append(edges[idx[i]])

    return all_edges

if __name__ == "__main__":
    Path("qubos").mkdir(parents=True, exist_ok=True)
    Path("plots").mkdir(parents=True, exist_ok=True)

    df_cities = load(CITIES_FILE)
    df_govts = load(GOVTS_FILE)

    govt_edges = [
        (0, 1), (0, 5), (1, 3), (1, 10), (2, 4), (2, 6), (2, 8), (2, 9),
        (3, 5), (3, 8), (3, 10), (4, 6), (4, 9), (6, 7), (7, 8), (8, 10)
    ]

    city_edges = gen_edges(df_cities, degree=5)

    #### FIN MAIN.PY ####

    print(city_edges)

    #On a 50 noeuds
    n=50

    #On tire les generateurs (10 sur 50)
    generateurs = random.sample(range(1,n+1), 10)
    print(sorted(generateurs))

    #Consommations 