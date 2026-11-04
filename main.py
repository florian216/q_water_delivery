"""
This module loads data, creates edges, and generates QUBO matrices.

1) Data loading
Load data from CSV files.
Each file contains GPS coordinates and population estimates of:
    - The 51 largest cities of the territory (cities_51largest.csv)
    - The 11 administrative regions of the territory (administrative_regions.csv)

In the following, the term "cities" can refer to either one of the 51 cities or to the 
administrative center of a region, depending on context.

2) Processing
- Generate edges between cities. The edges are either:
    - Hard-coded for the 11 regions dataset
    - Generated based on distance between pairs of cities (51 cities dataset)
- Generate QUBO matrices from the cities and edges.
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path
from plot_graphs import plot

# Paths to CSV files
CITIES_FILE = "cities_51largest.csv"
GOVTS_FILE = "administrative_regions.csv"


def load(fname):
    """
    Load a CSV file and return a pandas DataFrame.
    """
    path = os.path.join(os.getcwd(), fname)
    with open(path, "r") as f:
        df = pd.read_csv(f)
    return df


def gen_edges(df, degree):
    """
    Generate edges between nearest neighbours with fixed degreee Δ.

    For each city:
        1) Compute distance to all other cities
        2) Keep the Δ nearest neighbours
    """

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


def gen_qubo(_edges, name, weights=None, n=None):
    """
    Generate a QUBO matrix from a list of edges.

    Note:
    - Mapping edges -> QUBO is problem-dependent if weights are not provided.
    - QUBO -> spins mapping is intentionally omitted.
    """

    if n is None:
        n = 1 + max(max(edge) for edge in _edges)

    edges = [e for e in _edges if max(e) < n]

    Q = np.zeros((n, n))

    if weights is None:
        for edge in edges:
            Q[*edge] = 1.0
        Q += Q.T
    else:
        for edge in edges:
            Q[*edge] = 1.0

    Q += np.eye(n)

    output_path = os.path.join(os.getcwd(), f"qubos/qubo_{name}_{n}.json")
    with open(output_path, "w") as f:
        np.savetxt(f, Q)


# -------------------------
# Main execution
# -------------------------
if __name__ == "__main__":
    # Create the output directories if they do not exist
    Path("qubos").mkdir(parents=True, exist_ok=True)
    Path("plots").mkdir(parents=True, exist_ok=True)

    # Load data
    df_cities = load(CITIES_FILE)
    df_govts = load(GOVTS_FILE)

    # Define edges
    govt_edges = [
        (0, 1), (0, 5), (1, 3), (1, 10), (2, 4), (2, 6), (2, 8), (2, 9),
        (3, 5), (3, 8), (3, 10), (4, 6), (4, 9), (6, 7), (7, 8), (8, 10)
    ]

    city_edges = gen_edges(df_cities, degree=5)

    # Generate QUBO matrices
    for n in range(2, 12):
        gen_qubo(govt_edges, "regions", n=n)

    for n in range(2, 52):
        gen_qubo(city_edges, "cities", n=n)

    # Plot graphs
    for n in range(1 + len(df_govts)):
        plot(
            df_govts,
            n,
            govt_edges=govt_edges,
            scale=1e3,
            fname="plots/administrative_regions"
        )

    for n in range(1 + len(df_cities)):
        plot(
            df_cities,
            n,
            city_edges=city_edges,
            scale=500,
            fname="plots/cities"
            )
